# Backlog Epic 32 - Live tracking WebPush commercants

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre aux commercants qui l'activent sur leur profil d'etre notifies en temps quasi reel lorsqu'un achat confirme de coffret contient au moins une de leurs prestations actives.
- Decision produit : le live tracking est une fonctionnalite opt-in cote commercant, activee depuis l'application commercant ou le profil commercant, avec preference portee par `profils_commercants`.
- Decision technique : la notification est de type `WebPush`, pilotee par l'application commercant via ses abonnements push, et orchestree cote backend par une outbox dediee.
- Decision operationnelle : l'achat confirme cree des notifications WebPush tracees, relancables et auditables, sans exposer de donnees client non necessaires.
- Decision MVP : la notification est declenchee a la confirmation de paiement/achat, pas a l'ouverture de checkout.
- Decision payload : le payload WebPush contient uniquement un deep link applicatif opaque ; les identifiants `achat_id` et `coffret_id` restent cote serveur.
- Decision batch : l'envoi WebPush est ordonnance automatiquement comme les batchs email/SMS.
- Decision V2 : les ouvertures et interactions push sont trackees en V2, hors MVP.
- Decision exploitation : la fonctionnalite est pilotable par feature flag backend `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED`.

## Probleme

Les commercants n'ont pas aujourd'hui de signal temps reel lorsqu'un coffret contenant leur prestation est achete. Ils peuvent consulter leur dashboard operationnel, mais cette lecture reste retrospective et depend d'une action volontaire.

Pour les partenaires actifs, un signal d'achat peut renforcer l'engagement, donner de la visibilite sur la demande locale et inciter a maintenir leur profil et leurs prestations a jour.

## Risque business

- Les commercants percoivent moins bien la valeur apportee par Localeo entre deux validations de prestation.
- Les achats de coffrets contenant leurs offres restent invisibles jusqu'a consultation du dashboard ou jusqu'au passage client.
- Les partenaires actifs peuvent manquer de signaux positifs sur la dynamique commerciale.
- Une notification mal ciblee peut creer de la confusion si elle concerne un coffret ou une prestation non active.

## Risque technique

- Envoi direct WebPush depuis le parcours achat, avec risque de ralentir ou fragiliser la confirmation de paiement.
- Multiplication de notifications si plusieurs prestations du meme commercant sont dans un meme coffret.
- Abonnements WebPush expires, revoques ou invalides non nettoyes.
- Exposition de donnees client dans le payload push.
- Rejeu de webhook paiement produisant des notifications en double.
- Dependances fortes entre application commercant, backend et provider WebPush si le contrat n'est pas stable.

## Perimetre MVP

- Ajouter une preference commercant `live_tracking_achats_active` ou equivalente.
- Permettre a l'application commercant d'activer/desactiver le live tracking dans le profil commercant.
- Permettre a l'application commercant d'enregistrer, lister et revoquer ses abonnements WebPush.
- Stocker les abonnements WebPush par commercant et par device/navigateur.
- Detecter les commercants eligibles lors d'un achat confirme :
  - le coffret achete contient au moins une prestation active du commercant ;
  - le commercant est actif ;
  - la preference live tracking est activee ;
  - au moins un abonnement WebPush actif existe.
- Creer une notification WebPush par commercant eligible et par achat confirme, pas par prestation.
- Regrouper dans la notification le nombre de prestations du commercant presentes dans le coffret si necessaire.
- Envoyer via une outbox `webpush_sortants` ou modele equivalent, separee du parcours synchrone de paiement.
- Historiser statut, provider/resultat, erreurs, tentatives et date d'envoi.
- Nettoyer ou desactiver les abonnements invalides retournes par le service WebPush.
- Afficher les notifications WebPush dans le back-office exploitation et, si pertinent, dans la vision 360 commercant.

## Hors perimetre MVP

