# E85 — Implémentation et vérification locale

Le gestionnaire retrouve l’édition à traiter depuis le tableau de bord ou une liste filtrée. La fiche identifie séparément son étape métier et la rubrique ouverte. Une édition Juste Prix ou Vitrines suspendue apparaît parmi les priorités du gestionnaire. La recommandation ouvre le suivi où il peut lire le motif détaillé et les actions permises. La fermeture des participations, l’attribution des lots, leur remise et la fin de l’édition sont des décisions distinctes.

Le périmètre exécutable comprend Passeport commerçant, Tombola locale, Tombola publique, Chasse au trésor commerçante, Juste Prix Local et Jeu des vitrines. Les trois modèles prospectifs restent au stade des maquettes conformément au cadrage. [Variantes par modèle](modeles.md)

## Preuves par critère

Les scénarios navigateur exercent le portail avec des réponses API fictives, notamment les pannes et les droits restreints. Les essais PostgreSQL exercent les règles et les écritures réelles dans une base locale jetable. Les deux types de preuve sont complémentaires.

| Critère | Comportement exercé | Preuve ou limite |
| --- | --- | --- |
| CA-01 | Consulter une priorité puis retrouver commune, étape, rubrique et geste du dossier. | `productivity-workspace.mjs`, `po-organisateur.mjs` et `animation-workspace-ux.mjs`. |
| CA-02 | « Préparer le tirage » ouvre directement la revue. Éligibles et lots sont visibles avant toute attribution. | Parcours intégrés de la fiche à 390 et 1280 px, entrée directe et ancienne recommandation. |
| CA-03 | Annuler, confirmer, relire après perte de réponse et rouvrir l’édition. | `tirage-workflow.mjs` et services PostgreSQL. Deux confirmations concurrentes retrouvent le même tirage et les mêmes gains. |
| CA-04 | Présenter un refus, une lecture seule, une dotation sans lot ou un ancien résultat. | PostgreSQL et navigateur. Le fait de tirage enregistré prime sur une ancienne configuration incomplète. Le domaine refuse une nouvelle attribution sans lot. |
| CA-05 | Ouvrir les inscrits, les qualifiés ou une autre population documentée par le modèle, puis consulter le dossier individuel. | `e85-populations.mjs`, six modèles à 320 et 1280 px. Le détail conserve l’édition et le périmètre du compteur. |
| CA-06 | Chercher, filtrer, paginer, consulter puis revenir au déclencheur. | `productivity-workspace.mjs`, listes globales et populations spécialisées. Le total filtré est lu au serveur. Un total absent reste indéterminé. |
| CA-07 | Conserver la saisie et le dernier résultat confirmé, puis réessayer la seule lecture concernée. | Réessai catalogue et populations. Un seul bouton relit les données communes de configuration. Les produits, le contact et la dotation conservent leur lecture dédiée. `section-refresh-juste-prix.mjs` vérifie qu’une relecture pendant une clôture en cours ne la relance pas. |
| CA-08 | Ouvrir les destinations fréquentes, les anciens liens et le menu mobile, y compris depuis un formulaire modifié. | Bancs de navigation, d’en-tête et de bilan/diffusion. Retour du focus au déclencheur et protection de la saisie. |
| CA-09 | Créer ou demander la préparation, vérifier la publication, suivre la preuve propre au modèle et contrôler la population à la clôture. | Douze parcours continus du portail sur API synthétique, six modèles à 390 et 1280 px, dans le [banc de continuité des six modèles](../../../../localeo-animation/tests/browser/e85-parcours-modeles.mjs). Chaque parcours passe par le catalogue, le brouillon (réutilisation pour la Chasse), un blocage de publication, le dossier qualifié, la clôture, le tirage, le gain, la résolution du dossier et le bilan relu depuis les archives. La demande accompagnée de la Chasse, son accusé et sa reprise sont aussi exercés dans le banc de préparation. La correction du blocage côté producteur et les gestes des commerçants sont simulés dans le banc de continuité. Les preuves transactionnelles PostgreSQL sont exécutées séparément. |
| CA-10 | Tirer les Coffrets, les lots à remettre ou les bons numériques, puis consulter le gain et traiter les conditions de fin. | Bancs tirage, file globale et `suivi-animation.mjs fin-dossiers`. Contrôles PostgreSQL de concurrence pour les commandes de tirage et de fin. |
| CA-11 | Lire la fiche en pleine largeur et sur téléphone, utiliser le clavier, agrandir le texte et consulter les tableaux. | Bancs à 320, 390 et 1600 px, dont 320 px avec texte à 200 %. [Capture de la fiche Participants](../../produit/formation/animation/illustrations/guide-quotidien/participants-1600.png) |
| CA-12 | Depuis une liste filtrée, examiner une publication en attente, une vitrine suspendue puis une tombola prête au tirage. | Scénario multi-éditions automatisé à 320 et 1280 px, avec retour au filtre et au bouton d’origine, sans écriture. La comparaison chronométrée et l’observation des hésitations avec des gestionnaires restent à réaliser. [Protocole de recette](recette.md) |

