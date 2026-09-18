# Backlog Epic 10 - Authentification commercant par login / mot de passe

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Perimetre

Epic source : `Epic 10. Authentification commercant par login / mot de passe`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : remplacer l'authentification initiale du commercant par QR code par une authentification login / mot de passe, tout en conservant le principe de session commercant courte, revocable et protegee par scopes pour les actions sensibles.

## Statut global

- Epic 10 : `Termine`
- Avancement : implementation backend realisee pour le modele, les use cases, les APIs, les emails, le rate limiting, l'audit et le decommissionnement du `qr_commercant` ; verification runtime a finaliser dans un environnement Python disponible.

## Analyse d'impact

### Synthese

Le changement porte sur le facteur d'authentification initial du commercant. Le modele de session existant (`sessions_commercant`, token opaque, TTL, scopes, revocation) reste pertinent et doit etre conserve. Le concept de `qr_commercant` est decommissionne totalement avant production.

Le QR coffret client reste hors perimetre de remplacement : il continue a servir au parcours terrain de consommation d'une `CoffretInstance` et a l'ouverture d'une transaction de validation.

Comme l'application est encore en phase de developpement et qu'il n'existe pas de commercants actifs a migrer, aucune procedure de migration QR commercant vers login / mot de passe n'est prevue.

### Impacts fonctionnels

- Le commercant s'authentifie avec un identifiant de connexion et un mot de passe.
- L'identifiant recommande en V1 est l'email de contact du commercant, normalise en minuscules.
- L'ouverture de session commercant ne depend plus de `qr_commercant`.
- Le parcours "mot de passe oublie" devient obligatoire pour eviter une dependance au support.
- Le commercant doit pouvoir mettre a jour son mot de passe depuis une session valide.
- L'admin doit pouvoir initialiser ou reinitialiser l'acces d'un commercant lors de l'onboarding ou d'un incident.
- Les statuts commercant restent bloquants : un commercant `SUSPENDU` ou `ARCHIVE` ne doit pas pouvoir ouvrir une nouvelle session.
- Le parcours QR commercant est supprime du produit et ne doit pas etre expose au front.

### Impacts API

- Ajouter `POST /commercants/auth/login`.
- Ajouter `POST /commercants/auth/initialiser-mot-de-passe`.
- Ajouter `POST /commercants/auth/mot-de-passe-oublie`.
- Ajouter `POST /commercants/auth/reinitialiser-mot-de-passe`.
- Ajouter `POST /commercants/me/mot-de-passe`.
- Conserver `GET /commercants/session/valider` et `POST /commercants/session/{session_id}/invalider`.
- Supprimer les surfaces API liees au `qr_commercant` :
  - `POST /commercants/valider-qr` ;
  - l'usage de `qr_commercant` dans `POST /commercants/session/ouvrir` ;
  - les schemas de requete/reponse dedies au QR commercant.
- Maintenir les APIs protegees par `Authorization: Bearer <session_token>` sans changement de contrat pour les actions metier.

### Impacts use cases

Use cases a creer :
- `AuthentifierCommercantParMotDePasse`
- `DemanderReinitialisationMotDePasseCommercant`
- `ReinitialiserMotDePasseCommercant`
- `MettreAJourMotDePasseCommercant`
- `InitialiserAccesCommercant`

Use cases a adapter :
- `InitialiserSessionCommercant` doit pouvoir creer une session apres authentification login / mot de passe, sans verifier de QR.
- `VerifierSessionCommercant`, `ValiderSessionCommercant` et `InvaliderSessionCommercant` sont conserves.
- `ValiderQrCommercant` est supprime.
- `ReferencerCommercant` ne doit plus emettre de carte QR commercant ; il doit creer l'identifiant commercant et preparer ou envoyer le lien d'initialisation du mot de passe.
- `RegenererCarteIdentiteCommercant` est supprime.

### Impacts modele de donnees

Option recommandee V1 : creer une table dediee `identifiants_commercant`.

Champs recommandes :
- `id`
- `commercant_id`
- `login`
- `password_hash`
- `password_configured_at`
- `password_updated_at`
- `failed_attempts`
- `locked_at`
- `locked_reason`
- `date_creation`
- `date_derniere_connexion`

