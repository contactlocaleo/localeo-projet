# Specifications techniques API - EPIC 41 Animation locale

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

> Consolidation documentaire du 18 septembre 2026 : contributions Backend et Animation réunies. Les écarts sur les aperçus de flyers restent exposés dans le [registre commun](registre-arbitrages.md#divergence-documentaire-sur-les-flyers), sans nouvelle décision produit.

## Objet

Ce dossier porte les contrats techniques des APIs necessaires a la plateforme Localeo Animation. Il devient le point d'entree des travaux de specification API de l'EPIC 41.

La source UX courante est la [maquette V2](../../../livrables/design/animation/localeo-animation-maquette-v2.zip).

## État documentaire et applications concernées

L’EPIC 41 est classée terminée dans la [roadmap commune](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md). Le backend porte les règles et contrats ; Localeo Animation présente le portail partenaire, Localeo Commerçant les parcours terrain, et la Marketplace héberge Localeo Live. Les états de lots et prérequis ci-dessous sont des constats historiques ; leur conservation ne rouvre pas l’EPIC. La checklist s’applique à chaque livraison.

## Historique d’implémentation au 28 août 2026

- Le code du Lot 0 est implemente : entites de socle Animation, configuration versionnee, operations asynchrones, idempotence, erreurs, permissions, repositories SQLAlchemy, unite de travail et migration `v156`. La suite `pytest` doit etre rejouee dans un environnement Python compatible avant integration.
- Le domaine `abonnements_plateforme` et son port de verification sont reserves ; ses entites et use cases metier appartiennent au Lot 2.
- Le Lot 1 est implemente : partenaires, gestionnaires, habilitations persistantes, sessions Animation de huit heures, changement de commune active et controle tenant. Les cinq routes de session et contexte du Lot 1 sont enregistrees dans `app/main.py`.
- Le Lot 2 est implemente : offres, abonnements par partenaire/commune, droits effectifs, activation administrative auditee, continuite apres expiration, projection portail et registre idempotent des evenements Stripe. Le raccordement Billing au webhook Stripe sera active avec les secrets de test.
- L'`Epic 47 — Souscription et paiement de l'abonnement partenaire Animation`
  porte désormais l'évolution commerciale de ce socle : prix catalogue et
  négocié, gratuité, Checkout Stripe, activation après paiement et remontée des
  abonnements encaissés dans le suivi du CA.
- Les routes publiques, protegees et internes des lots backend de l'Epic 41 sont implementees : catalogue, inscriptions, validations, publication, flyer, pilotage, tirages, gains, bilans, supervision, actualites et commandes de lots.
- La synchronisation avec l'Epic 56 est implementee par la migration `v182` : demandes de participation commercant versionnees, diffusion email/inbox/WebPush, decision authentifiee, snapshot des participants a la publication, controle d'eligibilite des lots et acces commercant au flyer publie.
- Le tag OpenAPI `Animation locale` est deja declare.
- Les domaines `referencement`, `commercialisation`, `gestion_achats`, `documentaire`, `dam`, `exploitation`, `support` et `identite_acces` fournissent des briques reutilisables.

## Documents du dossier

- [Catalogue des APIs](catalogue-api.md) : inventaire classe en APIs a reutiliser, a faire evoluer et a implementer.
- [Conventions et contrats communs](conventions-contrats.md) : exposition, authentification, tenant, pagination, erreurs, idempotence et traitements asynchrones.
- [Registre des arbitrages](registre-arbitrages.md) : decisions `ARB-01` a `ARB-69`, criteres de recette et de production, et formulations sources contradictoires des flyers.
- [Contrat OpenAPI implémenté](openapi.json) : contrat généré hors ligne depuis le code backend le 18 septembre 2026. Il remplace les anciens instantanés cible et de test ; il décrit les routes et méthodes réellement implémentées, avec les annotations utiles à la maquette. Cette génération ne prouve pas que le même code est déjà déployé.
- [Rapport Figma des APIs manquantes](rapport-apis-manquantes.md) : retour du branchement mock et reconciliation avec les chemins canoniques Localeo.

## Documents amont

- [Backlog EPIC 41](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md)
- [Analyse API de la maquette V2](analyse-api-maquette.md)
- [DCT EPIC 41](dct.md)
- [Spécification des évolutions de l’application commerçant](application-commercant.md)
- [Architecture EPIC 41](../../architecture/backend/epics/epic-41-animation-locale-architecture.md)
- [Conventions API et OpenAPI](../../architecture/transverse/conventions-api-openapi.md)

## Spécifications fonctionnelles associées

- [Actualités : règles transverses](actualites.md), [pilotage partenaire](actualites-interface-animation.md) et [lecture dans Localeo Live](actualites-localeo-live.md).
- [Direction artistique et cycle de vie des flyers](flyer-direction-artistique.md).
- [Indicateurs économiques et d’usage des gains](indicateurs-economiques.md).

## Classement utilisé lors du cadrage

Chaque besoin est classe dans une seule categorie :

- `REUTILISER` : contrat existant consommable sans modification par le parcours cible ;
- `FAIRE_EVOLUER` : route ou capacite existante a etendre, sans deplacer la propriete metier vers `animation_locale` ;
- `IMPLEMENTER` : contrat specifique au domaine `animation_locale`, absent du backend.

La reutilisation d'un service ou repository existant ne signifie pas que le portail doit appeler directement son API publique. Par exemple, l'assistant de creation utilise les donnees de referencement et de commercialisation, mais passe par des projections d'eligibilite protegees appartenant a `animation_locale`.

## Prérequis consignés pour la livraison initiale

Le bilan historique annonçait le scope backend implémenté et demandait d’appliquer `v182`, de configurer `LOCALEO_FRONT_COMMERCANT_ANIMATION_INVITATION_URL_TEMPLATE`, de raccorder les écrans Animation et Commerçant, puis d’exécuter la recette de bout en bout et la checklist. Pour une livraison actuelle, vérifier ces points sur l’environnement cible ; cette liste historique ne constitue pas une preuve de déploiement ni un nouveau backlog.

## Documents complémentaires du dossier

- [Epic 41 - Checklist de mise en production](checklist-mise-en-production.md)

[Retour à l’index des spécifications](../INDEX.md)
