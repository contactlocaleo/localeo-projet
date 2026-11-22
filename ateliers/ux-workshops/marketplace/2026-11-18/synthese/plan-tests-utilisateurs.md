# Plan de tests auprès de vrais visiteurs et commerçants

Plan préparé le 18 novembre 2026. **Aucun participant réel n'a encore été recruté ni testé.** Les profils fictifs du [workshop](../workshop/compte-rendu.md) servent seulement à diversifier le recrutement. Les six scénarios ci-dessous se jouent sur la marketplace publique, sans authentification ; les maquettes statiques peuvent ensuite être montrées pour comparer la compréhension, mais leurs boutons sont inertes. Après implémentation éventuelle, rejouer les mêmes tâches sur une version de test autorisée.

## Recrutement et protocole

- Recruter des personnes **réelles** aux niveaux d'aisance numérique variés : au moins deux peu familières des achats en ligne, des habitants cherchant un cadeau local, un visiteur extérieur, une personne venue pour les animations, un utilisateur mobile habitué à comparer et deux commerçants partenaires aux habitudes numériques différentes. Ce sont des cibles de recrutement, pas un échantillon déjà obtenu.
- Alterner 320/390/430 px sur smartphone et 1440 px sur ordinateur selon l'équipement habituel des personnes. Ne pas imposer toutes les tâches à tous les profils si elles ne correspondent pas à leur intention réelle ; garder au moins un essai de chaque scénario.
- Avant chaque tâche : lire la consigne sans démonstration, laisser la personne naviguer, noter les paroles spontanées, hésitations, erreurs et retours arrière. Ne donner une aide qu'après avoir noté le point de blocage. Après la tâche, demander ce qu'elle s'attendait à voir ensuite.
- Noter séparément **réussite autonome**, **réussite avec aide**, **échec** et **non tenté** ; ne pas transformer les réactions simulées du workshop en données. La comparaison AVANT/APRÈS, si elle est faite, doit garder les mêmes questions neutres et signaler que l'APRÈS est une maquette non interactive.
- Ne soumettre aucun formulaire d'achat ou d'inscription, ne déclencher ni session Stripe ni achat. Demander un compte de test autorisé uniquement si un parcours réellement nécessaire l'exige. N'utiliser aucune donnée bancaire réelle.

## 1 — Première visite et proposition de valeur

- **Consigne neutre :** « Vous arrivez sur ce site pour la première fois. Regardez librement l'accueil. Dites-moi ce que vous pensez pouvoir y trouver, pour qui c'est utile et ce que vous feriez ensuite. »
- **À observer :** premiers éléments regardés, mots utilisés pour décrire un coffret, distinction entre expérience sur place, objet physique et carte cadeau, repérage de la recherche, des communes et des animations, temps et aide nécessaires pour choisir une première action.
- **Réussite :** sans suggestion de l'animateur, la personne comprend qu'il s'agit de moments à vivre auprès de commerçants locaux et trouve un chemin pertinent vers coffrets ou animations selon son intention. Toute interprétation de « colis » ou « simple crédit cadeau » est consignée, même si elle poursuit.
- **Orientation interrogée :** O-01. [Avant](../visuels/captures-avant/accueil-standard.png) · [après documentaire](../visuels/maquettes-apres/O-01.html).

## 2 — Découvrir une commune

- **Consigne neutre :** « Vous souhaitez découvrir ce que propose Bouliac. Montrez-moi comment vous y arriveriez et ce que vous pouvez y faire. »
- **À observer :** usage de recherche ou des liens de commune, compréhension des catégories, découverte des coffrets, adresses et animations, conservation du contexte au retour.
- **Réussite :** la personne atteint la page Bouliac, identifie au moins une offre et une autre catégorie locale sans aide, puis peut revenir à son point de départ ou retrouver la commune. Noter si les filtres perdus gênent le parcours.
- **Orientations interrogées :** O-01 et O-04 (P2 à réexaminer, pas de maquette dédiée). [Page réelle](../visuels/captures-avant/commune-390.png).

## 3 — Découvrir un commerçant et son rôle

