# Audit de performance — recherche publique Marketplace

Date : 12 septembre 2026. Endpoint : `GET /public/commercialisation/recherche?q=test&limit_total=8&limit_par_scope=4`.

## Conclusion

La priorité est de supprimer les lectures et diagnostics répétés. Sur le petit
jeu Latresne, une recherche sans résultat exécute **348 SELECT**, alors que la
réponse est vide. Les limites de résultats ne limitent pas le travail effectué.
Le coût augmente avec le catalogue entier, indépendamment du nombre de résultats.

Un changement de moteur de recherche ou une augmentation de la capacité serveur
ne sont pas nécessaires pour traiter ce premier problème. Le dépôt dispose déjà
de lectures groupées de vendabilité réutilisables.

## Périmètre et méthode

- Lecture du backend, du contrat Epic 33, du client Marketplace et de la campagne k6.
- Source backend locale : commit `5ca56fd` ; aucun changement applicatif réalisé pour cet audit.
- Deux appels HTTP publics à l'environnement de test : **503 en 194 ms**, puis
  **503 en 174 ms** en fin d'audit. Ce résultat
  mesure une indisponibilité, pas la performance de la recherche. Le commit et
  les paramètres du serveur déployé n'ont donc pas pu être vérifiés.
- Exécution instrumentée du cas d'usage réel, via son Unit of Work SQLAlchemy,
  sur PostgreSQL local puis sur la base de test depuis ce poste.
- Connexions imposées en lecture seule, six recherches séquentielles par cible,
  limite de dix secondes par instruction SQL, puis 16 plans
  `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` par cible. Aucun test de charge,
  aucune écriture métier, aucun appel Stripe/Brevo/Scaleway.
- Scénario explicite avec contrôles BUM et Stripe activés dans le processus
  d'audit. Ce n'est pas une attestation de la configuration du serveur API.
- PostgreSQL 18.3 ; 4 villes, 16 commerçants dont 14 actifs, 18 coffrets dont
  17 actifs, 40 prestations rattachées actives et 10 animations.
- La copie locale est celle de la construction du nouveau jeu, avant le
  rattachement Stripe ; la base distante contient le jeu finalisé. La comparaison
  principale porte sur `test`, sans correspondance, dont les parcours SQL sont
  identiques. Ne pas utiliser cette comparaison pour attester l'équivalence de
  visibilité de toutes les recherches entre les deux bases.

Les temps ci-dessous sont ceux du cas d'usage depuis le poste, hors HTTP,
middleware et sérialisation FastAPI. Les événements de profilage ajoutent un peu
de coût. L'échantillon est trop petit pour annoncer un p95 ou une capacité de
production. Le premier appel significatif inclut une initialisation ORM.

## Mesures

| Recherche | Limites total/catégorie | SELECT | Résultats | Local | Base de test depuis le poste |
| --- | --- | ---: | ---: | ---: | ---: |
| `t` | 8 / 4 | 0 | 0 | 0,11 ms | 0,19 ms |
| `test`, premier appel significatif | 8 / 4 | 348 | 0 | 811 ms | 7 928 ms |
| `test`, appel suivant | 8 / 4 | 348 | 0 | 473 ms | 7 413 ms |
| `latresne` | 8 / 4 | 348 | 1 ville | 440 ms | 8 019 ms |
| `passeport` | 8 / 4 | 356 | 1 animation | 598 ms | 8 433 ms |
| `test` | 1 / 1 | 348 | 0 | 505 ms | 7 513 ms |

Décomposition du deuxième appel `test` :

| Catégorie | SELECT | Lignes retournées cumulées | Temps local | Temps via base distante |
| --- | ---: | ---: | ---: | ---: |
| Villes | 1 | 4 | 2,2 ms | 60,8 ms |
| Commerçants | 1 | 14 | 2,4 ms | 23,5 ms |
| Prestations | 241 | 382 | 312,5 ms | 5 122,1 ms |
| Coffrets | 103 | 161 | 138,8 ms | 2 117,3 ms |
| Animations | 2 | 1 | 15,7 ms | 50,6 ms |

