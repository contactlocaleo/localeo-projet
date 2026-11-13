# Backlog Epic 55 - Moteur commun et chasse au tresor commercante

## Suivi

- Criticite : `Moyenne`.
- Statut : `En cours - bilans T1–T6 conservés ; évolution issue de l'audit du 13 novembre 2026 à implémenter ; conversion sur cible, pilote et ouverture à mener`.
- Catalogue V1 : `PASSEPORT_COMMERCANT`, `TOMBOLA_LOCALE`, `CHASSE_TRESOR_COMMERCANTE`.
- Dependances : Epics 41, 42, 46, 47 et 49.

La [specification detaillee unique](../../specifications/moteur-animation/localeo_animation_engine_spec.md) porte les regles, les decisions, les contrats proposes et la recette. Cette fiche conserve uniquement le suivi de livraison.

## Lot de conception technique

- [x] Dossier de conception couvrant contrats, persistance, concurrence, API/droits, médias et exploitation, établi à partir du code et relu le 19 septembre 2026 : [référence technique V1](../../specifications/moteur-animation/conception-technique.md).
- [x] Implémenter les lots T1–T6 et exécuter les contrôles techniques locaux ; preuves et limites dans le suivi.
- [ ] Achever les critères d’ouverture T6 : conversion sur cible, pilote humain, contrôle d’exploitation et déploiement coordonné.

Compte rendu par lot, décisions et preuves : [suivi d’implémentation](../../specifications/moteur-animation/suivi-implementation.md). Les cases cochées correspondent au code livré et vérifié localement, avec preuves par lot. Les opérations sur cible, le pilote et les droits ERP non accordés restent explicitement ouverts ; aucun déploiement n’est implicite.

## Livraison proposee

Organisation retenue : socle minimal puis développement par parcours complets associant domaine, API et interfaces ; les trois moteurs restent dans la livraison. Recette progressive pendant la réalisation, puis complète avant ouverture (TRE-ARB-81/TRE-ARB-82).

