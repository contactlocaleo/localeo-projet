# Localeo V72 - Refactoring conceptuel vers CoffretInstance

Cette version prépare le vocabulaire métier en remplaçant le concept `coffret acheté` par `coffret instance` partout où il apparaissait dans le code et la documentation.

## Principes
- `AchatCoffret` reste la transaction d'achat
- `CoffretInstance` devient le vocabulaire métier pour l'unité consommable
- les concepts dérivés sont renommés, notamment `StatutPrestationCoffretInstance`

## Remplacements principaux
- `StatutPrestationCoffretAchete` -> `StatutPrestationCoffretInstance`
- `StatutPrestationCoffretAcheteValeur` -> `StatutPrestationCoffretInstanceValeur`
- `StatutPrestationCoffretAcheteOrm` -> `StatutPrestationCoffretInstanceOrm`
- `statuts_prestation_coffret_achete` -> `statuts_prestation_coffret_instance`
- `statut_prestation_coffret_achete_id` -> `statut_prestation_coffret_instance_id`
