# Audit de Localeo Commerçants — sécurité, performance et fiabilité

> **Rapport historique sur la révision `e46322f`.** Les constats ci-dessous décrivent l’état initial, avant corrections. Consulter le [suivi des corrections et des validations](../../specifications/securisation-production/corrections-commercant-2026-09-05.md) pour l’état actuel et les limites restantes. La revue ultérieure du backend a notamment infirmé l’hypothèse d’un téléversement anonyme du constat F06 : l’ancienne route était protégée pour les administrateurs.

Date de mission : 5 septembre 2026. Référence du code : `e46322f`, arbre de travail initial propre. Audit du dépôt frontend ; aucun correctif applicatif appliqué, aucun test sur une API réelle, aucun déploiement. Les fichiers de preuve ajoutés utilisent exclusivement des données synthétiques. Les valeurs des fichiers d’environnement, secrets, journaux applicatifs et rapports historiques contenant potentiellement des données personnelles n’ont pas été consultées ni reproduites.

## A. Résumé exécutif

**Le niveau de risque du frontend audité est élevé**, principalement en raison d’un défaut reproductible d’isolation du cache entre comptes et d’une ambiguïté reproductible après validation d’une prestation. Cela ne constitue ni une preuve de compromission, ni une évaluation complète de la sécurité du système : le backend et l’infrastructure déployée ne sont pas disponibles.

Les cinq risques majeurs sont :

1. **Données du compte précédent dans le cache du compte suivant.** Une réponse tardive peut franchir le changement de compte dans le même onglet. Le défaut du cache est reproduit ; son occurrence à travers un parcours navigateur complet reste à mesurer.
2. **Déconnexion locale retardée par le réseau.** Le nettoyage local attend l’invalidation distante, sans délai maximal défini par l’application. Sur un appareil partagé, une déconnexion qui reste en attente laisse la session locale en place.
3. **Validation réalisée mais présentée comme une erreur.** Si le POST réussit puis que le rechargement échoue, le commerçant ne reçoit pas la confirmation de succès. Il peut recommencer une opération déjà réalisée. Un double effet financier dépendrait des protections du backend, non vérifiées.
4. **Compatibilité frontend/API non démontrée.** Des routes Animation et Finance appelées par le frontend sont absentes du contrat déclaré de référence. Les tests utilisent des réponses simulées et peuvent rester verts malgré une incompatibilité de déploiement.
5. **Téléversement d’images sans authentification applicative.** Le frontend et le contrat décrivent un endpoint public d’écriture. L’abus du stockage est fortement plausible si aucune protection serveur ou de passerelle ne le compense ; aucune exploitation réelle n’a été tentée.

Les conséquences possibles sont une divulgation entre utilisateurs d’un même navigateur, une perte de confiance dans les validations, des interruptions des parcours commerçants, des invitations manquées et des coûts de stockage abusifs.

**Points forts constatés :** rendu React sans sink HTML dangereux repéré dans `src/` et `public/`, Bearer explicite pour les appels protégés, contrôle d’expiration locale et validation distante de session, CSP restrictive et protections contre l’encadrement dans `render.yaml`, URL Stripe limitée à HTTPS et `connect.stripe.com`, sélection JPEG/PNG/WebP avec limite de 5 Mio côté client, clés d’idempotence sur plusieurs commandes Animation, versions attendues sur des commandes Finance, composants de récupération après erreur, cache borné à 100 entrées et 30 secondes, concurrence d’enrichissement des invitations limitée à quatre, polices locales et chargement différé de plusieurs modules.

**Actions urgentes :** isoler les requêtes et le cache par génération de session ; nettoyer la session locale immédiatement à la déconnexion ; distinguer une écriture réussie d’un rafraîchissement échoué ; vérifier la protection de l’upload et le contrat du backend effectivement déployé.

**Effort indicatif :** 2 à 4 jours-personnes pour le premier lot de corrections frontend et ses tests ; 12 à 22 jours-personnes pour l’ensemble des travaux frontend, compatibilité API, observabilité et validation sur préproduction. Une adaptation d’authentification par cookie/BFF pourrait ajouter 3 à 6 jours-personnes. Estimations non contractuelles, supposant l’accès rapide à un responsable backend ; une refonte serveur ou de l’infrastructure n’est pas incluse.

## Périmètre, méthode et informations manquantes

### Cartographie observée

```text
Navigateur / PWA React
  ├─ session en sessionStorage + état React
  ├─ API protégée : Authorization Bearer
  │    ├─ identité / profil / contact
  │    ├─ prestations / validation / annulation
  │    ├─ reversements / facturation / Chorus Pro
  │    ├─ animations / invitations / notifications
  │    └─ création du lien Stripe Connect
  ├─ API publique : catalogue, résolution QR Animation, upload DAM
  ├─ redirection HTTPS vers Stripe Connect
  └─ service worker : réception WebPush et ouverture de routes locales

Développement : Vite /api → proxy configurable
Déploiement déclaré : site statique Render → dist, repli SPA
Backend / base / stockage / prestataires : hors dépôt
```

Les versions verrouillées lues sont React 18.3.1, React Router 7.18.2, Vite 8.2.2, Vitest 4.1.11 et Playwright 1.62.1. Il s’agit d’un frontend JavaScript/JSX ; aucune implémentation serveur, SQL, migration ou infrastructure de base de données n’est présente dans le périmètre examiné. La documentation [docs/architecture.md](../../architecture/frontends/commercant/architecture.md) décrit en partie une organisation cible différente du code actuel.

