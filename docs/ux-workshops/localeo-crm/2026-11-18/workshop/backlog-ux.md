# Backlog UX proposé — étape 2

**Actualisation après décision complémentaire du 19 novembre :** seuils UX02 confirmés à **30 jours sans interaction / 60 jours sans évolution** ; pauses justifiées et dossiers clos exclus des alertes temporelles. UX01–UX05 sont spécifiées et implémentées localement : [conception et preuves dans l’EPIC 71](../../../../specifications/epic-71-crm-prospection/workshop-crm-20261118.md). Les mentions de seuils à définir et d’implémentation non engagée ci-dessous décrivent la préparation antérieure à cette demande explicite.

**Workshop simulé par IA le 19 novembre 2026.** Aucun des douze participants n’est une personne interrogée. Avis, débats et votes sont des simulations de points de vue ; ils ne constituent ni une étude utilisateur, ni une validation du produit, ni une mesure statistique.

Les O01–O18 renvoient aux [observations factuelles](../observations/observations-factuelles.md). Voir aussi la [couverture](../observations/couverture-pilotage-commercial.md), les [20 parcours](../observations/cartographie-parcours.md), les [captures](../observations/inventaire-ecrans.md) et les [limitations](../observations/limitations.md).

Les orientations v1 ont été figées après les avis initiaux, puis confrontées et votées. Le vote porte sur la solution, sa priorité et ses réserves. Une adoption autorise ici une orientation de conception uniquement : aucune implémentation, modification métier ou livraison. Les critères ci-dessous sont proposés, pas des résultats de tests. Efforts relatifs S/M/L/XL, sans devis technique ; confiance qualitative dans la preuve et dans la pertinence de la réponse. Aucun P0 démontré. Les capacités déjà présentes doivent être réutilisées.

<a id="ux01"></a>

## UX01 — Rendre visible un résumé quotidien et collectif

