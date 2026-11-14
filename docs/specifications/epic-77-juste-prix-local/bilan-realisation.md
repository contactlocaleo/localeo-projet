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

## Correctif Pro — accompagnement de la saisie et retour d’enregistrement (14 novembre 2026)

Le signalement concerne le champ « Unité ou format » sans explication et le
bouton grisé après enregistrement, sans confirmation visible à proximité.
Dans le composant local, un succès remplaçait la saisie par la réponse serveur
et désactivait normalement le bouton faute de modification restante ; son
message apparaissait au-dessus du formulaire, potentiellement hors écran.
Cette observation explique l’ambiguïté de l’interface, sans prouver le résultat
de la requête effectuée sur TEST par le commerçant.

Le champ explique désormais la quantité ou le conditionnement correspondant
au prix à deviner, avec les exemples « sachet de 500 g », « bouteille de 75 cl »,
« lot de 3 » et « à la pièce ». Près des boutons, Pro distingue l’enregistrement
en cours, le succès confirmé par le serveur, les modifications non enregistrées
et le résultat incertain. Les confirmations et erreurs utilisent le composant
commun de retour avec focus et mise en visibilité. Modifier un champ efface
l’ancienne confirmation et réactive l’enregistrement ; proposer à l’organisateur
reste une action distincte. Aucun succès n’est annoncé sur un refus ou une
erreur réseau, et une mutation incertaine exige toujours une relecture serveur.

Périmètre : `localeo-commercant` et ce bilan canonique. Contrat API, règles de
validation du domaine, migration, données et générateur de démonstration : sans
impact, car seuls l’accompagnement et les retours du formulaire changent.
Les preuves locales et le statut de livraison du correctif sont consignés
ci-dessous ; ils ne constituent pas une vérification du déploiement TEST.

Preuves sur la base Pro `0acaa1010190` avec ce correctif local :

- Vitest ciblé sur `JustePrixProduct` et `ParticipationRequestDetailPage` :
  12 tests réussis, dont attente de réponse, confirmation, nouvelle modification,
  refus serveur, résultat incertain et verrouillage après publication.
- Playwright `tests/e2e/juste-prix-product.spec.js --workers=1` : 3 parcours
  réussis à 320, 390 et 1280 pixels, API simulée, réponse de sauvegarde retardée,
  relecture après rechargement et absence de double mutation. Captures mobile
  et bureau inspectées ; build navigateur isolé réussi.
- Reproduction avant correction : le test d’aide accessible échouait faute
  d’explication associée au champ. La première exécution navigateur utilisait
  un champ de fixture incorrect (`modelCode` au lieu de `modele_code`) ; après
  correction de la fixture, les trois parcours passent sans modification du
  contrat applicatif.

Aucune réparation de données ni modification du backend n’est nécessaire.
Correctif vérifié localement ; aucun déploiement manuel réalisé dans le cadre
de cette intervention.

Le même retour est explicité pour « Proposer à l’organisateur » : pendant la
requête, le bouton affiche « Proposition en cours… » et bloque un second envoi.
Après confirmation serveur, une confirmation verte reçoit le focus près des
actions et le bouton indique « Proposition envoyée ». Après rechargement, Pro
rappelle que la proposition attend la validation de l’organisateur. Une erreur
ne confirme aucun envoi ; un résultat incertain impose toujours une relecture.
La reproduction ciblée échouait avant correction sur l’absence du libellé
d’attente. Vérification du correctif complété : **15 tests Vitest ciblés** et
**3 parcours Playwright** réussis à 320, 390 et 1280 pixels, avec proposition
retardée, confirmation visible et relecture après rechargement. Contrats,
données, migrations et statut de livraison restent inchangés.

## Correctifs Animation — décisions sur les produits et navigation de préparation (14 novembre 2026)

Sur la base Animation `87f4bc8c91de`, la proposition nécessitait « Examiner la
proposition » puis une décision dans un bloc situé sous la liste. Les actions
« Accepter la proposition » et « Demander une correction » sont désormais
accessibles près du contenu, du prix et de la révision. La demande ouvre le
dialogue de gestion commun, avec choix du motif et précisions ; « Autre motif »
exige un texte. Le payload conserve `expectedRevision` et le motif lisible du
contrat existant. Fermeture et annulation restent sans écriture, l’envoi bloque
les doubles clics, une erreur ne confirme aucune décision et impose une
relecture avant reprise. Les contrôles d’autorisation et de révision restent
au backend. Les produits sont présentés en lignes adaptées au mobile, avec
les actions à côté sur bureau et sous le contenu sur mobile.

Dans « Préparer », la navigation des rubriques reste visible pendant le
défilement. La configuration ajoute des accès directs aux informations,
règles, mission, commerces, lots, produits et prix, contact public, selon les
parties applicables au modèle. Sur mobile, écran peu haut ou largeur insuffisante
(notamment avec le texte agrandi), les accès utilisent un sélecteur compact sans
défilement horizontal du menu. L’en-tête de titre défile pour laisser la place au contenu.
La hauteur réelle de la barre est prise en compte pour que la partie ciblée
reste visible ; le focus suit le choix. Les formulaires restent montés et les
saisies non enregistrées sont conservées. La navigation entre rubriques garde
les protections de sortie existantes. La Chasse conserve son parcours guidé.

Preuves sur les changements locaux, sans API réelle ni fichier d’environnement
opérateur :

- `node tests/browser/juste-prix-products.mjs` : 6 scénarios réussis, décisions
  et dialogue à 320/390/1280 px, texte 200 %, motif obligatoire, annulation et
  retour du focus, CSRF, révision, conflit, réponse perdue et consultation sans
  droit de décision. Le mode `--baseline` échoue avant correction sur l’absence
  des actions directes. Captures mobile et dialogue inspectées.
- `node tests/browser/preparation-section-navigation.mjs` : 7 scénarios
  réussis sur l’application complète, Juste Prix à 320/390/1280 px, texte 200 %,
  écran de 520 px de hauteur, Passeport et Tombola publique. Cibles visibles
  sous la barre, focus, présence continue de la navigation, saisie préservée et
  absence d’écriture vérifiées, ainsi que l’absence de défilement horizontal
  dans le menu. L’ancien build échoue sur l’absence de cette
  navigation. Captures mobile et bureau inspectées.
- `pnpm typecheck`, `pnpm lint` et les 2 tests de `tests/juste-prix.test.mjs` :
  réussis. Build complet isolé via `scripts/build-generation-tests.mjs`, sortie
  `tmp/preparation-navigation-dist` : réussi, avec avertissement de taille de
  bundle. Rapports et captures restent dans les répertoires `tmp/` ignorés.

Dépôts affectés : Animation et documentation canonique. Backend, contrats API,
données, migrations et démonstration : sans impact, car les commandes et règles
restent identiques ; les motifs proposés sont une aide de saisie du texte
existant. Aucun déploiement manuel ni réparation de données réalisés ici. Les correctifs
Pro précédents restent dans leur dépôt, avec leurs preuves propres.

La revue UX indépendante a identifié un menu initialement défilant au texte
agrandi ; le correctif utilise désormais la largeur réelle disponible pour
choisir le sélecteur et autorise le retour à la ligne des liens. La relecture
du correctif n’a identifié aucun autre blocage concret.

Les correctifs sont versionnés séparément : Pro `bc7f305` (saisie et retours
d’enregistrement/proposition), Animation `074e3c084297a6915c67aac38b38888c025ae9f0`
(décisions produits et navigation de préparation). Leur publication Git ne
confirme pas l’état des déploiements automatiques ni la recette sur TEST.
