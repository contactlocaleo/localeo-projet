# Localeo V85 - Transactional Outbox Emails

## Objectif
Découpler l'envoi des emails des transactions métier tout en garantissant la persistance transactionnelle des demandes d'envoi.

## Principe
- les use cases créent des `EmailSortant` en base
- le provider n'est plus appelé directement dans la transaction métier
- un batch protégé envoie les emails en attente

## API ajoutée
- `POST /protected/emails/batch/envoyer`
- `POST /protected/emails/{email_id}/relancer`

## SQLAdmin
Vue `EmailSortantAdmin` ajoutée.

## Intégration réalisée
L'endpoint `POST /clients/coffrets-instances/{coffret_instance_id}/envoyer-lien-activation` crée désormais un email sortant en base au lieu d'envoyer directement le mail.
