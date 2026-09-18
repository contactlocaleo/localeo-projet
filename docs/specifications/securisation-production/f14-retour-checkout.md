# F14 - Consultation apres Checkout

`GET /gestion-achats/achats/depuis-session/{session_id}` exige desormais le token
de gestion de l'achat (`Authorization: Bearer ...` ou `X-Management-Token`).
La session Stripe sert uniquement a retrouver l'achat ; elle ne constitue plus
une autorisation. Le hash, l'expiration et la revocation du token local sont
verifies avant toute projection du detail. Sans token : refus avant appel Stripe.

Le front doit afficher un retour de paiement generique tant que l'utilisateur
n'a pas ouvert son lien de gestion recu par email. Il ne doit plus charger le
detail uniquement avec le session_id dans l'URL de retour. Le lien de gestion
existant reste le parcours d'acces ; aucun nouveau secret n'est place dans l'URL
Stripe. Cette modification de contrat doit etre livree avec l'adaptation du front.

Les journaux masquent les identifiants Checkout standards et le use case ne les
interpole plus. Les reponses achat/admin/internes portent no-store/no-referrer.
Le proxy doit masquer egalement les chemins contenant ces identifiants.
