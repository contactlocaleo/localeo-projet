# Regles de securisation de la mise en production

Ce document complete les specifications techniques et fonctionnelles pour les
correctifs de l'audit du 5 septembre 2026. Les constats historiques restent dans
[docs/audits/2026-09-05-audit-application.md](../../audits/backend/2026-09-05-audit-application.md).

## F02 - Consultation hybride commercant / acheteur

Une session `commercant:validation` exige au moins une prestation de l'instance
appartenant au commercant connecte. La connaissance des identifiants achat et
instance ne suffit pas. Le commercant ne voit que ses prestations et ne recoit
pas l'email du beneficiaire. Le token de gestion de l'acheteur conserve son
perimetre achat ; les controles d'expiration, revocation et rattachement restent
obligatoires. Un commercant sans prestation de l'instance recoit un refus 403.

## Specifications des autres correctifs

- [F03 - Sorties WebPush](f03-webpush.md)
- [F04 - Corps HTTP](f04-corps-http.md)
- [F05 - Limitation et IP](f05-limitation.md)
- [F06 - Checkout durable](f06-checkout-durable.md)
- [F07 - Reprise WebPush](f07-reprise-webpush.md)
- [F08 - Traitements asynchrones](f08-entrees-asynchrones.md)
- [F10 - Quotas publics](f10-endpoints-publics.md)
- [F11 - Lectures groupees](f11-lectures-prestations.md)
- [F12 - Usage des cles API](f12-cles-api.md)
- [F13 - Dependances et CI](f13-validation-reproductible.md)
- [F14 - Retour Checkout](f14-retour-checkout.md)
- [F15 - Acteur d'audit](f15-acteur-audit.md)
- [Verification SAST](sast-complementaire.md)
- [Migrations](migrations.md)

F01 est integre a la specification technique ; F09 au sprint de securite immediate.

## Correctifs complémentaires et interfaces

- [Commerçant F12 — Mesure d'accessibilité du build](accessibilite-commercant.md)
- [Commerçant F13 — Chargement différé du scanner](chargement-initial-commercant.md)
- [Marketplace — Contraste de la confirmation particulier en production](confirmation-contraste-marketplace.md)
- [Animation — Contrats corrigés avant production](contrats-animation.md)
- [Corrections du contre-audit d'integrite](contre-audit-integrite.md)
- [Corrections de l'audit Commerçant](corrections-commercant-2026-09-05.md)
- [Contrats correctifs Marketplace du 6 septembre 2026](corrections-marketplace-2026-09-06.md)
- [Corrections de l'audit d'integrite des donnees](integrite-donnees.md)
- [Marketplace — Sécurisation de l'ouverture en production](ouverture-marketplace.md)

[Retour à l’index des spécifications](../INDEX.md)

Les identifiants Fxx sont locaux à leur audit : F12 Commerçant ne désigne pas le même correctif que F12 Backend. Les préfixes d’application et les dates distinguent leurs sources.
