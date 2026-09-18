# Localeo V106 - Stabilisation runtime repositories

## Objectif
Remplacer l'ajout dynamique de méthode repository par une implémentation explicite et stable.

## Problème traité
Dans la V105, la méthode `obtenir_par_token_activation` était injectée dynamiquement dans le repository SQLAlchemy des `CoffretInstance`.
Cette approche compilait, mais restait fragile au runtime et moins lisible.

## Correction
- suppression du monkey-patch dynamique
- ajout d'une vraie méthode `obtenir_par_token_activation()` dans `CoffretInstanceRepositorySqlAlchemy`
- alignement du protocole `CoffretInstanceRepository`

## Effet
Les use cases d'activation et de consultation par token s'appuient désormais sur un repository explicite, plus robuste et mieux aligné avec le design DDD.
