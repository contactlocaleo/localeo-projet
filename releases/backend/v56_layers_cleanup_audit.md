# Localeo V56 - Audit et nettoyage léger des couches internes

## Objectif
Faire une passe prudente sur les couches internes après suppression des use cases non référencés,
sans supprimer agressivement des composants qui restent potentiellement nécessaires au runtime.

## Nettoyage effectué
- suppression des wrappers/use cases legacy encore présents
- suppression des `__pycache__`

## Principe
Les fichiers centraux `models.py`, `mappers.py`, `repositories_sqlalchemy.py` et `sqlalchemy_unit_of_work.py`
sont conservés pour éviter d'introduire de nouvelles régressions de démarrage.

## Couches conservées

- app/infrastructure/persistence/repositories/repositories_sqlalchemy.py
- app/infrastructure/persistence/mappers.py
- app/infrastructure/persistence/models.py
- app/infrastructure/persistence/uow/sqlalchemy_unit_of_work.py

Ces fichiers sont conservés car ils restent centraux pour le runtime, même si certains alias ou concepts hérités peuvent encore être présents.

## Références restantes pour CoffretClient

- aucune

## Références restantes pour PrestationCoffretClient

- aucune

## Références restantes pour CoffretCommercant

- aucune

## Références restantes pour PrestationCatalogue

- aucune

## Références restantes pour coffrets_commercants

- aucune

## Références restantes pour prestations_catalogue

- aucune

