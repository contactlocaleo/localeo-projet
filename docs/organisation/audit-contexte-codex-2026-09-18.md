# Audit du contexte et de l'outillage Codex — 18 septembre 2026

## Résultat et périmètre

Les cinq dépôts restent indépendants. Cette passe porte sur les fichiers `AGENTS.md`, `AGENT.md` et `README.md`, leurs références et les mécanismes locaux qui aident Codex à appliquer les invariants. Les applications n'ont reçu que des corrections de guides ; aucun comportement produit, contrat supprimé ou état de roadmap n'a été changé. Aucun commit, push ou déploiement n'a été effectué.

L'inventaire couvre **70 guides existants** : 47 dans `localeo-projet`, 12 dans le backend, 4 dans Animation, 3 dans Commerçant et 4 dans Marketplace. **29 guides existants ont été modifiés**. Les 46 README du dépôt central ont fait l'objet d'une lecture intégrale, y compris leurs grandes spécifications historiques. Les deux nouveaux skills et les documents d'accompagnement sont également contrôlés. L'[inventaire détaillé](audit-contexte-codex-2026-09-18.json) conserve les HEAD de référence, les tailles et fichiers modifiés, les résultats et l'examen des liens externes.

## Constats et corrections

| Constat | Correction | Effet attendu |
| --- | --- | --- |
| Le guide backend mêlait règles, catalogue d'epics et historique de releases. | Guide recentré sur les frontières, les invariants, les effets externes et les preuves ; liens vers les sources par tâche. | Moins de contexte permanent et moins de statuts concurrents de la roadmap. |
| Plusieurs README frontend étaient trop courts pour expliquer les prérequis et les effets des commandes. | Gestionnaire/verrou, commandes existantes, configuration, builds et tests précisés à partir du code. | Éviter les commandes supposées et les validations annoncées sans preuve. |
| Les guides voisins pouvaient être considérés comme hérités par le workspace. | Lecture explicite des instructions des dépôts touchés ; portée locale des skills/profils documentée. | Un contexte transverse cohérent sans créer de Git parent. |
| Les README d’exploitation et d’architecture conservaient des chemins et consignes de l’ancienne organisation. | Chemins de formation, démonstration et viewer corrigés ; conception rattachée au dossier canonique plutôt qu’à un document concurrent obligatoire. | Éviter de recréer les copies documentaires supprimées. |
| Les README EP47/48/50 mêlaient conception initiale et état technique courant. | Divergences Stripe signalées avec preuves ; bilan des batchs daté et relié au registre ; dépôt propriétaire de l’implémentation précisé. | Préserver les décisions produit et rendre les écarts visibles. |
| Des formulations ne distinguaient pas invariant métier et projection technique. | Domaine propriétaire, points d'entrée et test comportemental attendus explicités ; limites des contrôles statiques rappelées. | Les API, l'ERP et les batchs appliquent la même règle. |
| `envrac.md`, retiré de la roadmap, restait lié par les guides. | Liens obsolètes retirés sans recréer le document supprimé. | Navigation conforme à l'arbre actuel. |
| La documentation Commerçant mentionnait une icône absente, une ancienne palette et une double génération OpenAPI. | Sources vivantes liées, icônes réelles, tokens actuels, état du service worker et export unique décrits. | Distinguer ce qui existe de ce qui était prévu. |
| Le contrat embarqué Commerçant a été supprimé alors que deux lecteurs l'utilisent encore. | Absence et prérequis rendus visibles, sans restaurer implicitement le fichier. | Un import manquant ne devient pas une fausse validation d'intégration. |
| Les validations locales étaient parfois assimilées à une livraison ou à une suite entièrement réussie. | Commit/push/déploiement distingués ; teardown Playwright et échecs historiques qualifiés et datés. | Compte rendu vérifiable et limites explicites. |

Le [guide Codex](codex.md) rassemble le routage par type de tâche et les commandes. Les instructions courtes renvoient aux conventions canoniques ; elles ne reproduisent ni la spécification complète ni les catalogues de fonctionnalités.

### Évolution du contexte