## Contrats et exploitation

- La fiche accepte un fait optionnel `tirage_applicable`. Une ancienne édition de nature inconnue garde l’accès à la consultation autorisée. La projection de la file tient compte d’un tirage existant.
- Les listes de participants du Juste Prix et des Vitrines acceptent `avec_total`. La lecture de la Tombola publique demande aussi le total filtré. Le coût du comptage reste limité aux requêtes qui le demandent. [OpenAPI canonique](../epic-41-api/openapi.json)
- La reprise d’un jeu spécialisé suspendu tient compte de la période publiée. La lecture et la commande contrôlent la même règle. Avant confirmation de la clôture, le gestionnaire peut consulter les personnes qualifiées et revenir à son motif saisi. Le portail et la vue de gestion Juste Prix de l’ERP utilisent la disponibilité fournie par le backend. Les opérations de clôture et d’attribution conservent leurs contrôles serveur.
- Les modifications portent sur Localeo Animation, le backend et la documentation commune. Le schéma de stockage ne change pas. Les jeux de recette sont synthétiques. La refonte ne demande ni migration des éditions, ni nouvelle donnée obligatoire du générateur de démonstration.
- Les étapes de mission, de validation et de remise dans Pro conservent leurs écrans et leurs libellés. Le guide Commerçant reste applicable. Le guide Animation révisé comprend les captures de pilotage, de publication, de participants, de clôture et de tirage. Ses 25 pages ont été rendues et relues, la copie embarquée est identique au PDF canonique et le lien du portail a été testé. [Guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) · [Guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md)

## Contrôles complémentaires

La suite du portail a passé 437 tests, le contrôle TypeScript, ESLint et la construction applicative. Le banc du pilotage compte 14 scénarios réussis, dont le retour à la ligne d’origine après trois interventions.

Le test de performance des listes spécialisées demande une page de 25 personnes dans des éditions de 1 000 et 10 000 inscrits, avec autant de personnes dans une autre édition. Sur PostgreSQL 18 local, une seule requête a renvoyé les lignes et le total filtré exact de 500 ou 5 000 qualifiés. Les médianes observées sur dix lectures ont été de 6,50 et 6,59 ms avec total, contre 3,78 et 2,97 ms sans total. Ces mesures dépendent de la base locale. [Test de performance reproductible](../../../../localeo-backend/tests/performance/test_e85_populations_postgres.py)

Le lot PostgreSQL de 34 tests a couvert les projections de productivité, les chaînes Juste Prix et Vitrines et des commandes concurrentes. Un lot de 24 tests a vérifié les recommandations de suspension. Deux scénarios PostgreSQL supplémentaires ont enchaîné inscription en Tombola publique, gel, tirage, gain et remise. Les totaux de ces lots ne s’additionnent pas en un décompte de cas distincts.

Les sept contrôles PostgreSQL de démonstration sur les dotations et la fin sont passés après mise à jour de l’attendu du compteur d’unités non justifiées. La revue exige que ce compteur retombe à zéro avant de proposer de terminer.

Les contrôles unitaires transversaux du générateur présentent huit échecs également reproduits sur une copie du commit backend `f90e965f`, avant modifications. Sept viennent d’une fixture de génération dépourvue de session. Le huitième concerne une preuve de passage que le test attend de voir refuser. Les fichiers du générateur concernés ne sont pas modifiés par E85.

Les contrôles ci-dessus sont locaux. Le déploiement et la revue comparative avec des gestionnaires constituent des opérations distinctes. L’epic reste en cours.


## Refonte de la fiche du 26 novembre 2026

La barre de navigation indique l’étape métier pendant les consultations transversales. Une édition active ouvre Participation. La liste des participants, les validations applicables, l’historique des messages, la confirmation d’une clôture et le résultat du tirage se consultent dans la même édition. Les libellés de confirmation et les indicateurs du bilan suivent les données et capacités renvoyées par le serveur.

