# Localeo V49 - Passe imports et schéma SQL

Cette version corrige la passe finale de cohérence sur la V48.

## Corrections effectuées
- exceptions réalignées (`AchatCoffretIntrouvable`, `CoffretIntrouvable`)
- service QR réaligné sur `AchatCoffret`
- use cases et API de validation réalignés sur `AchatCoffret` et `StatutPrestationCoffretInstance`
- wrappers de compatibilité pour les anciens use cases encore présents
- `DDL/schema.sql` réaligné sur le nouveau modèle :
  - `coffrets`
  - `prestations_coffret`
  - `statuts_prestation_coffret_instance`
  - suppression du schéma `coffret_clients`

## Objectif
Réduire les imports cassés et aligner le schéma SQL avec le refactoring centré sur `AchatCoffret`.
