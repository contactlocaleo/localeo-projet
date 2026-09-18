# Audit sécurité et performance de `localeo-backend`

Date de l'audit : 29 août 2026

Nature : audit statique du code, de la configuration et de l'historique Git local

État du document : actions à planifier

Périmètre : backend FastAPI, SQLAdmin, persistance SQLAlchemy/PostgreSQL, traitements batch, médias, WebPush et intégrations externes

## Objet du document

Ce document formalise les résultats de l'audit sécurité et performance du backend Localeo et constitue le registre de suivi des mesures correctives.

Deux familles d'identifiants sont utilisées :

- `ASP-SEC-NNN` : constat de sécurité issu de l'audit ;
- `ASP-PERF-NNN` : constat de performance ou de fiabilité ;
- `ASP-ACT-NNN` : action de remédiation traçable.

Un identifiant ne doit jamais être réutilisé, même si le constat ou l'action est abandonné. Toute pull request, tout commit et toute preuve de recette relatifs à cet audit doivent mentionner l'identifiant `ASP-ACT-NNN` correspondant.

### États autorisés pour une action

| État | Signification |
| --- | --- |
| `À planifier` | Action reconnue, non affectée ou non planifiée. |
| `Planifiée` | Responsable et échéance définis. |
| `En cours` | Implémentation ou procédure engagée. |
| `Bloquée` | Dépendance ou arbitrage empêchant l'avancement. |
| `À valider` | Réalisation terminée, preuves de recette à contrôler. |
| `Terminée` | Critères de clôture satisfaits et preuves référencées. |
| `Risque accepté` | Action non réalisée sur décision explicite, datée et justifiée. |

## Synthèse exécutive

Le verdict est **NO GO pour la poursuite normale des évolutions tant que la tranche 0 n'est pas clôturée**.

Deux constats P0 sont confirmés :

1. des secrets potentiellement exploitables sont versionnés dans les fichiers d'environnement et présents dans l'historique Git ;
2. une API publique accepte des SVG actifs puis les restitue inline sur le même domaine que le backoffice, créant un scénario de XSS stockée.

Les principaux risques complémentaires concernent les rendus HTML SQLAdmin, la protection du compte administrateur, la gestion des uploads, les paginations en mémoire, les requêtes N+1, l'envoi WebPush et l'exécution de DDL au démarrage des instances.

| Axe | P0 | P1 | P2 | P3 | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sécurité | 2 | 3 | 4 | 1 | 10 |
| Performance / fiabilité | 0 | 4 | 1 | 0 | 5 |
| **Total** | **2** | **7** | **5** | **1** | **15** |

## État des constats

L'état `CORRIGE` atteste qu'une modification de code ou de configuration a été
appliquée dans le dépôt. L'état `VALIDE` n'est ajouté qu'après la nouvelle passe
d'audit et l'exécution des contrôles associés. Une validation externe reste
nécessaire lorsque la clôture dépend d'un fournisseur ou de l'infrastructure.

