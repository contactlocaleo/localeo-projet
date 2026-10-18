# E73 — Suivi de réalisation locale

Début : **18 octobre 2026**. [Spécification](README.md), [backlog](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md), [matrice des 63 critères et preuves](verification-livraison.md). Objectif : les 38 US, dans les dix lots demandés. Les lignes ci-dessous ne valent pas acceptation tant que les preuves correspondantes ne sont pas enregistrées.

## Restrictions et état initial

Implémentation, bases jetables locales, tests isolés et commits locaux uniquement. **Aucun push, pipeline distant, déploiement, migration/configuration de test/démo/production, envoi réel ou paiement réel.** Les vérifications humaines et hébergées restent des étapes futures explicites. Ne pas confondre commits et livraison.

| Dépôt / branche | HEAD initial | Travaux préexistants à préserver |
| --- | --- | --- |
| Projet / main | `cc9991dd3679075e232f53844362405acfdc77a2` | Spécification E73 et règles associées à committer séparément ; modification étrangère `docs/specifications/moteur-animation/suivi-implementation.md` exclue |
| Backend / main | `31807b633932c2a53bb64714e978359683f9cfe1` | Aucun changement suivi |
| Animation / main | `08863e8202a3caad3c886918b0543cd2f260aec3` | README, App.tsx, ExploitationView.tsx, tests/browser/exploitation.mjs : conservation et staging sélectif requis |
| Commerçant / main | `19f7a20ebedae79f50453aefbf48c9724ed28eb1` | Aucun changement |
| Marketplace / main | `4186e44e8320a9c016d678da3f28583849452867` | Aucun changement |

## Plan et statut des lots

| Lot | US / portée | Dépôts prévus | État / preuves / commits |
| --- | --- | --- | --- |
| 00 | Sources, référence initiale, protocole UX et suivi | Projet ; lecture des quatre applications | Sources et contrôles de référence : commit Projet `be776b1` ; matérialisation des squelettes UX poursuivie dans les lots applicatifs |
| 01 | US25–26 comptes, équipe, organisation, récupération, transfert | Backend, Animation, Projet | Implémenté et vérifié localement pour CA50–53 ; backend `45d0b56` et preuve complémentaire `a17e3f4`, Animation `05c0561`, Projet `9519696` ; limites de conservation et recette hébergée ci-dessous |
| 02 | US11–13 ; parties US24/36, périmètres et onboarding | Backend/ERP/OnBoard, Commerçant, Animation, Projet | Implémenté et vérifié localement pour les produits existants ; Backend `261ebdc`, Pro `bc9d1ac`, Animation `7cab528` ; branches numériques et exploitabilité reprises aux lots 05/10 |
| 03 | US03,14–17,27–28 ; souscriptions/modules/finance | Backend, Animation, Projet | À réaliser |
| 04 | US01–02,04 ; branche externe US07–08 | Backend, Animation, Marketplace/Live, Projet | À réaliser |
| 05 | US05–10 ; complément numérique US07–08 | Backend, Animation, Commerçant, Marketplace/Live, Projet | À réaliser |
| 06 | US19–20 ; import/deltas/reprise | Backend, Animation, Projet | À réaliser |
| 07 | US18,30 ; chasse et préparation accompagnée | Backend, Animation, Projet | À réaliser ; dépendance readiness E55 |
| 08 | US21–22 ; communication participants | Backend, Animation, Marketplace/Live, Projet | À réaliser |
| 09 | US23,29,31–33 ; parcours/site/assistance/bilans | Backend, Animation, Marketplace/Live, Projet | À réaliser |
| 10 | US34–38 ; finalisation US24, exploitabilité/pilote | Les cinq dépôts selon impact | À réaliser localement ; aucune activation distante autorisée |

Les US partagées ne sont acquises qu’après toutes leurs branches. Reprendre les identifiants CA du plan de vérification, sans en changer la portée. Chaque bilan de lot doit enregistrer fichiers/contrats, migrations, fixtures, commandes, résultats, revue, limites et commits par dépôt. Si nécessaire, subdiviser un lot en incréments explicitement non terminaux ; aucune validation par simple présence d’un fichier.

## Préparation UX et capacité

