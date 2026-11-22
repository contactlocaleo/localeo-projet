# Vérification des livrables visuels — étape 3

18 novembre 2026. Contrôle local en Chromium/Playwright des fichiers HTML documentaires. Ce n'est ni un test utilisateur ni une recette de l'application ou de Stripe.

- La [galerie](../visuels/comparatif-avant-apres.html) contient **sept** orientations, chacune avec une capture AVANT existante et une maquette APRÈS. Les sept images AVANT ont été décodées sans erreur par le navigateur ; aucune n'a été générée ou retouchée à cette étape.
- À 1440 px, les deux colonnes apparaissent côte à côte ; [aperçu de vérification](comparatif-desktop.png). À 390 px, les boutons AVANT / APRÈS changent le panneau visible ; [aperçu](galerie-mobile.png). Les panneaux et les fichiers après se défilent indépendamment.
- Les sept maquettes ont été ouvertes à 320, 390 et 430 px sans débordement horizontal. Chaque fichier possède un titre principal et n'inclut aucun formulaire HTML soumis. Les [aperçus statiques de contrôle](maquette-O-01.png) sont des captures de **maquettes**, pas du site réel.
- Le texte de O‑03 et O‑07 a été corrigé pendant la revue pour rester sur la fiche actuelle, sans inventer une nouvelle étape de commande. O‑06 distingue le détail de l'inscription. O‑08 représente uniquement la frontière à recetter.
- O‑01 conserve le champ de recherche de l'accueil ; l'ajustement porte sur la proposition de valeur et son contexte. Un contrôle supplémentaire à 320 px n'a montré aucun débordement horizontal ([aperçu](maquette-O-01-320.png)).
- Les boutons des maquettes sont inertes. Aucun appel réseau de commande, aucune inscription, session Stripe ni paiement n'a été lancé.

**Non vérifié :** conformité WCAG de l'application, lecture par technologies d'assistance, tests avec de vrais visiteurs/commerçants, fidélité contractuelle finale des textes, comportement de Stripe et retour de paiement. Ces points restent à traiter avant toute implémentation ou ouverture large. La [revue simulée](../workshop/arbitrages-maquettes.md) formule les questions de recherche.
