# Annexe — SRE et capacité

Complément indépendant de [06-sre.md](06-sre.md). Analyse statique uniquement, mêmes limites et révision. Aucun ancien audit ni autre rapport d'agent consulté.

## Protections réellement présentes

- `app/infrastructure/persistence/db.py:8-44` : valeurs pool validées et bornées, pré-ping, recyclage ; maximum théorique de connexions par processus = pool_size + max_overflow, soit 10 par défaut. Le nombre de processus/réplicas et `max_connections` PostgreSQL déployés restent inconnus ; aucun budget agrégé chiffrable.
- `app/infrastructure/scheduler/settings.py:139-145` : identité de propriétaire unique par PID et suffixe aléatoire. `scheduler/repository.py:34-96` : acquisition/renouvellement conditionnels en base et contrôle d'expiration ; `coordinator.py:160-172` : vérification de propriété avant soumission HTTP. Un leader distribué ne constitue toutefois pas une admission globale des requêtes déjà en cours ; arrêt scheduler avec `wait=False` (`:147-152`).
- Génération : sémaphore local non bloquant de deux places, claim committé avant calcul, renouvellement toutes les 30 s, rattachement avec vérification de bail/version (`worker_generation_animation.py:14,21-68,141-148`). Ce bornage est par processus, pas un quota global d'organisation. La perte du renouvellement n'annule pas le calcul mais le rattachement reste protégé : ce point n'est pas présenté comme perte d'intégrité.
- Moteur : `composition.py:12-18,77-84` configure des budgets SQL locaux (3 s de verrou, 15 s par instruction pour les transactions de génération, 60 s pour exploitation). Ce ne sont pas des limites globales de durée d'un lot ou de temps Python.
- Imports commerçants : `traitement_imports_commercants.py:101-123` borne de 1 à 100 lignes/passage, contrôle un budget entre unités (20 s par défaut, au plus 60 s) ; repository `imports_commercants_repository.py:251` applique 3 s verrou / 15 s SQL. Ne pas assimiler cet import borné aux générations ou aux anciens traitements CRM.
- Transport organisateur : budget global coopératif vérifié entre unités, limites de 100 et réseau hors transaction (`diffusion_messages_organisateur.py:14-68`). Activation explicitement contrôlée dans `communication_animation_batch_api.py:25,48` ; valeurs déployées inconnues.
- Push Live : claims par blocs de 20, durée de 10 min et renouvellement avant abonnement (`localeo_live_api.py:96-98,1257-1264,1298-1304`) ; finalisation séparée, abonnement expiré révoqué et revalidation métier avant envoi. Cette protection individuelle ne remplace pas le budget du cycle entier.

## Observations secondaires à vérifier

### A-SRE-01 — Le limiteur de lecture est lui-même un point SQL partagé

**HYPOTHÈSE À VÉRIFIER.** `limitation_lectures_live.py:51-83,181-205` (repository) sérialise les consommations d'origine sur la ligne singleton (`NO KEY UPDATE` pour origine existante, `FOR UPDATE` pour nouvelle allocation). Les clés personnelles existantes utilisent `KEY SHARE`, ce qui est une amélioration réelle : toutes les lectures ne prennent donc pas un verrou exclusif. Chaque origine autorisée met toutefois à jour les compteurs globaux avant commit. Verrous limités à 250 ms / instructions à 1 s. Une contention se traduit par indisponibilité et 503 (`app/api/limitation_lectures_live.py:6-18`), distincte du refus 429.

Consommateurs prouvés : lectures/pratique de participation dans `jeu_animation_api.py:64-84,131-156`. Ne pas étendre cette observation à tout le dashboard Live ni aux routes historiques sans appel du garde. Mesurer distribution du temps de verrou et du checkout de pool avant de conclure à une limite de débit ; l'attente du pool (30 s par défaut) intervient avant le budget SQL local. Amélioration éventuelle : allocation de jetons globale bornée, avec spécification de l'écart de quota autorisé et maintien du refus en cas de panne ; ne pas simplement retirer le singleton sans préserver la règle globale.

### A-SRE-02 — Le budget transport Web Push commence après DNS

**FORTEMENT ÉTAYÉ PAR LE CODE** sur le placement, impact de capacité **à vérifier** : `app/security/webpush.py:37-47` appelle `socket.getaddrinfo` avant de démarrer sa deadline de 15 s. Les connexions IP sont ensuite épinglées et bornées (`:58-91`), réponse limitée à 64 Kio, sans retry du POST : protections utiles. Le délai `kwargs['timeout']=10` (`:97-103`) ne borne pas cette résolution synchrone dans le transport personnalisé. Si DNS se bloque, un thread d'envoi reste occupé au-delà du budget annoncé. Correction ciblée : résolution dans un composant borné/cache avec expiration et capacité explicite ; préserver validation des IP publiques et épinglage TLS. Fréquence réelle et délai du résolveur système inconnus.

### A-SRE-03 — Les limites d'envoi internes ne sont pas validées comme celles du moteur

`emails_api.py:24` et `sms_api.py:16` exposent un `limit: int = 100` sans `Query(ge=1, le=...)`, contrairement à `generation_animation_batch_api.py:14` (maximum 2) et `communication_animation_batch_api.py:21-23,44-45` (maximum 100, budgets bornés). L'accès exige le scope batch ; cela n'établit ni abus ni entrée publique. Une commande interne avec un lot excessif peut prolonger SRE-01. Correction locale : bornes HTTP et garde applicative cohérentes ; compatibilité à examiner pour les commandes ops existantes.

## Vérifications recommandées, non exécutées

1. Test d'orchestration avec horloge contrôlée : handler au-delà de l'échéance et seconde invocation ; vérifier absence de concurrence non autorisée et finalisation propriétaire.
2. Faux fournisseur suspendu : constater que la correction outbox libère la connexion SQL, tout en préservant révocation, conservation et remise incertaine.
3. Scheduler avec transports retardés : vérifier budget réservé aux clôtures et compteurs d'attente/missed, sans interpréter un heartbeat actif comme preuve de ponctualité.
4. Charge SQL jetable du garde : latences checkout/verrou/instruction séparées, 429 et 503 séparés ; aucun seuil TPS avancé ici.

Aucun test ni contrôle exécutable n'a été lancé conformément au brief ; vérification limitée à lecture des sources et des références. Rapport documentaire d'audit seulement : aucun guide ni export documentaire canonique modifié.

Références rectifiées par l’orchestrateur après contrôle de plage : voir validation/rectifications-references.json. Conclusions de première analyse inchangées.
