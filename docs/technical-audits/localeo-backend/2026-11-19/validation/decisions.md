# Registre d’arbitrage utilisateur

Ouvert le 19 novembre 2026. **Aucune décision reçue. Aucune autorisation de développement enregistrée.** La demande d’étape 5 autorise la préparation de ce dossier et exige d’attendre le choix. Les votes simulés de l’étape 3 ne sont pas des décisions utilisateur. « En attente de choix » ci-dessous décrit un champ vide, pas une sélection implicite d’« À APPROFONDIR » ou de « REPORTÉE ».

## Choix demandés pour les P1

Aucun P0 dans le dossier. Les deux P1 sont indépendants ; le choix de l’un ne vaut pas choix de l’autre.

| ID | Proposition de l’orchestrateur | Preuve et limite | Décision utilisateur | Auteur / date / message |
| --- | --- | --- | --- | --- |
| OPT-01 | A / P1 / S — déporter les quatre batchs ERP | Scheduling local mesuré ; gain après déport et capacité HTTP NON MESURÉS | — En attente de choix | — |
| OPT-02 | B / P1 / M — budget/bail des cycles email/SMS | Code + simulation SQLite/UTC ; aucun double envoi ou dépassement réel de 361 s démontré | — En attente de choix | — |

Fiches prêtes à examiner : [OPT-01](../recommandations/backlog-final.md#opt-01--déporter-les-quatre-batchs-erp-hors-de-la-boucle), [OPT-02](../recommandations/backlog-final.md#opt-02--lier-travail-serveur-réservations-et-durée-de-bail). Les plans de retour arrière et tests y sont explicités. [Plan court](../recommandations/plan-optimisation.md), [mesures et limites](../benchmarks/resultats.md).

L’utilisateur peut choisir, **pour chaque ID** :

- **VALIDÉE** : accord explicite sur la correction et le périmètre de sa fiche ; conserver les conditions éventuelles formulées dans la réponse.
- **REFUSÉE** : ne pas développer cette correction ; conserver la preuve et le motif exprimé, sans effacer le risque.
- **À APPROFONDIR** : conserver les questions et preuves demandées ; aucune implémentation de la correction déduite de ce choix.
- **REPORTÉE** : conserver le risque et, si fourni, l’échéance ou le déclencheur de réexamen ; ne pas inventer de date.

Format de réponse possible : `OPT-01 : <choix> ; OPT-02 : <choix>`, avec conditions facultatives. Aucun choix prérempli. Seule la réponse explicite de l’utilisateur permet de renseigner les cellules correspondantes et de déterminer la suite pour les IDs désignés ; elle ne vaut pas autorisation de déploiement ou de migration.

## P2 sans choix reçu

| ID | Classe / priorité | Décision utilisateur | Auteur / date / conditions |
| --- | --- | --- | --- |
| OPT-03 | B / P2 | — En attente de choix | — |
| OPT-04 | B / P2 | — En attente de choix | — |
| OPT-05 | B / P2 | — En attente de choix | — |
| OPT-06 | B / P2 différable | — En attente de choix | — |
| OPT-07 | B / P2 | — En attente de choix | — |
| OPT-08 | B / P2 | — En attente de choix | — |

Ce registre contient huit candidats, sans statut produit modifié ni ticket créé. Les catégories C/D possibles sont des alternatives hors plan recommandé, pas des décisions de refus au nom de l’utilisateur. Le [backlog final](../recommandations/backlog-final.md) reste la référence des périmètres ; les rapports antérieurs restent historiques.

Après une réponse : enregistrer le choix exact, son auteur/date et ses conditions ; ne pas élargir le périmètre ni déduire une validation des autres lignes. Si la solution exige une rupture, une migration ou un refactoring important non prévu, présenter cette variante à l’arbitrage avant le travail qui en dépend.
