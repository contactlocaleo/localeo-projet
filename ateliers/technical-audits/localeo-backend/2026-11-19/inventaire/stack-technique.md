# Stack technique vérifiée

Versions **verrouillées**, pas versions installées ou déployées :

| Bibliothèque | Version | Source |
| --- | --- | --- |
| fastapi | 0.136.0 | [requirements.txt:571](../../../../../../localeo-backend/requirements.txt#L571) |
| starlette | 1.3.1 | [requirements.txt:1616](../../../../../../localeo-backend/requirements.txt#L1616) |
| uvicorn | 0.52.4 | [requirements.txt:1665](../../../../../../localeo-backend/requirements.txt#L1665) |
| sqlalchemy | 2.0.52 | [requirements.txt:1559](../../../../../../localeo-backend/requirements.txt#L1559) |
| psycopg | 3.3.5 | [requirements.txt:1305](../../../../../../localeo-backend/requirements.txt#L1305) |
| pydantic | 2.13.5 | [requirements.txt:1374](../../../../../../localeo-backend/requirements.txt#L1374) |
| sqladmin | 0.29.0 | [requirements.txt:1555](../../../../../../localeo-backend/requirements.txt#L1555) |
| apscheduler | 3.11.3 | [requirements.txt:154](../../../../../../localeo-backend/requirements.txt#L154) |
| requests | 2.34.2 | [requirements.txt:1540](../../../../../../localeo-backend/requirements.txt#L1540) |
| httpx | 0.28.1 | [requirements.txt:803](../../../../../../localeo-backend/requirements.txt#L803) |
| stripe | 14.3.0 | [requirements.txt:1623](../../../../../../localeo-backend/requirements.txt#L1623) |
| boto3 | 1.43.89 | [requirements.txt:215](../../../../../../localeo-backend/requirements.txt#L215) |
| qrcode | 8.2 | [requirements.txt:1532](../../../../../../localeo-backend/requirements.txt#L1532) |
| pillow | 12.3.0 | [requirements.txt:1085](../../../../../../localeo-backend/requirements.txt#L1085) |
| reportlab | 4.5.1 | [requirements.txt:1536](../../../../../../localeo-backend/requirements.txt#L1536) |
| pypdf | 6.18.1 | [requirements.txt:1506](../../../../../../localeo-backend/requirements.txt#L1506) |
| pywebpush | 2.5.0 | [requirements.txt:1528](../../../../../../localeo-backend/requirements.txt#L1528) |

Python : CI sur 3.12 et 3.14 ([.github/workflows/tests.yml:17](../../../../../../localeo-backend/.github/workflows/tests.yml#L17)). Le lanceur local `py -0p` expose Python 3.14 ; sa version exacte est consignée en validation. La version du service déployé n’est pas connue.

Framework FastAPI/Starlette, serveur ASGI Uvicorn : commande de développement `python -m uvicorn app.main:app --reload` dans [README.md:25](../../../../../../localeo-backend/README.md#L25). Aucun serveur WSGI ou Gunicorn n’est établi par les fichiers inspectés. Aucun nombre de workers ASGI effectif n’est établi ; le mode de développement n’est pas une configuration de production.

Les handlers `def` et `async def` coexistent. Le dépôt d’import fait explicitement appel — `run_in_threadpool` après lecture asynchrone bornée du fichier : [app/api/imports_commercants_api.py:258](../../../../../../localeo-backend/app/api/imports_commercants_api.py#L258). Les repositories utilisent des sessions SQLAlchemy synchrones, pas `AsyncSession` : [app/infrastructure/persistence/db.py:44](../../../../../../localeo-backend/app/infrastructure/persistence/db.py#L44). L’audit async devra suivre le chemin réellement exécuté et la version Starlette installée avant toute conclusion.

Transactions : UoW, commit explicite, fermeture systématique, rollback sur exception. Des verrous métier et advisory locks existent, par exemple [app/infrastructure/persistence/repositories/gestion_commercants_animation_repository.py:25](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/gestion_commercants_animation_repository.py#L25). Les migrations SQL sont versionnées sous `sql/` ; leur application réelle n’est pas vérifiée. PostgreSQL est indiqué par les URL normalisées et des requêtes spécifiques ; sa version serveur reste inconnue.

Tâches de fond : APScheduler `BackgroundScheduler`, thread coordinateur, exécuteur de threads, bail de leader en base, `coalesce=True`, `max_instances=1` : [app/infrastructure/scheduler/coordinator.py:110](../../../../../../localeo-backend/app/infrastructure/scheduler/coordinator.py#L110). Les opérations différées métier sont aussi persistées (tirages libres, imports, génération, communications), sans présumer d’un broker Celery/Redis.

Intégrations vérifiées :

| Intégration | Preuve de code |
| --- | --- |
| Brevo email et SMS via requests, délai de 20 s dans ces adaptateurs | [app/infrastructure/email/service_envoi_email.py:47](../../../../../../localeo-backend/app/infrastructure/email/service_envoi_email.py#L47), [app/infrastructure/sms/service_envoi_sms.py:24](../../../../../../localeo-backend/app/infrastructure/sms/service_envoi_sms.py#L24) |
| Stripe Connect, paiements, transferts et webhooks | [app/infrastructure/paiement/stripe_connect_gateway.py:141](../../../../../../localeo-backend/app/infrastructure/paiement/stripe_connect_gateway.py#L141) |
| Stockage local ou S3 via boto3 | [app/infrastructure/storage/document_storage.py:68](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L68) |
| geo.api.gouv, communes et géolocalisation | [app/infrastructure/integrations/geo_api_gouv.py:35](../../../../../../localeo-backend/app/infrastructure/integrations/geo_api_gouv.py#L35) |
| Web push | bibliothèque verrouillée ci-dessus ; assemblage API [app/main.py:578](../../../../../../localeo-backend/app/main.py#L578) |

Cette liste est un inventaire initial des adaptateurs vérifiés ; les fournisseurs supplémentaires des domaines fiscaux, génération et préparation devront être suivis depuis leurs factories par les missions concernées.

Caches : directives HTTP explicites dans le catalogue public (60 s + stale-while-revalidate 300 s) et `private, no-store` sur le dashboard : [app/api/animation_locale_api.py:3870](../../../../../../localeo-backend/app/api/animation_locale_api.py#L3870), [app/api/animation_locale_api.py:3316](../../../../../../localeo-backend/app/api/animation_locale_api.py#L3316). Un middleware de directives existe dans [app/http_cache.py:22](../../../../../../localeo-backend/app/http_cache.py#L22) ; son existence seule ne prouve pas son montage. Des `lru_cache` bornés existent dans [app/infrastructure/persistence/repositories/animation_locale_repositories.py:666](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L666). Aucun cache partagé Redis établi.

Observabilité : logs HTTP corrélés, route normalisée, statut et durée : [app/observability_http.py:29](../../../../../../localeo-backend/app/observability_http.py#L29) ; instrumentation applicative et appels lents : [app/observability_instrumentation.py:41](../../../../../../localeo-backend/app/observability_instrumentation.py#L41) ; santé et supervision scheduler. Aucun tableau de bord APM, export métrique ou relevé réel de saturation n’a été vérifié.

Les `lru_cache` repérés dans `animation_locale_repositories.py` conservent notamment la construction d’instructions SQL ; ils ne prouvent pas un cache de données métier. La présence ou activation d’un cache CDN externe reste inconnue.
