# SpÃ©cification technique - Marketplace Localeo

## 1. Objet

Ce document dÃ©crit la mise en Å“uvre technique de la version actuelle du frontend marketplace Localeo.

Il couvre :

- la stack et le bootstrap
- les routes et pages
- la couche d'accÃ¨s API
- la gestion d'Ã©tat et de configuration
- les feature flags
- le dÃ©ploiement et les points de vigilance

## 2. Stack technique

- React 18
- React Router DOM
- TanStack Query
- Vite 5
- CSS global maison
- serveur Node minimal pour le mode web service

Fichiers d'entrÃ©e principaux :

- [main.jsx](../../../../../localeo-marketplace/src/main.jsx)
- [App.jsx](../../../../../localeo-marketplace/src/App.jsx)

## 3. Bootstrap applicatif

Le bootstrap se fait dans [main.jsx](../../../../../localeo-marketplace/src/main.jsx).

ResponsabilitÃ©s :

- crÃ©ation du `QueryClient`
- enregistrement des options globales React Query
- montage React
- initialisation du `BrowserRouter`
- chargement des styles globaux

Configuration React Query actuelle :

- `staleTime = 60_000`
- `gcTime = 10 * 60_000`
- `retry = 1`
- `refetchOnWindowFocus = false`

## 4. Organisation du code

Le code source est structurÃ© de la maniÃ¨re suivante :

- `src/pages` : orchestration des Ã©crans mÃ©tier
- `src/components` : composants rÃ©utilisables de prÃ©sentation
- `src/services` : API, helpers mÃ©tier, runtime config et feature flags
- `src/store` : persistance de session lÃ©gÃ¨re
- `src/styles` : styles globaux

## 5. Routage

Les routes sont dÃ©finies dans [App.jsx](../../../../../localeo-marketplace/src/App.jsx).

Routes actives :

- `/`
- `/search`
- `/city`
- `/commercant`
- `/coffrets`
- `/coffret`
- `/coffret-instance`
- `/confirmation`
- `/commande-pro`
- `/confirmation-pro`
- `/mes-coffrets-pro`
- `/activer-coffret`
- `/activation-confirmee`
- `/qr-impression`
- `/retour-paiement`
- `/echec-paiement`

CaractÃ©ristiques :

- les pages sont chargÃ©es via `React.lazy`
- le fallback `Suspense` s'appuie sur des skeletons
- certaines routes sont conditionnÃ©es par feature flags

## 6. Pages et responsabilitÃ©s

### 6.1 DÃ©couverte

- [SearchCityPage.jsx](d:/OneDrive/Bureau/Documents/GitHub/localeo-marketplace/src/pages/SearchCityPage.jsx)
  - recherche de villes
  - prÃ©chargement de donnÃ©es de home
  - navigation vers catalogue, coffret ou commerÃ§ant
- [CoffretsPage.jsx](../../../../../localeo-marketplace/src/pages/CoffretsPage.jsx)
  - chargement ville, coffrets, commerÃ§ants
  - filtrage par type
  - ouverture du dÃ©tail coffret
- [CityPage.jsx](../../../../../localeo-marketplace/src/pages/CityPage.jsx)
  - variante Ã©ditorialisÃ©e de la vue ville
  - chargement enrichi et highlights

### 6.2 Conversion

- [CoffretPage.jsx](../../../../../localeo-marketplace/src/pages/CoffretPage.jsx)
  - chargement du coffret
  - enrichissement des prestations avec les commerÃ§ants
  - formulaire d'achat standard
  - entrÃ©e vers la commande pro
- [CommercantPage.jsx](../../../../../localeo-marketplace/src/pages/CommercantPage.jsx)
  - dÃ©tail commerÃ§ant
  - coffrets associÃ©s
- [CoffretInstancePage.jsx](../../../../../localeo-marketplace/src/pages/CoffretInstancePage.jsx)
  - consultation consommateur d'un coffret instance
  - agrÃ©gation achat + coffret instance + prestations + coffret source
  - consultation depuis lien email

### 6.3 Post-paiement

- [RetourPaiementPage.jsx](../../../../../localeo-marketplace/src/pages/RetourPaiementPage.jsx)
  - rÃ©solution de session de paiement
  - persistance du rÃ©sumÃ© de retour
  - redirection vers la bonne page finale
