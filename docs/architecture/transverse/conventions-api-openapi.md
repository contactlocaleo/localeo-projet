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

## Listes et coût des lectures

Appliquer la [convention performance et volumétrie](performance-volumetrie.md) aux nouvelles listes et aux lectures modifiées : pagination effective côté stockage, filtres d’accès avant limite, tri total, curseur par clé, `limit` par défaut 25 et maximum 100, enrichissements bornés et absence de total exhaustif systématique. Le schéma documente curseur, bornes, filtres/tris, cohérence de navigation et erreurs. Les sélecteurs, enfants de fiche et routes internes sont concernés. Les anciennes routes conservent leur contrat jusqu’à une migration explicite de leurs consommateurs ; leur dette n’autorise pas une nouvelle lecture non bornée.

## Migration des chemins

Pour les reorganisations structurelles type EPIC 40, la cible est une migration one-shot sans coexistence durable entre anciens et nouveaux chemins.

