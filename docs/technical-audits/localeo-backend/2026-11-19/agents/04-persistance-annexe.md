# Annexe — persistance

Complément de la [première analyse indépendante](04-persistance.md), sans consultation des rapports des autres agents. Cette annexe ne constitue pas une consolidation transverse.

## Contre-exemples et garanties observées

- `app/infrastructure/persistence/db.py:33–44`, `construire_options_pool` : taille/overflow/timeout/recycle configurables et validés ; valeurs par défaut 5/5/30 s/1800 s, pré-ping activé. Aucun diagnostic de sous-dimensionnement ne peut être tiré sans nombre de processus, sessions actives et capacités PostgreSQL effectives. Les limites autorisées de configuration ne sont pas les valeurs déployées.
- `app/infrastructure/persistence/uow/sqlalchemy_unit_of_work.py:76–80,216–225`, `SqlAlchemyUnitOfWork` : session créée explicitement, rollback sur exception, fermeture à la sortie, commit explicite. Aucune fuite globale démontrée. La construction d'une session ne suffit pas à prouver qu'une connexion est déjà empruntée.
- `app/infrastructure/persistence/repositories/productivite_animation.py:121–153`, `page` : portée et filtres avant `LIMIT`, curseur sur clés d'ordre, lecture `limit + 1`, compteurs sur les seuls IDs retenus. `dashboard_agregats:264–292` : cible jointe avant comptage, séries groupées et top 10, alertes limitées à 50. Le mode `borne` est donc distingué de DB-01.
- `app/infrastructure/persistence/repositories/animation_locale_repositories.py:1350–1382,1520–1544` : pages tenant pour participants et validations avec count et limite SQL. La présence d'autres méthodes non bornées ne prouve pas que ces pages les appellent.
- `app/infrastructure/persistence/repositories/repositories_sqlalchemy.py:1118–1134`, `EmailSortantRepositorySqlAlchemy.lister_a_envoyer` : état de travail filtré avant limite et réservation avec `SKIP LOCKED`. Ne pas généraliser DB-03 à toute l'outbox.
- `tests/integration/test_reaudit_integrity.py:76–97`, `test_reaudit002_expiration_respecte_validation_et_remboursement` : scénario source couvrant remboursement en cours et instance verrouillée par validation. Lu, non exécuté ; sa présence est une intention de preuve, pas un résultat courant. Il faut le préserver lors du remède DB-02.

## Observations secondaires et hypothèses non promues

**DB-S01 — Lectures unitaires des commerces du passeport.** `app/application/animation_locale/services/jeu_animation.py:399–408`, `ServiceJeuAnimation.lire`, parcourt les `merchantIds` et appelle `uow.commercants.obtenir` pour chacun. L'entrée montée est `GET /public/localeo-live/participations/{participation_id}`, `app/api/jeu_animation_api.py:73–89`, montage `app/main.py:543–544`. Motif répétitif étayé, mais longueur des parcours et fréquence réelle non établies ; non retenu parmi les majeurs devant les lots pouvant contenir des milliers d'instances. Un chargement par IDs serait envisageable. Aucun nombre de requêtes exécutées mesuré.

**DB-S02 — Index de sélection des expirations. HYPOTHÈSE À VÉRIFIER.** `CoffretInstanceOrm.date_expiration`, `app/infrastructure/persistence/models.py:498`, n'a pas de `index=True` ; la recherche textuelle des SQL n'a pas identifié d'index composite explicite correspondant au prédicat statut/date de DB-02/DB-03. Cela ne démontre ni absence d'index réel ni scan séquentiel : DDL historique, sélectivité et plan doivent être contrôlés sur une cible autorisée. Un index éventuel ne résoudrait ni N+1 ni ordre de filtrage. Aucun SQL ni `EXPLAIN` exécuté.

