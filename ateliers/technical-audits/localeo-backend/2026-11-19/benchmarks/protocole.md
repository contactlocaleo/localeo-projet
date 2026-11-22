# Protocole de l’étape 4

Autorisation : demande utilisateur « ÉTAPE 4 ». Cible créée pour cette campagne : processus Python local, données synthétiques, réseau et PostgreSQL interdits par `scripts/validation/test_isolated.py`. Aucun serveur applicatif, fournisseur ou fichier dotenv chargé. L’absence de base jetable explicitement désignée et de configuration de déploiement empêche la campagne HTTP/PostgreSQL ; ses scénarios restent **NON EXÉCUTÉS**. Les composants ci-dessous peuvent être étudiés sans cet environnement.

## Conditions et budgets fixés avant exécution

Backend `7049e7fafc76f9119924f1082a5ee7457a175d85`, checkout propre. Windows 11 10.0.26200, Intel Core i7-10510U, 4 cœurs / 8 processeurs logiques, RAM physique 17 007 263 744 octets (15,84 Gio). Python CPython 3.14.3 64 bits. Machine partagée avec les applications de l’opérateur, sans garantie de fréquence CPU ni d’exclusivité.

Versions installées observées : FastAPI 0.128.8, Starlette 0.50.0, SQLAlchemy 2.0.48, psycopg 3.3.3, pytest 8.4.2, python-dotenv 1.0.1, Pillow 12.2.0, Uvicorn 0.41.0. Elles diffèrent du verrouillage inventorié. Aucune installation ni mise à jour. FastAPI/Uvicorn ne sont pas exercés par les mesures ; la différence SQLAlchemy doit être rappelée pour le contrôle SQLite.

Outils retenus : `perf_counter`, `process_time`, `cProfile/pstats`, `tracemalloc`, compteurs Windows du processus via ctypes ; SQLAlchemy et SQLite en mémoire pour la simulation du bail. Les profileurs CPU natifs, k6, py-spy, memray et scalene ne sont pas nécessaires à ces trois essais. Aucun outil supplémentaire installé.

Un seul propriétaire d’exécution : orchestrateur. Aucun port ni base externe. Harness, JSON et profils bruts dans `localeo-backend/tmp/performance-stage4-2026-11-19/`, ignoré par Git ; manifestes expurgés et empreintes dans le dossier documentaire. Les définitions exécutées sont extraites par AST des sources exactes, sans modification de leur corps ; les dépendances remplacées sont explicitement nommées. Ce choix évite d’importer le module ERP et sa configuration. Il ne vaut pas test de routage, middleware ou contrat HTTP.

Seuils d’arrêt préétablis : processus >512 Mio de working set, mémoire physique disponible <1 Gio, campagne >60 s, cas unitaire >3 s ou erreur fonctionnelle inattendue. Contrôles avant/après les cas ; un watchdog demande l’arrêt à 60 s. Une allocation ne peut être interrompue exactement au franchissement mémoire : les petits volumes fixes et l’absence d’images limitent ce risque. Ne jamais ajouter un palier après un arrêt. Ces seuils protègent la machine ; **aucun SLA produit ou seuil d’acceptation de capacité n’est établi**.

## M01 — Frontière async/sync ERP

Exécuter les quatre fonctions `admin_lancer_batch_envoi_emails`, `admin_synchroniser_statuts_emails`, `admin_lancer_batch_envoi_sms`, `admin_synchroniser_statuts_sms` dans un event loop asyncio local. Conserver leurs corps, retirer uniquement les décorateurs de route. Doubles : identité opérateur, redirection, BatchRunner relayant `handler`, UoW non utilisée et services/batchs retournant des compteurs après une attente synchrone de 10 ms par appel. Aucun vrai envoi.

Email/envoi : 1, 5 puis 10 coroutines batch simultanément mises en file, avec une coroutine témoin prête juste après ; 20 répétitions par palier, même témoin sans attente fournisseur en contrôle. Les trois autres handlers sont vérifiés au palier 1, 20 répétitions. Aucun palier 25/50/100 sur ce banc : il amplifierait une attente injectée sans améliorer la preuve. Mesurer attente de la coroutine témoin depuis sa mise en file, durée de tour, CPU processus et erreurs. Percentiles par rang supérieur (`ceil(p*n)-1`), sans interpolation. À 20 échantillons, p99 = maximum observé, peu robuste.

Critère structurel : le témoin prêt doit pouvoir progresser pendant l’attente si un déport existe déjà. Son report à la fin des attentes synchrones confirme le défaut local ; aucun percentile HTTP, débit d’utilisateurs ou impact interprocessus n’en découle. Pas de prototype de correction : **gain après déport NON MESURÉ**. À réaliser après correction autorisée : même jeu avec déport de toute l’unité synchrone, vérification acteur/corrélation/réponse/erreurs et limites threadpool/SQL.

## M02 — Durée du bail et travail serveur

