# Epic 50 - Specification Localeo Marketplace

## Statut et objectif

| Champ | Valeur |
| --- | --- |
| Application | Localeo Marketplace B2C et parcours Pro |
| Epic | Epic 50 - Politique BUM et conformite fiscale |
| Statut du contrat | Backend principal disponible, un acces justificatif reste a exposer |
| Public | Visiteur, acheteur particulier, beneficiaire et acheteur Pro |
| Domaines | Catalogue, achat, justificatif, facture apres execution, credit B2B Pro |

La Marketplace doit vendre uniquement les coffrets autorises par la politique
BUM, expliquer correctement la promesse achetee, remettre un justificatif
d'acquisition et permettre la demande de facture de prestation apres execution.
Le parcours Pro ajoute les demandes groupees et le credit d'achat B2B.

## Principes produit obligatoires

- Seuls les coffrets `MULTI_PURPOSE / VALIDATED` sont commercialisables lorsque
  le garde de publication BUM est actif.
- Le frontend n'interprete jamais lui-meme `SOLO` ou `MULTI` comme `BUM` ou
  `BUU` et n'affiche pas le diagnostic fiscal.
- Une fiche distingue la promesse garantie des exemples de prestations
  indicatifs.
- A l'achat, Localeo remet un justificatif d'acquisition BUM, pas une facture
  du commercant pour les prestations sous-jacentes.
- La facture de prestation ne peut etre demandee qu'apres validation de la
  prestation concernee.
- Un achat Pro peut produire plusieurs factures, une par commercant.
- Le credit d'achat est reserve au parcours Pro. Il est non transferable et
  non remboursable en argent ; il ne doit jamais apparaitre dans le B2C.
- Une facture fournie reste immuable. Une correction est un document distinct
  reference a l'original.

## Segmentation des parcours

| Capacite | Visiteur | Particulier/beneficiaire | Acheteur Pro |
| --- | --- | --- | --- |
| Consulter le catalogue | Oui | Oui | Oui |
| Acheter un coffret | Oui | Oui | Oui |
| Consulter un coffret emis | Non | Avec token d'activation | Avec token de gestion |
| Demander une facture unitaire | Non | Oui | Oui si parcours instance |
| Demander des factures groupees | Non | Non | Oui |
| Consulter/utiliser le credit | Non | Non | Oui, apres code + OTP |

Le type de parcours est derive de `type_client`, jamais d'un simple choix
visuel non persiste. Les valeurs attendues sont notamment `PARTICULIER` et le
type professionnel accepte par le backend existant.

## Navigation et ecrans

| Route frontale proposee | Vue | Fonction |
| --- | --- | --- |
| `/coffrets` | Catalogue | Lister uniquement les offres exposees par l'API |
| `/coffrets/:id` | Fiche coffret | Promesse, contenu indicatif, mention et achat |
| `/checkout/:coffretId` | Achat | Coordonnees, type client, credit Pro et paiement |
| `/achat/:achatId` | Detail achat | Instances, paiement, justificatif et demandes Pro |
| `/coffret/:instanceId` | Detail beneficiaire | Prestations, progression et demandes unitaires |
| `/coffret/:instanceId/facturation` | Facturation beneficiaire | Profil, eligibilite, demande et documents |
| `/pro/credit` | Credit d'achat | Authentification, solde, lots et historique |

Les URLs protegees doivent etre ouvertes seulement apres resolution du token
associe. Un token ne doit jamais etre envoye a un outil de mesure d'audience.

## Fonction 1 - Catalogue conforme BUM

Routes :

- `GET /public/commercialisation/types-coffrets` ;
- `GET /public/commercialisation/coffrets` ;
- `GET /public/commercialisation/coffrets/du-moment` ;
- `GET /public/commercialisation/coffrets/{coffretId}`.

Le client ne doit pas recreer le predicat de vendabilite. Il affiche uniquement
les objets retournes. Une fiche deja ouverte qui devient non eligible peut
repondre `404` ; le client revient au catalogue avec un message neutre indiquant
que l'offre n'est plus disponible.

Champs contractuels a rendre :

```json
{
  "promesse_garantie": "Ce qui est contractuellement acquis",
  "contenu_indicatif": "Exemples susceptibles d'evoluer",
  "nature_contenu_prestations": "INDICATIVE",
  "mention_avant_achat": "Mention validee par Juridica",
  "mention_version": "version"
}
```

Regles d'affichage :

- `promesse_garantie` est la proposition principale de la fiche ;
- les prestations sont regroupees sous un libelle explicite `Exemples de
  prestations` lorsque `nature_contenu_prestations=INDICATIVE` ;
- `mention_avant_achat` est visible avant le bouton de confirmation, sans etre
  enfouie dans une infobulle ;
