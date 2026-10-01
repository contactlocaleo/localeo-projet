# EPIC 65 — Vérification et livraison

## Bilan d'implémentation V1.4

Le 1er octobre 2026, l'utilisateur a confirmé H01/H02 : achats et commandes
(lots Animation inclus), consultation et liens vers les actions existantes.
Les trois lots sont implémentés localement. L'EPIC est **En cours**, sans clôture,
commit, push ou déploiement réalisé dans cette intervention.

Contexte : backend `ad42635` et projet `92f3d2a`, avec modifications locales.
Les modifications documentaires V1.3 préexistantes sont conservées. Aucun
frontend séparé n'est modifié : l'ERP est servi par le backend.

### Comportements et preuves

| Critères | Implémentation et preuves locales |
| --- | --- |
| CA-01/08 | Routes HTML intégrées, API session ADMIN et middleware après registre persisté. `tests/api/test_epic65_consultations.py` monte le garde global réel sans bootstrap : cookie incomplet, rôle interdit, session expirée/révoquée, panne du registre, refus avant projection, 401 JSON même avec Accept HTML et no-store. |
| CA-02 | `ServiceConsultationAudit`, port dédié et SQL filtré avant pagination. Tests application et adaptateur : plus de 500 événements, égalités/UUID, `%` et `_` littéraux, dates égales, DST 23/25 h, historique contenant secrets/HTML/URL. PostgreSQL : pages au-delà du total et instantané conservé malgré insertion concurrente. |
| CA-03/04 | `ServiceConsultationPaiements`, normalisation et union de paiements partagées avec Vision 360 et sa recherche. SQL réel SQLite/PostgreSQL : 207 paiements et 205 achats enfants, devises, frais inconnus, commandes et succès multiples. Demandes de facture bornées à 20 avec compte total. Faux lien GET du reçu supprimé ; traces seules explicitement distinguées d'un fichier. |
| CA-05/06 | `ServiceConsultationReversements` partagé ERP/console, décisions pures `lecture_suivi.py`. PostgreSQL : fermeture des dossiers, sources explicites multiples, repli historique unique ou incomplet, exigences Stripe dues, compte historique, tentatives bancaires et échec tardif. Les montants du payout restent contextuels. |
| CA-07 | Pagination/compteurs/agrégats en SQL et lectures financières REPEATABLE READ READ ONLY. Banque parcourue par curseur serveur borné et politique pure par flux ; faits de page chargés par lots. Régressions de requêtes par ligne et de faux repli de source couvertes par `test_epic65_projection_bornage.py`. |
| CA-09/10 | Recettes Playwright Audit et Finance à 390/1440/1920 px : navigation, listes/détails/sections, filtres, retour/focus, erreurs, annulation des réponses obsolètes, purge après expiration, aucune mutation. Captures locales inspectées ; API simulées pour ces recettes. Contrats HTTP séparément vérifiés sur PostgreSQL réel. |

Les tests PostgreSQL emploient PostgreSQL 18.3 jetable, lié uniquement à
`127.0.0.1:55465`, base `localeo_audit_test`, avec schémas synthétiques isolés et
supprimés après chaque test. Aucun accès à la démo, à la production ou à Stripe.
Les fichiers de travail/captures restent ignorés sous `localeo-backend/tmp/`.

### Revue indépendante et corrections

- Session/audit : chaîne et occultation relues ; borne `date.min` corrigée en
  erreur 422, sélection des métadonnées supprimée de la requête de liste.
- Reversements : la première version faisait 16 puis 184 requêtes pour 1 puis
  25 commerces, et 15 puis 303 pour les reversements. La revue a imposé la lecture
  par lots et les curseurs bornés avant acceptation ; les tests reproduisent
  ces défauts puis contrôlent leur correction.
- Provenance : un candidat de paiement mal rattaché ne peut plus être éliminé
  avant de compter les tentatives et fabriquer un repli unique. Les références
  explicites restent conservées sans choisir le dernier paiement d'un achat.
