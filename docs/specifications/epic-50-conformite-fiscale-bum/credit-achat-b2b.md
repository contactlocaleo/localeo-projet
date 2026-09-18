# Epic 50 - Credit d'achat B2B sur coffrets expires

## Etat d'implementation

Le backend est implemente par `v209` a `v214` derriere
`LOCALEO_FEATURE_B2B_PURCHASE_CREDIT_ENABLED`. L'activation reste soumise aux
validations Finance/Juridica et aux recettes Stripe et exploitation.

## Decision de conception proposee

Lorsqu'un coffret achete en B2B expire avec une ou plusieurs prestations non
utilisees, Localeo peut attribuer a l'acheteur professionnel un credit d'achat.
Ce credit est utilisable sur une future commande de coffrets :

- par le partenaire dans Localeo Animation pour une commande de lots ;
- par l'organisation professionnelle dans la Marketplace Pro.

Le terme fonctionnel recommande est `credit d'achat B2B`. Le terme `cagnotte`
peut etre utilise dans l'interface, mais ne doit pas conduire a modeliser un
compte bancaire ou une monnaie librement transferable.

## Principes fiscaux et comptables

- les fonds de l'achat initial sont deja encaisses par Localeo ;
- aucune prestation non executee n'est reversee a un commercant ;
- le credit constitue une obligation de Localeo envers l'acheteur B2B ;
- l'attribution du credit ne constitue pas un nouvel encaissement ;
- l'utilisation du credit est un moyen de reglement partiel ou total d'un
  nouvel achat de BUM ;
- la TVA des prestations reste declenchee lors de leur execution ;
- les frais ou services propres a Localeo ne sont pas inclus dans le credit,
  sauf decision comptable explicite.

Le BOFiP indique qu'un BUM non utilise a son echeance ne declenche pas de TVA.
La transformation en credit, sa duree de validite et son traitement comptable
doivent toutefois etre confirmes par le conseil juridique et comptable.

## Beneficiaire

Le credit appartient exclusivement a l'acheteur contractuel :

- `ANIMATION_PARTNER` : couple partenaire Animation et, si la tarification
  l'exige, commune ;
- `PRO_ORGANIZATION` : organisation ayant passe la commande Pro.

La Marketplace cree une identite technique stable `organisation_pro_id`, sans
creer de compte utilisateur. Elle est rapprochee initialement par SIRET et par
l'adresse de facturation verifiee. Les achats, le compte de credit et les
demandes de facture Pro referencent cette identite.

Le SIRET est normalise et valide avant rapprochement. Une fusion, une scission
ou un changement de SIRET ne modifie jamais automatiquement le proprietaire du
credit : l'operation passe par le BackOffice, exige un justificatif et produit
une trace d'audit.

Le beneficiaire final du coffret, le commercant et l'administrateur ayant cree
la commande ne deviennent pas proprietaires du credit. Le credit n'est ni
transferable entre organisations, ni retirable en especes en V1.

## Montant attribue

Le credit ne doit pas etre calcule par une simple somme de prix catalogue. Il
est plafonne a la part du montant effectivement paye pour les prestations non
utilisees, apres remises et hors frais propres a Localeo.

```text
baseEligibleCommande
  = montantCoffretsEffectivementPaye
  - remboursements
  - fraisLocaleoNonCreditables

creditCoffretExpire
  = somme(allocationPayeeSnapshottee des prestations non utilisees)

creditAttribue
  = min(creditCoffretExpire, soldeEligibleNonDejaCredite)
```

L'allocation par prestation est snapshottee au paiement. La somme des
allocations d'un coffret ne peut pas depasser sa base eligible. Une prestation
executee, annulee avec regularisation ou deja creditee ne peut pas produire un
second credit.

Tous les montants sont representes en centimes. Apres allocation
proportionnelle et arrondi de chaque ligne, l'eventuel ecart residuel est porte
sur la derniere ligne eligible. Une contrainte impose que la somme des
allocations soit exactement egale a la base payee allouee.

## Fait generateur

Le credit est attribue lorsque `CoffretInstance` passe effectivement a
`EXPIRE`, apres verification transactionnelle des prestations :

```text
achat B2B paye
AND coffret instance expire
AND au moins une prestation non VALIDEE
AND absence de remboursement incompatible
AND absence de credit anterieur pour la meme allocation
```

Le batch existant d'expiration publie une commande idempotente de calcul. Une
correction ou annulation ulterieure produit un mouvement compensatoire ; aucun
solde n'est reecrit directement.

## Registre comptable applicatif

### `comptes_credit_achat_b2b`

| Colonne | Description |
| --- | --- |
| `id` | UUID |
| `owner_type`, `owner_id` | partenaire Animation ou organisation Pro |
| `devise` | `EUR` en V1 |
| `statut` | `ACTIVE`, `SUSPENDED`, `CLOSED` |
| `created_at`, `updated_at` | audit |

