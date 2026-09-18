# Localeo V51 - Correctif imports admin

Cette version corrige des erreurs d'import dans `app/infrastructure/admin/admin.py`
après le refactoring de nommage métier.

## Correctif
- `COFFRET_COMMERCANT_VALIDATORS` -> `COFFRET_VALIDATORS`
- `PRESTATION_CATALOGUE_VALIDATORS` -> `PRESTATION_COFFRET_VALIDATORS`

## Effet attendu
Le démarrage applicatif ne doit plus échouer sur ces imports admin.
