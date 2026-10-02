# E69 — Vérification et préparation de livraison

Version **V1.4 — scopes fonctionnels globaux, décision du 2 octobre 2026**. État : **En cours**.

## Correctif des refus Backoffice — 2 octobre 2026

Signalement : refus « Action non autorisée pour ce profil » avec un compte
Backoffice, corrélation `LOC-7ed07a53-ccea-4b71-9ba8-24ab9f136ce9`.
Les journaux de cette requête distante n'ont pas été consultés. La reproduction
locale sur la base backend `4635820` démontre les refus des pages Opérations,
Nouvelle offre Animation et configuration des offres : entrées absentes du
catalogue fermé. L'API des offres et l'adaptateur moteur conservaient aussi des
gardes historiques incompatibles avec le principal nominatif ; les consoles
moteur utilisaient le jeton CSRF historique.

Corrections : classification explicite des pages/API métier, offres via
`animation.gerer`, UUID et auteur interne conservés dans les opérations moteur,
CSRF nominatif dans les trois consoles. Chaque transaction du moteur revalide
la session et le scope avant lecture/rejeu/effet, dans sa propre UOW ; aucune
connexion d'autorité supplémentaire gardée pendant les appels métier ou le
stockage. Les liens SQLAdmin inutilisables sont retirés des parcours nominatifs.
Les formulaires de création commerçant/coffret exigent désormais le même scope
de gestion que leurs commandes, sans ouvrir la création au Lecteur.

Les gardes SQLAdmin, comptes internes, Audit, quotas, neutralisation, régularisation,
conservation, batchs et mouvements de fonds restent distinctes. Les parcours
partenaires et les sessions historiques conservent leurs contrats. La matrice
[permissions/surfaces](permissions-surfaces.md) précise les opérations ouvertes.

Reproduction initiale : **5 échecs / 41 succès** dans les tests HTTP des surfaces
réelles (trois refus Backoffice et deux formulaires trop ouverts au Lecteur).
Preuves finales exécutées avec `python scripts/validation/test_isolated.py`
depuis le backend, arguments `-q --tb=short`, sur l'arbre corrigé :

- **108 réussis** : `tests/security/test_acces_internes_surfaces.py`,
  `tests/api/test_offres_animation_erp.py`,
  `tests/domain/abonnements_plateforme/test_creation_offre.py`,
  `tests/application/abonnements_plateforme/test_creation_offre_animation.py`,
  `tests/security/test_erp_session_access.py`.
- **109 réussis** : `tests/api/test_e69_generation_interne.py`,
  `tests/application/services/test_autorisations_moteur.py`,
  `tests/api/test_generation_animation_api_t2.py`,
  `tests/api/test_navigation_consoles_animation_erp.py`,
  `tests/api/test_avancement_preparation_api.py`,
  `tests/api/test_exploitation_animation_api_t5.py`,
  `tests/api/test_parametres_exploitation_api_t6.py`,
  `tests/security/test_animation_batch_http.py`.
- **445 réussis** : `tests/architecture`,
  `tests/domain/test_domain_dedicated_classes.py`,
  `tests/application/use_cases/test_use_case_business_test_coverage.py`.

Les nouvelles preuves utilisent les gardes HTTP réels et un pool SQLite borné à
une connexion pour l'enveloppe transactionnelle. Elles couvrent le retrait de
scope/session avant effet ou reçu, puis entre deux phases de stockage ; les I/O
fournisseur restent hors transaction. La revue indépendante a vérifié le
catalogue fermé, les consommateurs de la factory et les liens des consoles.
Pas de nouvelle recette navigateur ni de scénario PostgreSQL concurrent pour
ce correctif ; aucun accès aux services ou à la base d'exploitation pendant les tests.
Les contrôles des guides, des sources exportées et `git diff --check` réussissent.

Impacts : backend et documentation E69 ; aucun changement de DTO, de schéma SQL,
de rôle stocké ou de données de démonstration, donc aucune migration, régénération
de jeu ni nouvelle variable requise. Les applications publiques restent hors
du correctif. Livraison à prévoir : backend avec ses templates et bundle
documentaire actualisé, puis recette avec un compte Backoffice sur la cible
(Opérations, offres, génération/préparation/suivi, et refus SQLAdmin).
Au terme de la validation locale, aucun commit, push ni déploiement n'avait été
effectué. Publication Git demandée ensuite : backend
`72f690c8e62c0d96ff0ebae30f0e7fbc57bff343` committé et poussé sur `origin/main`.
Le commit documentaire associé porte cette note, la matrice, le guide et le
suivi E69 en attente. Aucun déploiement applicatif n'a été exécuté ou vérifié.
La disparition du signalement distant reste à vérifier après livraison. **CA-18 reste ouvert** ;
cette correction des accès ne constitue pas une preuve de traçabilité des refus.

## Réexamen de clôture après publication — 2 octobre 2026

**Verdict inchangé : clôture bloquée par CA-18.** Révisions relues : backend
`4635820843402af9ed6f99da09567315d3e56ecc`, projet
`ba04181594b45d3ff2dbf27fce43f608fe74cc41`. Les deux arbres étaient propres et
les index vides au début de ce réexamen. La migration test v253 et la publication
Git sont acquises ; elles ne remplacent pas le correctif de traçabilité des refus.

Relecture du garde `_contexte_erp`, du middleware de session et de l'audit :
le refus intervient toujours avant `verified_actor`, et les événements génériques
ne portent toujours pas l'auteur interne et le scope demandé. La comparaison
avec le socle `86199b1` confirme que le commit publié ne corrige pas ce comportement.
Le diagnostic isolé des trois refus ERP/Support/Atelier et les tests V1.4 consignés
plus bas sont donc **réutilisés, sans nouvelle exécution**. Les suites migration
(12 réussis), architecture (445 réussis) et navigateur création/édition (390/1280)
restent valables pour le contenu publié ; elles ne prouvent pas CA-18.

La matrice des 27 critères et les actions correctives du premier bilan restent
applicables. Aucun critère retiré, aucun statut ou chemin modifié. Ce réexamen
ne réalise ni changement applicatif, ni migration, ni recette distante, ni commit,
push ou déploiement. Lot de commit préparé : **ce seul fichier**, message proposé
`docs(epic69): consigner le reexamen de cloture apres publication` ; index laissé vide.

Configuration/livraison restante : base test déjà en v253 ; pour les autres cibles,
appliquer les migrations manquantes dans l'ordre indiqué plus bas. Vérifier
`LOCALEO_ERP_URL` (origine HTTPS), transport mail et limites de renvoi 60 s / 5 par
24 h par défaut. La révision documentaire publiée `ba04181594b45d3ff2dbf27fce43f608fe74cc41`
contient le guide global E69 : elle peut être sélectionnée au build après contrôle
des empreintes. Le pin backend reste `b496d3efaa07c8a3806d8a499270c06529a5df1f`,
qui n'embarque pas ce guide. Déployer API et assets ERP/satellites ensemble, puis
recetter invitation, profils globaux, retrait/révocation et reprise admin.
La correction de CA-18 reste nécessaire avant de demander de nouveau la clôture.

## Publications et interventions précédentes

**Publication Git du 2 octobre, après les interventions ci-dessous :** backend
`4635820843402af9ed6f99da09567315d3e56ecc` committé et poussé sur `origin/main`.
Il inclut les scopes globaux, le formulaire sans périmètre territorial, la
recherche utilisateurs, v253 et la compatibilité v252 avec les tables précréées.
Les mentions « non committé » et « aucun push » plus bas décrivent l'état des
interventions au moment de leur exécution, avant cette publication autorisée.
La documentation est incluse dans le commit portant cette note ; la création du
skill de clôture fait l'objet d'un commit distinct. La publication Git ne prouve
pas le déploiement du code ; CA-18 reste ouvert.