- [x] Modele Animation generique : inscription, periode, territoire, publication et participation.
- [x] Permissions par action regroupées en profils prêts à l’emploi, contrôles serveur et périmètres partenaire/animation ; mapping aux habilitations existantes (TRE-ARB-68).
- [x] Verrou par participation et coordination des opérations globales au niveau animation ; ordre/protocole physique et scénarios de concurrence vérifiés sur PostgreSQL jetable (TRE-ARB-69).
- [x] Préparation guidée avec sauvegarde/reprise du brouillon, rubriques manquantes et récapitulatif avant publication (TRE-ARB-70).
- [x] Bibliothèque de fiches POI du partenaire, version et validation propres à chaque animation ; accès, QR et consignes revérifiés, éditions publiées préservées (TRE-ARB-71).
- [x] Nouvelles animations : inscriptions dès publication, fermeture à la fin ou anticipée, capacité facultative atomique ; reprise des inscrits conservée et paramètres des brouillons convertis contrôlés avant première publication.
- [x] DSL JSON avec enveloppe `common` et bloc `engineConfig` valide par le moteur du type.
- [x] Registres et trois moteurs specialises avec trois renderers : Passeport, Tombola, Chasse.
- [x] Modules internes au backend existant, interfaces communes, registre explicite et livraison coordonnée avec les frontends (TRE-ARB-64).
- [x] Modèles de validation backend comme source des schémas ; export automatique JSON Schema et contrôle de concordance, règles métier dans le domaine (TRE-ARB-65).
- [x] Version de contrat coordonnée par moteur pour configuration/commandes/projections ; versions de contenu et schéma commun distinctes, futures parties publiées préservées (TRE-ARB-66).
- [x] Définitions versionnées en JSON, participations/preuves/progression en tables structurées ; mapping, contraintes et migrations additives vérifiés sur PostgreSQL jetable (TRE-ARB-67).
- [x] Contrat extensible par type : schéma, règles, commandes, projections, préparation, renderer et capacités ; provider facultatif. Ajout de futurs types sans imposer le profil linéaire Chasse V1 au socle.
- [ ] Conversion des brouillons/configurations retenus : inventaire, simulation sans écriture, lots contrôlés/tracés/reprenables et contrôle de source ; ensemble validé avant ouverture, aucune suppression implicite de données (TRE-ARB-80).
- [ ] Bascule directe : aucune animation publiée avec l’ancien moteur, donc aucune coexistence ; moteur commun seul et consommateurs alignés avant ouverture.
- [x] Live non déployé : aucune rétrocompatibilité avec un ancien client ; conserver le versionnement des futures définitions et participations.
- [x] Cinematique complete de generation, prompt final persiste/exportable et dernier appel IA bouche.
- [x] Génération sur brief court : listes de commerçants et POI, fourchette d’étapes, durée approximative, public, difficulté, thème général et schéma attendu. Récit et parcours proposés dans ce cadre puis acceptés ; schéma à liste variable, écart au brief signalé, contrôles opérationnels hors prompt (TRE-ARB-87).
- [x] Provider de template Passeport : prompt genere, execution externe manuelle, depot et publication du resultat.
- [x] File ERP des demandes de creation de chasse : statuts, export du prompt, controles, publication manuelle du resultat, reprise et lien vers instance.
- [x] Finalisation idempotente de creation, distincte de publication publique de l’animation.
- [x] Aperçu des impacts avant retrait/correction, motif et confirmation explicite, recontrôle serveur et actualisation si impact obsolète (TRE-ARB-72).
- [x] Brouillon Animation unique créé dès le début de la demande, non publiable en attente et complété par le résultat accepté ; reprise sans doublon (TRE-ARB-73).
- [x] ERP : liste filtrable des demandes avec statuts/prochaine action/erreurs et fiche détaillée prompt/résultat/historique (TRE-ARB-74).
- [x] Quota disponible calculé depuis réservations/consommations, sans compteur supplémentaire ; journal et coordination transactionnelle partenaire/mois (TRE-ARB-75).
- [x] Quota de génération partagé par partenaire : 10/mois configurables dans l’ERP, réservation à la demande, consommation au résultat accepté, libération sur annulation préalable et corrections sans double décompte.
- [x] Quota mensuel en Europe/Paris sans report ; changement de plafond sur le mois courant et les suivants, passé inchangé, engagements conservés lors d’une baisse et places supplémentaires immédiatement disponibles lors d’une hausse (TRE-ARB-59).
- [x] Profil DSL Chasse V1 fermé : `ALL`, unique successeur `SUCCESS`, terminal sans transition ; autres combinaisons ambiguës refusées.
- [x] Parcours de chasse linéaire à ordre imposé ; fourchette d’étapes du brief (suggestion 5 à 8 par défaut) avec avertissement non bloquant ; défis QCM, information, association, remise en ordre et saisie courte (TRE-ARB-88).
- [x] Lieux/défis futurs masqués ; commerce nommé et localisé au déblocage, défi sur place ; une seule étape par commerçant.
- [x] Progression narrative, résolution, preuves, effets et qualification séparés ; état de régularisation explicite dans Live.
- [x] Protocole transactionnel et d’idempotence : courses clôture/correction/retrait/capacité, versions, résultat rejouable et effets uniques vérifiés.
- [x] Runtime de chasse : scan avant/apres resolution, indice et aide de resolution distincts disponibles apres une premiere mauvaise reponse, POI et qualification.
- [x] Information confirmée par « Continuer » sous réserve des autres conditions ; orientation par adresse et lien cartographique externe sans suivi de position Localeo.
- [x] Retrait d’etape uniquement global en V1, conservation des autres acquis et recalcul equitable ; aucune dispense individuelle.
- [x] Dépendances explicites validées avant publication ; retraits successifs résolus dans l’ordre.
- [x] Objets/indices indispensables fournis avec provenance de dispense sans fuite des étapes futures ; retrait définitif après démarrage et dernière étape requise non retirable, contrôle atomique.
- [x] Parcours Animation, Live et commercant, publication, duplication et tirage existant.
- [x] Chasse sans achat obligatoire ; inscription familiale adulte avec progression/chance uniques et sans données enfant.
- [x] Publication de chasse bloquée sans règlement et checklist confirmée (horaires, accords, trajet, accessibilité, consignes), avec auteur/date/version.
- [x] Preuve annulée avant clôture : nouveau scan requis, autres acquis conservés ; après clôture, population figée et anomalies tracées sans recalcul.
- [x] POI validés par l’organisateur sans seconde approbation Localeo : responsable, auteur, date, emplacement QR et observations ; photo facultative.
- [x] Alternatives textuelles obligatoires aux éléments visuels/sonores nécessaires aux défis, disponibles avec le contenu sans contourner les preuves.
- [x] Bibliothèque privée du partenaire/opérateurs habilités, versions acceptées uniquement ; réutilisation versionnée dans la même commune.
- [ ] Dépôt/publication ERP possibles par le même opérateur avec les deux permissions, contrôles et prévisualisation obligatoires, audit de chaque action.
- [x] QCM de 2 à 6 propositions avec une bonne réponse ; aucun score/classement V1 ; déclaration adulte obligatoire sans date de naissance à l’inscription de chasse.
- [x] Activités supplémentaires V1 : association un-à-un (2–6), ordre unique (3–6), mot/code et variantes normalisées ; définitions et commandes contrôlées par le domaine, aucun appel IA pour corriger (TRE-ARB-88).
- [x] Adapter génération/import/édition/prévisualisation et trois rendus Live accessibles au clavier ; solutions privées, présentation mélangée stable, reprise et aides après erreur valide ; tests de bornes, références, normalisation, idempotence et non-divulgation.
- [x] Récupération par lien email existant sans nouvelle participation ; génération décomptée sur le mois réservé, demandes sans expiration automatique et ancienneté ERP visible.
- [x] Conservation : prompts/réponses inutilisés 30 jours après terminaison/annulation, essais détaillés 90 jours après fin ; purge automatique avec exclusions, reprise et rapport ERP, complément technique du registre interne documenté.
- [x] Connexion nécessaire pour réponses/scans/validations ; conservation de la saisie en cours, reprise sur état serveur et réconciliation des commandes incertaines, sans progression locale ni synchronisation automatique.
- [x] Saisie temporaire liée à l’onglet, participation/étape/version ; restauration après rafraîchissement, suppression après validation confirmée ou expiration et aucune soumission automatique (TRE-ARB-76).
- [x] Modèles de réponse explicites et constructeurs dédiés par public, champs autorisés énumérés et tests de non-divulgation (TRE-ARB-77).
- [x] Journal d’audit commun raccordé à l’existant, corrections par nouvelles traces, corrélations et vues ERP filtrées ; conservation applicable (TRE-ARB-78).
- [x] Purge quotidienne configurable par lots reprenables, protections revérifiées, rapport et signalement des échecs (TRE-ARB-79).
- [x] Modifications après publication selon la phase : recontrôles avant démarrage, début figé ensuite, prolongation/capacité et réouverture explicite des inscriptions avant fin ; inscrits préservés, gel respecté et audit.
- [x] Départ et finale virtuels ou physiques au choix de l’organisateur, contrôles du lieu et preuves requises préservés (TRE-ARB-60).
- [x] Durée estimée et difficulté renseignées, conseils/avertissements non bloquants ; références ajustées après le pilote (TRE-ARB-61).
- [x] Passages actuellement valides en principal, annulations et historique séparés, sans doublon ni modification du gel (TRE-ARB-62).
- [ ] Tests métier/contrats à chaque évolution et scénarios entre applications par parcours terminé ; recette complète avant ouverture et contrôles obligatoires des dépôts maintenus (TRE-ARB-82).
- [ ] Recette de bout en bout et pilote sur une commune, une chasse et quelques commerces/POI : essai interne puis petit groupe de familles avant ouverture ; lieux/calendrier/participants à sélectionner (TRE-ARB-63).
- [ ] Bilan qualitatif du pilote : compréhension, faisabilité, scans, reprise et charge commerçante ; anomalies bloquantes corrigées et parcours concernés retestés avant ouverture (TRE-ARB-83).

