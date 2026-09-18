# Epic 48 — Ordonnancement des batchs avec APScheduler

## Statut

- Criticité : `Critique`
- Statut : `Termine`
- Domaine principal : `exploitation`
- Dépendance structurante : Epic 23 — Gestion des batchs et ordonnancement
- Cible de déploiement : service FastAPI existant sur Render, avec singleton
  logique garanti par un lease PostgreSQL

## Objectif

Intégrer APScheduler afin d'exécuter automatiquement les batchs Localeo selon
leurs fréquences cibles, tout en réutilisant l'inventaire, les verrous,
l'historique, les compteurs, le health et les reprises manuelles déjà livrés
par l'Epic 23.

L'ordonnanceur ne porte aucune règle métier. Il détermine qu'un traitement est
échu, puis appelle l'endpoint HTTP protégé correspondant. L'API conserve ainsi
la validation, l'exécution, le verrouillage et l'historisation canoniques.

## Contexte et problème

Les batchs sont actuellement exécutables par API protégée et par le
back-office. Leurs fréquences sont documentées, mais le déclenchement récurrent
reste dépendant d'un ordonnanceur externe ou d'une action manuelle.

Cette situation crée plusieurs risques :

- oubli ou retard d'un batch critique ;
- multiplication des configurations cron hors du dépôt ;
- absence de visibilité sur l'état réel de l'ordonnanceur ;
- divergence entre les paramètres documentés et ceux utilisés en production ;
- double déclenchement pendant un déploiement ou une mauvaise configuration ;
- reprise incertaine après une indisponibilité de la plateforme.

## Positionnement par rapport à l'Epic 23

L'Epic 23 reste le socle d'exécution et de supervision :

- `BATCH_DEFINITIONS` inventorie les traitements ;
- `BatchRunner` journalise les exécutions ;
- `verrous_batch` empêche les exécutions concurrentes ;
- `executions_batch` conserve les résultats ;
- le back-office permet le lancement manuel ;
- les endpoints de maintenance exposent inventaire, historique et health.

L'Epic 48 ajoute le moteur de planification dans le service FastAPI existant,
son élection de leader, son cycle de vie, sa projection de supervision et la
procédure de bascule depuis les déclencheurs externes.

## Principes validés

1. APScheduler est initialisé dans le lifespan du service **FastAPI existant**.
   Chaque worker peut lancer le coordinateur, mais seul le détenteur d'un lease
   PostgreSQL démarre et pilote les jobs.
2. La version cible est la branche stable APScheduler `3.11.x`, compatible avec
   Python 3.14 ; aucune préversion `4.x` n'est utilisée en production.
3. L'intégration utilise `BackgroundScheduler` afin que la boucle APScheduler
   n'occupe pas la boucle événementielle FastAPI.
4. Les planifications sont déclaratives et recréées au démarrage. Chaque
   fréquence possède une valeur par défaut et une surcharge par variable
   d'environnement validée au démarrage.
5. APScheduler ne devient ni un moteur métier ni une file de messages.
6. APScheduler appelle les endpoints HTTP protégés existants avec une clé API
   portant le scope `internal:batch`. Il n'appelle pas directement les use cases.
7. `BatchRunner`, `executions_batch` et `verrous_batch` restent obligatoires
   pour chaque exécution, quel que soit son point d'entrée.
8. Chaque job utilise `max_instances=1`. Le verrou SQL reste la protection
   transverse en cas de second ordonnanceur ou de lancement manuel simultané.
9. Le fuseau de planification est explicite et vaut `UTC` en production.
10. Le leader publie son lease, un heartbeat et les prochaines échéances afin
    que le health distingue un batch vide d'un ordonnanceur arrêté.
11. Une seule source de déclenchement automatique est active par batch pendant
    et après la bascule.
12. Les endpoints protégés sont conservés pour la reprise et le diagnostic.

## Périmètre fonctionnel

### Inclus

- ajout de la dépendance APScheduler avec une borne de version maîtrisée ;
- intégration d'un coordinateur APScheduler au lifespan FastAPI ;
- élection d'un leader par lease PostgreSQL pour supporter plusieurs workers,
  instances et le recouvrement temporaire des déploiements Render ;
- enrichissement structuré des définitions de batch avec endpoint HTTP,
  trigger, paramètres, clé de configuration, politique de retard et activation ;
- client HTTP interne authentifié pour appeler les endpoints batch existants ;
- surcharge de chaque fréquence par variable d'environnement ;
- enregistrement idempotent des jobs au démarrage ;
- politiques `coalesce`, `misfire_grace_time` et `max_instances` explicites ;
- arrêt propre du scheduler lors de la fermeture du lifespan FastAPI ;
- heartbeat de l'ordonnanceur et projection des prochaines exécutions ;
- supervision dans le back-office et dans le health batch ;
- activation globale par configuration ;
- identité technique stable `system:apscheduler` dans les traces ;
- tests unitaires, d'intégration et de non-régression ;
- configuration du service web Render en mode toujours actif ;
- procédure de bascule, arrêt, reprise et retour arrière.

### Hors périmètre initial

