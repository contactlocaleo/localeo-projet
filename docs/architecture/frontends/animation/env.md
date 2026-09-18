Variables d'environnement
=========================

Ce document liste les variables d'environnement utilisées par l'application et leur but.

- `VITE_API_URL` (requis en prod) : URL publique du backend (ex: `https://api.localeo.example`).
  - Utilisation : toutes les requêtes HTTP côté client doivent utiliser cette base.

- `VITE_MOCK` (optionnel) : `true` ou `false`. Lorsque `true`, l'application utilise les mocks locaux (utile en dev).

- `VITE_SENTRY_DSN` (optionnel) : DSN Sentry pour la capture d'erreurs en production.

Bonnes pratiques
- Ne mettez pas de secrets non chiffrés dans le dépôt. Utilisez le système de variables d'environnement de Render pour la production.
- Préférez `import.meta.env.VITE_*` pour lire les variables dans le code.
- Fournissez un fichier `.env.example` (fourni) et ne commitez jamais `.env`.

Exemple local (PowerShell)
```powershell
# create local .env from example
copy .env.example .env
# then edit .env to override values locally
```
