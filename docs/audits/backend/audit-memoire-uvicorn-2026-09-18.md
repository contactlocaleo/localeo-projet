# Audit mémoire du backend Localeo — 18 septembre 2026

## Conclusion

Le socle applicatif explique déjà une part importante des quelque 300 Mo signalés : le chargement du backend complet atteint environ **209 Mio** sur le poste Windows, avant toute requête et sans connexion à PostgreSQL. Uvicorn importé seul, avec l'interpréteur et le petit harnais de mesure, occupe environ **28 Mio**. Le coût principal est celui de l'application chargée dans son processus.

Ces résultats ne constituent pas une mesure du processus Linux de Render. Les 300 Mo distants restent à décomposer sur place : versions exactes, RSS du PID ou métrique du service, nombre de workers, scheduler, documentation consultée et traitements déjà exécutés. Une empreinte stable de cette taille ne démontre pas une fuite mémoire.

## Méthode et limites

- Code du répertoire de travail `localeo-backend`, y compris les modifications locales existantes ; aucune modification du code applicatif pour cet audit.
- CPython 3.12.14, Windows 64 bits, environnement Python `tmp/audit-venv` du backend.
- Uvicorn 0.52.4, FastAPI 0.136.0, Starlette 1.3.1, SQLAlchemy 2.0.52, Pydantic 2.13.5, Stripe 10.12.0, SQLAdmin 0.29.0, Pillow 12.3.0, ReportLab 4.5.1.
- Processus Python distinct pour chaque scénario. Mesure par `GetProcessMemoryInfo` : working set résident et mémoire privée engagée, en Mio (1 048 576 octets). Le working set Windows n'est pas strictement comparable au RSS Linux ; la mémoire privée n'est pas une seconde quantité à lui ajouter.
- Fichiers dotenv neutralisés, configuration de test factice, hooks d'audit interdisant les connexions réseau sortantes et la résolution DNS. Bootstrap, vérification de schéma et scheduler désactivés. Aucune donnée de démo ou de production utilisée.
- `gc.collect()` effectué après les imports. Les principaux chiffres ci-dessous sont mesurés sans tracemalloc, dont le surcoût fausserait la comparaison avec les 300 Mo.
- Les scénarios expérimentaux neutralisent des composants uniquement dans leur processus de mesure ; ils ne constituent pas une implémentation livrée ni une validation fonctionnelle des optimisations.

## Mesures de démarrage

| Étape dans un même processus | Working set, Mio | Mémoire privée, Mio |
| --- | ---: | ---: |
| Interpréteur + petit harnais de mesure | 17,65 | 11,34 |
| Après import d'Uvicorn | 27,80 | 18,68 |
| Après les imports d'API précédant l'import du back-office | 172,68 | 155,62 |
| Après les autres imports et l'instrumentation | 179,77 | 163,01 |
| Avant `setup_admin` | 185,59 | 168,62 |
| Après `setup_admin` | 198,02 | 180,28 |
| Application complètement importée, après GC | **208,54** | **191,25** |

Les points intermédiaires ont été injectés en mémoire dans le module de démarrage, sans modifier le fichier source. Des exécutions indépendantes sans cette instrumentation retrouvent environ 208,5 Mio. Les durées de démarrage ne sont pas un benchmark : plusieurs processus de mesure ont tourné simultanément.

L'application expose 590 objets de route au niveau principal, montages inclus, et charge 2 084 modules Python. Ce n'est pas le nombre exact d'opérations HTTP distinctes. La métadonnée SQLAlchemy contient 137 tables, sans que cela implique de charger leurs lignes. Dans le scénario contrôlé, le pool ne contient aucune connexion ouverte.

### Expériences ciblées

| Expérience, processus distinct | Working set après GC | Interprétation |
| --- | ---: | --- |
| Application complète de référence | 208,5 Mio | Socle au démarrage |
| Initialisation SQLAdmin neutralisée, imports conservés | 194,9 Mio | Environ 13,6 Mio évités ; ne mesure pas une séparation complète de l'ERP |
| Instrumentation automatique des use cases neutralisée | 207,9 Mio | Gain inférieur à 1 Mio dans ce protocole ; faible priorité |
| Import Stripe différé expérimentalement | 164,7 Mio | Environ 44 Mio évités avant la première utilisation de Stripe |
| Même processus, puis chargement effectif de Stripe sans appel API | 207,5 Mio | Le coût revient au premier usage : report du coût, pas suppression |
| Application complète après génération OpenAPI globale | 227,8 Mio | Environ 19 Mio supplémentaires dans ce processus |
| Après génération des trois variantes OpenAPI et GC | 226,3 Mio | Copies conservées, mais leur supplément n'est pas isolable par simple différence de RSS |

