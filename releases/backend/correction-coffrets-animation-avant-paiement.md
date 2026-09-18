# Coffrets d'animation avant paiement

Les coffrets selectionnes a la creation restent visibles dans Localeo Animation,
y compris avant les acceptations des commercants. Le catalogue communal sert a
les afficher et a modifier la selection ; l'eligibilite au paiement reste controlee
separement avec les participants effectifs de l'animation.

Le PATCH de configuration permet d'ajouter, retirer et changer les quantites avant
paiement et publication. En presence d'une commande impayee, il verrouille la
commande, verifie les preuves locales de paiement et fait expirer sa session
Stripe avant de retirer cette commande. La prochaine commande utilise les lots
enregistres. La commande retiree ne peut plus etre reprise par son ancien lien API.

Une session complete/payee chez Stripe, meme avant reception du webhook, interdit
la modification. Aucun remboursement n'est declenche par ce parcours. Les erreurs
de verification Stripe, la preparation du checkout et la capture du credit exigent
une actualisation avant une nouvelle tentative. Les lots payes et les animations
publiees restent verrouilles.

La creation et la reprise de commande utilisent le verrou de l'animation pour ne
pas se croiser avec une modification des lots. Les reservations de credit d'une
commande remplacee sont liberees dans la transaction de configuration.

Reference fournisseur : [expiration d'une session Checkout](https://docs.stripe.com/api/checkout/sessions/expire).

Validation : tests de domaine, service de financement, passerelle Stripe avec
doubles, non-regression paiement/webhook et parcours navigateur dans le depot
`localeo-animation`. Aucun paiement ni remboursement reel n'est necessaire.
