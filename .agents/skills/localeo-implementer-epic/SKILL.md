---
name: localeo-implementer-epic
description: Implémenter une epic Localeo à partir de sa spécification canonique, relier les critères d'acceptation aux tests et traiter les impacts entre dépôts. Ne pas déclencher pour une demande de plan seul, de cadrage ou une simple retouche rédactionnelle.
---

# Implémenter une epic Localeo

Lire le [guide transverse](../../../AGENTS.md), la spécification ciblée et la section « Implémenter et vérifier » du [cycle d'epic](../../../docs/organisation/cycle-epic.md). Lire les instructions des applications touchées et leur statut Git avant d'éditer.

1. Vérifier les critères de préparation et les décisions du périmètre demandé. Compléter une omission technique évidente et autorisée ; conserver explicitement les décisions métier non tranchées, sans développer leur branche dépendante. Ne pas recadrer toute l'epic pour une livraison partielle demandée.
2. Relier les critères de cette livraison aux tests existants ou à créer. Pour un bug, reproduire le comportement fautif par une preuve ciblée lorsque possible. Réutiliser [localeo-invariants](../localeo-invariants/SKILL.md) pour choisir le propriétaire et les scénarios significatifs.
3. Implémenter par incréments et vérifier ensemble producteurs, schémas et consommateurs modifiés. Respecter les guides locaux et le runner isolé du backend. Des travaux parallèles utilisent des fichiers ou worktrees distincts ; préserver tous les changements qui ne relèvent pas de la tâche.
4. Examiner la matrice des impacts de la spécification : documentation fonctionnelle, exploitation, migrations, contrats, fixtures et générateur de démonstration. Mettre à jour les sources canoniques et les consommateurs concernés dans la même livraison logique. Justifier les éléments sans objet.
5. Exécuter les tests proportionnés puis les contrôles requis. Ne pas remplacer un test métier par un build, masquer un échec par un skip ou annoncer une régression préexistante sans preuve. Distinguer réussite, échec, non-exécution et dette étayée ; un test ignoré n'est pas une réussite.
6. Pour une règle ou un contrat transverse sensible, faire relire indépendamment le diff et les tests avec le profil adapté. Intégrer les constats, vérifier les corrections et remplir le bilan d'acceptation du cycle. Une revue ne remplace pas les tests.
7. Rapporter le comportement livré, les dépôts et fichiers modifiés, les résultats et limites. Appliquer les critères de fin du cycle au périmètre réellement livré ; ne pas clôturer l'epic entière si une partie reste ouverte. Commit, push et déploiement suivent la demande courante et ne sont pas déduits de ce skill.