Table dediee pour les liens d'initialisation et de reinitialisation :
- `id`
- `commercant_id`
- `type_token` (`INITIALISATION`, `REINITIALISATION`)
- `token_hash`
- `date_creation`
- `date_expiration`
- `date_utilisation`
- `date_revocation`
- `ip_creation`
- `user_agent_creation`

Table dediee pour le rate limiting applicatif :
- `id`
- `operation` (`LOGIN`, `PASSWORD_RESET_REQUEST`)
- `login_normalise`
- `client_ip_hash`
- `window_start`
- `window_end`
- `attempts_count`
- `date_derniere_tentative`
- `blocked_until`

La table `commercants` peut conserver les donnees de contact. Le login ne doit pas etre simplement assimile au contact email sans contrainte d'unicite explicite.

### Impacts securite

- Stocker uniquement un hash de mot de passe robuste, jamais le mot de passe en clair.
- Utiliser `bcrypt` comme fonction de hash des mots de passe.
- Le cout bcrypt doit etre configurable par variable d'environnement, avec `LOCALEO_BCRYPT_ROUNDS=12` en valeur cible V1.
- Appliquer une politique minimale de mot de passe : 12 caracteres minimum, rejet des mots de passe contenant le login/email, rejet d'une liste locale de mots de passe faibles courants, sans rotation periodique obligatoire.
- La denylist de mots de passe faibles demarre en V1 par une liste locale dans le code, enrichissable ensuite.
- Ajouter une limitation de tentatives applicative stockee en table dediee : 5 echecs / 15 minutes / couple login + IP pour le login ; 5 demandes / 15 minutes / couple login + IP pour le mot de passe oublie.
- Verrouiller l'acces apres 5 echecs d'authentification consecutifs, seuil configurable ; le deverrouillage est manuel par admin en V1.
- Utiliser des messages d'erreur non enumerants sur login et mot de passe oublie.
- Journaliser les echecs et succes d'authentification sans secret.
- Les tokens d'initialisation et de reinitialisation doivent etre opaques, aleatoires, hashes en base, expirables et a usage unique.
- Duree maximale acceptable des liens : 24h. Valeurs V1 recommandees : initialisation 24h, reinitialisation 1h.
- Revoquer toutes les sessions existantes apres changement ou reinitialisation de mot de passe, y compris la session courante.

### Impacts emails et notification

- Ajouter un email d'initialisation d'acces commercant.
- Ajouter un email de reinitialisation de mot de passe.
- Les templates email cibles sont `acces_commercant_initialisation.html` et `mot_de_passe_commercant_reinitialisation.html`, inspires de la charte graphique des templates existants.
- Les emails doivent passer par l'outbox existante `EmailSortant`.
- L'URL front d'initialisation du mot de passe doit etre parametree par une variable d'environnement dediee.
- L'URL front de reinitialisation du mot de passe doit etre parametree par une variable d'environnement dediee, selon le meme principe que les autres URLs front.
- Les liens front doivent transporter un token brut en query param uniquement vers le front, puis le front appelle le backend avec le token.

### Impacts back-office / exploitation

- SQLAdmin doit permettre de voir l'etat d'acces d'un commercant sans afficher de hash ni de token.
- SQLAdmin doit permettre d'envoyer un lien d'initialisation.
- SQLAdmin doit permettre de declencher une reinitialisation d'acces.
- SQLAdmin doit permettre de verrouiller et deverrouiller l'acces d'un commercant.
- Les vues et actions SQLAdmin liees aux cartes QR commercant doivent etre supprimees.
- Aucune procedure de migration n'est necessaire : les donnees de developpement peuvent etre recreees ou ajustees par seed.

### Impacts front commercant

- Remplacer l'ecran de scan QR d'ouverture par un ecran login / mot de passe.
- Ajouter les ecrans :
  - mot de passe oublie ;
  - initialisation par lien ;
  - reinitialisation par lien ;
  - mise a jour du mot de passe connecte.
- Continuer a stocker et transmettre le `session_token` comme aujourd'hui.
- En cas de `Session expiree` ou `Session invalide`, rediriger vers le login.

### Impacts tests

