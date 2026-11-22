# Annexe indépendante — SRE et capacité

Complément de [06-sre.md](06-sre.md), première analyse indépendante au SHA backend `7049e7fafc76f9119924f1082a5ee7457a175d85`, 19 novembre 2026. Aucun rapport ni conclusion d’un autre spécialiste consulté avant finalisation. Aucun outil de performance exécuté.

## Observations secondaires, sans promotion artificielle en anomalie majeure

### O-SRE-01 — Émission de logs synchrone sur stdout

Statut : **HYPOTHÈSE À VÉRIFIER** pour une dégradation sous charge. Le mécanisme est visible : `configure_logging`, `app/logging_config.py:22–58`, installe un `logging.StreamHandler(sys.stdout)` ; `emit_log_event`, `app/observability.py:337–387`, appelle directement `logger.log`. Le formatter JSON reconstruit les métadonnées et assainit les extras (`observability.py:398–428`). Les hooks n’interposent pas de file asynchrone. `RequestContextMiddleware.dispatch`, `app/observability_http.py:29–89`, émet au début puis à la fin de la requête, dans son chemin async ; les appels `execute` instrumentés émettent aussi début/fin (`observability_instrumentation.py:94–119,156–188,191–298`).

La capture d’exceptions de journalisation rend les erreurs best effort ; elle n’impose pas de durée maximale à une écriture stdout bloquante. Un collecteur lent pourrait donc propager son attente, y compris au chemin de requête. Il manque la vitesse du sink, les niveaux effectifs, les octets et événements par requête : aucune saturation ni nécessité de nouvelle infrastructure de logs démontrée. Le volume croît avec les requêtes et invocations instrumentées ; les arguments DEBUG sont résumés avant l’appel à `emit_log_event`, même si DEBUG sera filtré (`instrumentation.py:112–118`), mais leur résumé évite de parcourir intégralement les collections ordinaires (`observability.py:281–310`).

Investigation proposée seulement : sink synthétique lent, temps d’écriture/formatage, p95 requêtes et événements/octet par flux. Une correction éventuelle doit préserver les événements de sécurité/audit ; échantillonner tout indistinctement ou introduire une file non bornée serait une nouvelle fragilité. Ne pas présenter `logging.yaml` DEBUG comme la configuration effective : `main.py:161,170` applique explicitement `configure_logging`, dont les défauts sont INFO et SQL WARNING.

### O-SRE-02 — Santé approfondie consommatrice de capacité

Statut : **HYPOTHÈSE À VÉRIFIER** sous consultations concurrentes. `ServiceSanteSysteme.execute`, `app/infrastructure/health/health_systeme.py:392–433`, crée un executor par invocation pour les checkers ; `_check_brevo:237–298` crée un second executor pour les clés distinctes. Les checkers SQL, schéma, batchs et files partagent l’engine applicatif. La route d’administration exécute ce service via `run_in_threadpool` (`app/infrastructure/admin/admin.py:7985`, lecture ciblée du site d’appel).

Il existe des timeouts fournisseurs et un état par checker ; aucune fréquence publique de polling n’est établie. La page indique explicitement que `/sante` est léger et que le diagnostic profond est protégé (`admin.py:5698`). Aucune raison de remplacer ce diagnostic ni de déclarer un problème majeur sur une utilisation support occasionnelle. Pour une exploitation automatisée future, relever le nombre d’appels simultanés et distinguer sonde de vie et diagnostic avant toute décision.

### O-SRE-03 — Renouvellement du bail et projection utilisent le pool applicatif

Statut : **HYPOTHÈSE À VÉRIFIER** quant à l’effet sous saturation. `SchedulerRepository` importe le même `SessionLocal` (`repository.py:8`) ; le renouvellement (`29–80`), le contrôle de propriété (`82–97`) et la synchronisation (`149–207`) ont besoin de SQL. `_coordination_loop`, `coordinator.py:74–108`, renouvelle puis synchronise la projection ; cette synchronisation fait un upsert par planification. Chaque événement de job appelle également la synchronisation (`173–204`). Le bail vaut 90 secondes et son heartbeat 30 secondes par défaut seulement (`config.py:152–155`).

Si le pool/SQL est bloqué suffisamment longtemps, le système peut perdre sa capacité de renouvellement et arrêter les nouvelles soumissions. Il s’agit d’une dépendance vérifiée, pas d’un flap constaté. Le contrôle d’owner avant envoi, l’expiration en horloge PostgreSQL et la reprise par autre propriétaire sont des protections. Aucun réglage de bail recommandé sans budget SQL/checkout et topologie réels.

## Protections qui limitent les conclusions

