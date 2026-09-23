# Développer et corriger Localeo avec Codex

Ce guide explique les demandes à formuler et les résultats à attendre. Le [guide technique Codex](codex.md) décrit les mécanismes ; le [cycle d'epic](cycle-epic.md) et le [cycle de correctif](cycle-correctif.md) portent les règles du travail.

## Préparer sa session

1. Ouvrir le workspace Localeo avec ses cinq dépôts. Pour un travail transverse, démarrer Codex dans `localeo-projet`, avec accès aux applications concernées. Cela rend les skills locaux découvrables. Depuis une application, demander explicitement de lire le skill dans le dépôt voisin ; les `AGENTS.md` locaux indiquent ce routage.
2. Garder la sélection IDE sur le code ou la spécification utile. Retirer une sélection volumineuse sans rapport avec la demande. Donner les chemins plutôt que recopier un schéma entier à chaque message.
3. Donner l'objectif, le comportement attendu et les contraintes connues. Il n'est pas nécessaire de recopier les règles du projet ni de citer tous les skills.
4. Pour un nouveau sujet, ouvrir une conversation distincte. Pour poursuivre le même travail, garder la conversation ou fournir la note courte de reprise décrite plus bas.

Les skills sont sélectionnés selon la demande ou appelés explicitement avec `$nom-du-skill`. Ils n'imposent pas de nouvelle confirmation pour une action déjà autorisée. Une question produit réellement bloquante reste une question : Codex ne doit pas inventer l'arbitrage.

## Exemple : du besoin à la livraison

### 1. Cadrer une epic

> Utilise $localeo-creer-epic pour cadrer ce besoin : [problème et utilisateurs]. Vérifie d'abord si une epic existante couvre ce besoin. Périmètre souhaité : […]. Contraintes : […].

Résultat attendu : epic créée ou existante enrichie, objectif observable, exclusions, dépendances et critères d'acceptation. Codex vérifie les identifiants et les états de la roadmap ; il ne crée pas un doublon pour suivre la conversation.

### 2. Spécifier

> Utilise $localeo-specifier-epic sur [chemin de l'epic]. Décris les règles, les comportements, les erreurs, les contrats et les tests attendus. Analyse les impacts sur les cinq dépôts, le générateur et l'exploitation. Signale les décisions manquantes.

Résultat attendu : spécification fonctionnelle et architecture cohérentes, règle portée par le domaine, critères reliés aux scénarios de test. Les critères « prêts à implémenter » du cycle d'epic doivent être satisfaits. Une décision bloquante non tranchée limite seulement la partie dépendante ; le reste peut avancer.

### 3. Implémenter et vérifier

> Utilise $localeo-implementer-epic pour réaliser [chemin de la spécification]. Implémente les critères [identifiants ou tout le périmètre], ajoute les tests appropriés et actualise les documents affectés. Vérifie les consommateurs et le générateur s'ils sont concernés.

Résultat attendu : changements par dépôt, tests des comportements, documentation à jour et compte rendu des preuves. Codex peut déléguer une revue indépendante sur une évolution transverse. Il conserve les fichiers déjà modifiés et les contrats de chaque application.

Pour demander explicitement la vérification du jeu généré :

> Utilise $localeo-verifier-demonstration pour vérifier la compatibilité du générateur avec [évolution]. Exécute les tests ciblés et, si les bases jetables requises sont disponibles, le cycle PostgreSQL complet. Distingue les contrôles non exécutés.

### 4. Préparer la livraison

> Utilise $localeo-preparer-deploiement pour préparer la livraison de [epic/correctif] vers [environnement]. Assemble les versions, preuves, migrations, documents et procédures. Produis le dossier de préparation avec ses blocages éventuels.

Résultat attendu : dossier traçable et [manifeste de préparation](preparer-livraison.md). Un rapport de tests local ne prouve ni un déploiement ni le bon fonctionnement de l'environnement cible.

Les demandes Git et exploitation sont distinctes. Exemples : « Commit les changements de cette epic dans chaque dépôt concerné », puis « Push ces commits ». Une demande explicite de déploiement doit identifier la cible ; les vérifications de la procédure s'appliquent alors.

## Exemple : corriger une anomalie

> Utilise $localeo-corriger. Dans [écran/API], quand [étapes], j'obtiens [erreur exacte]. J'attends [résultat]. Environnement/version : […]. Référence d'erreur : […]. Reproduis, identifie la cause, corrige et vérifie la non-régression. Voici les chemins ou fichiers utiles : […].

Les informations inconnues peuvent être indiquées comme telles. Éviter les accès privés, données personnelles et secrets dans le message.

Codex doit :

1. Retrouver le comportement attendu et distinguer l'observation d'une hypothèse.
2. Reproduire l'erreur avec une entrée minimale ou préciser pourquoi elle n'est pas reproduite.
3. Ajouter un test de régression utile : échec avant correction, succès après, lorsque le défaut s'y prête.
4. Corriger la cause et vérifier les autres points d'entrée concernés.
5. Actualiser les documents, contrats et données affectés ; indiquer les tests exécutés et les limites.

Une correction limitée n'exige pas une nouvelle epic. Si elle révèle une décision produit ou une refonte plus large, Codex expose cette dépendance au lieu de l'introduire implicitement. Pour une urgence, préciser la contrainte ; le rapport doit conserver les vérifications manquantes, même si le correctif est petit.

Pour reprendre un diagnostic :

> Poursuis le correctif [référence]. La reproduction est [test/commande]. La cause établie est […]. Restent [contrôle ou comportement]. Préserve les changements déjà présents et vérifie leur état avant de reprendre.

## Commandes de contrôle

Depuis `localeo-projet`, avec Python et Node disponibles :

```console
python scripts/quality.py plan --profile documentation-local
python scripts/quality.py run --profile documentation-workspace
python scripts/quality.py run --profile backend
python scripts/quality.py run --profile animation
python scripts/quality.py plan --profile workspace
python scripts/quality.py release --help
```

`plan` annonce les commandes, il ne les exécute pas. `run` enregistre les résultats dans `.artifacts/quality/` ; utiliser `--output` pour conserver plusieurs rapports sans remplacer le précédent. Lire `--help` et le plan avant une exécution complète. Les profils applicatifs nécessitent leurs dépendances installées et ne remplacent pas les tests spécifiques d'une epic. PostgreSQL et les parcours connectés ont leurs prérequis propres.

Les rapports distinguent échec et non-exécution. Un rapport préparatoire, partiel, ancien ou obtenu avant une modification ne devient pas automatiquement une preuve de livraison. Ne pas réduire la sélection pour masquer un test qui échoue.

## Comprendre les mécanismes

| Mécanisme | Rôle | Ce qu'il ne prouve pas |
| --- | --- | --- |
| `AGENTS.md` | Règles durables et liens utiles au périmètre | Leur respect effectif par le code |
| Skill | Procédure de cadrage, spécification, réalisation, correctif ou livraison | La réussite des tests |
| Hook Codex de début | Repérage des dépôts et rappel du contexte utile | La lecture de toutes les spécifications |
| Hook Codex de fin | Rappel des preuves à exposer si le workspace est modifié/incomplet | Une validation ou une interdiction de terminer |
| Hook Git local | Liens des Markdown modifiés dans l'index et liens entrants après suppression | La conformité métier |
| CI | Exécution reproductible des contrôles configurés | Les usages d'une cible réelle non testée |
| Revue indépendante | Recherche d'écarts de domaine, contrat ou preuve | Une garantie absolue d'absence de défaut |

Le hook Git se configure avec `python scripts/install_hooks.py --install` ; le script refuse de remplacer des hooks existants. `python scripts/install_hooks.py` affiche la configuration locale. Ne pas cumuler cette installation avec un second gestionnaire de hooks sans les intégrer explicitement.

Pour les hooks Codex, ouvrir `/hooks` dans une session du projet et examiner la définition versionnée. L'activation native exige la confiance de cette définition exacte ; elle ne peut pas être remplacée par une déclaration dans un document. Une nouvelle session peut être nécessaire pour découvrir les nouveaux skills.

## Reprendre sans recharger toute l'histoire

Conserver une note brève dans la conversation ou dans un fichier de travail ignoré, avec : objectif et périmètre, chemins canoniques, versions de travail, décisions établies, critères réalisés/restants, tests et résultats, prochain point à traiter. Relire le statut Git et les sources à la reprise. La note n'est ni une deuxième roadmap ni une preuve plus récente que le code.

## Reconnaître une tâche terminée

Le compte rendu permet de répondre à quatre questions : qu'est-ce qui a changé, quels critères sont couverts, quelles preuves ont été exécutées, qu'est-ce qui reste incertain ? « Build réussi » seul ne valide pas une règle métier ; « tests écrits » ne signifie pas « tests exécutés » ; « commit créé » ne signifie pas « déployé ».
