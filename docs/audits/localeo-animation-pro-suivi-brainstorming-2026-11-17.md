# Suivi des animations — audit et décisions de brainstorming UX

Séance du **17 novembre 2026**. Périmètre : Localeo Animation pour une association de commerçants et Localeo Pro pour des commerçants de bouche, principalement sur téléphone.

**Statut : orientations retenues en séance, à préciser et à tester.** Ce document ne constate pas leur implémentation et ne modifie ni les spécifications canoniques ni les statuts de la roadmap. Les cinq pistes ci-dessous répondent à des difficultés d'usage supposées ; aucune n'a été confirmée par un essai auprès d'utilisateurs réels.

**Suivi du 18 novembre 2026 :** le demandeur a choisi explicitement ce rapport
pour sa mise en œuvre, avec **message explicatif sans confirmation de sortie**
au scanner. L’évolution [E73-EVO-SUIVI-ANIMATION, SA-01 à SA-07](../specifications/epic-73-animation-et-ou-coffrets/parcours-organisateur.md#évolution-du-18-novembre-2026--suivi-animation-et-pro)
porte la spécification, la réalisation et les preuves. Les constats et limites
de la séance initiale restent conservés ci-dessous ; les autres rapports ne sont
pas adoptés par cette demande.

## Objectif, périmètre et méthode

L'objectif est d'aider chaque acteur à comprendre l'état d'une animation, savoir quoi faire, distinguer son action de l'attente d'un autre acteur, comprendre le résultat et reprendre après interruption. La priorité choisie est de **comprendre ce qui bloque une animation**, sur les trois phases : préparation, déroulement et fin. Les modèles représentatifs désignés sont la tombola locale avec commerçants invités, le passeport commerçant et le Juste Prix local.

La séance s'appuie sur une lecture ciblée des sources et des spécifications, des scénarios fictifs et des arbitrages du demandeur. Les audits existants sont utilisés comme éléments de diagnostic, sans adoption automatique de leurs recommandations. Aucun écran n'a été consulté dans une application, aucun test navigateur ni essai utilisateur n'a été réalisé, et aucune commande métier n'a été déclenchée. Aucun gain chiffré n'a été mesuré. La simulation ne remplace pas un essai avec des utilisateurs réels.

Le scénario principal concerne la préparation d'une tombola avec une boulangerie ayant accepté et une boucherie en attente de réponse. Les autres phases ont été examinées à partir d'exemples fictifs. Les règles propres au passeport et au Juste Prix doivent encore être vérifiées dans des parcours complets ; le [guide d'exploitation](../specifications/epic-55-moteur-animation/exploitation-moteur.md#juste-prix-local--e77) décrit le Juste Prix comme implémenté localement mais encore inactif. La tombola publique sans commerçant n'est pas évaluée par extrapolation.

Références locales relevées lors de la formalisation : Projet `8b20cf9`, Animation `845d94a`, Commerçant `e60ce30`. Les arbres applicatifs étaient propres lors de cette lecture ; le dépôt documentaire comportait déjà des modifications. Ces références ne prouvent pas les versions déployées.

Le [rapport d'une séance antérieure](localeo-animation-pro-suivi-decisions-ux-2026-11-17.md) est conservé. Les orientations de la présente séance sont tracées ici séparément ; en particulier, le demandeur a choisi pour la validation incertaine un **message clarifié seul**, sans confirmation supplémentaire de sortie.

## Parcours actuel et passages entre acteurs

| Moment | Association organisatrice | Commerçant | Passage à comprendre |
| --- | --- | --- | --- |
| Préparation et publication | Consulte l'assistant, puis les invitations pour identifier les demandes et les actions disponibles. | Retrouve l'invitation, lit la mission et les dates, puis accepte ou refuse. | Une relance ne vaut pas réponse. Une demande envoyée en attente peut empêcher la publication ; la liste des conditions applicables reste celle du serveur. |
| Préparation du commerce | Suit les déclarations de préparation si le suivi est actif. | Après acceptation, accède aux consignes et au kit ; si l'action est proposée, confirme ensuite « Je suis prêt ». | Accepter, télécharger le kit et déclarer le commerce prêt sont des faits distincts. Selon les règles existantes, le suivi actif peut conditionner l'ouverture du jeu. |
| Déroulement | Consulte le suivi de l'animation et les indicateurs disponibles. | Effectue les validations autorisées ; si le résultat est incertain, peut vérifier le reçu. | Une statistique ne confirme pas une opération individuelle. Une réponse réseau incertaine ne prouve ni succès ni absence d'enregistrement. |
| Fin et lots | Examine les dossiers et blocages, les actions permises et les étapes restantes. | Effectue les opérations de remise ou de consommation autorisées selon son rôle. | Clôture du jeu, information du gagnant, remise d'un lot et utilisation des prestations d'un coffret sont des faits distincts. |

Sources : [règles de participation et préparation](../specifications/epic-56-validation-participation-commercants-animation/README.md), [assistant organisateur](../../../localeo-animation/src/app/components/AssistantAnimationWorkspace.tsx), [invitations organisateur](../../../localeo-animation/src/app/components/MerchantParticipationTab.tsx), [détail de l'invitation Pro](../../../localeo-commercant/src/features/animations/pages/ParticipationRequestDetailPage.jsx), [préparation Pro](../../../localeo-commercant/src/features/animations/pages/AnimationPreparationPage.jsx), [scanner Pro](../../../localeo-commercant/src/ActionWorkspaces.jsx) et [fin de l'animation](../../../localeo-animation/src/app/components/FinAnimationWorkspace.tsx).

## Constats de sources et hypothèses à tester

| Constat dans les sources locales | Hypothèse d'usage, non confirmée |
| --- | --- |
| L'assistant distingue notamment les intervenants ; la rubrique Invitations présente les noms, états, échéances et possibilités de relance. | L'association peut devoir rapprocher plusieurs écrans pour identifier la personne concernée et l'action possible. |
| L'accueil Pro regroupe les invitations en attente sous « Répondre aux invitations Animation » ; ce lien ouvre une liste. | Un commerçant peut identifier tardivement la bonne animation lorsqu'il a plusieurs demandes. |
| Après acceptation, le détail ouvre le parcours de préparation ; la liste de préparation présente les participations acceptées. L'entrée d'accueil dédiée aux réponses en attente ne devient pas une tâche de préparation. | Après interruption, le commerçant peut croire que son travail est terminé ou ne pas retrouver la suite. |
| Le suivi organisateur affiche « Inscrits », « Parcours terminés », « Qualifiés » et « Preuves effectives ». Certaines statistiques d'accompagnement sont datées et peuvent être différées. | L'association peut confondre des personnes avec des validations ou utiliser un chiffre sans en comprendre la portée ou la fraîcheur. |
| Le scanner propose « Vérifier le résultat » en cas de validation non confirmée ; « Abandonner le scan » reste accessible. | Quitter pourrait être compris comme une annulation de l'opération, sans que cela établisse un doublon métier. |
| L'écran de fin propose les dossiers et un filtre « À résoudre ». Le rapport antérieur constate une ouverture ordinaire sur tous les dossiers. | Les dossiers traités peuvent rendre moins visibles ceux qui attendent encore une action ou une réponse. |

Sources complémentaires : [accueil Pro](../../../localeo-commercant/src/features/dashboard/MerchantHomePage.jsx), [kit commerçant](../../../localeo-commercant/src/features/animations/components/AnimationKitSection.jsx), [suivi organisateur](../../../localeo-animation/src/app/components/ExploitationView.tsx), [audit de pilotage](animation/localeo-animation-utilisabilite-pilotage-2026-11-17.md) et [rapport antérieur](localeo-animation-pro-suivi-decisions-ux-2026-11-17.md). Les constats portent sur le code lu, pas sur le comportement observé d'une personne ni sur l'état déployé.

## Cinq améliorations retenues

Les critères suivants préparent une validation UX ; ils ne créent pas de nouveaux critères d'acceptation canoniques. Les efforts sont qualitatifs et doivent être confirmés avec les producteurs et consommateurs des données.

### 1. Identifier les commerçants qui bloquent la publication

- **Écran et acteur :** explication du blocage dans Animation, pour l'association habilitée.
- **Problème supposé :** passer du blocage global aux commerçants concernés et aux actions possibles.
- **Décision :** combiner la présentation des noms, situations et actions autorisées dans le blocage avec un lien vers le suivi complet des invitations. Montrer la prochaine possibilité de relance lorsqu'elle est connue. L'annulation reste explicite, avec ses conséquences et sa confirmation existante.
- **Bénéfice attendu :** comprendre qui est attendu et agir sans recherche inutile. **Effort et risque :** enrichissement du blocage ; vérifier les données disponibles, droits, échéances, relectures et résultats incertains, sans fabriquer un responsable.
- **Critère de validation :** l'association identifie la demande en attente, sait si une relance est possible et comprend qu'elle ne constitue pas une réponse. Si le commerçant répond entre-temps, une relecture permet d'observer le nouvel état ; une lecture échouée ne fait pas disparaître le blocage.

### 2. Retrouver une invitation et reprendre la préparation

- **Écran et acteur :** accueil et préparation dans Pro, pour le commerçant autorisé.
- **Problème supposé :** retrouver une demande précise et sa suite après interruption.
- **Décision :** combiner des libellés explicites sur la suite et des accès directs depuis l'accueil à chaque invitation et préparation concernée. Lorsque le suivi est actif et la préparation reste à confirmer, proposer « Préparer mon commerce » selon l'état et les droits relus. Si le suivi est désactivé, conserver l'accès aux consignes sans inventer une tâche de confirmation ni un état de préparation.
- **Bénéfice attendu :** retrouver la bonne tâche entre deux clients. **Effort et risque :** états et permissions doivent rester fiables ; plusieurs entrées ne doivent pas encombrer l'accueil ou gêner l'accès au scanner. L'emplacement des consignes sans suivi reste à préciser.
- **Critère de validation :** après acceptation, interruption et retour sur téléphone, le commerçant retrouve la bonne animation et distingue accord, téléchargement du kit et déclaration « prêt » ; une préparation confirmée ailleurs ne reste pas affichée comme à faire après relecture.

### 3. Comprendre les chiffres de participation

- **Écran et acteur :** suivi dans Animation, pour l'association.
- **Problème supposé :** « combien de personnes ont participé ? » peut désigner plusieurs populations ou événements.
- **Décision :** combiner des questions concrètes (« combien se sont inscrits ? », « combien ont joué ? », « combien sont qualifiés ? ») et une définition courte de chaque indicateur, adaptée au modèle. Ne présenter un chiffre que si la donnée correspondante et sa définition sont fiables et disponibles.
- **Bénéfice attendu :** choisir le chiffre qui répond à la question et comprendre son périmètre. **Effort et risque :** les définitions et la fraîcheur doivent être vérifiées auprès des producteurs ; une donnée indisponible n'est pas zéro et une statistique différée ne doit pas paraître instantanée.
- **Critère de validation :** devant une tombola fictive avec 100 inscrits, 60 personnes qualifiées et 80 validations, l'association distingue les trois chiffres et explique que 80 validations ne représentent pas nécessairement 80 personnes. Les valeurs sont illustratives, pas des résultats mesurés.

Dans la [tombola locale](../specifications/epic-53-tombola-locale/README.md), la première validation effective qualifie le participant ; des validations suivantes peuvent alimenter les statistiques sans ajouter de chance. Pour le passeport, l'inscription et la fin du parcours sont distinctes. Pour le [Juste Prix](../specifications/epic-77-juste-prix-local/parcours-regles.md), une inscription ne vaut pas automatiquement réponse ou qualification ; les passages dépendent de la configuration. Ne pas extrapoler un même indicateur à tous les modèles.

### 4. Clarifier une validation incertaine

- **Écran et acteur :** scanner Pro, pour le commerçant ou le salarié effectivement habilité.
- **Problème supposé :** après une coupure, le commerçant pourrait prendre une absence de confirmation pour un échec ou une annulation.
- **Décision :** clarifier le message : le résultat n'est pas encore connu et doit être vérifié avant de recommencer. Le demandeur retient le message seul, sans nouvelle confirmation de sortie. Les mécanismes existants de reçu et de renvoi conditionnel restent inchangés.
- **Bénéfice attendu :** favoriser une décision fondée sur le résultat relu. **Effort et risque :** modification ciblée ; vérifier si le message suffit alors que « Abandonner le scan » reste accessible. La reprise après fermeture complète n'est pas promise.
- **Critère de validation :** après une réponse perdue, le commerçant reconnaît l'incertitude et choisit « Vérifier le résultat ». Si la vérification échoue, l'incertitude persiste ; aucun succès, échec ou annulation n'est annoncé sans preuve.

### 5. Repérer les opérations restantes en fin d'animation

- **Écran et acteur :** « Fin de l'animation » dans Animation, pour l'association.
- **Problème supposé :** les dossiers résolus peuvent masquer ceux qui attendent encore une action ou une réponse.
- **Décision :** ouvrir sur le filtre « À résoudre », en conservant l'accès à tous les dossiers ; expliquer la prochaine action et l'acteur attendu lorsque les données les établissent.
- **Bénéfice attendu :** distinguer une action de l'association d'une attente externe. **Effort et risque :** vérifier que la donnée permet d'attribuer correctement l'action et ne pas transformer la clôture d'un dossier en raccourci pour masquer un blocage.
- **Critère de validation :** l'association retrouve un lot restant à remettre, identifie ce qu'elle peut faire ou ce qu'elle attend du bénéficiaire, et distingue information du gagnant, remise et utilisation ultérieure d'un coffret.

## Points ouverts et règles à préserver

1. Vérifier les projections, droits, pagination et fraîcheur nécessaires aux noms, actions et états des invitations et des dossiers de fin ; une donnée inconnue reste explicitement inconnue.
2. Définir par modèle ce que signifie « avoir joué », la source du chiffre et la date de calcul ; ne pas confondre personnes, réponses, passages, qualifications et validations. Tester le passeport et le Juste Prix selon leurs capacités effectives.
3. Préciser l'accès aux consignes lorsque le suivi de préparation est désactivé et l'organisation de plusieurs tâches sur l'accueil mobile.
4. Tester si le message seul suffit en cas de résultat incertain ; la reprise après fermeture complète est une question ouverte, sans promesse de récupération.
5. Garder les règles métier et habilitations dans le backend ; aucun nouveau droit ni automatisme ne découle de ces orientations. Préserver les confirmations existantes, les relectures après résultat incertain et les formulaires, filtres, navigation et focus lors des actualisations locales.

## Protocole proposé — non exécuté

Faire essayer les parcours actuels puis les propositions à des responsables d'associations et à des commerçants de bouche d'aisance numérique variée. Utiliser des données fictives et un prototype ou environnement de démonstration maîtrisé ; les invitations, relances, décisions et validations sont simulées ou isolées des destinataires et données réels. Formuler les objectifs sans indiquer les boutons, varier l'ordre des variantes et utiliser les équipements habituels, notamment des téléphones physiques pour les commerçants.

| Rôle et départ | Objectif donné à la personne | Critère de réussite | Variante ou preuve à organiser |
| --- | --- | --- | --- |
| Association, liste des animations | « Je veux publier la tombola : qu'est-ce qui m'en empêche et que puis-je faire ? » | Identifie la boucherie en attente, l'action autorisée et l'attente qui subsiste. | Relance récente, droit insuffisant ou réponse arrivée entre-temps ; une lecture indisponible ne devient pas un succès. |
| Commerçant, accueil mobile sans notification | « Retrouvez l'invitation pour votre commerce et décidez si vous participez. » | Trouve la bonne animation, comprend mission et échéance et reconnaît le résultat confirmé. | Plusieurs invitations ou échéance dépassée ; observer les détours et la compréhension. |
| Commerçant, retour après acceptation | « Reprenez ce qu'il vous reste à préparer. » | Retrouve les consignes et distingue son accord du commerce prêt. | Suivi désactivé, kit indisponible ou préparation déjà confirmée par un autre accès autorisé. |
| Association, après réponse du commerçant | « Vérifiez ce qui a changé et si vous pouvez publier. » | Relit la réponse et vérifie les autres conditions plutôt que de supposer que la publication est autorisée. | Une autre condition bloque ou l'actualisation échoue. |
| Association, suivi en cours | « Combien de personnes se sont inscrites, ont joué et sont qualifiées ? » | Choisit les données disponibles et explique leur périmètre sans confondre personnes et validations. | Comparer tombola, passeport et Juste Prix selon les données disponibles ; statistique retardée ou absente. |
| Commerçant, validation après coupure | « Vérifiez si la validation a été enregistrée. » | Reconnaît le résultat inconnu et utilise la vérification avant une nouvelle tentative. | La vérification échoue encore ; observer aussi l'interprétation de « Abandonner le scan ». |
| Association, jeu clôturé | « Retrouvez ce qu'il reste à faire pour les lots. » | Identifie dossier, prochaine action et acteur attendu, sans confondre gagnant informé et lot remis. | Un autre acteur a déjà traité le dossier ; un coffret remis contient encore des prestations utilisables. |

Pour chaque tâche, observer la réussite sans assistance, hésitations, erreurs, retours en arrière, changements d'écran et ressaisies. Mesurer séparément le temps actif et les attentes. Consigner les observations, les simulations et les limites ; ne pas annoncer de gain avant mesure. La recette sur appareil et auprès d'utilisateurs réels reste à organiser.
