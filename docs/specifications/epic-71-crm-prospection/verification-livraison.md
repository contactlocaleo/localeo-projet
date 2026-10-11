# E71 — Vérification et livraison

Références : [README](README.md), [backlog et 24 critères](../../roadmap/a-faire/epic-71-crm-prospection-animation-coffrets-pro-backlog.md). **Tests produit prévus, non exécutés** : cette phase ne modifie aucun code applicatif et n'importe aucun prospect réel.

## Matrice de traçabilité

Les noms de suites ci-dessous sont des cibles d'implémentation, pas des fichiers annoncés existants. D = domaine pur, A = application/UoW, SQL = intégration PostgreSQL jetable, API = contrat et droits, UI = navigateur. Chaque ligne demande nominal et refus ; rejouer les mutations sensibles.

| Critère | Comportement / propriétaire | Preuve prévue | Documentation / contrat | Fixture / exploitation |
| --- | --- | --- | --- | --- |
| E71-CA-01 | Organisation/contact minimal, aucun compte ou envoi ; OrganisationProspect | D/A/API création incomplète et coordonnées invalides ; zéro appel métier externe | Parcours objets, POST organisations/contacts | Prospect synthétique incomplet ; migration additive |
| E71-CA-02 | Une structure, plusieurs affaires ; OpportuniteProspection | D/SQL deux axes et deux campagnes du même axe | Fiche et références | Organisation multi-axes sans copie forcée |
| E71-CA-03 | Transitions, pause, perte, gain, réouverture ; Opportunité | D matrices autorisé/refus, preuves absentes/périmées ; A lecture preuve | Transitions et contrat gain | Gain par chacun des trois axes, pause à réexaminer |
| E71-CA-04 | Événement et correction traçables | D/A note corrigée, dates séparées, aucun fournisseur invoqué | Chronologie, API événements | Note synthétique ; purge du texte libre |
| E71-CA-05 | Cycle tâche/responsable/échéance ; Tâche | D/API terminer/report/annuler, responsable révoqué | Mes actions, commande tâche | Tâche ouverte/terminée/en retard |
| E71-CA-06 | File calculée sans double rappel | A/UI horloge aux frontières Paris/UTC, DST et double lecture | Rappels et affichage dates | Pas d'envoi réel ; métriques de lecture |
| E71-CA-07 | Même filtre et comptage liste/tableau/carte | API/UI filtres URL, pagination, zéro résultat vs erreur | Contrat liste et carte | Portefeuille volumineux et accès clavier |
| E71-CA-08 | Aperçu sans écrit métier ; LotImport | A/parser XLSX, macros/liens actifs/ZIP expansif refusés ; formules jamais exécutées, caches d’estimation et URL textuelles distingués ; SQL aucune entité métier | Assistant et mapping | Fixtures synthétiques valides/hostiles ; limites stockage |
| E71-CA-09 | Anomalies, minimum et exclusions | D/A lignes incomplètes, aucune ville/email/heure inventée | Rapport par cellule/ligne | Lot partiellement rejeté |
| E71-CA-10 | Rapprochement explicite, pas fusion au nom | D/A/SQL homonymes et email générique partagé | Comparatif et provenance | Deux établissements distincts, opposition candidate |
| E71-CA-11 | Rejeu/reprise sans doublons | A/SQL deux confirmations concurrentes, bail expiré, panne après commit, fichier modifié/retrié | Identité source et protocole de reprise | Lot interrompu puis enrichi ; runbook reprise |
| E71-CA-12 | Bilan privé et correction bornée | API accès rapport refusé, correction version périmée, arrêt partiel | Imports et corrections admin | Fichier privé supprimé selon politique, métadonnées restantes |
| E71-CA-13 | Centre communal et groupe de points | API/UI plusieurs organisations/opportunités au même point | Carte indicative | Commune très dense, cluster au-delà limite |
| E71-CA-14 | Non-localisés et commune hors catalogue | D/A résolution ambiguë ; aucun CreerVille/publication appelé | Cache communal indépendant | Homonyme, INSEE avec zéro, commune absente catalogue |
| E71-CA-15 | Liste utilisable sans carte | UI mobile/clavier, fournisseur en panne, inspection requêtes tierces | Navigation/fallback et fournisseur retenu | Aucune coordonnée de contact envoyée au fond de carte |
| E71-CA-16 | Rattacher commerçant et dossier existants | A/API lien répété/concurrent, relation dossier vérifiée ; aucune activation/email | Port Référencement/OnBoard | Commerçant déjà créé avant reprise |
| E71-CA-17 | Lien Animation sans activation implicite | A/API partenaire seul ≠ gain, souscription active payée/gratuite, rôle sans SQLAdmin | Port Animation / chemins autorisés | Checkout en attente et abonnement actif |
| E71-CA-18 | Commande Pro réelle, référence typée | A/API ACHAT vs COMMANDE, paiement attendu/refus ; zéro renouvellement code crédit | Port Achats / gain | Organisation de crédit existante, commande impayée/payée |
| E71-CA-19 | Scopes globaux et droits cumulés | API/UI Lecteur/Backoffice/Finance/admin, accès direct, CSRF, session expirée, rapport privé | Matrice E69 et registre routes | Comptes synthétiques ; aucun élargissement SQLAdmin |
| E71-CA-20 | Opposition persistante et blocage sollicitation | D/A/SQL course opposition/tâche, réimport, réouverture, levée non autorisée | Politique ARB-07 et contrat oppositions | Opposition contact/structure et contact obsolète |
| E71-CA-21 | Versions, transaction, effets uniques | SQL/API deux versions concurrentes, clé identique/corps différent, révocation avant replay | Erreurs409, UoW et résultat commande | Deux sessions ; aucune perte silencieuse |
| E71-CA-22 | Calculs explicites sans faux CA | D/projection/API organisations vs affaires, devises, inconnus, gain réouvert | Indicateurs et définitions | Deux axes et estimation inconnue |
| E71-CA-23 | Guide et recette novice | UI utilisateur suit import→tâche→carte→rattachement ; accès guide selon droits | Guide canonique à rédiger avant livraison | Extension générateur E63, aucun contact réel |
| E71-CA-24 | Structure Gironde et anomalie X/Y | Parser/A fixture neuf onglets, 37 exceptions + une ligne normale, synthèses exclues | Mapping Gironde explicite | Aucun classeur source réel dans Git |

