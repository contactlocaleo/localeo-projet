# Configuration et ressources

Valeurs ci-dessous = **défauts du code**, jamais configuration effective. Les fichiers `.env` remplis ne sont ni lus ni copiés.

| Paramètre / ressource | Valeur ou état établi | Source |
| --- | --- | --- |
| Pool principal par engine/processus | size 5, overflow 5, timeout 30 s, recycle 1800 s, pre-ping true | [app/infrastructure/persistence/db.py:33](../../../../../../localeo-backend/app/infrastructure/persistence/db.py#L33) |
| Session ORM | autoflush false, autocommit false, expire_on_commit false | [app/infrastructure/persistence/db.py:44](../../../../../../localeo-backend/app/infrastructure/persistence/db.py#L44) |
| Budget connexion théorique | Avec les seuls défauts : au plus 10 connexions de ce pool par processus ; multiplier par processus/réplicas, puis ajouter outils et autres services. Ceci n’est pas une mesure de connexions ouvertes. | Même source ; nombre de processus inconnu |
| SQL génération / jeu | lock_timeout 3 s ; statement_timeout 15 s, `SET LOCAL` PostgreSQL | [app/infrastructure/animation_locale/composition.py:12](../../../../../../localeo-backend/app/infrastructure/animation_locale/composition.py#L12) |
| SQL exploitation globale | lock_timeout 3 s ; statement_timeout 60 s | [app/infrastructure/animation_locale/composition.py:78](../../../../../../localeo-backend/app/infrastructure/animation_locale/composition.py#L78) |
| Scheduler | désactivé par défaut, timezone UTC, 4 threads d’exécution | [app/config.py:130](../../../../../../localeo-backend/app/config.py#L130), [app/config.py:151](../../../../../../localeo-backend/app/config.py#L151) |
| Bail / renouvellement / poll | 90 s / 30 s / 15 s ; démarrage différé 15 s | [app/config.py:152](../../../../../../localeo-backend/app/config.py#L152) |
| HTTP scheduler | connexion 10 s par défaut ; lecture selon définition du batch | [app/config.py:160](../../../../../../localeo-backend/app/config.py#L160), [app/infrastructure/scheduler/http_client.py:61](../../../../../../localeo-backend/app/infrastructure/scheduler/http_client.py#L61) |
| Import commerçants | taille fichier 2 000 000 octets ; parseur avec budget nominal 5 s ; upload lit MAX_OCTETS+1 | [app/infrastructure/referencement/parseur_imports_commercants.py:13](../../../../../../localeo-backend/app/infrastructure/referencement/parseur_imports_commercants.py#L13), [app/api/imports_commercants_api.py:258](../../../../../../localeo-backend/app/api/imports_commercants_api.py#L258) |
| Catalogue public | page de 20 par défaut, plafond effectif 50 | [app/api/animation_locale_api.py:3886](../../../../../../localeo-backend/app/api/animation_locale_api.py#L3886) |
| Gestion commerçants | limit 25 par défaut, maximum 100 | [app/api/gestion_commercants_animation_api.py:107](../../../../../../localeo-backend/app/api/gestion_commercants_animation_api.py#L107) |
| Appels lents | défaut instrumentation 2000 ms, ajustable par variables nommées dans la source | [app/observability_instrumentation.py:41](../../../../../../localeo-backend/app/observability_instrumentation.py#L41) |
| Workers ASGI / limite threadpool / backlog | non établis pour le déploiement | commande de dev uniquement dans README |
| CPU, RAM, swap, disque, quota I/O | non connus pour le service cible | aucun relevé d’environnement cible fourni |
| PostgreSQL | version, max_connections, RAM, CPU, stockage, statistiques et taille inconnus | pas de connexion ouverte |
| Conteneurs / hébergement | indices Render dans README/config/CI ; aucun Dockerfile, Compose, render.yaml ou Procfile versionné repéré par inventaire Git | absence de manifeste dans le checkout, pas preuve d’absence de conteneur en exploitation |

Configuration chargée par le code : `.env`, puis `.env.local` dans les environnements prévus hors Render ; [app/config.py:1](../../../../../../localeo-backend/app/config.py#L1). Le service n’a pas été démarré. Les flags imports, campagnes, réversibilité et conservation doivent être relevés sous forme expurgée avant toute campagne.

Pour l’étape SRE après autorisation : demander un relevé sans secrets des commandes de démarrage, workers/réplicas, limites CPU/RAM, limites proxy et requêtes, version PostgreSQL, limites de connexion et tâches actives. Les paramètres et budgets seront fixés avant les mesures, sur environnement jetable local isolé. Aucun dimensionnement chiffré recommandé — ce stade.

Le parseur XLSX vérifie aussi au plus 200 entrées ZIP, 20 000 000 octets annoncés au total décompressé et 10 000 000 par entrée/XML (`parseur_imports_commercants.py:62–83`). Ce sont des bornes de code à prendre en compte avant tout constat mémoire.
