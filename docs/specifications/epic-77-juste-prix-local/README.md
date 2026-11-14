# E77 — Le Juste Prix Local

Spécification V1 du **13 novembre 2026**. État produit : **En cours**, selon la
[roadmap commune](../../roadmap/README.md). Les huit US et vingt critères
`E77-CA-01` à `E77-CA-20` du
[backlog canonique](../../roadmap/en-cours/epic-77-juste-prix-local-backlog.md)
restent la référence d'acceptation. Implémentation locale dans les quatre applications ; modèle commercial encore inactif. Les preuves et réserves sont consignées dans le bilan de réalisation.

## Résultat attendu

Chaque commerce retenu propose dans Pro un produit précis et son prix TTC.
L'organisateur approuve la proposition, choisit une tolérance commune, un seuil
de commerces réussis et l'exigence éventuelle de passages, puis publie une version
figée. Dans Live, l'habitant confirme une seule estimation par commerce. Une
bonne réponse compte immédiatement, ou après validation commerçante si les
passages sont requis. Atteindre le seuil ouvre une chance au tirage existant.

Le jeu est **inclus dans le forfait standard organisateur**. Aucun achat chez
le commerçant ni paiement habitant n'est nécessaire. Le prix deviné est distinct
de la valeur d'un lot. Les trois dotations existantes sont réutilisées : Coffrets,
lots libres externes ou bons numériques, avec leurs prérequis habituels.

## Documents canoniques

| Document | Contenu |
| --- | --- |
| [Parcours et règles](parcours-regles.md) | Préparation, validation, jeu mobile, confidentialité, incidents et permissions |
| [Architecture et contrats](architecture-contrats.md) | Existant vérifié, propriétaires, API cibles, concurrence, données et compatibilité |
| [Bilan de réalisation](bilan-realisation.md) | Implémentation locale, preuves, réserves et activation séparée |
| [Vérification et livraison](verification-livraison.md) | Matrice des vingt critères, performance, démonstration et ordre de livraison |

Socles : [moteur E55](../moteur-animation/README.md),
[participation E56](../epic-56-validation-participation-commercants-animation/README.md),
[Live E42](../epic-42-localeo-live/README.md),
[offre E73](../epic-73-animation-et-ou-coffrets/README.md),
[PIN E70](../epic-70-validation-pin/README.md),
[salariés E72](../epic-72-acces-salaries/README.md).

## Décisions confirmées le 13 novembre 2026

Les décisions `E77-DEC-01` à `07` restent acquises. Les réponses utilisateur
résolvent les quatre arbitrages du cadrage ; leurs identifiants sont conservés.

| Arbitrage | Décision acquise | Référence |
| --- | --- | --- |
| E77-ARB-01 | Une tolérance en euros commune à toute l'animation | E77-DEC-08 |
| E77-ARB-02 | Trouvé/non trouvé immédiatement ; prix exact révélé après clôture, sans indice plus/moins avant | E77-DEC-09 |
| E77-ARB-03 | Passage avant ou après réponse, tous deux avant clôture. Erreur publiée : suspension pour diagnostic, reprise identique ou annulation puis nouvelle édition corrigée, sans transfert automatique des réponses/chances | E77-DEC-10 |
| E77-ARB-04 | Inclus dans le forfait standard ; pas de module ni quota E75 recopié | E77-DEC-11 |

Les noms techniques, bornes structurelles et budgets cibles ci-dessous sont des
choix de conception, distincts des confirmations produit. Aucun arbitrage métier
bloquant ne reste ouvert pour cette V1. Les lots de réalisation et leurs preuves
sont définis dans le document de vérification. L'ouverture reste conditionnée à
leur implémentation et à la qualification de capacité, sans pilote ajouté comme
condition implicite de clôture.

## Périmètre applicatif

Backend/ERP : règles, droits, préparation, publication, supervision et tirage.
Animation : assistant, approbation et suivi. Pro : proposition du produit et
passages, avec droits salariés conservés. Marketplace : parcours **Live** et
liens d'accès, sans réouverture d'une surface animations dans Coffrets.

Pas d'IA, de classement au plus proche, de plusieurs essais, de correction du
prix publié, d'achat requis ni de nouveau moteur de lots. Le générateur et les
outils exécutables restent dans le backend ; les sources documentaires ici.
