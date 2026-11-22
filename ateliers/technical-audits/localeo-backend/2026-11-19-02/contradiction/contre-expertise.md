# Contre-expertise indépendante des dix candidats

19 novembre 2026. Mission effectivement reçue : [brief archivé](../prompts/brief-contradicteur.md). Modèle exact et effort : **INCONNU**. Les six rapports finalisés et leurs annexes, la consolidation et le backlog préliminaire ont été lus, puis les sources applicatives pertinentes ont été relues directement. Aucun ancien audit n'a été ouvert. Le skill `localeo-invariants` et la matrice de contrôles ont guidé la revue des garanties ; ils ne constituent pas des preuves d'exécution.

Les dix mécanismes restent défendables, mais plusieurs formulations de correction doivent être resserrées. Aucun vote entre agents n'est utilisé. **R01 et R10 peuvent rester P1 conditionnels**, sous scénario explicitement décrit ; ni incident ni saturation réelle ne sont démontrés. Sept autres restent P2 ; ce classement ne signifie pas que leur gain est mesuré. **R05 peut sortir du backlog principal comme P3 différable** : amélioration locale étroite, sans traitement du chargement intégral. Cette décision laisse neuf corrections prioritaires, sans chercher à conserver artificiellement dix fiches.

## Réserves bloquantes avant implémentation

- **R02 :** le compteur source est transactionnel et sémantiquement équivalent au COUNT actuel, sous intégrité des projections et migration effective. Il faut prouver ces préconditions sur la cible et conserver la coordination ; une projection absente n'est zéro que dans un schéma intègre.
- **R03 :** deux lectures et deux remèdes. Plafonner la cadence ne remplace jamais la recherche de la dernière preuve annulée servant à la régularisation.
- **R06 :** les délais connect/read/retries du SDK réduisent certaines attentes, mais ne donnent pas une deadline dure de bout en bout. Le cache est un mécanisme indépendant.
- **R08 :** paginer indépendamment gains et consommations sans enrichissement sur les mêmes IDs produirait de faux zéros à l'écran.
- **R10 :** arrêter une boucle après réservation globale laisserait des messages non commencés EN_COURS ; les emails d'accès interne peuvent ensuite être déclarés de remise incertaine. Réserver progressivement est une condition de correction, pas une optimisation facultative. Le budget doit aussi couvrir l'envoi salariés appelé à la fin du batch email.

## R01 — Confirmer le blocage, simplifier les handlers ERP

**Conserver, P1 conditionnel.** `app/api/juste_prix_api.py:123–133` attend le corps puis appelle directement le service synchrone. `services/juste_prix.py:57–99` ouvre ses unités de travail et prend la coordination exclusive. Les quatre fonctions ERP de `admin/admin.py:12523–12600` sont async et exécutent directement `BatchRunner.execute`, les envois ou synchronisations. Le mécanisme concerne les requêtes partageant cette boucle et ce processus ; il ne prouve pas une indisponibilité de tous les workers ou du service entier. Le dépôt Juste Prix a un consommateur Commerçant identifié ; les actions ERP sont opérateur, leur fréquence demeure inconnue.

**Alternative plus simple :** les quatre handlers ERP lus n'ont aucun `await` ; des endpoints FastAPI `def` constituent une solution locale à examiner, évitant quatre wrappers manuels. Le handler image conserve son async pour lire le corps, puis déporte l'unité synchrone entière. Dans les deux cas, sessions créées/fermées dans le thread, identité et contexte de corrélation préservés, mêmes erreurs/redirections/reçus. Le déplacement libère la boucle ; il ne borne ni les threads ni le SQL/fournisseur. Rejeter toute promesse de hausse de capacité globale fondée sur ce seul changement.

Preuve restante : témoin HTTP concurrent, pool/thread et rollback réels ; M01 n'exerce qu'un corps ERP extrait avec doubles, pas la route image ou le cycle ASGI.

