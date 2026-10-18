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
| 05 | US05–10 ; complément numérique US07–08 | Backend, Animation, Commerçant, Marketplace/Live, Projet | Parcours implémentés et vérifiés localement ; commits et limites de conservation/performance ci-dessous ; aucune mise en service |
| 06 | US19–20 ; import/deltas/reprise | Backend, Animation, Projet | Implémenté et vérifié localement ; Backend `bb4e1e8`, Animation `955fb94`, sources dans le commit documentaire du lot 06 ; preuves et limites ci-dessous |
| 07 | US18,30 ; chasse et préparation accompagnée | Backend, Animation, Projet | Implémenté et vérifié localement ; Backend `44c6429`, Animation `8979893`, Projet `7f80a6c` ; recette humaine et hébergement non exécutés |
| 08 | US21–22 ; communication participants | Backend, Animation, Marketplace/Live, Projet | Implémenté et vérifié localement : campagnes, préférences Live, quotas, fréquence et alertes internes ; consolidation conservation/restauration au lot 10 |
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

### Lot 05 — Bons numériques (en cours)

Le lot 04 documentaire est enregistré dans `87badb3`. Avant le lot numérique,
`tests/api/test_pin_validation_e70.py` passe **14 tests** (4,40 s, trois
dépréciations), runner isolé `tmp/e73-lot05-pin-baseline-01`.

Le protocole de préparation privée/scellement est étendu aux bons numériques
dans [tirage-libre-protocole.md](tirage-libre-protocole.md). `BonLot` possède la
validité, la consommation unique, la rotation, la révocation et la correction.
Les canaux QR/PIN partagent ce cœur ; le service de tirage conserve la politique
de population et remplacement. L'ordre de verrou a été précisé en faveur de
l'ordre E70 existant (demande avant cible), sans changer les règles produit.
Les preuves exécutées ci-dessous complètent ce protocole ; la finalisation du
flux d’historique et du cycle complet de démonstration reste en cours.

Périmètre réalisé : CA30 (modèles/version/exemplaires), CA31 (affectation et
libération explicite), branche numérique CA32/33 (tirage, attribution, email et
bon), CA34/35 (QR et PIN), CA36 (cycle et incidents). Les compléments CA15/19–22
réutilisent les périmètres courants et les acteurs principal/salarié, avec
continuité limitée au bon attribué. Cela ne clôt pas US24/36–38 ni l’epic entière.

Le bon appartient à `animation_locale`. Les capacités de consultation, la
signature QR et le rendu email sont des adaptateurs ; le PIN E70 orchestre la
même transition de remise. Une consommation active unique subsiste sous deux
scans salariés ou QR/PIN concurrents. Une correction conserve la preuve initiale
et n’autorise pas le rejeu d’une ancienne demande à consommer de nouveau.
Les gardes du commerce précèdent les verrous de demande/cible ; la suspension
et la révocation personnelle restent prioritaires sur toute continuité.

La migration `v272` crée onze tables numériques, les références et contraintes
d’exclusivité ainsi que les index. L’origine de lien existante est réutilisée.
Les clés QR et flags de workers sont documentés sans secret dans le modèle de
configuration et la [procédure des bons numériques](../../exploitation/exploitation/gerer-bons-numeriques-animation.md).
Les trois branches de dotation restent explicites et exclusives.

### Preuves locales du lot 05

Toutes les commandes Python ci-dessous utilisent
`.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`
depuis le backend, avec `--basetemp` neuf. Les tests SQL utilisent exclusivement
`127.0.0.1:55473/localeo_audit_test` ou la base de migrations jetable dédiée.
Les suites se recouvrent : leurs nombres ne sont pas un total de tests distincts.

