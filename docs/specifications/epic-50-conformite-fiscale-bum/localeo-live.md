# Epic 50 - Specification Localeo Live

## Statut et objectif

| Champ | Valeur |
| --- | --- |
| Application | Localeo Live |
| Epic | Epic 50 - Politique BUM et conformite fiscale |
| Statut du contrat | Socle notifications disponible, raccordement facture a implementer |
| Public | Beneficiaire d'un coffret suivi dans Localeo Live |
| Domaine | Notification et redirection vers les documents acheteur |

Le perimetre Epic 50 de Localeo Live est volontairement limite. Live informe
le beneficiaire lorsqu'une facture de prestation demandee devient disponible,
puis le redirige vers le detail securise porte par la Marketplace. Live ne
devient ni un espace Finance complet ni un outil de qualification BUM.

## Hors perimetre explicite

- qualification, validation ou requalification BUM ;
- saisie du profil fiscal d'un commercant ;
- traitement d'une demande par le commercant ;
- assistant d'emission de facture ;
- consultation ou utilisation du credit d'achat B2B ;
- consultation des factures de commission ou de souscription Localeo ;
- depot ou suivi operateur Chorus Pro ;
- stockage d'une copie persistante des documents PDF.

Ces fonctions appartiennent respectivement au BackOffice, a Localeo
Commercant, a la Marketplace Pro ou a Localeo Animation.

## Capacites attendues

1. Associer une installation Live a un coffret apres verification du token.
2. Permettre l'activation/desactivation de la categorie `FACTURATION`.
3. Recevoir une notification in-app et WebPush lorsqu'une facture est fournie.
4. Afficher l'etat lu/non lu et un badge de notifications.
5. Ouvrir un deep link interne sans inclure de secret.
6. Rediriger vers la vue facture de la Marketplace apres verification locale du
   token du coffret.
7. Gerer l'absence de permission WebPush sans perdre la notification in-app.

## Etat backend constate

Le backend expose deja :

- installations anonymes protegees par un secret ;
- preferences de categories et de villes ;
- abonnements WebPush ;
- suivi d'une ressource `COFFRET` apres verification du token ;
- boite de notifications paginee ;
- lecture unitaire et globale ;
- deep links et payloads structures.

En revanche, `DEFAULT_CATEGORIES` n'accepte actuellement que
`ACTUALITE_EDITORIALE`, `COFFRET`, `ANIMATION` et `GAIN`. Le service de demandes
de facture notifie l'acheteur par email mais ne cree pas de
`NotificationLocaleoLiveOrm`. La fonctionnalite Epic 50 n'est donc pas complete
dans Live tant que le raccordement decrit plus bas n'est pas livre.

## Installation et secret

Au premier demarrage :

1. Charger `GET /public/localeo-live/configuration`.
2. Creer l'installation par `POST /public/localeo-live/installations`.
3. Conserver `installation_id` et `installation_secret` dans le stockage local
   securise disponible pour la PWA.
4. Envoyer le secret uniquement dans `X-Localeo-Live-Secret`.
5. Proposer WebPush seulement si `webpush_enabled=true`, si une cle VAPID est
   presente et si le navigateur supporte le mecanisme.

Creation :

```json
{
  "categories_activees": {
    "ACTUALITE_EDITORIALE": true,
    "COFFRET": true,
    "ANIMATION": true,
    "GAIN": true,
    "FACTURATION": true
  },
  "ville_ids_suivies": []
}
```

`FACTURATION` est un ajout requis au contrat backend. Jusqu'a sa livraison, le
client conserve les categories retournees par le serveur et ne doit pas envoyer
une cle inconnue, sous peine de rejet metier.

La rotation utilise
`POST /public/localeo-live/installations/{installationId}/secret/rotation` et
remplace atomiquement le secret local. Une suppression de l'installation par
`DELETE .../installations/{installationId}` efface ensuite toutes les donnees
locales associees.

## Abonnement WebPush

Route : `POST /public/localeo-live/abonnements-webpush`.

```json
{
  "endpoint": "https://push-service/...",
  "keys": {
    "p256dh": "...",
    "auth": "..."
  },
  "installation_id": "uuid",
  "categories_activees": {},
  "ville_ids_suivies": []
}
```

Pour une installation existante, envoyer son secret dans le header. Le client
conserve `abonnement_id` afin de pouvoir revoquer uniquement l'abonnement avec
`DELETE /public/localeo-live/abonnements-webpush/{abonnementId}`.

