# Localeo V103 - Renommage endpoint validation

## Changement appliqué
L'endpoint de validation de prestation est renommé pour être plus explicite.

### Avant
- `POST /validation/valider`

### Après
- `POST /validation/valider-prestation`

## Motivation
Éviter toute ambiguïté avec d'autres validations possibles :
- validation paiement
- validation transaction
- validation technique

## Résultat
L'API exprime explicitement qu'elle valide une prestation.
