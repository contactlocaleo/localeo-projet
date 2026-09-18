# Conventions API et OpenAPI

## Objectif

Les API doivent rendre visibles deux axes distincts :

- le niveau d'exposition : public, protected ou internal ;
- le domaine fonctionnel qui porte le use case.

## Chemins HTTP

La convention cible est :

```text
/{exposition}/{domaine}/{ressource}
```

Exemples :

```text
/public/referencement/villes
/protected/gestion-achats/achats/{achat_id}
/internal/exploitation/batchs/expiration
```

## Tags OpenAPI

Chaque operation doit porter :

- un tag d'exposition : `public`, `protected` ou `internal` ;
- un tag de domaine : `referencement`, `commercialisation`, `gestion_achats`, `gestion_reversement`, `exploitation`, `support`, `profils`, `dam`, `documentaire`, `identite_acces` ou `animation_locale`.

Le chemin sert au routage et a la lisibilite d'integration. Les tags servent a filtrer les contrats OpenAPI et a produire des vues dediees.

## Contrats

Les contrats peuvent etre exposes en trois vues :

- public : routes consommables sans session back-office ni session commercant ;
- protected : routes avec authentification applicative ;
- internal : routes reservees a l'exploitation interne, aux batchs ou aux integrations controlees.

## Migration

Pour les reorganisations structurelles type EPIC 40, la cible est une migration one-shot sans coexistence durable entre anciens et nouveaux chemins.