Les commits backend `86199b1` et projet `4613ac2` ont été poussés dans leurs dépôts
indépendants. Cette publication Git ne prouve aucun déploiement, migration distante,
compte réel ni recette en environnement partagé. L'audit documentaire du 2 octobre
confronte les guides au code sans rejouer les tests métier ; les résultats de la
section « Preuves historiques exécutées — V1.3 » restent les preuves locales
précédemment consignées. **Ils ne valident pas
l'évolution V1.4**, qui possède les scénarios et le suivi distincts ci-dessous. Sources : [backlog](../../roadmap/en-cours/epic-69-profils-acces-erp-satellites-backlog.md),
[contrats](architecture-contrats.md), [permissions](permissions-surfaces.md).

**Intervention postérieure à la revue de clôture, 2 octobre 2026 : base de test
migrée de v250 à v253 sur demande explicite.** Voir le compte rendu ci-dessous.
Le code applicatif n'a pas été déployé par cette intervention ; CA-18 reste ouvert.

## Revue de clôture du 2 octobre 2026

**Verdict : clôture bloquée par CA-18, EPIC conservée En cours.** La demande de
clôture ne modifie ni les 27 critères ni leur périmètre. Les contrôles locaux V1.4
ci-dessous sont réutilisés ; ils ne sont pas présentés comme réexécutés lors de
cette revue. Révisions de base : backend `86199b1`, projet `4613ac2`, avec leurs
modifications locales non committées. Aucun environnement distant n'est utilisé.

La revue indépendante constate un refus correctement appliqué mais insuffisamment
attribué : dans `app/security/erp.py`, `_contexte_erp` lève le 403 avant d'affecter
`request.state.verified_actor`. Le middleware de session connaît le principal
interne, mais `app/audit.py::resolve_actor` ne le reprend pas. Les événements HTTP
génériques portent route, statut et corrélation, sans auteur nominatif ni scope
refusé. Les tests de surfaces prouvent le refus, pas la trace exigée par CA-18.
L'audit des mutations de comptes réussies ne couvre pas ce cas.

Reproduction isolée exécutée pendant la revue : **3 scénarios reproduisent le
défaut**, avec un `PrincipalInterne` Lecteur et les scopes `catalogue.gerer`,
`support.gerer`, `atelier.gerer`. Appel du garde, capture du 403, puis résolution
de l'auteur et émission du journal HTTP : `verified_actor` absent,
`resolve_actor(request) == "anonymous"`, aucun événement de refus du garde ;
`http.error.handled` n'a ni auteur ni scope. Les trois assertions de diagnostic
réussissent parce qu'elles constatent le défaut, **pas parce que CA-18 est validé**.
Le diagnostic temporaire, exécuté via le lanceur isolé du backend, a été supprimé ;
aucun test de non-régression volontairement rouge n'est ajouté à la suite permanente.

Commande du diagnostic : `scripts/validation/test_isolated.py --rootdir=<temp>
--confcutdir=<temp> <temp>/test_ca18_reproduction.py -q -s`, via Python 3.14.
Une première collecte hors dépôt a été interrompue ; la seconde, bornée au
temporaire, a produit ces trois résultats. Références relues :
`app/security/admin_session.py`, `app/security/erp.py`, `app/audit.py`,
`app/main.py::_log_handled_exception` et `app/observability_http.py`.

**Travail nécessaire avant clôture :** définir et raccorder une trace de refus
commune aux entrées ERP/Support/Atelier, attribuée au principal vérifié et contenant
l'action ou le scope demandé, le résultat et la corrélation, sans secret ni corps
de requête. Vérifier les refus et les succès par profil, les accès directs, les
alias et les parcours après révocation. Conserver les refus fermés et la séparation
avec l'admin historique. Ce correctif transversal n'est pas introduit silencieusement
dans la revue de clôture.

Un défaut borné a été corrigé pendant la revue : la liste utilisateurs envoyait
`email`/`nom`, ignorés par l'API qui attend `recherche`. Le champ **Nom ou email**
utilise désormais ce paramètre ; **État : Tous** omet le filtre vide. Un doublon
email affiche un conflit de création, plutôt qu'un faux conflit de version.
La recette `node tests/browser/epic69-acces-internes.cjs` a été réexécutée avec succès
à **390 et 1280 px**, avec contrôle des paramètres réellement envoyés, résultats,
rechargement et réponse de doublon au format API. Les routes métier y sont simulées :
cette preuve concerne l'interface, pas la remise d'un email réel.

### Couverture rapprochée pour la décision de clôture

Les groupes ID/HTTP/PG/TRANSPORT/SUR/MET/FIN/UI/DEMO/DOC sont définis dans les
preuves historiques plus bas ; leurs adaptations V1.4 et résultats sont consignés
dans la section suivante. « Vérifié sur scénarios ciblés » indique la portée réelle
des tests relus, sans certifier toutes les variantes de la grille de référence.
CA-18 empêche la décision globale d'acceptation, même avec ces suites réussies.

| Critères | Code et comportement rapprochés | Preuves exécutées réutilisées, sauf mention | Documentation / exploitation | Verdict |
| --- | --- | --- | --- | --- |
| CA-01/02/21 | Domaine `identite_acces`, contexte ERP, projections et union des scopes globaux | ID V1.4 (51), SUR/FIN (29), UI profils | Contrats, matrice, guide et OpenAPI globaux | Vérifié sur scénarios ciblés |
| CA-03/04/13/15/20 | Gardes par scope, commandes OnBoard/Support/Atelier, exceptions Backoffice, revalidation avant effet/rejeu | SUR/FIN (29), intégration/transition (23), UI OnBoard ; MET historique pour comportements inchangés | Catalogue d'actions ; argent et technique restent admin | Vérifié sur scénarios ciblés |
| CA-05/06/07/17 | Principal interne distinct, SQLAdmin fermé, admin historique indépendant | ID (51), SUR (29), gardes/API keys/OpenAPI (35), transition (23) | Guide de reprise ; aucun admin nominatif | Vérifié sur scénarios ciblés |
| CA-08/16/22 | Sessions, autorité relue, retrait de F, désactivation, rejeu et consommateurs UI | PG/transition (23), FIN (29), UI accès et suivi financier | Versions d'autorisation, sécurité et compte distinctes | Vérifié sur scénarios ciblés |
| CA-09 | Migration v253, conversion GLOBAL sans changement de profils/secrets ; démonstration/restauration | Migration PostgreSQL (1), DEMO unitaires (4) et PostgreSQL (4) | Inventaire et conversion en cible restent prérequis de livraison | Vérifié localement, bascule distante non exécutée |
| CA-10/11/19 | Projections paiements, pièces autorisées, Support financier et masquages | FIN/SUR (29), UI financier ; GED historique pour règles inchangées | E65, guide Finance et familles documentaires | Vérifié sur scénarios ciblés |
| CA-12/14 | Navigation, connexion/refus et consommateurs des scopes, purge après retrait | UI accès/OnBoard/Finance et SUR ; UI accès réexécuté après correction de recherche | Guide des libellés, accès directs ; retour automatique au satellite reste une limite UX | Vérifié sur scénarios ciblés ; appareil/PWA cible non recetté |
| **CA-18** | Audit des commandes de comptes présent ; auteur/contexte manquants sur les refus génériques | Revue des gardes, middleware HTTP et audit ; les succès des suites SUR ne prouvent pas cette exigence | Guide/export présents ; traçabilité des refus à compléter | **Partiel — bloque la clôture** |
| CA-23/24/25 | Création, unicité, invitation, finalité, initialisation et consommation atomique | ID (51), PG/transition (23), UI initialisation et recherche | Guide admin, contrat de création et récupération | Vérifié sur scénarios ciblés |
| CA-26/27 | Outbox, versions, renvoi explicite, email/état/rôle modifiés pendant transport/activation | ID (51), PG/TRANSPORT (23) | Guide états d'envoi, reprise manuelle et configuration | Vérifié sur scénarios ciblés ; fournisseur réel non testé |

