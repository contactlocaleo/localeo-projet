# E71 — Vérification et livraison

[Spécification V1](README.md), [backlog canonique](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md). **Implémentation locale et vérification en cours**. Le bilan ci-dessous distingue les tests réalisés des réserves. Aucun import réel ni envoi fournisseur. Les sections historiques de spécification restent datées. La carte reste en V1 sur confirmation utilisateur ; CSV standard seul et report de CA-24 (import spécifique Gironde) sont également confirmés.

## Matrice de traçabilité

D = domaine pur ; A = application/UoW ; SQL = PostgreSQL jetable ; API = droits/contrats ; UI = navigateur. La matrice décrit les preuves attendues ; les résultats exécutés et leurs limites figurent dans le bilan d’implémentation en fin de document.

| Critères | Propriétaire et scénario de preuve | Documentation / contrat | Fixtures et exploitation |
| --- | --- | --- | --- |
| CA-01/02 | Organisation/dossier : D/A/API minimum, deux contacts/deux périmètres, deux campagnes, zéro conversion/envoi | Parcours fiche et contrat prospects/dossiers | Structure synthétique multi-périmètre, migration additive |
| CA-03 | Opportunité : D matrice des six étapes, pause/réexamen, perte/réouverture, preuve absente/invalide/valide pour chaque objectif ; deux dossiers/une preuve en SQL concurrent, annulation métier concurrente, rejeu et réouverture sans double comptage | Transitions, règles de gain et ARB-04b | OnBoard accepté, souscription active/gratuite, commande payée ; aucun paiement créé |
| CA-04 | Événement : D/A note/correction, dates distinctes, double clic et ajouts concurrents, XSS texte échappé | Chronologie, erreurs de formulaire | Notes synthétiques, logs sans contenu et purge selon politique |
| CA-05/06 | Tâche/rappel : D/A/API cycle, échéance Paris/UTC/DST, projection prochaine action ; terminer/report/réaffecter avant envoi | Aujourd'hui, Rappels et commandes | Tâches retard/jour/futur, horloge contrôlée, aucun fournisseur réel |
| CA-07/22 | Projections : API/UI filtres communs liste/suivi/carte, comptages distincts et datés, pagination SQL, zéro résultat/erreur | Recherche, indicateurs et carte | N/10N, mêmes filtres, une structure plusieurs dossiers |
| CA-08/09 | Lot : parser/A CSV UTF-8 BOM/sans BOM, guillemets/retours ligne, colonnes manquantes/dupliquées/inconnues, rejet XLSX, limites, groupe contradictoire atomique | Dictionnaire CSV et aperçu | Fixtures synthétiques ; formule non évaluée, exports neutralisés, zéro écrit avant confirmation |
| CA-10/11 | Identité/import : SQL mêmes clés, réordre, nom changé, homonymes, contact répété, lot concurrent et source différente, namespace avec espaces/casse normalisé et création de source explicite ; panne après commit/reprise ; deux créations sources A/B ou manuel/import avec barrières SQL, candidat apparu après décision de distinction, erreur de sérialisation sans création automatique | Clés stables et plan immuable | Aucune duplication, bail expiré et jeton ancien refusé, marqueur d'effacement manuel protégé |
| CA-12 | Lot : API sources/décisions/confirmation versionnée/arrêt/reprise, rapport interdit après révocation ; acteur de reprise, exclusions, INIT sans effet, états terminaux et bilan par groupe fidèle | Imports et runbook | Stockage privé, fichier abandonné/purge, enrichissement post-import préservé |
| CA-13/14/15 | Localisation/carte : INSEE obligatoire de Nouvelle-Aquitaine pour création/changement de localisation, refus hors région, conservation des anciennes fiches, homonymes et hors catalogue ; points agrégés, dépassement de 500 sans curseur, clic groupe et pagination 25/100 ; mobile/clavier/panne fournisseur | Carte interactive, saisie régionale et fallback liste | Douze départements, ancien hors région/sans commune ; aucun contact/note transmis au fournisseur, aucune ville commerciale créée |
| CA-16/17/18 | Rattachement : A/API droits métier, cible de mauvais prospect, répétition, reprise après création externe ; gain conforme | Liens OnBoard/Animation/Achats | Aucun accès/checkout/paiement provoqué par import ou statut |
| CA-19/29 | Identité : D/API/UI toutes combinaisons de rôles/droits, absence de grant implicite, lecture liste/fiche/dossier autorisée et mutations refusées au lecteur, cardinalité des rôles éligibles sans élargissement historique, DTO/menus/registre fermés, CSRF, accès direct, session expirée ; révocation pendant commande/lot/rejeu | ERP profils, contrat droits et PWA | Comptes synthétiques sans droit/lecture/gestion/import/admin, pas d'élargissement SQLAdmin |
| CA-20/21 | Opposition/version : D/SQL course planification-opposition, fermeture pendant batch, réimport/réactivation, contact ciblé vs autre contact, coordonnée opposée réutilisée comme structure, tâche structure sans contact ciblé, correction concurrente et idempotence corps divergent | Politique commune et 409/422 | Aucun rappel sollicitant après opposition avant remise transport, versions et histoire conservées |
| CA-23 | UI parcours documenté : installation → import → fiche/carte → note → rappel → rattachement | Guide CRM, modèle CSV et aide contextuelle | Scénarios automatisés synthétiques ; aucun compte rendu de pilote requis pour clôture |
| CA-24 | **Reporté** : ancien import Gironde/sections communales | Historique E71-EVOL-02, hors V1 actuelle | Pas de fixture Gironde obligatoire pour valider le nouveau CSV |
| CA-25 | PWA/UI manifest/scope/start_url, navigation profonde, retour après auth, offline, mise à jour réelle seulement ; inspection caches et changement de compte | Installation, confidentialité et cycle PWA commun | 360/390/1280 px, clavier, ServiceWorker sans données privées |
| CA-26 | Push : A/API/UI opt-in/refus/unsupported, ownership abonnement, 404/410, panne/réessai/issue incertaine, clic hors session ; report et droits retirés | Préférences, intention/délivrance et états transport | Transport simulé, multi-appareils, aucune fuite de contact sur écran verrouillé |
| CA-27 | Email : D/A outbox éligible, préférence off/on, responsable différent, tâche annulée après enqueue, révocation avant revendication ; aucune régression des autres emails | Charte, garde d'expédition, runbook | Fournisseur simulé, destinataire interne vérifié uniquement, adresse absente/non vérifiée refusée ; preuve E69 liée à email_version, reprise depuis invitation consommée seulement, changement d’adresse entre opt-in/enqueue/envoi, réactivation volontaire et non-régression E69 ; pas de rattrapage massif |
| CA-28 | Import : INIT sur existant ignore tout ; UPSERT complète vide non protégé/ajoute contact/dossier ; notes/statut/rappels/opposition inchangés, absents conservés | Mode et règles par champ | Exemple P0001/P0002, téléphone A→B puis source C garde B ; contexte initial unique |

