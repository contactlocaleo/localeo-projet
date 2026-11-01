# E73 — Vérification, migration et livraison

Version de conception du **17 octobre 2026**, réalisation locale commencée le **18 octobre 2026**. [Dossier](README.md), [architecture](architecture-contrats.md), [critères canoniques](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md). La matrice décrit les preuves attendues ; leur exécution effective et leurs limites sont enregistrées par lot dans le [suivi de réalisation](suivi-implementation.md). Un scénario sans preuve enregistrée reste non exécuté. Un lien vérifié ou une revue documentaire ne valide pas un comportement applicatif.

## 1. Traçabilité des 63 critères

### Règle de clôture actualisée le 1er novembre 2026

La décision utilisateur **E73-DEC-CLOTURE-TESTS**, tracée dans le backlog,
sépare l’acceptation du développement de l’activation opérationnelle.
Les tests fonctionnels, PostgreSQL, contrats, interfaces, migrations et reprise
isolée conditionnent la clôture. Le pilote, les avis humains, la bascule des
domaines et l’exercice sur l’hébergement restent des actions de mise en service,
sans être des conditions de clôture de l’epic. Leur absence n’est pas convertie
en preuve de réussite. Les résultats historiques de recette restent inchangés.

Cette règle s’applique à CA-28/63 et aux extensions ; les contrôles locaux
doivent toujours vérifier les gardes, refus, intégrité et reprises. Les objectifs
hébergés RPO/RTO et le fonctionnement des fournisseurs ne sont pas attestés par
ces tests. Les sections d’exploitation ci-dessous conservent leur portée avant
activation, distincte du verdict de développement.

### Revue technique du 1er novembre 2026

**Clôture technique prononcée le 1er novembre 2026**, selon
E73-DEC-CLOTURE-TESTS : les 63 critères et les extensions sont raccordés aux
preuves exécutées ou explicitement réutilisées ci-dessous. Références examinées :
Projet `79f687b`, Backend `590e38b`, Animation `df71e72`, Marketplace `6c1aaac`,
Pro `6c7489e`. Les modifications de cette revue sont identifiées séparément ;
aucun SHA à venir n’est présenté comme exécuté.

Trois revues ciblées ont suivi les critères jusqu’aux producteurs et consommateurs :
dotations/périmètres, SaaS/équipes/imports/campagnes, Live/Pro et extensions.
Aucun développement métier manquant n’est établi dans ces périmètres. Deux
défauts des tests ont été reproduits puis corrigés :

- `test_catalogue_versionne_erp.py` appelait une vue SQLAdmin avec `None` au
  lieu d’une requête authentifiée. Le montage de l’API par une suite précédente
  rendait ce test dépendant de l’ordre. La correction conserve le vrai garde,
  une session ADMIN synthétique, le refus de l’édition ORM et ajoute trois
  refus avant lecture SQL pour Backoffice, Support et Finance. Le fichier seul
  passait avant correction ; la suite assemblée révélait le défaut.
- `tests/browser/saas-journey.mjs` cherchait les anciens blocs de l’Assistant.
  Il ouvre désormais les contrôles secondaires et vérifiés, conserve le contrôle
  exhaustif des neuf points, ajoute un seul point développé et garde navigation
  clavier, destination, aide et absence de mutation.

La revue indépendante a aussi identifié une lacune de preuve **CA-63** : les
tests existants couvraient séparément le cycle de dump/restauration et la reprise
des suppressions/révocations. Un nouveau test PostgreSQL les enchaîne sur un
état E73 réellement sauvegardé et restauré ; aucune garde métier n’est retirée.

#### Preuves renouvelées

| Dépôt / commande ou rapport | Résultat exécuté | Portée et limites |
| --- | --- | --- |
| Backend, `test_isolated.py`, `tmp/e73-closure-core-final-20261101.xml` | 128 réussites, aucun skip | Domaine dotations/bons/produits, API, ERP catalogue et projection Pro ; première exécution 124 réussites/1 échec de harnais/3 skips PG conservée |
| Backend, `tmp/e73-closure-catalogue-fixed.xml` | 9 réussites | Montage API avant SQLAdmin ; reproduit l’ordre qui échouait |
| Backend, `tmp/e73-closure-saas-20261101.xml` | 213 réussites et 3 skips PostgreSQL | Domaine/API SaaS ; les trois cas modules sont repris dans la passe PostgreSQL ci-dessous, pas déclarés réussis ici |
| Backend, `tmp/e73-closure-saas-support-20261101.xml` | 104 réussites, aucun skip | Support et coûts, domaine/API/transport |
| Backend, `tmp/e73-closure-76609eddaab0/architecture.xml` | 623 réussites, aucun skip | Architecture, classes de domaine et use cases dédiés |
| Backend, `tmp/e73-closure-76609eddaab0/recovery-tools.xml` | 35 réussites, aucun skip | Copie cohérente, remappage de fichiers et anciennes sessions à compteur nul |
| Backend, trois bancs `recette-e73-{public-operations,isolated,registry}.test.mjs` | 106 réussites, aucun skip | Prérequis, preuves, refus de fausse réussite et matrice de recette ; ne valent pas 106 recettes hébergées |
| Backend, `tmp/e73-closure-76609eddaab0/core-pg.xml` | 123 réussites, aucun skip, 517,07 s | Bases et schémas jetables, transactions, concurrence, modules et conservation ; les trois cas modules précédemment ignorés sont exécutés |
| Backend, `tmp/e73-closure-76609eddaab0/import-pg.xml` | 2 réussites, aucun skip, 12,18 s | Compteurs d’import réellement persistés après les changements de leurs producteurs |
| Backend, `run_demo_compatibility_tests.py`, `tmp/e73-closure-76609eddaab0/demo/results.xml` | 10 réussites, aucun skip, 735,13 s | Migrations courantes jusqu’à v285, génération, export/restauration, reset et refus des skips ; sept avertissements de réflexion SQLAlchemy |
| Backend, `test_restauration_saas_dump_postgres.py`, `tmp/e73-ca63-ef52d8c49ceb/result-04.xml` | 1 réussite, aucun skip, 16,30 s | Dump/restauration E73 effectifs, journal externe, refus/reprise/idempotence, ancien lien refusé et nouveau parcours opérationnel ; PostgreSQL local avec SCRAM |
| Animation, `pnpm test` | 295 réussites, aucun skip | Inclut les contrats et destinations du nouvel Assistant |
| Animation, `account-app.mjs` | 126 assertions réussies | Compte et équipe, 1280/320 px |
| Animation, `modules.mjs` | 70 scénarios / 994 assertions réussis | Droits, paiements, reprises, 1280/390/320 px et texte 200 % |
| Animation, `merchant-imports.mjs` | 22 scénarios / 292 assertions réussis | Import, refus, reprise et mobile |
| Animation, `reversibilite-catalogue.mjs` | 12 scénarios / 100 assertions réussis | Export/fermeture et catalogue |
| Animation, `assisted-preparation.mjs` | 18 scénarios / 234 assertions réussis | Préparation accompagnée, attentes, reprise et mobile |
| Animation, `saas-journey.mjs` | 26 scénarios / 295 assertions réussis | Assistant, support, nouvelle édition et mesures, bureau/mobile/texte 200 % |
| Marketplace, cinq fichiers Playwright, `tmp/e73-closure-local-consumers-20261101.log` | 32 scénarios réussis | `live-entry-redirects`, `live-discovery-unique`, `live-public-detail`, `live-flyer-image`, `digital-lot` ; build isolé, API simulées |
| Pro, cinq fichiers Vitest, `tmp/e73-closure-contracts-20261101.log` | 73 réussites | Contrats généraux, préparation, animations, bons et origines publiques |
| Pro, trois contrats de transport contre le canonique E41, `tmp/e73-closure-canonical-contracts-20261101.log` | 44 réussites | Ces tests recouvrent les 73 précédents ; pas d’addition des effectifs |

Backend : Python 3.14.3, lanceurs isolés sans dotenv, bootstrap, ordonnanceur ni
transport externe. PostgreSQL 18 est lancé exclusivement sur trois clusters
locaux neufs sous `tmp/e73-closure-76609eddaab0/`, avec noms de bases jetables
autorisés par les runners. Le premier démarrage de l’outillage temporaire a été
arrêté proprement après attente sur un pipe Windows hérité ; ce n’est pas une
anomalie produit ni une preuve de test. Aucune base TEST partagée n’est utilisée.
Les scripts front emploient des configurations de build/test isolées ; aucun
fournisseur réel n’est contacté. Les captures restent hors Git.

CA-63 utilise un quatrième cluster dédié, arrêté proprement comme les trois
précédents. Le premier passage du nouveau test avait omis la simulation exigée
avant purge réelle : le harnais ajoute cette simulation, sans modifier le garde.
Une tentative pendant un redémarrage incomplet est interrompue, non comptée ;
le rapport `result-04.xml` porte sur la version finale portable avec SCRAM.
La sauvegarde SQL restaure le schéma E73 synthétique et son ancien état, puis
la reprise traite le journal indépendant et les familles de conservation
courantes. Dossier et produits restent cohérents ; l’ancien lien restauré est
refusé, un nouveau lien fonctionne et son rejeu est refusé. Le stockage hébergé,
RPO/RTO et un nouveau parcours QR/PIN après ce dump ne sont pas attestés par
ce test ; les tests QR/PIN restent des preuves séparées de la passe PostgreSQL.

