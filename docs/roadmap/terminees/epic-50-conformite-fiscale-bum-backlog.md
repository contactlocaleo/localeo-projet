# Backlog Epic 50 - Politique BUM et conformite fiscale des coffrets

## Synthese

- Criticite : `Haute`
- Statut : `Implementation backend terminee - decision interne Localeo, controles Finance applicables et recettes externes requis avant activation production`
- Objectif : garantir que les coffrets commercialises par Localeo respectent la politique de Bons a Usages Multiples (BUM), tracer leur qualification, distinguer l'acquisition du bon de l'execution puis de la facturation de la prestation, et industrialiser l'onboarding terrain des commercants.
- Epic source : note de cadrage `EPIC_BUM_Conformite_Fiscale_Localeo.md` du 24 aout 2026.
- Dependances : Epics 1, 13, 14, 39, 41 et 46 ; catalogue, Marketplace, commandes B2C/Pro/Animation, Stripe Connect et application Commercant.
- Surfaces ciblees : Backend, BackOffice, Marketplace, Localeo Animation, espace Pro, application Commercant et application mobile interne `Localeo OnBoard`.

## Avancement d'implementation au 2 septembre 2026

Livre dans le backend :

- politiques BUM versionnees, diagnostic interne configurable des donnees de prestations et qualifications fiscales de coffrets historisees ;
- migration initiale idempotente `BUM_POLICY_2026_01` et qualification `MULTI_PURPOSE / VALIDATED` du catalogue existant avec l'acteur `SYSTEM_MIGRATION` ;
- API interne de politique, diagnostic des donnees de prestation, qualification de coffret et diagnostic de vendabilite ;
- garde central de vendabilite BUM, desactive par defaut, et passage automatique en `REQUALIFICATION_REQUIRED` apres modification du contenu d'une prestation ;
- neutralisation de la generation nouvelle du pack de factures commercant au paiement, avec maintien de la consultation individuelle des documents historiques ;
- profils de facturation et demandes de facture post-prestation avec anti-doublon, snapshots serveur, transitions versionnees et depot PDF par le commercant ;
- presentation contractuelle distinguant promesse garantie et contenu indicatif, avec wording Marketplace versionne ;
- justificatif d'acquisition BUM issu de la chaine documentaire existante, avec politique, wording, contexte et empreinte figes ;
- snapshot financier immuable sur le mouvement de reversement : brut TTC, commission Localeo HT/TVA/TTC, taux effectif, cible de 15 %, ecart, net et devise ;
- indicateurs d'activation, controles de dependance, readiness conditionnelle et tests cibles.

Tous les lots backend de l'Epic sont livres, y compris Localeo OnBoard,
l'assistant de facture, Chorus Pro manuel, les factures Localeo, le credit B2B
et les demandes groupees. Les applications clientes disposent des contrats API
necessaires ; leur composition visuelle eventuelle releve de leurs depots.

Restent des portes d'activation, et non des travaux d'implementation de ce
depot : decision interne Localeo sur les wordings et doctrines, controles
Finance applicables, recettes Stripe et Chorus, puis go/no-go d'exploitation.
Localeo peut solliciter un avis de conseil Juridica, sans que cet avis constitue
une validation engageant la responsabilite de Juridica.

## Ancrage dans l'existant

- `diagnostiquer_blocages_vendabilite_coffret` protege deja la Marketplace et l'initialisation du paiement : la qualification BUM devient un blocage supplementaire de ce controle central ;
- `PrestationCoffretVersionOrm` fournit le versionnement editorial a enrichir avec le questionnaire fiscal ;
- `ValidationPrestation` cree deja atomiquement le `MouvementReversement` lors de la consommation : ce flux est conserve ;
- les snapshots, `DocumentAchatCoffret`, le recu B2C et le recu Animation sont adaptes, pas recrees ;
- la generation de nouvelles factures commercants par achat issue de l'Epic 14 est neutralisee ; la consultation des documents historiques reste disponible ;
- `DemandeFacturationAchatOrm` est remplacee par la demande de facture au commercant rattachee aux prestations validees ; l'ancien concept de demande support de facturation n'est plus utilise ;
- `CommandeAchat` constitue deja la racine consolidee des lots Animation.