## Suites et commandes à produire à l'implémentation

Suites proposées : `tests/domain/prospection/`, `tests/application/prospection/`, tests API de capacités/imports/rattachements, tests SQL transactionnels et `tests/browser/prospection-erp.cjs`. Utiliser les runners du [backend](../../../../localeo-backend/README.md) ; pas de base de test partagée, démonstration ou production pour ces vérifications.

```text
python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q
```

Ajouter les suites comportementales réellement créées, puis PostgreSQL jetable et navigateur. Le domaine doit être testable sans ORM/UoW/fournisseur ; les adaptateurs doivent prouver les contraintes uniques et les transactions, pas seulement l'import des modules.

## Conservation et audit — blocage explicite ARB-07

Le [rattachement E70/E72](../identite-acces/conservation-validations-acces.md) concerne accès et preuves Coffret, pas les prospects. La lecture ciblée n'a pas établi de durée CRM applicable. **Ne pas réutiliser automatiquement cinq ans, douze mois ou une durée issue des paiements.** Faire valider les catégories, déclencheurs, durées et exceptions avant tout import de données réelles.

| Catégorie à rattacher à la politique | Déclencheur à décider | Traitement à concevoir et tester |
| --- | --- | --- |
| Organisations/contacts/opportunités sans relation métier | Dernier échange pertinent ou clôture, à valider | Suppression/anonymisation, traitement des contacts partagés et liens ; une lecture interne ne prolonge pas la durée |
| Notes, échanges et tâches | Date de l'événement/clôture, à valider | Purge contenu libre et attributs personnels, cohérence historique après suppression |
| Fichiers bruts, aperçus, rapports | Dépôt, abandon ou fin d'import, à valider séparément | Supprimer blob et copies temporaires, URLs et caches ; un fichier abandonné doit expirer |
| Correspondances d'origine/idempotence | Fin du lot et durée de possibilité de réimport, à définir | Préserver l'absence de doublon sans rétention illimitée de contenu personnel |
| Opposition / preuve de levée | Règle spécifique à valider | Identifiants minimaux nécessaires au blocage ; ne pas effacer automatiquement l'opposition avec le fichier source |
| Audit SQL, copies JSONL et sauvegardes | Politique de la finalité concernée | Métadonnées autorisées seulement ; suppression/rotation des segments chaînés selon mécanisme existant, reprise après restauration |