Compléter les cas performance de l'[architecture](architecture-contrats.md) : pages 25/100 et profondes, lignes SQL réellement lues, mémoire, N/10N, trafic mixte et saturation, import et worker concurrents. Une bonne pagination UI ne prouve pas la pagination SQL.

## Tests et clôture

Suites cibles : `tests/domain/prospection/`, `tests/application/prospection/`, API, PostgreSQL jetable, parcours navigateur CRM et tests transport simulé. Utiliser le [runner isolé backend](../../../../localeo-backend/scripts/validation/test_isolated.py) et les contrôles d'architecture locaux. Aucun accès à TEST partagé, aucune notification réelle implicitement incluse dans les tests.

Pour la clôture : **tests unitaires, intégration et fonctionnels de tous les critères actifs**, avec migrations/restauration synthétique, droits, fournisseurs simulés, PWA, import/reprise et capacité. Aucun pilote commercial, contact de prospect, validation municipale ou compte rendu UX externe ne constitue un critère de clôture. Des tests prévus ou ignorés ne valent jamais réussite. Le critère reporté reste visible comme hors V1 ; l’E71 reste En cours tant que tous les critères actifs ne sont pas vérifiés.

Les conditions d'activation réelle restent distinctes : configuration des transports, politique de conservation, hébergement et attribution des droits. Une campagne de test locale ne prouve pas un envoi au fournisseur ou une livraison réelle sur tous les navigateurs.

## Conservation et audit : décision restante ARB-07

Aucune durée CRM n'a été établie dans cette tâche. Ne pas importer par analogie les durées de conservation des achats/PIN. Avant données réelles, rattacher à la politique Localeo : prospects/contacts, notes/tâches, oppositions/preuves, fichiers/staging/rapports, clés de rapprochement/protections, idempotence, abonnements/intention/délivrance.

Prévoir déclencheurs et durées par catégorie, stockage SQL/objets/caches/sauvegardes, suppression/anonymisation cohérente et preuve de dry-run. Une lecture interne ne prolonge pas automatiquement la conservation. La purge des clés de source doit empêcher une réimportation silencieuse d'une personne opposée : référence minimale ou mise en quarantaine à requalifier selon la politique retenue, pas recréation aveugle.

Logs techniques : IDs, codes, versions, comptages, durée et corrélation uniquement. Aucun nom de personne, e-mail, téléphone, note, valeur de cellule, URL d'abonnement push ou lien signé. Rapports/fichiers privés à accès contrôlé, aucune copie en Git ou fixture réelle. Le modèle CSV versionné contient seulement ses en-têtes.

## Documentation, démonstration et impacts prévus à la spécification

Le bilan d’implémentation plus bas précise les éléments désormais livrés et testés.

