# Audit de Localeo — sécurité, performance, fiabilité et architecture

Date : 5 septembre 2026. Révision de référence : `bee7d1a721fc77fb2df38f6daa2ec3d4d87dcc53`.

Périmètre : dépôt local `localeo-backend`, code et configurations versionnées, documentation et tests accessibles. Les modifications préexistantes de roadmap et des spécifications Epic 60 n'ont pas été modifiées. Aucun correctif applicatif n'a été appliqué. Livrables associés : [vérifications reproductibles](../../../../localeo-backend/scripts/archives/2026-09-05-verifications.py) et [résultats locaux](2026-09-05-resultats.json).

## A. Résumé exécutif

**Le risque global du code audité est élevé. Le niveau de risque réel de la production reste à confirmer.** Plusieurs protections sérieuses existent, mais certaines peuvent être contournées ou ne couvrent pas tous les parcours. Aucun incident, vol de données ni exploitation en production n'a été constaté pendant cet audit.

Localeo gère des coffrets multi-prestations, leurs achats et activations, les commerçants, les animations locales, les reversements et la facturation. Une fuite d'information ou une panne peut affecter à la fois des acheteurs, des bénéficiaires, des commerçants et l'équipe d'exploitation.

Les cinq risques prioritaires sont :

1. **Contournement du contrôle d'accès interne par confusion du chemin HTTP** : la version Starlette épinglée et le middleware de Localeo permettent de faire diverger le chemin contrôlé du chemin routé. Le mécanisme est reproduit localement ; son exploitation distante dépend du proxy. Certaines routes d'exploitation n'ont pas de contrôle de session supplémentaire.
2. **Accès d'un commerçant à une instance d'achat sans vérifier son rattachement** : la présence d'une session avec le bon scope suffit sur deux routes hybrides. L'adresse du bénéficiaire et les prestations peuvent être consultées si les identifiants de la cible sont connus.
3. **Destination webpush fournie par le client sans restriction réseau** : le serveur peut être amené à contacter une destination privée. La chaîne applicative est constatée ; l'accès réseau réel et les conditions de notification restent à vérifier.
4. **Version Starlette affectée par un déni de service sur les formulaires** : le login admin parse le formulaire avant son limiteur. L'avis éditeur s'applique à la version déclarée ; aucun test volumineux n'a été exécuté.
5. **Création de paiement externe avant validation durable de l'achat** : une panne entre Stripe et le commit peut laisser une session distante sans achat correspondant ; une nouvelle tentative peut ensuite être incompatible avec l'idempotence Stripe.

Points forts constatés :

- Séparation domaine/application/infrastructure, adaptateurs de paiement et unité de travail avec rollback.
- Jetons métier hachés, vérification de révocation et d'expiration, comparaison constante pour les jetons de gestion et clés API.
- Vérification des signatures Stripe, contrôle CSRF par origine, cookies administrateur configurés HTTPS par défaut hors développement, contrôle des hôtes.
- Lecture bornée des fichiers, exclusions de formats actifs pour les images raster, inspection documentaire et intégration antivirus avec possibilité de refus en cas d'indisponibilité.
- Outbox et mécanismes de reprise, notamment des claims renouvelables pour le webpush grand public ; coordination du scheduler par bail en base.
- Logs corrélés et masquage de nombreuses données sensibles ; gestionnaire global des erreurs techniques avec réponse générique.
- Scans Gitleaks, Bandit et pip-audit dans le workflow de sécurité ; tests métier et sécurité nombreux ; campagnes k6 encadrées.

**Actions urgentes** : durcir le contrôle de chemin et l'accès des routes internes, vérifier le filtrage du proxy, fermer l'accès inter-commerçants, restreindre les sorties webpush et protéger le login contre les corps excessifs. Préparer en parallèle une montée de version cohérente FastAPI/Starlette/SQLAdmin et la reprise des paiements.

**Estimation indicative** : 4 à 7 jours-personne pour les premières réductions de risque et vérifications ; 20 à 35 jours-personne supplémentaires pour les corrections durables, tests d'intégration et qualification du déploiement. Total de l'ordre de **25 à 45 jours-personne**, hors refonte importante, migration complexe ou incident à traiter. Les efforts par constat se recouvrent : ne pas additionner mécaniquement le tableau. Hypothèse : un développeur connaissant le dépôt, un référent exploitation et un environnement de test disponibles. Ce n'est pas un engagement de calendrier.

## Périmètre, informations manquantes et cartographie

### Conditions de fiabilité de l'audit

Avant l'analyse, les éléments manquants suivants ont été signalés : environnement réellement déployé, volumétrie, métriques, configuration d'infrastructure et preuves de restauration. Ils empêchent de mesurer la performance de production ou de certifier sa sécurité ; ils n'empêchent pas l'identification de défauts dans le code.

N'ont pas été consultés : fichiers `.env`, secrets des plateformes, bases métier, fichiers stockés, journaux utilisateurs, historique Git à la recherche de secrets ou données personnelles. Aucun serveur applicatif n'a été démarré, aucune requête envoyée à Localeo/Stripe/Brevo, aucune migration ou campagne de charge exécutée. Les seules consultations réseau sont des sources publiques officielles sur les dépendances et les recommandations.

Le dépôt est un **monolithe modulaire Python/FastAPI**, avec SQLAlchemy synchrone et PostgreSQL, SQLAdmin, APScheduler, Pydantic, Stripe, Brevo, webpush et stockage documentaire compatible S3. Render est prévu dans la configuration et le guide agent ; le déploiement effectif n'a pas été inspecté. Les interfaces PWA embarquées sont dans le périmètre ; le frontend marketplace complet n'est pas disponible dans ce dépôt.

```text
Acheteur / bénéficiaire / commerçant / gestionnaire / opérateur
                       |
          Proxy et terminaison TLS [non inspectés]
                       |
                    FastAPI
        /public   /protected   /internal   /admin
                       |
   Dépendances d'identité + middleware + services métier
                       |
       SQLAlchemy / PostgreSQL / stockage documentaire
                       |
       Stripe Checkout/Connect — Brevo — services Push
                       ^
          Outbox / batchs / scheduler avec bail
```

Les préfixes `/protected` et `/internal` ne constituent pas à eux seuls une autorisation. Les frontières à vérifier sont l'identité de l'appelant, son scope, le propriétaire de la ressource, la commune ou le tenant et l'état métier de l'objet.

Flux critiques examinés : initialisation d'achat, consultation après Checkout, consultation hybride commerçant/acheteur, webhook de paiement, webhooks Connect, notifications, session admin, limitation d'authentification, documents, audit, migrations et orchestration des batchs. Les contrôles d'animation et de facturation ont été échantillonnés ; chaque règle de chaque route n'a pas fait l'objet d'un test d'intégration.

