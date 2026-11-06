# E73 — Localeo Live, entrée unique des animations

Évolution **E73-EVO-LIVE-UNIQUE**, demandée le **30 octobre 2026**.
L’epic 73 est **Terminée techniquement le 1er novembre 2026**, selon
E73-DEC-CLOTURE-TESTS et le [bilan de clôture](verification-livraison.md).
Les 63 critères initiaux et leurs résultats de recette restent conservés ;
les critères ci-dessous sont complémentaires et inclus dans cette revue.

## Décision et comportement attendu

En tant qu'habitant, découvrir les animations des communes choisies, s'inscrire
et retrouver ses participations dans un seul espace, Localeo Live, à
`https://animations.localeo.city`. En TEST : `https://test-animations.localeo.city`.
Le portail organisateur reste `gestion-animations.localeo.city`.

Cette décision remplace la surface publique marketplace Animation mise en place
par E73-EVO-DOMAINES et E73-EVO-UX-PUBLIC. Elle conserve le domaine décidé, les
données et les règles métier. Le même dépôt `localeo-marketplace` fournit Live
et Coffrets, sur leurs services respectifs ; aucun nouveau référentiel ni dépôt.
`LOCALEO_PUBLIC_SURFACE=ANIMATION` désigne désormais l'entrée Live. L'ancien
paramètre `surface=animations` ouvre aussi la transition vers Live.

**Arbitrage confirmé par l'utilisateur le 30 octobre : aucun nouveau compte
habitant.** Les communes sont mémorisées sur l'appareil ; leur association à un
compte ne s'applique que si un mécanisme existant la permet. L'installation
anonyme Live n'est pas un compte. Aucune synchronisation de compte n'est ajoutée.
Les contrôles existants des liens personnels, QR, PIN et WebAuthn restent en place.

Hors périmètre initial : refonte Coffrets, changement des règles d'animation,
catalogue ou base de participations distincts et recommandations personnalisées.
Le complément **E73-EVO-LIVE-ACCUEIL-RAPPELS** ci-dessous ajoute l'accueil
personnel et deux rappels facultatifs ; il remplace l'exclusion initiale des
nouvelles notifications pour ces deux seuls usages.

## Parcours et priorité mobile

### Évolution du 3 novembre 2026 — continuité habitant (E73-EVO-LIVE-CONTINUITE)

L'audit produit et sa mise en œuvre sont demandés le 3 novembre 2026. Cette
évolution conserve la clôture historique E73 et le choix sans nouveau compte.
Elle couvre les critères complémentaires suivants ; les preuves exécutées
sont consignées dans le suivi de réalisation, distinctes des tests prévus ici.

| Critère | Comportement attendu | Preuves prévues |
| --- | --- | --- |
| LC01 | Une liste de participations vide propose de retrouver une inscription existante, avec lien personnel ou restauration du carnet ; aucune recherche publique par adresse e-mail ne révèle les inscriptions. | Navigateur : nouvel appareil, lien absent/invalide, récupération et sauvegarde. |
| LC02 | Le scan du lieu possède un décodage de secours indépendant de BarcodeDetector et une alternative utilisable sans caméra ; le QR personnel et le PIN commerçant gardent leurs rôles distincts. | Décodeur, caméra indisponible, photo et QR invalide. |
| LC03 | Le domaine distingue tirage en attente, effectué avec gain, effectué sans gain et annulation ; l'interface ne déduit jamais un résultat de l'absence de lot. | Domaine, API personnelle, affichage de chaque état. |
| LC04 | Le badge reflète les non-lus autorisés, sans acquittement à l'ouverture ; le retour dans Live actualise le compteur. | Pagination, lecture, fermeture sans lecture et retour au premier plan. |
| LC05 | Les choix des nouvelles dans Live restent accessibles sans Push ; autorisation de l'appareil et accord organisateur restent distincts, facultatifs et révocables. | Push refusé/non compatible, réglages et retrait d'accord. |
| LC06 | L'accueil présente une action prioritaire et un résumé compact des nouveaux gains, messages et résultats disponibles, fondés sur les données personnelles autorisées. | États vide/erreur/partiel, absence de compteurs inventés et mobile. |
| LC07 | Les campagnes peuvent guider vers la participation ou les lots du destinataire sans conférer un accès nouveau ; l'absence d'accès utilise la récupération existante. | Destinataires distincts, accès révoqué, liens personnels et refus. |
| LC08 | Le centre propose réessai, filtre des non-lus et sélection d'une animation ; une importance n'est présentée que si elle est explicitement fournie. | Échec initial, filtres/pagination et lectures conservées. |
| LC09 | Les états bloquants proposent une aide contextualisée, avec coordonnées publiques autorisées lorsqu'elles existent et une procédure explicite sinon. | Aucun contact inventé, contexte du lot/animation et mobile. |
| LC10 | Le lieu actuellement accessible propose un itinéraire si son adresse est connue ; aucune étape future cachée n'est révélée. | Parcours chasse/passeport, adresse absente et lien encodé. |
| LC11 | La découverte propose recherche, filtres et sélection « Pour plus tard » sur l'appareil, distincte d'une inscription ; le partage ne contient que l'URL publique. | Recherche bornée, pagination, stockage refusé, partage sans token. |
| LC12 | Une date de tirage planifiée reste informative, ne déclenche pas de tirage et ne confirme pas de gain ; Live la présente seulement si elle existe et permet son ajout volontaire à l'agenda. | Configuration autorisée, date invalide, concurrence, API, affichage/repli et agenda sans donnée personnelle. |

Les célébrations reposent uniquement sur une étape réellement validée ou une
qualification confirmée. Elles respectent la réduction des animations et ne
bloquent pas l'action suivante. Les filtres locaux portent explicitement sur
les animations chargées ; une suite disponible reste accessible même si aucun
élément chargé ne correspond. Les favoris enregistrent des références publiques,
sans token ni duplication de participation. Les messages et états personnels
restent hors cache public. La livraison coordonne producteurs backend et Live ;
la saisie de date et les actions organisateur impliquent aussi leur consommateur
de gestion. La revue de contrats et les tests isolés ne valent pas recette de
Push réel, de caméra physique ou étude auprès d'habitants.

L'annonce de tirage est modifiable depuis Animation et le suivi ERP par un
gestionnaire autorisé, avec version attendue et clé d'idempotence. La date doit
être future et ne pas précéder la fin de l'animation ; elle peut être retirée.
Le domaine interdit la modification après réalisation/confirmation ou annulation
du tirage, ou lorsque l'animation est annulée ou archivée. Le fichier d'agenda contient uniquement
le titre et la date annoncée, sans accès personnel ni alarme imposée. Il ne se
met pas à jour automatiquement : cette limite est indiquée lors du téléchargement.