- file distribuée Celery, RabbitMQ, Kafka ou Render Workflows ;
- ordonnancement métier créé librement par les partenaires ;
- haute disponibilité active/active de plusieurs schedulers ;
- remplacement des webhooks temps réel ;
- suppression des endpoints batch existants ;
- exécution arbitraire de code ou d'URL configurée depuis le back-office ;
- stockage de secrets dans les définitions de jobs ;
- migration vers APScheduler 4 avant sa disponibilité stable et sa recette.

## User Stories

### `PRD-427` — Héberger l'ordonnanceur dans FastAPI

En tant qu'exploitant, je veux que le scheduler fonctionne dans le service
FastAPI déjà déployé afin de ne pas créer un second service Render, tout en
garantissant un unique leader actif.

Critères d'acceptation :

- le lifespan FastAPI démarre et arrête un coordinateur APScheduler ;
- chaque processus tente d'acquérir un lease PostgreSQL atomique ;
- seul le détenteur du lease démarre les jobs, les autres processus restant en
  veille et capables de prendre le relais après expiration ;
- une configuration invalide empêche le coordinateur de se déclarer sain et
  produit un diagnostic explicite ;
- le coordinateur utilise la configuration et la base pour son lease ; les
  providers métier restent exclusivement appelés derrière les endpoints HTTP.

### `PRD-428` — Structurer et configurer les planifications

En tant que développeur, je veux une définition exécutable de chaque fréquence
afin d'éliminer les pseudo-crons et les paramètres dispersés.

Critères d'acceptation :

- chaque batch automatique porte un identifiant stable, un endpoint, une
  fréquence par défaut, une clé d'environnement, un fuseau, des paramètres non
  sensibles et une politique de retard ;
- une expression cron fournie par l'environnement surcharge la valeur par
  défaut sans modification de code ;
- les batchs manuels ou de reprise ne sont jamais planifiés par défaut ;
- une validation au démarrage refuse les codes dupliqués, endpoints absents,
  clés de configuration incohérentes ou expressions cron invalides ;
- l'inventaire API expose la planification structurée sans casser les champs
  existants.

### `PRD-429` — Déclencher les endpoints HTTP protégés

En tant que mainteneur, je veux qu'APScheduler appelle les endpoints batch
existants afin que l'API demeure le point d'exécution canonique.

Critères d'acceptation :

- méthode, chemin, query string ou corps viennent exclusivement du registre
  applicatif validé ;
- l'URL de base et la clé API sont fournies par l'environnement ;
- la clé API possède le scope `internal:batch` et n'est jamais journalisée ;
- le correlation ID est transmis à l'API et récupéré dans le résultat ;
- toute réponse non `2xx`, timeout ou réponse invalide produit un échec
  APScheduler observable ;
- aucune URL complète arbitraire n'est exécutable depuis une donnée persistée.

### `PRD-430` — Enregistrer les jobs APScheduler de façon idempotente

En tant que système, je veux reconstruire les jobs au démarrage afin que la
configuration d'environnement effective soit appliquée après un déploiement.

Critères d'acceptation :

- chaque job utilise un `schedule_id` stable ; il est identique au `batch_code`
  sauf lorsqu'un même batch porte plusieurs planifications paramétrées, comme
  les reprises Stripe Connect à 14 et 90 jours ;
- un redémarrage remplace la définition précédente sans créer de doublon ;
- les jobs désactivés ne sont pas enregistrés ;
- les prochaines dates calculées sont projetées pour la supervision.

### `PRD-431` — Empêcher les exécutions concurrentes

En tant que responsable exploitation, je veux conserver une double protection
contre les exécutions parallèles afin de sécuriser les traitements idempotents
et les appels providers.

Critères d'acceptation :

- chaque job APScheduler utilise `max_instances=1` ;
- `BatchRunner` acquiert toujours le verrou SQL existant ;
- un lancement manuel concurrent est refusé proprement et historisé ;
- une seconde instance de scheduler accidentelle ne produit pas deux effets
  métier.

### `PRD-432` — Gérer les retards et redémarrages

En tant qu'exploitant, je veux une politique explicite des exécutions manquées
afin qu'un redémarrage ne provoque ni perte silencieuse ni rafale de traitements.

Critères d'acceptation :

- `coalesce` et `misfire_grace_time` sont définis par famille de batchs ;
- les batchs fréquents reprennent au prochain tick sans rejouer chaque échéance ;
- les batchs journaliers critiques peuvent déclencher une reprise unique au
  démarrage lorsqu'ils sont en retard ;
- toute reprise de démarrage passe par les mêmes verrous et traces.

### `PRD-433` — Gérer le cycle de vie du scheduler

En tant qu'exploitant, je veux un démarrage et un arrêt propres afin de réduire
les exécutions interrompues pendant les déploiements.

Critères d'acceptation :

- le lifespan relaie l'arrêt de la plateforme au coordinateur ;
- l'arrêt du lifespan libère le lease lorsque cela est possible ;
- il cesse d'accepter de nouveaux jobs avant de fermer ses exécuteurs ;
- son démarrage, son arrêt et toute erreur fatale sont journalisés ;
- un verrou expiré reste récupérable après une interruption brutale.

