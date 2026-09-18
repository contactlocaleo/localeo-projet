# Localeo V77 - Renommage ProtectedAPI vers ReversementAPI

## Objectif
Rendre le nom de l'API plus parlant et aligné avec le domaine métier.

## Modifications
- `app/api/protected_api.py` renommé en `app/api/reversements_api.py`
- import dans `app/main.py` mis à jour
- router renommé en `reversements_router`
- préfixe API renommé en `/reversements`
- tag OpenAPI renommé en `Reversements`

## Résultat
Les endpoints de reversements restent protégés par API key mais portent désormais un nom métier plus clair.
