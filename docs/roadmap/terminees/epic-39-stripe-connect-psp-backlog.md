# Epic 39 - Delegation des flux financiers a Stripe Connect

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : couvrir de bout en bout la delegation des paiements et reversements Localeo a Stripe Connect, depuis le paiement client jusqu'a l'eligibilite au transfer apres validation QR puis l'execution bimensuelle pilotee par Localeo, en conservant les objets internes de paiement/reversement comme projections metier alimentees par Stripe.
- PSP cible : `Stripe Connect`
- Modele cible : `separate charges and transfers`
- Mode Connect cible : `Express`
- Decision produit : le paiement client est traite par Stripe Connect sur le compte plateforme Stripe Localeo ; une prestation validee rend le montant transferable, mais les transfers vers les comptes connectes commercants restent declenches par Localeo lors de campagnes bimensuelles de reversement.
- Decision commercialisation : un coffret n'est vendable que si tous les commercants rattaches a ses prestations disposent d'un compte connecte Stripe eligible aux transfers ; si l'eligibilite Stripe se degrade apres achat, le reversement est bloque jusqu'a regularisation Stripe.
- Decision technique : chaque paiement porte un `transfer_group` stable au format canonique `achat:{achat_id}` ; `commande:{achat_id}` ne doit etre retenu que si le vocabulaire metier bascule explicitement d'achat vers commande.
- Decision technique : les transfers exigent `source_transaction` afin de rattacher le reversement a la charge d'origine ; la campagne repare la reference via `PaymentIntent.latest_charge` ou bloque l'appel Stripe.
- Decision conformite : les fonds clients destines aux commercants ne doivent pas transiter par un compte bancaire propre Localeo ; les virements, reversements, exports bancaires et confirmations manuelles sont completement decommissionnes dans la cible, sans fallback manuel ni mecanisme de retrocompatibilite operationnelle.
- Decision juridique cible : Localeo est une plateforme numerique d'intermediation exploitant une marketplace locale de services ; elle agit comme operateur de plateforme en ligne et mandataire d'encaissement pour le compte de commercants partenaires, sous reserve de validation juridique finale.
- Decision economique : Localeo gere les tarifs Stripe Connect, porte les frais Stripe, y compris les frais mensuels par compte actif, et les integre dans son modele de commission.
- Decision remboursement : apres transfer Stripe execute, la prestation est consideree executee et non remboursable par defaut ; les demandes sont traitees comme litiges, sans mecanisme de remboursement automatique.
- Decision migration : l'application n'etant pas en production, les reversements manuels peuvent etre supprimes plutot que migres en compatibilite historique.
- Decision calendrier : les campagnes bimensuelles sont executees le 1er et le 15 de chaque mois a 22h00, quel que soit le jour calendaire.
- Decision d'architecture : Stripe devient la source d'execution financiere ; les objets internes `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` restent le modele metier/back-office Localeo, mais sont alimentes par les notifications Stripe ou declenchent des operations Stripe.
- Extension : le suivi du virement bancaire (`payout` Stripe) depuis le solde Stripe connecte jusqu'au compte bancaire du commercant est porte par [l'EPIC 43](epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md), sans rouvrir le perimetre termine des Transfers de cette epic.

## Documents d'architecture