- Backend : domaine/API/migrations/worker, CRM et droits ERP, générateur et tests. Enregistrer domaine/tags/contrats à l'implémentation ; pas de fausse route publiée ici.
- Guides canoniques à livrer : prise en main CRM, import/reprise, configuration des droits et rappels, règles de gain/opposition/carte. Ajouter leur export à `documentation.exports.json` quand consommés et tester l'accès du lecteur. La présente conception n'est pas le manuel d'un écran disponible.
- Générateur backend : prospects synthétiques deux périmètres, contacts/homonymes, commune dense/non localisée/hors catalogue/Outre-mer, opposition, tâches, gains et import interrompu. Transports neutralisés. Étendre registre de tables, nettoyage, sauvegarde/restauration pour les nouvelles dépendances.
- Pro/Animation/Marketplace : pas de mutation des données ou nouvelles API publiques ; contrôler les liens consommateurs si leurs destinations sont changées. Les comptes et parcours de vente existants restent propriétaires de leurs règles.
- Geo : fonds/attribution/couverture à configurer et à tester ; aucune donnée CRM transmise au fournisseur, cache communal indépendant des villes marchandes.

## Livraison et reprise prévues

1. Appliquer ARB-04b confirmé (une preuve/un dossier) et tester sur fixtures ; arrêter conservation et paramètres de fournisseurs avant activation réelle.
2. Livrer migration additive/readiness, catalogue/DTO des droits, preuve de vérification d’adresse E69 et backend, fonctionnalités désactivées. Aucune preuve d’adresse créée à partir du seul état ACTIF. Ne pas réserver un numéro SQL dans cette spécification.
3. Livrer PWA CRM, routes privées, manifest/SW, contrats et guides ; configurer stockage, workers bornés, carte et canaux.
4. Exécuter la matrice locale et CI, migration/restauration sur base jetable, tests E69 et non-régression email ; aucune autorisation CRM ajoutée en masse.
5. Après autorisation d'exploitation distincte : vérifier HTTPS/installation, attribution d'un profil de recette, aperçu CSV, notification interne et transports configurés. Les tests déjà effectués restent distingués des observations de cible.
6. En incident : désactiver commandes/imports et producteurs de rappels ; interrompre proprement les lots, préserver groupes validés et états de remise. Ne pas supprimer les tables ni retirer un ancien message déjà remis au fournisseur.

Runbooks à produire : fichier invalide/doublon, résultat inconnu après timeout, conflit tardif, mauvais rattachement, droits retirés pendant lot, tâche annulée pendant envoi, backlog de notifications, panne carte, purge et restauration. Mesures : durée/état des lots, groupes rejetés/protégés/conflits, âge des files, échec/expiration/issue incertaine transport, conflits de version, temps SQL/mémoire, jamais contenu personnel.

## Historique — phase de spécification

Sources backend et documentation examinées en lecture ; nouvelle spécification et gabarit documentaire écrits. Revue indépendante des contrats effectuée puis corrections vérifiées : cible des tâches/oppositions, droits de lecture des dossiers, projection cartographique distincte, namespace d'import et cardinalité des droits E69. Aucune contradiction résiduelle identifiée dans ces corrections.

Contrôles documentaires exécutés le **3 novembre 2026**, dans `localeo-projet`, sur la base `7e09409` avec les modifications E71 locales :

- `python scripts/check_guidance.py` : 95 guides, 1 077 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 11 documents, 305 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 134 sources vérifiées.
- Lecture CSV standard du gabarit : 21 en-têtes uniques, concordance exacte avec le dictionnaire ; exemple documentaire : 2 prospects, 2 contacts et 3 dossiers distincts. Contrôle des identifiants : CA-01 à CA-29 sans trou ; seul CA-24 reporté, 28 actifs.
- Les quatre dépôts applicatifs restent propres et inchangés par cette phase. Les travaux locaux étrangers à E71 sont préservés ; aucun commit/push demandé pour cette spécification.

Ces contrôles valident la documentation, pas un import applicatif. **Tests CRM, migrations, import réel, envoi fournisseur et déploiement : non exécutés**, aucun code CRM implémenté par cette demande.

### Reprise et finalisation V1.1 du 3 novembre 2026

Relecture à la demande utilisateur sur base documentaire `3cdbf32` et travaux E71
locaux conservés. L’utilisateur confirme **CSV standard seul** et **une preuve de
gain pour un seul dossier**. Carte interactive maintenue ; aucune question métier
ouverte ne bloque désormais les développements sur données synthétiques.

La revue des producteurs identifie deux lacunes corrigées dans la conception :

1. `UtilisateurInterne.modifier` incrémente `email_version` sans retirer ACTIF :
   l’état actif ne prouve pas la vérification de la nouvelle adresse. Le fait
   versionné est porté par Identité interne, repris uniquement depuis une
   invitation consommée correspondante ; préférence et remise transport le vérifient.
2. Les clés par source ne protègent pas deux créations ressemblantes simultanées de
   sources différentes. Le contrôle de candidats et la création partagent désormais
   une transaction SERIALIZABLE sur toutes les entrées concernées ; décision
   devenue obsolète = réexamen explicite, jamais fusion ou retry aveugle.

Les contrats d’import explicitent aussi sources, décisions d’aperçu, confirmation
et reprise, acteurs, résultats par groupe et états terminaux. Les critères CA-03,
10/11/12/22/27/28 portent les preuves correspondantes. Les tests applicatifs restent
**à produire lors de l’implémentation** ; aucun résultat de revue ne les remplace.

La politique de conservation, le choix/configuration du fond cartographique et
les paramètres de transport restent des conditions d’activation avec données
réelles. Ils ne sont ni des pilotes obligatoires ni des preuves produit acquises.

