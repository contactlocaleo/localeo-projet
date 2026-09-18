# Audit MVP préproduction — Localeo Animation

Date : 29 août 2026  
Périmètre : dépôt `localeo-animation`, audit en lecture seule hors présent rapport  
Référentiel : risques MVP, OWASP pertinent au frontend React/TypeScript

## 1. Synthèse exécutive

**Verdict du réaudit du 30 août 2026 : corrections applicatives prêtes, mais NO-GO production tant que l'image Docker, les en-têtes effectifs, le responsive au navigateur et les parcours backend ne sont pas validés en recette.**

État courant : **10 constats CORRIGE**, dont **7 VALIDE** par contrôles reproductibles ; **3 corrections attendent une validation runtime** (MVP-01, MVP-03, MVP-05). MVP-04 reste ouvert car sa correction sûre exige une évolution coordonnée du backend (cookie `HttpOnly`, protection CSRF et gestion de session).

| Sévérité | Nombre |
|---|---:|
| P0 | 0 |
| P1 | 3 |
| P2 | 6 |
| P3 | 2 |

Les trois risques bloquants sont : une image Docker qui ne reçoit pas l'URL d'API et dont le proxy ne correspond pas aux routes appelées, une déconnexion qui ne révoque pas la session conformément au contrat OpenAPI, et une coque authentifiée non adaptée aux petits écrans malgré l'exigence mobile du MVP. Les principaux risques secondaires concernent le stockage du bearer token dans `localStorage`, l'absence d'en-têtes de sécurité, les limites d'accessibilité, le chargement monolithique, la troncature silencieuse au-delà de 100 éléments et l'absence de tests/lint/typecheck.

Niveau de confiance global : **moyen à élevé**. Les constats de code, de contrat et de build sont reproductibles. La confiance UX dynamique et backend est limitée par l'absence de navigateur connecté, d'API joignable, de backend, de base, de migrations et d'infrastructure de production dans ce dépôt.

### Architecture et parcours critiques

- SPA React 18 + TypeScript, construite par Vite 8 et servie soit statiquement, soit par Nginx dans une image multi-stage.
- `src/app/App.tsx` concentre routage, écrans et orchestration (341 358 octets) ; `src/app/api.ts` décrit le contrat client ; `src/app/httpClient.ts` centralise réseau/authentification.
- API externe via `VITE_API_URL`; aucun backend, modèle de données ou migration n'est présent.
- Authentification bearer, session persistée dans le navigateur.
- Parcours critiques cartographiés : connexion/session/déconnexion ; dashboard ; création et gestion d'animations ; demandes commerçants ; paiement des lots ; tirage/gains ; participants/validations ; flyers/exports ; support.

### Protocole exécuté

- Inventaire du dépôt, documentation, configuration, dépendances, variables (noms uniquement), contrat OpenAPI, appels réseau, état Git et recherches ciblées de sinks/règles OWASP.
- Build : `corepack.cmd pnpm build` — succès.
- Démarrage : `corepack.cmd pnpm dev --host 127.0.0.1` — succès sur `http://127.0.0.1:5173/`.
- Contrôle HTTP : `Invoke-WebRequest http://127.0.0.1:5173/` — 200 ; POST de connexion sans backend — 404.
- Audit dépendances : lecture de `pnpm-audit.json` (0 vulnérabilité sur 301 dépendances) et tentative `corepack.cmd pnpm audit --json`, sans résultat exploitable.
- Installation figée : `corepack.cmd pnpm install --frozen-lockfile` a demandé de supprimer/réinstaller `node_modules`; opération non confirmée pour préserver l'environnement. Le build utilise donc les modules déjà présents.
- Navigateur : connexion tentée selon le protocole du navigateur intégré ; aucun navigateur n'était disponible. Aucun Lighthouse/Core Web Vitals ni parcours visuel/clavier n'a donc été mesuré.

### Réaudit de validation — 30 août 2026

