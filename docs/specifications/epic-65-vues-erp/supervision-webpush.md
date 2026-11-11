# E65-EVO-WEBPUSH — Supervision des notifications Web Push

Évolution du 11 novembre 2026, demandée avec spécification, implémentation,
commit et push. La clôture historique de l’EPIC 65 reste inchangée.

## Résultat attendu et périmètre

Depuis **Supervision technique → Web Push**, un administrateur retrouve les
abonnements et l’historique des alertes, comprend un refus ou une attente,
révoque un abonnement avec un motif et rejoint les traitements existants.
La consultation se fait dans le shell ERP, sans parcourir des tables SQLAdmin.

Deux onglets **Abonnements** et **Historique**, un canal explicite par lecture :

| Canal | Abonnements | Historique |
| --- | --- | --- |
| `LIVE` — Localeo Live | `localeo_live_abonnements_webpush` | `localeo_live_notifications` |
| `PRO` — Localeo Pro | `abonnements_webpush_commercants` | `webpush_sortants` |
| `CONTROL` — Exploitation | `abonnements_webpush_exploitation` | `webpush_exploitation_sortants` |
| `CRM` — Localeo CRM | `crm_abonnements_push` | `crm_intentions_rappels`, canal `PUSH` exclusivement |
| `ORGANISATEUR` — Messages organisateur | Abonnements Live partagés, signalés comme tels | `diffusions_messages_organisateur` |

L’identifiant d’installation Live est une référence technique, sans identité
habitant déduite. Un historique filtré depuis un abonnement concerne son
installation, commerce ou compte : il ne constitue pas une preuve de remise
sur cet endpoint particulier. `ENVOYE`, `REMIS_SERVICE` et `REMIS_TRANSPORT`
indiquent une acceptation fournisseur, jamais la lecture sur le téléphone.

Le périmètre ne crée ni message de test, ni réenvoi arbitraire, ni activation
forcée, ni rotation VAPID. Les liens vers les batchs conservent leurs contrôles
et confirmations. Aucune action n’est déclenchée par un GET.
La confirmation d’une révocation depuis Messages organisateur rappelle que
l’abonnement est partagé avec Live : cet appareil perd les deux circuits.

## Critères d’acceptation

| ID | Déclencheur et résultat observable | Preuves attendues |
| --- | --- | --- |
| WP-01 | Le hub Supervision propose Web Push ; arrivée directe et retour conservent le shell, le parent et les filtres. | API page, navigation navigateur, clavier, 390/1440 px. |
| WP-02 | Seule une session ADMIN historique persistée peut consulter ou révoquer. Autres profils, session expirée et clé API seule refusés ; réponse privée non cachable. Révocation protégée CSRF et origine. | Tests 401/403, page/API, CSRF, expiration effaçant les données UI. |
| WP-03 | Abonnements paginés et filtrés par canal, état et destinataire exact ; dates, appareil connu et état explicites. Une donnée absente reste non renseignée. | Repositories réels, API fermée, état vide/erreur, absence de secrets. |
| WP-04 | Historique paginé par canal, statut et destinataire ; détail avec type, dates, tentatives connues et diagnostic assaini. Les états natifs sont conservés et expliqués. | Cinq canaux, filtre CRM PUSH, messages organisateur distincts, sécurité du rendu. |
| WP-05 | Depuis un abonnement, ouvrir l’historique de son destinataire puis revenir sans perdre les filtres. | Parcours navigateur, aucune fausse relation notification→endpoint. |
| WP-06 | Révoquer exige confirmation et motif non vide (3–500 caractères). La transition verrouille une cible, rend l’abonnement inactif, efface les secrets de livraison et audite l’acteur, le canal, la référence et le motif. Répéter sur une cible déjà révoquée ne produit pas de deuxième audit. Aucun autre abonnement/préférence/historique supprimé. | Domaine, application, PostgreSQL, répétition et concurrence ; CRM conserve ses règles de version et invalide les intentions concernées. |
| WP-07 | Liens contextuels vers les batchs et rappel des flags pertinents ; aucune clé, endpoint, hash de session, payload brut ou lien personnel exposé. Les erreurs historiques sont assainies et affichées comme texte. | Projections en liste blanche, XSS/secret sentinelles, pas d’appel fournisseur. |
| WP-08 | Pages bornées, sans N+1 ni total exhaustif ; listes de 25 par défaut et 100 maximum, curseur stable lié aux filtres. Recherche, détails et mutations résistent aux réponses obsolètes et à la perte de session. | Tests N/10N, pages profondes, concurrence, navigateur réseau lent/erreur. |

