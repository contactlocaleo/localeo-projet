# Spécification technique - Epic 10 - Authentification commerçant login / mot de passe

## Objectif

Remplacer le parcours d'authentification commerçant par QR code dans la PWA `localeo-commercant` par une authentification login / mot de passe, puis ajouter les parcours :

- mot de passe oublie ;
- initialisation du premier mot de passe depuis un lien email ;
- réinitialisation du mot de passe depuis un lien email ;
- mise à jour du mot de passe depuis une session commerçant valide.

La session commerçant existante reste le mécanisme d'autorisation des appels métier : token opaque, expiration, scopes, validation serveur et invalidation explicite.

## Perimêtre front

### Inclus

- Remplacer l'écran `MerchantAuthenticationGate` de scan QR commerçant par un écran de connexion.
- Ajouter des vues front pour les trois parcours publics non connectés :
  - demande de réinitialisation ;
  - définition du premier mot de passe ;
  - définition d'un nouveau mot de passe après oubli.
- Ajouter une vue connectée pour changer le mot de passe.
- Conserver la vérification de session via `GET /commercants/session/valider`.
- Conserver l'invalidation de session via `POST /commercants/session/{session_id}/invalider`.
- Nettoyer les messages UI qui demandent de rescanner le QR commerçant.
- Ne plus stocker `qr_commercant` dans `sessionStorage`.

### Hors périmètre front

- Hashage, rate limiting, audit, tokens emails et verrouillage compte, traités côté backend.
- Back-office SQLAdmin.
- QR client / QR pack instance, qui restent utilisés pour ouvrir une transaction de validation.

## Decisions validees

- Les liens email utilisént des query params front : `?mode=...&token=...`.
- Les endpoints backend Epic 10 sont disponibles dans l'environnement utilisé par la PWA, meme si `api/localeo-openapi.json` peut ne pas encore tous les lister.
- Le front affiche une jauge de politique mot de passe, tout en laissant le backend appliquer la validation définitive.

## État actuel constate

Le projet front est une PWA React/Vite compacte :

- `src/App.jsx` contient le shell, les appels API, l'authentification, le menu et les parcours métier.
- `src/styles.css` contient les styles globaux.
- La session est stockee dans `window.sessionStorage` sous la cle `localeo-merchant-session`.
- L'ouverture de session actuelle appelle `POST /commercants/session/ouvrir` avec `{ qr_commercant }`.
- La validation de prestation dans le front appelle encore `POST /validation/valider-prestation` avec `transaction_id`, `statut_prestation_pack_instance_id` et `qr_commercant`.
- Le contrat OpenAPI local cible n'attend plus `qr_commercant` : il attend `transaction_id`, `statut_prestation_coffret_instance_id` et `Authorization`.

## Contrats API requis

### Connexion

`POST /commercants/auth/login`

Requête :

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

Le front normalisé seulement les espaces de saisie (`trim`) et laisse la validation métier au backend. Le message d'erreur affiche doit rester non enumerant.

### Mot de passe oublié

`POST /commercants/auth/mot-de-passe-oublie`

Requête :

```json
{
  "login": "contact@commerce.fr"
}
```

Reponse attendue `202` :

```json
{
  "message": "Si le compte est eligible, un email de reinitialisation sera envoye."
}
```

Le front affiche toujours un état de confirmation generique lorsque la réponse est acceptee.

### Initialisation du premier mot de passe

`POST /commercants/auth/initialiser-mot-de-passe`

Requête :

```json
{
  "token": "token-brut-recu-par-email",
  "nouveau_mot_de_passe": "nouveau-mot-de-passe"
}
```

Reponse attendue `204`.

Le token est lu depuis l'URL front en query param :

```text
?mode=initialisation-mot-de-passe&token=<token>
```

Le front ne persiste pas ce token.

### Réinitialisation du mot de passe

`POST /commercants/auth/reinitialiser-mot-de-passe`

Requête :

```json
{
  "token": "token-brut-recu-par-email",
  "nouveau_mot_de_passe": "nouveau-mot-de-passe"
}
```

Reponse attendue `204`.

Le token est lu depuis l'URL front en query param :

```text
?mode=reinitialisation-mot-de-passe&token=<token>
```

