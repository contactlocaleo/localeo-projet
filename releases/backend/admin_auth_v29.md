# Localeo V29 - Authentification du back-office

Le back-office SQLAdmin sur `/admin` est maintenant protégé par une authentification simple basée sur session.

## Variables d'environnement
```env
LOCALEO_ADMIN_USERNAME=admin
LOCALEO_ADMIN_PASSWORD=change-me
LOCALEO_ADMIN_SESSION_SECRET=change-me-admin-secret
```

## Fonctionnement
- accès à `/admin`
- formulaire de login SQLAdmin
- authentification via username / password
- session Starlette

## Fichiers ajoutés
- `app/infrastructure/admin/auth.py`
- mise à jour de `app/infrastructure/admin/admin.py`
- mise à jour de `app/main.py`