- Tests unitaires du hash, de l'authentification, du verrouillage et des erreurs.
- Tests unitaires des tokens d'initialisation et de reinitialisation : expiration, usage unique, hash, invalidite.
- Tests d'integration des endpoints d'authentification et de session.
- Tests de non regression sur les APIs protegees par scope.
- Tests de non exposition des anciennes routes QR commercant si elles sont supprimees.

## Regles de gestion consolidees

- Un commercant actif peut ouvrir une session avec un login et un mot de passe valides.
- Un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas ouvrir de nouvelle session.
- Le login doit etre unique.
- Le mot de passe brut n'est jamais stocke ni journalise.
- Une authentification reussie emet une session commercant avec les scopes prevus.
- Une authentification echouee ne doit pas permettre de distinguer login inconnu et mot de passe incorrect.
- Le mot de passe oublie declenche un email si le login correspond a un commercant eligible, mais la reponse API reste generique.
- Un lien d'initialisation permet au commercant de definir son premier mot de passe sans mot de passe temporaire.
- Un token d'initialisation ou de reinitialisation est opaque, expire, a usage unique et stocke uniquement sous forme hashee.
- Un changement ou une reinitialisation de mot de passe revoque les sessions commercant existantes.
- La revocation apres changement ou reinitialisation concerne toutes les sessions, y compris la session courante.
- La mise a jour du mot de passe depuis une session valide exige le mot de passe courant.
- Le rate limiting du login et du mot de passe oublie est gere applicativement.
- Les actions commercant protegees restent controlees par session bearer et scopes.
- Le `qr_commercant`, les cartes d'identite commercant et les endpoints associes ne font plus partie du produit cible.

## Decisions produit actees

- Hashage des mots de passe : `bcrypt`.
- Cout bcrypt : `LOCALEO_BCRYPT_ROUNDS=12`, configurable par environnement.
- Politique mot de passe V1 : 12 caracteres minimum, rejet du login/email, rejet d'une denylist locale de mots de passe faibles.
- Denylist mot de passe V1 : liste locale minimale dans le code, enrichissable sans migration fonctionnelle.
- Duree des liens : maximum acceptable 24h ; initialisation 24h, reinitialisation 1h en valeur recommandee.
- Rate limiting login : 5 echecs / 15 minutes / login + IP.
- Rate limiting mot de passe oublie : 5 demandes / 15 minutes / login + IP.
- Stockage rate limiting : table dediee en base.
- Verrouillage compte : 5 echecs consecutifs, seuil configurable, deverrouillage admin uniquement en V1.
- Changement ou reinitialisation de mot de passe : revocation de toutes les sessions commercant.
- Decommissionnement QR commercant : suppression complete du concept `qr_commercant`.
- Onboarding commercant : envoi d'un lien d'initialisation, sans mot de passe temporaire.
- Back-office attendu : voir l'etat d'acces, envoyer un lien d'initialisation, reinitialiser, verrouiller et deverrouiller.
- Rate limiting : applicatif.
- Actions d'audit minimales : `auth.login.success`, `auth.login.failed`, `password.reset.requested`, `password.reset.succeeded`, `password.init.requested`, `password.init.succeeded`, `auth.login.updated`, `account.locked`, `account.unlocked`.

## Configuration cible

- `LOCALEO_BCRYPT_ROUNDS=12`
- `LOCALEO_PASSWORD_MIN_LENGTH=12`
- `LOCALEO_PASSWORD_RESET_TOKEN_TTL_MINUTES=60`
- `LOCALEO_PASSWORD_INIT_TOKEN_TTL_HOURS=24`
- `LOCALEO_AUTH_RATE_LIMIT_WINDOW_SECONDS=900`
- `LOCALEO_AUTH_LOGIN_MAX_FAILURES_PER_WINDOW=5`
- `LOCALEO_AUTH_PASSWORD_RESET_MAX_REQUESTS_PER_WINDOW=5`
- `LOCALEO_AUTH_ACCOUNT_LOCK_MAX_FAILURES=5`
- `LOCALEO_FRONT_COMMERCANT_PASSWORD_INIT_URL_TEMPLATE`
- `LOCALEO_FRONT_COMMERCANT_PASSWORD_RESET_URL_TEMPLATE`

