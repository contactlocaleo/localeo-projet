# Relancer un audit de performance Localeo Backend

Tu es l’orchestrateur d’un **nouvel audit indépendant** du backend Python Localeo. Inspecte directement le code réel. Objectif : identifier et mesurer les risques CPU, mémoire, concurrence, persistance et latence sur les flux critiques, puis proposer au plus 5 à 10 corrections locales compatibles, sans remplissage artificiel. Ne réalise aucune implémentation, migration, installation générale d’outils, modification de données réelles, commit, push ou déploiement. Aucun test de charge en production.
Oriente l'audit sur les uses cases liés à Localeo Live et la plateforme d'animation en priorité.


## 1. Trouver la référence et préserver les archives

Lis README et AGENTS.md du projet documentaire, puis les instructions locales des dépôts concernés. Les cinq dépôts restent indépendants ; ne crée pas de Git parent. Protège les modifications utilisateur. Les documents canoniques restent dans localeo-projet ; exécutables, harness et bruts dans leur dépôt applicatif ou stockage privé, jamais copiés comme données de travail dans le dépôt documentaire.

Liste `docs/technical-audits/localeo-backend/`. Identifie l’exécution antérieure la plus récente par date/suffixe et statut d’archive, puis lis son README, `benchmarks/protocole.md`, résultats, limites, manifeste, backlog final, décisions et synthèse. En cas de date/suffixe ambigu, consigne le choix. Ne sélectionne pas uniquement sur la date de modification d’un fichier. Le protocole peut avoir des amendements et plusieurs harness : respecte la provenance des scénarios retenus et les tentatives interrompues.

Releve la date locale réelle YYYY-MM-DD et son fuseau. **Crée un nouveau dossier**, avec suffixe -02, -03… si le nom existe ; n’écris ni rapports, ni contrôles, ni mesures dans l’ancienne exécution. Crée prompts/, inventaire/, agents/, contradiction/, benchmarks/, recommandations/, validation/, synthese/. Relève les empreintes des anciennes archives avant travail pour pouvoir prouver leur conservation.

Archive intégralement le prompt réellement invoqué et la demande utilisateur courante, par exemple `prompts/00-relance-utilisee.md`. Enregistre les briefs exacts réellement transmis aux agents. Si d’autres prompts d’étapes sont effectivement utilisés, conserve-les sous leur nom ; **ne recopie pas les six anciens prompts en prétendant qu’ils ont été invoqués cette fois-ci**. Un prompt manquant est signalé, jamais reconstruit fictivement. L’archive du 19 novembre 2026 fournit des références, pas une autorisation de réécrire l’historique.

## 2. Identifier les révisions et réanalyser la stack

Relève branche, commit et état des cinq dépôts, fichiers locaux pouvant affecter la mesure, Python réellement disponible, versions verrouillées/installées distinctes, matériel et ressources connues. Note explicitement modèle exact/effort de raisonnement s’ils sont exposés ; sinon INCONNU, sans les déduire du nom d’un agent ou des modèles disponibles.

Compare les commits backend courant et précédent par Git en lecture seule ; consigne SHAs et périmètre du diff, disponibilité des anciens objets et limites d’une comparaison avec checkout sale. Aucune absence d’un constat dans un ancien rapport ne prouve l’introduction d’une régression. Vérifie dans le code si une ancienne correction subsiste ; un statut historique ou un commit documentaire ne suffit pas.

Lis framework, serveur, modèle de concurrence, workers/pools, ORM/moteur SQL, transactions, scheduler/outbox, fournisseurs, caches, limites et observabilité. Ne charge aucun dotenv privé et n’importe pas app.main avec la configuration opérateur. Réutilise les gardes du README backend et `scripts/validation/test_isolated.py` après lecture de leur version courante. N’utilise aucune base simplement parce qu’un client PostgreSQL ou une URL héritée existe.

## 3. Cartographier les flux et contrats réels

Reconstitue endpoint → handler → services → repositories/persistance → traitements → réponse, avec fichiers, fonctions et lignes. Priorité aux validations QR, participation, consultation d’animations, dashboard/Live, gestion/import commerçants, clôture/tirage, résultats et autres flux coûteux réellement trouvés. Distingue mode borné/historique, moteurs, routes anciennes/récentes, absence/présence de médias ou d’en-tête Stripe. Identifie les consommateurs avant d’étendre la portée d’un constat.

