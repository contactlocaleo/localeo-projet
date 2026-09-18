# Epic 7. Tokens de consultation achat et coffret instance

## Statut

`Termine`

## Objectif

Securiser la consultation du detail d'un achat et d'une `CoffretInstance` via des tokens opaques dedies, distincts des QR codes metier et distincts entre niveau achat et niveau instance.

## Problemes a resoudre

- Un acheteur professionnel doit pouvoir consulter et piloter son achat de facon securisee sans compte utilisateur.
- Un beneficiaire d'une `CoffretInstance` doit pouvoir consulter uniquement son instance sans acceder au reste de l'achat.
- Le `qr_token` metier d'une `CoffretInstance` ne doit pas servir de jeton de consultation.
- Le modele actuel porte un `management_token` au niveau achat, mais pas encore de token dedie a la consultation d'une `CoffretInstance`.

## Perimetre

- Maintien du `management_token` au niveau `AchatCoffret`.
- Ajout d'un `consultation_token` au niveau `CoffretInstance`.
- Persistance uniquement du hash des tokens.
- Gestion du TTL et de la revocation.
- Protection des endpoints de consultation concernes.

## Hors perimetre

- Authentification par compte utilisateur.
- Reutilisation du `qr_token` comme jeton de consultation.
- Partage d'un meme token entre achat et `CoffretInstance`.

## User Stories

### `PRD-026` Consulter un achat via un management token

- En tant qu'acheteur professionnel, je veux consulter le detail d'un achat via un `management_token` dedie afin d'acceder de facon securisee aux informations de gestion de mon achat.
- Statut : `Termine`

Critères d'acceptation :
- le detail d'un achat est refuse sans `management_token` valide ;
- un token expire ou revoque est refuse ;
- le token achat ne donne acces qu'a l'achat cible.

### `PRD-027` Consulter une coffret instance via un consultation token

- En tant que beneficiaire d'une `CoffretInstance`, je veux consulter le detail de mon coffret via un `consultation_token` dedie afin d'acceder uniquement a mon instance.
- Statut : `Termine`

Critères d'acceptation :
- le detail d'une `CoffretInstance` est refuse sans `consultation_token` valide ;
- un token expire ou revoque est refuse ;
- le token ne donne acces qu'a la `CoffretInstance` cible ;
- le token ne permet pas d'acceder aux autres `CoffretInstances` du meme achat.
- le token permet aussi de consulter le statut des prestations associees a cette `CoffretInstance`.

### `PRD-028` Generer et stocker les tokens de consultation

- En tant que systeme, je veux generer et stocker de facon securisee les tokens de consultation achat et coffret instance afin de proteger les acces sans compte utilisateur.
- Statut : `Termine`

Critères d'acceptation :
- les tokens bruts sont generes de facon aleatoire ;
- seul le hash est stocke ;
- les metadonnees de creation, expiration et revocation sont persistées ;
- la verification se fait par comparaison du hash.

### `PRD-029` Revoquer un consultation token de coffret instance

- En tant qu'admin, je veux pouvoir revoquer un `consultation_token` de `CoffretInstance` afin de couper un acces devenu indesirable ou obsolete.
- Statut : `Termine`

Critères d'acceptation :
- une action d'administration permet de revoquer le token ;
- un token revoque ne permet plus la consultation ;
- la revocation est tracable.

## Regles de gestion