- Notification client final.
- Notification a l'activation de la `CoffretInstance` ou a la validation de prestation.
- Preferences avancees par coffret, prestation, ville ou type d'evenement.
- Digest quotidien ou hebdomadaire.
- Segmentation marketing ou campagnes push.
- Conversations push bidirectionnelles.
- Notifications temps reel via WebSocket.
- Garantie stricte de livraison temps reel.
- Payload push contenant des donnees personnelles client.

## User Stories

1. `PRD-223` En tant que commercant, je veux activer le live tracking sur mon profil afin d'etre informe des achats de coffrets contenant mes prestations actives.
   - Statut : `Termine`
   - Resultat attendu : une preference explicite est disponible cote application commercant.
   - Resultat attendu : la preference est desactivee par defaut si aucune decision commercant n'existe.

2. `PRD-224` En tant qu'application commercant, je veux enregistrer un abonnement WebPush afin que le backend puisse notifier le device autorise.
   - Statut : `Termine`
   - Resultat attendu : l'API accepte endpoint, cles `p256dh` et `auth`, user-agent/device label si disponible.
   - Resultat attendu : l'abonnement est rattache au commercant authentifie et non a un identifiant fourni librement.

3. `PRD-225` En tant qu'application commercant, je veux revoquer un abonnement WebPush afin d'arreter les notifications sur un device donne.
   - Statut : `Termine`
   - Resultat attendu : l'abonnement peut etre desactive par endpoint ou identifiant interne.
   - Resultat attendu : la deconnexion ou la suppression du consentement push peut revoquer l'abonnement.

4. `PRD-226` En tant que systeme, je veux identifier les commercants concernes par un achat confirme afin de notifier uniquement les partenaires pertinents.
   - Statut : `Termine`
   - Resultat attendu : seuls les commercants actifs avec prestation active dans le coffret achete sont eligibles.
   - Resultat attendu : un commercant n'est notifie qu'une fois par achat, meme s'il a plusieurs prestations dans le coffret.

5. `PRD-227` En tant que systeme, je veux creer une notification WebPush outbox lors d'un achat confirme afin de ne pas ralentir le parcours paiement.
   - Statut : `Termine`
   - Resultat attendu : l'achat confirme cree les lignes `webpush_sortants` ou equivalent dans la meme logique outbox que email/SMS.
   - Resultat attendu : l'idempotence empeche les doublons sur rejeu du webhook ou reprise de paiement.

6. `PRD-228` En tant que commercant, je veux recevoir une notification sobre et utile afin de comprendre qu'un coffret contenant mon offre vient d'etre achete.
   - Statut : `Termine`
   - Resultat attendu : le message indique le coffret achete et le nombre de prestations concernees.
   - Resultat attendu : aucune donnee personnelle client n'est incluse dans le payload push.
   - Resultat attendu : un lien applicatif ouvre le dashboard commercant ou le detail d'activite autorise.

7. `PRD-229` En tant qu'exploitant, je veux superviser les notifications WebPush afin de diagnostiquer les incidents de livraison.
   - Statut : `Termine`
   - Resultat attendu : le back-office affiche statut, date, commercant, achat/coffret rattache, tentatives et erreur.
   - Resultat attendu : les notifications en echec peuvent etre distinguees des abonnements invalides.

8. `PRD-230` En tant que responsable securite, je veux que les abonnements WebPush soient proteges afin d'eviter l'usurpation ou la fuite de donnees.
   - Statut : `Termine`
   - Resultat attendu : les APIs de gestion WebPush et de resolution du deep link exigent une session commercant valide.
   - Resultat attendu : la reception technique d'une notification ne cree pas de session commercant.
   - Resultat attendu : les endpoints push sont stockes comme donnees sensibles et ne sont pas exposes en clair dans les logs.
   - Resultat attendu : les abonnements sont revoques lors de suspension du commercant si necessaire.

9. `PRD-231` En tant que systeme, je veux nettoyer les abonnements invalides afin de limiter les echecs repetes.
   - Statut : `Termine`
   - Resultat attendu : un retour provider d'abonnement expire/invalide desactive l'abonnement concerne.
   - Resultat attendu : les envois suivants ignorent les abonnements inactifs.

