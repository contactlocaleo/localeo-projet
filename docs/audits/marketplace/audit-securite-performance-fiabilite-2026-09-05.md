# Audit logiciel — Localeo Marketplace et Localeo Live

Date : 5 septembre 2026. Référence Git : `d823251`, avec les modifications locales préexistantes de `AccueilPage.jsx`, `LiveFeed.jsx` et `live.css`. Audit du répertoire de travail, pas d'une version certifiée déployée.

## Périmètre, méthode et limites

Application comprise : marketplace publique de découverte et d'achat de coffrets, commandes professionnelles, activation/consultation/QR/facturation et PWA de suivi des coffrets et animations. Stack constatée : React 18, React Router 7, TanStack Query 5, Vite 8, serveur statique Node natif, IndexedDB et Web Storage. Hébergement Render décrit dans le README ; déploiement réel non inspecté.

Périmètre autorisé utilisé : sources, contrat OpenAPI local, documentation, configuration sous forme de code, métadonnées Git, dépendances et contrôles locaux isolés. Aucun correctif appliqué. Les seuls nouveaux fichiers sont ce rapport et deux scripts de diagnostic. Les fichiers `.env*` contenant des valeurs, les journaux existants, les secrets, les données du navigateur utilisateur et les comptes métier n'ont pas été consultés. Les valeurs utilisées pour les reproductions sont fictives.

Informations manquantes pour conclure sur le système complet : dépôt et version du backend ; matrice de rôles et de droits ; mécanismes d'expiration/révocation ; configuration réelle des domaines/CDN/TLS/CORS ; schéma et index BDD ; transactions et migrations ; configuration du prestataire de paiement et des webhooks ; volumes et pics ; SLO/SLA ; métriques p50/p95/p99 ; journaux expurgés ; sauvegardes et preuves de restauration ; contrats et registre des traitements. L'absence de ces informations n'est pas assimilée à l'absence des protections correspondantes.

Déroulement : cartographie des flux, lecture des composants sensibles, vérification des sources officielles pertinentes, lint et tests serveur existants, reproductions unitaires avec API/stockage simulés, essai SVG dans un navigateur vierge sans accès réseau, mesures de taille, classement et recommandations. Aucune charge ni intrusion sur un environnement distant. Seuls le registre npm et des documentations publiques ont été interrogés.

### Architecture et frontières de confiance

```text
Navigateur — même origine pour Marketplace et Live
  ├─ React / routes chargées à la demande / cache TanStack Query
  ├─ sessionStorage : contexte, brouillon pro, accès de gestion
  ├─ IndexedDB : carnet, jetons de consultation, installation Live
  ├─ Service worker /live/ : cache et notifications
  ├─ API métier externe : catalogue, paiement, achats, suivi, facturation
  ├─ prestataire de paiement : redirection vers checkout_url
  └─ Google Analytics : script chargé après acceptation

Serveur Node de production : dist + app-config.js + en-têtes HTTP
Vite en développement : proxy /api vers le backend configuré
Backend / BDD / prestataire / infrastructure : hors dépôt audité
```

Le serveur fourni ne relaie pas l'API en production : `/api/*` renvoie explicitement 502. Les contrôles de droits reposent nécessairement sur le backend ; les flags de routes frontend ne constituent pas une autorisation. Les jetons de consultation, activation, gestion et installation sont des capacités sensibles. Leur portée effective et leur validité ne peuvent pas être déduites des seuls noms de champs.

## A. Résumé exécutif

**Risque élevé sur les parcours sensibles du frontend, principalement en raison du passage de jetons dans les données Analytics. Aucune vulnérabilité critique ni compromission en production n'a été démontrée.** Le niveau de sécurité de l'ensemble backend/infrastructure reste indéterminé.

Les points forts sont concrets : CSP sans `unsafe-inline` ni `unsafe-eval` pour les scripts dans le serveur fourni, protection iframe, `Referrer-Policy: no-referrer`, validation HTTPS de la base API en production, liste explicite de clés de configuration publique, cache long des assets fingerprintés, compression, routes chargées à la demande, clés d'idempotence sur plusieurs parcours et page de retour paiement distinguant un résultat inconnu d'un échec. Le crédit B2B est conservé en mémoire avec contrôle de date. Le lint et les cinq tests serveur passent ; npm ne signale aucun avis de vulnérabilité dans l'arbre audité.

Les cinq risques majeurs :

1. **Jetons dans Analytics — F01.** Les paramètres de requête sont filtrés, mais les chemins de participation/feedback contenant un jeton sont conservés. Avec Analytics activé et accepté, ils sont placés dans les événements. Conséquence possible : accès à une ressource via un lien divulgué, selon la portée du jeton.
2. **Filtre SVG contournable — F02.** Exécution JavaScript reproduite sur SVG fictif en navigateur sans CSP ; la politique de scripts du serveur bloque le même essai. L'exploitabilité déployée dépend donc de la CSP et de la capacité d'un attaquant à fournir le SVG.
3. **Diffusion évitable d'informations sensibles — F03/F04.** Coordonnées personnelles placées dans l'URL d'initialisation d'achat ; jeton brut et données décodées affichés sur l'écran d'impression QR. Risques de conservation dans les traces, les copies de liens et les impressions.
4. **État local Live incohérent — F07/F09.** Création concurrente de plusieurs installations et mélange possible des communes pendant la pagination. Risques de suivis rattachés à une identité écrasée et de rendez-vous affichés dans le mauvais contexte.
5. **Parcours dépendants d'appels non bornés — F10/F15.** Pas de délai applicatif central et fiche coffret attendant la fin du chargement de chaque commerçant. Une requête suspendue peut empêcher d'acheter ou de retrouver un accès ; une erreur marchande terminée affiche en revanche un bandeau tout en laissant le coffret disponible.

Actions urgentes : supprimer toute émission Analytics sur les routes à capacités tant qu'un filtrage sûr n'est pas validé ; retirer les données de diagnostic QR du rendu public ; fermer le contournement SVG ; confirmer les en-têtes réellement servis ; examiner, avec l'exploitant, si les flux Analytics/logs contiennent historiquement des accès sensibles. Toute purge ou révocation doit suivre une analyse d'impact et une autorisation, car elle peut invalider les liens de clients.

Estimation indicative : **1–3 jours-personne pour les premières protections frontend**, **12–20 jours-personne pour les principaux correctifs frontend/serveur et leurs tests**, puis **5–10 jours-personne de coordination backend/exploitation** selon les contrats existants. Ces enveloppes se recouvrent avec les estimations par constat : elles ne s'additionnent pas ligne à ligne. Elles excluent une refonte du backend et une certification de conformité. Charge réelle et infrastructure peuvent modifier fortement l'effort.

