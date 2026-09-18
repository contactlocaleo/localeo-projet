# Epic 50 - Justificatif d'achat et demandes de facture

## Decision produit

Le processus actuel de generation de factures lors de l'achat est decommissionne.

Lors du paiement d'un coffret, Localeo genere uniquement un document recapitulatif d'achat, appele dans l'Epic `justificatif d'acquisition`. Aucune facture relative aux prestations contenues dans le coffret n'est emise a ce stade.

Le processus de facturation des prestations commence uniquement apres leur execution. Il remplace le processus de facturation par achat de l'Epic 14.

## Fondement fiscal a faire valider

L'article 256 ter du CGI prevoit que, pour un bon a usages multiples, la prestation effective realisee en echange du bon est soumise a la TVA, tandis que les transferts anterieurs du bon ne sont pas soumis a la TVA en tant que tels.

Le justificatif d'acquisition doit donc expliquer pourquoi il ne constitue pas une facture des prestations sous-jacentes. Le principe et la formulation definitive restent a valider par Juridica et le conseil comptable.

### Mention de travail versionnee

> **Justificatif d'acquisition d'un bon a usages multiples**
>
> Ce document atteste de l'acquisition d'un coffret Localeo constituant un bon
> a usages multiples. Il ne constitue pas une facture des biens ou prestations
> susceptibles d'etre fournis lors de son utilisation et ne comporte aucune TVA
> facturee au titre de ces operations sous-jacentes. La TVA applicable est
> determinee lors de la fourniture effective du bien ou de la prestation par le
> commercant concerne. Les eventuels frais ou services propres factures par
> Localeo font, le cas echeant, l'objet d'un document distinct.

Cette mention s'appuie sur la doctrine BOFiP selon laquelle les transferts d'un
BUM precedant son utilisation ne sont pas soumis a la TVA en tant que tels et
les documents eventuellement emis a cette occasion ne comportent aucune TVA
facturee. La taxation intervient lors de la fourniture effective. Sources de
travail : [BOI-TVA-CHAMP-10-10-40-50](https://bofip.impots.gouv.fr/bofip/11738-PGP.html/identifiant%3DBOI-TVA-CHAMP-10-10-40-50-20240214)
et [BOI-TVA-BASE-20-40](https://bofip.impots.gouv.fr/bofip/127-PGP.html/identifiant%3DBOI-TVA-BASE-20-40-20230118).

Elle reste une proposition a valider par Juridica et le conseil comptable avant
activation. Le titre et chaque paragraphe sont portes par une configuration
versionnee avec `version`, `status`, `effective_from`, `approved_by`,
`approved_at` et `content_hash`. Le document snapshotte la version utilisee ;
une modification ulterieure ne reecrit jamais un justificatif emis.

Il faut notamment confirmer :

- l'emploi du terme `bon a usages multiples` sur le document client ;
- la mention eventuelle de l'article 256 ter du CGI ;
- le traitement et le document applicables aux eventuels frais propres a Localeo ;
- les obligations documentaires distinctes en B2C et en B2B.

## Decommissionnement du processus actuel

Les fonctions suivantes ne doivent plus etre accessibles apres activation de l'Epic 50 :

- generation de `FACTURE_COMMERCANT` depuis un achat paye ;
- generation du pack `PACK_FACTURES_ZIP` par achat ;
- formulation selon laquelle Localeo emet la facture au nom et pour le compte du commercant ;
- demande de facturation creee depuis le formulaire de support sans prestation executee ;
- invitation, dans les emails d'achat, a demander les factures de toutes les prestations contenues dans le coffret.

La facture des frais propres a Localeo doit etre arbitree separement. Elle ne doit pas etre supprimee par assimilation avec la facture de prestation commercant.

Comme aucun coffret n'a ete commercialise, le decommissionnement est one-shot : aucune compatibilite fonctionnelle avec l'ancien parcours n'est requise.

## Condition d'ouverture d'une demande

Une personne peut demander une facture uniquement pour une prestation dont l'execution est materialisee par une `ValidationPrestation` active.

```text
ValidationPrestation existe
AND validation non annulee
AND demande active pour cette validation absente
```

Le demandeur peut etre :

- un particulier ayant achete ou reçu le coffret ;
- un client professionnel rattache a l'achat groupe ;
- un partenaire ou organisateur depuis Localeo Animation.

Les droits exacts doivent tenir compte de la relation entre acheteur et beneficiaire : l'acces au coffret ne doit pas permettre de demander une facture au nom d'une autre personne sans mandat ou informations de facturation adaptees.

## Points d'entree

### Particulier

Depuis la vue detaillee de son coffret :

- afficher les prestations executees ;
- proposer `Demander une facture` pour chaque prestation eligible ;
- afficher ensuite le statut et le document fourni.

### Achat professionnel

Depuis la vue detaillee de la commande ou du coffret multi :

- afficher les consommations de tous les coffrets rattaches a la commande ;
- conserver chaque prestation comme ligne unitaire eligible et tracable ;
- permettre `Demander les factures disponibles` ;
- creer une demande multi-lignes par couple `achat_pro + commercant` et permettre
  une demande complementaire pour les prestations executees plus tard.

Une demande groupee ne contient qu'un seul commercant, un seul acheteur, une
seule devise et un seul snapshot de facturation. Le document fourni declare
explicitement les lignes couvertes. Une ligne deja couverte par une facture
valide ne peut pas etre rattachee a une autre demande active.

Une facture mise a disposition est immuable. Une erreur est corrigee par un
document correctif ou un avoir reference, jamais par remplacement silencieux du
fichier. En V1, le depot accepte uniquement un PDF de 10 Mo maximum, controle
son type reel, calcule son empreinte SHA-256 et applique l'analyse antivirus du
socle documentaire avant publication.

### Localeo Animation

Depuis le suivi de la commande de lots :

- afficher les prestations executees issues des lots attribues ;
- permettre la demande au partenaire habilite ;
- afficher les demandes et factures mises a disposition pour cette animation.

## Donnees transmises au commercant

Localeo doit fournir les informations utiles sans calculer a la place du commercant la TVA, le HT ou la TVA due sur sa prestation.

### Identification de la demande

- reference unique de demande ;
- date de demande ;
- source `MARKETPLACE`, `PRO_ORDER` ou `ANIMATION` ;
- reference de commande et, le cas echeant, reference d'animation ;
- commentaire du demandeur.

### Prestation executee

- identifiant et date de `ValidationPrestation` ;
- reference de l'instance de coffret ;
- nom du coffret ;
- libelle et description snapshottee de la prestation ;
- version de prestation executee ;
- montant brut TTC facturable de la prestation, commission Localeo separee et montant net reverse ;
- preuve ou reference de validation, sans exposer le secret QR ;
- lieu ou etablissement concerne lorsqu'il est connu.

### Destinataire de la facture

- type d'acheteur ;
- nom et prenom ou raison sociale ;
- SIRET et numero de TVA lorsqu'applicables ;
- adresse de facturation ;
- email de facturation ;
- contact ;
- reference interne, bon de commande, engagement ou code service lorsqu'applicables.

Toutes ces informations sont figees dans `billing_snapshot` lors de la demande. Une modification ulterieure du profil ne change pas une demande deja transmise.

## Montant facture par le commercant

### Regle retenue

Le commercant facture la valeur brute TTC contractuelle de la prestation effectivement executee, avant deduction de la commission Localeo. Il ne facture ni le prix complet du coffret lorsqu'il contient d'autres prestations, ni le seul montant net reçu apres commission.

La commission Localeo constitue une operation separee, documentee par une facture Localeo au commercant lorsqu'elle est due. Le reversement correspond au montant brut facturable diminue de la commission TTC Localeo.

La cible commerciale est une commission equivalente a `15 % TTC` du montant brut TTC de la prestation executee. Le montant de commission etant deja configurable dans Localeo, l'Epic 50 reutilise cette configuration comme source de verite et n'introduit pas un second taux concurrent.

```text
commissionLocaleoTtc = montantConfigureEtSnapshotte

