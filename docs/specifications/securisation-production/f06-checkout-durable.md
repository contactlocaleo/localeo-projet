# F06 - Initialisation durable du paiement

L'achat PAYMENT_PENDING, la reservation de credit et les parametres immuables
de Checkout sont commits avant tout appel Stripe. Le fournisseur utilise une
cle derivee de l'UUID d'achat. En cas d'interruption, le meme Idempotency-Key
client reprend cette demande, avec le meme UUID, montant et reservation.
La reponse Stripe ne met a jour que checkout_url pour ne pas ecraser un statut
confirme simultanement par webhook. Un echec du commit initial interdit l'appel.

La reprise automatique est bornee a 23 heures, sous la retention minimale de
24 heures des cles Stripe. Au-dela, ou pour un achat historique sans demande,
une reconciliation est requise avant toute nouvelle session. Les clients doivent
conserver et rejouer leur Idempotency-Key ; sans cette cle, une nouvelle requete
reste une nouvelle intention d'achat. Le credit integral utilise l'evenement de
confirmation idempotent existant et peut etre repris apres interruption.

Appliquer v217 avant ce code. Les parametres sauvegardes contiennent les memes
donnees personnelles que l'achat et suivent sa politique d'acces et de retention.
