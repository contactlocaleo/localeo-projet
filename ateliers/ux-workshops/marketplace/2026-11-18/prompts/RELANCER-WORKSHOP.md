# RELANCER UN WORKSHOP UX MARKETPLACE LOCALEO

**Protocole de relance v1.0 — créé le 18 novembre 2026.** Cette instruction est autonome pour une nouvelle exécution. Elle ne reconstitue pas le `00-protocole-global.md` absent de l'exécution du 18 novembre. La marketplace publique est un parcours d'expériences locales chez plusieurs commerçants d'une commune, **pas** un colis matériel ni une carte cadeau générique.

## 1. Identifier le protocole et créer une exécution neuve

1. Depuis le dépôt documentaire `localeo-projet`, lire son `README.md` et les instructions AGENTS applicables. Identifier le dernier répertoire daté sous `docs/ux-workshops/marketplace/` ; lire son README, ses limites, sa provenance de protocole et ses décisions. Ce protocole v1.0 est la base de relance si aucune version ultérieure explicite n'existe.
2. Déterminer la date locale Europe/Paris (`YYYY-MM-DD`). Créer `docs/ux-workshops/marketplace/YYYY-MM-DD/` ; si une exécution distincte existe ce jour-là, ajouter `-02`, `-03`, etc. Créer `prompts/`, `observations/`, `workshop/`, `visuels/captures-avant/`, `visuels/maquettes-apres/`, `validation/` et `synthese/`. **Ne modifier aucun ancien workshop.**
3. Consigner dans le nouveau README date/heure, URL, branche/commit Git de chaque dépôt consulté, modèle et niveau de raisonnement seulement s'ils sont connus, version du protocole, objectif et statut.
4. Archiver **le texte complet réellement utilisé**. Si cette seule instruction gouverne toute la relance, la copier intégralement dans `prompts/00-protocole-global.md` et, pour la traçabilité demandée, dans `01-exploration.md` à `05-archivage.md`, avec une note séparée précisant qu'il s'agit du même prompt global, sans prompts d'étape distincts. Si des instructions d'étape distinctes sont reçues, archiver chacune à l'identique et marquer les autres comme non fournies. Ne jamais inventer un prompt historique.

## 2. Réexplorer le site réel

Explorer d'abord sans authentification `https://test-coffrets.localeo.city`, ou l'URL explicitement fournie pour la nouvelle exécution. Utiliser un navigateur automatisé, en priorité à 320, 390, 430 et 1440 px. Parcourir : arrivée, proposition de valeur, recherche/commune, page communale, liste et fiche coffret, garantie et exemples, commerçant et liens, animations et agenda Live, détail d'animation, cadeau, récapitulatif et frontière de paiement. Relever menus, filtres, retours, états vides, erreurs, chargements et prix/conditions lorsque l'observation est sûre. Demander un compte de test autorisé si un parcours requis nécessite une connexion.

Conserver des captures **réelles** datées dans `visuels/captures-avant/` et un inventaire d'écrans. Créer dans `observations/` : cartographie des parcours, inventaire, observations factuelles, analyse achat/Stripe et limites. Marquer chaque constat **OBSERVÉ**, **DÉDUIT** (code) ou **HYPOTHÈSE**. Distinguer TEST et production. Si les dépôts applicatifs sont accessibles, lire routes, pages, navigation, calendrier, commande et création de session Stripe en lecture seule ; ne pas confondre code et comportement observé.

**Frontière d'achat :** aucun paiement, aucune donnée bancaire réelle, aucune confirmation de commande. Avant toute soumission ou redirection, vérifier si l'action crée un achat, une réservation ou une session à effets métier. Si oui, s'arrêter **avant** l'action ; analyser le mécanisme par le code. Une recette Stripe n'a lieu que dans un protocole distinct après confirmation explicite de l'innocuité des effets métier. Ne pas générer d'achat réel.

## 3. Rejouer le workshop contradictoire

Sur les captures et observations, organiser une **simulation sur pièces**, clairement distincte d'une recherche auprès de vrais utilisateurs, avec douze rôles : cinq experts (UX e-commerce, conversion, Product Manager marketplace, accessibilité/contenu, UX Researcher) et sept profils variés (habitants dont personne peu familière du numérique, acheteur cadeau, visiteur extérieur, usager d'animations, utilisateur mobile habitué, deux commerçants). Les réactions fictives ne sont jamais présentées comme des mesures.

