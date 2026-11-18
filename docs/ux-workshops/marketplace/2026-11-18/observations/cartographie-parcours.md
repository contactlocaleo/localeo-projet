# Cartographie des parcours publics

Périmètre : environnement TEST, 18 novembre 2026, navigateur Chromium automatisé. `OBSERVÉ` désigne un écran ou un lien parcouru ; `DÉDUIT` un comportement lu dans le code ; `HYPOTHÈSE` une question pour le workshop.

| Parcours | Trajet et état constaté | Preuve |
| --- | --- | --- |
| A — Première impression | **OBSERVÉ** `/` redirige vers `/accueil`. Accroche « Trouvez un coffret. Vivez le local », recherche, commune, coffret vedette, mode d’emploi, agenda et Live. Menu mobile ouvrable. | `accueil-{compact,standard,grand,desktop}.png`, `menu-mobile-390.png` |
| B — Coffrets | **OBSERVÉ** `/recherche` propose Tout, Coffrets, Communes, Adresses, Expériences, Animations ; filtre commune, puis budget/type en mode Coffrets. La fiche `/coffret?...` expose prix, validité, promesse, expériences indicatives, partenaires et formulaire d’achat. | `parcours-1-390.png`, `parcours-3-390.png`, `coffret-{390,1440}.png` |
| C — Territoires et commerces | **OBSERVÉ** recherche Communes → `/city?ville_id=...` (Bouliac) → liste de coffrets, expériences, animations et adresses → `/commercant?commercant_id=...` (Café des Promeneurs) → coffret associé. Le fil d’Ariane et les liens ramènent vers la commune. | `parcours-2-390.png`, `commune-390.png`, `commercant-390.png` |
| D — Animations | **OBSERVÉ** `/recherche?type=ANIMATION` et la section agenda communal renvoient vers `test-live.localeo.city/live/animations/...`. La liste de commune est `/live/decouvrir?commune=...` ; le détail expose dates, règles, lots, commerces et inscription. | `animations-390.png`, `agenda-commune-390.png`, `animation-detail-390.png` |
| E — Achat | **OBSERVÉ** sélection d’un coffret → récapitulatif dans la fiche → e-mail et téléphone obligatoires → bouton « Acheter ce coffret - 59,90 € ». **DÉDUIT** l’envoi appelle `POST /public/gestion-achats/paiements/initialiser`, crée un achat et une session avant la redirection Stripe : arrêt avant soumission. | `coffret-390.png`, [analyse Stripe](parcours-achat-stripe.md) |
| F — Confiance et cadeau | **OBSERVÉ** mentions du coffret numérique reçu par e-mail, du paiement sécurisé, des partenaires, de la validité, de la carte cadeau préparée après achat et liens CGV/confidentialité/contact. Les CGV sont accessibles après chargement. | `accueil-desktop.png`, `coffret-390.png`, `parcours-5-1440.png` |

**DÉDUIT — routes :** `localeo-marketplace/src/App.jsx:291-338` déclare ces pages et les retours de paiement. Les anciennes entrées d’animations sont redirigées vers Live (`App.jsx:275-291`). Cette cartographie du code ne prouve pas que chaque chemin a été ouvert dans le navigateur.
