# Epic 40 - Organisation du backend par domaines fonctionnels

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : reorganiser les objets du backend Localeo par domaines fonctionnels visibles dans `app/domaine` et `app/application`, afin de rendre le code plus lisible, maintenable et evolutif.
- Decision architecture : la couche infrastructure reste transverse et ne doit pas etre dupliquee par domaine fonctionnel.
- Decision technique : le decoupage cible doit etre visible dans les packages domaine et application, pas seulement dans la documentation.
- Decision UX back-office : l'organisation du menu back-office doit s'aligner sur les memes domaines fonctionnels pour que l'interface d'administration reflete le modele mental cible.
- Decision API : les chemins d'API canoniques doivent porter le domaine fonctionnel dans le path de chaque endpoint.
- Decision contrat API : le domaine fonctionnel doit aussi apparaitre comme tag OpenAPI sur chaque operation exposee.
- Decision produit : les paths API peuvent evoluer pour porter le domaine fonctionnel, mais les comportements metier, payloads, schemas API et schemas SQL ne doivent pas changer pendant cette reorganisation.

## Documents d'architecture

- [Architecture applicative EPIC 40 - Domaines fonctionnels backend](../../architecture/backend/epics/epic-40-domaines-fonctionnels-architecture.md)

## Probleme

L'Epic 24 a deja clarifie la couche domaine par nature technique : `entities`, `value_objects`, `repositories`, `exceptions`. Cette structure a rendu les objets plus visibles individuellement, mais elle ne raconte pas encore les grands domaines fonctionnels Localeo.

Aujourd'hui, un developpeur doit connaitre le produit pour reconstituer mentalement quels objets participent a :
- l'exploitation ;
- le support ;
- le referencement ;
- la commercialisation ;
- les achats ;
- les reversements ;
- les profils commercants ;
- la gestion documentaire ou media.

La croissance du backend rend ce cout de lecture plus important. Les use cases applicatifs sont aussi regroupes dans un package plat, ce qui rend les workflows transverses difficiles a reperer.

Le back-office presente le meme enjeu cote exploitation : son menu contient deja des categories proches des domaines (`Support`, `Gestion reversement`, `Gestion referencement`) mais aussi des categories transverses comme `Pilotage`. Sans alignement, le code peut etre reorganise par domaine tandis que les operateurs continuent a naviguer dans une structure differente.

Les APIs exposent aussi un enjeu de lisibilite. Les routes actuelles sont principalement structurees par surface (`/public`, `/protected`, `/internal`, `/admin/api`) puis par ressource (`/coffrets`, `/achats`, `/reversements`, etc.). Pour rendre le decoupage fonctionnel explicite de bout en bout, le path canonique doit devenir : surface + domaine fonctionnel + ressource.

## Analyse critique du decoupage propose

Le decoupage propose couvre l'essentiel du backend actuel, mais il faut eviter deux pieges :

- `exploitation` risque de devenir un domaine fourre-tout si on y place tous les objets techniques ou transverses ;
- certains objets sont mieux isoles dans des domaines dedies pour garder une responsabilite claire.

### Points solides

- Separer `commercialisation`, `gestion_achats` et `gestion_reversement` est sain : ces domaines n'ont pas les memes invariants.
- Garder `profils` a part est pertinent : le profil commercant a son propre cycle de publication, distinct de l'entite `Commercant`.
- Sortir `support` de l'exploitation est pertinent : communication, contacts, timeline et notes servent le traitement client/partenaire.
- Garder l'infrastructure transverse est le bon choix : SQLAlchemy, stockage, email, SMS, paiement externe et admin ne doivent pas etre repliques par domaine.

### Ajustements recommandes

- Ajouter un domaine `identite_acces` pour les sessions, tokens, authentification, rate limit et acces commercants. Les ranger dans `exploitation` ou `referencement` melange securite, exploitation et catalogue.
- Ajouter un domaine `documentaire` distinct de `dam`. Le DAM porte images/media assets ; la gestion documentaire porte documents publics, contrats, documents clients et documents d'achat.
- Traiter `emails` et `sms` comme `communication_sortante` dans `exploitation` seulement si on les considere comme une outbox operationnelle. Les messages de support restent dans `support`.
- Classer `types_coffrets` dans `commercialisation`, car le type de coffret structure l'offre vendable.
- Garder `api_key` dans `identite_acces` ou `exploitation_securite`, pas dans l'exploitation operationnelle courante.
- Ne pas mettre les `CoffretInstance` dans `commercialisation` : elles appartiennent au cycle d'achat et d'execution d'un achat.

