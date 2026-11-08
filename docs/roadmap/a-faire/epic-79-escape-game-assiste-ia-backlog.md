# EPIC 79 — Escape Game assisté par l’IA

## Références et état

- **État produit : À faire**, cadrage du **6 novembre 2026**, selon la
  [roadmap commune](../README.md).
- Identifiant `79` vérifié dans les documents communs, namespaces applicatifs
  et noms de fichiers des quatre dépôts applicatifs ; aucun backlog E79 trouvé.
- Demande utilisateur : nouvelle animation **« Escape Game assisté par l’IA »**.
- Antériorité : l'[E41](../terminees/epic-41-plateforme-animation-locale-mvp-backlog.md)
  mentionne l'Escape Game parmi les extensions futures, sans en définir le jeu.
  Ce cadrage ne rouvre pas E41.
- Socles : [moteur et chasse E55](../../specifications/moteur-animation/README.md),
  [Live E42](../../specifications/epic-42-localeo-live/README.md),
  [participation commerçante E56](../../specifications/epic-56-validation-participation-commercants-animation/README.md),
  [Animation E73](../../specifications/epic-73-animation-et-ou-coffrets/README.md).
  L'[E75](../../specifications/epic-75-mots-croises-assistes-ia/README.md) donne
  un autre précédent de préparation assistée, sans imposer son offre commerciale
  à E79. Le processus retenu est celui de la chasse E55 :
  [préparation manuelle outillée et import contrôlé](../../specifications/moteur-animation/conception-technique.md).
- Le moteur E55 prévoit déjà QCM, information, association, remise en ordre et
  saisie de mot/code. La réutilisation de ces activités est à examiner ; un
  nouveau jeu ne signifie pas nécessairement un nouveau moteur indépendant.
- Cadrage uniquement : aucune spécification détaillée, implémentation, migration
  réservée, intégration IA ou preuve de test métier E79 à ce stade.

## Problème, acteurs et résultat attendu

Créer une animation scénarisée demande de concevoir un récit, des énigmes
cohérentes, des indices utiles et une fin atteignable. L'IA assiste cette
préparation selon le processus de la chasse au trésor ; Localeo contrôle la
proposition avant validation et publication, puis accompagne l'habitant dans Live.

**Acteurs :** organisateur dans Animation ; préparateur Localeo dans l'ERP selon
les droits retenus ; habitant dans Live ; commerçant dans Pro lorsqu'une énigme
ou un passage le concerne. Les habilitations de préparation, dépôt, acceptation
et publication reprennent la séparation du processus E55 ; leur raccordement
au nouveau type sera détaillé dans la spécification.

**Exemple proposé, pas un scénario imposé :** « Le secret de la place ».
Des énigmes donnent des fragments permettant d'ouvrir un coffre virtuel final.
L'habitant voit son objectif, résout un défi, obtient un fragment et débloque la
suite. Les étapes se déroulent dans la commune et les commerces, selon le mode
terrain retenu. Le coffre virtuel ne constitue pas un lot gagné.

La différence produit visée par rapport à une simple succession de questions
est une **mission narrative avec dépendances entre énigmes et résolution finale**.
Ce profil et ses limites doivent être confirmés à la spécification, sans modifier
les règles existantes de la chasse au trésor.

## Décisions et base proposée

| Référence | Nature | Contenu |
| --- | --- | --- |
| E79-DEC-01 | Demande utilisateur | Cadrer une nouvelle animation « Escape Game assisté par l’IA » |
| E79-DEC-02 | Confirmation utilisateur, ARB-01 | IA pour préparer scénario, énigmes et indices ; contrôle puis validation avant publication ; aucune IA nécessaire pendant la partie |
| E79-DEC-03 | Confirmation utilisateur, ARB-03 | Parcours dans la commune et chez les commerçants, guidé par Localeo Live |
| E79-DEC-04 | Confirmation utilisateur, ARB-04 | Une progression personnelle sur un téléphone, utilisable seul ou en famille ; pas d'équipe multi-téléphones synchronisée en V1 |
| E79-DEC-05 | Précision utilisateur, ARB-02 | Même processus de préparation que la chasse au trésor E55 : brief et prompt, traitement IA manuel outillé, import contrôlé, corrections/acceptation puis validation avant publication explicite ; pas de fournisseur automatique supplémentaire imposé |
| E79-PROP-04 | Proposition, ARB-05 | Enchaînement explicite d'énigmes et fragments/codes, puis énigme finale ; réutiliser les activités du moteur lorsqu'elles répondent au besoin |
| E79-PROP-05 | Proposition UX | Objectif courant, progression, inventaire des éléments obtenus et action principale visibles ; récit court, indices à la demande et reprise du carnet |