### `PRD-434` — Superviser la présence de l'ordonnanceur

En tant qu'exploitant, je veux connaître l'état et la dernière présence du
scheduler afin de diagnostiquer un arrêt avant que les batchs ne soient en
retard.

Critères d'acceptation :

- le leader publie son identité, sa version applicative, son démarrage, son
  lease et un heartbeat périodique ;
- la projection expose pour chaque batch son activation, son trigger et sa
  prochaine exécution ;
- le health devient `CRITICAL` si le heartbeat dépasse le seuil configuré ;
- les données de supervision ne deviennent pas une seconde source de vérité
  pour les règles métier.

### `PRD-435` — Piloter l'ordonnanceur depuis le back-office

En tant qu'administrateur, je veux visualiser les jobs planifiés avec les
exécutions afin de comprendre rapidement la situation opérationnelle.

Critères d'acceptation :

- la vue Batchs affiche état du scheduler, dernière présence et version ;
- elle affiche dernière et prochaine exécution, trigger, statut et retard ;
- le lancement manuel existant reste disponible ;
- aucune modification libre de callable ou de paramètres sensibles n'est
  proposée.

### `PRD-436` — Configurer et sécuriser l'ordonnanceur

En tant que responsable technique, je veux une configuration explicite afin de
maîtriser son activation selon l'environnement.

Critères d'acceptation :

- l'activation globale, le fuseau, l'identité, le heartbeat et la concurrence
  sont configurables ;
- l'URL de base de l'API, les expressions cron et le timeout de connexion HTTP
  sont configurables ; le timeout de lecture reprend celui de chaque batch ;
- la durée du lease et la fréquence de tentative des workers en veille sont
  configurables et cohérentes avec le heartbeat ;
- les secrets providers restent dans les mécanismes existants ;
- l'appel utilise `LOCALEO_INTERNAL_BATCH_API_KEY`, avec le scope
  `internal:batch` ;
- l'identité technique de la clé et le correlation ID sont propagés sans faire
  confiance à un acteur fourni librement par un header.

### `PRD-437` — Tester l'ordonnancement sans attendre le temps réel

En tant que responsable qualité, je veux des tests déterministes afin de valider
les triggers, retards et redémarrages sans tests lents.

Critères d'acceptation :

- l'horloge et le scheduler sont injectables ou pilotables dans les tests ;
- les tests couvrent enregistrement idempotent, job désactivé, misfire,
  coalescence, verrou concurrent, exception et arrêt ;
- aucun test automatisé n'attend plusieurs minutes ;
- les contrats de tests dédiés aux classes publiques sont respectés.

### `PRD-438` — Déployer et basculer sans double ordonnanceur

En tant qu'exploitant, je veux une procédure de déploiement progressive afin
d'activer APScheduler sans conserver les anciens déclencheurs automatiques.

Critères d'acceptation :

- le service FastAPI est d'abord déployé scheduler désactivé ;
- le plan Render garantit qu'au moins une instance web reste active ;
- la liste des déclencheurs externes à arrêter est vérifiée batch par batch ;
- l'activation est progressive, observable et réversible ;
- le rollback réactive une seule source de déclenchement ;
- la procédure de recette vérifie heartbeat, prochaine exécution, historique,
  compteurs et absence de doublons.

## Découpage proposé

| Lot | Contenu | Dépendances |
|---|---|---|
| 0 | Arbitrages, dépendance, contrats et choix de déploiement | Epic 23 |
| 1 | Catalogue structuré, configuration des fréquences et client HTTP | Lot 0 |
| 2 | Intégration APScheduler au lifespan et enregistrement des jobs | Lot 1 |
| 3 | Concurrence, misfires, reprise et arrêt propre | Lot 2 |
| 4 | Heartbeat, projection, health et back-office | Lots 2 et 3 |
| 5 | Configuration du service FastAPI Render et procédure de bascule | Lots 2 à 4 |
| 6 | Tests, recette générale et documentation d'exploitation | Lots 1 à 5 |

## Indicateurs de succès

- 100 % des batchs automatiques éligibles enregistrés avec un trigger valide ;
- un seul leader scheduler actif, quel que soit le nombre de workers HTTP ;
- 0 double effet métier lors d'un lancement concurrent ou d'un redéploiement ;
- heartbeat visible moins de deux minutes après le démarrage ;
- 100 % des exécutions APScheduler historisées avec acteur et correlation ID ;
- 0 ancien déclencheur automatique encore actif après la bascule complète ;
- diagnostic d'un scheduler arrêté possible depuis le back-office sans accès
  aux logs de la plateforme.

## Arbitrages

Les décisions `APS-ARB-01` à `APS-ARB-13` sont validées et intégrées. Leur
historique est conservé dans le
[`registre des arbitrages`](../../specifications/epic-48-apscheduler-ordonnancement-batchs/registre-arbitrages.md).

La conception technique initiale est disponible dans
[`docs/specifications/epic-48-apscheduler-ordonnancement-batchs`](../../specifications/epic-48-apscheduler-ordonnancement-batchs/README.md).