## Domaines fonctionnels cibles

### `exploitation`

Responsabilite : piloter les operations internes et les evenements techniques/metier transverses.

Objets actuels proposes :
- `LienCourt`
- `EvenementAudit`
- `EmailSortant`
- `SmsSortant`
- `ValidationPrestation`
- `ValidationSecours`
- `TransactionValidation`
- activites locales
- batchs
- PWA exploitation / Localeo Control
- statistiques operationnelles
- feedback prestation comme signal operationnel post-prestation

Reserve : ne pas y ranger l'authentification ni les objets purement catalogue.

### `support`

Responsabilite : traiter les demandes clients/commercants et les interactions support.

Objets actuels proposes :
- `MessageContact`
- `MotifContact`
- communications libres back-office
- notes internes commercants
- timeline support
- vision 360 client cote support
- reponses aux messages consommateur/commercant
- demandes de facturation si elles deviennent un objet metier dedie

### `referencement`

Responsabilite : administrer les partenaires et taxonomies de base avant exposition commerciale.

Objets actuels proposes :
- `Ville`
- `TypeCommercant`
- `Commercant`
- gouvernance catalogue
- referencement commercant
- listes et details commercants/villes/types commercants

### `identite_acces`

Responsabilite : gerer l'identite, les acces, tokens, sessions et controles d'authentification.

Objets actuels proposes :
- `TokenAccesCommercant`
- `SessionCommercant`
- `RateLimitAuthentification`
- `ApiKey`
- `IdentifiantCommercant`
- initialisation acces commercant
- authentification commercant
- reinitialisation mot de passe
- mise a jour mot de passe
- verification/revocation de sessions
- mecanique de generation, validation, expiration et revocation des tokens de consultation achat/coffret instance

Raison du domaine : ces objets ont des invariants de securite et de cycle de vie differents du referencement.

### `dam`

Responsabilite : gerer les assets media et images.

Objets actuels proposes :
- images
- media assets
- selection d'image
- stockage/metadata media si un objet domaine est introduit

Reserve : ne pas y ranger les documents juridiques ou documents d'achat.

### `documentaire`

Responsabilite : gerer les documents publics, prives, contractuels et rattachements documentaires transverses.

Objets actuels proposes :
- gestion documentaire
- documents publics
- documents commercants
- documents clients
- contrats/avenants/mandats
- rattachements documentaires

Lien avec `gestion_achats` :
- les documents d'achat peuvent etre produits par `gestion_achats`, mais leur referentiel transverse appartient a `documentaire`.

### `profils`

Responsabilite : gerer les profils commercants publies et leurs versions.

Objets actuels proposes :
- `ProfilCommercant`
- consultation profil commercant
- mise a jour contact commercant si rattachee au profil public
- mise a jour contenu prestation par commercant si le contenu sert la publication profil/prestation

Point a surveiller :
- le profil ne doit pas devenir un doublon de `Commercant`; il porte la publication et le contenu expose.

### `commercialisation`

Responsabilite : construire et exposer l'offre vendable.

Objets actuels proposes :
- `Coffret`
- `PrestationCoffret`
- `TypeCoffretConfig`
- recherche marketplace
- coffrets du moment
- ajout de prestation a un coffret
- consultation detail coffret/prestation
- rentabilite coffret si elle sert la construction d'offre

Reserve :
- les achats reels et instances achetees restent dans `gestion_achats`.

### `gestion_achats`

Responsabilite : gerer le cycle de vie d'une commande/achat client apres intention d'achat.

Objets actuels proposes :
- `AchatCoffret`
- `Paiement`
- `PaiementEvent`
- `CoffretInstance`
- `StatutPrestationCoffretInstance`
- remboursement achat
- activation coffret instance
- consultation achat/coffret instance
- expiration coffrets instances
- documents d'achat comme production documentaire
- reconciliation achat non confirme
- renvoi emails lies a l'achat
- use cases de consultation post-achat par token, en consommant la mecanique token portee par `identite_acces`

### `gestion_reversement`

Responsabilite : gerer les obligations et executions de reversement commercant.

Objets actuels proposes :
- `CompteBancaireCommercant`
- `CompteReversementCommercant`
- `MouvementReversement`
- `Reversement`
- `LigneReversement`
- `PaiementReversement`
- `LotPaiementReversement` decommissionne
- calcul reversement coffret
- campagnes Stripe Connect
- synchronisation transfer/webhook Stripe
- vision 360 reversements et paiements
- projections Stripe Connect de transfer portees par le backend

