# E78 — Vérification et livraison

L'[évolution partagée des essais limités du 22 novembre](../epic-77-juste-prix-local/verification-livraison.md#livraison-des-essais-limités--22-novembre-2026)
porte les preuves E77/E78-ESSAIS-01 à 08. Le budget configurable, le tampon
invalide et la qualification conservée au seuil remplacent l'essai unique des
nouvelles configurations ; les bilans et réserves historiques ci-dessous gardent
leur portée. Aucun changement de statut de l'epic.

Spécification du **15 novembre 2026**. Les seize critères restent ceux du
[backlog canonique](../../roadmap/en-cours/epic-78-jeu-des-vitrines-backlog.md).
Lire les [parcours](parcours-regles.md) et l'[architecture](architecture-contrats.md).
Les décisions produit sont résolues. Cette page conserve la matrice et les
preuves attendues définies le 15 novembre. Les résultats réellement exécutés
depuis le 16 novembre et leurs limites figurent dans le [bilan de réalisation](bilan-realisation.md).
Les contrôles de la phase documentaire sont conservés en fin de page.

## Matrice de traçabilité

| Critère | Comportement et propriétaire | Preuve prévue, résultat non exécuté | Documentation fonctionnelle / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| E78-CA-01 | Catalogue/offre et domaine Animation : créer le type dédié dans son contexte | Forfait standard autorisé, offre absente refusée, tenant/commune étrangers, aucun repli Passeport ou conversion d'une chasse | Assistant Animation/ERP ; type/version dans registres et contrats | Deux communes, organisateur autorisé/refusé | Déclaration ANIMATION standard distincte de l'activation technique |
| E78-CA-02 | Configuration/publication : règles explicites et prérequis complets | Seuil 0/1/N/N+1, absence du booléen de passage, booléen pris pour entier, 0/100/101 vitrines, dotation/accord/contrôle manquants ; publication refusée avec motif | Règlement, revue de publication, schéma privé | Brouillons prêts/incomplets ; 5 vitrines, seuil 3 | Migration additive, aucun contournement ERP |
| E78-CA-03 | PropositionVitrine : contenu privé du commerce principal | QCM 2..6 choix, un correct, IDs étrangers/dupliqués, champs trop longs, contenu échappé ; principal autorisé, salarié ou commerce voisin refusé | Pro, schéma de proposition, aperçu public et kit privé | Noël/Pâques, photo réelle facultative, contenu incomplet | DAM privé et rétention, aucun média inventé |
| E78-CA-04 | Proposition/contrôle/publication : révisions exactes | Modification après approbation, installation changée à contenu identique, contrôle obsolète, approbation ou publication concurrente ; aucun snapshot partiel | Contrats de révision, guide terrain, checklist organisateur | Installation non confirmée, contrôle périmé, contenu corrigé | Verrou de coordination, audit auteur/instant/révisions |
| E78-CA-05 | Accès Live et ciblage public | Catalogue, QR édition/vitrine, inscription puis retour à la cible ; ID étranger et client ne supportant pas E78 refusés | Routes/liens Live, flyer public | QR sans solution ni token personnel | Aucune surface de jeu concurrente dans Coffrets |
| E78-CA-06 | Politique de jeu : dates/statuts serveur | Avant début, au début, juste avant fin, à fin ; suspension/annulation ; horloge relue après attente de verrou ; formulaire ancien refusé | États Live et conflits API | Éditions future, ouverte, suspendue, terminée | UTC serveur/fuseau d'affichage ; pas d'extension implicite |
| E78-CA-07 | Moteur E78 : QCM, confirmation et correction | Annuler/modifier la sélection n'envoie rien ; bonne/mauvaise réponse enregistrée ; choix absent/étranger refusé sans consommation ; aucune correction client | SUBMIT_ANSWER/SINGLE_CHOICE, résultats dédiés ; consigne et confirmation | Succès et échec définitifs | Transaction réponse/progression/reçu, pas de deuxième essai |
| E78-CA-08 | Réponse et protocole commun : unicité/reprise | Même clé/même intention, même clé/autre choix, deux clés simultanées, reçu perdu après commit, reçu expiré ; une seule réponse et chance | Reçus, conflits, brouillons par participant/édition/vitrine | Réseau coupé avant/après commit, deux appareils | Contraintes PostgreSQL ; aucune clé nouvelle automatique |
| E78-CA-09 | Participation/Live : reprise et retour immédiat | Rechargement, récupération autre appareil, changement d'identité, réponse tardive d'une ancienne requête ; succès/échec sans révélation générale avant clôture | Carnet, bibliothèque locale et caches, projection personnelle | Plusieurs vitrines dont commandes incertaines | Pas de fuite privée dans service worker, logs ou cache partagé |
| E78-CA-10 | QualificationVitrines et attestations : mêmes conditions E77 | Deux modes ; réponse/passage dans les deux ordres et concurrents ; mauvais choix malgré visite ; preuve hors période/autre commerce/autre édition, PIN/salarié révoqué ; K-1/K/K+1 et chance unique | Seuil, merchantProofRequired, scan/PIN E70, droits E72 et progression X/K | Réponse seule, passage seul, les deux, seuil impossible pour un joueur | Coordination réponse/QR/PIN ; mode sans passage refuse la commande inutile |
| E78-CA-11 | Clôture/tirage et domaine lots existant | Commande initiale autorisée/refusée selon droit, checkpoint puis clôture interrompue/reprise, deux workers, réponse/passage en frontière, conservation concurrente, audience partielle refusée, annulation non tirable ; tirage/remise rejoués | Guide tirage, Mes lots, garde d'audience complète ; corrigé après clôture | Qualifiés/non-qualifiés, coffret/lot externe/bon numérique selon dotation existante | Lots bornés, checkpoint et bascule atomique ; pas de gain à la réponse |
| E78-CA-12 | Lectures de préparation/bilan : scope, agrégats et bornes | Pages 25/100, limite d'octets réduisant la page sans omission, filtre rare/vide, curseur falsifié/étranger/expiré, compteur daté ; pas de N+1 ni de réponses nominatives dans une synthèse | OpenAPI suivi, pages ERP-UX, modes vide/erreur/chargement | Deux communes, textes aux bornes et historique important | Index/plans, charge mixte et mémoire mesurés |
| E78-CA-13 | Exploitation : suspendre, reprendre identique ou annuler | Reprise après nouveau constat lié à l'incident/cycle courants ; plusieurs constats successifs restent valides ; ancien contrôle, incident modifié ou vitrine non recontrôlée refusés ; reprise après fin et clôture pendant suspension refusées ; mutation publiée/retrait/neutralisation refusés ; nouvelle édition sans transfert | Procédure terrain/support et règlement | Intrus absent, commerce fermé, solution erronée ; deux incidents bloquants ; suspension atteignant la fin | Motif/audit, acquisitions conservées, pas de baisse rétroactive du seuil ni réouverture implicite |
| E78-CA-14 | Domaine/droits/projections : confidentialité et compatibilité | Altérer IDs/versions/rôles ; accès sans ANIMATION ; sortie JSON/HTML, erreur, reçu, kit, QR, DAM, export et cache sans marqueur correct avant révélation ; anciens clients refusés | E41/E42 et contrats embarqués, permissions serveur, choix public distinct du corrigé privé | Principal/salarié/ERP lecture/gestionnaire/habitant, média privé | CSRF/Bearer, rate limit, conservation/anonymisation/gels et export autorisé |
| E78-CA-15 | Présentation Animation/Pro/Live : parcours accessible | 320/390 px, PC 1280, texte 200 %, clavier/lecteur d'écran, radios, focus confirmation/retour, cibles 44 px, mouvement réduit, texte sans couleur seule | Checklist ERP-UX-01..12 et principes Live ; kit accessible | Vitrine sans photo, libellé long, erreur réseau, résultat à vérifier | Captures/rapport navigateur, aucun appel ou notification réel |
| E78-CA-16 | Tous propriétaires : couverture et capacité sans régression | Domaine/application/API/PostgreSQL/consommateurs/navigateur, N/10N et charge mixte ; comparer les moteurs existants ; succès/échec/non exécuté distincts | Matrice renseignée avec commandes, commits et rapports réels | Génération/restauration et remappage des versions | Capacités avant activation ; ni tests d'import ni liens comme preuve métier |