Refuser les notifications navigateur ne desactive pas la boite in-app. L'ecran
de preferences distingue clairement `Notifications dans l'application` et
`Notifications systeme`.

## Associer un coffret a Live

Apres activation du coffret, appeler :

`POST /public/localeo-live/installations/{installationId}/suivis`

```json
{
  "type_ressource": "COFFRET",
  "ressource_id": "coffret-instance-uuid",
  "token": "token d'activation"
}
```

Le secret Live est envoye dans `X-Localeo-Live-Secret`. Le backend verifie le
token avant de creer le suivi. Le client conserve l'identifiant `suivi.id` et
peut supprimer l'association par `DELETE .../suivis/{suiviId}`.

Le token du coffret n'est jamais recopie dans la notification, le deep link,
les analytics ou les logs. Il reste necessaire pour consulter le passeport et
la facture dans le perimetre du coffret.

## Preferences

- Lire : `GET /public/localeo-live/installations/{installationId}/preferences` ;
- Modifier : `PUT /public/localeo-live/installations/{installationId}/preferences`.

Le client effectue une mise a jour complete de `categories_activees` et
`ville_ids_suivies`, en preservant les categories inconnues retournees par une
version plus recente du backend. La categorie `FACTURATION` est activee par
defaut pour une nouvelle installation, mais l'utilisateur peut la desactiver.

## Boite de notifications

Route paginee :

`GET /public/localeo-live/installations/{installationId}/notifications?limit=25&cursor=<date>`

Reponse :

```json
{
  "items": [{
    "id": "uuid",
    "categorie": "FACTURATION",
    "titre": "Votre facture est disponible",
    "corps": "La facture demandee est disponible dans votre espace.",
    "deeplink": "/live/coffrets/uuid/factures/demande-uuid",
    "payload": {
      "eventType": "FACTURE_PRESTATION_DISPONIBLE",
      "coffretInstanceId": "uuid",
      "invoiceRequestId": "uuid"
    },
    "statut": "ENVOYEE",
    "date_creation": "date ISO-8601",
    "date_envoi": "date ISO-8601",
    "lue_at": null
  }],
  "count": 1,
  "next_cursor": null
}
```

Le client trie selon l'ordre serveur, concatene les pages sans doublon par
`id` et n'utilise pas `count` comme total global. Le badge correspond au nombre
d'elements charges dont `lue_at=null`, complete si necessaire par une projection
serveur future.

Lecture :

- `POST .../notifications/{notificationId}/lecture` ;
- `POST .../notifications/lecture-globale`.

Un clic marque d'abord la notification comme lue, puis traite le deep link. Un
echec de lecture ne doit pas bloquer l'ouverture, mais il est retente au
prochain rafraichissement.

## Evenements Epic 50 a raccorder

Contrat minimal V1 :

| Evenement | Categorie | Cible | Effet client |
| --- | --- | --- | --- |
| `FACTURE_PRESTATION_DISPONIBLE` | `FACTURATION` | Installation suivant le coffret | Ouvrir la demande unitaire Marketplace |
| `FACTURE_GROUPEE_DISPONIBLE` | `FACTURATION` | Installation explicitement rattachee a l'achat Pro | Ouvrir le detail achat Pro |
| `FACTURE_PRESTATION_CORRIGEE` | `FACTURATION` | Meme cible que l'originale | Ouvrir la chronologie des documents |

Le raccordement backend doit :

1. ajouter `FACTURATION` aux categories autorisees ;
2. rechercher les installations actives qui suivent le `COFFRET` concerne ;
3. verifier que la preference `FACTURATION` est active ;
4. creer une notification in-app idempotente ;
5. laisser le batch WebPush existant envoyer la notification ;
6. conserver une `source_key` unique incluant type d'evenement, demande et
   version/document ;
7. ne rien creer pour une installation revoquee.

Exemple de contrat de production :

```json
{
  "categorie": "FACTURATION",
  "titre": "Votre facture est disponible",
  "corps": "La facture demandee est disponible dans votre espace Localeo.",
  "deeplink": "/live/coffrets/{coffretInstanceId}/factures/{invoiceRequestId}",
  "payload": {
    "eventType": "FACTURE_PRESTATION_DISPONIBLE",
    "coffretInstanceId": "uuid",
    "invoiceRequestId": "uuid"
  },
  "sourceKey": "FACTURE_PRESTATION_DISPONIBLE:{requestId}:{documentId}"
}
```