Voir [l'analyse detaillee de l'existant](../../specifications/epic-50-conformite-fiscale-bum/analyse-existant-impacts.md).
Voir [la specification fonctionnelle](../../specifications/epic-50-conformite-fiscale-bum/specification-fonctionnelle.md).
Voir [la checklist contractuelle](../../specifications/epic-50-conformite-fiscale-bum/checklist-contractuelle-bum-facturation.md).
Voir [la conception technique implementable](../../specifications/epic-50-conformite-fiscale-bum/conception-technique.md).
Voir [la conception du credit d'achat B2B](../../specifications/epic-50-conformite-fiscale-bum/credit-achat-b2b.md).
Voir aussi [le workflow du justificatif et des demandes de facture](../../specifications/epic-50-conformite-fiscale-bum/workflow-demandes-factures.md).
Voir aussi [la gestion des factures emises par Localeo](../../specifications/epic-50-conformite-fiscale-bum/factures-localeo.md).
Voir enfin [le parcours d'onboarding commercant mobile](../../specifications/epic-50-conformite-fiscale-bum/onboarding-commercant-mobile.md).

## Decision structurante

Tout coffret commercialise doit etre qualifie `MULTI_PURPOSE` et avoir un statut de qualification `VALIDATED`. La distinction commerciale `SOLO / MULTI` ne determine jamais la qualification fiscale `BUM / BUU`.

Le moteur applicatif realise un screening d'eligibilite, pas une qualification juridique definitive. Localeo assume la decision d'adopter et d'activer toute regle, mention fiscale ou donnee obligatoire susceptible de l'engager. Un avis Juridica peut eclairer cette decision sans constituer une validation engageant Juridica.

## Perimetre fonctionnel

1. collecter les donnees juridiques, fiscales et factuelles du partenaire ;
2. diagnostiquer en interne les donnees des prestations et qualifier uniquement les coffrets ;
3. bloquer toute publication non validee BUM sur tous les canaux ;
4. historiser les decisions, versions de politique et donnees sources ;
5. distinguer promesse garantie et contenu indicatif sur la Marketplace ;
6. produire un justificatif d'acquisition sans calcul de TVA sous-jacente ;
7. maintenir le cycle `paiement -> emission -> consommation -> reversement` ;
8. permettre, apres consommation validee, une demande de facture adressee au commercant ;
9. suivre ces demandes cote Pro, Animation, Commercant et BackOffice.
10. convertir en credit d'achat B2B la part eligible des prestations non utilisees lors de l'expiration d'un coffret et permettre son utilisation sur une future commande Pro ou Animation.
11. guider l'equipe commerciale pendant le rendez-vous d'onboarding, collecter les preuves et rendre explicites les capacites ouvertes ou bloquees du commercant.

## Hors perimetre V1

- revue manuelle ou campagne de requalification du catalogue existant : aucun coffret n'a encore ete ouvert a la commercialisation ;
- qualification juridique entierement automatique ;
- emission par Localeo d'une facture au nom du commercant ;
- calcul par Localeo de la TVA de la prestation executee ;
- facturation electronique interentreprises, integration PDP et automatisation Chorus Pro hors factures adressees aux entites publiques ;
- traitement comptable definitif des reliquats expires non creditables ou des credits arrives a echeance.
- credit d'achat pour les particuliers, retrait en especes ou transfert entre organisations.

## Regles metier invariantes

- publication autorisee uniquement si `taxQualification = MULTI_PURPOSE` et `qualificationStatus = VALIDATED` ;
- `UNKNOWN` ou une information incomplete conduit a une revue, jamais a une validation BUM automatique ;
- une modification substantielle peut placer l'offre en `REQUALIFICATION_REQUIRED` et la retirer de la publication ;
- le paiement d'un coffret ne declenche pas le reversement au commercant ;
- seule une consommation `VALIDATED` rend la prestation eligible au reversement et a une demande de facture ;
- une consommation ne peut appartenir qu'a une demande de facture active ;
- justificatif d'acquisition, facture de prestation et facture de commission Localeo restent trois objets distincts.
- le commercant facture le montant brut TTC de la prestation executee avant commission Localeo ; la commission est facturee separement et le reversement est net de cette commission ;
- le montant de commission deja configurable reste la source de verite ; il est exprime TTC, avec une cible commerciale de 15 % du montant brut TTC de la prestation ;
- Localeo extrait et acquitte la TVA incluse dans cette commission sans l'ajouter au montant configure ;
- aucun credit B2B ne peut exceder la part effectivement payee et allouee aux prestations non utilisees ;
- le solde de credit est calcule depuis un registre immuable de mouvements, jamais modifie directement.
- une case cochee par le client mobile ne remplace jamais un diagnostic serveur, une preuve contractuelle ou une decision habilitee ;
- l'application d'onboarding reutilise les donnees canoniques et ne maintient aucun profil commercant ou prestation parallele ;
- la publication, la qualification BUM, l'activation financiere et l'envoi d'une invitation sont des actions explicites, habilitees et auditees.

## Organisation en cinq scopes

Le **scope BackOffice** designe ici tout ce qui doit etre implemente dans le
backend actuel, y compris le domaine, la persistence, les API, les traitements
asynchrones et les ecrans d'administration. Les autres scopes decrivent les
parcours a implementer dans chaque application consommatrice de ces API.

### Scope Localeo OnBoard

Ce scope porte l'application mobile interne utilisee pendant les rendez-vous :

- preparer, affecter, ouvrir et reprendre un dossier d'onboarding (`PRD-551`) ;
- afficher une checklist versionnee, conditionnelle et expliquee (`PRD-552`) ;
- completer les informations canoniques du commercant et verifier les doublons
  (`PRD-553`) ;
- photographier ou televerser les contrats et justificatifs signes (`PRD-554`) ;
- creer ou completer les prestations et afficher leurs blocages BUM et de
  publication (`PRD-555`) ;
- verifier commission, facturation, Stripe Connect et reception des demandes
  de facture (`PRD-556`) ;
- envoyer l'invitation et constater l'activation sans manipuler le mot de passe
  du commercant (`PRD-557`) ;
- calculer une matrice de capacites et cloturer le rendez-vous (`PRD-558`) ;
- superviser le portefeuille de dossiers et les actions de suivi (`PRD-559`).

Les arbitrages `BUM-ARB-42` a `BUM-ARB-48` retiennent le nom
`Localeo OnBoard`, un MVP exclusivement en ligne, l'usage du profil
`Localeo Admin` existant et un test de connexion realise par le commercant sur
son propre telephone. La liste documentaire reste configurable et sa
proposition minimale doit etre adoptee par Localeo apres les controles internes
applicables. Juridica peut apporter un conseil non engageant.

### Scope BackOffice / backend actuel

Ce scope porte le socle transverse et la responsabilite fiscale de Localeo :

- politique BUM, questionnaire, screening, qualification, historique et
  migration initiale des coffrets (`PRD-448` a `PRD-454`) ;
- predicat central de vendabilite applique a tous les canaux (`PRD-454`) ;
- snapshots et generation des justificatifs d'acquisition (`PRD-456` a
  `PRD-458`) ;
- cycle consommation, calcul des montants figes, mouvements et campagnes de
  reversement (`PRD-459`) ;
- aggregate de demande de facture au commercant, anti-doublon, workflow,
  notifications et API (`PRD-460` a `PRD-463`) ;
- pilotage, requalification, securite et audit (`PRD-464` a `PRD-466`) ;
- donnees publiques, mandat et file de depot manuel Chorus Pro (`PRD-467` a
  `PRD-469`) ;
- aggregate `FactureLocaleo`, sequence fiscale, avoirs et rendu documentaire
  idempotent (`PRD-470`, `PRD-473`) ;
- emission d'une facture de commission par commercant a la cloture de chaque
  campagne de reversement (`PRD-471`) ;
- emission de la facture d'abonnement Animation apres confirmation du paiement
  (`PRD-472`).
- registre, calcul, reservations et rapprochement du credit d'achat B2B
  (`PRD-474` a `PRD-476`).

### Scope Commercant

Ce scope porte les fonctions visibles dans l'application Commercant :

- renseigner son profil fiscal et les donnees factuelles de ses prestations,
  reprises lorsque necessaire dans la convention de partenariat signee
  (`PRD-450`, `PRD-469`) ;
- recevoir une demande de correction portant sur ces donnees factuelles, sans
  voir ni valider le diagnostic fiscal interne (`PRD-451`, `PRD-452`) ;
- recevoir et traiter les demandes de facture de prestation : accuse de
  reception, traitement, depot d'une facture externe ou emission assistee sous
  le controle du commercant (`PRD-462`, `PRD-560`) ;
- recevoir les notifications de nouvelle demande, de rejet Chorus Pro ou de
  correction attendue (`PRD-462`, `PRD-469`) ;
- consulter et telecharger la facture de commission Localeo associee a chaque
  campagne de reversement, son detail et l'avoir eventuel (`PRD-471`,
  `PRD-473`) ;
- rapprocher visuellement brut des prestations, commission TTC, ventilation
  HT/TVA et net reverse.
- aucun credit d'achat B2B n'est porte par le commercant ni visible dans son
  application.

Le commercant reste l'emetteur de la facture de prestation adressee au client.
Localeo est l'emetteur de la facture de commission adressee au commercant.

### Scope Marketplace

