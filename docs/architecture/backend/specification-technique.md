# Specifications techniques - Localeo Backend

> Mise a jour du 7 septembre 2026 : [commission par prestation et saisie en euros](../../specifications/epic-60-vision-360-commercialisation/commission-par-prestation.md). Cette decision remplace les anciennes regles de marge cible par coffret/type.

## 1. Objet

Ce document decrit l'etat technique de `localeo-backend` : stack, architecture, modules, flux, persistance, securite, observabilite, integrations et points d'exploitation.

## 2. Stack

- Langage : Python.
- Framework HTTP : FastAPI / Starlette.
- Administration : SQLAdmin.
- ORM : SQLAlchemy.
- Base : PostgreSQL.
- Driver : `psycopg`.
- Paiement : Stripe SDK Python.
- Email/SMS : Brevo via `requests`.
- Configuration : `python-dotenv` et variables d'environnement.
- Password hashing : `bcrypt`.
- QR : signatures HMAC avec keyring.

## 3. Organisation applicative

### 3.1 `app/main.py`

Responsabilites :

- configure logging, traces et runtime config ;
- instancie FastAPI ;
- branche CORS si configure ;
- ajoute `SessionMiddleware` pour SQLAdmin ;
- protege les routes `/internal/*` par session admin ;
- decide les autorisations sur le chemin ASGI, jamais sur une URL reconstruite
  depuis `Host` ; rejette les autorites HTTP malformees ou dupliquees avant tout
  traitement ; les donnees PWA internes exigent aussi une session au router ;
- inclut les routers publics et proteges ;
- configure SQLAdmin ;
- personnalise OpenAPI ;
- centralise les exception handlers.

### 3.2 `app/api`

Expose les endpoints HTTP :

- `villes_api.py`, `types_*_api.py`, `coffrets_api.py`, `commercants_api.py` ;
- `paiements_api.py`, `achats_api.py`, `coffret_instances_api.py` ;
- `validation_api.py`, `feedbacks_prestation_api.py`, `activites_locales_api.py` ;
- `contacts_api.py`, `profils_commercants_api.py` ;
- `emails_api.py`, `sms_api.py`, `maintenance_api.py`, `reversements_api.py` ;
- `images_api.py`, `liens_courts_api.py`, `qr_api.py`, `statistiques_api.py` ;
- `documents_api.py` pour la gestion documentaire transverse.

### 3.3 `app/application`

Contient les use cases, services applicatifs et `UnitOfWork`.

Principes :

- chaque scenario metier est porte par une classe `execute(...)` ;
- les transactions passent par `SqlAlchemyUnitOfWork` quand le use case est transactionnel ;
- les services applicatifs factorisent tokens, sessions, documents, profils, feedbacks, activites, audit, email/SMS ;
- `gestion_documentaire.py` porte upload, metadonnees, mise a jour de contenu, publication, audit, rattachements, stockage externe et controle d'acces commercant.

Regle Unit of Work obligatoire pour les evolutions :

- tout use case qui lit ou modifie la base doit recevoir ou instancier un `uow_factory`, puis ouvrir sa transaction avec `with self.uow_factory() as uow` ;
- les commits et rollbacks d'un use case doivent passer par `uow.commit()` et `uow.rollback()` ;
- un use case ne doit pas importer ni utiliser directement `SessionLocal`, `session_factory`, `session.commit()` ou `session.rollback()` ;
- les services applicatifs appeles depuis un use case doivent reutiliser le `uow` ou la `session` fournie par le use case appelant, sans ouvrir de transaction autonome ;
- les effets secondaires persistants lies a une action metier, par exemple outbox email/SMS/WebPush, audit ou activite locale, doivent etre crees dans la meme transaction metier que l'action source ;
- les batchs d'envoi doivent consommer les outbox deja creees et ne doivent pas rescanner les donnees metier pour reconstruire implicitement des notifications ;
- les exceptions a cette regle doivent rester cantonnees aux composants d'infrastructure ou d'orchestration technique explicitement documentes, par exemple le suivi d'execution des batchs.

