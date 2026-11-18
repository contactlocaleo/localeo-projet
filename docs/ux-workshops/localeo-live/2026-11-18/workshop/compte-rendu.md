# Compte rendu — six ateliers simulés

**Statut : simulation de conception, aucun entretien ni test habitant réalisé.** Les citations ci-dessous sont des répliques fictives, condensées pour la lisibilité. Les participants n’ont pas réellement utilisé l’application. Les avis professionnels sont eux aussi simulés ; l’exploration de l’étape 1 et la consultation des captures par l’agent principal sont les seules preuves d’interface employées.

## Dossier, personnes et méthode

Source unique de cette exécution : `docs/ux-workshops/2026-11-18/`. Lecture intégrale du README et des quatre documents d’observation, consultation des 15 captures conservées. L’instruction complète de l’étape 2 est archivée dans [02-workshop.md](../prompts/02-workshop.md). Aucun code, scénario personnel réel ou donnée applicative n’a été modifié.

Les six experts : UX Designer senior (hiérarchie et navigation), expert accessibilité (perception et interaction), Product Manager B2C (missions de lancement), expert onboarding (entrée et activation), UX Researcher (qualité des preuves), facilitateur produit (contradiction et arbitrages).

Les six habitants fictifs : Marie, 72 ans, peu numérique, tombola/lot ; Jean-Pierre, 64 ans, occasionnel, QR ; Sophie, 46 ans, intermédiaire, sorties familiales ; Thomas, 32 ans, expérimenté, rapidité ; Nathalie, 55 ans, faible appétence, lot/retrait ; Lucie, 21 ans, connectée, suivi et prochaines animations. Les profils expriment des priorités, pas des comportements déduits mécaniquement de leur âge.

Déroulement pour chaque atelier : présentation des preuves → avis individuels → réactions individuelles → contradiction → forces et problèmes → orientations stabilisées → vote nominatif → décision. Les voix reçues ont été conservées sans rééquilibrage. Le registre complet figure dans [votes-et-arbitrages.md](votes-et-arbitrages.md). Une majorité simulée ne rend pas un comportement conforme ni une hypothèse vraie.

## Qualité des preuves consultées

- **OBSERVÉ à l’étape 1 :** O1–O11 sont les références du [registre factuel](../observations/observations-factuelles.md). D1 y désigne le code, non un parcours testé.
- **OBSERVÉ SUR CAPTURE :** `01-accueil-430x844.png` présente « Ouverture de votre carnet… » et des squelettes. Il ne prouve ni accueil stabilisé ni chargement bloqué. `01-accueil-390x844.png` est une image courte ne présentant pas toute la navigation ; l’absence dans l’image ne prouve pas l’absence dans l’application.
- **OBSERVÉ SUR CAPTURE :** sur les images de page entière, la barre fixe apparaît devant une portion du contenu. Sans essai de défilement/focus, il est impossible d’en déduire qu’une action est inutilisable.
- **OBSERVÉ SUR CAPTURE :** longues descriptions dans le programme, blocs « Conditions non renseignées » dans deux fiches, bouton de récupération QR à texte sombre sur fond vert. La compréhension, la complétude des données et le contraste conforme restent à vérifier.
- **HYPOTHÈSES H1–H6 :** bénéfices proposés respectivement sur compréhension initiale, continuité QR, lot actionnable, programme compact, accessibilité et reprise. Aucune durée, taux d’erreur, émotion ou réussite n’a été mesuré.

Les [principes UX canoniques](../../../../produit/live/principes-ux.md) constituent une contrainte de cohérence : en-tête et trois onglets conservés, domaine propriétaire des règles. Le workshop n’a pas autorité pour les remplacer ; les alternatives ont néanmoins été débattues.

## Atelier A — Première impression

**Écrans et parcours présentés.** O1–O3. [Accueil stabilisé à 320 px](../visuels/captures-avant/01-accueil-320x844.png), [accueil à 390 px](../visuels/captures-avant/01-accueil-390x844.png), [Découvrir Bouliac](../visuels/captures-avant/02-decouvrir-bouliac-390x844.png). Carnet vide, action Découvrir, récupération, trois onglets ; pas de mesure de compréhension.

**Avis indépendants des experts — simulés.**

