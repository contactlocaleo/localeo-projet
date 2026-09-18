# Refus des QR malformes

Les signatures non ASCII et les champs de type/cle non scalaires sont refuses
comme QR invalides avant comparaison cryptographique. Ils ne provoquent plus
d'erreur serveur et suivent le comptage des echecs de scan. Quatre cas de
regression s'ajoutent aux tests de rotation et de revocation.
