# Epic 50 - Analyse de l'existant et impacts

## Objet

Ce document contextualise l'Epic 50 par rapport au backend Localeo implemente au 24 aout 2026. Il distingue les briques reutilisables, les adaptations necessaires et les comportements a remplacer. Le constat porte sur le code actuel et ne vaut pas validation juridique.

## Synthese

Localeo dispose deja du cycle operationnel principal : catalogue versionne, controle central de vendabilite, paiement Stripe, instances de coffret, validation de prestation, reversements Stripe Connect, snapshots, documents d'achat, audit et commandes de lots Animation.

L'Epic 50 doit donc principalement :

1. ajouter la qualification BUM et ses preuves au referentiel ;
2. l'integrer au garde-fou de vendabilite existant ;
3. completer le referencement partenaire et prestation ;
4. adapter le recu existant en justificatif d'acquisition BUM ;
5. remplacer la facture commercant generee a l'achat par une demande liee aux prestations validees ;
6. reutiliser le reversement deja declenche par la validation ;
7. etendre les parcours Pro et Animation existants.

## Cartographie de l'existant

| Domaine | Existant implemente | Impact Epic 50 |
| --- | --- | --- |
| Coffret | `Coffret` porte type commercial, prix, duree, ville, statut et blocage d'usage | Ajouter la qualification fiscale sans modifier `type_coffret` |
| Prestation | `PrestationCoffret` porte contenu, commercant, montant de reversement, statut et version | Collecter les donnees factuelles et leurs snapshots pour un diagnostic interne ; ne porter aucune qualification BUM sur la prestation |
| Versionnement | `PrestationCoffretVersionOrm` historise contenu, montant, auteur, motif et date | Reutiliser cet historique comme source des changements imposant une requalification |
| Vendabilite | `diagnostiquer_blocages_vendabilite_coffret` controle coffret actif, commercants et Stripe Connect | Ajouter ici le blocage fiscal unique |
| Marketplace et achat | Liste, detail, recherche et `InitialiserPaiement` utilisent deja le controle de vendabilite | Proteger toutes les entrees sans dupliquer la regle BUM |
| Achat | `AchatCoffret` gere B2C, Pro, quantite et origine Animation | Conserver cette racine documentaire |
| Commande groupee | `CommandeAchat` fige acheteur, lignes, prix et quantites pour Animation | Reutiliser pour justificatif et suivi consolides |
| Instances | `CoffretInstance` gere attente, activation, utilisation, expiration et annulation | Conserver ce cycle sans requalifier retroactivement les droits acquis |
| Consommation | `ServiceValidationPrestation` cree atomiquement `ValidationPrestation` | Utiliser cette validation comme execution et source de facturabilite |
| Reversement | La validation cree deja un `MouvementReversement` idempotent et compatible Stripe Connect | Consolider les invariants, ne pas reconstruire le flux |
| Documents | Snapshots de facturation, lignes, references, hashes, PDF et ZIP existent | Reutiliser le moteur et adapter sa semantique |
| Recu | Le PDF precise deja qu'il n'est pas une facture fiscale | Le transformer en justificatif d'acquisition BUM |
| Facture commercant | L'Epic 14 genere une facture par commercant et par achat avant consommation | Incompatible avec la cible Epic 50 : neutraliser cette generation |
| Demande existante | `DemandeFacturationAchatOrm` est une demande support par achat avec un booleen `traitee` | Migrer cet objet vers la demande de facture au commercant et supprimer son usage support actuel |
| Animation | Commande de lots, paiement, reservation, recu et consultation documentaire existent | Adapter ces briques et ajouter le suivi post-consommation |
| Audit | `EvenementAuditOrm` trace acteur, action, phase et ressource | Reutiliser, complete par des historiques metier immuables |
| TVA Localeo | Configuration TVA et facture de frais de service Localeo existent | Conserver distinct du traitement fiscal du bon et de la facture commercant |

## 1. Qualification BUM absente

### Constat

- le coffret ne porte que son type commercial et son statut ;
- la prestation ne porte aucun questionnaire fiscal ;
- aucun historique de qualification ou version de politique n'existe ;
- le controle de vendabilite ne connait pas la conformite BUM.

### A traiter

