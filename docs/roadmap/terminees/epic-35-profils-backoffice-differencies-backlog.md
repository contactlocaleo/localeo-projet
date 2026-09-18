# Backlog Epic 35 - Profils back-office differencies

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : remplacer l'acces SQLAdmin unique par une gestion de comptes back-office differencies, avec roles, profils et permissions adaptees aux usages support, exploitation, finance et administration.
- Decision contexte : l'Epic 34 reutilise la session SQLAdmin actuelle en MVP ; cette epic porte l'evolution vers des profils back-office differencies.
- Decision MVP : introduire des utilisateurs back-office applicatifs, sans remettre en cause immediatement les ecrans SQLAdmin existants.
- Hors scope MVP : SSO entreprise, federation d'identite, MFA obligatoire, gestion fine champ par champ.

## Probleme

Le back-office actuel repose sur un identifiant administrateur unique configure par variables d'environnement. Ce modele convient au demarrage, mais il ne permet pas de distinguer les responsabilites, limiter les actions sensibles, tracer clairement l'acteur humain ni appliquer des droits differencies selon les profils.

## Risque business

- Des operateurs peuvent acceder a des zones ou actions qui ne correspondent pas a leur mission.
- Les actions sensibles sont moins maitrisables si tous les utilisateurs partagent le meme niveau d'acces.
- L'audit perd de la valeur si l'identite back-office n'est pas rattachee a un utilisateur distinct.
- Les surfaces internes comme Localeo Control ou les vues finance ont besoin de droits differencies.

## Risque technique

- SQLAdmin ne fournit pas automatiquement une gestion de roles applicatifs complete.
- Une migration trop large peut casser l'acces admin existant.
- Les routes `/internal/*` et les vues SQLAdmin doivent partager un controle d'acces coherent.
- Les permissions doivent rester simples pour eviter une matrice impossible a maintenir.

## Perimetre MVP

- Creer un referentiel `utilisateurs_backoffice`.
- Creer un referentiel de roles/profils back-office.
- Gerer les roles MVP :
  - `ADMIN`
  - `EXPLOITATION`
  - `SUPPORT`
  - `FINANCE`
  - `LECTURE_SEULE`
- Remplacer l'authentification admin unique par une authentification utilisateur back-office.
- Conserver une compatibilite de migration depuis `LOCALEO_ADMIN_USERNAME` / `LOCALEO_ADMIN_PASSWORD`.
- Stocker en session l'identite utilisateur et ses roles.
- Controler l'acces aux routes `/admin`, `/internal/*` et aux APIs internes sensibles.
- Appliquer les permissions aux vues/actions principales SQLAdmin.
- Auditer les connexions, deconnexions, echecs et actions sensibles avec `backoffice_user_id`.
- Documenter la matrice de permissions MVP.

## Hors perimetre MVP

- SSO OAuth/OIDC/SAML.
- MFA obligatoire.
- Delegation temporaire de droits.
- Droits par champ ou par ligne metier.
- Gestion multi-tenant.
- Workflow complet de validation de creation utilisateur.

## User Stories

1. `PRD-251` En tant qu'administrateur, je veux creer un utilisateur back-office afin de donner un acces nominatif aux operateurs.
   - Statut : `Termine`
   - Resultat attendu : un utilisateur back-office porte login, nom, email, statut, roles et dates de cycle de vie.
   - Resultat attendu : le mot de passe est stocke uniquement sous forme de hash robuste.

2. `PRD-252` En tant qu'administrateur, je veux affecter des roles a un utilisateur afin de limiter ses acces au perimetre utile.
   - Statut : `Termine`
   - Resultat attendu : les roles MVP `ADMIN`, `EXPLOITATION`, `SUPPORT`, `FINANCE`, `LECTURE_SEULE` sont disponibles.
   - Resultat attendu : un utilisateur peut porter un ou plusieurs roles.

3. `PRD-253` En tant qu'operateur back-office, je veux me connecter avec mon compte personnel afin que mes actions soient tracees nominativement.
   - Statut : `Termine`
   - Resultat attendu : la connexion SQLAdmin utilise le referentiel utilisateurs back-office.
   - Resultat attendu : la session contient l'identite utilisateur et ses roles.

4. `PRD-254` En tant que responsable securite, je veux que les routes internes verifient les permissions afin de proteger les actions sensibles.
   - Statut : `Termine`
   - Resultat attendu : les routes `/internal/*` peuvent exiger une permission ou un role.
   - Resultat attendu : un acces non autorise retourne un refus explicite et audite.

5. `PRD-255` En tant qu'administrateur, je veux que les vues SQLAdmin respectent les roles afin d'eviter l'exposition inutile d'ecrans.
   - Statut : `Termine`
   - Resultat attendu : les vues SQLAdmin peuvent etre masquees ou refusees selon les roles.
   - Resultat attendu : les actions `create`, `edit`, `delete` peuvent etre limitees par profil.

6. `PRD-256` En tant que profil support, je veux acceder aux ecrans de support sans acceder aux actions finance ou configuration critique.
   - Statut : `Termine`
   - Resultat attendu : le role `SUPPORT` accede aux messages, timeline, mode secours et aides operationnelles.
   - Resultat attendu : le role `SUPPORT` ne peut pas modifier les configurations sensibles ni les paiements.

