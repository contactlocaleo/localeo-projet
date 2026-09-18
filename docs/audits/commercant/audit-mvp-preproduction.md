# Audit MVP préproduction — application commerçant Localeo

> Rapport historique du 29 août 2026. Les états de clôture actualisés, preuves backend et risques résiduels sont centralisés dans [le registre du 7 septembre](remediation-preproduction-2026-09-06.md). Les constats ci-dessous restent les preuves datées de cet audit.

Date de l'audit : 29 août 2026  
Périmètre : dépôt `localeo-commercant`, PWA React/Vite et contrat OpenAPI fourni  
Environnement communiqué : `https://test-commercant.localeo.city/`

## 1. Synthèse exécutive

### Verdict : `NO-GO`

Après corrections et réaudit, deux des trois P1 initiaux sont corrigés et validés : React Router/Vite sont à jour et le contrôle E2E d'accessibilité passe. Le verdict reste `NO-GO` car SEC-01, le téléversement DAM anonyme, exige une correction backend absente de ce dépôt. SEC-03 reste également ouvert en P2. Les configurations SEC-05, UX-03 et PERF-03 sont corrigées dans le code mais attendent respectivement un redéploiement Render et une exécution Lighthouse CI Linux pour être validées.

| Sévérité | Nombre |
|---|---:|
| P0 | 0 |
| P1 | 3 |
| P2 | 6 |
| P3 | 2 |

Niveau de confiance global : **moyen à élevé** pour le frontend et le contrat API ; **faible à moyen** pour l'infrastructure et les contrôles serveur non présents dans ce dépôt.

Principaux risques :

- usage abusif du stockage DAM et dépôt anonyme de contenu ;
- redirections ouvertes/XSS possibles via une version vulnérable du routeur ;
- navigation par lecteurs d'écran incohérente et pipeline E2E non passant ;
- vol du bearer token en cas de XSS, car il est conservé dans `sessionStorage` ;
- redirection vers une URL Stripe non validée côté client ;
- dégradation sensible au volume sur la liste d'invitations et ressources initiales surdimensionnées.

### Limites

- L'URL corrigée répond en HTTPS et ses réponses publiques ont été inspectées le 29 août 2026. Aucun navigateur interactif ni compte de test n'était toutefois disponible : les parcours rendus/authentifiés, cookies, CORS des API et comportements métier distants n'ont pas été observés.
- Le JavaScript distant (`index-7rJbdDE9.js`, 326 132 octets) ne porte pas le même hash que le build local produit pendant l'audit (`index-CO6uxr9c.js`, 325 500 octets). Les constats de code doivent donc être revalidés après déploiement du commit candidat exact.
- Aucun compte de test ni jeu de données distant n'a été fourni. Les parcours authentifiés ont été exercés via les mocks Playwright existants, sans action destructive.
- Le backend et sa base ne sont pas dans ce dépôt. Les autorisations objet/tenant, requêtes SQL, index, rate limits, journalisation, sauvegardes, webhooks et contrôles réels de fichiers ne peuvent pas être confirmés par le frontend.
- Lighthouse a échoué lors de l'arrêt/nettoyage de Chrome sous Windows (`EPERM`/`taskkill: accès refusé`). Aucun score Lighthouse n'est présenté comme mesure valide.
- `npm audit` reflète les avis connus du registre au 29 août 2026 ; il ne prouve pas l'exploitabilité de chaque dépendance transitive.

## 2. Cartographie et protocole

### Architecture observée

- React 18.3.1, React Router DOM 7.18.2 et Vite 8.2.2 après correction.
- SPA/PWA avec service worker dédié aux notifications push.
- API distante sous `/api/public` et `/api/protected`, authentification par bearer token.
- Fonctionnalités critiques : connexion/récupération de mot de passe, validation de prestation par QR, profil/page publique avec upload d'images, animations/invitations, reversements, Stripe Connect, support et Web Push.
- Découpage différé présent pour dashboard, animations et reversements, mais `src/App.jsx` reste un module de 6 295 lignes et `src/styles.css` compte 4 142 lignes.