Contrôles de finalisation exécutés sur cette V1.1 :

- Revue indépendante des contrats après correction : les deux lacunes ci-dessus
  sont levées ; aucune contradiction bloquante identifiée dans les sections relues.
- `python scripts/check_guidance.py` : 95 guides, 1 077 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 11 documents,
  305 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 134 documents vérifiés.
- `git -c core.safecrlf=false diff --check` : réussi.
- Contrôle CSV avec la bibliothèque standard Python : 21 colonnes uniques en
  concordance avec le dictionnaire ; exemple de 2 prospects, 2 contacts et 3 dossiers.
  Les 29 identifiants sont présents sans trou ni doublon dans le backlog et la
  matrice ; 28 actifs, CA-24 reporté.
- Les quatre dépôts applicatifs sont propres et inchangés. Seul le dépôt
  documentaire est modifié pour E71 ; les autres travaux locaux sont préservés.

Ces résultats sont documentaires. Aucun test produit CRM, aucune migration,
aucun import réel ni déploiement n’ont été exécutés. Aucun commit ou push n’est
réalisé dans cette phase de spécification.


## Implémentation locale — 3–4 novembre 2026

État roadmap : **En cours**. Le périmètre fonctionnel est implémenté dans le
backend (PWA `/internal/crm/`, domaine/application/persistence, API, droits ERP,
imports et rappels). La documentation canonique porte le [guide utilisateur](guide-utilisateur.md),
l’[exploitation](exploitation.md), le [contrat extrait](openapi.json) et le modèle CSV.
Les trois frontends publics/professionnels ne consomment pas ces nouveaux contrats ;
ils restent inchangés. Aucun sixième dépôt n’est créé.

### Preuves exécutées

Dernier passage consolidé sur les fichiers figés : **888 tests réussis en
84,22 s**, couvrant domaine, intégration, sécurité, PWA et architecture. Deux tests
de capacité import sont désélectionnés car mesurés séparément (aucun skip assimilé
à un succès). Les 28 avertissements concernent l’adaptateur datetime SQLite
déprécié ; aucun échec dans cette suite. La migration-restauration finale v292, index compris,
est rejouée avec succès en **42,47 s**. Les deux parcours Chromium CRM et rappels
sont rejoués avec succès après les corrections d’import et de navigation.
Les **13 tests de limite HTTP** passent également : import CRM de 10 Mio,
enveloppe multipart bornée, corps fragmenté ou taille déclarée erronée,
limite générale des autres routes conservée.

Commande de la suite consolidée, depuis le backend avec le runner isolé et
l’URL explicite du PostgreSQL jetable :

```console
python scripts/validation/test_isolated.py --postgres-test-url <postgresql-jetable> tests/domain/prospection tests/domain/identite_acces/test_crm_identite.py tests/application/test_crm_identite_preuve.py tests/api/test_crm_rappels_api.py tests/security/test_crm_core_postgres.py tests/integration/test_crm_rappels_postgres.py tests/integration/prospection tests/security/test_crm_pwa.py tests/security/test_crm_nominatif_postgres.py tests/unit/test_demonstration_crm.py tests/application/exploitation/test_schema_readiness.py tests/security/test_pwa_lifecycle.py tests/security/test_request_body_limits.py tests/unit/test_crm_agregats.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -k "not import_10000_lignes_budget_postgres and not profil_dix_groupes" -q --tb=short -s
```


- Tests domaine, PostgreSQL jetable et HTTP : créations atomiques, contacts et
  dossiers distincts, six étapes, pertes/pauses/réouvertures, preuves canoniques,
  attribution exclusive concurrente, idempotence, versions, notes/corrections,
  oppositions et invalidation des rappels.
- Imports : parseur strict, staging sans effet portefeuille, INIT/UPSERT,
  protection des champs effacés, plan immuable, rapprochement explicite,
  concurrence entre sources, droit retiré/reprise, panne atomique et rapport.
- Identité/rappels : droits sans grant implicite, preuve d’adresse liée à la
  version d’invitation, relecture avant remise, réaffectation, préférence,
  expiration appareil, issue transport incertaine et absence de verrou métier
  pendant le réseau. Le batch générique ne remet pas les e-mails CRM.
- **36 tests PWA/HTTP** réussis : activation fermée, routes profondes, retour de
  connexion contrôlé, ressources neutres, cache privé interdit, guide canonique,
  cycle partagé de mise à jour et conservation des autres PWA.
- Navigateur Chromium : création prospect+dossier, note conservée après 409 et
  rejeu de même clé, pause Paris→UTC, sept vues à **1440/1280/768/390/360/320 px**, absence de
  débordement horizontal/double défilement, révocation en cours de saisie,
  accès lecteur, aucun stockage local de données privées. Captures examinées
  dans le répertoire privé `tmp/crm-qa/` du backend.
- Worker/notifications navigateur : payload hostile ignoré, destination CRM
  fermée, nettoyage limité aux caches CRM, opt-out malgré canal désactivé,
  CSRF/idempotence et effacement de l’écran après un refus d’accès.
