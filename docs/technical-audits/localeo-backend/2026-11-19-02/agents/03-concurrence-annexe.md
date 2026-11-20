# Annexe — async et concurrence

Complément de [03-concurrence.md](03-concurrence.md). Modèle exact : **INCONNU** ; effort de raisonnement : **INCONNU**. Lecture indépendante, sans autre rapport ni mesure.

## Protections qui bornent les conclusions

- Les endpoints Live/jeu prioritaires sont majoritairement `def` : `app/api/localeo_live_api.py:511-615`, `jeu_animation_api.py:61-163`, `merchant_animation_scan_api.py:27-41`. Leur SQL consomme des threads ; cela ne prouve pas un blocage de l’event loop.
- Le dépôt d’import, `imports_commercants_api.py:258-267`, borne le fichier, déporte le service complet dans `run_in_threadpool` et ferme le fichier en `finally`.
- Jeu et scans prennent une coordination partagée, les mutations globales une coordination exclusive (`animation_locale_repositories.py:246-269`, `moteur_animation_repositories.py:29-49`). Tous les scans ne sont pas sérialisés par un verrou exclusif d’animation. Le commerce est néanmoins verrouillé pour son attestation/cadence (`repositories_sqlalchemy.py:131-135`, `validations_animation.py:114-153`) : cette garde protège des invariants et ne doit pas simplement être supprimée.
- `ServiceCommandesIdempotentesAnimation.executer`, `commandes_idempotentes.py:58-93`, conserve reçu et effets dans la même transaction ; la UoW jointe ne committe pas. `lire`, `:95-109`, essaie un verrou pour répondre EN_COURS sans attente ; l’autorisation est recontrôlée après verrouillage pour les commandes.
- `worker_generation_animation.py:17-80` réserve au plus deux places **par processus**, committe le claim avant calcul, renouvelle le bail sur un thread, puis vérifie propriétaire/version/expiration au rattachement (`:143-150`). Les claims SQL protègent entre processus. Ne pas déduire de ce worker un appel IA massif implicite : il traite aussi les étapes manuelles.
- Tirages libres : cycle de 20 s entre unités, 25 unités par défaut/100 maximum (`traitement_tirages_libres.py:5-17`), phases transactionnelles et indexation par page de 500 (`tirages_libres.py:217-271`). Ce budget n’annule pas une unité en cours. Le chemin coffrets historique `ServiceTiragesAnimation.lancer`, `tirages_animation.py:239-275`, charge au contraire sa population et crée les gains atomiquement. Vérifier type de dotation et consommateur avant toute généralisation.
- Live WebPush : tranches de 20, bail de 10 min, claim committé avant envoi, renouvellement avant abonnement, finalisation conditionnée au claim (`localeo_live_api.py:96-98`, `:1048-1232`, `:1235-1376`). Les rappels de gains utilisent un transport dédié et sont exclus de cette sélection. Pas de transaction SQL conservée pendant le transport public dans ce chemin.
- L’ordonnanceur utilise thread de coordination et pool distincts (`scheduler/coordinator.py:52-61`, `:117-128`) ; son `requests` synchrone ne tourne pas sur l’event loop. L’arrêt du lifespan utilise `asyncio.to_thread` (`app/main.py:188`, lu sans import).

## Observations secondaires

### S-CONC-01 — Autres frontières async avec travail synchrone

**FORTEMENT ÉTAYÉ PAR LE CODE**, même mécanisme que CONC-01, priorité secondaire : `images_api.py:139-174` valide/sanitize et ouvre une session SQL dans `_store_image` async ; `pwa_exploitation_api.py:602-625` appelle directement les use cases après `await request.json()` ; `admin/admin.py:11716-11725` et `:11830-11839` exécutent un batch WebPush synchrone depuis une action async ; `atelier_assiste_api.py:102-108`, `:129-190` traite ses commandes synchrones après lecture async. Une passe ciblée est justifiée, sans conclure que toutes les routes ERP sont affectées. Correction : unité de travail complète dans un thread ; effort S par frontière, contrat conservable. Aucune mesure.

### S-CONC-02 — Le BatchRunner ne renouvelle pas son bail et ne borne pas le handler serveur

**HYPOTHÈSE À VÉRIFIER**, exploitation/batches Live. `batchs.py:608-696` crée un verrou expirant à `timeout_seconds + 60`, appelle `handler()` sans timer/renouvellement, puis supprime seulement le verrou portant sa corrélation. Le read-timeout HTTP de l’ordonnanceur (`scheduler/http_client.py:45-61`) n’annule pas le traitement serveur. Pour `localeo_live.webpush.envoyer`, timeout déclaré de 300 s (`batchs.py:235-244`) ; le handler peut traiter jusqu’à 500 notifications en série et plusieurs abonnements chacune. Au-delà de 360 s, une autre exécution peut prendre le verrou. Les claims de notification apportent une protection supplémentaire : cela ne prouve pas des doublons. Le client peut aussi signaler un échec alors que le serveur poursuit. Vérifier avec fournisseur ralenti/lancement concurrent. Correction : budget serveur avec reprise durable, ou bail renouvelé et propriétaire vérifié ; effort M, risque moyen, contrat conservable.

