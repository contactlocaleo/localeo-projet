# Backlog Epic 44 - Observabilite et logs des Use Cases

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : rendre chaque execution de Use Case identifiable, correlable et
  exploitable afin d'accelerer le diagnostic des incidents sans exposer de
  donnees sensibles.
- Exigence fondatrice : chaque appel d'un Use Case public doit produire un log.
- Pourquoi maintenant : les parcours metier, batchs, webhooks et actions
  back-office se multiplient. Les logs HTTP ou provider ne permettent pas
  toujours de savoir quel Use Case a ete execute, pendant combien de temps et
  avec quelle issue.
- Domaine fonctionnel cible : transverse `observabilite`.
- Surfaces concernees : API publique et protegee, routes internes, back-office,
  webhooks, batchs et traitements hors requete HTTP.
- Architecture :
  [EPIC 44 - Observabilite et logs des Use Cases](../../architecture/backend/epics/epic-44-observabilite-logs-use-cases-architecture.md).

## Etat actuel constate

Le backend dispose deja de plusieurs briques :

- `RequestContextMiddleware` cree ou propage `X-Request-ID` ;
- `app/observability.py` fournit la facade transverse, le contexte et la
  redaction des donnees ;
- `app/observability_instrumentation.py` recherche les classes applicatives
  exposant `execute` et journalise `started`, `succeeded` et `failed` ;
- `app/logging_config.py` configure les niveaux et les formats texte/JSON ;
- les batchs possedent leur propre `correlation_id` et un historique persistant ;
- les actions sensibles utilisent un audit persistant distinct des logs.

Les ecarts backend constates lors du cadrage ont ete traites. Les points encore
ouverts relevent maintenant du deploiement et des applications clientes :

- configurer le Log Stream Render et la source Better Stack ;
- creer les dashboards, alertes, retentions et habilitations ;
- adapter les applications clientes pour afficher et copier `Reference erreur` ;
- executer la recette runtime complete en environnement partage.

Cette EPIC consolide et fiabilise le socle existant. Elle ne demande pas
d'ajouter manuellement un `logger.info` dans chaque Use Case.

## User Stories

### PRD-391 - Journaliser chaque appel de Use Case

En tant qu'exploitant, je veux disposer d'un log pour chaque appel de Use Case
afin de savoir quels traitements applicatifs ont reellement ete executes.

Resultats attendus :

- toute methode publique `execute`, synchrone ou asynchrone, d'un Use Case sous
  `app.application` est instrumentee automatiquement ;
- chaque invocation produit un evenement `use_case.started` ;
- chaque invocation produit exactement un evenement terminal
  `use_case.succeeded` ou `use_case.failed` ;
- les appels imbriques de Use Cases sont journalises comme des invocations
  distinctes ;
- un `use_case_invocation_id` unique permet de relier debut et fin ;
- le nom de classe, le module et le domaine fonctionnel sont identifies ;
- l'instrumentation ne modifie ni la signature, ni le resultat, ni les
  exceptions du Use Case.

### PRD-392 - Definir un contrat de log stable et structure

En tant qu'exploitant, je veux un schema de log stable afin de rechercher et
agreger les executions sans analyser des messages libres.

Resultats attendus :

- les champs communs sont au minimum `timestamp`, `level`, `event`,
  `environment`, `service`, `use_case`, `module`, `domain`,
  `use_case_invocation_id`, `outcome` et `duration_ms` lorsqu'elle est connue ;
- les noms d'evenements sont stables et documentes ;
- le format production cible est exploitable comme JSON structure ;
- un format texte lisible peut rester disponible en developpement local ;
- les champs absents sont omis ou nuls de maniere coherente ;
- une version de schema permet de faire evoluer le contrat sans ambiguite.

### PRD-393 - Correler Use Cases, requetes, batchs et webhooks

En tant que support technique, je veux suivre une execution de bout en bout afin
de retrouver tous les logs associes a une meme action.

Resultats attendus :

- un appel HTTP propage son `request_id` dans tous les logs de Use Cases ;
- un batch propage son `correlation_id` dans tous les logs de Use Cases ;
- un webhook expose au minimum son `request_id`, le type d'evenement et un
  identifiant provider assaini lorsque celui-ci est autorise ;