- [x] Missions de préparation : idéalement deux variantes par commerce, exigences/produits/messages à confirmer, contenus et aides cohérents, une seule position par commerce (TRE-ARB-89).
- [x] Raccorder invitations EPIC 56 : relecture organisateur, choix unique et confirmations explicites, versions, refus, échéances, relances et audit ; aucun accord dans le résultat IA.
- [x] Stabiliser le parcours selon réponses, supports à fournir et checklist de mise en place ; assembler seulement les missions retenues. Publication impossible avec attente, engagement périmé ou préparation manquante ; minimum de commerçants fixé par chasse ; sous ce seuil, publication bloquée et adaptation/annulation explicite par l’organisateur, sans annulation automatique.
- [x] Tester retrait avant lancement, modification après accord, duplications sans consentement, non-divulgation et courses avec réponse/publication/annulation ; adapter Animation/ERP et application Commerçant.


Points ouverts : la CLI de conversion et les contrats coordonnés sont testés, leur application sur la cible reste à effectuer. Le dépôt et l’acceptation ERP du résultat IA sont livrés ; le droit de publication publique ERP n’a pas été élargi (revue automatique d’approbation refusée, voir le suivi T3/T6). Les contrôles techniques ciblés sont verts, mais deux recensements de couverture conservent leur dette antérieure ; pilote et bilan terrain non exécutés.

