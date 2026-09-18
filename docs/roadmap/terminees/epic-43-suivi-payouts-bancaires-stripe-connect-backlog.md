# Backlog Epic 43 - Suivi des virements bancaires Stripe Connect

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : prolonger le suivi des transfers Stripe Connect jusqu'au virement vers le compte bancaire du commercant, sans confondre le solde Stripe connecte et le compte bancaire externe.
- Pourquoi maintenant : l'EPIC 39 confirme aujourd'hui le transfer `tr_...` vers le compte Stripe connecte, mais Localeo ne sait pas encore dire si les fonds ont ete inclus dans un payout `po_...`, sont en transit, verses ou retournes par la banque.
- Prerequis : flux `separate charges and transfers` de l'EPIC 39 actif, comptes Express eligibles aux payouts et webhook comptes connectes configure.
- Domaine fonctionnel cible : `gestion_reversement`.
- Surfaces concernees : backend, webhook Stripe Connect, back-office finance/support et application commercant.
- Declinaison frontend : [EPIC 43 - Impacts application commercant](epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md).

## Decisions de cadrage actees

- Le `Transfer` Stripe et le `Payout` bancaire sont deux etapes distinctes.
- `Reversement.statut = PAYE` conserve le sens `fonds transferes vers le solde Stripe du commercant`.
- Le suivi bancaire est porte par un statut distinct et ne doit pas reutiliser les statuts du transfer.
- Les payouts automatiques Stripe sont conserves en cible ; Localeo ne cree pas un payout manuel par reversement dans le MVP.
- Un payout peut regrouper plusieurs transfers et plusieurs reversements.
- Un reversement peut etre rattache a plusieurs tentatives de payout lorsqu'un premier payout echoue puis est repropose.
- Le champ historique `PaiementReversement.stripe_payout_id` ne constitue pas, seul, un modele de rapprochement suffisant.
- Le rapprochement detaille s'appuie sur `payout.reconciliation_completed`, les balance transactions du compte connecte et le `destination_payment` du Transfer.
- `payout.paid` n'est pas considere comme irreversible : un `payout.failed` tardif doit pouvoir corriger la projection locale.
- Les coordonnees bancaires completes restent gerees par Stripe et ne sont pas repliquees dans Localeo.
- L'association `AssociationPayoutPaiementReversement` devient la source de verite du rapprochement ; le champ direct `PaiementReversement.stripe_payout_id` est migre puis supprime sans periode de double ecriture.
- Un payout `paid` conserve `statut_stripe = paid` tandis que `statut_rapprochement` evolue de `EN_ATTENTE` ou `EN_COURS` vers `RAPPROCHE` apres association aux paiements de reversement.
- Une reconciliation terminee mais impossible produit `statut_rapprochement = NON_RAPPROCHE` ; les payouts manuels ou instantanes recus sans detail suffisant produisent `NON_RAPPROCHABLE`.
- Localeo supporte completement les payouts automatiques standard. Les payouts manuels ou instantanes sont recus et affiches, mais Localeo ne les cree pas et ne promet pas leur rapprochement exact.
- Le rattrapage s'execute toutes les 6 heures sur les payouts incomplets des 14 derniers jours, complete par un controle nocturne sur 90 jours et un rejeu cible par `po_...` ou `acct_...`.
- Le backfill initial remonte jusqu'au premier Transfer Stripe Connect Localeo connu.
- L'alerte d'absence de payout utilise actuellement les seuils de repli J+7 et J+10 ouvrables. Le calcul depuis la disponibilite des fonds, le calendrier Stripe et la desactivation pour un calendrier manuel reste a finaliser avant ouverture.
- Un passage tardif de `paid` a `failed` met `statut_stripe = failed`, sans retrograder `Reversement.statut = PAYE`, declenche une alerte critique finance/support et informe le commercant. Aucun nouveau Transfer ou Payout n'est cree automatiquement.
- Les motifs d'echec exposes au commercant utilisent une taxonomie controlee ; le code et le detail Stripe assainis restent reserves au back-office autorise.
- Les donnees financieres normalisees, associations, statuts, montants et motifs publics sont conserves 10 ans apres la cloture de l'exercice concerne. Le payload webhook minimise et le detail technique d'echec sont conserves 13 mois en acces restreint. `trace_id.value` est conserve 5 ans en acces restreint puis supprime ; seule une destination masquee est conservee.
- L'acces complet a `trace_id.value` est reserve a la finance et au support L2 avec audit ; le support L1 n'en voit qu'une valeur masquee. L'application commercant ne l'expose qu'apres 10 jours ouvrables suivant un payout annonce verse mais non recu, ou lorsqu'une action explicite est requise.
- Le terme public est `virement bancaire`. Les termes `payout`, `po_...`, `payout.*` et les statuts de rapprochement restent limites au backend, au back-office technique et aux echanges Stripe.
- La projection conserve deux dimensions independantes : le statut Stripe du payout et le statut de rapprochement Localeo. Le statut affiche au commercant est calcule a partir de ces deux dimensions.
- Les appels Payout et les evenements Connect restent sur l'API Stripe v1, y compris si Accounts v2 est utilise pour d'autres fonctions. Une version d'API v1 explicite et identique est epinglee dans le backend, la destination d'evenements Stripe et les tests de contrat.

## User Stories

