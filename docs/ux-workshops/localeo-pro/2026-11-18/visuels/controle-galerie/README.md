# Contrôles de rendu — étape 3 uniquement

18 novembre 2026. Chromium via Playwright, fichiers locaux. **Ces contrôles concernent la galerie et les maquettes ; ils ne sont pas la validation métier ou utilisateur de l’étape 4.**

- 18 états rendus à 390 px et 1440 px : 36 PNG APRÈS, sans erreur JavaScript ni débordement horizontal au rendu.
- Largeurs de contrôle : 320, 390, 768 et 1440 px. Aucun débordement horizontal sur les 18 prototypes ni sur la galerie.
- Cinq orientations présentes ; les 36 variantes d’image ont été chargées et décodées dans la galerie à chaque largeur.
- À 320/390 px : bascules Avant/Après vérifiées, activation au clavier de la bascule Après. À 768/1440 px : deux panneaux visibles côte à côte.
- Ouverture de l’accordéon du kit vérifiée. Boutons métier limités à une indication de démonstration ; aucun appel applicatif.
- Inspection visuelle principale : messages du scanner, confirmation, succès, doublon, refus, états incertains ; notifications ; accueil et préparation ; kit ; reprise et expiration. Galerie inspectée sur mobile et ordinateur.
- Contrôle documentaire des liens locaux et vérificateurs du dépôt exécutés avec succès. Aucun identifiant de connexion ajouté ; aucune nouvelle capture authentifiée.

Un premier essai automatisé a attendu sur le décodage d’une image chargée à la demande, hors écran. Il a été interrompu ; les dix images initiales de la galerie sont désormais chargées immédiatement. La nouvelle exécution est terminée sans échec. Aucune application distante n’était impliquée.

Preuves : [résultats structurés](resultats.json), [galerie ordinateur](galerie-desktop.png), [comparatif kit](galerie-kit-desktop.png), [mobile Après](galerie-mobile-apres.png), [mobile Avant](galerie-mobile-avant.png).

Les PNG de ce dossier sont des captures du **comparatif local**, jamais des captures AVANT du produit. Le haut d’une capture réelle peut contenir un espace vide ou une barre fixe déplacée par la capture longue d’origine ; aucune retouche n’a été faite pour améliorer artificiellement l’AVANT.

Non exécutés : test sur téléphone physique, lecteur d’écran, zoom navigateur à 200 %, audit complet des contrastes, recette réseau ou serveur, tests avec commerçants. Aucune conformité ni efficacité mesurée n’est revendiquée.
