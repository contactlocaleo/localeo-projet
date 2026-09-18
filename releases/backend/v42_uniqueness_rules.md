# Localeo V42 - Règles d'unicité métier

Cette version ajoute les trois propositions d'unicité métier :

## Contraintes ORM / base
- Ville : unicité sur `(nom, code_postal)`
- Type commerçant : unicité sur `libelle`
- Commerçant : unicité sur `(nom, ville_id)`
- Prestation catalogue : unicité sur `(coffret_id, libelle)`

## SQLAdmin
- validation d'unicité sur les objets administrables
- filtres et recherche ajoutés sur les principales vues admin
- affichage amélioré pour l'exploitation

## Fichiers modifiés
- `app/infrastructure/persistence/models.py`
- `app/infrastructure/admin/validators.py`
- `app/infrastructure/admin/admin.py`