Le job PostgreSQL de `.github/workflows/tests.yml` inclut ce nouveau scénario,
avec clients PostgreSQL 18 et `LOCALEO_TEST_PG_BIN`. Le YAML et la sélection
du test sont vérifiés ; aucune exécution GitHub Actions distante n’est annoncée.

#### Réutilisation des preuves et contrats

Les résultats antérieurs cités dans les raccordements ci-dessous et dans le
[suivi](suivi-implementation.md) sont **réutilisés**, sans annoncer un nouveau
rejeu. La comparaison des producteurs SaaS depuis `7f74166` montre des changements
sur la projection des modules actifs et les compteurs d’import, couverts par
les passes ciblées ; les règles équipes/password, campagnes, préparation
accompagnée, support, valorisation, coûts et réversibilité restent inchangées.
Les suites transactionnelles des lots 01/03/06/07/08/09/10 conservent donc leur
valeur pour ces règles, avec leurs limites initiales. Le cycle de démonstration
est renouvelé car sa dernière preuve consolidée précédait les migrations récentes.

Les rappels Live gardent les preuves domaine/PostgreSQL du 30 octobre : leurs
producteurs restent inchangés depuis `586a51f`. Les 38 scénarios de participations
et les menus Pro vérifiés le 1er novembre sont réutilisés sur leurs sources
inchangées. Les 60 scénarios Assistant, 40 parcours workspace et tests du guide
Chasse consignés juste avant `df71e72` restent applicables ; le nouveau banc
SaaS complète leur intégration.

Le contrat embarqué Pro a été confronté au canonique E41, avec déréférencement
et exécution des transports contre ce canonique. Quatorze différences sont
compatibles avec les opérations consommées : annotation de fichier multipart,
champs Flyer optionnels ignorés par le normaliseur, propriétés/état de gains
ou bilans d’opérations non consommées par Pro. Aucun champ obligatoire de
commande Pro ne change ; aucune édition manuelle de snapshot n’est nécessaire.
Empreintes SHA256 : Pro `dc2ef8ce8417d5da366001eb4b6a997e5b9d53e07212f9b409a7fb3707f5989f`,
canonique `ff15ee2576b51515a83fbf0cff3581c5aebe0b8d71ef54477c67ad3da91a58e2`.

#### Extensions incluses dans la revue

| Critères complémentaires | Code et preuves techniques | Actions d’activation séparées |
| --- | --- | --- |
| LIVE-01 à 12, DOMAINES-01 à 04 | Routage Live, catalogue public, communes, ancien carnet, redirections et contrats d’origines ; 32 navigateurs actuels et preuves de découverte/participations réutilisées | DNS/TLS, même API réelle, routes rechargées sur hébergement, anciens liens et PWA installée |
| UX-PUBLIC-01 à 03 | Géolocalisation, navigation et contexte public repris dans LIVE-UNIQUE ; l’ancienne interface marketplace Animation est remplacée par Live, les parcours Coffrets sont conservés | Autorisation GPS et liens sur les appareils cibles |
| LIVE-UX-01 à 04, HOME-01 à 06, ALERTE-01 à 05 | Priorités bornées, données serveur, refus sans consentement, déduplication/horaires/concurrence PostgreSQL et interface mobile ; preuves des 30 octobre/1er novembre reliées aux sources inchangées | Réception Push sur appareil avec accord volontaire, tâches et fournisseurs configurés |
| OA-01 à 04, CA-16/17/18/19 précisés | Référencement/onboarding par produit, absence de contrat/RDV/Stripe pour Animation seule, menus Pro ; preuves du 1er novembre et contrats Pro renouvelés | Vérifier après livraison les permissions et le commerce de recette explicitement qualifié |
| FLYER-01 à 05 | Backend droits/conflits/PDF/QR et UI du lot Flyer, image publique contrôlée ; nouveaux parcours `live-flyer-image` sans illustration inventée | Vérification du rendu et téléchargement réels après livraison |
| UX-ERP-01 à 03 et guide de publication | Navigation, headers/retours, états et actions, contrôles clavier/mobile/zoom ; preuves ERP et nouvelle recette SaaS | Validation d’usage et accompagnement, sans les annoncer effectués |

Les matrices détaillées restent dans leurs spécifications canoniques. Cette
synthèse les raccorde au bilan de clôture, sans créer un second backlog.

#### Verdicts des critères de base

Les raccordements par lot ci-dessous donnent les fichiers et comportements
détaillés. Cette table distingue les preuves renouvelées des résultats antérieurs
réutilisés ; elle couvre les 63 IDs sans additionner des suites qui se recouvrent.

| Critères | Propriétaire, preuve et résultat observable | Verdict technique au 1er novembre |
| --- | --- | --- |
| CA-01 à 11, 29 | Dotation/attribution dans le domaine Animation ; domaine et API renouvelés, PostgreSQL `test_dotation_animation_postgres.py` et `test_tirages_libres_postgres.py` : choix, gel, candidats, ordre, confirmation/remise/reprise et refus. Parcours Coffrets et navigateurs dotation/gain des lots 02/04/05 réutilisés | Vérifiés |
| CA-12 à 14, 37 à 41, 54 à 55 | Droits/modules et commandes commerciales ; domaine/API actuels, catalogue ERP authentifié, PostgreSQL modules/droits et navigateur modules renouvelés. Paiements/remboursements concurrents et factures du lot 03 réutilisés | Vérifiés |
| CA-15 à 22, 26 | Référencement/identités et engagements ; périmètres, onboarding, RDV Animation, droits courants et PIN historiques rejoués en PostgreSQL. Pro, OnBoard et extension OA du 1er novembre réutilisés ; refus de nouveaux usages après retrait et suspension prioritaire | Vérifiés |
| CA-23 à 24 | Catalogue public et Live ; redirections, découverte, fiche, anciens accès et bons dans les 32 parcours navigateur renouvelés ; reprise du carnet, consentement et stockage des lots 04/05/09 et LIVE réutilisés | Vérifiés dans les tests ; domaines/appareils réels à contrôler à l’activation |
| CA-25 | Projections ERP/Support/Atelier, jamais propriétaires des règles ; tests produits du lot 10 (75 réussites avec réversibilité) réutilisés, architecture et projection Pro renouvelées ; droits territoriaux, distinction des produits, refus fournisseur et CSV de page | Vérifié |
| CA-27 | Générateur, inventaire des tables, migrations et cycle réel de démonstration : 10 tests renouvelés, dont sauvegarde/restauration et reprise après interruption | Vérifié |
| CA-28 | Accès/tenants, contrats producteurs-consommateurs, readiness modules, harnais isolés et documentation de livraison ; suites backend/Animation/Pro renouvelées et contrôles du lot 10 réutilisés | Vérifié selon E73-DEC-CLOTURE-TESTS ; publication et pilote séparés |
| CA-30 à 36 | Inventaire, attribution numérique et consommation ; PostgreSQL inventaire/PIN/tirages/ordre renouvelé : exclusivité, concurrence, refus, remplacement et intégrité. Contrats Pro et parcours bon Live renouvelés ; incidents et email du lot 05 réutilisés | Vérifiés |
| CA-42 à 45 | Import commerçants ; domaine/API, 22 scénarios navigateur et deux tests PostgreSQL des compteurs renouvelés, reprise/concurrence du lot 06 réutilisée | Vérifiés |
| CA-46, 57 | Quota chasse, publication et préparation accompagnée ; concurrence du dernier crédit/readiness du lot 07 réutilisée, 18 scénarios navigateur et domaine/API renouvelés | Vérifiés |
| CA-47 à 49 | Campagnes, audience, consentement, quotas et diffusion ; transactions/concurrence/rollback/transport des lots 08/10 réutilisés, tests SaaS et navigateur communication renouvelés | Vérifiés ; aucune réception fournisseur réelle revendiquée |
| CA-50 à 53 | Identité et organisation ; tests sessions, invitations, transfert et concurrence du lot 01 réutilisés, domaine/API et compte/équipe navigateur renouvelés | Vérifiés |
| CA-56, 58 à 60 | Assistant, support et valorisation ; tests métier/API support renouvelés, PostgreSQL lot 09 réutilisé, guide/Assistant et 26 scénarios SaaS actuels. Une lecture ne publie ni ne consomme de quota | Vérifiés |
| CA-61 à 62 | Coûts, réversibilité et fermeture ; domaine/API coûts renouvelés, 43 tests coûts/lectures et 75 export/fermeture du lot 10 réutilisés, 12 scénarios navigateur renouvelés | Vérifiés |
| CA-63 | Conservation et reprise ; 123 tests PostgreSQL actuels incluent purges/révocations/gardes. Le nouveau `test_restauration_saas_dump_postgres.py` sauvegarde un état E73, détruit/restaure réellement son schéma jetable, rejoue le journal externe et les purges, puis vérifie réouverture et accès | Vérifié selon E73-DEC-CLOTURE-TESTS ; preuve intégrée locale réussie et raccordée à la CI |