Les variables d'URL front doivent contenir un placeholder explicite pour injecter le token, par exemple `{token}`.

## Templates email cibles

### Initialisation d'acces commercant

- Fichier : `app/infrastructure/email/templates/acces_commercant_initialisation.html`
- Objet recommande : `Initialisez votre acces commercant Localeo`
- Placeholders : `{{localeo_icon_url}}`, `{{nom_commercant}}`, `{{login}}`, `{{duree_validite}}`, `{{lien_initialisation}}`
- Contenu : annonce de l'acces prepare, rappel de l'identifiant, bouton de definition du premier mot de passe, lien brut de secours, avertissement de securite.

### Reinitialisation de mot de passe commercant

- Fichier : `app/infrastructure/email/templates/mot_de_passe_commercant_reinitialisation.html`
- Objet recommande : `Reinitialisez votre mot de passe Localeo`
- Placeholders : `{{localeo_icon_url}}`, `{{nom_commercant}}`, `{{duree_validite}}`, `{{lien_reinitialisation}}`
- Contenu : confirmation de la demande, bouton de choix d'un nouveau mot de passe, lien brut de secours, rappel que les sessions existantes seront revoquees, message de securite si la demande n'est pas reconnue.

## Contrat API front cible

### `POST /commercants/auth/login`

Requete :
```json
{
  "login": "contact@commerce.fr",
  "password": "mot-de-passe"
}
```

Reponse `200` :
```json
{
  "session_token": "opaque-token",
  "expires_at": "2026-04-21T12:00:00Z",
  "scopes": ["commercant:session", "commercant:transaction"],
  "commercant": {
    "id": "uuid",
    "nom": "Commerce"
  }
}
```

### `POST /commercants/auth/mot-de-passe-oublie`

Requete :
```json
{
  "login": "contact@commerce.fr"
}
```

Reponse `202` non enumerante :
```json
{
  "message": "Si le compte est eligible, un email de reinitialisation sera envoye."
}
```

### `POST /commercants/auth/initialiser-mot-de-passe`

Requete :
```json
{
  "token": "token-brut-recu-par-email",
  "nouveau_mot_de_passe": "nouveau-mot-de-passe"
}
```

Reponse `204`.

### `POST /commercants/auth/reinitialiser-mot-de-passe`

Requete :
```json
{
  "token": "token-brut-recu-par-email",
  "nouveau_mot_de_passe": "nouveau-mot-de-passe"
}
```

Reponse `204`.

### `POST /commercants/me/mot-de-passe`

Requete :
```json
{
  "mot_de_passe_courant": "mot-de-passe-actuel",
  "nouveau_mot_de_passe": "nouveau-mot-de-passe"
}
```

Reponse `204`. Toutes les sessions du commercant sont revoquees, y compris la session courante.

## Flux cible recommande

1. Le commercant saisit son login et son mot de passe.
2. Le backend verifie les identifiants et le statut du commercant.
3. Le backend cree une `session_commercant` opaque avec TTL et scopes.
4. Le front utilise `Authorization: Bearer <session_token>` pour les APIs protegees.
5. Le commercant peut demander une reinitialisation en cas d'oubli.
6. Le commercant peut changer son mot de passe depuis son espace authentifie.

## Backlog priorise

### Story `PRD-046` - Authentifier un commercant par login / mot de passe

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre au commercant d'acceder a l'application sans QR dedie.

Criteres d'acceptation :
- Un endpoint `POST /commercants/auth/login` accepte un login et un mot de passe.
- Le systeme verifie le hash bcrypt du mot de passe sans exposer le secret.
- Le systeme refuse un commercant non `ACTIF`.
- Le systeme refuse un acces verrouille.
- En cas de succes, le systeme emet un `session_token`, `expires_at`, les scopes et le resume du commercant.
- En cas d'echec, la reponse ne permet pas de savoir si le login existe.
- Les echecs sont audites avec l'action `auth.login.failed`.
- Les succes sont audites avec l'action `auth.login.success`.
- Le login est refuse si aucun mot de passe n'a encore ete initialise.

