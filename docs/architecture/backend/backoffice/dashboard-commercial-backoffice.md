# Dashboard commercial du BackOffice

Le dashboard opérationnel propose trois fenêtres : aujourd'hui, sept jours et trente jours. Chaque fenêtre est comparée à la fenêtre immédiatement précédente de même durée. Pour « aujourd'hui », la comparaison porte sur la même durée écoulée la veille.

## Définitions des indicateurs

| Indicateur | Définition |
| --- | --- |
| CA encaissé | Somme en euros des achats `PAYMENT_CONFIRMED` dont la date de paiement appartient à la période. |
| Commandes | Nombre de ces achats payés. |
| Coffrets vendus | Somme des quantités des achats payés ; ce nombre peut être supérieur au nombre de commandes. |
| Panier moyen | CA encaissé divisé par le nombre de commandes. |
| Commission Localeo | Somme des commissions brutes des paiements finalisés. La valeur stockée en centimes est convertie en euros à l'affichage. |
| Coffrets les plus vendus | Classement par quantité vendue, puis par CA. |
| Commerçants les plus actifs | Classement par nombre de prestations validées pendant la période. |

Une période précédente vide produit la mention « Nouveau » et non un pourcentage artificiel.

## Alertes actionnables

- les coffrets actifs arrivant à échéance dans la fenêtre de relance et ayant au moins une prestation restante ouvrent une liste dédiée ;
- les remboursements au statut `ECHEC` ouvrent la liste des remboursements recherchée sur ce statut ;
- les erreurs WebPush commerçants, exploitation et Localeo Live ouvrent chacune leur file avec la recherche `ECHEC` appliquée.

Les cartes sans résultat ne remontent pas dans la zone « À traiter en priorité ». Les alertes critiques sont classées avant les avertissements.