- une action back-office expose l'identite technique de l'acteur selon les
  regles d'audit existantes ;
- les appels imbriques peuvent porter un `parent_use_case_invocation_id` ;
- une execution hors HTTP recoit un identifiant de correlation genere si aucun
  contexte n'existe.

### PRD-394 - Proteger les secrets et donnees personnelles

En tant que responsable securite et conformite, je veux que les logs soient
minimises afin qu'ils ne deviennent pas une source de fuite de donnees.

Resultats attendus :

- mots de passe, tokens, signatures, API keys, secrets Stripe, QR, liens signes,
  IBAN et payloads provider complets ne sont jamais journalises ;
- les arguments et valeurs de retour complets ne sont pas journalises au niveau
  nominal ;
- les identifiants metier utiles sont ajoutes par liste blanche ou extracteur
  controle, pas par serialization generique de tout objet ;
- les valeurs autorisees sont tronquees et les collections sont resumees par
  leur nombre lorsque le detail n'est pas necessaire ;
- les messages d'exception sont assainis avant emission ;
- des tests automatiques couvrent la redaction des principales familles de
  secrets et donnees personnelles.

### PRD-395 - Qualifier les succes, erreurs metier et erreurs techniques

En tant qu'exploitant, je veux distinguer les issues d'une execution afin de
prioriser correctement les incidents.

Resultats attendus :

- un succes est journalise en `INFO` avec sa duree ;
- une erreur metier attendue est identifiee par un code stable et un niveau
  adapte, sans faux incident technique ;
- une erreur technique inattendue est journalisee en `ERROR` avec type
  d'exception et stack trace ;
- l'evenement terminal contient `outcome=success`, `business_error` ou
  `technical_error` ;
- la meme exception n'est pas dupliquee inutilement a chaque couche ;
- les erreurs restent relancees vers les gestionnaires existants sans etre
  absorbees par l'instrumentation.

### PRD-396 - Mesurer les performances des Use Cases

En tant que responsable exploitation, je veux mesurer la duree des Use Cases
afin d'identifier les lenteurs et regressions.

Resultats attendus :

- chaque evenement terminal contient `duration_ms` ;
- les seuils de lenteur peuvent etre configures globalement puis surcharges par
  Use Case critique ;
- un Use Case lent produit un signal identifiable sans transformer un succes en
  erreur ;
- les aggregations permettent d'observer volume, taux d'echec et percentiles de
  duree par Use Case ;
- le surcout de l'instrumentation est mesure et borne par un test de performance
  simple.

### PRD-397 - Garantir automatiquement la couverture des Use Cases

En tant que responsable qualite, je veux empecher l'ajout d'un Use Case non
journalise afin de conserver une couverture complete dans le temps.

Resultats attendus :

- un inventaire automatique identifie les classes applicatives publiques
  exposant `execute` ;
- un test echoue si un Use Case eligible n'est pas instrumente ;
- les methodes synchrones, asynchrones, heritees et decorees sont couvertes ;
- les exclusions exceptionnelles sont explicites, documentees et testees ;
- l'instrumentation est idempotente et ne double pas les wrappers lors d'un
  rechargement ;
- le nombre de Use Cases instrumentes au demarrage est journalise et comparable
  au nombre attendu.

### PRD-398 - Configurer les niveaux et le volume des logs

En tant qu'exploitant, je veux piloter le niveau des logs sans redeployer le code
afin d'adapter la verbosite au contexte.

Resultats attendus :

- `LOCALEO_USE_CASES_LOG_LEVEL` pilote effectivement le namespace canonique
  `localeo.use_cases.*` ;
- les evenements debut et fin nominaux restent disponibles selon la politique
  de production actee ;
- les details de diagnostic sont separes du contrat nominal et desactives par
  defaut en production ;
- aucune configuration ne peut activer l'emission de secrets ;
- la politique de volume, cout, rotation et degradation en cas de collecteur
  indisponible est documentee.

### PRD-399 - Rechercher et superviser les logs en exploitation

En tant qu'operateur, je veux rechercher les logs par identifiant et Use Case
afin de diagnostiquer rapidement un incident.

Resultats attendus :

- les logs sont centralises dans un outil interrogeable par environnement ;
- la recherche accepte au minimum `request_id`, `correlation_id`,
  `use_case_invocation_id`, nom de Use Case, outcome et periode ;
