# Initialisation de l’audit de performance du backend Localeo

Date locale : 2026-11-19 — Europe/Paris, date du contexte client. Répertoire : `2026-11-19` (suffixe incrémental en cas de doublon).
Statut : **étapes 1 à 4 terminées ; étape 5 préparée, arbitrage utilisateur en attente**. Aucun choix utilisateur reçu sur les corrections. Aucun code applicatif modifié ; composants synthétiques mesurés hors réseau à l’étape 4, aucune campagne HTTP/PostgreSQL exécutée.

| Dépôt inspecté | Branche | Commit | état initial |
| --- | --- | --- | --- |
| localeo-projet | main | `f437465c577d3754b8743c6c48519f0d7606613e` | ?? docs/ux-workshops/localeo-crm/ |
| localeo-backend | main | `7049e7fafc76f9119924f1082a5ee7457a175d85` | propre |

Stack vérifiée dans les sources : FastAPI, Starlette, Uvicorn, SQLAlchemy synchrone, psycopg, PostgreSQL, SQLAdmin, APScheduler. Les versions verrouillées et leurs preuves figurent dans [la stack](inventaire/stack-technique.md).
Configuration initiale : inspection statique des sources et exemples versionnés. À l’étape 4, exécution de composants extraits et de domaine via le lanceur isolé, SQLite synthétique en mémoire, aucun dotenv privé, app.main, PostgreSQL ou fournisseur réel. Configuration déployée, CPU et RAM alloués inconnus ; ressources du poste et versions installées distinctes du verrouillage dans le protocole de mesure.

- [Architecture](inventaire/architecture.md), [catalogue API](inventaire/catalogue-api.md), [flux critiques](inventaire/flux-critiques.md).
- [Configuration et ressources](inventaire/configuration-ressources.md), [limites](inventaire/limitations.md).
- [Plan d’orchestration et format commun](inventaire/plan-orchestration-agents.md).
- [Prompt intégral](prompts/01-initialisation.md), [validation](validation/README.md).

`localeo-projet` reçoit les documents ; les harness et sorties de mesure de l’étape 4 restent dans un dossier `tmp/` ignoré du backend. Aucun code applicatif, contrat consommé, critère d’acceptation, migration, paramètre ops ou générateur n’est modifié. Aucun commit, push ni déploiement.
Les références de lignes sont celles du checkout inspecté ; elles ne prouvent pas une version déployée. Les sources applicatives restent dans leur dépôt indépendant.

Étape 2 : [prompt intégral](prompts/02-agents.md). Les destinations demandées sont désormais `agents/01-cpu.md`, `02-memoire.md`, `03-concurrence.md`, `04-persistance.md`, `05-api.md` et `06-sre.md`, avec une annexe séparée par mission. Elles remplacent les noms prévisionnels de l’étape 1. Chaque première analyse reste indépendante ; aucun rapprochement de conclusions n’est effectué avant l’étape 3.

Accès aux [six rapports et annexes](agents/README.md) et à la [vérification de l’étape 2](validation/etape-2-verification.md). Les constats sont étayés par inspection statique ; aucune mesure de saturation ni aucun gain ne sont établis. Les doublons éventuels restent volontairement présents dans leurs missions respectives.

Étape 3 : [prompt](prompts/03-contradiction.md), [consolidation par flux](contradiction/consolidation.md), [causes racines](contradiction/causes-racines.md), [contre-expertise indépendante](contradiction/contre-expertise.md), [débat et votes simulés](contradiction/debats-et-votes.md). Les 17 constats d’origine sont couverts par 14 causes candidates après déduplication et scission des deux mécanismes des médias Live.

Le [backlog préliminaire](recommandations/backlog-preliminaire.md) retient huit orientations : deux P1 et six P2, aucun P0. [Secondaires et remèdes différés](recommandations/annexe-optimisations-secondaires.md), [plan de mesures non exécuté](recommandations/plan-mesures.md), [preuves documentaires de l’étape 3](validation/etape-3-controles.json). Les votes sont une simulation analytique explicite des six perspectives ; aucune nouvelle consultation électorale réelle des spécialistes n’est revendiquée. Le contradicteur n’a pas de voix.

Étape 4 : [prompt](prompts/04-benchmarks.md), [protocole et amendement](benchmarks/protocole.md), [résultats et tentatives](benchmarks/resultats.md), [CPU](benchmarks/profils-cpu.md), [mémoire](benchmarks/profils-memoire.md), [limites](benchmarks/limites.md), [backlog révisé](recommandations/backlog-mesure.md), [vérification](validation/etape-4-verification.md). Scheduling ERP et allocations CSV mesurés localement ; bail reproduit en simulation logique. Trois tentatives échouées/arrêtées conservées, puis succès CSV réduit. Aucune capacité de déploiement ni gain après correction démontré. Huit orientations maintenues, deux P1 et six P2 conditionnels ; cette campagne de mesures n’autorise aucune implémentation.

Étape 5 : [prompt archivé](prompts/05-validation.md), [huit fiches finales](recommandations/backlog-final.md), [quick win proposé](recommandations/quick-wins.md), [plan court](recommandations/plan-optimisation.md), [registre d’arbitrage](validation/decisions.md). Une proposition A conditionnelle (OPT-01), sept B, aucun C/D recommandé ; deux P1 et six P2, aucun P0. Les deux P1 sont soumis séparément au choix VALIDÉE / REFUSÉE / À APPROFONDIR / REPORTÉE. Tous les champs de décision restent vides ; les votes simulés ne constituent aucune autorisation. Aucun nouveau benchmark, patch, migration ou déploiement à cette étape ; gains après correction toujours NON MESURÉS.
