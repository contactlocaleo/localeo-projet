# Epic 50 - Specification Localeo Commercant

> Consolidation de la spécification backend et de sa déclinaison Commerçant.
> Le socle commun est conservé une fois ; les précisions Commerçant sur les routes,
> champs multipart, correction, lecture d'une demande groupée et PRO-009 sont intégrées.
> Les constats OpenAPI du 4 septembre et les résultats de tests cités sont historiques :
> ils ne valent ni nouvel audit du backend courant ni preuve de déploiement.
> Cette réorganisation ne lève aucun prérequis produit ni aucun flag Finance.

## Statut et objectif

| Champ | Valeur |
| --- | --- |
| Application | Localeo Commercant |
| Epic | Epic 50 - Politique BUM et conformite fiscale |
| Statut du contrat | Backend disponible, interfaces clientes a implementer |
| Public | Commercant et collaborateurs habilites |
| Domaine principal | Finance et facturation des prestations executees |

Contrat de reference verifie le 4 septembre 2026 : OpenAPI
`1.0.0+acfeaa2`, expose sur l'environnement BackOffice de test. Les routes et
corps de requete ci-dessous reprennent ce contrat ; les structures de reponse
encore publiees sans schema sont decrites comme des attentes fonctionnelles et
doivent etre confirmees avant implementation.

Cette specification decrit le perimetre a integrer dans Localeo Commercant. Le
commercant reste l'emetteur et le responsable de ses factures de prestation.
Localeo fournit les donnees factuelles, orchestre la demande, securise le
document et peut proposer un assistant d'emission facultatif.

## Regles non negociables

- Le commercant ne qualifie, ne valide et ne requalifie jamais un coffret BUM.
- L'interface ne doit afficher aucune action `Valider BUM`, aucun diagnostic
  fiscal interne et aucun statut d'instruction reserve au BackOffice.
- Une demande de facture n'existe qu'apres validation d'une prestation.
- Le montant facture par le commercant est le brut TTC de la prestation.
- La commission Localeo est affichee separement et ne reduit pas le montant de
  la facture adressee au client.
- Le net reverse est une information de rapprochement, pas le montant facture.
- Le paiement du coffret n'est pas l'emission de la facture de prestation.
- Une facture fournie ou emise est immuable. Toute correction produit un avoir
  ou une facture corrective referencee.
- L'assistant ne choisit jamais le taux ou le traitement de TVA.
- Aucun credit d'achat B2B n'est visible ou utilisable dans cette application.

## Habilitations

Toutes les routes sont protegees par la session commercant et le scope
`commercant:validation`.

| Capacite | Commercant habilite | Autre commercant | BackOffice |
| --- | --- | --- | --- |
| Lire ses demandes | Oui | Non | Via ses outils propres |
| Changer leur statut | Oui | Non | Non dans cette application |
| Fournir une facture | Oui | Non | Non dans cette application |
| Emettre via l'assistant | Oui, si active | Non | Non |
| Consulter les factures Localeo | Oui | Non | Via ses outils propres |
| Accepter/revoquer le mandat Chorus | Oui, si active | Non | Consultation operateur separee |

Une ressource hors perimetre doit etre presentee comme introuvable. Le client
ne doit jamais essayer de contourner le cloisonnement en reutilisant un ID
recu par un autre compte.

## Navigation et ecrans

Les routes frontales ci-dessous sont proposees. Elles peuvent etre adaptees au
routeur de l'application, mais les vues et les transitions sont obligatoires.

| Route frontale proposee | Vue | Contenu attendu |
| --- | --- | --- |
| `/finance` | Accueil Finance | Compteurs par statut, demandes recentes, factures Localeo recentes |
| `/finance/demandes` | Demandes unitaires | Recherche, filtres de statut, liste et etat vide |
| `/finance/demandes/:id` | Detail unitaire | Snapshots, chronologie, actions et remise de facture |
| `/finance/demandes-groupees` | Demandes groupees | Demandes Pro/Animation et nombre de lignes |
| `/finance/demandes-groupees/:id` | Detail groupe | Lignes immuables, totaux, actions et correction |
| `/finance/factures-localeo` | Factures Localeo | Factures de commission et avoirs, telechargement |
| `/finance/chorus-pro` | Mandat Chorus | Mandat actif, preuve, perimetre et revocation |

