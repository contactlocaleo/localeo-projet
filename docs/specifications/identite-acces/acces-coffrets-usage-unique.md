# Acces coffret par lien a usage unique

Les liens #code=cl1... sont captures et effaces avant requete API. Le code est
echange une fois par POST, avec deduplication des appels paralleles (detail,
prestations et QR) et conservation en memoire du resultat pendant sa validite.
Le bearer cs1... est envoye uniquement dans Authorization et conserve dans
sessionStorage ; la bibliotheque Live enregistre la session resolue, pas le
code email. La session expire apres huit heures et reste revocable cote serveur.

La session resolue est aussi associee au coffret et a l'empreinte SHA-256 du
code dans sessionStorage (100 acces maximum, isoles par configuration API).
Une reouverture du meme email dans le meme onglet, meme apres rechargement ou
echec du chargement du detail, reutilise cette session sans rejouer le code.
Les pages detail et QR retrouvent en priorite la session du coffret demande :
l'ouverture d'un deuxieme lot ne remplace pas l'acces au premier. Le code brut
n'est pas conserve dans le stockage. Un nouveau code est echange separement.
Si le meme lien est reintroduit sans recharger le document, les pages detail
et QR retirent de nouveau le fragment et relancent le chargement des donnees,
au lieu de conserver une erreur React Query de la tentative precedente.

L'expiration est controlee avant reutilisation ; chaque requete de donnees
reste soumise aux controles de revocation du backend. La reprise ne prolonge
pas la session. Sans stockage disponible, l'acces reste utilisable dans la
page courante ; apres fermeture de l'onglet, suppression du stockage ou dans
un autre navigateur, un code deja consomme necessite un nouveau lien.

Un acces refuse propose un renvoi vers l'adresse deja enregistree, sans champ
email ni revelation de cette adresse. Les codes uses ne permettent pas de
creer de nouvelles sessions. Les liens retour excluent aussi le code afin
d'eviter sa reinjection dans une URL de contact.

Les anciens liens de consultation restent lisibles pendant la migration.
Deployer avec le backend et la migration v233. Les demandes de renvoi sont
limitees cote serveur ; aucun message distant n'est envoye par les tests.

Apres renouvellement, la confirmation dans Live remplace la session expiree du
coffret deja present dans le carnet. Aucun doublon de coffret n'est cree.

Les liens consommes avant cette correction ne disposent pas de cette
association persistante. Si leur session ne peut pas etre retrouvee, le
parcours de renvoi reste necessaire ; aucun ancien code n'est reactive.