Ce scope couvre la Marketplace B2C ainsi que les vues d'achat professionnel qui
reposent sur son parcours coffret :

- masquer ou rendre non achetable tout coffret non valide BUM (`PRD-454`) ;
- distinguer la promesse garantie des exemples indicatifs et afficher les
  mentions validees avant achat (`PRD-455`) ;
- remplacer la facture commercant generee a l'achat par le justificatif
  d'acquisition BUM (`PRD-456`, `PRD-457`) ;
- collecter ou reutiliser le profil de facturation du particulier ou de
  l'acheteur Pro (`PRD-458`) ;
- depuis le detail du coffret, permettre une demande de facture uniquement
  apres prestation validee et afficher son statut puis le document fourni par
  le commercant (`PRD-460`, `PRD-461`, `PRD-463`) ;
- proposer une vue multi-coffrets pour l'acheteur Pro, sans exposer les donnees
  d'un autre acheteur (`PRD-463`) ;
- recevoir les notifications email et, si disponible, WebPush lors de la mise
  a disposition de la facture (`PRD-462`).
- pour l'acheteur Pro, consulter le credit de son organisation et l'appliquer a
  une nouvelle commande (`PRD-476`, `PRD-477`).

### Scope Animation

Ce scope couvre Localeo Animation pour le partenaire organisateur :

- appliquer le meme blocage de commercialisation BUM que la Marketplace
  (`PRD-454`) ;
- produire et exposer le justificatif d'acquisition de la commande Animation
  (`PRD-457`) ;
- collecter le profil de facturation, y compris les references Chorus Pro d'une
  entite publique (`PRD-458`, `PRD-467`) ;
- permettre la demande de facture de prestation apres execution, suivre son
  traitement et telecharger la facture du commercant (`PRD-460` a `PRD-463`) ;
- afficher la facture de souscription Localeo Animation emise apres paiement,
  ainsi que ses avoirs eventuels (`PRD-472`, `PRD-473`) ;
- notifier le contact de facturation et afficher le statut du depot Chorus Pro
  lorsque le partenaire est une entite publique (`PRD-468`, `PRD-472`).
- consulter le credit du partenaire dans son perimetre autorise et l'appliquer
  a une commande de lots (`PRD-476`, `PRD-477`).

## Travaux de finalisation non bloquants

Tous les arbitrages structurants sont rendus. L'implementation du socle peut
commencer. Quatre travaux restent a finaliser avant l'activation des fonctions
concernees :

- wording definitif du justificatif d'acquisition (`BUM-ARB-08`) ;
- liste conditionnelle des references Chorus Pro par destinataire public
  (`BUM-ARB-14`) ;
- liste minimale des pieces et preuves d'onboarding par type de commercant
  (`BUM-ARB-45`) ;
- cadre de numerotation, responsabilite d'emission, mandat eventuel et mentions
  de l'assistant de facturation commercant (`BUM-ARB-49`).

Ces valeurs sont externalisees et versionnees afin de ne pas bloquer le schema,
les cas d'usage et les contrats API.

## Details des User Stories

### Lot 0 - Decision interne Localeo et gouvernance

#### `PRD-448` Valider la politique BUM et ses formulations

- Priorite : `P0`
- Statut : `Implemente - decision interne Localeo requise avant activation`
- Faire adopter par Localeo les criteres, donnees obligatoires, clauses de la convention partenaire, mentions Marketplace et libelles documentaires. Un avis Juridica peut etre sollicite a titre de conseil non engageant.
- Versionner la politique sous une reference telle que `BUM_POLICY_2026_01`.
- Aucun wording provisoire ne doit etre presente comme un avis juridique definitif.

#### `PRD-449` Versionner et configurer les regles de screening

- Priorite : `P0`
- Statut : `Implemente backend`
- Chaque evaluation conserve la version des regles et de la politique juridique.
- Les regles evoluent sans reecriture silencieuse de l'historique.

### Lot 1 - Referencement et qualification

#### `PRD-450` Completer le profil fiscal et les donnees factuelles partenaire

- Priorite : `P0`
- Statut : `Implemente`
- Collecter les donnees validees juridiquement et conserver version, date, acteur et preuve de la convention partenaire ; aucune attestation BUM autonome n'est portee par le commercant.
- Le profil canonique porte l'identite legale, le regime fiscal, les adresses
  et le representant ; la convention signee versionnee est conservee dans le
  stockage documentaire securise et conditionne la checklist OnBoard.

#### `PRD-451` Collecter le questionnaire d'eligibilite d'une prestation

- Priorite : `P0`
- Statut : `Implemente backend - diagnostic interne admin uniquement`
- Capturer le caractere defini ou variable du contenu, les operations alternatives, les traitements TVA possibles et `contentIsIndicative`.
- La reponse `NE SAIT PAS` impose une revue.

#### `PRD-452` Executer le screening d'eligibilite

- Priorite : `P0`
- Statut : `Implemente backend`
- Produire `AUTO_ELIGIBLE`, `REVIEW_REQUIRED` ou un autre statut configure, avec motif explicite.
- Ne jamais presenter le resultat automatique comme une qualification juridique definitive.

#### `PRD-453` Qualifier et historiser un coffret

- Priorite : `P0`
- Statut : `Implemente backend`
- Conserver au niveau du coffret qualification, statut, motif, date, auteur, versions et snapshot des donnees sources.
- Permettre une revue BackOffice et une qualification globale des coffrets Multi.
- Initialiser par migration les coffrets existants en `MULTI_PURPOSE / VALIDATED`, avec le motif `INITIAL_CATALOG_BOOTSTRAP`, l'acteur technique `SYSTEM_MIGRATION` et la version de politique initiale.
- Toute modification significative posterieure soumet ces coffrets aux memes regles de requalification que les nouveaux coffrets.

#### `PRD-454` Bloquer la publication des offres non conformes

- Priorite : `P0`
- Statut : `Implemente backend - recette multicanal requise avant activation`
- Appliquer le meme garde-fou a la Marketplace, au B2C, au Pro, aux associations, collectivites et a Localeo Animation.
- Une requalification requise retire l'offre de tous les canaux selon une politique a arbitrer.
- Etendre le diagnostic central de vendabilite afin que les routes publiques et `InitialiserPaiement` reutilisent la meme regle.

### Lot 2 - Presentation et documents d'acquisition

#### `PRD-455` Distinguer promesse garantie et contenu indicatif

- Priorite : `P0`
- Statut : `Implemente backend - contrats de restitution exposes, wording externe a valider`
- Les fiches Marketplace separent ce qui est garanti des exemples indicatifs et affichent la mention juridiquement validee avant achat.

#### `PRD-456` Generer le justificatif d'acquisition BUM

