# Observations factuelles et inspection du code

## Constats dans le navigateur

| ID | Qualification | Constat | Preuve |
| --- | --- | --- | --- |
| O01 | **OBSERVÉ** | L’URL communiquée affiche l’espace gestionnaire « Localeo Animation » ; le compte commerçant y obtient HTTP 401. Le portail Pro documenté accepte la connexion. | [portail](../visuels/captures-avant/00-portail-fourni-mobile.png), [refus](../visuels/captures-avant/01-portail-fourni-refus-mobile.png), [accueil Pro](../visuels/captures-avant/03-accueil-pro-mobile.png). |
| O02 | **OBSERVÉ** | L’accueil place « Scanner un QR » comme action principale et expose les préparations et invitations plus bas dans la page. Le bas de navigation mobile donne Accueil, Scanner, Animations, Plus. | [mobile](../visuels/captures-avant/03-accueil-pro-mobile.png), [ordinateur](../visuels/captures-avant/10-accueil-pro-desktop.png). |
| O03 | **OBSERVÉ** | L’accueil affiche « 2 animations en cours » et « 1 à venir » ; la liste Animation affiche « En cours (3) » et « À venir (1) ». Une carte classée en cours porte la période 14–16 novembre, antérieure à la date locale du test (18 novembre). L’origine de cet écart n’a pas été diagnostiquée. | [accueil](../visuels/captures-avant/03-accueil-pro-mobile.png), [liste](../visuels/captures-avant/05-animations-mobile.png). |
| O04 | **OBSERVÉ** | La caméra ne démarre pas dans Chromium automatisé sur mobile émulé ni sur ordinateur. La saisie manuelle reste accessible. « not-a-localeo-qr » produit « Erreur de lecture du QRCode du pack. » et le scanner reste disponible. | [mobile](../visuels/captures-avant/04-scanner-mobile.png), [ordinateur](../visuels/captures-avant/12-scanner-desktop.png), [erreur](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png). |
| O05 | **OBSERVÉ** | La boîte Animation contient neuf notifications de test dont une non lue, avec filtres Toutes/À lire/Lues et liens « Voir l’animation » ou « Voir la demande ». Aucun WebPush n’a été reçu pendant l’essai. | [notifications](../visuels/captures-avant/09-notifications-generales-mobile.png). |
| O06 | **OBSERVÉ** | Les invitations chargées sont acceptées ; aucune demande ne nécessite de réponse. La préparation les liste avec dates et accès direct. | [invitations](../visuels/captures-avant/06-invitations-mobile.png), [préparations](../visuels/captures-avant/07-preparation-mobile.png). |
| O07 | **OBSERVÉ** | Le détail Vitrines montre mission, kit, état « commerce prêt », préparation approuvée et contrôlée ; le parcours guidé présente l’étape 4/4. La Tombola à venir indique que les validations ne sont pas ouvertes. | [Vitrines](../visuels/captures-avant/13-detail-vitrines-mobile.png), [préparation](../visuels/captures-avant/16-preparation-vitrines-mobile.png), [Tombola](../visuels/captures-avant/15-detail-tombola-mobile.png). |
| O08 | **OBSERVÉ** | Le guide déplié nomme `flyer-animation.pdf`, distingue son QR d’inscription du QR de validation et liste les consignes. Il affiche la période sous forme d’instants ISO UTC (`…T…Z`) alors que l’interface annonce « heure de Paris ». | [guide](../visuels/captures-avant/21-guide-preparation-mobile.png). |
| O09 | **OBSERVÉ** | Un rechargement de la route scanner dans la session courante reste authentifié ; le message d’erreur QR n’est plus affiché. | [après rechargement](../visuels/captures-avant/20-retour-rechargement-mobile.png). |

## Lecture ciblée de l’implémentation

| ID | Qualification | Ce que le code établit | Source |
| --- | --- | --- | --- |
| C01 | **DÉDUIT** | Les routes protégées couvrent préparation, détail Animation, notifications, invitations et scanner. | `localeo-commercant/src/App.jsx:728-739`, `src/app/routes.js:66-75`. |
| C02 | **DÉDUIT** | Le scanner classe les QR avant action. Un QR Animation est résolu en lecture avant l’écran distinct « Valider cette étape ». Le résultat incertain invite à vérifier le reçu ; succès, rejeu et erreur disposent de messages distincts. | `src/features/validation/ValidationActionWorkspace.jsx:64-90`, `:329-378`, `:615-630`. |
| C03 | **DÉDUIT** | Le kit est lu puis le bouton de téléchargement peut appeler `kit/preparer` avant le fichier. L’action « Je suis prêt » est une commande distincte et dépend des actions autorisées par le serveur. | `src/features/animations/components/AnimationKitSection.jsx:32-75`, `:110-126`, `src/features/animations/api.js:48-57`. |
| C04 | **DÉDUIT** | La page de préparation distingue la participation acceptée, le parcours Vitrines guidé et les autres modèles ; elle expose mission, kit, et lien vers la demande complète. | `src/features/animations/pages/AnimationPreparationPage.jsx:34-48`. |
| C05 | **DÉDUIT** | Le résumé Animation d’accueil charge animations, invitations et notifications et se réactualise quand la page redevient visible. | `src/features/dashboard/useAnimationHomeSummary.js:10-76`. |
| C06 | **DÉDUIT** | Le service worker possède des handlers `push` et `notificationclick`. Les réglages appareil passent par un abonnement WebPush explicite. | `public/sw.js:50-90`, `src/features/notifications/useDeviceNotifications.js:52-53`. |

## Questions UX pour l’étape suivante

Ces points sont des **HYPOTHÈSES**, sans validation terrain : H01, le décalage des compteurs peut faire douter de l’état des animations ; H02, « Télécharger mon kit » n’indique pas avant clic qu’une préparation serveur peut être déclenchée ; H03, les dates UTC brutes du guide peuvent être prises pour des horaires locaux ; H04, la navigation vers une tâche après plusieurs jours peut nécessiter un repère plus direct. Les captures ci-dessus fondent les questions, sans démontrer leur impact utilisateur.
