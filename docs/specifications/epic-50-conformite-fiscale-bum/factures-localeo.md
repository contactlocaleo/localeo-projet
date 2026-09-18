# Epic 50 - Factures emises par Localeo

## Perimetre

Localeo gere deux familles de factures dont il est l'emetteur :

- la facture de commission adressee au commercant ;
- la facture de souscription a l'offre Localeo Animation adressee au partenaire.

Ces documents sont distincts de la facture de prestation emise par le commercant
apres execution du coffret et du justificatif d'acquisition remis lors de
l'achat d'un BUM.

## Decision d'architecture : snapshot fiscal puis rendu a la demande

La source de verite est une facture structuree et immuable en base. Lors de son
emission, Localeo fige l'emetteur, le destinataire, les lignes, les montants,
les taux et montants de TVA, la devise, la date d'exigibilite, les references
metier et la version du modele documentaire. Le numero de facture est attribue
une seule fois avec `SequenceFacturationOrm`.

Le PDF n'est qu'une representation de cette facture. Il peut etre genere au
moment de l'emission ou plus tard, a la premiere consultation, puis conserve
dans le stockage documentaire. Les appels suivants retournent le meme document
ou le regenerent depuis le meme snapshot et la meme version de rendu. Ils ne
recalculent jamais les montants et n'attribuent jamais un nouveau numero.

Cette approche concilie :

- immutabilite et audit des donnees fiscales ;
- generation physique facultative et economie de stockage initiale ;
- disponibilite d'un PDF pour l'utilisateur, la comptabilite et Chorus Pro ;
- idempotence en cas de webhook Stripe, rejeu d'outbox ou double clic ;
- correction par avoir, sans modification silencieuse d'une facture emise.

## Aggregate commun `FactureLocaleo`

| Groupe | Donnees a figer |
| --- | --- |
| Identite | `id`, `type`, numero, statut, dates d'emission et d'exigibilite, devise |
| Emetteur | identite legale Localeo, adresse, SIREN/SIRET, TVA intracommunautaire et coordonnees bancaires applicables |
| Destinataire | type d'acteur, identifiant metier, raison sociale ou nom, adresse, SIRET et TVA intracommunautaire si applicables |
| Lignes | libelle, quantite, prix unitaire HT, remise, taux TVA, montant TVA, total HT et TTC |
| Totaux | total HT, total TVA par taux, total TTC, deja regle et net a payer |
| Origine | identifiant et version du snapshot source, references Stripe ou campagne de reversement |
| Secteur public | SIRET destinataire, code service, engagement juridique, commande, marche ou contrat |
| Document | version du gabarit, cle de stockage, empreinte, date de generation et type MIME |
| Audit | cle d'idempotence, auteur ou evenement source, dates et motif d'annulation ou d'avoir |

La cle d'idempotence est unique par type de facture et evenement economique.
Une facture emise est immuable. Une correction produit un avoir reference a la
facture initiale, puis, si necessaire, une nouvelle facture.

## Facture de commission au commercant

La facture porte sur le service rendu par Localeo au commercant. Elle ne doit
pas etre confondue avec la facture de la prestation executee par ce dernier.

La regle validee est une facture consolidee par commercant et par campagne de
reversement. Son snapshot contient la liste des `ValidationPrestation` et des
`MouvementReversement` inclus, la valeur brute TTC des prestations, la
commission configurable TTC, sa ventilation HT/TVA selon la configuration
Localeo applicable et le net reverse. La cible de 15 % reste informative : le
montant configure et snapshote fait autorite.

La cloture de la campagne constitue l'evenement d'emission et fige la facture.
L'enregistrement fiscal doit etre cree avant l'ordre de reversement. Ces
operations sont rendues atomiques conformement a `BUM-ARB-23`. Une
panne de generation du PDF ne doit en revanche pas modifier la campagne ni
creer une seconde facture. La cle
d'idempotence est `COMMISSION:{commercant_id}:{campagne_reversement_id}`. La
facture est rendue accessible au commercant et peut etre notifiee par les
canaux deja prevus pour son application.

## Facture d'abonnement Localeo Animation

La facture porte sur la souscription Localeo vendue au partenaire. Elle est
emise apres confirmation du paiement, a partir du snapshot de
`SouscriptionPlateforme` defini par l'Epic 47 : offre et commune, periode,
prix HT, taux et montant de TVA, TTC, devise et coordonnees de facturation.

Le webhook Stripe confirme le paiement mais Stripe ne devient pas une seconde
source de numerotation fiscale. La reference Stripe est conservee comme preuve
de reglement. La cle d'idempotence est fondee sur le paiement Localeo ou, a
defaut, sur le `payment_intent` Stripe. Un rejeu du webhook retrouve la facture
existante.

La facture remplace la simple preuve de paiement comme document fiscal, tout en
conservant cette preuve dans l'audit. Elle est mise a disposition dans Localeo
Animation et envoyee au contact de facturation. Pour une entite publique, elle
alimente la meme file de depot manuel Chorus Pro que les autres factures.

## Cycle minimal

```text
evenement economique confirme
          |
recherche par cle d'idempotence
          |
creation et snapshot atomiques
          |
numero fiscal attribue une fois
          |
facture emise et notification
          |
PDF genere maintenant ou a la demande
          |
correction eventuelle par avoir
```

## Points techniques a conserver

- reutiliser `SequenceFacturationOrm` avec un scope Localeo, sans sequence
  concurrente dans Stripe ou dans chaque canal ;
- creer un aggregate documentaire generique plutot que rattacher ces factures
  a `DocumentAchatCoffretOrm`, qui appartient au cycle d'achat du coffret ;
- verrouiller transactionnellement la cle d'idempotence et l'attribution du
  numero ;
- versionner le gabarit et conserver l'empreinte du PDF materialise ;
- autoriser la regeneration uniquement depuis le snapshot et la version de
  rendu d'origine ;
- ne pas supprimer ni modifier une facture emise ; utiliser un avoir ;
- appliquer les habilitations du commercant, du partenaire et du BackOffice a
  la consultation et au telechargement.
