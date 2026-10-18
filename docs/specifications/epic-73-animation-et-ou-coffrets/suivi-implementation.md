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
| 02 | US11–13 ; parties US24/36, périmètres et onboarding | Backend/ERP/OnBoard, Commerçant, Animation, Projet | Implémenté et vérifié localement pour les produits existants ; Backend `261ebdc` et raccord asset `59d89d0`, Pro `bc9d1ac`, Animation `7cab528`, Projet `afd77cd` ; branches numériques et exploitabilité reprises aux lots 05/10 |
| 03 | US03,14–17,27–28 ; souscriptions/modules/finance | Backend, Animation, Pro (contrat), Projet | Implémenté et vérifié localement ; Backend `4f3a3b1`, Animation `79903e3`, Pro `8212252`, Projet `6a3d747` ; activation des modules futurs aux lots 06/07/08 |
| 04 | US01–02,04 ; branche externe US07–08 | Backend, Animation, Marketplace/Live, Pro (contrat), Projet | Implémenté et vérifié localement ; Backend `7502282`, Animation `d0b92f7`, Marketplace `1473e05`, Pro `30aeed3`, sources dans le commit documentaire lot 04 ; branche numérique au lot 05 |
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

Raccord complémentaire : le module `perimetres-commercants.js` était absent de la liste des fichiers servis par le shell ERP. Le commit local `59d89d0` l’ajoute ; `tests/api/test_erp_perimetres_asset.py`, runner isolé, `.artifacts/e73-lot02-asset` : **1 réussite**, chargement HTTP et cache privé vérifiés. Cette preuve complète la recette navigateur qui intercepte les fichiers locaux.

### Lot 03 — Souscriptions et modules (en cours)

L’accès au catalogue est réservé aux administrateurs. Les anciennes écritures directes SQLAdmin d’offre sont fermées au profit de versions explicites. Les autorisations `abonnements:modules_octroyer` (Backoffice) et `abonnements:remboursements_decider` (Finance) sont attribuées séparément ; aucun changement de profil ne les attribue implicitement. La migration `v267_autorisations_modules_internes.sql` étend seulement les codes permis, sans accorder de droit.

Premières preuves, sans validation finale du lot :

- `tests/application/test_autorisations_dediees_internes.py tests/domain/identite_acces/test_acces_interne_dedicated.py`, runner isolé `.artifacts/e73-lot03-grants-02` : **36 réussites**.
- `tests/api/test_offres_animation_erp.py tests/security/test_acces_internes_surfaces.py tests/infrastructure/admin/test_catalogue_versionne_erp.py tests/api/test_erp_perimetres_asset.py`, `.artifacts/e73-lot03-admin-02` : **72 réussites**. La première passe avait 71 réussites et une attente Backoffice obsolète ; E73 restreint désormais cette création aux administrateurs, avec assertion de refus avant SQL.
- `node tests/browser/epic69-acces-internes.cjs` : réussi à 390/1 280 px après extension des autorisations dédiées.
- `node tests/browser/epic73-modules-erp.cjs` : réussi à 320/1 280 px sur réponses synthétiques locales : octroi versionné, dates Paris avec navigateur réglé à New York, conflit et saisie conservée, historique borné, catalogue versionné, décision de remboursement sans retrait implicite.

Les contrôles de droits/quota/paiement, migrations complètes et contrats réels restent en cours. Les trois modules seront proposés à l’achat seulement après réalisation et vérification de leurs parcours dans les lots 06/07/08 ; leur présence au catalogue n’atteste pas leur disponibilité.

Contrôles supplémentaires de l'intégration (lot encore en cours) :

