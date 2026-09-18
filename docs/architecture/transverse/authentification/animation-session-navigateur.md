# Session navigateur Localeo Animation

Le frontend statique appelle directement le backend configuré dans VITE_API_URL,
avec credentials: include. Aucune passerelle /api ni changement de domaine/DNS.
Les deux origines doivent être HTTPS et appartenir au même site, par exemple
test-animation.localeo.city et test-backoffice.localeo.city. Les sites tiers
ne sont pas supportés par ce transport SameSite=Lax.

Le frontend envoie X-Animation-Session: cookie. Le serveur vérifie l'origine et
dépose __Host-localeo_animation (HttpOnly, Secure, SameSite=Lax, Path=/, sans
Domain) sur son propre hôte. Le JSON contient uniquement l'identité, l'échéance
et un HMAC CSRF lié au jeton. Aucun jeton d'authentification dans Web Storage.

GET /protected/identite-acces/animation/sessions/me recontrôle la session,
l'expiration, la révocation, le gestionnaire, le partenaire et les habilitations.
La durée absolue n'est pas renouvelée : LOCALEO_ANIMATION_SESSION_TTL_SECONDS,
8 heures par défaut. Toute écriture par cookie exige l'origine exacte autorisée
et X-Animation-CSRF. La connexion exige l'origine autorisée. La déconnexion
révoque le jeton puis supprime le cookie, y compris si la session a expiré.

## CORS limité au portail

AnimationBrowserMiddleware s'exécute avant les middlewares de session et de
CSRF administrateur. Il traite uniquement le protocole X-Animation-Session:
cookie et les prévols OPTIONS qui demandent cet en-tête. Les routes autorisées
sont celles du portail Animation, les sessions et les routes publiques qu'il
utilise ; ce protocole ne permet pas d'atteindre /admin, /internal ou une autre
API protégée. Les clients sans ce protocole gardent leur politique existante.

Les prévols autorisent uniquement les origines exactes déclarées, les méthodes
utilisées et Content-Type, X-Animation-Session, X-Animation-CSRF, Idempotency-Key.
Les réponses exposent Content-Disposition, X-Correlation-ID et X-Request-ID.
Les requêtes same-site restent soumises à l'origine exacte ; un sous-domaine
voisin non déclaré ne suffit pas. Les requêtes cross-site sont refusées.

Les cookies autres que le cookie Animation sont retirés du scope ASGI avant
le décodage de la session administrateur. Les Set-Cookie autres qu'Animation
sont filtrés sur ces réponses. Une session BackOffice ouverte sur le même hôte
ne bloque donc pas les écritures Animation, ne les authentifie pas et n'est
pas modifiée par elles. Les contrôles CSRF du BackOffice restent inchangés.
Les réponses API du protocole sont Cache-Control: no-store et varient selon
l'origine. Ne pas activer CORS_ALLOW_CREDENTIALS globalement.

## Configuration et déploiement

Déployer d'abord ce backend, puis reconstruire le frontend statique.
LOCALEO_ANIMATION_PORTAIL_URL fournit par défaut la seule origine autorisée.
LOCALEO_ANIMATION_BROWSER_ORIGINS, si définie, remplace cette liste : origines
HTTPS séparées par des virgules, sans chemin, slash final ni joker. Une liste
invalide ferme l'accès. Garder test et production séparés.

Pour le test, vérifier LOCALEO_ANIMATION_PORTAIL_URL=https://test-animation.localeo.city.
Si LOCALEO_ANIMATION_BROWSER_ORIGINS existe, elle doit contenir cette même
origine exacte. Le frontend conserve VITE_API_URL=https://test-backoffice.localeo.city.
Le CORS global et l'hébergement statique restent inchangés. Aucune migration SQL.

En dev, utiliser le même hôte localhost ou 127.0.0.1 sur deux ports et déclarer
l'origine de Vite. HTTP local n'est permis qu'en mode dev ; les attributs de
sécurité du cookie restent actifs grâce à l'exception localhost du navigateur.

Sans X-Animation-Session: cookie, les clients API conservent le transport Bearer.
Un Authorization malformé ne déclenche jamais de repli sur le cookie.

## Recette

Les tests de tests/security/test_animation_browser_session.py couvrent les deux
origines, prévols, requêtes réelles, CSRF, cookies administrateur, révocation,
expiration et habilitations. Les tests CSRF et d'authentification existants
restent applicables. Le frontend fournit un parcours Chrome entre deux ports,
sans proxy. Compléter par la recette HTTPS déployée : connexion, rechargement,
nouvel onglet, écriture, déconnexion et refus du jeton révoqué.