1. `PRD-381` En tant qu'operateur technique, je veux recevoir les evenements payout des comptes connectes afin de suivre le versement bancaire apres le transfer Stripe.
   - Statut : `Fait backend`
   - Resultat attendu : le webhook `POST /public/stripe-connect/webhook` accepte `payout.created`, `payout.updated`, `payout.paid`, `payout.failed`, `payout.canceled` et `payout.reconciliation_completed`.
   - Resultat attendu : chaque evenement est verifie avec `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET` et le compte commercant est identifie depuis `event.account`.
   - Resultat attendu : les evenements de payout ne sont pas traites sur le webhook du compte plateforme.
   - Resultat attendu : `account.external_account.updated` est egalement traite afin de detecter la desactivation du compte bancaire apres un echec de virement ; le traitement existant de `account.updated` est conserve.
   - Resultat attendu : le backend et la destination d'evenements Connect utilisent une version Stripe API v1 epinglee et testee ; l'EPIC ne depend pas d'evenements Accounts v2.

2. `PRD-382` En tant que responsable finance, je veux disposer d'une projection locale des payouts Stripe afin de connaitre leur montant, leur destination et leur statut.
   - Statut : `Fait backend`
   - Resultat attendu : une entite `PayoutStripe` conserve `stripe_payout_id`, `stripe_account_id`, montant, devise, statut, methode, caractere automatique, date d'arrivee, destination masquee, references de balance transaction et informations d'echec.
   - Resultat attendu : `stripe_payout_id` est unique et les mises a jour sont idempotentes.
   - Resultat attendu : le payload Stripe conserve est minimise et ne contient pas de coordonnees bancaires completes.
   - Resultat attendu : les durees de conservation et droits d'acces suivent la politique actee dans cet epic.
   - Resultat attendu : `statut_stripe` (`pending`, `in_transit`, `paid`, `failed`, `canceled`) et `statut_rapprochement` (`EN_ATTENTE`, `EN_COURS`, `RAPPROCHE`, `NON_RAPPROCHE`, `NON_RAPPROCHABLE`) sont stockes separement.

3. `PRD-383` En tant que systeme de rapprochement, je veux conserver la reference `destination_payment` du Transfer afin de relier le credit du compte connecte au reversement Localeo.
   - Statut : `Fait backend`
   - Resultat attendu : le port et le gateway Stripe exposent `destination_payment_id` en plus de `stripe_transfer_id` et de la balance transaction plateforme.
   - Resultat attendu : la reference `py_...` est stockee sur la projection de paiement de reversement ou dans une projection d'association explicite.
   - Resultat attendu : les anciens transfers peuvent etre enrichis par une reprise Stripe sans recreer d'operation financiere.

4. `PRD-384` En tant que systeme, je veux projeter les webhooks payout de maniere idempotente et independante de leur ordre afin de conserver un etat bancaire coherent.
   - Statut : `Fait backend`
   - Resultat attendu : les statuts Stripe `pending`, `in_transit`, `paid`, `failed` et `canceled` sont normalises dans la projection locale.
   - Resultat attendu : un doublon `evt_...` ne cree ni payout ni association supplementaire.
   - Resultat attendu : un evenement tardif `payout.failed` peut remplacer un etat precedemment `paid` et conserve la cause de l'echec.
   - Resultat attendu : ce retour tardif ne retrograde pas le statut `PAYE` du reversement, declenche une alerte critique et n'initie automatiquement aucun nouveau flux financier.

5. `PRD-385` En tant que responsable finance, je veux rapprocher chaque payout automatique des transfers qu'il contient afin de justifier les montants verses en banque.
   - Statut : `Fait backend`
   - Resultat attendu : apres `payout.reconciliation_completed`, le backend liste les balance transactions avec le filtre `payout=po_...` dans le contexte `Stripe-Account: acct_...`.
   - Resultat attendu : les transactions sont rapprochees de `destination_payment_id`, puis de `PaiementReversement` et `Reversement`.
   - Resultat attendu : une association explicite payout/paiement conserve le montant rapproche et la balance transaction du compte connecte.
   - Resultat attendu : une transaction non rapprochee est tracee comme anomalie sans etre affectee arbitrairement a un reversement.
   - Resultat attendu : un payout `paid` conserve son statut Stripe pendant que le rapprochement evolue de `EN_ATTENTE` ou `EN_COURS` vers `RAPPROCHE`, ou vers `NON_RAPPROCHE` si aucune association fiable n'est possible.
   - Resultat attendu : la table d'association est la source de verite ; le champ `PaiementReversement.stripe_payout_id` est migre puis supprime dans la meme evolution fonctionnelle.