- un tableau de bord presente volumes, erreurs et lenteurs des Use Cases
  critiques ;
- des alertes peuvent etre definies sur hausse du taux d'erreur, absence
  anormale d'execution et depassement de duree ;
- les acces aux logs de production sont limites et revus ;
- un lien ou une procedure permet de passer d'un `request_id` communique par un
  utilisateur aux logs correspondants.

### PRD-400 - Documenter et recetter l'observabilite

En tant qu'equipe d'exploitation, je veux une procedure de lecture et de recette
afin d'utiliser le nouveau dispositif de maniere homogène.

Resultats attendus :

- le schema et les niveaux des logs sont documentes ;
- une matrice indique les champs par contexte HTTP, batch, webhook et
  back-office ;
- une recette couvre succes, erreur metier, erreur technique, appel imbrique,
  async, batch et redaction de secrets ;
- la procedure explique comment diagnostiquer un incident a partir d'un
  `request_id` ;
- un controle post-deploiement verifie que les logs arrivent dans le collecteur
  sans donnees sensibles ;
- les responsabilites de consultation, retention et suppression sont actees.

### PRD-401 - Exposer un correlationId dans chaque erreur

En tant qu'utilisateur ou operateur support, je veux que chaque erreur contienne
un `correlationId` afin de pouvoir transmettre une reference unique et retrouver
immediatement les logs associes.

Resultats attendus :

- toute reponse HTTP d'erreur emise par le backend contient un champ JSON
  `correlationId` non vide, quel que soit son statut 4xx ou 5xx ;
- la couverture inclut les erreurs metier, authentification et autorisation,
  validation FastAPI/Pydantic `422`, ressource ou route inexistante `404`,
  limitation eventuelle, fournisseur externe et exception inattendue `500` ;
- pour une requete HTTP, `correlationId` reprend l'identifiant racine cree ou
  accepte par le middleware de requete ; aucun second identifiant concurrent
  n'est genere ;
- la meme valeur est presente dans les logs HTTP et Use Cases associes ;
- le header de correlation expose par la reponse transporte la meme valeur ;
- lorsqu'une erreur se produit hors HTTP, notamment dans un batch, webhook
  differe ou action back-office, un identifiant de correlation est cree ou
  propage et rendu visible dans le resultat operateur ;
- la reponse technique `500` reste generique et ne revele ni exception, ni
  stack trace, ni secret ; `correlationId` sert de cle de diagnostic ;
- les contrats OpenAPI et les applications consommatrices tolerent et affichent
  cette reference dans leurs ecrans d'erreur ;
- la reference est presentee sous le libelle utilisateur constant
  `Reference erreur` et reste visuellement separee du message fonctionnel ;
- les applications permettent de copier la reference complete en une action et
  indiquent `Communiquez cette reference au support` ;
- le format genere par Localeo est reconnaissable sous la forme
  `LOC-<UUID>`, par exemple
  `LOC-2d36be3d-6af3-4ad0-867e-99ffdbfdcf70` ;
- la reference n'est jamais tronquee dans le contrat, les logs, le presse-papier
  ou les echanges avec le support ; un affichage visuel abrege n'est autorise
  que si la valeur complete reste accessible et copiable ;
- des tests de contrat garantissent la presence, le format et la coherence du
  `correlationId` pour chaque famille d'erreur.

Convention actee :

- contrat JSON public : `correlationId` ;
- format des valeurs generees par Localeo : `LOC-<UUID>` ;
- libelle visible : `Reference erreur` ;
- logs et contexte Python internes : `correlation_id` ;
- le champ historique `request_id` est mappe vers la meme valeur pendant la
  migration et ne doit jamais designer une autre execution ;
- `request_id` est maintenu comme alias deprecie jusqu'a une prochaine version
  majeure afin d'eviter un breaking change.

### PRD-402 - Piloter la journalisation par un utilitaire transverse

En tant que developpeur, je veux utiliser un utilitaire unique pour construire,
enrichir, securiser, formater et emettre les logs afin de garantir le meme
contrat d'observabilite sur tous les points d'entree.

Resultats attendus :

- le module transverse d'observabilite fournit une facade publique unique pour
  ouvrir ou enrichir un contexte, recuperer le `correlation_id` courant et
  emettre un evenement structure ;