- [Architecture applicative EPIC 39 - Delegation des flux financiers a Stripe Connect](../../architecture/backend/epics/epic-39-stripe-connect-architecture.md)
- [ADR-2026-07-09 - Decisions d'implementation EPIC 39 Stripe Connect](../../architecture/decisions/ADR-2026-07-09-epic-39-stripe-connect-implementation.md)

## Documents juridiques et contractuels

- Annexe contractuelle - Flux financiers Stripe Connect — source historique non retrouvée (`annexe-flux-financiers-stripe-connect.md` ; voir [le registre des sources absentes](../../organisation/sources-historiques-absentes.md))

## Decisions d'implementation actees

Les recommandations d'implementation sont actees par l'ADR EPIC 39 et doivent
guider le decoupage des tickets techniques :

- l'integration Stripe Connect est protegee par le feature flag
  `LOCALEO_FEATURE_STRIPE_CONNECT_ENABLED` ;
- les variables de configuration cibles sont `LOCALEO_STRIPE_SECRET_KEY`,
  `LOCALEO_STRIPE_WEBHOOK_SECRET`,
  `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET`,
  `LOCALEO_STRIPE_ONBOARDING_RETURN_URL` et
  `LOCALEO_STRIPE_ONBOARDING_REFRESH_URL` ;
- les URLs `LOCALEO_STRIPE_ONBOARDING_RETURN_URL` et
  `LOCALEO_STRIPE_ONBOARDING_REFRESH_URL` pointent vers l'application
  commercant, pas vers le back-office ni vers une route interne ;
- les noms historiques `STRIPE_API_KEY` et `STRIPE_WEBHOOK_SECRET` doivent etre
  migres vers ces noms cibles ou documentes comme alias techniques transitoires ;
- le developpement peut demarrer en environnement Stripe test dedie, mais
  l'activation production reste interdite sans go/no-go juridique, finance et
  conformite PSP ;
- la strategie de migration est one-shot : l'application n'etant pas en
  production sur ces flux, les anciens parcours manuels sont supprimes plutot
  que conserves en compatibilite ;
- les statuts cibles des mouvements sont `A_CALCULER`, `TRANSFERABLE`,
  `BLOQUE_ONBOARDING_STRIPE`, `EN_CAMPAGNE`, `TRANSFER_DEMANDE`,
  `TRANSFER_CONFIRME`, `ECHEC_TRANSFER` et `ANNULE` ;
- l'implementation commence par un lot technique 0 : modele interne, ports
  applicatifs Stripe, journal minimal d'operations, idempotence, feature flag et
  inventaire de decommissionnement des flux manuels.

### Etat d'implementation code

- 2026-07-09 : les endpoints API de creation/execution de reversement manuel
  sont retires ; seul `POST /protected/gestion-reversement/reversements/campagnes-stripe/lancer`
  reste expose pour declencher les transfers.
- 2026-07-09 : les routes back-office internes de generation de reversements,
  preparation de lots, export CSV et confirmation/echec manuel sont retirees.
- 2026-07-09 : le back-office pilote les reversements via la vision 360 et le
  lancement de campagne Stripe Connect.
- 2026-07-09 : les anciens use cases applicatifs de reversement manuel sont
  retires du code ; les statuts manuels `A_INITIER`, `EN_COURS_MANUEL` et le
  mode `MANUEL_BANQUE` ne sont plus des valeurs de domaine produisibles.
- 2026-07-09 : les routes commercant d'onboarding Stripe Connect sont exposees
  sous `/protected/referencement/commercants/me/stripe-connect`, avec creation
  de lien d'onboarding et resynchronisation du compte connecte.
- 2026-07-09 : l'initialisation paiement refuse un coffret contenant une
  prestation d'un commercant non eligible Stripe Connect lorsque le flux Stripe
  Connect est actif.
- 2026-07-14 : le controle PRD-308B est mutualise entre paiement et
  back-office ; la publication d'un coffret ou d'une prestation non reversable
  est refusee avec motif detaille, l'indicateur `Vendabilite Stripe` affiche le
  commercant concerne, et la vendabilite est recalculee apres regularisation
  Stripe synchronisee.
- 2026-07-09 : la validation QR cree un `MouvementReversement` `TRANSFERABLE`
  si le compte connecte est eligible, `BLOQUE_ONBOARDING_STRIPE` sinon, et ne
  cree jamais de transfer Stripe immediat. Lorsque Stripe Connect est inactif,
  un nouveau mouvement reste `A_CALCULER` et ne retombe plus sur le statut
  historique `A_REVERSER`.
- 2026-07-11 : les campagnes Stripe Connect verifient l'existence d'un
  `PaiementReversement` portant la meme cle d'idempotence metier avant toute
  creation de transfer, afin d'eviter de doubler un flux financier deja demande
  ou confirme.

## Probleme

La chaine financiere actuelle porte des objets internes de paiement et reversement, avec une part importante de pilotage manuel. Localeo doit evoluer vers Stripe Connect pour fiabiliser le paiement client, l'onboarding financier des commercants, les transfers apres execution de prestation, les reprises d'incident et le rapprochement operationnel.

La cible conserve les objets internes de paiement et reversement, mais change leur role. Ils ne pilotent plus un processus manuel banque : ils deviennent des projections metier et back-office des operations Stripe. Stripe porte l'execution financiere ; Localeo conserve `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` pour relier les operations Stripe aux achats, coffrets, validations, commercants, remboursements, support, audit et pilotage finance.

L'enjeu n'est pas seulement de remplacer un appel de paiement. L'epic doit couvrir toute la chaine :
- creation et suivi des comptes connectes commercants ;
- paiement client ;
- rattachement paiement / commande / coffret ;
- validation QR ;
- constitution des mouvements transferables ;
- pilotage bimensuel des transfers ;
- remboursement ;
- webhooks Stripe ;
- back-office finance ;
- audit, idempotence et reprise.

## Objectif operationnel

Permettre a Localeo de vendre un coffret, d'initialiser le paiement client via Stripe Connect sur le compte plateforme Stripe Localeo, sans transit des fonds commercants par les comptes bancaires propres Localeo, puis de rendre les fonds transferables des la validation QR effective. L'execution du reversement commercant reste pilotee par Localeo via des campagnes bimensuelles, qui creent les transfers Stripe vers les comptes connectes eligibles.

## Perimetre MVP

- Creer et suivre les comptes connectes Stripe des commercants.
- Utiliser des comptes Connect de type `Express`.
- Stocker le lien entre `Commercant` et `stripe_account_id`.
- Gerer l'etat d'onboarding Stripe Connect et les blocages de capacite de paiement ou de transfer.
- Bloquer la publication ou la vente d'un coffret si une prestation rattachee depend d'un commercant sans compte connecte Stripe eligible.
- Initialiser les paiements clients via Stripe.
- Parametrer le modele `separate charges and transfers`.
- Associer chaque paiement client a un `transfer_group` stable au format canonique `achat:{achat_id}`.
- Conserver les references Stripe utiles : Checkout Session, PaymentIntent, Charge, Customer si applicable.
- Ne creer aucun transfer Stripe au moment du paiement client.
- Creer un `MouvementReversement` apres validation QR d'une prestation ; il n'est transferable que si le compte connecte Stripe du commercant est eligible.
- Placer un mouvement en statut bloque, par exemple `BLOQUE_ONBOARDING_STRIPE`, si le compte connecte Stripe devient incomplet ou non eligible apres l'achat.
- Creer les transfers Stripe uniquement dans le cadre d'une campagne de reversement pilotee par Localeo, avec une frequence cible bimensuelle.
- Rattacher chaque transfer au commercant beneficiaire, a la prestation validee, au paiement d'origine et au `transfer_group`.
- Exiger `source_transaction` et reparer la charge d'origine depuis le paiement avant tout appel de transfer.
- Gerer les remboursements Stripe en distinguant les cas avant et apres transfer.
- Garantir l'idempotence des creations de comptes connectes, paiements, transfers, remboursements et traitements webhook.
- Synchroniser les statuts Stripe utiles par webhooks verifies.
- Exposer les blocages et echecs Stripe dans le back-office finance.
- Conserver `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` comme objets metier internes.
- Alimenter ces objets depuis les webhooks Stripe et les commandes Stripe initiees par le backend.
- Supprimer les lots de paiement bancaire, exports manuels, confirmations de virement et reversements manuels des parcours operationnels cibles.
- Documenter et faire valider la qualification juridique du modele Stripe Connect retenu.
- Documenter l'invariant de flux financier cible : aucun fonds commercant ne transite par un compte bancaire propre Localeo.
- Documenter le mecanisme de cantonnement, segregation ou protection des fonds applicable chez Stripe, ou identifier le risque residuel a faire arbitrer.
- Aligner les contrats, mandats, CGV, factures et libelles back-office avec le role reel de Localeo dans le modele PSP cible.

## Hors perimetre MVP

- Payout instantane ou calendrier de payout avance par commercant.
- Execution automatique immediate du transfer Stripe au moment de la validation QR.
- Marketplace multi-devises.
- Comptabilite analytique complete.
- Rapprochement comptable automatise avance avec Stripe Sigma.
- Gestion avancee des litiges et chargebacks.
- Rejeu operationnel ou retrocompatibilite des anciens use cases de paiement manuel.
- Conservation d'un historique manuel de production : non applicable a date, l'application n'etant pas en production.
- Suppression des objets internes `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` comme modele metier/back-office.
- Modele `destination charges` comme cible principale.
- Transfers avant validation QR.

## User Stories

1. `PRD-307` En tant qu'operateur back-office, je veux creer ou rattacher un compte connecte Stripe a un commercant afin de le rendre eligible aux reversements PSP.
   - Statut : `Termine`
   - Resultat attendu : un commercant peut porter un `stripe_account_id` unique.
   - Resultat attendu : la creation est idempotente et ne cree pas plusieurs comptes Stripe pour le meme commercant.
   - Resultat attendu : l'action est auditee avec le commercant, l'operateur et l'identifiant Stripe.
   - Implementation : `2026-07-14` - creation idempotente, rattachement back-office d'un compte `acct_...` existant avec controle d'unicite et journalisation `operations_stripe`.

2. `PRD-308` En tant que commercant, je veux finaliser mon onboarding Stripe Connect afin de pouvoir recevoir les reversements Localeo.
   - Statut : `Termine`
   - Resultat attendu : le backend peut generer un lien d'onboarding Stripe.
   - Resultat attendu : le statut d'onboarding, les exigences Stripe et les capacites requises sont synchronises.
   - Resultat attendu : un commercant non eligible est visible comme bloque dans le pilotage finance.
   - Resultat attendu : une documentation detaillee du processus d'onboarding commercant est produite et maintenue.
   - Resultat attendu : la documentation couvre les pre-requis, les etapes Stripe, les responsabilites Localeo/commercant/Stripe, les donnees collectees, les statuts, les blocages, les reprises et les impacts sur les reversements.
   - Implementation : `2026-07-14` - synchronisation API et webhook `account.updated`, action back-office de synchronisation, procedure operationnelle [docs/ops/exploitation/onboarder-commercant-stripe-connect.md](../../exploitation/exploitation/onboarder-commercant-stripe-connect.md).

2B. `PRD-308B` En tant que responsable commercialisation, je veux bloquer la vente d'un coffret contenant une prestation d'un commercant non eligible Stripe Connect afin d'eviter de vendre des prestations non reversables.
   - Statut : `Termine`
   - Resultat attendu : la publication ou la mise en vente d'un coffret verifie l'eligibilite Stripe Connect de tous les commercants rattaches aux prestations du coffret.
   - Resultat attendu : un coffret contenant au moins une prestation rattachee a un commercant sans compte connecte Stripe eligible est marque non vendable ou bloque a la publication.
   - Resultat attendu : le back-office affiche le motif de blocage et le commercant concerne.
   - Resultat attendu : la regularisation Stripe Connect du commercant permet de reevaluer automatiquement ou manuellement la vendabilite du coffret.
   - Implementation : `2026-07-14` - controle de vendabilite Stripe Connect mutualise, blocage paiement avec motif detaille, blocage publication coffret/prestation dans le back-office, indicateur `Vendabilite Stripe` et reevaluation dynamique apres synchronisation Stripe.

3. `PRD-309` En tant que systeme de paiement, je veux initialiser les paiements client selon le modele `separate charges and transfers` afin que Stripe Connect traite le paiement sur le compte plateforme Stripe Localeo.
   - Statut : `Termine`
   - Resultat attendu : le paiement est cree chez Stripe sur le compte plateforme Stripe Localeo.
   - Resultat attendu : le paiement est rattache a `AchatCoffret`, aux coffrets instances concernes et au client lorsque disponible.
   - Resultat attendu : aucun transfer automatique vers un compte connecte n'est cree au paiement.
   - Resultat attendu : la configuration Stripe ne repose pas sur `destination charge`.
   - Implementation : `2026-07-14` - Checkout cree un PaymentIntent cote plateforme sans `transfer_data`, `destination` ni `application_fee_amount`; aucun transfer Stripe n'est cree au paiement.

4. `PRD-310` En tant que systeme, je veux associer chaque paiement a un `transfer_group` stable `achat:{achat_id}` afin de relier la charge Stripe a l'achat et aux futurs transfers.
   - Statut : `Termine`
   - Resultat attendu : le `transfer_group` est determine des l'initialisation du paiement.
   - Resultat attendu : le meme groupe est reutilise pour tous les transfers issus de la commande.
   - Resultat attendu : le format canonique du groupe est `achat:{achat_id}`.
   - Implementation : `2026-07-14` - le gateway paiement force le `transfer_group` canonique `achat:{achat_id}` dans la Checkout Session et dans `payment_intent_data`, et le webhook reprojette toujours cette valeur canonique.

5. `PRD-311` En tant que systeme, je veux conserver les references Stripe du paiement d'origine afin de supporter reversements, remboursements, support et rapprochement.
   - Statut : `Termine`
   - Resultat attendu : Checkout Session, PaymentIntent, Charge et Customer sont conserves quand disponibles.
   - Resultat attendu : les references sont rattachees a l'achat, au coffret instance lorsque pertinent, a l'objet `Paiement` et au journal evenementiel Stripe.
   - Resultat attendu : les references sensibles ne sont pas exposees dans les logs ou surfaces publiques.
   - Implementation : `2026-07-14` - persistance `stripe_checkout_session_id`, `stripe_payment_intent_id`, `stripe_charge_id`, `stripe_customer_id`, `transfer_group` et metadonnees Stripe; la reconciliation Checkout recupere PaymentIntent, Charge et Customer via expansions Stripe et enrichit les paiements existants.

6. `PRD-312` En tant que systeme de validation, je veux rendre un montant transferable uniquement apres validation QR et eligibilite Stripe Connect afin que le commercant soit reverse apres execution effective de la prestation et compte connecte conforme.
   - Statut : `Termine`
   - Resultat attendu : la validation QR reste la condition declenchante de l'eligibilite au reversement PSP.
   - Resultat attendu : la validation cree ou confirme un `MouvementReversement`, rattache a la prestation validee, au commercant, au paiement d'origine et au `transfer_group`.
   - Resultat attendu : si le compte connecte Stripe est eligible, le mouvement devient transferable.
   - Resultat attendu : si le compte connecte Stripe est incomplet, bloque ou non eligible, le mouvement passe en statut bloque type `BLOQUE_ONBOARDING_STRIPE` et n'entre pas en campagne.
   - Resultat attendu : aucun transfer Stripe n'est cree immediatement si la campagne bimensuelle de reversement n'est pas lancee.
   - Resultat attendu : un rejeu de validation ou de webhook ne cree pas de double mouvement transferable.
   - Implementation : `2026-07-14` - la validation QR cree un mouvement `TRANSFERABLE` uniquement si le commercant est eligible Stripe Connect, sinon `BLOQUE_ONBOARDING_STRIPE`; aucun transfer Stripe n'est appele dans le chemin de validation; l'idempotence repose sur la cle stable `mouvement:statut-prestation:{statut_id}` et le rejeu retourne le mouvement existant.

7. `PRD-312B` En tant que responsable finance, je veux piloter les transfers Stripe de maniere bimensuelle afin de conserver la maitrise operationnelle du reversement commercant.
   - Statut : `Termine`
   - Resultat attendu : les mouvements transferables sont selectionnables dans une campagne de reversement bimensuelle.
   - Resultat attendu : Localeo peut controler les blocages, montants et comptes connectes avant creation des transfers Stripe.
   - Resultat attendu : la campagne cree les `Reversement` et `PaiementReversement` cibles, puis les transfers Stripe idempotents.
   - Resultat attendu : le back-office distingue les mouvements transferables, les transfers demandes, les transfers confirmes et les echecs.
   - Implementation : `2026-07-14` - la campagne Stripe selectionne les mouvements `TRANSFERABLE` et les reprises `ECHEC_TRANSFER`, cree les `Reversement` et `PaiementReversement` pour les nouveaux mouvements, et bloque les mouvements non tracables avant appel Stripe.

8. `PRD-313` En tant que responsable finance, je veux que chaque transfer utilise `source_transaction` afin de rattacher le reversement a la charge client d'origine.
   - Statut : `Termine`
   - Resultat attendu : le backend conserve la reference de charge Stripe exploitable pour `source_transaction`.
   - Resultat attendu : si la charge d'origine est absente, le backend la resout via `PaymentIntent.latest_charge`, la persiste et bloque le transfer si elle reste introuvable.
   - Resultat attendu : le transfer conserve le `transfer_group` dans tous les cas.
   - Implementation : `2026-08-12` - le transfer Stripe exige le `transfer_group` et la `source_transaction` du paiement d'origine ; la campagne repare les references manquantes depuis le paiement ou `PaymentIntent.latest_charge`, propage les webhooks tardifs vers les mouvements existants et n'appelle pas Stripe si la charge reste introuvable. La piste `OperationStripe` utilise la cle de requete Stripe effective et met a jour une operation existante lors d'une reprise, sans insertion dupliquee.

9. `PRD-314` En tant que systeme, je veux synchroniser les webhooks Stripe afin de suivre paiement, onboarding, transfer, remboursement et echec.
   - Statut : `Termine`
   - Resultat attendu : les webhooks sont verifies par signature.
   - Resultat attendu : les evenements sont traites de maniere idempotente.
   - Resultat attendu : les projections locales et le journal minimal d'operations Stripe sont mis a jour sans exposer de donnees sensibles.
   - Implementation : `2026-08-07` - deux destinations sont separees par source : le webhook plateforme `/public/stripe/webhook` synchronise `transfer.*`, `checkout.session.*`, `payment_intent.*`, `charge.*` et `refund.*` ; le webhook comptes connectes `/public/stripe-connect/webhook` traite uniquement `account.updated`. Chaque destination verifie son propre secret de signature et les evenements financiers restent dedoublonnes par `stripe-connect:webhook:{event_id}` puis journalises dans `operations_stripe` avec rattachement metier quand disponible.

10. `PRD-315` En tant qu'operateur finance, je veux voir les paiements, mouvements transferables et transfers Stripe dans la vision finance afin de suivre ce qui est en attente, execute, rembourse ou en echec.
   - Statut : `Termine`
   - Resultat attendu : les vues finance affichent les montants, commercants, prestations, `transfer_group`, statut Stripe et references Stripe.
   - Resultat attendu : les blocages onboarding, echecs de paiement et echecs de transfer sont visibles.
   - Resultat attendu : aucune action de reversement manuel, export bancaire ou confirmation bancaire n'est disponible dans les vues finance cibles.
   - Implementation : `2026-07-14` - la Vision 360 reversements expose les mouvements transferables, transfers en attente/confirmes/echec, blocages Stripe Connect, frais PSP par flux, controles avocat/finance/exploitation et export CSV enrichi pour validation runtime avec donnees Stripe simulees.

11. `PRD-316` En tant que responsable exploitation, je veux pouvoir rejouer ou reprendre un paiement ou transfer en echec sans doubler un flux financier afin de securiser les incidents Stripe.
    - Statut : `Termine`
    - Resultat attendu : chaque operation Stripe porte une cle d'idempotence metier.
    - Resultat attendu : une reprise conserve l'historique de l'echec precedent.
    - Resultat attendu : un transfer deja reussi ne peut pas etre recree pour la meme validation.
    - Implementation : `2026-07-14` - la cle `stripe:transfer:mouvement:{mouvement_id}` est reutilisee en reprise ; un `PaiementReversement` en echec est remis en demande sans creation de doublon, tandis qu'un transfer deja demande/confirme est detecte et non recree.

12. `PRD-317` En tant que support Localeo, je veux gerer les remboursements Stripe en tenant compte des transfers deja effectues afin de traiter proprement les annulations et incidents client.
    - Statut : `Termine`
    - Resultat attendu : un remboursement avant transfer et une demande post-transfer traitee comme litige sont distingues.
    - Resultat attendu : les contraintes Stripe sont visibles dans le back-office.
    - Resultat attendu : le lien entre remboursement client, paiement d'origine et transfers commercants reste auditable.
    - Implementation : `2026-07-14` - l'action back-office de remboursement Stripe classe les demandes post-transfer en litige sans appeler automatiquement Stripe, execute les refunds avant transfer avec idempotence, annule les mouvements transferables non encore transferes, expose les contraintes Stripe dans la fiche remboursement et journalise le lien paiement -> remboursement -> transfer dans `operations_stripe`.

13. `PRD-318` En tant que responsable finance, je veux suivre les frais Stripe afin d'analyser la rentabilite reelle des paiements et reversements.
    - Statut : `Termine`
    - Resultat attendu : les frais connus sur paiement, transfer ou remboursement sont conserves quand Stripe les expose.
    - Resultat attendu : les calculs de rentabilite peuvent distinguer montant client, montant reverse, frais PSP et marge Localeo.
    - Resultat attendu : le back-office peut simuler et afficher commission Localeo brute, frais Stripe estimes ou reels, et commission Localeo nette.
    - Implementation : `2026-07-14` - conservation des references de balance transaction Stripe et des montants de frais/net exposes sur les paiements client, transfers Stripe Connect et remboursements ; calcul de commission Localeo brute et nette estimee ; exposition back-office et Vision 360 finance.
    - Validation runtime : `2026-07-14` - ajout d'un test de rendu avec donnees Stripe simulees verifiant l'affichage HTML et l'export CSV des frais PSP, commissions et nets transfers.

14. `PRD-366` En tant que responsable juridique et finance, je veux qualifier le role de Localeo dans le modele Stripe Connect afin de limiter le risque d'exercice non autorise d'une activite de prestataire de services de paiement.
    - Statut : `Termine`
    - Resultat attendu : le modele retenu decrit clairement qui encaisse, qui detient les fonds, qui execute les transfers et quel est le role de Localeo.
    - Resultat attendu : le besoin ou l'absence de besoin d'enregistrement ACPR, d'agent PSP ou de distributeur PSP est documente par une validation juridique.
    - Resultat attendu : les ecarts entre le modele cible et les contrats existants sont listes avec une decision de correction.
    - Resultat attendu : une annexe contractuelle dediee aux flux Stripe Connect est produite pour relecture et annexion aux CGV ou au contrat commercant.

15. `PRD-367` En tant que responsable finance, je veux prouver que les fonds destines aux commercants ne transitent pas par les comptes bancaires propres Localeo afin de reduire le risque lie au mandat d'encaissement historique.
    - Statut : `Termine`
    - Resultat attendu : les flux paiement, balance Stripe, transfer, payout et compte bancaire sont cartographies.
    - Resultat attendu : le modele cible interdit tout virement des fonds commercants vers un compte bancaire propre Localeo avant reversement.
    - Resultat attendu : aucun fallback manuel banque n'est autorise ; un blocage Stripe ou onboarding suspend le reversement jusqu'a resolution via Stripe.
    - Resultat attendu : l'annexe contractuelle mentionne explicitement l'absence de transit par les comptes bancaires propres Localeo dans le flux nominal.

16. `PRD-368` En tant que responsable juridique, je veux documenter le mecanisme de cantonnement, segregation ou protection des fonds applicable chez Stripe afin de qualifier le risque de perte des creances commercants.
    - Statut : `Termine`
    - Resultat attendu : les elements contractuels ou documentaires Stripe utiles sont references dans le dossier de conformite.
    - Resultat attendu : le traitement d'une defaillance de Localeo entre paiement client et transfer commercant est analyse.
    - Resultat attendu : les limites ou risques residuels sont explicites et soumis a arbitrage.
    - Resultat attendu : l'annexe contractuelle identifie les points de validation Stripe/juridique sur balances, reserves, transfers, payouts et protection des fonds.

17. `PRD-369` En tant que responsable produit, je veux aligner les documents contractuels et les libelles produit avec le modele PSP cible afin d'eviter une contradiction entre le fonctionnement reel et les engagements contractuels.
    - Statut : `Termine`
    - Resultat attendu : mandat de facturation/encaissement, CGV, contrat commercant, factures et mentions back-office sont audites.
    - Resultat attendu : les termes `encaissement`, `reversement`, `mandat`, `compte plateforme` et `transfer` sont valides avec le conseil juridique.
    - Resultat attendu : aucune communication ne laisse entendre que Localeo conserve les fonds commercants sur ses comptes bancaires propres si ce n'est pas le modele juridiquement valide.

18. `PRD-370` En tant que responsable produit et technique, je veux requalifier les objets internes de paiement/reversement afin qu'ils soient alimentes par Stripe et ne pilotent plus d'operations manuelles.
    - Statut : `Termine`
    - Resultat attendu : `Paiement` est cree ou synchronise depuis Checkout Session, PaymentIntent, Charge et les webhooks Stripe.
    - Resultat attendu : `MouvementReversement` represente l'obligation metier issue d'une validation QR et porte les references Stripe utiles au transfer.
    - Resultat attendu : `Reversement` represente le regroupement ou suivi metier des mouvements a transferer via Stripe, sans preparation de virement bancaire manuel.
    - Resultat attendu : `PaiementReversement` represente l'execution Stripe du reversement, par exemple transfer ou payout selon le modele retenu, et non une saisie bancaire manuelle.
    - Resultat attendu : les donnees et parcours de reversement manuel sont supprimes, l'application n'etant pas en production.
    - Resultat attendu : aucune vue back-office cible ne depend d'un lot bancaire manuel pour executer un paiement commercant.
    - Resultat attendu : les anciens use cases de paiement manuel sont retires des surfaces operationnelles sans archive applicative de retrocompatibilite.
    - Implementation : `2026-07-14` - les routes d'export/confirmation/generation bancaire manuelle restent absentes, les vues back-office visibles sont limitees aux projections Stripe (`Paiement`, `MouvementReversement`, `Reversement`, `PaiementReversement`), la documentation operationnelle pointe vers Stripe Connect et les libelles residuels de virement bancaire ont ete remplaces par des references de transfer Stripe.

## Regles de gestion

- Stripe Connect est le PSP cible de l'epic.
- Le modele cible est `separate charges and transfers`, pas `destination charges`.
- Le type de compte Connect cible est `Express`.
- Localeo gere les tarifs Stripe Connect et porte les frais Stripe, y compris les frais mensuels par compte actif.
- Un commercant ne peut recevoir un transfer Stripe que s'il dispose d'un compte connecte eligible.
- Le compte connecte Stripe est rattache au `Commercant`, pas a une prestation isolee.
- Un coffret ne peut pas etre publie ou vendu si l'une de ses prestations reference un commercant sans compte connecte Stripe eligible aux transfers.
- Le paiement client est traite par Stripe Connect sur le compte plateforme Stripe Localeo.
- Les fonds destines aux commercants ne doivent pas transiter par un compte bancaire propre Localeo dans le modele cible.
- Le vocabulaire produit et contractuel doit distinguer compte plateforme Stripe, balance Stripe, compte connecte commercant et compte bancaire propre Localeo.
- Le paiement client doit conserver les references Stripe necessaires au rapprochement : Checkout Session, PaymentIntent, Charge, Customer si disponible.
- Le `transfer_group` est cree des l'initialisation du paiement et reste stable.
- Le format canonique du `transfer_group` est `achat:{achat_id}` ; `commande:{achat_id}` ne peut etre retenu que si le vocabulaire metier remplace explicitement `achat` par `commande`.
- Aucun transfer commercant n'est cree au moment du paiement client si la prestation n'est pas encore validee.
- Une validation QR cree l'obligation metier de reversement ; le mouvement ne devient transferable que si le compte connecte Stripe du commercant est eligible.
- Si le compte connecte Stripe est incomplet, bloque ou non eligible apres l'achat, le mouvement est cree en statut `BLOQUE_ONBOARDING_STRIPE` et reste exclu des campagnes de reversement.
- La regularisation Stripe Connect requalifie les mouvements bloques comme transferables lors d'une synchronisation webhook ou d'une resynchronisation back-office.
- Un transfer Stripe n'est cree que pour un mouvement transferable et uniquement lors d'une campagne de reversement pilotee par Localeo.
- La frequence cible de pilotage des campagnes de reversement est bimensuelle.
- Un transfer correspond a une obligation de reversement issue d'une prestation validee et selectionnee dans une campagne.
- Le montant du transfer est calcule par les regles metier Localeo existantes, notamment le montant de reversement de la prestation dans le coffret.
- Aucun montant de transfer n'est saisi librement au moment de la validation.
- Le transfer doit pointer vers le compte connecte du commercant beneficiaire.
- `source_transaction` est obligatoire ; une charge d'origine introuvable bloque le transfer avant appel Stripe.
- Le `transfer_group` est obligatoire meme si `source_transaction` n'est pas utilisable.
- La creation de compte connecte, paiement, transfer, remboursement et traitement webhook doit etre idempotente.
- Les webhooks Stripe synchronisent l'etat d'une operation, mais ne remplacent pas les decisions metier Localeo.
- Les objets internes `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` restent dans le modele cible.
- Ces objets ne declenchent plus de virement bancaire manuel ni d'export bancaire dans le chemin nominal.
- Ces objets portent les references Stripe, statuts synchronises, cles d'idempotence et evenements d'audit necessaires au support et au pilotage.
- Les flux manuels banque sont completement decommissionnes des parcours operationnels cibles.
- L'application n'etant pas en production, les reversements manuels existants peuvent etre supprimes dans la migration cible plutot que conserves en retrocompatibilite.
- La qualification juridique du modele PSP et le mecanisme de protection des fonds doivent etre valides avant mise en production du flux cible.

## Conformite PSP, cantonnement et preuves attendues

Cette section ne constitue pas un avis juridique. Elle cadre les elements produit, techniques et operationnels a documenter pour permettre la validation par le conseil juridique, la finance et Stripe.

### Risques couverts

- Risque d'exercice non autorise d'une activite de prestataire de services de paiement si Localeo encaisse des fonds clients sur ses comptes bancaires propres avant de les reverser aux commercants.
- Risque d'absence de cantonnement, segregation ou protection des fonds destines aux commercants entre le paiement client et le transfer ou payout commercant.
- Risque de contradiction entre le fonctionnement cible Stripe Connect et les documents existants de mandat, CGV, contrat commercant ou facturation.

### Invariants produit

- Stripe Connect est la couche d'execution des paiements, transfers, remboursements et payouts.
- Localeo orchestre les decisions metier : vente du coffret, validation QR, calcul du montant transferable, campagne bimensuelle de reversement, audit et support.
- Localeo ne doit pas recevoir sur ses comptes bancaires propres les fonds clients destines aux commercants dans le flux cible.
- Les objets internes de paiement et reversement restent dans le chemin nominal comme projections metier Stripe ; ils ne constituent pas une detention des fonds ni une execution bancaire manuelle.
- La validation QR reste la condition metier d'eligibilite au transfer, mais l'execution du transfer reste pilotee par Localeo lors des campagnes bimensuelles et ne doit pas transformer Localeo en teneur de fonds sur compte bancaire propre.
- Les anciens flux manuels banque ne disposent d'aucun fallback ni mecanisme de retrocompatibilite operationnelle ; ils sont remplaces par les campagnes Stripe Connect ou bloques jusqu'a resolution Stripe.

### Dossier de preuve attendu

- Schema de flux cible paiement, balance Stripe, transfer, payout et compte bancaire.
- Qualification du role Localeo dans Stripe Connect : plateforme, agent, distributeur ou autre qualification retenue.
- Decision documentee sur le besoin ou l'absence de besoin d'enregistrement ACPR.
- References contractuelles Stripe utiles pour le traitement, la detention, la segregation ou la protection des fonds.
- Analyse du cas de defaillance Localeo entre paiement client et transfer commercant.
- Annexe contractuelle dediee aux flux Stripe Connect, relue par le conseil juridique avant integration aux CGV ou au contrat commercant.
- Liste des documents contractuels Localeo a modifier : CGV, contrat commercant, mandat existant, factures, mentions back-office et annexes.
- Decision de go/no-go juridique avant production.

### Criteres d'acceptation conformite

- Le dossier de conformite est relu par le conseil juridique avant activation du flux Stripe Connect en production.
- Les documents contractuels ne contredisent pas le modele de flux implemente.
- Le back-office finance ne propose que les flux Stripe Connect operationnels ; les anciens flux manuels sont supprimes.
- Un test ou controle d'exploitation prouve qu'aucun payout commercant cible ne passe par un compte bancaire propre Localeo.
- Les tickets techniques ne peuvent pas fermer l'epic si les points `EP39-JUR-*` restent sans decision.

## Simulation indicative frais Stripe

Simulation realisee pour cadrer le modele economique d'une vente de coffret a `49,00 EUR` avec deux reversements commercants de `21,00 EUR` chacun. Les montants sont indicatifs : les frais reels dependent du contrat Stripe, du type de carte, du pays de la carte, du type de compte Connect, des options de payout et des eventuels tarifs negocies.

Sources tarifaires a revalider avant mise en production :

- [Stripe France - tarifs Payments](https://stripe.com/fr/pricing) : cartes standard EEE a `1,5 % + 0,25 EUR`, cartes premium EEE a `1,9 % + 0,25 EUR`, cartes britanniques a `2,5 % + 0,25 EUR`, cartes internationales a `3,25 % + 0,25 EUR`.
- [Stripe France - tarifs Connect](https://stripe.com/fr/connect/pricing) : selon le modele ou Stripe gere les tarifs, aucun frais supplementaire pour la plateforme ; selon le modele ou la plateforme gere les tarifs, frais Connect indicatifs de `2 EUR` par compte actif par mois et `0,25 % + 0,10 EUR` par virement effectue.

### Hypotheses metier

- Montant paye par le client : `49,00 EUR`.
- Reversement commercant 1 : `21,00 EUR`.
- Reversement commercant 2 : `21,00 EUR`.
- Total reversements commercants : `42,00 EUR`.
- Commission Localeo brute avant frais Stripe : `7,00 EUR`.
- Les frais Stripe sont portes par Localeo.
- Le scenario cible retient le modele ou Localeo gere les tarifs Stripe Connect.
- Aucun remboursement, litige, conversion de devise, Instant Payout ou tarif negocie n'est applique.

### Scenario nominal - carte standard EEE

| Element | Calcul | Montant |
| --- | ---: | ---: |
| Paiement client |  | `49,00 EUR` |
| Reversements commercants | `21,00 + 21,00` | `42,00 EUR` |
| Commission Localeo brute | `49,00 - 42,00` | `7,00 EUR` |
| Frais paiement Stripe | `49,00 * 1,5 % + 0,25` | `0,99 EUR` |
| Frais Connect variables cibles | `2 * (21,00 * 0,25 % + 0,10)` | `0,31 EUR` |
| Frais Stripe estimes avec frais Connect variables | `0,99 + 0,31` | `1,30 EUR` |
| Commission Localeo nette apres frais Stripe | `7,00 - 1,30` | `5,70 EUR` |

Les frais mensuels de comptes actifs, lorsqu'ils sont applicables au contrat Stripe, sont portes par Localeo et doivent etre suivis dans la rentabilite globale, hors calcul unitaire de cette transaction.

### Sensibilite par type de carte

| Type de carte | Frais paiement Stripe | Frais Stripe avec Connect variable | Commission Localeo nette |
| --- | ---: | ---: | ---: |
| Carte standard EEE | `0,99 EUR` | `1,30 EUR` | `5,70 EUR` |
| Carte premium EEE | `1,18 EUR` | `1,49 EUR` | `5,51 EUR` |
| Carte britannique | `1,48 EUR` | `1,79 EUR` | `5,21 EUR` |
| Carte internationale | `1,84 EUR` | `2,15 EUR` | `4,85 EUR` |

### Points a confirmer

- Documentation tarifaire contractuelle Stripe applicable au modele Connect Express ou Accounts v2 equivalent.
- Nature exacte des frais appliques aux transfers, payouts ou virements selon le contrat Stripe final.
- Prise en charge des frais Stripe : decidee, Localeo porte les frais et les integre a sa commission.
- Traitement des frais mensuels de comptes actifs : decide, cout absorbe par Localeo.
- Arrondis exacts appliques par Stripe et reconciliation avec les `balance_transaction`.
- Impact des remboursements, litiges, cartes premium, cartes internationales et conversions de devise.

## Modele cible indicatif

### `Commercant`

- `stripe_account_id`
- `stripe_onboarding_statut`
- `stripe_charges_enabled`
- `stripe_payouts_enabled`
- `stripe_requirements_due`
- `stripe_onboarding_updated_at`

### `Paiement`

- `provider` : `STRIPE`
- `stripe_checkout_session_id`
- `stripe_payment_intent_id`
- `stripe_charge_id`
- `stripe_customer_id`
- `transfer_group`
- `mode_flux_financier` : `SEPARATE_CHARGES_AND_TRANSFERS`
- `statut_stripe`
- `stripe_fee_amount`
- `commission_localeo_brute`
- `commission_localeo_nette_estimee`
- `metadata_stripe`

### `MouvementReversement`

- `provider` : `STRIPE`
- `mode_execution` : `PSP_STRIPE_CONNECT`
- `validation_prestation_id`
- `commercant_id`
- `paiement_id`
- `montant`
- `devise`
- `transfer_group`
- `stripe_transfer_id` si cree
- `stripe_source_transaction_id` si utilise
- `statut_mouvement` : `A_CALCULER`, `TRANSFERABLE`, `BLOQUE_ONBOARDING_STRIPE`, `EN_CAMPAGNE`, `TRANSFER_DEMANDE`, `TRANSFER_CONFIRME`, `ECHEC_TRANSFER`, `ANNULE`
- `motif_blocage`
- `idempotency_key`
- `metadata_stripe`

### `Reversement`

- `provider` : `STRIPE`
- `mode_execution` : `PSP_STRIPE_CONNECT`
- `commercant_id`
- `transfer_group`
- `statut_reversement`
- `montant_total`
- `date_demande_transfer`
- `date_confirmation_transfer`
- `metadata_stripe`

### `PaiementReversement`

- `provider` : `STRIPE`
- `mode_execution` : `PSP_STRIPE_CONNECT`
- `reversement_id`
- `stripe_transfer_id`
- `stripe_payout_id` si disponible et pertinent
- `stripe_status`
- `idempotency_key`
- `date_demande_operation`
- `date_confirmation_operation`
- `motif_echec`
- `metadata_stripe`

### Journal evenement Stripe

- `operation_type` : `PAYMENT`, `TRANSFER`, `REFUND`, `PAYOUT_SYNC`
- `provider` : `STRIPE`
- `mode_execution` : `PSP_STRIPE_CONNECT`
- `objet_metier_type`
- `objet_metier_id`
- `stripe_transfer_id`
- `stripe_payment_intent_id`
- `stripe_charge_id`
- `stripe_refund_id`
- `stripe_source_transaction_id`
- `transfer_group`
- `stripe_status`
- `idempotency_key`
- `date_demande_operation`
- `date_confirmation_operation`
- `motif_echec`
- `metadata_stripe`

### Dossier conformite PSP

- `qualification_modele_psp`
- `role_localeo`
- `besoin_enregistrement_acpr`
- `decision_juridique_statut`
- `date_validation_juridique`
- `references_contractuelles_stripe`
- `analyse_cantonnement_fonds`
- `annexe_contractuelle_flux_stripe_connect`
- `documents_localeo_a_mettre_a_jour`
- `decision_go_no_go_production`

## Workflows cibles

### Cadrage conformite initial

1. Le produit et la finance decrivent le flux cible Stripe Connect.
2. L'architecture cartographie le chemin des fonds : paiement, balance Stripe, transfer, payout, compte bancaire.
3. Le conseil juridique qualifie le role Localeo et le besoin eventuel d'enregistrement ACPR.
4. Les documents Stripe utiles sur la protection des fonds sont references.
5. Les CGV, contrats commercants, mandats existants, factures, mentions back-office, annexes et libelles produit sont corriges si necessaire.
6. La decision de go/no-go juridique est conservee dans le dossier de preuve.

### Onboarding commercant

1. L'operateur ouvre la fiche commercant.
2. Le backend cree ou retrouve le compte connecte Stripe Express.
3. Le backend genere un lien d'onboarding Stripe Express.
4. Le lien Stripe est ouvert depuis l'application commercant ou un parcours authentifie.
5. Le commercant complete les informations requises chez Stripe.
6. Stripe redirige le navigateur vers l'application commercant via `return_url` ou `refresh_url`.
7. L'application commercant appelle le backend pour resynchroniser le compte ou regenerer un lien expire.
8. Les webhooks Stripe synchronisent les capacites et exigences.
9. Le back-office affiche le commercant comme eligible ou bloque.
10. La documentation d'onboarding commercant decrit le parcours nominal, les statuts, les pieces attendues, les erreurs frequentes, les reprises, les routes application commercant et les actions support.

### Paiement client

1. Le client consulte un coffret vendable.
2. Le backend a prealablement verifie que tous les commercants des prestations du coffret disposent d'un compte connecte Stripe eligible.
3. Si un commercant n'est pas eligible Stripe Connect, le coffret n'est pas vendable et le paiement n'est pas initialise.
4. Le backend initialise le paiement Stripe sur le compte plateforme.
5. Le backend calcule un `transfer_group` stable au format `achat:{achat_id}`.
6. Le paiement est confirme par Stripe.
7. Le backend conserve Checkout Session, PaymentIntent, Charge et `transfer_group`.
8. Aucun transfer commercant n'est cree a cette etape.

### Degradation d'eligibilite Stripe apres achat

1. Un achat a ete realise alors que le coffret etait vendable.
2. Le compte connecte Stripe d'un commercant devient incomplet, bloque ou non eligible avant validation QR ou avant campagne.
3. Le coffret deja achete reste utilisable par le client.
4. A la validation QR, le backend cree le `MouvementReversement` avec le statut `BLOQUE_ONBOARDING_STRIPE`.
5. Le mouvement reste visible en back-office finance, mais n'est pas selectionnable dans une campagne de reversement.
6. Le commercant est relance pour finaliser ou regulariser Stripe Connect.
7. A regularisation, un webhook Stripe ou une resynchronisation rend le mouvement transferable pour une prochaine campagne.

### Paiement client historique sans controle vendabilite

1. Si un achat anterieur a la mise en place du controle vendabilite contient une prestation d'un commercant non eligible Stripe Connect, il suit le meme parcours de blocage que la degradation d'eligibilite apres achat.
2. Aucun fallback manuel banque n'est autorise.
3. Le reversement reste bloque jusqu'a regularisation Stripe Connect.

### Validation QR et transfer

1. Le commercant valide la prestation via le parcours QR.
2. Le backend verifie la validite de la prestation et du coffret.
3. Le backend calcule le montant a reverser.
4. Le backend verifie l'eligibilite Stripe Connect du commercant.
5. Si le commercant est eligible Stripe Connect, le backend cree ou confirme un `MouvementReversement` transferable, sans creer immediatement le transfer Stripe.
6. Si le commercant n'est pas eligible Stripe Connect, le backend cree ou confirme un `MouvementReversement` bloque `BLOQUE_ONBOARDING_STRIPE`, non selectionnable en campagne.
7. Le mouvement reste visible en back-office finance jusqu'a la campagne de reversement ou jusqu'a regularisation Stripe.

### Campagne bimensuelle de reversement

1. L'operateur finance Localeo ouvre ou controle la campagne de reversement bimensuelle planifiee le 1er ou le 15 du mois a 22h00.
2. Le backend liste les mouvements transferables issus de prestations validees.
3. L'operateur controle les blocages : compte connecte non eligible, montant incoherent, incident remboursement ou decision de conformite manquante.
4. L'operateur confirme la campagne.
5. Le backend cree les `Reversement` et `PaiementReversement` cibles.
6. Le backend cree les transfers Stripe avec destination, montant, devise, `transfer_group` et `source_transaction` obligatoires.
7. Les webhooks Stripe confirment ou corrigent l'etat des transfers.
8. Les statuts internes distinguent mouvement transferable, transfer demande, transfer confirme et echec.

### Remboursement

1. L'operateur ou le workflow support demande un remboursement.
2. Le backend identifie le paiement Stripe d'origine et les transfers deja executes.
3. Si aucun transfer n'a ete execute, le remboursement client peut etre traite sans compensation commercant.
4. Si un transfer a deja ete execute, la prestation est consideree executee et non remboursable par defaut.
5. Toute demande post-transfer est traitee comme litige ou geste commercial exceptionnel, avec decision support/finance, sans remboursement automatique ni fallback bancaire manuel.
6. Le remboursement Stripe ou le litige et ses effets internes sont audites.

## Impacts sur les epics existantes

- Epic 6 : le montant de reversement de `PrestationCoffret` reste la source de verite du montant a transferer.
- Epic 12 : le traitement manuel banque est decommissionne pour les nouveaux flux ; `PaiementReversement` reste mais represente l'execution Stripe.
- Epic 13 : la generation de reversements conserve les objets internes, mais leur execution cible devient la creation de transfers Stripe dans des campagnes bimensuelles portant uniquement sur les mouvements rendus transferables par validation QR.
- Epic 20 : les remboursements doivent etre recadres selon les contraintes Stripe, notamment avant ou apres transfer.
- Epic 28 : le calcul de rentabilite doit integrer les frais Stripe, transfers, remboursements et echecs.
- Epic 30 : la vision 360 finance doit afficher les statuts Stripe Connect et les operations Stripe, sans dependre des anciens lots de paiement bancaire pour les nouveaux flux.
- Epic 35 : les actions d'onboarding, reprise de paiement/transfer et consultation finance doivent etre protegees par roles.

## Securite, conformite et audit

- Les secrets Stripe sont configures par environnement, jamais stockes en base.
- Les webhooks Stripe sont verifies par signature.
- Les donnees bancaires commercant sont collectees et gerees par Stripe Connect autant que possible.
- Localeo ne stocke pas d'IBAN commercant si Stripe Connect devient la source operationnelle suffisante.
- Les fonds commercants ne transitent pas par un compte bancaire propre Localeo dans le modele cible valide.
- Les objets internes de paiement/reversement portent le suivi metier des operations Stripe, sans execution bancaire manuelle.
- Le mecanisme de protection, segregation ou cantonnement des fonds chez Stripe doit etre documente dans le dossier de conformite.
- La qualification juridique du modele Stripe Connect est une condition de mise en production.
- Aucune exception manuelle banque n'est autorisee dans la cible ; un incident de paiement ou reversement doit etre resolu via Stripe ou rester bloque.
- Les actions back-office sensibles sont reservees aux profils habilites.
- Chaque creation ou reprise de paiement, transfer ou remboursement est auditee.
- Les logs ne doivent pas exposer de secret, payload Stripe sensible ou donnee bancaire complete.

Actions d'audit minimales :
- `stripe.connected_account.created`
- `stripe.connected_account.onboarding_link.created`
- `stripe.connected_account.updated`
- `stripe.payment.initialized`
- `stripe.payment.succeeded`
- `stripe.payment.failed`
- `stripe.transfer.requested`
- `stripe.transfer.succeeded`
- `stripe.transfer.failed`
- `stripe.transfer.retry.requested`
- `stripe.refund.requested`
- `stripe.refund.succeeded`
- `stripe.refund.failed`

## Lots d'implementation

### Lot 0 - Conformite PSP et qualification des flux

- Cartographier le flux financier cible et les frontieres entre Stripe, Localeo et les commercants.
- Qualifier le role juridique de Localeo dans Stripe Connect.
- Documenter le besoin ou l'absence de besoin d'enregistrement ACPR.
- Documenter le mecanisme de cantonnement, segregation ou protection des fonds applicable chez Stripe.
- Auditer et aligner CGV, contrats commercants, mandat existant, factures, mentions back-office et annexes.
- Valider que les flux cibles ne transitent pas par un compte bancaire propre Localeo.
- Obtenir une decision de go/no-go juridique avant activation production.

### Lot 0T - Socle technique Stripe Connect

- Ajouter le feature flag `LOCALEO_FEATURE_STRIPE_CONNECT_ENABLED`.
- Normaliser les variables de configuration Stripe Connect cibles.
- Definir les ports applicatifs Stripe Connect : compte connecte, paiement, transfer, remboursement et webhook.
- Ajouter le journal minimal des operations Stripe et les cles d'idempotence metier.
- Preparer les migrations one-shot des objets internes conserves comme projections Stripe.
- Inventorier les anciens usages operationnels manuels a supprimer : lots bancaires, exports, confirmations et paiements manuels.
- Poser les statuts cibles des mouvements : `A_CALCULER`, `TRANSFERABLE`, `BLOQUE_ONBOARDING_STRIPE`, `EN_CAMPAGNE`, `TRANSFER_DEMANDE`, `TRANSFER_CONFIRME`, `ECHEC_TRANSFER`, `ANNULE`.
- Verifier que l'environnement de test Stripe permet le scenario bout en bout sans activation production.

### Lot 1 - Socle Stripe Connect commercants

- Ajouter les champs Stripe Connect sur les commercants.
- Implementer la creation idempotente de compte connecte.
- Generer les liens d'onboarding.
- Utiliser l'application commercant comme cible `return_url` et `refresh_url` des liens d'onboarding.
- Synchroniser les capacites via webhook.
- Afficher l'eligibilite dans le back-office.
- Produire la documentation detaillee du processus d'onboarding commercant Stripe Connect.

### Lot 2 - Paiement client Stripe

- Adapter l'initialisation paiement Stripe.
- Generer et persister le `transfer_group` canonique `achat:{achat_id}`.
- Persister Checkout Session, PaymentIntent et Charge.
- Garantir l'absence de transfer automatique au paiement.
- Tester les webhooks de paiement.

### Lot 3 - Mouvements apres validation QR

- Brancher la creation du `MouvementReversement` sur la validation QR.
- Statuer le mouvement en transferable si le compte connecte Stripe est eligible.
- Statuer le mouvement en `BLOQUE_ONBOARDING_STRIPE` si le compte connecte Stripe est incomplet, bloque ou non eligible.
- Interdire la creation immediate de transfer Stripe au moment de la validation QR.
- Exposer les mouvements transferables et bloques dans le back-office finance.
- Ajouter les cles d'idempotence du mouvement.
- Gerer les rejeux de validation sans double mouvement.

### Lot 3B - Campagnes bimensuelles de transfers Stripe

- Ajouter le pilotage de campagne bimensuelle de reversement par Localeo.
- Selectionner les mouvements transferables eligibles.
- Creer les `Reversement` et `PaiementReversement` de campagne.
- Creer les transfers Stripe uniquement apres validation de la campagne.
- Exiger `source_transaction` et reparer les references historiques avant reprise.
- Ajouter les cles d'idempotence de transfer.
- Gerer les echecs et reprises controlees.
- Mettre a jour les statuts internes.

### Lot 4 - Remboursements et support

- Distinguer remboursement avant transfer et apres transfer.
- Integrer les remboursements Stripe au workflow support.
- Afficher les contraintes de remboursement dans le back-office.
- Auditer les remboursements et impacts sur reversements.

### Lot 5 - Pilotage finance et exploitation

- Adapter la vision 360 finance.
- Supprimer les modes manuel banque des parcours operationnels et ne conserver que Stripe Connect.
- Exposer les blocages onboarding.
- Ajouter les alertes paiements/transfers/remboursements en echec.
- Documenter les procedures d'exploitation Stripe Connect.

### Lot 6 - Requalification des objets internes autour de Stripe

- Cartographier les usages existants de `Paiement`, `MouvementReversement`, `Reversement`, `PaiementReversement`, lots de paiement et exports bancaires.
- Requalifier `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` comme projections metier Stripe.
- Identifier et supprimer les donnees et parcours de reversement manuel non necessaires, l'application n'etant pas en production.
- Remplacer les actions d'export ou confirmation bancaire par des commandes Stripe et des synchronisations webhook.
- Adapter les vues finance pour lire les objets internes enrichis des references Stripe.
- Documenter la strategie de migration et les controles de non-regression.

### Lot 7 - Tests et reprise

- Tester creation compte connecte idempotente.
- Tester blocage de publication ou vente d'un coffret contenant une prestation d'un commercant non eligible Stripe Connect.
- Tester paiement avec `transfer_group`.
- Tester absence de transfer avant validation QR.
- Tester creation de mouvement transferable apres validation QR.
- Tester creation de mouvement `BLOQUE_ONBOARDING_STRIPE` si le compte connecte devient non eligible apres achat.
- Tester requalification d'un mouvement bloque en mouvement transferable apres regularisation Stripe Connect.
- Tester absence de transfer Stripe immediat apres validation QR.
- Tester creation transfer lors d'une campagne bimensuelle.
- Tester `source_transaction` present et alternative Stripe documentee sans `source_transaction`.
- Tester webhook signe et idempotent.
- Tester reprise sans double paiement ou double transfer.
- Tester remboursement avant transfer.
- Tester traitement en litige des demandes post-transfer.

## Validations externes non bloquantes pour la cloture implementation

Ces points ne bloquent pas la cloture technique de l'EPIC 39. Ils restent des
conditions de validation juridique, finance ou conformite avant activation
production :

- validation juridique finale du mecanisme de cantonnement, segregation ou protection des fonds applicable chez Stripe ;
- validation juridique finale de la qualification Localeo comme plateforme numerique d'intermediation, operateur de plateforme en ligne et mandataire d'encaissement ;
- validation juridique finale de l'annexe Stripe avant integration aux CGV, contrat commercant, mandat existant, factures, mentions back-office et annexes ;
- validation contractuelle definitive des tarifs, comptes actifs, balances, reserves, responsabilites et protection des fonds Stripe ;
- decision de go/no-go production juridico-finance avant activation de `LOCALEO_FEATURE_STRIPE_CONNECT_ENABLED` en production.

## Tickets clotures

Les tickets techniques, operationnels et documentaires suivants sont traites dans
le code, le back-office ou la documentation locale :

- `EP39-T00A` Feature flag `LOCALEO_FEATURE_STRIPE_CONNECT_ENABLED` et blocage d'activation production sans decision de go/no-go.
- `EP39-T00B` Variables de configuration Stripe Connect cibles et alias historiques documentes.
- `EP39-T00C` Ports applicatifs Stripe Connect pour compte connecte, paiement, transfer, remboursement et webhook.
- `EP39-T00D` Journal minimal `operations_stripe` et cles d'idempotence metier.
- `EP39-T00E` Strategie one-shot et mapping des statuts cibles Stripe Connect.
- `EP39-T00F` Inventaire et retrait des usages operationnels des lots bancaires, exports et confirmations manuelles.
- `EP39-T01` Champs Stripe Connect sur `Commercant`.
- `EP39-T02` Creation idempotente de compte connecte Stripe Express.
- `EP39-T03` Liens d'onboarding Stripe Express.
- `EP39-T04` Synchronisation des webhooks de compte connecte.
- `EP39-T04B` Documentation du processus d'onboarding commercant Stripe Connect.
- `EP39-T04C` Blocage publication et vente des coffrets contenant une prestation d'un commercant non eligible Stripe Connect.
- `EP39-T04D` Reevaluation de la vendabilite apres regularisation Stripe Connect.
- `EP39-T05` Initialisation paiement en modele separate charges and transfers.
- `EP39-T06` `transfer_group` canonique `achat:{achat_id}`.
- `EP39-T07` Charge Stripe d'origine conservee pour `source_transaction`.
- `EP39-T08` Mouvements transferables apres validation QR sans transfer immediat.
- `EP39-T08A` Mouvements `BLOQUE_ONBOARDING_STRIPE` si compte connecte non eligible.
- `EP39-T08B` Campagnes bimensuelles de creation des transfers Stripe.
- `EP39-T09` Idempotence et reprise des paiements/transfers.
- `EP39-T10` Remboursements avant transfer et litiges post-transfer.
- `EP39-T11` Vision 360 finance adaptee aux statuts Stripe Connect.
- `EP39-T12` Procedures d'exploitation Stripe Connect.
- `EP39-T13` Requalification `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` comme projections metier Stripe.
- `EP39-T14` References Stripe, statuts webhook et cles d'idempotence rattaches aux objets internes.
- `EP39-T15` Donnees et parcours operationnels de reversement manuel retires, l'application n'etant pas en production.
- `EP39-JUR-02` Invariant aucun transit des fonds commercants par un compte bancaire propre Localeo documente.
- `EP39-JUR-04` Documents et libelles produit alignes avec le modele PSP cible dans le perimetre documentaire local traite.
- `EP39-JUR-05` Suppression des virements et reversements manuels sans fallback operationnel documentee.


## Compléments Commerçant — impacts Stripe Connect

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### Objectif

Ce document formalise les evolutions a prevoir dans l'application commercant dans le cadre de l'EPIC 39 - Delegation des flux financiers a Stripe Connect.

L'application commercant doit permettre au commercant de comprendre, finaliser et suivre son onboarding Stripe Connect, ainsi que les impacts de son eligibilite Stripe sur la vendabilite de ses prestations et sur ses reversements.

### Contexte EPIC 39

L'EPIC 39 met en place Stripe Connect comme modele cible pour les paiements et reversements :

- paiement client encaisse via Stripe sur le compte plateforme Localeo ;
- aucun transfer commercant au moment du paiement ;
- creation d'un mouvement de reversement lors de la validation QR ;
- transfer Stripe execute ulterieurement via campagnes bimensuelles ;
- blocage des ventes ou reversements si le compte Stripe Connect du commercant n'est pas eligible ;
- suppression des parcours bancaires manuels pour les nouveaux flux.

### Frontiere entre application commercant et webhooks Stripe

L'application commercant gere uniquement l'experience utilisateur d'onboarding
et les deux routes de retour navigateur. Elle ne recoit aucun webhook Stripe et
ne doit contenir aucune cle API Stripe ni aucun secret de signature `whsec_...`.

Les deux destinations Stripe sont exclusivement exposees par le backend :

- `POST /public/stripe/webhook` recoit les evenements du compte plateforme pour
  les paiements, charges, remboursements et transfers. La signature est verifiee
  avec `LOCALEO_STRIPE_WEBHOOK_SECRET` ;
- `POST /public/stripe-connect/webhook` recoit les evenements emis pour les
  comptes connectes et traite uniquement `account.updated`. La signature est
  verifiee avec `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET`.

Ces destinations utilisent actuellement les evenements Stripe API v1 au format
Snapshot. Les evenements v2 Thin ne sont pas pris en charge par les handlers
backend actuels. Les routes frontend `/stripe-connect/onboarding/return` et
`/stripe-connect/onboarding/refresh` sont des callbacks de navigation et ne
doivent jamais etre configurees comme destinations webhook.

### APIs backend deja disponibles cote application commercant

Les routes suivantes sont exposees cote backend et doivent etre consommees par l'application commercant.

#### Onboarding Stripe Connect

- `GET /protected/referencement/commercants/me/stripe-connect`
  - consulter le statut Stripe Connect du commercant connecte ;
  - recuperer l'eligibilite reversement, les capacites Stripe et le statut onboarding.

- `POST /protected/referencement/commercants/me/stripe-connect/onboarding`
  - creer ou retrouver le compte connecte Stripe ;
  - generer un lien d'onboarding Stripe Express ;
  - retourner l'URL Stripe a ouvrir par le commercant.

- `POST /protected/referencement/commercants/me/stripe-connect/synchroniser`
  - resynchroniser le compte connecte apres retour Stripe ou action utilisateur ;
  - mettre a jour les statuts locaux.

Le payload Stripe Connect expose actuellement l'identifiant du compte Stripe,
le statut d'onboarding, `stripe_charges_enabled`, `stripe_payouts_enabled`, les
exigences restantes, le motif de desactivation, l'eligibilite Localeo et, le cas
echeant, l'URL d'onboarding. Le champ interne
`stripe_onboarding_updated_at` n'est pas encore expose par cette API.

#### Reversements commercant

- `GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mouvements/a-reverser`
  - lister les mouvements de reversement encore a traiter ;
  - afficher les montants transferables, en cours, bloques ou en echec ;
  - inclure notamment `ECHEC_TRANSFER` avec son `motif_blocage` afin que les
    echecs en attente de reprise restent visibles du commercant.

- `GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mois/{nb_mois}`
  - afficher l'historique des reversements effectues ;
  - restituer les paiements/reversements confirmes.

Limites du contrat actuel : le payload des mouvements expose desormais le motif
de blocage ou du dernier echec. Les deux routes ne fournissent pas encore le
statut Stripe Connect du commercant, le detail du transfer Stripe et sa
reference dediee. Ces informations constituent des evolutions du contrat API a
realiser avant de les rendre obligatoires dans l'interface.

### Evolutions a prevoir cote application commercant

#### 1. Ajouter une section Stripe Connect dans le profil commercant

L'application commercant doit afficher une section dediee au compte Stripe Connect.

Informations a afficher :

- statut onboarding Stripe Connect ;
- eligibilite reversement ;
- capacite `charges` active ou inactive ;
- capacite `payouts` active ou inactive ;
- exigences Stripe restantes si elles sont exposees ;
- motif de blocage lisible ;
- date de derniere synchronisation, apres exposition de
  `stripe_onboarding_updated_at` dans le payload backend.

Actions attendues :

- bouton `Configurer mon compte Stripe` ;
- appel a `POST /protected/referencement/commercants/me/stripe-connect/onboarding` ;
- redirection vers `onboarding_url` retournee par le backend ;
- bouton `Synchroniser mon compte` ;
- appel a `POST /protected/referencement/commercants/me/stripe-connect/synchroniser`.

#### 2. Implementer les routes de retour Stripe

Les URLs Stripe Connect ciblees par la configuration backend doivent pointer vers l'application commercant.

Routes a prevoir :

- `/stripe-connect/onboarding/return`
- `/stripe-connect/onboarding/refresh`

##### Page return

Comportement attendu :

1. afficher un etat `Verification de votre compte Stripe` ;
2. appeler `POST /protected/referencement/commercants/me/stripe-connect/synchroniser` ;
3. afficher le statut final ;
4. proposer un retour vers le profil ou le tableau de bord commercant.

Point important : le retour Stripe ne prouve pas que l'onboarding est complet. La page doit toujours declencher une resynchronisation backend.

##### Page refresh

Comportement attendu :

1. verifier que la session commercant est encore valide ;
2. appeler `POST /protected/referencement/commercants/me/stripe-connect/onboarding` ;
3. recuperer un nouveau lien Stripe ;
4. rediriger le navigateur vers ce nouveau lien.

Cas d'erreur a gerer :

- session commercant expiree ;
- lien Stripe expire ou deja utilise ;
- compte toujours incomplet ;
- API Stripe indisponible ;
- erreur backend temporaire.

#### 3. Afficher les impacts metier de l'eligibilite Stripe

Lorsque le compte Stripe Connect n'est pas eligible, l'application doit expliquer les impacts concrets.

Messages a prevoir :

- les prestations peuvent ne pas etre vendables ;
- les coffrets contenant ces prestations peuvent etre bloques a la vente ;
- les reversements sont suspendus jusqu'a regularisation ;
- aucun virement bancaire manuel n'est prevu dans le modele cible ;
- la regularisation doit etre realisee dans le parcours Stripe.

Formulation recommandee :

> Votre compte Stripe Connect doit etre finalise pour permettre la vente de vos prestations et le versement de vos reversements.

Formulations a eviter :

- `paiement en attente cote Localeo` ;
- `virement manuel a venir` ;
- `merci d'envoyer votre IBAN par email` ;
- toute formulation laissant penser que Localeo collecte directement les donnees bancaires ou KYC.

#### 4. Adapter les vues reversements

Les vues existantes de reversements doivent etre adaptees a la logique Stripe Connect.

##### Mouvements a reverser

Informations a afficher :

- montant ;
- prestation ;
- coffret ;
- date de validation QR ;
- statut du mouvement ;
- motif de blocage eventuel ;
- statut Stripe Connect du commercant.

Statuts a rendre lisibles :

- `TRANSFERABLE` : pret pour une prochaine campagne Stripe ;
- `BLOQUE_ONBOARDING_STRIPE` : bloque tant que le compte Stripe Connect n'est pas eligible ;
- `TRANSFER_DEMANDE` : transfer Stripe demande ;
- `TRANSFER_CONFIRME` : transfer Stripe confirme ;
- `ECHEC_TRANSFER` : echec de transfer Stripe.

Message important :

> La validation d'une prestation cree un droit au reversement, mais le transfer Stripe n'est pas execute immediatement. Les transfers sont pilotes par campagnes de reversement Localeo.

##### Historique des reversements

Informations a afficher :

- periode ;
- montant ;
- statut du reversement ;
- statut du transfer Stripe ;
- reference Stripe si disponible ;
- date de demande du transfer ;
- date d'execution ou de synchronisation ;
- echec eventuel et message de reprise.

Libelles recommandes :

- `Reversement via Stripe Connect` ;
- `Transfer Stripe demande` ;
- `Transfer Stripe execute` ;
- `Transfer Stripe en echec` ;
- `Reversement bloque - compte Stripe Connect a regulariser`.

Libelles a supprimer ou eviter :

- `virement bancaire` ;
- `paiement manuel` ;
- `export bancaire` ;
- `IBAN commercant`.

#### 5. Ajouter des notifications commercant

Notifications a prevoir :

- invitation initiale a finaliser Stripe Connect ;
- rappel si Stripe demande des informations complementaires ;
- compte devenu non eligible ;
- reversement bloque ;
- reversement demande via Stripe ;
- transfer Stripe en echec ;
- regularisation Stripe reussie.

Contraintes :

- ne jamais demander l'envoi d'un IBAN, d'une piece d'identite ou d'un document KYC par email ;
- renvoyer vers le parcours Stripe depuis une session authentifiee ;
- ne pas inclure de lien Stripe sensible reutilisable dans les emails de relance.

#### 6. Adapter le dashboard commercant

Le tableau de bord commercant doit exposer un etat synthétique Stripe Connect.

Indicateurs recommandes :

- statut du compte Stripe Connect ;
- alerte prioritaire si le compte n'est pas eligible ;
- montant a reverser ;
- montant bloque pour cause Stripe Connect ;
- derniers reversements demandes ;
- derniers reversements en echec.

Exemples de badges :

- `Compte Stripe a configurer` ;
- `Informations Stripe requises` ;
- `Compte eligible` ;
- `Compte bloque` ;
- `Reversements suspendus`.

#### 7. Ajouter une aide integree

Une aide courte doit etre disponible depuis l'application commercant.

Contenu recommande :

- pourquoi Stripe Connect est necessaire ;
- ce que Stripe collecte ;
- ce que Localeo ne collecte pas ;
- pourquoi un compte incomplet bloque ventes et reversements ;
- que faire si Stripe demande des informations complementaires ;
- qui contacter cote support Localeo.

#### 8. Contraintes securite et conformite

L'application commercant doit respecter les contraintes suivantes :

- ne pas collecter d'IBAN ni de documents KYC dans Localeo ;
- ne stocker aucune cle API Stripe ni aucun secret webhook dans l'application ;
- ne jamais appeler les routes backend `/public/stripe/webhook` et
  `/public/stripe-connect/webhook` depuis le navigateur ;
- ne pas afficher de donnees bancaires sensibles Stripe ;
- ne pas stocker localement l'URL d'onboarding au-dela de la session utile ;
- proteger les ecrans Stripe Connect par session commercant authentifiee ;
- gerer proprement l'expiration de session avant redirection Stripe ;
- ne pas exposer les details techniques Stripe inutiles au commercant ;
- conserver des messages comprehensibles et actionnables.

### Priorisation recommandee

#### Priorite 1 - Parcours indispensable

1. Section Stripe Connect dans le profil commercant.
2. Bouton de lancement onboarding.
3. Pages `return` et `refresh`.
4. Synchronisation du statut apres retour Stripe.
5. Messages de blocage vendabilite/reversement.

#### Priorite 2 - Pilotage reversements

1. Adaptation des vues reversements.
2. Affichage des mouvements bloques `BLOQUE_ONBOARDING_STRIPE`.
3. Historique des transfers Stripe.
4. Suppression des libelles de virement manuel.

#### Priorite 3 - Experience et support

1. Notifications de regularisation.
2. Aide integree Stripe Connect.
3. Indicateurs dashboard.
4. Messages de reprise en cas d'erreur Stripe.

### Definition of Done application commercant

L'impact EPIC 39 cote application commercant peut etre considere traite lorsque :

- un commercant authentifie peut consulter son statut Stripe Connect ;
- un commercant peut lancer ou reprendre son onboarding Stripe ;
- les pages `return` et `refresh` Stripe sont implementees ;
- les callbacks frontend restent distincts des deux destinations webhook backend ;
- l'application resynchronise le statut apres retour Stripe ;
- les impacts sur vendabilite et reversements sont visibles ;
- les reversements affichent les statuts Stripe Connect pertinents ;
- les mouvements bloques par onboarding Stripe sont explicites ;
- aucun parcours ne demande d'IBAN ou de document KYC dans Localeo ;
- aucune cle API Stripe ni aucun secret webhook n'est livre au frontend ;
- aucun libelle ne laisse croire a un virement bancaire manuel pour les nouveaux flux ;
- les champs affiches par les vues Stripe Connect et reversements existent dans
  le contrat API, ou sont explicitement identifies comme evolutions a venir ;
- les erreurs Stripe sont affichees de facon actionnable ;
- les messages sont coherents avec la documentation onboarding Stripe Connect.


### Précisions du contrat côté commerçant

#### APIs backend deja disponibles cote application commercant / Reversements commercant

- `GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mouvements/a-reverser`
  - lister les mouvements de reversement encore a traiter ;
  - afficher les montants transferables ou bloques.

Limites du contrat actuel : les payloads de ces deux routes ne fournissent pas
encore tous les champs UX decrits plus bas, notamment le motif de blocage, le
statut Stripe Connect du commercant, le detail du transfer Stripe et sa
reference dediee. Ces informations constituent des evolutions du contrat API a
realiser avant de les rendre obligatoires dans l'interface.
