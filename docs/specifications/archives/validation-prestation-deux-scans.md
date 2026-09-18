# Validation de prestation - Flux UX, API et modele de donnees

> **Cadrage historique, non applicable comme contrat courant.** Le parcours
> à deux scans, ses API cibles et son modèle proposé sont conservés pour leur
> provenance. Le [mapping de validation](../validation-prestations/contrats-api.md)
> et les [règles corrigées](../securisation-production/corrections-commercant-2026-09-05.md) portent le parcours
> documenté : QR client/coffret dans un corps JSON, puis validation autorisée par
> la session commerçant. Ce document ne justifie pas une nouvelle authentification
> du commerçant à chaque prestation.

## Contexte

La validation d'une prestation concerne obligatoirement une prestation rattachee a une instance de pack.

La validation se fait via une transaction de validation en 2 temps :
- identification du commercant par scan de son QR code
- validation de la prestation par scan du QR code du client

## Vocabulaire

**Pack instance**
Occurrence concrete d'un pack achete ou active pour un client.

**Prestation**
Element executable rattache a une instance de pack, realisable par un commercant.

**Validation transaction**
Objet technique et metier qui porte le workflow temporaire de validation d'une prestation.

## Parcours UX cible

### Ecran 1 - Liste des prestations
**Objectif**
Permettre au commercant d'identifier une prestation eligible a la validation.

**Contenu**
- reference prestation
- reference instance de pack
- client
- libelle prestation
- statut prestation
- etat de transaction si une transaction existe deja
- CTA `Demarrer la validation`

**Regles**
- le CTA n'est visible que pour les prestations validables
- une prestation deja validee n'est plus validable
- une prestation hors perimetre commercant n'est jamais accessible

### Ecran 2 - Initialisation de la transaction
**Objectif**
Creer une transaction de validation avant tout scan.

**Contenu**
- recap de la prestation
- recap de l'instance de pack
- message expliquant le process en 2 scans
- CTA `Commencer`

**Resultat**
- creation d'une transaction en statut `initiated`
- navigation vers l'ecran de scan commercant

### Ecran 3 - Scan QR commercant
**Objectif**
Identifier le commercant qui execute la validation.

**Contenu**
- camera / lecteur QR
- rappel de la prestation cible
- message d'instruction `Scannez votre QR commercant`
- action secondaire `Annuler`

**Resultats possibles**
- succes : transaction passe en `merchant_verified`
- QR invalide : message d'erreur et nouvelle tentative
- QR valide mais commercant non autorise : blocage
- abandon : transaction annulee ou expiree selon la regle definie

### Ecran 4 - Scan QR client
**Objectif**
Verifier que le client presente bien le QR correspondant a la prestation de l'instance de pack attendue.

**Contenu**
- camera / lecteur QR
- etat `Commercant verifie`
- message d'instruction `Scannez le QR client`

**Resultats possibles**
- succes : prestation validee, transaction `completed`
- QR client invalide : message d'erreur et nouvelle tentative
- QR client valide mais ne correspondant pas a l'instance de pack ou a la prestation attendue : refus
- expiration ou interruption : transaction `expired` ou `aborted`

### Ecran 5 - Confirmation
**Objectif**
Confirmer la fin du processus.

**Contenu**
- message de succes
- reference transaction
- reference prestation
- reference instance de pack
- horodatage
- CTA `Retour a mes prestations`

## Machine d'etat recommandee

### Statut de prestation
- `pending`
- `in_progress`
- `validated`
- `cancelled`
- `locked`

### Statut de transaction de validation
- `initiated`
- `merchant_verified`
- `completed`
- `failed`
- `aborted`
- `expired`

### Transitions principales
- `initiated` -> `merchant_verified`
- `merchant_verified` -> `completed`
- `initiated` -> `aborted`
- `merchant_verified` -> `aborted`
- `initiated` -> `expired`
- `merchant_verified` -> `expired`
- `initiated` -> `failed`
- `merchant_verified` -> `failed`

## API cible

## 1. Consulter les prestations validables

`GET /api/merchant/prestations`

**Query params possibles**
- `status`
- `pack_instance_id`
- `search`
- `page`
- `page_size`

