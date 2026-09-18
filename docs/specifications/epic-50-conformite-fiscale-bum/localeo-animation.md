# Epic 50 - Specification Localeo Animation

## Statut et objectif

| Champ | Valeur |
| --- | --- |
| Application | Localeo Animation |
| Epic | Epic 50 - Politique BUM et conformite fiscale |
| Constat historique du contrat | Backend principal disponible, statut Chorus a exposer |
| Public | Gestionnaire d'un partenaire et d'une commune habilitee |
| Domaines | Catalogue de lots, commande, credit, documents et facturation |

L'etat produit courant est porte par le [backlog commun de l'Epic 50](../../roadmap/terminees/epic-50-conformite-fiscale-bum-backlog.md).
Les mentions de disponibilite et les etapes d'implementation ci-dessous
conservent le constat de leur redaction ; leur consolidation ne constitue pas
une nouvelle preuve de recette ou de mise en production.

Localeo Animation permet au partenaire organisateur de commander des lots de
coffrets conformes, de consulter son credit d'achat B2B, de demander les
factures des prestations executees et de recevoir les factures de souscription
emises par Localeo.

## Principes produit obligatoires

- Le partenaire ne qualifie jamais fiscalement un coffret.
- Le catalogue Animation utilise le meme predicat de commercialisation BUM que
  la Marketplace.
- Une commande payee genere un justificatif d'acquisition, pas les factures des
  prestations contenues dans les coffrets.
- Les factures de prestation sont demandees apres execution et separees par
  commercant.
- La facture de souscription Animation est emise par Localeo et reste distincte
  des factures emises par les commercants.
- Le credit est rattache au couple partenaire + commune active et ne peut etre
  deplace vers une autre commune depuis l'interface.
- Le backend choisit les lots de credit en FEFO ; l'utilisateur ne choisit pas
  leur ordre de consommation.
- Pour une entite publique, les donnees Chorus Pro sont collectees selon les
  obligations retournees par l'annuaire, sans rendre tous les champs requis par
  defaut.

## Habilitations et isolation

Les routes sont protegees par la session Animation existante.

| Action | Permission minimale |
| --- | --- |
| Lire catalogue, commande, credit, demandes et documents | `LIRE` |
| Creer une commande, reserver le credit, demander une facture | `MODIFIER` |
| Annuler ou reprendre une commande | Permission imposee par la route existante |

Chaque appel est limite au `partenaire_id` de la session et a
`commune_active_id`. Un changement de commune impose de vider les donnees en
cache puis de recharger credit, catalogue, commandes et factures. Une reponse
`404` ne doit pas reveler qu'une commande existe dans un autre tenant.

## Navigation et ecrans

| Route frontale proposee | Vue | Fonction |
| --- | --- | --- |
| `/animations/:id/coffrets` | Coffrets eligibles | Selection des lots conformes |
| `/animations/:id/commande` | Commande de lots | Acheteur, recapitulatif, credit et paiement |
| `/animations/:id/commande/:commandeId` | Suivi commande | Etat, reprise, annulation et documents |
| `/finance/credit` | Credit d'achat | Solde, echeances, lots et historique |
| `/finance/demandes` | Factures de prestation | Eligibilite et suivi par commercant |
| `/finance/factures-localeo` | Factures Localeo | Souscriptions, avoirs et telechargements |

Les modules Finance peuvent etre regroupes en onglets dans l'application
existante. Ils restent des vues non imbriquees et scannables sur mobile.

## Fonction 1 - Choisir uniquement des coffrets eligibles

Le selecteur de lots appelle :

`GET /protected/animation-locale/communes/{communeId}/coffrets-eligibles`

La reponse contient notamment :

```json
{
  "id": "uuid",
  "nom": "Nom du coffret",
  "eligible": true,
  "raisons_non_eligibilite": [],
  "metadata": {}
}
```

Le frontend affiche uniquement les lignes `eligible=true` comme ajoutables.
Une ligne non eligible peut etre montree en lecture seule avec ses raisons si
le produit veut expliquer une configuration existante, mais aucun bouton ne
permet de forcer son ajout. Le client ne deduit pas l'eligibilite depuis le
type commercial du coffret.

Si une configuration devient invalide entre affichage et commande, le `409` ou
l'erreur metier impose de recharger le catalogue et le montant.

## Fonction 2 - Creer une commande de lots

Route :

`POST /protected/animation-locale/animations/{animationId}/commande-lots`

Header obligatoire : `Idempotency-Key`, genere une seule fois par tentative de
commande et conserve pour toute reprise strictement identique.

