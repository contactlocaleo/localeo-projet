# Protection de l'ecriture du referentiel coffret

La creation d'un type de coffret est reservee a
`POST /internal/commercialisation/types-coffrets`, avec une session ADMIN
et un jeton `X-CSRF-Token` issu de la session ERP. Le POST public est retire
(405) ; le GET public reste disponible pour la marketplace.

Aucun consommateur applicatif du POST public n'a ete trouve. Les outils
d'integration qui l'utilisaient doivent migrer vers la route interne.
Tests : `tests/security/test_type_coffret_write_authorization.py`.
