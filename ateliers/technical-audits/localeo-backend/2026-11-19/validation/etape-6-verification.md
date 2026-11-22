# Vérification finale et inventaire de l’archive

Exécution `2026-11-19`, finalisée par la demande d’étape 6. Les décisions de correction ne sont pas reçues. **Aucun livrable requis manquant**, aucun prompt manquant reconstruit. L’archive reste locale, non committée ; aucun dépôt distant ni sauvegarde externe attesté.

## Livrables contrôlés

| Groupe | Présence vérifiée | Statut |
| --- | --- | --- |
| Prompts | Six demandes réellement utilisées, 01 à 06 ; un prompt de relance nouveau et non exécuté | 7 présents ; concordance des six demandes relue avec la conversation, cinq premiers fichiers inchangés |
| Cartographie | Architecture, stack, catalogue API, flux critiques, configuration/ressources, limites, orchestration | 7 présents |
| Analyses indépendantes | CPU, mémoire, concurrence, persistance, API, SRE | 6 rapports ; respectivement 2/4/3/3/3/2 constats majeurs, tous ≤5 |
| Annexes des spécialistes | Une par mission | 6 présentes |
| Consolidation / contradiction | Consolidation, causes racines, contre-expertise, débats et votes | 4 présents ; 17 constats couverts par 14 causes candidates |
| Backlogs et recommandations | Préliminaire, secondaires, plan de mesures, backlog mesuré, final, quick wins, plan d’optimisation | 7 présents ; huit corrections principales |
| Benchmarks | Protocole, résultats, limites, profils CPU, profils mémoire | 5 présents ; provenance des tentatives 03/04 et arrêts conservée |
| Décisions | Registre d’étape 5 | Présent, huit choix toujours vides |
| Synthèse | Rapport exécutif, roadmap conditionnelle, comparaison historique | 3 présents ; aucune évolution quantitative entre protocoles différents |
| Index final | README du dossier | Présent, métadonnées et limites finalisées |

Total : **47 fichiers requis vérifiés**, hors fichiers auxiliaires de validation et index secondaires. [Inventaire détaillé et contrôles](etape-6-controles.json), [registre des prompts et empreintes](etape-6-prompts.json). La présence d’un document de mesure n’implique pas que tous ses scénarios ont été exécutés.

## Intégrité et conservation

À l’entrée de l’étape 6, 86 fichiers existaient dans cette exécution. **Seul README.md est modifié**, à la demande expresse de finalisation ; son contenu antérieur exact est conservé dans [readme-avant-archivage.txt](readme-avant-archivage.txt) et son SHA256 correspond à la baseline. Cette capture textuelle se lit dans le contexte de son ancien emplacement README.md ; elle n’est pas un guide déplacé dont les liens auraient été réécrits. Tous les autres fichiers préexistants, dont prompts 01–05, rapports, mesures et décisions, sont inchangés. La [baseline d’archivage](etape-6-baseline.json) en porte les empreintes.

Aucune autre exécution datée de cette série ne préexiste. Les 22 fichiers historiques sous `docs/audits/backend/` sont vérifiés inchangés ; ils ont uniquement été consultés pour la comparaison. La réserve de l’ancien catalogue est explicitée dans cette comparaison, sans réécrire la consolidation ni créer une neuvième correction. Les travaux utilisateur hors audit sont préservés.

Les 14 artefacts du manifeste d’étape 4 existent toujours dans le backend ignoré et leurs empreintes concordent. Ils ne sont ni déplacés ici ni rejoués. Aucun résultat CSV partiel perdu lors de la tentative 03 n’est reconstitué. Ces artefacts hors Git restent une dépendance de reproduction exacte : s’ils disparaissent, le protocole reste disponible mais l’original ne peut pas être prétendu récupéré.

Le [manifeste final](manifest-archive.json) contient chemins relatifs, tailles et SHA256 des fichiers du dossier ; lui-même et [son empreinte](manifest-archive.sha256) sont exclus de sa liste pour éviter une référence circulaire. Vérification finale par recalcul après génération. Il s’agit d’intégrité locale, pas d’une signature ou d’une preuve de sauvegarde distante.

## Contrôles techniques et confidentialité

Contrôle UTF-8, parsing des JSON, présence des chemins, existence/plage de **1 771 références fichier/ligne** et liens Markdown locaux. `py -3.14 scripts/check_guidance.py` : **118 guides / 1 758 liens, zéro erreur et avertissement** ; [rapport général](etape-6-guidance.json). Tous les Markdown de l’audit ajoutés via `--document` : **155 guides/documents / 3 436 liens, zéro erreur et avertissement** ; [rapport ciblé](etape-6-liens.json). Le [premier passage](etape-6-liens-premier-passage.json) conserve 36 erreurs : la capture exacte du README avait été interprétée comme un guide Markdown déplacé, et deux rapports n’existaient pas encore lors de leur premier contrôle. Capture renommée en .txt sans altérer ses octets, rapports générés, puis contrôle relancé. Aucune source historique ou assertion affaiblie. Les ancres Markdown et les sites externes ne sont pas vérifiés automatiquement par l’outil de liens ; les liens de preuve source sont contrôlés par fichier et ligne.

3 405 fichiers backend suivis de la baseline hors dotenv privés sont identiques ; checkout backend et trois frontends propres. Les SQL suivis n’ont pas changé. Aucun test applicatif, benchmark, accès base/fournisseur, migration, installation, commit, push ou déploiement exécuté pendant l’archivage. Cette vérification porte sur les actions de l’audit, pas sur un état de déploiement externe inconnu.

Aucun secret détecté par relecture ciblée/provenance et recherche de clés privées, jetons fournisseurs, clés AWS, JWT, identifiants dans URL et affectations littérales sensibles. Les sorties ne contiennent que règles/emplacements éventuels, jamais les valeurs suspectes. Aucun dotenv privé ou fichier d’accès n’est lu pour ce contrôle. Cette recherche ciblée n’est pas une certification exhaustive de tout format de secret possible ; les noms de variables et empreintes SHA ne sont pas des secrets.

## Revues indépendantes et inconnues conservées

Deux sous-agents en lecture seule pour l’étape 6 : historique/code et revue de l’archive/rejouabilité, sans ressources de test partagées. Avis favorable sans réserve bloquante. Le prompt de relance impose un contexte neuf aux six spécialistes (`fork_turns="none"` si disponible) pour que les conclusions historiques lues par l’orchestrateur ne contaminent pas leurs premières analyses.

Inconnues et validations non acquises : modèle exact/effort des agents, configuration et ressources déployées, environnement HTTP/PostgreSQL représentatif, SLA produit, mesures après correction et choix utilisateur. Ces éléments sont signalés, pas remplacés par des valeurs supposées. Deux mécanismes mesurés localement et un bail simulé ne prouvent aucune capacité de production. Aucun gain après correction mesuré.

## Reprise

[RELANCER-AUDIT.md](../prompts/RELANCER-AUDIT.md) permet de sélectionner le dernier protocole, créer une nouvelle exécution date/suffixe, réinspecter le code et les commits, lancer six analyses indépendantes, contredire/consolider, mesurer seulement sur cible sûre, comparer puis attendre le choix utilisateur. Toute exécution future préserve ce dossier et les bruts antérieurs. Les huit corrections du [registre](decisions.md) restent non arbitrées à la clôture documentaire.
