# Limites des mesures

Aucun HTTP/PostgreSQL intégré exécuté, aucune cible jetable explicitement désignée. Pas d'app.main, dotenv privé, fournisseur ou données réelles. Le lanceur neutralise bootstrap/scheduler/dotenv/réseau/psycopg. SQLite mémoire est créé seulement par M02.

Versions installées distinctes du verrouillage. Machine partagée, cocharge/énergie/fréquence/caches non stabilisés : timings versus référence NON COMPARABLES pour attribuer une tendance ou un gain, malgré mêmes sources/scénarios. Allocations CSV mêmes octets identiques descriptivement ; pas une capacité globale.

M01 utilise AST et doubles injectant 10 ms, ne valide ni routage/ASGI/auth/middleware/UoW réels. M02 : mappings minimaux, deux callbacks imbriqués, pas deux workers PostgreSQL ; +361 s logique. Remises, réservations et effets non exercés.

M06 inclut générateur synthétique dans temps/CPU ; encodage de vérification hors fenêtre allocations, SQL/client lent absents. p95/p99 sur 7 =max ; p99 sur 20 =max. tracemalloc couvre Python, pas natif ; snapshots=retenu, pas churn total. Working set ponctuel et maximum cumulatif séparés.

M-LIVE-01 : tuple/UUID préexistants, transitoires seulement ; assertions d'appartenance du harness ajoutent du CPU linéaire. Plateau des pics à5k/10k, aucune pente constante démontrée. Double Random déterministe, pas coût/qualité de l'aléatoire sûr. Le tirage complet et ses invariants ne sont pas validés.

Aucune correction ou variante optimisée : gain après correction NON MESURÉ. Aucun SLA, nombre d'utilisateurs, fuite/OOM ou saturation qualifié. Les budgets protègent le poste.

Bruts/harness/outils ignorés hors archive Git : empreintes locales vérifiées, sauvegarde distante non garantie. Trois tests composants réussis ne sont pas une recette métier ou contrat complète.