- Pool fini et paramètres validés : `db.py:8–44`, size/overflow/timeout/recycle/pre-ping. Le plafond par processus n’est pas un relevé de connexions ouvertes et ne couvre pas les autres services/engines.
- Propriétaire scheduler unique comprenant PID et suffixe aléatoire : `settings.py:139–161`. Acquisition atomique du bail par upsert conditionnel, temps PostgreSQL et contrôle avant chaque job : `repository.py:29–97`, `coordinator.py:160–171`.
- Un seul exemplaire par schedule et coalescence : `coordinator.py:114,124–134`. Ce bornage empêche de décrire une file scheduler infinie simplement parce que des crons se répètent.
- Pas de session `requests.Session` mutable partagée par défaut entre jobs : `http_client.py:29–32,49`. Délais connect/read explicites, corrélation et résultat d’appel journalisés ; pas de boucle de retry HTTP immédiate dans cet adaptateur.
- Worker génération : `_PLACES_TRAITEMENT = BoundedSemaphore(2)`, acquisition non bloquante, claims commit avant calcul, executor borné et renouvellement par thread (`worker_generation_animation.py:14–56`). Ce plafond est local au processus, mais les claims et versions restent durables. Ne pas conclure à une concurrence globale égale à deux sans topologie.
- Génération et jeu : `unite_travail_generation`, `composition.py:12–18`, configure des budgets SQL locaux ; exploitation globale, lignes 78–84, utilise d’autres budgets. Ils ne deviennent pas des timeouts SQL universels pour tous les endpoints.
- CRM : `WorkerActualisationCRM.traiter_un`, `actualisation_worker.py:64–184`, réserve une unité, ferme ses transactions avant collecte externe, renouvelle les baux, borne les reprises fournisseur et persiste les reports avec jitter/Retry-After ; `traiter:201–215` borne le nombre de jobs. Ces protections ne sont pas assimilées au batch email.
- Priorité CRM : `priorite_worker.py:45–92`, au plus 25 unités, transactions distinctes, `statement_timeout`/`lock_timeout` de deux secondes par unité ; les contrôles monotones après calcul ne sont pas des interruptions CPU universelles.
- Santé des files : `_count_queue` et `_check_notification_queues`, `health_systeme.py:167–205`, comptent les anciens envois éligibles et échecs. Santé batch : derniers états, durée/retard, verrou et ordonnanceur (`batchs.py:758–853`). Le repository expose donc déjà des signaux de retard ; leur collecte/alerte effective n’est pas connue.
- L’observabilité assainit et résume les données, filtre selon niveau, corrèle les appels et borne les stacks formatées ; absence de mesures pool/CPU/RSS repérées dans les recherches ne prouve pas l’absence d’APM ou de métriques hébergeur.

## Fichiers effectivement inspectés

Lecture complète ou sections utiles affichées directement, sans import :

- Racine backend : `AGENTS.md`, `AGENT.md`, `README.md`, `logging.yaml`, `performance/README.md` ; recherche ciblée sur `.env.example` et les seuls exemples `deploy/*.example`.
- Démarrage/configuration : `app/main.py` (lifespan, montage/middlewares et recherche instrumentation), `app/config.py` (scheduler, validation et recherches timeout/worker), `app/logging_config.py`, `app/observability.py`, `app/observability_http.py`, `app/observability_instrumentation.py`.
- Scheduler : `app/infrastructure/scheduler/coordinator.py`, `http_client.py`, `settings.py`, `repository.py`.
- Traitements : `app/application/exploitation/services/batchs.py`, `app/api/emails_api.py`, `app/application/exploitation/use_cases/emails_batch.py`, `app/infrastructure/email/batch_salaries.py`, `service_envoi_email.py`, `app/domaine/exploitation/services/reservation_envoi.py` ; recherche ciblée dans `email_sortant.py` et `app/infrastructure/sms/service_envoi_sms.py`.
- SQL/capacité : `app/infrastructure/persistence/db.py`, `uow/sqlalchemy_unit_of_work.py` (construction/fermeture), `repositories/repositories_sqlalchemy.py` (repository email), `app/infrastructure/health/health_systeme.py`.
- Workers/contre-exemples : `app/application/animation_locale/services/worker_generation_animation.py`, `app/infrastructure/animation_locale/composition.py`, `app/infrastructure/prospection/actualisation_worker.py`, `app/infrastructure/persistence/priorite_worker.py` ; recherche timeout ciblée dans `fournisseurs_actualisation.py`.
- Sites d’appel : `app/api/validation_api.py`, `app/application/exploitation/use_cases/valider_prestation.py`, `app/api/maintenance_api.py`, `app/infrastructure/admin/admin.py` (recherches ciblées santé et ligne d’appel).
- Projet : README/guide transverse fourni, `prompts/02-agents.md` et `inventaire/configuration-ressources.md`, `flux-critiques.md`, `plan-orchestration-agents.md`. L’inventaire a servi à orienter la lecture, pas à remplacer la preuve source.

## Contrôles et limites

Réalisés : lectures `Get-Content` numérotées, recherches `rg` et `rg --files`, inventaire ciblé `git ls-files`, `git rev-parse HEAD`, `git status --short` backend. Certaines recherches initiales de chemins avec wildcard Windows ou noms supposés ont retourné un fichier introuvable ; elles ont été remplacées par recherches de fichiers ou dossiers existants. Aucun échec d’exécution applicative n’en découle.

Non exécutés : tests y compris isolés, compilation/import, build, générateurs, k6, profilage, mesure de logs/ressources, healthchecks, accès réseau/base/fournisseur, migration et chargement de configuration privée. Les outils performance n’ont été lus qu’en README. Le contrôle documentaire global peut être effectué par l’intégrateur ; cette annexe n’annonce aucun résultat de contrôle non exécuté.

À relever avant une mesure autorisée : commande ASGI exacte, workers/réplicas, CPU/RAM et limites de conteneur, budgets proxy, flags actifs et crons effectifs expurgés, budget total de connexions PostgreSQL et autres consommateurs, niveaux/sink de logs, tailles/âge des outbox. Leur absence empêche un avis de dimensionnement, pas les constats de mécanisme du rapport. Aucune recommandation de taille de machine ou de nombre arbitraire de workers n’est donnée.

Impact de cette livraison : uniquement deux documents dans `localeo-projet`. Sans impact d’exécution sur critères d’acceptation produit, contrats/consommateurs, migrations, paramètres ops ou générateur : aucune de ces sources n’est modifiée. Les pistes sont à instruire séparément ; aucun commit, push ou déploiement.
