# Vérification de l’étape 4

Relecture indépendante par le sous-agent `validation_benchmarks`, sans exécution de sa part et après inspection directe des quatre handlers ERP, BatchRunner, outbox email, service export et producteur CSV. Il a corrigé la structure de compteur Windows du harness, souligné la granularité CPU et refusé un déclassement global du CSV fondé sur le seul petit jeu. L’orchestrateur conserve OPT-06 en P2 conditionnel. Aucune délégation des ressources d’exécution : un seul processus de mesure à la fois, sous responsabilité de l’orchestrateur.

Quatre tentatives conservées dans [le manifeste expurgé](etape-4-manifeste.json). Tentative 01 : échec instrumentation avant mesure ; 02 : échec extraction dataclass ; 03 : M01/M02 complets puis arrêt au seuil de temps de profilage CSV ; 04 : CSV seul, volumes réduits, succès. Les résultats intermédiaires CSV de 03 ne sont pas utilisés. Le seuil n’a pas été relevé. Réseau et PostgreSQL bloqués par le lanceur isolé ; SQLite ne reçoit que des données synthétiques en mémoire. Aucun app.main ou dotenv privé chargé.

Résultats retenus : M01/M02 de `results-attempt03.json`, M06 de `results-attempt04.json`, avec hashes des sources et des quatre harness. Deux P1 et six P2 maintenus, aucun P0 ; aucune optimisation implémentée, aucun gain après correction mesuré. Ni capacité HTTP, ni pool PostgreSQL, ni OOM de déploiement démontrés.

Vérifications exécutées : 3 405 fichiers suivis du backend contrôlés par SHA256, aucun changement ; douze rapports spécialisés/annexes identiques à la baseline de l’étape 3 ; sept livrables/prompt présents ; 31 références fichier/ligne valides ; 14 artefacts bruts vérifiés par empreinte. 240 tours M01, 21 exports chronométrés et neuf profils d’allocations CSV retenus. [Contrôles structurés](etape-4-controles.json).

`py -3.14 scripts/check_guidance.py` : 118 guides, 1 733 liens, zéro erreur/avertissement ; contrôle additionnel des documents d’étape 4 : 103 guides/documents, 1 519 liens, zéro erreur/avertissement. [Rapport général](etape-4-guidance.json), [rapport ciblé](etape-4-liens.json). Revue finale indépendante favorable, aucune réserve bloquante. Aucun test métier ou contrôle de capacité n’est remplacé par ces contrôles de liens. Les rapports spécialisés, la consolidation et le backlog préliminaire restent historiques et ne sont pas réécrits pour présenter les mesures comme disponibles aux étapes précédentes. Aucun fichier exporté via documentation.exports.json modifié, donc contrôle des sources exportées non requis ici.

Dépôt documentaire modifié uniquement sous ce dossier d’audit ; travaux utilisateur `docs/ux-workshops/localeo-crm/` préservés. Backend : seuls harness/profils/sorties ignorés dans `tmp/performance-stage4-2026-11-19/` ; aucun fichier applicatif suivi modifié. Aucune migration, donnée réelle, installation, commit, push ou déploiement.

L’étape 5 attend l’autorisation utilisateur.