| Contrôle | Résultat réel |
| --- | --- |
| Architecture, recensement domaine et use cases | `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py`, `tmp/e73-lot05-architecture-final-02` : **519 réussites** (10,02 s) |
| Inventaire, BonLot, ports, crypto et choix de dotation | 28 réussites initiales ; après correction des métadonnées des huit types dédiés, **21 réussites** domaine/registre/crypto, sans exclusion de contrôle |
| PG inventaire/remise, conservation numérique et Animation, API inventaire | `test_inventaire_bons_postgres.py`, `test_conservation_bons_numeriques_e73.py`, `test_conservation_postgres_t6.py`, `test_inventaire_bons_lots_e73.py` : **32 réussites** (120,08 s), `tmp/e73-lot05-inventaire-conservation-03` |
| Compléments inventaire et droits | Génération 251 unités en 100/100/51, reprises concurrentes, isolation de reçus, libération de surplus : **3 réussites** (10,48 s) ; lecture Lecteur sans commande, isolation/rejeu : **3 réussites** (9,94 s) |
| Tirage numérique, email, accès personnel et scellement | **51 tests uniques réussis** : suite principale 50/50 (279,66 s), puis 15/15 sur les tirages après ajout du contrôle de budget avant chaque page, dont un nouveau test ; `tmp/e73-lot05-w2-final` et `tmp/e73-lot05-w2-budget-final` |
| PIN numérique | `test_pin_bons_lots_postgres.py` : **9 réussites** (65,03 s), `tmp/e73-lot05-pin-pg-03` : courses QR/PIN principal/salarié, correction/rejeu, rotation, rollback de notification, PIN bloqué mais QR autorisé, retrait et suspension |
| Transport API PIN | `test_pin_bon_lot_e73.py test_pin_validation_e70.py` : **22 réussites** (11,93 s), `tmp/e73-lot05-pin-transport-02` |
| Régression PIN Coffrets/Animation/salariés | Suite initiale : 19 réussites, deux échecs sur le formatage SQL de l’historique ; correction puis reprise des trois cas concernés : **3 réussites** (65,36 s), `tmp/e73-lot05-pin-regressions-02` ; 21 tests distincts finalement validés |
| Migration complète et rejeu | `test_data015_migrations.py` jusqu’à v272 : **3 réussites** (83,40 s), avant l’ajout éventuel des index du flux d’historique ; contrôle final à compléter |
| Animation | **197 tests Node réussis** après copie des contrats ; types, lint et build isolé réussis ; navigateur **38 scénarios/416 assertions** de régression lot 04 et **10 scénarios/100 assertions** numériques à 320/1 280 px |
| Localeo Pro | QR bons et contrats : **60 tests ciblés distincts** validés, build et quatre scénarios navigateur réussis avant passage de l’historique au flux ; complément à enregistrer |
| Live, stockage et discriminants | `node --test tests/security/library-backup.test.cjs tests/security/animation-gain.test.cjs` : **8 réussites** (8,76 s), restauration d’accès propre à chaque bon, aucun QR/consigne/coordonnée privée persisté |
| Live, navigateur | `digital-lot.spec.cjs` : **4 scénarios réussis** en production locale après correction de contraste ; même suite **4 réussites sous React StrictMode** avant retouche de présentation, capacité de fragment préservée ; 320/1 280 px, heure de Paris malgré navigateur New York, états terminaux, réseau indisponible, PIN dont la réponse est perdue |
| Live, analyse et build | ESLint ciblé réussi et Vite isolé réussi ; la limite préexistante du lint global sur le répertoire de travail EPERM reste celle du lot 04 |
| Générateur ciblé | **14 tests PG/registre** (6,57 s), puis **6 tests unitaires** ; deux modèles, cinq exemplaires, trois affectés et deux disponibles, aucun bon/QR/email prématuré ; onze tables classées `replace` |

Le scellement numérique a été mesuré avec 10 000 candidats, 1 000 bons et
120 commerces : **37 requêtes, deux écritures finales, environ 716 Ko de mémoire**,
au plus seize lectures par tranche préparatoire. Les gardes de commerce sont
prises seulement au scellement, par pages de cent ; délai de verrou de trois
secondes et budget de vingt secondes avec rollback/reprise testés. Ce n’est
pas encore la preuve de charge simultanée transverse du lot 10.

Deux revues indépendantes ont contrôlé les branches tirage/bon et PIN/droits.
Elles ont conduit à corriger les reçus inter-organisations, les actions proposées
aux Lecteurs et le calcul UTC des quatre-vingt-dix jours d’historique Animation.
Six tests de frontière échouaient avant correction (changement d’heure,
configuration/date/surcharge). Le flux par curseur est désormais intégré dans
Pro ; ses **19 tests PostgreSQL/API** passent, sans skip (83,67 s), puis les
quatre tests API repassent après contrôle des dates HTTP extrêmes (3,60 s).
L’ancienne route reste compatible avec un offset limité à 10 000.

Le cycle complet de démonstration a révélé **quatre échecs et trois réussites**
sur une clé étrangère modèle/version lors de la génération. Ce défaut a été
reproduit et corrigé ; le cycle final passe **7 tests** en 557,78 s, avec quatre
avertissements SQLAlchemy de réflexion `dialect_options`, sans skip.
Le runner `scripts/validation/run_demo_compatibility_tests.py` a utilisé
uniquement les clusters jetables `127.0.0.1:10407` et `127.0.0.1:55448`, avec
sortie `tmp/e73-lot05-demo-compatibility-20261018-final03` : génération,
dump/installation, échec contrôlé, restauration et reset. Le refus initial
sur une base jetable non vide a été résolu en recréant seulement cette base,
après vérification de son répertoire local et de l’absence de connexions.
Aucun environnement partagé n’a été contacté.

Le besoin nominatif du gain numérique est raccordé à la conservation existante :
remise/révocation ferment ce besoin, correction le réouvre ; un engagement
expiré mais non résolu et les autres gains/gels conservent leur effet propre.
La purge physique bornée des capacités et contextes expirés/révoqués sera
raccordée au dispositif commun au **lot 10, avant ouverture**. Les preuves
humaines, le transport réel et l’hébergement restent non exécutés.