Le front ne persiste pas ce token.

Après succès, le front redirige vers la connexion avec un message invitant à se connecter avec le nouveau mot de passe.

### Mise à jour du mot de passe connecté

`POST /commercants/me/mot-de-passe`

Headers :

```http
Authorization: Bearer <session_token>
Content-Type: application/json
```

Requête :

```json
{
  "mot_de_passe_courant": "mot-de-passe-actuel",
  "nouveau_mot_de_passe": "nouveau-mot-de-passe"
}
```

Reponse attendue `204`.

Après succès, toutes les sessions sont considerees révoquées. Le front supprime donc la session locale et retourne à la connexion.

## Contrat validation de prestation

Le contrat OpenAPI local de `POST /validation/valider-prestation` est déjà compatible avec le decommissionnement du QR commerçant.

Contrat cible constate :

```http
POST /validation/valider-prestation?transaction_id=...&statut_prestation_coffret_instance_id=...
Authorization: Bearer <session_token>
```

Le front actuel doit donc être aligne sur ce contrat :

- renommer le paramètre envoyé de `statut_prestation_pack_instance_id` vers `statut_prestation_coffret_instance_id` ;
- supprimer l'envoi de `qr_commercant` ;
- conserver l'envoi du bearer token via `Authorization`.

## Parcours UX cibles

### Connexion

1. Le commerçant arrive sur l'application sans session locale valide.
2. L'application affiche un formulaire avec :
   - login ;
   - mot de passe ;
   - action de connexion ;
   - lien vers mot de passe oublie.
3. À la soumission, le front appelle `POST /commercants/auth/login`.
4. En succès, le front stocke la session dans `sessionStorage` et affiche le menu.
5. En erreur, le front affiche un message non enumerant, sans distinguer login inconnu, mot de passe invalide, compte verrouillé ou compte non initialise.

### Mot de passe oublié

1. Depuis l'écran de connexion, le commerçant ouvre la vue "Mot de passe oublié".
2. Il saisit son login.
3. Le front appelle `POST /commercants/auth/mot-de-passe-oublie`.
4. Si l'API repond `202`, le front affiche une confirmation generique.
5. Si l'API repond `429` ou erreur technique, le front affiche un message opérationnel sans exposer l'existence du compte.

### Initialisation du premier mot de passe

1. Le commerçant ouvre le lien email d'initialisation.
2. Le front détecte le mode via l'URL `?mode=initialisation-mot-de-passe&token=...`.
3. Il affiche un formulaire nouveau mot de passe / confirmation.
4. Le front vérifie :
   - champs non vides ;
   - confirmation identique ;
   - longueur minimale connue si exposee côté front.
5. Le front affiche une jauge de politique mot de passe pour guider la saisie.
6. Le backend reste responsable de la politique définitive.
7. En succès, le front retire le token de l'état local et revient à la connexion.

### Réinitialisation après oubli

Parcours identique à l'initialisation, avec l'URL `?mode=reinitialisation-mot-de-passe&token=...`, mais appelant `POST /commercants/auth/reinitialiser-mot-de-passe`.

### Mise à jour connectée

1. Depuis le menu commerçant, ajouter une entrée "Modifier mon mot de passe".
2. La vue affiche :
   - mot de passe actuel ;
   - nouveau mot de passe ;
   - confirmation.
3. À la soumission, appeler `POST /commercants/me/mot-de-passe`.
4. En succès, supprimer la session locale et revenir à la connexion avec un message de confirmation.
5. En `401`/`403`, supprimer la session locale et revenir à la connexion.

## Gestion de session

La structure stockee reste proche de l'existant :

```json
{
  "session_token": "opaque-token",
  "expires_at": "2026-04-21T12:00:00Z",
  "scopes": ["commercant:session"],
  "session_id": "uuid-optionnel",
  "commercant": {
    "commercant_id": "uuid",
    "nom": "Commerce",
    "statut": "ACTIF"
  }
}
```

Changements :

- supprimer `qr_commercant` ;
- remplacer les messages "Veuillez rescanner votre QR code" par "Veuillez vous reconnecter" ;
- continuer a valider la session avant affichage du menu ;
- continuer a invalider la session distante lors de la deconnexion si `session_id` est connu.