Cette regle doit etre verifiee a chaque nouvelle evolution applicative et lors des revues de code.

### 3.4 `app/domaine`

Contient :

- entites metier ;
- enums et statuts ;
- exceptions metier ;
- value objects (`Email`, `NumeroTelephone`, `CodePostal`, `MontantEuroCentimes`) ;
- contrats de repositories.

Organisation DDD cible :

```text
app/domaine/
  entities/
    une_classe_par_entite.py
  value_objects/
    une_classe_par_value_object.py
  repositories/
    une_classe_ou_protocole_par_repository.py
  exceptions/
    une_classe_par_exception_metier.py
```

Regles :

- chaque entite metier doit avoir un nom explicite et un fichier dedie ;
- les enums et statuts fortement rattaches a une entite restent dans le fichier de cette entite au debut ;
- chaque entite porte les invariants qui dependent de son etat et protege ses propres transitions ;
- chaque value object doit porter ses invariants dans une classe dediee ;
- une regle qui associe plusieurs objets metier est portee par un service de domaine pur lorsqu'elle ne peut
  pas appartenir naturellement a un seul agregat ;
- la couche application orchestre le chargement, la transaction, les ports et les effets secondaires, mais
  ne devient pas proprietaire des invariants ;
- toute condition metier ajoutee dans un service applicatif doit etre justifiee comme orchestration ou
  deplacee vers le domaine ;
- une Epic doit documenter les agregats, invariants et transitions modifies avant de detailler les services
  applicatifs et les routes ;
- chaque repository domaine est un port, pas une implementation SQLAlchemy ;
- chaque exception metier doit exprimer une intention metier precise ;
- les anciens modules `modeles.py`, `value_objects.py` et `exceptions.py` ne doivent pas rester comme facades de compatibilite durables apres la migration ;
- la migration doit etre one-shot et sans changement fonctionnel ;
- le package cible des value objects est `value_objects`, pas `value_objets`.

Gestion des imports et noms publics :

- les classes, enums, protocoles et exceptions deja importes par les autres couches sont consideres comme des noms publics ;
- un deplacement de fichier peut s'accompagner d'un renommage public si le nouveau nom est explicite et migre partout dans la meme passe ;
- les anciens chemins d'import doivent etre supprimes des consommateurs dans la meme passe ;
- les nouveaux chemins d'import doivent pointer directement vers les packages cibles ;
- un renommage public exige la mise a jour immediate de tous les imports consommateurs ;
- les modules historiques sont supprimes ou vides de definitions metier apres verification de l'absence d'imports consommateurs.

### 3.5 `app/infrastructure`

Contient :

- modeles ORM ;
- repositories SQLAlchemy ;
- mappers domaine/ORM ;
- gateway Stripe ;
- services Brevo email/SMS ;
- service QR ;
- stockage documentaire local/S3 ;
- back-office SQLAdmin ;
- modeles media et reversements.

### 3.6 `app/security`

Contient les dependances et helpers securite :

- `api_keys.py` : API key hashee, prefix, scope ;
- `management_token.py` : controle des tokens achat et activation ;
- `consultation_token.py` : generation URL/hash/expiration consultation ;
- `activation_token.py` : activation token ;
- `commercant_session.py` : extraction bearer et controle session commercant.

## 4. Architecture technique

L'application suit une architecture en couches pragmatique :

1. Route FastAPI.
2. Dependances de securite.
3. Use case applicatif.
4. Unit of Work.
5. Repository SQLAlchemy.
6. Mapper domaine/ORM.
7. Provider externe si necessaire.

Le couplage n'est pas strictement hexagonal : plusieurs use cases retournent directement des dictionnaires destines aux schemas API. Ce choix reste coherent avec le stade produit, mais doit etre surveille si la complexite front augmente.

## 5. Persistance

### 5.1 Tables principales

