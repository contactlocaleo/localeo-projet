# Conception technique - Epic 59 Tests de performance des API

## 1. Architecture cible

Le banc de performance est externe au processus FastAPI. Les scripts k6 sont
versionnes dans le projet et executes directement par le binaire k6 installe
sur le poste Windows de l'administrateur, sans Docker.
Grafana Cloud k6 Free recoit les metriques et fournit leur consultation, sans
generer lui-meme la charge et sans ajouter de dependance au runtime Python.

```text
Poste administrateur
    |
    +-----> k6 natif -----> Backend cible -----> PostgreSQL
                |                 |
                |                 +-----> fournisseurs simules sur cible ephemere
                v
          Grafana Cloud k6
          resultats et seuils
```

Le processus k6 local produit la charge et transmet les resultats a Grafana
Cloud.
Les metriques Render, applicatives et PostgreSQL restent consultees dans leurs
outils d'exploitation puis sont correlees par la fenetre temporelle et le
`runId`.

```text
performance/k6/
  VERSION
  config/
    environments.js
    production-readonly.js
  journeys/
    marketplace.js
    localeo-live.js
    commercant.js
    animation.js
    backoffice.js
    achat-coffret.js
    exploitation.js
    traitements-asynchrones.js
  profiles/
    smoke.js
    nominal.js
    peak.js
    stress.js
    spike.js
    soak.js
  lib/
    auth.js
    checks.js
    data.js
    guardrails.js
    tags.js
    thresholds.js
  main.js

scripts/performance/
  build-dataset.ps1
  build_dataset.py
  dataset_small.py
  load-secrets.ps1
  run-campaign.ps1
  run-k6.ps1
  run_campaign.py
  common.py

tests/performance/
  test_dataset_small.py
  test_k6_core_contract.py
  test_campaign_safety.py
```

La logique d'un parcours ne contient pas sa charge. Un profil selectionne les
parcours, leur debit, leur concurrence, leur duree et leurs seuils.

Le binaire est installe avec le paquet Windows officiel, par exemple
`winget install k6 --source winget`, ou avec l'installeur officiel. La version
validee est inscrite dans `performance/k6/VERSION` et controlee par le preflight.
Une mise a niveau de k6 est une modification explicite du banc, jamais une
consequence automatique d'un lancement.

## 2. Integration Grafana Cloud et configuration

### 2.1 Projet Cloud

Un projet Grafana Cloud k6 dedie `localeo-api-performance` regroupe les tests.
Le script fournit dans `options.cloud` le `projectID`, un nom stable compose du
parcours et du profil, et les tags `run_id`, `commit`, `target`, `journey`,
`profile` et `dataset`.

Le binaire local utilise l'authentification configuree par `k6 cloud login` ou
les variables `K6_CLOUD_TOKEN` et `K6_CLOUD_STACK_ID`, puis execute `k6 cloud
run --local-execution`. Le token Cloud n'est jamais transmis au backend cible
et n'est pas accessible au code metier des parcours.

Avant chaque campagne, l'administrateur verifie dans Grafana Cloud les limites
du compte Free et la duree de retention effective. Aucun depassement payant ne
doit etre possible sans un nouvel arbitrage.

### 2.2 Variables du banc

Variables retenues :

