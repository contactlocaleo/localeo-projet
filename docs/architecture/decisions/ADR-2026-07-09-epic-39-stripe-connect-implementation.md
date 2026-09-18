# ADR-2026-07-09 - Decisions d'implementation EPIC 39 Stripe Connect

## Statut

Acceptee.

## Contexte

L'EPIC 39 remplace les flux historiques de reversement manuel par une
delegation des paiements et reversements a Stripe Connect.

Les choix produit deja actes sont :

- PSP cible : Stripe Connect ;
- type de compte Connect cible : Express ;
- modele financier : `separate charges and transfers` ;
- pilotage Localeo des campagnes de transfer le 1er et le 15 a 22h00 ;
- absence de fallback bancaire manuel ;
- conservation des objets internes comme projections metier et back-office.

Il restait a acter les recommandations d'implementation pour eviter une
integration trop diffuse : configuration cible, garde-fous de mise en
production, statut metier des mouvements, strategie de migration et ordre des
lots techniques.

Ce document ne constitue pas un avis juridique. La mise en production reste
conditionnee a la validation du dossier de conformite PSP.

## Decision

### 1. Configuration et activation

L'integration Stripe Connect est activee par environnement et protegee par un
feature flag :

- `LOCALEO_FEATURE_STRIPE_CONNECT_ENABLED`

Les variables de configuration cibles sont :

- `LOCALEO_STRIPE_SECRET_KEY` ;
- `LOCALEO_STRIPE_WEBHOOK_SECRET` ;
- `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET` ;
- `LOCALEO_STRIPE_ONBOARDING_RETURN_URL` ;
- `LOCALEO_STRIPE_ONBOARDING_REFRESH_URL`.

Les destinations webhook sont separees par source :

- `POST /public/stripe/webhook` recoit les evenements du compte plateforme
  (paiements, charges, remboursements et transfers) et utilise
  `LOCALEO_STRIPE_WEBHOOK_SECRET` ;
- `POST /public/stripe-connect/webhook` recoit les evenements des comptes
  connectes, limite le traitement a `account.updated` et utilise
  `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET`.

Les deux URLs d'onboarding Stripe Connect pointent vers l'application
commercant, pas vers le back-office Localeo :

- `LOCALEO_STRIPE_ONBOARDING_RETURN_URL=https://commercants.localeo.fr/stripe-connect/onboarding/return`
- `LOCALEO_STRIPE_ONBOARDING_REFRESH_URL=https://commercants.localeo.fr/stripe-connect/onboarding/refresh`

Le backend reste seul responsable de la creation des `AccountLink` Stripe et de
la synchronisation des statuts. L'application commercant gere l'experience de
retour, verifie la session commercant et appelle le backend avec un `state`
opaque signe ou un mecanisme equivalent anti-CSRF.

Les noms historiques `STRIPE_API_KEY` et `STRIPE_WEBHOOK_SECRET`, lorsqu'ils
existent encore, doivent etre migres vers ces noms cibles ou documentes comme
alias techniques de compatibilite transitoire.

Le developpement et les tests peuvent demarrer sur un environnement Stripe de
test dedie. L'activation production reste interdite tant que la validation
juridique, finance et conformite PSP n'est pas obtenue.

### 2. Strategie de migration

La migration est one-shot, car l'application n'est pas encore en production
pour ces flux.

Les objets metier conserves sont :

- `Paiement` ;
- `MouvementReversement` ;
- `Reversement` ;
- `PaiementReversement`.

Ils deviennent des projections Stripe. Ils ne doivent plus piloter de virement
bancaire manuel, d'export bancaire ou de confirmation manuelle.

Les lots de paiement bancaire, exports et parcours de confirmation manuelle
sont retires des surfaces operationnelles cibles, sans fallback ni
retrocompatibilite applicative.

### 3. Statuts cibles des mouvements de reversement

Les statuts cibles des mouvements de reversement Stripe sont :

| Statut | Signification |
| --- | --- |
| `A_CALCULER` | La validation ou l'evenement metier est connu, mais le montant/referentiel financier doit encore etre confirme. |
| `TRANSFERABLE` | Le mouvement est eligible a une campagne Stripe Connect. |
| `BLOQUE_ONBOARDING_STRIPE` | Le compte connecte commercant est absent, incomplet, bloque ou non eligible. |
| `EN_CAMPAGNE` | Le mouvement est selectionne dans une campagne bimensuelle non finalisee. |
| `TRANSFER_DEMANDE` | Le transfer Stripe a ete demande de maniere idempotente. |
| `TRANSFER_CONFIRME` | Stripe a confirme le transfer. |
| `ECHEC_TRANSFER` | Le transfer a echoue et doit etre repris via Stripe apres correction. |
| `ANNULE` | Le mouvement est neutralise par une regle metier ou une decision auditee. |

Les anciens libelles issus du flux manuel, notamment `A_REVERSER` ou `ECHEC`
generique, ne doivent pas etre utilises comme cible Stripe Connect. Ils peuvent
etre mappes temporairement pendant la refonte technique si du code historique
les reference encore.

### 4. Ordre d'implementation

L'implementation doit commencer par un lot technique 0 avant les parcours
fonctionnels :

1. modele interne et migrations one-shot ;
2. ports applicatifs Stripe Connect, paiement, transfer, remboursement et
   webhook ;
3. journal minimal des operations Stripe et idempotence ;
4. feature flag d'activation Stripe Connect ;
5. inventaire puis retrait des usages operationnels manuels.

Les lots fonctionnels s'enchainent ensuite dans l'ordre suivant :

1. onboarding et eligibilite commercants Stripe Connect ;
2. controle de vendabilite des coffrets ;
3. paiement client avec `transfer_group` ;
4. validation QR et mouvements transferables ou bloques ;
5. campagnes bimensuelles de transfers Stripe ;
6. webhooks, reprises et rapprochement ;
7. remboursements et support ;
8. back-office finance cible.

## Consequences

- Le code doit pouvoir etre livre et teste en environnement test Stripe sans
  autoriser la production par accident.
- Les endpoints, use cases et vues back-office doivent lire les projections
  internes, mais declencher les operations financieres exclusivement via Stripe.
- Les tests doivent couvrir l'idempotence et le scenario complet : commercant
  eligible, coffret vendable, achat paye, validation QR, mouvement transferable,
  campagne, transfer Stripe confirme.
- Les blocages Stripe ne doivent pas etre contournes par une procedure bancaire
  manuelle.
- Les documents contractuels et le dossier de preuve restent les pre-requis de
  go-live production.

## Alternatives considerees

- **Destination charges** : ecarte comme cible principale, car le besoin Localeo
  impose de ne transferer les fonds qu'apres validation QR et campagne
  bimensuelle.
- **Stripe Custom** : ecarte pour le MVP, car Express reduit la charge
  d'onboarding, KYC et support compte connecte.
- **Reversement manuel en fallback** : ecarte pour des raisons de conformite,
  d'audit et de coherence contractuelle.
- **Retrocompatibilite applicative des anciens lots bancaires** : ecartee car
  l'application n'est pas en production sur ces flux.
