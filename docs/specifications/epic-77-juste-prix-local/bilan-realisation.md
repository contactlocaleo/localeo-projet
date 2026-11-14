# E77 — Bilan de réalisation locale

13 novembre 2026. **En cours**, modèle inactif. Ce bilan décrit le code local
non commité des cinq dépôts, les contrôles réellement exécutés et les réserves.
Il ne prononce ni clôture, ni déploiement, ni activation commerciale.

## Comportement réalisé

Le commerçant principal prépare son produit, son format, sa description, son
prix TTC en centimes et éventuellement une image fournie dans Pro. Enregistrer
et proposer sont deux actions distinctes. L’organisateur approuve la révision
dans Animation ou dans la console ERP « Juste Prix Local » ; modifier un produit
annule son approbation. La publication recontrôle les produits des commerces
retenus sous coordination exclusive et compile leur instantané privé.

Le gestionnaire choisit explicitement seuil, tolérance commune et passages
requis. Live présente ces règles avant inscription. Chaque produit reçoit une
seule estimation confirmée, même incorrecte. Le résultat trouvé/non trouvé est
immédiat ; aucun indice plus/moins n’est fourni. Les passages requis peuvent
précéder ou suivre la réponse, dans la période publiée. Le seuil donne une
chance au tirage existant. Les prix exacts ne sont renvoyés qu’à la participation
autorisée après clôture effectivement confirmée.

Suspension et reprise conservent exactement les règles publiées. L’annulation
conserve les faits, sans transfert automatique des réponses/chances, crédit ou
remboursement. Les produits publiés et la correction des preuves E77 restent
verrouillés : une erreur suit la procédure d’incident, pas une réévaluation.

Le suivi dédié utilise des pages à curseur 25/100 et des compteurs datés,
sans estimations nominatives. La clôture ferme immédiatement les écritures,
prépare le gel par lots de 100 et confirme audience, qualifications et statut
dans la transaction finale. Un checkpoint et une empreinte chaînée
`E77-CHAIN1` sont persistés avec chaque lot. Cette empreinte identifie une
exécution ; elle ne doit pas être comparée entre deux populations recréées.
Le tirage générique refuse une audience E77 en préparation.

## Dépôts, contrats et données

| Dépôt | Réalisation |
| --- | --- |
| Backend | Moteur et stratégie E77, propositions révisionnées, snapshot de publication, commandes/reçus, réponses et compteurs, qualification, clôture durable, API privées/personnelles, console ERP, migration additive v318 et démonstration locale |
| Animation | Création/configuration explicites, approbation des propositions, suivi paginé des participants et exploitation avec confirmations |
| Commerçant | Produit/prix proposés dans la participation acceptée, image fournie, proposition distincte, état à corriger/approuvé et verrou publié |
| Marketplace/Live | Registre et renderer E77, présentation avant inscription, saisie décimale stricte, revue puis confirmation, résultats persistés et prix après clôture |
| Projet | Spécification, bilan, guides, OpenAPI canoniques E41/E42 et roadmap ; backlog déplacé en cours |

Les cinq tables `animation_juste_prix_*` stockent propositions, réponses,
progressions, compteurs et exploitation/checkpoint. Les autres moteurs gardent
leurs règles. Les contrats moteur générés sont recopiés dans les trois
consommateurs avec manifestes/empreintes ; OpenAPI est généré hors ligne depuis
le backend (1 142 chemins complets, 83 dans la vue Live). Aucun bundle généré
n’est versionné dans le backend.

La migration v318 initialise le modèle **inactif**, inclus dans le forfait
standard ; aucun tarif/module supplémentaire n’est créé. Aucun secret,
fichier média de test ou dump n’est ajouté au dépôt documentaire. Les données
de démonstration et le registre de sauvegarde restent dans le backend.

## Preuves locales

Environnement : Windows, Python 3.14, Node 24, Chromium Playwright et PostgreSQL
18 jetable sur boucle locale, port 55477. Les tests backend utilisent le lanceur
`scripts/validation/test_isolated.py`, sans dotenv ni réseau externe. Les tests
PostgreSQL utilisent `--postgres-test-url` vers cette base exclusivement.