| Expert | Avis |
| --- | --- |
| UX Designer senior | Le lien entre carnet, gains et dates doit pouvoir se comprendre sans multiplication des destinations. |
| Expert accessibilité | Les mots visibles aident ; la compréhension de « carnet » et l’annonce de la navigation restent à vérifier. |
| Product Manager B2C | La première action doit correspondre aux trois missions ; aucun taux d’activation n’a été mesuré. |
| Expert onboarding | Une explication courte peut relier la promesse de l’application aux points d’entrée. |
| UX Researcher | La présence d’un libellé ne prouve pas sa découvrabilité ; comparer les tâches avant de conclure. |
| Facilitateur produit | Clarifier les trois missions dans les trois onglets ; tout changement de navigation serait un arbitrage distinct. |

**Réactions individuelles des habitants — simulées.**

| Habitant | Réaction fictive |
| --- | --- |
| Marie | « Si le carnet est vide, dites-moi ce que je peux y faire. Pour les dates, je chercherais calendrier. » |
| Jean-Pierre | « Je viens pour l’animation de l’affiche. Après, je regarderai ce que propose Bouliac. » |
| Sophie | « Je veux trouver une sortie et revenir voir les dates facilement. » |
| Thomas | « Je veux voir où cliquer ; pas relire une explication à chaque visite. » |
| Nathalie | « Je veux surtout retrouver mon gain et savoir où aller. » |
| Lucie | « J’aimerais comprendre le carnet et trouver vite ce qui arrive à Bouliac. » |

**Débat contradictoire simulé.** Marie, Sophie et Lucie défendent un onglet Calendrier parce qu’il nomme leur intention. UX et PM opposent le coût d’une destination supplémentaire au programme déjà présent dans Découvrir. L’expert accessibilité et le researcher refusent de déduire une bonne architecture du seul nombre d’onglets. Thomas réserve son jugement sur A1 tant que la place du texte n’est pas visible. Le facilitateur maintient A1 comme explication courte du carnet vide et A2 comme changement distinct, sans fusionner les votes.

**Points forts.** Action de découverte explicite, reprise visible, navigation à trois libellés.

**Problèmes et incertitudes.** H1 : le vocabulaire « carnet » et l’accès indirect aux dates pourraient laisser les missions incomplètement comprises. La rubrique Coffrets est visible, mais aucune confusion réelle n’a été observée.

**Orientations soumises et votes.**

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| A1 | Relier explicitement le carnet aux trois missions | 11 | 0 | 1 | ADOPTÉE |
| A2 | Ajouter un quatrième onglet Calendrier | 3 | 6 | 3 | REJETÉE |

**Décision enregistrée.** A1 adoptée comme clarification limitée ; A2 rejetée. Le besoin d’un accès aux dates nommé reste pris en compte dans A1/D1 sans quatrième onglet. Les conditions et critères adoptés sont détaillés dans le [backlog](backlog-ux.md), les votes individuels dans le [registre](votes-et-arbitrages.md).

## Atelier B — Participation aux animations, avec entrée QR

**Écrans et parcours présentés.** O5, O6, O9. [Fiche Juste prix](../visuels/captures-avant/03-detail-juste-prix-390x844.png), [inscription](../visuels/captures-avant/04-inscription-juste-prix-390x844.png), [fiche Vitrines](../visuels/captures-avant/05-detail-vitrines-390x844.png), [QR invalide](../visuels/captures-avant/10-qr-invalide-390x844.png). Quatre coordonnées requises, cases obligatoires/facultative, récupération sur code invalide. Aucun scan valide ni inscription envoyée.

**Avis indépendants des experts — simulés.**

| Expert | Avis |
| --- | --- |
| UX Designer senior | Les écrans d’entrée existent ; il faut éprouver le fil complet, surtout la confirmation et le retour. |
| Expert accessibilité | Noms des champs, aides, erreurs et focus doivent rester reliés à l’animation et à l’étape. |
| Product Manager B2C | Analyser l’usage des coordonnées et les consommateurs avant de supprimer une obligation métier. |
| Expert onboarding | Le nom de l’animation et une confirmation explicite doivent donner du sens à l’action. |
| UX Researcher | Ni abandon ni perte de contexte mesurés ; un QR invalide ne représente pas le parcours positif. |
| Facilitateur produit | Séparer continuité de navigation et évolution des règles de collecte ; les confirmations viennent du domaine. |