**Response exemple**
```json
{
  "items": [
    {
      "prestation_id": "pre_001",
      "pack_instance_id": "pi_456",
      "pack_label": "Pack Gourmand",
      "prestation_label": "Remise du panier",
      "customer_display": "Claire Martin",
      "status": "pending",
      "scheduled_at": "2026-03-26T10:30:00Z",
      "validation_transaction": null
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

## 2. Consulter le detail d'une prestation

`GET /api/merchant/prestations/{prestation_id}`

**Response exemple**
```json
{
  "prestation_id": "pre_001",
  "pack_instance_id": "pi_456",
  "pack_label": "Pack Gourmand",
  "prestation_label": "Remise du panier",
  "status": "pending",
  "customer": {
    "display_name": "Claire Martin"
  },
  "validation": {
    "validated_at": null,
    "validated_by_merchant_id": null,
    "transaction_id": null
  }
}
```

## 3. Initialiser une transaction de validation

`POST /api/merchant/prestations/{prestation_id}/validation-transactions`

**Body exemple**
```json
{
  "pack_instance_id": "pi_456"
}
```

**Response exemple**
```json
{
  "transaction_id": "vtx_789",
  "status": "initiated",
  "prestation_id": "pre_001",
  "pack_instance_id": "pi_456",
  "expires_at": "2026-03-26T10:45:00Z"
}
```

## 4. Verifier le QR commercant

`POST /api/merchant/validation-transactions/{transaction_id}/verify-merchant`

**Body exemple**
```json
{
  "merchant_qr_payload": "signed-merchant-token"
}
```

**Response exemple**
```json
{
  "transaction_id": "vtx_789",
  "status": "merchant_verified",
  "merchant_id": "mer_123",
  "verified_at": "2026-03-26T10:31:00Z"
}
```

## 5. Verifier le QR client et terminer la validation

`POST /api/merchant/validation-transactions/{transaction_id}/verify-customer`

**Body exemple**
```json
{
  "customer_qr_payload": "signed-customer-token"
}
```

**Response exemple**
```json
{
  "transaction_id": "vtx_789",
  "status": "completed",
  "prestation": {
    "prestation_id": "pre_001",
    "status": "validated",
    "validated_at": "2026-03-26T10:31:24Z"
  }
}
```

## 6. Consulter une transaction

`GET /api/merchant/validation-transactions/{transaction_id}`

## 7. Abandonner une transaction

`POST /api/merchant/validation-transactions/{transaction_id}/abort`

## Regles metier minimales

- une transaction ne peut concerner qu'une seule prestation
- une transaction ne peut concerner qu'une seule instance de pack
- le scan client est impossible tant que le scan commercant n'est pas valide
- le QR client doit correspondre a l'instance de pack attendue
- une prestation `validated`, `cancelled` ou `locked` ne peut pas ouvrir une nouvelle transaction
- la transaction doit expirer apres une duree definie

## Modele de donnees cible

## Entite `pack_instance`

```json
{
  "id": "pi_456",
  "pack_id": "pack_001",
  "customer_id": "cus_777",
  "status": "active",
  "activated_at": "2026-03-25T09:10:00Z"
}
```

## Entite `prestation`

```json
{
  "id": "pre_001",
  "pack_instance_id": "pi_456",
  "merchant_id": "mer_123",
  "label": "Remise du panier",
  "status": "pending",
  "scheduled_at": "2026-03-26T10:30:00Z",
  "validated_at": null,
  "validated_by_merchant_id": null,
  "validation_transaction_id": null
}
```

## Entite `validation_transaction`

```json
{
  "id": "vtx_789",
  "prestation_id": "pre_001",
  "pack_instance_id": "pi_456",
  "merchant_id": "mer_123",
  "status": "merchant_verified",
  "merchant_verified_at": "2026-03-26T10:31:00Z",
  "customer_verified_at": null,
  "completed_at": null,
  "expires_at": "2026-03-26T10:45:00Z",
  "failure_reason": null
}
```

## Entite `validation_transaction_event`

```json
{
  "id": "vte_001",
  "transaction_id": "vtx_789",
  "type": "merchant_qr_verified",
  "occurred_at": "2026-03-26T10:31:00Z",
  "payload": {
    "merchant_id": "mer_123"
  }
}
```

## Recommandations techniques

- utiliser des QR codes signes ou porteurs d'un token non forgeable
- eviter d'encoder des donnees sensibles en clair dans le QR
- rendre la transaction idempotente sur les etapes de scan
- journaliser les echecs de scan et les refus metier
- prevoir une verification serveur de la coherence entre `prestation`, `pack_instance`, `merchant` et `customer`

## Questions de conception restantes

- faut-il autoriser plusieurs transactions simultanees pour une meme prestation ?
- que faire d'une transaction interrompue apres scan commercant valide ?
- le QR client porte-t-il seulement l'identifiant de l'instance de pack ou aussi celui de la prestation ?
- faut-il un mode fallback manuel en cas de camera indisponible ?