Le squelette gestion et le squelette communication ainsi que leurs parcours de référence sont définis dans [les parcours SaaS, section 5](perimetres-parcours-saas.md). Les premières réalisations doivent matérialiser organisation/commune, navigation stable, états vides/erreurs et continuité des formulaires. Prévoir une revue locale du parcours organisateur liste → création → contrôle de publication et du parcours visiteur découverte → inscription → Live avant généralisation. La recette humaine suit Localeo puis Martignas-sur-Jalle ; elle n’est pas encore réalisée.

Capacité : 10 communes, 10 000 participants au total, 10 utilisateurs actifs simultanément ; paliers et distributions concentrées décrits par E73-PERF-01 à 08. Les tests hébergés, RPO 4 h/RTO 8 h sur hébergement représentatif et ouverture du pilote restent **non exécutés**. Les essais locaux n’en constituent pas une preuve de livraison.

## Dépendances et contrôles initiaux

E55, E68, E70 et E72 restent dans leur état produit propre. Les contrats et implémentations réels sont relus pour chaque lot dépendant ; leur existence ne prouve pas une disponibilité hébergée. E71 reste une epic indépendante ; adapter les projections nécessaires sans réaliser implicitement tout le CRM.

- Documentation : `check_guidance.py` ciblé : 102 guides, 1 181 liens, zéro erreur/avertissement ; `sync_documentation.py --check-sources` : 122 documents vérifiés ; `git diff --check` réussi.
- Backend : `scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q --basetemp .artifacts/e73-baseline-20261018-01 --tb=short` : **467 réussites**. Le premier essai sans répertoire temporaire explicite comptait 452 réussites et 15 erreurs de permission du répertoire Windows temporaire ; la reprise isolée dans le workspace les résout sans modifier les assertions.
- Animation : baseline frontend confiée au lot 01 ; résultat à consigner.
- PostgreSQL : inventaire local en lecture seule ; aucune connexion à une base d’exploitation.

## Journal de réalisation

### Lot 00 — Préparation

Lecture des instructions, inventaire des cinq dépôts et répartition des responsabilités. Backend lot 01 et frontend lot 01 confiés à des agents distincts, sans permission de commit/push ; intégration et commits par l’agent principal. Inventaire de tests PostgreSQL confié en lecture seule. Aucun changement applicatif déclaré validé à ce stade.

### Lot 01 — Comptes et équipes

Périmètre : US25–26 / E73-CA-50 à 53. Le domaine `EquipeOrganisation` possède les changements d’appartenances, délégations et responsabilité ; les services orchestrent transactions, identité globale, invitations et projections. Le portail comporte les parcours compte, équipe, choix d’organisation/commune et récupération d’accès. L’ERP permet la vérification des demandes et la récupération assistée avec preuve et motif. Les listes équipe, invitations et demandes sont paginées en SQL ; les contrôles de responsabilité utilisent une lecture ciblée de la racine et du nombre de responsables.

Les nouvelles routes sont intégrées à la liste explicite du middleware navigateur Animation : contrôle d’origine, prévol CORS, cookie, CSRF et séparation des routes ERP. Une session d’identité seule peut accepter une invitation sans recevoir de données d’organisation. La perte du contexte d’une session complète continue de produire un refus.

Migrations préparées : `v260_e73_equipes_organisations.sql` et `v261_reinitialisation_mot_de_passe_animation.sql`. Le générateur local produit les appartenances et rattachements synthétiques ; le registre d’export/restauration inclut les six nouvelles tables. Les invitations et récupérations réelles n’ont pas été envoyées. Une future reprise des comptes historiques nécessite la vérification explicite de leurs responsabilités et rattachements ; aucune responsabilité n’est déduite automatiquement.

Preuves réellement exécutées :

