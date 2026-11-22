# ÉTAPE 5 — ARBITRAGE DES OPTIMISATIONS BACKEND

Tu es chargé de préparer la décision finale sur les corrections de performance Localeo Backend.

## 1. Contexte

Lis :

- Les audits spécialisés.
- La consolidation.
- La contre-expertise.
- Les benchmarks.
- Le backlog révisé.

Archive ce prompt dans `prompts/05-validation.md`.

## 2. Objectif

Présenter un plan d'optimisation court, pragmatique et techniquement justifié.

Le plan doit privilégier :

- Les corrections locales.
- Les gains mesurables.
- Les faibles risques.
- L'absence de breaking change.
- La préservation des contrats API.
- La maîtrise des coûts de développement.

## 3. Classification

**A — Quick win**

Correction locale, faible risque, sans rupture.

**B — Optimisation ciblée**

Modification limitée avec bénéfice significatif plausible.

**C — Refactoring important**

Modification structurante ou risque élevé.

**D — Breaking change**

Modification incompatible avec les contrats ou comportements existants.

Privilégie A et B.

Les catégories C et D doivent rester exceptionnelles et faire l'objet d'une justification spécifique.

## 4. Fiche de décision

Pour chaque optimisation :

- ID.
- Cause racine.
- Flux métier concernés.
- API impactées.
- Références au code.
- Preuve.
- Mesures.
- Solution minimale.
- Alternative.
- Gain mesuré ou estimé.
- Effort S/M/L/XL.
- Risque de régression.
- Compatibilité.
- Tests nécessaires.
- Plan de retour arrière.
- Priorité.

## 5. Arbitrage

Présente les corrections P0/P1 et attends mon choix :

- VALIDÉE.
- REFUSÉE.
- À APPROFONDIR.
- REPORTÉE.

Ne présume jamais de ma décision.

Les votes simulés ne constituent pas une autorisation de développement.

## 6. Livrables

Crée :

- `recommandations/backlog-final.md`
- `recommandations/quick-wins.md`
- `recommandations/plan-optimisation.md`
- `validation/decisions.md`

Le backlog final doit contenir prioritairement 5 à 10 corrections maximum, sauf nécessité démontrée.

## 7. Contraintes

Aucune implémentation.

Aucun déploiement.

Aucune migration.

Aucune modification applicative.

Mets à jour le README et attends mon autorisation.
