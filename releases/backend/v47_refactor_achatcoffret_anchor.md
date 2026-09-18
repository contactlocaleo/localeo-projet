# Localeo V47 - Refactoring domaine sur AchatCoffret comme ancre unique

## Renommages
- Coffret prestation commerciale -> Coffret
- Prestation catalogue -> Prestation coffret

## Suppression / remplacement
- suppression du concept `CoffretClient`
- remplacement de `PrestationCoffretClient` par `StatutPrestationCoffretInstance`
- rattachement des statuts de prestations instance à `AchatCoffret`

## Nouveau principe
`AchatCoffret` devient l'ancre unique pour :
- le paiement
- les statuts des prestations instance
- les transactions de validation
- les validations de prestations
