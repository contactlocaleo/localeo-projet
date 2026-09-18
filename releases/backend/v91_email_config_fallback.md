# Localeo V91 - Fallback configuration email

## Objectif
Éviter le blocage du démarrage quand la configuration Brevo n'est pas encore définie.

## Ajouts
- `BREVO_API_KEY`
- `BREVO_SENDER_EMAIL`
- `BREVO_SENDER_NAME`
- `EMAIL_DEV_MODE`

## Comportement
- si `BREVO_API_KEY` est absente et `EMAIL_DEV_MODE=true` :
  - le provider email ne casse pas l'application
  - le batch email retourne un envoi simulé (`dev_skipped`)
- si `BREVO_API_KEY` est absente et `EMAIL_DEV_MODE=false` :
  - une erreur métier explicite est levée

## Fichiers concernés
- `app/config.py`
- `app/infrastructure/email/service_envoi_email.py`
- `.env.example`