## Architecture et contrats

Le domaine Exploitation porte la décision de révocation administrative motivée
et sa répétition. L’application orchestre transaction, chargement verrouillé,
adaptation aux canaux existants et audit. La persistance réalise les projections
bornées et l’effacement des secrets ; aucune route ni vue ne réimplémente la
transition. Les retraits consentis existants et les workers restent propriétaires
de leurs validations à l’envoi. Une remise fournisseur déjà commencée ne peut
pas être rappelée par cette commande.

La page `/internal/erp/webpush` utilise les API internes sous
`/internal/exploitation/supervision-webpush`, protégées comme Audit E65/E69 :

- `GET /abonnements` et `GET /historique` : `canal`, `statut`, `destinataire`,
  `cursor`, `limit` (1–100). Canal par défaut `LIVE`. Destinataire exact borné
  à 200 caractères (UUID pour Live/Pro/CRM, identifiant acteur pour Control).
- `GET /abonnements/{id}?canal=…` et `GET /historique/{id}?canal=…` : détail
  unique, 404 sans fuite inter-canal. Organisateur partage les abonnements Live.
- `POST /abonnements/{id}/revoquer` : `{canal, motif, expectedVersion?}`, CSRF ERP existant.
  La version courante est obligatoire pour CRM, qui possède déjà ce contrôle.
  Réponse après commit `{changed, item}`, avec l’état courant ; échec transactionnel
  sans succès affiché. Relecture avant décision et verrou de ligne.
  Une cible CRM déjà révoquée répond `changed: false` même si la version fournie
  précède la révocation ; la présence de version reste obligatoire. Une cible
  active avec version périmée est refusée. Seules les intentions PUSH devenues
  invalides de ce destinataire sont annulées ; les rappels EMAIL sont préservés.

Réponse de liste : `{items, nextCursor, hasMore, generatedAt}` ; tri descendant
sur création et identifiant. Pas de total global. Le curseur contrôle canal,
onglet et filtres ; aucun chargement de toutes les pages côté navigateur.
Chaque item commun expose `id`, `canal`, `destinataire`, `destinataireLabel`,
`createdAt`. Abonnement : `actif`, `deviceLabel`, `lastUsedAt`, `revokedAt`,
`version` (CRM, sinon `null`), `motifRevocation` (Pro/Control, sinon `null`).
Historique : `statut`, `type`, `titre`, `tentatives`, `sentAt`,
`nextAttemptAt`, `lastAttemptAt`, `diagnostic`. Champs non disponibles : `null`.
Le titre organisateur provient du message lié ; son détail ajoute `messageId`
et `campagneId`. Aucun corps ou contenu brut JSON n’est exposé. Les diagnostics
fournisseur libres sont remplacés par une catégorie HTTP reconnue ou une
indication de masquage ; les codes métier connus sont conservés. Les types,
filtres et erreurs sont validés côté serveur.

Filtres d’abonnement : `ACTIF`, `REVOQUE`. Filtres d’historique natifs :

| Canal | Statuts acceptés |
| --- | --- |
| LIVE | `A_ENVOYER`, `EN_COURS_ENVOI`, `ENVOYE`, `ERREUR_TEMPORAIRE`, `ERREUR_DEFINITIVE`, `ANNULE` |
| PRO / CONTROL | `A_ENVOYER`, `EN_COURS_ENVOI`, `ENVOYE`, `ECHEC_TEMPORAIRE`, `ECHEC_DEFINITIF`, `ANNULE` |
| CRM | `EN_ATTENTE`, `EN_TRANSPORT`, `REMIS_TRANSPORT`, `ECHEC_CERTAIN`, `ECHEC_DEFINITIF`, `INCERTAIN`, `ANNULE`, `EXPIRE` |
| ORGANISATEUR | `A_ENVOYER`, `EN_COURS`, `ERREUR_TEMPORAIRE`, `INCERTAIN`, `REMIS_SERVICE`, `ECHEC`, `PARTIEL`, `SANS_ABONNEMENT`, `REFUSE` |

L’interface présente des libellés français et des dates en heure de Paris.
Filtres non personnels en URL ; destinataire exact conservé en mémoire, pas
dans le lien de navigation. Réponses obsolètes ignorées/annulées, un seul appel
actif par vue. Une perte de session efface les projections déjà affichées.

