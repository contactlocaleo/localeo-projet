# E77 — Vérification et livraison

V1 du 13 novembre 2026. Les vingt critères restent dans le
[backlog](../../roadmap/en-cours/epic-77-juste-prix-local-backlog.md).
La [conception](architecture-contrats.md) et les [parcours](parcours-regles.md)
définissent le comportement à prouver. Cette matrice conserve les preuves prévues lors de la spécification. Les résultats réellement exécutés et les réserves de l’implémentation sont dans le [bilan de réalisation](bilan-realisation.md).

## Traçabilité et preuves à produire

Les noms de suites E77 sont des destinations prévues ; ils ne désignent pas des
fichiers déjà présents. Domaine sous `tests/domain/animation_locale/`, application
et API dans leurs répertoires de tests backend ; concurrence dans une suite
PostgreSQL jetable, et parcours dans chaque frontend concerné.

| Critère | Comportement / propriétaire | Preuve prévue | Documentation / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| CA-01 | Offre E73 et domaine : modèle standard autorisé | Catalogue, création autorisée/refus sans droits, quota standard distinct des modules | README, catalogue et guide organisateur ; OpenAPI E41 | Souscription standard et compte non autorisé | Type inactif jusqu'aux consommateurs prêts |
| CA-02 | Configuration E77 : seuil 1..N, tolérance commune et mode explicites | 0, 1, N, N+1 ; booléen pris pour entier, valeur absente, 100/101 commerces ; publication refusée | Parcours/règles et schéma privé | Seuils atteignables/inatteignables | CHECK/validation, aucune valeur implicite |
| CA-03 | Application de préparation : récapitulatif fiable | Blocage localisé, prochaine action et récapitulatif sur données enregistrées | Assistant et guide organisateur | Brouillon incomplet/prêt | Recette bureau/mobile |
| CA-04 | Proposition : commerce courant seul | Enregistrer/proposer/corriger ; refus autre commerce et salarié, visuel absent, contenu invalide | API E41/Pro, guide Pro | Deux commerces aux droits séparés | Audit et droits révoqués immédiatement |
| CA-05 | Proposition/configuration : approbation de la révision publiée | Modification après approbation, approbation concurrente, publication concurrente ; aucun prix courant repris | Schémas privés et parcours d'approbation | Proposition à corriger et version approuvée | Migration additive, snapshot immuable |
| CA-06 | Politique temporelle de domaine | Juste avant début, début inclus, fin exclue, suspendue/annulée/clôturée ; horloge après attente verrou | Règlement et erreurs 409 | Dates contrôlées par horloge de test | Batch tardif ne prolonge pas le jeu |
| CA-07 | Accès Live et routage | QR animation/commerce, inscription/récupération, visite non créée par QR, lien direct et retour | Liens, supports, guide Live ; contrat public | Carnet existant, nouveau participant, stockage indisponible | Origines Live selon environnement |
| CA-08 | Exécution : réponse confirmée une fois | Édition libre, annulation sans requête, confirmation, mauvais montant/precision, clavier mobile | Contrat MONEY_ESTIMATE et confirmation | Réponse absente puis correcte/incorrecte | Pas de mutation hors ligne simulée |
| CA-09 | MontantJeu et politique E77 | Centimes exacts, bornes ±T, dépassement d'un centime, T=0, P=0, T>P, maximum ; flottants/booléens refusés | Règlement, DTO strict | Prix exact et tolérance non nulle | Aucun montant privé dans erreurs/logs |
| CA-10 | Exécution/idempotence : reçu et unicité | Double clic, deux clés/deux montants concurrents, première exécution absente, clé même/différent corps, rollback, réponse perdue, reçu après fin | Reçus 200/202/404, conflits 409 | Reçu confirmé/commande incertaine | Unicité DB, audit sans nouvelle chance |
| CA-11 | Qualification : bonne réponse ET preuve si requis | Deux ordres, deux commandes simultanées, QR public, commerce étranger, mauvais prix malgré visite, PIN révoqué/salarié refusé | API E70/Pro et état personnel séparé | Passage seul, prix seul, les deux | Outbox système existante, pas d'envoi réel en tests |
| CA-12 | Qualification : réponse seule sans passage requis | Bonne réponse qualifiante, aucune dépendance aux visites ; commande passage E77 inutile refusée | Mode explicite en Live et règlement | Sans passages avec zéro validation | Ne pas modifier les autres moteurs |
| CA-13 | Qualification : seuil et chance unique | Sous seuil, au seuil, au-delà ; commerce jamais compté deux fois, résultat confirmé relu | Compteurs personnels et suivi | 5 commerces/seuil3, 2/3/4 réussites | Compteur cohérent, projection datée distincte |
| CA-14 | Accès personnel/exécution persistée | Rechargement, récupération autre appareil, deux participations distinctes, révocation et réponses tardives | Carnet et récupération E42 | Carnet rempli, lien personnel | Aucun cache API/service worker privé |
| CA-15 | Clôture/tirage : audience cohérente | Commande à la frontière, clôture interrompue/reprise, audience intermédiaire invisible, tirage rejoué ; révélation après clôture seulement | Contrat résultat/prix et guide tirage | Qualifiés et non-qualifiés figés | Job durable/reprise et vérification de version |
| CA-16 | Domaine lots existant | Coffret, lot externe et bon numérique, retrait autorisé/refus/double consommation ; aucune confusion prix/valeur | Guides lots et Mes lots E73 | Trois variantes de dotation | Aucun changement de règles financières |
| CA-17 | Animation : incident sans réévaluation | Édition publiée refusée API/ERP, suspension, reprise identique, annulation, nouvelle édition sans transfert ; aucune neutralisation | Procédure support et règlement | Incident avant/après réponses | Motif/audit, aucune prolongation implicite |
| CA-18 | Projections de suivi : droits et bornes | Pagination 25/100, filtres avant limite, agrégats datés, comptage exact, absence de N+1 et de prix publics | OpenAPI suivi et guide ERP | Historique et deux communes | Index/plans et diagnostic sans secrets |
| CA-19 | Contrats/accès : pas de fuite ni de fallback | DTO sérialisés sans référence avant clôture, manifestes, client inconnu/ancien, altération participant/commerce/version, caches et médias/supports | E41/E42, contrats embarqués générés | Acteurs autorisés/restreints, ancien client | Livraison coordonnée, activation finale seulement |
| CA-20 | Ensemble du parcours et capacité | Domaine/application/API/PostgreSQL, PC 1280, mobiles 320/390, texte 200 %, clavier/focus/mouvement réduit, N/10N et charge mixte | Présent dossier, checklist ERP-UX et LIVE-UX | Génération/restauration cohérentes | Budgets ci-dessous ; limites séparées des succès |