6. `PRD-386` En tant que commercant, je veux distinguer le transfer vers mon compte Stripe du versement vers ma banque afin de comprendre ou se trouvent mes fonds.
   - Statut : `Fait backend`
   - Resultat attendu : l'API commercant expose uniquement les codes publics `VIREMENT_A_VENIR`, `VIREMENT_EN_COURS`, `VIREMENT_EFFECTUE_CONFIRMATION_EN_COURS`, `VIREMENT_EFFECTUE`, `ECHEC_VIREMENT`, `VIREMENT_ANNULE` ou `VIREMENT_DETAILS_INDISPONIBLES`.
   - Resultat attendu : la date d'arrivee estimee, la date du dernier evenement et un motif d'echec exploitable sont exposes quand disponibles.
   - Resultat attendu : aucun IBAN, identifiant bancaire complet ou message Stripe interne sensible n'est expose.
   - Resultat attendu : le motif public est issu d'une taxonomie controlee (`coordonnees bancaires invalides`, `compte ferme`, `refus bancaire`, `devise non supportee`, `action requise` ou `incident technique`).
   - Resultat attendu : la reference de tracage bancaire n'est exposee qu'apres 10 jours ouvrables suivant un payout annonce verse mais non recu, ou lorsqu'une action explicite est requise.
   - Resultat attendu : le endpoint existant `GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mois/{nb_mois}` est enrichi de facon additive avec `virements_bancaires`, une liste permettant de representer plusieurs tentatives sans exposer les codes internes `PAYOUT_*`.

7. `PRD-387` En tant qu'application commercant, je veux afficher la chronologie du reversement jusqu'au compte bancaire afin de donner une information claire au partenaire.
   - Statut : `A faire application commercant`
   - Resultat attendu : l'interface distingue `Reversement transmis a Stripe`, `Virement bancaire a venir`, `Virement bancaire en cours`, `Virement effectue` et `Echec du virement bancaire`.
   - Resultat attendu : un payout regroupant plusieurs reversements n'est pas presente comme un virement individuel de meme montant si ce n'est pas le cas.
   - Resultat attendu : en cas d'echec, l'application oriente le commercant vers la mise a jour de ses informations bancaires dans Stripe.
   - Resultat attendu : aucun libelle commercant n'emploie `payout`, `paid`, `failed`, `rapprochement` ou un identifiant `po_...`.
   - Resultat attendu : `VIREMENT_EFFECTUE_CONFIRMATION_EN_COURS` est affiche `Virement effectue - details en cours de confirmation` et `VIREMENT_DETAILS_INDISPONIBLES` est affiche `Virement effectue - details indisponibles`.

8. `PRD-388` En tant qu'operateur finance ou support, je veux superviser les payouts et leurs echecs afin de traiter les incidents bancaires sans confondre transfer et payout.
   - Statut : `Fait backend - validation canaux requise en recette`
   - Resultat attendu : le back-office permet de rechercher par `po_...`, `tr_...`, `acct_...`, commercant, statut et periode.
   - Resultat attendu : les vues 360 affichent montant du payout, nombre de reversements rapproches, date d'arrivee, destination masquee, statut, code et message d'echec.
   - Resultat attendu : un payout en echec ou non rapproche genere une alerte operationnelle et une trace d'audit.
   - Resultat attendu : l'absence de payout genere un avertissement deux jours ouvrables apres la prochaine date attendue, puis une alerte critique apres cinq jours ouvrables ; les seuils de repli sont sept et dix jours ouvrables lorsque le calendrier est indisponible.
   - Resultat attendu : `trace_id.value` complet est limite a la finance et au support L2 avec audit ; le support L1 n'accede qu'a une valeur masquee.
   - Resultat attendu : les routes finance sont `GET /protected/gestion-reversement/payouts`, `GET /protected/gestion-reversement/payouts/{stripe_payout_id}`, `POST /protected/gestion-reversement/payouts/{stripe_payout_id}/reconcilier` et `POST /protected/gestion-reversement/payouts/rattrapage`, protegees par `internal:finance`.
   - Resultat attendu : les anomalies sont persistantes et visibles dans le back-office ; une alerte critique est envoyee par email au groupe finance/support configure.
   - Resultat attendu : un echec de virement declenche un email commercant et, si le commercant a active ce canal, une WebPush dedoublonnee par payout et transition de statut.

9. `PRD-389` En tant que responsable exploitation, je veux pouvoir reconciler les payouts manquants ou incomplets sans creer de nouveau flux financier afin de reparer les projections locales.
   - Statut : `Fait backend`
   - Resultat attendu : un traitement de reprise liste les payouts recents des comptes connectes et rejoue leur projection de facon idempotente.
   - Resultat attendu : la reprise peut enrichir les anciens transfers avec `destination_payment` et rattacher les payouts deja termines.
   - Resultat attendu : aucun appel de reprise ne cree de Transfer ou Payout Stripe.
   - Resultat attendu : la reprise s'execute toutes les 6 heures sur 14 jours, avec un controle nocturne sur 90 jours, un backfill initial depuis le premier Transfer Connect et un rejeu cible par payout ou compte connecte.
   - Resultat attendu : les echecs permanents et anomalies restantes declenchent une alerte exploitable.
   - Resultat attendu : le rattrapage est expose par `POST /protected/gestion-reversement/payouts/rattrapage/batch` et enregistre dans le catalogue des batchs avec verrou, execution auditee et relance manuelle autorisee.
   - Resultat attendu : un batch quotidien de purge supprime les payloads et details techniques arrives a echeance, masque ou supprime `trace_id.value` apres cinq ans et ne supprime jamais les donnees financieres soumises a la conservation de dix ans.
   - Resultat attendu : la purge propose un `dry_run`, est auditee et est exposee par `POST /protected/exploitation/maintenance/payouts/purger`.

