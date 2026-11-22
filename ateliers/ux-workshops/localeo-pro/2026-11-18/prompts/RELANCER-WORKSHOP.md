# RELANCER LE WORKSHOP UX LOCALEO PRO

Version 1.0 — préparée le 18 novembre 2026. **Prompt autonome pour une nouvelle exécution ; non exécuté dans l’archive qui le contient.**

Tu dois conduire une nouvelle exploration et un workshop UX de Localeo Pro, carnet opérationnel du commerçant participant aux animations de sa commune, puis soumettre les orientations à ma validation. Ne modifie aucun code applicatif, contrat, donnée réelle ou exécution historique. Ne développe, ne commite, ne pousse et ne déploie rien automatiquement.

## 1. Retrouver le protocole et préserver l’historique

Depuis le dépôt documentaire Localeo, lis le README et les AGENTS.md applicables. Examine les exécutions dans `docs/ux-workshops/localeo-pro/`, triées par date locale et suffixe numérique. Identifie la plus récente, son statut, son protocole et ses décisions ; ne confonds pas un workshop d’une autre application avec un précédent Pro.

Lis les six fichiers `prompts/00-protocole-global.md` à `prompts/05-archivage.md`, la provenance, le rapport exécutif, le backlog, les votes, les observations, les limites et le registre des décisions du dernier dossier. Si un fichier manque ou n’est pas une transcription exacte, signale-le sans inventer d’historique. Identifie la dernière version documentée, consigne celle utilisée et les adaptations nécessaires. Le présent prompt couvre l’ensemble du cycle de relance ; les archives restent des références, leurs anciens marqueurs d’arrêt ne valent pas nouvelle décision utilisateur.

Crée un nouveau dossier avec la date locale : `docs/ux-workshops/localeo-pro/YYYY-MM-DD/`. S’il existe, ajoute `-02`, puis `-03`, etc. Ne réutilise ni n’écrase un ancien dossier. Crée `prompts/`, `observations/`, `workshop/`, `visuels/captures-avant/`, `visuels/maquettes-apres/`, `validation/` et `synthese/`. Relève date/heure/fuseau, branche et commit du dépôt documentaire et des applications inspectées, version déployée si observable, modèle/niveau de raisonnement seulement s’ils sont réellement connus.

Archive ce prompt intégral dans la nouvelle exécution. Pour chaque phase, archive le texte complet réellement appliqué et sa provenance, avec les adaptations datées. Si le même prompt pilote plusieurs phases, l’indiquer explicitement ; ne fabriquer aucun prompt historique séparé. Remplace tous les identifiants par `[CONFIDENTIEL]`. Conserve les versions antérieures à toute révision.

## 2. Accès autorisé et périmètre

URL Pro de référence lors de l’exécution du 18 novembre 2026 : `https://test-commercant.localeo.city`. L’adresse `https://test-animations.localeo.city` avait ouvert le portail organisateur. Vérifie la cible actuelle dans les sources canoniques avant d’utiliser un compte ; signale tout changement de portail.

Les identifiants ne sont pas inclus dans ce prompt. Demande le compte de test autorisé s’il n’a pas été fourni dans la session. Utilise exclusivement les identifiants fournis pour cette exécution, jamais un secret retrouvé ailleurs. N’enregistre ni login, ni mot de passe, ni jeton, ni valeur QR dans les fichiers, logs, URL, captures ou historique versionné. Prends les captures de connexion avant saisie ou après effacement des champs.

Quatre missions : première impression/prise en main ; validation des participations ; notifications/préparation ; kit et logistique. Coffrets, reversements et statistiques avancées sont exclus, sauf perturbation concrète de la navigation prioritaire.

## 3. Explorer réellement

Utilise Playwright ou un navigateur automatisé, d’abord sur smartphone puis sur ordinateur. Distingue mobile émulé et téléphone physique. Relève dimensions, navigateur, version et contexte. Explore : connexion, accueil, détail d’animation, accès scanner, QR et confirmation, erreurs/doublons, boîte et réception des notifications, préparation, kit/supports/consignes, retour dans l’application.

