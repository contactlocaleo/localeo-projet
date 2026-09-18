# Architecture Frontend Marketplace

## Objectif

Ce document dÃ©crit l'architecture frontend actuelle de la marketplace Localeo, ses responsabilitÃ©s, ses flux principaux, ses choix techniques et les points de vigilance pour les Ã©volutions futures.

Le pÃ©rimÃ¨tre couvre :

- l'application React/Vite
- le routage et les pages mÃ©tier
- la gestion des donnÃ©es et de l'Ã©tat
- la configuration runtime
- le mode de dÃ©ploiement statique et Render Web Service

## Vue d'ensemble

La marketplace est une SPA React construite avec Vite. Elle expose un parcours principal court :

1. recherche d'une ville
2. consultation des coffrets disponibles
3. dÃ©tail d'un coffret
4. paiement ou parcours pro

L'application est organisÃ©e autour de quatre axes :

- `pages` pour les Ã©crans mÃ©tier
- `components` pour les composants de prÃ©sentation rÃ©utilisables
- `services` pour les accÃ¨s API, la configuration et les helpers mÃ©tier
- `store` pour la persistance lÃ©gÃ¨re de contexte en session

## Stack technique

- React 18
- React Router DOM
- TanStack Query
- Vite
- CSS global maison sans design system externe

EntrÃ©e principale : [main.jsx](../../../../../localeo-marketplace/src/main.jsx)

## Architecture applicative

### Composition gÃ©nÃ©rale

Le frontend suit une architecture simple de type :

- `App` = composition du layout global et des routes
- `pages` = orchestration de l'Ã©cran, chargement des donnÃ©es, navigation
- `components` = rendu rÃ©utilisable, skeletons, feedback, breadcrumb, blocs de valeur
- `services` = couche d'accÃ¨s aux API et logique transverse
- `store` = persistance temporaire via `sessionStorage`

Cette architecture est adaptÃ©e Ã  un produit de taille petite Ã  moyenne, avec un nombre de flux encore limitÃ©.

## Rendu et bootstrap

Point d'entrÃ©e : [main.jsx](../../../../../localeo-marketplace/src/main.jsx)

ResponsabilitÃ©s :

- crÃ©ation du `QueryClient`
- montage React
- activation de `BrowserRouter`
- chargement des feuilles CSS globales

DÃ©cisions structurantes :

- le routeur utilise `BrowserRouter`
- la politique React Query est dÃ©finie globalement
- les styles sont chargÃ©s globalement, sans CSS modules

Implication :

- les URLs doivent Ãªtre compatibles avec la stratÃ©gie hash
- les liens absolus applicatifs doivent intÃ©grer cette contrainte

## Routage

DÃ©finition des routes : [App.jsx](../../../../../localeo-marketplace/src/App.jsx)

Pages principales :

- `/search`
- `/city`
- `/coffrets`
- `/coffret`
- `/confirmation`
- `/commande-pro`
- `/confirmation-pro`
- `/mes-coffrets-pro`
- `/activer-coffret`
- `/activation-confirmee`
- `/retour-paiement`
- `/echec-paiement`

Le chargement des pages est lazy via `React.lazy`, avec `Suspense`.

ResponsabilitÃ© de `App.jsx` :

- fournir le layout global
- filtrer certaines routes via feature flags
- maintenir une navigation de haut niveau simple

## DÃ©coupage par domaines fonctionnels

### 1. DÃ©couverte

Pages :

- [SearchCityPage.jsx](d:/OneDrive/Bureau/Documents/GitHub/localeo-marketplace/src/pages/SearchCityPage.jsx)
- [CityPage.jsx](../../../../../localeo-marketplace/src/pages/CityPage.jsx)
- [CoffretsPage.jsx](../../../../../localeo-marketplace/src/pages/CoffretsPage.jsx)

ResponsabilitÃ©s :

- recherche de ville
- affichage de la sÃ©lection locale
- navigation vers le dÃ©tail d'un coffret

### 2. Produit / conversion

Pages :

