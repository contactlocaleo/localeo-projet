# Vérification des six rapports — étape 2

Périmètre : qualité des rapports et traçabilité des preuves, après finalisation indépendante de chaque spécialiste. Ce document ne constitue ni une consolidation des anomalies ni une contre-expertise comparative de l’étape 3.

Six véritables sous-agents Codex ont été utilisés avec contexte séparé (`fork_turns=none`). Tous ont confirmé une lecture directe par shell et déclaré n’avoir consulté aucun autre rapport. Les spécialistes disposaient exclusivement de leur mission et des chemins vers instructions, prompt et cartographie. Les sources et les relevés de lecture sont documentés dans leurs annexes ; la limite d’outillage rencontrée lors de l’étape 1 n’a pas empêché ces missions.

| Rapport | Constats majeurs | Vérification de contenu |
| --- | --- | --- |
| CPU | CPU-01, CPU-02 | Matérialisations et filtres du pilotage, mappers repositories, puis pagination et qualification historiques relus directement ; modes et moteurs optimisés explicitement distingués |
| Mémoire | MEM-01 à MEM-04 | Chargements du dashboard, décodage et conservation des rasters OnBoard, copies de population gelée, tampon CSV et fenêtre temporelle relus |
| Concurrence | ASY-01 à ASY-03 | Handlers ERP async, appel direct du handler batch, réservation/transaction pendant fournisseur et acquisition/libération/échéance du verrou relus |
| Persistance | DB-01 à DB-03 | Branche historique, sélection verrouillée et relations ORM de l’expiration, filtre de relances après LIMIT et index livrés relus |
| API | API-01 à API-03 | Projection du dashboard, hydratation après fermeture UoW, validation WebP, budget et adaptateur S3, retour Stripe et expansions relus |
| SRE | SRE-01, SRE-02 | Durée de bail et timeout client distincts du handler, executor unique, appels HTTP bloquants, calendrier des jobs et surcharge des crons relus |

Chaque constat principal comporte identifiant, domaine, fichiers/lignes, symbole, mécanisme, flux/entrée, conséquences et déclencheur, preuve source, absence de mesure disponible, confiance, correction minimale, effort, risque et breaking change. Les effets possibles sur d’autres domaines et les causes candidates sont indiqués indépendamment. Les cinq axes de classement sont explicités par rapport. Aucun rapport ne dépasse cinq anomalies ; les observations secondaires et contre-exemples sont séparés en annexe. Les classifications des majeurs sont toutes **FORTEMENT ÉTAYÉ PAR LE CODE** ; aucune mesure, reproduction d’incident, performance acquise ou gain chiffré n’est inventé.

Retouches après premières versions : préfixes `/protected` des chaînes CPU et `/internal` de la chaîne OnBoard mémoire ; ajout de liens et de la révision au rapport concurrence, correction d’une ligne de commit email ; référence de la route retour de paiement et catégorie d’effort API-03 normalisée à M. Ces retouches sont documentaires, signalées dans les rapports concernés et n’ajoutent ni constat ni rapprochement entre missions. La proposition mémoire de nouveaux refus d’images est explicitement marquée breaking change et n’est pas autorisée à l’implémentation ; privilégier une optimisation compatible avant tout arbitrage futur.

Les contrôles automatisés finaux sont enregistrés dans [etape-2-controles.json](etape-2-controles.json) : présence des six rapports et annexes, plafond de cinq, existence des liens, validité des références de lignes, empreintes des rapports et intégrité du backend. Les contrôles documentaires figurent dans [etape-2-guidance.json](etape-2-guidance.json) et [etape-2-liens.json](etape-2-liens.json). Les états provisoires restent conservés comme tels.

Résultats : contrôle transverse des guides réussi (118 guides, 1697 liens, zéro erreur) ; contrôle ciblé final réussi après création de son rapport JSON ; six rapports et six annexes présents, aucun lien source invalide ni dépassement du plafond. Le premier passage ciblé avait signalé uniquement le lien vers son propre rapport, qui n’était créé qu’en fin de commande : [premier passage conservé](etape-2-liens-premier-passage.json). La création de ce fichier a résolu la référence ; le passage final est conservé séparément. `git diff --check` réussit ; aucun test métier ne découle de ces contrôles.

Le backend reste au commit `7049e7fafc76f9119924f1082a5ee7457a175d85`, avec arbre propre et empreintes des 3405 fichiers suivis hors dotenv identiques au relevé initial. Aucun code applicatif, contrat consommé, critère d’acceptation, migration, paramètre d’exploitation ou générateur n’est modifié : absence d’impact d’exécution de ces livrables documentaires. Seul le dossier de cet audit dans `localeo-projet` reçoit des écritures ; les modifications utilisateur voisines restent préservées.

Aucun test métier, benchmark, profilage, test de charge, import applicatif, connexion base, appel fournisseur, migration, déploiement ou refactoring exécuté. Les vérifications de liens ne remplacent aucune preuve de capacité. Les ressources et versions effectivement déployées restent inconnues. Aucun export documentaire modifié : contrôle de sources exportées non requis pour cette étape.

Arrêt demandé : les rapports restent séparés, sans registre de causes communes alimenté, sans ticket, sans dédoublonnage et sans priorité transverse. Attendre l’autorisation utilisateur avant l’étape 3.