Les validations et autres écritures ne sont permises qu’avec données dédiées de test et autorisation explicite pour ces effets. Ne valide aucune participation réelle, n’envoie aucune notification à un véritable commerçant non participant et ne fais aucune action destructive. Inspecte les effets éventuels du téléchargement du kit avant clic. Si un QR, un état, une autorisation ou un appareil manque, documente « non exécuté » ; ne simule pas sa réussite. Un rechargement immédiat n’est pas un retour après plusieurs jours.

Si les dépôts sont disponibles, inspecte en lecture seule routes, composants, scan, confirmation/reçu, notifications, préparation et kit. Distingue implémenté, accessible, réellement vérifié et hypothétique. Ne réimplémente aucune règle métier dans un prototype.

Produis `observations/cartographie-parcours.md`, `inventaire-ecrans.md`, `observations-factuelles.md` et `limitations.md`. Attribue un ID stable à chaque constat et la qualification **OBSERVÉ**, **DÉDUIT** ou **HYPOTHÈSE**, avec preuve datée. Enregistre exclusivement des captures réelles dans `visuels/captures-avant/` ; indique les artefacts de capture longue sans en déduire un défaut non observé.

## 4. Simuler le workshop contradictoire

Prends douze rôles fictifs, tous explicitement simulés : cinq experts (UX senior, accessibilité, PM B2B, opérations terrain, researcher/facilitateur) et sept commerçants (Martine, fleuriste 63 ans très peu à l’aise ; Patrick, boulanger 57 ans pressé/interrompu ; Nadia, salon 44 ans anticipant la préparation ; Julien, restaurant 35 ans exigeant rapidité/fiabilité ; Claire, boutique 51 ans occasionnelle ; Hugo, commerce spécialisé 29 ans très à l’aise ; Isabelle, librairie 48 ans usage intermittent). Ce ne sont pas des personnes interrogées.

Avant débat, chacun formule indépendamment ses observations à partir des mêmes preuves. Organise sept ateliers : première impression, validation, notifications, préparation, kit/logistique, situations de service, simplification/adoption. Pour chacun : preuves, douze avis individuels, débat, points forts, difficultés, orientations et votes. Conserve les désaccords et les incertitudes. Ne prétends pas qu’un rôle a vu une image si seule une transcription lui était accessible.

Chaque rôle a une voix, facilitateur compris sans voix supplémentaire. Vote nominatif argumenté pour/contre/abstention : **7 à 12 pour = ADOPTÉE ; 6 = NON ADOPTÉE ; 0 à 5 = REJETÉE**. Les abstentions ne réduisent jamais le seuil. Vérifie douze votants uniques par orientation et les totaux. Les risques critiques restent visibles quel que soit le vote.

Priorise P0 (bloque une action essentielle ou risque opérationnel majeur), P1 (friction importante ou risque significatif), P2 (amélioration différable), P3 (confort/évolution secondaire). Ne crée aucun P0 sans preuve justifiée. Pour chaque orientation : ID, mission, constat/source, conséquence, solution, bénéfice hypothétique, critères, effort S/M/L/XL, confiance, priorité et vote.

Produis les six fichiers `workshop/rapport-executif.md`, `compte-rendu.md`, `votes-et-arbitrages.md`, `backlog-ux.md`, `orientations-rejetees.md`, `quick-wins.md`. Le rapport inclut sept notes heuristiques sur 10 motivées (impression, navigation, validation, notifications, préparation, kit, accessibilité), la matrice des commerçants/missions, les priorités avant ouverture à 500 commerces et une recommandation GO/GO SOUS CONDITIONS/NO GO clairement distincte de ma décision.

## 5. Produire les comparatifs visuels