L'ancien rapport [docs/audits/audit-mvp-preproduction.md](audit-mvp-preproduction.md) annonce certains sujets corrigés. Cette affirmation historique ne clôt pas les constats actuels : les chemins Analytics et l'écran QR restent concernés. Le présent rapport décrit le code effectivement lu et les essais du 5 septembre.

## B. Tableau des constats

Légende : **C** = confirmé par code et/ou reproduction ; **P** = risque fortement probable, impact final à vérifier ; **H** = hypothèse à vérifier. P1 = traitement prioritaire, P2 = planifié à court terme, P3 = amélioration. La criticité qualifie le risque, la confiance qualifie la preuve ; ce sont deux dimensions distinctes. Efforts en jours-personne, comprenant un contrôle ciblé.

| ID | Domaine | Constat / confiance | Preuve principale | Criticité | Impact | Probabilité / condition | Correction | Effort | Priorité |
|---|---|---|---|---|---|---|---|---|---|
| F01 | Sécurité | Jeton de chemin conservé dans Analytics — C | `analytics.js:256,271,298`, sonde `analytics-path-token` | Élevée | Divulgation d'un accès de participation/feedback | Élevée si Analytics actif et accepté sur ces routes ; collecte distante non inspectée | Exclure routes sensibles et normaliser les routes autorisées | 1–2 | P1, 48 h |
| F02 | Sécurité | Filtre SVG contourné par animation d'URL — C ; exploit distant H | `safeSvg.js:1,14,36`, sonde Chromium | Moyenne ; élevée si SVG contrôlable et CSP absente | Exécution dans l'origine de l'application | Conditionnelle ; essai bloqué par la politique de scripts du serveur | Image passive ou assainisseur éprouvé avec liste de primitives QR | 1–2 | P1, 48 h |
| F03 | Confidentialité | Coordonnées d'achat en query string — C | `api.js:281,452–482`, contrat OpenAPI local | Moyenne | Copie dans traces HTTP/APM et outils intermédiaires | URL construite à chaque achat ; rétention des logs inconnue | Migrer contrat et client vers JSON ; filtrage des journaux | 1–3, front + API | P1 |
| F04 | Sécurité | Diagnostic QR public contient le jeton brut — C | `QrPrintPage.jsx:20,118–139` | Moyenne | Copies, captures et impressions augmentent l'exposition | Directe à l'ouverture de cette page ; droit déjà requis par le lien | Capturer puis nettoyer URL, masquer token/payload/KID | 0,5–1 | P1, 48 h |
| F05 | Vie privée | Retrait du consentement non propagé au script déjà chargé — P | `analytics.js:114–142,158–193`, sonde `analytics-withdrawal` | Moyenne | Mesure automatique susceptible de continuer | Dépend de GA4/mesure améliorée ; événements applicatifs bloqués | Propager le retrait et valider arrêt des émissions/cookies | 1–2 | P1 |
| F06 | Sécurité / PWA | Cache trop général, y compris chemins sensibles — C ; cache API conditionnel | `public/live/sw.js:14–26`, sonde cache | Moyenne | Persistance excessive, données anciennes ou sensibles hors ligne | Requêtes même origine sans `/api/`, sans query ni `/qr` | Cache réservé aux assets explicitement autorisés | 1–2 | P1 |
| F07 | Fiabilité | Création concurrente d'installations — C | `liveInstallation.js:10–24`, appels LiveApp/LiveAnimations | Moyenne | Identités et suivis divergents | Reproduit : 2 créations pour 2 appels sans identité initiale | Promesse partagée, coordination multi-onglets, idempotence API | 1–2 | P1 |
| F08 | Maintenabilité | Ancien formulaire Live à idempotence divergente, sans ouverture dans le parcours actuel — C | `LiveAnimations.jsx:127,136,155,174`, sonde de fonction isolée | Faible | Régression si ce code est réactivé | Hypothèse de réactivation ; pas de doublon sur le parcours actuel démontré | Retirer le code mort ou partager le formulaire actif | 0,5–1 | P3 |
| F09 | Fiabilité | Pagination d'une ancienne commune ajoutée à la nouvelle — C | `LiveFeed.jsx:139–155`, sonde pagination | Moyenne | Fil local faux et cache incohérent | Réponse tardive pendant changement de filtre/commune | Annulation et contrôle de génération/contexte | 0,5–1,5 | P2 |
| F10 | Fiabilité | Absence de délai applicatif central, annulation partielle — C | `api.js:217–328`, sonde checkout | Moyenne | Chargement prolongé, boutons bloqués, reprise paiement difficile | Connexion suspendue ou service qui ne termine pas | Délais par opération, signal propagé, reprise idempotente | 1–3 | P1 |
| F11 | Fiabilité serveur | Erreurs filesystem/stream non confinées — C ; panne process P | `server.cjs:102,137–140,180`, sonde EACCES simulée | Moyenne | Interruption possible de tout le service statique | Incident I/O ou course avec déploiement ; pas une attaque distante prouvée | `pipeline`, gestion erreurs et déploiement atomique | 1–2 | P2 |
| F12 | Déploiement / PWA | Asset absent renvoyé comme HTML 200, reprise incomplète — C | `server.cjs:185–186`, sonde asset manquant, `main.jsx:71–79` | Moyenne | Chargement de module impossible après changement de version | Ancien onglet/chunk supprimé ou cache incomplet | 404 assets, conservation versions, reprise contrôlée | 1–2 | P2 |
| F13 | Intégrité locale | Restauration du carnet non atomique et validation partielle — C | `liveLibrary.js:79–85`, sonde import partiel | Moyenne | Carnet partiellement remplacé malgré erreur globale | Sauvegarde incompatible ou quota/erreur de stockage | Validation complète puis transaction unique | 1–2 | P2 |
| F14 | Performance | Image principale PNG de 2 477 178 octets — C | `AccueilPage.jsx:812`, fichier dans `public/img` | Moyenne | Transfert initial coûteux sur mobile | Présente dans le rendu accueil ; LCP réel non mesuré | WebP/AVIF dimensionné, variantes responsives | 0,5–1 | P2 |
| F15 | Performance / fiabilité | Une requête par commerçant retarde le rendu de toute la fiche — C | `CoffretPage.jsx:299–309,477–497` | Moyenne | Latence de l'accès à l'achat via dépendance secondaire | Coût O(N) requêtes à cache froid ; attente du marchand le plus lent | Rendu progressif et/ou projection API agrégée | 1–3 | P2 |
| F16 | Tests | Suite visuelle couplée à une API distante et aux effets de bord — C | `playwright.desktop.config.cjs:19–25`, tests et `LiveApp.jsx:407` | Moyenne | Données de test modifiées, tests non déterministes | Appels non interceptés ; configuration réelle peut remplacer la cible | Réseau refusé par défaut + fixtures, intégration séparée | 1–3 | P1 avant automatisation |