- **Migration complète et restauration réelle** : base vide → baseline v147 →
  v292 (189 entrées de journal), rejeu sans migration, jeu synthétique CRM,
  archive `pg_dump` custom, `pg_restore --clean --single-transaction`,
  vérification des données et nouveau rejeu. Test PostgreSQL 18 réussi,
  aucun schéma simulé et aucune ancienne migration réécrite.
- Générateur : scénario synthétique deux périmètres, note, tâche interne et
  sollicitation bloquée via les services ordinaires ; registre de 20 tables
  CRM, contrôle de schéma et neutralisation des traitements à la restauration.

Suites concernées dans le backend : `tests/domain/prospection/`,
`tests/domain/identite_acces/test_crm_identite.py`,
`tests/application/test_crm_identite_preuve.py`,
`tests/security/test_crm_core_postgres.py`, `tests/security/test_crm_pwa.py`,
`tests/api/test_crm_rappels_api.py`, `tests/integration/prospection/`,
`tests/integration/test_crm_rappels_postgres.py`,
`tests/integration/test_crm_migration_restauration.py`,
`tests/unit/test_demonstration_crm.py`, `tests/browser/crm.cjs` et
`tests/browser/crm-rappels.cjs`.

Les transports sont simulés. La base utilisée est exclusivement
`localeo_audit_test`/`localeo_audit_migrations_test` sur le cluster local jetable,
via `scripts/validation/test_isolated.py --postgres-test-url …`.

### Revues indépendantes et corrections intégrées

Les revues croisées ont corrigé : distinction liée aux candidats et versions,
contrôle des droits métier sur les preuves, refus du gain Coffrets à partir d’un
OnBoard Animation seule, normalisation import partagée, file bornée et curseurs
liés à l’autorité, garde des comptes nominatifs, accès documentaire, préservation
de la saisie et de la clé après résultat incertain, opt-out et recherche des
responsables. La dernière revue UI corrige également la référence de rapprochement,
la limite HTTP dédiée au CSV 10 Mio (enveloppe bornée, autres routes inchangées),
l’affichage des anomalies/lignes CSV, la pagination des sources, les commandes
réservées au confirmateur et le lien direct après connexion. Un test de registre
fermé couvre toutes les routes CRM nominatives. La charge mixte fonctionnelle
importe 200 structures pendant 40 ajouts de notes rejoués et des lectures concurrentes :
aucune note perdue ni import doublé.

Aucune donnée privée ni permission réelle n’a été utilisée.

### Capacité mesurée localement

**Projections finales : 23 tests réussis en 219,01 s**, dont les deux régimes
10N, avec 100 % des requêtes servies. L’attente des files fait partie du temps
mesuré. Deux cartes et un tableau peuvent s’exécuter simultanément par processus ;
aucun résultat privé n’est mis en cache. Les seuils initiaux restent inchangés.

| Jeu final, dix lecteurs | Carte p95 / p99 | Tableau p95 / p99 | Résultat |
| --- | --- | --- | --- |
| 10N frais | 1 449,73 / 1 501,10 ms | 557,85 / 619,93 ms | Tous les budgets respectés |
| 10N entretenu par VACUUM | 1 920,56 / 1 924,12 ms | 575,14 / 637,87 ms | Tous les budgets respectés |
| Retour à dix après vingt, frais | 1 591,12 ms p95 | 735,95 ms p95 | Tous les budgets respectés, fenêtre 4,44 s |
| Retour à dix après vingt, entretenu | 1 640,47 ms p95 | 726,13 ms p95 | Tous les budgets respectés, fenêtre 4,54 s |

À vingt lecteurs, carte et tableau dépassent les budgets (jeu entretenu :
2 800,30 et 1 615,58 ms p95) ; les listes et recherches restent sous leurs budgets.
Le dimensionnement vérifié est donc dix lecteurs sur cette cible locale, pas un
SLA HTTP de production. La marge de la carte reste réduite sur le régime entretenu. Les rapports finaux
`final-files-separees-frais.json`, `final-files-separees-etabli.json` et les plans
`final-crm-plans-*.json` figurent dans `tmp/e71-mesures-20261104/` du backend ;
`sources-files-separees-finales.json` conserve les empreintes des sources testées.

Les mesures intermédiaires ci-dessous expliquent les corrections et restent
conservées ; elles ne remplacent pas le rejeu final.

Les seuils des tests n’ont pas été modifiés pour obtenir ces résultats. Les premières
mesures dépassaient les budgets carte/import ; les index, projections SQL et échanges
par groupe ont été optimisés en conservant droits, SERIALIZABLE, atomicité et fencing.

- Import 10 000 lignes / 10 000 structures : dépôt **0,957 s** (hors upload),
  aperçu **3,909 s**, durée totale **86,988 s**, mémoire additionnelle **12 Mio**.
  Seuils respectifs : 1 s, 120 s total et 128 Mio. Autorité de fixture pour cette
  mesure ; authentification et révocation réelles couvertes séparément. Boucle de
  service hors HTTP/cadence d’ordonnanceur : ce résultat ne valide pas un cron lent.