- Priorite : `P0`
- Statut : `Implemente backend - wording externe a valider avant activation`
- Produire un document telechargeable pour les achats B2C sans l'intituler automatiquement `Facture`.
- Utiliser `taxDocumentTreatment = MULTI_PURPOSE_VOUCHER` sans calculer la TVA des prestations sous-jacentes.
- Faire evoluer le recu et les snapshots existants plutot que creer une seconde chaine documentaire.
- Ajouter une mention expliquant que le recapitulatif n'est pas la facture des prestations sous-jacentes et que celles-ci sont facturables apres execution ; faire adopter le wording par Localeo, apres avis de conseil si necessaire.
- Decommissionner toute generation de facture commercant et de pack de factures au moment de l'achat.

#### `PRD-457` Etendre le justificatif aux commandes Pro et Animation

- Priorite : `P1`
- Statut : `Implemente backend - restitution multicanal a recetter`
- Inclure les identites, references de commande, animation, lignes, quantites, paiement et informations de facturation adaptees au canal.

#### `PRD-458` Gerer les profils de facturation et types d'acheteur

- Priorite : `P1`
- Statut : `Implemente backend - profils reutilisables et entites publiques`
- Supporter `INDIVIDUAL`, `BUSINESS`, `ASSOCIATION` et `PUBLIC_ENTITY` ainsi qu'un `BillingProfile` reutilisable.
- Conserver un snapshot immuable dans chaque demande de facture.

### Lot 3 - Execution, reversement et demandes de facture

#### `PRD-459` Aligner le cycle financier sur la consommation

- Priorite : `P0`
- Statut : `Implemente backend`
- Le paiement emet le coffret et place les fonds en attente ; la validation de consommation ouvre le droit commerçant et le reversement.
- Les coffrets expires non consommes ne generent ni consommation, ni reversement, ni demande de facture.
- Conserver `ServiceValidationPrestation` et `MouvementReversement`, qui implementent deja l'essentiel de ce flux.
- Remplacer l'ambiguite de `montant_reversement` par des montants distincts : prestation facturable TTC, commission Localeo HT/TVA/TTC et net reverse.
- Reutiliser le montant de commission configurable existant, afficher son taux effectif et son ecart a la cible de 15 % TTC, sans creer une seconde configuration concurrente.
- Snapshotter la commission TTC configuree et sa ventilation HT/TVA selon la configuration TVA Localeo applicable.
- Snapshotter ces montants lors de l'execution afin qu'une modification tarifaire ulterieure ne change pas la facture ni le reversement.

#### `PRD-460` Identifier les consommations facturables

- Priorite : `P1`
- Statut : `Implemente backend`
- N'exposer que les consommations validees sans demande active.
- Garantir le lien traçable avec commande, coffret, prestation, commercant, reversement et commission.
- Utiliser `ValidationPrestation` comme source de verite plutot que creer une entite `Redemption` concurrente.
- Autoriser l'initialisation par le particulier, le client professionnel ou le partenaire Animation habilite, en tenant compte de la relation entre acheteur et beneficiaire.

#### `PRD-461` Creer des demandes de facture unitaires ou groupees

- Priorite : `P1`
- Statut : `Implemente backend`
- Autoriser les sources `MARKETPLACE`, `PRO_ORDER` et `ANIMATION` en V1.
- Conserver une ligne et une contrainte anti-doublon par `ValidationPrestation` ; pour un achat Pro, autoriser une demande agregee par commercant contenant plusieurs lignes eligibles.
- Faire evoluer `DemandeFacturationAchatOrm` en aggregate de demande de facture au commercant, avec rattachement aux validations, workflow, snapshot et anti-doublon.
- Supprimer la creation d'une demande de facturation depuis le formulaire de support et le booleen historique `traitee`.
- Effectuer une migration one-shot du schema et du code, sans maintenir deux concepts en parallele puisqu'aucune demande de production n'est a reprendre.
- Neutraliser la generation de `FACTURE_COMMERCANT` au niveau de l'achat prevue par l'Epic 14.
- Transmettre au commercant les references de demande, commande, coffret, prestation validee, date d'execution, montant brut TTC facturable, commission separee, net reverse et snapshot complet des informations de facturation.
- Ne jamais transmettre le secret QR ni calculer le HT, la TVA ou le taux a la place du commercant.

#### `PRD-462` Notifier et permettre le traitement par le commercant

- Priorite : `P1`
- Statut : `Implemente backend`
- Notifier le commercant par email et dans son application, avec WebPush si ce canal est disponible.
- Exposer la demande dans Finance et gerer `REQUESTED -> ACKNOWLEDGED -> PROCESSING -> PROVIDED`, ainsi que `CANCELLED`, avec audit.
- Le commercant reste responsable de la facture et doit mettre a disposition le document, son numero et sa date.
- La mise a disposition declenche une notification au demandeur : email obligatoire et WebPush si Localeo Live est configure et autorise.

#### `PRD-560` Assister le commercant dans l'emission de sa facture

- Priorite : `P1 / Finance / Localeo`
- Statut : `Implemente backend - decision interne Localeo et controle comptable requis avant activation`
- Conserver deux modes de traitement : televerser une facture emise dans un
  outil externe ou utiliser l'assistant de facturation Localeo.
- Preparer un brouillon depuis les snapshots de la demande sans attribuer de
  numero definitif, sans envoyer le document et sans determiner le traitement
  de TVA a la place du commercant.
- Faire verifier et confirmer par le commercant son identite, le destinataire,
  les lignes, les dates, la TVA, les mentions et le reglement par coffret.
- Exiger une action explicite attestant que le commercant emet la facture sous
  sa responsabilite ; attribuer alors un numero dans une serie propre au
  commercant et generer le document immuable.
- Permettre une correction uniquement par avoir ou document correctif
  reference. Conserver acteur, date, version, donnees emises et empreinte.
- Preparer un modele de donnees structure afin de pouvoir raccorder
  ulterieurement une plateforme agreee de facturation electronique.
- Soumettre le cadre de numerotation, la qualification de Localeo comme simple
  outil ou tiers mandate et les mentions finales a validation
  interne Localeo apres controle comptable avant activation. Un avis Juridica
  non engageant peut etre sollicite si necessaire.
- Implemente le 1er septembre 2026 : brouillon structure pre-rempli sans
  numero, modification sous verrou optimiste, confirmation typee de la
  responsabilite du commercant, serie annuelle propre au commercant protegee
  contre la concurrence, snapshot d'emission immuable et PDF rattache a la
  demande. Une correction cree un avoir ou une facture corrective qui
  reference l'original, avec cle d'idempotence, sans modifier la facture
  emise. Les routes sont protegees par
  `LOCALEO_FEATURE_MERCHANT_INVOICE_ASSISTANT_ENABLED`, maintenu desactive
  tant que `BUM-ARB-49` n'est pas valide.

