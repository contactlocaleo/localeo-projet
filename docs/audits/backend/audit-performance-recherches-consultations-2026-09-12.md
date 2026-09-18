# Audit des services de recherche et de consultation — 12 septembre 2026

## Conclusion

La recherche Achats 360, le catalogue de coffrets, le catalogue public
d'animations, les compteurs d'activité Marketplace et la fiche Commerçant 360
sont les premières optimisations à engager. Les autres listes ne présentent pas
toutes le problème de lectures répétées : Localeo Support, les listes ERP et
les listes d'animations disposent déjà de lectures groupées ou de pagination SQL.

Deux corrections simples sont également identifiées : rechercher une ville
par sa clé primaire au lieu de charger toutes les villes, et supprimer le verrou
de mise à jour pris lors de la simple consultation d'un dossier commerçant ERP.

Cet audit ne modifie aucun code applicatif ni aucune donnée. Les changements
de recherche multiscope du travail précédent sont conservés, ainsi que les
modifications non liées à cet audit présentes dans les dépôts.

## Périmètre et méthode

- Revue des routes de recherche/consultation, cas d'usage, services, repositories
  et appels des interfaces Marketplace, ERP, Support et Animation.
- **28 scénarios profilés**, chacun deux fois sur PostgreSQL local et deux fois
  depuis le poste vers la base de test. Le tableau retient le second passage.
- Catalogue de test : 4 communes, 16 commerçants, 18 coffrets, 40 prestations,
  60 achats, 8 commandes, 58 instances, 10 animations et 100 participants.
- BUM et Stripe activés dans le processus de profilage distant. BUM activée et
  contrôle Stripe désactivé uniquement dans le processus local, dont les données
  précèdent le rattachement Stripe. Les résultats locaux et distants peuvent donc
  différer; leurs durées ne constituent pas un comparatif de déploiements.
- Connexions avec `default_transaction_read_only=on`, délai maximal de 10 s par
  SQL; garde du profileur de 2 000 requêtes et 60 s par appel. Aucun appel aux
  fournisseurs, envoi de message ou modification de configuration serveur.
- Les durées sont celles des services exécutés depuis le poste. **Ce ne sont
  pas des latences HTTP de l'API déployée, ni des p95 sous charge.** Elles incluent
  les allers-retours réseau vers PostgreSQL. Les compteurs portent sur les SELECT,
  hors authentification, middleware, rendu HTTP, commit et écriture d'audit.
  Les événements d'audit ajoutés en mémoire par certaines lectures ERP sont
  abandonnés à la fermeture de l'UoW du profileur, sans commit.
- Revue ciblée : ce n'est pas une certification exhaustive de chaque route.
  Les téléchargements d'images/PDF, exports volumineux, connexions utilisateur,
  mutations et appels aux fournisseurs ne sont pas chronométrés ici.

## Mesures

`Lignes lues` désigne la somme des lignes renvoyées par les SELECT au pilote,
pas les lignes parcourues physiquement par PostgreSQL. Les tailles de réponses
sont conservées dans les preuves privées, sans enregistrer leur contenu.

| Scénario | SELECT test | Local (ms) | Poste → base de test (ms) | Lignes lues test |
|---|---:|---:|---:|---:|
| `cities.search` | 1 | 3 | 82 | 1 |
| `cities.detail` | 1 | 2 | 81 | 4 |
| `cities.nearby` | 2 | 4 | 102 | 5 |
| `merchants.list` | 1 | 3 | 80 | 10 |
| `boxes.list` | 33 | 48 | 852 | 114 |
| `boxes.list.services` | 46 | 61 | 1087 | 144 |
| `boxes.detail` | 9 | 15 | 250 | 12 |
| `merchants.public_page` | 4 | 22 | 147 | 6 |
| `animations.catalogue` | 35 | 76 | 1222 | 41 |
| `animations.detail` | 9 | 18 | 305 | 15 |
| `animations.summary` | 1 | 9 | 106 | 6 |
| `purchases.search` | 306 | 423 | 6854 | 253 |
| `purchases.search.no_match` | 10 | 21 | 347 | 68 |
| `instances.search` | 2 | 13 | 129 | 26 |
| `instances.detail` | 3 | 15 | 136 | 4 |
| `instances.related` | 19 | 53 | 461 | 14 |
| `merchants.360` | 42 | 80 | 940 | 109 |
| `merchants.dashboard` | 3 | 8 | 123 | 15 |
| `erp.merchants.search` | 2 | 5 | 105 | 17 |
| `erp.sellability.list` | 2 | 12 | 178 | 19 |
| `erp.sellability.summary` | 11 | 18 | 326 | 12 |
| `onboard.list` | 1 | 11 | 101 | 16 |
| `onboard.metrics` | 1 | 5 | 88 | 16 |
| `animations.360.search` | 6 | 17 | 187 | 23 |
| `animations.360.timeline` | 8 | 15 | 225 | 31 |
| `activities.feed` | 2 | 59 | 136 | 6 |
| `activities.metrics` | 15 | 91 | 442 | 15 |
| `merchant.animations` | 6 | 96 | 262 | 12 |

