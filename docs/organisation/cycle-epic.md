# Cycle de travail d'une epic Localeo

Cette procédure relie cadrage, spécification, implémentation et preuves. Elle complète le [guide Codex](codex.md) et les [règles transverses](../../AGENTS.md). La [roadmap commune](../roadmap/README.md) reste l'unique référence d'état produit ; « prêt à spécifier » et « prêt à implémenter » sont des critères de préparation, pas de nouveaux statuts.

## Choisir le périmètre et le contexte

Une tâche commence par le besoin utilisateur, le statut Git des dépôts touchés et les sources ciblées. Les [instructions locales et commandes](../../repositories.json) orientent la lecture. Le contexte ne doit pas contenir un schéma complet ou une sélection IDE sans rapport avec la tâche ; fournir le chemin et rechercher les parties utiles.

Utiliser une conversation par epic ou intervention cohérente. Charger le backlog ciblé et le README de son dossier de spécification, puis seulement les règles et contrats nécessaires. Une petite correction peut porter son analyse dans le compte rendu ; elle ne nécessite pas automatiquement une nouvelle epic, tous les skills ni un dossier documentaire.

## Cadrer

Utiliser [localeo-creer-epic](../../.agents/skills/localeo-creer-epic/SKILL.md) et le [modèle de cadrage](../architecture/templates/epic-cadrage-template.md).

1. Rechercher une epic existante et ses arbitrages. Vérifier les identifiants communs et applicatifs, les fusions et abandons avant de créer un fichier.
2. Décrire problème, acteurs, résultat observable, périmètre, exclusions et dépendances. Distinguer faits vérifiés, hypothèses et propositions.
3. Écrire des critères d'acceptation identifiés dans l'epic et une première analyse des impacts. Les numéros de critères restent stables lorsque leur formulation évolue.
4. Mettre à jour le backlog canonique, les index et synthèses concernés. Lors d'un changement d'état autorisé, appliquer les déplacements et mises à jour prescrits par la roadmap, sans réécrire les bilans historiques.

**Prêt à spécifier :** le problème et le résultat attendu sont compréhensibles, le périmètre est borné, les critères sont observables et les questions ouvertes ont une portée explicite. Une question ne bloque que les travaux qui en dépendent ; ne pas demander une validation supplémentaire pour un choix déjà autorisé.

## Spécifier