10. `PRD-390` En tant que responsable qualite, je veux tester les parcours payout nominaux et en echec afin de securiser le passage en production.
   - Statut : `Tests unitaires ajoutes - recette Stripe a faire`
    - Resultat attendu : les tests couvrent payout groupe, evenements dans le desordre, doublons, `paid` puis `failed`, reconciliation en cours ou impossible, transaction inconnue, plusieurs tentatives, payouts manuels ou instantanes et isolation entre comptes connectes.
    - Resultat attendu : une procedure de recette Stripe test couvre un compte bancaire de succes et plusieurs codes d'echec documentes par Stripe.
    - Resultat attendu : les logs, exports et APIs sont verifies contre toute exposition de coordonnees bancaires completes.
    - Resultat attendu : les tests de contrat verifient la version Stripe API v1 epinglee, `account.external_account.updated`, les routes finance, les codes publics `VIREMENT_*` et l'absence du terme `payout` dans les libelles commercant.

## Statuts techniques cibles

| Niveau | Statuts | Signification |
| --- | --- | --- |
| Transfer Stripe | `TRANSFER_DEMANDE`, `TRANSFER_CONFIRME`, `ECHEC_TRANSFER` | Mouvement entre le compte plateforme et le solde Stripe connecte. |
| Reversement Localeo | `EN_COURS`, `PAYE`, `ECHEC`, `PARTIEL` | Agregat metier des transfers dus au commercant. |
| Statut Stripe du payout | `pending`, `in_transit`, `paid`, `failed`, `canceled` | Etat de l'acheminement transmis par Stripe. |
| Rapprochement Localeo | `EN_ATTENTE`, `EN_COURS`, `RAPPROCHE`, `NON_RAPPROCHE`, `NON_RAPPROCHABLE` | Etat de l'association entre payout et reversements Localeo. |

## Libelles destines aux commercants

| Code API public | Libelle commercant | Origine technique principale |
| --- | --- | --- |
| `VIREMENT_A_VENIR` | Virement bancaire a venir | payout `pending` |
| `VIREMENT_EN_COURS` | Virement bancaire en cours | payout `in_transit` |
| `VIREMENT_EFFECTUE_CONFIRMATION_EN_COURS` | Virement effectue - details en cours de confirmation | payout `paid`, rapprochement `EN_ATTENTE` ou `EN_COURS` |
| `VIREMENT_EFFECTUE` | Virement effectue | payout `paid`, rapprochement `RAPPROCHE` |
| `ECHEC_VIREMENT` | Echec du virement bancaire | payout `failed` |
| `VIREMENT_ANNULE` | Virement bancaire annule | payout `canceled` |
| `VIREMENT_DETAILS_INDISPONIBLES` | Virement effectue - details indisponibles | rapprochement `NON_RAPPROCHE` ou `NON_RAPPROCHABLE` |

Les etats `NON_RAPPROCHE` et `NON_RAPPROCHABLE` restent visibles en tant que tels uniquement dans les surfaces finance/support. L'application commercant recoit un code et un libelle publics sans notion de rapprochement.

## Donnees et objets cibles

- `PayoutStripe`
- `AssociationPayoutPaiementReversement`
- `destination_payment_id` sur la projection de Transfer
- repository de payouts et recherche par `stripe_payout_id`
- port Stripe de consultation des payouts et balance transactions d'un compte connecte
- use case de traitement webhook payout
- use case de reconciliation d'un payout
- traitement de rattrapage des payouts recents
- traitement de purge des donnees payout arrivees a echeance
- projection commercant et projection back-office finance

## Hors MVP initial

- Creation d'un payout manuel Localeo pour chaque reversement.
- Payout instantane pilote depuis Localeo.
- Modification par Localeo de l'IBAN ou du calendrier bancaire du commercant.
- Promesse contractuelle d'une date bancaire garantie a partir de `arrival_date`.
- Rapprochement exact des payouts instantanes lorsque Stripe ne fournit pas la reconciliation detaillee.
- Remplacement du Dashboard Stripe comme outil de gestion des coordonnees bancaires.

## Validations externes restantes

- Faire valider par le juridique et le DPO les durees de conservation actees avant mise en production.
- Faire valider par la finance les seuils d'alerte J+2/J+5 ouvrables et leurs seuils de repli J+7/J+10 ouvrables.
- Faire valider par le produit et le support la taxonomie des motifs d'echec ; les libelles de statut utilisent desormais le vocabulaire `virement bancaire` acte dans cet epic.

## Definition of Done

- Les six evenements payout et `account.external_account.updated` sont configures sur le webhook des comptes connectes ; `account.updated` reste traite.
- La version Stripe API v1 est epinglee et couverte par des tests de contrat.
- La signature et l'idempotence des webhooks sont testees.
- Les payouts sont persistes sans coordonnees bancaires completes.
- Les transfers conservent `destination_payment_id`.
- Les payouts automatiques termines sont rapproches de leurs reversements.
- Les statuts transfer, reversement et payout restent distincts dans le domaine et les APIs.
- Le back-office et l'application commercant exposent une chronologie coherente.
- L'application commercant n'expose aucun terme ou statut technique `payout`.
- Les routes finance, les canaux d'alerte, le rattrapage et la purge sont operationnels et audites.
- Les echecs tardifs et les reprises sont couverts par des tests.
- Une procedure de recette test et une procedure d'exploitation sont publiees.


## Impacts dans l’application commerçant

Ce complément est réuni au backlog de l’EPIC. Ses états de préparation et de recette sont historiques ; l’état produit commun reste **Terminée**.