Les mesures locales PERF-01/02/04/08 du lot 10 restent des résultats historiques
avec leurs volumes, distributions et budgets consignés dans le suivi. Elles
ne sont ni un nouveau benchmark du HEAD, ni un SLA hébergé. Les limites à vingt
acteurs et des lecteurs historiques restent visibles.

#### Actions de livraison distinctes de la clôture

Cette revue ne change ni contrat HTTP, ni migration, ni variable applicative.
Les prérequis existants restent ceux du [guide de configuration](../../exploitation/technique/configurer-epic-73.md).
Les versions distantes n’ont pas été contrôlées pendant cette revue.

| Composant | Action de mise en service | Valeur attendue / contrôle |
| --- | --- | --- |
| Backend et PostgreSQL | Livrer les producteurs avant Animation, Pro et Live ; appliquer les migrations manquantes dans leur ordre | Schéma courant jusqu’à `v285_catalogue_animation_premium.sql`, incluant v284 Live ; readiness et lecture du catalogue Premium |
| API et workers | Partager base, stockage privé et trousseaux ; programmer les traitements réellement ouverts | Flags commerciaux, tirages, génération, imports, préparation, campagnes, coûts et exports fermés par défaut ; leur activation seule ne démarre pas les jobs |
| Bons, PIN et communication | Provisionner ou conserver les clés serveur, sans rotation destructrice lors de la livraison | `LOCALEO_BON_LOT_QR_KEYS_JSON` / `LOCALEO_BON_LOT_QR_ACTIVE_KID`, trousseau PIN existant, `LOCALEO_COMMUNICATION_IDENTITY_KEYS_JSON` / `LOCALEO_COMMUNICATION_IDENTITY_ACTIVE_KID` ; aucune valeur secrète dans un frontend |
| Reprise et conservation | Configurer journal indépendant, stockage/sauvegardes et garde ; isoler les écrivains durant une restauration | `LOCALEO_SAAS_RESTAURATION_GUARD_ENABLED=true` ; réouverture uniquement après preuve conforme. Mesurer RPO 4 h / RTO 8 h sur l’hébergement avant activation ; ne pas promettre de rollback des données |
| Live / Coffrets / gestion | Configurer domaines, TLS, origines API et routes directes | `animations.localeo.city` sert Live, `gestion-animations.localeo.city` la gestion ; en TEST, préfixe `test-`. Coffrets garde `LOCALEO_PUBLIC_SURFACE=COFFRETS`, Live `ANIMATION` ; conserver les anciennes origines des carnets et leur reprise volontaire |
| Documents et OnBoard | Générer le bundle depuis le prochain commit documentaire et vérifier manifeste/empreintes côté lecteur | La révision locale non commitée n’est pas publiée ; réapprouver le support Animation modifié avant toute communication facultative, sans réémettre les anciennes intentions |
| Recette de mise en service | Vérifier les parcours sur la version livrée, avec comptes et appareils dédiés | Accès public, inscription, reprise, historique, ancien lien, refus de droits et notifications consenties ; avis pilote suivis séparément, sans résultat inventé |

Les rapports privés et captures restent dans les dépôts applicatifs hors Git.
La campagne de recette historique conserve ses **40 scénarios entièrement validés
sur 130** et ses 90 partiels ; les tests techniques ci-dessus ne la réécrivent pas.

#### Lots de commit préparés et contrôles documentaires

| Dépôt | Contenu relu | Message proposé |
| --- | --- | --- |
| `localeo-backend` | Test catalogue ERP authentifié et refus, nouveau test de restauration réelle, raccordement au job PostgreSQL | `test(e73): verify authenticated catalogue and real restore recovery` |
| `localeo-animation` | Banc SaaS adapté au guide Assistant, contrôles exhaustifs et action courante unique | `test(e73): align SaaS journey with guided assistant` |
| `localeo-projet` | Décision utilisateur, matrice et bilan, statut Terminée, déplacement du backlog, index/compteurs/liens et distinction recette/activation | `docs(e73): close epic on verified technical tests` |

Marketplace et Pro sont vérifiés sans modification versionnée. Aucun code
applicatif, contrat API, migration ou générateur n’est modifié par cette revue ;
les contrôles correspondants prouvent la compatibilité avec les sources actuelles.
Les artefacts de recette, secrets et fichier `debug.log` préexistant restent
hors de ces lots. Aucun index Git, commit, push ou déploiement n’est effectué.
Contrôles documentaires finaux : `check_guidance.py` — **94 guides, 1 057 liens,
aucune erreur ni alerte** ; `--changed --all-markdown` — **18 documents,
647 liens, aucune erreur ni alerte** ; `sync_documentation.py --check-sources` —
**132 documents vérifiés**. `git diff --check` passe dans les trois dépôts
modifiés. Le déplacement ne change aucun alias d’export ni contrat de lecteur :
seuls les liens documentaires vers le backlog changent, contrôlés après déplacement.

L'évolution du 22 octobre ajoute une [matrice de cinq critères flyer](flyers-contextualises.md#critères-ajoutés)
E73-CA-FLYER-01 à 05, distincte de la base historique ci-dessous. Ses scénarios
RM-FLYER-01 à 05 et les preuves du suivi couvrent les modes de dotation, nombres,
illustration, droits et concurrence.

Le [plan de recette métier](recette-metier.md) complète cette matrice par 25 fiches
fonctionnelles : objet, accès, prérequis, manipulations et résultats observables.
Il prépare la validation humaine sans remplacer les preuves techniques ci-dessous.

Chaque ligne associe le CA à une preuve observable ; les identifiants `E73-T-*` nomment des scénarios à réaliser, pas des fichiers déjà présents. Les tests de domaine utilisent horloge/faits et ports doubles, les tests transactionnels une base PostgreSQL jetable, les contrats les DTO réels, les parcours navigateur des comptes synthétiques. Les références de documents, fixtures et livraison sont décrites après la matrice.

