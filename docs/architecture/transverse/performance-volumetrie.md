# Performance, volumétrie et tenue en charge

Convention de conception du **18 octobre 2026**, applicable aux nouvelles évolutions et aux chemins existants qu’elles modifient, dans les cinq dépôts Localeo. Elle complète les [contrats API](conventions-api-openapi.md), la [matrice d’architecture](controle-architecture.md) et le [dispositif de mesure E59](../../specifications/epic-59-tests-performance-api/README.md). Elle ne certifie pas les performances actuelles et ne déclenche pas une réécriture générale.

## Objectif et limites

Une consultation interactive doit dépendre de la page ou de la cible demandée, pas du volume global de la plateforme. Une recherche indexée peut garder un coût logarithmique ; un export exhaustif, un calcul global ou un tirage complet garde un travail proportionnel à sa population. Pour ces traitements, borner mémoire, transactions, concurrence et pression sur les parcours interactifs plutôt que promettre une durée constante.

Aucune architecture ne garantit des temps constants avec un trafic illimité. Chaque évolution touchant données ou trafic décrit son enveloppe de capacité, ses budgets et son comportement à saturation. Un seuil non mesuré est un objectif, jamais une performance acquise. Une exception précise périmètre, justification, borne, preuve et condition de réexamen dans la spécification concernée.

## P01 — Contrat de coût par opération

Pour les parcours concernés, documenter : population totale et population autorisée, filtres et tris, taille de page/lot, colonnes rendues, nombre de requêtes, objets hydratés, stratégie d’accès/index, frontière transactionnelle, cadence/concurrence et preuve attendue. Inclure les routes ERP, sélecteurs, permissions, workers et exports, pas seulement les listes publiques.

La spécification fixe les bornes structurelles dès la conception. Avant activation, le rapport de capacité complète p95/p99, taux d’erreur, débit soutenu, mémoire et attente de verrous/pool, avec matériel et volumes. Reprendre les seuils de parcours E59 en indiquant leur statut ; un seuil initial n’est pas une garantie contractuelle.

## P02 — Pagination côté serveur et curseurs stables

- Toute nouvelle liste dont la cardinalité peut croître est paginée **dans la requête de stockage**, après filtrage par droits et périmètre. Ni chargement complet suivi d’une tranche en mémoire, ni filtrage d’accès après `LIMIT`.
- Valeurs par défaut des nouvelles listes HTTP : `limit=25`, maximum `100`, validation serveur et contrat OpenAPI. Une exception bornée, par exemple un référentiel fini, doit annoncer sa cardinalité maximale. Les enfants d’une fiche sont également bornés ou servis par des sous-listes.
- Utiliser une pagination par clé pour les listes évolutives : ordre total avec identifiant unique de départage, par exemple `(created_at DESC, id DESC)`, prédicat de continuation aligné sur cet ordre et index correspondant. Un curseur opaque qui contient seulement un numéro de page/offset ne satisfait pas cette règle. Éviter les offsets profonds ; leur maintien historique exige un plafond et un plan de compatibilité.
- Le curseur est validé, lié aux filtres, au tri, au contexte d’accès et à la version de contrat ; il n’accorde aucun droit. Définir ordre des valeurs nulles, expiration et réponse au changement de filtre. Lire au plus `limit + 1` racines pour produire `has_more`/`next_cursor`, sans `COUNT(*)` exhaustif obligatoire.
- Un ordre immuable est préférable. Pour un tri sur champ modifiable, annoncer la sémantique de navigation vivante et permettre une réinitialisation ; pour un export, une audience ou une preuve exigeant exhaustivité, utiliser un instantané cohérent. Un curseur seul ne garantit pas un instantané face aux mises à jour/suppressions.
- Joindre une collection ne doit pas multiplier les racines avant pagination : paginer d’abord les IDs autorisés, puis enrichir cette seule page par requêtes groupées. Pas de total recalculé sur tout l’historique à chaque page ; total facultatif, projeté/daté, ou calcul dédié selon le besoin.

## P03 — Lectures ciblées, absence de N+1 et mémoire bornée