## R02 — Équivalence du compteur établie en source, dépendance à vérifier

**Conserver, P2 ; ne pas retirer le verrou.** `participants_animation.py:104` compte tous les participants pour la capacité ; `:127` recompte après insertion pour tester `==1`. Le repository `animation_locale_repositories.py:1331–1333` ne filtre aucun statut. Son `ajouter`, juste avant, appelle `flush` : le deuxième COUNT inclut bien la nouvelle ligne.

`sql/v283_e73_compteurs_lectures.sql:3,11–47` verrouille les tables pendant installation/bootstrap, maintient les deltas de **toutes** les lignes par animation dans des triggers AFTER STATEMENT INSERT/UPDATE/DELETE, vide au TRUNCATE et retire les groupes à zéro. Un UPDATE changeant l'animation soustrait l'ancienne et ajoute la nouvelle ; une simple modification de statut n'affecte pas le nombre. Les écritures du compteur participent à la transaction des participants. Il ne s'agit donc pas d'un compteur de qualification ou d'un cache éventuellement différé. L'absence de groupe correspond à zéro dans un schéma intègre.

Lire `N` avant insertion suffit à la capacité puis tester `N == 0` pour le premier inscrit, sous les mêmes garanties de coordination et absence de mutation concurrente non coordonnée ; ne pas comparer ce N pré-insertion à 1. La migration présente dans Git et le contrôle de readiness des colonnes ne prouvent ni application effective ni triggers actifs ni absence de dérive. Exiger équivalence COUNT/compteur sur insert, suppression, transfert, rollback, cascade/TRUNCATE pertinents, puis capacité/inscriptions/clôture concurrentes. Aucun de ces tests n'a été exécuté ici. Garder le domaine propriétaire de la politique de capacité ; l'adaptateur fournit le fait exact.

Alternative sans nouvelle dépendance : garder un seul COUNT pré-insertion et le réutiliser. Elle retire le deuxième comptage mais garde le coût de lecture proportionnel ; c'est un repli plus limité si la projection ne peut pas être contractualisée immédiatement.

## R03 — Confirmer deux projections auxiliaires distinctes

**Conserver, P2, deux sous-lots explicitement liés.** `validations_animation.py:133–143` ne charge les récentes qu'en absence de preuve effective, puis calcule le statut à partir de leur longueur. `ValidationAnimation.qualifier_cadence` distingue seulement moins de 60 et au moins 60. La sélection de 60 IDs maximum, sans tri, donne ce fait exact sans changer le seuil domaine.

Conserver les filtres actuels : commerce, `validated_at >= now - 1 minute`, **tous statuts et toutes animations de ce commerce** ; la requête actuelle n'a pas de borne supérieure `<= now`. Ne pas introduire silencieusement ce filtre ou un filtre VALIDEE. Les anomalies sont aussi enregistrées ; l'optimisation ne doit pas arrêter d'enregistrer après le seuil. Les rejeux effectifs évitent déjà cette lecture.

La seconde lecture doit retourner la dernière annulation du même participant, commerce et étape, selon `(annulee_at ou validated_at, str(id))`, et préserver `regularise_validation_id` seulement quand la nouvelle preuve est VALIDEE. Une LIMIT sur l'historique avant ces filtres pourrait perdre la référence. Les ports ciblés ne redéfinissent pas la règle. Tester 59/60, anomalies, dates égales, annulations hors cible, QR/PIN ; plans SQL et temps restent inconnus. L'index commerçant/date existe : aucune recommandation d'index supplémentaire automatique.

## R04 — Confirmer le ciblage et les populations, borner sans perdre l'atomicité

**Conserver, P2.** `notifications_localeo_live.py:43–94` lit les installations actives globales avant filtre de commune ; `:97–120,160–203` charge les paires installation/participant puis agrège le statut gagnant. La publication et le tirage appellent ces producteurs dans leur transaction. La clôture/neutralisation possède déjà un parcours borné, à ne pas accuser.