- `tests/integration/test_comptes_internes_postgres.py`, `.artifacts/e73-lot03-grants-pg` : **8 réussites** ; persistance des grants et retrait sur session existante.
- `tests/application/test_souscriptions_regressions.py`, `.artifacts/e73-lot03-e47-regressions-04` : **38 réussites** ; activation commerciale séparée de l'identité, rollback et replay, invitation explicite après habilitation, réinitialisation d'une heure. La fixture a été raccordée aux tables E73 ; un doublon de fonction qui masquait un test a été retiré.
- `tests/integration/test_demo_modules_abonnements.py tests/unit/test_demonstration_registry.py tests/api/test_erp_perimetres_asset.py tests/api/test_modules_dates_contract.py`, `.artifacts/e73-lot03-demo-03`, PostgreSQL local : **12 réussites**. Le premier essai métier a détecté l'absence de reprise des débits dans le générateur ; correction par le service normal, sans validation automatique de la reprise.
- `tests/integration/test_data015_migrations.py`, `.artifacts/e73-lot03-migrations-01`, base exclusive `localeo_audit_migrations_test` : **3 réussites**, migrations complètes jusqu'à v267, rejeu et atomicité.
- `node tests/browser/epic73-modules-erp.cjs` : nouvelle réussite à 320/1 280 px incluant perte de réponse puis reprise avec exactement la même clé/corps, et confirmation motivée des conditions historiques ; formats d'unités alignés sur les vrais DTO.
- Première passe architecture/application intégrée, `.artifacts/e73-lot03-integration-01` : **533 réussites, 3 échecs**. Deux régressions de transition d'expiration après 30 jours sont renvoyées au propriétaire du service ; le troisième échec détecte le nom/format des déclarations de classes de tests dédiées. Correction en cours, aucune assertion supprimée ou affaiblie.

Le contrat hors ligne contient à cette étape **786 routes** ; il est recopié dans
les consommateurs Animation et Pro, sans prétendre à leur livraison. Les
anciennes éditions directes du catalogue ne constituent plus un chemin de mutation.

Recette Animation : **183 tests Node réussis**, types/lint/build isolé réussis,
**484 assertions dans 36 scénarios navigateur** à 320/1 280 px. Le navigateur
réglé à New York vérifie les heures affichées à Paris ; les scénarios couvrent
expiration sans abonnement courant, période future, quota/historique paginés,
premières coordonnées de facturation, perte de réponse et reprise explicite.
Les quatre hunks préexistants « Clôturer » restent intacts et exclus du futur commit.
La revue frontend/producer a détecté puis fait corriger les dates sans fuseau et
le calcul « déjà acheté » dépendant de la première page des droits.

`tests/security/test_commerce_animation_browser.py`, runner isolé
`.artifacts/e73-commerce-browser-real-01` : **4 réussites** avec la vraie pile
cookie/CORS/CSRF et une session révoquée ; refus avant appel métier. Le service
commercial est simulé dans cette preuve de transport, séparée des preuves SQL.

Pro : **42 tests de contrats réussis** avec
`node node_modules/vitest/vitest.mjs run src/lib/api/contracts.test.js src/lib/api/preparation.contract.test.js --config tmp/e73-lot03-vitest.config.mjs --maxWorkers=2`.
La configuration jetable impose `envDir:false` et des valeurs publiques synthétiques.
Le premier lancement avec la configuration Vite habituelle n'est pas retenu
comme preuve d'isolation. Seul le contrat embarqué Pro est modifié dans ce lot.

