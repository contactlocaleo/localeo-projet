# Audit Localeo Animation et backend — 5 septembre 2026

> **Mise à jour après corrections — 5 septembre 2026.** Les sections A à E
> conservent les constats, preuves et recommandations de l'audit initial, établis
> avant correction. Elles ne décrivent donc pas toutes l'état actuel du code.
> Les douze constats F01–F12 ont depuis reçu des correctifs, tests et mises à jour
> de spécification, commités et poussés. La section F, en fin de rapport, fait foi
> pour leur suivi et distingue correction du code, validation locale et recette
> restant à réaliser. Aucun déploiement ni validation de production n'est attesté.

## A. Résumé exécutif

**Risque global estimé lors de l'audit initial : élevé sur la fiabilité des parcours de souscription et d'animation.** Il ne s'agit pas d'une preuve de compromission ni d'une certification de sécurité. L'analyse initiale était statique, complétée par les vérifications frontend locales. Les tests ajoutés pendant les corrections sont recensés en section F ; la validation de concurrence sur PostgreSQL isolé reste à réaliser. Le risque résiduel de production n'a pas été réévalué.

Les modifications ont été commitées et poussées sur `origin/main` avant l'audit :

- Portail `localeo-animation` : `68ba6ae` — `feat(animation): add draft cancellation and quota usage display`.
- `localeo-backend` : `57b4fba` — `feat(animation): cancel drafts and release subscription quota`.

Ces push précédaient les correctifs d'audit. Le rapport initial a ensuite été
commité et poussé dans `localeo-animation` sous `9164e8c`. Les commits de correction
sont détaillés en section F.

### Cinq risques prioritaires

1. Une erreur pendant l'activation d'une souscription peut laisser des droits actifs alors que la commande passe en rapprochement ; la répétition du même webhook ne répare pas cet état (F01).
2. Deux publications concurrentes peuvent dépasser le quota du même abonnement (F02).
3. Les mots de passe initiaux sont conservés en clair dans les emails sortants persistés ; leur confidentialité dépend aussi de l'outbox, de ses exports et de ses sauvegardes (F03).
4. L'annulation d'un brouillon peut remettre plusieurs cycles d'invitation dans l'état « courant », incompatible avec l'unicité en base (F04).
5. La sélection des coffrets ne parcourt que la première page, filtrée ensuite par conformité : des coffrets vendables deviennent invisibles (F05).

Conséquences possibles : accès incohérents après encaissement, crédits dépassés, support manuel, animation impossible à annuler ou à configurer, exposition d'identifiants après accès non autorisé aux emails stockés. Aucune perte financière ni fuite effective n'a été observée.

### Points forts observés

- Contrôle global des routes internes, vérification des sessions Animation et contrôles partenaire/commune sur les parcours examinés.
- Signature Stripe vérifiée avant distribution ; vérification du statut payé, du montant et de la devise dans le traitement des souscriptions.
- Transactions, outbox et contraintes d'unicité déjà présentes ; verrouillage de plusieurs ressources métier, dont les animations.
- CSP et en-têtes de sécurité dans Nginx ; protection d'origine pour les écritures avec cookie d'administration.
- Contrôles de formats documentaires et limitation des uploads présents dans le code.
- CI frontend avec typage, lint, tests et build ; CI backend déclarant Gitleaks, pip-audit et Bandit. Leur présence n'atteste pas du résultat des dernières exécutions distantes.

**Rectification du diagnostic antérieur :** l'absence de garde au niveau du seul routeur Epic 47 ne démontrait pas un accès public. `B:app/main.py:294` protège globalement `/internal/` (contrôle effectif à partir de la ligne 334). La garde ajoutée au routeur constitue une défense supplémentaire, pas la preuve d'une ancienne exposition anonyme.

### Effort indicatif

Prévoir **15 à 25 jours-personne**, recette incluse, pour les corrections prioritaires, tests PostgreSQL de concurrence, parcours frontend et sécurisation de l'invitation. Estimation de planification, non devis ; les charges des constats se recouvrent. Ajouter une campagne infrastructure/exploitation dont l'effort dépendra des accès et de l'environnement fourni. Priorité immédiate : F01–F04 et tests de non-régression de F05–F07.

## Périmètre, méthode et limites

### Cartographie

| Composant | Responsabilité et flux | Frontière de confiance |
| --- | --- | --- |
| React 18 / TypeScript / Vite, servi par Nginx | Session navigateur, appels HTTP, création/configuration/publication d'animations | Navigateur non fiable ; permissions à revérifier côté API |
| FastAPI / SQLAlchemy | API Animation, backoffice, règles métier, persistence | Session Bearer Animation ou cookie administrateur ; cloisonnement partenaire/commune |
| PostgreSQL | Commandes, abonnements, quotas, invitations versionnées, audit et outbox | Atomicité, unicité et concurrence interrequêtes |
| Stripe | Checkout et webhooks signés | Service externe ; doublons, délais et rapprochements possibles |
| Emails, documents et tâches planifiées | Invitations, notifications d'échéance, flyers | Persistence de contenus sensibles, reprises et supervision |

Les versions ci-dessus proviennent du code et des manifestes, pas d'une inspection de production. Le backend est un monolithe modulaire avec couches domaine/application/infrastructure ; le service de souscription utilise directement les ORM et orchestre paiement, droits, emails et audit. Cette concentration explique le risque concret F01, sans justifier à elle seule un passage aux microservices.

