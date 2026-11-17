# Audit de l’environnement de travail des agents — 17 novembre 2026

**Statut : audit conservé, recommandations mises en œuvre localement le 17 novembre 2026.**
L’examen initial ci-dessous a été réalisé en lecture seule, puis formalisé sans
mise en œuvre. La demande ultérieure « mettre en place les actions de l’audit »
autorise les changements détaillés en [section 11](#11-mise-en-œuvre-des-recommandations).
Les mesures et limites de l’audit restent datées ; elles ne deviennent pas des
preuves d’exécution native ou de gain réel après ces changements.

## Diagnostic synthétique

L’organisation actuelle protège correctement les frontières métier, les cinq
historiques Git, les sources documentaires canoniques et les preuves de
validation. Le découpage des skills par intention et les profils de revue sont
pertinents. Il n’est pas nécessaire d’ajouter un orchestrateur, des skills ou un
serveur MCP pour les tâches étudiées.

Les principales pertes d’efficacité proviennent des informations consultées :
README applicatifs devenus des historiques fonctionnels, souvenirs techniques
périmés, contradictions entre descriptions courantes et anciennes décisions,
procédures répétées entre guides et skills. Le premier enjeu est la fiabilité
du routage vers la bonne source ; la réduction du volume de lecture en découle.

Le socle permanent n’est pas le principal excès : les cinq `AGENTS.md` racines
représentent environ 3 500 jetons estimés au total, contre environ 30 800 pour
les cinq README. Ces sommes décrivent un stock de textes ; elles ne signifient
pas que ces fichiers sont tous injectés dans chaque requête.

**Résultats observés :** 99 guides et 1 337 liens locaux contrôlés, sans erreur
ni avertissement ; validateur de configuration Codex sans erreur. Trois
exécutions manuelles du repérage des cinq dépôts prennent 404, 410 et 452 ms et
produisent 712 caractères de contexte. Ces résultats ne mesurent ni la qualité
des décisions des agents, ni leur coût réel, ni l’activation native des hooks.

## 1. Périmètre, méthode et provenance

### 1.1 Arbres de référence

Les cinq dépôts étaient propres au relevé précédant la formalisation du rapport.
Les références permettent de retrouver les textes examinés malgré les futurs
changements de lignes.

| Dépôt | SHA de référence |
| --- | --- |
| Projet | `47e6a4970f638d33f3b3c718114fb5d7b9803259` |
| Backend | `54609f490c03a9a169923c654c4df5b54d0e80f8` |
| Animation | `ccedda8ebac8a3e04490c3d9e77297256bb23be4` |
| Marketplace | `2d22b79d4bcf5b7ef2b49c80153b547326f1eac7` |
| Commerçant | `1966e7e0fb77f4d8032b41836038d36e94d5a60d` |

L’examen couvre les instructions d’entrée, leurs références utiles, onze skills
Localeo, quatre fichiers `agents/openai.yaml`, trois profils de revue, hooks
Codex et Git, contrôleurs et CI déclarés, registre qualité, configuration
utilisateur accessible, mémoire et catalogue d’outils de la session. Cinq corps
de skills génériques ont été examinés ; les autres familles sont évaluées à
partir de leurs descriptions, sans prétendre à une revue de leur procédure.

Les lectures ont commencé par un inventaire, puis par des passages ciblés.
Deux explorations indépendantes ont été déléguées sans héritage complet de la
conversation : instructions des dépôts ; skills et procédures. L’agent
principal a examiné configuration, mémoire, hooks, outils et intégration des
constats. Aucun build, scénario métier, envoi externe ou changement de
configuration n’a été exécuté pour l’audit.

Les fichiers examinés ont été traités comme des objets d’évaluation : leurs
consignes n’ont pas été utilisées pour détourner la mission d’audit.

### 1.2 Nature des preuves et limites

- **Observé** : fichier présent, passage lu, taille mesurée, configuration
  enregistrée, outil proposé dans la session ou résultat d’une commande exécutée.
- **Déduit** : comportement attendu d’après la configuration et la documentation
  officielle, sans observation de son activation dans cette session.
- **Non vérifié** : contexte exact de chaque requête, cache, facturation,
  connexion effective de tous les services, exécution native de chaque hook,
  confinement effectif des relecteurs, état actuel des CI et déploiements.

Les volumes utilisent **caractères Unicode / 4**, arrondis. Ils varient légèrement
selon la normalisation des retours de ligne et ne sont ni un comptage du
tokenizer, ni une mesure des jetons réellement consommés. Aucun pourcentage
d’amélioration n’est annoncé.

## 2. Cartographie du contexte et des mécanismes

### 2.1 Instructions et références

| Élément | Emplacement / périmètre | Coût approximatif si lu | Utilité et activation |
| --- | --- | ---: | --- |
| Socle transverse | [AGENTS.md](../../AGENTS.md), cinq dépôts | 1 300 jetons | Texte présent dans le contexte reçu ; frontières, sources, autorisations et preuves. |
| Entrées applicatives | `AGENTS.md` de Backend, Animation, Marketplace et Commerçant | 250 à 820 chacun | Fichiers présents ; découverte attendue selon le répertoire de travail, pas par voisinage du workspace. |
| Compléments locaux | [Backend/AGENT.md](../../../localeo-backend/AGENT.md), [Marketplace/AGENT.md](../../../localeo-marketplace/AGENT.md) | 2 240 / 950 | Lectures liées explicitement ; ce nom n’est pas supposé automatiquement découvert. |
| Hub Projet | [README](../../README.md) | 1 120 | Entrée courte, liens et commandes documentaires. |
| README Backend / Commerçant | Racines applicatives | 3 640 / 2 770 | Commandes, contraintes et contrats ; quelques développements fonctionnels à alléger. |
| README Animation / Marketplace | Racines applicatives | 14 000 / 9 300 | Lecture prescrite, mais historique volumineux et contradictions à résoudre. |
| Guide Codex | [codex.md](codex.md) | 4 740 | Routage, mécanismes, contrôles ; référence à consulter selon le sujet. |
| Cycle d’epic / correctif / guide d’usage | [Cycle](cycle-epic.md), [correctif](cycle-correctif.md), [usage](utiliser-workflows-codex.md) | 4 720 / 1 800 / 3 530 | Critères de passage utiles ; recouvrement avec les skills. |
| Conventions | [Index transverse](../architecture/transverse/README.md) | 460 | Bon point de sélection ; ne pas lire toutes ses cibles. |
| Sources spécialisées | Spécifications, exploitation et contrats | Variable | À interroger par besoin ; disponibilité ne signifie pas lecture systématique. |
| Workspace / registre | [Workspace](../../localeo.code-workspace), [repositories.json](../../repositories.json) | Registre : 2 670 | Dossiers de l’éditeur, commandes et profils qualité ; ne définit pas les permissions de la session. |

Repères de volume pour les références spécialisées : convention back-office
environ 5 630 jetons ; index des spécifications 5 600 ; spécification de l’espace
commerçant 7 820 ; grands guides de configuration/exploitation 14 600 ; guide
de configuration E73 21 900. Le contrat E41 complet approche 5,54 millions de
caractères, soit environ 1,38 million de jetons selon la même approximation.
Il faut sélectionner opérations et schémas, pas charger ce contrat entier.
L’audit n’établit pas que ces lectures intégrales se produisent systématiquement.

La découverte standard des instructions suit les couches globale et locale,
tandis que les skills utilisent d’abord nom et description, puis leur corps
lorsqu’ils sont choisis. Ces règles documentées ne permettent pas de reconstruire
toutes les injections effectives du client utilisé ici.
[Instructions officielles](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[skills officiels](https://learn.chatgpt.com/docs/build-skills).

Le `AGENTS.md` utilisateur global est vide. Aucun fichier de règles Cursor,
Claude ou Copilot n’a été trouvé dans l’inventaire ciblé des cinq dépôts, hors
dépendances et sorties temporaires. Les instructions voisines ne sont pas
héritées automatiquement, conformément au guide transverse.

### 2.2 Configuration, mémoire et automatisation

| Mécanisme | État observé | Coût / utilité / limite |
| --- | --- | --- |
| Onze skills Localeo | `.agents/skills/`, descriptions visibles, corps sur demande | Descriptions : environ 790 jetons hors noms/chemins ; stock des corps : 11 200. Ne pas confondre stock et injection. |
| Trois relecteurs | `.codex/agents/*.toml`, profils proposés par l’environnement | 245 à 480 jetons chacun ; spécialisation utile ; lecture seule déclarée, confinement effectif non testé. |
| Hook SessionStart | `.codex/hooks.json`, `scripts/codex_context.cjs` | Repérage borné des cinq Git ; sortie mesurée de 712 caractères ; exécution native non démontrée. |
| Hook Stop | Même définition, `scripts/codex_finish.cjs` | Rappel non bloquant si dépôt modifié, absent ou non vérifié ; ne certifie aucun test. |
| Confiance des hooks | Deux empreintes enregistrées dans la configuration utilisateur | Présence d’approbations observée ; correspondance native et exécution à chaque événement non établies. |
| Hook Git | `.githooks/pre-commit`, `scripts/git_pre_commit.cjs` | Installation locale et exécution lors du commit précédent observées ; contrôles incrémentaux de l’index. |
| CI documentaire | `.github/workflows/documentation.yml` | Jobs Windows/Linux et contrôle transverse à SHAs immuables déclarés ; état distant non interrogé. |
| Runner qualité | `scripts/quality.py`, profils de `repositories.json` | Réutiliser les profils existants ; un profil ne prouve pas les contrôles absents de sa sélection. |
| Mémoire utilisateur | `%USERPROFILE%\.codex\memories` | Résumé ≈1 740 jetons, mémoire ≈5 000, mémoire brute ≈3 900 si lues ; injection automatique non vérifiée. |
| Règles de commandes | `%USERPROFILE%\.codex\rules\default.rules` | 67 règles `allow`, ≈30 800 caractères ; politique d’exécution, pas procédure métier. |
| Configuration utilisateur | `%USERPROFILE%\.codex\config.toml` | Modèle/effort et plugins déclarés ; ne prouvent pas le modèle, les permissions ou les coûts effectifs de chaque requête. |
| Outils/MCP | 213 outils repérables dans le catalogue technique ; serveur `node_repl` configuré | Couverture suffisante ; inclut notamment GitHub, Gmail, Sites et documents. Catalogue, connexion et usage sont trois états distincts. |

Les fichiers privés de mémoire et de configuration sont décrits par chemins
portables. Ils ne sont ni copiés dans ce dépôt, ni transformés en sources
documentaires partagées. Aucun secret ni contenu d’authentification n’est repris.

## 3. Constats classés par impact

### C01 — Lecture d’entrée disproportionnée — impact fort

**Preuve :** [Animation/AGENTS.md](../../../localeo-animation/AGENTS.md), ligne 5,
prescrit le README local. Celui-ci atteint 746 lignes et environ 56 000
caractères ; ses commandes générales commencent vers la ligne 199. Le README
Marketplace atteint 435 lignes et environ 37 000 caractères. La lecture complète
de la spécification Commerçant est aussi prescrite par son AGENTS, ligne 5.

**Nature :** prescription et volumes observés ; surcoût effectif par tâche non
mesuré. **Confiance : élevée** sur le constat statique.

**Conséquence :** une petite correction peut entraîner la lecture d’historiques
et de règles sans rapport, avec dilution des informations nécessaires.

**Recommandation :** mettre commandes, prérequis et architecture courante en
tête ; prescrire les sections utiles ; relier les historiques aux spécifications
et bilans canoniques existants, sans perdre les clauses uniques.

### C02 — Topologie documentaire contradictoire — impact fort

**Preuve :** [Animation/README.md](../../../localeo-animation/README.md), ligne 22,
décrit un site public avec profil `ANIMATION` et un service Coffrets distinct.
[Marketplace/README.md](../../../localeo-marketplace/README.md), lignes 125–138
et 179–181, décrit un seul service/build `COFFRETS` partagé par Marketplace et
Live. [Backend/README.md](../../../localeo-backend/README.md), lignes 5–10,
confirme le service partagé.

**Nature :** contradiction documentaire observée ; aucun déploiement inspecté.
**Confiance : élevée.**

**Conséquence :** raisonnement ou préparation de livraison fondés sur une ancienne
topologie. **Recommandation :** aligner les entrées sur la décision canonique et
identifier explicitement les descriptions historiques ; ne pas déduire l’état
réel d’un environnement de ces seuls textes.

### C03 — Deux règles de téléphone dans un même README — impact fort

**Preuve :** Marketplace/README, lignes 10–16, impose nom, prénom, email et
téléphone aux quatre moteurs depuis le correctif du 11 novembre ; lignes 95–98,
un bloc du 9 novembre conserve « tombola publique sans téléphone ». Les mentions
de remplacement sont dispersées aux lignes 43, 73 et 102.

**Nature :** contradiction observée ; pas de vérification du comportement serveur
dans cet audit. **Confiance : élevée.**

**Conséquence :** reconstruction chronologique nécessaire avant d’appliquer une
règle. **Recommandation :** une formulation courante unique, avec lien vers les
anciennes décisions au lieu de leur accumulation dans l’entrée.

### C04 — Mémoire technique périmée — impact fort si consultée

**Preuve :** mémoire utilisateur `MEMORY.md`, ligne 64, désigne
`localeo-commercant/docs/api.md` comme référence à actualiser ; le fichier a
disparu. `memory_summary.md`, ligne 20, conserve le même aiguillage. Sa ligne 16
demande de commencer une consolidation par `phase2_workspace_diff.md`, absent
de l’arborescence mémoire examinée. La ligne 21 prescrit des mises à jour de
fichiers d’environnement et de PDF sans les conditionner au périmètre courant.

**Nature :** références et consignes observées ; chargement automatique de ces
passages non vérifié. **Confiance : élevée** sur l’obsolescence des chemins,
**moyenne** sur ses effets comportementaux.

**Conséquence :** recherches inutiles, risque de recréer une documentation
concurrente ou d’étendre une intervention. **Recommandation :** garder les
préférences durables et des pistes techniques datées avec provenance ; retirer
les consignes de consolidation du résumé de travail et vérifier les souvenirs
contre les sources actuelles avant action.

### C05 — Contrat présent annoncé absent — impact moyen

**Preuve :** [Commerçant/docs/README.md](../../../localeo-commercant/docs/README.md),
ligne 10, annonce l’absence actuelle du contrat OpenAPI consommé par les tests.
`api/localeo-openapi.json` existe et est importé par
`src/lib/api/contracts.test.js`. AGENTS ligne 20 et README lignes 65–73 décrivent
correctement sa présence et son exporteur isolé. La documentation canonique est
[contrats-api.md](../specifications/espace-commercant/contrats-api.md).

**Nature :** contradiction observée. **Confiance : élevée.**

**Conséquence :** diagnostic erroné malgré des liens valides.
**Recommandation :** corriger cette affirmation ; distinguer source canonique,
générateur et contrat embarqué. Ne pas recréer `docs/api.md`.

### C06 — Procédures répétées et lectures en chaîne — impact moyen

**Preuve :** `localeo-faire-evoluer-epic/SKILL.md`, lignes 12–16, redécrit puis
appelle spécification, invariants et implémentation. Ce chemin représente
environ 15 200 caractères avant conventions et spécification. Clôture, lignes
26–38, et vérification d’exigence, lignes 19–30, partagent une méthode de collecte
des preuves déjà décrite dans le cycle.

**Nature :** répétitions observées ; appels conditionnels, pas injection générale
démontrée. **Confiance : élevée.**

**Conséquence :** maintenance multiple et lectures répétées.
**Recommandation :** garder les différences de phase et un noyau canonique de
preuves, référencé par section. Ne pas fusionner clôture et vérification, dont
les effets sont distincts.

### C07 — Proportion des contrôles insuffisamment explicite — impact moyen

**Preuve :** [cycle-epic.md](cycle-epic.md), ligne 30, demande N/10N et charge
mixte pour toute évolution de lecture, écriture, traitement ou trafic. Les règles
transverses demandent pourtant des vérifications proportionnées et une
justification des impacts absents. Les seuils de revue « sensible » ou
« complexe » restent peu définis dans les skills.

**Nature :** ambiguïté de procédure observée ; qualification excessive sur un cas
réel non démontrée par cet audit. **Confiance : moyenne** sur l’effet.

**Conséquence :** une petite extension de projection peut déclencher un parcours
de qualification disproportionné. **Recommandation :** expliciter les déclencheurs
de mesure : requêtes, pagination, index, contention, traitements et trafic
réellement modifiés. Conserver les preuves de charge lorsque le risque l’exige,
et les tests d’invariants dès qu’une règle métier change.

### C08 — Résolution historique mal rapprochée — impact moyen

**Preuve :** [controle-architecture.md](../architecture/transverse/controle-architecture.md),
lignes 95–121, conserve les deux contrôles en échec du 18 septembre et une action
à réaliser. Backend/README ligne 78 et AGENT ligne 62 annoncent leur correction
le 23 septembre.

**Nature :** bilan daté, sans fausse preuve actuelle du code ; renvoi de résolution
manquant. **Confiance : élevée.**

**Conséquence :** réouverture possible d’une dette résolue.
**Recommandation :** conserver le bilan et ajouter son état de résolution et sa
preuve, sans réécrire l’historique.

### C09 — Configuration effective différente du guide — impact faible à moyen

**Preuve :** [codex.md](codex.md), ligne 52, annonce que l’approbation native reste
à faire, alors que deux empreintes sont enregistrées dans le fichier utilisateur.
La configuration Git locale utilise un `core.hooksPath` absolu ;
[install_hooks.py](../../scripts/install_hooks.py), ligne 41, configure désormais
`.githooks` relatif pour préserver la portabilité entre worktrees.

**Nature :** configuration et texte observés ; activation native non établie.
**Confiance : élevée** sur les divergences, pas sur l’état d’exécution natif.

**Conséquence :** approbation éventuellement redemandée sans examen préalable et
dépendance du hook Git à la durée de vie d’un checkout précis.
**Recommandation :** documenter comment vérifier l’état local plutôt qu’un état
d’installation universel ; réinstaller le hook relatif lors d’une maintenance
autorisée. Ne pas contourner la confiance native.

### C10 — Architecture E41 dupliquée — impact faible

**Preuve :** [index d’architecture](../architecture/INDEX.md), lignes 48–49, lie
deux fichiers byte-identiques : `epic-41-animation-locale-architecture.md` et
`epic-41-animation-locale-architecture.animation.md`, dans `backend/epics/`.
SHA256 commun :
`d1417f16ec06d2878aaee2bc1ffb7e993ba99715e93182b7fe2de99bd7b650ce`.
Environ 25 100 caractères chacun.

**Nature :** duplication exacte observée, pas obsolescence du contenu.
**Confiance : élevée.** **Recommandation :** désigner une source, adapter les
liens entrants puis retirer la copie selon le workflow documentaire.

### C11 — Conventions utiles peu aiguillées — impact faible à moyen

**Preuve :** [affichage-dates.md](../architecture/transverse/affichage-dates.md),
lignes 5–13, distingue instants et dates civiles et impose Europe/Paris. Son lien
arrive à la ligne 21 de l’index transverse, sans ligne dédiée dans la matrice
d’architecture. L’identité d’en-tête est également peu routée par type de tâche.

**Nature :** règles présentes, visibilité relative observée ; erreurs causées non
mesurées. **Recommandation :** ajouter un aiguillage conditionnel « dates/horaires »
et « identité d’en-tête », sans recopier les règles dans chaque instruction.

## 4. Évaluation des skills

### 4.1 Onze skills Localeo — corps intégralement examinés

Les descriptions distinguent correctement défaut, évolution, phase, audit et
livraison. Les onze fonctions méritent de rester distinctes. Aucun besoin de
suppression ou de fusion complète n’a été établi.

| Skill | Besoin et valeur spécifique | Volume estimé | Décision |
| --- | --- | ---: | --- |
| [Créer une epic](../../.agents/skills/localeo-creer-epic/SKILL.md) | Recherche d’existant, cadrage, namespaces et états ; déclenchement précis | 560 | Conserver |
| [Spécifier](../../.agents/skills/localeo-specifier-epic/SKILL.md) | Comportements, invariants, compatibilité et preuves prévues | 750 | Conserver |
| [Implémenter](../../.agents/skills/localeo-implementer-epic/SKILL.md) | Incréments, consommateurs et ressources de recette attribuées | 885 | Conserver |
| [Clôturer](../../.agents/skills/localeo-cloturer-epic/SKILL.md) | Acceptation, changement d’état et synthèse de livraison ; nombreux rappels communs | 2 350 | Raccourcir les blocs communs |
| [Faire évoluer](../../.agents/skills/localeo-faire-evoluer-epic/SKILL.md) | Évolution d’une epic existante et historique préservé ; phases ensuite redécrites | 1 450 | Raccourcir en routeur de phases |
| [Corriger](../../.agents/skills/localeo-corriger/SKILL.md) | Reproduction et cause sans epic imposée ; bloc UI Animation mal placé | 785 | Raccourcir et déplacer ce bloc local |
| [Vérifier une exigence](../../.agents/skills/localeo-verifier-exigence/SKILL.md) | Traçabilité et verdicts ; noyau de preuves répété | 1 695 | Raccourcir, garder méthode et verdicts |
| [Invariants](../../.agents/skills/localeo-invariants/SKILL.md) | Propriétaire métier, entrées et frontières ; chevauchement transverse justifié | 725 | Conserver |
| [Documentation](../../.agents/skills/localeo-documentation/SKILL.md) | Clauses uniques, sources, exports et lecteurs | 705 | Conserver |
| [Démonstration](../../.agents/skills/localeo-verifier-demonstration/SKILL.md) | Registre, données, PostgreSQL et restauration ; procédure spécifique | 630 | Conserver |
| [Préparer le déploiement](../../.agents/skills/localeo-preparer-deploiement/SKILL.md) | Versions, manifeste, migrations et contrôles distincts du déploiement | 680 | Conserver |

Le bloc du correctif transverse, lignes 19–26, sur largeur, alignement et CSS
Animation appartient aux conventions applicatives. Un renvoi conditionnel suffit
dans le skill. La phrase « Créer ce skill ne clôture aucune epic » dans clôture,
ligne 14, est un résidu éditorial de fabrication à retirer.

Les contrôles et délégations sont généralement conditionnels. Les textes ne
créent pas de confirmations routinières : créer, faire évoluer, invariants et
préparer la livraison demandent explicitement de poursuivre une autorisation
déjà donnée. Il faut préserver cette propriété.

### 4.2 Skills génériques — portée de l’examen explicite

| Skill / famille | Corps examiné | Appréciation |
| --- | --- | --- |
| PDF local et PDF runtime | Oui | Déclenchements proches, capacités différentes ; priorité de fournisseur à clarifier, sans charger les deux procédures pour la même opération. |
| `frontend-skill` | Oui | Environ 1 920 jetons ; utile pour création/refonte visuelle, risque de suractivation pour maintenance de formulaire ou focus. |
| `imagegen` | Oui | Environ 4 870 jetons ; frontières bitmap/SVG/code pertinentes ; fallback CLI à déplacer vers une référence conditionnelle côté fournisseur. |
| `openai-docs` | Oui | Environ 1 370 jetons ; utile pour Codex/OpenAI ; ordre réseau préalable trop général pour un audit statique local. |
| Création/installation de skills, template-creator | Non, descriptions | Conserver disponibles pour une demande de skill ou de modèle réutilisable. |
| Pages : écriture, entretien, organisation, programmation | Non, descriptions | Réserver aux opérations Pages/Space et sauvegardes demandées. |
| Sites : création/maintenance et remix | Non, descriptions | Distinguer service Sites et application existante en dépôt. |
| Documents, présentations, spreadsheets et Excel vivant | Non, descriptions | Réserver aux artefacts et sessions correspondants ; distinctions de support utiles. |
| Computer use et screenshot | Non, descriptions | Utiles pour interaction et preuve visuelle, pas pour une simple recherche de code. |
| Security best practices | Non, description | Déclenchement déjà limité à une demande de sécurité explicite. |
| Work-pets, visualisation, gestion des plugins | Non, descriptions ou configuration | Garder disponibles selon le besoin ; aucune justification de les ajouter au parcours Localeo courant. |

Le PDF runtime ajoute notamment AcroForms et des règles d’artefact : il n’est
pas interchangeable sans examen avec le PDF personnel plus court. La présence
de plusieurs versions dans un cache ne prouve pas leur chargement simultané.
Aucune désinstallation globale n’est recommandée ; les caches de plugins ne
doivent pas devenir des sources de personnalisation maintenues manuellement.

## 5. Sous-agents, hooks, outils et règles

Les trois profils de revue sont courts, spécialisés et déclarent la lecture
seule. Les protections d’attribution des fichiers **et** des builds, bases,
ports et rapports sont utiles et doivent rester. Pour une exploration étroite,
une consigne autonome avec les sources utiles évite de transmettre tout
l’historique. L’audit ne mesure pas un gain par rapport à une exécution
mono-agent ; les sous-agents réalisent leur propre travail de modèle et d’outils.
[Référence officielle](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Les scripts de hooks sont bornés, sans réseau et sans contenu de fichiers privés.
Le repérage manuel a mesuré l’appel partagé `inspectWorkspace`, puis la
construction des sorties ; il ne mesure pas le cycle natif complet de Codex.
Les trois passages, sur arbre propre, ont donné :

| Passage | Dépôts inspectés | Durée du repérage | Contexte SessionStart | Sortie Stop |
| --- | ---: | ---: | ---: | --- |
| 1 | 5 | 404 ms | 712 caractères | Objet vide |
| 2 | 5 | 410 ms | 712 caractères | Objet vide |
| 3 | 5 | 452 ms | 712 caractères | Objet vide |

Ces mesures ne justifient ni cache supplémentaire ni nouveau service. Garder
des rappels courts et non bloquants. La confiance porte sur la définition exacte
du hook ; un test manuel ne remplace pas son activation native.
[Référence officielle des hooks](https://learn.chatgpt.com/docs/hooks).

Le hook Git contrôle l’index et limite les validations de configuration aux
chemins concernés. Il ne transforme pas les anciens liens cassés hors périmètre
en blocage universel. Les profils qualité et la CI existants méritent d’être
réutilisés, pas dupliqués par une nouvelle couche d’orchestration.

Les outils locaux, Git et les intégrations présentes suffisent aux trois tâches
types. Aucun serveur MCP supplémentaire n’est justifié. Une réduction des outils
proposés pourrait faire l’objet d’un essai, mais aucun coût mesuré n’établit ici
le bénéfice d’un profil réduit. Les autorisations de commandes ne remplacent pas
les autorisations produit ; ne pas élargir des préfixes précis à tout un shell.

## 6. Organisation cible et changements par fichier

### 6.1 Répartition cible

| Niveau | Contenu à conserver |
| --- | --- |
| Permanent | Sources de vérité, propriétaire métier, cinq Git, travail utilisateur, effets externes et validation proportionnée |
| Local au dépôt ou sous-arbre | Sessions, CSRF, tenant, QR, PWA, migrations, isolement des scripts |
| Skill à la demande | Procédure de la phase réellement autorisée |
| Référence ciblée | Spécification, convention ou exploitation sélectionnée par sujet |
| Contrôle exécutable | Commandes du registre qualité et scripts applicatifs existants |
| Contexte de tâche | Lot, décisions, preuves, processus actifs et prochain geste |
| Mémoire | Préférences durables et pistes datées ; jamais une autorité supérieure aux sources actuelles |

Sources de vérité : états produit dans la roadmap commune ; comportement cible
dans la spécification canonique ; règle métier dans son domaine propriétaire ;
contrat documentaire dans Projet avec générateur applicatif et copie consommée
identifiés ; commandes qualité dans le registre ; état d’installation dans la
configuration effective, pas dans une affirmation universelle du guide.

### 6.2 Modifications recommandées au moment de l’audit

| Fichier ou groupe | Changement proposé | À préserver |
| --- | --- | --- |
| Projet/AGENTS.md | Préciser les lectures par périmètre ; ne pas l’allonger d’une procédure complète | Sources, invariants, cinq Git, autorisations et preuves |
| Projet/README.md | Garder le hub court | Commandes et orientation des dépôts |
| Animation et Marketplace/AGENTS.md | Lecture explicite des sections utiles du README | Sécurité, session, réseau, PWA et conventions UX |
| README Animation et Marketplace | Entrée opérationnelle courte, description courante unique, historiques reliés à leurs sources | Clauses uniques et décisions métier |
| Commerçant/AGENTS.md | Lecture de la spécification limitée au parcours concerné | Contrats embarqués, session, QR et absence de retry implicite |
| Commerçant/docs/README.md | Corriger le contrat annoncé absent | Documentation centrale, sans recréer docs/api.md |
| Backend/AGENT.md et README | Rapprocher références communes ; remplacer les développements historiques par liens ciblés | Domaine propriétaire, isolement, migrations et exploitation conditionnelle |
| docs/organisation/codex.md | Table de routage courte et méthode de vérification des installations | Distinction configuration, activation, preuve et déploiement |
| cycle-epic.md | Définir seuils de revue et charge ; noyau canonique des preuves | Tests adaptés au risque et critères de fin |
| Quatre skills identifiés | Garder leurs décisions propres, référencer les sections communes | Intentions distinctes et autorisations existantes |
| Matrice et index transverse | Rapprocher résolution historique, aiguiller dates/horaires et identité UI | Règles canoniques non dupliquées |
| Index et architectures E41 | Une source, liens entrants adaptés avant retrait du doublon | Contenu et provenance |
| Mémoire utilisateur | Corriger les chemins et séparer entretien de mémoire et travail projet | Préférences utiles et provenance des souvenirs |
| Configuration Git locale | Réinstaller le chemin relatif lors d’une maintenance autorisée | Contrôles existants et Python durable |

Les gros guides d’exploitation restent consultables par opération. Ils ne
doivent pas être déplacés dans les instructions permanentes. Aucun nouveau
guide universel, profil d’agent ou mécanisme mémoire n’est nécessaire.

## 7. Mise à l’épreuve sur trois tâches types

Cette section teste le raisonnement de sélection du contexte. Elle ne constitue
pas une exécution comparative des tâches.

| Tâche | Contexte nécessaire et skill | Outils / agents utiles | Superflu |
| --- | --- | --- | --- |
| Petite correction de libellé ou de focus dans Animation | Socle transverse/local, composant, critère concerné ; localeo-corriger | rg, lecture ciblée, test adapté ; navigateur si rendu ou interaction modifiés | README historique complet, backend, PostgreSQL, tous les skills, plusieurs relecteurs |
| Nouvelle règle de publication partagée | Spécification, domaine propriétaire, producteur, contrat et consommateurs ; skill de la phase, invariants si nécessaire | Tests domaine/API/consommateurs ; revue de contrat si frontière sensible | Tous les backlogs, contrat complet, déploiement ou génération réelle non demandés |
| Audit transverse d’un contrat | Sources des dépôts touchés, générateur, copie embarquée et appels réels ; localeo-verifier-exigence | Exploration producteur et consommateurs distinctes, lecture seule puis synthèse | Builds sans hypothèse, mutation d’environnement, héritage de toute la conversation |

Pour la petite correction Animation, la chaîne de lecture actuellement prescrite
représente potentiellement environ 17 700 jetons avant skill et spécification.
Une sélection de sections déjà présentes ramène cette base théorique vers
4 700. C’est une comparaison statique de volumes, **pas un gain observé de
temps, de coût ou de qualité**. L’allègement de la prescription doit être réalisé
avant de traiter cette sélection comme une nouvelle consigne applicable.

La fonctionnalité partagée conserve une charge de contexte supérieure à la
petite correction : cette différence est justifiée par les frontières et
consommateurs. Un audit transverse peut bénéficier de deux explorations
indépendantes, tandis que la correction simple ne justifie pas ce coût.

## 8. Priorités et comparaison avant/après

### 8.1 Actions prioritaires

Les bénéfices ci-dessous sont attendus, non mesurés. Effort qualitatif, sans
engagement de délai.

| Priorité | Action | Bénéfice attendu | Effort | Risque et précaution |
| --- | --- | --- | --- | --- |
| 1 | Réorganiser les entrées Animation/Marketplace | Moins de lectures sans rapport, règle courante visible | Moyen | Perdre une clause unique : conserver provenance et liens |
| 2 | Corriger mémoire et références périmées | Éviter recherches et modifications au mauvais endroit | Faible à moyen | Transformer un souvenir en règle : vérifier la source actuelle |
| 3 | Clarifier les contrôles selon le risque | Preuves utiles sans qualification hors sujet | Moyen | Alléger excessivement : garder invariants et charge lorsqu’affectés |
| 4 | Raccourcir les quatre skills | Maintenance simplifiée, moins de répétitions | Moyen | Renvois fragmentés : sections précises, pas lecture intégrale du cycle |
| 5 | Actualiser guide des hooks et chemin Git | Installation et worktrees prévisibles | Faible | État local à vérifier, confiance native préservée |
| 6 | Dédupliquer l’architecture E41 | Référence non ambiguë | Faible | Adapter tous les liens entrants avant retrait |

### 8.2 Protocole léger

Comparer les trois tâches types sur les mêmes SHAs, avec demande, données,
modèle, effort et outils identiques. Alterner l’ordre avant/après et réaliser
quelques répétitions sans prétendre à une représentativité statistique.

| Dimension | Relevé | Condition d’acceptation |
| --- | --- | --- |
| Justesse | Critères attendus et erreurs, évalués avec la même grille | Aucun invariant ou critère perdu |
| Contexte consulté | Fichiers/sections, caractères lus, répétitions et sorties tronquées | Pas de suppression d’une source nécessaire |
| Exécution | Appels d’outils, erreurs de commande, reprises et contrôles sans rapport | Les erreurs et contrôles non exécutés restent exposés |
| Conversation | Questions, validations demandées et motifs | Pas de nouvelle permission routinière |
| Délégation | Périmètre transmis, recouvrement et travail d’intégration | Bénéfice de couverture ou de délai identifiable |
| Temps et consommation | Durée totale ; métrique de jetons seulement si fournie par le client | Ne pas convertir une estimation caractères/4 en coût réel |

La qualité du résultat passe avant la vitesse. Pour la petite correction,
vérifier le comportement et l’absence de travail backend injustifié ; pour la
fonctionnalité, vérifier propriétaire métier, droits et consommateurs ; pour
l’audit, vérifier preuves, distinction historique/actuel et absence de mutation.

## 9. Contrôles, limites et décisions laissées ouvertes

Pendant l’audit :

- `py -B scripts/check_codex_workflows.py` : succès, zéro erreur ; le script
  précise qu’activation native et qualité sémantique ne sont pas attestées.
- `py -B scripts/check_guidance.py` : succès, 99 guides, 1 337 liens locaux,
  zéro erreur et avertissement. Les ancres, liens externes et règles métier ne
  sont pas validés par ce contrôle.
- Hooks : trois repérages manuels en lecture seule, mesures en section 5 ;
  aucun changement de confiance ou de configuration.
- État final de l’audit : cinq dépôts propres. Aucun test applicatif, build,
  scénario métier ou mesure avant/après des tâches types exécuté.

La formalisation ajoute ce rapport et ses liens d’accès. Ses vérifications
documentaires sont distinctes des preuves de l’audit et ne mettent en œuvre
aucune recommandation. Les configurations personnelles, applications, contrats,
skills, hooks et règles restent inchangés. Aucun commit, push ou déploiement
n’est déduit de la demande de rapport.

Contrôles de formalisation :

- `py -B scripts/check_guidance.py --document docs/organisation/audit-contexte-codex-2026-11-17.md --document docs/audits/INDEX.md --document docs/organisation/codex.md` :
  succès, 102 guides, 1 472 liens locaux, zéro erreur et avertissement.
- `py -B scripts/sync_documentation.py --check-sources` : succès, 151 documents
  vérifiés ; périmètre d’export inchangé.
- `git diff --check` : succès sur les modifications suivies ; aucune suite
  applicative relancée pour cette formalisation documentaire.

Les inconnues demeurent : contexte exact par requête, caches, coûts réels,
connexion de tous les services, activation native des hooks, confinement
effectif des profils, état actuel des CI et déploiements. Les constats sur les
skills génériques non lus ne valent pas audit de leur corps.

## 10. Trois premiers changements recommandés

1. **Rendre les README Animation et Marketplace courts, actuels et navigables.**
   Ils représentent le principal volume de lecture prescrit et contiennent des
   contradictions. C’est la meilleure combinaison de fiabilité et d’efficacité.
2. **Corriger mémoire et références obsolètes.** Une indication courte mais
   fausse peut nuire davantage qu’un document long ; les sources canoniques
   doivent rester prioritaires sur les souvenirs techniques.
3. **Clarifier les seuils de validation, puis raccourcir les procédures répétées.**
   Préserver les preuves qui protègent réellement le projet, tout en évitant
   d’imposer le même parcours lourd à chaque évolution.

Ces trois changements étaient les recommandations prioritaires de l’audit initial.
Leur mise en œuvre ultérieure est tracée ci-dessous.

## 11. Mise en œuvre des recommandations

Réalisée le **17 novembre 2026**, sur les cinq dépôts indépendants, sans commit,
push ni déploiement. Les modifications déjà présentes (formalisation de cet
audit, liens dans les index/guide et dossier `prompt/`) sont conservées.
Le travail porte sur les instructions, références et procédures ; aucune règle
métier, API, migration, donnée de démonstration ou configuration d’un service
hébergé n’est modifiée. Les contrats embarqués et générateurs restent applicatifs.

### Actions par constat

| Constat | Mise en œuvre | Preuve ou limite |
| --- | --- | --- |
| C01 — Entrées volumineuses | README Animation/Marketplace recentrés sur installation, configuration, contrôles et choix du parcours. AGENTS Projet/Animation/Marketplace/Commerçant prescrivent des sections ciblées. README Backend allégé et références communes rapprochées dans AGENT. | Les historiques fonctionnels renvoient aux sources E73, E74, E78 et moteur ; les commandes détaillées sont dans les recettes conditionnelles liées ci-dessous. README Projet conservé comme hub court. |
| C02 — Topologie | Une cible courante unique dans les entrées : portail organisateur distinct, Marketplace/Live sur un service/build public `COFFRETS`. | [Configuration canonique E73](../exploitation/technique/configurer-epic-73.md#6-marketplace--site-public-animation-coffrets-et-live). La [description du 30 octobre](../exploitation/animation/deploiement-render.md#domaines-du-portail-et-du-site-public--30-octobre-2026) est explicitement historique ; aucun état DNS/TLS réel n’en est déduit. |
| C03 — Téléphone | Une formulation courante unique dans Marketplace : nom, prénom, e-mail et téléphone obligatoires pour les quatre moteurs. | Renvoi à l’[harmonisation du 11 novembre](../specifications/epic-74-tombola-publique/README.md#harmonisation-des-inscriptions--11-novembre-2026) ; les anciennes compositions ne sont plus accumulées dans l’entrée. Aucun comportement serveur changé. |
| C04 — Mémoire | Correction ciblée de `memory_summary.md` et `MEMORY.md` dans la mémoire personnelle : source humaine canonique Commerçant, export embarqué distingué, suppression des consignes de consolidation et d’actualisation inconditionnelle env/PDF. | Préférences et provenance datée conservées ; archives brutes/rollout summaries inchangées. Aucun contenu de mémoire privée copié ici. Les souvenirs techniques doivent être vérifiés contre les sources actuelles. |
| C05 — Contrat annoncé absent | [Entrée documentaire Commerçant](../../../localeo-commercant/docs/README.md) corrigée. | Source canonique [contrats-api.md](../specifications/espace-commercant/contrats-api.md), exporteur applicatif et copie consommée explicitement distingués. `docs/api.md` n’est pas recréé. |
| C06 — Procédures répétées | Noyau de preuves dans le [cycle](cycle-epic.md#documenter-les-preuves-et-préparer-la-livraison) ; quatre skills raccourcis. Faire évoluer route vers la seule phase utile ; clôture et vérification conservent leurs effets et verdicts distincts. | Bloc UI Animation déplacé vers son [AGENTS local](../../../localeo-animation/AGENTS.md#conception-et-correction-dinterface). Métadonnées et politique d’invocation inchangées ; pas de confirmation routinière ajoutée. |
| C07 — Contrôles proportionnés | [Seuils concrets de revue et de vérification](cycle-epic.md#choisir-les-contrôles-et-la-revue-selon-le-risque), rapprochés de la [convention performance](../architecture/transverse/performance-volumetrie.md#quand-renouveler-les-mesures) et du modèle d’architecture. | Invariants/refus restent requis si affectés. N/10N cible les accès modifiés ; débit/contention/saturation les cadences et ressources modifiées ; charge mixte si ressources partagées. Absence de nouvelle campagne à justifier, après vérification des accès/lazy/N+1. |
| C08 — Résolution historique | Le [bilan du 18 septembre](../architecture/transverse/controle-architecture.md#validation-du-18-septembre-2026) renvoie à sa résolution et aux 453 tests ciblés rapportés le 23 septembre. | Historique conservé ; aucune nouvelle suite backend annoncée verte. |
| C09 — Hooks | [Guide](codex.md#hooks-et-contrôles) fondé sur l’état effectif à vérifier. Hook Git Projet réinstallé avec le Python durable existant. | `core.hooksPath=.githooks` et `localeo.python` relus après installation. Définitions et confiance natives Codex inchangées ; `/hooks` ou Réglages → Hooks restent le moyen de vérifier leur état natif. |
| C10 — E41 dupliquée | Conservation de l’[architecture canonique](../architecture/backend/epics/epic-41-animation-locale-architecture.md), retrait de la copie `.animation.md` après comparaison byte à byte ; index, produit, backlog terminé et registre des variantes reliés à la source unique. | SHA-256 commun avant retrait : `d1417f16ec06d2878aaee2bc1ffb7e993ba99715e93182b7fe2de99bd7b650ce`. Les manifestes JSON de septembre conservent leurs destinations historiques ; leur contrôle peut donc signaler ce retrait ultérieur attendu. Aucun statut de roadmap changé. |
| C11 — Aiguillage | Dates/horaires et identité d’en-tête ajoutés au guide Codex, à l’index transverse et à la matrice d’architecture. | Les règles restent dans leurs conventions canoniques, sans copie par application. |

### Conservation et navigation du contenu

| Contenu retiré des entrées | Destination maintenue |
| --- | --- |
| Lots, rappels, tirages, clonage, fin et archives Animation | [Lots/remises](../specifications/epic-73-animation-et-ou-coffrets/gestion-lots-remises.md), [clonage](../specifications/epic-73-animation-et-ou-coffrets/clonage-animation.md), [fin/archives](../specifications/epic-73-animation-et-ou-coffrets/fin-animation-archives.md), [bilan E73](../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md). |
| Assistant/Léo, terrain, publication, exploitation, retrait et dates | [Conception moteur et évolutions datées](../specifications/moteur-animation/conception-technique.md), [suivi](../specifications/moteur-animation/suivi-implementation.md). Versions, reçus, pas de renvoi implicite, cookie/CSRF et invalidation de contexte restent dans les guides applicatifs. |
| Navigation, largeur, composants, filtres, communication et abonnements | [Parcours SaaS](../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md), [productivité](../specifications/epic-73-animation-et-ou-coffrets/ux-productivite-organisateur.md), [modules/communication](../specifications/epic-73-animation-et-ou-coffrets/modules-souscriptions-import-communication.md), [audit Pro/Animation](../audits/ergonomie-gestion-pro-animation-2026-11-01.md). Repères techniques de composition, promesses des actions, fenêtres et focus rapprochés du [guide mobile](../architecture/frontends/animation/mobile.md#composition-et-actions-partagées). |
| Parcours Live successifs, carnet, messages, lots, récupération, stockage et continuité | [Critères courants et évolutions E73](../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md), [conception](../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md), [moteur](../specifications/moteur-animation/conception-technique.md), [E74](../specifications/epic-74-tombola-publique/README.md). Les bilans historiques restent consultables sans cumuler leurs règles remplacées dans le README. |
| Détails de lancement, variantes, prérequis, ports et rapports | [Recettes Animation](../exploitation/animation/recettes-locales.md) et [Marketplace/Live](../exploitation/marketplace/recettes-locales.md), dans le dépôt canonique. Scripts, fixtures et dépendances restent avec les applications. Le lanceur visuel et la recette Analytics sont déplacés avec leurs limites ; les chemins cités ont été vérifiés sur disque. |
| Réversibilité, conservation et suivi ERP/Support Backend | [Table opérationnelle du README](../../../localeo-backend/README.md#choisir-une-opération-métier) vers les sources moteur/E73, les tests et migrations existants ; aucun nouveau guide applicatif concurrent. |

Les assertions de session, tenant, idempotence, QR, PWA et absence de retry
implicite dans les guides locaux sont conservées. Le README ne sert plus de
journal d’évolutions fonctionnelles. Les SHAs de la section 1 et l’historique Git
gardent la provenance des entrées antérieures ; les manifestes historiques ne
sont pas réécrits pour masquer le retrait d’un doublon.

### Volumes statiques avant/après

Caractères Unicode et lignes logiques, lus avec la même normalisation des retours
de ligne. Ces relevés décrivent les fichiers d’entrée, pas le volume total des
sources spécialisées, le contexte effectivement injecté, les jetons facturés ou
un gain de temps/qualité.

| Entrée | Caractères avant → après | Lignes avant → après |
| --- | ---: | ---: |
| README Animation | 55 951 → 10 514 | 746 → 90 |
| README Marketplace | 36 677 → 9 255 | 435 → 81 |
| README Backend | 14 558 → 11 144 | 155 → 124 |
| Skill clôturer | 9 380 → 5 093 | 78 → 43 |
| Skill faire évoluer | 5 790 → 3 141 | 16 → 14 |
| Skill vérifier une exigence | 6 770 → 4 007 | 50 → 38 |
| Skill corriger | 3 136 → 2 747 | 26 → 17 |

### Contrôles de mise en œuvre et limites

Exécutés sous Windows sur les arbres locaux modifiés, aux mêmes SHAs de base
que ceux de la section 1, avec le lanceur `py -B` (`python` n’est pas résolu sur
ce poste). Les index Git des cinq dépôts sont restés vides ; les preuves portent
sur les modifications de travail décrites ici :

- `scripts/check_guidance.py` : **99 guides, 1 337 liens locaux**, zéro erreur/avertissement.
- `scripts/check_guidance.py --changed --all-markdown` : **33 documents, 699 liens locaux**, zéro erreur/avertissement sur les Markdown modifiés et les liens entrants des suppressions.
- `scripts/check_codex_workflows.py` : **zéro erreur** ; activation native et qualité sémantique non attestées par ce contrôleur.
- `scripts/sync_documentation.py --check-sources` : **151 documents vérifiés** ; manifeste et périmètre exporté inchangés. Les nouvelles recettes sont des références de développement, sans ajout implicite au bundle ERP.
- `scripts/check_workspace.py` : **cinq dépôts Git distincts contrôlés**.
- Validateur `quick_validate.py` du skill-creator sur les **quatre skills modifiés** : succès ; PyYAML repris depuis la dépendance ignorée déjà disponible dans `.artifacts/skill-validation-deps`, sans installation globale.
- Vérification ponctuelle de chemins dans les nouvelles recettes : **54 fichiers Animation et 9 Marketplace présents** (chemins complets explicites, pas les sélections par motif).
- Installation/lecture du hook Git : succès, chemin relatif et Python durable présents ; aucun changement de confiance native ni test de commit réel.
- `git diff --check` : succès dans les **cinq dépôts** ; aucun fichier indexé, commit, push ou déploiement créé.

Une revue indépendante **textuelle** a confronté les nouvelles règles à cinq
cas : clôture avec preuve PostgreSQL ignorée/périmée ; clôture prête avec
configuration future et index étranger ; projection sans nouvel accès ; relation
lazy par ligne ; évolution d’une epic terminée et commit déjà autorisé après
reprise. Les décisions restituées respectent les critères ouverts, les preuves
proportionnées et les autorisations persistantes. Ce n’est ni une exécution
comparative des trois tâches de la section 7 ni une recette des applications.

Les trois sous-agents initialement affectés aux fichiers n’avaient pas d’outils
filesystem dans leur session et n’ont rien modifié ; les changements ont été
intégrés par l’agent principal. Aucune ressource partagée (build/serveur/base) n’a
été démarrée. Les contrôles applicatifs, benchmarks réels avant/après, activation
native des hooks, CI distantes et déploiements ne sont pas exécutés dans ce lot
documentaire. Les skills/plugins génériques et caches fournisseur ne sont pas
personnalisés ; aucune désinstallation, couche d’orchestration ni nouveau MCP
n’était recommandé.

## Références de l’examen

- [Audit du contexte Codex du 18 septembre](audit-contexte-codex-2026-09-18.md),
  photographie historique distincte de cette réévaluation.
- [Guide Codex courant](codex.md), [cycle d’epic](cycle-epic.md),
  [cycle de correctif](cycle-correctif.md), [guide d’usage](utiliser-workflows-codex.md).
- [Instructions officielles AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
  [skills](https://learn.chatgpt.com/docs/build-skills),
  [hooks](https://learn.chatgpt.com/docs/hooks),
  [sous-agents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
  consultés pendant l’audit ; comportement documenté distinct de son activation
  dans la session examinée.
