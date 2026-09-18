# Contraste de la confirmation particulier en production

Anomalie découverte lors de la campagne F16 sur le bundle compilé : les styles partagés de confirmation pouvaient être chargés après le thème particulier et écraser, à spécificité égale, le fond et les couleurs du statut. Le panneau devenait transparent, avec du texte clair illisible sur la page claire.

Le thème particulier est désormais explicitement limité à l'ancêtre `.marketplace-shell--confirmation`. Il prime sur les styles partagés quel que soit l'ordre des chunks CSS, sans `!important` et sans modifier les thèmes professionnel ou de suivi.

Sur mobile, les états succès, avertissement, erreur et information conservent leur fond opaque et leurs textes sombres. Aucun changement des règles de validation du paiement : un résultat non confirmé n'est jamais présenté comme payé.

Tests : les deux ordres de chargement CSS et les quatre états sont vérifiés dans Chromium ; le test navigateur existant mesure aussi le contraste minimal de 4,5:1 sur la page compilée.