- [CoffretPage.jsx](../../../../../localeo-marketplace/src/pages/CoffretPage.jsx)
- [ConfirmationPage.jsx](../../../../../localeo-marketplace/src/pages/ConfirmationPage.jsx)
- [RetourPaiementPage.jsx](../../../../../localeo-marketplace/src/pages/RetourPaiementPage.jsx)
- [StatutPaiementPage.jsx](../../../../../localeo-marketplace/src/pages/StatutPaiementPage.jsx)

ResponsabilitÃ©s :

- chargement du dÃ©tail coffret
- enrichissement avec les commerÃ§ants associÃ©s
- initialisation du paiement
- suivi de retour de paiement

### 3. Parcours pro / gestion

Pages :

- [CommandeProPage.jsx](../../../../../localeo-marketplace/src/pages/CommandeProPage.jsx)
- [ConfirmationProPage.jsx](../../../../../localeo-marketplace/src/pages/ConfirmationProPage.jsx)
- [MesCoffretsProPage.jsx](../../../../../localeo-marketplace/src/pages/MesCoffretsProPage.jsx)
- [ActiverCoffretPage.jsx](../../../../../localeo-marketplace/src/pages/ActiverCoffretPage.jsx)
- [ActivationConfirmeePage.jsx](../../../../../localeo-marketplace/src/pages/ActivationConfirmeePage.jsx)

ResponsabilitÃ©s :

- commande multi-coffrets
- consultation d'achat
- activation et envoi de liens
- affichage de statuts mÃ©tier

## Gestion des donnÃ©es

### Couche API

Fichier principal : [api.js](../../../../../localeo-marketplace/src/services/api.js)

RÃ´le :

- centraliser les appels HTTP
- construire les URLs Ã  partir de la base API
- parser et uniformiser les erreurs
- gÃ©rer les en-tÃªtes de gestion pour les parcours pro

Points importants :

- la base API vient de `LOCALEO_API_BASE_URL`
- en production, un warning console est Ã©mis si la base API reste relative
- certains tokens sont lus depuis l'URL puis persistÃ©s en session

API exposÃ©es :

- villes
- coffrets
- commerÃ§ants
- paiements
- achats
- activation

### React Query

TanStack Query est la couche standard de rÃ©cupÃ©ration et cache.

RÃ¨gles globales dÃ©finies dans [main.jsx](../../../../../localeo-marketplace/src/main.jsx) :

- `staleTime = 60s`
- `gcTime = 10 min`
- `retry = 1`
- pas de refetch au focus fenÃªtre

Usage observÃ© :

- `useQuery` pour les vues simples
- `useQueries` pour charger plusieurs entitÃ©s liÃ©es
- `prefetchQuery` pour accÃ©lÃ©rer le parcours

### Ã‰tat local de session

Fichier : [sessionStore.js](../../../../../localeo-marketplace/src/store/sessionStore.js)

Le store session sert Ã  conserver :

- la ville sÃ©lectionnÃ©e
- le coffret sÃ©lectionnÃ©
- certains rÃ©sultats dÃ©jÃ  chargÃ©s
- des jetons utiles au parcours pro

Choix architectural :

- stockage minimal
- sÃ©rialisation JSON simple
- pas de state manager global dÃ©diÃ©

Ce choix reste adaptÃ© tant que :

- le nombre de flows transverses reste limitÃ©
- les dÃ©pendances entre Ã©crans restent simples

## Configuration et feature flags

### Runtime config

Fichier : [runtimeConfig.js](../../../../../localeo-marketplace/src/services/runtimeConfig.js)

Le frontend lit `window.__APP_CONFIG__` via :

- [public/app-config.js](../../../../../localeo-marketplace/public/app-config.js) pour le mode statique
- [server.cjs](../../../../../localeo-marketplace/server.cjs) pour le mode Render Web Service

Variables principales :

- `LOCALEO_API_BASE_URL`
- `LOCALEO_FEATURE_PAYMENT_ENABLED`
- `LOCALEO_FEATURE_PRO_ORDERS_ENABLED`
- `LOCALEO_FEATURE_HOME_DISCOVERY_TILES_ENABLED`

### Feature flags

Fichier : [featureFlags.js](../../../../../localeo-marketplace/src/services/featureFlags.js)

RÃ´le :