### F01 — Jetons dans les données de navigation Analytics

`buildSanitizedPageContext` nettoie la query string puis concatène `resolvedPathname` tel quel. Les routes `src/App.jsx:207,214–215,224` contiennent explicitement `:token` ; `animationRegistration.js:37–38` fabrique également `/live/animations/ajouter/{token}`. `AnalyticsRouteTracker.jsx:15–22` suit les chemins sans exclure ces pages. La sonde confirme qu'un jeton fictif de chemin survit dans `page_location`, alors qu'un jeton de query string est retiré.

Conséquence technique : une valeur d'accès est passée à `gtag`. Conséquence métier possible : consultation ou utilisation d'une capacité par un tiers accédant aux traces, si le jeton est encore valide et suffisant. Ni accès aux données Google ni exploitation métier n'ont été tentés. La longueur maximale de 120 caractères n'est pas une protection : elle peut préserver tout ou partie du secret. Les premières commandes de configuration du tag n'établissent pas non plus un contexte de page explicitement assaini avant chargement.

Correction : ne pas initialiser le tag sur les routes sensibles en accès direct ; désactiver leur suivi lors d'une navigation SPA avec tag déjà chargé ; utiliser des noms de routes autorisés et non le chemin réel. Examiner aussi les événements automatiques, le titre et le référent collectés par le fournisseur. Compensation immédiate : désactiver Analytics globalement le temps du correctif si l'exclusion par route ne peut pas être livrée immédiatement. Vérifier les émissions dans un collecteur simulé et contrôler les traces historiques par un opérateur habilité, avec résultats expurgés.

### F02 — Contournement du nettoyage SVG

Le filtre retire certains éléments et vérifie seulement `href`, `xlink:href` et `src`. Il conserve `<animate attributeName="href" values="javascript:…">`. Le navigateur peut donc modifier une URL après nettoyage. Les points d'insertion sont `AfficherQrCoffretPage.jsx:377,530` et `QrPrintPage.jsx:26,110`.

Reproduction : `node docs/audits/probe-svg-2026-09-05.cjs`. Sur une page vierge, sans requête distante, un SVG fictif passé dans le vrai filtre conserve l'animation et exécute au clic uniquement `window.__auditSvgMarker=1`. Le même essai avec la politique de scripts du serveur conserve l'URL animée mais **n'exécute pas** le marqueur. La CSP est introduite via une balise meta pour cette contre-épreuve ; elle vérifie `script-src`, pas les directives HTTP telles que `frame-ancestors`.