- Catalogue : `villes`, `types_commercants`, `types_coffrets`, `commercants`, `coffrets`, `prestations_coffret`, `prestations_coffret_versions`.
- Profils : `profils_commercants`, `profils_commercants_versions`.
- Achat : `achats_coffret`, `coffrets_instances`, `paiements`, `paiement_events`.
- Documents : `configuration_tva_localeo`, `achats_coffret_facturation_snapshot`, `achats_coffret_facturation_snapshot_lignes`, `documents_achat_coffret`, `demandes_facturation_achat`, `sequences_facturation`, `documents`, `document_rattachements`.
- Usage : `statuts_prestation_coffret_instance`, `transactions_validation`, `validations_prestation`, `validations_secours`.
- Feedback/activite : `feedbacks_prestation`, `activites_locales`.
- Auth commercant : `identifiants_commercant`, `sessions_commercant`, `tokens_acces_commercant`, `rate_limits_authentification`.
- Support : `motifs_contact`, `messages_contact`, `liens_courts`.
- Notifications : `emails_sortants`, `sms_sortants`, `relances_expiration_coffrets`.
- Batchs : `executions_batch`, `verrous_batch`.
- Reversements : `comptes_reversement_commercants`, `mouvements_reversement`, `comptes_bancaires_commercants`, `reversements`, `lignes_reversement`, `lots_paiement_reversement`, `paiements_reversement`.
- Technique : `api_keys`, `evenements_audit`, `media_assets`.

### 5.2 Migrations

Le dossier `sql/` contient des scripts versionnes. Le bootstrap peut aussi creer/adapter certains elements au demarrage.

Point d'exploitation :

- en production, la source de verite doit etre une chaine de migration explicite ;
- `create_all` et les patchs bootstrap sont utiles en local mais ambigus pour un go-live strict.

## 6. Flux techniques

### 6.1 Paiement Stripe

1. `POST /public/gestion-achats/paiements/initialiser`.
2. Creation de `AchatCoffret`.
3. Appel `stripe.checkout.Session.create`.
4. Stripe rappelle `POST /public/stripe/webhook`.
5. Verification `Stripe-Signature`.
6. Dedupe par `paiement_events`.
7. Creation paiement, instances, QR, outbox, snapshots et audit.

### 6.2 Achat professionnel

1. Validation paiement.
2. Generation `management_token`.
3. Stockage `management_token_hash`.
4. Creation d'instances `EN_ATTENTE_ACTIVATION`.
5. Gestion via routes `/protected/achats/*`.
6. Activation via management token ou activation token.

### 6.3 Consultation instance

1. Generation `consultation_token`.
2. Stockage hash, dates et revocation.
3. Transport via bearer sur les APIs backend.
4. Construction de liens front contenant actuellement le token.
5. Verification hash, expiration et revocation a chaque consultation.

### 6.4 Session commercant

1. Login normalise.
2. Verification bcrypt.
3. Rate limit login + IP.
4. Creation session opaque.
5. Stockage hash du token.
6. Verification scope par dependance FastAPI.
7. Revocation manuelle ou purge.

### 6.5 Validation terrain

1. Commercant authentifie.
2. Lecture QR client signe.
3. Creation transaction courte.
4. Validation prestation.
5. Creation validation, mouvement de reversement, email de confirmation.

### 6.6 Outbox email/SMS

1. Use case metier cree `EmailSortant` ou `SmsSortant`.
2. Batch reserve les messages.
3. Provider Brevo est appele.
4. Statut local mis a jour.
5. Batch de synchronisation recupere les statuts provider.

### 6.7 Reversements Stripe Connect

1. Les validations creent des mouvements.
2. Les mouvements sont agreges en reversements.
3. Les mouvements transferables sont selectionnes dans une campagne bimensuelle.
4. Les transfers sont executes via Stripe Connect.
5. Les statuts sont synchronises via Stripe et audites.

Les anciens lots de paiement manuel, exports CSV et confirmations bancaires sont
decommissionnes par l'EPIC 39 et ne doivent pas etre reutilises comme fallback.

### 6.8 Gestion documentaire transverse

Routes principales :

