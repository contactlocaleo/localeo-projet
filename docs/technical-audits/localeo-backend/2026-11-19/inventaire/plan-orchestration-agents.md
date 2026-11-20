# Plan d’orchestration — soumis — autorisation

Statut : **six missions définies, aucune mission spécialisée exécutée**. Objectif : optimisations ciblées, compatibles, sans refonte majeure. L’agent principal assure intégration, dédoublonnage, contradiction et rapport final ; il ne cumule pas arbitrairement les impacts estimés par les missions.

## Ordre et ressources

1. Après autorisation, prévol : vérifier que chaque agent peut réellement lire un fichier backend et citer commit/lignes ; sinon arrêter cette mission et signaler la limite, sans inventer ses résultats.
2. Trois vagues de deux missions indépendantes : CPU + mémoire, async + persistance, API + SRE. Deux spécialistes au maximum laissent un créneau pour une revue indépendante et respectent les quatre créneaux disponibles avec l’orchestrateur.
3. Les missions relisent les sources elles-mêmes ; la présente carte sert de point d’entrée, pas de preuve de seconde main. Chaque mission écrit uniquement son rapport et son annexe sous `agents/`, et n’écrit aucun code applicatif.
4. Aucune ressource d’exécution partagée allouée — ce stade : ni serveur, port, base, build, profiler ni test de charge. Une future mesure autorisée aura un propriétaire unique, une base jetable et un dossier d’artefacts propre dans le backend/stockage privé ; pas de sorties d’exécution dans ce dépôt documentaire.
5. Après les rapports, revue croisée en lecture des causes candidates, puis scénarios de validation proposés. Mesures, corrections et activation restent des phases distinctes.

## Missions et livrables réservés

| Mission | Rapport principal | Annexe | Périmètre |
| --- | --- | --- | --- |
| CPU et algorithmes | `agents/cpu-rapport.md` | `agents/cpu-annexe.md` | Complexité selon population, tris, sérialisation, hashing, QR/PDF/images, règles du moteur et tirages. Distinguer coût Python, SQL et réseau. |
| Mémoire et allocations | `agents/memoire-rapport.md` | `agents/memoire-annexe.md` | Objets hydratés, collections et copies, bytes/archives, rétention ORM, caches et bornes après décompression. Préparer N/10N, RSS et allocations sans lancer la campagne. |
| Async et concurrence | `agents/async-rapport.md` | `agents/async-annexe.md` | Chemins sync/async réels, threadpool, appels bloquants, verrous, idempotence, backpressure, délais et annulation. Ne pas attribuer une opération sync au thread événementiel sans suivre son appel. |
| Persistance | `agents/persistance-rapport.md` | `agents/persistance-annexe.md` | SQL réel visible dans sources, cardinalités, pagination, N+1, indexes livrés, transactions/verrous, sessions/pool. Un index déclaré ne prouve pas le plan effectif. |
| Performance API | `agents/api-rapport.md` | `agents/api-annexe.md` | Coût complet endpoint/dépendances/auth/handler/projections/réponse, taille de payload, pagination, cache HTTP, polling et latence perçue des jobs. Séparer branches historiques et bornées. |
| SRE et capacité | `agents/sre-rapport.md` | `agents/sre-annexe.md` | Topologie vérifiée, workers/réplicas, pools, scheduler et files, budgets de ressources, timeouts/retries, observabilité, saturation et reprise. Expliciter les inconnues de déploiement. |

Chaque rapport principal contient **cinq constats majeurs au maximum**, classés par impact probable. Les observations supplémentaires vont en annexe ; zéro constat est acceptable si aucune anomalie n’est suffisamment étayée. Les briefs préparés sont dans [agents](../agents/README.md).

## Format commun obligatoire

En-tête : mission, auteur, commit/backend et état du checkout, fichiers effectivement lus, méthode, contrôles exécutés et non exécutés, limites. Aucun secret, donnée client, URL privée ou token.

Pour chacun des cinq constats maximum :

