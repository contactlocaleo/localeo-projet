# Localeo Live — Audit UX du carnet digital

13 septembre 2026 — Analyse du frontend à partir du commit `e02df9e`.

## Choix retenu pour la refonte

Après discussion, l’implémentation conserve deux rubriques distinctes dans un seul carnet : « Mes coffrets » et « Mes animations ». Leur position reste fixe. Le retour habituel ouvre la dernière rubrique consultée ; les liens personnels mènent à l’élément concerné. La découverte est accessible séparément. Les propositions de liste mélangée figurant dans l’audit initial ci-dessous n’ont pas été retenues.

La refonte ajoute le QR directement sur les participations, condense leur état, retire la bienvenue bloquante et enregistre après les actions explicites d’ajout ou d’inscription. Les liens externes sans intention d’ajout explicite conservent un aperçu avec un bouton unique. La conservation reste locale ; la récupération entre appareils et la suppression de champs d’inscription ne sont pas incluses.

## Niveau de confiance et limites des recommandations

Réexamen après discussion : les constats de structure sont vérifiables dans le code ; les effets sur la compréhension et la réussite des utilisateurs restent à mesurer. Aucun test du parcours complet sur téléphone depuis les vrais e-mails et QR distribués n'a été effectué dans cet audit.

| Recommandation | Niveau de confiance | Limite ou validation nécessaire |
| --- | --- | --- |
| Statut personnel et accès au QR visibles dans le carnet | Élevé | Conserver le QR lui-même derrière une action volontaire et respecter les états métier |
| Éviter la bienvenue bloquante avant l'enregistrement | Élevé | Conserver une information courte sur ce qui est enregistré et où le retrouver |
| Une seule décision explicite d'ajout | Élevé sur le principe | Un clic « Consulter » ou un scan ne constitue pas une intention d'enregistrer ; vérifier les vrais libellés et destinations |
| Faire du carnet la destination principale de retour | Cohérent avec l'objectif produit exprimé | Définir séparément première visite, retour habituel et ouverture d'un lien personnel |
| Fusionner coffrets et animations dans deux onglets « Mon carnet / Découvrir » | Hypothèse de conception | Comparer avec une version conservant deux accès directs « Mes coffrets / Mes animations » ; moins d'onglets peut ajouter une étape de filtrage |
| Rendre le téléphone facultatif | Conditionnel | Vérifier son rôle effectif dans l'organisation de l'animation et le contrat backend |

Les spécifications existantes prévoient un aperçu avant confirmation pour les coffrets et un ajout explicite au carnet ([contrat frontend](../../specifications/epic-42-localeo-live/frontend-pwa.md), [arbitrage LIVE-ARB-20](../../specifications/epic-42-localeo-live/registre-arbitrages.md)). Supprimer une confirmation est donc une proposition d'évolution de ce parcours, et non la correction d'un écart à la spécification. Garder un aperçu avec un seul bouton d'ajout lorsque le lien d'entrée est ambigu ou ne présente pas suffisamment le coffret.

Les objectifs chiffrés ci-dessous sont des cibles de prototype, sans garantie d'amélioration. La priorité est la réussite sans aide, la compréhension de l'enregistrement et le temps pour retrouver le QR. Le nombre de clics ne suffit pas à mesurer la facilité d'un parcours ([Nielsen Norman Group, The 3-Click Rule for Navigation Is False](https://www.nngroup.com/articles/3-click-rule/)).

## Décision recommandée

Faire du carnet l’accueil et le centre de Localeo Live. Le service doit permettre de **conserver un coffret ou une participation, retrouver son état et présenter son code** avec un minimum de décisions.

Les actualités, les offres et la découverte locale restent accessibles dans un espace secondaire. Les parcours d’entrée depuis un e-mail ou un QR doivent aboutir à l’élément personnel concerné, avec une confirmation claire de son enregistrement.

## Périmètre et méthode

Audit heuristique du code des parcours actuellement routés : achat → consultation/ajout du coffret ; QR d’animation → fiche publique → inscription → ajout ; retour au carnet ; consultation du statut et présentation du QR. Les recommandations s’appuient également sur des principes UX de visibilité du statut et de présentation progressive des informations.