Les contrôles d'architecture (445 réussis) sont réutilisés pour les modifications
V1.4. La revue de clôture ne modifie que la recherche UI, son test navigateur et
la documentation. Les dettes UI et de rétention listées plus bas sont conservées ;
elles ne sont pas assimilées sans preuve à un échec de CA-18. L'absence de
déploiement ne constitue pas, à elle seule, le motif du refus de clôture.

Contrôles exécutés après les corrections de cette revue : `check_guidance.py`
**89 guides / 931 liens**, puis `--changed --all-markdown` **19 Markdown / 418 liens**,
sans erreur ni avertissement ; `sync_documentation.py --check-sources`
**119 sources valides**. Bundle temporaire de **119 documents** reconstruit,
empreintes vérifiées et guide E69 résolu par le lecteur ERP, identique à la source ;
temporaire supprimé, aucune publication distante. Les index Git restent vides.

## Évolution V1.4 — implémentation et vérifications locales

Référence : **E69-SCOPES-GLOBAUX-20261002**. Les profils gardent leur matrice
fonctionnelle ; les anciennes limitations de communes sont supprimées pour tous
les comptes internes. Les identifiants CA-01 à CA-27 sont conservés. Les anciens
tests de refus territorial doivent évoluer au titre de cette décision explicite,
sans affaiblir les refus de fonctions, de données sensibles ou de commandes d'argent.

| Preuve propre à la V1.4 | Résultat attendu | État au cadrage du 2 octobre |
| --- | --- | --- |
| Domaine et DTO — CA-01/02/04/21/23 | Profils fixes, scopes exacts globaux, union B+F ; création `{role}`, compatibilité GLOBAL vide, refus COMMUNES/null/nonvide et scopes forgés | Lot domaine/application/API : 51 réussis ; scopes exposés en fiche/liste, y compris comptes inactifs sans session autorisée |
| Contexte et écrans — CA-02/13/14/15/16/21 | `scopes:list[str]`, alias `capabilities` GLOBAL ; aucun contexte/sélecteur de communes ; Finance sans catalogue et Lecteur sans mutation | Playwright accès internes (390/1280 px), OnBoard et suivi financier réussis ; contrats et JS à livrer ensemble |
| Lectures et commandes multi-communes — CA-02/04/10/11/19/20 | Fonctions autorisées accessibles sur toutes les communes ; mêmes masquages, familles documentaires et restrictions financières | Lots surfaces/Finance 29 réussis et intégration/transition 23 réussis ; recette cible à compléter |
| Migration v253 — CA-08/09/16/27 | Conversion GLOBAL vide, incrément `version`/`authorizationVersion` des seuls comptes modifiés ; sessions valides avec relecture d'autorité ; application unique suivie par version/checksum | 1 test PostgreSQL local réussi ; inventaire et recette cible à compléter |
| Révocation et compatibilité — CA-06/07/08/12/17/22 | Retrait de F effectif avant lecture/rejeu, formulaire ancien obsolète, admin historique indépendant, API keys batch séparées | Lot intégration/transition : 23 réussis ; complément API keys/gardes/OpenAPI : 35 réussis |
| Démonstration/restauration — CA-09/18 | Comptes générés globaux, secrets restaurés neutralisés ; anciens formats lisibles dans le rapport, conversion des anciennes attributions par v253 séparément | 4 unitaires de lecture des formats role-only/GLOBAL/ancien COMMUNES et 4 PostgreSQL de génération/restauration réussis |
| Documentation/contrat | Guides, export documentaire et OpenAPI alignés ; bilan historique préservé | OpenAPI canonique E41 régénéré (673 chemins) ; 94 guides/1 037 liens sans erreur ni avertissement, 119 sources exportées vérifiées, contrôle des différences réussi |

Lots locaux V1.4 rapportés le 2 octobre : **51 tests domaine/application/API**,
**1 test PostgreSQL de migration**, **29 tests surfaces/Finance** et **445 tests
d'architecture** réussis. Playwright accès internes (390/1280 px), OnBoard et
suivi financier réussis ; **4 tests unitaires et 4 PostgreSQL** de
démonstration/restauration réussis. Lot d'intégration **23 réussis** : concurrence
comptes, transport, délégation Animation, projection/effets OnBoard et transition
des principaux. Avertissements SQLAlchemy préexistants sur cycles de clés
étrangères et SQLite conservés. Contrat OpenAPI régénéré : **673 chemins**. Ces lots restent
distincts, ne sont pas additionnés et ne valent ni recette complète ni déploiement.
Le complément API keys/gardes/OpenAPI a réussi : **35 tests**, dans
`test_api_key_principal.py`, `test_api_key.py`, `test_erp_session_access.py`,
`test_internal_openapi_protection.py` et `test_generate_openapi_documentation.py`.
La recette globale déployée reste à réaliser. Les contrôles documentaires des six sources ont réussi : **94 guides,
1 037 liens, aucune erreur ni avertissement**, **119 documents exportés** valides
et contrôle des différences réussi ; aucun bundle déployé ni migration distante.

Contrôle final du workspace : **89 guides/931 liens**, puis **19 Markdown
modifiés/417 liens**, sans erreur ni avertissement. Un bundle V1.4 temporaire
de **119 documents** a été construit, ses empreintes contrôlées et le guide
résolu par le lecteur réel de l'ERP : contenu identique à la source, avec les
droits sur toutes les communes. Le bundle temporaire a été nettoyé et l'instance
PostgreSQL jetable arrêtée. Contexte testé : backend `86199b1` et projet `4613ac2`
avec les modifications locales V1.4 ; les trois frontends voisins sont inchangés.

Les nouveaux tests ont aussi été exécutés contre l'ancienne révision dans un
temporaire : lots **5 échecs/14 réussis**, puis **1 échec/2 réussis** sur l'ancienne
acceptation des attributions territoriales. Ils matérialisent l'écart V1.3/V1.4,
pas un défaut de l'ancienne décision produit ; le lot V1.4 courant atteint 51 réussis.

Ne pas reporter un succès V1.3 dans cette table sans avoir exécuté le scénario
V1.4 sur le nouvel arbre. L'évolution ne donne lieu ici à aucun commit, push,
déploiement, envoi de mail ni création de compte réel.

## Traçabilité des 27 critères

Les scénarios ci-dessous constituent les exigences de référence. Les groupes de
preuves ajoutés à chaque critère renvoient aux fichiers historiques à conserver
ou adapter ; leurs résultats plus bas ne certifient pas cette cible V1.4.
Les variantes et la recette déployée restent à vérifier.
D = domaine pur, A = application/HTTP, P = PostgreSQL isolé, UI = navigateur.