Les références `F:` désignent la racine de `localeo-animation`, `B:` celle du dépôt voisin `localeo-backend`. Les numéros de ligne correspondent aux sources examinées aux commits indiqués.

Lecture ciblée : accès et middlewares, client HTTP et session, souscriptions et quotas, webhook Stripe, annulation et cycles d'invitation, coffrets/BUM, modèles ORM, configuration de persistence, uploads, CI et tests. Recherche de sinks dangereux et de documentation d'exploitation ; pas de revue exhaustive ligne à ligne de toutes les fonctionnalités du backend.

Aucun accès aux secrets `.env`, aucune donnée client consultée, aucun test d'intrusion, aucune charge, migration ou écriture de base. Les recherches documentaires externes ne contenaient ni code privé ni donnée métier. Les contrôles fonctionnels backend décrits ci-dessous sont **proposés**, pas exécutés.

Manquent pour conclure sur l'exploitation réelle : topologie et versions déployées, configuration effective non secrète, isolation PostgreSQL, volumes, traces et métriques anonymisées, historique CI, inventaire des dépendances réellement installées, politiques de conservation, sauvegardes et preuve de restauration, RPO/RTO/SLO, préproduction jetable avec Stripe simulé. Aucun interpréteur `python`/`py` n'était trouvé par `Get-Command` ; les tests Python n'ont pas été exécutés. Cela ne prouve pas l'absence de tout environnement Python sur le poste.

### Vérifications locales exécutées

| Vérification | Résultat et portée |
| --- | --- |
| `npm.cmd test` | 14 tests réussis ; principalement contrats textuels, pas des parcours navigateur |
| `npm.cmd run typecheck` | Réussi, aucune erreur TypeScript remontée |
| `npm.cmd run lint` | Réussi, aucune erreur ESLint remontée |
| `npm.cmd run build` | Réussi ; Vite indique 1 629 modules et 873 ms pour ce build local |
| `corepack.cmd pnpm audit --json` | Premier essai bloqué par `EACCES` réseau ; nouvel essai autorisé réussi : 414 dépendances rapportées, zéro avis de vulnérabilité à cette date. Ne couvre ni Python ni les images système |
| Parsing JSON des deux copies [docs/specifications/epic-41-api/openapi.json](../../specifications/epic-41-api/openapi.json) | JSON valides et copies identiques lors du contrôle préalable au commit |
| `git … diff --cached --check` avec `core.whitespace=cr-at-eol` | Réussi avant commit ; prise en compte des fins de ligne Windows |
| Inspection Git et push des deux dépôts | Push réussis sur `origin/main` ; pas une preuve de déploiement |

Build mesuré : bundle principal JS **468,95 kB / 121,93 kB gzip**, CSS **125,78 kB / 20,35 kB gzip**. Ces valeurs proviennent de Vite, pas d'un transfert réseau observé. Elles ne démontrent pas un problème de chargement : aucune mesure LCP, INP, p50/p95/p99, débit, consommation mémoire ou temps SQL n'est disponible. Ne pas convertir le temps de build en temps de réponse utilisateur.

## B. Tableau des constats

« Confirmé » signifie démontré dans le code, sauf mention explicite de test exécuté. Les probabilités sont qualitatives et conditionnelles, non des fréquences mesurées. P1 : prioritaire ; P2 : planifié. Aucun constat critique d'exploitation anonyme n'est établi.