Le menu Finance affiche un badge calcule sur les demandes `REQUESTED`. Une
notification ouvrant une demande doit mener directement au detail apres
controle de session et de perimetre.

## Parcours 1 - Traiter une demande unitaire

1. Charger `GET /protected/commercants/me/facturation/demandes`.
2. Afficher la reference, la source, la date de demande, le statut et les
   montants de rapprochement.
3. Ouvrir le detail par
   `GET /protected/commercants/me/facturation/demandes/{demandeId}`.
4. Pour `REQUESTED`, proposer `Accuser reception`.
5. Pour `ACKNOWLEDGED`, proposer `Demarrer le traitement`.
6. Pour `PROCESSING`, proposer deux modes exclusifs : deposer une facture PDF
   externe ou utiliser l'assistant lorsque celui-ci est active.
7. Apres `PROVIDED`, rendre la vue en lecture seule et afficher numero, date et
   statut de mise a disposition.
8. Pour `CANCELLED`, afficher l'etat terminal sans action de reouverture.

### Automate de statut

```text
REQUESTED -> ACKNOWLEDGED -> PROCESSING -> PROVIDED
    |              |             |
    +--------------+-------------+-> CANCELLED
```

Transitions API :

| Etat courant | Commande | Requete |
| --- | --- | --- |
| `REQUESTED` | Accuser reception | `POST .../{id}/accuser-reception` |
| `ACKNOWLEDGED` | Demarrer | `POST .../{id}/demarrer` |
| `REQUESTED`, `ACKNOWLEDGED`, `PROCESSING` | Annuler | `POST .../{id}/annuler` |
| `PROCESSING` | Fournir PDF | `POST .../{id}/facture` |

Chaque transition JSON envoie `{ "expectedVersion": version }`. En cas de
`409`, recharger la demande, expliquer qu'elle a ete modifiee et ne pas
rejouer automatiquement l'action.

### Donnees du detail

Le client consomme les champs suivants sans recalcul financier :

```json
{
  "id": "uuid",
  "reference": "...",
  "validationPrestationId": "uuid",
  "commercantId": "uuid",
  "source": "MARKETPLACE | PRO_ORDER | ANIMATION",
  "status": "REQUESTED | ACKNOWLEDGED | PROCESSING | PROVIDED | CANCELLED",
  "billingSnapshot": {},
  "prestationSnapshot": {},
  "financialSnapshot": {},
  "comment": null,
  "requestedAt": "date ISO-8601",
  "invoiceDocumentId": null,
  "invoiceNumber": null,
  "invoiceDate": null,
  "version": 1
}
```

Le panneau financier affiche, depuis `financialSnapshot`, le brut TTC de la
prestation, la commission TTC, sa ventilation HT/TVA si elle existe, et le net
reverse. Le libelle principal doit etre `Montant brut TTC a facturer`.

## Parcours 2 - Deposer une facture externe

Le formulaire envoie un `multipart/form-data` sur
`POST /protected/commercants/me/facturation/demandes/{demandeId}/facture` :

| Champ | Regle client |
| --- | --- |
| `file` | Un fichier PDF non vide, taille limite issue de la configuration |
| `invoiceNumber` | Obligatoire, valeur emise par le commercant |
| `invoiceDate` | Obligatoire, date ISO `YYYY-MM-DD` |
| `expectedVersion` | Version affichee dans le detail |

Le client verifie extension et type MIME avant envoi, sans presenter ce
controle comme une validation fiscale. Le bouton est desactive pendant
l'envoi. Un succes remplace immediatement l'ecran par l'etat `PROVIDED`.

## Parcours 3 - Utiliser l'assistant facultatif

L'assistant n'est affiche que si le produit l'autorise et si les routes ne
repondent pas `404`. Son activation depend de
`LOCALEO_FEATURE_MERCHANT_INVOICE_ASSISTANT_ENABLED=true` et de la validation
Juridica/comptable `BUM-ARB-49`.

1. Creer le brouillon avec `POST .../{id}/facture-assistee/brouillon`, puis le
   reprendre avec `GET .../{id}/facture-assistee/brouillon`.
2. Afficher et rendre editables les donnees de `draftData`.
3. Enregistrer par `PATCH .../{id}/facture-assistee/brouillon` avec
   `expectedVersion` et `invoiceData`.