Contrainte unique `(owner_type, owner_id, devise)`.

### `mouvements_credit_achat_b2b`

Registre immuable :

| Colonne | Description |
| --- | --- |
| `id`, `account_id` | identite et compte |
| `type` | `CREDIT_EXPIRATION`, `DEBIT_PURCHASE`, `REVERSAL`, `EXPIRATION`, `ADMIN_ADJUSTMENT` |
| `amount` | montant positif ; le sens vient du type |
| `status` | `PENDING`, `POSTED`, `CANCELLED` |
| `source_type`, `source_id` | coffret expire, commande ou correction |
| `idempotency_key` | unique |
| `occurred_at`, `posted_at` | dates |
| `expires_at` | echeance eventuelle du lot de credit |
| `metadata` | allocations et references, sans secret |
| `created_by`, `reason` | audit, motif obligatoire pour ajustement |

Le solde disponible est une projection : credits postes moins debits postes,
expirations et reservations actives. Il n'est jamais modifie par un simple
`UPDATE balance = ...`.

### `reservations_credit_achat_b2b`

Une reservation evite une double depense pendant un checkout : compte,
commande, montant, statut `ACTIVE/CAPTURED/RELEASED/EXPIRED`, expiration et cle
d'idempotence. Une contrainte garantit une reservation active par commande.

### `codes_credit_achat_b2b`

Le credit est presente sous la forme d'un code saisissable avant Stripe. Ce
code designe un instrument rattache au compte ; le registre de mouvements, et
non le code, reste la source de verite du solde.

| Colonne | Description |
| --- | --- |
| `id`, `organisation_pro_id` | instrument et organisation Pro |
| `code_hash`, `code_suffix` | empreinte et derniers caracteres affichables ; jamais de code en clair en base |
| `buyer_email_hash`, `buyer_identity_snapshot_id` | acheteur autorise et identite contractuelle |
| `status` | `ACTIVE`, `REPLACED`, `REVOKED` |
| `issued_at`, `revoked_at` | cycle de vie |

Le code aleatoire a forte entropie est transmis hors des URL et ne doit jamais
apparaitre dans les logs.

Une organisation ne possede qu'un code actif. Plusieurs expirations alimentent
des lots distincts dans son compte, chacun conservant sa propre echeance. Le
backend consomme en priorite le lot expirant le plus tot.

Le code est emis lors de l'attribution du premier credit et notifie a l'adresse
de facturation verifiee. Le message d'emission ne contient jamais un OTP actif.
Une reemission revoque immediatement le code precedent sans modifier le compte.

Chaque lot expire a `23:59:59 Europe/Paris` a la date affichee. Une reservation
creee avant cette limite reste valable 30 minutes. Si elle est ensuite liberee,
la part provenant d'un lot dont l'echeance est depassee n'est plus disponible.

### `allocations_credit_expiration`

Relie le mouvement de credit a `CoffretInstance`, `ValidationPrestation` ou au
statut de prestation non utilise, avec le montant alloue. Une contrainte unique
par prestation et mouvement interdit le double credit tout en autorisant des
composantes cash et credit portant des echeances distinctes.

## Utilisation lors d'un achat

```text
creation commande
  -> saisie du code avant Stripe
  -> verification du code et de l'acheteur autorise
  -> calcul du solde disponible et du montant applicable
  -> reservation atomique
  -> reste a payer par Stripe
     -> paiement confirme : capturer reservation et poster debit
     -> paiement echoue/expire : liberer reservation
  -> commande payee lorsque credit capture + paiement = total attendu
```

Une commande entierement payee par credit ne cree pas de paiement Stripe mais
suit le meme cas d'usage de confirmation, de snapshot et d'emission des
coffrets. La cle de capture est `B2B_CREDIT_PURCHASE:{commande_id}`.

Le montant applique est `min(soldeDisponible, totalCommande)`. Si le credit est
superieur au total, seul le montant de la commande est debite et le reliquat
reste disponible sur le meme code. S'il est inferieur ou egal, le solde est
integralement reserve puis le code passe a `EXHAUSTED` seulement apres
confirmation du paiement complet. En cas d'echec ou d'expiration Stripe, la
reservation est liberee et le code redevient utilisable.

En cas d'annulation ou de remboursement, Stripe ne rembourse jamais plus que la
part effectivement payee par Stripe. La part reglee par credit est restituee par
un mouvement compensatoire qui conserve l'echeance du lot d'origine.

Le credit minore le **reste a payer**, pas le montant brut de la commande. Le
justificatif conserve le total avant credit, le credit utilise et le paiement
Stripe, afin de ne pas presenter le credit comme une remise commerciale.

Le justificatif d'acquisition affiche separement : total de commande, credit
utilise, paiement externe et reste paye, sans calculer la TVA des prestations
sous-jacentes.

