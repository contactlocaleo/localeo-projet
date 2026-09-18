# Architecture solution - Localeo Backend

## 1. Vue d'ensemble

`localeo-backend` est le backend transactionnel de Localeo, marketplace locale de coffrets digitaux multi-prestations.

Il fournit :

- une API publique pour catalogue, achat, paiement, consultation, feedback et support ;
- une API protegee pour commercants, achats, validation terrain, batchs et maintenance ;
- un back-office SQLAdmin pour exploitation et support ;
- des integrations Stripe, Brevo Email, Brevo SMS et PostgreSQL ;
- des mecanismes d'audit, d'outbox, de tokens, de reversements et de gestion documentaire.

## 2. Decoupage logique

```text
Front marketplace / espace commercant / liens email-SMS
        |
        v
FastAPI app (app/main.py)
        |
        +-- app/api              Routes HTTP et schemas
        +-- app/security         Dependances auth, API keys, tokens
        +-- app/application      Use cases et services applicatifs
        +-- app/domaine          Entites, value objects, repositories, exceptions
        +-- app/infrastructure   ORM, repositories, providers, SQLAdmin
        +-- app/utils            Helpers dates, images, slugs
        |
        v
PostgreSQL + Stripe + Brevo + Scaleway Object Storage
```

## 3. Bounded contexts metier

### Catalogue

- Villes.
- Types de commercants.
- Types de coffrets.
- Commercants.
- Coffrets.
- Prestations.
- Profils publics commercants.
- Images/media.

### Achat et activation

- Achat particulier.
- Achat professionnel.
- Paiement Stripe.
- Instances de coffret.
- Tokens de gestion, activation, consultation.
- QR client et code de verification.

### Usage terrain

- Authentification commercant.
- Session bearer.
- Transaction de validation.
- Validation de prestation.
- Mode secours telephonique.
- Feedback post-prestation.

### Support et exploitation

- Messages de contact.
- Timeline support.
- Documents d'achat.
- Gestion documentaire transverse.
- Demandes de facturation.
- Remboursements.
- Audit.

### Finance commercant

- Mouvements de reversement.
- Reversements.
- Comptes bancaires.
- Campagnes de reversement Stripe Connect.
- Transfers Stripe.
- Synchronisation des statuts de paiement et reversement.
- Archives d'audit des anciens paiements manuels non actionnables.

### Notifications

- Outbox email.
- Outbox SMS.
- Relances avant expiration.
- Information d'expiration.
- Synchronisation provider.

## 4. Style d'architecture

L'architecture est en couches, orientee use cases, avec une influence hexagonale pragmatique.

Principes :

- les routes HTTP restent fines ;
- les use cases portent les scenarios metier ;
- la persistance est encapsulee par UnitOfWork et repositories ;
- les providers externes sont isoles dans l'infrastructure ;
- les tokens et controles d'acces sont centralises dans `app/security` ;
- SQLAdmin est assume comme back-office d'exploitation couple aux ORM.

## 5. Couches

### Couche API

Responsabilites :

- exposer les routes ;
- declarer les parametres et schemas ;
- brancher les dependances de securite ;
- deleguer aux use cases ;
- laisser les exceptions metier remonter vers les handlers globaux.

### Couche Application

Responsabilites :

- orchestrer les scenarios metier ;
- piloter les transactions ;
- appeler les services applicatifs ;
- creer les outbox ;
- produire les audits.

La couche application orchestre le metier, mais ne possede pas ses invariants. Elle peut charger les objets,
assembler les faits necessaires et coordonner les ports ; toute regle qui doit rester vraie quel que soit le
point d'entree est deleguee a une entite, un objet-valeur ou un service de domaine. Une condition metier ne
doit pas etre conservee dans un service applicatif uniquement parce que celui-ci dispose du Unit of Work.

### Couche Domaine

Responsabilites :

- definir les concepts et statuts ;
- porter les invariants, transitions et decisions metier ;
- fournir les value objects ;
- definir les contrats de repositories.

Principe DDD cible :

- `app/domaine/entities` contient les entites metier, avec une classe par entite et un nom explicite ;
- les enums et statuts fortement rattaches a une entite restent dans le fichier de cette entite au debut ;
- `app/domaine/value_objects` contient les value objects, avec une classe par value object ;
- `app/domaine/repositories` contient les ports repositories, avec une classe ou un protocole par repository ;
- `app/domaine/exceptions` contient les exceptions metier, avec une classe par exception ;
- les anciens modules domaine larges ne doivent pas rester comme facades de compatibilite durables apres la migration ;
- les renommages publics du domaine sont acceptes pendant la migration one-shot si les imports consommateurs sont migres immediatement ;
- tout renommage public doit etre applique dans tous les imports consommateurs dans la meme passe ;
- la couche domaine ne depend pas de FastAPI, SQLAlchemy, SQLAdmin, Stripe, Brevo ou Pydantic.
- une entite porte les regles liees a son propre etat et protege elle-meme ses transitions ;
- un objet-valeur porte validation, normalisation et operations de la valeur qu'il represente ;
- un service de domaine porte une decision pure associant plusieurs objets metier, sans base, reseau ou
  fournisseur externe ;