**Réactions individuelles des habitants — simulées.**

| Habitant | Réaction fictive |
| --- | --- |
| Marie | « Pour ma tombola, je veux revoir son nom et savoir si je suis bien inscrite. » |
| Jean-Pierre | « Si le code ne marche pas, dites-moi comment retrouver l’animation. Je préfère donner moins d’informations. » |
| Sophie | « Après l’inscription, je ne veux pas refaire la recherche ; peut-être que les coordonnées servent à nous prévenir. » |
| Thomas | « Je scanne pour une animation précise et je veux continuer dessus, avec le minimum à saisir. » |
| Nathalie | « Je n’ai pas envie de remplir plusieurs fois des informations ; moins de champs m’encouragerait. » |
| Lucie | « Après un lien ou un code, je veux continuer la même animation. Expliquez pourquoi vous voulez mon téléphone. » |

**Débat contradictoire simulé.** Jean-Pierre, Thomas, Nathalie et Lucie demandent la suppression de nom/téléphone ; PM, onboarding et facilitateur jugent que la simulation ne permet pas de changer les obligations. Marie et Sophie veulent connaître leur utilité ; UX, accessibilité et recherche s’abstiennent sur B2. Le chercheur insiste sur l’absence de parcours positif. B1 est donc votée comme cible et recette conditionnelle : un clic ne doit jamais être présenté comme une participation confirmée.

**Points forts.** Nom de l’animation présent sur le formulaire, coordonnées nommées, choix facultatif distingué, sortie de récupération sur lien invalide.

**Problèmes et incertitudes.** H2 : continuité et confirmation pourraient être incomprises ; aucun défaut de bout en bout prouvé. Les fiches Juste prix/Vitrines affichent « Conditions non renseignées » dans un bloc ; l’effet sur la compréhension et la qualité des données de test restent à instruire.

**Orientations soumises et votes.**

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| B1 | Conserver le contexte de l’animation du QR à la reprise | 12 | 0 | 0 | ADOPTÉE |
| B2 | Supprimer les champs nom et téléphone obligatoires | 4 | 3 | 5 | REJETÉE |

**Décision enregistrée.** B1 adoptée sous condition de données de test et preuve ; B2 rejetée. Ne pas transformer une préférence de saisie en suppression immédiate des règles. Les conditions et critères adoptés sont détaillés dans le [backlog](backlog-ux.md), les votes individuels dans le [registre](votes-et-arbitrages.md).

## Atelier C — Gestion des lots

**Écrans et parcours présentés.** O7, O8 et D1. [Mes lots vide](../visuels/captures-avant/08-lots-vides-390x844.png), [récupération](../visuels/captures-avant/09-retrouver-carnet-390x844.png). Aucun gain attribué visible. Les dotations prévues des fiches ne sont pas des gains personnels.

**Avis indépendants des experts — simulés.**

| Expert | Avis |
| --- | --- |
| UX Designer senior | Prioriser les questions où, quand et comment ; aucune difficulté d’un lot réel ne peut être affirmée. |
| Expert accessibilité | Exprimer les états en texte ; une couleur ou un QR ne suffit pas à indiquer la remise. |
| Product Manager B2C | Le retrait est une mission de lancement à vérifier sur un cas réel avant de chiffrer des corrections. |
| Expert onboarding | Le premier gain doit expliquer sa disponibilité et le geste concret attendu. |
| UX Researcher | Distinguer gain prévu, attribué, disponible, présenté et remis dans les futures tâches de compréhension. |
| Facilitateur produit | La présentation ne crée pas la règle de consommation ; « vu » et « remis » restent distincts. |

**Réactions individuelles des habitants — simulées.**

| Habitant | Réaction fictive |
| --- | --- |
| Marie | « Qu’ai-je gagné, jusqu’à quand, et où dois-je aller ? » |
| Jean-Pierre | « Avant de partir, je veux savoir que c’est bien disponible pour moi. » |
| Sophie | « Il faut comprendre qui peut retirer le lot et à quel endroit. » |
| Thomas | « La date limite, le lieu et le bouton utile au même endroit. » |
| Nathalie | « Est-ce que j’ai vraiment gagné et est-ce que je peux encore en profiter ? » |
| Lucie | « Je veux voir si je peux l’utiliser maintenant ; ouvrir le code ne doit pas le consommer. » |