Le compteur de lignes est cumulatif : il comprend les relectures et le résultat
du COUNT, pas 562 objets distincts. Sur la base distante, 7 062 ms sur 7 413 ms
sont mesurées dans le pilote SQL, soit 95,3 %. Ce temps inclut le réseau ; il
ne représente pas du temps CPU PostgreSQL.

Les 16 instructions examinées sur la base distante s'exécutent côté PostgreSQL
en **0,018 à 0,282 ms** chacune, à cache chaud, sans lecture de blocs hors cache
partagé dans ces plans. Les scans séquentiels sur quelques lignes sont normaux.
Ces mesures ne préjugent pas des plans ni du coût à grand volume. La méthode
d'interprétation est décrite dans la [documentation EXPLAIN PostgreSQL](https://www.postgresql.org/docs/18/using-explain.html).

## Constats et optimisations prioritaires

### P0 — Filtrer le texte avant de vérifier la vendabilité

Dans `rechercher_marketplace_multi_scope.py:187-188` et `:221`, le contrôle
`coffret_est_eligible_catalogue` intervient avant `_matches`. Ainsi, `test`
déclenche la vérification des coffrets de chacune des 40 prestations, puis des
17 coffrets actifs, même si aucun libellé ne contient ce terme.

Le chemin passe par `gouvernance_catalogue.py:36-42`, qui appelle
`VendabiliteRepository.evaluer([coffret.id])`. Ce repository relit coffret,
prestations, commerçants, commune, politique BUM et qualification : **six SELECT
par appel** dans le scénario mesuré. L'identity map SQLAlchemy ne supprime pas
ces `select(...)` explicites.

La formule observée est `6 requêtes de base + 6 × (40 + 17) = 348`.
Sans BUM, le nombre par diagnostic diffère ; le défaut de répétition reste présent.

Action : éliminer immédiatement les libellés sans correspondance, puis évaluer
uniquement les candidats. Pour `test`, cela rend les **342 lectures de
vendabilité inutiles**, soit 98,3 % des SELECT de cet appel. Il s'agit d'une
réduction déduite du parcours, pas d'un gain de latence déjà mesuré après correction.
Cette première étape conserve encore les quatre chargements globaux : elle doit
être suivie de la recherche SQL décrite ci-dessous.

### P0 — Grouper les diagnostics et réutiliser leur résultat dans la requête

Un même coffret est contrôlé pour plusieurs prestations, puis dans la catégorie
coffrets. Regrouper les identifiants distincts des candidats et utiliser
`diagnostics_catalogue` (`gouvernance_catalogue.py:94`) ou
`VendabiliteRepository.evaluer(ids)` (`vendabilite_repository.py:17`).

Conserver une carte de diagnostics limitée à la requête HTTP, partagée entre
prestations et coffrets. Lire la politique active une fois par groupe. Un groupe
non vide peut être évalué par six lectures, au lieu de six par objet. Pour les
gros ensembles, traiter des lots bornés et vérifier le coût du parcours des
commerçants dans l'évaluateur ; grouper le SQL ne suffit pas à garantir un coût
CPU linéaire pour des milliers de candidats.

La visibilité doit rester contrôlée avec les règles existantes. Ne pas prendre
les quatre premiers candidats puis supprimer les inéligibles sans compléter la
liste : un résultat éligible pourrait se trouver juste après.

### P1 — Rechercher et limiter dans PostgreSQL, avec une projection courte

Les méthodes villes, commerçants, prestations et coffrets utilisent `.all()`
sans filtre textuel ni `LIMIT` SQL (`:114`, `:129-138`, `:165-177`, `:208-217`).
Elles chargent des objets ORM complets et leurs relations. Le tri SQL par nom
est ensuite suivi d'un second tri Python par score et nom normalisé.

Créer des méthodes de repository dédiées aux suggestions : identifiant,
libellé, champs de sous-titre, cible et faits strictement nécessaires à la
visibilité. Appliquer le filtre textuel, le classement et la limite au plus près
des données. Préserver le classement exact > préfixe > inclusion, puis nom
normalisé et identifiant. Normaliser une seule fois les libellés utiles.