- l'utilitaire genere, valide, propage et restaure le `correlationId` sans fuite
  de contexte entre requetes ou taches asynchrones concurrentes ;
- un identifiant fourni par un appelant n'est accepte qu'apres validation de sa
  longueur et de son format ; une valeur invalide est remplacee par un nouvel
  identifiant `LOC-<UUID>` et ne peut pas injecter de contenu dans les logs ;
- l'utilitaire centralise le schema, le formatage, l'horodatage, les niveaux,
  les durees, la redaction, la troncature et les champs techniques communs ;
- le contexte HTTP enrichit les evenements avec la methode, le modele de route,
  le statut et un `user_agent` assaini et borne ; la query string brute, les
  cookies et les headers d'authentification ne sont jamais journalises ;
- les valeurs du `User-Agent` ne sont pas considerees fiables : elles sont
  normalisees, tronquees a une taille documentee et ne sont jamais utilisees
  comme identifiant d'acteur ;
- de petits adaptateurs HTTP, webhook, batch et back-office alimentent le meme
  utilitaire ; ils ne reconstruisent ni le format ni les champs communs ;
- l'instrumentation des Use Cases delegue a cet utilitaire la creation des
  evenements `started`, `succeeded` et `failed` ;
- les champs specifiques a un domaine sont ajoutes uniquement par une liste
  blanche ou un extracteur explicite ;
- l'utilitaire ne contient aucune regle metier et ne depend pas d'un fournisseur
  de collecte ;
- une erreur de formatage ou d'emission est assainie et n'interrompt jamais le
  traitement metier ;
- des tests unitaires couvrent le format, la redaction, le `User-Agent`, la
  validation du `correlationId`, la restauration du contexte et l'isolation
  synchrone et asynchrone.

Regle d'usage :

- les middlewares, adaptateurs et instrumentations ne doivent pas appeler
  directement `logging` pour produire les evenements contractuels de l'EPIC ;
- les logs ponctuels purement techniques restent possibles, mais reutilisent le
  contexte et les fonctions de redaction de l'utilitaire des qu'ils portent une
  correlation ou une donnee applicative.

## Contrat minimal propose

Exemple indicatif d'un evenement terminal :

```json
{
  "schema_version": "1",
  "timestamp": "2026-08-12T18:00:00.000Z",
  "level": "INFO",
  "event": "use_case.succeeded",
  "service": "localeo-backend",
  "environment": "test",
  "domain": "gestion_reversement",
  "module": "app.application.gestion_reversement.use_cases.transfers_stripe",
  "use_case": "LancerCampagneTransfersStripe",
  "use_case_invocation_id": "uuid",
  "parent_use_case_invocation_id": null,
  "request_id": "LOC-2d36be3d-6af3-4ad0-867e-99ffdbfdcf70",
  "correlation_id": "LOC-2d36be3d-6af3-4ad0-867e-99ffdbfdcf70",
  "outcome": "success",
  "duration_ms": 84.2
}
```

Le contrat final ne doit pas dependre de la phrase visible dans `message`.

## Decisions de cadrage initiales

- L'exigence couvre chaque invocation, pas seulement chaque classe de Use Case.
- Le socle est transversal et centralise ; les logs manuels dans chaque Use Case
  restent reserves aux decisions metier utiles.
- Le format, le contexte, le `correlationId`, le `User-Agent`, la redaction et
  l'emission des logs contractuels sont pilotes par un utilitaire unique.
- Le namespace canonique est `localeo.use_cases.*`.
- Une invocation produit un evenement de debut et exactement un evenement de
  fin.
- Le contexte est porte par `ContextVar` pour fonctionner en synchrone et
  asynchrone.
- Toute erreur expose un `correlationId` communicable au support et present dans
  les logs associes.
- Sur HTTP, `correlationId` et le `request_id` interne representent la meme
  correlation racine ; aucun nouvel identifiant independant n'est cree.
- Les logs de Use Cases ne remplacent ni les evenements d'audit persistants, ni
  les historiques de batchs, ni les evenements metier.
- Les arguments et resultats complets sont interdits dans les logs nominaux de
  production.
- L'indisponibilite du collecteur de logs ne doit pas bloquer le traitement
  metier.