10. `PRD-232` En tant que responsable produit, je veux cadrer les evenements notifiables afin d'eviter une surcharge de notifications.
    - Statut : `Termine`
    - Resultat attendu : le MVP couvre uniquement l'achat confirme d'un coffret contenant une prestation active du commercant.
    - Resultat attendu : activation, expiration, validation de prestation et feedback restent hors MVP.

## Regles de gestion

- Le live tracking WebPush est inactif si le feature flag `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED` est desactive.
- Quand le feature flag est desactive, les APIs commercant de preference et d'abonnements WebPush refusent l'activation ou la creation de nouvel abonnement.
- Quand le feature flag est desactive, un achat confirme ne cree aucune ligne `webpush_sortants`.
- Quand le feature flag est desactive, le batch WebPush n'envoie aucune notification et retourne un resultat explicite `feature_disabled`.
- Le feature flag est evalue cote backend sur les points d'entree metier, pas uniquement dans l'IHM.
- Le live tracking est opt-in cote commercant.
- Un commercant suspendu, archive ou non actif ne recoit pas de notification live tracking.
- Une prestation non active ne rend pas le commercant eligible.
- L'evenement declencheur MVP est l'achat confirme apres paiement valide.
- Un achat confirme ne doit produire au maximum qu'une notification live tracking par commercant.
- Un rejeu technique de l'evenement achat ne doit pas produire de doublon.
- La notification ne doit jamais exposer email, telephone, nom ou prenom client.
- La notification peut exposer le nom du coffret et un indicateur de volume de prestations concernees.
- Le payload envoye au navigateur ne doit contenir ni `achat_id`, ni `coffret_id`, ni autre reference metier directe ; il contient uniquement un deep link opaque resolu cote application/backend.
- La reception d'une notification WebPush ne requiert pas de session commercant active et ne doit jamais initialiser une session.
- Au clic sur la notification, l'application ouvre le deep link opaque ; si aucune session commercant locale n'est valide, elle demande une authentification avant d'appeler l'API de resolution.
- L'API de resolution du deep link verifie la session commercant, le rattachement de la reference opaque au commercant authentifie et l'expiration de la reference.
- L'envoi WebPush ne doit pas etre synchrone avec la confirmation de paiement.
- Les abonnements WebPush sont rattaches au commercant authentifie.
- Les abonnements invalides doivent etre desactives automatiquement quand le provider le signale.
- La desactivation de la preference live tracking n'efface pas l'historique d'envoi.
- La suppression/revocation d'un abonnement n'efface pas l'historique d'envoi, mais doit supprimer rapidement les secrets permettant d'envoyer a nouveau.
- Les notifications doivent etre auditables depuis le back-office.
- Le batch WebPush est ordonnance automatiquement selon la meme logique d'exploitation que les batchs email/SMS, avec route interne relancable pour reprise incident.

## Modele de donnees cible

### Preference live tracking

Table cible : `profils_commercants`

- `live_tracking_achats_active BOOLEAN NOT NULL DEFAULT FALSE`
- `live_tracking_achats_active_at`
- `live_tracking_achats_desactive_at`

Le champ de preference commercant ne remplace pas le feature flag global : la notification exige a la fois `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED=true` et `live_tracking_achats_active=true`.

### Abonnement WebPush

Table cible : `abonnements_webpush_commercants`

- `id`
- `commercant_id`
- `endpoint_hash`
- `endpoint_chiffre` ou `endpoint`
- `p256dh`
- `auth`
- `device_label`
- `user_agent`
- `actif`
- `date_creation`
- `date_derniere_utilisation`
- `date_revocation`
- `motif_revocation`
- `date_purge_secrets`

