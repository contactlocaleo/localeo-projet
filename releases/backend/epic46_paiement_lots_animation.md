# Epic 46 — Paiement des lots Localeo Animation

## Livré

- Commande professionnelle multi-lignes et checkout Stripe unique.
- Confirmation exclusive par webhook, achats enfants et instances réservées idempotentes.
- Reprise des sessions expirées ou en échec et réconciliation locale des projections.
- Publication interdite avant réservation complète des lots.
- Tirage exhaustif : tous les lots achetés doivent être attribués avant la clôture.
- Activation atomique du coffret lors de l'envoi du gain, avec outbox email.
- Paiement de commande résolu depuis chaque achat enfant pour Stripe Connect.
- Reçu consolidé, reçus et factures détaillées téléchargeables depuis l'animation.
- Remboursement total avant publication, y compris suivi asynchrone `refund.updated`.
- Vues SQLAdmin en lecture seule et diagnostic de readiness.

## Déploiement

1. Configurer les trois clés `LOCALEO_ANIMATION_LOTS_*` documentées dans le guide d'exploitation.
2. Appliquer `sql/v173_epic46_commandes_lots_animation.sql` avec `scripts/database/apply_migrations.py`.
3. Vérifier le webhook Stripe et le diagnostic de schéma.
4. Effectuer une recette Stripe Test complète avant activation en production.

Le plafond monétaire et le découpage documentaire doivent être validés par finance/risque et comptabilité/juridique avant le go-live.