| Variable | Role |
| --- | --- |
| `LOCALEO_PERF_BASE_URL` | URL absolue du backend cible |
| `LOCALEO_PERF_ALLOWED_HOSTS` | Hôtes explicitement autorises pour le tir |
| `LOCALEO_PERF_TESTS_ALLOWED` | Confirmation explicite d'autorisation |
| `LOCALEO_PERF_TARGET_KIND` | `ephemeral` ou `production` |
| `LOCALEO_PERF_PRODUCTION_ALLOWED` | Seconde confirmation exigee pour la production |
| `LOCALEO_PERF_DATABASE_MUTATION_ALLOWED` | Confirmation destructive exigee avant import ou restauration |
| `LOCALEO_PERF_DATABASE_URL` | Connexion PostgreSQL de la cible ephemere, injectee comme secret |
| `LOCALEO_PERF_BACKUP_DIR` | Repertoire local hors Git pour le backup temporaire |
| `LOCALEO_PERF_K6_PROJECT_ID` | Identifiant du projet Grafana Cloud k6 |
| `LOCALEO_PERF_K6_TEST_NAME` | Nom stable du test dans le projet Cloud |
| `LOCALEO_PERF_BACKGROUND_JOBS_DISABLED` | Confirmation que scheduler et batchs sont neutralises sur la cible ephemere |
| `LOCALEO_PERF_USER_ACCESS_BLOCKED` | Confirmation que les utilisateurs ordinaires ne peuvent pas acceder a la cible ephemere |
| `LOCALEO_PERFORMANCE_TEST_MODE` | Active les reglages backend de performance uniquement avec `LOCALEO_ENV=performance` |
| `LOCALEO_PERFORMANCE_PUBLIC_RATE_LIMIT_MAXIMUM` | Plafond public dedie au backend de performance ; sans effet sur les autres environnements |
| `LOCALEO_PERF_EXPECTED_K6_VERSION` | Version native de k6 exigee par le preflight |
| `LOCALEO_PERF_PROFILE` | `smoke`, `nominal`, `peak`, `stress`, `spike` ou `soak` |
| `LOCALEO_PERF_DATASET` | `small`, `reference` ou `capacity` |
| `LOCALEO_PERF_RUN_ID` | Identifiant unique de campagne |
| `LOCALEO_PERF_MAX_VUS` | Plafond dur d'utilisateurs virtuels |
| `LOCALEO_PERF_MAX_RPS` | Plafond dur de debit |
| `LOCALEO_PERF_MAX_DURATION` | Duree maximale autorisee |
| `LOCALEO_PERF_COMMIT` | SHA du commit backend teste |

Les valeurs fonctionnelles sont passees aux scripts k6 par le wrapper
PowerShell. `K6_CLOUD_TOKEN` et `K6_CLOUD_STACK_ID` servent uniquement a
l'authentification du binaire local a Grafana Cloud.

### 2.3 Preflight obligatoire

Le lanceur doit echouer avant le premier appel si :

- le binaire `k6` est absent ou sa version differe de la version attendue ;
- `pg_dump`, `pg_restore` ou `psql` sont absents ou incompatibles avec la
  version PostgreSQL cible ;
- `LOCALEO_PERF_TESTS_ALLOWED` n'est pas vrai ;
- l'hote cible n'appartient pas a l'allowlist ;
- la production est ciblee sans mode `production`, seconde confirmation et
  autorisation administrateur ;
- un parcours mutable ou un profil `stress`, `spike` ou `soak` cible la
  production ;
- un plafond est absent, invalide ou depasse ;
- une operation de base est demandee sans
  `LOCALEO_PERF_DATABASE_MUTATION_ALLOWED=true` ;
- l'espace disque disponible ne permet pas de creer et verifier le backup ;
- les secrets necessaires au parcours demande sont absents.

Les secrets sont injectes au lancement depuis le gestionnaire de secrets. Ils
ne sont ni versionnes, ni imprimes dans les rapports.

La production accepte uniquement les operations de lecture ou les `POST` sans
effet de bord explicitement inventories, avec une charge bornee et un arret
automatique. Les ecritures, fournisseurs externes et campagnes lourdes ciblent
un environnement ephemere cree a la demande.

### 2.4 Matrice d'autorisation des parcours

