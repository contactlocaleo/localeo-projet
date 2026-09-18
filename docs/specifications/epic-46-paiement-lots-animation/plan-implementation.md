# Plan d'implémentation

## Principes

- Séparer backend et frontend.
- Livrer par incréments réversibles.
- Remplacer directement le financement Animation par ligne, qui n'est pas déployé en production, sans couche de compatibilité.
- Caractériser les flux existants avant migration.
- Exécuter les tests Stripe Connect et documents avec les tests de paiement, pas comme vérification tardive.

## Backend B0 — Décisions intégrées et tests de caractérisation

- Consigner les 16 arbitrages validés dans l'Epic, les contrats et l'architecture.
- Couvrir le parcours professionnel mono-coffret, le webhook, les documents et la résolution `source_transaction`.
- Figer les contrats OpenAPI et le plan de retrait du socle par ligne.

Sortie : modèle et contrat validés ; aucun point P0 ouvert.

## Backend B1 — Commande multi-lignes

- Ajouter `CommandeAchat` et `LigneCommandeAchat`.
- Ajouter repositories, mappers, UoW et migration additive.
- Calculer les snapshots depuis la configuration et le catalogue.
- Appliquer les limites de 20 lignes, 100 instances, `EUR` et le plafond monétaire configuré.
- Garantir unicité de commande active et idempotence.

Sortie : commande persistée sans appel Stripe, avec tests d'invariants et concurrence.

## Backend B2 — Checkout Stripe unique

- Étendre le port de paiement avec plusieurs `line_items`.
- Configurer les URLs de retour Animation.
- Créer/rejouer la session Stripe et exposer la façade protégée.
- Enregistrer les métadonnées commande sans PII.

Sortie : un seul checkout Stripe Test pour plusieurs coffrets.

## Backend B3 — Webhook et matérialisation

- Résoudre le webhook par `commande_id`.
- Persister le paiement unique.
- Créer idempotemment un achat enfant et les instances par ligne.
- Implémenter `A_RECONCILIER` et le job de réparation locale.

Sortie : une confirmation Stripe produit exactement les achats et instances attendus.

## Backend B4 — Publication et workflow

- Ajouter la projection financière agrégée.
- Exposer actions et incidents avec modèles de réponse dédiés.
- Vérifier la couverture sous transaction lors de la publication.
- Distinguer désactivation commerciale et blocage légal, fraude ou sécurité.
- Retirer la projection et l'initialisation des financements Animation par ligne.

Sortie : aucune animation insuffisamment financée ne peut être publiée.

## Backend B5 — Gain, activation et Stripe Connect

- Réserver l'instance avec verrouillage concurrent.
- Associer gain et instance de façon atomique.
- Résoudre le paiement de commande depuis l'achat enfant pour les reversements.
- Placer la notification gagnant dans l'outbox et rendre la relance idempotente.
- Refuser la clôture tant que chaque lot acheté n'a pas un gain attribué.

Sortie : attribution unique et `source_transaction` disponible pour chaque consommation.

## Backend B6 — Documents, annulation et réconciliation

- Générer le reçu consolidé et les documents détaillés par achat enfant et commerçant.
- Exposer la consultation et le téléchargement audité du dossier de facturation depuis l'animation.
- Implémenter expiration et reprise.
- Implémenter uniquement les annulations/remboursements validés.
- Ajouter vues support, alertes et diagnostics de readiness.

Sortie : incidents exploitables et chaîne documentaire validée.

## Frontend F1 — Récapitulatif

- Afficher lignes, quantités, prix unitaires, sous-totaux et total en centimes formatés.
- Afficher l'identité de facturation et les mentions d'activation différée.
- Ne transmettre aucun montant faisant autorité.

## Frontend F2 — Checkout et retour

- Générer `Idempotency-Key` stable.
- Rediriger vers l'URL retournée.
- Afficher une confirmation en attente et poller la commande.
- Ne jamais conclure au paiement depuis la query string.

## Frontend F3 — Workflow et incidents

- Afficher configuré/payé/réservé/attribué.
- Proposer les seules actions autorisées par le backend.
- Expliquer les états en attente, échec et réconciliation.
- Afficher l'accès au reçu et au dossier de facturation de la commande payée.
- Expliquer le blocage de clôture et le nombre de lots restant à attribuer ; suivre les envois séparément.

## Recette R1 — Intégration

- Un et plusieurs types de coffrets.
- Double clic et appels concurrents.
- Checkout abandonné, expiré, refusé et repris.
- Webhook dupliqué, désordonné et tardif.
- Échec de matérialisation puis réconciliation.
- Publication concurrente à la confirmation.
- Attribution et activation concurrentes.
- Documents et somme des lignes.
- Reversement avec charge de la commande.
- Retrait effectif des endpoints et projections de financement Animation par ligne.
- Clôture refusée si un gain manque, puis acceptée après attribution de tous les lots.

## Go/no-go production

- migrations appliquées et readiness verte ;
- Stripe Test et webhook signés validés ;
- décision comptable/juridique documentée ;
- aucun arbitrage ouvert ;
- runbook de réconciliation et remboursement disponible ;
- tableaux de bord et alertes opérationnels ;
- contrat OpenAPI publié et frontend aligné.
- découpage documentaire validé par comptabilité/juridique et plafond monétaire configuré avec finance/risque.