Le premier palier simple est le filtre SQL commune/catégorie et une insertion idempotente groupée. Pour borner réellement les objets, pages stables d'installations **distinctes**, enrichissement gagnant sur tous leurs participants et insertions par lot, sans accumulation ORM en attente. Conserver l'équivalence des préférences absentes/nulles, titre, payload, source_key et le OR gagnant si une installation suit plusieurs participations. Les lots dans la même transaction bornent les buffers, pas sa durée ni sa mémoire totale automatiquement. Une diffusion asynchrone avec commits intermédiaires serait un changement de garantie/reprise séparé. Mesurer installations étrangères N/10N à cible fixe ; aucun coût intégré établi ici.

## R05 — Garder exclusivement la suppression de la copie list

**Déclasser P3 différable en annexe ; portée fortement réduite.** `tirage_animation.py:74–94` vérifie les doublons par set puis passe `list(tuple_ids)` à `sample`. `ServiceTiragesAnimation` injecte normalement `secrets.SystemRandom` ; les doubles ciblés relus dans `test_tirage_tous_lots_animation.py:21–24` et `test_tirage_gain_animation.py:81` acceptent une séquence ou en font une liste. Le tuple peut donc être proposé directement, sous vérification du contrat de toutes les sources injectées.

**Ne pas supprimer la vérification des doublons du domaine**, même si la persistance est unique ; les autres constructeurs ont le droit de fournir des données invalides. Ne pas inclure réservoir, pagination/reprise ou changement d'aléatoire dans ce petit lot. L'intégralité des UUID, le tuple, le set de vérification et éventuellement les allocations internes de sample subsistent ; le pic exact dépend des phases et du nombre de gagnants. Le gain mémoire n'est pas égal a priori à la taille de la liste retirée. O(N) et verrou exclusif demeurent. Aucune promesse de mémoire bornée, d'uniformité nouvellement validée ou d'amélioration SQL.

Le déclassement concerne cette **copie seule**, pas toute la cause RC-06. La population intégralement chargée sous coordination exclusive reste une piste distincte à mesurer avant de grandes jauges. Le faible pic transitoire communiqué à 10 000 IDs ne suffit pas à déclasser ce mécanisme intégré : les UUID et le tuple préexistaient à la fenêtre, SQL et temps de verrou en sont absents, et aucun avant/après n'est disponible. La baisse de priorité repose sur l'étroitesse du remède et l'absence de gain démontré, sans conclure à l'innocuité de la population complète.

## R06 — Politique I/O explicite, sans promesse de deadline dure

**Conserver, P2 ; séparer le cache.** `contenu_generation.py:335–345,368–395` vérifie le budget autour de `get`, et `document_storage.py:83–109` n'injecte pas de configuration explicite connect/read/retries et lit tout le Body sans fermeture explicite. Le stockage LOCAL a un autre mécanisme ; le fournisseur réellement utilisé n'est pas établi. Les limites de contenu ne prouvent pas la borne d'une lecture préalable d'un objet remplacé.

Ajouter politique I/O explicite, lecture taille autorisée + sentinelle et fermeture Body ; appliquer le budget restant aux opérations compatibles, sans modifier les autres lecteurs du stockage partagé. Un read-timeout peut être une limite d'inactivité, les retries cumulent des attentes, et une vérification monotone après lecture n'interrompt pas l'appel en cours. Si la cible exige une deadline dure, sa conception/exécution doit être un lot distinct et prouvé ; un thread abandonné ne signifie pas I/O annulée.

Le cache d'octets validés traite les relectures/décodages, non le dépassement d'une première I/O : garder RC-11 séparée. Préserver autorisation courante, provenance, SHA, erreurs et retrait/conservation ; pas de cache public improvisé. Mesures manquantes : provider effectif, latence get/read/décodage, trickle/retries et réponse après expiration navigateur.

## R07 — Confirmer le risque de lectures séquentielles, réutiliser avec précision