| Contrôle | Commande / preuve | Résultat |
| --- | --- | --- |
| Transport navigateur, mot de passe, API et persistance | `scripts/validation/test_isolated.py tests/security/test_animation_browser_session.py tests/security/test_mot_de_passe_animation_postgres.py tests/api/test_animation_password_api.py tests/application/identite_acces/test_gestion_mot_de_passe_animation.py tests/application/identite_acces/test_gestion_acces_animation_reset.py tests/domain/identite_acces/test_mot_de_passe_animation.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp .artifacts/e73-password-final-01 --tb=short` | **130 réussites**, deux avertissements de dépréciation Starlette/httpx |
| Migrations complètes, rejeu et démonstration/restauration | `scripts/validation/test_isolated.py tests/integration/test_data015_migrations.py tests/security/test_demo_equipes_animation_postgres.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_migrations_test --basetemp .artifacts/e73-migrations-final-01 --tb=short` | **4 réussites** ; avertissement SQLAlchemy de réflexion `dialect_options` |
| Régression frontend Animation | `npm.cmd test` | **181 réussites**, zéro échec et zéro test ignoré ; types et lint réussis |
| Navigateur ERP | `node tests/browser/equipes-animation-erp.cjs` | Réussi à 390 et 1 280 px : lecture, preuve obligatoire, CSRF/idempotence, erreurs 409, issue réseau incertaine et relecture, absence de débordement |
| Navigateur portail | `node tests/browser/organisation-access.mjs` et `node tests/browser/account-app.mjs` | 111 assertions de composants et 48 assertions dans App ; API synthétique locale, formats mobile et bureau |
| Contrats embarqués et build isolé | Export hors ligne `generate_epic41_openapi.py`, copie consommateur Animation ; `node --test tests/generation-http-contracts.test.mjs tests/publication-http-contracts.test.mjs` ; `node scripts/build-generation-tests.mjs` | 749 routes exportées, 5 tests réussis, build réussi sans fichier opérateur ; avertissement de chunk principal 839,83 ko, à traiter dans la maîtrise des chargements du lot 09 |
| Pagination et plans SQL équipe | `scripts/validation/test_isolated.py tests/security/test_equipes_animation_performance_postgres.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp .artifacts/e73-team-perf-02 -q -s --tb=short` | **2 réussites**, 10 103 appartenances dont 6 002 dans une organisation ; requêtes réelles capturées puis `EXPLAIN ANALYZE BUFFERS`, aucun réglage forçant un index |

Les pages d’équipe initiale, suivante et après 5 000 membres utilisent `idx_equipe_animation_membres_page`, avec limite 26 et curseur SQL, sans `OFFSET`. Mesures ponctuelles à chaud : 0,037 / 0,067 / 0,040 ms pour ces requêtes, coûts estimés 4,31 / 4,38 / 6,85. La liste d’organisations utilise `idx_equipe_animation_organisations_page` ; PostgreSQL choisit librement une lecture séquentielle de la petite table des 102 organisations pour une jointure, sans balayage des appartenances. La projection complète utilise neuf requêtes pour des pages de 1 ou 100 membres, avec respectivement 3 ou 102 membres hydratés au maximum. Ces mesures caractérisent la lecture locale et ne prouvent ni le trafic simultané ni un engagement de temps de réponse.

Revue indépendante : les premiers 42 tests métier/HTTP/PG passaient, mais deux scénarios supplémentaires ont révélé une acceptation après suspension globale de l’auteur et une récupération vers un successeur suspendu. Les corrections et tests persistés ont été vérifiés indépendamment : `test_equipes_animation_postgres.py -k 'invitation_refuse_auteur_suspendu or recuperation_refuse_identite_suspendue'`, runner PostgreSQL local, répertoire `.artifacts/e73-review-corrections-01` : **2 réussites, 14 désélections**. Une course changement d’organisation/révocation de session a également été corrigée et revérifiée sur PostgreSQL : la session révoquée reste inutilisable, même après écriture d’une ancienne projection. Les interfaces portail et ERP ont été relues séparément de leurs auteurs.

Le PostgreSQL utilisé est un cluster créé pour cette tâche sur boucle locale, avec deux bases jetables distinctes. Le runner désactive la configuration opérateur et les effets externes. Ces preuves ne concernent aucune base partagée.

Contrôles finaux backend, préfixe commun `.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`, suffixe commun `-q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp <répertoire indiqué> --tb=short` :

