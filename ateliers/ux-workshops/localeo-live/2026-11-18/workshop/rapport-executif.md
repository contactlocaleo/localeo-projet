# Rapport exécutif — Localeo Live / Bouliac

**Recommandation : GO SOUS CONDITIONS.** La base publique est exploitable pour poursuivre la conception : trois destinations stables, animations datées, fiches, inscription et récupération visibles. L’ouverture à 10 000 habitants n’est pas validée par cette étape : la participation positive, le carnet rempli et l’utilisation d’un lot restent non testés. Si ces conditions ne sont pas levées avant demain, ce GO conditionnel ne vaut pas autorisation de lancement.

Ce workshop est une **simulation de six experts et six habitants**, réalisée le 18 novembre 2026 à partir de l’exploration Playwright de Bouliac et de ses 15 captures. Les propos, votes et appréciations ne proviennent d’aucun test habitant. Ils permettent de préparer des choix à vérifier, pas de mesurer une satisfaction, une conversion ou une capacité de charge.

## Ce que le dossier permet de conclure

Les trois missions ont des points d’entrée dans l’application. Le programme présente deux animations en cours et une à venir ; il n’est donc pas nécessaire de déduire l’absence de calendrier de l’absence d’une grille mensuelle. En revanche, les longues cartes placent l’accès aux prochaines dates après beaucoup de contenu. L’intérêt d’un affichage plus compact est une hypothèse de conception étayée par cette densité visible.

L’état vide de Mes lots explique l’absence de gain et propose une récupération. Ce constat ne renseigne pas sur un lot réellement attribué. De même, le QR invalide montre une sortie possible, sans prouver qu’un QR valide permet d’aller jusqu’à une participation confirmée.

La consultation des images nuance la couverture annoncée à l’étape 1 : **l’accueil à 430 px est un écran de chargement**, l’accueil à 390 px est une image courte, et les captures de pages longues superposent la barre fixe à une portion du contenu. Cette superposition ne démontre pas une action inaccessible après défilement. Les variantes Découvrir à 320/390/430 px sont disponibles. Voir la [qualité des preuves dans le compte rendu](compte-rendu.md).

## Notes heuristiques sur 10

Ces notes sont un jugement de conception de l’agent intégrateur, non une moyenne de votes ou un score de tests. Repères : 1–2 = repères essentiels absents sur la surface vue ; 3–4 = difficultés de présentation importantes ; 5–6 = repères présents mais lecture ou compréhension à clarifier ; 7–8 = surface observée globalement claire ; 9–10 = présentation particulièrement aboutie. Une note élevée n’étend jamais la couverture à un état non testé.

| Dimension | Note | Justification et portée | Confiance |
| --- | ---: | --- | --- |
| Première impression | 7/10 | Carnet vide, découverte et récupération explicites ; les trois missions ne sont pas réunies dans un message initial et le programme reste indirect. Accueil stabilisé à 320 px. | Moyenne |
| Participation aux animations | 6/10 | Fiche, dates et action d’inscription présentes ; longues explications avant la saisie, et QR positif/confirmation/reprise non couverts. Note de l’entrée publique seulement. | Faible |
| Gestion des lots | 6/10 | État vide compréhensible avec récupération. La note porte uniquement sur cette entrée ; l’utilisation d’un gain attribué est **non évaluée**. | Faible |
| Calendrier | 5/10 | Périodes et dates réelles visibles, accès au détail ; les longues cartes retardent le repérage des prochaines animations. Pas de pénalité pour absence de grille mensuelle. | Moyenne |
| Maniabilité mobile | 7/10 | Repères textuels et navigation récurrente ; Découvrir inspecté sur trois largeurs sans débordement signalé. Zoom, clavier virtuel et actions derrière la barre fixe à éprouver. | Moyenne à faible |
| Accessibilité | 5/10 | Textes visibles et champs nommés sont une base ; bouton de récupération QR visuellement peu contrasté à mesurer. Focus, contrastes, lecteur d’écran et redistribution non contrôlés. Note visuelle provisoire, sans conclusion de conformité. | Faible |

Aucune moyenne globale n’est calculée : elle masquerait les parcours non inspectés.

## Arbitrages

Douze orientations ont reçu chacune douze votes fictifs. **Six sont adoptées, six rejetées**, selon le seuil fixe de sept voix favorables. Le [registre nominatif](votes-et-arbitrages.md) contient les 144 bulletins et leurs arguments.

| Orientation adoptée | Pour / contre / abstention | Priorité |
| --- | --- | --- |
| A1 — Expliquer les trois missions et nommer l’accès au programme | 11 / 0 / 1 | P2 |
| B1 — Continuité de l’animation du QR à la reprise | 12 / 0 / 0 | P1, vérification préalable |
| C1 — Lot confirmé, conditions pratiques et action adaptée | 12 / 0 / 0 | P1, vérification préalable |
| D1 — Programme compact avec accès Prochainement | 11 / 0 / 1 | P1 |
| E1 — Contrôles d’accessibilité et corrections des écarts établis | 12 / 0 / 0 | P1, vérification préalable |
| F1 — Reprise personnelle par état et prochaine action | 12 / 0 / 0 | P2, complément conditionnel |