- `corepack.cmd pnpm check` : **succès** — TypeScript, ESLint, 4 tests de contrat sur 4 et build de production.
- `corepack.cmd pnpm audit --prod --json` : **succès** — 0 vulnérabilité info, low, moderate, high ou critical sur 258 dépendances de production.
- Smoke HTTP du serveur Vite : **200**, document racine présent, titre sans marqueur « Dev ».
- Build de production : **succès**, sans avertissement de configuration ; 1 628 modules transformés.
- Navigateur intégré : **indisponible** après tentative de connexion ; validation visuelle responsive et clavier non exécutée.
- Docker : **indisponible** dans l'environnement de réaudit ; construction de l'image et contrôle `curl -I` sur Nginx non exécutés.
- Backend/API : absent de ce dépôt et non joignable ; révocation effective du token, isolation multi-tenant et parcours métier de bout en bout restent à valider en recette.
- État Git : les modifications préexistantes de roadmap/spécifications hors audit ont été préservées.

## 2. Tableau des constats

### MVP-01 — Configuration Docker incompatible avec l'API réelle

- État de correction : **CORRIGE**
- État de validation : **À VALIDER EN IMAGE** — build applicatif et configuration inspectés avec succès ; moteur Docker indisponible pendant le réaudit.
- Axe : performance / sécurité opérationnelle
- Sévérité : **P1**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : déploiement Docker, tous les parcours API
- Description : l'image ne déclare aucun `ARG`/`ENV VITE_API_URL`; `.dockerignore` exclut le lockfile; le fallback Nginx ne proxifie que `/api/`, alors que le client appelle `/public/...` et `/protected/...` quand l'URL est vide. `proxy_pass http://backend:80/` dépend en outre d'un hôte non défini dans ce dépôt.
- Impact : la connexion et tous les parcours métier sont indisponibles avec la recette Docker documentée, ou servis par le fallback SPA au lieu du backend.
- Preuve : `src/env.ts:1-6`, `Dockerfile:7-14`, `.dockerignore:8`, `nginx.conf:6-12`, `DEPLOY.md:1-10`; le POST local vers `/public/identite-acces/animation/sessions` renvoie 404 sans backend.
- Reproduction : construire l'image sans argument explicite puis inspecter le bundle pour l'URL d'API ; lancer l'image et POSTer sur `/public/identite-acces/animation/sessions`.
- Correction : choisir une stratégie unique et testée : (a) `ARG VITE_API_URL` puis `ENV VITE_API_URL=$VITE_API_URL` au stage builder, avec secret/publicité documentés, ou (b) appels relatifs sous `/api` et proxy Nginx vers une URL backend résoluble sans supprimer par erreur le préfixe. Copier `pnpm-lock.yaml` et supprimer le fallback `|| pnpm install`.
- Mesure compensatoire : déployer en Static Site avec `VITE_API_URL` défini au build et effectuer un smoke test API avant ouverture.
- Effort : **S**

### MVP-02 — La déconnexion ne révoque pas la session serveur

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — contrat automatisé vert et quality gate complet réussi.
- Axe : sécurité
- Sévérité : **P1**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : déconnexion/session
- Description : le client fait `POST /auth/logout`; le contrat embarqué définit `DELETE /protected/identite-acces/animation/sessions/current` avec bearer token.
- Impact : l'interface efface localement la session même si l'appel échoue, mais le token reste valide côté serveur jusqu'à expiration. Un token copié ou compromis continue donc de fonctionner après « Se déconnecter ».
- Preuve : `src/app/api.ts:689-691`, `src/app/App.tsx:6058-6063`, `src/imports/openapi.json:18003-18044`.
- Reproduction : se connecter, conserver le token dans un client HTTP, cliquer sur déconnexion, puis appeler `GET /protected/identite-acces/animation/sessions/me` avec ce token ; il ne doit plus être accepté.
- Correction : appeler `httpClient.delete(getApiUrl('/protected/identite-acces/animation/sessions/current'))`; tester que la réponse est 204 et que le token devient inutilisable. Décider explicitement du comportement hors ligne, sans masquer la non-révocation.
- Mesure compensatoire : réduire fortement la durée des sessions et fournir une révocation administrative jusqu'au correctif.
- Effort : **XS**

### MVP-03 — Coque authentifiée non responsive sur mobile