- Le `management_token` reste porte par `AchatCoffret`.
- Le `consultation_token` est porte par `CoffretInstance`.
- Le `consultation_token` protege la consultation du detail de la `CoffretInstance` et du statut des prestations associees.
- Le `qr_token` ne doit jamais etre reutilise comme token de consultation.
- Les tokens sont des tokens opaques aleatoires.
- Les tokens bruts ne sont jamais stockes en base.
- Les tokens sont verifies par hash.
- Les tokens portent un TTL explicite.
- Le `consultation_token` expire a la date d'expiration de la `CoffretInstance`, majoree d'un nombre de jours configurable.
- Les tokens peuvent etre revoques.
- Le `consultation_token` d'une `CoffretInstance` ne doit jamais permettre la consultation d'un autre objet.
- Si la `CoffretInstance` est rattachee a un achat `PARTICULIER`, le detail de consultation peut inclure les informations de l'achat utiles au beneficiaire.
- Si la `CoffretInstance` est rattachee a un achat `PROFESSIONNEL`, aucune information globale de l'achat ne doit etre exposee via le `consultation_token` de la `CoffretInstance`.
- Les APIs backend attendent le `management_token` et le `consultation_token` dans l'entete `Authorization`.
- Les liens email de consultation achat et `CoffretInstance` pointent vers le front applicatif avec le token en query param.
- Le front transforme ensuite le token recu en query param en entete `Authorization` pour les appels backend.

## Impacts de modele recommandes

### `AchatCoffret`

Le modele actuel conserve :
- `management_token_hash`
- `management_token_created_at`
- `management_token_expires_at`
- `management_token_revoked_at`

### `CoffretInstance`

Ajouter :
- `consultation_token_hash`
- `consultation_token_created_at`
- `consultation_token_expires_at`
- `consultation_token_revoked_at`

## Use cases recommandes

- `GenererConsultationTokenCoffretInstance`
- `VerifierConsultationTokenCoffretInstance`
- `RevoquerConsultationTokenCoffretInstance`
- `ConsulterDetailCoffretInstanceParToken`

## APIs candidates

- `GET /achats/{achat_id}`
  Protection : `management_token`
  Transport backend : `Authorization`
  Transport lien front : `?management_token=...`

- `GET /coffrets-instances/{coffret_instance_id}`
  Protection : `consultation_token`
  Transport backend : `Authorization`
  Transport lien front : `?consultation_token=...`

Ou variante si on veut expliciter la destination :
- `GET /coffrets-instances/{coffret_instance_id}/detail`

- `GET /coffrets-instances/{coffret_instance_id}/prestations`
  Protection : `consultation_token`
  Transport backend : `Authorization`

## Design cible d'implementation

### Endpoints cibles

- `GET /achats/{achat_id}`
  - protection : `management_token`
  - usage : consultation et gestion d'un achat

- `GET /coffrets-instances/{coffret_instance_id}`
  - protection : `consultation_token`
  - usage : consultation detaillee d'une `CoffretInstance`

- `GET /coffrets-instances/{coffret_instance_id}/prestations`
  - protection : `consultation_token`
  - usage : consultation du statut des prestations associees

### Use cases cibles

- `GenererConsultationTokenCoffretInstance`
  - genere le token initial ;
  - calcule son expiration ;
  - persiste le hash et les metadonnees.

- `VerifierConsultationTokenCoffretInstance`
  - verifie presence, validite, expiration et revocation ;
  - retourne la `CoffretInstance` autorisee.

- `ConsulterDetailCoffretInstanceParToken`
  - retourne le detail de la `CoffretInstance` ;
  - inclut les informations d'achat uniquement si l'achat source est `PARTICULIER` ;
  - retourne `Information de l'achat non disponible` si l'achat source est `PROFESSIONNEL` et que ces informations sont demandees.

- `ListerPrestationsCoffretInstanceParToken`
  - retourne la liste des prestations associees a la `CoffretInstance` ;
  - retourne leur statut courant ;
  - peut inclure la date de validation si disponible.

- `RegenererConsultationTokenCoffretInstance`
  - revoque automatiquement l'ancien token ;
  - genere le nouveau token ;
  - renvoie le mail de consultation ;
  - est reserve a l'administration.

- `RevoquerConsultationTokenCoffretInstance`
  - revoque explicitement le token courant ;
  - est reserve a l'administration.

### Helpers securite cibles

Module recommande :
- `app/security/consultation_token.py`

Helpers recommandes :
- `hash_consultation_token(raw_token: str) -> str`
- `extract_consultation_token_from_authorization(...)`
- `require_consultation_token_for_coffret_instance(...)`

### Payload cible detail coffret instance