- `POST /admin/api/documents/admin` : upload et creation de metadonnees documentaires ;
- `POST /admin/api/documents/admin/{document_id}/contenu` : remplacement du contenu binaire d'un document existant sans changer son identifiant ni ses rattachements ;
- `POST /admin/api/documents/admin/{document_id}/html` : creation ou mise a jour du contenu HTML derive ;
- `POST /admin/api/documents/admin/{document_id}/publier` : publication directe admin ;
- `POST /admin/api/documents/admin/{document_id}/archiver` : archivage fonctionnel ;
- `GET /admin/api/documents/admin/{document_id}/download` : telechargement backend admin ;
- `GET /public/documents?scope=SITE_PUBLIC` : listing public des documents publies exposables sur le site ou la marketplace ;
- `GET /public/documents/{type_document}` : consultation HTML publique du contenu publie ;
- `GET /public/documents/{document_id}/download` : telechargement public via backend ;
- `GET /protected/commercants/documents` : liste des documents prives rattaches au commercant authentifie ;
- `GET /protected/commercants/documents/{document_id}/download` : telechargement commercant avec verification du rattachement.

Modeles :

- `DocumentOrm` stocke les metadonnees documentaires, le statut, les scopes, le format, le hash et la reference opaque de stockage ;
- la mise a jour d'un document remplace son contenu et recalcule les metadonnees techniques, sans creer de nouvelle version fonctionnelle ;
- `DocumentRattachementOrm` rattache un document a une ressource metier (`COMMERCANT`, `CLIENT`, `ACHAT_COFFRET`, `COFFRET_INSTANCE`).

Stockage :

- aucun binaire n'est stocke en base ;
- `LocalDocumentStorage` ecrit en filesystem pour le developpement ;
- `S3DocumentStorage` utilise `boto3` et une API S3 compatible pour Scaleway Object Storage ;
- la cle de stockage est prefixee par la configuration applicative et reste opaque pour les utilisateurs.

Back-office :

- `GestionDocumentaireAdmin` expose `/admin/gestion-documentaire` ;
- l'upload PDF avec option `Version HTML` ouvre un ecran de preview/edition ;
- la sauvegarde de l'ecran HTML cree un document derive rattache au PDF source.

### 6.9 Tests fonctionnels domaine et application

La couche de tests fonctionnels cible les regles metier sans passer par HTTP ni par SQLAdmin.

Organisation cible :

```text
tests/
  domain/
    entities/
    value_objects/
  application/
    fakes/
    builders/
    services/
    use_cases/
```

Regles :

- les tests domaine couvrent les invariants des entites et value objects ;
- toute nouvelle regle metier possede au moins un test domaine sans Unit of Work, ORM, base ou fournisseur
  externe ;
- les tests application couvrent les use cases et services applicatifs via fakes de repositories, Unit of Work et providers ;
- toute modification d'un use case, d'un service applicatif ou d'un objet du domaine doit creer ou mettre a jour le test associe dans la meme livraison ;
- toute modification de la couche infrastructure, notamment repository, mapper, provider, gateway, stockage, SQLAdmin ou integration externe, doit creer ou mettre a jour le test associe dans la meme livraison ;
- chaque use case applicatif public exposant `execute` doit disposer d'une classe `Test<UseCase>` dediee dans `tests/application/use_cases` avec des scenarios metier ou workflow observables ; l'import, l'existence de classe ou la simple instanciation sont interdits comme couverture ;
- chaque classe publique de `app/domaine` doit disposer d'un fichier de test dedie sous `tests/domain/<domaine>/<categorie>` ; ce fichier sert de point d'ancrage et ne remplace pas les scenarios metier ;
- les tests peuvent regrouper plusieurs classes d'un meme domaine fonctionnel lorsque cela rend les scenarios plus lisibles ;
- chaque test doit verifier une regle observable, un invariant, une transition d'etat, un appel de port ou un contrat technique utile ; un simple test d'import ou d'existence de classe ne suffit pas a couvrir la classe ;
- les tests ne doivent pas appeler Stripe, Brevo, une base de donnees ou un service externe ;
- les donnees de test doivent etre fictives et sans secret reel ;
- chaque UC fonctionnel majeur doit etre rattache a un test cible ou a une justification hors perimetre ;
- le cahier de test backoffice reste la reference de recette UI, mais ses invariants metier doivent etre traduits en tests application quand ils sont independants de l'interface.