| Parcours | Production | Environnement ephemere |
| --- | --- | --- |
| `PERF-JRN-01` Marketplace | Lectures publiques et accueil agrege sans achat | Parcours complet hors paiement reel |
| `PERF-JRN-02` Localeo Live | Configuration et lectures sur installations synthetiques existantes | Onboarding, preferences, suivis et lectures |
| `PERF-JRN-03` Commercant | Authentification unique puis consultations seulement | Invitations, decisions et validations comprises |
| `PERF-JRN-04` Animation | Authentification unique, dashboard, listes et details | Mutations, tirages, gains et exports au volume maximal |
| `PERF-JRN-05` BackOffice | Authentification unique, pages et API en lecture | Mutations, support, communications simulees et exports |
| `PERF-JRN-06` Achat coffret | Interdit | Stripe Test et cycle de vie complet |
| `PERF-JRN-07` Exploitation | Health, readiness et diagnostics en lecture | Parcours complet autorise |
| `PERF-JRN-08` Traitements asynchrones | Interdit | Backlog, concurrence, interruption et reprise |

`production-readonly.js` constitue une allowlist positive des groupes et
operations autorises. Une route absente de ce manifeste est refusee, meme si sa
methode HTTP est `GET`. Les authentifications techniques necessaires sont
taguees et executees une seule fois par utilisateur virtuel ; elles ne sont pas
incluses dans la boucle de charge nominale.

### 2.5 Secrets et acces reseau

Les credentials applicatifs utilises par les parcours proteges sont stockes
dans la source de secrets Grafana Cloud k6, disponible pour l'execution locale
avec k6 v2, ou dans un mecanisme chiffre equivalent approuve. Ils ne sont pas
passes comme options visibles du test.

La production utilise des comptes de performance dedies, avec les permissions
minimales de lecture. L'environnement ephemere utilise des comptes distincts
autorises a modifier uniquement les donnees du `runId` courant.

Le domaine de chaque backend cible doit figurer dans `LOCALEO_TRUSTED_HOSTS`.
CORS n'a pas a autoriser k6, car k6 n'est pas un navigateur et n'applique pas
la politique CORS. La cible doit etre joignable directement depuis le poste de
l'administrateur.

## 3. Modelisation des parcours

### 3.1 `PERF-JRN-01` Internaute Marketplace

- charger l'accueil geolocalise avec
  `POST /public/referencement/villes/proches/accueil` ;
- rechercher une ville, un commercant, une prestation ou un coffret ;
- consulter les profils et catalogues publics ;
- parcourir les collections avec leurs contrats de pagination ;
- consulter un coffret.

Modele principal : arrivees ouvertes exprimees en parcours par seconde.
L'initialisation de paiement appartient a `PERF-JRN-06`.

### 3.2 `PERF-JRN-02` Internaute Localeo Live

- charger `/public/localeo-live/configuration` ;
- creer une installation uniquement dans le scenario d'onboarding ;
- lire et modifier les preferences ;
- consulter suivis, animations et notifications ;
- marquer une notification comme lue ;
- consulter participation, QR code et passeport coffret.

Les installations recurrentes sont preparees avant le tir et reparties entre
les utilisateurs virtuels. Un profil `spike` reproduit l'ouverture simultanee
suivant une notification.

### 3.3 `PERF-JRN-03` Commercant

- ouvrir une session de test et charger le contexte commercant ;
- consulter activite, animations et notifications ;
- ouvrir puis accepter ou refuser une invitation ;
- valider une prestation ou une etape d'animation avec un QR unique ;
- consulter les documents et informations utiles.

Modele principal : utilisateurs concurrents avec temps de reflexion. Les tests
d'idempotence utilisent volontairement la meme ressource ; les autres ecritures
utilisent une ressource unique par iteration.

### 3.4 `PERF-JRN-04` Animation / collectivite

- ouvrir une session Animation ;
- consulter contexte portail, commune active et abonnement ;
- consulter dashboard, modeles et animations ;
- ouvrir detail, configuration et workflow ;
- consulter participants, validations, live, tirages, gains, flyers et bilans ;
- mesurer separement les exports CSV et PDF.

Creation, publication, cloture, tirage et envoi de gain sont des sous-scenarios
specialises. Ils ne sont pas repetes dans la boucle nominale.

