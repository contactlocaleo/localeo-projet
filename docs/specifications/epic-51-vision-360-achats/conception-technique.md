# Conception technique - Epic 51 Vision 360 des achats

## 1. Etat et objectif

- Etat : conception technique initiale et MVP backend implementes le 25 aout 2026.
- Statut : lots `A0` a `A5` implementes ; recette runtime et mesures de performance a finaliser.
- Domaine proprietaire : `gestion_achats`.
- Surface : API interne et BackOffice Localeo.

Cette conception fournit une vue de lecture consolidee d'une commande ou d'un achat historique. Elle permet d'expliquer le parcours complet `commande -> paiement -> achats -> instances -> apres-vente`, de connaitre le cout Stripe reel et de detecter les incoherences sans creer une seconde source de verite.

## 2. Decisions structurantes

Les arbitrages `ACH360-ARB-01` a `ACH360-ARB-06` sont appliques comme invariants :

1. la racine est `CommandeAchat` lorsqu'elle existe, sinon `AchatCoffret` ;
2. l'unique paiement reussi est le paiement faisant foi ; plusieurs succes produisent une alerte critique et aucun choix silencieux ;
3. un frais Stripe absent reste `null`, puis devient une alerte apres 24 heures ;
4. paiement, frais, remboursements et frais de remboursement restent separes ; aucun net comptable consolide n'est calcule sans validation finance ;
5. les coordonnees sont masquees par defaut et leur affichage complet est reserve a `ADMIN` avec audit ;
6. le MVP est en lecture seule et pointe vers les actions metier existantes.

## 3. Architecture cible

### 3.1 Principe

La Vision 360 est une projection synchrone construite depuis les tables metier existantes. Elle ne possede ni aggregate d'ecriture, ni table `vision_360_achat`, ni cache persistant.

```text
API interne / BackOffice
          |
          v
ServiceVision360Achats
  |-- ResolveurRacineAchat
  |-- ProjectionRechercheAchats
  |-- ProjectionSyntheseAchat
  |-- ProjectionPaiementsAchat
  |-- ProjectionChronologieAchat
  `-- DetecteurAlertesAchat
          |
          v
