# Localeo V32 - Filtres de recherche

## API villes
Recherche non stricte de type « commence par » sur le nom :

```http
GET /villes?nom_commence_par=Bor
```

## API commerçants
Recherche par ville :

```http
GET /commercants?ville_id=<uuid_ville>
```

## API coffrets
Recherche des coffrets par ville :

```http
GET /coffrets?ville_id=<uuid_ville>
```
