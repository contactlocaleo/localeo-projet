# Backlog Epic 14 - Documents d'achat et facturation du coffret

## Perimetre

Epic source : `Epic 14. Documents d'achat et facturation du coffret`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : encadrer les documents emis lors de l'achat d'un coffret multi commercants, en faisant de `achats_coffret` la racine documentaire, et en distinguant le recu client immediat, les factures sous-jacentes generables a la demande et leur tracabilite.

## Statut global

- Epic 14 : `Termine`
- Avancement : cadrage produit et legal V1 a transformer en implementation documentaire et back-office.

## Analyse d'impact

### Synthese

Localeo vend un coffret contenant plusieurs prestations de plusieurs commercants, mais n'est pas vendeur des prestations elles-memes. Localeo agit comme intermediaire, encaisse le paiement, reverse les montants de prestation aux commercants et facture ses propres frais de service au client.

La chaine documentaire doit donc distinguer :
- un `recu de paiement` simple emis a l'achat pour le client final ;
- des `factures commercant` emises au nom et pour le compte des commercants pour chaque achat, avec une ligne par prestation incluse ;
- une `facture Localeo` pour les frais de service factures au client ;
- un `pack documentaire` genere a la demande, assemble dans une archive `ZIP`.

### Objectif V1 retenu

Le mode V1 retenu est :
- emission automatique d'un `recu de paiement` lors de la validation du paiement ;
- ajout du recu en piece jointe au mail contenant le QR code du coffret ;
- mention explicite dans le mail invitant le client a utiliser le formulaire de contact avec sa reference d'achat pour demander ses factures ;
- generation a la demande d'un lot de `PDF` rassembles dans un `ZIP` contenant :
  - une facture par commercant et par achat ;
  - une facture Localeo de frais de service ;
- acces a cette generation depuis le back-office sur la fiche d'un `AchatCoffret` et, par commodite operatoire, depuis la `CoffretInstance` rattachee quand elle existe.

## Regles de gestion consolidees

- Un `recu de paiement` peut etre emis uniquement si le paiement de l'`AchatCoffret` est valide.
- Le `recu de paiement` n'est pas une facture fiscale ; il sert de justificatif client simple.
- Le `recu de paiement` peut rester a une ligne unique avec le montant total `TTC` paye.
- La generation des factures detaillees est reservee aux `AchatCoffret` dont le paiement est valide.
- Une facture commercant V1 est generee par commercant et par achat, avec une ligne par prestation du commercant dans le coffret.
- Le pack facture V1 contient :
  - une facture commercant par commercant ;
  - une facture Localeo pour les frais de service lies a l'achat ;
  - aucun document de reversement.
- Chaque facture commercant doit mentionner que Localeo agit au nom et pour le compte du commercant, conformement au mandat de facturation retenu.
- La facture Localeo doit faire apparaitre la `TVA` sur les frais de service uniquement si la TVA est applicable pour Localeo au moment de l'achat.
- Le taux et l'applicabilite de `TVA` doivent etre figes a l'instant de l'achat pour permettre une regeneration fidele ulterieure.
- `AchatCoffret` constitue la racine documentaire de reference pour le recu, le snapshot de facturation et le pack facture.
- Les identites de facturation utiles doivent etre figees au moment de l'achat :
  - client ;
  - commercant ;
  - Localeo ;
  - libelles ;
  - montants ;
  - TVA applicable ou non.
- La regeneration d'un meme pack documentaire ne doit pas modifier le contenu legal de la version deja emise.
- Le `ZIP` n'est pas persiste en V1 ; il est regenere a la demande a partir du snapshot fige.
- Un coffret ne peut pas etre partiellement rembourse : le remboursement est total pour le coffret ou l'instance annulee, ou refuse si une consommation rend l'annulation impossible.
- L'annulation d'un coffret ou d'une instance de coffret invalide aussi les prestations associees encore non consommees : leurs statuts passent de `A_VALIDER` a `ANNULEE`.
- Les avoirs sont hors perimetre V1 ; le remboursement est traite hors systeme sur le moyen de paiement initial.
- Toute generation de pack facture doit etre auditée.

## Flux cible recommande

1. Le paiement de l'`AchatCoffret` est valide.
2. Le systeme genere un `recu de paiement` PDF simple.
3. Le systeme joint ce recu au mail d'envoi du QR code du coffret.
4. Le pied du mail indique qu'une demande de documents de facturation peut etre faite via le formulaire de contact en rappelant la reference d'achat.
5. Depuis le back-office, un operateur autorise ouvre la fiche de l'`AchatCoffret` ou la `CoffretInstance` rattachee.
6. Si l'`AchatCoffret` est paye, il peut demander la generation du pack facture.
7. Le systeme produit :
   - une facture PDF par commercant ;
   - une facture PDF Localeo pour les frais de service ;
   - une archive `ZIP` regroupant l'ensemble.