Compléments de finalisation :

- PIN numérique/API E70 et contrats moteur relancés après les corrections :
  `test_pin_bons_lots_postgres.py test_pin_bon_lot_e73.py
  test_pin_validation_e70.py test_contrats_moteur_t1.py`,
  `tmp/e73-lot05-root-pin-final-04` : **51 réussites** (36,18 s), trois
  avertissements de dépréciation, zéro skip.
- Le défaut de clé étrangère est reproduit avec les contraintes réelles dans
  `test_modele_generation_et_unites_meme_uow_respectent_vraies_cles_etrangeres`.
  `sauver_modele()` persiste maintenant la version avant l’opération suivante,
  sans commit intermédiaire ; le test passe (**1 réussite**, 5,20 s). Le
  générateur ne contourne aucune contrainte.
- Après ajout des cinq index du flux Pro dans v272 : migrations/rejeu et
  générateurs OpenAPI, `tmp/e73-lot05-migrations-contrats-final-03` :
  **11 réussites** (54,82 s). E41 expose 828 routes, E42 en expose 55 ; copie
  consommateur Animation/Pro effectuée, quatre contrats Pro réussis.
- Live : le scénario de changement de bon ignore la réponse tardive du précédent
  et masque immédiatement son QR. La suite finale sous React StrictMode passe
  **5 scénarios**, dont 320/1 280 px et les états de remise. Les callbacks du carnet
  sont également liés au bon courant. Le serveur passe **13 tests**, dont le
  fallback SPA du lien personnel avec `no-store`. Les fermetures Playwright
  Windows nécessitent l’arrêt du seul serveur local créé par le test après
  exécution réussie ; aucun service distant ou autre processus n’est arrêté.
- Pro : **67 tests unitaires** puis 27 revalidés après la normalisation d’erreur,
  **11 scénarios navigateur** (six nouveaux/Paris et cinq régressions), build
  isolé et quatre contrats finaux réussis. Les filtres suivent les journées
  Europe/Paris même depuis New York, y compris les transitions de 23/25 heures.

- Pro, relecture d’un résultat incertain : identité du bon et de l’opération
  vérifiées ensemble ; aucun rejeu avec le contexte d’un autre bon. **17 tests
  unitaires et quatre scénarios navigateur** passent après ce durcissement.
- Architecture finale : même commande que ci-dessus,
  `tmp/e73-lot05-architecture-final-03` : **519 réussites** (15,46 s).
- Régression des passages salariés E72 : remplacement du test d’une méthode
  privée supprimée par les lectures SQL avant/à l’échéance, avec contrôle du
  maintien des preuves. Échec reproduit puis fichier entier
  `test_animation_salaries_e72.py` : **4 réussites**, aucun skip (9 s),
  `tmp/e73-lot05-historique-salarie-final`.
- Animation : copie isolée HEAD + seuls fichiers du lot 05 dans
  `tmp/e73-lot05-staged`, sans configuration opérateur ni modifications
  préexistantes « Clôturer » : types, lint, build et **huit tests de contrats**
  réussis ; manifestes d’empreintes conservés dans les artefacts locaux.

### Performance de l’historique et limites à solder au lot 10

Le nouveau flux effectue six requêtes repository constantes, sans `COUNT` ni
`OFFSET`. Les essais avec 30 000 occurrences, une page profonde à 27 000,
des filtres de mode et collisions de date/UUID entre types utilisent les index
avec au plus 26 occurrences par branche pour une page de 25. La rétention
des bons s’appuie sur une borne calendaire indexée exacte de cinq ans,
y compris les années bissextiles. Avec 10 000 bons expirés : aucune occurrence
lue ni jointure, environ 0,52 ms dans la mesure locale.

**Exception transitoire E73-PERF-02/04 à solder au lot 10 avant ouverture :**
la sélection des anciennes validations Coffrets/Animation dépend encore de
l’expiration portée par leurs objets parents. Les plans avec 10 000 occurrences
expirées lisent 10 000 validations et interrogent leurs archives/surcharges
(environ 38 ms Coffrets et 206 ms Animation). La réponse et le nombre de requêtes
sont bornés, mais ce travail SQL augmente avec les archives. Le lot 10 doit
raccorder un filtrage indexable à la politique canonique d’expiration, puis
rejouer ces plans ; ne pas présenter le flux comme une preuve de coût constant
pour tous les historiques. Les plans sont enregistrés dans
`.artifacts/e73-historique-flux-performance.json` et
`.artifacts/e73-historique-flux-expiration.json` du backend.

Commits locaux du lot 05 : backend `1cd9564`, Animation `2eee756`, Pro `63b64bc`,
Marketplace/Live `8e54957` ; sources dans le commit documentaire du lot 05.
Les seules modifications étrangères à ce lot sont
préservées hors index. Aucun push ni déploiement.

