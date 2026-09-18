# Contrats API cibles

> Consolidation documentaire du 18 septembre 2026 : contrat backend et compléments du portail Animation réunis. Les divergences de code HTTP de rejeu et de séquence clôture/tirage sont identifiées ci-dessous ; la consolidation ne les arbitre pas.

## Conventions

- Surface partenaire : `/protected/animation-locale`.
- Authentification et tenant : session Animation existante.
- Permission d'initialisation : `animation:modifier`.
- Permission de publication : `animation:publier`.
- `Idempotency-Key` obligatoire sur toute commande financière.
- Montants en centimes entiers et devise ISO `EUR` ; aucun `float` monétaire.
- Les lignes et prix sont recalculés depuis la configuration courante et le catalogue. Le frontend ne fournit pas de montant faisant autorité.
- Les URLs de retour Stripe proviennent de la configuration backend.
- Le MVP accepte uniquement `EUR`, au maximum 20 lignes et 100 instances par commande, dans la limite du plafond monétaire configuré.

## Configuration backend

| Clé | Rôle |
|---|---|
| `LOCALEO_ANIMATION_LOTS_CHECKOUT_SUCCESS_URL` | Template absolu de retour après checkout, contenant `{animation_id}` et `{commande_id}`. |
| `LOCALEO_ANIMATION_LOTS_CHECKOUT_CANCEL_URL` | Template absolu de retour après annulation, contenant `{animation_id}` et `{commande_id}`. |
| `LOCALEO_ANIMATION_LOTS_MAX_AMOUNT_CENTS` | Plafond strictement positif du total d'une commande en centimes ; valeur fixée avec finance/risque avant production. |

Les deux URLs sont validées au démarrage, ne viennent jamais du navigateur et peuvent varier par environnement. Le retour navigateur n'est pas une preuve de paiement.

## Créer ou rejouer la commande

```http
POST /protected/animation-locale/animations/{animation_id}/commande-lots
Idempotency-Key: animation:{animation_id}:lots:v{configuration_version}
```

Payload minimal recommandé :

```json
{
  "acheteur": {
    "raison_sociale": "Partenaire Animation",
    "nom_contact": "Jean Dupont",
    "email": "gestionnaire@example.fr",
    "telephone": "+33600000000",
    "adresse_facturation": {
      "ligne1": "1 rue Locale",
      "code_postal": "33360",
      "ville": "Latresne",
      "pays": "FR"
    }
  }
}
```

**Champ présent dans la source Animation :** l’exemple reprend `acheteur.raison_sociale`. Son absence dans l’exemple backend ne suffit pas à établir s’il est obligatoire ; ce point doit être vérifié dans le contrat API effectif.

Les lots ne sont pas répétés dans le payload : le backend lit la version courante de la configuration afin d'éviter un second contrat concurrent.

**Divergence de contrat à vérifier :** la source backend décrit une réponse `201`, y compris lors d’un rejeu signalé par `idempotent_replay` ; la source Animation décrit `201` puis `200` pour le rejeu. L’exemple de corps ci-dessous est commun, mais aucun code HTTP de rejeu n’est nouvellement arbitré par la fusion.

```json
{
  "commande_id": "uuid",
  "animation_id": "uuid",
  "configuration_version": 3,
  "statut": "PAIEMENT_EN_COURS",
  "montant_total_centimes": 19500,
  "devise": "EUR",
  "checkout_url": "https://checkout.stripe.com/c/pay/...",
  "lignes": [
    {
      "ordre": 1,
      "coffret_id": "uuid",
      "libelle": "Coffret découverte",
      "prix_unitaire_centimes": 7500,
      "quantite": 2,
      "montant_ligne_centimes": 15000,
      "instances_reservees": 0
    }
  ],
  "idempotent_replay": false
}
```

## Consulter l'état financier

```http
GET /protected/animation-locale/animations/{animation_id}/commande-lots
```

La réponse expose :

- statut agrégé ;
- références métier, jamais les secrets Stripe ;
- dates de création, paiement et réservation ;
- total et lignes snapshotées ;
- quantités configurées, payées, matérialisées, réservées et attribuées ;
- actions autorisées et blocages ;
- incident de réconciliation avec code public assaini.
- documents disponibles, dont le reçu consolidé et le dossier de facturation.

Exemple d'action :

```json
{
  "code": "ATTENDRE_CONFIRMATION",
  "libelle": "Confirmation Stripe en cours",
  "autorisee": false
}
```

## Reprendre après échec ou expiration