Les ports de lecture expriment critères, projection, ordre et borne. Pour une liste, sélectionner uniquement les colonnes nécessaires, sans charger l’agrégat complet, les pièces binaires, les contenus d’audit ou les collections historiques. Les adaptateurs peuvent produire des DTO de lecture ; cela ne leur transfère pas les invariants métier.

Interdire une lecture non bornée de type `.all()`/`list(query)`/`SELECT *` sur une population évolutive dans un parcours interactif ou un job. Une collecte après un `LIMIT` effectif ou sur un ensemble de clés lui-même borné est permise. Un itérateur n’est pas une preuve de streaming si le driver ou la session ORM conserve toutes les lignes : vérifier la mémoire et libérer les objets entre lots.

Éviter les requêtes par ligne, les associations chargées paresseusement pendant la sérialisation et les appels HTTP individuels pour enrichir chaque carte. Privilégier enrichissements groupés, jointures bornées et projections. Le nombre de requêtes d’une page doit rester borné indépendamment du nombre total de lignes ; tester aussi 25 puis 100 résultats pour détecter un N+1. Une requête unique avec un produit cartésien géant n’est pas une amélioration.

Les listes de paramètres `IN`, les actions groupées, les quantités demandées et les données compressées entrantes sont bornées ; pour un ensemble volumineux, utiliser lots ou table de travail. Une limite de taille de fichier compressé ne borne pas sa taille décompressée ni la mémoire du parseur.

## P04 — Index conçus à partir des requêtes

Chaque chemin critique nomme ses prédicats d’égalité/périmètre, plage, tri et contrainte d’unicité ; la migration propose les index correspondants. Choisir l’ordre des colonnes selon la requête effective, souvent contexte/égalités puis plage/tri et ID. Vérifier les accès globaux des workers séparément des accès par tenant : un index commençant par tenant ne suffit pas automatiquement à une recherche globale des échéances.

Vérifier les index des clés de relation utilisées par jointures et suppressions ; leur présence n’est pas déduite de l’existence d’une FK. Prévoir les unicités d’idempotence et les index partiels des états actifs/à traiter quand ils sont adaptés. Éviter les index redondants : coût d’écriture, taille, maintenance et contention font partie de la décision.

Pour l’email ou les textes normalisés, aligner normalisation métier, colonne/expression indexée et prédicat. Une recherche par sous-chaîne, un `OR` sur plusieurs champs ou un filtre JSON ne bénéficient pas automatiquement d’un index B-tree ordinaire ; prévoir un accès adapté ou restreindre explicitement le contrat de recherche. Ne pas ajouter un moteur ou une extension sans besoin démontré.

Vérifier les plans PostgreSQL sur des données représentatives, avec statistiques actualisées : `EXPLAIN (ANALYZE, BUFFERS)` sur une cible jetable, lignes parcourues/rendues, tris, lectures, spills et temps. `ANALYZE` exécute la requête ; pas de commande mutante sur une base d’exploitation. Un parcours séquentiel peut être correct pour une petite table ou un export couvrant la majorité des lignes : ne pas imposer un index par principe ni forcer le plan. À l’inverse, un index présent dans la migration ne prouve pas son utilisation utile.

## P05 — Traitements volumineux et projections

Exports, purges, diffusion, recalculs, reprises et migrations de données utilisent des jobs persistés et des lots bornés, avec progression, point de reprise, annulation adaptée et idempotence. Aucun export exhaustif dans une réponse HTTP synchrone ni archive complète en mémoire. Streamer aussi les fichiers/médias et borner l’espace temporaire ; conserver les droits et la rétention du contrat métier.

Définir une capture cohérente pour les traitements exhaustifs : source immuable/versionnée, matérialisation contrôlée ou instantané de base mesuré. Paginer avec un simple plafond d’ID ne fige pas des critères qui changent. Une longue transaction d’instantané peut retenir des versions et affecter la maintenance ; sa durée et son impact sont mesurés. Pas de verrou global conservé pendant les échanges réseau.

Les agrégations de bilan, coût et recherche globale sont incrémentales ou préparées si leur recalcul dépasse le budget interactif. Exposer date de calcul/couverture. Les compteurs de décision, droits, disponibilité et remboursements restent synchrones et cohérents ; un cache ou une projection différée ne remplace pas leur autorité. Une reconstruction depuis le journal est un traitement dédié, pas un scan de tout le journal à chaque commande.

