# Consolidation des backlogs par état — 18 septembre 2026

Les 23 EPIC des anciens dossiers Animation, Commerçant et Marketplace sont
désormais classées par état. Les variantes d’un même sujet et les compléments
des EPIC 25, 39 et 43 sont réunis dans un seul fichier par EPIC.
Les dossiers applicatifs ne conservent que les plans UX, sprints, tâches et timelines.

## Règles retenues

- Les états du tronc commun numéroté de 1 à 64 sont inchangés : 56 terminées,
  5 à faire, aucune en cours, 2 abandonnées et EPIC 61 fusionnée dans EPIC 60.
- Les paragraphes communs et les différences de typographie sont dédoublonnés.
  Les exigences supplémentaires, tableaux, clauses et références distinctes sont conservés.
- Les anciens états de stories et de lots ne remplacent pas l’état produit commun.
- La divergence historique de l’EPIC 46 sur la clôture et le tirage reste signalée
  dans le backlog unique, avec renvoi au registre PLOT-ARB-16 ; aucune décision métier nouvelle.

## Collisions de numéros et EPIC complémentaires

| Source historique | Destination unique | État et justification |
| --- | --- | --- |
| Marketplace 53 — pagination | [EPIC 57](../roadmap/terminees/epic-57-bornage-pagination-api-marketplace-backlog.md) | Terminée selon le tronc commun ; même sujet que l’EPIC 57, distinct de la tombola 53. |
| Marketplace 18 — Google Analytics | [EPIC-MARKETPLACE-18](../roadmap/terminees/epic-marketplace-18-google-analytics-marketplace-backlog.md) | V1 livrée selon son backlog ; collecte suspendue par MARKET-001. Distinct de la page commerçant immersive 18. |
| Marketplace 54 — identité visuelle | [EPIC-MARKETPLACE-54](../roadmap/a-faire/epic-marketplace-54-harmonisation-identite-visuelle-marketplace-backlog.md) | En cours : implémentation locale livrée, revue et recette connectée attendues selon son backlog. Distinct du calendrier de l’Avent 54, toujours à faire. |
| EPIC-PRES-CONTENU-001 — édition des prestations | [EPIC-PRES-CONTENU-001](../roadmap/terminees/epic-animation-edition-prestations.md) | Parcours d’édition directe déjà présent, confirmé par la spécification de la version actuelle et les constats de l’EPIC 62. Le futur sas reste à faire dans l’EPIC 62. |

Les identifiants préfixés conservent leur provenance applicative sans réattribuer
les numéros du tronc commun. Au total, le suivi réunit 67 identifiants :
58 terminés, 5 à faire, 1 en cours, 2 abandonnés et 1 fusionné.

## Traçabilité

Le [manifeste des fusions](fusions-roadmap-2026-09-18.json) référence les 26
fichiers retirés, leur empreinte avant fusion et leur destination unique.
Le manifeste de migration initial conserve ses sources et empreintes originales ;
ses destinations sont actualisées avec conservation du chemin précédent.
Les liens entrants, index et synthèses sont actualisés. La sauvegarde de travail
antérieure aux fusions reste hors dépôt, dans le répertoire temporaire local.

## Vérifications

- Les 26 sources retirées ont une destination existante. Leurs clauses ont été
  comparées à la sauvegarde avant fusion, en neutralisant typographie, titres et
  anciens statuts : aucune clause non représentée.
- Aucun backlog d'EPIC ne reste dans `animation`, `commercant` ou `marketplace`.
  Aucun numéro d'EPIC commun n'a plusieurs fichiers dans les dossiers d'état.
- Les cinq racines Git restent indépendantes ; toutes les destinations du
  manifeste de migration existent (`scripts/check_workspace.py`).
- Les 109 exports et leurs sources sont inchangés et vérifiés par le synchroniseur
  et par le contrôleur autonome du backend ; aucune resynchronisation nécessaire.
- Le contrôle des liens retrouve les deux références déjà manquantes avant
  intervention vers `localeo-marketplace/api/localeo-openapi.json`, dans
  `docs/specifications/epic-42-localeo-live/frontend-pwa.md` et
  `docs/audits/marketplace/audit-preproduction-2026-09-06.md`. Aucun nouveau lien cassé.
- `git diff --check` passe dans le dépôt transverse et pour le guide Marketplace.

Dépôts modifiés par cette consolidation : `localeo-projet` (documentation) et
`localeo-marketplace` (liens du guide `AGENT.md`). Aucun code applicatif modifié.