Le fichier backend `AGENT.md` passe de **24 114 à 8 636 octets**, soit environ **64 % de réduction**. Ses 328 lignes deviennent 66 lignes ; la taille en octets est le meilleur indicateur ici, plusieurs règles étant regroupées en paragraphes. Les invariants utiles restent présents.

Les README frontend sont volontairement plus complets : l'objectif n'est pas une réduction uniforme, mais de garder les instructions automatiquement chargées courtes et de rendre les détails accessibles à la demande. Les informations d'installation ne sont plus recopiées dans plusieurs guides du même dépôt. Les notices de provenance et de licence restent conservées.

## Mécanismes créés

| Élément | Emplacement | État et portée |
| --- | --- | --- |
| Skill documentaire | [.agents/skills/localeo-documentation](../../.agents/skills/localeo-documentation/SKILL.md) | Déplacement/fusion, source canonique, liens, exports et consommateurs ; utilisable depuis le projet. |
| Skill invariants | [.agents/skills/localeo-invariants](../../.agents/skills/localeo-invariants/SKILL.md) | Règle, propriétaire, points d'entrée, contrat et preuves ; exclut les simples retouches visuelles. |
| Profil de revue métier | [localeo-invariant-reviewer.toml](../../.codex/agents/localeo-invariant-reviewer.toml) | Lecture seule demandée ; constats étayés, aucune correction implicite. |
| Profil de revue des contrats | [localeo-contract-reviewer.toml](../../.codex/agents/localeo-contract-reviewer.toml) | Producteurs, générateurs et consommateurs entre dépôts ; lecture seule demandée. |
| Hook Codex de contexte | [.codex/hooks.json](../../.codex/hooks.json), [script Node](../../scripts/codex_context.cjs) | Démarrage/reprise/compaction : présence et statut des dépôts, rappel des sources. Créé et testé ; confiance native non enregistrée. |
| Contrôleur de guides | [check_guidance.py](../../scripts/check_guidance.py) | Hors réseau, guides Git suivis et nouveaux non ignorés ; fichiers sur disque ou index Git. |
| Hook Git optionnel | [.pre-commit-config.yaml](../../.pre-commit-config.yaml) | Contrôle de l'index du dépôt documentaire, y compris les cibles supprimées. Définition préparée, installation non effectuée. |

Les profils héritent du modèle et de l'effort du parent. Aucun modèle imposé, serveur MCP, plugin supplémentaire, accès distant, réglage global ou extension des permissions n'a été ajouté. La découverte des profils reste propre au client et à une nouvelle session ; leur chargement natif n'a pas été prouvé par un lancement de sous-agent configuré.

Le hook de contexte ne charge aucun fichier `.env` et ne restitue aucun contenu de fichier ni valeur de configuration ; il ne restitue que les noms prédéfinis des dépôts et leur catégorie de statut. Il ne bloque pas une action et ne prétend pas vérifier les règles métier. Les noms de fichiers retournés par Git ne sont pas injectés dans le contexte.