Les propositions sont des hypothèses de travail. Les choix d'E75, E77 ou E78,
y compris les passages obligatoires, réponses uniques, tarifs et quotas, ne
constituent pas des décisions pour ce jeu. L'absence de réponse aux questions
ne vaut pas confirmation utilisateur.

## Périmètre

### Inclus dans le cadrage

- Création d'une édition avec thème, public, difficulté, lieux/commerces,
  périodes, objectif et règles de fin, à préciser avec l'organisateur.
- Brief et prompt de préparation IA, proposition issue du traitement manuel
  outillé puis import contrôlé selon le processus E55 confirmé en ARB-02 ;
  correction, aperçu et validation de la version finale.
- Contrôle des réponses attendues, dépendances, indices, accessibilité des lieux
  et cohérence narrative ; simulation du parcours avant publication.
- Expérience Live : introduction brève, mission courante, énigmes, réponses,
  éléments débloqués, indices et finale ; liens/QR orientés Live et reprise
  d'une progression existante.
- Parcours terrain : informations pratiques, accords commerçants, kit public
  et consignes privées ; responsabilités de préparation et éventuelle validation
  de passage à préciser dans les modalités E55 et en ARB-05.
- Suivi organisateur : préparation, progressions agrégées, blocages, réussite
  et incidents ; support avec droits bornés.
- Fin du jeu et éventuelle qualification au tirage/remise via les mécanismes
  existants selon ARB-07 ; distinguer réussite narrative et gain réel.

### Règles et responsabilités à préserver

Le **processus de préparation retenu** est celui de la chasse au trésor :

1. Le gestionnaire renseigne son brief et les lieux/commerces autorisés.
2. Localeo prépare et conserve le prompt et le contexte attendus.
3. L'opérateur habilité traite la demande avec l'IA en préparation, puis dépose
   le résultat dans le parcours d'import contrôlé.
4. Les contrôles de structure, cohérence et jouabilité précèdent l'acceptation ;
   les corrections produisent une nouvelle version à contrôler.
5. La préparation terrain, les accords et les validations humaines requis sont
   complétés avant publication.
6. Une commande de publication explicite fige la version validée. Accepter le
   résultat IA ne publie pas l'animation ; les permissions restent distinctes,
   sans imposer deux approbateurs différents si le socle ne le demande pas.

Cette réutilisation concerne la préparation et ses contrôles. Elle ne tranche
ni l'offre commerciale, ni les règles de progression, de passage ou de gain E79.

- **Le domaine backend porte la vérité du jeu** : disponibilité d'une énigme,
  correction, essais, déblocages, indices acquis et réussite finale. Les clients
  et l'IA ne peuvent ni inventer un succès ni attribuer un lot.
- Une génération est une proposition, jamais une publication ni une validation
  automatique. Une régénération ou modification invalide les approbations des
  contenus modifiés ; les effets sur le reste du scénario doivent être contrôlés.
- La publication fige le scénario, ses solutions et les règles jouées. Aucune
  réécriture dynamique ou modification rétroactive implicite pendant une partie.
- Vérifier que la finale est atteignable, que les prérequis existent et qu'aucune
  dépendance interdite ou référence manquante ne bloque la progression. Le profil
  autorisé, notamment linéaire ou à embranchements, reste à arbitrer.
- Projections publiques et privées distinctes : seules les étapes/indices
  autorisés sont transmis ; pas de solution ou code final caché dans le client.
