# Epic 50 - Specification fonctionnelle

## 1. Objet et statut

Cette specification constitue la reference fonctionnelle de l'Epic 50. Elle
decrit la qualification fiscale BUM des coffrets, les documents d'acquisition,
le cycle financier apres consommation, les demandes de facture, les factures
emises par Localeo, le credit d'achat B2B et l'onboarding terrain des
commercants avec `Localeo OnBoard`.

Statut : `Pret pour implementation par lots`. Les validations externes encore
ouvertes sont des conditions d'activation des fonctions concernees, pas des
blocages de conception ou de developpement.

## 2. Objectifs

- ne commercialiser que des coffrets qualifies `MULTI_PURPOSE` et valides ;
- distinguer l'acquisition du bon, l'execution de la prestation, le reversement
  et les differents documents de facturation ;
- conserver une preuve versionnee de chaque decision fiscale et financiere ;
- permettre au commercant de fournir une facture externe ou de l'emettre avec
  un assistant, sous son controle et sa responsabilite ;
- emettre les factures de commission et d'abonnement dues a Localeo ;
- traiter les destinataires publics et le depot manuel Chorus Pro ;
- convertir en credit B2B la part eligible des prestations non consommees ;
- guider l'equipe Localeo pendant l'onboarding d'un commercant et rendre ses
  capacites operationnelles explicites.

## 3. Acteurs

| Acteur | Responsabilites principales |
| --- | --- |
| Administrateur Localeo | Qualifier, superviser, corriger, publier, auditer et traiter les exceptions |
| Equipe commerciale Localeo | Realiser l'onboarding depuis `Localeo OnBoard` avec le profil `Localeo Admin` du MVP |
| Commercant | Fournir ses informations et preuves, accepter les engagements, executer la prestation et transmettre sa facture |
| Acheteur particulier | Acheter le coffret, consulter son justificatif et demander une facture apres consommation |
| Acheteur Pro | Acheter, consulter le justificatif, demander les factures et utiliser son credit d'achat |
| Partenaire Animation | Acheter des lots, consulter documents et factures, demander les factures et utiliser son credit |
| Juridica / Finance | Valider les formulations, politiques et traitements identifies dans le registre |
| Stripe Connect | Verifier le compte de paiement et executer les reversements |
| Chorus Pro | Recevoir les factures destinees aux entites publiques |

## 4. Vocabulaire fonctionnel

| Terme | Definition |
| --- | --- |
| BUM | Bon a usages multiples : la TVA de la prestation sous-jacente est determinee lors de sa fourniture effective |
| BUU | Bon a usage unique, non commercialisable dans le perimetre cible |
| Screening | Evaluation automatique d'eligibilite, sans valeur de decision juridique definitive |
| Qualification | Decision historisee prise par un acteur habilite |
| Justificatif d'acquisition | Document d'achat du BUM, distinct d'une facture de prestation |
| Validation de prestation | Fait constatant l'execution de la prestation et ouvrant les traitements financiers associes |
| Demande de facture | Demande adressee au commercant pour une ou plusieurs prestations executees |
| Credit d'achat B2B | Solde ferme, non remboursable et non transferable, utilisable sur un futur achat B2B eligible |
| Capacite d'onboarding | Resultat serveur indiquant si une action operationnelle est possible ou bloquee |

## 5. Perimetre

### 5.1 Qualification et publication

Le systeme collecte les donnees factuelles utiles pour chaque prestation. Il
execute un diagnostic interne non decisionnel, puis permet a un administrateur
de prendre au niveau du coffret une decision motivee et historisee. Un
diagnostic central interdit toute publication lorsque la qualification est
absente, obsolete ou incompatible avec la politique BUM.

### 5.2 Acquisition et documents

Apres paiement, l'acheteur recoit un justificatif d'acquisition qui ne presente
pas la TVA des prestations sous-jacentes. Le document snapshotte l'identite des
parties, le contenu contractuel, les montants, la politique et le wording
utilises lors de son emission.

### 5.3 Execution, reversement et facture de prestation

La validation de la prestation constitue le fait generateur applicatif. Elle
fige le montant brut TTC, la commission Localeo TTC, sa ventilation et le net a
reverser. L'acheteur peut ensuite demander au commercant une facture portant sur
la prestation executee. Localeo orchestre et trace la demande, mais n'emet pas
la facture a la place du commercant. Celui-ci peut televerser une facture
externe ou utiliser un assistant qui prepare un brouillon puis exige sa
confirmation explicite avant numerotation, generation et mise a disposition.

### 5.4 Factures emises par Localeo

Localeo emet :

- la facture de commission adressee au commercant lors de la cloture d'une
  campagne de reversement ;