| Objet vérifié | Contrôle local |
| --- | --- |
| Orientation | Ouverture par statut, liens directs historiques, lecture seule, menu Actions et retour du focus. [Banc des rubriques](../../../../localeo-animation/tests/browser/animation-workspace-ux.mjs) |
| Participation | Populations, filtres, retour du dossier et présentation des premières lignes sur ordinateur. [Parcours des modèles](../../../../localeo-animation/tests/browser/e85-parcours-modeles.mjs) |
| Communication | Quota, brouillon, aperçu, aide, clavier et lecture seule sur trois largeurs. [Recette des communications](../../../../localeo-animation/tests/browser/communication-ux.mjs) |
| Attribution | Lots libres avec zéro éligible, coffrets insuffisants, consultation sans droit d’écriture et commande dont le résultat est incertain. [Banc dotation](../../../../localeo-animation/tests/browser/dotation.mjs) |
| Bilan | Mesures connues, couverture partielle, satisfaction, exports et conservation du dernier résultat lors d’une erreur de lecture. [Contrôles du bilan](../../../../localeo-animation/tests/browser/bilan-visual-checks.mjs) |

Les douze parcours continus réussissent à 1280 × 800 et 390 × 800, de la création à la réouverture de l’archive. Sur les six modèles, la première participation est entièrement visible à 1280 × 800 dans le scénario nominal. Le banc dotation couvre douze combinaisons de scénario et de largeur pour les confirmations, leurs blocages et les commandes incertaines. Le banc du bilan passe sur huit configurations, y compris avec texte agrandi. La suite unitaire Animation compte 437 tests réussis.

La livraison concerne le portail Animation et le guide Animation. Elle réutilise les règles et les contrats existants. Aucune migration ni adaptation du générateur de démonstration, du portail Commerçant ou des procédures d’exploitation n’est requise. Les recettes locales emploient des éditions synthétiques. La comparaison chronométrée avec des gestionnaires reste à réaliser.

## Retour entre rubriques et accès à la liste

| Geste du gestionnaire | Résultat vérifié en navigateur sur des éditions synthétiques |
| --- | --- |
| Reprendre une animation depuis la liste | Deux lignes complètes sont visibles à 1280 × 800 et une ligne avec son action à 390 × 800. Après consultation, la vue enregistrée, les filtres, la page 2 et le focus sur la ligne d’origine sont restitués. [Recette de la liste](../../../../localeo-animation/tests/browser/productivity-workspace.mjs) |
| Changer de vue dans une rubrique | Depuis Fin et archivage, Gains ou Historique, la première vue de la rubrique est directement accessible. La navigation est aussi vérifiée à 320 px et avec le texte à 200 %. [Recette de navigation](../../../../localeo-animation/tests/browser/animation-workspace-ux.mjs) |
| Comprendre un tirage ou une fin bloqués | Avant le gel, les compteurs dépendant des participations indiquent « Après clôture ». Un tirage confirmé peut afficher zéro. Le gestionnaire peut ouvrir la revue de clôture ou le dossier sans gagnant concerné, puis revenir à la liste des dossiers. La consultation ne déclenche aucune commande métier. [Tirage](../../../../localeo-animation/tests/browser/dotation.mjs) · [Fin et archivage](../../../../localeo-animation/tests/browser/fin-animation.mjs) |

Les six modèles ont été parcourus de la création à la consultation de l’archive sur ordinateur et téléphone. La suite unitaire du portail compte 438 tests réussis. Le [guide Animation de 26 pages](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) illustre les vues enregistrées, la navigation de clôture et le tirage avant le gel. Les liens du profil et de l’assistance servent la même version que le PDF canonique. Le complément concerne le portail Animation et sa documentation. Les contrats backend, le schéma de données et les gestes du guide Commerçant restent identiques.

## Pilotage quotidien et repères visuels dans les onglets