| Critère / groupes de preuves locales | Comportement et scénarios de référence | Documentation / contrat | Fixtures / livraison |
| --- | --- | --- | --- |
| CA-01 — ID, HTTP | Identité : D combinaisons de rôles, A attribution admin et refus rôle ADMIN ; résultat audit/version | DTO compte, guide attribution | L/B/F/B+F ; migration ne crée pas d'admin |
| CA-02 — SUR, FIN, UI | Identité + projections : A/UI listes/détails/compteurs filtrés, aucune donnée technique à L | Matrice `metier.consulter` | Toutes communes, données mixtes accessibles, noms identiques |
| CA-03 — SUR, MET, UI | Identité + métier : A refus L par méthode/URL/alias/commande en masse/GET à effet ; aucun appel fournisseur | Catalogue d'actions | Fake mail/Stripe/IA et état DB inchangés hors audit/session |
| CA-04 — MET, UI | Métier + identité : A/UI B gère parcours catalogue/onboarding/Support/Atelier ; garde domaine conservé | Matrice par action et contrats consommateurs | Dossier éligible/inéligible ; inventaire des refus résiduels |
| CA-05 — SUR, HTTP | Identité : A SQLAdmin CRUD/actions/exports, technique, batch, alias et profond refusés à L/B/F/B+F | Principal typé, cartes/navigation | Même compte avec rôle falsifié dans requête |
| CA-06 — HTTP, UI | Auth historique : A/UI login configuré, SQLAdmin et outils conservés | Compatibilité historique | Session avant/après migration ; compte historique non migré |
| CA-07 — ID, HTTP | Identité : A rôle métier ne peut créer/inviter/attribuer/reset un utilisateur interne | API utilisateurs | Falsification champs compte/capacité/CSRF |
| CA-08 — ID, PG, UI | Identité : P/UI retrait rôle et désactivation pendant session/commande/rejeu | Point d'ordre transactionnel | Deux sessions, ancien formulaire, commande déjà en file |
| CA-09 — PG, DEMO | Migration : P inventaire/correspondance explicite, conversion globale explicitement décidée, profils inchangés et admin préservé | Procédure bascule | Anciens rôles dont FINANCE/EXPLOITATION ; rollback sans restauration de secrets |
| CA-10 — FIN, MET | Documentaire + identité : A export/pièce mêmes champs et scope fonctionnel global ; lien réutilisé après révocation refusé | Lecture de document existant | Pièce KYC, facture et reçu absent ; aucune génération cachée |
| CA-11 — FIN, UI | Finance + identité : A/UI E65 L/B/F autorisés aux projections limitées, Audit/argent admin seuls | Dépendance E65 actualisée | Compteurs toutes communes, commande multi-communes lisible, révélations masquées |
| CA-12 — UI | Interfaces : UI clavier/petit écran/login retour/refus ancien lien | Guide/navigation | Pages ERP, Support, Atelier, aucun redirect loop SQLAdmin |
| CA-13 — SUR, PG | Identité + orchestration : A capacité inconnue refusée ; P retrait avant worker/rejeu | Registre explicite et refus des entrées inconnues | Reçu existant, compte service et principal humain distincts |
| CA-14 — SUR, UI | Interfaces + identité : A accès direct sans session, API, pièce/export/PWA refusés | Guards et caches | Cache chaud puis logout ; aucune donnée hors écran |
| CA-15 — SUR, MET, UI | Atelier/Support : A L lit mais ne génère pas d'IA, coffret, réponse ou mail | Commandes séparées des GET | Espion fournisseur ; facture absente ne déclenche pas rendu |
| CA-16 — PG, UI | Sessions : P/UI utilisateur désactivé sur ERP et PWA ouverte, tâche différée | Session/revalidation | Requête suivante refusée ; vieux contenu retiré à réception refus |
| CA-17 — HTTP | Auth historique : A panne référentiel interne, accès configuré encore utilisable si registre historique disponible | Guide reprise | Panne comptes métier distincte de panne DB générale |
| CA-18 — ID, DOC | Audit : A chaque commande/refus tracés sans token/hash/password ; UI guide accessible à l'admin via bundle | Guide et lecteur documentaire | Tests du manifeste, absence de secret dans logs/emailpreview |
| CA-19 — FIN, UI | Finance : A/UI consultation/export et tickets/notes financiers Support | **E69-ARB-05 option A retenue** ; rattachement et projection Support dédiés | Paiement avec/sans instance, ticket financier autorisé et ticket général refusé ; état bancaire inchangé |
| CA-20 — SUR, MET, UI | Finance + identité : A/P commandes d'argent réservées refusées à B/F/B+F ; exceptions ARB-06 autorisées à B sur toutes les communes | Capacité `finance.executer` distincte des trois capacités métier | Tous alias, reprise, idempotence ; F seul refusé aux exceptions |
| CA-21 — ID, FIN, UI | Identité : D/P union B+F des scopes fonctionnels globaux | Attribution par rôle | B+F toutes communes ; aucun scope admin ni commande d'argent ajouté |
| CA-22 — PG, FIN, UI | Identité : P/UI retrait F, B continue, export spécialisé et vieux lien refusés | Version d'autorisation | Tâche différée et résultat de commande historique |
| CA-23 — ID, PG | Identité + outbox : P création/invitation unique, doublon email et retry ; A refus non-admin | POST utilisateur et reçu | Course même email, commit échoue, transport arrêté |
| CA-24 — ID, HTTP, UI | Identité : D/P validité/politique password, ouverture non consommatrice, validation atomique ; UI première connexion | Formulaire, email HTML/texte | Compte attente sans session métier ; mot de passe mal confirmé |
| CA-25 — ID, PG | Identité : D/P liens expirés/falsifiés/remplacés/autre finalité, double activation | Erreurs génériques/token ERP | Horloge fixée, frontières expiration, jeton Animation |
| CA-26 — PG, TRANSPORT | Identité + communication : P génération renouvelée, suivi inconnu/échec, pas de doublon logique | Outbox et guide de renvoi | Fournisseur accepte puis timeout ; précédent email reçu tard |
| CA-27 — PG, TRANSPORT | Identité : P changement email/état/rôle contre activation ou transport | Versions et annulation | Ancien lien impossible, envoi engagé distingué d'envoi en attente |

Compléments de preuve des critères existants, actualisés en V1.4 :

| Critères | Scénario supplémentaire | Résultat attendu |
| --- | --- | --- |
| CA-01/07/23 | DTO `{role}` ; ancienne forme GLOBAL vide ; puis rôle ADMIN, scope null/COMMUNES/nonvide, rôle dupliqué ou état injecté | Formes canoniques et compatibilité acceptées ; autres cas rejetés sans mutation ni faux compte historique |
| CA-02/04/21 | B+F, ressource A+B, création, déplacement ou rattachement entre communes | Scopes fonctionnels globaux ; opérations permises selon profil et invariants métier ; aucune restriction territoriale ni droit admin implicite |
| CA-10/19/22 | Retrait F d'un compte B+F puis demande d'export spécialisé avec ancien paramètre/projection | Export Finance refusé ; export métier B limité à ses colonnes autorisées sur toutes les communes, pas de colonnes cachées envoyées |
| CA-06/12/16 | Connexion historique puis nominative dans un autre onglet ; contexte/monitor/PWA anciens | Principal courant cohérent, admin sans UUID métier fictif, droits recalculés, pas de boucle SQLAdmin |
| CA-08/16 | Modifier attribution puis consulter sans nouveau login ; révoquer les sessions ensuite | Première étape conserve session mais change capacités ; seconde invalide la session ; versions non interchangeables |
| CA-02/11/14 | Finance appelle directement contexte ERP et référentiels | Aucune liste catalogue complète, données limitées à la tâche financière autorisée |
| CA-24/25/27 | Modifier fragment/route de reset en initialisation, annuler invitation d'un autre compte, renvoyer reset | Refus de finalité/cible invalide ; renvoi légitime par route reset, une seule génération utilisable |
| CA-08/23/26 | Activité du monitor et mise à jour d'envoi pendant édition admin | Pas de conflit artificiel de version ; mutation admin concurrente réelle reste détectée |

## Scénarios techniques de référence

Comportements V1.2 conservés, portée actualisée V1.4 :

- CA-04/20/21 : B autorisé sur BUM VALIDER/SUSPENDRE avec conditions de domaine,
  activation déjà à zéro et annulation impayée non active, sur toutes les communes ;
  L/F refusés, aucun rôle admin ni commande financière directe introduit par B+F.
- CA-04/20 : prix positif, commande payée ou active, version obsolète et absence
  de confirmation restent refusés ; aucun remboursement, remise ou annulation
  de facture implicitement autorisé par les trois ouvertures.