## Volumétrie et livraison

Chaque requête sélectionne une famille et `limit+1` lignes en base, détail par
clé primaire. Les listes évitent les colonnes de secrets et les collections ORM.
Ajouter les index de tri/filtrage manquants dans une migration nouvelle,
sans modifier les anciennes migrations. Pas d’agrégat global synchronisé.

Budget local avant activation : N=1 000 puis 10N=10 000 lignes par famille,
page 25/100, première page et page profonde, filtre destinataire et statut,
absence de résultat. Au plus 3 requêtes SQL par page, p95 < 500 ms sur PostgreSQL
jetable local ; détail/révocation < 500 ms hors attente concurrente. Vérifier
plans et mémoire bornée. Charge mixte : quatre lecteurs et une révocation
concurrente, absence de doublon d’audit et de verrou global. Les mesures locales
ne constituent pas une qualification de l’hébergement distant.

Backend et documentation modifiés ; les PWA consommatrices ne changent pas de
contrat. Le correctif Push mobile préparé précédemment est livré dans des commits
séparés. Migration d’index avant ouverture de l’écran ; aucun flag supplémentaire.
Pas de données métier à convertir. Le générateur conserve ses schémas, scénarios
et consentements ; les nouveaux états de test sont des fixtures synthétiques.

### Mise en service

La migration additive `localeo-backend/sql/v307_supervision_webpush.sql`
ajoute les index de pagination manquants ; elle réutilise les deux index Live
équivalents déjà présents depuis v275. Les tests l’appliquent à un schéma
PostgreSQL jetable. Aucun changement de colonne ni de consentement.

Lors de la livraison autorisée, vérifier la cible puis exécuter le dry-run
de `scripts/database/apply_migrations.py`, examiner toutes les migrations
en attente, puis appliquer selon la procédure habituelle avant d’ouvrir
l’écran. Le lancement réel des batchs garde ses flags et contrôles existants.
Après livraison, contrôler l’accès ADMIN, un filtre de chaque canal et le
retour abonnement → historique ; utiliser uniquement un abonnement de recette
désigné pour vérifier une révocation. Aucun push réel n’est nécessaire pour
ouvrir ou tester la consultation. Un retour de version applicative peut
conserver ces index ; ne pas réactiver un abonnement révoqué par SQL.

## Suivi de réalisation

Spécification établie avant implémentation. Réalisation locale du 11 novembre
2026 sur la base backend `63f8ce8`, livrée par le commit `63abb86`, poussé
sur `main`. Le correctif Push mobile précédent est poussé séparément :
backend `63f8ce8` et Marketplace/Live `a7b3320`.
Aucune donnée distante modifiée, notification réelle envoyée ou migration
distante appliquée. Le statut historique de l’EPIC 65 reste inchangé.

### Preuves de comportement

| Critères | Preuves exécutées et résultat |
| --- | --- |
| WP-01/05 | `node tests/browser/epic65-webpush-erp.cjs` : parcours complets à 390 et 1440 px, filtres, pagination, détail → historique → retour et focus ; paramètres publics préservés après navigation navigateur. Réussi. |
| WP-02 | `tests/security/test_supervision_webpush_access.py` : **28 tests réussis** sur l’application réellement montée, registre de session SQLite jetable, refus des profils internes seuls/combinés, session absente/révoquée, clé API seule et CSRF/origine ; page et assets accessibles à l’ADMIN persisté. |
| WP-03/04/07 | Tests domaine/application/API `test_supervision_webpush*` : **35 tests réussis**, contrats fermés, états natifs, refus, pagination et assainissement. Le harnais navigateur vérifie aussi chaque canal/statut et un texte hostile sans interprétation HTML. |
| WP-06/08 | `tests/infrastructure/test_supervision_webpush_postgres.py` : projections et migration sur PostgreSQL jetable, transactions, concurrence, cibles CRM et mesures de volumétrie ; résultats détaillés ci-dessous. |
| WP-08 côté interface | Réponse de recherche obsolète ignorée, 503 distingué de l’état vide, conflit CRM conservant le motif, expiration pendant lecture et mutation sans réaffichage. Réussi dans le harnais Web Push. |