Après import complet, un contrôle de 30 secondes sans requête reste stable à 208,53 Mio. Ce contrôle court, sans scheduler ni base, ne permet pas d'écarter une fuite dans un parcours métier ou sur plusieurs heures.

Une seconde vérification démarre réellement Uvicorn sur un port local attribué automatiquement, avec le lifespan applicatif, sans requêtes entrantes : **209,55 Mio** de working set et **192,11 Mio** de mémoire privée. La mesure reste identique après 10, 20 et 30 secondes. La protection réseau du harnais autorise uniquement, en plus du serveur local, la paire de sockets de réveil interne de la boucle asyncio Windows ; les connexions à la base et aux services externes restent interdites.

Les imports isolés à partir du même socle Uvicorn donnent : FastAPI +15 Mio ; Stripe et ses dépendances +58 Mio ; SQLAlchemy seul +18,5 Mio ; unité de travail SQLAlchemy de Localeo et ses dépendances +45,7 Mio ; rendu des reçus PDF et ses dépendances +8,5 Mio. **Ces chiffres se recoupent et ne doivent pas être additionnés.**

### Allocations Python retenues

Une exécution distincte avec `tracemalloc`, profondeur de pile 1, retrouve environ **156 Mio d'allocations suivies** après import et GC. Principaux sites d'allocation : importlib (40,5 Mio dans `_bootstrap_external`), `typing_extensions` (20,1 Mio), champs Pydantic (7,4 Mio), `typing` (6,5 Mio), routes FastAPI (4,4 Mio), puis plusieurs postes SQLAlchemy. Cela corrobore le poids des modules, types, schémas et objets de routage. Le fichier ayant alloué un objet n'identifie pas nécessairement le composant métier qui le conserve.

Le traceur utilise lui-même environ **80 Mio** pour stocker les traces, et le processus instrumenté atteint 359 Mio : ce dernier chiffre est volontairement exclu du diagnostic de l'empreinte normale. Les allocations suivies ne sont ni le RSS complet ni une décomposition exhaustive de la mémoire native.

## Causes constatées dans le code

1. **Chargement simultané de toutes les surfaces.** `app/main.py` importe les API publiques, commerçantes, animations, exploitation et ERP, puis appelle `setup_admin` sans condition. Les schémas Pydantic, dépendances FastAPI, modèles ORM et vues SQLAdmin restent accessibles pendant la vie du processus. Une API sans visiteurs conserve ce socle.
2. **SDK Stripe chargé immédiatement.** `app/infrastructure/paiement/paiement_gateway.py:2` et `stripe_connect_gateway.py:6` importent Stripe au niveau du module et configurent ses attributs globaux. Le test de chargement différé mesure un potentiel d'environ 44 Mio au démarrage de l'application actuelle.
3. **Schéma OpenAPI construit et conservé au premier accès.** `app/main.py:604` conserve le schéma global ; `:565` effectue un `deepcopy` pour chacune des trois surfaces, gardées dans `SURFACE_OPENAPI_CACHE`. Ce coût n'existe pas avant le premier usage de la documentation. Les copies contiennent encore les composants du schéma global.
4. **Import systématique des use cases pour les logs.** `app/observability_instrumentation.py:301` parcourt et importe les modules applicatifs. Le gain mesuré en le neutralisant est faible aujourd'hui : ces modules sont déjà largement importés par les API. Ce mécanisme devrait néanmoins être revu si l'on introduit des chargements différés, pour éviter de les annuler.
5. **Activité possible en l'absence de visiteurs.** Si activé, `app/main.py:156` démarre le scheduler. `app/infrastructure/scheduler/coordinator.py` lance sa coordination et les batchs, dont les requêtes passent par `http_client.py`. L'absence de trafic public ne signifie donc pas l'absence de traitements internes.

## Améliorations proposées, par priorité

### 1. Établir la mesure Linux du service déployé

Relever, au redémarrage puis après quelques minutes, le nombre de PID Python, leur RSS/PSS et la mémoire du service Render. Vérifier la commande effective et `WEB_CONCURRENCY` : plusieurs workers répliquent le socle applicatif. `--reload` est réservé au développement. Ne pas modifier le nombre de workers sans vérifier les besoins de débit et de disponibilité.