- CA-19 : création, modification et relecture d'un ticket et de ses notes sans instance,
  migration préservant les anciens tickets, notes internes bornées, responsable éligible et faux rattachement refusé ; aucun
  ticket général exposé par simple modification d'un type envoyé par le client.
- CA-24/25/26 : lien INITIALISATION valide avant 24 h et expiré à l'échéance ;
  renvoi crée une nouvelle génération ; reset déclenché uniquement par l'admin.

1. Tests de domaine sans ORM pour états, cumul, scopes fonctionnels globaux, finalité de jeton et
   autorisation ; cas frontière et refus inclus.
2. Tests applicatifs : HTTP/CSRF, identité stable, réponses masquées, projections
   et contrats, effet externe absent en refus. Tester aussi le hook d'autorisation
   avant récupération d'un reçu de commande existant.
3. PostgreSQL jetable : contraintes, ordre des verrous, deux connexions concurrentes,
   révocation vs login vs commande, double consommation, outbox et audit atomiques.
   Une simulation séquentielle seule ne prouve pas ces courses.
4. Tests consommateurs ERP/JS/monitor/PWA : capacités, liens, erreurs JSON/HTML,
   expiration et ancienne version frontend ; inventaire des routes sans garde.
5. Recette par attribution, y compris B+F et ressources sur plusieurs communes. Admin historique
   peut reprendre l'exploitation sans compte nominatif, sans exception anonyme.

## Preuves historiques exécutées — V1.3

Le contenu de cette section et les constats de l'audit documentaire du 2 octobre
sont conservés comme historique. Les succès de portée territoriale décrivent
l'ancienne décision D06 ; ils ne prouvent pas les scopes globaux V1.4.

Les lots se recouvrent : **ne pas additionner les résultats** pour annoncer un
total unique. PostgreSQL a été utilisé sur une instance locale jetable avec
schémas isolés ; aucun test n’a utilisé une base distante ou un fournisseur réel.

| Groupe | Preuves et comportement ciblé | Résultat local |
| --- | --- | --- |
| ID | [Domaine](../../../../localeo-backend/tests/domain/identite_acces/test_acces_interne_dedicated.py), [application comptes](../../../../localeo-backend/tests/application/test_comptes_internes.py), API et régressions communication/session : rôles, scopes, états, tokens, idempotence | Lot cœur **85 réussis**, recouvrant HTTP/TRANSPORT |
| HTTP | [API comptes](../../../../localeo-backend/tests/api/test_comptes_internes_api.py), [transition des principaux](../../../../localeo-backend/tests/security/test_transition_principaux_internes.py) : CSRF, endpoints publics, reprise historique | Rerun API **10 réussis**, déjà inclus dans le cœur |
| PG | [Concurrence comptes](../../../../localeo-backend/tests/integration/test_comptes_internes_postgres.py) : même email, double consommation, login/révocation, retrait rôle/rejeu, renvoi/activation, transport/désactivation | **6 réussis**, connexions PostgreSQL concurrentes |
| TRANSPORT | [Courses transport](../../../../localeo-backend/tests/integration/test_e69_transport_interne.py), suites comptes/exploitation : crash après acceptation possible, synchronisation après activation | Lot **52 réussis**, dont **2 nouveaux tests PostgreSQL** ; pas de reprise aveugle ni réécriture du corps purgé |
| SUR | [Surfaces internes](../../../../localeo-backend/tests/security/test_acces_internes_surfaces.py) : SQLAdmin/Ops/Control/Audit fermés aux nominatifs, Finance sans catalogue, méthodes/routes inconnues refusées | Lot d’intégration **127 réussis, 0 ignoré**, puis lot gardes/documentation/OpenAPI **35 réussis** ; registre des routes vérifié, sans prétendre couvrir tout comportement historique |
| MET | [Effets OnBoard](../../../../localeo-backend/tests/api/test_e69_onboard_effects.py), contrats OnBoard, [portées](../../../../localeo-backend/tests/integration/test_e69_perimetre_onboard.py), [délégation Animation](../../../../localeo-backend/tests/application/test_e69_delegation_animation.py) | API/contrats **26 réussis**, dont **6 nouveaux scénarios** ; premier lot PG portées/délégation **4 réussis**, repris avec compléments activité/projections dans le lot **127 réussis** |
| FIN | [API Finance](../../../../localeo-backend/tests/api/test_e69_finance.py), [projections/persistance](../../../../localeo-backend/tests/infrastructure/persistence/test_e69_finance.py), [migration Support](../../../../localeo-backend/tests/infrastructure/persistence/test_e69_support_migration.py) et E65/vision360 | Lots recouvrants **68**, **20**, puis **12 réussis** ; complément recherche/chronologie **16 réussis**. Dernier rerun GED **12 réussis** : propriétaire, famille, rattachements et cohérence source/destinataire |
| UI | [Accès internes](../../../../localeo-backend/tests/browser/epic69-acces-internes.cjs), [suivi financier](../../../../localeo-backend/tests/browser/epic69-suivi-financier.cjs), [OnBoard](../../../../localeo-backend/tests/browser/epic69-onboard.cjs) | Node/Playwright réussis : capacités, B+F, initialisation sans login automatique, CSRF, Lecteur sans mutation, purge et réponses tardives |
| DEMO | [Unitaires](../../../../localeo-backend/tests/unit/test_demo_comptes_internes.py), [génération/restauration PG](../../../../localeo-backend/tests/integration/test_demo_comptes_internes.py) | **2 unitaires + 4 PostgreSQL réussis** ; générateur complet et restauration neutralisée |
| DOC | Trois présents documents, guide canonique et manifeste d’export | **91 guides, 992 liens, 0 erreur, 0 avertissement** pour les trois docs ; export/bundle **119 documents** contrôlés localement |

Régressions navigateur réussies : [Audit E65](../../../../localeo-backend/tests/browser/epic65-audit-erp.cjs),
[Finance E65](../../../../localeo-backend/tests/browser/epic65-finance-erp.cjs),
[accès commerçant](../../../../localeo-backend/tests/browser/acces-commercant-erp.cjs),
[Atelier](../../../../localeo-backend/tests/browser/atelier-assiste-erp.cjs) et
[adresse ERP/OnBoard](../../../../localeo-backend/tests/browser/adresse-commercant-erp-onboard.cjs)
(création/édition et préservation, CSRF, largeurs 390 et 1280 px).

Le lot final de **35 réussis** inclut les surfaces internes, les lecteurs documentaires,
le générateur OpenAPI et sa protection : nouvelles routes explicitement classifiées,
route inconnue refusée et retrait Backoffice contrôlé avant relecture d’un reçu.

Suite d’architecture obligatoire : **445 réussis**, tests/architecture,
test_domain_dedicated_classes et test_use_case_business_test_coverage.

Compléments finaux : [projection checklist OnBoard](../../../../localeo-backend/tests/integration/test_e69_checklist_projection.py)
et progression existante, **6 réussis**, puis **2 PostgreSQL réussis** après contrôle
des aptitudes ERP. Aucune réécriture des snapshots globaux pendant les lectures.
Les titres de documents masqués, anciens blocages et taux historiques ne ressortent
plus dans les listes, récapitulatifs ou indicateurs nominatifs. Les indicateurs et
le filtre de blocage recalculent chaque dossier du périmètre visible ; cette voie
demande une mesure de charge en cible. La liste ordinaire reste paginée en SQL.

Deux contrôles documentaires métier supplémentaires réussis : refus des pièces
non autorisées et masquage des détails techniques antivirus/lisibilité. Le test
navigateur des accès internes a été rejoué avec le lien convention métier autorisé
et son équivalent SQLAdmin refusé. Instance PostgreSQL locale jetable arrêtée après
les validations ; aucune base distante utilisée.

