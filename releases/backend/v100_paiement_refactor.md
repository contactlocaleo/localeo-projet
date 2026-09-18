# V100 - Paiement API

## Endpoints

### Initialiser paiement
POST /paiements/initialiser

### Valider paiements (webhook Stripe)
POST /paiements/valider

## Remarques
- L'initialisation est maintenant clairement portée par l'API paiement
- Le webhook Stripe est renommé en "valider"