Traiter sept ateliers : A première impression ; B commune ; C commerçants ; D compréhension/choix du coffret ; E animations/calendrier ; F achat/confiance jusqu'à la frontière Stripe ; G simplification/attractivité. Pour chaque atelier, montrer les écrans observés, avis individuels, objections et points forts/faibles. Conserver les désaccords.

Chaque rôle dispose d'une voix par orientation. Enregistrer **les douze votes individuels et leurs arguments**. Seuil fixe : 7–12 favorable = ADOPTÉE ; 6 = NON ADOPTÉE ; 0–5 = REJETÉE ; une abstention ne réduit pas le seuil. Prioriser P0 bloquant, P1 indispensable, P2 différable, P3 secondaire. Pour chaque orientation, documenter ID, parcours, problème, preuve/hypothèse, conséquence, solution, bénéfice, critères d'acceptation, effort S/M/L/XL, priorité, confiance et vote. Les problèmes critiques demeurent documentés même sans vote.

Créer `workshop/rapport-executif.md`, `compte-rendu.md`, `votes-et-arbitrages.md`, `backlog-ux.md`, `orientations-rejetees.md` et `quick-wins.md`. Le rapport comporte neuf notes heuristiques /10 justifiées (première impression, concept coffret, communes, commerçants, fiche coffret, calendrier, achat, confiance, accessibilité mobile), une matrice profils × parcours, les cinq améliorations principales **si elles sont justifiées**, et GO / GO SOUS CONDITIONS / NO GO. Une note n'est ni une mesure de conversion ni un audit normatif.

## 4. Produire les maquettes autorisées par le vote

Maquetter seulement les orientations adoptées à au moins 7/12 et classées P0/P1. Pour chacune, relier une capture AVANT réelle à une proposition APRÈS dans `visuels/maquettes-apres/`, sans prétendre que l'APRÈS existe dans l'application. Respecter les codes Localeo, les composants existants, la lisibilité mobile et le sens d'un coffret de **moments à vivre sur place**. Ne pas inventer une page Stripe observée. Une orientation qui n'est qu'une porte de recette peut recevoir une carte de contrôle clairement non produit.

Créer `visuels/comparatif-avant-apres.html` : ID, priorité, parcours, problème, AVANT, APRÈS, bénéfice, effort et vote ; colonnes côte à côte sur ordinateur, bascule clavier/souris avant/après sur mobile. Faire une revue contradictoire simulée des cinq experts et sept profils, conserver objections, et revoter si la proposition change substantiellement l'orientation. Mettre les références visuelles dans le backlog.

## 5. Demander et enregistrer la décision du propriétaire

Préparer `validation/dossier-decision.md` avec, pour chaque P0/P1 adoptée, problème, conséquence hypothétique, vote simulé, AVANT, APRÈS, bénéfice, effort, risques et dépendances ; séparer les risques critiques. Initialiser `validation/decisions.md` à **EN ATTENTE**, puis demander au propriétaire **VALIDÉE / REFUSÉE / À RÉVISER / REPORTÉE** pour chaque orientation. Ne pas assimiler vote simulé et validation. N'inscrire une décision que sur réponse explicite, avec date si connue, commentaire, conditions et maquette. Préparer un backlog potentiel séparant ces statuts. **Aucune implémentation automatique, aucun achat, aucun paiement.**

## 6. Comparer, archiver et arrêter

Créer `synthese/roadmap-ux.md` (avant lancement P0/P1 validées, après retours P2, futur P3 sans planifier une orientation rejetée) et `plan-tests-utilisateurs.md` avec au moins six scénarios à mener auprès de **vraies** personnes : première visite, commune, commerçant, coffret, calendrier et achat arrêté avant soumission. Pour chaque scénario, préciser consigne neutre, observations et critère de réussite ; inclure des personnes peu familières du numérique et des commerçants.

Comparer à l'exécution précédente si elle existe : corrigé **seulement si vérifié**, persistant, nouveau, priorité, notes heuristiques et décisions. Ne pas modifier l'archive précédente. Vérifier intégrité des prompts réellement fournis, fichiers, captures, maquettes, liens, absence de modification applicative et absence de transaction. Documenter tout manque ou changement de consigne. Exécuter les contrôles documentaires proportionnés du dépôt. Mettre le README à jour avec statut final, parcours, limites, comptes d'orientations, décisions, modèle/niveau connus et liens.

Présenter le nouveau répertoire, le statut, les manques, la comparaison et les décisions en attente. **Attendre la validation du propriétaire avant toute suite** ; ne pas implémenter, pousser, déployer ou payer dans le cadre de ce workshop.
