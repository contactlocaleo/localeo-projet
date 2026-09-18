# V37 - Nettoyage complet des noms de paiement

Cette version supprime les suffixes et libellés `Stripe` restants dans les imports, modules et use cases de l'API paiement.

## Noms finaux
- `InitialiserPaiement`
- `ValiderPaiement`
- `PaiementGateway`
- `paiement_events`

## Endpoints
- `POST /paiement/initialiser`
- `POST /paiement/valider`