#### `PRD-463` Suivre les demandes cote Pro et Animation

- Priorite : `P1`
- Statut : `Implemente backend`
- Afficher les prestations executees, leur eligibilite, le statut et les factures disponibles sans exposer de donnees d'un autre acheteur.
- Pour un particulier, exposer la facture depuis la vue detaillee du coffret.
- Pour un achat Pro, exposer une vue detaillee de commande et une vue multi-coffrets.
- Pour une demande partenaire, exposer le suivi et le document dans Localeo Animation.

### Lot 4 - BackOffice, alertes et qualite

#### `PRD-464` Piloter la conformite fiscale dans le BackOffice

- Priorite : `P1`
- Statut : `Implemente BackOffice et API`
- Fournir files d'attente, decisions, motifs, versions, requalifications et liens d'audit.

#### `PRD-465` Detecter les modifications imposant une requalification

- Priorite : `P1`
- Statut : `Implemente backend`
- Surveiller composition, categorie, contenu, conditions et donnees ayant fonde la decision.
- Toute transition et toute consequence de depublication sont auditees.

#### `PRD-466` Couvrir securite, activation et non-regression

- Priorite : `P0`
- Statut : `Implemente backend - go/no-go externe requis`
- Tester tous les canaux et verifier autorisations, idempotence, concurrence et non-divulgation.
- Verifier que la migration qualifie tous les coffrets existants de maniere idempotente et auditable.
- La premiere commercialisation est impossible tant que les garde-fous BUM ne sont pas actifs et verifies.

### Lot 5 - Integration Chorus Pro

#### `PRD-467` Collecter et valider les references Chorus Pro

- Priorite : `P1`
- Statut : `Implemente backend - recette annuaire Chorus requise`
- Etendre le profil de facturation public avec SIRET destinataire, code service, numero d'engagement, references de commande, marche et contrat.
- Consulter ou synchroniser l'annuaire Chorus Pro pour connaitre les champs obligatoires de chaque destinataire.
- Figer ces informations dans le snapshot de la facture et du depot.
- Implemente le 1er septembre 2026 : le profil `PUBLIC_ENTITY` conserve SIRET,
  structure Chorus, activite du destinataire, codes services observes et
  exigences conditionnelles de service et d'engagement. La synchronisation
  admin est versionnee, datee par le serveur et auditee ; la creation de la
  demande fige ensuite l'integralite du profil dans son snapshot. Le
  raccordement reel a l'annuaire reste soumis a la recette Chorus Pro.

#### `PRD-468` Piloter le depot manuel des factures dans Chorus Pro

- Priorite : `P1`
- Statut : `Implemente backend - recette Chorus requise`
- Fournir une file BackOffice `A_DEPOSER` regroupant les factures Localeo d'abonnement et les factures de prestation emises par les commercants.
- Permettre a un operateur Localeo de telecharger le document et les references, puis d'enregistrer le depot effectue sur le portail Chorus Pro.
- Suivre operateur, date, identifiant Chorus, statuts, suspensions, rejets, acceptation et paiement sans confondre demande, document et depot.
- Une integration API PISTE ou un operateur raccorde est reporte en V2 et pourra reutiliser le meme modele de suivi.
- Implemente le 1er septembre 2026 : `depots_chorus_pro` separe la demande,
  le document et le depot, fige le destinataire public, impose une cle
  d'idempotence et expose la file admin, le telechargement et les transitions
  auditees jusqu'au paiement. Le flux des factures commercants alimente cette
  file. Les factures Localeo d'abonnement sont raccordees par `PRD-470` a
  `PRD-472` ; la recette externe Chorus demeure une porte d'activation.

#### `PRD-469` Mandater Localeo pour le depot des factures commercants

- Priorite : `P0 / Localeo / Finance`
- Statut : `Implemente backend - decision interne Localeo et recette Chorus requises`
- Faire accepter au commercant un mandat versionne autorisant Localeo a deposer ses factures destinees aux entites publiques.
- Conserver version, acceptation, date, acteur, perimetre, revocation et preuve.
- Le commercant reste emetteur et responsable des donnees fiscales ; Localeo controle la completude technique et assure le depot.
- Notifier commercant et demandeur lorsqu'un rejet ou une correction exige leur intervention.
- Implemente le 1er septembre 2026 : le mandat actif est unique par commercant,
  versionne, rattache a une preuve PDF publiee, borne aux factures publiques et
  revocable avec motif. Toute facture publique commercant exige ce mandat avant
  preparation du depot. Le snapshot rappelle que le commercant reste emetteur ;
  les rejets notifient le commercant et le demandeur et une correction cree un
  nouveau depot idempotent sans modifier le document d'origine.

### Lot 6 - Factures emises par Localeo

#### `PRD-470` Creer l'aggregate commun de facture Localeo

- Priorite : `P0`
- Statut : `Implemente backend - validation comptable requise`
- Gerer les types `COMMISSION_COMMERCANT` et `ABONNEMENT_ANIMATION` dans un modele commun.
- Figer emetteur, destinataire, lignes, HT, TVA, TTC, devise, references metier et version du gabarit dans un snapshot immuable.
- Reutiliser `SequenceFacturationOrm` pour attribuer un numero fiscal une seule fois et garantir en base l'unicite de la cle d'idempotence.
- Une facture emise n'est jamais modifiee : toute correction passe par un avoir reference.
- Implemente le 1er septembre 2026 : `factures_localeo` et
  `lignes_facture_localeo` figent le snapshot fiscal, les sources, les lignes,
  les totaux et la version de gabarit. Les series annuelles factures/avoirs
  utilisent `SequenceFacturationOrm`, un verrou transactionnel et un index
  partiel pour le scope Localeo sans identifiant.

#### `PRD-471` Facturer la commission au commercant

- Priorite : `P1 / Finance`
- Statut : `Implemente backend - recette Finance requise`
- Emettre une facture consolidee par commercant et campagne de reversement.
- Inclure les validations et mouvements rapproches, le brut TTC des prestations, la commission configurable TTC, sa ventilation HT/TVA et le net reverse.
- Utiliser une cle stable `COMMISSION:{commercant_id}:{campagne_reversement_id}` afin qu'un rejeu ne cree ni doublon ni nouveau numero.
- Mettre le document a disposition du commercant et notifier son emission.
- Lorsque la facturation Localeo est activee, la creation d'une campagne Stripe
  emet atomiquement la facture avant le premier ordre de transfer. Un snapshot
  de commission incomplet bloque la campagne ; le detail conserve validation,
  mouvement, brut TTC, commission HT/TVA/TTC et net reverse.

#### `PRD-472` Facturer la souscription au partenaire Animation

