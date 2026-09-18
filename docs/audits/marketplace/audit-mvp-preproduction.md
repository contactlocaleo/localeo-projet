# Audit MVP préproduction — Localeo Marketplace

Date : 29 août 2026  
Périmètre : dépôt `localeo-marketplace`, révision locale non modifiée (un fichier non suivi préexistant dans `docs/roadmap`)  
Méthode : revue statique React/Vite/Node, build production, audit npm, serveur local de production et suite Playwright du dépôt. Aucun test destructif ni appel de production.

## 1. Synthèse exécutive

**Verdict après contre-audit : GO sous conditions.** Les neuf constats directement corrigeables dans ce dépôt sont corrigés et validés. Les conditions restantes portent sur les systèmes absents du périmètre local : backend, autorisations multi-tenant, webhooks/paiement réels, base et infrastructure déployée.

| Constats initiaux | P0 | P1 | P2 | P3 |
|---|---:|---:|---:|---:|
| Identifiés | 0 | 3 | 5 | 1 |
| Restant ouverts après validation | 0 | 0 | 0 | 0 |

Principaux risques : divulgation de jetons donnant accès à des achats/coffrets, parcours principal totalement cassé par une variable de déploiement absente, et fausse perception d'échec après un paiement potentiellement réussi. Niveau de confiance global : **élevé sur le dépôt frontend et son serveur**, **faible à moyen sur le système complet**, car le backend, la base, les migrations, Stripe/webhooks, le reverse proxy/CDN et la configuration Render réelle ne sont pas présents.

Limites : navigateur intégré indisponible ; les parcours UI ont donc été vérifiés via Playwright local. Aucun compte ni donnée réaliste, aucun test de charge, aucune mesure Lighthouse/Core Web Vitals, aucun test lecteur d'écran, aucun pentest du backend, aucune validation de sauvegarde/restauration BDD, de TLS/DNS ou d'observabilité en production. L'audit des dépendances couvre les avis publiés par npm au moment du test, pas les vulnérabilités inconnues.

## 2. Tableau des constats

### MVP-SEC-01 — Jetons d'accès et données personnelles dans les URL

- **Axe / sévérité :** Sécurité — **P1**
- **État de correction : CORRIGÉ** — les paramètres sensibles sont capturés puis supprimés immédiatement de l'URL, ne sont plus propagés entre pages et le jeton d'activation n'est plus rendu dans l'interface.
- **État de validation : VALIDÉ** — assertions Playwright de nettoyage sur activation, confirmation, gestion pro, QR et consultation ; suite complète réussie deux fois.
- **Statut / confiance / effort :** confirmé / élevé / M
- **Fonctionnalités :** activation, consultation de coffret, gestion pro, retour paiement
- **Description :** les jetons d'activation, de consultation et de gestion sont lus puis réinjectés dans la query string ; l'adresse e-mail bénéficiaire est également placée dans l'URL. Le jeton d'activation est même rendu en clair dans un champ et sur la confirmation.
- **Impact :** exposition dans l'historique, captures, copier-coller, journaux de proxy/analytics et en-tête `Referer` vers des ressources tierces. Selon les droits du jeton, une fuite peut donner accès à un achat ou à un coffret. L'e-mail est une donnée personnelle.
- **Preuve :** `ActiverCoffretPage` construit la confirmation avec `token`, `email` et `consultation_token`; `RetourPaiementPage` ajoute `management_token`; la couche API persiste l'autorisation dans `sessionStorage` sans nettoyer l'URL.
- **Reproduction :** ouvrir `/activer-coffret?achat_id=A&coffret_instance_id=C&token=SECRET`, activer avec une réponse contenant `email_beneficiaire` et `consultation_token`, puis observer l'URL de `/activation-confirmee`; même observation avec `/retour-paiement?...&management_token=SECRET`.
- **Fichiers/lignes :** `src/pages/ActiverCoffretPage.jsx:12-13,55-61,96-97`; `src/pages/ActivationConfirmeePage.jsx:9-16`; `src/pages/RetourPaiementPage.jsx:64-70,130`; `src/services/api.js:66-87,110-132`; `src/store/sessionStore.js:1-16`.
- **Correction :** échanger une seule fois les liens à jeton contre une session serveur protégée par cookie `HttpOnly; Secure; SameSite`, puis supprimer immédiatement les paramètres via `history.replaceState`. Ne jamais remettre un jeton ou un e-mail dans les routes suivantes ; ne pas afficher le jeton brut.
- **Mesure compensatoire :** politique `Referrer-Policy: no-referrer`, durée/usage unique des jetons, révocation rapide, filtrage systématique des URL dans logs et analytics.