Les logs ne reçoivent que IDs opaques, code d'action/résultat, versions, tailles/comptages et corrélation. Une liste autorisée de champs CRM est nécessaire : la sanitisation générique de secrets ne suffit pas. Pas d'email, téléphone, nom de personne, note, contenu de cellule, URL privée signée ni payload intégral. Les erreurs de parsing nomment feuille/ligne/code plutôt que la valeur sensible.

La politique doit être versionnée et applicable aux données SQL, stockage objet, fichiers de travail, exports autorisés, JSONL et restaurations. Réserver les durées à une configuration validée ; l'absence de politique empêche l'activation CRM avec données réelles. Tester la purge en dry-run sur fixtures, l'effectif supprimé et le maintien d'oppositions selon la politique choisie. Ne pas altérer une chaîne JSONL par suppression arbitraire de lignes.

## Démonstration et impacts documentaires

Étendre le générateur dans le backend, jamais déplacer ses scripts/données ici. Ajouter organisations/contacts synthétiques, une organisation à deux axes, homonymes, doublon de source, opposition, non-localisé, commune hors catalogue, pauses/retards, gains des trois axes et lot interrompu. Les identités métier liées doivent provenir des parcours de génération existants ; aucun checkout, email ou fichier réel.

Produire un guide commercial ERP canonique couvrant interprétation des états, import/erreurs, rapprochement, carte, tâches, opposition et passage au métier. L'ajouter au bundle via `documentation.exports.json` seulement lorsqu'il est rédigé et consommé ; ne pas publier ce brouillon de conception comme manuel d'un écran disponible. Tester droits de lecture et liens du guide côté ERP. Mettre à jour domaine/tags API et catalogue de capacités lors de l'implémentation, pas en déclarant des routes fictives actuelles.

Pas de migration fonctionnelle ni de changement de contrat requis dans Commerçant, Animation ou Marketplace pour la V1 par rattachement. Vérifier leurs liens si une destination publique change ultérieurement. Le contrat d'achats, le crédit Pro, les permissions E69 et les invitations existantes restent propriétaires de leurs comportements.

## Ordre de livraison et exploitation

1. Résoudre les arbitrages bloquants ; valider politique de conservation, mapping, fournisseur carte/couverture et volumes.
2. Livrer migrations additives et contrôles de schéma, domaine/use cases, permissions et API avec option CRM désactivée. Aucun numéro de migration réservé dans cette spécification.
3. Livrer ERP avec mêmes droits, liste disponible indépendamment du fournisseur de carte ; configurer stockage privé, bornes d'import, worker/baux et cache géographique.
4. Exécuter tests métier/contrats, démonstration synthétique et recette mobile/clavier ; vérifier que l'import ne produit ni compte ni notification ni publication.
5. Pilote restreint explicitement autorisé : aperçu, mapping approuvé, import, reprise, vérification droits et purge. Une approbation de cette spécification n'autorise pas à importer le classeur réel.
6. Activer progressivement. Retour arrière par désactivation des commandes/imports et conservation des données cohérentes ; interrompre les workers sans perdre les lignes validées. Pas de suppression des tables comme première action de reprise.

