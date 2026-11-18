# Workshop UX Localeo Live — 2026-11-18

**Suite du 18 novembre 2026 : les six orientations sont retenues pour cadrage
par l'utilisateur, avec A1/F1 en P2.** Le [registre courant](validation/decisions.md),
l'[audit des suites](../../../audits/marketplace/localeo-live-workshop-arbitrages-2026-11-18.md)
et le [cadrage E73-WL](../../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-live-20261118)
font foi pour cette décision. Les mentions d'attente ci-dessous décrivent
l'archivage initial ; maquettes détaillées et essais habitants restent distincts.

La demande suivante autorise spécification et implémentation :
[réalisation locale et preuves E73-WL](../../../specifications/epic-73-animation-et-ou-coffrets/workshop-live-20261118.md),
avec limites humaines explicites.

- Date locale : 2026-11-18 (Europe/Paris)
- URL : https://test-live.localeo.city
- Branche documentaire : main
- Commit documentaire initial : 7164846f266cc0c073dc0c4642c569d9b8c6676c
- Objectif : explorer les parcours mobiles des animations, des lots et du calendrier avant le workshop UX.
- Statut : **PARTIEL** ; étapes 1 à 3 produites avec limites, étape 4 préparée sans décision utilisateur, étape 5 archivée. B1/C1/D1/E1 restent en attente ; aucune orientation validée par l’utilisateur.
- Répertoire de travail : D:\OneDrive\Bureau\Documents\GitHub\localeo-projet\docs\ux-workshops\2026-11-18

## Bilan de l’étape 1

- Commune de référence : Bouliac.
- Dépôt applicatif consulté en lecture seule : `localeo-marketplace`, branche `main`, commit `db4dc57e6b2fd78f83a9d2981d181c0eb17c582d`.
- Navigateur : Chromium via Playwright, vues mobiles 320 × 844, 390 × 844 et 430 × 844.
- Captures : 15 PNG dans `visuels/captures-avant/`, refaites après suppression des premières captures conformément à la demande.
- Livrables : `observations/cartographie-parcours.md`, `inventaire-ecrans.md`, `observations-factuelles.md`, `limitations.md`.
- À la clôture de l’étape 1, aucun workshop, aucune maquette et aucune validation habitant n’avaient été commencés.

## Bilan de l’étape 2 — workshop simulé

- Date locale : 18 novembre 2026 ; même dossier et même commune, Bouliac.
- Instruction complète recopiée sans modification dans [prompts/02-workshop.md](prompts/02-workshop.md).
- Six ateliers, six experts et six habitants fictifs ; aucun entretien ou test habitant réel.
- Douze orientations, 144 votes nominatifs simulés : six adoptées et six rejetées ; seuil fixe de sept voix sur douze.
- Recommandation : **GO SOUS CONDITIONS**. Les parcours QR positif, participation confirmée, carnet rempli et utilisation des lots restent à éprouver ; les contrôles d’accessibilité restent à exécuter.
- Quatre orientations prioritaires pour une ouverture large : B1, C1, D1, E1. A1 et F1 restent adoptées en P2 ; aucun P0 prouvé.
- Nuance des preuves : l’accueil à 430 px a été capturé pendant son chargement ; les superpositions de barre fixe dans les captures longues ne démontrent pas un blocage après défilement. Détails dans le compte rendu.
- Dépôt modifié : `localeo-projet` uniquement, dans ce dossier. Aucune modification applicative, aucune maquette, aucun commit, push ou déploiement.

Livrables :

- [Rapport exécutif](workshop/rapport-executif.md) : notes heuristiques, matrice habitants/parcours, recommandation.
- [Compte rendu](workshop/compte-rendu.md) : avis individuels, débats et décisions des six ateliers.
- [Votes et arbitrages](workshop/votes-et-arbitrages.md) : registre nominatif et décomptes.
- [Backlog UX](workshop/backlog-ux.md) : six orientations adoptées et critères proposés.
- [Orientations rejetées](workshop/orientations-rejetees.md) : alternatives et arguments minoritaires.
- [Quick wins](workshop/quick-wins.md) : trois actions limitées rattachées aux orientations adoptées.

À la fin de l’étape 2, les prompts 00, 03, 04 et 05 restaient « PROMPT À FOURNIR ». Les prompts 03 et 04 ont depuis été complétés ; 00 et 05 restent à fournir.

Contrôles documentaires de fin d’étape :

