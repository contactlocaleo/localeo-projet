# Plan de mesures ciblées

Exécution autorisée immédiatement limitée aux composants du [protocole](../benchmarks/protocole.md), propriétaire orchestrateur. Les campagnes ci-dessous sont **NON EXÉCUTÉES**, aucune cible HTTP/PostgreSQL jetable n'étant désignée par la demande. La présence d'un lanceur ou client psql ne vaut pas désignation. Aucun budget produit accepté.

| Question | Scénario synthétique proposé | Preuves attendues |
| --- | --- | --- |
| Async image/ERP et QR | Un adaptateur synchrone lent/bloqué, un dépôt ou batch puis une lecture légère ; lancer à 1 concurrent avant tout palier | Progression du témoin, p50/p95/p99 HTTP, erreurs, CPU, threads/pool ; identité, sessions, reçu et rollback |
| Inscription / capacité | Même animation à N puis 10N inscrits ; deux inscriptions distinctes, même email/reçu, dernier crédit/plafond et scan/clôture concurrents | Temps SQL et durée de coordination exclusive ; nombre actuel/compteur exact, premier inscrit, token/outbox et état final identiques |
| QR/PIN cadence | 0/59/60/61 preuves puis historique synthétique plus grand, tous statuts ; annulations avec dates égales | SQL/rows/allocations, règle domaine et référence de régularisation inchangées ; plans avec index déjà livrés |
| Notifications publication/résultat | Une commune cible constante, installations étrangères N/10N ; une installation avec plusieurs participations dont une gagnante | Ciblage, source_key et déduplication ; lignes lues/insérées, mémoire Python/RSS, temps de commit et rollback |
| Tirage Coffrets | Population gelée N/10N, peu de lots puis plus de lots ; rejeu/concurrence | Profil chargement UUID, copies Python, temps sous verrou ; uniformité, rangs, gel et absence de double gain |
| Médias Live | Animation sans média, local rapide puis stockage double lent/trickle/corrompu, même projection autorisée | SQL/stockage/décodage/base64 séparés ; fermeture Body, budget restant et erreurs ; pas de capacité extrapolée d'un double |
| Passeport | 1/10/50 commerces distincts, identity map froide/chaude | SELECT réels, octets/mapping, ordre et adresse ; absence d'un commerce, même JSON |
| Pilotage / gains | Même page/cible avec N/10N participants et tenants étrangers, puis gains sur plusieurs pages | Agrégats/totaux équivalents, page préservée, durée serveur et premier rendu distincts, SQL/allocations et réponse obsolète |
| Baux/outbox | Deux lanceurs, fournisseur lent puis accepté/crash, avant/après échéance et perte de propriétaire | Durée cycle, âge file, réservations, verrous/connexions et rapprochement ; aucun doublon ou message non commencé faussement incertain |

Avant toute campagne intégrée future : explicitement désigner la cible jetable et ses ressources/versions/migrations, seed et empreinte, limites de réseau, fournisseurs doubles, concurrence/durée/outils, budgets et procédure d'arrêt. Commencer à 1, mesurer retour à la normale avant hausse conditionnelle ; pas de 50/100 utilisateurs par défaut. Fixer séparément seuils RSS/CPU/pool/erreurs/latence propres à cette cible avant lancement. Échauffement et profils doivent être séparés des fenêtres temporelles, mêmes jeux/caches/versions avant/après. Une limite dépassée ne se relève pas pour obtenir un succès.

Pas de capacité ou gain démontré tant que la méthode ne couvre pas le parcours réel. Les essais de domaine/AST/SQLite n'exercent ni proxy, réseau, workers, PostgreSQL ou effets fournisseurs. Toute mesure future après correction requiert un choix distinct ; aucune correction implémentée dans cet audit.