| Geste | Observation en recette locale |
| --- | --- |
| Commencer la journée | Les trois premières interventions précèdent le choix de période et les graphiques. La première action tient dans la hauteur initiale de 800 px sur ordinateur et téléphone. Une file vide confirmée a son propre message. [Tableau de bord](../../../../localeo-animation/tests/browser/dashboard-pilotage.mjs) |
| Passer d’une recommandation à son dossier | Pour trois lots définitivement sans gagnant, le tableau de bord et la liste ouvrent le dossier de justification. Revenir restitue le focus au bouton d’origine. Plusieurs dossiers conduisent à la liste « À résoudre ». Les filtres et droits sont appliqués à l’édition consultée. [Liste et retours](../../../../localeo-animation/tests/browser/productivity-workspace.mjs) · [Fin de l’animation](../../../../localeo-animation/tests/browser/fin-animation.mjs) |
| Publier puis suivre les participants | Le reçu indique la date effective quand elle est connue et permet de rejoindre le suivi autorisé. L’identité et l’accès au participant précèdent les actions de gestion. Le même enchaînement passe pour les six modèles à 1280 et 390 px, jusqu’à la consultation de l’archive. [Parcours continus](../../../../localeo-animation/tests/browser/e85-parcours-modeles.mjs) |
| Comprendre le tirage et le bilan | Les lots en attente d’attribution sont distincts des lots à justifier. Le bilan présente le résultat confirmé, y compris zéro gagnant, ou l’état de tirage connu. Les mesures propres à un tirage sont omises quand il ne s’applique pas. [Bilan](../../../../localeo-animation/tests/browser/bilan-visual-checks.mjs) |
| Se repérer à l’intérieur d’un onglet | Les pictogrammes de gestion accompagnent les libellés des indicateurs, des états et des gestes principaux. Le reçu de publication, le quota de communication, la clôture et les chiffres clés du bilan sont illustrés dans le [guide Animation de 26 pages](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf). |

Les lectures du backend enrichissent les recommandations et l’état d’attribution. Les nouveaux champs sont facultatifs pour les consommateurs. La projection du bilan et ses indicateurs sont lus dans le même instantané. Aucun changement de schéma, de configuration de déploiement ou de données de démonstration n’est requis. Les gestes des commerçants restent ceux du guide Pro.

Les 438 tests unitaires du portail, TypeScript, ESLint et la construction applicative passent. La recette du portail couvre 4 scénarios de tableau de bord, 20 de navigation depuis les priorités et les listes, 42 de fin et de gestion des dossiers, ainsi que 8 configurations du bilan. Le guide canonique et la copie embarquée sont identiques. Les accès depuis le profil et l’assistance ont été contrôlés sur deux largeurs.

Neuf scénarios PostgreSQL du parcours transversal vérifient notamment la même recommandation en liste et en fiche, le refus d’une justification prématurée, la conservation d’une preuve historique et la cohérence d’une lecture pendant la confirmation du tirage. La lecture de la recommandation de fin utilise trois requêtes pour une édition comme pour 25. La régression PostgreSQL couvre en outre le bilan, la productivité, les limites de commune et d’organisation, et l’archivage sans lot. [Contrôles de fin et de productivité](../../../../localeo-backend/tests/security/test_productivite_fin_public_postgres.py)

Le banc local a parcouru des listes de 1 000 et 10 000 éditions. Avec 10 000 éditions et un cache chaud, la lecture d’une page de 25 a pris au maximum 47 ms sur cinq essais et la file d’actions 179 ms. Ces mesures concernent l’adaptateur PostgreSQL local, hors HTTP. [Banc reproductible](../../../../localeo-backend/tests/security/test_productivite_animation_postgres.py)

Les preuves navigateur utilisent une API synthétique et les preuves transactionnelles une base PostgreSQL locale. Les parcours de ce lot restent à observer avec des gestionnaires sur l’environnement publié.

## E85-EVO-01 — Refonte de la navigation et de la préparation

| Critères | Preuves locales |
| --- | --- |
| CA-13 · Navigation par état | Douze parcours complets couvrent les six modèles à 390 et 1280 px. La frise et les anciens liens passent 39 scénarios à 320, 390 et 1280 px. La recette des retours et des alertes couvre 21 scénarios organisateur, 20 scénarios de productivité et 68 écrans d’alertes. |
| CA-14 · Visuel et QR | La recette PostgreSQL vérifie l’ajout et le retrait de l’illustration, l’Assistant, les visuels de configuration, l’isolation entre éditions et l’accès public au QR après publication. Le banc de personnalisation du flyer passe 184 contrôles sur trois modes de dotation. Le parcours intégré à 320 et 1280 px vérifie le focus sur l’illustration, l’ajout, le retour au contrôle relu et le retrait. |
| CA-15 · Liste et réemploi | Vues enregistrées 9/9, dont zoom à 200 %, et clonage 31/31, dont Archives et restauration du focus. |
| CA-16 · Création et lot libre | Douze parcours de création manuelle, huit scénarios de sauvegarde et reprise avec verrouillage du modèle, et cinq scénarios Chasse. Dotation 12/12, plus quatre scénarios avec texte agrandi à 200 %. |

