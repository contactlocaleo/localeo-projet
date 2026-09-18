# F15 - Identite de l'acteur d'audit

L'acteur est issu du principal authentifie (identifiant technique de cle API,
commercant ou achat) ou de la session admin signee. En son absence il vaut
`anonymous`, y compris lors d'un echec d'authentification. X-Actor-ID n'est jamais
une autorite et aucun prefixe de secret n'est journalise comme identite.
