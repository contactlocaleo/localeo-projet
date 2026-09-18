# EPIC 60 - Contrats API implementes V1

Reference executable : `app/api/erp_api.py`, `erp_schemas.py`, `erp_responses.py`
et OpenAPI genere par FastAPI. Les specifications fonctionnelles detaillees
completent ces contrats. Les identifiants sont des UUID.

## Securite et transactions

Session signee obligatoire. ADMIN global ; EXPLOITATION limite a ses communes.
Qualification fiscale, navigation avancee et mesures globales reservees a ADMIN.
Absence de session : 401 ; role/CSRF : 403 ; ressource hors perimetre : 404.
Chaque commande exige X-CSRF-Token et Idempotency-Key (ASCII visible, 1..128).
Le jeton vient du GET /internal/erp/api/contexte. La simulation ne demande
pas de cle d'idempotence. Une origine explicite differente est refusee.

Meme cle et meme commande : resultat initial, replayed=true. Cle reutilisee
avec une autre commande : 409. Version obsolete : 409. Schema invalide : 422.
Reevaluation limitee a 10/minute/acteur : 429. Les cles expirent apres 24 h.
Ecritures, versions, audit et recalcul sont transactionnels. Les reponses
contenant des donnees sont Cache-Control: no-store.

## Routes de la version livree

Historique des modeles (migration `v226_historique_modeles_prestation.sql`) :

- GET `/internal/erp/api/commercants/{mid}/modeles/{modele_id}/versions` :
  `page` / `pageSize`, versions decroissantes, `versionCourante`, `historiqueComplet`.
- GET `/internal/erp/api/coffrets/{cid}/prestations/{pid}/modele` :
  `versionRattachee`, `versionCourante`, `version` archivee ou null ;
  `copieInitiale` explicite si l'ancienne revision n'a pas ete conservee.
- Le detail coffret enrichit chaque prestation avec `modele` (id,
  versionRattachee, versionCourante), ou null pour une creation sans modele.

Les lectures respectent le perimetre ERP et les associations commercant/modele
et coffret/prestation. Aucun retour silencieux de la version courante a la
place d'une version historique manquante. Les versions sont ajoutees sans
modifier les snapshots precedents. Appliquer v226 avant le backend associe.

GET `/internal/erp/api/commercants` accepte `query` (nom uniquement), `villeId`
(UUID optionnel), `page` et `pageSize`. Les filtres nom et ville se cumulent
avec le perimetre territorial autorise. Chaque resultat expose `villeNom`
en plus de `villeId`. Une chaine UUID dans `query` est recherchee comme un nom.

Le detail commercant ERP expose `activation.profilComplet` et
`activation.blocages` (code et label des champs manquants). OnBoard expose
le meme diagnostic dans `commercant.activation`. L'activation ACTIF exige
uniquement nom, commune, type de commerce et email de contact renseignes,
recontroles au moment de l'ecriture. Elle ne valide pas le dossier OnBoard.

Le POST `/internal/erp/api/coffrets/{cid}/qualifier` utilise desormais
`action` (`VALIDER` par defaut ou `SUSPENDRE`), `verification_confirmee`
(obligatoirement true pour valider), `motif` (commentaire obligatoire),
`expected_version` (coffret) et `qualification_version` (qualification courante).
Les champs libres `qualification` et `statut` ne sont plus acceptes par ce
parcours ERP. Une validation produit MULTI_PURPOSE / VALIDATED ; la suspension
d'une BUM validee cree une version REQUALIFICATION_REQUIRED et conserve
l'historique. Les controles ADMIN, CSRF, idempotence et versions restent actifs.
Les autres API fiscales conservent leurs contrats.

Les schemas nommes ci-dessous definissent les champs, enums et limites.
Une creation de commercant/coffret reste BROUILLON. Les montants sont saisis
en centimes entiers ; les snapshots de prestations vendues sont preserves.