- `mention_version` est conservee avec les donnees du checkout pour la trace
  fonctionnelle, sans etre mise en avant pour l'utilisateur ;
- le client ne complete pas un champ contractuel absent avec un texte invente.

## Fonction 2 - Initialiser et terminer l'achat

L'initialisation appelle
`POST /public/gestion-achats/paiements/initialiser`. Les donnees sont des
parametres de requete selon le contrat backend actuel.

| Parametre | B2C | Pro | Regle |
| --- | --- | --- | --- |
| `coffret_id` | Requis | Requis | ID de la fiche chargee |
| `email_client` | Requis | Requis | Email de contact/facturation |
| `telephone_client` | Requis | Requis | Format accepte par le backend |
| `type_client` | `PARTICULIER` | Valeur Pro | Verrouille le parcours |
| `quantite` | Requis | Requis | Entier positif |
| `nom_entreprise` | Non | Requis | Identite acheteur |
| `nom_contact` | Non | Requis | Contact acheteur |
| `siret` | Non | Requis | 14 chiffres normalises |
| `credit_terms_accepted` | Jamais | Si credit utilise | Doit etre explicite |
| `credit_terms_version` | Jamais | Si credit utilise | Version chargee par API |
| `localeo_live_installation_id` | Facultatif | Facultatif | Raccordement Live autorise |

Headers :

- `Idempotency-Key` genere une fois au debut de la tentative et reutilise en
  cas de reprise identique ;
- `X-Localeo-Credit-Session` contient la session Pro seulement si le credit est
  applique ;
- `X-Localeo-Live-Secret` accompagne `localeo_live_installation_id` ;
- les secrets ne sont jamais ajoutes aux URLs.

Reponse utile :

```json
{
  "achat_id": "uuid",
  "checkout_url": "https://... ou null",
  "type_client": "...",
  "quantite": 1,
  "nom_entreprise": null,
  "nom_contact": null,
  "idempotent_replay": false,
  "credit_applique_centimes": 0,
  "montant_stripe_centimes": 10000
}
```

Si `checkout_url` est renseignee, rediriger vers Stripe. Si elle vaut `null`,
le credit couvre 100 % du total : afficher directement l'etat de confirmation
et interroger le detail d'achat, sans simuler un passage Stripe.

Un `409` de prix, de version, d'idempotence ou d'eligibilite impose de recharger
la fiche et le recapitulatif avant une nouvelle confirmation.

## Fonction 3 - Justificatif d'acquisition

Apres confirmation du paiement, le parcours affiche :

- le statut de la commande ;
- la repartition argent/credit pour un achat Pro ;
- le libelle `Justificatif d'acquisition d'un bon a usages multiples` ;
- la mention selon laquelle le document n'est pas la facture des prestations ;
- un bouton de telechargement du document versionne.

Le justificatif conserve total de commande, credit utilise, paiement Stripe,
references d'achat et wording approuve. Il ne doit pas afficher une TVA
reconstituee sur les prestations sous-jacentes.

**Prerequis backend restant :** le document est genere et joint a l'email,
mais aucune route Marketplace securisee ne liste ou telecharge actuellement
`DocumentAchatCoffretOrm`. Avant d'implementer le bouton, exposer une liste et
un telechargement proteges par token de gestion ou d'activation. Les routes
`/internal/*` et l'API documentaire generique ne sont pas des solutions de
contournement acceptables.

## Fonction 4 - Detail d'achat et d'instance

Le detail Pro s'appuie sur les routes existantes :

- `GET /protected/gestion-achats/achats/{achatId}` ;
- `GET /protected/gestion-achats/achats/{achatId}/coffrets-instances` ;
- `GET /protected/gestion-achats/achats/{achatId}/coffrets-instances/{instanceId}` ;
- `GET /protected/gestion-achats/achats/{achatId}/coffrets-instances/{instanceId}/prestations`.

Le token de gestion est transmis par `Authorization: Bearer <token>` ou
`X-Management-Token`. Le detail beneficiaire utilise le token d'activation
attendu par les routes d'instance. Le client distingue les prestations
executees des prestations non executees et ne propose jamais une demande pour
une prestation non eligible.

## Fonction 5 - Profil de facturation beneficiaire

Routes protegees par le token de l'instance :

- `GET /public/coffrets-instances/{instanceId}/profils-facturation` ;
- `POST /public/coffrets-instances/{instanceId}/profils-facturation` ;
- `PATCH /public/coffrets-instances/{instanceId}/profils-facturation/{profilId}`.

Payload de creation/modification :

```json
{
  "label": "Profil principal",
  "billing": {
    "buyerType": "INDIVIDUAL | BUSINESS | ASSOCIATION | PUBLIC_ENTITY",
    "legalName": "...",
    "billingEmail": "...",
    "address": {
      "line1": "...",
      "postalCode": "...",
      "city": "...",
      "country": "FR"
    }
  },
  "expectedVersion": 1
}
```

