# Localeo V90 - Paiement pro avec nom d'entreprise et nom du contact

## Ajouts
Pour un paiement professionnel, le système gère désormais :
- `nom_entreprise`
- `nom_contact`

## API concernée
- `POST /paiement/initialiser-pro`

## Persistance
Les champs sont stockés sur `AchatCoffret` / `AchatCoffretOrm`.

## Back-office
Les informations sont visibles dans SQLAdmin sur la vue `AchatCoffretAdmin`.