### 3.5 `PERF-JRN-05` Administrateur BackOffice

- authentifier une session administrateur avec cookies et CSRF ;
- charger dashboard et listes SQLAdmin ;
- effectuer les recherches et ouvrir les visions 360 ;
- consulter catalogue, documents, support, communications et reversements ;
- modifier uniquement les objets reserves au `runId`.

Les pages HTML et les API internes sont mesurees avec des tags distincts. Les
operations financieres ou de communication sont simulees ou neutralisees.

### 3.6 `PERF-JRN-06` Achat et cycle de vie d'un coffret

- initialiser un paiement Stripe de test ;
- confirmer le paiement par un webhook signe de test ;
- rejouer le webhook pour mesurer l'idempotence ;
- retrouver achat et instances creees ;
- ajouter une instance a Localeo Live ;
- consulter son passeport puis valider une prestation dediee.

Ce parcours mesure la chaine transactionnelle independamment du trafic de
consultation Marketplace.

### 3.7 `PERF-JRN-07` Exploitation / Localeo Control

- charger resume du jour, evenements et animations ;
- consulter health des batchs et readiness ;
- ouvrir les surfaces de diagnostic autorisees.

Ce parcours est execute seul puis en parallele d'une pointe Marketplace ou
Live. Les outils de diagnostic doivent rester accessibles sous charge.

### 3.8 `PERF-JRN-08` Traitements asynchrones

- injecter un backlog borne et identifiable ;
- declencher ou laisser reprendre les batchs autorises ;
- mesurer debit, age du plus ancien element et temps d'absorption ;
- interrompre puis reprendre le traitement ;
- verifier revendication concurrente, idempotence et absence de doublons.

Sur l'environnement ephemere, Stripe utilise ses cles de test, l'email utilise
`EMAIL_DEV_MODE=true`, le SMS `SMS_DEV_MODE=true`, le WebPush un adaptateur
simule et le stockage un espace dedie. Leur latence et leurs erreurs peuvent
etre controlees. Aucun de ces effets de bord n'est autorise pendant un
benchmark de production.

### 3.9 Authentification et sessions

- Marketplace utilise les routes publiques sans identifiant ;
- Localeo Live repartit des couples `installation_id`/secret distincts entre
  les utilisateurs virtuels ;
- Commercant et Animation utilisent des comptes synthetiques dedies a leur
  role et n'authentifient pas a nouveau chaque iteration ;
- BackOffice conserve un cookie et le jeton CSRF dans le cookie jar du VU ;
- les credentials et tokens ne figurent jamais dans les tags, erreurs ou
  artefacts ;
- un scenario d'authentification separe peut mesurer la connexion sur la cible
  ephemere, sans la confondre avec la performance des ecrans metier.

En production, seuls des comptes synthetiques preexistants et explicitement
autorises sont utilises. Aucune donnee n'y est preparee ou nettoyee par le banc.

## 4. Profils de charge

| Profil | Usage | Declenchement retenu |
| --- | --- | --- |
| `smoke` | Verifier scripts, donnees et contrats avec une charge minimale | Manuel, avant toute campagne |
| `nominal` | Reproduire la baseline technique puis le pic observe | Manuel |
| `peak` | Verifier une pointe soutenue, initialement deux fois le nominal | Manuel et supervise |
| `stress` | Augmenter par paliers jusqu'au franchissement des seuils | Manuel, supervise, cible ephemere |
| `spike` | Produire une montee brutale, notamment apres WebPush | Manuel, supervise, cible ephemere |
| `soak` | Detecter fuites, accumulation et epuisement de ressources | Manuel, supervise, cible ephemere |

Marketplace utilise principalement un modele d'arrivees ouvertes. Les portails
Commercant, Animation et BackOffice utilisent des utilisateurs concurrents avec
temps de reflexion. Les tests de capacite d'un endpoint peuvent employer un
debit constant independant de sa latence.

### 4.1 Calibration initiale sans mesure de trafic

