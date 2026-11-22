# Dossier de décision — UX Marketplace Localeo

18 novembre 2026 · [galerie AVANT / APRÈS](../visuels/comparatif-avant-apres.html) · [backlog UX](../workshop/backlog-ux.md) · [votes](../workshop/votes-et-arbitrages.md). Les votes sont ceux de **douze rôles simulés** ; aucune orientation n'est validée par le propriétaire du produit à ce stade. Les conséquences utilisateur ci-dessous sont des **hypothèses**, pas des résultats de tests. Pour chacun des sept choix, renseigner ensuite [decisions.md](decisions.md) avec **VALIDÉE**, **REFUSÉE**, **À RÉVISER** ou **REPORTÉE**, commentaire et conditions éventuelles.

## O-08 — Recette contrôlée de la frontière Stripe

- **Parcours :** F, achat et confiance. **Priorité :** P0, porte de validation du lancement ; aucune panne de paiement n'est constatée. **Vote simulé :** 12/12.
- **Problème :** le bouton final n'a pas été activé car l'initialisation crée un achat et une session avant redirection. La page Stripe et le retour sont inconnus. **Conséquence possible :** un acheteur pourrait être bloqué ou ignorer l'état de sa commande si la transition échoue.
- **AVANT :** [fiche et bouton final réels, 390 px](../visuels/captures-avant/coffret-390.png) ; [mécanisme déduit du code](../observations/parcours-achat-stripe.md). **APRÈS :** [carte de recette](../visuels/maquettes-apres/O-08.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-08). La carte **n'est pas** une nouvelle interface ni une capture Stripe.
- **Bénéfice attendu :** une décision d'ouverture étayée par des preuves du parcours complet. **Effort :** M.
- **Risques et dépendances :** environnement et données de test autorisés ; innocuité des effets métier établie **avant** toute requête ; contrôle du retour succès/échec, de l'idempotence et de l'état de commande ; aucun paiement ou donnée bancaire réelle dans ce dossier. Une validation de l'orientation n'autoriserait pas à elle seule un achat.

## O-02 — Garantie et exemples sur la fiche coffret

- **Parcours :** D/F, choix du coffret et confiance. **Priorité :** P1. **Vote simulé :** 12/12.
- **Problème :** la promesse garantie, les expériences indicatives et la réservation sont espacées dans une longue fiche. **Conséquence possible :** attente erronée sur ce qui est dû pour 59,90 €.
- **AVANT :** [fiche réelle](../visuels/captures-avant/coffret-390.png). **APRÈS :** [maquette](../visuels/maquettes-apres/O-02.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-02).
- **Bénéfice attendu :** distinction nette entre droit acquis, exemples et modalités avant la décision. **Effort :** M.
- **Risques et dépendances :** formulation à confronter à la promesse canonique du coffret, aux CGV et aux prestations effectivement tenues par les commerçants ; ne pas transformer un exemple en garantie.

## O-01 — Proposition de valeur mobile

- **Parcours :** A/G, première impression. **Priorité :** P1. **Vote simulé :** 11/12.
- **Problème :** la première phrase mobile n'explicite pas les commerçants et le parcours multi-prestations comme le fait davantage l'ordinateur. **Conséquence possible :** confusion avec un colis ou une carte cadeau générique, départ prématuré.
- **AVANT :** [accueil réel 390 px](../visuels/captures-avant/accueil-standard.png). **APRÈS :** [maquette](../visuels/maquettes-apres/O-01.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-01).
- **Bénéfice attendu :** comprendre que le coffret fait vivre plusieurs moments chez des commerçants locaux et peut s'offrir. **Effort :** S.
- **Risques et dépendances :** titre plus long à éprouver à 320 px et en dix secondes ; conserver recherche, accès aux coffrets et accès distinct aux animations ; validation éditoriale de la phrase.

## O-03 — Parcours du cadeau avant le formulaire

- **Parcours :** D/F, achat cadeau. **Priorité :** P1. **Vote simulé :** 10/12.
- **Problème :** la fiche mentionne e-mail, téléphone, carte cadeau après paiement et activation en différents endroits. **Conséquence possible :** doute sur l'adresse à saisir et sur ce que recevra le bénéficiaire.
- **AVANT :** [formulaire réel sur la fiche](../visuels/captures-avant/coffret-390.png). **APRÈS :** [maquette](../visuels/maquettes-apres/O-03.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-03).
- **Bénéfice attendu :** séquence acheteur → réception → carte cadeau → bénéficiaire compréhensible avant achat. **Effort :** S.
- **Risques et dépendances :** vérifier dans le produit réel les destinataires, la chronologie, l'activation et l'usage du téléphone ; éviter la répétition avec O-07 ; aucun nouveau formulaire ou écran n'est proposé.

