# Écrans et repères de code

| Écran | Route ou accès | Preuve |
| --- | --- | --- |
| Carnet rempli | `/live/carnet` | [Session 390](../visuels/captures-avant/session-carnet-390.png) |
| Passeport et tombola personnels | `/live/animations?participation=…` | [Passeport](../visuels/captures-avant/session-passeport-bouliac-390.png) · [Tombola](../visuels/captures-avant/session-tombola-latresne-390.png) |
| Lots, lot libre et tirages | `/live/lots`, détail ouvert depuis sa carte | [Liste](../visuels/captures-avant/session-lots-390.png) · [Détail](../visuels/captures-avant/session-detail-lot-390.png) · [Tirages](../visuels/captures-avant/session-tirages-390.png) |
| Découvrir et fiche publique | `/live/decouvrir`, `/live/animations/{id}` | [Programme](../visuels/captures-avant/public-programme-390.png) · [Passeport public](../visuels/captures-avant/public-passeport-390.png) |
| Formulaire d’inscription et refus | Fiche → inscription, lien d’ajout invalide | [Inscription](../visuels/captures-avant/public-formulaire-390.png) · [Refus](../visuels/captures-avant/public-qr-invalide-390.png) |

Lecture seule du code local. `LiveUnifiedCarnet` agrège les accès du navigateur. `LiveAnimations` et `LiveAnimationGame` présentent les états et actions. `LiveLots` distingue lots, tirages et récupération. La carte d’un lot libre peut porter le responsable et les consignes renseignées. Le bon à présenter dépend de l’existence d’un accès correspondant. `LiveDiscovery` groupe par statut public et formate les dates séparément.

[Navigation et routes Live](../../../../../../localeo-marketplace/src/live/LiveApp.jsx) · [Carnet](../../../../../../localeo-marketplace/src/live/LiveUnifiedCarnet.jsx) · [Participations](../../../../../../localeo-marketplace/src/live/LiveAnimations.jsx) · [Lots](../../../../../../localeo-marketplace/src/live/LiveLots.jsx) · [Programme](../../../../../../localeo-marketplace/src/live/LiveDiscovery.jsx)
