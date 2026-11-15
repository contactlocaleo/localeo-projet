# Audit de la structure Localeo et plan de fiabilisation

Date de référence : **15 novembre 2026**. Périmètre : les cinq dépôts Localeo,
leur documentation, leurs tests, leurs workflows CI, leurs skills et leurs hooks.

**La structure générale est cohérente. Les améliorations prioritaires portent
sur la fiabilité d'exécution des contrôles, leur couverture continue et
l'exactitude des procédures utilisées pour agir.** Le projet dispose déjà de
nombreux mécanismes utiles ; les quatre lots doivent les compléter et les
raccorder.

Ce rapport consolide l'audit initial et sa contre-revue. Il remplace le premier
lotissement en sept chantiers par quatre lots plus ciblés. Au moment de sa
rédaction, la préparation de l'implémentation a été interrompue pendant la
lecture des sources : **aucun des quatre lots n'est implémenté ou commité**.
Le rapport et son référencement dans l'index sont des travaux documentaires.

> Suivi de réalisation : les quatre lots ont ensuite été mis en œuvre dans
> Projet, Backend, Animation et Commerçant. Le [bilan de mise en œuvre](implementation-structure-harnais-2026-11-15.md)
> décrit les changements, preuves locales et limites restantes. Les états
> « à implémenter » ci-dessous conservent la photographie de l’audit initial ;
> ils ne constituent pas le suivi courant. Les commits par lot sont référencés
> dans le bilan après la demande explicite de commit et push.

## 1 Synthèse des décisions

| Décision | Conséquence pour les travaux |
| --- | --- |
| Préserver les cinq dépôts indépendants et la documentation canonique | Aucun regroupement Git ni duplication de spécifications par application. |
| Réutiliser les runners et les rapports existants | Corriger leurs garanties et raccorder les preuves applicatives. |
| Prioriser les défauts démontrés | Traiter les cibles PostgreSQL héritées, les deux tests ignorés et les processus survivant aux timeouts. |
| Compléter la CI selon le risque | Commencer par les scénarios critiques existants, puis étendre selon le coût et les lacunes constatées. |
| Corriger les instructions opérationnelles avant les archives | Les commandes d'export Pro et les chemins juridiques passent avant les liens historiques. |
| Conserver les hooks consultatifs | La preuve de réussite appartient aux tests et aux rapports, pas au statut Git seul. |
| Réduire progressivement les gros modules | Extraire des responsabilités lors des évolutions qui les touchent, avec preuve de non-régression. |

Ordre proposé : **lot 1 et corrections documentaires prioritaires du lot 3 en
parallèle, puis lot 2, fin du lot 3 et lot 4**. Les ressources de test et les
fichiers modifiés doivent avoir des propriétaires distincts pendant le travail
parallèle.

## 2 Périmètre et niveau de preuve

### Versions examinées

Les arbres de travail étaient propres lors de l'audit et avant la rédaction
du rapport. Les constats ci-dessous se rapportent à ces versions locales.

| Dépôt | Responsabilité | SHA de référence |
| --- | --- | --- |
| localeo-projet | Documentation, coordination et outils transverses | `c1c7faf2b18c0f0eb4b7f1f69b4ed26e75db8afb` |
| localeo-backend | Domaine, API, ERP, traitements et migrations | `be01e615218a21e7b413739287ccbd551d5c3a63` |
| localeo-animation | Interface des organisateurs | `5dbfe45170d36bd929d4fcf6f8a1a55d1a34c16d` |
| localeo-commercant | Localeo Pro | `bdc9a54d06182847307574da404753c8b0b79c2d` |
| localeo-marketplace | Marketplace et Localeo Live | `59c69bd6cefdccd16c89cf5164c11a8ac5bf354d` |

### Méthode et limites

La revue combine lecture des producteurs et consommateurs, analyse des
commandes effectivement sélectionnées, vérifications documentaires et trois
contre-revues indépendantes sur des périmètres différents de la première
lecture. Les défauts de configuration et de processus ont été éprouvés avec des
fixtures synthétiques.

Les preuves locales ne renseignent pas l'activation native des hooks dans le
client, les protections de branche GitHub, les résultats des derniers jobs
distants ou l'état des environnements hébergés. Ces éléments restent à vérifier
lors de la mise en service des contrôles. Aucune connexion à une base partagée,
publication, migration ou communication réelle n'a été nécessaire à l'audit.

### Résultats des contrôles

Les décomptes documentaires correspondent au corpus avant ajout de ce rapport.