Pour une opération métier atomique dont les résultats peuvent être nombreux, distinguer préparation invisible et validation finale. Décrire bornes et protocole de visibilité/reprise ; ne pas remplacer silencieusement « tout ou rien » par des commits partiels. Les parties nécessairement proportionnelles au nombre de résultats restent mesurées ; le simple passage en job ne résout pas une transaction ou une collection non bornée.

## P06 — Trafic, contention et saturation

Limiter durée et nombre de lignes verrouillées aux invariants concernés ; ordre de verrous commun. Ne pas charger toutes les appartenances pour autoriser une cible, ni verrouiller toute une commune pour une remise. Préserver les contrôles immédiats de révocation et les règles DDD ; leur optimisation repose sur des faits courants indexés/versionnés, pas sur leur omission.

Les jobs prennent un nombre borné de tâches avec bail court, échéance et reprise. Un `SKIP LOCKED` sans `LIMIT` reste non borné. Configurer parallélisme, taille des lots, budgets de connexion, délais SQL/verrous/réseau et nombre de retries ; ajouter temporisation et dispersion des reprises. Une file persistée absorbe un pic, pas un déficit permanent de capacité : suivre son âge et son débit, isoler les traitements lourds des validations et éviter qu’un gros tenant monopolise les workers.

À saturation, mettre en attente les tâches autorisées ou refuser explicitement selon le contrat ; ne pas accumuler sans borne requêtes, threads, promesses, connexions ou mémoire. L’échec technique n’est pas un quota commercial. Les retries ne doublent aucun effet et ne déclenchent pas une tempête de requêtes. Ne pas créer un worker/concurrent par destinataire.

## P07 — Frontends et caches

Charger uniquement les pages visibles/demandées ; ne pas parcourir automatiquement toutes les pages pour recréer une pagination locale ou un sélecteur. Déclencher la recherche côté serveur, annuler les requêtes obsolètes et borner rafraîchissements, polling et enrichissements concurrents. Borner les pages conservées en mémoire et les éléments DOM ; une liste virtualisée ne corrige pas un téléchargement exhaustif.

Clés de cache par contexte autorisé/filtres/tri/version ; invalidation au changement d’organisation, de droits ou de mutation pertinente. Ne pas servir des droits révoqués depuis un cache ancien ni mélanger des tenants. Le cache peut réduire le coût d’une lecture déjà bornée ; vérifier aussi le comportement à froid et les reconstructions simultanées. Une optimisation de cache ne dispense pas d’un index ou d’une stratégie de données appropriée.

## P08 — Preuves et critères de revue

Réutiliser [E59](../../specifications/epic-59-tests-performance-api/conception-technique.md) et sa [procédure](../../exploitation/technique/executer-campagne-tests-performance-api.md), sans lancer implicitement une charge sur un environnement partagé. Compléter les tests API par mémoire/rendu navigateur pour P07.

| Axe | Preuve attendue |
| --- | --- |
| Volumétrie | Même page/cible à N puis 10N données, en faisant croître séparément le tenant consulté, les tenants étrangers et l’historique ; premières et pages profondes, filtres fréquents/rares, absence de résultat |
| Trafic | Jeu fixe, paliers de concurrence/débit, tenant très actif, plusieurs tenants, lectures/écritures/jobs mêlés ; point de saturation et retour à la normale |
| Requêtes | SQL réellement exécuté, nombre de requêtes, lignes parcourues/hydratées, octets, plan et index ; absence de coût linéaire en volume global pour une page ou une cible |
| Ressources | p50/p95/p99, erreurs, mémoire maximale, CPU/I/O, pool et verrous, taille/âge des files ; caches froids et chauds distingués |
| Reprise | Interruption entre lots et après commit, worker concurrent, acteur révoqué, premier/dernier crédit ; aucun doublon ni changement de règle pour gagner du temps |

Avant de conclure, renseigner budgets chiffrés et résultats dans la matrice de l’epic : environnement, commit, index/statistiques, données, profil, limites et comparaison. Un budget dépassé ou non mesuré ne vaut pas acceptation. Une dégradation proportionnelle au volume global sur un parcours censé être borné impose une correction ou une exception explicite ; ne pas choisir des seuils permissifs après le test pour masquer la régression.