### MVP-PERF-01 — Le serveur accepte une configuration qui rend toute l'API inutilisable

- **Axe / sévérité :** Performance/disponibilité — **P1**
- **État de correction : CORRIGÉ** — le serveur refuse désormais toute configuration de production sans URL API HTTPS absolue et répond en JSON 502 sur `/api/*` au lieu du fallback SPA.
- **État de validation : VALIDÉ** — tests serveur fail-fast et anti-fallback réussis deux fois.
- **Statut / confiance / effort :** confirmé sous condition / élevé / S
- **Fonctionnalité :** toutes les données et transactions
- **Description :** sans `LOCALEO_API_BASE_URL`, `server.cjs` publie `/api`; ce serveur ne proxifie pourtant pas `/api` et renvoie le HTML SPA pour toute route inconnue.
- **Impact :** l'application se charge mais tous les appels métier reçoivent `index.html`; découverte, achat, activation et support deviennent inutilisables. Le défaut est silencieux jusqu'aux premiers appels.
- **Preuve :** lancement `PORT=8180 npm start`, puis `GET /app-config.js` retourne `LOCALEO_API_BASE_URL: "/api"`; le fallback SPA est inconditionnel.
- **Reproduction :** `npm run build`; démarrer `npm start` sans variable; appeler `/app-config.js`, puis `/api/public/referencement/villes` : la seconde réponse est le document HTML.
- **Fichiers/lignes :** `server.cjs:13-26,87-98`; `src/services/api.js:14-40`; `README.md:31-64`.
- **Correction :** en environnement production, refuser de démarrer si l'URL API absolue HTTPS manque, ou implémenter/configurer explicitement le reverse proxy `/api`. Exclure `/api/*` du fallback SPA et retourner un 502/404 JSON.
- **Mesure compensatoire :** variable Render obligatoire et smoke test automatisé vérifiant un endpoint API réel avant bascule trafic.

### MVP-UX-01 — Une panne réseau au retour de paiement est présentée comme un échec

- **Axe / sévérité :** UX/UI — **P1**
- **État de correction : CORRIGÉ** — trois tentatives bornées, état indéterminé explicite, consigne anti-double achat et action de reprise remplacent désormais la fausse redirection d'échec.
- **État de validation : VALIDÉ** — scénario Playwright panne persistante puis reprise réussie, passé lors des deux suites complètes.
- **Statut / confiance / effort :** confirmé / élevé / M
- **Fonctionnalité :** retour de paiement
- **Description :** si la vérification par `session_id` échoue, l'erreur est seulement journalisée hors production ; l'état reste `pending`, puis l'utilisateur est redirigé vers `/echec-paiement`. Aucun retry, délai, bouton de reprise ou message « paiement en vérification » n'est proposé.
- **Impact :** un client débité pendant une interruption réseau raisonnable peut croire son achat échoué, recommencer et générer support ou double achat.
- **Preuve :** le `catch` continue le flux, puis toute valeur différente de `succes` déclenche la redirection d'échec.
- **Reproduction :** activer le paiement, ouvrir `/retour-paiement?session_id=test` en bloquant l'appel `.../achats/depuis-session/test`; observer la redirection vers `/echec-paiement?statut=pending...`.
- **Fichiers/lignes :** `src/pages/RetourPaiementPage.jsx:60-87,112-125`; `src/services/api.js:457-466`.
- **Correction :** état dédié « vérification en cours », retries bornés avec backoff, action « Réessayer », reprise après rechargement et résolution idempotente côté serveur ; réserver l'écran d'échec aux statuts négatifs vérifiés.
- **Mesure compensatoire :** lien de suivi envoyé par e-mail et consigne support explicite, sans proposer un second paiement tant que le statut est inconnu.

### MVP-SEC-02 — En-têtes HTTP de sécurité absents