`expectedVersion` est omis a la creation et obligatoire a la modification. Pour
une entite non individuelle, le formulaire ajoute les identifiants legaux
requis. Pour `PUBLIC_ENTITY`, il ajoute les champs conditionnels decrits dans
la specification Animation ; la synchronisation annuaire reste un traitement
backend/operateur et ne doit pas etre simulee par le navigateur.

## Fonction 6 - Demande unitaire apres execution

Le bouton `Demander une facture` est affiche uniquement pour une validation de
prestation exposee comme eligible et sans demande active.

Creation :

`POST /public/coffrets-instances/{instanceId}/demandes-facture`

```json
{
  "validationPrestationId": "uuid",
  "billingProfileId": "uuid facultatif",
  "billing": null,
  "comment": "Information utile facultative"
}
```

Le client envoie soit `billingProfileId`, soit un objet `billing`. La reponse
peut contenir `idempotentReplay=true` ; elle est alors traitee comme un succes,
pas comme un doublon a afficher en erreur.

Suivi et telechargement :

- `GET /public/coffrets-instances/{instanceId}/demandes-facture` ;
- `GET /public/coffrets-instances/{instanceId}/demandes-facture/{demandeId}/telecharger`.

Libelles de statut acheteur :

| Statut | Libelle |
| --- | --- |
| `REQUESTED` | Demande envoyee au commercant |
| `ACKNOWLEDGED` | Demande recue par le commercant |
| `PROCESSING` | Facture en preparation |
| `PROVIDED` | Facture disponible |
| `CANCELLED` | Demande annulee |

Seul `PROVIDED` permet le telechargement. La facture est celle du commercant,
et non de Localeo.

## Fonction 7 - Demandes groupees d'un achat Pro

Le detail d'achat Pro doit presenter une vue multi-coffrets et une action
`Demander les factures disponibles`.

- Eligibles : `GET /protected/gestion-achats/achats/{achatId}/demandes-facture-groupees/eligibles` ;
- Creer : `POST /protected/gestion-achats/achats/{achatId}/demandes-facture-groupees` ;
- Suivre : `GET /protected/gestion-achats/achats/{achatId}/demandes-facture-groupees` ;
- Telecharger : `GET /protected/gestion-achats/achats/{achatId}/demandes-facture-groupees/{demandeId}/telecharger`.

Creation :

```json
{
  "validationPrestationIds": ["uuid-1", "uuid-2"],
  "billing": {}
}
```

Une selection vide signifie `toutes les prestations eligibles`. L'interface
doit l'expliquer dans le recapitulatif. Une action peut retourner plusieurs
demandes : le backend separe obligatoirement les lignes par commercant. Le
client affiche donc un resultat par commercant et permet une demande
complementaire lorsque d'autres prestations deviennent eligibles.

Une correction retournee avec `previousRequestId`, `correctionType` et
`correctionReason` est ajoutee a la chronologie du document d'origine.

## Fonction 8 - Authentification au credit Pro

Cette fonction est absente du B2C et masquee lorsque
`LOCALEO_FEATURE_B2B_PURCHASE_CREDIT_ENABLED=false`.

1. Charger `GET /public/credits-achat-b2b/conditions` et afficher `text`.
2. Saisir le code de credit puis appeler `POST /public/credits-achat-b2b/otp`
   avec `{ "creditCode": "..." }`.
3. Toujours afficher la meme confirmation generique afin de ne pas reveler si
   un code existe.
4. Saisir l'OTP a 6 chiffres et exiger l'acceptation non pre-cochee de la
   version courante.
5. Appeler `POST /public/credits-achat-b2b/sessions`.
6. Conserver `accessToken` uniquement en memoire applicative jusqu'a
   `expiresAt` ; ne pas utiliser l'URL ni un stockage persistant.

Validation OTP :

```json
{
  "challengeId": "uuid",
  "otp": "123456",
  "termsAccepted": true,
  "termsVersion": "version retournee par /conditions"
}
```

L'OTP expire apres 10 minutes et la session de credit apres 30 minutes. Les
messages d'erreur ne distinguent pas code inconnu, OTP faux ou expire.

## Fonction 9 - Consulter et appliquer le credit

`GET /public/credits-achat-b2b/me`, avec le bearer de session credit, retourne :

```json
{
  "accountId": "uuid",
  "ownerType": "PRO_ORGANIZATION",
  "ownerId": "uuid",
  "currency": "EUR",
  "status": "ACTIVE",
  "balanceCents": 12000,
  "reservedCents": 3000,
  "nextExpiryAt": "date ISO-8601",
  "lots": [],
  "history": []
}
```