- toute nouvelle Epic identifie ses agregats, invariants et transitions avant ses services applicatifs et API ;
- toute regle existante modifiee dans `app/application` doit etre replacee dans le domaine lorsque sa nature
  metier le permet, conformement a l'[ADR domaine d'abord](../decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md).

### Couche Infrastructure

Responsabilites :

- modeles ORM ;
- repositories SQLAlchemy ;
- mapping ;
- providers Stripe/Brevo ;
- back-office SQLAdmin ;
- services techniques.
- stockage documentaire externe local ou S3 compatible.

### Couche Tests Fonctionnels

Responsabilites :

- tester les invariants du domaine sans infrastructure ;
- tester les use cases et services applicatifs avec Unit of Work fake ;
- remplacer les providers externes par des fakes ou stubs ;
- tracer la couverture des UC fonctionnels par une matrice de tests ;
- accompagner toute modification d'un use case, d'un objet domaine ou d'un composant infrastructure par la creation ou la mise a jour du test associe dans la meme livraison ;
- maintenir une classe `Test<UseCase>` dediee pour chaque use case applicatif public exposant `execute`, avec au moins un scenario metier ou workflow observable ;
- maintenir un fichier de test dedie pour chaque classe publique de `app/domaine`, range par domaine fonctionnel et categorie ;
- regrouper les tests par domaine fonctionnel lorsque plusieurs classes participent a la meme regle metier ;
- refuser les tests purement structurels comme couverture metier : les tests doivent verifier une regle observable, un invariant, une transition d'etat, un appel de port ou un contrat technique utile ; l'import, l'existence de classe ou la simple instanciation ne suffisent pas.

Structure cible :

- `tests/domain/<domaine>/entities` pour les entites rattachees a un domaine fonctionnel ;
- `tests/domain/shared/value_objects` pour les value objects partages ;
- `tests/application/use_cases` pour les scenarios applicatifs ;
- `tests/application/services` pour les services applicatifs ;
- `tests/infrastructure` pour les repositories, mappers, gateways, providers, stockage et integrations techniques ;
- `tests/application/fakes` et `tests/application/builders` pour les donnees et ports de test.

## 6. Donnees

La base PostgreSQL contient les familles suivantes :

- referentiels et catalogue ;
- achats, paiements et instances ;
- validations et feedbacks ;
- auth commercant et tokens ;
- support, documents et remboursements ;
- referentiel documentaire transverse et rattachements ;
- emails, SMS et relances ;
- reversements Stripe Connect et projections de paiement ;
- medias ;
- audit et API keys.

Les identifiants metier sont majoritairement des UUID.

Le stockage documentaire suit une regle stricte : la base conserve uniquement les metadonnees et references opaques de stockage (`storage_provider`, `storage_bucket`, `storage_key`, hash, taille, MIME type). Les binaires sont stockes hors base, via un adaptateur local en developpement ou Scaleway Object Storage compatible S3 en production.

## 7. Flux principaux

### 7.1 Achat particulier

```text
Client -> /public/gestion-achats/paiements/initialiser -> Stripe Checkout
Stripe -> /public/stripe/webhook -> ValiderPaiement
ValiderPaiement -> Achat confirme
                -> CoffretInstance ACTIVE
                -> QR + consultation token
                -> statuts prestations
                -> email/SMS outbox
                -> document/snapshot
```

### 7.2 Achat professionnel

```text
Client pro -> Paiement Stripe
Webhook -> achat confirme
        -> management token
        -> N instances EN_ATTENTE_ACTIVATION
Acheteur pro -> /protected/achats/* avec token
Beneficiaire -> activation
Activation -> QR + consultation token + prestations
```

### 7.3 Validation terrain

```text
Commercant -> login -> session bearer
Client presente QR
Commercant -> ouvrir transaction
Commercant -> valider prestation
Systeme -> ValidationPrestation
        -> MouvementReversement
        -> Email confirmation
        -> Feedback token
```

### 7.4 Mode secours

```text
Support -> Back-office Coffret instance
        -> Mode secours
        -> decision AUTORISE / REFUSE / A_CONTROLER
        -> ValidationSecours
        -> audit
        -> validation nominale si AUTORISE
```

### 7.5 Reversements

```text
Validation prestation -> MouvementReversement
Back-office -> campagne Stripe Connect
Stripe -> transfer Connect
Webhook Stripe -> confirmation ou echec
Back-office -> reprise Stripe idempotente si necessaire
```

## 8. Securite dans l'architecture

### Existante

- API keys internes hashees et scopees.
- Tokens opaques hashees pour sessions, management, activation, consultation.
- Bcrypt pour mots de passe commercants.
- Rate limiting applicatif sur auth commercant.
- Signature Stripe.
- Session admin SQLAdmin.
- Protection middleware des routes `/internal/*`.
- Audit metier persistant.
- Documents prives servis via backend uniquement, sans exposition directe des URLs de stockage.
- Cloisonnement applicatif des documents prives commercants : un commercant authentifie ne peut consulter que les documents rattaches a son propre compte.

