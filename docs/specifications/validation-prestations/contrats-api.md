# Validation de prestation - Mapping OpenAPI et decoupage ecrans

## Source analysee

Contrat analyse : `api/localeo-openapi.json`.

## APIs identifiees dans le contrat

### 1. Ouvrir une transaction de validation

`POST /protected/exploitation/validation/ouvrir-transaction`

**Parametres**
- Corps JSON `{ "qr_coffret_instance": "…" }`, obligatoire ; aucune donnée QR dans la query.
- `Authorization: Bearer <session_token>` avec une session commercant.

**Reponse**
- `transaction_id`
- `achat_id`
- `coffret_instance_id`
- `date_expiration`
- `statut`

**Lecture**
- cette API ouvre une transaction a partir d'un QR code d'instance de coffret.
- elle suppose qu'un QR code lie a l'instance de coffret est scanne avant le choix de la prestation.

### 2. Lister les prestations d'une instance de coffret

`GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`

**Parametres**
- `achat_id` en path.
- `coffret_instance_id` en path.
- `Authorization: Bearer <session_token>` pour le contexte Commerçants.

**Lecture**
- cette API recupere les statuts de prestations disponibles une fois l'instance de coffret identifiee.
- chaque ligne expose `id`, `prestation_coffret_id`, `commercant_id`, `statut` et `date_validation`.

### 3. Consulter une instance de coffret

`GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}`

**Lecture**
- utile pour afficher le recap de l'instance de coffret avant validation.
- le detail renvoie notamment `coffret_id`, utilise ensuite pour recuperer les libelles.

### 4. Consulter le detail public du coffret

`GET /public/coffrets/{coffret_id}`

**Lecture**
- permet de recuperer le nom du coffret et les libelles des prestations sources.
- le front mappe `prestation_coffret_id` vers les prestations du coffret.

### 5. Valider une prestation

`POST /protected/exploitation/validation/valider-prestation`

**Parametres**
- `transaction_id` en query, obligatoire.
- `statut_prestation_coffret_instance_id` en query, obligatoire.
- `Authorization: Bearer <session_token>` avec une session commercant.

**Lecture**
- cette API finalise la validation pour le commercant connecte.
- elle n'attend plus de `qr_commercant`.
- elle repond avec `validation_id`, `coffret_instance_id`, `statut_prestation_coffret_instance_id`, `mouvement_reversement_cree` et `statut`.

## Decoupage ecrans compatible contrat

### Ecran 1 - Scanner le QR client/coffret

**But**
Ouvrir la camera du telephone pour scanner le QR de l'instance de coffret.

**Action**
- lire le QR code client / coffret.
- appeler `POST /protected/exploitation/validation/ouvrir-transaction` avec
  `Authorization: Bearer <session_token>` et le corps JSON
  `{ "qr_coffret_instance": "…" }` ; ne pas transmettre le QR dans l'URL.

### Ecran 2 - Selectionner la prestation

**But**
Choisir la prestation a valider sur l'instance de coffret scannee.

**Donnees**
- recap instance via `GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}`.
- liste des statuts via `GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`.
- libelles via `GET /public/coffrets/{coffret_id}`.

**UI**
- recap coffret.
- liste des prestations.
- CTA par ligne `Valider cette prestation` uniquement pour les prestations attribuees au commercant connecte.

### Ecran 3 - Confirmation

**But**
Afficher le succes ou l'erreur finale apres appel de validation.

**Action**
- appeler `POST /protected/exploitation/validation/valider-prestation` avec :
  - `transaction_id`
  - `statut_prestation_coffret_instance_id`
  - `Authorization`

## Synthese

Le contrat OpenAPI courant porte un parcours :
- scan QR client / instance de coffret.
- ouverture de transaction.
- selection de prestation.
- validation par la session commercant.

Le QR commercant est decommissionne : l'identite commercant vient de la session `Authorization`.


## PRO-012 — Référence après remédiation

Pour le comportement courant (connexion par mot de passe ou carte, reprise, erreurs réseau et scan Animation), consulter [docs/specification/specification-version-actuelle.md](../espace-commercant/README.md) et [docs/api.md](../espace-commercant/contrats-api.md). Les anciennes descriptions à deux scans ne signifient pas une nouvelle authentification commerçant à chaque prestation.