- Aucun echantillonnage ne supprime les evenements nominaux exiges pour une
  invocation ; le sampling eventuel ne concerne que des details de diagnostic.

## Hors perimetre initial

- remplacement de l'audit financier ou de securite par des logs volatils ;
- stockage du contenu complet des requetes et reponses HTTP ;
- journalisation SQL en production au niveau `DEBUG` par defaut ;
- ajout manuel d'un logger dans chaque Use Case ;
- observabilite frontend ou mobile, a traiter dans une declinaison separee ;
- tracing distribue complet entre tous les fournisseurs externes, reporte a la
  phase 2 OpenTelemetry.

## Arbitrages actes

### Collecte et recherche

- Better Stack Telemetry est le collecteur cible, avec une source stockee dans
  la region Allemagne ;
- l'application ecrit les evenements sur la sortie standard et reste
  independante du fournisseur ; Render transmet les logs vers Better Stack par
  un Log Stream chiffre ;
- l'explorateur Render reste une solution de diagnostic de secours sur sa duree
  de retention native ;
- l'auto-hebergement de Grafana/Loki et l'integration directe d'un SDK
  fournisseur ne font pas partie du MVP.

### Format, niveaux et volume

- le schema contractuel est versionne `1` ;
- les environnements test, preproduction et production emettent du JSON
  structure ; le poste local peut utiliser un rendu texte lisible, construit a
  partir des memes champs ;
- les niveaux nominaux sont `INFO` pour les evenements HTTP et Use Cases,
  `WARNING` pour les anomalies et `ERROR` pour les echecs techniques ;
- `DEBUG` est desactive par defaut en production et n'autorise jamais
  l'exposition de champs interdits ;
- un `User-Agent` est assaini, prive de caracteres de controle et limite a
  512 caracteres ; il ne constitue jamais un identifiant d'utilisateur.

Configuration de reference a introduire :

```env
LOCALEO_LOG_FORMAT=json
LOCALEO_LOG_LEVEL=INFO
LOCALEO_USE_CASES_LOG_LEVEL=INFO
LOCALEO_SQL_LOG_LEVEL=WARNING
LOCALEO_LOG_USER_AGENT_MAX_LENGTH=512
LOCALEO_LOG_SLOW_USE_CASE_MS=2000
LOCALEO_LOG_SCHEMA_VERSION=1
```

### Retention

- developpement local : aucune retention geree par l'application ;
- test : 14 jours ;
- preproduction : 30 jours ;
- production : 90 jours ;
- les audits financiers et de securite restent conserves dans leurs supports
  persistants selon leurs propres politiques ; les logs ne les remplacent pas.

### Seuils de supervision

- un evenement de Use Case est qualifie de lent a partir de 2 000 ms ;
- une alerte de performance est emise lorsque le p95 depasse 1 500 ms pendant
  15 minutes, avec au moins 20 executions dans la fenetre ;
- ces seuils peuvent etre surcharges par Use Case sans modifier le schema ;
- une alerte technique est emise a partir de 3 echecs en 5 minutes ou lorsque
  le taux d'echec technique depasse 5 % sur la fenetre ;
- pour un paiement, reversement, webhook Stripe ou batch critique, le premier
  echec definitif declenche une alerte ;
- une erreur metier n'emet pas d'alerte individuelle ; seule une hausse anormale
  agregee peut declencher une alerte.

### Identifiants et donnees autorises

- la liste blanche transverse autorise notamment `achat_id`,
  `coffret_instance_id`, `commercant_id`, `paiement_id`, `reversement_id`,
  `validation_prestation_id` et `batch_execution_id` ;
- les identifiants Stripe non secrets (`event`, `request`, `payment_intent`,
  `transfer`, `payout` et compte Connect) sont autorises uniquement lorsqu'ils
  sont utiles au diagnostic du flux concerne ;
- chaque domaine peut ajouter un identifiant seulement par un extracteur
  explicite, teste et documente ;
- email, telephone, nom, adresse, IBAN, token, cle API, cookie, QR code,
  header d'autorisation, payload complet et valeurs de query string restent
  interdits.

### Droits de consultation

- les profils exploitation et responsables techniques consultent les logs
  complets assainis ;
- le support dispose d'une recherche limitee par `correlationId` et des champs
  necessaires au diagnostic ;
