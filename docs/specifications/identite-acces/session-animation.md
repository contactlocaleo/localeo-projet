# Authentification et session navigateur — Localeo Animation

> Référence documentaire consolidée depuis `docs/session-navigateur.md` et
> l'ancien `docs/roadmap/auth.md` de Localeo Animation. Le transport navigateur
> courant est le cookie HttpOnly, confirmé par la lecture du frontend et du backend.
> Les anciennes instructions Bearer en mémoire sont historiques, décrites à la fin
> de ce document ; elles ne constituent pas une seconde règle active du portail.
> La réorganisation documentaire n'introduit ni nouveau transport ni décision produit.

## Contrat navigateur courant

La connexion appelle `POST /public/identite-acces/animation/sessions` avec
`email` et `mot_de_passe`. Le client du portail annonce explicitement le transport
par l'en-tête `X-Animation-Session: cookie`, également envoyé lors des lectures
et écritures protégées du portail. Les écritures authentifiées ajoutent
`X-Animation-CSRF` ; le jeton d'authentification reste inaccessible au JavaScript.

La connexion crée une session serveur dont seul le condensat du jeton est stocké
en base. Le navigateur reçoit le jeton dans le cookie
`__Host-localeo_animation`, `HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`, sans
attribut `Domain`. Aucun jeton d’authentification n’est renvoyé en JSON ni écrit
dans localStorage ou sessionStorage.

À chaque démarrage, `GET /protected/identite-acces/animation/sessions/me`
vérifie la session avant de monter les vues privées. Le serveur contrôle
l’expiration, la révocation, l’état du gestionnaire et du partenaire ainsi que
ses habilitations. L’identité et une valeur CSRF liée à la session restent en
mémoire. Une erreur réseau propose de réessayer ; une réponse 401 présente la
connexion. L’URL courante est conservée.

La durée absolue existante n’est pas prolongée :
`LOCALEO_ANIMATION_SESSION_TTL_SECONDS`, 8 heures par défaut. Le cookie reprend
cette durée ; le serveur reste l’autorité sur l’échéance. Le rechargement ne crée
ni session ni cookie nouveau.
Les sessions Bearer existantes restent utilisables par les autres clients API.

Pour les appels de session du portail, le frontend statique appelle directement
`VITE_API_URL` avec `credentials: include`. Les lectures explicitement anonymes
omettent les credentials et les en-têtes de session. Le cookie reste limité à l'hôte du backend : il n'est
pas partagé via un attribut Domain. Les domaines du frontend et du backend
doivent être HTTPS et appartenir au même site (par exemple deux sous-domaines
de localeo.city), ce qui permet de conserver SameSite=Lax sans cookie tiers.

Le backend autorise les requêtes CORS avec cookies uniquement sur les routes
du portail et pour les origines exactes configurées. Les prévols OPTIONS
autorisent les méthodes et en-têtes utilisés, dont Idempotency-Key. Les réponses
exposent les identifiants de corrélation et Content-Disposition.
Les écritures par cookie exigent une origine autorisée et X-Animation-CSRF.
Un sous-domaine voisin non déclaré reste refusé, même en same-site. Les appels
cross-site sont refusés. Aucune donnée de session n'est mise en cache.

Le middleware Animation retire les autres cookies avant les middlewares de
session/CSRF administrateur et filtre les Set-Cookie de la réponse. Il protège
ainsi la session BackOffice ouverte sur le même hôte ; les protections des
routes administrateur restent actives. Le service worker ne cache que les
ressources publiques du frontend.

La déconnexion révoque la session en base puis supprime le cookie. Une session
déjà expirée ou révoquée peut également être supprimée. Si le réseau échoue,
l’application bloque les vues privées et propose de réessayer. Seul le marqueur
non sensible `localeo_logout_pending=1` est conservé dans sessionStorage pour
reprendre cette opération après un rechargement du même onglet. Il est supprimé
après confirmation serveur. Ce marqueur ne donne aucun droit d’accès.

## Droits, commune et continuité du parcours

Ces exigences déjà présentes dans l'ancien document ANIM-012/014 restent applicables :