Produis les sept documents inventaire : architecture.md, stack-technique.md, catalogue-api.md, flux-critiques.md, configuration-ressources.md, limitations.md, plan-orchestration-agents.md. Les comptes statiques de routes sont des opérations potentielles, pas une preuve de routes déployées ou de trafic.

## 4. Relancer six analyses indépendantes

Utilise six véritables sous-agents Codex si disponibles : CPU/algorithmes, mémoire, async/concurrence, persistance, performance API, SRE/capacité. Respecte la limite de simultanéité de l’hôte ; plusieurs vagues sont acceptables. Si indisponibles, réalise des analyses séparées et documente cette limite.

Chaque spécialiste doit lire le code lui-même et finaliser sa première analyse **sans lire les conclusions des autres ni reprendre les anciens diagnostics comme verdict**. Crée les sous-agents avec un contexte neuf (`fork_turns="none"` si l’outil le permet) : l’orchestrateur ayant déjà lu les archives ne doit pas transmettre son historique complet. Fournis seulement instructions applicables, cartographie neutre, sources et mission propre, sans conclusions historiques ou des autres agents. Si cet isolement n’est pas disponible, signale la limite d’indépendance. Attribue des fichiers distincts `agents/01-cpu.md` à `06-sre.md`, annexes séparées, et aucun serveur/base/benchmark partagé. Un seul propriétaire exécute les mesures ensuite. Les agents ne sont pas seuls dans le workspace et ne doivent pas revenir sur les edits d’autrui.

Rapport principal : **cinq constats majeurs maximum**, sans quota à remplir, classés impact/probabilité/criticité/preuve/facilité. Pour chacun : ID, domaine, fichier/lignes, fonction, mécanisme, flux et API, conséquence, déclencheur, preuve source, mesure disponible, confiance, correction minimale, effort S/M/L/XL, risque, breaking change et domaines transverses. Statuts distincts : CONFIRMÉ PAR MESURE, FORTEMENT ÉTAYÉ PAR LE CODE, HYPOTHÈSE À VÉRIFIER. Pas de temps, gain ou volume inventé. Les observations secondaires vont en annexe.

## 5. Consolider et contredire

Après finalisation des six premières analyses, relis-les et vérifie les preuves dans le code. Regroupe par **cause racine et flux métier** : symptômes CPU/mémoire/SQL d’un même chargement doivent donner une correction commune si elle suffit. Conserve distincts les mécanismes exigeant des remèdes différents. Lie les anciens et nouveaux identifiants par sens, pas par leur seule chaîne « API-01 ».

Mandate un contradicteur indépendant : faux positifs, priorité excessive, optimisation prématurée, correction plus simple, compatibilité, régression et mesures manquantes. Produis consolidation.md, causes-racines.md, contre-expertise.md, debats-et-votes.md. Six voix simulées sont permises, ≥4 favorables pour adopter une orientation ; contradicteur sans vote. Dis explicitement ce qui est simulé et ce qui provient d’un agent réel. Le vote n’est ni preuve ni autorisation, les problèmes critiques restent documentés.

P0/P1 exigent mesure réelle, preuve solide ou scénario de charge crédible explicité. Ne confonds pas mauvaise pratique et saturation avérée. Prépare backlog-preliminaire.md, annexe des secondaires et plan-mesures.md.

## 6. Rejouer uniquement les mesures sûres

L’invocation de ce prompt autorise l’analyse et les petits bancs de composants **hors réseau, isolés, synthétiques et bornés** dont le protocole a été vérifié. Une campagne HTTP/SQL exige une cible jetable explicitement désignée et autorisée dans la demande en cours. Sans cet environnement ou si les gardes ne sont pas démontrées, prépare le protocole et indique NON EXÉCUTÉ, sans chercher une cible réelle.

