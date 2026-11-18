# Rapport exécutif — workshop UX Marketplace Localeo

18 novembre 2026 · environnement TEST · [prompt](../prompts/02-workshop.md) · [preuves de l'étape 1](../observations/observations-factuelles.md)

## Statut de la démarche

Il s'agit d'un **atelier contradictoire sur pièces, avec douze rôles simulés** : cinq expertises et sept profils fictifs. Personne n'a été recruté ni interrogé. Les réactions, votes, notes et priorités ci-dessous sont des jugements heuristiques et des hypothèses de décision, **pas des mesures utilisateur**. Les captures et le code examinés à l'étape 1 sont les seules preuves d'observation. Le [compte rendu](compte-rendu.md) garde les désaccords ; les [votes](votes-et-arbitrages.md) sont individuels.

## Décision

**GO SOUS CONDITIONS** pour une ouverture à 10 000 visiteurs : la découverte publique est parcourable, mais l'ouverture ne devrait pas être annoncée sans une recette contrôlée de l'initialisation Stripe et du retour de paiement, une vérification éditoriale du catalogue destiné au public, et une clarification sur la fiche de ce qui est garanti, de ce qui est indicatif et du parcours du bénéficiaire. Ces conditions sont des décisions proposées par l'atelier simulé, non une certification de mise en production. L'essai Stripe n'a pas été fait : le bouton envoie une requête qui crée un achat avant la redirection ([preuve](../observations/parcours-achat-stripe.md)).

## Notes heuristiques sur 10

Ces notes comparent les écrans observés aux objectifs du workshop ; elles ne sont ni un score d'accessibilité normatif, ni un taux de conversion.

| Dimension | Note | Justification et limite |
| --- | ---: | --- |
| Première impression | 7 | Accroche, recherche et coffret vedette visibles ; le premier écran mobile n'explicite pas aussi bien les commerçants et l'idée de cadeau que l'ordinateur. [Captures](../visuels/captures-avant/accueil-standard.png). |
| Compréhension du concept de coffret | 5 | Le mode d'emploi et la fiche expliquent le parcours local, mais la promesse garantie et les expériences indicatives cohabitent ; la compréhension réelle reste à tester. [Fiche](../visuels/captures-avant/coffret-390.png). |
| Découverte des communes | 7 | Filtre Communes, page Bouliac et liens vers coffrets, adresses et agenda fonctionnent dans le relevé ; la recherche générale mélange six catégories. [Parcours](../observations/cartographie-parcours.md). |
| Visibilité des commerçants | 6 | Page dédiée, photo, expérience et coffret associés ; certaines données TEST sont des contenus provisoires et les informations pratiques méritent une vérification éditoriale. [Capture](../visuels/captures-avant/commercant-390.png). |
| Fiches coffrets | 6 | Prix, validité, partenaires et formulaire sont visibles ; la portée précise des prestations et la réservation demandent une formulation plus directe avant décision. [Capture](../visuels/captures-avant/coffret-390.png). |
| Calendrier des animations | 7 | Deux animations en cours et deux à venir pour Bouliac, dates et détails dans Live ; le changement de domaine/marque peut brouiller la continuité. [Agenda](../visuels/captures-avant/agenda-commune-390.png). |
| Parcours d'achat | 5 | Prix total et champs requis visibles sur la fiche ; le formulaire, la page Stripe et le retour de paiement n'ont pas été soumis/testés. Cette note est **provisoire**. [Frontière](../observations/parcours-achat-stripe.md). |
| Confiance et réassurance | 6 | Validité, réservation, paiement sécurisé, CGV et aide existent ; la séquence d'envoi au bénéficiaire et les conditions essentielles restent dispersées. [Observation](../observations/observations-factuelles.md). |
| Accessibilité mobile | 6 | Accueil et navigation inspectés à 320, 390 et 430 px ; autres écrans surtout à 390 px. Aucun audit clavier, lecteur d'écran ou contraste complet : note **provisoire**. [Limites](../observations/limitations.md). |

## Matrice des sept profils et parcours prioritaires

Chaque cellule indique une **question de test hypothétique**, pas une réaction mesurée. A : arrivée ; B/C : commune/commerçant ; D : coffret ; E : animations ; F : achat/cadeau.

| Profil fictif | A — Comprendre | B/C — Découvrir | D — Choisir | E — Animations | F — Acheter/offrir |
| --- | --- | --- | --- | --- | --- |
| Marie, 68 ans | Comprend-elle « coffret par e-mail » ? | Retrouve-t-elle une adresse locale ? | Distingue-t-elle exemples et droit acquis ? | Repère-t-elle la date utile ? | Sait-elle ce que recevra sa petite-fille ? |
| Sophie, 42 ans | Voit-elle l'idée de cadeau local ? | Trouve-t-elle sa commune rapidement ? | Compare-t-elle la valeur proposée ? | Trouve-t-elle une sortie proche ? | Comprend-elle les conditions de validité ? |
| Thomas, 34 ans | Sait-il que les moments se vivent sur place ? | Situe-t-il la commune et ses commerces ? | Comprend-il réservation et disponibilité ? | Identifie-t-il les dates pendant son séjour ? | Est-il rassuré sur l'usage à distance ? |
| Claire, 51 ans | Sépare-t-elle coffrets et animations ? | Rejoint-elle l'agenda de sa commune ? | Est-ce pertinent pour sa visite ? | Distingue-t-elle voir et s'inscrire ? | Aucun achat prioritaire ; teste-t-elle la continuité Live ? |
| Lucie, 25 ans | Atteint-elle vite les offres ? | Filtre-t-elle sans perdre le contexte ? | Compare-t-elle prix et contenu ? | Ouvre-t-elle un détail sans rupture ? | Le récapitulatif suffit-il avant paiement ? |
| Nadia, 46 ans | Comprend-elle la place des partenaires ? | Retrouve-t-elle sa fiche ? | Vérifie-t-elle sa prestation exacte ? | Son commerce est-il lié à l'animation ? | Voit-elle les promesses faites au client ? |
| Patrick, 58 ans | Comprend-il l'offre globale ? | Son adresse est-elle identifiable ? | La description est-elle fidèle ? | Comprend-il sa présence dans Live ? | Peut-il expliquer l'utilisation à un client ? |

## Si 10 000 visiteurs arrivent demain : cinq améliorations

1. **O-08 — Valider sans risque le passage commande → Stripe → retour**, avec environnement et données de test autorisés, avant toute ouverture large. Ce point est une condition de vérification, pas une affirmation de panne.
2. **O-02 — Rendre explicite sur chaque fiche ce qui est garanti et ce qui est seulement illustratif**, avec réservation et validité au même endroit.
3. **O-01 — Décrire dès le premier écran mobile le coffret comme un parcours d'expériences chez plusieurs commerçants, à vivre localement et à offrir par e-mail.**
4. **O-03 — Montrer avant achat qui reçoit quoi, quand, et comment le bénéficiaire utilise le coffret.**
5. **O-05 — Contrôler les fiches commerçants et les contenus de l'environnement réellement ouvert au public**, puis remplacer les contenus provisoires s'ils y sont présents.

Les orientations adoptées O-04, O-06 et O-07 restent utiles ; leur ordre dépendra de tests réels. Les points forts sont une offre locale visible, des liens commune–commerce–coffret et un agenda Live déjà parcourable. Les risques majeurs portent sur l'interprétation de l'offre, la qualité éditoriale et la partie paiement non vérifiée. Tester avec de vrais visiteurs la compréhension en dix secondes, le choix d'un coffret, le cadeau et le passage vers Live ; tester avec de vrais commerçants la fidélité des fiches et des prestations. Voir les [critères d'acceptation](backlog-ux.md) et les [limites](../observations/limitations.md).