| Fichiers / répertoire temporaire | Résultat |
| --- | --- |
| `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/domain/identite_acces/test_equipe_organisation_dedicated.py tests/application/services/test_equipes_animation.py tests/api/test_equipes_animation_api.py tests/security/test_equipes_animation_postgres.py tests/api/test_acces_animation_erp.py tests/security/test_animation_browser_session.py` ; `.artifacts/e73-team-final` | **620 réussites**, avant ajout de la preuve T1 |
| `tests/security/test_equipes_animation_postgres.py tests/application/services/test_equipes_animation.py tests/api/test_equipes_animation_api.py` ; `.artifacts/e73-team-audit-final` | **25 réussites**, après ajout de la preuve T1 |
| `tests/security/test_generation_animation_postgres.py` ; `.artifacts/e73-team-generation-final` | **24 réussites** : tâches non commencées suspendues, reprise contrôlée et régressions de génération |
| `tests/security/test_animation_finance_tenant.py` ; `.artifacts/e73-team-finance-final` | **4 réussites**, zéro skip après raccordement du test à la variable du runner isolé ; le premier essai ignoré faute de variable historique ne constituait pas une preuve |
| `tests/security/test_session_animation_revocation_race.py` ; `.artifacts/e73-session-race-01` (sans `--tb=short`) | **1 réussite**, vraie révocation concurrente et ancienne projection ; preuve durable ajoutée au commit complémentaire `a17e3f4` |

Les suites se recouvrent : leurs nombres ne sont pas additionnés en un total de tests distincts. Les contrôles frontend des 15 appels compte/équipe contre l’OpenAPI passent dans `tests/organisation-http-contracts.test.mjs` (3 tests). Le scénario `tests/browser/animation-lots.mjs` couvre lecteur avec/sans Achat à 320/1 280 px. Le scénario `tests/browser/generation-preparation.mjs` couvre la suspension explicite sans polling ni reprise automatique (70 contrôles à 390/1 280 px). Les 4 hunks préexistants « Clôturer » d’App.tsx restent exclus du commit ; types et build isolé ont aussi réussi sur une copie de l’index Git dans `tmp/e73-lot1-staged`, indépendante de ces modifications.

Conservation : classification T1/T8 et dates sources documentées dans l’architecture ; audit minimal des changements d’habilitation implémenté. Le raccordement des purges et la preuve de leur reprise après restauration restent une obligation du lot 10 avant mise en service. Les recettes humaines Localeo puis Martignas-sur-Jalle et tout contrôle hébergé restent non exécutés. Aucun push ni déploiement.

### Lot 02 — Périmètres commerçants

Le domaine Référencement porte la décision produit, distincte du statut général du commerce. Les migrations locales préparées sont `v262_e73_perimetres_commercants.sql` et `v263_autorisations_dediees_internes.sql`. Les commandes ERP imposent version, motif et idempotence ; le rôle Backoffice ne suffit pas sans autorisation dédiée. Le générateur prépare des racines `A_REVOIR`, sans suggérer ni activer automatiquement les produits des commerces existants. Son registre classe les décisions, preuves d’engagement et reçus avec le jeu métier.

OnBoard utilise une preuve de convention explicitement rattachée à chaque produit et un support Animation seule. Les onglets financiers et prestations suivent l’applicabilité projetée par le serveur. L’ERP distingue revue individuelle et bascule communale ; son historique se charge sur demande, par pages SQL de 25. Les anciennes mutations ORM directes SQLAdmin Commerçant/Prestation sont fermées au profit des parcours transactionnels ERP, avec liens explicites.

Premières preuves exécutées par l’intégration (ne constituent pas encore la validation finale du lot) :

| Contrôle | Commande / résultat |
| --- | --- |
| ERP/OnBoard mobile et bureau | `node tests/browser/epic73-perimetres.cjs` : réussi à 320/1 280 px, revue sans présélection, consultation seule, rattachement de convention sur dossier clos, conflit avec saisie conservée, historique paginé et confirmation de bascule communale |
| Régressions OnBoard | `node tests/browser/onboard-administration.cjs` : 7 scénarios réussis ; `node tests/browser/epic69-onboard.cjs` : Lecteur/Backoffice, scopes, actualisation de droits et purge de session réussis |
| Autorisation dédiée ERP | `node tests/browser/epic69-acces-internes.cjs` : réussi à 390/1 280 px ; l’autorisation n’est jamais attribuée implicitement par le changement de rôle |
| Générateur/registre | Runner isolé, `tests/unit/test_demonstration_registry.py tests/integration/test_demo_perimetres_commercants.py`, base locale jetable, `.artifacts/e73-demo-scopes-01` : **10 réussites** |
| Pagination et index historique | Runner isolé, `tests/security/test_historique_perimetres_postgres.py -q -s`, base locale jetable, `.artifacts/e73-history-perf-01` : **1 réussite**, 10 000 décisions dont 6 000 concentrées sur un commerce ; deux pages distinctes, 26 lignes SQL maximum, absence de chargement des snapshots et d’OFFSET ; `EXPLAIN ANALYZE BUFFERS` utilise `ix_historique_perimetres_commerce_date` (0,076 et 0,093 ms ponctuels) |
| Administration et adresses | `.artifacts/e73-admin-boundary-01` : 24 réussites, 1 échec de double de session incomplet dans le test de modification d’adresse ERP ; correction du double confiée au propriétaire, résultat de reprise à enregistrer |
| Sources documentaires | `sync_documentation.py --check-sources` via Python isolé : 123 documents vérifiés |