**Débat contradictoire simulé.** Le facilitateur soumet C2 comme raccourci possible entre affichage et consommation. Les habitants le refusent : Marie pourrait montrer l’écran pour demander de l’aide, Sophie pour préparer un retrait et Lucie l’ouvrir plusieurs fois. Le PM et l’expert accessibilité soulignent le risque d’une transition involontaire. Le researcher conteste toute conclusion sur le lot réel à partir du vide. C1 reçoit l’accord comme cible à confronter à l’existant, sans imaginer un écran personnel absent des preuves.

**Points forts.** État vide explicite, récupération et aide visibles ; onglet Mes lots stable.

**Problèmes et incertitudes.** H3 : l’ordre des informations pratiques pourrait conditionner l’autonomie. Aucune preuve de consignes manquantes sur un gain attribué. C2 représente un risque introduit par une proposition, pas un incident actuel.

**Orientations soumises et votes.**

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| C1 | Rendre le lot confirmé immédiatement compréhensible et actionnable | 12 | 0 | 0 | ADOPTÉE |
| C2 | Consommer automatiquement le lot à l’affichage du QR | 0 | 12 | 0 | REJETÉE |

**Décision enregistrée.** C1 adoptée ; C2 rejetée unanimement. Le risque fonctionnel resterait signalé même si la simulation avait voté autrement. Les conditions et critères adoptés sont détaillés dans le [backlog](backlog-ux.md), les votes individuels dans le [registre](votes-et-arbitrages.md).

## Atelier D — Calendrier des animations : liste, cartes ou grille

**Écrans et parcours présentés.** O4, O5, O11. [Programme à 320 px](../visuels/captures-avant/02-decouvrir-bouliac-320x844.png), [programme à 430 px](../visuels/captures-avant/02-decouvrir-bouliac-430x844.png), [tombola à venir](../visuels/captures-avant/06-detail-tombola-390x844.png). En ce moment précède Prochainement ; dates présentes ; /live/calendrier redirige vers Découvrir.

**Avis indépendants des experts — simulés.**

| Expert | Avis |
| --- | --- |
| UX Designer senior | Comparer des dates doit primer sur le nom du composant ; les cartes longues demandent beaucoup de lecture. |
| Expert accessibilité | Une liste séquentielle est une base utile ; compacter ne signifie ni réduire le texte ni les cibles. |
| Product Manager B2C | Trois événements ne justifient pas à eux seuls une grille obligatoire à développer et maintenir. |
| Expert onboarding | Le premier choix nécessite assez d’information pour distinguer les animations, sans tout le règlement. |
| UX Researcher | L’avantage comparé liste/grille dépend des tâches et de la densité ; aucun test comparatif réalisé. |
| Facilitateur produit | Améliorer le programme dans Découvrir est compatible avec la structure retenue ; garder les dates métier. |

**Réactions individuelles des habitants — simulées.**

| Habitant | Réaction fictive |
| --- | --- |
| Marie | « La prochaine animation sans lire toutes les grandes affiches ; pas de petites cases imposées. » |
| Jean-Pierre | « Pour prévoir mon mois, j’aime voir les dates ensemble. » |
| Sophie | « Je cherche souvent le week-end prochain, pas seulement aujourd’hui. » |
| Thomas | « Je veux comparer plusieurs animations rapidement. » |
| Nathalie | « Je regarderai peut-être ensuite ; mon lot passe avant les prochaines dates. » |
| Lucie | « Je veux aller directement à ce qui arrive après. Une grille seulement si j’en ai besoin. » |

**Débat contradictoire simulé.** Jean-Pierre soutient la grille mensuelle par défaut pour organiser son mois. Sophie préfère une liste ; Marie veut un mot connu pour accéder aux dates mais refuse de petites cases. UX propose de conserver l’identité des cartes tout en raccourcissant leur contenu ; accessibilité exige texte et surfaces d’action lisibles. Le PM refuse que l’absence de grille soit traitée comme une fonctionnalité manquante. D1 est précisée : accès Prochainement, dates et informations de choix, sans masquer achat requis ou restrictions essentielles.