Les guides fonctionnels canoniques
[Animation](../moteur-animation/exploitation-moteur.md),
[espace commerçant](../espace-commercant/README.md),
[Live](../epic-42-localeo-live/README.md) et les procédures
[E73](../../exploitation/technique/configurer-epic-73.md) seront actualisés avec
les libellés effectivement livrés. Ne pas décrire dès maintenant des écrans
disponibles aux utilisateurs. Le règlement type doit accueillir tolérance,
réponse définitive, passages, révélation et incident avant publication réelle.

## Performance et volumétrie

Appliquer la [convention transverse](../../architecture/transverse/performance-volumetrie.md)
et [E59](../epic-59-tests-performance-api/README.md). Les chiffres suivants sont
des **budgets de conception à mesurer**, jamais des résultats acquis.

Enveloppe initiale : N=1 000 participants actifs/animation, 20 commerces et
20 000 couples potentiels ; 10N=10 000 participants, mêmes commerces et
200 000 couples. Tester séparément le maximum de 100 commerces (jusqu'à un
million de couples) et un historique réparti entre 100 communes. La mémoire et
le nombre de requêtes par page ne doivent pas croître avec l'historique global.

| Parcours / propriétaire | Filtres, projection, borne | Accès / index attendu | Transactions, mémoire, reprise | Budget initial et preuve |
| --- | --- | --- | --- | --- |
| Catalogue/annuaire/produits — lectures API | Droits/animation, ordre `(commerce_id)` stable, 25 par défaut/100 max ; détails ciblés | Index animation/commerce, enrichissement groupé des commerces et médias | Au plus limit+1 racines, pas d'historique en enveloppe | <=6 requêtes, p95 500 ms / p99 1 s, réponse <=256 Kio ; plans et N/10N, pages25/100 |
| Propositions — Pro/Animation/ERP | Commerce courant ou animation autorisée ; état/commerce et curseur contextualisé | Unicité animation/commerce, index animation/état/commerce | Mise à jour optimiste sur révision ; publication vérifie max100 éléments | <=8 requêtes lecture, p95 500 ms ; modification concurrente testée |
| Réponse / attestation — domaine et UoW | Cible unique, corps <=16 Kio ; idempotency key8..128 | Unicité participant/commerce, lecture réponse/preuve ciblée ; compteur incrémental cohérent | Coordination partagée puis participant, pas de réseau sous verrou ; 2 s max d'attente verrou avant refus explicite | <=20 requêtes, p95 800 ms / p99 1,5 s à 20 écritures/s ; coût stable N/10N |
| Carnet personnel et détail — API/Live | Participation autorisée, réponses/produits sous-listes25/100 ; résumé compteur synchrone | Participant/version puis commerce ; pas de scan de tous les participants | Invalidation par participant/versions, annulation des requêtes anciennes | <=8 requêtes, p95 500 ms / p99 1 s ; delta mémoire <=16 Mio par requête |
| Bilan organisateur / recherche — lecture | Animation/état, ordre immuable `(created_at,id)` ou équivalent réel ; total facultatif daté | Index tenant/animation/filtres/tri à valider sur plans | Agrégats préparés, pas de COUNT complet à chaque page ; filtres avant LIMIT | <=8 requêtes, p95 800 ms / p99 1,5 s ; aucun N+1 page25/100 |
| Clôture / audience / reconstruction — worker | Population figée, lots <=500, checkpoint et version | Index animation/participant pour parcours complet ; index des jobs prêts globalement | Un worker par animation ; préparation invisible puis bascule atomique ; mémoire bornée, reprise sans doublon | O(participants+réponses), delta RSS <=128 Mio ; objectif <=120 s à10N/20 commerces, à mesurer séparément au maximum100 |