| Critère | Comportement / propriétaire | Preuve attendue — résultats dans les raccordements et le journal | Contrat / guide | Fixture | Livraison |
| --- | --- | --- | --- | --- | --- |
| E73-CA-01 | Cycle Animation seul, `animation_locale` | E73-T-01 : externe et numérique jusqu’à remise sans commande Coffret | D1 | F1/F2 | L2/L4 |
| E73-CA-02 | Coffrets seul, commercialisation/achats | E73-T-02 : acheter et consommer sans souscription ou onboarding Animation | D1/D3 | F3 | L1/L4 |
| E73-CA-03 | Choix explicite, Animation | E73-T-03 : omissions refusées, trois branches affichées sans présélection | D1 | F1/F2/F4 | L2 |
| E73-CA-04 | Publication libre, Animation | E73-T-04 : blocage commun pertinent ; aucun blocage paiement Coffrets | D1 | F1/F2 | L2 |
| E73-CA-05 | Parcours Coffrets acquis | E73-T-05 : commandes/réservation/envois et gains anciens identiques après migration | D1/D4 | F4/F12 | L1/L2 |
| E73-CA-06 | Ordre de lots, Animation | E73-T-06 : quantités multiples, ordre gelé, surplus en fin sans gagnants inventés | D1 | F1/F2 | L2 |
| E73-CA-07 | Tirage et population figée | E73-T-07 : 0/moins/autant de candidats, un lot par participant, suppléants stables au rejeu | D1 | F1/F2 | L2 |
| E73-CA-08 | Gain et communication | E73-T-08 : confirmation puis outbox email, consignes adaptées, aucun objet financier fictif | D1 | F1/F2 | L2 |
| E73-CA-09 | Reprise email | E73-T-09 : échec/timeout après acceptation, gain unique et statut d’envoi distinct de remise | D1 | F2 | L2/L5 |
| E73-CA-10 | Suivi externe / remplacement | E73-T-10 : contact/remise séparés, autorisations, refus avant 14 jours sans refus explicite, retirage explicite | D1 | F1 | L2 |
| E73-CA-11 | Gel de mode, Animation | E73-T-11 : changement contre engagement/publication en deux transactions ; un état final cohérent | D1 | F2/F4 | L2 |
| E73-CA-12 | Classement et forfait | E73-T-12 : passeport/tombola inclus, chasse distincte, variantes sans supplément | D2 | F5 | L3 |
| E73-CA-13 | Inclusion / droit explicite | E73-T-13 : droit inclus valide sans paiement fictif, consommation du bon quota | D2 | F5 | L3 |
| E73-CA-14 | Version catalogue | E73-T-14 : catalogue modifié par admin seulement, période acquise inchangée, renouvellement à confirmer | D2 | F5/F12 | L3 |
| E73-CA-15 | Périmètres ERP, référencement/identité | E73-T-15 : admin/Backoffice dédié autorisés ; principal/salarié/API non habilités refusés | D3 | F3/F4 | L1 |
| E73-CA-16 | Onboarding Animation | E73-T-16 : ouverture sans pièces Coffrets, prérequis Animation manquants explicités | D3 | F1 | L1 |
| E73-CA-17 | Ajout de périmètre | E73-T-17 : champs communs réutilisés, complément requis, ancien périmètre utilisable | D3 | F4 | L1 |
| E73-CA-18 | Communications OnBoard | E73-T-18 : contrats et séquences par périmètre, confirmation d’envoi conservée | D3 | F1/F4 | L1/L5 |
| E73-CA-19 | Navigation et accès directs Pro | E73-T-19 : trois périmètres, menus, appels API et liens profonds cohérents | D3 | F1/F3/F4 | L1/L4 |
| E73-CA-20 | Commerce Animation dans jeu à coffrets | E73-T-20 : accepter/valider passage sans devenir fournisseur Coffrets | D1/D3 | F4 | L1/L2 |
| E73-CA-21 | Scan/PIN/salarié | E73-T-21 : cible par périmètre, histoire autorisée, aucune élévation salarié | D1/D3 | F2/F3/F4 | L1/L2 |
| E73-CA-22 | Retrait et continuité | E73-T-22 : session ouverte, nouvelle action refusée ; seuls engagements préexistants continuent, suspension prioritaire | D3 | F7 | L1/L4 |
| E73-CA-23 | Site Animation | E73-T-23 : découverte/fiche commerce/inscription/Live sans dépendance Coffrets | D3 | F1/F2 | L4 |
| E73-CA-24 | Anciens liens et origines | E73-T-24 : reprise carnet, mêmes identités, QR/email anciens, accepter/refuser Push sans blocage | D3 | F12 | L4 |
| E73-CA-25 | ERP/Support/CRM/Atelier | E73-T-25 : projections typées, sommes sans lots libres, sélection fournisseur filtrée et refus serveur | D3/D4 | F1/F3/F4 | L1/L4 |
| E73-CA-26 | Migration manuelle périmètres | E73-T-26 : non vérifié bloque sa bascule, contrôle concurrent, pas de suggestion/activation automatique | D4 | F12 | L1 |
| E73-CA-27 | Générateur/restauration | E73-T-27 : génération par services normaux, export/restore et refus identiques aux données créées par UI | D4 | Toutes | L5 |
| E73-CA-28 | Tests de préparation de livraison | E73-T-28 : contrats/consommateurs, accès, isolation et gardes de readiness vérifiés ; versions/configuration/preuves documentées. Pilote séparé à l’activation selon E73-DEC-CLOTURE-TESTS | D4 | F12 | L1–L6 |
| E73-CA-29 | Gestion externe | E73-T-29 : aucun QR ni compte Pro imposé ; non renseigné différent de non remis | D1 | F1 | L2 |
| E73-CA-30 | Modèles/exemplaires | E73-T-30 : quantité exacte, commerçant unique/modèle, snapshots et secrets distincts, création hors commune refusée | D1 | F2 | L2 |
| E73-CA-31 | Affectation exclusive | E73-T-31 : deux animations concurrentes, libération confirmée jamais attribué seulement | D1 | F2 | L2 |
| E73-CA-32 | Attributions et remplaçants | E73-T-32 : concurrence attribution/rejeu/remplacement, ancien bon révoqué et nouvelle validité complète | D1 | F2 | L2 |
| E73-CA-33 | Accès bon et QR | E73-T-33 : durée 1/90/365 et bornes invalides, QR remplacé ancien refusé, renvoi sans nouveau gain | D1 | F2 | L2/L4 |
| E73-CA-34 | Consommation unique | E73-T-34 : course scan/PIN et réponse perdue, une consommation active, acteur PIN = commerce | D1 | F2/F7 | L2 |
| E73-CA-35 | Refus de consommation | E73-T-35 : autre commerce, QR remplacé, PIN bloqué, expiration/révocation/non-attribution, reçu déjà remis | D1 | F2/F7 | L2 |
| E73-CA-36 | Incidents bon | E73-T-36 : prolongations jusqu’au plafond, correction tracée, révocation/remplacement contre scan/PIN | D1 | F2 | L2 |
| E73-CA-37 | Catalogue modules | E73-T-37 : prix/quotas/échéances/permissions visibles, modules officiels et historiques acquis | D2 | F5 | L3 |
| E73-CA-38 | Achat module | E73-T-38 : paiement confirmé/échec/doublon/retour navigateur, droit une fois, prorata et autorisation Achat | D2 | F5 | L3 |
| E73-CA-39 | Cadeau/essai | E73-T-39 : habilitation ERP, motif, durée/quota ajustés, aucune transaction financière fictive | D2 | F5 | L3 |
| E73-CA-40 | Droits cumulés | E73-T-40 : inclus/acheté/offert/essai chevauchants, maximum sans recharge ni suppression du droit acheté | D2 | F5 | L3 |
| E73-CA-41 | Fin commerciale et retrait | E73-T-41 : module/base expiré ou retrait anticipé, opérations engagées bornées, historique conservé | D2/D3 | F7 | L3 |
| E73-CA-42 | Aperçu import | E73-T-42 : XLSX/CSV, mapping, 100/101 lignes, 2 Mo/dépassement, champs obligatoires et conflits email/SIRET | D2 | F6 | L3 |
| E73-CA-43 | Import confirmé | E73-T-43 : lignes valides seulement, droits courant/commune, fiche à vérifier sans accès/invitation, rapport | D2 | F6 | L3 |
| E73-CA-44 | Deltas | E73-T-44 : référence/source/local, cellules vides, email contact ≠ login, changement après aperçu | D2 | F6 | L3 |
| E73-CA-45 | Reprise import | E73-T-45 : crash après ligne réussie, expiration avant/après démarrage, reprise sans doublon ni nouvelle ligne | D2 | F6/F7 | L3 |
| E73-CA-46 | Quota chasse indépendant | E73-T-46 : 5/an, prorata plafond, publication concurrente dernier crédit, E55 prêt/non prêt | D2/D3 | F5/F10 | L3 |
| E73-CA-47 | Module Push et quotas | E73-T-47 : absent/actif/essai, premier mois, reset Paris/DST, dernier crédit concurrent, automatique indépendant | D2 | F8 | L3 |
| E73-CA-48 | Audience/permissions/fréquence | E73-T-48 : quatre groupes, fenêtre +30 jours, Live sans Push, plusieurs appareils/animations, révocation avant démarrage | D2 | F8 | L3/L4 |
| E73-CA-49 | Suivi/reprise Push | E73-T-49 : incertain/partiel, suspension et confirmation, fréquence 3×, alerte regroupée, aucun double dépôt Live | D2 | F8 | L3/L5 |
| E73-CA-50 | Mot de passe oublié | E73-T-50 : connu/inconnu réponse identique, 1 h/usage unique, anciennes sessions révoquées | D3 | F9 | L1 |
| E73-CA-51 | Mot de passe changé | E73-T-51 : identité revérifiée, sessions du seul compte invalidées, reconnexion explicite | D3 | F9 | L1 |
| E73-CA-52 | Organisation et invitations | E73-T-52 : rattachement ERP, 7 jours, renvoi/rejeu, compte existant réutilisé sans droits automatiques | D3 | F9 | L1 |
| E73-CA-53 | Équipe et responsabilité | E73-T-53 : retrait immédiat, tâches, transfert accepté concurrent au départ, récupération assistée | D3 | F9 | L1 |
| E73-CA-54 | Souscription autonome | E73-T-54 : renouvellement avant/après échéance, upgrade/downgrade, arrêt, remboursement concurrent plafonné | D2 | F5 | L3 |
| E73-CA-55 | Facturation | E73-T-55 : permission Achat, nouveaux documents seulement, anciennes pièces identiques, autre tenant refusé | D2 | F5/F9 | L3 |
| E73-CA-56 | Guide première animation | E73-T-56 : trois dotations, prérequis et attentes visibles sans bypass de publication | D3 | F1/F2/F4 | L4 |
| E73-CA-57 | Préparation chasse | E73-T-57 : 5 jours ouvrés, pause complément, alerte retard/relance même demande, validation terrain | D3 | F10 | L4/L5 |
| E73-CA-58 | Aide/support | E73-T-58 : guide/FAQ/échanges, réponse humaine 2 jours ouvrés, notes internes inaccessibles | D3 | F10 | L4 |
| E73-CA-59 | Prochaine édition | E73-T-59 : même commune, nouveau brouillon et sélection, aucune copie participants/gains/accords/QR | D3 | F10 | L4 |
| E73-CA-60 | Mesure de valeur | E73-T-60 : définitions et inconnues, source QR, objectifs gelés, satisfaction 1..5 sans identité affichée | D3 | F10 | L4 |
| E73-CA-61 | Coûts/budgets | E73-T-61 : constaté/estimé/absent, séparation client/interne, seuils 80/100 sans effet commercial | D2 | F11 | L5 |
| E73-CA-62 | Export/fermeture | E73-T-62 : responsable seul, CSV/médias/guide sous 5 jours ouvrés, accès 30 jours, fermeture distincte et continuité | D3 | F11 | L5 |
| E73-CA-63 | Tests de restauration et garde de reprise | E73-T-63 : restauration isolée, intégrité, tâches, suppressions/révocations et refus sans preuve conforme. RPO 4 h/RTO 8 h hébergés à vérifier avant activation selon E73-DEC-CLOTURE-TESTS | D4 | F12 | L6 |