Les parcours critiques sont la connexion/révocation, le scan et la validation, l’annulation, l’upload et la modération d’une page publique, les invitations Animation, les reversements et factures, les liens Stripe et les notifications. Les identifiants reçus du navigateur et ses feature flags ne constituent jamais une autorisation serveur.

**Informations nécessaires pour un audit complet :** environnement à certifier et version déployée ; backend et middleware d’autorisation ; comptes synthétiques de deux commerçants ; configuration CORS et en-têtes effectifs ; quotas/antivirus du DAM ; durée et révocation des sessions ; garanties transactionnelles et d’idempotence ; métriques anonymisées p50/p95/p99, erreurs et volumétrie ; politiques de conservation, contrats de sous-traitance et registre de traitements ; sauvegardes et preuves de restauration ; objectifs RPO/RTO/SLO ; CI et configuration Render effectives. Leur absence limite la confiance mais n’empêche pas l’audit du dépôt.

La revue a porté sur les sources applicatives, les clients HTTP, le cache, les contrats, le worker, la configuration de build/déploiement/CI et les tests. Elle combine recherche statique, exécution des tests locaux, compilation isolée, simulation de courses asynchrones et consultation des références officielles. Aucun test de charge, scan réseau, injection sur service réel, envoi de message ou upload externe n’a été effectué.

## B. Tableau des constats

Criticité = impact potentiel ; probabilité = conditions nécessaires et exposition estimée, sans fréquence statistique. P0 = traiter/vérifier sous 48 heures ; P1 = sous 30 jours ; P2 = sous 90 jours. Les efforts se recouvrent et ne doivent pas être additionnés mécaniquement. C = confirmé par preuve ; FP = fortement probable ; H = hypothèse à vérifier ; IM = information manquante.

| ID | Domaine / confiance | Constat | Preuve | Criticité | Impact | Probabilité | Correction | Effort | Priorité |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | Confidentialité / C | Une ancienne réponse peut contaminer le cache de la nouvelle session | `src/features/animations/queries.js:48`, `:75`, `:81` ; reproduction locale | Élevée | Données du compte A affichables à B dans le même onglet | Conditionnelle : changement de compte et réponses croisées | Génération de session monotone, rejet des réponses anciennes et invalidation à la déconnexion | 1–2 j | P0 |
| F02 | Session / C | Déconnexion locale après attente réseau non bornée par l’application | `src/App.jsx:489`, `:6233` ; `src/app/useMerchantSession.js:22` | Élevée | Session laissée localement active pendant l’attente | Moyenne, réseau dégradé et appareil partagé | Nettoyer immédiatement l’état et le stockage ; révoquer en parallèle avec délai maximal | 0,5–1 j | P0 |
| F03 | Fonctionnel / C | Seulement la première page des animations et invitations | `src/features/animations/queries.js:101`, `:113` ; `api.js:17`, `:27` | Moyenne | Éléments invisibles et échéances manquées | Élevée dès dépassement des limites du serveur | Conserver la pagination et permettre de charger la suite | 1–2 j | P1 |
| F04 | Intégrité / C | Succès de validation masqué par échec du GET suivant | `src/App.jsx:3865` ; reproduction locale | Élevée | Répétition d’action, support et rapprochement difficiles | Moyenne en mobilité ; double effet serveur non démontré | Distinguer écriture et rafraîchissement, réconcilier avant relance | 1–2 j | P0 |
| F05 | Disponibilité / C | Toute erreur de validation de session efface la connexion | `src/App.jsx:470`, `:6140` | Moyenne | Une panne API provoque des reconnexions inutiles | Moyenne lors d’une panne ou coupure | Distinguer session invalide, accès interdit et indisponibilité ; bloquer les actions en état indéterminé | 0,5–1 j | P1 |
| F06 | API / FP | Écriture DAM publique sans identité envoyée | `src/App.jsx:750` ; OpenAPI `/paths/~1public~1dam~1images/post` | Élevée si non compensée | Abus de stockage, hébergement de contenus indésirables | Inconnue sans passerelle/backend | Authentification ou autorisation d’upload limitée ; quotas et validation serveur | 1–3 j | P0 vérification |
| F07 | Configuration / C + H | Fichiers `.env` suivis et préfixe client large | `git ls-files '.env*'` ; `vite.config.js:65` ; `.gitignore:1` | Moyenne | Exposition possible lors de futurs ajouts de secrets | Inconnue ; aucun secret constaté | Séparer configuration publique et privée, exclure les fichiers locaux, garde CI | 0,5–1 j | P1 |
| F08 | Confidentialité / C + H | QR du coffret envoyé dans la query string | `src/App.jsx:508` | Moyenne | Copie possible du QR dans logs et outils de diagnostic | Dépend de la journalisation serveur | Corps POST et filtrage des logs, avec migration du contrat | 0,5–1,5 j | P1 |
| F09 | Finance / C | Des erreurs réseau sont converties en listes vides | `src/features/finance/FinancePages.jsx:49`, `:97` | Moyenne | Vue incomplète présentée comme complète, PDF en échec sans retour | Élevée lors d’un échec des branches concernées, si module activé | État indisponible par section et erreur de téléchargement visible | 0,5–1 j | P1 |
| F10 | Compatibilité / C + H | Contrat de référence incomplet par rapport aux appels frontend | `docs/api.md:5`, `src/features/animations/api.js:16`, `src/features/finance/api.js:3`, `api/localeo-openapi.json:1` | Élevée | Parcours susceptibles d’échouer après déploiement | Inconnue sans contrat déployé | Aligner OpenAPI, tests de contrat et ordre de déploiement | 1–3 j | P0 vérification |
| F11 | Performance / C + FP | Enrichissement pouvant ajouter deux requêtes par invitation | `src/features/animations/pages/ParticipationRequestsPage.jsx:37`, `:66` | Moyenne | Attente de la liste et trafic supplémentaires | Dépend du caractère incomplet des résumés | Compléter les résumés API ou enrichir au détail | 1–2 j | P1 mesure |
| F12 | Validation / C | Les tests navigateur ne vérifient pas les en-têtes Render ni le vrai backend | `playwright.config.js:18` ; `tests/e2e/animations.spec.js:14` ; `render.yaml:13` | Moyenne | Régression de déploiement non détectée | Moyenne | Test local du build avec CSP, puis contrats en préproduction | 1–2 j | P1 |
| F13 | Architecture / C | Authentification, API et nombreux écrans concentrés dans App | `src/App.jsx:323`, `:3500`, `:6068` | Faible | Maintenance risquée et code initial plus lourd | Certaine pour le couplage ; impact utilisateur non mesuré | Extraire progressivement API et écrans sensibles, mesurer les bundles | 2–4 j progressifs | P2 |
| F14 | Session / C + H | Bearer accessible au JavaScript dans sessionStorage | `src/app/useMerchantSession.js:25` | Moyenne, défense en profondeur | Vol de session si exécution JavaScript malveillante | Conditionnelle ; aucune XSS démontrée | Durée limitée, CSP, dépendances contrôlées ; étudier cookie HttpOnly/BFF | 0,5 j étude ; 3–6 j si migration | P2 |
| F15 | Exploitation / C + IM | Diagnostic navigateur local, supervision réelle inconnue | `src/app/AppErrorBoundary.jsx:17`, `FeatureErrorBoundary.jsx:13` | Moyenne | Incidents difficiles à relier à une requête serveur | Inconnue sans observabilité externe | Collecte expurgée, corrélation, alertes et restauration testée | 1–3 j côté front | P1 |
| F16 | Finance / C | Révocation Chorus sans traitement du rejet asynchrone | `src/features/finance/FinancePages.jsx:104` | Moyenne | Échec de révocation sans message ni état fiable | Certaine si requête rejetée et fonction activée | Catch, état occupé, erreur visible et relecture du mandat | 0,5 j | P1 |