Exécuter la classe `BatchRunner`, ses convertisseurs d’exécution et la définition catalogue `emails.envoyer` issus de l’AST. Domaine `ExecutionBatch` réel ; tables ORM minimales SQLite en mémoire pour les seuls attributs utilisés. Sessions réelles SQLAlchemy, opérations DELETE/INSERT/COMMIT réelles SQLite. Corrélation locale sans réseau. Aucun modèle ou schéma applicatif durable créé.

Horloge logique initiale fixe, avant expiration à +359 s puis après à +361 s pour le bail source timeout 300 +60. Dans le handler du premier runner encore actif, tenter un second lancement avant et après expiration. Relever rejet/acceptation, nombre maximal de handlers présents dans la pile, états finaux et nettoyage. Les 361 secondes sont une **avance d’horloge simulée**, pas une durée de traitement ou de latence mesurée. Exécutions imbriquées dans un thread, pas deux workers PostgreSQL.

Critère structurel : second lancement refusé avant expiration, accepté après alors que le premier handler n’est pas revenu ; le timeout ne stoppe donc pas ce handler dans ce modèle. Ne pas conclure à un double envoi ni à la sécurité des verrous PostgreSQL. Aucune réservation d’email ni rupture client réellement exercée. Mesure avant/après encore nécessaire : PostgreSQL jetable, deux lanceurs, >100 messages synthétiques, fournisseur lent/erreur/accepté puis crash, réservation progressive, reprise et révocation. Gains de capacité et de délai **NON MESURÉS**.

## M06 — CSV paiements

Exécuter directement le module source `export_financier.py` (imports stdlib uniquement) et sa fonction `produire_csv`, colonnes finance réelles. Générateur synthétique de lignes ASCII à 11 colonnes, identifiants de longueur fixe ; aucune liste globale en entrée. Volumes initialement prévus : 1 000, 10 000, 50 000 lignes, concurrence 1. Un échauffement par volume, sept répétitions temporelles sans profileur, trois répétitions allocations distinctes avec tracemalloc ; cProfile séparé. Vérifier BOM, nombre de lignes et empreinte identique entre répétitions.

**Amendement avant la tentative 04 :** la tentative 03 a arrêté le profilage CSV sur un cas de 4,315 s dépassant le seuil de 3 s. Aucun seuil relevé, aucun palier supérieur ajouté. Nouvelle campagne réduite, CSV seul : 1 000, 5 000, 10 000 lignes ; cProfile à 10 000. Les résultats M01/M02 de la tentative 03 restent conservés et ne sont pas rejoués. La tentative 03 ne conserve pas les mesures intermédiaires CSV : elles ne seront pas utilisées. Le volume précis du cas interrompu n’était pas journalisé et ne sera pas déduit comme une mesure.

Mesures : durée, CPU processus, débit de **lignes CSV/s**, taille de la chaîne encodée, allocations Python courantes/pic, working set avant/après et maximum historique du processus. Les instantanés RSS ne sont pas un pic par export ; le maximum Windows est cumulatif. La projection SQL, ses pages, l’encodage HTTP et le client lent ne sont pas exercés. p50/p95/p99 de sept exports décrivent seulement ces échantillons ; p95/p99 = maximum, aucune prétention à une distribution stable.

Critère structurel : pic Python et chaîne retournée croissent avec la sortie malgré entrée génératrice. Ne pas déduire d’OOM ou de fuite. Aucun spool implémenté ; gain mémoire/latence après correction **NON MESURÉ**. Après correction autorisée : mêmes octets/BOM/formules/ordre, projection fermée avant réponse, mémoire et disque bornés, erreurs/abandon/nettoyage, deux exports simultanés.

## Campagne intégrée préparée, non exécutée

M03 relances, M04 Live/statistiques, M05 expiration, M07 médias et M08 Stripe restent définis dans le [plan de mesures](../recommandations/plan-mesures.md). Ne pas remplacer PostgreSQL par SQLite pour leurs plans, verrous, transactions ou capacité. M09–M13 restent secondaires.

Sur une future cible jetable explicitement désignée : relever workers, pool, limites CPU/RAM et proxy ; fournisseurs locaux doubles ; seed synthétique déterministe N/10N et distribution tenants ; paliers 1 puis 10, au plus 25 si les budgets préalables le permettent. Ne pas lancer 50/100 par défaut. Échauffement 30 s puis observation 60 s par palier, repos jusqu’au retour des ressources, trois répétitions ; plafond de campagne 15 min. Fixer avec ops les limites propres à la cible avant lancement. Proposition d’arrêt conservatrice à valider : RSS >70 % de la limite cible, mémoire disponible <20 %, CPU >80 % sur 10 s, erreurs >1 % sur 100 requêtes, p99 >2 s sur 100 requêtes ou attente pool >1 s. Ces chiffres sont des garde-fous proposés, pas des SLA acceptés ni des résultats. Collecter p50/p95/p99, req/s, erreurs, CPU/requête, RSS, SQL/temps/rows, checkout/pool/locks, âge de file et saturation workers. Comparer avant/après à mêmes ressources, jeu et versions, sans cumul artificiel des gains.