Les e-mails réellement envoyés, les URL encodées dans les QR distribués et les enregistrements des premiers tests utilisateurs n’ont pas été examinés. Les chemins d’entrée sont donc distingués selon les variantes supportées par le frontend. Les nombres de clics sont des décomptes du chemin nominal dans le code, pas des mesures de sessions réelles. L’incidence du navigateur, des erreurs réseau et des écrans système reste à tester.

## Constats structurants

| Constat dans l’application | Conséquence UX probable | Recommandation |
| --- | --- | --- |
| `/live/` et le démarrage de l’application installée ouvrent le fil d’actualités. | Un retour pour utiliser un coffret ou une participation commence par une navigation supplémentaire. | Ouvrir « Mon carnet » par défaut. Conserver les ouvertures directes vers un élément depuis les liens personnels. |
| La navigation principale comporte Actualités, Coffrets, Animations et Réglages ; l’en-tête expose aussi Marketplace, installation et notifications. | Plusieurs destinations sollicitent l’attention avant l’action recherchée. | Deux destinations principales : « Mon carnet » et « Découvrir ». Réglages et aide dans l’en-tête ; installation proposée au bon moment. |
| Un écran de bienvenue modal apparaît à la première visite de Live, y compris sur une page d’ajout. | L’utilisateur doit découvrir l’application avant de terminer la tâche qui l’a amené. | Retirer cet écran bloquant des liens d’entrée ; introduire le carnet dans la confirmation d’enregistrement. |
| Depuis la fiche d’un coffret, « Ajouter à Localeo Live » conduit à une seconde confirmation d’ajout. | Répétition de l’intention et incertitude sur le moment où l’ajout est effectif. | Une seule action explicite d’ajout, suivie de la validation du lien et de l’enregistrement. |
| L’inscription publique d’une animation conduit à `AddAnimation`, qui demande encore « Ajouter à mon carnet ». | Un utilisateur peut être inscrit sans retrouver sa participation dans le carnet. | Une soumission « M’inscrire et enregistrer » réalise les deux opérations, avec traitement distinct des éventuels échecs. |
| La fiche d’animation rassemble présentation, dates, état, règles, actualités, lots, commerçants, règlement et progression. Le formulaire est rendu dans son pied de page. | Le contenu de découverte reste présent pendant une tâche personnelle. Le focus du formulaire aide à y accéder, mais ne simplifie pas la structure de la page. | Une vue d’inscription courte et une vue de participation centrée sur le statut, le QR et les validations. |
| Le QR du coffret est accessible depuis sa carte ; celui d’une participation nécessite d’ouvrir le détail. | Deux comportements pour une même tâche chez le commerçant. | Un bouton « Présenter mon QR » directement sur les deux types d’éléments. |
| « Mes animations » et « À découvrir » partagent la même page ; une animation peut être sauvegardée sans inscription. | « Dans mon carnet » peut être interprété comme « Je suis inscrit ». | Afficher explicitement « À suivre · Non inscrit » pour une simple sauvegarde, et privilégier les participations actives. |
| Les cartes cumulent plusieurs statuts, compteurs et actions, dont le retrait et les notifications. | Le résultat utile doit être reconstruit à partir de plusieurs indices. | Un statut personnel principal, une information secondaire utile et une action dominante. |
| Le carnet est conservé localement dans IndexedDB ; la sauvegarde transférable est un export/import de fichier dans les réglages. | L’utilisateur peut croire qu’installer l’application suffit à protéger ou synchroniser son carnet. | Expliquer brièvement le stockage réel et rendre la récupération plus simple. Ne promettre aucune synchronisation inexistante. |

## Parcours 1 — Depuis l’e-mail d’un coffret

### Parcours actuels supportés

- **Lien de consultation** : clic dans l’e-mail → fiche du coffret → « Ajouter à Localeo Live » → bienvenue au premier accès → « Ajouter à mes coffrets » → liste des coffrets.
- **Lien direct d’ajout** : clic dans l’e-mail → bienvenue au premier accès → aperçu du coffret → « Ajouter à mes coffrets » → liste des coffrets.

Le dépôt documente la possibilité d’un bouton direct dans l’e-mail ; sa présence et sa place dans les e-mails réellement reçus restent à vérifier.

### Parcours cible

**E-mail : « Ajouter à mon carnet » → vérification et enregistrement → coffret personnel enregistré, prêt à utiliser.**

