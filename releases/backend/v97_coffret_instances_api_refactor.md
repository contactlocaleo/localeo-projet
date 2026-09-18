# Localeo V97 - Refactor API CoffretInstance

## Objectif
Regrouper tout le cycle de vie des `CoffretInstance` dans une API cohérente.

## Nouveau point d'entrée
- `/coffrets-instances`

## Endpoints principaux
- `GET /coffrets-instances/{coffret_instance_id}`
- `GET /coffrets-instances?achat_id=...`
- `GET /coffrets-instances/{coffret_instance_id}/prestations`
- `POST /coffrets-instances/{coffret_instance_id}/activer`
- `POST /coffrets-instances/{coffret_instance_id}/envoyer-lien-activation`
- `GET /coffrets-instances/activation/{token}`
- `POST /coffrets-instances/activation/{token}`

## Choix
- le flux QR technique reste dans `/validation/*`
- la lecture métier et le cycle de vie des coffrets sont regroupés sous `/coffrets-instances`

## Impact
- meilleure cohérence API
- simplification côté frontend
- `CoffretInstance` devient le point d'entrée naturel de son cycle de vie
