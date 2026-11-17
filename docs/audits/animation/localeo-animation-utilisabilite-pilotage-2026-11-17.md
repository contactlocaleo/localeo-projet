# Localeo Animation utilisabilité et pilotage

Audit du **17 novembre 2026**, rattaché à **E73-AUDIT-UX-PILOTAGE-20261117**.
Objectif : permettre à un organisateur de comprendre l’état de son animation,
identifier l’action utile et l’effectuer avec un minimum d’hésitation, sur
ordinateur, tablette et téléphone.

**Diagnostic réévalué à la demande de l’utilisateur : la priorité est la continuité
du parcours de gestion d’une animation.** Le premier audit donnait trop de poids
aux corrections locales et pas assez aux passages entre préparation, publication,
suivi et fin. Les outils existent, mais plusieurs raccordements demandent encore
à l’organisateur de retrouver lui-même le bon écran et la prochaine tâche.

La cible est un espace d’animation qui ouvre le travail pertinent, mène chaque
action à son emplacement exact et permet de reprendre après une interruption.
Elle doit s’appuyer sur l’Assistant, le suivi et le guide de fin existants. L’ajout
d’un tableau de bord intermédiaire n’est pas retenu comme solution par défaut.

**Complément demandé sur les appareils mobiles :** le téléphone et la tablette
deviennent des conditions de réussite de chaque lot du parcours central. La cible
est de pouvoir préparer, publier, intervenir et terminer une animation au toucher,
avec les mêmes droits et conséquences explicites. L’adaptation de la largeur seule
ne démontre pas cette utilisabilité ; le clavier, le paysage et les interruptions
doivent également être éprouvés.

