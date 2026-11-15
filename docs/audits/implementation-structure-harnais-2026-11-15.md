# Mise en œuvre de l’audit structure, documentation et harnais

Date : 15 novembre 2026. Source : [audit et critères](structure-documentation-harnais-2026-11-15.md).
Les cinq dépôts restent indépendants. Les modifications portent sur Projet,
Backend, Animation et Commerçant ; Marketplace reste inchangée. La demande
ultérieure « commit et push » autorise leur publication sur les branches `main`.
Les commits par lot sont référencés ci-dessous. Aucun déploiement, envoi réel
ou accès à une base partagée n’est effectué.

## Exécution et isolation — lot 1

- L’audit backend délègue au runner isolé commun. Il exige une URL explicite
  limitée au rôle et aux noms de bases jetables autorisés sur `127.0.0.1`.
  Les deux variables de fixtures sont harmonisées ; les variables natives `PG*`
  sont effacées. Les gardes couvrent sockets, `connect_ex`, psycopg synchrone et
  asynchrone. Les tests utilisent une fausse cible héritée sans la contacter.
- Le preflight charge la configuration puis impose `SKIP_BOOTSTRAP=True` avant
  l’import applicatif. Le test remplace le bootstrap par un échec explicite et
  vérifie le contrôle nominal avec une configuration résolue initialement active.
- Le runner qualité possède un Job Object Windows avant de libérer son lanceur.
  Il termine et attend les descendants, même si leur parent a disparu ; les
  processus étrangers restent hors de ce job. POSIX utilise un groupe séparé,
  terminé également après un parent réussi qui laisserait un serveur actif.
  Timeout et interruption ont des reproductions avec petits-enfants synthétiques.
- Les builds Pro/Animation réutilisent leurs builders synthétiques dans des
  sorties uniques. Vitest Pro conserve toute sa sélection avec des paramètres
  publics explicites. Les tests de contamination des builds vérifient deux
  sorties distinctes et l’absence des valeurs héritées dans les scripts livrés.
- La publication initiale des rapports utilise un renommage exclusif Windows
  et un lien exclusif POSIX. Les mises à jour restent atomiques ; les attentes
  Windows bornées ne permettent jamais d’écraser une modification extérieure.

## Couverture, diagnostics et contrats — lot 2

L’audit PostgreSQL applique les migrations livrées avec `--migrate`. Un test
contrôle les contraintes de portée des exécutions et provoque un refus SQL réel
sur une révision invalide. Les deux scénarios de concurrence sont obligatoires :
absence, skip, xfail ou échec invalident le profil. Leurs anciennes fixtures,
qui n’atteignaient plus le service actuel, utilisent désormais les repositories
réels et la barrière de coordination PostgreSQL. Une version de progression
périmée donne lieu dans le scénario à une relecture et une nouvelle intention
explicite ; aucune répétition automatique de commande n’est ajoutée au produit.

| Invariant / parcours | Preuve sélectionnée | Limite |
| --- | --- | --- |
| Clôture contre scan, deux validations conservées | Deux scénarios de concurrence obligatoires | PostgreSQL jetable uniquement |
| Portée financière partenaire/commune | `test_animation_finance_tenant.py` | Fixtures SQL ciblées |
| Création atomique et idempotence | `test_animation_creation_atomicity.py` | API/prestations voisines hors de ce scénario |
| Contraintes livrées | `test_animation_audit_migrations.py`, migrations depuis base vide | Aucun environnement hébergé vérifié |
| Génération/restauration et migrations complètes | Job démonstration préexistant, conservé | Campagne démonstration non rejouée dans cette tâche |
| Navigation, session, Lots et remises, PWA | `pnpm test:browser:critical`, API synthétique, Chromium local verrouillé | Autres recettes et appareils physiques hors sélection |
| Console ERP exploitation | `npm run test:browser:erp`, six scénarios 390/1280 px | Autres recettes ERP hors sélection |
| Types, champs requis, enums et réponses | Comparaison de 58 opérations Pro et 334 Animation, schémas transitifs | Périmètres déclarés, pas identité des exports complets |

