# API

## Contrat local

Le contrat local attendu par les consommateurs est `api/localeo-openapi.json`, dans le dépôt commerçant. Ce fichier est actuellement absent ; voir [la source des contrats et la limite de validation](#source-des-contrats--pro-012). La convention de routage est :

- `/public/{domaine}/*` : endpoints publics sans authentification.
- `/protected/{domaine}/*` : endpoints app avec session commercant ou token applicatif selon l'endpoint.
- `/internal/*` : endpoints back-office admin.

Le front utilise `LOCALEO_API_BASE_URL` comme base locale, puis ajoute ces prefixes et les domaines metier (`identite-acces`, `referencement`, `commercialisation`, `exploitation`, `support`, `gestion-achats`, `gestion-reversement`, `profils`, `dam`). En developpement, `/api` est reecrit par Vite vers `VITE_PROXY_TARGET`.

## Endpoints utilises par la PWA commercant

### Authentification

`POST /protected/identite-acces/commercants/auth/login`
- ouvre une session commercant avec login et mot de passe.

`POST /protected/identite-acces/commercants/auth/mot-de-passe-oublie`
- declenche l'envoi d'un lien de reinitialisation.

`POST /protected/identite-acces/commercants/auth/initialiser-mot-de-passe`
- initialise le mot de passe depuis un token d'activation.

`POST /protected/identite-acces/commercants/auth/reinitialiser-mot-de-passe`
- reinitialise le mot de passe depuis un token.

`GET /protected/identite-acces/commercants/session/valider`
- verifie la session commercant courante.

`POST /protected/identite-acces/commercants/session/{session_id}/invalider`
- invalide une session commercant.

### Profil, prestations et reversements

`GET /protected/profils/commercants/me`
- recupere le profil du commercant connecte.

`PATCH /protected/referencement/commercants/me/contact`
- met a jour les coordonnees de contact du commercant connecte.

`POST /protected/identite-acces/commercants/me/mot-de-passe`
- modifie le mot de passe du commercant connecte.

`GET /protected/commercialisation/commercants/{commercant_id}/prestations`
- liste les prestations du commercant.

`GET /protected/commercialisation/commercants/{commercant_id}/prestations/{prestation_id}`
- recupere le detail d'une prestation commercant.

`PATCH /protected/profils/commercants/me/prestations/{prestation_id}`
- met a jour le contenu editable d'une prestation.

`GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mouvements/a-reverser`
- La colonne `Version à l’achat` utilise `prestation_version`, figée sur le statut de prestation de l’instance achetée. Elle n'utilise jamais `prestation_version_courante` ; une version d'achat absente s'affiche `Non renseignée`.
- Ce champ nécessite le déploiement du backend qui l'expose. Le frontend reste compatible avec une réponse ancienne sans ce champ, sans afficher la version courante à sa place.
- liste les mouvements de reversement en attente.

`GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mois/{nb_mois}`
- liste l'historique des reversements.

### Stripe Connect

`GET /protected/referencement/commercants/me/stripe-connect`
- consulte le statut d'onboarding, les capacites Stripe et l'eligibilite du commercant connecte.
- reponse attendue : `stripe_onboarding_statut`, `stripe_charges_enabled`, `stripe_payouts_enabled`, `stripe_requirements_due`, `stripe_disabled_reason` et `stripe_connect_eligible`.

`POST /protected/referencement/commercants/me/stripe-connect/onboarding`
- cree ou retrouve le compte Stripe Express et genere un lien d'onboarding temporaire.
- le front redirige uniquement vers `onboarding_url` et ne conserve pas cette URL.

`POST /protected/referencement/commercants/me/stripe-connect/synchroniser`
- resynchronise le compte connecte apres un retour Stripe ou une action explicite du commercant.
- le retour Stripe ne suffit jamais a conclure que le compte est eligible.

La route `POST /protected/gestion-reversement/reversements/campagnes-stripe/lancer` du contrat est reservee a une cle `X-API-KEY` avec le scope `internal:finance`. Elle ne doit pas etre appelee depuis la PWA commercant.

### Contact Localeo

`GET /public/support/contacts/motifs?cible=COMMERCANT`
- liste les motifs actifs proposés au commerçant.

`POST /protected/support/commercants/{commercant_id}/messages`
- crée un nouveau fil de contact depuis la session commerçant.

`GET /protected/support/commercants/{commercant_id}/messages`
- liste les fils et messages de contact du commerçant.

`GET /protected/support/commercants/{commercant_id}/messages/{thread_id}`
- récupère les messages d'un fil de discussion.

`POST /protected/support/commercants/{commercant_id}/messages/{thread_id}/reponses`
- ajoute une réponse commerçant dans un fil existant.

### Validation de prestation

`POST /protected/exploitation/validation/ouvrir-transaction`
- ouvre une transaction à partir du corps JSON `{ "qr_coffret_instance": "…" }`, avec Bearer commerçant. Aucun QR dans la query.
- reponse attendue : `transaction_id`, `achat_id`, `coffret_instance_id`, `date_expiration`, `statut`.

`GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}`
- recupere le recap de l'instance de coffret.

`GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`
- liste les statuts de prestations de l'instance de coffret.
- Avec une session commerçant, cette liste ne contient que ses propres prestations. Elle ne permet pas de calculer la progression globale : utiliser le `statut` de l'instance du coffret pour son état global et le relire après une mutation.

`GET /public/commercialisation/coffrets/{coffret_id}`
- recupere le detail public du coffret et les libelles de prestations.

`POST /protected/exploitation/validation/valider-prestation?transaction_id=...&statut_prestation_coffret_instance_id=...`
- finalise la validation d'une prestation pour la session commercant.
- le front n'envoie plus de `qr_commercant`.

`POST /protected/exploitation/validation/validations/{validation_prestation_id}/annuler`
- annule une validation de prestation recente pour la session commercant.
- corps attendu : `{ "motif": "...", "commentaire": "..." }`.
- le delai d'affichage cote front est configure par `LOCALEO_VALIDATION_PRESTATION_API_ANNULATION_MAX_HOURS`, avec `24` heures par defaut.
- l'autorisation finale reste controlee par le backend.

### Notifications WebPush

`GET /protected/exploitation/commercants/me/notifications/preferences`
- recupere les preferences de notification du commercant connecte, dont `live_tracking_achats_active`.

`PATCH /protected/exploitation/commercants/me/notifications/preferences`
- active ou desactive la preference de live tracking achats.
- corps attendu : `{ "live_tracking_achats_active": true }`.

`GET /protected/exploitation/commercants/me/webpush/abonnements`
- liste les abonnements WebPush connus pour le commercant connecte.

`POST /protected/exploitation/commercants/me/webpush/abonnements`
- enregistre l'abonnement navigateur de l'appareil courant.
- corps attendu : `endpoint`, `keys`, `device_label` et `user_agent`.

`DELETE /protected/exploitation/commercants/me/webpush/abonnements/{abonnement_id}`
- supprime l'abonnement WebPush d'un appareil.

`POST /protected/exploitation/commercants/me/webpush/deeplinks/resoudre`
- resout un deeplink opaque issu d'une notification WebPush apres authentification.
- corps attendu : `{ "deeplink": "localeo://commercant/live-tracking/{opaque_reference}" }`.

## Contraintes metier

- une validation porte sur une prestation liee a une instance de coffret.
- la session commercant est verifiee par `Authorization: Bearer <session_token>`.
- l'autorisation de valider une prestation reste controlee par le backend.
- les donnees bancaires et KYC sont collectees par Stripe, jamais par la PWA Localeo.
- l'URL d'onboarding Stripe est temporaire et ne doit pas etre stockee localement.
- le QR client/coffret sert a ouvrir la transaction ; la session Bearer autorise la validation sans rescanner la carte commerçant. La connexion par carte reste un parcours alternatif.
- le WebPush est active volontairement par compte commercant et par appareil.
- une notification WebPush ne doit pas exposer de donnees personnelles, `achat_id`, `coffret_id` ou autre identifiant metier direct.
- le deeplink WebPush est opaque et resolu seulement avec une session commercant valide.


### Résolution de scan Animation — PRO-005

`POST /protected/animation-locale/commercants/me/participants/resoudre` : Bearer de scope `commercant:validation`, JSON `qr_token` (20 à 512 caractères). Réponse sans données personnelles : animation/commune, participant.reference, etapes limitées au commerce. Cache-Control: private, no-store. La validation reste une commande distincte sur `/protected/animation-locale/validations`.

La saisie manuelle accepte la valeur encodée dans le QR Coffret, l’URL du QR
Animation ou son identifiant opaque copié depuis la marketplace. Les espaces de
copie des tokens sont retirés et le padding Base64URL du QR Coffret signé est
rétabli avant envoi. Le QR Coffret reste transmis dans `qr_coffret_instance`,
l’identifiant Animation dans `qr_token`, sous session commerçant. Le serveur
conserve les contrôles de signature, expiration et révocation. La saisie ne
déclenche aucune consommation avant confirmation. Le code court de secours
Coffret ne remplace pas la valeur encodée dans le QR.

Le champ commerçant « Identifiant du QR code » correspond au bloc du même nom
affiché avec le QR du bénéficiaire. Il reste disponible lorsque la caméra est
indisponible ; la validation de la prestation ou de l’étape reste à confirmer.

### Source des contrats — PRO-012

L'[exporteur du dépôt commerçant](../../../../localeo-commercant/scripts/export-openapi.py) utilise `localeo-backend/app.main:app` via le [lanceur isolé](../../../../localeo-backend/scripts/validation/test_isolated.py), sans charger dotenv ni ouvrir de connexion réseau. Il écrit uniquement `api/localeo-openapi.json` ; aucune copie `docs/openapi.json` n'est produite.

Constat au 18 septembre 2026 : le fichier et son dossier `api/` sont absents après leur suppression dans le dépôt commerçant. [contracts.test.js](../../../../localeo-commercant/src/lib/api/contracts.test.js) importe toujours le fichier, et [check-deployment.mjs](../../../../localeo-commercant/scripts/check-deployment.mjs) le lit pour comparer un déploiement. Ces contrôles ne peuvent pas être déclarés réussis en cet état.

L'exporteur nécessite les dépendances Python du backend voisin et un dossier de sortie existant : il ne crée pas `api/`. Les prérequis sont dans le [README commerçant](../../../../localeo-commercant/README.md#contrat-openapi-manquant). Le [contrat documentaire canonique EPIC 41](../epic-41-api/openapi.json) reste consultable, mais les consommateurs ci-dessus ne le chargent pas automatiquement. Cette mise à jour ne restaure ni ne génère d'artefact. Un export décrit le code local ; il ne prouve pas son déploiement.

### Contrat signé du commerçant

Dans « Mes informations », la section « Mon contrat » charge les documents par
GET /protected/documentaire/commercants/documents (Bearer, scope commercant:profil).
Elle conserve les types CONTRAT_COMMERCANT et CONVENTION_COMMERCANT non archivés.
Les scans OnBoard sont déposés au statut BROUILLON : ce statut n’empêche pas leur
accès. Le téléchargement utilise GET /protected/documentaire/commercants/documents/{document_id}/download,
avec la même session, et enregistre le fichier original sous son nom documentaire.
Le serveur contrôle le rattachement au commerçant. Aucun modèle public de contrat
ne remplace le document personnel ; l’absence et les erreurs restent explicites.
Raccourci « Mon contrat » dans le menu Compte et dans la préparation du compte.
