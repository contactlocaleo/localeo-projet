# Localeo Animation — exploration et workshop UX du 18 novembre 2026

**Statut courant : onze orientations autorisées, implémentées et poussées ; recette UX à valider. Aucune autorisation de développement encore attendue dans ce périmètre. D2 conserve sa validation fonctionnelle explicite. Maquettes et revue du workshop simulées.**

**Suite explicitement demandée après le workshop :** les skills de spécification
et d'implémentation ont été invoqués pour E73-EVO-WORKSHOP-UX-20261118.
Les onze orientations retenues ont été réalisées localement ; les preuves et
limites figurent dans le [bilan canonique WA](../../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#workshop-ux-20261118).
Cette suite ne transforme pas les votes simulés en essais humains et ne
réécrit pas les décisions individuelles de maquette consignées à l'étape 4.
La demande ultérieure autorise également les commits, le push et la mise à
jour du schéma TEST ; leur résultat est consigné dans ce même bilan.

## Exécution

- Début des relevés : 18 novembre 2026 à 11 h 27, Europe/Paris (UTC+01:00).
- Dernières captures : vers 11 h 41 ; consolidation documentaire : 11 h 43, le même jour.
- Consolidation du workshop simulé : 18 novembre 2026 vers 12 h 01, Europe/Paris ; horodatage exact du contrôle dans le manifeste d’étape 2.
- URL analysée : https://test-animations.localeo.city — titre observé « Localeo Animation [TEST] ».
- Contexte : organisateur autorisé, Association Test Thibaut, commune de Bouliac. Aucun identifiant de connexion archivé.
- Dépôt documentaire : `localeo-projet`, branche `main`, commit `7164846f266cc0c073dc0c4642c569d9b8c6676c`.
- Code Animation lu : commit local `80c42809ff751ba99895b4634180663609a365aa`. Le commit effectivement déployé n’a pas été identifié.
- Agent : Codex, famille GPT-6 connue par le contexte ; révision exacte et niveau de raisonnement non exposés.
- Protocole : instruction utilisateur « ÉTAPE 1 — INITIALISATION ET EXPLORATION UX LOCALEO ANIMATION », version reçue pour cette exécution, [texte complet expurgé](prompts/01-exploration.md).
- Workshop : instruction « ÉTAPE 2 — WORKSHOP UX LOCALEO ANIMATION » fournie en pièce jointe, [texte complet identique à la source](prompts/02-workshop.md). Version 1 des orientations ; avis indépendants, débat puis votes. Le [prompt complet de l’étape 3](prompts/03-maquettes.md) a ensuite été fourni et exécuté ; le [prompt complet de l’étape 4](prompts/04-validation.md) a ensuite été fourni pour préparer les décisions ; l’étape 5 Animation n’a pas été fournie.
- Méthode : Playwright/Chromium connecté à l’environnement, ordinateur 1440 × 1000 puis fenêtre mobile 390 × 844 ; inspection ciblée des sources Animation et backend, sans modification applicative.

## Objectif

Préparer le workshop sur la création/publication, l’intégration des commerçants, le suivi opérationnel, la clôture et le pilotage global. La promesse « créer une animation simple en 5 à 10 minutes, puis la piloter en toute autonomie » **n’est pas validée** : aucune mesure avec un organisateur réel et aucune publication complète dans cette exploration.

## Résultats essentiels

- Connexion, tableau de bord, recherche, création d’une tombola et d’un passeport, reprise de brouillon et clonage effectivement exécutés.
- Aperçu d’import exécuté avec deux lignes synthétiques sans coordonnées ; aucune confirmation de création de fiches.
- Consultation des participations, invitations acceptées existantes, notifications, gagnants, dossiers de fin et bilans.
- Publication du brouillon bloquée par les accords commerçants manquants ; clôture explorée jusqu’à sa confirmation, sans l’exécuter.
- Communication inaccessible lors du contrôle : deux réponses HTTP 500 relevées, dont une après actualisation.
- Sept étapes avant l’enregistrement initial du brouillon ; seuil de passeport à ajuster pour deux commerces ; libellés de diagnostic parfois techniques ; doublons potentiels de nom/adresse non signalés dans l’aperçu d’import.
- Huit écrans mesurés à 390 px sans débordement horizontal global. Cela ne prouve pas une recette sur téléphone réel ni une conformité d’accessibilité complète.

## Écritures de test conservées

Trois nouveaux brouillons, clairement préfixés `UX TEST 2026-11-18`, restent dans l’environnement : tombola, passeport et clone. Un flux et un dépôt d’import restent à l’état d’aperçu. [Détail et identifiants des objets](observations/limitations.md#objets-de-test-créés).

Aucune invitation, notification, publication, clôture, remise ou suppression déclenchée. Les invitations des nouveaux brouillons sont restées à envoyer. Aucun achat ni paiement. Les objets existants ont été consultés ; aucun état d’animation existante n’a été modifié par cette exploration.

## Livrables d’exploration

- [Cartographie des 18 parcours](observations/cartographie-parcours.md)
- [Inventaire des écrans et captures](observations/inventaire-ecrans.md)
- [Observations factuelles et hypothèses](observations/observations-factuelles.md)
- [Mesures de parcours](observations/mesures-parcours.md)
- [Limitations et objets créés](observations/limitations.md)
- [Repères du code et mécanismes](observations/sources-code.md)
- [Relevés techniques expurgés](observations/releves-techniques.json)
- [Contrôles documentaires et intégrité](observations/controle-final.md)
- [Captures réelles](visuels/captures-avant/) : 63 PNG, sans reconstruction ; les masques roses occultent les coordonnées présentes sur certaines vues.
- [Prompt complet de l’étape 1](prompts/01-exploration.md). Les emplacements 00 et 05 signalent les instructions Animation non fournies.

## Résultats et livrables du workshop simulé

Le workshop utilise cinq perspectives expertes et sept profils métier fictifs, préparés en trois groupes séparés. Il ne remplace pas des entretiens ni des tests utilisateurs. Les versions exactes de modèle et niveaux de raisonnement des agents ne sont pas exposés ; aucun paramètre de modèle n’a été imposé aux délégations.

- **17 orientations proposées ; 204 votes simulés ; 11 adoptées**, dont **1 P0 et 8 P1** ; 2 P2 adoptées. Cinq propositions rejetées, une non adoptée à six voix. Seuil fixe : sept POUR sur douze.
- **Conclusion : NO GO pour une ouverture autonome immédiate à 500 organisations.** Communication échoue dans le contexte testé ; plusieurs parcours critiques restent non vérifiés de bout en bout. Cette conclusion n’affirme pas une panne globale.
- **Validation utilisateur à la fin de l’étape 2 : aucune.** Adoption simulée ne vaut ni validation de conception ni autorisation de développement. Les maquettes et la décision ultérieure D2 sont référencées ci-dessous.
- [Rapport exécutif : notes heuristiques, risques et cinq priorités](workshop/rapport-executif.md)
- [Compte rendu : sept ateliers et matrice des sept profils](workshop/compte-rendu.md)
- [Votes nominatifs, arguments et débats](workshop/votes-et-arbitrages.md)
- [Backlog complet et critères futurs](workshop/backlog-ux.md)
- [Orientations rejetées ou non adoptées](workshop/orientations-rejetees.md)
- [Quick wins candidats](workshop/quick-wins.md)
- [Propositions exactes soumises](workshop/orientations-soumises.md)
- Avis initiaux : [experts](workshop/avis-independants-experts.md), [métier 1](workshop/avis-independants-metier-1.md), [métier 2](workshop/avis-independants-metier-2.md)
- Bulletins structurés : [experts](workshop/bulletins-experts.json), [métier 1](workshop/bulletins-metier-1.json), [métier 2](workshop/bulletins-metier-2.json) ; [résultats calculés](workshop/resultats-votes.json), [détails du backlog](workshop/details-orientations.json)
- [Contrôle final de l’étape 2](workshop/controle-etape-2.md) et [empreintes de l’étape 2](workshop/manifest-etape-2-sha256.json)

Le manifeste sous `observations/` décrit l’état de fin d’étape 1 : il est conservé comme preuve historique. Le README et le prompt 02 ont évolué à l’étape 2 ; les observations et 63 captures restent celles de l’exploration initiale. Les limites de cadrage de certaines images sont précisées dans le compte rendu.

À la fin de l’étape 2, les dossiers `validation/` et `synthese/` étaient réservés aux étapes suivantes. Le dossier `validation/` est maintenant initialisé pour l’étape 4 ; `synthese/` reste réservé. Les archives Localeo Pro et Localeo Live restent distinctes et ne sont pas modifiées. Aucune nouvelle action sur l’application ni sur ses données pendant l’étape 2.


## Étape 3 — propositions visuelles livrées

Consolidation le 18 novembre 2026 ; horodatage exact dans le manifeste d’étape 3. Périmètre fermé : **A1, B1, B2, B3, C1, C2, D1, D2, E1** (1 P0, 8 P1, toutes adoptées à au moins sept voix simulées).

- [Ouvrir la galerie comparative](visuels/comparatif-avant-apres.html) : côte à côte sur ordinateur, bascule avant/après sur mobile, filtres priorité/parcours et liens vers chaque état.
- [Maquettes HTML isolées](visuels/maquettes-apres/README.md) : **9 parcours, 30 états, 60 rendus PNG bureau/mobile** dans la version finale v2. Quatre captures supplémentaires documentent les contrôles de la galerie.
- [Revue contradictoire](workshop/revue-maquettes.md) : 108 fiches initiales et six questions par fiche, explicitement simulées ; relecture ciblée v2 par les douze rôles.
- [Arbitrages complémentaires](workshop/arbitrages-maquettes.md) : corrections visuelles C2/E1, sauvegarde B1 remontée, vocabulaire et filtres clarifiés. Aucun changement substantiel identifié ; aucun nouveau vote.
- [Backlog relié aux maquettes](workshop/backlog-ux.md) ; [sources et correspondances AVANT/APRÈS](visuels/preuves-comparatif.json).
- [Contrôles de l’étape 3](workshop/controle-etape-3.md), [interactions locales](workshop/controle-interactions-maquettes.json), [empreintes finales](workshop/manifest-etape-3-sha256.json).
- [Itération v1 conservée](visuels/maquettes-apres/iterations/v1/manifest-v1.json), pour lire les avis sans les réattribuer aux rendus corrigés.

**Limites :** B3 n’a pas de cadrage AVANT montrant directement le seuil ; AN-05 et le relevé DOM portent le constat. Communication n’est pas réparée par une maquette. Le contrat de brouillon partiel B1, le circuit canonique C1, les faux positifs C2 et les vérifications métier restent ouverts. Les contrôles locaux ne valent ni test humain ni conformité d’accessibilité complète.

Aucune nouvelle connexion à l’environnement TEST ni nouvelle action sur ses données pendant l’étape 3. Aucun code applicatif modifié. Les données des maquettes sont fictives, leurs boutons changent seulement des états locaux ; aucune API n’est appelée. Les 63 captures AVANT sont inchangées. Les manifestes précédents restent historiques ; README, prompt 03 et backlog ont évolué pour cette livraison.

**Fin de l’étape 3 :** propositions livrées sans validation ni implémentation. L’instruction ultérieure d’étape 4 autorise la préparation du dossier de décision ci-dessous.


## Étape 4 — registre actualisé après réalisation

Préparation le 2026-11-18T12:38:07+01:00. Le [prompt complet reçu](prompts/04-validation.md) est archivé. Cette instruction ne vaut pas accord sur les orientations.

- [Dossier des neuf orientations à décider](validation/orientations-a-decider.md) : parcours, problème, conséquence, priorité, vote simulé, AVANT réel, APRÈS v2, bénéfice, effort et dépendances pour chaque ID.
- [Risques critiques non résolus](validation/risques-critiques.md), séparés des décisions ; les rejets simulés ne suppriment pas les besoins associés.
- [Registre des décisions](validation/decisions.md) : **11 réalisations autorisées, implémentées et poussées ; 11 recettes UX à valider**. D2 conserve sa validation de direction fonctionnelle ; aucun accord de recette inventé.
- [Backlog réalisé](validation/backlog-implementation-potentiel.md) : objectifs et critères reliés au bilan canonique d’implémentation.
- [Contrôle de préparation](validation/controle-preparation.md) ; [manifest de préparation](validation/manifest-preparation-sha256.json).

Les votes, maquettes et captures de l’étape 3 restent inchangés. Son manifeste est historique : seuls README et prompt 04 évoluent parmi ses fichiers. Les nouvelles pièces sont dans `validation/`. Aucun test applicatif ni nouvelle connexion à l’environnement TEST à cette étape. Aucun code applicatif modifié.

**Reste à valider :** la recette UX du résultat, avec les choix VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE et les conditions éventuelles. Le développement est réalisé et poussé ; les migrations TEST 324 à 326 sont appliquées. Le déploiement des nouvelles interfaces et la recette humaine ne sont pas attestés. Les choix de recette non exprimés restent À VALIDER.

## Suites cadrées le 18 novembre 2026

À la demande d’analyser les évolutions/corrections à réaliser, les onze orientations adoptées sont reliées à l’[EPIC 73 — E73-EVO-WORKSHOP-UX-20261118](../../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-ux-20261118) : 18 critères, lots P0/P1 et P2 distincts, écarts aux travaux AP/PO/SA existants. Aucun nouveau numéro d’epic ni réouverture de sa clôture historique.

L’utilisateur privilégie explicitement l’atelier en cas de contradiction : D2 remplace la destination Bilan de PO-13 ; le volet de clôture automatique future E2/CAF est retiré, report/rapport indépendants à recadrer. Le registre trace D2 sans inventer huit validations individuelles supplémentaires. Les six propositions non retenues ne sont pas ajoutées au programme.

Au moment du cadrage initial seulement : aucun code applicatif modifié. La réalisation ultérieure est tracée dans le bilan canonique et le registre actualisé. Les captures, maquettes, votes et rapports restent les preuves historiques. Les manifestes d’étape 3 et de préparation d’étape 4 décrivent leurs versions antérieures ; les documents de décision/README ont évolué après l’arbitrage.