- Couverture : des montants contradictoires pour le même flux ne produisent
  plus une preuve partielle. Les tentatives sont consommées sans stocker toutes
  les associations en mémoire ni additionner plusieurs fois le même flux.
- Paiements : le payeur historique anormal ne doit pas interrompre la liste ;
  les statuts financiers inconnus restent non renseignés avec diagnostic.

### Exécutions et limites

Validation locale du 1er octobre 2026 :

| Contrôle | Résultat |
| --- | --- |
| Suite intégrée : architecture, domaine, application, API, PostgreSQL, sécurité et non-régressions ERP/360 | **760 tests réussis**, aucun ignoré, 159,63 s. 13 avertissements SQLAlchemy sur le cycle de tables `profils_commercants` / `profils_commercants_versions` dans la fixture EPIC 60 inchangée. |
| Dernier passage ciblé Paiements / Vision 360 après revue | **110 tests réussis**, 19,27 s ; recoupe la suite intégrée, ne s'y additionne pas. |
| Compatibilité du générateur : registre et démonstration | **15 tests réussis**, 1,57 s ; aucune génération d'environnement. |
| Recettes navigateur Audit et Finance | Deux scripts réussis à **390, 1440 et 1920 px**, avec captures inspectées. |
| Export OpenAPI hors ligne | **645 chemins** ; 26 ajouts, aucun ancien chemin retiré ou modifié. Parmi les ajouts, 15 concernent E65 et 11 rattrapent des routes déjà présentes dans le backend. |
| Documentation, dernier contrôle standard | **87 guides**, **908 liens locaux** et **118 sources exportées** contrôlés ; aucune erreur ni avertissement documentaire. |

Les tests de bornage constatent un nombre de requêtes constant entre des pages
de 1 et 25 lignes : **13/13** pour les commerces, **15/15** pour la section
reversements et **3/3** pour les virements. Les EXPLAIN ANALYZE Paiements sur
2 000 lignes synthétiques (1 200 sélectionnées) donnent 13,668 ms pour la page
de 25 lignes et 11,98 ms pour la synthèse d'un groupe ; ces mesures locales
ne constituent pas un engagement de performance.

Points d'entrée reproductibles depuis le backend :

```powershell
python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q
python scripts/validation/test_isolated.py tests/infrastructure/persistence/test_epic65_audit_postgres.py tests/infrastructure/persistence/test_suivi_reversements_postgres.py tests/infrastructure/persistence/test_epic65_projection_bornage.py tests/infrastructure/admin/test_epic65_console_parite_postgres.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55465/localeo_audit_test -q
python scripts/validation/test_isolated.py tests/unit/test_demonstration_registry.py tests/unit/test_demonstration.py -q
node tests/browser/epic65-audit-erp.cjs
node tests/browser/epic65-finance-erp.cjs
python scripts/documentation/generate_epic41_openapi.py
```

Les deux premières commandes extraient des sous-ensembles de la suite intégrée
citée ci-dessus ; elles ne représentent pas deux exécutions supplémentaires.
La commande PostgreSQL exige de recréer une instance jetable locale au préalable.
Depuis le dépôt projet : `python scripts/check_guidance.py` puis
`python scripts/sync_documentation.py --check-sources`. `git diff --check`
réussit dans les deux dépôts.

Les scénarios navigateur utilisent des réponses simulées. La recette sur un
environnement déployé et des sessions réelles reste à faire ; voir la
[recette back-office](../../exploitation/recette/recette-backoffice-preproduction.md).
Les EXPLAIN sur jeux synthétiques vérifient les requêtes, sans prouver une
capacité ou un temps de réponse en production. Aucun nouvel index n'est ajouté
sans mesure représentative. La console et l'export historiques parcourent
toutes les pages du périmètre ; ils restent des sorties complètes, distinctes
de la consultation ERP paginée.

### Impacts et livraison

