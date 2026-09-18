# Revocation des QR et des transactions de consommation

Appliquer `sql/v232_revocation_qr_transactions.sql` avec le runner habituel
avant de demarrer le nouveau backend. Le controle de schema exige la colonne.
Les transactions OPEN anterieures sont expirees ; il suffit de rescanner.

Chaque QR nouvellement emis contient un identifiant aleatoire `jti` signe.
Le QR enregistre sur l'instance est l'emission active. Les anciens QR sans
`jti` restent compatibles seulement s'ils correspondent exactement a cette
emission : aucune exception de verification n'est accordee aux anciens QR.

La regeneration du QR ou du lien de consultation remplace le QR actif.
La revocation du lien efface le QR actif, puisqu'il pouvait etre recupere
avec ce lien. Pour reprendre l'utilisation, regenerer le QR ou le lien et
utiliser le nouvel email. Les anciens bons imprimes deviennent inutilisables
apres cette operation explicite.

Une transaction conserve l'empreinte du QR scanne. La consommation recontrole
cette empreinte sous le meme verrou d'instance que la regeneration/revocation.
Un scan anterieur ne permet donc pas de contourner une revocation ulterieure.
Les rejeux de transactions deja terminees restent idempotents.

Le QR reste un titre au porteur ; la confirmation du beneficiaire appartient
au troisieme lot de l'audit.
