# Utiliser Codex dans le workspace Localeo

Ce guide décrit le fonctionnement local des cinq dépôts. Les [règles transverses](../../AGENTS.md) restent la référence ; les états produit viennent de la [roadmap](../roadmap/README.md). L'[audit du 18 septembre 2026](audit-contexte-codex-2026-09-18.md) conserve les constats et les validations de cette mise en place.

Commencer par le [guide d'usage développement et correctif](utiliser-workflows-codex.md) pour les demandes types, les résultats attendus et la reprise d'une tâche. Le [cycle d'epic](cycle-epic.md), le [cycle de correctif](cycle-correctif.md) et la [préparation de livraison](preparer-livraison.md) décrivent les critères de passage et les preuves.

## Charger le contexte utile

Codex découvre les `AGENTS.md` depuis la racine du dépôt jusqu'au répertoire courant. Un dossier voisin du workspace n'est pas un parent : lire son guide lorsqu'il entre dans le périmètre. Les `AGENT.md` locaux sont des compléments explicitement liés, pas un nom de découverte supposé. Un guide automatique doit rester court ; les catalogues de fonctionnalités et les résultats datés vivent dans leurs documents. [Découverte officielle](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

| Tâche | Lire ensuite | Preuve attendue |
| --- | --- | --- |
| Règle métier ou transition | Spécification concernée, guide backend, [matrice d'architecture](../architecture/transverse/controle-architecture.md) | Invariant, propriétaire métier, cas nominal/refus et entrées affectées. |
| API partagée | [Conventions API](../architecture/transverse/conventions-api-openapi.md), producteur et consommateurs réels | Contrat, accès et comportement des consommateurs ; génération distincte du déploiement. |
| Interface/PWA | README et guide de l'application, spécification concernée | Test ciblé et, si le rendu change, contrôle visuel ; session/cache/permissions selon le périmètre. |
| Déplacement/fusion de documents | [Index des spécifications](../specifications/INDEX.md), roadmap, [exports et lecteurs](../exploitation/technique/reference-documentation-centralisee.md) | Source canonique unique, liens entrants/sortants, contrat d'export et lecteurs préservés. |
| Exploitation/démonstration | Procédure de l'environnement et guide local des scripts | Cible explicite, effets de la commande connus et vérification propre à l'opération. |
| Retouche rédactionnelle | Document et voisins utiles | Liens et exactitude du texte ; pas de batterie métier sans rapport. |

Lire d'abord `git status` et le diff du périmètre ; rechercher les symboles/chemins ciblés avec `rg`. Ne pas injecter tout le corpus, les contrats OpenAPI complets, les logs ni les secrets dans le contexte. Une affirmation de recette ou de déploiement exige une preuve distincte d'un build local.

## Skills locaux, chargés selon la tâche

| Skill | Usage | Exemple |
| --- | --- | --- |
| [localeo-documentation](../../.agents/skills/localeo-documentation/SKILL.md) | Migration, consolidation et audit documentaire avec consommateurs | « Utilise $localeo-documentation pour consolider les documents de cet epic. » |
| [localeo-invariants](../../.agents/skills/localeo-invariants/SKILL.md) | Règle métier, transition ou contrat partagé | « Utilise $localeo-invariants pour vérifier cette évolution avant de la coder. » |
| [localeo-creer-epic](../../.agents/skills/localeo-creer-epic/SKILL.md) | Cadrer un besoin en vérifiant la roadmap existante | « Crée ou enrichis l'epic correspondant à ce besoin. » |
| [localeo-specifier-epic](../../.agents/skills/localeo-specifier-epic/SKILL.md) | Transformer le cadrage en comportements et contrats testables | « Spécifie cette epic et ses impacts transverses. » |
| [localeo-implementer-epic](../../.agents/skills/localeo-implementer-epic/SKILL.md) | Réaliser une spécification avec preuves et documentation | « Implémente ces critères et vérifie leurs consommateurs. » |
| [localeo-corriger](../../.agents/skills/localeo-corriger/SKILL.md) | Reproduire, diagnostiquer et corriger une anomalie | « Corrige cette erreur avec une preuve de non-régression. » |
| [localeo-verifier-demonstration](../../.agents/skills/localeo-verifier-demonstration/SKILL.md) | Compatibilité des données générées avec le produit | « Vérifie le générateur après cette migration. » |
| [localeo-preparer-deploiement](../../.agents/skills/localeo-preparer-deploiement/SKILL.md) | Rassembler versions, contrôles et procédures de livraison | « Prépare le dossier de livraison vers cet environnement. » |

Ils sont versionnables dans `.agents/skills` de **localeo-projet**. Leur nom et description permettent une sélection implicite ; le corps n'est chargé qu'à l'utilisation. Les dépôts applicatifs voisins ne les découvrent pas automatiquement. Pour une tâche transverse, démarrer dans `localeo-projet` avec accès aux dépôts concernés ; sinon lire explicitement la fiche par son chemin. Aucun skill global ni copie applicative n'est installé. [Découverte et portée des skills](https://learn.chatgpt.com/docs/build-skills).

## Deux profils de revue

- [localeo-invariant-reviewer](../../.codex/agents/localeo-invariant-reviewer.toml) : placement des règles, contournements par les points d'entrée, preuves comportementales.
- [localeo-contract-reviewer](../../.codex/agents/localeo-contract-reviewer.toml) : sources, générateurs, schémas, lecteurs et compatibilité entre dépôts.

Les profils sont locaux à `localeo-projet`, demandent la lecture seule et héritent du modèle/effort du parent. L'hôte et les paramètres de session restent déterminants pour les permissions effectives. Confier un sous-problème indépendant, des fichiers précis et un résultat vérifiable ; le parent intègre les conclusions. Pour des agents qui éditent, attribuer des fichiers distincts. Une petite correction ne justifie pas de délégation. [Format officiel des profils](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Hooks et contrôles

Le [hook Codex SessionStart](../../.codex/hooks.json) appelle [codex_context.cjs](../../scripts/codex_context.cjs) au démarrage, à la reprise et après compaction. Il indique les dépôts absents, modifiés ou non vérifiables, puis rappelle les sources et la séparation commit/push/déploiement. Il lit le statut Git, sans contenu des fichiers, réseau ni écriture. Git et Node doivent être disponibles dans le PATH ; chaque commande Git a un délai limité.

La définition est créée et son script testé. **L'activation native reste à effectuer dans une nouvelle session du projet : ouvrir `/hooks`, examiner puis approuver cette définition.** Codex exige la confiance du projet et du hook exact ; une modification de la définition peut nécessiter un nouvel examen. Cette opération n'est pas remplacée par l'autorisation de créer les fichiers. Aucun contournement de confiance ni réglage global n'a été ajouté. [Règles officielles des hooks](https://learn.chatgpt.com/docs/hooks).

Le hook `Stop` appelle [codex_finish.cjs](../../scripts/codex_finish.cjs). Si un dépôt est modifié, absent ou non vérifiable, il rappelle d'exposer les preuves et les impacts ; il ne bloque pas la fin du tour, ne relance pas automatiquement l'agent et ne déduit aucun succès des messages. Les deux hooks sont en lecture seule et leurs sorties restent courtes. La confiance doit porter sur la définition actuelle contenant ces deux événements.

Le [contrôleur de guides](../../scripts/check_guidance.py) vérifie hors réseau les liens de `AGENTS.md`, `AGENT.md`, `README.md` et des skills locaux dans les cinq dépôts :

```console
python scripts/check_guidance.py --document docs/organisation/codex.md
python scripts/check_guidance.py --changed
python scripts/check_guidance.py --repo . --staged
python scripts/sync_documentation.py --check-sources
python -m unittest discover -s tests -p test_guidance.py
node --test tests/test_codex_context.cjs
```

`--staged` lit le contenu de l'index et vérifie les cibles du même dépôt dans l'index, y compris une cible supprimée ; les cibles voisines sont vérifiées sur disque. `--changed` inclut les guides renvoyant vers les fichiers supprimés. `--document` ajoute un Markdown au contrôle. Les dépôts voisins absents sont signalés ; un `--repo` explicitement demandé et absent est une erreur. Ce contrôle ne valide pas les ancres, les URL externes ni la justesse métier du texte.

Le [hook Git local](../../.githooks/pre-commit) utilise le contrôle de l'index de `localeo-projet`, y compris lorsqu'une suppression touche une cible sans modifier un README. Il est distinct des hooks Codex. Installer avec le Python à utiliser pour ses contrôles :

```console
python scripts/install_hooks.py --install
python scripts/install_hooks.py
```

L'installateur configure uniquement `core.hooksPath` et `localeo.python` dans ce dépôt. Il refuse de remplacer un gestionnaire contenant des hooks actifs ; aucun réglage global ni applicatif voisin n'est modifié. Node doit être disponible. Si le chemin de Python change, relancer l'installation. La [configuration pre-commit](../../.pre-commit-config.yaml) reste une alternative pour un environnement utilisant déjà ce gestionnaire ; ne pas installer les deux séparément. Le vérificateur ne stage aucun fichier et ne crée aucun commit.

Le hook utilise `--staged --changed --all-markdown` : il vérifie aussi les spécifications et procédures modifiées, ainsi que les liens entrants vers une cible supprimée. Il ne transforme pas les anciens liens cassés de documents inchangés en blocage d'une correction indépendante. Cette vérification incrémentale complète le contrôle général des guides.

## Contrôles et preuves reproductibles

[repositories.json](../../repositories.json) conserve les profils et commandes du [runner qualité](../../scripts/quality.py). `plan` décrit les commandes ; `run` les exécute et rapporte leurs résultats, les versions Git et les contrôles non exécutés dans `.artifacts/quality/`. Le profil `documentation-local` fonctionne sans applications voisines ; `documentation-workspace` contrôle aussi leurs liens. Les profils applicatifs utilisent leurs outils locaux et le profil `demonstration` exige explicitement les bases PostgreSQL jetables. Un profil ne prouve pas des contrôles absents de sa sélection.

```console
python scripts/quality.py plan --profile workspace
python scripts/quality.py run --profile documentation-workspace --output .artifacts/quality/documentation.json
python scripts/check_codex_workflows.py
```

Le [validateur de configuration](../../scripts/check_codex_workflows.py) vérifie les noms/descriptions des skills et les budgets locaux de contexte : 8000 octets pour le guide automatique racine, 14000 octets par skill, 1800 tokens au maximum pour le hook de début. Ce sont des garde-fous du projet, pas les limites universelles de Codex. Le contrôle des liens reste assuré par `check_guidance.py` ; une évaluation sur des cas représentatifs vérifie les décisions que prennent les workflows.

La [CI documentaire](../../.github/workflows/documentation.yml) distingue les outils locaux et la validation des cinq dépôts à des références immuables. L'accès privé et les règles de branche doivent être configurés dans GitHub. Le [guide de livraison](preparer-livraison.md) décrit les preuves nécessaires ; ni une CI partielle ni l'existence d'un workflow ne prouvent la recette d'un environnement.

## Exécuter et interpréter les validations

Depuis l'environnement Python activé, utiliser `python` ; depuis l'environnement Node, utiliser le gestionnaire et le verrou du README applicatif. Les scripts de contrôle documentaire utilisent la bibliothèque standard Python. Le hook de contexte utilise seulement Node et Git.

Les contrôles métier et de frontières existants sont décrits dans la [matrice d'architecture](../architecture/transverse/controle-architecture.md). Ils restent nécessaires lorsqu'une règle change. Les skills, profils et rappels du hook orientent le travail ; ils ne prouvent pas qu'un invariant est respecté.

`check_workspace.py` compare aussi les destinations du manifeste historique de migration. Son échec peut correspondre à des suppressions ultérieures ; examiner chaque cas sans recréer automatiquement des documents retirés. La suite complète `unittest discover -s tests` inclut les exigences de couverture des procédures opératoires, qui présentent une dette connue. L'audit daté distingue ces limites des contrôles ajoutés ici.

Pour une session parallèle, éviter deux builds qui écrivent le même répertoire de sortie. Reporter les tests réussis, les échecs, les contrôles non exécutés et les limites d'environnement séparément. Ne pas présenter une suite interrompue au nettoyage comme un succès complet.