| Contrôle | Résultat et portée |
| --- | --- |
| Domaine E77 | **24 succès** : bornes inclusives, centimes stricts, zéro, précision, essai définitif, deux ordres, seuil/chance unique et approbation révisionnée dans `tests/domain/animation_locale/test_juste_prix_dedicated.py` |
| API, contrats, architecture et démonstration ciblés | 777 succès au passage groupé ; domaine rejoué ensuite (24 succès), API rejouée avec le conflit de jeu fermé (9 succès) ; corps 16 Kio, image 5 Mio/type, cible merchant imposée, erreurs sans copie d’input et no-store vérifiés |
| PostgreSQL E77 | 11 succès : migration sur schéma préexistant, conflit concurrent entre réponses, rejeu après fin, confidentialité, révision/approbation, deux ordres réels de preuve/réponse, mauvais prix malgré visite, suspension, rollback/reprise et restauration |
| Clôture/restauration | `pg_dump`/`pg_restore` PostgreSQL18 d’un schéma synthétique contenant une réponse et un checkpoint partiel ; reprise sans doublon et audience finale exacte. Ce test ne valide pas une restauration complète d’environnement |
| Backend élargi | 1 889 succès, 12 échecs, 7 ignorés. Les douze échecs se reproduisent sur le SHA initial `8246ba1b` dans un worktree isolé : libellé catalogue historique, doubles de publication/réversibilité, ancienne modification de dates, doubles de matérialisation et de population de tirage. Aucun skip ajouté ni assertion affaiblie |
| Pro | Suite ciblée produit/registre : 7 succès sur produit/registre, puis les 4 cas produit rejoués après le dernier ajustement ; sauvegarde et proposition séparées, montant exact, résultat incertain et verrou publié. Build test réussi |
| Animation | TypeScript et lint réussis ; **331 tests réussis** au passage final. Attente « quatre moteurs » mise à jour en cinq avec vérification E77. Build test réussi, avertissement de taille de chunk conservé |
| Live | 11 tests ciblés réussis (registre/empreintes, protocole et montants), build réussi. Le lint global rencontre EPERM dans une sortie préexistante `output/bum-politique/pytest-approval-1` ; lint ciblé des sources modifiées réussi |
| Navigateur composants | `scripts/validation/recette_juste_prix.mjs` : Pro, Animation et Live à 1 280/390/320 px, texte 200 %, clavier/focus, mouvement réduit, aucune requête externe ; sauvegarde/proposition, approbation et commande Live exacte. API simulées, pas un parcours déployé de bout en bout |
| Navigateur ERP | `tests/browser/juste-prix-ux.cjs` : approbation et suspension avec motif/CSRF/révision, 1 280/390/320 px et texte 200 % à 320, absence de débordement de page. Tables dans leur région défilante ; sélection par nom/contexte et détails techniques secondaires |
| Revue indépendante | Extrait de clôture, dépendances précisées et incrément de regroupement SQL examinés ; aucun défaut certain établi. Le relecteur n’avait pas d’outils : aucune inspection indépendante complète du diff ni exécution de tests |

Les rapports de travail restent ignorés dans `.artifacts/epic77-*` du backend
et `tmp/epic77-tests-final.log` d’Animation. Les tentatives échouées sont
distinctes des reprises ; elles ne constituent pas des succès cumulables.

## Mesures et limites de capacité

`tests/performance/test_juste_prix_postgres_capacity.py` exerce des UoW locales,
avec états synthétiques de vingt réponses correctes par participant. Il ne
remplit pas une table de 200 000 reçus et ne mesure pas le réseau HTTP.
L’autorisation du participant, les notifications et le rafraîchissement final
des statistiques sont substitués dans cette fixture. Les chiffres ne prouvent
donc pas les budgets complets de l’API authentifiée.

| Population | Produits/participant | Requêtes/page mesurée | Latence locale maximale sur 10 lectures | Clôture | Lots |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 000 | 20 | 7 | 27,2 ms | 3,27 s | 11 |
| 10 000 | 20 | 7 | 41,8 ms | 31,65 s | 101 |

Première mesure : dix requêtes/page et clôture trop coûteuse ; corrigé par
réutilisation de la configuration, absence de lecture des preuves inutiles,
cache des faits communs et écritures groupées. Les assertions de budget restent
inchangées. Les deux mesures corrigées et les huit tests PostgreSQL alors
présents ont passé ensemble : dix succès.

**Restent à qualifier avant activation** : charge HTTP mixte 80 lectures/20
écritures par seconde sur quinze minutes, pointe, pool/verrous et débit des
autres moteurs ; mémoire RSS et plans SQL ; maximum 100 commerces, historique
100 communes ; chaîne authentifiée complète, PIN/révocation salariés, supports
et récupération entre appareils ; trois dotations jusqu’au retrait ; génération,
remappage et anonymisation d’un environnement de démonstration complet. Les
douze dettes de test ne sont pas des preuves vertes des parcours E73.

## Traçabilité de l’acceptation

« Implémenté » désigne le comportement codé ; « partiel » indique une preuve
complémentaire nécessaire, jamais un critère accepté par défaut.

