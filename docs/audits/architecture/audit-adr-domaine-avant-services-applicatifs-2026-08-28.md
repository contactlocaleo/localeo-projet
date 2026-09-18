# Audit de conformité à l'ADR « domaine avant services applicatifs »

Date : 28 août 2026

Périmètre : backend Localeo, analyse statique de `app/application` et confrontation avec
`app/domaine`

ADR de référence : `ADR-2026-08-28-domaine-avant-services-applicatifs.md`

## Conclusion

La dérive est réelle mais encore maîtrisable. Le domaine n'est pas uniformément anémique : plusieurs
entités protègent déjà correctement leurs transitions (`Animation.publier`, demande de participation,
opération Animation, email et SMS sortants). En revanche, les règles ajoutées au rythme des Epics se sont
accumulées plus vite dans les services applicatifs que dans les agrégats, particulièrement pour Animation,
les achats et l'exploitation.

Une réécriture globale n'est ni nécessaire ni souhaitable. Le bon point d'intervention est maintenant :
figer la dérive, puis extraire les règles par parcours métier complet, avec des tests de caractérisation.

## Méthode et limites

L'inventaire porte sur 186 fichiers Python de la couche application, dont 153 non vides :

- 58 fichiers placés dans un répertoire `services` ;
- 67 fichiers applicatifs lèvent au moins une exception dont le nom signale une décision métier ;
- 49 fichiers applicatifs modifient directement un attribut `statut` ;
- 42 fichiers applicatifs importent directement les modèles ORM de persistance.

Ces nombres sont des signaux de recherche, pas autant de violations. Une projection de lecture peut
légitimement filtrer des statuts et un cas d'usage doit légitimement charger et sauvegarder. Chaque candidat
a donc été qualifié selon cette question : la règle doit-elle rester vraie depuis tous les points d'entrée ?

## Écarts prioritaires

| Priorité | Parcours | Indice observé | Écart à corriger | Cible proposée |
| --- | --- | --- | --- | --- |
| P0 | Commandes de lots Animation | `animation_locale/services/commandes_lots.py` concentre 28 décisions signalées et 13 mutations de statut | Cycle de commande, paiement, expiration, remboursement et réconciliation distribués dans l'application | Enrichir `CommandeAchat` avec des commandes métier explicites et centraliser la matrice de transitions |
| P0 | Paiement des commandes de lots | `gestion_achats/use_cases/valider_paiement_commande_lots.py` concentre 19 décisions signalées et 12 mutations | Le webhook décide et applique directement plusieurs transitions métier | Faire traduire Stripe en faits techniques, puis appliquer ces faits à `CommandeAchat` dans le domaine |
| P0 | Participation des commerçants | `animation_locale/services/demandes_participation_commercants.py` concentre 15 décisions signalées et 16 mutations | Une partie du cycle est dans l'entité, une autre reste dans le service | Achever le déplacement dans `DemandeParticipationCommercantAnimation` et un service de domaine d'éligibilité |
| P0 | Cycle de vie Animation | `gestion_animations.py`, `publication_animation.py`, `synchronisation_statuts_animation.py` | `Animation` ne protège actuellement que `publier`; dates, démarrage, clôture, annulation et modification restent dispersés | Faire de `Animation` la source unique de la matrice de transitions et de la cohérence temporelle |
| P1 | Tirage et gains | `animation_locale/services/tirages_animation.py` concentre 11 décisions et 11 mutations | `TirageAnimation` et `GainAnimation` portent surtout des données | Ajouter gel de population, tirage, attribution et envoi du gain comme comportements métier |
| P1 | Validation des prestations | `exploitation/use_cases/annuler_validation_prestation.py` et `service_validation_prestation.py` | L'entité `ValidationPrestation` ne porte aucun comportement alors que les cas d'usage protègent le cycle | Introduire les transitions de validation, annulation, signalement et correction dans l'agrégat concerné |
| P1 | Achat de coffret | `gestion_achats/use_cases/valider_paiement.py` modifie directement l'achat et matérialise les instances | `AchatCoffret` ne protège ni paiement confirmé/échoué ni idempotence fonctionnelle | Ajouter les transitions de paiement à `AchatCoffret`; conserver la matérialisation et les effets dans l'application |
| P1 | Actualités Animation | `animation_locale/services/actualites_animation.py` concentre 16 décisions | Statuts éditoriaux, publication, masquage et expiration n'ont pas de modèle de domaine dédié | Créer une entité `ActualiteAnimation` comportementale |
| P2 | Profils commerçants | `profils/services/service_profils_commercants.py` concentre 15 décisions | Validation/publication et cohérence du profil sont pilotées par un service | Enrichir l'agrégat profil lors de la prochaine évolution fonctionnelle |
| P2 | Référencement et Stripe Connect | `referencement/use_cases/stripe_connect_onboarding.py` mêle états métier et états fournisseur | La traduction des états Stripe et la décision d'activation sont proches | Isoler un fait fournisseur, puis laisser le commerçant décider sa transition métier |
| P2 | Documentaire et support | Plusieurs contrôles sont dans des services applicatifs | Mélange de validations techniques et métier, mais risque immédiat moindre | Traiter au fil des évolutions, après les parcours financiers et Animation |