**Points forts.** Dates et états visibles, groupes temporels, détail ouvrable ; la tombola annonce son démarrage prochain.

**Problèmes et incertitudes.** OBSERVÉ SUR CAPTURE : longues descriptions avant Prochainement. H4 : le repérage d’une date future pourrait demander trop de parcours visuel. Aucun temps de recherche mesuré.

**Orientations soumises et votes.**

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| D1 | Présenter un programme chronologique compact et un accès Prochainement | 11 | 0 | 1 | ADOPTÉE |
| D2 | Imposer une grille mensuelle par défaut sur mobile | 1 | 11 | 0 | REJETÉE |

**Décision enregistrée.** D1 adoptée ; Nathalie s’abstient. D2 rejetée malgré la préférence de Jean-Pierre. Une vue mensuelle optionnelle n’est ni adoptée ni déclarée inutile. Les conditions et critères adoptés sont détaillés dans le [backlog](backlog-ux.md), les votes individuels dans le [registre](votes-et-arbitrages.md).

## Atelier E — Maniabilité et accessibilité

**Écrans et parcours présentés.** O2 et limites de capture. [Accueil 320 px](../visuels/captures-avant/01-accueil-320x844.png), [chargement 430 px](../visuels/captures-avant/01-accueil-430x844.png), formulaire 04 et QR 10. Aucun test clavier, zoom, lecteur d’écran ou mesure de contraste disponible.

**Avis indépendants des experts — simulés.**

| Expert | Avis |
| --- | --- |
| UX Designer senior | Les captures montrent des repères mais pas toute l’interaction ; vérifier avant de qualifier un obstacle. |
| Expert accessibilité | Contrôler focus, restitution, contrastes, redistribution et erreurs sur les processus complets. |
| Product Manager B2C | Prioriser les obstacles démontrés pour les missions ; ne pas transformer une impression en dette certaine. |
| Expert onboarding | Une première visite doit rester praticable avec aides d’accès et messages compréhensibles. |
| UX Researcher | Non testé ne signifie ni conforme ni défaillant ; la qualité d’une capture limite l’inférence. |
| Facilitateur produit | Les résultats de recette détermineront la correction et sa priorité, indépendamment de sa popularité. |

**Réactions individuelles des habitants — simulées.**

| Habitant | Réaction fictive |
| --- | --- |
| Marie | « J’ai besoin d’agrandir et de comprendre les boutons. » |
| Jean-Pierre | « Si ça ne marche pas, expliquez-moi la suite avec des mots simples. » |
| Sophie | « Entre deux choses, je veux savoir ce qu’il faut corriger sans deviner. » |
| Thomas | « Ça doit fonctionner aussi quand j’agrandis ou navigue autrement. » |
| Nathalie | « Je ne veux pas apprendre de nouveaux dessins pour retrouver mon lot. » |
| Lucie | « Certaines icônes me suffisent, mais pas forcément celles propres à l’application. » |

**Débat contradictoire simulé.** L’option E2 vise une navigation moins chargée. Lucie s’abstient, car elle connaît certaines icônes ; les autres habitants refusent la disparition de tous les mots. L’expert accessibilité rappelle qu’un nom accessible invisible ne remplace pas le texte visible pour chacun. UX refuse de diagnostiquer un bouton inaccessible sur la seule superposition de la barre fixe dans une capture longue. E1 devient un contrôle suivi de corrections ciblées, avec le bouton QR comme point d’attention à mesurer.

**Points forts.** Navigation avec mots et pictogrammes ; champs et choix visibles ; largeur mobile prise en compte.

**Problèmes et incertitudes.** H5 : contraste du bouton QR, focus masqué ou lecture au zoom pourraient poser problème, sans mesure actuelle. La capture 430 px témoigne d’un chargement, sans information sur sa durée.

**Orientations soumises et votes.**

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| E1 | Vérifier l’accessibilité puis corriger les obstacles établis | 12 | 0 | 0 | ADOPTÉE |
| E2 | Remplacer les libellés de navigation par des icônes seules | 0 | 11 | 1 | REJETÉE |