### `animation_locale`

Responsabilite : porter l'enveloppe du futur domaine de plateforme d'animation locale, en coherence avec l'Epic 41.

Objets actuels proposes pour l'Epic 40 :
- package domaine cible ;
- package application cible ;
- reservation du segment API `/animation-locale` ;
- tag OpenAPI `Animation locale`.

Reserve :
- l'implementation fonctionnelle du moteur d'animation, du Passeport commercant, des participants, validations, tirages et bilans reste portee par l'Epic 41.

## Organisation cible du menu back-office

Le menu back-office doit reprendre les domaines fonctionnels cibles afin que le vocabulaire de navigation soit coherent avec le code.

### Categories recommandees

- `Exploitation`
  - dashboard operationnel ;
  - Localeo Control ;
  - batchs exploitation ;
  - validations et validations de secours ;
  - transactions de validation ;
  - liens courts ;
  - emails, SMS et WebPush sortants ;
  - activites locales ;
  - feedbacks prestation ;
  - evenements d'audit.
- `Support`
  - timeline support ;
  - vision 360 client ;
  - messages de contact ;
  - motifs de contact ;
  - communication libre ;
  - notes internes ;
  - demandes de facturation.
- `Referencement`
  - villes ;
  - types commercants ;
  - commercants.
- `Identite acces`
  - sessions commercants ;
  - identifiants commercants ;
  - tokens et acces commercants ;
  - API keys ;
  - rate limit authentification ;
  - actions d'initialisation ou reinitialisation d'acces.
- `DAM`
  - media assets ;
  - images et selection d'image.
- `Documentaire`
  - gestion documentaire ;
  - documents ;
  - rattachements documentaires.
- `Profils`
  - profils commercants ;
  - versions de profils ;
  - demandes ou validations de publication profil.
- `Commercialisation`
  - coffrets ;
  - prestations de coffrets ;
  - versions de prestations ;
  - types coffrets ;
  - vision 360 coffret si elle sert principalement la gestion de l'offre.
- `Gestion achats`
  - achats coffrets ;
  - coffrets instances ;
  - paiements clients ;
  - remboursements ;
  - documents d'achat ;
  - statuts de prestations d'instances.
- `Gestion reversement`
  - comptes bancaires commercants ;
  - comptes de reversement ;
  - mouvements de reversement ;
  - reversements ;
  - lignes de reversement ;
  - lots de paiement ;
  - paiements de reversement ;
  - vision 360 reversements.
- `Animation locale`
  - enveloppe du domaine animation locale ;
  - futures animations, participants, validations et bilans ;
  - entree cible quand l'Epic 41 sera engagee.

### Exceptions assumees

- Les vues d'aide operationnelle sont rattachees a `Support` car elles servent les operateurs back-office.
- Une entree de pilotage globale peut rester visible si elle sert de tableau de bord transverse, mais les vues specialisees doivent etre rattachees a leur domaine principal.
- Les vues SQLAdmin generiques restent techniquement implementees dans `infrastructure/admin`, mais leur `category` doit utiliser le vocabulaire fonctionnel cible.
- Les libelles du menu doivent eviter les prefixes heterogenes comme `Gestion referencement`, `Gestion Achats / Paiements` et `Pilotage` quand un domaine clair existe.

## Organisation cible des APIs

Les endpoints canoniques doivent inclure le domaine fonctionnel dans le path. La convention recommandee est :

```text
/{surface}/{domaine}/{ressource}
```

Surfaces conservees :
- `/public` pour les APIs exposees au site et aux parcours publics ;
- `/protected` pour les APIs authentifiees cote commercant/client/partenaire selon les mecanismes existants ;
- `/internal` pour les routes internes back-office et exploitation ;
- `/admin/api` pour les APIs back-office administratives deja rattachees a l'admin.

### Exemples de mapping cible