8. Le systeme journalise la generation dans l'audit.
9. Si l'achat doit etre annule avant consommation, l'operateur peut enregistrer l'annulation depuis la fiche de l'`AchatCoffret` ou de la `CoffretInstance` rattachee avec les informations utiles au remboursement hors systeme.

## Evolutions de modele recommandees

### `DocumentAchatCoffret`

Ajouter une entite ou un aggregate documentaire permettant de tracer les documents emis pour un `AchatCoffret`, avec rattachement optionnel a une `CoffretInstance` pour les usages operationnels.

Champs recommandes :
- `id`
- `achat_id`
- `coffret_instance_id` nullable
- `type_document` : `RECU_PAIEMENT`, `FACTURE_COMMERCANT`, `FACTURE_LOCALEO`, `PACK_FACTURES_ZIP`
- `emetteur_type` : `LOCALEO`, `COMMERCANT`
- `emetteur_id` nullable
- `reference_document`
- `date_generation`
- `version`
- `fichier_nom`
- `stockage_path` ou `blob_key`
- `hash_contenu`

### Snapshot de facturation achat

Ajouter un snapshot de donnees de facturation au moment de l'achat pour figer les mentions et montants. Ce snapshot est rattache a `AchatCoffret`, qui constitue la racine documentaire.

Champs recommandes :
- `achat_id`
- `reference_achat`
- `date_achat`
- `client_nom`
- `client_prenom`
- `client_email`
- `adresse_facturation_client` nullable en V1 tant qu'aucune demande de facturation n'a ete faite
- `montant_total_ttc`
- `montant_frais_service_ht`
- `montant_frais_service_tva`
- `montant_frais_service_ttc`
- `tva_localeo_applicable`
- `taux_tva_localeo` nullable
- `raison_sociale_localeo`
- `adresse_localeo`
- `mentions_legales_localeo`
- pour chaque prestation :
  - `prestation_id`
  - `commercant_id`
  - `raison_sociale_commercant`
  - `adresse_commercant`
  - `libelle_prestation`
  - `montant_prestation_ttc`
  - `mentions_emetteur_commercant`

### Comment figer les valeurs

Le figement ne doit pas reposer sur les tables vivantes du catalogue ou des commercants au moment ou l'on genere la facture.

Le mecanisme V1 recommande est :
- a la validation du paiement, le systeme copie dans une structure dediee de snapshot toutes les valeurs utiles a la facturation ;
- ces valeurs copiees deviennent la source de verite documentaire pour toute generation ulterieure ;
- si l'adresse, la raison sociale, les libelles ou la regle de TVA changent ensuite dans les tables metier, la facture regeneree continue d'utiliser le snapshot ;
- les donnees de facturation client manquantes a l'achat, notamment `nom`, `prenom` et `adresse de facturation`, peuvent etre completees ulterieurement via un flux `demande de facturation`, sans modifier les autres valeurs financieres deja figees.
- la `CoffretInstance` n'est qu'un point d'acces operationnel ; le rattachement de reference reste `achat_id`.

### Numerotation documentaire

Prevoir une source de numerotation separee par emetteur et par type de document legal :
- sequence Localeo pour les factures Localeo ;
- sequence dediee par commercant pour les factures commercants generees au nom et pour le compte.

## Impacts use cases

Use cases a creer :
- `GenererRecuPaiementCoffret`
- `JoindreRecuAuMailQrCoffret`
- `GenererPackFacturesCoffret`
- `TelechargerPackFacturesCoffret`
- `CompleterDonneesFacturationDepuisDemandeContact`
- `AnnulerCoffretInstanceAvantConsommation`

Use cases a adapter :
- envoi du mail QR coffret : ajout du recu et du message de demande de facture ;
- paiement achat coffret : capture du snapshot de facturation ;
- formulaire de contact : ajout d'un motif `demande de facturation` et des champs associes ;
- audit documentaire : trace de generation et telechargement si requis.

Convention de rattachement :
- les use cases documentaires prennent `achat_id` comme entree metier principale ;
- la `CoffretInstance` peut servir de point d'entree back-office, mais doit etre resolue vers son `achat_id`.

## Impacts back-office