- la facture d'abonnement adressee au partenaire Animation apres confirmation
  du paiement.

Une facture emise est immuable. Toute correction passe par un avoir reference.

### 5.5 Entites publiques et Chorus Pro

Le profil public contient le SIRET destinataire et les obligations observees
dans l'annuaire Chorus Pro. Le code service et le numero d'engagement juridique
ne sont obligatoires que lorsque le destinataire les exige. Le MVP prepare et
suit un depot manuel ; une integration automatique est hors perimetre V1.

### 5.6 Credit d'achat B2B

A l'expiration d'un coffret Pro ou Animation, la part effectivement payee et
allouee aux prestations eligibles non consommees peut alimenter un compte de
credit. Le solde resulte exclusivement d'un registre de mouvements. Une
reservation temporaire protege le paiement mixte credit plus Stripe.

### 5.7 Onboarding commercant

`Localeo OnBoard` est une PWA interne en ligne utilisee pendant le rendez-vous.
Elle permet de reprendre un dossier, completer les donnees canoniques, collecter
les documents, preparer les prestations, verifier Stripe Connect, envoyer
l'invitation et calculer les capacites operationnelles. Le commercant teste son
acces sur son propre telephone sans communiquer son mot de passe.

## 6. Parcours fonctionnels

### PF-50-01 - Qualifier et publier un coffret

1. le commercant fournit les donnees factuelles de ses prestations et signe la convention partenaire applicable ;
2. le moteur produit un screening explique et versionne ;
3. l'administrateur accepte, refuse ou demande une revue ;
4. la qualification du coffret est calculee et historisee ;
5. la publication rejoue le diagnostic central ;
6. seules les offres `MULTI_PURPOSE / VALIDATED` sont publiees.

### PF-50-02 - Acheter et recevoir le justificatif

1. le canal controle la vendabilite avant le paiement ;
2. le paiement confirme emet les droits sans creer de dette commercant ;
3. le systeme snapshotte les donnees d'achat et la version documentaire ;
4. le justificatif est genere de maniere idempotente et mis a disposition.

### PF-50-03 - Executer, reverser et demander une facture

1. le commercant valide l'execution de la prestation ;
2. le systeme cree atomiquement le snapshot financier et le mouvement de
   reversement ;
3. la consommation devient eligible a une demande de facture ;
4. l'acheteur cree une demande unitaire ou groupee selon son parcours ;
5. le commercant depose un PDF existant ou verifie puis emet un brouillon
   prepare par l'assistant ;
6. l'acheteur est notifie et peut telecharger le document dans son perimetre.

### PF-50-04 - Emettre une facture Localeo

1. l'evenement economique est confirme ;
2. le snapshot fiscal et le numero sont crees atomiquement ;
3. le PDF est genere ou regenere de maniere idempotente ;
4. le destinataire consulte le document ;
5. une erreur ulterieure produit un avoir sans modifier la facture initiale.

### PF-50-05 - Crediter une expiration B2B

1. un traitement detecte le coffret expire ;
2. il exclut les prestations consommees, remboursees ou non eligibles ;
3. il calcule l'allocation en centimes sans depasser la base payee ;
4. il inscrit un mouvement de credit idempotent ;
5. l'organisation consulte puis reserve le solde lors d'une commande eligible ;
6. la confirmation consomme la reservation, tandis qu'un echec la libere.

### PF-50-06 - Onboarder un commercant

1. le commercial recherche le commercant et evite les doublons ;
2. il cree ou reprend le dossier affecte ;
3. `Localeo OnBoard` charge la checklist versionnee et conditionnelle ;
4. les informations et documents sont enregistres dans leurs referentiels
   canoniques ;
5. le backend recalcule les capacites et explique chaque blocage ;
6. le commercial envoie l'invitation ;
7. le commercant active et teste son compte sur son telephone ;
8. le dossier est valide ou cloture avec un plan d'actions restant.

## 7. Regles de gestion