- Dates/statuts et périmètres d'accès du domaine préservés. Un QR public est
  un point d'entrée, pas une réponse correcte ni une preuve de présence.
- Double clic, reprise réseau et rechargement retrouvent le même état : aucun
  double fragment, essai indû, déblocage supplémentaire ou double gain.
- Aucune donnée personnelle de participant, secret d'accès ou progression réelle
  à transmettre à un fournisseur IA pour préparer le scénario. Fournisseur,
  intégration, budgets et conservation restent à instruire avant tout appel réel.
- Mobile d'abord : énigme/action en premier, récit progressif, contrôles accessibles,
  retour clair après réponse, indices et aide faciles à distinguer. Les éléments
  graphiques proviennent des médias réellement préparés et validés.
- Listes, états de jeu et traitements de génération bornés ; mesures et budgets
  selon la [convention de performance](../../architecture/transverse/performance-volumetrie.md).

### Hors périmètre proposé pour une V1 simple

Le rôle de l'IA et l'absence d'équipes synchronisées découlent de DEC-02/04.
Les autres limites restent à préciser avec les arbitrages ouverts.

- Maître du jeu conversationnel en temps réel, scénario réécrit par un LLM
  pendant la partie ou correction probabiliste des réponses par IA.
- Coopération multi-appareils synchronisée, chat d'équipe et compétition en direct.
- Réalité augmentée, reconnaissance d'images, serrures ou salles physiques pilotées.
- Refonte des autres jeux, nouveau moteur de tirage ou nouveau compte habitant.
- Offre commerciale ou chronomètre punitif hérités implicitement d'un autre jeu.

## User stories

| ID | Besoin | Critères |
| --- | --- | --- |
| E79-US01 | Organisateur : décrire le jeu attendu dans un brief guidé | CA-01 à 02 |
| E79-US02 | Préparateur : produire avec l'IA puis contrôler un scénario jouable | CA-03 à 05 |
| E79-US03 | Organisateur : confirmer terrain, contenus et publication | CA-06 à 07 |
| E79-US04 | Habitant : comprendre sa mission et progresser dans les énigmes | CA-08 à 11 |
| E79-US05 | Habitant : demander un indice et reprendre sa partie | CA-12 à 13 |
| E79-US06 | Organisateur/habitant : distinguer réussite, gain éventuel et incident | CA-14 à 15 |
| E79-US07 | Localeo : garantir droits, confidentialité, usage mobile et capacité | CA-16 à 18 |

## Critères d'acceptation cibles