Les curseurs sont opaques, liés au tenant/acteur/filtres/ordre/version, sans
offset profond ; durée technique 30 minutes, 422 si invalide, nouveau parcours
après expiration. L'UI conserve la pile de curseurs pour revenir ; elle ne
fabrique ni total ni numéro de page. Un tri modifiable indique la navigation
vivante ; l'audience de tirage utilise un instantané, jamais ces curseurs vivants.

Charge mixte prévue pendant 15 minutes après préchauffage : 80 lectures/s,
20 écritures/s, 100 sessions simultanées et une clôture d'une autre animation.
Rejouer à N/10N, puis une pointe à deux fois le débit pendant 60 s. Hors refus
métier et limitations attendues, erreurs techniques <1 %. Mesurer p95/p99,
pool/verrous, CPU, RSS, lignes/blocs lus, débit du worker et dégradation des
autres moteurs. À10N, latence interactive <=1,5 fois celle de N, dans les budgets.

Saturation : queues/pool bornés, 429/Retry-After pour fréquence et 503 pour
transaction indisponible ; pas de boucle de réessai en client. Conserver le
limiteur existant de commandes, ajuster uniquement sur mesure. Tester aussi
un participant fortement ciblé, les conflits entre deux appareils et des
commandes arrivées à la fin. Le plafond100 commerces est une borne de conception,
pas une capacité prouvée ; tout écart de budget bloque l'ouverture du périmètre
concerné ou exige une limite explicitement documentée, sans affaiblir un test.

## Données de démonstration et non-régression

Préparer des jeux synthétiques avec/sans passages, tolérance0/50 centimes,
prix0/1250, seuil3 sur5, réponse fausse définitive, passage seul/réponse seule,
qualification, incident suspendu et clôture avec trois variantes de lots.
Inclure commerçant principal, salarié autorisé/révoqué, organisateurs de deux
communes et profils ERP lecture/mutation. Génération, sauvegarde, restauration,
remappage et anonymisation doivent préserver références, résultats et versions.
Le générateur peut référencer les prix privés dans ses données synthétiques,
jamais dans un livrable public ni une sauvegarde versionnée ici.

