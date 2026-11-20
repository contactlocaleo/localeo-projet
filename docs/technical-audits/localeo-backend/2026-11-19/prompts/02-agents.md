# ÉTAPE 2 — AUDITS SPÉCIALISÉS MULTI-AGENTS

Tu es l'orchestrateur des audits de performance du backend Python Localeo.

## 1. Préparation

Charge les livrables de cartographie de l'étape 1.

Archive ce prompt dans `prompts/02-agents.md`.

Utilise de véritables sous-agents Codex indépendants si disponibles.

Sinon, réalise des analyses séparées et signale cette limitation.

Les agents ne doivent pas consulter les conclusions des autres avant de finaliser leur première analyse.

**Chaque agent doit inspecter directement le code source.**

## 2. Missions des agents

### Agent 1 — CPU et algorithmes

Analyse :

- Complexité algorithmique.
- Boucles coûteuses.
- Calculs répétitifs.
- Sérialisation.
- Transformations inutiles.
- Traitements CPU-bound.

Livrable : `agents/01-cpu.md`

### Agent 2 — Mémoire Python

Analyse :

- Chargements massifs.
- Collections non bornées.
- Copies inutiles.
- Allocations.
- Rétention d'objets.
- Buffers et fichiers volumineux.

Livrable : `agents/02-memoire.md`

### Agent 3 — Concurrence

Analyse :

- Event loop.
- Async/await.
- Appels bloquants.
- Workers.
- Threads et processus.
- Timeouts.
- Contention.

Livrable : `agents/03-concurrence.md`

### Agent 4 — Persistance

Analyse :

- Requêtes répétitives.
- N+1.
- Pagination.
- Transactions.
- Connexions.
- Pools.
- Chargements excessifs.

Adapte l'analyse à la technologie réellement utilisée.

Livrable : `agents/04-persistance.md`

### Agent 5 — Performance API

Analyse :

- Chemins d'exécution.
- Traitements coûteux.
- Dépendances externes.
- Payloads.
- Sérialisation.
- Appels redondants.
- Latence potentielle.

Livrable : `agents/05-api.md`

### Agent 6 — SRE et capacité

Analyse :

- CPU et RAM.
- Workers.
- Limites des conteneurs.
- Saturation.
- Timeouts.
- Observabilité.
- Risques sous charge.

Livrable : `agents/06-sre.md`

## 3. Limitation des constats

**Chaque agent doit présenter au maximum cinq anomalies majeures dans son rapport principal.**

Classe-les selon :

1. Impact potentiel.
2. Probabilité de survenue.
3. Criticité du flux métier.
4. Niveau de preuve.
5. Facilité de correction.

Les problèmes secondaires sont consignés dans une annexe séparée.

Ne remplis pas artificiellement les cinq places : si deux problèmes seulement sont significatifs, présente uniquement ces deux problèmes.

## 4. Contrat de preuve obligatoire

Pour chaque anomalie :

- Identifiant.
- Domaine.
- Fichier et lignes.
- Fonction ou méthode.
- Mécanisme technique.
- Flux métier concerné.
- Conséquence possible.
- Conditions de déclenchement.
- Preuve dans le code.
- Mesure disponible.
- Niveau de confiance.
- Correction minimale.
- Effort S/M/L/XL.
- Risque de régression.
- Breaking change : oui/non.

Classe les constats :

- CONFIRMÉ PAR MESURE.
- FORTEMENT ÉTAYÉ PAR LE CODE.
- HYPOTHÈSE À VÉRIFIER.

N'invente aucune mesure ni aucun gain.

## 5. Analyse transverse obligatoire

Chaque agent doit indiquer les autres domaines susceptibles d'être affectés par son constat.

Exemple : un chargement excessif peut affecter simultanément la persistance, la mémoire et la sérialisation.

Signale les causes racines possibles sans consulter les autres rapports.

## 6. Contraintes

Aucune modification applicative.

Aucun benchmark non autorisé.

Aucune migration.

Aucun déploiement.

Aucun refactoring.

## 7. Fin d'étape

Vérifie les six rapports.

Présente les cinq constats majeurs au maximum par agent.

Ne consolide pas encore les résultats.

Attends mon autorisation avant l'étape 3.
