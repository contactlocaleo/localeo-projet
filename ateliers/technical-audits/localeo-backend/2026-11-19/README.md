# Audit de performance Localeo Backend — archive du 19 novembre 2026

Date locale : 2026-11-19 — Europe/Paris, date du contexte client. Répertoire : `2026-11-19` (suffixe incrémental en cas de doublon).
Statut final : **ARCHIVÉ — dossier de diagnostic et d’arbitrage préparé ; corrections non arbitrées**. L’étape 6 finalise cette exécution, sans en créer une nouvelle. Aucun choix utilisateur reçu sur les huit corrections. Aucun code applicatif modifié ; composants synthétiques mesurés hors réseau à l’étape 4, aucune campagne HTTP/PostgreSQL exécutée. L’archivage n’atteste ni une capacité de production ni une validation produit.

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

## Synthèse et rejouabilité

- [Rapport exécutif](synthese/rapport-executif.md), [roadmap conditionnelle](synthese/roadmap-performance.md), [comparaison historique](synthese/comparaison-precedent.md).
- [Prompt complet d’archivage](prompts/06-archivage.md), [prompt de relance dans une nouvelle exécution](prompts/RELANCER-AUDIT.md).
- [Inventaire et vérification finale](validation/etape-6-verification.md), [contrôles structurés](validation/etape-6-controles.json), [manifeste SHA256 de l’archive](validation/manifest-archive.json), [empreinte du manifeste](validation/manifest-archive.sha256).

Les cinq prompts précédents sont conservés à l’identique et concordent avec les demandes utilisées dans cette conversation ; le sixième archive la demande d’étape 6. Aucun prompt manquant reconstruit. Les rapports, mesures, décisions et contrôles des étapes antérieures restent historiques : leurs statuts décrivent leur date de production. L’index courant est ce README final ; les sous-index antérieurs sont conservés comme preuves de progression.

## Métadonnées finales