Mesures structurelles par AST : **514 fichiers Python applicatifs, 450 sous `tests`, 15 scripts ; 468 déclarations de routes HTTP dont 81 asynchrones.** Ce nombre inclut les déclarations présentes dans le code, sans garantir leur montage effectif. Le nombre de fichiers de tests n'est ni un nombre de tests exécutés ni un taux de couverture.

## B. Tableau des constats

Criticité = conséquence plausible dans le périmètre indiqué. Probabilité = appréciation qualitative avec préconditions. Confiance : **C** confirmé par le code ou une preuve locale ; **P** fortement probable, validation d'intégration manquante. Les conditions de production sont détaillées sous chaque constat. P0 : traiter immédiatement ; P1 : prochain cycle, sous 30 jours ; P2 : sous 90 jours.

| ID | Domaine | Constat | Preuve principale | Criticité | Impact | Probabilité | Correction | Effort | Priorité | Confiance |
| -- | ------- | ------- | ------ | --------- | ------ | ----------- | ---------- | ------ | ------ | ------ |
| F01 | Sécurité | Chemin interne contournable via Host malformé | `app/main.py:295`, `app/api/pwa_exploitation_api.py:565`, preuve locale | Élevée | Lecture d'informations d'exploitation sans session | Moyenne, si le proxy laisse passer le Host | Contrôler `scope['path']`, dépendances de session et version corrigée | 1–3 j hors migration groupée | P0 | C pour le mécanisme |
| F02 | Sécurité | Consultation hybride sans lien commerçant–achat | `app/security/management_token.py:107`, `app/api/achats_api.py:109` | Élevée | Données de bénéficiaires et prestations hors périmètre | Moyenne, session et IDs connus requis | Principal typé et contrôle de rattachement | 2–4 j | P0 | C |
| F03 | Sécurité | SSRF potentielle via endpoint webpush | `app/api/localeo_live_api.py:91,316,1180`, `live_tracking_webpush.py:143,323` | Élevée | Requêtes serveur vers réseau privé, indisponibilité | Moyenne, envoi effectif et egress requis | Hôtes autorisés, contrôle DNS/redirects et filtrage réseau | 2–4 j | P0 | C pour le flux, P pour exploitation |
| F04 | Sécurité/disponibilité | Starlette vulnérable aux formulaires urlencoded | `requirements.txt:2`, `app/infrastructure/admin/auth.py:62` | Élevée | Épuisement CPU/mémoire avant authentification | Élevée si login public sans protection amont | Limites avant parsing et migration compatible | 3–6 j, partagé F01/F13 | P0 | C version et appel concernés |
| F05 | Sécurité/concurrence | IP déclarative et compteur non atomique | `app/audit.py:12`, `service_rate_limit_authentification.py:42`, `repositories_sqlalchemy.py:696` | Moyenne | Contournement des seuils d'authentification | Moyenne à élevée selon proxy/concurrence | IP issue du transport validé, compteur atomique, limites multicritères | 2–4 j | P1 | C IP, P dépassement concurrent |
| F06 | Fiabilité/paiement | Effet Stripe avant commit de l'achat | `initialiser_paiement.py:272,351,399` | Élevée | Checkout orphelin, achat bloqué, support financier | Moyenne lors de panne/timeout | Achat durable, état de reprise et clé Stripe stable | 4–7 j | P1 | P pour panne de bout en bout |
| F07 | Fiabilité/performance | Webpush commerçant sans reprise des EN_COURS ni timeout explicite | `live_tracking_webpush.py:323,363,372,376,398` | Élevée | Notifications perdues ou worker/connexion immobilisés | Moyenne lors d'arrêt ou provider lent | Claims expirables, timeout, I/O hors transaction, suivi par abonnement | 3–5 j | P1 | C structure, P incident |
| F08 | Performance/disponibilité | I/O synchrones dans handlers async | `app/api/stripe_connect_api.py:40`, `app/infrastructure/admin/auth.py:61`, `app/api/documents_api.py:156` | Moyenne | Retard des autres requêtes du même worker | Élevée dès qu'une I/O attend | Déporter l'unité synchrone entière dans le pool de threads | 2–4 j | P1 | C structure, impact non chronométré |
| F09 | Sécurité/configuration | Mot de passe admin par défaut accepté si login renommé | `app/config.py:567` | Élevée si mal configuré | Compromission du compte admin | Faible à moyenne ; configuration réelle inconnue | Tester le mot de passe indépendamment du login | 0,5–1 j | P0 | C |
| F10 | Sécurité/abus | Paiement et support publics sans limiteur visible | `app/api/paiements_api.py:12`, `app/api/contacts_api.py:34` | Moyenne | Spam support, gonflement DB/outbox, appels Stripe | Élevée sans limitation amont | Quotas avant effets coûteux et contrôles anti-abus | 1–3 j | P1 | C absence applicative, exposition à vérifier |
| F11 | Performance | Une lecture repository par prestation | `lister_prestations_coffret_instance_achat.py:25`, `repositories_sqlalchemy.py:167` | Moyenne | Latence linéaire avec nombre de prestations | Élevée sur ce parcours ; enjeu selon taille réelle | Chargement groupé/projection | 0,5–1 j | P2 | C, comptage local |
| F12 | Performance | Écriture de la même clé API à chaque requête | `app/security/api_keys.py:54` | Moyenne | Sérialisation d'UPDATE sur clé partagée | Moyenne si appels concurrents | Mise à jour espacée et atomique de last_used_at | 0,5–1 j | P2 | C écriture, P contention |
| F13 | Livraison | Résolution non figée et absence de job pytest dans la CI visible | `requirements.txt:1`, `.github/workflows/security.yml:1` | Moyenne | Builds divergents, régressions non bloquées | Moyenne | Verrouillage transitif, tests CI, checks requis | 2–4 j | P1 | C dépôt, CI externe inconnue |
| F14 | Sécurité/données | Session Checkout utilisée comme capacité de lecture et journalisée | `achats_api.py:38`, `consulter_achat_depuis_session_checkout.py:17,24` | Moyenne | Consultation personnelle après fuite d'un identifiant Checkout | Moyenne pour lecteur de logs ; ID non devinable supposé | Échange limité vers jeton local, masquage et no-store | 2–4 j | P1 | C chemin et log, durée distante inconnue |
| F15 | Traçabilité | Acteur d'audit fourni par X-Actor-ID prioritaire | `app/audit.py:24,59` | Moyenne | Attribution trompeuse d'une action sensible | Élevée pour un appelant autorisé pouvant choisir l'en-tête | Acteur issu du principal validé ; déclaration séparée | 1–2 j | P1 | C |

