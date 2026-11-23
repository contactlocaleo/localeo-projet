# Inventaire des écrans et repères de code

## Écrans du site TEST

| Écran ou état | Route ou accès | Captures |
| --- | --- | --- |
| Accueil stabilisé | `/` → `/live/carnet` | [320](../visuels/captures-avant/01-carnet-320.png), [390](../visuels/captures-avant/01-carnet-390.png), [430](../visuels/captures-avant/01-carnet-430.png) |
| Sélection et programme de Bouliac | `/live/decouvrir` | [Choix 390](../visuels/captures-avant/02-choisir-bouliac-390.png), [320](../visuels/captures-avant/20-programme-bouliac-320.png), [390](../visuels/captures-avant/20-programme-bouliac-390.png), [430](../visuels/captures-avant/20-programme-bouliac-430.png) |
| À venir vide | Ancre de période dans Découvrir | [320](../visuels/captures-avant/21-prochainement-clavier-320.png), [390](../visuels/captures-avant/21-prochainement-clavier-390.png), [430](../visuels/captures-avant/21-prochainement-clavier-430.png) |
| Détail d’animation et QR sur place | `/live/animations/{id}` | [Juste Prix](../visuels/captures-avant/23-fiche-juste-prix-390.png), [Vitrines](../visuels/captures-avant/23-fiche-vitrines-390.png), [tombola QR](../visuels/captures-avant/31-fiche-qr-public-390.png) |
| Inscription publique | `/live/animations/{id}/inscription` | [Tombola par e-mail](../visuels/captures-avant/41-formulaire-tombola-email-390.png) |
| Fiche indisponible | `/live/animations/{id}`, détail du Passeport | [Première lecture](../visuels/captures-avant/61-passeport-detail-390.png), [après « Réessayer »](../visuels/captures-avant/62-passeport-apres-reessai-390.png) |
| Ajout d’un accès refusé | `/live/animations/ajouter/{code}` | [Refus et focus clavier](../visuels/captures-avant/37-qr-refuse-focus-390.png) |
| Carnet de participations et lots vides | `/live/animations`, `/live/lots` | [Participations](../visuels/captures-avant/35-participations-vides-390.png), [lots](../visuels/captures-avant/34-lots-vides-390.png) |
| Retour et récupération | `/live/communes` → retour navigateur, `/live/retrouver-mon-carnet` | [Retour avec Bouliac](../visuels/captures-avant/30-retour-navigateur-390.png), [récupération prête](../visuels/captures-avant/40-recuperation-stable-390.png) |
| Chargement du programme | `/live/decouvrir` pendant la lecture | [Programme en chargement](../visuels/captures-avant/25-programme-chargement-390.png) |
| Programme partiel après HTTP 429 | `/live/decouvrir` en lecture ordinaire | [Message et bouton de reprise](../visuels/captures-avant/66-programme-contre-verification-390.png) |
| Coffrets, entrée secondaire | Onglet Coffrets dans Découvrir | [Catalogue à 390](../visuels/captures-avant/65-coffrets-entree-390.png) |

## Lecture du dépôt Marketplace

Ces éléments sont **DÉDUITS** du commit local `ccd4ac72432d17a0c39d090d73b14e095d796f84`.

| Surface | Composants et responsabilités |
| --- | --- |
| Routes et navigation | `src/App.jsx` donne la main à `LiveApp` sur `/live/*`. `LiveApp.jsx` sélectionne les vues, porte `Header` et `BottomNav`, et utilise `LiveRoot.jsx` en repli. `liveReturnNavigation.js` et `liveDiscoveryNavigation.js` mémorisent les retours de contexte. |
| Programme et dates | `LiveHome.jsx` intègre la sélection de commune et `LiveDiscovery.jsx`. Les groupes utilisent `statut_public` et les dates publiques sont formatées séparément. `LiveDrawCalendar.jsx` porte l’export ICS d’un tirage. |
| Fiche, inscription et accès | `LiveAnimationDetail.jsx` compose `LivePublicAnimationView.jsx`. La route d’inscription utilise `AnimationPublicPage`. `LiveRegistrationGuard.jsx` et `useLiveRegistrations.js` représentent la lecture de l’accès et de l’inscription. `AddAnimation` lit un lien d’accès dans `LiveApp.jsx`. `PlaceQrScanner.jsx` intervient dans le parcours de jeu autorisé, pour le QR de lieu. |
| Suivi, lots et reprise | `LiveUnifiedCarnet.jsx`, `LiveAnimations.jsx`, `LiveAnimationGame.jsx`, `LiveParticipationCard.jsx` et `LiveLots.jsx` présentent les états. `liveLibrary.js` conserve les accès sur l’appareil et `LiveCarnetRecovery.jsx` porte la récupération par lien e-mail. |
| Composants réutilisés | `LiveActivityIcon.jsx`, `LiveLoadingState.jsx`, `LiveRefreshButton.jsx`, `LiveParticipationAction.jsx` et `LiveRegistrationGuard.jsx` couvrent les motifs communs. |

[Routeur Marketplace](../../../../../../localeo-marketplace/src/App.jsx#L295) · [Navigation et vues Live](../../../../../../localeo-marketplace/src/live/LiveApp.jsx#L166) · [Groupes du programme](../../../../../../localeo-marketplace/src/live/LiveDiscovery.jsx#L28) · [Fiche publique](../../../../../../localeo-marketplace/src/live/LivePublicAnimationView.jsx#L148) · [Récupération](../../../../../../localeo-marketplace/src/live/LiveCarnetRecovery.jsx#L40) · [Lots](../../../../../../localeo-marketplace/src/live/LiveLots.jsx#L106)