- Priorite : `P0`
- Statut : `Implemente backend - recette Finance requise`
- Emettre la facture apres confirmation du paiement depuis le snapshot de `SouscriptionPlateforme` de l'Epic 47.
- Conserver les references Stripe comme preuve de reglement sans deleguer a Stripe la source de numerotation fiscale Localeo.
- Rendre le document disponible dans Localeo Animation et l'envoyer au contact de facturation.
- Pour une entite publique, transmettre la facture et ses references a la file de depot manuel Chorus Pro.
- Le backend conserve les snapshots de facturation, de prix et de paiement sur
  la souscription, exige `PAID` et une reference Stripe, emet de maniere
  idempotente, notifie le contact, cloisonne l'acces partenaire et rend le PDF.
  Un destinataire public alimente `depots_chorus_pro`. Le webhook de paiement
  de l'Epic 47 est raccorde et protege par la cle fiscale idempotente.

#### `PRD-473` Generer les PDF de maniere idempotente

- Priorite : `P1`
- Statut : `Implemente backend`
- Permettre une generation immediate ou a la premiere consultation, exclusivement depuis le snapshot immuable.
- Conserver version du gabarit, cle de stockage, empreinte, date de generation et type MIME.
- Un nouvel appel restitue le document existant ou le regenere a l'identique sans recalcul, renumerotation ni nouvelle emission.
- Cloisonner les acces entre commercants, partenaires et operateurs BackOffice.
- Le rendu utilise exclusivement `invoice_snapshot` et `template_version`,
  conserve `document_id`, SHA-256 et date de rendu, puis restitue le meme
  document aux appels suivants. Les routes verifient le destinataire
  commercant ou partenaire ; le BackOffice conserve son acces.

### Lot 7 - Credit d'achat B2B sur coffrets expires

#### `PRD-474` Calculer le credit des prestations non utilisees

- Priorite : `P0 / Finance / Localeo`
- Statut : `Implemente backend - controle Finance et decision interne Localeo requis`
- A l'expiration d'un coffret B2B, calculer la part effectivement payee allouee aux prestations non utilisees.
- Exclure les prestations validees, remboursements et frais Localeo non creditables.
- Garantir qu'une allocation ne peut etre creditee qu'une fois.
- Implemente le 2 septembre 2026 : le batch d'expiration calcule chaque
  allocation depuis le montant effectivement finance, retranche les frais
  Localeo non creditables, exclut les prestations consommees et protege le
  rejeu par une contrainte d'unicite et des cles d'idempotence.

#### `PRD-475` Gerer le registre et les reservations de credit

- Priorite : `P0`
- Statut : `Implemente backend`
- Utiliser un registre immuable de mouvements et calculer le solde comme une projection.
- Reserver le credit pendant le checkout, le capturer au paiement et le liberer en cas d'echec ou d'expiration.
- Interdire les soldes modifies directement et auditer toutes les regularisations.
- Rapprocher periodiquement credits attribues, consommes, expires et annules avec le passif restant, ainsi que les reservations avec les commandes et paiements Stripe.
- Implemente le 2 septembre 2026 : le registre append-only, les lots a echeance,
  les imputations FEFO, les reservations verrouillees 30 minutes et le batch de
  rapprochement, les regularisations BackOffice auditees et l'acceptation
  versionnee des conditions sont livres par `v209`, `v211` et `v214`.

#### `PRD-476` Utiliser le credit dans les commandes Animation et Pro

- Priorite : `P1`
- Statut : `Implemente backend - recette paiement requise`
- Accepter un paiement mixte credit et Stripe, ainsi qu'une commande entierement payee par credit.
- Permettre la saisie d'un code avant Stripe ; appliquer le minimum entre le solde et le total, conserver le reliquat ou epuiser le code apres paiement confirme.
- En Marketplace Pro sans compte, exiger en plus du code un OTP envoye a l'email de facturation snapshotte et utiliser une session courte ; le code seul n'autorise aucune consommation.
- Rattacher achats et credits a une identite technique `organisation_pro_id` determinee initialement par SIRET + email verifie ; maintenir un code actif par organisation et plusieurs lots de credit echeances.
- En cas d'annulation, limiter le remboursement Stripe a la part Stripe et restituer la part credit avec son echeance d'origine.
- A l'expiration d'un coffret paye par credit, ne restituer la part credit que si son lot source est encore valide, sans jamais prolonger son echeance ; creer un nouveau lot de 12 mois uniquement pour la part payee en argent.
- Conserver la repartition dans le snapshot et sur le justificatif d'acquisition.
- Ne jamais exposer le credit au parcours B2C.
- Implemente le 2 septembre 2026 : Animation et Marketplace Pro supportent le
  paiement mixte et 100 % credit. Marketplace exige une session code + OTP ;
  les webhooks capturent ou liberent la reservation et les remboursements
  restaurent uniquement les composantes encore valides a leur echeance
  d'origine. Le split est snapshotte sur l'acquisition.

#### `PRD-477` Exposer le credit dans Animation et la Marketplace Pro

- Priorite : `P1`
- Statut : `Implemente backend`
- Afficher solde, prochaine echeance, historique et origine des mouvements.
- Afficher le credit applicable dans le recapitulatif de commande.
- Appliquer les habilitations du partenaire ou de l'organisation professionnelle.
- Dans Animation, reutiliser la session gestionnaire ; dans la Marketplace Pro, donner acces par code + OTP a une session de consultation restreinte.
- Emettre le code au premier credit sans OTP actif dans le meme message et notifier creation, echeance proche, consommation et remplacement via l'outbox.
- Implemente le 2 septembre 2026 : les API cloisonnees exposent solde, lots,
  prochaine echeance et historique. Le code est hache, l'OTP est limite et
  expire, et l'outbox couvre creation, consommation, echeance et remplacement.
  Animation cloisonne le compte par partenaire + commune. L'achat Pro est
  rattache a `organisation_pro_id` par `v213` et l'acceptation des conditions
  est tracee par `v214`.

#### `PRD-478` Regrouper les demandes de facture d'un achat Pro

- Priorite : `P1`
- Statut : `Implemente backend`
- Depuis le detail d'un achat Pro, proposer une demande groupee par commercant pour toutes les prestations executees et facturables de cet achat.
- Creer une demande et une facture distinctes par commercant, meme lorsque l'action utilisateur est unique.
- Snapshotter les lignes selectionnees, beneficiaires, montants, dates d'execution et donnees de facturation, et exclure celles deja rattachees a une demande active ou une facture.
- Permettre une demande complementaire lorsque d'autres prestations du meme achat sont executees plus tard.
- Limiter chaque demande a un commercant, un acheteur, une devise et un snapshot de facturation ; rendre toute facture fournie immuable et corriger par document correctif ou avoir reference.
- Accepter uniquement un PDF de 10 Mo maximum, controle par type reel, empreinte SHA-256 et analyse antivirus avant publication.
- Implemente le 2 septembre 2026 : `v210` cree une demande distincte par
  commercant avec lignes et snapshots immuables. L'action sans selection prend
  toutes les prestations eligibles. `v212` rattache les factures correctives
  et avoirs a l'original avec une cle d'idempotence. Les vues Pro, Animation et
  commercant sont cloisonnees ; les demandes complementaires excluent les
  validations deja actives et le depot reutilise la chaine documentaire
  securisee (type reel, SHA-256, antivirus et plafond 10 Mo).