**Activation restante :** ouvrir une nouvelle session dans `localeo-projet`, puis `/hooks` pour examiner et approuver le hook exact. Cette étape appartient au mécanisme de confiance de Codex ; aucun contournement n'est utilisé. Le hook Git peut être installé séparément dans un environnement Python équipé de `pre-commit`. Les commandes et sources officielles sont dans le [guide d'utilisation](codex.md#hooks-et-contrôles).

## Vérifications réalisées

| Contrôle | Résultat |
| --- | --- |
| Liens locaux des guides et nouveaux documents | **78 guides et documents, 749 liens locaux, zéro erreur et zéro avertissement**. Le vérificateur ne valide pas les ancres. |
| Liens externes | 13 URL inventoriées : 11 réponses HTTP 200, 0 lien cassé confirmé ; Unsplash non vérifiable après redirection vers un challenge, Figma exclu du contrôle documentaire. Pas d'appel à une API métier. |
| Tests du contrôleur | **14 tests réussis** : références Markdown, espaces/parenthèses, exclusions, fichier indexé différent du disque, suppression dans l'index, cibles voisines et guides impactés. |
| Synchroniseur documentaire | **16 tests exécutés : 15 réussis, 1 ignoré** pour la création de symlink sous Windows. Contrôle des **117 sources exportées réussi**. |
| Script du hook | **1 test réussi** sur les statuts distincts, les erreurs Git et la non-divulgation des noms de fichiers. Exécution réelle directe et via la commande Windows réussie, depuis la racine et un sous-dossier ; cinq dépôts trouvés. |
| Skills | Deux validations `quick_validate.py` réussies. PyYAML installé uniquement dans `tmp/` ignoré pour ce validateur, sans modifier l'environnement global. |
| Découverte Codex | `codex debug prompt-input` confirme le guide transverse et les deux skills dans l'entrée du modèle. CLI locale `0.154.0-alpha.6.1`. |
| Profils de sous-agents | TOML valide, champs requis présents, mode lecture seule, aucun modèle/effort fixé ; revue indépendante des instructions. Pas de preuve de lancement natif de ces profils. |
| Mise à l'épreuve du skill invariants | Revue déléguée du contrat Commerçant : deux lecteurs directs, un générateur, artefact et dossier absents ; classé comme invariant technique, sans inventer un nouvel agrégat métier. |
| Guides frontend | 105 liens locaux, une ancre et 29 références de commandes contrôlés ; Animation : **13 tests ciblés réussis** ; Commerçant : **une suite échoue à l'import, zéro test exécuté**, contrat absent. |
| Guides backend | 82 liens locaux et ancres contrôlés ; commandes confrontées aux scripts, dépendances et workflows. Suite métier non relancée pour ces changements de texte. |
| Documents Commerçant canoniques | 25 liens et ancres contrôlés ; concordance CSS, manifeste et listeners du service worker vérifiée. |
| Diff Git | Contrôle des espaces et revue des changements dans les cinq dépôts. |

Commandes frontend exécutées lors de cette passe, depuis leurs racines respectives :

```console
# localeo-animation
node --test tests/auth-memory.test.mjs tests/http-context.test.mjs tests/pwa.test.mjs tests/build-environment.test.mjs
# localeo-commercant
node node_modules/vitest/vitest.mjs run src/lib/api/contracts.test.js --maxWorkers=2
```

Les contrôles HTTP mesurent l'accessibilité, pas l'exactitude du contenu ni les ancres. Les exemples de code et URL de services ne sont pas visités. Les captures de résultats datées ne sont pas transformées en promesses permanentes.

## Limites et suites utiles

1. **Contrat Commerçant :** [contracts.test.js](../../../localeo-commercant/src/lib/api/contracts.test.js) et [check-deployment.mjs](../../../localeo-commercant/scripts/check-deployment.mjs) lisent `api/localeo-openapi.json`, absent. [export-openapi.py](../../../localeo-commercant/scripts/export-openapi.py) écrit ce contrat sans créer son dossier. La correction fonctionnelle doit rétablir une chaîne source/générateur/consommateurs cohérente ; cette passe documentaire ne restaure pas une suppression utilisateur déjà commitée.
2. **Manifeste historique :** `check_workspace.py` signale encore **10 destinations absentes** du manifeste de migration après les réorganisations/suppressions ultérieures. Il ne faut pas recréer automatiquement ces fichiers. Le contrôle actuel des guides est distinct de cette vérification historique.
3. **Couverture métier :** les deux échecs de recensement backend restent décrits dans le [contrôle d'architecture](../architecture/transverse/controle-architecture.md#validation-du-18-septembre-2026). Les exigences documentaires des procédures opératoires comportent également une dette antérieure ; la suite complète n'a pas été relancée. Aucun test n'a été affaibli.
4. **Marketplace :** la fermeture Playwright avait été interrompue après cinq scénarios réussis lors de la validation précédente. Ce constat local ne constitue ni une réussite globale ni une panne universelle. Aucun nouveau build ou parcours connecté lancé ici.
5. **Portée Codex :** les skills/profils sont locaux au projet documentaire et ne s'installent pas implicitement chez les voisins. Le [guide](codex.md) explique le point de départ transverse et la lecture explicite depuis une application. Les configurations de confiance, hooks Git installés et protections de branche ne sont pas modifiés.
6. **Preuve finale :** skills, agents et hooks aident à retrouver les bonnes règles. Leur efficacité repose toujours sur les tests comportementaux ciblés, les contrôles d'architecture existants et la revue du diff.
