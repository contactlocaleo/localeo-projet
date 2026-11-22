# Petits correctifs proposés, sous choix utilisateur

Trois classes A conditionnelles dans les neuf fiches : R01 frontière async/sync, R03 projections auxiliaires QR/PIN, R07 résumés commerces du passeport. Leur périmètre court ne dispense pas des preuves de contexte/session, seuil/régularisation ou ordre/adresse.

R01 est P1 sous scénario du même event loop ; les quatre ERP sans await peuvent utiliser def, l'image async doit déporter l'unité après lecture. R03 et R07 restent P2 sans impact intégré mesuré ; aucune migration d'index ou nouveau cache proposé par défaut.

R05, suppression de copie tirage, reste P3 différable en annexe. Pas de gain démontré ; la population complète sous verrou demande un autre remède, pas une promesse de mémoire bornée.

Effort S relatif, pas estimation en jours. Tests et retours arrière dans [les fiches](backlog-final.md). Gains après correction NON MESURÉS.
