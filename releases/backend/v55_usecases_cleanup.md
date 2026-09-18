# Localeo V55 - Nettoyage des use cases non référencés

## Objectif
Supprimer les use cases qui ne sont référencés par aucune API afin de réduire le bruit dans le projet.

## Use cases supprimés
- `consulter_detail_coffret_client.py`
- `lister_coffrets_commercants.py`
- `lister_prestations_coffret_client.py`

## Use cases encore référencés par les APIs

### `app/api/clients_api.py`
- `consulter_detail_achat_coffret.py`

### `app/api/commercants_api.py`
- `lister_commercants.py`
- `referencer_commercant.py`
- `regenerer_carte_identite_commercant.py`
- `consulter_historique_prestations_commercant.py`
- `consulter_detail_commercant.py`

### `app/api/coffrets_api.py`
- `lister_coffrets.py`
- `consulter_detail_coffret.py`

### `app/api/paiement_api.py`
- `initialiser_paiement.py`
- `valider_paiement.py`

### `app/api/types_commercants_api.py`
- `lister_types_commercants.py`
- `creer_type_commercant.py`

### `app/api/validation_api.py`
- `ouvrir_transaction_validation.py`
- `valider_prestation.py`

### `app/api/villes_api.py`
- `lister_villes.py`
- `creer_ville.py`
- `consulter_detail_ville.py`

## Nettoyage complémentaire
- suppression des répertoires `__pycache__` pour éviter des faux positifs ou des confusions de chargement au runtime.