- `/public/villes` -> `/public/referencement/villes`
- `/public/types-commercants` -> `/public/referencement/types-commercants`
- `/public/types-coffrets` -> `/public/commercialisation/types-coffrets`
- `/public/coffrets` -> `/public/commercialisation/coffrets`
- `/public/recherche` -> `/public/commercialisation/recherche`
- `/public/commercants/{id}/page` -> `/public/profils/commercants/{id}/page`
- `/public/images` -> `/public/dam/images`
- `/public/documents` -> `/public/documentaire/documents`
- `/public/paiements` -> `/public/gestion-achats/paiements`
- `/public/qr` -> `/public/gestion-achats/qrcode` pour la consultation/affichage technique d'un QR token
- `/protected/validation` -> `/protected/exploitation/validation` pour les transactions de validation ouvertes apres scan du QR coffret
- `/public/contacts` -> `/public/support/contacts`
- `/public/feedbacks-prestation` -> `/public/exploitation/feedbacks-prestation`
- `/public/activites-locales` -> `/public/exploitation/activites-locales`
- `/protected/achats` -> `/protected/gestion-achats/achats`
- `/protected/coffrets-instances` -> `/protected/gestion-achats/coffrets-instances`
- `/protected/reversements` -> `/protected/gestion-reversement/reversements`
- `/protected/commercants` -> `/protected/referencement/commercants` pour les donnees referentiel, ou `/protected/profils/commercants` pour les contenus de profil
- `/protected/emails` -> `/protected/exploitation/emails`
- `/protected/sms` -> `/protected/exploitation/sms`
- `/protected/webpush` -> `/protected/exploitation/webpush`
- `/protected/maintenance` -> `/protected/exploitation/maintenance`
- `/admin/api/documents` -> `/admin/api/documentaire/documents`
- `/admin/api/profils-commercants` -> `/admin/api/profils/profils-commercants`
- `/internal/reversements/...` -> `/internal/gestion-reversement/reversements/...`
- `/internal/messages-contact/...` -> `/internal/support/messages-contact/...`
- `/internal/communications-libres` -> `/internal/support/communications-libres`
- `/internal/media-assets` -> `/internal/dam/media-assets`
- `/internal/profils-commercants/...` -> `/internal/profils/profils-commercants/...`
- `/internal/pwa-exploitation/...` -> `/internal/exploitation/pwa/...`

### Regles de migration API

- La route avec domaine devient la route canonique.
- Les anciens paths ne sont pas conserves comme aliases de compatibilite.
- La migration des consommateurs doit etre coordonnee dans la meme livraison que les nouveaux paths.
- Les tags OpenAPI doivent reprendre le domaine fonctionnel.
- Les noms de routers FastAPI doivent suivre la convention du domaine.
- Les tests doivent verifier les nouveaux paths canoniques.
- Les routes purement techniques comme `/sante`, `/docs`, `/openapi.json`, `/email-assets/localeo.png` peuvent rester hors domaine si elles ne portent pas un workflow metier.

### Contrats OpenAPI

Chaque operation exposee dans le contrat OpenAPI doit porter le domaine fonctionnel comme tag principal.

Le contrat global `/openapi.json` reste disponible pour les usages techniques transverses. En complement, trois contrats filtres par surface doivent etre exposes pour faciliter l'integration et limiter le bruit documentaire :

- `/openapi/public.json` et `/docs/public` pour les endpoints `/public/*` ;
- `/openapi/protected.json` et `/docs/protected` pour les endpoints `/protected/*` ;
- `/openapi/internal.json` et `/docs/internal` pour les endpoints `/internal/*` et `/admin/api/*`.

La separation public/protected/internal est donc portee par le contrat expose, tandis que le tag principal des operations reste le domaine fonctionnel.

Tags de domaine cibles :
- `Exploitation`
- `Support`
- `Referencement`
- `Identite acces`
- `DAM`
- `Documentaire`
- `Profils`
- `Commercialisation`
- `Gestion achats`
- `Gestion reversement`
- `Animation locale`

Regles :
- le premier tag de chaque operation doit etre le domaine fonctionnel ;
- un tag secondaire par ressource peut etre ajoute si necessaire, par exemple `Coffrets`, `Paiements`, `Messages contact`, mais il ne remplace pas le tag de domaine ;
- les surfaces API sont exposees par contrats dedies plutot que par un tag principal `Public`, `Protected` ou `Internal` ;
- aucun tag d'alias de compatibilite n'est attendu car les anciens paths ne sont pas conserves ;
- les tags techniques existants comme `Admin internal`, `Coffrets`, `Paiements`, `Documents public` doivent etre remplaces ou completes par le tag de domaine ;
- les tags hors domaine sont autorises uniquement pour les routes techniques non metier comme `Systeme`, sante, documentation ou assets techniques.