Comparer successivement : démarrage ; passage des healthchecks ; ouverture de la documentation ; premier paiement ; traitement de documents/flyers ; exécution des batchs. Utiliser des parcours de test autorisés, sans provoquer un paiement réel pour mesurer la mémoire.

Exemples en shell Render/Linux, avec le PID applicatif identifié au préalable :

```sh
ps -eo pid,ppid,rss,nlwp,args
cat /proc/<PID>/smaps_rollup
cat /proc/<PID>/status
```

Le RSS de `ps` est généralement en Kio. Lire séparément la métrique Render, qui est présentée au niveau du service/de ses instances. Vérifier également l'unité Mo/Mio : cela explique quelques pourcents, pas à lui seul l'écart observé.

### 2. Charger Stripe à la demande

Centraliser l'obtention/configuration du client dans un provider chargé au premier appel Stripe, en évitant de conserver les imports immédiats dans l'autre gateway. Potentiel mesuré au démarrage : environ 44 Mio par processus. Ce gain disparaît pour un worker qui utilise ensuite Stripe. Prévoir la latence du premier appel et les tests de paiement, webhook et Connect ; ne pas confondre l'expérience de mesure avec une correction prête à publier.

### 3. Réduire le coût de la documentation

Envisager de générer les documents OpenAPI au build pour les servir comme fichiers, si cela respecte les règles d'accès et la configuration des schémas. Sinon, éviter les copies profondes de composants inchangés et construire des variantes réellement filtrées. Vérifier qu'aucune mutation n'altère le schéma partagé. Gain exact de cette refonte à mesurer ; la simple suppression des copies ne garantit pas de récupérer les 19 Mio observés.

### 4. Découpler progressivement les surfaces API et ERP

Une fabrique d'application avec imports conditionnels peut limiter ce que charge chaque type de worker. Désactiver seulement `setup_admin` économise environ 14 Mio dans l'expérience, car les bibliothèques partagées restent chargées. Séparer en deux services peut augmenter la consommation totale en dupliquant les dépendances : à justifier par le dimensionnement et l'isolation, pas seulement par la taille d'un PID.

### 5. Surveiller les pics documentaires et images

La lecture DAM (`app/api/images_api.py:178`) charge le binaire avant de vérifier la condition ETag ; une requête retournant 304 charge donc encore le contenu depuis PostgreSQL. Une lecture initiale des seules métadonnées, puis du binaire si nécessaire, réduirait ce travail. Conserver la validation des contenus lors de l'import et les règles applicables aux assets historiques. Ce point concerne l'activité, pas le socle à froid ; la validation actuelle du GET inspecte la signature et ne décode pas toute l'image avec Pillow.

Le renderer de flyers dispose déjà d'un sémaphore par processus et d'un cache de polices borné à 64 entrées ; le rendu des reçus a un cache de fontes borné à 1. Ne pas présenter ces caches comme une fuite avérée. L'audit flyers du 29 août documente déjà une réduction du pic mémoire : préserver ces protections. Les uploads d'images peuvent néanmoins décoder jusqu'à 16 millions de pixels ; surveiller les traitements simultanés et les dimensions réelles, pas seulement les octets du fichier compressé.

## Actions à éviter sans preuve

- Forcer périodiquement le garbage collector : il ne peut pas libérer les classes, routes, modules et caches encore référencés. Le GC manuel n'a pas réduit le socle mesuré.
- Réduire le pool SQLAlchemy comme premier remède au coût à froid : les connexions sont créées à la demande et le socle mesuré existe avec zéro connexion ouverte.
- Accuser les dépendances simplement installées : un paquet inutilisé sur disque ne consomme pas sa taille d'installation en mémoire du processus.
- Conclure à une fuite à partir d'une mesure unique, ou promettre une empreinte cible Linux à partir du seul poste Windows.

## Références

- [FastAPI — mémoire par processus](https://fastapi.tiangolo.com/deployment/concepts/#memory-per-process).
- [Python — tracemalloc et son propre surcoût](https://docs.python.org/3/library/tracemalloc.html).
- [Render — métriques des services et des instances](https://render.com/docs/service-metrics).
- Audit local antérieur : [docs/audits/audit-performance-generation-flyer-2026-08-29.md](audit-performance-generation-flyer-2026-08-29.md).

Aucun correctif, déploiement, commit ou changement de configuration Render effectué pendant cet audit.