## Preuves à produire

Les noms de nouveaux fichiers ci-dessous sont des **cibles**, non des tests présents :
`tests/domain/animation_locale/test_jeu_vitrines.py`,
`tests/api/test_jeu_vitrines_contract.py`,
`tests/security/test_jeu_vitrines_postgres.py` et
`tests/performance/test_jeu_vitrines_postgres_capacity.py` dans le backend.
Suivre les lanceurs isolés de son AGENTS au moment de l'implémentation ; base
PostgreSQL jetable, horloge pilotée et fournisseurs factices, aucun envoi externe.
Le test domaine prouve la règle, le test SQL ses contraintes/concurrences et
le test API les refus réels, la sérialisation et les droits.

Compléter les suites communes plutôt que créer une copie d'E77 : attestations,
PIN, sessions salariées, participation E56, publication, dotations, tirage,
conservation, exports de contrat. Tester particulièrement la simultanéité
réponse/scan/PIN/suspension/clôture et la révocation entre lecture et confirmation.
Une mauvaise réponse définitive reste consommée même après expiration du reçu.
Le gel d'audience est repris sans oublier un passage confirmé avant sa fermeture.

Animation couvre assistant/règles, approbation et contrôle, publication,
exploitation, bilan et nouvelle édition. Pro couvre invitation acceptée,
préparation/installation/kit et scan ; le salarié ne voit aucune action de contenu.
Live couvre découverte/lien ciblé, liste, confirmation, PIN si requis, reçus,
reprise, qualification, clôture et accès aux lots. Étendre les tests de registres,
manifestes/empreintes et négociation de **chaque** frontend : aucun fallback.
Conserver les non-régressions Juste Prix, Passeport, Chasse et Tombolas.

