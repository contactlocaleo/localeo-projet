# Stack technique et versions

Sources verrouillées requirements.txt : FastAPI 0.136.0, Starlette 1.3.1, Uvicorn 0.52.4, SQLAlchemy 2.0.52, psycopg 3.3.5, SQLAdmin 0.29.0, APScheduler 3.11.3, boto3 1.43.89. PostgreSQL serveur/version déployée INCONNU.

Python réellement disponible : lanceur py -3.14, CPython 3.14.3 64 bits. La commande python du PATH est un alias Microsoft Store non fonctionnel ; aucun outil installé pour la remplacer. CI annoncée 3.12/3.14. Relevé installé indépendant : [runtime](../validation/runtime.json). FastAPI 0.128.8, Starlette 0.50.0, Uvicorn 0.41.0, SQLAlchemy 2.0.48 et psycopg 3.3.3 diffèrent du verrouillage. Les composants mesurés n'exercent pas ASGI.

Serveur Uvicorn et framework sync/async mixtes : routes jeu Live def synchrones ; les handlers async qui appellent une unité synchrone directement restent sur le thread de boucle. Aucun nombre effectif de workers/réplicas observé. Aucun changement de dépendances.

Modèle exact et effort de raisonnement de l'orchestrateur et des agents : INCONNU, identifiants exacts non exposés ; aucune déduction depuis les noms ou modèles disponibles.
