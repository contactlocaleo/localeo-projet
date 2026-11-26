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