| ID | Domaine | Constat | Preuve | Criticité | Impact | Probabilité | Correction | Effort | Priorité | Confiance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | Transactions / paiement | Activation partielle conservable après erreur ; replay ignoré | `B:app/application/abonnements_plateforme/service_souscriptions.py:232,291,338` | Élevée | Droits et paiement désynchronisés | Moyenne, si erreur en cours d'activation | Frontière transactionnelle et reprise explicite | 3–5 j | P1 | Mécanisme confirmé ; incident fortement probable sous injection d'erreur |
| F02 | Concurrence / quota | Comptage puis insertion sans verrou d'abonnement | Même fichier `:366` ; modèles `:2068` | Élevée | Publication au-delà du crédit acheté | Moyenne, si publications simultanées | Verrou commun ou allocation atomique | 1–2 j | P1 | Fortement probable ; interleaving non exécuté |
| F03 | Confidentialité | Mot de passe initial en clair dans l'outbox | Même service `:520` ; `B:app/infrastructure/persistence/mappers.py:755` | Élevée | Compromission de compte si lecture des contenus persistés | Conditionnelle à un accès outbox/export | Invitation à usage unique et durée limitée | 2–4 j | P1 | Stockage confirmé ; aucune fuite observée |
| F04 | Intégrité / invitations | Annulation transforme aussi les anciens cycles en courants | `B:app/application/animation_locale/services/gestion_animations.py:274` | Élevée | Annulation en échec / historique altéré | Moyenne, si ancien cycle non annulé | Ne traiter que les demandes courantes autorisées | 1–2 j | P1 | Chemin confirmé ; collision fortement probable |
| F05 | Fonctionnel / pagination | Coffrets vendables masqués après la page 1 | `F:src/app/api.ts:814` ; `B:app/api/animation_locale_api.py:1297` | Moyenne | Configuration impossible ou incomplète | Élevée dès volume suffisant | Éligibilité avant pagination et navigation complète | 1–3 j | P1 | Confirmé par les deux contrats de code |
| F06 | Emails / disponibilité | Le deuxième renvoi de paiement échoue avec plusieurs emails | Service souscriptions `:179,463` | Moyenne | Relance de paiement cassée | Élevée après deux emails conservés | Existence booléenne, clé de session, renvoi distinct | 0,5–1 j | P1 | Confirmé statiquement |
| F07 | Onboarding | Déduplication des invitations par partenaire et non gestionnaire | Service souscriptions `:512` | Moyenne | Nouveau gestionnaire sans invitation | Élevée pour un second gestionnaire du partenaire | Clé d'invitation par gestionnaire/cycle | 1–2 j | P1 | Confirmé statiquement |
| F08 | Machine à états | Commande annulée réactivable par action admin | Service souscriptions `:137,191,202` | Moyenne | Annulation administrative non terminale | Moyenne, action admin nécessaire | Transitions explicites et verrouillage | 1–2 j | P2 | Contrôle manquant confirmé ; règle métier à valider |
| F09 | Performance | Travail SQL synchrone dans webhook `async` | `B:app/api/stripe_platform_api.py:61` | Moyenne | Blocage du worker événementiel sous trafic | Conditionnelle aux durées et concurrence | Threadpool borné ou worker durable | 1–3 j | P2 | Chemin bloquant confirmé ; impact non mesuré |
| F10 | Performance SQL | Vérification BUM par coffret dans une boucle | API coffrets `:1303` ; service BUM `:204` | Moyenne | Nombre de requêtes proportionnel à la page | Élevée sur pages remplies | Chargement groupé et politique lue une fois | 1–2 j | P2 | Forme N+1 confirmée ; latence inconnue |
| F11 | Sessions navigateur | Jeton Bearer persistant dans localStorage | `F:src/app/auth.ts:8` | Moyenne | Vol de session si script hostile exécuté | Non établie, XSS non démontrée | Session HttpOnly ou stratégie mémoire adaptée | 2–4 j | P2 | Stockage confirmé ; exploitation hypothétique |
| F12 | Planification | Alertes d'échéance sans rattrapage des jours manqués | Service souscriptions `:415` | Moyenne | Notification perdue, statut administratif périmé | Moyenne après indisponibilité du job | Rattrapage borné et expiration indépendante | 1–2 j | P2 | Confirmé statiquement |

### F01 — Une erreur ne remet pas les droits créés à zéro

`_activer_commande` insère et flush les abonnements actifs (318–340), puis active les gestionnaires/habilitations et prépare leurs invitations (342–354). Le `except Exception` appelant (293–299) ne rollback pas ces changements : il passe seulement commande et souscriptions en `A_RECONCILIER`, puis commit. Une exception applicative après le premier flush peut donc conserver les droits déjà créés. Une exception SQL peut, elle, rendre la transaction inutilisable et faire échouer ce commit.

Le dédoublonnage (232–236) considère toute trace existante comme traitée, y compris `ECHEC`. Cela interdit une reprise automatique par répétition du même événement ; il faut un rapprochement explicite, pas supprimer arbitrairement la trace. Le simple état `A_RECONCILIER` peut être un choix métier valide, mais il ne compense pas les effets partiels.

Reproduction sûre à ajouter : commande test de deux communes ; injecter une `RuntimeError` dans `_preparer_invitation`, après les insertions d'abonnements. Vérifier dans une nouvelle session si des abonnements `ACTIF` subsistent avec commande `A_RECONCILIER`. Rejouer le même événement ; constater le retour `already_processed`. Répéter avec erreur SQL et vérifier absence de session empoisonnée.

Compensation proposée : alerte sur chaque rapprochement, contrôle croisé paiement/droits et procédure opérateur idempotente. Ne pas désactiver ni supprimer aveuglément des droits de clients payants. La gestion des savepoints et du rollback est documentée par [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html).

### F02 — Le verrou d'une animation ne protège pas le quota commun

Le comptage des consommations actives (379–384) précède une insertion sans verrou sur l'abonnement. L'unicité porte sur `(abonnement_id, animation_id, type_consommation)`, pas sur un plafond. `publication_animation.py:188` appelle ce code ; `abonnements_plateforme_repositories.py:67` ne verrouille pas non plus l'abonnement courant.

Scénario PostgreSQL isolé, isolation READ COMMITTED : quota 1, deux animations distinctes A/B ; synchroniser les deux transactions après leur comptage à zéro, puis insérer et commit. L'unicité A/B n'empêche pas les deux consommations. Une isolation SERIALIZABLE et une gestion correcte des retries pourraient changer le résultat ; configuration effective inconnue.

Compensation : sérialiser temporairement les publications du même abonnement côté service/opérations et surveiller `used > quota`. Un bouton désactivé côté navigateur ne protège pas plusieurs onglets ou workers.

### F03 — Un hash correct ne protège pas la copie dans l'email

Le mot de passe est généré aléatoirement puis hashé pour le gestionnaire, mais intégré aux corps HTML et texte (520–527). `from_email_sortant` copie les corps en base (`mappers.py:762`) dans des colonnes Text (`models.py:1037`). Le problème démontré est cette seconde copie lisible, non une faiblesse prouvée de l'aléa ou du hash.

Validation sans donnée réelle : inviter un gestionnaire fictif, vérifier que l'outbox ne contient plus de mot de passe après correction ; tester consommation unique, expiration et révocation du lien. Une invitation à usage unique reste sensible dans l'email, mais ne doit plus permettre une connexion durable après activation.