```json
{
  "acheteur": {
    "nom_contact": "...",
    "email": "...",
    "telephone": "...",
    "adresse_facturation": {
      "ligne1": "...",
      "code_postal": "...",
      "ville": "...",
      "pays": "FR"
    }
  },
  "appliquerCreditAchat": true,
  "creditTermsAccepted": true,
  "creditTermsVersion": "version courante"
}
```

Le client charge les conditions avec
`GET /public/credits-achat-b2b/conditions` avant d'afficher l'option credit. La
case d'acceptation est obligatoire, non pre-cochee et rattachee a la version
retournee. La session Animation suffit : aucun code ni OTP n'est demande.

La reponse `CommandeLotsAnimationPayload` est la source de verite :

```json
{
  "commande_id": "uuid",
  "animation_id": "uuid",
  "configuration_version": 4,
  "statut": "PAIEMENT_EN_COURS",
  "montant_total_centimes": 20000,
  "devise": "EUR",
  "checkout_url": "https://... ou null",
  "quantite_commandee": 10,
  "quantite_reservee": 0,
  "quantite_attribuee": 0,
  "acheteur": {},
  "lignes": [],
  "action": {
    "code": "ATTENDRE_CONFIRMATION",
    "libelle": "Confirmation Stripe en cours",
    "autorisee": false
  },
  "incident": null,
  "idempotent_replay": false
}
```

Le frontend execute uniquement l'action autorisee retournee :

| Code | Comportement |
| --- | --- |
| `PAYER_COMMANDE_LOTS` | Ouvrir le formulaire de commande |
| `REPRENDRE_PAIEMENT` | Appeler la route de reprise |
| `ATTENDRE_CONFIRMATION` | Polling borne puis rafraichissement manuel |
| `ATTENDRE_RESERVATION` | Afficher le traitement sans double paiement |
| `CONSULTER_DOCUMENTS` | Ouvrir les documents de commande |
| `CONTACTER_SUPPORT` | Afficher la reference d'incident |
| `COMMANDE_REMBOURSEE` | Etat terminal en lecture seule |

Si `checkout_url` est `null`, le credit couvre la totalite. Le client reste
dans l'application et recharge la commande jusqu'a l'etat final. Sinon, il
redirige vers Stripe.

## Fonction 3 - Reprendre, suivre et annuler

- Lire : `GET /protected/animation-locale/animations/{animationId}/commande-lots` ;
- Reprendre : `POST /protected/animation-locale/animations/{animationId}/commande-lots/{commandeId}/reprendre` ;
- Annuler : `POST /protected/animation-locale/animations/{animationId}/commande-lots/{commandeId}/annuler`.

Reprise et annulation envoient une nouvelle `Idempotency-Key`. L'annulation
envoie `{ "motif": "..." }` avec au moins cinq caracteres. Une commande
`A_RECONCILIER` ne doit pas etre relancee ou annulee en boucle ; elle dirige
vers le support avec `incident.code` et sans detail technique sensible.

## Fonction 4 - Consulter le credit Animation

Route : `GET /protected/animation-locale/credits-achat`.

La vue affiche :

- `balanceCents`, montant encore disponible ;
- `reservedCents`, montant retenu par des commandes en cours ;
- `nextExpiryAt`, prochaine echeance ;
- `lots[]`, avec montant restant, source et echeance ;
- `history[]`, mouvements credit/debit, statut, origine et date d'effet.

Le montant affiche comme applicable est `min(balanceCents, total commande)`.
Il est indicatif avant reservation. Le backend calcule le split final.

Pour une commande deja creee, la route
`POST /protected/animation-locale/credits-achat/commandes/{commandeId}/reserver`
accepte `{ "totalCents": totalCourant }` et retourne `amountCents`,
`stripeAmountCents` et `paymentSplit`. Elle sert a une revalidation explicite
du split ou a une reprise ; elle ne doit pas etre appelee en parallele de la
creation de commande qui reserve deja le credit.

En cas de `409 Le total de commande a change`, recharger la commande, recalculer
le recapitulatif visuel et redemander confirmation.

## Fonction 5 - Documents d'acquisition

Une commande payee ou dont les instances sont reservees expose :

- `GET /protected/animation-locale/animations/{animationId}/commande-lots/{commandeId}/documents` ;
- `GET /protected/animation-locale/animations/{animationId}/commande-lots/{commandeId}/documents/{documentId}/telecharger`.

Chaque element fournit `document_id`, `type_document`, `reference_document`,
`fichier_nom`, `date_generation` et `download_url`. La liste contient le recu
consolide et les justificatifs d'acquisition BUM des achats sous-jacents.

Regles de presentation :

- utiliser le titre contractuel du justificatif retourne ;
- rappeler qu'un recu consolide est une preuve de paiement, pas la facture des
  prestations ;
