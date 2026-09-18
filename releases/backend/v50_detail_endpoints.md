# Localeo V50 - Endpoints de détail

Cette version ajoute les endpoints de détail suivants :

- `GET /villes/{id}`
- `GET /commercants/{id}`
- `GET /coffrets/{id}`

## Objectif
Faciliter :
- les pages détail front
- le deep linking
- le routage front
- les parcours marketplace plus standards

## Détail du coffret
`GET /coffrets/{id}` retourne le coffret avec la liste de ses prestations.
