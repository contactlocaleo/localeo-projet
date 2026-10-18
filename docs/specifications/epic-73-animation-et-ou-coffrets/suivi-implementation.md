# E73 — Suivi de réalisation locale

Début : **18 octobre 2026**. [Spécification](README.md), [backlog](../../roadmap/a-faire/epic-73-animation-et-ou-coffrets-backlog.md), [matrice des 63 critères et preuves](verification-livraison.md). Objectif : les 38 US, dans les dix lots demandés. Les lignes ci-dessous ne valent pas acceptation tant que les preuves correspondantes ne sont pas enregistrées.

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
| 00 | Sources, référence initiale, protocole UX et suivi | Projet ; lecture des quatre applications | Préparation en cours ; commit documentaire initial à enregistrer |
| 01 | US25–26 comptes, équipe, organisation, récupération, transfert | Backend, Animation, Projet | En préparation ; CA50–53 non vérifiés |
| 02 | US11–13 ; parties US24/36, périmètres et onboarding | Backend/ERP/OnBoard, Commerçant, Animation, Projet | À réaliser |
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
