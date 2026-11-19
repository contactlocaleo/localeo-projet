# RELANCER LE WORKSHOP UX LOCALEO CRM

**Protocole de relance v1.0 — créé le 19 novembre 2026 pour une exécution future.** Ce document est une nouvelle consolidation ; il ne prétend pas être le protocole global utilisé en novembre. L’exécution source avait des prompts séquentiels 01–05 et aucun protocole global distinct fourni.

## Mission et périmètre autorisé

Prépare un workshop UX complet sur Localeo CRM pour une petite équipe prospectant communes, associations de commerçants et professionnels : comprendre la prospection, connaître les actions, qualifier les prospects, gérer les rendez-vous et collaborer sans oubli. Privilégie simplicité et efficacité pour des personnes peu familières des CRM.

Environnement par défaut : https://test-crm.localeo.city. Confirme sa disponibilité et sa nature TEST à partir de la session et des sources autorisées. Utilise un accès sécurisé disponible en session ou un gestionnaire de secrets ; sinon demande uniquement l’accès manquant. N’inscris aucun identifiant de connexion dans un fichier, une capture, un journal ou un prompt archivé. Remplace toute valeur sensible par `[CONFIDENTIEL]`. Ne contacte personne et n’envoie aucun message externe.

Aucune modification du code applicatif, aucun commit, push ou déploiement. Explore en lecture ; pour les parcours d’écriture, utilise exclusivement des objets fictifs autorisés, identifiés et isolés. Ne modifie aucun prospect, tâche ou RDV préexistant réel. Prépare l’inventaire et le nettoyage ciblé des seuls objets créés ; ne supprime jamais un objet dont la nature et l’autorisation ne sont pas établies.

## 1 — Identifier le protocole et préserver l’historique

Lis le README et les AGENTS.md applicables du dépôt documentaire, puis les instructions ciblées du CRM si une lecture de code est utile. Inventorie `docs/ux-workshops/localeo-crm/` ; repère la dernière exécution et ses prompts réellement archivés. Cherche un protocole de relance explicitement versionné plus récent que v1.0 ; si présent, lis-le et documente la version utilisée. Une date de fichier seule ne prouve pas une version de protocole. Une lacune historique reste une lacune.

Calcule la date locale Europe/Paris et crée un nouveau dossier `YYYY-MM-DD`, puis `-02`, `-03`, etc. si nécessaire. Ne réutilise ni ne modifie une exécution précédente. Crée `prompts/`, `observations/`, `workshop/`, `visuels/captures-avant/`, `visuels/maquettes-apres/`, `validation/`, `synthese/`. Relève branche, commit, heure, modèles et niveaux de raisonnement effectivement exposés ; indique « inconnu » sinon. Conserve un inventaire d’empreintes des archives précédentes pour vérifier leur préservation.

Archive le présent prompt réellement invoqué, avec sa version et ses adaptations explicites, dans le nouveau `prompts/00-protocole-global.md`. Archive ensuite chaque instruction de phase effectivement utilisée sous `01-exploration.md` à `05-archivage.md`. Si aucune instruction distincte n’est utilisée pour une phase, note cette réalité et renvoie au protocole complet ; ne fabrique pas un message utilisateur historique. Conserve un journal des changements de protocole.

##  — Explorer le CRM réel

Utilise Playwright ou un navigateur automatisé, ordinateur d’abord puis smartphone. Capture uniquement les écrans réellement obtenus ; expurge les secrets et données personnelles non nécessaires avant leur archivage. Signale toute anonymisation partielle. Ne fabrique aucune capture AVANT. En cas d’échec d’accès, consigne la limite et continue les analyses indépendantes, sans simuler un parcours produit réussi.

Vérifie et documente séparément : première connexion, découverte du tableau de bord, état global de la prospection, priorités, recherche, création de prospect, qualification, statut, contact, historique, tâche, relance, retards, réservation de RDV, agenda, modification/report/annulation, préparation de démonstration, compte rendu et résultat, affectation, activité collective. Ne présuppose aucune fonctionnalité.

Contrôle particulièrement les prospects sans responsable, sans prochaine action, sans interaction récente, les relances en retard, RDV à venir, opportunités sans évolution, doublons potentiels et actions par utilisateur. Distingue prospect/dossier/action, populations, périodes, filtres, pagination, droits et livraison effective des rappels. L’absence de preuve ne prouve pas une absence de fonctionnalité.

Si accessible, lis le code des routes, composants, modèles, statuts, formulaires, filtres, tâches, agenda, notifications et affectations. Identifie le commit local et la version déployée si possible. Une commande codée ne prouve pas son utilisabilité réelle. Aucune modification applicative.

Produis `observations/cartographie-parcours.md`, `inventaire-ecrans.md`, `observations-factuelles.md`, `couverture-pilotage-commercial.md`, `limitations.md` et les captures AVANT. Chaque constat porte un ID, la mention OBSERVÉ / DÉDUIT / HYPOTHÈSE, sa preuve et les limites de confiance. Inventorie les objets fictifs créés. Actualise le README et attends l’autorisation de passer au workshop.

## 3 — Workshop contradictoire simulé

Après autorisation, fais réagir cinq experts simulés : UX SaaS B2B ; CRM/Sales Operations ; responsable commercial ; onboarding/accessibilité ; UX Research/facilitation. Ajoute sept personas fictifs : Delphine, commerciale expérimentée ; Marc, responsable commercial ; Sophie, assistante commerciale ; Patrick, commercial peu familier des CRM ; Julie, commerciale très connectée ; Nathalie, utilisatrice occasionnelle ; Thomas, cofondateur et pilote commercial. Aucun avis simulé ne doit être présenté comme un entretien réel.