Surfaces recommandees :
- fiche `AchatCoffret` comme surface documentaire de reference ;
- action `Generer le pack factures` sur la fiche d'une `CoffretInstance` payee ;
- action `Annuler l'instance` sur la fiche d'une `CoffretInstance` non consommee ;
- affichage de l'etat documentaire :
  - recu genere ou non ;
  - pack facture genere ou non ;
  - date de derniere generation ;
- action de telechargement du `ZIP` depuis le back-office ;
- eventuelle vue de consultation des documents deja emis.

Informations minimales attendues :
- reference d'achat ;
- statut de paiement ;
- date d'achat ;
- nombre de prestations ;
- nombre de factures commercants ;
- montant total paye ;
- montant des frais de service Localeo ;
- indicateur TVA Localeo applicable ;
- informations de paiement utiles au remboursement hors systeme ;
- historique de generation.

## Securite et audit

- Seuls des operateurs back-office habilites peuvent generer ou telecharger le pack facture.
- Les documents fiscaux ne doivent pas etre accessibles si le paiement n'est pas valide.
- Le recu client peut etre envoye automatiquement a l'acheteur sans ouverture du pack facture detaille.
- Les documents doivent etre regenereables a l'identique tant que la version de reference reste la meme.

Actions d'audit minimales :
- `purchase.receipt.generated`
- `purchase.invoice_pack.generated`
- `purchase.invoice_pack.downloaded`
- `purchase.coffret_instance.cancelled`

Portee d'audit retenue :
- `coffret_instance_id`
- `achat_id` ou `reference_achat`
- `operateur_identifiant` pour les actions back-office
- liste des documents generes
- version documentaire
- informations d'annulation utiles si l'instance est annulee

## User Stories

### Story `PRD-065` - Generer un recu de paiement a l'achat du coffret

Priorite : `P0`
Statut : `Termine`

Valeur metier : fournir immediatement au client un justificatif simple de son achat.

Criteres d'acceptation :
- a validation du paiement, le systeme genere un `recu de paiement` PDF ;
- le recu reprend au minimum la reference d'achat, la date, le montant total `TTC` et l'identite Localeo ;
- le recu est rattache a l'`AchatCoffret` et, si pertinent, reference la `CoffretInstance` associee ;
- le recu peut etre retrouve ou regenere sans changer son contenu legal de reference.

### Story `PRD-066` - Joindre le recu au mail d'envoi du QR code et orienter la demande de facture

Priorite : `P0`
Statut : `Termine`

Valeur metier : informer proprement le client des documents disponibles sans complexifier le mail principal.

Criteres d'acceptation :
- le mail d'envoi du QR code joint le recu de paiement ;
- le pied du mail mentionne l'usage du formulaire de contact pour demander les documents de facturation ;
- la reference d'achat a rappeler est visible dans le mail ;
- le wording reste compatible avec le fait que le recu n'est pas une facture.

### Story `PRD-067` - Generer le pack facture d'un coffret paye

Priorite : `P0`
Statut : `Termine`

Valeur metier : produire a la demande l'ensemble des documents fiscaux sous-jacents a un achat multi commercants.

Criteres d'acceptation :
- la generation est possible uniquement si le paiement de l'`AchatCoffret` est valide ;
- le systeme genere une facture commercant par commercant avec une ligne par prestation du commercant dans l'achat ;
- le systeme genere une facture Localeo pour les frais de service ;
- tous les `PDF` sont rassembles dans une archive `ZIP` telechargeable ;
- les documents s'appuient sur un snapshot de donnees fige au moment de l'achat.

### Story `PRD-068` - Rendre la generation du pack facture accessible depuis le back-office

Priorite : `P0`
Statut : `Termine`

Valeur metier : donner a l'exploitation un moyen simple de satisfaire les demandes client.

Criteres d'acceptation :
- la fiche d'un `AchatCoffret` paye expose l'action `Generer le pack factures` ;
- une `CoffretInstance` rattachee peut aussi exposer cette action par commodite, apres resolution vers `achat_id` ;
- un achat non paye ne propose pas l'action ;
- le back-office permet ensuite de telecharger le `ZIP` genere ;
- l'historique des generations est visible.

### Story `PRD-069` - Tracer la generation documentaire dans l'audit

Priorite : `P1`
Statut : `Termine`

Valeur metier : garantir la tracabilite des emissions et des telechargements documentaires.

Criteres d'acceptation :
- la generation du recu produit un audit `purchase.receipt.generated` ;
- la generation du pack facture produit un audit `purchase.invoice_pack.generated` ;
- le telechargement du pack facture produit un audit `purchase.invoice_pack.downloaded` ;
- l'audit conserve la reference d'achat, l'`AchatCoffret`, la `CoffretInstance` si applicable et l'identite de l'operateur.