La revue a identifié puis fait corriger les frontières suivantes : continuité pendant une redemande, lecture ERP sans grant de gestion, Stripe depuis une URL directe, filtrage SQL des historiques/notifications avant pagination et compléments sur dossier clos. Les corrections sont intégrées et vérifiées par les preuves ci-dessous. La recette humaine et la bascule pilote ne sont pas exécutées.

Vérifications complémentaires de l’intégration :

- `tests/infrastructure/admin/test_perimetres_mutations_erp.py tests/application/conformite_fiscale_bum/test_adresse_onboard_erp.py`, runner isolé et `.artifacts/e73-admin-boundary-02` : **24 réussites** ; le double ERP incomplet est corrigé sans changer les assertions.
- `tests/integration/test_data015_migrations.py`, base locale exclusive `localeo_audit_migrations_test`, `.artifacts/e73-migrations-lot02` : **3 réussites**, migrations complètes et rejeu jusqu’à v263. L’indexation supplémentaire de pagination est vérifiée séparément après stabilisation.
- `node tests/browser/epic73-perimetres.cjs` rejoué après ajout du complément : réussi à 320/1 280 px ; dossier clos sans complément en lecture, complément Coffrets avec seuls champs autorisés modifiables, statut `CLOTURE` conservé.
- Contrats Animation, `node --test tests/organisation-http-contracts.test.mjs tests/generation-http-contracts.test.mjs tests/publication-http-contracts.test.mjs` : **8 réussites** sur l’export intermédiaire de 756 routes.
- `check_guidance.py` : **94 guides, 1 000 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources` : **123 documents vérifiés**.

Dette backend reproduite indépendamment sur le commit antérieur au lot `a17e3f4`, extrait dans un répertoire temporaire sans configuration opérateur : `test_missions_medias_t3.py`, `test_modification_animation_en_cours.py`, `test_tirage_tous_lots_animation.py` sous `tests/application/animation_locale`, runner isolé, `.artifacts/e73-lot02-baseline-failures` : **9 échecs et 2 réussites**. Les deux premiers échecs sont des doubles sans `configurations_animation`, trois concernent l’ancien parcours de modification après publication remplacé par la commande versionnée, quatre des doubles sans `coordinations_animation`. Les mêmes neuf échecs sont observés dans la passe large du lot ; aucun skip ni affaiblissement d’assertion. Ces scénarios doivent être repris dans les lots qui modifient effectivement les parcours Animation/tirage.

Pro est enregistré localement dans `bc9d1ac` ; le contrat Animation synchronisé dans `7cab528` conserve tous les travaux utilisateur préexistants hors index. Preuves Pro : suite unitaire intermédiaire **487 réussites**, ciblés finance/reset **24**, pagination finale **11**, contrats OpenAPI finaux **46** ; recette navigateur **28/28** puis **16/16** avec curseur à 320/1 280 px ; build isolé réussi. Les suites se recouvrent et ne constituent pas un total à additionner. La recette complète a donné **106 réussites et 7 échecs**, tous reproduits sur le HEAD antérieur `19f7a20` (`business-ux`/`merchant-contract`) ; une dernière suite unitaire complète interrompue après ralentissement n’est pas comptée comme verte. Son timeout de récupération de mot de passe passe ensuite dans la reprise ciblée sans modification de l’assertion.

La portée de ce lot couvre CA15–19 et CA26 pour les produits existants, ainsi que les branches Coffrets/passages des CA20–22. Les bons numériques et leur continuité restent à compléter au lot 05 ; les vues transverses et la restauration complète des CA25/27 restent au lot 10. Aucun de ces critères partagés n’est déclaré acquis dans son intégralité sur la seule preuve du lot 02.

Preuves backend complémentaires, préfixe commun `.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`, suffixe `-q --basetemp <répertoire> --tb=short` ; les scénarios PostgreSQL ajoutent explicitement l’URL locale jetable déjà documentée :

| Contrôle / fichiers | Résultat |
| --- | --- |
| Architecture, application Animation et périmètres ; `.artifacts/e73-perimetres-final-01` | **702 réussites**, dont architecture ; 6 doubles nouveaux et 3 erreurs de fixture corrigés puis repris ci-dessous, 9 échecs préexistants reproduits sur référence |
| `tests/security/test_perimetres_validations_postgres.py`, régressions application catalogue chasse, financement lots, avertissement lots/participants, suivi préparation, supports commerce chasse, paiements individuels/lots et scénario commission ERP ; `.artifacts/e73-perimetres-final-02` | **80 réussites** après correction des doubles, dont vrais QR/PIN PostgreSQL et refus sous suspension |
| `tests/api/test_perimetres_commercants_api.py tests/domain/referencement/test_perimetres_commercant.py tests/application/use_cases/test_initialiser_paiement.py tests/application/use_cases/test_stripe_connect_onboarding.py` ; `.artifacts/e73-perimetres-last-01` | **42 réussites**, dont transport HTTP assemblé avec refus métier 403 et refus avant fournisseur |
| Domaine et PG périmètres après alignement du conflit sur `CONFLIT_VERSION` ; `.artifacts/e73-conflict-contract-01` | **21 réussites** |
| OnBoard, droits et finance ; `.artifacts/e73-onboard-finance-final-01`, puis compléments `.artifacts/e73-complement-01` | Respectivement **678** puis **210 réussites** ; suites partiellement communes, avant finitions de pagination |
| `tests/security/test_facturation_continuite_postgres.py tests/security/test_onboarding_produits_postgres.py`, avec API de dépôt et tests curseur/complément/détail groupé ; `.artifacts/e73-final-finance-context-01` | **7 scénarios PG réussis**, 32 tests réussis au total, un double E50 obsolète corrigé et repris dans la ligne suivante |
| `tests/application/conformite_fiscale_bum/test_service_preparation_onboarding.py tests/application/conformite_fiscale_bum/test_curseur_factures.py tests/api/test_facturation_continuite_upload.py tests/security/test_grouped_invoice_detail.py` ; `.artifacts/e73-final-finance-context-02` | **26 réussites** : complément, curseur lié au contexte, refus de lecture directe et droits avant stockage |
| `tests/api/test_facturation_continuite_upload.py` ; `.artifacts/e73-final-chorus-01` | **11 réussites**, y compris les trois routes Chorus marchandes |
| Migrations complètes jusqu’à `v264_pagination_factures_commercant.sql`, même test DATA015 ; `.artifacts/e73-migrations-lot02-final` | **3 réussites**, aucune base partagée |
| Domaine périmètres, Stripe Connect, paiements individuels/lots et validations PostgreSQL ; `.artifacts/e73-perimetres-final-boundaries-01` | **65 réussites** après séparation des lectures historiques et des validations résiduelles ; appels fournisseur hors verrou métier |
| Attestations moteur PostgreSQL et salariés E72 ; `.artifacts/e73-perimetres-recus-final-01`, puis reçu après retrait sans engagement `.artifacts/e73-perimetres-recu-clos-final` | **11 réussites**, puis **1 réussite** supplémentaire pour la lecture historique d’une animation close |

Les deux listes de factures marchandes conservent leur tableau JSON et annoncent la page suivante dans `X-Next-Cursor` (exposé au navigateur), avec `limit=25`, maximum 100. Le curseur est lié au commerce, à la famille, au tri et à la version. Les actions sont calculées en lectures groupées, sans cache de droits persistant. Sur 10 000 demandes simples et 10 000 groupées : 9/10 requêtes constantes pour 2 ou 51 racines lues ; plans réels indexés sans forçage, mesures ponctuelles 0,229/0,565 ms. Les anciennes listes acheteur/Animation conservent leur contrat et leur dette de pagination, sans nouveau calcul marchand par ligne ; cette dette doit être traitée dans les lots finance/parcours concernés. Ces mesures ne démontrent pas les dix utilisateurs simultanés ni la charge mêlée du lot 10.
