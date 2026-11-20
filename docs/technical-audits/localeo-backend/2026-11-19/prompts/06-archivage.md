# ÉTAPE 6 — ARCHIVAGE ET REJOUABILITÉ AUDIT PERFORMANCE LOCALEO BACKEND

Tu es chargé de finaliser l'archivage de l'audit multi-agents.

## 1. Répertoire

Utilise :

`docs/technical-audits/localeo-backend/YYYY-MM-DD/`

Ne modifie jamais les exécutions précédentes.

## 2. Prompts

Vérifie :

- `prompts/01-initialisation.md`
- `prompts/02-agents.md`
- `prompts/03-contradiction.md`
- `prompts/04-benchmarks.md`
- `prompts/05-validation.md`
- `prompts/06-archivage.md`

Enregistre cette instruction complète dans `prompts/06-archivage.md`.

Chaque fichier doit contenir le prompt réellement utilisé.

Ne reconstruis pas fictivement un prompt manquant.

## 3. Vérification des livrables

Contrôle :

- Cartographie.
- Rapports des six agents.
- Consolidation.
- Causes racines.
- Contre-expertise.
- Débats et votes.
- Backlog.
- Benchmarks.
- Plan d'optimisation.
- Décisions.
- Quick wins.

Signale les éléments manquants.

## 4. Synthèse exécutive

Crée :

- `synthese/rapport-executif.md`
- `synthese/roadmap-performance.md`

Présente :

- Les principaux goulots.
- Les causes racines.
- Les problèmes confirmés.
- Les hypothèses non vérifiées.
- Les API à risque.
- Les corrections prioritaires.
- Les gains mesurés ou estimés.
- Les risques de régression.
- Les éventuels refactorings importants.

Distingue :

- Corrections immédiates.
- Optimisations à moyen terme.
- Évolutions architecturales futures.

## 5. Comparaison historique

Si un audit précédent existe, crée :

`synthese/comparaison-precedent.md`

Compare :

- Les problèmes corrigés.
- Les problèmes persistants.
- Les nouveaux risques.
- Les métriques comparables.
- Les performances API.
- Les évolutions CPU et mémoire.
- Les décisions précédentes.

Ne compare quantitativement que des mesures réalisées dans des conditions suffisamment similaires.

## 6. Métadonnées

Finalise le README avec :

- Date.
- Branche et commit.
- Stack réelle.
- Configuration matérielle connue.
- Modèles et niveaux de raisonnement connus.
- Périmètre.
- Méthodes.
- Benchmarks exécutés.
- Limitations.
- Nombre de problèmes consolidés.
- Nombre de causes racines.
- Nombre de corrections proposées.
- Nombre de P0/P1.
- Statut des validations.
- Statut final.

## 7. Rejouabilité

Crée :

`prompts/RELANCER-AUDIT.md`

Ce prompt doit permettre de :

1. Identifier le dernier protocole.
2. Créer un nouveau répertoire daté.
3. Réanalyser le code réel.
4. Comparer les commits.
5. Relancer les six agents.
6. Consolider par causes racines.
7. Réaliser la contre-expertise.
8. Rejouer les benchmarks sûrs.
9. Reprioriser les corrections.
10. Comparer les résultats historiques.
11. Préserver les anciens audits.
12. Attendre ma validation.

## 8. Vérification finale

Vérifie :

- L'intégrité des fichiers.
- Les chemins.
- L'absence de secrets.
- L'absence de modification applicative.
- L'absence de migration ou déploiement.
- La conservation des audits précédents.

Présente le répertoire archivé et le prompt de relance.

Ne réalise aucune implémentation.