Le bouton indique déjà l’intention d’enregistrer : une deuxième confirmation n’apporte pas de décision supplémentaire. Afficher ensuite « Coffret ajouté à votre carnet », le nom du coffret, sa validité et « Présenter mon QR ». Le détail des prestations reste accessible depuis la carte ou la fiche personnelle.

Conditions de fonctionnement :

- Une visite issue d’un simple lien « Consulter mon coffret » ne doit pas être assimilée silencieusement à une demande d’ajout. Y proposer un seul bouton d’ajout.
- Si le coffret est déjà présent, ouvrir le même élément et actualiser son accès si nécessaire ; ne pas créer de doublon.
- Confirmer l’ajout après réussite du stockage local. Si le stockage échoue, conserver l’accès au coffret et proposer de réessayer.
- Ne pas faire dépendre l’ajout de l’installation de l’application ou de l’activation des notifications.
- Présenter une option de retrait accessible pour rendre cet ajout réversible, sans afficher le retrait comme une action principale.

## Parcours 2 — Depuis le QR d’une animation

### Parcours actuel, si le QR ouvre la fiche publique

**Scan → présentation de l’animation → ouvrir l’inscription → saisir les coordonnées et accepter le règlement → confirmer l’inscription → bienvenue Live au premier accès → ajouter au carnet → liste des animations.**

Le formulaire impose actuellement prénom, nom, e-mail et téléphone. L’inscription et l’enregistrement local sont deux étapes distinctes.

Si le QR contient déjà un lien personnel de participant, l’entrée est différente : la participation existe. Il faut ouvrir ou enregistrer cet accès, sans repasser par une inscription.

### Parcours cible pour une nouvelle inscription

**Scan du QR d’inscription → écran court de participation → « M’inscrire et enregistrer » → confirmation et participation personnelle.**

L’écran doit donner juste assez de contexte pour décider : nom de l’animation, condition principale de participation, dates utiles et lot ou bénéfice. Le règlement complet reste accessible avant son acceptation. La présentation détaillée, les actualités et les fiches des partenaires restent consultables à la demande.

Après soumission : « Vous êtes inscrit. Votre participation est dans votre carnet », puis « Présenter mon QR » et le nombre de validations requises. Lorsque le QR est ouvert volontairement depuis cette confirmation, aucune visite du détail ne doit être nécessaire.

Points à traiter :

- Vérifier la nécessité de chaque champ avec l’organisateur. Rendre le téléphone facultatif s’il n’est pas indispensable, en coordonnant la modification avec le backend.
- Conserver les choix de communication explicites et facultatifs ; ne pas les confondre avec l’enregistrement au carnet.
- Si l’inscription réussit mais que le carnet ne peut pas être enregistré, annoncer les deux faits distinctement et permettre de réessayer uniquement l’enregistrement.
- Réutiliser le même accès lors d’un retour ; ne pas inciter à se réinscrire pour retrouver son QR.
- Réunir visuellement une animation suivie et sa participation lorsqu’elles concernent le même événement. Les types de stockage actuels permettent des entrées distinctes ; ce cas mérite un test dédié.

## Réduire les clics sans masquer l’essentiel

Convention : clics sur les liens/boutons qui font progresser le parcours ; hors saisie, cases à cocher, scan et ouverture système du lien, défilement, installation facultative et erreurs. Le clic dans l’e-mail est inclus. « Premier accès » inclut la fermeture de la bienvenue Live.

| Tâche et point de départ | Chemin nominal actuel | Cible proposée |
| --- | --- | --- |
| E-mail de consultation → coffret enregistré, premier accès | 4 clics | 2 si le lien reste un lien de consultation |
| E-mail avec bouton direct d’ajout → coffret enregistré, premier accès | 3 clics | 1 clic explicite dans l’e-mail |
| Fiche publique après scan → participation enregistrée, premier accès | 4 clics, plus saisie et acceptation | 1 soumission depuis un écran directement dédié à l’inscription ; 2 si une présentation préalable est nécessaire |
| Accueil Live → QR d’un coffret déjà enregistré, hors bienvenue | 2 clics | 1 clic depuis le carnet |
| Accueil Live → QR d’une participation déjà enregistrée, hors bienvenue | 3 clics | 1 clic depuis le carnet |

Ces cibles ne constituent pas une règle universelle du nombre de clics. Une action supplémentaire est justifiée lorsqu’elle permet une décision utile. L’objectif est de supprimer les confirmations répétées et la recherche d’information avant une action courante.