- Portefeuille 100 000 prospects, 300 000 dossiers, 600 000 tâches et 1 million
  d’événements : dix lecteurs, 100 requêtes mixtes en **3,12 s**. p95 par opération :
  liste25 **77,54 ms**, liste100 **85,37 ms**, recherche **129,50 ms**,
  carte **1 265,16 ms**, tableau **568,08 ms**. Budgets respectés lors de ce passage seulement.
  Ces mesures portent sur la persistance, pas sur un SLA HTTP ou un hébergement réel.

- Avant la correction finale des agrégats, une campagne sur un jeu **fraîchement chargé**, après ANALYZE mais
  avant VACUUM, constate à dix lecteurs **1 110,88 ms** p95 au tableau de bord
  (budget 1 000 ms : **échec**) et **1 921,22 ms** à la carte (budget respecté).
  À vingt lecteurs, saturation : p95 liste100 **3 104 ms**, carte **3 729 ms**,
  tableau **2 679 ms**. Les paliers 1/5 passent. Le premier résultat favorable
  ne remplace pas ce contre-exemple ; le test nominal garde son assertion.
- Croissance indépendante de l’historique : 10 000 prospects et 1 million
  d’événements, historique paginé sans doublon ; médianes liste25/100
  **2,01 / 3,89 ms**, recherche **13,24 ms**, carte **37,49 ms**, tableau **12,02 ms**.
  Les projections ne lisent pas le journal des notes.

Artefacts synthétiques locaux : `tmp/e71-mesures-20261104/` dans le backend
(N, historique seul et 10N frais avec les paliers). Non versionnés, ils contiennent
les distributions et plans ; les chiffres et limites durables sont consignés ici.

- Toujours avant la correction finale, mesure après **VACUUM explicite** : 1/5 lecteurs respectent les budgets,
  mais à dix lecteurs la carte atteint **2 404,12 ms** p95 / **3 153,41 ms** p99 et
  le tableau **1 928,83 ms** p95 / **2 313,26 ms** p99. **Échec nominal confirmé**.
  Vingt lecteurs saturent les cinq opérations mesurées. Au retour immédiat à dix
  (fenêtre 8,07 s), carte **3 108,72 ms** p95 et tableau **1 472,57 ms** p95 :
  retour à la normale non démontré. EXPLAIN tableau avant/après VACUUM :
  **159,84 → 125,81 ms** ; carte **635,61 → 470,95 ms**. Les scans des agrégats
  (100 000 organisations / 300 000 dossiers) restent coûteux sous concurrence.
  Les artefacts `10N-etabli-vacuum-paliers-et-retour.json`, `plans-frais.json` et
  `plans-vacuum.json` complètent le répertoire indiqué plus haut.

- **Rappels — avant optimisation des préférences, cadence d’un passage/minute** :
  10 000 tâches, 20 000 intentions (internes et externes), 5 000 e-mails et
  5 000 push simulés, aucun annulé/incertain. Vidage en **270,237 s** (budget 600 s :
  respecté) mais 99 % préparées en **139,529 s** (budget 120 s : **échec**, +19,529 s).
  Les protections de révocation, timeout et équité sont conservées ; l’ancienne
  mesure favorable de 105,10 s ne valide pas ce dernier état. Dix tests fonctionnels
  supplémentaires passent : sessions administrateur, authentification et contention
  avec libération du slot. Revue indépendante des trois corrections terminée.
  RSS du processus pytest partagé : base **218,238 Mio**, pic **265,195 Mio**,
  delta **46,957 Mio**. Le delta inférieur à 64 Mio ne valide pas la limite absolue
  d’un worker dédié. Rapport final `tmp/crm-performance-rappels.json` ; rapport
  initial séparé `tmp/crm-performance-rappels-initial.json`.

### Optimisations ciblées et rejeu

Les préférences de rappel sont lues sous verrou une seule fois par transaction,
avec invalidation à la modification, au commit et au rollback. Aucun droit ni
fait d’autorité n’est conservé entre transactions. **28 tests ciblés réussissent**.
Le comparatif indicatif de 1 000 tâches (trois paires) réduit la médiane de
8,550 à 6,772 s ; ce petit jeu ne remplace pas le scénario de capacité.

Sur les **10 000 tâches**, avec un worker, même cadence de 60 s et mêmes contrôles,
la préparation de 99 % atteint **133,303 s** : le budget de 120 s reste dépassé.
Les 10 000 remises terminent en **256,138 s**, sous le budget de 600 s.
Dix tests de non-régression supplémentaires passent. RSS partagé : pic **258,54 Mio**,
delta **40,152 Mio** ; le budget absolu de 64 Mio n’est toujours pas validé.
Rapports locaux : `tmp/crm-performance-rappels.json` et comparaison conservée
`tmp/crm-performance-rappels-avant-optimisation-preferences.json`.

Une seconde mesure avec **deux workers** mais toujours 50 s d’admission donne
**128,780 s** pour 99 % des intentions commitées (échec 120 s), **261,650 s**
pour les 10 000 remises (réussite 600 s). Aucun doublon : 5 000 e-mails et
5 000 push simulés, aucun annulé/incertain. Le rapport est conservé sous
`tmp/crm-performance-rappels-deux-workers-admission50.json`.