```http
POST /protected/animation-locale/animations/{animation_id}/commande-lots/{commande_id}/reprendre
Idempotency-Key: animation:{animation_id}:commande:{commande_id}:reprise:{numero}
```

La reprise crée une nouvelle session Stripe sur la même commande immuable uniquement si aucun paiement n'est confirmé. Elle ne crée pas une seconde commande ni de nouvelles lignes.

## Validation de publication

Le contrat existant :

```http
GET /protected/animation-locale/animations/{animation_id}/validation-publication
```

ajoute une erreur stable lorsque la commande n'est pas en `INSTANCES_RESERVEES` :

```json
{
  "valide": false,
  "erreurs": ["PAIEMENT_LOTS_INCOMPLET"],
  "actions_requises": [
    {
      "code": "PAYER_COMMANDE_LOTS",
      "commande_id": "uuid",
      "quantite_attendue": 3,
      "quantite_reservee": 0
    }
  ]
}
```

La commande de publication refait ce contrôle sous transaction ; le frontend ne fait jamais autorité.

## Documents accessibles depuis l'animation

```http
GET /protected/animation-locale/animations/{animation_id}/commande-lots/{commande_id}/documents
GET /protected/animation-locale/animations/{animation_id}/commande-lots/{commande_id}/documents/{document_id}/telecharger
```

La collection distingue explicitement `RECU_PAIEMENT_CONSOLIDE`, les factures par achat enfant et commerçant, et la facture Localeo lorsque celle-ci est applicable. Le reçu n'est jamais présenté comme une facture fiscale. Seuls les documents de la commande payée appartenant au tenant de l'animation sont retournés ; le téléchargement est authentifié, audité et ne révèle aucun chemin de stockage.

La fiche Animation consomme ce contrat pour afficher l'action `Consulter la facture des lots`. Si plusieurs documents fiscaux existent, l'action ouvre le dossier de facturation ou télécharge son archive plutôt que de présenter artificiellement une facture unique.

## Annulation et remboursement

Le MVP expose uniquement l'annulation avec remboursement total avant publication et tant qu'aucune instance n'est activée :

```http
POST /protected/animation-locale/animations/{animation_id}/commande-lots/{commande_id}/annuler
```

Le payload contient un motif stable et un commentaire optionnel. Un `202` peut être utilisé si le remboursement Stripe est asynchrone. Toute demande sur une commande publiée, attribuée ou partiellement activée renvoie `409` au MVP. Aucun remboursement partiel n'est exposé.

## Retrait du contrat par ligne

Le financement par ligne n'étant pas en production, les endpoints suivants sont retirés du contrat Animation au profit de la commande consolidée :

```http
GET /protected/animation-locale/animations/{animation_id}/lots/financements
POST /protected/animation-locale/animations/{animation_id}/lots/{lot_ordre}/paiement/initialiser
```

Il n'existe ni fallback, ni dépréciation longue, ni reprise de données historiques `LOT_ANIMATION` pour ce mode.

## Clôture et attribution

**Divergence de séquence à conserver dans la revue de contrat :**

- La source backend et son amendement `PLOT-ARB-16` du 26 août décrivent une clôture qui fige les éligibles sous transaction, suivie du tirage créant un gain principal pour chaque lot acheté.
- La source Animation décrit un contrôle d’attribution de tous les lots avant clôture, avec `409 LOTS_ACHETES_NON_ATTRIBUES`, `quantite_achetee` et `quantite_attribuee`.

Ces descriptions ordonnent différemment clôture et tirage ; la consolidation ne choisit pas une nouvelle règle. Dans les deux sources, `quantite_envoyee` reste exposé pour le suivi et l’envoi demeure distinct de l’attribution.

## Réponses modélisées

Chaque réponse JSON possède un `response_model` dédié dans OpenAPI. Les collections de dictionnaires libres sont exclues pour les lignes, actions, incidents et projections financières. Les erreurs conservent le contrat commun avec `detail`, `correlationId`, `request_id` et, lorsque pertinent, un `code` métier stable.

## Correctif ANIM-002 — clés des opérations de paiement

Les reprises et annulations utilisent une clé opaque UUID (36 caractères), stable
pour une même tentative. Les identifiants d'animation et de commande restent dans
la route et la clé de stockage locale ; ils ne sont pas concaténés au header.
Le contrat serveur reste `8 <= len(Idempotency-Key) <= 128`.


## Correctifs de préproduction

Consulter les [contrats corrigés ANIM](../securisation-production/contrats-animation.md) pour les seuils, dates, crédit, rejeu et suivi des opérations.