| Identifiant | Regle |
| --- | --- |
| `E50-RG-001` | Le type commercial `SOLO / MULTI` ne determine jamais la qualification fiscale |
| `E50-RG-002` | Seul un coffret `MULTI_PURPOSE / VALIDATED` peut etre publie sur un canal |
| `E50-RG-003` | Une donnee incomplete produit une revue, jamais une validation automatique |
| `E50-RG-004` | Toute decision conserve politique, regles, donnees sources, acteur, date et motif |
| `E50-RG-005` | Une modification substantielle impose une requalification et bloque les nouvelles ventes |
| `E50-RG-006` | Une requalification ne retire pas les droits deja acquis par les acheteurs |
| `E50-RG-007` | L'achat n'ouvre aucun droit au reversement avant consommation validee |
| `E50-RG-008` | Justificatif BUM, facture commercant et facture Localeo sont des objets distincts |
| `E50-RG-009` | Le commercant facture le brut TTC de la prestation ; Localeo facture separement sa commission TTC |
| `E50-RG-010` | Le reversement correspond au brut TTC diminue de la commission configuree |
| `E50-RG-011` | Une validation ne peut appartenir qu'a une demande de facture non annulee |
| `E50-RG-012` | Une facture emise ne peut etre modifiee ; une correction cree un avoir |
| `E50-RG-013` | Le code service et l'engagement Chorus sont conditionnels aux exigences du destinataire |
| `E50-RG-014` | Le credit ne depasse jamais la part payee allouee aux prestations eligibles non consommees |
| `E50-RG-015` | Le credit B2B est non remboursable, non transferable et limite a l'acheteur contractuel en V1 |
| `E50-RG-016` | Le solde de credit est calcule depuis les mouvements confirmes, sans mise a jour directe |
| `E50-RG-017` | Une case cochee dans OnBoard ne remplace ni une preuve ni un diagnostic serveur |
| `E50-RG-018` | Les actions de publication, qualification, activation et invitation sont explicites et auditees |
| `E50-RG-019` | Aucun contrat, mot de passe ou token d'invitation n'est conserve durablement sur le telephone |
| `E50-RG-020` | La connexion est testee par le commercant sur son appareil, sans partage de secret avec Localeo |
| `E50-RG-021` | L'assistant de facturation est facultatif et l'upload d'une facture externe reste disponible |
| `E50-RG-022` | Un brouillon assiste n'est ni numerote, ni emis, ni transmis au demandeur |
| `E50-RG-023` | Seul le commercant authentifie peut confirmer qu'il emet la facture sous sa responsabilite |
| `E50-RG-024` | La confirmation attribue atomiquement un numero dans une serie propre au commercant et genere le document |
| `E50-RG-025` | Le commercant confirme explicitement les donnees fiscales ; Localeo ne choisit pas son taux ou son regime de TVA |
| `E50-RG-026` | Une facture assistee emise est immuable et toute correction utilise un avoir ou un document correctif reference |

## 8. Etats et transitions

### 8.1 Qualification

| Etat | Transitions autorisees |
| --- | --- |
| `PENDING` | `VALIDATED`, `REJECTED` |
| `VALIDATED` | `REQUALIFICATION_REQUIRED` |
| `REJECTED` | `PENDING` apres correction |
| `REQUALIFICATION_REQUIRED` | `PENDING` |

### 8.2 Demande de facture

| Etat | Transitions autorisees |
| --- | --- |
| `REQUESTED` | `ACKNOWLEDGED`, `CANCELLED` |
| `ACKNOWLEDGED` | `PROCESSING`, `CANCELLED` |
| `PROCESSING` | `PROVIDED`, `CANCELLED` |
| `PROVIDED` | terminal ; correction par nouveau document reference |
| `CANCELLED` | terminal ; une nouvelle demande peut etre creee |

### 8.3 Dossier d'onboarding

`BROUILLON -> RDV_PLANIFIE -> EN_COURS -> PRET_A_VALIDER -> VALIDE ->
CLOTURE`.

`A_COMPLETER` peut etre atteint depuis `EN_COURS` ou `PRET_A_VALIDER`.
`ABANDONNE` est terminal et exige un motif. Une validation recalcule toujours
les capacites dans la transaction.

### 8.4 Facture commercant assistee

`DRAFT -> ISSUED` ou `DRAFT -> CANCELLED`. `ISSUED` et `CANCELLED` sont
terminaux. Le numero definitif n'existe qu'apres la transition atomique vers
`ISSUED`. Une correction d'une facture emise cree une nouvelle piece
referencee et ne modifie jamais l'original.

## 9. Capacites d'onboarding

Le backend retourne pour chaque capacite `READY`, `BLOCKED` ou
`NOT_APPLICABLE`, avec les causes et prochaines actions :

- `PORTAIL_VISIBLE` ;
- `PRESTATION_PUBLIABLE` ;
- `COFFRET_PUBLIABLE` ;
- `BUM_READY` ;
- `COMMISSION_BILLABLE` ;
- `INVOICE_REQUEST_READY` ;
- `PAYOUT_READY` ;
- `PORTAL_ACCESS_READY`.

