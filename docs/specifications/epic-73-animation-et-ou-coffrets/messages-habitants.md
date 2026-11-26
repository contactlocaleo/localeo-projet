# E73 — Messages habitants

Évolution **E73-EVO-MESSAGES-HABITANTS**, demandée le **15 novembre 2026**.
Elle prolonge les parcours Animation/Live de l'epic 73, sans modifier sa clôture
historique ni les critères des campagnes organisateur. Le
[backlog E73](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md)
porte le rattachement ; les critères nouveaux **MH-01 à MH-15** sont ci-dessous.

## Besoin et décisions

Un habitant inscrit à une animation peut contacter son organisateur depuis sa
participation Live, en indiquant un motif et un message. L'organisateur retrouve
ces échanges dans **Messages habitants**, depuis l'animation ou depuis l'entrée
globale de **Suivre l'activité**, et répond dans le même fil.

Choix utilisateur confirmés le 15 novembre : **plusieurs échanges dans un fil** ;
**réponses dans Live avec indicateur non lu, sans email**. La réponse est un
service sollicité par un participant, indépendant du module payant Communication,
de ses quotas et des préférences de campagnes/Push. Aucun email, SMS ou Push n'est
créé par cette évolution. Les nouvelles collectives et le support de l'organisateur
auprès de Localeo conservent leurs parcours propres.

Motifs V1 : `QUESTION_JEU` (« Question sur le jeu »), `PROBLEME_PARCOURS`
(« Problème pendant le jeu »), `LOT_REMISE` (« Lot ou remise »), `AUTRE`
(« Autre demande »). Le motif est obligatoire et fixé à la création du fil.
Chaque message contient du texte simple non vide, de 1 à 4 000 caractères après
trim ; aucune pièce jointe, HTML actif, édition ou suppression de message en V1.
Le serveur fixe l'auteur et l'instant. Aucun correcteur, qualification ou lot
n'est modifié en réponse à un échange.

## Existant vérifié et écart

Sources locales au début du travail : projet `1759c67` avec la spécification E78
non commitée à préserver ; backend `b417e631`, Animation `9e81844d`, Marketplace
`59c69bd6`. Les quatre applications étaient propres. Ces constats ne décrivent
pas un environnement déployé.

| Source | Existant et adaptation |
| --- | --- |
| Backend `services/participants_animation.py` et `preferences_messages_organisateur.py` | Résolution de preuve personnelle, participant non anonymisé et recontrôle transactionnel réutilisables |
| Backend `communication/`, `services/commandes_idempotentes.py` et autorisations Animation | Nouveau domaine de conversation ; même protocole reçu/effet atomique et session/commune courantes |
| Backend `models_messages_organisateur.py` | Les messages descendants exigent une campagne et une préférence ; aucune conversation à détourner |
| Animation `App.tsx`, `AnimationDetailNavigation.tsx`, `OrganizerSupportWorkspace.tsx` | Navigation et patron liste/fil disponibles ; nouveau composant partagé entre entrée globale et animation |
| Marketplace `LiveAnimationGame.jsx`, `LiveParticipationMessages.jsx` | Point commun aux moteurs ; ajouter une section personnelle de conversations avec badge non lu |
| Live `LiveMessages.jsx` et `useLiveMessages.jsx` | Nouvelles collectives conservées ; avis de réponse personnelle sans contenu privé dans la messagerie unifiée et les compteurs d'animation |

## Parcours et règles

### Habitant

Depuis la participation, l'action secondaire **Contacter l'organisateur** ouvre
le formulaire motif/message. **Mes échanges avec l'organisateur** permet de
retrouver les fils de cette participation, y compris sur un autre appareil après
récupération de son accès. Deux participations à la même animation restent
distinctes ; l'animation seule ou une installation Live ne prouve aucun accès.

Le formulaire indique l'animation et l'organisateur. Annuler n'envoie rien.
Après enregistrement confirmé, ouvrir le fil ; après erreur, préserver la saisie.
Un résultat réseau incertain propose **Vérifier l'envoi**, puis seulement si le
reçu est absent une relance explicite de la même intention et de la même clé.
Ne jamais renvoyer automatiquement ni produire un second fil au rechargement.
Les brouillons et intentions restent en mémoire de l'onglet, purgés au changement
de participation/identité ; aucun texte privé dans carnet, localStorage ou cache PWA.

Les messages sont datés, avec auteur **Vous** ou **L'organisateur**. Le fil garde
le motif initial et un formulaire de réponse. L'habitant voit un indicateur de
réponse non lue fondé sur le serveur. Afficher la liste ne marque rien comme lu.
Après affichage effectif du fil, acquitter explicitement le dernier numéro de
message organisateur réellement affiché ; une réponse arrivée après ce numéro
reste non lue. La lecture ne marque jamais la demande comme traitée.