La calibration s'effectue d'abord sur la cible ephemere :

1. executer un smoke avec `1 VU` et une iteration de chaque parcours retenu ;
2. appliquer un premier palier de `1 iteration/s` pendant cinq minutes ;
3. doubler le debit a chaque palier tant que les seuils et ressources restent
   stables ;
4. au premier echec, revenir au dernier palier valide et progresser par pas de
   `25 %` pour identifier le premier point de saturation ;
5. retenir comme baseline technique `70 %` du plus haut debit stable ;
6. remplacer cette baseline par une charge nominale metier lorsque des mesures
   de trafic fiables seront disponibles.

Chaque palier comporte une montee progressive avant son plateau. Le changement
de palier exige l'accord de l'administrateur qui surveille CPU, memoire,
connexions et erreurs. En production, aucune progression automatique n'est
permise : chaque nouveau plafond fait l'objet d'un lancement distinct.

### 4.2 Contraintes par cible

- production : `smoke`, `nominal` borne et eventuellement `peak` en lecture,
  apres validation explicite ;
- ephemere : tous les profils et tous les parcours ;
- `stress`, `spike` et `soak` : exclusivement ephemere ;
- tests asynchrones et fournisseurs : exclusivement ephemere.

### 4.3 Capacite du generateur local

Le poste local fait partie du systeme de mesure. Le preflight enregistre la
version de k6, Windows, le nombre de CPU logiques, la memoire disponible et le
type de connexion reseau, sans collecter de donnee personnelle inutile.

Pendant la campagne, l'administrateur surveille aussi CPU, memoire et debit du
poste. Un resultat n'est pas qualifiable si le generateur local sature ou ne
produit pas le debit demande. Deux campagnes ne sont comparees que si le profil
du poste, la version de k6 et les conditions reseau sont equivalents.

## 5. Campagnes isolees et campagne mixte

Chaque parcours est d'abord execute seul. Cela attribue un ralentissement au
bon sous-systeme et etablit sa capacite propre.

La repartition mixte initialement proposee pour les parcours interactifs est :

| Parcours | Part initiale |
| --- | ---: |
| Marketplace | 55 % |
| Localeo Live | 25 % |
| Commercant | 10 % |
| Animation / collectivite | 5 % |
| Administrateur BackOffice | 3 % |
| Achat coffret | 2 % |

Cette repartition initiale est validee par `PERF-ARB-07`, puis sera recalibree
avec les metriques reelles. Les
parcours Exploitation et Traitements asynchrones sont injectes comme charges de
fond ou campagnes controlees ; ils ne sont pas dilues dans ces pourcentages.

## 6. Jeux de donnees

| Profil | Usage |
| --- | --- |
| `small` | Validation locale rapide des scripts |
| `reference` | Baseline et executions manuelles comparables |
| `capacity` | Stress, pointe et endurance |

Les donnees couvrent plusieurs communes, des catalogues publies, des comptes et
habilitations par role, des installations Live, des animations sur plusieurs
annees, des participants, validations, gains, notifications, achats et lignes
d'outbox.

### 6.1 Donnees de base et surcouche de campagne

Le chargement separe deux ensembles :

1. un socle synthetique stable et volumineux, commun aux campagnes comparables ;
2. une surcouche mutable propre au `runId`, contenant comptes, installations,
   invitations, QR codes, achats de test et ressources reservees aux ecritures.

Le socle est genere de maniere deterministe avec une graine fixe. Il est valide,
puis exporte sous forme de dump PostgreSQL `data-only`. Le dump n'est pas
versionne dans Git : il est conserve comme artefact prive. Le depot contient son
manifeste, sa version, son empreinte SHA-256 et le niveau de migration attendu.

```text
output/performance/datasets/small/
  small.dump
  small.json
  secrets.json
  k6/
    marketplace.json
    localeo-live.json
    commercant.json
    animation.json
    backoffice.json
    achat-coffret.json
    exploitation.json
    traitements-asynchrones.json
```