commissionLocaleoTtcCible
  = arrondiMonetaire(montantPrestationFacturableTtc * 15 / 100)

montantNetReverse
  = montantPrestationFacturableTtc
  - commissionLocaleoTtc
```

Le BackOffice affiche l'ecart eventuel entre le montant configure et la cible de 15 %, sans recalculer silencieusement la configuration existante. Le choix de rendre cet ecart bloquant reste une regle de gouvernance commerciale.

La commission configuree est TTC : Localeo doit en extraire et acquitter la TVA applicable. La TVA n'est donc pas ajoutee une seconde fois. Les montants HT et TVA sont calcules a partir du TTC selon le taux de TVA Localeo en vigueur, puis snapshottes au moment de l'execution.

Exemple :

```text
Prestation executee                          30,00 EUR TTC
Commission Localeo 15 % TTC                   4,50 EUR TTC
Facture du commercant au demandeur           30,00 EUR TTC
Facture de commission Localeo au commercant   4,50 EUR TTC
Reversement net au commercant                25,50 EUR
```

Avec une TVA Localeo a 20 %, la commission de `4,50 EUR TTC` se ventile en `3,75 EUR HT` et `0,75 EUR` de TVA. Cette ventilation est propre a la commission Localeo et ne determine pas la TVA de la prestation du commercant.

### Evolution du modele existant

Le champ actuel `montant_reversement` est ambigu s'il sert a la fois de valeur de prestation, de montant de facture et de net verse. Le modele cible doit separer :

```text
montantPrestationFacturableTtc
commissionLocaleoTtcConfiguree
commissionLocaleoTtcCible15Pourcent
commissionLocaleoHt
commissionLocaleoTva
commissionLocaleoTtc
montantNetReverse
```

Ces valeurs sont snapshottees sur la version de prestation, la consommation et la demande de facture. Les contraintes garantissent la coherence arithmetique, sans calculer le taux de TVA de la prestation a la place du commercant.

### Facture acquittee par le BUM

La facture de prestation doit pouvoir indiquer que son reglement est deja intervenu au moyen du coffret :

```text
Total TTC de la prestation        30 EUR
Reglement par coffret Localeo    -30 EUR
Net a payer                        0 EUR
```

Pour une entite publique, le cadre Chorus Pro correspondant a une facture deja payee, notamment le cadre `A2`, doit etre confirme par Juridica, la comptabilite et la recette Chorus Pro avant mise en production.

## Traitement par le commercant

Le commercant reçoit une notification lors de la creation de la demande et accede a la section Finance de son application.

```text
REQUESTED -> ACKNOWLEDGED -> PROCESSING -> PROVIDED
       \                            /
                    CANCELLED