### F01 — Isolation du cache : défaut reproduit

`activateSession()` vide les maps de cache, de requêtes et de générations. Les requêtes déjà lancées continuent. Une requête de A et une requête de B pour la même clé obtiennent alors toutes deux la génération `1`. Le callback de A vérifie seulement la génération par clé, pas l’identité de session. Si A termine après B, il remplace les données de B. La lecture suivante de B retourne A sans réseau, jusqu’à expiration ou invalidation.

Le script joint appelle le véritable corps de `query()` dans une VM avec deux promesses pilotées et des identités synthétiques. Il confirme le résultat erroné et l’absence de nouvelle requête. Il ne démontre pas une fuite entre machines ou entre sessions de navigateurs distinctes. Le parcours complet dépend de la survie d’une requête lors du changement de compte ; plusieurs appelants passent un signal, mais cela ne protège pas les appelants sans signal ni une réponse déjà résolue.

Autre comportement reproduit : deux consommateurs partagent la promesse du premier ; annuler le signal du premier rejette aussi la demande du second. Une annulation individuelle peut donc produire une erreur sur un écran encore actif.

Mesure compensatoire : imposer temporairement un rechargement complet du document lors du changement de compte. Vider seulement les maps n’est pas suffisant, car une ancienne requête peut les remplir à nouveau. `clearAnimationQueries()` est exportée mais aucun appel applicatif à cette fonction n’a été repéré hors de sa définition.

### F02 et F05 — Session et indisponibilité réseau

`handleLogoutRequest()` attend `invalidateMerchantSession()` avant `handleLogout()`. Aucun signal d’expiration n’est fourni à cette requête. Le catch protège le nettoyage après un rejet, mais pas tant que la promesse n’est pas réglée. Le bouton peut indiquer une attente ; cela ne nettoie pas le Bearer en mémoire ou dans le stockage. La durée réelle dépend aussi des délais du navigateur et du réseau, pas d’une limite applicative.

Reproduction sûre à ajouter au navigateur : simuler une invalidation qui ne termine jamais, cliquer sur Déconnexion, vérifier immédiatement l’absence de session et le retour à l’accueil. Préserver la révocation distante avec le token capturé, mais ne pas laisser son attente retarder le nettoyage local.

À l’inverse, la vérification de session efface la session pour toute exception, notamment un 500 ou une coupure, puis redirige vers l’authentification. Une panne ne prouve pas qu’une session est révoquée. Prévoir un état « vérification indisponible », sans permettre de mutation tant que l’autorisation reste indéterminée. Ne pas transformer un 403 de permission métier en expiration globale sans le contrat correspondant.

### F03 — Pagination tronquée

Le client API propose `page`, avec `page_size=20` pour les animations et `page_size=50` pour les invitations. Les fonctions `loadMerchantAnimations` et `loadParticipationRequests` appellent toujours la page 1. Les normalisateurs `contracts.js:165` et `:175` retournent seulement les items ; les métadonnées de pagination sont perdues. Les pages ne proposent pas de navigation vers les résultats suivants.

Le défaut de code est confirmé. L’existence de commerçants dépassant ces limites et le comportement exact du serveur restent inconnus. Validation proposée : API locale synthétique de 21 animations et 51 invitations, deuxième page distincte ; tous les éléments doivent être accessibles, sans charger arbitrairement toute la base. Afficher le caractère partiel de la liste est une compensation temporaire.

### F04 — Écriture réussie, lecture échouée

