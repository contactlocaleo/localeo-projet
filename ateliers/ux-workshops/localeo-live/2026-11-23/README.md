# Relance du workshop UX Localeo Live — 23 novembre 2026

**Statut · PARTIEL, archive vérifiée. Les cinq étapes documentaires sont terminées et les six maquettes P1 sont validées. Les parcours personnels et les essais avec des habitants restent à éprouver.**

| Repère | Valeur |
| --- | --- |
| Date et heure | 23 novembre 2026, Europe/Paris. Premières lectures vers 07 h 45, dossier créé à 07 h 46 et dernières captures vers 07 h 54. Archivage entrepris à 08 h 55. |
| Site et commune | [Localeo Live TEST](https://test-live.localeo.city/) · Bouliac 33270 |
| Objectif | Explorer la participation et sa reprise, les lots et le programme daté. Consultation secondaire des coffrets. |
| Branche et commit documentaires à l’ouverture | `main` · `224870a826bdff3d2c0fe7af3bc62d700f0d4832` |
| Branche et commit Marketplace consultés | `main` · `ccd4ac72432d17a0c39d090d73b14e095d796f84` · [portée de la preuve](observations/limitations.md) |
| Chemin de cette exécution | `ateliers/ux-workshops/localeo-live/2026-11-23/`. Ce dossier regroupe aussi les visuels d’appoint. |
| Navigateur | Chromium 151 via Playwright, vues tactiles de 320 × 844, 390 × 844 et 430 × 844 CSS px. |
| Modèle et protocole | Codex, famille GPT-6. Le niveau exact de raisonnement et les identifiants des sous-agents ne sont pas établis. [Demande de relance du 23 et protocoles 01 à 05](prompts/README.md). |

Au démarrage, aucun workshop Localeo Live explicitement terminé n’a été trouvé. Le [18 novembre](../2026-11-18/README.md) a servi de référence provisoire. Ses six orientations ont été retenues pour cadrage. La comparaison rapproche les observations et les décisions des deux exécutions. Les [instructions de relance et la réponse sur le périmètre](prompts/README.md) sont archivées avec les références historiques. Le prompt global 00 historique reste manquant.

## Étape 1 — Résultats et preuves

- L’accueil stabilisé donne les repères pour les trois missions. Le raccourci « Prochainement » atteint l’état vide et y déplace le focus sur les trois largeurs.
- L’aperçu initial de Bouliac affiche 10 animations « En cours » et 0 à venir. Huit cartes « En cours » portent une date de fin antérieure au 23 novembre. Les fiches Juste Prix et Vitrines explicitent l’attente de la clôture.
- La fiche « Passeport commercant » est indisponible malgré sa présence dans l’aperçu initial. Le formulaire d’une tombola publique contient deux consignes opposées sur la visite chez un commerçant.
- L’exploration couvre les formulaires vierges, le refus d’un accès invalide, les états vides et le retour vers Bouliac. Un essai ultérieur du programme a affiché un message de limitation de débit.
- 34 captures PNG du site ont été conservées. Les 15 JPG fournis restent à leur emplacement d’origine et documentent notamment des exemples personnels. [Captures du navigateur](visuels/captures-avant/) · [Visuels fournis](visuels/visuels-fournis.md)

| Livrable | Lien |
| --- | --- |
| Parcours inspectés et suites réelles | [Cartographie](observations/cartographie-parcours.md) |
| Écrans, routes et composants | [Inventaire](observations/inventaire-ecrans.md) |
| Constats, déductions et comparaison historique | [Observations factuelles](observations/observations-factuelles.md) |
| Parcours personnels et contrôles restant à couvrir | [Limites](observations/limitations.md) |

Le périmètre public a été confirmé par l’utilisateur. QR valide, réception du lien e-mail, inscription confirmée, progression personnelle et utilisation d’un lot restent à couvrir. Les répertoires des phases suivantes sont préparés localement. Seul `localeo-projet` est concerné par les ajouts de cette exploration. Les quatre dépôts applicatifs sont propres au contrôle Git et les guides Commerçant et Animation sont sans impact pour ce travail d’observation.

Contrôles de clôture de l’étape 1. `check_guidance.py` et `check_workspace.py` réussis. Les 139 liens relatifs du dossier résolvent leurs cibles. Les 34 PNG ont été relus visuellement, rapprochés de leurs traces navigateur et contrôlés aux dimensions annoncées. La demande jointe et les huit fichiers historiques copiés ont été comparés octet par octet.

## Étape 2 — Workshop simulé

Le 23 novembre 2026, à partir de 08 h 05 (Europe/Paris), six experts et six habitants fictifs ont débattu des trois missions en six ateliers. Le workshop s’appuie sur les preuves publiques et les visuels fournis. Les réactions, notes et votes sont simulés. [Autorisation reçue](prompts/02-autorisation.txt) · [Protocole d’étape](prompts/02-workshop.md)

- **14 propositions, 168 votes nominatifs, 8 orientations adoptées et 6 rejetées.** Six P1, deux P2 et aucun P0 établi à l’échelle d’une mission entière. Seuil fixe de sept voix favorables.
- **NO GO simulé pour une ouverture à 10 000 habitants le lendemain.** La fiche Passeport indisponible, les consignes contradictoires de la tombola et l’interprétation du programme motivent les premières actions publiques. Les parcours positifs QR et lots ainsi que les contrôles d’accessibilité restent à éprouver. La 429 observée demande une vérification d’exploitation.

| Livrable | Contenu |
| --- | --- |
| [Rapport exécutif](workshop/rapport-executif.md) | Notes heuristiques, matrice habitants × parcours et cinq améliorations avant ouverture. |
| [Compte rendu](workshop/compte-rendu.md) | Avis individuels, preuves, débats et arbitrages des six ateliers. |
| [Votes et arbitrages](workshop/votes-et-arbitrages.md) | Bulletins complets, décomptes et risques conservés. |
| [Backlog UX](workshop/backlog-ux.md) | Priorités, efforts, bénéfices, critères et confiance. |
| [Orientations rejetées](workshop/orientations-rejetees.md) | Options écartées et raisons des avis minoritaires. |
| [Actions à faible effort](workshop/quick-wins.md) | Trois actions rattachées aux orientations adoptées. |
| [Comparaison](synthese/comparaison-precedent.md) | Écarts observés, résultats simulés et décisions comparés au 18 novembre. |

Les travaux de cette étape sont documentaires et confinés à ce dossier. Le dossier du 18 reste la référence de comparaison et les guides Commerçant et Animation ne sont pas affectés par la simulation.

Contrôles de clôture de l’étape 2. `check_guidance.py` et `check_workspace.py` réussis. Les 238 liens relatifs du dossier, les douze avis par atelier, les 168 votes, leurs décomptes et les correspondances avec le backlog ont été vérifiés. Le contrôle Git des quatre dépôts applicatifs est propre.

## Étape 3 — Maquettes avant et après

Le 23 novembre 2026 à partir de 08 h 19 (Europe/Paris), 24 états ont été préparés pour B1, B3, C1, D1, D3 et E1, les six P1 adoptées. Les 34 captures réelles de l’étape 1 restent les preuves publiques de référence. La galerie distingue capture équivalente, capture de contexte et AVANT manquant. [Autorisation reçue](prompts/03-autorisation.txt) · [Protocole d’étape](prompts/03-maquettes.md)

| Livrable | Contenu |
| --- | --- |
| [Comparatif avant / après](visuels/comparatif-avant-apres.html) | Vue côte à côte sur ordinateur, bascule sur mobile, états, bénéfices, votes et efforts. |
| [Référence des maquettes](visuels/reference-maquettes.md) | Correspondances et conditions pour les 24 états. |
| [Revue contradictoire](visuels/revue-contradictoire.md) | Six avis d’experts, les cinq questions aux six habitants et les ajustements retenus. Tous les avis sont simulés. |
| [Contrôles des maquettes](visuels/controle-maquettes.md) | 72 lectures à 320/390/430 px et 24 lectures avec texte agrandi à 200 %, bascule mobile et focus ciblé. |

La revue a précisé les libellés et les retours sans changer les orientations adoptées. Les votes d’origine s’appliquent. La règle réelle de la tombola, les accès QR et lots, la restauration du programme et les aides d’accès restent conditionnés à la recette. Le backlog relie chaque P1 à ses planches. Les fichiers sont isolés dans ce dossier de `localeo-projet`. Les guides Commerçant et Animation sont sans impact pour ce travail de maquette.

## Étape 4 — Validation des maquettes

Le 23 novembre 2026 (Europe/Paris), l’utilisateur a validé l’ensemble présenté en réponse à la demande de validation. L’accord porte sur B1, B3, C1, D1, D3 et E1, dans la version `2026-11-23-maquettes-v1` de la galerie et de ses 24 états. Les parcours personnels et les contrôles de recette identifiés restent à éprouver dans Live. [Réponse exacte](prompts/04-decision-utilisateur.txt) · [Protocole d’étape](prompts/04-validation.md)

| Livrable | Contenu |
| --- | --- |
| [Revue des propositions](validation/revue-pour-decision.md) | Missions, preuves, votes, maquettes, bénéfices, efforts et risques ouverts. |
| [Registre des décisions](validation/decisions.md) | Accord collectif enregistré pour les six P1, avec date et version. |
| [Empreintes de la version validée](validation/maquettes-validees.json) | Empreintes SHA-256, liste des états, captures et ressources. |
| [Travaux applicatifs potentiels](validation/travaux-applicatifs-potentiels.md) | Ordre proposé, dépendances et preuves de recette. |

Contrôles de validation réussis. Les 27 empreintes du manifeste, les 371 liens locaux et la concordance entre les six décisions, les votes et les 24 états ont été vérifiés. La galerie s’ouvre aux six destinations et la bascule à 390 px fonctionne dans Chromium. Le contrôle Git est propre dans les quatre dépôts applicatifs.

## Étape 5 — Archivage final

L’accord d’archivage a été reçu le 23 novembre 2026. Les observations, les 34 PNG du site, les 168 votes, la galerie, ses 24 états et les décisions des six P1 sont conservés dans ce dossier. Le [manifeste de l’archive](synthese/manifeste-archive.json) enregistre leurs empreintes. [Autorisation exacte](prompts/05-autorisation.txt) · [Protocole d’archivage](prompts/05-archivage.md)

| Livrable | Contenu |
| --- | --- |
| [Inventaire de l’archive](synthese/inventaire-archivage.md) | Livrables, références de roadmap, limites et anomalies ouvertes. |
| [Comparaison avec le 18 novembre](synthese/comparaison-precedent.md) | Écarts vérifiés, constats nouveaux et orientations, votes, priorités et notes comparés. |
| [Plan proposé de tests utilisateurs](validation/plan-tests-utilisateurs.md) | Scénarios pour Bouliac, critères observables et prérequis d’une recette autorisée. |
| [Prompt autonome de relance](prompts/RELANCER-WORKSHOP.md) | Reprise du protocole et des points d’arrêt dans une nouvelle conversation. |

Le QR valide, l’inscription confirmée, le retrait de lot et la reprise personnelle restent à vérifier. Les constats fonctionnels du 23 et la limitation de débit restent documentés. La roadmap canonique conserve le cadrage du 18 et les suites du 23 figurent dans les travaux potentiels. La décision de développer relève d’une instruction ultérieure.

Contrôles d’archivage. Empreintes de la version validée et de l’archive, prompts exacts, liens relatifs, couverture des 34 captures et décompte des votes contrôlés. Galerie rouverte dans Chromium avec ses 24 états et la bascule mobile. Les cinq dépôts Git restent indépendants et le contrôle des quatre dépôts applicatifs est propre.
