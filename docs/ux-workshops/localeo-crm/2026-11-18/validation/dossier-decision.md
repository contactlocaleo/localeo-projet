# Dossier de décision — orientations UX Localeo CRM

Préparé le **19 novembre 2026**, heure de Paris, dans l’exécution commencée le 18 novembre. **Cinq orientations P1 en attente de votre décision ; aucune orientation validée.** Aucun P0 démontré. L’adoption et les préférences des douze profils sont simulées ; elles ne valent pas accord utilisateur.

Sources : [rapport exécutif](../workshop/rapport-executif.md), [backlog UX](../workshop/backlog-ux.md), [votes motivés](../workshop/votes-et-arbitrages.md), [observations factuelles](../observations/observations-factuelles.md), [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html) et [revue des maquettes](../visuels/arbitrages-complementaires.md).

Les risques critiques pour la mise en usage sont présentés séparément dans le [registre des risques non résolus](risques-non-resolus.md). Le GO sous conditions du workshop concerne la préparation d’un pilote encadré sur ordinateur, sans validation d’un usage autonome à dix personnes.

## Lecture rapide

| ID | Orientation | Priorité | Vote simulé pour/contre/abstention | Effort relatif |
| --- | --- | --- | --- | --- |
| [UX01](#ux01) | Rendre visible un résumé quotidien et collectif | P1 | 12 / 0 / 0 | M |
| [UX02](#ux02) | Donner accès aux listes de risques du portefeuille | P1 | 8 / 1 / 3 | L |
| [UX03](#ux03) | Clarifier les responsables du prospect, du dossier et de l'action | P1 | 12 / 0 / 0 | S |
| [UX04](#ux04) | Expliciter le rattachement de la prochaine action | P1 | 12 / 0 / 0 | M |
| [UX05](#ux05) | Rendre vérifiable la continuité du rendez-vous jusqu'à la prochaine étape | P1 | 12 / 0 / 0 | M |

S = limité, M = intermédiaire, L = important : estimations relatives du workshop, sans engagement de délai ni devis technique. UX03 est estimée S pour les libellés ; une interaction d’affectation à compléter devra être réestimée. Aucun bénéfice n’a encore été mesuré auprès d’utilisateurs réels.

**Point d’attention UX02 :** 8 votes d’adoption, mais 7 réserves visuelles sur 12. Décider de l’orientation et, si nécessaire, préciser les conditions sur l’agencement, les définitions et la recette mobile.

## Comment décider

Pour chaque ID, indiquer **VALIDÉE**, **REFUSÉE**, **À RÉVISER** ou **REPORTÉE**, avec commentaire et conditions éventuelles. Une réponse partielle laisse les autres orientations en attente. « VALIDÉE » vaut accord sur l’orientation et ses conditions explicites ; cette phase ne déclenche aucune implémentation. Les risques restent ouverts tant que leurs preuves de levée manquent.

Le [registre des décisions](decisions.md) sera renseigné à réception de vos choix ; le [backlog potentiel](backlog-implementation-potentiel.md) sera alors réparti selon ces choix. Les P2 UX06–UX10 et les propositions rejetées en simulation UX11–UX13 sont hors du présent périmètre ; elles ne sont pas enregistrées comme refusées par vous.

<a id="ux01"></a>

## UX01 — Rendre visible un résumé quotidien et collectif

- **Parcours :** Accueil, priorités, suivi collectif.
- **Priorité / effort :** P1 / M ; confiance : Moyenne.
- **Vote simulé :** 12 POUR, 0 CONTRE, 0 ABSTENTION ; orientation adoptée au seuil de 7/12.
- **Préférence visuelle simulée :** 12 APRÈS, 0 AVANT, 0 RÉSERVE.
- **Décision utilisateur :** EN ATTENTE DE DÉCISION.

**Problème.** L'accueil personnel vide et les indicateurs collectifs repliés ne donnent pas immédiatement l'état du portefeuille.

**Preuves.** OBSERVÉ O01–O02 ; DÉDUIT O16. Compréhension réelle : HYPOTHÈSE. Voir les [observations](../observations/observations-factuelles.md) et la [couverture du pilotage](../observations/couverture-pilotage-commercial.md).

**Conséquence utilisateur possible.** Un nouvel utilisateur pourrait confondre aucune action personnelle et aucune activité collective.

**Orientation proposée.** Conserver Mes actions/Équipe, afficher un résumé compact de la portée sélectionnée (retards, actions du jour, prochains RDV) et un accès explicite aux indicateurs collectifs existants ; distinguer zéro, chargement et indisponibilité.

**Bénéfice attendu.** Démarrer la journée avec des priorités et une portée compréhensibles.

**Capture AVANT :** [ouvrir la capture réelle](../visuels/captures-avant/01-accueil-bureau.png). Aujourd’hui, portée Mes actions : trois files vides ; les indicateurs partagés sont repliés en bas. Le volume collectif n’est pas visible dans cette capture.

**Maquettes APRÈS :** [comparaison côte à côte / bascule mobile](../visuels/comparatif-avant-apres.html#ux01). Données fictives ; les images ne prouvent pas le fonctionnement du CRM.

- [ux01-accueil](../visuels/maquettes-apres/ux01-accueil.html) — [PNG bureau](../visuels/maquettes-apres/ux01-accueil-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux01-accueil-mobile.png).
- [ux01-equipe](../visuels/maquettes-apres/ux01-equipe.html) — [PNG bureau](../visuels/maquettes-apres/ux01-equipe-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux01-equipe-mobile.png).
- [ux01-etats](../visuels/maquettes-apres/ux01-etats.html) — [PNG bureau](../visuels/maquettes-apres/ux01-etats-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux01-etats-mobile.png).

**Risques et dépendances.** R01, R04, R05. Les compteurs doivent conserver la même population, période et pagination que les listes. Dépend des termes clarifiés par UX03/UX04 et des définitions de UX02 ; aucun total collectif exhaustif encore prouvé. Voir le [registre](risques-non-resolus.md).

**Preuves attendues avant mise en usage, proposées et non acquises :**

1. La portée, la période et le fuseau sont visibles pour chaque total ; un zéro personnel ne qualifie jamais le portefeuille collectif.
2. Chaque total ouvre la liste correspondante avec les mêmes filtres ; nombres et pagination sont cohérents sur un jeu de test contrôlé.
3. L'état vide explique la portée et permet d'ouvrir l'équipe ; aucun chargement ou échec ne devient un faux zéro.

<a id="ux02"></a>

## UX02 — Donner accès aux listes de risques du portefeuille

- **Parcours :** Pilotage global et filtres.
- **Priorité / effort :** P1 / L ; confiance : Moyenne sur le besoin ; faible sur les fonctions manquantes.
- **Vote simulé :** 8 POUR, 1 CONTRE, 3 ABSTENTIONS ; orientation adoptée au seuil de 7/12.
- **Préférence visuelle simulée :** 5 APRÈS, 0 AVANT, 7 RÉSERVE : pas de préférence majoritaire pour la maquette.
- **Décision utilisateur :** EN ATTENTE DE DÉCISION.

**Problème.** Le repérage global des non attribués, sans suivi récent et dossiers stagnants n'est pas établi.

**Preuves.** HYPOTHÈSE de couverture insuffisante ; couverture-pilotage-commercial.md. O09, O16 ; filtre dossier sans action DÉDUIT du code. Voir les [observations](../observations/observations-factuelles.md) et la [couverture du pilotage](../observations/couverture-pilotage-commercial.md).

**Conséquence utilisateur possible.** Des dossiers à risque pourraient rester hors du champ de la revue d'équipe.

**Orientation proposée.** Vérifier et rendre accessibles les vues existantes ; compléter seulement les manques pour non attribués, prospects sans action, dossiers sans action, sans interaction récente, sans évolution, retards et RDV à venir. Définir les populations et seuils avec le métier.

**Bénéfice attendu.** Une revue de portefeuille vérifiable, avec des listes permettant d'agir.

**Capture AVANT :** [ouvrir la capture réelle](../visuels/captures-avant/14-fiche-avec-action-bureau.png). Fiche de test : une prochaine action est affichée en haut, mais le dossier en bas reste sans prochaine action. Cela illustre la distinction des unités ; cette capture ne prouve pas l’absence d’une liste globale.

Capture complémentaire : [01-accueil-bureau.png](../visuels/captures-avant/01-accueil-bureau.png).

**Maquettes APRÈS :** [comparaison côte à côte / bascule mobile](../visuels/comparatif-avant-apres.html#ux02). Données fictives ; les images ne prouvent pas le fonctionnement du CRM.

- [ux02-risques](../visuels/maquettes-apres/ux02-risques.html) — [PNG bureau](../visuels/maquettes-apres/ux02-risques-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux02-risques-mobile.png).
- [ux02-prospects](../visuels/maquettes-apres/ux02-prospects.html) — [PNG bureau](../visuels/maquettes-apres/ux02-prospects-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux02-prospects-mobile.png).

**Risques et dépendances.** R01, R02, R04, R05. Vérifier les vues existantes avant tout complément ; définir populations, délais d’inactivité/stagnation et traitement des pauses avec le métier. Dépend de UX03/UX04 et des droits d’accès. Les exemples de la maquette ne fixent aucune règle métier. Les catégories se recoupent ; ne pas les additionner. Voir le [registre](risques-non-resolus.md).

**Preuves attendues avant mise en usage, proposées et non acquises :**

1. Chaque risque précise unité (prospect ou dossier), population, horizon et seuil ; pause justifiée et dossiers clos ont un traitement explicite.
2. Un jeu contrôlé couvre chaque risque, l'absence de risque et les cas de recouvrement ; total et liste concordent sur toutes les pages.
3. Les filtres responsable/équipe restent visibles ; les listes qui se recoupent ne sont pas additionnées comme un total de prospects uniques.

<a id="ux03"></a>

## UX03 — Clarifier les responsables du prospect, du dossier et de l'action

- **Parcours :** Création, qualification, affectation.
- **Priorité / effort :** P1 / S ; confiance : Moyenne.
- **Vote simulé :** 12 POUR, 0 CONTRE, 0 ABSTENTION ; orientation adoptée au seuil de 7/12.
- **Préférence visuelle simulée :** 12 APRÈS, 0 AVANT, 0 RÉSERVE.
- **Décision utilisateur :** EN ATTENTE DE DÉCISION.

**Problème.** Le responsable requis à la création est celui du dossier ; le prospect peut rester non attribué.

**Preuves.** OBSERVÉ O04–O05 ; confusion HYPOTHÈSE O17. Voir les [observations](../observations/observations-factuelles.md) et la [couverture du pilotage](../observations/couverture-pilotage-commercial.md).

**Conséquence utilisateur possible.** Une personne pourrait croire le prospect pris en charge alors que seule une opportunité l'est.

**Orientation proposée.** Nommer chaque rôle dans les formulaires et confirmations ; montrer le responsable du prospect et proposer son affectation explicite, sans copier silencieusement le propriétaire du dossier.

**Bénéfice attendu.** Savoir qui suit la relation et qui porte chaque action.

**Capture AVANT :** [ouvrir la capture réelle](../visuels/captures-avant/09-creation-prospect-bureau.png). Création d’un prospect avec premier dossier. Le champ Responsable est en fin de formulaire ; la fiche obtenue laisse le prospect non attribué. La confusion est une hypothèse, pas une erreur métier démontrée.

Capture complémentaire : [11-fiche-prospect-test-bureau.png](../visuels/captures-avant/11-fiche-prospect-test-bureau.png).

**Maquettes APRÈS :** [comparaison côte à côte / bascule mobile](../visuels/comparatif-avant-apres.html#ux03). Données fictives ; les images ne prouvent pas le fonctionnement du CRM.

- [ux03-responsabilites](../visuels/maquettes-apres/ux03-responsabilites.html) — [PNG bureau](../visuels/maquettes-apres/ux03-responsabilites-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux03-responsabilites-mobile.png).
- [ux03-creation](../visuels/maquettes-apres/ux03-creation.html) — [PNG bureau](../visuels/maquettes-apres/ux03-creation-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux03-creation-mobile.png).

**Risques et dépendances.** R03, R04. Conserver les propriétaires distincts et vérifier les permissions. Aucune copie silencieuse du responsable. L’affectation réelle et la compréhension des trois rôles restent à tester. L’extrait de création ne remplace pas le formulaire complet. Voir le [registre](risques-non-resolus.md).

**Preuves attendues avant mise en usage, proposées et non acquises :**

1. Création et récapitulatif distinguent les trois responsabilités ; aucun libellé isolé Responsable ne laisse son périmètre indéterminé.
2. Créer un dossier attribué sur prospect non attribué conserve ce choix et l'explique ; deux responsables différents restent possibles.
3. Lors d'une affectation, le récapitulatif indique quels objets changent et lesquels conservent leur responsable.

<a id="ux04"></a>

## UX04 — Expliciter le rattachement de la prochaine action

- **Parcours :** Planifier une tâche, relancer, suivre un dossier.
- **Priorité / effort :** P1 / M ; confiance : Élevée sur l'état observé ; moyenne sur la solution.
- **Vote simulé :** 12 POUR, 0 CONTRE, 0 ABSTENTION ; orientation adoptée au seuil de 7/12.
- **Préférence visuelle simulée :** 11 APRÈS, 0 AVANT, 1 RÉSERVE.
- **Décision utilisateur :** EN ATTENTE DE DÉCISION.

**Problème.** Après création d'une action de prospect, son dossier reste Sans prochaine action.

**Preuves.** OBSERVÉ O08–O09 ; risque d'incompréhension DÉDUIT, pas preuve de perte d'action. Voir les [observations](../observations/observations-factuelles.md) et la [couverture du pilotage](../observations/couverture-pilotage-commercial.md).

**Conséquence utilisateur possible.** Une alerte pourrait être ignorée comme un faux positif ou provoquer une tâche en doublon.

**Orientation proposée.** Afficher le périmètre de chaque action et permettre de choisir explicitement un dossier pertinent quand le parcours le permet ; depuis le dossier, garder son contexte. Expliquer pourquoi une alerte persiste.

**Bénéfice attendu.** Des prochaines actions interprétables au bon niveau.

**Capture AVANT :** [ouvrir la capture réelle](../visuels/captures-avant/14-fiche-avec-action-bureau.png). La zone Prochaine action concerne le prospect ; l’alerte Sans prochaine action reste visible dans la ligne du dossier. Aucun rattachement de tâche n’a été perdu.

Capture complémentaire : [13-planifier-action-bureau.png](../visuels/captures-avant/13-planifier-action-bureau.png).

**Maquettes APRÈS :** [comparaison côte à côte / bascule mobile](../visuels/comparatif-avant-apres.html#ux04). Données fictives ; les images ne prouvent pas le fonctionnement du CRM.

- [ux04-action](../visuels/maquettes-apres/ux04-action.html) — [PNG bureau](../visuels/maquettes-apres/ux04-action-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux04-action-mobile.png).
- [ux04-suivi](../visuels/maquettes-apres/ux04-suivi.html) — [PNG bureau](../visuels/maquettes-apres/ux04-suivi-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux04-suivi-mobile.png).

**Risques et dépendances.** R03, R04, R05. Vérifier les associations prospect/dossier/action du domaine et des API avant de modifier le parcours. Dépend des libellés de UX03 ; aucune couverture automatique de tous les dossiers. Une réserve simulée subsiste sur la longueur. Voir le [registre](risques-non-resolus.md).

**Preuves attendues avant mise en usage, proposées et non acquises :**

1. Une action du prospect reste distincte d'une action de dossier ; aucun rattachement automatique ambigu.
2. Sur un prospect à deux dossiers, chaque création affiche son contexte avant confirmation ; la fiche et les listes montrent le même rattachement.
3. Le dossier sans tâche garde son alerte avec une explication, même si le prospect a une autre action ; action et rappel restent deux dates distinctes.

<a id="ux05"></a>

## UX05 — Rendre vérifiable la continuité du rendez-vous jusqu'à la prochaine étape

- **Parcours :** Réserver, retrouver, préparer, modifier, réaliser, relancer.
- **Priorité / effort :** P1 / M ; confiance : Faible sur le manque ; élevée sur la nécessité de recette.
- **Vote simulé :** 12 POUR, 0 CONTRE, 0 ABSTENTION ; orientation adoptée au seuil de 7/12.
- **Préférence visuelle simulée :** 10 APRÈS, 0 AVANT, 2 RÉSERVE.
- **Décision utilisateur :** EN ATTENTE DE DÉCISION.

**Problème.** La réservation est prouvée, mais sa continuité dans l'agenda et après le rendez-vous n'est pas démontrée.

**Preuves.** OBSERVÉ O11–O12 ; code de modification/compte rendu présent ; UI non vérifiée, voir limitations.md. Voir les [observations](../observations/observations-factuelles.md) et la [couverture du pilotage](../observations/couverture-pilotage-commercial.md).

**Conséquence utilisateur possible.** La confiance dans le suivi de bout en bout reste insuffisante pour un déploiement autonome.

**Orientation proposée.** Partir des commandes existantes ; garantir un accès explicite au rendez-vous confirmé et au bon jour d'agenda, puis préparation, compte rendu et proposition de prochaine action. Ajouter seulement les raccords absents après recette.

**Bénéfice attendu.** Retrouver et poursuivre un rendez-vous sans recherche ni ressaisie inutile.

**Capture AVANT :** [ouvrir la capture réelle](../visuels/captures-avant/04-agenda-bureau.png). Agenda de la semaine du 16 au 22 novembre : un RDV annulé préexistant est affiché. Le nouveau RDV réservé pour le 26 novembre n’a pas été retrouvé pendant la recette interrompue. Aucune disparition n’est démontrée.

Capture complémentaire : [15-creation-rendez-vous-bureau.png](../visuels/captures-avant/15-creation-rendez-vous-bureau.png).

**Maquettes APRÈS :** [comparaison côte à côte / bascule mobile](../visuels/comparatif-avant-apres.html#ux05). Données fictives ; les images ne prouvent pas le fonctionnement du CRM.

- [ux05-confirmation](../visuels/maquettes-apres/ux05-confirmation.html) — [PNG bureau](../visuels/maquettes-apres/ux05-confirmation-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux05-confirmation-mobile.png).
- [ux05-agenda](../visuels/maquettes-apres/ux05-agenda.html) — [PNG bureau](../visuels/maquettes-apres/ux05-agenda-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux05-agenda-mobile.png).
- [ux05-compte-rendu](../visuels/maquettes-apres/ux05-compte-rendu.html) — [PNG bureau](../visuels/maquettes-apres/ux05-compte-rendu-bureau.png), [PNG mobile](../visuels/maquettes-apres/ux05-compte-rendu-mobile.png).

**Risques et dépendances.** R04, R05, R06. Réutiliser les commandes existantes après recette. Vérifier disponibilités, permissions, historique, préférences et réception des rappels. Pas de tâche silencieuse ni de message externe implicite. Le compte rendu montre deux états successifs, pas un écran unique imposé ; deux réserves simulées subsistent. Voir le [registre](risques-non-resolus.md).

**Preuves attendues avant mise en usage, proposées et non acquises :**

1. La confirmation mène au rendez-vous enregistré et à sa période d'agenda, avec prospect, responsable, horaires et statut cohérents.
2. Modifier, reporter et annuler un RDV fictif préservent le contexte, contrôlent les disponibilités et laissent une trace ; refus conserve les saisies.
3. Réaliser exige le compte rendu prévu par le domaine et propose une prochaine action ou une absence motivée ; aucune tâche n'est créée silencieusement.
4. Le rappel interne et l'absence de message au prospect sont explicites ; réception et préférences sont vérifiées sur comptes de test.