Navigation basse initiale : **Découvrir**, **Mes participations**, **Mes communes**.
Le complément Accueil/Rappels remplace le premier libellé par **Accueil**, sans
changer son URL `/live/decouvrir` ni supprimer la découverte publique.
Depuis le correctif du **31 octobre 2026**, la navigation comporte quatre entrées,
dans cet ordre : **Accueil**, **Mes participations**, **Mes lots**, **Mes communes**.
**Mes lots** ouvre directement `/live/lots` avec son propre titre de page et
remplace le sous-onglet du carnet. La destination reste active dans le détail
d'un bon ; les URL personnelles et les accès enregistrés sont conservés.
Découvrir présente les animations publiques **En ce moment** et **Prochainement**.
Une fiche montre titre, commune, dates, description, conditions et action autorisée.
Sa présentation sert l'entrée dans le jeu : type d'animation, **Votre défi** et
action de participation précèdent les textes détaillés. Pour un passeport
explicitement identifié, un objectif de validations positif configuré est mis
en chiffres ; tombola et chasse conservent des invitations adaptées à leur type.
Un type inconnu reste générique. Aucun avancement personnel, classement ni gain
n'est déduit de cette fiche publique. Les compteurs de `dynamique` connus sont
accompagnés de pictogrammes, avec une mention de dotation totale pour les lots.
Les récompenses et adresses participantes restent consultables avec leurs liens
existants. Description, conditions et règlement sont accessibles dans des volets
ouvrables, avec raccourcis depuis l'en-tête. Les actions d'inscription, de reprise
et de récupération gardent leurs autorisations et leur contexte de provenance.
Les cartes et l'en-tête de fiche reprennent exclusivement l'image personnalisée
configurée dans **Flyer**, lorsqu'elle existe et que le serveur l'autorise.
Sans image, après retrait ou si elle ne charge pas, le contenu reste lisible
sans illustration de remplacement ni colonne vide. La couverture du jeu et
les illustrations de ses étapes ne servent pas de repli. Voir le
[contrat Flyer](flyers-contextualises.md#règles-de-conception-et-contrats).
L'inscription réutilise le formulaire existant sous `/live/animations/:id/inscription`.
Les participations et lots personnels conservent leurs accès dans le carnet.

Harmonisation du **3 novembre 2026** : la page personnelle ouverte par
**Commencer mon parcours** ou **Reprendre mon parcours** reprend les surfaces
arrondies, pictogrammes et commandes de retour/actualisation de Live. Le titre,
le nombre réel d'étapes terminées et la qualification fournie par le serveur
forment un aperçu commun ; l'étape active et son action précèdent les options.
**Mon inscription** et **Messages de l'organisateur** sont des volets secondaires
accessibles au clavier. Une décision de consentement non confirmée ouvre
automatiquement son volet, y compris après rechargement, sans renvoi implicite.
L'adresse absente reste explicitement indiquée dans le volet d'inscription.
Les thèmes configurés du jeu et des étapes restent prioritaires ; sans couleur
de surface explicite, leur fond sert de repli pour préserver le contraste.
Le scan du lieu, le QR personnel, le PIN, les gains et la satisfaction gardent
leurs composants et autorisations. Aucun score ni illustration fictifs ajoutés.

Complément du même jour : l'actualisation utilise une icône seule, placée sur
la même ligne que le titre (participations, parcours, bon et en-têtes existants).
Sa cible tactile reste de 44 px, avec nom accessible, infobulle, focus visible
et état de chargement. Le titre peut revenir à la ligne sans repousser l'icône
en dessous. Les actions explicites de réessai après erreur gardent leur texte.

Conception mobile d'abord : écran de référence 320–390 px, pas de débordement
horizontal, champs à 16 px, actions tactiles d'au moins 44 px, navigation à portée
du pouce et marge de sécurité PWA. Pas d'accueil marketing avant les tâches.
États de chargement, vide, erreur, stockage refusé et réseau indisponible explicites.
Le clavier, le focus, le texte agrandi à 200 % et la réduction des animations
restent utilisables. Les libellés de navigation peuvent revenir à la ligne.

Précision UX mobile du **31 octobre 2026** : Live privilégie les interactions
et la progression réelle. Sur la fiche publique, l'action principale unique
(inscription ouverte ou accès aux participations existantes) reste accessible
pendant le défilement sur téléphone, au-dessus de la navigation basse. Sa
position suit la hauteur réelle de cette navigation, y compris avec du texte
agrandi ; un espace est réservé pour accéder au bas de la page. Sur un écran
de faible hauteur, l'action reste dans le flux pour préserver la lecture.
Les raccourcis vers lots, adresses et conditions précèdent les informations
détaillées. La récupération est nommée **Retrouver mon inscription**, distincte
de l'inscription ; les accès personnels et le contexte de provenance sont conservés.

L'accueil conserve une priorité dominante et deux suivantes compactes, avec
anneaux, étapes restantes et actions de reprise. Un raccourci **Les défis locaux**
permet de rejoindre le programme sans parcourir ces priorités. Le résumé
**Mes communes** affiche son compteur puis **Choisir une commune** : les liens
individuels et la modification se déplient à la demande, sans repousser le
catalogue derrière dix communes. La sélection initiale, lorsqu'elle est vide,
conserve la recherche et la géolocalisation volontaire.

**Mes lots**, complété à la demande du **3 novembre 2026**, réunit désormais
les **coffrets, bons numériques et lots libres** gagnés via les participations
auxquelles l'installation possède un accès personnel valide. Cette demande
remplace la restriction antérieure aux seuls bons enregistrés sur l'appareil.
Les gains à utiliser, activer ou retirer et les gains en préparation précèdent
l'historique replié **Déjà utilisés ou retirés**, qui contient aussi les lots
expirés, annulés, refusés ou remplacés. L'état provient du serveur : un coffret
envoyé ne vaut pas coffret consommé, une remise libre doit être explicitement
déclarée, une qualification ne vaut pas attribution.

Pictogrammes par nature, compteurs des éléments affichés, cartes de récompense
et actions larges permettent une lecture rapide. **Nouveau** signifie que le
gain n'a pas encore été consulté sur cet appareil ; le clic sur sa consultation
ou l'ouverture de ses consignes mémorise seulement son identifiant localement.
Ce repère ne vaut ni retrait, ni consommation, ni écriture métier. Il reste
indépendant de l'état serveur et n'est pas affiché sur les gains historiques.

Les bons ajoutés localement restent visibles même sans suivi de participation.
Ils portent **Dernier état connu**, vérifié à l'ouverture du bon exact. Une
attribution serveur et un bon local de même identifiant ne sont affichés qu'une
fois, avec l'état serveur prioritaire. La liste ne délivre aucune capacité
personnelle : sans accès au bon enregistré, **Voir mon lot** reprend la
participation personnelle et son parcours existant. Le stockage du carnet
et la récupération par e-mail restent explicites.

**Mes prochains tirages** présente uniquement les participations explicitement
qualifiées par le moteur, dans le périmètre autorisé et encore en attente de
tirage selon la projection serveur. Aucun classement ni chance de gain n'est
inventé. Le modèle actuel ne prévoit pas de date de tirage planifiée :
**Date à annoncer** est affiché, sans utiliser la date de fin de l'animation
comme date de tirage. Les résultats gagnés ne sont jamais déduits d'un parcours
terminé à 100 %.

Gains et tirages possèdent des paginations indépendantes. Les compteurs restent
ceux des éléments affichés, sans promettre un total global. Une page de
tirages filtrée peut être vide tout en offrant une suite. Une panne laisse
les bons enregistrés accessibles et propose un réessai explicite, sans effacer
le carnet. L'actualisation garde son icône dans la ligne du titre.

La recherche ajoute ou retire des communes sans changer les inscriptions. Une
commune partagée par URL constitue un contexte de consultation : son ouverture
ne modifie pas silencieusement les communes suivies. Le suivi exige une action.

**Mes communes** privilégie les repères graphiques : nombre de communes suivies
sur ce navigateur, pictogramme de localisation, nom, code postal disponible et
état de suivi. Chaque commune propose **Voir les animations**, avec un retrait
secondaire nommé explicitement pour les lecteurs d'écran. Recherche et
**Autour de moi** sont regroupés ; les détails d'utilisation de la position
restent accessibles à la demande. Le compteur ne représente ni un nombre
d'animations ni un score : la borne reste de dix communes. Aucune carte, photo
ou statistique territoriale n'est inventée. La même présentation sert la page
dédiée et la sélection initiale intégrée à Découvrir, avec états vide et erreurs.

## Audit d’usage du 1er novembre 2026 — habitant peu familier du numérique

L’audit expert parcourt la découverte, le choix d’une commune, l’inscription,
la reprise d’un accès personnel et les lots sur téléphone. Il conserve le Live
immersif existant : repères visuels et actions de participation avant les
explications secondaires. Il ne constitue pas un essai avec de vrais habitants.

| Situation | Obstacle constaté | Comportement corrigé |
| --- | --- | --- |
| Recherche de commune indisponible | « Réessayez » sans moyen de relancer le même texte | Bouton **Réessayer la recherche**, saisie conservée et aucune sélection automatique |
| Lien communal invalide | **Choisir une commune** efface le contexte sans ouvrir le choix lorsque des communes sont déjà suivies | Accès réel à **Mes communes**, sans modifier la sélection enregistrée |
| Programme vide après sélection | Le bandeau demande encore de choisir une commune | Chargement, vrai vide et indisponibilité distingués ; **Modifier mes communes** sur le vrai vide, réessai sur panne |
| Détail personnel en panne | Le retrait du carnet est l’action proposée dans l’erreur | **Réessayer** reprend le même accès ; conservation locale expliquée, retrait secondaire dans les options |
| Fiche publique ouverte directement | Le retour aux animations mène au carnet personnel | Retour par défaut à la découverte ; provenance et retour contextuel existants prioritaires |
| Navigation avant inscription | **Mes participations** apparaît active sur une fiche publique | Fiche et inscription restent rattachées à **Accueil** ; les accès personnels, ajouts au carnet et lots conservent leur rubrique |
| Retrouver une inscription | Titre « Ajouter une inscription » et nouvelle inscription en concurrence avec la récupération | Titre **Retrouver mon inscription**, e-mail et action principale uniques ; nouvelle inscription sous **Pas encore inscrit ?** |
| Suite de récupération par e-mail | Étape suivante peu explicite | **Vérifiez votre boîte e-mail**, courriers indésirables, ouverture du dernier lien puis ajout au carnet ; réponse conditionnelle conservant la confidentialité |
| Inscription refusée ou non confirmée | Champs requis peu explicites et erreur éloignée du focus ; action identique avant/après réponse incertaine | Quatre champs obligatoires annoncés, notifications **Facultatif**, erreur focalisée, **Réessayer la même inscription** sans nouvelle clé ni modification du corps conservé |

Principes retenus : une tâche et une action principale identifiables, mêmes
termes que la navigation, textes courts donnant une prochaine action réelle,
saisies préservées après erreur et retrait séparé de la reprise. La fermeture
rend le focus au déclencheur ; **Utiliser une autre adresse** revient au champ
e-mail. Mobile, clavier et texte agrandi restent utilisables. Le GPS et
l’installation de l’application restent facultatifs ; aucun compte habitant
ni nouvelle étape de connexion n’est ajouté.

L’interface possède ces corrections de présentation. Règles d’inscription,
participations, consentements, tokens et contrats restent dans leurs producteurs
existants ; aucune donnée ni migration n’est créée. Les preuves locales et les
limites de l’audit figurent dans le [suivi d’implémentation](suivi-implementation.md).

## Audit d’usage du 2 novembre 2026 — continuité et actions

Cette passe suit le parcours d’un habitant : choisir une commune, découvrir
une animation, s’inscrire, reprendre son parcours et consulter un lot. Elle
complète l’audit précédent, sans remplacer les règles de participation. La
lecture des sources est complétée par des parcours navigateur isolés sur mobile
et PC ; il ne s’agit pas d’un essai auprès d’habitants réels.

| Priorité | Obstacle observé | Correction |
| --- | --- | --- |
| Haute | Retour de fiche perdant le filtre communal et la position de lecture | Provenance transmise par les cartes et la vedette ; retour à la commune consultée, restauration de la position et du focus lorsque le résultat est chargé. Le passage par l’inscription conserve cette provenance. |
| Haute | « Voir le détail » cache la reprise du jeu, derrière le QR | Action personnelle principale **Commencer mon parcours**, **Reprendre mon parcours** ou **Voir ma participation**, selon les données disponibles ; présentation du QR conservée séparément. |
| Haute | Détail personnel sans adresse, retour navigateur quittant la liste | Ouverture avec `?participation=` pour l’accès exact ; actualisation et historique du navigateur conservent la destination. Retour à la liste avec position et focus mémorisés temporairement. |
| Moyenne | Actualisation par icône seule ou boutons différents, sans retour visible dans le jeu | Composant commun avec icône et **Actualiser**, libellé accessible contextualisé, état **Actualisation…** et bouton désactivé pendant la lecture. Saisie de jeu conservée ; aucune commande métier rejouée. |
| Moyenne | « Mes animations », « carnet » et « Mes participations » désignent la même destination | **Mes participations** pour la destination ; composant de retour commun aux fiches, parcours et bons. « Carnet » reste utilisé pour expliquer la conservation locale. |
| Moyenne | « Ajouter une autre inscription » ouvre une récupération | **Retrouver une autre inscription**, distinct de l’action de nouvelle inscription. |
| Moyenne | À 200 % de texte, l’actualisation comprime le titre et les actions coupent leurs mots | En-tête et boutons passent sur des lignes distinctes lorsque la largeur manque ; le nombre dans l’anneau reste sur une ligne. |

L’esprit jeu repose sur les défis, les anneaux de progression, les lots et les
indicateurs réellement disponibles. Les appels publics emploient **Découvrir
l’animation** ; les actions personnelles disent ce qui va se passer. Une courte
apparition d’écran, sans déplacement des commandes, accompagne la navigation ;
elle est désactivée lorsque les mouvements sont réduits. Les contrôles conservent
une cible tactile de 44 px et un focus visible.

Les deux compléments de cet audit sont traités :

- La présentation vedette + carte compacte a été remplacée le 3 novembre par
  une seule carte complète par animation, pour libérer le premier écran.
  Le visuel Flyer, le défi et les compteurs restent dans cette carte ; le
  bandeau communal présente uniquement le contexte et l'aperçu des périodes.
- Au retour d’une fiche, les pages supplémentaires déjà consultées sont relues
  depuis l’API, avec ses curseurs courants, avant de restaurer position et focus.
  Le retour explicite, le retour navigateur et le rechargement dans la fiche
  conservent ce parcours. Seuls les repères de navigation (communes/périodes,
  nombre de pages, position et lien) sont mémorisés, pour dix entrées d’historique
  au maximum dans la session du navigateur ; aucune réponse du catalogue ni
  donnée personnelle n’est mise en cache par ce mécanisme.

Une erreur de pagination conserve les pages fraîchement obtenues et propose une
reprise des pages manquantes. Si l’animation a disparu du catalogue courant, le
focus revient au titre du programme. **Actualiser** et le changement de sélection
communale repartent de la première page. Le stockage indisponible conserve le
retour dans la session ouverte ; après rechargement, la provenance transmise
par le lien reste utilisable pour le retour explicite.

Impacts : présentation et navigation Marketplace/Live, documentation E73 ;
aucun contrat API, règle métier, droit, migration, paramètre d’exploitation ou
générateur modifié par ce correctif UX. Les images restent celles configurées,
les données personnelles et les consentements gardent leur traitement existant.
Les résultats et les limites de vérification figurent dans le
[suivi d’implémentation](suivi-implementation.md).

## Contre-audit du 2 novembre 2026 — validation du nouveau parcours

Cette revue expert contrôle l’arbre local Marketplace `bb8b585` complété des
correctifs UX précédents. Elle combine des scénarios navigateur isolés, des
captures et une lecture indépendante des parcours. Les API sont simulées :
elle ne valide ni le site TEST déployé ni l’usage avec de vrais habitants.

**Bilan :** le parcours courant est plus cohérent : quatre destinations stables,
actions de découverte/reprise distinctes, récupération d’inscription explicite,
carte vedette allégée et retour aux pages déjà parcourues. La nouvelle passe ne
remet pas en cause ces acquis. Elle a identifié les huit points ci-dessous.
L’audit initial ne modifiait pas le code ; leur prise en compte a ensuite été
demandée et implémentée dans le correctif décrit après ce tableau.

| Priorité | Constat et nature | Traitement recommandé et preuve attendue |
| --- | --- | --- |
| Haute | **Action masquée au clavier.** Dans Découvrir, Tab peut placer le focus sur un bouton derrière la navigation basse. Reproduit à 390×844 et 568×320 ; la capture montre l’action entièrement recouverte. | Réserver la zone visible lors du défilement vers le focus, en tenant compte des barres haute/basse et des actions fixes. Rejouer la tabulation complète, texte agrandi et écran bas ; le contrôle focalisé doit rester visible. Sources : `live.css`, `live-play-shell.css`, navigation commune. |
| Moyenne | **Animation disparue au retour.** Si l’animation de page 3 n’existe plus dans les réponses fraîches, le titre du programme reçoit le focus mais l’ancien scroll est conservé, loin du titre. Défaut reproduit. | Restaurer l’ancienne position seulement si le lien d’origine existe ; sinon montrer réellement le programme et expliquer son actualisation. Source : `LiveDiscovery.jsx`, effet de restauration. |
| Moyenne | **QR réaffiché par l’historique.** Détail → retour liste → Présenter mon QR → Avancer navigateur → Retour : la fenêtre QR réapparaît sans nouvelle action ni lecture. Défaut reproduit, sans preuve d’accès non autorisé. | Fermer la fenêtre et invalider sa lecture lors du changement de destination personnelle, tout en conservant les pages de la liste. Vérifier Back/Forward et absence de réouverture automatique. Source : état `qr` de `LiveAnimations.jsx`. |
| Moyenne | **Consigne contradictoire sur une fiche déjà enregistrée.** Lorsque l’enrichissement personnel manque, « Dans mon carnet ✓ » et « Ouvrir mes participations » peuvent coexister avec « Ajoutez-la au carnet ». Défaut rédactionnel reproduit. | Donner priorité à la présence locale pour la consigne ; garder une récupération distincte pour une autre inscription. Vérifier les combinaisons inscription connue, accès local et lecture d’enrichissement indisponible. Source : pied de fiche de `LiveAnimationDetail.jsx`. |
| Moyenne | **Panne de Mes lots sans réessai.** L’échec de lecture du carnet affiche une aide e-mail, mais aucune commande pour réessayer sur place. Lacune de récupération observée. | Ajouter une action de réessai à la lecture locale, sans effacer le carnet ; tester refus transitoire puis réussite et refus persistant. Source : `LiveLots.jsx`, lecture initiale. |
| Moyenne | **Portée de Mes lots ambiguë.** La liste contient les bons numériques enregistrés, alors que le vide dit « Retrouvez ici vos lots gagnés ». Les autres gains restent dans la participation ; le renvoi est caché sous l’aide e-mail. Optimisation de compréhension, pas un défaut du contrat de gains. | Préciser simplement « Vos bons enregistrés sur cet appareil » et rendre visible l’accès aux autres récompenses dans Mes participations. Ne pas déplacer ni dupliquer les gains sans évolution fonctionnelle distincte. Source : états vide/liste de `LiveLots.jsx`. |
| Basse | **Deux chemins au premier choix de commune.** Sans commune suivie, un bouton ouvre Mes communes alors que la recherche est déjà présente dans l’accueil. Optimisation de fluidité ; aucun blocage. | Faire du bouton un raccourci vers la recherche intégrée, avec focus dans le champ, puis garder Mes communes comme destination de gestion. Sources : `LiveCommunityScene.jsx` et `LiveDiscovery.jsx`. |
| Basse | **Repères de navigation invalides.** Une entrée de session volontairement corrompue avec `pages:{}` provoque un écran d’erreur ; Actualiser reproduit l’échec. Robustesse démontrée sur donnée injectée, pas défaut constaté en usage nominal. | Valider et ignorer les repères invalides, puis repartir de la première page. Tester structure erronée et stockage indisponible sans perdre les accès personnels. Sources : `liveDiscoveryNavigation.js`, `LiveDiscovery.jsx`. |

**Prise en compte des huit points :**

- Un traitement commun de la tabulation ajuste uniquement le défilement
  nécessaire pour révéler le contrôle devant les barres réellement visibles.
  Il mesure le conteneur extérieur même dans le formulaire d’inscription,
  respecte les actions fixes et celles dans le flux sur écran bas, et laisse
  les dialogues natifs ou ARIA gérer leur propre navigation. Les focus de
  retour programmatiques restent indépendants de ce traitement.
  Le piège de focus commun inclut les dialogues natifs ouverts et les éléments
  dépliables. L’inscription Live n’exécute plus la restauration différée de la
  marketplace, qui pouvait ramener en haut un formulaire déjà parcouru au clavier.
- Lorsque le lien d’origine n’est plus présent, focus et défilement reviennent
  ensemble au titre du programme ; une explication signale l’actualisation.
  Les repères de navigation sont validés depuis la session comme depuis l’état
  de l’historique, limités aux champs utiles et ignorés si leur structure est
  invalide. Ils ne remplacent jamais la lecture des données courantes.
- Tout changement de destination personnelle ferme le QR et invalide sa lecture
  en cours. Une nouvelle présentation explicite reste possible ; les pages de
  la liste et les accès personnels sont conservés.
- La présence locale prime dans la consigne de fiche : **Cette animation est
  enregistrée sur cet appareil. Retrouvez-la dans Mes participations.** Ce texte
  reste juste pour un ancien signet, sans promettre un accès personnel absent.
- Mes lots précise les bons numériques locaux, expose le lien vers les autres
  récompenses et permet de réessayer sa lecture. La réponse d’un écran quitté
  est ignorée ; le bouton est désactivé pendant la nouvelle lecture.
- Sans commune suivie, **Choisir mes communes** place le focus dans la recherche
  déjà affichée et la rend visible, sans changer de page. Si cette recherche
  n’est pas présente, notamment dans un contexte de lien communal invalide,
  le choix ouvre la page Mes communes.

Les tests et captures du correctif complètent les preuves initiales dans le
suivi. Le contrôle du focus s’appuie sur le principe de
[focus non entièrement masqué du W3C](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).
Les largeurs réduites sont examinées selon le principe de
[redistribution du contenu](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html),
sans prétendre à un audit exhaustif de conformité WCAG.

Les preuves, commandes et résultats distincts sont consignés dans le
[suivi d’implémentation](suivi-implementation.md). Aucun arbitrage métier,
contrat API, droit, migration ou générateur ne change dans cet audit.

## Nouvel audit du 2 novembre 2026 — après les huit corrections

Relecture depuis le point de vue d’un habitant, sur l’arbre local intégrant les
huit corrections précédentes. Le périmètre comprend la découverte, les communes,
les inscriptions et leur récupération, les participations, les lots et les
interactions de jeu. Les résultats exécutés sont consignés dans le
[suivi de réalisation](suivi-implementation.md#2-novembre-2026--nouvel-audit-live-après-les-huit-corrections).
Cet audit ne modifie pas le code de production et ne vaut pas recette du site déployé.

Le parcours courant conserve ses améliorations : une entrée directe dans les
animations, des actions de participation distinctes de la récupération, un carnet
unique et une navigation utilisable au clavier avec les barres fixes. Les huit
points précédents restent corrigés dans les scénarios rejoués. Aucune nouvelle
refonte visuelle générale n’est justifiée par les observations de ce passage.

Trois points restent à traiter, dans l’ordre recommandé :

| Priorité | Observation reproduite | Conséquence pour l’habitant | Optimisation proposée |
| --- | --- | --- | --- |
| P2 — lien personnel | Un lien personnel est validé (200), puis la lecture du contact échoue (503). L’écran « Garder ma participation » n’affiche que l’erreur, sans réessai. Une recharge après rétablissement du service fonctionne. | Une personne arrivant depuis son e-mail peut croire que son inscription ou son lien est invalide. | Ajouter **Réessayer la vérification**, un état occupé et une explication rassurante ; garder les contrôles d’accès et ignorer les réponses tardives. |
| P2 — commune partagée | Après un 503 sur la lecture de la commune passée en URL, **Actualiser** ne refait pas cette lecture. Le message invite pourtant à réessayer. Une recharge du navigateur conserve le filtre et réussit. | L’action proposée ne permet pas de reprendre ; changer de commune paraît être la seule solution. | Relancer aussi la commune lors de l’actualisation ou proposer **Réessayer cette commune**, sans modifier les communes suivies. |
| P3 — visibilité de l’incident personnel | Avec six animations publiques, l’avis d’échec des priorités personnelles commence à environ 3 126 px du haut sur un écran 390 × 844. Le bouton d’actualisation est en haut, sans réessai à proximité de l’avis. | L’accueil paraît normalement chargé alors que les défis personnels ont disparu temporairement ; il faut parcourir le catalogue pour comprendre. | Afficher un avis compact près de l’emplacement des défis personnels, avec réessai et accès au carnet, tout en laissant la découverte disponible. |

Ces défauts de reprise ne démontrent ni perte de données ni inscription dupliquée.
Les deux premiers ont un contournement par recharge de page ; le troisième
conserve l’accès à **Mes participations** dans la navigation. Les captures et
comptages de requêtes distinguent les observations des recommandations. Les
tests exploratoires constatant un défaut ne sont pas comptés comme une preuve
de conformité de ce comportement.

## Critères ajoutés et preuves

Les numéros 01 à 12 reprennent les CA1 à CA12 fournis par l'utilisateur.

| Critère | Résultat observable et preuve attendue |
| --- | --- |
| E73-EVO-LIVE-01 | Catalogue et détail consultables sans compte, y compris sans carnet local ; aucune permission personnelle déduite de la consultation. |
| E73-EVO-LIVE-02 | Recherche et sélection de plusieurs communes, persistance locale, modification et stockage refusé ; aucun compte nouveau selon l'arbitrage confirmé. |
| E73-EVO-LIVE-03 | Deux périodes, seuls résultats publics retournés par le producteur, pagination et état vide permettant de modifier les communes. |
| E73-EVO-LIVE-04 | Fiche vers inscription ou participation, même contexte d'animation et code de diffusion ; conservation des mécanismes d'accès existants, aucun nouvel écran de connexion fictif. |
| E73-EVO-LIVE-05 | Même participation et historique après reprise volontaire du carnet, sans création de compte, doublon métier ou effacement de l'origine. |
| E73-EVO-LIVE-06 | `/live/decouvrir?commune=<UUID>` partageable ; `/live/animations/:id` et anciens liens personnels fonctionnels. |
| E73-EVO-LIVE-07 | Domaine HTTPS dédié, même backend, accès directs et actualisation ; vérification DNS/TLS et hébergée distincte des tests locaux. |
| E73-EVO-LIVE-08 | Anciens liens personnels et QR conservés ; aucune redirection globale des capacités ni utilisation du secret d'installation d'une autre origine. |
| E73-EVO-LIVE-09 | Ancien catalogue et `surface=animations` quittent l'interface marketplace, contexte commune/animation conservé ; reprise du carnet proposée avant sortie d'origine. |
| E73-EVO-LIVE-10 | Navigation Animation de la marketplace vers Live ; parcours Coffrets et anciens `/live/*` conservés. |
| E73-EVO-LIVE-11 | Découverte, communes, inscription et carnet utilisables à 320/390 px et en PWA ; safe-area et accès au clavier. |
| E73-EVO-LIVE-12 | Recette de bascule : domaine, lecture anonyme, inscription, reprise des accès, historique, redirections et non-régression Coffrets. Aucune mise en service déclarée sur la seule base d'un build. |

## Complément UX du 30 octobre 2026 — E73-EVO-LIVE-UX

Retour utilisateur après la première version : supprimer le rappel de marque
au-dessus de Découvrir, clarifier son icône et conserver **Mes communes** comme
unique écran de gestion. Les anciens accès Réglages `?focus=city` ouvrent cet
écran ; les réglages de carnet et notifications restent disponibles. Leur
ouverture ne remplace ni ne synchronise implicitement une commune par défaut.

La découverte présente la dynamique et le défi de chaque animation, en priorité
mobile, sans faux classement, probabilité de gain ou activité simulée.

| Critère ajouté | Comportement attendu |
| --- | --- |
| E73-EVO-LIVE-UX-01 | Marque conservée dans l'en-tête, sans rappel dans le contenu Découvrir ; boussole et libellé Découvrir, repère cartographique pour Mes communes ; suppression du raccourci icône redondant de la surface Animation. |
| E73-EVO-LIVE-UX-02 | Recherche et modification des communes dans Mes communes ; aucun second sélecteur dans Réglages ; catégories de notification et Push conservent exactement les communes choisies, y compris une sélection vide. |
| E73-EVO-LIVE-UX-03 | Cartes avec l'image personnalisée du Flyer si disponible, sinon sans illustration : statut serveur, défi configuré s'il existe, nombres publics de participants, gagnants et unités en dotation. Zéro confirmé distinct d'une valeur inconnue ; ancien backend compatible sans compteurs. |
| E73-EVO-LIVE-UX-04 | À 320/390 px, pas de débordement, liens tactiles et données lisibles ; texte agrandi, clavier et réduction des mouvements préservés. |

Contrat additif catalogue/détail : `dynamique` avec `nombre_participants`,
`nombre_gagnants`, `nombre_lots_a_gagner`, entiers non négatifs ou valeurs
inconnues nulles. Participants = inscriptions présentes, tous statuts confondus,
selon le compteur métier existant. Gagnants = participants disposant d'une
attribution courante, hors suppléants et attributions remplacées ; pour les lots
libres, le tirage doit être confirmé, selon les projections de bilan.
Lots = nombre total d'unités de la dotation, pas nombre de catégories de lots,
ni stock restant. Cette portée est indiquée sur la carte. Aucune identité,
capacité personnelle ou donnée de contact n'est publiée.

Le backend fournit cette projection de lecture groupée pour la page publique
autorisée ; aucun appel par carte et aucun calcul métier côté interface. Le
frontend omet les valeurs absentes, négatives ou non entières sans les convertir
en zéro. Le défi reprend le nombre de validations configuré sans fabriquer une
progression personnelle. Les compteurs sont ceux de la lecture, sans promesse
de mise à jour en temps réel. L'ancien champ `nombre_lots` reste compatible.

Impacts : backend et contrat OpenAPI documentaire additifs, consommateur Live
et fixtures adaptés ; pas de migration, nouveau compte, permission, commande
métier, tâche, fournisseur ou configuration DNS. Les données de démonstration
existantes alimentent les mêmes lectures ; pas de génération réelle nécessaire.
La validation hébergée et les mesures PostgreSQL de volumétrie restent distinctes
des tests isolés. Les preuves sont consignées dans le suivi d'implémentation.

## Évolution du 30 octobre 2026 — E73-EVO-LIVE-ACCUEIL-RAPPELS

Demande acceptée : un accueil personnel mobile et deux rappels personnels
facultatifs, pour terminer un parcours et agir avant sa fermeture. Cette
évolution remplace le premier onglet Découvrir par **Accueil**, conserve ses URL
et le catalogue public et étend le périmètre antérieurement exclu des nouveaux
rappels personnalisés. Aucun compte habitant n'est créé. L’EPIC 73 restait alors
**En cours** ; les critères et preuves historiques ne sont pas réécrits.

### Parcours et décisions retenues

**US-LIVE-ACCUEIL.** En tant que participant, voir immédiatement les parcours
proches de leur objectif ou de leur échéance et reprendre le bon accès personnel.
Depuis le correctif UX du **31 octobre 2026**, l'accueil ouvre sur le défi personnel
prioritaire lorsqu'il existe, afin de rendre son action visible dès l'arrivée
sur mobile. La vie des communes suivies vient ensuite, ou ouvre l'accueil en
l'absence de priorité : accroche contextualisée, animation à rejoindre avec l'image
personnalisée du Flyer si disponible, nombre réel de participants à cette
animation et accès directs aux périodes. Les nombres d'animations sont ceux
de l'aperçu chargé, dédupliqués par période ; pagination et erreurs sont
signalées comme un aperçu partiel. Aucune somme d'habitants uniques, activité
instantanée ou illustration par défaut n'est inventée. Une indisponibilité
totale propose de réessayer ; le vrai vide propose de modifier les communes.

Une priorité personnelle principale et deux suivantes compactes sont présentées
avant le programme communal. Un raccourci **Mes défis à reprendre**
dans l'en-tête y mène directement, même sur mobile. L'accueil ne présente plus
de section **Mes autres participations**, de pagination ni de liaison des accès.
Le lien **Toutes mes participations** rejoint `/live/animations`.
Cette page réunit le carnet local et les participations liées à l'installation,
avec déduplication par identifiant exact de participation ; deux inscriptions
à la même animation restent distinctes. Depuis le correctif UX du **1er novembre
2026**, elles apparaissent dans une seule liste : aucun bloc **Mes accès liés**
ni compteur technique vide. Les accès distants absents du carnet
proposent **Retrouver mon inscription**, qui ouvre le formulaire e-mail existant sans
créer ni substituer un token. Une entrée importée sans accès utilisable propose
aussi une récupération explicite ; elle ne permet pas de présenter un QR.

**Mes participations** reprend les images Flyer disponibles, les pictogrammes,
les anneaux et les étapes validées/restantes. Les nombres du carnet portent sur
les entrées présentes sur l'appareil, sans fabriquer un total global à partir
d'une page distante. Les gains et qualifications
conservent leurs statuts serveur, indépendamment du pourcentage. Une progression
absente ou incohérente n'est pas représentée par un anneau à zéro. La pagination
distante remplace la page précédente, au plus 50 éléments par page ; les anciens
accès se relient uniquement sur action explicite, par lots de 50 et avec deux
requêtes concurrentes au plus. Un échec de synchronisation laisse le carnet
local utilisable, avec ses informations conservées et l'état d'erreur visible.
Une unique action **Actualiser mes participations**, lorsqu'il existe des
participations ou une lecture à reprendre, recharge la liste et propose la
liaison explicite des anciens accès utilisables. Un lot supplémentaire reste
une action volontaire **Actualiser les participations suivantes**. Aucun
rattachement n'est déclenché par le simple affichage de la page.
La pagination distante conserve les entrées locales ; ses commandes restent
disponibles même lorsqu'une page entière est déjà présente dans le carnet.
Le vide d'accueil n'est présenté qu'après confirmation de l'absence de résultats,
jamais pendant le chargement ou à la suite d'une erreur de lecture distante.
Sur l'accueil, **Actualiser** recharge participations et catalogue, avec annulation des
anciennes lectures et sans parcourir toutes les pages implicitement.
Les visiteurs sans carnet disposent d'abord de la découverte. La navigation
comporte quatre entrées : Accueil, Mes participations, Mes lots, Mes communes.

Complément graphique du **31 octobre 2026** : privilégier l'image du Flyer en
pleine largeur plutôt qu'un grand panneau de texte. Limiter l'ouverture à un
titre local, une animation et des repères chiffrés avec pictogrammes et libellés.
La progression personnelle prend la forme d'un anneau chiffré, accompagné du
nombre d'étapes validées et restantes ; elle ne vaut ni qualification ni gain.
Les descriptions et conditions des cartes restent accessibles dans **En bref**,
sans être tronquées ; la fiche complète et son inscription restent accessibles.
Sans image configurée, conserver la présentation structurée sans illustration
de remplacement. Les pictogrammes d'interface restent décoratifs pour les aides
techniques ; les valeurs, libellés et noms accessibles portent l'information.

Sur l’**Accueil**, les communes suivies prennent la forme d’une seule ligne
**Choisir une commune**, avec pictogramme et nombre de communes suivies. Elle
se déplie pour afficher les noms complets et les accès individuels, puis
**Modifier mes communes**. Consulter une commune ouvre son contexte partagé
sans changer la sélection. Les dix choix restent accessibles sans défilement
horizontal, y compris avec des noms longs et du texte agrandi. Sans commune
suivie, conserver la recherche et la géolocalisation volontaire existantes.

La direction visuelle de Live est un **espace de jeu local** : navigation basse
en dock avec destination active contrastée, défi personnel sur surface sombre,
anneau et étapes restantes au premier plan, action de reprise ou de récupération
explicite. Chaque carte du programme associe le Flyer configuré, le type de jeu et les
compteurs disponibles à une action **Découvrir l’animation**. La fiche expose
ensuite l’action autorisée selon le statut et les règles du serveur. Les cartes mettent l'objectif et l'action avant
les textes détaillés. Passeport, tombola et chasse utilisent les mêmes libellés
de type dans l'accueil, le catalogue et la fiche ; seul un passeport explicite
présente un objectif public de validations. Les participations disposent de
surfaces distinctes pour lire leur progression et accéder à leur QR.

Cet habillage est limité à la surface Animation et conserve les parcours
Coffrets. La sensation de jeu repose sur les objectifs configurés et les
progressions réelles, sans points, classement, compte à rebours ni activité en
temps réel inventés. Les mouvements accompagnent l'entrée ou l'action ; le
réglage de réduction des animations les supprime. Les textes restent complets
à 200 %, les cibles tactiles et les marges de sécurité PWA sont conservées.

Le **centre de notifications** reprend la typographie, les couleurs, les
pictogrammes et les actions arrondies de Live. Les catégories et dates précèdent
le titre, l’animation éventuelle et le message complet. Les mentions **Non lue /
Lue** restent lisibles sans dépendre d’une couleur ou d’une baisse d’opacité.
Le compteur concerne uniquement les messages affichés, y compris après
pagination ; il ne prétend pas donner le total distant. La fermeture reste
accessible pendant le défilement et le dialogue est nommé dès son ouverture,
y compris depuis `/live/messages`. Chargement, absence de nouvelles, erreur et
pagination conservent leurs états explicites. Consulter le centre ne marque
aucun message comme lu et ne demande pas de permission Push ; la lecture d’un
message, le marquage des messages affichés et leurs destinations gardent les
commandes existantes. Ce composant partagé reste utilisable sur Live Coffrets.

Un parcours est « presque terminé » s'il est commencé, encore accessible et
incomplet, avec une étape restante ou une progression confirmée d'au moins 80 %.
Le nombre requis provient de l'objectif métier effectif, jamais du nombre de
commerces disponibles. « Derniers jours » signifie une échéance effective de
participation dans les 72 heures à venir, encore strictement future, avec des
étapes manquantes et une participation encore autorisée. Les deux indications
peuvent coexister sur une seule entrée. Une progression inconnue ou une erreur
de lecture ne devient pas zéro, une urgence ou une qualification.

Les priorités de la page sont triées : deux indications réunies, fin proche,
presque terminé, autres parcours ; puis échéance la plus proche et identifiant
stable. La page annonce explicitement une suite lorsqu'elle est partielle ;
aucun compteur ou classement global n'est déduit d'une page. Deux inscriptions
distinctes à une même animation gardent leurs accès et progressions distincts.
Le même identifiant de participation n'est pas présenté plusieurs fois.

**US-LIVE-RAPPELS.** En tant que participant, choisir deux rappels automatiques
indépendants, distincts des campagnes organisateur et sans quota commercial :

- **Mes parcours presque terminés** : une étape réellement restante sur un
  parcours commencé ; le seuil d'affichage de 80 % ne déclenche pas ce Push.
- **Mes animations qui se terminent bientôt** : échéance effective dans
  les 72 heures, participation encore possible, objectif incomplet.

Une participation terminée, annulée, inaccessible ou dont l'accès est révoqué
ne reçoit pas de rappel. Un parcours achevé en attente de régularisation ou
de qualification n'est pas réinterprété comme des étapes restant à jouer.
Les neutralisations et adaptations du parcours suivent les projections métier
existantes. Une qualification ou un gain reste exclusivement confirmé par le
backend ; le pourcentage ne les accorde pas.

Un seul rappel logique de chaque type par participation et installation,
avec au plus un rappel personnel par jour civil et installation. Les deux
types d'une même participation sont fusionnés ; plusieurs participations
éligibles peuvent être regroupées dans ce rappel quotidien. Aucun troisième
rappel à 24 heures n'est ajouté. La purge de la boîte de réception ne réarme
pas les rappels. Les doublons de transport éventuels réutilisent le même tag.

La préparation et l'envoi sont limités à **09 h incluses–20 h exclues, heure
de Paris**, avec gestion des changements été/hiver. Les états, préférences,
liens de suivi et échéances sont revérifiés juste avant l'envoi. Une attente
hors créneau ne prolonge pas le droit de participer ni une échéance dépassée.
Le transport peut répéter une remise après un incident réseau ; l'unicité
garantie porte sur le rappel logique et sa réservation durable.

Les préférences `RAPPEL_PRESQUE_TERMINE` et `RAPPEL_FIN_PROCHE` sont
**false par défaut**, y compris pour les installations existantes. Elles se
gèrent séparément dans Réglages ; ni l'inscription ni l'ouverture de l'accueil
ne demande la permission navigateur. Un refus de Push ne bloque pas l'accueil,
les participations ou la messagerie. Les catégories et communes antérieures
sont préservées. La préférence des campagnes organisateur reste indépendante.

### Architecture et contrats

Le domaine `animation_locale` possède la politique de priorisation et de rappel.
Il consomme la progression du moteur, ses preuves et son calendrier effectif ;
il ne dépend ni de l'ORM, ni du navigateur, ni du fournisseur Web Push.
L'application charge les faits, contrôle les accès et orchestre les transactions.
Le repository borne les lectures et écrit les réservations ; les interfaces
présentent les décisions, sans recalculer les seuils métier en JavaScript.

Lecture additive : `GET /public/localeo-live/installations/{id}/tableau-de-bord`,
avec `X-Localeo-Live-Secret` et `Cache-Control: private, no-store`. La réponse
expose `generated_at`, `items`, `count` de la page et `next_cursor`. Chaque item
contient `participation_id`, `animation_id`, `nom`, `commune:{id,nom}`, `type`,
`statut_participation`, `date_fin`, `progression:{total,validees,restantes,pourcentage}`,
`commencee`, `terminee`, `disponible`, `indicateurs:{presque_terminee,fin_proche}`
et un `deeplink`. La page est bornée à 50 participations, sans parcours exhaustif
implicite des pages ou chargement global préalable en mémoire. Seuls les suivis
autorisés de l'installation authentifiée sont consultables, même hors catalogue
public. Aucun token, e-mail, identité ou solution privée n'est exposé.

Le lien commun est `/live/animations?participation=<UUID>` : il ouvre uniquement
l'entrée locale portant cet identifiant. Un carnet absent propose la reprise
de l'accès ; aucune autre participation à la même animation n'est substituée.
Un digest de plusieurs participations ouvre Mes participations.

Les anciens suivis ne prouvent pas quel token personnel a été validé. Une
migration ajoute la référence nullable au token effectivement présenté, sans
rattachement historique heuristique. Le tableau et les rappels exigent une
capacité encore valide ; la réponse distingue les accès à actualiser par
`acces_a_actualiser` (indicateur entier 0 ou 1, sans comptage exhaustif). Depuis
le carnet local, l'action explicite **Actualiser mes participations** relie les
participations avec leurs propres tokens existants,
par lots de 50 et deux requêtes concurrentes au plus. Les échecs partiels sont
visibles. Ni nouveau token, ni inscription, ni autorisation de rappel ne sont
créés par cette opération ; un token révoqué reste refusé.

Les deux catégories sont ajoutées au contrat de préférences existant. La
configuration publique expose `rappels_participations_disponibles: true` ; un
ancien backend sans ce champ conserve ses réglages et son catalogue. Un tableau
indisponible conserve les accès du carnet et propose une actualisation, sans
simuler l'absence de participations.

La préparation utilise un traitement batch protégé, borné, simulable par défaut,
destiné à un passage toutes les 15 minutes. Un curseur durable ou explicitement
reprenable évite de retraiter indéfiniment les premières installations. Les
réservations installation/jour et participation/type sont atomiques, uniques et
indépendantes de la rétention de l'inbox. Le verrou d'installation coordonne
préférences et rappels concurrents. La notification réutilise l'outbox et les
claims de transport existants, sans nouvelle intégration fournisseur.

### Critères et preuves attendues

| Critère ajouté | Résultat observable et preuve prévue |
| --- | --- |
| E73-HOME-01 | Accueil de jeu local : priorité personnelle et action visibles d'abord sur mobile, trois priorités au maximum, puis vie des communes suivies ; visiteur sans priorité vers découverte et participation publique. Image Flyer seule, aperçu partiel explicite, accès aux périodes, type de jeu cohérent et compteurs à pictogrammes. Autres participations et pagination sur Mes participations ; navigation et anciens liens conservés. |
| E73-HOME-02 | Indicateurs calculés par le domaine, frontière 80 %, une étape, 72 h, commencement et objectif effectif ; inconnus et états terminaux exclus. |
| E73-HOME-03 | Tri explicite, absence de doublon par participation, plusieurs accès à la même animation indépendants, pagination et état partiel. |
| E73-HOME-04 | Secret d'installation, refus croisé, aucune donnée sensible et aucune réponse personnelle mise en cache ; ancien backend et erreurs explicites. |
| E73-HOME-05 | Reprise exacte depuis l'accueil ou Push, accès absent sans substitution, parcours terminés/qualification/gains conservés. |
| E73-HOME-06 | 320/390 px et bureau, clavier, cibles tactiles, texte agrandi, mouvements réduits ; aucune nouvelle permission automatique. |
| E73-ALERTE-01 | Deux préférences opt-in indépendantes, défaut false neuf/existant, retrait effectif sans altérer les autres catégories ou communes. |
| E73-ALERTE-02 | Une étape restante pour le Push, fin dans 72 h, fusion des deux types et regroupement de participations ; aucun rappel après terminaison. |
| E73-ALERTE-03 | Un type/participation/installation et un rappel/jour, deux workers concurrents, rollback, purge inbox, reprise après incident sans doublon logique. |
| E73-ALERTE-04 | Créneau Paris 09–20, été/hiver, expiration pendant attente, revalidation préférences/accès/progression juste avant transport. |
| E73-ALERTE-05 | Batch borné, simulation sans écriture/envoi, progression du curseur, fournisseur simulé ; recette réelle distincte. |

| Impact | Décision et preuve à produire |
| --- | --- |
| Backend / API / batch | Domaine pur, lecture privée, catégories additives, registre durable, refus et concurrence ; tests isolés et PostgreSQL jetable. |
| Marketplace / Live | Accueil et réglages, mêmes carnet/communes ; contrats et parcours Playwright sur API simulées. |
| ERP / Animation / Pro | Pas de nouvel écran ni de commande : les nouvelles fonctionnalités sont destinées aux habitants dans Live. |
| Données / migration | Migration additive du registre et des index, anciennes préférences sans opt-in implicite ; restauration et introspection du générateur à examiner. |
| Documentation / exploitation | Contrat canonique, guide Live, batch, cadence, limites de transport et ordre backend avant frontend à actualiser. |

Budgets locaux : page de 50 suivis maximum, aucun enrichissement HTTP personnel
par carte, deux lectures frontend concurrentes au plus, préparation de 100
installations maximum par lot et absence de transaction englobant l'envoi réseau.
Les tests vérifient les bornes, accès/index et reprises ; les mesures hébergées
de latence et de charge mixte restent une vérification d'activation distincte.
Les preuves locales exécutées et les limites de recette hébergée sont consignées
dans le [suivi d'implémentation](suivi-implementation.md), sous la référence
**E73-EVO-LIVE-ACCUEIL-RAPPELS**. Elles ne clôturent pas toute l'EPIC 73.

## Invariants, contrats et conservation

Le backend reste propriétaire de la visibilité publique, des dates et autorisations
d'inscription, des progressions, attributions, consommations et historiques.
L'interface groupe les projections existantes et n'accorde aucun droit supplémentaire.
Réutiliser `fetchPublicAnimations`, `fetchPublicAnimation`, `searchVilles`, le
formulaire d'inscription et les contrats de participation existants. Aucun nouveau
contrat OpenAPI n'est annoncé pour une association à un compte inexistante.

Le catalogue est borné : au plus dix communes suivies et deux lectures concurrentes,
pagination indépendante par commune et période, détection des curseurs répétés,
annulation des anciennes recherches et déduplication par animation. Une erreur
partielle ne devient pas un résultat complet vide. Ces bornes d'interface ne
constituent pas une mesure de capacité serveur ; avant activation, mesurer sur
1 puis 10 communes les requêtes, latences, volumes et erreurs en charge mixte.
Budget cible de navigation : interactions locales immédiates, état de chargement
visible sans attendre la dernière commune ; les résultats restent consultables
si une autre commune échoue. La tenue en charge hébergée reste à prouver.

Le carnet est en IndexedDB par origine. Un DNS ne peut pas migrer ce stockage.
Conserver `/live/reprise-carnet` sur l'ancien domaine : export privé puis import
volontaire sur le nouveau, validation et fusion transactionnelles existantes,
mêmes identifiants et capacités, sans nouvelle inscription. Aucun token ajouté à
une URL de transition. L'ancien carnet reste présent. Les anciens liens personnels
restent servis lorsque leur redirection ne peut préserver l'accès sans risque.

## Impacts et ordre de livraison de la bascule initiale

Ce tableau concerne **E73-EVO-LIVE-UNIQUE**. Le complément Accueil/Rappels
ci-dessus ajoute ensuite une migration backend, un contrat de lecture et un
traitement batch ; son ordre de livraison et ses impacts priment pour ces ajouts.

| Périmètre | Impact et vérification |
| --- | --- |
| Marketplace / Live | Routes, navigation, découverte multi-communes et sélection locale, inscription sous scope `/live/`, transition de l'ancien catalogue ; tests Node et navigateur mobile/bureau. |
| Backend / ERP / batchs | Aucun changement de règle, schéma ou commande métier prévu ; mêmes endpoints publics et privés. Les liens générés continuent à être acceptés par les routes de compatibilité. |
| Portail Animation / Pro | Aucun nouveau parcours métier ; liens publics et QR existants conservés. Les origines publiques dédiées déjà prévues restent applicables. |
| Données / migrations | Pas de migration SQL ni duplication de participation ; reprise locale du carnet explicite. Pas de synchronisation de compte ou de secret d'installation entre origines. |
| Démonstration | Réutiliser communes, animations et participations synthétiques existantes ; adapter les scénarios de navigation, sans régénérer des données réelles. |
| Exploitation | Deux services publics conservés, même API ; DNS/TLS du service Live, cache et PWA, maintien des anciens accès et reprise de carnet avant retrait de toute ancienne origine. |

Préparer le bundle et ses tests, déployer le même backend compatible et le frontend
Live sur TEST, configurer le domaine dédié et vérifier TLS. Contrôler ensuite les
douze parcours et la reprise du carnet avec un utilisateur de recette. Mettre à
jour les liens marketplace et générés après cette vérification. Ne pas retirer
l'ancien hébergement des accès personnels ni sa page de reprise du carnet.
Le repli conserve le même backend et les données ; rétablir le bundle précédent
et ses origines sans effacer de carnet. Un service worker précédent doit toujours
permettre l'ouverture des anciens accès. Commit, push et déploiement sont séparés.

## Suivi des preuves

Les résultats réels et limites sont consignés dans le
[suivi d'implémentation](suivi-implementation.md). Les 130 scénarios historiques
de [recette métier](recette-metier.md) conservent leurs statuts ; cette évolution
ajoute ses propres parcours de bascule et n'est pas validée par leurs anciens succès.

## Audit du 3 novembre 2026 — accueil recentré sur les animations

Référence **E73-UX-ACCUEIL-ALLEGE**, complément de E73-HOME-01 et de la
continuité habitant. L'audit expert porte sur l'arbre local et des parcours
navigateur synthétiques ; il ne constitue pas un test auprès d'habitants réels.

| Priorité | Obstacle | Présentation retenue |
| --- | --- | --- |
| Haute | Le grand bloc « Ça se passe à… » repousse le programme et répète la première animation | Bandeau communal compact, compteurs des périodes chargées ; une seule carte par animation, avec son Flyer réel. |
| Haute | Recherche et filtres occupent l'accueil avant toute intention de recherche | Loupe nommée dans le header, panneau ouvert volontairement, saisie focalisée ; fermeture clavier et bouton explicite vers les résultats. |
| Haute | La sélection des communes ajoute un bloc avant les animations | Une ligne dépliable avec compteur et mêmes liens, sans changer les communes suivies. |
| Moyenne | Actions secondaires aussi présentes que l'accès à l'animation | Un bouton principal par carte ; « Pour plus tard » et « Partager » en pictogrammes nommés, cibles de 44 px et état de conservation explicite. |
| Moyenne | Des filtres fermés pourraient masquer des résultats sans explication | Résumé visible des filtres actifs, accès à leur modification et effacement avec restitution du focus. |

Les participations prioritaires, gains et messages conservent leur place.
La recherche reste limitée au programme chargé : ouvrir les filtres ne relit
pas le catalogue. Les pages supplémentaires, erreurs partielles, liens directs,
retours avec filtre/position/focus et types de jeu restent couverts. Les grands
textes ne sont pas tronqués et aucune image ou activité n'est inventée.

Impacts : frontend Marketplace/Live et documentation uniquement. Aucun contrat
API, invariant métier, droit, donnée de démonstration, migration ou paramètre
d'exploitation ne change. Une mise en service nécessitera la livraison du
frontend ; les résultats locaux sont consignés dans le suivi d'implémentation.


## Correctif du 3 novembre 2026 — entrées publiques et origine Live

Les liens publics d’inscription, flyers, QR, catalogue et confirmation tombola
utilisent l’origine dédiée configurée et les chemins `/live/animations/{id}`,
`/inscription` ou `/confirmation-email` selon leur fonction. L’inscription reste
absente lorsque le backend la ferme. Aucun changement des règles d’admission,
des participations ou de leurs accès déjà émis.

Sur l’ancien service Marketplace, `/live`, `/live/decouvrir` et les fiches ou
inscriptions publiques ouvrent le domaine Live configuré. Seuls les contextes
publics autorisés (animation, commune, source) sont repris. Les confirmations avec
secret, ajouts au carnet, participations personnelles, lots et reprise de carnet
restent sur leur origine. Un carnet non vide ou inaccessible propose sa sauvegarde
avant sortie ; aucun accès n’est transmis automatiquement entre domaines.
Les pages personnelles historiques partagent désormais l’habillage et l’en-tête
Live, tout en conservant les fonctions Coffrets nécessaires sur leur origine.

Constat sur TEST, en lecture publique : le 3 novembre, le service Marketplace
configurait encore son propre domaine comme destination des animations et l’API
renvoyait des chemins relatifs `/animations/{id}`. La
[procédure de configuration](../../exploitation/technique/configurer-epic-73.md#contrôle-des-liens-live-après-bascule)
détaille la valeur à corriger sur les services concernés. Cette observation ne
constitue ni une modification de configuration distante ni un déploiement.

Rattachement aux critères E73-EVO-LIVE-06/08/09/10/12. Contrats : mêmes champs et
paramètres, destinations publiques absolues ; aucune migration SQL ni réparation
de carnet. Les exemples de déploiement et le guide d’exploitation sont mis à jour.
Les tests utilisent des données synthétiques, sans email réel ; la production des
supports de démonstration reprend le même producteur de liens.


Preuves de ce correctif, bases backend `931cef4`, Marketplace `9be43e9` et
documentation `87b6da6`, avec modifications locales :

- Backend : 4 reproductions en échec avant correction (mail de confirmation,
  publication et projections résumé/détail), puis **225 tests ciblés réussis**
  via `scripts/validation/test_isolated.py` : 110 tests des services/API et
  115 tests de transport, CORS et profils. Le détail des nouveaux cas figure dans
  `tests/application/services/test_liens_publics_animation.py`,
  `test_flyer_animation.py` et `test_catalogue_animations_publiques.py` du backend.
  Contrôles d’architecture, classes de domaine et couverture des use cases :
  **637 succès**.
- Frontend : trois reproductions navigateur échouaient avant correction
  (/live sur ancien domaine, inscription sans changement d’origine, habillage
  historique différent). Les tests de routage et conservation des accès
  (`live-entry-routing.test.cjs`, `animation-surface-satisfaction.test.cjs`) :
  **7 succès** ; ESLint des fichiers modifiés : réussi.
- Playwright avec build isolé sans `.env`, API simulées :
  `live-entry-redirects.spec.cjs` et `live-animation-surface.spec.cjs`, **18 succès** ;
  `e74-tombola-email.spec.cjs`, **12 succès**. Les parcours vérifient ouverture
  directe/actualisation, contexte public, carnet conservé/exporté/repris,
  anciens accès Coffrets et confirmation tombola. Capture mobile de l’habillage
  historique inspectée, sans débordement horizontal.
- Deux assertions historiques cherchaient encore « Mes lots » parmi les onglets
  du carnet et des onglets Animation retirés : comparaison avec
  `HEAD:src/live/LiveCarnetHeader.jsx` confirmant cette divergence déjà présente.
  Elles vérifient maintenant l’entrée dédiée dans la navigation principale,
  l’absence de doublon et les liens Coffrets conservés. Une fixture HTML de
  redirection a aussi reçu son charset UTF-8 ; assertions de destination conservées.
- Revue indépendante ciblée des producteurs et consommateurs : aucun écart
  bloquant identifié, aucune migration implicite de capacité ou d’origine.
- Vérification documentaire : 98 guides, 1 124 liens locaux, zéro erreur ou
  avertissement ; 134 sources exportées vérifiées ; `git diff --check` réussi
  dans les trois dépôts modifiés.

Aucun commit, push, déploiement, email réel ou changement distant de configuration
réalisé dans cette phase. Les variables Animation de suivi/actualités restent à
aligner selon les exemples de déploiement ; l’origine Coffrets reste indépendante.

## Correctif du 5 novembre 2026 — QR participant à l’ouverture

Suivi : [ANO-MPL-E73-LIVE-04](../../roadmap/anomalies/marketplace.md#ano-mpl-e73-live-04--qr-participant-accessible-avant-le-début).
Cette correction précise l’action personnelle des critères E73-EVO-LIVE-04/05/08/11 ;
elle ne rouvre pas l’epic et ne modifie ni inscription ni éligibilité au tirage.

**Invariant :** l’accès personnel et l’inscription peuvent être consultés avant
l’animation, mais le QR de validation commerçant ne peut être présenté hors de
sa période autorisée. Début inclus, fin exclue et état compatible sont décidés
par `Animation.autoriser_scan` ; la préparation reste contrôlée par sa politique
existante. Les routes et la PWA ne recalculent pas les dates indépendamment.

Le détail personnel expose une capacité supplémentaire :

```json
{
  "presentation_qr": {
    "disponible": false,
    "motif": "ANIMATION_NON_DEMARREE",
    "ouvre_le": "2026-11-06T08:00:00Z"
  }
}
```

`motif` vaut `ANIMATION_NON_DEMARREE`, `ANIMATION_TERMINEE`,
`ANIMATION_INDISPONIBLE` ou null ; `ouvre_le` n’est fourni que pour le début futur
effectif. Une préparation non prête ne signifie pas automatiquement « à venir ».
L’ancienne `qr_url` reste présente et ne contient pas de token, mais les routes
`/public/localeo-live/participations/{id}/qrcode` et
`/public/animation-locale/participants/{token}/qrcode` refusent désormais la
génération non autorisée. Token, inscription et historique sont conservés.

Parcours :

- Carnet, passeport, tombola locale et chasse : action désactivée **Bientôt ouvert**
  avant le début, explication et date en heure de Paris lorsqu’elle est connue.
  L’utilisateur peut consulter sa participation ; aucun appel QR anticipé.
- À l’ouverture, une actualisation relit le serveur et permet l’action habituelle.
  L’horloge du téléphone ne décide pas du droit. Sans capacité (ancien serveur),
  repli prudent sur les états publics/jeu ; `PUBLIEE` et token seuls ne suffisent pas.
- Le chargement ne montre pas l’identifiant personnel. Un refus métier/accès du
  service QR ne déclenche pas le secours par code manuel ; actualiser la fiche.
  Les erreurs techniques restent distinctes des refus de période.
- Le lien e-mail `#qr` attend une lecture personnelle courante et ne contourne pas
  le refus. Une ouverture refusée n’est pas rejouée automatiquement à l’heure de début.
- Actualisation individuelle/globale, fermeture et navigation invalident les
  réponses QR retardées. La fenêtre dépend de la capacité courante, pas de la
  copie de participation au moment du clic.

Les QR de remise des lots (Coffrets/bons numériques), QR de lieu et d’inscription
restent distincts et inchangés. La tombola publique ne propose toujours pas de
QR commerçant. Les contrôles PIN déjà présents restent conservés.

Impacts : backend, PWA Live et schéma `ParticipationLivePayload` partagé. Le champ
est ajouté aux réponses ; le serveur actuel le produit toujours et la nouvelle
PWA accepte les anciens payloads. Les schémas fermés embarqués et empreintes
Marketplace, Animation et Pro sont alignés sur ce payload ; les deux modèles QR
des vues OpenAPI documentaires 41/42 et des consommateurs sont repris des exports
hors ligne. Les divergences historiques voisines (notamment CRM) ne sont pas
absorbées par cette correction. Aucun changement de version moteur de jeu,
migration SQL, donnée de démonstration, permission ou variable d’environnement.
Les fixtures synthétiques couvrent le nouveau DTO ; pas de génération sur TEST.

| Axe | Vérification locale et limite |
| --- | --- |
| Règle et API | `test_presentation_qr_participant.py`, `test_qr_participant_periode.py`, suites participants/préparation/PIN : 71 succès ; ancien comportement reproduit avec cinq refus manquants. Deux doubles historiques complétés, assertions conservées. |
| Contrats et projections | `test_contrats_moteur_t1.py`, `test_localeo_live_backend_api.py`, `test_projections_jeu_t4.py` : 34 succès ; modèles générés, empreintes et contrôles des consommateurs ciblés. |
| Architecture | Contrôles backend architecture, classes de domaine et couverture des use cases : 660 succès. |
| Présentation | Helpers QR, transport jeu et registre Marketplace : 13 succès ; ESLint ciblé réussi. Première campagne développement : 32 scénarios réussis (parcours, navigation et lots). Après revue : 17 scénarios réussis sur build de production isolé, dont dix QR (320/1280 px, ouverture, refus période/préparation, réponse tardive, actualisation globale et anciens liens e-mail) et sept de navigation. Aucun trafic métier réel ; les campagnes se recouvrent et ne s’additionnent pas. |
| Consommateurs | Animation : quatre tests registre/contrat publication réussis ; Pro : 34 tests contrats/registre réussis. Seuls les exports fermés et OpenAPI de ce payload changent dans ces deux dépôts, pas leur UI. |
| Données et exploitation | Aucun appel réel de QR/publication sur TEST et aucun envoi externe pour ce correctif ; pas de SQL ni migration. Livrer backend et PWA, avec contrats embarqués ; les anciens accès restent valides. Aucun déploiement attesté. |

## Commerçants partenaires — accès pratique depuis Live

Complément **E73-EVO-LIVE-COMMERCANTS**, demandé le **6 novembre 2026**, lié à
ANO-MPL-E73-LIVE-05. La clôture historique de l'epic reste conservée.

L'habitant doit pouvoir choisir où se rendre sans quitter Live pour le catalogue
Coffrets. L'entrée **Commerçants** apparaît à côté du titre de l'accueil, dans la
place déjà réservée à ses commandes ; la navigation basse à quatre entrées reste
lisible sur petit écran. L'annuaire dispose des entrées **Animations / Commerçants**.
Depuis une animation classique et son parcours personnel, **Les commerçants de
l'animation** ouvre directement sa liste filtrée. Les visites d'un passeport
proposent aussi **Adresse et horaires**.

| Critère | Comportement observable |
| --- | --- |
| LM01 | L'annuaire `/live/commercants` présente les commerçants actifs d'animations publiques en cours ou à venir, avec recherche par nom et filtre de commune. Une sélection explicite d'animation peut aussi consulter ses partenaires après clôture, si elle reste publiquement visible. |
| LM02 | `/live/commercants/:id` présente d'abord l'adresse, l'itinéraire et les horaires publiés, puis les animations publiques associées ; chaque animation rejoint sa fiche Live. Les contenus éditoriaux et informations d'accessibilité restent secondaires. |
| LM03 | Une adresse ou des horaires absents sont explicitement signalés. Aucune ouverture actuelle, distance, photo de remplacement, adresse ou donnée de contact n'est inventée. Les coordonnées opérationnelles ne deviennent pas publiques. |
| LM04 | Les filtres restent dans l'URL et le retour conserve le contexte animation, parcours ou liste. Après une erreur de page suivante, les résultats déjà chargés restent visibles et le réessai reprend cette page. Une réponse obsolète ne remplace pas un filtre plus récent. |
| LM05 | Aucun lieu futur d'une chasse n'est révélé par l'annuaire ni par le filtre commerçant du catalogue. La chasse conserve le lieu courant autorisé et son itinéraire ; aucune nouvelle fiche publique d'un lieu secret n'est créée. |
| LM06 | Sur mobile 320 px et bureau, les commandes restent accessibles et sans débordement horizontal. L'accès aux commerçants ne repousse pas la première action d'animation sous la navigation basse de l'accueil. |

### Contrat et responsabilité

Deux lectures sous `/public/animation-locale` :

- `GET /commercants` : filtres `commune_id`, `animation_id`, `q` (100 caractères
  maximum), `cursor` et `page_size` (25 par défaut, 100 maximum ; Live demande 12).
  Réponse `items`, `count` de la page, `pagination.page_size`,
  `pagination.next_cursor` et `has_more`. Aucun total global déduit du nombre chargé.
- `GET /commercants/{commercant_id}` : fiche d'un commerçant actif associé à une
  animation classique publiquement visible, y compris clôturée. Refus 404 hors
  de ce périmètre ; filtres facultatifs `commune_id` et `animation_id` conservés.

Chaque ligne expose `id`, `nom`, `adresse`, `commune`, `image_url` et
`horaires_texte`. La fiche ajoute `profil_publie`, `description`, `site_web_url`,
`acces_transport` et `accessibilite`. Ces contenus sont lus uniquement dans la
version publiée du profil. Aucun numéro de téléphone public n'existe actuellement
sur ce contrat : `contact_telephone`, destiné aux opérations, n'est pas utilisé.
Les liens de site acceptent HTTP(S) uniquement, sans identifiant intégré.

`ServiceCommercantsLive` compose une projection de lecture avec les prédicats
existants de `ServiceCatalogueAnimationsPubliques` : publication, commune,
abonnement, modèle, période et associations effectives, dont retraits acceptés.
Cette lecture SQL reprend la frontière du catalogue public existant ; elle ne
porte aucune nouvelle transition ni règle de validation. La règle de passage
reste dans le domaine et les accès QR conservent leur contrôle d'ouverture.
Le partage du prédicat commerçant évite une seconde règle d'appartenance.

La recherche et les associations sont filtrées en stockage. La pagination ordonnée
nom/identifiant charge au plus `page_size + 1` lignes, avec un curseur lié aux
filtres ; un curseur invalide est refusé en 422. Les profils sont joints dans la
même requête, sans requête par commerçant ni collecte exhaustive d'animations.
Les animations de la fiche utilisent le catalogue public existant filtré par
`commercant_id`, avec sa propre pagination.

### Impacts et vérification

- Backend et Marketplace/Live : nouvelle lecture et parcours. Sources OpenAPI
  documentaires E41/E42 et copies embarquées Animation/Pro synchronisées depuis
  l'export hors ligne, uniquement pour les deux routes et cinq modèles concernés.
  Aucun changement d'interface Pro ou Animation, ni du contrat moteur de jeu.
- Sans migration : les adresses et versions publiées existent déjà. Le générateur
  de démonstration n'a pas de nouveau champ obligatoire ; les preuves utilisent
  des fixtures synthétiques. Aucun jeu ni compte TEST modifié.
- Exploitation : livrer backend et PWA ensemble ; une API ancienne produit une
  indisponibilité explicite et un réessai, jamais une liste fictive. Aucune nouvelle
  variable, permission, tâche planifiée ou notification.
- Backend : 34 tests ciblés réussis, dont six scénarios PostgreSQL/HTTP réels sur
  une base locale jetable ; 660 contrôles d'architecture réussis. Rejeu final de
  deux scénarios de curseur mal typé et parité des filtres réussi, avec recouvrement
  de la campagne précédente. Un scénario supplémentaire vérifie une seule requête
  et au plus 26 lignes pour une page de 25 sur 102 commerces ; cette mesure locale
  ne constitue pas une recette de charge. Base jetable arrêtée après vérification.
- Présentation : `live-merchants.spec.cjs`, `live-home-density.spec.cjs` et
  `live-qr-opening.spec.cjs` couvrent 22 scénarios distincts. La première intégration
  repoussait l'action de l'accueil sous la navigation ; correction vérifiée sans
  affaiblir l'assertion. Dernières exécutions : 12 scénarios parcours/QR réussis,
  puis dix scénarios annuaire/accueil réussis après compaction. Build de production
  isolé, écrans 320/390/1280 px, captures mobiles et bureau, aucun trafic métier
  réel. ESLint ciblé réussi ; les cinq modèles et deux routes exportés concordent
  avec le générateur et leurs références se résolvent. Contrats consommateurs :
  quatre tests Animation et 34 tests Pro réussis. Les campagnes antérieures se
  recouvrent et ne s'additionnent pas.
- Limite : aucun succès distant ou déploiement TEST n'est déduit des preuves locales.
