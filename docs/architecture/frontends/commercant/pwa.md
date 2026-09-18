# PWA & Offline

- `manifest.webmanifest` : manifeste d'application genere au build.
- `public/sw.js` : service worker de l'application.
- `icon.svg` : icone de l'app.
- `display: 'standalone'`.
- `theme_color: '#0078d4'`.

## Web Push Epic 32

Dans Localeo, le WebPush sert au live tracking achats cote commercant.
Il permet de prevenir un appareil abonne lorsqu'un achat confirme contient une prestation du commerce.
Le commercant garde la main sur deux niveaux d'activation : la preference de compte et l'abonnement de chaque appareil.

Ce canal ne remplace pas les emails ou les SMS.
Il est concu comme une alerte immediate de l'application commercant, soumise aux permissions du navigateur et au support WebPush de l'appareil.

- `public/sw.js` gere la reception des evenements `push` et transporte uniquement un deeplink opaque vers l'application au clic.
- `src/lib/webPush.js` gere les preferences live tracking, l'abonnement navigateur, l'enregistrement backend et la resolution du deeplink.
- L'activation est exposee dans `Mes informations personnelles` sous `Live tracking achats`.
- La reception d'une notification ne cree jamais de session commercant. La resolution du deeplink se fait seulement apres authentification.

Variables d'environnement :

- `LOCALEO_WEB_PUSH_PUBLIC_KEY` : cle publique VAPID obligatoire pour abonner un navigateur.
- `LOCALEO_WEB_PUSH_PREFERENCES_ENDPOINT` : endpoint protege des preferences, par defaut `/commercants/me/notifications/preferences`.
- `LOCALEO_WEB_PUSH_SUBSCRIPTIONS_ENDPOINT` : endpoint protege des abonnements, par defaut `/commercants/me/webpush/abonnements`.
- `LOCALEO_WEB_PUSH_DEEPLINK_RESOLUTION_ENDPOINT` : endpoint protege de resolution, par defaut `/commercants/me/webpush/deeplinks/resoudre`.

Contrat backend attendu :

- `GET /protected/commercants/me/notifications/preferences`.
- `PATCH /protected/commercants/me/notifications/preferences` avec `{ "live_tracking_achats_active": true }`.
- `GET /protected/commercants/me/webpush/abonnements`.
- `POST /protected/commercants/me/webpush/abonnements` avec `endpoint`, `keys`, `device_label` et `user_agent`.
- `DELETE /protected/commercants/me/webpush/abonnements/{abonnement_id}`.
- `POST /protected/commercants/me/webpush/deeplinks/resoudre` avec `{ "deeplink": "localeo://commercant/live-tracking/{opaque_reference}" }`.

Payload WebPush cible :

```json
{
  "type": "ACHAT_COFFRET_CONTENANT_PRESTATION",
  "title": "Un coffret contenant votre offre vient d'être acheté",
  "body": "Coffret Découverte locale - 1 prestation chez vous",
  "deeplink": "localeo://commercant/live-tracking/{opaque_reference}"
}
```

Le payload WebPush ne doit pas contenir de donnees personnelles, `achat_id`, `coffret_id` ou autre identifiant metier direct.
Le deeplink doit rester opaque pour que sa resolution cote backend se fasse uniquement apres authentification du commercant.

## Etapes suivantes

1. Gerer la mise en cache des ressources statiques et API.
2. Ajouter une strategie de renouvellement de service worker.