- **Axe / sévérité :** Sécurité — **P2**
- **État de correction : CORRIGÉ** — CSP, `Referrer-Policy`, `nosniff`, protection d'encapsulation et `Permissions-Policy` sont appliqués à toutes les réponses du serveur.
- **État de validation : VALIDÉ** — test HTTP automatisé des en-têtes réussi deux fois.
- **Statut / confiance / effort :** confirmé au serveur Node / élevé / S
- **Fonctionnalité :** surface web entière
- **Description/impact :** le serveur local ne publie ni CSP, ni `X-Content-Type-Options`, ni `Referrer-Policy`, ni protection d'encapsulation (`frame-ancestors`/`X-Frame-Options`). Cela augmente l'impact d'une XSS, la fuite d'URL sensibles et le clickjacking. Un edge peut les ajouter, mais aucune preuve n'est disponible.
- **Preuve/reproduction :** `Invoke-WebRequest http://127.0.0.1:8180/accueil` ne retourne que type, cache et en-têtes Node usuels.
- **Fichiers/lignes :** `server.cjs:48-67`; `index.html:1-29`.
- **Correction :** ajouter au serveur/edge une CSP testée, `Referrer-Policy: no-referrer`, `X-Content-Type-Options: nosniff`, `Permissions-Policy` minimale et `frame-ancestors 'none'` ou liste métier. Déployer CSP d'abord en report-only si nécessaire.
- **Mesure compensatoire :** configuration équivalente contrôlée au CDN avec test de non-régression.

### MVP-SEC-03 — Dépendances React Router avec avis de sécurité connus

- **Axe / sévérité :** Sécurité — **P2**
- **État de correction : CORRIGÉ** — React Router DOM/Router ont été migrés vers `7.18.2`; Vite et son plugin React ont aussi été portés vers les versions corrigées, avec un plancher Node `20.19.0` explicite.
- **État de validation : VALIDÉ** — `npm audit --json` retourne zéro vulnérabilité et le build Vite 8 réussit.
- **Statut / confiance / effort :** confirmé / élevé / S
- **Fonctionnalité :** routage
- **Description/impact :** `npm audit --omit=dev --json` signale trois paquets de production de sévérité modérée, dont des redirections ouvertes/XSS. L'app emploie des destinations issues d'API (`ShortLinkRedirectPage`, notifications), ce qui justifie la correction même si toutes les variantes SSR ne s'appliquent pas.
- **Preuve/reproduction :** commande ci-dessus : 0 critique, 0 haute, 3 modérées, correction disponible ; avis `GHSA-2j2x-hqr9-3h42`, `GHSA-wrjc-x8rr-h8h6`, `GHSA-337j-9hxr-rhxg`, `GHSA-jjmj-jmhj-qwj2`.
- **Fichiers/lignes :** `package.json:15-19`; `package-lock.json:764,1608,1623`; `src/pages/ShortLinkRedirectPage.jsx:5-14,39-47`.
- **Correction :** mettre React Router à une version corrigée compatible, reconstruire, exécuter les 24 tests puis retester les redirections `//`, antislash et schémas actifs.
- **Mesure compensatoire :** limiter toutes les destinations à une allowlist d'origines et de chemins côté backend et frontend.

### MVP-PERF-02 — Aucune compression ni mise en cache des assets fingerprintés

- **Axe / sévérité :** Performance — **P2**
- **État de correction : CORRIGÉ** — le serveur négocie Brotli/gzip, ajoute `Vary` et ETag, met `/assets/*` en cache immuable un an et conserve HTML/configuration en `no-store`.
- **État de validation : VALIDÉ** — tests de négociation Brotli/gzip et d'asset fingerprinté immuable réussis deux fois.
- **Statut / confiance / effort :** confirmé au serveur Node / élevé / S
- **Fonctionnalité :** chargement initial et revisites
- **Description/impact :** les fichiers hashés sont servis sans gzip/Brotli, `Cache-Control`, ETag ni `Vary`. Le bundle principal JS de 256 138 octets est donc transféré intégralement ; le CSS global fait 257,21 kB. Les revisites retéléchargent les ressources.
- **Preuve/reproduction :** build Vite : JS initial 256,09 kB (80,35 kB gzip), CSS initial 257,21 kB (41,28 kB gzip). `GET /assets/index-8in9kqzW.js` via `npm start` : 256 138 octets, sans `Content-Encoding` ni cache.
- **Fichiers/lignes :** `server.cjs:48-67`; `src/main.jsx:10-16`.
- **Correction :** compression Brotli/gzip au proxy ou serveur, et `Cache-Control: public,max-age=31536000,immutable` pour `/assets/*`; conserver HTML et `app-config.js` non cachés. Ajouter un budget de bundle.
- **Mesure compensatoire :** servir derrière un CDN configuré et vérifier les en-têtes sur le domaine final.