- État de correction : **CORRIGE**
- État de validation : **À VALIDER AU NAVIGATEUR** — build et inspection du drawer responsive réussis ; aucun navigateur intégré disponible pour les quatre largeurs cibles.
- Axe : UX/UI
- Sévérité : **P1**
- Statut / confiance : **probable / élevée par inspection, dynamique à vérifier**
- Fonctionnalité : navigation et tous les écrans authentifiés
- Description : la racine utilise `h-screen overflow-hidden`, avec une sidebar toujours visible et fixe à `w-56`; aucune variante mobile, drawer ou masquage responsive ne lui est appliqué. La TopBar reste sur une seule ligne.
- Impact : à 320–375 px, 224 px sont consommés par la sidebar, laissant trop peu de largeur aux formulaires, tableaux et actions critiques. Le MVP mobile est fortement dégradé.
- Preuve : `src/app/App.tsx:1091-1149`, `1190-1272`, `6137-6152`. La recherche responsive ne trouve aucune règle sur la sidebar.
- Reproduction : ouvrir une session à 320×568 et 375×667, parcourir dashboard, liste, détail et assistant de création, vérifier absence de chevauchement/défilement horizontal et accès à toutes les actions.
- Correction : sidebar en drawer mobile avec déclencheur accessible, TopBar adaptable, conteneurs/tableaux à défilement contrôlé, puis tests aux largeurs 320/375/768/1440 px.
- Mesure compensatoire : annoncer temporairement un support desktop uniquement si le périmètre métier l'autorise explicitement.
- Effort : **M**

### MVP-04 — Bearer token persistant dans `localStorage`

- État de correction : **NON CORRIGE — BACKEND REQUIS**
- État de validation : **NON APPLICABLE**
- Axe : sécurité
- Sévérité : **P2**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : authentification/session
- Description : la session complète, token inclus, est sérialisée dans `localStorage` et relue au démarrage.
- Impact : toute XSS sur l'origine, extension malveillante ou accès local au profil peut extraire un bearer token réutilisable. L'absence de CSP augmente le rayon d'impact.
- Preuve : `src/app/auth.ts:4-10`, `18-38`; `src/app/httpClient.ts:29-35`.
- Reproduction : après connexion, constater la clé `localeo_session` dans le stockage du navigateur (ne pas copier le token dans des logs).
- Correction : préférer une session en cookie `HttpOnly`, `Secure`, `SameSite` avec protection CSRF adaptée ; sinon token court en mémoire, rotation et révocation efficaces.
- Mesure compensatoire : TTL court, CSP stricte, hygiène XSS et révocation serveur.
- Effort : **L** (backend inclus)

### MVP-05 — En-têtes de sécurité et politique de cache absents de Nginx

- État de correction : **CORRIGE**
- État de validation : **À VALIDER EN IMAGE** — directives CSP, anti-framing, nosniff et cache inspectées ; réponses Nginx non testables sans moteur Docker.
- Axe : sécurité / performance
- Sévérité : **P2**
- Statut / confiance : **confirmé dans la recette Docker / élevée**
- Fonctionnalité : shell SPA et actifs statiques
- Description : Nginx ne définit ni CSP, ni `X-Content-Type-Options`, ni protection anti-framing, ni `Referrer-Policy`, ni `Permissions-Policy`; aucune stratégie de cache longue pour les actifs hashés ni cache court pour HTML n'est définie.
- Impact : défenses navigateur réduites contre XSS/clickjacking et rechargements inutilement coûteux. Une couche edge externe pourrait compenser, mais elle n'est pas visible.
- Preuve : `nginx.conf:1-13`; `index.html:1-15`.
- Reproduction : `curl -I` sur `/` et un actif de l'image déployée, puis contrôler les en-têtes.
- Correction : ajouter les en-têtes au serveur/edge, CSP d'abord en report-only puis enforce, et cache `immutable` pour `/assets/*` hashés avec `no-cache` pour `index.html`.
- Mesure compensatoire : appliquer et vérifier les mêmes politiques au CDN/edge.
- Effort : **S**

