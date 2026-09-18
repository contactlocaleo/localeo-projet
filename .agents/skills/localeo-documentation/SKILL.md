---
name: localeo-documentation
description: Réorganiser, fusionner ou déplacer la documentation Localeo entre ses cinq dépôts ; corriger ses liens, exports et consommateurs. Utiliser pour une migration documentaire, un audit des guides ou une consolidation de roadmap. Ne pas déclencher pour une simple correction de texte sans impact sur les chemins, les états ou les exports.
---

# Documentation Localeo

Lire le [guide transverse](../../../AGENTS.md) et le README du périmètre. Les chemins de cette fiche partent de son dossier ; les commandes ci-dessous s'exécutent depuis la racine de `localeo-projet`.

1. Examiner `git status` dans les dépôts concernés. Recenser sources, consommateurs exécutables, liens entrants et exports avant de déplacer un fichier. Préserver les modifications utilisateur et les fichiers ignorés ; ne pas transformer une demande de rangement en purge générale.
2. Déterminer la source canonique avec l'[index des spécifications](../../../docs/specifications/INDEX.md) et la [roadmap](../../../docs/roadmap/README.md). Un numéro applicatif peut désigner un autre epic : comparer le périmètre et les décisions, pas seulement le numéro. Le dossier d'état courant prime sur les anciennes stories.
3. Pour un doublon exact, comparer le contenu ; pour deux variantes, conserver les clauses et arbitrages uniques avec leur provenance. Une contradiction produit reste explicite tant qu'une décision ne la résout pas. Ne pas inventer un état ou une recette à partir d'une implémentation locale.
4. Modifier les sources documentaires dans `localeo-projet`, puis leurs lecteurs/liens. Les générateurs restent applicatifs ; un contrat JSON consommé par des tests frontend n'est pas un document supprimable sans adapter ces consommateurs. Appliquer le [contrat d'export](../../../docs/exploitation/technique/reference-documentation-centralisee.md) si `documentation.exports.json` est concerné. Ne pas versionner le bundle runtime.
5. Vérifier les guides avec `python scripts/check_guidance.py`. Pour un autre Markdown modifié, ajouter `--document chemin/relatif.md` ; pour les exports, lancer `python scripts/sync_documentation.py --check-sources`. Tester les lecteurs si leurs chemins ou formats changent. Examiner les liens entrants après une suppression. Distinguer dette historique et régression du changement.
6. Rendre les déplacements, fusions et suppressions traçables dans le compte rendu demandé. Indiquer les dépôts affectés et les vérifications réelles. Créer un rapport dédié seulement pour une migration ou un audit qui le justifie. Commits, push et déploiements suivent la demande en cours.

Pour un inventaire important, déléguer par dépôt avec des fichiers distincts. Conserver la décision de fusion et la vérification des références partagées dans une seule tâche d'intégration.
