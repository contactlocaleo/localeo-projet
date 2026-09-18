# Localeo V86 - Généralisation complète de l'outbox email

## Objectif
Supprimer les envois directs d'emails dans les use cases métier et faire passer les notifications applicatives par `EmailSortant`.

## Changements appliqués
- `ValiderPaiement` :
  - ne fait plus d'envoi direct
  - crée transactionnellement un `EmailSortant` de confirmation coffret
- `ValiderPrestation` :
  - ne fait plus d'envoi direct
  - crée transactionnellement un `EmailSortant` de prestation utilisée
- les APIs n'injectent plus `ServiceEmail` dans ces use cases

## Résultat
- plus d'appel direct au provider email dans la transaction métier
- les emails sont garantis en base si la transaction commit
- le batch `/protected/emails/batch/envoyer` devient le point d'exécution technique unique des envois