| Champ | Valeur / portée |
| --- | --- |
| Date et fuseau | 2026-11-19, Europe/Paris, date locale du contexte client ; pas de conversion depuis une horloge serveur supposée |
| Documentation | main, `f437465c577d3754b8743c6c48519f0d7606613e` ; livrables locaux non committés au moment de l’archivage |
| Backend audité et à l’archivage | main, `7049e7fafc76f9119924f1082a5ee7457a175d85`, checkout suivi propre ; mêmes sources depuis la baseline |
| Consommateurs inspectés selon parcours | Marketplace main `9527ebbfee23f7c5249ce4078c5c3f476da2d924` ; Commerçant main `c61f196774c477065dfc51ebb87fc1a02404329b` ; Animation main `7688f1cea11bec8599bacbfaa512b265c36fed3a` ; aucun modifié |
| Python connu | Poste CPython 3.14.3 64 bits ; CI 3.12/3.14 ; Python déployé inconnu |
| Stack source verrouillée | FastAPI 0.136.0, Starlette 1.3.1, Uvicorn 0.52.4, SQLAlchemy 2.0.52 synchrone, psycopg 3.3.5, PostgreSQL serveur/version inconnus ; SQLAdmin 0.29.0, APScheduler 3.11.3 ; détails dans la stack |
| Versions installées du banc | FastAPI 0.128.8, Starlette 0.50.0, Uvicorn 0.41.0, SQLAlchemy 2.0.48, psycopg 3.3.3, pytest 8.4.2 ; distinctes du verrouillage. FastAPI/Uvicorn non exercés par les composants mesurés |
| Matériel du banc | Windows 11 10.0.26200 ; Intel Core i7-10510U, 4 cœurs / 8 logiques ; RAM physique 17 007 263 744 octets (15,84 Gio), machine partagée |
| Ressources déployées | Workers/réplicas, limites CPU/RAM/conteneurs, pool effectif, configuration proxy et cron non observés. Défaut pool SQL source 5+5 et executor scheduler 4 threads ≠ capacité allouée. Aucun conteneur mesuré |
| Modèles / raisonnement | Orchestrateur Codex, famille GPT-6 déclarée dans le contexte de l’agent ; identifiant exact/variante et niveau de raisonnement non exposés ou non consignés. Modèle exact et effort des six spécialistes, contradicteur et relecteurs : inconnus dans les preuves archivées ; aucune déduction à partir des capacités disponibles |
| Agents réels / voix | Six spécialistes indépendants et un contradicteur indépendant ; revues supplémentaires des mesures, de l’arbitrage et de l’historique. Votes de l’étape 3 simulés explicitement, pas un nouveau scrutin réel ni une autorisation |
| Périmètre | CPU, mémoire, concurrence, persistance, latence API et capacité SRE ; QR, participation, animations/Live, dashboards, commerçants/imports, clôture/tirage/résultats, communications, finance et documents |
| Méthodes | Lecture directe du code et des consommateurs, inventaire AST, contrat de preuve, six analyses indépendantes puis déduplication par cause/flux, contre-expertise, bancs locaux et comparaison documentaire historique |
| Taille de cartographie | 1 329 modules Python parsés ; 1 346 opérations HTTP statiques potentielles après expansion, pas un relevé de trafic ou de déploiement |
| Constats d’origine | 17 majeurs : CPU 2, mémoire 4, concurrence 3, persistance 3, API 3, SRE 2 ; six annexes |
| Problèmes consolidés | 14 problèmes causaux distincts : huit principaux et six pistes/risques annexés, pas 14 incidents mesurés |
| Causes racines | 14 causes candidates RC-01 à RC-14, dont huit retenues dans les corrections proposées ; détail des symptômes et conditions dans causes-racines.md |
| Corrections proposées | Huit : une A conditionnelle, sept B ; aucun C/D dans le plan recommandé |
| Priorités principales | P0 =0 ; P1 =2 (OPT-01, OPT-02) ; P2 =6 ; secondaires P2/P3 dans l’annexe |
| Benchmarks exécutés | M01 : 240 tours de scheduling sur corps ERP extraits et doubles, paliers 1/5/10 ; M02 : simulation SQLite/UTC du bail ; M06 : CSV 1 000/5 000/10 000 lignes, 21 exports chronométrés, neuf profils allocations et cProfile séparé |
| Tentatives conservées | 01/02 échecs de harness, 03 arrêt au seuil CSV après M01/M02 complets, 04 succès CSV réduit ; provenance exacte dans resultats.md |
| Mesures non exécutées | HTTP/PostgreSQL intégrés, M03–M05/M07–M08 et M09–M13 ; cible jetable explicitement désignée absente. Pas de saturation workers/pools ni p50/p95/p99 API qualifiés |
| Gains après correction | NON MESURÉS pour les huit corrections ; bénéfices qualitatifs plausibles, aucun pourcentage ou coût de développement fiable inventé |
| Validations techniques | Rapports et mesures relus, contre-expertise et revues indépendantes favorables sous limites ; contrôles documentaires/intégrité dans les rapports d’étape 6 |
| Validations utilisateur | 0 choix reçus, 8 en attente ; la demande d’étape 6 autorise l’archivage uniquement |
| Exécution / statut final | Aucun patch applicatif, migration, donnée réelle modifiée, installation, commit, push ou déploiement ; archive locale finalisée, aucun gain implémenté |

## Limites de l’archive et conservation

Les bruts et quatre états du harness restent dans `localeo-backend/tmp/performance-stage4-2026-11-19/`, ignorés par Git, avec 14 empreintes dans le manifeste de l’étape 4. Ils sont disponibles et vérifiés localement à l’archivage, **pas inclus dans une archive Git ni garantis par une sauvegarde externe**. Leur suppression empêcherait une reproduction exacte à partir de ce seul dépôt ; le prompt de relance impose de signaler cette limite et de qualifier tout nouveau harness. Aucun script exécutable ou brut déplacé ici.

Tous les fichiers préexistants de cette exécution sont conservés à l’identique, à l’exception de ce README que l’utilisateur demande explicitement de finaliser ; son état avant archivage est conservé dans [readme-avant-archivage.txt](validation/readme-avant-archivage.txt). Aucune autre exécution datée de cette série n’existe ; les anciens audits backend sous docs/audits/backend restent intacts. Les artefacts temporaires antérieurs et les travaux utilisateur hors audit sont préservés.

Le manifeste SHA256 couvre les fichiers du dossier sauf lui-même et son empreinte séparée pour éviter une dépendance circulaire. Toute nouvelle campagne doit utiliser une nouvelle date ou un suffixe ; toute correction de cette archive devra être un addendum traçable dans une nouvelle exécution, jamais une réécriture silencieuse. Cette archive est un dossier vérifiable localement, sans prétention de signature cryptographique ou de dépôt distant déjà effectué.
