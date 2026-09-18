# Localeo V71 - Refacto consolidé

Cette version part de `localeo_v57_targeted_internal_cleanup` et intègre proprement :

- sécurisation des APIs sensibles par API key (`X-API-KEY`)
- module de reversements commerçants
- intégration atomique de la création du mouvement de reversement dans `ValiderPrestation`
- bootstrap des nouveaux modèles SQLAlchemy
- endpoints protégés pour créer et exécuter les reversements

## Endpoints publics
- `/villes`
- `/commercants`
- `/coffrets`
- `/clients`
- `/validation/*`

## Endpoints protégés
- `/reversements`
- `/reversements/{reversement_id}/executer`
- `/protected/paiement/*`

## Garantie métier
Une validation de prestation crée dans la même transaction :
- une `ValidationPrestation`
- un `MouvementReversement`

Donc pas d'écart possible entre les deux en cas d'échec transactionnel.