La capacité d'un attaquant à influencer un SVG de l'API n'est pas établie. Ce constat prouve une barrière de nettoyage défaillante, pas une XSS exploitable en production. Préférer un QR livré en image passive ; sinon utiliser un assainisseur maintenu et une liste très restreinte de primitives SVG, sans liens, styles ni animation. [DOMPurify documente l'assainissement HTML/SVG et sa configuration](https://github.com/cure53/DOMPurify). Compensation : conserver et vérifier la CSP sur tous les modes d'hébergement ; elle ne remplace pas le nettoyage.

### F03 — Données personnelles dans l'URL de paiement

La sonde appelle le vrai client avec des valeurs fictives et intercepte `fetch` : méthode POST, aucun corps, présence de `email_client`, `telephone_client` et `nom_contact` dans la query string. Le contrat local `api/localeo-openapi.json`, opération `/public/gestion-achats/paiements/initialiser`, déclare bien ces coordonnées en paramètres `query` et ne déclare pas de `requestBody`.

Il faut donc une évolution coordonnée du contrat backend : remplacer seulement l'appel frontend par du JSON casserait potentiellement les achats. Un POST avec paramètres d'URL reste visible aux systèmes qui journalisent l'URI ; HTTPS ne retire pas ces valeurs des logs du destinataire. Aucune présence réelle dans les journaux n'a été recherchée. [OWASP recommande de tenir les informations sensibles hors des URL HTTP](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#sensitive-information-in-http-requests).

Correction : transition vers un corps JSON, tests de compatibilité, puis retrait des anciens paramètres. Compensation : filtrage des query strings sur les routes de paiement dans reverse proxy/APM et réduction des accès/rétentions. Vérifier également `fetchQrDetail`, qui envoie son jeton en query string (`api.js:600–601`).

### F04 — Écran d'impression QR trop révélateur

L'écran conserve `?token=…`, affiche le jeton brut, le KID et le JSON décodé ; le bloc de métadonnées n'est pas marqué `screen-only`. Il s'agit de la capacité déjà présentée par le porteur du lien : ce n'est pas un accès sans autorisation démontré. Cependant ce rendu multiplie les occasions de copie et laisse le secret dans une URL visible.

Correction : conserver uniquement le QR, les informations utiles et un état de validité, avec un diagnostic détaillé réservé à un outil d'assistance habilité. Capturer la capacité en mémoire avant nettoyage de l'URL, puis prévoir le comportement d'un rechargement et de l'impression. Compensation : limiter temporairement la distribution des liens d'impression et informer le support de ne pas demander de capture contenant le jeton. Tester l'URL, le DOM et le PDF d'impression avec valeurs fictives.

### F05 — Retrait du consentement incomplet dans la session ouverte

`setAnalyticsConsent('refused')` et `resetAnalyticsConsent()` modifient le stockage et émettent l'événement interne. Les événements envoyés par les wrappers applicatifs sont alors bloqués : c'est une protection effective. Mais aucun appel `gtag('consent', 'update', …)`, aucune désactivation fournisseur et aucune gestion des cookies déjà créés n'apparaissent. Le script déjà chargé reste actif.

La sonde confirme zéro commande de mise à jour et le blocage des wrappers. La poursuite d'événements automatiques dépend des réglages réels GA4 ; elle est probable, pas mesurée ici. [Google décrit la mise à jour du consentement lors d'un changement de choix](https://developers.google.com/tag-platform/security/guides/consent). [La CNIL rappelle que le consentement doit pouvoir être retiré à tout moment avec la même simplicité](https://www.cnil.fr/fr/cookies-et-autres-traceurs/que-dit-la-loi).

Correction : gérer l'état initial, l'acceptation, le retrait et le changement inter-onglets, en vérifiant les requêtes automatiques et non seulement `trackEvent`. Choisir explicitement une politique « aucune émission après refus » ou une autre politique juridiquement validée : un simple changement Consent Mode peut encore autoriser certaines requêtes sans cookies. Compensation : arrêt du tag jusqu'à validation. Ce contrôle technique ne constitue pas une certification RGPD.

### F06 — Cache PWA insuffisamment limité

Le worker accepte tout GET de même origine sans query string, sans `/api/` et sans `/qr`. Il ne filtre ni les en-têtes d'autorisation, ni `Cache-Control`, ni les chemins d'accès personnel. La sonde démontre qu'une réponse fictive `private, no-store` à une requête avec autorisation passe dans `cache.put`, et que le chemin d'ajout d'une animation avec jeton sert de clé de cache.

Nuance importante : l'API de production est décrite comme externe, donc ses réponses sont exclues par le contrôle d'origine. En développement `/api/` est exclu. Le risque de mise en cache de réponses métier exige une future configuration même origine sans ce préfixe ; ce n'est pas une fuite de réponses de production constatée. Pour les pages SPA à jeton, le HTML mis en cache est le shell, pas une fiche participant rendue côté serveur. C'est d'abord le **chemin sensible** qui persiste. La Cache API ne suit pas automatiquement les règles de cache HTTP ; les entrées doivent être gérées explicitement. [MDN, Cache](https://developer.mozilla.org/en-US/docs/Web/API/Cache).

Correction : liste positive d'assets et shell canonique ; aucun chemin de transfert, QR ou API ; contrôle des en-têtes ; stratégie explicite pour `app-config.js` et versions. Le code actuel ne rattache pas l'écriture de cache à `event.waitUntil` et ne gère pas son échec : la disponibilité hors ligne n'est donc pas garantie par le seul succès réseau. Compensation : conserver l'API sur l'origine prévue et traiter les caches existants lors de la migration.

### F07 — Installation Live non unique lors du premier accès

`ensureLiveInstallation` lit IndexedDB, crée une installation si absente puis l'enregistre. Il n'y a pas de promesse partagée. `LiveApp.jsx:407` et `LiveAnimations.jsx:149` peuvent déclencher cet accès dès l'ouverture du catalogue ; Settings et Push ajoutent d'autres chemins.

La sonde reproduit deux réponses d'installation différentes pour deux appels concurrents, alors qu'une seule identité finit stockée. Elle ne simule pas un backend de production. Des suivis rattachés à l'identité écrasée pourraient devenir invisibles depuis l'identité finale. Correction : dédupliquer les appels en cours, libérer le verrou en cas d'erreur et couvrir plusieurs onglets via verrou navigateur ou protocole idempotent backend. Compensation : charger une seule identité au niveau racine et la transmettre, après analyse des installations déjà créées.

### F08 — Ancien formulaire conservé avec une idempotence différente

Le formulaire Marketplace actif garde une clé dans une référence React. Un ancien gestionnaire du catalogue Live (`LiveAnimations.jsx:155`) appelle au contraire `crypto.randomUUID()` à chaque soumission. La sonde appelle directement cette fonction extraite : deux erreurs de retour sans changement de formulaire produisent deux clés distinctes.

**La traçabilité jusqu'à l'interface change le classement :** `registration` est initialisé à `null`, et ses seuls setters restants le remettent à `null`. Le bouton actuel (`LiveAnimations.jsx:127`) ouvre `/animations/{id}?inscription=1`, qui utilise le formulaire partagé. Aucun chemin actuel ouvrant l'ancienne modale n'a été trouvé. Cette sonde ne démontre donc pas un défaut de reprise accessible à l'utilisateur aujourd'hui. Le risque est une réactivation ultérieure du code mort, avec comportement différent. Correction à faible urgence : retirer cette branche après confirmation ou la remplacer par le formulaire partagé ; conserver des tests de reprise sur le parcours actif. La compensation actuelle est précisément le routage vers ce formulaire. Les doublons backend restent non vérifiés.

### F09 — Réponse tardive ajoutée au mauvais fil

Le chargement initial de `LiveFeed` possède un drapeau `active`, mais `loadMore` n'en possède pas. Après changement de commune ou de filtre, il ajoute sa réponse à l'état courant, puis écrit sous l'ancienne clé de cache capturée.

La sonde retarde la page 2 de la commune A, remplace l'état par la commune B puis libère la réponse A : les éléments B et A se retrouvent dans le même fil. Correction : une génération de requête ou une clé de contexte vérifiée au retour, plus annulation ; éventuellement `useInfiniteQuery` avec clé territoriale stable. Compensation : bloquer le changement de contexte pendant la pagination serait possible mais dégraderait l'expérience. Tester aussi le retour d'une erreur tardive et le démontage.

### F10 — Requêtes sans délai applicatif

Certains GET et POST acceptent un signal transmis par l'appelant. Il n'existe pas de budget temporel central. `postAsQuery`, `getWithHeaders`, PUT/PATCH/DELETE et téléchargements ne propagent pas tous un signal. La sonde du checkout constate l'absence de signal dans la requête.

Cela ne signifie pas qu'aucun délai n'existe dans le navigateur, TCP ou le backend. Cela signifie que l'application ne borne pas le temps avant de proposer une reprise. Les retries React Query ne commencent qu'après le rejet d'une tentative ; ils ne résolvent pas une tentative qui ne se termine pas. Correction : délai par classe d'opération, annulation cohérente et traitement métier de l'incertitude pour les écritures. Compensation : deadlines serveur/proxy documentées et écran de statut consultable sans refaire l'achat. Une expiration client ne prouve jamais que le paiement ou l'inscription a échoué.

### F11 — Défaut de confinement des erreurs serveur

Les `statSync` sont exécutés dans le gestionnaire HTTP sans protection. Les streams de fichiers et de compression sont reliés par `.pipe()` sans gestionnaire d'erreur. La sonde remplace seulement le filesystem par une erreur EACCES fictive : l'exception sort du gestionnaire.

Un incident I/O réel ou un fichier retiré entre vérification et lecture peut interrompre le processus ou une réponse ; aucun crash réel ni déni de service distant n'a été tenté. Les statuts d'auto-redémarrage et la redondance Render sont inconnus. Correction : erreurs de requête confinées, `stream.pipeline`, gestion client déconnecté, réponse générique et journaux corrélés sans URL sensible. Compensation : déploiement atomique et supervision/redémarrage. Le recours à des appels synchrones est également à mesurer sous charge avant de conclure à un goulot d'étranglement.

### F12 — Cohérence de version et récupération PWA

Une requête locale sur `/assets/AUDIT-MISSING.js` obtient **200, Content-Type text/html**, avec le shell SPA. C'est inadapté à une ressource JS manquante. Un onglet ancien qui charge ensuite un chunk supprimé peut rencontrer une erreur de module. `AppErrorBoundary` fournit un rechargement manuel : ce n'est pas systématiquement un écran blanc.

Le worker précharge seulement quatre URL, sans manifeste des chunks. Son fallback hors ligne peut servir le shell pour une ressource manquante. Son nom de cache est fixe dans le code ; une mise à jour de bundle ne garantit donc pas une nouvelle version de ce cache. En outre, l'enregistrement dans `main.jsx:71–79` est décidé au démarrage selon l'URL : une entrée dans Live par navigation SPA depuis l'accueil ne déclenche pas ce bloc avant un rechargement. Ne pas en déduire une indisponibilité universelle hors ligne : des assets déjà visités peuvent être en cache.

Correction : 404 pour ressources manquantes, conservation des assets N-1, préchargement/versionnement cohérent et gestion contrôlée des échecs d'import. [Vite documente le cas des anciens chunks supprimés lors d'un déploiement et `vite:preloadError`](https://vite.dev/guide/build.html#load-error-handling). Tester un onglet ouvert pendant une mise à jour, un formulaire non enregistré, puis le premier lancement hors ligne. Compensation : rechargement guidé sans boucle et conservation des anciennes ressources.

### F13 — Restauration partielle du carnet

L'import vérifie format/version/tableau, filtre certains éléments puis les enregistre avec `Promise.all`, chacun dans sa propre transaction. Les types de token/détail, la taille du fichier et les doublons ne sont pas complètement validés. La sonde remplace l'enregistrement par un succès puis un échec : un élément est écrit alors que l'import rejette globalement.

Correction : valider l'ensemble du document avant mutation, définir la politique de fusion/remplacement, puis utiliser une transaction unique. Afficher les éléments rejetés explicitement et protéger contre les fichiers excessivement volumineux. Les sauvegardes incluent les jetons et les détails du carnet en JSON ; cette portabilité est fonctionnelle, mais le fichier doit être présenté comme un moyen d'accès, pas comme un export anodin. La sauvegarde n'embarque pas le magasin `meta` : elle ne rétablit pas l'identité d'installation ni automatiquement ses abonnements. Compensation : conserver une sauvegarde avant fusion et tester le refus sans écriture. Ne pas conseiller un chiffrement local avec clé stockée à côté comme remède suffisant.

### F14 — Image d'accueil disproportionnée

`public/img/hero-commerce-v29.png` : **2 477 178 octets**, référencée par l'image de fond de `AccueilPage.jsx:812`. Aucune variante responsive n'est indiquée sur ce style. C'est une mesure de fichier et de code, pas une mesure de transfert réel avec CDN ou un résultat LCP.

Correction ciblée : produire une version WebP/AVIF aux dimensions nécessaires et mesurer visuellement, puis utiliser des variantes si la composition le justifie. La compression texte du serveur ne corrige pas le poids de ce PNG. Ne pas optimiser les trois autres grands PNG de parcours uniquement parce qu'ils sont présents dans `public` : leur chargement effectif n'a pas été établi ici. Compensation : cache CDN/HTTP et stratégie de dimensions adaptées ; le bénéfice prioritaire concerne une première visite à cache froid.

### F15 — Dépendance globale aux commerçants de la fiche

Après le détail coffret, `useQueries` lance une requête par identifiant commerçant distinct. Ces requêtes sont parallèles et disposent d'un cache de cinq minutes : ce sont des protections utiles. Toutefois le chargement global agrège chaque résultat : le rendu reste un skeleton tant qu'un commerçant charge. Une erreur marchande terminée affiche un bandeau mais ne masque pas le coffret à elle seule (`CoffretPage.jsx:497`). L'enjeu démontré est donc le délai du marchand le plus lent, aggravé par l'absence de deadline, pas un blocage définitif sur toute erreur marchande.

Pour N commerçants absents du cache, le code provoque N appels supplémentaires ; c'est un N+1 **HTTP frontend**, pas un N+1 SQL démontré. Correction : afficher le coffret disponible pendant le chargement des détails marchands, ou demander une projection publique agrégée. Définir explicitement si certains états marchands doivent bloquer l'achat pour raison métier. Compensation : parallélisation, cache existant, retry et rendu maintenu après erreur terminée. Valider avec un commerçant lent, un indisponible et un coffret à plusieurs partenaires ; mesurer le temps jusqu'au bouton d'achat utilisable.

### F16 — Tests visuels non entièrement isolés

Le serveur Playwright utilise par défaut une API de test distante, avec possibilité de remplacement par l'environnement, et réutilise un serveur existant. Les tests n'ont pas de refus réseau global et plusieurs parcours appellent réellement des fonctions susceptibles de créer une installation Live. Les tests de layout en développement ne valident pas non plus la CSP servie par Node.

C'est une configuration constatée, pas la preuve que la suite a modifié une donnée distante pendant cet audit : elle n'a pas été exécutée globalement. Correction : réseau refusé par défaut, fixtures complètes et profils séparés pour E2E simulé et intégration dédiée avec données jetables. Puis tests de production build/CSP/service worker. Compensation : ne pas lancer cette suite sur un serveur réutilisé de provenance inconnue. Les cinq tests serveur et les sondes fournies ont été exécutés localement.

## Observations supplémentaires et informations manquantes

| Sujet | État / preuve | Conséquence et suite recommandée |
|---|---|---|
| Compression HTTP | C, faible : `selectEncoding('br;q=0,gzip;q=1')` retourne `br` (`server.cjs:92–97`) | Ne respecte pas le refus explicite de Brotli. Parser les facteurs q ; ajouter test `q=0`, préférences et jokers. Effort 0,5 j, P3. |
| Configurations Git | C sur les noms uniquement : `.env.local`, `.env.production`, `.env.test` sont suivis malgré `.gitignore` | Ce n'est pas une preuve de secret commité : aucun contenu ni historique sensible consulté. Faire vérifier par l'exploitant, sortir les configurations privées du suivi après validation et ne conserver que des exemples. |
| Préfixe d'environnement | C, risque latent : `envPrefix: ['VITE_', 'LOCALEO_']`, `vite.config.mjs:38` | Un futur secret préfixé `LOCALEO_` pourrait être exposé s'il est consommé côté client. Préfixes publics explicites et contrôle CI de non-exposition ; aucun secret exposé démontré. |
| Ordre des `.env` | C : le générateur charge `.env.{mode}` avant `.env.local` (`write-app-config.cjs:46–50`) | Une valeur locale peut remplacer une valeur spécifique au mode. Alignement avec le chargeur Vite et tests à valeurs fictives. La configuration effective n'a pas été lue. |
| Redirection checkout pro | C : `CommandeProPage.jsx:203` affecte directement `res.checkout_url`, contrairement au contrôle de protocole du parcours particulier | Risque conditionnel si la réponse devient contrôlable ; aucune redirection exploitable par un utilisateur établie. Centraliser validation HTTPS/origines du prestataire, avec tests. |
| Stockage de données sensibles | C : brouillon pro, résumés d'achat et jetons en session/IndexedDB (`CommandeProPage.jsx:65–78`, `RetourPaiementPage.jsx:39–60`, `liveLibrary.js`) | Compromission de scripts même origine aurait un impact important. Définir minimisation, effacement, expiration et révocation ; éviter d'invalider sans remplacement le modèle de carnet hors ligne. Aucun contournement d'autorisation backend démontré. |
| Erreurs API | C : message/payload API repris par `api.js:204–211`, puis affichage direct dans plusieurs écrans Live/pro | Une erreur serveur détaillée pourrait être exposée. Le contenu réel des erreurs est inconnu. Généraliser les messages publics et conserver un identifiant de corrélation ; pas une XSS via texte JSX. |
| Authentification / IDOR / JWT / sessions | Information manquante côté serveur | Tester permissions par objet et tenant, portée des capacités, expiration, révocation et échange session paiement → gestion, avec comptes/ressources dédiés. Un préfixe `/protected/` dans une URL ne démontre ni protection ni défaut. |
| CSRF / CORS | Information manquante | Les appels sensibles inspectés utilisent surtout des en-têtes de capacité, sans `credentials: include`. Aucun CSRF déclaré sur cette seule base. Vérifier cookies réels et politique CORS côté API. |
| SQL/NoSQL, injections, SSRF, upload | Implémentation backend absente | Le serveur Node inspecté ne reçoit pas ces traitements. Aucune injection, SSRF ou traversée de répertoire exploitable démontrée. Vérifier backend, stockage des images et intégrations. |
| Chiffrement, rate limiting, anti-abus, audit métier | Configuration déployée absente | HTTPS de base API vérifié par code ; TLS réel, chiffrement BDD, quotas OTP/inscriptions/paiement et journalisation d'actions restent à auditer. |
| Sauvegardes BDD et continuité | Information manquante | L'export du carnet n'est pas une sauvegarde du système. Exiger RPO/RTO, restauration chronométrée, migrations réversibles et procédure de retour arrière. |
| CI/CD et conteneurs | Aucun workflow/conteneur identifié dans les fichiers inspectés ; processus externe possible | README recommande `npm install && npm run build`. Préférer `npm ci`, tests/revue avant déploiement, artefacts immuables et dépendances surveillées. Contrôles Render/GitHub réels à confirmer. |
| Documentation / dette | C : architecture annonce encore `HashRouter` (`frontend-architecture-marketplace.md:63,68,480`) ; code utilise `BrowserRouter` (`main.jsx:3,63`) | Risque concret de liens entrants et configuration d'hébergement erronés. Corriger ces informations avant de s'en servir pour une évolution ; pas de refonte générale recommandée. |
| Observabilité | Logs console et request_id visibles ; pas d'instrumentation p95/Web Vitals/erreurs distante identifiée dans `src` | Le monitoring peut exister à l'extérieur. Définir un collecteur d'erreurs expurgé, des métriques de parcours et alertes liées aux SLO avant optimisation plus large. |

### Performance : mesures disponibles et limites

Mesures en octets, gzip calculé avec Node local. **Artefacts `dist` déjà présents**, pas un nouveau build certifié des sources ni les tailles effectivement transférées en production.

| Ressource | Taille brute | Gzip local |
|---|---:|---:|
| Entrée JS `index-B6_p-s-y.js` | 262 838 | 81 699 |
| CSS global `index-BxcRl_CD.css` | 283 681 | 45 985 |
| Chunk Live `LiveApp-zPMReYYy.js` | 83 664 | 22 437 |
| CSS Live `live-BiFkx2mC.css` | 69 073 | 12 166 |
| Image principale accueil PNG | 2 477 178 | Non pertinent ici |

Le CSS global est chargé depuis `main.jsx`, y compris à l'entrée dans Live. Son volume justifie un profil de couverture CSS par page avant extraction ; il ne suffit pas à conclure à une lenteur perceptible. `LiveApp.jsx` concentre routage, persistance, préférences, notifications et composants : les problèmes d'identité et de cache ainsi que le formulaire historique encore présent démontrent un intérêt concret à mutualiser ces services, sans imposer une migration TypeScript ou des microservices.

La compression Brotli est recalculée à chaque réponse admissible (`server.cjs:138`). Un coût CPU sous fort trafic est plausible, mais n'a pas été mesuré : précompression/CDN à étudier seulement après mesure ou pour simplifier l'exploitation. Aucun résultat p50/p95/p99, débit, taux d'erreur réel, CPU/mémoire de production, fuite mémoire ou lenteur SQL n'est inventé. Les tests fonctionnels à très faible volume ne sont pas un benchmark.

Pour obtenir ces mesures : environnement dédié représentatif, données synthétiques, profil mobile/cache froid puis chaud, collecte des temps API et Web Vitals, corrélation frontend/API, métriques par route et dépendance. Tout test de charge distant nécessite un périmètre et une autorisation distincts.

## C. Plan d'action priorisé

### Immédiat — sous 48 heures

1. Frontend + exploitation : neutraliser le passage de capacités à Analytics (F01), vérifier les émissions automatiques et décider si un examen des données historiques est nécessaire. Critère : aucune capacité fictive dans les sorties du collecteur simulé sur tous les chemins sensibles.
2. Frontend : fermer le contournement SVG (F02) et retirer le diagnostic QR public (F04). Exploitation : confirmer la CSP sur l'origine finale. Critère : charge malveillante inerte même sans CSP ; QR valide toujours imprimable.
3. QA : rendre l'exécution réseau des tests explicite (F16) avant toute automatisation ; maintenir des mocks pour les créations/achats. Critère : aucun appel externe inattendu.
4. Backend + exploitation : préparer F03, identifier le format de transition et la politique de journaux. Révocation/purge uniquement si l'examen révèle une exposition nécessitant ces actions.

Corrections rapides à fort bénéfice : exclusion Analytics des routes sensibles, retrait token/payload QR, image d'accueil optimisée, promesse d'installation partagée dans un onglet, garde de contexte sur pagination. Le verrou multi-onglets et la migration API demandent un travail supplémentaire.

### Court terme — sous 30 jours

- F03/F05/F06 : contrat JSON, retrait effectif du consentement, cache PWA restreint et migration de ses anciennes entrées.
- F07/F09/F10 : identité unique, isolation des résultats par commune, délais et états de résultat incertain ; vérifier l'idempotence du parcours actif avec le backend.
- F11/F12/F13 : erreurs serveur confinées, mise à jour N/N-1, restauration du carnet atomique.
- F14/F15 : réduire l'image et isoler les dépendances marchandes, puis mesurer le gain sur un parcours réaliste.
- Mettre les sondes transformées en tests de non-régression dans une suite isolée ; contrôler le build de production, les en-têtes et l'entrée SPA vers Live.

### Moyen terme — sous 90 jours

- Audit backend avec matrice de droits, deux tenants/comptes de test et vérifications d'objets/capacités, sans données réelles.
- Vérification des signatures de webhooks, de l'unicité/idempotence, des montants, transactions et états de paiement.
- Revue de CORS, quotas, expiration/révocation, configuration hébergement, backups/migrations/rollback et isolation des environnements.
- Revue de conformité avec le responsable des traitements : finalités, minimisation, durées, exercice des droits, sous-traitants et preuves de consentement.
- Définition de SLO et instrumentation des erreurs/performances ; budgets d'assets fondés sur mesures, documentation technique actualisée et retrait du formulaire historique F08.

### Amélioration continue

Audits de dépendances réguliers, installations reproductibles, tests d'incidents et de restauration, parcours synthétiques non destructifs, revue des changements de tags Analytics, contrôle des assets et de la compatibilité de versions. Mettre à jour les constats avec preuve de correction et version livrée ; ne pas se limiter à un statut documentaire « corrigé ».

## D. Correctifs proposés — à valider avant application

Ces extraits illustrent des changements ciblés. Ils ne sont ni appliqués ni validés comme un patch complet ; ils doivent être adaptés au contrat et au navigateur cible.

### 1. Routes Analytics autorisées — F01

```js
const TRACKED_ROUTES = new Map([
  ['/accueil', 'accueil'],
  ['/city', 'commune'],
  ['/coffrets', 'catalogue_coffrets'],
  ['/coffret', 'fiche_coffret'],
  ['/animations', 'catalogue_animations']
]);

function publicPageContext(pathname) {
  const route = TRACKED_ROUTES.get(pathname);
  return route ? { page_path: pathname, page_title: route } : null;
}
// Déterminer ce contexte AVANT d'initialiser le tag.
// Compléter par le blocage des mesures automatiques lors des routes exclues.
```

Effet secondaire : baisse volontaire du nombre de pages mesurées ; les indicateurs de conversion doivent utiliser des événements métier sans capacités. Validation : navigation directe et SPA avec consentement absent/accepté/retiré, liens courts/feedback/participant, collecteur fictif et sentinelles. Contrôler les événements automatiques après chargement préalable du tag.

### 2. QR sous forme d'image passive ou SVG restreint — F02/F04

```jsx
// Contrat cible : image issue du service QR, pas HTML actif inséré dans le DOM.
<img src={qrImageDataUri} alt="QR code de votre coffret" />
```

Si l'insertion SVG est indispensable, utiliser un assainisseur maintenu avec liste positive de tags et attributs nécessaires au générateur QR. Ne pas se contenter d'ajouter `animate` à une liste noire. Effets secondaires : texte/logo/style SVG éventuellement supprimés ; tester lisibilité au scanner, impression et zoom. Non-régression : SVG standard, SVG malformé, liens/animations/événements/scripts, sans puis avec CSP. Le marqueur de la sonde doit rester inactif dans les deux cas.

### 3. Initialisation JSON et reprise — F03/F10

```js
// À utiliser seulement lorsque l'API accepte le nouveau corps JSON.
return postJson('/public/gestion-achats/paiements/initialiser', {
  coffret_id: coffretId,
  email_client: email,
  telephone_client: telephone,
  type_client: typeClient,
  quantite
}, { headers: { 'Idempotency-Key': operationKey }, signal });
```

La clé reste attachée à la même intention en cas de réponse perdue. Une modification significative du panier/formulaire exige une politique explicite pour créer une nouvelle intention sans dupliquer l'ancienne. Effet secondaire : migration backend indispensable, y compris B2B/crédit. Validation : réponse perdue après commit, double clic, retry, retour après rechargement, erreur de validation et panier modifié ; résultat unique vérifiable côté serveur.

```js
async function fetchWithDeadline(url, options = {}, timeoutMs = 15_000) {
  const controller = new AbortController();
  const cancel = () => controller.abort();
  if (options.signal?.aborted) cancel();
  else options.signal?.addEventListener('abort', cancel, { once: true });
  const timer = setTimeout(cancel, timeoutMs);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    return await parseResponse(response); // le délai couvre aussi le corps
  } finally {
    clearTimeout(timer);
    options.signal?.removeEventListener('abort', cancel);
  }
}
```

15 s est un exemple à adapter, pas une mesure ni un SLO proposé sans contexte. Les téléchargements demandent une politique propre. Une annulation d'écriture doit mener à « résultat à vérifier », avec même clé lors de reprise, pas à une conclusion d'échec définitif.

### 4. Déduplication de l'installation — F07

```js
let installationInFlight = null;

export function ensureLiveInstallation(options) {
  if (!installationInFlight) {
    installationInFlight = loadOrCreateInstallation(options)
      .finally(() => { installationInFlight = null; });
  }
  return installationInFlight;
}
```

`loadOrCreateInstallation` encapsule la lecture, création et persistance actuelles. Cette correction couvre un contexte JavaScript ; plusieurs onglets exigent une coordination supplémentaire. Ne pas perdre les préférences de commune des appels concurrents : les appliquer après résolution de l'identité. Tests : deux appels identiques simultanés, deux onglets, échec de création/écriture, réessai après échec, options de commune différentes.

### 5. Cache limité aux ressources publiques — F06

```js
function mayCache(request, response) {
  const url = new URL(request.url);
  const staticPath = url.pathname.startsWith('/assets/') ||
    ['/live/', '/live/manifest.webmanifest',
      '/icons/localeo-live-icon.png',
      '/icons/localeo-live-favicon-64.png'].includes(url.pathname);
  return request.method === 'GET' && url.origin === self.location.origin &&
    !url.search && staticPath && response.ok &&
    !request.headers.has('Authorization') &&
    !request.headers.has('X-Localeo-Live-Secret') &&
    !/no-store|private/i.test(response.headers.get('Cache-Control') || '');
}
```

Prévoir séparément un shell hors ligne explicitement public : le serveur actuel sert le HTML avec `no-store`, donc cet exemple strict ne le mettrait pas en cache. Effet secondaire : parcours hors ligne à redéfinir avant livraison. Tests : caches avec jetons anciens, API même origine, réponse privée, erreur/quota, mise à jour et configuration runtime. Attendre l'écriture via `event.waitUntil` et traiter son rejet.

### 6. Serveur et versions — F11/F12

```js
const { pipeline } = require('node:stream');
// Après ouverture contrôlée du fichier et choix éventuel du compresseur :
pipeline(fileStream, response, error => {
  if (error) {
    // Journal technique expurgé avec identifiant de requête.
    // Ne pas réécrire des en-têtes déjà envoyés.
  }
});
// Route absente dans /assets/ : 404 explicite, jamais index.html.
```

Ajouter le compresseur dans la chaîne si nécessaire. Entourer séparément les opérations filesystem ; ne pas « corriger » avec un simple `uncaughtException` global qui laisserait le processus dans un état indéfini. Tests : EACCES/ENOENT simulés, suppression entre ouverture et lecture, client déconnecté, HEAD, 304, compression et ancien chunk après déploiement. Compensation de version : conserver N-1 et proposer une reprise compatible avec les formulaires non sauvegardés.

Pour F09/F13/F15/F16 : convertir les scénarios décrits dans chaque constat en tests isolés avant implémentation — réponse ancienne ignorée, import invalide sans aucune écriture, fiche accessible avec un commerçant indisponible, échec systématique de tout appel réseau inattendu.

## E. Niveau de confiance et preuves d'exécution

**Confiance élevée** dans les comportements reproduits par les sondes locales et dans les lignes de code citées. **Confiance moyenne** dans leurs conséquences métier, conditionnées par backend/configuration. **Information manquante** pour sécurité et charge de production, droits multi-tenant, exploitation de secrets, conformité globale et continuité d'activité.

| Vérification | Résultat observé | Limite |
|---|---|---|
| `npm.cmd run lint` | Succès, zéro erreur | Pas une preuve de correction métier ou de sécurité |
| `npm.cmd run test:server` | 5/5 réussis | Serveur local sur artefacts existants ; pas l'API métier |
| `npm.cmd audit --json --ignore-scripts` | 0 vulnérabilité signalée, 128 dépendances comptées au total par npm | Avis connus du registre au moment du contrôle ; ne couvre pas le code maison ni un runtime déployé différent |
| `node docs/audits/probes-audit-2026-09-05.cjs` | Succès ; reproductions Analytics, query checkout, installation, idempotence, cache, pagination, import et serveur | API/stockages simulés ; aucune écriture métier ni tentative d'exploitation distante |
| `node docs/audits/probe-svg-2026-09-05.cjs` | Marqueur exécuté sans CSP, bloqué avec la politique de scripts du serveur | Page Chromium vierge, tout accès réseau interdit, SVG fictif |
| Taille des fichiers et gzip Node | Mesures consignées ci-dessus | `dist` préexistant, pas un build neuf ni un transfert production |
| Suite visuelle complète / charge / pentest | Non exécutés | Couplage distant décrit en F16 ; aucun accord pour charge/intrusion production |

Le premier appel npm audit a échoué en accès réseau restreint. Après autorisation d'accès au registre, la commande a réussi sans installation ni modification de dépendances. Selon [la documentation npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit/), le contrôle interroge les avis du registre sur l'arbre des dépendances ; « zéro avis » n'est pas une attestation d'absence de vulnérabilité.

Les scripts de diagnostic **affirment volontairement le comportement défectueux observé** : ils ne doivent pas être intégrés tels quels comme tests de succès après correction. Ils sont fournis pour reproduire l'état audité ; inverser/adapter leurs assertions lors de leur transformation en tests de non-régression.

Autres commandes de lecture utilisées : `rg --files`, recherches `rg -n` ciblées, `Get-Content` sur sources/documents non secrets, `git status --short`, `git ls-files '.env*'` (noms seulement), `git rev-parse --short HEAD`, inventaire des tailles de fichiers, extraction des seuls noms/emplacements des paramètres checkout depuis OpenAPI. Runtime local constaté : Node `v24.14.0`, npm `11.9.0`. Aucun build supplémentaire ni script de génération de configuration exécuté pendant cet audit.

### Vérifications nécessaires pour lever les incertitudes

1. Quelle révision et quelle configuration de domaines/API sont réellement en production et préproduction ? Le serveur Node fourni et sa CSP sont-ils effectivement utilisés, ou un hébergeur statique/CDN les remplace-t-il ?
2. Analytics est-il activé en production, avec quelles mesures automatiques, rétentions et personnes habilitées ? Faire rechercher par l'exploitant des chemins sensibles dans un résultat expurgé, sans transmettre les jetons.
3. Le SVG QR est-il exclusivement généré à partir de primitives fixes côté serveur ? Une donnée d'organisateur/commerçant peut-elle influencer son markup ?
4. Les jetons de gestion/consultation/participation sont-ils bornés, révocables et attachés à une ressource/tenant ? Quelles vérifications protègent l'échange depuis une session de paiement ?
5. Quelles garanties d'idempotence/unicité existent pour inscriptions, installations, checkout, activation et demandes de facture ? Peut-on récupérer un résultat après perte de réponse ?
6. Quels volumes, pics, délais attendus et SLO guident les mesures ? Quels exports expurgés de latence/erreurs/ressources sont disponibles ?
7. Quelles preuves de restauration, objectifs RPO/RTO, migrations et procédures de retour arrière existent ?
8. Qui valide finalités, rétentions, consentement, suppression/export et sous-traitants des données personnelles ?

Ces réponses complèteront l'audit système. Elles ne sont pas nécessaires pour valider puis traiter les défauts frontend déjà reproduits.
