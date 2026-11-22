# Backlog d’implémentation potentiel — non engagé

**Actualisation après décision complémentaire du 19 novembre :** seuils UX02 confirmés à **30 jours sans interaction / 60 jours sans évolution** ; pauses justifiées et dossiers clos exclus des alertes temporelles. UX01–UX05 sont spécifiées et implémentées localement : [conception et preuves dans l’EPIC 71](../../../../../docs/specifications/epic-71-crm-prospection/workshop-crm-20261118.md). Les mentions de seuils à définir et d’implémentation non engagée ci-dessous décrivent la préparation antérieure à cette demande explicite.

Préparé le **19 novembre 2026**. Source de statut : [décisions utilisateur](decisions.md). Les cinq orientations UX01–UX05 sont validées explicitement le 19 novembre ; les seuils UX02 restent à définir. Aucune implémentation, aucun devis ni calendrier n’est engagé. Les critères ci-dessous proviennent du [backlog UX](../workshop/backlog-ux.md), sans nouveau périmètre.

## Orientations VALIDÉES

UX01–UX05 validées le 19 novembre 2026, détaillées ci-dessous. Seuils UX02 à définir. Voir le [cadrage canonique E71](../../../../../docs/roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md#audit-crm-20261118).

## Orientations À RÉVISER

Aucune décision de ce type reçue. Les réserves simulées sur UX02 ne constituent pas un classement décidé par l’utilisateur.

## Orientations REPORTÉES

Aucune décision de ce type reçue.

## Orientations REFUSÉES

Aucune décision de ce type reçue. Les rejets du workshop simulé sont hors de ce registre de validation.

## Lots UX01–UX05 validés — détail et dépendances

Ordre d’étude du cadrage : clarifier UX03/UX04, vérifier l’existant pour UX02/UX05, puis consolider UX01 et les listes. Cet ordre n’autorise aucune exécution. Toute dépendance à une orientation refusée ou reportée devra être réexaminée sans l’implémenter implicitement.

### UX01 — Rendre visible un résumé quotidien et collectif

Statut : VALIDÉE le 19 novembre 2026. Priorité : P1. Effort relatif : M.

**Lot validé à spécifier :** Conserver Mes actions/Équipe, afficher un résumé compact de la portée sélectionnée (retards, actions du jour, prochains RDV) et un accès explicite aux indicateurs collectifs existants ; distinguer zéro, chargement et indisponibilité.

**Dépendances et réserves :** R01, R04, R05. Les compteurs doivent conserver la même population, période et pagination que les listes. Dépend des termes clarifiés par UX03/UX04 et des définitions de UX02 ; aucun total collectif exhaustif encore prouvé.

**Recette proposée :**

- La portée, la période et le fuseau sont visibles pour chaque total ; un zéro personnel ne qualifie jamais le portefeuille collectif.
- Chaque total ouvre la liste correspondante avec les mêmes filtres ; nombres et pagination sont cohérents sur un jeu de test contrôlé.
- L'état vide explique la portée et permet d'ouvrir l'équipe ; aucun chargement ou échec ne devient un faux zéro.

[Références visuelles et preuves](dossier-decision.md#ux01) · [maquette principale](../visuels/maquettes-apres/ux01-accueil.html).

### UX02 — Donner accès aux listes de risques du portefeuille

Statut : VALIDÉE le 19 novembre 2026. Priorité : P1. Effort relatif : L.

**Lot validé à spécifier :** Vérifier et rendre accessibles les vues existantes ; compléter seulement les manques pour non attribués, prospects sans action, dossiers sans action, sans interaction récente, sans évolution, retards et RDV à venir. Définir les populations et seuils avec le métier.

**Dépendances et réserves :** R01, R02, R04, R05. Vérifier les vues existantes avant tout complément ; définir populations, délais d’inactivité/stagnation et traitement des pauses avec le métier. Dépend de UX03/UX04 et des droits d’accès. Les exemples de la maquette ne fixent aucune règle métier. Les catégories se recoupent ; ne pas les additionner.

**Recette proposée :**

- Chaque risque précise unité (prospect ou dossier), population, horizon et seuil ; pause justifiée et dossiers clos ont un traitement explicite.
- Un jeu contrôlé couvre chaque risque, l'absence de risque et les cas de recouvrement ; total et liste concordent sur toutes les pages.
- Les filtres responsable/équipe restent visibles ; les listes qui se recoupent ne sont pas additionnées comme un total de prospects uniques.

[Références visuelles et preuves](dossier-decision.md#ux02) · [maquette principale](../visuels/maquettes-apres/ux02-risques.html).

### UX03 — Clarifier les responsables du prospect, du dossier et de l'action

Statut : VALIDÉE le 19 novembre 2026. Priorité : P1. Effort relatif : S.

**Lot validé à spécifier :** Nommer chaque rôle dans les formulaires et confirmations ; montrer le responsable du prospect et proposer son affectation explicite, sans copier silencieusement le propriétaire du dossier.

**Dépendances et réserves :** R03, R04. Conserver les propriétaires distincts et vérifier les permissions. Aucune copie silencieuse du responsable. L’affectation réelle et la compréhension des trois rôles restent à tester. L’extrait de création ne remplace pas le formulaire complet.

**Recette proposée :**

- Création et récapitulatif distinguent les trois responsabilités ; aucun libellé isolé Responsable ne laisse son périmètre indéterminé.
- Créer un dossier attribué sur prospect non attribué conserve ce choix et l'explique ; deux responsables différents restent possibles.
- Lors d'une affectation, le récapitulatif indique quels objets changent et lesquels conservent leur responsable.

[Références visuelles et preuves](dossier-decision.md#ux03) · [maquette principale](../visuels/maquettes-apres/ux03-responsabilites.html).

### UX04 — Expliciter le rattachement de la prochaine action

Statut : VALIDÉE le 19 novembre 2026. Priorité : P1. Effort relatif : M.

**Lot validé à spécifier :** Afficher le périmètre de chaque action et permettre de choisir explicitement un dossier pertinent quand le parcours le permet ; depuis le dossier, garder son contexte. Expliquer pourquoi une alerte persiste.

**Dépendances et réserves :** R03, R04, R05. Vérifier les associations prospect/dossier/action du domaine et des API avant de modifier le parcours. Dépend des libellés de UX03 ; aucune couverture automatique de tous les dossiers. Une réserve simulée subsiste sur la longueur.

**Recette proposée :**

- Une action du prospect reste distincte d'une action de dossier ; aucun rattachement automatique ambigu.
- Sur un prospect à deux dossiers, chaque création affiche son contexte avant confirmation ; la fiche et les listes montrent le même rattachement.
- Le dossier sans tâche garde son alerte avec une explication, même si le prospect a une autre action ; action et rappel restent deux dates distinctes.

[Références visuelles et preuves](dossier-decision.md#ux04) · [maquette principale](../visuels/maquettes-apres/ux04-action.html).

### UX05 — Rendre vérifiable la continuité du rendez-vous jusqu'à la prochaine étape

Statut : VALIDÉE le 19 novembre 2026. Priorité : P1. Effort relatif : M.

**Lot validé à spécifier :** Partir des commandes existantes ; garantir un accès explicite au rendez-vous confirmé et au bon jour d'agenda, puis préparation, compte rendu et proposition de prochaine action. Ajouter seulement les raccords absents après recette.

**Dépendances et réserves :** R04, R05, R06. Réutiliser les commandes existantes après recette. Vérifier disponibilités, permissions, historique, préférences et réception des rappels. Pas de tâche silencieuse ni de message externe implicite. Le compte rendu montre deux états successifs, pas un écran unique imposé ; deux réserves simulées subsistent.

**Recette proposée :**

- La confirmation mène au rendez-vous enregistré et à sa période d'agenda, avec prospect, responsable, horaires et statut cohérents.
- Modifier, reporter et annuler un RDV fictif préservent le contexte, contrôlent les disponibilités et laissent une trace ; refus conserve les saisies.
- Réaliser exige le compte rendu prévu par le domaine et propose une prochaine action ou une absence motivée ; aucune tâche n'est créée silencieusement.
- Le rappel interne et l'absence de message au prospect sont explicites ; réception et préférences sont vérifiées sur comptes de test.

[Références visuelles et preuves](dossier-decision.md#ux05) · [maquette principale](../visuels/maquettes-apres/ux05-confirmation.html).

## Impacts à cadrer lors d’une éventuelle demande d’implémentation

Le CRM/ERP consulté relève de `localeo-backend` ; aucune modification des quatre applications n’est effectuée ici. Les autres interfaces n’ont pas d’impact identifié dans ces orientations, à vérifier si un contrat partagé évolue. Les règles d’affectation, de rattachement et de rendez-vous restent portées par le domaine ; les interfaces doivent les présenter sans les redéfinir.

Avant tout lot autorisé ultérieurement : reprendre les critères d’acceptation ci-dessus, réutiliser l’existant et identifier les impacts sur contrats/consommateurs, documentation fonctionnelle et exploitation, migrations et générateur de démonstration. Aucun changement de schéma ni de contrat n’est décidé dans cette préparation ; les tests applicatifs et les éventuelles adaptations du générateur restent à déterminer selon le changement réel. Les données illustrées sont fictives.

Choix enregistrés : cinq validations, aucun refus, report ou demande de révision ; seuils UX02 à définir. README et cadrage E71 actualisés. Une validation UX ne déclenche pas une implémentation automatique.