### MVP-06 — Accessibilité clavier et noms accessibles incomplets

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — test de contrat des contrôles critiques, lint, types et build verts.
- Axe : UX/UI
- Sévérité : **P2**
- Statut / confiance : **confirmé par inspection / élevée**
- Fonctionnalité : connexion, navigation, notifications, dialogues
- Description : les labels de connexion ne sont pas associés aux champs (`htmlFor`/`id` absents), plusieurs boutons icône n'ont qu'un `title` ou aucun nom accessible, les notifications cliquables sont des `div` sans clavier/role, et plusieurs overlays maison n'exposent ni `role=dialog`, ni modalité, ni gestion de focus.
- Impact : lecteurs d'écran et utilisateurs clavier ne peuvent pas identifier ou activer fiablement des fonctions critiques.
- Preuve : `src/app/App.tsx:988-1014`, `1137-1142`, `1208-1236`, `1251-1266`, `1041-1059`; exemple d'overlay `2030-2054`.
- Reproduction : Tab/Shift+Tab depuis la connexion et dans notifications/dialogues ; inspection de l'arbre d'accessibilité ; test NVDA/VoiceOver.
- Correction : lier labels/champs, ajouter `aria-label`, utiliser `button` pour les éléments interactifs, adopter les composants Dialog Radix existants avec focus trap/restauration, garantir un focus visible.
- Mesure compensatoire : aucune acceptable pour les actions critiques ; prioriser connexion et navigation.
- Effort : **M**

### MVP-07 — Chargement initial monolithique et image surdimensionnée

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — build mesuré : JS principal 440,27 kB (115,02 kB gzip), QR différé 23,47 kB et icône 3,70 kB.
- Axe : performance
- Sévérité : **P2**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : chargement initial
- Description : le build produit un seul chunk applicatif de 461,02 kB (122,57 kB gzip) et une icône PNG de 555,12 kB affichée à 40–44 px. Les vues sont rendues via un switch mais importées statiquement ; `Suspense` ne crée aucun découpage.
- Impact : téléchargement, parsing et exécution inutiles avant la connexion et sur chaque parcours, particulièrement sensibles sur mobile/réseau lent.
- Preuve : sortie de `corepack.cmd pnpm build`; `src/app/App.tsx:1-48`, `974`, `1095-1099`, `6114-6149`; actif `src/imports/localeo-animation-icon.png` de 555 126 octets.
- Reproduction : lancer le build et relever les tailles ; profiler le réseau sur cache vide.
- Correction : `React.lazy` par grandes vues, extraire `App.tsx`, optimiser l'icône en SVG/WebP/PNG dimensionné, supprimer les dépendances non utilisées.
- Mesure compensatoire : compression Brotli/Gzip et cache immutable, sans remplacer le découpage.
- Effort : **M**

### MVP-08 — Listes silencieusement limitées à 100 éléments

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — test automatisé de collecte multipage vert.
- Axe : UX/UI / performance
- Sévérité : **P2**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : animations, participants, demandes commerçants
- Description : plusieurs écrans demandent `page_size: 100` puis filtrent/localement affichent ces résultats, sans navigation vers les pages suivantes. D'autres index appellent la liste avec la pagination par défaut.
- Impact : dès le 101e élément, données et actions deviennent invisibles, donnant une vue métier fausse.
- Preuve : `src/app/App.tsx:1518-1533`, `1585`, `4475-4479`, `4714`; `src/app/components/MerchantParticipationTab.tsx:81-84`.
- Reproduction : injecter 101+ animations/participants/demandes et rechercher l'élément de la page 2.
- Correction : pagination serveur explicite avec contrôles, total visible, recherche serveur et conservation des filtres.
- Mesure compensatoire : surveillance de volume et export complet accessible jusqu'au correctif.
- Effort : **M**

### MVP-09 — Aucun filet automatisé lint/typecheck/test

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — `pnpm check` réussit : typecheck, lint, 4/4 tests et build.
- Axe : sécurité / performance / UX
- Sévérité : **P2**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : livraison
- Description : seuls `dev` et `build` existent ; aucun test, lint, typecheck ou CI n'est présent. Vite transpile TypeScript mais ne constitue pas un contrôle de types complet.
- Impact : régressions sur auth, paiements, doubles soumissions, erreurs réseau, accessibilité et contrats API non détectées avant production.
- Preuve : `package.json:7-10`, absence de fichiers `*test*`/`*spec*`, `tsconfig*.json`, configuration ESLint et workflow CI.
- Reproduction : `rg --files -g '*test*' -g '*spec*' -g 'tsconfig*.json' -g '.github/**'`.
- Correction : ajouter au minimum typecheck strict, lint, tests unitaires du client/auth/routage, tests composants des états, et E2E des parcours critiques dans CI.
- Mesure compensatoire : recette manuelle signée et smoke tests documentés avant chaque déploiement.
- Effort : **L**