Taches :
- Ajouter le modele d'identifiants commercant.
- Ajouter le service de hash et verification bcrypt.
- Ajouter la configuration du cout bcrypt.
- Ajouter le rate limiting applicatif du login.
- Implementer le use case `AuthentifierCommercantParMotDePasse`.
- Ajouter l'endpoint de login.
- Adapter la creation de session pour accepter un commercant deja authentifie.
- Ajouter les tests unitaires et API.

Definition of done :
- Un commercant `ACTIF` peut ouvrir une session sans QR.
- Le contrat de session existant reste compatible avec les APIs protegees.

### Story `PRD-047` - Gerer le mot de passe oublie

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre au commercant de recuperer son acces sans intervention support.

Criteres d'acceptation :
- Un endpoint `POST /commercants/auth/mot-de-passe-oublie` accepte un login.
- La reponse API est generique, que le login existe ou non.
- Si le login est eligible, un token de reinitialisation expire est cree et stocke sous forme hashee.
- Un email de reinitialisation est prepare via l'outbox.
- Le lien de reinitialisation utilise une URL front parametree par variable d'environnement, par exemple `LOCALEO_FRONT_COMMERCANT_PASSWORD_RESET_URL_TEMPLATE`.
- Le template d'URL doit permettre d'injecter le token de reinitialisation.
- La demande eligible est auditee avec l'action `password.reset.requested`.
- Les demandes trop frequentes sont limitees.

Taches :
- Ajouter le modele de token d'acces commercant avec type `REINITIALISATION`.
- Implementer le use case `DemanderReinitialisationMotDePasseCommercant`.
- Ajouter le template email.
- Ajouter la configuration de l'URL front de reinitialisation dans `app/config.py`.
- Ajouter le rate limiting applicatif de la demande de reinitialisation.
- Ajouter l'endpoint de demande.
- Ajouter les tests de non enumeration et de cooldown.

Definition of done :
- Le commercant peut initier une recuperation de compte de facon securisee.

### Story `PRD-048A` - Initialiser le premier mot de passe via lien

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre l'onboarding d'un commercant sans mot de passe temporaire et sans QR commercant.

Criteres d'acceptation :
- Le back-office peut envoyer un lien d'initialisation a un commercant eligible.
- Le token d'initialisation est opaque, expire, a usage unique et stocke uniquement sous forme hashee.
- Le lien d'initialisation utilise `LOCALEO_FRONT_COMMERCANT_PASSWORD_INIT_URL_TEMPLATE`.
- Un endpoint `POST /commercants/auth/initialiser-mot-de-passe` accepte un token et un nouveau mot de passe.
- Le nouveau mot de passe respecte la politique minimale.
- Le hash du mot de passe est cree et `password_configured_at` est renseigne.
- Le token est marque comme utilise.
- L'initialisation demandee est auditee avec l'action `password.init.requested`.
- L'initialisation reussie est auditee avec l'action `password.init.succeeded`.

Taches :
- Implementer le use case `InitialiserAccesCommercant`.
- Ajouter le template email d'initialisation.
- Ajouter la configuration `LOCALEO_FRONT_COMMERCANT_PASSWORD_INIT_URL_TEMPLATE`.
- Ajouter l'endpoint d'initialisation.
- Ajouter les actions SQLAdmin d'envoi de lien d'initialisation.
- Ajouter les tests d'expiration, usage unique, hash et audit.

Definition of done :
- Un commercant peut definir son premier mot de passe via un lien envoye par email, sans mot de passe temporaire.

### Story `PRD-048` - Reinitialiser un mot de passe via token

Priorite : `P0`
Statut : `Termine`

Valeur metier : finaliser le parcours de recuperation et restaurer l'acces du commercant.

Criteres d'acceptation :
- Un endpoint `POST /commercants/auth/reinitialiser-mot-de-passe` accepte un token et un nouveau mot de passe.
- Le token est refuse s'il est inconnu, expire, deja utilise ou revoque.
- Le nouveau mot de passe respecte la politique minimale.
- Le hash du mot de passe est mis a jour.
- Le token est marque comme utilise.
- Toutes les sessions commercant existantes sont revoquees.
- La reinitialisation reussie est auditee avec les actions `password.reset.succeeded` et `auth.login.updated`.

