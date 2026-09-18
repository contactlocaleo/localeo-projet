# Activation du gestionnaire Animation (F03)

Apres activation de la souscription, le gestionnaire recoit un lien a usage
unique valable 24 heures et choisit son mot de passe. Aucun mot de passe n'est
envoye par email. Le portail lit le token depuis le fragment `#activation=...`
et efface ce fragment de l'historique courant ; il ne le stocke pas dans le
navigateur. Le formulaire demande et confirme le mot de passe, puis appelle
`POST /public/identite-acces/animation/invitations/activer` avec un corps JSON
`{token, mot_de_passe}`. Le backend valide expiration, usage unique, statut et
politique de mot de passe. Une reponse 204 permet de revenir a la connexion.

Un lien expire/deja utilise est refuse. Le renouvellement releve de
l'administrateur ; renvoyer un ancien email ne renouvelle pas sa validite.
Coordonner le deploiement du portail avec la migration backend v216.
