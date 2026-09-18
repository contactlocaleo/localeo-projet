# En-tête commun aux applications internes

Localeo ERP, Localeo OnBoard, Localeo Support et Localeo Ops utilisent les mêmes ressources
`app-header.js` et `app-header.css` pour leur bandeau de navigation.

- Identité Localeo et nom de l'application active ; le nom ramène à son accueil.
- Lien « Accueil ERP » sur ordinateur, également disponible dans le menu
  « Applications » sur mobile via « Localeo ERP ».
- Menu commun vers les quatre applications et déconnexion de la session interne.
- Application active signalée ; menu accessible au clavier, fermeture par Échap
  ou clic extérieur. Aucun appel métier supplémentaire pour afficher le bandeau.

Les commandes propres à chaque application restent sous le bandeau : contexte
et création dans l'ERP, connexion réseau, actualisation et nouveau dossier dans
OnBoard. Le menu latéral ERP conserve sa navigation et son bouton mobile.
Les liens empruntent les routes authentifiées existantes et ne modifient pas
les habilitations. Les fiches custom hors de ces quatre shells restent inchangées.
