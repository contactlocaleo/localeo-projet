# E75 — Vérification et livraison

[Décisions](README.md) · [Architecture](architecture-contrats.md).
Tous les scénarios métier ci-dessous sont **prévus, non exécutés** pour E75.
Ils définissent la vérification attendue ; aucun pilote externe ne remplace ces tests.

## Traçabilité des 18 critères

Les identifiants du backlog restent inchangés. U = domaine pur, I = application,
HTTP et/ou PostgreSQL isolé, F = parcours navigateur. Les fichiers E75 seront créés
au développement ; les suites existantes à prolonger sont indiquées plus bas.
Chaque critère doit recevoir un résultat réel et un lien vers son test lors de
l’implémentation, sans assimiler une compilation ou un contrôle de liens à une preuve métier.

| Critère | Comportement et propriétaire | Preuves prévues | Documentation / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| E75-CA-01 | Catalogue/droits : offre 190 € HT/12 mois/5, unité propre, activation après paiement | U/I : prix, prorata, paiement en attente/confirmé, callback répété, aucun crédit chasse/standard débité ; F achat | E73 modules, catalogue, assistant E75 | Client sans module, achat en attente puis acquis | Version catalogue, mapping module/unité ; aucun octroi historique automatique |
| E75-CA-02 | Domaine droits : absent, expiré, mauvaise commune, quota épuisé, continuité | U/I : tous les refus, essai/cadeau tracés, publication engagée conservée ; F messages actionnables | Conditions acquises E73, erreurs modules | Dernier crédit, droits expirés, deux communes | Readiness explicite, erreur domaine traduite sans 500 |
| E75-CA-03 | Préparation : demande valide et idempotente | U/I : même clé, clé réutilisée avec autre corps, droits révoqués ; F étape suivante visible | Brief, états, suivi accompagné | Brouillon complet et incomplet | Calendrier versionné et échéance cinq jours ouvrés |
| E75-CA-04 | Tentatives : échec sans perte de proposition | U/I : JSON invalide, bail expiré, interruption avant/après commit, double worker ; F reprise | Import/rapport/reçus | Candidat retenu puis import invalide | Limites, file persistée, coûts inconnus distincts de zéro |
| E75-CA-05 | Grille : validité déterministe avant validation/publication | U : croisements incompatibles, orphelins, mots accidentels, doublons, hors bornes, connectivité, définition manquante ; I contournement import/API refusé | Schéma privé et erreurs localisées | Une grille valide et jeux invalides ciblés | Import borné ; aucun appel fournisseur pour contrôler |
| E75-CA-06 | Préparation : édition/régénération et approbation exacte | U/I : remplacement explicite, refus version périmée, correction conservée, accord invalidé ; F relecture | Empreintes/révisions, accord organisateur et commerce | Deux candidats concurrents, corrections humaines | Audit acteur/révision ; reprise sans écrasement |
| E75-CA-07 | Animation/droits : publication atomique unique | I PostgreSQL : deux publications sur dernier crédit, double clic, échec compilation, crash réponse après commit ; F succès/erreur distincts | Publication/reçu/contrôle terrain | Grille approuvée, dotation et commerces prêts/non prêts | Transaction commune débit/compilation/publication/outbox |
| E75-CA-08 | Projections/supports : même jeu et liens Live | I : URL environnement, QR, PDF, pas de solution ; F QR→Live et fiches par commerce | Flyer, kits, liens directs | Plusieurs indices par commerce, vendeur de lots distinct | Rendu PDF accessible et contrôle de domaine Live |
| E75-CA-09 | Live : saisie mobile et alternative par mot | F : 320 px/desktop/zoom 200 %, clavier, lecteur d’écran, croisement, focus, réduction mouvement | Contrat grille, guide joueur | Grille minimale et maximale | Pas de dépendance IA pendant le jeu |
| E75-CA-10 | Exécution : sauvegarde/reprise sans nouvelle chance | U/I/F : réseau avant/après commit, reçu 202/404/200, deux onglets/appareils, conflit, ancien brouillon/version | SAVE_CROSSWORD, versions, stockage local | Progression partielle, brouillon non confirmé | Limites d’écriture, expiration brouillons, reprise contrôlée |
| E75-CA-11 | Accès/projections : aucune solution ni données tierces | I : accès anonyme/tiers/commerce/salarié non habilité ; inspection cache, export carnet, PDF, logs et erreurs ; F accès expiré | DTO privés/publics et règles de cache | Deux participants/deux communes | No-store, purge/conservation et audit sans contenu secret |
| E75-CA-12 | Domaine qualification : grille juste ET tous les passages | U/I : matrice grille vide/fausse/juste × aucun/partiel/tous passages ; QR/PIN concurrents, normalisation ; F grille validée non modifiable et badge correct | CHECK_CROSSWORD, attestations et qualification | Un commerce portant plusieurs mots, une attestation seulement | Une chance ; pas d’achat imposé ni auto-attestation |
| E75-CA-13 | Exploitation : fermeture et annulation | U/I : limite exacte UTC, écriture hors ligne tardive, clôture concurrente, retrait/reprise, annulation et rejeu reçu ; F retour explicite | États d’exploitation et refus | Animation retirée, fermée et annulée | Retrait ne prolonge pas les dates ; nouvelle édition sans transfert |
| E75-CA-14 | Gel/tirages : population valide et figée | I PostgreSQL : zéro/un/plusieurs qualifiés, insuffisance candidats, doublon tirage, suppléants et provenance ; F bilan | Contrats gel/tirage existants étendus | Ensemble mixte éligible/non éligible | Construction bornée, reprise du gel et publication atomique |
| E75-CA-15 | Dotation : trois modes et remise distincte du passage | U/I/F : coffret, libre externe, bon numérique, notification, retrait et consommation, rejeu QR/PIN | E73 gains/remise et Live Mes lots | Gagnants des trois modes, lots retirés ou non | Outbox idempotente ; aucun envoi réel en test |
| E75-CA-16 | Lectures : bilan cohérent, pagination et coût séparé | I : pagination SQL, N/10N, filtres rares, SQL compté, aucun N+1 ; F pages/états vides | Bilan et contrats de listes | Plusieurs communes, historique volumineux | Compteurs datés, coûts IA internes jamais prix client supposé |
| E75-CA-17 | Préparation/jeu : bornes et indisponibilité IA | I : surcharge 429, plafond génération, fichier énorme/profond, fournisseur indisponible, jeu publié fonctionnel ; charge mixte | Limites, reprises et erreurs | Import invalide, opérateur absent, trafic borné | Alertes file/erreurs/délai, pas de secret dans logs |
| E75-CA-18 | Compatibilité/migration : modèles existants préservés | I/F : anciens clients, contrats/empreintes, migrations depuis base antérieure, restauration, générateur ; régression chasse/passeport/tombolas | E41/E42, moteur, guides existants | E75 synthétique + fixtures historiques sans conversion | Ordre de livraison, activation fermée, rollback compatible |

