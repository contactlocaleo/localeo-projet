# Inventaire des écrans

| Écran/route | Mobile | Ordinateur | Fonctions visibles et preuve |
| --- | --- | --- | --- |
| Connexion `/` | **OBSERVÉ** | Non inspecté | Login, mot de passe, récupération d’accès, installation : [capture](../visuels/captures-avant/02-connexion-pro-mobile.png). |
| Accueil `/menu` | **OBSERVÉ** | **OBSERVÉ** | Scanner prioritaire, notification à traiter, activité Animation, invitations, préparation : [mobile](../visuels/captures-avant/03-accueil-pro-mobile.png), [ordinateur](../visuels/captures-avant/10-accueil-pro-desktop.png). |
| Scanner `/validation` | **OBSERVÉ** | **OBSERVÉ** | Caméra en erreur dans les deux contextes, saisie manuelle disponible : [mobile](../visuels/captures-avant/04-scanner-mobile.png), [ordinateur](../visuels/captures-avant/12-scanner-desktop.png), [erreur locale](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png). |
| Animations `/animations` | **OBSERVÉ** | **OBSERVÉ** | Onglets En cours/À venir/Terminées, cartes et détails : [mobile](../visuels/captures-avant/05-animations-mobile.png), [ordinateur](../visuels/captures-avant/11-animations-desktop.png). |
| Invitation `/animations/invitations` et `/commercants/animations/invitations/:id` | **OBSERVÉ** | Non inspecté | Aucune demande en attente ; historique accepté, détail mission, règlement et contact : [liste](../visuels/captures-avant/06-invitations-mobile.png), [détail](../visuels/captures-avant/18-invitation-acceptee-mobile.png). |
| Préparation `/animations/preparation` et `/:demandeId` | **OBSERVÉ** | Non inspecté | Liste des participations acceptées, étapes guidées Vitrines et étapes simples Tombola : [liste](../visuels/captures-avant/07-preparation-mobile.png), [Vitrines](../visuels/captures-avant/16-preparation-vitrines-mobile.png), [Tombola](../visuels/captures-avant/17-preparation-tombola-mobile.png). |
| Détail animation `/animations/:id` | **OBSERVÉ** | Non inspecté | Missions, dates, kit, guide, scanner si ouvert : [Vitrines](../visuels/captures-avant/13-detail-vitrines-mobile.png), [Juste Prix](../visuels/captures-avant/14-detail-juste-prix-mobile.png), [Tombola](../visuels/captures-avant/15-detail-tombola-mobile.png). |
| Notifications `/notifications` | **OBSERVÉ** | Non inspecté | Notifications PIN et Animation, filtres, neuf notifications Animation de test dont une non lue : [capture](../visuels/captures-avant/09-notifications-generales-mobile.png). |
| Guide de préparation (panneau dans préparation) | **OBSERVÉ** | Non inspecté | Équipe, flyer, QR d’inscription, consignes, déclaration prêt : [guide ouvert](../visuels/captures-avant/21-guide-preparation-mobile.png). |
| `/animations/notifications` | **OBSERVÉ, URL directe uniquement** | Non inspecté | « Animation inaccessible » ; l’onglet Notifications pointe en réalité vers `/notifications` : [capture](../visuels/captures-avant/08-notifications-animation-mobile.png). Cette URL directe ne représente pas le parcours utilisateur prévu. |
| Confirmation/doublon QR | **DÉDUIT du code, non atteint** | Non inspecté | États de confirmation et de reçu dans `localeo-commercant/src/features/validation/ValidationActionWorkspace.jsx:615-630`. |
| Notification WebPush du système | **DÉDUIT du code, non reçue** | Non inspecté | `localeo-commercant/public/sw.js:50-90` ; aucun envoi effectué. |

**HYPOTHÈSE à vérifier en atelier :** la position des accès « Notifications » et « Préparation » suffit pour retrouver une action attendue après plusieurs jours. Aucun test utilisateur n’a encore été mené.