- **Contrats** : OpenAPI canonique exporté hors ligne depuis le code. L'export
  complet reprend aussi des routes Atelier et accès commerçant déjà présentes
  dans le backend mais absentes du précédent instantané ; aucune ancienne route
  n'a été retirée. Aucun contrat embarqué des trois frontends n'est consommateur E65.
- **Données/migrations** : aucune nouvelle table, colonne, transition ou donnée
  obligatoire. Aucun backfill, réécriture de compte Stripe ou rapprochement.
- **Démonstration** : générateur inchangé, les projections lisent les tables
  existantes. Les cas rares sont couverts par les fixtures synthétiques ; aucun
  jeu réel ni accès privé n'est généré ou copié dans la documentation.
- **Fonctionnel/ops** : guides formation/exploitation et recette actualisés.
  CSV 360 : colonnes devise, montants connus/inconnus, couverture et dossier ERP ;
  retrait de l'état bancaire déduit du dernier payout. URL, campagne, export et
  audit d'export historiques conservés ; nouvelles vues sans écriture métier.
- **Reprise** : livrer backend et assets ERP ensemble. Aucun ordre de migration
  ou secret nouveau. Une version applicative précédente retrouve ses vues
  historiques sans restauration de données, puisque la consultation n'en modifie pas.

L'évolution E35 Lecteur/Backoffice reste exclue de cette livraison. Les tests
ADMIN ne valent pas validation de ces futurs profils.

