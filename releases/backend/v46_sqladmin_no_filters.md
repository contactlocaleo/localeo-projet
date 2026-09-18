# Localeo V46 - Stabilisation SQLAdmin

Cette version supprime les `column_filters` des vues SQLAdmin pour éviter
les erreurs de compatibilité rencontrées sur certaines versions de SQLAdmin.

## Correctif
- retrait des `column_filters` dans `app/infrastructure/admin/admin.py`

## Effet attendu
Les vues liste de l'admin doivent s'afficher sans l'erreur :
`AttributeError ... has no attribute 'parameter_name'`