Le portail passe 441 tests, TypeScript, ESLint et le build. Côté backend, 791 contrôles d’architecture et 36 tests de la sélection PostgreSQL passent. Les suites backend élargies présentent cinq échecs dans des doubles ou des assertions historiques. La comparaison avec `HEAD` confirme que les chemins en cause sont inchangés. Les suites élargies restent à rejouer sur `HEAD` pour confirmer cette attribution.

Le [guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) compte 26 pages rendues et relues. Ses 25 liens de sommaire et 25 liens de retour sont vérifiés. La copie embarquée est identique. Le profil et l’assistance servent le PDF contrôlé à 390 et 1 024 px, y compris lorsque la lecture des demandes d’assistance échoue. Le guide Commerçant reste applicable aux gestes de consultation du flyer et d’utilisation des QR.

La livraison réutilise les contrats API, le stockage et la configuration de déploiement. Le test `test_complete_dataset_relations` sur PostgreSQL 18 jetable confirme les dix visuels distincts rattachés aux éditions générées et les deux préparations prévues sans image. La boucle de correction s’appuie sur Backend et Animation. La recette a utilisé des API synthétiques et PostgreSQL local. L’EPIC 85 est en cours.

## E85-EVO-02 — Rubriques selon l’état de l’édition

| Critère | Preuves locales |
| --- | --- |
| CA-17 · Reprendre une préparation | Six configurations de liste passent, dont 320 et 390 px et le zoom à 200 %. Le lien historique ouvre le dossier et les retours restituent la recherche, le filtre, la deuxième page et le focus, aussi depuis **À traiter**. Huit scénarios de sauvegarde et reprise passent. Le banc du guide vérifie le retour à 390 et 1 024 px. [Liste et retours](../../../../localeo-animation/tests/browser/mobile-first-lists.mjs) · [Sauvegarde et reprise](../../../../localeo-animation/tests/browser/wa-b1-preparations.mjs) |
| CA-18 · Navigation suivant l’état | Le banc organisateur passe 29 scénarios Chromium à 1 280 et 390 px, avec un contrôle de repli à 320 × 256 px. L’ancien lien Tirage explique la fermeture attendue sans lecture du tirage, la fermeture effective ouvre Tirage et Bilan, et le résumé d’annulation et les destinations historiques restent accessibles selon les droits. Le banc de navigation passe huit scénarios, dont 320 et 390 px et texte à 200 % à 320 et 1 280 px. La frise passe 39 scénarios à 320, 390 et 1 280 px. [Parcours organisateur](../../../../localeo-animation/tests/browser/po-organisateur.mjs) · [Navigation](../../../../localeo-animation/tests/browser/animation-workspace-ux.mjs) · [Frise](../../../../localeo-animation/tests/browser/workflow-timeline.mjs) |
| CA-19 · Réglages après publication | Le banc organisateur contrôle le focus de l’ancien lien sur Dates et inscriptions, le droit de lecture et la configuration publiée en lecture seule. Le banc dédié passe à 390 et 1 280 px pour la capacité, la prolongation et la réouverture des inscriptions, la lecture seule, la garde de saisie, le conflit et la récupération d’un reçu après perte de réponse. Le banc du guide vérifie les dates et inscriptions, le contact et l’annonce du tirage dans Exploitation. [Parcours organisateur](../../../../localeo-animation/tests/browser/po-organisateur.mjs) · [Réglages d’exploitation](../../../../localeo-animation/tests/browser/parametres-exploitation.mjs) |

Le portail passe 442 tests, TypeScript et ESLint. Les six modèles passent leurs 12 parcours complets à 390 et 1 280 px. Le bilan passe huit configurations de largeur et de zoom. L’entrée depuis Mes archives ouvre le bilan définitif à 320 et 1 280 px et laisse les dossiers de fin accessibles. Le banc du guide produit 37 captures sur deux largeurs sans erreur navigateur, lecture API imprévue ni écriture.

Le [guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) compte 27 pages rendues et relues. Il ajoute un geste dédié aux réglages après publication et documente l’accès à Préparations et au bilan provisoire. Les 26 entrées de sommaire, les 26 liens de retour et les 27 signets ont été contrôlés. `npm run guide:check` confirme l’identité de la copie embarquée et le [banc du guide](../../../../localeo-animation/tests/browser/animation-guide.mjs) vérifie les liens au clavier et le PDF servi à 390 et 1 024 px, y compris avec l’assistance indisponible.

