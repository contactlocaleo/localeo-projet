# Rapport exécutif — Localeo Live à Bouliac

**Recommandation simulée. NO GO pour une ouverture demain à 10 000 habitants.** Deux parcours publics présentent des défauts reproduits. Le Passeport est proposé dans le programme mais sa fiche renvoie 404. Le formulaire d’une tombola donne deux consignes opposées sur la visite commerçante. Le QR valide, l’inscription confirmée et le retrait d’un lot restent à éprouver. L’aperçu public affiche aussi des dates passées sous « En cours », et une lecture ultérieure a reçu HTTP 429 dans le contexte automatisé. [Observations et preuves](../observations/observations-factuelles.md)

La simulation réunit douze rôles fictifs et s’appuie sur les 34 captures publiques de l’exploration mobile et la documentation. Les visuels fournis ont éclairé les discussions sur les états personnels. Les 168 suffrages ont donné huit orientations adoptées et six rejetées. La recommandation exprime le jugement simulé sur le scénario d’ouverture. [Votes nominatifs](votes-et-arbitrages.md) · [Compte rendu](compte-rendu.md)

## Notes heuristiques sur 10

Les notes évaluent les surfaces documentées. Repères communs au 18 novembre. 1–2 indique des repères essentiels absents, 3–4 des obstacles importants, 5–6 des repères présents avec difficultés ou portée limitée, 7–8 une surface globalement claire, 9–10 une présentation particulièrement aboutie. Les notes sont des jugements documentés et ne mesurent ni taux de réussite ni satisfaction.

| Dimension | 18 nov. | 23 nov. | Argument du 23 et limite |
| --- | ---: | ---: | --- |
| Première impression | 7 | **8** | La phrase du carnet relie les trois missions aux destinations visibles sur les trois largeurs. La trouvabilité spontanée de « Découvrir » reste à mesurer. Confiance moyenne. |
| Participation | 6 | **5** | Fiches datées, formulaire et issue du QR invalide sont repérables. Le Passeport 404 et les conditions contradictoires de la tombola dégradent l’entrée publique. La confirmation et le QR positif restent hors note. Confiance moyenne sur le public. |
| Gestion des lots | 6 | **6** | L’état vide explique où apparaîtront les lots et propose une récupération. La note couvre l’accès public. Le retrait et les états réels restent non évalués. Confiance faible. |
| Calendrier | 5 | **5** | « Prochainement » est directement accessible, avec dates visibles. Les dates passées sous « En cours » et la fiche indisponible limitent la possibilité de décider. Le groupe à venir était vide. Confiance moyenne. |
| Maniabilité mobile | 7 | **7** | La navigation et le retour vers Bouliac sont démontrés. L’usage sur appareil, avec clavier virtuel et texte agrandi, reste à examiner. Confiance moyenne à faible. |
| Accessibilité | 5 | **6** | Focus de période, activation clavier du lien de récupération et contraste de ce lien mesurés. Les formulaires, erreurs et états personnels demandent une recette avec aides d’accès. Confiance faible. |

[Rapport heuristique du 18 novembre](../../2026-11-18/workshop/rapport-executif.md) · [Comparaison détaillée](../synthese/comparaison-precedent.md)

## Habitants et parcours

Chaque cellule est une attente ou une difficulté supposée par le rôle simulé.

| Habitant simulé | Découvrir | QR et inscription | Retrouver et utiliser un lot | Consulter les dates | Revenir |
| --- | --- | --- | --- | --- | --- |
| Marie, 72 ans, très peu à l’aise | Reconnaître où sont sa tombola et ses gains | Savoir s’il faut se rendre dans un commerce et ce qui est demandé | Où aller, avant quel jour, pouvoir ouvrir son code à l’avance | Comprendre « En cours » avec une date passée | Retrouver sa tombola et lire l’action suivante |
| Jean-Pierre, 64 ans, usage occasionnel | Retrouver le programme après le choix de la commune | Reconnaître l’inscription réussie après le scan | Vérifier adresse, échéance et possibilité de rouvrir le code | Utiliser une liste des prochains jours | Revenir à la liste après une fiche indisponible |
| Sophie, 46 ans, sorties en famille | Repérer les sorties du week-end | Préparer une sortie en connaissant les visites requises | Préparer ce qu’il faut présenter au comptoir | Lire la date d’emblée et décider du trajet | Reprendre la préparation vendredi |
| Thomas, 32 ans, usage expérimenté | Se rendre vite au jeu | Connaître les champs avant de s’engager et rouvrir le lien | Voir la validité et montrer le QR plus tard | Comparer les dates en liste | Retrouver l’endroit qu’il a quitté |
| Nathalie, 55 ans, peu d’appétence numérique | Aller directement à « Mes lots » | Lire les obligations clairement et pouvoir être guidée sur le QR | Lire « À retirer », le lieu et la date limite | Savoir si le déplacement vaut encore la peine | Vérifier si son lot reste disponible |
| Lucie, 21 ans, usage fréquent | Accéder aux jeux actuels et prochains en trois entrées | Retrouver le même jeu après le QR | Consulter le QR avant d’arriver | Utiliser « Prochainement » et garder la liste | Lire l’état et la prochaine action avant de choisir les rappels |

## Cinq améliorations décisives avant une ouverture à 10 000

1. **D3 · Garantir l’accès aux fiches référencées.** Vérifier la cohérence entre le programme et le détail. Une fiche devenue indisponible permet de continuer dans le contexte communal.
2. **B1 · Unifier les consignes d’inscription.** Faire confirmer la règle de la tombola et aligner fiche, règlement affiché et formulaire, avec les champs obligatoires annoncés.
3. **D1 · Clarifier les dates et le statut.** Afficher une éventuelle fin prévue dépassée à côté du statut officiel. Préserver le raccourci « Prochainement ».
4. **B3 · Éprouver le QR jusqu’au carnet.** Exécuter un scénario valide de bout en bout et corriger toute rupture vérifiée de confirmation ou de reprise.
5. **C1 · Éprouver le retrait d’un lot attribué.** Vérifier les consignes, les états et la distinction entre consultation du QR et remise.

Les cinq orientations sont P1 et adoptées. La recette E1 s’applique à leurs parcours et reste P1. Avant un nouveau jugement de lancement, vérifier les retours d’erreur et la portée de la 429 dans une recette d’exploitation adaptée. La lecture automatisée d’un programme partiel ne renseigne pas sur la capacité à servir 10 000 habitants. [Backlog et critères](backlog-ux.md) · [Limites de preuve](../observations/limitations.md)

**Décision simulée sur le scénario demandé · NO GO.** Les corrections publiques et les recettes personnelles ci-dessus sont les premières conditions de réévaluation.