Les snapshots et fichiers k6 ne contiennent ni secret brut, ni token actif, ni
donnee issue de la production. Les valeurs brutes sont conservees dans le
sidecar prive `secrets.json`, ignore par Git, alors que seuls leurs hashes sont
inseres dans PostgreSQL.

### 6.2 Construction d'un snapshot

La construction controlee d'un snapshot execute les etapes suivantes :

1. creer une base vide isolee ;
2. appliquer toutes les migrations ;
3. generer des UUID v5 et entites communes avec la graine versionnee
   `epic59-small-v1` ;
4. reutiliser les fonctions de hash metier pour les sessions, API keys et
   tokens, en produisant de nouveaux secrets bruts a chaque generation ;
5. utiliser des insertions groupees ORM dans une transaction unique ;
6. valider les cardinalites, relations, statuts et index attendus ;
7. produire le dump `data-only` et son manifeste ;
8. calculer puis enregistrer l'empreinte SHA-256.

Le generateur refuse une base contenant deja des villes, commercants, coffrets,
achats, animations ou installations Live. Le dump n'est jamais reutilise si son
empreinte ne correspond pas au manifeste ou avec une version de schema
incompatible.

### 6.3 Orchestration par la campagne

`run-campaign.ps1` est l'unique point d'entree d'une campagne mutable. Il gere
la sauvegarde, l'import du dataset, l'execution k6 et la restauration. Les
scripts internes ne doivent pas etre appeles directement en exploitation.

Avant toute mutation, la campagne :

1. verifie que la cible est `ephemeral` et refuse la production ;
2. acquiert un verrou PostgreSQL dedie pour interdire deux campagnes
   concurrentes ;
3. verifie que le scheduler, les batchs et les acces utilisateurs sont
   neutralises sur la cible ;
4. releve la version du schema et les marqueurs de controle de la base ;
5. execute un `pg_dump` complet au format custom, sans owner ni ACL ;
6. calcule l'empreinte SHA-256 du dump et verifie sa lisibilite avec
   `pg_restore --list` ;
7. enregistre dump, empreinte et etat dans
   `output/performance/<runId>/database-before.dump`.

L'import ne commence que si la sauvegarde est validee. La campagne remet alors
la base ephemere a zero, applique les migrations du commit teste, verifie
l'empreinte du snapshot `data-only`, charge le profil demande et valide les
cardinalites minimales declarees dans le manifeste. Les ressources k6 non
secretes sont fournies par les fichiers JSON rattaches au meme manifeste ; les
secrets restent injectes par l'environnement.

Elle produit ensuite `state.json`, contenant la derniere etape terminee, le
resultat expurge du test et, lorsque necessaire, le chemin du dump de reprise.
Le preflight `k6 inspect` constitue la preuve que configuration, plafonds,
parcours et ressources sont lisibles avant la premiere mutation de la base.

`state.json` progresse dans les etats `PREFLIGHT_OK`,
`BACKUP_VERIFIED`, `DATASET_LOADED`, `SMOKE_OK`, `TEST_FINISHED`,
`RESTORE_VERIFIED` ou `RESTORE_FAILED`. Le repertoire de backup est exclu de
Git et ses chemins ne sont jamais construits a partir d'une valeur non validee.

La preparation est idempotente pour un meme `runId`. Une nouvelle campagne
utilise un nouvel identifiant afin d'eviter les collisions entre utilisateurs
virtuels et les resultats d'une campagne precedente.

### 6.4 Restauration garantie

La restauration est placee dans le bloc de finalisation de la campagne et est
executee apres succes, echec de seuil, erreur k6 ou interruption controlee :

1. arreter les appels k6 et maintenir les traitements de fond desactives ;
2. remettre la base ephemere a zero ;
3. restaurer `database-before.dump` avec `pg_restore` ;
4. verifier version de schema, readiness et marqueurs releves avant campagne ;
5. liberer le verrou PostgreSQL uniquement apres validation ;
6. supprimer le dump temporaire apres validation de la restauration.