## Changements techniques front proposes

### `src/App.jsx`

- Remplacer `openMerchantSession(qrValue)` par `loginMerchant({ login, password })`.
- Supprimer `validateMerchantQr`, `getMerchantQrDetectionState` et les usages de scan QR commerçant.
- Conserver les helpers QR pack (`getPackQrDetectionState`, scanner pack) pour la validation client.
- Remplacer `MerchantAuthenticationGate` par `MerchantLoginGate`.
- Ajouter des composants internes :
  - `ForgotPasswordView` ;
  - `PasswordInitializationView` ;
  - `PasswordResetView` ;
  - `PasswordUpdateView`.
- Ajouter des fonctions API :
  - `requestMerchantPasswordReset(login)` ;
  - `initializeMerchantPassword({ token, newPassword })` ;
  - `resetMerchantPassword({ token, newPassword })` ;
  - `updateMerchantPassword({ currentPassword, newPassword, sessionToken })`.
- Adapter `confirmValidation` pour ne plus envoyer `qr_commercant` et pour utiliser `statut_prestation_coffret_instance_id`.

### `src/styles.css`

- Ajouter les styles du formulaire de connexion et des formulaires mot de passe.
- Reutiliser les conventions existantes de `validation-shell`, `validation-summary`, boutons et feedback.
- Retirer uniquement les styles devenus inutiles pour le scan QR commerçant si aucun autre écran ne les utilisé.

### Documentation

- Mettre à jour [docs/specification/specification-version-actuelle.md](../espace-commercant/README.md) après validation de la spec.
- Mettre à jour [docs/backlog/spec-validation-prestation-openapi-mapping.md](../validation-prestations/contrats-api.md), qui décrit encore l'ancien contrat avec `qr_commercant`.

## États et erreurs

Messages front recommandes :

- Login invalide : `Connexion impossible. Verifiez vos identifiants et reessayez.`
- Session expirée : `Votre session a expiré. Veuillez vous reconnecter.`
- Mot de passe oublié accepté : `Si un compte eligible correspond a ce login, un email va être envoye.`
- Token invalide ou expiré : `Ce lien n'est plus valide. Demandez un nouveau lien.`
- Mot de passe change : `Votre mot de passe a été mis à jour. Connectez-vous à nouveau.`

Le front ne doit jamais afficher le mot de passe, le token de reset ou un detail permettant d'enumerer les comptes.

## Strategie de livraison

1. Brancher le login/password sur `POST /commercants/auth/login`.
2. Remplacer les messages et le stockage de session pour supprimer `qr_commercant`.
3. Ajouter le parcours mot de passe oublie.
4. Ajouter les parcours initialisation et réinitialisation par token.
5. Ajouter la mise à jour du mot de passe connectée.
6. Adapter la validation de prestation au contrat OpenAPI local sans `qr_commercant`.
7. Nettoyer le code mort QR commerçant.

## Criteres d'acceptation front

- Un commerçant peut ouvrir une session avec login / mot de passe.
- Une session existante valide rouvre directement le menu.
- Une session expirée ou invalide renvoie vers la connexion.
- Le front ne demande plus de scanner ou saisir un QR commerçant pour s'authentifiér.
- Le front ne stocke plus `qr_commercant`.
- Le mot de passe oublie affiche une réponse generique.
- Les liens d'initialisation et de réinitialisation permettent de définir un mot de passe.
- Les formulaires de creation de mot de passe affichent une jauge de politique mot de passe.
- Le changement de mot de passe connecté révoqué localement la session et retourne à la connexion.
- Le QR pack/client reste disponible pour ouvrir la transaction de validation.
- La validation de prestation n'envoie plus de `qr_commercant`.





### PRO-004 — Déconnexion locale immédiate
La session mémoire, le stockage, le cache Animation et le contexte de validation sont supprimés avant la révocation réseau. La révocation utilise le délai HTTP borné de 15 secondes. Une erreur distante est signalée sans restaurer la session ni perturber une nouvelle connexion. L'expiration locale est contrôlée par temporisation et au retour du focus. Validation : 3 tests ciblés réussis (`src/lib/logout.test.js`, `src/app/useMerchantSession.test.jsx`). La révocation serveur reste vérifiée sous BACK-001.