## Préparation et évolutions ultérieures

- [ ] Comparer les fournisseurs IA pendant le développement V1, sur les mêmes briefs ; intégrer le fournisseur retenu après le pilote, avec les mêmes contrats et contrôles (TRE-ARB-84, choix 25.B).
- [ ] Après V1, cadrer en priorité le rallye à ordre libre comme prochain type d’animation ; conserver le profil linéaire de la Chasse V1 (TRE-ARB-85, choix 26.C).
- [ ] Après V1, concevoir l’adaptation contrôlée vers un nouveau brouillon dans une autre commune : lieux remplacés, faits revus, nouvelles validations et provenance conservée (TRE-ARB-86, choix 27.A).

La comparaison fournisseur prépare la suite pendant le développement. Le traitement manuel reste celui de la V1 ; intégration IA réelle, rallye et adaptation intercommunes ne sont pas des fonctionnalités requises pour la première livraison.

## Évolution du 24 septembre 2026 — E55-ILL-01

Demande : améliorer l’accueil des joueurs grâce à une image mettant en scène chaque étape de la chasse. Le prompt backend demandait déjà une couverture, mais les illustrations d’étape restaient facultatives. L’évolution exige dans le prompt une scène adaptée à chaque étape et à chaque mission candidate, par héritage pertinent ou surcharge, sans divulguer la solution ni les lieux futurs.

- [x] E55-ILL-01-A : modifier le prompt backend et l’exemple documentaire Latresne ; conserver les budgets WebP/base64 et signaler toute image manquante comme résultat incomplet dans les instructions.
- [x] E55-ILL-01-B : vérifier la non-régression de l’héritage, de la sélection des médias et des projections existantes ; suite ciblée et architecture : 505 tests réussis sous Python 3.14.
- [ ] Évaluer une génération outillée et la compréhension des scènes par des joueurs ; aucune génération réelle réalisée pour cette modification de prompt.