```

Pour terminer la demande, le commercant choisit l'un des deux modes :

- televerser une facture deja emise dans son outil habituel, avec son numero et
  sa date ;
- utiliser l'assistant de facturation Localeo decrit ci-dessous.

Dans les deux cas, Localeo conserve au minimum :

- le document facture ;
- le numero de facture ;
- la date de facture ;
- la date de mise a disposition ;
- eventuellement un commentaire.

Localeo conserve le document et ses metadonnees mais ne calcule ni ne valide automatiquement le traitement TVA applique par le commercant.

## Assistant de facturation commercant

### Positionnement

L'assistant facilite la saisie mais ne transfere pas a Localeo la responsabilite
d'emission. Localeo pre-remplit un brouillon depuis les snapshots immuables de
la demande. Le commercant authentifie controle, complete puis declenche
explicitement l'emission en son nom et sous sa responsabilite.

L'interface utilise le terme `Assistant de facturation`. Le document identifie
le commercant comme vendeur ou prestataire. Une mention discrete peut indiquer
`Document genere avec Localeo`, sans presenter Localeo comme l'emetteur de la
facture de prestation.

### Cycle de vie

```text
DRAFT -> ISSUED
   \
    -> CANCELLED
```

- `DRAFT` : modifiable, sans numero fiscal definitif, non telechargeable par le
  demandeur et jamais transmis comme facture ;
- `ISSUED` : numero attribue, snapshot et PDF figes, mise a disposition du
  demandeur ;
- `CANCELLED` : brouillon abandonne sans consommation de numero.

La commande d'emission verrouille le brouillon et la sequence, attribue le
numero, snapshotte les donnees et cree la demande de rendu dans une seule
transaction metier. Le rendu PDF est rejouable : lorsqu'il est disponible, une
seconde transaction rattache le document, marque la demande `PROVIDED` et cree
l'evenement de notification. Un replay retourne toujours la meme facture et le
meme numero.

### Donnees pre-remplies et confirmation

L'assistant propose :

- l'identite et les coordonnees du commercant ;
- l'identite du destinataire issue du snapshot de facturation ;
- la prestation, la date d'execution et le montant brut TTC ;
- le reglement deja effectue au moyen du coffret et le net a payer nul ;
- les references de commande, de demande et de prestation utiles.

Le commercant doit verifier ou renseigner :

- la date d'emission et, si necessaire, la date d'exigibilite ;
- son regime, son taux et ses montants de TVA ou la mention d'exoneration ;
- les mentions propres a son activite ;
- la serie de numerotation configuree ;
- les informations Chorus lorsque le destinataire est public.

Avant emission, une confirmation explicite indique que le commercant a verifie
les donnees et emet la facture sous sa responsabilite. Localeo conserve
l'utilisateur, la date, l'adresse IP selon la politique d'audit, la version du
formulaire, le snapshot confirme et l'empreinte du document.

### Numerotation et corrections

La numerotation appartient au commercant. Pour le mode assiste, Localeo gere
une serie dediee configuree pour ce commercant, chronologique, continue et
verrouillee en concurrence. Aucun numero n'est attribue a un brouillon. Le code
de serie et son point de depart sont acceptes par le commercant avant la
premiere emission et ne peuvent etre corriges que par une procedure BackOffice
auditee.

Une facture `ISSUED` est immuable. Une erreur donne lieu a un avoir ou a un
document correctif reference, avec une nouvelle numerotation conforme. Un
document ne peut jamais etre remplace silencieusement.

### Preparation de la facturation electronique

Le PDF est une representation du snapshot structure, pas la seule source de
donnees. Le modele conserve les champs necessaires a une future sortie
Factur-X, UBL ou CII et au raccordement d'une plateforme agreee. L'activation
du canal B2B electronique suivra le calendrier et les specifications de
l'administration :

- [mentions obligatoires d'une facture](https://www.economie.gouv.fr/entreprises/gerer-son-entreprise-au-quotidien/gerer-sa-comptabilite-et-ses-demarches/mentions-obligatoires-dune-facture-tout-savoir) ;
- [facturation electronique et plateformes agreees](https://www.impots.gouv.fr/facturation-electronique-et-plateformes-agreees).

Le cadre de numerotation, la qualification exacte de Localeo comme outil ou
tiers mandate et les mentions finales restent soumis a validation
Juridica/comptable avant activation (`BUM-ARB-49`).

## Notifications

### Creation de la demande

Destinataire : commercant concerne.

- email obligatoire en V1 ;
- notification dans l'application Commercant ;
- WebPush commercant si le canal est disponible et active ;
- aucun document fiscal joint avant traitement.

Le message contient la reference, le demandeur, la prestation, la date d'execution, le montant utile et un lien securise vers la demande.

### Mise a disposition de la facture

Destinataire : personne ou organisation ayant cree la demande.

- email obligatoire avec lien securise, plutot que piece jointe par defaut ;
- WebPush si Localeo Live est installe, configure et autorise ;
- disponibilite dans Localeo Animation si la demande provient d'un partenaire ;
- disponibilite dans la vue detaillee du coffret pour un particulier ;
- disponibilite dans la vue detaillee de la commande et la vue multi-coffrets pour un achat professionnel.

### Autres evenements recommandes

- rappel au commercant pour une demande non prise en charge ;
- notification au demandeur en cas d'annulation motivee ;
- notification en cas de remplacement du document ;
- audit des echecs et reprises d'envoi sans dupliquer la demande.

## Autorisations et confidentialite

- le commercant ne voit que les demandes qui le concernent ;
- le particulier ne voit que les demandes autorisees par son acces au coffret et son identite ;
- le client Pro ne voit que les commandes de son organisation ;
- le partenaire Animation ne voit que son tenant, sa commune et ses animations autorisees ;
- les URLs de facture sont protegees, temporaires ou servies apres controle d'autorisation ;
- les notifications ne contiennent pas de donnees fiscales sensibles inutiles ;
- le QR ou son secret ne sont jamais transmis au commercant dans le dossier de facturation.

## Modele cible contextualise

`DemandeFacturationAchatOrm` est migree vers un modele tel que :

```text
DemandeFactureCommercant
  id
  reference
  commercantId
  requesterType
  requesterId
  source
  orderId
  billingSnapshot
  status
  requestedAt
  acknowledgedAt
  providedAt
  cancelledAt
  invoiceDocumentId
  invoiceNumber
  invoiceDate
  comment
