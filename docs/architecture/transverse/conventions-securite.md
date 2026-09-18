# Conventions securite

## Exposition

Les routes sont classees selon trois niveaux :

- `public` : accessible sans authentification applicative, avec controles anti-abus si necessaire.
- `protected` : accessible apres authentification ou token applicatif valide.
- `internal` : reserve aux usages d'exploitation, batchs, back-office ou integrations controlees.

## Identite et acces

Le domaine `identite_acces` porte :

- sessions ;
- tokens ;
- API keys ;
- authentification ;
- autorisations ;
- rate limit.

Les domaines metier consomment ces mecanismes sans les reimplementer.

## Audit

Les actions sensibles doivent produire un evenement d'audit exploitable :

- validation ou annulation de validation ;
- remboursement ;
- generation ou paiement de reversement ;
- changement de statut d'un coffret ou d'une animation ;
- changement d'habilitation ou d'acces.

## Idempotence

Les flux sensibles aux repetitions doivent etre idempotents ou detecter explicitement les doublons :

- webhooks paiement ;
- validation QR ;
- creation de reversement ;
- generation de document ;
- envoi de notification.