Contrôles documentaires intermédiaires : `check_guidance.py` **94 guides,
1 000 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources`
**123 sources vérifiées**. Le lot reste en cours : revue des nouveaux octrois
sur conditions historiques, suspension sur plusieurs périodes et raccordement
du Checkout ERP historique à une intention durable, sans appel fournisseur
sous verrou métier.

Après corrections, `.artifacts/e73-lot03-integration-02` réunit architecture,
couverture des classes métier/use cases, régressions E47, démonstration SQL et
contrat des dates : **539 réussites**, deux dépréciations `utcfromtimestamp`
préexistantes dans le parcours Checkout historique. Les échecs d'expiration
de la première passe sont corrigés ; les classes de tests dédiées sont détectées
par le contrôle sans modifier celui-ci. Le test périmètres du lot 02 est renommé
`test_perimetres_commercant_dedicated.py`, avec ses assertions conservées.

Finalisation du lot 03 :

- Migrations complètes et rejeu jusqu'à **v268**, base locale exclusive,
  `.artifacts/e73-lot03-migrations-02` : **3 réussites** (68,13 s).
- Finance, droits assemblés, factures, API et worker : runner isolé PostgreSQL,
  `.artifacts/e73-commerce-final-01` ; fichiers
  `tests/security/test_commerce_droits_integration_postgres.py`,
  `test_checkout_erp_async_postgres.py`, `test_commerce_abonnements_postgres.py`,
  tests domaine commande/devis/prorata/avoirs, traitement commerce, gateway et
  webhooks Stripe : **56 réussites** (38,54 s), trois dépréciations.
  Deux anciens échecs de fixture supposaient un rôle interne ADMIN nommé
  inexistant ; les scénarios corrigés prouvent le refus Finance et suspension,
  sans élargir la permission historique `finance.executer`.
- `node tests/browser/epic73-checkout-erp.cjs` : **réussi à 320/1 280 px**,
  intention durable, attente explicite et lien visible après confirmation.
- `node tests/browser/epic73-modules-erp.cjs` : **réussi à 320/1 280 px** avec
  compteur divergent ; le libellé mobile ajouté par CSS empêchait la recherche
  accessible exacte du test, désormais ciblée sur la cellule Disponible avec
  assertion exacte « Indisponible ». Aucune assertion métier retirée.
- Animation : **502 assertions dans 38 scénarios navigateur**, types/lint/build
  isolé réussis ; `tests/modules-http-contracts.test.mjs` **2 réussites** après
  export final. Les nombres remplacent les comptages intermédiaires recouvrants.

Les lectures de quotas sont vérifiées avec 10 000 droits et 10 000 consommations,
sans recompter le journal. Les listes de commandes/remboursements sont vérifiées
sur 10 000 lignes chacune avec plans PostgreSQL et curseurs. Ces preuves ne
constituent pas encore le test de trafic transverse du lot 10. Les fournisseurs
restent simulés, les modules futurs indisponibles et la recette humaine non exécutée.

Dernière suite core : `test_modules_plateforme_postgres.py`,
`test_modules_plateforme_api.py`, `test_modules_acquis_dedicated.py`,
`test_souscriptions_regressions.py`, `test_verification_droit_plateforme.py`,
runner isolé et PostgreSQL local `.artifacts/e73-core-final-08` : **66 réussites**
(18,86 s), quatre dépréciations. La revue indépendante finale des compteurs et
du Checkout ERP n'a trouvé aucun nouvel écart concret ; c'est une revue de code
et des tests persistés, distincte de leur exécution par les auteurs/intégrateur.

Une copie de l'index Animation dans `tmp/e73-lot03-staged` exclut les quatre
hunks utilisateur : `npm.cmd run typecheck` et le build isolé y réussissent.
Le chunk principal de 863,29 ko conserve la dette de découpage identifiée pour
le lot 09. Les contrôles finaux de documentation donnent **94 guides,
1 000 liens, zéro erreur/avertissement**, **123 sources vérifiées**.

Limites opératoires préparées : un compteur divergent exige le service motivé
de contrôle/reconstruction, sans écran supplémentaire dans ce lot ; un second
paiement concurrent portant sur une période devenue incompatible reste à
rapprocher, sans créditer deux droits. Aucun fournisseur réel, worker distant,
push ni livraison n'a été utilisé. Le lot 03 est enregistré localement ; les
branches de continuité import/chasse/messages seront complétées avec leurs
opérations réelles dans les lots 06 à 08.

### Lot 04 — Animation et lots externes

Le domaine `ConfigurationDotation` possède le choix et son gel ; le domaine
d'attribution libre possède le suivi et les conditions de remplacement. Les
lots externes n'entraînent aucun achat, activation ou reversement Coffrets.
Le [protocole de tirage libre](tirage-libre-protocole.md) décrit la préparation
privée bornée et sa confirmation. Les écrans présentent séparément attribution,
envoi de l'email et déclaration de remise. Les bons numériques restent
indisponibles jusqu'au lot 05.

Premières preuves locales, complétées par les vérifications finales plus bas :

- Backend : `tests/security/test_gains_live_projection_postgres.py` et
  `tests/api/test_localeo_live_animations_inscription.py`, runner isolé,
  PostgreSQL local, `.artifacts/e73-lot04-live-04` : **7 réussites** (6,44 s).
  La projection de catalogue ne lit que les participations des animations de
  la page. Sur 10 000 participations et 10 000 gains, 3 requêtes constantes
  pour 1 ou 25 racines, sous-requêtes limitées et index réel ; mesure ponctuelle
  0,139 ms pour la projection de gain. Aucun gain privé n'est exposé avant
  confirmation, ni à un autre participant. Ce contrôle ne prouve pas le trafic
  simultané du lot 10.
- Générateur : `test_demo_dotations_animation.py` et
  `test_demonstration_registry.py`, runner isolé PostgreSQL,
  `.artifacts/e73-lot04-demo-01` : **10 réussites** (3,23 s). Le premier brouillon
  synthétique utilise deux lignes de lots externes et trois unités ; les
  historiques publiés conservent une dotation Coffrets explicite et gelée par
  le domaine. Le registre classe les neuf tables du lot comme données du jeu
  à remplacer, sans importer les anciens gagnants. La génération transverse
  complète reste à réaliser au lot 10.
- Marketplace : `node --test tests/security/animation-gain.test.cjs
  tests/security/library-backup.test.cjs` : **5 réussites**. Nature inconnue
  refusée, ancien gain Coffret compatible, absence de coordonnées/consignes
  privées dans le carnet IndexedDB et ses exports.
- Marketplace : ESLint ciblé et build Vite en mode isolé réussis. Le lint global
  rencontre un **EPERM de lecture** dans
  `output/demo-generation/pytest-bum-registry` ; aucune suppression de ce
  répertoire de travail ni modification des règles de lint.
- Navigateur Marketplace : contrat public de détail existant et
  `tests/visual/external-animation-gain.spec.cjs`, serveur local isolé :
  **3 scénarios réussis** (19,8 s), dont accès gagnant direct à 320/1 280 px,
  heure de Paris malgré navigateur New York, actualisation au clavier,
  remise déclarée puis attribution remplacée et refus de nature inconnue.
  Le gain précède la progression de jeu et aucun QR de lot Coffret n'est
  fabriqué pour une remise externe.

Les migrations complètes, la revue indépendante, les contrats et les contrôles
du parcours organisateur/tirage ont ensuite été exécutés comme suit.

Preuves de finalisation avant enregistrement :

| Contrôle | Résultat réel / artefact |
| --- | --- |
| Domaine, architecture, contrats moteur, projection Live et générateur ciblé | Runner isolé, `tests/architecture`, recensement domaine/use cases, `test_gains_live_projection_postgres.py`, API Live, dotation de démonstration, registre et `test_contrats_moteur_t1.py` ; `.artifacts/e73-lot04-integration-02` : **545 réussites** (39,61 s) |
| Configuration, publication, génération, jeu, financement et anciens tirages | Suite core sur quinze fichiers, `.artifacts/e73-lot04-core-final-12` : **161 réussites**, deux avertissements de dépendances ; inclut paiement Coffrets tardif à rapprocher sans émission d’instances |
| Conservation d’identité | `tests/security/test_conservation_postgres_t6.py`, `.artifacts/e73-lot04-conservation-02` : **18 réussites** (57,8 s) ; gains ouverts et réserve préservent l’archive, remise puis purge de l’identité sans effacer la preuve |
| Migrations complètes et rejeu | `test_data015_migrations.py`, base locale exclusive, `.artifacts/e73-lot04-migrations-02` : **3 réussites** (42,8 s), jusqu’à v271 incluant index réserve et compteur BIGINT |
| Animation | **191 tests Node**, **416 assertions dans 38 scénarios navigateur** à 320/1 280 px, régression chasse Coffrets **254 contrôles** à 390/1 280 px ; types, lint, build isolé et deux tests de contrats HTTP réussis |
| Marketplace | `npm run test:security` : **112 réussites** ; ESLint ciblé et build isolé réussis ; `external-animation-gain.spec.cjs` : **5 scénarios réussis** (34,8 s), lien email, reprise/expiration, pagination publique et états Live à 320/1 280 px |
| Pro, contrats consommateurs | Quatre fichiers Vitest contrat API/préparation/registre moteur/animations : **63 réussites** (13,71 s, export final) ; aucun parcours de consommation de lot externe ajouté |

Ces suites se recouvrent ; leurs nombres ne forment pas un total de tests distincts.
Les revues croisées ont fait corriger les curseurs malformés (400), l’ordre commun
de lecture/réservation des suppléants et le total BIGINT des unités. Le carnet Live
refuse une version inconnue et préserve les discriminants inconnus après stockage
et réimport ; il ne les requalifie jamais en Coffrets.

Le tirage a été mesuré avec 10 000 candidats et 1 000 lignes de lots : une tranche
de 500 attributions utilise 16 lectures SQL et environ 2,5 Mo de mémoire. Le
scellement externe produit deux écritures, indépendamment de la réserve. Les
plans utilisent les index de population et de classement, sans tri aléatoire ni
chargement intégral. Une dotation de trois milliards d’unités avec un participant
ne matérialise qu’une attribution. Cela ne démontre pas encore la charge
simultanée transverse du lot 10.

Les contrats générés E41/Live et les trois consommateurs moteur sont synchronisés.
Le [guide organisateur](../../produit/formation/animation/guide-animation-preproduction.md)
et la [procédure de tirage](../../exploitation/exploitation/gerer-tirages-libres-animation.md)
décrivent les états et reprises. La liste globale reste nommée **Tirages Coffrets** ;
les lots libres se suivent depuis chaque animation, avant unification au lot 09.
Le traitement effectif reste désactivé par défaut. Les recettes humaines et toute
activation hébergée restent non exécutées.

Dette étayée : `test_modification_animation_en_cours.py` donne **3 échecs et
1 réussite** (3,81 s) sur les sources du HEAD antérieur `4f3a3b16`, dans une copie
isolée. Les 2 032 fichiers app/scripts/tests et la configuration pytest sont
contrôlés contre l’archive Git (`.artifacts/e73-lot04-baseline-proof.json`).
Ces tests attendent encore le PATCH direct de `date_fin` après publication et
deux anciens messages ; le domaine exige désormais la commande versionnée des
paramètres d’exploitation. Le lot 04 ne modifie ni ces tests ni cette règle.

Revue SQL complémentaire : le plan de la deuxième page de suppléants parcourait
10 000 candidats par semi-jointure malgré le `LIMIT` apparent. La sonde scalaire
corrélée, bornée et indexable corrige ce parcours. Le test avec les pages initiale,
suivante et au rang 9 000 vérifie maintenant les requêtes réelles : une ligne
sondée et 26 lignes de page, aucun candidat filtré, tri final de 26 lignes,
32 à 33 buffers. Les temps ponctuels sont de 0,19 à 0,46 ms, sans forcer le
planificateur. Le plan fautif est conservé dans
`.artifacts/e73-tirage-libre-reserve-plans-avant-correction.json`.

La copie de l’index Animation `tmp/e73-lot04-staged` passe types et build isolé,
sans les quatre hunks utilisateur « Clôturer ». Le chunk principal de 907,80 ko
reste à découper au lot 09. Les commits d’interfaces du lot 04 sont locaux :
Animation `d0b92f7`, Marketplace `1473e05`, Pro `30aeed3`.

Après cette correction SQL, la revue indépendante a réexécuté
`test_attribution_lot_libre_dedicated.py`, `test_email_lot_externe.py` et
`test_tirages_libres_postgres.py` : **28 tests distincts réussis**, dont 16
PostgreSQL en 84,13 s (`tmp/e73-lot04-audit-pg-final-03`), deux avertissements
Starlette/AnyIO, aucun skip. Les trois plans de réserve sont conservés dans
`.artifacts/e73-tirage-libre-reserve-plans.json`. Le premier essai interrompu
pendant la récupération du PostgreSQL local ne vaut pas validation ; seuls
les résultats terminés sont retenus.

Compatibilité de démonstration complète :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot04-demo-compatibility-20261018-resume` : **7 réussites**
en 586,51 s, trois modules obligatoires, zéro skip, quatre avertissements de
réflexion SQLAlchemy. Les cycles installation, panne injectée, restauration et
reset utilisent uniquement les deux clusters jetables de cette tâche. XML et
log sont conservés dans le répertoire indiqué et son fichier `.log` voisin.
Les garde-fous du runner passent **31 tests** (0,35 s). Les ports locaux peuvent
être fournis explicitement et doivent être distincts ; le répertoire de sortie
doit être neuf dans `tmp/`, aucun résultat antérieur n’est effacé.

Le commit backend `7502282` clôt le travail applicatif local du lot 04. Les
générations transverses des dix lots, la charge simultanée, les recettes humaines
et les preuves d’hébergement restent à réaliser selon leur lot. Aucun push,
envoi fournisseur ou déploiement n’a eu lieu.