- afficher la repartition credit/Stripe si elle figure dans le snapshot ;
- traiter le telechargement comme PDF ou ZIP selon `Content-Type` et
  `Content-Disposition` ;
- ne pas renommer un document en `Facture commercant`.

## Fonction 6 - Collecter les donnees de facturation

Le partenaire doit pouvoir maintenir un profil reutilisable pour les demandes
de facture et la souscription Animation.

Socle commun :

```json
{
  "buyerType": "BUSINESS | ASSOCIATION | PUBLIC_ENTITY",
  "legalName": "...",
  "billingEmail": "...",
  "address": {
    "line1": "...",
    "postalCode": "...",
    "city": "...",
    "country": "FR"
  },
  "siret": "14 chiffres"
}
```

Champs publics V1 :

```json
{
  "chorusRecipientCode": "SIRET",
  "chorusDirectoryCheckedAt": "date ISO-8601",
  "chorusRecipientActive": true,
  "chorusServiceCode": "valeur conditionnelle",
  "chorusServiceCodeRequired": false,
  "legalCommitmentNumber": "valeur conditionnelle",
  "legalCommitmentRequired": false,
  "purchaseOrderReference": null,
  "contractNumber": null,
  "marketNumber": null,
  "contactName": null
}
```

Le SIRET, le destinataire actif et la date de controle annuaire sont requis
pour une entite publique. Le code service et l'engagement juridique ne sont
requis que si les indicateurs correspondants valent `true`.

**Prerequis backend restant :** le backend valide les snapshots, mais Localeo
Animation ne dispose pas d'une API de profil partenaire reutilisable ni d'une
route publique de synchronisation annuaire. Ne pas appeler la route BackOffice
`/internal/conformite-fiscale/bum/profils-facturation/*`. Exposer un contrat
protege par session Animation avant d'implementer l'edition persistante.

## Fonction 7 - Demander les factures de prestation

Depuis une commande, charger les prestations eligibles :

`GET /protected/animation-locale/facturation/demandes-groupees/commandes/{commandeId}/eligibles`

L'utilisateur selectionne les prestations executees ou conserve la selection
vide signifiant `toutes les prestations eligibles`, puis appelle :

`POST /protected/animation-locale/facturation/demandes-groupees/commandes/{commandeId}`

```json
{
  "validationPrestationIds": ["uuid-1", "uuid-2"],
  "billing": {}
}
```

Le resultat est une liste, car une action cree une demande distincte par
commercant. La vue globale consomme
`GET /protected/animation-locale/facturation/demandes-groupees` et affiche :

- reference, commercant, date et statut ;
- chaque prestation et sa date d'execution ;
- montant brut TTC par ligne et devise ;
- numero/date de facture lorsque disponible ;
- lien avec la demande precedente lorsqu'il s'agit d'une correction.

Le telechargement est disponible seulement pour `PROVIDED` via
`GET /protected/animation-locale/facturation/demandes-groupees/{demandeId}/telecharger`.

Libelles :

| Statut | Libelle partenaire |
| --- | --- |
| `REQUESTED` | Envoyee au commercant |
| `ACKNOWLEDGED` | Recue par le commercant |
| `PROCESSING` | En preparation |
| `PROVIDED` | Facture disponible |
| `CANCELLED` | Demande annulee |

Une demande complementaire reste possible pour les prestations executees plus
tard. Les lignes deja rattachees a une demande active ne sont pas proposees.

## Fonction 8 - Factures de souscription Localeo

Routes :

- `GET /protected/animation-locale/factures-localeo` ;
- `GET /protected/animation-locale/factures-localeo/{factureId}/telecharger`.

La liste affiche `ABONNEMENT_ANIMATION` et `AVOIR_ABONNEMENT`, avec numero,
statut, dates, lignes, totaux et facture d'origine. Une souscription totalement
gratuite n'est pas presentee comme une facture payee. Un remboursement apres
emission produit un avoir reference.

Pour un partenaire public, le libelle de depot Chorus doit etre separe du
statut de facture. La facture peut etre `ISSUED` alors que son depot est encore
`PREPARED` ou `SUBMITTED`.

**Prerequis backend restant :** les depots Chorus sont exposes uniquement au
BackOffice. Ajouter une projection partenaire en lecture seule, cloisonnee au
partenaire, avant d'afficher `PREPARED`, `SUBMITTED`, `ACCEPTED` ou `REJECTED`
dans Localeo Animation.

## Notifications

Le contact de facturation recoit les notifications backend pour les factures
disponibles, les echeances de credit et les evenements de souscription. Dans
l'application, les deep links ouvrent la commune active et la ressource cible.
Si la commune ne correspond pas, demander d'abord son changement explicite.

Ne jamais inclure dans une notification un token, un profil complet de
facturation, des coordonnees bancaires ou le detail fiscal d'une facture.