**Références visuelles — étape 3.** [Comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#ux01) · [scènes, captures et preuves](../visuels/inventaire-maquettes.md) · [revue et arbitrages complémentaires](../visuels/arbitrages-complementaires.md). Maquettes statiques uniquement ; vote et priorité inchangés. Validation utilisateur reçue le 19 novembre 2026 pour UX01–UX05 ; seuils UX02 à définir, voir le [registre](../validation/decisions.md).

- Atelier / parcours : A — Accueil, priorités, suivi collectif.
- Priorité / effort : **P1 / M**.
- Confiance : Moyenne.
- Vote simulé : **ADOPTÉE — 12 pour, 0 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** L'accueil personnel vide et les indicateurs collectifs repliés ne donnent pas immédiatement l'état du portefeuille.

**Preuve ou hypothèse.** OBSERVÉ O01–O02 ; DÉDUIT O16. Compréhension réelle : HYPOTHÈSE. Captures : [01](../visuels/captures-avant/01-accueil-bureau.png), [04](../visuels/captures-avant/04-agenda-bureau.png), [05](../visuels/captures-avant/05-rappels-bureau.png).

**Conséquence possible.** Un nouvel utilisateur pourrait confondre aucune action personnelle et aucune activité collective.

**Solution proposée.** Conserver Mes actions/Équipe, afficher un résumé compact de la portée sélectionnée (retards, actions du jour, prochains RDV) et un accès explicite aux indicateurs collectifs existants ; distinguer zéro, chargement et indisponibilité.

**Bénéfice attendu.** Démarrer la journée avec des priorités et une portée compréhensibles.

**Critères d’acceptation proposés :**

1. La portée, la période et le fuseau sont visibles pour chaque total ; un zéro personnel ne qualifie jamais le portefeuille collectif.
2. Chaque total ouvre la liste correspondante avec les mêmes filtres ; nombres et pagination sont cohérents sur un jeu de test contrôlé.
3. L'état vide explique la portée et permet d'ouvrir l'équipe ; aucun chargement ou échec ne devient un faux zéro.

<a id="ux02"></a>

## UX02 — Donner accès aux listes de risques du portefeuille

**Références visuelles — étape 3.** [Comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#ux02) · [scènes, captures et preuves](../visuels/inventaire-maquettes.md) · [revue et arbitrages complémentaires](../visuels/arbitrages-complementaires.md). Maquettes statiques uniquement ; vote et priorité inchangés. Validation utilisateur reçue le 19 novembre 2026 pour UX01–UX05 ; seuils UX02 à définir, voir le [registre](../validation/decisions.md).

- Atelier / parcours : B — Pilotage global et filtres.
- Priorité / effort : **P1 / L**.
- Confiance : Moyenne sur le besoin ; faible sur les fonctions manquantes.
- Vote simulé : **ADOPTÉE — 8 pour, 1 contre, 3 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Le repérage global des non attribués, sans suivi récent et dossiers stagnants n'est pas établi.

**Preuve ou hypothèse.** HYPOTHÈSE de couverture insuffisante ; couverture-pilotage-commercial.md. O09, O16 ; filtre dossier sans action DÉDUIT du code. Captures : [01](../visuels/captures-avant/01-accueil-bureau.png), [11](../visuels/captures-avant/11-fiche-prospect-test-bureau.png), [14](../visuels/captures-avant/14-fiche-avec-action-bureau.png).

**Conséquence possible.** Des dossiers à risque pourraient rester hors du champ de la revue d'équipe.

**Solution proposée.** Vérifier et rendre accessibles les vues existantes ; compléter seulement les manques pour non attribués, prospects sans action, dossiers sans action, sans interaction récente, sans évolution, retards et RDV à venir. Définir les populations et seuils avec le métier.

**Bénéfice attendu.** Une revue de portefeuille vérifiable, avec des listes permettant d'agir.

**Critères d’acceptation proposés :**

1. Chaque risque précise unité (prospect ou dossier), population, horizon et seuil ; pause justifiée et dossiers clos ont un traitement explicite.
2. Un jeu contrôlé couvre chaque risque, l'absence de risque et les cas de recouvrement ; total et liste concordent sur toutes les pages.
3. Les filtres responsable/équipe restent visibles ; les listes qui se recoupent ne sont pas additionnées comme un total de prospects uniques.

<a id="ux03"></a>

## UX03 — Clarifier les responsables du prospect, du dossier et de l'action

**Références visuelles — étape 3.** [Comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#ux03) · [scènes, captures et preuves](../visuels/inventaire-maquettes.md) · [revue et arbitrages complémentaires](../visuels/arbitrages-complementaires.md). Maquettes statiques uniquement ; vote et priorité inchangés. Validation utilisateur reçue le 19 novembre 2026 pour UX01–UX05 ; seuils UX02 à définir, voir le [registre](../validation/decisions.md).

- Atelier / parcours : C — Création, qualification, affectation.
- Priorité / effort : **P1 / S**.
- Confiance : Moyenne.
- Vote simulé : **ADOPTÉE — 12 pour, 0 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Le responsable requis à la création est celui du dossier ; le prospect peut rester non attribué.

**Preuve ou hypothèse.** OBSERVÉ O04–O05 ; confusion HYPOTHÈSE O17. Captures : [09](../visuels/captures-avant/09-creation-prospect-bureau.png), [11](../visuels/captures-avant/11-fiche-prospect-test-bureau.png), [13](../visuels/captures-avant/13-planifier-action-bureau.png).

**Conséquence possible.** Une personne pourrait croire le prospect pris en charge alors que seule une opportunité l'est.

**Solution proposée.** Nommer chaque rôle dans les formulaires et confirmations ; montrer le responsable du prospect et proposer son affectation explicite, sans copier silencieusement le propriétaire du dossier.

**Bénéfice attendu.** Savoir qui suit la relation et qui porte chaque action.

**Critères d’acceptation proposés :**

1. Création et récapitulatif distinguent les trois responsabilités ; aucun libellé isolé Responsable ne laisse son périmètre indéterminé.
2. Créer un dossier attribué sur prospect non attribué conserve ce choix et l'explique ; deux responsables différents restent possibles.
3. Lors d'une affectation, le récapitulatif indique quels objets changent et lesquels conservent leur responsable.

<a id="ux04"></a>

## UX04 — Expliciter le rattachement de la prochaine action

**Références visuelles — étape 3.** [Comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#ux04) · [scènes, captures et preuves](../visuels/inventaire-maquettes.md) · [revue et arbitrages complémentaires](../visuels/arbitrages-complementaires.md). Maquettes statiques uniquement ; vote et priorité inchangés. Validation utilisateur reçue le 19 novembre 2026 pour UX01–UX05 ; seuils UX02 à définir, voir le [registre](../validation/decisions.md).

- Atelier / parcours : E — Planifier une tâche, relancer, suivre un dossier.
- Priorité / effort : **P1 / M**.
- Confiance : Élevée sur l'état observé ; moyenne sur la solution.
- Vote simulé : **ADOPTÉE — 12 pour, 0 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Après création d'une action de prospect, son dossier reste Sans prochaine action.

**Preuve ou hypothèse.** OBSERVÉ O08–O09 ; risque d'incompréhension DÉDUIT, pas preuve de perte d'action. Captures : [13](../visuels/captures-avant/13-planifier-action-bureau.png), [14](../visuels/captures-avant/14-fiche-avec-action-bureau.png).

**Conséquence possible.** Une alerte pourrait être ignorée comme un faux positif ou provoquer une tâche en doublon.

**Solution proposée.** Afficher le périmètre de chaque action et permettre de choisir explicitement un dossier pertinent quand le parcours le permet ; depuis le dossier, garder son contexte. Expliquer pourquoi une alerte persiste.

**Bénéfice attendu.** Des prochaines actions interprétables au bon niveau.

**Critères d’acceptation proposés :**

1. Une action du prospect reste distincte d'une action de dossier ; aucun rattachement automatique ambigu.
2. Sur un prospect à deux dossiers, chaque création affiche son contexte avant confirmation ; la fiche et les listes montrent le même rattachement.
3. Le dossier sans tâche garde son alerte avec une explication, même si le prospect a une autre action ; action et rappel restent deux dates distinctes.

<a id="ux05"></a>

## UX05 — Rendre vérifiable la continuité du rendez-vous jusqu'à la prochaine étape

**Références visuelles — étape 3.** [Comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#ux05) · [scènes, captures et preuves](../visuels/inventaire-maquettes.md) · [revue et arbitrages complémentaires](../visuels/arbitrages-complementaires.md). Maquettes statiques uniquement ; vote et priorité inchangés. Validation utilisateur reçue le 19 novembre 2026 pour UX01–UX05 ; seuils UX02 à définir, voir le [registre](../validation/decisions.md).

- Atelier / parcours : D — Réserver, retrouver, préparer, modifier, réaliser, relancer.
- Priorité / effort : **P1 / M**.
- Confiance : Faible sur le manque ; élevée sur la nécessité de recette.
- Vote simulé : **ADOPTÉE — 12 pour, 0 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** La réservation est prouvée, mais sa continuité dans l'agenda et après le rendez-vous n'est pas démontrée.

**Preuve ou hypothèse.** OBSERVÉ O11–O12 ; code de modification/compte rendu présent ; UI non vérifiée, voir limitations.md. Captures : [04](../visuels/captures-avant/04-agenda-bureau.png), [15](../visuels/captures-avant/15-creation-rendez-vous-bureau.png).

**Conséquence possible.** La confiance dans le suivi de bout en bout reste insuffisante pour un déploiement autonome.

**Solution proposée.** Partir des commandes existantes ; garantir un accès explicite au rendez-vous confirmé et au bon jour d'agenda, puis préparation, compte rendu et proposition de prochaine action. Ajouter seulement les raccords absents après recette.

**Bénéfice attendu.** Retrouver et poursuivre un rendez-vous sans recherche ni ressaisie inutile.

**Critères d’acceptation proposés :**

1. La confirmation mène au rendez-vous enregistré et à sa période d'agenda, avec prospect, responsable, horaires et statut cohérents.
2. Modifier, reporter et annuler un RDV fictif préservent le contexte, contrôlent les disponibilités et laissent une trace ; refus conserve les saisies.
3. Réaliser exige le compte rendu prévu par le domaine et propose une prochaine action ou une absence motivée ; aucune tâche n'est créée silencieusement.
4. Le rappel interne et l'absence de message au prospect sont explicites ; réception et préférences sont vérifiées sur comptes de test.

<a id="ux06"></a>

## UX06 — Alléger visuellement la création sans retirer les règles métier

- Atelier / parcours : C — Créer un prospect et son premier dossier.
- Priorité / effort : **P2 / M**.
- Confiance : Moyenne.
- Vote simulé : **ADOPTÉE — 9 pour, 0 contre, 3 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** La création regroupe informations de structure et premier dossier dans un long formulaire.

**Preuve ou hypothèse.** OBSERVÉ O04, capture 09 ; effort cognitif HYPOTHÈSE. Captures : [09](../visuels/captures-avant/09-creation-prospect-bureau.png), [12](../visuels/captures-avant/12-ajout-contact-bureau.png).

**Conséquence possible.** Une saisie occasionnelle peut paraître plus lourde que nécessaire.

**Solution proposée.** Regrouper le minimum requis et l'objectif du premier dossier ; rendre les compléments progressifs et annoncer ce qui sera créé. Conserver commune, propriétaire de dossier et contrôle des ressemblances.

**Bénéfice attendu.** Saisir le minimum utile sans rendre la qualification exhaustive obligatoire.

**Critères d’acceptation proposés :**

1. Nom, commune et responsable de dossier sont repérables avec leur justification ; coordonnées et qualification restent facultatives selon règles existantes.
2. Annuler un complément ou rencontrer une erreur ne perd pas les champs saisis ; résumé avant enregistrement des objets créés.
3. Un doublon plausible déclenche le rapprochement existant, avec possibilité de consulter la fiche avant de confirmer une création distincte.

<a id="ux07"></a>

## UX07 — Remplacer la valeur null dans la dernière interaction

- Atelier / parcours : G — Lire une fiche sans historique.
- Priorité / effort : **P2 / S**.
- Confiance : Élevée.
- Vote simulé : **ADOPTÉE — 12 pour, 0 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Le mot technique null apparaît sous Aucun échange consigné.

**Preuve ou hypothèse.** OBSERVÉ O18. Captures : [11](../visuels/captures-avant/11-fiche-prospect-test-bureau.png), [14](../visuels/captures-avant/14-fiche-avec-action-bureau.png).

**Conséquence possible.** L'état vide paraît défectueux et peut diminuer la confiance.

**Solution proposée.** Afficher un état vide unique et compréhensible quand aucune dernière interaction n'existe.

**Bénéfice attendu.** Une fiche lisible dès sa création.

**Critères d’acceptation proposés :**

1. Une fiche sans échange n'affiche ni null ni undefined ; elle indique Aucun échange consigné.
2. Une fiche avec échange affiche toujours sa date et son contenu utiles, sans masquer un état d'erreur distinct.

<a id="ux08"></a>

## UX08 — Faciliter le retour aux résultats filtrés

- Atelier / parcours : G — Recherche, consultation de fiche, retour à la liste.
- Priorité / effort : **P2 / M**.
- Confiance : Faible.
- Vote simulé : **ADOPTÉE — 7 pour, 1 contre, 4 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** La recherche et les filtres sont disponibles, mais leur conservation au retour et après action n'a pas été vérifiée.

**Preuve ou hypothèse.** OBSERVÉ O03 ; risque de perte de contexte HYPOTHÈSE, pas bug établi. Captures : [02](../visuels/captures-avant/02-prospects-bureau.png), [10](../visuels/captures-avant/10-recherche-prospect-bureau.png).

**Conséquence possible.** En cas de perte de contexte, les commerciaux répéteraient leur recherche.

**Solution proposée.** Recetter puis, si nécessaire, compléter la conservation des filtres, page, position et focus après consultation et actualisation locale ; indiquer les filtres actifs.

**Bénéfice attendu.** Traiter une série de prospects sans recommencer la navigation.

**Critères d’acceptation proposés :**

1. Une recherche suivie de fiche/retour restitue termes, filtres, page et focus logique.
2. L'enregistrement d'une action actualise les données concernées sans effacer le formulaire ou la navigation.
3. Réinitialiser est explicite et ne modifie pas silencieusement la portée individuelle/équipe.

<a id="ux09"></a>

## UX09 — Rendre la transmission d'un dossier explicite

- Atelier / parcours : F — Affecter, transmettre, reprendre un portefeuille.
- Priorité / effort : **P2 / M**.
- Confiance : Faible à moyenne.
- Vote simulé : **ADOPTÉE — 10 pour, 0 contre, 2 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Plusieurs responsables existent ; la propagation d'un transfert aux tâches et RDV n'a pas été observée.

**Preuve ou hypothèse.** OBSERVÉ O05, O10–O11 ; risque de transfert incomplet HYPOTHÈSE. Captures : [11](../visuels/captures-avant/11-fiche-prospect-test-bureau.png), [05](../visuels/captures-avant/05-rappels-bureau.png), [04](../visuels/captures-avant/04-agenda-bureau.png).

**Conséquence possible.** L'équipe pourrait supposer à tort que les engagements ont tous changé de responsable.

**Solution proposée.** Présenter avant/après les responsabilités concernées et les engagements restant à l'ancien titulaire ; prévoir une note de transmission facultative et une trace, sans transfert global silencieux.

**Bénéfice attendu.** Une reprise de dossier avec responsabilités explicites.

**Critères d’acceptation proposés :**

1. Le transfert distingue prospect, dossier, tâches et RDV ; aucun objet n'est réattribué sans choix explicite autorisé.
2. Après confirmation, ancien/nouveau responsables et date sont consultables par les rôles autorisés.
3. Une action future et un RDV de test encore affectés à l'ancien titulaire sont signalés ; les erreurs n'effacent pas le contexte.

<a id="ux10"></a>

## UX10 — Expliquer la qualification et les statuts au point d'usage

- Atelier / parcours : C — Qualifier, prioriser, changer l'étape.
- Priorité / effort : **P2 / S**.
- Confiance : Moyenne.
- Vote simulé : **ADOPTÉE — 10 pour, 0 contre, 2 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Potentiel, priorité, étape et Non calculé désignent des notions distinctes dont la compréhension n'est pas testée.

**Preuve ou hypothèse.** OBSERVÉ O13, O06 ; confusion HYPOTHÈSE ; règles d'étapes DÉDUITES du code. Captures : [06](../visuels/captures-avant/06-qualification-bureau.png), [11](../visuels/captures-avant/11-fiche-prospect-test-bureau.png).

**Conséquence possible.** Un prospect non calculé pourrait être pris pour un prospect sans intérêt.

**Solution proposée.** Donner un exemple court pour potentiel/étape/priorité et expliquer Non calculé ; exposer les conséquences des transitions existantes, sans nouveau score opaque.

**Bénéfice attendu.** Qualifier progressivement avec des termes compris.

**Critères d’acceptation proposés :**

1. Non calculé signifie absence de calcul, sans équivalence visuelle avec faible potentiel.
2. Un exemple distingue état du prospect, étape du dossier et priorité ; les obligations de gain/pause/réouverture sont expliquées au moment utile.
3. La qualification manquante ne bloque pas une prise de note ou une prochaine action si le domaine ne l'exige pas.

<a id="ux11"></a>

## UX11 — Bloquer toute sortie de dossier sans prochaine action datée

- Atelier / parcours : E — Clôture de consultation et suivi.
- Priorité / effort : **P2 / L**.
- Confiance : Faible.
- Vote simulé : **REJETÉE — 0 pour, 12 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Une prochaine action peut manquer sur un dossier.

**Preuve ou hypothèse.** OBSERVÉ O09 ; efficacité d'un blocage systématique HYPOTHÈSE. Captures : [14](../visuels/captures-avant/14-fiche-avec-action-bureau.png).

**Conséquence possible.** Sans contrôle, un dossier peut être oublié ; avec blocage, les utilisateurs peuvent saisir de fausses tâches.

**Solution proposée.** Rendre une prochaine action datée obligatoire à chaque sortie de dossier, y compris dossiers en pause ou clos.

**Bénéfice attendu.** Viser une couverture totale des dossiers par une échéance.

**Critères d’acceptation proposés :**

1. Aucune sortie du dossier n'est possible sans tâche datée associée, quel que soit son statut.
2. Le blocage est testé sur pause, gain et perte ; effets de tâches factices mesurés avant décision d'implémentation.

<a id="ux12"></a>

## UX12 — Attribuer automatiquement les prospects non affectés à tour de rôle

- Atelier / parcours : F — Affectation d'équipe.
- Priorité / effort : **P3 / L**.
- Confiance : Faible.
- Vote simulé : **REJETÉE — 0 pour, 10 contre, 2 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Une fiche peut rester sans responsable du prospect.

**Preuve ou hypothèse.** OBSERVÉ O05 ; pertinence d'une distribution automatique HYPOTHÈSE. Captures : [11](../visuels/captures-avant/11-fiche-prospect-test-bureau.png).

**Conséquence possible.** La file des non attribués peut s'accumuler ; une mauvaise attribution peut méconnaître les territoires.

**Solution proposée.** Répartir automatiquement tous les prospects non attribués à tour de rôle entre membres actifs, sans validation individuelle.

**Bénéfice attendu.** Réduire le travail manuel de distribution.

**Critères d’acceptation proposés :**

1. La répartition est traçable et équilibrée en nombre entre membres actifs.
2. Les effets sur territoires, absences et relations préexistantes sont explicitement évalués avant mise en production.

<a id="ux13"></a>

## UX13 — Exiger les coordonnées complètes et la qualification dès la création

- Atelier / parcours : C — Créer et qualifier.
- Priorité / effort : **P3 / M**.
- Confiance : Faible.
- Vote simulé : **REJETÉE — 0 pour, 12 contre, 0 abstention(s)**. Détail dans [votes et arbitrages](votes-et-arbitrages.md).

**Problème.** Une fiche initiale peut ne pas disposer de coordonnées ni de qualification.

**Preuve ou hypothèse.** OBSERVÉ O04, O13 ; nécessité de complétude immédiate HYPOTHÈSE. Captures : [09](../visuels/captures-avant/09-creation-prospect-bureau.png), [06](../visuels/captures-avant/06-qualification-bureau.png).

**Conséquence possible.** Des fiches peu exploitables peuvent s'accumuler ; une obligation peut empêcher de noter un nouveau prospect.

**Solution proposée.** Bloquer la création sans téléphone, e-mail, contact nommé et qualification complète.

**Bénéfice attendu.** Viser des fiches immédiatement exploitables.

**Critères d’acceptation proposés :**

1. Une création sans l'un des quatre éléments est refusée avec explication.
2. La proportion de prospects impossibles à saisir sans inventer une information est mesurée avant tout déploiement.

## Dépendances et frontières

UX03 clarifie les propriétaires ; UX04 clarifie le périmètre des actions ; UX02 doit reprendre ces définitions avant de compter les risques ; UX01 expose ensuite des agrégats cohérents. UX05 commence par une recette des commandes existantes. UX09 dépend de la définition des responsabilités et des permissions. UX08 applique la préservation du contexte demandée par les conventions de gestion, sans prétendre à une régression observée.

Le CRM est porté par le dépôt backend : domaine pour les règles, application pour l’orchestration, PWA CRM pour la présentation. Si une orientation conduit ultérieurement à changer une règle, un contrat ou une notification, la spécification et ses consommateurs devront être examinés dans la phase autorisée. Aucun contrat, migration, générateur, roadmap canonique ou code applicatif n’est modifié à cette étape ; les trois autres applications ne sont pas affectées par ces documents.
