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