## Ce qui n'est pas un écart

Restent dans la couche application :

- transaction, Unit of Work, chargement et persistance ;
- contrôle du tenant, des habilitations et du point d'entrée ;
- idempotence technique, audit, outbox et déclenchement des notifications ;
- projections de lecture, tableaux de bord et Vision 360 ;
- traduction d'un événement Stripe, sans décision sur la transition métier ;
- stockage documentaire et orchestration de la génération d'un flyer.

Restent dans l'infrastructure : SQLAlchemy, Stripe, email, webpush, fichiers, QR, PDF et PNG.

## Premier refactoring appliqué : flyer Animation

La nouvelle version du flyer sert de tranche pilote conforme à l'ADR :

- `ContenuFlyerAnimation` construit un contenu cohérent, valide l'URL et la période, puis fige les libellés
  métier ;
- `ServiceFlyerAnimation` charge le contexte et orchestre la génération et le stockage ;
- `FlyerAnimationRenderer` ne réalise que la composition graphique PDF/PNG ;
- les tests sont séparés entre domaine, application et infrastructure.

Le choix éditorial « faire scanner le QR chez le commerçant » n'est ainsi ni caché dans ReportLab ni
recalculé par le cas d'usage.

## État de réalisation

Première tranche mise en œuvre le 28 août 2026 :

- `Animation` protège désormais modification, publication, démarrage, clôture, suppression, disponibilité
  du flyer et autorisation du tirage ;
- `CommandeAchat` protège le paiement, l'expiration, la réconciliation, la matérialisation des instances et
  le remboursement ;
- `DemandeParticipationCommercantAnimation` protège aussi le changement d'échéance, la sortie du cycle
  courant et la décision sur une demande de retrait ;
- `PopulationEligibleAnimation`, `GainAnimation` et `ParticipantAnimation` protègent la sélection du tirage,
  le remplacement et l'envoi des gains ainsi que le passage au statut gagnant ;
- `AchatCoffret` protège désormais la confirmation, l'échec et la réconciliation du paiement ;
- le cycle de validation des prestations est porté par `ValidationPrestation`,
  `StatutPrestationCoffretInstance`, `CoffretInstance`, `TransactionValidation` et le mouvement de
  reversement associé ;
- une politique de domaine centralise la mission, les échéances, les acceptations et le snapshot des
  commerçants nécessaires à la publication d'une Animation ;
- `ActualiteAnimation` protège les statuts éditoriaux, la programmation, la publication, le masquage,
  l'expiration et la suppression ;
- `ProfilCommercant` et `VersionProfilCommercant` protègent la proposition, la soumission, la modération,
  les vérifications, la publication et le masquage ;