Taches :
- Implementer le use case `ReinitialiserMotDePasseCommercant`.
- Ajouter l'endpoint de reinitialisation.
- Ajouter la revocation des sessions existantes du commercant.
- Ajouter les tests d'expiration, usage unique et revocation.

Definition of done :
- Un token valide permet de definir un nouveau mot de passe une seule fois.

### Story `PRD-049` - Mettre a jour son mot de passe depuis une session valide

Priorite : `P1`
Statut : `Termine`

Valeur metier : permettre au commercant de maintenir la securite de son compte.

Criteres d'acceptation :
- Un endpoint `POST /commercants/me/mot-de-passe` est protege par session commercant.
- Le mot de passe courant est obligatoire.
- Le nouveau mot de passe respecte la politique minimale.
- Toutes les sessions existantes sont revoquees apres changement, y compris la session courante.
- Une trace d'audit `auth.login.updated` est produite sans secret.

Taches :
- Implementer le use case `MettreAJourMotDePasseCommercant`.
- Ajouter l'endpoint protege.
- Ajouter la verification du mot de passe courant.
- Ajouter les tests d'autorisation et de revocation.

Definition of done :
- Un commercant connecte peut changer son mot de passe sans passer par le support.

### Story `PRD-050` - Decommissionner le `qr_commercant`

Priorite : `P1`
Statut : `Termine`

Valeur metier : simplifier le produit avant production en supprimant un mode d'authentification non retenu.

Criteres d'acceptation :
- Le concept de `qr_commercant` est retire du parcours produit.
- Les endpoints et schemas QR commercant ne sont plus exposes.
- `ReferencerCommercant` ne genere plus de carte QR commercant.
- Les use cases, repositories, modeles et vues admin dedies aux cartes QR commercant sont supprimes.
- Les nouveaux commercants disposent d'un identifiant d'acces unique.
- Le back-office permet de voir l'etat d'acces.
- Le back-office permet d'envoyer un lien d'initialisation.
- Le back-office permet de declencher une reinitialisation d'acces.
- Le back-office permet de verrouiller et deverrouiller un acces.
- L'onboarding envoie un lien d'initialisation permettant au commercant de definir son premier mot de passe.
- Le decommissionnement du `qr_commercant` n'a aucun impact sur le QR coffret client.

Taches :
- Adapter `ReferencerCommercant` pour creer l'identifiant commercant et preparer ou envoyer le lien d'initialisation du mot de passe.
- Adapter SQLAdmin pour piloter l'etat d'acces, l'initialisation, la reinitialisation et le verrouillage.
- Supprimer les endpoints, schemas et use cases QR commercant.
- Supprimer les scopes et actions dedies a la carte commercant.
- Mettre a jour les specifications fonctionnelles et techniques.

Definition of done :
- Le code et la documentation ne presentent plus le `qr_commercant` comme un mecanisme disponible.

## Chantiers transverses

### BX-EP10-01 - Securite des mots de passe

Priorite : `P0`

Livrables :
- hashage bcrypt ;
- cout bcrypt configurable ;
- politique de mot de passe ;
- denylist locale minimale de mots de passe faibles ;
- verrouillage temporaire apres echecs repetes ;
- rate limiting applicatif login et mot de passe oublie ;
- journalisation securisee des tentatives.

### BX-EP10-02 - Persistence

Priorite : `P0`

Livrables :
- tables d'identifiants et de tokens d'initialisation/reinitialisation ;
- table dediee de rate limiting applicatif ;
- support de l'initialisation par lien ;
- support du verrouillage/deverrouillage ;
- repositories dedies ;
- contraintes d'unicite du login.

### BX-EP10-03 - Emails et liens front

Priorite : `P0`

Livrables :
- template email d'initialisation `acces_commercant_initialisation.html` ;
- template email de reinitialisation `mot_de_passe_commercant_reinitialisation.html` ;
- URL front d'initialisation configurable par variable d'environnement ;
- URL front de reinitialisation configurable par variable d'environnement ;
- strategie d'expiration des liens.

### BX-EP10-04 - Decommissionnement du `qr_commercant`

