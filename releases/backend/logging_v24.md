# Localeo V24 - Logging

Cette version ajoute un gestionnaire de logs simple pour améliorer l'exploitation et le troubleshooting.

## Ajouts
- `app/logging_config.py`
- logs sur les requêtes HTTP entrantes / sortantes
- logs dans les use cases
- logs dans :
  - `ServiceQr`
  - `PaiementGateway`
  - `ServiceEmail`
  - `bootstrap`

## Variable d'environnement
```env
LOCALEO_LOG_LEVEL=INFO
```

## Exemple de log
```text
2025-03-15 10:00:00 | INFO | localeo.main | Requête entrante GET /villes
```