### A durcir avant production

- fermer les endpoints publics d'ecriture non publics ;
- proteger upload image ;
- ajouter CSRF back-office ;
- rediger query strings et tokens dans les logs ;
- supprimer les tokens sensibles des URLs ou les isoler derriere liens courts/echange POST ;
- desactiver ou proteger OpenAPI en production ;
- ajouter TrustedHost/security headers ;
- sortir les secrets des fichiers suivis Git ;
- formaliser retention RGPD et purge des donnees sensibles.

## 9. Back-office

SQLAdmin est la surface d'exploitation principale.

Vues custom :

- Dashboard operationnel.
- Batchs exploitation.
- Timeline support.

Model views principales :

- Ville, Type commercant, Type coffret.
- Commercant, Acces commercant.
- Coffret, Prestation coffret, versions.
- Profil commercant, versions.
- Achat coffret, Coffret instance, Paiement, Remboursement achat.
- Documents et demandes de facturation.
- Gestion documentaire : upload, metadonnees, publication, archivage, preview HTML et rattachements.
- Statuts de prestations, transactions, sessions, validations.
- Comptes bancaires, mouvements, reversements, paiements, lots.
- Motifs et messages support.
- Emails, SMS, liens courts.
- API keys, audit, executions batch, verrous batch.
- Images, activites locales, feedbacks.

Routes internes de documentation :

- `/internal/docs/backoffice`.
- `/internal/docs/reversements`.

## 10. Observabilite

L'architecture prevoit :

- `X-Request-ID` ;
- logs HTTP ;
- logs de use cases ;
- logs d'invariants ;
- evenements d'audit persistants ;
- historique d'execution des batchs ;
- health operationnel des batchs critiques ;
- timeline support agregeant plusieurs sources.

Point d'attention : les logs doivent etre expurges des tokens et donnees personnelles inutiles.

## 11. Integrations externes

### Stripe

- Creation de checkout session.
- Webhook signe.
- Transfers Stripe Connect pilotes par campagnes, avec intention durable et cle d'idempotence stable.
- Reconciliation depuis le back-office avec les operations Stripe ; cette action ne constitue pas un virement bancaire manuel.
- Les payouts Stripe du compte connecte vers la banque sont distincts des transfers depuis la plateforme.

### Brevo

- Email transactionnel.
- SMS transactionnel.
- Synchronisation des statuts.
- Mode dev pour environnements non production.

### Frontends

- Marketplace.
- Espace achat professionnel.
- Activation beneficiaire.
- Consultation de coffret.
- Espace commercant.
- Feedback prestation.

Les URLs front sont configurees par variables d'environnement.

### Scaleway Object Storage

- Stockage production cible pour les documents publics et prives.
- Acces via API S3 compatible.
- Region cible : Paris.
- Bucket cible : `localeo-archives`.
- Prefixe applicatif cible : `/archives`.
- Le backend sert les fichiers aux utilisateurs et conserve les references Scaleway opaques.

## 12. Decisions structurantes

- Un `AchatCoffret` represente la commande.
- Une `CoffretInstance` represente l'unite activable/consommable.
- Une prestation consommee cree une validation et un mouvement de reversement.
- Les notifications passent par outbox.
- Les reversements commercants passent exclusivement par Stripe Connect, sans fallback bancaire manuel, conformement a l'[ADR EPIC 39 acceptee](../decisions/ADR-2026-07-09-epic-39-stripe-connect-implementation.md). Les anciennes donnees de paiement manuel sont des archives d'audit non actionnables. Le [guide de pilotage Stripe Connect](../../exploitation/exploitation/piloter-reversements-stripe-connect.md) est la procedure d'exploitation applicable.
- Les profils publics commercants sont versionnes et moderes.
- Les activites publiques sont anonymisees.
- Les documents publics sont versionnes ; publier une nouvelle version archive l'ancienne version publiee pour le meme type/scope.
- Les documents publics HTML peuvent etre derives d'un PDF via une preview retouchable avant sauvegarde.
- Les documents prives et PDF publics sont servis via backend, pas par URL directe du stockage objet.

## 13. Risques architecturaux connus

- Back-office tres puissant et couple a la base.
- Cohabitation scripts SQL et bootstrap runtime.
- Tokens front encore presents dans des URLs.
- Upload media public dans l'etat actuel.
- Retention RGPD a completer.
- Plusieurs APIs d'ecriture publiques a verrouiller avant production.

## 14. Cible d'evolution

Court terme avant go-live :

- durcissement securite/RGPD ;
- migration config/secrets propre ;
- redaction logs ;
- protection CSRF ;
- protection upload et endpoints publics ;
- tests securite go-live.

Moyen terme :

- RBAC back-office ;
- MFA admin ;
- migration Alembic stricte ;
- chiffrement applicatif de certains champs financiers ;
- retention automatisee par categorie de donnees ;
- separation progressive de vues metier admin si besoin.
