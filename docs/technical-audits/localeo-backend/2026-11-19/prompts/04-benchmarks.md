# ÉTAPE 4 — BENCHMARKS ET VALIDATION DES HYPOTHÈSES

Tu es chargé de mesurer les principaux risques identifiés lors de l'audit multi-agents Localeo Backend.

## 1. Contexte

Lis :

- Les audits spécialisés.
- La consolidation.
- Les causes racines.
- La contre-expertise.
- Le backlog préliminaire.
- Le plan de mesures.

Archive ce prompt dans `prompts/04-benchmarks.md`.

## 2. Objectif

Confirmer ou infirmer les problèmes prioritaires.

Ne benchmarke pas toutes les API.

Concentre les mesures sur les goulots identifiés et les flux métier les plus critiques.

## 3. Sécurité

Aucun test de charge en production.

Utilise uniquement un environnement isolé et autorisé.

Aucune modification durable du code applicatif.

Aucune modification de données métier réelles.

Si l'environnement de benchmark n'est pas disponible, prépare un protocole de mesure sans l'exécuter.

## 4. Outils

Sélectionne les outils adaptés à la stack réelle :

- cProfile.
- py-spy.
- tracemalloc.
- memray.
- scalene.
- Outils de benchmark HTTP.
- Outils de profiling de la persistance.

N'installe pas tous les outils sans justification.

## 5. Mesures

Lorsque possible :

- Latence p50, p95, p99.
- Débit.
- Taux d'erreur.
- CPU.
- Mémoire résidente.
- Allocations.
- Temps CPU par requête.
- Nombre d'accès aux données.
- Temps cumulé des accès.
- Saturation des workers et pools.

Documente les conditions :

- Matériel.
- Version Python.
- Configuration.
- Volumétrie.
- Concurrence.
- Durée.
- Outils.

## 6. Scénarios de charge

Prépare des niveaux progressifs adaptés aux ressources disponibles.

Exemples indicatifs :

- 1 utilisateur.
- 10 utilisateurs concurrents.
- 25 utilisateurs concurrents.
- 50 utilisateurs concurrents.
- 100 utilisateurs concurrents.

Fixe des seuils d'arrêt.

Ne cherche pas à saturer dangereusement l'environnement.

## 7. Validation des causes racines

Pour chaque problème :

1. Mesure le comportement actuel.
2. Vérifie le mécanisme suspect.
3. Identifie le goulot dominant.
4. Confirme ou infirme l'hypothèse.
5. Évalue la correction minimale.
6. Propose les mesures avant/après nécessaires.

Ne fabrique aucun gain chiffré.

Si le gain est inconnu, indique NON MESURÉ.

## 8. Révision du backlog

Réévalue les priorités selon les résultats.

Retire du backlog principal les hypothèses infirmées.

Déclasse les optimisations dont l'impact apparaît faible.

Conserve les problèmes non mesurables dans une catégorie distincte, avec leur niveau de confiance.

Maintiens un backlog principal de 5 à 10 optimisations maximum, sauf justification critique.

## 9. Livrables

Crée :

- `benchmarks/protocole.md`
- `benchmarks/resultats.md`
- `benchmarks/limites.md`
- `benchmarks/profils-cpu.md`
- `benchmarks/profils-memoire.md`
- `recommandations/backlog-mesure.md`

Pour chaque optimisation, distingue :

- Gain démontré.
- Gain plausible.
- Gain non mesuré.

## 10. Fin d'étape

Présente les goulots confirmés, les hypothèses infirmées et le backlog révisé.

Ne modifie aucun code applicatif.

Attends mon autorisation avant l'étape 5.