- `py -3 scripts/check_guidance.py` : succès, 100 guides, 1 351 liens, aucune erreur ni avertissement.
- Contrôle ciblé : prompt 02 identique octet par octet au fichier fourni ; 12 rôles, 144 votes, totaux et seuils cohérents ; six livrables, 55 liens locaux valides, 15 captures conservées.
- Tests applicatifs et essais habitants : non exécutés à cette étape documentaire ; aucune validation fonctionnelle supplémentaire revendiquée.

## Bilan de l’étape 3 — propositions visuelles

- Commune : **Bouliac** ; même exécution datée.
- [Instruction complète](prompts/03-maquettes.md) enregistrée.
- Périmètre exclusif : **B1, C1, D1, E1**, quatre P1 adoptées. Aucun P0 établi ; A1/F1 P2 hors maquettes.
- **14 planches HTML isolées**, exportées en **28 PNG APRÈS** (fenêtre et contenu complet), plus les captures de contrôle. Les **15 captures réelles AVANT** de Bouliac sont conservées.
- [Galerie comparative](visuels/comparatif-avant-apres.html) : côte à côte sur ordinateur, bascule sur mobile, quatre orientations et leurs états ; identifiant, priorité, vote, bénéfice attendu, effort qualitatif M.
- [Référence de conception](visuels/reference-maquettes.md) : correspondances avant/après, conditions d’état, données, comportements attendus et fonctions conservées.
- [Revue contradictoire](visuels/revue-contradictoire.md) : six experts et six habitants fictifs, avis distincts et cinq questions habitants. Revue des contenus transmis ; inspection visuelle par l’agent principal. Aucun test habitant réel.
- Ajustements : incertitude d’inscription explicitée, « Bon annulé » pour REVOQUE, retrait absent des états non utilisables, voie de retour depuis un QR invalide sans inscription. Aucun changement substantiel de périmètre, donc aucun nouveau vote ; arbitrages complémentaires enregistrés.
- [Backlog](workshop/backlog-ux.md) enrichi de références vers les maquettes ; votes d’origine conservés.
- [Contrôles techniques locaux](visuels/controles/controle-technique.md) : 42 lectures à 320/390/430 px sans débordement, quatre planches avec texte agrandi, galerie à quatre largeurs, clavier ciblé et palette mesurée. Ces preuves concernent les maquettes, sans audit de conformité de l’application.

### Limites conservées

C1 ne dispose pas d’un AVANT avec lot attribué : l’état vide réel n’est pas un équivalent. Les lots et coordonnées APRÈS sont fictifs ; les confirmations B1 et les états d’erreur illustratifs ne sont pas des parcours réels testés. QR valide et accès personnels de test restent nécessaires à la recette. Les boutons métier des planches sont inertes.

B1/C1/E1 restent conditionnés à la vérification des écarts avant retouche. Les gains de compréhension et les préférences sont des hypothèses ; aucune validation terrain n’a eu lieu.

Seul `localeo-projet` est modifié pour cette étape, dans ce dossier. Aucun code applicatif, contrat, migration, jeu de démonstration, commit, push ou déploiement modifié ou exécuté. L’étape de validation habitant n’est pas commencée.

**Arrêt à l’étape 3 : validation utilisateur attendue.**

Ce point d’arrêt historique est suivi par la préparation de l’étape 4 ci-dessous ; la demande de revue ne constitue pas une validation des maquettes.

Contrôles documentaires de l’étape 3 : `py -3 scripts/check_guidance.py` réussi (100 guides, 1 357 liens, aucune erreur ni avertissement) ; 171 références locales du dossier contrôlées sans cible manquante ; instruction 03 comparée au texte fourni, identique hors fins de ligne ; inventaire confirmé de 15 captures AVANT, 14 HTML et 28 PNG APRÈS. Le dépôt applicatif consulté reste propre au contrôle Git.

## Étape 4 — revue prête, décisions attendues

- Préparée le 18 novembre 2026, Europe/Paris, dans le même dossier et pour Bouliac.
- [Instruction complète](prompts/04-validation.md) enregistrée.
- [Revue pour décision](validation/revue-pour-decision.md) : quatre P1, missions, problèmes, votes, captures, maquettes, bénéfices, efforts et risques ; points critiques et réserves minoritaires conservés. Aucun P0 établi.
- [Registre des décisions utilisateur](validation/decisions.md) créé : B1/C1/D1/E1 en attente, sans date de décision ni maquette déclarée validée.
- [Empreintes des maquettes soumises](validation/maquettes-soumises.json) enregistrées pour identifier précisément la version présentée.
- Choix proposés : VALIDÉE, REFUSÉE, À RÉVISER ou REPORTÉE, avec commentaires et conditions éventuelles.
- Aucun vote simulé transformé en décision utilisateur. A1/F1 P2 restent hors de cette revue.
- La liste des travaux applicatifs potentiels sera préparée après les décisions, par catégorie. Aucun développement exécuté ; une instruction explicite séparée reste nécessaire.