### MVP-PERF-03 — Cascade de quatre appels pour afficher un coffret

- **Axe / sévérité :** Performance — **P2**
- **État de correction : CORRIGÉ** — instance et prestations sont chargées en parallèle, les annulations React Query sont propagées à chaque fetch et une annulation n'est plus masquée par le fallback commerçants.
- **État de validation : VALIDÉ** — inspection du graphe d'appels, build réussi et parcours détail/QR réussis dans deux suites complètes.
- **Statut / confiance / effort :** confirmé par inspection / élevé / M
- **Fonctionnalité :** détail et QR d'un coffret
- **Description/impact :** instance puis prestations sont chargées séquentiellement, puis détail coffret, puis commerçants. Sur réseau mobile, quatre RTT s'additionnent avant le contexte complet ; les méthodes GET ne propagent généralement pas d'`AbortSignal`.
- **Preuve/reproduction :** suivre `fetchConsumerCoffretInstanceContext`; les quatre `await` sont en cascade. Les pages QR et détail appellent ce contexte.
- **Fichiers/lignes :** `src/services/api.js:211-218,469-493`; `src/pages/AfficherQrCoffretPage.jsx:357-363`; `src/pages/CoffretInstancePage.jsx:398-404`.
- **Correction :** paralléliser instance/prestations, agréger le contexte côté API si possible, puis lancer les dépendances restantes ; propager `signal` à tous les fetchs et mesurer p50/p95 avant/après.
- **Mesure compensatoire :** skeleton déjà présent et cache React Query de 60 s.

### MVP-UX-02 — Dialogues Live sans confinement clavier complet

- **Axe / sévérité :** UX/UI — **P2**
- **État de correction : CORRIGÉ** — un confinement cyclique Tab/Shift+Tab couvre tous les dialogues Live, empêche le focus de sortir vers l'arrière-plan et fournit un nom accessible à l'inbox.
- **État de validation : VALIDÉ** — test Playwright dédié du cycle Tab et du retour forcé dans l'inbox réussi.
- **Statut / confiance / effort :** probable / moyen / M
- **Fonctionnalité :** onboarding, confidentialité, QR, inscription, notifications
- **Description/impact :** les dialogues utilisent `aria-modal` et reçoivent un focus initial, mais aucun focus trap ni inertie du contenu arrière n'est implémenté. Le dialogue notifications n'a pas de nom accessible. Au clavier/lecteur d'écran, Tab peut atteindre l'arrière-plan et le contexte du dialogue devient ambigu.
- **Preuve/reproduction :** inspection du gestionnaire global : focus du premier bouton et Escape uniquement. À terminer dans un navigateur avec Tab/Shift+Tab et NVDA/VoiceOver.
- **Fichiers/lignes :** `src/live/LiveApp.jsx:63-79,156,257,341,351`.
- **Correction :** composant Dialog partagé avec titre accessible, confinement cyclique du focus, `inert` sur l'arrière-plan, restauration du focus et tests clavier automatisés.
- **Mesure compensatoire :** Escape et restauration du focus existent déjà.

### MVP-QUAL-01 — Couverture de validation incomplète et suite intermittente

