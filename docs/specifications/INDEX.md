# Spécifications

Mise à jour : **18 septembre 2026**. Les documents sont regroupés par fonctionnalité et EPIC ; les contributions backend et interfaces partagent le même dossier.

Commencer par le README du sujet, puis consulter ses règles, contrats et arbitrages. Les états ci-dessous reprennent le classement de la [roadmap commune](../roadmap/README.md). Les bilans datés et les anciennes tâches à réaliser restent des éléments historiques : ce rangement ne vaut pas nouvelle recette ni nouveau développement.

## Priorités en cours et à cadrer

- **En cours : EPIC 70**, [validation par PIN sur téléphone client](epic-70-validation-pin/README.md), spécification V1 du 5 octobre : droits, contrats, concurrence QR/PIN, notifications et 34 critères reliés aux preuves ; implémentation et tests locaux du 7 octobre, sans déploiement.

- **Terminée : EPIC 66**, [Localeo Atelier](epic-66-localeo-atelier/README.md), V1.2 du 29 septembre 2026 implémentée localement : PWA, prix AUTO/MANUEL et prompt expérience ; 23 critères avec traçabilité, clôture produit confirmée le 1er octobre 2026 ; réserves techniques de livraison dans le bilan.
- **Terminée : EPIC 65**, [vues ERP audit, paiements et reversements](epic-65-vues-erp/README.md), V1.4 clôturée le 2 octobre 2026 ; dix critères vérifiés, droits E69 intégrés ; bilan des tests et configuration de livraison.
- **Terminée : EPIC 69**, [accès ERP et satellites](epic-69-acces-internes/README.md), V1.4 clôturée le 2 octobre après correction CA-18 : scopes globaux, invitation/récupération, Finance et exceptions Backoffice. Les 27 critères sont conservés ; preuves, migration v253 et configuration de livraison dans le bilan, sans déploiement implicite.
- **En cours : EPIC 55**, [moteur commun et chasse au trésor](moteur-animation/README.md).
- **En cours : EPIC 68**, [processus d'onboarding commerçant](epic-68-preparation-onboarding/README.md), V1.2 implémentée localement : sept étapes du référencement à la finalisation ; espace sans dépôt, contrat imprimable avant J, signature jour J et dépôt interne ; confirmation avant chaque séquence mail/SMS. Paramètres validés, guide ERP et supports ; preuves et livraison test suivies dans le bilan.
- **À faire :** [EPIC 54 — Calendrier de l'Avent](epic-54-calendrier-avent-local/README.md) et [EPIC 58 — Filtre annuel](epic-58-filtre-annuel-global/README.md).
- Cadrage encore porté par la roadmap : [EPIC 62 — Validation des modifications de prestations](../roadmap/a-faire/epic-62-validation-modifications-prestations-backlog.md), [EPIC 64 — Rétractation](../roadmap/a-faire/epic-64-parcours-retractation-en-ligne-backlog.md) et [EPIC-MARKETPLACE-54 — Identité visuelle](../roadmap/a-faire/epic-marketplace-54-harmonisation-identite-visuelle-marketplace-backlog.md). Aucun dossier de spécification détaillée supplémentaire n'est créé sans contenu.

## Parcours transverses

| Dossier | Contenu | Applications |
| --- | --- | --- |
| [Installation et mise à jour PWA](installation-mise-a-jour-pwa.md) | Évolution PWA-20260929 : boutons header, aide iOS/Android, mise à jour explicite | Live, Animation, Commerçant, Ops, Atelier, Support, OnBoard |
| [Identité et accès](identite-acces/README.md) | Authentification, sessions, activation, accès aux coffrets | Backend, Animation, Commerçant, Marketplace |
| [Validation des prestations](validation-prestations/README.md) | Scan client, QR et contrats API | Backend, Commerçant, Marketplace |
| [Espace commerçant](espace-commercant/README.md) | Vue fonctionnelle, contrats et [adresse postale](espace-commercant/adresse-postale.md) | Backend, Commerçant, Animation, Onboard |
| [Sécurisation de la production](securisation-production/README.md) | Correctifs d'audit, intégrité, accessibilité et résilience | Backend et trois interfaces |

## Spécifications par EPIC

| EPIC | Dossier | État produit | Applications concernées |
| --- | --- | --- | --- |
| 41 | [Plateforme Animation, actualités et flyers](epic-41-api/README.md) | Terminée | Backend, Animation, Commerçant, Marketplace / Live |
| 42 | [Localeo Live, carnet et inscriptions](epic-42-localeo-live/README.md) | Terminée | Backend, Marketplace / Live |
| 45 | [Vision 360 Animation](epic-45-vision-360-animation/README.md) | Terminée | Backend, Animation |
| 46 | [Paiement des lots](epic-46-paiement-lots-animation/README.md) | Terminée | Backend, Animation |
| 47 | [Abonnement partenaire](epic-47-souscription-abonnement-partenaire-animation/README.md) | Terminée | Backend, Animation |
| 48 | [Ordonnancement des traitements](epic-48-apscheduler-ordonnancement-batchs/README.md) | Terminée | Backend |
| 49 | [Animations publiques](epic-49-animations-marketplace/README.md) | Terminée | Backend, Marketplace |
| 50 | [BUM, facturation et conformité](epic-50-conformite-fiscale-bum/README.md) | Terminée | Backend et trois interfaces |
| 51 | [Vision 360 Achats](epic-51-vision-360-achats/README.md) | Terminée | Backend |
| 52 | [Accueil géolocalisé](epic-52-accueil-marketplace-geolocalise/README.md) | Terminée | Backend, Marketplace |
| 53 | [Tombola et catalogue de modèles](epic-53-tombola-locale/README.md) | Terminée | Backend, Animation, Live |
| 54 | [Calendrier de l’Avent](epic-54-calendrier-avent-local/README.md) | À faire | Backend, Animation, Live |
| 55 | [Moteur commun, DSL et chasse au trésor](moteur-animation/README.md) | En cours | Backend et trois interfaces |
| 56 | [Participation des commerçants](epic-56-validation-participation-commercants-animation/README.md) | Terminée | Backend, Animation, Commerçant |
| 57 | [Catalogues publics et pagination](epic-57-bornage-pagination-api-marketplace/README.md) | Terminée | Backend, Marketplace |
| 58 | [Filtre annuel global](epic-58-filtre-annuel-global/README.md) | À faire | Backend, Animation |
| 59 | [Tests de performance API](epic-59-tests-performance-api/README.md) | Terminée | Backend |
| 60 | [Vision 360 Commercialisation](epic-60-vision-360-commercialisation/README.md) | Terminée | Backend |
| 63 | [Démonstrations communes](epic-63-demonstrations-communes/README.md) | Terminée | Backend et trois interfaces |
| 65 | [Vues ERP audit, paiements et reversements](epic-65-vues-erp/README.md) | Terminée | Backend ERP |
| 66 | [Localeo Atelier — Coffrets assistés par IA](epic-66-localeo-atelier/README.md) | Terminée | Backend ERP/PWA/DAM, Marketplace et contrats partagés |
| 68 | [Préparation et finalisation de l'onboarding](epic-68-preparation-onboarding/README.md) | En cours | Backend ERP/OnBoard, communications, documents, Commerçant |
| 69 | [Profils et accès ERP/satellites](epic-69-acces-internes/README.md) | Terminée | Backend ERP, Support, Atelier, OnBoard, documents et sessions |
| 70 | [Validation par PIN sur téléphone client](epic-70-validation-pin/README.md) | En cours | Backend/ERP, Commerçant, Marketplace/Live ; contrats Animation partagés |

## Contrats et historique

- [OpenAPI Animation — EPIC 41](epic-41-api/openapi.json), [Live — EPIC 42](epic-42-localeo-live/openapi.json) et [Vision 360 Animation — EPIC 45](epic-45-vision-360-animation/openapi.json).
- [Contrat des corrections Marketplace du 6 septembre](corrections-marketplace-2026-09-06.openapi.json), lié à la [spécification consolidée](securisation-production/corrections-marketplace-2026-09-06.md). Les chemins des quatre contrats JSON sont conservés pour leurs consommateurs.
- [Spécifications historiques](archives/README.md), [bilan de consolidation](../organisation/reorganisation-specifications-2026-09-18.md) et [provenance des fichiers](../organisation/reorganisation-specifications-2026-09-18.json).

Pour une évolution, modifier le document canonique et ses arbitrages, mettre à jour les liens et conserver les bilans datés. Les scripts exécutables et générateurs restent dans les applications.
