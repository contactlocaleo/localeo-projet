# Registre des anomalies

## Correction du 11 novembre 2026 — Bilan et diffusion par support

- **Cause démontrée dans les sources** : l’interface présentait l’unité brute
  `NOMBRE`, la création de supports se trouvait dans Bilan, et le PDF historique
  n’exposait que quelques totaux. L’attribution d’inscription existait, mais
  aucun compteur de clic ou d’ouverture QR n’était collecté.
- **Correction** : Communiquer reçoit « Liens et QR de diffusion » après Flyer,
  avec trois mesures par support et date de collecte. Les vignettes Bilan
  masquent uniquement l’unité `NOMBRE`. Le PDF multipage assemble résultats,
  objectifs conditionnels, diffusion, taux de satisfaction/commentaires et audit
  dans un même instantané. La nouvelle redirection publique compte les ouvertures
  sans identifier les visiteurs et conserve les contrôles du catalogue.
- **Preuves** : huit scénarios navigateur, création/QR adjacents et contrôles
  PostgreSQL jetables ; captures mobile/ordinateur et quatre pages PDF examinées.
  La revue indépendante a identifié un refus de capacité des tombolas publiques :
  reproduction rouge puis correction verte avec capacités serveur explicites.
  Commandes et résultats dans la
  [vérification de livraison](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md).
- **Impacts** : backend, Animation et documentation ; OpenAPI embarqués
  Animation et Pro synchronisés. Les contrats moteur JSON et Marketplace/Live
  ne consomment pas ces DTO de diffusion et restent inchangés.
  Migration v310 requise avant livraison ; pas
  de nouveau droit, batch, secret ou flag. Schéma de démonstration additif et
  colonnes nullables compatibles avec les captures existantes ; pas de donnée
  de démonstration modifiée ni de génération sur environnement partagé.
  Aucun déploiement ou migration TEST effectué. Les ouvertures historiques
  restent non collectées ; les anciens QR doivent être remplacés pour compter
  leurs nouvelles ouvertures.

## Correction du 11 novembre 2026 — e-mail et détail de participation

- **Cause** : les gains libres/numériques ne projetaient pas l’e-mail ; sans
  nom, `gainWinnerName` utilisait la référence technique. Les Coffrets avaient
  le même repli. Aucune lecture individuelle organisateur n’alimentait une
  fenêtre de participation. Base Animation `f1dad12`, Backend `3a55fae`.
- **Correction** : e-mail autorisé comme identité cliquable dans gagnants,
  suivi et listes de participants. `ParticipationIdentity` ouvre une fenêtre
  `ManagementDialog` avec inscription, état, progression, validations et
  coordonnées autorisées. GET individuel protégé, sans collecte globale ni
  écriture ; calcul par moteur existant ou provenance gelée. Email complet
  tombola publique seulement, masquage conservé ailleurs. Projections
  personnelles Live et secrets d’accès non enrichis. Lectures groupées des
  gains conservées, sans requête par ligne.
- **Preuves** : le nouveau scénario sur le build précédent échoue sur
  l’absence du bouton e-mail. Après correction, `dotation.mjs` valide
  **22 parcours PC/mobile**, dont panne/réessai, 403, identité inattendue,
  réponse tardive, email masqué/absent, lecture simple et traitement de gain.
  `global-read.mjs` valide **4 parcours** et l’ouverture depuis la liste,
  sans perdre recherche ni pagination. Captures examinées à 320/1280 px.
  Deux parcours supplémentaires valident le texte à 200 %, dont 320×568 px,
  et deux autres le détail depuis les gains Coffrets.
  **78 tests backend ciblés, 693 contrôles d’architecture, 27 tests PostgreSQL,
  13 tests Node Animation et 31 tests de contrats Pro réussis**. TypeScript, ESLint et
  build isolé contrôlés ; voir la vérification de livraison pour les
  preuves finales et limites.
