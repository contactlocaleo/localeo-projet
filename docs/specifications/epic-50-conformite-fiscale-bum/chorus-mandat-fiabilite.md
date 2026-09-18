# F16 — Révocation Chorus sans traitement du rejet asynchrone

Une seule commande de mandat peut être en cours dans un écran. Une révocation utilise la version du mandat affichée (`expectedVersion`). Les écritures ne sont jamais rejouées automatiquement.

Après une écriture réussie ou une réponse non confirmée, le frontend relit le mandat. Seule cette lecture détermine son état affiché. Si elle échoue, les commandes d’acceptation et de révocation sont masquées ; « Réessayer » effectue uniquement une lecture. Un HTTP 401 signale la session expirée. Les preuves des dépôts antérieurs restent conservées.

L’opération est bornée à 15 secondes et annulée au départ de l’écran ou au changement de session. Une réponse tardive ne peut pas mettre à jour le nouvel écran. Une annulation réseau ne signifie pas que le serveur a annulé l’écriture : une nouvelle lecture est obligatoire avant toute nouvelle commande.

Validation : `src/features/finance/ChorusPage.test.jsx` (réponse perdue, relecture indisponible, double soumission, 401, changement de session et délai). Les tests de contrat couvrent les routes et champs JSON. Les simulations locales ne certifient pas l’état d’un mandat en production.