Si la restauration echoue, la campagne passe a `RESTORE_FAILED`, conserve le
dump et son empreinte, maintient l'environnement bloque et fournit les donnees
de reprise dans `state.json`. Elle ne masque jamais cet echec
derriere le resultat k6.

### 6.5 Distribution aux utilisateurs virtuels k6

Les fichiers JSON destines a k6 ne contiennent que les identifiants et donnees
non secretes necessaires aux parcours. Ils sont charges dans le contexte
d'initialisation avec `open()` puis partages par `SharedArray`.

- les lectures peuvent reutiliser un jeu d'identifiants selon une distribution
  stable ;
- chaque ecriture recoit une ressource unique determinee par le VU et
  l'iteration ;
- une ressource deja consommee n'est jamais reutilisee, sauf test explicite
  d'idempotence ;
- les secrets sont recuperes separement depuis la source de secrets et ne sont
  jamais inscrits dans les fichiers JSON.

Le preflight verifie que le nombre de ressources mutables couvre le maximum
theorique d'iterations du profil demande.

### 6.6 Production et nettoyage

Aucun backup de campagne, seed, import, restauration ou nettoyage n'est execute
sur la production. Les parcours de production utilisent un petit manifeste
d'identifiants synthetiques preexistants, exclusivement autorises en lecture.
Un `pg_dump` de production fausserait la mesure et ajouterait une charge inutile
pour un benchmark sans mutation ; la politique normale de sauvegarde de
production reste independante de l'Epic.

La restauration de `database-before.dump` est l'unique retour a l'etat
principal pris en charge. Aucun script de nettoyage partiel n'est fourni : cela
evite une suppression par plage, wildcard ou anciennete qui pourrait toucher
des donnees ne pouvant pas etre rattachees exactement au `runId`.

## 7. Seuils initiaux

Ces seuils sont des propositions de demarrage. Ils deviennent contractuels
uniquement apres baseline sur un environnement representatif.

| Parcours ou operation | Seuil p95 initial |
| --- | ---: |
| Marketplace - lectures simples | 400 ms |
| Marketplace - accueil agrege | 800 ms |
| Localeo Live - listes et notifications | 600 ms |
| Commercant - lectures | 700 ms |
| Commercant - ecritures | 1 000 ms |
| Animation - listes et detail | 700 ms |
| Animation - dashboard et agregats | 900 ms |
| BackOffice - listes et recherches | 1 000 ms |
| Visions 360 | 1 500 ms |
| Achat - operations transactionnelles internes | 1 000 ms |
| Exports CSV/PDF | 2 500 ms |

Sous charge nominale, le taux d'erreurs inattendues propose est inferieur a
`0,5 %`, aucune iteration ne doit etre abandonnee faute de generateur et les
checks fonctionnels critiques doivent tous reussir. Les erreurs metier attendues
ne sont pas confondues avec les erreurs techniques.

### 7.1 Conditions d'arret anticipe

Une campagne est interrompue lorsque l'un des cas suivants est observe :

- taux d'erreurs techniques superieur ou egal a `2 %` pendant 30 secondes ;
- p95 superieur au double du seuil du parcours pendant 60 secondes ;
- iterations abandonnees par manque de VU ;
- redemarrage d'une instance, saturation durable du pool SQL ou perte de
  readiness ;
- effet de bord externe inattendu ;
- decision manuelle de l'administrateur.

Ces conditions protegent la cible mais ne remplacent pas les seuils de succes,
plus stricts, utilises pour qualifier le resultat final.

## 8. Mesures et diagnostic

### Cote generateur

- debit demande et debit effectivement produit ;
- latences p50, p90, p95 et p99 ;
- taux d'erreurs et checks par tag ;
- iterations abandonnees ;
- temps de connexion, attente, transfert et traitement.

### Cote plateforme