### S-CONC-03 — La deadline WebPush exclut la résolution DNS

**HYPOTHÈSE À VÉRIFIER**, `app/security/webpush.py:33-45` : `socket.getaddrinfo` est synchrone et précède la deadline de 15 s. Les bornes connect/read ne bornent pas cette résolution. `envoyer_webpush` remplace aussi le timeout transmis (`:87-92`). Risque de retard de worker à qualifier selon DNS/runtime ; aucun blocage observé. Le transport HTTP possède des bornes et évite les retries après envoi : ne pas annoncer globalement un transport sans timeout.

### S-CONC-04 — La reprise Live concerne la notification entière

**FORTEMENT ÉTAYÉ PAR LE CODE**, `localeo_live_api.py:1287-1374` : si un abonnement échoue après un succès, la notification globale passe en erreur ; `abonnement_ids_utilises` met à jour les dates d’utilisation sans enregistrer durablement une livraison par abonnement. Une reprise peut donc réémettre sur les abonnements déjà servis. Le tag stable (`:1327`) peut atténuer les doublons visuels sans supprimer les appels fournisseur. Coût potentiel de la granularité de livraison ; pas de preuve de double effet métier. Prioriser si erreurs partielles/multiabonnements fréquents. Correction possible : état durable par abonnement, effort M, migration additive et revalidation des droits.

### S-CONC-05 (CONC-03) — Les workers d’import peuvent converger sur le même lot et suspendre sur contention

- **Statut : HYPOTHÈSE À VÉRIFIER.** Le chemin de contention est établi ; son occurrence dépend du lancement de plusieurs workers ou d’une opération concurrente. **Domaine :** import/gestion commerçants et exploitation.
- **Sources / fonctions :** `app/infrastructure/persistence/repositories/imports_commercants_repository.py:243-258`, `prochaine_operation`, `garder_budget`, `prochaine_ligne` ; `app/application/referencement/services/traitement_imports_commercants.py:14-29`, `_suspendre`, `:31-49`, `commencer`, `:51-118`, `traiter_ligne`, `:120-146`, `travailler` ; `scripts/exploitation/traiter_imports_commercants.py:12-27`.
- **Mécanisme / preuve :** la prochaine opération est choisie par `ORDER BY created_at,id LIMIT 1`, sans claim, bail ni `SKIP LOCKED`. Plusieurs processus peuvent choisir le même lot. Chaque ligne reprend les gardes de droit/identité puis flux/lot. Une candidate changée est détectée et produit `reessayer`, protégeant l’application. Mais `garder_budget` fixe `lock_timeout=3000ms` et toute exception technique dans `traiter_ligne` appelle `_suspendre`, qui suspend techniquement le lot. Une attente de verrou >3 s peut donc demander une reprise humaine sans erreur de données. `_suspendre` ouvre sa propre UoW sans réappliquer ces budgets locaux.
- **Flux / consommateur :** CLI `scripts/exploitation/traiter_imports_commercants.py --apply`, avec ou sans `--import-id`. Aucun `BatchRunner` ni singleton n’encadre ce script. Il traite les plans durables confirmés par l’API ; ce n’est pas le parsing d’un fichier dans un handler async.
- **Conséquence / déclencheur :** second lancement simultané, ou garde commune/tenant/commerce retenue par une autre opération : connexions consommées, parallélisme peu utile et suspension possible pour contention. **Pas de duplication métier démontrée** : transactions par ligne et contrôle de candidate restent protecteurs.
- **Confiance : élevée sur le code, moyenne sur le scénario opérationnel. Impact : moyen à élevé. Probabilité : inconnue**, moyenne si multiworker. **Criticité : moyenne, conditionnelle.**
- **Correction locale minimale :** distinguer les erreurs SQL transitoires de verrou/concurrence et rendre la ligne réessayable sans suspendre le lot. Pour plusieurs workers, réserver durablement une opération ou choisir un lot non pris selon une stratégie explicite, sans garder une transaction SQL ouverte pendant tout le lot. Appliquer aussi un budget à la suspension.
- **Effort : M. Risque : moyen**, ordre des gardes, permissions révoquées et reprise. **Pas de breaking change HTTP nécessaire** ; migration additive possible si claim durable. Domaines transverses : droits SaaS, référentiel, imports et exploitation. Preuves attendues : deux workers/deux lots puis même lot, garde retenue >3 s, avancement sans double effet ni suspension purement due au timeout. Non exécutées.

## Limites

Lecture ciblée des frontières async, idempotence/UoW, participation, import, génération, tirages et WebPush. Pas d’inspection de volumes, topologie déployée ou plans SQL. Le pool par défaut lu dans `app/infrastructure/persistence/db.py:33-45` est de 5 connexions +5 overflow **par processus** ; valeurs déployées inconnues. Ce défaut seul ne prouve pas un sous-dimensionnement. Aucun test, benchmark, réseau, base, serveur, dotenv ou import d’application exécuté. Aucun code applicatif modifié.

Références rectifiées par l’orchestrateur après contrôle de plage : voir validation/rectifications-references.json. Conclusions de première analyse inchangées.