- **Impacts** : backend et Animation ; OpenAPI canoniques E41/E42 et contrats
  embarqués Animation/Pro synchronisés. Aucun changement de cycle de vie,
  droit accordé, migration, batch ou configuration ; aucune génération de
  démonstration nécessaire (lecture additive, données existantes inchangées).
  Déployer le backend avant l’interface. Aucun déploiement TEST attesté.

## Correction du 11 novembre 2026 — libellé de traitement d’un gain

Dans la liste des gains de `ExternalPrizesWorkspace`, le bouton « Suivre ce
gain » devient **Traiter ce gain**, selon la demande utilisateur. Son ouverture
du dossier et ses protections sont conservées. Le scénario navigateur existant
est adapté au nouveau nom accessible : `dotation.mjs reader follow`, quatre
parcours à 320/1280 px, **40 contrôles réussis**, API simulée. Build isolé
réussi, avertissement de taille du bundle existant. Changement rédactionnel
Animation uniquement, sans impact métier, contrat, permission, migration,
configuration ni donnée de démonstration. Pas de vérification distante.

## Correction du 11 novembre 2026 — prochaine action et navigation alignées

Sur la base Animation `6c96310`, la prochaine action occupait une rangée
séparée sous l’en-tête dans Piloter, Communiquer et Résultats ; le guide
Préparer la supprimait, ce qui décalait la navigation entre espaces.
Le scénario `WORKSPACE_CASE=header` reproduit avant correction l’action
hors de l’en-tête (`tmp/animation-header-before/`).

`AnimationDetailView` présente désormais la prochaine action à côté du
statut dans `WorkspaceHeader`, avec une largeur adaptative. Le guide garde
son action propre ; une réserve non interactive et masquée aux technologies
d’assistance stabilise l’en-tête. Les actions secondaires utilisent partout
le même panneau repliable. La navigation ne change plus de hauteur entre
les quatre espaces. Les parcours, confirmations et protections restent actifs.

Preuves locales : huit formats 320–1600 px, dont texte à 200 %, valident
la position des quatre espaces, statut et action côte à côte, cible de
44 px, navigation clavier vers le contenu et absence de mutation API.
Huit recettes de défilement valident le contenu unique, le chargement de
liste et la destination de la prochaine action. Captures PC/mobile/zoom
inspectées dans `localeo-animation/tmp/animation-header-ux/`.
Huit recettes de navigation supplémentaires vérifient les droits, liens
directs, chargement différé et gardes de sortie avec saisie en cours.
TypeScript, ESLint et build isolé réussis (avertissement de taille Vite).

Impacts : présentation Animation et documentation seulement ; aucune règle
métier, contrat, permission, migration, configuration d’exploitation ou donnée
de démonstration modifiée, car les commandes existantes sont réutilisées.
Vérification locale avec API simulée ; version TEST non inspectée.

## Correction du 11 novembre 2026 — notifications au-dessus des fenêtres

La demande vise les messages temporaires de succès/erreur, selon la précision
utilisateur. Le Toaster global avait un niveau de superposition 100, tandis
que `ManagementDialog` utilisait 101. La reproduction PC/mobile montre que le
bouton de fermeture du message était recouvert par la fenêtre : contrôle par
`elementFromPoint`, rapport rouge `localeo-animation/tmp/notification-overlay-AYTuag/`.

Le Toaster est extrait dans `components/Toaster.tsx` et rendu par portail dans
le body ; la couche commune `--app-layer-notifications: 110` est au-dessus des
fenêtres existantes (50–101). Seuls les messages interceptent les pointeurs.
Le composant conserve les annonces `status`/`alert`, les détails d'erreur,
la fermeture et l'expiration. La fenêtre conserve sa navigation clavier et
son focus ; fermer la notification ne ferme pas la fenêtre.

