# V165 - Backend Localeo Live grand public

Cette version livre les lots backend B0 à B8 de l'Epic 42.

## Capacités livrées

- contrat OpenAPI 3.1 dédié et reproductible ;
- passeport coffret protégé par Bearer token ;
- catalogue, inscription et suivi public des animations ;
- actualités éditoriales globales ou ciblées sur le référentiel `villes` existant ;
- installations anonymes, rotation/révocation du secret, préférences WebPush et suivis ;
- inbox persistante, diffusion idempotente, reprises exponentielles et purge ;
- supervision/readiness et écrans Localeo Control ;
- séparation des configurations WebPush Control et Live grand public.

## Migration

Appliquer `sql/v165_epic42_localeo_live_backend.sql` avant d'activer le canal WebPush public.

Les anciennes variables `LOCALEO_WEBPUSH_LIVE_*` sont dépréciées au profit de `LOCALEO_WEBPUSH_CONTROL_*`. Localeo Live grand public utilise uniquement `LOCALEO_WEBPUSH_PUBLIC_LIVE_*`.

## Vérification

- générer le contrat avec `python scripts/documentation/generate_epic42_openapi.py` ;
- consulter `/internal/exploitation/localeo-live/readiness` ;
- garder `LOCALEO_WEBPUSH_PUBLIC_LIVE_ENABLED=false` tant que les deux clés VAPID grand public ne sont pas configurées et recettées.
