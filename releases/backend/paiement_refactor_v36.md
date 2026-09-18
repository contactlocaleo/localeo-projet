
# V36 Refactor Paiement

Renommage métier complet :

Use cases :
- InitialiserPaiement
- ValiderPaiement

Routes :
POST /paiement/initialiser
POST /paiement/valider

Objectif :
supprimer le vocabulaire technique (checkout / webhook)
et garder un langage métier cohérent.
