# Localeo V107 - Observabilité HTTP et erreurs standardisées

## Objectif
Améliorer le socle de production avec :
- un `request_id` corrélable sur chaque appel HTTP
- une journalisation HTTP de base
- des réponses d'erreur standardisées

## Ajouts
- middleware `RequestContextMiddleware`
- header `X-Request-ID` sur toutes les réponses
- inclusion du `request_id` dans les erreurs métier et techniques

## Effets
- débogage plus simple
- meilleure traçabilité en production
- support facilité côté frontend et exploitation

## Fichiers ajoutés
- `app/api/error_models.py`
- `app/observability_http.py`