- **Axe / sévérité :** UX/UI — **P3**
- **État de correction : CORRIGÉ** — ESLint couvre désormais tout le dépôt, cinq tests serveur et des scénarios Playwright réseau/URL ont été ajoutés, avec une commande `npm test` unifiée. Deux fichiers JSX historiques syntaxiquement invalides ont aussi été réparés.
- **État de validation : VALIDÉ** — `npm test` réussi deux fois consécutivement à 25/25, puis une troisième fois à 26/26 après ajout du contrôle clavier dédié ; lint 0 erreur et serveur 5/5 à chaque passage.
- **Statut / confiance / effort :** confirmé / élevé / M
- **Fonctionnalité :** qualité globale
- **Description/impact :** il n'existe ni lint, ni tests unitaires/intégration hors un fichier Playwright. La première exécution a donné 22/24, puis les deux échecs Live ont passé isolément (2/2), indiquant une interdépendance ou instabilité. Aucun contrôle automatique d'accessibilité, de doubles soumissions hors cas couverts, de retour arrière ou de réseau lent global.
- **Preuve/reproduction :** `npm run test:visual:desktop` → 22 réussis, 2 échoués en 3,6 min ; `npx playwright test --config=playwright.desktop.config.cjs --last-failed` → 2 réussis en 32,5 s.
- **Fichiers/lignes :** `package.json:7-14`; `tests/visual/desktop-layout.spec.cjs:1-790`; `playwright.desktop.config.cjs:1-27`.
- **Correction :** isoler état/service worker/IndexedDB par test, ajouter lint, tests des services et scénarios paiement/activation réseau, clavier et double clic.
- **Mesure compensatoire :** la suite couvre déjà 24 scénarios desktop/mobile représentatifs.

## 3. Analyse UX/UI

Parcours rendus par Playwright : accueil à 1024/1280/1440/1920, pages publiques représentatives, catalogue et fiche coffret mobile, accueil sans commune et géolocalisation, commerçant, confirmations particulier/pro, suivi, commande/gestion pro, activation, retour paiement, consultation/impression QR, contact, pages juridiques, erreurs, avis et Localeo Live. Les 22 scénarios initiaux réussis confirment l'absence de débordement horizontal sur les tailles testées, la présence de plusieurs états vides/erreur, des boutons désactivés pendant soumission et une idempotence pour achat/inscription.

Priorité UX : corriger la récupération du retour paiement (MVP-UX-01), puis auditer réellement le clavier et les lecteurs d'écran sur les dialogues (MVP-UX-02). Les doubles clics sont correctement limités sur les principaux formulaires inspectés (`loading`/`submitting` + `Idempotency-Key`), mais le backend doit confirmer l'idempotence. Les retours arrière contenant encore des jetons restent à corriger via MVP-SEC-01.

## 4. Analyse des performances

Mesures locales observées : build réussi en 8,30 s, 179 modules ; entrée JS 256,09 kB / 80,35 kB gzip ; CSS global 257,21 kB / 41,28 kB gzip ; chunks par route effectifs, dont `LiveApp` 83,80 kB / 23,25 kB gzip. Le serveur Node transmet réellement 256 138 octets pour l'entrée JS, sans compression ni cache. Trois familles Google Fonts et douze graisses sont demandées par une feuille externe bloquante (`index.html:4-10`).

Risques déduits : cascade API du détail coffret, CSS global volumineux et dépendance réseau aux polices. Core Web Vitals, TTFB réel, mémoire/CPU, volumes et p95 API non mesurés : ils exigent une préproduction représentative, Lighthouse/WebPageTest et télémétrie RUM. Base, index, pagination serveur et N+1 backend non vérifiables dans ce dépôt.

## 5. Analyse de sécurité

Risques confirmés : exposition de jetons/PII dans les URL, absence d'en-têtes au serveur fourni et dépendances vulnérables. Contrôles efficaces observés : rendu React sans `dangerouslySetInnerHTML`; SVG QR traité par un service dédié; paramètres de chemins encodés; requêtes sensibles utilisent des en-têtes d'autorisation; clé d'idempotence sur achat et inscription; analytics possède une liste de paramètres sensibles à exclure; configuration runtime ne contient pas de secret serveur.

Vérifications incomplètes : autorisation objet/tenant, durée et révocation des jetons, CORS/CSRF/cookies, rate limiting, injections, SSRF, uploads, webhooks Stripe, validation backend, logs, suppression/export/rétention RGPD, secrets d'infrastructure et sécurité BDD. Méthode recommandée : audit séparé du dépôt backend et de la configuration déployée, tests d'autorisation croisée avec deux comptes/tenants, inspection des webhooks signés, scan SAST/DAST non destructif sur préproduction et revue des journaux expurgés.

## 6. Checklist de mise en production