Chaque réponse organisateur apparaît aussi dans **Messages** de Localeo Live,
avec un avis « L’organisateur vous a répondu », le nom de l'animation et une
action **Lire la réponse**. Le compteur existant de la vignette d'animation dans
**Mon carnet** inclut ces réponses non lues et ouvre les messages de l'animation.
L'avis ouvre la participation exacte puis son fil ; deux participations à la
même animation conservent leurs accès distincts. Ni le texte privé, ni le motif,
ni le nom de l'habitant ne sont recopiés dans l'avis ou le stockage du carnet.
La liaison personnelle valide de l'installation est requise pour l'avis ; une
installation seule, une preuve révoquée/expirée ou un participant anonymisé
n'accorde aucun accès. Les préférences de campagnes et le Push restent indépendants.
Ouvrir la messagerie, filtrer ou consulter un avis ne l'acquitte pas. L'action
globale de lecture conserve les réponses privées pour leur lecture dans le fil.
L'acquittement personnel confirme les numéros affichés puis actualise le badge
Messages et le compteur de vignette ; une réponse plus récente reste non lue.

L'accès et l'écriture restent possibles après clôture, fin ou archivage, tant que
la preuve personnelle et les données de participation sont valides. Le gel du
jeu n'est pas un gel de l'assistance, notamment pour une question sur un lot.
Une preuve expirée/révoquée, une participation anonymisée ou étrangère produit
un refus explicite ; proposer la récupération existante lorsque pertinente.

### Organisateur

**Suivre l'activité → Messages habitants** regroupe les conversations de
l'organisation et de la commune actives. Ce n'est pas une boîte interorganisations
ou multicommunale. Dans une animation, **Communiquer → Messages habitants** ouvre
le même composant avec filtre d'animation imposé, y compris pour une édition
terminée/archivée. Les données et le brouillon ne suivent pas un changement de
commune, d'organisation ou de session.