- **Consigne neutre :** « À partir de Bouliac, choisissez un commerce qui vous intéresse. Montrez-moi ce que ce commerce propose ici et comment cela se relie à une expérience ou à un coffret. »
- **À observer :** capacité à ouvrir une fiche, compréhension de la description, photo et informations pratiques, lien vers le coffret et retour à la commune ; demander ensuite au commerçant réel si la prestation et la formulation sont fidèles.
- **Réussite :** le visiteur trouve une fiche et son coffret associé sans aide ; le commerçant interrogé peut confirmer ou corriger explicitement les éléments publiés. Une fiche seulement jolie mais inexacte ne réussit pas ce scénario.
- **Orientation interrogée :** O-05. [Avant](../visuels/captures-avant/commercant-390.png) · [après documentaire](../visuels/maquettes-apres/O-05.html).

## 4 — Comprendre et choisir un coffret

- **Consigne neutre :** « Imaginez que vous cherchez une expérience à offrir. Comparez les offres disponibles puis ouvrez celle que vous choisiriez. Expliquez ce que son prix vous donne et ce qui dépend encore des commerces. »
- **À observer :** usage des filtres et de la liste, prix retenu, distinction garantie/exemples, validité après activation, besoin de réservation, identification des adresses et raisons du choix.
- **Réussite :** la personne peut justifier un choix ou un refus en citant le prix, la promesse garantie, au moins une limite des exemples indicatifs, la validité et la réservation, sans attribuer au coffret une prestation non promise.
- **Orientations interrogées :** O-02 et O-07. [Avant](../visuels/captures-avant/coffret-390.png) · [après documentaire](../visuels/maquettes-apres/O-02.html).

## 5 — Consulter le calendrier communal

- **Consigne neutre :** « Vous cherchez une animation à venir à Bouliac. Trouvez-en une, sa date et les informations nécessaires pour décider si vous voulez y participer. Arrêtez-vous avant toute inscription. »
- **À observer :** passage Marketplace → Localeo Live, conservation de Bouliac, repérage des dates et règles, distinction entre consulter le détail et s'inscrire, capacité à revenir vers la commune.
- **Réussite :** la personne identifie une animation à venir et sa date, trouve le détail et peut dire où la participation aurait lieu, sans inscription effective. Toute perte de repère au changement de domaine est notée.
- **Orientation interrogée :** O-06. [Liste AVANT](../visuels/captures-avant/animations-390.png) · [agenda Live réel](../visuels/captures-avant/agenda-commune-390.png) · [après documentaire](../visuels/maquettes-apres/O-06.html).

## 6 — Se préparer à acheter, sans paiement

- **Consigne neutre :** « Vous envisagez d'offrir ce coffret. Parcourez les informations disponibles jusqu'au dernier bouton avant paiement, sans l'activer. Dites-moi ce que vous recevriez, ce que recevrait votre proche, le total, les conditions et ce que vous pensez qu'il se passerait ensuite. »
- **À observer :** lecture de l'e-mail et du téléphone requis, destinataire supposé, carte cadeau, activation, total, CGV/confidentialité, perception du paiement sécurisé et hésitations. **Point d'arrêt impératif : avant toute soumission du formulaire.**
- **Réussite :** la personne peut expliquer prix, destinataire, séquence cadeau, validité/réservation et prochaine étape attendue, tout en trouvant les conditions avant le bouton ; aucun appel à `POST /public/gestion-achats/paiements/initialiser` n'est envoyé.
- **Orientations interrogées :** O-03, O-07 et O-08. [Avant](../visuels/captures-avant/coffret-390.png) · [après cadeau](../visuels/maquettes-apres/O-03.html) · [après conditions](../visuels/maquettes-apres/O-07.html) · [carte de recette](../visuels/maquettes-apres/O-08.html).

## Analyse et décision après les sessions

Rassembler pour chaque scénario les faits observés, citations courtes autorisées, aides données et échecs, puis comparer aux critères sans inventer de taux. Vérifier avec les commerçants les écarts éditoriaux. Les défauts récurrents peuvent faire évoluer la [roadmap](roadmap-ux.md), mais un changement de priorité ou de maquette demande une décision explicite. La validation de la transition Stripe reste un **protocole technique distinct**, à préparer seulement après confirmation de l'innocuité des effets métier ; ce plan de tests utilisateurs s'arrête avant le bouton.
