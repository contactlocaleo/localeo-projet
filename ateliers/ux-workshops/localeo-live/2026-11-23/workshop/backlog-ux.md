# Backlog UX — orientations adoptées par la simulation

Les estimations S/M/L/XL sont relatives au périmètre décrit. Le niveau de confiance distingue l’observation du problème, la cause et le bénéfice attendu. Le vote complet et les propositions alternatives figurent au registre. [Votes nominatifs](votes-et-arbitrages.md) · [Principes Live](../../../../../docs/produit/live/principes-ux.md)

P1 couvre une friction majeure ou un contrôle d’aptitude au lancement. P2 couvre une amélioration utile et différable. Aucun P0 n’est établi à l’échelle d’une mission entière. D3 bloque l’accès à une animation observée. Le risque de diffusion de ce défaut et la portée du HTTP 429 restent à qualifier.

| Orientation | Pour / contre / abstention | Priorité | Effort indicatif |
| --- | --- | --- | --- |
| A1 | 8 / 0 / 4 | P2 | S |
| B1 | 12 / 0 / 0 | P1 | S |
| B3 | 11 / 0 / 1 | P1 | M |
| C1 | 11 / 0 / 1 | P1 | M |
| D1 | 12 / 0 / 0 | P1 | M |
| D3 | 12 / 0 / 0 | P1 | M |
| E1 | 11 / 0 / 1 | P1 | M |
| F1 | 11 / 0 / 1 | P2 | M |

## D3 — Ouvrir une fiche annoncée et retrouver le programme