**Conserver, P2 conditionnel.** `jeu_animation.py:403–408` appelle `session.get` indirectement par commerce pour un passeport. L'identity map peut servir des hits ; cela interdit d'annoncer un nombre de SELECT effectif sans instrumentation. Le dashboard préchargé est un autre parcours.

`repositories_sqlalchemy.py:143–170` offre déjà `lister_resumes(ids=...)`, mais sélectionne bien davantage que nom/adresse et trie par nom. Le réutiliser est une alternative simple ; une projection dédiée réduit encore les colonnes. Reconstruire impérativement l'ordre merchantIds et la même erreur de commerce absent, ainsi que la conversion d'adresse. Aucun nouveau filtre de statut implicite. La cardinalité du passeport n'a pas ici de maximum métier explicite : un énorme IN unique ne devient pas une preuve de coût borné ; prévoir lots de clés au besoin sans changer le contrat public. Tester SQL froid/chaud et JSON identique.

## R08 — La pagination doit porter sur la ligne affichée enrichie

**Conserver, P2 transverse backend/Animation.** `GainsAnimTab`, `App.tsx:2939 et suivantes`, attend gains et consommation ; `collectPages` collecte séquentiellement jusqu'au total, avec une garde de 1 000 pages. C'est une borne de sécurité réelle, pas une page interactive ; ne pas qualifier la boucle d'infinie. Les gains viennent de la route liste intégrale `animation_locale_api.py:2747–2753` et les consommations de la route paginée `:2798–2810`.

Le rendu fait `conso.find(c => c.gain_id === g.id)` puis utilise zéro si absent. Deux listes paginées indépendamment peuvent donc afficher une consommation fausse : **paginer d'abord les gains autorisés et enrichir la page de leur consommation**, ou définir une projection jointe dédiée. Exposer les agrégats exacts séparés selon les mêmes définitions qu'aujourd'hui (gains actifs, ENVOYE, consommation zéro/partielle), pas des totaux calculés sur la page. Route additive et ancienne route conservée pour compatibilité ; aucune preuve d'inventaire exhaustif des clients externes. Préserver page, focus, filtres et erreurs/reprises. Aucun premier rendu navigateur mesuré.

## R09 — Agréger les mêmes faits, distinguer les écrans actuels

**Conserver, P2.** `pilotage_animation.py:65–80` hydrate participants, validations valides et notifications tenant avant filtre animation. `:101–126` contient un dashboard historique plus large. Les appels courants au live sont bien visibles dans `App.tsx:1792` (statistiques du workflow) et `:1987` (tirage). Le workflow seul n'effectue pas ce chargement de statistiques : c'est son écran qui appelle aussi live. Le dashboard courant borné n'est pas accusé du mécanisme historique.

Les COUNT/GROUP BY doivent préserver les **statuts des participants actuellement comptés**, la sélection des validations et les calculs de moyenne/requis, pas les remplacer par des mesures de qualification de sémantique différente. Pour le dashboard historique : périmètre tenant/animations avant agrégation, archives et filtres, dates inclusives selon PeriodePilotage, jours Europe/Paris. `faits_tirage_dans_uow` hydrate aussi gains/tirages : les variantes de réponse/actions doivent être examinées pour éviter un faux « tout est désormais borné » après correction des seuls compteurs. Les alertes sont une collection : les cibler est un premier palier ; les paginer changerait leur contrat et demande une décision explicite. Pas de hausse P1 sans cardinalités/fréquences et mesures des lecteurs actuels.

## R10 — Budget de cycle et propriété, sans confusion avec la remise fournisseur

**Conserver P1 conditionnel**, à expliciter au même titre que R01. `batchs.py:608–700` supprime un bail expiré puis admet une autre invocation ; `handler()` n'est pas limité. La libération compare correctement correlation_id. `scheduler/http_client.py:51–63` borne l'attente du client, sans annuler le serveur. Le scénario 100 remises séquentielles à environ 4 s dépasse le bail source de 360 s ; sa fréquence réelle et la topologie déployée ne sont pas connues.

