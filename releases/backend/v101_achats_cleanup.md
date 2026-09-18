
# V101 - Nettoyage API Achats

## Suppression
- POST /achats
- POST /achats/pro

## Nouvelle responsabilité

API Achat = consultation uniquement :
- GET /achats/{id}
- GET /achats/{id}/coffrets-instances

## Déplacement logique
- Création → API Paiement (/paiements/initialiser)