Non-régression ERP : `node tests/browser/erp-menu-ux.cjs` (**35 scénarios**)
et `node tests/browser/erp-page-template.cjs` (**24 scénarios**) réussis.
Contrôles architecture, classes de domaine et couverture des use cases :
**689 tests réussis** via le lanceur isolé. La première exécution a signalé
deux erreurs de fixtures de sécurité et le recensement manquant de la nouvelle
classe de domaine ; ces trois points ont été corrigés, puis les deux suites
concernées entièrement rejouées (28 et 689 succès).

Revue indépendante des contrats et de la sécurité terminée sans constat
bloquant. Les écarts de statuts, le motif de révocation, l’entrée du hub et
le titre organisateur ont été corrigés. Captures finales inspectées dans
`localeo-backend/.artifacts/webpush-erp-ui/`, abonnement et historique à
390/1440 px. Les API sont simulées dans ces parcours navigateur ; les
adaptateurs et les autorisations sont testés séparément côté serveur.

### PostgreSQL et volumétrie — résultat final

Les **3 tests PostgreSQL** sont réussis, puis rejoués après les derniers
ajustements de fixture et d’index : **3 succès en 40,55 s**. La migration v307
comporte 26 index, dont l’index partiel des intentions CRM à annuler. Les tests
utilisent les colonnes des modèles et migrations réels dans un schéma jetable,
sans leurs dépendances de clés étrangères externes au périmètre.

Résultats de 18 mesures : quatre familles d’abonnements et cinq historiques,
à **1 000 puis 10 000 lignes par famille**, pages 25/100, filtres d’état et de
destinataire, zéro résultat et 30 pages successives sans doublon :

- **1 requête SQL par page** ; p95 maximal **137,25 ms** à N et **36,88 ms** à 10N ;
- détail au maximum **3,66 ms**, révocation au maximum **17,57 ms** ;
- pic de mémoire tracée au maximum **289 600 octets** ;
- plans de pagination profonde retournant **26 lignes**, parcours d’index
  et jointure indexée pour les messages organisateur ;
- quatre lecteurs et une révocation simultanés, deux révocations concurrentes
  d’une même cible avec un seul audit, rollback après échec d’audit vérifiés ;
- CRM : seuls les PUSH en attente concernés sont annulés, e-mails et autres
  appareils conservés ; titre et références organisateur réellement reliés.

Rapport final : `localeo-backend/.artifacts/webpush-e65-performance.json`.
Les rapports `webpush-e65-performance-initial.json` et
`webpush-e65-performance-before-plan-fixture-fix.json` sont conservés : la
première mesure de plan utilisait une fixture au mauvais fuseau et retournait
zéro ligne. Elle n’est pas retenue comme preuve finale de page profonde.
La base locale dédiée sur le port 55488 a été arrêtée après recette.

Ces résultats couvrent WP-01 à WP-08 localement. Ils ne prouvent ni un
déploiement, ni une réception sur téléphone, ni la capacité de l’hébergement
distant. Contrôles documentaires : liens sans erreur et 148 sources exportées
validées ; la livraison doit embarquer leur bundle actualisé si nécessaire.

### Matrice des impacts

| Critères | Propriétaire et preuves attendues | Contrat et documentation | Démonstration et livraison |
| --- | --- | --- | --- |
| WP-01/05 | Interface ERP : navigation, historique du destinataire, retour et filtres conservés ; parcours navigateur | Contrat interne de cette spécification et guide de prise en main ERP | Fixtures navigateur synthétiques ; aucun parcours PWA consommateur modifié |
| WP-02 | Sécurité ERP : session ADMIN persistée, refus des autres profils, CSRF, expiration | Même périmètre que les outils techniques historiques ; aucun droit E69 ajouté | Comptes de test simulés ; aucune habilitation distante modifiée |
| WP-03/04/07 | Adaptateur de lecture : projections fermées des cinq familles, états natifs, diagnostics assainis | API interne consommée par ERP seulement ; procédure de reprise des notifications actualisée | Schéma métier et générateur inchangés ; aucune donnée réelle nécessaire |
| WP-06 | Domaine Exploitation : décision de révocation ; application : verrou, transaction et audit ; PostgreSQL : purge et répétition | Commande administrative distincte des retraits consentis existants ; version CRM conservée | Fixtures de concurrence/rollback ; aucun appel fournisseur ni migration de données |
| WP-08 | Persistance et interface : curseurs, limites, index, réponses obsolètes ; mesures N/10N et charge mixte | Bornes et budgets ci-dessus ; bilan des mesures avant livraison | Migration additive d’index ; application avant ouverture de l’écran, pas de nouveau flag |
