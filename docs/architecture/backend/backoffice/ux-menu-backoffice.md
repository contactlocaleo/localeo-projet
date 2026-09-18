# Conventions UX et menu du BackOffice

Les entrées personnalisées du menu sont enregistrées par identité unique. Le démarrage échoue si une même `BaseView` est déclarée plusieurs fois, ce qui protège notamment les consoles Animation.

Les badges utilisent une palette commune : vert pour succès/actif, orange pour attente ou action requise, rouge pour erreur ou blocage, gris pour archivage/expiration et bleu pour information. Les principaux statuts techniques ont un libellé français partagé.

Les listes privilégient les informations nécessaires au traitement immédiat. Les champs secondaires restent disponibles dans la fiche détaillée ; la liste des achats est volontairement limitée à dix colonnes et la pagination standard est de 25 lignes.

Les opérations exposées par une action SQLAdmin présentent une confirmation. Les retours d'action ajoutent l'identifiant de corrélation lorsqu'il est disponible afin de retrouver rapidement les traces correspondantes.