Pour CA-11/17, tester expressément `REQUEST_HINT`, `REQUEST_HELP` et la lecture
de résultat d’étape existante : aucun contournement des projections E75 privées
ou des indices terrain n’est permis par un ancien chemin chasse.

Compléments de recette de la seconde revue du 4 novembre :

- CA-05/12 : `cœur`, `CŒUR`, `coeur` et les deux casses de `æ` ont la même
  normalisation à l’import, dans la saisie et au contrôle ; leurs longueurs et
  croisements sont calculés après expansion des ligatures.
- CA-10/13 : succès enregistré avant fermeture/retrait/annulation, puis réponse
  perdue et rejeu avec la même clé : même reçu, aucun effet supplémentaire et
  projection courante relue. Une nouvelle clé ou une commande jamais enregistrée
  est refusée après fermeture/retrait ; un accès révoqué ne récupère pas le reçu.
- CA-10/13 : une projection issue d’un reçu ancien ne rétablit pas visuellement
  une participation annulée ou une qualification invalidée par correction de preuve.

## Suites et commandes à préparer

Backend : ajouter les tests de valeurs/politiques E75 dans
`tests/domain/animation_locale/` et d’orchestration dans `tests/application/`.
Prolonger `test_contrats_moteur_t1.py`, `test_projections_jeu_t4.py` et les suites
PostgreSQL `tests/security/test_generation_animation_postgres.py`,
`test_preparation_accompagnee_postgres.py`, `test_publication_moteur_postgres_t3.py`,
`test_jeu_animation_postgres.py`, `test_attestations_moteur_postgres_t4.py`,
`test_exploitation_moteur_postgres.py`, `test_tirages_libres_postgres.py` et
`test_tirages_numeriques_postgres.py`.

Utiliser `python scripts/validation/test_isolated.py` depuis le backend pour les
tests isolés ; compléter par les contrôles d’architecture prescrits dans son
AGENT.md. Les scénarios PostgreSQL et de charge exigent la cible jetable de leur
runner, jamais une base d’exploitation implicite. Ne pas déclarer les tests verts
sur la seule présence des fichiers ou d’un job CI.