Référence : [parcours](README.md), [architecture et contrats](architecture-contrats.md),
[critères du backlog](../../roadmap/en-cours/epic-65-vues-erp-audit-paiements-reversements-backlog.md).
La matrice initiale V1.3 ci-dessous conserve les preuves prévues. Le
[bilan V1.4](#bilan-dimplementation-v14) distingue les exécutions locales
du 1er octobre 2026, les limites et les opérations d'environnement non réalisées.

## Matrice de traçabilité

Les noms `test_epic65_*` désignent des fichiers à créer dans le backend ; les
tests existants cités ensuite sont à conserver. Cette matrice est le suivi
unique des critères, à enrichir avec commandes, résultats et limites réels.

| Critère | Comportement et propriétaire | Preuves prévues | Documentation / contrat | Démonstration | Exploitation |
| --- | --- | --- | --- | --- | --- |
| E65-CA-01 | Navigation ERP, adaptateur IHM et contrôle d’accès | Tests HTML/URL directe et navigateur des trois listes/détails, absence de redirection SQLAdmin pour consulter ; liens d’actions inchangés | README E65, `erp_ui.py`, guide back-office | ADMIN et EXPLOITATION | Livraison commune assets/API, anciennes URL conservées |
| E65-CA-02 | Projection audit, domaine exploitation | Plus de 500 événements hors filtre devant un événement pertinent ; filtres combinés en SQL, ordre à dates égales, métadonnées et chemins historiques contenant secrets/HTML/URL hostile, acteur absent/unknown/anonymous | Contrat Audit, guide support/audit | Succès/échec/phase inconnue, ressources manquantes | Index et volumétrie, aucun log de corps sensible |
| E65-CA-03 | Projection paiements et politique d’état gestion achats | Tous états bruts/normalisés, dates source, origines, racine achat/commande, deux succès ambigus, frais inconnus/connus et aucun appel Stripe | Contrat Paiements, guide finance | Paiement simple, commande multi-achats, tentatives échouées puis succès | Dépendance aux projections existantes, disponibilité visible |
| E65-CA-04 | Projection de rattachement et domaine documentaire | Achats enfants paginés, trace seule/fichier disponible/absence/lecture indisponible, demande liée ; espion sur générateur pour prouver aucun appel ; aucun faux téléchargement du reçu dans E65 ou la page de traces liée | Contrat section achats, guide finance/documents | Commande avec plusieurs achats et disponibilité documentaire différente | Droits des liens documentaires vérifiés séparément |
| E65-CA-05 | Domaine reversement et port de lecture commun | ERP/360 sur même jeu ; mouvements sans reversement, dossiers fermés hors fenêtre, état annulé, requirements_due non vide, référence manquante ; aucun double comptage | Politique de pipeline, contrat périmètre, guide finance | À préparer, en cours, transféré, échec | Corriger les écarts de lecture identifiés sans changer les commandes |
| E65-CA-06 | Payout et associations du domaine | Transfer sans association ; paid/pending/failed, rapprochement inconnu, un payout pour deux reversements, multiples tentatives et échec tardif ; montant inclus distinct du global ; associations A_ENRICHIR/legacy, devise incohérente et rattachements ambigus exclus de preuve complète | DTO virements et guide financier | Couverture bancaire complète/partielle/inconnue | Aucun nouveau Transfer/Payout ni rapprochement en GET |
| E65-CA-07 | Ports SQL et projections cohérentes | Plus de 100 objets, jointures multiples, pages extrêmes, totaux avant pagination, deux devises/devise absente, null vs zéro, lecture cohérente, changement concurrent visible | Enveloppes et sémantique des dates | Plusieurs pages, dates égales, anciennes références | `EXPLAIN` représentatif, migration d’index si justifiée |
| E65-CA-08 | Identité et accès + adaptateurs | ADMIN accepté ; anonyme, session incomplète, EXPLOITATION refusés avant repository ; contrôle HTML/JSON/documents/section directe ; aucune clé batch substituée à session | Matrice ADMIN conservée, OpenAPI futur | Profils locaux synthétiques | Pas d’élargissement implicite des préfixes middleware |
| E65-CA-09 | Orchestration et UI | Échec count/synthèse/section, session expirée, réponse tardive après filtre ou compte ; aucun zéro/état payé fabriqué ; GET répété sans mutation | Contrat d’erreur et guide de reprise | Doubles de ports en erreur, réseau simulé | Corrélation visible, consultation disponible sans Stripe |
| E65-CA-10 | Présentation ERP | Navigateur 1440/1920/390 px, clavier, focus retour, libellés, tableaux longs, chargement et détail replié | Parcours E65 et captures de recette | Libellés longs et références multiples | Validation visuelle des vues finales, pas d’acceptation par build seul |

## Tests à produire et non-régression

### Domaine et orchestration

- Politique partagée des états de paiement : conserver la normalisation de
  Vision 360, sans valeur « succès » par défaut pour un statut inconnu.
- Parité E65 / Vision 360 : une commande avec un paiement réussi direct et un
  second sur son achat enfant conserve les deux paiements et le diagnostic
  `AMBIGUOUS` ; une tentative hors période de liste reste visible dans le dossier.
  Tester la sélection SQL commune, pas uniquement le mapping d’un DTO simulé.
- Classement pur des mouvements, éligibilité Stripe via le commerçant et suivi
  bancaire via le payout. Tester les règles sans ORM ni fournisseur.
- Devises : EUR/eur/espaces réunis dans un même groupe, filtre normalisé,
  absence et format invalide sans repli EUR ; EUR/USD restent distincts. Une
  différence de casse seule ne rend pas le rapprochement bancaire incohérent.
- Nouveaux tests `tests/application/exploitation/test_epic65_audit.py`,
  `tests/application/gestion_achats/test_epic65_paiements.py` et
  `tests/application/gestion_reversement/test_epic65_suivi.py` : orchestration,
  erreurs des ports, rattachements et absence d’effets. Les doubles fournissent
  des faits, sans recopier la politique métier.
- Refus d’accès testé avant toute requête aux données ; pas seulement absence
  de bouton dans la page.
- La preuve d'absence de mutation espionne les ports métier et fournisseurs,
  sans interdire la vérification technique de session. Liste, détail, section
  et actualisation n'appellent ni Stripe, ni un générateur documentaire, ni
  une commande financière, même si une donnée financière manque.

### Adaptateurs et contrats

- Tests PostgreSQL sur **base jetable** : filtrage avant LIMIT, pagination et
  jointures, agrégats par devise, lecture liste/synthèse cohérente, dates UTC
  historiques et journées Paris de 23/25 heures pour Audit/Paiements.
- Campagnes février, année bissextile, fin de mois, première/seconde moitié ;
  filtres inversés/incomplets/excessifs refusés, jamais inversés silencieusement.
- Couples `campaign`/`month` incomplets ou combinés à des dates refusés ; détails
  Audit/Paiement/Reversement refusant les filtres de période, suivi d’un commerce
  conservant ces filtres ; dates nulles triées en dernier et
  achats enfants paginés par date puis UUID, y compris une racine ACHAT isolée.
- Sources des reversements : deux paiements explicitement liés au même achat
  tous deux conservés, un paiement partagé entre mouvements affiché une seule
  fois ; référence absente, références d’achat contradictoires et plusieurs
  tentatives sans lien explicite signalées incomplètes. Une tentative récente
  échouée ne remplace pas un paiement explicitement lié plus ancien. Vérifier
  aussi la console historique après extraction, sans écriture de rapprochement.
- Compte Stripe historique : reversement vers A et compte commerçant courant B,
  payout vers A correctement associé reste cohérent ; payout vers B ne prouve
  pas le flux vers A. Destination historisée manquante ou intention présente
  contradictoire : couverture non attestée. L'absence d'intention seule ne
  disqualifie pas une destination historisée cohérente. Aucune réparation ni
  appel Stripe en GET.
- `tests/api/test_epic65_consultations.py` à créer : schémas fermés, statuts HTTP,
  cache no-store, aucune route de mutation et sérialisation sans données brutes.
- Monter également `AdminSessionMiddleware` et le garde global dans le montage
  isolé : cookie signé mais session persistée absente/expirée/révoquée refusé,
  registre indisponible en 503, projection non appelée. Une API E65 anonyme
  répond 401 JSON même avec `Accept: text/html` ; une page HTML redirige en 303.
  Vérifier `no-store` sur tous les refus et l'ordre des nouvelles routes avant
  les captures génériques du shell. Les tests avec cookie seul ne remplacent
  pas ces scénarios.
- Confronter les requêtes réelles du navigateur au contrat Pydantic exporté ;
  une requête en erreur n’est pas transformée en résultat vide dans l’UI.
- Vérifier les liens documents sur une vraie source de test ; une réponse HTTP
  réussie sur un contrat simulé ne prouve pas la bonne association aux achats.
  Une trace sans route de lecture sûre produit `TRACE_ONLY`, aucun `documentLink` ;
  une erreur produit `UNKNOWN`, jamais `NONE`. La page de traces liée ne propose
  plus le GET reçu invalide ; aucune génération n'est déclenchée pour le remplacer.
  Plus de 20 liens/diagnostics vérifient compteurs avant limite, troncature
  explicite et accès aux détails ; aucun chemin de stockage ne devient un href.
- Audit : jeton dans un segment de `path` ou dans `resourceId`, query/fragment,
  metadata imbriquée et clé inconnue ne sont pas sérialisés. Vérifier le gabarit
  reconnu ou null, les UUID/entiers admis, les booléens refusés comme compteurs,
  `metadataRedacted` distinct de `metadataTruncated` et la recherche par ID d'événement.
- Repli d'une source sans `paiement_id` : achat enfant avec paiement direct de
  commande unique ; puis ajout d'un paiement sur un autre enfant, qui rend le
  repli incomplet. Ne pas éliminer une tentative échouée ou hors période.
- Payout : deux BalanceTransactions différentes (Transfer et compte connecté)
  mais références destination/compte cohérentes sont acceptées ; comptes ou
  destinations contradictoires sont signalés. Deux tentatives du même flux ne
  doublent pas la couverture, quel que soit leur statut bancaire.
- Paramètres répétés/inconnus, page après la dernière et jeu stable à dates
  égales ; insertion entre deux pages et reprise explicite à la première.
  `generatedAt` ne sert pas de jeton d'instantané. Tester les statuts HTML
  séparément des erreurs JSON et le refus de rôle avant recherche d'un UUID.

### Dépendance de recette E35

La matrice ci-dessus valide le socle ADMIN. Pour une livraison combinée avec
`E35-PROFILS-20260928`, compléter E65-CA-01/04/08/09 par les preuves E35-PROF-11 :
lectures financières Lecteur/Backoffice/Admin, audit Admin seul, périmètres
identiques entre listes, synthèses, détails et pièces ; aucun lien vers console
technique pour les profils métier et aucune commande pour Lecteur. Révoquer ou
réduire le profil dans un autre onglet doit produire le refus dès la requête
suivante et effacer les données devenues interdites. Ces tests dépendent de la
politique et des contrats E35 ; ils ne sont ni exécutables ni réputés réussis
sur la seule base des gardes ADMIN actuels.

### Suites existantes à préserver

- `tests/security/test_erp_session_access.py` et
  `tests/integration/test_epic60_erp.py` : sessions, droits et navigation existants.
- `tests/infrastructure/admin/test_reversements_360_finance_runtime.py` :
  finance 360 après extraction, export existant et différences de lecture tracées.
- `tests/infrastructure/admin/test_backoffice_transactional_views_readonly.py`
  et `test_backoffice_audit_snapshots.py` : lecture seule et données d’audit.
- `tests/application/use_cases/test_vision_360_achats.py` : normalisation, racines,
  frais inconnus et droits techniques.
- `tests/application/services/test_audit_animation_query.py` : filtrage avant
  pagination sans modifier la projection spécialisée Animation.
- `tests/api/test_reversements_api.py`, tests payouts et use cases reversements :
  conserver le comportement des API finance, commandes et suivis commerçants.

Commandes à exécuter lors de l’implémentation, depuis le backend, avec le runner
isolé documenté ; ne pas importer l’application avec les secrets de l’opérateur :

```console
python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q
python scripts/validation/test_isolated.py tests/security/test_erp_session_access.py tests/integration/test_epic60_erp.py tests/infrastructure/admin/test_reversements_360_finance_runtime.py tests/application/use_cases/test_vision_360_achats.py -q
```

Ajouter les nouveaux fichiers de domaine/application/API et les tests PostgreSQL
appropriés une fois créés. Un skip pour base indisponible reste **non exécuté**,
jamais preuve de pagination ou de cohérence financière. Le navigateur utilise
une configuration isolée et des comptes synthétiques ; pas l’environnement réel
ni des opérations Stripe pour vérifier une consultation.

## Données de démonstration

L’EPIC ne crée pas de nouvelle donnée obligatoire : aucun changement de schéma
fonctionnel n’est prévu. Le générateur de l’EPIC 63 et son registre de tables sont
donc des lecteurs/producteurs à **vérifier**, pas à modifier automatiquement.

Scénarios minimaux : deux commerces, plusieurs périodes et devises, mouvement
non affecté, reversement constitué avec éléments hors période, tentative échouée
puis succès, paiement aux frais inconnus, commande multi-achats, pièce manquante,
payout groupé et couverture bancaire partielle, audit historique non assaini.
Les états bancaires rares sont représentés dans des fixtures de test, sans
envoyer de fonds. Examiner les jeux existants avant d’ajouter des profils ou
événements au générateur ; s’il est modifié, appliquer le workflow démonstration
et vérifier installation/restauration sur cibles jetables. Aucun accès réel ou
fichier de profils privé n’est copié dans la documentation.

## Documentation et exploitation à actualiser à la livraison

La présente spécification est la référence de conception. À l’implémentation :

- mettre à jour le [guide de formation back-office](../../produit/formation/backend/guide-backoffice-localeo.md)
  et le [guide d’exploitation back-office](../../exploitation/exploitation/reference-guide-backoffice.md)
  avec les nouvelles destinations, sens des dates et distinction Transfer/virement ;
- compléter la [recette back-office](../../exploitation/recette/recette-backoffice-preproduction.md)
  avec les scénarios E65, sans les marquer réussis avant exécution ;
- documenter les nouveaux contrats via le générateur OpenAPI backend et vérifier
  ses consommateurs ERP ; conserver le contrat publié actuel tant que le code
  ne porte pas les nouvelles routes ;
- examiner les guides finance de la console 360 pour les corrections explicites
  de lecture, sans modifier les règles Stripe ou réintroduire des paiements manuels.

Déploiement prévu dans un même backend : migration additive d’index éventuelle,
services/API, puis assets ERP compatibles. Aucun déploiement des trois frontends
n’est requis. Si assets et API coexistent temporairement en versions différentes,
une route manquante affiche « Vue indisponible », sans repli sur des données
incomplètes. Les anciens écrans restent accessibles aux ADMIN par leurs URL.
Le retour de version restaure l’ancienne navigation ; aucun état financier ni
audit n’a été transformé par cette livraison. Un éventuel index additionnel peut
rester présent selon sa migration, sans promettre un rollback destructif.

Vérifications sur une cible **explicitement autorisée** : ADMIN et EXPLOITATION,
listes/détails/document existant, totaux et filtres, absence de requête fournisseur,
droits des anciennes actions, liens entrants, pages lentes et erreurs corrélées.
Les volumes de référence doivent être mesurés avant de fixer une durée cible ;
aucun SLA ni date de livraison n’est supposé accepté.

## Résultats de la spécification initiale — 26 septembre

- Lecture des sources et analyse indépendantes des paiements/audit et reversements réalisées.
- Revue indépendante de contrat réalisée puis relue après corrections : dates et
  tris explicites, racines incomplètes, sections inconnues, portée de recherche,
  liste positive de métadonnées et distinction entre statut payout et cohérence
  des associations. Aucun constat bloquant restant sur le périmètre décrit.
- Tests applicatifs, PostgreSQL, navigateur et recette physique : **non exécutés**, car aucune implémentation n’est demandée à cette phase.
- `check_guidance.py --changed --all-markdown` avec les trois documents E65
  explicitement sélectionnés : **12 guides, 244 liens locaux, aucune erreur ni avertissement**.
- `sync_documentation.py --check-sources` : **118 documents vérifiés**.
- `git diff --check` réussi. Ces contrôles documentaires ne prouvent ni le
  comportement de l’API cible ni la couverture des scénarios de recette.
- Hypothèses H01/H02 et volumes d’exploitation : voir le README. Ils ne doivent
  pas être transformés en décisions utilisateur supposées.

## Revue de spécification V1.1 — 27 septembre

- Sources locales confrontées au backend `eec63d2` et au projet `696d487` ; aucune
  vérification d’un environnement déployé.
- Revue indépendante des contrats audit/paiements/droits effectuée. Le cas des
  paiements attachés aux achats enfants est intégré à la lecture commune et aux
  preuves prévues. Les sources de reversements multiples ou ambiguës sont
  explicites ; période du suivi commerce et détails complets restent distincts.
- Périmètre conservateur H01/H02 exploitable pour l’implémentation ; abonnements
  agrégés et nouveaux formulaires financiers restent exclus. Volumes et index
  à mesurer lors de l’implémentation, sans promesse de performance chiffrée.
- Contrôles documentaires : `check_guidance.py` avec les cinq documents modifiés
  explicitement sélectionnés, **90 guides et 924 liens locaux, aucune erreur ni
  avertissement** ; `sync_documentation.py --check-sources`, **118 documents** ;
  `git diff --check` réussi.
- Aucun code applicatif modifié ; tests métier, PostgreSQL et navigateur
  **non exécutés**. L’état produit reste **À faire**.

## Revue de spécification V1.2 — 30 septembre

- Sources locales relues sur backend `3252c72` et projet `484f10d`, puis
  modifications documentaires locales E65. La modification préexistante du
  suivi des environnements de démonstration est hors périmètre et préservée.
- Revue indépendante paiements/reversements et relecture des corrections :
  traces documentaires distinctes des fichiers, candidats sources communs à
  la Vision 360, transactions Stripe plateforme/compte connecté distinguées,
  diagnostics et liens bornés. Constats intégrés au contrat et aux preuves prévues.
- Contrôles de session/droits et sources audit relus ; garde ADMIN conservé,
  dépendance E35 explicite, chemins d'audit avec jetons occultés, pagination
  et statuts HTTP précisés. Les identifiants CA-01 à CA-10 sont conservés.
- Préparation : socle ADMIN exploitable pour H01/H02. L'ouverture E35 attend sa
  politique, ses périmètres/masquages et ses preuves ; agrégation d'abonnements
  et nouveaux formulaires financiers restent hors périmètre sans complément.
  Plans SQL, index et volumes restent à mesurer à l'implémentation.
- Aucun code applicatif ni OpenAPI publié modifié ; aucun test métier,
  PostgreSQL ou navigateur exécuté. Aucun commit, push ou déploiement.
  L'état produit reste **À faire**.
- Contrôles documentaires réussis : `scripts/check_guidance.py`, avec les six
  documents E65/backlog/index/roadmap modifiés explicitement sélectionnés :
  **91 guides, 982 liens locaux, 0 erreur, 0 avertissement** ;
  `scripts/sync_documentation.py --check-sources` : **118 documents vérifiés** ;
  `git diff --check` réussi. L'interpréteur configuré par `localeo.python` a
  été utilisé après constat que `python` n'était pas accessible dans le PATH
  du bac à sable. Ces contrôles ne prouvent pas les comportements cibles.

## Revue de spécification V1.3 — 1er octobre

- Sources examinées : backend `ad42635`, projet `92f3d2a`, sans modification
  applicative. Routes E65 toujours absentes ; navigation Audit/Paiements/
  Reversements vers SQLAdmin confirmée. Les statuts de la roadmap restent
  **À faire**, les identifiants E65-CA-01 à E65-CA-10 sont conservés.
- Session : distinction registre persistant, cookie ERP et garde ADMIN ;
  scénarios de révocation/indisponibilité à tester dans la chaîne complète.
  Refus JSON malgré `Accept: text/html`, cache des refus et ordre des routes
  IHM précisés. Les écritures techniques de session ne sont pas des mutations
  financières et ne sont pas interdites par les assertions de lecture seule.
- Revue indépendante des contrats financiers intégrée : normalisation commune
  EUR/eur pour filtres, comparaisons et agrégats ; compte Stripe historisé du
  reversement, sans remplacement par le compte commerçant courant. Une intention
  absente n'invalide pas seule cette référence ; une contradiction est signalée.
- Lots L01/L02/L03 et dépendances explicités. H01/H02 ont été représentées à
  l'utilisateur sans réponse enregistrée dans cette revue ; elles restent des
  hypothèses. Aucune extension abonnements, commande intégrée ou profil E35
  n'est considérée approuvée implicitement. L01 reste indépendant.
- Contrôles documentaires : `scripts/check_guidance.py`, avec les huit documents
  modifiés sélectionnés, **93 guides, 1 087 liens, 0 erreur, 0 avertissement** ;
  `scripts/sync_documentation.py --check-sources`, **118 documents vérifiés** ;
  `git diff --check` réussi. L'interpréteur Python local a exécuté ces contrôles
  depuis le dépôt documentaire.
- Aucun test métier, PostgreSQL, navigateur, export OpenAPI ni générateur de
  démonstration exécuté pour cette spécification. Aucun commit, push ou déploiement
  effectué dans cette phase. Les tests ajoutés au plan restent à produire lors
  de l'implémentation ; les preuves documentaires ne les remplacent pas.