## Gestion des erreurs

| HTTP | Comportement attendu |
| --- | --- |
| `400` | Afficher une erreur de saisie contextualisee |
| `401` | Relancer l'authentification Animation |
| `403` | Signaler l'absence d'habilitation sans exposer le tenant cible |
| `404` | Ressource absente, autre tenant ou fonction desactivee |
| `409` | Recharger commande, credit ou profil avant confirmation |
| `422` | Associer chaque erreur au champ de facturation concerne |
| `5xx` | Conserver l'idempotency key et proposer une reprise identique |

## UX, accessibilite et securite

- La commune active reste visible dans toutes les vues Finance et Commande.
- Les montants en centimes sont formates sans flottants.
- Le split `credit / Stripe` est visible avant confirmation et apres paiement.
- Les statuts ont un texte ; la couleur seule ne porte aucune information.
- L'acceptation des conditions n'est jamais pre-cochee.
- Les listes de lignes passent en disposition verticale sur petit ecran.
- Les documents et snapshots fiscaux ne sont pas places dans les analytics.
- Les reponses d'un tenant precedent sont supprimees au changement de commune.

## Criteres d'acceptation

- Aucun coffret non eligible n'est commandable.
- Aucun ecran Animation ne propose de valider ou requalifier un BUM.
- Le credit consulte appartient au partenaire et a la commune actifs.
- Le parcours gere paiement Stripe, mixte et 100 % credit.
- Un `checkout_url=null` ne declenche aucune redirection Stripe.
- Les justificatifs et recus ne sont pas presentes comme factures de prestation.
- Les demandes sont creees par commercant et seulement apres execution.
- Une selection vide est recapituloee comme toutes les lignes eligibles.
- Une correction ne remplace pas le document original.
- Les factures de souscription et les factures commercants sont separees.
- Un partenaire public voit les exigences Chorus conditionnelles.
- Aucune donnee d'une autre commune ou d'un autre partenaire n'est visible.

## Decoupage d'implementation recommande

1. `LA-50-01` : catalogue eligible et blocages de configuration.
2. `LA-50-02` : commande de lots idempotente et etats de reprise.
3. `LA-50-03` : consultation du credit et paiement mixte/100 % credit.
4. `LA-50-04` : documents de commande et justificatifs BUM.
5. `LA-50-05` : eligibilite et demandes groupees par commercant.
6. `LA-50-06` : factures Localeo et avoirs de souscription.
7. `LA-50-07` : profil partenaire/public apres contrat backend dedie.
8. `LA-50-08` : statut Chorus apres projection backend partenaire.
9. `LA-50-09` : notifications, accessibilite, E2E et isolation tenant.

## Dependances d'activation

- `LOCALEO_FEATURE_BUM_PUBLICATION_GUARD_ENABLED=true` ;
- `LOCALEO_FEATURE_BUM_QUALIFICATION_ENABLED=true` ;
- wording d'acquisition BUM approuve et configure dans la politique active ;
- `LOCALEO_FEATURE_MERCHANT_INVOICE_REQUEST_ENABLED=true` ;
- `LOCALEO_FEATURE_LOCALEO_INVOICING_ENABLED=true` ;
- `LOCALEO_FEATURE_B2B_PURCHASE_CREDIT_ENABLED=true` avec version et texte des
  conditions configures ;
- `LOCALEO_FEATURE_CHORUS_MANUAL_DEPOSIT_ENABLED=true` pour le depot public ;
- URLs Stripe Animation, webhooks et batchs de rapprochement recetes.

## ANIM-001 ? Autorisations de facturation

Toutes les lectures, demandes et telechargements sont limites au partenaire ET a la
commune active. Les demandes groupees sont jointes a leur commande puis animation
avant restitution. Les factures et avoirs Localeo portent la commune dans la reference
serveur `municipalityId`; un avoir herite de sa facture d'origine. Une facture historique
sans commune reste accessible au back-office mais n'est pas publiee dans le portail
avant regularisation de son rattachement par la procedure administrative auditee.
Une permission sur A n'autorise jamais la facturation de B du meme partenaire.


## ANIM-006 - Credit couvrant integralement les lots

La commande passe en PAIEMENT_EN_COURS sans URL Stripe via une transition de
domaine exigeant exactement le total reserve. La confirmation reste conditionnee
a la capture verifiee du credit, puis a la materialisation des lots. Un rejeu apres
interruption de cette finalisation reprend la meme commande et le meme evenement
interne; une commande deja payee/reservee ne redemarre pas un checkout.

Complement ANIM-001 : seule la route d administration autorisee demande
explicitement une liste toutes communes. Les routes du portail gardent le
filtrage communal obligatoire; ce choix interne n est pas un parametre public.