Contrôler régression Passeport, Chasse, Tombola locale/publique, E56, E70/E72 et
dotations E73. Réutiliser notamment les suites existantes
[contrats moteur](../../../../localeo-backend/tests/application/test_contrats_moteur_t1.py),
[attestations PostgreSQL](../../../../localeo-backend/tests/security/test_attestations_moteur_postgres_t4.py),
[PIN Animation](../../../../localeo-backend/tests/application/services/test_actions_pin_animation_e70.py)
et les tests de registres et contrats des trois frontends. Leur existence ne
vaut pas exécution ni couverture E77.

## Lots de réalisation et livraison

| Lot | Contenu / critères | Dépendances et sortie attendue |
| --- | --- | --- |
| 1 | Domaine, stockage, produit privé, approbation et publication — CA01..05/09/17/19 | Décisions acquises ; schémas et routes privées finalisés, migration additive, modèle encore inactif ; tests domaine et contrats |
| 2 | Estimations, reçus, passages, qualification et clôture — CA06..15/18/19 | Lot1 ; preuve PostgreSQL de concurrence/période/reprise et audience figée |
| 3 | Assistant, Pro et Live, dotations/supports — CA03..08/11..19 | Contrats des lots1/2 ; registres/manifestes/renderers, parcours PC/mobile et droits ; aucun prix dans QR/supports |
| 4 | Démonstration, capacité, documentation et livraison — CA20 et preuves transverses | Lots1..3 ; matrice renseignée avec résultats réels et limites, activation autorisée seulement après qualification |

Les quatre lots ont donné lieu à l’implémentation locale demandée ensuite ; le lot de qualification complète conserve les réserves du bilan.

Ordre de livraison : migration additive et backend E77 inactif ; schémas/OpenAPI
canoniques et exports générés ; Animation, Pro et Live prêts ; bundle documentaire
si nécessaire ; vérifications ciblées ; activation explicite du modèle standard.
Ne pas modifier les droits ou quotas des autres jeux. Vérifier après livraison
catalogue, approbation, réponse, passage, reçu et qualification sur une animation
autorisée, sans notification externe ou tirage réel implicite.

Incident de livraison : masquer les nouvelles créations E77, suspendre le jeu
touché si nécessaire, conserver faits/reçus et versions, diagnostiquer avec
identifiants de corrélation sans prix ni tokens dans les journaux. Ne pas
supprimer les nouvelles tables pour revenir à un code ancien. Après publication,
appliquer la procédure d'incident des parcours et les droits d'exploitation
existants. La reprise et la clôture doivent être testées avant ouverture.

## Historique des contrôles de spécification

- Lecture des producteurs et consommateurs : effectuée, périmètre et chemins
  dans l'architecture ; aucune vérification d'environnement déployé.
- Tests métier, PostgreSQL, navigateur, capacité et génération/restauration :
  **non exécutés**, puisqu'aucune implémentation E77 n'est produite.
- Revue indépendante du profil contrats : effectuée **sur résumé uniquement**,
  accès fichiers indisponible dans sa session. Constats intégrés : rattachement
  temporel des preuves, portée de révélation, empreinte canonique/idempotence,
  checkpoint d'audience et absence d'estimations nominatives dans les bilans.
  Cette revue ne constitue pas une inspection indépendante du code.
- `py -3.14 scripts/check_guidance.py` avec les neuf documents modifiés ajoutés
  par `--document` : **105 guides, 1 561 liens locaux, zéro erreur/avertissement**.
- `py -3.14 scripts/sync_documentation.py --check-sources` : **150 documents
  vérifiés**. Aucune source OpenAPI générée ni liste d'exports n'est modifiée.
- `git diff --check` : réussi. Le raccourci `python` du système était indisponible ;
  les contrôles Python ont été exécutés avec le lanceur `py -3.14`.

La conception couvre les vingt critères et les quatre arbitrages résolus ;
elle est prête à implémenter dans l'ordre indiqué. La capacité mesurée et la
preuve de comportement restent des conditions de livraison, pas des résultats
de cette spécification. Aucun commit, push, déploiement ou activation effectué.