Recette réussie à 320/1280 px : messages succès/erreur, détail, hit-test
de fermeture, clavier, Échap, réouverture avec message déjà présent,
expiration et absence de débordement. Rapport
`localeo-animation/tmp/notification-overlay-4PphqG/report.json` ; captures avant
et après conservées. Reproduction : `node tests/browser/notification-overlay.mjs`.
Présentation seule : aucune règle métier, API, permission, migration, batch,
configuration d'exploitation ni donnée de démonstration modifiée pour ce
correctif. Aucun déploiement attesté sur TEST.


## Correction du 11 novembre 2026 — retour visible de l'envoi d'un message

Le clic sur **Envoyer le message** semble sans effet, sans confirmation ni
erreur. Sur la base Animation `e197d86` avec modifications locales, le cas
minimal reproduit bien un POST `/envoyer`, mais sa confirmation est à
`y=-1180 px` hors de la zone visible après le clic à 320 px. Le banc utilise
le vrai formulaire et `#app-main` défilant ; l'API est simulée et aucun
message n'est diffusé réellement. Capture d'échec conservée dans
`localeo-animation/tmp/communication-send-feedback-fOR6jD/`.

Les retours de commande utilisent le composant partagé `FeedbackMessage` :
confirmation, refus et résultat incertain reçoivent le focus et deviennent
visibles après l'action. Le calcul d'aperçu conserve le focus de travail.
Confirmation explicite, droits, versions, bouton bloqué pendant la requête,
clé unique et rapprochement par reçu sont conservés.

Preuves : **6 scénarios navigateur réussis** à 320/1280 px (succès,
refus 409 et réponse perdue), rapport `tmp/communication-send-feedback-H50t6G/report.json` ;
**11 scénarios de workflow** dans `tmp/communication-workflow-9NiHJY/` ;
**15 tests Node** campagnes, HTTP et suivi réussis. La preuve vérifie le POST,
la position dans le viewport et l'absence de double envoi ; la seule présence
d'un texte dans le DOM ne suffit pas. TypeScript, lint complet et build isolé de production réussis ; avertissement de taille du bundle consigné au bilan.

Impact limité à la présentation Animation et ses fixtures. Aucun changement
du contrat, des règles de diffusion, des permissions, de migration, de batch,
de configuration ni du générateur ; leurs comportements ne sont pas modifiés.
Le cas distant signalé n'a pas été consulté ; le correctif local ne constitue
pas une preuve d'envoi ni de déploiement sur TEST.


## Correction du 11 novembre 2026 — timeline du cycle de vie

- **Signalement** : « Test animation Thibaut » clôturée, mais des étapes de
  configuration, de publication ou de tirage semblent encore non validées dans
  **Publication et clôture**. Le cas distant n’a pas été consulté.
- **Cause reproduite sur Animation `26cc7fd`** : l’interface reconstruisait dix
  étapes à partir d’un cycle serveur à huit étapes. Elle ajoutait Configuration
  et Prête à publier, puis traitait les phases de suivi du tirage libre comme
  des codes absents du cycle local. La reproduction navigateur échoue sur les
  deux étapes supplémentaires avant correctif, capture conservée dans
  `localeo-animation/tmp/workflow-timeline-vMdWoJ/` (non versionnée).
- **Correction** : présentation directe de l’ordre, des libellés et des états
  renvoyés par `/workflow`. Les phases Tirage en préparation, Tirage à vérifier
  et Tirage terminé sont conservées, indépendamment du statut persistant
  `CLOTUREE`. Les étapes passées sont cochées ; l’étape actuelle est nommée et
  marquée `aria-current="step"` dans une liste ordonnée. Chargement, erreur,
  réponse invalide et cycle annulé sont explicites, sans progression inventée.
- **Preuves locales** : 36 scénarios navigateur à 320/1280 px réussis dans
  `localeo-animation/tmp/workflow-timeline-pKknv0/report.json` ; quatre recettes
  ciblées finales dans `tmp/workflow-timeline-wzuCAc/`. Les deux scénarios de
  clôture existants à 390/1280 px et sept tests Node de navigation/annulation
  passent. TypeScript, ESLint et build isolé de l’application réussis ; captures
  PC/mobile inspectées. Aucun appel API réel ni commande métier exécutés.
