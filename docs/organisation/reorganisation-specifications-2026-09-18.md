# Réorganisation des spécifications — 18 septembre 2026

Le dossier [spécifications](../specifications/INDEX.md) comporte désormais **24 dossiers fonctionnels ou d'EPIC**, avec un point d'entrée par dossier. Les contributions backend et interfaces sont regroupées autour du même sujet.

## Bilan

- **40 fichiers déplacés**, avec leurs liens entrants et sortants adaptés.
- **19 variantes fusionnées et retirées**, après comparaison des clauses ; les éléments uniques sont conservés dans les sources canoniques.
- **Un parcours obsolète archivé** : l'ancienne validation par deux scans. Le parcours de référence utilise une session commerçant et le QR client.
- **Cinq README créés** pour les accès, la validation, les archives, le moteur commun et la Vision 360 Achats.
- **159 fichiers initiaux → 145 fichiers** ; chaque source est rattachée à une destination dans le [manifeste](reorganisation-specifications-2026-09-18.json).

## Organisation retenue

Les anciens dossiers génériques Animation, Backend, Commerçant et Marketplace sont répartis entre leurs fonctionnalités et EPIC. Les fichiers EPIC 41 isolés à la racine rejoignent `epic-41-api/`, avec les images des flyers. Le parcours géolocalisé rejoint l'EPIC 52 ; les inscriptions multiples et l'email d'achat rejoignent l'EPIC 42.

Les sujets transverses disposent d'entrées [Identité et accès](../specifications/identite-acces/README.md), [Validation des prestations](../specifications/validation-prestations/README.md), [Espace commerçant](../specifications/espace-commercant/README.md) et [Sécurisation de la production](../specifications/securisation-production/README.md). Les identifiants de correctifs sont distingués par leur application et leur audit.

Le moteur commun conserve sa [spécification unique](../specifications/moteur-animation/localeo_animation_engine_spec.md). Les EPIC 62, 64 et Marketplace 54 restent accessibles depuis leur cadrage de roadmap ; aucun nouveau contrat détaillé n'est inventé.

## Consolidations et actualisation

| Périmètre | Traitement |
| --- | --- |
| EPIC 41 — 8 variantes | Compléments ANIM conservés ; états historiques et actualités clarifiés ; formulations contradictoires des flyers réunies avec provenance. |
| EPIC 47 — 2 variantes | Procédure principale conservée avec les correctifs de souscription, invitations et reprise. |
| EPIC 50 — 1 variante | Compléments ANIM-001/006 et restrictions conservés. |
| EPIC 53 — 3 variantes | Catalogue API, formulaire, constantes, erreurs, tests frontend et impacts des arbitrages intégrés. L'hypothèse initiale sans table est remplacée explicitement par le référentiel persistant confirmé par la migration v187. |
| EPIC 58 — 3 variantes | Déduplication sans modifier les décisions encore ouvertes. |
| Correctifs Marketplace et Commerçant — 2 variantes | Contributions backend et frontend réunies ; MARKET-001 à 010 et F01 à F16 conservés. |

Les index et synthèses reflètent les emplacements présents avant cette intervention : **EPIC 55 en cours**, **EPIC-MARKETPLACE-54 à faire**. Aucun de ces backlogs n'est déplacé à nouveau. Les anciens bilans techniques restent datés et ne constituent pas une nouvelle preuve de livraison.

L'exemple de validation QR emploie le corps JSON et Bearer déjà décrits par son contrat. La géolocalisation de l'ancien cadrage d'actualités Live est identifiée comme hors MVP selon LIVE-ARB-31 ; les anciens noms de navigation sont explicités par renvoi à l'EPIC 42.

## Réserves conservées

- **Flyers avant publication :** ARB-22/28/48 présentent encore deux formulations historiques contradictoires. Le [registre EPIC 41](../specifications/epic-41-api/registre-arbitrages.md#divergence-documentaire-sur-les-flyers) les conserve avec référence à ANI-PART-ARB-11. Le remplacement graphique V3 par V4 est distinct de ce conflit.
- **QR d'authentification commerçant :** la description du 7 septembre évoque une carte de secours, alors que l'EPIC 5 est abandonnée. L'écart est visible dans la [vue commerçant](../specifications/espace-commercant/README.md) ; il ne rouvre pas la décision produit.
- **ANO-ANI-02 :** la proposition et son patch sont conservés dans l'EPIC 50, avec leur mention préparé/non appliqué.
- La variante d'architecture EPIC 41, extérieure aux spécifications, reste répertoriée dans les [variantes à harmoniser](variantes-a-harmoniser.md).

## Vérifications et limites

- Les **159 sources** ont une destination existante ; les **19 variantes retirées** étaient identiques à la sauvegarde avant leur suppression.
- Les **quatre contrats JSON**, **deux PNG** et **un patch** sont inchangés par SHA-256. Les chemins des contrats OpenAPI restent stables ; aucun générateur applicatif ne nécessite de déplacement.
- Les **117 sources exportables** sont présentes. Les tests de synchronisation documentaire passent : **15 réussis, un ignoré** (création de liens symboliques indisponible sous Windows).
- Les **145 fichiers sont accessibles depuis l’index**, avec **zéro lien cassé dans les spécifications** après les déplacements. Les vérifications portent sur la documentation et sa synchronisation, pas sur une nouvelle recette fonctionnelle des applications.
- Le contrôle global conserve **10 destinations de migration déjà absentes avant cette tâche**, toutes dans d'anciens documents de planification, ainsi que **trois liens historiques hors spécifications** : notes `envrac`, ancien backlog de validation commerçant et ancien contrat Marketplace cité dans un audit. Ces fichiers n'ont pas été recréés et leurs suppressions antérieures sont préservées.

Le dépôt **localeo-projet** porte la réorganisation, les références et les index. Dans **localeo-backend**, seul `AGENT.md` est actualisé pour les liens de roadmap et les états courants. Aucun code applicatif, script ou configuration d'exécution n'est modifié par cette tâche ; les trois dépôts frontend sont inchangés.

La sauvegarde préalable et les fichiers de travail sont dans `%TEMP%/localeo-specifications-reorganisation-20260918/`. Les chemins sources et leurs empreintes restent consultables dans le manifeste ; les manifestes de migration antérieurs conservent leurs sources et suivent les nouvelles destinations.
