# Localeo V40 - Correctif SQLAdmin

Cette version corrige uniquement la configuration SQLAdmin de la V39.

## Correctifs
- suppression de l'usage simultané de `form_columns` et `form_excluded_columns`
- remplacement des relationships dans `column_list` par des colonnes simples `_id`
- conservation des relationships uniquement dans `form_columns` pour les listes de sélection

## Résultat
Les erreurs suivantes ne doivent plus apparaître :
- `Cannot use a column and joined key together`
- `Cannot use form columns and form excluded columns together`
