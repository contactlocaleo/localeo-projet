# Parcours d’achat et frontière Stripe

## Écran effectivement observé

**OBSERVÉ** Sur la fiche du coffret « À table, puis en balade » à 59,90 €, le visiteur voit la promesse, deux adresses, la validité de 90 jours après activation, le détail des expériences, les modalités de réservation, puis le formulaire « Adresse e-mail de réception » et « Téléphone de contact (obligatoire) ». La page explique que le coffret sera accessible après confirmation du paiement et qu’une carte cadeau peut ensuite être préparée. Le bouton final porte « Acheter ce coffret - 59,90 € ». Capture : [`coffret-390.png`](../visuels/captures-avant/coffret-390.png).

## Mécanisme lu dans le code, non exécuté

- **DÉDUIT** `localeo-marketplace/src/pages/CoffretPage.jsx:460-504` : l’envoi valide e-mail et téléphone, appelle `api.createCheckout`, valide l’URL retournée puis fait `window.location.assign(checkoutUrl)`.
- **DÉDUIT** `localeo-marketplace/src/services/api.js:700-745` : `createCheckout` envoie `POST /public/gestion-achats/paiements/initialiser` avec coffret, e-mail, téléphone, type de client et quantité, ainsi qu’une clé d’idempotence et un jeton de retour.
- **DÉDUIT** `localeo-backend/app/api/paiements_api.py:15-35` : cette route invoque `CreerAchatEtInitialiserPaiement`. `localeo-backend/app/application/gestion_achats/use_cases/initialiser_paiement.py:398-438` enregistre et valide l’achat, demande un checkout au fournisseur, conserve l’URL puis valide de nouveau l’unité de travail. L’appel a donc des effets métier avant la redirection du navigateur.

**Point d’arrêt sûr : avant toute soumission du formulaire.** Aucun `POST /paiements/initialiser`, création d’achat, session Stripe, confirmation de commande ni paiement n’a été déclenché dans cet audit. La page Stripe et son rendu ne sont pas vérifiés. Une validation de ce passage demanderait une procédure de test distincte et la confirmation préalable de l’innocuité des effets métier, conformément à la consigne.