Les **18 critères E79-CA-01 à E79-CA-18** sont des cibles. Les modalités liées
aux arbitrages restent conditionnelles ; aucun test métier n'est déclaré exécuté.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E79-CA-01 | Organisateur habilité, modèle disponible | Créer un Escape Game | Brouillon identifiable et brief guidé ; aucune conversion d'une chasse existante |
| E79-CA-02 | Préparateur, brief incomplet ou complet | Préparer la demande IA | Thème, public, contraintes et objectifs explicites ; données manquantes signalées, pas de lieu/commerce ou d'accord inventé |
| E79-CA-03 | Préparateur autorisé, brief préparé selon E55 | Préparer le prompt, traiter avec l'IA puis importer la proposition | Prompt/contexte et provenance du résultat conservés, contrôles et erreurs compréhensibles, correction/reprise possibles ; aucun appel IA automatique ou publication déclenché par le dépôt |
| E79-CA-04 | Proposition avec énigmes et finale | Contrôler le scénario | Réponses, références, prérequis et atteignabilité contrôlés ; scénario incomplet, dépendance interdite ou finale inaccessible bloque la validation |
| E79-CA-05 | Contenu déjà approuvé | Modifier ou régénérer une partie | Différences et éléments à revalider identifiés ; aucune ancienne approbation réutilisée pour un contenu modifié |
| E79-CA-06 | Mode terrain retenu, organisateur/commerçants concernés | Confirmer lieux, commerces et kit | Préparatifs et accords requis traçables, consignes publiques/privées séparées ; publication refusée si un prérequis matériel obligatoire manque |
| E79-CA-07 | Organisateur prêt à publier | Simuler puis publier | Parcours contrôlable jusqu'à la finale, version approuvée figée et règles lisibles ; aucun changement du jeu publié par simple régénération |
| E79-CA-08 | Habitant via Live ou QR | Ouvrir puis démarrer | Mission/conditions compréhensibles, arrivée dans le bon jeu ; aucune soumission hors dates/statuts autorisés, authentification selon les accès existants |
| E79-CA-09 | Énigme accessible selon le profil retenu | Répondre correctement | Validation serveur, élément obtenu et suite déverrouillée selon les seuls prérequis publiés ; étape verrouillée inaccessible par URL/API manipulée |
| E79-CA-10 | Réponse incorrecte ou essais épuisés | Soumettre une réponse | Effet conforme aux règles d'essais retenues, retour explicite et prochaine action ; aucun fragment ou déblocage injustifié |
| E79-CA-11 | Tous prérequis de finale obtenus, ou incomplets | Répondre à l'énigme finale | Réussite seulement avec prérequis et réponse correcte ; inventaire et état final cohérents, sans lot attribué implicitement |
| E79-CA-12 | Participant demandant de l'aide | Consulter un indice | Indice autorisé pour l'énigme et règle d'accès/pénalité explicite selon ARB-06 ; pas de révélation anticipée des autres solutions |
| E79-CA-13 | Partie commencée, rechargement ou réponse réseau perdue | Reprendre ou rejouer la commande | Progression, fragments et indices conservés ; aucun essai, fragment ou gain doublé ; pas de nouveau compte imposé |
| E79-CA-14 | Partie réussie et règle de récompense publiée | Consulter résultat et éventuelle qualification | Réussite narrative distincte de qualification/gain ; tirage et lots existants réutilisés uniquement selon ARB-07 |
| E79-CA-15 | Lieu indisponible ou énigme erronée en jeu | Déclarer et traiter l'incident | Traitement explicite/tracé et information des joueurs selon ARB-08 ; aucune réécriture silencieuse de la version jouée |
| E79-CA-16 | Autre participant/commerce ou client incompatible | Lire/modifier un état privé, récupérer les solutions | Refus serveur et compatibilité explicite ; solutions, identifiants personnels et secrets absents des projections non autorisées et demandes IA |
| E79-CA-17 | Joueur sur mobile, au clavier ou avec lecteur d'écran | Comprendre l'objectif, répondre et demander de l'aide | Action principale et progression visibles, contrôles accessibles, récit progressif et absence de débordement horizontal ; aucun chronomètre/pénalité non annoncé |
| E79-CA-18 | Implémentation et fixtures futures | Exécuter les preuves proportionnées | Domaine, orchestration, API/consommateurs et parcours vérifient prérequis, erreurs, indices, reprise/concurrence, droits, incidents et non-régression ; générations et lectures bornées, capacité mesurée ; échecs/non-exécutés distingués des succès |

## Impacts à instruire

