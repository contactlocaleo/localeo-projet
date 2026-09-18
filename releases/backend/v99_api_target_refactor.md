# Localeo V99 - Refactor API selon le découpage cible

## Découpage retenu
- API Ville
- API Statistique
- API Commerçant
- API Coffret
- API Email
- API Reversement
- API Achat
- API Paiement
- API Validation

## Suppressions
Les APIs qui ne rentraient pas dans ce découpage ont été supprimées du projet.

## Répartition
### Publiques
- `/villes*`
- `/statistiques`
- `/commercants*`
- `/coffrets*`
- `/achats*`
- `/paiements/webhooks/stripe`
- `/validation/*`

### Protégées par API key
- `/protected/emails*` → `internal:batch`
- `/protected/reversements*` → `internal:finance`

## Notes
- la gestion back-office de création / modification des villes, commerçants et coffrets reste portée par SQLAdmin
- l'API paiement ne gère plus que le retour Stripe
- l'API achat gère l'acte d'achat, particulier et professionnel, ainsi que la consultation des instances générées
