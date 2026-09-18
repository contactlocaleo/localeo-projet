# Localeo V81 - Couverture SQLAdmin étendue

## Objectif
Rendre pilotables et visualisables depuis SQLAdmin :
- les `CoffretInstance`
- les objets de reversement
- les comptes bancaires commerçants
- les transactions de validation
- les validations de prestations

## Vues ajoutées / complétées
- `CoffretInstanceAdmin`
- `CompteReversementCommercantAdmin`
- `MouvementReversementAdmin`
- `CompteBancaireCommercantAdmin`
- `ReversementAdmin`
- `LigneReversementAdmin`
- `PaiementReversementAdmin`

## Choix
- les objets calculés / générés métier restent majoritairement en lecture seule
- les comptes bancaires commerçants restent éditables depuis le back-office
- les vues de suivi exposent les identifiants pivots (`coffret_instance_id`, `reversement_id`, etc.)

## Point d'attention
Cette passe améliore la couverture SQLAdmin mais ne remplace pas une vérification runtime complète sur un environnement équipé de toutes les dépendances.
