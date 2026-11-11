# Specification backend et API - Localeo Live

## Messages organisateur — catégorie Animations, correction du 11 novembre 2026

`categories_activees.ANIMATION` dans les préférences d’installation devient le
réglage commun pour les messages organisateur des participations prouvées.
Au dépôt, au moins une installation active liée et autorisée est nécessaire ;
aucun abonnement Push n’est exigé pour conserver le message dans Live. Avant
chaque transport, vérifier la propre catégorie de l’installation destinataire,
sa liaison, son accès personnel et un abonnement actif avec endpoint.
Les anciennes préférences par animation sont historiques : lecture dépréciée
avec `mode_gestion=CATEGORIE_ANIMATION` et `reglages_url`, ancienne commande
refusée avec 409 et orientation vers Réglages. Les reçus d’anciennes décisions
restent lisibles, sans modifier le choix global. Les messages déjà déposés
restent consultables ; absence de liaison ou retrait avant dépôt ne déclenche
pas de campagne rétroactive. La [spécification E73 et ses critères MA](../epic-73-animation-et-ou-coffrets/modules-souscriptions-import-communication.md#7-messages-organisateur-live-et-web-push)
définit les preuves, la compatibilité et les limites inchangées.

## Livraison Push sur mobile — correctif du 11 novembre 2026

Le transport des alertes Live classiques transmet un TTL explicite de
86 400 secondes au fournisseur, afin de permettre une livraison différée si
le téléphone est temporairement injoignable. Le statut `ENVOYE` constate
l’acceptation fournisseur, sans garantir l’affichage sur l’appareil.

Pour les rappels personnels, la politique du domaine `animation_locale`
calcule les secondes entières restantes avant 20 h Paris et la première fin
d’animation des candidats retenus. L’application relit l’horloge après
revalidation ; un budget nul annule l’envoi. Le transport utilise la durée de
la dernière revalidation de chaque abonnement. Les consentements, créneaux,
quotas et contrôles d’accès existants restent applicables.

Il s’agit d’un contrat interne application/transport : aucun champ public ni
schéma de données nouveau. La durée limite la conservation fournisseur, pas
l’heure absolue d’affichage. Le circuit distinct des campagnes organisateur
conserve son TTL de 24 heures et sa programmation propre ; voir la
[procédure de diagnostic](../../exploitation/technique/reprendre-notifications-sortantes.md#localeo-live-installé-sur-un-téléphone).

## Récompenses personnelles et tirages qualifiés — 3 novembre 2026

Deux lectures complètent le carnet, avec `X-Localeo-Live-Secret`, une
installation active et les mêmes suivis de participation valides que le tableau
de bord : token participant non expiré, non révoqué, participant non anonymisé.
Une installation ne donne aucun droit sur les participations d'une autre.

- `GET /public/localeo-live/installations/{installation_id}/recompenses`
  rassemble les gains coffrets, bons numériques et lots libres issus des
  tirages réalisés ou confirmés, y compris l'historique des remises et
  consommations. Les suppléants non promus restent exclus.
- `GET /public/localeo-live/installations/{installation_id}/tirages-a-venir`
  retourne les participations qualifiées par le moteur dans les animations
  publiées, en cours ou clôturées, avec dotation et sans tirage déjà réalisé,
  confirmé ou annulé. La progression visuelle seule ne prouve pas cette
  qualification.

Les réponses sont privées (`Cache-Control: private, no-store`) et ne contiennent
ni token personnel, ni QR, ni identité civile. Leur enveloppe contient
`generated_at`, `items`, `next_cursor` et `incomplet`. `page_size` vaut 25 par
défaut, de 1 à 50. Les curseurs sont liés à la liste et à l'installation ; les
curseurs malformés sont refusés avec `CURSEUR_INVALIDE`.

Les récompenses sont triées globalement en SQL : groupe `DISPONIBLE` avant
`HISTORIQUE`, puis attribution récente et identifiant stable. `etat` distingue
`A_UTILISER`, `A_ACTIVER`, `A_RETIRER`, `EN_PREPARATION`, `A_VERIFIER`, `UTILISE`,
`REMIS`, `EXPIRE`, `ANNULE`, `REMPLACE` et `NON_REMIS`. Le groupe est une priorité
d'affichage, pas une autorisation de consommation : un coffret en préparation
ou un état à vérifier n'est pas présenté comme utilisable. Un coffret partiellement
consommé reste `ACTIVE`/`A_UTILISER` ; `UTILISE` n'apparaît qu'après consommation
complète. Une remise libre déclarée et un refus explicite rejoignent l'historique.
Les bons utilisent la consommation effective, sa correction et leur expiration.

Chaque récompense porte `id`, `nature`, `libelle`, `animation_id`,
`animation_nom`, `participation_id`, `etat`, `groupe`, `attributed_at`,
`expires_at`, `coffret_instance_id`, `bon_id`, `consignes`,
`responsable_remise` et un `deeplink` vers sa participation. Ouvrir/utiliser le
lot conserve les contrôles et capacités personnelles existants.

Chaque tirage à venir porte `participation_id`, `animation_id`, `animation_nom`,
`commune`, `qualifie: true`, `date_fin_animation`, `date_tirage` (instant UTC ou null) et
`deeplink`. La date provient uniquement de l'annonce enregistrée par l'organisateur.
Sans annonce, afficher « Date à annoncer » ; la fin d'animation n'est pas une date de tirage. La page
borne les candidats avant qualification : elle peut être vide avec un curseur
suivant. Le client conserve alors l'action de chargement de la suite. Les
compteurs des cartes chargées ne sont pas des totaux globaux.

Producteur : `ServiceRecompensesLive` et `RecompensesLiveRepository` ; schémas
fermés `RecompensesLivePayload` et `TiragesAVenirLivePayload` exposés dans
[OpenAPI Live](openapi.json). Consommateur : page « Mes lots » de Localeo Live.

## Audit habitant — continuité et messages, 3 novembre 2026

Les deux listes de lots acceptent `participation_id` optionnel. Le filtre est
appliqué en stockage après vérification des suivis et avant pagination ; il ne
donne aucun accès supplémentaire. Le curseur appartient aussi à ce filtre.

`GET /public/localeo-live/installations/{installation_id}/messages` ajoute
`unread_count`, total global exact des messages accessibles non lus, indépendant
de `limit`, `cursor`, `unread_only` et `animation_id`. Ces deux derniers filtres
sont optionnels ; ils s'appliquent avant les limites de chaque branche SQL. Les
compteurs sont calculés par agrégats SQL, jamais en chargeant l'historique côté
application. Chaque item expose `animation_id`, `animation_nom`,
`participation_id` lorsqu'ils sont connus et `importance` (`NORMAL`, `IMPORTANT`,
`URGENT`). Ouvrir la messagerie ne marque rien comme lu : seule la commande de
lecture existante modifie cet état.

Une campagne organisateur peut choisir les destinations `PARTICIPATION` ou
`MES_LOTS`, en plus des destinations existantes. Le domaine accepte uniquement
ces valeurs fermées. Après contrôle de l'audience, des accords et des capacités,
le worker construit le lien personnel vers `/live/animations?participation=…`
ou `/live/lots?participation=…`. Aucun token n'est inséré dans le message.
L'importance est explicitement choisie par l'organisateur et figée avec le
contenu au départ de campagne ; elle ne contourne ni accord ni fréquence.

Le détail personnel et les items du tableau de bord portent `resultat_tirage` :
`statut`, `realise_at`, `date_prevue`. Les statuts possibles sont `SANS_TIRAGE`,
`NON_QUALIFIE`, `EN_ATTENTE`, `GAGNANT`, `NON_GAGNANT`, `REMPLACE`, `ANNULE`.
`NON_GAGNANT` exige un tirage confirmé/réalisé et l'appartenance à sa population
figée. L'absence de gain, une date passée ou un compteur visuel ne suffisent pas.
La lecture groupée utilise deux requêtes de faits pour au plus 50 participations,
puis une lecture des dates annoncées ; aucune requête par carte.

L'annonce est gérée par `GET/PUT …/animation-locale/animations/{id}/tirage-annonce`
sur les surfaces `/protected` (Animation) et `/internal` (ERP). La commande
demande `expected_version`, `date_prevue` avec offset ou null pour retirer
l'annonce, et `Idempotency-Key`. Elle vérifie les droits courants, le tenant,
le verrou d'animation et la version avant écriture/audit. La date doit être future
et au moins égale à la fin effective de l'animation ; un résultat déjà confirmé
ou une annulation interdit la modification. La version initiale est 0. Cette
annonce informative ne déclenche ni tirage automatique ni notification.

La migration backend `v287_e73_live_audit.sql` précède les lecteurs : importance
des campagnes et table `animation_tirages_annonces`. Les annonces sont incluses
dans l'export d'organisation et dans le registre de sauvegarde/restauration de
démonstration. La conservation suit la famille des métadonnées d'animation.
Aucune migration des participations existantes, aucun compte habitant ni
nouvelle base de participations ; seule la migration additive v287 est requise.

L'évolution du 30 octobre 2026
[E73-EVO-LIVE-ACCUEIL-RAPPELS](../epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-30-octobre-2026--e73-evo-live-accueil-rappels)
ajoute une lecture privée de tableau de bord, des préférences opt-in et des
rappels personnels dédupliqués. Les contrats générés sont dans
[OpenAPI Live](openapi.json) ; les états historiques décrits ici ne prouvent
pas l'activation de ces nouveaux traitements.

> Consolidation des exemplaires `localeo-backend` et `localeo-marketplace`.
> Le socle backend conserve les compléments absents de l'ancienne copie Marketplace :
> installation indépendante du Push, façade participation, actualités Animation,
> protection des QR et propositions de carnet partagé selon le document concerné.
> Les statuts « validé » et « à valider » des arbitrages sont conservés ; cette fusion
> documentaire ne constitue ni une nouvelle validation métier ni une preuve de déploiement.

> Statut d'implementation : lots backend B0 a B8 termines. Le contrat genere est disponible dans [Contrat OpenAPI EPIC 42](openapi.json) et se regenere avec `@localeo-backend/scripts/documentation/generate_epic42_openapi.py`.

> Evolution de conception : la persistance et le partage multi-appareils du carnet sont specifies separement dans [Spécification du carnet partagé](carnet-partage-backend.md). Les contrats B9 a B11 ne sont pas encore ajoutes a l'OpenAPI tant que les arbitrages `LIVE-ARB-41` a `LIVE-ARB-51` ne sont pas valides.

## 1. Architecture cible

Le domaine d'experience `localeo_live` compose les domaines existants sans reprendre leur responsabilite metier :

- `referencement` pour communes et commercants ;
- `commercialisation` pour les catalogues de coffrets ;
- `gestion_achats` pour les achats et coffrets instances ;
- `animation_locale` pour animations, inscriptions et participations ;
- `exploitation` pour outbox et diffusion WebPush ;
- stockage local PWA pour la bibliotheque de liens personnels, sans profil serveur au MVP ;
- `support` pour les demandes d'aide.

Les chemins suivent `/{exposition}/{domaine}/{ressource}`. Les lectures restent sous les domaines proprietaires et les ressources personnelles sont resolues par un token opaque porte par le lien.

## 2. Acces sans compte

Le MVP ne cree aucun compte client et aucune session personnelle. Un coffret est accessible avec son token de consultation ; une participation est accessible avec son token participant. La PWA peut sauvegarder ces liens uniquement sur l'appareil, dans une bibliotheque locale que l'utilisateur peut consulter et supprimer.

Le backend ne recoit jamais la liste complete de cette bibliotheque. Les tokens sont envoyes uniquement au contrat qui les resout, ne sont places ni dans les journaux ni dans les analytics ou payloads WebPush, et ne sont pas caches durablement par le service worker. Le lien magique et la synchronisation multi-appareils sont reportes apres le MVP.

Les emails transactionnels destines aux beneficiaires de coffrets et aux participants Animation comportent un pied Localeo Live commun en HTML et en texte. Le lien profond de la ressource est privilegie lorsqu'un token valide est disponible ; sinon le lien ouvre `LOCALEO_FRONT_LIVE_URL`. Les emails commerçants, partenaires, finance et support ne sont pas enrichis automatiquement.

Pour une notification transactionnelle personnelle, l'utilisateur active explicitement le suivi d'une ressource apres resolution valide de son token. Le backend conserve l'association entre l'installation et l'identifiant interne de la ressource, mais ni le token brut ni le contenu complet de la bibliotheque locale.

L'ajout depuis la vue detaillee du coffret ne requiert pas de nouvelle API backend : la PWA reutilise la projection passeport et, uniquement si l'utilisateur active ensuite le suivi, le contrat d'association installation-ressource. Le transfert `sessionStorage` ou fragment reste une responsabilite frontend et le token brut n'est jamais envoye a l'API de suivi apres sa verification.

## 3. Catalogue des contrats

### 3.1 APIs a reutiliser

| ID | Contrat/capacite | Usage Localeo Live |
| --- | --- | --- |
| LIVE-REU-01 | `GET /public/referencement/villes` | Choix de commune et contexte local. |
| LIVE-REU-02 | `GET /public/referencement/commercants` et `/{id}` | Nouveaux commercants et fiches publiques. |
| LIVE-REU-03 | `GET /public/commercialisation/coffrets` et `/{id}` | Nouveaux coffrets et catalogue. |
| LIVE-REU-04 | Consultation securisee d'un coffret instance | Detail, QR, solde et prestations du passeport. |
| LIVE-REU-05 | APIs publiques `animation_locale` | Detail d'une animation et inscription sans compte. |
| LIVE-REU-06 | Progression participant par token | Suivi ponctuel d'une participation sans profil. |
| LIVE-REU-07 | DAM/documentaire | Visuels editoriaux, coffrets, commercants et animations. |
| LIVE-REU-08 | Outbox et batch WebPush | Diffusion fiable, reprise et supervision technique. |

### 3.2 APIs a faire evoluer

| ID | Domaine | Evolution | Priorite |
| --- | --- | --- | --- |
| LIVE-EVO-01 | `gestion_achats` | Enrichir la consultation par token avec une projection passeport graphique. | P0 |
| LIVE-EVO-02 | `animation_locale` | Lister les animations publiques en cours et retourner le lien/token participant apres inscription. | P0 |
| LIVE-EVO-04 | `exploitation` | Creer un canal WebPush grand public et ses categories, distinct du canal Control. | P0 |
| LIVE-EVO-05 | `activites_locales` | Ajouter activites manuelles, programmation et scope global ou multi-villes, sans nouveau referentiel Commune. | P0 |
| LIVE-EVO-06 | `referencement` et `commercialisation` | Alimenter les types existants `COMMERCANT_ACTIVE` et `COFFRET_ACTIVE`. | P1 |
| LIVE-EVO-07 | marketplace | Ajouter bannieres d'installation, deep links et detection PWA installee. | P0 |
| LIVE-EVO-08 | `support` | Permettre une demande contextualisee par coffret, animation ou notification. | P1 |
| LIVE-EVO-09 | `activites_locales` + `animation_locale` | Ajouter `animation_id`, le type `ACTUALITE_ANIMATION`, la projection Animation et la diffusion par la categorie `ANIMATION`, sans nouveau moteur editorial. | P0 |

### 3.3 APIs a implementer

| ID | Methode et chemin cible | Description | Priorite |
| --- | --- | --- | --- |
| LIVE-API-001 | `GET /public/exploitation/activites-locales` | Reutiliser le feed marketplace, filtre par ville, type et scope. | P0 |
| LIVE-API-001A | `type_activite=COFFRET|COMMERCANT|ANIMATION|NEWS` | Les categories fonctionnelles du filtre sont traduites vers les types techniques du feed (`COFFRET_ACTIVE`, `COMMERCANT_ACTIVE`, `ANIMATION_PUBLIEE`, `ACTUALITE_ANIMATION`, etc.) ; les types techniques restent acceptes directement. | P0 |
| LIVE-API-002 | `GET /public/exploitation/activites-locales/{activite_id}` | Detail partageable d'une activite ou news manuelle. | P1 |
| LIVE-API-003 | `POST /internal/exploitation/activites-locales` | Creer manuellement une actualite globale ou scopee sur une ou plusieurs villes existantes. | P0 |
| LIVE-API-004 | `PATCH /internal/exploitation/activites-locales/{activite_id}` | Modifier contenu, programmation, visibilite et communes. | P0 |
| LIVE-API-005 | `GET /public/exploitation/activites-locales?type_activite=ANIMATION` | Retourner publications d'animation et annonces de publication dans le filtre fonctionnel `Animations`. | P0 |
| LIVE-API-009 | `GET /public/animation-locale/animations` | Animations publiees, ouvertes ou en cours, filtrables par commune. | P0 |
| LIVE-API-010 | `GET /public/localeo-live/coffrets/{coffret_instance_id}/passeport` avec token Bearer | Projection passeport, progression et prochaines prestations, sans token dans l'URL. | P0 |
| LIVE-API-011 | `POST /public/animation-locale/animations/{animation_id}/inscriptions` | Inscription sans compte et retour obligatoire du `participant_url`. La creation renvoie `201 CONFIRMEE`. Toute nouvelle soumission avec le meme email normalise est refusee en `409 Conflict`, sans nouveau token ni renvoi du QR. | P0 |
| LIVE-API-012 | `GET /public/animation-locale/participants/{token}` | Detail, QR participant, progression, qualification et gain. | P0 |
| LIVE-API-013 | `GET /public/localeo-live/installations/{installation_id}/preferences` | Preferences du navigateur, protegees par un secret d'installation. | P0 |
| LIVE-API-013A | `POST /public/localeo-live/installations` | Creer l'identite technique locale et retourner son secret une seule fois, sans activer WebPush. | P0 |
| LIVE-API-014 | `PUT /public/localeo-live/installations/{installation_id}/preferences` | Remplacer categories et identifiants de villes suivies. | P0 |
| LIVE-API-015 | `POST /public/localeo-live/abonnements-webpush` | Enregistrer abonnement, installation et preferences sans compte. | P0 |
| LIVE-API-016 | `DELETE /public/localeo-live/abonnements-webpush/{abonnement_id}` | Revoquer avec le secret d'installation. | P0 |
| LIVE-API-017 | `POST /public/localeo-live/installations/{installation_id}/suivis` | Apres verification d'un token, suivre un coffret ou une participation sur cette installation. | P0 |
| LIVE-API-018 | `DELETE /public/localeo-live/installations/{installation_id}/suivis/{suivi_id}` | Arreter le suivi d'une ressource avec le secret d'installation. | P0 |
| LIVE-API-019 | `GET /public/localeo-live/installations/{installation_id}/notifications` | Inbox transactionnelle paginee, accessible avec le secret d'installation. | P0 |
| LIVE-API-020 | `POST /public/localeo-live/installations/{installation_id}/notifications/{notification_id}/lecture` | Marquer une notification comme lue de facon idempotente. | P1 |
| LIVE-API-021 | `POST /public/localeo-live/installations/{installation_id}/notifications/lecture-globale` | Marquer toute l'inbox de l'installation comme lue. | P1 |
| LIVE-API-022 | `GET /public/localeo-live/participations/{participation_id}` | Projection d'une participation et de sa progression, protegee par Bearer token. | P0 |
| LIVE-API-023 | `GET /public/localeo-live/participations/{participation_id}/qrcode` | QR de participation sans token dans l'URL, protege par Bearer token et non cache. | P0 |
| LIVE-API-024 | `GET /public/localeo-live/installations/{installation_id}/animations` | Catalogue personnalise protege par le secret d'installation. Chaque animation expose `est_inscrit`, `participation_id`, `participation_statut` et `dans_carnet`. | P0 |
| LIVE-API-025 | `GET /public/localeo-live/installations/{installation_id}/animations/{animation_id}` | Detail personnalise d'une animation avec les memes informations d'inscription. | P0 |

## 4. Categories d'evenements

- types existants du feed : `COMMERCANT_ACTIVE`, `COFFRET_ACTIVE`, `PRESTATION_COFFRET_ACTIVE`, `COFFRET_POPULAIRE` et autres types publies ;
- nouveaux types : `ANIMATION_PUBLIEE`, `ACTUALITE_EDITORIALE` et `ACTUALITE_ANIMATION` ;
- `COFFRET_ACTIVE`, `COFFRET_BIENTOT_EXPIRE`, `PRESTATION_VALIDEE` ;
- `ANIMATION_INSCRIPTION_CONFIRMEE`, `ANIMATION_ETAPE_VALIDEE`, `ANIMATION_RESULTAT`, `GAIN_DISPONIBLE`.

`ACTUALITE_EDITORIALE` est creee manuellement. Elle porte zero, une ou plusieurs villes du referentiel existant ; zero signifie une publication globale.

`ACTUALITE_ANIMATION` est creee depuis Localeo Animation. Elle porte obligatoirement `animation_id`, herite de la ville de l'animation, apparait sous le filtre `ANIMATION` et utilise cette meme categorie de preference pour l'inbox et le WebPush.

## 5. Regles non fonctionnelles

- pagination par curseur du feed et des notifications ;
- `ETag`/`If-None-Match` sur les lectures publiques et synchronisables ;
- idempotence sur inscriptions, rattachements, lectures et abonnements push ;
- rate limiting sur inscription, resolution de token et gestion des abonnements ;
- deep links en HTTPS sur une origine publique configurable ;
- payload push sans PII, contenant seulement categorie, libelle sobre et URL autorisee ;
- suppression automatique des abonnements WebPush invalides ;
- journalisation correlee et metriques d'envoi sans token ni contenu personnel ;
- objectifs indicatifs : p95 lecture 500 ms, commandes 800 ms hors traitement asynchrone.

## 5.1 Decisions techniques validees

- les tokens coffret et participant existants sont reutilises sans conversion ;
- un token invalide, expire ou revoque produit un etat explicite et n'est jamais renouvele automatiquement ;
- l'installation WebPush utilise un identifiant opaque et un secret rotatif non recuperable apres effacement local ;
- le suivi transactionnel conserve uniquement l'association installation-ressource verifiee ;
- apres une inscription, Localeo Live rattache la participation a l'installation par `POST .../suivis` avec le type `PARTICIPATION` et le token participant ; ce rattachement est idempotent et le token est valide avant association ;
- le catalogue et le detail personnalises ne sont jamais mis en cache publiquement : `est_inscrit` signale une participation valide connue de l'installation, `participation_id` permet d'ouvrir son detail, `participation_statut` en expose l'etat et `dans_carnet` signale le rattachement a l'appareil ;
- une participation anonymisee peut rester rattachee au carnet, mais elle retourne `est_inscrit=false` et aucun `participation_id` exploitable ;
- les actualites manuelles suivent `BROUILLON`, `PROGRAMMEE`, `PUBLIEE`, `MASQUEE`, `EXPIREE` ;
- les actualites globales n'ont aucune ville et les actualites ciblees utilisent `activites_locales_villes`, relation plusieurs-a-plusieurs vers `villes` ; `ville_id` reste disponible pour les activites metier mono-ville ;
- l'inbox transactionnelle est conservee cote backend par installation ;
- les installations inactives, abonnements revoques et notifications techniques sont conserves 90 jours ; les activites conservent les durees de l'Epic 16 ;
- les publications editoriales sont gerees exclusivement depuis le backend/back-office ;
- les publications d'animation reutilisent le cycle editorial mais sont gerees depuis la fiche Animation sous controle du tenant et de `animation:gerer_actualites` ; leur cle de notification est `ACTUALITE_ANIMATION:{actualite_id}`.

## 6. Donnees principales

- `ActiviteLocale` et relation `activites_locales_villes` : contenu manuel, programmation, visibilite et scopes vers le referentiel `villes` existant ; `animation_id` rattache optionnellement une publication au domaine Animation ;
- `InstallationLive` : identifiant opaque, secret de gestion, preferences et dates techniques, sans profil client ;
- `SuiviRessourceInstallationLive` : installation, type et identifiant interne de ressource verifies, sans token brut ;
- bibliotheque de liens coffrets/participations : donnee exclusivement locale au navigateur ;
- `PreferenceNotificationLive` : categories et territoires suivis par installation ;
- la categorie canonique des actualites est `ACTUALITE_EDITORIALE`; les alias entrants `EDITORIAL`, `ACTUALITE` et `ACTUALITES` sont normalises pour compatibilite avec les premiers clients ;
- `AbonnementWebPushLive` et `NotificationLiveSortante` : endpoint, statut, tentatives et deeplink.

## 7. OpenAPI et erreurs

Une vue OpenAPI 3.1 dediee doit maintenant etre initialisee. Elle couvre les schemas, exemples, erreurs standard, regles d'idempotence et identifiants de correlation. Elle reutilise les erreurs `400`, `401`, `403`, `404`, `409`, `422`, `429` et `503`. Aucun contrat ne doit exposer directement un modele ORM.