Apres revocation ou invalidation definitive, `endpoint_chiffre` ou `endpoint`, `p256dh` et `auth` sont supprimes ou rendus inutilisables. La ligne peut rester temporairement pour audit avec `endpoint_hash`, dates et motif.

### Outbox WebPush

Table cible : `webpush_sortants`

- `id`
- `type_notification` : `ACHAT_COFFRET_CONTENANT_PRESTATION`
- `commercant_id`
- `achat_id`
- `coffret_id`
- `statut` : `A_ENVOYER`, `EN_COURS_ENVOI`, `ENVOYE`, `ECHEC_TEMPORAIRE`, `ECHEC_DEFINITIF`, `ANNULE`
- `titre`
- `corps`
- `payload`
- `date_creation`
- `date_planifiee`
- `date_envoi`
- `nb_tentatives`
- `erreur_derniere`
- `correlation_id`

Les colonnes `achat_id` et `coffret_id` sont reservees au serveur pour l'idempotence, le diagnostic et le back-office. Elles ne sont pas transmises dans le payload WebPush.

Contrainte recommandee :
- unicite metier sur `(type_notification, commercant_id, achat_id)` pour garantir l'idempotence.

### Retention cible

- Abonnements WebPush revoques ou invalides : desactivation immediate et suppression des secrets d'envoi au plus tard sous 7 jours, idealement au moment de la revocation.
- Trace non sensible d'abonnement revoque : conservation recommandee 90 jours avec `endpoint_hash`, `commercant_id`, dates et motif, puis purge ou anonymisation.
- Notifications `webpush_sortants` : conservation operationnelle 90 jours pour support, audit et diagnostic, puis purge ou anonymisation du payload et des erreurs detaillees.
- Les durees doivent etre configurables, par exemple `LOCALEO_WEBPUSH_ABONNEMENT_REVOQUE_RETENTION_DAYS=90` et `LOCALEO_WEBPUSH_SORTANT_RETENTION_DAYS=90`.
- Les payloads et logs ne doivent pas contenir de donnees personnelles client ; les erreurs provider sont tronquees si elles exposent endpoint ou materiel d'abonnement.

## APIs cibles

### Preferences live tracking

- `GET /protected/commercants/me/notifications/preferences`
- `PATCH /protected/commercants/me/notifications/preferences`
- Scope : session commercant.
- Si le feature flag global est desactive, `GET` expose un etat non disponible et `PATCH` refuse l'activation.

Payload cible :

```json
{
  "live_tracking_achats_active": true
}
```

### Abonnements WebPush

- `GET /protected/commercants/me/webpush/abonnements`
- `POST /protected/commercants/me/webpush/abonnements`
- `DELETE /protected/commercants/me/webpush/abonnements/{abonnement_id}`
- Scope : session commercant.
- Si le feature flag global est desactive, `POST` refuse la creation d'un nouvel abonnement et `GET` peut rester disponible pour afficher l'etat existant.

Payload cible de creation :

```json
{
  "endpoint": "https://push.example/subscription",
  "keys": {
    "p256dh": "...",
    "auth": "..."
  },
  "device_label": "Chrome mobile"
}
```

### Resolution deep link WebPush

- `POST /protected/commercants/me/webpush/deeplinks/resoudre`
- Scope : session commercant.
- La reference opaque est refusee si elle est inconnue, expiree, deja invalidee ou rattachee a un autre commercant.
- Si l'application n'a pas de session valide au clic, elle authentifie le commercant avant d'appeler cette API.

### Batch d'envoi WebPush

- `POST /protected/webpush/batch/envoyer?limit=100`
- Scope : `internal:batch`
- Route relancable manuellement pour reprise incident, mais ordonnancee automatiquement en production comme email/SMS.

## Payload WebPush cible

```json
{
  "type": "ACHAT_COFFRET_CONTENANT_PRESTATION",
  "title": "Un coffret contenant votre offre vient d'etre achete",
  "body": "Coffret Decouverte locale - 1 prestation chez vous",
  "deeplink": "localeo://commercant/live-tracking/{opaque_reference}"
}
```