### MVP-10 — Affordances visibles sans action réelle

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — test de contrat vert ; les actions inachevées sont désormais explicitement indisponibles.
- Axe : UX/UI
- Sévérité : **P3**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : connexion, commune, aide
- Description : « Mot de passe oublié ? » n'a aucun handler ; le sélecteur de commune n'a aucune action ; Documentation et FAQ ne font qu'afficher un toast.
- Impact : perte de confiance et blocage de récupération de compte, sans indication que les fonctions sont indisponibles.
- Preuve : `src/app/App.tsx:1002-1005`, `1192-1196`, `3525-3543`.
- Reproduction : activer ces contrôles ; aucune navigation ni mutation n'a lieu.
- Correction : implémenter les parcours ou masquer/désactiver explicitement avec message honnête avant MVP.
- Mesure compensatoire : lien de support fonctionnel et procédure de récupération manuelle.
- Effort : **S**

### MVP-11 — Marqueur « Dev » et monitoring non câblé

- État de correction : **CORRIGE**
- État de validation : **VALIDE** — titre HTTP contrôlé sans marqueur Dev, instrumentation d'erreurs inspectée, lint/types/build verts.
- Axe : UX/UI / sécurité opérationnelle
- Sévérité : **P3**
- Statut / confiance : **confirmé / élevée**
- Fonctionnalité : shell et gestion d'erreurs
- Description : le titre HTML contient « Dev » ; `VITE_SENTRY_DSN` est lu mais jamais utilisé et l'ErrorBoundary ne remonte rien.
- Impact : qualité perçue réduite et erreurs de rendu invisibles pour l'exploitation.
- Preuve : `index.html:9`, `src/env.ts:3`, `src/app/ErrorBoundary.tsx:16-19`.
- Reproduction : provoquer une erreur de rendu et vérifier l'absence d'événement de monitoring.
- Correction : titre de production, branchement d'un outil de monitoring avec filtrage PII, release et source maps privées.
- Mesure compensatoire : journalisation edge et canal support surveillé.
- Effort : **S**

## 3. Analyse UX/UI

### Parcours examinés

- Connexion : cas nominal inspecté ; validation HTML native et état de chargement présents ; erreur réseau affichée. Double clic réduit par `disabled={loading}`. Récupération de mot de passe absente.
- Session : expiration et reconnexion prévues ; déconnexion locale fonctionne, révocation serveur incorrecte.
- Navigation : routes et retour arrière via `popstate` présents. Sur URL inconnue, retour silencieux au dashboard (`src/app/App.tsx:219-245`) plutôt qu'un état 404.
- Création/gestion d'animation : assistant multi-étapes, confirmations et états de chargement présents ; tests dynamiques des interruptions/doubles soumissions impossibles sans backend/navigateur.
- Tirage, gains, paiements, suppressions : idempotency keys employées sur de nombreuses commandes (`src/app/api.ts:712-918`), contrôle positif. Les DELETE ne reçoivent pas de clé d'idempotence et restent à vérifier côté serveur.
- États : skeletons, vides, erreurs/retry et toasts sont largement présents. Plusieurs contrôles restent factices et les dialogues maison sont faibles en accessibilité.

Le design est cohérent visuellement par inspection (palette, espacements, composants récurrents), mais la preuve responsive et accessibilité dynamique manque. Les contenus longs sont souvent tronqués, parfois avec `title`; les tableaux devront être vérifiés avec noms/emails/communes longs et valeurs absentes.

## 4. Analyse des performances

### Mesures observées

Conditions : Windows, Node 24.14.0, dépendances locales existantes, Vite 8.2.1, build de production.

| Ressource | Brut | Gzip calculé par Vite |
|---|---:|---:|
| JS principal | 440,27 kB | 115,02 kB |
| JS erreurs | 20,54 kB | 5,11 kB |
| JS QR différé | 23,47 kB | 8,86 kB |
| CSS | 125,18 kB | 20,27 kB |
| Icône PNG importée | 3,70 kB | non indiqué |
| HTML | 0,73 kB | 0,39 kB |

