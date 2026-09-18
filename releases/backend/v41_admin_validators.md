# Localeo V41 - Validateurs SQLAdmin

Cette version ajoute des validateurs de saisie côté SQLAdmin, alignés sur les règles métier de base.

## Fichiers ajoutés ou modifiés
- `app/infrastructure/admin/validators.py`
- `app/infrastructure/admin/admin.py`

## Objets couverts
- Ville
- Type commerçant
- Commerçant
- Coffret commerçant
- Prestation catalogue

## Exemples de règles
- champs obligatoires
- longueurs minimales / maximales
- email optionnel mais valide si saisi
- téléphone optionnel mais valide si saisi
- prix strictement positif
- durée de validité strictement positive
- type de coffret contrôlé