La relecture du [guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md) a confirmé que les gestes d’invitation, de préparation du commerce, de consultation du flyer et d’utilisation des QR de lieu s’appliquent toujours. Le portail utilise les statuts, capacités et contrats API existants. Les scénarios de démonstration existants couvrent les états concernés. Cette recette locale utilise des données synthétiques. La qualification avec des gestionnaires en environnement publié reste à faire.

### Ajustements du 26 novembre 2026

Le modèle choisi apparaît à côté de **Nouvelle animation**. Les informations demandées avant de poursuivre sont présentées dans l’encart **Pour continuer**. La revue **Clôture** s’ouvre depuis la fiche dès la publication, y compris avant l’échéance. **Gains et remises** distingue la déclaration d’une remise de lot externe des autres événements de suivi.

Chromium confirme 12 parcours de création, 29 parcours organisateur et huit configurations de navigation, dont texte à 200 %. La déclaration de remise passe dix scénarios à 320 et 1 280 px. Ces scénarios couvrent la confirmation, le refus du lot, le conflit de version, la lecture seule et le reçu après perte de réponse. Le guide Animation et sa copie embarquée ont été actualisés et relus. L’accès au PDF passe à 390 et 1 024 px. [Déclaration de remise](../../../../localeo-animation/tests/browser/dotation.mjs) · [Guide dans l’application](../../../../localeo-animation/tests/browser/animation-guide.mjs)

<a id="e85-evo-03-priorite-remise"></a>

## E85-EVO-03 — Priorité à la remise du lot

La recette E85-CA-20 part d’Animation `a69d11c` et des modifications
locales. Le build avant cette évolution reproduit le formulaire de suivi
affiché d’emblée à 320 px. Après l’évolution, l’ouverture donne la priorité
à la déclaration de remise. La commande secondaire ouvre le suivi sur demande.

- Le [banc Dotation](../../../../localeo-animation/tests/browser/dotation.mjs)
  passe 20 parcours ciblés à 320 et 1 280 px. Les cas remise et refus sont
  rejoués avec l’annulation au clavier et le retour du focus, puis à 320 px
  avec texte à 200 %. Les cas de conflit de version et de réponse perdue
  conservent les saisies et la vérification du reçu.
- Les scénarios ciblés du [banc Bons numériques](../../../../localeo-animation/tests/browser/digital-prizes.mjs)
  et du [banc Productivité](../../../../localeo-animation/tests/browser/productivity-operations.mjs)
  valident le suivi d’un bon, la reprise d’une page de gains, la saisie pendant
  la relecture de l’historique et le reçu après réponse perdue. Les deux bancs
  complets s’arrêtent aussi sur la version de départ, respectivement sur une
  sélection de stock désactivée et sur le filtre de recherche des participants
  masqué. Les scénarios de suivi ont été rejoués séparément.
- Les 442 tests de `pnpm test`, TypeScript, ESLint et le build isolé passent.
  Les formes de commande, droits et reçus viennent du contrat existant.
  La recette s’appuie sur des réponses API synthétiques. Les données de
  démonstration disponibles suffisent à alimenter le détail du gain.
- Le [guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf)
  présente les deux actions et la confirmation de remise en page 22. Les
  captures du choix initial à 390 et 1 024 px se trouvent dans le rapport de
  recette. Les 28 pages du PDF et ses 54 liens internes ont été vérifiés.
  La copie embarquée correspond au PDF canonique et son accès dans le build
  a été vérifié aux deux largeurs. Le guide Commerçant couvre la remise par
  le Scanner de Pro, qui relève d’un autre parcours.

## E85-EVO-BILAN-DIFFUSION — Bilan et rapport à partager

Recette locale du 27 novembre 2026, sur les bases Backend `204c6466` et
Animation `7e936e4` avec l’évolution. Les contrôles finaux de rendu et
d’architecture ont aussi été rejoués avec Backend `aea3811d`.
Voir les [critères du bilan](bilan-diffusion.md).