**Étape 3.** Trois planches illustrent l’indisponibilité, l’erreur temporaire et le retour au programme. [Comparatif D3](../visuels/comparatif-avant-apres.html#D3) · [Conditions de retour](../visuels/reference-maquettes.md#conditions-et-arbitrages-de-présentation)

- **Mission et preuve** · Découvrir et participer. OBSERVÉ O08. La carte Passeport était dans le programme et le service de détail a retourné HTTP 404 à l’ouverture et après réessai. La cause reste inconnue. [Carte](../visuels/captures-avant/27-programme-retabli-390.png) · [Détail 404](../visuels/captures-avant/61-passeport-detail-390.png)
- **Solution et bénéfice** · Vérifier la cohérence entre référencement public et détail. En cas d’indisponibilité confirmée, indiquer comment continuer dans le programme de la commune. Un habitant peut choisir une autre sortie sans reprendre sa recherche.
- **Critères** · Une carte éligible ouvre la fiche correspondante. Tester une fiche accessible, le retrait entre affichage et ouverture, puis une erreur temporaire. L’issue permet de retrouver commune, filtres pertinents et position ou focus utile. Une fiche retirée reste indisponible après réessai et le message permet de comprendre la suite.
- **Effort, priorité, confiance** · M pour reproduire, qualifier et traiter le parcours de retour. Réestimer si la publication est en cause. P1. Élevée sur le blocage d’une fiche, faible sur sa cause et son étendue.

## B1 — Rendre cohérentes les conditions d’inscription

**Étape 3.** Fiche et formulaire liés sur un exemple conditionnel sans visite. [Comparatif B1](../visuels/comparatif-avant-apres.html#B1) · [Formulaire](../visuels/maquettes-apres/planche.html?etat=B1-formulaire)

- **Mission et preuve** · Participer. OBSERVÉ O04. Promesse centrée sur l’e-mail, quatre champs obligatoires et deux consignes incompatibles sur la visite commerçante dans le formulaire consulté. Aucune soumission dans cette exécution. [Entrée](../visuels/captures-avant/63-tombola-inscription-action-390.png) · [Formulaire](../visuels/captures-avant/41-formulaire-tombola-email-390.png)
- **Solution et bénéfice** · Faire confirmer les conditions de cette tombola, puis aligner fiche, formulaire et règlement visible sur la règle publique de l’animation. Annoncer les informations obligatoires avant l’ouverture du formulaire. L’habitant sait ce qu’il prépare et s’il doit se déplacer.
- **Critères** · Une tombola sans visite et un scénario avec visite autorisée montrent des consignes cohérentes sur la fiche et dans le formulaire. Une règle absente ou incertaine n’accorde aucune dispense ni obligation. Les champs requis sont annoncés avant ouverture et au formulaire. Le retour retrouve la fiche.
- **Effort, priorité, confiance** · S pour le diagnostic et le périmètre de présentation de la tombola, sous réserve de la règle confirmée. P1. Élevée sur l’incohérence visible, moyenne sur l’effort et le bénéfice.

## D1 — Clarifier disponibilité et dates dans le programme

**Étape 3.** Quatre états pour le programme avec fin prévue dépassée, l’état vide, le futur fictif et la lecture partielle. [Comparatif D1](../visuels/comparatif-avant-apres.html#D1) · [Programme partiel](../visuels/maquettes-apres/planche.html?etat=D1-partiel)

- **Mission et preuve** · Consulter les dates. OBSERVÉ O02–O03. Huit des dix cartes « En cours » avaient dépassé leur fin prévue. Les fiches Juste Prix et Vitrines donnent une explication. Le raccourci « Prochainement » est vérifié aux trois largeurs. [Programme](../visuels/captures-avant/20-programme-bouliac-390.png) · [Détail](../visuels/captures-avant/23-fiche-juste-prix-390.png)
- **Solution et bénéfice** · Rendre la fin prévue et le statut officiel distinguables dès la carte. Garder le lien de période et rapprocher les dates du titre si nécessaire. L’habitant peut comparer les dates et comprendre ce que le statut indique avant de cliquer.
- **Critères** · Vérifier une animation avec fin future, une fin prévue dépassée avant clôture et une prochaine animation réelle ou équivalente dans un jeu autorisé. Le texte reste cohérent entre carte et détail et repose sur les faits publics. Le raccourci reste utilisable au clavier avec un titre de destination visible. Un état vide ou partiel garde un libellé distinct et compréhensible.
- **Effort, priorité, confiance** · M. P1. Élevée sur la coexistence du badge et des dates, moyenne sur la formulation à retenir. Le navigateur n’établit ni un droit de jouer ni la cause du statut.

## B3 — Éprouver la continuité du QR à la reprise

**Étape 3.** Cinq états illustrés de l’entrée QR au carnet, dont le refus et la soumission incertaine. Les AVANT personnels restent indisponibles. [Comparatif B3](../visuels/comparatif-avant-apres.html#B3) · [Réponse incertaine](../visuels/maquettes-apres/planche.html?etat=B3-incertain)

- **Mission et preuve** · Rejoindre et retrouver une animation. OBSERVÉ O05. Consigne QR et code du jour sur une fiche, refus récupérable sur une autre route. HYPOTHÈSE. La continuité via un QR valide, l’e-mail et le carnet peut présenter un écart. [Fiche QR](../visuels/captures-avant/31-fiche-qr-public-390.png) · [Accès refusé](../visuels/captures-avant/37-qr-refuse-focus-390.png) · [Limites](../observations/limitations.md)
- **Solution et bénéfice** · Avec une recette test autorisée, suivre chaque point d’entrée réel jusqu’au résultat et au retour. Corriger les ruptures reproduites. L’habitant reconnaît son animation, connaît le résultat de sa démarche et peut la reprendre.
- **Critères** · Vérifier QR et code valides, QR invalide ou expiré, échec récupérable, confirmation puis reprise de la même animation après interruption. Vérifier e-mail reçu et lien personnel si le scénario l’exige. Montrer la confirmation après réussite attestée. En cas d’incertitude, afficher l’état connu et une action sûre.
- **Effort, priorité, confiance** · M pour préparer et réaliser la recette. Toute correction dépend du résultat. P1. Élevée sur la lacune de preuve, faible sur l’existence d’un défaut positif.

## C1 — Vérifier le lot réel, son état et ses consignes

**Étape 3.** Sept états fictifs avec et sans action de retrait. La capture de Mes lots vide sert de contexte. [Comparatif C1](../visuels/comparatif-avant-apres.html#C1) · [À retirer](../visuels/maquettes-apres/planche.html?etat=C1-disponible)

- **Mission et preuve** · Retrouver et utiliser un lot. OBSERVÉ O06. Mes lots est vide sur carnet neuf. Les JPG fournis illustrent une carte « À retirer ». HYPOTHÈSE. La lisibilité et la fiabilité des consignes dans les états personnels restent à vérifier. [État vide](../visuels/captures-avant/34-lots-vides-390.png) · [Visuels fournis](../visuels/visuels-fournis.md)
- **Solution et bénéfice** · Vérifier sur lots autorisés l’état affiché, la validité, le lieu et l’action disponible. Corriger les écarts de présentation ou de reprise établis. L’habitant peut préparer son retrait et comprendre une indisponibilité.
- **Critères** · Couvrir lot à retirer, remis, expiré, annulé et état incertain. Vérifier les consignes renseignées, le dernier état connu, la relecture et la séparation entre consultation de l’action et remise confirmée. L’ouverture d’un code laisse le statut métier inchangé tant que la remise n’a pas été confirmée.
- **Effort, priorité, confiance** · M pour la recette des états. P1. Élevée sur la limite actuelle, faible sur un écart concret du retrait. La capture du 23 équivalente à un lot attribué manque.

## E1 — Contrôler l’accessibilité des trois missions

**Étape 3.** Trois planches illustrent l’accès refusé, la récupération prête et une erreur e-mail. [Comparatif E1](../visuels/comparatif-avant-apres.html#E1) · [Contrôles de clavier et d’agrandissement](../visuels/controle-maquettes.md)

- **Mission et preuve** · Transverse. OBSERVÉ O02 et O05. Focus de période et activation du lien QR refusé vérifiés, contraste de ce lien mesuré à 390 px. HYPOTHÈSE. Des obstacles peuvent apparaître ailleurs, notamment pendant une erreur ou une saisie. [Focus Prochainement](../visuels/captures-avant/21-prochainement-clavier-390.png) · [Focus QR](../visuels/captures-avant/37-qr-refuse-focus-390.png)
- **Solution et bénéfice** · Contrôler les chemins et corriger les obstacles reproduits. Préserver les destinations textuelles et les issues des erreurs. L’habitant peut continuer à son rythme avec clavier, agrandissement ou lecteur d’écran.
- **Critères** · Vérifier focus visible et non masqué, ordre de navigation, annonce des changements et erreurs, noms des commandes et retour au contexte sur chaque mission. À 320 px et avec texte agrandi, les consignes, erreurs et actions restent lisibles et activables. Relever contrastes et dimensions des actions essentielles sur leurs états pertinents. Vérifier sur appareil avec clavier virtuel et sur lecteur d’écran.
- **Effort, priorité, confiance** · M pour une recette ciblée. P1. Élevée sur les contrôles manquants, faible sur les éventuels défauts non mesurés.

## A1 — Préserver les repères et vérifier l’accès au programme

- **Mission et preuve** · Première visite. OBSERVÉ O01–O02. Les trois destinations sont expliquées et « Prochainement » est accessible. HYPOTHÈSE. Certains habitants pourraient chercher d’abord un mot explicite pour le programme. [Carnet 320](../visuels/captures-avant/01-carnet-320.png) · [Découvrir 390](../visuels/captures-avant/20-programme-bouliac-390.png)
- **Solution et bénéfice** · Conserver la structure actuelle et vérifier la trouvabilité du programme au moyen de tâches de première visite. Une retouche de libellé dépend d’un problème établi. Le bénéfice attendu porte sur l’orientation initiale.
- **Critères** · Demander à des habitants de trouver sans aide leurs animations, leurs lots et la prochaine animation communale. Relever chemin, hésitations et interprétation de « Découvrir ». Si un écart apparaît, comparer les libellés proposés avec la même tâche.
- **Effort, priorité, confiance** · S pour préparer et conduire la vérification ciblée. P2. Élevée sur les repères présents, faible sur la nécessité d’une retouche.

## F1 — Vérifier la prochaine action à la réouverture du carnet

- **Mission et preuve** · Suivre une participation dans le temps. OBSERVÉ O06–O07. L’accès à la récupération et le retour vers la commune existent. Les JPG montrent un carnet rempli, sans preuve du geste de réouverture. HYPOTHÈSE. L’état accepté et la prochaine action peuvent être difficiles à retrouver. [Récupération](../visuels/captures-avant/40-recuperation-stable-390.png) · [Visuels d’appoint](../visuels/visuels-fournis.md)
- **Solution et bénéfice** · Reprendre une participation existante après une interruption ordinaire, à la différence de l’arrivée QR vérifiée en B3. Confirmer l’état et la prochaine action, puis combler les écarts observés. L’habitant retrouve ce qu’il a commencé.
- **Critères** · Vérifier la réouverture avec deux participations, une action disponible, une participation achevée et un résultat encore inconnu. Les éléments sont identifiables, la prochaine action suit l’état confirmé et « Retrouver mon carnet » reste accessible.
- **Effort, priorité, confiance** · M pour la recette accompagnée. P2. Faible sur les écarts éventuels, moyenne sur la pertinence de la tâche à valider.
