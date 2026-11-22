# Cinq orientations UX à décider

18 novembre 2026. Toutes sont **P1**, adoptées par le workshop simulé avec au moins sept voix sur douze. Aucun P0 produit établi. A1/G1, classées P2, ne sont pas soumises dans ce lot. **Suite : les cinq orientations ont été validées par l'utilisateur pour E80 le 18 novembre ; voir le registre.** Les fiches ci-dessous conservent leurs questions et hypothèses telles qu'elles ont été présentées avant la réponse.

[Registre à compléter après votre réponse](decisions.md) · [Galerie complète](../visuels/comparatif-avant-apres.html) · [Risques ouverts, indépendants des votes](risques-ouverts.md).

Les votes sont indiqués dans l’ordre **pour / contre / abstention**, sur douze rôles fictifs. Les bénéfices sont des hypothèses. Effort relatif : **M** = parcours ou composant ; **L** = plusieurs états ou couches, investigation comprise. Aucun délai de développement estimé ou engagé. Les images APRÈS sont des maquettes isolées, pas des captures du produit modifié.

## B1 — Comprendre le scan et son résultat

- **Mission :** M2, validation des participations.
- **Problème :** **OBSERVÉ O04**, le rejet d’un QR invalide parle de « pack » et n’explique pas le prochain geste. **DÉDUIT C02**, confirmation, doublon et reçu existent dans le code ; leur fonctionnement réel reste à éprouver.
- **Conséquence commerçant :** hésiter sur le QR à demander ou sur l’enregistrement du passage, notamment devant une file de clients.
- **Priorité / vote / effort :** **P1 · 11 / 1 / 0 · M**. [Vote B1](../workshop/votes-et-arbitrages.md#b1). Patrick conserve son opposition au coût de la confirmation.
- **AVANT réel :** [erreur locale « pack »](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png).
- **APRÈS proposé :** [erreur avec reprise](../visuels/maquettes-apres/b1-erreur-mobile.png), [confirmation](../visuels/maquettes-apres/b1-confirmation-mobile.png), [doublon](../visuels/maquettes-apres/b1-doublon-mobile.png), [résultat toujours inconnu](../visuels/maquettes-apres/b1-toujours-inconnu-mobile.png). [Les huit états et formats](../visuels/comparatif-avant-apres.html#B1).
- **Bénéfice attendu :** comprendre le résultat et choisir le geste suivant, en distinguant QR reconnu et validation confirmée.
- **Risques / dépendances :** R01/R02/R05 ; QR de test autorisés et téléphones physiques ; reçu identifiable et état serveur ; annonces accessibles et focus. Pas de succès sans confirmation, pas de renvoi aveugle. Mesurer le coût de confirmation en caisse. L’AVANT ne montre pas les états succès/doublon/incertain.
- **Décision attendue :** VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE ; précisez les états ou conditions concernés si nécessaire.

## C1 — Distinguer information et action attendue

- **Mission :** M3, notifications et préparation.
- **Problème :** **OBSERVÉ O05**, section PIN vide avant les messages Animation ; résumé de non-lu sans tâche identifiée.
- **Conséquence commerçant :** perdre du temps à retrouver le contexte ou confondre lecture d’un message et travail terminé.
- **Priorité / vote / effort :** **P1 · 12 / 0 / 0 · M**. [Vote C1](../workshop/votes-et-arbitrages.md#c1).
- **AVANT réel :** [boîte de notifications](../visuels/captures-avant/09-notifications-generales-mobile.png).
- **APRÈS proposé :** [information reçue](../visuels/maquettes-apres/c1-notifications-mobile.png), [action attendue malgré lecture](../visuels/maquettes-apres/c1-action-mobile.png). [Comparatif et ordinateur](../visuels/comparatif-avant-apres.html#C1).
- **Bénéfice attendu :** identifier les actions encore utiles et y accéder directement, sans perdre l’historique ni la fonction PIN.
- **Risques / dépendances :** R07/R05 ; disponibilité d’un état d’action fiable et actuel, liens autorisés après contrôle de session. Aucun devoir inventé depuis un message non lu. Lire ne termine pas la préparation. Le cas de tâche est fictif ; aucune réception push/email n’a été prouvée.
- **Décision attendue :** VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE, avec commentaire éventuel.

## D1 — Clarifier dates, état et prochaine préparation

- **Missions :** M3 et M4, préparation, kit et logistique ; accueil utilisé comme point d’entrée.
- **Problème :** **OBSERVÉ O03/O07**, deux animations en cours à l’accueil contre trois dans la liste, dont une période passée ; plusieurs états de préparation à distinguer.
- **Conséquence commerçant :** douter de la période, ne pas savoir qui doit agir ou solliciter l’organisateur pour interpréter l’état.
- **Priorité / vote / effort :** **P1 · 9 / 0 / 3 · L**. [Vote D1](../workshop/votes-et-arbitrages.md#d1). UX, accessibilité et Martine craignent la surcharge de statuts.
- **AVANT réel :** [accueil](../visuels/captures-avant/03-accueil-pro-mobile.png), [liste et compteur divergent](../visuels/captures-avant/05-animations-mobile.png), [préparation prête](../visuels/captures-avant/16-preparation-vitrines-mobile.png).
- **APRÈS proposé :** [accueil](../visuels/maquettes-apres/d1-accueil-mobile.png), [incomplet](../visuels/maquettes-apres/d1-incomplet-mobile.png), [attente organisateur](../visuels/maquettes-apres/d1-attente-mobile.png), [prêt](../visuels/maquettes-apres/d1-pret-mobile.png). [Comparatif et ordinateur](../visuels/comparatif-avant-apres.html#D1).
- **Bénéfice attendu :** voir une prochaine action et son responsable, avec détails accessibles et scanner conservé en premier.
- **Risques / dépendances :** R03/R05 ; diagnostic du périmètre et de la source des compteurs avant correction. Les valeurs proposées restent illustratives. Aucune nouvelle règle de période, échéance ou fusion des états ; règles métier au backend. Cas incomplet/attente non observés sur le compte. Vérifier la compréhension des états et les transitions en heure de Paris.
- **Décision attendue :** VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE, avec réserves éventuelles sur la hiérarchie.

## E1 — Rendre le kit utilisable en boutique

- **Mission :** M4, kit d’animation et logistique.
- **Problème :** **OBSERVÉ O08**, dates ISO UTC dans le guide et consignes éloignées du téléchargement. Le contenu du PDF reste non vérifié.
- **Conséquence commerçant :** mal interpréter la fin de période, confondre les QR ou assimiler téléchargement et préparation terminée.
- **Priorité / vote / effort :** **P1 · 12 / 0 / 0 · M**. [Vote E1](../workshop/votes-et-arbitrages.md#e1).
- **AVANT réel :** [guide ouvert](../visuels/captures-avant/21-guide-preparation-mobile.png).
- **APRÈS proposé :** [kit mobile](../visuels/maquettes-apres/e1-kit-mobile.png), [kit ordinateur](../visuels/maquettes-apres/e1-kit-desktop.png). [Comparatif](../visuels/comparatif-avant-apres.html#E1).
- **Bénéfice attendu :** relier le flyer à l’impression, l’affichage, le test du QR et la préparation de l’équipe ; distinguer inscription et validation ; lire directement la fin à minuit.
- **Risques / dépendances :** R04/R03 ; vérifier le fichier réel et ses effets de préparation serveur avant de promettre son contenu. Un seul flyer cité par le guide est représenté. Conversion des instants en heure de Paris sans modifier la borne métier. Téléchargement distinct de « Je suis prêt », toujours explicite et autorisé. Impression et QR non éprouvés.
- **Décision attendue :** VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE, avec conditions éventuelles sur le kit et les dates.

## F1 — Retrouver le contexte après interruption ou absence

- **Missions :** M1 à M4, continuité de prise en main, validation, notifications et préparation.
- **Problème :** **OBSERVÉ O09**, seul un rechargement immédiat est testé ; expiration, perte de réponse et retour après plusieurs semaines restent inconnus. **DÉDUIT C05**, actualisation au retour de visibilité déjà présente.
- **Conséquence commerçant :** **HYPOTHÈSE**, recommencer une action, manquer une échéance ou ne plus savoir si une confirmation a été envoyée.
- **Priorité / vote / effort :** **P1 · 12 / 0 / 0 · L**. [Vote F1](../workshop/votes-et-arbitrages.md#f1).
- **AVANT réel :** [rechargement immédiat du scanner](../visuels/captures-avant/20-retour-rechargement-mobile.png).
- **APRÈS proposé :** [retour](../visuels/maquettes-apres/f1-retour-mobile.png), [session expirée](../visuels/maquettes-apres/f1-session-mobile.png), [interruption avant confirmation](../visuels/maquettes-apres/f1-interruption-mobile.png). [Comparatif et ordinateur](../visuels/comparatif-avant-apres.html#F1).
- **Bénéfice attendu :** reprendre au bon contexte et retrouver la tâche encore valable, sans supposer l’enregistrement d’une validation.
- **Risques / dépendances :** R02/R01/R07 ; vérifier les capacités existantes avant ajout. Après reconnexion, relire droits et état serveur ; aucune mutation rejouée automatiquement, aucun succès local, aucun QR/jeton dans l’URL. B1 porte le résultat de transaction, F1 la continuité de session et de navigation. Comparaison réelle après absence toujours à réaliser.
- **Décision attendue :** VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE, avec conditions éventuelles de reprise.

## Portée de la décision

La recommandation « GO SOUS CONDITIONS » du rapport demeure une conclusion du workshop simulé. Elle ne préjuge pas de votre décision. Les [risques ouverts](risques-ouverts.md) restent visibles même si une orientation est refusée ou reportée. Les conditions que vous exprimerez seront consignées séparément des prérequis proposés dans le dossier.