### F01 — Confusion du chemin utilisé pour protéger les routes internes

Règle de revue : FASTAPI-AUTH-001. `protect_internal_backoffice_routes` prend `request.url.path` (`app/main.py:295`) et applique ensuite `startswith('/internal/')`. Les routes `resume_jour` et `evenements` (`app/api/pwa_exploitation_api.py:565,570`) délèguent aux services sans dépendance de session propre. Leur router n'en impose pas non plus.

Starlette 0.50.0 reconstruit l'URL à partir du Host ; son TrustedHostMiddleware compare la partie située avant le premier deux-points. Cela permet à un Host contenant un port suivi d'un faux chemin de satisfaire la liste d'hôtes tout en modifiant `request.url.path`. Sources : [TrustedHostMiddleware 0.50.0](https://raw.githubusercontent.com/Kludex/starlette/0.50.0/starlette/middleware/trustedhost.py), [URL 0.50.0](https://raw.githubusercontent.com/Kludex/starlette/0.50.0/starlette/datastructures.py). L'éditeur documente ce mécanisme dans [CVE-2026-48710](https://github.com/Kludex/starlette/security/advisories/GHSA-86qp-5c8j-p5mr), corrigé à partir de 1.0.1.

La preuve `F01_host_path` utilise une adresse `.test` et le middleware réel extrait par AST : chemin normal → 401 ; chemin reconstruit à partir d'un Host malformé → fonction suivante atteinte, sans session. La transformation Starlette est reproduite d'après ses sources ; Starlette lui-même n'est pas installé. **Il ne s'agit pas d'une preuve HTTP derrière le proxy de production.** Les routes munies d'une dépendance de session supplémentaire restent protégées contre ce seul contournement.

Correction : utiliser le chemin ASGI pour l'autorisation et ajouter une dépendance obligatoire à chaque router interne sensible ; conserver une liste explicite des seules ressources statiques publiques. Tester aussi `/admin/internal/`, les slashs et les chemins encodés. Mesure compensatoire : limiter immédiatement l'accès réseau à l'exploitation, rejeter les Host invalides au proxy et vérifier le comportement du proxy avec un petit test sur une cible isolée.

### F02 — Accès inter-commerçants aux coffrets d'achat

Règle : FASTAPI-AUTH-001, contrôle d'accès objet. Dans `require_bearer_or_management_token_for_achat`, la branche commerçant retourne `VerifierSessionCommercant(...).execute(...)` sans vérifier `achat_id` contre le commerçant. Le vérificateur contrôle bien état, expiration et scope (`verifier_session_commercant.py:25`), mais ne reçoit aucun achat.

Les routes de détail d'instance et de prestations ignorent ce principal via `_ = Depends(...)` (`app/api/achats_api.py:109,155`). Le service de détail vérifie seulement que l'instance appartient à l'achat, puis retourne `email_beneficiaire` (`consulter_coffret_instance_achat.py:7`). Le service de prestations retourne les statuts et IDs des commerçants sans filtrage par appelant.

Preuve locale : une session simulée du commerçant A est acceptée pour l'achat B, et la définition réelle du service retourne le champ bénéficiaire de B. Préconditions : session valide avec scope `commercant:validation`, identifiants valides connus et objet existant. Aucun mécanisme d'énumération massive des UUID n'est démontré ; aucun droit d'écriture supplémentaire n'est établi.

Correction : conserver un principal discriminant acheteur et commerçant, vérifier l'appartenance métier et minimiser la réponse commerçant. Clarifier si le scan doit autoriser un commerçant sans prestation dans le coffret ; même dans ce cas, définir explicitement quels champs lui sont nécessaires. Compensation : désactiver temporairement la branche commerçant sur ces lectures après adaptation du parcours de scan. Validation : matrice A/B, achat particulier/professionnel, jeton acheteur valide, expiré et révoqué, instance d'un autre achat.

### F03 — Destination réseau webpush non maîtrisée

Règle : prévention SSRF. `CreerAbonnementLiveRequest.endpoint` est une chaîne avec longueur minimale (`app/api/localeo_live_api.py:91`). La route publique peut créer une installation puis stocke directement l'endpoint (`:316–343`). Le batch transmet cette valeur à `webpush` (`:1180`). Le parcours commerçant ne vérifie que la présence de l'endpoint et des clés (`live_tracking_webpush.py:143–169`), puis transmet également l'endpoint au provider (`:323`).

La vérification locale confirme qu'une destination privée synthétique atteint le faux provider. Aucun paquet réseau n'est envoyé. Pour une exploitation réelle, il faut des clés de souscription valides, une configuration VAPID active, une notification à envoyer et une sortie réseau autorisée. La méthode et le corps sont contraints par webpush : **ni lecture arbitraire de fichiers, ni récupération de métadonnées cloud, ni exfiltration d'une clé privée ne sont démontrées**.

Correction : liste d'hôtes de services push nécessaires, HTTPS, ports autorisés, absence d'identifiants dans l'URL, contrôles de résolution et des redirections au moment de l'envoi. Bloquer les réseaux privés et sensibles au niveau egress en défense supplémentaire. La [fiche SSRF OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) recommande notamment une validation applicative et réseau, et de traiter les redirections/DNS. Ne pas considérer un simple `startswith('https://')` comme suffisant. Compensation : désactiver l'envoi des abonnements non validés. Validation en environnement isolé avec doubles HTTP, DNS et redirections, sans cible réelle.

### F04 — Déni de service lors du parsing des formulaires

Règle : FASTAPI-DEPLOY, bornage des ressources. Le dépôt impose `starlette==0.50.0`. L'avis [CVE-2026-54283](https://github.com/Kludex/starlette/security/advisories/GHSA-82w8-qh3p-5jfq) affecte les versions de 0.4.1 incluse à 1.3.1 exclue : les limites de formulaire ne s'appliquent pas correctement au format urlencoded. Le correctif éditeur commence en 1.3.1.

`AdminAuthBackend.login` appelle `await request.form()` avant la vérification du débit. Aucun middleware global limitant les octets reçus n'apparaît dans `app/main.py`. Les limites de lecture d'UploadFile sont utiles, mais interviennent après le parsing du formulaire et ne couvrent pas ce problème.

Correction : plafonner le corps avant parsing, y compris les requêtes sans Content-Length, et mettre à niveau la pile. Ne pas forcer isolément Starlette 1.x : [FastAPI 0.128.0 déclare Starlette <0.51.0](https://raw.githubusercontent.com/fastapi/fastapi/0.128.0/pyproject.toml). Choisir et tester un ensemble compatible avec SQLAdmin, puis le figer. Compensation : seuil bas propre au login, rejet précoce et limitation de débit au proxy. Validation : petits dépassements de limites dans un test local, pas un payload volumineux ni un test de saturation.

### F05 — Limitation d'authentification fragile

Règle : prévention des abus. `extract_client_ip` privilégie sans vérification `X-Forwarded-For`, puis `X-Real-IP`. Le login admin utilise cette valeur dans le compteur. La preuve locale montre qu'une adresse déclarée remplace celle du transport. Si le proxy conserve l'en-tête arbitraire, changer cet en-tête change de compartiment de limitation. La normalisation du proxy n'est pas connue. `appliquer_rate_limit_public`, qui utilise `request.client.host`, n'est pas concerné par cette même extraction directe.

Le compteur suit un schéma lire–modifier–écrire sans verrou visible (`service_rate_limit_authentification.py:42–74`, `repositories_sqlalchemy.py:696–729`). Sa contrainte unique inclut `window_start` (`models.py:808`) : deux créations concurrentes avec des horodatages différents ne désignent pas nécessairement la même fenêtre. Des mises à jour peuvent également perdre un incrément. Ce dépassement concurrent est fortement probable mais non reproduit sur PostgreSQL.

Correction : configurer les proxies de confiance au serveur ASGI, utiliser l'adresse transport ainsi normalisée, incrément atomique sur une fenêtre stable, plafonds par compte et par origine. Compensation : quota au proxy. Tests : en-têtes forgés, proxy légitime, deux workers et tentatives parallèles à la limite, en base de test jetable.

### F06 — Paiement et transaction locale ne se reprennent pas de façon durable

`InitialiserPaiement.execute` crée un nouvel UUID d'achat (`:272`), ajoute l'objet, appelle Stripe (`:351–363`) puis commit (`:399`). `SqlAlchemyUnitOfWork.__exit__` rollback en cas d'exception. La clé d'idempotence est optionnelle dans l'API ; quand elle est fournie, elle est transmise à Stripe avec des métadonnées contenant l'UUID nouvellement créé (`paiement_gateway.py:36–49`).

Scénario plausible : Stripe crée le Checkout ; la réponse réseau est perdue ou le commit échoue ; l'achat disparaît par rollback. Au rejeu, un UUID différent est produit. Sans clé, un second Checkout peut être créé ; avec la même clé, des paramètres différents peuvent empêcher la reprise. Une session distante peut aussi référencer un achat inexistant. **Aucun double débit n'a été constaté et une création de Checkout n'est pas à elle seule un débit.**

Le paiement intégral par crédit B2B appelle aussi `ValiderPaiement` après le commit (`:400–407`) : vérifier la reprise d'un arrêt à cet endroit. Correction : état durable d'initialisation, clé provider liée à un identifiant stable, reprise/réconciliation des appels ambigus et distinction claire entre réservation et confirmation. Compensation : suivi des achats en attente et réconciliation des Checkout ; ne pas relancer automatiquement avec une nouvelle clé. Tests avec gateway factice réussissant puis faute au commit, timeout après création distante, rejeu simultané et arrêt avant confirmation crédit.

### F07 — Notifications commerçant bloquées après interruption

Le batch sélectionne `A_ENVOYER` et `ECHEC_TEMPORAIRE`, marque toutes les lignes `EN_COURS_ENVOI`, puis commit avant de les traiter (`live_tracking_webpush.py:355–377`). Aucun retour automatique des lignes `EN_COURS_ENVOI` vers les candidates n'apparaît dans ce module. Un arrêt après ce commit laisse donc jusqu'au lot réclamé hors de la sélection des relances. Le verrou global de BatchRunner protège les exécutions ordinaires, mais ne répare pas l'état des notifications.

Les appels provider se font ensuite à l'intérieur d'une unité de travail avec connexion SQL utilisée, et sans timeout applicatif explicite. La [documentation pywebpush](https://github.com/web-push-libs/pywebpush) prévoit un paramètre timeout ; sa valeur effective dépend de la version résolue, non installée ici. Ne pas supposer une absence absolue de timeout interne. Plusieurs abonnements sont envoyés séquentiellement et l'état d'envoi n'est finalisé qu'au niveau notification : un échec partiel peut provoquer un renvoi aux destinataires déjà servis.

Correction : reprendre le mécanisme de claim expirant et renouvelable déjà présent dans `localeo_live_api.py`, envoyer hors transaction SQL, borner le temps réseau et suivre les résultats par abonnement. Compensation : procédure de détection des EN_COURS anciens, reprise contrôlée avec risque de doublon documenté. Tests : arrêt après claim, provider lent, bail expiré, perte du claim, envoi partiel et redémarrage. Ne pas rejouer en masse les lignes de production sans validation des conséquences métier.

### F08 — Blocage potentiel de la boucle asynchrone

Le webhook Connect est `async def` mais appelle directement des services SQLAlchemy synchrones (`stripe_connect_api.py:40–52`). Le login admin et certains uploads documentaires combinent aussi attente asynchrone puis SQL, inspection ou stockage synchrone. À l'inverse, le webhook plateforme utilise déjà `run_in_threadpool` (`stripe_platform_api.py:72–81`).

Lorsqu'un appel synchrone attend la base ou un tiers dans le thread de l'event loop, les autres requêtes de ce worker attendent également. La durée réelle n'a pas été mesurée. Déporter l'opération synchrone complète, avec création et fermeture de sa session SQL dans le même thread ; ne pas partager une session vivante entre threads. Compensation : réduire l'exposition/concurrence des routes coûteuses et surveiller event-loop lag et pool SQL. Tester une I/O factice temporisée en concurrence avec une route légère ; qualifier p95/p99 ensuite sur cible isolée.

### F09 — Garde de configuration admin incomplète

`_is_weak_admin_config` considère les identifiants faibles seulement si **login et mot de passe** sont simultanément ceux par défaut. Renommer le login tout en conservant le mot de passe par défaut désactive donc ce signal, à secret de session distinct. La preuve utilise exclusivement des valeurs synthétiques.

Correction : refuser le mot de passe par défaut indépendamment du nom d'utilisateur et définir une politique de longueur/robustesse des secrets. Vérifier sans divulgation les paramètres de production et les éventuels comptes partagés. Compensation : protéger l'admin par contrôle réseau ou identité fédérée et changer un mot de passe faible s'il est effectivement utilisé. Tests unitaires : nom renommé + mot de passe par défaut, nom standard + mot de passe fort, absence de secret et environnement de développement explicitement autorisé. L'usage d'un mot de passe faible réel n'est pas établi.

### F10 — Actions publiques coûteuses sans protection anti-abus locale

L'initialisation de paiement n'applique pas le limiteur public déjà utilisé ailleurs. Le support consommateur non authentifié crée des messages, prépare un email support et une notification d'exploitation (`creer_message_contact_consommateur.py:132–167`) sans limiteur visible. Le caractère public de ces fonctionnalités est légitime ; l'absence de quota est le risque.

Une répétition de requêtes valides peut multiplier les écritures et appels tiers. L'idempotence optionnelle du paiement ne constitue pas une limitation face à un appelant qui change ou omet sa clé. Correction : quota par origine et contexte pertinent, bornes de taille et anti-automatisation graduée avant tout effet coûteux. Compensation : règles ciblées au proxy. Tests : petites séries en mémoire avec faux providers et compteur d'effets, rejet 429 avant création de Checkout/outbox. Éviter le blocage global de tous les utilisateurs partageant une adresse réseau.

### F11 — Lectures N+1 sur les prestations

Après lecture de l'instance et des statuts, une compréhension appelle `uow.prestations_coffret.obtenir` pour chaque ligne (`lister_prestations_coffret_instance_achat.py:25–28`). Le repository fait un `session.get` individuel (`repositories_sqlalchemy.py:167`). Pour des IDs distincts non déjà chargés, cela entraîne des recherches SQL individuelles.

Mesure locale : 1/10/100 prestations → 1/10/100 appels individuels, en plus des deux lectures préalables. **Ce sont des appels à un repository factice, pas des requêtes PostgreSQL chronométrées.** L'impact probable est un coût croissant avec N ; l'urgence dépend du nombre réel de prestations et de la latence DB.

Correction : lecture groupée des IDs ou projection jointe des champs nécessaires. Tester l'identité des réponses, les prestations manquantes et un nombre de requêtes borné avec instrumentation SQL. Aucune nécessité de cache ni d'index supplémentaire n'est démontrée ici.

### F12 — Mise à jour systématique de la clé API

Chaque authentification valide met à jour `last_used_at` puis commit (`app/security/api_keys.py:54–56`). Des requêtes simultanées utilisant la même clé écrivent la même ligne, y compris pour des consultations. L'écriture est confirmée ; son coût et la contention ne sont pas mesurés.

Correction : mise à jour conditionnelle espacée, atomique, ou agrégation de l'usage hors du parcours principal. Ne pas mettre en cache aveuglément l'état actif/scope, au risque de retarder une révocation. Compensation : clés par composant appelant et mesure des attentes de verrous. Validation : compteur d'UPDATE, révocation immédiatement respectée et concurrence avec une clé partagée.

### F13 — Reproductibilité et barrière CI incomplètes dans le dépôt

`requirements.txt` contient des intervalles et au moins une dépendance sans version (`itsdangerous`). Aucun lock transitif avec hashes n'est visible parmi les fichiers suivis inspectés. Deux installations peuvent donc diverger. Le seul workflow versionné trouvé effectue Gitleaks, pip-audit et Bandit ; il ne lance pas pytest, les migrations ou un démarrage isolé. Une pipeline externe et les checks requis de branche peuvent exister : ils n'ont pas été consultés.

Les avis F01/F04 sont des problèmes identifiés séparément ; **aucune prétention à un scan CVE exhaustif des dépendances transitives**. Ni pip-audit ni Bandit n'ont été exécutés localement. Correction : lock reproductible, mise à jour encadrée, audit du graphe installé, job de tests isolés et validation des migrations sur PostgreSQL jetable. Pour la supply chain, figer les actions/images à des identifiants immuables et contrôler les mises à jour. Compensation : exiger provisoirement une preuve de qualification associée au commit avant promotion.

### F14 — Capacité de lecture Checkout insuffisamment cloisonnée

`GET /protected/gestion-achats/achats/depuis-session/{session_id}` n'exige pas de jeton local (`achats_api.py:38`). Le service récupère la session Stripe, lit son `achat_id`, puis retourne le détail de l'achat. Ce détail contient notamment email et téléphone de l'acheteur (`consulter_detail_achat_coffret.py:33–52`). Aucun contrôle de révocation/expiration du management token n'est effectué sur ce chemin alternatif.

L'identifiant Checkout est journalisé dans un message INFO (`consulter_achat_depuis_session_checkout.py:17`). Le masquage des champs structurés contenant `session` existe, mais les expressions de masquage de texte libre ne retirent pas cet identifiant : reproduction locale avec un identifiant entièrement synthétique. Les lecteurs des logs peuvent ainsi posséder une capacité de consultation pendant la période où la récupération Stripe reste possible. Aucune durée illimitée de récupération côté Stripe n'est affirmée.

Correction : échange initial étroitement limité vers un jeton local borné et révocable, minimisation de la réponse, suppression de l'identifiant des messages libres et des logs d'accès amont, `Cache-Control: no-store` sur les réponses sensibles. Compensation : restreindre l'accès aux logs et leur conservation ; ne pas extraire de vrais IDs pour vérifier ce constat. Tests : callback initial autorisé, rejeu après expiration/révocation refusé selon contrat, logs synthétiques masqués. Préserver le parcours de retour de paiement pendant la migration.

### F15 — Journal d'audit attribuable par l'appelant

`resolve_actor` accepte `X-Actor-ID` avant toute identité tirée des mécanismes d'authentification. `log_sensitive_action` utilise ce résultat lorsqu'aucun acteur explicite n'est passé. La preuve locale montre qu'une valeur arbitraire devient l'acteur. Certaines autres routes passent déjà un principal de clé API validé : elles ne sont pas concernées par ce seul défaut.

Impact : fausse attribution d'une consultation ou action dans l'audit, sans gain de privilège HTTP. Correction : acteur obtenu depuis le principal validé, déclaration client conservée seulement dans un champ distinct si utile et borné. Compensation : supprimer l'en-tête au proxy et corréler avec un identifiant serveur ; cela ne remplace pas le correctif applicatif. Tests : X-Actor-ID contradictoire, clé API, session commerçant, session admin, token acheteur et événement anonyme.

## C. Plan d'action priorisé

### Immédiat — sous 48 heures

- Responsable backend + exploitation : traiter F01 au niveau application et vérifier le filtrage Host ; restreindre l'accès interne jusqu'à qualification. Critère : la route d'exploitation refuse toute requête sans session, indépendamment du Host ou de l'alias.
- Responsable backend : fermer F02 après validation du contrat métier minimal de scan. Critère : un commerçant hors périmètre ne reçoit aucun champ bénéficiaire.
- Responsable exploitation : limiter les sorties webpush aux services requis ou suspendre les envois non vérifiés (F03).
- Responsable exploitation + backend : borner le corps du login avant parsing et préparer la migration compatible F04. Critère : dépassement faible rejeté avant authentification, sans charge.
- Responsable exploitation : contrôler de façon non divulguante le mot de passe admin ; corriger le garde F09.
- Responsable backend : retirer les identifiants Checkout des messages de logs F14 ; documenter les mesures compensatoires effectives.

### Court terme — sous 30 jours

- Qualifier et déployer le couple FastAPI/Starlette/SQLAdmin corrigé, avec graphe de dépendances figé et tests CI (F04/F13).
- Rendre l'initialisation du paiement durable et reprenable (F06), avec cas d'échec après effet distant.
- Corriger le cycle des notifications commerçant, les timeouts et les transactions longues (F07).
- Déporter les I/O synchrones des handlers async sensibles (F08).
- Fiabiliser la limitation d'authentification et couvrir paiement/support (F05/F10).
- Uniformiser les capacités de consultation et les acteurs d'audit (F14/F15).
- Exécuter les tests PostgreSQL réels de concurrence sur une base jetable, établir un premier profil de performance et confirmer les contrôles amont.

### Moyen terme — sous 90 jours

- Selon mesures, supprimer le N+1 et les UPDATE excessifs des clés API (F11/F12).
- Extraire les parcours admin/notifications au fur et à mesure des correctifs, avec tests de contrat ; ne pas entreprendre de réécriture globale.
- Formaliser puis tester restauration base + objets + configuration, RPO/RTO et procédure de rollback.
- Qualifier les droits par commune/tenant sur l'ensemble des routes et la révocation des sessions admin.
- Établir l'inventaire des données personnelles, durées de conservation, purges et accès aux audits/exports.

### Amélioration continue

- Scans de dépendances planifiés, mises à jour régulières et checks requis à la fusion.
- Tests négatifs d'autorisation et de panne pour chaque nouveau parcours sensible.
- Tableau de bord : latence par route, erreurs, attente du pool SQL, event-loop lag, âge des outbox, paiements en attente et échec de réconciliation.
- Exercices de restauration et revue des accès opérateurs ; campagnes de charge uniquement sur cibles explicitement autorisées.

Corrections rapides à fort bénéfice : F09 (garde indépendant du login), F01 (chemin ASGI et session de router), F14 (journalisation), F08 sur le webhook Connect en réutilisant le modèle plateforme. Ces actions restent à tester et à valider ; elles n'ont pas été appliquées.

## D. Correctifs proposés — exemples à adapter, non appliqués

### D1. Autorisation interne indépendante du Host

```python
# Dans le middleware : utiliser le chemin routé, y compris après réécriture.
path = request.scope.get("path", "")

# Sur les routes internes de données : dépendance de session obligatoire.
data_router = APIRouter(
    prefix="/internal/exploitation/pwa/api",
    dependencies=[Depends(require_admin_session)],
)
```

Conserver les exceptions statiques sur un router distinct. Effet secondaire : les outils internes qui accédaient sans session doivent être authentifiés. Validation : tests TestClient/ASGI avec Host normal, port, caractères interdits, alias `/admin/internal/`, absence de cookie et session valide. Vérifier ensuite la chaîne proxy sur une instance isolée, sans récupérer de données métier réelles.

### D2. Identité et périmètre objet explicites

```python
# Pseudocode : helpers et type Principal à créer selon le contrat métier.
principal = authentifier_acheteur_ou_commercant(request)
instance = charger_instance_dans_achat(achat_id, instance_id)
if principal.kind == "commercant":
    exiger_prestation_du_commercant(instance, principal.commercant_id)
    return projection_scan_minimale(instance, principal.commercant_id)
exiger_jeton_de_gestion(principal, achat_id)
return projection_acheteur(instance)
```

Effet secondaire : certaines réponses commerçant auront moins de champs. Faire évoluer le client et tester A/B, champs personnels et liens d'appartenance. Un UUID opaque ne remplace pas ce contrôle.

### D3. Refus du mot de passe par défaut

```python
def _is_weak_admin_config() -> bool:
    return (
        ADMIN_PASSWORD == DEFAULT_ADMIN_PASSWORD
        or not ADMIN_PASSWORD
        or ADMIN_SESSION_SECRET in {None, DEFAULT_ADMIN_SESSION_SECRET}
    )
```

Ajouter séparément les contrôles de robustesse nécessaires ; cet exemple corrige le défaut logique précis, pas toute la politique d'identité. Effet secondaire attendu : un déploiement auparavant accepté peut refuser de démarrer. Vérifier sa configuration sans afficher les valeurs avant promotion ; conserver le mécanisme explicite de développement si le contrat le prévoit.

### D4. Webhook Connect hors event loop

```python
async def webhook_stripe_connect(request, stripe_signature):
    payload = await lire_corps_borne(request)  # helper à implémenter
    return await run_in_threadpool(
        verifier_et_traiter_connect, payload, stripe_signature
    )

def verifier_et_traiter_connect(payload, signature):
    event = StripeConnectGateway().verifier_webhook_connect(payload, signature)
    return traiter_evenement_compte_connecte(event)
```

Conserver signature, journalisation utile et codes d'erreur. La session SQL doit naître et se fermer dans le worker. Effet secondaire : consommation du pool de threads, qui doit rester cohérente avec le pool DB. Régression : signature invalide, événement ignoré, événement dupliqué, exception SQL et appel concurrent léger.

### D5. Claims et appels webpush bornés

```text
Transaction courte : sélectionner des candidats avec verrou adapté,
attribuer claim_id + expiration et enregistrer la tentative ; commit.
Hors transaction : valider destination et envoyer avec timeout explicite.
Transaction courte : finaliser seulement si claim_id est toujours propriétaire.
Reprise : rendre éligibles les claims expirés, avec limite de tentatives.
```

Réutiliser le code grand public déjà présent plutôt que créer un troisième moteur de queue. Ajouter un résultat par abonnement pour les échecs partiels. Effet secondaire : la livraison reste généralement « au moins une fois » ; prévoir déduplication côté client quand possible, sans promettre exactement une fois. Validation : arrêt après chaque frontière de transaction, bail renouvelé/perdu, timeout et envois partiels.

### D6. Achat durable avant effet externe

```text
1. Transaction : créer ou retrouver l'achat via une clé métier unique,
   conserver son UUID et son état PAYMENT_INITIALIZING ; commit.
2. Appeler Stripe avec une clé dérivée de cet UUID et de l'opération.
3. Transaction : enregistrer checkout/session et état ; commit.
4. Après résultat ambigu : rejouer la même opération ou réconcilier,
   sans créer une nouvelle identité d'achat.
```

Cette modification demande une machine d'états et un traitement des réservations B2B. Elle peut créer des lignes d'initialisation abandonnées à purger/réconcilier. Tester la perte de réponse Stripe, un commit rejeté, deux requêtes simultanées et un webhook arrivant avant l'étape 3. Un mock Stripe doit mémoriser les appels pour détecter les doubles créations.

## E. Niveau de confiance, couverture et limites

### Vérifications réellement exécutées

La bibliothèque standard de Python 3.12.14 a été utilisée avec `-B`. L'environnement de travail n'a pas FastAPI, SQLAlchemy, pytest, psycopg, requests ou pywebpush installés dans cet interpréteur. Aucune installation ni import de `app.main` n'a été effectué.

Le script extrait les seules définitions nécessaires par AST, injecte des dépendances factices et interdit les connexions socket ainsi que la résolution DNS. Il ne charge pas `.env`, ne contacte pas de DB et n'écrit aucune donnée métier. Il exécute **sept vérifications**, toutes reproduisant le comportement décrit :

| Vérification | Résultat | Limite de la preuve |
| --- | --- | --- |
| F01 Host/chemin | 401 normal ; middleware traversé avec chemin reconstruit | Transformation Starlette modélisée depuis source officielle ; proxy non testé |
| F02 autorisation hybride | Principal A accepté pour achat B ; champ bénéficiaire retourné | Authentification valide simulée ; absence de test HTTP complet |
| F05/F15 en-têtes | IP et acteur déclaratifs retenus | Normalisation réseau de production inconnue |
| F09 configuration | Renommer le login neutralise le garde du mot de passe par défaut | Toutes les valeurs sont synthétiques |
| F11 cardinalité | 1, 10, 100 lectures individuelles pour 1, 10, 100 prestations | Pas de latence ni plan PostgreSQL mesurés |
| F03/F07 provider | Destination privée passée au faux provider ; timeout non fourni | Pas de chiffrement push ni requête réseau exécutés |
| F14 logs | Identifiant Checkout synthétique non masqué dans le texte | Aucun vrai log consulté |

Analyse AST : **979 fichiers Python analysés, zéro erreur syntaxique**. Cela ne prouve ni la validité des imports, ni la compatibilité des dépendances, ni le démarrage ou l'exactitude métier. Le script d'audit est volontairement un reproducteur des défauts actuels ; après correction, ses assertions doivent être remplacées par des tests de non-régression vérifiant le refus des comportements dangereux.

### Performance : mesuré et non mesuré

Les seules mesures sont la structure du code et le comptage local F11. **Latence médiane, p95, p99, débit, taux d'erreur sous charge, mémoire en service et durée SQL : non mesurés.** Aucun résultat de campagne authentifié et expurgé n'a été fourni. Les logs et artefacts de campagne potentiellement sensibles n'ont pas été ouverts.

Le pool SQL est configurable, par défaut 5 connexions et 5 d'overflow par processus (`app/infrastructure/persistence/db.py:36`). Ce n'est pas une mauvaise valeur en soi. À W workers, le budget théorique de ce pool seul est W × 10 connexions ; y ajouter les autres processus et outils. La capacité réelle de PostgreSQL est inconnue. Une transaction gardée pendant une attente fournisseur (F06/F07) augmente le temps d'occupation de ce budget.

Plan de mesure ultérieur : cible éphémère autorisée, données synthétiques reproductibles, parcours k6 existants, warmup identifié, mesures par route et version, latences DB et attente du pool. Commencer par concurrence faible et fixer les seuils selon un objectif métier validé. Mesurer F08 par une requête légère concurrente à un provider factice lent ; mesurer F11 par compteur SQL, puis EXPLAIN ANALYZE sur base de test. Aucun ajout d'index, cache, CDN ou microservice n'est justifié sans ces éléments.

### Architecture et maintenabilité

La structure en couches fournit de bons points d'extension, mais elle n'est pas suivie uniformément. `app/infrastructure/admin/admin.py` compte 15 263 lignes ; `animation_locale_api.py` 3 065 ; `localeo_live_api.py` 1 287 et contient aussi la mécanique de claims et d'envoi. La taille seule n'est pas une vulnérabilité. Le problème concret est la coexistence de traitements synchrones, présentation, autorisations et transactions dans des composants difficiles à qualifier séparément, et de deux implémentations webpush aux propriétés de reprise différentes (F07).

Priorité : extraire le service de notification et les opérations administratives touchées par les correctifs, conserver des handlers fins, expliciter les principaux types d'identité, ajouter des tests de contrat d'accès. Une conversion en microservices ou une réécriture ORM ne sont pas justifiées par la charge inconnue. README présente encore un historique de versions ancien ; `AGENT.md` et la documentation d'architecture donnent de meilleurs points d'entrée. Documenter clairement quelle configuration et quelle procédure de déploiement font autorité.

### Scénarios de panne et comportement actuel

| Scénario | Comportement observé dans le code | Incertitude / validation nécessaire |
| --- | --- | --- |
| DB indisponible | Pool avec pre-ping ; exceptions et erreurs génériques ; rollback d'UoW | Temps réel de timeout et reprise des connexions |
| Stripe réussit, commit local échoue | Rollback possible après effet distant | F06 : injection de faute et réconciliation |
| Processus arrêté après claim commerçant | EN_COURS exclus de la prochaine sélection | F07 : reprise durable à ajouter |
| Provider push lent | Appel dans UoW commerçant, timeout non explicitement choisi | Valeur effective de la dépendance ; occupation des connexions |
| Worker bloqué dans Connect | I/O sync dans route async | F08 : retard des requêtes concurrentes |
| Scheduler perd son bail | Arrêt du scheduler leader prévu dans coordinator | Tester perte de DB, double processus et retour réseau |
| Deux migrations démarrent ensemble | Lecture des migrations appliquées puis transactions par script ; aucun verrou global visible | Risque probable de course ; imposer un seul exécuteur ou verrou advisory, à tester |
| Retour arrière applicatif après migration | Checksums suivis ; état du schéma contrôlable | Pas de preuve de compatibilité ancien code/nouveau schéma ou de restauration |

`scripts/database/apply_migrations.py:101` doit rester hors des vérifications de production automatiques non autorisées : même `dry_run` crée la table de suivi si nécessaire avant de retourner les migrations attendues. Ce comportement est confirmé par lecture (`:107–116,151`), et le script n'a pas été exécuté. Utiliser une base jetable pour sa qualification.

### Couverture sécurité et exploitation

| Sujet demandé | Conclusion de cette revue | Confiance / information manquante |
| --- | --- | --- |
| Authentification, scopes et IDOR | Contrôles présents ; F01/F02/F05/F09 | Preuves locales ; matrice exhaustive des tenants à compléter |
| Sessions/cookies/JWT | Tokens opaques hachés ; SessionMiddleware pour admin ; F14 | Révocation serveur des sessions admin et SSO/MFA amont non établis ; pas de JWT central identifié |
| SQL/commandes/templates | SQLAlchemy paramétré dans les parcours lus ; aucun exploit d'injection démontré | Recherche statique ciblée, pas une preuve d'absence générale |
| XSS/HTML | Échappements présents dans PWA/admin ; HTML documentaire admin publié sur la même origine (`documents_api.py:289`) | HTML administrateur non assaini visible ; exposition à évaluer selon droits des éditeurs. Pas de XSS utilisateur non privilégié démontré |
| CSP, CSRF, CORS | Origine CSRF et en-têtes de base présents ; CORS configurable | CSP restrictive et configuration effective du proxy à vérifier |
| SSRF/redirections | F03 confirmé comme flux ; avis Starlette Windows à qualifier | Sorties réseau et OS de production non inspectés |
| Uploads | Lecture bornée, MIME/signatures, inspection et antivirus disponibles | Parsing préalable F04 ; efficacité antivirus, taille globale HTTP et limites d'images décompressées à qualifier |
| PDF actifs | Détection de motifs binaires dans `document_upload.py:42` | Une recherche de tokens ne certifie pas l'absence d'actions encodées/compressées ; pas de preuve d'exécution PDF réalisée |
| Erreurs/logs/audit | Réponses techniques génériques, masquage structuré ; F14/F15 | Rétention, accès opérateurs et intégrité du stockage externe non vérifiés |
| Secrets | Aucune valeur réelle lue ; mécanismes par environnement et scan CI présents | Aucun certificat d'absence de secrets dans l'historique ni de rotation effective |
| TLS et chiffrement au repos | Configuration HTTPS admin prévue | Certificats, TLS interne, chiffrement DB/S3/sauvegardes et politiques bucket inconnus ; le nom `endpoint_chiffre` seul ne prouve pas un chiffrement applicatif |
| Dépendances et supply chain | F01/F04/F13 ; workflow en lecture seule au niveau permissions | Graphe réellement déployé, provenance des builds et checks requis non vérifiés |
| Conteneurs et déploiement | Pas de Dockerfile/manifeste de déploiement suivi identifié dans les recherches ciblées | Image, UID, ressources, réseau, rollback et gestion des environnements inconnus |
| Sauvegardes/PRA | Documentation opérationnelle existante | Aucune preuve d'exercice de restauration, RPO/RTO ou disponibilité contractuelle fournie |
| RGPD | Données personnelles avérées dans achats, contacts, documents et audits | Pas de conclusion de conformité juridique ; registre, finalités, bases légales, durées, sous-traitants et droits à vérifier |
| Frontend/bundles/CDN | PWA embarquées lues par échantillonnage | Marketplace et métriques navigateur absentes : poids initial, Core Web Vitals et CDN non évalués |

Pour la protection des données personnelles, utiliser le [guide de sécurité de la CNIL](https://www.cnil.fr/fr/guide-de-la-securite-des-donnees-personnelles) comme support de revue avec le responsable compétent : habilitations, traçabilité, sauvegardes et contrôle des prestataires. Cet audit technique ne constitue pas une certification RGPD.

L'avis [Starlette StaticFiles/UNC sur Windows](https://github.com/Kludex/starlette/security/advisories/GHSA-wqp7-x3pw-xc5r) a également été consulté. Le poste local est Windows, mais cela ne prouve pas que le service déployé l'est. Cette applicabilité reste une hypothèse, et aucun chemin UNC n'a été ouvert ou testé.

### Commandes et traçabilité

Commandes de lecture utilisées : `git status --short`, `git rev-parse HEAD`, `git ls-files` sur workflows/verrous/manifests, `rg --files`, `rg -n` sur `app`, `tests`, `scripts` et documentation ciblée, `Get-Content` sur le code et les instructions. Aucun `Get-Content` sur un `.env` ni sur les données de `storage`/logs. Le cache pytest et certains répertoires d'installation Python n'étaient pas accessibles ; aucune modification de leurs permissions n'a été effectuée.

Commande reproductible, depuis la racine, dans un environnement Python 3.12+ :

```powershell
python -B docs/audits/2026-09-05-verifications.py
```

Dans cette session, l'interpréteur utilisé était `C:\Users\casta\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. Sa sortie a été conservée dans `2026-09-05-resultats.json`. `python` et `py` n'étaient pas disponibles dans le PATH. La suite pytest existante n'a pas été exécutée : dépendances applicatives absentes dans l'interpréteur accessible. Le lanceur `scripts/validation/test_isolated.py` a été lu ; il désactive dotenv et bloque sockets et psycopg. Son exécution devra se faire avec les dépendances qualifiées, après sélection des tests ne manipulant que des données synthétiques et sans le test qui lit `.env.example` si l'interdiction de consultation des fichiers d'environnement reste stricte.

## Questions et vérifications nécessaires pour lever les incertitudes

1. Quel commit, quelles versions installées, quel OS et quels feature flags tournent en production et préproduction ? Fournir un inventaire expurgé, sans variables secrètes.
2. Quel proxy précède Uvicorn ? Rejette-t-il un Host contenant un port suivi de caractères de chemin, remplace-t-il X-Forwarded-For et borne-t-il le corps avant parsing ? Quels réseaux peuvent joindre `/internal` et `/admin` ?
3. Quelle est la règle métier exacte d'accès d'un commerçant à une instance qui ne contient aucune de ses prestations ? Quels champs personnels sont nécessaires au scan ?
4. Les sorties réseau des workers sont-elles restreintes ? Quels services push doivent être autorisés et quelles notifications peuvent être déclenchées par une installation publique ?
5. Quelles sont les tailles réelles des achats/coffrets, la concurrence, les ressources workers/DB et les objectifs de latence/disponibilité ? Fournir uniquement des métriques agrégées.
6. Existe-t-il une réconciliation Stripe/achats et une procédure des notifications EN_COURS anciennes ? Quels tests de timeout, rejeu et panne sont déjà exécutés en environnement isolé ?
7. Où s'exécutent les tests bloquants de livraison, les migrations et les promotions ? Les checks requis, versions immuables et possibilités de rollback sont-ils documentés ?
8. Quand la dernière restauration base + fichiers a-t-elle été vérifiée, avec quel RPO/RTO ? Qui possède l'inventaire des traitements personnels, durées de conservation et droits opérateurs ?

Les validations d'intégration, de proxy et de charge restent à exécuter sur une cible isolée dont l'usage est explicitement autorisé. Les constats locaux et les correctifs proposés ci-dessus sont disponibles immédiatement pour revue.
