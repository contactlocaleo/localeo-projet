# E73 — Conception de l’adhésion habitant dans Localeo Live

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

[Retour à la spécification Live](localeo-live-entree-unique.md)
