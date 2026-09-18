# Analyse des écarts

## Synthèse

Le socle actuel sécurise le financement d'une ligne de lot avec le parcours d'achat professionnel. La cible de l'Epic ajoute une notion différente : une commande unique contenant plusieurs coffrets et payée par une seule transaction Stripe.

| Capacité | État actuel (`6455858`) | Cible Epic | Écart |
|---|---|---|---|
| Montant du lot | Prix catalogue × quantité | Identique | Couvert |
| Type d'achat | `PROFESSIONNEL` | Identique | Couvert |
| Checkout | Un par ligne de lot | Un pour toutes les lignes | Structurant |
| Paiement | Rattaché à un `AchatCoffret` | Rattaché à la commande | Structurant |
| Webhook | Crée les instances d'un seul coffret | Matérialise toutes les lignes | Structurant |
| Réservation | Déduite des achats `LOT_ANIMATION` et instances en attente | Suivie par commande et ligne | À expliciter |
| Publication | Bloquée sans achat, paiement et instances | Bloquée sans commande complètement couverte | Partiellement couvert |
| Gain | Active une instance prépayée | Identique, avec réservation concurrente robuste | Partiellement couvert |
| Facturation | Documents par achat mono-coffret | Reçu consolidé + détails par achat enfant proposés | Non couvert |
| Stripe Connect | Paiement retrouvé par `achat_id` | Paiement de commande retrouvé depuis chaque achat enfant | Non couvert |
| Reprise/expiration | Reprise par ligne | Reprise globale de commande | Non couvert |
| Remboursement | Parcours achat/instance existant | Politique commande multi-lots | Non couvert |
| Workflow | Actions `PAYER_LOT` par ligne | Sous-workflow financier agrégé | Non couvert |
| Bascule | Façade par ligne non déployée | Remplacement direct par la commande consolidée | Suppression à prévoir |

## Contraintes héritées

### Achat mono-coffret

`AchatCoffret` porte directement `coffret_id`, `quantite`, `montant` et les relations vers paiement, instances, documents et remboursements. Il ne peut pas représenter proprement plusieurs types de coffrets.

### Paiement mono-achat

`Paiement.achat_id` est obligatoire et `transaction_id` est unique. Créer un paiement par achat enfant avec la même transaction Stripe violerait l'unicité et donnerait une fausse représentation financière.

### Documents d'achat

Le snapshot documentaire et les factures sont construits à partir d'un achat. Une transaction consolidée impose de distinguer :

- la preuve du débit global remise au partenaire ;
- les achats enfants utilisés pour les prestations, documents détaillés et reversements ;
- les éventuels avoirs ou remboursements.

### Stripe Connect

Le transfert commerçant résout actuellement la charge Stripe depuis le paiement de l'achat d'origine ou le `transfer_group` `achat:{achat_id}`. Avec une commande multi-lignes, chaque achat enfant doit résoudre explicitement le même paiement de commande et la même charge, tout en conservant une clé d'idempotence propre au mouvement.

## Risques si la conception n'est pas corrigée

1. Double comptabilisation d'une transaction Stripe sur plusieurs achats.
2. Reversement impossible faute de `source_transaction` résolue depuis l'achat enfant.
3. Remboursement d'un achat enfant alors que Stripe a débité une commande globale.
4. Reçu ou facture dont le total ne correspond pas au débit Stripe.
5. Création partielle d'instances après webhook sans état de réconciliation fiable.
6. Double débit lors d'une reprise concurrente ou d'un webhook tardif.
7. Publication autorisée à partir d'une somme globale sans couverture par coffret.

## Recommandation

Créer une racine de commande multi-lignes plutôt que d'étendre `AchatCoffret` avec une collection optionnelle. Cela préserve le parcours Marketplace mono-coffret et rend visibles les invariants propres à la commande Animation.

L'API Animation reste la façade tenant-aware. `gestion_achats` possède la commande, le paiement et les achats enfants. Stripe reste un adaptateur d'infrastructure.

Le financement Animation par ligne n'étant pas en production, la migration ne reprend aucune commande, session ou paiement `LOT_ANIMATION` existant. Les endpoints d'écriture et projections spécifiques à ce mode sont remplacés, et les données locales de développement sont réinitialisées par une procédure explicitement limitée aux tables concernées.
