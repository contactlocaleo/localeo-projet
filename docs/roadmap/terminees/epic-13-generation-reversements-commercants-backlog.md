# Backlog Epic 13 - Generation des reversements commercants

## Perimetre

Epic source : `Epic 13. Generation des reversements commercants`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : outiller la preparation des reversements commercants a partir des `MouvementReversement` en attente, en creant des `Reversement` coherents, tracables et exploitables par la chaine de paiement.

## Statut global

- Epic 13 : `Termine`
- Avancement : noyau metier existant consolide, use cases de pilotage et back-office de generation engages.

## Analyse d'impact

### Synthese

Le backend cree deja des `MouvementReversement` lors de la validation d une prestation. Ces mouvements representent les montants dus a un commercant, mais ils doivent encore etre regroupes en objets `Reversement` avant toute phase de paiement.

Cette Epic couvre cette etape intermediaire :
- identifier les mouvements `A_REVERSER` eligibles ;
- verifier les preconditions de reversement ;
- regrouper les mouvements par commercant ;
- creer un `Reversement` et ses `LigneReversement` ;
- faire passer les mouvements en `EN_COURS_DE_REVERSEMENT`.

Elle preparait historiquement le terrain pour l Epic 12. Depuis la cible EPIC 39,
le paiement manuel en banque est decommissionne : les mouvements et reversements
servent de base aux campagnes Stripe Connect.

### Positionnement dans la chaine financiere

La chaine cible devient avec l'EPIC 39 :
1. validation de prestation ;
2. creation du `MouvementReversement` ;
3. generation du `Reversement` ;
4. selection dans une campagne bimensuelle ;
5. execution du transfer via Stripe Connect.

## Regles de gestion consolidees

- Un `MouvementReversement` est eligible a la generation d un reversement uniquement s il est en statut `A_REVERSER`.
- La generation d un reversement est faite par commercant.
- Dans la cible EPIC 39, un `Reversement` doit etre rattache a un compte connecte Stripe eligible.
- Un commercant sans compte connecte Stripe eligible reste bloque jusqu'a regularisation via Stripe.
- Un reversement doit contenir au moins une `LigneReversement`.
- Le `montant_total` du `Reversement` est la somme des montants des mouvements agreges.
- Le `montant_total` d un reversement doit etre strictement positif.
- Un mouvement deja rattache a un `Reversement` ne peut pas etre repris dans un autre reversement actif.
- La generation doit etre idempotente : un rejeu ne doit pas recreer un nouveau reversement avec les memes mouvements.
- La generation V1 est declenchee manuellement depuis le back-office.
- La generation peut etre lancee pour un commercant ou pour un lot multi commercants.
- En traitement lot, le resultat est partiel par commercant : un echec unitaire ne bloque pas les autres commerçants traites.
- Un `Reversement` en `EN_PREPARATION` est fige ; il n absorbe pas de nouveaux mouvements apres sa creation.
- La generation ne paie rien ; elle prepare seulement le `Reversement` en statut `EN_PREPARATION`.

## Flux cible recommande

1. L operateur lance manuellement la preparation pour un commercant ou un lot multi commercants.
2. Le systeme affiche aussi les commercants bloques faute de compte connecte Stripe eligible.
3. Le systeme verifie l existence et l'eligibilite Stripe Connect pour chaque commercant traite.
4. Le systeme recupere les `MouvementReversement` eligibles.
5. Le systeme cree un `Reversement` par commercant traite avec succes.
6. Le systeme cree une `LigneReversement` par mouvement rattache.
7. Les mouvements integres passent en `EN_COURS_DE_REVERSEMENT`.
8. Le `Reversement` cree passe en statut `EN_PREPARATION`.
9. Le reversement devient ensuite eligible a une campagne Stripe Connect pour traitement du transfer.

## Evolutions de modele recommandees

### `Reversement`

Le modele existant est reutilise.

Rappels :
- `id`
- `commercant_id`
- `compte_bancaire_id`
- `date_creation`
- `montant_total`
- `statut`

Statut cible a la creation :
- `EN_PREPARATION`

### `LigneReversement`

Le modele existant est reutilise pour porter le detail de chaque mouvement integre au reversement.

### `CompteReversementCommercant`

Le compte reversement reste cree a la demande via `obtenir_ou_creer`, lors du premier besoin de mouvement financier.

## Impacts use cases

Use cases a creer ou consolider :
- `ListerMouvementsEligiblesAuReversement`
- `GenererReversementCommercant`
- `GenererReversementsCommercantsEnLot`

Use cases existants impactes :
- `CreerReversementCommercant` : devient le coeur de l Epic et doit etre documente comme use case metier officiel de preparation.
- `AfficherMouvementReversementAReverser` : sert de surface de consultation cote commercant, sans pilotage.

## Impacts back-office

Surfaces recommandees :
- une page interne dediee de preparation des reversements ;
- une vue des mouvements eligibles au reversement ;
- une vue des commercants pret a passer en reversement ;
- une action de generation du reversement pour un commercant ;
- une action de generation en lot pour plusieurs commercants ;
- une vue du detail du reversement cree avec ses lignes.

Informations minimales attendues :
- commercant ;
- compte connecte Stripe eligible / absent / bloque ;
- nombre de mouvements eligibles ;
- montant total calcule ;
- date de creation du reversement ;
- statut du reversement.

## Securite et audit

- Seuls des operateurs back-office habilites peuvent generer des reversements.
- La generation doit etre entierement tracable.
- Aucun mouvement ne doit etre bascule en `EN_COURS_DE_REVERSEMENT` sans creation effective du `Reversement` et de sa `LigneReversement`.