Contrôle intégré des guides, des sources E69 et des index : **96 guides, 1 177 liens,
0 erreur, 0 avertissement**. Les lots de contrôles se recouvrent ; ne pas les additionner.
Syntaxe JS et contrôle des différences sans erreur. Des routes simulées dans
Playwright prouvent l’interface, pas la remise email ou l’installation PWA réelle.

### Constats de revue intégrés

- Autorisation avant rejeu idempotent et dans la transaction du métier ; aucun
  principal nominatif transformé en admin, aucune union des scopes entre capacités différentes.
- OnBoard conserve l’ordre d’autorisation pendant ses effets. Certains services
  historiques ont une transaction autonome : une pièce déjà créée ne peut pas
  être annoncée annulée si le diagnostic suivant échoue.
- Support financier : propriétaire unique, notes cloisonnées, responsable actif
  couvrant toute la source, sans modification bancaire par résolution de ticket.
- GED : facture PDF déjà publiée, exclusivement rattachée à la facture courante
  avec source/destinataire cohérents ; refus KYC, parent nul ou rattachement étranger.
- Transport incertain : pas de renvoi automatique aveugle ; consommation/annulation
  non contredite par une réponse tardive du fournisseur.

### Dette prouvée et recette restante

- Écarts d'interface constatés le 2 octobre : aucun filtre dédié « Invitations à
  reprendre » ; le conflit de doublon email ne fournit pas de lien vers la fiche
  existante ; le formulaire ne présente pas le récapitulatif des capacités sensibles
  refusées prévu en conception ; la connexion nominative renvoie toujours à `/internal/erp`, sans
  retour automatique au satellite initial. La recherche par email et la navigation
  depuis l'ERP permettent une reprise manuelle. Ces écarts restent à traiter contre
  les objectifs de conception ; ils ne réduisent pas les critères d'acceptation.
