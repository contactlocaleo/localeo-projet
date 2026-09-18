# Séparation Domaine / ORM – V23

## Domaine
Les objets métier sont dans :
- `app/domaine/modeles.py`

## Contrats repositories
Les interfaces sont dans :
- `app/domaine/repositories/protocols.py`

## ORM SQLAlchemy
Les modèles de persistance sont dans :
- `app/infrastructure/persistence/models.py`

## Mapping
La conversion domaine <-> ORM est dans :
- `app/infrastructure/persistence/mappers.py`

## Conséquence
Les use cases manipulent les objets du domaine, plus directement les classes SQLAlchemy.