Avant toute mesure : fixe matériel/configuration/versions, jeu et empreinte, concurrence/durée/outils, budgets et arrêts. Choisis quelques goulots prioritaires, pas toutes les API. Sépare échauffement, essais temporels et profilage ; relève métriques disponibles et leurs unités, erreurs et retours à la normale. Commence faible, ne rejoue pas 50/100 utilisateurs par défaut et ne relève pas un seuil après échec pour obtenir un succès.

Pour rejouer M01/M02/M06 du 19 novembre 2026, vérifie d’abord les empreintes des sources, harness et bruts du manifeste. Copie les harness utiles dans un **nouveau répertoire backend ignoré**, avec sorties propres à cette exécution. Le harness final ancien exerce seulement le CSV ; l’état tentative 03 comprend M01/M02 et un CSV interrompu. Prépare et archive la sélection réellement exécutée, sans relancer aveuglément le cas connu trop long ni écraser les anciens artefacts. N’altère jamais les corps applicatifs pour obtenir la mesure. Extraction AST/doubles, SQLite/horloge logique, tracemalloc et profilage complet HTTP/PostgreSQL n’ont pas la même portée.

Conserve chaque tentative échouée/interrompue avec commande expurgée, statut, motif, version du harness et empreinte ; ne perds pas les mesures achevées avant arrêt. Si les artefacts ignorés antérieurs sont absents, signale la perte de reproductibilité exacte ; n’invente pas les bruts. Un nouveau harness issu du protocole est une nouvelle méthode à qualifier, pas l’original prétendument récupéré.

Produis protocole.md, resultats.md, limites.md, profils-cpu.md, profils-memoire.md et backlog-mesure.md. Distingue gain démontré, bénéfice plausible et NON MESURÉ. Sans correction autorisée et essai avant/après, il n’y a pas de gain après correction. Aucune qualification de capacité API à partir de doubles ou de sept exports CSV.

## 7. Reprioriser et comparer l’historique

Conserve au plus 5 à 10 corrections principales sans remplissage artificiel ; élimine celles infirmées, déclasse celles dont l’impact est réellement faible, sépare les non mesurées avec confiance. Classes A quick win, B ciblée, C refactoring important, D incompatible ; privilégie A/B, justifie séparément C/D. Chaque fiche : cause, flux/API, preuves et mesures, minimum/alternative, gain inconnu ou démontré, effort, risques, compatibilité, tests et rollback préservant les effets métier. Produis backlog-final.md, quick-wins.md, plan-optimisation.md et validation/decisions.md.

Compare avec la précédente exécution et les anciens audits pertinents : corrigé vérifié/persistant/nouvellement documenté/non vérifié ; commits et décisions réelles, pas d’autorisation déduite. Une métrique n’est quantitativement comparable qu’avec mêmes scénarios, volumes/distribution, versions, matériel/limites, charge, méthode/unité et état des caches suffisamment proches. Sinon, écris NON COMPARABLE et explique pourquoi ; pas de tendance CPU/RAM ou de gain API entre des protocoles différents.

## 8. Archiver et attendre le choix

Produis synthese/rapport-executif.md, roadmap-performance.md et comparaison-precedent.md si une référence existe. Finalise README : dates/SHAs, stack, matériel, modèles/efforts connus ou inconnus, méthodes, mesures/limites, comptes des constats/problèmes/causes/corrections, P0/P1 et validations techniques distinctes des décisions utilisateur.

Vérifie présence et intégrité des livrables, chemins/lignes, absence de secrets par contrôle expurgé, Git et empreintes applicatives, conservation des anciens dossiers/bruts. Exécute les vérificateurs documentaires requis ; conserve leur résultat sans le confondre avec un test métier. Les scripts restent applicatifs, les bruts ignorés doivent être signalés comme dépendance de rejouabilité hors archive Git.

Archive le dossier et présente les P0/P1 avec les choix **VALIDÉE / REFUSÉE / À APPROFONDIR / REPORTÉE**. Laisse tous les champs sans choix tant que l’utilisateur n’a pas répondu. **Arrête-toi à cette validation ; aucune implémentation, migration ou livraison n’est autorisée par ce prompt.** Toute prochaine exécution aura un nouveau répertoire, les archives précédentes resteront intactes.


## Demande courante
Pièce jointe ci-dessus ; texte : `#`. Interprétation : exécuter la relance jointe.
