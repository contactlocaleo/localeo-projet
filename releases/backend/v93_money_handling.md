# Localeo V93 - Gestion monétaire clarifiée

## Constat
Le projet stocke les montants en **centimes** (entiers), ce qui est cohérent avec Stripe, mais peut être trompeur dans SQLAdmin où un humain pense souvent en euros.

## Choix conservé
- stockage en base : **centimes**
- intégration Stripe : **centimes**
- affichage SQLAdmin : **euros + rappel de la valeur en centimes**

## Ajouts
- value object `Money` dans `app/domaine/money.py`
- clarification visuelle dans SQLAdmin :
  - `prix` coffret
  - `montant` achat coffret

## Effet
Dans SQLAdmin :
- un montant stocké `1500` s'affiche comme `15.00 € (1500 cts)`
- cela évite l'impression de division par 10 ou 100

## Rappel de saisie
Tant que le schéma SQL reste en entier pour les montants :
- `15 €` doit être saisi comme `1500`
- `49 €` doit être saisi comme `4900`

## Evolution future possible
Si tu veux une saisie humaine en euros dans SQLAdmin, il faudra :
- soit passer les champs en `Numeric(10,2)`
- soit ajouter un champ/formulaire dédié qui convertit automatiquement euros -> centimes