- le client ne déduit aucun droit d'un jeton opaque ; le serveur vérifie la session,
  les droits et la commune à chaque appel ;
- la commune active est choisie parmi les habilitations renvoyées par le serveur ;
- l'expiration est surveillée par minuterie, au retour sur l'onglet et sur réponse 401 ;
- après reconnexion, la route interne demandée est conservée ;
- le retour Stripe n'établit jamais à lui seul que la commande est payée ;
- expiration, rôle révoqué, déconnexion avec réseau coupé, changement de commune
  et réponse HTTP retardée font partie de la recette ;
- les méthodes et en-têtes réellement utilisés sont vérifiés par les prévols CORS,
  ainsi que le refus d'une origine non autorisée.

L'ancien principe d'effacement local immédiat lors de la déconnexion se retrouve
dans le blocage immédiat des vues privées et la purge de la session en mémoire.
Il ne dispense pas de confirmer la révocation serveur : l'état de reprise de
déconnexion décrit ci-dessus est conservé en cas d'échec réseau.

Le [guide de formation Animation](../../produit/formation/animation/guide-animation-preproduction.md)
décrit les gestes utilisateur. Si un passage historique de ce guide décrit encore
le transport Bearer, le contrat navigateur courant du présent document prévaut.

## Déploiement

1. Déployer le backend avec AnimationBrowserMiddleware, avant le frontend.
2. Vérifier LOCALEO_ANIMATION_PORTAIL_URL. Son origine exacte est autorisée par
   défaut. Si LOCALEO_ANIMATION_BROWSER_ORIGINS existe, elle remplace cette liste :
   origines HTTPS séparées par des virgules, sans chemin, slash final ni joker.
   Garder des listes distinctes pour test et production.
3. Conserver le site statique Render, son domaine et son DNS. Les variables
   VITE_API_URL et LOCALEO_EXPECTED_API_ORIGIN doivent contenir l'origine HTTPS
   du backend ; LOCALEO_DEPLOY_TARGET vaut staging, demo ou production. Reconstruire
   et publier dist. Aucune passerelle /api n'est nécessaire.
4. Vérifier les prévols OPTIONS et les appels directs dans le navigateur :
   connexion, rechargement d'une fiche, nouvel onglet, déconnexion et rechargement.
   GET /protected/identite-acces/animation/sessions/me renvoie du JSON :
   401 sans session et 200 avec une session valide. Le cookie est HttpOnly,
   Secure, SameSite=Lax, sans Domain, sur l'hôte du backend.

Ne pas activer CORS_ALLOW_CREDENTIALS globalement. Aucune migration SQL.
Les autres clients conservent leur transport Bearer et leur politique CORS.

En développement, utiliser un backend local et configurer son origine dans
VITE_API_URL ; déclarer l'origine exacte de Vite côté backend en mode dev.
Utiliser le même nom d'hôte (localhost ou 127.0.0.1), avec deux ports différents.
Les cookies Secure restent actifs et reposent sur l'exception localhost du
navigateur. Un frontend local appelant le backend distant est cross-site et
ne constitue pas la configuration supportée pour ce cookie SameSite=Lax.

## Vérifications automatisées

- Backend : tests/security/test_animation_browser_session.py couvre les deux
  origines, CORS et ses prévols, CSRF, isolation des cookies administrateur,
  refus des autres namespaces, expiration, révocation et habilitations.
- Frontend : tests/browser-session.test.mjs, tests/auth-memory.test.mjs,
  tests/session-expiry.test.mjs et tests/logout-endpoint.test.mjs.
- Navigateur : node tests/browser/session-refresh.mjs démarre Vite sur 5174
  et une API synthétique sur un autre port, sans proxy. Il vérifie les vrais
  prévols CORS, le cookie HttpOnly, le rechargement, les onglets, les erreurs
  réseau, la reprise de déconnexion et l'absence de secrets dans Web Storage.
  Playwright utilise l'installation isolée dans tmp/mobile-qa. Cette recette
  locale complète les tests serveur sans remplacer la vérification déployée.


