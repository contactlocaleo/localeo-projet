# Localeo V96 - API keys & scopes

## Publiques
- `/villes*`
- `/commercants*`
- `/coffrets*`
- `/paiement/initialiser`
- `/paiement/initialiser-pro`
- `/paiement/valider`
- `/clients/achats-coffret/*`
- `/clients/coffrets-instances/*`
- `/activation/*`
- `/validation/*`
- `/statistiques`

## Internes
- `/internal/reversements*` → scope `internal:finance`
- `/internal/emails*` → scope `internal:batch`

## Header
- `X-API-KEY`

## Modèle
- table `api_keys`
- clé stockée hashée
- prefix d’identification
- scope technique
- activation / désactivation
- `last_used_at` pour l’audit