### Statut

- Version : passation frontend v1.
- Backend : implemente.
- Application commercant : a implementer.
- Epic source : [EPIC 43 - Suivi des virements bancaires Stripe Connect](epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md).
- Epic parente : [EPIC 39 - Impacts application commercant](epic-39-stripe-connect-psp-backlog.md).

### Objectif

Ce document constitue la version de l'EPIC 43 a integrer dans l'application
commercant.

L'application doit prolonger l'historique des reversements jusqu'au virement
sur le compte bancaire du commercant. Elle doit permettre de distinguer :

1. le reversement transmis au solde Stripe du commercant ;
2. le virement bancaire a venir ou en cours ;
3. le virement effectue, annule ou en echec.

Le vocabulaire affiche au commercant utilise exclusivement `virement
bancaire`. Les termes techniques Stripe `payout`, `paid`, `failed`,
`reconciliation`, `po_...` et `py_...` ne doivent jamais apparaitre dans
l'interface.

### Articulation avec l'EPIC 39

L'EPIC 39 et l'EPIC 43 suivent deux etapes differentes :

- EPIC 39 : Localeo transfere les fonds vers le solde du compte Stripe Connect
  du commercant ;
- EPIC 43 : Stripe verse ensuite les fonds disponibles vers le compte bancaire
  du commercant.

Le statut `PAYE` d'un reversement signifie que le transfer vers le compte
Stripe Connect est confirme. Il ne garantit pas, a lui seul, que la banque du
commercant a credite les fonds.

Un echec bancaire tardif ne modifie pas retroactivement le statut `PAYE` du
reversement. L'echec est affiche dans la chronologie du virement bancaire.

### Frontiere frontend/backend

L'application commercant :

- consomme la projection publique preparee par le backend ;
- affiche les statuts et libelles `VIREMENT_*` recus ;
- gere les etats de chargement, les actions et la navigation ;
- gere le deeplink WebPush `/reversements` ;
- reutilise le parcours Stripe Connect de l'EPIC 39 lorsqu'une action bancaire
  est requise.

L'application ne doit pas :

- appeler directement l'API Stripe ;
- recevoir ou traiter les webhooks Stripe ;
- reconstruire un statut bancaire depuis les statuts de reversement ;
- rapprocher des montants cote navigateur ;
- stocker une cle Stripe ou un secret `whsec_...` ;
- afficher un identifiant technique `po_...`, `py_...` ou un IBAN complet.

Les evenements Stripe, l'idempotence, le rapprochement, les alertes et les
notifications sortantes restent entierement geres par le backend.

### API backend a consommer

#### Historique des reversements

```http
GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mois/{nb_mois}
Authorization: Bearer <session_commercant>
```

Contraintes :

- `commercant_id` doit correspondre au commercant de la session ;
- la session doit disposer du scope `commercant:prestation` ;
- `nb_mois` doit etre strictement positif ;
- l'evolution est additive : les champs historiques restent disponibles et le
  tableau `virements_bancaires` est ajoute a chaque reversement.

#### Exemple de reponse

```json
[
  {
    "reversement_id": "4e9beafb-5ec1-4af1-8428-a86c128546f7",
    "montant_total": 26.68,
    "statut": "PAYE",
    "date_creation": "2026-08-12T08:10:00Z",
    "date_execution": "2026-08-12T08:12:00Z",
    "reference_paiement": "tr_example",
    "nb_mouvements": 1,
    "virements_bancaires": [
      {
        "statut_code": "VIREMENT_EFFECTUE",
        "statut_libelle": "Virement effectue",
        "montant_reversement_inclus": 26.68,
        "devise": "eur",
        "date_arrivee_estimee": "2026-08-14T00:00:00Z",
        "date_dernier_evenement": "2026-08-14T09:30:00Z",
        "destination_masquee": "Compte bancaire ****6789",
        "motif_echec": null,
        "action_requise": false,
        "lien_action": null,
        "reference_tracage_bancaire": null
      }
    ]
  }
]
```

#### Contrat TypeScript indicatif

```ts
export type StatutVirementBancaire =
  | "VIREMENT_A_VENIR"
  | "VIREMENT_EN_COURS"
  | "VIREMENT_EFFECTUE_CONFIRMATION_EN_COURS"
  | "VIREMENT_EFFECTUE"
  | "ECHEC_VIREMENT"
  | "VIREMENT_ANNULE"
  | "VIREMENT_DETAILS_INDISPONIBLES";

export interface VirementBancaireCommercant {
  statut_code: StatutVirementBancaire;
  statut_libelle: string;
  montant_reversement_inclus: number;
  devise: string;
  date_arrivee_estimee: string | null;
  date_dernier_evenement: string | null;
  destination_masquee: string | null;
  motif_echec: string | null;
  action_requise: boolean;
  lien_action: string | null;
  reference_tracage_bancaire: string | null;
}

export interface ReversementEffectue {
  reversement_id: string;
  montant_total: number;
  statut: string;
  date_creation: string | null;
  date_execution: string | null;
  reference_paiement: string | null;
  nb_mouvements: number;
  virements_bancaires: VirementBancaireCommercant[];
}
```

Le frontend doit tolerer les champs optionnels a `null` et un tableau
`virements_bancaires` absent dans un cache ou une ancienne reponse, en le
normalisant en tableau vide.