## 7. Securite

### 7.1 Protections existantes

- API keys internes hashees avec prefix et scope.
- Tokens opaques pour management, activation, consultation et sessions.
- Hash SHA-256 des tokens persistants.
- Comparaison constante via `hmac.compare_digest`.
- Password hashing bcrypt.
- Rate limit applicatif pour login et reset password commercant.
- Webhook Stripe signe.
- Middleware de protection des routes `/internal/*`.
- Validation runtime des secrets critiques.
- Erreurs HTTP globales avec `correlationId` canonique et alias deprecie
  `request_id` portant strictement la meme valeur.

### 7.2 Points techniques a corriger avant production

- Des endpoints publics d'ecriture existent et doivent etre proteges ou justifies.
- L'upload image public doit etre protege.
- Les SVG sont acceptes par l'API image ; cela doit etre interdit ou sanitise.
- Les tokens sont construits dans des URLs front et risquent de fuiter via logs/referrers.
- Les logs HTTP n'enregistrent que les noms des parametres de query string ; les
  valeurs restent exclues.
- SQLAdmin utilise une session cookie ; les actions POST doivent etre protegees contre CSRF.
- Les docs OpenAPI sont exposees par defaut ; elles doivent etre fermees ou protegees en production.
- `TrustedHostMiddleware` et headers de securite applicatifs ne sont pas visibles.
- Les secrets `.env.local` et `.env.test` sont suivis Git dans l'etat observe ; ils doivent etre retires et les secrets rotes.

### 7.3 RGPD et donnees sensibles

Donnees sensibles traitees :

- emails et telephones clients ;
- email beneficiaire ;
- messages support ;
- IP et user-agent ;
- corps HTML/textes emails ;
- contenus SMS ;
- IBAN et titulaires ;
- documents d'achat, snapshots de facturation et documents prives rattaches ;
- tokens et traces d'audit.

Exigences techniques :

- minimiser les donnees exposees par API et back-office ;
- masquer emails, telephones et IBAN quand l'affichage complet n'est pas necessaire ;
- definir retention et purge pour outbox, support, audit, activites, sessions et documents ;
- ne jamais logger les tokens bruts ;
- separer les usages publics anonymises des donnees nominatives ;
- servir les documents prives via backend uniquement ;
- verifier le rattachement `COMMERCANT` avant tout telechargement depuis l'application commercant.

## 8. Configuration

Fichier : `app/config.py`.

Familles de variables :

- Runtime : `LOCALEO_ENV`, `LOCALEO_DATABASE_URL`, `DATABASE_URL`.
- QR : `LOCALEO_QR_COFFRET_KEY_ID`, `LOCALEO_QR_COFFRET_SECRET`, `LOCALEO_QR_COFFRET_KEYRING`.
- Stripe : `LOCALEO_STRIPE_SECRET_KEY`, `LOCALEO_STRIPE_WEBHOOK_SECRET`.
- Stripe Connect EPIC 39 : `LOCALEO_FEATURE_STRIPE_CONNECT_ENABLED`,
  `LOCALEO_STRIPE_SECRET_KEY`, `LOCALEO_STRIPE_WEBHOOK_SECRET`,
  `LOCALEO_STRIPE_CONNECT_WEBHOOK_SECRET`,
  `LOCALEO_STRIPE_ONBOARDING_RETURN_URL`,
  `LOCALEO_STRIPE_ONBOARDING_REFRESH_URL`.
- Les URLs `LOCALEO_STRIPE_ONBOARDING_RETURN_URL` et
  `LOCALEO_STRIPE_ONBOARDING_REFRESH_URL` pointent vers l'application
  commercant, par exemple
  `https://commercants.localeo.fr/stripe-connect/onboarding/return` et
  `https://commercants.localeo.fr/stripe-connect/onboarding/refresh`.
  L'application commercant appelle ensuite le backend pour synchroniser le
  compte ou regenerer un `AccountLink`.