Le contrôle contractuel ignore les annotations et les opérations extérieures
aux périmètres déclarés. Ses tests positifs et négatifs couvrent les types,
champs requis, enums, réponses et propriétés nommées `description`. Il est
raccordé au profil workspace et à sa CI avec révisions épinglées.

Le profil transverse `browser-critical` attribue un dossier par contrôle,
référence les fichiers par chemins relatifs, tailles et SHA-256, et refuse les
artefacts requis absents. Un test copie les preuves ailleurs puis vérifie
qu’une altération bloque la préparation de livraison. Les traces, captures,
JSON et HTML Pro sont conservés par upload même sur échec ; audit backend et
pilote ERP disposent de résultats structurés et d’artefacts CI par révision.

Le branchement du socle a révélé une course entre la fermeture du menu du
compte et le dialogue de protection de saisie Animation. La navigation est
maintenant différée jusqu’à libération du menu. La recette utilise de vraies
saisies et le dialogue actuel, avec annulation, conservation des valeurs et
sortie explicite ; elle ne simule plus un événement retiré du produit. La
recette de session ouvre le menu actuel pour se déconnecter. La recette PWA
contrôle la géométrie réelle des quatre actions du bandeau et leurs cibles
tactiles, au lieu du plafond historique de 64 px incompatible avec le cadre
commun actuel de 72 px minimum. Son attente du service worker est bornée ; un
échec de lancement conserve un diagnostic et ferme son serveur. Le profil
Chromium jetable utilise un chemin temporaire court, séparé des preuves, pour
permettre CacheStorage sous Windows même avec un dossier de rapport profond.

## Procédures et contrôles documentaires — lot 3

Les vingt procédures identifiées ont des rubriques renseignées : symptôme,
résultat, action, contrôles et arrêt/escalade. Leur contenu antérieur est conservé
sous la procédure, avec ses réserves de mise en service. Les dix-huit entrées
manquantes sont ajoutées aux catalogues spécialisés. Le lecteur ERP est testé.
La commande Pro exporte les quatre moteurs, dont `JUSTE_PRIX_LOCAL`. Les exemples
juridiques exécutés depuis le backend pointent vers les sources Projet ;
l’attendu du contrat commerçant 1.1 est corrigé avec la provenance
`9cde5ff4ff764c962320d5dbd16c2a6d0233c808`. Aucun PDF ni empreinte n’est modifié.

Le contrôle courant vérifie les cinq racines Git ; l’audit des anciennes
destinations exige `--historical-migration`. L’inventaire des liens réutilise le
parseur et le corpus Git de `check_guidance.py`. Les trois références cassées
sont contextualisées comme historiques, sans recréer leurs anciennes cibles.
Les procédures, le catalogue juridique et les nouveaux vérificateurs sont
raccordés au profil documentaire local. La CI est définie sur Windows et Linux.

## Hooks et exercices de workflows — lot 4

`core.hooksPath=.githooks` résout le hook depuis chaque worktree. Le montage
supporté utilise le même Python durable et les applications sœurs. Deux vrais
worktrees avec espaces sont éprouvés, dont un après indisponibilité des scripts
du checkout initial. Les gestionnaires existants sont préservés. Les deux
installations de pré-commit refusent les contrôleurs partiellement indexés ;
l’index n’est jamais modifié. Les quatre métadonnées YAML existantes sont
contrôlées sans imposer ce fichier aux autres skills. Le hook Stop reste
consultatif et son silence sur un arbre propre reste intentionnel.

Sept exercices décisionnels ont été soumis à trois agents distincts avec des
sources synthétiques minimales et des extraits de règles. Faute d’outils dans
ces sous-agents, ils n’ont exécuté aucune opération ; leurs réponses constituent
une évaluation de décisions, séparée des tests exécutables de ce bilan.