- [ConfirmationPage.jsx](../../../../../localeo-marketplace/src/pages/ConfirmationPage.jsx)
  - confirmation particulier
- [ConfirmationProPage.jsx](../../../../../localeo-marketplace/src/pages/ConfirmationProPage.jsx)
  - confirmation professionnel
- [StatutPaiementPage.jsx](../../../../../localeo-marketplace/src/pages/StatutPaiementPage.jsx)
  - annulation, erreur, attente

### 6.4 Parcours pro et activation

- [CommandeProPage.jsx](../../../../../localeo-marketplace/src/pages/CommandeProPage.jsx)
  - saisie entreprise
  - initialisation du paiement pro
- [MesCoffretsProPage.jsx](../../../../../localeo-marketplace/src/pages/MesCoffretsProPage.jsx)
  - chargement achat
  - chargement coffrets instances
  - activation et envoi de lien
- [ActiverCoffretPage.jsx](../../../../../localeo-marketplace/src/pages/ActiverCoffretPage.jsx)
  - activation par token
- [ActivationConfirmeePage.jsx](../../../../../localeo-marketplace/src/pages/ActivationConfirmeePage.jsx)
  - confirmation d'activation
- [QrPrintPage.jsx](../../../../../localeo-marketplace/src/pages/QrPrintPage.jsx)
  - chargement du QR et impression

## 7. Couche API

La couche API est centralisÃ©e dans [api.js](../../../../../localeo-marketplace/src/services/api.js).

### 7.1 Principes

- base URL calculÃ©e Ã  partir de `LOCALEO_API_BASE_URL`
- normalisation de la base sans slash final
- parsing uniforme des rÃ©ponses JSON ou texte
- gestion d'erreur enrichie avec `request_id` si disponible
- support de paramÃ¨tres lus dans `window.location.search` et `window.location.hash`

### 7.2 Endpoints consommÃ©s

Catalogue :

- `GET /public/referencement/villes`
- `GET /public/referencement/villes/:id`
- `GET /public/commercialisation/coffrets`
- `GET /public/commercialisation/coffrets/:id`
- `GET /protected/referencement/commercants`
- `GET /protected/referencement/commercants/:id`

Paiement :

- `POST /public/gestion-achats/paiements/initialiser`

Achats :

- `GET /protected/gestion-achats/achats/:achatId`
- `GET /protected/gestion-achats/achats/depuis-session/:sessionId`
- `GET /protected/gestion-achats/achats/:achatId/coffrets-instances`
- `GET /protected/gestion-achats/achats/:achatId/coffrets-instances/:coffretInstanceId`
- `GET /protected/gestion-achats/achats/:achatId/coffrets-instances/:coffretInstanceId/prestations`

Activation :

- `POST /protected/gestion-achats/achats/:achatId/coffrets-instances/:coffretInstanceId/activer`
- `POST /protected/gestion-achats/achats/:achatId/coffrets-instances/:coffretInstanceId/envoyer-lien-activation`
- `GET /protected/gestion-achats/coffrets-instances/:coffretInstanceId`
- `GET /protected/gestion-achats/coffrets-instances/:coffretInstanceId/prestations`
- `GET /protected/gestion-achats/coffrets-instances/:coffretInstanceId/qrcode`

QR code :

- `GET /public/gestion-achats/qrcode/detail?token=...`

Contact :

- `GET /public/support/contacts/motifs`
- `POST /public/support/contacts/consommateur/messages`

### 7.3 AccÃ¨s managÃ©

Pour certaines routes de gestion, des en-tÃªtes sont injectÃ©s :

- `Authorization`
- `X-Management-Token`

Ces valeurs peuvent Ãªtre lues depuis l'URL puis persistÃ©es dans le store de session.

Dans cette version, le parcours consommateur de consultation d'une instance de coffret rÃ©utilise aussi `Authorization`, alimentÃ© Ã  partir de :

- `consultation_token`
- `consultationToken`

## 8. Persistance et Ã©tat

### 8.1 Session store

Le store de session est dÃ©fini dans [sessionStore.js](../../../../../localeo-marketplace/src/store/sessionStore.js).

CaractÃ©ristiques :

- clÃ© unique : `localeo-marketplace`
- persistance dans `sessionStorage`
- stratÃ©gie `read -> merge -> write`
- aucun schÃ©ma strict ni validation runtime