La liste paginée propose **À traiter / Répondus / Tous** et le motif. La boîte
globale propose le [filtre Animations de Suivre l’activité](ux-productivite-organisateur.md#évolution-du-26-novembre-2026--filtre-des-animations-dans-suivre-lactivité)
et la sélection d'une édition par nom. Chaque ligne
montre animation, participant identifié sans adresse email, motif, dernière
activité et état. Le détail rend le contexte visible avant le formulaire.
Les pages/retours/filtres sont conservés en mémoire ; les messages restent privés.

| Événement | État du fil et effets |
| --- | --- |
| Création ou nouveau message habitant | `A_TRAITER`, version suivante |
| Réponse organisateur confirmée | `REPONDU`, version suivante, réponse non lue par l'habitant |
| Simple ouverture/lecture | État de traitement inchangé ; seul le repère personnel de lecture peut avancer |
| Deux réponses à la même version | Une confirmée, l'autre en conflit ; recharger le fil et préserver le texte avant décision explicite |
| Répétition d'une commande confirmée | Même résultat ; aucun message ou fil supplémentaire |

Le lecteur consulte ; seul le gestionnaire disposant de `animation:modifier`
répond. Le backend fournit `allowedActions`, sans déduire l'autorisation du seul
statut de l'animation. Le droit payant `COMMUNICATION` n'est pas requis.
Pas d'assignation, de SLA, de classement manuel, de clôture de dossier ou d'envoi
collectif ajouté. Répondre constitue le traitement demandé.

### Présentation et accessibilité

Appliquer [LIVE-UX-01/02/05/07/08/09](../../produit/live/principes-ux.md) :
accès secondaire depuis la participation, progression principale conservée,
retour au bon objet, badge textuel accessible et aucun nouvel onglet de navigation
basse. Préserver un en-tête stable pendant chargement/actualisation.

Animation applique les [règles de gestion](../../architecture/transverse/conventions-backoffice.md#ux-des-pages-de-gestion-erp)
ERP-UX-01/02/04/05/07/08/09/10/11/12 : liste comparable, fiche puis action,
lecture seule explicite, résultat confirmé/incertain, filtres conservés et
protection des saisies. Prévoir 320/390/1280 px, texte 200 %, cibles 44 px,
clavier/focus, annonces de réponse/erreur, motifs nommés et messages longs échappés.

## Domaine, contrats et données

La racine `ConversationHabitant`, dans `animation_locale.communication`, porte
motif, identité de participation/animation, état, version et derniers numéros.
Elle valide le texte, les transitions et les versions ; elle ne charge pas tout
l'historique. Les messages immuables et le marqueur de lecture sont persistés
séparément ou par champs scalaires bornés. L'application autorise, orchestre la
transaction, appelle le domaine, persiste et audite ; les routes/clients ne
recalculent pas le traitement ou l'identité.

Contrats cibles partagés avant implémentation :

| Objet | Champs |
| --- | --- |
| Résumé de conversation | `id`, `organisationId`, `communeId`, `animationId`, `animationTitle`, `participantId`, `participantLabel`, `motif`, `statut`, `version`, `createdAt`, `updatedAt`, `dernierMessage` (aperçu borné), `nonLu`, `allowedActions` |
| Message | `id`, `numero`, `auteur` HABITANT/ORGANISATEUR, `texte`, `createdAt` ; pas d'email ni d'identifiant interne d'agent exposé à l'habitant |
| Page | `items`, `nextCursor` nullable, `hasMore` ; conversations et messages séparément paginés ; `hasUnread` sur la page personnelle, calculé sur tous ses fils par un EXISTS indexé, pas seulement les 25 rendus |
| Création | `{motif, message}` ; participant et animation issus de l'accès personnel |
| Réponse | `{message, expected_version}` ; auteur issu de l'accès, jamais du corps |
| Acquittement habitant | `{numero}` du message réellement affiché, monotone et borné à un numéro existant |
| Résultat de commande | `conversationId`, `messageId`, `version` ; pas de texte privé recopié dans le reçu |
| Reçu | `status: CONFIRMEE` avec `result`, `EN_COURS` ou `COMMANDE_NON_ENREGISTREE`, protocole commun |

Routes personnelles, sous `/public/localeo-live/participations/{participation_id}`
avec Bearer personnel et `Cache-Control: no-store` :

- GET/POST `/conversations` : liste ou création ; GET `/conversations/commandes/{cle}`.
- GET `/conversations/{id}` et GET `/conversations/{id}/messages` : détail et historique.
- POST `/conversations/{id}/messages` : réponse ; GET `/conversations/{id}/commandes/{cle}`.
- POST `/conversations/{id}/lecture` : repère personnel, idempotent par maximum du numéro.

Routes organisateur, sous `/protected/animation-locale/messages-habitants`,
cookie/CSRF et contexte de session : GET liste, GET `/{id}`, GET `/{id}/messages`,
POST `/{id}/messages`, GET `/{id}/commandes/{cle}`. Filtres `animation_id`,
`statut`, `motif`, `limit`, `cursor`. Aucune création de fil par l'organisateur.
Les commandes de création/réponse exigent `Idempotency-Key` (8..128 caractères).
Corps borné à 16 Kio, DTO stricts et erreurs sans copie du message/token.
Prévoir 401/410 accès invalide, 403 droit absent, 404 cible hors périmètre,
409 version/intention en conflit, 422 saisie, 413 taille, 429 débit, 503 indisponibilité.

La messagerie unifiée `/public/localeo-live/installations/{installation_id}/messages`
ajoute la nature de sortie `CONVERSATION` : un avis par message organisateur,
identifié par ce message immuable, avec les références animation/participation et
un lien vers le fil exact. `lue` est le booléen issu du repère numérique personnel ;
`lue_at` reste nul car aucune date d'acquittement n'est persistée pour le fil.
Le texte de réponse et le motif restent dans l'API personnelle. La pagination,
les filtres d'animation/non-lus, le total non lu et l'indicateur d'animation
incluent les avis. Le compteur `nouvelles_non_lues` du tableau de bord utilise
les mêmes preuves. La route de lecture générique continue de refuser cette
nature : seul l'acquittement personnel par numéro confirme sa lecture.

Sur écriture, conserver l'ordre de coordination commun : fermeture organisation
et autorisations organisateur si concernées, animation partagée, participant,
conversation. Revalider accès/session après attente des verrous. État, message,
repère non lu, audit et reçu sont atomiques. Même clé avec autre contenu : conflit.
Une lecture ou un envoi d'une réponse tardive d'un ancien contexte est ignoré par
les clients. L'audit contient références, type d'action, auteur, instant et version,
jamais le texte libre. Aucun transport externe n'est appelé sous verrou.

Migration additive, numéro libre vérifié au moment de l'écriture : conversations
et messages, FK cohérentes participant/animation et organisation/commune,
unicité `(conversation_id, numero)` ; index de boîte par organisation/commune/
état/activité/id, de participation/activité/id et d'historique conversation/numéro.
Le repère non lu est maintenu avec la réponse et indexé par participation ;
sa présence ne demande pas de charger tous les fils de l'habitant.
Pas de migration de campagnes ou conversion d'anciens messages Support.

Les contenus suivent la conservation de la participation : suppression des
messages/repères lors de son anonymisation ou purge autorisée, avec les mêmes
gels participant/animation/organisation et sans nouveau délai. Raccorder le
registre de conservation, le journal de non-réintroduction et les exports
d'organisation autorisés ; aucun token dans un export ou reçu. La purge et les
écritures prennent la même coordination, empêchant une réintroduction concurrente.

Producteur : DTO et routes backend ; OpenAPI canoniques E41/E42 générés par
`scripts/documentation/generate_epic41_openapi.py` et `generate_epic42_openapi.py`.
Le contrat embarqué Animation `src/imports/openapi.json` reprend l'export E41,
généré avec le chargeur isolé `export_openapi_offline.py`. Live consomme son transport API existant ; aucun
nouveau manifeste moteur n'est nécessaire. Les routes sont additives et les
anciens clients restent utilisables. Aucun impact Pro ou sur les moteurs de jeu.

## Coût et capacité

Conformément à la [convention de performance](../../architecture/transverse/performance-volumetrie.md),
les budgets ci-dessous sont des objectifs à mesurer, pas des performances acquises.

| Opération | Bornes et accès | Budget initial / preuve |
| --- | --- | --- |
| Boîte globale/personnelle | Page 25, max 100, filtre de droits avant LIMIT ; tri `(updated_at DESC,id DESC)`, curseur lié au scope/filtres ; au plus limit+1 racines | <=8 requêtes, p95 600 ms/p99 1,2 s, mémoire additionnelle <=16 Mio ; N/10N, tenants étrangers séparés |
| Fil | Derniers 25 messages, max 100, ordre numéro descendant puis rendu chronologique ; pages antérieures explicites ; pas d'historique dans résumé | <=6 requêtes, p95 600 ms/p99 1,2 s ; aucune croissance de mémoire avec l'historique |
| Création/réponse/lecture | Cible et champs bornés ; état et compteurs synchrones, pas de scan de tous les messages | <=20 requêtes, p95 800 ms/p99 1,5 s ; double clic, conflit, réseau et verrous |
| Conservation/export | Lots <=100, index participant/animation/organisation, checkpoints existants | Mémoire bornée, reprise et gels ; aucune archive en réponse HTTP synchrone |

N = 1 000 fils de 10 messages ; 10N = 10 000 fils. Faire croître séparément
l'organisation cible, les organisations étrangères et l'historique d'un fil.
Mesurer pages initiales/profondes, filtres vides/rares, requêtes/objets/plans SQL,
latences, mémoire et contention. Charge mixte cible : 20 lectures/s, 5 écritures/s,
10 sessions, pendant 5 minutes ; pointe à deux fois le débit pendant 60 secondes.
Erreurs techniques <1 %, latence à 10N <=1,5 fois N dans les budgets absolus.
429/Retry-After et 503 explicites ; pas de polling rapide ou de retry d'écriture
automatique. Un dépassement demeure un écart de capacité, sans seuil modifié après mesure.

## Critères et matrice de preuves

La matrice distingue les preuves attendues ; le bilan en fin de document
consigne leurs résultats réels et limites sur les arbres modifiés.

| Critère | Propriétaire / résultat attendu | Preuve prévue | Documentation / contrat | Démonstration / exploitation |
| --- | --- | --- | --- | --- |
| MH-01 | Participant exact : créer motif+message depuis sa participation | Nominal, sans inscription, mauvais token/participant, motif absent et texte invalide | Formulaire Live et API personnelle | Participant réel synthétique, aucun envoi externe |
| MH-02 | Domaine : fil multi-échanges immuable, motif initial stable | Habitant puis organisateur puis relance ; aucune modification du jeu | DTO fil/messages | Fil à traiter et fil répondu |
| MH-03 | Organisateur : boîte globale commune/organisation active | Autre commune/organisation, compte révoqué, filtre animation et pagination | Route globale, menu Messages habitants | Deux communes et profils gestionnaire/lecteur |
| MH-04 | Même service et écran depuis une animation | Filtre imposé, retour/focus, terminée/archivée autorisée pour assistance | Navigation contextuelle et globale | Édition en cours et terminée |
| MH-05 | Réponse confirmée → REPONDU ; nouveau message habitant → A_TRAITER | Domaine et HTTP ; ouvrir/lire ne traite pas ; lecteur ne répond pas | États et allowedActions | Pas de droit Communication requis |
| MH-06 | Non-lu habitant serveur, avis Messages Live et compteur de vignette ; acquittement du numéro affiché | Deux réponses entourant une lecture ; compteur reste non nul pour la seconde, rejet numéro étranger/futur ; avis → bon fil et refus d'accès sans lecture | Badge de participation, messagerie unifiée et lecture personnelle | Fil sans installation ni Push ; avis sur installation liée avec preuve valide |
| MH-07 | Réponse et reçu atomiques, intentions stables | Même clé rejouée, autre corps, deux versions concurrentes, perte après commit, erreur rollback | Contrats reçus et conflits | Aucun doublon après reprise |
| MH-08 | Confidentialité de bout en bout | Altération IDs, token révoqué, contexte tardif, XSS texte, cache, audit et export sans secret | DTO/no-store/CSRF/Bearer | Pas de notification générique exposant le corps |
| MH-09 | Support après fin/clôture/archivage avec accès valide | Trois états et anonymisation ; aucune réouverture de jeu | Sections terminales et refus | Accès récupéré sur autre appareil |
| MH-10 | Conservation/réversibilité cohérentes | Gels, suppression liée à anonymisation, course écriture/purge, export borné sans token | Politique de participation et procédure ops | Restauration/remappage et non-réintroduction |
| MH-11 | Listes et trafic bornés | N/10N, requêtes/plans, pages25/100 et filtre rare ; charge mixte | Budgets ci-dessus | Résultats mesurés distincts de la cible |
| MH-12 | UX mobile/gestion accessible | 320/390/1280 px, 200 %, clavier/focus, vide/erreur/attente, historique long, brouillon protégé | LIVE-UX et ERP-UX précisés | Rapports/captures isolés |
| MH-13 | Compatibilité des producteurs/consommateurs | OpenAPI E41/E42 et import Animation ; contrat HTTP et navigation existants | Générateurs et contrats canoniques | Migration avant clients, aucune activation commerciale |
| MH-14 | Démonstration représentative et rejouable | Création/réponse/lecture via services, fixtures synthétiques, sauvegarde/restauration | Guide génération et scénario canonique | Aucun email/SMS/Push ni base opérateur |
| MH-15 | Préserver campagnes, support Localeo et moteurs | Tests des parcours proches et revue indépendante des contrats/invariants | Sources canoniques liées, clôture historique E73 conservée | Résultats séparés, aucun déploiement implicite |

## Réalisation, livraison et preuves

Lots : (1) domaine, données, API, autorisations et conservation ; (2) Animation et
Live sur ces contrats ; (3) démonstration, exports de contrats, documentation,
preuves transverses et revue indépendante. Backend/migration avant clients ;
pas de nouvelle configuration de canal externe ni de module payant.

La démonstration reste dans le backend, sous son guide local : deux demandes
synthétiques, l'une à traiter, l'autre répondue/non lue puis acquittée. Une
regénération conserve des références cohérentes sans spam ni transport externe.
Diagnostic par corrélation/référence/version, sans texte libre ou preuve personnelle.
En retour arrière, conserver tables/faits et désactiver l'entrée UI concernée ;
ne pas supprimer les échanges pour revenir à un client ancien.

### Réalisation et impacts

Backend : domaine `ConversationHabitant`, service `ServiceMessagesHabitants`,
dépôt de lectures bornées et routes personnelles/organisateur. La migration
`sql/v322_messages_habitants.sql` crée les deux tables, leurs contraintes
composites et index. Son SHA-256 vérifié sur le schéma de recette et le plan
de sauvegarde/restauration est
`e2605b6ce84f674ec7790ca5681f2b94cfc737d553a287ecbffe1a6f5a642c52`.
Les contenus, reçus, audits minimaux, exports autorisés et
traitements de conservation utilisent les mécanismes ordinaires. Le nom public
de l'organisateur est ajouté optionnellement à `AnimationParticipationLive`,
avec un libellé de repli dans Live pour la coexistence des versions.

Animation : `ResidentMessagesWorkspace.tsx` est commun aux deux entrées ;
`messagesHabitantsApi.ts` contrôle le scope et les pages reçues. Live :
`LiveResidentConversations.jsx` est intégré à la participation commune aux
moteurs, avec transport personnel et marqueur de lecture explicite.

Les [consignes de traitement](../../exploitation/exploitation/traiter-messages-habitants-animation.md),
le [guide de formation Animation](../../produit/formation/animation/guide-animation-preproduction.md#répondre-aux-habitants-depuis-une-animation-ou-la-boîte-globale)
et la [configuration E73](../../exploitation/technique/configurer-epic-73.md#messages-habitants--évolution-du-15-novembre-2026)
sont actualisés. Le guide opérateur fait partie du manifeste des sources
exportées ; aucun bundle de déploiement n'est versionné dans le backend.

Sans impact sur Localeo Pro : aucun écran, jeton ou contrat commerçant n'est
consommateur de cette conversation privée. Sans impact sur les moteurs :
aucune réponse, qualification, dotation ou action de jeu n'est recalculée ;
le bloc Live est commun aux participations. Aucun canal externe, quota de
campagne, fournisseur ou nouveau délai de conservation n'est créé.

### Preuves locales du 15 novembre

Les rapports cités sont des sorties locales non versionnées. Les arbres
testés dérivent des versions indiquées au cadrage et incluent cette évolution.
Ces mesures précèdent la demande de commit/push et l'intervention TEST du
16 novembre décrite ci-dessous.

| Critères / contrôle | Résultat constaté |
| --- | --- |
| MH-01 à MH-10, MH-13/MH-15 — backend, domaine/API et architecture | Passage final : **764 tests réussis, zéro échec/skip**, `localeo-backend/tmp/messages-habitants-backend-final-statique.xml` : 13 tests du domaine/dépôt, 2 application, 10 API et 739 gardes d'architecture/couverture. |
| MH-01 à MH-10, MH-15 — PostgreSQL et parcours voisins | Passage final : **101 tests réussis, zéro échec/skip**, `tmp/messages-habitants-backend-final-fonctionnel.xml` : 23 conversations, 22 projection/QR Live, 6 progression, 18 conservation, 16 jeu Animation et 16 tirages libres. Les **23 tests conversations sont rejoués seuls avec succès après la dernière optimisation**, `tmp/messages-habitants-backend-final-pg.xml`. Inclut versions/concurrence, droits/révocations, preuve email, quatre attentes de verrous avec expiration, non-lu, rollback commun message/reçu/audit, purge T8 de l'audit et conservation du message métier. Les lots statique et fonctionnel totalisent 865 contrôles distincts ; les 23 reprises ne s'y additionnent pas. |
| MH-03/04/05/07/08/12/13 — Animation | Suite Node **351 réussites** avant revue ; **8 tests transport/contrat finaux** incluant Unicode ; types et lint réussis. Build isolé réussi puis **14 scénarios navigateur**, `localeo-animation/tmp/messages-habitants-animation-5b56yS/report.json` : 320/390/1280 px, texte 200 %, clavier/retour, filtres/pages, lecture seule, fin/archives, conflits, reçus, changement de commune, XSS échappé et 4 000 caractères Unicode. Captures inspectées. |
| MH-01/02/06/07/08/12/15 — Live | Recette finale **21 scénarios réussis, zéro échec/skip** (13 conversations, 8 continuité), `localeo-marketplace/test-results/visual-runs/2026-11-15T21-12-05-597Z-B4oDy7/results.json` ; **6 répétitions ciblées** des refus/acceptations de sortie réussies. 320/390/1280 px, texte 200 %, non-lu hors première page, course de lecture, conflit, reçu avant/après commit, changement de participation et navigation native. **12 tests Node réussis**, build isolé et ESLint `src/tests/scripts` réussis. API simulée en recette navigateur, complétée par les preuves backend. |
| MH-13 — contrats | E41 : **1 165 chemins** ; E42 : **90 chemins**. Copie Animation identique octet pour octet à E41, six chemins personnels alignés E42, trois réponses de reçu `202 EN_COURS` et `organisateur_nom` présents. Export UTF-8/LF corrigé pour Windows. |
| MH-13 — lecteurs et outils documentaires | **46 tests réussis, 2 non exécutés**, `tmp/messages-habitants-documentation-readers.xml` : lecture des guides, génération OpenAPI, préparation et contrôle du bundle. Les deux tests préexistants de liens symboliques sont ignorés par leur garde de plateforme, Windows refusant leur création ; aucune assertion ni garde n'a été modifiée. Comparaison sémantique E41 : dix chemins ajoutés, aucun chemin existant modifié ou supprimé ; seul schéma existant enrichi : `AnimationParticipationLive`. |
| MH-14 — démonstration | **31 tests unitaires démo/registre réussis**. Le scénario PostgreSQL messages passe, puis est rejoué avec succès sur la migration finale dans `tmp/messages-habitants-demo-final-retry/results.xml` : accès privé, création/réponse/lecture/rejeu, restauration des messages et du repère non lu, relance habitant remettant le fil à traiter. **Les 11 scénarios d'intégration sont couverts avec succès par le runner complet et les reprises ciblées** : neuf succès dans `tmp/mhd2/results.xml`, puis les deux scénarios restants réussis sans skip dans `tmp/messages-habitants-demo-retry2/results.xml` (359,30 s). Ces deux derniers vérifient le jeu complet, l'installation, la sauvegarde, la restauration, la reprise et le retour aux données d'origine. Le plan du cycle de vie contient l'empreinte finale de `v322` indiquée ci-dessus. |
| MH-11 — capacité | **Deux tests réussis, zéro échec/skip** ; rapports `.xml` et `.json` `tmp/messages-habitants-backend-capacite` et `tmp/messages-habitants-backend-capacite-axes`. Axes cible, périmètres étrangers et historique N/10N **sans écart** : lectures 5–6 requêtes, p95 au plus 52,1 ms ; créations/réponses organisateur/réponses habitant/lecture : **18/20/20/16 requêtes**, p95 au plus 58,9 ms. Mémoire au plus 0,73 Mio, ratio maximal 1,449. Le cas tout lu emploie l'index partiel `ix_mh_non_lu`, sans parcours du périmètre. Charge finale : **8 400 lectures et 2 100 écritures, zéro erreur**, 300,11 s au nominal puis 60,02 s à deux fois le débit ; p95/p99 lecture **194,03/229,93 ms**, écriture **231,37/260,69 ms**. Tous les budgets sont respectés sans modification de seuil. |
| Sources documentaires | **99 guides, 1 315 liens, zéro erreur/avertissement ; 151 sources exportées vérifiées** avec `check_guidance.py` et `sync_documentation.py --check-sources`. |

Le premier runner complet de démonstration (`tmp/mhd1/results.xml`) a produit
**8 échecs et 3 succès** : le nouveau scénario utilisait à tort les permissions
du moteur, qui n'incluent pas le droit ordinaire de modification Animation.
Le contexte du scénario a été corrigé pour les habilitations effectivement
provisionnées ; le test ciblé ci-dessus passe. Le second runner complet
(`tmp/mhd2/results.xml`) a produit **9 succès et 2 échecs de fixtures** :
handles hérités invalides de Git sous Windows, et QR expiré dans le scénario
de cycle de vie utilisant la date fixe de l'exemple opérateur. Une reprise
intermédiaire a confirmé le scénario messages et révélé deux préparatifs
incomplets : stderr hérité encore invalide, rendez-vous UTC refusé par la
configuration exigeant le décalage de Paris. Les corrections finales fixent
stdin à `DEVNULL`, stderr à `PIPE`, et le rendez-vous de cette recette à demain
avec `ZoneInfo("Europe/Paris")`. Les deux scénarios passent alors intégralement ;
aucune règle d'expiration, signature ou assertion n'est assouplie. La couverture
cumulée des onze scénarios est complète, sans présenter le runner antérieur
comme un passage intégral réussi.

Les mesures de capacité portent sur les services applicatifs réels et PostgreSQL,
y compris authentification métier, idempotence, audit et verrous. Elles ne
mesurent ni le serveur HTTP et son limiteur, ni le réseau ou le navigateur ;
elles ne constituent pas un débit de production. Les dix sessions organisateur
persistées sont distinctes, avec gestionnaire/participant communs pour exercer
une contention volontairement forte.

La revue indépendante a fait corriger le comptage UTF-16 d'Animation, la
revalidation datée d'habilitation après attente, la déclaration des reçus
202, le raccord de conservation des reçus et la garde de sortie Live. Une
recette Live intermédiaire (19/20) a révélé une course du retour navigateur
après refus du rechargement : le relais de garde est désormais installé
avant le routeur. Six essais ciblés répétés puis la recette complète 21/21
passent. La revue est en lecture seule, distincte des suites exécutées.
Le cache des faits d'autorisation est également renforcé pour revalider leurs
dates après les attentes de verrous du fil et du reçu ; les tests PostgreSQL
finaux couvrent ces courses et la revue ne constate plus de défaut restant.
Le dialogue de rechargement natif dépend de l'activation utilisateur du
navigateur ; aucun texte ou token n'est persisté pour contourner cette règle.

**État :** évolution implémentée et vérifiée localement : critères MH-01 à MH-15,
interfaces, contrats, capacité, démonstration et revue indépendante couverts.
Migration `v322` et backend à livrer avant les interfaces ; aucun déploiement
n'est attesté par ces preuves. Les
avertissements de bundle Animation >500 ko et de réflexion SQLAlchemy lors
des snapshots sont distingués des échecs. Aucun environnement opérateur n'a
été utilisé pour les tests ; PostgreSQL, données et accès sont jetables.
La commande globale `npm run lint` de Live rencontre une erreur EPERM
préexistante dans `output/bum-politique/pytest-approval-1` ; le contrôle
explicite de tous les répertoires source, tests et scripts passe.

### Mise à jour du schéma TEST — 16 novembre 2026

Sur demande explicite, `v322_messages_habitants.sql` est appliquée à TEST
le **16 novembre à 00 h 06 (Europe/Paris)**, après un dry-run ne désignant
que cette migration et une sauvegarde PostgreSQL complète. L'archive privée
fait 80 101 942 octets ; son inventaire `pg_restore --list` est vérifié.
Cette sauvegarde n'a pas fait l'objet d'une nouvelle restauration sur une
base distincte ; les cycles de restauration locaux sont documentés plus haut.

Les contrôles constatent le reçu et l'empreinte finale `v322`, les deux tables,
les sept index, les trois clés étrangères et les contraintes validées. Les
37 animations et 114 participations sont conservées ; les nouvelles tables
sont vides. Le dry-run final ne trouve aucune migration manquante et le
contrôle HTTP authentifié de readiness répond **200 / READY** avant et après
l'intervention. Les reçus et la sauvegarde restent dans
`localeo-backend/demonstrations/prive/messages-habitants-test-20261116/`.

Le profil documentaire exécuté lors de la préparation a détecté une structure
incomplète du nouveau guide d'exploitation. Elle est corrigée, puis les cinq
tests du référentiel de procédures, les 99 guides/1 315 liens et les 151 sources
exportées sont vérifiés avec succès. Le rapport global initial reste conservé
comme échec, distinct de cette reprise ciblée.

L'intervention vérifie la migration et la santé du schéma. Les parcours métier
distants restent à vérifier sur la nouvelle version applicative effectivement
déployée ; les commits et push ne constituent pas cette recette.

### Correctif du 16 novembre 2026 — Avis de réponse dans Live et sur la vignette

**Cause reproduite :** les réponses étaient persistées et signalées dans la
participation, mais absentes de l'union de messagerie et de ses compteurs.
Le test PostgreSQL minimal constatait **0 non-lu pour deux réponses** avant
correction. Le domaine `ConversationHabitant` reste propriétaire du repère
monotone ; la correction complète ses projections de lecture.

Chaque réponse produit désormais un avis calculé depuis son message immuable,
sans duplication de texte ni nouvel envoi externe. Messages, filtre d'animation,
indicateur et compteur de vignette utilisent la même preuve personnelle courante.
Le lien ouvre la participation et le fil exacts. L'avis reste non lu jusqu'à
l'acquittement personnel des numéros affichés ; la lecture globale l'exclut.
Le retour à la liste pendant un acquittement confirmé actualise les compteurs,
et le passage entre deux avis conserve les brouillons de fil en mémoire.

Arbres vérifiés : backend **b7bcad90**, Marketplace **585695d**, Animation
**bc2cd40**, projet **bc32cf8**, avec ce correctif local. Les changements E78
déjà présents dans le projet sont conservés.

| Vérification réellement exécutée | Résultat et limite |
| --- | --- |
| Backend, lanceur isolé : `tests/architecture`, recensements domaine/use cases, domaine/application messages habitants, tableau Live, compteur indisponible, API organisateur et contexte de notifications | **813 réussis, un échec préexistant** dans `test_marquer_lue_retourne_contexte_sans_recrire_message`. Reproduit sur le worktree HEAD backend inchangé : le double configure `session.get` alors que la route utilise `session.scalar`. Les contrôles d'architecture passent. |
| PostgreSQL 18 jetable, `test_messages_organisateur_postgres.py`, `test_messages_habitants_postgres.py`, contrats HTTP des deux messageries | **64 réussis** ; puis **38 réussis** sur messagerie, compteurs par animation, lectures d'adhésion et performance des campagnes après regroupement des agrégats SQL. Aucun skip. |
| Contrat final de lecture booléenne | Reprise du cas PostgreSQL de réponse privée : **1 réussi** ; API organisateur : **10 réussis**. `lue` exprime le repère et aucune date de lecture n'est inventée. |
| Capacité des réponses, `test_messages_organisateur_performance.py -k reponses_live` | **4 réussis** : historique propre et périmètre étranger à 1 000/10 000 réponses, deux pages de 25 sans doublon ni texte privé, **5 requêtes par page**, lectures **182,6–559,2 ms**, sous le budget de 600 ms. Plans et mesures dans `.artifacts/reponses-live-*.json`. Cette mesure locale ne constitue pas une charge HTTP ni une recette de trafic de production. |
| Live : tests Node messagerie/conversations et ESLint explicite sur `src tests scripts *.cjs *.mjs` | **10 tests réussis**, lint réussi. `npm run lint` reste bloqué par l'EPERM préexistant du dossier `output/bum-politique/pytest-approval-1`. |
| Live : Playwright `resident-conversations.spec.cjs`, build et serveur isolés | **19/19 réussis**, dont 320/390/1280 px, refus, lecture retardée, brouillon, concurrence et confidentialité ; reprise finale des **6 nouveaux scénarios : 6/6**, avec la projection booléenne. Captures mobile/bureau inspectées. Rapports `2026-11-16T07-05-10-129Z-ndyNxs` et `2026-11-16T07-09-54-281Z-vVGFNp` sous `test-results/visual-runs/`. |
| Live : suite voisine `live-messages-product.spec.cjs` | **14 réussis, un échec préexistant** : le test attend le lien de préférences après filtrage d'animation alors que la vue le réserve à la boîte globale. Échec identique sur le worktree HEAD Marketplace, rapport `2026-11-16T07-00-08-096Z-rYwQAl`. La première recette cumulée conserve aussi ses trois attentes de libellé zéro incorrectes dans les nouveaux tests ; elles sont corrigées avant les reprises réussies, sans modifier le comportement du compteur. |
| Contrats | E41/E42 et import Animation régénérés hors ligne depuis la même application ; **58 opérations Pro et 340 Animation sans divergence sémantique**, **8 tests de contrat messages habitants Animation réussis**. |

Une revue indépendante des extraits ciblés a identifié les cas brouillon et
acquittement retardé, corrigés et testés ci-dessus ; elle ne constitue pas une
revue exhaustive des fichiers ou une exécution indépendante des suites.

**Impacts :** backend et Live modifiés, contrat embarqué Animation synchronisé,
documentation canonique actualisée pour MH-06/MH-08/MH-13. Pro et ERP sans impact
fonctionnel : leurs parcours ne consomment pas ces avis. Aucune migration
supplémentaire à `v322`, aucun nouveau champ persistant, backfill ou paramètre
d'exploitation : les réponses déjà conservées sont projetées à la lecture.
Le générateur conserve ses conversations/réponses existantes ; aucun changement
de fixture de démonstration ou de canal externe n'est nécessaire. Aucun test
distant ni déploiement n'a été réalisé. La base et les serveurs de recette sont
jetables ; le serveur PostgreSQL de cette tentative est arrêté après les tests.