- transformer des chaÃ®nes de config en boolÃ©ens
- fournir une API mÃ©tier simple au reste de l'application

Flags actuels :

- activation du paiement standard
- activation du parcours pro
- activation des vignettes de dÃ©couverte home

## Ressources visuelles et helpers mÃ©tier

Fichier : [shared.js](../../../../../localeo-marketplace/src/services/shared.js)

ResponsabilitÃ©s :

- libellÃ©s mÃ©tiers de types de coffret
- formatage de prix
- sÃ©lection des images fallback
- normalisation de `image_uri`
- enrichissement d'un coffret avec ses commerÃ§ants

Point important :

`resolveImageUri` normalise les chemins relatifs du contrat API en `/api/...`, y compris les images `/public/images/...`, tout en prÃ©servant les assets statiques.

## Styles

Fichiers :

- [site-base.css](../../../../../localeo-marketplace/src/styles/site-base.css)
- [marketplace.css](../../../../../localeo-marketplace/src/styles/marketplace.css)
- [marketplace-digital.css](../../../../../localeo-marketplace/src/styles/marketplace-digital.css)

StratÃ©gie actuelle :

- styles globaux
- convention de classes structurÃ©e mais non encapsulÃ©e
- forte densitÃ© fonctionnelle dans `marketplace.css`

Avantages :

- rapiditÃ© d'itÃ©ration
- faible coÃ»t d'entrÃ©e
- styles faciles Ã  appliquer transversalement

Limites :

- risque de rÃ©gression CSS croisÃ©e
- difficultÃ© croissante de maintenance
- responsabilitÃ© trop concentrÃ©e dans un seul fichier

## DÃ©ploiement

### 1. Mode statique

Build :

- Vite gÃ©nÃ¨re `dist`
- un script gÃ©nÃ¨re aussi `app-config.js` Ã  partir des `.env*`

Contrainte :

- pas de proxy Vite en production
- l'API doit Ãªtre adressÃ©e via `LOCALEO_API_BASE_URL`

### 2. Mode Render Web Service

Serveur : [server.cjs](../../../../../localeo-marketplace/server.cjs)

RÃ´le :

- servir les fichiers statiques de `dist`
- gÃ©nÃ©rer `/app-config.js` dynamiquement depuis `process.env`
- fournir un fallback SPA vers `index.html`

Implication :

- la configuration dÃ©ployÃ©e peut Ãªtre changÃ©e via variables d'environnement Render
- un redÃ©marrage ou redeploy reste nÃ©cessaire pour relire `process.env`

## Flux principaux

### Flux 1 - DÃ©couverte d'un coffret

1. l'utilisateur arrive sur `/search`
2. il recherche une ville
3. la ville est persistÃ©e dans `sessionStorage`
4. la page `/coffrets` charge ville, coffrets et commerÃ§ants
5. le clic sur un coffret envoie vers `/coffret`
6. la page coffret recharge le dÃ©tail et enrichit les prestations

### Flux 2 - Achat standard

1. la page coffret collecte email et tÃ©lÃ©phone
2. le frontend appelle `/paiements/initialiser`
3. le backend renvoie `checkout_url`
4. le navigateur est redirigÃ©
5. les pages de retour/confirmation clÃ´turent le parcours

### Flux 3 - Parcours pro

1. commande entreprise
2. rÃ©cupÃ©ration de l'achat et des coffret instances
3. activation ou envoi de lien bÃ©nÃ©ficiaire
4. gestion des statuts via API d'achats/activation

## Forces de l'architecture actuelle

- architecture simple et lisible
- faible coÃ»t de maintenance Ã  court terme
- sÃ©paration correcte entre pages, composants et services
- configuration runtime dÃ©jÃ  en place
- intÃ©gration Render compatible avec pilotage par variables d'environnement

## Faiblesses et risques

### 1. CSS monolithique

Le fichier [marketplace.css](../../../../../localeo-marketplace/src/styles/marketplace.css) concentre une grande partie de la dette de maintenance frontend.

Risque :

- les Ã©volutions UI deviennent coÃ»teuses
- les rÃ©gressions visuelles deviennent difficiles Ã  anticiper

### 2. Couplage fort page <-> logique de chargement