- [ ] Tous les P1 ci-dessus corrigés et retestés.
- [ ] `LOCALEO_API_BASE_URL` HTTPS validée au démarrage ; `/api/*` ne tombe jamais sur le fallback SPA.
- [ ] Build reproductible Node 20, tests deux fois consécutives sans échec, audit npm sans vulnérabilité exploitable.
- [ ] Secrets uniquement dans le gestionnaire de secrets ; aucune URL/log/analytics ne contient de jeton ou PII.
- [ ] Migrations backend testées sur copie réaliste, sauvegarde restaurée, plan rollback chronométré.
- [ ] HTTPS/TLS, domaine, CORS et en-têtes sécurité/cache/compression vérifiés sur l'URL finale.
- [ ] Supervision synthétique accueil + API + checkout, logs avec `request_id`, alertes 5xx/latence/webhooks.
- [ ] Page et procédure de récupération pour erreurs paiement/API ; contact support opérationnel.
- [ ] Politique RGPD, consentement analytics, durées de conservation, export/suppression vérifiés avec le backend.
- [ ] Smoke tests post-déploiement : accueil, recherche, fiche, achat sandbox, retour paiement, activation, QR, Live, contact et liens juridiques.

## 7. Plan de correction

**Obligatoire avant déploiement, dans cet ordre :** (1) supprimer les jetons/PII des URL et définir leur échange/révocation côté backend ; (2) corriger le retour paiement avec statut indéterminé récupérable ; (3) rendre la configuration API fail-fast et ajouter le smoke test ; (4) mettre à jour React Router et poser les en-têtes de sécurité ; (5) activer compression/cache et exécuter deux fois la suite complète.

**Dans les 7 jours suivant le lancement :** paralléliser/agréger le contexte coffret, instrumenter p50/p95 et Core Web Vitals, fiabiliser l'isolation Playwright, tester clavier/lecteur d'écran et ajouter les scénarios réseau interrompu/double soumission.

**Ultérieurement :** fractionner le CSS critique, auto-héberger/subsetter les polices, ajouter lint/tests unitaires, budgets bundle et tests de volume.

## 8. Critères finaux de GO/NO-GO

GO uniquement si : zéro P0/P1 ouvert ; aucune URL finale ne contient `token`, `management_token`, `consultation_token` ou e-mail après l'échange initial ; un test réseau du retour paiement récupère un succès vérifié sans proposer de repayer ; le serveur refuse une configuration API absente et le smoke test API retourne du JSON attendu ; la suite complète passe deux fois de suite ; `npm audit` ne contient aucun avis ; compression et cache sont observés sur `/assets/*`; les en-têtes sécurité sont présents sur le domaine final ; sauvegarde/rollback et webhook paiement sont validés en préproduction.

NO-GO si un de ces critères échoue, si l'autorisation croisée backend n'a pas été testée, ou si le statut d'un paiement réel peut rester ambigu sans récupération.

## Commandes et outils utilisés

`rg`, `git status --short`, `npm run build`, `npm run test:visual:desktop`, `npx playwright test --config=playwright.desktop.config.cjs --last-failed`, `npm audit --omit=dev --json`, `PORT=8180 npm start`, `Invoke-WebRequest` sur `/accueil`, `/app-config.js` et un asset fingerprinté, inspection des captures Playwright. Le navigateur intégré était indisponible.

## Contre-audit après corrections

- `npm run build` : réussi avec Vite 8.2.2, 168 modules, entrée JS 216,66 kB / 67,34 kB gzip et CSS 249,78 kB / 40,44 kB gzip.
- `npm audit --json` : 0 vulnérabilité critique, haute, modérée ou faible.
- `npm test`, exécution 1 : lint sans erreur, serveur 5/5, Playwright 25/25.
- `npm test`, exécution 2 : lint sans erreur, serveur 5/5, Playwright 25/25.
- Validation finale après ajout du test accessibilité : lint sans erreur, serveur 5/5 et Playwright 26/26.
- Conclusion locale : tous les constats du dépôt sont **CORRIGÉS et VALIDÉS**. Les limites backend/infrastructure énoncées dans la synthèse demeurent et empêchent un GO inconditionnel.

## Cinq actions les plus urgentes

1. Retirer immédiatement jetons et e-mail des URL et du rendu.
2. Rendre le retour paiement résilient aux erreurs réseau et aux statuts inconnus.
3. Faire échouer le démarrage si l'API de production n'est pas explicitement configurée.
4. Mettre à jour React Router et déployer les en-têtes de sécurité, en priorité `Referrer-Policy` et CSP.
5. Activer compression/cache des assets, puis obtenir deux exécutions Playwright consécutives à 24/24.
