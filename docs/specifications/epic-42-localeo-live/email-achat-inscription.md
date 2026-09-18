# E-mail dans les détails personnels Localeo Live

Le détail du coffret présente « E-mail utilisé pour l’achat » depuis achat.email_acheteur
fourni par le passeport autorisé. L’adresse du bénéficiaire ne remplace pas celle de
l’acheteur. Si les informations d’achat sont indisponibles (notamment achat pro),
le détail indique « Adresse non disponible ».

Le détail de la participation sélectionnée dans le carnet présente « E-mail utilisé
pour l’inscription ». GET /public/localeo-live/participations/{id}?inclure_contact=true
ajoute email_inscription après résolution du Bearer et vérification de cette participation.
Sans cette option, la réponse demeure sans adresse e-mail. Une animation simplement
suivie et les pages générales d’une animation n’affichent pas d’adresse d’inscription.

L’e-mail d’inscription chargé pour le détail reste en mémoire, sans ajout
aux sauvegardes du carnet, aux URL ou aux événements de mesure d’audience.