Le payload recommande contient :
- `coffret_instance_id`
- `statut`
- `coffret_nom`
- `date_activation`
- `date_expiration`
- `achat`
  - renseigne uniquement si l'achat source est `PARTICULIER`
  - sinon message : `Information de l'achat non disponible`

### Payload cible prestations coffret instance

Chaque element recommande contient :
- `statut_prestation_coffret_instance_id`
- `prestation_id`
- `libelle`
- `description`
- `statut`
- `date_validation`

## Regles de cycle de vie recommandees

- generation du `management_token` a la validation du paiement pro ;
- generation du `consultation_token` a l'activation d'une `CoffretInstance` ;
- generation immediate du `consultation_token` pour une `CoffretInstance` particulier deja active ;
- expiration du `consultation_token` a `coffret_instance.date_expiration + extension configurable` ;
- revocation automatique de l'ancien `consultation_token` lors d'une regeneration ;
- renvoi d'un nouveau mail de consultation lors d'une regeneration ;
- regeneration disponible uniquement en administration depuis le detail de la `CoffretInstance` ;
- possibilite de revocation admin.

## Specification technique d'implementation

### 1. Generation

- le `management_token` achat conserve la strategie actuelle ;
- le `consultation_token` de `CoffretInstance` est un token opaque aleatoire ;
- generation recommandee : `secrets.token_urlsafe(32)` ;
- le token brut n'est utilise que :
  - au moment de construire le lien email ;
  - ou au moment de le retourner a un appel interne de generation.

### 2. Hash et stockage

- le hash recommande est `SHA-256` ;
- seul le hash est persiste en base ;
- la verification se fait par comparaison du hash du token recu avec le hash stocke ;
- la comparaison doit etre faite avec une comparaison resistante au timing quand c'est applicable.

### 3. Persistance

#### `AchatCoffret`

Le modele existant est conserve :
- `management_token_hash`
- `management_token_created_at`
- `management_token_expires_at`
- `management_token_revoked_at`

#### `CoffretInstance`

Ajouter :
- `consultation_token_hash`
- `consultation_token_created_at`
- `consultation_token_expires_at`
- `consultation_token_revoked_at`

### 4. Configuration

Ajouter une configuration dediee pour la prolongation de consultation apres expiration du coffret, par exemple :
- `LOCALEO_COFFRET_INSTANCE_CONSULTATION_TOKEN_EXTENSION_DAYS`

Le TTL effectif du `consultation_token` est calcule ainsi :
- `consultation_token_expires_at = coffret_instance.date_expiration + extension_configurable`

Le TTL du `management_token` achat conserve sa configuration actuelle.

### 5. Helpers techniques recommandes

Ajouter un module dedie, par exemple :
- `app/security/consultation_token.py`

Avec au minimum :
- `hash_consultation_token(raw_token: str) -> str`
- `validate_consultation_token_for_coffret_instance(coffret_instance_id: str, raw_token: str) -> bool`
- `require_consultation_token_for_coffret_instance(...)`

### 6. Use cases recommandes

#### `GenererConsultationTokenCoffretInstance`

Responsabilites :
- generer un token brut ;
- calculer son hash ;
- renseigner creation, expiration, revocation ;
- persister les metadonnees ;
- retourner le token brut au flux appelant.

#### `RegenererConsultationTokenCoffretInstance`

Responsabilites :
- revoquer automatiquement l'ancien token ;
- generer un nouveau token brut ;
- recalculer son hash et ses metadonnees ;
- persister le nouveau token ;
- declencher le renvoi du mail de consultation ;
- etre utilise uniquement par une action admin sur le detail de la `CoffretInstance`.

#### `VerifierConsultationTokenCoffretInstance`

Responsabilites :
- charger la `CoffretInstance` ;
- verifier presence du hash ;
- verifier absence de revocation ;
- verifier non-expiration ;
- verifier correspondance du hash ;
- retourner le detail utile a la consultation.

#### `RevoquerConsultationTokenCoffretInstance`

Responsabilites :
- charger la `CoffretInstance` ;
- verifier qu'un token existe ;
- renseigner `consultation_token_revoked_at` ;
- tracer la revocation.

