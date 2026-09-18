# F14 — Bearer accessible au JavaScript dans sessionStorage

## Protection appliquée

Le frontend retire la session du stockage et de la mémoire à l'échéance `expires_at`, même sans navigation, et invalide le cache Animation. Le retour au premier plan vérifie aussi cette échéance après une suspension des timers du navigateur. Une échéance renouvelée par le serveur remplace le timer précédent. Une session expirée ou illisible n'est pas restaurée.

La durée de session reste décidée par le backend (`COMMERCANT_SESSION_TTL_SECONDS`). Le backend conserve les contrôles de révocation, d'expiration et de scope à chaque accès protégé. Le timer frontend ne remplace aucun de ces contrôles. La déconnexion immédiate et les protections CSP font l'objet de F02 et F12.

Validation : `src/app/useMerchantSession.test.jsx`, tests d'indisponibilité de session et de déconnexion ; suite navigateur avec CSP.

## Limite résiduelle et évolution HttpOnly

Le contrat actuel exige un Bearer explicite et la PWA statique restaure une session après rechargement. Le correctif réduit sa persistance au-delà de sa validité, mais ne rend pas le Bearer inaccessible à un script malveillant pendant une session valide. F14 reste un risque résiduel identifié, sans XSS démontrée.

Un cookie HttpOnly nécessite une évolution coordonnée de l'hébergement et du backend, pas une option de `sessionStorage`. La cible à instruire est un intermédiaire de même origine qui conserve le Bearer côté serveur et remet au navigateur un identifiant de session opaque dans un cookie `Secure`, `HttpOnly`, avec une politique SameSite adaptée. Il doit vérifier l'origine et protéger les mutations contre CSRF, propager révocation/expiration, et ne jamais remettre le Bearer dans les réponses publiques.

Avant migration : valider les domaines d'hébergement, les liens entrants, l'authentification des autres clients de l'API, les parcours de rechargement, les refus CSRF et l'isolation entre deux commerçants. Déployer le backend/intermédiaire avant le frontend, avec un mécanisme de retour arrière défini. Aucun changement de cookie ni promesse d'immunité XSS n'est introduit par ce correctif.
