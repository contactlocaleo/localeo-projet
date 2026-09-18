# Localeo — projet transverse

Ce dépôt rassemble la connaissance produit, les décisions, les spécifications et les livrables des quatre applications Localeo. Chacun des cinq dépôts conserve son historique Git, ses commits et ses règles de livraison.

Ouvrir [localeo.code-workspace](localeo.code-workspace) dans VS Code, avec les cinq dossiers voisins. Le workspace organise l’éditeur ; il ne modifie pas les permissions d’un outil. Pour travailler sur plusieurs dépôts, démarrer l’agent dans un environnement autorisant explicitement les dossiers concernés.

| Dépôt | Responsabilité | Entrée locale |
|---|---|---|
| localeo-projet | Documentation, coordination et livrables | Ce fichier |
| localeo-backend | API FastAPI, domaine, données, ERP et traitements | [README](../localeo-backend/README.md) |
| localeo-marketplace | Marketplace publique et Localeo Live | [README](../localeo-marketplace/README.md) |
| localeo-commercant | Application et PWA commerçant | [README](../localeo-commercant/README.md) |
| localeo-animation | Interface des partenaires d’animation | [README](../localeo-animation/README.md) |

- [Produit](docs/produit/INDEX.md)
- [Architecture](docs/architecture/INDEX.md) et [conventions transverses](docs/architecture/transverse/README.md)
- [Spécifications par fonctionnalité](docs/specifications/INDEX.md), [moteur d’animation](docs/specifications/moteur-animation/localeo_animation_engine_spec.md)
- [Roadmap commune](docs/roadmap/README.md) et [anomalies](docs/roadmap/anomalies)
- [Exploitation](docs/exploitation/INDEX.md), [juridique](docs/juridique/INDEX.md), [audits](docs/audits/INDEX.md)
- [Livrables](livrables/INDEX.md) et [releases](releases/INDEX.md)
- [Compte rendu de réorganisation](docs/organisation/compte-rendu-reorganisation-2026-09-18.md)

## Modifier la documentation

Éditer les sources dans ce dépôt. Les contrats OpenAPI documentaires du backend sont également centralisés ici ; leurs générateurs restent dans le backend. Les lecteurs de l’ERP et les outils juridiques utilisent directement ce dépôt voisin ou la racine définie par `LOCALEO_DOCUMENTATION_ROOT`.

```console
python scripts/sync_documentation.py --check-sources
python scripts/check_workspace.py
python -m unittest discover -s tests
```

Pour livrer le backend seul, préparer un bundle non versionné puis vérifier ses empreintes. Les commandes, chemins et modalités de déploiement sont dans le [guide de documentation centralisée](docs/exploitation/technique/reference-documentation-centralisee.md). Le synchroniseur refuse d’écraser un bundle modifié localement. La CI backend teste les lecteurs et le contrôle d’intégrité sur des fixtures indépendantes ; le bundle réel se vérifie lors de la préparation du déploiement.

## Livrer une évolution

Identifier les applications affectées dans la spécification ; garder les détails propres à chaque moteur ou interface dans le même dossier métier. Réutiliser les identifiants d’arbitrage existants. Pour un changement transverse, vérifier et commiter séparément chaque dépôt concerné, puis renseigner les SHAs livrés dans un manifeste de release. Aucun sous-module ni dépôt Git parent n’est requis.

[repositories.json](repositories.json) décrit les chemins relatifs et les commandes. [Le manifeste initial](releases/reorganisation-2026-09-18.json) enregistre les HEAD avant réorganisation ; il ne représente pas une release déployée.