Les pages portent Ã  la fois :

- le chargement des donnÃ©es
- une partie de la logique mÃ©tier
- la composition visuelle

Risque :

- augmentation de la taille des composants Ã©cran
- difficultÃ© Ã  rÃ©utiliser ou tester la logique

### 3. Session store trop libre

Le store session accepte n'importe quel patch JSON sans contrat strict.

Risque :

- dÃ©rive de schÃ©ma
- dette de cohÃ©rence entre pages

### 4. Encodage / qualitÃ© de contenu

Le code contient encore certains textes historiques mal encodÃ©s ou ASCII-only.

Risque :

- dette de qualitÃ© perÃ§ue
- difficultÃ© de maintenance Ã©ditoriale

### 5. Faible encapsulation du domaine

Les concepts mÃ©tier `ville`, `coffret`, `prestation`, `achat`, `coffret instance` ne sont pas modÃ©lisÃ©s par modules dÃ©diÃ©s.

Risque :

- duplication des conventions
- dÃ©pendance implicite Ã  la forme brute des rÃ©ponses API

## Recommandations d'Ã©volution

### Court terme

- stabiliser le contrat des variables d'environnement
- normaliser dÃ©finitivement les textes et encodages
- documenter les conventions de navigation et de session
- regrouper les helpers mÃ©tier par domaine

### Moyen terme

- introduire des hooks mÃ©tier :
  - `useVille`
  - `usePacks`
  - `usePackDetail`
  - `useProOrder`
- sortir les sous-sections volumineuses des pages dans des composants dÃ©diÃ©s
- segmenter `marketplace.css` par domaine ou Ã©cran

### Long terme

- introduire une architecture frontend par domaines fonctionnels
- typer les contrats si migration vers TypeScript
- isoler un design system minimal
- ajouter des tests UI / intÃ©gration sur les flux critiques

## Dossier source - responsabilitÃ©s recommandÃ©es

### `src/pages`

Doit contenir :

- orchestration d'Ã©cran
- composition de sections
- navigation et branchements de flux

Ne devrait pas concentrer :

- helpers mÃ©tier longs
- transformation de donnÃ©es complexe
- logique UI rÃ©utilisable

### `src/components`

Doit contenir :

- composants rÃ©utilisables
- sections d'Ã©cran isolables
- composants de feedback et skeleton

### `src/services`

Doit contenir :

- accÃ¨s API
- configuration
- helpers mÃ©tier transverses
- conventions de transformation de donnÃ©es

### `src/store`

Doit contenir :

- persistance lÃ©gÃ¨re et clairement bornÃ©e

Ne devrait pas devenir :

- un state manager global informel

## DÃ©cisions architecturales actuelles

### ADR-001 - Utiliser `BrowserRouter`

Motif :

- URLs directes compatibles avec les liens entrants et le scope `/live/` de la PWA

ConsÃ©quence :

- les routes applicatives absentes du disque reçoivent le shell SPA ; les fichiers `/assets/*` absents renvoient 404
- les liens utilisent le chemin normal, sans préfixe `#` ; configurer ce fallback sur tout hébergement statique alternatif

### ADR-002 - Utiliser TanStack Query comme couche standard de rÃ©cupÃ©ration

Motif :

- Ã©viter une couche custom de cache et de synchronisation

ConsÃ©quence :

- les pages dÃ©pendent des `queryKeys` et du dÃ©coupage API existant

### ADR-003 - Utiliser `window.__APP_CONFIG__` pour la configuration runtime

Motif :

- permettre le pilotage de l'URL API et des feature flags sans rebuild strict du bundle

ConsÃ©quence :

- le comportement diffÃ¨re entre build statique et service Node runtime

### ADR-004 - Conserver un store session minimal

Motif :

- Ã©viter la complexitÃ© d'un state manager global complet

ConsÃ©quence :

- la discipline de schÃ©ma doit Ãªtre maintenue par convention

## Sujets Ã  traiter ensuite

1. formaliser les contrats de session
2. modulariser la couche CSS
3. extraire des hooks mÃ©tier
4. clarifier les conventions d'encodage et de contenu
5. documenter plus finement le parcours pro