`handleValidatePrestation()` exécute le POST, puis le GET de prestations, dans le même try. Le message de réussite arrive seulement après le GET et l’enrichissement. La simulation fait réussir le POST, rejeter le GET et constate un message d’erreur sans message de succès. Le statut local de la prestation reste ancien ; le verrou est libéré dans le finally.

Séparer les deux résultats : « validation enregistrée » puis, au besoin, « actualisation indisponible ». Conserver la référence retournée et empêcher une relance aveugle. Si la réponse du POST lui-même est perdue, indiquer « résultat à vérifier » et relire le statut avant de décider d’une relance. La présence d’un `transaction_id` ou d’un bouton désactivé n’est pas une preuve d’idempotence serveur. Le contrat énumère un 409, mais son implémentation transactionnelle n’est pas visible.

Mesure compensatoire : procédure de vérification du statut et support avant nouvelle validation ; aucun double débit n’a été observé ou provoqué.

### F06 — Surface d’écriture publique du DAM

Le POST `/public/dam/images` envoie seulement un FormData, sans Bearer. Dans le contrat de référence, cette opération n’a pas de propriété `security` ; son corps et ses réponses prévoient notamment des erreurs 413/415. Les restrictions JPEG/PNG/WebP et 5 Mio sont effectivement présentes dans le client ; elles ne remplacent pas les contrôles serveur et peuvent être contournées par un autre client.

Il faut vérifier authentification ou capacité d’upload limitée, quotas par utilisateur et IP, limites de dimensions/décompression, contrôle de signature MIME, réencodage, stockage non exécutable et traitement des fichiers orphelins. Le contrat ne suffit pas à prouver l’absence de ces mécanismes. Aucune requête d’upload n’a été exécutée. Compensation : restriction temporaire en passerelle et quotas stricts, à valider avec le fonctionnement des autres clients publics.

### F07, F08 et F14 — Données et secrets

Le suivi Git de `.env.local`, `.env.production` et `.env.test` est confirmé par leur nom seulement. Leur contenu n’a pas été lu. `envPrefix: ['VITE_', 'LOCALEO_']` rend ces espaces de noms exposables au client ; cela ne prouve ni qu’un secret y est présent ni que toutes les variables figurent nécessairement dans chaque bundle optimisé. Conserver un exemple et une configuration explicitement publique ; mettre les données privées côté serveur. Ne pas supprimer l’historique ni faire tourner des clés sans confirmer une exposition avec une procédure autorisée qui ne restitue pas les valeurs.

Le QR coffret est placé dans l’URL d’un POST. Cette URL peut être copiée dans des logs de serveur/proxy/APM, même sous TLS. Ce constat ne signifie pas qu’elle entre dans l’historique de navigation du navigateur. Faire évoluer le contrat vers un corps JSON et filtrer les champs correspondants dans l’observabilité. Le filtrage des logs existants est une vérification serveur, pas un fait établi.

Le sessionStorage limite la persistance à l’onglet mais reste lisible par JavaScript. Aucun chemin XSS exploitable n’a été trouvé pendant cette revue ; la CSP déclarée réduit le risque. Une migration vers des cookies HttpOnly implique un changement serveur, de CORS et de protection CSRF, et ne doit pas être introduite isolément. Les tokens d’initialisation de mot de passe sont lus depuis l’URL (`src/App.jsx:6042`) : vérifier également leur durée, usage unique et filtrage dans les logs ; ces contrôles serveur ne sont pas audités.

### F09 et F16 — Dégradation silencieuse de Finance

Le tableau de bord transforme tout rejet des demandes groupées ou factures Localeo en `[]`. Cela masque aussi un 401 sur ces branches et peut afficher zéro demande au lieu d’une indisponibilité. Les erreurs de téléchargement autres que session invalide sont également avalées. La révocation Chorus attend une promesse sans catch, sans état occupé et sans message d’échec ; les error boundaries React ne prennent pas en charge ce rejet d’événement asynchrone.

Ces chemins sont confirmés par lecture, pas par appel réel. Leur exposition dépend des flags Finance/Chorus, dont les valeurs déployées n’ont pas été lues. Une indisponibilité doit rester distincte d’une liste vide ; une révocation peut avoir été traitée malgré une réponse perdue, ce qui impose de relire le mandat. Compensations : avertissement d’indisponibilité et canal de support, sans conclure à tort que le mandat est révoqué.

### F10 et F12 — Contrats et vérifications de livraison

[docs/api.md](../../specifications/espace-commercant/contrats-api.md) désigne `api/localeo-openapi.json` comme référence. Ce fichier expose 260 chemins et annonce la version `1.1.0-20260919`. `docs/openapi.json` expose 116 chemins et annonce `1.0.0-RC3`. Le libellé de version du premier contient une date postérieure à la date de mission ; il est rapporté tel quel, sans supposer une chronologie de déploiement.

Les chemins exacts `/protected/animation-locale/commercants/me/contexte`, `/protected/animation-locale/commercants/me/animations`, `/protected/animation-locale/commercants/me/demandes-participation` et `/protected/commercants/me/facturation/demandes` ne figurent pas dans le premier contrat. La comparaison des chemins confirme la divergence documentaire ; elle ne démontre pas un 404 sur le backend actuel.

Les E2E lancent Vite en développement et simulent les réponses API. Ils ne servent pas la CSP Render. Le pipeline n’apporte donc pas, à lui seul, la preuve d’intégration réelle ou de compatibilité du build avec les en-têtes. Render déclare une réécriture SPA et aucun proxy `/api` dans ce fichier ; comme le client utilise `/api` par défaut, il faut vérifier qu’une URL absolue valide est bien injectée au build déployé. La CSP `connect-src` est limitée à l’origine du site et à `https://api.localeo.city` : vérifier sa correspondance avec chaque environnement. Aucun défaut de CORS ou de CSP en production n’est affirmé ici.

