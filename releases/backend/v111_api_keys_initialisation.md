# Initialisation D'Une API Key

## Objectif

Cette note decrit la procedure pour generer une nouvelle API key, la stocker en base et l'utiliser sur les endpoints proteges.

Le mecanisme actif repose sur :

- [app/security/api_keys.py](/c:/Users/casta/Google%20Drive/10_LOCALEO/backend/localeo_v107_observability_errors/app/security/api_keys.py)
- [app/domaine/api_keys.py](/c:/Users/casta/Google%20Drive/10_LOCALEO/backend/localeo_v107_observability_errors/app/domaine/api_keys.py)
- la table `api_keys`

Le header attendu par l'API est `X-API-KEY`.

## Scopes Disponibles

Les scopes actuellement declares dans le domaine sont :

- `internal:finance`
- `internal:batch`
- `internal:admin`
- `internal:ops`

Le controle de scope est strict : une cle `internal:admin` ne permet pas d'appeler un endpoint qui exige `internal:batch`.

## Ce Qui Est Stocke En Base

La cle brute n'est jamais stockee telle quelle.

Pour chaque API key, on stocke :

- `label` : nom lisible de la cle
- `key_prefix` : les 8 premiers caracteres de la cle brute
- `key_hash` : hash SHA-256 de la cle brute
- `scope` : scope autorise
- `active` : indicateur d'activation

## Procedure

### 1. Generer Une Cle Brute

Exemple PowerShell :

```powershell
$raw = "loc_batch_" + [guid]::NewGuid().ToString("N")
$prefix = $raw.Substring(0, 8)
$sha = [System.Security.Cryptography.SHA256]::Create()
$bytes = [System.Text.Encoding]::UTF8.GetBytes($raw)
$hashBytes = $sha.ComputeHash($bytes)
$hash = -join ($hashBytes | ForEach-Object { $_.ToString("x2") })

"RAW=$raw"
"PREFIX=$prefix"
"HASH=$hash"
```

La sortie fournit :

- `RAW` : la cle a conserver secretement
- `PREFIX` : la valeur a stocker dans `key_prefix`
- `HASH` : la valeur a stocker dans `key_hash`

### 2. Inserer La Cle En Base

Exemple pour une cle de batch :

```sql
INSERT INTO api_keys (
    id,
    label,
    key_prefix,
    key_hash,
    scope,
    active
) VALUES (
    gen_random_uuid(),
    'batch emails',
    '<PREFIX>',
    '<HASH>',
    'internal:batch',
    true
);
```

Exemple pour une cle d'operations :

```sql
INSERT INTO api_keys (
    id,
    label,
    key_prefix,
    key_hash,
    scope,
    active
) VALUES (
    gen_random_uuid(),
    'ops tool',
    '<PREFIX>',
    '<HASH>',
    'internal:ops',
    true
);
```

### 3. Appeler L'Endpoint

Exemple d'appel du batch email :

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/protected/emails/batch/envoyer?limit=100" `
  -Headers @{ "X-API-KEY" = "<RAW>" }
```

Exemple d'appel de synchronisation des statuts email :

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/protected/emails/batch/synchroniser-statuts?limit=100" `
  -Headers @{ "X-API-KEY" = "<RAW>" }
```

## Verification

Quelques controles utiles :

- si le header `X-API-KEY` est absent : `401 API key missing`
- si la cle n'existe pas ou ne correspond pas au hash : `403 API key invalid`
- si la cle est desactivee : `403 API key inactive`
- si le scope ne correspond pas : `403 Insufficient scope`

## Bonnes Pratiques

- Ne jamais stocker la cle brute dans le depot.
- Conserver la cle brute dans un coffre de secrets ou un gestionnaire de mots de passe.
- Utiliser une cle distincte par usage technique.
- Donner le scope minimum necessaire.
- Desactiver une cle compromise avec `active = false`.

## Exemple Complet

Valeurs generees :

```text
RAW=loc_batch_db0fef438c2a464a84614c64e8f5447f
PREFIX=loc_batc
HASH=47e48783c49b33b8dcae4d1d3b3c05eef12b73dfbad33ef9a8e3ab57242b67e5
```

Insertion :

```sql
INSERT INTO api_keys (
    id,
    label,
    key_prefix,
    key_hash,
    scope,
    active
) VALUES (
    gen_random_uuid(),
    'batch emails',
    'loc_batc',
    '47e48783c49b33b8dcae4d1d3b3c05eef12b73dfbad33ef9a8e3ab57242b67e5',
    'internal:batch',
    true
);
```



RAW=loc_batch_db0fef438c2a464a84614c64e8f5447f
PREFIX=loc_batc
HASH=47e48783c49b33b8dcae4d1d3b3c05eef12b73dfbad33ef9a8e3ab57242b67e5
