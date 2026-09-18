# Consolidation finale de la documentation backend — 18 septembre 2026

Les dernières copies documentaires ont été retirées de `localeo-backend`. Les sources sont dans `localeo-projet` et leurs consommateurs ont été adaptés. Les cinq dépôts restent indépendants. Aucun commit, push, publication juridique ni déploiement n’a été effectué.

## Résultat

| Ensemble initial | Traitement |
| --- | --- |
| 106 documents exportés sous backend/docs | Copies supprimées après vérification, sans divergence locale. |
| 2 exemples JSON et 1 script PowerShell sous docs | Relocalisés dans les scripts backend ; copies projet identiques retirées. |
| 2 contrats OpenAPI backend | Consolidés dans le projet ; exemplaires backend supprimés. |
| Ancien docs/README.md et documentation.snapshot.json backend | Retirés ; remplacés par l’entrée README et la préparation explicite du bundle. |
| 4 PDF juridiques sous output/pdf/v1.1 | Doublons identiques supprimés. |
| 4 DOCX et leur manifeste | Déplacés dans livrables/juridique/v1.1 ; chemins corrigés et empreintes vérifiées. |
| 9 PDF de procédures | Déplacés dans livrables/exploitation/backend, octets inchangés. |
| Recueil PDF de procédures | Conservé dans livrables/exploitation/backend/archives comme historique. |
| PDF de reversements manuels | Supprimé : flux décommissionné par EPIC 39, sans repli manuel selon EPIC 12. |
| 2 ZIP de maquettes Animation | Déplacés dans livrables/design/animation, V1 historique et V2 de référence. |

Les 112 fichiers initialement présents sous `backend/docs` sont traités ; ce répertoire est supprimé. Le [manifeste détaillé](migration-backend-2026-09-18.json) décrit 134 fichiers et outils, leurs empreintes initiales, destination et motif de traitement. Le manifeste initial garde la provenance et indique les destinations actuelles.

Le README backend a été réduit aux commandes et liens utiles : son historique V23–V71 existait déjà dans les releases du projet. La procédure performance canonique reprend tous les paramètres et commandes de l’ancienne notice longue. Les instructions de contribution, notices courtes des datasets et assets et licences des fontes restent près du code.

## Consommateurs et contrats

- ERP : résolveur commun, allowlist documentaire, anciennes URL conservées, configuration et PDF adaptés.
- CLI juridique : catalogue et profils dans la racine documentaire ; options explicites toujours disponibles.
- Générateurs OpenAPI : sortie canonique par défaut, option `--output` pour un backend isolé, export hors ligne sans secrets opérateur.
- EPIC 41 : 494 chemins et 344 schémas. Tous les anciens chemins sont conservés ; douze anciennes opérations absentes du code courant ont été retirées au profit des méthodes actuelles.
- EPIC 42 : 42 chemins et 344 schémas, dont cinq routes d’achat et paiement partagées. Toutes les références JSON internes des deux contrats sont résolues. Ils décrivent le code local, sans constituer une preuve de déploiement.
- Générateurs PDF : sources et sorties centralisées, neuf sources de procédures vérifiables sans génération.
- Tests du corpus transférés au projet ; tests backend autonomes avec fixtures.

Le backend lit le dépôt voisin ou `LOCALEO_DOCUMENTATION_ROOT`. Pour un déploiement isolé, suivre le [guide du bundle](../exploitation/technique/reference-documentation-centralisee.md). Ce bundle est un artefact généré et ignoré par Git. Aucun bundle n’a été laissé dans le backend pendant cette migration.

## Vérifications et limites

| Contrôle | Résultat |
| --- | --- |
| Workspace | Cinq racines Git distinctes, destinations présentes et anciens fichiers retirés. |
| Bundle réel | 116 documents et manifeste d’allowlist préparés dans Temp ; empreintes contrôlées contre les sources. |
| Synchroniseur | 15 tests réussis ; 1 ignoré faute de droit Windows de création de symlink. |
| ERP, configuration, résolveur et CLI | 47 tests ciblés réussis ; sources réelles vérifiées. |
| Générateurs OpenAPI | 10 tests ciblés réussis ; couverture des anciens chemins et références JSON vérifiée. |
| Sécurité PDF | 35 tests réussis. Conversion juridique optionnelle non rejouée : pdfplumber absent de cet environnement. |
| Corpus juridique | Empreintes et versions de 12 PDF publiables et 4 exclus vérifiées, ainsi que 4 paires PDF/DOCX de correction. |
| Architecture et contrôle d’empreintes backend | 380 tests réussis, 2 ignorés, 2 échecs préexistants de couverture métier. Les 469 fichiers d’entrée de ces deux contrôles sont identiques à la sauvegarde avant migration. |
| Structure des procédures | Résultats inchangés sur 42 procédures : 13 plans incomplets et 12 liens absents existaient déjà. Voir le [comparatif](controle-procedures-avant-apres-2026-09-18.md). |
| Liens | Aucun nouveau lien cassé. Deux liens préexistants vers le contrat absent de la Marketplace restent dans frontend-pwa.md et l’audit Marketplace du 6 septembre. |

La suite complète backend et la recette de déploiement n’ont pas été exécutées. Les exigences des contrôles historiques restent en place ; aucun échec n’a été masqué.

Les sauvegardes et bundles de contrôle restent dans le dossier temporaire `localeo-backend-docs-migration-20260918` de l’opérateur. Aucune donnée métier ou de démonstration, aucun secret, import ni base n’a été déplacé vers le dépôt documentaire.