### Lot 8 - Onboarding commercant mobile

#### `PRD-551` Creer et reprendre un dossier d'onboarding terrain

- Priorite : `P0`
- Statut : `Implemente`
- Permettre a un commercial habilite de preparer un rendez-vous, rechercher un
  commercant existant ou creer son brouillon sans doublon, affecter le dossier
  et reprendre la saisie sur mobile.
- Conserver statut, responsable, rendez-vous, prochaine action et historique.
- Implemente le 1er septembre 2026 : dossier persistant unique par commercant,
  recherche et reprise dans le referentiel, affectation, rendez-vous, prochaine
  action, version optimiste et audit. OnBoard permet aussi de creer, dans une
  transaction unique, le brouillon commercant canonique et son dossier ; le
  nom dans la commune et l'email sont controles contre les doublons. Cette
  creation n'envoie aucune invitation implicite.

#### `PRD-552` Piloter une checklist versionnee et conditionnelle

- Priorite : `P0`
- Statut : `Implemente`
- Afficher les controles applicables selon le type de commercant, ses
  prestations et les fonctions visees.
- Distinguer obligatoire, recommande et non applicable, expliquer chaque
  blocage et conserver la version de checklist utilisee.
- Ne jamais transformer une case client en preuve ou validation serveur.
- Implemente le 1er septembre 2026 : checklist `ONBOARD_2026_02` calculee cote
  serveur depuis les donnees canoniques, instantanee avec la version de la
  politique BUM active et restituee par categorie avec le responsable de chaque
  blocage. Les fonctions visees pilotent l'applicabilite ; chaque item distingue
  `REQUIRED`, `RECOMMENDED` et `NOT_APPLICABLE`, explique la regle appliquee et
  identifie explicitement le serveur comme source de preuve. Les exigences
  documentaires propres a un type de commercant sont configurees dans la
  politique BUM, sans figer dans le client la liste adoptee par Localeo.

#### `PRD-553` Completer le referentiel commercant pendant le rendez-vous

- Priorite : `P0`
- Statut : `Implemente`
- Saisir ou corriger les identites legale et commerciale, adresses, contacts,
  informations publiques, fiscales et de facturation dans les agregats
  canoniques existants.
- Controler format, unicite, habilitation territoriale et modifications
  concurrentes avant enregistrement.
- Implemente le 1er septembre 2026 : correction dans OnBoard du nom
  commercial, de la commune, du type, de la description et du contact avec
  validation email/telephone, unicite et version optimiste. L'identite legale
  et fiscale est portee par le profil de facturation canonique versionne :
  raison sociale, forme juridique, SIREN/SIRET coherents, regime de TVA,
  numero de TVA conditionnel, representant legal, siege et adresse
  d'exploitation. Un index actif interdit de partager un SIRET entre deux
  commercants et le perimetre territorial de session est controle avant une
  creation ou un changement de commune.

#### `PRD-554` Capturer et classer les documents signes

- Priorite : `P0 / Securite / Localeo`
- Statut : `Implemente`
- Photographier plusieurs pages ou televerser un PDF, verifier la lisibilite,
  classer la piece et renseigner version contractuelle, date et signataires.
- Reutiliser le stockage documentaire securise avec controle du type reel,
  taille bornee, empreinte, analyse antivirus, autorisation et audit.
- Ne conserver aucune copie durable sur le telephone apres envoi confirme.
- Implemente le 1er septembre 2026 : televersement d'un PDF ou de 1 a 20 pages
  JPEG/PNG assemblees en PDF, taille totale bornee, controle du type binaire,
  rejet des PDF actifs, empreinte SHA-256 et stockage documentaire existant.
  La version contractuelle, la date, les signataires, le nombre de pages, le
  diagnostic de lisibilite et sa confirmation sont historises. ClamAV est
  obligatoire hors developpement ; une piece non marquee `CLEAN` reste en
  brouillon et ne satisfait pas la checklist contractuelle.

#### `PRD-555` Finaliser les prestations et leur conformite BUM

- Priorite : `P0`
- Statut : `Implemente`
- Creer ou completer les prestations, leurs informations publiques, medias,
  valeurs et questionnaires BUM depuis les memes cas d'usage que les autres
  surfaces.
- Afficher le screening, le diagnostic de vendabilite et les actions restant a
  effectuer avant rattachement a un coffret ou publication.
- Implemente le 1er septembre 2026 : creation et modification versionnee d'une
  prestation depuis OnBoard, controle canonique de la marge du coffret,
  valeurs TTC et reversement, questionnaire derive de la politique BUM active,
  screening par version et invalidation des qualifications des coffrets
  affectes apres modification, televersement securise des visuels raster dans
  le DAM avec nouvelle version de prestation, et restitution des blocages du
  diagnostic canonique de vendabilite par coffret. OnBoard ne publie et ne
  qualifie rien : le commercial collecte les faits et la decision coffret
  reste reservee a l'administrateur Localeo dans la surface canonique.

#### `PRD-556` Valider la preparation financiere et documentaire

- Priorite : `P0 / Finance`
- Statut : `Implemente`
- Verifier le profil de facturation, l'acceptation de la commission, la
  preparation Stripe Connect, la reception des factures de commission et les
  coordonnees de traitement des demandes de facture.
- Integrer mandat et donnees Chorus Pro lorsque le contexte les rend
  applicables.
- Implemente le 1er septembre 2026 : saisie versionnee du profil de facturation
  canonique, preuve auditee de l'acceptation des conditions de commission,
  contacts distincts pour factures de commission et demandes de facture,
  confirmation du circuit de reception, et restitution en lecture seule de
  l'etat Stripe Connect. Le mandat Chorus est explicitement non applicable
  tant que le depot au nom du commercant reste desactive par la doctrine active.

#### `PRD-557` Ouvrir et tester l'acces a l'espace Commercant

- Priorite : `P0 / Securite`
- Statut : `Implemente`
- Envoyer ou regenerer l'invitation sans exposer son token au commercial.
- Constater l'activation et permettre au commercant de tester la connexion sur
  son propre appareil.
- Interdire au membre Localeo de choisir, connaitre ou conserver le mot de
  passe du commercant.
