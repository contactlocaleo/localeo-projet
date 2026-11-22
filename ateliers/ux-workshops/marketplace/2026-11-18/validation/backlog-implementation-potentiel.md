# Backlog d'implémentation potentiel — orientations validées, sans exécution

Ce document classe les suites possibles selon les [décisions du propriétaire](decisions.md). **Les sept orientations P0/P1 ont reçu la réponse globale « VALIDÉE » le 18 novembre 2026** ; aucun lot n'est pour autant planifié ou implémenté. Les maquettes sont des références de conception. Les risques à lever figurent dans le [dossier de décision](dossier-decision.md#risques-critiques-et-inconnues-non-résolus).

## Orientations VALIDÉES

| ID | Nature de la suite potentielle | Priorité / effort indicatifs | Dépendance préalable |
| --- | --- | --- | --- |
| O-08 | Préparer une **recette contrôlée**, distincte du code applicatif : innocuité des effets métier, test de redirection, erreur et retour Stripe. | P0 / M | Cadre de test autorisé ; aucun achat ou paiement réel. |
| O-02 | Clarifier sur la fiche la garantie, les exemples et la réservation près du prix. | P1 / M | Promesse canonique, CGV et validation des prestations partenaires. |
| O-01 | Réécrire l'accroche mobile en conservant recherche, coffrets et animations. | P1 / S | Test de compréhension et contrôle à 320/390/430 px. |
| O-03 | Expliquer la réception et l'usage du cadeau avant le formulaire existant. | P1 / S | Vérifier destinataires, chronologie, activation et téléphone. |
| O-05 | Contrôler les contenus réellement publiés puis corriger les fiches nécessaires. | P1 conditionnel / M | Inventaire de l'environnement de lancement et validation commerçants. |
| O-07 | Regrouper prix, validité, réservation et liens juridiques avant le bouton final. | P1 / S | Cohérence CGV ; coordination des textes O-02/O-03. |
| O-06 | Nommer Localeo Live dans les liens et vérifier le retour communal. | P1 / M | Contrat de navigation Marketplace–Live et test de l'inscription réelle. |

Ces lignes sont des **candidats**, non une autorisation de coder, de tester le paiement ou de déployer. O-08 est une porte de vérification, pas une maquette à implémenter.

## Orientations À RÉVISER

Aucune.

## Orientations REPORTÉES

Aucune.

## Orientations REFUSÉES

Aucune.

## Orientations hors de cette décision

O-04 est adoptée au vote simulé mais P2, hors du périmètre visuel et décisionnel de cette étape. O-09 et O-10 sont non retenues au workshop. La réponse globale « VALIDÉE » enregistrée ici ne change pas leurs statuts. Aucun commit applicatif, déploiement, commande ou paiement n'est prévu.