## Ancien transport ANIM-012/014 — historique, non applicable au portail courant

Le document `docs/roadmap/auth.md` décrivait un état antérieur du frontend.
Les différences ci-dessous sont conservées pour comprendre l'évolution, sans
maintenir deux contrats concurrents pour le navigateur.

| Sujet | Ancienne règle du portail | Contrat navigateur courant |
| --- | --- | --- |
| Réponse de connexion | Jeton opaque et expiration dans le JSON ; jeton uniquement en mémoire. | Identité, expiration et valeur CSRF en JSON ; authentification dans le cookie HttpOnly. |
| Requêtes protégées | `Authorization: Bearer …` et `credentials: 'same-origin'`. | `X-Animation-Session: cookie`, `credentials: 'include'`, `cache: 'no-store'` ; CSRF pour les écritures. |
| Isolation BackOffice | Aucun cookie BackOffice envoyé à l'API cross-origin. | Le navigateur peut transmettre les cookies de l'hôte backend ; le middleware Animation retire les autres cookies avant traitement et filtre les `Set-Cookie` de réponse. |
| CORS | Origine exacte, méthodes utilisées, `Authorization`, `Content-Type`, `Idempotency-Key` ; pas de généralisation de `credentials: include`. | Politique avec cookies limitée aux routes et origines Animation, avec `Content-Type`, `X-Animation-Session`, `X-Animation-CSRF`, `Idempotency-Key`. Aucune activation globale de CORS avec cookies. |
| Rechargement | Le jeton en mémoire n'était pas persisté. | Le cookie permet la restauration explicite par `/sessions/me` ; aucun secret d'authentification dans Web Storage. |

Les sessions Bearer sont toujours disponibles pour les autres clients API, selon
leur contrat propre. Cette compatibilité ne signifie pas que le portail utilise
les deux transports ou doive réintroduire un jeton dans son stockage JavaScript.

## Éléments vérifiés lors de la consolidation

La lecture de l'implémentation a confirmé les éléments suivants :

- [Client HTTP Animation](../../../../localeo-animation/src/app/httpClient.ts) : transport
  cookie, absence d'Authorization automatique, CSRF sur écritures et cache désactivé.
- [API frontend](../../../../localeo-animation/src/app/api.ts) et
  [état de session](../../../../localeo-animation/src/app/auth.ts) : identité et CSRF seulement,
  restauration par `/sessions/me`, reprise de déconnexion et suppression du stockage historique.
- [API backend](../../../../localeo-backend/app/api/animation_locale_api.py) : sélection du
  transport cookie, réponse sans jeton d'authentification dans ce mode, lecture et révocation.
- [Cookie et CSRF](../../../../localeo-backend/app/security/animation_cookie.py) : cookie
  `__Host-`, `Secure`, `HttpOnly`, `SameSite=Lax`, origine autorisée et vérification CSRF.
- [Middleware Animation](../../../../localeo-backend/app/security/animation_browser.py) :
  périmètre de routes, CORS dédié et isolation des cookies administrateur.
- [Service de session](../../../../localeo-backend/app/application/identite_acces/services/service_session_animation.py) :
  seul le condensat SHA-256 du jeton est conservé dans la session persistée.

Ces constats portent sur le code du workspace. Ils ne prouvent pas que la même
révision ou configuration est déployée dans un environnement distant.

Les cinq fichiers de tests frontend cités ci-dessous ont été exécutés lors de
la consolidation : **12 tests réussis**, sans appel à un environnement distant.

```sh
node --test tests/browser-session.test.mjs tests/auth-memory.test.mjs tests/session-expiry.test.mjs tests/logout-endpoint.test.mjs tests/http-client-credentials.test.mjs
```

Ils vérifient notamment la restauration d'identité, le retrait du Bearer lors du
passage en mode cookie, CSRF, l'absence de secrets persistés, les lectures anonymes,
la séparation des requêtes anonymes et authentifiées, l'expiration et la déconnexion.
Les tests backend et la recette navigateur intégrée décrits plus haut n'ont pas été
réexécutés dans cette passe documentaire.