Le payload ne doit pas contenir de donnee personnelle client, ni identifiant `achat_id` ou `coffret_id`. La reference opaque est resolue cote application/backend sous session commercant.

## Back-office cible

- Ajouter une vue `WebPush sortants`.
- Ajouter une vue ou section `Abonnements WebPush commercants`.
- Afficher les notifications WebPush recentes dans la vision 360 commercant si disponible.
- Afficher les erreurs WebPush dans les alertes operationnelles si le volume devient significatif.

## Lots d'implementation

### Lot 1 - Cadrage et modele

- Definir le modele preference live tracking.
- Definir le modele abonnement WebPush.
- Definir le modele outbox WebPush.
- Definir les statuts et contraintes d'idempotence.
- Ajouter la configuration `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED`, desactivee par defaut hors environnement explicitement autorise.

### Lot 2 - APIs commercant

- Ajouter lecture/mise a jour des preferences.
- Ajouter creation/liste/revocation des abonnements WebPush.
- Ajouter validation des payloads WebPush.
- Ajouter tests de securite session commercant.

### Lot 3 - Detection des commercants eligibles

- Brancher le declenchement sur l'achat confirme.
- Verifier le feature flag avant toute detection et creation outbox.
- Identifier les prestations actives du coffret.
- Grouper par commercant.
- Filtrer par statut commercant, preference et abonnement actif.
- Creer les lignes outbox idempotentes.

### Lot 4 - Provider WebPush et batch

- Ajouter le service d'envoi WebPush.
- Ajouter le batch d'envoi automatiquement ordonnance, avec route interne de reprise.
- Verifier le feature flag dans le batch avant tout envoi provider.
- Gerer retries, echecs definitifs et abonnements invalides.
- Ajouter logs et audit sans exposer les endpoints complets.
- Ajouter la purge des secrets d'abonnements revoques et la retention des notifications WebPush.

### Lot 5 - Back-office et observabilite

- Ajouter vues SQLAdmin WebPush.
- Ajouter compteurs dashboard si necessaire.
- Ajouter vision 360 commercant.
- Ajouter documentation operationnelle.

### Lot 6 - V2 tracking interactions push

- Tracker `OUVERT`, clic ou interaction push quand l'application commercant remonte l'evenement.
- Ajouter une table d'evenements WebPush ou un modele equivalent si le volume ou les analyses l'exigent.
- Ne pas bloquer le MVP sur ce tracking.

### Lot 7 - Tests

- Tester preference opt-in/opt-out.
- Tester creation/revocation abonnement.
- Tester achat confirme avec un commercant eligible.
- Tester achat confirme avec plusieurs prestations du meme commercant.
- Tester absence de notification si preference inactive.
- Tester absence de notification si prestation ou commercant inactif.
- Tester idempotence sur rejeu achat.
- Tester desactivation abonnement invalide.

## Definition of Done

- Un commercant peut activer/desactiver le live tracking.
- L'application commercant peut enregistrer et revoquer un abonnement WebPush.
- La fonctionnalite peut etre coupee globalement via `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED`.
- Un achat confirme de coffret contenant une prestation active cree une notification pour chaque commercant eligible.
- Un commercant n'est notifie qu'une fois par achat.
- Les notifications passent par une outbox WebPush et un batch d'envoi.
- Les abonnements invalides sont desactives.
- Aucun payload push ne contient de donnee personnelle client, ni `achat_id`, ni `coffret_id`.
- Le batch WebPush est ordonnance automatiquement comme les batchs email/SMS.
- Les secrets des abonnements revoques sont supprimes selon la politique de retention.
- Les envois, echecs et retries sont visibles en back-office.
- L'idempotence empeche les doublons sur rejeu d'evenement.
- Les tests couvrent preference, abonnement, detection, envoi et idempotence.

## Points arbitres restants

- Aucun point en suspens identifie a ce stade.