- finance et produit consultent uniquement des tableaux de bord agreges, sauf
  habilitation d'exploitation explicite ;
- l'administration des acces et leur revue periodique relevent du responsable
  securite ; le principe du moindre privilege s'applique en production.

### Compatibilite et OpenTelemetry

- `correlationId` devient le nom canonique du contrat public ;
- `request_id` reste un alias deprecie jusqu'a une prochaine version majeure de
  l'API et contient strictement la meme valeur ;
- OpenTelemetry n'est pas requis pour le MVP ; les champs optionnels `trace_id`
  et `span_id` sont reserves dans le schema afin de permettre une phase 2 sans
  casser le contrat de logs.

## Validations avant mise en production

Ces validations ne bloquent pas l'implementation :

- confirmer que le forfait Better Stack retenu couvre la region Allemagne, la
  retention de 90 jours, les volumes, les alertes et les droits attendus ;
- faire valider la retention de 90 jours et la liste blanche des identifiants
  par le responsable RGPD/DPO ;
- configurer et recetter le Log Stream Render, les tableaux de bord, les alertes
  et les habilitations avant l'ouverture en production.

## Etat d'implementation au 2026-08-13

Realise dans le backend :

- facade transverse de journalisation dans `app/observability.py` ;
- formatters texte et JSON, schema versionne, contexte `ContextVar`, redaction,
  validation des correlations et normalisation du `User-Agent` ;
- instrumentation automatique, synchrone et asynchrone, de toutes les methodes
  publiques `execute` sous `app.application` ;
- evenements `use_case.started`, `use_case.succeeded`, `use_case.failed` et
  `use_case.slow`, avec invocation parent/enfant et duree ;
- propagation HTTP, batch et webhook Stripe/Stripe Connect ;
- contrat d'erreur additif `correlationId` + alias `request_id`, headers
  `X-Correlation-ID` + `X-Request-ID`, y compris `404`, `422` et exceptions
  FastAPI ;
- contrat OpenAPI des erreurs et variables d'environnement documentees ;
- tests de redaction, format JSON, correlation, isolation async, resilience,
  couverture automatique des Use Cases et erreurs HTTP ajoutes.
- logs explicites du domaine ajoutes sur les invariants des value objects, les
  transitions de reversement et de notifications, ainsi que les decisions de
  consommabilite, Stripe Connect, scopes API et statut public des virements ;
- les erreurs providers, destinataires, tokens et motifs libres restent exclus
  des attributs de logs du domaine.

Restent a finaliser hors implementation backend :

- execution de la suite pytest dans un environnement projet complet ;
- affichage et copie de `Reference erreur` dans les applications clientes ;
- configuration Better Stack/Render, dashboards, alertes, retention et droits ;
- recette de recherche par `correlationId` en environnement partage.

## Definition of Done

- 100 % des Use Cases publics eligibles sont instrumentes automatiquement ;
- chaque invocation emet `started` puis exactement un evenement terminal ;
- les logs synchrones et asynchrones portent un schema stable ;
- `LOCALEO_USE_CASES_LOG_LEVEL` pilote le logger reellement utilise ;
- `request_id`, correlations batch/webhook et invocations imbriquees sont
  propagées ;
- toute erreur 4xx ou 5xx contient un `correlationId` non vide, coherent avec
  les logs et le header de reponse ;
- les interfaces affichent `Reference erreur`, la consigne de communication au
  support et une action de copie de la valeur complete ;
- les points d'entree et l'instrumentation utilisent l'utilitaire transverse et
  ne reconstruisent aucun champ commun de journalisation ;
- le `User-Agent` est assaini et borne, et les identifiants de correlation
  entrants sont valides avant propagation ;
- les secrets et donnees personnelles interdites sont couvertes par des tests ;
- succes, erreurs metier, erreurs techniques et lenteurs sont distinguables ;
- le collecteur, la retention, les droits et les alertes sont configures ;
- la recherche par `request_id` et nom de Use Case est recettee en environnement
  de test ;
- la documentation d'exploitation et le runbook de diagnostic sont publies ;
- aucun comportement metier n'est modifie par l'instrumentation ; le contrat
  d'erreur evolue uniquement de maniere additive avec `correlationId` selon la
  strategie de compatibilite actee.