### Lecture de la couverture par user story

Cette table relie les **38 US** aux lots effectivement réalisés et aux **63 CA**
ci-dessus. Elle ne remplace pas les résultats du [journal](suivi-implementation.md)
et ne transforme pas une preuve locale en validation humaine ou hébergée.
Les règles et parcours applicatifs sont distingués des opérations de bascule.

| US | Lots de réalisation | CA concernés | Limite d'acceptation |
| --- | --- | --- | --- |
| 01–02, 04–10 | 04–05, régressions Coffrets et continuité dans 02/10 | 01–11, 29–36 | Trois dotations couvertes par les tests locaux ; fournisseurs réels non sollicités |
| 03, 14–17, 27–28 | 03 puis raccords 06–08/10 | 12–14, 37–41, 54–55 | Catalogue, droits et facturation testés avec paiements/transports isolés |
| 11–13 | 02 puis numérique 05 et historique 10 | 15–22 | Périmètres/OnBoard/Pro testés ; aucune activation réelle de commerce |
| 18, 30 | 07 | 46, 57 | Quota et préparation accompagnée ; validation terrain de l'organisateur requise |
| 19–20 | 06 | 42–45 | Import/deltas/reprise synthétiques ; aucun fichier opérateur chargé dans un environnement |
| 21–22 | 08 puis conservation 10 | 47–49 | Campagnes/Live et refus locaux ; pas de livraison Push réelle |
| 23, 29, 31–33 | 09 | 23–24, 56, 58–60 | Site, assistant, support et résultats locaux ; DNS/origines et parcours hébergés non validés |
| 24 | 02 et 10 | 25 | ERP/Support et sélection Atelier ; E71 demeure une epic distincte, aucune vente automatique depuis une projection |
| 25–26 | 01 puis fermeture/conservation 10 | 50–53 | Identités et habilitations locales ; secrets/envois réels non activés |
| 34 | 10 | 61 | Coûts/alertes internes ; un coût estimé ou une marge indisponible n'est pas présenté comme constaté |
| 35 | 10 | 62 | Export et fermeture locaux ; seules les reprises réellement exécutables sont proposées |
| 36 | 02 et consolidation 10 | 26 | Outils de revue manuelle et refus testés ; saisie des périmètres existants et bascule communale non réalisées |
| 37 | 01–10 | 27 | Générateur et restauration locale ; résultat terminal du runner consigné dans le journal |
| 38 | 10 | 28, 63 | Procédures, contrats et contrôles locaux ; pilote, restauration hébergée RPO/RTO et mise en service **non exécutés** |

**Constat historique avant E73-DEC-CLOTURE-TESTS :** CA-28/63 et les branches
hébergées CA-23/24 empêchaient alors la clôture, même avec les commits locaux.
Le verdict courant figure dans la revue technique du 1er novembre ci-dessus.
Les recettes humaines et opérations hébergées restent à réaliser séparément ;
leur absence ne constitue plus une condition de clôture du développement.

### Raccordement des preuves locales du lot 04

Ces résultats portent sur la branche **Libre / Externe**. Les branches numériques
des critères partagés restent ouvertes jusqu’au lot 05. Les commandes, mesures,
limites et commits sont consignés dans le [suivi de réalisation](suivi-implementation.md).

| Critères | Preuves exécutées et portée |
| --- | --- |
| CA-01, 03, 04, 11 — branche externe | Domaine `test_configuration_dotation_dedicated.py`, PostgreSQL/HTTP `test_dotation_animation_postgres.py`, parcours navigateur Animation `tests/browser/dotation.mjs` : choix explicite, gel, publication sans paiement Coffrets, droits/tenant et reprise |
| CA-05 | Régressions financement/publication/tirage Coffrets et `test_valider_paiement_commande_lots.py` : paiement tardif après passage Libre à rapprocher, sans émission d’instances Coffrets |
| CA-06 à 10, 29 — branche externe | Domaine `test_attribution_lot_libre_dedicated.py`, PostgreSQL/HTTP `test_tirages_libres_postgres.py`, navigateur organisateur et `external-animation-gain.spec.cjs` : ordre, manque de candidats, un lot par participant, confirmation privée, email distinct de remise, réserve/remplacement/retirage, erreur et reçu |
| CA-07, 32 — limites externes | Mêmes tests PostgreSQL : confirmations concurrentes, remplacement contre remise et correction, reprise stable ; aucune preuve de révocation d’un bon numérique annoncée avant lot 05 |
| CA-08, 09 | Live `test_gains_live_projection_postgres.py`, jeu PostgreSQL, stockage réel IndexedDB et lien gagnant dans le navigateur : gain confirmé seulement, accès privé distinct du jeu, absence de faux QR/Coffret et versions inconnues refusées |
| Conservation / CA-27 partiel | `test_conservation_postgres_t6.py`, `test_demo_dotations_animation.py`, registre de démonstration et migrations locales : besoin d’identité externe et réserve, purge après remise, dotation synthétique par le domaine. La démonstration transverse de tous les lots et sa restauration restent au lot 10 |

Les preuves de volume couvrent 10 000 candidats, 1 000 lignes de lots, les index
réels, une préparation bornée et le coût constant du scellement externe. Elles
ne remplacent ni la charge simultanée transverse du lot 10 ni la recette humaine.

### Raccordement des preuves locales du lot 08