| Contrôle | Résultat observé | Interprétation |
| --- | --- | --- |
| Guides et liens locaux avec `check_guidance.py` | 98 guides, 1 273 liens, aucune erreur | Les entrées de documentation contrôlées sont accessibles. |
| Ensemble des Markdown avec `--all-markdown` | 755 documents, 4 935 liens, 3 erreurs | Les trois cibles manquantes sont dans des archives ou audits. |
| Sources exportées avec `sync_documentation.py --check-sources` | 150 sources vérifiées | Présence et cohérence des sources exportées ; aucune preuve de déploiement du bundle. |
| Configuration des workflows Codex | Aucune erreur du validateur | Validation structurelle ; elle ne démontre pas la qualité des décisions d'un agent. |
| Tests Node des hooks de contexte et de fin | 5 tests réussis | Comportement des scripts, sans preuve d'activation native. |
| Suite documentaire complète lors du premier audit | 117 tests annoncés, 39 échecs ou sous-échecs, 1 skip | Les 39 résultats sont concentrés dans trois méthodes ; ne pas les interpréter comme 39 défauts indépendants. |
| Nouvelle exécution ciblée procédures et catalogue juridique | 6 tests, mêmes 39 échecs ou sous-échecs, aucune erreur d'exécution ni skip | Confirme le périmètre documentaire décrit en F09. |
| Garde de configuration des tests de concurrence | Deux scénarios sélectionnés conduisent au skip dans une configuration propre | Reproduction synthétique du mécanisme ; le job GitHub lui-même n'a pas été exécuté pendant l'audit. |
| Arrêt des processus sur timeout | Un enfant synthétique écrit après le timeout de son parent | Défaut de nettoyage reproduit, sans réseau ni serveur. |
| Installation des hooks dans un worktree temporaire | Chemin hérité du dépôt principal et réinstallation protégée | Dépendance au chemin initial confirmée ; aucun écrasement silencieux observé. |

Le skip de la suite documentaire complète concernait la création d'un lien
symbolique indisponible sur ce poste Windows. Il est distinct des scénarios SQL
explicitement requis mais ignorés. Les sorties détaillées locales sont conservées
sous `.artifacts/structure-audit-20261115-145702/` et
`.artifacts/structure-counteraudit-20261115T142835Z/` ; ces répertoires ignorés ne
constituent pas des artefacts portables de livraison.

## 3 Fondations à conserver

La répartition entre domaine backend, orchestration et interfaces est explicite
dans les guides. Les sources canoniques vivent dans `localeo-projet`, les
générateurs dans leur application et les contrats embarqués auprès de leurs
consommateurs. Cette organisation évite plusieurs sources concurrentes.

Le [runner qualité](../../scripts/quality.py) possède déjà des rapports uniques,
une publication atomique, des tentatives liées par empreinte, les états Git avant
et après contrôle, le refus de preuves périmées ou liées à d'autres versions et
un manifeste coordonné de préparation. Le [guide de livraison](../organisation/preparer-livraison.md)
distingue préparation, déploiement et recette de la cible.

La CI backend comprend des tests PostgreSQL et une compatibilité démonstration
avec migrations et restauration. Live dispose d'un [harnais navigateur](../../../localeo-marketplace/scripts/visual-run-context.cjs)
avec sorties propres à chaque exécution et diagnostics CI. Pro exécute aussi
Playwright et Lighthouse. Animation possède déjà de nombreuses recettes
navigateur réutilisables.