| Cas joué | Observation produite | Revue de l’agent principal |
| --- | --- | --- |
| Besoin ambigu et identifiant historique | Réutilisation de l’epic 62 à faire ; question limitée aux champs couverts par le sas | Conforme ; aucun doublon ni statut inventé |
| Clôture avec skip et rapport périmé | Refus de clôture, CA3 non prouvé, conservation de `notes.txt` indexé, prochaine vérification identifiée | Conforme ; pas de preuve ancienne réutilisée |
| Import concurrent de génération | Règle au domaine, comparaison atomique date/dotation, refus sans écriture partielle, impacts API/ERP/batch/démo | Conforme ; classement de `nom` laissé explicite dans la fixture ambiguë |
| Reprise et données obligatoires | Restaurateur à adapter avec générateur, PostgreSQL annoncé non exécuté, note lot/preuves/serveur/prochain geste | Conforme ; aucune exécution inventée |
| Commit déjà autorisé et changements mixtes | Reprise sans reconfirmation, sélection limitée à l’epic, conservation de l’index étranger, configuration future distincte | Conforme ; aucun push ni déploiement implicite |
| Clôture prête et préparation du commit | EX-5 clôturable, trois critères prouvés sur SHA courant, sélection des seuls fichiers EX-5 et roadmap ; note étrangère conservée indexée, configuration future distincte | Conforme ; préparation sans commit global, push ni déploiement |
| Procédure déplacée et consommateur | Source canonique, export et résumé ERP raccordés, contrôles ciblés sans nouvel epic | Conforme ; générateur maintenu dans son application |

Aucune erreur décisionnelle de ces exercices ne justifie une nouvelle règle
générale dans les skills. Le protocole est complété sur autorisation persistante,
reprise et preuves périmées. Ces essais ne certifient pas l’exécution intégrale
des onze workflows par un agent outillé, ni l’activation native des hooks.

Empreintes des fiches utilisées comme référence d’évaluation :

| Skill | SHA-256 du SKILL.md |
| --- | --- |
| [localeo-cloturer-epic](../../.agents/skills/localeo-cloturer-epic/SKILL.md) | `5b47e08ffc198598562f7afc8e989502e0b0aef74846e4cb56e0cb60c50ccd12` |
| [localeo-corriger](../../.agents/skills/localeo-corriger/SKILL.md) | `a43bf4400d349e11501145f59d04f95b651a70ed3e022159a1f669182fa7ffab` |
| [localeo-creer-epic](../../.agents/skills/localeo-creer-epic/SKILL.md) | `50ea6fc383d174f29416604264c5d47b35149d564165739f5bfe9ae44f989768` |
| [localeo-documentation](../../.agents/skills/localeo-documentation/SKILL.md) | `685b5604cb0002794f016dbab88dc4dfe77f7e8b3d4fe8f46becbe2b4d223347` |
| [localeo-faire-evoluer-epic](../../.agents/skills/localeo-faire-evoluer-epic/SKILL.md) | `967acf64cb1a8a8d84e2c34a7daf612ca96bbc24d31616056a6e6a292c0f84c4` |
| [localeo-implementer-epic](../../.agents/skills/localeo-implementer-epic/SKILL.md) | `a050aac3786cb1ef0dc40cd6af494418f7f0fbb0407f6d5f27c4089979cc1301` |
| [localeo-invariants](../../.agents/skills/localeo-invariants/SKILL.md) | `9e9475574a9604e4c7cc08c8a5149779176adcccbd359862728eec5ea7004853` |
| [localeo-preparer-deploiement](../../.agents/skills/localeo-preparer-deploiement/SKILL.md) | `597b0605160017327d435597e147d92f296178ca8401bfe0989cd321ec9c7be6` |
| [localeo-specifier-epic](../../.agents/skills/localeo-specifier-epic/SKILL.md) | `03c89ab89d1beead5a98d82ab0937b64b540388315999a3e44d730a5a1063dc4` |
| [localeo-verifier-demonstration](../../.agents/skills/localeo-verifier-demonstration/SKILL.md) | `8238bcf05aa8fb0f28f8d91e29ec038645826ddba4ecea934437ae9837e7710a` |
| [localeo-verifier-exigence](../../.agents/skills/localeo-verifier-exigence/SKILL.md) | `6e734ac5b2229cd046c85d08432db3f6b19a2f352e112c58056f540275cb4ccc` |