## Optimisations prioritaires

### P1 — Recherche Achats 360

Route : `/internal/gestion-achats/vision-360/achats`.
Source : `app/application/gestion_achats/services/vision_360_achats.py:239`.

**306 SELECT pour afficher 25 résultats, environ 6,85 s depuis le poste vers la
base de test.** Environ 6,55 s sont passées dans les appels SQL/pilote.
Les commandes et achats sont chargés, puis les achats enfants, paiements,
instances, remboursements, documents et communications sont relus pour calculer
les alertes de toutes les racines candidates. La pagination intervient à la fin.
Même une recherche sans résultat lit 68 lignes et exécute 10 SELECT.

Un problème de complétude accompagne ce coût : seules les 500 dernières
commandes et les 500 derniers achats autonomes sont examinés **avant** le
filtre textuel et certains filtres de périmètre. Un achat ancien peut donc
être introuvable et le total affiché ne pas représenter tout l'historique.

Recommandation : sélection SQL des racines, filtres et autorisations avant
pagination, puis chargement groupé des données de la page. Pour le filtre
`has_alerts`, prévoir des prédicats SQL ou une projection d'alertes correctement
actualisée; ne pas paginer avant de l'appliquer. Réutiliser les règles métier de
calcul des alertes. Cible initiale : au plus 12–15 SELECT par page, y compris
quand le catalogue d'achats croît, et recherche des références au-delà de 500.

### P1 — Catalogue public de coffrets

Route : `/public/commercialisation/coffrets`, notamment `avec_prestations=true`.
Sources : `app/application/commercialisation/use_cases/lister_coffrets.py:15`
et `app/application/referencement/services/gouvernance_catalogue.py:74`.

Pour 13 coffrets, **33 SELECT sans prestations, 46 avec prestations**
(852 et 1 087 ms depuis le poste). Les diagnostics sont déjà groupés, mais chaque
coffret relit le compteur de prestations et la politique BUM active; l'option
prestations ajoute une lecture par coffret. Sur ce scénario : `7 + 2N` ou `7 + 3N`.

Recommandation : compter et charger les prestations actives par ensemble de
coffrets, lire une fois la politique active et la réutiliser pour la présentation.
Pousser le filtre de type au repository. Ajouter une pagination compatible avec
les consommateurs, après application correcte de la vendabilité. Cible sur
ce scénario : environ 8–10 SELECT au lieu de 46.

Le détail d'un coffret effectue 9 SELECT (250 ms) : priorité secondaire par
rapport à la liste. Réutiliser les données déjà chargées pour le diagnostic et
la présentation, sans supprimer le contrôle BUM/Stripe.

### P1 — Catalogue public d'animations

Routes : `/public/animation-locale/animations` et `/{animation_id}`.
Source : `app/application/animation_locale/services/catalogue_animations_publiques.py`,
méthodes `rechercher`, `_projections` et `obtenir`.

**35 SELECT pour 6 animations** (1 222 ms), 9 pour le détail observé.
La projection du catalogue appelle encore `blocages_coffret` pour chaque lot :
politique BUM, coffret et qualification sont relus. Le catalogue charge également
les données nécessaires à une fiche riche, même pour des cartes de liste.
La nouvelle méthode `suggestions` optimise uniquement la recherche multiscope;
elle n'a pas remplacé cette projection.

Recommandation : contrôle BUM groupé des lots distincts, une seule politique
par appel, projection de liste limitée aux champs réellement affichés, et
réutilisation des données de détail. Cible indicative : 7–9 SELECT sur ce scénario.

Attention fonctionnelle : la page SQL est limitée avant l'exclusion BUM, ce qui
peut produire une page incomplète. `obtenir` indexe `[0]` après projection et peut
échouer si la BUM exclut l'animation. La synthèse par commune utilise la requête
SQL sans la même exclusion des lots, ce qui peut désaligner les compteurs.
Harmoniser ces règles explicitement lors de l'optimisation.

### P1 — Compteurs d'activité Marketplace

Route : `/public/exploitation/activites-locales/metriques`.
Source : `app/api/activites_locales_api.py:138` et `:165`.

