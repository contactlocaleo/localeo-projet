---
name: localeo-verifier-exigence
description: Vérifier la prise en compte d'une exigence Localeo dans les spécifications, l'implémentation et les preuves de comportement, avec traçabilité et écarts entre dépôts. Utiliser pour une demande de conformité ou de couverture ciblée, même sans identifiant d'epic. Ne déclenche pas à elle seule une correction ni une évolution produit.
---

# Vérifier une exigence Localeo

Lire le [guide transverse](../../../AGENTS.md), les sources utiles dans l’[index des spécifications](../../../docs/specifications/INDEX.md) et la [roadmap](../../../docs/roadmap/README.md), puis les instructions des seules applications concernées.

## Établir et suivre l’attente

Reprendre exigence, source, version applicable et ID lorsqu’ils existent. Décomposer en résultats observables (acteur, préconditions, déclencheur, succès, refus et effets interdits). Garder les IDs ; de simples repères locaux suffisent sans epic. La demande explicite peut être examinée même si sa source est introuvable. Une epic terminée ne prouve pas une évolution ultérieure.

Distinguer demande, spécification et observation. Une divergence n’autorise pas à redéfinir l’exigence ; une ambiguïté qui change le verdict doit être clarifiée, en poursuivant les parties indépendantes. Délimiter la conclusion : documentaire si demandé, sinon code et preuves locales ; cible déployée seulement si identifiée et accessible.

Suivre chaque critère jusqu’aux fichiers et appels effectifs : propriétaire domaine et entrées pour une règle ; producteur, source canonique, générateur, copie et consommateurs pour un contrat ; données, projection et rendu pour un parcours. Une recherche de mots-clés localise mais ne prouve ni conformité ni absence. Utiliser [localeo-invariants](../localeo-invariants/SKILL.md) si la règle, transition ou frontière exige cette revue ciblée.

## Preuves et portée des actions

Appliquer le [noyau des preuves](../../../docs/organisation/cycle-epic.md#documenter-les-preuves-et-préparer-la-livraison) et les [seuils proportionnés](../../../docs/organisation/cycle-epic.md#choisir-les-contrôles-et-la-revue-selon-le-risque) : assertions et résultats sur l’arbre courant, fraîcheur des rapports, impacts et absences justifiées. Un prompt ne garantit pas sa sortie ; examiner le résultat réel sans inventer de nouveau refus serveur. Si une preuve manque, donner le scénario discriminant et ses prérequis.

La vérification seule conserve code applicatif et statuts ; les sorties temporaires restent possibles. Écrire dans le suivi canonique seulement si demandé. Si correction ou évolution est déjà autorisée, poursuivre avec [corriger](../localeo-corriger/SKILL.md) ou [faire évoluer](../localeo-faire-evoluer-epic/SKILL.md), puis revérifier ; sinon recommander les suites sans les implémenter.

## Verdict traçable

Présenter d’abord les écarts bloquants, leur effet observable et leur preuve, puis une matrice courte dans le support demandé ou le compte rendu :

| Critère | Source applicable | Code et consommateurs | Preuve, version et limites | Verdict / suite |
| --- | --- | --- | --- | --- |
| ID ou repère | Chemin et décision | Fichiers et comportement observé | Test/commande/rapport, contexte et résultat ou scénario manquant | État justifié et action ciblée |

- **Vérifié** : preuves adaptées au périmètre, sans écart ouvert sur ce critère.
- **Partiel** : nommer les parties couvertes et celles qui restent absentes/non vérifiées.
- **Non satisfait** : contradiction établie, avec scénario et preuve.
- **Non vérifiable en l’état** : preuve, accès ou arbitrage insuffisant ; préciser la condition pour conclure.
- **Sans objet** : hors périmètre applicable, avec raison.

Le verdict global garde tous les critères ouverts visibles. Distinguer réussites, échecs et non-exécutions, ainsi que dépôt absent ou non examiné. Ni statut d’epic, ni mention documentaire, ni total de tests verts ne prouve seul une exigence entière. Une preuve locale n’atteste pas un déploiement.