```

```text
DemandeFactureCommercantLigne
  id
  demandeId
  validationPrestationId
  prestationSnapshot
  montantPrestationFacturableTtcSnapshot
  commissionLocaleoTtcSnapshot
  montantNetReverseSnapshot
```

La contrainte anti-doublon doit porter sur `validationPrestationId` pour les demandes actives.

## Integration Chorus Pro

### Decision produit

Localeo prend en charge le depot Chorus Pro dans deux situations :

1. facture emise par Localeo a une entite publique, notamment pour un abonnement ;
2. facture de prestation emise par un commercant apres execution, deposee par Localeo pour son compte lorsque le demandeur est une entite publique.

Le commercant reste l'emetteur legal et fiscal de sa facture de prestation. Localeo agit uniquement comme mandataire ou operateur technique de depot et ne modifie pas les montants, taux ou mentions fournis.

### Prerequis organisationnels

- valider avec Juridica le mandat autorisant Localeo a deposer au nom du commercant ;
- versionner le mandat et conserver acceptation, date, acteur et perimetre ;
- definir la responsabilite en cas de rejet, erreur de facture ou correction ;
- rattacher chaque commercant concerne a une structure emettrice Chorus Pro identifiable ;
- habiliter les operateurs Localeo autorises a effectuer et enregistrer les depots manuels ;
- documenter la procedure de depot, de suivi, de correction et de remplacement d'un operateur.

### Donnees de l'entite publique destinataire

Le profil de facturation et son snapshot utilisent en V1 la liste minimaliste
suivante :

```text
buyerType = PUBLIC_ENTITY
legalName
siret
chorusRecipientCode (= siret en V1)
chorusDirectoryCheckedAt
chorusRecipientActive
chorusServiceCode
chorusServiceCodeRequired
legalCommitmentNumber
legalCommitmentRequired
```

Le `legalName`, le SIRET destinataire et le controle d'une structure active sont
toujours requis. Le code service et le numero d'engagement juridique sont
conditionnels aux parametres publies par la structure ou le service dans
l'annuaire Chorus Pro. Leur absence ou leur valeur invalide bloque le depot
uniquement lorsqu'ils sont declares obligatoires.

`purchaseOrderReference`, `contractNumber`, `marketNumber`, `billingAddress`,
`billingEmail` et `contactName` restent disponibles comme donnees facultatives
ou comme informations imposees par le contexte contractuel ; elles ne sont pas
des prerequis Chorus generiques du MVP. Le snapshot conserve les indicateurs
d'obligation observes et la date de consultation de l'annuaire. Cette regle est
alignee sur le [guide officiel de l'annuaire Chorus Pro](https://communaute.chorus-pro.gouv.fr/documentation/guide-dutilisation-de-lannuaire-des-structures-publiques-dans-chorus-pro/).

### Donnees de l'emetteur commercant

```text
issuerLegalName
issuerSiret
issuerVatNumber
issuerAddress
issuerBankDetailsReference
chorusStructureId
localeoMandateId
localeoMandateVersion
localeoMandateAcceptedAt
localeoMandateStatus
```

Les coordonnees bancaires et autres donnees sensibles ne doivent pas etre copiees dans les notifications. Leur format exact et leur necessite sont confirmes pendant la conception du dossier de depot.

### Donnees de facture a deposer

```text
invoiceNumber
invoiceDate
currency
invoiceType
invoicingFramework
totalExcludingTax
totalTax
totalIncludingTax
amountToPay
paymentTerms
issuerReference
recipientReference
purchaseOrderReference
legalCommitmentNumber
serviceCode
invoiceDocumentId
supportingDocumentIds[]
```

La facture et ses montants sont fournis et valides par l'emetteur. Localeo controle la completude technique, pas la justesse fiscale.

### Suivi technique du depot

Creer un objet de suivi distinct de la demande fonctionnelle, compatible avec un futur depot automatise :

```text
ChorusDeposit
  id
  invoiceRequestId
  invoiceDocumentId
  issuerType
  issuerId
  recipientSiret
  depositMode
  status
  chorusInvoiceId
  chorusFlowId
  submittedAt
  lastCheckedAt
  acceptedAt
  rejectedAt
  rejectionCode
  rejectionReason
  attemptCount
  idempotencyKey
  depositedBy
  technicalMetadata