Impacts, critères et preuves dans la [spécification canonique, section 8.1.2](../../specifications/moteur-animation/localeo_animation_engine_spec.md#812-thème-visuel-et-illustrations-de-lanimation). Aucun changement de statut de l’epic, de schéma ou de règle de publication. Les animations et prompts déjà enregistrés ne sont pas réécrits.

## Évolution du 24 septembre 2026 — E55-UX-08

Demande : harmoniser les sélections des commerçants et des coffrets, ainsi que
le fil d’Ariane, en prenant le Passeport commerçant comme référence. Ajouter
une consultation directe des commerçants en popin et des prestations des
coffrets. Avant cette évolution, la Chasse utilisait des listes et une
navigation différentes, et seuls les coffrets avaient une fiche consultable.

- [x] E55-UX-08-A : sélecteurs communs aux trois modèles, en création et configuration ; éligibilité, quantités et sélections conservées.
- [x] E55-UX-08-B : détails marchands accessibles depuis la sélection et les prestations des coffrets ; consultation sans mutation, erreurs réessayables et retour du focus.
- [x] E55-UX-08-C : fil d’Ariane commun sur bureau/mobile, navigation sans sauvegarde implicite ni perte des saisies ; phases de Chasse et blocages conservés.
- [x] E55-UX-08-D : preuves navigateur sur les trois modèles, non-régression des commandes et vérifications frontend/documentaires.

La [conception T6-UX08](../../specifications/moteur-animation/conception-technique.md#t6-ux08--sélections-et-fil-dariane-communs-e55-ux-08)
décrit les comportements et impacts ; le [suivi d’implémentation](../../specifications/moteur-animation/suivi-implementation.md)
consigne les preuves. Cette extension ne change ni le statut de l’epic ni les
conditions métier de publication, et ne nécessite aucune migration.

## Évolution du 24 septembre 2026 — kit et suivi de préparation

Demande utilisateur : une mission générée par commerce, supports joueurs par QR
sur flyers illustrés, kit et mode opératoire dans l’application commerçant,
option de suivi bloquant le démarrage tant que les participants ne sont pas prêts,
sauf forçage explicite. Voir les critères **E55-KIT-01 à 03** et
**E55-SUIVI-01 à 04** dans la
[conception canonique](../../specifications/moteur-animation/conception-technique.md#évolution-du-24-septembre-2026--kit-commerçant-et-préparation-du-démarrage).

- [x] Livrer et vérifier les nouveaux prompts et les kits accessibles au seul commerce concerné.
- [x] Livrer et vérifier le suivi facultatif et sa barrière serveur, avec forçage tracé.
- [x] Aligner les contrats, interfaces, guides et preuves de non-régression.

Cette évolution n’efface ni le bilan T1–T6 ni les travaux d’ouverture restants.

## Évolution du 25 septembre 2026 — E55-UX-09

Simplifier Localeo Animation pour un gestionnaire non technique : demande de
génération, réception du parcours graphique, consultation et configuration de
chaque étape, puis préparatifs et publication dans le même espace. Exploiter
la largeur desktop ; réserver prompts, requêtes et imports à l'ERP.

- [x] A : demande sans étape Commune de lecture ni outils techniques opérateur.
- [x] B : parcours illustré, ordre explicite, aperçu initial et inspecteur adaptable.
- [x] C : espace permanent, organisation/lots/financement regroupés et retour paiement.
- [x] D : invitations groupées avec destinataires explicites ; contrôle de publication automatique à l'ouverture.
- [x] E : préserver droits, saisies, relecture, accords, versions et résolution des commandes incertaines.

Critères, impacts et preuves dans la [conception E55-UX-09](../../specifications/moteur-animation/conception-technique.md#e55-ux-09--préparation-centrée-sur-le-parcours-25-septembre-2026)
et le [suivi d'implémentation](../../specifications/moteur-animation/suivi-implementation.md).
Le remplacement éventuel des attestations métier et une prédiction détaillée
des accords invalidés restent à préciser ; aucune preuve existante n'est
supprimée implicitement. Le statut de l'epic reste **En cours**.

## Évolution du 26 septembre 2026 — E55-UX-10

Jauge globale en haut à droite de la préparation, compteurs par rubrique et
détail des actions restantes, alimentés par les contrôles serveur enregistrés.

- [x] A : jauge et compteurs accessibles sur bureau et mobile.
- [x] B : contrôles restants, prérequis et blocages avec accès aux rubriques.
- [x] C : actualisation, erreurs, brouillons et isolation des réponses tardives.
- [x] D : projection serveur privée, sans modification des règles de publication.

Critères et impacts dans la [conception E55-UX-10](../../specifications/moteur-animation/conception-technique.md#e55-ux-10--avancement-de-la-préparation-26-septembre-2026).
Les résultats sont consignés dans le [suivi d'implémentation](../../specifications/moteur-animation/suivi-implementation.md).

## Évolution du 26 septembre 2026 — E55-UX-11, Terrain simplifié

Le gestionnaire doit préparer l’animation sans constituer un dossier de contrôle
par lieu ou mission. Cette décision remplace explicitement les obligations
terrain T3 et complète E55-UX-09/10 ; le statut de l’epic reste **En cours**.

- [x] A : deux blocs « Supports à installer » et « Préparation des participants »,
  sans formulaire de visite, contrôle de mission ni checklist obligatoire.
- [x] B : publication possible sans ces anciens dossiers ; accords, versions,
  lieux autorisés, supports QR nécessaires et contrôles de publication conservés.
- [x] C : jauge et bilan exempts des vérifications supprimées, sans validation
  fictive ni suivi « prêt » rendu obligatoire pour toutes les animations.
- [x] D : QR utilisables, droits, réception incertaine, clavier/mobile et données
  historiques préservés ; compatibilité avec l’exploitation après publication.

Critères et impacts dans la [conception E55-UX-11](../../specifications/moteur-animation/conception-technique.md#e55-ux-11--terrain-simplifié-26-septembre-2026).
Les preuves exécutées sont consignées dans le [suivi](../../specifications/moteur-animation/suivi-implementation.md).

## Évolution du 26 septembre 2026 — E55-UX-12, supports par responsable

Le commerçant installe les supports de sa propre étape. Le gestionnaire conserve
uniquement les supports des lieux publics. Cette évolution précise E55-UX-11-A/C,
sans remettre en place de checklist ni de double confirmation.

- [x] A : Terrain ne présente que les POI et masque ce bloc sans POI ; le suivi
  des commerces reste accessible.
- [x] B : l’acceptation d’une mission prépare son QR ; le kit contient le support
  de cette étape, distinct du flyer et du guide privé.
- [x] C : les anciennes acceptations disposent d’une reprise explicite au
  téléchargement, versionnée et idempotente ; les lectures n’écrivent rien.
- [x] D : isolation commerçant, QR utilisable, publication, jauge, reprise réseau
  et déclaration « prêt » indépendante sont préservés.

Voir la [conception E55-UX-12](../../specifications/moteur-animation/conception-technique.md#e55-ux-12--supports-par-responsable-26-septembre-2026)
et le [suivi](../../specifications/moteur-animation/suivi-implementation.md).
Implémentation vérifiée localement ; la recette PostgreSQL et le scan physique
restent à exécuter avant livraison. Le statut de l’epic reste **En cours**.

<a id="e55-audit-20261113"></a>
## Évolution du 13 novembre 2026 — fiabilité, parcours et capacité

Demande utilisateur : intégrer le contenu de l'audit de Localeo Animation,
Localeo ERP et Localeo Live dans l'EPIC 55. L'audit constate un socle livré,
des défauts reproduits et des preuves d'ouverture manquantes. Les bilans
historiques et le statut **En cours** sont conservés. Cette intégration prépare
les travaux ; elle ne les déclare ni implémentés ni vérifiés.

Les repères **E55-A01 à E55-A14** du rapport deviennent les critères stables
de cette évolution. Les défauts du comportement attendu relèvent de correctifs
rattachés à E55 ; les nouvelles capacités et études restent distinguées.
Le [complément fonctionnel](../../specifications/moteur-animation/localeo_animation_engine_spec.md#e55-audit-20261113),
la [conception et sa matrice](../../specifications/moteur-animation/conception-technique.md#e55-audit-20261113)
et le [bilan de référence](../../specifications/moteur-animation/suivi-implementation.md#e55-audit-20261113)
portent les scénarios, impacts et limites. Aucun nouveau backlog applicatif.

### Critères issus des constats

| Critère | Priorité / nature | Résultat attendu et reste à faire |
| --- | --- | --- |
| E55-A01 | P1 — évolution de résilience | [x] Une indisponibilité du carnet local ne bloque pas une nouvelle inscription autorisée par le serveur ; récupération, unicité et reprise après réponse perdue restent sûres. |
| E55-A02 | P1 — correctif ERP | [x] Après confirmation du reçu d'une décision, le gestionnaire peut prendre la suivante ; reçu absent, refusé ou incohérent ne libère pas indûment une commande incertaine. |
| E55-A03 | P1 — correctif de saisie | [x] Actualiser le suivi conserve le brief modifié ; quitter/changer de demande exige un abandon explicite lorsque la saisie serait perdue, dans Animation et l'ERP. |
| E55-A04 | P1 — correctif de disponibilité | [ ] Varier un UUID avec un accès invalide ne crée pas un nombre arbitraire de compteurs persistés ; limitation anonyme bornée, autorisation personnelle et purge sont vérifiées. |
| E55-A05 | P1 avant montée en charge — capacité | [ ] Participants, métriques, aperçu de retrait et gel disposent de lectures/mémoire bornées et d'une preuve N/10N sous charge mixte, sans altérer qualification ni population figée. |
| E55-A06 | P2 — correctif de résilience | [x] Une erreur de quota n'empêche pas de consulter un parcours déjà préparé ; seule l'action dépendante reste indisponible avec réessai. |
| E55-A07 | P2 — évolution ERP | [x] La recherche porte sur toute la file autorisée, avec filtres serveur et pagination ; un dossier hors de la page chargée reste trouvable. |
| E55-A08 | P2 — correctif d'états UI | [x] Invitations inconnues, erreur, liste vide et succès restent distincts ; une lecture réussie efface l'alerte précédente sans faux compteurs zéro ni messages techniques redondants. |
| E55-A09 | P2 — correctif Live | [x] Commencer/continuer est identifiable et réellement cliquable à 320/390/1280 px, sans recouvrement par la navigation, y compris quand le tirage est inconnu. |
| E55-A10 | P2 — évolution du contrat public | [x] Durée estimée, difficulté, public visé et nombre d'étapes disponibles sont présentés avant inscription, sans lieux futurs ni valeurs inventées. |
| E55-A11 | P2 — correctif d'interaction | [x] Une association en doublon donne une explication et une correction accessibles ; aucune tentative serveur ni aide métier n'est créée par cette erreur de formulaire. |
| E55-A12 | P2, requis avant ouverture — preuves | [x] Fixtures/attentes mises à jour et chaîne complète rejouée jusqu'à conservation ; aucun retrait d'assertion métier ni skip pour masquer les échecs. |
| E55-A13 | P2 — correctif d'accessibilité | [x] Après remise en ordre, le focus reste sur un contrôle utilisable de l'élément déplacé et sa nouvelle position est annoncée. |
| E55-A14 | P2 — correctif d'accessibilité | [x] Réponses et statut suivent l'agrandissement du texte à 200 %, avec actions accessibles, sans perte de contenu ni débordement horizontal à 320/390 px. |

### Axes complémentaires du rapport

- [x] **E55-OPT-01 — Guidage quotidien :** rendre visibles l'acteur attendu,
  la prochaine action, le relais humain Localeo et le délai de service applicable ;
  conserver la file et les filtres ERP après traitement. Pas de nouvelle promesse
  de délai ni de duplication des suivis existants.
- [x] **E55-OPT-02 — Étude d'impact des modifications :** préciser un aperçu
  des accords affectés avant édition importante, avec concordance serveur,
  coût et limites. Livrable attendu : conception et décision motivée ; le rapport
  ne suffit pas à spécifier ni autoriser une invalidation métier nouvelle.
- [x] **E55-OPT-03 — Invitations paginées :** afficher la première page sans
  collecter tout l'historique ; sélection et destinataires explicites conservés.
- [x] **E55-OPT-04 — Médias de jeu :** mesurer relectures, décodage, octets et
  latence à froid/chaud ; décider l'optimisation à partir du résultat, avec
  confidentialité, invalidation et mémoire bornée comme critères.
- [x] **E55-OPT-05 — Chargement Animation :** mesurer le premier accès à l'éditeur
  sur mobile ; décider le découpage du bundle selon le coût constaté. Le seul
  avertissement de taille du build ne prouve pas une lenteur.
- [ ] **E55-OPT-06 — Productivité et pilote :** établir une référence de temps
  de traitement, retours pour complément, première action utile, échecs de
  scan/reprise et abandon ; comparer après correction sans données privées dans
  les mesures. Vérifier la profondeur de navigation avec les trois acteurs.

### Lots et dépendances

| Lot | Critères | Condition de sortie |
| --- | --- | --- |
| L1 — Continuité et protection | A01–A04 | Cas nominaux, refus, perte de réponse, réconciliation et absence de double effet prouvés. |
| L2 — Parcours quotidien | A06–A11, A13–A14, OPT-01/03 | Contrats et rendus alignés ; recettes bureau/mobile/clavier/texte agrandi. Dépendances propres à chaque critère, pas d'attente artificielle de tout L1. |
| L3 — Capacité et preuves | A05/A12, OPT-02/04/05/06 | Mesures et décisions d'étude tracées ; chaîne transversale actuelle réussie. Les travaux indépendants peuvent commencer avec L1/L2. |
| L4 — Pilote et ouverture | Critères T6 existants, TRE-ARB-80/82/83 et droits ERP | Cible/version/capacité renseignées, conversion/contrats/permissions/conservation vérifiés, pilote Android/iPhone et familles, bilan et retests. |

Spécification complétée le 13 novembre : états d'accès temporaire et reçus ERP,
limiteur PostgreSQL à cardinalité bornée, projection Chasse exacte et synchrone,
reconstruction/bascule, gel par lots sans relecture exhaustive, pagination des
consommateurs réels, recherche normalisée/index existants et métadonnées publiques.
Les contrats et budgets initiaux de recette sont dans la conception canonique.
La recherche ignore les accents, conformément au service existant ; ce choix
remplace l'hypothèse initiale de l'intégration du rapport.

L1/L2 peuvent être implémentés par critères indépendants. Dans L3, alimenter
et reconstruire la projection avant d'activer les lecteurs ; prouver tous les
chemins de correction/retrait/gel avant la campagne N/10N. Les études gardent
leur livrable de décision motivée. Restent à produire : code, migrations,
exports, tests et mesures ; les valeurs de production A04 et la capacité
réelle nécessitent une cible renseignée. Le tirage des gagnants reste mesuré
séparément du gel. Aucun critère ni statut de livraison ne change ici.

La génération IA manuelle reste le choix V1 ; comparaison des fournisseurs et
évaluation des illustrations restent à mener selon E55-ILL-01/TRE-ARB-84.
L'intégration d'un fournisseur après pilote, le rallye libre et l'adaptation
intercommunes ne deviennent pas des prérequis de ce lot. Aucun changement de
droits ERP, migration, déploiement ou génération réelle n'est exécuté par la
phase de spécification décrite ci-dessus.

### Bilan de l'implémentation locale

Les critères cochés disposent de preuves locales dans le
[bilan d'implémentation](../../specifications/moteur-animation/suivi-implementation.md#e55-audit-20261113-implementation).
Les cases distinguent résultat vérifié et limites restantes ; aucune ne vaut
déploiement ni validation du pilote. Le code, les migrations, les contrats et
les adaptations de démonstration remplacent désormais les travaux annoncés
« à produire » dans la phase précédente.

A04 est implémenté et ses protections sont testées ; les mesures isolées
respectent le budget local. Sa qualification proxy/NAT et sa politique sur
cible restent à produire. A05 dispose des projections, lecteurs et traitements
par lots, mais sa capacité ne peut être acceptée sans toutes les mesures
prévues ; les essais intermédiaires et leurs dépassements restent visibles.
A12 est traité par réalignement et rejeu des suites concernées, avec résultats
détaillés au bilan. OPT-06 reste partiel faute de comparaison humaine de temps
de traitement. L4, la comparaison des fournisseurs et l'ouverture restent
ouverts ; le statut **En cours** est conservé.

## E55-EVOL-TRAITEMENT-20261113 — Simplifier le traitement ERP

Demande du 13 novembre : une fiche unique depuis l’examen de complétude et le
refus motivé jusqu’au prompt, à l’import JSON et à la validation finale ; reprise
du dossier en cours sans recommencer. Les [critères E55-DG-01 à E55-DG-10](../../specifications/moteur-animation/localeo_animation_engine_spec.md#e55-evol-traitement-20261113)
et la [conception](../../specifications/moteur-animation/conception-technique.md#e55-evol-traitement-20261113)
conservent les transitions et contrats existants. L’epic reste **En cours** ;
le bilan de cette évolution ne remplace pas les conditions historiques d’ouverture.

- [x] Décrire le dossier et ses étapes, les refus, la reprise et les impacts.
- [x] Réunir le parcours dans la console ERP et raccorder les anciens points d’entrée.
- [x] Vérifier les comportements et publier le [bilan local](../../specifications/moteur-animation/suivi-implementation.md#e55-evol-traitement-20261113), avec ses limites de recette déployée et de mesure humaine.

## Références

- [Registre TRE-ARB-01 a TRE-ARB-89](../../specifications/moteur-animation/localeo_animation_engine_spec.md#arbitrages).
- [Besoins PRD-520 a PRD-532 et lots proposes](../../specifications/moteur-animation/localeo_animation_engine_spec.md#livraison).
- [Compléments de conception](../../specifications/moteur-animation/localeo_animation_engine_spec.md#questions-ouvertes).
- [Recette et criteres de livraison](../../specifications/moteur-animation/localeo_animation_engine_spec.md#recette).
