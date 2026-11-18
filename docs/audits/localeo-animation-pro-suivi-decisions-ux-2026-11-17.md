# Rapport de décisions UX sur le suivi des animations dans Localeo Animation et Localeo Pro

Séance du **17 novembre 2026**. Destinataires : équipes produit, conception et développement Localeo.

L’organisateur doit identifier ce qui bloque son animation et les actions qu’il peut entreprendre. Le commerçant doit retrouver sa tâche, comprendre son résultat et reprendre après interruption. La séance initiale retient cinq améliorations ciblées dans les écrans existants, de la préparation à la fin d’une édition. Le [complément passeport du 17 novembre](#complément-passeport-du-17-novembre-2026) formalise une nouvelle séquence, limitée à la préparation et au déroulement, avec quatre priorités ordonnées.

**Statut : orientations produit retenues en séance, à préciser et à tester.** Ce rapport formalise les arbitrages ; il ne constate pas leur implémentation et ne modifie pas les statuts de la roadmap ni les spécifications canoniques.

Les sections précédant le complément conservent les décisions et le périmètre de la séance initiale. Pour la nouvelle séquence passeport, le complément précise les choix effectivement retenus ; la publication, la clôture et les autres modèles n’y ont pas été réexaminés. Les comptes rendus des autres séances restent distincts.

## Périmètre et méthode

La priorité exprimée est de **savoir quelles actions faire ensuite et repérer les blocages à traiter**. Les trois phases sont concernées : préparation, déroulement et fin. La première étude porte sur le **passeport commerçant** et la **tombola locale avec commerçants invités**, avec les deux perspectives : organisateur dans Localeo Animation et commerçant dans Localeo Pro, principalement sur téléphone.

Pour la préparation, l’objectif prioritaire de l’organisateur est **publier maintenant**. Il souhaite voir les **noms des commerçants concernés et les possibilités d’action pour chacun**. Les autres modèles, dont la tombola publique sans commerçant, ne sont pas évalués par extrapolation. Les interactions avec Live et les coffrets sont examinées lorsqu’elles changent la compréhension du suivi ou des droits restant utilisables.

La séance combine lecture ciblée du code et des documents, scénarios fictifs et arbitrages de l’utilisateur. Les audits antérieurs servent de diagnostic ; leurs recommandations ne sont pas considérées comme adoptées par défaut. Aucun parcours applicatif, test navigateur ou essai avec des utilisateurs réels n’a été exécuté pendant cette séance. Aucun gain de temps n’est mesuré.

Les références locales relevées lors de la formalisation sont : Projet `8b20cf9`, Animation `845d94a`, Commerçant `e60ce30`. Les deux arbres applicatifs sont propres à cette lecture ; ces références ne prouvent pas les versions déployées.

## Constats établis et hypothèses d’usage

Les constats ci-dessous portent sur les sources locales. Les difficultés humaines associées restent des hypothèses à éprouver.

| Constat établi dans les sources | Hypothèse d’usage |
| --- | --- |
| La liste Animation présente une prochaine action et son motif. L’assistant distingue les intervenants ; les noms, échéances et possibilités de relance sont détaillés dans Invitations. | L’organisateur doit rapprocher plusieurs informations avant de savoir qui bloque et comment agir. « En attente des commerçants » peut être compris comme une absence d’action possible pour lui. |
| L’accueil Pro présente une entrée groupée « Répondre aux invitations Animation », qui ouvre une liste avant le détail d’une demande. | Pour retrouver une invitation précise, le commerçant subit un détour et identifie tardivement l’animation concernée. |
| Après acceptation, la demande propose le parcours de préparation. L’entrée d’accueil relative aux invitations ne porte que sur les réponses attendues ; elle ne devient pas une tâche de préparation. | Après interruption, la disparition de l’invitation à traiter peut donner l’impression que tout est terminé. |
| Le scanner Pro distingue résultat confirmé et résultat incertain, avec « Vérifier le résultat ». « Abandonner le scan » reste accessible et réinitialise le contexte courant de vérification. | Quitter peut être compris comme l’annulation de la validation, puis conduire à une nouvelle tentative mal informée. Cela n’établit pas à lui seul un doublon métier. |
| Fin de l’animation présente déjà les blocages, les dossiers, les bénéficiaires et les actions disponibles. Le filtre « À résoudre » existe, mais l’ouverture ordinaire affiche tous les dossiers. | Les dossiers traités peuvent masquer ceux qui demandent encore une action ou une attente externe. |

Preuves de code : [liste des animations](../../../localeo-animation/src/app/components/AnimationsProductivityWorkspace.tsx), [assistant](../../../localeo-animation/src/app/components/AssistantAnimationWorkspace.tsx), [invitations organisateur](../../../localeo-animation/src/app/components/MerchantParticipationTab.tsx), [accueil Pro](../../../localeo-commercant/src/features/dashboard/MerchantHomePage.jsx), [liste des invitations Pro](../../../localeo-commercant/src/features/animations/pages/ParticipationRequestsPage.jsx), [détail de la demande](../../../localeo-commercant/src/features/animations/pages/ParticipationRequestDetailPage.jsx), [préparation du commerce](../../../localeo-commercant/src/features/animations/components/AnimationKitSection.jsx), [scanner utilisé par l’application](../../../localeo-commercant/src/ActionWorkspaces.jsx), [fin de l’animation](../../../localeo-animation/src/app/components/FinAnimationWorkspace.tsx).

## Parcours et passages entre acteurs

| Moment | Organisateur | Commerçant | Passage entre acteurs à rendre lisible |
| --- | --- | --- | --- |
| Invitation et publication | Identifie les réponses manquantes, suit ou relance les sollicitations selon les droits et délais existants. | Retrouve la demande, consulte sa mission et les conditions, puis accepte ou refuse. | La demande attend une réponse ; une relance ne constitue pas cette réponse. Après décision, le suivi organisateur doit être relu. |
| Préparation du commerce | Suit les déclarations de préparation lorsque ce suivi est activé. | Prépare supports et équipe, puis confirme « Je suis prêt » si cette action est proposée. | L’acceptation exprime un engagement ; la déclaration de préparation exprime un autre fait. Leur effet sur publication et ouverture du jeu reste celui des règles existantes. |
| Déroulement | Consulte l’activité et traite les situations relevant de ses droits. | Valide les passages autorisés et vérifie les résultats incertains. | Un message réseau ou une statistique ne remplace pas la confirmation de l’opération individuelle. Les effets d’une validation dépendent du modèle. |
| Fin et lots | Identifie les dossiers à résoudre, agit ou comprend l’acteur attendu, puis termine et archive selon les capacités disponibles. | Effectue les remises ou consommations autorisées lorsque le bénéficiaire se présente. | Information du gagnant, remise d’un lot, réception d’un coffret et consommation de ses prestations sont des faits distincts. |

## Cinq améliorations retenues

Les critères ci-dessous servent à préparer la validation UX. Ils ne créent pas de nouveaux identifiants de critères d’acceptation dans les epics. Les efforts sont des comparaisons qualitatives, à confirmer après examen des données et contrats disponibles.

### 1 Agir sur les commerçants qui bloquent la publication

**Écran et acteur :** explication du blocage de publication dans Localeo Animation, pour l’organisateur habilité. **Difficulté ciblée :** passer du blocage global aux personnes concernées et aux actions possibles.

**Décision retenue :** afficher les noms, la situation de chaque demande et ses actions autorisées directement dans le blocage. La relance s’effectue depuis cet emplacement ; l’annulation reste secondaire, explicite et confirmée. L’option limitée à un lien vers chaque invitation n’a pas été retenue.

Exemple fictif : huit commerçants ont accepté et deux n’ont pas répondu, toutes les autres conditions étant satisfaites. Pour le premier, la relance est disponible ; pour le second, une relance récente impose une attente dont l’échéance doit être compréhensible. Après succès, le retour indique que la relance est envoyée et que la réponse reste attendue.

**Bénéfice attendu :** réduire la recherche et permettre une décision sans détour. **Effort et risque :** supérieur à un simple lien ; les droits, délais, résultats incertains et mises à jour doivent rester fiables dans ce nouvel emplacement. L’urgence de publier ne doit pas transformer l’annulation en action principale.

**Validation proposée :** sans assistance, l’organisateur identifie les deux demandes bloquantes, distingue les possibilités de chacune et comprend qu’une relance ne permet pas immédiatement de publier. Si un commerçant a répondu entre-temps, le suivi reflète l’état relu. Une lecture échouée n’annonce pas la disparition du blocage.

### 2 Ouvrir directement chaque invitation depuis Pro

**Écran et acteur :** rubrique « À traiter » de l’accueil Pro, pour le commerçant autorisé. **Difficulté ciblée :** identifier et ouvrir une invitation précise entre deux clients, même sans avoir vu la notification.

**Décision retenue :** chaque entrée identifie l’animation, présente son échéance de réponse et ouvre directement le détail de l’invitation. Le passage obligatoire par la liste n’est pas retenu. Mission, règlement et décision explicite restent dans la demande ; le lien d’accueil n’accepte rien.

**Bénéfice attendu :** retrouver plus vite la tâche concernée. **Effort et risque :** enrichissement de l’entrée existante et de sa destination ; plusieurs invitations ne doivent pas surcharger l’accueil ni gêner l’accès au scanner, notamment pour un client présentant un coffret.

**Validation proposée :** depuis l’accueil mobile, retrouver et ouvrir la bonne invitation sans passer par la liste, puis identifier l’engagement demandé. Rejouer avec plusieurs invitations et avec un accès ne permettant pas de prendre cette décision.

### 3 Retrouver la préparation après acceptation et interruption

**Écran et acteur :** même rubrique de l’accueil Pro, pour le commerçant ayant accepté. **Difficulté ciblée :** perdre la suite de son travail ou confondre accord et préparation achevée.

**Décision retenue :** lorsque le suivi de préparation est actif et que la préparation reste à confirmer, l’entrée évolue vers « Préparer mon commerce » et ouvre le parcours concerné. Elle reste une tâche jusqu’à la confirmation effective « Je suis prêt », selon l’état et les droits courants. La simple amélioration du message affiché immédiatement après acceptation ne suffit pas à l’objectif de reprise retenu.

Télécharger le kit ne termine pas la préparation. Si le suivi est désactivé, l’accès aux consignes reste utile, sans prétendre connaître l’avancement réel ni imposer une nouvelle confirmation. L’emplacement précis de cet accès sans tâche reste à préciser.

**Bénéfice attendu :** conserver une prochaine action identifiable après interruption. **Effort et risque :** supérieur à une retouche de confirmation ; l’état doit être relu pour éviter une tâche périmée ou une disparition prématurée.

**Validation proposée :** après avoir accepté puis quitté Pro, retrouver les préparatifs, reconnaître que l’accord est déjà enregistré et distinguer kit téléchargé et commerce prêt. Tester aussi une préparation confirmée entre-temps par un autre accès autorisé et une lecture momentanément indisponible.

### 4 Comprendre une validation incertaine et les conséquences de la sortie

**Écran et acteur :** scanner et résultat de validation dans Pro, pour le commerçant ou l’accès salarié habilité. **Difficulté ciblée :** comprendre ce qui s’est produit lorsque la connexion coupe après la confirmation d’un passage.

**Décision retenue :** clarifier l’incertitude, mettre « Vérifier le résultat » en évidence et protéger la sortie par une explication de ses conséquences. Quitter ne signifie pas annuler une validation éventuellement enregistrée. Les mécanismes existants de vérification et de renvoi conditionnel gardent leur autorité.

La reprise depuis une nouvelle entrée « Validation à vérifier » sur l’accueil n’est **pas retenue à ce stade**. Elle reste une hypothèse à tester ; sa fiabilité après fermeture complète n’est pas établie par la séance. Cette décision ne promet donc pas une récupération après fermeture ou redémarrage.

**Bénéfice attendu :** éviter les décisions fondées sur une fausse certitude. **Effort et risque :** modification ciblée des messages et de la sortie ; la distinction entre refus confirmé et résultat inconnu doit rester intacte. Une vérification qui échoue encore conserve l’incertitude.

**Validation proposée :** après une confirmation perdue, le commerçant reconnaît l’état inconnu, choisit la vérification et explique correctement l’effet de la sortie. Aucun message ne lui fait croire que la validation est réussie, annulée ou absente sans preuve correspondante.

### 5 Identifier les opérations restantes avant de terminer une édition

**Écran et acteur :** « Fin de l’animation » dans Localeo Animation, pour l’organisateur. **Difficulté ciblée :** croire que le jeu clôturé et les gagnants informés signifient que toute la gestion est terminée.

**Décision retenue :** ouvrir les dossiers « À résoudre », avec le lot et le bénéficiaire comme repères, puis expliciter la prochaine action et l’acteur attendu lorsqu’ils sont connus. Réutiliser les actions autorisées et les confirmations existantes. L’option limitée au filtre initial n’a pas été retenue.

Exemple fictif : un lot attend son retrait et la réception d’un coffret envoyé n’est pas attestée. L’organisateur distingue ce qu’il peut traiter de ce qui attend un bénéficiaire ou un autre intervenant. Un coffret effectivement remis peut encore contenir des prestations utilisables : leur consommation ne doit pas être présentée comme une condition supplémentaire de fin. Inversement, un e-mail envoyé ne prouve pas la réception.

**Bénéfice attendu :** savoir quels dossiers empêchent de terminer et comment les traiter. **Effort et risque :** enrichissement de la présentation au-delà du filtre existant ; l’acteur attendu ne doit pas être déduit arbitrairement d’un statut générique. « Clôturer ce dossier » ne doit pas devenir un raccourci banal pour faire disparaître un blocage, notamment lorsqu’un bon serait révoqué.

**Validation proposée :** retrouver sans aide les dossiers restants, identifier action personnelle et attente externe, comprendre l’effet d’une décision et distinguer remise, réception et consommation. Si un autre acteur a déjà traité un dossier, la relecture doit permettre de comprendre le nouvel état.

## Règles et responsabilités à préserver

Le backend conserve les règles métier, les habilitations, les transitions et les décisions de disponibilité. Les interfaces présentent ces décisions ; une nouvelle entrée ou une action rapprochée ne donne aucun droit supplémentaire. Lorsque les données ne permettent pas d’identifier un acteur ou un résultat, l’interface doit exprimer cette limite.

- Accepter une invitation, préparer le commerce et ouvrir le jeu restent des étapes distinctes. La déclaration « prêt » conserve son caractère conditionnel au suivi activé.
- Une relance ne vaut pas réponse. Annuler une invitation empêche d’y répondre ; l’effet doit être annoncé avant confirmation.
- Un résultat inconnu ne vaut ni succès ni absence d’enregistrement. Aucun renvoi automatique d’une écriture n’est introduit.
- Clôturer le jeu, terminer l’édition et l’archiver gardent leurs effets propres. Les droits acquis et les possibilités de consultation dans Live et Pro restent gouvernés par leurs règles existantes.
- Les actualisations locales préservent filtres, navigation, saisies et focus. Une réponse ancienne ne doit pas masquer un état plus récent.

Références canoniques : [participation et préparation commerçantes E56](../specifications/epic-56-validation-participation-commercants-animation/README.md), [parcours organisateur E73](../specifications/epic-73-animation-et-ou-coffrets/parcours-organisateur.md), [productivité organisateur E73](../specifications/epic-73-animation-et-ou-coffrets/ux-productivite-organisateur.md), [fin et archives](../specifications/epic-73-animation-et-ou-coffrets/fin-animation-archives.md), [lots et remises](../specifications/epic-73-animation-et-ou-coffrets/gestion-lots-remises.md), [guide commerçant et incidents réseau](../produit/formation/commercant/guide-commercant.md), [conventions de gestion](../architecture/transverse/conventions-backoffice.md).

## Points encore ouverts

1. **Plusieurs tâches sur mobile :** ordre, place et volume des entrées visibles ; conserver la priorité opérationnelle du scanner sans perdre les invitations.
2. **Préparation sans suivi activé :** préciser où retrouver les consignes et comment présenter leur disponibilité sans créer un faux état d’avancement.
3. **Données de responsabilité et de prochaine action :** vérifier les projections disponibles pour les blocages de publication et les dossiers de fin avant de promettre une attribution exacte.
4. **Reprise d’une validation après fermeture complète :** décider de son intérêt à partir des essais et examiner la capacité réelle de récupération avant toute promesse.
5. **Étendue de la recette :** tester les deux modèles étudiés selon leurs capacités et règles propres. Chasse, Juste Prix, Jeu des vitrines et tombola publique nécessitent une séquence distincte. La compréhension des indicateurs de participation pendant le jeu n’a pas été arbitrée dans la séance initiale ; le complément ci-dessous retient une définition et une évolution ciblées sur le passeport.

## Protocole de test proposé

Faire essayer les parcours à des organisateurs et commerçants d’aisance numérique variée. Utiliser des données fictives, un prototype ou un environnement de démonstration maîtrisé. Les relances, décisions et validations sont simulées ou isolées des destinataires et données réels. Le protocole n’a pas été exécuté.

Observer d’abord le parcours actuel, puis les mêmes situations dans la proposition. Donner l’objectif avec les mots de l’utilisateur, sans indiquer le bouton à choisir. Varier l’ordre des variantes pour limiter l’effet d’apprentissage. Utiliser un téléphone pour les commerçants et les équipements habituels des organisateurs ; l’émulation ne remplace pas un essai sur appareil réel.

| Tâche et point de départ | Objectif donné | Réussite observable | Variante défavorable |
| --- | --- | --- | --- |
| 1 Organisateur depuis la liste des animations | « Je veux publier cette animation. Qu’est-ce qui m’en empêche et que puis-je faire ? » | Identifie les demandes nominatives, distingue les actions permises et comprend l’attente après relance. | Une relance vient d’être faite ; une autre demande peut encore être relancée. |
| 2 Commerçant depuis l’accueil mobile, sans notification | « Retrouvez la proposition pour votre commerce et décidez si vous participez. » | Ouvre directement la bonne demande, comprend mission et conditions, puis reconnaît le résultat confirmé de sa décision. | Plusieurs invitations ; échéance dépassée ou accès ne permettant pas la décision. |
| 3 Commerçant après acceptation puis interruption | « Reprenez ce qu’il vous reste à préparer pour cette animation. » | Retrouve les préparatifs et distingue accord, téléchargement et confirmation de préparation. | Suivi désactivé, kit indisponible ou préparation déjà confirmée par un autre accès. |
| 4 Organisateur après une réponse commerçant | « Vérifiez ce qui a changé et ce qu’il reste à faire avant de publier. » | Reconnaît l’état relu et la prochaine action sans perdre son contexte. | L’actualisation échoue ; l’utilisateur comprend que le contrôle est indisponible, pas que le blocage a disparu. |
| 5 Commerçant après confirmation d’un passage | « Dites si ce passage est enregistré et poursuivez avec l’action appropriée. » | Distingue confirmation, refus et incertitude ; vérifie avant de recommencer et comprend l’effet de la sortie. | Réponse perdue puis vérification encore indisponible, avec un autre client qui attend. |
| 6 Organisateur après clôture du jeu et information des gagnants | « Retrouvez ce qui reste à traiter pour terminer cette édition. » | Identifie les dossiers et les acteurs, comprend les décisions possibles et distingue réception du coffret et consommation. | Un dossier vient d’être traité ailleurs ; un coffret remis comporte encore des prestations utilisables. |

Pour la dernière tâche, vérifier aussi la compréhension côté commerçant : un coffret remis mais non entièrement consommé peut conserver des prestations autorisées malgré la fin de son animation. Le libellé d’état ne doit pas faire croire que tous les droits sont éteints. Les effets dans Live restent ceux des transitions existantes.

Mesurer, pour chaque tâche, la réussite sans assistance, les hésitations, erreurs, retours en arrière, changements d’écran et ressaisies. Séparer **temps actif** et **attente** des réponses, traitements ou autres acteurs. Consigner les aides apportées et les verbalisations qui expliquent une confusion ; ne pas réduire le bilan à un temps moyen.

Les essais devront établir les difficultés confirmées, celles qui ne se reproduisent pas, les gains effectivement observés et les limites persistantes. Aucun objectif chiffré de gain n’est adopté par ce rapport.

## Impacts et suite documentaire

Ce tableau décrit la formalisation initiale. Le complément précise notamment le besoin supplémentaire de calcul et de contrat pour l’indicateur du passeport.

| Périmètre | Effet de la formalisation et impact éventuel des décisions |
| --- | --- |
| Projet | Ajout du présent rapport et de son entrée dans l’index des audits. Les orientations sont reliées aux sources canoniques, sans nouvelle epic ni changement de statut de roadmap. |
| Animation | Consommateur futur des décisions 1 et 5 ; vérifier les données de prochaine action, les droits, les attentes et les retours de commande. Aucun code modifié pour ce rapport. |
| Commerçant | Consommateur futur des décisions 2, 3 et 4 ; préserver scanner, capacités des comptes et continuité du travail. Aucun code modifié pour ce rapport. |
| Backend et contrats | Aucun contrat ni invariant modifié par la formalisation. La disponibilité des données nécessaires reste à vérifier avant spécification ; aucun nouvel endpoint ni changement de schéma n’est décidé. |
| Marketplace et Live | Aucun changement direct décidé. Les effets sur participation, affichage des gains et droits acquis doivent être couverts lors de la recette transverse. |
| Documentation fonctionnelle et exploitation | Les guides actuels restent la description du produit existant. Leurs mises à jour suivront les comportements réellement spécifiés et réalisés. |
| Migrations, démonstration et déploiement | Sans changement pour ce rapport. Les besoins de données de test devront couvrir les variantes retenues ; aucune migration, génération réelle ou opération de déploiement n’est déclenchée. |

La suite consiste à préparer les essais et préciser les comportements retenus dans les spécifications concernées, en s’appuyant sur les arbitrages existants. Cette formalisation ne déclenche ni implémentation, ni commit, ni publication applicative.

## Complément passeport du 17 novembre 2026

### Périmètre, décisions et niveau de preuve

La nouvelle séquence porte sur **la préparation et le déroulement d’un passeport commerçant**, avec un responsable associatif bénévole et un commerçant principalement sur téléphone, susceptible d’être interrompu par ses clients. Les deux questions directrices retenues sont « Que reste-t-il à faire, et par qui ? » avant le jeu, puis « Les inscrits jouent-ils, et mon dernier geste a-t-il bien été enregistré ? » pendant le jeu.

Le demandeur a validé les quatre orientations ci-dessous, leur ordre de priorité et la confirmation de sortie limitée aux validations envoyées dont le résultat reste inconnu. Les échanges sur une boulangère interrompue et un client attendant le résultat d’un passage sont des **scénarios fictifs discutés**, pas des essais sur téléphone. Les difficultés humaines et bénéfices restent des hypothèses ; aucun gain chiffré n’a été mesuré, aucun test navigateur ou utilisateur n’a été exécuté et aucune commande métier n’a été déclenchée. Seule la formalisation documentaire a ensuite été demandée.

Références locales : Projet `8b20cf9`, Animation `845d94a`, Commerçant `e60ce30`, Backend `56464443`. Le dépôt Projet contenait déjà des modifications ; les trois dépôts applicatifs consultés étaient propres. Ces références ne prouvent pas les versions déployées.

| Constat de source | Difficulté supposée à éprouver |
| --- | --- |
| Pro possède une entrée « Préparation des animations » et un accès depuis la participation acceptée. L’accueil ne transforme pas l’invitation acceptée en tâche de préparation. | Le commerçant pourrait croire avoir terminé ou ne pas retrouver les préparatifs après interruption. |
| Le suivi organisateur affiche déjà les noms et déclarations de préparation ; le suivi peut être désactivé. | Une déclaration manquante pourrait être prise pour la preuve que le commerce n’est pas installé. |
| Le scanner distingue succès, refus et résultat incertain, avec « Vérifier le résultat » ; la sortie réinitialise le contexte courant. | Le commerçant pourrait interpréter la sortie comme une annulation du passage. |
| « Parcours commencés » compte les exécutions avec un début enregistré ; une commande de démarrage peut précéder une validation chez un commerçant. | Ce compteur pourrait être interprété comme le nombre de participations ayant déjà un passage validé. |

Sources : [accueil Pro](../../../localeo-commercant/src/features/dashboard/MerchantHomePage.jsx), [navigation Pro](../../../localeo-commercant/src/app/merchantNavigation.js), [parcours de préparation](../../../localeo-commercant/src/features/animations/pages/AnimationPreparationPage.jsx), [kit et confirmation](../../../localeo-commercant/src/features/animations/components/AnimationKitSection.jsx), [suivi des préparations](../../../localeo-animation/src/app/components/PreparationTrackingView.tsx), [scanner Pro](../../../localeo-commercant/src/ActionWorkspaces.jsx), [indicateurs affichés](../../../localeo-animation/src/app/components/ExploitationView.tsx), [calcul des métriques](../../../localeo-backend/app/infrastructure/persistence/repositories/exploitation_animation_repository.py), [persistance du démarrage](../../../localeo-backend/app/application/animation_locale/services/jeu_animation.py) et [commande de démarrage du moteur](../../../localeo-backend/app/domaine/animation_locale/moteurs/execution.py).

### Quatre priorités retenues

L’ordre porte sur les priorités produit et les premiers essais à organiser, sans déclencher leur implémentation. Les critères ci-dessous ne sont pas de nouveaux critères d’acceptation canoniques.

| Priorité, écran et acteur | Solution minimale retenue | Bénéfice attendu | Critère de validation |
| --- | --- | --- | --- |
| **1 — Accueil Pro, commerçant** | Dans « À traiter », montrer « Préparer mon commerce — [animation] » avec accès direct, lorsque la participation est acceptée, le suivi actif et la préparation encore à confirmer. | Retrouver son travail après interruption. | Depuis l’accueil, retrouver les consignes sans aide et distinguer acceptation, téléchargement du kit et préparation confirmée. |
| **2 — Scanner Pro, commerçant ou salarié habilité** | Clarifier le résultat inconnu, garder la vérification comme action principale et demander confirmation au moment de quitter une validation envoyée encore incertaine. | Prendre une décision compréhensible au comptoir et expliquer la situation au client. | Vérifier avant de recommencer ; comprendre que quitter n’annule pas une validation éventuellement enregistrée. |
| **3 — Suivi de préparation, organisateur** | Présenter d’abord les commerces dont la préparation reste à confirmer, avec leurs noms et le geste attendu du commerçant dans Pro. | Identifier qui contacter et ce que l’association attend réellement. | Nommer les commerces concernés et distinguer absence de déclaration, état terrain inconnu et conditions d’ouverture du jeu. |
| **4 — Suivi du jeu, organisateur** | Présenter les inscriptions à côté des « Participations avec au moins un passage validé », avec une définition et une fraîcheur explicites ; garder les qualifications accessibles ensuite. | Distinguer inscription et participation attestée chez les commerces. | Expliquer les chiffres sans confondre inscriptions, passages, qualifications et personnes physiques. |

#### 1. Retrouver la préparation dans Pro

La tâche ouvre directement le parcours de l’animation concernée. Elle reste présente après téléchargement du kit : installer les supports et informer l’équipe restent des gestes distincts. Elle quitte « À traiter » après confirmation effective de « Je suis prêt » ; les consignes restent accessibles dans Préparation. Si la confirmation est incertaine, proposer sa vérification sans annoncer une réussite. Une relecture doit tenir compte d’une préparation confirmée depuis un autre accès autorisé.

Si le suivi est désactivé, conserver les consignes sans créer d’obligation de déclaration ni prétendre connaître l’avancement réel. Plusieurs tâches ne doivent pas gêner l’accès au scanner, notamment lorsqu’un client présente un QR d’animation ou de coffret.

L’option consistant seulement à clarifier la liste Préparation n’a pas été retenue comme réponse suffisante à la reprise depuis l’accueil. **Effort et risque :** évolution des lectures et de la présentation à préciser selon les données disponibles, les droits, la pagination et l’actualisation. Afficher éventuellement un téléchargement effectué reste une piste conditionnée à une information fiable ; le clic de téléchargement ne constitue pas à lui seul une preuve de réception du fichier et aucun nouveau suivi de téléchargement n’est décidé.

#### 2. Comprendre le résultat et la sortie du scanner

Le texte proposé pour l’incertitude est :

> **Le passage reste à vérifier**\
> Il a peut-être été enregistré. Vérifiez le résultat avant de recommencer.\
> **Vérifier le résultat**

Si la vérification échoue encore, afficher « Nous ne pouvons pas encore confirmer le résultat. » : l’échec de la lecture ne devient pas un échec du passage. Une nouvelle tentative d’écriture reste soumise aux mécanismes existants de reçu et de renvoi conditionnel ; aucun renvoi automatique n’est introduit.

La confirmation suivante est retenue **uniquement après envoi d’une validation dont le résultat reste inconnu** :

> **Quitter sans connaître le résultat ?**\
> Le passage a peut-être été enregistré. Quitter cet écran ne l’annule pas.\
> **Revenir à la vérification** · **Quitter quand même**

La vérification est l’action principale, mais la sortie reste possible si un autre client attend. Les sorties ordinaires restent directes avant envoi ou après résultat confirmé ; les protections existantes pendant une commande en cours sont préservées. La confirmation ne promet pas de retrouver la vérification après fermeture ou redémarrage.

**Arbitrage :** la confirmation au moment de quitter a été préférée à une seule explication permanente près du bouton. La récupération après fermeture complète et une nouvelle tâche d’accueil dédiée ne sont pas retenues dans ce traitement minimal. Le [rapport de l’autre séance](localeo-animation-pro-suivi-brainstorming-2026-11-17.md) conserve son arbitrage « message seul » ; ce choix distinct n’est pas appliqué à la présente séquence. **Effort et risque :** présentation et gestion de sortie ciblées, sans modification des autorisations ou des décisions métier ; tester la compréhension et la liberté de sortie.

#### 3. Comprendre les confirmations attendues par l’association

La clarification du suivi existant a été retenue plutôt que l’ajout des noms dans une nouvelle synthèse. Exemple fictif : six commerces ont accepté et quatre ont confirmé. Présenter « Préparation des commerces — 4 confirmations sur 6 », puis les deux commerces « À confirmer » et les commerces ayant confirmé, avec leur date.

Employer « Préparation à confirmer » plutôt que « Pas prêt ». Préciser : « Le commerçant confirme dans Pro lorsque ses supports et son équipe sont prêts. » L’absence de déclaration ne prouve pas que les supports ne sont pas installés. Contacter le commerce ne le déclare pas prêt et ne déclenche aucune nouvelle relance automatique. Une actualisation permet de constater sa confirmation.

L’information sur l’ouverture du jeu reste distincte : toutes les préparations confirmées ne signifient pas que la période de jeu a commencé. **Effort et risque :** hiérarchie et formulation a priori limitées, à vérifier sur plusieurs commerces, avec suivi désactivé ou lecture indisponible ; préserver les droits et les conditions de démarrage existantes.

#### 4. Mesurer les participations ayant un passage validé

La séance retient un indicateur défini ainsi : **nombre d’inscriptions distinctes ayant au moins une validation de passage encore valable pour cette animation au moment du calcul**. Chaque participation compte une fois, quel que soit le nombre de commerces visités. Les validations annulées sont exclues ; une participation sans aucune validation encore valable ne satisfait plus ce critère. Ce libellé ne décrit pas une activité « aujourd’hui ».

Exemple fictif : une participation obtient trois validations dans trois commerces ; elle compte pour **une participation avec un passage validé et trois passages validés**. Une inscription familiale reste une inscription : ni ce compteur ni celui des inscriptions ne mesurent automatiquement le nombre de personnes physiques.

Présenter en premier les inscriptions enregistrées et les participations avec au moins un passage validé. Les qualifications restent accessibles pour comprendre la progression vers le tirage. Une valeur indisponible n’est jamais un zéro ; préciser la fraîcheur et éviter une comparaison trompeuse entre chiffres de dates différentes.

**Arbitrage :** expliquer seulement les chiffres existants ne répond pas directement au besoin retenu. Le compteur « Parcours commencés » ne doit pas être renommé pour lui attribuer cette autre signification. **Effort et risque :** calcul backend et contrat supplémentaires à définir et tester, sans modifier les règles de validation, de qualification ou de tirage. La définition vise le passeport ; son application à la tombola, la Chasse, le Juste Prix ou le Jeu des vitrines exige un examen distinct.

### Protocole priorisé et points encore ouverts

Commencer par les deux essais Pro sur téléphone, puis examiner le suivi avec les organisateurs. Comparer les parcours actuels et les propositions avec des personnes d’aisance numérique variée, sur leurs équipements habituels. Utiliser des données fictives dans un prototype ou un environnement de démonstration isolé ; les commandes et communications de l’essai sont simulées ou isolées des données et destinataires réels. Donner les objectifs sans nommer les boutons et varier l’ordre des variantes.

| Rôle et point de départ | Objectif donné | Réussite attendue | Hésitation ou cas défavorable à éprouver |
| --- | --- | --- | --- |
| Commerçant, accueil Pro après acceptation puis interruption | « Retrouvez ce qu’il vous reste à préparer. » | Ouvre les bons préparatifs, distingue accord, kit et confirmation de préparation. | Nouveau départ après téléchargement sans installation ; plusieurs animations ; préparation confirmée ailleurs ; suivi désactivé ; droits insuffisants. |
| Commerçant, réponse perdue après confirmation d’un passage | « Dites si le passage est enregistré et ce que vous allez faire. » | Vérifie et explique au client ce qui est confirmé ou inconnu ; comprend l’effet de la sortie. | Vérification encore impossible, autre client en attente ; comparer avec une sortie avant envoi et après résultat confirmé. |
| Organisateur, fiche de préparation | « Quels commerces devez-vous contacter et qu’attendez-vous d’eux ? » | Identifie les confirmations manquantes et le geste du commerçant, sans conclure à une absence d’installation. | Un commerce a confirmé entre-temps ; actualisation indisponible ; période de jeu non commencée malgré toutes les confirmations. |
| Organisateur, suivi du jeu | « Combien d’inscriptions ont donné lieu à un passage validé ? » | Distingue inscriptions, participations avec passage, total des passages et qualifications. | Plusieurs passages pour la même participation, inscription familiale, dernière validation annulée, donnée absente ou différée. |

Pour chaque tâche, observer la réussite sans assistance, les hésitations, erreurs, retours en arrière, changements d’écran et ressaisies. Mesurer séparément le temps actif et l’attente. **Ce protocole n’a pas été exécuté** ; les réponses du demandeur pendant la séance valent arbitrages produit, pas preuves d’utilisabilité.

Restent à préciser : les états complets et actualisés des tâches Pro, leur place lorsqu’elles sont nombreuses, la fiabilité d’un éventuel repère de téléchargement, les conséquences exactes de la sortie selon le contexte de vérification conservé, et le calcul, contrat, coût et fraîcheur du nouvel indicateur. La récupération après fermeture complète reste une étude distincte. Aucune difficulté humaine n’est encore confirmée par un essai réel.

### Impacts et limites de cette formalisation

- **Projet :** complément du présent rapport et actualisation de son entrée d’index ; les contenus des autres séances et les modifications préexistantes sont conservés. Les critères ci-dessus restent des objectifs de recette, sans changement de spécification ou de roadmap.
- **Commerçant :** futures évolutions de l’accueil et du scanner ; respecter les capacités de chaque compte, la reprise et l’accès aux tâches existantes. Aucun code modifié.
- **Animation :** futures évolutions du suivi de préparation et des indicateurs. Aucun nouveau tableau de bord décidé ; aucun code modifié.
- **Backend et contrats :** le nouvel indicateur nécessite une définition de lecture, un calcul et une exposition fiables à son consommateur. La formalisation ne change aucun contrat ; endpoints, stratégie de calcul et éventuelle persistance restent à préciser. Les règles métier demeurent dans le domaine.
- **Live et coffrets :** aucun changement direct décidé, car la séquence concerne la coordination et le suivi dans Pro/Animation. Préserver la distinction des QR et l’accès au scanner ; aucun effet supplémentaire sur les participations ou droits des coffrets n’est décidé.
- **Documentation fonctionnelle et exploitation :** mises à jour à prévoir selon les comportements effectivement spécifiés puis réalisés ; les guides actuels ne sont pas modifiés pour annoncer des fonctions non livrées.
- **Migrations et générateur de démonstration :** aucun changement pour cette formalisation. Les besoins éventuels dépendront du calcul retenu et des lectures nécessaires ; prévoir les cas de plusieurs animations, passages répétés, validation annulée et confirmation effectuée ailleurs dans les jeux de recette. Aucune génération réelle, migration, publication ou opération de déploiement n’est exécutée.

[Retour à l’index des audits](INDEX.md)
