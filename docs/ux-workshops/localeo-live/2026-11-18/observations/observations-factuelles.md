# Observations factuelles

Contexte : Chromium/Playwright, émulation mobile tactile, 320 × 844, 390 × 844 et 430 × 844. Commune de référence : Bouliac. Navigateur vierge, sans accès personnel ni inscription effectuée.

| ID | Statut | Constat | Parcours et capture |
| --- | --- | --- | --- |
| O1 | OBSERVÉ | La racine de `test-live.localeo.city` aboutit à `/live/carnet`. Le carnet vide donne « Découvrir les animations » et « Retrouver mon carnet ». | Entrée ; `01-accueil-*` |
| O2 | OBSERVÉ | La navigation basse présente « Mon carnet », « Mes lots », « Découvrir » sur les trois largeurs. Aucun débordement horizontal détecté sur Découvrir à 320, 390 et 430 px. | Entrée/découverte ; `01-*`, `02-*` |
| O3 | OBSERVÉ | La recherche « Bouliac » renvoie Bouliac 33270. Après « Suivre Bouliac », la sélection est visible dans Découvrir. | Découverte ; `02-decouvrir-bouliac-*` |
| O4 | OBSERVÉ | Le programme de Bouliac présente deux animations en cours (« Test juste prix Local », « Test jeu des vitrines ») et une à venir (« Test tombola Locale »), chacune avec une période et « Voir l’animation ». | Découverte/calendrier ; `02-*` |
| O5 | OBSERVÉ | Les fiches des trois animations présentent leurs dates, une dotation prévue et un accès à l’inscription. La fiche tombola annonce que le parcours de jeu sera disponible au démarrage. | Fiches ; `03-*`, `05-*`, `06-*` |
| O6 | OBSERVÉ | L’inscription Juste prix demande quatre coordonnées obligatoires, la majorité et l’acceptation du règlement ; l’option de nouvelles est facultative. | Inscription ; `04-*` |
| O7 | OBSERVÉ | Le carnet de participations et Mes lots sont vides dans ce navigateur neuf. Mes lots affiche d’abord un état de lecture, puis son état vide. | Suivi/lots ; `07-*`, `08-*` |
| O8 | OBSERVÉ | Le formulaire de récupération demande un e-mail ; l’envoi à vide est bloqué par le navigateur. Aucun lien n’a été demandé. | Récupération ; `09-*` |
| O9 | OBSERVÉ | Un code d’ajout d’animation volontairement invalide aboutit à « Cet accès n’est plus disponible » et propose « Retrouver mon accès ». | Entrée QR invalide ; `10-*` |
| O10 | OBSERVÉ | Après navigation vers Communes puis retour navigateur, Découvrir revient avec Bouliac sélectionnée et ses animations visibles. | Retour ; `11-*` |
| O11 | OBSERVÉ | L’URL `/live/calendrier` redirige vers `/live/decouvrir`. Les dates sont présentées dans le programme et les fiches, sans grille mensuelle visible pendant cet essai. | Calendrier ; `02-*`, `03-*`, `06-*` |
| D1 | DÉDUIT | Le code prévoit des états personnels de lot, un détail de bon numérique et l’export ICS d’une date de tirage ; ils n’ont pas été exercés avec des données réelles. | Code ; `LiveLots.jsx`, `LiveDrawCalendar.jsx` |

Aucune hypothèse sur la compréhension ou la satisfaction des habitants n’est formulée à cette étape.
