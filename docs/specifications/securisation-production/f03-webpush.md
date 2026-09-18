# F03 - Destinations WebPush

La souscription et chaque envoi exigent HTTPS, port 443, aucun identifiant ni
fragment, et un hote exact de `LOCALEO_WEBPUSH_ALLOWED_HOSTS`. Par defaut :
`fcm.googleapis.com`, `updates.push.services.mozilla.com`, `web.push.apple.com`.
Ajouter un fournisseur uniquement apres validation par l'exploitation, sans joker.

Le transport refuse toute resolution contenant une IP non publique. Il se
connecte a l'IP validee en conservant le nom TLS et SNI, sans proxy d'environnement
ni redirection. Les attentes connexion/lecture sont bornees et la reponse est
limitee a 64 Kio. Les abonnements existants non conformes ne sont pas envoyes.
L'exploitation doit aussi restreindre les sorties reseau aux fournisseurs utiles.

Le transport prefere les adresses IPv4 aux adresses IPv6 afin de fonctionner
sur les hebergeurs sans sortie IPv6. Si la connexion echoue avant l'envoi,
il essaie les autres IP deja validees, dans un budget partage de 15 secondes.
Une erreur de lecture, une erreur TLS ou une reponse HTTP ne declenche pas ce
repli : un POST potentiellement deja recu ne doit pas etre repete a ce niveau.
Les retries de notification restent geres par les batchs et leurs outbox.
