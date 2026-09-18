# Utiliser Codex dans le workspace Localeo

Ce guide décrit le fonctionnement local des cinq dépôts. Les [règles transverses](../../AGENTS.md) restent la référence ; les états produit viennent de la [roadmap](../roadmap/README.md). L'[audit du 18 septembre 2026](audit-contexte-codex-2026-09-18.md) conserve les constats et les validations de cette mise en place.

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

## Deux skills locaux

| Skill | Usage | Exemple |
| --- | --- | --- |
| [localeo-documentation](../../.agents/skills/localeo-documentation/SKILL.md) | Migration, consolidation et audit documentaire avec consommateurs | « Utilise $localeo-documentation pour consolider les documents de cet epic. » |
| [localeo-invariants](../../.agents/skills/localeo-invariants/SKILL.md) | Règle métier, transition ou contrat partagé | « Utilise $localeo-invariants pour vérifier cette évolution avant de la coder. » |

Ils sont versionnables dans `.agents/skills` de **localeo-projet**. Leur nom et description permettent une sélection implicite ; le corps n'est chargé qu'à l'utilisation. Les dépôts applicatifs voisins ne les découvrent pas automatiquement. Pour une tâche transverse, démarrer dans `localeo-projet` avec accès aux dépôts concernés ; sinon lire explicitement la fiche par son chemin. Aucun skill global ni copie applicative n'est installé. [Découverte et portée des skills](https://learn.chatgpt.com/docs/build-skills).

## Deux profils de revue

- [localeo-invariant-reviewer](../../.codex/agents/localeo-invariant-reviewer.toml) : placement des règles, contournements par les points d'entrée, preuves comportementales.
- [localeo-contract-reviewer](../../.codex/agents/localeo-contract-reviewer.toml) : sources, générateurs, schémas, lecteurs et compatibilité entre dépôts.

Les profils sont locaux à `localeo-projet`, demandent la lecture seule et héritent du modèle/effort du parent. L'hôte et les paramètres de session restent déterminants pour les permissions effectives. Confier un sous-problème indépendant, des fichiers précis et un résultat vérifiable ; le parent intègre les conclusions. Pour des agents qui éditent, attribuer des fichiers distincts. Une petite correction ne justifie pas de délégation. [Format officiel des profils](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Hooks et contrôles

Le [hook Codex SessionStart](../../.codex/hooks.json) appelle [codex_context.cjs](../../scripts/codex_context.cjs) au démarrage, à la reprise et après compaction. Il indique les dépôts absents, modifiés ou non vérifiables, puis rappelle les sources et la séparation commit/push/déploiement. Il lit le statut Git, sans contenu des fichiers, réseau ni écriture. Git et Node doivent être disponibles dans le PATH ; chaque commande Git a un délai limité.

La définition est créée et son script testé. **L'activation native reste à effectuer dans une nouvelle session du projet : ouvrir `/hooks`, examiner puis approuver cette définition.** Codex exige la confiance du projet et du hook exact ; une modification de la définition peut nécessiter un nouvel examen. Cette opération n'est pas remplacée par l'autorisation de créer les fichiers. Aucun contournement de confiance ni réglage global n'a été ajouté. [Règles officielles des hooks](https://learn.chatgpt.com/docs/hooks).

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

Un [hook Git pre-commit optionnel](../../.pre-commit-config.yaml) utilise le contrôle de l'index de `localeo-projet`. Il s'exécute aussi lorsqu'une suppression touche une cible sans modifier un README. Il est distinct du hook Codex et n'est pas installé automatiquement :

```console
python -m pip install pre-commit
python -m pre_commit install
```

Ce hook ne remplace pas les hooks déjà configurés dans les applications. Sans installation, la commande de contrôle reste utilisable directement. Le vérificateur ne stage aucun fichier et ne crée aucun commit.

## Exécuter et interpréter les validations

Depuis l'environnement Python activé, utiliser `python` ; depuis l'environnement Node, utiliser le gestionnaire et le verrou du README applicatif. Les scripts de contrôle documentaire utilisent la bibliothèque standard Python. Le hook de contexte utilise seulement Node et Git.

Les contrôles métier et de frontières existants sont décrits dans la [matrice d'architecture](../architecture/transverse/controle-architecture.md). Ils restent nécessaires lorsqu'une règle change. Les skills, profils et rappels du hook orientent le travail ; ils ne prouvent pas qu'un invariant est respecté.

`check_workspace.py` compare aussi les destinations du manifeste historique de migration. Son échec peut correspondre à des suppressions ultérieures ; examiner chaque cas sans recréer automatiquement des documents retirés. La suite complète `unittest discover -s tests` inclut les exigences de couverture des procédures opératoires, qui présentent une dette connue. L'audit daté distingue ces limites des contrôles ajoutés ici.

Pour une session parallèle, éviter deux builds qui écrivent le même répertoire de sortie. Reporter les tests réussis, les échecs, les contrôles non exécutés et les limites d'environnement séparément. Ne pas présenter une suite interrompue au nettoyage comme un succès complet.
