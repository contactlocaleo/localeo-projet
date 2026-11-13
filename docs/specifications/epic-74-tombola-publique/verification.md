# E74 — Preuves attendues et recette

Revue actualisée le 13 novembre 2026. [Périmètre](README.md), [contrats et invariants](architecture-contrats.md), [critères canoniques](../../roadmap/en-cours/epic-74-tombola-publique-backlog.md).

## Revue de clôture — 13 novembre 2026

**Clôture bloquée ; état En cours et chemin du backlog conservés.** La demande
de clôture ne retire aucun des 16 critères. Deux écarts principaux subsistent :
le refus du stockage IndexedDB empêche l’inscription dans Live (CA07/11), et la
preuve complète de capacité spécifiée reste incomplète (CA15). Le rendu final
des flyers des trois dotations et la restauration d’une sauvegarde contenant
des gains restent aussi à compléter dans cette campagne. Une activation ou un
pilote déployé ne sont pas ajoutés comme nouvelles conditions de clôture.

### Révisions, périmètre et preuves renouvelées

Bases Git : projet `c28bbed351a0d55bb7425b14bb33d06ce4ad91a1`, backend
`d4ca2788448e67c21b9ebf2c6459f81b570f39a4`, Animation
`7104f9be04fa63cfb479fbd04aa746787c125b54`, Marketplace/Live
`afe7139c8b12d9d7dbfaf9c6ac4790e75016c1b0`, Pro
`4b40b4adf864beeb55e342b86379b2a61b075ef3`. Les preuves ci-dessous portent
sur ces bases, plus les corrections de tests et de documentation de cette revue,
sans changement du code produit. Les dix fichiers déjà modifiés pour la fin
d’animation E73 sont préservés ; roadmap et index comportent des lots distincts.

| Contrôle exécuté | Résultat et preuve locale | Portée |
| --- | --- | --- |
| Domaine, application, API et générateur unitaire E74 | **98 succès**, `localeo-backend/tmp/e74-cloture-isoles.xml` | Quatre champs, inscription immédiate, ancien contrat, capacité de lecture, refus et coordonnées explicites du générateur. |
| Architecture et recensements obligatoires | **709 succès**, `tmp/e74-cloture-architecture.xml` | `tests/architecture`, `test_domain_dedicated_classes.py`, `test_use_case_business_test_coverage.py`. |
| Inscription, publication, gains et parcours PostgreSQL | Première campagne **70 succès, 1 échec** d’attente périmée, `tmp/e74-cloture-postgres.xml` ; contrôle corrigé **2 succès**, `tmp/e74-cloture-vision-final.xml` | Quatre suites `test_tombola_publique_postgres.py`, `test_tombola_publique_publication_postgres.py`, `test_tombola_publique_gains.py`, `test_tombola_publique_parcours_postgres.py`. L’échec Vision360 attendait un prénom absent après avoir créé « Léa ». Deux cas prouvent désormais identité actuelle masquée et identité historique absente. |
| Recherche participants ajoutée depuis la preuve historique | **1 succès** dans `tmp/e74-cloture-postgres-complement.xml` | `test_recherche_email_litterale_reference_exacte_curseur_et_dto` ; ce rapport contient aussi une première tentative Vision360 échouée, remplacée par le rapport final ci-dessus. |
| Chaîne complète de migrations, sauvegarde/restauration et générateur complet | Première campagne **2 échecs d’assertions périmées**, puis **2 succès**, `tmp/e74-cloture-migrations-initial.xml` et `tmp/e74-cloture-migrations-final.xml` | Chaîne courante jusqu’à v314, présence/ordre v288/v289, modèle inactif, rejeu et `pg_dump/pg_restore`. Générateur sans commerce, droits/quota réels, quatre coordonnées, anciens états et PDF local. |
| Contrats Node Live et Animation | **14 succès Live**, **7 succès Animation** | Live : `tombola-email`, `animation-engine-registry`, `catalogue-pagination` ; Animation : `public-tombola`, `animation-engine-registry`, `publication-http-contracts`. Commandes HTTP simulées et négociation. |
| Live navigateur | **54 succès**, run `2026-11-13T12-49-15-123Z-ovwEVk` (7,3 min) | E74, identité des quatre moteurs, communes et carnet ; 320/390/1280 px et texte à 200 %, API synthétiques. Le défaut IndexedDB ci-dessous est une reproduction supplémentaire. |
| Animation navigateur | **3 parcours réussis**, 1280/390/320 px ; `node tests/browser/public-tombola.mjs` | Build isolé réussi, captures `tmp/public-tombola-qa/*.png`. Présélection du modèle, dialogue accessible et endpoints négociant la capacité actualisés dans le banc ; création/assistant/participants/flyer testés. Avertissement de bundle >500 kB conservé. |

PostgreSQL **18**, instance jetable sur `127.0.0.1:55834`, bases réservées
`localeo_audit_test` et `localeo_audit_migrations_test`, fixtures à schémas isolés.
Toutes les recettes backend utilisent `scripts/validation/test_isolated.py` ;
aucun `.env` opérateur, fournisseur ou base d’exploitation. Les e-mails sont
capturés en outbox. Les suites se recouvrent : ne pas additionner leurs comptes.
Les rapports XML sont des sorties ignorées, les tests restent versionnés.

Les corrections de tests conservent les assertions métier : v289 n’est plus
supposée dernière migration du dépôt, les coordonnées actuelles remplacent
l’ancienne attente de prénom nul, et un cas distinct conserve la lecture
d’une identité historique absente. Aucune assertion de quota, qualification,
preuve, outbox, restauration ou masquage n’a été supprimée pour obtenir du vert.

### Écart navigateur reproduit