| Critère | Vérification exécutée |
| --- | --- |
| E85-CA-21 | Deux volets du [banc Bilan](../../../../localeo-animation/tests/browser/animation-workspace-ux.mjs) réussis, chacun sur huit configurations jusqu’à 320 px avec texte à 200 %. Les scénarios couvrent notamment les états provisoire et définitif, les téléchargements des trois formats, le focus après actualisation et le refus de télécharger les annexes quand la route de diffusion est indisponible. |
| E85-CA-22 | Quatre tests [PostgreSQL 18.3](../../../../localeo-backend/tests/security/test_bilan_pdf_postgres.py) réussis sur une base jetable migrée. Ils couvrent le changement de jour de Paris en été et en hiver, le tenant, les validations exclues, les bornes et la cohérence de l’instantané pendant une inscription concurrente. Les deux plans synthétiques utilisent les index d’édition. La médiane passe de 2,1 à 18,2 ms entre 1 000 et 10 000 lignes cibles par table pour 30 jours rendus. |
| E85-CA-23 | Les [tests de rendu](../../../../localeo-backend/tests/infrastructure/test_bilan_animation_pdf.py) vérifient les états du tirage, les mesures manquantes, le regroupement des dates, les valeurs et les pics, la pagination, la langue et les liens du sommaire. Toutes les pages de rapport complet, provisoire partiel et interne ont été rendues et relues sur données fictives. |
| E85-CA-24 | Les [tests API](../../../../localeo-backend/tests/api/test_bilan_pdf_export.py) et [de l’instantané](../../../../localeo-backend/tests/application/animation_locale/test_bilan_pdf_snapshot.py) vérifient les droits, le refus du débordement et les deux projections. Les deux PDF déclarent le transport de session Animation dans le contrat généré, documentaire et embarqué. La route CSV conserve le contrat déjà consommé. |

Les 44 tests backend ciblés et les 793 contrôles d’architecture passent. Les
443 tests d’Animation, TypeScript, ESLint et le build isolé passent. Le profil
général de défilement s’arrête dans la liste Animations avant le Bilan, avec
le même résultat sur un build antérieur.

Le [guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf)
présente le téléchargement en page 25 et utilise des captures réelles du
portail sur API synthétique. Les 30 pages rendues et les 58 liens internes ont
été relus. La copie distribuée est vérifiée depuis Aide et support et le menu
du compte à 390 et 1 024 px, y compris lorsque le support est indisponible. Le
guide Commerçant couvre les gestes dans Pro. Les données de démonstration
existantes alimentent les mêmes lectures. Les vérifications publiées ici
portent sur l’environnement local.

## E85-EVO-VISUEL · 28 novembre 2026

Les vérifications locales utilisent les bases Backend `d4e26d90`, Animation `60832f9`, Marketplace `ec7cf5f` et Pro `46a6990`, avec le diff de cette évolution. [Spécification du visuel](visuel-animation.md)

| Critère | Vérification locale |
| --- | --- |
| E85-CA-25 | Les tests navigateur Animation vérifient la navigation par la revue et le lien ancien, le focus, le choix d’un exemple, l’import et le retrait. Recette de navigation à 320, 390 et 1 280 px. [Navigation](../../../../localeo-animation/tests/browser/flyer-navigation.mjs) · [Personnalisation](../../../../localeo-animation/tests/browser/flyer-personnalisation.mjs) |
| E85-CA-26 | Les tests d’infrastructure vérifient la présence, le décodage et la distinction des 18 WebP, à raison de trois par moteur. La planche rendue permet de relire le geste de scan et le thème dans les deux recadrages. [Catalogue des visuels](../../../../localeo-backend/tests/infrastructure/animation_locale/test_exemples_visuels.py) |
| E85-CA-27 | Le passage des 18 couvertures finales par le backend donne des vignettes Live de 9,6 à 14,7 Kio, des cartes Marketplace de 21,9 à 34,0 Kio et des images de fiche de 99,2 à 171,3 Kio. Les tests vérifient aussi la conversion des anciens PNG. Deux scénarios navigateur par lecteur vérifient le chargement et le repli dans Live, Marketplace et Pro sur téléphone et bureau. [Conversions](../../../../localeo-backend/tests/infrastructure/animation_locale/test_illustration_flyer.py) · [Visibilité Pro](../../../../localeo-commercant/tests/e2e/animations.spec.js) |
| E85-CA-28 | Les cas ciblés sur PostgreSQL 18 couvrent la sélection et le refus d’un exemple étranger, le rattachement atomique du PNG et de ses trois WebP, la diffusion, le renouvellement d’URL au remplacement et le retrait. La recette du flyer vérifie conflit et reprise par reçu. [Tests transactionnels](../../../../localeo-backend/tests/security/test_illustration_flyer_publique_postgres.py) |
| E85-CA-29 | Les 31 pages Animation et les 18 pages Pro ont été rendues et relues. Les captures finales illustrent un passage validé par QR. Les liens chargent en navigateur les PDF identiques aux copies canoniques. Les contrats synchronisés présentent 445 opérations Animation et 70 Pro sans écart sémantique. [Guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) · [Guide Commerçant](../../../livrables/formation/commercant/guide-quotidien-localeo-commercant.pdf) |