La checklist minimale propose contrat signe incluant les clauses BUM,
immatriculation verifiee, acceptation de la commission, profil
fiscal/facturation et preparation Stripe. OnBoard collecte et controle les
elements BUM mais ne porte aucune attestation contractuelle autonome. Le RIB,
les justificatifs reglementaires et les droits medias sont conditionnels. Cette
politique reste configurable et soumise a validation Juridica/Finance avant
activation.

## 10. Autorisations

- le BackOffice et `Localeo OnBoard` utilisent le profil `Localeo Admin` dans
  le MVP ;
- le commercant accede uniquement a ses demandes, documents et donnees ;
- un acheteur accede uniquement aux achats, demandes et credits de son
  perimetre verifie ;
- un partenaire Animation est limite a son partenaire et a sa commune ;
- chaque telechargement de document refait le controle d'autorisation ;
- l'introduction future de profils BackOffice differencies ne doit pas modifier
  les contrats metier.

## 11. Exigences non fonctionnelles

- toutes les mutations rejouables acceptent une cle d'idempotence ;
- les montants sont calcules en centimes ou en `Decimal`, jamais en flottants ;
- les contraintes d'unicite critiques sont garanties en base ;
- les documents sont servis apres autorisation par URL courte signee ;
- les donnees fiscales et financieres utilisees sont snapshottees ;
- les actions sensibles produisent un evenement d'audit ;
- les notifications sont asynchrones et dedupliquees ;
- les nouveaux controles peuvent etre actives progressivement par feature flag ;
- l'application OnBoard ne fonctionne pas hors ligne dans le MVP.

## 12. Hors perimetre V1

- qualification juridique entierement automatique ;
- commercialisation de coffrets BUU ;
- emission par Localeo d'une facture au nom du commercant ;
- calcul par Localeo de la TVA propre a la prestation executee ;
- integration automatique a l'API Chorus Pro ;
- credit pour les particuliers, remboursement en especes ou transfert de credit ;
- stockage hors ligne de documents dans `Localeo OnBoard` ;
- gestion de profils BackOffice differencies.

## 13. Criteres d'acceptation transverses

- aucun canal ne publie ou ne vend un coffret non conforme ;
- les droits acquis restent utilisables apres une requalification ;
- un paiement seul ne cree aucun reversement commercant ;
- une validation rejouee ne cree ni second mouvement ni seconde demande ;
- une confirmation d'emission rejouee retourne la meme facture et le meme
  numero sans consommer une nouvelle valeur de sequence ;
- le justificatif ne se presente pas comme facture des prestations ;
- une facture et son snapshot restent identiques apres modification du catalogue ;
- aucune ligne de consommation n'est facturee deux fois ;
- un acces croise a un document ou a un credit est refuse ;
- deux traitements concurrents ne peuvent consommer le meme credit ;
- OnBoard explique chaque capacite bloquee et ne contourne aucun invariant ;
- les transitions, telechargements et corrections sensibles sont auditables.

## 14. Tracabilite produit

| Capacite | User Stories | Documents detailles |
| --- | --- | --- |
| Politique, screening et publication | `PRD-448` a `PRD-455` | `registre-arbitrages.md`, `analyse-existant-impacts.md` |
| Justificatif et profils acheteur | `PRD-456` a `PRD-458` | `workflow-demandes-factures.md` |
| Execution, demandes et assistant de facturation | `PRD-459` a `PRD-463`, `PRD-560` | `workflow-demandes-factures.md` |
| Administration et qualite | `PRD-464` a `PRD-466` | `conception-technique.md` |
| Chorus Pro | `PRD-467` a `PRD-469` | `workflow-demandes-factures.md` |
| Factures Localeo | `PRD-470` a `PRD-473` | `factures-localeo.md` |
| Credit d'achat B2B | `PRD-474` a `PRD-478` | `credit-achat-b2b.md` |
| Localeo OnBoard | `PRD-551` a `PRD-559` | `onboarding-commercant-mobile.md` |

## 15. Conditions d'activation encore ouvertes

| Arbitrage | Condition | Fonctions concernees |
| --- | --- | --- |
| `BUM-ARB-08` | Validation Juridica/comptable du wording | Justificatif d'acquisition |
| `BUM-ARB-14` | Recette de la liste conditionnelle | Depot Chorus Pro |
| `BUM-ARB-45` | Validation Juridica/Finance des preuves | Checklist OnBoard |
| `BUM-ARB-49` | Validation Juridica/comptable du cadre de numerotation, d'emission assistee et de facturation electronique | Assistant de facturation commercant |
| `BUM-ARB-27`, `29`, `30`, `32`, `40` | Validations juridique, comptable et contractuelle | Credit d'achat B2B |

Les valeurs correspondantes sont externalisees, versionnees et desactivees en
production tant que leur validation n'est pas referencee.