- Régression unitaires démonstration : **139 réussis, 7 échecs** dans
  test_demo_animation_deadlines. La fixture SimpleNamespace n’a pas de session,
  alors que animation_history utilise session.execute. Cet appel a été retrouvé
  dans le générateur de **HEAD** par git show HEAD:scripts/demonstration/generator.py,
  recherche de self.session.execute(insert(m.CoordinationAnimationOrm) ; E69 n’y
  ajoute que son appel de seed interne.
  Dette préexistante conservée, sans skip ni correction hors périmètre.
- Pas de tâche périodique universelle purgeant les corps d’invitations déjà
  envoyées, seulement expirées et jamais consommées ni annulées. Consommation,
  annulation et invalidité avant transport sont neutralisées, mais ne prouvent
  pas une politique de rétention entièrement automatisée.
- Recette cible non exécutée : remise email, environnement du lien, proxy/cookies
  HTTPS, appareil/PWA, permissions effectives, bascule et reprise historique.
- Les preuves ciblées ne certifient pas toutes les variantes des 27 critères,
  tous les alias historiques ou toutes les courses possibles. Les tableaux
  de référence restent la grille de revue et de recette avant ouverture réelle.

## Démonstration et restauration

La cible V1.4 conserve les huit comptes via domaine/ports : L, B, F, B+F actifs ;
attente ; invitation expirée ; désactivé ; échec d’envoi. Leurs attributions sont
globales et n'affectent aucune commune. Le cumul à deux communes distinctes du jeu
V1.3 est remplacé explicitement ; ses anciennes preuves restent dans l'historique.
Contacts de type gestionnaire, sans fusion avec Animation : Mathilde/Émilie et
leurs droits sont conservés. Les secrets restent dans les artefacts privés.
Le registre comprend les cinq tables de comptes internes et les notes financières.
Aucun email réel, session ou invitation utilisable n’est créé ; seule une trace
historique d’échec neutralisée illustre le défaut de remise.

La restauration vérifie l’empreinte originale de sauvegarde avant transformation,
puis une empreinte distincte de l’état neutralisé : sessions révoquées, liens
annulés, outbox désarmée, anciens hash de mot de passe effacés, versions incrémentées.
ACTIF revient à EN_ATTENTE_INITIALISATION ; DESACTIVE reste DESACTIVE. Emails,
identités, profils et attributions sont conservés. La restauration ne convertit
pas automatiquement les anciens formats territoriaux : appliquer la procédure
de compatibilité et v253 avant ouverture au nouveau backend. Le rapport sait
lire ces anciens formats, sans les transformer. initialized_at reste historique, sans valeur
d’autorisation. Nouvelle invitation admin nécessaire, ancien mot de passe invalide.
Le reçu distingue l’empreinte originale et l’empreinte de restauration sécurisée.

## Migrations, configuration et livraison ordonnées

### Incident d'initialisation : email test vers l'hôte de production — 2 octobre 2026

Signalement : après ouverture du lien d'initialisation, arrivée sur
`/admin/login` avec un fragment d'activation. Incident rattaché à **E69-CA-24/25**,
déjà couverts par l'epic ; aucune nouvelle epic ni modification des critères.
Le jeton signalé n'est ni recopié dans ce dossier, ni utilisé dans les contrôles.

Constats en lecture seule :

- `https://test-backoffice.localeo.city/internal/initialiser-acces` et ses assets
  publics répondent HTTP 200 sans session ; aucune redirection vers SQLAdmin.
  Même résultat sur l'alias `test-api.localeo.city`.
- Le dernier email `INVITATION_INTERNE` dans la base de test, créé le
  **2 octobre 2026 à 13:22:45 UTC**, statut `ENVOYE`, contient en HTML/texte la
  destination **`https://backoffice.localeo.city/internal/initialiser-acces`**.
  Seuls l'hôte et le chemin sont rapportés, aucun destinataire ou secret.
- L'ouverture sans jeton de cette destination renvoie **303 vers `/admin/login`**.
  Cette différence d'hôte explique le symptôme pour cet email ; la rétention du
  fragment lors d'une redirection n'implique pas un lien initial vers SQLAdmin.
- Le producteur `app/infrastructure/email/acces_interne.py` prend l'origine dans
  `LOCALEO_ERP_URL`, impose le chemin `/internal/initialiser-acces` et n'utilise pas
  l'hôte de la requête. Le constat porte sur le mail stocké : la valeur effective
  actuelle de la configuration hébergée n'a pas été lue ou modifiée.

Reprise à effectuer sur le **backend de test** : définir
`LOCALEO_ERP_URL=https://test-backoffice.localeo.city`, appliquer cette configuration
au processus hébergé, puis renvoyer une invitation depuis la fiche utilisateur.
Le changement de variable ne réécrit pas un email déjà préparé ou envoyé ; le
renvoi explicite remplace le précédent lien. Vérifier dans le nouveau mail l'hôte
`test-backoffice.localeo.city`, puis l'ouverture du formulaire sans session admin,
l'initialisation et la première connexion. Ne pas déplacer un jeton vers la
production pour diagnostiquer l'incident.

Impact : configuration et recette E69, sans migration ni changement du contrat,
du générateur ou des droits. Aucun compte modifié, mot de passe initialisé, email
renvoyé ou paramètre distant changé pendant le diagnostic. Cette ouverture GET
ne prouve pas la consommation POST ni la remise du nouveau mail ; recette après
correction de configuration à compléter. Le blocage CA-18 reste distinct.

### Diagnostic du formulaire territorial encore affiché — 2 octobre 2026

Signalement après migration du test : le formulaire utilisateur propose encore
un périmètre de communes. Lecture authentifiée du fichier
`https://test-api.localeo.city/internal/erp/assets/utilisateurs-internes.js` :
HTTP 200, `Cache-Control: no-store`, contenu identique au fichier de la révision
backend `86199b1` après normalisation des fins de ligne, différent de l'arbre
local V1.4. Empreinte du contenu reçu :
`4580e8337d136ffd0a6b74c1c8bb0959ca7dae40a6b954e323109648bd7568f4`.
Session de diagnostic fermée ; aucun utilisateur créé ou modifié sur le test.

La cause vérifiée sur ce serveur est **l'ancienne version applicative encore
servie**, et non une migration v253 manquante. La suppression du sélecteur existe
déjà dans les modifications locales non publiées : champ Profil seul, indication
des droits sur toutes les communes, attributions envoyées sous la forme `{role}`.
Elle s'applique à l'ajout et à l'édition ; les droits territoriaux des gestionnaires
Animation constituent un parcours distinct et ne sont pas modifiés par E69.

La recette `node tests/browser/epic69-acces-internes.cjs` est complétée et réussit
à **390/1280 px** : choix successif Lecteur/Backoffice/Finance/B+F en création,
puis enregistrement de chacun en édition ; un seul sélecteur Profil, aucun champ
territorial et corps POST/PATCH contenant les rôles seuls. Les échanges API sont
simulés localement ; cette preuve ne constitue pas une modification en cible.
Les deux premières exécutions du test complété ont révélé un sélecteur de message
de succès incorrect puis ambigu dans le test ; corrigé sans changer le comportement
applicatif ni affaiblir les assertions de périmètre et de requête.

Action de livraison restante : publier les modifications V1.4 et le correctif de
migration v252, puis déployer le backend et ses assets ensemble. Vérifier ensuite
le formulaire servi et rouvrir la page. La migration de base seule ne remplace pas
les assets ERP. Aucun commit/push ni déploiement exécuté par ce diagnostic.
Pas de nouvelle migration, variable, contrat API ou adaptation du générateur :
le formulaire cible et le contrat global V1.4 étaient déjà corrigés localement.

### Migration du test effectuée le 2 octobre 2026

Cible sélectionnée par `.env.test`, distincte de la démo et de la production :
base `localeo_backoffice_p6c9`, PostgreSQL 18.3. Le dry-run initial annonçait
uniquement v251/v252/v253, dernière version suivie v250. Sauvegarde complète
`pg_dump` au format custom créée avant écriture, SHA-256 enregistré, catalogue lu
par `pg_restore --list` ; aucune restauration de sauvegarde n'a été nécessaire.

La première tentative a appliqué v251, puis annulé la transaction v252 :
`notes_support_financier` existait déjà, sans les colonnes financières sur la
table Support. Le bootstrap ORM peut produire cet état. La reproduction PostgreSQL
locale a échoué avec `DuplicateTable` sur la table précréée, tandis que le cas sans
précréation réussissait (**1 échec / 1 réussite**).

Correction bornée de v252 : conserver la table avec `CREATE TABLE IF NOT EXISTS`
et installer le default serveur `created_at`, absent de la table ORM. Aucun
effacement de table ou de note. Les anciennes empreintes LF/CRLF de v252 sont
explicitement acceptées par le runner, comme les compatibilités historiques
existantes ; une base ayant appliqué la migration originale ne la rejoue pas.
Le schéma final et les invariants Support sont inchangés, sans changement de contrat
API, de règle métier ou du générateur. Les données et notes existantes sont
conservées ; les fixtures couvrent désormais les deux chemins.

Preuves après correction : **12 tests réussis** via `test_isolated.py`, comprenant
`test_e69_support_migration.py`, `test_e69_scopes_globaux_migration.py` et
`test_apply_migrations.py` ; **445 contrôles d'architecture réussis**. Instance
PostgreSQL jetable arrêtée après les contrôles.

Reprise distante vérifiée : **v252 puis v253 appliquées**, maximum suivi **253**,
dry-run final vide et checksums valides. Contraintes de propriétaire Support et
de portée GLOBAL validées ; aucun compte interne ni note financière créé. Les
comptages commerçants/achats/paiements/Support et l'empreinte des champs historiques
des dossiers Support sont identiques avant/après. Aucun email envoyé, aucun seed,
aucune modification de la démo ou de la production par cette intervention.

Preuves et sauvegarde privées, non versionnées, dans le dépôt backend :
`tmp/e69-migration-test-20261002/20261002T080355Z/` ;
`resultat.json` conserve la première tentative et `resultat-reprise.json` le succès.
La sauvegarde est `avant-e69.dump`. Ces fichiers ne doivent pas être ajoutés au commit.

**Avant le prochain déploiement du backend test, publier aussi le correctif v252
et son runner** : la base enregistre désormais l'empreinte corrigée ; l'ancien
artefact ne la connaît pas. Aucun commit/push ni déploiement applicatif n'a été
effectué. L'audit CA-18 reste à corriger avant clôture d'E69 ; la migration seule
ne vaut pas recette des parcours, invitations ou permissions en cible.

### Prérequis des prochaines livraisons

Synthèse opératoire de la revue de clôture, valable pour chaque cible à renseigner
(test désormais migré, démo/production non modifiées). La V1.4 n'ajoute aucune variable ; les réglages
d'introduction d'E69 restent nécessaires.

| Composant | Action / ordre | Valeur ou défaut sans secret | Contrôle de réussite |
| --- | --- | --- | --- |
| Documentation projet | Publier le futur commit documentaire avant de construire la livraison backend | SHA publié à choisir ; aucun SHA local inventé | Guide E69 et alias présents dans cette révision |
| Base backend | Sauvegarder/inventorier ; en maintenance, appliquer les migrations manquantes v251, v252 puis v253 avant nouveau backend | Runner de migrations avec version/checksum ; pas de rejeu brut du SQL | Attributions GLOBAL/[], profils inchangés, versions incrémentées pour les seuls comptes convertis, admin préservé |
| Backend / liens email | Vérifier `LOCALEO_ERP_URL` | Origine HTTPS cible, sans chemin `/internal/erp` | Invitation pilote vers le bon hôte, initialisation possible |
| Backend / invitations | Configurer si nécessaire `LOCALEO_INTERNE_INVITATION_INTERVAL_SECONDS` et `LOCALEO_INTERNE_INVITATION_MAX_PER_DAY` | Respectivement **60** secondes et **5** invitations par compte sur 24 h par défaut | Renvoi contrôlé et suivi d'envoi ; aucun renvoi aveugle après résultat incertain |
| Mail / admin | Vérifier transport mail existant et configuration `LOCALEO_ADMIN_*` | Valeurs/secrets déjà provisionnés, jamais copiés dans ce bilan | Remise réelle contrôlée sur pilote ; accès admin et SQLAdmin toujours disponibles |
| Backend / bundle | Mettre à jour `SOURCE_REVISION` après publication, ou passer la révision publiée au préparateur ; reconstruire le bundle | Pin actuel `b496d3efaa07c8a3806d8a499270c06529a5df1f` insuffisant pour E69 | 119 sources locales, empreintes et lecture du guide contrôlées ; refaire sur artefact livré |
| Backend / lecteur | Vérifier l'emplacement documentaire effectif | Bundle `.runtime/documentation` ou `LOCALEO_DOCUMENTATION_ROOT` si chemin explicitement monté | `/internal/docs/knowledge/formation/gerer-utilisateurs-internes.md` accessible à l'admin |
| ERP et satellites embarqués | Livrer API, contrats et JS ERP/Support/Atelier/OnBoard ensemble | Même livraison backend ; aucun déploiement des trois frontends publics requis par E69 | Profils globaux, B+F, refus, retrait et révocation, cache/PWA, ancienne session et admin |
| Exploitation | Avant ouverture, vérifier le correctif CA-18 et la politique de conservation des emails expirés | Pas de nouvelle variable ni tâche de purge prétendue existante | Trace des refus attribuée sans secret ; procédure de rétention explicite |

### Séquence détaillée

1. Préparer sauvegarde et inventaire des accès réellement déployés sans extraire
   de secret ; contrôler l’admin historique et son registre indépendant.
2. Appliquer [v251 comptes](../../../../localeo-backend/sql/v251_comptes_internes.sql)
   puis [v252 Support](../../../../localeo-backend/sql/v252_support_financier.sql),
   puis `v253_scopes_internes_globaux.sql` pour l'évolution V1.4.
   v251/v252 ont leurs preuves locales historiques ; v253 a une preuve PostgreSQL
   locale distincte. Suivre son application unique via version/checksum, sans
   rejouer directement son SQL d'ajout de contrainte. Inventorier
   les comptes passant de COMMUNES à GLOBAL vide ; incrémenter `version` et
   `authorizationVersion` des seuls comptes modifiés, sans révoquer leurs sessions
   ni changer `securityVersion`. Aucun admin converti ni invitation envoyée.
   Appliquer v253 avant le nouveau backend, en maintenance avec commandes internes
   suspendues pour éviter des écritures concurrentes pendant la conversion. Le
   nouveau modèle rejette les lignes COMMUNES résiduelles. Aucune migration distante
   n'est exécutée par cette phase documentaire ; aucune nouvelle variable d'environnement.
3. Vérifier `LOCALEO_ERP_URL` (origine HTTPS, sans `/internal/erp`), transport mail
   et limites selon la [configuration des comptes internes](../../exploitation/technique/reference-configuration-environnement.md#comptes-internes-erp--epic-69) :
   LOCALEO_INTERNE_INVITATION_INTERVAL_SECONDS (60 défaut),
   LOCALEO_INTERNE_INVITATION_MAX_PER_DAY (5 défaut). Invitations 24 h, sessions
   15 min d’inactivité/8 h absolues ; limites login et mot de passe existantes,
   bcrypt borné en octets. Contrôler leurs valeurs effectives en cible.
4. Livrer backend, contrats et JS ERP/Support/Atelier/OnBoard ensemble. Garder les
   nouveaux comptes fermés avant vérification des projections/refus ; une ancienne
   session EXPLOITATION ne devient pas un compte nominatif.
5. Choisir une révision documentaire publiée contenant le guide E69 et les
   corrections du présent audit, puis préparer le bundle avec empreintes et vérifier
   sa lecture ERP. Le pin `SOURCE_REVISION` du
   [préparateur backend](../../../../localeo-backend/scripts/documentation/prepare_documentation.py)
   reste `b496d3efaa07c8a3806d8a499270c06529a5df1f` : cette révision ne contient
   ni le guide E69 ni son entrée d'export. Un build utilisant ce pin ne les embarque
   donc pas. La mise à jour du pin relève de la livraison après publication du SHA
   retenu ; elle n'est pas effectuée par cet audit documentaire.
   Créer un pilote autorisé ; recette invitation, profils globaux, B+F et
   accès autorisés sur plusieurs communes sans sélecteur territorial,
   retrait/révocation et SQLAdmin. Ces actions distantes restent à exécuter.

Retour arrière : fermer l’entrée nominative, révoquer liens/sessions, conserver
les données additives et reprendre par l’admin. Ne pas utiliser un artefact
interprétant un cookie nominatif comme admin, ni restaurer d’anciens secrets actifs.

## Guide backoffice

Source : [guide-backoffice.md](guide-backoffice.md). L’alias d’export
**docs/ops/formation/gerer-utilisateurs-internes.md** est ajouté au manifeste pour
le lecteur **/internal/docs/knowledge/formation/gerer-utilisateurs-internes.md**.
Gestion et guide réservés à l’admin historique. Un bundle temporaire réel de
119 documents a été construit, ses empreintes recontrôlées et la résolution du
guide par le lecteur ERP vérifiée en V1.3, puis le temporaire nettoyé. Cela ne
constitue pas une preuve de déploiement ; refaire le contrôle sur le bundle livré
depuis la révision documentaire publiée retenue à l'étape 5.

Contrôle documentaire du 2 octobre sur l'arbre local après corrections : sources
exportées valides, bundle temporaire de **119 documents** construit et empreintes
recontrôlées. Le lecteur réel du backend résout l'alias du guide E69 vers un contenu
identique à la source corrigée, sans le lien relatif ambigu vers `README.md`.
Le temporaire a été nettoyé ; aucun bundle distant ni configuration backend n'a
été modifié. Les contrôles des guides et des Markdown modifiés ont réussi ; les
tests métier consignés plus haut n'ont pas été rejoués pour cet audit.

Le contrat OpenAPI complet canonique E41 a été régénéré hors ligne : **673 chemins**.
Il contient les routes publiques et internes, sans annoncer qu’un serveur partagé
expose déjà ce contrat. Le contrôle des sources exportées a réussi sur **119 documents**.

## Lots de commit préparés — sans indexation

Les deux dépôts sont sur `main`. Le lot porte les modifications V1.4 déjà présentes
et les corrections bornées de cette revue ; **ce n'est pas un commit de clôture**.
La liste exacte des fichiers, SHA de base et empreintes SHA-256 est préparée dans
l'artefact local ignoré `.artifacts/epic69-cloture/preparation-commit.json` du dépôt
projet. Toute modification ultérieure impose de le renouveler. Aucun fichier
mixte E69/autre tâche n'a été identifié dans les lots retenus.

| Dépôt | Lot retenu | Message proposé |
| --- | --- | --- |
| `localeo-backend` | 25 fichiers : domaine/service/API comptes et contexte ERP ; permissions et utilisateurs UI ; générateur/rapport ; migration v253, compatibilité v252 précréée, runner et tests associés | `fix(epic69): appliquer les scopes globaux et fiabiliser la migration et la recherche` |
| `localeo-projet` | 16 fichiers : dossier E69, backlog/index/roadmap, OpenAPI E41, dépendances E65, identité et configuration | `docs(epic69): actualiser les scopes globaux et le bilan de cloture` |

Exclus du lot E69 : `.agents/skills/localeo-cloturer-epic/`,
`docs/organisation/codex.md`, `docs/organisation/cycle-epic.md` et
`docs/organisation/utiliser-workflows-codex.md`. Ils constituent la création du
workflow, tâche distincte déjà en attente ; message possible :
`chore(codex): ajouter le workflow de cloture des epics`. L'artefact les répertorie
séparément. Aucun artefact de démonstration privé, secret ou bundle n'est inclus.
Les trois dépôts frontends publics sont propres et hors lot.

Index Git laissés vides. Aucun commit, push, fusion ou déploiement effectué.
La migration de la base de test, exécutée ensuite sur demande explicite et
documentée ci-dessus, ne change pas ce constat concernant le code applicatif.
Après correction de CA-18, renouveler les preuves concernées et la revue de
clôture avant tout déplacement vers `terminees`.

## Bilan d’acceptation

Dépôts modifiés : backend (domaine, application, adaptateurs, ERP et satellites
embarqués, SQL, générateur, tests) et projet (spécifications, contrats, guide).
Aucun nouveau rôle interne dans les applications publiques Animation, Commerçant
ou Marketplace ; leurs populations d’authentification restent distinctes.
Bilan historique V1.3 : les décisions V1.2 étaient appliquées — récupération
administrée, Finance via Support et trois commandes métier Backoffice. La V1.4
conserve ces fonctions et remplace leurs portées territoriales par des scopes
globaux. Les preuves locales V1.4 sont consignées séparément ci-dessus. Cette
évolution reste **en cours** : la revue de clôture identifie le blocage **CA-18**
sur la traçabilité des refus. Les commits cités en tête ont été poussés ; les
modifications V1.4 et le correctif de recherche restent non committés. Les tests
V1.4 sont réutilisés, et la recette navigateur affectée a été réexécutée.
**L’EPIC reste en cours.** La revue de clôture n'avait exécuté aucune migration
distante ; l'intervention suivante a migré la base de test jusqu'à v253. Aucune
clôture ni recette applicative déployée n'est annoncée.
