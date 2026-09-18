# Localeo V82 - API statistiques

## Endpoint ajouté
- `GET /statistiques`

## Données retournées
- `nb_villes_actives_referencees`
- `nb_commercants_actifs_references`
- `nb_coffrets_vendus_aujourdhui`
- `nb_coffrets_vendus_cette_semaine`

## Règles
- les coffrets vendus sont calculés sur les achats avec statut `PAYMENT_CONFIRMED`
- le calcul jour / semaine se base sur `date_paiement`
- les commerçants actifs sont filtrés sur `statut = ACTIF`
