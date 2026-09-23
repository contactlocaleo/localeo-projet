---
name: localeo-verifier-demonstration
description: Adapter et vérifier le générateur de démonstration Localeo après une évolution du domaine, des permissions, du schéma ou des contrats. Utiliser aussi pour une régression du jeu généré ; ne déclenche pas une génération sur un environnement réel.
---

# Compatibilité du jeu de démonstration

Lire le [guide transverse](../../../AGENTS.md), les [invariants du générateur](../../../../localeo-backend/scripts/demonstration/AGENTS.md), puis seulement la partie concernée de la [recette canonique](../../../docs/exploitation/demonstration/realisation-recette.md). Les commandes applicatives s'exécutent dans `localeo-backend`.

1. Relier l'évolution aux modèles, migrations, permissions, publications et lecteurs concernés. Examiner le registre du générateur et les tests `tests/unit/test_demonstration_*.py` correspondants. Une nouvelle table exige une politique explicite ; une relation valide ne prouve pas sa visibilité dans l'API.
2. Adapter les données et adaptateurs sous `scripts/demonstration/` aux interfaces ordinaires du produit. Ne pas créer de mode démo dans les applications ni contourner une règle métier. Signaler séparément un défaut produit découvert par le jeu.
3. Exécuter les tests unitaires ciblés avec le runner isolé du backend. Pour la compatibilité PostgreSQL, suivre le workflow `.github/workflows/demo-compatibility.yml` et son runner dédié : bases jetables explicitement gardées, migrations courantes, génération, vérification, dump/restauration et reprise après échec. Un skip ou une absence de PostgreSQL signifie « non exécuté ».
4. Vérifier un parcours observable affecté sur ce même jeu : catalogue public, participants/progression, lecture gestionnaire ou accès commerçant selon le changement. Réutiliser les repositories/API normaux ; ajouter une preuve navigateur quand la régression concerne leur présentation. Les tests de structure complètent ces preuves.
5. Distinguer ces contrôles des opérations Stripe/Brevo/S3 réelles. La [procédure opérateur](../../../docs/exploitation/demonstration/exploitation.md) porte leur préparation, cible et preuves privées. Une demande de compatibilité ne vaut pas autorisation de reset, d'envoi ou de transfert vers une base d'exploitation.
6. Rendre compte des versions du backend/générateur, migrations, scénarios exécutés, résultats et limites. Mettre à jour la recette ou la procédure canonique si le comportement opérateur change ; ne versionner ni accès, QR, données, dump ni journaux privés.