| Critères | Réalisation / preuve | Réserve d’acceptation |
| --- | --- | --- |
| CA01–02 | Offre standard, paramètres explicites, limites de domaine et publication | Création avec souscription et droits réels à recetter |
| CA03–05 | Assistant, produit Pro, approbation Animation/ERP, révisions et snapshot | Assistant complet et publication/approbation concurrentes à recetter |
| CA06–10 | Période sous verrou, commande unique, précision, concurrence et reçus | Entrées QR/inscription/récupération et panne réseau sur parcours complet |
| CA11–13 | Deux ordres dans le domaine et PostgreSQL, réponse fausse définitive, seuil et chance unique | Attestation PIN/salarié et commande simultanée via API complètes |
| CA14–15 | Persistance, accès personnel, clôture transactionnelle par lots et restauration | Récupération autre appareil et course réponse/fin via authentification réelle |
| CA16–17 | Socle des trois lots, suspension/reprise/annulation sans réévaluation | Trois dotations/retraits E77 de bout en bout ; E73 conserve ses dettes de tests |
| CA18–19 | Pagination, compteurs datés, contrats générés, prix personnels après clôture | Plans/charge, supports réels et matrice complète de droits |
| CA20 | Recette des composants/ERP, N/10N et restauration partielle | Capacité complète et démonstration intégrée encore partielles |

## Mise en service et reprise

1. Qualifier les réserves ci-dessus, puis livrer la migration additive v318 et
   le backend avec le modèle inactif. Ne pas supprimer les nouvelles tables en
   retour arrière.
2. Livrer ensemble les trois consommateurs, les OpenAPI/contrats et le bundle
   documentaire vérifié si l’environnement le requiert.
3. Vérifier les droits de lecture/modification/clôture, session/CSRF et accès
   commerçant principal. La console ERP est
   `/internal/erp/animations/juste-prix`, accessible depuis le suivi Animation.
4. Vérifier le batch `animations.juste_prix.cloturer` (une invocation par minute,
   25 animations sélectionnées, 250 lots ou 30 secondes de travail maximum).
   L’interface peut poursuivre un lot explicitement ; une panne conserve le
   checkpoint transactionnel. Diagnostiquer la panne avant reprise répétée.
5. Après qualification et autorisation de mise en service, activer explicitement
   `JUSTE_PRIX_LOCAL` dans le catalogue existant. L’implémentation ne l’active pas.

Pour un incident publié, suspendre, diagnostiquer et reprendre à règles/dates
identiques pendant la période, ou annuler et préparer une nouvelle édition.
Aucune notification externe, activation, migration réelle, commande de tirage
réel, commit, push ou déploiement n’a été exécuté pour cette réalisation.

Contrôles documentaires finaux : 108 guides et 1 618 liens locaux, zéro erreur/avertissement ; 150 sources exportées vérifiées. Contrats moteur : 107 fichiers conformes par consommateur. `git diff --check` réussi dans les cinq dépôts. Base jetable arrêtée, serveurs temporaires fermés.

## Publication et migration TEST — 14 novembre 2026

Demande utilisateur explicite : commit et push des cinq dépôts, puis mise à
jour de la base TEST. Le modèle reste inactif ; son activation et la recette
applicative cible sont distinctes.

La cible TEST a été identifiée séparément de la production. Une sauvegarde
PostgreSQL18 complète de 76 977 406 octets a été créée dans le stockage local
privé ignoré du backend, puis son archive contrôlée avec `pg_restore --list`.
La sauvegarde de cette intervention n’a pas été restaurée sur TEST.

Le runner canonique a vérifié les checksums puis appliqué uniquement
`v318_juste_prix_local.sql`, empreinte
`56b76f479006c0832ce4f213ddd6b68cd75d42f272adadc83d192dbb09dbd305`.
Readiness avant et après : **READY**. Les cinq tables E77 sont présentes,
le modèle `JUSTE_PRIX_LOCAL` existe en version 1 avec `actif=false`, et une
seconde simulation ne prévoit aucune migration. Aucune base de production
n’a été modifiée ; aucun tirage ou envoi externe n’a été déclenché.
Les reçus et la sauvegarde restent sous `.artifacts/epic77-test-delivery/`
dans le backend ; aucune donnée ou configuration privée n’est versionnée ici.

Les profils de préparation workspace et démonstration ont été exécutés pour
cette publication ; leurs rapports restent privés sous `.artifacts/quality/`.
La collecte pytest globale et le lint global Marketplace conservent les
limites documentées ; leur état ne remplace pas les preuves ciblées E77.
Le push de code ne prouve pas la réussite des déploiements automatiques ni la
recette métier du service TEST. Le bundle backend est épinglé sur le commit
documentaire de cette livraison.
