# Epic 50 - Conception technique

## 1. Objet et statut

Ce document transforme le cadrage fonctionnel de l'Epic 50 en cible
implementable dans `localeo-backend`. Il couvre les cinq scopes BackOffice,
Localeo OnBoard, Commercant, Marketplace et Animation, tout en conservant un
unique socle de regles, de donnees et d'audit dans le backend.

Les choix structurants du registre sont acquis. Les seuls travaux restant a
finaliser pendant l'implementation sont le wording definitif du justificatif
(`BUM-ARB-08`) et la liste conditionnelle des champs Chorus Pro
(`BUM-ARB-14`), ainsi que la validation Juridica/Finance de la liste minimale
des preuves d'onboarding (`BUM-ARB-45`). Ils sont portes par configuration et
le cadre Juridica/comptable de l'assistant de facturation (`BUM-ARB-49`). Ils
sont portes par configuration et ne bloquent pas le schema cible.

L'extension de credit d'achat B2B est decrite dans
[Credit d'achat B2B sur coffrets expires](credit-achat-b2b.md). Son registre de
mouvements s'ajoute au modele cible, mais son lot de livraison reste conditionne
aux validations externes indiquees dans `BUM-ARB-27`, `BUM-ARB-29`,
`BUM-ARB-30`, `BUM-ARB-32` et `BUM-ARB-40`.

Le parcours terrain est decrit dans
[Onboarding commercant mobile](onboarding-commercant-mobile.md). Les arbitrages
`BUM-ARB-42` a `BUM-ARB-48` retiennent le nom `Localeo OnBoard`, une PWA
interne en ligne, le profil `Localeo Admin` existant pour le MVP et le test de
connexion par le commercant sur son propre telephone. La politique de preuves
reste versionnee cote serveur afin d'integrer sa validation externe.

## 2. Principes d'architecture

1. Le backend est la source de verite pour la qualification, les montants, les
   workflows, les habilitations et les snapshots.
2. Marketplace, Animation et application Commercant ne recalculent aucune
   regle fiscale ou financiere.
3. Une donnee fiscale utilisee par un evenement economique est snapshottee ;
   une modification ulterieure du catalogue ne reecrit jamais l'historique.
4. Les effets metier et leurs enregistrements d'idempotence sont crees dans la
   meme transaction ; les emails, WebPush et rendus PDF sont rejouables.
5. Une facture emise est immuable. Une correction cree un avoir.
6. `ValidationPrestation` reste le fait generateur d'execution et
   `MouvementReversement` reste la source du reversement.
7. La qualification BUM enrichit
   `diagnostiquer_blocages_vendabilite_coffret` ; aucun canal ne porte son
   propre predicat.
8. Le stockage documentaire generique `DocumentOrm` est reutilise pour les
   factures. `DocumentAchatCoffretOrm` reste reserve au cycle d'achat.
9. Localeo OnBoard orchestre les memes cas d'usage que les autres interfaces.
   Sa checklist ne copie aucune donnee canonique et ne peut forcer une capacite
   declaree prete par le backend.
10. La completion globale est une projection de capacites independantes. Une
    publication ou une activation externe reste une commande explicite.

## 3. Decoupage applicatif cible

```text
app/domaine/
  onboarding_commercant/
    entities.py
    repositories.py
    services.py
  conformite_fiscale_bum/
    entities.py
    repositories.py
    services.py
  facturation_prestations/
    entities.py
    repositories.py
  facturation_localeo/
    entities.py
    repositories.py

app/application/
  onboarding_commercant/
    services/
    use_cases/
  conformite_fiscale_bum/
    services/
    use_cases/
  facturation_prestations/
    services/
    use_cases/
  facturation_localeo/
    services/
    use_cases/
  chorus_pro/
    services/
    use_cases/

app/infrastructure/persistence/
  models.py
  repositories/
  uow/sqlalchemy_unit_of_work.py

app/api/
  onboarding_commercant_api.py
  conformite_fiscale_bum_api.py
  facturation_prestations_api.py
  facturation_localeo_api.py
```

Le domaine Chorus Pro ne devient pas proprietaire des factures. Il ne gere que
leur depot et leur suivi.

## 4. Cartographie de l'existant

| Existant | Utilisation cible |
| --- | --- |
| `CoffretOrm`, `PrestationCoffretOrm` | Racines commerciales soumises au garde-fou BUM |
| `PrestationCoffretVersionOrm` | Version editoriale referencee par le screening et les snapshots |
| `diagnostiquer_blocages_vendabilite_coffret` | Point unique d'ajout du blocage `BUM_NON_VALIDE` |
| `AchatCoffretFacturationSnapshotOrm` | Base du justificatif d'acquisition et des identites d'achat |
| `ValidationPrestationOrm` | Fait generateur de la demande de facture et des montants d'execution |
| `MouvementReversementOrm` | Mouvement financier enrichi des montants bruts, commission et net |
| `ReversementOrm` et `LigneReversementOrm` | Campagne par commercant donnant lieu a facture de commission |
| `ConfigurationTvaLocaleoOrm` | Taux de TVA utilise pour ventiler la commission Localeo TTC |
| `AbonnementPlateformeOrm` et souscription Epic 47 | Origine de la facture d'abonnement Animation |
| `SequenceFacturationOrm` | Allocation transactionnelle des numeros Localeo |
| `DocumentOrm` | Stockage des PDF de facture et avoirs |
| `EmailSortantOrm`, WebPush, notifications Animation | Canaux asynchrones idempotents |
| `EvenementAuditOrm` / `ServiceAudit` | Journal des transitions et acces sensibles |
| `CommercantOrm`, profils et contacts | Donnees canoniques editees par le parcours terrain |
| `UtilisateurCommercantOrm` et invitations | Provisionnement et constat d'activation du compte, sans acces au mot de passe |
| Diagnostics de vendabilite et Stripe Connect | Sources des capacites de publication, reversement et facturation |

## 5. Modele de donnees

### 5.1 Politique et qualification BUM

#### `politiques_bum`

| Colonne | Type | Regle |
| --- | --- | --- |
| `id` | UUID | PK |
| `code_version` | TEXT | unique, ex. `BUM_POLICY_2026_01` |
| `statut` | TEXT | `BROUILLON`, `ACTIVE`, `ARCHIVEE` |
| `regles` | JSONB | questionnaire et regles de screening versionnes |
| `wording` | JSONB | cles de mentions, jamais HTML libre execute |
| `date_effet` | TIMESTAMP | obligatoire pour `ACTIVE` |
| `created_by`, `created_at` | TEXT, TIMESTAMP | audit |

Une seule politique peut etre `ACTIVE` a un instant donne. L'activation d'une
nouvelle version ne modifie aucune evaluation anterieure.

#### `diagnostics_fiscaux_prestations`

Conserve la prestation, sa version, la politique, les donnees factuelles
snapshottees, le resultat interne `AUTO_ELIGIBLE/REVIEW_REQUIRED/INELIGIBLE`,
les motifs et la date. Ce diagnostic n'est ni une qualification de la
prestation, ni une attestation ou une decision du commercant.
Contrainte unique sur `(prestation_coffret_id, prestation_version,
politique_id)`.

#### `qualifications_fiscales_coffrets`

| Colonne | Valeurs principales |
| --- | --- |
| `coffret_id` | FK coffret, index |
| `politique_id` | FK politique |
| `qualification` | `MULTI_PURPOSE`, `SINGLE_PURPOSE`, `UNKNOWN` |
| `statut` | `PENDING`, `VALIDATED`, `REJECTED`, `REQUALIFICATION_REQUIRED` |
| `motif` | obligatoire hors migration initiale standardisee |
| `qualified_by` | administrateur ou `SYSTEM_MIGRATION` |
| `source_snapshot` | JSONB des prestations et evaluations prises en compte |
| `qualified_at` | horodatage |

La qualification courante est la ligne la plus recente. L'historique n'est
jamais mis a jour. Un index partiel unique garantit une seule qualification
courante par coffret, via `is_current = true`.

### 5.2 Snapshot financier d'execution

Ajouter a `MouvementReversementOrm` :

- `montant_prestation_facturable_ttc NUMERIC(12,2)` ;
- `commission_localeo_ttc NUMERIC(12,2)` ;
- `commission_localeo_ht NUMERIC(12,2)` ;
- `commission_localeo_tva NUMERIC(12,2)` ;
- `taux_tva_localeo NUMERIC(5,2)` ;
- `commission_localeo_cible_ttc NUMERIC(12,2)` ;
- `montant_net_reverse NUMERIC(12,2)` ;
- `calcul_snapshot JSONB` ;
- `politique_calcul_version TEXT`.

Le champ historique `montant` devient l'alias persiste du net a reverser
pendant la transition. Une contrainte verifie :

```text
montant_net_reverse = montant_prestation_facturable_ttc - commission_localeo_ttc
commission_localeo_ttc = commission_localeo_ht + commission_localeo_tva
```

Les calculs utilisent `Decimal`, un arrondi monetaire explicite a deux decimales
et la configuration TVA Localeo applicable a `date_validation`.

### 5.3 Profil de facturation

Creer `profils_facturation` pour les valeurs reutilisables et ne jamais les
utiliser directement comme historique fiscal :

- proprietaire : `owner_type`, `owner_id` ;
- type : `INDIVIDUAL`, `BUSINESS`, `ASSOCIATION`, `PUBLIC_ENTITY` ;
- identite, raison sociale, SIRET, TVA, email et adresse ;
- references Chorus : code service, engagement, commande, marche, contrat ;
- `version`, `active`, `created_at`, `updated_at`.

Chaque demande et chaque facture copie les champs necessaires dans son snapshot.

### 5.4 Demande de facture au commercant

La table `demandes_facturation_achat` est migree one-shot et renommee
`demandes_facture_commercant`. Aucune donnee de production n'est reprise.

| Colonne | Description |
| --- | --- |
| `id`, `reference` | UUID et reference publique unique |
| `validation_prestation_id` | FK, unique pour toute demande non annulee |
| `commercant_id` | destinataire, index |
| `source` | `MARKETPLACE`, `PRO_ORDER`, `ANIMATION` |
| `requester_type`, `requester_id` | acteur demandeur |
| `achat_id`, `commande_id`, `animation_id` | racines d'autorisation facultatives |
| `statut` | workflow de la demande |
| `billing_snapshot` | identite complete du destinataire de facture |
| `prestation_snapshot` | prestation, coffret, version et date d'execution |
| `financial_snapshot` | brut TTC, commission separee, net reverse |
| `commentaire` | texte borne et nettoye |
| dates de transition | demande, prise en charge, traitement, fourniture, annulation |
| `invoice_document_id` | FK `DocumentOrm`, nullable |
| `invoice_number`, `invoice_date` | fournis par le commercant |
| `version` | verrouillage optimiste |

Un index partiel unique sur `validation_prestation_id` pour les statuts autres
que `CANCELLED` garantit l'anti-doublon. Une annulation ne reecrit pas
l'ancienne demande ; une nouvelle demande peut etre creee et reference
l'ancienne par `previous_request_id`.

Transitions autorisees :

```text
REQUESTED -> ACKNOWLEDGED -> PROCESSING -> PROVIDED
REQUESTED -> CANCELLED
ACKNOWLEDGED -> CANCELLED
PROCESSING -> CANCELLED
```

`PROVIDED` et `CANCELLED` sont terminaux. Le passage a `PROVIDED` exige le
document, le numero et la date de facture.

#### `brouillons_facture_commercant`

L'assistant de facturation repose sur un aggregate distinct du document final :

| Groupe | Colonnes |
| --- | --- |
| Identite | `id`, `demande_id`, `commercant_id`, `status`, `version` |
| Contenu | `seller_snapshot`, `buyer_snapshot`, `lines_snapshot`, `tax_snapshot`, `payment_snapshot`, `structured_invoice` |
| Numerotation | `series_id`, `invoice_number`, `invoice_date` |
| Emission | `confirmed_by`, `confirmed_at`, `issued_at`, `render_status`, `document_id`, `content_hash` |
| Audit | `created_at`, `updated_at`, `cancelled_at`, `cancellation_reason` |

Statuts : `DRAFT`, `ISSUED`, `CANCELLED`. Une contrainte unique garantit un
seul brouillon non annule par demande. `invoice_number` et `content_hash` sont
nuls en `DRAFT` et obligatoires en `ISSUED`. `document_id` devient obligatoire
lorsque `render_status = AVAILABLE`; un echec de rendu conserve la facture
emise et son numero, puis permet une reprise idempotente.

`tax_snapshot` est renseigne ou confirme par le commercant. Aucun service
Localeo ne deduit automatiquement le regime ou le taux de TVA de la prestation.
`structured_invoice` devient la source du rendu PDF et prepare une future
serialisation Factur-X, UBL ou CII.

#### `series_facture_commercant`

Conserve `id`, `commercant_id`, `code`, `prefix`, `next_number`,
`last_issued_at`, `status`, `accepted_by`, `accepted_at` et `version`. La
contrainte `(commercant_id, code)` est unique. La serie appartient au
commercant et ne partage jamais la sequence des factures emises par Localeo.

L'emission verrouille la serie, reserve et consomme le numero dans la meme
transaction que le passage du brouillon a `ISSUED`. Une annulation de brouillon
ne consomme aucun numero. Une facture emise ne libere jamais son numero.

### 5.5 Factures emises par Localeo

#### `factures_localeo`

Implemente par `v208_epic50_factures_localeo.sql`. La migration etend aussi
`abonnements_plateforme` avec les snapshots de facturation, tarification et
paiement requis avant emission.

| Groupe | Colonnes |
| --- | --- |
| Identite | `id`, `type`, `numero`, `statut`, `date_emission`, `date_exigibilite`, `devise` |
| Idempotence | `idempotency_key` unique, `source_type`, `source_id` |
| Acteurs | `emetteur_snapshot`, `destinataire_type`, `destinataire_id`, `destinataire_snapshot` |
| Montants | `total_ht`, `total_tva`, `total_ttc`, `deja_regle`, `net_a_payer` |
| Document | `document_id`, `template_version`, `content_hash`, `rendered_at` |
| Correction | `facture_origine_id`, `motif_avoir` |
| Audit | `created_by`, `created_at`, `issued_at`, `cancelled_at` |

Types : `COMMISSION_COMMERCANT`, `ABONNEMENT_ANIMATION`,
`AVOIR_COMMISSION`, `AVOIR_ABONNEMENT`.

Statuts : `DRAFT`, `ISSUED`, `CREDITED`, `CANCELLED`. Seul `DRAFT` est
modifiable. Un numero est attribue pendant la transition atomique vers
`ISSUED`.

#### `lignes_facture_localeo`

Conserve libelle, quantite, prix unitaire HT, taux TVA, HT, TVA, TTC, ordre et
`source_detail` JSONB. Les lignes de commission referencent les validations et
mouvements inclus sans FK polymorphe obligatoire.

#### Numerotation

`SequenceFacturationOrm` utilise :

- `scope_type = LOCALEO_INVOICE`, serie annuelle des factures ;
- `scope_type = LOCALEO_CREDIT_NOTE`, serie annuelle des avoirs ;
- `scope_id = NULL` ;
- verrou `SELECT ... FOR UPDATE` avant increment.

Format propose : `LOC-{annee}-{numero:06d}` et
`LOC-AV-{annee}-{numero:06d}`. Le format est une presentation ; l'unicite porte
sur `numero` et `type de serie`.

### 5.6 Depot Chorus Pro

La migration `v207_epic50_chorus_pro_manuel.sql` cree
`mandats_depot_chorus` et `depots_chorus_pro`. Le mandat conserve la version
contractuelle, le perimetre, l'acteur, les dates d'acceptation/revocation et le
document de preuve. Le depot conserve : facture ou demande source, document,
emetteur, destinataire snapshotte, mode `MANUAL`, statut stable, identifiants
Chorus, dates, rejet, compteur de tentatives, operateur, metadata et
`idempotency_key` unique.

Statuts : `A_DEPOSER`, `DEPOSEE`, `ACCEPTEE`, `SUSPENDUE`, `REJETEE`,
`MISE_EN_PAIEMENT`, `PAYEE`, `ANNULEE`.

Le meme aggregate accepte un emetteur `MERCHANT` avec mandat ou `LOCALEO`
sans mandat. En V1, l'operateur enregistre manuellement le depot et les retours
du portail. `PISTE_API` reste un mode reserve pour la V2.

### 5.7 Dossier d'onboarding commercant

#### `dossiers_onboarding_commercants`

| Groupe | Colonnes |
| --- | --- |
| Identite | `id`, `commercant_id`, `reference`, `statut`, `checklist_version` |
| Pilotage | `assigne_a`, `rendez_vous_at`, `prochaine_action`, `prochaine_action_responsable`, `prochaine_action_echeance` |
| Diagnostic | `checklist_snapshot`, `capabilities_snapshot`, `diagnosed_at` |
| Progression | `closed_at`, `motif_abandon` |
| Concurrence | `version`, `created_at`, `updated_at` |

Statuts : `BROUILLON`, `RDV_PLANIFIE`, `EN_COURS`, `A_COMPLETER`,
`PRET_A_VALIDER`, `VALIDE`, `CLOTURE`, `ABANDONNE`.

Le dossier reference un `CommercantOrm` cree au plus tard lors de la premiere
sauvegarde. La detection de doublon par SIRET, email et nom normalise precede
la creation. Les valeurs legales, publiques, fiscales et contractuelles restent
dans leurs agregats proprietaires.

#### Extension cible `items_onboarding_commercant`

| Groupe | Colonnes |
| --- | --- |
| Cle | `id`, `dossier_id`, `item_code`, `checklist_version` |
| Etat | `status`, `applicability`, `blocking_capabilities` |
| Preuve | `source_type`, `source_id`, `document_id`, `evidence_snapshot` |
| Decision | `checked_by`, `checked_at`, `comment`, `expires_at` |
| Concurrence | `version`, `created_at`, `updated_at` |

Cette table n'est pas creee par la premiere version. Celle-ci conserve un
instantane JSON versionne du diagnostic serveur dans le dossier. Une migration
ulterieure introduira les items persistants lorsque les validations manuelles
et les preuves documentaires de `PRD-552` et `PRD-554` seront implementees.

Statuts cibles : `TODO`, `IN_PROGRESS`, `READY`, `BLOCKED`, `NOT_APPLICABLE`,
`EXPIRED`. L'item memorise la preuve et la decision, pas une copie libre de la
donnee source. Une preuve manuelle exige acteur, date et commentaire ; une
preuve derivee est recalculee par le service de diagnostic.

La definition de checklist est versionnee cote serveur. Elle porte conditions
d'applicabilite, niveau obligatoire ou recommande, type de preuve, duree de
validite et capacites bloquees. Une ancienne version reste lisible pour l'audit.

#### Projection des capacites

La projection retourne pour chaque capacite `READY`, `BLOCKED` ou
`NOT_APPLICABLE`, les items bloquants et leur source. Elle n'est pas persistee
comme autorisation autonome : les commandes finales rejouent leurs propres
invariants dans la meme transaction.

### 5.8 Credit d'achat B2B

Le modele detaille est defini dans
[Credit d'achat B2B sur coffrets expires](credit-achat-b2b.md). Il repose sur :

- un compte unique par proprietaire contractuel et devise ;
- un registre immuable de mouvements `CREDIT`, `DEBIT`, `EXPIRATION` et
  `ADJUSTMENT` ;
- une allocation snapshottee par prestation lors de l'achat ;
- une reservation a duree limitee pour proteger le paiement concurrent ;
- un code opaque stocke sous empreinte et un OTP pour le parcours Pro sans
  compte permanent.

Le solde est une projection des mouvements confirmes diminuee des reservations
actives. Une contrainte et une cle idempotente empechent de crediter deux fois
la meme expiration ou de consommer deux fois la meme reservation.

## 6. Services applicatifs

### 6.1 Conformite BUM

- `EvaluerEligibilitePrestation` : execute les regles versionnees et persiste
  l'evaluation.
- `QualifierCoffret` : reserve a l'administrateur ; cree une nouvelle decision
  courante et archive la precedente.
- `DetecterRequalificationRequise` : compare la version publiee et le snapshot
  qualifie lors d'une modification significative.
- `InitialiserQualificationsCatalogue` : migration idempotente avec
  `SYSTEM_MIGRATION / INITIAL_CATALOG_BOOTSTRAP`.
- `VerifierVendabiliteBum` : retourne un blocage structure consomme par
  `diagnostiquer_blocages_vendabilite_coffret`.

### 6.2 Validation et reversement

Etendre `ServiceValidationPrestation.executer` dans sa transaction actuelle :

1. verrouiller et valider la prestation ;
2. resoudre version, montant brut, commission configuree et TVA Localeo ;
3. calculer les montants avec `Decimal` ;
4. creer `ValidationPrestation` ;
5. creer `MouvementReversement` et son snapshot financier ;
6. enregistrer l'evenement d'audit ;
7. commit ;
8. declencher les notifications existantes de maniere rejouable.

Cle mouvement existante conservee :
`mouvement:statut-prestation:{statut_prestation_id}`.

### 6.3 Demandes de facture

- `ListerPrestationsFacturables` applique les autorisations par surface.
- `CreerDemandeFactureCommercant` verrouille la validation, verifie qu'elle
  n'est pas annulee, cree les snapshots et la demande.
- `AccuserReceptionDemande`, `DemarrerTraitementDemande`,
  `AnnulerDemandeFacture` appliquent la machine a etats.
- `FournirFactureCommercant` controle PDF, taille, numero, date et proprietaire,
  cree le document puis passe la demande a `PROVIDED`.
- `CreerBrouillonFactureCommercant` pre-remplit les snapshots sans numero et
  sans notification au demandeur.
- `MettreAJourBrouillonFactureCommercant` exige le proprietaire authentifie et
  un verrou optimiste ; il ne calcule pas le regime ou le taux de TVA.
- `EmettreFactureCommercantAssistee` verrouille demande, brouillon et serie,
  valide la confirmation explicite, attribue le numero, fige le snapshot,
  marque la facture `ISSUED` et cree la demande de rendu atomiquement.
- `RendreFactureCommercantAssistee` cree ou retourne le document, puis passe
  la demande a `PROVIDED` et prepare la notification dans une transaction
  rejouable.
- `AnnulerBrouillonFactureCommercant` ne consomme aucun numero.
- `CreerCorrectionFactureCommercant` cree un avoir ou document correctif
  reference sans modifier le document emis.
- `ConsulterDemandeFacture` applique une policy d'autorisation commune aux
  routes et aux telechargements.

Cle de creation : `invoice-request:validation:{validation_id}`. Une violation
de contrainte retourne la demande existante avec `idempotent_replay = true`.

### 6.4 Facture de commission

La cloture d'une campagne de reversement appelle
`EmettreFactureCommissionCommercant` avant l'ordre de paiement :

```text
verrouiller reversement
  -> verifier tous les mouvements et snapshots
  -> retrouver ou creer facture par cle
  -> allouer numero
  -> figer lignes et totaux
  -> marquer ISSUED
  -> autoriser l'ordre de reversement
commit
  -> rendu PDF et notifications asynchrones
```

Cle : `COMMISSION:{commercant_id}:{reversement_id}`. Une panne PDF ne revient
pas sur la facture emise et ne duplique pas le paiement.

### 6.5 Facture d'abonnement Animation

Le traitement idempotent du webhook Stripe appelle
`EmettreFactureAbonnementAnimation` apres confirmation du paiement. La facture
reprend le snapshot de souscription Epic 47 ; Stripe ne fournit ni numero
Localeo ni recalcul fiscal.

Cle : `ABONNEMENT:{paiement_id}` ou, tant que le paiement generique n'est pas
disponible, `ABONNEMENT:STRIPE:{payment_intent_id}`.

### 6.6 Rendu documentaire

`RendreFactureLocaleo` :

- charge uniquement la facture `ISSUED` et ses lignes ;
- utilise `template_version` snapshottee ;
- produit des octets deterministes autant que le moteur PDF le permet ;
- calcule SHA-256 ;
- persiste `DocumentOrm` et l'empreinte ;
- retourne le document existant si deja genere ;
- interdit tout recalcul des montants.

### 6.7 Onboarding commercant

- `CreerOuReprendreDossierOnboarding` detecte les doublons et affecte le
  dossier.
- `ChargerChecklistOnboarding` resout la version et les items conditionnels.
- `MettreAJourDonneesOnboarding` delegue aux cas d'usage proprietaires du
  commercant, des contacts, des profils et des prestations.
- `AjouterPreuveOnboarding` controle puis rattache un `DocumentOrm` et sa
  metadata contractuelle.
- `EvaluerCapacitesOnboarding` appelle les diagnostics de referencement, BUM,
  vendabilite, Stripe Connect, facturation et identite-acces.
- `InviterUtilisateurCommercant` reutilise l'invitation existante et ne retourne
  jamais le token au client interne.
- `ValiderDossierOnboarding` verrouille le dossier, recalcule les capacites,
  refuse tout prerequis obligatoire manquant et journalise la decision.
- `CloreDossierOnboarding` produit le recapitulatif des actions et responsables
  restants sans modifier implicitement la publication.

## 7. Contrats API

Toutes les mutations acceptent `Idempotency-Key` et renvoient `409` pour une
transition concurrente incompatible, `422` pour une donnee incomplete et `403`
pour une ressource hors perimetre.

### 7.1 Scope BackOffice / backend

| Methode et route | Usage |
| --- | --- |
| `GET /internal/conformite-fiscale/bum/politiques` | Lister les versions |
| `POST /internal/conformite-fiscale/bum/politiques` | Creer une version |
| `POST /internal/conformite-fiscale/prestations/{id}/diagnostiquer` | Relancer le diagnostic interne depuis les donnees factuelles ; aucune qualification BUM de la prestation |
| `POST /internal/conformite-fiscale/bum/coffrets/{id}/qualifier` | Decision admin |
| `GET /internal/conformite-fiscale/bum/coffrets/{id}/diagnostic` | Diagnostic de publication |
| `GET /internal/facturation/demandes` | File des demandes |
| `GET /internal/facturation/factures-localeo` | Recherche et audit |
| `POST /internal/facturation/factures-localeo/{id}/rendre` | Rendu/reprise PDF |
| `POST /internal/facturation/factures-localeo/{id}/avoir` | Correction auditee |
| `GET /internal/chorus-pro/depots` | File operateur |
| `POST /internal/chorus-pro/depots/{id}/deposer` | Enregistrer depot manuel |
| `POST /internal/chorus-pro/depots/{id}/statut` | Reporter le statut Chorus |

Les ecrans SQLAdmin appellent les cas d'usage ; ils ne modifient pas directement
les tables fiscales.

### 7.2 Scope Commercant

| Methode et route | Usage |
| --- | --- |
| `GET /protected/commercants/me/facturation/demandes` | File personnelle |
| `GET /protected/commercants/me/facturation/demandes/{id}` | Detail et snapshots utiles |
| `POST .../{id}/accuser-reception` | `REQUESTED -> ACKNOWLEDGED` |
| `POST .../{id}/demarrer` | `ACKNOWLEDGED -> PROCESSING` |
| `POST .../{id}/facture` | Upload d'une facture externe et `PROVIDED` |
| `POST .../{id}/facture-assistee/brouillon` | Creer ou retourner le brouillon sans numero |
| `PATCH .../{id}/facture-assistee/brouillon` | Modifier les donnees sous verrou optimiste |
| `POST .../{id}/facture-assistee/emettre` | Confirmation commercant, numerotation et emission |
| `POST .../{id}/facture-assistee/annuler` | Abandonner le brouillon sans numero |
| `POST .../{id}/facture-assistee/correction` | Creer un avoir ou correctif reference |
| `POST .../{id}/annuler` | Annulation motivee |
| `GET /protected/commercants/me/factures-commission` | Liste par reversement |
| `GET .../{id}/telecharger` | PDF Localeo autorise |

### 7.3 Scope Marketplace

| Methode et route | Usage |
| --- | --- |
| `GET /public/coffrets-instances/{id}/facturation` | Prestations executees accessibles par token |
| `POST /public/coffrets-instances/{id}/demandes-facture` | Creation unitaire |
| `GET /public/coffrets-instances/{id}/demandes-facture` | Suivi |
| `GET .../demandes-facture/{demande_id}/telecharger` | Facture apres controle token/identite |
| `GET /protected/pro/commandes/{id}/facturation` | Vue multi-coffrets Pro |

La publication et l'initialisation du paiement conservent leurs routes ; elles
beneficient automatiquement du nouveau diagnostic BUM.

### 7.4 Scope Animation

| Methode et route | Usage |
| --- | --- |
| `GET /protected/animation-locale/animations/{id}/facturation-prestations` | Executions et demandes du tenant |
| `POST .../demandes-facture` | Creation pour une validation |
| `GET .../demandes-facture/{id}` | Suivi et document commercant |
| `GET /protected/animation-locale/abonnement/factures` | Factures Localeo du partenaire |
| `GET .../factures/{id}/telecharger` | PDF abonnement |
| `GET .../factures/{id}/chorus-pro` | Statut du depot public |

### 7.5 Scope Localeo OnBoard

Toutes les routes sont internes et authentifiees. Dans le MVP, elles sont
accessibles au profil `Localeo Admin`, qui dispose deja de l'ensemble des
droits BackOffice. Les invariants metier et l'audit restent obligatoires pour
chaque action sensible. Le contrat d'autorisation permettra d'introduire
ulterieurement un profil plus restrictif sans modifier les routes.

| Methode et route | Usage |
| --- | --- |
| `GET /internal/onboard` | Ouvrir la PWA interne |
| `GET /internal/onboard/api/commercants` | Rechercher les commercants canoniques |
| `GET /internal/onboard/api/dossiers` | Rechercher et filtrer les dossiers autorises |
| `POST /internal/onboard/api/dossiers` | Creer ou reprendre sans doublon |
| `GET /internal/onboard/api/dossiers/{id}` | Detail, checklist et capacites |
| `PATCH /internal/onboard/api/dossiers/{id}` | Affectation, rendez-vous et prochaine action |
| `POST /internal/onboard/api/dossiers/{id}/diagnostiquer` | Recalculer checklist et capacites |
| `POST /internal/onboard/api/dossiers/{id}/valider` | Verrouiller et valider le dossier |
| `POST /internal/onboard/api/dossiers/{id}/clore` | Cloturer le dossier |

Les routes de depot documentaire, de validation manuelle d'une preuve et
d'invitation sont des extensions planifiees, non exposees par cette premiere
version.

Les mises a jour de commercant et prestation reutilisent leurs routes ou cas
d'usage specialises. Une route generique d'onboarding ne doit pas contourner
leurs validations. Les reponses exposent un `etag` ou `version` et les
mutations refusent une version obsolete avec `409`.

### 7.6 Payloads minimaux

#### Qualification BackOffice

```json
{
  "qualification": "MULTI_PURPOSE",
  "status": "VALIDATED",
  "policyVersion": "BUM_POLICY_2026_01",
  "reason": "Validation du dossier et des prestations",
  "expectedVersion": 3
}
```

Reponse `200` : nouvelle qualification courante, version, auteur, date et
diagnostic de vendabilite recalcule.

#### Creation d'une demande

```json
{
  "validationPrestationId": "uuid",
  "billingProfileId": "uuid",
  "billing": {
    "buyerType": "PUBLIC_ENTITY",
    "legalName": "Commune exemple",
    "siret": "12345678900012",
    "billingEmail": "facturation@example.fr",
    "address": {
      "line1": "1 place de la Mairie",
      "postalCode": "33000",
      "city": "Bordeaux",
      "country": "FR"
    },
    "chorus": {
      "serviceCode": "SERVICE-01",
      "legalCommitmentNumber": "EJ-2026-001"
    }
  },
  "comment": null
}
```

Reponse `201` ou `200` en replay :

```json
{
  "id": "uuid",
  "reference": "DFC-2026-000001",
  "status": "REQUESTED",
  "idempotentReplay": false,
  "requestedAt": "2026-08-25T10:00:00Z"
}
```

Le backend ignore toute valeur financiere envoyee par le client et construit
`financial_snapshot` depuis la validation et le mouvement.

#### Mise a disposition par le commercant

Requete `multipart/form-data` : `file`, `invoiceNumber`, `invoiceDate`,
`comment`. Reponse : demande `PROVIDED`, metadata du document et indicateur
`chorusDepositRequired`.

#### Emission assistee par le commercant

Le brouillon expose un payload structure versionne. La commande d'emission
n'accepte ni numero ni totaux recalcules par le client :

```json
{
  "draftVersion": 3,
  "seriesCode": "LOCALEO-2026",
  "invoiceDate": "2026-08-30",
  "tax": {
    "regime": "VAT_APPLICABLE",
    "rate": "20.00",
    "exemptionMention": null
  },
  "merchantConfirmation": {
    "accepted": true,
    "wordingVersion": "MERCHANT_INVOICE_CONFIRMATION_2026_01"
  }
}
```

Le backend recharge demande et snapshots, controle la coherence des totaux,
verrouille la serie et retourne la facture `ISSUED`, son numero, son empreinte
et l'etat du rendu. L'URL protegee apparait lorsque le document est disponible.
`accepted=false`, une version obsolete ou une serie non configuree produit
`422` ou `409` sans consommer de numero.

#### Facture Localeo

```json
{
  "id": "uuid",
  "type": "COMMISSION_COMMERCANT",
  "number": "LOC-2026-000001",
  "status": "ISSUED",
  "issuedAt": "2026-08-31T18:00:00Z",
  "currency": "EUR",
  "totals": {"excludingTax": "3.75", "tax": "0.75", "includingTax": "4.50"},
  "source": {"type": "REVERSEMENT", "id": "uuid"},
  "document": {"available": true, "downloadUrl": "/protected/.../telecharger"}
}
```

Les montants monetaires sont serialises en chaines decimales, jamais en nombres
flottants.

#### Diagnostic d'onboarding

```json
{
  "dossierId": "uuid",
  "status": "IN_PROGRESS",
  "checklistVersion": "ONBOARDING_2026_01",
  "capabilities": {
    "PORTAIL_VISIBLE": {"status": "READY", "blockers": []},
    "BUM_READY": {
      "status": "BLOCKED",
      "blockers": ["PARTNER_CONVENTION_MISSING"]
    },
    "PORTAL_ACCESS_READY": {
      "status": "BLOCKED",
      "blockers": ["MERCHANT_INVITATION_NOT_ACTIVATED"]
    }
  },
  "nextActions": [
    {"code": "COLLECT_SIGNED_PARTNER_CONVENTION", "owner": "LOCALEO", "dueAt": null}
  ],
  "version": 4
}
```

### 7.7 Contrat d'erreur commun

```json
{
  "code": "INVOICE_REQUEST_ALREADY_EXISTS",
  "message": "Une demande existe deja pour cette prestation.",
  "correlationId": "LOC-...",
  "details": {"requestId": "uuid", "status": "REQUESTED"}
}
```

Codes stables principaux : `BUM_QUALIFICATION_REQUIRED`,
`BUM_REQUALIFICATION_REQUIRED`, `VALIDATION_NOT_INVOICEABLE`,
`INVOICE_REQUEST_ALREADY_EXISTS`, `INVALID_INVOICE_REQUEST_TRANSITION`,
`INVOICE_DOCUMENT_INVALID`, `LOCALEO_INVOICE_ALREADY_ISSUED`,
`CHORUS_DATA_INCOMPLETE`, `RESOURCE_OUTSIDE_SCOPE`.
Codes assistant : `MERCHANT_INVOICE_DRAFT_OUTDATED`,
`MERCHANT_INVOICE_CONFIRMATION_REQUIRED`, `MERCHANT_INVOICE_SERIES_MISSING`,
`MERCHANT_INVOICE_ALREADY_ISSUED`, `MERCHANT_INVOICE_TAX_DATA_INCOMPLETE`.
Codes onboarding : `ONBOARDING_DUPLICATE_MERCHANT`,
`ONBOARDING_CHECKLIST_OUTDATED`, `ONBOARDING_EVIDENCE_INVALID`,
`ONBOARDING_REQUIRED_ITEM_MISSING`, `ONBOARDING_CAPABILITY_BLOCKED`,
`MERCHANT_INVITATION_NOT_ACTIVATED`.

## 8. Evenements, notifications et traitements asynchrones

Evenements metier stables :

- `bum.qualification.changed` ;
- `prestation.validated` ;
- `merchant_invoice.requested` ;
- `merchant_invoice.acknowledged` ;
- `merchant_invoice.draft_created` ;
- `merchant_invoice.issued` ;
- `merchant_invoice.corrected` ;
- `merchant_invoice.provided` ;
- `merchant_invoice.cancelled` ;
- `localeo_invoice.issued` ;
- `localeo_credit_note.issued` ;
- `chorus_deposit.status_changed` ;
- `merchant_onboarding.started` ;
- `merchant_onboarding.evidence_added` ;
- `merchant_onboarding.capability_changed` ;
- `merchant_onboarding.validated` ;
- `merchant_onboarding.closed`.

V1 reutilise les tables de sortie existantes plutot que d'introduire une
plateforme de messages. Chaque notification possede une cle d'inclusion unique
derivee de `(event_type, resource_id, recipient, channel)`.

| Evenement | Email | In-app | WebPush |
| --- | --- | --- | --- |
| Demande creee | commercant | Commercant | si abonnement actif |
| Facture fournie | demandeur | surface origine | si configure |
| Facture commission emise | commercant | Finance commercant | facultatif |
| Facture abonnement emise | contact facturation | Animation | facultatif |
| Depot Chorus rejete | emetteur + operateur | BackOffice et surface origine | selon canal |

## 9. Autorisation et securite

- BackOffice : session administrateur ; motif obligatoire pour qualification,
  requalification, avoir et correction Chorus.
- Commercant : identite issue de session, `demande.commercant_id` obligatoire.
- Emission assistee : confirmation recente du commercant, wording versionne,
  aucune emission par un administrateur ou un traitement planifie ; les
  donnees fiscales confirmees sont auditees sans stocker de secret.
- Marketplace particulier : token de consultation chiffre/hashe et verification
  du rattachement a l'instance ; aucune enumeration par UUID seul.
- Pro : organisation de la session egale a celle de la commande.
- Animation : partenaire, commune et habilitation issus du contexte portail.
- Document : telechargement par controle applicatif puis URL courte signee ;
  aucun bucket public.
- Upload facture : PDF seulement en V1, taille bornee, controle MIME et
  signature, nom de fichier neutralise, analyse antivirus si disponible.
- Snapshots et journaux : pas de secret QR, pas de donnees bancaires dans les
  emails ou WebPush, masquage des donnees sensibles.
- Chaque creation, transition, rendu, telechargement, depot et correction est
  persiste via `ServiceAudit`.
- Localeo OnBoard : session interne forte du profil `Localeo Admin`, duree de
  session adaptee au mobile et reverification avant action sensible. Une
  permission dediee pourra etre ajoutee lorsque le BackOffice gerera des
  profils differencies.
- Le telephone ne conserve durablement ni contrat, ni token d'invitation, ni
  mot de passe. Les miniatures et caches sont nettoyes apres upload confirme.
- Le commercial ne peut valider une qualification BUM, une exception ou une
  publication que si une permission distincte l'autorise et si les invariants
  serveur sont rejoues.

## 10. Transactions et concurrence

| Operation | Protection |
| --- | --- |
| Qualification courante | verrou coffret + index partiel unique |
| Validation prestation | UPDATE conditionnel existant |
| Mouvement financier | cle idempotente existante unique |
| Demande facture | verrou validation + unique validation |
| Transition demande | `version` optimiste ou UPDATE sur statut attendu |
| Numero facture | ligne sequence `FOR UPDATE` |
| Facture commercant assistee | verrou demande + brouillon + serie, cle d'emission unique |
| Facture commission | unique `idempotency_key` avant reversement |
| Webhook abonnement | unique evenement Stripe + cle facture |
| Rendu PDF | verrou facture/document + retour du document existant |
| Depot Chorus | unique facture active + cle de depot |
| Dossier onboarding | version optimiste + verrou lors de la validation finale |
| Item de checklist | unique dossier + code + version de checklist |
| Upload de preuve | empreinte + cle idempotente + rattachement transactionnel |
| Invitation commercant | reutilisation de l'anti-doublon et des expirations existantes |

## 11. Migrations et activation

Les migrations additives implementees sont `v191` a `v214`. Elles couvrent
successivement les fondations BUM, demandes, snapshots financiers et
documentaires, presentation contractuelle, Localeo OnBoard, assistant de
facture, Chorus Pro, factures Localeo, registre de credit, demandes groupees,
echeances mixtes, corrections groupees, rattachement `organisation_pro_id` et
acceptation versionnee des conditions de credit. Elles doivent etre appliquees
dans cet ordre avant activation d'un indicateur Epic 50.

### Migration catalogue

Le script `InitialiserQualificationsCatalogue` est relancable :

```text
pour chaque coffret sans qualification courante
  creer MULTI_PURPOSE / VALIDATED
  qualified_by = SYSTEM_MIGRATION
  motif = INITIAL_CATALOG_BOOTSTRAP
  politique = version initiale
```

Il produit compteurs, anomalies et audit. Il ne republie aucun coffret.

### Decommissionnement

- supprimer l'appel de generation `FACTURE_COMMERCANT` a l'achat ;
- supprimer `PACK_FACTURES_ZIP` et ses CTA ;
- supprimer la creation de `DemandeFacturationAchatOrm` par le support ;
- conserver temporairement une lecture des anciens types documentaires seulement
  si une donnee locale de test l'exige ; aucune coexistence fonctionnelle ;
- faire echouer explicitement les anciennes commandes API avec `410 Gone`
  pendant une version, puis retirer les routes.

### Feature flags

- `FEATURE_BUM_QUALIFICATION_ENABLED` ;
- `FEATURE_BUM_PUBLICATION_GUARD_ENABLED` ;
- `FEATURE_MERCHANT_INVOICE_REQUEST_ENABLED` ;
- `FEATURE_MERCHANT_INVOICE_ASSISTANT_ENABLED` ;
- `FEATURE_LOCALEO_INVOICING_ENABLED` ;
- `FEATURE_CHORUS_MANUAL_DEPOSIT_ENABLED` ;
- `FEATURE_MERCHANT_ONBOARDING_ENABLED`.
- `FEATURE_B2B_PURCHASE_CREDIT_ENABLED`.

Le wording du credit est externalise par
`LOCALEO_B2B_CREDIT_TERMS_VERSION` et `LOCALEO_B2B_CREDIT_TERMS_TEXT` ; sa
version et son empreinte sont conservees a l'achat Pro et a la premiere
utilisation.

Localeo OnBoard ne porte aucune action de publication. Il prepare les donnees
et expose les diagnostics ; les actions de publication et la decision BUM du
coffret restent dans leurs surfaces canoniques.

Activation : schema -> migration catalogue -> BackOffice -> Localeo OnBoard en
pilote -> garde-fou en mode observation -> garde-fou bloquant -> demandes ->
assistant de facturation en pilote -> factures Localeo -> Chorus -> credit B2B
en pilote.

## 12. Observabilite

Metriques minimales :

- coffrets par statut de qualification ;
- blocages BUM par motif et canal ;
- demandes par statut, age et commercant ;
- delai demande-fourniture et echecs de notification ;
- brouillons de facture par statut, taux d'abandon, emissions et conflits de
  sequence ;
- ecart commission configuree / cible 15 % ;
- reversements sans facture de commission emise : doit rester a zero ;
- factures sans PDF, rendus en echec et replays ;
- depots Chorus par statut, age, rejet et tentative ;
- dossiers d'onboarding par statut, commercial, commune et age ;
- taux de completion au rendez-vous et delai jusqu'a validation ;
- blocages par item et par capacite ;
- echecs d'upload, invitations non activees et documents expires.

Alertes : publication contournee, doublon refuse, rupture arithmetique, sequence
indisponible, reversement sans facture, document inaccessible, file Chorus en
retard et echec permanent de notification.

## 13. Strategie de tests

### Domaine

- matrices de screening et version de politique ;
- transitions de qualification et requalification ;
- calcul Decimal brut/commission/TVA/net, arrondis et taux nul ;
- machines a etats demande, facture et depot ;
- brouillon assiste, confirmation commercant, numerotation et correction ;
- immutabilite et creation d'avoirs ;
- transitions du dossier, applicabilite des items et calcul independant des
  capacites d'onboarding.

### Persistence

- contraintes uniques et partielles ;
- concurrence sur validation, demande et sequence ;
- concurrence d'emission assistee, replay et absence de trou lie aux brouillons ;
- migration initiale executee deux fois ;
- rollback atomique facture/reversement ;
- aucune donnee support historique necessaire ;
- unicite dossier/item, concurrence sur validation et conservation des versions
  de checklist.

### API et autorisations

- chaque route nominale, `401`, `403`, `404`, `409`, `422` ;
- matrice particulier/Pro/Animation/commercant/admin ;
- acces croise interdit entre acheteurs, commercants et tenants ;
- replay avec la meme cle et conflit avec une charge differente ;
- telechargement document apres controle d'autorisation ;
- matrice `Localeo Admin` / utilisateur non authentifie, puis profil restreint
  lorsqu'il sera introduit ;
- upload multipart, version obsolete, doublon commercant et validation bloquee.
- creation et modification du brouillon, confirmation obligatoire, droits du
  commercant et refus d'une emission admin.

### Integration

- achat BUM -> justificatif, sans facture commercant ;
- validation -> snapshot financier -> mouvement ;
- demande -> notification -> upload -> notification demandeur ;
- demande -> brouillon -> confirmation commercant -> numero unique -> PDF ->
  notification demandeur ;
- cloture reversement -> facture commission -> paiement -> rendu PDF ;
- webhook Stripe rejoue -> une facture abonnement ;
- depot Chorus manuel, rejet, correction et acceptation ;
- annulation post-emission -> avoir et regularisation.
- rendez-vous -> collecte -> document signe -> prestation -> diagnostic BUM ->
  invitation -> validation ou plan d'actions restant.

### Non-regression

- parcours QR, feedback, Stripe Connect et payouts ;
- commandes Pro et lots Animation ;
- documents d'achat existants hors factures de prestation ;
- emails, WebPush et audit generique.
- referentiel, espace Commercant, Stripe Connect, documents et publication
  manipules depuis leurs autres surfaces.

## 14. Decoupage de livraison recommande

1. **Fondations BUM** : `PRD-448` a `PRD-454`, migrations et garde-fou en
   observation.
2. **Justificatif BUM** : `PRD-455` a `PRD-458`, decommissionnement Epic 14.
3. **Snapshot financier** : `PRD-459`, adaptation validation et reversement.
4. **Demandes commercant backend** : `PRD-460` a `PRD-462`.
5. **Assistant de facturation commercant** : `PRD-560`, brouillon structure,
   serie par commercant, confirmation explicite, emission et correction.
6. **Surfaces Marketplace, Pro et Animation** : `PRD-463`.
7. **Factures Localeo** : `PRD-470` a `PRD-473`, commission puis abonnement.
8. **Chorus Pro manuel** : `PRD-467` a `PRD-469`.
9. **Durcissement** : `PRD-464` a `PRD-466`, charge, securite et observabilite.
10. **Credit d'achat B2B et regroupement Pro** : `PRD-474` a `PRD-478`, registre,
   code + OTP, expiration, paiement mixte, surfaces Pro/Animation et demandes
   regroupees par achat/commercant apres validation des arbitrages.
11. **Onboarding commercant mobile** : `PRD-551` a `PRD-559`, dossier,
    checklist versionnee, documents signes, diagnostics par capacite, acces
    commercant et supervision commerciale selon les decisions
    `BUM-ARB-42` a `BUM-ARB-48` ; la liste documentaire doit etre validee avant
    activation.

Chaque lot est deployable derriere feature flag et doit conserver une base
compatible avec le lot suivant.

## 15. Definition de pret technique

L'implementation d'un lot peut commencer lorsque :

- ses tables, contraintes et proprietaires sont identifies dans ce document ;
- ses routes et sa matrice d'autorisation sont acceptees ;
- ses cles d'idempotence sont fixees ;
- ses evenements et notifications sont listes ;
- ses criteres de tests sont transformes en cas executables ;
- le wording est externalise lorsqu'il n'est pas encore valide.
- pour le lot OnBoard, le nom, l'usage exclusivement en ligne, les
  habilitations MVP et la preuve d'acces sont integres ; la liste des preuves
  reste configurable jusqu'a sa validation Juridica/Finance.

L'Epic est techniquement implementable par lots. La mise en production du
justificatif, du depot Chorus, de la checklist documentaire et de l'assistant
de facturation reste conditionnee aux validations externes identifiees en
section 1.

## 16. Tracabilite exigences vers composants

| Exigences | Composants principaux | Verification minimale |
| --- | --- | --- |
| `E50-RG-001` a `E50-RG-006` | domaine `conformite_fiscale_bum`, politique, evaluations, qualifications, diagnostic de vendabilite | tests de domaine et non-contournement multicanal |
| `E50-RG-007` a `E50-RG-011` | `ValidationPrestation`, snapshot financier, mouvement, demandes et lignes | tests transactionnels, concurrence et idempotence |
| `E50-RG-008`, `E50-RG-012` | documents d'achat, `FactureLocaleo`, sequences et avoirs | tests de snapshot, immutabilite et rendu rejouable |
| `E50-RG-013` | profils publics et `depots_chorus_pro` | recette des obligations destinataire et transitions Chorus |
| `E50-RG-014` a `E50-RG-016` | comptes, mouvements, allocations et reservations de credit | tests arithmetiques en centimes et concurrence |
| `E50-RG-017` a `E50-RG-020` | dossiers, items, documents, invitations et projection des capacites | tests de droits, absence de secret client et audit |
| `E50-RG-021` a `E50-RG-026` | brouillons, series commercant, rendu et documents correctifs | tests de confirmation, numerotation concurrente, immutabilite et droits |

La [specification fonctionnelle](specification-fonctionnelle.md) porte les
exigences `E50-RG-*`. Le backlog conserve la tracabilite vers les User Stories
`PRD-*`. Une evolution d'une regle doit mettre a jour ces trois niveaux dans le
meme changement documentaire ou applicatif.

## 17. Portes de deploiement et d'activation

| Porte | Conditions | Effet autorise |
| --- | --- | --- |
| `G0_SCHEMA_READY` | migrations testees deux fois, rollback documente, contraintes et indexes verifies | deploiement du schema sans exposition fonctionnelle |
| `G1_OBSERVATION_READY` | politique initiale chargee, diagnostics traces, tableaux de bord disponibles | garde-fou BUM en observation |
| `G2_PUBLICATION_GUARD_READY` | catalogue migre, aucun canal de contournement, recette de non-regression | blocage effectif des offres non conformes |
| `G3_DOCUMENT_READY` | `BUM-ARB-08` valide et version active configuree | emission du justificatif BUM |
| `G4_INVOICE_FLOW_READY` | snapshots, demandes, autorisations et notifications recetes | demandes de facture et factures Localeo |
| `G5_CHORUS_READY` | `BUM-ARB-14` valide en recette et procedure operatoire disponible | depot manuel Chorus Pro |
| `G6_CREDIT_READY` | validations `BUM-ARB-27`, `29`, `30`, `32`, `40` referencees | attribution et consommation du credit B2B |
| `G7_ONBOARD_READY` | `BUM-ARB-45` valide, stockage documentaire et droits recetes | activation de Localeo OnBoard |
| `G8_MERCHANT_INVOICE_ASSISTANT_READY` | `BUM-ARB-49` valide, serie, confirmation, rendu et corrections recetes | emission assistee par le commercant |

Chaque porte est reversible par feature flag, sauf les migrations de schema.
La desactivation d'une fonction empeche de nouvelles operations mais ne masque
ni ne supprime les donnees ou documents deja crees.

## 18. Contrat de livraison d'un lot

Un lot est livrable lorsque :

1. ses exigences `E50-RG-*` et User Stories `PRD-*` sont identifiees ;
2. domaine, cas d'usage, repositories, UoW, ORM et API respectent les frontieres
   de l'architecture existante ;
3. les migrations sont additives, idempotentes dans le processus du projet et
   ne modifient aucune migration deja appliquee ;
4. les erreurs API utilisent des codes stables et n'exposent pas de donnees
   sensibles ;
5. les tests domaine, persistence, API, autorisations, concurrence et
   non-regression du lot sont verts ;
6. metriques, logs, audit, procedure d'exploitation et strategie de retour
   arriere sont disponibles ;
7. la porte d'activation correspondante est soit satisfaite, soit maintenue
   fermee en production.