Exemples :
- `/public/commercialisation/coffrets` -> tag principal `Commercialisation` ;
- `/protected/gestion-achats/achats/{achat_id}` -> tag principal `Gestion achats` ;
- `/protected/gestion-reversement/reversements` -> tag principal `Gestion reversement` ;
- `/admin/api/documentaire/documents` -> tag principal `Documentaire` ;
- `/internal/support/messages-contact/{thread_id}/repondre` -> tag principal `Support`.

## Couverture des objets actuels

### Entites domaine

- `AchatCoffret` -> `gestion_achats`
- `ApiKey` -> `identite_acces`
- `Coffret` -> `commercialisation`
- `CoffretInstance` -> `gestion_achats`
- `Commercant` -> `referencement`
- `CompteBancaireCommercant` -> `gestion_reversement`
- `CompteReversementCommercant` -> `gestion_reversement`
- `EmailSortant` -> `exploitation`
- `EvenementAudit` -> `exploitation`
- `IdentifiantCommercant` -> `identite_acces`
- `LienCourt` -> `exploitation`
- `LigneReversement` -> `gestion_reversement`
- `LotPaiementReversement` -> `gestion_reversement`
- `MessageContact` -> `support`
- `MotifContact` -> `support`
- `MouvementReversement` -> `gestion_reversement`
- `Paiement` -> `gestion_achats`
- `PaiementReversement` -> `gestion_reversement`
- `PrestationCoffret` -> `commercialisation`
- `ProfilCommercant` -> `profils`
- `RateLimitAuthentification` -> `identite_acces`
- `Reversement` -> `gestion_reversement`
- `SessionCommercant` -> `identite_acces`
- `SmsSortant` -> `exploitation`
- `StatutPrestationCoffretInstance` -> `gestion_achats`
- `TokenAccesCommercant` -> `identite_acces`
- `TransactionValidation` -> `exploitation`
- `TypeCoffretConfig` -> `commercialisation`
- `TypeCommercant` -> `referencement`
- `ValidationPrestation` -> `exploitation`
- `ValidationSecours` -> `exploitation`
- `Ville` -> `referencement`

### Value objects

- `CodePostal` -> value object partage, utilise principalement par `referencement`
- `Email` -> value object partage
- `Money` -> value object partage finance
- `MontantEuroCentimes` -> value object partage finance
- `NumeroTelephone` -> value object partage
- `QrToken` -> value object partage entre `gestion_achats` et `exploitation`
- `VersionCarteCommercant` -> `identite_acces` ou historique de carte/acces commercant

Decision recommandee : conserver un package `shared/value_objects` ou `common/value_objects` plutot que dupliquer ces objets par domaine.

## Structure cible indicative

```text
app/domaine/
  exploitation/
    entities/
    repositories/
    exceptions/
  support/
    entities/
    repositories/
    exceptions/
  referencement/
    entities/
    repositories/
    exceptions/
  identite_acces/
    entities/
    repositories/
    exceptions/
  dam/
    entities/
    repositories/
    exceptions/
  documentaire/
    entities/
    repositories/
    exceptions/
  profils/
    entities/
    repositories/
    exceptions/
  commercialisation/
    entities/
    repositories/
    exceptions/
  gestion_achats/
    entities/
    repositories/
    exceptions/
  gestion_reversement/
    entities/
    repositories/
    exceptions/
  animation_locale/
    entities/
    repositories/
    exceptions/
  shared/
    value_objects/
    exceptions/

app/application/
  exploitation/
    use_cases/
    services/
  support/
    use_cases/
    services/
  referencement/
    use_cases/
    services/
  identite_acces/
    use_cases/
    services/
  dam/
    use_cases/
    services/
  documentaire/
    use_cases/
    services/
  profils/
    use_cases/
    services/
  commercialisation/
    use_cases/
    services/
  gestion_achats/
    use_cases/
    services/
  gestion_reversement/
    use_cases/
    services/
  animation_locale/
    use_cases/
    services/
```

## Regles d'architecture

- `app/infrastructure` reste transverse.
- Les adapters Stripe, email, SMS, stockage, SQLAlchemy et admin restent dans `infrastructure`.
- Les repositories domaine restent des ports dans leur domaine fonctionnel.
- Les implementations SQLAlchemy restent regroupees dans l'infrastructure.
- Les domaines fonctionnels peuvent importer des value objects partages.
- Les imports entre domaines doivent etre explicites et limites.
- Les workflows applicatifs transverses doivent vivre dans le domaine qui porte la decision principale.
- Aucun domaine ne doit importer FastAPI, SQLAlchemy ou un provider externe.
- Les APIs restent separees par surface publique/protegee/interne/admin, mais le segment suivant doit porter le domaine fonctionnel canonique.