**DB-S03 — Cadence des validations.** `app/application/animation_locale/services/validations_animation.py:132–138` charge les validations du commerçant de la dernière minute pour en prendre la longueur et les annulations du participant pour trouver la précédente. Le repository applique ces filtres en SQL ; `sql/v272_bons_lots_numeriques.sql:95` livre un index `(commercant_id,validated_at,id)`. Optimisation de projection possible, mais aucune anomalie majeure établie sans volumétrie de la minute et historique d'annulation. Les preuves anti-fraude ne doivent pas être remplacées par un seuil approximatif.

## Migrations et indexes lus

| Source livrée | Observation autorisée | Ce qui n'est pas prouvé |
|---|---|---|
| `sql/v141_relances_expiration_coffrets.sql:17–41` | Index simples et unicité partielle pour relances avant/après expiration | Installation effective, utilisation et coûts du plan |
| `sql/v272_bons_lots_numeriques.sql:94–102` | Index historiques par commerçant/date et modes | Sélectivité et temps des recherches |
| `sql/v282_e73_listes_globales.sql:2–5` | Index participants/validations par animation/date/ID | Performance des chargements sans portée animation |
| `sql/v313_animation_productivite.sql:2–10` | Extension trigrammes, index tenant/page, nom, préfixe email et référence | Extension installée et plans effectifs |
| `sql/v315_qualifications_exactes_animation.sql:12–18,55` | Index des projections de participants et qualification | Toute requête en tire effectivement parti |

Les recherches ont inclus `sql/schema.sql`, `baseline_v147.sql` et les migrations versionnées pour éviter de conclure à partir du modèle ORM seul. Aucun fichier SQL n'a été modifié ou appliqué. Les contraintes d'unicité sont des garanties de cohérence utiles ; elles ne transforment pas une boucle de requêtes en lecture groupée.

## Lectures directes et vérifications de mission

Instructions : README projet, backend `AGENTS.md`, `AGENT.md`, README ; prompt `prompts/02-agents.md`. Cartographie autorisée consultée : `inventaire/architecture.md` et `inventaire/flux-critiques.md`. Aucun autre rapport d'agent lu.

Sources directement ouvertes : `requirements.in`, passages du lock `requirements.txt`, `app/main.py`, `app/infrastructure/persistence/db.py`, UoW SQLAlchemy, `models.py`, `mappers.py`, repositories SQLAlchemy et Animation, repository productivité ; services pilotage, gestion, jeu et validations Animation ; use case expiration Coffrets ; API Animation et instances Coffrets ; définition de batchs. Recherches ciblées supplémentaires : services/UC gestion achats, repositories reversements, recherche achats et bilans. Ces recherches ne constituent pas une revue exhaustive de chacun de ces modules.

Tests sources lus : `tests/application/use_cases/test_gestion_achats_use_cases.py:416–448` (détail email et lots vides), `tests/integration/test_reaudit_integrity.py:76–97` (cohérence expiration/validation/remboursement). Aucun test exécuté ; aucune preuve existante de progression multi-page des relances n'est déduite de ces tests limités.

Commandes réellement utilisées : lecture de fichiers UTF-8 avec `Get-Content` et numérotation PowerShell ; recherches `rg`/inventaires `rg --files` ; `git rev-parse HEAD` et `git status --short`. Des globulations Windows invalides ont été remplacées par des recherches de répertoires ciblées ; elles n'ont déclenché aucun code métier. Les vérifications des documents livrés sont limitées à leur contenu et à leurs chemins. Les contrôles documentaires communs éventuels sont à coordonner par l'orchestrateur ; ce rapport ne revendique aucune exécution de leur part.

Limites : pas de schéma réel, statistiques PostgreSQL, plans, nombre de lignes, profil de connexions, cache chaud/froid, fréquence des clients, journaux ou télémétrie. Pas d'inventaire exhaustif de chaque requête et transaction. Aucun benchmark, serveur, migration, refactor, déploiement ou accès à des secrets. Les constats restent séparés d'une future campagne de mesure et de la décision de corriger.