`emails_batch.py:25–61` et `sms_batch.py:17–47` réservent aujourd'hui l'ensemble du lot avant de l'envoyer. Un simple break sur horloge ferait abandonner des réservations ; pour les emails de type ACCES_UTILISATEUR_INTERNE, `reprise_exige_rapprochement` peut ensuite qualifier de remise incertaine un message jamais commencé. Réserver progressivement, vérifier budget **avant** claim et transport, conserver une marge explicite et ne plus commencer d'unité après perte de propriété. L'email appelle ensuite `remise_salaries.execute(limit)` : ce second traitement doit recevoir le même budget restant ou être exclu explicitement de la garantie annoncée. Les compteurs et contrats batch doivent conserver une signification claire après traitement partiel.

Un budget vérifié entre unités est coopératif. Il ne borne pas durement l'unité réseau en cours et ne garantit donc pas à lui seul qu'un bail n'expirera jamais ; si cette garantie est exigée, établir bornes d'unité/marge ou renouvellement propriétaire et stratégie après perte. Ne pas renouveler indéfiniment un travail bloqué.

Les claims et `obtenir_pour_envoi` protègent les messages ; **l'overlap ne prouve aucun doublon**. R10 ne déplace pas le fournisseur hors transaction : `emails_batch.py:76–92` et `sms_batch.py:60–67` gardent connexion/verrous pendant le réseau. Les gardes d'accès/révocation SaaS de l'email rendent cette seconde correction distincte et plus délicate. Mesurer séparément admission du cycle, occupation SQL et incertitude fournisseur.

## Mesures et limites de preuve

Au début de cette mission les mesures étaient préparées. Pendant la revue, l'orchestrateur a communiqué leur achèvement sans erreur : M01 corps ERP AST avec attente injectée, M02 horloge logique/SQLite, CSV réduit et M-LIVE-01 domaine. **Cette contre-expertise n'a exécuté ni reproduit ces campagnes et ne les transforme pas en mesures intégrées.** Leurs bruts/manifeste et conclusions finales sont sous responsabilité de l'orchestrateur.

M01 ne mesure pas HTTP/ASGI ni le dépôt image. M02 peut montrer l'admission après expiration du bail, pas la concurrence PostgreSQL, la durée fournisseur réelle ou des doublons. Le CSV est hors des dix mécanismes prioritaires et ne valide aucun parcours Live. M-LIVE-01 commence avec tuple/UUID préparés ; il mesure des transitoires de construction/sélection et des contrôles de harness inclus dans le temps, pas la mémoire totale, le SQL, la contention ou un profil CPU pur du domaine. Un plateau de capacité du set entre deux tailles ne prouve pas une complexité mémoire constante. Aucune correction ni comparaison avant/après n'existe.

Restent non mesurés ici : p95/p99 HTTP, plans PostgreSQL, nombre réel de SELECT, attentes verrous/pool, RSS, trafic réel, topologie et migrations appliquées. Les preuves nécessaires sont ciblées dans le [plan de mesures](../recommandations/plan-mesures.md) ; elles doivent vérifier les invariants avant d'attribuer un gain. Aucun chiffre de capacité ni gain estimé n'est validé par cette revue.

Seul `localeo-projet/contradiction/contre-expertise.md` dans le présent dossier a été écrit. Backend et consommateurs sont restés en lecture seule ; aucun test, benchmark, import applicatif, réseau, base, serveur, build, commit, push ou déploiement exécuté par cet agent. Aucun guide ni export canonique modifié : vérificateurs documentaires non exécutés conformément au brief. Critères d'acceptation, contrats, migrations et générateur ne changent pas dans cette mission de diagnostic ; leurs impacts éventuels sont des conditions des futurs correctifs, pas des travaux déjà réalisés.