Pour l'inclusion au milieu d'un nom, prévoir un champ de recherche normalisé et
un index trigramme adapté. `pg_trgm` n'est présent ni sur les deux bases
inspectées ni dans les migrations recherchées. L'index existant sur
`LOWER(animation_animations.nom)` ne suffit pas à accélérer `%terme%`.
Les index GIN/GiST trigrammes peuvent servir à LIKE/ILIKE ; un motif sans
trigramme exploitable peut parcourir l'index entier, notamment `%ab%`. Prévoir
une stratégie explicite pour les deux caractères et la valider à grand volume.
[Référence PostgreSQL](https://www.postgresql.org/docs/18/pgtrgm.html).

La normalisation doit reproduire le contrat actuel : NFKD, suppression des
accents, casefold et espaces. Ne pas supposer que `lower(unaccent(...))` est
strictement équivalent sans tests. Échapper `%` et `_` lorsque la recherche doit
les traiter comme des caractères littéraux. Mesurer les index avant de les
multiplier ; certains index de clés étrangères/statut semblent redondants dans
le catalogue inspecté, mais leur suppression demande un audit séparé.

### P1 — Ne pas exécuter les catégories qui ne pourront plus être affichées

`execute()` appelle systématiquement les cinq catégories puis applique
`results[:total_limit]` (`:96-107`). Avec quatre villes et quatre commerçants
retenus, les trois catégories suivantes ne peuvent plus apparaître dans une
réponse limitée à huit éléments.

Calculer le nombre de places restantes et arrêter dès qu'il est nul. Transmettre
`min(limit_par_scope, places_restantes)` aux catégories suivantes. C'est compatible
avec la priorité actuelle VILLE > COMMERCANT > PRESTATION > COFFRET > ANIMATION.
Ne pas remplacer cette priorité par un classement global au score.

### P1 — Alléger la recherche d'animations

La recherche appelle le catalogue public complet avec `page_size=4`. Celui-ci
calcule un total inutilisé, charge la configuration JSON et produit une fiche
enrichie alors que la suggestion utilise essentiellement nom, id et commune.

`catalogue_animations_publiques.py:239-263` effectue le COUNT et la page ;
`:416-500` charge commerçants, coffrets, présence de flyers et contrôles BUM des
lots, puis construit règles et autres données non affichées dans la suggestion.
Le cas `passeport` passe ainsi à 356 SELECT. Aucun téléchargement de visuel ni
appel fournisseur n'a été identifié dans ce chemin de recherche.

Créer une projection de suggestion dédiée, sans COUNT ni enrichissements
inutiles. Conserver les règles de publication, dates, abonnement et BUM des lots,
en utilisant notamment les contrôles BUM groupés existants.

Deux points fonctionnels doivent être corrigés ou arbitrés avec cette évolution :
la page est limitée par statut/date avant le classement au score ; le filtre SQL
ILIKE sur le nom non désaccentué peut exclure une animation correspondant à la
requête normalisée. Le filtrage BUM après pagination peut aussi sous-remplir la
réponse. Une optimisation ne doit pas reproduire aveuglément ces limites.

### P2 — Annuler les appels obsolètes et calibrer l'expérience de saisie

Le client possède déjà un délai de saisie de 400 ms, un minimum de deux
caractères et un cache React Query de 30 secondes
(`MarketplaceMultiScopeSearch.jsx:88-104`). Le délai de 400 ms s'ajoute au temps
API avant d'afficher les suggestions. La configuration générale prévoit un
retry et désactive le refetch au focus.

Le `queryFn` ne consomme pas le signal d'annulation et `searchMarketplace`
ne le transmet pas, alors que `requestWithDeadline` sait le gérer. Relier
`queryFn({signal})` à `fetch` via les options existantes évitera de continuer
inutilement les appels obsolètes côté navigateur. Cela ne garantit pas l'arrêt
d'un traitement Python/SQL synchrone déjà lancé sur le serveur.
[Référence TanStack Query](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation).

Après réduction du coût backend, mesurer un délai de saisie de 200–250 ms.
Ne pas le réduire d'emblée : cela pourrait augmenter le nombre d'appels coûteux.
Ajouter une longueur maximale explicite de `q` et vérifier le traitement des
recherches répétées en échec, pour lesquelles le retry peut doubler le travail.

### P2 — Cache partagé et capacité, après réduction du coût unitaire

Le cas d'usage ne possède pas de cache de résultats partagé. Un cache des
candidats textuels, suivi d'un contrôle actuel de leur visibilité, est une piste.
Un cache de réponses complètes doit être invalidé sur publication/suspension,
modification des noms, prestations, BUM, Stripe, abonnement et changement de
fenêtre temporelle des animations. Un TTL seul peut exposer temporairement un
résultat devenu indisponible. Le choix du délai doit être produit, pas implicite.

La route est synchrone et garde son UoW pendant les cinq recherches. Les valeurs
par défaut du pool sont 5 connexions et 5 débordements par processus, avec
attente maximale de 30 secondes (`db.py:32-40`). Les réglages déployés ne sont pas
connus. Supprimer les centaines d'allers-retours avant d'augmenter ce pool ou
de paralléliser les catégories. Une conversion en async ne supprime pas le N+1.

## Contrats à protéger

Les villes recherchées ne sont pas filtrées sur `publiee_marketplace`, et les
commerçants sont filtrés sur ACTIF sans vérification du profil publié dans ce
cas d'usage. C'est un écart potentiel au contrat de visibilité de l'Epic 33,
à traiter explicitement avant de définir les prédicats d'une recherche SQL.

Tester : accents/casse/espaces, égalité/préfixe/inclusion, ordre des catégories,
limites globales, coffrets brouillons/BUM suspendue, comptes Stripe inéligibles,
abonnements expirés, lots non publiables, résultats remplis malgré des premiers
candidats exclus, absence de doublons liée aux jointures.

## Séquence de réalisation et validation proposée

1. Filtre textuel avant vendabilité, diagnostics groupés et réutilisation par
   requête ; test de non-régression du nombre de SQL. Viser **6 SELECT pour la
   recherche sans correspondance** dans le parcours actuel, hors middleware.
2. Projection SQL dédiée, normalisation/index, limite et arrêt des catégories ;
   projection d'animation légère. Viser un budget initial de **20 SELECT ou moins**
   pour une recherche courante, à préciser avec les règles de remplissage et les
   volumes, sans dégrader la complétude.
3. Mesurer l'API redémarrée avec `8/4`, sur des jeux de tailles croissantes, requêtes
   vides, rares, fréquentes et accentuées. La campagne Marketplace actuelle utilise
   `20/5` et un seuil p95 de 800 ms pour l'ensemble du parcours ; ajouter un seuil
   spécifique `marketplace.search`.
4. Objectif initial à valider : **p95 HTTP ≤ 200 ms et p99 ≤ 500 ms à chaud sous
   charge nominale convenue**, puis mesure au navigateur incluant la saisie.
   Ce sont des cibles proposées, pas des performances déjà démontrées.
5. Mesurer SQL par appel, lignes lues, temps CPU/ORM, attente du pool, durée DB,
   TTFB, erreurs et taux de cache. Valider chaque étape sur la même implantation
   API/DB et le même jeu ; ne pas comparer directement le poste distant à Render.

## Preuves conservées

Fichiers locaux ignorés par Git sous `output/performance/recherche-audit-20260912/` :
`profile_search.py`, `local.json`, `remote.json`, `http.json` et journaux. Ils contiennent les
compteurs, plans, index et paramètres de mesure, sans export des lignes métier
ni clés API. Ce rapport est la synthèse partageable. Aucun changement de code
applicatif, d'index ou de configuration serveur n'avait été appliqué pendant l'audit.

## Optimisation appliquée après l'audit

Le backend filtre les libellés avant tout diagnostic de vendabilité, évalue les
coffrets par lots de 32 candidats et réutilise les diagnostics entre prestations
et coffrets pendant un seul appel. Les lots suivants sont examinés si des
candidats sont exclus : la limite ne tronque pas prématurément les résultats.
Les règles BUM et Stripe restent celles du domaine. Aucun cache de décision
de publication n'est conservé entre les requêtes.

Les lectures du catalogue sélectionnent uniquement les colonnes nécessaires
aux suggestions. Les catégories suivantes ne sont plus interrogées lorsque
la limite globale est atteinte, sans modifier leur priorité.

Les animations utilisent la requête de visibilité publique existante
(abonnement, commune, dates et statut), avec une projection dédiée et des
contrôles BUM des lots groupés. Cette recherche n'effectue plus de COUNT,
de recherche documentaire ni de construction de règles et de fiches détaillées.
Elle applique la même normalisation Unicode que les autres catégories, traite
`%` et `_` littéralement, et classe les candidats avant la limite. Cela corrige
également la perte de suggestions pertinentes ou accentuées dans cette catégorie.

La Marketplace transmet le signal d'annulation TanStack Query au transport
HTTP. Le debounce de 400 ms et le cache client de 30 secondes sont conservés.
Localeo Commerçant et Localeo Animation ne nécessitent pas de modification du
contrat de cette route publique.

### Mesures avant / après

Même jeu de données et même profilage du cas d'usage, BUM et Stripe activés,
limites 8/4. Mesures ponctuelles à chaud, pas des percentiles sous charge :

| Recherche | SELECT avant → après | Local avant → après | Poste vers base de test avant → après |
|---|---:|---:|---:|
| `test` | 348 → 5 | 473 → 16 ms | 7 413 → 176 ms |
| `latresne` | 348 → 5 | 440 → 15 ms | 8 019 → 265 ms |
| `passeport` | 356 → 8 | 598 → 95 ms | 8 433 → 317 ms |

Un second contrôle local compare les réponses complètes de l'ancien et du
nouveau code pour `atelier`, `de`, `gourmand` et `escapade` : réponses identiques.
Stripe est désactivé uniquement dans ce processus de comparaison pour exercer
les résultats positifs du jeu local antérieur au rattachement Stripe.
Pour `de`, les huit résultats sont conservés avec **9 SELECT au lieu de 371**
(48 ms au lieu de 693 ms). Ce changement de flag ne concerne ni le serveur
ni les premières mesures ci-dessus.

Les preuves initiales sont conservées dans `before-local.json` et
`before-remote.json`; les nouveaux compteurs sont dans `local.json`,
`remote.json` et `comparison-local.json` du répertoire privé de profilage.

### Validation et limites

- 51 tests Python ciblés réussis : normalisation, ordre, limites, absence de
  diagnostic inutile, regroupement, remplissage après exclusion, cache limité
  à un appel, suggestions d'animations et règles de vendabilité/BUM.
- 4 tests PostgreSQL en lecture seule réussis sur le catalogue local Latresne :
  5 SELECT sans correspondance, 1 lorsque la ville remplit la liste,
  budget de 20 SELECT pour la recherche courante et contrôle des résultats
  par le diagnostic de domaine avec Stripe activé et désactivé.
- Build de production Marketplace et 12 tests du transport HTTP réussis,
  dont la propagation du signal et des paramètres de recherche.

Les tests SQL sont relançables avec `LOCALEO_SEARCH_TEST_DATABASE_URL` pointant
explicitement vers un petit catalogue PostgreSQL de recette et :
`python -m pytest tests/integration/test_recherche_marketplace_sql.py -q`.
Ils imposent des transactions en lecture seule et un délai SQL maximal de 10 s.

Cette livraison supprime le coût dominant sans migration. La sélection textuelle
reste en Python sur les colonnes légères : son coût demeure linéaire avec la
taille du catalogue. La normalisation indexée en SQL, les index trigrammes et
la campagne à gros volume restent des travaux distincts à réaliser pour le
passage à l'échelle. Aucun gain à gros volume ou p95 HTTP n'est donc revendiqué.
Les règles actuelles de publication des villes et des commerçants signalées
dans l'audit sont conservées.

Le code n'est pas encore déployé. Les mesures ci-dessus exécutent le cas
d'usage depuis le poste; la validation HTTP sous charge doit être effectuée
après déploiement et remise en service de l'API de test.