| Sujet | Analyse initiale et source |
| --- | --- |
| Domaine backend | **Concerné** : profil Escape Game, dépendances, inventaire/fragments, finale et règles d'aide ; examiner l'extension du moteur E55 avant de créer un moteur distinct |
| Application backend et IA | **Concernée** : réutiliser brief/prompt, traitement manuel outillé, import, contrôle, acceptation et reprise E55 selon DEC-05 ; adapter contrats et budgets au scénario E79 sans imposer un nouveau fournisseur intégré |
| Animation et ERP | **Concernés** : assistant guidé, préparation/simulation/validation, publication, suivi et incidents ; réutiliser les rôles/habilitations E55, raccordement au nouveau type à détailler |
| Pro | **Concerné pour le terrain retenu** : accords et kit ; préparation du contenu selon les modalités E55 et éventuel passage à préciser en ARB-05 ; pas d'accès aux solutions des autres commerces ajouté implicitement |
| Marketplace/Live | **Concerné pour Live** : rendu d'énigmes, inventaire, indices, finale et carnet mobile ; marketplace Coffrets conservée, liens vers Live |
| API et consommateurs | **Concernés** : configuration, génération/import, commandes et projections fermées publiques/privées, erreurs/compatibilité ; sources documentaires ici, générateurs et contrats embarqués dans les dépôts propriétaires |
| Persistance, migrations et existant | **À examiner** : versions, approbations, génération et état de jeu ; réutilisation des exécutions E55, données supplémentaires et unicités à préciser ; pas de numéro SQL réservé |
| Générateur et fixtures | **Concernés** : scénario atteignable/invalide, indices, erreurs/réussite, reprise, droits et incident terrain ; traitement des médias et conservation à préciser |
| Documentation fonctionnelle | **Concernée** : préparation organisateur/Localeo, guide et kit commerçant si terrain, prise en main Live, règles d'aide et de fin |
| Exploitation/déploiement | **À examiner** : offre/activation, secrets fournisseur seulement si intégration retenue, supervision génération, conservation, incidents et livraison coordonnée |
| Performance/volumétrie/coûts | **Concernés** : bornes scénario/médias, file et concurrence de génération si intégrée, lectures d'état et agrégations ; budgets à chiffrer et preuves N/10N/charge mixte avant activation |

## Arbitrages et décisions

**Quatre arbitrages résolus, quatre encore ouverts.** Le processus de préparation
E55 est repris sur demande explicite ; les autres règles ne sont pas déduites
des jeux existants.

| Référence | Décision attendue et recommandation | Dépendances |
| --- | --- | --- |
| E79-ARB-01 | **Résolu** : IA pour la préparation, jeu contrôlé et validé avant publication ; aucune IA nécessaire pendant la partie (DEC-02) | Déterminisme et absence de dépendance IA pendant le jeu |
| E79-ARB-02 | **Résolu** : même processus que la chasse au trésor E55 (DEC-05) : brief/prompt, traitement IA manuel outillé, import contrôlé, correction/acceptation et validation avant publication. Contrats, médias et budgets propres au type à détailler techniquement | Réutilisation du flux E55 et de ses habilitations ; acceptation distincte de publication |
| E79-ARB-03 | **Résolu** : jeu dans la commune et les commerces, guidé par Live (DEC-03) ; lieux et matériel propres à chaque édition à confirmer lors de sa préparation | Préparation, Pro/kit et QR |
| E79-ARB-04 | **Résolu** : une progression sur un téléphone, seul ou en famille ; équipes multi-appareils hors V1 (DEC-04) | Identité de la partie et reprise existante |
| E79-ARB-05 | **Ouvert** : progression linéaire recommandée en V1, fragments puis finale ; ou énigmes parallèles/embranchements ? Définir formes de réponses, éventuelle preuve de passage commerçante et réutilisation du moteur, sans héritage implicite des autres jeux | Déblocages, inventaire, contrôle de cohérence, validations et parcours |
| E79-ARB-06 | Chronomètre informatif, temps limité bloquant ou absence de durée de partie ? Nombre d'essais, indices gratuits/limités et éventuelles pénalités ; aucune valeur imposée au cadrage | Dates de partie, reprise, accessibilité et équité |
| E79-ARB-07 | Offre incluse/module payant, tarif HT, durée/quota et accompagnement ; réussite seule, tirage existant ou autre récompense ? Ne pas copier l'offre d'E75 | Souscription, publication, qualification et dotation |
| E79-ARB-08 | Énigme erronée ou lieu indisponible : suspension, reprise ou nouvelle édition et conséquences sur les parties en cours | Support, conservation et version publiée |

## Passage à la spécification

Les propositions permettent de cadrer le parcours sans présenter les arbitrages
comme acquis. Confirmer les choix avant de spécifier leurs branches dépendantes,
puis relier les 18 critères aux responsabilités, contrats, données, fixtures et
preuves selon le [cycle d'epic](../../organisation/cycle-epic.md). La clôture
reposera sur les tests pertinents ; ni pilote ni validation externe ne devient
une condition implicite par ce cadrage.