| Methode | Route complete | Corps Pydantic |
| --- | --- | --- |
| GET | `/internal/erp/api/contexte` | Aucun |
| GET | `/internal/erp/api/navigation` | Aucun |
| POST | `/internal/erp/api/mesures` | MesureParcoursCommande |
| GET | `/internal/erp/api/mesures` | Aucun |
| GET | `/internal/erp/api/activite` | Aucun |
| GET | `/internal/erp/api/commercants/{mid}/activite` | Aucun |
| POST | `/internal/erp/api/commercants/{mid}/notes` | NoteCommande |
| GET | `/internal/erp/api/commercants` | Aucun |
| POST | `/internal/erp/api/commercants` | CommercantCommande |
| GET | `/internal/erp/api/commercants/{mid}` | Aucun |
| PUT | `/internal/erp/api/commercants/{mid}` | ModifierCommercantCommande |
| POST | `/internal/erp/api/commercants/{mid}/statut` | StatutCommande |
| POST | `/internal/erp/api/commercants/{mid}/modeles` | ModeleCommande |
| PUT | `/internal/erp/api/commercants/{mid}/modeles/{modele_id}` | ModeleCommande |
| POST | `/internal/erp/api/commercants/{mid}/dossier/{action}` | VersionCommande |
| PUT | `/internal/erp/api/commercants/{mid}/dossier` | DossierCommande |
| POST | `/internal/erp/api/coffrets` | CoffretCommande |
| GET | `/internal/erp/api/coffrets/{cid}` | Aucun |
| PUT | `/internal/erp/api/coffrets/{cid}` | ModifierCoffretCommande |
| POST | `/internal/erp/api/coffrets/{cid}/rattachements` | RattachementCommande |
| POST | `/internal/erp/api/coffrets/{cid}/prestations` | PrestationCommande |
| PUT | `/internal/erp/api/coffrets/{cid}/prestations/{pid}` | PrestationCommande |
| POST | `/internal/erp/api/coffrets/{cid}/simuler` | VersionCommande |
| GET | `/internal/erp/api/coffrets/{cid}/fiscalite` | Aucun |
| POST | `/internal/erp/api/coffrets/{cid}/qualifier` | QualificationCommande |
| POST | `/internal/erp/api/coffrets/{cid}/publier` | VersionCommande |
| POST | `/internal/erp/api/coffrets/{cid}/retirer` | RetraitCommande |
| GET | `/internal/commercialisation/vision-360/synthese` | Aucun |
| GET | `/internal/commercialisation/vision-360/coffrets` | Aucun |
| GET | `/internal/commercialisation/vision-360/coffrets/{cid}` | Aucun |
| POST | `/internal/commercialisation/vision-360/coffrets/{cid}/reevaluer` | Aucun |
| GET | `/internal/commercialisation/vision-360/coffrets/{cid}/chronologie` | Aucun |
| GET | `/internal/commercialisation/vision-360/alertes` | Aucun |
| GET | `/internal/commercialisation/vision-360/territoires` | Aucun |

## Lecture du diagnostic

Filtres liste/synthese : villeId, typeCoffret, statutCoffret, verdict
(ALL/VENDABLE/NON_VENDABLE/INDETERMINE ; defaut NON_VENDABLE), query nom/UUID,
merchantId, code, family, blockedSinceFrom, blockedSinceTo, sort RECENT/OLDEST.
La synthese ignore seulement verdict. Page >= 1 ; pageSize 1..100, defaut 25.
Les pertes observees sont prioritaires, puis severite et anciennete choisie.

Detail : controlsPage, controlsPageSize 1..100, controlStatus facultatif.
Un controle expose code, family, severity, status PASSED/FAILED/UNKNOWN,
resourceType/resourceId, message, required, applicable, blocking, detectedAt
et treatment. Un controle inapplicable n'est pas un succes ; UNKNOWN requis
prime sur FAILED. Projection invalidee, perimee ou de version differente :
INDETERMINE avec derniere valeur connue distincte.

Le detail expose diagnosticHash, sourceRevision, controlCounts et
marketplaceExpectation (visibilite, HTTP attendu, eligibilite achat). Les
causes ne contiennent ni contacts ni identifiants/erreurs Stripe bruts.
La chronologie utilise limit 1..100 et un curseur opaque date/UUID.
Les alertes filtrent state OPEN/CLOSED/ALL, villeId, nature et code.
Les territoires filtrent villeId, typeCoffret, publication et coverage.

## Commandes et modules reutilises

Version attendue : commercant/version_referentiel, coffret/version_edition,
modele/version, prestation/version_courante, dossier Onboard/version.
Rattachement : modele_id, modele_version, expected_version du coffret,
confirmer_degradation. La copie reste independante du modele ulterieurement.

Publication : simulation cible ACTIVE puis recontrole lors de la commande.
Retrait : SUSPENDU ou ARCHIVE, avec controle des engagements. Qualification :
expected_version du coffret et qualification_version distinctes, motif requis.
Economie : moteur Epic 28 (prix, valeur intrinseque, reversements, commission
theorique, marge et minimum cible), hors frais externes et flux reels.

Documents, invitation/test portail et preparation financiere reutilisent
/internal/onboard/api/dossiers/... avec perimetre communal et CSRF. Le module
est ouvert sur /internal/erp/onboard?dossier=<uuid>. Les flags existants restent
applicables. Les mesures enregistrent UUID de parcours, type, etat et duree,
jamais le contenu saisi ; leurs agregats couvrent les 30 derniers jours.

## Batch protege

POST /protected/commercialisation/batch/reevaluer?limit=1000, scope internal:batch,
limite 1..2000. Compteurs evaluated, changed, errors, notifications. Traitement
chaque minute, transactions de 100, SKIP LOCKED, reconciliation a 15 minutes,
expiration de fraicheur a 20 minutes. Voir livraison-v1.md.
