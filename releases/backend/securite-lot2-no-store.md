# Absence de stockage des reponses sensibles

Cache-Control: no-store et Referrer-Policy: no-referrer couvrent toutes les
routes /protected/, les routes publiques gestion-achats et identite-acces,
ainsi que les anciens chemins achat. La politique concerne succes et erreurs.
Le PNG QR n'autorise plus une heure de cache navigateur.
Les routes internes gardent same-origin pour les formulaires CSRF.
Le catalogue public reste eligible a sa politique de cache habituelle.

Tests HTTP sur les vrais montages FastAPI : consultations, QR detail/PNG,
contacts prives, reponses avec et sans authentification et catalogue public.