Organise sept ateliers : A première impression ; B vision globale/exhaustivité ; C qualification ; D rendez-vous/agenda ; E relances/actions ; F collaboration ; G simplicité/productivité. Pour chacun : preuves d’écran, avis indépendants, réactions individuelles, confrontation contradictoire, forces, problèmes et orientations. Conserve les désaccords, pas d’unanimité forcée. Produis une matrice des sept personas et des parcours.

Fige chaque orientation avant vote : ID, parcours, problème, preuve/hypothèse, conséquence, solution, bénéfice, critères d’acceptation, effort S/M/L/XL, priorité et confiance. Priorités : P0 processus essentiel bloqué ou risque majeur de perte ; P1 friction importante/visibilité critique/risque d’oubli ; P2 amélioration différable ; P3 confort ou évolution future. Ne complète pas artificiellement les catégories.

Douze participants, une voix chacun et un argument nominatif par orientation. Seuil fixe de majorité : 7–12 POUR = ADOPTÉE ; 6 = NON ADOPTÉE ; 0–5 = REJETÉE. Les abstentions ne réduisent pas le seuil. Conserve les bulletins et contrôle les totaux. Les risques critiques restent documentés quel que soit le vote. L’adoption simulée ne vaut jamais validation utilisateur.

Produis dans `workshop/` : rapport exécutif, compte rendu, votes et arbitrages, backlog UX, orientations rejetées et quick wins. Le rapport présente GO / GO SOUS CONDITIONS / NO GO avec raisons, cinq améliorations majeures au plus pour dix commerciaux, et notes heuristiques sur 10 justifiées avec confiance : première impression, vision globale, qualification, RDV, relances, collaboration, productivité, accessibilité. N’invente aucune mesure de réussite. Actualise le README et attends l’autorisation des maquettes.

## 4 — Maquettes et comparaison

Après autorisation, maquette uniquement les P0/P1 adoptées à au moins 7 voix. Associe pour chacune ID, observation, vote, écran réel AVANT et proposition APRÈS clairement fictive. Respecte identité Localeo, composants, navigation, accessibilité, simplicité et effort maîtrisé. Maquettes isolées du code applicatif ; aucun enregistrement ni intégration CRM.

Crée `visuels/comparatif-avant-apres.html` avec comparaison côte à côte sur ordinateur et bascule sur mobile ; affiche parcours, problème, priorité, bénéfice, effort et vote. Conserve les sources et rendus locaux ; vérifie liens, rendu responsive et clavier.

Soumets les propositions aux cinq experts et sept personas simulés : compréhension de la prospection, visibilité des actions, simplicité de qualification, gestion des RDV, risques d’oubli, préférence AVANT/APRÈS ou réserve. Enregistre les réactions comme simulées. Toute modification substantielle de l’orientation exige un nouveau vote avant intégration ; les ajustements mineurs sont tracés. Mets à jour le backlog avec les références visuelles.

## 5 — Validation explicite et comparaison historique

Prépare une fiche par P0/P1 adoptée avec preuves, bénéfices, risques/dépendances, effort et vote. Présente séparément les risques critiques ouverts. Crée `validation/decisions.md` avec ID, statut, date connue, commentaire, conditions et maquette exacte. Tous les statuts commencent EN ATTENTE DE DÉCISION.

Présente à l’utilisateur les quatre choix VALIDÉE / REFUSÉE / À RÉVISER / REPORTÉE et attends sa réponse. Ne déduis aucune décision du vote ou d’une demande d’archivage. Enregistre fidèlement les décisions reçues, laisse les autres en attente. Un backlog potentiel distingue les quatre catégories sans implémentation automatique. Actualise le README et arrête la phase après enregistrement.

Dans la nouvelle exécution uniquement, compare au workshop précédent : problèmes corrigés/persistants/nouveaux/non vérifiés, priorités, notes et confiance, orientations validées/reportées. Une correction exige preuve de recette sur une version identifiée ; un changement de note peut refléter seulement une meilleure preuve. Si aucun précédent existe, indique « non applicable » sans inventer de comparaison.

## 6 — Archivage et rejouabilité, après autorisation

Contrôle prompts réellement utilisés, observations, cartographie, captures, rapport, bulletins nominatifs, backlog, rejets, quick wins, maquettes, galerie, décisions. Crée `synthese/roadmap-ux.md` : avant lancement seulement P0/P1 explicitement validées ; P2 après premiers retours ; P3 futures uniquement si adoptées. Sépare les candidats en attente et les rejets.

Crée `synthese/plan-tests-utilisateurs.md` pour de vraies séances : au moins première connexion, tableau de bord, qualification, RDV, relances et pilotage collectif. Pour chacun : préparation fictive autorisée, consigne neutre, observations, critères de réussite et traces de résultat à recueillir. Ne préremplis aucun succès. Prévois mobile, deux comptes, permissions et accessibilité selon les risques.

Le README final indique date/heure/fuseau, URL sans secrets, branche/commit, modèles/raisonnement connus ou inconnus, version réelle du protocole, parcours vérifiés et non vérifiés, limites, nombres proposés/adoptés/P0/P1, statut des validations, liens et état final. Vérifie intégrité et empreintes, chemins, images, prompts, absence de secrets et état Git des applications ; consigne toute anonymisation incomplète. Conserve les anciennes archives intactes. Fournis un prompt de relance versionné à jour, en précisant les changements sans réécrire l’histoire.

Restitue le dossier, les livrables, les contrôles et anomalies, puis le chemin du prompt de relance. Si protocole absent, validation manquante ou recette incomplète, déclare le workshop incomplet. Aucun push, déploiement ou modification applicative.
