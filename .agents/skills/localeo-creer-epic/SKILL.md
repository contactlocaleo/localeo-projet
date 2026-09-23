---
name: localeo-creer-epic
description: Créer ou recadrer une epic Localeo dans la roadmap commune à partir d'un besoin produit, avec périmètre et critères d'acceptation. Ne pas utiliser pour une correction ponctuelle sans demande d'epic, ni pour détailler une spécification déjà cadrée.
---

# Créer une epic Localeo

Lire le [guide transverse](../../../AGENTS.md), la [roadmap](../../../docs/roadmap/README.md) et la section « Cadrer » du [cycle d'epic](../../../docs/organisation/cycle-epic.md). Rechercher les epics et arbitrages du sujet avant de choisir un identifiant ; ne pas charger tous les backlogs.

1. Relever le problème observé, les acteurs, le résultat attendu et les contraintes exprimées. Distinguer constat vérifié, proposition et question ouverte. Réutiliser une epic existante quand la demande prolonge son périmètre ; ne pas rouvrir une epic terminée ni réinterpréter une fusion historique implicitement.
2. Définir le périmètre, les exclusions, les dépendances et des critères d'acceptation observables. Utiliser le [modèle de cadrage](../../../docs/architecture/templates/epic-cadrage-template.md) dans le backlog canonique ; conserver les rubriques pertinentes d'un document existant.
3. Pour une nouvelle epic, vérifier l'unicité de l'identifiant, y compris les namespaces applicatifs, et ajouter le fichier au dossier d'état approprié selon la roadmap. Mettre à jour les index et synthèses concernés. Ne pas inventer un état « prêt » parallèle aux états produit.
4. Remplir l'analyse d'impact initiale : applications, données de démonstration, contrats, documentation fonctionnelle et exploitation. À ce stade, un impact peut rester à examiner ; ne pas le déclarer sans objet par défaut.
5. Vérifier les liens avec `python scripts/check_guidance.py --document <chemin-du-backlog>` depuis `localeo-projet`. Rendre le cadrage, ses liens et les arbitrages encore nécessaires. Ne pas annoncer une spécification, une implémentation ou une livraison que ce travail n'a pas réalisée.

Continuer les éléments indépendants des questions ouvertes. Ne demander une décision que si elle change réellement le besoin, le périmètre ou un arbitrage produit ; un choix rédactionnel courant ne requiert pas d'approbation.