Le flyer A4 du Passeport a été rendu avec le visuel final. Le scan en boutique est lisible dans l’illustration et le QR d’inscription est visible dans son bloc dédié. La suite Node complète d’Animation est passée en relance. Six tests ciblés passent sur le catalogue final et le transfert des documents de démonstration.

La recette complète du jeu de démonstration sur PostgreSQL 18 donne 12 réussites, dont `test_complete_dataset_relations`, et deux échecs hors du parcours de visuel. Le scénario Vitrines Pâques refuse d’attester un passage sur une étape invalide. La recette de sauvegarde et réinstallation s’arrête à l’inventaire des trois tables Passkeys Pro. La relance ciblée réussit avec le visuel final, ses dérivés et les deux éditions publiques, l’une illustrée et l’autre en repli. [Tests du jeu de démonstration](../../../../localeo-backend/tests/integration/test_demo_dataset.py)

### Couvertures de Découvrir

**28 novembre 2026.** L’extension d’E85-CA-27 porte sur les cartes de **Découvrir** et les légendes de l’aperçu organisateur. Les bases locales sont Marketplace `ec7cf5f` et Animation `60832f9` avec leurs modifications de travail. Chromium utilise les builds isolés et les API simulées. [Décision et recette attendue](visuel-animation.md#couverture-des-cartes-découvrir-dans-live)

- **E85-CA-27.** À 320, 390 et 1 280 px, les scénarios vérifient le bandeau de 160 px sur toute la largeur, la miniature d’une réponse historique, une période à carte seule et une liste mixte. Les requêtes contiennent une miniature paysage par carte illustrée et le visuel de fiche à l’ouverture. L’action s’ouvre au clavier et reprend le focus au retour. Les captures avec les dérivés WebP du Passeport et du Jeu des vitrines ont été relues. Ces fichiers de 480 × 270 px pèsent 28 924 et 24 958 octets, sous le plafond de 35 Kio. [Recette des couvertures](../../../../localeo-marketplace/tests/visual/live-iconography-discovery.spec.cjs)
- **E73-LH-07 et E73-LH-08.** Le contrôle du premier écran à 390 px passe pour une édition sans image et une édition au format compact historique. La couverture paysage place l’action plus bas dans le défilement. La réponse 404 différée conserve la hauteur du bandeau et la position du bouton. Les retours depuis la troisième page et la vignette de fiche commerce sont vérifiés sur les tailles prévues. [Stabilité](../../../../localeo-marketplace/tests/visual/live-hierarchy-fluidity.spec.cjs) · [Continuité](../../../../localeo-marketplace/tests/visual/live-discovery-continuity.spec.cjs) · [Liste commerce](../../../../localeo-marketplace/tests/visual/live-card-actions-layout.spec.cjs)
- **Guide Animation.** Le parcours de choix et de retrait confirme les deux légendes à 320, 390 et 1 280 px. La page 15 a été rendue et relue. La comparaison du rendu confirme l’identité des 30 autres pages. Le test d’accès vérifie le lien et les octets du PDF embarqué. Le guide Commerçant décrit la fiche Pro, qui consomme le visuel de fiche indépendamment du catalogue Live. [Guide Animation](../../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) · [Navigation](../../../../localeo-animation/tests/browser/flyer-navigation.mjs) · [Accès au guide](../../../../localeo-animation/tests/browser/animation-guide.mjs)

La première passe `2026-11-28T11-44-04-158Z-2HyrJF` compte 70 réussites et sept écarts sur la hauteur d’image et les attentes des tests concernés. Après correction, `2026-11-28T11-50-26-506Z-nSlzAy` confirme les trois scénarios de couverture et les retours de navigation. Elle isole un écart de fixture dans le contrôle du premier écran, qui s’exécutait avec le paysage. `2026-11-28T11-52-19-736Z-jD7Xdx` valide les trois scénarios de compatibilité et de stabilité avec les entrées prévues. Les rapports sont conservés sous `localeo-marketplace/test-results/visual-runs/`.

Le choix de variante est local à l’interface et utilise les URL, budgets et contrôles de visibilité du contrat existant. Les deux exemples proviennent du catalogue déjà livré. Les règles et données de génération, les migrations et la configuration de diffusion relèvent du [périmètre du visuel partagé](visuel-animation.md#images-et-contrat).