## Perimetre MVP

- Cartographier tous les objets domaine, repositories, services et use cases actuels.
- Valider la liste finale des domaines fonctionnels.
- Deplacer `app/domaine` vers une structure par domaine fonctionnel.
- Deplacer `app/application/use_cases` vers une structure par domaine fonctionnel.
- Deplacer les services applicatifs vers les domaines fonctionnels correspondants.
- Aligner les categories du menu back-office SQLAdmin sur les domaines fonctionnels cibles.
- Reclasser les vues back-office existantes dans les bonnes categories sans changer leurs routes ni leurs permissions.
- Definir les conventions de paths API par surface et domaine fonctionnel.
- Migrer les routers API vers des paths canoniques contenant le domaine fonctionnel.
- Supprimer les anciens paths dans la meme livraison que la migration vers les paths canoniques.
- Mettre a jour les consommateurs frontend/API dans la meme livraison.
- Conserver `app/infrastructure` transverse.
- Mettre a jour tous les imports.
- Mettre a jour `bootstrap`, Unit of Work et wiring applicatif si necessaire.
- Ajouter des tests d'import et de compilation.
- Documenter les regles de dependance inter-domaines.

## Hors perimetre MVP

- Modifier les tables SQL.
- Modifier les contrats fonctionnels des APIs.
- Conserver durablement les anciens paths API en parallele des nouveaux.
- Refaire les aggregates metier en profondeur.
- Changer le comportement des use cases.
- Remplacer SQLAdmin ou restructurer l'infrastructure.
- Reconcevoir visuellement toute l'interface back-office.
- Introduire un bus d'evenements ou un framework de modules.

## User Stories

1. `PRD-319` En tant que developpeur, je veux une cartographie des objets backend par domaine fonctionnel afin de comprendre rapidement ou se trouve chaque responsabilite.
   - Statut : `A faire`
   - Resultat attendu : chaque entite, repository, service applicatif et use case a un domaine cible.
   - Resultat attendu : les objets ambigus sont listes avec une decision explicite.

2. `PRD-320` En tant qu'architecte, je veux valider le decoupage cible afin d'eviter qu'`exploitation` devienne un domaine fourre-tout.
   - Statut : `A faire`
   - Resultat attendu : les domaines `identite_acces`, `documentaire` et `animation_locale` sont retenus dans la cartographie cible.
   - Resultat attendu : `TypeCoffretConfig`, `IdentifiantCommercant` et tokens de consultation ont une affectation actee.
   - Resultat attendu : le rattachement du QR coffret et du feedback prestation est acte avant implementation.

3. `PRD-321` En tant que developpeur, je veux que `app/domaine` soit organise par domaines fonctionnels afin de lire le modele metier par contexte.
   - Statut : `A faire`
   - Resultat attendu : les entites et repositories sont deplaces dans les packages fonctionnels cibles.
   - Resultat attendu : les value objects partages restent dans un espace commun.

4. `PRD-322` En tant que developpeur, je veux que les use cases applicatifs soient rassembles par domaine afin de retrouver rapidement les workflows.
   - Statut : `A faire`
   - Resultat attendu : `app/application/use_cases` n'est plus un package plat.
   - Resultat attendu : chaque use case est deplace dans le domaine qui porte la decision metier principale.

5. `PRD-323` En tant que developpeur, je veux que les services applicatifs soient rattaches a leur domaine fonctionnel afin d'eviter les services transverses mal delimites.
   - Statut : `A faire`
   - Resultat attendu : les services de session, audit, documents, profils, activites locales, SMS, email et batchs ont un domaine cible.

6. `PRD-324` En tant que mainteneur, je veux conserver l'infrastructure transverse afin de ne pas dupliquer les adapters techniques par domaine.
   - Statut : `A faire`
   - Resultat attendu : `app/infrastructure` reste le point d'integration SQLAlchemy, providers externes, stockage, admin, email, SMS et paiement.

7. `PRD-325` En tant que mainteneur, je veux des regles d'import inter-domaines afin d'eviter les dependances circulaires.
   - Statut : `A faire`
   - Resultat attendu : les imports autorises et interdits sont documentes.
   - Resultat attendu : les dependances transverses passent par `shared` ou par des ports explicites.