Le dernier changement de concurrence compte les insertions réellement créées
(`RETURNING`) et réserve la préparation d’une tâche par un verrou transactionnel
non bloquant. Les contrôles d’autorité restent inchangés. La revue indépendante a
également corrigé le report entre sélection et relecture : aucun marqueur n’est
créé avant la nouvelle échéance, qui reste éligible ensuite. **29 tests ciblés**
réussissent sur cet état. La fenêtre d’admission passe ensuite à 58 s pour réduire
le temps inactif du passage, sans modifier les budgets de validation.

### Résultat final des rappels

**Deux workers, admission 58 s, cadence 60 s**, sur les mêmes 10 000 tâches :

- 99 % des intentions **commitées**, observées par une connexion indépendante :
  **124,666 s**, soit **échec du budget 120 s de 4,666 s**.
- 10 000 remises en **235,753 s**, sous le budget de 600 s, sur quatre passages.
- 5 000 e-mails et 5 000 push simulés ; **zéro doublon, annulation ou incertitude**.
- RSS du processus partagé : pic **133,629 Mio**, delta **23,613 Mio**. Ces valeurs
  ne valident pas un RSS absolu de 64 Mio par worker isolé.
- Les quatre tests fonctionnels ciblant contention/slots, concurrence,
  restitution du claim et report à une nouvelle échéance réussissent.

Rapport local conservé :
`tmp/crm-performance-rappels-deux-workers-admission58-final.json`.
Le délai de préparation reste une réserve explicite ; aucun seuil n’a été
modifié et le test de capacité reste en échec sur cette assertion. Les transports
réels, leurs quotas et latences ne font pas partie de cette mesure.

### Restant avant vérification intégrale

1. **CA-06/26/27 — préparation des rappels** : réduire la préparation de 99 %
   des intentions de **124,666 s à 120 s** sur le protocole final (deux workers,
   admission 58 s, cadence 60 s, 10 000 tâches). La remise respecte son budget.
   La réserve de préparation reste ouverte, sans changement d’assertion.
2. **Mémoire des rappels — dépassement de conception** : un processus Python
   neuf sur Windows, sans pytest ni FastAPI, atteint déjà **84,31 Mio RSS** à l’import de la
   composition (budget absolu 64 Mio), avant toute tâche. Étapes mesurées :
   Python 15,91 ; isolation/pilote PostgreSQL 34,65 ; SQLAlchemy 53,18 ; modèles
   ORM partagés 73,76 ; identité 76,50 Mio. Une composition dédiée plus légère
   et une mesure sur la cible Linux sont nécessaires ; aucun budget n’est
   réinterprété en mémoire additionnelle. Cette mesure ne contacte aucune base.
   Rapport et commande reproductible : `tmp/crm-memoire-worker-isole.json`
   dans le backend (artefact local synthétique, hors Git).
3. La charge mixte fonctionnelle import/notes/lectures est vérifiée, mais pas un
   protocole complet HTTP à 1/5/10/20 utilisateurs mêlant tous les transports,
   imports et rappels sur une cible dimensionnée. Les temps de persistance ne
   constituent pas une mesure de latence HTTP de bout en bout.

### Limites et activation

La couverture n’est pas déclarée intégralement clôturée tant qu’un budget ou un
scénario reste ouvert. Les conditions d’activation demeurent ARB-07 (conservation),
choix du fournisseur de tuiles, secrets VAPID/e-mail, planification des workers et
attribution explicite des droits. Aucun pilote ni validation UX externe n’est
exigé pour les tests produit. Aucun commit, push, déploiement ou migration TEST
n’est réalisé dans cette tâche.

### Contrôles documentaires finaux

- `python scripts/check_guidance.py` : 95 guides, 1 081 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 13 documents,
  374 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 137 sources vérifiées.
- Contrat CRM régénéré hors ligne : 41 chemins et 28 schémas, réponses 503 des
  agrégats incluses. `git diff --check` réussi dans les deux dépôts modifiés.
- Captures supplémentaires 360 et 1280 px examinées après le dernier parcours
  navigateur ; aucune correction d’interface supplémentaire nécessaire.

## Carte Nouvelle-Aquitaine — correctif du 4 novembre 2026

Demande : limiter la carte régionale et permettre de filtrer ses douze
départements. La carte nationale et ses raccourcis outre-mer ne correspondaient
plus au périmètre souhaité. Correction sur les changements locaux issus du
backend `32106fd` et du dépôt documentaire `17218a0`.

La projection SQL impose les départements de Nouvelle-Aquitaine avant agrégation,
indépendamment de l’emprise rectangulaire et du code postal. Le filtre département
et la région sont conservés en ouvrant la liste et sa pagination. La liste générale
reste nationale ; les fiches sans INSEE disposent d’un accès distinct tous territoires.
Le cadrage initial, le dézoom et le recentrage utilisent l’enveloppe régionale ou
départementale, y compris lorsqu’aucun prospect ne correspond aux filtres.

Preuves locales :