Les preuves ci-dessous complètent les règles commerciales du lot 03. Le
[suivi de réalisation](suivi-implementation.md#lot-08--communication-participants)
consigne les commandes exécutées, résultats, mesures et reprises de tests.

| Critères | Preuves exécutées et portée |
| --- | --- |
| CA-47 | Domaine `test_campagnes_organisateur_dedicated.py`, PostgreSQL `test_campagnes_organisateur_postgres.py` : débit unique au premier dépôt, concurrence du dernier crédit, audience sans destinataire autorisé sans débit, ouverture technique indépendante des notifications automatiques |
| CA-48 | Mêmes suites, `test_messages_organisateur_postgres.py` et navigateur Animation/Live : quatre groupes, préférence explicite, fenêtre publication/+30 jours, contrôle courant de session et autorisation, message Live sans installation Push, liaison personnelle vérifiée et retrait |
| CA-49 | `test_diffusion_messages_organisateur.py`, `test_execution_campagnes_organisateur.py`, `test_sollicitation_postgres_e73.py` et navigateur ERP : baux/reprises, absence de double dépôt, suspension et confirmation, réglage 1/24 h et seuil 3×, alerte regroupée et outbox transactionnelle |
| Performance / frontières | Suites `test_campagnes_organisateur_performance.py`, `test_messages_organisateur_performance.py` et cas volumineux de sollicitation : pages SQL bornées, index réels, audience traitée par lots, dix lecteurs locaux ; contrôles d'architecture et de contrat HTTP |

Ces preuves locales ne constituent pas un envoi fournisseur réel, une recette
humaine ni une capacité démontrée de l'hébergement. La purge transversale, les
gels et la réapplication des règles après restauration restent à vérifier au
lot 10 ; aucune durée supplémentaire n'est introduite pour ce lot.

### Raccordement des preuves locales du lot 09 — vérifié localement

| Critères | Preuves et limites |
| --- | --- |
| CA-23/24 | Site public Animation, fiche commerce, source d'inscription, continuité explicite du carnet et satisfaction Live ; navigateur mobile/bureau et texte agrandi. Origines/DNS et recette hébergée non exécutés |
| CA-56 | `test_assistant_animation_api.py` et `test_assistant_quota_postgres.py` : contrôles propriétaires sans publication, synchronisation de statut ni débit lors d'une lecture ; refus de session et de quota |
| CA-58 | `test_demande_organisation_dedicated.py`, `test_support_organisations_postgres.py`, `test_support_organisations_http_postgres.py`, `epic73-support-organisations.cjs` : deux jours ouvrés, notes privées, droits courants, concurrence, rollback, email unique, reçus et saisie préservée |
| CA-59/60 | Domaine Valorisation, `test_valorisation_animation_postgres.py`, API et navigateur : nouvelle édition sans données personnelles copiées, provenance, objectifs, sources, satisfaction et mesures agrégées ; réconciliation explicite hors GET |
| CA-27, partiel | Migration v276 depuis une base vide, rejeu, atomicité et correspondance aux modèles : trois réussites locales. Générateur/registre : 23 réussites ; démonstration complète, reprise après interruption et restauration : dix réussites, 571,16 s, aucune base partagée. La preuve hébergée et la consolidation de conservation restent au lot 10 |

Les résultats finaux, artefacts et corrections de revue sont consignés dans le
[suivi](suivi-implementation.md). Le [guide des parcours et du support](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrit l'exploitation. Le lot 09 est terminé localement ; les critères du lot 10,
la recette humaine et les vérifications hébergées restent non réalisés. Le lot 10
n'est pas commencé, conformément à la consigne du 19 octobre.

### Raccordement des preuves locales du lot 10

Les commandes, résultats finaux et éventuels écarts de ces contrôles sont
consignés dans le [journal de réalisation](suivi-implementation.md). Les tests
ci-dessous s'exécutent sur les sources locales et des bases jetables, sans
transport externe. Leur existence ne remplace pas un résultat d'exécution.

| Couverture | Tests backend et consommateurs | Frontière vérifiée |
| --- | --- | --- |
| CA-25 / US24 | `test_suivi_produits_postgres.py`, `test_suivi_produits_api.py`, `epic73-suivi-produits.cjs` | ERP/Support réels, produits distincts, scope communal, trois dotations, attribution/remise/correction, CSV de page et index |
| CA-61 / US34 | `test_pilotage_economique_dedicated.py`, `test_pilotage_economique_postgres.py`, `test_pilotage_economique_http_postgres.py`, `test_pilotage_economique_performance.py`, `epic73-pilotage-economique.cjs` | Mesures constatées/estimées/absentes, corrections, budgets, alertes, droits internes et absence d'effet commercial |
| CA-62 / US35 | `test_reversibilite_organisation_dedicated.py`, `test_reversibilite_organisations_postgres.py`, `test_reversibilite_organisations_api.py`, `epic73-reversibilite.cjs` ; Animation `reversibilite-catalogue.mjs` | Export privé et médias, capture/reprise, révocation du responsable, engagements, fermeture et reprise réellement disponible |
| US37 / conservation | `test_conservation_saas_postgres.py`, `test_conservation_audit_saas_postgres.py`, `test_conservation_saas_live_postgres.py`, `test_conservation_saas_cli.py`, `test_conservation_saas_structure.py` | Dates sourcées, gels, dépendances, copies SQL/JSONL/Live, reçus expirés, minimisation et reprise |
| CA-63 / US38, partie locale | Tests de reprise dans `test_conservation_saas_postgres.py` et runner de compatibilité démonstration | Journal indépendant, droits et secrets restaurés, purge avant réouverture, refus HTTP/readiness ; **ne prouve pas RPO/RTO hébergés** |
| PERF-01/02/04/08, partie locale | `test_lectures_globales_animation_postgres.py`, `test_compteurs_lectures_v283.py`, `test_historique_cibles_v280.py`, `test_e73_charge_mixte_locale.py` ; Animation `global-read.mjs` | Pages et compteurs, fraîcheur, scopes, rollback, suppression, croissance et concurrence mesurées |
| Contrats et raccordement | `test_erp_animation_equipe_shell.py`, `test_saas_exploitation_batch.py`, tests OpenAPI ; Animation `lot10-http-contracts.test.mjs` | Modules JS réellement servis, tâches inactives par défaut, commandes/reçus/pages conformes au producteur |

Les suites de chaque lot se recouvrent : leurs nombres ne doivent pas être
additionnés pour annoncer un nombre de tests distincts. Les limites de charge
du banc et les dettes historiques restent explicitement séparées des preuves.
L'ouverture du pilote et la recette humaine Localeo puis Martignas-sur-Jalle,
ainsi que l'exercice sur l'hébergement, restent des étapes futures.

### Documents et guides associés

- **D1** : [dotation et lots](dotation-lots.md) ; actualiser à l’implémentation les parcours organisateur, les supports de gain, l’aide scanner Pro, E70 et les projections Live. Contrats gagnants discriminés et consommation.
- **D2** : [modules, souscriptions, import et communication](modules-souscriptions-import-communication.md) ; guides catalogue/finance ERP, espace « Mes modules », modèles CSV/XLSX, rapports, aide communication et alertes Ops. Contrats commerciaux, imports et campagnes.
- **D3** : [périmètres et parcours SaaS](perimetres-parcours-saas.md) ; guides OnBoard/contrats commerçants, rôles et aide partenaire, support, site Animation, réversibilité. Contrats identités/périmètres/projections et anciennes URL.
- **D4** : [architecture et contrats](architecture-contrats.md), présent plan et [recette générale](../../exploitation/recette/cahier-recette-generale-avant-mep.md) ; registre de conservation et procédures incident, migrations, démonstration, manifeste de livraison.

Ces références identifient les mises à jour futures des documents d’usage. Les guides aujourd’hui utilisés en exploitation ne sont pas réécrits comme si E73 était livrée.

## 2. Données de démonstration et preuves de non-régression

| Fixture | Cas à générer / vérifier |
| --- | --- |
| F1 | Animation seule, dotation externe, plusieurs modèles/quantités, responsable de remise sans compte Pro ; lot non renseigné/remis/refusé et aucun candidat |
| F2 | Animation seule, bons numériques : plusieurs exemplaires, disponible/affecté/attribué/consommé/expiré/révoqué/remplacé, commerce et salarié, gain en échec email |
| F3 | Commerce et client Coffrets seuls ; achat, prestation et règlement existants sans droits Animation |
| F4 | Commerce mixte, jeu à coffrets avec participant commerçant Animation seul ; onboarding complémentaire incomplet |
| F5 | Deux organisations et communes, droits inclus/achetés/offerts/essai/expirés avec chevauchements, conditions catalogue ancienne/nouvelle, factures et remboursements simulés |
| F6 | XLSX/CSV 100 lignes, 101 lignes refusées, fichier trop grand, conflit email partagé/SIRET, cellules vides, correction locale, crash/reprise et delta de version |
| F7 | Périmètre retiré avec bons attribués, jeu publié et prestations vendues ; module expiré ; salarié révoqué et commerce suspendu pour vérifier la priorité des refus |
| F8 | Participants communs à deux animations d’une commune, deux appareils, accord messages sans Push, suivi commune seul exclu, campagnes suspendues/en cours/incertaines |
| F9 | Un compte organisateur dans deux organisations, responsable/gestionnaire/lecteur et permissions distinctes ; invitation remplacée et transfert en attente |
| F10 | Préparation chasse complète/en attente client/en retard/prête, support interne/externe, nouvelle édition, objectifs et données manquantes, avis facultatif |
| F11 | Budget absent/80 %/100 %, coûts estimés/constatés, export prêt/expiré, fermeture avec engagement ouvert puis transfert documenté |
| F12 | Données historiques avec périmètre à revoir manuellement, ancien lien/QR, archives/suppressions/révocations, outbox et paiement en résultat incertain au moment d’une sauvegarde |

Le générateur reste dans le backend : [instructions locales](../../../../localeo-backend/scripts/demonstration/AGENTS.md), [générateur](../../../../localeo-backend/scripts/demonstration/generator.py), [registre des tables](../../../../localeo-backend/scripts/demonstration/table_registry.json), [schéma](../../../../localeo-backend/scripts/demonstration/schema.py), [archive](../../../../localeo-backend/scripts/demonstration/archive.py). Mettre à jour création, découverte des dépendances, inventaire, export des accès et restauration ensemble. Ajouter les nouvelles tables au registre avec leurs relations/ordre ; un schéma inconnu doit être signalé plutôt qu’omis de l’archive.

Le code actuel capture un schéma et ses migrations puis vérifie des empreintes de tables/lignes/séquences à la restauration ; conserver ces contrôles et couvrir aussi objets, QR/invitations et effets externes E73. Les profils synthétiques ne doivent pas contenir de comptes réels ; artefacts, accès, secrets et fichiers d’import restent dans le répertoire privé opérateur, pas dans ce dépôt documentaire. Aucun mode démo, contournement de droit ou donnée fictive financière dans `app/` pour faciliter le scénario.

Régressions obligatoires : E46 achat lots, E47 souscriptions, E55 moteur/publication/gel, E56 participation, E68 onboarding et confirmation des communications, E70 PIN/coffrets/passages/conservation, E72 salariés/scan/historique. Étendre les tests pertinents existants au lieu de prétendre que leur ancien succès couvre les nouveaux types. Les jobs PostgreSQL doivent réellement s’exécuter : un skip ne prouve ni contrainte d’unicité ni ordre de verrouillage.

## 3. Lots de réalisation et dépendances

Les neuf regroupements du backlog restent dans l’epic ; les jalons L1 à L6 ci-dessous organisent les dépendances techniques, sans promettre une livraison partielle du pivot complet.

| Jalon | Contenu | Conditions de passage |
| --- | --- | --- |
| L1 — Accès et données de base | Identité/appartenance, périmètres/prérequis, revue manuelle, filtres métier ERP/Pro/Atelier, lecture typée | Migration additive prouvée, isolation et droits contrôlés dès la requête suivante ; accès historiques conservés |
| L2 — Dotation et remise | Choix de mode, modèles/stock, gains libres, QR/PIN, incidents, Live/email | Tous les lecteurs savent distinguer les cibles ; concurrence et régressions Coffrets démontrées |
| L3 — Droits commerciaux | Conditions figées/catalogue, commandes et modules, quotas, import, chasse, campagnes | Permissions L1, souscription et paiements réconciliés ; aucun achat proposé pour une capacité non disponible |
| L4 — Parcours SaaS et site | Équipe/portail, facturation, assistant, accompagnement, support, réemploi/bilans, origine Animation | Modules utiles prêts, contrats et liens anciens vérifiés ; DNS/TLS/SW/cookies testés sur la cible |
| L5 — Exploitabilité | Exports/fermeture, conservation, coûts, alertes, documentation et générateur | Classes de conservation mappées, rapports exploitables, démonstration restaurable, transport simulé dans les tests |
| L6 — Pilote et reprise | Sauvegarde/restauration, recette réelle pilote, extension progressive | Preuves de CA-28/63, responsable de bascule identifié ; aucun commerce non vérifié basculé |

La chasse reste dépendante de la readiness E55, indépendamment du module payé ; refuser ou différer l’achat si le service ne peut pas être fourni, expliquer le diagnostic et utiliser une réconciliation support pour une commande déjà confirmée. Cette spécification ne clôture pas E55, E68, E70 ou E72.

## 4. Séquence de migration et d’ouverture

1. Épingler les SHAs des cinq dépôts, l’empreinte des contrats et l’état des travaux locaux. Préparer le pilote **Martignas-sur-Jalle**, choisi le 18 octobre, après validation interne Localeo ; désigner le responsable technique et le responsable de vérification métier, inventorier les engagements et sources de sauvegarde.
2. Sur copie jetable, tester les migrations additives avec [l’outil standard](../../../../localeo-backend/scripts/database/apply_migrations.py) ; aucune modification d’un SQL déjà appliqué. Vérifier interruption/reprise et checksums. La [procédure schéma](../../exploitation/technique/deployer-et-verifier-schema.md) demeure l’entrée opératoire.
3. Préparer les instantanés commerciaux et appartenances à partir des faits, signaler ambiguïtés ; faire saisir les périmètres commerce manuellement dans l’ERP. Pas de proposition automatique. Capturer les engagements autorisés à continuer sans élargir les rôles.
4. Déployer backend compatible en lecture, contrôles de readiness et workers comprenant les nouveaux types. Conserver fermées les nouvelles écritures/modules non vérifiés, sans couper les parcours historiques par un flag global.
5. Livrer les lecteurs Animation, Pro, Marketplace/Live et ERP, leurs contrats embarqués et emails typés. Les versions anciennes/PWA en cache ne doivent pas pouvoir confirmer un nouveau type qu’elles ne savent pas présenter ; proposer mise à jour ou erreur explicite.
6. Vérifier les paramètres non secrets : URL publique Animation et URL Live canonique, allowlists origines/CORS/CSP, cookies/session/SW, comptes fournisseurs de test, clés QR/PIN et rotations, plafonds import, calendrier de service, destinataires Ops, cadence des jobs et échéances. Réutiliser les clés existantes lorsqu’elles ont le même objectif ; nommer les nouveaux réglages lors de l’implémentation, aucun secret dans les docs.
7. Exécuter l’exercice de restauration §5 et la recette pilote sur données contrôlées. Ouvrir seulement les capacités livrées et vérifiées de la commune validée ; publier un rapport de bascule avec refus observés et conditions de retour. Étendre commune par commune sur le même contrôle.

Retour arrière : distinguer rollback binaire avant données nouvelles et correction compatible après usage. Après émission d’un bon ou droit module, ne pas effacer tables, attributions ou paiements pour revenir à l’ancienne version. Suspendre les nouvelles commandes touchées, garder les engagements lisibles et honorables dans le service compatible, réconcilier puis corriger. Un incident sécurité peut exiger une suspension plus forte, explicite et auditée ; la continuité commerciale n’est pas un contournement.

## 5. Exercice de reprise — CA-63

**Responsable : équipe technique Localeo.** Avant mise en service, puis chaque trimestre et après modification majeure du dispositif de sauvegarde/restauration. RPO **4 heures maximum**, RTO **8 heures maximum** ; ces valeurs sont des objectifs à démontrer, pas des garanties d’exploitation déjà vérifiées.

Périmètre cohérent : base et journal nécessaire au point de reprise, objets DAM/documentaires/private imports/export encore requis, configuration/version du code, références et accès aux secrets gérés séparément, habilitations/révocations/suppressions, état des tâches/outbox, idempotence et rapprochement des fournisseurs. Une sauvegarde base seule ne suffit pas si les documents ou clés nécessaires ne sont plus accessibles. L’exercice utilise un environnement isolé représentatif, avec interdiction d’envoyer aux vrais destinataires ou de rejouer des paiements réels.

Mesures : `incident_at`, `dernier_instant_restituable_coherent`, `reouverture_parcours_essentiels_at`. La perte mesurée doit être au plus 4 h ; le temps entre l’incident simulé et la réouverture validée doit être au plus 8 h. Inclure la préparation, la restauration et les contrôles, pas seulement la durée de `pg_restore`. Documenter l’hypothèse de détection et l’écart éventuel plutôt que déplacer le départ du chronomètre après le diagnostic.

Procédure d’exercice :

1. Définir le scénario de panne, sauvegarde choisie, volume représentatif, dernière transaction témoin et état des objets ; relever heures UTC et versions.
2. Restaurer sur cible vierge isolée, contrôler empreintes, relations, schéma/migrations et droits. Réappliquer les suppressions et révocations dues avant ouverture.
3. Maintenir les envois et tâches automatiques fermés pendant le rapprochement des effets externes. Pour paiement, message ou remise dont le résultat est incertain dans la fenêtre perdue, retrouver les preuves/IDs externes ou mettre la cible en attente de traitement ; ne pas autoriser une répétition aveugle au motif du RPO accepté.
4. Jouer accès/responsable/salarié, participation, lot externe, scan/PIN, bons corrigés/révoqués, droits module expirés et imports/campagnes partiels. Vérifier qu’un ancien accès révoqué et un ancien QR remplacé restent refusés.
5. Réouvrir les parcours essentiels sur la cible d’exercice après cohérence démontrée, reprendre les jobs sans duplication, mesurer RPO/RTO et consigner résultats des [DR-001 à DR-008](../../exploitation/recette/cahier-recette-generale-avant-mep.md).
6. Archiver rapport daté : environnement/versions, sauvegardes/objets, durées, échantillons rapprochés, refus, incertitudes, opérateurs, écarts et correction. Preuve absente ou objectif manqué : **mise en service concernée bloquée**, exercice à refaire après correction.

Une restauration locale éphémère de démonstration est une preuve utile de cohérence de l’outillage, pas la preuve hébergée de ce critère. Aucun exercice distant n’est exécuté par la rédaction de ce dossier.

## 6. Contrôles et bilan de cette spécification

### Preuves UX et accessibilité attendues

Exigence transverse du 18 octobre, détaillée dans les [parcours SaaS, section 5](perimetres-parcours-saas.md), applicable à US23/29 et aux parcours de gestion des lots, imports, campagnes et souscriptions. Les critères métier restent inchangés ; ces preuves complètent leur recette.

| ID | Parcours / preuve | Résultat attendu |
| --- | --- | --- |
| E73-UX-01 | Organisateur débutant : liste → création → brouillon → contrôle de publication, trois dotations | Contexte commune visible, prochaine action compréhensible, étapes et blocages expliqués ; retour à la liste conserve filtres/page, aucune réussite anticipée |
| E73-UX-02 | Visiteur : accueil public → animation → participation → retour Live | Compréhension dates/lieu/règles et action principale ; découverte sans compte, accès participant distinct de l’accès gestionnaire ; aucun détour imposé par Coffrets |
| E73-UX-03 | Import en conflit, campagne en attente, tirage `202`, réponse perdue et refus de droit | États lisibles et annoncés, saisie conservée, reprise de la même opération, action de résolution ou aide accessible ; aucune répétition involontaire d’un effet |
| E73-UX-04 | Clavier et lecteur d’écran sur les deux parcours, menus, formulaires et fenêtres | Noms et structure compréhensibles, focus visible/ordonné/restauré, aucune impasse ; erreurs et résultats annoncés, sens indépendant des couleurs |
| E73-UX-05 | Mobile 320 pixels CSS, texte 200 %, contrastes, réduction des animations | Informations et actions conservées, absence de débordement global ; contrôles tactiles et critères de contraste de conception vérifiés |
| E73-UX-06 | Essai des deux parcours par des personnes peu familières de Localeo, plus audit automatisé | Compte rendu des réussites, erreurs et hésitations ; obstacles essentiels corrigés avant généralisation. Un audit automatisé seul ne vaut pas validation de l’accessibilité |

Conserver captures/états, scénario, appareil/navigateur et technologie d’assistance, résultats et corrections dans les preuves de réalisation. Aucun essai utilisateur, recette navigateur ou audit d’accessibilité exécuté lors de cette rédaction.

Organisation de la validation confirmée le 18 octobre : **Localeo en premier**, puis essais avec la **commune pilote de Martignas-sur-Jalle**. La première passe corrige les obstacles internes avant présentation au pilote ; la seconde vérifie la compréhension et l’usage des parcours par les personnes concernées. Consigner les retours et corrections avant extension aux autres communes. Ce choix désigne les étapes de recette, pas une validation déjà obtenue.

### Preuves de performance attendues à l’implémentation

Appliquer [P01 à P08](../../architecture/transverse/performance-volumetrie.md) et la matrice d’accès E73. Ces scénarios complètent les CA, sans changer les tarifs, quotas commerciaux ou règles de tirage. Réutiliser le [banc E59](../epic-59-tests-performance-api/conception-technique.md) et des données synthétiques sur cible jetable ; la présente revue ne lance aucune campagne de charge.

| ID / couverture | Scénario discriminant | Critère observable |
| --- | --- | --- |
| E73-PERF-01 — listes, CA-12/18/20/25/37/53 | Pages 25 et 100, première et curseur profond ; faire croître séparément tenant consulté, tenants étrangers et historique à N/10N ; filtres rares/fréquents et liste vide | Limite effective en SQL et portée d’accès avant limite, enrichissement borné, nombre de requêtes stable, pas d’hydratation proportionnelle au volume global ; plans et buffers conservés |
| E73-PERF-02 — validations, CA-08/10/35/36 | Scan/PIN sous lecture d’historique, grand stock et nombreuses autres communes | Recherche ciblée et droits courants ; aucune double remise, index utile, pas de verrou de commune ou de chargement d’historique complet |
| E73-PERF-03 — campagne et quotas, CA-38/40/47/49 | Audience N/10N, deux campagnes d’une commune, publication simultanée et autres communes, derniers crédits, bail expiré | Premier débit unique, fréquence correcte ; continuation sans mutex de quota ; mémoire bornée, attente de verrous et âge de file mesurés, progression équitable |
| E73-PERF-04 — bilans/coûts, CA-60/61 | Même nombre d’animations affichées, croissance participants/passages/gains/avis ; cache froid/chaud | Totaux par agrégation/projection, détails paginés, pas de N+1 ni lecture complète des enfants ; fraîcheur annoncée et budget interactif tenu |
| E73-PERF-05 — import/jobs, CA-44/45/46 | Import 100 lignes puis nombreuses opérations indépendantes ; ambiguïtés, fichiers compressés, échéances massives, interruption/reprise | Limites 100/2 Mo et décompression/parseur maîtrisés ; rapprochement indexé, jobs bornés, aucun accès automatique ; pas de scan de l’annuaire par ligne ni de claim global |
| E73-PERF-06 — export, CA-62 | N/10N lignes et octets de médias, modifications pendant capture, arrêt capture puis assemblage, responsable retiré | Manifeste cohérent, mémoire et espace temporaire dans leurs budgets, reprise sans mélange d’instantanés ; aucun verrou métier pendant transfert ; archive complète ou échec explicite |
| E73-PERF-07 — tirage, CA-07/32 | Faire varier séparément population, nombre de lots et commerces ; double confirmation et retrait de périmètre | Préparation sans effet publié, réserve exhaustive/unicité, confirmation atomique, mémoire/temps sous verrou mesurés ; aucune troncature pour accélérer |
| E73-PERF-08 — frontend et charge mixte, CA-18/24/53 | Navigation/polling pendant imports, campagnes, exports et tirages, annulation/changement d’organisation | Aucun préchargement de toutes les pages, cache/DOM bornés, appels obsolètes annulés ; p95/p99 interactifs et taux d’erreur dans budgets, saturation explicite puis récupération |

Deux axes distincts : volume N/10N à trafic fixé, puis trafic par paliers à jeu fixé. Les valeurs de N, distribution par tenant, ancienneté, tailles de médias, durée et débit sont inscrits au rapport **avant** chaque campagne ; inclure une commune très active et beaucoup de petites communes. Ne pas tirer une conclusion de capacité d’un jeu minuscule ou d’un cache chaud seul.

Référence de départ confirmée le 18 octobre : **10 communes et 10 000 participants au total**, avec **10 utilisateurs actifs simultanément** pour représenter les connexions annoncées. Exécuter une répartition équilibrée puis une répartition concentrée, en gardant le total fixe. Pour l’axe volumétrie, comparer notamment 10 000 à 100 000 participants synthétiques à concurrence fixe ; pour l’axe trafic, augmenter par paliers au-delà de 10 utilisateurs sur le jeu de référence. Les scénarios notent cadence, temps entre actions, rôles, durée et requêtes/seconde réellement obtenues : connexions simultanées et débit HTTP ne sont pas équivalents. Les paliers supérieurs explorent la marge et la saturation, sans promettre leur prise en charge ni créer un quota commercial.

Budgets initiaux à calibrer : reprendre E59 pour Animation listes/détail (p95 700 ms), bilans (900 ms), ERP listes (1 000 ms), Pro écritures (1 000 ms), Live listes (600 ms), erreurs inattendues inférieures à 0,5 %. Ce sont des objectifs de départ, pas des résultats ni des SLA acquis. Définir aussi p99, mémoire, pool/verrous, débit soutenu et délai des jobs avant leur recette ; le délai de réponse d’acceptation d’un export/tirage ne représente pas son délai de fin. La phase terminale atomique du tirage doit disposer de son budget spécifique.

Archiver par scénario : SHA, migrations/index réellement installés, matériel, statistiques PostgreSQL, SQL/plans, nombre de requêtes/objets hydratés, latences, erreurs, ressources, attentes, débit/âge des files et comparaison. Une page dont le coût suit linéairement le volume global ou un budget dépassé reste un écart à traiter. La croissance linéaire du travail total d’un export/permutation est attendue ; la mémoire et l’impact interactif doivent rester bornés dans l’enveloppe déclarée. Les seuils et performances hébergées ne sont pas vérifiés par les contrôles documentaires.

### Preuves DDD attendues à l’implémentation

La [revue des frontières](architecture-contrats.md) complète les CA existants ; elle n’ajoute pas d’arbitrage produit. Chaque scénario ci-dessous doit distinguer test de règle pure, test d’orchestration et preuve transactionnelle réelle.

| Contrôle | Preuve attendue |
| --- | --- |
| Domaine indépendant | Construire agrégats/valeurs/politiques sans ORM, framework, configuration opérateur, réseau ni horloge implicite ; les contrôles d’import complètent les tests de refus et transitions, sans les remplacer |
| Frontières et adaptateurs | API, ERP et worker passent par les mêmes commandes ; faits interdomaines typés et versions courantes. Un frontend, un job ou un repository ne décide pas lui-même du quota, de la remise ou du périmètre |
| Remboursement | Politique pure du disponible : réservé, confirmé, rejet définitif, résultat inconnu et confirmation rejouée. Deux approbations concurrentes sous PostgreSQL ne dépassent jamais l’encaissement disponible ; réponse fournisseur perdue ne libère pas la réservation et ne retire pas implicitement un droit |
| Campagne volumineuse | Audience cohérente scellée, arrêt/reprise pendant préparation puis après premier message et au milieu du traitement. Aucune émission avant engagement ; quota débité une seule fois, aucun destinataire ajouté, aucune duplication Live et fréquence interanimations respectée |
| Verrous et bail | Deux connexions PostgreSQL font concourir démarrage, reprise et consommation du dernier crédit ; ordre commun conservé, worker au bail périmé refusé, aucun verrou de claim conservé dans la transaction métier |
| Projections et autorité | Tableau de bord volontairement retardé sans effet sur autorisation/quota/remboursement ; compteur de décision et journal atomiques, reconstruction contrôlée, refus sur incohérence |
| Transactions interagrégats | Échec injecté entre débit/publication, attribution/bon, ligne/fiche et message/fréquence : aucun état partiel acquis. Outbox non visible avant commit, livraison après commit reprenable sans recommencer la transition |

Les bornes techniques de capture/lot et les durées de transaction des campagnes seront mesurées à volume représentatif avant activation ; aucune performance n’est prouvée par cette seule conception. Les confirmations de tirage restent soumises à leur atomicité propre et doivent également faire l’objet de mesures de capacité.

À l’implémentation, lancer le [runner isolé backend](../../../../localeo-backend/scripts/validation/test_isolated.py) sur tests domaine/application/API ciblés, puis tests PostgreSQL/concurrence et contrôles d’architecture selon le [guide backend](../../../../localeo-backend/AGENT.md). Les scénarios E73-T-* doivent être rattachés aux fichiers réels dans cette matrice avec commande, SHA/arbre, environnement et résultat. Les contrats générés et consommateurs doivent être contrôlés ensemble. La démonstration utilise le [runner de compatibilité](../../../../localeo-backend/scripts/validation/run_demo_compatibility_tests.py) et ses bases jetables.

Lors de la rédaction initiale de la spécification, seuls les contrôles documentaires et la revue indépendante du [README](README.md) avaient été réalisés ; aucun contrôle applicatif ni déploiement n'avait été exécuté. Les preuves d'implémentation ajoutées depuis sont raccordées par lot ci-dessus et détaillées dans le [suivi de réalisation](suivi-implementation.md). Les exercices hébergés, la recette humaine et les déploiements restent non exécutés. Les travaux préexistants des dépôts voisins et du suivi moteur sont préservés.