## Organisation proposée du carnet

Accueil « Mon carnet » avec les coffrets et participations en cours, regroupés en deux sections légères. Ajouter des filtres seulement si le volume réel rend la liste difficile à parcourir. Faire remonter un lot disponible ou une échéance proche ; conserver un ordre stable pour les autres éléments. Les éléments terminés restent accessibles dans « Historique » ; une animation clôturée avec un lot à récupérer reste visible parmi les éléments utiles.

Navigation principale : **Mon carnet · Découvrir**. La commune et les filtres locaux appartiennent surtout à « Découvrir ». Le logo ramène au carnet. Une notification ouvre directement l’élément concerné.

Une carte doit répondre à trois questions : **Qu’est-ce que j’ai ? Où en suis-je ? Que puis-je faire ?**

| Situation | Information principale | Action principale |
| --- | --- | --- |
| Coffret utilisable | Nom ; prestations restantes ; date de validité | Présenter mon QR |
| Participation en cours | Nom ; « 2 validations sur 3 » | Présenter mon QR |
| Participation qualifiée | « Qualifié pour le tirage » ; date du tirage si connue | Voir ma participation |
| Gain attribué mais indisponible | « Gagnant · Lot en préparation » | Voir mon lot |
| Gain disponible | « Gagnant · Lot disponible » | Ajouter mon lot au carnet |
| Animation enregistrée sans inscription | « À suivre · Non inscrit » | M’inscrire, si les inscriptions sont ouvertes |
| Participation non gagnante | « Non gagnant », uniquement après confirmation du résultat par l’API | Voir le résultat |
| Coffret consommé | « Coffret utilisé » | Voir l’historique |

Les libellés et actions doivent respecter l’état réellement fourni par le service. L’absence de gain ne prouve pas un résultat non gagnant. Une animation clôturée ne dit pas, à elle seule, si l’utilisateur a gagné. La possibilité de continuer des validations après qualification dépend des règles de l’animation.

La correction récente du badge « Gagnant » répond au manque de visibilité. La prochaine étape UX est de condenser la lecture : par exemple « Gagnant · Lot disponible » prend la priorité sur « Inscription confirmée », « Qualifié », « 100 % » et « Clôturée » affichés simultanément.