#### `ConsulterDetailCoffretInstanceParToken`

Responsabilites :
- verifier le `consultation_token` ;
- retourner le detail de la `CoffretInstance` autorisee ;
- retourner aussi le statut des prestations associees a la `CoffretInstance` ;
- inclure les informations d'achat uniquement si l'achat source est de type `PARTICULIER` ;
- exclure les informations globales d'achat si l'achat source est de type `PROFESSIONNEL` ;
- ne jamais exposer les autres `CoffretInstances` du meme achat.

### 7. Endpoints recommandes

#### Consultation achat

- `GET /achats/{achat_id}`
- protection : `management_token`
- transport backend : `Authorization`
- transport du lien email vers le front :
  - `?management_token=...`

#### Consultation coffret instance

- `GET /coffrets-instances/{coffret_instance_id}`
- ou `GET /coffrets-instances/{coffret_instance_id}/detail`
- transport backend : `Authorization`
- transport du lien email vers le front :
  - `?consultation_token=...`

#### Consultation des prestations d'une coffret instance

- `GET /coffrets-instances/{coffret_instance_id}/prestations`
- protection : `consultation_token`
- transport backend : `Authorization`

### 8. Strategie front / email recommandee

- les mails contiennent un lien front avec le token approprie en query param ;
- le front peut ouvrir directement la page a partir de ce lien ;
- le front lit le token ;
- le front appelle ensuite le backend avec `Authorization` ;
- le front peut retirer ensuite le token de l'URL navigateur ;
- il n'y a pas de support backend cible pour un `management_token` ou un `consultation_token` en query param.

### 9. Erreurs metier / techniques attendues

- `Consultation token missing`
- `Consultation token unavailable`
- `Consultation token invalid`
- `Token expire`
- `Token revoque`
- `Coffret instance introuvable`
- `Information de l'achat non disponible`

### 10. Surface SQLAdmin recommandee

Ajouter sur la vue detail `CoffretInstance` :
- etat du `consultation_token` ;
- dates de creation / expiration / revocation ;
- action de regeneration ;
- action de revocation.

### 11. Impacts email recommandes

- les emails de consultation / activation de `CoffretInstance` peuvent embarquer le lien de consultation base sur `consultation_token` ;
- les emails achat pro conservent le lien base sur `management_token` pour la gestion achat ;
- le `qr_token` ne doit jamais etre presente comme mecanisme de consultation detaillee.

### 12. Ordre d'implementation recommande

1. Ajouter les champs de persistance `consultation_token_*` sur `CoffretInstance`.
2. Ajouter la config TTL dediee.
3. Ajouter les helpers de hash / verification.
4. Implementer `GenererConsultationTokenCoffretInstance`.
5. Brancher la generation au bon moment metier.
6. Implementer `VerifierConsultationTokenCoffretInstance`.
7. Implementer `RegenererConsultationTokenCoffretInstance`.
8. Exposer l'endpoint de consultation `CoffretInstance` protege.
9. Ajouter l'action admin de regeneration / revocation SQLAdmin.
10. Mettre a jour les templates email et la documentation.

## Tickets techniques proposes

1. Ajouter les champs de persistance `consultation_token_*` sur `CoffretInstance`.
2. Introduire les helpers de hash et verification pour le `consultation_token`.
3. Generer le `consultation_token` aux moments metier appropries.
4. Proteger la consultation detaillee d'une `CoffretInstance` par `consultation_token`.
5. Ajouter la regeneration admin du `consultation_token` sur le detail `CoffretInstance`, avec revocation automatique de l'ancien token et renvoi du mail.
6. Ajouter la revocation admin du `consultation_token` dans SQLAdmin.
7. Documenter les nouveaux flux de consultation securisee.

## Decisions a instruire

- format final des endpoints de consultation `CoffretInstance` ;

## MARKET-002 — Retour de paiement

Acces de statut dedie a duree bornee, distinct des capacites de gestion et consultation. Voir [contrat](../../specifications/securisation-production/corrections-marketplace-2026-09-06.md).