### Story `PRD-070` - Gerer la TVA Localeo sur les frais de service

Priorite : `P0`
Statut : `Termine`

Valeur metier : emettre une facture Localeo conforme selon l'applicabilite de la TVA.

Criteres d'acceptation :
- la facture Localeo fait apparaitre la TVA uniquement si elle est applicable ;
- le taux de TVA utilise est celui fige au moment de l'achat ;
- l'absence de TVA applicable reste explicite sur le document si necessaire ;
- la regeneration conserve le meme traitement TVA.

### Story `PRD-071` - Mentionner le mandat de facturation Localeo sur les factures commercants

Priorite : `P0`
Statut : `Termine`

Valeur metier : rendre les factures commercants coherentes avec le role d'intermediaire de Localeo.

Criteres d'acceptation :
- chaque facture commercant mentionne que Localeo agit au nom et pour le compte du commercant ;
- la mention est homogène sur tous les documents concernes ;
- les donnees emetteur du commercant restent clairement visibles ;
- le document reste compatible avec la strategie de numerotation retenue.

### Story `PRD-072` - Collecter les donnees de facturation via le formulaire de contact

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre de completer les donnees client strictement necessaires a la facturation sans alourdir le tunnel d'achat initial.

Criteres d'acceptation :
- le formulaire de contact propose un motif `demande de facturation` ;
- ce motif ajoute les champs `nom`, `prenom` et `adresse de facturation` ;
- ces donnees sont utilisees pour la generation documentaire uniquement ;
- la demande est rattachee a une reference d'achat explicite et resolue vers `achat_id`.

### Story `PRD-073` - Annuler une instance de coffret avant consommation

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre un traitement d'annulation propre, trace et exploitable pour un remboursement hors systeme.

Criteres d'acceptation :
- une `CoffretInstance` non consommee peut etre annulee depuis sa fiche back-office ;
- l'annulation passe la `CoffretInstance` a `ANNULE` et les prestations associees encore `A_VALIDER` a `ANNULEE` ;
- les informations de paiement utiles au remboursement sont affichees au moment de l'annulation ;
- l'operateur peut saisir les informations utiles sur l'annulation et le remboursement hors systeme ;
- l'annulation produit un audit `purchase.coffret_instance.cancelled`.

## Points complementaires a traiter

- figer la strategie de numerotation legale des factures commercants et des factures Localeo ;
- confirmer le niveau de donnees client a figer a l'achat si une future facturation autonome client est visee ;
- definir la retention minimale des snapshots et des traces de generation ;
- verifier contractuellement l'existence du mandat de facturation avec chaque commercant ;
- preciser les regles metier exactes d'annulation selon le cycle de vie de la `CoffretInstance`.

## Decisions actees

- Le client recoit automatiquement un `recu de paiement` lors de l'achat.
- Le recu est joint au mail d'envoi du QR code du coffret.
- Le mail invite le client a utiliser le formulaire de contact avec sa reference d'achat pour demander ses documents de facturation.
- Le formulaire de contact expose un motif `demande de facturation` avec collecte de `nom`, `prenom` et `adresse de facturation`.
- Les documents fiscaux detailles sont generes a la demande depuis le back-office.
- Le pack facture contient une facture par commercant et par achat, avec une ligne par prestation, ainsi qu'une facture Localeo de frais de service, assemblees dans un `ZIP`.
- `AchatCoffret` est la racine documentaire de reference pour le recu, le snapshot et le pack facture.
- La generation du pack facture est reservee aux `AchatCoffret` dont le paiement est valide.
- La TVA Localeo apparait sur la facture Localeo uniquement si elle est applicable.
- La regle TVA Localeo est pilotee par une configuration dediee et les montants calcules sont figes a l'achat.
- Les factures commercants mentionnent que Localeo agit au nom et pour le compte du commercant.
- Les factures commercants utilisent une numerotation a sequence dediee par commercant.
- Les factures Localeo utilisent une sequence unique Localeo.
- Le `ZIP` n'est pas stocke en V1 ; il est regenere a la demande a partir du snapshot de facturation.
- Une `CoffretInstance` peut etre annulee depuis le back-office avant consommation avec trace d'audit associee.

## Hors perimetre V1

- envoi automatique des factures detaillees au client a chaque achat ;
- remboursement partiel, explicitement exclu par la regle produit ;
- avoir ;
- portail client de telechargement autonome des factures ;
- facturation electronique B2B sortante ;
- signature electronique ou cachet qualifie des documents ;
- rapprochement comptable automatise entre documents et reversements.