SQLAlchemyUnitOfWork -> sources metier existantes
```

Les projections sont placees dans :

`app/application/gestion_achats/services/vision_360_achats.py`

Les schemas et routes sont places dans une API dediee :

`app/api/vision_360_achats_api.py`

Le routeur est monte sous `/internal/gestion-achats/vision-360` dans `app/main.py`. Le rendu BackOffice reste dans `app/infrastructure/admin/admin.py`, selon les conventions des autres visions 360.

### 3.2 Responsabilites

| Composant | Responsabilite |
| --- | --- |
| `ResolveurRacineAchat` | Resoudre une `root_key`, une reference d'achat ou une reference Stripe vers une racine unique et appliquer les habilitations avant chargement. |
| `ProjectionRechercheAchats` | Rechercher, filtrer, trier et paginer sans charger les collections detaillees. |
| `ProjectionSyntheseAchat` | Consolider identite, contexte, lignes, achats enfants, instances, documents et apres-vente. |
| `ProjectionPaiementsAchat` | Ordonner les tentatives, identifier le paiement faisant foi et exposer les donnees financieres sans approximation. |
| `ProjectionChronologieAchat` | Fusionner des evenements multi-sources dans un ordre stable et une pagination par curseur. |
| `DetecteurAlertesAchat` | Produire des alertes calculees, codees et testables sans les persister au MVP. |
| `ServiceSynchroniserFinancesPaiementStripe` | Completer montant brut, Balance Transaction, frais et net Stripe pour tous les parcours. Ce service est distinct de la projection. |

## 4. Racine de lecture unifiee

### 4.1 Identite stable

Chaque resultat expose :

```json
{
  "rootKey": "COMMANDE:550e8400-e29b-41d4-a716-446655440000",
  "rootType": "COMMANDE",
  "rootId": "550e8400-e29b-41d4-a716-446655440000"
}
```

Les valeurs autorisees de `rootType` sont :

- `COMMANDE` lorsque `CommandeAchatOrm` est la racine ;
- `ACHAT` pour un `AchatCoffretOrm` sans `commande_achat_id`.

Un achat enfant n'apparait pas comme une seconde racine dans la recherche par defaut. Une recherche directe par sa reference retourne la commande parente et renseigne `matchedResource` pour expliquer la correspondance.

### 4.2 Resolution

L'ordre de resolution est explicite :

1. `rootKey` typee ;
2. `reference_achat` ;
3. UUID recherche dans les deux tables ;
4. reference Stripe recherchee dans `PaiementOrm` ;
5. reference de remboursement.

Si une valeur non typee correspond a plusieurs racines, l'API repond `409 AMBIGUOUS_PURCHASE_ROOT` avec les `rootKey` candidates. Elle ne choisit jamais selon un ordre technique.

## 5. Evolution du modele de paiement

### 5.1 Lacunes constatees

`PaiementOrm` contient deja les references Stripe, `stripe_fee_amount`, `stripe_net_amount`, `commission_localeo_brute` et `commission_localeo_nette_estimee`. Il ne fige toutefois pas explicitement :

- le montant brut effectivement paye ;
- la devise retournee par Stripe ;
- la date de derniere synchronisation financiere ;
- l'etat de completude de cette synchronisation.

Le parcours unitaire enrichit deja les frais depuis la Balance Transaction. Le parcours des commandes de lots conserve les references, mais doit appeler le meme service d'enrichissement financier.

### 5.2 Colonnes ajoutees a `paiements`

| Colonne | Type | Nullabilite | Regle |
| --- | --- | --- | --- |
| `montant_brut_centimes` | `INTEGER` | nullable pour reprise historique | montant effectivement capture par Stripe, jamais deduit du net ; strictement positif lorsqu'il est connu. |
| `devise` | `TEXT` | nullable pour reprise historique | code ISO en majuscules ; `EUR` pour les flux Localeo actuels. |
| `stripe_financials_synced_at` | `TIMESTAMP` | nullable | date UTC de lecture reussie de la Balance Transaction. |
| `stripe_financials_status` | `TEXT` | non nul, defaut `PENDING` | `PENDING`, `COMPLETE`, `FAILED` ou `NOT_APPLICABLE`. |
| `stripe_financials_last_error` | `TEXT` | nullable | diagnostic interne sans secret ni payload complet. |

Contraintes :

- `montant_brut_centimes > 0` lorsqu'il n'est pas nul ;
- frais et net restent nullable tant que le statut n'est pas `COMPLETE` ;
- en statut `COMPLETE`, montant brut, devise, Balance Transaction, frais, net et date de synchronisation sont obligatoires ;
- `montant_brut_centimes = stripe_fee_amount + stripe_net_amount` pour une Balance Transaction de paiement complete, sous reserve du signe et du type Stripe verifies par le service.

### 5.3 Alimentation future

`ServiceSynchroniserFinancesPaiementStripe` recoit un `PaiementOrm` et :

1. resout le PaymentIntent puis la Charge si necessaire ;
2. recupere la Balance Transaction via le port Stripe existant ;
3. verifie devise, type et references ;
4. persiste atomiquement brut, frais, net, references et statut ;
5. journalise l'echec technique sans transformer une absence temporaire en zero.

Il est appele :

- apres validation d'un paiement unitaire ;
- apres validation d'une commande Pro ou Animation ;
- par le webhook lorsqu'une information financiere devient disponible ;
- par une reprise idempotente pour les paiements `PENDING` ou `FAILED`.

La cle d'idempotence est le `PaiementOrm.id`. Une synchronisation complete peut etre rejouee ; elle ne modifie une valeur figee que si Stripe retourne la meme Balance Transaction. Une divergence produit une alerte et un evenement d'audit technique.

### 5.4 Reprise historique

La migration ajoute les colonnes et index sans inventer les donnees manquantes :

- pour un paiement reussi unique, `montant_brut_centimes` peut etre repris depuis `CommandeAchat.montant_total_centimes` ou, pour une racine historique, depuis le montant contractuel de l'achat uniquement si la correspondance est exacte et non ambigue ;
- la devise peut etre initialisee a `EUR` pour les flux Stripe Localeo identifies ;
- frais, net et references existants sont conserves ;
- un paiement disposant de toutes les valeurs coherentes passe `COMPLETE` ;
- les autres restent `PENDING` et sont repris par le service Stripe ;
- aucune lecture du JSON Stripe historique n'est utilisee comme unique preuve lors d'une ambiguite.

Une migration SQL, proposee en prochaine version libre, ajoute egalement :

- un index sur `(status, stripe_financials_status, date_creation)` pour la reprise ;
- les index de recherche manquants sur les references metier ou Stripe identifies par `EXPLAIN ANALYZE`.

## 6. Paiement faisant foi et calculs

### 6.1 Classification des tentatives

Une tentative est classee depuis les statuts metier normalises, pas depuis un libelle affiche :

- `SUCCEEDED` : paiement Stripe confirme (`status=paid` ou equivalence centralisee) ;
- `PENDING` : confirmation ou moyen asynchrone en attente ;
- `FAILED` : echec explicite ;
- `EXPIRED` : Checkout Session expiree ;
- `UNKNOWN` : valeur non reconnue, avec alerte.

La fonction de normalisation est unique et partagee par les validations, la reconciliation et la Vision 360.

### 6.2 Selection

```text
0 succes  -> aucun paiement faisant foi
1 succes  -> paiement faisant foi
>1 succes -> aucun choix automatique + alerte ACH_PAYMENT_MULTIPLE_SUCCESSES
```

Les tentatives echouees ou expirees sont affichees, mais ne participent jamais aux indicateurs financiers.

### 6.3 Indicateurs

| Champ API | Source ou formule |
| --- | --- |
| `orderedAmountCents` | montant de la commande, ou montant contractuel de l'achat historique. |
| `paidAmountCents` | `paiement_faisant_foi.montant_brut_centimes`. |
| `stripeFeeAmountCents` | `paiement_faisant_foi.stripe_fee_amount`, nullable. |
| `stripeNetAmountCents` | `paiement_faisant_foi.stripe_net_amount`, nullable. |
| `effectiveFeeRate` | frais / brut, nullable si une valeur manque ou si brut non positif. |
| `localeoGrossCommissionCents` | snapshot du paiement, nullable. |
| `localeoEstimatedNetCommissionCents` | snapshot du paiement, avec `estimated=true`. |
| `refundedAmountCents` | somme des seuls remboursements `REMBOURSE`. |
| `refundStripeFeeAmountCents` | somme des frais connus des remboursements executes ; nullable si couverture incomplete. |

Aucun champ `accountingNetAmount` n'est expose au MVP.

## 7. Contrats API

### 7.1 Recherche

`GET /internal/gestion-achats/vision-360/achats`

Parametres :

- `query` : reference, UUID, email, telephone, entreprise ou reference Stripe ;
- `rootType`, `origin`, `customerType`, `purchaseStatus`, `paymentStatus`, `hasAlerts` ;
- `dateFrom`, `dateTo` en UTC ;
- `page` par defaut `1`, `pageSize` par defaut `25`, maximum `100` ;
- `sort` limite a `createdAt`, `paidAt`, `amount` et `severity`.

La reponse contient `items`, `page`, `pageSize`, `total`, `generatedAt`. Chaque item expose seulement les donnees necessaires a l'identification, les coordonnees masquees et le niveau d'alerte maximal.

La recherche SQL fusionne commandes et achats autonomes, applique le texte,
l'origine, le statut et les communes autorisees avant le tri et la pagination.
Elle couvre tout l'historique, sans limite implicite de 500 racines. Le tri
descendant `(createdAt, rootType, rootId)` reste stable entre les pages; `%` et
`_` saisis par l'operateur sont des caracteres litteraux.

Les alertes de la page sont une projection SQL agregee des achats enfants,
paiements, instances, documents, remboursements et communications. Les
conditions proviennent du service de domaine `conditions_alertes_achat`,
egalement utilise par le detail. La recherche execute deux SELECT pour une
page non vide, un seul pour une recherche vide ou hors pagination. Sans filtre
`hasAlerts`, seuls les faits des racines de la page sont enrichis. Avec ce
filtre, la projection est appliquee avant le COUNT et la pagination: le total
reste exact et aucune alerte ancienne n'est ecartee. Ce cas implique donc
l'agregation SQL de l'ensemble des racines candidates, sans charger leurs
details en memoire Python ni mettre en cache des donnees financieres.

### 7.2 Synthese

`GET /internal/gestion-achats/vision-360/achats/{root_key}`

Sections :

- `identity` : racine, reference, origine, contexte, dates et statuts sources ;
- `buyer` : type, organisation et coordonnees masquees ou completes selon autorisation ;
- `orderLines` : coffret, quantite, prix et montant ;
- `financialSummary` : montants distincts et completude ;
- `childPurchases` : achats enfants ;
- `instancesSummary` et liste courte des instances ;
- `afterSalesSummary` : remboursements, documents, communications et objets Epic 50 disponibles ;
- `alertsSummary` ;
- `links` : types et identifiants de ressources, le frontend construisant les URL.

Le parametre `includePersonalData=false` est disponible. `true` est accepte uniquement pour `ADMIN` et declenche l'audit de consultation.

### 7.3 Paiements

`GET /internal/gestion-achats/vision-360/achats/{root_key}/paiements`

Retourne :

- `authoritativePaymentId` nullable ;
- `financialCompleteness` : `COMPLETE`, `PENDING`, `FAILED`, `AMBIGUOUS` ou `NOT_PAID` ;
- les tentatives ordonnees par `date_creation`, puis `id` ;
- les references techniques dans un objet `stripeReferences`, reserve aux profils autorises ;
- les remboursements rattaches a chaque paiement.

### 7.4 Chronologie

`GET /internal/gestion-achats/vision-360/achats/{root_key}/chronologie`

Parametres : `cursor`, `limit` maximum `100`, `eventType`, `severity`, `dateFrom`, `dateTo`.

Curseur opaque base64url contenant `occurred_at` et une cle stable `source_type:source_id:event_code`. Tri descendant par ces deux valeurs. Le curseur est signe avec la cle applicative afin d'empecher sa modification.

La chronologie fusionne en SQL les quinze sources de dates et ne lit au plus
que `limit + 1` evenements. Chaque branche applique le curseur, les bornes
inclusives `date_from`/`date_to` facultatives et sa propre limite avant la fusion.
Les dates avec fuseau sont ramenees en UTC. Les egalites sont departagees par
la cle stable en collation `C`, comme dans le tri lexicographique historique.
Le controle territorial utilise un EXISTS SQL; il ne charge pas tous les
achats enfants pour verifier le droit de consultation. Les payloads Stripe,
corps des communications et metadonnees d'audit ne sont pas charges.

Chaque evenement contient :

- `eventCode`, `category`, `occurredAt`, `label`, `status`, `severity` ;
- `resourceType`, `resourceId` et metadonnees non sensibles ;
- `source` pour distinguer donnee metier, audit, Stripe, document ou communication.

### 7.5 Alertes

`GET /internal/gestion-achats/vision-360/achats/{root_key}/alertes`

Les alertes sont calculees a la demande et contiennent `code`, `severity`, `detectedAt`, `message`, `resourceType`, `resourceId`, `resolutionLinkType` et `resolutionResourceId`.

## 8. Taxonomie initiale des alertes

| Code | Severite | Condition |
| --- | --- | --- |
| `ACH_PAYMENT_MISSING` | `CRITICAL` | racine marquee payee sans paiement reussi. |
| `ACH_PAYMENT_MULTIPLE_SUCCESSES` | `CRITICAL` | plusieurs paiements reussis pour la meme racine. |
| `ACH_PAYMENT_AMOUNT_MISMATCH` | `CRITICAL` | brut paye different du montant commande. |
| `ACH_STRIPE_FINANCIALS_PENDING` | `WARNING` | paiement reussi depuis plus de 24 h sans donnees financieres completes. |
| `ACH_STRIPE_FINANCIALS_FAILED` | `ERROR` | derniere synchronisation Stripe en echec. |
| `ACH_UNKNOWN_PAYMENT_STATUS` | `WARNING` | statut non reconnu par la normalisation. |
| `ACH_CHILD_PURCHASE_MISSING` | `CRITICAL` | ligne payee sans achat enfant attendu. |
| `ACH_INSTANCE_COUNT_MISMATCH` | `CRITICAL` | nombre d'instances different de la quantite commandee. |
| `ACH_STATUS_INCONSISTENT` | `ERROR` | statuts commande, achat et instances incompatibles. |
| `ACH_RECONCILIATION_REQUIRED` | `ERROR` | commande `A_RECONCILIER` ou `derniere_erreur` renseignee. |
| `ACH_REFUND_FAILED` | `ERROR` | remboursement `ECHEC`. |
| `ACH_REFUND_AMOUNT_INVALID` | `CRITICAL` | remboursements executes superieurs au montant paye. |
| `ACH_REQUIRED_DOCUMENT_MISSING` | `WARNING` | document requis absent apres le delai metier. |
| `ACH_REQUIRED_NOTIFICATION_FAILED` | `WARNING` | communication obligatoire absente ou en echec. |

Les seuils temporels sont centralises dans une configuration applicative, avec 24 heures par defaut pour les finances Stripe. Ils ne sont pas codes dans le frontend.

## 9. Chronologie et sources

| Categorie | Sources |
| --- | --- |
| Commande | creation, changements de statut, paiement, reservation et derniere erreur de `CommandeAchatOrm`. |
| Achat | creation, paiement et statut de `AchatCoffretOrm`. |
| Paiement | `PaiementOrm`, `PaiementEventOrm` et evenements d'audit associes. |
| Instance | creation, activation, expiration, annulation et validations. |
| Apres-vente | remboursements, documents, demandes de facture et credits B2B lorsqu'ils existent. |
| Communication | emails, SMS et notifications associes a l'achat ou a ses instances. |
| Audit | `EvenementAuditOrm` limite aux types et identifiants de la racine. |

La projection ne lit pas tous les payloads JSON pour fabriquer une chronologie. Elle utilise d'abord les colonnes structurees et une liste blanche de metadonnees d'audit.

## 10. Securite et audit

### 10.1 Habilitations

- `ADMIN` : acces plateforme ; coordonnees completes uniquement avec `includePersonalData=true` ;
- `EXPLOITATION` : acces a la vue avec coordonnees masquees ; lorsque la racine appartient a un contexte territorial, appliquer les communes autorisees avant toute agregation ;
- autres profils : acces refuse au MVP.

La policy est appliquee dans la requete de resolution. Un identifiant direct ne permet jamais de contourner le filtre de territoire.

### 10.2 Donnees protegees

- email : deux premiers caracteres puis masquage ;
- telephone : quatre derniers chiffres ;
- aucune URL Checkout, management token, token de consultation, payload Stripe brut ou secret n'est expose ;
- les references Stripe sont visibles uniquement dans la zone technique des profils autorises ;
- les erreurs ne contiennent ni coordonnee ni payload externe.

### 10.3 Audit

Auditer :

- consultation avec coordonnees completes : `gestion_achats.vision_360.personal_data.viewed` ;
- export futur, hors MVP ;
- divergence financiere detectee lors d'une synchronisation : `gestion_achats.payment.financials.diverged` ;
- reprise Stripe manuelle executee depuis son use case existant ou futur, jamais depuis un GET.

Une consultation standard avec donnees masquees est journalisee techniquement, mais ne cree pas un evenement d'audit metier a chaque rafraichissement.

## 11. BackOffice

Deux vues SQLAdmin specifiques sont ajoutees :

- `/admin/vision-360-achats` : recherche et filtres ;
- `/admin/vision-360-achats-detail?root_key=...` : synthese avec onglets.

Onglets MVP :

1. `Synthese` ;
2. `Paiements et couts Stripe` ;
3. `Achats et instances` ;
4. `Documents et apres-vente` ;
5. `Chronologie` ;
6. `Alertes`.

La synthese affiche les montants avec leur nature explicite. `0,00 EUR` n'est jamais utilise pour une donnee financiere inconnue ; le rendu est `En attente` ou `Indisponible`. Les identifiants Stripe sont replies par defaut.

Les boutons sont des liens vers les pages existantes : reconciliation, remboursement, renvoi de communication, documents, Vision 360 Client et Vision 360 Animation. Aucun formulaire de mutation n'est implemente dans cette vue au MVP.

## 12. Performance et indexation

Objectifs mesures sur un jeu representatif :

- recherche et synthese : p95 inferieur a 500 ms ;
- paiements et alertes : p95 inferieur a 750 ms ;
- chronologie : p95 inferieur a 1 seconde pour 100 elements.

Regles :

- recherche paginee en SQL, jamais apres chargement Python ;
- chargement des collections par requetes groupees, sans N+1 ;
- agregats par racine et non sur l'ensemble du catalogue ;
- maximum 100 elements par page ;
- aucun cache au MVP pour les donnees financieres et alertes ; cache de 30 secondes acceptable uniquement pour la synthese non sensible apres mesure ;
- index ajoutes seulement apres verification des plans, en priorite sur references, FK de racine, statuts et dates.

## 13. Gestion des erreurs

| Code HTTP | Code applicatif | Cas |
| --- | --- | --- |
| `400` | `INVALID_PURCHASE_ROOT_KEY` | cle mal formee ou filtre invalide. |
| `403` | `PURCHASE_VIEW_FORBIDDEN` | role ou territoire non autorise. |
| `404` | `PURCHASE_ROOT_NOT_FOUND` | racine absente dans le perimetre autorise. |
| `409` | `AMBIGUOUS_PURCHASE_ROOT` | reference non typee correspondant a plusieurs racines. |
| `422` | `INVALID_PURCHASE_VIEW_PERIOD` | periode inverse ou trop large. |
| `500` | erreur standard correlee | erreur inattendue sans donnee sensible. |

Toutes les erreurs suivent les conventions de l'Epic 44 et retournent un `correlationId`.

## 14. Strategie de tests

### 14.1 Tests unitaires

- resolution commande, achat historique, achat enfant et reference ambigue ;
- masquage email et telephone ;
- normalisation de tous les statuts de paiement ;
- selection avec zero, un ou plusieurs succes ;
- calcul des indicateurs avec valeurs completes, nulles et remboursements ;
- chaque regle d'alerte, avec tests aux bornes du delai de 24 heures ;
- tri stable et encodage du curseur.

### 14.2 Tests d'integration

- recherche combinee et pagination ;
- commande Pro multi-lignes et lot Animation ;
- achat historique sans commande ;
- paiement echoue puis reussi ;
- deux paiements reussis ;
- paiement sans frais puis enrichissement Stripe idempotent ;
- quantite commandee differente des instances creees ;
- remboursement partiel, total et en echec ;
- chronologie multi-sources sans fuite de payload.

### 14.3 Tests de securite et contrat

- acces refuse aux profils non internes ;
- cloisonnement territorial avant agregation ;
- masquage par defaut ;
- affichage complet reserve a `ADMIN` et audite ;
- schema OpenAPI et non-regression des codes d'erreur ;
- absence de token, URL Checkout et payload Stripe dans toutes les reponses.

### 14.4 Tests de migration

- migration sur schema vide et historique ;
- reprise exacte d'un paiement unitaire et d'une commande ;
- conservation de `null` en cas ambigu ;
- execution idempotente ;
- readiness bloque si les nouvelles colonnes indispensables manquent.

## 15. Observabilite

Metriques proposees :

- `localeo_purchase_360_request_duration_seconds` par endpoint et resultat ;
- `localeo_purchase_payment_financials_pending_total` ;
- `localeo_purchase_payment_financials_sync_total` par resultat ;
- `localeo_purchase_360_alert_total` par code et severite ;
- `localeo_purchase_360_ambiguous_payment_total`.

Les logs contiennent `correlation_id`, `root_type`, `root_id`, code d'alerte et duree. Ils excluent coordonnees, payloads Stripe et tokens.

## 16. Ordre d'implementation

### Lot A0 - Contrats et fondations

- schemas API, erreurs, enums, policy d'acces et `rootKey` ;
- migration des colonnes financieres et readiness ;
- service commun de normalisation et synchronisation Stripe ;
- contrat OpenAPI et jeux de donnees de reference.

### Lot A1 - Recherche et synthese

- resolveur de racine ;
- recherche paginee ;
- synthese commande/achat ;
- premiere vue BackOffice.

### Lot A2 - Paiements et frais Stripe

- paiement faisant foi et tentatives ;
- alimentation uniforme des achats unitaires, Pro et Animation ;
- reprise idempotente des donnees manquantes ;
- onglet financier et alertes associees.

### Lot A3 - Achats et instances

- reconciliation lignes, achats enfants et instances ;
- synthese des statuts et alertes de coherence ;
- liens vers les ressources existantes.

### Lot A4 - Apres-vente

- documents, remboursements et communications ;
- branchement conditionnel des demandes de facture et credits de l'Epic 50 ;
- chronologie multi-sources.

### Lot A5 - Industrialisation

- alertes completes, audit et observabilite ;
- tests de charge, optimisation des index et documentation d'exploitation ;
- recette B2C historique, Pro et Animation.

## 17. Compatibilite avec l'Epic 50

La Vision 360 ne depend pas de l'implementation complete de l'Epic 50 pour demarrer. Les sections suivantes sont additives :

- justificatif d'acquisition BUM dans les documents ;
- demandes et factures de prestation dans l'apres-vente ;
- factures Localeo ;
- mouvements de credit d'achat B2B consommes ou generes.

Les ressources sont branchees par identifiants metier et exposees uniquement si leurs tables sont disponibles dans la version de schema requise. Une fois le lot Epic 50 deploye, son schema devient un prerequis de readiness normal ; aucun `try/except` SQL durable ne masque une migration absente.

## 18. Points non bloquants conserves

- la formule d'un eventuel net comptable apres remboursements reste hors contrat jusqu'a validation finance ;
- un dashboard agrege multi-achats pourra reutiliser les definitions de cette epic, mais constitue un besoin separe ;
- des actions directes pourront etre ajoutees apres le MVP uniquement en appelant les use cases existants avec confirmation et audit ;
- une projection analytique ou un cache persistant ne sera envisage qu'apres mesure des performances reelles.

## 19. Definition technique de termine

- les trois parcours B2C historique, Pro et Animation utilisent la racine unifiee ;
- le montant brut et les finances Stripe sont figes et synchronises de maniere idempotente ;
- plusieurs paiements reussis ne sont jamais consolides silencieusement ;
- les contrats distinguent toute valeur inconnue de zero ;
- toutes les listes sont paginees et les requetes critiques respectent leur budget ;
- les donnees personnelles, references techniques et payloads sont proteges ;
- la chronologie et les alertes sont deterministes et testees ;
- les migrations, le readiness, l'OpenAPI, les tests et la documentation d'exploitation sont livres ;
- aucune action metier n'est executee par une route GET de la Vision 360.