8. `PRD-326` En tant que developpeur, je veux migrer les imports sans facade durable afin de ne pas conserver deux organisations concurrentes.
   - Statut : `A faire`
   - Resultat attendu : les anciens imports plats sont remplaces.
   - Resultat attendu : aucune facade de compatibilite durable n'est ajoutee.

9. `PRD-327` En tant que responsable qualite, je veux des tests de non-regression sur la reorganisation afin de verifier qu'aucun comportement ne change.
   - Statut : `A faire`
   - Resultat attendu : compilation Python, tests d'import et tests applicatifs critiques passent.
   - Resultat attendu : aucun comportement public ni payload API ne change hors migration explicite des paths.

10. `PRD-328` En tant que responsable technique, je veux mettre a jour la documentation architecture afin que le decoupage soit compris et maintenu.
    - Statut : `A faire`
    - Resultat attendu : la documentation explique les domaines, leurs responsabilites et les regles de dependance.

11. `PRD-329` En tant que mainteneur, je veux une strategie de migration one-shot coordonnee afin de basculer directement vers l'organisation cible.
    - Statut : `A faire`
    - Resultat attendu : le plan de bascule one-shot est documente par domaine, dependance et consommateur impacte.
    - Resultat attendu : la livraison cible laisse le code compilable, les consommateurs mis a jour et aucune double source de verite durable.

12. `PRD-330` En tant qu'operateur back-office, je veux que le menu d'administration soit organise selon les domaines fonctionnels afin de retrouver les ecrans avec le meme vocabulaire que le backend.
    - Statut : `A faire`
    - Resultat attendu : les categories SQLAdmin reprennent les domaines cibles.
    - Resultat attendu : les vues existantes sont reclassees sans changer leurs routes.
    - Resultat attendu : les exceptions transverses comme aide/documentation ou tableau de bord global sont explicitement justifiees.

13. `PRD-331` En tant qu'integrateur frontend/API, je veux que le domaine fonctionnel soit visible dans le path de chaque endpoint afin de comprendre immediatement le contexte metier de l'API appelee.
    - Statut : `A faire`
    - Resultat attendu : les routes canoniques suivent la convention `/{surface}/{domaine}/{ressource}`.
    - Resultat attendu : les surfaces `/public`, `/protected`, `/internal` et `/admin/api` sont conservees.
    - Resultat attendu : les routes techniques non metier sont explicitement exclues ou documentees.

14. `PRD-332` En tant que mainteneur, je veux migrer directement les anciens paths vers les paths canoniques afin de ne pas conserver deux contrats API concurrents.
    - Statut : `A faire`
    - Resultat attendu : les anciens paths ne sont pas conserves comme aliases.
    - Resultat attendu : les tests couvrent les nouveaux paths canoniques.
    - Resultat attendu : les consommateurs frontend/API sont mis a jour dans la meme livraison.

15. `PRD-333` En tant qu'integrateur API, je veux que chaque operation du contrat OpenAPI porte le domaine fonctionnel comme tag afin de filtrer et lire la documentation selon le meme decoupage que le backend.
    - Statut : `A faire`
    - Resultat attendu : le premier tag OpenAPI de chaque operation metier est le domaine fonctionnel.
    - Resultat attendu : les tags de ressource sont secondaires et ne remplacent pas le domaine.
    - Resultat attendu : les contrats `/openapi/public.json`, `/openapi/protected.json` et `/openapi/internal.json` exposent chacun uniquement leur surface API.
    - Resultat attendu : les documentations `/docs/public`, `/docs/protected` et `/docs/internal` pointent vers le contrat filtre correspondant.
    - Resultat attendu : les routes techniques non metier explicitent pourquoi elles ne portent pas de domaine.

## Ordre recommande de livraison

1. `PRD-319`
2. `PRD-320`
3. `PRD-325`
4. `PRD-321`
5. `PRD-322`
6. `PRD-323`
7. `PRD-324`
8. `PRD-326`
9. `PRD-327`
10. `PRD-328`
11. `PRD-329`
12. `PRD-330`
13. `PRD-331`
14. `PRD-332`
15. `PRD-333`

## Proposition de tickets implementables