Les onze skills ont des responsabilités identifiées. Le [cycle d'epic](../organisation/cycle-epic.md)
définit la reprise et un protocole d'évaluation. La roadmap distingue également
les clôtures historiques des extensions ouvertes : la réserve GL-16 apparaît
dès le début de la [roadmap commune](../roadmap/README.md).

## 4 Constats confirmés et recommandations

P1 désigne ici une correction à traiter en premier en raison d'une garantie
d'exécution ou d'une preuve critique manquante. P2 désigne une amélioration
importante et ciblée. P3 relève de l'entretien ou d'un besoin conditionnel.
Ces priorités ne constituent pas une mesure d'incidents observés en production.
Les identifiants F01 à F13 servent uniquement à relier les constats aux lots.

### F01 Une configuration PostgreSQL héritée peut détourner le runner audit

**Priorité P1 sur un poste opérateur — lot 1.** Le
[runner audit Animation](../../../localeo-backend/scripts/validation/run_animation_audit_tests.py)
fixe certaines URL mais conserve `LOCALEO_AUDIT_POSTGRES_URL`. La
[fixture financière](../../../localeo-backend/tests/security/test_animation_finance_tenant.py)
privilégie cette variable. Son filtrage de `socket.connect` ne couvre pas les
connexions natives libpq, contrairement au
[runner isolé principal](../../../localeo-backend/scripts/validation/test_isolated.py).

Une expérience avec une URL fictive confirme que la variable reste intacte et
que les autres fonctions de connexion ne sont pas protégées. Aucun accès réel
indésirable n'a été constaté. Réutiliser l'isolation existante, exiger une cible
jetable explicite et neutraliser les configurations héritées qui peuvent la
remplacer.

### F02 Deux scénarios SQL annoncés ne sont pas exécutés dans une CI propre

**Priorité P1 — lots 1 et 2.** Le
[workflow audit Animation](../../../localeo-backend/.github/workflows/animation-audit.yml)
sélectionne le fichier de concurrence. Le runner fournit
`ANIMATION_TEST_DATABASE_URL`, tandis que la
[fixture concernée](../../../localeo-backend/tests/security/test_animation_validation_concurrency.py)
lit uniquement `LOCALEO_AUDIT_POSTGRES_URL` puis appelle `pytest.skip` si elle est
absente. Les deux scénarios touchés sont :

- `test_scan_attend_cloture_et_refuse_sans_modifier_la_population` ;
- `test_deux_scans_concurrents_conservent_les_deux_validations`.

Harmoniser les variables dans le lot 1, puis rendre l'exécution de ces scénarios
obligatoire dans ce job au lot 2. Les tests de domaine du même fichier ne sont
pas tous ignorés ; les skips légitimes de la suite générale restent distincts.

### F03 Le preflight peut déclencher le bootstrap en TEST ou développement

**Priorité P2 — lot 1.** Le
[preflight backoffice](../../../localeo-backend/scripts/validation/check_backoffice_preproduction.py)
importe `app.main`, qui peut appeler le bootstrap. Celui-ci peut créer ou
rattraper le schéma et insérer des données hors production. Il retourne sans
ces opérations lorsque `LOCALEO_ENV=production`. La procédure prévoit par
ailleurs une copie isolée après migrations.

Le qualificatif « non destructif » ne garantit donc pas la lecture seule en
TEST/dev. Neutraliser le bootstrap après résolution de la configuration et avant
l'import applicatif. Un simple défaut de variable d'environnement ne suffit pas
face au chargement prioritaire de `.env.local`. Une refonte complète de
l'initialisation n'est pas nécessaire pour corriger ce CLI.

### F04 Un timeout ne garantit pas l'arrêt des descendants

**Priorité P2 — lot 1.** Dans [quality.py](../../scripts/quality.py), le timeout
de `subprocess.run` termine le processus direct, puis le runner peut passer au
contrôle suivant. Un enfant synthétique a continué à écrire après cet arrêt.
Un serveur ou un build peut ainsi conserver une ressource et perturber la suite.

Gérer les processus appartenant à chaque contrôle, arrêter leurs descendants sur
timeout ou interruption et attendre leur libération. La terminaison doit rester
limitée aux ressources possédées par le runner, y compris sous Windows.

### F05 Les commandes de validation ne partagent pas toutes la même isolation

**Priorité P2 — lot 1.** Le [registre qualité](../../repositories.json) lance
les builds Pro et Animation en mode démo sans environnement synthétique
explicite. Leurs configurations Vite peuvent charger les fichiers du poste.
Le `npm test` général de Pro utilise aussi cette configuration, alors que ses
recettes navigateur et son profil ergonomie disposent déjà d'une isolation.

Réutiliser les builders isolés, préserver la sélection complète des tests Pro et
produire des sorties propres à l'exécution. Le rapport doit décrire les paramètres
publics utiles sans enregistrer les secrets hérités. Aucun appel réel indu par
les tests Pro n'a été démontré lors de l'audit.

### F06 Animation dispose de recettes navigateur hors de sa CI

**Priorité P2 — lot 2.** Le
[workflow Animation](../../../localeo-animation/.github/workflows/quality.yml)
exécute `pnpm check`, dont la sélection Node ne lance pas les recettes de
`tests/browser`. Certaines chargent Playwright depuis Marketplace. Ce couplage
documenté concerne la reproductibilité des recettes, pas le runtime produit.

Déclarer une dépendance locale verrouillée et sélectionner un socle Chromium
critique. Les recettes ERP présentent également des dépendances voisines : les
recenser dans le lot 2 et rendre autonome le parcours ERP retenu, avant une
extension progressive. Le lancement systématique de toutes les recettes à
chaque changement n'est pas justifié.

### F07 Les diagnostics et preuves applicatives sont inégalement conservés

**Priorité P2 — lot 2.** Pro produit des traces et captures Playwright mais son
[workflow](../../../localeo-commercant/.github/workflows/frontend-quality.yml)
téléverse surtout les résultats Lighthouse. Certains jobs backend n'émettent pas
de résultat structuré conservé. Le standard transverse existe déjà.

Conserver les diagnostics pertinents, même en cas d'échec, et les rattacher au
rapport qualité avec versions, commandes, scénarios et empreintes. Un rapport
local ignoré ne doit pas devenir la seule pièce d'une livraison vérifiable.

### F08 Les contrats sont contrôlés partiellement sans dérive Pro démontrée

**Priorité P2 — lot 2.** Les tests frontend vérifient des opérations et schémas
contre leurs contrats embarqués. La comparaison locale confirme l'identité du
contrat canonique E41 et de sa copie Animation. Les douze chemins supplémentaires
absents de la copie Pro concernent les parcours organisateur ou Live ; ils ne
démontrent pas une API Pro manquante.

Automatiser la comparaison des opérations et schémas réellement consommés,
y compris les types, champs requis, enums et réponses importants. Préserver les
contrats embarqués ; ne pas exiger l'identité de fichiers complets dont les
périmètres ou annotations peuvent différer légitimement.

### F09 Les procédures comportent une dette de contenu et de classement

**Priorité P2 — lot 3.** Les 39 sous-échecs se décomposent en 18 absences dans
les catalogues spécialisés, 20 documents au plan non conforme et une assertion
juridique obsolète. Les deux premiers groupes concernent ensemble 20 documents.
Les 18 documents sont présents dans l'index général.

La dette dépasse le cosmétique : le lecteur ERP extrait notamment la rubrique
« Problèmes traités » pour résumer les procédures. Toutefois, l'absence d'une
rubrique ne démontre pas que tout le contenu métier est faux. Des documents
possèdent déjà des instructions et diagnostics utiles à préserver.

Deux erreurs opérationnelles passent en premier :

- le [README Pro](../../../localeo-commercant/README.md) prescrit un export de
  trois moteurs qui omet `JUSTE_PRIX_LOCAL`, pourtant reconnu par le registre et
  les tests actuels ;
- la [procédure juridique](../exploitation/technique/publier-documents-juridiques.md)
  décrit encore les PDF comme sources du backend et donne un chemin absent de
  ce dépôt, alors que les sources canoniques sont dans `localeo-projet`.

Le [test juridique](../../tests/test_legal_corpus.py) attend trois documents en
version 1.1 ; le contrat commerçant est passé à cette version dans le commit
`9cde5ff4ff764c962320d5dbd16c2a6d0233c808`. Corriger l'attendu avec cette
provenance, sans modifier le PDF ou le catalogue pour satisfaire le test.

### F10 Le contrôle historique du workspace ne décrit plus son état courant

**Priorité P3 — lot 3.** [check_workspace.py](../../scripts/check_workspace.py)
traite encore les destinations de la migration du 18 septembre comme des chemins
actuels obligatoires. Dix destinations ont disparu depuis. Son inventaire ancien
des liens n'a pas le même périmètre ni le même parseur que `check_guidance.py`.

Séparer l'intégrité des cinq racines Git de la vérification historique. Corriger
ou contextualiser les trois références historiques cassées sans recréer des
documents retirés ni effacer la provenance des audits. Les 492 références de
l'ancien inventaire ne doivent pas être annoncées comme 492 liens cassés avérés.

### F11 Les hooks ont des limites précises pour les worktrees et le staging

**Priorité P2 ou P3 selon l'usage — lot 4.** L'
[installateur](../../scripts/install_hooks.py) configure un chemin absolu partagé
par les worktrees. Il refuse toutefois de remplacer des hooks existants : aucun
écrasement silencieux n'a été reproduit. La disparition du checkout initial peut
rendre ce chemin indisponible. Le hook de contexte suppose la topologie de dépôts
frères documentée ; il accepte bien un `.git` fichier.

Le pré-commit lit les données indexées, mais exécute les contrôleurs présents sur
disque. Le cas à traiter est celui d'un contrôleur partiellement indexé dont une
modification locale masque un défaut de la version commitée. Choisir une solution
limitée à ce cas et tester le montage worktree réellement supporté.

### F12 Les évaluations des skills doivent être actualisées

**Priorité P3 — lot 4.** Un protocole de cinq cas est déjà défini dans le cycle
d'epic. Les preuves disponibles ne couvrent pas toutes les évolutions récentes
des onze skills. Le validateur contrôle les fiches, TOML et hooks, mais pas toutes
les métadonnées YAML maintenues.

Rejouer le protocole, le compléter sur les autorisations déjà données et les
reprises, et conserver les observations. Vérifier légèrement les métadonnées
existantes. Le silence du hook de fin sur un arbre propre est un comportement
intentionnel, pas un défaut à corriger ; sa portée reste consultative.

### F13 La concentration du code appelle un entretien progressif

**Priorité P3 — hors chantier immédiat.** Certains fichiers backend et frontend
concentrent de nombreuses responsabilités. La taille seule ne démontre ni une
violation métier ni un gain certain à les découper. Prioriser les extractions
selon les changements répétés, les régressions et la difficulté des tests.
Renforcer le typage par module lorsque cela améliore une évolution concrète.

## 5 Détail des quatre lots à implémenter

### Lot 1 Fiabiliser l'exécution des contrôles

**État : à implémenter.** Constats : F01, F02 pour la configuration, F03, F04 et
F05. Dépôts : Projet, Backend, Pro et Animation. Dépendance : aucune.

L'objectif est de rendre explicites les cibles, l'environnement et les ressources
possédées par chaque contrôle. Une commande qui échoue ou est interrompue doit
laisser un état déterminé avant la commande suivante.

| Travail | Périmètre principal | Preuve attendue |
| --- | --- | --- |
| Réutiliser l'isolation backend commune et valider la cible jetable | Runners de validation et fixtures audit Animation | Une URL héritée fictive ne remplace pas la cible autorisée ; les voies de connexion sont couvertes. |
| Harmoniser les variables et les exemples de commande | Fixtures financières et concurrence, invocation CI et README nécessaires | Le job transmet la même cible que celle lue par les fixtures. |
| Neutraliser le bootstrap du preflight après chargement de configuration | CLI preproduction et test associé | Toute tentative de bootstrap fait échouer le test ; le contrôle nominal reste opérationnel. |
| Nettoyer les descendants possédés après timeout ou interruption | `scripts/quality.py` et ses tests | L'enfant synthétique ne poursuit plus son travail ; le contrôle suivant démarre après libération. |
| Isoler les builds Pro et Animation et Vitest Pro général | Builders existants, configuration Vitest et registre qualité | Un environnement fictif contaminé ne change pas les cibles ; toute la sélection de tests reste présente. |
| Attribuer une sortie distincte par exécution | Répertoires de build et rapports concernés | Deux tentatives ne se remplacent pas et ne réutilisent pas un build étranger. |

**Critères d'acceptation :**

- L1-01 : une configuration opérateur héritée ne peut pas détourner l'audit vers
  une autre base ; une cible invalide est refusée avant toute connexion.
- L1-02 : le preflight n'exécute aucun bootstrap, même avec une configuration
  locale qui l'aurait normalement activé.
- L1-03 : après timeout ou interruption, aucun descendant possédé par le contrôle
  ne continue à servir ou écrire ; l'arrêt ne touche aucun processus étranger.
- L1-04 : les builds et tests concernés fonctionnent sans fichier privé et
  conservent leur sélection fonctionnelle complète.
- L1-05 : les rapports conservent les échecs et interruptions, sans secret ni
  affirmation de succès fondée uniquement sur la fin du processus parent.

**Validation :** reproductions minimales avant correction lorsque possible,
tests d'isolation et de processus, tests des runners, suite Pro concernée et
builds synthétiques des deux applications. Vérifier les branches Windows et
Linux avec preuves distinctes ; une exécution Windows ne certifie pas Linux.

**Livrables :** correctifs et tests, commandes documentées cohérentes, bilan des
versions et résultats. Aucun changement de modèle métier ni migration n'est
attendu. Si l'invocation CI doit changer pour rester fonctionnelle, l'adapter dans
ce lot ; l'élargissement de couverture appartient au lot 2.

### Lot 2 Compléter la couverture continue et conserver les diagnostics

**État : à implémenter.** Constats : F02 pour l'exécution obligatoire, F06, F07 et
F08. Dépôts : Backend, Animation, Pro et Projet ; Marketplace sert de référence
et n'est modifiée que si un consommateur réel l'exige. Dépendance : lot 1 pour
les runners et configurations communs.

| Travail | Périmètre principal | Preuve attendue |
| --- | --- | --- |
| Rendre les deux scénarios de concurrence obligatoires | Job audit Animation, rapport de tests | Les deux identifiants sont présents et exécutés ; leur skip fait échouer ce profil. |
| Compléter la sélection SQL selon les invariants sensibles | Jobs PostgreSQL existants | Tableau des invariants, tests retenus et couverture indirecte déjà apportée par la démonstration. |
| Vérifier un schéma réellement migré pour les scénarios qui en dépendent | Fixtures et migrations sur base jetable | Les contraintes ou index nécessaires au scénario sont ceux de la version livrée, et pas seulement d'un `create_all`. |
| Rendre les recettes Animation autonomes | Dépendance Playwright verrouillée, commande et build isolé | Une installation propre d'Animation suffit à rejouer le profil navigateur. |
| Ajouter un socle Chromium CI | Navigation, Lots et remises, session et PWA | Une régression significative de chaque parcours sélectionné fait échouer le job. |
| Recenser et raccorder le parcours ERP pilote | Dépendances navigateur backend et recette retenue | Commande autonome et scénario explicite ; les autres recettes restent identifiées comme hors sélection. |
| Conserver les diagnostics Pro et les résultats structurés utiles | Upload des traces, captures et résultats backend | Les artefacts sont publiés même si le contrôle échoue. |
| Raccorder les artefacts au runner transverse | Rapports applicatifs et qualité | SHA, commande, scénarios, résultat et empreinte de l'artefact sont retrouvables. |
| Vérifier les contrats effectivement consommés | Générateurs et tests consommateurs existants | Une incompatibilité pertinente est détectée ; une différence extérieure au périmètre ne bloque pas artificiellement. |

**Critères d'acceptation :**

- L2-01 : les deux scénarios SQL de concurrence passent sans skip dans leur job
  obligatoire ; leur absence ou non-exécution est détectée.
- L2-02 : le profil Chromium Animation fonctionne sur une installation propre
  et ses tests négatifs démontrent que les erreurs ne sont pas masquées.
- L2-03 : les échecs Pro et backend concernés laissent des diagnostics
  récupérables et reliés à la bonne révision.
- L2-04 : les invariants retenus sont associés à des preuves adaptées ; les
  profils de charge lourde ou exclus sont nommés sans être présentés comme joués.
- L2-05 : les contrôles contractuels couvrent les opérations et schémas
  consommés, y compris les changements incompatibles de types ou de réponses.
- L2-06 : les rapports et artefacts sont transportables vers un autre poste,
  avec leurs références et empreintes vérifiables.

**Validation :** PostgreSQL jetable préparé par migrations pour les profils
concernés, navigateur sur API synthétique, essais d'échec contrôlé pour vérifier
la collecte de diagnostics, comparaison contractuelle positive et négative.
L'exécution des workflows après publication et le paramétrage des règles GitHub
constituent une étape externe distincte des preuves locales.

**Livrables :** jobs et commandes maintenus, dépendances verrouillées,
cartographie de couverture, artefacts reliés au standard existant et bilan des
scénarios joués. Il n'est pas demandé d'exécuter toutes les recettes ou toutes
les campagnes volumétriques à chaque PR.

### Lot 3 Corriger les procédures et contenir la dette documentaire

**État : à implémenter.** Constats : F09 et F10. Dépôts : Projet et README
applicatifs concernés. Dépendance : aucune pour les corrections de contenu ;
coordonner les commandes finales avec les lots 1 et 2.

| Ordre | Travail | Résultat attendu |
| --- | --- | --- |
| 1 | Ajouter le Juste Prix à la commande d'export Pro | La procédure préserve les quatre moteurs reconnus, avec l'exclusion volontaire des moteurs non pris en charge. |
| 2 | Corriger les sources et chemins du publicateur juridique | Les exemples fonctionnent depuis le répertoire de travail annoncé et pointent vers les sources canoniques. |
| 3 | Actualiser l'assertion de version juridique | L'attendu reflète le changement versionné du contrat commerçant ; les contrôles d'empreinte restent intacts. |
| 4 | Réviser les 20 documents et compléter les 18 entrées spécialisées | Le lecteur trouve le symptôme, les prérequis, l'action, les contrôles et les conditions d'arrêt. |
| 5 | Séparer état actuel et historique des README concernés | Les commandes et comportements actuels sont lisibles sans reconstituer la chronologie. |
| 6 | Séparer vérification courante du workspace et audit de migration | Les cinq racines restent contrôlées sans exiger des documents supprimés légitimement. |
| 7 | Corriger ou contextualiser les trois références historiques | Leur provenance reste compréhensible et les liens utiles sont valides. |
| 8 | Raccorder les contrôles documentaires à la CI selon leur périmètre | Les nouveaux écarts ne peuvent plus s'accumuler silencieusement. |

La conformité au plan type doit conserver le contenu utile. Un statut ou une
date de vérification documentaire ne doit pas être présenté comme une recette
réussie sur un environnement. Ne pas ajouter des rubriques vides pour obtenir
un test vert et ne pas retirer des exigences sans décision justifiée.

**Critères d'acceptation :**

- L3-01 : les commandes prioritaires pointent vers des sources existantes et
  produisent le périmètre attendu, vérifié hors publication réelle.
- L3-02 : les tests de procédures et du catalogue juridique passent sans
  modification de complaisance des PDF, empreintes ou règles de contrôle.
- L3-03 : les catalogues spécialisés couvrent les procédures exportées et le
  lecteur ERP conserve des résumés utiles.
- L3-04 : le contrôle du workspace courant est indépendant des destinations
  historiques ; les liens documentaires modifiés sont valides.
- L3-05 : les 150 sources exportées ou leur nouveau nombre justifié restent
  vérifiées ; les lecteurs sont testés si leur contrat change.
- L3-06 : les contrôles adaptés empêchent les nouvelles régressions et les
  clôtures historiques comme les réserves actives restent inchangées.

**Validation :** tests procédures et catalogue, tests des vérificateurs modifiés,
contrôle des guides et des Markdown modifiés, sources exportées, puis suite
documentaire complète. Distinguer les skips de plateforme légitimes des preuves
requises. Vérifier les lecteurs lorsqu'un chemin ou une structure consommée
change ; un simple contrôle de liens ne suffit pas.

**Livrables :** procédures et catalogues corrigés, guides actuels clarifiés,
contrôleur de workspace ajusté, prévention des nouveaux écarts et bilan. Aucun
document historique supprimé ni nouveau statut produit inventé.

### Lot 4 Entretenir les skills et les hooks

**État : à implémenter.** Constats : F11 et F12. Dépôt : Projet. Dépendance : les
commandes et preuves finales des lots 1 à 3 pour les exemples qui les utilisent.

| Travail | Mise en œuvre attendue | Preuve attendue |
| --- | --- | --- |
| Rejouer les cinq cas du protocole existant | Exercices contrôlés avec sources minimales et sans action externe réelle | Résultats observés, version des skills, écarts et reprises consignés. |
| Compléter les cas manquants | Autorisation de commit déjà donnée, reprise, preuve périmée et changements étrangers | Décisions conformes à la demande, conservation des travaux et absence de clôture sans preuve. |
| Supporter explicitement le montage worktree retenu | Installation et découverte documentées, préservation des hooks existants | Deux worktrees testés, chemins avec espaces et indisponibilité du checkout initial. |
| Traiter les contrôleurs partiellement indexés | Contrôle ciblé de cohérence ou exécution de la version indexée, selon la solution minimale retenue | Une réparation non indexée ne masque pas un contrôleur indexé invalide. |
| Vérifier les métadonnées réellement maintenues | Cohérence des YAML existants, fiches et profils attendus | Des fixtures invalides sont détectées sans imposer des fichiers optionnels à tous les skills. |
| Conserver la portée consultative des hooks | Documentation de ce qu'ils observent et de ce qu'ils ne prouvent pas | Les tests du hook de fin et les limites annoncées restent cohérents. |

**Critères d'acceptation :**

- L4-01 : les cas représentatifs sont effectivement joués et leurs résultats
  séparés de la simple validation syntaxique.
- L4-02 : une installation dans un worktree ne dégrade pas les autres
  installations ni un gestionnaire de hooks existant.
- L4-03 : les contrôleurs partiellement indexés sont traités explicitement,
  sans modifier automatiquement l'index utilisateur.
- L4-04 : les métadonnées prises en charge sont documentées et contrôlées.
- L4-05 : le hook de fin reste consultatif et ne transforme pas un arbre propre
  en preuve de tests, de commit, de push ou de déploiement.

**Validation :** tests unitaires de configuration et hooks, vrais dépôts Git
temporaires avec worktrees, cas indexé/non indexé, exercices de workflow et revue
indépendante de leurs résultats. La confiance native des hooks reste un état de
l'hôte, distinct de ces vérifications.

**Livrables :** corrections ciblées, protocole enrichi si nécessaire, bilan
d'évaluation daté et guide d'utilisation actualisé. Aucun nouveau registre
produit, agent permanent ou hook de fin bloquant n'est requis.

## 6 Organisation de la réalisation et des commits

| Étape | Travail possible | Condition de passage |
| --- | --- | --- |
| A | Lot 1 et contenu documentaire prioritaire du lot 3 en parallèle | Fichiers et ressources attribués ; aucune dépendance implicite entre builds. |
| B | Lot 2 sur les runners stabilisés | Les garanties du lot 1 sont testées ; les commandes utilisées sont disponibles. |
| C | Finalisation du lot 3 | Les procédures décrivent les commandes finales et leurs contrôles. |
| D | Lot 4 | Les exercices utilisent les versions et preuves consolidées. |

La demande d'un commit par lot s'applique **dans chaque dépôt affecté** : les
cinq historiques sont indépendants. Un lot transverse peut donc produire
plusieurs commits, associés par le même numéro de lot et un bilan commun. Ne
pas créer de Git parent et ne pas mélanger les changements de lots différents
dans un même commit.

Pour chaque lot, conserver la liste des fichiers, les versions de départ, les
résultats, les ressources encore actives et le prochain geste selon la note de
reprise du cycle d'epic. L'agent principal intègre les travaux et vérifie les
écarts ; deux agents ne partagent pas un même répertoire de build ou une même
base de recette.

Un lot est terminé lorsque ses critères applicables sont vérifiés, son diff est
relu, ses commandes et impacts sont documentés et ses commits sont identifiés.
Un échec, un skip requis ou une vérification indisponible reste explicite et ne
peut être transformé en réussite par la seule présence d'un fichier de CI.

Les changements attendus concernent les outils, les tests et la documentation.
Ils n'impliquent aucune migration de données métier, activation de fonctionnalité
ou réparation de base TEST. Commit, push, configuration GitHub, activation des
hooks et déploiement restent des opérations distinctes selon la demande en cours.

## 7 Périmètres différés

- La refonte générale de `admin.py`, des grandes routes ou des composants
  frontend reste progressive et rattachée à des évolutions concrètes.
- Le durcissement global du typage attend une sélection de modules et des
  bénéfices vérifiables ; il ne doit pas bloquer les corrections prioritaires.
- Les campagnes de capacité complètes et les recettes sur appareils physiques
  restent suivies dans les spécifications concernées. Ces quatre lots ne lèvent
  pas implicitement GL-16, LA-16 ou les autres réserves produit.
- Les paramètres effectifs des services hébergés, protections de branche et
  confiance native des hooks seront vérifiés lors de leur mise en service.

## 8 Annexe documentaire à traiter dans le lot 3

Les 20 documents suivants constituent l'union des écarts de format et de
catalogue. Tous sont exportés vers les lecteurs ERP. Dix-huit manquent dans
leur catalogue spécialisé ; aucun de ces dix-huit n'est absent de l'index général.

| Document | Plan type à compléter | Catalogue spécialisé à compléter |
| --- | --- | --- |
| [Provisionner les référentiels](../exploitation/technique/provisionner-referentiels.md) | Oui | Oui |
| [Sessions administration](../exploitation/technique/sessions-administration.md) | Oui | Oui |
| [Publier les documents juridiques](../exploitation/technique/publier-documents-juridiques.md) | Oui | Non |
| [Communiquer avec les participants](../exploitation/exploitation/communiquer-participants-animation.md) | Oui | Oui |
| [Corriger les accents](../exploitation/exploitation/corriger-accents-contenus-animation.md) | Oui | Oui |
| [Créer une offre Animation](../exploitation/exploitation/creer-offre-animation.md) | Oui | Oui |
| [Désactiver l'antivirus documentaire](../exploitation/exploitation/desactiver-antivirus-documentaire.md) | Oui | Oui |
| [Gérer les accès Animation](../exploitation/exploitation/gerer-acces-animation.md) | Oui | Oui |
| [Gérer les bons numériques](../exploitation/exploitation/gerer-bons-numeriques-animation.md) | Oui | Oui |
| [Gérer les souscriptions](../exploitation/exploitation/gerer-souscriptions-animation.md) | Oui | Oui |
| [Gérer les tirages libres](../exploitation/exploitation/gerer-tirages-libres-animation.md) | Oui | Oui |
| [Importer les commerçants](../exploitation/exploitation/importer-commercants-animation.md) | Oui | Oui |
| [Localeo Ops](../exploitation/exploitation/localeo-ops.md) | Oui | Oui |
| [Localeo Support](../exploitation/exploitation/localeo-support.md) | Oui | Oui |
| [Menu Animation ERP](../exploitation/exploitation/menu-animation-erp.md) | Oui | Oui |
| [Parcours de la plateforme Animation](../exploitation/exploitation/parcours-plateforme-animation.md) | Oui | Oui |
| [Préparer une chasse accompagnée](../exploitation/exploitation/preparer-chasse-accompagnee.md) | Oui | Oui |
| [Profil de facturation Localeo](../exploitation/exploitation/profil-facturation-localeo.md) | Oui | Oui |
| [Reprise des commissions](../exploitation/exploitation/reprise-commissions.md) | Oui | Oui |
| [Exploiter le SaaS Animation](../exploitation/exploitation/exploiter-saas-animation.md) | Oui | Non |

Les trois références historiques cassées se trouvent dans
[l'index Commerçant avant réorganisation](../archives/commercant/index-avant-reorganisation.md),
[l'audit Marketplace de septembre](marketplace/audit-preproduction-2026-09-06.md)
et [l'audit Live du 7 novembre](marketplace/localeo-live-adhesion-ux-ui-2026-11-07.md).
Leur traitement doit préserver la distinction entre chemin historique et cible
actuelle.