**15 SELECT pour cinq indicateurs et trois périodes** (442 ms).
Chaque couple indicateur/période déclenche un COUNT distinct.
Recommandation : agréger les périodes et types en SQL avec des agrégats
conditionnels, en conservant le comptage distinct des communes et les filtres
de visibilité/expiration. Cible : 1–2 SELECT.

Le flux d'actualités lui-même est mieux structuré : **2 SELECT**, pagination
par curseur en SQL, jointures anticipées et rattachements aux communes groupés.
Il n'est pas prioritaire au même titre que ses compteurs.

### P1 — Fiche Commerçant 360

Page : `/admin/vision-360-commercant-detail`.
Source : `app/application/referencement/use_cases/vision_360_commercant_backoffice.py:166`.

**42 SELECT sur le commerçant de test choisi** (940 ms; 43 sur le jeu local).
Les quatre périodes déclenchent chacune quatre agrégations, puis la fiche
charge immédiatement profil, prestations, validations, achats, support,
communications, documents, anomalies, activités, audit et notes.

Recommandation : regrouper les agrégations des périodes par source, charger
les sections secondaires à l'ouverture de leur onglet et limiter les colonnes.
Conserver des requêtes bornées et la fraîcheur des données financières.
Cible initiale : 10–15 SELECT pour l'écran initial, lectures annexes à la demande.

### P1 — Verrou en consultation ERP commerçant

Route : `/internal/erp/api/commercants/{mid}`.
Source : `app/application/commercialisation/services/atelier_erp.py:59` et `:134`.

`detail_commercant` appelle `dossier`, qui effectue un `SELECT ... FOR UPDATE`.
Le verrou peut rester détenu pendant la construction du détail et l'évaluation
des aptitudes jusqu'au commit de `session_erp`. Plusieurs consultations ou une
modification du dossier peuvent donc attendre inutilement.

