# Conception — Paiement des lots Animation

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-46-paiement-lots-animation.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

> Consolidation documentaire du 18 septembre 2026 : synthèse commune des versions Backend et Animation. Les mentions de livraison ci-dessous sont des constats documentaires datés, pas une recette nouvelle.

## Objet

Ce dossier prépare l'implémentation de la commande professionnelle multi-lots décrite dans [`epic-46-paiement-lots-animation.md`](../../roadmap/terminees/epic-46-paiement-lots-animation.md).

Il remplace le socle par ligne livré par le commit `6455858`. Ce socle garantit déjà le paiement non nul, la confirmation Stripe, la réservation des instances et le blocage de publication ; comme il n'est pas déployé en production, aucune compatibilité de données ni d'API n'est requise lors du passage au checkout unique.

## Statut

- Cadrage technique : réalisé.
- Architecture recommandée : commande d'achat multi-lignes dans `gestion_achats`.
- Arbitrages : les 16 décisions du registre sont validées et intégrées.
- Implémentation backend, selon sa documentation : terminée le 21 août 2026 (commande multi-lignes, checkout Stripe, webhook, réconciliation, publication, tirage, activation, documents et remboursement total).
- Contrat OpenAPI : publié dans le contrat Animation de l'Epic 41.
- Numéro d'Epic : 46 ; l'Epic 42 reste attribuée à Localeo Live.

La copie Animation indiquait encore « prête à démarrer » pour le checkout multi-lots. Cette indication n’établit pas l’état de livraison du frontend ; la présente synthèse conserve la livraison backend documentée et renvoie à la roadmap commune pour le statut global.

## Documents

- [Analyse des écarts](analyse-ecarts.md)
- [Architecture et modèle de données](architecture-modele.md)
- [Contrats API](contrats-api.md)
- [Flux Stripe, concurrence et réconciliation](flux-stripe-reconciliation.md)
- [Procédure d'exploitation `A_RECONCILIER`](../../exploitation/exploitation/reconcilier-commande-lots-animation.md)
- [Plan d'implémentation](plan-implementation.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Décisions structurantes validées

Créer une vraie `CommandeAchat` multi-lignes. Le paiement Stripe est rattaché à cette commande ; chaque ligne confirmée matérialise un `AchatCoffret` enfant et ses instances réservées. Les reversements retrouvent le paiement de commande par une relation persistée, jamais en recopiant une transaction Stripe sur plusieurs paiements ni par recherche heuristique.

Le socle d'initialisation par ligne est retiré sans migration de compatibilité. La fiche Animation donne accès au reçu consolidé et au dossier de facturation. Le tirage attribue tous les lots achetés ; une instance n'est associée qu'à l'envoi irréversible du gain. La séquence exacte clôture/tirage diverge entre les copies, y compris entre ce résumé historique et l’amendement backend du 26 août : voir le [contrat consolidé](contrats-api.md) et le [registre](registre-arbitrages.md), qui conservent cet écart sans créer une nouvelle décision.

## Prérequis résiduels

Aucun arbitrage fonctionnel ou technique du registre ne bloque le démarrage. Avant la mise en production, le découpage documentaire doit être validé par comptabilité/juridique et le plafond monétaire configurable doit être fixé avec finance/risque.

## Livraison backend

- Migration : `sql/v173_epic46_commandes_lots_animation.sql`.
- API partenaire : création, lecture, reprise, annulation et documents sous `commande-lots`.
- API interne : `POST /internal/animation-locale/commandes-lots/reconcilier`.
- Webhooks : `checkout.session.completed`, `checkout.session.expired` et `refund.updated`.
- Exploitation : commandes et lignes consultables en lecture seule dans SQLAdmin.

[Retour à l’index des spécifications](../INDEX.md)