La vue personnelle commence par le statut, l’action et les validations/prestations. Les actualités, lots de présentation, détails des partenaires et règlement passent ensuite. Les conditions nécessaires à la participation restent visibles avant l’inscription. C’est une application de la [présentation progressive des informations](https://www.nngroup.com/articles/progressive-disclosure/), qui réserve le premier niveau aux besoins fréquents.

## Conserver, installer, retrouver

Employer un vocabulaire constant : **carnet**, **coffret**, **participation**, **présenter mon QR**. Éviter l’alternance entre carnet, bibliothèque et passeport pour désigner le même espace.

Après un premier ajout réussi, proposer discrètement « Ajouter Localeo Live à mon écran d’accueil », avec « Plus tard ». Expliquer le stockage actuel en une phrase : « Votre carnet est enregistré dans ce navigateur. Conservez votre e-mail pour retrouver ce coffret. » La phrase de récupération doit être adaptée aux participations et au lien réellement envoyé.

Tester le parcours complet sur appareil réel : lien reçu dans Gmail ou Outlook, navigateur ouvert, installation éventuelle, fermeture, puis réouverture. Le stockage local impose de vérifier cette continuité ; une promesse de récupération automatique entre navigateurs ou appareils serait prématurée.

À moyen terme, proposer une récupération par lien personnel simple, sans imposer la création d’un compte avant le premier enregistrement. L’export de fichier reste une possibilité avancée ; il ne devrait pas porter à lui seul la promesse de récupération grand public. Ce chantier dépend de la gestion des accès côté backend.

En cas de réseau indisponible, conserver une représentation identifiable des éléments déjà enregistrés et proposer « Réessayer ». La liste des coffrets assimile actuellement tout échec de résolution à « Accès expiré » : distinguer une panne de réseau d’une expiration évite d’inciter au retrait d’un coffret encore valide. Ne promettre l’utilisation hors connexion des QR qu’après validation de leur fonctionnement et des contraintes d’accès.

## Ordre de mise en œuvre

| Priorité | Lot | Critère d’acceptation |
| --- | --- | --- |
| P0 | Entrées e-mail et QR sans bienvenue bloquante ; une seule décision d’enregistrement | L’élément est présent à l’arrivée, sans seconde confirmation d’ajout ; erreurs de stockage et d’inscription distinguées |
| P0 | Carnet en accueil et accès direct aux QR | Après réouverture, présenter le QR d’un élément visible demande un clic |
| P0 | Cartes personnelles allégées | Nom, état pertinent et action sont identifiables sans ouvrir le détail ; retrait et préférences passent en actions secondaires |
| P1 | Vue d’inscription et vue personnelle dédiées ; découverte regroupée | Aucune traversée du contenu éditorial nécessaire pour s’inscrire, connaître son résultat ou présenter son QR |
| P1 | Installation différée, récupération et erreurs compréhensibles | Un utilisateur peut fermer puis retrouver son élément ; une panne réseau n’est pas annoncée comme une expiration |
| P2 | Récupération entre appareils et autres améliorations de confort | Parcours défini et validé avec le backend et les appareils cibles |

Le premier lot peut conserver l’identité visuelle et les composants existants. Le gain prioritaire vient de l’ordre des écrans, de la fusion des étapes d’ajout et de la hiérarchie des actions.

## Protocole de validation proposé

Faire une première comparaison qualitative avec 5 à 8 personnes de niveaux d’aisance numérique différents. Ce groupe sert à repérer les difficultés ; il ne fournit pas une estimation statistique du taux de réussite de tous les clients.

Tâches sans guider les clics :

1. « Vous venez de recevoir ce coffret. Gardez-le pour l’utiliser plus tard. »
2. « Vous voyez cette animation chez un commerçant. Inscrivez-vous et gardez votre participation. »
3. Fermer l’application, changer de tâche, puis demander : « Vous êtes chez le commerçant. Montrez votre code. »
4. « Le tirage a eu lieu. Dites-moi si vous avez gagné et ce que vous pouvez faire. »
5. « Vous avez fermé le navigateur. Retrouvez votre coffret. » Tester aussi le chemin d’installation choisi par la personne.

Mesurer : réussite sans aide, temps jusqu’à l’enregistrement, temps pour afficher le QR, clics de progression, retours en arrière, erreurs et hésitations. Demander « Est-ce enregistré ? Où le retrouverez-vous ? » pour vérifier la compréhension.

Cibles de conception à valider : QR en un clic depuis un carnet déjà ouvert ; aucun écran facultatif avant l’enregistrement ; confirmation comprise sans aide ; statut gagnant reconnu sans ouverture du détail. Compléter les événements d’inscription existants par le succès effectif de l’enregistrement local : une inscription réussie ne suffit pas à prouver que le carnet est utilisable.

## Références de l’audit

Code examiné :

- [Accueil, navigation, bienvenue, ajout et carnet des coffrets](../../../../localeo-marketplace/src/live/LiveApp.jsx)
- [Manifeste et destination d’ouverture](../../../../localeo-marketplace/public/live/manifest.webmanifest)
- [Entrée depuis la fiche coffret](../../../../localeo-marketplace/src/pages/CoffretInstancePage.jsx)
- [Fiche publique d’animation et passage à l’inscription](../../../../localeo-marketplace/src/pages/AnimationPublicPage.jsx)
- [Formulaire d’inscription](../../../../localeo-marketplace/src/components/AnimationRegistrationForm.jsx)
- [Entrée personnelle d’une participation](../../../../localeo-marketplace/src/pages/AnimationParticipantPage.jsx)
- [Liste des animations personnelles et découverte](../../../../localeo-marketplace/src/live/LiveAnimations.jsx)
- [Structure du détail d’animation](../../../../localeo-marketplace/src/components/AnimationDetailView.jsx)
- [Conservation locale et export/import du carnet](../../../../localeo-marketplace/src/live/liveLibrary.js)
- [Contrat documenté des liens d’e-mail](../../specifications/epic-42-localeo-live/frontend-pwa.md)

Principes externes : rendre l’état du système visible et utiliser des termes familiers ([Nielsen Norman Group, heuristiques d’utilisabilité](https://www.nngroup.com/articles/ten-usability-heuristics/)) ; réserver les informations secondaires à une consultation volontaire ([Nielsen Norman Group, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)) ; justifier chaque information demandée dans un formulaire ([GOV.UK Design System, Question pages](https://design-system.service.gov.uk/patterns/question-pages/)).
