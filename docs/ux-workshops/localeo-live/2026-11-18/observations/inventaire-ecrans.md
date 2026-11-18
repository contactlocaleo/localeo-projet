# Inventaire des écrans et composants

## Écrans vus dans le navigateur

| Écran | URL ou entrée | Statut et preuve |
| --- | --- | --- |
| Mon carnet vide | `/live/carnet`, depuis la racine du domaine | OBSERVÉ — `01-accueil-*` |
| Découvrir, Bouliac suivie | `/live/decouvrir` | OBSERVÉ — `02-decouvrir-bouliac-*` |
| Fiches d’animation Bouliac | `/live/animations/{id}` | OBSERVÉ — `03-*`, `05-*`, `06-*` |
| Inscription Juste prix | `/live/animations/{id}/inscription` | OBSERVÉ — `04-*` |
| Mes participations vide | `/live/animations` | OBSERVÉ — `07-*` |
| Mes lots vide | `/live/lots` | OBSERVÉ — `08-*` |
| Récupération du carnet | `/live/retrouver-mon-carnet` | OBSERVÉ — `09-*` |
| Ajout par code invalide | `/live/animations/ajouter/code-invalide` | OBSERVÉ — `10-*` |
| Retour vers Découvrir | `/live/communes` puis retour navigateur | OBSERVÉ — `11-*` |

## Repères du dépôt Marketplace

Tous les éléments ci-dessous sont **DÉDUITS** du code, sans constituer une preuve de fonctionnement dans le navigateur pour leurs états personnels.

- Routage principal : [`App.jsx`](../../../../../../localeo-marketplace/src/App.jsx) lignes 289–338 ; `/live/*` est confié à `LiveApp`.
- Routage Live : [`LiveApp.jsx`](../../../../../../localeo-marketplace/src/live/LiveApp.jsx) lignes 756–784 ; détails, inscription, lots, découverte, carnet, communes, récupération et réglages.
- Navigation : `Header` et `BottomNav` dans `LiveApp.jsx` lignes 134–195 et 784 ; onglets « Mon carnet / Mes lots / Découvrir ».
- Découverte et dates des animations : [`LiveDiscovery.jsx`](../../../../../../localeo-marketplace/src/live/LiveDiscovery.jsx) lignes 24, 114–141 et 381–388 ; [`LiveAnimationDetail.jsx`](../../../../../../localeo-marketplace/src/live/LiveAnimationDetail.jsx) lignes 49, 176–201 ; [`LivePublicAnimationView.jsx`](../../../../../../localeo-marketplace/src/live/LivePublicAnimationView.jsx) lignes 87–148.
- Participation et carnet : [`LiveAnimations.jsx`](../../../../../../localeo-marketplace/src/live/LiveAnimations.jsx), [`LiveUnifiedCarnet.jsx`](../../../../../../localeo-marketplace/src/live/LiveUnifiedCarnet.jsx), [`LiveAnimationGame.jsx`](../../../../../../localeo-marketplace/src/live/LiveAnimationGame.jsx).
- Lots : [`LiveLots.jsx`](../../../../../../localeo-marketplace/src/live/LiveLots.jsx) lignes 102–108, 173–198, 243–333 ; états et détail d’un bon numérique.
- Calendrier : `LiveDiscovery.jsx` groupe les animations par période ; [`LiveDrawCalendar.jsx`](../../../../../../localeo-marketplace/src/live/LiveDrawCalendar.jsx) lignes 5–15 produit un fichier ICS pour un tirage. Aucun écran de calendrier mensuel distinct repéré dans le routage Live.
- Accès et récupération : [`LiveCarnetRecovery.jsx`](../../../../../../localeo-marketplace/src/live/LiveCarnetRecovery.jsx) lignes 40–95 ; [`liveLibrary.js`](../../../../../../localeo-marketplace/src/live/liveLibrary.js) lignes 93–104 utilise IndexedDB pour le carnet local. L’inscription publique est servie par `AnimationPublicPage` via `LiveApp.jsx` ligne 770. L’interface inspectée ne présentait pas de connexion par mot de passe.
- Composants réutilisables : [`LiveActivityIcon.jsx`](../../../../../../localeo-marketplace/src/live/LiveActivityIcon.jsx), [`LiveLoadingState.jsx`](../../../../../../localeo-marketplace/src/live/LiveLoadingState.jsx), [`LiveCarnetHeader.jsx`](../../../../../../localeo-marketplace/src/live/LiveCarnetHeader.jsx), [`LiveDrawCalendar.jsx`](../../../../../../localeo-marketplace/src/live/LiveDrawCalendar.jsx).