4. Exiger une revue recapitulant emetteur, destinataire, lignes, dates, TVA,
   mentions, reglement par coffret et totaux.
5. Exiger une case non pre-cochee confirmant la responsabilite du commercant.
6. Emettre avec `POST .../{id}/facture-assistee/emettre` et l'action typee
   `ISSUE_MERCHANT_INVOICE`.
7. Afficher le numero attribue et permettre le telechargement du PDF.

Structure du brouillon :

```json
{
  "schemaVersion": "MERCHANT_INVOICE_DATA_2026_01",
  "issuer": {},
  "recipient": {},
  "invoiceDate": "YYYY-MM-DD",
  "currency": "EUR",
  "lines": [{
    "description": "...",
    "executionDate": "date ISO-8601",
    "quantity": 1,
    "totalIncludingTax": "...",
    "taxTreatment": null,
    "taxRate": null,
    "totalExcludingTax": null,
    "totalTax": null
  }],
  "totals": {
    "totalExcludingTax": null,
    "totalTax": null,
    "totalIncludingTax": "...",
    "amountToPay": "0.00"
  },
  "payment": {
    "method": "LOCALEO_VOUCHER",
    "status": "PAID",
    "reference": "..."
  },
  "mentions": []
}
```

L'interface ne doit ni preselectionner un taux de TVA, ni calculer un taux a
partir du TTC, ni masquer les champs encore a confirmer. La fermeture d'un
brouillon non enregistre doit demander confirmation. L'annulation utilise
`POST .../{id}/facture-assistee/annuler` avec `expectedVersion`.

Emission :

```json
{
  "expectedVersion": 3,
  "action": "ISSUE_MERCHANT_INVOICE",
  "merchantResponsibilityConfirmed": true
}
```

Correction via `POST .../{id}/facture-assistee/correction` :

```json
{
  "originalInvoiceId": "uuid",
  "correctionType": "CREDIT_NOTE | CORRECTIVE_INVOICE",
  "invoiceData": {},
  "reason": "Motif explicite",
  "idempotencyKey": "uuid-client-stable",
  "action": "ISSUE_MERCHANT_INVOICE_CORRECTION",
  "merchantResponsibilityConfirmed": true
}
```

Le telechargement utilise
`GET .../{demandeId}/facture-assistee/{factureId}/telecharger` et doit traiter
la reponse comme un blob PDF, en respectant `Content-Disposition`.

## Parcours 4 - Demandes groupees Pro et Animation

`GET /protected/commercants/me/facturation/demandes-groupees` retourne les
demandes limitees a un seul commercant, un acheteur, une devise et un snapshot
de facturation. Le detail est porte dans chaque element :

```json
{
  "id": "uuid",
  "reference": "...",
  "merchantId": "uuid",
  "status": "REQUESTED | ACKNOWLEDGED | PROCESSING | PROVIDED | CANCELLED",
  "currency": "EUR",
  "billingSnapshot": {},
  "requestSnapshot": {},
  "lines": [{
    "validationPrestationId": "uuid",
    "prestationSnapshot": {},
    "financialSnapshot": {}
  }],
  "invoiceDocumentId": null,
  "invoiceNumber": null,
  "invoiceDate": null,
  "previousRequestId": null,
  "correctionType": null,
  "correctionReason": null,
  "version": 1,
  "createdAt": "date ISO-8601"
}
```

Les transitions passent par `POST .../{id}/transition` avec `target` et
`expectedVersion`. Le depot utilise `POST .../{id}/facture`, au format
`multipart/form-data`, avec les champs obligatoires `file`, `invoiceNumber`,
`invoiceDate` et `expectedVersion`. Il accepte uniquement un PDF de 10 Mo
maximum. La vue doit afficher chaque ligne et la somme des bruts TTC, sans
fusionner les prestations ni les commercants.

Apres `PROVIDED`, une correction est initiee par
`POST .../{id}/corrections`. Le client genere une `idempotencyKey` stable par
tentative utilisateur et conserve le lien `previousRequestId` dans la
chronologie. Il ne remplace jamais visuellement le document original.

```json
{
  "correctionType": "CREDIT_NOTE | CORRECTIVE_INVOICE",
  "reason": "Motif explicite",
  "idempotencyKey": "uuid-client-stable"
}
```

Le contrat exige une cle d'idempotence de 8 a 200 caracteres et un motif non
vide limite a 1 000 caracteres.