### Vérifications réalisées

- inspection de l'architecture, du code, des configurations, contrats API, workflows CI et variables d'environnement ;
- recherche des sinks XSS, stockages de jetons, redirections, appels authentifiés, service worker et scripts tiers ;
- `npm.cmd test -- --reporter=verbose` ;
- `npm.cmd run build:prod` ;
- `npm.cmd run test:e2e` ;
- `npm.cmd audit --json` avec accès au registre npm ;
- `npm.cmd run test:lighthouse` (échec d'outillage, métriques non retenues) ;
- inventaire des artefacts de production et tailles gzip fournies par Vite.

### Réaudit après corrections

- 13 fichiers de tests unitaires, **63 tests réussis sur 63** ;
- **6 scénarios Playwright réussis sur 6**, dont axe-core sans violation critique ; le runner reste accroché après les résultats sous Windows et a été interrompu ;
- build production Vite 8.2.2 réussi en 0,81 s lors de la dernière passe ;
- dépendances de production : **0 vulnérabilité** avec `npm audit --omit=dev` ;
- audit complet : 10 avis résiduels (7 high, 1 moderate, 2 low), tous dans la chaîne de développement `@lhci/cli` 0.15.1 ; aucune version corrigée de LHCI n'est publiée, et la proposition npm de revenir à 0.1.0 n'est pas une remédiation sûre ;
- Lighthouse reconnaît les trois passes et budgets, mais Chrome échoue sous Windows avant la première mesure (`taskkill`/WebSocket) ;
- build final : JS principal 332,05 Ko brut / 94,42 Ko gzip, CSS 73,43 Ko / 13,02 Ko gzip ;
- aucun test distant post-déploiement n'a été réalisé, les commits n'étant pas encore déployés.

## 3. Tableau des constats

| ID | Axe | Sévérité | Statut / confiance | Fonctionnalité | Impact | Effort |
|---|---|---|---|---|---|---|
| SEC-01 | Sécurité | P1 | **NON CORRIGÉ — backend requis** / élevé | Upload DAM | Stockage et contenu téléversables sans identité appelante | M |
| SEC-02 | Sécurité | P1 | **CORRIGÉ · VALIDÉ** / élevé | Routage | React Router 7.18.2, audit runtime sans vulnérabilité | S à M |
| UX-01 | UX/UI | P1 | **CORRIGÉ · VALIDÉ** / élevé | Animations | `tabpanel` présent dans tous les états | XS |
| SEC-03 | Sécurité | P2 | **NON CORRIGÉ — backend requis** / élevé | Session | Bearer token exfiltrable par tout XSS exécuté sur l'origine | L |
| SEC-04 | Sécurité | P2 | **CORRIGÉ · VALIDÉ** / élevé | Stripe Connect | Navigation désormais limitée à HTTPS sur `connect.stripe.com` | S |
| PERF-01 | Performance | P2 | **CORRIGÉ · VALIDÉ** / élevé | Shell initial | Icône du shell remplacée par la variante 192 px de 44,7 Ko | S |
| PERF-02 | Performance | P2 | **CORRIGÉ · VALIDÉ** / élevé | Invitations | Enrichissements bornés à quatre et chargements partagés dédupliqués | M |
| SEC-05 | Sécurité | P2 | **CORRIGÉ** — déploiement à valider / élevé | En-têtes HTTP | Baseline versionnée dans la configuration Render | S |
| UX-03 | UX/UI | P2 | **CORRIGÉ** — déploiement à valider / élevé | Installation PWA | Type MIME du manifeste configuré dans Render | XS |
| PERF-03 | Performance | P3 | **CORRIGÉ** — à valider / élevé | Mesure CI | Trois passes et budgets Web Vitals explicites | S |
| UX-02 | UX/UI | P3 | **CORRIGÉ · VALIDÉ** / élevé | Upload images | Formats allowlistés et limite locale de 5 Mo | S |

### SEC-01 — Téléversement DAM sans authentification

**État : NON CORRIGÉ — évolution backend requise.** Ajouter un header depuis le frontend ne protégerait pas une route qui continue d'accepter les appels anonymes. La désactivation du parcours a été écartée car elle supprimerait une fonctionnalité métier sans supprimer l'endpoint exposé.

- Règle : OWASP File Upload / contrôle d'accès serveur.
- Preuve : `uploadPublicImage` envoie un `POST` vers `/public/dam/images` sans `Authorization` dans `src/App.jsx:742-750`. Le contrat `api/localeo-openapi.json:1` expose `POST /public/dam/images`, ne déclare aucune propriété `security` et documente des réponses 200/413/415.
- Reproduction non destructive : inspecter l'opération OpenAPI puis constater que `buildPublicApiUrl` construit bien `/api/public/...` dans `src/lib/api/http.js:37-39` et que le client n'ajoute aucun bearer token.
- Impact : un acteur anonyme peut tenter d'occuper le stockage, diffuser du contenu via l'origine Localeo ou augmenter les coûts. Les contrôles de type/taille backend réduisent l'impact mais ne remplacent ni authentification ni quotas.
- Correction : déplacer la création vers une route protégée, vérifier le commerçant et son droit à modifier sa page, imposer quotas par commerçant/IP, taille stricte, détection réelle du type, décodage/réencodage d'image, nom serveur aléatoire et stockage non exécutable.
- Mesure compensatoire : désactiver l'upload en production ou limiter la route au réseau/WAF et appliquer un quota global très bas jusqu'à correction.

### SEC-02 — React Router vulnérable

**États : CORRIGÉ · VALIDÉ.** Validation : React Router 7.18.2/Vite 8.2.2 résolus, build réussi, 63 tests unitaires réussis et `npm audit --omit=dev` à zéro vulnérabilité.

- Règle : dépendances et supply chain.
- Preuve : `package.json:24` demande `react-router-dom ^6.30.0`; `npm ls` résout `react-router-dom@6.30.0`, `react-router@6.30.0` et `@remix-run/router@1.23.0`, versions signalées par `npm audit`. Le rapport indique notamment GHSA-2w69-qvjg-hvjx (XSS via open redirect), GHSA-9jcx-v3wj-wh4m, GHSA-wrjc-x8rr-h8h6 et GHSA-2j2x-hqr9-3h42. Total audit : 16 vulnérabilités, dont 11 high, 2 moderate, 3 low et 0 critical. Une partie des high est limitée à l'outillage de développement Lighthouse/Vite, mais React Router est embarqué au runtime.
- Reproduction : `npm.cmd audit --json` puis `npm ls react-router react-router-dom @remix-run/router`.
- Impact : selon les chemins contrôlables transmis à `<Link>`/`navigate`, un attaquant peut provoquer une redirection externe et, pour certaines variantes, une XSS avec interaction utilisateur.
- Correction : mettre à niveau React Router vers une version corrigée compatible, relancer les tests unitaires/E2E, et valider explicitement toute destination issue d'une API ou d'une URL. Ne pas appliquer aveuglément la proposition erronée de downgrade de LHCI vers `0.1.0`.
- Mesure compensatoire : n'accepter que des chemins internes commençant par un seul `/`, rejeter `//`, antislashs et schémas, et éviter toute navigation avec entrée non fiable.
- Mise en œuvre : `react-router-dom` et `react-router` sont résolus en 7.18.2 ; `@remix-run/router` vulnérable n'est plus installé. Vite est également passé à 8.2.2 avec `@vitejs/plugin-react` 6.1.1 pour fermer ses avis directs. Ces versions exigent Node.js 20 ou supérieur. L'audit limité aux dépendances de production ne signale plus aucune vulnérabilité.

### UX-01 — Onglets ARIA invalides pendant le chargement

**États : CORRIGÉ · VALIDÉ.** Validation : test unitaire de relation ARIA réussi et scénario Playwright/axe-core réussi sans violation critique.

- Preuve : `src/features/animations/components/AnimationUi.jsx:35` ajoute `aria-controls="animation-panel-en-cours"`, tandis que le retour anticipé de chargement dans `src/features/animations/pages/AnimationsListPage.jsx:34` ne rend aucun élément portant cet ID. Axe-core signale `aria-valid-attr-value`, impact `critical`. Le test échoue à `tests/e2e/accessibility.spec.js:14`.
- Reproduction : `npm.cmd run test:a11y` ou `npm.cmd run test:e2e`.
- Impact : relation onglet/panneau invalide pour les technologies d'assistance et pipeline CI non passant (`.github/workflows/frontend-quality.yml:21`).
- Correction : rendre le `tabpanel` et son ID dans tous les états, y compris chargement/erreur, ou retirer temporairement `aria-controls` jusqu'à présence effective du panneau.
- Mesure compensatoire : aucune acceptable pour livrer avec une CI verte ; correction XS.
- Mise en œuvre : l'état de chargement rend désormais le `tabpanel` ciblé, avec `aria-labelledby` réciproque et `aria-busy`. Un test unitaire vérifie la relation avant résolution des requêtes.

### SEC-03 — Bearer token conservé dans `sessionStorage`

**État : NON CORRIGÉ — évolution backend requise.** Retirer le stockage côté client sans cookie `HttpOnly` ou mécanisme de renouvellement serveur casserait la reprise de session au rafraîchissement sans fermer correctement le risque.

- Preuve : la session complète, incluant `session_token`, est lue et écrite sous `localeo-merchant-session` dans `src/app/useMerchantSession.js:4-25`. Elle est ensuite placée dans l'en-tête `Authorization` par `src/lib/api/http.js:41-45`.
- Impact : toute XSS exécutée sur l'origine peut lire et exfiltrer le jeton jusqu'à son expiration. `sessionStorage` limite la persistance à l'onglet, pas l'accès JavaScript.
- Correction : privilégier une session serveur en cookie `HttpOnly`, `Secure`, `SameSite` avec protection CSRF, ou à défaut conserver un access token très court uniquement en mémoire avec rotation/refresh protégé.
- Mesure compensatoire : durée très courte, révocation à la déconnexion, CSP stricte, absence de scripts tiers et surveillance des sessions.

### SEC-04 — URL d'onboarding Stripe non validée avant navigation

**États : CORRIGÉ · VALIDÉ.** Validation : sept cas unitaires réussis et recherche statique confirmant que les deux redirections passent par l'allowlist.

- Preuve : `src/features/stripeConnect/StripeConnectPanel.jsx:62-64` appelle `window.location.assign(nextPayload.onboarding_url)` et `src/features/stripeConnect/StripeConnectCallbackPage.jsx:19-20` appelle `replace` avec la valeur de l'API, sans validation locale.
- Impact : une réponse backend compromise ou mal configurée peut rediriger vers un site de phishing ou un schéma actif.
- Correction : parser via `new URL`, imposer `https:` et une allowlist des hôtes Stripe attendus ; idéalement renvoyer un identifiant d'opération plutôt qu'une URL arbitraire.
- Mesure compensatoire : CSP `navigate-to` lorsque supporté et validation stricte côté serveur.
- Mise en œuvre : `src/features/stripeConnect/safeOnboardingUrl.js` centralise une allowlist stricte `https://connect.stripe.com`; les deux redirections refusent désormais toute valeur invalide. Sept tests unitaires couvrent les schémas actifs, HTTP, chemins relatifs et hôtes trompeurs.

### PERF-01 — Ressources initiales trop lourdes

**États : CORRIGÉ · VALIDÉ.** Validation : build production réussi ; le shell et le manifeste générés référencent les variantes 192/512 px, plus l'original de 555 Ko.

- Mesures initiales : JS principal 325,50 Ko brut / 92,86 Ko gzip ; CSS 74,92 Ko / 13,01 Ko gzip ; sept polices WOFF2 totalisent environ 172 Ko bruts. `public/localeo-pro-icon.png` pèse 555 114 octets et était utilisé dans le shell à `src/app/ApplicationFrame.jsx:19`. Le dossier public contient aussi `hero-v27.png` de 2 874 236 octets, copié dans `dist` mais non référencé par le code inspecté.
- Impact : LCP et affichage de l'en-tête dégradés sur réseau mobile ; empreinte de déploiement inutile.
- Correction : générer une icône d'affichage à la taille réellement rendue (WebP/AVIF ou PNG optimisé), réserver le grand original au manifeste si nécessaire, sous-ensembler les graisses de police, supprimer l'asset hero inutilisé et poursuivre le découpage de `App.jsx`.
- Mesure compensatoire : cache long immutable et compression HTTP correcte.
- Mise en œuvre : le shell, le dialogue PWA et l'icône Apple utilisent désormais `/icon-192.png` (44 651 octets) au lieu de l'original de 555 114 octets. Le manifeste déclare explicitement les variantes 192 et 512 px. Le gain sur l'icône du shell est de 510 463 octets bruts, soit 91,96 %.

### PERF-02 — Fan-out N+1 sur les invitations

**États : CORRIGÉ · VALIDÉ.** Validation : test avec dix invitations réussi, concurrence observée ≤ 4 et un seul chargement pour l'animation partagée.

- Preuve : `src/features/animations/pages/ParticipationRequestsPage.jsx:34-58` peut charger le détail de la demande puis celui de l'animation pour chaque élément incomplet. La ligne 66 lance tous les enrichissements via `Promise.all`, sans limite de concurrence.
- Impact : pour N invitations incomplètes, jusqu'à `1 + 2N` requêtes, saturation du navigateur/API, écran de chargement plus long et risque de rate limiting.
- Correction : enrichir la réponse de liste côté serveur, ou fournir un endpoint batch ; à défaut dédupliquer les animations et limiter la concurrence.
- Mesure compensatoire : pagination stricte et cache partagé par identifiant d'animation.
- Mise en œuvre : un pool de quatre workers borne les enrichissements tout en conservant l'ordre. Le cache de requêtes existant déduplique les animations communes. Le test couvre dix invitations et prouve une concurrence maximale de quatre ainsi qu'un seul chargement de l'animation partagée.

### SEC-05 — Baseline d'en-têtes de sécurité incomplète sur l'environnement de test

**État : CORRIGÉ — validation distante après redéploiement en attente.**

- Preuve distante : `GET https://test-commercant.localeo.city/` retourne 200 via Cloudflare avec `X-Content-Type-Options: nosniff`, mais sans `Content-Security-Policy`, `X-Frame-Options`, `Referrer-Policy` ni `Permissions-Policy`. Le même constat est observé sur JS, CSS, manifeste et service worker. Le dépôt ne définit pas non plus de CSP dans `index.html:3-14`.
- Impact : absence de défense en profondeur contre XSS, framing/clickjacking et fuite d'URL de provenance. L'application permet des actions métier authentifiées, ce qui rend l'anti-framing particulièrement pertinent.
- Correction : définir ces en-têtes à l'edge ; commencer la CSP en report-only, puis l'appliquer avec `frame-ancestors 'none'` ou une allowlist documentée. Valider HSTS séparément après confirmation de HTTPS sur tous les sous-domaines concernés.
- Mesure compensatoire : règle Cloudflare bloquant l'embedding et surveillance des violations CSP avant enforcement.
- Mise en œuvre : `render.yaml` versionne CSP, anti-framing, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, cache immutable des assets hashés et rewrite SPA. La CSP autorise l'API de production, les images HTTPS et blob nécessaires aux aperçus, tout en bloquant objets, framing et bases externes. L'application de cette configuration au service Render existant doit être confirmée dans le Dashboard ou via Blueprint Sync.

### UX-03 — Type MIME incorrect du manifeste PWA

**État : CORRIGÉ — validation distante après redéploiement en attente.**

- Preuve distante : `GET https://test-commercant.localeo.city/manifest.webmanifest` retourne 200 et 436 octets, mais `Content-Type: binary/octet-stream`. Le serveur de développement prévoit pourtant `application/manifest+json` dans `vite.config.js:49-52` ; cette configuration ne s'applique pas au fichier statique déployé.
- Impact : détection ou installation PWA non fiable selon le navigateur et téléchargement possible du manifeste au lieu de son interprétation.
- Correction : configurer Cloudflare/l'hébergeur pour servir `.webmanifest` en `application/manifest+json; charset=utf-8`, puis vérifier l'installabilité dans Chrome et Safari.
- Mesure compensatoire : aucune nécessaire si l'installation PWA n'est pas un parcours MVP critique, mais la correction est XS.
- Mise en œuvre : une règle Render ciblée sur `/manifest.webmanifest` impose `application/manifest+json; charset=utf-8`. Le serveur Vite local utilisait déjà ce type.

### PERF-03 — Mesure Lighthouse insuffisamment robuste

**État : CORRIGÉ — validation CI Linux en attente.** La configuration est reconnue et Lighthouse tente bien trois passes, mais Chrome échoue au démarrage/nettoyage sous Windows avant toute mesure exploitable.

- Preuve initiale : `lighthouserc.json:7` configurait une seule exécution. L'audit local a échoué lors du nettoyage/démarrage du profil Chrome et n'a produit aucun score exploitable.
- Impact : variabilité élevée et absence de baseline fiable pour détecter une régression.
- Correction : exécuter au moins trois passes en CI Linux, conserver la médiane et archiver les rapports ; ajouter des budgets explicites LCP/CLS/INP/TBT et poids des ressources.
- Mise en œuvre : Lighthouse CI effectue désormais trois passes et impose LCP ≤ 2,5 s, CLS ≤ 0,1, avec avertissements FCP > 2 s et TBT > 300 ms. Les artefacts locaux Lighthouse et Playwright sont ignorés par Git.

### UX-02 — Garde-fous d'upload incomplets côté interface

**États : CORRIGÉ · VALIDÉ.** Validation : cinq cas unitaires de format/taille réussis, build production réussi et régression du scan QR supprimée.

- Preuve : `src/App.jsx:2634-2647` vérifie seulement `file.type.startsWith("image/")`; `src/App.jsx:2988-2991` utilise `accept="image/*"` sans taille maximale annoncée ni vérifiée avant envoi.
- Impact : attente inutile et message tardif pour un fichier trop lourd ; le MIME déclaré par le navigateur n'est pas une garantie de sécurité.
- Correction : indiquer formats/taille, vérifier la taille avant envoi, compresser/redimensionner pour l'UX ; conserver tous les contrôles de sécurité côté serveur.
- Mise en œuvre : le sélecteur accepte uniquement JPEG, PNG et WebP ; le code refuse avant réseau tout fichier de plus de 5 Mo et affiche un message précis. La validation est centralisée et couverte par cinq cas unitaires. Ces contrôles restent des garde-fous UX et ne remplacent pas ceux du serveur.

## 4. Analyse UX/UI

### Parcours couverts

- route protégée sans session vers la connexion ;
- consultation d'une animation et retour à la même liste ;
- ouverture et acceptation confirmée d'une invitation sous mocks ;
- lisibilité des reversements ;
- visibilité du scanner dans le premier écran mobile ;
- contrôle axe-core de la liste d'animations.

Résultat après correction : les six scénarios E2E sont passants, y compris axe-core. Le dépôt présente de bons fondamentaux : focus de route testé, live announcer, états vides/chargement/erreur fréquents, boutons d'action désactivés pendant plusieurs soumissions et cibles tactiles minimales de 44 px.

Non vérifié : rendu interactif de l'environnement distant, contraste visuel complet, zoom 200/400 %, lecteurs d'écran réels, clavier sur tous les dialogues, contenus longs, coupures réseau sur tous les parcours, double soumission de toutes les actions et responsive tablette. À terminer avec une session de test réelle sur Chrome/Firefox/Safari et NVDA/VoiceOver.

## 5. Analyse des performances

### Mesures retenues

- build production final réussi en 0,81 s ;
- JS principal final : 332,05 Ko brut / 94,42 Ko gzip ;
- CSS final : 73,43 Ko brut / 13,02 Ko gzip ;
- chunks différés : dashboard 11,50 Ko, animations 25,67 Ko, reversements 3,61 Ko ;
- icône de shell : 555 114 octets ; sept fichiers de polices : environ 172 Ko ;
- aucun score Core Web Vitals valide obtenu.

Le découpage différé existant est positif. Les priorités sont l'image de marque surdimensionnée, la rationalisation des polices, le fan-out des invitations et la stabilisation des mesures CI. Les performances base de données, compression CDN, cache API, temps serveur, mémoire et volumes réels restent à mesurer depuis une plateforme connectée au backend.

## 6. Analyse de sécurité

### Contrôles positifs observés

- lockfile présent et CI utilisant `npm ci` (`.github/workflows/frontend-quality.yml:17`) ;
- React rend les données métier via JSX, sans `dangerouslySetInnerHTML`, `eval`, `document.write` ou réception `postMessage` détectés ;
- API protégée centralisée avec bearer token ;
- QR Animation soumis à une allowlist d'origines et chemins canoniques ;
- service worker sans cache d'API ou de données personnelles : il gère uniquement push et navigation same-origin ;
- fenêtres d'impression ouvertes avec `noopener,noreferrer` ;
- secrets privés évidents non détectés dans les variables examinées ; la clé Web Push est publique par nature.

### Risques et vérifications incomplètes

Les corrections prioritaires sont SEC-01 à SEC-04. Côté serveur, exiger des tests d'autorisation objet et tenant pour chaque endpoint contenant un ID, des quotas sur login/reset/upload/support/validation, la validation réelle des images, la rotation des sessions, la non-journalisation des tokens et mots de passe, la vérification des webhooks Stripe, ainsi que des sauvegardes/restaurations testées. Ces contrôles ne sont pas attestables depuis ce dépôt frontend.

## 7. Checklist de mise en production

### Application et infrastructure

- [ ] Corriger UX-01 et obtenir une CI entièrement verte sur le commit candidat.
- [ ] Corriger SEC-01 et SEC-02 ; accepter explicitement les risques P2 restants.
- [ ] Construire avec `npm ci` puis `npm run build:prod`, déployer uniquement `dist`.
- [ ] Vérifier que Vite dev/preview n'est jamais exposé en production.
- [ ] Exécuter trois Lighthouse CI et archiver les rapports.

### Configuration, secrets et réseau

- [ ] Confirmer qu'aucune variable `LOCALEO_*` sensible n'est embarquée : `envPrefix` expose toutes ces variables au client (`vite.config.js:69`).
- [ ] Vérifier TLS, CSP, nosniff, clickjacking, referrer et permissions sur les réponses réelles.
- [ ] Vérifier CORS par allowlist exacte et absence de wildcard avec credentials.
- [ ] Tester rotation/révocation des sessions et absence de tokens dans logs/monitoring.

### Base, fichiers, exploitation et conformité

- [ ] Authentifier/quoter l'upload, valider et réencoder les images côté serveur.
- [ ] Tester les autorisations inter-commerçants/communes sur chaque ressource.
- [ ] Tester sauvegarde, restauration, migrations et rollback sur copie réaliste.
- [ ] Configurer logs corrélés, alertes 5xx/latence/auth/upload et rétention maîtrisée.
- [ ] Documenter données personnelles, finalités, durées, export et suppression.
- [ ] Vérifier signature/idempotence des webhooks Stripe et procédure d'incident.

### Smoke tests après déploiement

- [ ] Connexion, expiration et déconnexion de session.
- [ ] Scan QR nominal, QR invalide, double scan et interruption réseau.
- [ ] Profil, upload image, brouillon et soumission modération.
- [ ] Invitation acceptée/refusée avec double clic empêché.
- [ ] Stripe Connect retour/refresh et reversements.
- [ ] Push notification/deeplink, installation PWA et mise à jour du service worker.

## 8. Plan de correction

### Obligatoire avant déploiement

1. Protéger et quoter `/public/dam/images` (SEC-01).
2. Mettre à niveau React Router et tester toutes les navigations (SEC-02).
3. Rendre le panneau ARIA pendant tous les états et remettre E2E/CI au vert (UX-01).
4. Valider strictement les URLs Stripe (SEC-04).
5. Vérifier en environnement accessible les en-têtes, autorisations tenant, quotas, TLS, webhooks, sauvegardes et smoke tests.

### Dans les 7 jours suivant le lancement

1. Réduire l'icône et les polices, supprimer les assets inutilisés (PERF-01).
2. Supprimer le fan-out N+1 des invitations (PERF-02).
3. Fiabiliser Lighthouse et créer une baseline à trois passes (PERF-03).
4. Ajouter taille/formats et compression UX des images (UX-02).
5. Corriger le type MIME du manifeste PWA (UX-03) et définir la trajectoire de migration du bearer token hors Web Storage (SEC-03).

### Améliorations ultérieures

- décomposer progressivement `App.jsx` et `styles.css` par domaines sans régression ;
- étendre les E2E aux erreurs, doubles soumissions, retour arrière et réseau interrompu ;
- ajouter tests lecteurs d'écran, navigateurs multiples et budgets de performance par route ;
- automatiser revue de dépendances et SBOM.

## 9. Critères finaux GO/NO-GO

Le verdict devient `GO sous conditions` puis `GO` seulement si :

- aucun P0/P1 n'est ouvert ;
- `npm test`, `npm run build:prod`, `npm run test:e2e` et `npm run test:lighthouse` passent sur le même commit ;
- `npm audit` ne contient aucune vulnérabilité high/critical exploitable au runtime, avec exceptions d'outillage documentées et isolées de la production ;
- l'upload exige une identité, des droits, quotas, taille/type réels et stockage sûr ;
- les tests d'isolation inter-commerçants et d'autorisation serveur passent ;
- les URLs Stripe sont `https:` et limitées aux hôtes attendus ;
- les réponses déployées possèdent les en-têtes de sécurité approuvés ;
- trois passes Lighthouse sur mobile atteignent au minimum les budgets actuels (performance 0,75, accessibilité 0,90, bonnes pratiques 0,85), sans régression majeure de LCP/CLS/INP ;
- sauvegarde/restauration et rollback ont été testés ;
- les smoke tests critiques passent sur l'environnement candidat.

## Les cinq actions les plus urgentes

1. Fermer l'upload DAM anonyme.
2. Mettre React Router à une version corrigée.
3. Corriger le `tabpanel` absent pendant le chargement et remettre la CI au vert.
4. Valider les URLs Stripe côté client et serveur.
5. Ajouter les en-têtes de sécurité manquants et exécuter les parcours authentifiés, contrôles tenant, quotas et sauvegardes sur le commit candidat exact.