Consommateurs : tests de registres/empreintes dans les trois applications ;
Animation `tests/assisted-preparation-http-contracts.test.mjs` et
`publication-http-contracts.test.mjs`, parcours navigateur E75 dérivé du workflow
guidé chasse ; Live `tests/security/live-game.test.cjs`, `library-backup.test.cjs`,
`service-worker.test.cjs` et parcours visuel grille ; Pro contrats animation,
scanner salariés, kit et scan/PIN. Vérifier les scripts de chaque package avant
d’enregistrer les commandes exactes dans le bilan de réalisation.

## Performance : objectifs avant activation

Appliquer la [convention transverse](../../architecture/transverse/performance-volumetrie.md).
Ces budgets initiaux sont des **objectifs à mesurer**, pas une capacité acquise.
Enveloppe de recette : N = 10 000 participations, 10N = 100 000, jusqu’à 10 000
sur une animation ; faire croître séparément autres communes et historique.
Charge mixte cible : 100 joueurs simultanés, 20 commandes/s, 40 lectures/s,
5 attestations/s, deux préparations et un gel en parallèle sur cible isolée.

| Parcours / propriétaire | Accès et bornes | Index et cohérence | Budget / preuve |
| --- | --- | --- | --- |
| Lecture jeu / animation_locale | Une participation autorisée, grille ≤225 cases/25 mots/25 commerces ; ≤10 requêtes SQL, aucune lecture d’autres participants | Clé participation/configuration ; accès token indexé, projection sans historique chargé | p95 ≤400 ms, p99 ≤1 s, réponse ≤64 Ko ; N/10N et caches froids |
| Sauvegarde/contrôle/passage | Patch ≤225 cellules, HTTP ≤16 Ko ; ≤15 requêtes SQL ; une commande en vol par client, autosave au plus une fois/5 s si changements, flush avant contrôle | Exécution unique, reçus cible/clé, preuve effective participant/commerce ; verrou ciblé, délai verrou cible 1 s | p95 ≤500 ms, p99 ≤1,5 s ; aucune double chance, erreur technique <1 % hors refus attendus |
| Liste préparations/participants | 25 par défaut, 100 maximum, SQL limit+1, ordre `(created_at,id)` ; filtre d’accès avant limite ; ≤8 requêtes par page | `(commune_id,statut,created_at,id)` pour préparation ; `(animation_id,created_at,id)` pour participants ; ajuster au SQL réel, expliquer les plans | p95 ≤500 ms, p99 ≤1 s à N/10N, sans offset profond/N+1 |
| Publication | Une animation, ≤25 mots/commerces ; aucun chargement population ; transaction courte | Animation, approbation empreinte, droit/période/unité, unicité consommation | p95 ≤1 s, p99 ≤2 s ; dernier crédit concurrent et rollback prouvés |
| Import/préparation | JSON E75 ≤256 Ko, profondeur ≤16, 25 mots ; deux workers maximum, un candidat actif par animation | Demande/tentative unique, statut/échéance pour claim borné, bail et CAS existants | Contrôle déterministe ≤2 s hors IA externe ; croissance mémoire worker ≤64 Mo par import, mesure fichiers invalides |
| Gel/tirage/export | Travail O(participants) assumé, lots de 500 maximum, curseur durable, population non visible avant finalisation | `(animation_id,participant_id)` et provenance `(population_id,participant_id)` unique ; instantané logique/version gelée | 100 000 lignes ≤120 s, mémoire additionnelle ≤128 Mo ; charge interactive respecte ses budgets et reprise après interruption |
| Bilan | Agrégats/projection par animation et révision ; fraîcheur affichée ≤60 s ; décisions de droits toujours synchrones | Projection par animation/version ; reconstruction par lots, pas de scan des participations à chaque affichage | p95 ≤500 ms ; comparaison compteurs/provenance et reconstruction |

