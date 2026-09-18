# PWA, installation et WebPush

## Installation et manifeste

Le manifeste `manifest.webmanifest` est servi en développement et généré au build par [vite.config.js](../../../../../localeo-commercant/vite.config.js). Il déclare `display: 'standalone'`, une orientation portrait et les icônes [192 px](../../../../../localeo-commercant/public/icon-192.png) et [512 px](../../../../../localeo-commercant/public/icon-512.png). Aucun fichier `icon.svg` n'est fourni.

Au 18 septembre 2026, le manifeste conserve `theme_color: '#0078d4'` et `background_color: '#f5f9ff'`. Ces valeurs diffèrent des tokens de l'[interface actuelle](ui-components.md) ; cette description ne modifie pas la configuration de build.

[src/main.jsx](../../../../../localeo-commercant/src/main.jsx) enregistre `/sw.js` au chargement et laisse l'application utilisable si l'enregistrement échoue. L'interface d'installation est portée par [PwaInstallButton.jsx](../../../../../localeo-commercant/src/app/PwaInstallButton.jsx).

## WebPush Epic 32

Le WebPush avertit un appareil abonné lorsqu'un achat confirmé contient une prestation du commerce. Le commerçant choisit sa préférence de compte et l'abonnement de chaque appareil. Ce canal complète les emails et SMS ; il dépend des permissions du navigateur et du support WebPush de l'appareil.

- [public/sw.js](../../../../../localeo-commercant/public/sw.js) reçoit `push`, affiche la notification et ouvre ou remet au premier plan l'application au clic. Il transmet le deeplink opaque à la page de suivi.
- [src/lib/webPush.js](../../../../../localeo-commercant/src/lib/webPush.js) gère les préférences, l'abonnement navigateur, son enregistrement backend et la résolution du deeplink. La clé publique `LOCALEO_WEB_PUSH_PUBLIC_KEY` est nécessaire à l'abonnement ; ce module définit les éventuels endpoints configurables et leurs valeurs par défaut.
- L'activation est présentée dans « Mes informations personnelles », sous « Live tracking achats ». Les [contrats de notifications](../../../specifications/espace-commercant/contrats-api.md#notifications-webpush) décrivent les appels protégés.

Une notification ne crée jamais de session commerçant. Son deeplink reste opaque et n'est résolu qu'après authentification. Le payload ne doit exposer ni données personnelles, ni `achat_id`, `coffret_id` ou autre identifiant métier direct. Le type d'alerte achat est `ACHAT_COFFRET_CONTENANT_PRESTATION`.

## Limite hors ligne

Le service worker actuel écoute `push` et `notificationclick` ; il n'a aucun gestionnaire `fetch` ni stratégie de cache hors ligne. L'installation de la PWA ne garantit donc pas l'accès aux données sans réseau.

Ne pas introduire implicitement de cache pour les API authentifiées, de rejeu de mutation ou de validation simulée après une indisponibilité réseau. Une évolution du cache statique ou du cycle de mise à jour du service worker demande un périmètre et des tests dédiés ; elle n'est pas implémentée par ce document.