## Recensement des recettes ERP hors pilote

Les recettes suivantes référencent encore un dépôt frontend voisin ; elles
restent hors du job pilote autonome, sans être présentées comme exécutées :

`acces-commercant-erp.cjs`, `admin-shell.cjs`, `adresse-commercant-erp-onboard.cjs`, `animation-consoles-shell-ux.cjs`, `animation-navigation-erp.cjs`, `atelier-assiste-erp.cjs`, `atelier-fournisseurs-perimetres.cjs`, `atelier-prix.cjs`, `atelier-pwa.cjs`, `batchs-manuels.cjs`, `commercants-erp-ux.cjs`, `connexion-interne.cjs`, `conservation-erp.cjs`, `contact-public-erp.cjs`, `control-header-mobile.cjs`, `crm-actualisations.cjs`, `crm-agenda.cjs`, `crm-carte-axes.cjs`, `crm-correctifs.cjs`, `crm-import-progress.cjs`, `crm-priorite.cjs`, `crm-productivite.cjs`, `crm-qualification-productivite.cjs`, `crm-qualification.cjs`, `crm-rappels.cjs`, `crm-selecteurs.cjs`, `crm.cjs`, `epic65-audit-erp.cjs`, `epic65-finance-erp.cjs`, `epic65-webpush-erp.cjs`, `epic69-acces-internes.cjs`, `epic69-onboard.cjs`, `epic69-suivi-financier.cjs`, `epic73-checkout-erp.cjs`, `epic73-modules-erp.cjs`, `epic73-modules-ux.cjs`, `epic73-operations-ux.cjs`, `epic73-perimetres.cjs`, `epic73-pilotage-economique.cjs`, `epic73-preparations-service.cjs`, `epic73-reversibilite.cjs`, `epic73-sollicitations.cjs`, `epic73-suivi-produits.cjs`, `epic73-support-organisations-ux.cjs`, `epic73-support-organisations.cjs`, `epic73-verifications-import.cjs`, `epic74-participants-erp.cjs`, `equipes-animation-erp.cjs`, `erp-gestion-admin.cjs`, `erp-gestion-animation.cjs`, `erp-gestion-preparations.cjs`, `erp-gestion.cjs`, `erp-home-applications.cjs`, `erp-menu-ux.cjs`, `erp-page-template.cjs`, `erp-productivite.cjs`, `erp-session-dialog.cjs`, `erp-template-modules.cjs`, `generation-erp-guidance.cjs`, `generation-erp-workflow.cjs`, `generation-erp.cjs`, `gestionnaire-souscription-ux.cjs`, `habilitations-animation-erp.cjs`, `header-mobile.cjs`, `juste-prix-ux.cjs`, `modules-utilisateurs-erp.cjs`, `offre-version-navigation.cjs`, `onboard-administration.cjs`, `onboard-dossier-ux.cjs`, `ops-alert-priorities.cjs`, `parametres-exploitation-erp.cjs`, `paris-dates.cjs`, `pin-validation-erp.cjs`, `preparation-erp.cjs`, `pwa-lifecycle.cjs`, `shell-navigation.cjs`, `souscriptions-responsable-erp.cjs`, `support-loading.cjs`, `tirage-annonce-erp.cjs`.

## Preuves et limites

Les résultats locaux portent sur Windows, Python 3.14.3 et Node 24.14.0.
Les workflows Linux/Node 22 sont configurés mais leur exécution distante et les
protections de branche restent externes. Les versions Git de départ sont celles
de l’audit ; les arbres modifiés ne sont pas des révisions de livraison validées.

- Pro : 89 fichiers Vitest, 642 tests réussis ; build synthétique réussi et test
  de contamination sur deux sorties réussi.