Aucun P0 n’est affirmé faute de blocage reproduit. Les votes favorables aux parcours personnels approuvent une exigence à contrôler ; ils ne prouvent pas une fonction manquante. Les [alternatives rejetées](orientations-rejetees.md), dont l’onglet Calendrier et la suppression de deux champs, restent documentées avec les arguments minoritaires.

## Matrice habitants × parcours

**Chaque cellule est une attente ou une difficulté hypothétique simulée, jamais un résultat de tâche.** L’âge ne suffit pas à déduire un besoin d’accessibilité.

| Habitant simulé | Découvrir et choisir | QR et inscription | Retrouver/utiliser un lot | Consulter les dates | Revenir |
| --- | --- | --- | --- | --- | --- |
| Marie, 72 ans | Comprendre le carnet vide et trouver la tombola | Garder le nom de la tombola et une confirmation lisible | Lire où, avant quand et quoi présenter | Chercher un mot connu pour les dates, sans petites cases imposées | Retrouver sa tombola et la suite |
| Jean-Pierre, 64 ans | Reconnaître l’animation de l’affiche | Reprendre après QR défaillant sans refaire la recherche | Vérifier la disponibilité avant de partir | Préférence pour voir le mois, à tester | Retrouver l’action après fermeture |
| Sophie, 46 ans | Choisir une sortie avec ses proches, sans présumer de filtres famille existants | Retrouver l’animation choisie après inscription | Comprendre les personnes et conditions de retrait autorisées | Accéder rapidement au week-end ou aux dates prochaines | Retrouver ce qui est confirmé |
| Thomas, 32 ans | Aller au choix sans texte introductif répété | Éviter ressaisie et perte de contexte | Date limite, lieu et action au même endroit | Comparer plusieurs animations datées | Reprendre sans se souvenir du dernier écran |
| Nathalie, 55 ans | Repérer d’abord Mes lots | Comprendre la nécessité des informations demandées | Savoir si le gain est confirmé et comment en profiter | Besoin secondaire ; pas de préférence forte | Retrouver le gain une semaine après |
| Lucie, 21 ans | Repérer prochaines animations et suivi | Continuer la même animation après un lien ou QR | Savoir si le lot est utilisable maintenant | Accès direct aux prochaines dates, grille facultative | État certain et prochaine action |

## Conditions avant une ouverture large

1. **B1/F1 :** disposer d’un QR Bouliac valide et d’une identité autorisée ; vérifier inscription confirmée, participation, interruption et reprise, récupération et états d’erreur.
2. **C1 :** inspecter des lots de test attribués, disponibles, remis, expirés/révoqués et non vérifiables ; confirmer les consignes réelles et la séparation entre consultation et remise.
3. **E1 :** contrôler les trois missions avec clavier, lecteur d’écran, zoom et petit écran ; corriger les obstacles essentiels confirmés. Le workshop ne certifie pas l’accessibilité.
4. **A1/D1 :** confronter le vocabulaire d’entrée et le programme proposé à des habitants réels, notamment pour « trouver la prochaine animation à Bouliac ». Les effets attendus des recommandations restent à mesurer.

Ces conditions sont des suites de recette, non des résultats acquis. Le volume de 10 000 habitants n’a fait l’objet d’aucune validation de charge.

## Réponse à la question des cinq améliorations pour demain

Quatre orientations adoptées constituent les priorités avant une ouverture large ; l’ordre combine risque pour une mission et densité effectivement visible. La simulation ne justifie pas d’ajouter artificiellement une cinquième amélioration indispensable.

1. **B1 — Rendre la chaîne QR → inscription → confirmation → reprise compréhensible**, en vérifiant d’abord le parcours positif et en corrigeant les ruptures constatées.
2. **C1 — Permettre de comprendre et utiliser un lot confirmé**, avec validité, lieu/modalité et action adaptée ; contrôler les états réels avant toute retouche.
3. **D1 — Rendre les prochaines animations immédiatement repérables**, dans un programme daté plus compact et relié au détail.
4. **E1 — Lever les obstacles d’accessibilité effectivement établis**, notamment dans les formulaires, messages d’erreur et reprises.

A1 reste une amélioration utile et peu coûteuse en P2, sans caractère indispensable établi. F1 reste également adoptée en P2 ; sa recette est en partie couverte par B1/C1. Ces deux orientations sont conservées au backlog sans compléter artificiellement la liste prioritaire.

La décision reste **GO SOUS CONDITIONS**, avec les limites ci-dessus. [Compte rendu](compte-rendu.md), [backlog détaillé](backlog-ux.md) et [quick wins](quick-wins.md) accompagnent ce rapport.