Utiliser [localeo-specifier-epic](../../.agents/skills/localeo-specifier-epic/SKILL.md). Enrichir d'abord le document canonique dans l'[index des spécifications](../specifications/INDEX.md), avec le [modèle d'architecture](../architecture/templates/epic-architecture-template.md) lorsque sa profondeur est utile.

La conception rapproche le comportement existant vérifié et le comportement cible. Identifier les invariants et leur propriétaire selon la [matrice d'architecture](../architecture/transverse/controle-architecture.md), puis les entrées API, ERP, batch et interfaces réellement affectées. Décrire les transitions autorisées et refusées, les permissions et les effets secondaires. Examiner concurrence, répétition, reprise après échec et audit selon le risque.

Un contrat partagé indique son producteur, sa source canonique, ses générateurs et consommateurs. La spécification précise la compatibilité avec les données et versions existantes, les migrations nécessaires et l'ordre de livraison lorsque les applications ne peuvent évoluer indépendamment. Ne pas inventer de compatibilité ascendante ni de migration réversible sans preuve.

### Matrice de traçabilité

Conserver cette matrice dans la spécification ou son bilan existant, pas dans un nouveau registre parallèle. Elle peut regrouper plusieurs critères partageant les mêmes impacts. « Sans objet » exige une raison ; « à examiner » n'équivaut pas à « aucun impact ».

| Critère | Comportement et propriétaire | Preuve prévue puis résultat | Documentation fonctionnelle / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| Identifiant du critère | Déclencheur, résultat/refus, domaine et entrées | Test ou scénario, chemin, commande, état réel | Source canonique à modifier ou raison d'absence d'impact | Scénario, schéma, permissions, restauration ou raison d'absence d'impact | Migration, configuration, diagnostic, reprise ou raison d'absence d'impact |

**Prêt à implémenter :** les comportements du périmètre ont des critères et preuves prévues ; les responsabilités et contrats sont identifiés ; les impacts de données, documentation, démonstration et exploitation sont examinés ; aucun arbitrage bloquant n'est implicite. Les tests prévus ne sont pas présentés comme exécutés. Une partie indépendante peut être implémentée avant résolution d'une autre, si ce découpage est explicite.

## Implémenter et vérifier

Utiliser [localeo-implementer-epic](../../.agents/skills/localeo-implementer-epic/SKILL.md) pour une implémentation d'epic. Respecter les instructions de chaque dépôt et préserver les modifications existantes. La spécification peut évoluer avec une découverte vérifiée ; expliquer la conséquence sur les critères et les tests, sans changer silencieusement la règle produit.

Les tests doivent prouver les résultats observables : domaine pour les invariants, application pour l'orchestration et les refus d'accès, adaptateurs pour persistance et intégrations, consommateurs pour les contrats, parcours navigateur pour les interactions critiques concernées. Utiliser les outils isolés du backend ; aucune base d'exploitation ni envoi externe réel ne doit devenir une dépendance implicite des tests.

Pour une correction, reproduire le défaut avec un test ciblé lorsque cela apporte une preuve utile. Ne pas ajouter de tests qui recopient l'implémentation ou d'assertions d'import factices. Exécuter les contrôles requis puis élargir si les changements ou résultats révèlent un risque supplémentaire. Un échec d'architecture ne justifie pas l'absence silencieuse des tests fonctionnels.

Les travaux parallèles doivent avoir des fichiers ou worktrees distincts et des résultats attendus précis. Une revue indépendante est utile pour une règle sensible ou un contrat partagé : demander les scénarios manquants et les risques concrets aux profils décrits dans le guide Codex. L'agent principal intègre et vérifie les corrections.

### Critères de fin du périmètre livré

- Chaque critère retenu a une preuve pertinente, ou une limite explicitement déclarée empêchant de le considérer vérifié.
- Les tests et contrôles requis ont un résultat réel ; aucun échec, skip ou contrôle non exécuté n'est assimilé à une réussite. Une dette préexistante est étayée par une comparaison ou une référence vérifiable.
- Producteurs, contrats et consommateurs concernés sont cohérents. Les migrations et adaptations du générateur sont vérifiées lorsqu'elles sont nécessaires.
- Les documents fonctionnels, contrats, procédures et sources exportées concernés sont actualisés ; les éléments sans objet sont justifiés dans la matrice.
- Les constats de revue affectant les critères sont corrigés ou restent des limites visibles. Le compte rendu distingue le livré, le non vérifié et le restant.

Ces critères ne clôturent pas automatiquement une epic ni ne prouvent sa mise en production. Ne pas présenter une livraison partielle comme la fin de l'epic. Commit, push, préparation de livraison et déploiement restent des opérations distinctes suivant la demande en cours.

## Documenter les preuves et préparer la livraison

Un résultat de contrôle indique le dépôt, le chemin du test ou de la commande, le contexte testé (SHA si l'arbre est propre, ou SHA de base et modifications locales), l'environnement pertinent et le résultat. Référencer les rapports CI ou artefacts existants sans recopier les journaux ni leurs secrets. Des résultats obtenus sur un autre arbre ne valident pas automatiquement le changement courant.

Pour les documents, `python scripts/check_guidance.py --document <document>` vérifie les liens locaux. Pour les sources exportées, ajouter `python scripts/sync_documentation.py --check-sources`. Ces contrôles ne prouvent pas la justesse fonctionnelle ; vérifier les lecteurs si un contrat change. Les règles d'export restent celles de la [documentation centralisée](../exploitation/technique/reference-documentation-centralisee.md).

Le dossier de livraison rassemble les SHAs des dépôts affectés, les preuves, les migrations et leur ordre, les configurations requises sans secrets, les empreintes des artefacts pertinents, les vérifications après livraison et les procédures de reprise applicables. Consulter les [releases](../../releases/INDEX.md) et l'[exploitation](../exploitation/INDEX.md). Une procédure écrite ou un build local ne prouve pas un déploiement ou une restauration effective.

## Reprendre une tâche longue

Conserver une note de reprise courte dans le support de travail déjà utilisé (conversation, description de PR ou note temporaire locale). Éviter une seconde spécification versionnée et toute donnée sensible. Format conseillé :

```text
Objectif et périmètre autorisé :
Sources canoniques et critères concernés :
Décisions prises / questions ouvertes :
Dépôts, branches, SHAs de base et fichiers modifiés :
Contrôles exécutés, résultats et limites :
Prochaine action et dépendances :
```

À la reprise, vérifier le statut Git et la fraîcheur des preuves avant d'utiliser cette note. La note facilite la navigation ; le code, la spécification et les résultats vérifiables restent les sources.

## Évaluer les skills sur des cas représentatifs

Ces scénarios constituent un protocole d'évaluation, **pas un compte rendu de tests déjà exécutés**. Les jouer dans un espace temporaire ou un worktree dédié, sans modifier la roadmap active ni contacter de service réel. Donner à l'évaluateur le besoin et les sources minimales ; conserver les critères attendus pour la revue indépendante.

| Cas | Demande et matériaux minimaux | Comportement à vérifier |
| --- | --- | --- |
| Cadrage ambigu et identifiant historique | « Crée une epic pour ajouter un sas de validation aux modifications de prestations. » Fournir la roadmap et le backlog Epic 62 existant. | Retrouve le périmètre existant, ne crée pas de doublon, distingue besoin couvert et extension proposée, pose uniquement les questions qui changent le périmètre. |
| Contrat partagé et concurrence | « Spécifie l'import d'une réponse de génération quand le brouillon source a évolué. » Fournir le dossier moteur d'animation et les chemins du producteur ERP et des contrôles de version. | Vérifie l'existant, identifie le propriétaire de règle et les différences significatives, prévoit le succès sans changement et le refus après changement pertinent, rend les impacts consommateurs et démonstration explicites. |
| Non-régression et évolution des données | « Implémente une évolution du schéma de démonstration selon cette spécification. » Fournir une spécification d'exercice, le générateur, le restaurateur et les tests concernés dans le worktree. | Adapte génération et restauration ensemble, choisit des preuves comportementales, ne masque pas les tests PostgreSQL indisponibles ou ignorés, documente les limites et la reprise. |

Pour chaque essai, enregistrer la version du skill et des sources, les artefacts produits, les oublis ou erreurs observés, les reprises nécessaires et les vérifications réellement exécutées. Une validation syntaxique de skill ne vaut pas réussite de ces scénarios. Comparer avec le même besoin avant modification du skill lorsque possible ; faire évoluer les instructions à partir des écarts constatés, sans accumuler des règles générales pour chaque incident.
