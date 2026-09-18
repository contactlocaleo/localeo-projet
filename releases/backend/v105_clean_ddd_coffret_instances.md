# Localeo V105 - Clean DDD sur Achat / Activation / CoffretInstance

## Objectif
Supprimer les accès directs à la base depuis les APIs et réaligner les endpoints sur des use cases dédiés.

## Endpoints réalignés
### Achat
- `GET /achats/{achat_id}`
- `GET /achats/{achat_id}/coffrets-instances`
- `GET /achats/{achat_id}/coffrets-instances/{coffret_instance_id}`
- `GET /achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`
- `POST /achats/{achat_id}/coffrets-instances/{coffret_instance_id}/activer`
- `POST /achats/{achat_id}/coffrets-instances/{coffret_instance_id}/envoyer-lien-activation`

### Activation
- `GET /activation/{token}`
- `POST /activation/{token}`

## Use cases ajoutés
- `ConsulterCoffretInstanceAchat`
- `ListerPrestationsCoffretInstanceAchat`
- `ActiverCoffretInstanceAchat`
- `EnvoyerLienActivationCoffretInstanceAchat`
- `ConsulterActivationCoffretInstance`
- `ActiverCoffretInstanceParToken`

## Résultat
- plus d'accès direct `SessionLocal()` dans ces APIs
- logique métier déplacée dans les use cases
- APIs réduites à un rôle d'orchestration