Le backend actuel fournit `GET /protected/commercants/me/facturation/demandes-groupees/{id}`. Le détail et le rafraîchissement utilisent cet endpoint authentifié. Le service filtre simultanément l’ID et le commerçant de la session ; une demande étrangère renvoie 404. La liste ne sert pas de fallback de détail.

## Parcours 5 - Factures emises par Localeo

La vue `Factures Localeo` consomme :

- `GET /protected/commercants/me/factures-localeo` ;
- `GET /protected/commercants/me/factures-localeo/{factureId}/telecharger`.

Elle affiche les types `COMMISSION_COMMERCANT` et `AVOIR_COMMISSION`, le numero,
les dates, les totaux, le statut, la source, le lien vers la facture d'origine
et les lignes de campagne. Une facture de commission Localeo ne doit jamais
etre presentee comme la facture de prestation du client.

## Parcours 6 - Mandat Chorus Pro

Cette vue est masquee tant que
`LOCALEO_FEATURE_CHORUS_MANUAL_DEPOSIT_ENABLED=false`.

- Lire le mandat actif : `GET /protected/commercants/me/facturation/chorus-pro/mandat`.
- Accepter : `POST /protected/commercants/me/facturation/chorus-pro/mandat`.
- Revoquer : `POST /protected/commercants/me/facturation/chorus-pro/mandat/{mandatId}/revoquer`.

L'acceptation exige l'affichage du contrat versionne, la preuve documentaire et
une confirmation explicite non pre-cochee :

```json
{
  "action": "ACCEPT_CHORUS_DEPOSIT_MANDATE",
  "confirmed": true,
  "contractVersion": "version validee",
  "scope": { "publicInvoices": true },
  "proofDocumentId": "uuid"
}
```

La revocation exige le motif, `expectedVersion` et l'action
`REVOKE_CHORUS_DEPOSIT_MANDATE`. Elle ne retire ni ne modifie les preuves des
depots anterieurs.

## Donnees factuelles et profil fiscal

Localeo Commercant doit permettre au commercant de consulter les donnees
factuelles qui seront reprises dans ses factures : identite legale, adresses,
SIREN/SIRET, TVA intracommunautaire le cas echeant, regime declare, representant
et contact de facturation. Il peut signaler une correction, sans voir le
diagnostic BUM ni approuver une qualification fiscale du coffret.

**Prerequis backend restant :** aucune route commercant Epic 50 ne permet
actuellement de lire ou corriger ce profil depuis Localeo Commercant. Cette vue
ne doit pas appeler les routes BackOffice `/internal/conformite-fiscale/*`.
Avant implementation, exposer un contrat protege `me` dedie, avec version
optimiste et workflow de correction factuelle.

## Écarts OpenAPI relevés le 4 septembre — état à revalider avant intégration

Les écarts ci-dessous proviennent de la déclinaison Commerçant ; la copie backend
ne les documentait pas. Ils sont conservés comme points de vérification, sans
affirmer qu'ils subsistent dans le contrat aujourd'hui déployé.

- Les reponses `200` des routes commercant unitaires, groupees, Chorus et
  factures Localeo sont publiees avec un schema vide. Les exemples de cette
  specification ne remplacent pas un schema de reponse versionne.
- Les routes de telechargement de facture assistee et de facture Localeo sont
  annoncees en `application/json`, alors que le parcours attend un PDF. Le
  backend doit publier `application/pdf` avec un schema binaire et documenter
  `Content-Disposition` avant branchement du telechargement.
- Aucun contrat protege `me` de lecture ou correction du profil fiscal n'est
  expose ; `LC-50-07` reste bloque par ce prerequis.

## Gestion des erreurs

| HTTP | Comportement interface |
| --- | --- |
| `400` | Afficher l'erreur de fichier ou de signature PDF pres du champ |
| `401` | Expirer la session et retourner a l'authentification |
| `403` | Afficher une page d'acces refuse sans detail de ressource |
| `404` | Ressource absente ou fonction desactivee ; masquer le module concerne |
| `409` | Recharger la ressource et demander une nouvelle confirmation |
| `413` | Indiquer la taille maximale autorisee |
| `422` | Associer les erreurs de saisie aux champs concernes |
| `5xx` | Conserver le brouillon local non sensible et proposer un nouvel essai |