Build de réaudit réussi en 1,72 s, 1 628 modules transformés. Aucune métrique LCP/INP/CLS/TTFB n'est annoncée : Lighthouse et navigateur indisponibles. Les temps locaux ne sont pas représentatifs de la production.

### Goulots et contrôles positifs

- Risques confirmés : chunk principal unique, image trop lourde, absence de cache Nginx, composant monolithique.
- Risques déduits : nombreuses vues et dépendances chargées avant besoin ; listes jusqu'à 100 entrées rendues/filtrées côté client.
- Contrôles positifs : timeout réseau 20 s, retries désactivés par défaut, déduplication des GET simultanés (`src/app/httpClient.ts:38-42`, `103-115`), pagination contractuelle disponible, SVG natif pour les graphiques.
- Backend non présent : N+1, index SQL, requêtes lentes, CPU/mémoire serveur, compression API et cache serveur non vérifiables.

## 5. Analyse de sécurité

### Risques confirmés

- Bearer token exposé au JavaScript persistant (MVP-04).
- La révocation client (MVP-02), les en-têtes Nginx (MVP-05) et la reproductibilité Docker (MVP-01) sont corrigés dans le code ; leur comportement bout en bout reste à confirmer sur une recette avec backend et moteur Docker.

### Contrôles efficaces observés

- Aucun secret suivi dans `.env`; seul `.env.example` est versionné. Les valeurs `VITE_*` sont correctement à considérer publiques.
- Aucun `dangerouslySetInnerHTML`, `eval`, `new Function`, `document.write`, service worker ou `postMessage` applicatif détecté.
- JSX échappe les chaînes affichées ; URL et identifiants de routes sont encodés dans plusieurs chemins.
- Client HTTP centralisé, timeout/abort, bearer header, déduplication des GET, clés d'idempotence sur de nombreuses commandes.
- Lockfile présent dans le dépôt hors contexte Docker ; `pnpm-audit.json` enregistré indique 0 vulnérabilité connue sur 301 dépendances.

### Vérifications incomplètes et risque résiduel

- Backend absent : authentification réelle, hash de mots de passe, rate limiting, autorisation objet/tenant, validation serveur, injections, CORS, cookies/CSRF, logs, webhooks Stripe, fichiers, export/suppression/rétention, sauvegardes et isolation des communes **non vérifiés**. Risque résiduel élevé ; auditer le dépôt backend et tester deux tenants/comptes sur un environnement dédié.
- Production/edge non accessibles : TLS, DNS, headers effectifs, WAF, compression, cache, erreurs et observabilité **non vérifiés**. Vérifier par `curl -I`, SSL Labs/équivalent autorisé et console de la plateforme après déploiement de recette.
- Dépendances : le scan en ligne du 30 août 2026 indique 0 vulnérabilité connue sur 258 dépendances de production. Le rejouer en CI à chaque livraison, car ce résultat évolue avec les avis de sécurité.
- Paiements : retours succès/annulation routés côté client, mais signature webhook, vérification serveur, montants, devise, idempotence et rapprochement **non vérifiés**. Tester avec Stripe sandbox et événements rejoués.
- Upload/DAM : l'application saisit une URI, pas un fichier ; allowlist d'origines et sécurité du serveur DAM **non vérifiées**.

## 6. Checklist de mise en production