Constat statique, **aucun test de contention ni profilage de ce verrou n'a été
exécuté sur la base de test**. Séparer la lecture simple de la lecture verrouillée;
garder les verrous dans les commandes qui modifient le dossier. Un verrou de
ligne peut bloquer les opérations concurrentes qui réclament un verrou incompatible.
[Documentation PostgreSQL](https://www.postgresql.org/docs/18/explicit-locking.html).

### P1 — Détail d'une ville : correction simple

Route : `/public/referencement/villes/{ville_id}`.
Source : `app/application/referencement/use_cases/consulter_detail_ville.py:10`.

Une seule requête, mais **toutes les villes sont chargées et converties en
objets métier** avant la recherche de l'identifiant en Python. Aujourd'hui,
4 lignes sont lues pour en retourner une; le coût sera proportionnel au nombre
de villes. Remplacer `uow.villes.lister()` par le repository `obtenir(id)` et
conserver le même comportement 404. Vérifier par test qu'une seule ligne est lue.

## Seconde priorité et montée en volume

| Service | Constat | Action recommandée |
|---|---|---|
| Support — objets connexes `/internal/erp/api/instances/{id}/connexes` | 19 SELECT : contrôle d'accès + COUNT/liste pour 9 familles, même vides; 461 ms. Le résumé les charge automatiquement (`instances.js:56`). | Charger les familles visibles à la demande, regrouper les compteurs, sélectionner uniquement les champs du résumé. Garder leur pagination et leurs permissions. |
| Synthèse vendabilité `/internal/commercialisation/vision-360/synthese` | 11 SELECT, dont une requête par famille de blocage; 326 ms. | Agrégations conditionnelles groupées, sans recalculer toute la vendabilité en ligne. |
| Chronologies Animation 360 et Achats 360 | Chargement de toutes les sources, fusion/tri/filtre/curseur en Python; 8 SELECT et 31 lignes seulement dans l'animation mesurée. | Appliquer dates et curseurs aux sources SQL; fusion SQL ou fusion bornée des sources. Tester plusieurs milliers d'événements et les égalités de dates. |
| Indicateurs Animation 360 | Participants, validations et gains chargés intégralement puis agrégés en Python; cache présent mais le remplissage reste coûteux. Constat statique. | COUNT/SUM/groupement temporel SQL; conserver le périmètre d'autorisation dans le cache. |
| Recherche/liste villes | Préfixe SQL mais aucune limite; proximité : toutes les villes publiées géoréférencées, calculs de distance en Python. | Limite contractuelle pour suggestions; présélection géographique avant distance exacte si volume nécessaire. Ne pas changer silencieusement l'inclusion géographique. |
| Liste commerçants et catalogue coffrets | Listes sans pagination; certains filtres de statut/type en Python. | Filtrage au repository, projections légères, pagination avec adaptation des consommateurs. |
| OnBoard — liste et indicateurs | 1 SELECT chacun, mais tous les dossiers sont chargés. Les blocages sont filtrés après sérialisation et les indicateurs calculés en Python. | Pagination SQL et agrégations; préserver la sémantique du filtre de blocage. |
| Profil public commerçant | 4 SELECT, 147 ms; pas de N+1 constaté. Toutes les notes de feedback sont néanmoins chargées pour calculer la moyenne. | Agrégation SQL des avis; pas de refonte prioritaire de toute la fiche. |
| Dashboard commerçant | 3 SELECT; projection de colonnes et période bornée. Les lignes détaillées sont ensuite agrégées en Python. | Surveiller les commerçants à fort historique avant d'engager une refonte. |

Les usages d'OFFSET méritent des mesures sur les pages profondes : PostgreSQL
calcule également les lignes sautées. Préférer un curseur lorsque le parcours
le permet, avec un ordre total et stable.
[Documentation PostgreSQL](https://www.postgresql.org/docs/18/queries-limit.html).

## Services déjà raisonnablement structurés

- Recherche instances Support : **2 SELECT** avec filtres et pagination SQL;
  détail : **3 SELECT** hors écriture d'audit du parcours HTTP.
- Liste commerçants ERP : **2 SELECT**, filtres et pagination SQL.
- Liste de suivi de vendabilité : **2 SELECT**, projection de diagnostic existante.
- Recherche Animation 360 : **6 SELECT**, pagination SQL et chargements groupés.
- Liste des animations du commerçant : **6 SELECT**, pagination SQL et agrégat
  groupé des validations. Le portail gestionnaire utilise lui aussi des résumés
  groupés (`animation_locale_api.py:1365`), revu statiquement.
- Fil d'actualités public : **2 SELECT** avec curseur SQL.

Ces constats portent sur les volumes actuels, pas sur une capacité garantie
à forte charge. Les jointures explicites et chargements groupés évitent de
produire une requête supplémentaire à chaque accès à une relation ORM.
[Documentation SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html).

## Effet des interfaces et ordre de réalisation

La page ville Marketplace appelle le catalogue avec les prestations, les
commerçants, les animations et les compteurs. La fiche commerçant recharge aussi
le catalogue et les commerçants de la commune pour construire son contexte
(`CityPage.jsx:298`, `CommercantPage.jsx:439`). Le coût cumulé d'une page ne se
résume donc pas à celui de son endpoint principal. Vérifier quels enrichissements
sont nécessaires immédiatement, partager les clés de cache et propager
l'annulation aux lectures devenues inutiles. Ne pas retirer des informations
utiles ou changer le parcours sans vérifier les consommateurs.

Ordre conseillé :

1. Catalogue coffrets + catalogue animations + compteurs Marketplace, pour
   accélérer les pages publiques les plus sollicitées.
2. Recherche Achats 360, dont le coût et la troncature de l'historique justifient
   un chantier dédié en parallèle de priorité produit, puis Commerçant 360.
3. Détail ville et lecture ERP sans verrou, corrections courtes à intégrer
   au premier lot compatible.
4. Objets connexes Support, synthèses et chronologies.
5. Tests à volume croissant, index adaptés aux requêtes finales, puis capacité
   sous charge. Éviter de commencer par augmenter le pool ou ajouter un cache
   global de réponses dont la publication/BUM/Stripe serait difficile à invalider.

Chaque correction doit conserver les autorisations, l'ordre stable, les versions
historiques, les règles de publication, les filtres BUM/Stripe et les totaux.
Ajouter des budgets de SELECT, des tests de pagination/complétude et des jeux
avec nombreux candidats exclus. Mesurer ensuite les endpoints HTTP déployés
avec p50/p95/p99, concurrence, erreurs et attente du pool. Les budgets proposés
ci-dessus sont des cibles de réalisation, pas des résultats déjà atteints.

## Preuves conservées

Répertoire local ignoré par Git :
`output/performance/consultations-audit-20260912/`.

- `profile_reads.py`, `profile_additional.py` : profileurs bornés, en lecture seule.
- `local.json`, `remote.json`, `additional-local.json`, `additional-remote.json` :
  compteurs, durées, volumes renvoyés et empreintes/fréquences des SELECT.
- Aucun contenu de réponse, paramètre SQL sensible ou secret n'est enregistré
  dans le rapport. Les fichiers de configuration et clés API sont conservés.

Le profilage n'applique aucune migration et n'installe aucun index. La priorité
donnée aux index devra être confirmée par des plans d'exécution sur les volumes
cibles; cet audit établit d'abord les coûts structurels et les requêtes répétées.