## Exigences UX, accessibilite et securite

- Afficher les montants avec la devise retournee, sans calcul flottant.
- Conserver les nombres monetaires sous la forme recue par l'API.
- Afficher le statut avec un libelle et du texte, jamais par la couleur seule.
- Rendre tous les formulaires utilisables au clavier et annoncer les erreurs.
- Ne pas mettre les snapshots fiscaux, documents ou IDs de demande dans des
  outils d'analytics tiers.
- Ne jamais journaliser le contenu d'un PDF, les coordonnees bancaires ou le
  snapshot complet de facturation dans le navigateur.
- Ne pas stocker les documents telecharges dans un cache applicatif persistant.
- Sur mobile, conserver le recapitulatif financier avant les actions et rendre
  la barre d'action stable sans recouvrir le contenu.

## Criteres d'acceptation

- Une demande ne peut suivre que l'automate documente.
- Un `409` ne provoque jamais un rejeu silencieux.
- Le brut TTC, la commission et le net reverse sont trois valeurs distinctes.
- Un PDF externe invalide, vide ou trop volumineux est refuse proprement.
- L'assistant n'est pas visible si son flag est inactif.
- L'emission assistee est impossible sans confirmation explicite.
- Une facture emise est en lecture seule et une correction cree un document
  reference distinct.
- Les demandes groupees affichent toutes leurs lignes et leur origine.
- Les factures de commission et leurs avoirs sont telechargeables.
- Aucun ecran ni texte ne laisse entendre que le commercant valide le BUM.
- Un utilisateur ne peut lire aucune ressource d'un autre commercant.

## Decoupage d'implementation recommande

1. `LC-50-01` : navigation Finance, listes unitaires et detail.
2. `LC-50-02` : automate, verrou optimiste et depot PDF externe.
3. `LC-50-03` : demandes groupees et corrections.
4. `LC-50-04` : factures Localeo et rapprochement commission.
5. `LC-50-05` : assistant d'emission derriere feature flag.
6. `LC-50-06` : mandat Chorus Pro derriere feature flag.
7. `LC-50-07` : profil factuel apres livraison du contrat backend `me`.
8. `LC-50-08` : tests E2E, accessibilite, erreurs et cloisonnement.

## Dependances d'activation

- `LOCALEO_FEATURE_MERCHANT_INVOICE_REQUEST_ENABLED=true` pour les demandes ;
- `LOCALEO_FEATURE_LOCALEO_INVOICING_ENABLED=true` pour les factures Localeo ;
- `LOCALEO_FEATURE_MERCHANT_INVOICE_ASSISTANT_ENABLED=true` apres validation
  de `BUM-ARB-49` pour l'assistant ;
- `LOCALEO_FEATURE_CHORUS_MANUAL_DEPOSIT_ENABLED=true` apres validation du
  mandat et recette Chorus Pro ;
- wording, documents contractuels et donnees fiscales valides par les acteurs
  indiques dans le registre d'arbitrages.

### PRO-009 — Aligner Finance sur le backend actuel
Le GET de détail groupé existe désormais et filtre l'identifiant avec le commerçant : la spécification obsolète a été corrigée, aucun fallback global n'est ajouté. Les erreurs Finance ne sont plus présentées comme des listes vides (PRO-003). Les lectures abandonnées sont annulées/ignorées et une réponse d'ancien compte ne peut remplacer le compte courant ; verrou synchrone des commandes. Les quatre flags Epic 50 sont explicitement désactivés en production avant recette/arbitrages. Validation : 6 tests Finance réussis ; test backend `test_grouped_invoice_detail.py` réussi lors de la passe sécurité (217 tests). Le statut produit de l'Epic 50 reste inchangé.


## Provenance des précisions de contrat

La version backend décrivait « créer ou reprendre le brouillon » avec `POST`.
La déclinaison Commerçant distingue la création par `POST` et la reprise par
`GET`, précise l'émission et la correction par les routes dédiées, puis ajoute
les champs multipart obligatoires et les limites d'idempotence. Cette version
plus explicite est conservée ici comme contrat documenté du 4 septembre.
Le comportement de rejeu du `POST` reste celui du backend : la distinction des
lectures frontend n'en déduit pas un changement d'idempotence. Aucun nouveau
contrat ou arbitrage fiscal n'est créé par cette fusion.