- Animation : types et lint réussis ; 339 tests Node réussis, dont les tests
  négatifs de harnais et d’échec de lancement Chromium, et l’isolation des builds.
- Backend ciblé : 36 tests réussis sur PostgreSQL 18 local jetable, migrations
  comprises, aucun skip ; lecteur ERP inclus. Les deux cas de concurrence et le
  refus SQL sur schéma migré figurent dans le JUnit et son manifeste SHA-256.
  Architecture : 730 tests réussis. Pilote navigateur : six scénarios réussis.
  Le serveur PostgreSQL possédé par cette tâche est arrêté après les contrôles.
- Documentation : suite complète de 129 cas, dont 128 réussis et un skip de création
  de lien symbolique propre à ce poste Windows ; après ajout du dernier cas de
  nettoyage des descendants, le profil `documentation-workspace` est réussi,
  dont 49 tests qualité et les contrôles des hooks, procédures et contrats.
- Guides et Markdown : 757 documents, 5 009 liens locaux, zéro erreur ni warning.
- Sources exportées : 150, sans modification de manifeste ni de contrat lecteur.
- Le premier passage élargi backend a donné 1 243 succès et 15 échecs. Les deux
  scénarios SQL obsolètes et le test de sous-processus sont corrigés par ce lot.
  Douze autres échecs restent dans les tests catalogue, publication, modification
  en cours, reçus, supports et tirage ; ils ne sont ni supprimés ni ignorés.
  La CI générale audit ne peut donc pas être annoncée verte sur ces seuls contrôles.

Les campagnes de charge, la démonstration complète et les appareils physiques
restent hors sélection. Aucune modification de règle métier, migration produit
ou adaptation du générateur de démonstration n’est nécessaire : les changements
concernent le harnais, les lecteurs documentaires existants et une transition de
focus/menu sans effet sur le contrat métier. Les réserves GL-16/LA-16, les états
historiques de roadmap et les conditions de déploiement restent inchangés.

## Dette backend observée dans la sélection étendue

Les douze échecs restants portent sur des tests et du code métier non modifiés
par ce chantier. Ils sont conservés comme limites, sans changer les assertions
pour annoncer une CI verte :

| Fichier | Échecs | Cause observée |
| --- | ---: | --- |
| `test_lot3_catalogue.py` | 1 | Libellé attendu sans accent contre libellé actuel accentué |
| `test_catalogue_chasse_t2.py` | 1 | Doublure sans propriété `reversibilite` |
| `test_modification_animation_en_cours.py` | 3 | Ancienne modification directe de date ; commande d’exploitation versionnée requise |
| `test_recu_unique_commande_lots.py` | 1 | Doublure sans `obtenir_pour_mise_a_jour` |
| `test_supports_commerce_chasse.py` | 2 | Doublure sans propriété `reversibilite` |
| `test_tirage_tous_lots_animation.py` | 4 | Doublure sans `obtenir_entete_population_courante` |

La première relance du contrôle d’architecture depuis le shell a également
révélé un handle stdin Windows non héritable. La relance avec stdin `DEVNULL`
réussit ; aucune assertion d’architecture n’a été modifiée pour cela. Le runner
et la collecte Git du manifeste évitent désormais cet héritage inutile.

## Emplacement des preuves locales

Les sorties restent ignorées par Git. L’archive
`.artifacts/structure-harnais-evidence-20261115.zip` regroupe 362 fichiers,
dont les 343 artefacts navigateur référencés, les rapports qualité, le JUnit
backend, son manifeste et les journaux de contrôle. Ses fichiers ont été relus
depuis le ZIP et comparés à leurs empreintes. SHA-256 de l’archive :
`da7ed520414ec1488b96f34d50fb248d9b77dd85e2538a87694d84a4213a3a09`.