## Performance et volumétrie

Appliquer la [convention transverse](../../architecture/transverse/performance-volumetrie.md)
et [E59](../epic-59-tests-performance-api/README.md). Les valeurs suivantes sont
des **budgets de conception à mesurer**, pas des résultats ni une capacité acquise.

N = 1 000 participants dans une édition de 20 vitrines ; 10N = 10 000 participants
dans la même édition. Ajouter séparément le maximum de 100 vitrines (jusqu'à un
million de couples participant/vitrine), 100 communes étrangères et l'historique.
Faire varier chaque population indépendamment pour détecter les scans globaux.

| Parcours / propriétaire | Projection, filtre, borne et accès attendu | Coût / transaction / budget initial |
| --- | --- | --- |
| Vitrines et sélecteurs — API/ERP/Live | Périmètre avant LIMIT ; ordre stable `(merchant_id)` ; page 25/max 100, lecture limit+1 ; index animation/merchant, enrichissement commerces/médias groupé | <=8 requêtes SQL, aucune donnée binaire dans liste ; p95<=500 ms/p99<=1 s, projection<=256 000 octets, delta mémoire requête<=16 Mio |
| Proposition et préparation — Pro/Animation | Propre commerce ou animation/état ; unicité `(animation_id,merchant_id)`, index `(animation_id,state,merchant_id)` ; détail ciblé, historique sous-liste | Lecture<=8 requêtes, écriture<=20 ; révision optimiste puis coordination publication ; p95<=800 ms/p99<=1,5 s |
| Réponse et passage — domaine/UoW | Une cible, corps<=16 Kio ; unicités réponse/commande/preuve ; lecture ciblée par participant/défi et configuration | <=20 requêtes SQL, aucune croissance selon nombre de participants ; attente verrou<=2 s puis refus explicite ; p95<=800 ms/p99<=1,5 s à 20 écritures/s |
| Carnet et reçus — API/Live | Participant autorisé, compteurs synchrones et sous-liste 25/max 100 ; index participant/step et clé de reçu avec son scope | <=8 requêtes, p95<=500 ms/p99<=1 s ; pas de chargement de toute une édition pour lire un participant |
| Bilan participants — Animation/ERP | Animation et filtres avant limite ; ordre `(inscrit_at,id)`, index aligné, référence exacte ; comptes projetés/datés, aucun COUNT exhaustif par page | <=8 requêtes, p95<=800 ms/p99<=1,5 s ; pas de jointure multipliant les racines avant pagination |
| Publication — domaine/application | Au plus 100 vitrines et leurs contrôles exacts ; copie bornée de la configuration, pas des participants | Une transaction cohérente ; pas de DAM/réseau sous verrou ; p95<=1 s/p99<=2 s au maximum 100 |
| Clôture/audience — worker | Parcours cohérent des participants figés ; index animation/participant ; jobs prêts indexés globalement ; lot<=100 | Un worker par édition ; plafond 25 éditions/250 lots/30 s par passage ; delta RSS<=128 Mio, objectif clôture<=120 s à 10N/20 vitrines, maximum 100 mesuré séparément |
| Exports/conservation/reconstruction — jobs existants | Ajouter les tables E78, FK indexées, lots<=100 et checkpoint ; source versionnée, droits et gels avant sélection | Travail O(population concernée), jamais synchrone exhaustif ; mémoire<=128 Mio supplémentaire, progression/reprise et annulation adaptées |