- CPU, memoire et redemarrages ;
- workers disponibles et files d'attente ;
- connexions PostgreSQL, attente du pool SQLAlchemy et timeouts ;
- duree et volume des requetes SQL ;
- verrous, contentions et requetes lentes ;
- profondeur et age des outbox ;
- duree, debit et echec des batchs.

Chaque campagne conserve l'horodatage permettant de correler les deux sources.

## 9. Resultats et execution manuelle

Le resultat agrege est lisible dans Grafana Cloud k6. Les mesures, la
configuration effective expurgee et les metadonnees de campagne sont conservees
pendant une semaine. Un seuil franchi provoque l'echec de la campagne.

### 9.1 Procedure de lancement

1. choisir la cible, le parcours, le profil, le dataset et les plafonds ;
2. verifier les limites et la retention du projet Grafana Cloud Free ;
3. authentifier le binaire local avec `k6 cloud login` sans journaliser le
   token ;
4. lancer `run-campaign.ps1`, seul point d'entree operateur ;
5. laisser la campagne executer le preflight et, sur cible ephemere, verrouiller
   puis sauvegarder la base ;
6. laisser la campagne importer le dataset, creer la surcouche `runId` et
   valider la readiness ;
7. executer par la campagne le smoke puis `k6 cloud run --local-execution
   performance/k6/main.js` ;
8. surveiller Grafana Cloud, le generateur local, Render et PostgreSQL ;
9. laisser le bloc de finalisation restaurer la base, quel que soit le resultat
   k6 ;
10. verifier la preuve de restauration avant de mettre en veille la cible.

Les parcours isoles sont lances sequentiellement. La campagne mixte est lancee
explicitement apres leur validation. Pointe, stress, spike et endurance restent
surveilles jusqu'a leur fin ou leur arret anticipe. Aucune campagne n'est
declenchee par la CI ou un ordonnanceur.

Les parcours isoles ne sont pas lances en parallele sur la meme cible, sauf si
la campagne cherche explicitement a mesurer leur contention.

### 9.2 Nommage et preuve

Nom Grafana Cloud :

```text
localeo-api/<target>/<journey>/<profile>
```

Chaque run conserve pendant une semaine :

- `runId`, commit et date ;
- cible et topologie ;
- parcours, profil, dataset et plafonds ;
- version des scripts ;
- empreinte du backup initial et statut de restauration, sans conserver le dump
  dans Grafana Cloud ;
- resultat des checks et seuils ;
- lien Grafana Cloud et synthese de diagnostic ;
- identite de l'administrateur declencheur.

## 10. Topologie de l'environnement ephemere

- PostgreSQL : `0,5 CPU` et `1 Go RAM` ;
- backend Render : `0,5 CPU` et `512 Mo RAM` ;
- creation et initialisation a la demande ;
- destruction ou mise en veille apres collecte des resultats ;
- ecarts avec la production inscrits dans les metadonnees de campagne.

## 11. Verification du banc de test

Le banc possede ses propres tests de non-regression :

- validation des variables et des plafonds ;
- refus d'un hote absent de l'allowlist ;
- refus d'un parcours mutable en production ;
- refus de `stress`, `spike` et `soak` en production ;
- absence de secrets dans le resume et les tags ;
- unicite des donnees mutables par `runId` ;
- echec attendu lorsqu'un seuil de reference est volontairement depasse ;
- smoke de chaque parcours sur le dataset `small`.

Ces controles sont executes manuellement avant une campagne ; ils ne creent pas
de declenchement automatique de charge.

## 12. Validation de l'action d'audit

`ASP-ACT-036` peut passer a `CORRIGE` lorsque scripts, donnees, seuils et
procedure sont livres. Le second etat `VALIDE` exige :

- une campagne de reference reproductible reussie ;
- une preuve d'echec sur une regression controlee ;
- des resultats archives et rattaches au commit ;
- un diagnostic possible depuis les metriques serveur ;
- la confirmation qu'aucun effet externe reel n'a ete produit.
