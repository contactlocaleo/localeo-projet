# Support et navigation transverse du BackOffice

La **Timeline support** est le point d'entrée recommandé pour une réclamation. Son champ de recherche globale accepte un email, un téléphone, une référence d'achat, un identifiant d'achat ou d'instance, une transaction PSP et un identifiant de message fournisseur.

La timeline regroupe achat, paiement, instance, activation, notifications, consommation, reversement, remboursement, expiration et audit. Les métadonnées sensibles restent masquées. Le contexte et les événements connus proposent un lien direct vers leur ressource SQLAdmin.

Des raccourcis supplémentaires relient :

- l'achat à ses paiements, instances, remboursements, emails et documents ;
- la validation au mouvement de reversement attendu ;
- le mouvement à sa validation source, son reversement et ses paiements de reversement ;
- les emails, SMS, paiements et instances à leur timeline support.

La fiche commerçant affiche avant toute suspension ou archivage le nombre de prestations à traiter, de coffrets actifs et d'instances clients encore en cours. Un blocage doit être résolu par les workflows métier, jamais par modification SQL.
