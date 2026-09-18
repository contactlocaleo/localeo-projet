# Localeo V89 - Startup hardening

## Correctif principal
Le provider `ServiceEnvoiEmail` expose maintenant une méthode publique unifiée :

- `envoyer(destinataire, objet, corps_html, corps_texte)`

Ce correctif réaligne le provider avec le use case batch `LancerBatchEmails`, qui attendait cette signature.

## Effets
- le démarrage reste inchangé
- l'endpoint `POST /protected/emails/batch/envoyer` ne doit plus échouer sur un `AttributeError`
- le provider email reste cantonné au batch technique

## Points à vérifier en environnement
- dépendances Python installées
- variables Brevo configurées
- schéma DB à jour
- accès PostgreSQL opérationnel