Compensation : geler la promotion des modules concernés jusqu’à validation de leur contrat et réaliser un smoke test avec comptes fictifs en préproduction. Ne pas remplacer simplement les mocks par des appels production.

## Performance : mesures et impact probable

### Résultats locaux reproductibles

Machine de travail Windows, Node 24.14.0. La CI déclare Node 22 : les résultats locaux ne certifient pas cette autre version. Build Vite 8.2.2 isolé, sans lecture des `.env`, sans configuration Render et sans plugin de manifest dynamique. Il sert à vérifier la compilation et le poids du code, pas l’environnement production.

| Mesure | Résultat | Limite d’interprétation |
| --- | --- | --- |
| Compilation isolée | Réussie ; 71 modules ; 2,52 s rapportées par Vite au premier passage | Une mesure locale, aucun percentile |
| Chunk JavaScript principal | 338,23 kB ; gzip 96,44 kB | N’inclut pas les chunks partagés et toutes les ressources |
| CSS principal | 94,86 kB ; gzip 17,01 kB | Feuille globale, coût réel de rendu non mesuré |
| Chunk Animation | 29,30 kB ; gzip 7,94 kB | Chargement différé |
| Chunk Finance | 15,56 kB ; gzip 4,67 kB | Présence dans le build ne prouve pas l’activation déployée |
| Chunk Dashboard | 12,79 kB ; gzip 3,44 kB | Chargement différé |
| Polices émises | 8 WOFF2, environ 223,4 kB au total | Toutes ne sont pas nécessairement téléchargées au premier écran |
| Tests locaux avec un worker | 16 fichiers, 76 tests réussis ; 82,53 s de durée totale rapportée | Ne mesure pas la latence métier |

Les valeurs de gzip sont celles de Vite, en kB décimaux, et non une observation de la compression HTTP effectivement servie. Aucun p50/p95/p99, débit, taux d’erreur de production, pic mémoire, CPU ou temps SQL ne peut être fourni à partir de ces résultats.

### F11 — Amplification réseau démontrable

Pour N invitations avec résumé insuffisant, l’enrichissement appelle le détail de chaque demande puis, si nécessaire, le détail de son animation : **jusqu’à 1 + 2N lectures logiques**, avant retries et sans cache utile. À N=50 avec animations distinctes et informations toujours manquantes, cela représente jusqu’à 101 lectures. La limite de quatre workers réduit la concurrence mais le rendu final attend `Promise.all` ; un détail lent retarde la liste. C’est un maximum structurel, pas un trafic mesuré chez un commerçant. Les retries de lecture peuvent augmenter le nombre de tentatives.

Le scan de coffret ajoute aussi un appel par commerçant distinct absent du cache local des noms (`src/App.jsx:3699`). Les détails du coffret sont demandés après les deux lectures instance/prestations (`:3734`). Plusieurs requêtes sont correctement parallélisées ; les optimisations doivent cibler l’enrichissement obligatoire, pas éliminer ces protections ou lancer un chargement massif.

Avant changement, mesurer en préproduction les appels par ouverture, la proportion de résumés incomplets et la latence du dernier détail. Fixer un objectif de nombre d’appels, compléter la réponse de liste ou différer les détails, puis comparer les mêmes données synthétiques avec cache froid et chaud.

### F13 — Couplage et ressources initiales

`src/App.jsx` compte 6 390 lignes et `src/styles.css` 4 856. Le premier regroupe clients HTTP, authentification, scan, formulaires et routage, malgré plusieurs extractions récentes et imports lazy. Des fonctions `legacy*` subsistent. Cette organisation augmente le périmètre à relire pour modifier un flux sensible ; les fonctions inutilisées peuvent être éliminées par le build, donc leur présence source ne prouve pas à elle seule un surcoût de bundle.

Le chunk principal et la CSS fournissent une base mesurée pour suivre une extraction progressive. Leur taille ne suffit pas à déclarer l’application lente. Prioriser l’extraction du client HTTP, de la validation et de l’authentification pour appliquer uniformément timeout, erreurs et tests ; vérifier ensuite le coût sur un appareil mobile représentatif. Les images disposent de limites de taille côté sélection ; le redimensionnement, les variantes et le CDN du DAM restent inconnus.

## Fiabilité, exploitation et couverture

| Scénario | Réaction actuelle observée dans le code | Limite / validation nécessaire |
| --- | --- | --- |
| Réponse tardive du compte précédent | Peut alimenter le cache courant | F01 reproduit au niveau du cache |
| API d’invalidation qui ne termine pas | Nettoyage local attend | F02 ; test navigateur synthétique recommandé |
| API de vérification de session en 500 | Session effacée et retour connexion | F05 confirmé par chemin de code |
| POST validation réussi, GET en échec | Erreur affichée, succès absent | F04 reproduit |
| Branche Finance indisponible | Certaines listes deviennent vides | F09 confirmé par chemin de code |
| Révocation Chorus rejetée | Rejet asynchrone sans traitement local | F16, si feature activée |
| Échec de rendu React | Écran de secours avec retour/réessai | Protection constatée ; ne couvre pas les événements asynchrones |
| Navigation quittée pendant lecture | Plusieurs pages annulent via AbortController | Finance `useLoad` ne transmet pas le signal au loader (`FinancePages.jsx:20`) ; risque de réponses obsolètes à tester |
| Réseau totalement hors ligne | Pas de cache de navigation dans `public/sw.js` | Push uniquement ; aucune promesse d’usage métier hors ligne vérifiée |
| Panne Stripe ou push | Erreurs de certaines fonctions gérées côté UI | Disponibilité du tiers et reprise après effet distant non testées |