### Lot 06 — Import et protection des corrections locales

Périmètre : US19–20 / CA42–45, avec consommation des droits du lot 03.
Le domaine Référencement porte le lot d’import, les résolutions et la
provenance à trois versions. L’application orchestre une transaction par
ligne, avec le référencement et OnBoard ; le portail expose les décisions
et la progression. Le transport reste dans le namespace d’import, distinct
des mutations ERP. La [procédure d’import](../../exploitation/exploitation/importer-commercants-animation.md)
décrit les commandes et contrôles vérifiés localement.

Première preuve d’intégration :
`scripts/validation/test_isolated.py tests/security/test_imports_browser_e73.py
tests/security/test_animation_browser_session.py -q --tb=short
--basetemp tmp/e73-lot06-browser-root-01` : **118 réussites** (14 s), deux
avertissements de dépréciation, aucun skip. Dépôt multipart avec origine,
cookie/CSRF, lecture privée et refus des routes Référencement/ERP étrangères.
Cette preuve de transport ne valide pas encore le traitement métier complet.


Parcours intégrés : source Excel/CSV privée, flux stable, mapping explicite,
aperçu et rapprochement email avec contrôle d’identité, choix champ par champ,
import partiel, commandes idempotentes et reprise des seules lignes restantes.
Les créations passent par Référencement et OnBoard : brouillon à vérifier,
sans compte, invitation, périmètre actif ni participation. Les corrections
SIRET/commune sont décidées dans l’ERP ; un déplacement de commune rend la
fiche opaque à l’ancien import. Une incohérence avec le profil financier
courant bloque les nouveaux usages concernés, sans modifier les documents
émis. Après demande ERP, le mapping est figé pour préserver sa preuve ; un
nouveau dépôt dans le même flux permet de corriger les colonnes.

La migration locale `v273_imports_commercants.sql` crée les sept tables et les
index des flux/plans/provenances/vérifications, et accepte une catégorie
absente uniquement pour une fiche en brouillon. L’ouverture reste désactivée
par défaut (`LOCALEO_IMPORTS_COMMERCANTS_APPLY=false`) ; le catalogue ne propose
pas l’achat d’un parcours fermé. Le middleware borne aussi le corps multipart
avant parsing, indépendamment de Content-Length ; parseur, stockage et SQL
du dépôt s’exécutent hors boucle ASGI.

Revue croisée : correction d’un reçu créé avant la disponibilité effective du
fichier. Le client conserve fichier et clé jusqu’à disponibilité confirmée ;
panne avant/après stockage puis reprise explicite ne crée pas de second lot.
Les contrôles de version, les gels de conservation, la reprise après premier
traitement et les mises à jour de commune ont fait l’objet de cas PostgreSQL.
Les gels sont exclus de la sélection des purges puis revérifiés sous verrou,
pour ne pas bloquer les opérations suivantes. Les sources et instantanés de
travail sont purgés après trente jours ; provenance et audit restent distincts.

Preuves finales disponibles (préfixe backend :
`.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py` ;
les suites se recouvrent, leurs totaux ne s’additionnent pas) :

| Contrôle | Résultat local |
| --- | --- |
| Domaine import, API et rejet ERP/remapping | **38 réussites**, `tmp/e73-lot06-core-final-06.xml` ; dépôt hors boucle ASGI inclus |
| Changement de commune bout en bout | **1 réussite**, `tmp/e73-lot06-core-commune-07.xml` ; adresse atomique et confidentialité après déplacement |
| Référencement/OnBoard, corrections ERP, domaine/API/assets | **23 réussites**, `tmp/e73-lot06-preparation-final-03.log` ; concurrence et correction de commune incluses |
| Raccord fiscal et facture assistée existante | **23 réussites**, `tmp/e73-lot06-fiscal-coherence-01.log` ; snapshots inchangés et usages incohérents refusés |
| Garde-fous architecture, recensement, transport navigateur, limites multipart, parseur adversarial et readiness catalogue | **576 réussites**, `tmp/e73-lot06-architecture-final-03` ; deux avertissements de dépendances, aucun skip |
| Migration depuis la base vide, rejeu et compatibilité modèles | **3 réussites**, `tmp/e73-lot06-migrations-final-04` ; PostgreSQL jetable uniquement |
| Animation, copie HEAD + seuls fichiers du lot 06 | **206 tests Node**, types/lint/build réussis ; **22 scénarios navigateur, 292 assertions**, 320/1 280 px ; pas de configuration opérateur ni des changements préexistants Clôturer dans la copie |
| ERP vérifications d’import | Navigateur réussi à 320/1 280 px : motif, lecture seule, CSRF/idempotence, réponse perdue réconciliée, textes échappés |
| Sources et liens documentaires | **94 guides / 1 001 liens**, zéro erreur/alerte ; **126 sources exportées** vérifiées |