- ajouter au coffret qualification, statut, version de politique et derniere decision ;
- ajouter les donnees d'eligibilite aux versions de prestation ;
- creer un historique fiscal distinct de l'historique editorial ;
- initialiser les coffrets techniques en `MULTI_PURPOSE / VALIDATED` avec `SYSTEM_MIGRATION` et `INITIAL_CATALOG_BOOTSTRAP` ;
- ajouter la non-conformite BUM au diagnostic central de vendabilite.

## 2. Referencement partenaire incomplet

### Constat

`CommercantOrm` contient identite commerciale, contacts, ville, type et donnees Stripe Connect. Le profil public dispose d'un workflow de versionnement et moderation. Depuis le lot OnBoard, les informations juridiques et fiscales structurees sont portees par le profil de facturation canonique versionne ; la preuve de convention partenaire signee reste geree par le stockage documentaire transverse.

### A traiter

- etendre le referentiel sans dupliquer le profil public ;
- separer donnees publiques, contractuelles et fiscales privees ;
- rattacher la convention partenaire a une version de texte et a sa preuve de signature ;
- reutiliser les habilitations existantes avec des droits explicites.

## 3. Questionnaire et requalification

### Constat

Les prestations sont deja versionnees et les modifications commercant passent par moderation. Les auteurs, dates, motifs et anciennes valeurs sont donc disponibles.

### A traiter

- ajouter le questionnaire BUM a la proposition de version ;
- detecter les champs sensibles pendant la moderation ;
- passer les coffrets concernes en `REQUALIFICATION_REQUIRED` ;
- bloquer les nouvelles ventes sans invalider automatiquement les droits acquis ;
- ne pas creer un second versionnement concurrent.

## 4. Documents d'achat a realigner

### Existant reutilisable

- le snapshot fige acheteur, coffret, prix, validite, Localeo et lignes de prestation ;
- `DocumentAchatCoffret` conserve type, emetteur, reference, version, hash et fichier ;
- le recu B2C et le recu consolide Animation indiquent deja ne pas etre des factures fiscales ;
- la facture des frais de service Localeo est separee.

### Conflit avec l'Epic 50

Le service actuel peut generer une facture commercant par achat avant consommation et indique que Localeo agit au nom et pour le compte du commercant. La cible Epic 50 retient que l'achat BUM ne facture pas la prestation et que la demande n'est possible qu'apres execution. Le commercant peut ensuite televerser sa facture ou utiliser un assistant : Localeo prepare le brouillon, mais le commercant verifie les donnees fiscales et declenche lui-meme l'emission sous sa responsabilite (`PRD-560`).

### A traiter

- transformer le recu en justificatif d'acquisition BUM ;
- conserver la facture des frais de service Localeo si elle reste applicable ;
- neutraliser la creation de nouvelles `FACTURE_COMMERCANT` et du pack ZIP actuel ;
- conserver temporairement les anciens types tant que l'absence de documents emis n'est pas verifiee ;
- remplacer le formulaire lie a l'achat par un workflow lie aux validations.

## 5. Demande de facture existante insuffisante

`DemandeFacturationAchatOrm` stocke aujourd'hui une demande de support, une adresse et un booleen `traitee`. Elle n'a ni validation de prestation, ni commercant, ni source Pro/Animation, ni workflow, ni snapshot complet, ni contrainte anti-doublon.

La decision retenue est de faire evoluer cet objet plutot que d'en creer un second. Comme aucune commercialisation n'a eu lieu, aucun historique de production ne justifie la coexistence des deux modeles.

La migration cible doit :

- renommer le concept metier en demande de facture au commercant, avec un nom ORM tel que `DemandeFactureCommercantOrm` ;
- conserver une racine de demande et ajouter une table de lignes reliant chaque demande a une `ValidationPrestation` ;
- remplacer `traitee` par les statuts `REQUESTED`, `ACKNOWLEDGED`, `PROCESSING`, `PROVIDED` et `CANCELLED` ;
- ajouter `commercant_id`, source, demandeur, commande, dates de traitement, commentaire et snapshot de facturation ;
- garantir en base qu'une validation ne peut appartenir qu'a une demande active ;
- supprimer les champs et parcours propres a la demande support lorsqu'ils ne servent pas la nouvelle cible ;
- retirer la creation automatique depuis `CreerMessageContactConsommateur` ;
- adapter ou supprimer la vue SQLAdmin actuelle ;
- effectuer une migration one-shot sans couche de compatibilite fonctionnelle.

## 6. Cycle financier deja largement aligne

La validation existante verifie l'instance, marque atomiquement la prestation, cree `ValidationPrestation`, puis un `MouvementReversement` idempotent transferable ou bloque selon Stripe Connect.

