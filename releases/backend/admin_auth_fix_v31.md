# Localeo V31 - Correctif authentification SQLAdmin

## Correctifs appliqués
- chargement du `.env` via `python-dotenv`
- `AdminAuthBackend(secret_key=ADMIN_SESSION_SECRET)`
- suppression du `SessionMiddleware` manuel dans `main.py`
- session gérée uniquement par l'auth backend SQLAdmin

## Symptôme corrigé
- `POST /admin/login` retournait `200`
- mais l'écran restait sur la page de login

## Variables requises
```env
LOCALEO_ADMIN_USERNAME=admin
LOCALEO_ADMIN_PASSWORD=change-me
LOCALEO_ADMIN_SESSION_SECRET=change-me-admin-secret
```
