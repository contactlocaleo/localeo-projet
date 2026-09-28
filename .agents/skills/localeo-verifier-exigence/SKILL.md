---
name: localeo-verifier-exigence
description: Vérifier la prise en compte d'une exigence Localeo dans les spécifications, l'implémentation et les preuves de comportement, avec traçabilité et écarts entre dépôts. Utiliser pour une demande de conformité ou de couverture ciblée, même sans identifiant d'epic. Ne déclenche pas à elle seule une correction ni une évolution produit.
---

# Vérifier une exigence Localeo

Lire le [guide transverse](../../../AGENTS.md), puis les seules sources utiles dans l'[index des spécifications](../../../docs/specifications/INDEX.md) et la [roadmap](../../../docs/roadmap/README.md). Lire les instructions locales de chaque application effectivement concernée. Conserver le périmètre demandé : une exigence n'impose pas l'audit complet des cinq dépôts.

## Établir ce qui doit être vérifié

- Reprendre l'exigence donnée, sa source et son identifiant lorsqu'il existe. Retrouver sa version applicable, ses critères et les décisions qui la remplacent ou la précisent. Une epic terminée ne prouve pas la réalisation d'une évolution ultérieure ; les statuts courants priment sur les anciennes stories.
- Décomposer les formulations générales en résultats observables : acteur, préconditions, déclencheur, résultat attendu, refus et effets interdits pertinents. Préserver les identifiants existants ; de simples repères locaux suffisent si aucun critère n'est identifié.
- Distinguer la demande actuelle, le comportement spécifié et le comportement observé. Une divergence entre eux est un constat, pas une autorisation de redéfinir l'exigence. Si une ambiguïté change le verdict, demander la précision et poursuivre les parties indépendantes. Une source introuvable n'empêche pas d'examiner une attente clairement formulée par l'utilisateur.
- Préciser la portée de la conclusion : documentation seule si demandée, sinon implémentation et preuves locales ; environnement déployé seulement s'il est identifié et accessible. Relever branche, SHA et modifications locales des dépôts examinés pour dater les preuves.

## Suivre le comportement jusqu'à ses consommateurs

Pour chaque critère, retrouver les fichiers et appels effectifs qui le réalisent, ainsi que les tests qui pourraient le contredire. Une recherche de mots-clés sert à localiser, pas à conclure à la conformité ou à l'absence d'implémentation.

- Pour une règle métier, identifier le propriétaire dans le domaine backend et les entrées concernées (API, ERP, batch, webhook). Appliquer [localeo-invariants](../localeo-invariants/SKILL.md) si la vérification porte sur une règle, une transition ou un contrat partagé.
- Pour un contrat, suivre producteur, source canonique, générateur, contrat embarqué et consommateurs réels. Pour un parcours, suivre données, projection et interface jusqu'au résultat visible. Examiner permissions, états et chemins alternatifs lorsqu'ils changent le résultat attendu.
- Vérifier les impacts pertinents sur documentation fonctionnelle et ops, données existantes, migrations, configuration, fixtures et générateur de démonstration. Justifier les éléments sans objet ; signaler un dépôt manquant ou non examiné sans le déclarer conforme.
- Distinguer instruction et garantie : une exigence écrite dans un prompt ne prouve pas la conformité d'une sortie générée ; une validation de schéma ne prouve pas sa pertinence métier ou visuelle. Examiner les contrôles et résultats réels correspondant à l'attente, sans inventer un nouveau refus serveur si celui-ci n'est pas exigé.

## Rassembler les preuves

Choisir les contrôles dans la [matrice d'architecture](../../../docs/architecture/transverse/controle-architecture.md). Lire les assertions des tests pertinents et exécuter les contrôles existants proportionnés sur l'arbre courant, dans les environnements isolés prescrits. Pour un comportement visuel, examiner le rendu quand il est accessible ; une revue du code ne vaut pas recette navigateur. Ne pas charger la configuration d'exploitation ni contacter un fournisseur ou une base réelle implicitement pour un audit.

Un test écrit, ignoré, interrompu ou non exécuté n'est pas une preuve réussie. Un build, un import ou un contrôle documentaire ne suffit pas à prouver une règle métier. Vérifier le cas nominal et les refus ou variantes déterminants pour le critère. Si une preuve manque, décrire le scénario discriminant et les prérequis nécessaires ; ne pas fabriquer de test miroir pour produire un résultat vert. Une dette préexistante exige une référence ou comparaison vérifiable.

La vérification seule conserve les sources applicatives et les statuts de roadmap. Les rapports et sorties temporaires de contrôle restent possibles ; consigner les résultats dans le suivi canonique seulement si demandé, sans créer un registre concurrent. Si la correction ou l'évolution est déjà autorisée dans la demande en cours, poursuivre avec [localeo-corriger](../localeo-corriger/SKILL.md) ou [localeo-faire-evoluer-epic](../localeo-faire-evoluer-epic/SKILL.md), puis revérifier les critères concernés. Sinon présenter les actions recommandées sans les implémenter.

## Rendre un verdict traçable

Présenter d'abord les écarts qui empêchent de satisfaire l'exigence, leur conséquence observable et les preuves associées. Donner ensuite une matrice courte, dans le compte rendu ou le support canonique demandé, en réutilisant la [traçabilité du cycle d'epic](../../../docs/organisation/cycle-epic.md) lorsqu'elle existe :

| Critère / attente | Spécification applicable | Implémentation et consommateurs | Preuves et limites | Verdict / suite |
| --- | --- | --- | --- | --- |
| Identifiant ou repère local | Chemin et décision | Chemins et comportement constaté | Test, commande, version, résultat réel ou scénario manquant | État justifié et action ciblée |

Employer des verdicts explicites par critère :

- **Vérifié** : preuves adaptées au comportement et au périmètre annoncé, sans écart ouvert sur ce critère.
- **Partiel** : couverture de certaines parties seulement ; nommer celles qui manquent ou restent non vérifiées.
- **Non satisfait** : contradiction établie avec l'attente ; indiquer le scénario et la preuve, plutôt qu'une simple absence de mot-clé.
- **Non vérifiable en l'état** : preuves, accès ou arbitrage insuffisants ; donner la condition qui permettrait de conclure.
- **Sans objet** : hors du périmètre applicable, avec justification.

Le verdict global ne masque aucun critère partiel, non satisfait ou non vérifiable. Distinguer réussites, échecs, non-exécutions et limites ; relier chaque suite recommandée à un écart. Une preuve locale n'atteste pas un déploiement. Ne pas déclarer l'exigence entièrement satisfaite à partir du seul statut d'epic, d'une mention documentaire ou d'un nombre total de tests verts.