L'Epic 50 doit :

- garder `ValidationPrestation` comme source de verite de l'execution ;
- ne pas creer une entite `Redemption` qui la dupliquerait ;
- rattacher la demande de facture migree a cette validation et au mouvement existant ;
- tester qu'un paiement seul ne cree aucun reversement ;
- aligner validations de secours, annulations et expirations sur ces invariants.

## 7. Pro et Animation a etendre

`AchatCoffret` supporte deja les professionnels et les lots Animation. `CommandeAchat` offre une racine consolidee et les instances de lots restent inactives jusqu'a attribution.

Il faut reutiliser ces liens pour les justificatifs et le suivi des demandes, et ne pas introduire une seconde chaine de commandes. Un `BillingProfile` ne sera ajoute que pour la saisie et la reutilisation en amont ; chaque document ou demande conservera son snapshot.

## 8. Onboarding terrain a industrialiser

Le referentiel, les prestations, les invitations, Stripe Connect, les
documents et les controles de vendabilite existent deja, mais ils sont repartis
entre plusieurs interfaces et ne forment pas un parcours de rendez-vous. Il
n'existe pas de dossier d'onboarding versionne, de checklist conditionnelle ni
de diagnostic consolide indiquant pourquoi un commercant ne peut pas encore
etre publie, facture, reverse ou sollicite pour une facture.

L'Epic ajoute donc une PWA mobile interne, nommee provisoirement `Localeo
Onboard`. Elle doit orchestrer les cas d'usage existants, pas reimplementer les
regles dans le frontend. Les nouveaux objets se limitent au dossier, aux items
de checklist, aux preuves et au pilotage commercial ; les donnees metier restent
dans leurs agregats actuels.

Voir [le cadrage du parcours mobile](onboarding-commercant-mobile.md).

## Matrice d'action

| Composant | Action |
| --- | --- |
| `Coffret` / `CoffretOrm` | Etendre avec la synthese fiscale |
| `PrestationCoffretVersionOrm` | Etendre avec le questionnaire BUM |
| Controle de vendabilite | Ajouter le motif BUM |
| `InitialiserPaiement` | Reutiliser le diagnostic existant |
| `ServiceValidationPrestation` | Conserver comme source de consommation |
| `MouvementReversement` | Conserver et rattacher aux demandes si necessaire |
| Snapshots d'achat | Reutiliser pour le justificatif |
| `DocumentAchatCoffretOrm` | Reutiliser pour la tracabilite documentaire |
| Generation `FACTURE_COMMERCANT` | Neutraliser puis remplacer |
| `DemandeFacturationAchatOrm` | Migrer vers `DemandeFactureCommercantOrm` et supprimer le concept support actuel |
| `EvenementAuditOrm` | Reutiliser pour l'audit operationnel |
| `CommandeAchat` | Reutiliser comme racine consolidee Animation/Pro |
| Referentiel, prestations et profils | Reutiliser comme sources canoniques de Localeo OnBoard |
| Invitations commercant | Reutiliser sans exposer token ni mot de passe au commercial |
| `DocumentOrm` | Reutiliser pour les contrats et justificatifs signes |
| Dossier et checklist d'onboarding | Ajouter comme orchestration et projection, sans copie des donnees metier |

## Ordre d'implementation contextualise

1. modele fiscal, historique et migration d'initialisation ;
2. integration au controle central de vendabilite ;
3. referencement partenaire et questionnaire des versions de prestation ;
4. adaptation des recus B2C et Animation ;
5. neutralisation de la facture commercant a l'achat ;
6. migration de `DemandeFacturationAchatOrm` vers les demandes commercant rattachees a `ValidationPrestation` ;
7. vues BackOffice et Commercant ;
8. suivis Pro et Animation ;
9. recette multicanal avant premiere commercialisation.
10. application mobile d'onboarding, diagnostics par capacite et supervision
    du suivi commercial.

## Non-objectifs

- reconstruire Stripe, Stripe Connect ou les reversements ;
- remplacer le cycle des `CoffretInstance` ;
- dupliquer `ValidationPrestation` ;
- recreer le moteur documentaire ;
- migrer des ventes ou factures de production puisqu'aucun coffret n'a ete commercialise ;
- conserver la facture commercant a l'achat uniquement parce qu'elle est deja codee.
- creer un second referentiel commercant ou une seconde API de prestation pour
  l'application mobile.