Les curseurs sont opaques et liés au contexte autorisé, filtres, tri et version,
sans offset profond ; durée technique 30 minutes, erreur 422 si invalide/expiré.
Une liste vivante ne promet pas un instantané entre deux pages ; l'audience de
tirage, elle, en exige un. L'UI conserve au plus trois pages visibles/demandées,
ne précharge pas tout le catalogue, annule les requêtes obsolètes et ne conserve
pas une réponse d'une ancienne commune/participation. Recherche par nom normalisé
via le sélecteur existant ; tout nouveau prédicat doit justifier son index réel.

Campagne prévue sur cible isolée : 80 lectures/s, 20 écritures/s, 100 sessions,
15 minutes après préchauffage, une clôture sur une autre édition ; pointe à 2×
pendant 60 s. Rejouer N/10N à froid et à chaud, pages 25/100, début/fin de parcours,
filtre courant/rare/vide. À 10N, p95<=1,5×N tout en restant dans les budgets.
Hors refus métier et limitations attendues, erreurs techniques<1 %.
Mesurer p50/p95/p99, débit soutenu, RSS, CPU/I/O, objets hydratés, SQL/plans
`EXPLAIN (ANALYZE, BUFFERS)`, lignes/blocs lus, pool/verrous et âge des jobs.

La saturation produit 429 avec `Retry-After` ou 503, pas de file/threads/retries
sans borne. Conserver les limiteurs communs et les mesurer avant ajustement ;
pas de retry automatique avec une clé différente. Vérifier tenant très actif,
plusieurs tenants et participant ciblé par deux appareils. Un dépassement demande
une correction ou une limite documentée avant activation, sans affaiblir les tests.

## Documentation, démonstration et données