Sur Live, remplacer `indexedDB.open` dès le chargement par une fonction lançant
`DOMException('Storage unavailable', 'SecurityError')`, puis ouvrir le formulaire
d’une tombola publique publiée : `useLiveRegistrations` passe en erreur et
`LiveRegistrationGuard` affiche « Vérifier mon inscription ». À 390 px,
**aucun formulaire, aucun champ d’identité et aucune commande d’inscription**.
La préférence facultative devient ainsi un prérequis au jeu, contrairement au
[comportement accepté](README.md#suivi-de-la-commune-et-notifications).

Preuves Chromium :
`localeo-marketplace/test-results/visual-runs/2026-11-13T12-49-15-123Z-ovwEVk/indexeddb-review/result-confirmed.json`
et `indexeddb-denied-focus-390.png`. Empreinte des sources Live :
`775f0562f525612a55cf39cb88639578eae651450e08b24563d9aaff3a730782`.
Le scénario historique « stockage refusé » ne refusait que `localStorage.setItem`
après affichage du formulaire ; son succès ne couvre pas ce cas.

Action nécessaire : distinguer indisponibilité du stockage et incertitude sur
une inscription existante, permettre la participation dans le premier cas,
préserver déduplication/reprise serveur et récupération par e-mail. Ajouter une
preuve navigateur avant/après correction, puis renouveler les quatre moteurs.
La correction de ce garde partagé est un travail produit restant, pas une
modification implicite de la présente clôture documentaire.

Autres écarts de présentation établis par la revue, sans correction produit dans
ce lot : la fiche Live (`livePublicDetailPresentation.mjs`), le flyer Animation
(`FlyerWorkspace.tsx`) et sa configuration (`App.tsx`) annoncent encore surtout
e-mail/règlement ; `PublicTombolaParticipants.tsx` indique « Prénom facultatif ».
Aligner ces textes sur les quatre champs actuels en distinguant les anciennes
valeurs manquantes. Le succès `PublicTombolaRegistration.jsx` annonce un lien
« envoyé » dès le 202 ; il faut distinguer mail préparé et livraison effective.
À 320 px/texte 200 %, l’introduction du formulaire conserve une taille fixe de
13 px : pas de débordement observé, mais agrandissement incomplet de cette phrase.

### Matrice actuelle des 16 critères

Les chemins backend sont relatifs à `localeo-backend`. Les preuves historiques
restent ci-dessous pour leur périmètre exact ; elles ne valent pas réexécution.

| Critère | Spécification et code effectif | Preuve actuelle / documentation | Verdict |
| --- | --- | --- | --- |
| CA01 | Catalogue standard, `catalogue_modules.py`, stratégie Tombola publique | Tests domaine et générateur avec droits réels ; guide organisateur | **Vérifié** |
| CA02 | `ServiceCommandesPublicationAnimation` → `ServiceDroitsModules` → compte d’usage | Publication/rejeu PostgreSQL et générateur : un débit, refus sans abonnement ; conditions acquises non modifiées | **Vérifié** |
| CA03 | Politique de publication, compilation et dotation externe | Création/publication sans commerce, refus sans lots, règlement/dates, générateur complet | **Vérifié** |
| CA04 | Assistant Animation, autorisations organisation/commune backend | Recette navigateur et tests de lecture hors périmètre ; aucun changement de permissions | **Vérifié dans les scénarios ciblés** |
| CA05 | Flyer public et route Live vers l’animation | URL sans accès personnel, ancienne ouverture sans mutation, QR/PDF du générateur ; scan physique non requis | **Vérifié** |
| CA06 | Présentation du flyer et socle PDF E73 | Prévisualisation, quantités et absence de parcours commerçant ; PDF externe généré ; texte des coordonnées incomplet et rendu final personnalisé des trois modes non relu | **Partiel** : aligner les textes et compléter les rendus |
| CA07 | Identité domaine → `ServiceVerificationEmailAnimation.inscrire` ; formulaire partagé | SQL réel quatre champs, preuve/mail atomiques et identité protégée ; navigateur bloqué si IndexedDB refusée | **Partiel** : défaut Live reproduit |
| CA08 | Reçus, verrous et unicité participant/e-mail | Concurrence, rollback, reprise après perte de réponse, aucun accès personnel dans réponse publique | **Vérifié** |
| CA09 | Politique d’ouverture, contrôle après verrou et anciens liens | Refus avant/après période, clôture et courses d’horloge PostgreSQL | **Vérifié** |
| CA10 | Préférence de commune séparée de qualification/consentement | Refus volontaire du suivi sans effet sur les chances ; aucune prospection/Push implicite | **Vérifié** pour stockage disponible ; panne traitée en CA11 |
| CA11 | Mes communes, stockage local facultatif et garde d’inscription | Ajout/retrait/limite testés ; indisponibilité IndexedDB bloque le formulaire | **Non satisfait** |
| CA12 | `ParticipantsEmailLecture`, gel et preuve native | Pagination/recherche/totaux, gel revalidant la preuve, distinction déclaré/vérifié ; profil mémoire traité en CA15 | **Vérifié fonctionnellement** |
| CA13 | Population figée et services de tirage E73 | Gains PostgreSQL trois modes, zéro/insuffisance/suppléants/rejeu | **Vérifié** |
| CA14 | Gains, notification et suivi de remise existants | Parcours réel externe et bon numérique ; distribution Coffrets simulée à sa frontière, invariant tirage/stockage réel | **Vérifié dans les frontières testées**, limite Coffrets conservée |
| CA15 | Routes protégées, limiteurs, curseurs et traitements bornés | Refus/permissions/erreurs privés testés ; capacité complète et RSS manquants | **Partiel** |
| CA16 | Registres, migrations additives, démonstration et anciens moteurs | Migration/rejeu/restauration, générateur quatre champs, recettes des moteurs ; sauvegarde de gains non couverte par cette restauration | **Partiel** pour la restauration complète spécifiée |

### Contrats, documentation et impacts

Comparaison hors ligne : E41/E42 correspondent aux routes et composants du
producteur actuel ; seule la métadonnée `/info/version` diffère. La copie OpenAPI
Animation est identique au canonique. Les **98 exports moteur Live sont conformes**.
Le contrôle Animation échoue sur `participation-live.schema.json` et `manifest.json` :
deux champs optionnels d’aperçu de dotation Live manquent dans cette copie.
Le consommateur direct Live les possède ; aucun défaut E74 démontré sur Animation.
Cette dérive doit être synchronisée avec son producteur, sans la confondre avec
un refus du nouveau formulaire. OpenAPI omet aussi certains refus effectivement
gérés (`409/410/429`, curseur invalide) : enrichissement documentaire du producteur
restant, sans prétendre qu’une régénération seule le corrige.

Les guides d’identité, générateur et README Animation sont corrigés ; l’index
des spécifications qui annonçait encore E74 « À faire » et sans implémentation
est aligné sur la roadmap. Aucun changement de règle, API, migration, donnée,
permission, fournisseur ou configuration produit dans ce lot ; donc aucun
nouveau secret, tarif, DNS ni job. Les chemins exportés ne changent pas.
La publication ERP d’un bundle et l’état déployé ne sont pas vérifiés ici.

### Lot de commit et livraison

Lot projet : bilan E74, architecture, backlog, roadmap/index et guide générateur.
Message proposé : `docs(e74): documenter la revue de clôture et les écarts restants`.
Lot backend : quatre fichiers de tests E74 (migration, générateur, Vision360,
capacité). Message : `test(e74): actualiser les preuves des inscriptions publiques`.
Lot Animation : README et recette navigateur `public-tombola.mjs`, sélecteurs
de présélection/dialogue et négociation actualisés sans retirer les contrôles.
Message : `test(e74): actualiser la recette du portail Animation`.
Live/Pro : aucune source modifiée. Isoler les hunks E74 de roadmap/index des
ajouts E73 déjà présents. Aucun staging, commit, push ni déploiement dans ce lot.

| Composant / environnement | Action de livraison | Valeur attendue ou défaut | Source / contrôle |
| --- | --- | --- | --- |
| Backend, cible à renseigner | Sauvegarder puis appliquer la chaîne prévue avec le runner canonique ; vérifier v288 puis v289 et leur empreinte | Pas de nouveau SQL E74 pour les quatre coordonnées ; recette locale actuelle jusqu’à v314, sans consigne d’application aveugle à une cible inconnue | `scripts/database/apply_migrations.py`, contrôle migrations en attente/rejeu ; historique TEST distinct ci-dessous |
| Backend + Live + Animation | Livrer des versions compatibles et actualiser les PWA | Corps nom/prénom/e-mail/téléphone ; ancien corps e-mail seul refusé 422 ; anciens liens maintenus | Contrats et parcours inscription → un mail → carnet → récupération |
| URL et signature | Vérifier `LOCALEO_FRONT_LIVE_URL`, fallback SPA, `LOCALEO_QR_COFFRET_KEY_ID` et `LOCALEO_QR_COFFRET_KEYRING` existants | URL par défaut `https://localeo.app/live`, à adapter à la cible ; matériel de signature requis hors dev, valeurs privées | `app/config.py`, ouverture du lien public et de l’accès personnel |
| Transport / scheduler | Vérifier `EMAIL_DEV_MODE`, fournisseur existant et `emails.envoyer` | Mode dev par défaut en dev ; `BREVO_EMAIL_API_KEY` ou `BREVO_API_KEY` provisionné dans le gestionnaire de secrets existant si envoi réel ; job toutes les 2 minutes, limite 100, scope `internal:batch` | Outbox et corrélation ; 202 ne prouve pas la livraison |
| Conservation | Vérifier `animations.conserver` et `LOCALEO_ANIMATION_CONSERVATION_APPLY` | 03:30 UTC, limite 100 ; application désactivée par défaut (`false`), sous-traitement `maintenance_email` limité à 500 | Rapport dry-run puis application selon procédure d’exploitation |
| Catalogue | Activer explicitement après résolution des réserves et revue de mise en service | v288 initialise `actif=false` ; aucune conversion automatique ni activation pendant cette revue | Administration du catalogue ; santé et création/lecture/fin d’une tombola |
| Documentation / ERP | Générer puis sélectionner le bundle de la révision documentaire retenue | Révision du futur commit à renseigner ; générateur actuellement épinglé sur `598ae97bcdcb992f40f0780db30b8e50f1873e56`, sans preuve de publication actuelle | `documentation.exports.json`, empreintes et lecteur cible ; aucun bundle versionné ajouté |

Ordre : sauvegarde/migrations compatibles, backend puis consommateurs coordonnés,
santé/readiness et recette synthétique, puis activation explicite. Vérifier les
anciennes participations et les refus après fermeture. En reprise, arrêter les
nouvelles créations par le catalogue et les inscriptions par les transitions
autorisées ; garder les lecteurs et remises E74. Ne pas promettre un retour à un
ancien schéma ou une suppression des données ; privilégier un correctif en avant.

### Capacité renouvelée le 13 novembre

**5 tests réussis**, `localeo-backend/tmp/e74-cloture-capacite.xml` et `.log` :
quatre cas N/10N × ancien parcours/inscription directe, puis gel. Exécution seule,
après arrêt des recettes navigateur et des autres suites, sur Windows 11,
Python 3.14.3, PostgreSQL 18, 8 processeurs logiques. Cinquante clients,
20 commandes/s ; 100 commandes historiques en environ 5 s ou 50 inscriptions
directes en 2,52–2,68 s. L’inscription directe inclut rendu et insertion du mail
réels en outbox, avec vérification des 50 participations, preuves et mails uniques.

| Population | Parcours | Page p95 | Commande p95 / p99 | Seconde commande p95 / p99 |
| --- | --- | --- | --- | --- |
| 1 000 | Demande historique puis confirmation | 38,74 ms | 209,49 / 285,51 ms | 113,29 / 146,28 ms |
| 10 000 | Demande historique puis confirmation | 27,93 ms | 174,78 / 293,38 ms | 82,53 / 163,50 ms |
| 1 000 | Inscription directe quatre champs | 20,47 ms | 182,10 / 209,64 ms | Sans étape intermédiaire |
| 10 000 | Inscription directe quatre champs | 30,01 ms | 386,94 / 451,71 ms | Sans étape intermédiaire |

Les seuils existants sont conservés : page/commande p95 <500 ms et commande
p99 <1 s. Total exact séparé à 10 000 : 23,58–32,35 ms. Plan `Index Only Scan`,
26 lignes, deux requêtes par page. Gel de 10 000 preuves : **6,96 s**, 141 SQL,
lots de 500, aucun objet ORM de provenance accumulé ; seuil <10 s respecté.

Ces mesures ne couvrent pas RSS, endurance, contention détaillée, détail public
sous charge ni mélange simultané lecture/inscription/gel/tirage/outbox. Le schéma
ciblé des commandes applique v288/v289, pas tous les triggers de la chaîne complète.
Le gel conserve des tableaux Python de provenance O(N). Produire le profil mémoire
et la charge mixte prévus avant d’attester CA15 ; les résultats actuels ne prouvent
ni une rafale instantanée ni la capacité de l’hébergement cible.

### Contrôles documentaires et fin de recette

`check_guidance.py` : **97 guides, 1 239 liens, aucune erreur ni avertissement**.
`check_guidance.py --changed --all-markdown` : **15 guides, 563 liens**, sans
erreur ni avertissement. `sync_documentation.py --check-sources` : **150 documents
vérifiés**. `git diff --check` réussi dans projet, backend et Animation.
Les trois revues indépendantes couvrent domaine, parcours et contrats ; la
relecture finale contrats/exploitation ne relève pas d’erreur factuelle dans
le bilan. Aucune ancienne preuve Pro ou opération TEST n’est présentée comme
réexécutée. PostgreSQL jetable et serveurs de recette arrêtés, port Live libéré.
La reprise porte sur les écarts ci-dessus, pas sur une nouvelle décision de périmètre.

## Correctif du 11 novembre 2026 — formulaire homogène

Demande explicite : tous les formulaires actuels d’inscription utilisent **nom,
prénom, e-mail et téléphone obligatoires**, à l’image de la tombola commerçante.
Cette demande remplace la collecte publique limitée à l’e-mail ; les résultats
historiques ci-dessous décrivent le contrat antérieur. Bases : Marketplace
`3a38530`, Backend `d90a0af`, Projet `1c69016`, plus modifications locales.
Les travaux de diagnostic du carnet, présents avant cette demande, restent séparés.

La reproduction navigateur avant correction échoue sur l’absence du champ Nom
en tombola publique à 390 px : rapport
`localeo-marketplace/test-results/visual-runs/2026-11-11T20-04-26-075Z-x989Sg`.
La reproduction API refuse également les quatre champs (422).

Backend : **103 tests ciblés réussis**, rapport
`localeo-backend/tmp/registration-homogeneous-final.xml` ; validation pure,
API quatre champs, refus des blancs, persistance à la création et conversion
d’une attente, rejeu identique, refus d’un corps modifié et identité déjà confirmée
préservée. **697 contrôles d’architecture et recensements réussis**, rapport
`tmp/registration-homogeneous-architecture.xml`. Les fixtures PostgreSQL ont été
adaptées au nouveau corps mais ne sont pas exécutées : aucune base jetable
n’était allouée à cette recette. Ces tests isolés ne prouvent pas la concurrence SQL.

Contrats : exports E41 (**1105 chemins**) et E42 (**81 chemins**) régénérés ;
copie Animation identique au canonique, contrat Pro régénéré hors ligne.
**31 tests contrats Pro et 4 tests HTTP Animation réussissent**. Les contrats
moteur de progression restent inchangés. Tous les processus de recette sont arrêtés.

Preuves frontend : **16 parcours des quatre moteurs réussis**, à 320/390/1280 px
et texte à 200 %, dans `tests/visual/animation-registration-identity.spec.cjs` ;
rapports `2026-11-11T20-05-19-662Z-QOpdp0` et `2026-11-11T20-07-25-087Z-ytuFhL`.
**20 régressions E74 réussies** dans `e74-tombola-email.spec.cjs`, dont double clic,
reprise identique après perte de réponse, stockage refusé, renvoi volontaire,
refus et ancien lien. **12 tests Node réussis** : contrat HTTP quatre champs,
preuves et non-divulgation/absence de collecte Analytics réactivée.
Les builds sont isolés, sans lecture de `.env`, sans API distante ni envoi réel.
Captures des formulaires public/commerçant à 390 px relues.

ESLint ciblé sur `src` et les tests modifiés réussit. Le lint global `npm run lint`
ne s’exécute pas jusqu’au bout : refus Windows `EPERM` en parcourant le répertoire
de sortie non modifié `output/bum-politique/pytest-approval-1`. Cette limite est
distincte d’un résultat vert ; aucune règle ESLint n’a été neutralisée.

Impacts : validation d’identité de domaine partagée, commandes classique et
publique, formulaires partagés, contrats OpenAPI, entrées explicites de démonstration.
Les colonnes existent : aucune nouvelle migration ni réparation de données.
Coordonnées déclarées pour la gestion de la participation, mêmes catégories de
conservation, anonymisation et accès ; aucune prospection ou autorisation Push
ajoutée. La notice de formulaire annonce les quatre champs et leur finalité.
Aucune recette mobile physique, mesure de charge, migration ou livraison sur TEST
n’est réalisée par ces preuves locales. Les anciens clients e-mail seul doivent
être actualisés avec le backend. L’epic conserve son statut en cours.

La revue indépendante valide les quatre champs pour les formulaires actuels et
leurs deux commandes de création. Elle relève une exception historique maintenue :
`demander-verification` puis `confirmer-email` conserve son ancien contrat
prénom/e-mail. Le formulaire actuel ne l’appelle pas. Ce correctif ne prétend donc
pas imposer les quatre champs à toutes les anciennes entrées API ; il préserve
les liens et clients historiques explicitement maintenus par E74. Un retrait de
ces anciennes commandes doit être traité avec leurs consommateurs et non déduit
d’une modification des champs affichés.

## Évolution E74-EVOL-INSCRIPTION-DIRECTE — 3 novembre 2026

Attendu : depuis QR ou Live, e-mail et règlement puis inscription qualifiée immédiatement, un seul mail transactionnel de confirmation, accès personnel/carnet via ce mail. Observé avant correction : prénom obligatoire et mail intermédiaire de vérification. La reproduction navigateur à 320 px échoue bien sur la présence du prénom avant correction. Les preuves de cette évolution sont distinguées ci-dessous des résultats historiques. Bases Git : projet `11b0016`, backend `3473635`, Live `9e4f1a1`, Animation `9fc4e8b`, plus les changements locaux. La reproduction API du nouveau parcours échouait en 404 avant correction puis répond en 202.

Périmètre : domaine/application/API/SQL/e-mail et lecteurs backend, Live, portail Animation, contrats générés et documentation canonique. La migration additive v289 distingue adresse déclarée et vérifiée, sans qualifier d’anciennes attentes. Aucun changement des règles de gain, quota, droits ou validation Pro/PIN des autres modèles. Pas de nouveau fournisseur, secret ou DNS ; le générateur doit passer par les commandes métier.

### Preuves de l’inscription directe

| Contrôle | Résultat | Portée |
| --- | --- | --- |
| Backend domaine/application/API | **65 succès** | Inscription sans prénom, preuve discriminée, réponse publique sans accès, refus, contrat et ancien parcours maintenu. Runner isolé `scripts/validation/test_isolated.py`. |
| Architecture et couverture use cases | **637 succès** | `tests/architecture`, `tests/domain/test_domain_dedicated_classes.py`, `tests/application/use_cases/test_use_case_business_test_coverage.py`. |
| Intégration PostgreSQL | **66 succès distincts** | Inscription directe/ancienne, concurrence et dernière place, rejeu, rollback e-mail, conversion d’attente, compteurs, gel, tirage, trois modes de gains et remise, Vision 360 sans prénom, export et anonymisation. Restauration rejouée avec attente, preuve vérifiée, inscription directe et outbox ; aucun transport e-mail réel. |
| Migration et restauration | **1 test réussi sur base locale jetable** | Chaîne complète jusqu’à v289 et pg_dump/pg_restore ; aucune application sur TEST partagé. |
| Générateur complet | **1 succès PostgreSQL** | Création, modification, publication, quota et participations directes/historiques par commandes ordinaires, outbox neutralisée. |
| Live navigateur | **20 scénarios E74 distincts et 6 régressions réussis** | 320/390/1280 px, QR/fiche/formulaire, absence de demande de vérification intermédiaire, réponse perdue, double clic, refus 409/410/429, anciens liens, accès personnel → carnet → jeu `NON_REQUISE`. API simulées ; backend vérifié séparément. |
| Localeo Animation | **3 scénarios navigateur réussis**, **11 tests Node réussis**, types/lint/build réussis | 320/390/1280 px, création, flyer et participants ; avertissement de taille du bundle conservé. |
| Live contrats/API | **7 tests Node réussis**, lint ciblé réussi | Lint global empêché par `EPERM` dans un ancien répertoire `output`, sans lien avec les sources modifiées ; ce contrôle global n’est pas annoncé réussi. |
| Exports | **Conformes** | OpenAPI E41/E42 régénérés, copie Animation identique à E41 ; 98 fichiers de contrats moteur identiques dans chacun des deux consommateurs. `sync_documentation.py --check-sources` : 134 documents vérifiés. |
| Documentation | **Réussie** | `check_guidance.py` global et vérifications des guides touchés ; `git diff --check` sans erreur. |

Les tests PostgreSQL ciblés sont dans `tests/security/test_tombola_publique_postgres.py`, `test_tombola_publique_gains.py`, `test_tombola_publique_parcours_postgres.py`, `test_tombola_publique_migration_complete.py` et `test_demo_tombola_publique_locale_postgres.py`, exécutés via le runner isolé avec une instance temporaire sur le port 55439.

Les totaux de suites peuvent se recouvrir : ne pas les additionner en tests uniques. Le premier test de restauration a rencontré `WinError 50` dans le lancement Windows de `pg_dump` ; la fixture utilise désormais une entrée standard isolée, puis le test a été rejoué avec succès. La vérification n’a pas été supprimée.

Revue indépendante des invariants et consommateurs sans écart bloquant restant. Les captures du formulaire et du succès ont été relues ; les cibles tactiles secondaires utilisent les styles existants, avec un dernier rejeu de trois scénarios réussi à 320/390 px et sur le renvoi. La revue a également corrigé le lecteur Vision 360 qui supposait un prénom toujours présent. L’annulation des anciens mails intermédiaires en attente réutilise le garde d’outbox, y compris après réservation abandonnée.

**Livraison :** v289 a ensuite été appliquée à TEST le 3 novembre 2026, après sauvegarde et contrôles ; voir le compte rendu d’exploitation. Les commits backend `05ff776`, Live `6817447` et Animation `4f4b5e6` portent le nouveau parcours. Les tests locaux ci-dessus précèdent cette opération ; les contrôles de santé après migration ne prouvent pas l’achèvement du déploiement de ces commits. Aucun envoi réel n’a été effectué. Les anciens règlements publiés sont conservés et peuvent encore mentionner l’ancienne étape ; les anciennes PWA E74 peuvent afficher un libellé d’adresse vérifiée devenu inexact. Voir la [procédure](exploitation.md). Aucune capacité de production ni nouvelle mesure de charge n’est déduite de ces tests.

## Bilan historique d’implémentation avec vérification intermédiaire

Les tests ci-dessous ont été exécutés sur les changements locaux, sans activation du TEST partagé et sans envoi d'e-mail réel. Bases Git : projet `e6bddec`, backend `3437cfc`, Animation `e275bd5`, marketplace/Live `4dbc897`, Pro `054feab`. L'epic reste **En cours** : les scénarios complémentaires indiqués ci-dessous ne sont pas réputés validés par un build ou par une recette navigateur à API simulée.

Les preuves PostgreSQL utilisent une instance locale jetable, port 55474, une base de recette et des schémas uniques par fixture. Les e-mails sont capturés dans l'outbox. Le backend est toujours exécuté par `scripts/validation/test_isolated.py`.

## Matrice historique des 16 critères

U = unitaire ; I = intégration application/API/PostgreSQL ; F = navigateur. Les parcours F actuels simulent les réponses API ; ils ne constituent pas à eux seuls le scénario intégral avec backend et transport e-mail réels.

| Critère | Preuves exécutées | Compléments de recette à distinguer |
| --- | --- | --- |
| E74-CA-01 | U registre à quatre moteurs, modèle public et capacité standard ; F sélection du modèle dans Animation. | Catalogue activé uniquement dans les fixtures ; aucune activation distante. |
| E74-CA-02 | I publication PostgreSQL sans commerce, rejeu d'une publication, un seul appel quota ; suites existantes des droits/quota. | La recette du générateur complète ce test par un vrai abonnement, les droits acquis et le contrôle d’un débit unique après rejeu. |
| E74-CA-03 | U compilation/règles sans commerce ; I publication normale, snapshot marchand vide, refus sans lots et sans débit. | Recette PostgreSQL sur migrations complètes : création, modification, publication, flyer et quota réel réussis pour une commune sans commerce (lots externes). |
| E74-CA-04 | U assistant et sections non applicables ; I pages/compteurs hors commune refusés ; F assistant et navigation. | Pas de preuve nouvelle de toutes les combinaisons de rôles E73. |
| E74-CA-05 | F accès direct au formulaire, aucun secret personnel dans le lien public ; ouverture du lien de confirmation sans POST. | Scan d'un QR imprimé avec caméra physique non exécuté ; pas requis pour prouver le traitement de l'URL. |
| E74-CA-06 | U flyer public contextualisé et quantités ; F flyer sans étapes commerçantes. | Rendu PDF final des trois modes non rejoué dans cette campagne. |
| E74-CA-07 | U preuve/identité minimale ; I attente puis confirmation, outbox atomique, ancien endpoint refusé ; F confirmation explicite et entrée dans Live. | Chaîne de services réels e-mail → gel → tirage externe → accès → remise réussie ; le navigateur est vérifié séparément. |
| E74-CA-08 | I demandes/confirmations concurrentes, rejeu, secret étranger, clé réutilisée, accès révoqué, renvoi/remplacement, récupération ; F reprise. | Les succès rejoués ne prolongent ni preuve ni accès. |
| E74-CA-09 | U fenêtre/date/règlement ; I expiration, fermeture, confirmation bloquée par clôture, gel revalidant les preuves. | Trois courses supplémentaires passent : expiration à 31 min, fermeture à 61 min, demande retardée de 2 h ; aucun accès ni preuve tardifs. |
| E74-CA-10 | F participation et suivi de commune séparés ; inscription ne crée aucun consentement de communication. | Aucun canal de communication inter-animations ajouté. |
| E74-CA-11 | F suivi facultatif, réutilisation de Mes communes et stockage local ; régressions Live. | Pas de nouveau compte habitant ni de synchronisation inventée entre appareils. |
| E74-CA-12 | I pages bornées, portée du curseur, totaux/compteurs, attentes non comptées publiquement, export minimal ; gel de 10 000 preuves réelles. | Mémoire globale du processus non profilée ; provenance minimale du gel encore O(N). |
| E74-CA-13 | I trois modes après gel avec identité minimale, zéro/insuffisance/exact/suppléants ; U stratégies existantes réutilisées. | 22 tests PostgreSQL couvrent les trois modes, populations 0/1/2/5, insuffisance Coffrets, suppléants et rejeu. |
| E74-CA-14 | I notification, accès et projection Live du bon numérique ; confirmation externe distincte de la remise ; régressions Pro. | Remise externe, consommation du bon et reprises testées ; financement/activation Coffrets simulés à la frontière de distribution, tirage et stockage réels. |
| E74-CA-15 | I secret/rejeu/révocation, limitation durable et 429, isolation des pages ; F mobile/clavier ; capacité N/10N au débit nominal. | Rafale simultanée de 50 : p95 ~2 s, dépasse le budget nominal ; voir mesures et limites. |
| E74-CA-16 | I migration complète/rejeu/restauration, états attente/preuve/outbox rejouables ; U/I négociation anciens lecteurs ; F régressions trois moteurs. | Générateur : entrée locale explicite complète vérifiée, séparée du build historique ; dotation externe.  Huit échecs de régression reproduits sur la base inchangée. |

Revue indépendante : le défaut d’horloge capturée avant verrou a été corrigé et sa correction relue ; le coût mémoire de la provenance du gel reste explicitement O(N). Les objets ORM de provenance sont désormais évités lors de l’insertion par lots.

## Résultats et commandes reproductibles

Les logs mentionnés sont des sorties locales ignorées par Git dans `localeo-backend/tmp/`. Ils ne contiennent aucun accès de production. Les tests constituent la preuve versionnable ; les chiffres sont ceux de cette exécution, sans extrapolation à Render.

| Contrôle | Résultat | Preuve locale |
| --- | --- | --- |
| Intégration E74 : e-mail, publication, gains, transport, démonstration | **113 réussites** | `e74-integration-final.log` ; fichiers `tests/security/test_tombola_publique_*.py`, `tests/api/test_tombola_publique_email.py`, suites démonstration ciblées |
| Contrat HTTP de pagination sur PostgreSQL | **1 réussite** | `e74-http-pages.log` : borne 100, curseur invalide, `next_cursor: null`, aucun total implicite, autre commune refusée |
| Adaptateurs conservation/capacités et compteurs historiques après correction du filtre vide | **28 réussites** | `e74-adaptateurs-corriges.log` ; `test_conservation_moteur_api_t6.py`, `test_capacites_lecture_live_e74.py`, `test_compteurs_lectures_v283.py` |
| Chaîne SQL complète jusqu'à v288, rejeu et restauration pg_dump/pg_restore | **1 réussite** | `e74-migration-finale.log`, `test_tombola_publique_migration_complete.py` ; modèle installé inactif |
| Régression large backend | **1 560 réussites, 8 échecs, 7 ignorés** | `e74-regression-finale.log` ; les ignorés ne sont pas des réussites |
| Reproduction des huit échecs sur backend inchangé `3437cfc` | **8 mêmes échecs, 28 réussites** | `e74-baseline-failures.log`, worktree détaché local |
| Courses d’horloge, exports et e-mail E74 | **26 réussites** | `e74-course-horloge.log` ; tests des verrous, instantané export et compteurs sans hydratation |
| Refus abonnement et paramètres publics | **5 réussites**, vrai contrat de droit | `e74-refus-droits.log` ; absence d’abonnement ne provoque plus de 500, fermeture publique sans commerce |
| Démonstration locale complète | **11 tests unitaires et 1 test PostgreSQL réussis** | `test_demo_tombola_publique_locale_postgres.py`, migrations complètes, PDF local, droits et quota réels |
| Conservation et borne e-mail finale | **28 réussites** | `e74-purge-borne-finale.log` : maintenance limitée à 500 même lorsque le batch principal reçoit 1 000 |
| Validation finale groupée gains/e-mail/droits | **53 réussites** | `e74-validation-finale.log`, après optimisation des insertions du gel |
| Contrôles finaux architecture/application | **642 réussites** | `e74-derniers-controles.log` ; inclut refus de validation commerçante d’une participation publique |
| Architecture + intégration e-mail/export | **656 réussites** | `e74-exports-architecture.log` |
| Gains, trois modes et tailles de population | **22 réussites** | `.artifacts/e74-gains-complement.log`, `test_tombola_publique_gains.py` |
| Parcours réel après publication jusqu’à remise | **1 réussite** | `.artifacts/e74-parcours-complet.log`, `test_tombola_publique_parcours_postgres.py` |
| Capacités lecteurs catalogue/Live/global/jeu | **74 réussites** | `.artifacts/e74-live-readers-tests.log` |
| Animation | **299 tests Node réussis**, typage/lint/build réussis ; navigateur 320/390/1280 px réussi | `localeo-animation/tmp/e74-tests-final.log`, `tests/browser/public-tombola.mjs` ; avertissement de taille de bundle conservé |
| Live | **154 tests sécurité réussis**, **12 tests navigateur E74** et **19 régressions navigateur** réussis ; lint ciblé/build réussis | `localeo-marketplace/tmp/e74-security-final.log`, `tests/visual/e74-tombola-email.spec.cjs` |
| ERP/Support | Scénario participants réussi aux largeurs 320/1280, clavier/zoom ; régression suivi produits réussie | `tests/browser/epic74-participants-erp.cjs` |
| Pro | **36 tests ciblés réussis** | Réutilisation du bon numérique, sans nouveau flux d'inscription commerçante |

Ces suites se recouvrent : ne pas additionner leurs totaux comme un nombre de tests uniques. Le lint global marketplace rencontre une erreur de permission dans des sorties locales préexistantes (`output`/`tmp`) ; le lint des sources modifiées passe.

Les huit échecs backend de base concernent un libellé accentué du catalogue et des fixtures historiques incomplètes (réversibilité, mise à jour versionnée, verrou de commande lots). Ils ont été reproduits sur le commit initial, sans modification ni skip pour les rendre verts.

### Capacité mesurée

`tests/performance/test_e74_capacite_locale.py` : **2 tests réussis**, N=1 000 puis 10 000, 50 clients, arrivées limitées au débit spécifié de 20 commandes/s. À 10 000 : page p95 11,94 ms, total 14,92 ms, demande p95 39,51 ms / p99 54,02 ms, confirmation p95 35,70 ms / p99 37,46 ms. Plan `Index Only Scan`, 26 lignes et deux requêtes par page. Log `e74-capacite-nominale.log`.

`tests/performance/test_e74_gel_local.py` : **1 réussite**, gel de 10 000 participants en **5,88 s**, 141 requêtes, lecture et insertion par lots de 500, aucun objet ORM de membre/provenance accumulé ; log `e74-gel-membres-bornes.log`. La même exécution compte **17 tests réussis** avec les régressions de clôture, publication et le parcours e-mail → remise.

La réduction mémoire a d’abord fait dépasser le budget du gel (10,06 à 16,96 s selon le mode d’insertion). Le profilage a conduit à des insertions SQL groupées avec compilation réutilisable pour les membres et la provenance ; le dernier résultat ci-dessus passe le budget de 10 s sans modifier son assertion.

Deux essais de rafale instantanée de 50 commandes ont dépassé le budget nominal (p95 ~2,0–2,3 s ; logs `e74-capacite.log`, `e74-capacite-v2.log`). Le scénario nominal ne représente pas cette rafale. La fixture de capacité exécute v288 sur le schéma ciblé ; les mesures ne prouvent ni les ressources de l'hébergement cible ni la charge cumulée de tous les triggers historiques. Mesure RSS, endurance et charge mixte avec tirage/outbox restent à produire.

Exemple de relance locale, depuis le backend, avec une base jetable déjà préparée :

```powershell
& 'C:/Users/casta/AppData/Local/Python/bin/python.exe' scripts/validation/test_isolated.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55474/localeo_audit_test tests/security/test_tombola_publique_postgres.py -q -s --tb=short
```

La migration complète utilise une seconde base vide réservée `localeo_audit_migrations_test` ; son test refuse une base contenant des données initiales.

## Plan de couverture de référence (spécification)

Dans le backend, suivre le runner isolé décrit par son `AGENTS.md`. La recette ne dépend d'aucun compte réel, base TEST partagée, fournisseur e-mail ou validation de pilote.

| Dépôt | Fichiers/scénarios ciblés |
| --- | --- |
| Backend — nouveaux | `tests/domain/animation_locale/test_tombola_publique.py` : compilation, identité, qualification et refus ; `tests/application/services/test_tombola_publique_email.py` : transactions/outbox/reçus ; `tests/api/test_tombola_publique_email.py` : contrats et anti-contournement ; `tests/security/test_tombola_publique_postgres.py` : contraintes, gel et concurrence. |
| Backend — existants | `tests/domain/animation_locale/test_tombola_locale.py`, `test_politique_participation_publication.py` ; `tests/application/services/test_participants_animation.py` ; `tests/api/test_localeo_live_animations_inscription.py` ; `tests/security/test_publication_classique_t4.py`, `test_exploitation_moteur_postgres.py`, `test_tirages_libres_postgres.py`, `test_tirages_numeriques_postgres.py`. |
| Animation | Tests existants `animation-engine-registry.test.mjs`, `assistant-presentation.test.mjs`, `assistant-navigation.test.mjs`, `publication-http-contracts.test.mjs`, `flyer-http-contracts.test.mjs` ; nouveau scénario navigateur `e74-tombola-publique` couvrant création → publication → QR → participants → tirage/remise. |
| Marketplace/Live | Tests registre, installation, jeu, communes ; scénarios existants `live-registration-clarity.spec.cjs`, `live-game.spec.cjs`, `live-lots-unified.spec.cjs`, `live-habitant-communes.spec.cjs`, `organizer-messages.spec.cjs` ; nouveau `e74-tombola-email.spec.cjs`. |
| Commerçant/Pro | Remise de bon numérique E74, refus d'une qualification par scan/PIN et non-régression des validations commerçantes des autres modèles. Pas de nouveau flux d'inscription Pro à tester. |
| Projet / contrats | Liens de documentation, exports depuis producteurs, empreintes schémas et contrats embarqués ; ces contrôles accompagnent les tests consommateurs et ne les remplacent pas. |

## Parcours fonctionnels courants à vérifier

1. **Sans commerce, bout en bout** : organisation de test sans commerce → standard → lots externes → assistant → publication → flyer/QR → e-mail/règlement → inscription immédiatement qualifiée (une chance) → un mail capturé localement → lien personnel et ajout au carnet, sans nouvelle qualification → clôture → tirage confirmé → lot visible dans Live → remise par organisateur. Vérifier toutes les identités et versions entre écrans et base.
2. **Reprise et autre appareil** : s’inscrire sur A, perdre la réponse puis rejouer la même commande ; un participant/une preuve/une chance/un mail. Ouvrir l’accès personnel sur B sans installation connue, puis l’ajouter au carnet sans nouvelle qualification. Reprendre ensuite sur A par e-mail. Aucun état local n'accorde l'éligibilité.
3. **Secret et prévisualisation** : la réponse publique d’inscription ne contient ni token ni identifiant personnel ; GET, robot de messagerie et préchargement n’écrivent rien ; pour les anciens liens, secret étranger, expiré, révoqué ou remplacé refusés ; nouvelle clé sur secret consommé sans nouvelle mutation. L'ancien endpoint et la récupération ne donnent pas d'accès en attente. Révocation bloque le reçu de succès.
4. **Clôture en course** : deux transactions réelles PostgreSQL, barrière synchronisée ; inclure une inscription commise avant gel ou refuser celle passée après ; rejouer aussi la confirmation historique. Aucun qualifié absent de la population par course ; aucun lien tardif ne l'étend. Rejouer après arrêt worker.
5. **Trois modes, population insuffisante** : lots externes et numériques avec zéro/un/plusieurs candidats ; Coffrets refuse si exemplaires supérieurs aux candidats, sans émission partielle ni modification de dotation. Nombre exact et cas suffisant vérifiés également.
6. **Mobile et préférences** : 320/390 px et PC, clavier/zoom, commandes accessibles, liens retour et rafraîchissement cohérents ; suivi commune refusé puis ajouté/retiré, notifications refusées, stockage indisponible, limite dix. Participation et lots restent utilisables dans chaque cas.
7. **Compatibilité** : anciennes tombolas/passeports/chasses avant et après migration, ancienne PWA face au catalogue/direct E74, cache et mise à jour ; aucun type inconnu envoyé à un lecteur qui ne le comprend pas sans réponse explicite de mise à jour.
8. **Volumétrie et exploitation** : N/10N selon budgets d'architecture, charge mixte lectures/inscriptions/confirmations historiques/gel, plusieurs habitants sur même IP ; total exact, plans/index, bornes mémoire, délais, saturation explicite. Restaurer une sauvegarde isolée contenant attentes, preuves, outbox et gains, puis reprendre sans doublon.

### Cas limites de récupération et de rejeu (CA08/09/15)

- Après fermeture, appeler les deux routes de récupération pour une adresse absente, en attente et confirmée : même 202 public ; aucune création, preuve ni nouvelle chance ; seul le confirmé encore autorisé reçoit un accès par l'outbox. Tester également la limite `date_fin + 90 jours`, l'anonymisation et les délais de renvoi.
- Confirmer avant expiration, perdre la réponse, puis rejouer la même commande après les 30 minutes du challenge et après fermeture, avant les 24 heures du reçu : même succès autorisé, sans prolongation d'accès ni mutation de population. Une première confirmation avec un challenge expiré reste refusée.
- Rejouer avec secret incorrect, autre animation, autre corps ou clé, reçu expiré, accès révoqué ou participant anonymisé : aucun accès restitué. Vérifier que la recherche d'un reçu ne contourne pas les contrôles d'autorisation courants.

## Documentation et données à livrer avec le code

- Compléter les guides Animation/ERP avec le parcours sans commerce et l'avertissement Coffrets ; le guide Live avec inscription directe, accès personnel par mail, récupération et suivi local ; le support stand avec QR/lien et saisie de l’adresse.
- Actualiser les sources de règlement/notice selon les finalités et durées réellement appliquées, sans affirmer une validation juridique obtenue. Leur revue de mise en service reste distincte des tests de clôture.
- Régénérer les contrats depuis le backend, puis mettre à jour les manifestes/schémas embarqués et vérifier empreintes et tests de chaque lecteur.
- Adapter le générateur backend et ses assertions aux états de preuve ; aucun accès réel ou donnée privée dans les fixtures. Vérifier suppression/anonymisation/restauration, pas seulement création des tables.
- Documenter activation, fermeture d'urgence, limitation de débit, échecs d'e-mail, reprise outbox, purge et retour vers l'avant. Décrire les variables effectivement introduites lors du développement avec exemples sans secret ; aucune variable hypothétique à configurer aujourd'hui.

## Bilan de préparation

Les choix produit sont fixés et les responsabilités, contrats cibles, limites existantes et preuves sont identifiés. Les travaux peuvent être implémentés par lots : domaine/données et contrats → consommateurs et UX → intégration/recette/capacité → activation. L’inscription directe réutilise la pagination et le gel existants ; ses preuves doivent vérifier les deux provenances de qualification.

La clôture technique nécessite les preuves pertinentes réussies pour les 16 critères. Une vérification locale ne vaut pas déploiement ; une action pilote ou une preuve externe n'est pas une condition ajoutée à la clôture. Les preuves locales acquises figurent en tête de ce document. Aucune activation distante n'a été effectuée ; les compléments de tests restent visibles dans la matrice.

## Historique — contrôles de spécification avant implémentation

- Exploration en lecture des producteurs backend et des consommateurs Animation/Live, puis revue indépendante `localeo-contract-reviewer` des trois documents. Les trois écarts relevés (négociation des clients historiques, contrat de pagination, affichage des dates) ont été corrigés et leur résolution confirmée en seconde lecture. Aucun reste concret dans ces points ; cela ne vaut pas test d'implémentation.
- Dépôt documentaire, base `7b3d5e5` et modifications locales E74 : `python scripts/check_guidance.py` avec `--document` pour les trois fichiers de ce dossier, le backlog E74, la roadmap et l'index. Résultat : **99 guides, 1 158 liens locaux, zéro erreur, zéro avertissement**.
- Aucun contrat généré ni entrée de `documentation.exports.json` modifié dans cette phase ; pas de lecteur applicatif à exécuter pour un changement d'export. Les tests domaine/intégration/navigateur, migrations, charge et génération de démonstration restent **non exécutés**.

### Reprise de spécification du 3 novembre 2026

- Base documentaire `e6bddec`, backend `3437cfc` ; les choix produit et les 16 critères restent inchangés. Précisions apportées sur la récupération après fermeture et la reprise d'un succès au-delà du délai initial du challenge, avec leurs scénarios de refus.
- Nouvelle revue en lecture seule par `localeo-contract-reviewer` des contrats, producteurs et consommateurs ; relecture des précisions : aucun écart bloquant restant identifié dans ce périmètre. La récupération historique jusqu'à `date_fin + 90 jours` a été vérifiée dans le service et l'entité participant.
- Contrôles locaux : `check_guidance.py` sur les six documents E74/index/roadmap, **99 guides, 1 158 liens, zéro erreur et avertissement** ; `sync_documentation.py --check-sources`, **134 documents vérifiés** ; `git diff --check` réussi. Python utilisé par chemin explicite, l'alias système étant indisponible.
- Seul le dépôt documentaire est modifié. Aucun code, contrat généré, migration, test métier, envoi ou déploiement réalisé. Le périmètre est prêt à implémenter ; l'état produit reste **À faire**.


## Contrôles documentaires et contrats après implémentation

- `check_guidance.py` incluant les six documents E74 : **100 guides, 1 107 liens, zéro erreur et avertissement**.
- `sync_documentation.py --check-sources` : **134 sources vérifiées**.
- Export moteur avec `--check` : **98 fichiers conformes** dans Animation et dans Live ; les OpenAPI E41/E42 proviennent du producteur local, et le contrat embarqué Animation correspond à E41.
- `git diff --check` : réussi dans les cinq dépôts. Pro reste inchangé.
- Aucun commit, push, activation de modèle, migration distante ni envoi réel effectué. Les quatre dépôts modifiés restent indépendants.


## Correctif du 3 novembre 2026 — lecture publique refusée à Live

Signalement : fiche Live sur TEST, animation `87246fa7-237f-42f9-983e-92d6daf4f9ed`,
réponse `CLIENT_ANIMATION_INCOMPATIBLE`, corrélation
`LOC-93d2915e-19f2-45a7-9e71-7e062b17d52d`, moteur requis
`TOMBOLA_PUBLIQUE:1.0`. Rattachement : accès public E74-CA-05 et compatibilité des
clients. Les logs distants n’ont pas été consultés.

Cause reproduite sur backend `2e896ae` : la route de détail accepte le paramètre
`moteurs_supportes` mais ne le transmet pas au catalogue. Le client compatible est
alors traité comme historique et reçoit le même HTTP 409 que dans le signalement.
Le correctif transmet le paramètre jusqu’au contrôle existant. Les anciens clients
incompatibles restent refusés ; une déclaration malformée reçoit 422 avant toute
lecture, une fiche absente reste 404 sans révéler son moteur.

Défaut adjacent reproduit dans Live, base `901c660` : la lecture d’une page de lots
supplémentaires omet aussi `moteurs_supportes`. La couche HTTP déclare désormais les
mêmes capacités pour le détail et ses pages de lots, en conservant curseur et limite.
La revue ciblée des autres consommateurs n’identifie pas d’oubli correspondant dans
Localeo Animation ou l’ERP.

Preuves locales :

- Avant correction, `tests/api/test_tombola_publique_lecture.py` : 2 échecs attendus
  (compatible refusé en 409, déclaration invalide non contrôlée), 5 succès.
  Le catalogue et le gestionnaire HTTP réels sont utilisés avec stockage et
  projection simulés, sans connexion à une base distante.
- Après correction, lanceur `scripts/validation/test_isolated.py` sur ce test,
  `tests/api/test_capacites_lecture_live_e74.py`, `tests/api/test_tombola_publique_email.py`,
  `tests/application/services/test_capacites_lecture_tombola_publique.py` et
  `tests/application/services/test_catalogue_animations_publiques.py` : **43 succès**.
- Contrôles d’architecture, classes de domaine et couverture des use cases via
  le même lanceur isolé : **637 succès**.
- Live : régression de négociation des pages de lots d’abord en échec ; après
  correction, `node --test` sur `catalogue-pagination.test.cjs`,
  `animation-engine-registry.test.cjs` et `live-dashboard-api.test.cjs` : **11 succès**.
  ESLint sur les deux fichiers modifiés : réussi.
- Parcours navigateur `e74-tombola-email.spec.cjs` via le serveur isolé Playwright
  (build sans `.env`, API simulées), formats 320/390/1280 px, confirmation,
  récupération et refus : **12 succès**, sortie 0.
- Revue indépendante du correctif : aucun écart bloquant identifié ; les tests
  API ci-dessus ne constituent pas une validation de stockage PostgreSQL réel.

Impacts : backend, consommateur Live et ce suivi documentaire. Le contrat HTTP
existant est respecté, sans nouveau schéma ni export à régénérer. Aucune règle de
qualification, droit, donnée, migration, configuration ou génération de démonstration
ne change ; aucune réparation de participation n’est nécessaire pour ce défaut.
La livraison nécessite le backend corrigé et le bundle Live pour la pagination des
lots. Aucun commit, push, déploiement ou rejeu sur TEST effectué à ce stade.
