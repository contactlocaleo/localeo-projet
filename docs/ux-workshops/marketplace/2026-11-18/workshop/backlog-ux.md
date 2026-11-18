# Backlog UX — orientations adoptées

Atelier sur pièces du 18 novembre 2026. **OBSERVÉ** = navigateur de l'étape 1 ; **DÉDUIT** = code consulté ; **HYPOTHÈSE** = conséquence ou réaction à vérifier. Les votes sont simulés et détaillés dans [votes-et-arbitrages.md](votes-et-arbitrages.md). Priorités proposées : P0 bloquant, P1 indispensable, P2 différable, P3 secondaire. L'effort est un ordre de grandeur, sans chiffrage technique.

## O-08 — Recetter la transition de paiement avant ouverture large

- **Visuel étape 3 :** [comparatif AVANT / carte de recette APRÈS](../visuels/comparatif-avant-apres.html#O-08) · [carte seule](../visuels/maquettes-apres/O-08.html). La carte n'est pas un écran Stripe ni une proposition d'interface.
- **Parcours :** F, achat et confiance. **Problème :** la chaîne complète après le bouton n'est pas vérifiée.
- **Preuve :** **DÉDUIT** `POST /public/gestion-achats/paiements/initialiser` crée un achat et une session avant redirection ; **OBSERVÉ** arrêt avant soumission. [Analyse](../observations/parcours-achat-stripe.md).
- **Conséquence :** **HYPOTHÈSE** une erreur à cette frontière pourrait bloquer ou laisser incertain un acheteur.
- **Solution :** préparer une recette isolée, autorisée et sans achat réel : données de test, effets métier explicitement jugés innocuits, contrôles de l'URL, du retour, de l'échec et de la reprise ; documenter les résultats avant ouverture.
- **Bénéfice :** décision de lancement fondée sur un parcours complet vérifié.
- **Acceptation :** protocole approuvé ; aucune donnée bancaire réelle ; traces d'une session TEST, du retour succès/échec et de l'état de commande ; anomalies bloquantes traitées ou ouverture reportée.
- **Effort :** M. **Priorité :** P0 comme *porte de validation*, sans panne constatée. **Confiance :** élevée sur la lacune de preuve, indéterminée sur le comportement Stripe. **Vote :** 12/12, ADOPTÉE.

## O-02 — Délimiter la promesse du coffret

- **Visuel étape 3 :** [comparatif](../visuels/comparatif-avant-apres.html#O-02) · [maquette](../visuels/maquettes-apres/O-02.html).
- **Parcours :** D/F. **Problème :** prix et expériences indicatives peuvent être lus comme la liste garantie.
- **Preuve :** **OBSERVÉ** sur [la fiche à 390 px](../visuels/captures-avant/coffret-390.png), promesse garantie, deux exemples et mention « prestations présentées sont indicatives » sont séparés dans une page longue. **HYPOTHÈSE** de confusion, non mesurée.
- **Conséquence :** **HYPOTHÈSE** attente erronée sur les prestations, la réservation ou la valeur du coffret.
- **Solution :** près du prix, afficher un bloc « Ce qui est garanti / exemples possibles / comment réserver », avec termes cohérents dans les sections détaillées.
- **Bénéfice :** décision d'achat fondée sur la prestation effectivement due.
- **Acceptation :** une personne peut identifier, sans parcourir les CGV, la garantie, les éléments indicatifs, la validité et le besoin de réservation ; les libellés n'ajoutent aucune promesse nouvelle au contrat.
- **Effort :** M. **Priorité :** P1. **Confiance :** moyenne, car ambiguïté visuelle observée mais effet utilisateur non testé. **Vote :** 12/12, ADOPTÉE.

## O-01 — Clarifier le concept dès l'arrivée mobile

- **Visuel étape 3 :** [comparatif](../visuels/comparatif-avant-apres.html#O-01) · [maquette](../visuels/maquettes-apres/O-01.html).
- **Parcours :** A/G. **Problème :** le premier écran mobile dit « moments à vivre sur place » et « coffret à recevoir par e-mail » sans nommer les commerçants ni le parcours multi-prestations.
- **Preuve :** **OBSERVÉ** écart de formulation mobile/ordinateur dans [les captures d'accueil](../visuels/captures-avant/accueil-standard.png). **HYPOTHÈSE** de compréhension plus lente sur mobile.
- **Conséquence :** **HYPOTHÈSE** le visiteur assimile le coffret à un colis ou une carte cadeau générique, ou quitte l'accueil.
- **Solution :** formuler en une phrase le parcours d'expériences locales auprès de plusieurs commerçants, puis l'option cadeau numérique ; conserver une action principale vers les coffrets et un accès distinct aux animations.
- **Bénéfice :** première décision d'exploration plus juste.
- **Acceptation :** à 320, 390 et 430 px, la phrase essentielle et l'action principale sont visibles sans ambiguïté ; test qualitatif à faire reformuler ce qu'est un coffret et où il se vit.
- **Effort :** S. **Priorité :** P1. **Confiance :** moyenne. **Vote :** 11/12, ADOPTÉE.

## O-03 — Expliquer l'envoi et l'usage du cadeau avant le bouton

- **Visuel étape 3 :** [comparatif](../visuels/comparatif-avant-apres.html#O-03) · [maquette](../visuels/maquettes-apres/O-03.html).
- **Parcours :** D/F. **Problème :** le formulaire demande e-mail et téléphone et évoque une carte cadeau préparée après paiement, sans schéma court du destinataire et de l'activation au point de décision.
- **Preuve :** **OBSERVÉ** [fiche coffret](../visuels/captures-avant/coffret-390.png) et [CGV chargées sur ordinateur](../observations/observations-factuelles.md). **HYPOTHÈSE** d'hésitation cadeau.
- **Conséquence :** **HYPOTHÈSE** Marie ou Sophie ne sait pas quel e-mail fournir ni ce que recevra le proche.
- **Solution :** résumer avant formulaire : acheteur reçoit le coffret après paiement, peut préparer la carte cadeau, bénéficiaire active/utilise selon les règles ; expliciter l'e-mail demandé et le rôle du téléphone.
- **Bénéfice :** achat-cadeau plus compréhensible et moins d'erreurs de destinataire.
- **Acceptation :** séquence, destinataire des messages et usage du téléphone sont décrits fidèlement au comportement réel ; test utilisateur capable de les restituer sans aide.
- **Effort :** S. **Priorité :** P1. **Confiance :** moyenne. **Vote :** 10/12, ADOPTÉE.

## O-05 — Vérifier la qualité des fiches commerçants à publier

- **Visuel étape 3 :** [comparatif](../visuels/comparatif-avant-apres.html#O-05) · [maquette](../visuels/maquettes-apres/O-05.html). Le texte illustratif n'est pas validé par le commerçant.
- **Parcours :** C/G. **Problème :** le catalogue TEST comprend des noms et textes provisoires ; une mise en ligne similaire affaiblirait la crédibilité des partenaires.
- **Preuve :** **OBSERVÉ** « Commercant 1 » et autres contenus de test dans le relevé, sans extrapolation à la production. [Constat](../observations/observations-factuelles.md). La [fiche Café des Promeneurs](../visuels/captures-avant/commercant-390.png) montre photo, coffret et expérience.
- **Conséquence :** **HYPOTHÈSE conditionnelle** si ces contenus sont publiés, visiteurs et commerçants pourraient douter de l'offre.
- **Solution :** contrôler l'environnement réellement ouvert, corriger les fiches provisoires présentes, valider avec les commerçants la description et les prestations promises.
- **Bénéfice :** offre crédible et fidèle aux partenaires.
- **Acceptation :** inventaire éditorial des communes, coffrets et commerces publiés ; aucun placeholder dans l'environnement de lancement ; validation d'un échantillon par des commerçants réels.
- **Effort :** M. **Priorité :** P1 si le contenu TEST se retrouve dans l'environnement d'ouverture ; sinon P2 de maintenance éditoriale. **Confiance :** élevée sur TEST, faible sur production non inspectée. **Vote :** 9/12, ADOPTÉE.

## O-07 — Placer les conditions décisives avant l'action d'achat

- **Visuel étape 3 :** [comparatif](../visuels/comparatif-avant-apres.html#O-07) · [maquette](../visuels/maquettes-apres/O-07.html).
- **Parcours :** F. **Problème :** les liens CGV et confidentialité sont sous le bouton final et les règles d'utilisation sont réparties dans la fiche.
- **Preuve :** **OBSERVÉ** [fiche coffret](../visuels/captures-avant/coffret-390.png). Aucune preuve d'abandon.
- **Conséquence :** **HYPOTHÈSE** hésitation ou achat avec compréhension incomplète des conditions.
- **Solution :** synthèse avant le bouton du prix total, de la validité, de la réservation et des liens CGV/confidentialité, sans duplication contradictoire.
- **Bénéfice :** décision plus éclairée et repère de confiance au bon moment.
- **Acceptation :** ces informations sont lisibles avant l'action finale à 390 px et 1440 px ; texte et CGV restent cohérents ; aucun texte ne prétend que la page Stripe a été vérifiée.
- **Effort :** S. **Priorité :** P1. **Confiance :** moyenne. **Vote :** 10/12, ADOPTÉE.

## O-06 — Baliser le passage Marketplace → Localeo Live

- **Visuel étape 3 :** [comparatif](../visuels/comparatif-avant-apres.html#O-06) · [maquette](../visuels/maquettes-apres/O-06.html).
- **Parcours :** E/G. **Problème :** l'agenda et les détails passent sur un autre domaine avec une autre marque d'en-tête.
- **Preuve :** **OBSERVÉ** les liens conservent Bouliac dans l'URL et [Live](../visuels/captures-avant/agenda-commune-390.png) sépare en cours/à venir. **HYPOTHÈSE** de rupture ressentie.
- **Conséquence :** **HYPOTHÈSE** un visiteur peut croire avoir quitté Localeo ou confondre détail et inscription.
- **Solution :** libeller le lien « Voir l'animation sur Localeo Live », expliquer avant le départ que la participation se fait dans Live et offrir un retour identifiable vers la commune.
- **Bénéfice :** continuité et intention de participation plus claires.
- **Acceptation :** destination et action annoncées avant clic ; filtre communal conservé ; lien de retour vérifié ; test Claire distingue consultation et inscription.
- **Effort :** M. **Priorité :** P1. **Confiance :** moyenne-faible sans test utilisateur. **Vote :** 8/12, ADOPTÉE.

## O-04 — Donner une entrée commune plus lisible dans la recherche

- **Parcours :** B/G. **Problème :** la recherche générale mêle six types de résultats et l'entrée par territoire peut être noyée.
- **Preuve :** **OBSERVÉ** 81 résultats généraux, filtre Communes (4) et Coffrets (17) lors du relevé. [Parcours](../observations/cartographie-parcours.md). Aucun échec de recherche mesuré.
- **Conséquence :** **HYPOTHÈSE** un visiteur venu pour une commune doit décoder plusieurs catégories.
- **Solution :** rendre l'entrée « Choisir une commune » plus explicite et préserver le filtre actif lors de la navigation/du retour ; éviter une refonte de recherche avant tests.
- **Bénéfice :** accès plus direct au territoire sans perdre la richesse du catalogue.
- **Acceptation :** accès communal identifiable sur mobile ; retour depuis une fiche garde la catégorie et la commune choisies ; recherche de Bouliac testée auprès de visiteurs.
- **Effort :** M. **Priorité :** P2. **Confiance :** moyenne-faible. **Vote :** 8/12, ADOPTÉE.