- **Impacts** : interface et type TypeScript du consommateur alignés sur le
  contrat existant. Backend, OpenAPI, règles métier, habilitations, migrations,
  batchs, paramètres d’exploitation et générateur de démonstration inchangés :
  seule la restitution de la lecture est corrigée. La
  [spécification de suivi](../../specifications/epic-73-animation-et-ou-coffrets/tirage-libre-protocole.md#exécution-locale-et-activation-future)
  décrit cette présentation. Aucun déploiement réalisé ; contrôle de l’animation
  TEST à effectuer après livraison de Localeo Animation.

## Correction du 11 novembre 2026 — consulter les gagnants

**Complément après la précision utilisateur « le détail des gains ».** La vue
initiale restait centrée sur des fiches de lots. Depuis la base Animation
`4cdd4dd`, **Gains & remise** présente d’abord une liste synthétique, avec le
gagnant en première colonne/titre mobile, son lot, le statut de remise et
**Voir le détail du gain**. Le détail conserve consignes, suivi, date du premier
email réussi et interventions. La gestion des bons numériques vient après la
liste. Le retour conserve la page courante ; aucun nouveau chargement global de
participants ni dédoublonnage côté navigateur n’est ajouté.

La reproduction du défaut d’ergonomie échoue avant correctif sur l’absence de
la liste (`tmp/tirage-existing-Ezww4I/`). Après correction : 22 scénarios navigateur,
182 assertions à 320/1280 px, dont plusieurs gagnants, référence sans nom,
pagination, refus et aller-retour au détail, réussissent dans
`localeo-animation/tmp/tirage-existing-4JyXfc/`. Le banc numérique passe ses
12 scénarios/116 assertions ; ses réponses 404 simulées préexistantes sur les
sélecteurs de préparation/contact public ne constituent pas une vérification de
ces routes. Onze tests Node, TypeScript, ESLint et build isolé réussissent.
Captures PC/mobile inspectées. Présentation seule : aucun changement backend,
contrat API, règle de remise, migration ou donnée de démonstration.

- **Signalement** : impossibilité de consulter les gagnants depuis
  **Résultats → Gains & remise**. Version distante et animation non précisées ;
  aucun accès aux données de TEST réalisé.
- **Causes locales reproduites**, sur les bases Animation `3716485` et backend
  `d34f33b` : une erreur de lecture du tirage empêche même l’appel des gains ;
  les tombolas publiques ne collectent pas de nom/prénom et les gains libres
  affichent seulement « Participant — rang N ». Le mapping Coffrets produit
  aussi une identité vide ou « None None ».
- **Correctif** : la liste des gagnants libres est relue malgré une
  indisponibilité technique du suivi du tirage, avec avertissement explicite.
  Le nom et la référence d’inscription identifient le gagnant dans la liste
  et dans son détail ; la référence remplace le nom absent. Le mapping Coffrets
  conserve le même principe. Les refus d’accès et changements de contexte
  purgent les données, y compris dans le détail. Les reçus absents conservent
  le parcours de vérification et de rejeu explicite de la même commande.
- **Preuves** : deux scénarios navigateur échouent avant correction, sur
  l’identification publique et la liste masquée par un 503 du tirage ; cinq
  assertions backend échouent sur les identités. Après correction : 40 scénarios
  navigateur à 320/1280 px, 406 assertions, 11 tests Node, types, lint et build
  isolé de l’application réussis. La dernière recette des sept cas gagnants
  confirme 14 scénarios et 96 assertions. Captures inspectées sur PC et mobile,
  dans `localeo-animation/tmp/tirage-existing-F7uzIu/` et
  `localeo-animation/tmp/tirage-existing-hJptiX/` (non versionnées).
  Backend : 732 contrôles architecture/recensement/mapping réussis ; cinq
  exécutions PostgreSQL finales réussies sur une base locale jetable : deux cas
  HTTP, deux lectures personnelles Live et le mapping Coffrets SQL. Ils vérifient
  les références, les refus 403/404, la lecture seule, la pagination et l’absence
  de référence de gestion dans Live personnel. Une régression élargie
  intermédiaire avait détecté deux incompatibilités avec ce contrat personnel
  fermé ; elles ont été corrigées et chacun des deux cas a réussi au rejeu,
  sans changer le DTO personnel.
- **Impacts** : projection de lecture, pas de nouvelle règle de tirage.
  `animation:lire` reste nécessaire ; les permissions de commande sont inchangées.
  Pas d’adresse brute supplémentaire ni de référence de gestion dans les lectures
  publiques/personnelles. Contrats OpenAPI E41/E42 actualisés ; les trois schémas
  de gains du contrat embarqué Animation sont synchronisés avec l’export runtime.
  Les écarts préexistants du reste de ce snapshot ne sont pas intégrés au correctif.
  La [spécification des lots](../../specifications/epic-73-animation-et-ou-coffrets/dotation-lots.md#consulter-les-gagnants-dans-localeo-animation)
  décrit la lecture. Aucune migration ni donnée de démonstration à modifier :
  la référence existe déjà. Aucun nouveau réglage d’exploitation, envoi de
  message, tirage réel ou déploiement effectué. Livrer backend et Animation
  pour disposer de la référence dans l’interface ; vérification TEST à effectuer
  après déploiement.

## ANO-ANI-CHARTE-CRM-20261104 — Alignement sur la charte de gestion CRM

La palette, la navigation, les composants de formulaire et la hiérarchie
typographique de Localeo Animation sont harmonisés avec Localeo Pro sur la
référence CRM. Le [suivi commun](../../audits/ergonomie-gestion-pro-animation-2026-11-01.md#harmonisation-sur-localeo-crm--4-novembre-2026)
conserve les constats, corrections, impacts et preuves locales. Les transitions,
droits et confirmations d’animation restent inchangés ; aucun déploiement réalisé.

### Correction du 10 novembre 2026 - Focus du sélecteur de commune

- **Observé et cause** : un clic sur « Commune active » affichait un contour
  orange à l'intérieur du champ du bandeau bleu. Reproduction locale sur la
  base Animation `89c7f6e` : Chromium applique `:focus-visible` au sélecteur
  natif même au clic ; la règle commune de `actions.css` ajoutait alors un
  contour ocre de 3 px autour du seul `select`.
- **Correction** : dans `application-frame.css`, le repère de focus est porté
  par le champ complet `.commune-picker`, en blanc sur bleu, sur 2 px. Le
  contour intérieur est retiré dans ce seul contexte. Le clavier conserve un
  repère visible, qui disparaît en quittant le champ ; la sélection native et
  la commande de changement de commune sont inchangées.
- **Preuves locales** : `pnpm typecheck`, `pnpm lint` et
  `node scripts/build-generation-tests.mjs` réussis. Le scénario existant
  `WORKSPACE_CASE=shell` de `animation-workspace-ux.mjs`, complété pour cette
  recette par le clic, Tab, l'ouverture au clavier, Échap et la sortie du
  champ, passe sur dix formats de 320 à 1600 px, paysage et texte à 200 %.
  Styles calculés et absence de mutation vérifiés ; captures PC/mobile
  examinées dans `localeo-animation/tmp/commune-picker-focus/`, non versionnées.
- **Impacts** : CSS de présentation dans Animation et suivi documentaire ici.
  Aucun contrat API, règle métier, droit, migration, générateur de démonstration
  ou paramètre d'exploitation modifié. Version distante non vérifiée et
  déploiement non effectué.

### Correction du 10 novembre 2026 - Alignement des actions des modèles

- **Observé et cause** : dans le catalogue **Modèles**, le bouton « Créer une
  animation » suivait directement le contenu variable de chaque vignette. Une
  description, un badge ou des prérequis supplémentaires décalait donc l'action
  par rapport à la vignette voisine. La reproduction locale sur la base
  Animation `89c7f6e` mesure un écart de 57 px entre deux boutons d'une même
  rangée.
- **Correction** : chaque vignette devient une colonne occupant toute la hauteur
  de sa cellule de grille et son action, disponible ou désactivée, est repoussée
  en bas. Les contenus restent libres de grandir ; les boutons d'une même rangée
  conservent le même niveau. Sur mobile, les vignettes restent empilées.
- **Preuves locales** : le scénario navigateur `leo-assistant.mjs` utilise deux
  contenus de hauteurs différentes et contrôle l'alignement exact à 1280 px,
  ainsi que le parcours et le rendu à 390 px. Le scénario échoue avant correction
  avec les positions `338,44` et `281,39` px, puis réussit après correction. Les
  captures PC et mobile ont été examinées dans
  `localeo-animation/tmp/leo-browser-captures/`, non versionnées.
- **Impacts** : mise en page et test ciblé dans Animation, sans changement de
  comportement, contrat API, règle métier, droit, migration, démonstration ou
  exploitation. Version distante non vérifiée et déploiement non effectué.

### Correction du 10 novembre 2026 - En-tête et navigation du détail

- **Observé et cause** : le détail d'une animation séparait le retour, le nom,
  la commune, les dates et le statut sur plusieurs niveaux verticaux. Sur
  ordinateur, quatre onglets d'espaces étaient suivis d'une seconde rangée de
  sous-onglets de même apparence. Cette hiérarchie consommait de la hauteur et
  rendait les deux niveaux de navigation difficiles à distinguer.
- **Correction** : le contexte de l'animation est réuni dans un en-tête compact,
  sur la même ligne que le retour à la liste lorsque la largeur le permet. Une
  seule barre de navigation présente les quatre espaces **Préparer**, **Piloter**,
  **Communiquer** et **Résultats**, puis un sélecteur libellé pour la rubrique de
  l'espace actif. Sur mobile, le sélecteur groupé unique est conservé. Les droits,
  liens directs, alias, gardes de sortie et chargements différés restent inchangés.
- **Preuves locales** : le scénario navigateur
  `WORKSPACE_CASE=navigation` échoue avant correction sur l'absence du nouvel
  en-tête compact. Après correction, huit formats de 320 à 1600 px, dont le
  texte à 200 %, valident la géométrie de l'en-tête, la barre unique, les cibles
  tactiles, le clavier, les habilitations et l'absence de débordement ou de
  mutation API. Les captures PC, tablette, mobile et zoom ont été examinées dans
  `localeo-animation/tmp/animation-workspace-ux/`, non versionnées.
- **Impacts** : présentation, navigation locale et tests dans Animation ; aucun
  contrat API, règle métier, droit, migration, donnée de démonstration ou
  paramètre d'exploitation modifié. Version distante non vérifiée et déploiement
  non effectué.

## ANO-ANI-HEADER-COMPTE-20261103 — Espace réservé aux rubriques du menu

- **Observé** : dans le shell connecté de Localeo Animation, les documents,
  l’identité, l’organisation, la version et les actions de compte/déconnexion
  occupaient un pied de menu non rétractable, réduisant la hauteur des rubriques.
  Cause confirmée dans `Sidebar` et `.app-navigation__account`, sur la base
  applicative `4116e0e` ; aucune observation de version distante revendiquée.
- **Correction** : déplacement dans le menu « Mon compte et documents » de
  l’en-tête. Identité compacte sur PC, initiales sur petit écran, identité
  complète à l’ouverture. Les documents s’ouvrent dans un autre onglet pour
  préserver la saisie ; l’accès Compte et équipe garde la protection de navigation,
  et la déconnexion appelle le parcours serveur existant. Le menu latéral ne
  conserve que les rubriques. Styles corrigés à la source, règles du pied retirées.
- **Preuves locales** : TypeScript et ESLint réussis ; 297 tests Node réussis,
  aucun ignoré ; build isolé réussi avec avertissement de taille de bundle.
  Le scénario navigateur `WORKSPACE_CASE=shell` vérifie dix formats PC/mobile,
  paysage et texte à 200 %, les bornes de largeur, le clavier et le focus,
  les liens, la garde de saisie et la déconnexion avec API simulée. Captures dans
  `localeo-animation/tmp/pro-alignment/`, non versionnées.
- **Impacts** : présentation seule dans `localeo-animation` et documentation
  dans `localeo-projet`. Réutilisation du contexte déjà chargé par l’en-tête ;
  pas de contrat API, permission, règle métier, migration ou donnée de démonstration
  modifiés. Aucun nouveau paramètre d’exploitation. Déploiement non effectué.

## ALL
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-ANI-01 | inscription | Erreur « Failed to fetch » après « Tout envoyer » dans l’onglet Invitations, alors que les invitations sont bien envoyées et visibles après actualisation. | Corrigé côté interface : vérification de l’état serveur après une perte de réponse, sans nouvel envoi automatique. Validation en environnement réel à effectuer. |
| ANO-ANI-02 | facturation | La demande facturation porte sur un identifiant de commande qui n'est pas disponible (uuid), une demande de facturation doit porté sur une animations (ces lots). Chaque demande doit être consultable pour voir si l'ensemble des factures relatibes aux lots d'animation sont disponible ou sinon il doit être possible de consulter l'état des demandes et de les relancers. Un état général sur le dossier doit permettre de savoir si il est complet (toutes les factures sont recues) ou non | Interface corrigée et testée. Complément backend de relance et de complétude préparé et testé ; autorisation explicite requise pour son application après refus du contrôle automatique. Voir docs/specifications/ano-ani-02-facturation-animation.md. |
| ANO-ANI-03 | Origine API HTTPS explicite obligatoire. lors du build pour déploiement dans Re,der | A corriger |

## Correction du 30 octobre 2026 — découverte publique et carnet Animation

Retour utilisateur sur `test-animations.localeo.city`, confirmé configuré
`LOCALEO_PUBLIC_SURFACE=ANIMATION` par lecture publique de `app-config.js`.
L’accueil spécifique utilisait une liste sans commande de géolocalisation,
un en-tête vert distinct des codes Coffrets, et Live conservait son onglet
Coffrets ainsi que cette rubrique comme destination mémorisée par défaut.

Correction dans `localeo-marketplace` : géolocalisation volontaire via le
service E52 existant, commune réellement résolue et choix manuel préservé ;
identité bleu/orange/papier partagée, filtres avant la mise en avant ; onglet
Coffrets masqué et entrée Live adaptée à la surface ANIMATION. Les données,
liens directs et ajouts Coffrets restent conservés. Aucun changement backend,
de schéma ou de droit, ni migration ou réparation de données nécessaire.

L’extension et l’analyse UX sont rattachées à **E73-EVO-UX-PUBLIC** dans les
[parcours canoniques](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md).
La reproduction initiale constate l’absence du bouton dans le navigateur avant
correction. Les preuves finales et les limites de livraison sont consignées
dans le [suivi](../../specifications/epic-73-animation-et-ou-coffrets/suivi-implementation.md).
Les propositions de confirmation d’inscription et d’immersion du jeu restent
distinctes de cette correction. Aucun déploiement distant effectué.

## Correction du 29 septembre 2026 — icônes PWA

- Attendu : conserver la famille graphique Live/OnBoard sans fond sombre autour du marqueur Animation.
- Cause : `scripts/export-pwa-icons.ps1` ajoutait un fond opaque sombre à tous les exports PWA, alors que le logo source et le favicon étaient déjà transparents.
- Correction locale : exports 192/512 transparents ; Apple 180 et maskable 512 sur fond blanc, avec leurs marges conservées ; fond de lancement du manifeste blanc.
- Preuves : contrôle visuel des exports Apple, dimensions et transparence des quatre exports ; `node --test tests/pwa.test.mjs tests/pwa-lifecycle.test.mjs` (9 succès) ; `node scripts/build-pwa-tests.mjs` réussi, avec avertissement de taille du bundle.
- Impact limité aux ressources statiques et à leur export : aucun contrat API, règle métier, migration ou générateur de démonstration modifié. Déploiement et vérification sur appareils iOS/Android non effectués ; le renouvellement des icônes déjà installées dépend du système.

## Correction du 23 octobre 2026 — descriptions des lots engagés (RM-11-03)

- Attendu : après modification de la description courante d’un modèle, pouvoir relire la description initiale des exemplaires et de la dotation engagés, conformément à [RM-11-03](../../specifications/epic-73-animation-et-ou-coffrets/recette-metier.md#rm-11-03).
- Reproduction : sur le clone isolé, le gestionnaire A1 affecte des exemplaires puis modifie la description du modèle. Le backend conserve correctement les descriptions initiales ; les lignes de stock et de dotation ne les affichaient pas.
- Cause et correction locale : `DigitalPrizeAssignments` et `DigitalPrizeInventory` présentent désormais respectivement `snapshot.description` et `unit.description` lorsqu’elles existent, comme texte React échappé, avec retours à la ligne et mots longs. Aucune description n’est reconstruite depuis le modèle courant.
- Preuves : scénario navigateur rouge avant correction, puis 16 contrôles réussis à 1280/320 px, dont l’absence d’interprétation HTML ; six tests adjacents de contrats et commandes réussis. Build isolé sans configuration opérateur réussi. Vérifications TypeScript et ESLint réussies. Rejeu sur les mêmes objets du clone réussi après installation coordonnée des deux composants : descriptions initiales visibles dans les deux lignes, description courante distincte et snapshots API préservés. Les cinq étapes RM-11-03 sont reliées à des preuves privées figées et contrôlées par empreinte. Aucun commit, push ou déploiement sur TEST partagé.
- Impacts : présentation seule dans Localeo Animation ; API et règle de conservation backend inchangées, sans migration ni réparation de données. Le générateur et ses exports fournissent déjà ces descriptions ; aucun nouveau paramètre d’exploitation.

## Correction du 24 octobre 2026 — auteur du suivi des gains externes (RM-10-03)

- Attendu : relire l’auteur et la date des événements de contact, réponse, déclaration de remise et correction dans le suivi du gain, selon la [recette métier E73](../../specifications/epic-73-animation-et-ou-coffrets/recette-metier.md).
- Reproduction : sur une animation externe dédiée du clone, les quatre événements sont enregistrés par les vrais formulaires. Leur API fournit l’identifiant de l’auteur, mais les lignes de l’historique n’affichent que le type, la date et le motif. La déclaration et sa correction restent correctement conservées côté backend.
- Correction locale : `ExternalGainFollowup` présente désormais `acteur` comme texte React échappé, avec un libellé explicite et des mots longs repliables. L’interface ne reconstitue ni identité ni habilitation.
- Preuves : scénario navigateur rouge avant correction, puis 24 contrôles réussis à 1280/320 px ; parcours adjacent de réponse perdue réussi. Build isolé, TypeScript et ESLint réussis. Après installation coordonnée du seul composant sur le clone, dix contrôles de relecture réussissent à 1280/320 px sur les quatre mêmes événements : auteurs et dates conservés, états inchangés et aucune nouvelle commande métier. Les preuves privées sont figées et contrôlées par empreinte.
- Impacts : affichage seul ; contrat API, règles métier, permissions, migrations et générateur inchangés puisque l’auteur existe déjà dans chaque événement. La réception email externe, la distinction documentaire « Non remis » et l’entrée Localeo en écriture restent des limites distinctes de ce correctif ; aucun nouvel état ni rôle n’a été ajouté.