### Regles de presentation

#### Matrice des statuts publics

| Code API | Libelle principal | Ton visuel | Message ou action |
| --- | --- | --- | --- |
| `VIREMENT_A_VENIR` | Virement bancaire a venir | Neutre | Les fonds sont disponibles ou en preparation chez Stripe. |
| `VIREMENT_EN_COURS` | Virement bancaire en cours | Information | Afficher la date d'arrivee estimee lorsqu'elle existe. |
| `VIREMENT_EFFECTUE_CONFIRMATION_EN_COURS` | Virement effectue - details en cours de confirmation | Information positive | Ne pas presenter les details comme definitifs. |
| `VIREMENT_EFFECTUE` | Virement effectue | Succes | Afficher la destination masquee et la date disponibles. |
| `ECHEC_VIREMENT` | Echec du virement bancaire | Erreur | Afficher le motif public et le bouton d'action si requis. |
| `VIREMENT_ANNULE` | Virement bancaire annule | Avertissement | Expliquer qu'un prochain traitement peut etre necessaire sans le promettre. |
| `VIREMENT_DETAILS_INDISPONIBLES` | Virement effectue - details indisponibles | Neutre | Ne pas afficher d'erreur technique ni inventer une date. |

Le frontend doit utiliser `statut_libelle` fourni par le backend comme libelle
principal. La matrice locale sert de repli et de reference de design, pas de
source permettant de recalculer le statut.

#### Montants

- `montant_total` est le montant total du reversement Localeo ;
- `montant_reversement_inclus` est la part de ce reversement incluse dans le
  virement bancaire concerne ;
- un virement Stripe peut regrouper plusieurs reversements ;
- l'application ne doit donc jamais presenter le montant technique total d'un
  virement groupe comme s'il correspondait a un seul reversement ;
- formater la devise avec `Intl.NumberFormat`, apres normalisation du code
  `eur` en `EUR` ;
- ne pas recalculer de commission ni de frais Stripe dans l'application.

#### Dates

- `date_execution` : date de confirmation du transfer du reversement vers
  Stripe Connect ;
- `date_arrivee_estimee` : estimation Stripe, non garantie ;
- `date_dernier_evenement` : derniere information bancaire connue ;
- ne pas remplacer une date absente par la date courante ;
- afficher les dates dans le fuseau et le format local de l'utilisateur ;
- utiliser la formulation `Arrivee estimee` et non `Versement garanti le`.

#### Destination bancaire

- afficher uniquement `destination_masquee` lorsqu'elle est fournie ;
- ne jamais reconstituer ou demander un IBAN ;
- ne jamais mettre la destination masquee dans un champ editable ;
- si elle est absente, masquer entierement la ligne plutot qu'afficher une
  valeur technique.

#### Reference de tracage bancaire

`reference_tracage_bancaire` est deja filtree par le backend. Elle peut etre
retournee lorsqu'une action est requise ou apres le delai prevu pour un
virement annonce effectue mais non recu.

Lorsqu'elle est non nulle :

- afficher `Reference de recherche bancaire` ;
- proposer une action de copie ;
- expliquer qu'elle peut etre communiquee a la banque pour rechercher le
  virement ;
- ne jamais la journaliser dans les outils analytics ou les rapports d'erreur
  frontend.

### Chronologie a afficher

Chaque reversement doit presenter une chronologie composee au minimum de :

1. `Reversement transmis a Stripe`, derive de `date_execution` lorsque le
   reversement est `PAYE` ;
2. une ou plusieurs tentatives de virement bancaire issues de
   `virements_bancaires` ;
3. pour chaque tentative, son statut, son montant inclus, ses dates et son
   eventuelle action.

Le tableau backend est ordonne du plus recent au plus ancien. L'application
peut conserver cet ordre dans une liste de tentatives ou l'inverser dans une
frise chronologique, mais elle ne doit jamais fusionner plusieurs tentatives.

#### Aucun detail bancaire disponible

Lorsque `virements_bancaires` est vide :

- conserver l'information `Reversement transmis a Stripe` si le reversement
  est `PAYE` ;
- afficher un message neutre : `Les details du virement bancaire ne sont pas
  encore disponibles.` ;
- ne pas conclure a un echec ;
- ne pas afficher `Virement effectue` sans projection bancaire recue.

#### Plusieurs tentatives

Un premier virement peut echouer puis etre repropose par Stripe. Dans ce cas :

- afficher chaque tentative separement ;
- conserver l'echec historique ;
- mettre visuellement en avant la tentative la plus recente ;
- ne pas additionner les montants des tentatives comme s'ils avaient tous ete
  verses ;
- ne pas masquer un echec `paid` devenu `failed` lorsque le backend le
  reprojette en `ECHEC_VIREMENT`.

### Action requise et reprise Stripe

Lorsque `action_requise=true` :

- afficher un bouton principal `Mettre a jour mes informations bancaires` ;
- utiliser `lien_action` comme route de navigation interne ;
- le contrat actuel retourne `/stripe-connect/onboarding/refresh` ;
- cette page doit reutiliser le parcours EPIC 39 : demander un nouveau lien
  d'onboarding au backend puis rediriger vers Stripe ;
- ne jamais traiter `lien_action` comme une URL webhook ou une URL d'API ;
- apres le retour Stripe, resynchroniser le compte Connect selon l'EPIC 39,
  puis recharger l'historique des reversements.