Performance : une prévisualisation de **100 lignes parmi 10 000 commerces**
utilise **trois requêtes groupées**, avec candidats bornés et enrichissement par
clé ; aucun balayage de la table des commerces dans le plan mesuré. Les pages
d’imports de 1 et 100 éléments prennent toutes deux **13 requêtes**, avec pics
mémoire Python d’environ 454 et 664 ko. La page profonde après 9 000 imports
utilise un Index Scan de 26 lignes, sans OFFSET. Ces mesures locales ne valent
pas preuve de capacité hébergée. Artefacts backend :
`.artifacts/e73-import-preparation-performance.json` et
`.artifacts/e73-imports-pagination-performance.json`.

Le chunk import Animation est chargé séparément (40,82 ko). L’avertissement
sur le bundle principal de 934,60 ko reste rattaché au lot 09. Pro et Live ne
consomment aucune nouvelle route d’import et ne reçoivent aucun accès implicite ;
aucune modification fonctionnelle n’y est nécessaire pour ce lot. La recette
humaine Localeo/Martignas-sur-Jalle et les essais d’hébergement restent à faire.

Derniers contrôles : **16 tests PostgreSQL complets du noyau import réussis**
(311,03 s, `tmp/e73-lot06-core-proof.md` dans le backend) ; **10 tests des
exports OpenAPI réussis**, `tmp/e73-lot06-contracts-final` (72,37 s).
Les exports canoniques E41/E42 comportent respectivement 844 et 55 routes ;
E42 conserve ses routes Live et reçoit seulement les schémas communs actualisés.
La copie embarquée Animation est synchronisée. Les fins de lignes et espaces
terminaux SQL sont normalisés sans changement sémantique.