Le worker ne met pas en cache de réponses API ; aucune persistance automatique hors ligne de données métier n’a été trouvée à cet endroit. Ses notifications utilisent le titre et le corps reçus : l’absence de données personnelles dans les push dépend du producteur backend et ne peut être certifiée par le texte canonique de secours. La navigation au clic est ramenée à l’origine de l’application ; la résolution des deeplinks passe par le backend après authentification.

**F15 :** les error boundaries écrivent un diagnostic expurgé dans `console.error`, ce qui évite d’y envoyer directement la session. La référence d’incident de l’écran global est produite localement. Aucune collecte distante correspondant à cette référence n’a été repérée dans le code examiné. Une instrumentation externe peut exister : il faut la vérifier. `createApiError` collecte un identifiant de corrélation mais peut aussi reprendre un message/detail serveur (`src/lib/api/http.js:85`) ; l’exposition effective d’une stack, de SQL ou de données personnelles dans ces erreurs reste une hypothèse, sans preuve de réponse réelle.

La configuration Lighthouse ne teste que `/`, avec trois runs, et prévoit un upload vers `temporary-public-storage` (`lighthouserc.json:25`). Ce script n’a pas été lancé pendant l’audit afin de ne pas publier d’artefact. Cette destination doit rester réservée à des parcours sans données sensibles ; aucune fuite existante n’est affirmée. Les actions CI sont référencées par tags `@v4`, et le workflow ne fixe pas explicitement les permissions du token : vérifier les restrictions effectives du dépôt et envisager permissions minimales et versions immuables. Aucune compromission de chaîne logicielle n’est démontrée.

### Domaines examinés sans conclusion négative démontrée

| Domaine | Conclusion permise par les preuves |
| --- | --- |
| XSS / injection de templates | Aucun sink `dangerouslySetInnerHTML`, `innerHTML`, `document.write`, `eval` ou `new Function` trouvé dans les sources applicatives inspectées ; absence de preuve n’est pas garantie exhaustive |
| CSRF / cookies | Les appels protégés utilisent explicitement Bearer ; aucun défaut CSRF n’est établi. Cookies/session serveur hors périmètre |
| IDOR / rôles / scopes | Identifiants commerçant, achat, prestation, fil et facture manipulés côté client ; contrôle d’appartenance et scopes à tester côté serveur avec deux comptes synthétiques |
| SQL / NoSQL / commandes / SSRF | Pas d’implémentation serveur correspondante dans ce dépôt ; ne pas qualifier des appels navigateur de SSRF serveur |
| Téléversements | Validation client constatée ; contrôle de contenu, antivirus et autorisation serveur inconnus |
| TLS / chiffrement au repos | URLs et CSP configurées ; certificats, terminaison TLS et chiffrement stockage non audités. `secure:false` concerne le proxy de développement Vite, pas une preuve de TLS production désactivé |
| CORS / en-têtes | Configuration Render examinée ; réponses réellement servies non interrogées |
| Dépendances | Lockfile présent ; audit npm tenté mais registre inaccessible. Aucun résultat de vulnérabilité ni déclaration « zéro CVE » disponible |
| Rate limiting / prévention des abus | Contrôle serveur/passerelle non accessible ; aucun test de bruteforce effectué |
| Transactions / concurrence serveur | Idempotency-Key et expectedVersion présents sur certains flux ; unicité et atomicité du backend non vérifiables |
| SQL lent / index / pools / files | Base, requêtes et métriques absentes ; aucune recommandation d’index inventée |
| Backups / restauration / rollback / conteneurs | Site statique déclaré, pas de preuves opérationnelles de restauration ou de rollback ni de conteneur audité |
| RGPD | Coordonnées commerçants, contact, facturation et abonnements push identifiés par les schémas/champs ; aucune donnée personnelle réelle consultée. Base légale, conservation, droits, sous-traitants et transferts non vérifiés |

Il n’est donc pas possible de délivrer un avis de conformité RGPD ou OWASP complet. Les recommandations de traçabilité, de conservation et de restauration doivent être validées avec les responsables du traitement et de l’exploitation.

## C. Plan d’action priorisé

### Immédiat — sous 48 heures

1. Traiter F01 : génération de session, rejet des résultats périmés, nettoyage et test A/B avec réponses inversées. Compensation immédiate possible : rechargement complet lors du changement de compte.
2. Traiter F02 : déconnexion locale immédiate, révocation distante bornée, scénario hors ligne.
3. Traiter F04 : séparer succès métier et rechargement, préserver la référence de validation, procédure de réconciliation.
4. Vérifier F06 avec le propriétaire du DAM : authentification, quotas et limites effectives. Si aucune protection, restreindre l’endpoint avant de l’exposer davantage.
5. Lever F10 : obtenir l’OpenAPI déployé, comparer les routes critiques et vérifier les flags actifs avant promotion.

### Court terme — sous 30 jours

Corriger la pagination F03, les états indisponibles F05/F09 et la révocation F16. Introduire un client HTTP commun avec délai maximal, annulation et erreurs typées ; ne pas relancer automatiquement les écritures sans garantie d’idempotence. Encadrer les variables publiques F07, migrer le QR hors URL F08, ajouter tests de contrat et smoke tests du build/CSP F12. Mettre en place diagnostics expurgés et corrélation F15. Exécuter l’audit des dépendances depuis un environnement autorisé ayant accès au registre, puis qualifier séparément dépendances livrées et outillage.

### Moyen terme — sous 90 jours