- Stripe Connect est traduit en `FaitCompteStripeConnect`, puis `Commercant` décide de son éligibilité et
  de son statut d'onboarding ;
- `PaiementReversement`, `Reversement` et `ExecutionBatch` protègent leurs transitions opérationnelles ;
- `AlerteVirementBancaire` protège la redétection et la résolution des alertes Stripe ;
- `ActualiteEditoriale` porte le cycle éditorial des actualités génériques de Localeo Live ;
- `Document` protège la publication, l'archivage et l'éligibilité d'une version HTML publique ;
- `MessageContact`, `MotifContact` et `AchatCoffret` portent désormais les invariants support relatifs au
  contenu, à la compatibilité d'un motif et à l'éligibilité d'un remboursement ;
- les services conservent le chargement, les transactions, Stripe, les notifications, l'audit et la
  persistance ;
- un contrat d'architecture interdit de réintroduire une affectation directe de statut pour ces agrégats
  dans les services migrés.

La dette recensée dans cet audit est traitée, y compris les compléments documentaire, support, actualités
génériques et alertes de virement. Les appels à `datetime.utcnow`, dépréciés par la version de Python utilisée,
ont également été supprimés des applications, tests et valeurs par défaut SQLAlchemy.

Les affectations ORM qui subsistent sont des opérations explicites de mapping entre entité métier et modèle de
persistance, ou des états purement techniques de files d'envoi. Elles ne constituent pas une règle métier
concurrente. Toute nouvelle transition métier doit continuer à être ajoutée au domaine et au contrat
d'architecture.

## Plan de remise en conformité

### Étape 0 — éviter une nouvelle dérive

- Exiger dans chaque conception d'Epic la liste des agrégats, invariants et transitions modifiés.
- Exiger un test de domaine autonome pour chaque règle valable quel que soit le point d'entrée.
- Refuser toute nouvelle mutation directe de statut dans l'application lorsqu'une entité domaine existe.
- Conserver le contrôle automatisé interdisant au domaine de dépendre de l'application ou de
  l'infrastructure (`tests/architecture/test_module_contracts.py`).

### Étape 1 — sécuriser le cycle Animation

1. Écrire des tests de caractérisation de la publication, du passage en cours, de la clôture et de
   l'annulation.
2. Ajouter les comportements à `Animation`, avec une horloge fournie en paramètre.
3. Remplacer progressivement les affectations de statut dans les services par ces comportements.
4. Conserver notifications, audit et persistance dans les cas d'usage.

### Étape 2 — traiter participation, lots et gains

Procéder verticalement : une transition et tous ses points d'entrée à la fois. Commencer par la commande de
lots, car elle combine le plus grand nombre de décisions et un risque financier. Poursuivre avec les demandes
de participation, puis le tirage et les gains.

### Étape 3 — achats et exploitation

Déplacer les transitions de paiement dans `AchatCoffret` et `CommandeAchat`, puis le cycle de validation dans
un agrégat exploitation. Les callbacks fournisseur deviennent des adaptateurs de faits et ne modifient plus
directement les statuts.

### Étape 4 — dette opportuniste — réalisée

Profils, référencement, documentaire et support ont été remis en conformité pour les invariants identifiés.
Une limite de taille ou de nombre de services reste un mauvais indicateur : le critère est la propriété des
invariants.

## Stratégie de livraison

Chaque refactoring doit conserver le comportement observable et tenir dans un commit autonome :

1. tests de caractérisation ;
2. ajout du comportement domaine et de ses tests ;
3. remplacement de l'ancienne décision applicative ;
4. suppression de la règle dupliquée ;
5. tests ciblés, contrats d'architecture, puis suite complète.

La première séquence recommandée est le cycle de vie `Animation`, avant toute nouvelle extension de
l'Epic 41. Elle est plus petite que la commande de lots et permettra de valider la méthode de migration sans
risque financier direct.