| Profil / preuve | Rapport local relatif à Projet |
| --- | --- |
| Chromium Animation et ERP : réussi | `.artifacts/quality/run-20261115T154212.324708Z-tqomqebp/run.json` |
| Documentation workspace : réussi | `.artifacts/quality/run-20261115T153819.888347Z-m0povyp0/run.json` |
| Deux builds synthétiques : réussi | `.artifacts/quality/run-20261115T152702.132729Z-2mgd0v4b/run.json` |
| PostgreSQL : 36 réussites, zéro skip | `../localeo-backend/.artifacts/audit-backend-verified.xml` et `.manifest.json` |
| Suite documentaire : 128 réussites, un skip | `.artifacts/documentation-unittest-verified.log` |
| Dernières fiches réflexes : six tests réussis | `.artifacts/documentation-content-confirmed.log` |

Le socle navigateur réussit les dix parcours de navigation, les 112 scénarios
Lots et remises, le parcours de session, les scénarios PWA et les six scénarios
ERP. Le rapport lie la tentative précédente sans réutiliser ses réussites.
Les anciennes tentatives échouées restent disponibles séparément. L’archive
n’est pas une preuve de release : les arbres sont modifiés et les contrôles
externes explicitement cités plus haut restent à exécuter.

## Commits par lot

Créés après la demande explicite de commit et push du 15 novembre 2026.
Le découpage de l’index conserve à l’octet les contenus de travail validés ;
les dernières modifications de ce bilan concernent uniquement les références
et l’état de publication. Les preuves précédentes restent des preuves sur
arbres modifiés, pas des contrôles CI attestés sur ces nouveaux SHAs.

| Dépôt | Lot | Commit |
| --- | --- | --- |
| `localeo-projet` | 1 | [`a118484dd1`](https://github.com/contactlocaleo/localeo-projet/commit/a118484dd1cf3718c1b42908925a7753176908c0) |
| `localeo-backend` | 1 | [`959c5eaa14`](https://github.com/contactlocaleo/localeo-backend/commit/959c5eaa146708b4df9dea363d98999a390939a2) |
| `localeo-animation` | 1 | [`fcc64b1e35`](https://github.com/contactlocaleo/localeo-animation/commit/fcc64b1e35cae656b3baf68474e4e55c1102cc24) |
| `localeo-commercant` | 1 | [`829fcaaa0f`](https://github.com/contactlocaleo/localeo-commercant/commit/829fcaaa0f6f1b5d8e96a435a8a34d571367086d) |
| `localeo-projet` | 2 | [`0a57b95914`](https://github.com/contactlocaleo/localeo-projet/commit/0a57b9591435bca0710a706c5c7c505bf425fe33) |
| `localeo-backend` | 2 | [`272a60a1bd`](https://github.com/contactlocaleo/localeo-backend/commit/272a60a1bde8026a7c4afdfcd32aa63630fdaeee) |
| `localeo-animation` | 2 | [`de083ecbdb`](https://github.com/contactlocaleo/localeo-animation/commit/de083ecbdbad99367f783f7686cbdfbc51777ac5) |
| `localeo-commercant` | 2 | [`9d902dc59f`](https://github.com/contactlocaleo/localeo-commercant/commit/9d902dc59f2bdc3ad5bd29690841f3023e8229fc) |
| `localeo-projet` | 3 | [`a986645511`](https://github.com/contactlocaleo/localeo-projet/commit/a986645511020f72f53f201796b68dbba65b502f) |
| `localeo-commercant` | 3 | [`8453252c54`](https://github.com/contactlocaleo/localeo-commercant/commit/8453252c54de3529e8646ae17c1c930a2c73c676) |
| `localeo-projet` | 4 | [`8dc9522f84`](https://github.com/contactlocaleo/localeo-projet/commit/8dc9522f84f80bc75dba1b24061277097487d46a) |

Le présent audit et son bilan sont regroupés dans un commit documentaire de
coordination après ces onze commits. Les push suivent les commits ; leur
succès est vérifié par comparaison des références distantes. Aucun push forcé
ni déploiement n’est prévu. Marketplace ne reçoit aucun commit.
