# Inventaire visuel — étape 3

Les AVANT sont les PNG réels de l’étape 1. Les APRÈS sont des rendus de fichiers HTML documentaires, avec données fictives : **ce ne sont pas des captures du produit**. Bureau : viewport 1440 × 1000 ; mobile : 390 × 844 ; images pleine page, hauteur variable. Les hauteurs finales sont dans [le contrôle des rendus](controle-rendus.json). Aucun fichier applicatif n’est utilisé comme source modifiée.

[Ouvrir la galerie avant/après](comparatif-avant-apres.html). Sur ordinateur : deux colonnes ; sur smartphone : bascule, sélection de scène, lien vers le rendu à taille réelle. Sans JavaScript : les deux vues restent lisibles l’une après l’autre. Les images avant sont toujours celles du bureau.

## UX01 — Accueil et portée

P1 · effort M · adopté 12/12. Références : O01–O02, O16. [Backlog](../workshop/backlog-ux.md#ux01).

**AVANT.** Aujourd’hui, portée Mes actions : trois files vides ; les indicateurs partagés sont repliés en bas. Le volume collectif n’est pas visible dans cette capture.

[01-accueil-bureau.png](captures-avant/01-accueil-bureau.png)

**APRÈS.** Accueil vide de même portée, exemple équipe peuplé et trois états de chargement. Les liens de compteurs positifs atteignent les listes illustrées.

| Scène | HTML statique | PNG bureau | PNG mobile |
| --- | --- | --- | --- |
| ux01-accueil | [Ouvrir](maquettes-apres/ux01-accueil.html) | [Bureau](maquettes-apres/ux01-accueil-bureau.png) | [Mobile](maquettes-apres/ux01-accueil-mobile.png) |
| ux01-equipe | [Ouvrir](maquettes-apres/ux01-equipe.html) | [Bureau](maquettes-apres/ux01-equipe-bureau.png) | [Mobile](maquettes-apres/ux01-equipe-mobile.png) |
| ux01-etats | [Ouvrir](maquettes-apres/ux01-etats.html) | [Bureau](maquettes-apres/ux01-etats-bureau.png) | [Mobile](maquettes-apres/ux01-etats-mobile.png) |


## UX02 — Situations à suivre

P1 · effort L · adopté 8/12. Références : O09, O16 ; couverture du pilotage. [Backlog](../workshop/backlog-ux.md#ux02).

**AVANT.** Fiche de test : une prochaine action est affichée en haut, mais le dossier en bas reste sans prochaine action. Cela illustre la distinction des unités ; cette capture ne prouve pas l’absence d’une liste globale.

[14-fiche-avec-action-bureau.png](captures-avant/14-fiche-avec-action-bureau.png), [01-accueil-bureau.png](captures-avant/01-accueil-bureau.png)

**APRÈS.** Suivi des dossiers sans prochaine action, liste des prospects non attribués, catégories de risques et unités. Les délais ne sont pas préremplis ; aucune refonte Kanban.

| Scène | HTML statique | PNG bureau | PNG mobile |
| --- | --- | --- | --- |
| ux02-risques | [Ouvrir](maquettes-apres/ux02-risques.html) | [Bureau](maquettes-apres/ux02-risques-bureau.png) | [Mobile](maquettes-apres/ux02-risques-mobile.png) |
| ux02-prospects | [Ouvrir](maquettes-apres/ux02-prospects.html) | [Bureau](maquettes-apres/ux02-prospects-bureau.png) | [Mobile](maquettes-apres/ux02-prospects-mobile.png) |


## UX03 — Responsabilités explicites

P1 · effort S · adopté 12/12. Références : O04–O05, O17. [Backlog](../workshop/backlog-ux.md#ux03).

**AVANT.** Création d’un prospect avec premier dossier. Le champ Responsable est en fin de formulaire ; la fiche obtenue laisse le prospect non attribué. La confusion est une hypothèse, pas une erreur métier démontrée.

[09-creation-prospect-bureau.png](captures-avant/09-creation-prospect-bureau.png), [11-fiche-prospect-test-bureau.png](captures-avant/11-fiche-prospect-test-bureau.png)

**APRÈS.** Fiche avec rôles et récapitulatif d’affectation ; extrait ciblé des responsabilités à la création. La qualification du potentiel reste hors périmètre.

| Scène | HTML statique | PNG bureau | PNG mobile |
| --- | --- | --- | --- |
| ux03-responsabilites | [Ouvrir](maquettes-apres/ux03-responsabilites.html) | [Bureau](maquettes-apres/ux03-responsabilites-bureau.png) | [Mobile](maquettes-apres/ux03-responsabilites-mobile.png) |
| ux03-creation | [Ouvrir](maquettes-apres/ux03-creation.html) | [Bureau](maquettes-apres/ux03-creation-bureau.png) | [Mobile](maquettes-apres/ux03-creation-mobile.png) |


## UX04 — Prochaine action rattachée

P1 · effort M · adopté 12/12. Références : O08–O09. [Backlog](../workshop/backlog-ux.md#ux04).

**AVANT.** La zone Prochaine action concerne le prospect ; l’alerte Sans prochaine action reste visible dans la ligne du dossier. Aucun rattachement de tâche n’a été perdu.

[14-fiche-avec-action-bureau.png](captures-avant/14-fiche-avec-action-bureau.png), [13-planifier-action-bureau.png](captures-avant/13-planifier-action-bureau.png)

**APRÈS.** Formulaire d’action et choix prospect/dossier ; deux dossiers après enregistrement, dont l’un reste sans action avec explication.

| Scène | HTML statique | PNG bureau | PNG mobile |
| --- | --- | --- | --- |
| ux04-action | [Ouvrir](maquettes-apres/ux04-action.html) | [Bureau](maquettes-apres/ux04-action-bureau.png) | [Mobile](maquettes-apres/ux04-action-mobile.png) |
| ux04-suivi | [Ouvrir](maquettes-apres/ux04-suivi.html) | [Bureau](maquettes-apres/ux04-suivi-bureau.png) | [Mobile](maquettes-apres/ux04-suivi-mobile.png) |


## UX05 — Du rendez-vous à sa suite

P1 · effort M · adopté 12/12. Références : O11–O12 ; limites de recette. [Backlog](../workshop/backlog-ux.md#ux05).

**AVANT.** Agenda de la semaine du 16 au 22 novembre : un RDV annulé préexistant est affiché. Le nouveau RDV réservé pour le 26 novembre n’a pas été retrouvé pendant la recette interrompue. Aucune disparition n’est démontrée.

[04-agenda-bureau.png](captures-avant/04-agenda-bureau.png), [15-creation-rendez-vous-bureau.png](captures-avant/15-creation-rendez-vous-bureau.png)

**APRÈS.** Confirmation, agenda du bon jour et préparation, puis deux états du compte rendu et de sa suite. Les commandes existantes sont représentées sans recette métier.

| Scène | HTML statique | PNG bureau | PNG mobile |
| --- | --- | --- | --- |
| ux05-confirmation | [Ouvrir](maquettes-apres/ux05-confirmation.html) | [Bureau](maquettes-apres/ux05-confirmation-bureau.png) | [Mobile](maquettes-apres/ux05-confirmation-mobile.png) |
| ux05-agenda | [Ouvrir](maquettes-apres/ux05-agenda.html) | [Bureau](maquettes-apres/ux05-agenda-bureau.png) | [Mobile](maquettes-apres/ux05-agenda-mobile.png) |
| ux05-compte-rendu | [Ouvrir](maquettes-apres/ux05-compte-rendu.html) | [Bureau](maquettes-apres/ux05-compte-rendu-bureau.png) | [Mobile](maquettes-apres/ux05-compte-rendu-mobile.png) |


## Contrôles de livraison

24 rendus sans débordement horizontal détecté aux deux dimensions ; cinq comparaisons testées en bureau et mobile ; sélection des douze scènes ; bascules clavier Entrée et états aria-pressed ; correspondance des images responsive ; repli sans JavaScript. Aucun test fonctionnel du CRM exécuté. Les contrôles de contraste portent sur la palette documentaire, pas sur une conformité accessibilité du produit.

[Rapport technique de galerie](controle-galerie.json), [aperçu du comparatif bureau](controle-galerie-bureau.png), [aperçu du comparatif mobile](controle-galerie-mobile.png), [manifeste et empreintes des AVANT](manifest-maquettes.json). Ces deux aperçus sont des captures de la galerie locale, jamais des preuves de l’application.