- Front : URLs de success, cancel, commande, activation, consultation, feedback, liens courts.
- Workflows : TTL tokens, sessions, transactions, relances, feedbacks, purge.
- Auth : bcrypt rounds, longueur mot de passe, rate limits.
- Admin : username, password, session secret, defaults insecure.
- Brevo : email/SMS API keys, sender.
- Gestion documentaire : provider stockage, endpoint S3, region, bucket, prefixe, secrets S3, taille maximale upload, MIME autorises.
- Animation locale et Localeo Live : `LOCALEO_ANIMATION_PUBLIC_URL_TEMPLATE`, `LOCALEO_ANIMATION_PARTICIPANT_URL_TEMPLATE`, `LOCALEO_ANIMATION_PORTAIL_URL`, `LOCALEO_FRONT_COMMERCANT_ANIMATION_INVITATION_URL_TEMPLATE`, `LOCALEO_ANIMATION_MERCHANT_CONSENT_ENFORCED`, `LOCALEO_FRONT_LIVE_URL`, `LOCALEO_FRONT_LIVE_AJOUTER_COFFRET_URL_TEMPLATE`, `LOCALEO_FRONT_LIVE_AJOUTER_ANIMATION_URL_TEMPLATE`, `LOCALEO_FRONT_LIVE_ANIMATION_URL_TEMPLATE`, `LOCALEO_ANIMATION_OPERATION_MAX_ATTEMPTS`, `LOCALEO_ANIMATION_OPERATION_RETENTION_DAYS`, `LOCALEO_ANIMATION_SESSION_TTL_SECONDS`.
- Accueil geolocalise Epic 52 : `LOCALEO_VILLES_PROCHES_RAYON_KM` (defaut `30`), `LOCALEO_VILLES_PROCHES_MAX_RAYON_KM` (defaut `100`), `LOCALEO_VILLES_PROCHES_MAX_RESULTATS` (defaut `50`) et `LOCALEO_GEO_API_GOUV_COMMUNES_URL` (defaut `https://geo.api.gouv.fr/communes`).
- CORS : origins, regex, credentials, methods, headers.
- Societe : nom, adresse, mentions legales.

## 9. Observabilite

Composants :

- `logging_config.py` : configuration loggers.
- `observability_http.py` : adaptateur HTTP, correlation, `User-Agent` assaini
  et duree.
- `observability.py` : facade unique, contexte, redaction, format texte/JSON,
  emission, logs metier, regles, invariants et timing.
- `observability_instrumentation.py` : instrumentation automatique des methodes
  `execute` des Use Cases.
- `audit.py` et `service_audit.py` : evenements persistants.

Le domaine utilise explicitement `log_decision`, `log_business_rule` et
`log_invariant` aux points ou une decision importante est calculee, une
transition d'etat est appliquee ou un invariant peut rejeter l'operation. Il
n'existe pas d'instrumentation automatique des methodes du domaine.

Exigences :

- conserver `X-Correlation-ID` et son alias `X-Request-ID` sur chaque reponse ;
- exposer `correlationId` et l'alias `request_id` dans chaque erreur JSON 4xx/5xx ;
- journaliser les actions sensibles ;
- eviter les donnees personnelles et secrets dans les logs ;
- journaliser les entrees/sorties en `INFO` et reserver les parametres filtres au `DEBUG` ;
- distinguer les rejets metier (`WARNING`) des erreurs techniques (`ERROR`) ;
- tracer la duree et signaler les appels lents ;
- utiliser `evenements_audit` pour les investigations metier.
- historiser les executions batch dans `executions_batch` avec compteurs, statut, duree et correlation id.
- bloquer les doubles executions d'un meme batch via `verrous_batch`.

### 9.1 Supervision batchs

