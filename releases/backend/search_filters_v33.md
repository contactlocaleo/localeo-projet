# Localeo V33 - Recherche avancée

## Villes
Recherche par préfixe :

GET /villes?nom_commence_par=Bo

## Commerçants
Recherche par ville :

GET /commercants?ville_id=<uuid>

Filtre type :

GET /commercants?ville_id=<uuid>&type_commercant_id=<uuid>

## Coffrets
Recherche par ville :

GET /coffrets?ville_id=<uuid>

Filtre type de coffret :

GET /coffrets?ville_id=<uuid>&type_coffret=gourmand

## Coffrets avec prestations

GET /coffrets?ville_id=<uuid>&avec_prestations=true