**Décision enregistrée.** E1 adoptée ; E2 rejetée, avec abstention de Lucie. Aucun certificat de conformité ni P0 fondé sur les captures seules. Les conditions et critères adoptés sont détaillés dans le [backlog](backlog-ux.md), les votes individuels dans le [registre](votes-et-arbitrages.md).

## Atelier F — Simplification et adoption

**Écrans et parcours présentés.** O7, O8, O10. [Participations vides](../visuels/captures-avant/07-participations-vides-390x844.png), [récupération](../visuels/captures-avant/09-retrouver-carnet-390x844.png), [retour à Bouliac](../visuels/captures-avant/11-retour-decouvrir-bouliac-390x844.png). Le carnet rempli, le retour après plusieurs jours et les notifications ne sont pas éprouvés.

**Avis indépendants des experts — simulés.**

| Expert | Avis |
| --- | --- |
| UX Designer senior | Une prochaine action peut donner du sens au retour ; vérifier le carnet rempli avant de le redessiner. |
| Expert accessibilité | Récupération et changements d’état doivent rester perceptibles dans tous les états du carnet. |
| Product Manager B2C | Revenir pour une activité réelle est une hypothèse plus concrète qu’une sollicitation préalable. |
| Expert onboarding | Relier le retour à un bénéfice déjà identifié, sans demander un engagement avant découverte. |
| UX Researcher | Le maintien de Bouliac est observé ; rétention et reprise personnelle ne sont pas mesurées. |
| Facilitateur produit | Réutiliser la recette de B1/C1 ; ne pas ajouter de mécanique secondaire au périmètre. |

**Réactions individuelles des habitants — simulées.**

| Habitant | Réaction fictive |
| --- | --- |
| Marie | « Je veux retrouver ma tombola et savoir ce qu’il reste à faire. » |
| Jean-Pierre | « Si je ferme après avoir scanné, je veux retrouver ce que j’avais commencé. » |
| Sophie | « Je veux retrouver ce qui est confirmé ; je choisirai les rappels après. » |
| Thomas | « Reprendre sans devoir me souvenir de l’écran où j’étais. » |
| Nathalie | « Une semaine après, retrouver mon gain sans tout refaire. » |
| Lucie | « Mes participations et ce qui se passe ensuite ; des rappels pour une animation que j’ai choisie. » |

**Débat contradictoire simulé.** Le facilitateur oppose la demande de notifications dès l’entrée à la reprise dans le carnet. Sophie et Lucie envisagent des rappels contextualisés mais refusent la sollicitation préalable ; cela ne vote pas une nouvelle fonction de notification. Le PM conditionne F1 à un écart observé, le code contenant déjà un carnet personnel. Thomas souligne le coût de retrouver son écran, Nathalie celui de retrouver son gain. Le researcher interdit d’en déduire un taux de retour.

**Points forts.** Récupération accessible dans le vide, Bouliac conservée au retour navigateur.

**Problèmes et incertitudes.** H6 : un état et une prochaine action pourraient faciliter la reprise. On ne sait pas encore si le carnet rempli répond déjà à ce besoin. La visibilité des coffrets ne justifie pas d’étendre le workshop à leurs parcours.

**Orientations soumises et votes.**

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| F1 | Organiser la reprise autour de l’état confirmé et de la prochaine action | 12 | 0 | 0 | ADOPTÉE |
| F2 | Demander les notifications avant la découverte | 0 | 12 | 0 | REJETÉE |

**Décision enregistrée.** F1 adoptée comme complément conditionnel en P2 ; F2 rejetée. Les raisons de revenir restent des hypothèses liées aux trois missions. Les conditions et critères adoptés sont détaillés dans le [backlog](backlog-ux.md), les votes individuels dans le [registre](votes-et-arbitrages.md).

## Clôture de la simulation

Six orientations sont adoptées ; six alternatives sont conservées séparément. Aucun P0 établi et aucun résultat d’usager réel ajouté au dossier. Les risques fonctionnels et d’accessibilité restent signalés indépendamment du score de vote. Le [rapport exécutif](rapport-executif.md) présente les notes heuristiques, la matrice des six habitants et quatre orientations prioritaires, sans compléter artificiellement à cinq.

Recommandation : **GO SOUS CONDITIONS**, limitée par les parcours personnels et contrôles d’accessibilité non exécutés. Étape 2 terminée ; autorisation attendue avant l’étape 3.