Mesurer les lectures d’enrichissement F11, corriger seulement les goulots établis, extraire progressivement les parcours de `App.jsx` F13. Évaluer l’évolution des sessions F14 avec le backend. Effectuer un exercice de restauration et rollback avec objectifs RPO/RTO explicites, des tests d’autorisation inter-commerçants et de rejeu en préproduction, ainsi qu’une revue de conservation des données et notifications.

### Amélioration continue

Suivre latence p50/p95/p99 des parcours, taux d’erreur, volumes et coût du DAM ; fixer des SLO métiers. Ajouter budgets de ressources initiales et tests contractuels à chaque changement d’API. Définir propriétaires et échéances des risques ; vérifier la correction par preuves et réexaminer les exceptions. Maintenir l’inventaire des dépendances, les sauvegardes testées et des alertes exploitables.

**Corrections rapides à fort bénéfice :** nettoyage local immédiat (F02), différenciation indisponible/vide (F09), catch et retour visible Chorus (F16), exclusion des environnements privés et convention des variables publiques (F07). L’isolation du cache F01 reste prioritaire même si elle exige davantage de tests de concurrence.

## D. Correctifs proposés — exemples non appliqués

Les exemples ci-dessous illustrent le changement ; ils ne sont pas des patchs validés du produit. Les corrections ne seront appliquées qu’après validation, conformément au périmètre d’audit demandé.

### D1. Cache : génération de session et de ressource

```js
let sessionEpoch = 0;

function activateSession(token) {
  if (activeSessionToken !== token) {
    sessionEpoch += 1;
    activeSessionToken = token;
    cache.clear();
    pending.clear();
    generations.clear();
  }
}

// Dans query(), après activateSession() :
const requestEpoch = sessionEpoch;
// Puis, après la lecture et sa normalisation :
if (requestEpoch !== sessionEpoch) {
  throw new DOMException('Session remplacée', 'AbortError');
}
if (generations.get(key) === generation) {
  cache.set(key, { value, updatedAt: Date.now() });
}
```

Faire aussi incrémenter l’epoch au logout, et invalider la génération de la ressource lors d’une mutation : supprimer seulement le cache ne neutralise pas une lecture déjà en cours. Les consommateurs doivent ignorer un AbortError après démontage. L’annulation d’un consommateur ne doit pas annuler la lecture partagée des autres : signal par abonné ou gestion explicite du nombre d’abonnés.

Effet secondaire : requêtes obsolètes écartées, donc parfois une lecture supplémentaire. Validation : inverser A/B puis B/A, logout pendant lecture, mutation pendant lecture, deux abonnés dont un seul est annulé, expiration TTL et plafond du cache. Le script de preuve actuel attend volontairement le bug : créer de vrais tests de non-régression qui attendent son absence après correction.

### D2. Nettoyage local immédiat, révocation indépendante

```js
async function handleLogoutRequest(session) {
  window.sessionStorage.removeItem('localeo-merchant-session');
  clearAnimationQueries(); // version corrigée : incrémente aussi l'epoch
  handleLogout('');
  try {
    await invalidateMerchantSession(session.session_id, session.session_token, {
      signal: AbortSignal.timeout(8000),
    });
  } catch {
    // Signaler de façon expurgée que la révocation distante est non confirmée.
  }
}
```

Adapter `invalidateMerchantSession` pour transmettre le signal ; protéger les champs absents et les exceptions de stockage ; prévoir un fallback d’AbortController selon les navigateurs supportés. Le délai de huit secondes est un exemple de politique à calibrer, pas une mesure. Une interruption réseau ne garantit pas la révocation serveur : conserver une expiration serveur courte et un mécanisme de révocation approprié.

Validation : réseau suspendu, 204, 401, 500, stockage indisponible, double clic. La vue privée et le stockage doivent disparaître immédiatement ; aucune donnée de session ne doit être envoyée au diagnostic.

### D3. Séparer validation et actualisation

```js
const result = await validatePackPrestation(command);
rememberConfirmedValidation(result); // état local et référence, sans QR persistant
showSuccess('Validation enregistrée.');
try {
  await refreshPrestations();
} catch {
  showWarning('Validation enregistrée ; actualisation indisponible.');
}
```

Si le POST échoue sans réponse certaine, ne pas prétendre qu’aucune modification n’a eu lieu. Interroger le résultat via transaction/référence ; convenir avec le backend d’une clé d’idempotence stable par intention et d’une contrainte atomique. Effet secondaire : nouvel état « résultat à vérifier » et logique de reprise. Tests : POST 200 + GET 500, réponse POST perdue après commit, rejeu, double clic et conflit réel distinct d’un replay.

### D4. Pagination et états de service explicites

```js
// Forme indicative ; utiliser les vrais champs du contrat aligné.
return {
  items: payload.items.map(normalizeItem),
  page: payload.page,
  total: payload.total,
  hasMore: payload.has_more,
};
```

Inclure page et filtres dans la clé de cache ; afficher un bouton page suivante/charger plus et un compteur partiel. Ne pas déduire un total certain de la longueur de la première page. Pour Finance, traiter les promesses en états séparés (`fulfilled` / `rejected`) et propager les erreurs d’authentification. Tests : zéro résultat, seuil exact, une page supplémentaire, erreur en page 2, changement de filtre, branche secondaire 401/500. Effet secondaire : plus d’états UI mais information fidèle et charge maîtrisée.

### D5. Upload et configuration publique

```js
// Exemple de contrat cible à convenir avec le backend, route non existante présumée.
await fetch(buildProtectedApiUrl('/dam/images'), {
  method: 'POST',
  headers: buildAuthHeaders(sessionToken),
  body: formData,
});
```