Priorite : `P1`

Livrables :
- endpoints QR commercant supprimes ;
- documentation nettoyee des references au `qr_commercant` ;
- suppression du QR comme pre-requis d'authentification ;
- suppression des cartes QR commercant.

### BX-EP10-05 - Couverture de tests

Priorite : `P0`

Livrables :
- tests unitaires use cases ;
- tests API login / oubli / reset / changement ;
- tests de non regression session et scopes ;
- tests de revocation des sessions.
- tests de rate limiting applicatif ;
- tests d'audit des actions `auth.login.success`, `auth.login.failed`, `password.reset.requested`, `password.reset.succeeded`, `password.init.requested`, `password.init.succeeded`, `auth.login.updated`, `account.locked`, `account.unlocked`.

## Dependances

- Existence d'un email de contact fiable pour chaque commercant.
- Front commercant capable d'afficher les ecrans login, initialisation, oubli, reset et changement de mot de passe.
- Configuration d'URLs front pour les liens d'initialisation et de reinitialisation, dont la variable dediee au lien de reinitialisation de mot de passe commercant.
- Outbox email operationnelle.
- Aucun besoin de migration de commercants actifs, l'application etant encore en phase de developpement.

## Ordre recommande de livraison

1. `BX-EP10-01` et `BX-EP10-02`
2. `PRD-046`

   - Statut : `Termine`
3. `PRD-047`

   - Statut : `Termine`
4. `PRD-048A`

   - Statut : `Termine`
5. `PRD-048`

   - Statut : `Termine`
6. `PRD-049`

   - Statut : `Termine`
7. `PRD-050`

   - Statut : `Termine`
8. `BX-EP10-03`, `BX-EP10-04`, `BX-EP10-05` en continu

## Proposition de tickets implementables

- `EP10-T01` Ajouter les tables `identifiants_commercant` et `tokens_acces_commercant`.
- `EP10-T02` Ajouter les modeles domaine et ORM d'identifiants commercant.
- `EP10-T03` Ajouter le repository d'identifiants commercant.
- `EP10-T04` Ajouter le service de hash de mot de passe.
- `EP10-T04B` Ajouter la configuration du cout bcrypt.
- `EP10-T04C` Ajouter la denylist locale minimale de mots de passe faibles.
- `EP10-T05` Implementer `AuthentifierCommercantParMotDePasse`.
- `EP10-T06` Ajouter `POST /commercants/auth/login`.
- `EP10-T07` Implementer `DemanderReinitialisationMotDePasseCommercant`.
- `EP10-T08` Ajouter les configurations d'URL front d'initialisation et de reinitialisation de mot de passe commercant.
- `EP10-T08B` Ajouter les templates email d'initialisation et de reinitialisation.
- `EP10-T09` Ajouter `POST /commercants/auth/mot-de-passe-oublie`.
- `EP10-T10` Implementer `InitialiserAccesCommercant`.
- `EP10-T11` Ajouter `POST /commercants/auth/initialiser-mot-de-passe`.
- `EP10-T12` Implementer `ReinitialiserMotDePasseCommercant`.
- `EP10-T13` Ajouter `POST /commercants/auth/reinitialiser-mot-de-passe`.
- `EP10-T14` Implementer `MettreAJourMotDePasseCommercant`.
- `EP10-T15` Ajouter `POST /commercants/me/mot-de-passe`.
- `EP10-T16` Revoquer les sessions apres changement ou reset de mot de passe.
- `EP10-T17` Ajouter le pilotage SQLAdmin des acces commercant.
- `EP10-T18` Supprimer les endpoints, schemas et use cases `qr_commercant`.
- `EP10-T19` Supprimer la generation de carte QR commercant dans `ReferencerCommercant`.
- `EP10-T20` Nettoyer la documentation produit et technique des references au `qr_commercant`.
- `EP10-T21` Ajouter la table et le service de rate limiting applicatif login et mot de passe oublie.
- `EP10-T22` Ajouter les audits `auth.login.success`, `auth.login.failed`, `password.reset.requested`, `password.reset.succeeded`, `password.init.requested`, `password.init.succeeded`, `auth.login.updated`, `account.locked`, `account.unlocked`.