Compensation : restreindre les accès aux contenus et exports d'emails, vérifier rétention et sauvegardes, privilégier la réinitialisation sécurisée. Aucune purge des emails existants sans analyse de conservation et validation. Le chiffrement disque ne suffit pas contre un lecteur autorisé de l'outbox.

### F04 — Annulation et unicité du cycle courant

`lister_par_animation` retourne **tous** les cycles (`animation_locale_repositories.py:644`). L'annulation ignore seulement `ANNULEE` et impose `conserver_courante=True` aux autres. La méthode domaine (`demande_participation_commercant.py:136`) affecte directement `est_courante`. L'index partiel `uq_animation_demande_participation_courante` (`models.py:1727`) n'autorise qu'une demande courante par animation/commerçant.

Fixture isolée : ancien cycle `REFUSEE`, `est_courante=False`, et cycle récent courant pour le même commerçant ; annuler le brouillon. Le traitement tente de conserver les deux courants et entre en conflit avec l'index. L'Unit of Work rollback en cas d'exception : on anticipe un échec d'annulation, pas une corruption silencieuse de la base. Avec un seul cycle, le refus est transformé en annulation ; confirmer séparément si cette présentation est la règle attendue pour une annulation complète du jeu.

Compensation : ne pas modifier manuellement les cycles pour forcer le passage ; diagnostiquer les animations concernées en lecture seule. Ce constat concerne **l'annulation du brouillon**, pas une preuve que le correctif d'ajout de commerçant est encore défaillant.

### F05 — Filtrage correct, mais ensemble incomplet

Le portail demande `eligible=true` sans page ni collecte de pages. Le backend limite à 25 candidats (`animation_locale_api.py:1283`), effectue le filtre SQL statut/couverture puis `offset/limit` (`animation_locale_repositories.py:346–355`), et applique la conformité BUM **après** cette limite (1302–1312). Le total du repository est jeté ; la réponse reste une liste.

Fixture : 26 coffrets actifs ordonnés, 25 premiers bloqués BUM, 26e vendable. La requête du sélecteur renvoie une liste vide. Même sans blocage BUM, le 26e ne peut pas être atteint par cet appel. Ne pas résoudre en supprimant simplement la limite : filtrer intégralement avant pagination et fournir un contrat paginé stable, puis adapter le sélecteur.

Compensation : diagnostic en préproduction avec jeu de données représentatif ; ne pas rendre artificiellement vendables les coffrets bloqués pour contourner le problème.

### F06 — Le renvoi rend sa propre requête non scalaire

Le premier email est inséré ; un premier renvoi `force=True` ajoute un deuxième email du même type/source. Le renvoi suivant exécute `scalar_one_or_none()` sur les deux lignes **avant** de tester `force`. Il provoque donc `MultipleResultsFound` si ces emails sont conservés. De plus, une nouvelle session Checkout peut être créée sans nouvel email, car la déduplication ne distingue pas les sessions.

Test isolé : checkout initial, deux renvois successifs ; attendre trois emails et aucune erreur. Puis expirer le lien, créer une nouvelle session simulée et vérifier que l'email contient le nouveau lien. Compensation : éviter les renvois répétés tant que le défaut n'est pas corrigé, avec procédure opérateur contrôlée.

### F07 — Invitation partagée entre gestionnaires du même partenaire

La recherche de l'invitation (`service_souscriptions.py:513–517`) utilise seulement type et `manager.partenaire_id`. Si un premier gestionnaire a déjà son email persisté, l'activation ultérieure d'un autre gestionnaire du même partenaire retourne à la ligne 519 avant de préparer son accès.

Test : deux gestionnaires distincts, même partenaire, activations successives sur communes distinctes sans abonnement concurrent ; vérifier une invitation adressée à chacun. Réactiver le même dossier ne doit pas régénérer son mot de passe ni dupliquer l'invitation. Compensation : vérifier la livraison par gestionnaire et utiliser le parcours de réinitialisation autorisé, sans envoyer de mot de passe manuellement.

### F08 — États terminaux insuffisamment protégés

`creer_checkout` refuse les montants gratuits et les commandes `PAYEE`, mais pas `ANNULEE`. Après appel Stripe, il réécrit l'état en `PAIEMENT_EN_COURS`. `activer_gratuitement` vérifie montant zéro et confirmation `OUI`, pas l'annulation. Ce sont des actions administratives protégées ; **pas un contournement d'authentification démontré**.

Test : annuler une commande test puis appeler chaque action admin appropriée avec Stripe simulé. Attendre un refus avant tout appel externe ou création de droits, sauf si la réouverture est une fonctionnalité explicitement autorisée et auditée. Compensation : masquer les actions incohérentes dans le backoffice, sans considérer le masquage comme une protection serveur suffisante.

### F09–F10 — Goulots structurels, sans chiffre de latence inventé