Actions d audit minimales :
- `reversement.generated`
- `reversement.generation.failed`

Portee d audit retenue :
- audit au niveau reversement ;
- `commercant_id`, `reversement_id`, `nb_mouvements`, `montant_total` et la liste des mouvements agreges doivent etre presents dans les metadonnees utiles.

## User Stories

### Story `PRD-060` - Lister les mouvements eligibles au reversement

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre a l exploitation d identifier rapidement ce qui peut etre agrege en reversement.

Criteres d acceptation :
- le systeme liste les `MouvementReversement` en statut `A_REVERSER` ;
- la liste est regroupable par commercant ;
- la liste indique explicitement les commercants sans compte connecte Stripe eligible comme bloques ;
- la liste expose le montant total potentiel par commercant.

### Story `PRD-061` - Generer un reversement pour un commercant

Priorite : `P0`
Statut : `Termine`

Valeur metier : preparer un reversement exploitable a partir des mouvements dus a un commercant.

Criteres d acceptation :
- le systeme cree un `Reversement` en statut `EN_PREPARATION` ;
- le systeme cree les `LigneReversement` associees ;
- les mouvements integres passent en `EN_COURS_DE_REVERSEMENT` ;
- le montant total du reversement est coherent avec la somme des mouvements ;
- la creation est refusee si aucun compte connecte Stripe eligible n existe.

### Story `PRD-062` - Generer les reversements en lot pour plusieurs commercants

Priorite : `P0`
Statut : `Termine`

Valeur metier : accelerer le traitement operationnel des reversements.

Criteres d acceptation :
- le systeme peut generer plusieurs `Reversement` en une operation ;
- chaque commercant produit son propre reversement ;
- les commercants sans compte connecte Stripe eligible sont exclus de la generation et signales explicitement ;
- l operation reste atomique par commercant ;
- un echec sur un commercant ne bloque pas les autres commercants du lot.

### Story `PRD-063` - Garantir l idempotence et eviter les doublons de generation

Priorite : `P0`
Statut : `Termine`

Valeur metier : proteger la chaine financiere contre la double preparation.

Criteres d acceptation :
- un mouvement deja rattache a un reversement n est pas repris ;
- un rejeu de la meme generation ne cree pas de doublon ;
- les reversements deja en `EN_PREPARATION`, `EN_COURS` ou `PAYE` n absorbent pas de nouveaux mouvements sans action explicite.

### Story `PRD-064` - Auditer la generation des reversements

Priorite : `P1`
Statut : `Termine`

Valeur metier : faciliter le support et le controle de la preparation financiere.

Criteres d acceptation :
- chaque generation reussie produit un audit `reversement.generated` ;
- chaque echec produit un audit `reversement.generation.failed` ;
- les informations utiles de controle sont conservees sans fuite de donnees superflues.

## Decisions actees

- La generation des reversements est une etape distincte du paiement des reversements.
- La generation V1 est manuelle depuis le back-office.
- Un reversement est genere par commercant.
- La generation en lot multi commercants est dans le perimetre V1.
- Le traitement d un lot est partiel par commercant.
- Dans la cible EPIC 39, le compte connecte Stripe eligible est obligatoire pour generer un reversement transferable.
- Un montant total strictement positif est requis pour generer un reversement.
- Le statut cible du reversement a la creation est `EN_PREPARATION`.
- Un reversement `EN_PREPARATION` est fige apres creation.
- Les mouvements integres passent a `EN_COURS_DE_REVERSEMENT`.
- Les commercants bloques sans compte connecte Stripe eligible restent visibles dans la surface de pilotage.
- La surface V1 de preparation est une page interne dediee.
- L Epic 13 alimente historiquement l Epic 12 ; dans la cible EPIC 39, elle alimente les campagnes Stripe Connect.

## Hors perimetre V1

- calcul automatique de calendrier de reversement ;
- seuil minimum de reversement configurable ;
- retenues, ajustements ou compensations complexes ;
- fusion ou decoupage manuel d un reversement deja cree ;
- rapprochement avec le paiement bancaire.

## Chantiers transverses

### BX-EP13-01 - Pilotage des mouvements eligibles

Priorite : `P0`

Livrables :
- vue des mouvements `A_REVERSER` ;
- regroupement par commercant ;
- signalement des blocages Stripe Connect.

### BX-EP13-02 - Consolidation des use cases de generation

Priorite : `P0`

Livrables :
- formalisation de `CreerReversementCommercant` ;
- generation multi commercants en lot ;
- garanties d idempotence.

### BX-EP13-03 - Audit et exploitation

Priorite : `P1`

Livrables :
- audits de generation ;
- visibilite back-office du resultat de preparation.

## Ordre recommande de livraison

1. `PRD-060`


   - Statut : `Termine`
2. `PRD-061`

   - Statut : `Termine`
3. `PRD-062`

   - Statut : `Termine`
4. `PRD-063`

   - Statut : `Termine`
5. `PRD-064`

   - Statut : `Termine`

## Proposition de tickets implementables

- `EP13-T01` Lister les mouvements eligibles au reversement.
- `EP13-T02` Formaliser `CreerReversementCommercant` comme use case produit de generation.
- `EP13-T03` Ajouter la generation des reversements pour plusieurs commercants.
- `EP13-T04` Ajouter les controles d'eligibilite Stripe Connect.
- `EP13-T05` Ajouter les protections d idempotence sur la generation.
- `EP13-T06` Ajouter les surfaces back-office de preparation des reversements.
- `EP13-T07` Ajouter les audits `reversement.generated` et `reversement.generation.failed`.
