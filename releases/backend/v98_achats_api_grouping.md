# Localeo V98 - Regroupement vers l'API Achats

## Objectif
Regrouper les endpoints liés à la commande et au paiement sous une API métier cohérente : `/achats`.

## Nouveaux endpoints
- `POST /achats`
- `POST /achats/pro`
- `GET /achats/{achat_id}`
- `GET /achats/{achat_id}/coffrets-instances`
- `POST /achats/webhooks/stripe`

## Correspondance avec l'ancien design
- `POST /paiement/initialiser` → `POST /achats`
- `POST /paiement/initialiser-pro` → `POST /achats/pro`
- `GET /clients/achats-coffret/{achat_id}` → `GET /achats/{achat_id}`
- `GET /clients/achats-coffret/{achat_id}/coffrets-instances` → `GET /achats/{achat_id}/coffrets-instances`
- `POST /paiement/valider` → `POST /achats/webhooks/stripe`

## Choix
Le paiement est considéré comme une étape du cycle de vie d'un achat, et non comme une API métier autonome.

## Impact
- API plus lisible côté frontend
- cohérence renforcée autour de la ressource `Achat`