ClÃ©s utilisÃ©es dans cette version :

- `selectedVille`
- `selectedCoffret`
- `coffretsVille`
- `commercantsVille`
- `loadedVilleId`
- `loadedVilleFetched`
- `paymentReturnSummary`
- `proOrderDraft`
- `managementToken`
- `authorization`

### 8.2 Ã‰tat UI local

Chaque page porte son propre Ã©tat local de formulaire, chargement, erreurs et succÃ¨s.

## 9. Feature flags et runtime config

### 9.1 Runtime config

La lecture de configuration se fait dans [runtimeConfig.js](../../../../../localeo-marketplace/src/services/runtimeConfig.js) via `window.__APP_CONFIG__`.

ClÃ©s configurÃ©es :

- `LOCALEO_API_BASE_URL`
- `LOCALEO_FEATURE_PAYMENT_ENABLED`
- `LOCALEO_FEATURE_PRO_ORDERS_ENABLED`
- `LOCALEO_FEATURE_HOME_DISCOVERY_TILES_ENABLED`

### 9.2 Feature flags

Les flags sont exposÃ©s dans [featureFlags.js](../../../../../localeo-marketplace/src/services/featureFlags.js).

RÃ¨gles actuelles :

- `paymentEnabled` : active le paiement standard
- `proOrdersEnabled` : n'est vrai que si le paiement standard est actif et que le flag pro est actif
- `homeDiscoveryTilesEnabled` : active les blocs de dÃ©couverte sur la home

## 10. Helpers mÃ©tier

Le fichier [shared.js](../../../../../localeo-marketplace/src/services/shared.js) centralise :

- le formatage des prix
- les labels de type de coffret
- la rÃ©solution d'image
- la sÃ©lection d'images fallback
- l'enrichissement d'un coffret avec les commerÃ§ants

Point important :

`resolveImageUri` gÃ¨re les images absolues, les chemins relatifs et les fallbacks statiques.

## 11. Styles

Fichiers principaux :

- [site-base.css](../../../../../localeo-marketplace/src/styles/site-base.css)
- [marketplace.css](../../../../../localeo-marketplace/src/styles/marketplace.css)
- [marketplace-digital.css](../../../../../localeo-marketplace/src/styles/marketplace-digital.css)

StratÃ©gie actuelle :

- CSS global
- conventions de nommage mÃ©tier / BEM-like
- pas de CSS Modules
- pas de design system encapsulÃ©

ConsÃ©quences :

- forte vitesse d'itÃ©ration
- risque de rÃ©gression croisÃ©e plus Ã©levÃ©
- dette de maintenance croissante sur `marketplace.css`

## 12. DÃ©ploiement

### 12.1 Build statique

Le build est produit par Vite vers `dist`.

Un script gÃ©nÃ¨re Ã©galement `public/app-config.js` / `dist/app-config.js` en fonction de l'environnement cible.

### 12.2 Serveur Node

Le mode web service s'appuie sur [server.cjs](../../../../../localeo-marketplace/server.cjs).

ResponsabilitÃ©s :

- servir les fichiers de `dist`
- exposer `/app-config.js`
- injecter les variables d'environnement au runtime
- assurer le fallback SPA vers `index.html`

### 12.3 Variables d'environnement serveur

Variables supportÃ©es :

- `PORT`
- `LOCALEO_API_BASE_URL`
- `LOCALEO_FEATURE_PAYMENT_ENABLED`
- `LOCALEO_FEATURE_PRO_ORDERS_ENABLED`
- `LOCALEO_FEATURE_HOME_DISCOVERY_TILES_ENABLED`

## 13. Flux techniques principaux

### 13.1 Flux dÃ©couverte

1. recherche ville sur `/search`
2. Ã©criture de la ville dans le store
3. prÃ©chargement de `ville`, `coffrets`, `commercants`
4. navigation vers `/coffrets`

### 13.2 Flux dÃ©tail coffret

1. lecture du `coffret_id`
2. chargement `coffret`
3. calcul des IDs commerÃ§ants liÃ©s aux prestations
4. chargement parallÃ¨le des commerÃ§ants
5. enrichissement local avant rendu

### 13.3 Flux paiement

1. collecte du formulaire
2. appel `createCheckout`
3. redirection navigateur vers `checkout_url`
4. retour backend vers `/retour-paiement`
5. rÃ©cupÃ©ration achat via session
6. redirection finale vers succÃ¨s ou Ã©chec

