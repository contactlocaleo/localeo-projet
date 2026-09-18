# Localeo V102 - Nettoyage des use cases

## Objectif
Aligner le nommage des use cases avec le découpage API actuel :
- l'API `achats` ne crée plus d'achat
- l'API `paiements` porte désormais l'entrée de création + initialisation paiement

## Changement appliqué
Ajout d'un use case métier explicite :

- `CreerAchatEtInitialiserPaiement`

Ce use case réutilise l'implémentation existante de `InitialiserPaiement`, mais
avec un nom plus clair et plus cohérent avec le découpage fonctionnel du projet.

## Impact
- pas de changement de comportement
- amélioration de lisibilité
- meilleure cohérence entre API, use cases et domaine