| Identifiant | État de correction | État de validation | Commentaire |
| --- | --- | --- | --- |
| `ASP-SEC-001` | **CORRIGE (dépôt)** | Validation externe requise | Fichiers d'environnement retirés du suivi, exemple neutralisé, hook pre-commit et CI de scan de l'historique ajoutés. Rotation et purge de l'historique distant restent opérationnelles. |
| `ASP-SEC-002` | **CORRIGE** | **VALIDE** | Upload DAM authentifié, limité et soumis à quota ; formats raster vérifiés par signature, SVG retiré de l'IHM et refusé à l'entrée comme à la restitution, avec `nosniff`. |
| `ASP-SEC-003` | **CORRIGE** | **VALIDE** | Les libellés dynamiques des helpers SQLAdmin sont échappés et couverts par un test de régression XSS. |
| `ASP-SEC-004` | **CORRIGE** | **VALIDE** | Le login SQLAdmin réutilise le rate limiter persistant par identifiant et IP, avec remise à zéro après succès. |
| `ASP-SEC-005` | **CORRIGE** | **VALIDE** | Tous les chemins d'upload images et documentaires, API comme SQLAdmin, lisent par blocs et s'interrompent dès `limite + 1` octet. |
| `ASP-SEC-006` | **CORRIGE** | **VALIDE** | Toute écriture portant le cookie de session exige une preuve same-origin stricte (`Origin`, `Referer` ou Fetch Metadata), y compris sous `/public`, en complément de `SameSite=Lax`. |
| `ASP-SEC-007` | **CORRIGE** | **VALIDE** | Le cookie admin active `Secure` par défaut hors développement via une configuration explicite et documentée. |
| `ASP-SEC-008` | **CORRIGE** | **VALIDE** | Les schémas complets, protégés et internes ainsi que leurs Swagger exigent désormais une session admin ; seule la surface publique reste anonyme. |
| `ASP-SEC-009` | **CORRIGE** | **VALIDE** | Validation explicite de `Host` sans joker hors développement, rejet des hôtes étrangers et en-têtes globaux `nosniff`, anti-frame, referrer et permissions. |
| `ASP-SEC-010` | **CORRIGE** | **VALIDE** | Les retours du backoffice n'acceptent plus que les chemins admin/internal relatifs ou issus de l'hôte courant. |
| `ASP-PERF-001` | **CORRIGE** | **VALIDE** | Toutes les listes Animation inventoriées, y compris les commerçants/coffrets éligibles, appliquent recherche, filtres, total, ordre stable et pagination dans SQL. |
| `ASP-PERF-002` | **CORRIGE** | **VALIDE** | Résumés, validations, configurations, gains, flyers, bilans, actualités et couverture des coffrets sont chargés en lots à budget SQL constant par page. |
| `ASP-PERF-003` | **CORRIGE** | **VALIDE** | Réservation atomique avec `SKIP LOCKED`, lease renouvelé avant chaque envoi, abandon d'un claim perdu, abonnements groupés, timeout réseau et sémantique at-least-once documentée. |
| `ASP-PERF-004` | **CORRIGE** | **VALIDE** | Le bootstrap DDL et les seeds sont neutralisés en production ; les migrations versionnées pre-deploy deviennent obligatoires et la readiness reste non mutante. |
| `ASP-PERF-005` | **CORRIGE** | **VALIDE** | Pool SQLAlchemy explicitement borné, validé et configurable (`size`, débordement, timeout, recyclage et `pre_ping`) avec valeurs de départ documentées. |

## Contre-audit de validation

Le contre-audit a été exécuté après les correctifs, puis recommencé chaque fois
qu'il révélait un contournement ou une régression. Il a notamment conduit à
fermer les lectures SQLAdmin non bornées, la route DAM oubliée par le contrôle
CSRF, les paginations d'éligibilité, les N+1 des actualités et un tri SQL non
déterministe.

Contrôles finaux :

- **66 tests sécurité/backoffice réussis** : uploads, XSS, authentification
  admin, CSRF, cookie, OpenAPI, hôtes/en-têtes et redirections ;
- **96 tests performance/fiabilité ciblés réussis** : repositories Animation,
  bilans, flyers, participations, validations, WebPush, readiness, migration,
  pool et bootstrap ;
- **2 tests d'automatisation sécurité réussis** pour le hook pre-commit et la CI ;
- `git diff --check` réussi et worktree propre après les commits ;
- revue statique finale des transactions WebPush et des endpoints paginés.

Les validations ci-dessus portent sur les corrections contrôlables dans le
dépôt. Restent hors validation locale : rotation/révocation des secrets,
nettoyage coordonné de l'historique distant, vérification de la configuration
Render et du pre-deploy, mesures PostgreSQL réelles, `EXPLAIN ANALYZE`, alertes
et tests de charge sur données représentatives. Le premier passage de la
nouvelle CI doit également être observé ; le scan d'historique est censé rester
bloquant tant que la purge coordonnée n'a pas été réalisée.

État consolidé des actions :

- **validées dans le dépôt** : `ASP-ACT-004`, `006` à `009`, `013`, `015`,
  `018` à `025`, `027`, `028`, `033` et la partie budget SQL de `034` ;
- **corrigées côté application, complément d'exploitation requis** :
  `ASP-ACT-010`, `012`, `014`, `017` et `029` ;
- **corrigées, validation CI requise** : `ASP-ACT-031` et `032` ;
- **dépendantes d'une action externe ou de mesures d'environnement** :
  `ASP-ACT-001` à `003`, `005`, `011`, `016`, `026`, `030`, la partie
  latence de `034`, `035` et `036`.

