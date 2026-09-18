# F07 - Reprise des envois WebPush commercants

Les claims sont pris sous verrou de ligne PostgreSQL `FOR UPDATE SKIP LOCKED`.
Un envoi EN_COURS_ENVOI sans activite depuis 10 minutes peut etre repris. Avant
l'envoi, le worker verrouille la ligne et verifie le statut et l'horodatage de
son claim. Un ancien worker ne peut donc finaliser une nouvelle prise.
Le verrou reste acquis pendant les envois de cette notification ; le transport
F03 borne chaque appel reseau. Apres cinq tentatives interrompues ou echouees,
la notification est classee en echec definitif pour investigation.

La livraison est au moins une fois : une interruption apres acceptation par
le fournisseur et avant commit peut produire un doublon. Une notification ne
constitue jamais une validation de prestation ou une ecriture financiere.
Un suivi par abonnement/exactement une fois n'est pas garanti par WebPush.