Le titre et le corps n'incluent ni montant, ni identite fiscale, ni numero de
facture, ni nom complet du beneficiaire. Ces donnees sont chargees seulement
apres authentification sur l'ecran cible.

## Deep link et redirection Marketplace

Route frontale proposee :

`/live/coffrets/:coffretInstanceId/factures/:invoiceRequestId`

Traitement :

1. Verifier que le coffret est suivi localement et qu'un token est disponible.
2. Sans token, afficher une action `Ouvrir mon lien d'activation` ; ne pas
   reveler les donnees de la demande.
3. Avec token, appeler la route de suivi Marketplace
   `GET /public/coffrets-instances/{instanceId}/demandes-facture`.
4. Verifier que `invoiceRequestId` appartient a la liste retournee.
5. Si le statut est `PROVIDED`, afficher l'action de telechargement Marketplace.
6. Sinon, afficher le statut courant sans inventer de date de disponibilite.

Le service worker ouvre ou focalise une fenetre appartenant a l'origine
autorisee. Il n'ouvre jamais directement une URL externe provenant du payload.
Un deep link non reconnu retourne a la boite de notifications.

## Comportement hors ligne

- La boite peut afficher les metadonnees deja chargees.
- Une notification non lue peut etre marquee localement comme en attente de
  synchronisation.
- Le document n'est pas telecharge ni mis en cache automatiquement.
- Le deep link affiche un etat hors ligne et reprend la verification au retour
  du reseau.
- Aucun statut financier ne doit etre deduit d'une donnee en cache obsolete.

## Gestion des erreurs

| Situation | Comportement |
| --- | --- |
| WebPush non supporte/refuse | Conserver les notifications in-app |
| Secret Live invalide (`401`) | Reinitialiser l'installation avec consentement |
| Coffret/token invalide (`401/403/404`) | Masquer le detail et proposer le lien d'activation |
| Notification inconnue | Retirer l'element local obsolete |
| Deep link inconnu | Ouvrir la boite, sans redirection externe |
| API indisponible | Afficher le cache et proposer un nouvel essai |

## Securite, confidentialite et accessibilite

- Stocker le secret Live et les tokens de coffret separement.
- Ne jamais inclure de secret dans les URLs ou le payload WebPush.
- Ne pas afficher de montant ou identite fiscale sur l'ecran verrouille.
- Valider les deep links par liste blanche de routes internes.
- Respecter le consentement WebPush et permettre la revocation.
- Afficher l'etat lu/non lu autrement que par la couleur seule.
- Annoncer les nouvelles notifications aux technologies d'assistance sans
  deplacer brutalement le focus.
- Le badge ne modifie pas la largeur de la barre de navigation.

## Criteres d'acceptation

- Un coffret ne peut etre suivi qu'apres verification de son token.
- Desactiver `FACTURATION` bloque les nouvelles notifications de facture.
- Une facture fournie cree au plus une notification par version/document.
- La notification in-app existe meme sans permission WebPush.
- Un clic marque la notification comme lue et ouvre la bonne ressource.
- Aucun secret ou montant fiscal n'apparait dans le WebPush.
- Un utilisateur sans token ne voit aucun detail de facture.
- Une correction ouvre une nouvelle entree liee, sans masquer l'originale.
- Live ne contient aucun ecran de qualification BUM, de credit ou d'emission.
- Les installations revoquees ne recoivent plus de notification.

## Decoupage d'implementation recommande

1. `LL-50-01` backend : ajouter la categorie `FACTURATION`.
2. `LL-50-02` backend : projeter les evenements de facture vers les suivis.
3. `LL-50-03` frontend : preference et badge Facturation.
4. `LL-50-04` frontend : cartes de notification et lecture.
5. `LL-50-05` frontend : deep link securise vers la Marketplace.
6. `LL-50-06` : service worker WebPush, confidentialite et hors ligne.
7. `LL-50-07` : tests E2E installation, revocation, idempotence et isolation.

## Dependances d'activation

- `LOCALEO_WEBPUSH_PUBLIC_LIVE_ENABLED=true` uniquement pour le canal WebPush ;
- cles VAPID et sujet WebPush configures ;
- batch de generation/envoi Live actif ;
- `LOCALEO_FEATURE_MERCHANT_INVOICE_REQUEST_ENABLED=true` ;
- ajout backend de `FACTURATION` et du projecteur d'evenements ;
- route Marketplace cible disponible et origine de deep link autorisee.