- [ ] Build depuis un clone propre avec `pnpm install --frozen-lockfile` et lockfile inclus dans Docker.
- [ ] `VITE_API_URL` effectivement présent dans le bundle attendu ou proxy relatif validé ; aucun secret dans `VITE_*`.
- [ ] Smoke tests connexion, contexte, liste, création, publication, paiement sandbox, tirage, export, déconnexion/révocation.
- [ ] Typecheck, lint, tests et E2E verts en CI ; artefact immuable identifié par SHA.
- [ ] Migrations backend appliquées sur copie/restauration testée ; plan de rollback documenté.
- [ ] Sauvegarde base chiffrée, restauration chronométrée et objectifs RPO/RTO approuvés.
- [ ] HTTPS valide, redirection HTTP→HTTPS et domaine/DNS contrôlés.
- [ ] CSP, anti-framing, nosniff, Referrer-Policy, Permissions-Policy et cache vérifiés sur les réponses réelles.
- [ ] CORS limité aux origines nécessaires ; cookies et CSRF validés selon le mode d'authentification.
- [ ] Secrets dans le gestionnaire de la plateforme, rotation et moindre privilège ; aucun secret dans logs/bundle/source maps.
- [ ] Rate limiting sur login, support, exports, tirages et actions coûteuses.
- [ ] Monitoring frontend/backend, corrélation, métriques, alertes 5xx/latence et procédure d'astreinte.
- [ ] Pages d'erreur et indisponibilité testées ; messages sans stack/PII.
- [ ] Politique RGPD : finalités, minimisation, consentements, droits d'accès/export/suppression, rétention et sous-traitants.
- [ ] Déploiement progressif, rollback artefact + base et responsable de décision identifiés.
- [ ] Après déploiement : smoke test synthétique, vérification headers, logs, version affichée et absence d'erreurs console.

## 7. Plan de correction

### Obligatoires avant déploiement

1. Corriger et tester la chaîne Docker/API/lockfile (MVP-01), car elle conditionne tous les autres tests.
2. Corriger la révocation de session et ajouter son test bout en bout (MVP-02).
3. Décider le support mobile ; si inclus comme demandé, corriger la coque et valider 320/375/768/1440 px (MVP-03).
4. Ajouter les en-têtes de sécurité minimum et vérifier les réponses réelles (MVP-05).
5. Mettre en place une recette backend dédiée et exécuter les smoke tests auth, tenant, paiement, mutations et exports.

### Dans les 7 jours suivant le lancement

1. Corriger les blocages clavier/lecteur d'écran prioritaires (MVP-06).
2. Implémenter la pagination serveur complète (MVP-08).
3. Ajouter les quality gates CI minimaux et tests des parcours critiques (MVP-09).
4. Découper le bundle et optimiser l'icône (MVP-07).
5. Câbler monitoring et alertes, supprimer le marqueur Dev (MVP-11).

### Améliorations ultérieures

1. Migrer la session vers un mécanisme réduisant l'exposition XSS (MVP-04), en coordination avec le backend/CSRF.
2. Finaliser ou retirer les affordances factices (MVP-10).
3. Mesurer Lighthouse/Core Web Vitals sur données et appareils représentatifs, puis fixer des budgets.

## 8. Critères finaux GO/NO-GO

Le GO ne peut être donné que si tous les critères suivants sont démontrés :

- Image/Static Site issu d'un clone propre, build figé réussi, et SHA affiché correspondant au commit livré.
- Connexion réelle réussie ; réponse API JSON ; aucun appel `/public`/`/protected` servi par le fallback HTML.
- Déconnexion : l'ancien token reçoit 401 sur `/sessions/me` immédiatement après révocation.
- Aucun P0/P1 ouvert. Tout P2 reporté possède propriétaire, échéance et mesure compensatoire validée.
- Parcours création → publication → paiement sandbox → tirage → envoi gain → export exécuté sans erreur bloquante, avec double clic et interruption réseau testés.
- Deux comptes de tenants/communes différents ne peuvent lire ou modifier les ressources l'un de l'autre (tests IDOR serveur).
- 320, 375, 768 et 1440 px : aucune action critique inaccessible, aucun scroll horizontal de page, navigation clavier complète.
- En-têtes production vérifiés ; TLS valide ; aucun secret dans bundle, logs ou source maps publiques.
- Test avec 101+ éléments : l'élément de page 2 est trouvable et actionnable.
- CI verte : build, typecheck, lint, tests unitaires/intégration et E2E critiques.
- Sauvegarde/restauration et rollback testés ; alertes 5xx/latence reçues par un responsable.

## Cinq actions les plus urgentes

1. Réparer la configuration Docker/API et rendre l'installation strictement reproductible.
2. Corriger l'endpoint de déconnexion et prouver la révocation du token.
3. Mettre à disposition une recette backend et exécuter les tests d'autorisation multi-tenant/paiement.
4. Corriger la coque mobile puis valider les quatre largeurs cibles au navigateur.
5. Poser les en-têtes de sécurité et les quality gates CI avant le feu vert.