La vue affiche le solde disponible, la part reservee, la prochaine echeance,
les lots et l'historique. Les lots sont consommes en FEFO par le backend ; le
client ne permet pas de choisir un lot.

Dans le checkout Pro :

- afficher le credit maximum applicable et la repartition estimee ;
- exiger a nouveau l'acceptation des conditions si la version change ;
- transmettre session et version lors de l'initialisation ;
- utiliser les montants `credit_applique_centimes` et
  `montant_stripe_centimes` de la reponse comme valeurs finales ;
- pour une annulation, ne jamais promettre un remboursement bancaire de la
  part payee en credit.

## Notifications et raccordement Localeo Live

L'email de mise a disposition est emis par le backend. Si une installation
Localeo Live est associee a l'achat, la Marketplace doit fournir un deep link
vers le detail d'achat ou d'instance, jamais un lien direct contenant un token.
Le contrat d'evenement Live manquant est decrit dans
`localeo-live.md`.

## Gestion des erreurs

| HTTP | Comportement attendu |
| --- | --- |
| `400` | Corriger les parametres ou le format de saisie |
| `401` | Demander le token d'achat/instance ou relancer le code + OTP |
| `403` | Session invalide, expiree ou ressource hors perimetre |
| `404` | Offre/ressource absente ou fonction desactivee |
| `409` | Recharger prix, eligibilite, profil ou commande avant confirmation |
| `422` | Afficher les erreurs sous les champs de facturation |
| `5xx` | Conserver la cle d'idempotence pour une reprise strictement identique |

## Securite, accessibilite et qualite

- Aucun token dans l'URL, les logs, les analytics ou les messages d'erreur.
- Les tokens d'activation et de gestion sont cloisonnes par ressource.
- La session de credit n'accorde aucun acces general au compte acheteur.
- Les montants en centimes sont formates en devise sans arithmetique flottante.
- L'acceptation des conditions et les confirmations ne sont jamais pre-cochees.
- Statuts, erreurs et repartition de paiement restent comprehensibles sans
  couleur et avec un lecteur d'ecran.
- Les boutons de telechargement annoncent le type PDF et le nom du document.
- Les vues achat et facture sont utilisables sur mobile sans tableau debordant.

## Criteres d'acceptation

- Un coffret non retourne par le catalogue ne peut pas etre achete.
- La promesse garantie et le contenu indicatif sont visuellement distincts.
- La mention versionnee est visible avant confirmation d'achat.
- Aucun document d'achat n'est appele `facture commercant`.
- Une demande unitaire est impossible avant execution.
- Une demande groupee produit un resultat separe par commercant.
- Une facture n'est telechargeable qu'en statut `PROVIDED`.
- Le credit est invisible dans tous les parcours particuliers.
- Le code seul ne donne acces ni au solde ni au paiement.
- Les paiements 100 % credit ne redirigent pas vers Stripe.
- La session credit expiree est effacee du client.
- Aucun acheteur ne peut consulter les donnees d'un autre achat.

## Decoupage d'implementation recommande

1. `LM-50-01` : presentation contractuelle du catalogue et gestion du `404`.
2. `LM-50-02` : checkout idempotent et recapitulatif BUM.
3. `LM-50-03` : detail achat/instance et profil de facturation.
4. `LM-50-04` : demandes unitaires, statut et telechargement.
5. `LM-50-05` : demandes groupees Pro par commercant.
6. `LM-50-06` : authentification code + OTP et espace credit.
7. `LM-50-07` : paiement mixte et 100 % credit.
8. `LM-50-08` : acces justificatif apres ajout du contrat backend.
9. `LM-50-09` : deep links Live, tests E2E, accessibilite et cloisonnement.

## Dependances d'activation

- `LOCALEO_FEATURE_BUM_PUBLICATION_GUARD_ENABLED=true` avant ouverture du
  catalogue ;
- `LOCALEO_FEATURE_BUM_QUALIFICATION_ENABLED=true`, prerequis du garde ;
- `LOCALEO_FEATURE_MERCHANT_INVOICE_REQUEST_ENABLED=true` pour les demandes ;
- `LOCALEO_FEATURE_B2B_PURCHASE_CREDIT_ENABLED=true` avec conditions versionnees
  pour le credit Pro ;
- wording du justificatif `BUM-ARB-08` valide et configure ;
- route securisee de consultation du justificatif a livrer avant d'afficher le
  telechargement dans la Marketplace.

## Correctifs MARKET-002, MARKET-003, MARKET-009 et MARKET-010

Retour de paiement fonde sur le statut backend, acceptation Pro independante du credit et quantite entiere de 1 a 1000 : voir le [contrat correctif](../securisation-production/corrections-marketplace-2026-09-06.md) et la [formation et recette](../../exploitation/guide-corrections-marketplace-2026-09-06.md). Ces controles conditionnent la livraison du parcours credit.