- `GET /protected/maintenance/batchs` expose l'inventaire operationnel.
- `GET /protected/maintenance/batchs/executions` expose l'historique d'execution.
- `GET /protected/maintenance/batchs/health` expose un statut `OK`, `WARNING` ou `CRITICAL`.
- `POST /protected/maintenance/activites-locales/purger` expose la purge des activites locales en mode batch automatise.

## 10. Back-office

SQLAdmin expose :

- vues modeles pour les ORM principaux ;
- vues custom : dashboard operationnel, batchs exploitation, timeline support ;
- routes internes HTML pour rentabilite, QR, mode secours, reversements, documentation ;
- actions de moderation, relance, regeneration, purge, export et cloture.

Routes documentation :

- `/internal/docs/backoffice` redirige vers le viewer Markdown de la base de
  connaissance `docs/ops` : exploitation, technique, formation et recette.
- `/internal/docs/knowledge/{document_path}` publie un document Markdown situé
  sous `docs/ops`, sans autoriser de sortie de ce répertoire.
- `/internal/docs/procedures` génère le catalogue des procédures depuis
  `docs/ops/technique/` et `docs/ops/exploitation/`.
- `/internal/docs/reversements` lit [docs/ops/exploitation/piloter-reversements-stripe-connect.md](../../exploitation/exploitation/piloter-reversements-stripe-connect.md).

## 11. Integrations

### Stripe

- Checkout session.
- Webhook signe.
- Reconciliation manuelle possible depuis back-office.

### Brevo email

- Envoi transactionnel.
- Statut provider.
- Mode dev configurable.

### Brevo SMS

- Envoi transactionnel.
- Statut provider.
- Mode dev configurable.

### Frontends

- Marketplace catalogue et achat.
- Retour paiement.
- Gestion achat pro.
- Activation beneficiaire.
- Consultation coffret.
- Espace commercant.
- Feedback prestation.

## 12. Tests techniques indispensables

- Import et startup config par environnement.
- Routes publiques/protegees : auth et authz.
- IDOR achats, instances, prestations et commercants.
- Webhook Stripe invalide, duplique, incomplet.
- Login commercant : rate limit, lock, session expiry.
- Tokens : expiration, revocation, mauvais token.
- Upload image : type, taille, auth.
- CSRF back-office.
- Redaction logs.
- Batchs email/SMS : reservation, retry, statut.
- Reversements : idempotence de lot, export, cloture.
- RGPD : purge sessions, activites, outbox et masquage PII.

## 13. Limites connues

- `create_all` et scripts SQL cohabitent.
- Plusieurs use cases retournent des dictionnaires de presentation.
- Le back-office est couple aux ORM.
- Les routes publiques d'ecriture doivent etre durcies.
- La retention RGPD n'est pas completement formalisee dans le code.
- Les tokens front en query string sont un risque de fuite.

## 14. Commandes de lots Localeo Animation (Epic 46)

- `CommandeAchat` est la racine financière d'une configuration de lots et possède plusieurs `LigneCommandeAchat` immuables.
- Un seul `Paiement` référence soit un `AchatCoffret` classique, soit une `CommandeAchat` ; la contrainte SQL `ck_paiements_racine_unique` l'impose.
- Après le webhook Stripe, chaque ligne matérialise un `AchatCoffret` professionnel enfant et exactement `quantite` instances `EN_ATTENTE_ACTIVATION`.
- Les reversements retrouvent la charge de commande depuis l'achat enfant via `commande_achat_id` ; aucune transaction Stripe n'est dupliquée.
- La sélection d'une instance lors de l'envoi d'un gain utilise `FOR UPDATE SKIP LOCKED` et la FK unique `animation_gains.coffret_instance_id`.
- Le contrat protégé est exposé sous `/protected/animation-locale/animations/{animation_id}/commande-lots` et la réparation locale sous `/internal/animation-locale/commandes-lots/reconcilier`.
- La migration de référence est `sql/v173_epic46_commandes_lots_animation.sql`.

## Correctifs Marketplace 2026-09-06

Voir [contrat des correctifs MARKET](../../specifications/securisation-production/corrections-marketplace-2026-09-06.md).