7. `PRD-257` En tant que profil finance, je veux acceder aux reversements, paiements et indicateurs financiers sans administrer tout le catalogue.
   - Statut : `Termine`
   - Resultat attendu : le role `FINANCE` accede aux vues reversements, paiements, remboursements et indicateurs financiers.
   - Resultat attendu : les actions non financieres sensibles restent refusees.

8. `PRD-258` En tant que profil exploitation, je veux acceder aux batchs, notifications et Localeo Control afin de piloter l'activite quotidienne.
   - Statut : `Termine`
   - Resultat attendu : le role `EXPLOITATION` accede au dashboard operationnel, batchs, Localeo Control, emails/SMS/WebPush sortants.
   - Resultat attendu : les actions de configuration critique restent reservees a `ADMIN`.

9. `PRD-259` En tant qu'auditeur, je veux retrouver l'utilisateur back-office a l'origine d'une action afin d'ameliorer la tracabilite.
   - Statut : `Termine`
   - Resultat attendu : les evenements d'audit sensibles portent `backoffice_user_id`, login et roles utiles.
   - Resultat attendu : les anciennes actions restent consultables meme si elles n'ont pas d'utilisateur nominatif.

10. `PRD-260` En tant qu'exploitant, je veux migrer depuis l'admin unique sans rupture afin de ne pas bloquer l'acces au back-office.
    - Statut : `Termine`
    - Resultat attendu : un utilisateur `ADMIN` initial peut etre cree depuis la configuration existante.
    - Resultat attendu : la migration documente comment retirer progressivement l'admin unique.

## Regles de gestion

- Un utilisateur back-office desactive ne peut plus se connecter.
- Un utilisateur doit avoir au moins un role actif pour acceder au back-office.
- `ADMIN` dispose de tous les droits MVP.
- `LECTURE_SEULE` ne peut pas executer d'action destructive ou de modification.
- Les permissions sont verifiees cote backend, pas seulement par masquage IHM.
- Toute action sensible doit conserver un audit avec l'identite back-office quand elle existe.
- Les routes Localeo Control de l'Epic 34 exigent a minima `ADMIN` ou `EXPLOITATION`.

## Modele cible

### Utilisateur back-office

Table cible : `utilisateurs_backoffice`

- `id`
- `login`
- `email`
- `nom_affiche`
- `password_hash`
- `statut`
- `roles`
- `created_at`
- `updated_at`
- `last_login_at`
- `disabled_at`
- `disabled_reason`

### Permissions

MVP possible : permissions derivees des roles en code, documentees dans une matrice.

Evolution possible : table `permissions_backoffice` et table de liaison role/permission si la matrice devient trop grande.

## APIs et integration cible

- Adapter `AdminAuthBackend` pour charger les utilisateurs back-office.
- Ajouter helpers de controle :
  - `require_backoffice_session`
  - `require_backoffice_role`
  - `require_backoffice_permission`
- Adapter les routes `/internal/*` sensibles.
- Surcharger `is_accessible` / `is_visible` sur les vues SQLAdmin critiques.
- Ajouter une page SQLAdmin de gestion des utilisateurs back-office reservee a `ADMIN`.

## Lots d'implementation

### Lot 1 - Modele et migration

- Ajouter modele ORM `UtilisateurBackoffice`.
- Ajouter bootstrap/migration de table.
- Initialiser un utilisateur `ADMIN` depuis la configuration actuelle.

### Lot 2 - Authentification

- Adapter `AdminAuthBackend`.
- Stocker `backoffice_user_id`, `admin_username` et `roles` en session.
- Conserver une procedure de reprise admin en cas de mauvaise configuration.

### Lot 3 - Permissions routes internes

- Ajouter helpers de securite back-office.
- Proteger routes `/internal/*` et batchs sensibles.
- Auditer les refus d'acces.

### Lot 4 - Permissions SQLAdmin

- Ajouter une base de vue SQLAdmin permissionnee.
- Masquer/refuser les vues selon roles.
- Limiter create/edit/delete sur les vues critiques.

### Lot 5 - Gestion utilisateurs

- Ajouter vue SQLAdmin reservee `ADMIN`.
- Permettre creation, desactivation, changement de roles et reinitialisation mot de passe.

### Lot 6 - Documentation et tests

- Documenter la matrice de permissions.
- Ajouter guide exploitation migration admin unique.
- Tester login, refus, roles et audit.

## Definition of Done

- Les utilisateurs back-office nominaux existent.
- Les roles MVP sont disponibles et documentes.
- SQLAdmin utilise les comptes back-office pour authentifier les operateurs.
- Les routes internes sensibles verifient les roles ou permissions.
- Les vues/actions SQLAdmin critiques sont controlees par profil.
- Les actions sensibles sont auditees avec l'utilisateur back-office.
- La migration depuis l'admin unique est documentee et testee.

## Points arbitres restants

- Confirmer si le MVP impose seulement des roles en code ou une table de permissions administrable.
- Confirmer si le mot de passe oublie back-office est inclus au MVP ou traite dans une V2.
- Confirmer si la MFA est une V2 ou une exigence des le premier deploiement production.
