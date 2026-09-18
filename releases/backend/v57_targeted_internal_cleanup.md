# Localeo V57 - Nettoyage ciblé des couches internes

Cette version fait une passe fichier par fichier sur les couches internes pour réduire les restes des anciens concepts,
sans supprimer les composants centraux du runtime.

## Fichiers réalignés
- `app/infrastructure/persistence/mappers.py`
- `app/infrastructure/persistence/uow/sqlalchemy_unit_of_work.py`

## Nettoyage complémentaire
- retrait des alias de compatibilité inutiles dans :
  - `app/domaine/modeles.py`
  - `app/infrastructure/persistence/models.py`
  - `app/domaine/exceptions.py`

## Objectif
Garder une base plus propre et plus lisible pour le runtime, avec moins de références héritées.