**Décision utilisateur ajoutée après l’audit :** tous les modèles doivent partager
les mêmes codes UX de création. La
[règle canonique E73-EVO-CREATION-UX-COMMUNE et ses critères CU-01 à CU-06](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md#règle-du-17-novembre-2026--création-homogène-des-animations)
sont validés et spécifiés, avec réalisation et recette encore à effectuer.
Ils complètent R02/R06 ; les autres recommandations ne sont pas adoptées par
cette seule décision.

Ce rapport présente **six axes de parcours R01 à R06**, puis conserve les
**12 constats locaux U01 à U12** du premier passage. L’ordre de traitement révisé
remplace la priorité initialement donnée à une succession de retouches. Ce sont
des propositions d’audit, distinctes de la règle de création validée ci-dessus.
Aucun code applicatif ni statut d’epic n’est modifié. Les améliorations du 12 novembre restent suivies dans
[E73-EVO-ANIMATION-PRODUCTIVITE](../../specifications/epic-73-animation-et-ou-coffrets/ux-productivite-organisateur.md).

## Périmètre et preuves

Acteurs : responsable, gestionnaire d’animation et lecteur pour les consultations
autorisées. Parcours principal : retrouver une animation, préparer sa publication,
suivre les participations, ajuster les dates et inscriptions, traiter un incident,
clôturer puis rejoindre les opérations de fin. Accès au compte et choix d’un
modèle sont examinés comme points d’entrée.

Références : [parcours SaaS E73](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md),
[conception du moteur](../../specifications/moteur-animation/conception-technique.md),
[conventions de lecture locale](../../architecture/transverse/conventions-backoffice.md#recherche-et-actualisation-ciblée-des-résultats)
et [audit du 12 novembre](localeo-animation-ux-productivite-2026-11-12.md).
La roadmap indique les sept lots de productivité implémentés et AP-22 partiellement
vérifié : les constats historiques ne sont pas repris comme des défauts actuels.

- **C — code actuel** : Animation `74a45f27bd66caa219b56b5d86e191ee513351d4`,
  Projet `2c985737ec5221179fcb98f85bad4ce0d308e7c7` avant ce rapport. Arbres propres
  au début de la première revue. Backend `20ec49c92690d5078ec697c527f1a20054c9a4d1` :
  la réévaluation examine aussi la politique de recommandation et la construction
  de l’Assistant, sans audit exhaustif des règles métier.
- **V — rendu local** : captures produites par les recettes existantes sur API
  simulée, puis inspectées. Exploitation à 1280/390 px ; Assistant à 1600/390 px
  et 320 px avec texte à 200 %. Ces captures ne décrivent pas un déploiement TEST.
  Le complément mobile ajoute des recettes et captures à 390 × 844, 844 × 390,
  768 × 1024 et 1024 × 768 pixels CSS, avec contexte tactile Chromium. Les
  interactions automatisées ne constituent pas un essai au doigt sur appareil.
- **H — hypothèse d’usage** : difficulté de compréhension, temps de tâche ou
  bénéfice attendu. Aucun test avec organisateurs ni gain de productivité mesuré.

Deux contre-revues indépendantes ont examiné les extraits transmis : pilotage et
accès/navigation/création. Elles n’avaient pas d’accès autonome aux fichiers et
ne constituent pas des recettes supplémentaires. Une nouvelle contre-revue du
parcours central a notamment remis en cause l’utilité d’un accueil supplémentaire
et confirmé la nécessité de distinguer étape du cycle et interventions courantes.

L’accès au navigateur ouvert a été interrompu par l’outil, faute de pouvoir
vérifier son URL. Aucun parcours distant n’a donc été observé pendant cet audit.
Les commandes des recettes agissent exclusivement sur des données synthétiques.
Téléphone physique, lecteur d’écran, contrastes, rôles réels et connexion réelle
restent hors des preuves produites ici. L’audit n’attribue pas de note globale
d’utilisabilité ou de conformité accessible.

## Contre-audit du parcours central

### Ce que la réévaluation change

- **U01 à U04 restent à traiter**, notamment la protection de la saisie. Leur
  correction seule ne rendrait pas le parcours complet suffisamment guidé.
- **La présence de quatre groupes n’établit pas leur intuitivité.** Le critère
  principal devient la capacité à accomplir une tâche sans explorer ces groupes.
  Leur suppression n’est pas davantage justifiée par les preuves actuelles.
- **La fin n’est pas dépourvue de guide.** Le composant FinAnimationWorkspace
  accompagne déjà les dossiers, la terminaison et l’archivage ; les gains ont
  déjà un lien direct vers leur dossier. L’amélioration porte sur les passages
  depuis la clôture et le tirage, puis sur le repérage du travail restant.
- **La recommandation principale suit le cycle de vie.** Elle ne résume pas
  toutes les interventions de l’organisateur. La présenter comme l’unique travail
  à faire pourrait masquer un message ou une validation à examiner.
- **La simplicité ne se réduit pas au nombre de clics.** Elle se mesure aussi
  à l’absence de recherche d’écran, de ressaisie et de perte de contexte, ainsi
  qu’à la compréhension des conséquences d’une décision.

### Lecture de bout en bout

Les chemins ci-dessous sont reconstruits dans le code courant. Ils ne sont pas
des temps de tâche observés et ne supposent pas que tous les utilisateurs suivent
le même itinéraire. Les raccourcis existants restent pris en compte.

| Tâche de l’organisateur | Chemin ou comportement actuel établi | Friction à résoudre | Cible proposée |
| --- | --- | --- | --- |
| Retrouver une animation et reprendre | Le nom dans la liste ouvre la fiche sans onglet ; son défaut est Publication et clôture. Une création ou un clonage ouvre l’Assistant. Les recommandations ont leurs propres destinations. | Le point d’arrivée dépend de l’entrée, même pour une intention comparable. | Une entrée ordinaire adaptée à la phase ; un lien de tâche ouvre toujours sa destination précise. Un retour conserve son contexte. |
| Compléter dates, lots ou règlement | Sur les modèles manuels, plusieurs actions de l’Assistant ouvrent Configuration sans section ciblée. La Chasse dispose de liens plus précis. | L’utilisateur connaît la tâche, mais doit encore rechercher le formulaire. | Ouvrir le bon champ ou bloc, garder l’animation et la tâche identifiables, proposer la suite après enregistrement confirmé. |
| Résoudre un blocage puis publier | Assistant, contrôles de publication et Configuration exposent des informations liées. Les erreurs du contrôle générique sont des textes ; la publication effective est dans Configuration. | Traduire une erreur en endroit à corriger et retrouver ensuite la publication. | Un blocage compréhensible avec correction ciblée, puis retour au contrôle actualisé. |
| Passer de la publication au suivi | Après succès, les composants de publication affichent un texte renvoyant à Publication et clôture, sans bouton. L’Assistant « Consulter le suivi » mène au workflow ; la recommandation de suivi mène au Live. | Le succès ne conduit pas clairement à l’activité suivante ; un même intitulé recouvre deux vues. | Confirmation conservée et action explicite vers le suivi pertinent, avec état « publiée, à venir » si elle n’a pas commencé. |
| Interrompre puis reprendre une préparation | Le guide Chasse garde ses panneaux visités pendant son montage, mais sa sous-étape courante n’est pas écrite dans l’URL. Le changement de rubrique démonte le guide. | Revenir peut rouvrir la première étape ou celle du lien initial. | Reprise de la sous-étape enregistrée, avec données relues et gardes de saisie conservées. |
| Surveiller et intervenir le jour J | Suivi, participants, validations et messages sont répartis ; certains compteurs sont dans un détail replié. La boîte de messages possède déjà « À traiter ». | Distinguer rapidement une intervention utile d’un indicateur informatif. | Suivi principal avec accès ciblé aux situations autorisées, sans recopier les outils de traitement. |
| Clôturer et achever l’édition | Recommandations et guide de fin existent ; clôture, tirage et remises ont des vues distinctes. | Conserver une vision de la suite en passant d’une opération à l’autre. | Raccorder ces étapes, afficher ce qui reste et ouvrir le bon dossier. Terminer et archiver gardent leurs confirmations distinctes. |

### R01 Ouvrir immédiatement le travail pertinent

**Priorité produit élevée : chaque reprise de gestion est concernée.** Dans
[App.tsx](../../../../localeo-animation/src/app/App.tsx), AnimationDetailView
initialise l’onglet à `workflow` ; handleOpen construit une URL sans onglet,
tandis que création et clonage demandent `assistant`. Le workflow porte le titre
**Publication et clôture**, y compris lorsqu’il sert d’entrée à une animation
en préparation ou en cours. Ce constat ne signifie pas que tous les accès
passent par cet écran : les recommandations fournissent déjà des raccourcis.

**Proposition :** adapter l’entrée ordinaire de la fiche à la phase, en réutilisant
les vues actuelles : préparation guidée avant publication ; suivi après publication ;
opérations de fin après clôture, avec tirage si applicable ; consultation du
résultat pour une édition achevée. Le statut et les autorisations restent issus
du serveur. Un lien profond explicite et un retour vers une tâche en cours
priment sur cet atterrissage par défaut. Une évolution de phase ne doit pas
déplacer brutalement un utilisateur en train de travailler.

Conserver un repère commun court : animation, commune, dates, phase et tâche
courante. Le contenu principal change avec le besoin ; la navigation spécialisée
garde des libellés et emplacements stables. **Pas de nouvel écran obligatoire
« résumé », puis d’un deuxième clic pour commencer.**

**Preuve attendue :** ouvrir une animation en préparation, publiée à venir, en
cours et clôturée ; identifier la tâche pertinente sans parcourir le sélecteur.
Vérifier séparément lien direct, retour de liste et utilisateur en lecture seule.

### R02 Faire de la préparation un parcours qui aboutit à la publication

La règle commune de création CU-01 à CU-06 s’applique en amont de ce parcours :
mêmes repères, progression, actions, formulaires, états et protections pour tous
les modèles, avec contenu métier adapté. Sa source normative est la spécification
liée en tête du rapport ; ses preuves restent à produire séparément.

**Priorité produit élevée : c’est le premier accomplissement majeur.**
[assistantNavigation.ts](../../../../localeo-animation/src/app/lib/assistantNavigation.ts)
envoie les actions dates, dotation, règlement et publication des modèles manuels
vers `configuration` sans cible de section. Les destinations Chasse sont plus
fines ; les vitrines disposent aussi d’une destination spécifique. La friction
est donc inégale selon le modèle, et non une absence générale de guidage.

Dans App.tsx, WorkflowPublicationReadiness rend erreurs et actions requises
en texte. La publication effective se trouve en fin de Configuration via
[PublicationReadiness](../../../../localeo-animation/src/app/components/LotPaymentPanel.tsx).
La Chasse a son propre guide et un bouton de retour aux étapes incomplètes.

**Proposition :** prolonger le rôle de l’Assistant : contrôle incomplet → bloc
exact à compléter → résultat d’enregistrement → contrôle actualisé et suite
disponible. Un clic sur « Compléter les dates » doit déjà résoudre la recherche
de l’écran. Un blocage doit indiquer ce qui manque, qui peut agir et où intervenir.
Un retour explicite au parcours reste disponible sans rechercher l’Assistant.

La création initialise l’animation ; les contrôles préparent sa publication.
Leur articulation doit expliquer ce qui a été acquis et ce qui reste, sans
redemander une information déjà enregistrée. **Aucune ressaisie systématique
n’est démontrée par cet audit.** Il ne propose donc pas de supprimer les étapes
de création au seul motif qu’un Assistant suit.

Préserver les parcours adaptés : pas de commerce ou de terrain imposé à un modèle
qui n’en a pas besoin ; pas de séquence rigide pour les tâches indépendantes ;
attente d’un commerçant ou d’un traitement distinguée d’une action organisateur.
Ne pas ajouter une troisième progression à l’Assistant et au guide Chasse.

**Preuve attendue :** sur un modèle manuel et sur la Chasse, partir d’un blocage,
atteindre directement sa correction puis retrouver la publication. Tester aussi
un prérequis externe, un refus de droit et une configuration modifiée par autrui.

### R03 Raccorder le succès, la tâche suivante et la reprise

**Priorité produit élevée : l’interface doit accompagner les transitions.**
[HuntPublication.tsx](../../../../localeo-animation/src/app/components/HuntPublication.tsx)
et PublicationReadiness conservent après publication le message « Consultez
Publication et clôture pour son suivi », sans action associée. Par ailleurs,
le lien post-publication de l’Assistant aboutit au workflow, alors que la
recommandation CONSULTER_SUIVI aboutit au Live.

[HuntPreparationWorkspace.tsx](../../../../localeo-animation/src/app/components/HuntPreparationWorkspace.tsx)
change sa sous-étape dans un état local. Lors d’un remontage,
[initialPreparationStage](../../../../localeo-animation/src/app/lib/preparationWorkflow.ts)
reprend le paramètre d’entrée ou la première étape. Le code préserve les panneaux
pendant les déplacements internes au guide ; **il ne s’agit pas d’une perte
systématique de saisie à chaque étape**. La rupture concerne le retour après
sortie de ce guide. Elle reste à reproduire en recette interactive.

**Proposition :** après une opération confirmée, montrer ce qui vient de réussir
et une action précise vers la suite, sans navigation automatique. Après publication :
**Ouvrir le suivi de l’animation** ; après traitement d’un dossier : revenir au
travail restant. La destination doit être cohérente avec le libellé et la phase.

Conserver la sous-étape et le contexte de retour tant qu’ils restent valides,
sans persister de brouillons ou de données personnelles. Les listes possèdent
déjà leurs mécanismes de restauration : les réutiliser. Un résultat incertain
reste à vérifier via son reçu ; il ne doit pas être présenté comme un succès
pour permettre de passer artificiellement à la suite.

**Preuve attendue :** terminer une tâche puis reprendre le parcours sans recherche
de rubrique ; quitter puis retrouver la vérification terrain ; refuser une sortie
sale sans déplacement d’URL ou de focus ; traiter un résultat incertain avant la
suite qui en dépend.

### R04 Faire du suivi le poste de travail quotidien

**Priorité produit élevée pour l’exploitation.** La
[politique de recommandation](../../../../localeo-backend/app/domaine/animation_locale/services/recommandation_animation.py)
porte préparation, publication, clôture, tirage et fin. Elle ne constitue pas
un arbitrage global entre ces étapes, les messages et les validations. Le suivi
offre des indicateurs ; certains faits potentiellement à examiner sont dans
un détail replié (U07). Les alertes existantes doivent être inventoriées avant
de créer une nouvelle projection.

**Proposition :** distinguer visuellement l’étape du cycle et **À traiter dans
cette animation**. Ce dernier accès rejoint les outils actuels, déjà filtrés
sur l’animation et le motif : message, validation ou dossier identifié. Chaque
entrée explique le besoin et fournit une destination actionnable. Une donnée
inconnue ne devient pas « aucune tâche » ; une simple statistique ne devient
pas une alerte. La file ne peut pas être calculée depuis une seule page de liste.

Conserver les indicateurs qui permettent de constater que l’animation fonctionne,
même quand rien n’est à traiter. Donner un accès explicite aux ajustements
autorisés — dates et inscriptions notamment — et garder leur garde de saisie.
Éviter de recopier la messagerie, les participants ou leurs formulaires dans le
suivi : le gain recherché est l’orientation et le retour, pas un écran géant.

**Preuve attendue :** détecter et traiter une situation concrète, puis retrouver
le suivi ; refaire avec zéro intervention, données indisponibles, rôle lecteur
et deux situations de nature différente. Démontrer que les mêmes faits ne sont
pas comptés deux fois et qu’aucune priorité métier n’est inventée par le frontend.

### R05 Accompagner la fin jusqu’au bilan en réutilisant son guide

**Priorité élevée à l’approche de la clôture.**
[FinAnimationWorkspace.tsx](../../../../localeo-animation/src/app/components/FinAnimationWorkspace.tsx)
affiche déjà blocages, dossiers, terminaison, archivage distinct et accès au bilan.
Il restaure aussi le point de travail après une décision. Le lien Gains → dossier
de fin est déjà ciblé : il faut préserver cette réalisation AP-20.

**Proposition :** raccorder la sortie de clôture et du tirage à ce guide, avec
un résumé des opérations applicables et du travail restant. Chaque obstacle
résoluble ouvre l’objet concerné. Le filtre **À résoudre** existe mais n’est pas
celui activé initialement : tester son ouverture par défaut pour un gestionnaire
arrivant afin de traiter la fin, tout en conservant **Tous** et le contexte d’un
retour. Un lecteur ou une animation terminale a un besoin de consultation différent.

Présenter les termes par leur conséquence : clôturer les participations, attribuer
les gains si nécessaire, traiter les remises, terminer, puis archiver. Le modèle
et les décisions serveur déterminent les étapes réellement applicables. Cette
présentation n’ajoute ni ordre universel rigide, ni fusion des opérations, ni
archivage automatique.

**Preuve attendue :** partir de la clôture et rejoindre le bilan avec un dossier
bloquant ; refaire sans tirage applicable, avec tirage en cours et sans droit de
terminer. L’utilisateur peut expliquer ce qui reste et l’effet de sa décision.

### R06 Téléphone et tablette : réaliser toute la gestion au toucher

**Priorité transversale dès le premier lot.** L’objectif est la réussite du même
parcours sur les trois supports. Le suivi quotidien doit notamment rester rapide
sur téléphone ; la préparation et le traitement de plusieurs dossiers doivent
exploiter l’espace d’une tablette sans exiger de souris. Les dispositions peuvent
différer, tout en conservant actions, libellés, droits et contexte.

#### Acquis vérifiés et limite de la preuve

[mobile.css](../../../../localeo-animation/src/styles/mobile.css) prévoit des champs
de 44 px de hauteur minimale, des adaptations au pointeur tactile et des caractères
d’au moins 16 px pour les champs dans ces contextes. Les dialogues portallés ont
leurs propres règles de dimensions dans
[management-dialog.css](../../../../localeo-animation/src/styles/management-dialog.css)
et gèrent leur focus. App.tsx synchronise la hauteur visible via `visualViewport`.
Ces protections existent : l’audit ne préconise pas de les reconstruire.

Les recettes exploitation et paramètres passent sur les quatre dimensions
précitées, avec le build isolé du code audité. Quatre captures ont été examinées :
suivi sur tablette portrait/paysage, confirmation de clôture en paysage téléphone,
et paramètres sur téléphone portrait. La confirmation en paysage conserve ses
actions visibles dans l’état capturé. **Le clavier système n’était pas ouvert.**

#### R06.1 Corriger une différence de taille tactile dans les confirmations

**Constat mesuré, à traiter en priorité dans R06.** La ligne qui coche « Je confirme
la clôture définitive et le gel de la population » présente ces dimensions :

| Fenêtre CSS, contexte tactile | Case native | Zone du libellé associé, également activable |
| --- | --- | --- |
| 390 × 844, téléphone portrait | 20 × 20 px | 358 × 44 px |
| 844 × 390, téléphone paysage | 13 × 13 px | 796 × 20 px |
| 768 × 1024, tablette portrait | 13 × 13 px | 720 × 20 px |
| 1024 × 768, tablette paysage | 13 × 13 px | 752 × 20 px |

La largeur du libellé facilite l’activation, mais la hauteur de la zone passe
de 44 à 20 px. La règle qui agrandit les labels de cases dans mobile.css est
limitée à 767 px ; la règle `pointer: coarse` ne couvre pas ces labels. Le même
type de structure apparaît dans la confirmation de retrait global ; sa dimension
reste à mesurer séparément. Ce constat ne concerne pas tous les boutons, qui
disposent déjà de règles tactiles.

**Cible :** une zone d’activation confortable d’au moins 44 × 44 px pour ces
contrôles principaux, y compris tablette et téléphone paysage ; séparer clairement
l’accord sur les conséquences du bouton qui exécute la commande. Ce choix reprend
la cible de conception E73. Le [critère W3C 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced)
correspond au niveau AAA et comporte des exceptions : cette mesure seule n’établit
pas une non-conformité AA, ni une conformité globale.

#### R06.2 Donner accès à la tâche sans parcourir le menu complet

Le sélecteur téléphone peut exposer 18 rubriques. Garder ce menu pour accéder à
toutes les fonctions, et proposer des raccourcis contextualisés pour les tâches
fréquentes : reprendre la préparation, traiter un message, ajuster les inscriptions,
ouvrir un dossier de fin. Éviter de demander successivement le groupe puis la
rubrique quand l’intention de l’utilisateur est déjà connue.

Conserver le nom de l’animation, l’état et le retour avec une hiérarchie compacte.
Les captures montrent plusieurs niveaux de contexte avant le contenu. Mesurer
la place laissée à la tâche et le défilement nécessaire, sans conclure à une action
inaccessible à partir de la seule hauteur d’en-tête. Employer **Suivi de l’animation**
de façon cohérente lorsque les liens désignent la même vue. Une barre d’action
fixe n’est acceptable que si elle ne masque ni champ, ni erreur, ni confirmation.

#### R06.3 Concevoir explicitement le cas tablette

Les seuils actuels créent des combinaisons à examiner :

| Largeur disponible | Comportement actuel dans les sources | Point à vérifier |
| --- | --- | --- |
| Jusqu’à 767 px | Navigation générale mobile, sélecteur des rubriques et fiches de listes | Accès direct aux tâches et place utile dans la hauteur restante |
| 768 à 1023 px | Navigation générale mobile, mais groupes de rubriques et tableaux | Densité, lisibilité des colonnes et commandes accessibles au doigt |
| À partir de 1024 px | Menu latéral de 224 px, groupes et tableaux | La largeur utile du contenu est inférieure à celle de la fenêtre ; ne pas supposer qu’une tablette paysage dispose d’un grand bureau |

Sources : [application-frame.css](../../../../localeo-animation/src/styles/application-frame.css),
[animation-detail-navigation.css](../../../../localeo-animation/src/styles/animation-detail-navigation.css)
et [ResponsiveTable.tsx](../../../../localeo-animation/src/app/components/ResponsiveTable.tsx).
La préparation prévoit déjà une variante compacte pour faible hauteur et des
adaptations au conteneur. **Ces combinaisons ne constituent pas en elles-mêmes
un défaut.** Les captures de suivi ne démontrent pas la qualité de toutes les listes.

**Cible :** choisir fiches, tableaux et éventuelles colonnes selon l’espace utile
et la tâche. Un tableau doit conserver identité, état et action indispensables
sans obliger à balayer horizontalement pour chaque dossier ; les détails peuvent
rester accessibles à la demande. Ne pas imposer de rotation pour agir. Au changement
d’orientation ou en écran partagé, conserver rubrique, filtre et saisie tant que
la session et le contexte restent valides. Vérifier aussi tablette avec clavier
ou pointeur externe.

#### R06.4 Saisir et confirmer avec le clavier ouvert

**Recette physique prioritaire, non exécutée ici.** Ouvrir dates, capacité, motif
de modification, réponse à un habitant et confirmation sensible. Le champ actif,
son libellé, son erreur et l’action de validation doivent rester atteignables
sans fermer le clavier pour comprendre la suite. Utiliser des contrôles adaptés
à la donnée, conserver les valeurs en cas d’erreur et expliquer l’enregistrement.

La hauteur visible et le défilement des dialogues existent déjà. Leur bon
comportement doit être vérifié avec les claviers iOS/iPadOS et Android, les
sélecteurs de dates natifs, les barres du navigateur et le texte agrandi. Ne pas
déduire ce résultat d’un simple redimensionnement Chromium. La vigilance sur les
éléments fixes suit les recommandations [W3C sur la redistribution du contenu](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).

#### R06.5 Rendre les listes efficaces au doigt

Pour participants, validations, messages et dossiers de fin : afficher d’abord
l’identité utile, l’état, le besoin d’intervention et l’action précise. Garder
recherche, filtres appliqués et retour à l’élément ouvert. Afficher clairement
le nombre d’éléments sélectionnés pour les opérations qui le permettent ; ne pas
introduire de traitement groupé dans une décision qui exige un examen individuel.

Vérifier boutons, cases, menus et filtres au toucher, sans dépendance au survol
ni icône seule ambiguë. Le maintien d’une grande zone tactile ne suffit pas si
deux commandes importantes se confondent ou si l’action est cachée dans un menu
générique. Les états vides, refus et rechargements locaux restent explicites.

#### R06.6 Reprendre après interruption et réseau dégradé

Reproduire la mise en arrière-plan, le verrouillage, le retour à l’application,
la perte de réseau et une réponse tardive pendant une sauvegarde ou une clôture.
L’organisateur doit savoir si le travail est enregistré, encore local ou à vérifier.
Les recettes synthétiques couvrent déjà plusieurs pertes de réponse et la
réconciliation : elles ne reproduisent pas une suspension réelle par le système.

Conserver les gardes et reçus existants, vérifier le résultat avant une nouvelle
commande et relire droits/état après reprise lorsque nécessaire. Aucun envoi
automatique différé ni cache de données privées n’est proposé. Une perte de session
ou un rechargement complet ne doit pas être présenté comme garantissant la
récupération des brouillons. L’accès à la connexion et à la reprise reste compréhensible.

## Constats locaux conservés du premier audit

Les priorités ci-dessous qualifient les défauts locaux ; elles ne remplacent pas
l’ordre de réalisation du parcours révisé plus loin.

P1 : risque de perte de travail ou ambiguïté sur une décision importante.
P2 : repérage et efficacité du pilotage quotidien. P3 : opportunité à valider.
Effort S : retouche localisée ; M : plusieurs composants ; L : projection serveur
et consommateurs. Les effets d’usage restent à mesurer.

| Constat | Priorité | Preuve | Effort indicatif | Axe |
| --- | --- | --- | --- | --- |
| U01 | P1 | C + V | S | Nommer explicitement l’ouverture des dates et inscriptions |
| U02 | P1 | C | S/M | Protéger les paramètres saisis avant de quitter le suivi |
| U03 | P1 | C | S/M | Expliquer les actions indisponibles sans survol |
| U04 | P1 | C | M | Supprimer l’ambiguïté du bouton de clôture de repli |
| U05 | P2 | C + V | M/L | Relier les opérations de fin dans un parcours lisible |
| U06 | P2 | C + V, effet H | M | Réduire les détours entre rubriques |
| U07 | P2 | C, effet H | M/L | Faire ressortir les situations nécessitant une intervention |
| U08 | P2 | C + V | S/M | Expliquer la fraîcheur et la portée des actualisations |
| U09 | P2 | C + V | S/M | Stabiliser le vocabulaire et préciser les verbes d’action |
| U10 | P2 | C | S | Faire correspondre le bouton Flyer à son effet |
| U11 | P2 | C, effet H | S | Orienter la première connexion et l’invitation |
| U12 | P3 | C, effet H | M | Aider à choisir un modèle selon le besoin d’animation |

## Constats sur le pilotage

### U01 Ouvrir les paramètres ne doit pas se présenter comme une actualisation

Dans [ExploitationParameters.tsx](../../../../localeo-animation/src/app/components/ExploitationParameters.tsx),
ligne 47, le bloc **Dates et inscriptions** ne montre initialement que sa
description et **Actualiser**. Ce bouton exécute `setOpen(true)` puis `load()` :
il ouvre le formulaire et charge les paramètres. La capture locale
`tmp/e55-impl-animation-exploitation-captures/suivi-1280.png` confirme cet état.

Un organisateur cherchant à prolonger son animation ou à modifier la capacité
doit deviner qu’Actualiser donne accès à une modification. Proposer **Consulter
les dates et inscriptions**, puis **Modifier** si le serveur l’autorise.
Réserver Actualiser à la relecture d’un contenu déjà ouvert.

**Recette cible :** depuis le suivi, trouver dates, capacité et fermeture sans
ouvrir d’autres rubriques ; accès en lecture seule intelligible pour un lecteur.

### U02 La saisie des paramètres n’est pas protégée par la garde de sortie

Le même composant calcule `dirty` ligne 38, mais l’utilise seulement pour bloquer
son actualisation et proposer l’abandon. Il n’enregistre pas cet état dans
`useJourneyNavigation`. Le hook de commande protège les écritures en cours ou
incertaines, avec `dirty=false` via
[PreparationNavigation.tsx](../../../../localeo-animation/src/app/components/PreparationNavigation.tsx),
ligne 12, et non une modification qui n’a pas encore été envoyée.

**Séquence déduite du code, non jouée dans une session distante :** ouvrir les
dates → changer une valeur ou saisir un motif → sélectionner Participants →
revenir au suivi. Le démontage du formulaire détruit cette saisie sans la garde
commune des formulaires enregistrés. Relier ce formulaire à la garde existante,
y compris pour les retours navigateur et changements de commune.

**Recette cible :** refuser la sortie conserve valeur, rubrique, URL et focus ;
accepter abandonne explicitement ; une commande incertaine exige toujours la
recherche de son reçu. Il s’agit d’un écart ciblé aux attentes AP-03/04, à traiter
par le cycle de correctif, sans déclarer toutes les protections absentes.

### U03 Les raisons de blocage doivent être visibles

Dans [App.tsx](../../../../localeo-animation/src/app/App.tsx), ligne 1842, les
actions du workflow utilisent `disabled={!action.enabled}` et transmettent
`blocked_reason` uniquement à `title`. Le composant
[ActionButton.tsx](../../../../localeo-animation/src/app/components/ActionButton.tsx)
rend bien un bouton HTML désactivé ; il n’ajoute pas d’explication visible.
Le contenu peut aussi comporter des blocages globaux, sans garantir l’association
de chaque raison à son action.

Afficher sous l’action **ce qui manque**, **qui peut agir** et, lorsque la
destination existe, **où résoudre le point**. Un motif dans une infobulle ne
suffit pas pour le tactile ou pour un bouton exclu du parcours Tab.

**Recette cible :** comprendre un refus sans survol et rejoindre sa résolution
sans contourner les autorisations serveur.

### U04 Une absence d’actions serveur ne doit pas suggérer une clôture disponible

[App.tsx](../../../../localeo-animation/src/app/App.tsx), ligne 1854, propose
**Clôturer l’animation** lorsque `wfActions` est vide et que le statut local est
`en_cours`, ou lorsque la recommandation est CLOTURER. Cette condition n’exige pas
une action de clôture explicitement activée dans la liste du workflow. Après
une erreur de lecture de celui-ci, sa liste peut également être vide.

Le clic rejoint seulement le parcours de confirmation ; la vérification finale
des droits existe. **Aucun contournement d’autorisation n’est établi.** La
friction est une promesse d’action potentiellement suivie d’un refus ailleurs.
Présenter la capacité serveur explicite, ou un état indisponible avec relecture.

**Recette cible :** tester workflow vide, erreur, lecture seule et clôture
autorisée ; aucune disponibilité ne doit être déduite du seul statut En cours.
Préserver la possibilité métier de clôture anticipée lorsqu’elle est autorisée.

### U05 Les opérations de fin sont réparties entre plusieurs espaces

[AnimationDetailNavigation.tsx](../../../../localeo-animation/src/app/components/AnimationDetailNavigation.tsx),
lignes 12 et 26 : Publication et clôture est dans **Piloter** ; Fin et archivage,
Tirage, Gains et remise et Bilan sont dans **Résultats**. Le cycle de vie rendu par
[AnimationLifecycle.tsx](../../../../localeo-animation/src/app/components/AnimationLifecycle.tsx)
indique l’étape courante mais ne fournit pas de liens vers ses opérations.

La prochaine action et le dossier de fin existent déjà. Les compléter par une
vue courte : **état courant → travail restant → prochaine opération autorisée**,
avec accès aux écrans existants. Expliquer notamment que clôturer les
participations, tirer, remettre un lot, terminer et archiver sont des faits
différents. L’ordre et les éléments applicables viennent du serveur et du modèle.

**Recette cible :** après clôture, un organisateur trouve le tirage, les remises
restantes et la condition d’archivage sans explorer chaque rubrique. Réutiliser
[Fin et archives](../../specifications/epic-73-animation-et-ou-coffrets/fin-animation-archives.md)
et [Lots et remises](../../specifications/epic-73-animation-et-ou-coffrets/gestion-lots-remises.md).
La clôture automatique spécifiée séparément ne devient pas un acquis de cet audit.

### U06 Les retours entre groupes coûtent des gestes supplémentaires

Sur ordinateur, un groupe puis un sélecteur donnent accès aux rubriques. Changer
de groupe ouvre systématiquement sa première rubrique : Participants →
Communiquer → Piloter ramène au Live. Sur mobile, un sélecteur unique réunit les
quatre groupes, avec jusqu’à 18 rubriques si Actualités est autorisé.

C’est le comportement **spécifié**, pas une régression de restauration des listes.
Tester une reprise de la dernière rubrique par groupe, ou des raccourcis
contextuels vers Participants, messages et remises. Garder les quatre espaces,
les liens directs et les gardes ; éviter de réintroduire une rangée de 18 onglets.
Une mémorisation remplacerait une décision du 31 octobre et doit être spécifiée
explicitement avant réalisation.

**Recette cible :** consulter un participant, répondre à un message puis reprendre
la consultation sans rechercher à nouveau la rubrique ; même logique sur mobile.

### U07 Les situations à examiner sont mêlées aux statistiques secondaires

[ExploitationView.tsx](../../../../localeo-animation/src/app/components/ExploitationView.tsx),
ligne 101, affiche quatre indicateurs principaux. Les preuves
signalées, anomalies après gel et générations en attente humaine figurent dans
**Détail des validations et de l’accompagnement**, avec les autres métriques.
Le composant ne fait pas remonter ces compteurs près du résumé.

Proposer un bloc court **À examiner**, seulement lorsqu’un fait mérite une
intervention autorisée, avec compteur, explication et destination. Une anomalie
historique ou une statistique non actionnable ne doit pas devenir une tâche.
Vérifier les alertes déjà produites sur l’accueil pour éviter les doublons.

**Recette cible :** une situation nécessitant réellement une intervention est
repérable sans déplier les statistiques ; zéro tâche n’est pas une panne ; un
lecteur ne reçoit pas une action interdite. La nécessité d’une nouvelle
projection backend reste à établir en conception.

### U08 La portée et la fraîcheur des relectures doivent être compréhensibles

Le suivi, les statistiques détaillées, les étapes et le gel possèdent plusieurs
boutons Actualiser appelant la même relecture d’exploitation. Les événements
récents ont leur propre lecture. Une date de calcul est prévue dans le détail
des statistiques d’accompagnement, mais pas comme repère commun du résumé.

Conserver l’actualisation locale et les formulaires montés ; annoncer ce qui a
été relu et distinguer **lecture à l’instant** de **calcul différé des mesures**.
L’absence de polling n’est pas un défaut et ne justifie pas, à elle seule, son
ajout. Aucun défaut de cohérence des compteurs n’est démontré ici.

**Recette cible :** une relecture indique sa portée, une erreur locale laisse le
contexte utilisable et une saisie ou un reçu en cours n’est pas remplacé.

### U09 Les termes et les actions doivent annoncer une tâche reconnaissable

Le menu nomme le suivi **Live**, son écran **Suivre l’animation** ; les métriques
emploient Qualifiés, participants éligibles et preuves effectives selon les vues.
Le workflow utilise **Agir maintenant** alors que l’en-tête propose le libellé
précis de la recommandation. Ces formulations sont établies par le code et les
captures ; leur compréhension reste à tester.

Choisir un terme stable pour le suivi organisateur, distinct de Localeo Live
pour l’habitant. Définir brièvement les termes métier au premier usage et donner
aux actions le verbe exact : vérifier, consulter, publier ou préparer la clôture.
Ne pas fusionner des indicateurs qui décrivent des populations différentes.

**Recette cible :** un organisateur explique la différence entre inscrit,
parcours terminé et éligible au tirage, puis désigne l’effet du bouton principal.

### U10 Le bouton Flyer annonce un téléchargement mais ouvre une rubrique

[App.tsx](../../../../localeo-animation/src/app/App.tsx), vers la ligne 1870 :
**Télécharger le flyer** appelle `onTabChange("flyer")` et ne télécharge pas.
Renommer **Ouvrir le flyer**, ou proposer un téléchargement direct seulement
lorsqu’un document courant est disponible et autorisé.

**Recette cible :** le premier effet du clic correspond à son libellé, y compris
lorsqu’il faut encore générer ou régénérer le support.

## Axes sur les points d’entrée

### U11 La première connexion mérite une orientation courte

[App.tsx](../../../../localeo-animation/src/app/App.tsx), lignes 835 à 935 :
la connexion présente des champs labellisés, l’autocomplétion, la récupération
et les erreurs annoncées. Le parcours d’invitation existe dans
[AccountAccess.tsx](../../../../localeo-animation/src/app/components/AccountAccess.tsx).
L’écran de connexion ne précise toutefois pas comment utiliser une invitation
ni à qui demander un premier accès ; le mot de passe ne peut pas être affiché.

Ajouter une aide courte à la première connexion et un affichage du mot de passe
accessible. Conserver le processus d’invitation existant et les réponses neutres
de récupération, sans introduire une inscription ou une attribution de droits
automatique.

**Recette cible :** une personne invitée arrivée sur la connexion sait retrouver
la bonne entrée ; une invitation expirée mène à la procédure existante.

### U12 Le choix du modèle peut mieux présenter le travail de l’organisateur

Le catalogue de [App.tsx](../../../../localeo-animation/src/app/App.tsx), vers
la ligne 2300, comporte descriptions, prérequis, disponibilité et badge Léo pour
la chasse. Les cartes utilisent la même icône Ticket et la même action de
création. La comparaison de l’effort de préparation n’est pas structurée par
le composant ; les descriptions reçues peuvent déjà contenir des indications.

Tester une présentation comparable : objectif, expérience proposée au public,
besoin de commerces, préparation terrain et accompagnement disponible. Afficher
une estimation d’effort seulement si elle peut être étayée. La création possède
déjà jusqu’à sept étapes adaptées, cinq sans commerçants pour la tombola publique,
et explique la publication séparée : leur suppression n’est pas recommandée
sans observation du parcours.

**Recette cible :** un novice choisit le modèle adapté à un cas concret et cite
les préparatifs nécessaires, sans ouvrir plusieurs formulaires pour comparer.

## Principes communs à préserver dans la cible

Dans la fiche existante, la première lecture devrait répondre à quatre questions :

1. **Où en est mon animation ?** Nom, commune, période, état et fraîcheur utile.
2. **Que dois-je faire maintenant ?** Action précise, motif, intervenant et,
   s’il y en a, blocages à résoudre.
3. **Que faut-il surveiller ?** Participation, situations à examiner et accès
   direct au participant, au message ou au dossier concerné.
4. **Que se passera-t-il ensuite ?** Opération suivante et conséquences d’une
   décision, notamment à la clôture et lors des remises.

Ces réponses s’intègrent aux vues de travail existantes, sans imposer un écran
de résumé supplémentaire. Les espaces spécialisés restent disponibles. L’Assistant à neuf
contrôles et le guide Chasse à cinq étapes sont deux niveaux différents ; leur
progression et leurs validations serveur doivent rester identifiables, sans
nouveau troisième indicateur de préparation.

## Ordre de traitement révisé

La conception du parcours complet commence dès le premier lot. Elle n’attend pas
la fin des retouches de libellés. Le premier objectif démontrable est : **reprendre
une préparation, résoudre un blocage, publier et rejoindre le suivi sans chercher
une rubrique**. Le deuxième est le traitement quotidien, puis la fin de l’édition.

| Lot proposé | Contenu | Preuve attendue avant de le déclarer livré |
| --- | --- | --- |
| 1 Réparations ciblées et conception du parcours | U01 à U04/U10, cible tactile R06.1 ; qualifier les raccordements R02/R03 et les libellés U09 | Dates trouvables, saisie protégée, refus explicites, permissions et reçus ; cible tactile sur téléphone/tablette ; parcours couvrant les phases sans nouvel écran intermédiaire obligatoire |
| 2 De la préparation au suivi | R01 à R03, U06, R06 | Destinations exactes sur modèle manuel et Chasse ; reprise de sous-étape ; publication puis accès direct au suivi ; clavier, portrait/paysage et liens entrants vérifiés sur téléphone/tablette |
| 3 Exploitation et achèvement | R04/R05, U05/U07/U08, R06 | Intervention autorisée ouverte depuis le suivi, retour conservé, clôture → opérations applicables → dossier de fin → bilan ; listes tactiles, interruptions et séparation des décisions sensibles |
| 4 Prise en main complémentaire | U11, puis U12 selon observation | Première connexion/invitation et choix de modèle ; ce lot ne retarde pas le travail sur la gestion d’une animation |

Ces lots sont proposés, sans engagement de réalisation ni estimation en jours.
La règle de création CU-01 à CU-06 est désormais validée ; elle doit accompagner
la réalisation du parcours dès la création, sur tous les supports. Sa validation
ne vaut ni adoption de tous les lots, ni preuve d’implémentation.
Les points U02 et les explications de refus se qualifient d’abord comme correctifs
d’attentes existantes. Les changements de navigation, de synthèse et d’orientation
doivent être spécifiés comme évolutions. Si une nouvelle synthèse des tâches
requiert un contrat serveur, elle dépasse une retouche de présentation. Les
critères AP existants conservent leurs identifiants et leurs preuves historiques.

| Traçabilité proposée | Existant à préserver | Écart à spécifier ou à qualifier |
| --- | --- | --- |
| R01/R04 | AP-01/02 : recommandation serveur, permissions, distinction action/consultation | Atterrissage ordinaire selon phase ; liens vers les interventions de l’animation sans transformer la recommandation de cycle en classement universel |
| R02/R03, U02/U06 | AP-03 à 06 : gardes, isolation du contexte, retours de listes | Ciblage du formulaire, reprise de sous-étape et passage publication → suivi ; U02 à reproduire comme correctif ciblé |
| R05 | AP-20 et spécifications Fin/Archives, Lots/Remises | Raccordement des opérations et filtre de travail initial ; conservation du lien dossier déjà livré |
| R06, tous les axes | Cibles tactiles E73, adaptations de hauteur, recettes mobiles existantes et AP-22 partiel | Qualifier la hauteur de confirmation R06.1 ; recettes téléphone/tablette, clavier réel, écran partagé et tâches complètes |

## Recette de simplicité proposée

Organiser une étude formative avec des organisateurs novices et habitués, sur
les mêmes données avant et après évolution. Un petit groupe permet d’identifier
des difficultés ; il ne prouve pas statistiquement un gain pour toute la population.
Observer le geste réel, sans donner le nom de la rubrique à ouvrir.

| Scénario | Résultat attendu proposé | Mesure |
| --- | --- | --- |
| « Reprenez cette animation et dites ce qu’il reste avant publication » | État, prochain geste et éventuelle attente externe compris | Réussite sans aide, temps jusqu’à compréhension, rubriques explorées |
| « Corrigez ce blocage de dates, puis préparez la publication » | Le lien de tâche atteint le bon formulaire en une activation ; retour au contrôle actualisé | Navigation de recherche, retours arrière, erreurs et ressaisies |
| « Publiez, puis vérifiez que tout est prêt pour le démarrage » | Résultat confirmé compris ; suivi joignable directement depuis la confirmation | Détours, confusion publiée/en cours, destination effective |
| « Consultez un message, puis reprenez votre vérification terrain » | Animation, tâche et sous-étape retrouvées ; saisie protégée si elle existe | Contexte restauré, perte de saisie, temps de reprise |
| « Une situation nécessite votre intervention pendant l’animation » | Situation trouvée, action autorisée réalisée, retour au suivi | Réussite, interventions manquées, faux signaux d’urgence, changements d’écran |
| « Terminez cette édition dont un lot reste à traiter » | Dossier ciblé atteint ; travail restant et différence terminer/archiver compris | Détours, mauvaise décision tentée, compréhension des effets |
| « Prolongez les inscriptions depuis votre téléphone » | Contrôle trouvé, changement explicite et résultat vérifié | Recherche du bouton, clavier/focus, défilement gênant, erreur ou abandon |

Rejouer au minimum les variantes modèle manuel/Chasse, gestionnaire/lecteur,
animation à venir/en cours/clôturée, aucun travail restant, refus serveur,
conflit de version et réponse incertaine. Les durées sont mesurées à partir de
points de départ identiques ; les confirmations utiles ne sont pas comptées
comme des détours à supprimer. Fixer les objectifs de réduction de temps et de
réussite après cette référence initiale. **Aucun gain chiffré n’est établi.**

Cette méthode se concentre sur les raccordements du parcours, conformément à
l’approche [parcours de service complet du GDS/DfE](https://apply-the-service-standard.education.gov.uk/guides/understanding-service-boundaries/cross-service-journeys).
La clarté de la position et de la prochaine étape s’appuie également sur le
guide [W3C — Make Each Step Clear](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o1p04-clear-steps/).
Ces références de conception ne constituent pas une certification de conformité.

### Matrice de recette téléphone et tablette

Les dimensions sont exprimées en pixels CSS, sans équivalence automatique avec
un modèle commercial. Les mesures d’efficacité se font séparément par support ;
une moyenne globale ne doit pas masquer un parcours difficile sur téléphone.

| Situation | Preuve disponible dans cet audit | Vérification restante prioritaire |
| --- | --- | --- |
| Téléphone portrait 390 × 844 | Exploitation et paramètres : succès ; capture et cible tactile mesurée | Parcours complet au doigt sur iOS et Android, dont message et publication |
| Téléphone paysage 844 × 390 | Mêmes recettes : succès ; confirmation visible, cible de case de 20 px | Clavier ouvert, erreurs de saisie et accès aux commandes dans une faible hauteur |
| Tablette portrait 768 × 1024 | Mêmes recettes : succès ; suivi inspecté, cible de case de 20 px | Participants, validations et dossiers de fin en tableaux ; toucher sans souris |
| Tablette paysage 1024 × 768 | Mêmes recettes : succès ; suivi inspecté avec menu latéral, cible de case de 20 px | Largeur utile des listes et de la préparation ; clavier physique et tactile |
| Passage portrait/paysage pendant confirmation | Redimensionnement simulé : case cochée conservée, aucune commande métier envoyée, aux quatre départs | Rotation réelle ; conservation d’une saisie de motif et des filtres, au-delà de cette seule case |
| Petite largeur, texte agrandi et écran partagé | Ancienne recette Assistant à 320 px et texte 200 % ; pas de nouvelle preuve sur le parcours complet | 320/360 px, texte 200 %, tablette à 820/1180 px et fenêtre partagée ; aucun défilement horizontal global requis pour agir |
| Réseau lent, perte de réponse, arrière-plan et verrouillage | Scénarios synthétiques de réconciliation réussis dans les recettes | Suspension réelle, retour au navigateur/PWA, session expirée, absence de doublon et résultat compréhensible |

Pour chaque tâche, relever réussite sans aide, changements de rubrique,
défilements de recherche, erreurs de toucher, temps de reprise et compréhension
du résultat. Vérifier également zoom, focus et annonces accessibles ; le tactile
ne dispense pas de navigation clavier ou de lecteur d’écran.

## Vérifications réalisées et limites

Les premières recettes figurent ci-dessous avec leur provenance. La contre-revue
du parcours a ajouté une lecture ciblée des sources ; le complément téléphone et
tablette ajoute ensuite les exécutions précisées plus bas. Les effets d’usage
restent à observer avec des organisateurs. Aucune performance ni validation
utilisateur n’est revendiquée.

| Commande dans Animation | Résultat sur l’arbre audité |
| --- | --- |
| `ANIMATION_TEST_DIST=tmp/audit-ux-20261117-dist node scripts/build-generation-tests.mjs` | Succès, sans configuration opérateur ; avertissement Vite sur un fragment supérieur à 500 kB, sans mesure de lenteur réelle |
| `node tests/browser/exploitation.mjs` avec ce même répertoire | Succès à 1280/390 px : retraits, clôture, droits, pertes de réponse, réconciliation et continuité |
| `node tests/browser/parametres-exploitation.mjs`, première exécution | Succès observé à 1280/390 px, mais rattachement au build courant retiré : le script stock fixe `tmp/generation-browser-dist` et ignore `ANIMATION_TEST_DIST`. Ce dossier datait du 14 novembre. La nouvelle exécution sur build explicite ci-dessous remplace cette preuve pour le code audité ; U02 reste non reproduit |
| `node tests/browser/assistant-resume-ux.mjs` | Succès des 12 scénarios, dont 320 px et texte à 200 % |
| `WORKSPACE_CASE=navigation node tests/browser/animation-workspace-ux.mjs` avec ce même répertoire | Échec à 1600 px sur une assertion de focus : le test n’admet qu’un bouton ou un titre, le code focalise un `div tabindex=-1`. Désalignement à qualifier, pas preuve d’une perte de focus |
| Même recette sans `WORKSPACE_CASE` | Échec : attente de l’ancienne région « Animations nécessitant une action » ; le code courant affiche « À traiter » et la fixture conserve l’ancienne forme `animations_a_action`. Scénario incomplet, pas preuve de panne de l’accueil réel |

**Complément mobile/tablette exécuté sur Animation
`74a45f27bd66caa219b56b5d86e191ee513351d4`, arbre applicatif inchangé :**

- Build isolé réutilisé : `tmp/audit-ux-20261117-dist`, produit le 17 novembre.
- Copies temporaires de `exploitation.mjs` et `parametres-exploitation.mjs` dans
  `tmp/audit-mobile-tablette-20261117/` : seules dimensions, option `hasTouch`,
  destinations de captures et sélection explicite du build des paramètres ont
  été adaptées. Assertions existantes conservées. Les sources et leurs empreintes
  sont consignées dans `provenance.json` ; ports locaux éphémères et rapports
  distincts, aucune configuration opérateur.
- Avec `ANIMATION_TEST_DIST=tmp/audit-ux-20261117-dist`, exécution par `node` des
  deux copies : **huit passages réussis**, soit quatre formats par recette.
  Ils couvrent exploitation, clôture, droits, conflits, ajustements des paramètres
  et résultats incertains selon les scénarios existants.
- `node tmp/audit-mobile-tablette-20261117/mesures-tactiles.mjs` : sonde ciblée
  de dimensions et redimensionnement, quatre passages réussis. Mesures conservées
  dans `tactile/mesures-*.json`. Une première tentative a échoué sur un localisateur
  altéré par l’encodage du script temporaire ; corrigée avant ces mesures, elle
  n’établit pas un défaut applicatif. Cette sonde n’exécute aucune commande métier.
- Quatre captures inspectées dans les sous-dossiers `exploitation` et
  `parametres-exploitation` : `suivi-768.png`, `suivi-1024.png`,
  `confirmation-844.png`, `parametres-390.png`. Le déplacement du contenu interne
  entre captures interdit d’en déduire une disparition de l’en-tête.

Ces exécutions utilisent Chromium avec API synthétique et pointeur tactile émulé.
Elles ne couvrent ni Safari/iPadOS, ni clavier virtuel réel, ni utilisation au doigt,
ni suspension du navigateur par le système. Les serveurs se sont fermés après
exécution. Les scripts et artefacts restent temporaires et non versionnés dans
le dépôt applicatif ; aucune modification du code produit ni des tests versionnés.

Contrôles documentaires réussis depuis Projet :
`py -3.14 scripts/check_guidance.py` (99 guides, 1 332 liens, zéro erreur ou
avertissement), `py -3.14 scripts/sync_documentation.py --check-sources`
(151 documents) et `git diff --check`. Le lanceur `py -3.14` a remplacé
l’alias `python` indisponible dans cette session.

Les captures d’exploitation courantes sont dans
`localeo-animation/tmp/e55-impl-animation-exploitation-captures/`, celles de
l’Assistant dans `tmp/assistant-resume-ux/`. La capture de navigation à 1600 px
est dans `tmp/audit-ux-20261117/animation-workspace-ux/`. Ces sorties restent
locales et non versionnées ; les anciens fichiers de ces dossiers n’ont pas
été considérés comme des preuves de cette exécution. Les serveurs des recettes
se sont fermés ; aucun serveur d’audit n’est laissé actif.

## Impacts et rattachement

- **Dépôt modifié : Projet**, pour ce rapport, son index, la règle commune de
  création dans les parcours SaaS, ses liens de spécification et son suivi E73.
  Aucun code applicatif modifié ; aucun commit, push ou déploiement.
- **Animation** : consommateur principal des éventuels correctifs et évolutions.
  **Backend** : propriétaire conservé des droits, transitions, qualifications,
  conséquences, reçus et décisions de prochaine action. R01/R02/R04/R05 et
  U05/U07/U08 pourraient nécessiter des projections de lecture ou des destinations
  de tâche à concevoir ; aucune API n’est ajoutée
  par cet audit. Ne pas recréer ces décisions dans les composants.
- **Live et Pro** : pas de changement demandé à leurs parcours. Les conséquences
  d’une décision organisateur sur participants et commerces restent à vérifier
  si une évolution est ensuite spécifiée. Les règles ERP propres aux pages de
  gestion ne sont pas imposées comme une nouvelle structure à cette PWA.
- **Documentation fonctionnelle et exploitation** : spécification commune de
  création complétée par la décision utilisateur. Aucune procédure opérateur ni
  aide utilisateur ne présente cette cible comme déjà réalisée ; les futurs
  libellés/parcours devront être répercutés lors de leur réalisation.
- **Contrats, migrations, données et générateur** : sans modification à la phase
  d’audit ; aucun changement de schéma, de fixture versionnée ou d’environnement.
  Les scénarios de démonstration devront couvrir les phases et blocages retenus
  si la cible est implémentée. Les réserves AP-22/GL-16 existantes sont conservées.

La prochaine phase utile est de spécifier le parcours **préparer → publier →
suivre**, en qualifiant parallèlement les correctifs U01 à U04/U10, puis son
prolongement jusqu’à la fin d’édition. La mesure initiale auprès des organisateurs
reste à réaliser. L’epic E73 reste historiquement Terminée ; E55 et les autres
évolutions gardent leur suivi propre.