- ID stable (`CPU-01`, `MEM-01`, `ASY-01`, `DB-01`, `API-01`, `SRE-01`), titre factuel, rang et impact probable.
- Statut : fait de code / hypothèse causale / mesuré / réfuté / non concluant. Confiance faible, moyenne ou forte avec justification. Un fait de code ne vaut pas mesure d’impact.
- Localisation : dépôt, SHA, fichier, symbole, lignes ; extrait minimal sans secret. Décrire le chemin d’appel qui rend le coût atteignable.
- Flux Fxx et liste `méthode + endpoint + variante + acteur` ; conditions de déclenchement, volume, concurrence et périmètre tenant.
- Symptôme observable attendu, cause racine candidate et mécanisme CPU/mémoire/I/O/verrou/pool/réseau. Coût en fonction de N, éléments effectivement bornés, inconnues.
- Preuves disponibles et contre-exemples : chemins non touchés, limites déjà présentes, branches conditionnelles ; distinguer existence d’un index et usage mesuré.
- Impact métier (validation, inscription, clôture, argent, attente) et technique (ressource, propagation, reprise). Pas de score de latence ou gain numérique inventé.
- Proposition ciblée sans breaking change, alternatives et compromis, effort/risque estimés, invariants propriétaires du domaine et contrats/consommateurs — préserver.
- Validation proposée : environnement isolé, données synthétiques, protocole N/10N ou charge mixte, métriques, seuils — fixer avant exécution, cas de refus/rejeu/concurrence, critère de réfutation et retour arrière.
- Liens vers cause transverse existante ou indication — nouvelle candidate à, dépendances et observations en annexe.

Fin de rapport : maximum cinq constats classés, couverture F01–F12, questions ouvertes, mesures nécessaires, actions sûres candidates. Aucune correction ni campagne implicite.

## Consolidation et contradiction

L’orchestrateur tient [le registre des causes](../contradiction/registre-causes.md). Clé candidate : mécanisme + symbole propriétaire + données/ressource + condition d’exécution ; un endpoint seul n’est pas une cause. Exemple de structure, sans préjuger d’une anomalie : plusieurs routes appelant la même projection pourraient partager une cause ; les mêmes symptômes provenant d’un verrou et d’un rendu image garderaient deux causes distinctes.

Un ID `RC-xxx` relie plusieurs constats et tous leurs endpoints. Garder chaque preuve et auteur ; ne pas compter plusieurs fois le même impact. Une cause peut expliquer plusieurs symptômes ; un symptôme peut avoir plusieurs causes jusqu’à contradiction. Les observations supplémentaires restent consultables, sans multiplier les tickets.

Avant toute recommandation, un lecteur indépendant reprend le code, les bornes et branches actuelles, cherche une réfutation et documente les désaccords dans `contradiction/`. L’absence de mesure reste visible. Un seul ticket candidat par cause confirmée, avec sous-actions éventuelles ; aucun ticket externe n’est créé dans cette étape.

Priorité : ordonner impact métier (blocage validation/argent/inscription/clôture), portée et fréquence, ressource partagée/saturation, ampleur et durée, puis confiance de preuve, effort et risque de changement. P0 : indisponibilité avérée ou effet métier critique ; P1 : chemin critique et dégradation forte démontrée/probable avec déclencheur établi ; P2 : impact borné ou moins fréquent ; P3 : piste — mesurer. Un classement probable reste provisoire jusqu’aux mesures. La confiance est un axe séparé de la gravité.

## Flux transverses — éprouver

- F01 + F02 : pics de scans/validations, session/autorisation, règles, verrous et écritures jusqu’au reçu, avec rejeux et QR révoqué.
- F03 + F04 + F09 : découverte — inscription — email/accès — jeu — résultat ; suivre temps HTTP et délai de livraison séparément.
- F05 + F06 + F07 : pilotage et recherche sous import actif, volumes de la commune et des autres tenants, pages profondes, droits révoqués et focus/formulaire si un changement frontend était proposé.
- F08 + F09 + F12 : clôture — gel — tirage — notification — consultation ; cohérence et preuve de population, durée de transaction et retard des opérations différées.
- F10 + F01 + F08 : achat/financement — disponibilité — attribution/validation, sans affaiblir l’idempotence financière.
- F11 + F12 avec F01–F05 : génération/exports/communications en concurrence avec trafic interactif ; files, mémoire, pool et retour — la normale.

La couverture se décline par moteur (tombola, chasse, vitrines, juste prix), modes de dashboard, tirage Coffrets/libre et actor principal/salarié/organisateur. Elle doit rester proportionnée aux chemins réellement atteignables.