## Périmètre et limites

L'audit couvre notamment :

- la composition des routeurs publics, protégés et internes ;
- les sessions, API keys et contrôles d'accès observables dans le code ;
- les uploads d'images et de documents ;
- les rendus du backoffice SQLAdmin ;
- les intégrations Stripe, Brevo et WebPush ;
- le bootstrap du schéma et la configuration SQLAlchemy ;
- les listes, agrégations et paginations du domaine Animation ;
- les fichiers suivis par Git et leur historique local.

L'audit n'inclut pas de test d'intrusion sur une instance déployée, de lecture d'une base distante, de test de charge réel, de validation de la configuration Render ni d'analyse dynamique des dépendances. Les constats signalés comme probables doivent être confirmés sur l'infrastructure cible.

## Registre des constats de sécurité

| Identifiant | Priorité | Confiance | Constat | Impact principal | Preuves | Effort indicatif | Risque de régression |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-SEC-001` | P0 | Confirmée | Secrets versionnés dans `.env.local`, `.env.test` et l'historique Git. | Compromission possible de l'administration, de la base, des paiements, de Brevo, du stockage, des API internes et des clés VAPID. | [`.env.local`](../../../../localeo-backend/.env.local#L1), [`.env.test`](../../../../localeo-backend/.env.test#L1), [session admin](../../../../localeo-backend/app/infrastructure/admin/auth.py#L47) | Moyen | Élevé si la rotation est incomplète ou mal ordonnancée. |
| `ASP-SEC-002` | P0 | Confirmée | Dépôt public de SVG actifs et restitution inline sur le domaine applicatif. | XSS stockée avec actions possibles dans le contexte d'une session administrateur. | [routeur public](../../../../localeo-backend/app/main.py#L328), [MIME autorisés](../../../../localeo-backend/app/api/images_api.py#L18), [upload](../../../../localeo-backend/app/api/images_api.py#L99), [restitution](../../../../localeo-backend/app/api/images_api.py#L145) | Moyen | Moyen pour les contenus éditoriaux utilisant des SVG. |
| `ASP-SEC-003` | P1 | Confirmée | Valeurs métier injectées dans `Markup` sans échappement systématique. | XSS stockée dans SQLAdmin via un nom ou libellé contrôlable. | [`_render_relation`](../../../../localeo-backend/app/infrastructure/admin/admin.py#L1131), [`_render_list`](../../../../localeo-backend/app/infrastructure/admin/admin.py#L1180) | Faible | Faible. |
| `ASP-SEC-004` | P1 | Confirmée | Connexion administrateur sans limitation de tentatives visible. | Force brute ou credential stuffing contre le compte administrateur global. | [authentification SQLAdmin](../../../../localeo-backend/app/infrastructure/admin/auth.py#L47) | Faible à moyen | Moyen derrière un proxy partageant une IP. |
| `ASP-SEC-005` | P1 | Confirmée | Corps d'upload chargés entièrement en mémoire avant contrôle de taille. | Déni de service mémoire ; consommation non bornée du stockage pour l'upload public. | [images](../../../../localeo-backend/app/api/images_api.py#L105), [documents](../../../../localeo-backend/app/api/documents_api.py#L157), [contrôle tardif](../../../../localeo-backend/app/application/documentaire/services/gestion_documentaire.py#L449) | Moyen | Faible si les limites fonctionnelles restent inchangées. |
| `ASP-SEC-006` | P2 | Confirmée sur l'absence de contrôle | Les écritures authentifiées par cookie ne disposent pas d'une protection CSRF explicite. | Action administrative non souhaitée dans certains scénarios same-site, sous-domaine compromis ou XSS. | [cookie de session](../../../../localeo-backend/app/main.py#L312), [écritures profils](../../../../localeo-backend/app/api/profils_commercants_api.py#L55), [écritures documents](../../../../localeo-backend/app/api/documents_api.py#L141) | Moyen | Moyen sur les formulaires et appels JavaScript existants. |
| `ASP-SEC-007` | P2 | Confirmée | Le cookie administrateur n'active pas explicitement l'attribut `Secure`. | Exposition du cookie si un environnement non local accepte une connexion HTTP. | [SessionMiddleware](../../../../localeo-backend/app/main.py#L312) | Faible | Faible, sous réserve que la production soit exclusivement HTTPS. |
| `ASP-SEC-008` | P2 | Confirmée | Les documentations et schémas OpenAPI protégés et internes sont publics. | Facilitation de la cartographie des routes et contrôles internes. | [Swagger protégé/interne](../../../../localeo-backend/app/main.py#L238), [OpenAPI protégé/interne](../../../../localeo-backend/app/main.py#L644) | Faible | Faible. |
| `ASP-SEC-009` | P2 | Probable | Absence dans le code d'une validation des hôtes et d'en-têtes de sécurité globaux. | Défense en profondeur incomplète ; état réel dépendant du proxy Render. | [middlewares applicatifs](../../../../localeo-backend/app/main.py#L249) | Faible | Moyen pour une CSP appliquée sans inventaire des scripts SQLAdmin. |
| `ASP-SEC-010` | P3 | Confirmée | Redirection du backoffice fondée directement sur `Referer`. | Redirection externe exploitable principalement pour du phishing. | [`_redirect_back`](../../../../localeo-backend/app/infrastructure/admin/admin.py#L1041) | Très faible | Faible. |

## Registre des constats de performance et de fiabilité

| Identifiant | Priorité | Confiance | Constat | Impact principal | Preuves | Effort indicatif | Risque de régression |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-PERF-001` | P1 | Confirmée | Plusieurs paginations sont appliquées après chargement complet des résultats. | Temps SQL et mémoire proportionnels au volume total, même pour une petite page. | [liste des animations](../../../../localeo-backend/app/api/animation_locale_api.py#L1301), [notifications](../../../../localeo-backend/app/api/animation_locale_api.py#L2290) | Élevé | Moyen sur le tri, le total et la stabilité des pages. |
| `ASP-PERF-002` | P1 | Confirmée | Requêtes N+1 sur les participants, validations, configurations et gains. | Plus de 200 requêtes possibles pour une page de 100 participants. | [participants](../../../../localeo-backend/app/api/animation_locale_api.py#L2354), [gains](../../../../localeo-backend/app/api/animation_locale_api.py#L1917) | Moyen | Moyen sur les agrégats et versions de configuration. |
| `ASP-PERF-003` | P1 | Confirmée | Appels WebPush réalisés dans une transaction longue, sans réservation atomique du lot. | Doublons entre workers, N+1 SQL, verrous prolongés et reprise fragile après erreur. | [sélection et envoi](../../../../localeo-backend/app/api/localeo_live_api.py#L941) | Élevé | Élevé ; la concurrence et l'idempotence doivent être recettées. |
| `ASP-PERF-004` | P1 | Confirmée | Création et rattrapage du schéma au démarrage, activés par défaut. | Démarrage lent, contention DDL et couplage entre disponibilité et droits de migration. | [activation par défaut](../../../../localeo-backend/app/config.py#L72), [appel au démarrage](../../../../localeo-backend/app/main.py#L260), [bootstrap](../../../../localeo-backend/app/bootstrap.py#L546) | Moyen | Élevé sans étape de migration pre-deploy fiable. |
| `ASP-PERF-005` | P2 | Probable | Pool SQLAlchemy non dimensionné ni durci explicitement. | Connexions périmées ou saturation selon le nombre de workers et la limite PostgreSQL. | [création du moteur](../../../../localeo-backend/app/infrastructure/persistence/db.py#L5) | Faible | Moyen si les valeurs sont choisies sans métriques. |

## Registre des actions

### Tranche 0 — Confinement immédiat

La tranche 0 bloque la reprise normale des développements fonctionnels.

| Identifiant | Constat lié | Action | Priorité | Dépendances | Effort | Responsable | Échéance | État | Critère de clôture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-ACT-001` | `ASP-SEC-001` | Inventorier les secrets présents dans les fichiers suivis et dans l'historique, sans reproduire leurs valeurs dans un ticket ou un log. | P0 | Aucune | Faible | À affecter | À définir | À planifier | Inventaire exhaustif des fournisseurs, environnements et propriétaires validé. |
| `ASP-ACT-002` | `ASP-SEC-001` | Révoquer et régénérer les secrets de base, admin, Stripe, Brevo, stockage S3, batchs internes et WebPush. | P0 | `ASP-ACT-001` | Moyen | À affecter | Immédiate | À planifier | Anciennes valeurs révoquées et nouvelles valeurs vérifiées dans chaque environnement. |
| `ASP-ACT-003` | `ASP-SEC-001` | Invalider toutes les sessions administrateur après rotation du secret de session. | P0 | `ASP-ACT-002` | Très faible | À affecter | Immédiate | Un ancien cookie signé ne permet plus d'accéder au backoffice. |
| `ASP-ACT-004` | `ASP-SEC-001` | Retirer `.env.local` et `.env.test` de l'index Git et fournir des exemples ne contenant que des valeurs factices. | P0 | `ASP-ACT-001` | Faible | À affecter | Immédiate | Aucun fichier d'environnement réel n'est suivi sur la branche principale. |
| `ASP-ACT-005` | `ASP-SEC-001` | Nettoyer l'historique Git selon une procédure coordonnée avec sauvegarde, gel des contributions et réinitialisation des clones. | P0 | `ASP-ACT-002`, `ASP-ACT-004` | Moyen | À affecter | À définir | Le scan de toutes les références Git ne retrouve plus les secrets identifiés. |
| `ASP-ACT-006` | `ASP-SEC-002` | Retirer immédiatement `image/svg+xml` des formats acceptés et refuser sa restitution inline. | P0 | Aucune | Faible | À affecter | Immédiate | Un SVG envoyé avec n'importe quel nom ou MIME est rejeté ; les SVG historiques ne sont plus actifs sur le domaine applicatif. |
| `ASP-ACT-007` | `ASP-SEC-002`, `ASP-SEC-005` | Protéger l'upload d'images par authentification, autorisation, rate limiting et quota. | P0 | Aucune | Moyen | À affecter | Immédiate | Un appel anonyme est refusé et les limites sont couvertes par des tests. |
| `ASP-ACT-008` | `ASP-SEC-002` | Décider puis mettre en œuvre la stratégie média cible : réencodage bitmap ou domaine média sans cookie. | P0 | `ASP-ACT-006` | Moyen | À affecter | À définir | Aucun contenu actif contrôlé par un utilisateur n'est servi dans l'origine du backoffice. |

### Tranche 1 — Sécurisation applicative

| Identifiant | Constat lié | Action | Priorité | Dépendances | Effort | Responsable | Échéance | État | Critère de clôture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-ACT-009` | `ASP-SEC-003` | Échapper toutes les valeurs dynamiques utilisées par `_render_relation`, `_render_list` et les helpers SQLAdmin équivalents. | P1 | Aucune | Faible | À affecter | À définir | Les charges `<script>` et `<img onerror>` sont affichées comme texte dans toutes les vues concernées. |
| `ASP-ACT-010` | `ASP-SEC-004` | Ajouter une limitation des tentatives de connexion par identifiant et adresse source avec délai progressif et journalisation. | P1 | Aucune | Moyen | À affecter | À définir | Le seuil configuré bloque temporairement les tentatives et produit un événement exploitable. |
| `ASP-ACT-011` | `ASP-SEC-004` | Définir la cible d'authentification admin : secret statique renforcé à court terme, comptes nominatifs et MFA avant le multi-opérateur. | P2 | Arbitrage d'exploitation | Moyen | À affecter | À définir | La décision est documentée et aucun compte partagé n'est utilisé. |
| `ASP-ACT-012` | `ASP-SEC-005` | Lire les uploads par blocs, interrompre la lecture au dépassement et définir une limite au proxy. | P1 | `ASP-ACT-007` pour les images | Moyen | À affecter | À définir | Un corps dépassant la limite est rejeté sans chargement intégral en mémoire. |
| `ASP-ACT-013` | `ASP-SEC-006` | Ajouter une protection CSRF aux routes d'écriture authentifiées par cookie et vérifier l'en-tête `Origin`. | P2 | Inventaire des formulaires | Moyen | À affecter | À définir | Une écriture sans preuve CSRF ou provenant d'une origine étrangère est refusée. |
| `ASP-ACT-014` | `ASP-SEC-007` | Activer le cookie `Secure` hors développement et documenter sa durée de vie. | P2 | HTTPS confirmé | Faible | À affecter | À définir | Les tests de production simulée observent `Secure`, `HttpOnly` et le `SameSite` attendu. |
| `ASP-ACT-015` | `ASP-SEC-008` | Désactiver ou protéger par session admin les Swagger et OpenAPI protégés et internes en production. | P2 | Aucune | Faible | À affecter | À définir | Un utilisateur anonyme ne peut pas récupérer les schémas protégés ou internes en production. |
| `ASP-ACT-016` | `ASP-SEC-009` | Auditer la configuration Render, puis répartir explicitement validation d'hôte et en-têtes de sécurité entre proxy et application. | P2 | Accès configuration Render | Faible | À affecter | À définir | La matrice des en-têtes et hôtes autorisés est documentée et testée. |
| `ASP-ACT-017` | `ASP-SEC-009` | Déployer les en-têtes manquants, dont `X-Content-Type-Options`, une politique de referrer et une politique iframe ; préparer la CSP à partir d'un inventaire. | P2 | `ASP-ACT-016` | Moyen | À affecter | À définir | Les en-têtes sont vérifiés automatiquement sans casser SQLAdmin. |
| `ASP-ACT-018` | `ASP-SEC-010` | Limiter les redirections de retour à des chemins relatifs ou à une liste d'origines autorisées. | P3 | Aucune | Très faible | À affecter | À définir | Un `Referer` externe ne provoque jamais une redirection hors des origines autorisées. |

### Tranche 2 — Performance des parcours critiques

| Identifiant | Constat lié | Action | Priorité | Dépendances | Effort | Responsable | Échéance | État | Critère de clôture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-ACT-019` | `ASP-PERF-001` | Inventorier toutes les listes paginées après matérialisation complète et définir leur tri stable. | P1 | Aucune | Faible | À affecter | À définir | L'inventaire couvre route, repository, filtres, tri, total et volume cible. |
| `ASP-ACT-020` | `ASP-PERF-001` | Déplacer filtres, tri, total et limitation dans les repositories SQL, avec curseur lorsque le volume le justifie. | P1 | `ASP-ACT-019` | Élevé | À affecter | À définir | La mémoire et le nombre de lignes chargées restent bornés par la taille de page. |
| `ASP-ACT-021` | `ASP-PERF-002` | Regrouper le chargement des validations et configurations nécessaires aux pages de participants. | P1 | Aucune | Moyen | À affecter | À définir | Le nombre de requêtes reste constant entre une page de 10 et de 100 participants. |
| `ASP-ACT-022` | `ASP-PERF-002` | Charger en lot les instances et statistiques de prestations utilisées par la consommation des gains. | P1 | Aucune | Moyen | À affecter | À définir | Le nombre de requêtes ne croît plus linéairement avec le nombre de gains. |
| `ASP-ACT-023` | `ASP-PERF-003` | Mettre en place une réservation atomique des notifications WebPush avec état `EN_COURS` et verrouillage compatible multi-workers. | P1 | Conception de reprise | Élevé | À affecter | À définir | Deux workers concurrents ne peuvent pas réclamer la même notification. |
| `ASP-ACT-024` | `ASP-PERF-003` | Effectuer les appels WebPush hors transaction longue, puis enregistrer chaque résultat dans une transaction courte. | P1 | `ASP-ACT-023` | Moyen | À affecter | À définir | Une destination lente ne maintient pas de transaction SQL ouverte et un échec n'annule pas tout le lot. |
| `ASP-ACT-025` | `ASP-PERF-003` | Précharger les abonnements du lot et définir timeouts, reprise et idempotence des envois. | P1 | `ASP-ACT-023` | Moyen | À affecter | À définir | Absence de N+1 sur le lot et comportement de reprise documenté et testé. |

### Tranche 3 — Déploiement et base de données

| Identifiant | Constat lié | Action | Priorité | Dépendances | Effort | Responsable | Échéance | État | Critère de clôture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-ACT-026` | `ASP-PERF-004` | Rendre obligatoire l'application des migrations dans l'étape pre-deploy. | P1 | Pipeline de déploiement | Moyen | À affecter | À définir | Un échec de migration empêche le déploiement de la nouvelle version. |
| `ASP-ACT-027` | `ASP-PERF-004` | Activer `LOCALEO_SKIP_BOOTSTRAP=true` en production après sécurisation du pre-deploy. | P1 | `ASP-ACT-026` | Faible | À affecter | À définir | Aucun worker applicatif n'exécute de DDL au démarrage. |
| `ASP-ACT-028` | `ASP-PERF-004` | Ajouter au readiness un contrôle non mutant de compatibilité du schéma critique. | P1 | `ASP-ACT-026` | Moyen | À affecter | À définir | Une instance au schéma incompatible reste non prête avec un diagnostic exploitable. |
| `ASP-ACT-029` | `ASP-PERF-005` | Mesurer les connexions par instance et dimensionner `pool_size`, `max_overflow`, `pool_timeout`, `pool_pre_ping` et `pool_recycle`. | P2 | Métriques PostgreSQL/Render | Faible | À affecter | À définir | La somme des pools reste sous la limite PostgreSQL et les connexions périmées sont récupérées proprement. |
| `ASP-ACT-030` | `ASP-PERF-001`, `ASP-PERF-002`, `ASP-PERF-005` | Exécuter des `EXPLAIN ANALYZE` sur données représentatives et créer uniquement les index composites justifiés. | P2 | Données de préproduction anonymisées | Moyen | À affecter | À définir | Chaque index ajouté possède une requête cible, une mesure avant/après et un contrôle du coût d'écriture. |

### Tranche 4 — Prévention et surveillance continue

| Identifiant | Constat lié | Action | Priorité | Dépendances | Effort | Responsable | Échéance | État | Critère de clôture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ASP-ACT-031` | `ASP-SEC-001` | Ajouter un scanner de secrets en pre-commit et dans la CI, incluant l'historique des branches proposées. | P1 | `ASP-ACT-004` | Faible | À affecter | À définir | Une fixture contenant un faux secret connu fait échouer la CI. |
| `ASP-ACT-032` | Tous les constats sécurité | Ajouter une analyse de dépendances et une revue SAST Python/FastAPI à la CI. | P2 | Aucune | Faible | À affecter | À définir | Les rapports sont archivés et une politique de blocage par sévérité est documentée. |
| `ASP-ACT-033` | `ASP-SEC-002` à `ASP-SEC-010` | Créer une suite de régression sécurité dédiée aux uploads, sessions, CSRF, rendus HTML, redirections et documentation interne. | P1 | Correctifs correspondants | Moyen | À affecter | À définir | Chaque constat corrigé possède au moins un test qui échouait avant correction. |
| `ASP-ACT-034` | `ASP-PERF-001`, `ASP-PERF-002` | Définir un budget de requêtes SQL et de latence pour les endpoints d'animation critiques. | P2 | `ASP-ACT-020` à `ASP-ACT-022` | Moyen | À affecter | À définir | Les budgets sont vérifiés sur des jeux de 10, 25 et 100 éléments. |
| `ASP-ACT-035` | `ASP-PERF-003`, `ASP-PERF-005` | Exposer et superviser durée des batchs, taille des lots, reprises, doublons, pool SQL et requêtes lentes. | P2 | Actions de tranches 2 et 3 | Moyen | À affecter | À définir | Dashboard et alertes disposent de seuils, propriétaires et procédure de réaction. |
| `ASP-ACT-036` | Tous les constats performance | Mettre en place un test de charge reproductible sur des volumes représentatifs. | P2 | Environnement de préproduction | Moyen | À affecter | À définir | Scénario, données, résultats de référence et seuils d'échec sont versionnés. |

## Ordonnancement recommandé

```text
ASP-ACT-001 ──> ASP-ACT-002 ──> ASP-ACT-003
       │               └──────> ASP-ACT-005
       └──────> ASP-ACT-004 ──> ASP-ACT-031

ASP-ACT-006 ──> ASP-ACT-008
ASP-ACT-007 ──> ASP-ACT-012

ASP-ACT-019 ──> ASP-ACT-020 ──> ASP-ACT-034
ASP-ACT-023 ──> ASP-ACT-024 ──> ASP-ACT-025
ASP-ACT-026 ──> ASP-ACT-027
       └──────> ASP-ACT-028
```

Les actions `ASP-ACT-001` à `ASP-ACT-008` constituent le chemin de confinement. Les actions indépendantes de la tranche 1 peuvent ensuite être développées en parallèle. Les optimisations SQL doivent être précédées de mesures et suivies de budgets automatisés.

## Critères de levée du NO GO

Le NO GO de l'audit peut être levé lorsque :

- `ASP-ACT-001` à `ASP-ACT-008` sont à l'état `Terminée` ;
- les anciennes sessions et valeurs secrètes ont été invalidées ;
- aucun upload anonyme ou SVG actif n'est accepté ;
- `ASP-ACT-009`, `ASP-ACT-010` et `ASP-ACT-012` sont terminées ;
- les tests de sécurité ciblés sont verts ;
- les preuves de clôture sont référencées dans le tableau de suivi ci-dessous.

La levée du NO GO ne clôt pas les actions P2 et P3 : elles restent suivies jusqu'à réalisation ou acceptation formelle du risque.

## Tableau de suivi des preuves

Ce tableau est à compléter au fil des réalisations. Une action ne passe à `Terminée` qu'après ajout d'une preuve vérifiable.

| Action | Pull request / commit | Tests ou preuve opérationnelle | Validé par | Date | Commentaire |
| --- | --- | --- | --- | --- | --- |
| `ASP-ACT-001` |  |  |  |  |  |
| `ASP-ACT-002` |  |  |  |  |  |
| `ASP-ACT-003` |  |  |  |  |  |
| `ASP-ACT-004` |  |  |  |  |  |
| `ASP-ACT-005` |  |  |  |  |  |
| `ASP-ACT-006` |  |  |  |  |  |
| `ASP-ACT-007` |  |  |  |  |  |
| `ASP-ACT-008` |  |  |  |  |  |

Pour les actions suivantes, ajouter une ligne au moment de leur passage à `Planifiée` afin de conserver ce tableau lisible.

## Tests de validation attendus

### Sécurité

- refus d'un upload image anonyme ;
- refus d'un SVG, d'un fichier polyglotte et d'un MIME usurpé ;
- rejet d'un corps trop volumineux avant sa lecture complète ;
- affichage littéral de `<script>` et `<img onerror>` dans SQLAdmin ;
- invalidation des anciens cookies après rotation du secret ;
- présence de `Secure`, `HttpOnly` et du `SameSite` attendu en configuration de production ;
- rejet d'une écriture sans preuve CSRF ou avec une origine étrangère ;
- limitation des tentatives de connexion ;
- impossibilité de consulter les schémas internes anonymement ;
- refus des redirections vers une origine externe.

### Performance et fiabilité

- nombre constant de requêtes pour 10, 25 et 100 participants ;
- pagination testée avec 10 000 puis 100 000 animations ;
- absence de doublon avec deux workers WebPush concurrents ;
- reprise correcte après échec d'une destination WebPush ;
- démarrage simultané de plusieurs workers sans DDL ;
- readiness négatif sur un schéma incompatible ;
- contrôle des limites de pool sous le nombre maximal d'instances prévu.

## Points positifs conservés comme exigences

Les remédiations ne doivent pas dégrader les protections déjà présentes :

- API keys internes hachées, comparaison constante et contrôle de scope : [`api_keys.py`](../../../../localeo-backend/app/security/api_keys.py#L27) ;
- validation des signatures Stripe et Stripe Connect : [`paiement_gateway.py`](../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py#L140), [`stripe_connect_gateway.py`](../../../../localeo-backend/app/infrastructure/paiement/stripe_connect_gateway.py#L378) ;
- refus des secrets manquants et des valeurs admin faibles hors développement : [`config.py`](../../../../localeo-backend/app/config.py#L521) ;
- réponses génériques pour les erreurs techniques inattendues : [`main.py`](../../../../localeo-backend/app/main.py#L892) ;
- timeouts explicites sur les appels Brevo et de l'ordonnanceur ;
- contrôles de tenant et idempotence sur les parcours Animation ;
- signature HMAC des curseurs de pagination.

## Commandes de contrôle recommandées

À exécuter après mise en œuvre des actions concernées :

```powershell
python -m pytest -q
python -m pytest tests/security tests/api -q
python -m pip_audit -r requirements.txt
git diff --check
git status --short --branch
```

Le nettoyage d'historique Git est une opération coordonnée et potentiellement destructive. Il doit faire l'objet d'une procédure dédiée ; aucune commande de réécriture automatique n'est prescrite par ce document.