Travaille uniquement sur les orientations P0/P1 adoptées avec au moins sept voix. Réutilise l’identité et les composants actuels, privilégie les optimisations ciblées, isole tous les prototypes du code applicatif. Ne produis pas artificiellement un écran pour un sujet non adopté.

Pour chaque orientation, associe une capture AVANT réelle à une proposition APRÈS explicitement étiquetée. Si la preuve manque, tente de la produire dans la cible autorisée ; si cela reste impossible, expose la limite sans reconstruire un faux AVANT. Illustre les états utiles du scanner, notifications, préparation et kit selon le périmètre voté.

Crée `visuels/comparatif-avant-apres.html`, consultable localement et responsive : côte à côte sur ordinateur, bascule sur mobile. Affiche ID, priorité, problème, AVANT/APRÈS, bénéfice, effort, vote et limites. Conserve maquettes et sources dans `visuels/maquettes-apres/`. Vérifie rendu, liens, images et commandes de comparaison.

Soumets les propositions aux douze rôles simulés : compréhension, geste immédiat, temps potentiel, erreur, préférence et difficulté restante. Conserve les objections. Si l’orientation change substantiellement, organise un nouveau vote nominatif au seuil de sept. Trace les arbitrages, versions de maquettes et références dans le backlog. Aucun vote fictif n’autorise un développement.

## 6. Comparer au précédent et préparer la décision

Compare uniquement avec des exécutions Localeo Pro : corrigé réellement vérifié avec nouvelle preuve ; persistant réobservé ; nouveau constat ; non revérifié ; priorité modifiée ; notes heuristiques avec confiance et protocole ; décisions utilisateur validées/reportées/à réviser/refusées. Une disparition visuelle, une maquette ou une fonction vue dans le code ne prouve pas une correction. Ne transporte pas une ancienne validation vers une proposition changée.

Crée `synthese/comparaison-precedent.md`, ou indique clairement l’absence de précédent. Préserve tous les anciens fichiers. Prépare `synthese/roadmap-ux.md` : avant lancement seulement P0/P1 explicitement validées ; après premiers retours P2 et ajustements ; futures P3 adoptées à soumettre. Si aucune orientation n’est validée, la première catégorie reste vide ; ne réactive pas les solutions rejetées.

Prépare `synthese/plan-tests-commercants.md` avec au moins cinq scénarios de terrain, cinq commerçants réels à recruter dont au moins deux peu familiers du numérique, consignes neutres, critères, observations, jeu de test autorisé et reprise différée réellement planifiée. Ce plan n’est pas une campagne exécutée.

Présente chaque P0/P1 adoptée avec problème, conséquence, mission, vote, effort, AVANT/APRÈS, bénéfice et dépendances. Expose séparément les risques critiques, y compris les besoins derrière les solutions rejetées. Initialise `validation/decisions.md` à **EN ATTENTE** sauf décision explicite connue pour cette nouvelle proposition. Permets les choix VALIDÉE, REFUSÉE, À RÉVISER, REPORTÉE avec commentaire, conditions et date connue. Prépare une synthèse et un backlog potentiel sans développement.

## 7. Archiver, restituer et attendre

Finalise le README : date/heure, URL, branches/commits, modèles et niveaux connus seulement, version du protocole, parcours réellement vérifiés, limites, nombres proposés/adoptés/P0-P1, décisions, liste des livrables et statut terminé/partiel/interrompu. Vérifie intégrité, liens, images, prompts, votes, absence de secrets et préservation des dossiers historiques. Produis des empreintes SHA-256 sans inclure de secrets ni données de session ; documente les exclusions.

Présente le dossier, les orientations à décider, les preuves manquantes et le prompt de relance. **Arrête-toi et attends ma validation explicite.** Si je réponds partiellement, conserve les autres lignes en attente. Après mes décisions, enregistre-les fidèlement, actualise la synthèse et le README, puis arrête-toi. Aucune implémentation, publication ou validation automatique ne découle de ce workshop.
