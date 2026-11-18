# Registre des décisions utilisateur — Localeo Animation

Préparé le 2026-11-18T12:38:07+01:00. **État actualisé le 18 novembre 2026 : réalisation autorisée, onze orientations implémentées et poussées ; recette UX à valider.** Mise à jour demandée par l’utilisateur après clarification de la différence entre réalisation et validation du résultat.

Référence : maquettes v2, [dossier des neuf orientations](orientations-a-decider.md), [risques critiques](risques-critiques.md).

La demande ultérieure d’utiliser `localeo-specifier-epic` et `localeo-implementer-epic` a autorisé la réalisation du périmètre cadré. La demande suivante a autorisé commit, push et migrations TEST. **Aucune de ces onze orientations n’attend encore une autorisation de développement.**

La validation du résultat UX reste distincte : elle pourra être **VALIDÉE / REFUSÉE / À RÉVISER / REPORTÉE**, avec commentaire et conditions explicites. Aucun accord de recette n’est déduit des votes simulés, des tests automatisés ou de la présente mise à jour.

| ID | Décision de réalisation — 2026-11-18 | État de réalisation | Recette UX | Référence de la maquette |
| --- | --- | --- | --- | --- |
| A1 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — A1](../visuels/maquettes-apres/A1.html) |
| B1 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — B1](../visuels/maquettes-apres/B1.html) |
| B2 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — B2](../visuels/maquettes-apres/B2.html) |
| B3 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — B3](../visuels/maquettes-apres/B3.html) |
| C1 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — C1](../visuels/maquettes-apres/C1.html) |
| C2 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — C2](../visuels/maquettes-apres/C2.html) |
| D1 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — D1](../visuels/maquettes-apres/D1.html) |
| D2 | AUTORISÉE — direction fonctionnelle VALIDÉE explicitement | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — D2](../visuels/maquettes-apres/D2.html) |
| E1 | AUTORISÉE — demande globale | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | [v2 — E1](../visuels/maquettes-apres/E1.html) |
| F1 | AUTORISÉE — demande globale, P2 | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | Aucune maquette d’étape 3 ; bilan WA-15 |
| G1 | AUTORISÉE — demande globale, P2 | IMPLÉMENTÉE ET POUSSÉE | À VALIDER | Aucune maquette d’étape 3 ; bilan WA-16 |

Condition fonctionnelle D2 : « Consulter le suivi » ouvre le suivi opérationnel ; Bilan reste distinct. Aucun commentaire ni condition individuelle de recette reçu pour les onze orientations. Date de validation de recette : non connue.

## Synthèse

- Réalisation autorisée, implémentée et poussée : **11 orientations** (9 P0/P1, 2 P2).
- Autorisation de développement encore attendue dans ce périmètre : **0**.
- Recette UX : **11 à valider**, aucune validation, révision, report ou refus de recette enregistré.
- D2 conserve en plus sa validation explicite de direction fonctionnelle.
- Base TEST : migrations **324 à 326 appliquées**, contrôle du schéma **READY**. Déploiement effectif des nouvelles interfaces non vérifié.

Preuves : [bilan canonique WA](../../../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#workshop-ux-20261118). Commits poussés : projet `6cb62ed`, backend `5342a77f`, Animation `fe23313`, Pro `93794e4`.

## Historique

Initialisation du registre à réception de l’instruction d’étape 4. Aucun choix, commentaire ou condition attribué à l’utilisateur. Aucune date de validation inventée.

À l’étape 4 initiale, huit orientations étaient en attente et D2 seule validée fonctionnellement. Les demandes ultérieures de spécification, réalisation puis commit/push ont autorisé et conduit à l’implémentation des onze orientations cadrées. Le libellé unique « EN ATTENTE DE DÉCISION » est remplacé par les trois états séparés ci-dessus. Le [backlog](backlog-implementation-potentiel.md) et le README reflètent cet état courant ; les manifestes antérieurs restent des preuves historiques.

## Arbitrage reçu le 18 novembre 2026 — cadrage des suites

À la question explicite opposant la destination Bilan de PO-13 au suivi opérationnel de D2, l’utilisateur répond : « il faut privilégier les retours de l'atelier à l'existant si contrediction ». D2 est donc VALIDÉE sur sa direction fonctionnelle. La primauté s’applique aussi au rejet E2 : clôture automatique future retirée, sans annuler les besoins indépendants de report/rapport. C2 ne contient aucun choix rendant facultatifs les identifiants de création.

La demande d’analyse et de cadrage inscrit les onze orientations adoptées dans le programme de l’[EPIC 73 — E73-EVO-WORKSHOP-UX-20261118](../../../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-ux-20261118). Elle n’est pas convertie en huit accords individuels supplémentaires sur les maquettes. F1/G1 P2 n’avaient pas de maquette d’étape 3. Votes et avis simulés restent inchangés.
