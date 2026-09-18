# Localeo V26 - Architecture propre

## Changements
- `ServiceEmail` déplacé vers `app/infrastructure/email/service_email.py`
- exceptions métier ajoutées dans `app/domaine/exceptions.py`
- remplacements ciblés des `ValueError` par des exceptions de domaine
- handlers globaux FastAPI pour convertir les exceptions en réponses HTTP cohérentes

## Statut
- `ServiceQr` : infrastructure
- `PaiementGateway` : infrastructure
- `ServiceEmail` : infrastructure
- exceptions métier : domaine