- Implemente le 1er septembre 2026 : envoi et regeneration de l'invitation
  depuis OnBoard via le cas d'usage canonique, token uniquement hache en base,
  lien transmis par email sans restitution a l'operateur, et affichage de
  l'etat d'activation/verrouillage. Le test sur l'appareil du commercant est
  confirme explicitement et audite sans collecter de secret ; cette preuve
  conditionne la capacite d'acces au portail.

#### `PRD-558` Calculer les capacites et cloturer le rendez-vous

- Priorite : `P0`
- Statut : `Implemente`
- Calculer cote serveur les capacites `PORTAIL_VISIBLE`,
  `PRESTATION_PUBLIABLE`, `COFFRET_PUBLIABLE`, `BUM_READY`,
  `COMMISSION_BILLABLE`, `INVOICE_REQUEST_READY`, `PAYOUT_READY` et
  `PORTAL_ACCESS_READY`.
- Restituer les blocages par capacite, leur responsable et leur prochaine
  action ; refuser la validation si un prerequis obligatoire manque.
- Exiger des confirmations explicites pour toute publication ou action externe.
- Implemente le 31 aout 2026 : les huit capacites sont calculees cote serveur,
  la validation est refusee tant que la checklist ou une capacite bloque, et
  seule une validation explicite permet ensuite la cloture. Chaque capacite
  restitue ses prerequis bloquants, leur responsable et la prochaine action.
  L'envoi externe d'une invitation exige une confirmation typee dans le
  contrat API ; aucune publication externe n'est declenchee par OnBoard.

#### `PRD-559` Superviser le portefeuille d'onboarding commercial

- Priorite : `P1`
- Statut : `Implemente`
- Rechercher et filtrer les dossiers par commercial, statut, commune, blocage,
  prochaine action et echeance.
- Produire un recapitulatif partageable des elements valides, des pieces
  attendues et des actions assignees, sans exposer les documents sensibles.
- Mesurer duree, taux de completion au rendez-vous et principaux blocages.
- Implemente le 31 aout 2026 : PWA interne `Localeo OnBoard`, file de dossiers,
  recherche par commercant, commune ou reference, filtre par statut, progression
  et vue detail responsive. Les filtres serveur couvrent commercial, commune,
  blocage et echeance ; un recapitulatif texte partageable restitue uniquement
  les validations et actions sans metadata documentaire sensible. Les
  indicateurs consolident duree, completion courante, principaux blocages et
  taux de completion snapshotte au premier diagnostic apres le rendez-vous.

## Ordonnancement recommande

1. `PRD-448` et decision interne Localeo, eventuellement eclairee par un avis Juridica non engageant ;
2. modele et versionnement (`PRD-449` a `PRD-453`) ;
3. garde-fou de publication et presentation (`PRD-454`, `PRD-455`) ;
4. justificatifs et cycle financier (`PRD-456`, `PRD-457`, `PRD-459`) ;
5. facturation post-execution et assistant commercant (`PRD-458`, `PRD-460` a
   `PRD-463`, `PRD-560`) ;
6. pilotage, alertes et durcissement (`PRD-464` a `PRD-466`) ;
7. mandat, donnees publiques et depot manuel Chorus Pro (`PRD-467` a `PRD-469`).
8. factures Localeo, commission et abonnement Animation (`PRD-470` a `PRD-473`).
9. credit d'achat B2B, paiement mixte et regroupement Pro (`PRD-474` a `PRD-478`), apres validation des arbitrages dedies.
10. application mobile `Localeo OnBoard` et checklist terrain (`PRD-551` a
    `PRD-559`) selon les arbitrages rendus ; conserver la checklist desactivee
    en production jusqu'a validation de sa liste documentaire.

## Definition de termine

- aucun coffret non valide BUM n'est publiable ;
- tous les coffrets anterieurs a l'Epic sont initialises `MULTI_PURPOSE / VALIDATED` avec une trace de migration ;
- toute qualification est versionnee, motivee et auditable ;
- aucune commercialisation ne peut commencer avant l'activation des garde-fous BUM ;
- la Marketplace distingue garantie et exemple indicatif ;
- chaque canal produit le justificatif d'acquisition attendu ;
- paiement, consommation, reversement et facturation restent des evenements distincts ;
- aucune facture ne peut etre demandee avant une consommation validee ;
- les lignes unitaires sont creees sans doublon et peuvent etre regroupees par achat Pro et commercant ; les demandes sont notifiees et suivies ;
- le commercant peut televerser une facture externe ou utiliser l'assistant ;
  aucun brouillon n'est numerote ou transmis avant sa confirmation explicite ;
- deux emissions concurrentes ou rejouees produisent une seule facture et un
  seul numero dans la serie propre au commercant ;
- une facture assistee emise reste immuable, y compris en cas d'echec puis de
  reprise du rendu PDF ;
- Localeo ne calcule pas la TVA de la prestation commerçant en V1 ;
- le montant facture par le commercant correspond au brut TTC de la prestation executee, avant commission Localeo ;
- la commission configurable est TTC, vise 15 % du brut TTC et inclut la TVA dont Localeo doit s'acquitter ;
- la facture peut constater un reglement integral par coffret avec un net a payer nul, apres decision interne Localeo sur le wording et le cadre Chorus Pro ;
- les formulations et hypotheses fiscales sont versionnees et leur activation
  reste bloquee tant que l'auteur et la date de la decision interne Localeo ne
  sont pas traces ;
- les factures destinees aux entites publiques sont deposees et suivies par Localeo dans Chorus Pro ;
- Localeo depose les factures commercants uniquement sous mandat valide et conserve la preuve du depot.
- les factures de commission et d'abonnement Animation sont numerotees une seule fois a partir d'un snapshot fiscal immuable ;
- leur PDF peut etre genere a la demande de maniere idempotente et toute correction utilise un avoir.
- les coffrets B2B expires generent au plus une fois le credit eligible de leurs prestations non utilisees ;
- toute utilisation de credit est reservee puis capturee ou liberee, avec un historique auditable dans Animation ou la Marketplace Pro.
- un commercial peut conduire un onboarding depuis un mobile sans acces direct
  a SQLAdmin et sans dupliquer les donnees canoniques ;
- les contrats et justificatifs signes sont classes, versionnes, controles et
  auditables ;
- la cloture du dossier repose sur des diagnostics serveur par capacite et
  identifie explicitement toute action restante ;
- le commercant dispose d'un acces fonctionnel a son espace ou d'une action de
  suivi assignee, sans que l'equipe Localeo ne manipule son mot de passe.

## Suivi du rapport Marketplace du 6 septembre 2026

MARKET-002, MARKET-003, MARKET-009 et MARKET-010 sont implementes et couverts par les tests locaux. Le [guide de livraison et recette](../../exploitation/guide-corrections-marketplace-2026-09-06.md) precise les controles encore requis sur la cible avant activation du credit. Cette mise a jour ne clot pas les autres lots de l'epic.
