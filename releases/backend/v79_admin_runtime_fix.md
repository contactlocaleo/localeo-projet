# Localeo V79 - Fix runtime SQLAdmin

## Problème corrigé
Au démarrage, SQLAdmin échouait sur une référence invalide :

- `StatutPrestationCoffretInstanceOrm.coffret_instance_id`

Après le refactoring vers `CoffretInstance`, cette entité n'est plus reliée directement à `AchatCoffret` mais à :

- `coffret_instance_id`

## Correction appliquée
Dans `app/infrastructure/admin/admin.py` :
- remplacement de `achat_id` par `coffret_instance_id` dans les vues admin concernées
- réalignement de l'affichage admin avec le modèle métier actuel

## Impact
Le démarrage ne doit plus échouer sur cette erreur d'attribut SQLAlchemy côté admin.