- **43 tests Python réussis** : API HTTP, PostgreSQL jetable, combinaisons de
  filtres, exclusion d’une commune hors région pourtant dans l’emprise, douze
  départements, compteurs, pagination, liaison des curseurs aux filtres,
  plafond de 500 groupes et portefeuille synthétique de 10 000 prospects.
- **652 contrôles d’architecture et de recensement validés** : 651 lors de la
  suite initiale ; le dernier test, affecté par la capture Windows de `git init`
  (`WinError 6`), réussit inchangé avec `-s`.
- `node tests/browser/crm.cjs` : parcours CRM réussi avec Leaflet réel et tuiles
  synthétiques locales. Sélection Gironde, transmission des filtres lors du zoom,
  dézoom borné, liens vers la liste et une commune, accès sans commune, état vide
  Charente, réinitialisation et repli sans fond cartographique vérifiés. Sept vues
  contrôlées de 320 à 1440 px ; captures régionales à 320 et 1280 px.
- Documentation : `python scripts/check_guidance.py` et
  `python scripts/sync_documentation.py --check-sources` réussissent.

Contrat OpenAPI canonique et guide utilisateur mis à jour. Générateur inchangé :
les nouveaux filtres sont des paramètres de lecture facultatifs, sans modification
du format des fiches ou de leur création. Aucune migration, réparation de données,
clé supplémentaire ni changement de fournisseur de tuiles. Les règles métier et
permissions restent inchangées. La campagne complète de charge à 100 000 prospects
et la vérification sur TEST ne sont pas rejouées ; les réserves antérieures de
performance des rappels restent ouvertes. Aucun commit, push ou déploiement dans
ce correctif.

## Correctif du 4 novembre 2026 — Saisie des prospects en Nouvelle-Aquitaine

La restriction de carte ne limitait pas les écritures. Le domaine Prospection
porte désormais la règle des douze départements : INSEE obligatoire pour toute
création et tout changement effectif de localisation. Les entrées manuelles et
imports INIT/UPSERT l'appliquent ; les fiches historiques hors région ou sans
commune conservent leur suivi et leurs contacts modifiables.

Le formulaire recherche puis sélectionne la commune. Les mutations manuelles
utilisent le référentiel local `crm_communes`, alimenté uniquement par les
réponses de la recherche serveur ; le réseau précède la transaction courte de
cache et reste absent des transactions métier. Les imports contrôlent hors
réseau le territoire déclaré par INSEE, sans certifier l'existence du code ni
la concordance de son libellé. Un ancien plan incompatible est recalculé puis
refusé avant toute mutation du groupe.

Preuves locales :

- Deux tests d'import ont reproduit les refus manquants avant correction.
  **72 scénarios distincts d'import réussis**, domaine/CSV/HTTP/PostgreSQL et
  charge mixte, dont 10 000 lignes. Création absente/hors région, conservation
  des localisations historiques, protections et plans devenus obsolètes couverts.
- **74 tests ciblés serveur réussis** (73 dans la suite finale, puis un test
  PostgreSQL supplémentaire) : domaine, application, HTTP, persistance réelle,
  carte, démonstration et charge mixte. Vérification spécifique de l'ordre
  recherche réseau avant SQL, du cache réel, du nom canonique, du code inconnu,
  de l'idempotence et des refus sans effet.
- **653 contrôles d'architecture et de recensement réussis** avec `-s` et sortie
  fichier pour éviter le problème Windows de capture subprocess ; assertions
  inchangées. PostgreSQL jetable arrêté après les contrôles.
- `node tests/browser/crm.cjs` réussi : commune requise, sélection régionale,
  absence de résultat, erreur de recherche sans perte de sélection, réponse
  périmée ignorée, modifications non géographiques de fiches historiques,
  INSEE sans nom conservé, localisation avec confirmation d'homonymes. Sept vues
  de 320 à 1440 px ; formulaires à 320/1280 px inspectés visuellement.
- Revue indépendante des règles/imports/cache et du formulaire ; les deux
  écarts détectés (sélection historique sans nom, confirmation d'homonymes)
  sont corrigés et couverts par les tests navigateur.
- Documentation : guides, liens des Markdown modifiés et sources exportées
  validés ; `git diff --check` réussi dans backend et projet.

**Réserve de charge distincte** : le banc PostgreSQL à 100 000 prospects dépasse
le budget carte de 2 s p95 (2,884 s base fraîche ; 3,819 s après vacuum). Les cas
à 10 000 passent ; listes et tableaux de bord passent à dix lecteurs. Le
correctif de saisie ne change pas la requête de lecture cartographique (seule la
constante des départements est partagée avec le domaine). Ces échecs restent
consignés, sans affaiblissement du seuil ni conclusion de validation complète
des performances. Ils ne constituent pas un refus fonctionnel de saisie.

CA-01/08/09/10/14 et documentation fonctionnelle/technique actualisés ; contrat
OpenAPI canonique régénéré, exemples CSV et fixtures du générateur de démonstration
adaptés. Aucune migration requise : colonnes et cache communal existent déjà.
Aucun import réel, envoi, réparation de données, commit, push ou déploiement TEST.
Les autres travaux locaux des dépôts sont conservés.
