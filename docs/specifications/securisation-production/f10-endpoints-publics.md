# F10 - Limites paiement et support publics

Chaque IP peut initialiser au plus 10 paiements et envoyer au plus 5 messages
support par fenetre `LOCALEO_AUTH_RATE_LIMIT_WINDOW_SECONDS`. Changer l'email,
le coffret ou la cle d'idempotence ne renouvelle pas le quota. Les operations
sont comptees avant creation d'achat, Stripe, persistance du contact ou email.
Le depassement renvoie 429 avec Retry-After (indicatif, 60 secondes).

Un message support contient de 1 a 10 000 caracteres ; son email est borne a
254 caracteres. La cle d'idempotence de paiement est bornee a 128 caracteres.
Le mode de tests de performance reste interdit en production par la garde de
configuration existante. Une protection de debit globale au proxy complete
ces quotas applicatifs contre les sources distribuees.