F09 : après `await request.body()`, le webhook appelle directement le traitement synchrone et SQLAlchemy. Ce code ne devient pas non bloquant parce que la route est `async`. Le hash d'invitation peut aussi s'exécuter dans ce chemin. Risque : les requêtes partageant la boucle du worker attendent les opérations synchrones. La documentation [FastAPI sur la concurrence](https://fastapi.tiangolo.com/async/) distingue les routes synchrones déportées automatiquement et les fonctions utilitaires appelées directement.

F10 : chaque coffret appelle `blocages_coffret`, qui recharge la politique (`service_conformite_bum.py:35,205`), le coffret et, selon le cas, sa qualification courante (`:228,258`). Le nombre de lectures augmente avec la page ; la quantité exacte dépend des sorties anticipées et du cache d'identité SQLAlchemy. Aucun plan SQL ni chronométrage n'a été exécuté.

Validation : sur environnement jetable, instrumentation du nombre de requêtes pour 1/25/100 coffrets ; mesurer p50/p95/p99 et lag de boucle sous concurrence contrôlée avec Stripe simulé. Comparer avant/après à configuration identique. Compensations : pagination bornée déjà présente ; dimensionnement surveillé des workers/pools, pas multiplication arbitraire des connexions. Charger politique et qualifications en lot avant d'introduire un cache pouvant périmer la conformité BUM.

### F11 — Persistance du Bearer dans le navigateur

`saveSession` sérialise la session complète dans localStorage. Le client vérifie l'expiration et nettoie au logout ; cela ne protège pas le jeton contre du JavaScript exécuté dans l'origine. La CSP est une défense existante. Aucune chaîne XSS exploitable n'a été démontrée ; la présence de `dangerouslySetInnerHTML` dans le composant chart n'établit pas à elle seule une entrée attaquable.

Recommandation conditionnée à l'architecture des domaines : cookie HttpOnly sécurisé avec protections CSRF et origine adaptées, ou access token court en mémoire avec renouvellement protégé. `sessionStorage` ne protège pas contre XSS. [OWASP HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html) déconseille les identifiants de session dans localStorage.

Validation : connexion, rechargement, multi-onglets, expiration, révocation, logout, CORS et CSRF ; ne jamais transmettre le jeton réel à un collecteur de test. Compensation : CSP restrictive, éviter les scripts tiers non maîtrisés, durées/revocation serveur vérifiées.

### F12 — Job absent un jour, échéance manquée

`notifier_expirations` ne traite que les jours dont `remaining` appartient exactement aux seuils configurés (424–426). L'état `EXPIRE` est affecté dans cette boucle seulement à J0 (458–459), et après recherche d'une souscription. Une exécution manquée n'est pas rattrapée le lendemain. Cela ne démontre pas un maintien illicite des accès : les contrôles de droits et de dates doivent être testés indépendamment du statut administratif.

Test à horloge simulée : sauter un seuil puis J0, relancer à J+1 ; vérifier notification de rattrapage selon règle métier et statut final. Deux exécutions concurrentes ne doivent pas doubler les notifications. Compensation : alerter sur absence d'exécution et échéances dépassées ; séparer l'expiration des droits de la disponibilité de l'envoi d'email.

## C. Plan d'action

### Sous 48 heures

- Faire valider F01–F04 par tests isolés à injection de panne et concurrence. Suspendre l'élargissement du déploiement Epic 47 si les invariants financiers échouent en recette.
- Désigner le responsable du rapprochement et définir l'alerte commandes/droits incohérents, sans modification automatique de données réelles.
- Restreindre la consultation/export des emails sensibles et inventorier leur conservation.
- Corriger après validation les gains rapides F06 et F07, puis F04 et F05 ; ajouter les scénarios de non-régression **avant** le correctif.
- Obtenir les résultats CI des commits poussés et établir un environnement PostgreSQL jetable explicitement non productif.

### Sous 30 jours

- Atomicité et reprise des souscriptions (F01), verrou commun de quota (F02), transitions terminales (F08).
- Invitation à usage unique (F03), pagination métier complète (F05), rattrapage des échéances (F12).
- Tests exécutant réellement les fonctions API et composants ; les regex de `tests/sellable-boxes-contract.test.mjs:7` et `tests/animation-cancellation-contract.test.mjs:12` ne détectent pas les défauts décrits. Conserver ces contrats en complément, pas en remplacement.
- Batterie API de cloisonnement : partenaire A/B, commune active différente, session révoquée, permission insuffisante, animation étrangère ; tests des routes internes avec middleware complet, pas uniquement du routeur.
- Contrôler versions installées, scans de dépendances et images, configuration effective CORS/cookies/TLS sans valeurs secrètes ; vérifier branch protection et blocage de merge sur CI.

### Sous 90 jours

- Mesurer puis traiter F09/F10 ; établir des budgets réseau/SQL et un protocole de performance reproductible.
- Traiter F11 avec la topologie réelle des domaines ; valider migration et logout des anciennes sessions.
- Extraire progressivement du service de souscription la machine à états et les politiques d'invitation/reprise ; réduire le couplage au rythme des tests, sans refonte totale préalable.
- Exercice de restauration sur cible isolée, validation des migrations et du rollback applicatif ; fixer RPO/RTO avec l'exploitation.
- Vérifier rétention emails/webhooks/audit, accès aux exports et procédures de droits des personnes. Pas de conclusion juridique RGPD sans registre des traitements et politiques effectives.

### En continu

- Surveiller erreurs webhook, rapprochements en attente, âge de l'outbox, absence de jobs, incohérences quota et échecs d'annulation ; logs corrélés sans jetons ni corps d'emails sensibles.
- Rejouer les tests panne/concurrence/pagination à chaque évolution des souscriptions et animations.
- Scans de dépendances et secrets en CI, mises à jour contrôlées, images/actions épinglées selon la politique de maintenance.
- Exercer périodiquement la restauration et réviser les objectifs de service à partir des mesures.

## D. Exemples proposés lors de l'audit initial — schémas illustratifs

Les extraits ci-dessous sont les propositions initiales, pas une copie des
implémentations finales. Consulter les commits de la section F pour le code appliqué.

### D1. Isoler l'activation du paiement reçu

Schéma à adapter, pas un patch prêt à fusionner : verrouiller la commande dans la transaction, garder la preuve du paiement, isoler **tous** les effets d'activation dans un savepoint, puis traiter explicitement la reprise.

```python
with session.begin():
    commande = session.execute(
        select(CommandeSouscriptionPlateformeOrm)
        .where(CommandeSouscriptionPlateformeOrm.id == commande_id)
        .with_for_update()
    ).scalar_one()
    # Valider evenement, session, montant/devise et transition autorisee.
    # Enregistrer la reception du paiement avant le savepoint.
    try:
        with session.begin_nested():
            result = self._activer_commande(
                session, commande, gratuite=False, acteur="stripe:webhook"
            )
            session.flush()
    except Exception:
        # Aucun droit partiel ne doit survivre au rollback du savepoint.
        commande.statut = "A_RECONCILIER"
        trace.statut = "ECHEC"
        # Enregistrer une cause assainie et declencher le circuit de reprise.
    else:
        trace.statut = "TRAITE"
```

Attention : `begin_nested()` flush les modifications déjà en attente avant le savepoint. Créer les droits seulement **dans** celui-ci. Les pannes de connexion/commit demandent un traitement de niveau supérieur ; ce schéma ne les résout pas toutes. Les appels externes ne sont pas rollbackables. Séparer réception, traitement et reprise si adoption d'une inbox durable ; n'acquitter HTTP 2xx qu'après stockage durable. Les doublons sont attendus dans le modèle [Stripe Webhooks](https://docs.stripe.com/webhooks).

Tests : panne avant/après chaque étape, doublon même événement, événements distincts même commande, montant incorrect, session obsolète, reprise sans double droit ni double email. Effets secondaires : davantage de verrouillage ; définir ordre des verrous, délais et retries bornés.

### D2. Verrouiller la ressource portant le quota

```python
abonnement = session.execute(
    select(AbonnementPlateformeOrm)
    .where(AbonnementPlateformeOrm.id == abonnement_id)
    .with_for_update()
).scalar_one_or_none()
# Sous ce verrou : verifier l'etat, recompter les consommations actives,
# verifier le replay, puis inserer avant commit de la publication.
```

Tous les consommateurs doivent suivre ce protocole ; coordonner également les restitutions de crédits et modifications de quota. Conserver l'unicité comme défense supplémentaire. Test à deux transactions : exactement une publication réussit pour quota 1 ; replay ne consomme rien ; annulation restitue une seule fois. Effets secondaires : contention entre publications du même abonnement, nécessitant des délais d'attente maîtrisés.

### D3. Préserver les cycles d'invitation

```python
for demande in repository.lister_par_animation(animation.id):
    if not demande.est_courante:
        continue
    # Appliquer ici la matrice validee : en attente / acceptee / refusee.
    # Ne jamais remettre un cycle historique dans l'etat courant.
    demande.annuler(now, motif, conserver_courante=True)
    repository.mettre_a_jour(demande)
```

Décider explicitement du sort d'un refus courant lors de l'annulation totale. Test : plusieurs cycles, refus historique inchangé, unicité courante, rollback si lots payés, annulation répétée, crédit rendu une seule fois. Effet visible : l'historique ne change plus rétroactivement ; adapter le libellé UI à cette distinction.

### D4. Séparer existence, renvoi et identité du destinataire

```python
existing_id = session.execute(
    select(EmailSortantOrm.id).where(*conditions).limit(1)
).scalar_one_or_none()
if existing_id and not force:
    return
```

Cette modification minimale empêche l'erreur multiligne, mais ne résout pas seule la concurrence ni le lien Checkout périmé. Définir une clé d'envoi initial `(commande, checkout_session, type)` et une identité propre à chaque demande de renvoi. Pour l'invitation, clé `(gestionnaire, cycle_invitation)`, pas partenaire seul. Émettre un lien d'activation à usage unique plutôt qu'un mot de passe ; conserver seulement le hash du jeton côté authentification.

Tests : trois renvois, nouvelle session après expiration, activation du deuxième gestionnaire, replay, lien expiré, jeton déjà consommé. Effet secondaire : migration/déduplication des métadonnées existantes à préparer sans suppression aveugle d'emails.

### D5. Rendre la pagination conforme à l'éligibilité réelle

Calculer la vendabilité complète avant `LIMIT/OFFSET` ou construire une projection filtrable transactionnellement fiable. Retourner `items` et métadonnées de pagination ; adapter le frontend avec navigation/recherche ou collecte bornée selon le volume. Ne pas arrêter une collecte sur une page vide tant que le backend filtre encore après pagination.

Tests : 0/1/25/26/101 candidats, pages entièrement bloquées, mélange BUM/couverture/statuts, tri stable, politique BUM modifiée, animation d'un autre partenaire refusée. Effet secondaire : évolution du contrat API et du client à coordonner ; garder le blocage à la publication/achat même si le sélecteur est correct.

## E. Niveau de confiance et vérifications restantes

### Ce que l'audit ne conclut pas

- Pas d'IDOR, injection SQL/commande, SSRF, XSS ou accès administrateur anonyme démontré sur les chemins examinés. Cela ne signifie pas absence globale de vulnérabilités.
- Aucun statut de conformité RGPD, aucun contrôle du chiffrement au repos, des certificats réels, des règles réseau ou de l'isolation des environnements.
- Aucun RPO/RTO validé. La documentation comporte des procédures de schéma/restauration (`B:docs/ops/technique/deployer-et-verifier-schema.md`) et de campagne de performance ; leur existence ne prouve pas qu'une restauration a réussi en exploitation.
- Aucun index à ajouter « par principe » : les contraintes pertinentes ont été examinées, mais aucun `EXPLAIN ANALYZE`, volume ou statistique PostgreSQL n'a été collecté.
- Aucune fuite mémoire ou saturation de pool établie. Le pool est configuré dans `B:app/infrastructure/persistence/db.py` ; sa capacité effective doit être rapprochée du nombre de workers et de la limite PostgreSQL.
- Le scan npm actuel ne remonte aucun avis pour les 414 dépendances rapportées ; cela n'exclut pas les vulnérabilités inconnues. Aucun scan Python ou des images système n'a été exécuté localement. Les plages de versions Python et les images flottantes rendent nécessaire cette vérification en CI et sur l'image effectivement déployée.

### Questions pour lever les incertitudes

1. Quelle version est réellement déployée, sur quelle topologie (workers, reverse proxy, PostgreSQL, stockage et scheduler) ?
2. Peut-on disposer d'une préproduction jetable avec données synthétiques, Stripe simulé et les résultats CI des deux commits ?
3. Quels volumes d'animations/coffrets/souscriptions et quels objectifs de latence/disponibilité faut-il respecter ?
4. Une commande annulée doit-elle pouvoir être rouverte, et un refus doit-il rester visible comme refus après annulation complète de l'animation ?
5. Qui peut consulter les emails persistés, combien de temps sont-ils conservés et comment sont protégés les exports/sauvegardes ?
6. Quelle est la dernière restauration réussie et mesurée ? Quelle procédure permet de reprendre un paiement en rapprochement sans double activation ?

Le niveau de confiance est élevé sur les chemins de code explicitement cités, moyen sur les conséquences concurrentes et opérationnelles, insuffisant pour une assurance de sécurité/performance de production. Les recommandations de sécurité ont été structurées avec le skill `security-best-practices` pour React/TypeScript et FastAPI ; les contrôles métier et preuves du dépôt priment sur les recommandations génériques.

## F. État des points traités et à traiter

### Synthèse au 5 septembre 2026

- **12/12 constats corrigés dans le code**, avec tests et spécifications actualisés
  selon les changements de règles. Les correctifs sont poussés sur `origin/main`
  des dépôts concernés ; cela ne prouve pas leur déploiement.
- **403 tests backend ciblés réussis** lors de la validation croisée finale,
  exécutée avec `scripts/validation/test_isolated.py`, sans accès aux services externes.
  Les tests transactionnels utilisent SQLite éphémère ; ils ne valident pas les
  verrous ni les interleavings réels PostgreSQL. Deux avertissements de dépréciation
  `datetime.utcfromtimestamp` subsistent, sans échec de test.
- **25 tests frontend réussis**, ainsi que le typage, le lint et le build via
  `npm.cmd run check`. Ils ne constituent pas une recette navigateur complète.
- Ces résultats proviennent de la campagne de correction précédente, pas d'une
  nouvelle exécution lors de cette mise à jour documentaire. La suite backend
  complète et les résultats CI distants ne sont pas attestés ici.

### Points traités : correctifs et traçabilité

Dans le tableau, **corrigé** signifie implémenté, testé localement dans la portée
indiquée et poussé ; la clôture opérationnelle reste conditionnée aux validations
du tableau suivant. `B` = backend ; `F` = portail Animation.

| ID | État | Correction réalisée et couverture locale | Commit(s) |
| --- | --- | --- | --- |
| F01 | Corrigé | Activation isolée dans un savepoint ; aucun droit ou email partiel après échec injecté. Reprise du même événement limitée à l'erreur technique identifiée et au contenu identique ; incohérences financières non rejouées automatiquement. | B `cd4e753` |
| F02 | Corrigé, concurrence PostgreSQL à valider | Verrou d'abonnement avant comptage/insertion ; restitution coordonnée et flush explicite. Tests de quota, replay, restitution et émission du SQL `FOR UPDATE`. | B `b34e3f6` |
| F03 | Corrigé, migration à appliquer | Mot de passe initial remplacé par un lien d'activation à usage unique, valable 24 h ; hash du jeton côté authentification, choix du mot de passe et renouvellement administratif. Tests d'activation, expiration, réutilisation, suspension, mot de passe et API. | B `1c9032a` ; F `e0b8f24` |
| F04 | Corrigé | Annulation limitée aux invitations courantes non refusées ; refus et cycles historiques conservés. Matrice de statuts testée et confirmation UI adaptée. | B `7bf659a` ; F `c1daf6a` |
| F05 | Corrigé | Filtrage de vendabilité avant pagination SQL et collecte des pages dans le sélecteur. Tests de pages bloquées, coffrets non vendables et parcours frontend jusqu'à 205 résultats. | B `b235281` ; F `982b12f` |
| F06 | Corrigé | Recherche d'existence bornée et déduplication liée à la session Checkout. Tests de renvois multiples, refus de lien expiré et nouvel email pour un nouveau Checkout. | B `e6f69ee` |
| F07 | Corrigé | Invitation identifiée par gestionnaire ; compatibilité avec les anciens emails par destinataire. Le dossier d'invitation empêche un renvoi après purge des emails ; tests de deux gestionnaires du même partenaire et de replay. | B `9d93ffc` |
| F08 | Corrigé | Transitions administratives autorisées explicitement et commande verrouillée ; annulation terminale, activation gratuite idempotente, expiration tardive sans déclassement d'une commande payée. Tests d'états interdits sans effets externes. | B `58e7195` |
| F09 | Corrigé, charge à mesurer | Validation Stripe et traitement SQL déportés dans le pool borné Starlette/AnyIO, sans acquittement anticipé. Tests d'exécution hors boucle événementielle et de signature invalide. | B `a6309f3` |
| F10 | Corrigé, latence à mesurer | Politique lue une fois et chargements BUM groupés, sans cache global. Nombre de requêtes identique pour 1, 25 et 100 coffrets ; motifs comparés au contrôle unitaire. | B `f9b1371` |
| F11 | Corrigé | Bearer uniquement en mémoire ; suppression de l'ancien stockage sans restauration. Tests de reconnexion après rechargement, expiration, déconnexion et stockage indisponible. | F `b2ff9e0` |
| F12 | Corrigé, concurrence du job à valider | Rattrapage du dernier seuil franchi pendant 30 jours, déduplication et expiration indépendante des notifications. Tests d'horloge, jours manqués, répétition, limite de rattrapage et exclusion des suspensions. | B `bee7d1a` |

### Points à traiter ou à valider avant clôture opérationnelle

Ces actions sont des suites de recette, déploiement et exploitation ; elles ne
signifient pas que les douze corrections de code restent à implémenter.

| Priorité | Points concernés | Action restante | Critère de clôture |
| --- | --- | --- | --- |
| P1 | F03 | Valider puis appliquer `B:sql/v216_invitations_gestionnaires_animation.sql` selon la procédure de déploiement, avant l'utilisation du nouveau parcours. La migration est préparée, non exécutée pendant cette intervention. | Migration réussie sur PostgreSQL jetable, stratégie de retour validée et schéma cible vérifié au déploiement. |
| P1 | F01, F02, F07, F08, F12 | Exécuter les scénarios réellement concurrents sur PostgreSQL isolé : événements d'une même commande, quota 1 avec deux publications, renouvellement/activation d'invitation, annulation/paiement et deux jobs d'échéance. | Absence de double droit, dépassement de quota, double consommation de lien ou notification ; reprise cohérente après attente/échec de verrou. |
| P1 | F03, F04, F05, F06, F11 | Effectuer une recette de bout en bout en préproduction, avec comptes synthétiques et Stripe Test/simulé : invitation reçue, activation, renvoi de paiement, historique, catalogue et sessions. | Parcours validés sur navigateurs cibles, y compris rechargement, nouvel onglet, expiration, révocation et logout. |
| P1 | Tous | Vérifier CI et versions effectivement déployées des deux dépôts ; coordonner schéma, backend et frontend. | CI requise verte, versions identifiées et contrôles post-déploiement documentés. |
| P1 | F01, F03 | Examiner les commandes historiques en rapprochement et la conservation des anciens emails contenant un mot de passe. Les corrections ne réparent ni ne purgent rétroactivement ces données. | Procédure opérateur approuvée, accès/rétention évalués, éventuelles réinitialisations ou réparations autorisées et tracées, sans suppression aveugle. |
| P2 | F09, F10 | Mesurer latences p50/p95/p99, retard de boucle, contention et utilisation des pools sous charge contrôlée. | Comparaison avant/après reproductible et budgets de performance validés ; le seul nombre de requêtes ne suffit pas. |
| P2 | F01, F02, F12 | Vérifier la supervision des rapprochements, quotas, outbox et exécutions du planificateur. | Alertes testées, responsable désigné et procédures de reprise exercées. |
| P2 | Sécurité/exploitation transverses | Vérifier scans Python/images/secrets, configuration réelle CORS/TLS/CSP, accès aux exports, sauvegardes et restauration. | Preuves CI et d'exploitation disponibles ; RPO/RTO et politique de conservation validés. Aucune certification de sécurité ou de conformité n'est déduite des tests locaux. |

### Règles et effets visibles à retenir

- Une commande annulée ne se réouvre pas par Checkout ou activation gratuite.
  Les refus des commerçants et les anciens cycles restent visibles sans être
  transformés en invitations courantes annulées.
- Le gestionnaire choisit son mot de passe depuis un lien temporaire ; l'email
  ne contient plus de mot de passe initial. Le lien reste sensible jusqu'à sa
  consommation ou son expiration.
- Le rechargement de l'application ou l'ouverture d'un nouvel onglet nécessite
  une reconnexion. La suppression de localStorage ne révoque pas à elle seule les
  anciennes sessions serveur, qui restent soumises à leur expiration/révocation.
- La date de fin d'abonnement est inclusive : notification possible à J0,
  expiration des droits dès J+1. Le rattrapage n'envoie pas tous les anciens seuils.

**Bilan : corrections applicatives F01–F12 terminées et poussées ; recette
PostgreSQL, migration, validation du déploiement et preuves d'exploitation restent
à compléter avant de déclarer l'audit clôturé en production.**
