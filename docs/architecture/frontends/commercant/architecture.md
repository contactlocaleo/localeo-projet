# Architecture actuelle — application Commerçants

Révision : 7 septembre 2026, remédiation PRO-001 à PRO-012.

## Modules et transport

React, React Router et Vite. `src/App.jsx` contient le shell, l’authentification et le menu. `src/ActionWorkspaces.jsx` charge les parcours historiques (validation, profil, prestations, reversements, support) à la demande ; `src/appSupport.jsx` partage leurs helpers et appels API. `src/app/` porte session, navigation et frontières d'erreur. Animation, Finance, dashboard et Stripe Connect résident dans `src/features/`. Styles et polices sont locaux ; les pages modulaires sont chargées à la demande.

`src/lib/api/` partage les URLs, le Bearer, les erreurs et le transport. Le délai de 15 secondes couvre requête et corps, sans retry automatique de mutation. 401 expire la session ; 403 reste un refus distinct.

## Session et cache

Le Bearer est dans sessionStorage, jamais dans une URL. Le backend vérifie session, scope et propriété de chaque ressource. La déconnexion efface immédiatement l'état local avant révocation réseau ; expiration par temporisation et retour de focus. Le cache Animation est uniquement mémoire, borné et séparé par époque de session. Les lectures et mutations tardives de l'ancien compte sont rejetées.

## Validation

QR coffret et participant sont résolus côté serveur à partir d'un corps JSON. La résolution Animation est authentifiée et expose seulement la référence participant et l'étape propre au commerce. La commande conserve tous ses contrôles backend et son atomicité ; le verrou local n'est qu'une protection d'interface.

Un conflit ou ANOMALIE n'est pas un succès. Une commande confirmée reste distincte d'une relecture échouée. Dans ce cas les actions coffret sont bloquées jusqu'à réconciliation. Une transaction consommée exige un nouveau scan pour une autre prestation. La reprise stocke seulement identifiants, propriétaire et expiration, sans QR ni Bearer supplémentaire ; un refresh relit le serveur sans rejouer de commande.

Les invitations conservent la clé d'une décision incertaine. Un enrichissement tardif ne remplace pas une décision. Une action refusée par le serveur reste interdite. Les listes paginées refusent d'afficher une réponse incomplète comme complète.

## Livraison

Le build refuse les cibles API/QR non conformes à la production connue. Les flags Finance restent explicitement désactivés avant recette produit. Le service worker gère les notifications sans cache API hors ligne. Les conditions d'exploitation ne sont pas prouvées par les seuls tests locaux : voir le [registre](../../../audits/commercant/remediation-preproduction-2026-09-06.md) et la [procédure](../../../exploitation/commercant/mise-en-production.md).
