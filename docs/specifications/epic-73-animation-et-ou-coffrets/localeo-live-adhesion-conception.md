# E73 — Conception de l’adhésion habitant dans Localeo Live

## 16. Simplicité — E73-EVO-LIVE-SIMPLICITE

Conception du 11 novembre 2026 : [critères LS-01 à LS-13](localeo-live-entree-unique.md#évolution-du-11-novembre-2026--simplicité-e73-evo-live-simplicite).
Direction visuelle : un carnet personnel aéré, des objets reconnaissables et
un chemin graphique dont la progression repose sur les confirmations réelles.

Le détail tombola place nom, workflow et prochaine action autorisée avant les
accès et préférences secondaires. Il évite l'empilement ticket/qualification/
résultat décrivant plusieurs fois le même état. Les quatre étapes ont chacune
une icône et un libellé court ; une explication nécessaire tient en une phrase.
Le PIN et les préférences s'ouvrent volontairement, sans perdre les saisies ni
les garde-fous. La navigation entre onglets conserve la zone communale ; les
transitions se limitent au focus, aux états des commandes et aux dépliages,
sans déplacement décoratif et avec mouvement réduit respecté.

Le passeport réunit compteur, état et visites dans le même bloc. Les tampons
des commerces constituent sa seule collection ; la rangée synthétique répétée
est supprimée. Le QR et le lien vers l'annuaire appartiennent à ce bloc, avec
les dates confirmées disponibles dans chaque visite. La simplification ne
retire aucun commerce ni ne transforme une visite inconnue en validation.

Les précisions utilisateur cadrent les trois entrées : Carnet pour suivre les
inscriptions non archivées par l’organisateur, Lots pour retrouver les gains et leur animation,
Découvrir pour les animations actuelles/futures, les favoris et les commerces.
Précision du 11 novembre 2026 : le carnet exclut les simples suivis et les
animations archivées, sans effacer les accès enregistrés. Les animations
clôturées, annulées et celles dont le tirage est terminé restent visibles avec
leur état ; aucune date ni panne ne vaut archivage. Les coffrets déjà présents gardent
leur récupération existante. Le statut animation vient du domaine backend,
jamais du pourcentage personnel ou de l'horloge du navigateur.
`disponible` décrit la possibilité d'une nouvelle action de jeu, pas le droit
de lire le carnet. Les participations confirmées ELIGIBLE/TERMINE/GAGNANT
gardent leurs tampons et leur détail avec `disponible:false` ; aucune action de
validation n'est accordée par ce maintien. Les accès refusés/inconnus conservent
leur contrôle à l'ouverture, sans fausse progression.

La vignette expose `resultat_tirage.date_prevue`, déjà fourni par le tableau de
bord, sans lecture du détail par carte. « Tirage prévu le » précède la date et
l'heure de Paris, aussi avant qualification. Les états EN_ATTENTE et
NON_QUALIFIE sans `realise_at` autorisent cette annonce ; résultat, annulation,
date invalide ou retrait serveur la retirent. L'horloge ne transforme jamais
une annonce passée en résultat. Une projection locale est marquée « à vérifier ».
Ce complément LS-13 ne modifie ni contrat, ni règle métier, ni générateur.
Dans la vignette d'une animation, l'ordre DOM est état/date, action principale,
puis tampons : la date et l'action restent visibles sur le premier petit
viewport, et la collection conserve son espace en défilant. Les tampons du
détail et les autres catégories du carnet gardent leur composition propre.

La cloche d'une vignette ouvre `/live/messages?animation_id=…` avec retour/focus
sur cette vignette. Le compteur du tableau privé est groupé par animation et
applique les mêmes preuves d'accès que l'indicateur de messagerie. Une valeur
absente/null n'est pas un zéro. Le reçu de lecture existant précède tout
décrément ; le retour ou un reçu dans la messagerie superposée actualise le
carnet. Les droits révoqués ne laissent pas de projection privée active.

Le badge de Mes lots lit les pages privées sans créer d'installation depuis un
lien public. Il ne compte que les lots disponibles non acquittés ; une lecture
bornée/incomplète est indiquée par « + » ou un état à vérifier. Le clic explicite
« J’ai vu ce lot » écrit le repère local avant d'actualiser les autres vues et
onglets. Ouverture de liste, navigation ou dépliage n'acquittent rien. Une erreur
de stockage garde le repère Nouveau et propose de réessayer. Aucune remise,
activation de coffret ou validation QR n'est déclenchée par cet acquittement.
La fusion inclut les bons enregistrés localement, signalés comme état à
vérifier jusqu'à confirmation serveur, et les déduplique par identifiant de bon.
L'acquittement utilise une transaction IndexedDB readwrite unique, y compris
entre onglets sans Web Locks. La lecture groupée de messages émet un seul
signal d'actualisation après ses reçus confirmés, même en cas de succès partiel
transitoire. Un refus d'accès invalide les reçus encore en vol et leur signal :
un ancien succès ne peut ni effacer le refus ni rétablir un état « à jour ».
Le contexte d'installation et cette invalidation restent distincts du filtre :
un reçu confirmé pendant un changement d'animation actualise la vue courante,
sans conserver les messages ou les curseurs de pagination de l'ancienne vue.
Le menu secondaire garde « Retrouver mon carnet » vers le parcours existant.

Réutiliser `LiveActivityIcon`, les projections de jeu et le filtrage existants.
Ne pas déduire une transition métier de la position dans le workflow. Le
composant n'accorde aucun droit et masque les accès sensibles pendant une
revalidation. Les messages ciblés sont filtrés dès la lecture du contexte et
ne reprennent pas une liste mémorisée d'une autre animation. La coquille de
Découvrir demeure montée entre ses deux vues ; le contenu et ses filtres
locaux se remplacent sous les onglets. Préserver les anciennes URLs publiques.

Recette prévue : états tombola, PIN, consentement, messages ciblés, carnet sans
bandeau et onglets à 320/390 px, desktop, clavier et texte agrandi. Le bilan
sépare tests simulés, captures inspectées et recette hébergée non exécutée.

## 15. Participation — E73-EVO-LIVE-PARTICIPATION

Conception du 10 novembre 2026, avant réalisation des huit lots. Les critères
PA et leurs impacts sont définis dans la [spécification fonctionnelle](localeo-live-entree-unique.md#évolution-du-10-novembre-2026--participation-e73-evo-live-participation).
Le [bilan](verification-livraison.md#évolution--e73-evo-live-participation-10-novembre-2026)
sépare preuves prévues, exécutées et limites. Application des principes
LIVE-UX-01 à 10, sans modifier les règles de participation ou de remise.

### Lots 0 et 1 — fondation commune

Le lot 0 livre cette matrice et sa traçabilité. Le lot 1 réutilise
`LiveActivityIcon`, `LiveJourneyStamps`, le shell et les tokens existants : pas
de nouvelle bibliothèque ni d'images raster pour les pictogrammes. Corps/actions
14 px en unités relatives, champs 16 px, cibles 44 px, sections 12 px et actions
9 px. Vert `#09685e` pour agir/onglet actif, papier chaud pour le carnet, alerte
explicite pour les incidents. Les tampons compacts gardent contour/symbole/coche,
avec moins de crénelage et sans double détail décoratif à petite taille.

### Lot 2 — confirmation et continuité

`LiveApp` conserve l'identité exacte renvoyée par la sauvegarde de bibliothèque.
La confirmation reste sur une route compatible et ouvre cet objet via son
identifiant local, jamais le premier objet de la même animation. Le contexte
de retour utilise `liveReturnNavigation` (chemins autorisés, sans credential).
La confirmation mentionne que l'accès est gardé sur cet appareil, sans promettre
une synchronisation. Les anciennes listes restent accessibles. La tombola
publique confirme l'inscription indépendamment de la réception de l'e-mail ;
elle n'invente pas de token local. L'installation PWA reste secondaire.

### Lot 3 — états de reprise

`AddAnimation` et `AddCoffret` distinguent : vérification, panne transitoire,
refus/expiration, stockage local échoué, succès. Un nouvel essai est une lecture
avec les credentials déjà consommés et gardés dans une référence en mémoire.
Les réponses d'une ancienne route/un composant démonté sont ignorées ; le bouton
reste désactivé pendant l'essai. Aucun retry automatique d'inscription. Un
échec contact après lecture ne réinscrit pas et ne mélange pas deux personnes.

Précision après lecture du producteur : un code coffret `cl1.*` s'échange une
seule fois. Un échange sans réponse confirmée affiche une incertitude et propose
un nouveau lien ; aucun bouton ne rejoue cette commande comme un GET. Une fois
la session reçue, un GET passeport échoué peut être retenté avec cette session
sans rééchanger le code. La projection d'un refus est retirée et une réponse
tardive après navigation ne déclenche ni sauvegarde automatique ni redirection.

L'entrée coffret sans identifiant devient un guide, distinct d'un lien personnel
refusé. L'utilisateur retrouve le **lien personnel du coffret** dans son dernier
e-mail, importe sa sauvegarde via `/live/reglages#live-backup` ou contacte
l'émetteur. `RenvoiLienCoffret` reste limité à un UUID connu ; la réponse générique,
les limites et la non-réactivation d'un accès révoqué sont conservées. Pas de
nouvelle récupération globale par e-mail, pas de migration/configuration.

### Lot 4 — découverte et aperçu public

Le catalogue actuel ne renvoie pas le nom des lots : `lots` n'est rempli que
dans le détail. Ajouter une projection additive `apercu_dotation`, au plus trois
éléments publics par animation (nature, nom et quantité publique prévue), sans changer
`lots`, les curseurs, les filtres ou les compteurs. La projection contient
uniquement des informations déjà autorisées sur le détail public. Aucun gagnant,
prestataire privé, accès, stock interne ou prochaine étape de chasse.

Le producteur `catalogue_animations_publiques` est réutilisé par la recherche.
Les adaptateurs enrichissent seulement les IDs de la page, avec sélection bornée
en base et requêtes groupées ; aucun chargement de tous les lots puis tranche
Python, ni appel détail par carte. Les anciens clients ignorent l'ajout ; les
nouveaux acceptent un backend sans ce champ et affichent le nombre/nature connus.
Le générateur de contrat reste dans le backend, les OpenAPI canoniques dans le
projet. Après lecture du producteur, les champs retenus sont `nature`
(`COFFRET`, `LOT_EXTERNE`, `BON_NUMERIQUE`), `nom` (160 caractères au plus)
et `quantite` (quantité prévue publique, pas stock restant). Aucune image de lot
n'est actuellement publique dans ce contrat : elle n'est pas ajoutée ici.

| Coût | Borne / preuve prévue |
| --- | --- |
| Catalogue/recherche | Pagination existante conservée, 50 animations maximum ; enrichissement sur les seuls IDs de page, trois aperçus maximum par animation |
| Requêtes | Extension groupée constante par page, sans requête de dotation par animation ; comparer pages 1/10/50 et populations N/10N. Le N+1 historique de configuration de l'ancien catalogue n'est pas présenté comme résolu |
| Mémoire/payload | Au plus 150 objets d'aperçu, noms bornés ; mesurer octets et nombre de lignes hydratées. Coffrets : limiter les références avant lecture des noms |
| Accès SQL | Index existants animation/ordre à vérifier ; fenêtre/lecture latérale bornée selon adaptateur réel ; plans PostgreSQL sur cible jetable si disponible |
| Capacité | Objectif Live p95 600 ms, p99 1 200 ms, erreurs < 0,5 % à dix lecteurs concurrents ; mesures isolées et charge mixte requises avant activation, pas de garantie issue d'un test unitaire |

La carte affiche le bénéfice avant son action et conserve condition d'achat et
objectif connus. Une donnée absente n'est pas complétée par une promesse. Les
aperçus de passeport/chasse annoncent le type de parcours, sans progrès personnel
fictif. La grille s'adapte au petit nombre de résultats et les périodes vides
restent compactes. Recherche/favoris et choix volontaire de commune sont maintenus.

### Lot 5 — carnet, étapes et lots

Réutiliser la priorité calculée par le carnet ; améliorer sa hiérarchie visuelle
sans ajouter de classement ou d'urgence. La prochaine action porte l'objet et
un verbe, les autres cartes gardent leur accès. Les filtres locaux n'effectuent
pas de nouvelles lectures. L'historique et les détails restent volontaires.

L'interactivité d'une étape utilise seulement les faits autorisés retournés
par le parcours personnel : visites confirmées ou étape courante. Un tampon
d'aperçu fondé sur un nombre seul reste décoratif, non cliquable. La progression
inconnue, le gain et la qualification restent distincts. Les lots conservent
leurs contrôles de revalidation, le QR personnel et leur retour exact.

Le travail sur le détail traite aussi le constat PM-R06 connexe : masquer le
PIN pendant revalidation, retirer projection/QR/contact/PIN après 401/403/404/410,
garder une lecture ancienne explicitement non actionnable après panne temporaire,
et ignorer un résultat d'étape tardif après changement de génération de lecture.

### Lot 6 — mesure sans réactivation

Instrumentation dans les composants/projections de parcours et la politique
Analytics existante. Valeurs fermées `source_page`, `animation_type`, `stage`,
`initial_participation` (empty/present/unknown), `programme_state` (none/available/empty/unknown).
Aucune URL libre, donnée de formulaire, identifiant métier, token ni QR.
L'état initial est capturé une seule fois par visite en mémoire ; illisible ne
signifie pas nouveau. Les acquisitions ultérieures ne changent pas le dénominateur.
La présence d'un accès personnel de participation stocké est un proxy prudent
de participation existante : aucun balayage des API privées n'est ajouté pour
certifier tous les droits. Un ancien accès expiré conservé exclut donc cette
visite du groupe vide. Le taux ne mesure pas la première participation de la
personne dans l'absolu. Un retrait du consentement réinitialise la frontière de
mesure avec l'identité du transport ; les actions antérieures ne sont pas rejouées.
Une inscription est mesurée après succès serveur ; un favori, un ajout d'accès
existant ou un affichage de QR n'en est pas une. Les reçus/événements déjà vus
sont dédupliqués en mémoire et ne sont jamais transmis comme identifiants.
Le début du formulaire correspond à la première interaction, pas au montage.

Les étapes du funnel sont mesurables à l'aide d'événements autorisés ; taux
principal et limites par appareil/visite sont ceux de PA-15. Le consentement et
la suspension existants contrôlent toujours le transport. Aucune configuration
d'exploitation n'est activée par ce lot ; collecte réelle et baseline absentes
sont explicites. Les tests utilisent un transport capturé et aucun service réel.

Deux événements autorisés sont ajoutés : `live_participation_entry` puis
`live_participation_stage`. Ce dernier distingue `catalogue`, `detail`,
`form_started`, `registration_confirmed`, `access_added`, `step_confirmed` et
`reward_opened`. Les anciens événements gardent leur contrat. L'entrée ne se
répète pas pendant la même visite ; le retrait du consentement ou la sortie
de page annule les lectures métriques encore en attente. Un retour depuis
l'historique conservé du navigateur démarre une nouvelle frontière de mesure.
Une action antérieure au consentement n'est pas émise si l'acceptation arrive
pendant la lecture asynchrone de la bibliothèque.

Une commune reçue par lien partagé attend sa résolution avant la mesure du
catalogue : chargement et erreur ne signifient jamais « sans commune ». Une
lecture explicitement inconnue remplace le contexte précédent ; seules les
étapes qui ne fournissent pas d'état conservent le dernier contexte connu.
Le collecteur local importe la même politique que le navigateur, sans seconde
liste d'événements à synchroniser ni nouvel endpoint backend.

Calcul : D = nombre de visites distinctes (`client_id`, `session_id` éphémères)
avec entrée et `initial_participation=empty` ; N = sous-ensemble de D ayant
au moins un `registration_confirmed` serveur ; taux = N/D. Présent et inconnu
sont publiés séparément, jamais ajoutés à D. Les segments utilisent le premier
état de programme connu dans la visite, ou `unknown` si aucun catalogue n'a
été lu. Formulaire commencé/confirmé fournit une seconde conversion. Le clic
sur un QR, le favori et l'ajout d'un ancien accès ne comptent pas dans N.

Mesure de départ : après activation explicite distincte de cette livraison,
observer sept jours complets, publier D, N, part inconnue, couverture du
consentement et erreurs de lecture ; prolonger si le volume ne permet pas de
comparer les parcours. Aucune baseline réelle n'est disponible ici. Comparer
à période et communes comparables, sans attribuer une variation au seul design.
La mesure n'utilise aucun rattachement entre appareils ou aux participants.

### Lot 7 — recette et livraison

Réutiliser les suites de parcours et ajouter les refus pertinents ; corriger
les deux anciens sélecteurs « Choisir mes communes » sans retirer les assertions
de focus/viewport. Exécuter lint, tests Node ciblés, Playwright, build isolé,
tests backend isolés et contrôles documentaires selon les fichiers modifiés.
Les preuves restent liées à leur arbre/commit. Revue indépendante du contrat
public et des refus d'accès. Les dettes PM-R06/LA-16/LP ne sont pas closes par
une capture nominale ou un changement de palette.

Scénario humain préparé : quatre nouveaux habitants choisissent une animation,
expliquent bénéfice/effort et participent sans guidage ; deux revenants retrouvent
leur progression puis un lot. Observer réussite autonome, temps, erreurs,
compréhension de la confirmation et du retour. Cette recette n'est pas simulée
par un agent. Déploiement TEST et capacité hébergée restent distincts des commits.


**7 novembre 2026 — E73-EVO-LIVE-ADHESION.** Complément technique et recette des
[17 critères canoniques](localeo-live-entree-unique.md#évolution-du-7-novembre-2026--adhésion-habitant-e73-evo-live-adhesion),
issus des 13 recommandations du [rapport](../../audits/marketplace/localeo-live-adhesion-ux-ui-2026-11-07.md).
Les critères ne sont pas dupliqués ici. Ce document fixe les choix précédemment
laissés ouverts. Leur implémentation locale a été demandée ensuite le même jour ;
le [bilan de réalisation](verification-livraison.md) consigne les preuves effectives,
les limites et les actions d’activation. Les contrats ci-dessous ne constituent
pas une attestation de déploiement. La clôture historique E73 reste conservée.

## 1. Décisions de réalisation

| Référence | Décision | Effet sur la préparation précédente |
| --- | --- | --- |
| LA-T01 | Accueil composé à partir de fenêtres bornées existantes, avec couverture explicite. | Pas de projection de classement global ni d’historique de dernière activité. Les 50 premiers suivis ne sont pas présentés comme les plus prioritaires de toute l’installation. |
| LA-T02 | Nouvelle lecture publique `/animations/recherche`, réutilisant les prédicats du catalogue, sans total exhaustif. | L’ancienne route, son format et ses consommateurs restent compatibles. Le service de recherche existant qui calcule un total n’est pas appelé tel quel par la nouvelle route. |
| LA-T03 | Présence de messages non lus par animation, via une lecture dédiée `EXISTS`. | Pas de compteur calculé en parcourant la messagerie, ni d’utilisation du compteur global comme compteur de l’animation. |
| LA-T04 | Contact d’aide facultatif, explicitement publié par l’organisateur ; sous-ressource versionnée dédiée. | Une vraie capacité de contact public est développée, avec état vide pour les anciennes animations ; aucun contact privé n’est recyclé. |
| LA-T05 | Pour les chasses, réutilisation du lieu courant autorisé ; complément pratique personnel à la demande. | L’annuaire public continue d’exclure les chasses ; pas de divulgation de lieux futurs. |
| LA-T06 | Pas de nouveau canal ni de nouveau type de notification. | Réutiliser publication, adaptation, clôture, résultat et rappels existants. L’UI ne garantit pas la réception d’un push. |
| LA-T07 | Tous les A01–A13 sont couverts ; les options exploratoires restent distinctes. | Pas de carte interactive, récupération groupée, synchronisation de compte, filtre « famille » non qualifié, score ou partage de bilan dans cette réalisation. Ces options ne conditionnent aucun des 17 critères. |
| LA-T08 — ajustement d’implémentation | Projection technique indexée des dates effectives du catalogue en base, migration additive v304. | Les premières mesures N/10N ont montré que les sous-requêtes puis la matérialisation JSON à chaque recherche dépassaient le budget. Les dates dérivées sont synchronisées dans la transaction de leurs sources ; aucune projection globale de priorité personnelle n’est créée. |

## 2. Composition des écrans et états

### 2.1 Accueil et première valeur — A01, A04, A10

Sur mobile, ordre : header léger avec recherche/messages ; contexte communal
compact ; **une** action personnelle ; programme en cours puis à venir ; prochain
rendez-vous connu. Installer et les opérations de sauvegarde restent contextuels
et accessibles dans Réglages. Navigation basse conservée : Accueil, Mes
participations, Mes lots, Mes communes. Commerçants reste l’entrée existante.

Sources chargées une fois par ouverture/rafraîchissement, dédupliquées par les
hooks partagés : tableau de bord **50**, récompenses **25**, tirages **25**.
Les notifications réutilisent le provider existant. Aucune pagination automatique
de ces sources pour compléter un classement. Les lectures indépendantes de
l’accueil sont limitées à **3 en vol** ; celles du catalogue à **2** dans ce budget.
Un retour au premier plan peut rafraîchir les lectures si âgées de plus de 60 s,
avec une seule séquence mutualisée, jamais une commande ni un polling permanent.

Sur les candidats chargés, appliquer LA-01 dans l’ordre défini dans la
spécification fonctionnelle : combiné fin proche/presque fini, fin proche seule,
presque fini seul, nouveau lot utilisable, participation ordinaire disponible,
tirage qualifié. Un blocage métier autoritaire associé au candidat remplace son
CTA par l’explication et la reprise autorisée ; **un message URGENT ne bloque pas
un jeu**. Sans motif métier disponible, pas de blocage reconstruit par Live.
Une participation ordinaire sans progression exploitable reste consultable,
sans nombre d’étapes supposé. À égalité : échéance croissante, null à la fin,
puis type de ressource et identifiant ; pas de rang dépendant de l’ordre réseau.

Couverture partielle si une source a `incomplet`/`next_cursor`, si des accès locaux
ne sont pas liés à l’installation, ou si une source manque/échoue. Afficher
« Parmi vos suivis chargés », avec le lien vers la liste paginée concernée. Les
sources lisibles restent utiles ; aucune panne ne devient « vous n’avez aucune
participation ». Un ancien bon uniquement local est indiqué « état à vérifier »
jusqu’à lecture autorisée ; il ne prend pas la place d’un gain disponible confirmé.

« Nouveau lot » garde sa définition locale (`live-rewards-seen-v1`) : aucune
lecture inter-appareils déduite. L’affichage sur l’accueil ne marque pas le lot
consulté. Sur une installation sans suivi, ne pas créer de participation pour
personnaliser : découverte et récupération suffisent. Suivre une commune ne lie
pas automatiquement toutes les participations utilisant le même e-mail.

Carte découverte : visuel configuré ou pictogramme, titre, commune, période,
une phrase de défi, un seul indicateur et CTA « Découvrir l’animation ».
Choix de l’indicateur : lots à gagner si nombre connu et positif, sinon
participants si connu et positif ; sinon aucun. Les chiffres complets, dont
zéro, restent dans la fiche ; un total de dotation n’est jamais nommé « lots
restants ». Favori/partage demeurent secondaires, nommés/accessibles. La
promesse concrète est spécifique au moteur : un passeport peut demander des
passages ; une tombola publique demande une inscription, pas une visite.

Réutiliser tokens et composants Live : titre/page, retour contextuel, refresh,
badge d’état, carte/action, états vide/erreur et cercle de progression. Conserver
les tailles de titres actuelles ; texte utile 16 px, métadonnées au moins 14 px
dans les composants repris. Les contrôles ont une zone de 44 × 44 px minimum.
Une étiquette visible accompagne les actions métier ; loupe/refresh peuvent
rester iconographiques avec nom accessible. Le vert signifie succès confirmé,
les alertes sont réservées à une information utile. Aucune nouvelle pile CSS.

### 2.2 Inscription, carnet et installation — A02, A03

Le succès de tombola affiche « Inscription enregistrée » uniquement après la
réponse métier confirmée, puis : **1. Ouvrez l’e-mail reçu ; 2. Ajoutez votre
participation à Live**. Le lien d’aide « Je ne retrouve pas l’e-mail » ouvre la
récupération existante pour cette animation, jamais un renvoi automatique.
Une demande en cours/issue incertaine conserve sa clé et l’écran de vérification
existant. Le succès ne signifie ni livraison du mail ni adresse vérifiée.
L’écran ne stocke aucun pseudo-accès construit à partir de l’adresse déclarée.

Le guide « Retrouver mes participations sur ce téléphone » conserve trois voies :
ouvrir son lien personnel ; choisir l’animation puis demander la récupération
neutre par e-mail ; restaurer une sauvegarde. Pas de recherche publique des
participations d’une adresse. Sur sauvegarde invalide, aucune modification ;
sur import valide, fusion et rapport selon le contrat existant, sans suppression
du carnet d’origine. Un accès expiré ne donne pas lieu à une nouvelle inscription.

Après ajout effectif au carnet, proposer une fois dans le contexte courant
« Retrouvez votre parcours et vos lots en un geste » et l’installation. Un refus
ferme l’invitation et n’est pas réinterprété comme consentement à un rappel.
L’aide adapte les instructions déjà disponibles pour iOS/Android ; ouverture dans
un autre navigateur : expliquer la récupération, sans promettre une copie automatique.
Installer ne déclenche ni permission push ni copie de token vers une URL publique.

### 2.3 Jeu, commerce, réussite — A07, A11

Le retour de réussite est déclenché par la confirmation de la commande personnelle
courante, identifié par son reçu et la version de progression. Un GET initial,
un refresh ou un reçu déjà présenté ne provoque pas une nouvelle célébration.
L’état « déjà présenté » reste en mémoire de la session de jeu ; pas de journal
permanent d’accomplissements à ajouter au carnet. Durée cible 180–300 ms,
sans mouvement bloquant, son ou vibration automatique ; version statique pour
`prefers-reduced-motion`. Le message de succès est annoncé une fois par une zone
de statut, sans voler le focus au champ ou à la prochaine action.

Après confirmation : état coché, compteur serveur et CTA autorisé. Une qualification
est annoncée seulement si le moteur la confirme ; à défaut, afficher le parcours
complété avec sa situation réelle. Un conflit de version recharge la projection,
préserve la saisie autorisée et ne rejoue pas automatiquement la commande.

Pour une animation classique, « Où aller ? » utilise l’annuaire filtré existant
et conserve identifiant de participation et contexte de retour en état de
navigation, jamais son token dans l’URL. Pour une chasse, seul le lieu courant
révélé par la projection de jeu est éligible à la lecture personnelle §3.4.
Une adresse absente reste absente ; aucune distance, durée ou ouverture actuelle
n’est calculée à partir d’horaires textuels.

### 2.4 Messages, récompenses et fin — A06, A08, A09, A12, A13

Dans la participation ouverte, charger un indicateur de non-lu par animation,
pas un appel par carte de liste. « Des nouvelles de cette animation » ouvre
`/live/messages?animation_id=<id>` ; le filtre de l’URL initialise le provider,
reste dans les retours et ne crée aucun droit. Aucun compteur chiffré local
n’est affiché avec un total global. Ouvrir la liste ne marque rien comme lu ;
les gestes de lecture existants restent explicites.

Le bloc préférences affiche séparément accord organisateur, permission appareil
et deux rappels personnels. Une permission impossible ou refusée explique
comment lire dans Live ; un accord retiré conserve les effets métier et l’historique
selon le contrat existant. Les catégories marketing ne sont jamais activées par
une inscription, l’ajout au carnet ou un clic sur le guide.

Mes lots conserve disponibles avant historique, nouveaux avant déjà consultés ;
à nouveauté égale, échéance connue croissante puis attribution décroissante et
clé stable **sur la page affichée**, sans promettre un tri global des pages si
l’API ne le fournit pas. Le CTA dépend de la nature ET de l’état courant : bon
à retirer → accès au détail autorisé puis présenter ; coffret → ouvrir/activer
selon droit ; lot externe → consignes. QR absent du résumé agrégé. Lieu/échéance
manquants : mention explicite et aide, aucune extraction de droits du texte.

Tirage : date et agenda existants, mention « ne se met pas à jour automatiquement »
après export agenda ; aucune date calculée à partir de la fin de l’animation.
Notifications de résultat existantes réutilisées. Après résultat publié, proposer
au plus trois animations publiques du même périmètre de communes, hors animation
courante, via la recherche serveur ; pas de profilage ni sélection « pour vous ».
Absence de résultat : retour au programme. Une panne ne signifie pas que le
tirage n’a pas eu lieu.

Bilan : nom, état réel du parcours, étapes confirmées/total si connus, résultat,
lots accessibles et avis facultatif. Pas de comptage « commerces découverts »
déduit du nombre d’étapes. Pas de lieux futurs, pas de panorama narratif reconstruit,
pas de partage de ce bilan personnel. L’aide inscription/jeu/retrait affiche le
contact public §3.3 si présent, sinon les consignes existantes.

## 3. Contrats cibles

Les noms de routes/champs de cette section sont retenus pour l’implémentation.
Les erreurs gardent l’enveloppe commune `detail`, `code`, `correlationId` et
`request_id`. Le statut/corps d’une ancienne route n’est pas changé implicitement.

### 3.1 Capacité et recherche publique — LA-05

Étendre `GET /public/localeo-live/configuration` avec un objet additif `capacites` :
`recherche_catalogue: 1`, `indicateur_messages: 1`, `contact_public: 1`,
`lieu_courant_pratique: 1`. Absence, null ou version inconnue = capacité indisponible.
N’annoncer une version que lorsque son code ET sa readiness de schéma sont prêts.
Une panne de configuration ne devient pas une activation. Les champs existants
push/rétention restent inchangés. Aucun nouveau secret/flag opérateur nécessaire.

**GET `/public/animation-locale/animations/recherche`**, déclarée avant la route
`/{animation_id}`, ne nécessite pas de compte. Réutiliser le catalogue public
pour publication, abonnement, visibilité communale, moteur supporté et dotation.

| Entrée | Règle |
| --- | --- |
| `commune_ids` répété | 1 à 10 UUID distincts, triés pour l’empreinte. Absence ou liste vide : 422, pas d’élargissement implicite au territoire entier. Un lien communal remplace le périmètre de recherche sans modifier les communes suivies. |
| `q` | Facultatif, 120 caractères maximum après trim, normalisation de recherche existante (casse/accents) ; nom d’animation uniquement, commune via filtre dédié. Chaîne normalisée vide = sans recherche ; 1 caractère = 422 ; 2 caractères = préfixe ; dès 3 = sous-chaîne littérale. Échapper `%`, `_` et `\` avant LIKE. Libellé UI « Nom de l’animation ». |
| `modeles` répété | 0 à 4 codes connus, dédupliqués ; intersection avec `moteurs_supportes`, jamais élargissement. Code inconnu = 422 ; connu mais non supporté = aucun résultat correspondant. Aucun type n’est déduit de son titre. |
| `statut_public` | `EN_COURS` ou `A_VENIR`, facultatif : les deux. Pas de clôturées dans cette recherche de découverte ; les anciennes routes de détail restent disponibles selon leurs règles. |
| `periode` | `TOUTES` (défaut), `AUJOURDHUI`, `WEEKEND`. Fenêtre Paris résolue par le serveur, bornes UTC inclus/exclus. Chevauchement strict `debut < fin_fenetre` et `fin > debut_fenetre`. |
| `page_size`, `cursor` | 12 par défaut, 1–50 ; curseur opaque signé/versionné, 1024 caractères maximum. Pas d’offset. `moteurs_supportes` reprend le contrat existant. |

Réponse 200 : `items` (DTO public existant), `count` (page), `page_size`,
`next_cursor`, `has_more`, `as_of` et `periode_resolue` (null pour TOUTES, sinon
`{debut, fin, fuseau: "Europe/Paris"}`). Pas de `total` exhaustif. Une page vide
est légitime ; `next_cursor` est null lorsqu’il n’y a plus de résultat.
L’adaptateur Live dédié conserve ce format, sans alimenter un normaliseur ancien
qui attendrait un total. Les autres usages de `fetchPublicAnimations` sont conservés.

Ordre total : rang EN_COURS puis A_VENIR évalué à `as_of`, date de début effective,
UUID croissants. Le curseur contient dernier triplet, `as_of`, fenêtre résolue,
empreinte des filtres normalisés/capacités et version. Les dates de classement
sont figées pendant la navigation, mais publication/accès/visibilité/échéance
sont revalidés au moment de chaque lecture. Navigation vivante : une modification
peut déplacer une ligne ; dédupliquer par ID les pages affichées et proposer
actualisation. Ne pas présenter le résultat comme un instantané d’export.

Curseur altéré, mal formé ou lié à d’autres filtres : 422 `CURSEUR_INVALIDE`.
Version différente ou âge > 30 minutes : 409 `RECHERCHE_A_RECOMMENCER` ; conserver
les filtres et demander explicitement de recharger la première page. Date fenêtre
ancienne conservée dans le libellé jusqu’au rechargement. Indisponibilité : 503
selon l’erreur de catalogue existante ; surcharge : 429 avec `Retry-After`, sans
requêtes répétées en boucle. Réponse publique sans donnée personnelle, cache HTTP
`no-store` pour éviter une ancienne visibilité servie après retrait.

Implémentation SQL : nouvelle méthode de page sans COUNT, réutilisant
`_requete_base`/`_requete_visible`, sélection `limit + 1`, enrichissement groupé
de cette page. Réutiliser `nom_recherche` et les index B-tree/trigrammes de v276,
pas le `nom ILIKE` non normalisé du chemin historique. Aucun nouveau moteur de
recherche. Tester plans sur dates effectives/surcharges et filtres communaux ;
si un index additionnel est nécessaire, l’ajouter par migration vérifiée.

**Ajustement LA-T08 après mesures** : conserver en base les dates effectives
déjà définies par la configuration publiée et les surcharges d’exploitation,
dans `animation_plannings_catalogue_live`, avec index adaptés à la commune,
aux dates et au tri stable. La migration additive
`v304_projection_planning_catalogue_live.sql` et ses triggers
répercutent uniquement les modifications des sources de ces
dates dans la même transaction ; une inscription ou un compteur ne relance pas
ce calcul. Le domaine conserve la décision métier et la visibilité reste contrôlée
par les mêmes prédicats, avant la limite. Tester la parité avec la lecture
historique, les révisions non publiées, la suppression d’une surcharge, les
transitions et les modifications concurrentes. La capacité de nouvelle recherche
reste indisponible tant que table, index et synchronisation attendus manquent.
Les anciennes lectures gardent leur voie compatible sur un schéma non migré.

UI : recherche temporisée 300 ms, annulation de la précédente ; une page 12
en cours et une page 12 à venir au démarrage, filtre période conservé. Cache
mémoire de **5 contextes**, **5 pages de 12 par période**, plafond **120 cartes**
par contexte ; éviction LRU. Au-delà, navigation par fenêtres précédent/suivant
avec curseurs, pas accumulation illimitée. Retour depuis une fiche retrouve
filtre, fenêtre et focus ; fenêtre évincée rechargée explicitement sans traverser
toutes les pages. URL encode uniquement filtres publics ; aucun token.

### 3.2 Indicateur de messages — LA-06

**GET `/public/localeo-live/installations/{id}/messages/indicateur?animation_id=<UUID>`**.
Authentification `X-Localeo-Live-Secret` et installation active, comme la liste
existante ; un paramètre animation ne prouve jamais une participation. Réponse
200 `{animation_id, has_unread: boolean, generated_at}`. Vérifier d’abord un suivi
personnel valide vers cette animation ; sinon retourner false. Ensuite, `EXISTS`
sur messages personnels et notifications autorisés liés à l’animation, avec les
prédicats d’accès courant, expiration et preuve de chaque branche du repository.
Cette garde supplémentaire concerne uniquement cet indicateur de participation :
elle ne retire pas les notifications générales de la messagerie historique.
Sans élément autorisé : false sans révéler une inscription extérieure. Installation
invalide : même refus que les routes Live actuelles. Valeur mal formée : 422.

Un seul appel par détail ouvert, annulé à la navigation. Pas de liste libre d’IDs
ni de boucle par carte. La route actuelle `messages?limit=1` n’est pas un substitut :
elle calcule encore un compteur global. Aucun acquittement sur ce GET, pas de
cache public, en-têtes privés `no-store`. Révocation du suivi ou de son accès
prise en compte immédiatement ; pas de capacité accordée par le booléen.

### 3.3 Contact public d’aide — LA-12

Nouveau concept optionnel du domaine Animation : `ContactPublicAnimation`,
lié à une animation, versionné indépendamment de la configuration du jeu.
Objet-valeur avec `libelle` (1–80 caractères si activé), `email` (nullable,
validation existante, max 254), `telephone` (nullable, format international
normalisé, 8–15 chiffres après `+`), `publie` (bool), `version` (entier).
Au moins un canal si publié ; rejeter CR/LF et caractères de contrôle dans les
canaux et le libellé ; pas de HTML, URL libre, pièce jointe ou contact
repris automatiquement d’un utilisateur. Rendu échappé ; `mailto:`/`tel:` sont
construits à partir de valeurs validées, pas fournis par le client.

**GET/PUT `/protected/animation-locale/animations/{id}/contact-public`**,
permission `LIRE` pour GET, `MODIFIER` pour PUT et contrôle partenaire/commune
comme le planning de tirage, avec refus de PUT en mode consultation. GET retourne
l’état administrable avec `animation_id`, `modifiable`, `motif_indisponibilite` ;
absence persistée = `publie:false`, canaux null, version 0.
PUT reçoit les quatre champs éditables plus `expected_version` et l’en-tête
d’idempotence selon `ServiceCommandesIdempotentesAnimation`.

Voie ERP : **GET/PUT `/internal/animation-locale/animations/{id}/contact-public`**,
avec `contexte_generation`, `factory_animation_autorisee`, contrôle du périmètre
et interdiction d’écriture en mode consultation. GET exige
`animation:exploitation_lire`. PUT exige la nouvelle permission métier
`animation:contact_public_modifier`, ajoutée à `PERMISSIONS_MOTEUR` et
`PERMISSIONS_ERP_BACKOFFICE`, jamais à `PERMISSIONS_ERP_EXPLOITATION`.
Le rôle EXPLOITATION garde la lecture seule ; ne pas supposer que le contexte
ERP accorde déjà `animation:modifier`. Les deux voies utilisent le même service,
les mêmes versions, commandes idempotentes et règles de publication.

Publication explicite depuis Animation, section informations pratiques/aide :
aperçu des coordonnées, mention « Visible par les habitants », validation
volontaire. L’enregistrement de coordonnées seules ne coche jamais Publier.
ERP passe par le même use case. Statuts BROUILLON, CONFIGUREE, PUBLIEE, EN_COURS,
CLOTUREE ou ANNULEE : modification autorisée au gestionnaire habilité ; ARCHIVEE :
seule dépublication/effacement autorisés. Pas de quota, paiement, republication
de moteur ou notification automatique liés à ce contact.

Transaction : session et droits revalidés, verrou animation puis contact,
comparaison de version, modification de domaine, audit et reçu idempotent dans
le même commit. Première création : version attendue 0, contrainte unique sur
animation. Même clé/corps = même résultat, clé réutilisée avec autre corps ou
version périmée = 409, respectivement `IDEMPOTENCY_CONFLICT` et `VERSION_OBSOLETE`,
sans les fusionner dans le client. Rejeu n’écrase pas une version plus récente ;
réautoriser aussi avant restitution d’un reçu existant, pas seulement avant
mutation. 422 données invalides ; refus de périmètre sans fuite.

**GET `/public/animation-locale/animations/{id}/contact-public`** : autoriser
uniquement une animation accessible via le catalogue/détail public ; 404 sinon.
200 `{contact:null}` si non publié, sinon
`{contact:{libelle,email,telephone}, version}` ; aucun champ interne/auteur.
Pour une participation personnelle encore consultable après retrait du catalogue,
la lecture §3.4 possède une variante contact avec son propre contrôle participant.
Après dépublication, résultat null dès la prochaine lecture ; `no-store` sur ces
réponses et exclusion SW. Ne pas prétendre pouvoir effacer une coordonnée que
quelqu’un a déjà copiée.

Persistance additive : table `animation_contacts_publics`, PK/FK `animation_id`,
libellé, email, téléphone nullable, publié false par défaut, version >= 1,
dates création/modification. Absence de ligne signifie version 0 ; CHECK au
moins un canal valide/non vide si publié, index PK suffisant. FK de suppression
cohérente avec suppression autorisée de l’animation ; pas de suppression d’un
participant en cascade. Aucun backfill des contacts privés. Audit auteur/action/
version/champs changés, sans copie des coordonnées dans les logs HTTP.

### 3.4 Pratique personnelle — LA-11/12

Sous le préfixe personnel déjà utilisé par le jeu, nouvelles lectures :
**GET `/public/localeo-live/participations/{participation_id}/lieu-courant/pratique`**
et **GET `/public/localeo-live/participations/{participation_id}/contact-public`**.
Authentification Bearer du participant, mêmes contrôles et protections de
journalisation que `jeu_animation_api.py`. Aucun token dans l’URL. Au montage,
le client utilise l’accès déjà détenu, pas une recherche de token par e-mail.
Le paramètre existant `inclure_contact` expose l’e-mail personnel du participant :
il ne doit jamais être réutilisé pour le contact de l’organisateur.

La lecture de lieu ne prend **aucun identifiant de lieu demandé par le client**.
L’application récupère la projection de jeu courante autorisée puis sa référence
de lieu courant. Moteur incompatible : refus existant ; aucun lieu courant
révélé : 200 avec `lieu:null`. L’enveloppe commune est
`{lieu, definition_version, progression_version, exploitation_revision, step_id}` :
les trois versions sont les entiers de la projection autorisée, `step_id` est
l’identifiant de son étape courante ou null en l’absence d’étape. Le lieu renseigné
contient `{nom,adresse,horaires_texte,site_web_url}`, champs inconnus null.
Nom/adresse issus du lieu publié autorisé ;
horaires/site seulement si référence à un commerce et profil public effectivement
publié. Aucun enrichissement d’un lieu futur ou d’un profil privé. Un changement
de l’une des trois versions ou de l’étape rend la réponse précédente obsolète
côté client. Comparer aussi le contexte de participation actif avant affichage ;
rejeter une réponse tardive après progression, neutralisation ou changement de
participation. Nouvel affichage après lecture courante, aucun changement de
progression dans ce GET.

La lecture de contact vérifie la participation courante puis l’animation associée,
sans paramètre permettant de viser une autre animation ; même enveloppe publique
du §3.3. L’accès révoqué/expiré est refusé suivant la politique existante, pas
contourné par le fait d’avoir conservé une ancienne URL. Les deux réponses sont
privées, `no-store`, exclues de l’IndexedDB, des exports de carnet et du SW.

## 4. Mesure, données et compatibilité

### 4.1 Analytics — LA-17

L’analytics reste soumis au flag, à la disponibilité du transport et au consentement
existants ; la suspension actuelle n’est pas levée. Instrumentation préparée,
sans activer de collecte. Réutiliser la politique fermée ; ajouts cibles :
`live_next_action_opened`, `live_registration_success_viewed`,
`live_recovery_guide_opened`, `live_step_success_viewed`, `live_reward_action_opened`.
Attributs autorisés uniquement : `action_kind` parmi `REPRENDRE`, `RECUPERER`,
`CONSULTER_LOT`, `CONSULTER_TIRAGE`, `LIRE_MESSAGE`, `VOIR_LIEU`, `CONTACTER` ;
`source_page` parmi `live_home`, `live_animation_list`, `live_detail`, `live_lots`,
`live_messages`, `live_settings`, `live_registration` ; `animation_type` parmi
les quatre moteurs pris en charge ; `outcome` parmi `SUCCES`, `INDISPONIBLE`.
Ces valeurs sont autorisées dans les nouveaux schémas d’événement uniquement,
dans `analyticsPolicy.mjs` partagée avec le transport. Ne pas élargir une constante
globale utilisée par les anciens événements ni leurs attributs autorisés.
Zéro URL libre, query string, e-mail, UUID de participation/animation, token,
QR, contact, commune précise ou saisie de recherche. Compter l’ajout au carnet
avec un nouvel événement fermé `live_library_access_added` (pas d’événement
équivalent dans la liste actuelle) ; ne pas doubler `animation_registration_succeeded`
pour une simple vue de l’écran de réussite.

Documenter les dénominateurs : affichages de réussite et ouvertures d’action,
pas personnes uniques. La participation réelle reste confirmée par le backend,
pas par un événement de clic. Aucun taux de rétention inter-appareils annoncé.
Le dispositif utilise une identité éphémère en mémoire : le retour habitant à
7 jours n’est pas mesurable par cette instrumentation. Il reste un suivi
qualitatif distinct et n’impose aucun identifiant persistant nouveau.

### 4.2 Migrations, lecteurs et démonstration

Migration additive **v303_contact_public_animation.sql** pour
`animation_contacts_publics`, puis **v304** pour la projection technique des
dates et ses index, sans modifier une SQL déjà appliquée. Pas de migration des
participations, lots, préférences ou carnet.
Moteur et `ParticipationLivePayload` inchangés grâce aux lectures dédiées ; si
l’implémentation souhaite les étendre, cela exige une révision de cette conception
et l’alignement de toutes les copies fermées, pas un champ ajouté silencieusement.

Producteurs : backend/API/domaine/adaptateurs ; consommateurs : Marketplace/Live
et Animation pour la saisie du contact, ERP pour le même acte administrateur.
Pro ne reçoit pas de nouvelle fonction ; non-régression QR/PIN et contrats partagés.
OpenAPI documentaires E41/E42 générés hors ligne dans le projet après ajout des
routes ; copies embarquées synchronisées uniquement sur les composants affectés.
La prose cible ne remplace pas les schémas runtime futurs.

Générateur : champ facultatif n’invalide pas les anciens scénarios ; ajouter
fixtures contact publié/non publié/sans canal, permissions et restauration de
la table. La démonstration pédagogique peut ajouter un contact fictif réservé
à ses données synthétiques. Aucun compte réel, e-mail ou domaine opérateur réutilisé.
Adapter inventaire de sauvegarde/restauration et ordre des FK, puis tester dump/
restore isolé de cette table ; aucune génération ou migration sur TEST implicite.

### 4.3 Coexistence et exploitation

1. Backend et migration additive : readiness contrôle table/colonnes/contraintes
   et routes, ainsi que la projection/index/synchronisation de dates v304 ;
   capacité de chaque lecture annoncée seulement si prête.
2. Animation/ERP : formulaire de contact selon capacité ; l’absence de contact
   ne bloque ni préparation ni publication d’une animation.
3. Live : détection de capacités ; ancien serveur → parcours existant et filtre
   local explicitement limité, nouveaux filtres masqués avec explication. Ne pas
   ignorer un filtre serveur demandé par l’utilisateur.
4. Contrôle après livraison : recherches, retours, carnet historique, contact
   retiré et absence de fuite ; pas de publication d’animation ni envoi requis.

Pas de job ni secret supplémentaire. Retrait de la nouvelle UI possible sans
effacement de carnet ; rollback applicatif garde la table additive. Dépublier
un contact reste possible dans le backend livré ; ne pas supprimer la table
comme procédure automatique de retour arrière. Diagnostiquer par code/corrélation,
version de capacité et compteur technique, jamais par copie d’un accès personnel.

## 5. Budgets et preuves de performance — LA-16

**Objectifs de recette, pas mesures acquises.** Référence de test isolée : API
2 vCPU/4 Gio, PostgreSQL 2 vCPU/4 Gio, même réseau local, pool borné à 10 ; déclarer
versions et index. Si cet environnement n’est pas disponible, rapporter la limite
et un profil équivalent documenté avant mesure, pas relever les seuils après échec.

| Chemin | Budget d’acceptation |
| --- | --- |
| Recherche page 12/50, filtre courant/rare/vide | p95 ≤ 500 ms, p99 ≤ 1 s à 10 lecteurs ; ≤ 10 requêtes SQL par page indépendamment de 12/50 ; ≤ page_size+1 animations hydratées, aucune collection globale. |
| Indicateur messages | p95 ≤ 200 ms, p99 ≤ 500 ms ; ≤ 4 requêtes incluant authentification ; EXISTS indexé, aucun COUNT exhaustif. |
| Contact public/personnel | p95 ≤ 250 ms, p99 ≤ 600 ms ; ≤ 6 requêtes hors lecture moteur nécessaire pour le lieu courant ; contact indexé par animation. |
| Lieu courant | p95 ≤ 500 ms, p99 ≤ 1 s ; un seul parcours personnel chargé, aucun chargement des projections des autres participants. Réutiliser les limites de la lecture jeu existante. |
| Mémoire | Surcoût API ≤ 10 Mio pour recherche page 50 entre repos et requête ; pas de croissance proportionnelle à N. Frontend ≤ 120 cartes DOM par contexte ; cache borné selon §3.1. |
| UX sur réponses simulées stables | Affichage d’attente dès le début, maintien de géométrie/focus ; action principale visible sans scroll à 390 × 844 et atteignable sans masquage à 320 × 568, y compris avec données personnelles denses. |

N : 1 000 animations, 10 000 participations, 50 000 messages ; 10N : dix fois
chaque volume. Faire croître séparément la commune/installation consultée et
les données étrangères. Fenêtre de 50 suivis testée aussi sur une installation
avec plus de 50 suivis ; cela doit produire une couverture partielle, pas un scan.
Mesurer premières et pages profondes, mots de deux/trois caractères, variantes
accentuées, changement de date Paris, filtres sans résultat et migrations à froid.

Trafic : 1 puis 10 lecteurs sur 5 minutes après stabilisation, puis 10 lectures
avec 2 écritures par seconde (inscription/validation alternées) et traitement
de notification simulé. Mesurer erreurs, p50/p95/p99, CPU, mémoire, pool, verrous,
buffers et lignes parcourues. Aucune erreur 500 ni doublon métier ; les écritures
respectent leurs budgets existants et leur p95 ne régresse pas de plus de 20 %
par rapport au même jeu sans les nouvelles lectures. Paliers de saturation
20/40 concurrents : refus borné documenté (429/503), retour au régime nominal
après 60 s, aucune file mémoire croissante. Pas de test de charge sur TEST partagé.

Les index nominaux de v276 ne constituent pas une preuve suffisante. Enregistrer
EXPLAIN ANALYZE BUFFERS, statistiques, répétitions à froid/chaud et plans des
prédicats de visibilité. Une page dont le coût croît linéairement avec les données
étrangères impose une correction ; pas de seuil relevé a posteriori. Les chemins
personnels gardent authentification/révocation même si leur budget est dépassé.

## 6. Recette traçable et condition de fin

Chaque ligne complète la matrice fonctionnelle existante. Les noms de nouveaux
tests ci-dessous sont ceux proposés à la conception. L’implémentation regroupe
certains scénarios dans les suites existantes : les chemins réellement exécutés,
leurs résultats et les limites figurent dans le
[bilan de réalisation locale](verification-livraison.md#réalisation-locale-de-lévolution).
Cette matrice de recette ne constitue pas un résultat de test.

| Scénarios | Critères | Preuves attendues |
| --- | --- | --- |
| LA-T01 accueil ordinaire/urgent/lot/tirage ; 51 suivis ; source en panne ; ancien bon local ; deux inscriptions même animation | 01, 08, 09, 15 | Node helpers + Playwright `live-adhesion-home.spec.cjs` ; absence de fetch exhaustif, couverture partielle exacte, aucun accès emprunté. |
| Tombola QR et Live, réponse en cours/perdue, même clé, adresse préexistante, absence d’e-mail reçu ; guide lien/import/appareil | 02, 03, 15 | Suites E74 existantes + `live-adhesion-continuity.spec.cjs` ; aucune chance/mail supplémentaire ; reprise sans effacement. |
| Catalogue complet, accent/casse/LIKE littéral, 10 communes, 50+1, minuit/DST, cursor altéré/expiré, visibilité retirée entre pages | 04, 05, 16 | Tests API/PostgreSQL `test_recherche_animations_live.py`, contrat OpenAPI et Playwright `live-adhesion-discovery.spec.cjs`. Plans et charge §5. |
| Non-lu d’une autre animation/installation, suivi révoqué avec notification historique restante (indicateur false, historique conservé), affichage sans acquittement, URL filtrée, push refusé | 06, 15, 16 | `test_indicateur_messages_live.py`, régression messages + `live-adhesion-messages.spec.cjs`. |
| Étape confirmée vs incorrecte vs reçu en cours, reçu répété, version ancienne, 100 % non qualifié, mouvement réduit | 07, 14, 15 | Régression domaine moteur + Playwright `live-adhesion-game.spec.cjs`, aucune célébration fictive. |
| Bon révoqué/consommé, lot externe sans date, coffret à activer, tirage absent/perdant/gagnant, bilan sans total | 08, 09, 13 | Suites lots/tirages existantes + `live-adhesion-rewards.spec.cjs`. |
| Contact publié/non publié, 0→1 concurrent, version périmée, rejeu clé/corps, droit révoqué avant mutation ou reçu, hors commune, archive ; ERP BACKOFFICE autorisé vs EXPLOITATION interdit ; coordonnées interdites | 12 | Domaine `test_contact_public_animation.py`, orchestration/HTTP/PostgreSQL ; absence de fuite publique/audit ; formulaire Animation et ERP. |
| Lieu courant/futur, réponse tardive après changement de participation/étape ou de chaque révision, profil commerce privé, pas d’adresse, mauvais token, contact sur animation retirée | 11, 12, 15 | `test_pratique_participation_live.py`, consommateurs Live, invariants chasse/QR/PIN préservés. |
| Toutes pages aux trois formats, texte 200 %, clavier ouvert, focus/retour, contraste et noms accessibles ; aucun scroll horizontal | 10, 14 | Playwright et calculs de contraste sur rendu ; parcours clavier et arbre d’accessibilité automatisés. Lecteur d’écran/appareils physiques consignés séparément avant activation. |
| Consentement refusé, transport inactif, attribut non autorisé, pas de donnée dans URLs/events, absence de sync implicite | 17 | Tests policy/transport analytics et stockage existants étendus ; aucun fournisseur réel. |
| Ancien client/nouveau backend, nouveau client/ancienne capacité, dump/restore contact et migration rejouée | Tous selon impact | Tests contrats, readiness, migration et restauration isolée ; inventaire démonstration actualisé. |

Commandes prévues : runner backend `scripts/validation/test_isolated.py` pour
domaine/application/adaptateurs et contrôles d’architecture ; suites Node de
sécurité Marketplace et Playwright via son serveur isolé ; suites API/UI du
portail Animation selon son guide local. Exécuter les fichiers effectivement
créés et les non-régressions touchées, avec sorties enregistrées dans le
[bilan E73](verification-livraison.md). Les noms proposés ne doivent pas être
présentés comme des fichiers existants avant implémentation.

Fin de l’évolution : critères 01–17 vérifiés sur l’arbre livré, contrats et
consommateurs alignés, migration/readiness et bornes mesurées, aucun échec ou skip
converti en succès. Le pilote habitant et la mesure de rétention sont un suivi
produit ; ils ne bloquent pas la clôture technique demandée par E73-DEC-CLOTURE-TESTS.
La disponibilité TEST, les capacités d’installation iOS/Android et les livraisons
mail/push réelles ne sont pas déduites des tests simulés.

## 7. Hiérarchie et fluidité — E73-EVO-LIVE-HIERARCHIE

**8 novembre 2026 : conception puis réalisation locale** ; preuves et limites
au [bilan E73](verification-livraison.md). Les critères canoniques sont
[LH-01 à LH-12](localeo-live-entree-unique.md#évolution-du-8-novembre-2026--hiérarchie-et-fluidité-e73-evo-live-hierarchie).
Ce complément applique les huit recommandations de l’audit après déploiement.
Il précise la composition du §2.1 et la stabilité visuelle du §5 sans modifier
les budgets API, droits ou preuves historiques. Le tableau de fin du §6 concerne
LA-01 à LA-17 ; la présente évolution exige ses propres preuves.

### 7.1 Architecture et responsabilité

Réutiliser `LiveHome`, `LiveDiscovery`, `LiveCommunityScene`, `LiveExploreNav`,
`LiveMerchants`, `LiveRefreshButton`, les hooks dashboard/rewards et les helpers
de navigation. Le contexte communal de découverte doit pouvoir être affiché
avant l’action personnelle ; son déplacement ne monte pas une seconde instance
du catalogue. Un propriétaire unique des filtres et des lectures alimente la
composition. La scène communautaire est simplifiée ou absorbée ; ses compteurs
et états de couverture restent disponibles sans reproduire le même en-tête.

Pas de nouvelle entité, table, commande ou projection backend. Les domaines
Animation, participations et gains gardent leurs règles ; Live ne déduit aucun
droit du maintien visuel d’une lecture. Le §3 conserve les producteurs, contrats
et capacités existants. Ni OpenAPI documentaire ni contrat embarqué ne change.
Les adaptations de la gestion de chargement restent dans les hooks/services,
sans dupliquer les règles métier dans les cartes ou routes.

### 7.2 Composition et langage graphique

- Header compact conservant identité, recherche et messages. Installer reste
  contextuel ; Réglages reste accessible. Actualiser reste iconographique, nommé,
  sur la ligne de titre et ne crée pas une ligne textuelle supplémentaire.
  Sur l’accueil, **Mon Live et Actualiser sont dans l’en-tête de l’application,
  sur une seule ligne** ; le titre n’est pas répété dans le contenu. Jusqu’à
  720 px, logo compact, titre, actualisation, recherche et menu restent visibles.
  Le menu regroupe notifications (avec indicateur non-lu), réglages,
  installation et retour aux coffrets lorsqu’il est applicable.
- Contexte communal sur une ligne adaptable : un nom, ou les deux premiers noms
  puis le nombre supplémentaire ; la commande ouvre le sélecteur existant avec
  la liste complète. À zéro commune, une invitation courte et une action Choisir
  mes communes ; ni sections vides artificielles ni compteur zéro prématuré.
- Une action personnelle au plus, issue de `nextLiveAction` sans nouvel ordre
  métier. Lorsqu’elle manque réellement, pas de réservation permanente. Pendant
  sa première lecture, une zone compacte bornée ; après la réponse, son insertion
  est évaluée dans la mesure de stabilité et ne vole pas le focus.
- `LiveExploreNav` devient une navigation de liens Animations / Commerçants,
  `aria-current="page"`, mêmes dimensions et emplacement relatif sur les deux
  vues ; aucun faux widget d’onglets ARIA sans gestion correspondante du clavier.
- Titres de périodes accompagnés d’icônes distinctes (activité/calendrier), d’un
  accent chaud pour le présent et d’un traitement bleu/encre pour le futur.
  Conserver le vert pour les succès confirmés. Aucun état dépend de la couleur
  seule. Les raccourcis de période s’intègrent à la découverte sans gros résumé.
- Cartes : ordre LH-07, un CTA principal, une métrique maximum ; favoris/partage
  en actions secondaires de 44 × 44 px avec nom accessible. Texte principal
  16 px, métadonnées 14 px minimum sur les composants repris, titres aux tailles
  Live existantes. Une à trois colonnes suivant largeur, jamais de texte utile
  réduit pour forcer l’objectif du premier écran. Les cartes sans photo restent
  compactes ; aucune réservation de hauteur d’image si aucune URL n’est connue.
- Flyer connu : ratio réservé avant décodage ; en erreur, pictogramme sobre
  dans cette zone pour éviter un saut pendant la lecture. Au prochain montage,
  un état d’absence établi peut adopter la variante compacte. Les exemples de
  typographie, accents, séparateurs et icônes utilisent les tokens existants ;
  retirer les règles contradictoires à leur source, pas de seconde feuille de
  surcharges globale.
- Annuaire et accueil partagent gouttières et largeur de cadre ; la fiche
  commerçant peut limiter les paragraphes à une largeur lisible à l’intérieur.
  La navigation fixe réserve son espace bas, y compris safe-area mobile et zoom.

### 7.3 Modèle d’état des lectures

État de présentation proposé : clé de contexte, données de la dernière réussite,
date de réussite, requête en cours/génération et erreur. Ce modèle n’est ni un
nouveau contrat réseau ni un objet métier. Le simple compteur de rafraîchissement
ne fait pas partie de l’identité du contexte.

| Situation | Affichage | Transition/refus |
| --- | --- | --- |
| Aucun contexte communal | Choix des communes | Pas d’appel catalogue sans sélection. |
| Première lecture du contexte, sans résultat connu | Titre stable, ossature de deux cartes au plus et une annonce par zone | Les placeholders sont ignorés par l’arbre d’accessibilité et non cliquables ; `aria-busy` sur la zone. |
| Réussite | Données, date de réussite, portée exacte | Seule une réponse réussie et vide produit un état vide. |
| Revalidation du même contexte | Données précédentes, indicateur local réservé dans l’en-tête, annonce unique | Ne pas vider les listes ; remplacer la page en un seul commit d’état. Aucun déplacement de focus. |
| Échec réseau avec données précédentes | Dernière lecture explicitement datée et Réessayer | Ne pas modifier sa date ; zone déclarée périmée, pas de statut métier confirmé depuis cette copie. |
| Échec sans données | Erreur locale et Réessayer | Les autres sources restent affichées ; pas de boucle automatique. |
| Changement de contexte | Structure conservée ; anciennes données non présentées comme nouvelles | Annuler/ignorer l’ancienne génération, réinitialiser les curseurs du contexte remplacé. |
| 401/403/404/410 ou révocation explicite d’une ressource privée | Retirer immédiatement la copie privée et proposer la reprise autorisée | Pas de stale privé sur refus d’accès ; ne pas effacer le carnet historique par une simple panne réseau. |

Clé de contexte publique : ensemble trié de communes, période, recherche
normalisée, type, filtre de dates et version/capacité serveur. Clé de contexte
annuaire : commune éventuelle, animation éventuelle et recherche. La clé de page
ajoute à ce contexte le curseur de départ ; le curseur ne change pas à lui seul
le contexte de filtres. Clé personnelle :
installation, ressource/participation et génération locale d’accès, sans inclure
de secret dans les logs ou URL. Changement/suppression des accès invalide toutes
les lectures privées concernées ; données privées conservées uniquement en
mémoire de la vue autorisée, pas en cache module partagé ni stockage supplémentaire.

Pendant une revalidation personnelle, un lien vers une fiche reste possible
avec vérification courante à l’arrivée. Les QR, PIN, retraits, qualification et
actions de gain ne sont jamais réactivés depuis la copie ; chaque action conserve
les contrôles autoritaires existants. Une erreur privée ne masque pas le programme
public. Une erreur du programme ne devient pas « aucune animation ».

Mutualiser une séquence en cours entre focus, visibilitychange et clic refresh.
Avant 60 s depuis la dernière tentative automatique, aucun refresh automatique
supplémentaire ; après 60 s, une séquence au maximum. Le clic explicite peut
relancer après terminaison même avant 60 s. Pas de polling ni de file de clics
à rejouer. Annuler au démontage ; une réponse terminant malgré l’annulation est
ignorée par le contrôle de génération et de clé. Pas de retry de commande métier.

Un retour de fiche retrouve filtre, position et élément d’origine via les helpers
existants. Les copies publiques en mémoire peuvent accélérer ce retour, mais ne
suppriment pas la revalidation prévue par le parcours ; si la carte a disparu,
placer le focus sur le titre de période et expliquer sobrement son indisponibilité.
La restauration se fait une seule fois après les premières lectures qui peuvent
modifier la géométrie, y compris la zone personnelle de l’accueil. Un geste ou
une saisie commencé pendant cette attente garde la main ; aucun rappel différé
ne reprend ensuite le scroll ou le focus. `loading` décrit la première lecture
des récompenses, `revalidating` la relecture avec copie ; les contrôles d’accueil
et de Mes lots restent occupés dans les deux états.
Une pagination ne cumule pas une page provenant d’une ancienne génération avec
une page fraîche. Pour lever toute ambiguïté lorsque plusieurs pages sont
affichées, la revalidation reconstruit **la fenêtre actuellement visible en
entier**, avant remplacement atomique :

1. Capturer le curseur de début de fenêtre, le nombre `k` de pages effectivement
   conservées (1 à 5) et l’identifiant du premier élément visible avec son décalage
   dans la fenêtre de lecture. Ne pas reconstruire les anciennes fenêtres évincées.
2. Relire depuis ce début puis suivre uniquement les nouveaux curseurs, en série
   pour cette fenêtre, au plus `k` requêtes et moins si la fin est atteinte. Un
   catalogue serveur affichant une seule page ne relit que cette page. Ce mécanisme
   remplace les pages déjà demandées ; il n’anticipe aucune nouvelle page.
3. Conserver la fenêtre précédente identifiée en revalidation pendant cette
   préparation. Ne pas publier une page isolée ni mélanger les générations. En
   cas d’échec d’une page, garder toute l’ancienne fenêtre datée et proposer
   Réessayer. Annuler la préparation si les filtres ou droits changent. Pendant
   cette séquence, ne pas lancer une pagination concurrente ; la navigation vers
   les fiches reste disponible avec ses contrôles existants.
4. Au succès, remplacer la fenêtre, ses curseurs et ses compteurs ensemble.
   Restaurer l’ancre et le focus sans déplacement lorsque l’élément existe encore.
   S’il a disparu, utiliser le prochain élément de l’ancien ordre encore présent ;
   à défaut, le titre de section, avec annonce « Le programme a changé ». Le
   maintien de position exigé par LH-04 s’applique aux éléments conservés ; cette
   disparition réelle est l’exception explicite, pas une permission de remonter
   systématiquement en haut de page.

En cas de curseur de début périmé, interrompre et proposer une reprise explicite
depuis la première page avec les mêmes filtres, sans boucle. Les deux périodes
sont deux fenêtres indépendantes ; un échec de l’une n’efface pas l’autre. Les
fenêtres en préparation restent bornées à une copie supplémentaire par fenêtre
active (60 éléments par fenêtre au maximum), hors DOM, libérée au commit, à
l’échec ou à l’annulation. Les limites de concurrence globales restent appliquées.
En multi-communes legacy, répartir ce budget en pages entières : les tableaux
bruts de pages respectent aussi le plafond, même si quelques places restent
inutilisées. Tronquer uniquement la liste rendue ne suffit pas.

### 7.4 Annuaire, filtres et adresse

Les routes restent `/live/decouvrir`, `/live/commercants` et
`/live/commercants/:id`. Le retour issu d’une animation conserve son filtre et
sa provenance ; un accès direct possède un retour de secours explicite.
La navigation générale retrouve les filtres propres à chaque vue, sans copier
une recherche d’animation dans la recherche d’un commerce.

Le contrat annuaire ne prend qu’une commune : ne pas lui passer la sélection
multiple du catalogue et ne pas agréger toutes ses pages par commune. Un filtre
communal explicite reste affiché ; sans filtre, indiquer Toutes les communes et
« Commerçants des animations publiques ». Les communes suivies alimentent le
sélecteur existant sans prétendre filtrer automatiquement les résultats. Un
filtre d’animation garde un libellé visible et une action Retirer le filtre.

Une ligne résultat comporte le nom complet, le rattachement libellé sans
confusion avec l’adresse, une photo autorisée ou l’icône commerce, Horaires et
animations et Y aller si disponible. Les libellés longs reviennent à la ligne.
La fiche expose l’adresse complète, les horaires publiés, les animations publiques
associées et le descriptif en second plan. Les coordonnées absentes ne sont pas
inventées ; un itinéraire reste un lien externe identifié.

Pour LH-10, isoler un helper pur d’affichage : découper les vrais retours à la
ligne, ignorer les lignes vides, comparer les lignes consécutives après trim,
réduction des espaces et casse ; garder la première représentation. Aucune
suppression de mots répétés au sein d’une ligne, aucune correction d’adresse
postale par heuristique. L’itinéraire utilise toujours la valeur canonique
existante. Tests avec la ligne répétée trois fois, deux bâtiments différents,
ponctuations différentes et adresse monoligne. Vérifier séparément, en lecture,
la provenance du cas TEST si nécessaire ; le diagnostic ne déclenche ni SQL ni
édition de commerce. Si la source est effectivement incorrecte, consigner une
anomalie de données indépendante avec la cause établie et la réparation proposée.

### 7.5 Bornes et objectifs de fluidité

Les bornes et budgets du §5, dont p95 API ≤ 500 ms, restent inchangés ; la
présentation ne résout ni ne ferme LA-16. Les nouveaux contrôles ci-dessous sont
des cibles à tester, pas des mesures acquises.

| Chemin | Borne / politique | Preuve attendue |
| --- | --- | --- |
| Accueil | Sources personnelles 50/25/25 ; catalogue serveur 12 par période ; pas de requête commerçant pour le nouveau lien. Maximum 3 lectures en vol, dont 2 catalogue, comme §2.1. | Comparaison du nombre d’appels avant/après, premier accès et refresh ; aucune lecture par carte ni collecte exhaustive. |
| Catalogue | Cache public 5 contextes maximum, limites §3.1 et plafond 120 cartes DOM conservés ; snapshots de revalidation remplacés, jamais ajoutés indéfiniment. | 30 changements de filtres et retours ; taille des collections plafonnée ; réponses inversées et retrait de visibilité. |
| Annuaire | Requêtes 12 commerces par page, au plus 5 pages/60 commerces conservés dans la fenêtre affichée ; au-delà, fenêtre suivante explicite, pas de scroll infini. Conserver 5 curseurs de retour maximum ; retour plus ancien vers le début avec information explicite. | Fixtures 12, 60, 61 et 600 commerces ; aucune requête supplémentaire avant action, mêmes filtres et aucun doublon ; retour sur fiche dans la fenêtre courante. |
| Première attente | Ossature immédiate ; pas de délai artificiel minimum. Un indicateur de revalidation visuel peut être différé de 150 ms pour éviter un flash, sans retarder les données ou l’annonce accessible. | Réponses simulées 50 ms, 300 ms, 2 s, timeout ; une annonce par zone, aucune succession de titres d’attente. |
| Mouvement | Feedback press/focus dès l’événement ; transitions 120–180 ms ; aucune attente de fin d’effet avant navigation. Mouvement réduit : effets non essentiels désactivés. | Horloge contrôlée, clavier, double clic et reduced-motion ; aucun effet lié au scroll automatique. |
| Géométrie | Sur le scénario de revalidation, position des CTA/focus conservée tant que les données n’ont pas changé. CLS ≤ 0,1 sur parcours reproductible à 390 × 844, images/font chargées puis chargement initial séparé. | Enregistrer les layout-shifts et les rectangles des commandes avant/pendant/après ; n’exclure aucun déplacement de façon opportuniste. Le CLS seul ne prouve pas la stabilité des clics. |

Aucun nouveau type de requête SQL n’est prévu. La revalidation d’une fenêtre
annuaire déjà étendue peut désormais relire jusqu’à cinq pages au lieu de revenir
à la première : ce coût est explicite, en série et borné, sans nouvel appel tant
que la séquence précédente n’est pas terminée. Vérifier les lectures existantes
à froid et à chaud avec fixtures N/10N ; compléter LA-16 selon son protocole isolé pour
déclarer cette dernière satisfaite. Aucun test de charge sur TEST partagé.
Observer mémoire navigateur et collections après les 30 cycles ; libérer les
générations annulées et les références d’images, pas seulement limiter le DOM.

### 7.6 Recette et livraison

| Critères | Tests ciblés dans Marketplace | Résultat / traçabilité |
| --- | --- | --- |
| LH-01/02 | `tests/visual/live-home-density.spec.cjs`, `live-home-community.spec.cjs`, `live-home-communes.spec.cjs`, `live-hierarchy-fluidity.spec.cjs` : 0/1/plusieurs communes, action personnelle, présent/futur, zéro/partiel, titres longs. | Réalisation locale ; résultats au bilan E73. |
| LH-03/04/05 | `live-personal-refresh.spec.cjs`, `live-hierarchy-fluidity.spec.cjs`, `live-discovery-continuity.spec.cjs` et tests Node des hooks/helpers : première lecture, même contexte, refus privé, réponse tardive, focus+visibility simultanés, refresh répété, curseur périmé, capacités ancienne/nouvelle. Trois pages chargées puis retrait d’un élément et réponses inversées : au plus trois lectures de pages pour la fenêtre revalidée, commit atomique, ancienne génération ignorée et ancre/focus restitués selon §7.3. | Réalisation locale ; résultats au bilan E73. |
| LH-06/09/10 | `live-merchants.spec.cjs` : arrivée générale vs animation, filtre unique/multiple non implicite, adresse, absence de photo/horaires, fenêtre 60+, retour et accès direct ; helper adresse en test unitaire. | Réalisation locale ; résultats au bilan E73. |
| LH-07/08 | `live-discovery-dynamics.spec.cjs`, `live-discovery-unique.spec.cjs`, `live-hierarchy-fluidity.spec.cjs` : trois moteurs, une métrique, images absentes/lentes/erreur, date/CTA, favoris/partage. | Réalisation locale ; résultats au bilan E73. |
| LH-11/12 | Suites home, discovery-continuity et `live-hierarchy-accessibility.spec.cjs` : vide vs erreur, couverture, aide, reduced-motion, clavier, absence de célébration au refresh ; règles du jeu de reçu confirmé inchangées. | Réalisation locale ; résultats et limites au bilan E73. |

Les noms abrégés du tableau sont sous `tests/visual/` ; les tests Node sont
`live-personal-refresh.test.cjs`, `live-discovery-navigation.test.cjs`,
`live-discovery-window.test.cjs` et `live-merchant-window.test.cjs` sous
`tests/security/`. Matrice de rendu : 320 × 568, 390 × 844,
768 × 1024, 1280 × 800 ; zoom 200 %, clavier et mouvement réduit. Contrôler les
contrastes sur rendu : texte courant ≥ 4,5:1, grands textes ≥ 3:1, composants
utiles et focus ≥ 3:1. Consigner les captures et états réellement vérifiés ;
un build seul n’atteste pas LH-01 ni LH-12. Ne pas assouplir les assertions de
droits/retour/fraîcheur au motif que le markup change.

Livraison applicative limitée à Marketplace/Live après tests Node, suites
navigateur touchées, lint et build selon le guide local. Aucun changement de
configuration, domaine, permission, contrat exporté ou SQL identifié. Maintenir
les deux origines historiques et leurs accès personnels. Repli possible sur le
bundle précédent sans migration descendante ni effacement du carnet.

Les fixtures isolées couvrent les nouveaux états ; pas de modification de données
de démonstration partagées. Backend, Animation et Pro restent compatibles avec
leurs contrats actuels. Le [bilan E73](verification-livraison.md) consigne les
résultats de réalisation, distincts des contrôles de spécification. Aucun essai habitant, mail réel ou accord
pilote n’est ajouté aux conditions de clôture technique.

## 8. Performance des lectures — E73-EVO-LIVE-PERFORMANCE

**Conception du 8 novembre 2026, non implémentée à cette phase.** Source :
[audit performance API](../../audits/backend/audit-performance-api-localeo-live-2026-11-08.md).
Les [18 critères LP](localeo-live-entree-unique.md#évolution-du-8-novembre-2026--performance-des-lectures-live-e73-evo-live-performance)
sont canoniques dans la spécification fonctionnelle. Ce chapitre précise leur
réalisation et remplace, pour ces chemins, les choix antérieurs incompatibles :
chargement intégral du carnet, liaison préalable exhaustive des lots et compteur
global obligatoire. Les comportements LA/LH et la réserve LA-16 sont conservés.

### 8.1 Responsabilités et décisions

| Propriétaire | Responsabilité conservée et changement technique |
| --- | --- |
| Domaine Animation et registre de moteurs | Publication, dates effectives, capacité, inscription, qualification, règlement, passage et lieux révélés restent les règles existantes. Les faits sont chargés autrement ; le moteur ne reçoit ni statut ni preuve déduits par le frontend. |
| Domaine des accès et communication participants | Secret d’installation, token de participation, révocation et accord organisateur restent contrôlés pour chaque demande. Une liaison technique n’est ni inscription ni consentement ; un indicateur n’est pas un acquittement. |
| Application backend | UoW de lecture authentifiée, faits groupés par page, DTO de carte, contrôle de visibilité minimal pour les lots, orchestration du visuel et instrumentation. Pas de règle métier réimplémentée en route ou dans une projection SQL. |
| Adaptateurs PostgreSQL/stockage | Pagination, projections bornées, index démontrés utiles, lecture groupée des preuves ; éventuelles données dérivées synchronisées par leurs producteurs. Pas de charge globale ou historique avant découpage de page. |
| Marketplace/Live | Fenêtres et états d’affichage, file priorisée, déduplication par contexte, annulation, cache public en mémoire et synchronisation explicite des accès. Les résumés locaux sont des repères, jamais une autorisation. |

Décisions : pas de compte habitant, moteur, événement de notification, campagne,
score ou API de récupération par email nouveaux. Pas de cache persistant des
réponses API, pas d’augmentation automatique du pool ou du délai client.
Les scripts de tests restent dans leur dépôt applicatif ; ce chapitre ne crée
pas un nouveau registre de résultats.

### 8.2 Contrats HTTP et coexistence — LP-01/05/10/18

Les ajouts ci-dessous sont des **contrats cibles**, à développer et générer
ensemble avec leurs lecteurs. Les OpenAPI actuels ne sont pas modifiés pour
annoncer une fonction absente. Préfixes : catalogue
`/public/animation-locale`, personnel `/public/localeo-live`.

| Contrat cible | Compatibilité et sémantique |
| --- | --- |
| `GET /configuration` personnel : `capacites.catalogue_cartes=1` | Promet les deux options de catalogue ci-dessous sur les routes ancienne et moderne. Absence/0 : requêtes actuelles uniquement. Les capacités de moteurs et de recherche existantes restent indépendantes. |
| Catalogue `/animations` : `inclure_total: bool=true` | Défaut : contrat inchangé, `count=len(items)`, `pagination.total` entier exact et curseur existant. Opt-in `false` : même enveloppe et ordre, `pagination.total=null`, aucun COUNT global ; les clients continuent avec `next_cursor`, jamais avec le total. Nouveau schéma de variante, sans rendre le total absent pour les anciens clients. Aucun total approximatif ou inventé. |
| `/animations` et `/animations/recherche` : `projection=COMPLETE` par défaut, ou `CARTE_V1` | Sans option : DTO public actuel. Avec `CARTE_V1` : variante homogène `items: CarteAnimationLiveV1[]`, même enveloppe de pagination propre à chaque route. Aucune page mélangeant les deux DTO. Le nom versionné entre dans l’URL et la clé de cache ; il n’accorde aucun droit. Le détail `GET /animations/{id}` conserve sa réponse complète. |
| `CarteAnimationLiveV1` | `id`, `nom`, `commune:{id,nom}`, `date_debut`, `date_fin`, `statut_public`, `modele_code`, `visuel_url` nullable, `regles_participation:{nombre_validations_requises}` nullable selon moteur, `dynamique:{nombre_lots_a_gagner,nombre_participants}` avec valeurs réelles ou null si inconnues. Types et sens reprennent le DTO actuel. Pas de description complète, règlement, liste commerçants/lots/coffrets ni données privées. Zéro est une valeur connue ; absence n’est pas zéro. La promesse tombola/chasse reste déterminée par son moteur. |
| `GET /configuration` : `capacites.messagerie_legere=1` | Promet les deux options de messagerie suivantes. Ancien frontend : comportement identique ; nouveau frontend sans capacité : API actuelle, sans présumer un total nullable. |
| `GET /installations/{id}/messages?inclure_total=true` | Défaut actuel : `unread_count` entier exact. Opt-in `false` : `unread_count=null`, page et curseur inchangés, aucun comptage global. Ne pas remplacer le total par le nombre non lu de la page. Les branches NOTIFICATION/ORGANISATEUR et leurs droits restent celles du service courant. |
| `GET /installations/{id}/messages/indicateur` : `animation_id` devient facultatif | Avec UUID : même réponse qu’actuellement, même périmètre animation. Sans UUID : indicateur global autorisé de l’installation, réponse `{animation_id:null,has_unread:boolean,generated_at:UTC}`. Au plus deux EXISTS pour les deux branches de messages, aucune liste ni total. Secret toujours requis, `no-store`. Un autre UUID ne donne aucun accès supplémentaire. |

La liste historique conserve sa politique actuelle : les messages ORGANISATEUR
exigent une preuve personnelle valide ; les notifications NOTIFICATION restent
lisibles par leur installation sans réintroduire une preuve personnelle absente.
Le badge global emploie exactement ce périmètre de liste. L’indicateur contextualisé
par animation reste plus restrictif selon §3.2 : preuve personnelle courante
obligatoire pour ses deux branches. Aucun badge ni notification historique ne
permet d’ouvrir une destination privée avec un accès révoqué.
Les notifications historiques sans `animation_id` restent incluses dans le badge
global et leur liste selon l’installation, sans leur inventer de preuve d’animation.
Le global n’est donc pas l’union des indicateurs contextualisés de participation.

Le mapper commun `src/services/publicAnimations.js` doit conserver `total:null`
au lieu de le remplacer par `items.length`. Les compteurs de `CityPage`,
`AccueilPage`, `CommercantPage` et `AnimationsCatalogPage` gardent la lecture
avec total. Les lecteurs sans compteur exhaustif, dont LiveDiscovery et les
animations d’une fiche commerce Live, peuvent seuls négocier l’opt-out.
La portée du total de messages existant reste celle du contrat actuel ; ne
pas le renommer total filtré par animation sans évolution distincte.

Le passage de total exact à inconnu invalide l’ancien compteur mémorisé dans
`useLiveMessages` : pas de conservation d’un entier périmé avec `??`. Le header
utilise le point de présence global, la page affiche « non lus dans cet aperçu »
si nécessaire. Zéro non-lu parmi des pages chargées ne signifie pas « vous êtes
à jour » tant que l’indicateur global ou contextualisé approprié n’a pas confirmé
l’absence dans son propre périmètre. Les reçus de lecture locaux ne remplacent
pas cette vérification serveur.

Les valeurs de projection inconnues et options invalides donnent 422 ; aucune
substitution silencieuse par une autre projection. Les erreurs d’accès, capacité
moteur incompatible et projection non prête gardent leurs codes existants.
Les clients anciens n’utilisant aucune option reçoivent la même forme et la même
sémantique qu’avant. Un nouveau lecteur n’envoie ces options qu’après la capacité
correspondante ; repli déterministe, sans essai-erreur répété.

Un changement de projection ou d’option de total réinitialise la fenêtre côté
client. Les anciennes requêtes sans options conservent leurs curseurs ; les
nouveaux curseurs lient aussi la variante de représentation. Pas d’invalidation
globale des liens déjà distribués. La modernisation du catalogue historique
réutilise le chargement groupé mais conserve ses filtres commerçant/coffret,
ses statuts dont clôturé et son ordre ; elle ne le remplace pas aveuglément par
une recherche moderne dont le périmètre est différent.

Concrètement, absence d’option ou valeurs historiques explicites : dictionnaire
de signature et décodeur historiques inchangés, sans ajouter une clé par défaut
à l’empreinte signée moderne. Variantes négociées : version/empreinte distinctes
liant projection et option de total, y compris pour le format legacy différent.
Un curseur historique n’est accepté que dans sa représentation historique ;
mismatch : erreur de curseur déjà prévue pour la route, sans repli silencieux.

Producteurs : `animation_locale_api.py`, `recherche_animations_live_api.py`,
`messages_organisateur_api.py`, `localeo_live_api.py`, schémas et services backend.
Source documentaire de contrat : [OpenAPI Live E42](../epic-42-localeo-live/openapi.json),
généré hors ligne par `scripts/documentation/generate_epic42_openapi.py` du
backend. Les contrats moteur embarqués ne changent pas : ces DTO sont des vues
de catalogue et de messagerie, pas une nouvelle version du jeu.
Lecteurs : transport `src/services/api.js`, capacités, discovery, cartes,
fiche commerce et messages Live. Les cartes Marketplace Coffrets restent en
projection complète tant qu’elles n’ont pas été adaptées ; leurs usages du
descriptif et de l’inscription ne doivent pas disparaître.

### 8.3 Lectures backend bornées — LP-01 à 09

**Catalogue.** Paginer les racines autorisées, puis charger en groupe les
configurations effectives, modèles, retraits, paramètres, dotations et compteurs
nécessaires à cette seule page. La clé du dernier élément réutilise ses dates
effectives déjà lues. Aucun SELECT par carte, paramètre ou retrait. Le total
reste calculé uniquement pour le contrat historique qui le demande ; il ne
conditionne plus les lectures Live négociées. `CARTE_V1` ne charge pas une fiche
complète pour ensuite jeter ses champs ; les nombres de partenaires/coffrets
sont agrégés pour la page sans hydratation de toutes leurs fiches.

**Fiche publique et lots.** Avant optimisation de la fiche, relever SQL, pool,
projection, sérialisation et éventuel stockage pour les mêmes données. Grouper
les enrichissements réellement redondants ; ne supprimer aucun champ du détail
existant. La sous-liste de lots commence par le contrôle de visibilité minimal
commun au catalogue, puis une seule lecture `limit+1`. Ne pas appeler `obtenir`
pour cette autorisation. Visibilité négative : même réponse de refus, aucune
lecture publique de contenu. La mesure de la fiche inclut partenaires et lots
réels du jeu synthétique, pas uniquement un détail vide.

**Personnel.** Chaque GET dashboard/récompenses/tirages utilise une seule UoW
et le contrôle courant secret/installation avant sa projection. L’activité
technique n’est mise à jour que si son timestamp est plus ancien que 60 s :
UPDATE conditionnel atomique, monotone, sans `FOR UPDATE` gardé pendant le rendu.
Des requêtes simultanées ne doivent pas toutes réécrire une valeur récente.
L’intervalle ne modifie ni validité ni révocation ; il rend la date d’activité
approximative à une minute pour la rétention. Ajouter cette minute de grâce au
cutoff de purge (date enregistrée strictement antérieure à cutoff moins 60 s),
en conservant ses autres conditions, pour ne jamais supprimer plus tôt qu’avec
une date exacte ; tester la frontière temporelle et la concurrence avec une lecture.
Le commit technique éventuel reste court ; aucune transaction SQL n’encadre
l’accès au stockage distant ou la réponse HTTP complète.
Authentifier puis matérialiser la projection avant l’UPDATE d’activité ; cet
UPDATE conditionnel intervient en toute fin de transaction, suivi immédiatement
du commit. Aucun accès au stockage ni sérialisation HTTP sous son verrou.

Charger toutes les preuves email de la page dans une lecture dédiée de port,
puis les transmettre aux faits du moteur, avec absence explicite. Ne pas laisser
un `session.get` par participant ni substituer un booléen calculé par la route
au résultat du moteur. Conserver les préchargements existants du dashboard.
Le périmètre `participation_id` reste appliqué en stockage avant pagination.

**Plafond d’inscriptions.** Qualifier le sous-plan corrélé avec/sans plafond,
y compris les valeurs NULL et 0, inscriptions annulées et suppressions selon
la sémantique actuelle. V1 privilégie une requête/index adaptés sans nouveau
compteur métier. Si les budgets échouent, une projection de comptage ne peut
être adoptée qu’avec invariant documenté d’égalité au décompte courant, reprise
historique et maintenance dans la même transaction de chaque insertion,
suppression et modification pertinente. Tous les producteurs API/ERP/import/batch
doivent alors être recensés et testés avant activation. Pas de compteur différé
utilisé pour ouvrir une inscription ; un échec de budget maintient LP-07 ouvert.

**Annuaire.** Mesurer les prédicats et tris réels `q`, commune, animation et
`lower(nom) COLLATE C,id` ; première et page profonde, terme courant/rare/vide.
La migration d’un index éventuel utilise exactement l’expression normalisée et
les filtres servis, après comparaison `EXPLAIN (ANALYZE,BUFFERS)` N/10N.
Ne pas ajouter un trigram redondant par principe, forcer un index sur une petite
table, ni transformer le rattachement organisateur en filtre d’adresse postale.

**Readiness.** Mesurer le contrôle de catalogue système séparément ; la capture
de l’audit indique environ 0,5 ms d’exécution locale, sans preuve qu’il est le
goulot. **Décision V1 : conserver un contrôle DB courant par recherche** et le
réutiliser dans cette seule demande, sans second contrôle identique en aval.
Le cache positif inter-requêtes envisagé dans l’audit n’est pas retenu : un TTL
de 30 s pourrait masquer un trigger désactivé alors que la requête reste valide.
Un futur remplacement exige un mécanisme prouvé de détection/invalidation à
chaque lecture, y compris hors migration coordonnée, et les mêmes fault injections.
Ne pas affaiblir ces assertions pour retirer un aller-retour peu coûteux.

Le contrôle peut aussi alimenter la readiness au démarrage ; en cas d’échec,
l’application reste vivante mais la recherche répond 503
`CATALOGUE_ANIMATION_EN_PREPARATION`, jamais un résultat incomplet présenté
comme complet. Une réparation permet la reprise sans cache négatif durable.
Schéma, index, contraintes et triggers v304, ainsi que la garde BUM, restent
vérifiés. Aucun cache de readiness n’emporte une décision de visibilité métier.

### 8.4 Chargement Live et ordonnancement — LP-12 à 15

**Carnet.** Afficher d’abord les résumés locaux avec « à vérifier » tant que
le serveur n’a pas confirmé l’état. Page locale de **12 entrées**, navigation
explicite ; aucune pagination automatique pour reconstruire tout le carnet.
Producteur de revalidation limité à **2 entrées en cours**, sans soumettre N
promesses à la file globale. Chaque carte réussie est publiée indépendamment ;
un accès refusé est purgé de la vue autorisée, une panne reste une panne.
L’ordre de la page reste stable pendant les réponses. Lorsqu’un tri s’appuie
sur des données serveur encore partielles, il est annoncé comme tel ; le
résumé local ne qualifie ni urgence ni gain disponible.

Une cible `participation=<UUID>` est recherchée dans le stockage local par clé
et lue directement, sans attendre la page ou scanner le serveur. Sans accès
local exact, reprise neutre existante ; aucune autre participation à la même
animation n’est utilisée. Une ouverture fait **un seul GET de participation**
partagé en vol avec le moteur et au plus un GET de fiche contextualisée, sans
troisième relecture au montage. Un instantané d’affichage récent peut être
présenté en attendant ce contrôle ; il ne permet pas de présenter le QR ni
d’exécuter une commande. Les clés privées incluent installation, participation
et version locale d’accès ; la mutualisation par animation est limitée à la
fiche publique ou à sa contextualisation pour la même installation.

**Lots et liaisons.** Les GET récompenses et tirages des suivis existants partent
immédiatement ; leurs réponses ne s’attendent pas mutuellement. Chaque résultat
valide vérifie encore identité/contexte avant application. La liaison normale
est faite une fois lors de l’ajout confirmé d’un accès au carnet, avec les
credentials existants, puis reçue et rattachée à l’installation concernée.
Un reçu local évite un POST systématique au remontage mais n’accorde aucun droit.

Pour un ancien carnet non lié ou une nouvelle installation, conserver les bons
locaux en état à vérifier et afficher la couverture partielle. Proposer
« Synchroniser mes accès » : **au plus 5 accès par action, concurrence 2**,
progression explicite et suite demandée par l’utilisateur ; pas de boucle
automatique des 50 accès avant consultation. Une fois des liaisons confirmées,
revalider les pages concernées une fois. Échec isolé : conserver la liste des
accès restants, sans doublonner inscription, accord ou participation. La
révocation serveur prévaut toujours ; perte de réponse traitée selon les
garanties de répétition du contrat de liaison existant, sans créer de nouvelle
commande de participation.

**Priorités.** Garder le plafond **3 GET Live actifs, 40 en attente maximum**.
Priorité 1 : configuration initiale nécessaire, navigation demandée, détail et
page visible ; priorité 2 : revalidation des éléments visibles ; priorité 3 :
badge et lectures secondaires. Au plus deux lectures de priorité 2/3 actives,
laissant un créneau au parcours demandé ; deux recherches de période maximum.
FIFO à priorité égale ; après quatre départs prioritaires consécutifs, servir
une attente plus basse encore utile. Pas de préemption d’une commande métier.
Ces bornes sont un plafond technique, pas une invitation à remplir la file.

Dédupliquer en vol les GET réellement identiques, par route/filtres/capacités
et contexte autorisé. Aucun secret en clé de métrique ou URL publique. Un appel
partagé est annulé lorsque plus aucun lecteur ne l’attend, pas au démontage du
premier composant encore utilisé par un second. Propager `AbortSignal` jusqu’au
transport du carnet, de la fiche contextualisée et du moteur ; ignorer aussi
toute réponse d’une ancienne génération. L’annulation navigateur ne garantit
pas l’interruption d’un SQL déjà envoyé ; délais serveur restent nécessaires.
Le budget global **15 s, attente comprise**, ne redémarre pas à la sortie de file.

**Accueil et configuration.** Sans installation ni accès local, aucune création
d’installation ni requête privée pour simplement découvrir. Avec installation
existante, ne pas déduire l’absence de suivis de l’absence de carnet local :
continuer les lectures autorisées. Une création nécessaire au suivi, à l’ajout
d’accès ou à l’activation volontaire des notifications garde son parcours.
Configuration partagée en vol et **60 s en mémoire**, y compris Réglages/WebPush ;
clé origine API et version de contrat. Erreur sans dernier résultat valide :
état/repli ancien explicite, aucune capacité positive inventée. Ne pas prolonger
une capacité expirée par un cache service worker.

Le shell utilise l’indicateur global, la page messages seule charge les corps.
`has_unread=true` produit une pastille nommée « Des nouvelles à lire », jamais
un faux nombre 1 ; `false` n’annonce l’absence que dans le périmètre lu.
Polling visible existant au plus toutes les 60 s, focus/visibility mutualisés
selon LH ; pas de polling des messages complets à chaque vue. Les indicateurs
ne demandent pas de permission push et ne marquent rien lu.

Fenêtres publiques et annuaire restent bornées et remplacées atomiquement selon
§7.3 : la priorité ne permet pas d’afficher une combinaison de pages anciennes
et nouvelles. Leur contenu reste visible pendant la revalidation, même si
plusieurs pages doivent être relues. Pas de parallélisation aveugle de curseurs.

### 8.5 Cartes, images et mémoire — LP-10/11/18

La vue de carte légère est opt-in ; elle n’appelle pas le détail pour calculer
sa promesse. Son cache public en mémoire reprend les bornes existantes de
**5 contextes, 120 cartes par contexte** avec clés incluant projection,
capacités, filtres et origine. La fiche publique et l’inscription peuvent
partager cette seule lecture publique, TTL **60 s**, avec revalidation ; elles
n’en déduisent jamais un droit d’inscription, de passage ou de QR. Aucun cache
durable de fiche ou de capacité, et aucun cache privé nouveau. À l’erreur
d’accès, retirer la donnée concernée selon LH. La projection de carte ne doit
pas servir de substitut incomplet à une fiche attendue par un ancien lecteur.

Flyer : conserver le fichier source et ses contrôles de 5 Mo/intégrité.
Créer à la validation de l’image une dérivée de carte de **largeur maximale
960 px**, sans agrandissement, orientation corrigée, métadonnées retirées,
**150 Kio maximum**, format WebP ou format sûr déjà supporté par l’outillage.
Si cette borne ne peut être tenue, la carte utilise la variante sans image ;
le flyer source reste disponible par son parcours. La génération se fait une
fois par hash source, hors transaction SQL longue ; son échec ne publie aucune
dérivée partielle. Aucun service IA ni illustration par défaut n’est requis.

`visuel_url` de la carte négociée peut viser la sous-ressource additive
`GET /animations/{id}/illustration-flyer/miniature`, avec le même contrôle de
visibilité que la source et `Cache-Control: no-store`. Chaque demande revalide
la référence autorisée actuelle avant de lire les bytes. Un cache interne
facultatif par hash vérifié, **32 Mio maximum par processus, TTL 5 min**, peut
éviter un accès stockage répété ; il ne met jamais en cache une autorisation.
Retrait/changement de référence : ancienne URL refusée ou référence actuelle
seulement, aucun accès direct public à une clé de stockage privée. Les requêtes
déjà autorisées en vol gardent la même frontière de concurrence que la source.

Anciennes images : pas de retraitement exhaustif au premier GET ni de
téléchargement du source 5 Mo dans chaque carte. Une reprise optionnelle est un
job à lots de **25 références**, concurrence 1, checkpoint/reprise par hash,
validation de visibilité et quota d’espace avant écriture ; aucun traitement
sur TEST partagé pendant le développement. Tant que la dérivée n’est pas prête,
le nouveau DTO indique `visuel_url:null`, l’ancien DTO reste inchangé. Sauvegarde,
restauration, suppression et conservation englobent les dérivées ou leur
reconstruction déterministe depuis la source. La miniature ne crée pas un
nouveau droit de publication.

### 8.6 Coût, budgets et preuve de capacité — LP-16

Budgets d’acceptation cibles sur le banc de référence §5 : API et PostgreSQL
chacun 2 vCPU/4 Gio, même réseau, pool de lecture de test 10 sans débordement.
La latence HTTP inclut autorisation, acquisition de connexion, projection et
sérialisation ; les métriques SQL sont détaillées séparément. Les objectifs
nouveaux de fiche, personnel, annuaire et lots ne sont pas des mesures acquises.

| Famille | Borne et accès | Budget cible, premier résultat et page profonde |
| --- | --- | --- |
| Recherche moderne | Page 12/50, 1 à 10 communes, keyset, racines ≤page+1, enrichissement de la seule page | Budgets §5 conservés : p95 ≤500 ms, p99 ≤1 s, ≤10 SQL, surcoût Python ≤10 Mio. |
| Ancien catalogue négocié sans total | Page ≤50 ; mêmes filtres/ordre/visibilité, configurations/retraits groupés | p95 ≤500 ms, p99 ≤1 s ; ≤10 SQL, nombre indépendant de 1/12/50 et N/10N. Ancien total demandé : un COUNT supplémentaire admis, coût global déclaré et mesuré ; ce chemin ne qualifie pas la lecture rapide Live. |
| Fiche publique et annuaire | Une racine ; annuaire défaut Live 12, serveur max 100 existant ; index après plans | p95 ≤500 ms, p99 ≤1 s ; fiche ≤12 SQL, annuaire ≤10, pas de requête par enfant. Données de détail réellement représentatives et bornes de sous-listes existantes mesurées. |
| Dashboard, récompenses, tirages | Pages serveur ≤50 ; défauts frontend 50/25/25, faits et preuves groupés | Chaque route p95 ≤500 ms, p99 ≤1 s ; ≤20 SQL incluant contrôle et éventuelle activité, nombre indépendant de 1/10/50 participations. Pas de requête par participant. |
| Messages négociés sans total | Page défaut 25/max 100, branches bornées avant union ; total séparé | p95 ≤500 ms, p99 ≤1 s ; ≤6 SQL incluant authentification. Indicateur global/par animation : §5, ≤4 SQL, p95 ≤200 ms/p99 ≤500 ms. |
| Page de lots publics | Contrôle ciblé puis `limit+1`, défaut 25/max 100 | ≤6 SQL, p95 ≤250 ms, p99 ≤600 ms ; pas de projection détail préalable. |
| Contact / lieu courant | Une animation ou une participation autorisée | Budgets §5 inchangés, y compris exclusion des futurs lieux cachés. |
| Cartes et miniature | DTO léger, aucune collection ; miniature ≤150 Kio | Page de 12 cartes ≤24 Kio JSON brut et page 50 ≤100 Kio avec fixture nominale de noms/communes longs déclarée. Mesurer aussi compression ; ne pas tronquer des titres pour passer. Miniature chaude p95 ≤250 ms/p99 ≤600 ms hors génération ; aucune génération synchrone au GET. |
| Frontend | 3 GET actifs, 2 entrées revalidées, page carnet 12 ; caches §8.5 | Résumé local rendu sans attendre le réseau ; une réponse utile reçue n’attend pas une autre source pour apparaître. Pas de promesse de temps réseau depuis une simulation navigateur. |

Le budget SQL compte les statements réellement exécutés, y compris contrôles,
SET et activité ; distinguer SELECT et écritures dans la mesure. Les tableaux de
l’audit comptant seulement SELECT ne prouvent pas cette cible complète. Les
coûts autoritaires d’ouverture et de qualification ne sont pas exclus pour
faire passer un plafond. Les relations/faits sur les IDs de page sont bornés ;
les index de recherche et projection v276/v304 restent vérifiés et non supposés.

Campagne isolée : **N=1 000 animations/10 000 participations/50 000 messages**,
puis 10N ; faire croître séparément le périmètre lu, les données étrangères et
l’historique. Inclure 0/1 000/10 000 inscrits par animation plafonnée, 1/10/50
participations d’installation dont tombolas publiques, 1/10/50 partenaires et
lots, 1 000/10 000 commerces avec noms et rattachements variés. Premières et
pages profondes, q courant/rare/vide, accents, 2/3 caractères, zéro résultat,
images source/dérivée absentes, index/readiness indisponibles.

Après stabilisation, **cinq minutes à 1 puis 10 lecteurs**, charge mixte §5
(2 écritures/s, notifications simulées), puis saturation 20/40. Conserver les
budgets des écritures et régression p95 ≤20 % ; zéro 500, doublon, fuite ou
perte de validité. Refus de surcharge borné selon le contrat 429/503 existant,
pas une file sans limite ; retour au nominal sous 60 s. Les délais pool/SQL/
verrous sont instrumentés puis bornés pour que la réponse ou le refus arrive
dans le délai client global de 15 s ; ne pas conserver aveuglément une attente
de pool de 30 s pour ces lectures. Leur réglage respecte le budget total de
connexions de tous les workers, sans pool supplémentaire non compté.
Enveloppe de refus cible : **au plus 5 s côté serveur**, acquisition de connexion
**500 ms maximum**, SQL de lecture **2 s maximum par statement**, attente de
verrou **250 ms maximum**. Ces plafonds techniques ne remplacent pas les budgets
p95/p99 plus stricts. Les adapter par les mécanismes de lecture bornée existants,
sans modifier les délais des commandes métier ni masquer leurs résultats
incertains ; documenter les clés réellement utilisées à la livraison.

Enregistrer HTTP p50/p95/p99, erreurs/débit, SQL et plans, lignes/objets, CPU,
mémoire, pool et verrous ; captures premier accès et lectures chauffées séparées.
Un résultat matériel non équivalent est une preuve locale limitée ; un test
simulé, un test vert de bornage, une moyenne ou trois GET TEST ne valent pas
acceptation des percentiles. Le job de qualification doit échouer ou produire
un verdict non accepté si un budget échoue, sans modifier les seuils après coup.

### 8.7 Diagnostic et sécurité — LP-17

Réutiliser corrélation HTTP et instrumentation existantes. Décomposer par nom
de route normalisé : attente de file navigateur, HTTP, application, acquisition
pool, SQL total/nombre, projection/sérialisation, stockage/octets, statut et
fraîcheur. Histogrammes agrégés ; aucune étiquette par habitant, commune, token,
UUID de participation, email, recherche libre ou URL personnelle. Pas de texte
SQL avec paramètres ni secrets dans les journaux. En navigateur, mesures
locales/fixtures et outils de diagnostic existants ; aucune nouvelle collecte
Analytics sans le consentement existant, ni beacon ajouté pour cet audit.

La corrélation peut être restituée à l’erreur selon le contrat actuel ; ne pas
révéler des détails DB dans le public pour faciliter le diagnostic. L’observation
ne conserve ni corps privé ni cache d’autorisation ; son coût est inclus dans
les budgets. Le lien avant/après associe SHA, index, hardware et fixture à la
même campagne, sans comparer une mesure de service local à un HTTP distant.

### 8.8 Données, livraison et reprise — LP-18

Livrer backend avant le nouveau consommateur. N’annoncer une capacité qu’après
présence des handlers/schémas, tests de compatibilité et readiness de ses données.
Un backend nouveau sert encore l’ancien frontend ; un frontend nouveau sans
capacité utilise les formes historiques, avec leurs limites de performance
signalées. La coexistence ne permet pas de déclarer le chemin moderne qualifié
à partir de la seule compatibilité de l’ancien chemin.

Aucun changement d’inscription, token, lot, consentement, suivi ou compte n’est
nécessaire pour ces optimisations. Activité throttled : précision de rétention
et tests de purge à adapter, pas de suppression anticipée. Index/miniatures et
éventuelle projection de comptage sont des migrations **additives**, à numéroter
lors de la réalisation après inventaire des migrations réellement présentes ;
ne pas modifier v276/v304 ni réserver ici un numéro pouvant être pris ailleurs.
Pour chaque index, documenter taille/coût d’écriture et stratégie de création
compatible avec le runner de migration, sans présumer `CONCURRENTLY` disponible.

La référence de miniature, son hash et son état de préparation doivent être
persistés dans l’adaptateur d’illustration, pas dans l’agrégat pour créer une
nouvelle règle métier. Reprise historique bornée hors requête, journal d’échec
technique, réexécution idempotente par hash. Restauration : readiness des
projections, références valides et régénération possible des dérivées avant
annonce de capacité. Source manquante : image absente, aucun substitut inventé.

Rollback : retirer les capacités nouvelles et revenir au lecteur précédent,
sans DROP, migration descendante destructive ni effacement du carnet. Les
liaisons confirmées restent valides ; les reprises en cours peuvent être
suspendues à leur checkpoint. Pas d’annulation de commande métier pour annuler
un cache ou une optimisation. Aucun réglage TEST/production n’est appliqué par
cette spécification.

Sources à actualiser lors de la réalisation :
[campagne performance E59](../../exploitation/technique/executer-campagne-tests-performance-api.md),
[configuration E73](../../exploitation/technique/configurer-epic-73.md),
[communication participants](../../exploitation/exploitation/communiquer-participants-animation.md),
[flyers](flyers-contextualises.md) et guides Live du dossier E42.
Leur mise à jour décrira les fonctions effectivement livrées ; aucun guide
d’exploitation ne doit présenter les capacités cibles comme déjà disponibles.

### 8.9 Traçabilité, preuves à produire et préparation

Toutes les lignes suivantes sont **prévues, non exécutées pour cette évolution**.
Les tests/GET de l’audit sont des baselines, conservées au bilan, pas des tests
de correction. Réutiliser d’abord les suites existantes ; les noms de nouveaux
fichiers seront inscrits au bilan seulement après création et exécution.

| Critères | Propriétaire / contrat | Preuve prévue | Documentation / fixtures / démonstration | Exploitation / livraison |
| --- | --- | --- | --- | --- |
| LP-01/06/10 | Catalogue application + adaptateurs ; DTO/option de total opt-in, autorisation lots existante | PostgreSQL requêtes pages 1/12/50, classique avec retraits, BUM actif/inactif, anciennes/nouvelles réponses, curseurs et visibilité retirée ; contrats HTTP et cartes Live/Coffrets | OpenAPI E42 généré et API frontend alignés à l’implémentation ; fixtures N/10N, anciens moteurs ; pas de modification des règles/générateur métier | Backend avant frontend ; pas de migration métier pour regroupement, readiness des index existants |
| LP-02/07/08/09 | Service catalogue/annuaire, faits d’inscription et readiness technique | Plans et budgets avec enfants/inscrits, filtres historiques, SQLcount global croissant mais hydratation page bornée ; schéma/index manquant, trigger désactivé après un succès, réparation et bases distinctes ; comparaison avant/après | Conception §8, guide E59 et exploitation à enrichir lors de réalisation ; fixtures synthétiques, aucune donnée TEST | Index/projection seulement si preuve ; configuration de capacité et readiness au déploiement ; pas de garantie sans hardware équivalent |
| LP-03/04 | Accès courant, application des lectures, moteur de qualification inchangé | Deux UoW anciennes vs une cible, activité concurrente, preuve absente/révoquée, mélange moteurs, 1/10/50 ; domaine sans ORM pour sémantique et SQL réel pour groupement | Règles d’accès et E74 réutilisées, purge d’installation testée ; fixtures sans vrais emails ; générateur inchangé pour ce lot | Pas de migration pour groupement ; activité technique et minute de grâce de purge à livrer ensemble, rollback sans suppression anticipée |
| LP-05 | Communication participants ; messagerie/indicateur négociés | Ancien client avec total exact ; opt-in null ; filtre animation/global, 5 000/50 000 messages, preuve/token révoqué, anciennes notifications, lecture explicite et cardinalité SQL | OpenAPI E42 et guide messages ; simulations des deux capacités, pas de campagne réelle | Déploiement backend d’abord ; pas de nouveau canal, quota ou consentement |
| LP-11 | Adaptateur média, visibilité de domaine existante | Source ≤5 Mo, dérivée ≤150 Kio, orientation, hash erroné, panne, retrait, concurrence, quota cache, reprise interrompue, sauvegarde/restauration | Fixtures images réelles de test sans personnages générés ; guide flyer et sauvegardes ; générateur seulement pour nouvelle référence dérivée si nécessaire | Migration additive de métadonnées et job borné si reprise demandée ; aucun traitement partagé implicite |
| LP-12/13/14/15 | Hooks/carnet/transport Live, ressources et accès existants | Node file/cache/liaisons, puis Playwright carnets 0/1/10/50+, réponse bloquée/inversée, changement installation, deux tokens même animation, navigation ciblée, 40 attentes, annulation partagée, lots partiels, config Réglages/WebPush | Guides carnet/lots et cette conception ; fixtures backend ancien/nouveau, bibliothèque corrompue et stockage refusé ; aucun peuplement TEST | Lint/build et serveur navigateur isolé ; pas de secret nouveau, pas de migration du carnet pour pagination ; préservation des reçus éventuels par installation |
| LP-16/17 | Adaptateurs de mesure + campagne E59 | Cinq minutes, charge mixte/saturation, budgets SQL/mémoire/latence et reprise ; logs sans données sensibles ; métriques bornées ; test vert structurel distingué du verdict capacité | Procédure performance à actualiser avec vrais chemins de tests et sorties ; rapports au bilan E73, pas de registre concurrent | Environnement isolé représentatif requis pour acceptation technique ; aucune preuve pilote/mail réel demandée |
| LP-18 | Producteur backend + consommateurs Live/Coffrets | Matrice quatre combinaisons de versions, variantes contrat, accès directs/retours, curseurs, repli et retrait, non-régression QR/PIN/liaisons | Contrats générés actuels seulement après implémentation ; architecture et guides touchés exportés selon manifeste | Sources puis exports vérifiés, migrations puis backend puis client ; repli sans perte ; cinq dépôts indépendants |

Commandes cibles : backend `scripts/validation/test_isolated.py` avec une base
jetable explicite pour adaptateurs/contrats et tests d’architecture requis ;
Marketplace suites Node puis Playwright isolé, lint/build. Aucun test réseau ne
dépend de TEST partagé ou d’une livraison email/push réelle.

**Préparation :** périmètre spécifié, pas d’arbitrage métier bloquant identifié.
LP-01/03/04/05/06/10/12/13/14/15/17/18 ont leurs choix de réalisation ;
LP-02/07/08/09/11/16 comprennent une étape de profilage/qualification sur cible
isolée avant de choisir l’optimisation physique ou d’activer sa capacité.
Le profil matériel de référence et les plans ne sont pas inventés : leur absence
empêche de déclarer la capacité vérifiée, sans bloquer les corrections indépendantes.
La fin exige **18 critères vérifiés**, consommateurs et migrations cohérents,
et aucun budget échoué présenté comme réussi. Les résultats et limites restent
au [bilan E73](verification-livraison.md), distincts de la clôture historique.

## 9. Fiche animation immersive — E73-EVO-LIVE-FICHE

**9 novembre 2026 — réalisation locale Marketplace/Live.** Complément des
[12 critères E73-FD](localeo-live-entree-unique.md#évolution-du-9-novembre-2026--fiche-animation-immersive-e73-evo-live-fiche),
issus du [rapport visuel](../../audits/marketplace/localeo-live-fiche-animation-ux-ui-2026-11-08.md).
Ce chapitre remplace les choix de composition de fiche publique incompatibles
avec cette cible, sans modifier les règles de jeu ni les décisions LA/LH/LP
sur les droits, la fraîcheur, les lots, les contrats et les bornes.

### 9.1 Périmètre, responsabilités et contrat consommé

Périmètre : `/live/animations/{animation_id}`, lien public et retours associés.
L’inscription et la participation personnelle restent des parcours distincts.
L’interface présente les faits ; domaine Animation et moteur conservent dates,
visibilité, ouverture des inscriptions, capacité, conditions, qualification,
tirage, gains et lieux révélés. Accès existants : un état inscrit de
l’installation ne constitue jamais un token de participation.

Réalisation dans `localeo-marketplace` : `LiveAnimationDetail`, nouvelle variante
`LivePublicAnimationView` et helpers `livePublicDetailPresentation.mjs`,
`AnimationRulesAndRegulation` réutilisé pour le règlement, `LiveJourneyHelp`,
navigation et feuille existante `live-public-detail.css`.
Le badge de notifications lit seulement une installation déjà présente sur une
fiche publique : aucun POST d’initialisation ni renouvellement implicite sur
refus. Les autres parcours de notifications conservent leur initialisation.
Réutiliser les composants/tokens de l’accueil. Le composant partagé doit
isoler explicitement la variante **publique Live**, par prop/classe de variante ;
ne pas changer implicitement le jeu personnel, le détail historique ni les
consommateurs Coffrets en corrigeant des sélecteurs globaux.

Pas d’endpoint ni de champ API nouveau requis. Source de contrat :
[OpenAPI Live E42](../epic-42-localeo-live/openapi.json), producteur backend
actuel. Consommation : détail public complet, enrichissement facultatif de
l’installation existante, carnet local, lots paginés et annuaire public autorisé.
Ne pas remplacer ce détail par `CARTE_V1` de LP-10, trop limité pour ses règles.
Cette conception est implémentable avec le backend actuel ; les optimisations
LP sont une livraison distincte, compatibles par leurs capacités négociées.
Une donnée publique absente reste inconnue, jamais fabriquée à partir du titre
ou d’un statut local. Aucun email ni accès personnel dans une URL publique.

### 9.2 Composition, hiérarchie et styles — FD-01/02/09/10

**Barre locale** : retour nommé à gauche, repère « L’animation », actualiser
iconographique à droite avec nom accessible « Actualiser l’animation ».
Le titre de l’animation reste le seul h1 dans la carte d’introduction ; le repère
de barre n’est pas un deuxième titre principal. Le retour conserve son libellé
contextuel, la fenêtre, les filtres, l’ancre et le focus LA/LH existants.

**Mobile, ordre de lecture :**

1. Carte Votre défi : pictogramme du moteur, commune, statut et période compacte,
   titre ; promesse en phrase et éventuel flyer sous le titre ; conditions
   essentielles lisibles ; action primaire et récupération secondaire.
2. Comment jouer ? : guide court illustré adapté au moteur.
3. À gagner : aperçu réel ; Où jouer ? : partenaires publics autorisés.
4. Description, conditions complètes/règlement et aide dépliables ; favori/partage
   dans une seule zone secondaire près de l’identité, sans dupliquer la récupération.

Une action primaire logique, un seul élément interactif pour celle-ci : sur
mobile, son conteneur peut être fixé au-dessus de la navigation basse comme
actuellement, sans dupliquer deux liens focusables. Réserver dans le contenu la
hauteur réellement mesurée de cette action, de la navigation et des safe areas.
Les cibles d’ancres et les champs ouverts ne doivent pas être masqués. À 393 × 852,
fixture nominale (titre ≤80 caractères, conditions ≤240), titre, promesse,
conditions et CTA atteignables dans le premier écran ; CTA visible au-dessus de
la navigation. À 320 × 568, texte long et zoom 200 %, contenu intégral accessible
par défilement sans chevauchement ni défilement horizontal, sans tronquer une
condition pour satisfaire la hauteur.

Largeur bureau : même enveloppe maximale **1 080 px** que l’accueil ; dès 960 px
utiles, composition en deux zones possible dans cette enveloppe : défi/guide
principaux, récompenses/partenaires complémentaires. L’ordre DOM reste celui du
mobile et le clavier le suit. Aucune seconde barre d’actions fixe latérale.

Même palette, arrondis, bordures et pictogrammes que les cartes de découverte.
Action primaire bleu nuit et état/focus contrastés ; orange réservé aux accents
et repères existants, pas à un second bouton concurrent. Titres aux tokens
actuels, corps lisible **16 px**, métadonnées **14 px** minimum dans les blocs
repris, cibles **44 × 44 px**. Couleur toujours accompagnée d’un signe/texte.
Modifier les styles sources des composants, supprimer les règles devenues
inutiles dans le périmètre ; pas de nouvelle feuille de surcharges, dépendance
UI ou CSS global affectant les autres surfaces.

Flyer présent : bandeau après le titre, les conditions essentielles et les
actions, **128 px maximum sur mobile**, visuel
complémentaire **240 px maximum sur bureau**, ratio et recadrage stables.
Cette priorité maintient les conditions visibles avant le CTA fixe à 393 × 852,
y compris pour un titre de 80 caractères et des conditions de 240 caractères ;
le visuel complémentaire ne consomme pas leur budget de premier écran.
Conserver l’image configurée et son contrôle de publication ; ne pas faire
dépendre le titre/CTA du décodage de l’image. Absence connue : pictogramme et
accent de moteur, sans emplacement photographique vide. Image attendue en
erreur : même géométrie avec pictogramme de repli, sans nouvelle photographie.
Les éventuelles miniatures LP-11 restent optionnelles ; aucun nouveau média IA.

### 9.3 Promesse, conditions et guide — FD-01/07

Le nombre du défi est intégré à une phrase, sans grand chiffre isolé. Pour un
passeport, nombre positif fourni par `regles_participation` ou repli historique
autorisé : « Faites valider votre passage chez N commerçants » selon le sens
existant du moteur ; à défaut, « Découvrez le parcours chez les commerçants ».
Ne pas déduire un nombre de la taille d’une liste de partenaires ou d’un titre.

Source des conditions : `regles_participation` puis champ historique `regles`,
conformément au mapper existant. Les quatre clés publiques connues sont
`conditions_participation`, `nombre_validations_requises`, `inscription_requise`,
`age_minimum`. Présenter des valeurs valides avec libellés métier ; null reste
absent, zéro n’est pas supprimé automatiquement. Une valeur de structure
inconnue n’est pas convertie avec `String(objet)` ni présentée en clé technique.
Une ancienne chaîne simple publique reste visible intégralement ; un ancien
tableau de chaînes publiques peut être montré comme conditions textuelles.
Aucun objet inconnu n’est parcouru pour fabriquer des règles.

**Avant le CTA**, rendre le texte public `conditions_participation` intégral
lorsqu’il existe, ainsi que l’âge et l’inscription requise déclarés, sans
accordéon obligatoire ni ellipsis. La mise en page peut donc grandir pour un
texte long. Pas d’extraction automatique de la notion d’achat/gratuité par regex,
troncature, résumé IA ou lecture du titre. Dans la fixture Delphine, le texte
« Effectuer un achat, sans montant minimum… » doit ainsi être visible dès
l’introduction. Donnée absente : indiquer « Conditions non renseignées » et
laisser le règlement accessible, sans inventer une gratuité ni un nouvel
interdit ; les contrôles d’inscription restent ceux du serveur.

Le guide est une liste ordonnée de **trois repères au maximum**, avec pictogramme
et libellé court ; il décrit le parcours, pas une progression personnelle :

| Moteur pris en charge | Repères de parcours, adaptés aux conditions réellement publiées |
| --- | --- |
| Passeport commerçant | S’inscrire si requis → faire valider les passages annoncés → retrouver le suivi et la suite autorisée dans Live. L’achat n’est affiché comme condition que via le texte public fourni, jamais comme règle reconstruite localement. |
| Tombola locale | S’inscrire si requis → réaliser le passage selon les conditions publiées → consulter son suivi et les informations de tirage disponibles. Aucun gain garanti. |
| Tombola publique | Saisir son email → attendre la confirmation serveur d’inscription → conserver son accès personnel reçu par email pour retrouver la participation. Aucun email intermédiaire imposé, aucun achat ni passage ajouté. |
| Chasse au trésor | Ouvrir son parcours autorisé → suivre les énigmes révélées → consulter la progression confirmée. Aucune adresse future ni solution dans le guide public. |

Si le contrat ne permet pas de choisir un repère sans supposer une action,
employer un libellé neutre ou réduire le nombre de repères. Moteur inconnu :
présentation générique et refus de capacité existants, pas de guide d’un autre jeu.

Conditions complètes et règlement gardent leur version et accès au document
officiel. Le raccourci Conditions **ouvre** la section avant scroll/focus ;
l’arrivée directe avec `#animation-conditions` fait de même après chargement.
Focus sur le summary/titre nommé, marge au header fixe ; pas de fermeture par
une revalidation. Le lecteur peut ensuite fermer volontairement l’accordéon.
Le règlement complet peut rester replié, sans seconde ouverture nécessaire pour
atteindre les conditions de participation. Tout markup public reste échappé.

### 9.4 Actions, accès et états — FD-03/08/11/12

Précision du **11 novembre 2026 — inscription déjà connue** : les vignettes de
Découvrir et la fiche publique affichent un pictogramme de confirmation avec le
libellé visible **Déjà inscrit** pour une participation du carnet correspondant
à l’identifiant exact de l’animation. Un favori ou simple suivi public ne suffit
pas. La découverte lit le carnet une fois par vue, sans appel privé par vignette.
Une participation unique ouvre son accès précis ; plusieurs proposent
**Choisir ma participation** sans en sélectionner une arbitrairement. Le retour
conserve les filtres, le défilement et le focus de Découvrir.

Le lien direct vers le formulaire vérifie aussi ce contexte : pas de nouvelle
saisie proposée lorsqu’une inscription locale ou déclarée par l’installation
est connue. Le cas sans accès personnel propose **Retrouver mon inscription**.
Cette dernière vérification utilise un seul GET privé existant et ne crée pas
d’installation. Chargement et échec restent explicites, avec réessai ; aucune
inscription n’est envoyée pour effectuer ce contrôle. Une nouvelle vérification
ne détruit pas un formulaire déjà commencé ; il reste désactivé pendant le
contrôle. Un changement confirmé d’accès actualise les badges et actions.

Le badge est un repère de navigation, pas une autorisation de jeu : expiration,
révocation, qualification et résultat sont revérifiés dans le parcours personnel.
Sur un autre appareil ou domaine, la récupération volontaire reste nécessaire.
L’unicité animation/e-mail et les refus/reprises métier backend restent inchangés.
Cette précision complète FD-03 et ne crée ni compte habitant, API ou migration.

L’action prend en compte séparément : réponse publique courante, ouverture
annoncée par le serveur, accès locaux précis et enrichissement d’installation.
La découverte est disponible sans créer d’installation. Ordre de décision :

| Situation | Action et message |
| --- | --- |
| Première lecture ou identité A/B incohérente | Aucun CTA métier actif, cadre d’attente stable ; retour disponible. |
| Accès local unique à cette animation | « Reprendre ma participation » → `/live/animations?participation=<UUID>` pour cette ressource exacte ; le parcours personnel revalide token et état. Pas d’accès emprunté ni de QR dans la fiche publique. |
| Plusieurs participations locales à cette animation | « Choisir ma participation » ouvre une liste locale accessible, labels permettant de distinguer les accès sans exposer leur token ; aucun choix arbitraire. Sélection explicite → même route ciblée. |
| Installation déclarant inscrit, sans accès personnel local | « Retrouver mon inscription » ouvre la récupération existante. Ne pas promettre d’ouvrir le parcours avec le seul état `est_inscrit`. |
| Aucun accès et inscriptions annoncées ouvertes | « M’inscrire » vers la route existante, contexte/source conservés. Une animation à venir peut autoriser cette action. « Déjà inscrit ? Retrouver mon accès » en secondaire. |
| Aucun accès, inscriptions fermées | Message d’indisponibilité/motif public fourni ; pas de CTA d’inscription. Récupération d’un accès déjà existant reste disponible. |
| Animation annulée/inaccessible au catalogue public | Le contrat public actuel ne renvoie pas `ANNULEE` : refus générique « Animation indisponible », sans tenter d’en déduire la cause depuis le carnet. Retour et entrée Mes participations pour les accès locaux ; aucune relance d’inscription ou invitation au tirage. L’historique personnel autorisé peut ensuite expliquer l’annulation s’il reçoit ce statut. |
| Clôturée | Message « Animation terminée » et seuls faits publics disponibles ; aucune date de tirage ni résultat détaillé inventé. Accès personnel consultable, libellé « Consulter ma participation ». |
| Résultat/gain personnel | Pas de section de résultat public en V1 : le DTO public actuel ne fournit ni résultat ni preuve de publication. Les détails autorisés restent dans la participation personnelle. Un nombre de gagnants connu ne permet pas d’annoncer le gain d’un habitant. |

Le refus public et la clôture ne suppriment pas l’accès autorisé à l’historique
personnel. Aucune ancienne copie publique n’est utilisée pour contourner ce refus.
Un favori ou une fiche enregistrée
n’entre pas dans la liste des participations confirmées. Stockage illisible :
état explicite et récupération, pas une affirmation « vous n’êtes pas inscrit ».
Accès en erreur réseau : état à vérifier ; refus confirmé : aucun droit conservé
comme valide. Le parcours existant décide de la suite possible.

La récupération est secondaire près du CTA lorsqu’il y en a un, ou primaire
dans le cas sans accès personnel mais inscription connue. Ouvrir le formulaire
ne l’envoie pas ; réponse de récupération neutre, retour et focus conservés.
Un seul favori et un seul partage ; partager reconstruit uniquement l’URL
publique. Aide intitulée pour la découverte/inscription, sans phrase annonçant
« votre étape » ou « votre chance dans le suivi ci-dessus » si ce suivi n’est
pas présent. Le contact public reste chargé seulement sur ouverture volontaire.

### 9.5 Indicateurs, lots et partenaires — FD-04/05/06

Une métrique dominante, selon les faits publics disponibles : statut `CLOTUREE`
et `dynamique.nombre_gagnants` positif → nombre de gagnants, sans nom, détail de
résultat ou affirmation de publication ; sinon animation non clôturée et dotation
connue positive → lots à gagner ; sinon participants connus positifs → participants ;
sinon pas de métrique dominante. Sur animation clôturée, une dotation reste une
dotation prévue, pas une nouvelle occasion de gagner. Le DTO public actuel ne
fournit pas de résultat détaillé ; aucun champ fictif n’est ajouté aux mocks pour
simuler sa publication. Les autres chiffres connus, dont zéro, restent
consultables dans un groupe secondaire « En chiffres » ; pas trois grands
nombres concurrents. La dotation est toujours libellée « Dotation prévue »,
jamais « lots encore disponibles ». Aucune animation de chiffre ni compteur
personnel public ; dates exactes en Europe/Paris, pas de nouveau compte à rebours.

À gagner (ou « Dotation » après clôture) : **trois premiers lots maximum**, dans l’ordre serveur, libellé,
nature et quantité connues ; état de couverture partielle si nécessaire.
Conserver les mentions « fictif/de formation ». Bouton « Voir les lots » ouvrant
le détail de section, **pages de 25**, navigation explicite. Pour lots externes
et bons numériques, utiliser le curseur et la sous-ressource serveur existants.
Pour coffrets, le contrat actuel embarque une liste sans curseur : pagination
de présentation sur la liste déjà reçue, aucun appel `/lots` de lots libres pour
la compléter. Son coût de transfert/hydratation demeure la réserve LP-02, pas
une pagination serveur prétendument acquise. Pas de collecte automatique ni de nombre total déduit
d’un aperçu. Le bloc ne marque aucun lot personnel consulté et ne promet ni
qualification ni attribution. Absence, panne et dotation inconnue restent
trois états distincts ; les autres sections demeurent utilisables.

Où jouer ? : **deux partenaires publics maximum** provenant des données
autorisées déjà disponibles ; « Tous les commerçants » mène à l’annuaire avec
`animation_id` et contexte de retour. Afficher le profil public, puis horaires/
itinéraire lorsqu’ils existent ; pas de statut « ouvert maintenant » déduit
de texte libre. Aperçu incomplet nommé comme tel ; aucun compteur extrapolé.
Pour une chasse, aucune liste publique de lieux : expliquer qu’ils se dévoilent
dans le parcours, et proposer la reprise uniquement avec l’accès personnel.
Pas d’appel par partenaire ni par carte, pas de second téléchargement de tout
l’annuaire pour remplir deux emplacements. L’ancre publique `#animation-lots`
et l’entrée d’annuaire existantes restent fonctionnelles.

L’adaptation de présentation reconnaît les coffrets classiques par leurs champs
actuels, notamment `LOT_A_GAGNER` avec `coffret_id` ; un libellé « Coffret » dans
l’interface ne crée pas un nouvel enum API. Ne pas envoyer une variante de
dotation inventée pour obtenir une liste ou prétendre qu’elle est paginée côté SQL.

### 9.6 Lecture, fraîcheur et continuité — FD-09/10/12

Clé de rendu : origine API, `animation_id`, moteurs/capacités, puis identité
personnelle distincte si disponible. Changement A→B : invalider immédiatement
l’ancien contenu et ses CTA, anciens états de carnet/récupération/aide compris ;
annuler A et ignorer toute réponse tardive. Seul un payload dont l’ID correspond
à B peut activer un lien vers B. Ne pas se contenter de changer le paramètre
d’URL en gardant la projection A. Le focus initial du titre se réinitialise par
animation et n’interrompt jamais une saisie de récupération après enrichissement.

Première lecture : ossature de la fiche cible, une annonce de statut ; pas de
grand panneau de spinner autonome. Succès public : afficher sans attendre le
personnel ; un échec d’enrichissement privé ne masque pas la fiche publique.
Un changement d’installation purge l’enrichissement concerné et ne mélange pas
deux identités. Une réponse privée tardive ne rétablit pas un accès retiré.

Séparer les trois refus : fiche publique → retirer la copie publique et ses
actions ; installation → retirer seulement son enrichissement ; accès personnel
→ invalider la projection de cette participation. Un refus public ne révoque
pas un token local et ne prouve pas que son historique est inaccessible. Une
erreur d’installation ne supprime pas les autres accès personnels du carnet.

Actualiser le même contexte : contenu conservé avec indicateur discret et
commande mutualisée ; erreur conserve la dernière lecture datée, refus confirmé
retire les données inaccessibles. L’affichage conservé n’autorise aucune action
métier depuis une copie périmée. Retour au focus après **60 s** : revalidation
mutualisée avec visibilitychange, pas de timer de polling supplémentaire.
Propager l’annulation et respecter le plafond de **3 GET Live simultanés** et
le délai de **15 s attente incluse**, sans multiplier les appels par section.
Si LP-14 n’est pas encore livré, utiliser le transport existant borné ; ne pas
créer un ordonnanceur concurrent propre à la fiche.

Chargement de lots/partenaires étendu uniquement sur action. Respecter les
bornes §8 lorsqu’elles seront livrées ; conserver en V1 les méthodes d’accès
existantes. Les anciens volumes embarqués dans le détail restent à qualifier
par LP-02 : l’aperçu visuel borné ne prouve pas une hydratation SQL bornée.
Pas de cache API service worker, de cache personnel supplémentaire ou de
stockage de réponse dans le carnet pour contourner une relecture autorisée.

### 9.7 Recette, impacts et condition de fin

| Critères | Propriétaire / comportement | Recette de référence, résultats au bilan | Documentation / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- |
| FD-01/02/04/09 | Présentation Live ; faits publics du backend inchangés | Tests unitaires des sélecteurs/promesses ; Playwright accueil→fiche avec/sans flyer, 0/null/valeurs positives, titre et conditions longs, image lente/erreur ; captures 320 × 568, 393 × 852, 768 × 1024 et 1280 × 800 | Cette conception et guide Live du dossier E42 à actualiser lors de réalisation ; fixtures synthétiques reprenant achat obligatoire et mention formation, sans modifier TEST | Marketplace uniquement ; pas de SQL, permission, secret ou média supplémentaire ; lint/build requis |
| FD-03/08/11 | Navigation et accès locaux ; autorité du parcours personnel et des statuts conservée | Unique/multiple/absent, installation seule, favori seul, stockage refusé, accès expiré/révoqué, future ouverte/fermée, refus public d’annulation et clôture avec/sans nombre de gagnants ; absence de résultat public inventé ; récupération sans envoi automatique | Contrat E42 et règles E73/E74 réutilisés, pas de nouvel OpenAPI ; anonymes et deux participations même animation dans les fixtures | Pas de migration carnet ni création d’accès ; repli bundle sans perte, retour depuis les origines historiques conservé |
| FD-05/06/07 | Lots publics, annuaire autorisé, accordéons accessibles | Trois modes de dotation, quantité absente, plus de 25 lots, panne d’une source ; deux partenaires puis annuaire paginé et retour ; chasse sans lieu divulgué ; ancre Conditions en lien direct, tactile et clavier, focus/marge et règlement versionné | Fixtures de données manquantes, titres longs et structures de règles inconnues ; aucune modification du générateur métier requise pour ce seul rendu | Services actuels réutilisés ; pas de compteur nouveau, collecte exhaustive, pagination automatique ou email réel |
| FD-10/12 | État de lecture et navigation ; droits backend inchangés | A→B avec latence et réponses inversées, double refresh, focus+visibility, erreur publique/personnelle et retrait ; aucun CTA croisé ; retour programme/commerce, ancres et positions ; non-régression du jeu/inscription/Coffrets partageant les composants | Articulation LA/LH/LP conservée ; mocks isolés, pas de recette sur tokens réels | Pas de hausse de pool/délais ni migration ; charge/performance LP séparées, LA-16 non fermée par les tests de rendu |

Accessibilité : clavier complet et focus visible, noms des boutons iconographiques,
cibles 44 px, zoom 200 %, pas de dépendance à la couleur ; contrastes mesurés sur
rendu ≥4,5:1 pour texte courant et ≥3:1 pour grands textes/composants/focus.
Mouvement réduit respecté ; transitions courtes non bloquantes, aucune célébration
de réussite sur GET. Tester CTA fixe, navigation basse, champs et ancres en
hauteur réduite ; ne pas remplacer les assertions de géométrie par un simple
comptage d’éléments. Mesurer déplacement à l’échec du flyer ; l’audit n’a pas
fourni de valeur CLS de référence.

Réutiliser suites Node et Playwright de la Marketplace avec serveur/API isolés,
lint et build selon son guide. Les noms de nouveaux tests seront consignés au
bilan après création/exécution ; aucun test prévu n’est un résultat vert.
Pas de base, inscription, email ou notification réelle nécessaires à la recette.
Pas de nouvelle migration, configuration, contrat API, table ou adaptation
métier du générateur : les données et permissions existantes suffisent ; seules
les fixtures de présentation et guides sont concernés. Backend, ERP, Pro et
Animation conservent leurs contrats. Préserver les travaux locaux du header.

**Réalisation locale :** les douze axes sont implémentés dans la variante
publique Live. Les scénarios A→B, états personnels, refus publics et image en
erreur utilisent des fixtures isolées ; ils ne constituent pas une recette
déployée sur des accès réels. La fin demande les 12 critères vérifiés, les
non-régressions des composants partagés, la recette visuelle/accessibilité et
les contrôles requis réussis. Résultats et limites au
[bilan E73](verification-livraison.md), distincts de la clôture historique,
sans pilote externe, commit, push ou déploiement implicites.

## 10. Carnet personnel unifié — E73-EVO-LIVE-CARNET

### 10.1 Existant vérifié et écart

Préparation du 9 novembre 2026 : projet `13565af`, Marketplace `6d9e783`, backend
`8851cbd`, avec modifications documentaires en cours. Les
[critères CN-01 à 17](localeo-live-entree-unique.md#évolution-du-9-novembre-2026--carnet-personnel-unifié-e73-evo-live-carnet)
reprennent les cinq sections du PDF ; ils ne sont pas validés par les tests FD.

| Source réelle | Comportement actuel | Écart cible |
| --- | --- | --- |
| Marketplace `src/live/liveLibrary.js` | IndexedDB commun aux types coffret, animation, participation et bon_lot ; export/import v1, 5 Mo et 1 000 entrées maximum | Composer une liste commune sans réécriture ni migration destructive des accès ; ne pas dépasser les limites de restauration existantes |
| `LiveApp.jsx`, `LiveCarnetHeader.jsx`, `liveStore.js` | Quatre destinations, listes séparées ; coffrets masqués sur la surface Animation ; dernière rubrique mémorisée | Trois destinations et carnet commun ; préserver URLs ciblées et contexte de retour ; ne pas rediriger une inscription ou un lien personnel vers la racine |
| `LiveParticipationRecovery.jsx`, API `animation_locale_api.py` | Renvoi par animation/e-mail, réponse neutre, token livré à l’adresse enregistrée ; tombola distincte | Entrée Retrouver mon carnet explicite ; récupération groupée après choix CN-ARB-01 et preuve vérifiée, sans recherche publique révélant l’existence des objets |
| Backend `consultation_access_api.py`, use case `RenvoyerLienConsultationPublic` | Renvoi propre à une instance : bénéficiaire puis acheteur en repli, lien borné à 24 h et usage unique | Conserver le destinataire et la preuve propres au coffret ; pas d’accès global déduit de l’e-mail d’un achat |
| `AnimationRegistrationForm.jsx`, `CreerInscriptionAnimationRequest`, service participants | Téléphone obligatoire dans UI et schéma classique, normalisation inconditionnelle ; entité participant nullable | CN-ARB-02 doit aligner UI, API, application et domaine ; ne pas traiter la nullabilité SQL comme une autorisation suffisante |
| `PublicTombolaRegistration.jsx` et schéma tombola | E-mail et règlement, sans téléphone | Préserver ce contrat et l’issue incertaine/idempotence, compacter seulement la présentation indépendante |

La bibliothèque contient des capacités d’accès, non une identité partageable.
L’installation anonyme et ses suivis serveur exigent les preuves de chaque
ressource ; suivre une commune ne prouve aucun droit personnel. Vérifier les
contrats embarqués à l’implémentation ; les chemins ci-dessus décrivent les
producteurs examinés, sans certifier l’environnement déployé.

### 10.2 Présentation, navigation et continuité

Un composant de carnet compose les ressources déjà accessibles. Garder les clés
composites type/identifiant d’accès ; plusieurs participations à une même
animation restent plusieurs objets. Afficher des liens vers les parcours
existants ; le détail revalide le droit avant présentation, consommation ou
validation. Un refus retire uniquement la projection visée. Le résumé local
est « à vérifier » jusqu’au succès courant ; il n’autorise jamais une action.

La liste conserve son ordre initial stable au sein des groupes actifs/historique,
même si une carte obtient un nouveau badge d’échéance. Les pages de **12**
limitent rendu et revalidation ; pas de boucle sur toute la bibliothèque pour
produire un total. Au plus **3 GET Live simultanés**, délai **15 s attente incluse**,
annulation au changement de contexte et réponses tardives ignorées selon LP.
Un état partiel s’affiche par source ; un filtre ne transforme pas une source
en panne en type absent. L’enregistrement pour plus tard reste une référence
publique et ne devient ni accès personnel ni preuve de progression.

Entrées publiques et personnelles existantes restent résolues. Mémoriser les
positions/filtres par destination avec les mécanismes existants, sans token
dans une préférence, analytics ou journal. Racine générique : vérifier les
entrées locales avant de choisir carnet connu ou découverte ; stockage refusé
→ découverte avec aide, sans écran bloqué. Pas d’import inter-origines silencieux.
Le transfert volontaire et les services Coffrets existants restent disponibles.

Cloche dans le même emplacement d’en-tête, réglages par engrenage ; les icônes
complètent les mots. Carte personnelle complète au premier écran nominal à
390 × 844, suite perceptible, pas de grand bloc explicatif avant le contenu.
CSS et composants Live existants, vrais visuels ou repli graphique ; aucun
nouveau média généré ni nouvelle pile. Au zoom ou titre long, lisibilité et
accès aux actions priment sur le nombre de cartes visibles.

### 10.3 Règles, contrats et décisions dépendantes

**Invariant propriétaire :** les domaines Animation et Identité/Accès/Coffrets
conservent la décision sur participation, attribution, bénéficiaire, validité,
consommation et révocation. L’application orchestre la récupération ; API,
ERP, batch et Live ne réimplémentent pas ces règles. La liste est une projection
de lecture et non un agrégat « habitant » créé pour l’occasion.

La composition et l’harmonisation réutilisent les API et le format carnet v1.
La récupération groupée est un nouveau contrat conditionnel, **pas un endpoint
disponible** : demande neutre → preuve envoyée au destinataire autorisé →
vérification bornée → restitution des seules ressources autorisées, paginée et
explicitement partielle si nécessaire. Un GET public ne crée pas d’inscription
ni ne lie de participation. CN-ARB-01 résolu au §10.5 fixe la portée et les
bornes ; réutiliser identité/accès et email/outbox existants, pas un
second système de comptes. Tester adresse absente/partagée, preuve expirée,
rejouée, révoquée, multi-ressources et panne avant/après livraison simulée.

CN-ARB-02 est précisé par la demande du 11 novembre : nom, prénom, e-mail et
téléphone obligatoires pour toute nouvelle inscription, tombola publique incluse.
Les anciennes coordonnées absentes ne sont pas inventées ; présentation et
claviers/autocomplete sont partagés. Mettre à jour OpenAPI canonique E41/E42 concerné,
contrat embarqué et lecteurs lorsque ces contrats changent effectivement.

Les nouvelles structures éventuelles sont additives ; ne pas modifier une
migration appliquée. Ordre : backend compatible et migration/readiness, puis
consommateurs utilisant la capacité annoncée ; ancien backend conserve les
moyens de récupération actuels. Un repli frontend garde carnets et liens, et
ne prétend pas annuler un email déjà émis. Aucun secret, envoi réel, changement
de flag, migration TEST, commit ou déploiement ne découle de cette conception.

### 10.4 Matrice de preuves et impacts

| Critères / lot | Propriétaire, contrat et tests à produire | Documentation, données et exploitation |
| --- | --- | --- |
| CN-01/02/03/06/09 — carnet et navigation | Marketplace : bibliothèque v1 et routes existantes ; Node stockage/ordre/clé de ressource, navigateur liens ciblés, retour/filtre/position, origine historique, vide/erreur/partiel et accès multiples | Guide Live E42, README Marketplace et guide E73 à actualiser ; fixtures mixtes et restauration existante. Sans migration pour la seule UI, pas de générateur backend modifié artificiellement |
| CN-04/05/15/16 — objets et droits | Autorité backend existante ; UI à 1/10/50/>50 objets, accès coffret bénéficiaire, refus privés, latence inversée et pagination ; compter requêtes et cartes pour prouver les bornes, aucune consommation sur GET | Fixtures de droits et états exacts, pas de compteurs synthétiques exposés comme vrais. LP/LA-16 restent séparés ; aucune nouvelle projection publique ou cache API |
| CN-08/11/12 — inscription | UI partagée, schémas et domaine selon CN-ARB-02 résolu ; classique avec téléphone/tombola sans téléphone, format invalide, clé rejouée, mail non reçu, accès effectivement ajouté vs simple confirmation | Contrats d’inscription conservés ; conserver anciennes coordonnées et consentements, pas de reprise à vide. Générateur métier sans changement pour la présentation, emails simulés uniquement |
| CN-10 — récupération | Identité/Accès et participations ; preuve vérifiée avant restitution, anti-énumération, expiré/rejeu/révocation, exclusion coffrets, concurrence et reprise partielle ; revue indépendante du contrat | CN-ARB-01 résolu, bornes §10.5 ; migration/readiness et sauvegarde/restauration à vérifier. Aucun nouvel envoi ni service activé par la préparation |
| CN-07/13/14/17 — découverte et cohérence | Composants Live ; 390 × 844, 320 × 568, 1280 × 800, zoom 200 %, clavier, contraste, mouvement réduit ; cloche/non-lu, engrenage, une animation et plusieurs territoires | Fixtures synthétiques, réutilisation de vrais médias configurés ; pas de contrat métier/migration pour la présentation. Captures et assertions géométriques au bilan, appareils physiques explicitement non exécutés |

### 10.5 Arbitrages du 9 novembre et contrat de récupération retenu

Décision du 9 novembre, précisée le 11 novembre : téléphone **obligatoire**
classique conservé et formulaire homogène à quatre champs obligatoires (nom,
prénom, e-mail, téléphone) étendu à la tombola publique. Cette dernière précision
remplace l’exception sans téléphone. Les contrats d’inscription sont mis à jour ;
aucune migration ni reconstitution de coordonnées historiques. Voir le
[périmètre E74 actualisé](../epic-74-tombola-publique/README.md#harmonisation-des-inscriptions--11-novembre-2026).

Récupération groupée limitée aux **participations et lots associés**. Pas de
coffrets récupérés ni de droits acheteur/bénéficiaire changés. La preuve établit
le contrôle de la boîte ayant reçu les accès, pas une identité civile ni une
fusion des personnes d’une famille. Les tokens révoqués/expirés et participants
anonymisés ne sont pas recréés pour contourner un refus.

Contrat cible : demande par e-mail avec réponse neutre, challenge opaque haché
valide **15 minutes**, limitation IP/adresse et **un renvoi au plus par cinq
minutes**, puis confirmation explicite POST à usage unique. L’URL de réception
emploie un fragment nettoyé immédiatement ; pas de preuve dans analytics/logs.
Restitution de **50 participations maximum**, couverture partielle explicite,
ajout volontaire dans le carnet par ressource. Les lots sont relus par l’accès
participant existant ; aucun listing global de gains par e-mail.

| Route publique réalisée | Entrée / sortie | Refus et compatibilité |
| --- | --- | --- |
| `POST /public/localeo-live/carnet/recuperations` | Corps `{email}` ; 202 neutre avec `message`, `renvoi_apres_secondes:300`, sans existence ni nombre de ressources | 422 saisie invalide, 429 quota, 503 capacité/schéma indisponible ; aucun ajout local ni confirmation d’envoi réel |
| `POST /public/localeo-live/carnet/recuperations/confirmer` | Corps `{secret}` ; 200 avec `items` (participation_id, animation_id, animation_nom, token, expires_at), `incomplet`, `perimetre:PARTICIPATIONS_ET_LOTS_ASSOCIES` | 410 expiré/révoqué/consommé/invalide, 429 quota, 503 indisponible ; réponse privée no-store ; une issue incertaine ne rejoue pas automatiquement la preuve |
| `GET /public/localeo-live/configuration` existant | Capacité additive `capacites.recuperation_carnet:1` si table/colonnes et index requis présents, sinon 0 | Ancien client ignore la nouvelle capacité ; ancien backend ou erreur → UI conserve les voies historiques |

Contrat canonique [E42 OpenAPI](../epic-42-localeo-live/openapi.json), générateur
`localeo-backend/scripts/documentation/generate_epic42_openapi.py` ; appels
effectifs dans `localeo-marketplace/src/services/api.js`. Les schémas
d’inscription, moteurs, QR/PIN et contrats embarqués Animation restent inchangés.
L’application charge les candidats bornés puis quatre ensembles de faits ;
participants et au plus un token valide par participant sont verrouillés en
ordre stable. La consommation du challenge, les nouveaux accès bornés à leur
échéance existante et l’audit sont dans la même transaction. Le renvoi email
utilise l’outbox existante, sans transport fournisseur dans la transaction.

Migration additive **v306** : table `live_recuperations_carnet`, index de recherche
email/expiration des challenges, index de recherche globale participants par
email/date/ID et index de sélection d’un token valide par participant. Schéma
ORM, readiness et annonce de capacité alignés. La preuve est classée SECRET ;
les copies email sont minimisées selon leur durée/utilisation, les challenges
expirés sont purgés par lots bornés et les restaurations ferment ces preuves.
Le registre et la restauration démonstration ne recréent pas de challenge actif.
Les tests isolés et PostgreSQL locaux sont au bilan ; **v306 appliquée à TEST
le 9 novembre sur demande explicite**, table et quatre index valides contrôlés.
Cette migration ne prouve pas le déploiement des applications. Livrer
backend/migration avant UI. Sur ancien backend, conserver liens personnels,
récupération par animation et sauvegarde, sans promettre la capacité groupée.

Conditions de fin : critères du périmètre réalisé et refus significatifs testés,
non-régressions inscription/QR/PIN/Coffrets, contrats cohérents et guides mis à
jour, contrôles locaux réussis et limites de charge explicites. Les deux
décisions sont désormais résolues. La demande
engage spécification puis implémentation ; preuves réelles au bilan, sans
assimiler revue documentaire à recette ni rouvrir l’epic terminée.

## 11. Carnet de tampons — E73-EVO-LIVE-TAMPONS

**Thèse visuelle :** une page de carnet claire, papier chaud et empreintes encrées,
où les découvertes faites donnent envie de compléter les places encore libres.
Ordre de lecture : identité de l’animation, collection et compteur, état confirmé,
prochaine action. Les icônes SVG/CSS reprennent la boutique pour le passeport,
la boussole pour la chasse et le ticket pour les tombolas. Pas de nouveau média
à télécharger. Les cartes restent des objets personnels à ouvrir.

**Interaction :** les tampons sont informatifs, les actions gardent leurs verbes.
La validation confirmée garde le retour bref de `confirmedMilestone` ; aucune
animation d’acquisition au montage. Les transitions des actions restent discrètes
et désactivées avec mouvement réduit. Le détail des commerces conserve adresses,
horaires et dates, avec la présentation personnelle avant les visites.

**Sources :** `summary.type` et `dashboardProgress` pour la liste ;
`jeu.progression.terminees/requises`, `commerces[].valide/dateValidation` et
`etapeCourante` pour le détail. Compteur exact, rendu borné à huit empreintes.
Une empreinte résume une unité confirmée ; elle ne définit pas un lieu ou l’ordre
du parcours. Dans un grand objectif encore incomplet, l’aperçu conserve au moins
une empreinte vide pour ne pas suggérer visuellement une collection complète.
Le statut et `eligible` restent autoritaires : objectif rempli
n’implique ni qualification ni gain. Une tombola n’utilise pas le compteur comme
un parcours de visites. Les refus retirent toujours les projections concernées.

| Impact | Traitement et preuves |
| --- | --- |
| Critères TP-01/02/06 | Composant partagé et projection `unifiedCarnet` ; tests Node des comptes/moteurs, tests navigateur carnet mixte, refus, anonymisation, liens et pagination conservés. |
| Critères TP-03/04/05 | `LiveAnimationGame` et protocole existant ; tests parcours passeport/chasse/tombola, régularisation à 100 %, reçus rejoués/incertains et refresh neutre. |
| Critère TP-07 | Captures et assertions 320/390/1280, zoom 200 %, clavier et mouvement réduit ; essais sur téléphone physique et étude habitant suivis séparément. |
| Contrats, domaine, permissions | Sans modification : données déjà fournies par backend ; aucune règle calculée ou commande ajoutée par l’interface. Aucun changement ERP, Animation ou Commerçant. |
| Données, migration, configuration | Sans modification : aucun champ persisté, flag, batch ni migration requis ; ancien backend sans type utilise le rendu générique. |
| Documentation et exploitation | Guide Live, README Marketplace et bilan E73 mis à jour. Livraison du frontend seule après vérifications ; retour à la version précédente sans reprise de données. |
| Générateur et fixtures | Générateur backend inchangé car aucun état métier nouveau. Fixtures frontend synthétiques enrichies : zéro/partiel/plein, grands objectifs, moteurs distincts et carnet mixte. Aucun appel/envoi réel nécessaire à la recette. |

[Retour à la spécification Live](localeo-live-entree-unique.md)

## 12. Carnet de bord — E73-EVO-LIVE-CARNET-BORD

Thèse visuelle : carnet papier calme, tampons encrés et objets reconnaissables,
avec une action utile immédiatement repérable. Composition : prochaine action,
objets en cours, puis historique/enregistrés ; vide avec trois pictogrammes et
deux intentions. Fiche publique : défi, progression et récompense, conditions
courtes puis détails volontaires. Interactions : aides/filtres dépliables,
retour au contexte et gratification sur reçu confirmé ; mouvement réduit.

Invariants : le backend Animation et Identité/Accès vérifie chaque rattachement
et lecture avec installation et token participant. Le frontend orchestre la
reprise ; aucune fusion par animation/e-mail, inscription ni gain créé. Les
projections privées sont invalidées au refus ou changement d’accès/installation.
GET et ouverture d’un résumé ne valident ni commerce, ni remise, ni consentement.

Reprise par le POST existant `participations-personnelles` : **50 accès par
action**, **2 en vol**, puis **2 lectures agrégées de 12 objets** par page.
Aucun appel par tampon/carte ni pagination automatique. Suite/reprise explicite,
échec partiel signalé, accès locaux séparés conservés. Seul le refus
d’installation reconnu permet un renouvellement borné ; timeout/refus de token
ne le déclenche pas. Budget conservé lors des notifications de changement
d’installation pour éviter une boucle de créations. Tester 10/100 accès et
concurrence avec transport simulé ; capacité SQL existante suivie par LA-16,
aucune nouvelle requête backend ni charge TEST.

La prochaine action utilise les seuls objets confirmés chargés et indique une
couverture partielle. Aucun calcul d’éligibilité ; un coffret seulement mémorisé
reste à vérifier à l’ouverture : à défaut d’action confirmée sur une animation
ou un lot, proposer « Vérifier mon coffret » avec cet état explicite, jamais
« Présenter » depuis sa copie locale. Le gain conserve nature/identifiant/participation
dans sa destination, sans faire d’un paramètre de navigation une preuve d’accès.
Un parcours complété reste en cours de suivi tant que son tirage est en attente.
Les résultats terminaux confirmés rendent sa participation secondaire dans
l’historique ; un lot encore disponible reste un objet actif distinct. Sans
résultat exploitable, ne pas déduire la fin d’une animation du nombre de tampons.

| Périmètre | Impacts et preuves |
| --- | --- |
| CB01/02/04/05 | Navigation, carnet et lots Marketplace ; tests Node et navigateur mixte/vide/partiel, destinations exactes, clavier et captures. Guides E42/UX actualisés. |
| CB03 | Orchestration frontend des contrats existants ; restauration, renouvellement/refus, changement en vol, bornes et revue indépendante. Domaine, schéma API et persistance inchangés. |
| CB06/07/08/09 | Découverte, fiche, inscription, récupération et commerces ; tests des contextes/obligations et captures mobiles. Téléphone, consentements et preuves de récupération conservés. |
| Migration / configuration / applications voisines | Sans objet : endpoints existants, aucun flag, batch, migration ou changement ERP/Animation/Commerçant. Livraison frontend et documentation après recette. |
| Générateur / fixtures | Fixtures frontend mixtes et refus enrichies ; aucun état métier nouveau, générateur backend inchangé. Aucun envoi ou donnée d’exploitation dans les tests. |

Résultats et limites au bilan après exécution ; cette conception ne remplace
pas les preuves de rendu ni la recette du service déployé.

## 13. Parcours mobiles — E73-EVO-LIVE-PARCOURS-MOBILE

Consolidation du 10 novembre 2026, après le commit Marketplace `b9fb30d`.
[Critères PM-01 à PM-09](localeo-live-entree-unique.md#évolution-du-10-novembre-2026--parcours-mobiles-e73-evo-live-parcours-mobile),
[audit source](../../audits/marketplace/localeo-live-mobile-participation-lots-decouverte-2026-11-10.md)
et [matrice de preuves](verification-livraison.md#évolution--e73-evo-live-parcours-mobile-10-novembre-2026).
Ce complément précise les §7/9/10/11/12 sans changer leurs contrats métier.

### 13.1 Présentation et états

Le frontend présente les états confirmés par les domaines backend existants
Animation, Lots et Coffrets ; il ne décide ni qualification, ni gain, ni remise.
La prochaine action précède les informations secondaires. La référence visuelle
est [LIVE-UX-09](../../produit/live/principes-ux.md#live-ux-09--partager-la-lisibilité-de-localeo-pro),
avec les marqueurs du carnet et les gratifications sur reçu confirmé conservés.

| État | Présentation et comportement |
| --- | --- |
| Première lecture | `LiveLoadingState`, ossature statique réutilisée par `LiveLoadingShell` et les pages ; aucune commande provisoire, aucun faux vide. En-tête, navigation et retour restent présents lorsque connus. |
| Relecture | Conserver l'objet descriptif et sa position ; signaler la vérification. Les capacités du bon et du coffret sont suspendues jusqu'à confirmation de leur accès. Une identité différente ne réutilise pas le panneau de l'objet précédent. |
| Succès vide | Afficher l'état vide avec découverte ou récupération selon la page. Ne pas confondre absence locale, page partielle et absence confirmée. |
| Échec de transport | Dernier état connu explicite, reprise disponible ; aucune copie ne confirme un droit. Dans Découvrir, conserver le programme de la requête courante sans laisser une ancienne commune écraser la nouvelle. |
| Refus confirmé | Retirer la projection protégée concernée ; la conservation visuelle ne prime pas sur le refus. La portée vérifiée bon/coffret est distincte des limites du jeu consignées au bilan. |
| Commande en cours ou issue incertaine | Conserver formulaire, saisie et issue ; vérifier via le protocole existant, sans réexécution automatique. |

Le langage de chargement concerne module Live/carnet, participation et QR,
fiche/inscription, lots/bon/coffret/facture, découverte, messages, communes,
commerces, récupération/confirmation, réglages, fil local et juridique.
Import de sauvegarde et restauration locale gardent leur formulaire immédiat :
aucune attente distante fictive. Une erreur longue peut agrandir son emplacement.

### 13.2 Retours, bornes et compatibilité

`liveReturnNavigation` conserve le chemin explicite et le contexte de retour ;
`liveLotsNavigation` filtre les métadonnées propres à Mes lots. Elles indiquent
historique ouvert, identifiant de carte, position et nombre de pages par source.
Elles ne transportent ni projection métier, ni token, ni curseur privé. Une
destination ou un identifiant n'accorde aucun accès. Deux participations à la
même animation restent distinctes ; aucun regroupement par nom ou e-mail.

La reconstruction est limitée à **cinq pages par source** (lots distants,
tirages, bons locaux), à partir des lectures existantes. Les bons locaux sont
relus depuis IndexedDB, puis leur droit vérifié lors de l'ouverture ; leur
présence n'est pas une validation distante. La pagination suivante reste
volontaire. Échec ou fin de source arrête la progression ; un geste pendant
l'attente prend priorité sur le repositionnement. Le détail disparu est
annoncé, sans substitution d'un autre gain. Les tirages ne bénéficient pas de
la promesse de retour à une carte de lot.

Cette borne frontend ne vaut pas qualification de charge : le test navigateur
de continuité couvre deux pages de lots distants, la borne cinq est testée dans
le helper. Recette de cinq pages, dépassement et sources combinées restent au
bilan. Les budgets, mesures N/10N et charge mixte LA-16/LP conservent leur suivi ;
aucune nouvelle mesure de capacité SQL ou de latence hébergée n'est annoncée.
Les tailles des pages et les contrats des producteurs restent inchangés.

### 13.3 Impacts et livraison

| Impact examiné | Conclusion pour ce complément |
| --- | --- |
| Applications | Réalisation déjà poussée dans Marketplace/Live ; Pro fournit la référence visuelle et son code ne change pas. Animation et backend ne changent pas dans cette consolidation. |
| Contrats, permissions, concurrence | Aucun endpoint ni schéma partagé modifié ; accès exacts et contrôles serveur conservés. Annulation/réponses tardives et refus sont des comportements de non-régression, avec limites explicites au bilan. |
| Données, migration, coexistence | Aucun schéma ou format métier ajouté ; métadonnées de navigation filtrées et anciennes entrées sans métadonnées utilisables via le repli existant. Pas de migration ni opération sur les données d'exploitation. |
| Documentation fonctionnelle | Critères PM et décisions dans la spécification Live, LIVE-UX-08/09 conservés, entrée E42 reliée à ce complément. Audit historique maintenu et rattaché au suivi canonique. |
| Fixtures et générateur | Fixtures frontend synthétiques déjà enrichies pour lenteur, refus, retour, pagination et mobile ; aucun état de domaine ajouté, donc générateur backend inchangé. |
| Exploitation | Livraison frontend seule, aucun flag, batch, secret ou ordre de migration nouveau. Vérifier le SHA servi et les parcours sur TEST ; un push ne prouve pas cette recette. Revenir à l'artefact frontend précédent si nécessaire, sans modifier le carnet ni les droits. Aucune opération distante effectuée par ce complément. |

Les preuves et actions ouvertes sont centralisées dans le bilan ; ni les
corrections historiques ni leur qualification technique ne sont recréées ici.

## 14. Iconographie et respiration — E73-EVO-LIVE-ICONOGRAPHIE

[Critères IA](localeo-live-entree-unique.md#évolution-du-10-novembre-2026--iconographie-et-respiration-e73-evo-live-iconographie),
issus du rapport du 10 novembre. Thèse visuelle : carnet calme et lisible,
objets reconnaissables et tampons encrés, avec une prochaine action immédiatement
identifiable. Composition : identité/état, progression ou information décisive,
action, puis détails volontaires. Interactions : focus et dépliage existants,
gratification confirmée préservée ; aucune entrée animée ni nouveau geste caché.

La correspondance des icônes est une projection de présentation, pas une règle
métier. Le backend conserve l'autorité sur état, qualification, gain, droits et
consommation. Les accès, mutations, refus et métadonnées de retour existants ne
sont pas modifiés pour réduire le texte.

La famille `LiveActivityIcon` fournit les dessins utilitaires partagés : cadeau
pour lot, boîte pour coffret, carnet, parcours, QR et états explicites. Les
tampons ne sont pas remplacés par ces pictogrammes. Taille utile 20–24 px pour
commande, 28–32 px pour objet ; nom accessible porté par la commande, SVG
décoratif masqué. Les libellés importants demeurent visibles.

Espacements cibles : 8 px à l'intérieur d'une information, 12–16 px entre groupes,
16 px entre cartes, 24 px entre sections. Intérieur de carte 16 px à 390,
12 px à 320. Ces valeurs sont ajustées à la composition et testées avec les
actions visibles ; aucune marge globale n'est imposée au détriment du premier
viewport. Un seul cadre de progression et pas de sous-cadres redondants.

La compaction ne doit pas faire disparaître l'aide « Aller au défi » lorsque
le formulaire n'est que partiellement visible : le bouton principal de réponse
doit être entièrement hors des bandes fixes avant de retirer cette aide. Le
focus reste dirigé vers le défi, sans validation ni commande supplémentaire.

| Critères | Propriétaire / composants | Preuves prévues | Documentation / contrat | Fixtures / générateur | Exploitation |
| --- | --- | --- | --- | --- | --- |
| IA-01/07/10 | LiveLots, projection d'icônes, récupération ; états fournis par backend inchangés. | Lots de chaque nature/état, vide complet vs partiel, refus, retour exact, lecture/commandes inchangées ; capture et clavier mobile. | Spécification IA et principes UX ; pas de contrat API nouveau. | Fixtures frontend synthétiques enrichies ; pas de nouvel état backend. | Frontend seul ; aucune migration/activation. |
| IA-02/03/04/08 | Carnet, participation, QR, famille utilitaire et navigation. | Carnet mixte, grands objectifs, moteurs, QR indisponible/frais/refusé, focus, nom accessible ; 320/390 et texte agrandi. | IA-D01/02, CN/TP/PM conservés. | Tests existants adaptés seulement aux attentes remplacées ; générateur inchangé. | Réserve PM-R06 distincte ; aucun accès personnel de TEST requis. |
| IA-05/06/09 | Fiche, découverte et communes. | Avec/sans image, objectif inconnu, conditions, CTA nominal, périodes vides/partielles/en erreur, recherche, favoris, localisation et stockage refusés. | FD/LH/CN conservés ; limite dix communes et consentement inchangés. | Réponses simulées ; aucun appel distant des tests. | Aucun flag ni batch ; recette déployée distincte de la preuve locale. |

Données, permissions et coexistence : aucun schéma API, persistance métier,
contrat de stockage ou route modifié. Les lectures restent bornées comme avant,
pas de lecture supplémentaire pour produire une icône ou un espace vide. Les
autres applications et leurs générateurs n'ont aucun changement à consommer.
Le rollback du frontend ne requiert pas de reprise de données. Livrer les
sources Live et la documentation ; contrôler les parcours après déploiement
sans confondre build local et version servie. Résultats réels à consigner au bilan.
