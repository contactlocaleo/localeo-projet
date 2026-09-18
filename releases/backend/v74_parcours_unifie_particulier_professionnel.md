# Localeo V74 - Parcours d'achat unifié particulier / professionnel

## Principe
- `AchatCoffret` reste la transaction d'achat
- `CoffretInstance` devient l'unité métier consommable ou activable

## Parcours particulier
1. Paiement validé
2. Création d'un `CoffretInstance` par quantité
3. Activation automatique
4. Génération du QR
5. Création des statuts de prestations consommables

## Parcours professionnel
1. Paiement validé
2. Création d'un `CoffretInstance` par quantité
3. Statut `EN_ATTENTE_ACTIVATION`
4. Token d'activation généré
5. Activation plus tard via un lien ou une API

## APIs ajoutées
- `POST /paiement/initialiser` avec `type_client` et `quantite`
- `GET /clients/achats-coffret/{achat_id}/coffrets-instances`
- `POST /clients/coffrets-instances/activer`

## Validation
Les QR utilisés en validation concernent désormais le `CoffretInstance` actif.