Nouvelles listes par curseur opaque lié à filtres/tri/périmètre/version, expirant
après 24 h ; changer le filtre réinitialise la navigation. Aucun total exhaustif
obligatoire. Préciser tri des nulls et navigation vivante dans les schémas.
Relever matériel, commits, p95/p99, pool, verrous, requêtes/lignes, octets, mémoire,
âge de file et plans PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` sur cible jetable.
Mesurer aussi saturation et retour à la normale ; ne pas ajuster a posteriori un
budget pour cacher une régression.

Limitation joueur : conserver le limiteur partagé de commandes Live et ses
fenêtres configurées, annoncé dans le contrat ; 429 avec reprise explicite,
backoff borné et pas de boucle automatique. Le jeu n’a pas de quota métier
d’essais. Ne pas compter un refus de débit comme une mauvaise réponse.
L’IA externe n’a pas de timeout HTTP applicatif : c’est une attente de traitement
humain suivie par l’échéance d’accompagnement. Reprises worker bornées, sans
génération en boucle ; coûts externes saisis comme constatés ou inconnus, jamais
inventés à partir du nombre de propositions.

## Données, démonstration et documents à livrer

La migration est additive, sans renuméroter les migrations déjà appliquées.
Tester départ depuis la dernière base antérieure, contraintes et index réels,
relance et compatibilité de lecture des modèles existants. Pas de conversion de
chasse ni attribution automatique de droits E75 ; initialiser seulement la
version catalogue désactivée et le registre technique. Contrôler sauvegarde puis
restauration dans deux bases jetables avec notifications neutralisées.

Adapter le générateur backend sous `scripts/demonstration/` en suivant son guide
local : petite grille synthétique reproductible, commerces avec périmètre
Animation prêts, organisateur et salarié de droits différents, jeu ouvert/fermé,
progrès partiels et gains. Les solutions de démonstration restent privées comme
les vraies. Aucun appel IA ni email réel nécessaire aux fixtures. Tests de
génération, idempotence et restauration avant toute génération sur une cible.

Mettre à jour pendant l’implémentation les guides Animation/ERP de préparation,
Pro de validation et Live de participation/gains, les procédures E73 module et
accompagnement, les fiches PDF, les OpenAPI E41/E42 et les contrats embarqués.
Les supports de règlement/inscription reprennent le parcours chasse avec la règle
de grille et de passages E75 ; aucune acceptation historique n’est forgée.
Ce dossier de conception n’a pas de lecteur runtime : aucun nouvel export dans
`documentation.exports.json` à ce stade. Les guides destinés au runtime seront
ajoutés au manifeste lors de leur livraison, avec contrôle des empreintes.

## Ordre de livraison et reprise

1. Produire et tester migration, domaine et contrats backend ; activation E75
   fermée par défaut. Ajouter un contrôle de disponibilité propre au modèle/module,
   et non la seule disponibilité de la chasse.
2. Exporter les contrats hors ligne et adapter Animation, Live et Pro, leurs
   registres, tests, réception des erreurs et caches. Ne pas annoncer une capacité
   avant sa prise en charge complète.
3. Déployer les composants compatibles et la documentation ; vérifier schéma,
   calendrier, droits, catalogue et trois capacités. Lire la disponibilité E75
   côté serveur pour conditionner achat, nouvelle préparation et publication.
4. Exécuter la recette isolée puis la vérification autorisée de l’environnement
   cible : parcours acquisition, préparation/import/approbation, publication,
   inscription, saisie, passages QR/PIN, gel, trois lots. Aucun déploiement ou
   appel mutateur sur TEST n’est autorisé par cette spécification seule.
5. Ouvrir explicitement le modèle/module après réussite des preuves. Sur incident,
   fermer les nouvelles acquisitions/préparations/publications sans casser les
   animations engagées. Garder un backend et des clients sachant lire E75 tant
   qu’une animation E75 existe ; revenir à un ancien binaire incompatible n’est
   pas un rollback sûr. Ne pas supprimer la migration ou les participations.

Diagnostics : identifiants animation/demande/révision/commande, codes de refus,
temps, délai d’accompagnement, candidats invalides et âge de file. Ne pas logger
réponses, solutions, jetons, PIN ou coordonnées personnelles. Alertes Ops sur
échéances et erreurs techniques, sans nouvelles campagnes aux participants.

## Contrôles de cette spécification

- Lecture des producteurs/consommateurs : réalisée, résultats intégrés à l’architecture.
- Revue indépendante `localeo-contract-reviewer` du 4 novembre : réalisée ; chemin Live complet `/public`, noms `actionsAutorisees`/`allowedActions` et générateur OpenAPI Pro précisés ; essais de contournement par anciens chemins d’aide ajoutés. Aucun blocage de conception relevé dans son périmètre.
- Seconde revue ciblée du même jour : priorité du reçu déjà enregistré sur le refus de nouvelle mutation après fermeture/retrait, projection courante après réconciliation et normalisation des ligatures minuscules précisées ; cas de test associés ajoutés sans nouvel arbitrage produit.
- Contrôles documentaires du 4 novembre : `python scripts/check_guidance.py` réussi (96 guides, 1 096 liens, zéro erreur/avertissement) ; `python scripts/check_guidance.py --all-markdown --changed` réussi (7 documents, 141 liens, zéro erreur/avertissement) ; `python scripts/sync_documentation.py --check-sources` réussi (137 documents) ; `git diff --check` réussi.
- Tests unitaires, intégration, fonctionnels et charge E75 : non exécutés ; code à implémenter.
- Migration, activation, envoi réel, commit, push et déploiement : non réalisés dans cette phase.