Les conditions du credit sont affichees lors de l'achat B2B puis a sa premiere
utilisation. Localeo conserve la version acceptee, la date, le canal et
l'identite verifiee. Leur wording et leur opposabilite restent soumis a
validation Juridica.

## API backend

### Animation et Marketplace Pro

- `GET /protected/animation-locale/credits-achat` : solde, lots et historique
  du couple partenaire + commune actif ;
- `POST /protected/animation-locale/credits-achat/commandes/{id}/reserver` :
  reservation explicite, egalement integree a la creation de commande ;
- `GET /public/credits-achat-b2b/conditions` : wording et version actifs ;
- `POST /public/credits-achat-b2b/otp` : demande non enumerable d'OTP ;
- `POST /public/credits-achat-b2b/sessions` : verification OTP, acceptation des
  conditions et creation d'un bearer court ;
- `GET /public/credits-achat-b2b/me` : solde Pro limite a l'organisation ;
- `POST /public/gestion-achats/paiements/initialiser` avec
  `X-Localeo-Credit-Session` : reservation et paiement mixte ou integral.

Les routes metier Animation et Pro exposent ces capacites sous leur contexte
tenant. Le backend deduit toujours le proprietaire de la session et de la
commande ; aucun `owner_id` fourni par le navigateur ne fait autorite.

### BackOffice

- recherche des comptes, mouvements, sources et reservations ;
- recalcul explicatif du solde ;
- `POST /internal/conformite-fiscale/credits-achat-b2b/comptes/{id}/ajustements`
  pour une regularisation compensatoire idempotente avec motif obligatoire ;
- interdiction de modifier ou supprimer un mouvement poste ;
- alertes sur solde negatif, reservation expiree non liberee et double source.

## Visibilite Animation

Localeo Animation affiche :

- solde disponible et date de prochaine expiration ;
- historique : coffrets expires, credits attribues et commandes financees ;
- credit maximal utilisable dans le recapitulatif d'une commande de lots ;
- repartition `credit / paiement Stripe` avant confirmation ;
- credit consomme sur le justificatif et le detail de commande.

## Visibilite Marketplace Pro

L'espace acheteur professionnel affiche les memes informations au niveau de
l'organisation : solde, historique, prochaine echeance et application au
panier. Le parcours B2C n'expose ni ne consomme ce credit.

La V1 ne necessite pas de compte Pro permanent. L'acces repose sur une session
legere obtenue par code + OTP envoye a l'adresse de facturation snapshottee lors
de l'achat d'origine. Ce bearer court est limite au credit et doit etre conserve
uniquement pendant le checkout par l'application cliente. La possession du code seul ne
permet jamais de le depenser. Un changement d'adresse ou une delegation passe
par une procedure BackOffice auditee avec verification de l'organisation.
La recuperation exige le controle du SIRET et d'un justificatif : l'ancien code
est revoque puis un nouveau est emis, sans modifier le compte ni son historique.

## Securite, audit et conservation

- chaque attribution, reservation, liberation, debit, expiration et ajustement
  est audite ;
- limiter les tentatives par IP, code et email, utiliser des reponses non
  enumerables, un verrouillage temporaire et des alertes d'anomalie ;
- ne stocker ni journaliser le code ou l'OTP en clair ;
- toute mutation accepte une cle d'idempotence ;
- les operations de solde utilisent verrou de compte et contraintes en base ;
- un administrateur ne modifie jamais directement le solde ;
- les historiques et justificatifs sont conserves selon la politique fiscale
  configurable de l'Epic ;
- les exports comptables rapprochent encaissement initial, passif de credit,
  utilisation et reliquat.

Un controle periodique verifie l'invariant suivant et rapproche les
reservations du statut reel des commandes et paiements Stripe :

```text
credits attribues - credits consommes - credits expires - credits annules
  = passif de credit restant
```

Les notifications metier couvrent au minimum : creation du credit, prochaine
expiration, consommation, remplacement du code et anomalie necessitant une
intervention. Leur echec est rejouable par l'outbox et n'annule jamais le
mouvement financier deja valide.

## Decisions retenues et validations externes

Les choix produit sont retenus : validite de 12 mois, proprietaire partenaire +
commune ou organisation Pro, code unique par organisation, consommation par
echeance la plus proche, credit non remboursable et non transferable, paiement
mixte et restitution ventilee en cas d'annulation.

Restent soumis a validation externe avant activation : qualification juridique
et wording du credit, comptabilisation du passif et de son expiration, ainsi que
la formule d'allocation financiere definitive.

Lorsqu'un coffret achete avec un paiement mixte expire inutilise, la part payee
en argent produit un nouveau lot valable 12 mois. La part payee par credit n'est
restituee que si son lot source est encore valide et conserve exactement son
echeance d'origine. Une echeance depassee ne peut donc jamais etre prolongee par
des achats successifs.