Générateur et restauration complète : **7 tests réussis**, quatre avertissements
SQLAlchemy de réflexion, 855,49 s. Commande exécutée dans le backend :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot06-demo-complete-01`. Deux imports synthétiques passent
par les services, conservent une correction locale puis purgent leurs sources
avant export. Le wrapper transactionnel du générateur restaure ses budgets
SQL après chaque sous-transaction ; les limites runtime restent inchangées.
Les premiers essais incomplets ne servent pas de preuve finale.

Commits locaux du lot 06 : Backend `bb4e1e8`, Animation `955fb94`, sources dans
le commit documentaire du lot 06. Les changements préexistants
Clôturer/Exploitation/README restent hors commit ; les fichiers de préparation
du lot 07 sont exclus du commit backend du lot 06. Aucun push ni déploiement.

### Lot 07 — Chasse et préparation accompagnée

Périmètre : US18/30, CA46/57. La chasse conserve son quota dédié, consommé à
publication et non à la demande, au complément ou à la reprise technique. Le
suivi accompagné distingue complétude, préparation, complément attendu,
préparation prête, reprise et annulation. La cible de cinq jours ouvrés repose
sur un calendrier Localeo explicite et figé ; une attente suspend ce décompte.
Le portail présente cible initiale, estimation révisée et retard séparément.
L’ERP permet le traitement sans dépendre de l’Atelier Coffrets. Les messages de
service passent par l’outbox email ordinaire, indépendamment du futur module
Communication participants.

La validation terrain est une preuve de l’animation, de sa révision et de son
empreinte. Une modification pertinente l’invalide ; un modèle réutilisé ne la
transporte pas à la nouvelle édition. Les sessions et habilitations courantes
sont revérifiées avant les commandes et reçus. Le catalogue commercial et les
anciennes commandes de forfait contenant la chasse consomment la même
disponibilité technique injectée : ouverture explicite et calendrier valide.

Migration locale : `v274_preparation_accompagnee.sql`, suivi/événements/terrain,
projections et index des sélecteurs, opérations et tentatives. Les reprises de
données incohérentes échouent atomiquement avec un diagnostic ; elles ne
créent aucun droit ni service historique fictif. La surveillance des retards
est bornée, simulée par défaut, et indépendante de l’ouverture de nouvelles
demandes. Elle écrit une alerte unique par demande/version d’échéance, sans
modifier la version métier à chaque passage. Ops lit au plus 26 références
et affiche une borne `25+` si nécessaire.

La [procédure de préparation accompagnée](../../exploitation/exploitation/preparer-chasse-accompagnee.md)
décrit les responsabilités, le calendrier et les configurations préparées :
`LOCALEO_PREPARATIONS_ACCOMPAGNEES_APPLY`,
`LOCALEO_PREPARATIONS_ACCOMPAGNEES_ALERTES_APPLY`,
`LOCALEO_CALENDRIER_SERVICE_JSON`. Aucune valeur d’horaire métier ni ouverture
d’environnement n’a été imposée.

Preuves exécutées à ce stade, sans additionner les suites qui se recouvrent :

| Contrôle | Résultat local |
| --- | --- |
| Architecture, recensements, domaine, application et API | **621 réussites**, 31,96 s ; `tmp/e73-lot07-architecture-final18.xml`. La passe précédente avait 15 erreurs de préparation du répertoire Windows global, résolues par le répertoire isolé du dépôt sans changer les assertions |
| Génération E55, suivi accompagné, conservation et pagination PostgreSQL | **53 réussites**, 194,77 s ; `tmp/e73-lot07-pg-final16.xml` |
| Préparation historique et contrôle de publication terrain | **38 réussites**, `tmp/e73-lot07-publication15.xml` |
| Exports OpenAPI documentaires | **10 réussites**, 76,66 s ; `tmp/e73-lot07-contracts-final-01`. E41 : 876 chemins ; E42 : 55. E41 embarqué Animation identique au canonique après normalisation des fins de ligne |
| Calendrier, surveillance, disponibilité catalogue et régression tableau Ops | **29 réussites**, `tmp/e73-lot07-root-final-02` |
| Disponibilité injectée dans les commandes de forfait et régressions souscriptions | **43 réussites**, quatre avertissements de dépréciation ; `tmp/e73-lot07-readiness-regression-01` |
| Migration complète depuis une base vide, rejeu et modèles | **3 réussites**, 78,46 s ; `tmp/e73-lot07-migrations-final-03` |
| Reprise de projections historiques et rollback sur incohérence | **2 réussites**, `tmp/e73-lot07-reprise-01` |
| Surveillance concurrente et lecture Ops avec historique volumineux | **2 réussites**, `tmp/e73-lot07-surveillance-pg-03` |
| Sélecteurs PostgreSQL | **3 réussites** ; 26 plans sur 10 000 lieux, 10 000 modèles et 10 000 commerces ; deux requêtes par page, aucun balayage séquentiel des catalogues |
| Portail Animation, copie HEAD + seuls fichiers du lot | **212 tests Node**, types/lint/build réussis ; suivi **18 scénarios/234 assertions**, génération **74**, préparation chasse **258**, mobile/bureau et affichage Paris |
| ERP préparation et génération | Recettes navigateur 320/1 280 px et 390/1 280 px réussies ; action accessible sans Atelier Coffrets |
| Sonde du générateur synthétique | **1 réussite**, 85,09 s ; vérification globale du jeu, droits client/lecteur, complément réel et absence de débit de publication |

Les performances des opérations ont été éprouvées avec 10 000 opérations du
tenant, 10 000 opérations antérieures d’autres tenants et 10 000 tentatives :
pages 1/100 en deux requêtes, sans plan forcé et sans chargement des gros
résultats. Le détail borne ses tentatives à 25 et fournit la suite paginée.
La surveillance a également été mesurée avec 10 000 archives, 10 000 demandes
en attente et 201 actives, sur les index partiels de file et d’Ops. Artefacts :
`.artifacts/e73-preparation-pagination-performance.json`,
`.artifacts/e73-selecteurs-performance.json` et
`.artifacts/e73-preparations-alertes-performance.json`.

Revue croisée : corrections des contrats de curseur, de la revalidation de
session, du lien d’email vers la route réelle du portail et de deux dépendances
vers l’infrastructure. Les reprises automatiques E55 ne sont pas bloquées dès
la première erreur transitoire ; leurs dates historiques sans fuseau sont
écrites et comparées en UTC. Les sources du générateur préservent l’ordre
global des verrous et emploient une période annuelle cohérente avec les droits.

La revue indépendante des raccords de surveillance et de disponibilité n’a
relevé aucun défaut bloquant (`tmp/e73-lot07-revue-root-w2.md` dans le backend).
Les contrôles documentaires passent : **94 guides / 1 003 liens**, aucune erreur
ni alerte, et **127 sources exportées**. Le premier contrôle d’export a détecté
un identifiant de bundle utilisant le chemin source ; il a été corrigé vers
le namespace documentaire `docs/ops`, sans déplacer la source canonique.

Générateur et restauration : la suite complète a réussi **7 scénarios sur 8**
(360,05 s, quatre avertissements de réflexion SQLAlchemy,
`tmp/e73-lot07-demo-complete-02`). Le huitième a identifié un contrôle de fixture
qui comptait les versions de configuration comme des animations distinctes.
La correction vérifie toutes les versions, dix animations avec chacune un
visuel cohérent et dix visuels distincts. Elle conserve les contrôles stricts
de neutralisation des emails et emploie de vraies sessions synthétiques pour
les lectures produit désormais protégées. Ce seul scénario a été rejoué avec
succès : **1 réussite**, 56,50 s, un avertissement de réflexion,
`tmp/e73-lot07-demo-relations-reprise-01.log`. Les sept scénarios non modifiés,
dont export/restauration, n’ont pas été rejoués inutilement. Aucun échec n’est
masqué. Une ligne vide finale de v274 a été supprimée au contrôle Git, sans
modifier son SQL ; aucune base partagée n’a été touchée.

Commits locaux du lot 07 : Backend `44c6429`, Animation `8979893`, sources dans
le commit documentaire du lot 07. Aucun push ni déploiement.
Pro et Marketplace ne consomment pas ces nouvelles routes. Les deux sélecteurs
historiques exhaustifs restant dans App et le bundle principal Animation sont
suivis aux lots 09/10. La conservation physique des nouvelles familles reste
à prouver au lot 10. Recette humaine et hébergement : non exécutés.

### Lot 08 — Communication participants

Périmètre : US21–22, CA47–49. Le portail propose préparation, aperçu,
programmation, confirmation, rapport et reprise d'une campagne. Les quatre
groupes restent limités à une animation. L'état de traitement, le dépôt Live
et le résultat Push sont distincts. Les dates sont affichées en Europe/Paris.
Les formulaires préservent les propositions et réconcilient une réponse perdue
par reçu avant toute répétition explicite de la même commande.

Le domaine possède les transitions et décisions de fenêtre, préférence,
sollicitation et audience. L'application capture puis prépare une audience
durable par lots, débite un crédit au premier dépôt Live et reprend sans
modifier audience ou compteur. Le transport est séparé, avec baux et intentions
durables ; les fournisseurs sont simulés dans toutes les preuves. Une campagne
sans destinataire autorisé ne consomme aucun crédit.

La préférence organisateur est explicite et indépendante du consentement
historique aux notifications. Le message est disponible sans installation Push,
puis peut être lu après liaison personnelle vérifiée d'un carnet. Les listes
fusionnent des pages bornées et n'exposent aucun endpoint ou secret. Un retrait
de préférence, de droit ou une suspension reste contrôlé côté serveur.

L'ERP permet de consulter le réglage communal et les alertes, puis de les
modifier avec l'autorisation dédiée `animation:sollicitation_gerer`, un motif et
une version. La configuration initiale reste 1 message/24 h et un seuil à 3×.
Les alertes sont regroupées par commune/période, avec un email interne à leur
ouverture ; ni reprise ni clôture ne remettent la fréquence à zéro. Une garde
partagée du réglage empêche sa modification concurrente pendant la décision.

Migration `v275_campagnes_organisateur.sql` : 23 tables dédiées, index de listes,
files et purges, nouvelles dates effectives Animation et permission ERP sans
octroi automatique. Le backfill exige des preuves de publication et de clôture,
dont un gel de population pour cette dernière. L'absence de preuve conserve une
fenêtre à vérifier. La migration n'active aucun module ni worker.

Preuves root déjà exécutées (runner backend isolé ; suites recouvrantes) :

| Contrôle | Résultat local |
| --- | --- |
| ERP PostgreSQL/API/configuration | **24 réussites**, `tmp/e73-lot08-root-pg04.xml` : CAS, concurrence, rollback email/alerte, grant/session révoqués dans la composition réelle, garde tenant contre suspension |
| Disponibilité commerciale et configuration finale | **13 réussites**, `tmp/e73-lot08-readiness02.xml` ; trousseau, emails internes, VAPID et flags des deux workers requis pour les nouveaux usages |
| Exécuteur campagnes | **8 réussites**, `tmp/e73-lot08-execution.xml` ; simulation sans claim/écriture et budget avant le lot suivant |
| Migration vide/rejeu/atomicité/modèles et reprise historique | **4 réussites**, 62,44 s, `tmp/e73-lot08-migrations02.xml` ; PostgreSQL local jetable, schéma final des 23 tables |
| Réponses HTTP Animation | **11 réussites**, `tmp/e73-lot08-responses02.xml` ; deux réponses antérieures complétées dans OpenAPI sans changer leur JSON |
| ERP mobile/bureau | `node tests/browser/epic73-sollicitations.cjs` réussi à 320/1 280 px : 404 du reçu puis renvoi de même clé, attente202, CAS409 avec proposition reprise et confirmation, pagination, lecture seule, texte échappé et Paris |
| Chargement réel du module ERP | **6 réussites**, deux avertissements de dépréciation, `tmp/e73-lot08-assets03.xml` : contrôle HTTP de la page et du module `sollicitations.js` ; ajout de ce fichier à la liste d'assets autorisés, oubli non détectable par la recette navigateur servie sur des fixtures |
| Campagnes : domaine, PostgreSQL, HTTP réel, HMAC et performance | **54 réussites**, 182,49 s, `tmp/e73-lot08-pg12.xml` ; débit concurrent du dernier crédit, rollback du premier dépôt, audience figée et fenêtre après démarrage |
| Participants et synchronisation existants | **8 réussites**, `tmp/e73-lot08-legacy01.xml` |
| Derniers cas campagnes et recensement | **33 réussites**, `tmp/e73-lot08-target14.xml` : 30 tests domaine, recensement complet et roundtrip UTC sous fuseau SQL Europe/Paris ; reprise du cas de fixture signalé dans `final13` |
| Architecture et API antérieures | **586 réussites** dans `tmp/e73-lot08-architecture02.xml` et un échec de déclaration de preuve ; ce dernier est corrigé et rejoué dans `target14`, sans skip ni exclusion |
| Exports documentaires et contrat Live | **10 réussites**, `tmp/e73-lot08-contracts03.xml` ; E41 **896 routes**, E42 **60 routes** |
| Live, préférences, transport, concurrence et purge | Ensemble de **47 tests distincts** validés au fil des suites W2 : 17 PostgreSQL, 11 domaine, 9 API, 9 transport/CLI et 1 performance ; détails dans la note locale backend `tmp/e73-lot08-preuves-w2.md` |
| Animation, seuls fichiers du lot dans une copie du HEAD | **220 tests Node**, types/lint/build réussis ; **36 scénarios navigateur / 684 assertions**, 320/1 280 px et fuseau Los Angeles ; trois contrats campagnes rejoués après l'export définitif |
| Marketplace / Live | **113 tests de sécurité**, lint ciblé réussi, **12 scénarios navigateur** (neuf antérieurs et trois nouveaux) ; les trois nouveaux rejoués avec code natif 0 après un avertissement de l'enveloppe PowerShell |
| Accessibilité Live additionnelle | **1 scénario réussi**, 21,3 s : 320 px et texte agrandi à 200 %, navigation clavier, accord/retrait/lecture/fermeture sans débordement ; le débordement du titre constaté à la première passe a été corrigé, captures inspectées |
| Démonstration et cycle complet sauvegarde/transfert/restauration | **9 réussites**, aucun échec ni skip, 509,77 s, `tmp/e73-lot08-demo-complete02/results.xml` ; scénario Communication avec les deux flags finaux ; six avertissements SQLAlchemy de réflexion. L'exécution précédente interrompue ne constitue pas une preuve |

La page profonde d'alertes parmi **20 000 lignes** (10 000 dans la commune et
10 000 ailleurs) utilise l'index communal et lit 26 lignes pour une page de 25,
sans OFFSET ni balayage de l'autre commune. Une première assertion avait détecté
l'emploi de l'index global ; le curseur inclut désormais la commune dans la
comparaison, sans forcer le plan ni affaiblir le test. Artefact local backend :
`.artifacts/e73-sollicitation-performance.json`.

Campagnes : sur **10 communes et 10 000 participants**, les pages de 1 et 100
éléments utilisent chacune 20 requêtes. Dix lecteurs simultanés ont pris de
0,191 à 1,039 s par lecture sur le poste local ; la capture de 1 000 participants
a pris 0,260 s. Les index sont vérifiés sans forçage du plan. Messagerie :
10 000 messages personnels, 10 000 notifications historiques et 10 000
participants ; deux pages et leurs cent faits exigent cinq requêtes, sans
balayage des grandes tables. Ces mesures ciblées ne démontrent ni le mélange
de parcours du lot 10 ni la capacité de l'hébergement cible.

Le chunk Communication est chargé à la demande (36,32 ko ; gzip 9,91 ko).
L'avertissement sur le bundle principal Animation reste pris en charge au lot
09. Le commit local Animation est `08f4d98` ; il contient seulement les 21
fichiers vérifiés, avec les quatre hunks Clôturer et les autres modifications
utilisateur préexistantes laissés hors index.

Marketplace : commits locaux `0fa79e4`, puis `c16bb30` pour le correctif
320 px/texte à 200 %, sans réécriture d'historique. Son lint global rencontre
un refus d'accès Windows dans le répertoire historique de sortie
`output/demo-generation/pytest-bum-registry` ; le lint des sources et des tests
touchés a réussi, sans ajout d'exclusion pour masquer ce refus.

Backend : commit local `2cda9d6`, 92 fichiers explicitement indexés. La commande
finale `run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot08-demo-complete02` a terminé avec le code 0. La base
de construction jetable a été recréée avant cette exécution après le retrait
d'espaces de fin de ligne dans v275 ; aucune empreinte de migration appliquée
n'a été contournée. Les sources et l'index sont restés figés pendant la preuve.

La revue indépendante a corrigé la fenêtre +30 jours dans les reprises et la
projection du rapport pour ne pas restituer de compteur technique hors contrat.
Les contrôles globaux ont également révélé deux réponses anciennes non décrites
(batch d'exemplaires et demande de mot de passe), désormais modélisées. Les
premiers contrôles de recensement ont signalé des classes sans preuve dédiée ;
leurs résultats ne sont pas présentés comme une suite verte.

La [procédure Communication](../../exploitation/exploitation/communiquer-participants-animation.md)
décrit réglages, préférences, workers, rotations de clés et reprise. Les contenus
des messages suivent la politique Live existante ; le raccord transversal aux
gels/purges et la preuve après restauration des nouvelles familles restent au
lot 10. Les essais utilisateurs Localeo/Martignas et toute capacité hébergée sont
non exécutés. Aucun fournisseur réel ni environnement partagé n'a été utilisé.
