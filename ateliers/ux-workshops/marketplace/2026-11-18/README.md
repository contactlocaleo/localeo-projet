# Exploration UX Marketplace Localeo

- Date locale : 2026-11-18 (Europe/Paris)
- Heure de clôture documentaire : 19:10 (Europe/Paris)
- URL : https://test-coffrets.localeo.city
- Branche Git documentaire : main
- Commit Git documentaire au début et à la fin : a79fa4e935e0560d4ea19ef6e98e4f72e44d77f1 (dossier encore non suivi par Git)
- Modèle connu : Codex basé sur GPT-6 pour cette session d'archivage ; variante et niveau de raisonnement non exposés. Modèles et niveaux des étapes antérieures non consignés.
- Version du protocole : relance v1.0 créée à l'étape 5 ; prompt global historique 00 non fourni
- Objectif : audit des parcours publics, workshop contradictoire et propositions visuelles
- Statut final : archivé localement **avec réserve** sur le prompt 00 manquant ; sept orientations P0/P1 validées par réponse globale du propriétaire le 2026-11-18 ; aucune implémentation

Les prompts complets reçus sont archivés dans [`prompts/01-exploration.md`](prompts/01-exploration.md), [`prompts/02-workshop.md`](prompts/02-workshop.md), [`prompts/03-maquettes.md`](prompts/03-maquettes.md), [`prompts/04-validation.md`](prompts/04-validation.md) et [`prompts/05-archivage.md`](prompts/05-archivage.md). [`prompts/00-protocole-global.md`](prompts/00-protocole-global.md) reste un marqueur car aucun prompt global distinct n'a été fourni. La [provenance et les corrections d'archive](synthese/notes-protocole.md) en donnent le détail. Le [prompt de relance autonome](prompts/RELANCER-WORKSHOP.md) est une nouvelle version v1.0, pas une reconstitution du 00.

Les constats sont dans [`observations/`](observations) : [cartographie](observations/cartographie-parcours.md), [inventaire des écrans](observations/inventaire-ecrans.md), [observations factuelles](observations/observations-factuelles.md), [frontière Stripe](observations/parcours-achat-stripe.md) et [limites](observations/limitations.md). Les 27 captures sont dans [`visuels/captures-avant/`](visuels/captures-avant).

L’exploration publique s’est faite avec Chromium automatisé sur 320, 390, 430 et 1440 px pour l’accueil, puis principalement 390 et 1440 px sur les parcours. Le point d’arrêt de l’achat est **avant la soumission du formulaire**, car cet appel crée un achat côté backend. Aucun paiement ni inscription n’a été exécuté.

L'étape 2 est un **workshop contradictoire simulé sur ces preuves**, avec cinq expertises et sept profils fictifs. Aucun utilisateur ni commerçant réel n'a été interrogé ; réactions, votes et notes heuristiques ne sont pas des mesures. Livrables : [rapport exécutif](workshop/rapport-executif.md), [compte rendu des sept ateliers](workshop/compte-rendu.md), [votes et arbitrages](workshop/votes-et-arbitrages.md), [backlog UX](workshop/backlog-ux.md), [orientations non retenues](workshop/orientations-rejetees.md) et [actions rapides](workshop/quick-wins.md). La décision proposée est **GO SOUS CONDITIONS**, dont la recette sûre du passage Stripe et le contrôle des contenus effectivement publiés.

L'étape 3 présente [la galerie comparative AVANT / APRÈS](visuels/comparatif-avant-apres.html), sept [maquettes documentaires](visuels/maquettes-apres/README.md) pour les orientations adoptées P0/P1, et la [revue contradictoire simulée](workshop/arbitrages-maquettes.md). Les captures AVANT sont celles de l'étape 1, sans retouche. O‑04 (P2) n'est pas maquettée ; O‑08 est une carte de recette et non une fausse page Stripe. Les propositions de texte et de prestation demandent une validation métier et commerçant avant implémentation. Aucune application, commande ou session de paiement n'a été modifiée ou créée. **Validation utilisateur des maquettes attendue.**

L'étape 4 met à disposition le [dossier de décision des sept orientations](validation/dossier-decision.md), les [décisions enregistrées](validation/decisions.md) et le [backlog d'implémentation potentiel](validation/backlog-implementation-potentiel.md). Le propriétaire a répondu globalement « VALIDÉE » le 18 novembre 2026, après la présentation des sept orientations P0/P1 ; les sept statuts sont enregistrés comme **VALIDÉE**, sans commentaire ni condition supplémentaire individuelle. Les votes simulés restent distincts de cette décision. Aucune implémentation, recette Stripe ou mise en production n'en découle automatiquement.

## Synthèse de l'exécution

- **Parcours vérifiés :** A première impression, B recherche et coffrets, C communes et commerçants, D animations et agenda Live, E achat jusqu'avant soumission, F confiance et cadeau. Voir la [cartographie](observations/cartographie-parcours.md).
- **Limites :** Stripe, retour post-paiement, inscription Live, erreurs forcées et audit complet d'accessibilité non vérifiés ; contenus observés en TEST seulement. Voir les [limites détaillées](observations/limitations.md).
- **Orientations :** 10 proposées au workshop simulé ; 8 adoptées à 7 voix ou plus ; parmi elles, 7 P0/P1 maquettées puis **VALIDÉES** par réponse globale du propriétaire. O-04 reste P2, hors de cette validation ; O-09 rejetée et O-10 non adoptée.
- **Suite documentaire :** [roadmap UX](synthese/roadmap-ux.md), [plan de tests avec de vrais utilisateurs](synthese/plan-tests-utilisateurs.md), [contrôle final](validation/controle-final.md). Aucun workshop marketplace précédent n'existe dans ce workspace, donc aucune comparaison historique n'a été créée.
- **Statut :** archive locale avec réserve sur le prompt 00 ; dossier non commité/non poussé. Aucun achat réel, aucune donnée bancaire et aucune modification applicative.

Vérifications : [contrôles visuels Chromium/Playwright](validation/revue-visuelle.md) et [contrôle final](validation/controle-final.md) ; `py -3 scripts/check_guidance.py` réussi (110 guides, 1 627 liens locaux, 0 erreur, 0 alerte) ; `py -3 scripts/sync_documentation.py --check-sources` réussi (151 documents). Dépôts applicatifs consultés en lecture seule : `localeo-marketplace` et `localeo-backend`. Aucun commit, push ou déploiement pour ce dossier.
