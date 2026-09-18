# Localeo V104 - Complément API Achat / Activation

## Endpoints ajoutés sous Achat
- `GET /achats/{achat_id}/coffrets-instances/{coffret_instance_id}`
- `GET /achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`
- `POST /achats/{achat_id}/coffrets-instances/{coffret_instance_id}/activer`
- `POST /achats/{achat_id}/coffrets-instances/{coffret_instance_id}/envoyer-lien-activation`

## Endpoints Activation réintroduits
- `GET /activation/{token}`
- `POST /activation/{token}`

## Objectif
Couvrir complètement :
- le suivi détaillé d'un achat pro
- le pilotage de ses coffret instances
- l'activation bénéficiaire par token