**Étape 4 en cours : attente des décisions utilisateur.** La validation finale n’est pas acquise. Seuls les livrables documentaires de ce dossier sont modifiés.

Contrôles de préparation : instruction 04 comparée au texte fourni, identique hors fins de ligne ; 55 références locales de la revue/du registre/du README vérifiées sans cible manquante ; empreintes de 48 fichiers de présentation enregistrées ; `py -3 scripts/check_guidance.py` réussi (100 guides, 1 361 liens, aucune erreur ni avertissement).

## Étape 5 — archivage de l’état partiel

- Exécution commencée le **18 novembre 2026**, heure initiale exacte non relevée ; archivage terminé le **18 novembre 2026 à 10:08 (Europe/Paris)**. URL analysée : `https://test-live.localeo.city`. Branche documentaire `main`, commit initial et courant `7164846f266cc0c073dc0c4642c569d9b8c6676c` ; dépôt Marketplace consulté en lecture seule au commit `db4dc57e6b2fd78f83a9d2981d181c0eb17c582d`.
- Modèle : famille GPT-6 indiquée par l’environnement Codex ; identifiants exacts et niveaux de raisonnement des différentes étapes et sous-agents **non connus**. Aucun niveau n’est inventé.
- Version du protocole : instructions archivées [01](prompts/01-exploration.md), [02](prompts/02-workshop.md), [03](prompts/03-maquettes.md), [04](prompts/04-validation.md) et [05](prompts/05-archivage.md), plus [compléments Bouliac et remplacement des captures](prompts/01-complements.md). Le prompt global [00](prompts/00-protocole-global.md) reste **PROMPT À FOURNIR** : son texte exact manque.
- Parcours vérifiés : accueil/carnet vide, Découvrir Bouliac et ses trois fiches, formulaire d’inscription non soumis, QR invalide, participations et lots vides, récupération non envoyée, programme daté, redirection calendrier et retour navigateur ; détails et preuves dans [observations](observations/observations-factuelles.md) et [captures AVANT](visuels/captures-avant/01-accueil-320x844.png). Vues mobiles 320/390/430 px.
- Limites majeures : QR valide, inscription confirmée, participation personnelle, lot attribué/remis et test habitant réel absents ; aucune validation de charge ou conformité d’accessibilité générale. [Limites détaillées](observations/limitations.md).
- Résultats : **12 orientations proposées, 6 adoptées, 6 rejetées ; aucun P0 établi, 4 P1, 2 P2, aucun P3.** Votes simulés par 12 rôles au seuil de 7 voix ; [registre](workshop/votes-et-arbitrages.md), [backlog](workshop/backlog-ux.md), [rapport exécutif](workshop/rapport-executif.md).
- Visuels : 15 PNG AVANT réels, 14 HTML et 28 PNG APRÈS ; [manifeste des fichiers et empreintes](synthese/manifeste-visuels.md), [galerie comparative](visuels/comparatif-avant-apres.html), [référence](visuels/reference-maquettes.md) et [revue simulée](visuels/revue-contradictoire.md).
- Validation : [registre](validation/decisions.md) présent ; **B1/C1/D1/E1 EN ATTENTE**, sans accord utilisateur et sans maquette déclarée validée. A1/F1 P2 hors revue finale.
- [Inventaire des livrables et manques](synthese/inventaire-archivage.md) ; [absence de précédent](synthese/comparaison-precedent.md) ; [prompt autonome de relance](prompts/RELANCER-WORKSHOP.md).
- Roadmap canonique existante, mais aucun report de ce backlog UX non validé. **Plan de tests utilisateurs dédié manquant** ; les critères de recette ne sont pas des résultats de terrain.

**L’archivage est achevé ; le workshop demeure partiel tant que les décisions utilisateur et les preuves personnelles manquent.** Aucun développement autorisé par cet archivage.

Contrôles finaux d’archivage : fichiers du workshop accessibles, 15 captures AVANT et 14 maquettes HTML/28 PNG APRÈS référencées dans le [manifeste](synthese/manifeste-visuels.md) ; 289 liens locaux contrôlés sans cible manquante ; galerie et 14 maquettes ouvertes via Playwright, quatre orientations et bascule mobile fonctionnelles, sans erreur de page ni ressource manquante. `py -3 scripts/check_guidance.py` : 100 guides, 1 383 liens, zéro erreur ou avertissement. Les quatre dépôts applicatifs restent propres au contrôle Git. Aucun dossier antérieur à celui-ci n’existe dans `docs/ux-workshops/`.
