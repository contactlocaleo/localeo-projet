# Localeo V54 - Passe de correction démarrage

Cette version corrige la passe de cohérence interne pour limiter les erreurs de démarrage.

## Corrections principales
- réalignement de `initialiser_paiement.py` sur le nouveau modèle `Coffret`
- réalignement de `lister_coffrets_commercants.py`
- réalignement complet de `repositories_sqlalchemy.py` sur :
  - `CoffretOrm`
  - `PrestationCoffretOrm`
  - `PaiementEventOrm`
  - `StatutPrestationCoffretInstanceOrm`
- correction de l'exception `CoffretCommercantIntrouvable`

## But
Supprimer les références internes cassées aux anciens concepts qui provoquaient des erreurs d'import ou d'attribut au démarrage.
