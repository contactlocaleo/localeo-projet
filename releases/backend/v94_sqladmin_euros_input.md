# Localeo V94 - Saisie SQLAdmin en euros avec conversion automatique

## Objectif
Permettre une saisie humaine en euros dans SQLAdmin, tout en conservant le stockage en centimes en base.

## Portée
- vue `CoffretAdmin`

## Comportement
- dans le formulaire SQLAdmin, le champ `prix` est présenté en euros
- avant persistance, la valeur est automatiquement convertie en centimes
- lors du pré-remplissage d'un coffret existant, la valeur stockée en centimes est reconvertie en euros

## Exemple
- saisie : `49.00`
- stockage : `4900`
- affichage liste : `49.00 € (4900 cts)`

## Choix
Le stockage en centimes est conservé pour rester cohérent avec Stripe et l'ensemble du modèle actuel.