### 13.4 Flux pro

1. paiement multi-coffrets
2. consultation d'achat
3. chargement coffrets instances
4. chargement dÃ©tail + prestations par coffret instance
5. activation ou envoi de lien via API

### 13.5 Flux consommateur coffret instance

1. l'utilisateur ouvre un lien email vers `/coffret-instance`
2. le frontend lit `coffret_instance_id` et `consultation_token`
3. `consultation_token` est propagÃ© dans le header `Authorization`
4. le frontend charge `achat`
5. le frontend charge `coffret instance`
6. le frontend charge les `prestations` du coffret instance
7. si `coffret_id` est prÃ©sent dans le coffret instance, le frontend charge aussi le coffret source
8. le rendu agrÃ¨ge les donnÃ©es pour une lecture consommateur

## 14. Contraintes et risques techniques

### 14.1 Couplage page / logique

Les pages portent encore beaucoup de logique mÃ©tier et de chargement.

Impact :

- fichiers volumineux
- testabilitÃ© rÃ©duite
- duplication de conventions

### 14.2 Store non typÃ©

Le store session est librement extensible.

Impact :

- risque de dÃ©rive de schÃ©ma
- dÃ©pendances implicites entre pages

### 14.3 Encodage Ã©ditorial

Le dÃ©pÃ´t contient encore des textes historiquement mal encodÃ©s ou non harmonisÃ©s.

Impact :

- qualitÃ© perÃ§ue
- dette de maintenance documentaire et UI

### 14.4 Contrats API bruts

Le front dÃ©pend fortement des noms de champs backend sans couche de mapping dÃ©diÃ©e.

Impact :

- fragilitÃ© en cas d'Ã©volution de contrat
- logique de fallback dispersÃ©e dans les pages

### 14.5 Contrat d'accÃ¨s consommateur indirect

La page consommateur `/coffret-instance` depend actuellement de :

- `achat_id`
- `coffret_instance_id`

ainsi que d'un `consultation_token` transmis en query param puis injectÃ© dans `Authorization`.

Impact :

- le lien email doit transporter plusieurs paramÃ¨tres sensibles
- le contrat backend n'est pas encore exposÃ© sous la forme minimale `coffrets-instances/:id` publique

## 15. Recommandations d'Ã©volution

### Court terme

- aligner toute la documentation sur `BrowserRouter` et non plus `HashRouter`
- normaliser les textes et l'encodage sur l'ensemble du dÃ©pÃ´t
- expliciter le contrat du session store
- isoler les rÃ¨gles de transformation API

### Moyen terme

- extraire des hooks mÃ©tier : `useVille`, `useCoffrets`, `useCoffretDetail`, `useAchat`
- sortir les blocs volumineux des pages en composants de section
- dÃ©couper `marketplace.css` par domaine

### Long terme

- typer les contrats via TypeScript ou schÃ©mas runtime
- formaliser les modÃ¨les mÃ©tier cÃ´tÃ© front
- ajouter des tests E2E sur les flux paiement et pro

## 16. SynthÃ¨se

La version actuelle repose sur une architecture frontend simple, pragmatique et exploitable en production :

- SPA React + Vite
- routage navigateur standard
- cache et chargement via TanStack Query
- configuration runtime via `window.__APP_CONFIG__`
- persistance lÃ©gÃ¨re de session

Le principal enjeu technique n'est pas la stack elle-mÃªme, mais la maÃ®trise progressive de la dette de structure, de contenu et de contrats API.





## Correctifs de securite du 6 septembre 2026

Voir le [contrat des correctifs MARKET](../../../specifications/securisation-production/corrections-marketplace-2026-09-06.md), qui complete les parcours et les regles de livraison.


### Annulation des recherches multiscope

Le signal fourni par TanStack Query est transmis par `MarketplaceMultiScopeSearch`
a `api.searchMarketplace(query, limites, { signal })`, puis au transport HTTP.
Une recherche devenue sans observateur est annulee cote navigateur, notamment
lorsque la recherche debounced change ou lorsque le composant est demonte.
Le debounce de 400 ms et le cache de 30 secondes restent inchanges.
L'annulation du transport ne garantit pas l'interruption d'une requete SQL
deja demarree sur le serveur.