## O-05 — Qualité de la fiche commerçant

- **Parcours :** C/G, découverte des partenaires. **Priorité :** P1 **si** le contenu provisoire observé en TEST figure dans l'environnement ouvert, sinon P2 éditorial. **Vote simulé :** 9/12.
- **Problème :** des fiches TEST portent des noms et textes provisoires ; la qualité et l'exactitude des fiches de lancement ne sont pas établies. **Conséquence possible, conditionnelle :** moindre crédibilité pour visiteurs et commerçants si ces données sont publiées.
- **AVANT :** [fiche Café des Promeneurs réelle en TEST](../visuels/captures-avant/commercant-390.png) ; [constat des placeholders](../observations/observations-factuelles.md). **APRÈS :** [maquette](../visuels/maquettes-apres/O-05.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-05).
- **Bénéfice attendu :** présentation fidèle du commerce et de ses prestations, sans données provisoires publiées. **Effort :** M.
- **Risques et dépendances :** inventaire de l'environnement effectivement destiné au public, vérification avec des partenaires réels et droits d'usage des photos ; la maquette ne vaut pas validation du contenu.

## O-07 — Conditions décisives avant l'action d'achat

- **Parcours :** F, achat et réassurance. **Priorité :** P1. **Vote simulé :** 10/12.
- **Problème :** les liens CGV/confidentialité se trouvent sous le bouton et les conditions d'usage sont dispersées. **Conséquence possible :** achat avec compréhension incomplète ou hésitation au dernier geste.
- **AVANT :** [bloc d'achat réel](../visuels/captures-avant/coffret-390.png). **APRÈS :** [maquette](../visuels/maquettes-apres/O-07.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-07).
- **Bénéfice attendu :** prix total, validité, réservation et conditions consultables avant l'action finale. **Effort :** S.
- **Risques et dépendances :** cohérence juridique avec CGV, confidentialité et promesse réelle ; éviter un résumé redondant ou contradictoire avec O-02/O-03 ; la maquette reste dans la fiche existante.

## O-06 — Passage explicite à Localeo Live

- **Parcours :** E/G, animations. **Priorité :** P1. **Vote simulé :** 8/12.
- **Problème :** la consultation des animations passe vers un autre domaine et un autre en-tête sans destination nommée dans chaque action. **Conséquence possible :** perte de repère ou confusion entre voir le détail et s'inscrire.
- **AVANT :** [liste réelle Marketplace](../visuels/captures-avant/animations-390.png), [agenda Live](../visuels/captures-avant/agenda-commune-390.png) et [détail](../visuels/captures-avant/animation-detail-390.png). **APRÈS :** [maquette](../visuels/maquettes-apres/O-06.html) et [comparatif](../visuels/comparatif-avant-apres.html#O-06).
- **Bénéfice attendu :** le visiteur sait que le détail et la participation se poursuivent sur Localeo Live, avec sa commune conservée. **Effort :** M.
- **Risques et dépendances :** liens de retour et filtre communal à vérifier dans les deux applications ; libellés à aligner sur les actions effectivement disponibles ; l'inscription n'a pas été testée.

## Risques critiques et inconnues non résolus

1. **Paiement de bout en bout inconnu — O-08.** L'appel d'initialisation a des effets métier ; aucune session Stripe, commande de test ni page de retour n'ont été déclenchées. C'est une **lacune de preuve**, non une panne affirmée. [Analyse](../observations/parcours-achat-stripe.md).
2. **Portée contractuelle de l'offre — O-02/O-03/O-07.** Les maquettes rapprochent promesse, exemples, cadeau et conditions, mais les textes doivent être vérifiés contre le comportement réel, la promesse canonique et les CGV avant publication. Une mauvaise formulation pourrait créer une attente erronée. [Revue](../workshop/arbitrages-maquettes.md).
3. **Contenus de lancement inconnus — O-05.** Les placeholders sont **observés en TEST seulement** ; l'environnement de lancement n'a pas été contrôlé. La priorité P1 de ce point reste conditionnelle. [Observation](../observations/observations-factuelles.md).
4. **Accessibilité et erreurs non auditées.** Aucun audit complet clavier/lecteur d'écran/contraste, aucun état vide ou erreur réseau systématique et aucun retour d'achat n'ont été vérifiés. Cela ne prouve pas un défaut, mais empêche une conclusion complète sur la qualité du parcours. [Limites](../observations/limitations.md).

La proposition « GO SOUS CONDITIONS » du [rapport exécutif](../workshop/rapport-executif.md) est une recommandation simulée, **pas une validation de lancement**. Aucune orientation ne passe automatiquement en mise en œuvre.