- `EP40-T01` Cartographier entites, repositories, services et use cases actuels.
- `EP40-T02` Valider les domaines fonctionnels cibles et les objets ambigus.
- `EP40-T03` Ajouter la documentation des regles d'import inter-domaines.
- `EP40-T04` Creer les packages fonctionnels dans `app/domaine`.
- `EP40-T05` Creer les packages fonctionnels dans `app/application`.
- `EP40-T06` Preparer le deplacement des objets `referencement` vers les packages cibles.
- `EP40-T07` Preparer le deplacement des objets `commercialisation` vers les packages cibles.
- `EP40-T08` Preparer le deplacement des objets `gestion_achats` vers les packages cibles.
- `EP40-T09` Preparer le deplacement des objets `gestion_reversement` vers les packages cibles.
- `EP40-T10` Preparer le deplacement des objets `support`, `exploitation`, `identite_acces`, `profils`, `dam` et `documentaire` vers les packages cibles.
- `EP40-T11` Mettre a jour les imports API, bootstrap, tests et infrastructure.
- `EP40-T12` Ajouter les tests d'import et de compilation.
- `EP40-T13` Mettre a jour la documentation architecture.
- `EP40-T14` Aligner les categories du menu back-office sur les domaines fonctionnels.
- `EP40-T15` Definir la convention de paths API par surface et domaine.
- `EP40-T16` Preparer les routers API vers les paths canoniques avec domaine.
- `EP40-T17` Basculer en one-shot les paths API et les consommateurs vers les paths canoniques.
- `EP40-T18` Aligner les tags OpenAPI sur les domaines fonctionnels.
- `EP40-T19` Creer l'enveloppe `animation_locale` : packages, segment API reserve et tag OpenAPI.
- `EP40-T20` Exposer les contrats OpenAPI filtres par surface : public, protected et internal.

Note : les tickets de preparation peuvent etre traites separement, mais la bascule effective des imports et des paths API se fait en une seule livraison cible.

## Risques

- Refactor massif difficile a relire.
- Imports circulaires entre domaines.
- Domaine `exploitation` trop large et peu utile.
- Ambiguite entre `referencement`, `commercialisation` et `profils`.
- Duplication des value objects partages.
- Migration partielle laissant deux organisations concurrentes.
- Perte d'ergonomie si les vues de pilotage transverses sont deplacees sans raccourci clair.
- Rupture frontend ou partenaire si les routes API changent sans mise a jour coordonnee des consommateurs.
- Documentation OpenAPI moins lisible si les tags de ressource remplacent les tags de domaine.

## Decisions actees

- Le domaine `identite_acces` est retenu.
- Le domaine `documentaire` est retenu et reste distinct de `dam`.
- Le domaine `animation_locale` est integre a la cartographie cible sous forme d'enveloppe ; son implementation fonctionnelle reste portee par l'Epic 41.
- `TypeCoffretConfig` est classe dans `commercialisation`.
- `IdentifiantCommercant` est classe dans `identite_acces`, car l'objet porte login, hash de mot de passe, verrouillage et tentatives de connexion.
- Les tokens de consultation sont classes dans `identite_acces` pour leur mecanique de securite ; les use cases de consultation post-achat restent dans `gestion_achats`.
- Aucun domaine `qr` n'est cree : le `qr_token` de `CoffretInstance` et son cycle de vie sont rattaches a `gestion_achats`.
- Les usages de scan et de validation terrain du QR coffret sont rattaches a `exploitation`.
- `QrToken` reste un value object partage entre `gestion_achats` et `exploitation`.
- La signature, verification cryptographique et gestion des cles QR restent dans `infrastructure/securite`.
- `FeedbackPrestation` est rattache a `exploitation` comme signal operationnel post-prestation.
- Une passerelle peut creer un `MessageContact` ou une alerte `support` si un feedback exige un traitement humain, sans deplacer l'objet source.
- Le back-office conserve un raccourci de pilotage transverse pour le dashboard global.
- Les vues specialisees sont rattachees a leur domaine : reversements dans `Gestion reversement`, client/support dans `Support`, coffret dans `Commercialisation`.
- Les anciens paths API ne coexistent pas avec les nouveaux paths canoniques.
- Les surfaces API sont separees dans trois contrats OpenAPI dedies : `/openapi/public.json`, `/openapi/protected.json` et `/openapi/internal.json`.
- Les endpoints `/docs/public`, `/docs/protected` et `/docs/internal` exposent les documentations interactives associees.
- Le contrat interne inclut les endpoints `/internal/*` et `/admin/api/*`.
- Les routes publiques migrent en une seule fois.
- La migration globale est one-shot.

## Decisions a prendre avant implementation

- Aucune decision bloquante restante a ce stade.