Si `action_requise=true` mais `lien_action=null`, afficher le motif et proposer
le contact support sans inventer de lien Stripe.

### Notifications WebPush

Le backend peut creer une notification WebPush d'echec avec le contrat
suivant :

```json
{
  "type": "VIREMENT_BANCAIRE_ECHEC",
  "title": "Echec d'un virement bancaire",
  "body": "Une verification de vos informations bancaires peut etre necessaire.",
  "deeplink": "/reversements"
}
```

L'application doit :

- reconnaitre le type `VIREMENT_BANCAIRE_ECHEC` ;
- ouvrir `/reversements` au clic ;
- recharger les donnees depuis l'API plutot que se fier au contenu du push ;
- appliquer le parcours de session existant si l'utilisateur n'est plus
  authentifie ;
- ne jamais afficher de donnees bancaires ou de reference technique dans la
  notification systeme.

Le canal utilise actuellement la preference et l'abonnement WebPush deja mis
en place. Aucun nouveau secret ni nouvelle variable Stripe n'est necessaire
cote application.

### Evolutions a realiser dans l'application

#### 1. Couche API centralisee

- etendre le modele `ReversementEffectue` avec `virements_bancaires` ;
- ajouter les types enumeres du contrat ci-dessus ;
- normaliser `virements_bancaires ?? []` ;
- conserver l'appel existant a l'historique par nombre de mois ;
- ne pas creer de nouvel appel direct vers les routes finance
  `/protected/gestion-reversement/payouts` ; elles sont reservees au
  back-office et au scope `internal:finance`.

#### 2. Vue historique des reversements

- conserver les informations actuelles du reversement ;
- ajouter une section `Suivi du virement bancaire` ;
- afficher une synthese de la tentative la plus recente ;
- permettre de consulter les tentatives precedentes ;
- gerer explicitement le tableau vide et les valeurs nulles.

#### 3. Composants recommandes

- `VirementBancaireStatus` : badge accessible fonde sur `statut_code` ;
- `VirementBancaireTimeline` : chronologie des tentatives ;
- `VirementBancaireFailure` : motif public et action de regularisation ;
- `BankTraceReference` : affichage et copie de la reference autorisee ;
- `ReversementBankTransferSummary` : synthese integree a la ligne ou carte du
  reversement.

Ces noms sont indicatifs. L'application doit respecter son architecture de
composants existante et centraliser le mapping des statuts afin d'eviter des
libelles divergents entre les pages.

#### 4. Navigation

- rendre `/reversements` accessible depuis le dashboard et les notifications ;
- conserver `/stripe-connect/onboarding/refresh` comme route frontend ;
- apres regularisation Stripe, revenir vers l'historique ou proposer un bouton
  explicite `Voir mes reversements` ;
- ne pas inclure d'identifiant `po_...` dans l'URL publique.

#### 5. Accessibilite

- ne pas transmettre l'etat uniquement par la couleur ;
- associer icone, libelle et texte au statut ;
- annoncer les mises a jour asynchrones de la chronologie ;
- rendre l'action de copie utilisable au clavier ;
- fournir un retour visible apres copie de la reference bancaire.

### Etats UX a couvrir

#### Chargement

- afficher un squelette ou un etat de chargement local a la section ;
- eviter de masquer tout l'historique lors d'un rafraichissement en
  arriere-plan.

#### Erreur API

- conserver les donnees precedemment chargees si possible ;
- proposer `Reessayer` ;
- ne pas traduire une erreur reseau en echec de virement bancaire.

#### Session expiree

- utiliser le parcours de reconnexion existant ;
- reprendre ensuite la navigation vers `/reversements` ou le parcours Stripe
  demande.

#### Statut inconnu

Pour assurer la compatibilite ascendante, un code futur inconnu doit etre
affiche avec un style neutre et le `statut_libelle` fourni. L'application ne
doit ni planter ni convertir ce code en succes.

### Vocabulaire autorise

Libelles recommandes :

- `Reversement transmis a Stripe` ;
- `Suivi du virement bancaire` ;
- `Virement bancaire a venir` ;
- `Virement bancaire en cours` ;
- `Virement effectue` ;
- `Echec du virement bancaire` ;
- `Mettre a jour mes informations bancaires` ;
- `Arrivee estimee` ;
- `Reference de recherche bancaire`.

Libelles interdits dans l'interface commercant :

- `payout` ou `payout Stripe` ;
- `paid`, `failed`, `pending`, `in_transit` ;
- `rapprochement`, `NON_RAPPROCHE`, `NON_RAPPROCHABLE` ;
- `destination_payment` ;
- tout identifiant `po_...` ou `py_...` ;
- `IBAN invalide` lorsque le backend fournit une categorie publique plus
  generale ;
- toute promesse de date bancaire garantie.

Le terme `Transfer Stripe` peut rester utilise dans les zones EPIC 39 qui
expliquent l'etape technique vers le solde Connect, mais la nouvelle etape doit
etre nommee `virement bancaire`.

### Securite et confidentialite

- ne persister dans aucun stockage frontend que les donnees necessaires au
  fonctionnement courant ;
- ne pas envoyer `reference_tracage_bancaire`, `destination_masquee` ou
  `motif_echec` aux outils analytics ;