Lors de l'implémentation, actualiser le guide
[d'exploitation Animation](../moteur-animation/exploitation-moteur.md),
l'[espace commerçant](../espace-commercant/README.md),
[Live](../epic-42-localeo-live/README.md), le règlement et les kits, ainsi que les
[procédures E73](../../exploitation/technique/configurer-epic-73.md).
Documenter les libellés réellement livrés, la différence contenu/installation/
contrôle, la réponse définitive, les deux modes de passage, la révélation et
l'incident. Cette phase n'annonce aucun écran E78 déjà disponible.

Le générateur reste dans `localeo-backend/scripts/demonstration/`, avec entrée
`generator.py` et module E78 dédié à créer sur le patron `juste_prix.py`.
Passer par les services d'application pour préparer/approuver/contrôler et produire
des versions cohérentes ; ne pas fabriquer par SQL des états interdits en domaine.
Prévoir Noël/Pâques/autre thème, 5 commerces/seuil 3, les deux modes de passage,
préparation incomplète, contrôle obsolète, réponses juste/fausse, passage seul,
seuil atteint/impossible, suspension/reprise, annulation et clôture.
Inclure principal, salarié autorisé/révoqué, ERP lecture/mutation et deux communes.
Les solutions synthétiques restent privées ; aucun export, secret ou fichier de
démonstration n'est versionné dans le dépôt documentaire.

Génération, sauvegarde/restauration et remappage doivent préserver révisions,
preuves, FK, résultats et audience. Anonymisation/gels/conservation doivent
inclure les nouvelles tables et photos privées, avec refus en cas de clôture
concurrente. Aucun nouveau délai de rétention n'est instauré.
Sans impact sur la règle financière des lots et leur remise : réutilisation des
dotations existantes, avec preuve de bout en bout du raccordement E78.
Sans impact IA/fournisseur de génération : aucun contenu généré automatiquement
n'est demandé pour ce jeu.

## Lots et ordre de livraison

| Lot | Critères et responsabilité | Dépendances / sortie attendue |
| --- | --- | --- |
| 1 | Domaine/configuration, proposition, contrôle matériel, persistance/publication et offre — CA-01..04/13/14 | Décisions acquises ; migration additive à numéro libre, modèle encore inactif ; tests domaine/versions/publication et contrats privés |
| 2 | Réponses, attestations scan/PIN, qualification, reçus, exploitation/clôture/tirage — CA-06..11/13/14 | Lot 1 ; preuves PostgreSQL de concurrence et d'audience complète, deux modes de passage |
| 3 | Assistant Animation/ERP, Pro et Live, kits — CA-03..10/12..15 | Contrats lots 1/2 stabilisés ; manifestes et négociation, parcours mobile/accessibilité, états/récupération et rôles |
| 4 | Démonstration, documentation, capacité et intégration — CA-16 et ensemble de la matrice | Lots 1..3 ; résultats réels attachés aux commits, limites explicites, procédures de reprise et configuration vérifiées |

Livrer migration additive puis backend avec E78 inactif ; générer contrats
canoniques E41/E42 et exports consommateurs ; livrer Animation, Pro et Live
compatibles ; contrôler les empreintes et le bundle documentaire si nécessaire ;
activer le modèle standard après les preuves requises. Il n'y a pas de migration
des éditions des autres jeux, ni de tarif/quota E78 à configurer.
L'autorisation de spécifier ne déclenche ni activation, ni commit, ni push, ni
déploiement. Un pilote externe n'est pas ajouté comme condition implicite de clôture.

En incident de livraison, empêcher les nouvelles créations et suspendre l'édition
touchée si nécessaire. Conserver versions, réponses, preuves et reçus ; utiliser
des corrélations sans solution/jeton dans les diagnostics. Un ancien backend ne
doit pas lire E78 comme un autre jeu ; ne pas supprimer les tables pour revenir
à une version antérieure. Après publication, appliquer la procédure d'incident
du jeu, sans conversion, transfert automatique ou correction rétroactive.

## Contrôles de cette phase de spécification

- Producteurs et consommateurs : lecture effectuée dans les cinq dépôts, bases
  et chemins dans l'architecture ; aucun service déployé observé.
- Tests métier, API, PostgreSQL, navigateur, capacité et démonstration :
  **non exécutés**, aucune implémentation E78 produite pendant cette phase.
- Revue indépendante `localeo-contract-reviewer` : effectuée en lecture des
  documents réels et des points de code ciblés. Deux écarts de conception corrigés
  et relus : nouveau constat lié à l'incident pour reprendre, commande initiale
  de clôture explicite. Précisions finales intégrées : limite temporelle de reprise
  et référence stable du cycle de suspension, distincte de la révision optimiste.
  Aucun autre écart bloquant signalé ; cette revue ne constitue pas un test métier.
- `scripts/check_guidance.py`, avec les sept fichiers modifiés ajoutés par
  `--document` : **104 guides, 1 472 liens locaux, zéro erreur/avertissement**.
- `scripts/sync_documentation.py --check-sources` : **150 documents vérifiés**.
  Ces deux commandes ont été exécutées avec
  `C:/Users/casta/AppData/Local/Python/bin/python3.exe` ; elles ne valident pas
  le comportement des futurs lecteurs E78.
- Encodage UTF-8 et présence de **16 critères uniques identiques** dans le backlog
  et la matrice : contrôlés. `git diff --check` : réussi.
- Seul `localeo-projet` est modifié ; les quatre dépôts applicatifs sont propres.
  Aucun contrat machine, migration ou générateur n'a été modifié dans cette phase.

Reprise au 15 novembre : lot courant = spécification ; prochain geste = implémentation du lot 1
sur demande. Aucun serveur, build ou base temporaire n'est démarré pour cette
phase. Les tests et mesures applicatifs ci-dessus restent à produire.