Le serveur doit effectivement exiger l’identité, vérifier les permissions et appliquer les quotas ; déplacer seulement l’URL côté client ne sécurise rien. Si le DAM doit rester public pour d’autres usages, choisir une capacité d’upload courte, limitée en taille et en nombre d’objets. Ne pas placer de clé API privée dans une variable `LOCALEO_` pour contourner ce besoin.

Effets secondaires : compatibilité des autres clients et migration du contrat. Validation sur stockage isolé : anonyme refusé, compte autorisé accepté, dépassement de quota/volume rejeté, signature MIME incohérente rejetée, ancien client traité selon la migration. Aucun de ces uploads n’a été effectué pendant cet audit.

## E. Niveau de confiance et registre des vérifications

**Confiance élevée** dans les chemins de code cités et les résultats des simulations F01/F04. **Confiance moyenne** dans la probabilité d’occurrence métier, faute de métriques et de parcours réels. **Aucune certification** de l’API, de l’infrastructure ou de conformité. Les étiquettes C + H distinguent un fait confirmé de sa conséquence encore hypothétique ; une criticité élevée ne transforme pas une hypothèse en incident.

| Vérification | Commande / méthode | Résultat |
| --- | --- | --- |
| État initial | `git status --short`, `git rev-parse --short HEAD` | Propre ; `e46322f` |
| Inventaire / revue | `rg --files`, recherches ciblées et lectures de code/configuration | Sources référencées dans les constats ; aucun AGENTS.md repéré dans le dépôt |
| Fichiers d’environnement | `git ls-files '.env*'` | Noms seulement ; aucun contenu consulté |
| Contrats | `JSON.parse` des deux OpenAPI, comparaison des clés `paths`, inspection des `security`/paramètres | Divergence F10 et endpoint DAM public documenté |
| Détection de sinks | Recherche des sinks HTML/exécution dans `src/` et `public/` | Aucun résultat pour les motifs mentionnés, hors tests |
| Première tentative de tests | `npm test -- --reporter=dot` | Lanceur PowerShell bloqué par politique locale ; utilisation de `npm.cmd` ensuite |
| Tests en concurrence par défaut | `npm.cmd test -- --reporter=dot` | 74 tests exécutés réussis, mais sortie 1 : timeout de démarrage d’un worker ; résultat global non valide |
| Relance adaptée | `npm.cmd test -- --reporter=dot --maxWorkers=1` | **16 fichiers, 76 tests réussis, sortie 0**, 82,53 s |
| Course cache et validation | `node docs/audits/reproduce-audit-2026-09-05.mjs` | Trois assertions de comportement reproduites, sortie 0 ; aucun réseau |
| Build isolé | API Vite `build`, configFile false, envDir false, React, SHA fictif ; script reproductible joint | Réussite ; tailles indiquées plus haut |
| Dépendances | `npm.cmd audit --package-lock-only --ignore-scripts --json` | Échec d’accès à l’endpoint d’advisories npm ; pas de conclusion CVE |
| E2E / Lighthouse | Configuration et tests lus, pas exécutés pendant cet audit | Évite appels non simulés via proxy et publication automatique Lighthouse ; couverture runtime manquante explicitement conservée |
| API / production | Aucun appel métier | IDOR, charges, quotas et contrôles serveur non testés |

Le script de reproduction extrait les corps du code audité et remplace les entrées réseau par des promesses synthétiques. Il prouve des défauts de logique locale ; il ne remplace pas un test intégré React/navigateur. Le script de build reproductible désactive en plus tous les préfixes d’environnement client et n’altère pas `dist/` ; ses fichiers sont écrits sous `tmp/audit-2026-09-05-dist`.

### Références externes utilisées

- Les variables injectées dans un frontend doivent être considérées publiques ; les modes et règles d’exposition sont décrits dans la [documentation officielle Vite](https://vite.dev/guide/env-and-mode.html).
- Le stockage de session accessible au JavaScript exige de considérer le scénario XSS et le cycle de vie de la session : [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) et [OWASP HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html).
- Les vérifications complémentaires de sécurité des traitements s’appuient sur le [guide CNIL](https://www.cnil.fr/fr/guide-de-la-securite-des-donnees-personnelles), notamment [traçabilité](https://www.cnil.fr/fr/securite-tracer-les-operations) et [sauvegardes](https://www.cnil.fr/fr/securite-sauvegarder). Ce sont des axes de vérification, pas un avis juridique de conformité.

### Questions et vérifications finales pour lever les incertitudes

1. Quelle version frontend/backend et quel environnement faut-il certifier ? Quel OpenAPI correspond à cette version, et quels flags Animation/Finance/Chorus sont actifs ?
2. Le DAM public impose-t-il une capacité, un quota et des contrôles de contenu côté serveur/passerelle ?
3. Quelles garanties atomiques empêchent une seconde validation et permettent de retrouver le résultat après perte de réponse ?
4. Quelle durée maximale et quel mécanisme de révocation des sessions sont effectifs ? Des postes sont-ils partagés entre commerçants ?
5. Peut-on disposer de comptes fictifs inter-commerçants et d’un stockage isolé en préproduction pour les tests d’autorisation et de reprise ?
6. Quels volumes dépassent 20 animations ou 50 invitations ; quels sont les percentiles de latence et taux d’échec actuels ?
7. Quels en-têtes, CORS, logs expurgés, alertes, sauvegardes, RPO/RTO et preuves de restauration sont réellement en place ?
8. Qui porte la conservation des données, les demandes d’exercice de droits et la revue des sous-traitants, notamment DAM, push et facturation ?