- ne pas inclure ces donnees dans les logs console, traces ou captures
  automatiques de rapports d'erreur ;
- ne pas proposer de formulaire de saisie bancaire Localeo ;
- ne pas exposer les routes internes finance ou batch ;
- conserver la verification que le commercant consulte uniquement ses propres
  reversements ;
- ne jamais embarquer `LOCALEO_STRIPE_SECRET_KEY`,
  `LOCALEO_STRIPE_WEBHOOK_SECRET` ou
  `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET` dans l'application.

### Plan d'implementation recommande

1. `EP43-APP-T01` Mettre a jour le contrat API central et les types.
2. `EP43-APP-T02` Ajouter le mapping accessible des sept statuts publics.
3. `EP43-APP-T03` Enrichir l'historique des reversements avec la synthese
   bancaire.
4. `EP43-APP-T04` Implementer la chronologie et les tentatives multiples.
5. `EP43-APP-T05` Implementer le parcours d'echec et la reprise onboarding
   Stripe.
6. `EP43-APP-T06` Gerer la reference de recherche bancaire et sa copie.
7. `EP43-APP-T07` Gerer le WebPush `VIREMENT_BANCAIRE_ECHEC` et son deeplink.
8. `EP43-APP-T08` Ajouter les tests unitaires, de contrat, d'accessibilite et
   de navigation.
9. `EP43-APP-T09` Mettre a jour la documentation API et la recette applicative.

### Strategie de tests

#### Tests de contrat

- la reponse sans `virements_bancaires` historique est normalisee en `[]` ;
- les sept codes `VIREMENT_*` sont acceptes ;
- les champs optionnels acceptent `null` ;
- un code futur inconnu ne provoque pas d'erreur de rendu ;
- aucun type frontend n'exige un identifiant technique non expose.

#### Tests de composants

- rendu de chaque statut public ;
- rendu sans date ni destination ;
- rendu d'un motif d'echec sans action ;
- rendu d'un echec avec action ;
- rendu et copie de la reference bancaire ;
- rendu de plusieurs tentatives sans addition des montants ;
- tableau vide avec message neutre ;
- verification des libelles accessibles sans dependance exclusive a la
  couleur.

#### Tests de parcours

- consultation d'un reversement transmis a Stripe sans detail bancaire ;
- virement a venir puis en cours ;
- virement effectue avec destination masquee ;
- virement effectue avec confirmation des details en cours ;
- details indisponibles ;
- virement annule ;
- virement en echec avec redirection vers le parcours Stripe ;
- premiere tentative en echec puis nouvelle tentative effectuee ;
- clic WebPush avec session active ;
- clic WebPush apres expiration de session ;
- erreur API pendant un rafraichissement.

#### Controle du vocabulaire

Ajouter un test ou une verification statique sur les contenus destines au
commercant afin d'interdire les termes techniques `payout`, `paid`, `failed`,
`NON_RAPPROCHE`, ainsi que les motifs `po_` et `py_`.

### Recette fonctionnelle

La recette doit au minimum verifier :

1. un reversement `PAYE` sans virement rapproche ;
2. un virement automatique `pending` ;
3. un virement `in_transit` avec date estimee ;
4. un virement `paid` rapproche ;
5. un virement `paid` dont les details sont encore en cours ;
6. un virement `failed` avec motif public et action ;
7. un passage tardif de virement effectue a echec ;
8. plusieurs reversements inclus dans un virement groupe ;
9. plusieurs tentatives pour un meme reversement ;
10. l'absence de toute donnee bancaire complete ou de terme technique dans
    l'interface.

### Definition of Done application commercant

L'impact EPIC 43 peut etre considere termine lorsque :

- la couche API consomme `virements_bancaires` de maniere additive ;
- l'historique distingue le transfer Stripe Connect et le virement bancaire ;
- les sept statuts publics sont rendus avec des libelles accessibles ;
- le montant affiche correspond a la part du reversement incluse et non au
  montant total d'un virement groupe ;
- plusieurs tentatives restent distinctes ;
- un tableau vide n'est jamais presente comme un echec ;
- les dates estimees ne sont pas presentees comme garanties ;
- les valeurs nulles et les codes futurs sont toleres ;
- une action requise permet de reprendre le parcours Stripe Connect EPIC 39 ;
- le WebPush d'echec ouvre `/reversements` et provoque un rechargement API ;
- la reference bancaire n'est affichee que lorsqu'elle est fournie ;
- aucune donnee sensible n'est envoyee aux logs ou analytics ;
- aucun terme technique interdit n'apparait dans l'interface ;
- les tests de contrat, composants, navigation et accessibilite passent ;
- la recette Stripe Test couvre succes, echec, tentative multiple et virement
  groupe.

### Limites backend connues pour la premiere integration

- le calcul d'absence de virement utilise encore les seuils de repli J+7 et
  J+10 ouvrables ; le calendrier bancaire Stripe cible sera integre dans une
  evolution backend ulterieure ;
- les alertes d'absence sont destinees au back-office et ne constituent pas un
  nouveau statut frontend ;
- l'application ne dispose pas d'une route commercant autonome de detail par
  virement : la source publique reste l'historique des reversements ;
- les routes `/protected/gestion-reversement/payouts/**` sont reservees aux
  usages finance et batch et ne doivent pas etre consommees par l'application.