Suivre nombre/durée/état des lots, baux expirés, lignes en conflit/rejet, échecs géographie/carte, conflits de version et purges. Les métriques ne contiennent pas de coordonnées personnelles. Prévoir runbooks pour timeout après confirmation, reprise du lot, mauvais rattachement, retrait d'accès pendant import, fichier invalide et fournisseur indisponible. À l'exécution différée, revérifier droits de l'auteur avant chaque unité de travail ; révoquer suspend les lignes restantes, pas les lignes déjà validées.

## État des vérifications de cette phase

- Lecture des producteurs et consommateurs ciblés : effectuée sur sources locales ; pas d'appel métier ni d'inspection du fichier privé.
- Revue indépendante de conception : effectuée en lecture ; intégration du plan d’import immuable après confirmation, de la distinction entre idempotence et partage d’une preuve de gain, et des tests séparant contenu actif interdit et valeurs de provenance admissibles.
- Validation documentaire du 9 octobre : `python scripts/check_guidance.py` — 93 guides / 979 liens, zéro erreur ; `python scripts/check_guidance.py --all-markdown --changed` — 9 documents / 157 liens, zéro erreur ; `python scripts/sync_documentation.py --check-sources` — 122 documents vérifiés. Ces contrôles ne prouvent pas les comportements CRM.
- Tests de produit CRM, migrations, navigateur CRM, performance, import réel et déploiement : **non exécutés**, aucun code CRM livré dans cette phase.

## Preuves supplémentaires E71-EVOL-01 — prévues, non exécutées

- CA-08/24 : profil réutilisé sur février, ajout de lignes au-delà des plages V2, colonnes déplacées/manquantes et règle X/Y conditionnelle ; un changement de structure impose revalidation ciblée.
- CA-09/11 : table B/C/N complète, champ source inchangé/CRM corrigé, source changée/CRM intact, deux modifications divergentes, convergence, cellule vide et absence de baseline ; protection conservée après « Garder CRM » et après modification locale aller-retour.
- CA-10/11 : lignes retriées, retour d’un absent, homonymes, mois plus ancien et deux imports concurrents ; aucun doublon ni recul silencieux de baseline.
- CA-11/12 : correction CRM entre aperçu et confirmation, panne/reprise, même fichier avec autre clé HTTP ; aucun écrasement et décisions de champ auditées une seule fois.
- UI : parcours mensuel court avec inchangés masqués, compteurs, comparaison en trois colonnes, exclusion des conflits et bilan ; conserver les droits d’import Backoffice/admin.
- Démonstration : trois classeurs synthétiques janvier/février/mars et corrections locales intermédiaires ; pas de copie du fichier privé. Conservation : intégrer snapshots et décisions de champ à ARB-07, pas de rétention implicite illimitée. Contrats/migrations : extension backend/ERP uniquement ; aucun nouveau effet dans les interfaces publiques ni import réel.

## Preuves supplémentaires E71-EVOL-02 — prévues, non exécutées

CA-08/09/24 : fixture à deux onglets utiles et onglets exclus ; seuls les objets Pipeline sont créés, les 33 colonnes communales sont affichées sous leurs libellés, aucune création de contact depuis O:R ; colonnes nouvelles/manquantes signalées. CA-10/14 : homonymes, INSEE absent, commune absente du CRM, doublon INSEE dans l’onglet et changement de nom ; aucun appel de création/publication Ville. CA-11/12 : delta mensuel sur champ communal corrigé, absence puis retour d’une commune, reprise partielle des deux destinations sans doublon. CA-07/13/19/22 : section accessible depuis commune/carte, droits Lecteur/Backoffice/Finance, nombre de sections exclu du compteur prospects.

Démonstration : communes et personnes entièrement synthétiques, section comportant 33 valeurs dont texte mixte en coordonnée publique et sources déclarées non vérifiées. Conservation : inclure contenus de section et snapshots dans ARB-07. Contrats/persistance : fiche communale et section distinctes du cache géographique, versions et unicité ; frontend public inchangé. Source examinée le 9 octobre : A7:AG28, 21 lignes/33 colonnes sans formule ; aucune validation externe des contenus.