```

Statuts Localeo proposes :

```text
A_DEPOSER
DEPOSEE
ACCEPTEE
SUSPENDUE
REJETEE
MISE_EN_PAIEMENT
PAYEE
ANNULEE
```

L'operateur reporte l'identifiant et le statut constates dans Chorus Pro. Les codes bruts sont conserves dans les metadonnees, puis traduits dans un statut Localeo stable.

### Orchestration

```text
Facture mise a disposition par le commercant
              |
      destinataire public ?
          /           \
        non            oui
        |               |
notification       controle annuaire,
demandeur          mandat et references
                        |
               depot manuel Chorus Pro
                        |
             suivi accepte / suspendu / rejete
                        |
             notifications et actions de correction
```

- une file BackOffice regroupe les factures `A_DEPOSER` ;
- l'operateur telecharge le PDF et copie les references preparees par Localeo ;
- apres depot sur le portail, il enregistre identifiant Chorus, date et statut ;
- un controle empeche de marquer deux fois la meme facture comme deposee sans action explicite de correction ;
- un rejet ne doit pas etre redepose sans correction du document ou des references ;
- l'acceptation Chorus Pro et la mise a disposition Localeo sont deux statuts distincts ;
- le demandeur et le commercant sont informes des rejets necessitant une action ;
- tous les depots, consultations, corrections et telechargements sont audites.

### Factures d'abonnement Localeo

La meme file BackOffice Chorus Pro est reutilisee lorsque Localeo facture directement une entite publique pour un abonnement. Dans ce cas :

- Localeo est l'emetteur, pas le mandataire du commercant ;
- la facture provient du domaine abonnement et conserve sa propre reference ;
- le destinataire, le service et l'engagement utilisent le meme profil public ;
- le suivi du depot utilise `ChorusDeposit` ;
- les droits, documents et ecritures restent separes des demandes de facture de prestation.

## Criteres d'acceptation

- aucun processus ne genere une facture commercant lors de l'achat ;
- aucun brouillon assiste ne recoit de numero ou n'est transmis avant la
  confirmation explicite du commercant ;
- deux confirmations concurrentes ou rejouees produisent une seule facture et
  un seul numero ;
- une facture assistee emise est immuable et sa correction est referencee ;
- l'achat genere uniquement le justificatif d'acquisition attendu, hors document propre a d'eventuels frais Localeo ;
- aucune demande n'est possible sans prestation validee et non annulee ;
- particulier, Pro et partenaire Animation disposent du point d'entree adapte ;
- le commercant reçoit les donnees suffisantes et une notification ;
- le commercant peut fournir sa facture et en reste responsable ;
- le demandeur est notifie par email et, si disponible, par WebPush ;
- la facture est disponible sur la surface d'origine et dans les vues de suivi appropriees ;
- aucun autre client, commercant ou tenant ne peut consulter la demande ou le document ;
- chaque transition, notification et telechargement sensible est audite.
- une facture destinee a une entite publique apparait dans une file BackOffice et est deposee manuellement par un operateur Localeo ;
- Localeo peut deposer ses factures d'abonnement et, sous mandat, les factures emises par les commercants ;
- les champs obligatoires du destinataire sont controles depuis les parametres Chorus Pro ;
- les identifiants et statuts de depot sont suivis sans confondre demande, facture et soumission ;
- les rejets fonctionnels sont presentes aux acteurs avec une action de correction ;
- aucune information d'authentification Chorus Pro n'apparait dans les journaux ou les notifications ;
- le modele permet de remplacer ulterieurement le depot manuel par une API ou un operateur sans modifier le workflow metier.

### Evolution V2

Une integration API PISTE OAuth2 ou le recours a un operateur deja raccorde est hors perimetre V1. Elle pourra automatiser la creation et le suivi des depots en reutilisant `ChorusDeposit`, les snapshots et les statuts stables de Localeo.
