---
name: localeo-specifier-epic
description: Spécifier une epic Localeo cadrée en comportements, invariants, contrats et preuves attendues avant son implémentation. Utiliser pour une conception fonctionnelle ou technique transverse, pas pour créer un nouveau backlog ni pour coder une epic déjà spécifiée.
---

# Spécifier une epic Localeo

Lire le [guide transverse](../../../AGENTS.md), le backlog ciblé, son dossier dans l'[index des spécifications](../../../docs/specifications/INDEX.md) et la section « Spécifier » du [cycle d'epic](../../../docs/organisation/cycle-epic.md). Lire les guides applicatifs seulement pour les dépôts affectés.

1. Vérifier les critères d'acceptation et l'état produit courant. Examiner les producteurs et consommateurs réels pour documenter l'existant ; une intention de backlog ou un ancien bilan ne prouve pas un comportement courant.
2. Décrire les parcours et leurs refus significatifs : acteur, préconditions, action, résultat, effets conservés ou interdits. Garder des identifiants stables de critères dans l'epic. Rendre les hypothèses et décisions ouvertes explicites.
3. Appliquer [localeo-invariants](../localeo-invariants/SKILL.md) pour les règles, transitions et contrats partagés. Identifier le propriétaire de domaine avant les endpoints. Adapter le [modèle d'architecture](../../../docs/architecture/templates/epic-architecture-template.md) dans le dossier canonique ; ne pas dupliquer une conception existante ni créer une spécification vide.
4. Décrire le contrat et sa compatibilité, les changements de données, les permissions, la concurrence et les effets secondaires lorsqu'ils sont concernés. Relier chaque critère aux preuves prévues et aux impacts documentation/démonstration/exploitation dans la matrice du cycle. Distinguer les tests prévus des tests exécutés.
5. Relever les obstacles à l'implémentation selon les critères de préparation du cycle. Une incertitude qui affecte une décision métier reste bloquante pour la partie dépendante ; poursuivre la conception indépendante. Ne pas transformer une exception d'architecture en arbitrage implicite.
6. Contrôler les liens des documents modifiés et, si des sources exportées changent, `python scripts/sync_documentation.py --check-sources`. Présenter décisions, chemins canoniques, tests à produire et limites. La validation de liens ne valide pas la conception métier.

Pour un contrat transverse complexe, confier une revue en lecture seule au profil `localeo-contract-reviewer`, avec fichiers précis et questions de compatibilité. Intégrer les constats avant de considérer la conception exploitable.
