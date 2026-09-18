# Backlog Epic 51 - Vision 360 des achats BackOffice

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : fournir au BackOffice Localeo un point d'entree unique pour rechercher un achat, comprendre son etat de bout en bout, suivre son paiement et son cout Stripe, puis identifier rapidement les anomalies et les actions de support pertinentes.
- Domaine fonctionnel principal : `gestion_achats`.
- Surfaces ciblees au MVP : backend, API interne et BackOffice.
- Dependances : Epics 14, 20, 22, 30, 37, 39, 44, 46 et 50.

Voir [la conception technique](../../specifications/epic-51-vision-360-achats/conception-technique.md).

## Probleme

Les informations d'un achat existent mais sont reparties entre `CommandeAchat`, `LigneCommandeAchat`, `AchatCoffret`, `Paiement`, `CoffretInstance`, documents, demandes de facturation, remboursements, evenements Stripe et audit. Cette dispersion rend difficile la reponse rapide aux questions suivantes :

- le client a-t-il effectivement paye et pour quel montant ?
- combien Stripe a-t-il facture pour ce paiement ?
- le paiement a-t-il produit tous les achats et toutes les instances attendues ?
- ou se situe chaque coffret dans son cycle de vie ?
- quels documents, remboursements, demandes de facture ou credits sont lies a l'achat ?
- existe-t-il une anomalie necessitant une reprise ou une action support ?

## Ancrage dans l'existant

- `CommandeAchatOrm` est la racine des commandes multi-coffrets Pro et Animation ; elle porte le contexte, le montant total, le statut et les jalons de paiement et de reservation.
- `AchatCoffretOrm` reste l'unite commerciale d'achat d'un coffret et porte la reference d'achat, l'acheteur, l'origine, la quantite, le statut et les instances generees.
- `PaiementOrm` porte deja les identifiants Checkout Session, PaymentIntent, Charge et Balance Transaction ainsi que `stripe_fee_amount`, `stripe_net_amount`, `commission_localeo_brute` et `commission_localeo_nette_estimee`.
- `RemboursementAchatOrm` porte le suivi des remboursements et leurs donnees financieres Stripe.
- les visions 360 Client, Animation et Finance fournissent des liens de navigation connexes, mais aucune n'est centree sur l'achat lui-meme.
- l'Epic 22 et le journal d'audit fournissent les evenements utiles a une chronologie consolidee.
- l'Epic 50 ajoutera les justificatifs BUM, demandes de facture, factures et credits d'achat ; la vision doit pouvoir les integrer sans dupliquer leurs donnees.

La Vision 360 Achat est une projection de lecture calculee depuis ces sources. Elle ne possede pas de table metier propre et ne remplace aucun workflow existant.

## Perimetre MVP

### 1. Recherche et acces

- rechercher par reference d'achat, UUID d'achat ou de commande, email, telephone, entreprise, reference Stripe ou reference de remboursement ;
- filtrer par periode, origine (`MARKETPLACE`, `PRO`, `LOT_ANIMATION`), type de client, statut d'achat, statut de paiement et presence d'anomalie ;
- paginer et trier les resultats ;
- ouvrir une commande consolidee ou un achat unitaire, y compris les achats historiques sans commande parente.

### 2. Identite et contexte commercial

- reference, origine, canal, date, client ou organisation et coordonnees utiles au support ;
- commande parente, animation et partenaire lorsqu'ils existent ;
- lignes commandees, coffrets, quantites, prix unitaires et montant total ;
- statut metier global et jalons principaux : creation, paiement, creation des achats, reservation et activation des instances.

### 3. Vision paiement et cout Stripe

- montant paye, devise, fournisseur et statut du paiement ;
- frais Stripe reels en centimes et en euros issus de la Balance Transaction ;
- montant net Stripe et taux de frais effectif ;
- commission Localeo brute et nette estimee deja disponibles ;
- references Stripe utiles, repliees dans une zone technique ;
- etat de completude des donnees financieres, notamment lorsque les frais Stripe ne sont pas encore recuperes ;
- detail des tentatives de paiement lorsqu'une commande en possede plusieurs, sans additionner plusieurs fois les tentatives echouees au chiffre d'affaires.

### 4. Cycle de vie des achats et coffrets

- liste de tous les `AchatCoffret` de la commande ;
- nombre d'instances attendues, creees, en attente d'activation, actives, consommees, expirees ou annulees ;
- progression des prestations lorsque cette information est pertinente ;
- coherence entre quantite commandee, achats enfants et instances generees ;
- liens vers les vues detaillees de la commande, de l'achat, du client, de l'animation et des coffrets.

### 5. Documents et apres-vente

- document recapitulatif d'achat et autres documents disponibles ;
- remboursements demandes, en cours, executes ou en echec, avec montant brut et impact des frais Stripe lorsque disponible ;
- demandes de facture et factures associees lorsque l'Epic 50 est implementee ;
- credit d'achat B2B consomme ou genere lorsque l'Epic 50 est implementee ;
- communications importantes : confirmation, acces aux coffrets, relances et echecs d'envoi.

### 6. Chronologie et alertes

- chronologie consolidee des evenements de commande, paiement, achat, instance, remboursement, document, notification et audit ;
- alertes codees, datees et actionnables ;
- liens vers les actions metier existantes, sans mutation directe depuis l'agregat au MVP.

## Indicateurs affiches

Les montants sont exprimes en centimes dans le contrat interne et rendus en EUR avec deux decimales dans le BackOffice.

| Indicateur | Definition |
| --- | --- |
| Montant commande | Somme contractuelle des lignes de la commande ou montant de l'achat historique. |
| Montant effectivement paye | Montant du paiement reussi faisant foi, sans inclure les tentatives echouees. |
| Frais Stripe | `Paiement.stripe_fee_amount` issu de la Balance Transaction. |
| Net Stripe | `Paiement.stripe_net_amount`; a defaut, inconnu et non recalcule silencieusement. |
| Taux de frais effectif | `frais Stripe / montant paye`, lorsque les deux valeurs sont connues et positives. |
| Montant rembourse | Somme des remboursements effectivement confirmes. |
| Net encaisse apres remboursements | Net Stripe diminue des remboursements et couts connus, avec une definition technique figee avant implementation. |
| Commission Localeo brute | Valeur deja figee sur le paiement. |
| Commission Localeo nette estimee | Valeur deja figee sur le paiement, presentee explicitement comme estimation. |
| Instances attendues / creees | Quantite commandee comparee au nombre d'instances effectivement generees. |

## Alertes minimales

- commande payee sans achat enfant ou sans toutes les instances attendues ;
- achat confirme sans paiement reussi identifiable ;
- ecart entre montant commande et montant du paiement reussi ;
- paiement reussi sans frais Stripe apres un delai configurable ;
- plusieurs paiements reussis pour une meme racine d'achat ;
- statut commande, achat ou instance incoherent avec les jalons enregistres ;
- remboursement en echec, incomplet ou superieur au montant remboursable ;
- document d'achat ou communication obligatoire absent ou en echec ;
- commande bloquee en `A_RECONCILIER` ou avec `derniere_erreur` ;
- donnees Stripe partielles empechant le calcul du cout reel.

## Hors perimetre MVP

- comptabilite generale ou rapprochement bancaire exhaustif ;
- recalcul ou modification manuelle des frais Stripe ;
- nouvelle source de verite analytique ou copie des donnees Stripe ;
- declenchement direct d'un remboursement, d'une reconciliation ou d'une regeneration depuis la vue 360 ;
- dashboard agrege de chiffre d'affaires multi-achats, traite separement du detail 360 ;
- exposition de la vue aux clients, partenaires ou commercants ;
- stockage ou affichage du payload Stripe brut par defaut.

## User Stories

### PRD-479 - Rechercher un achat

En tant qu'operateur BackOffice, je veux rechercher une commande ou un achat avec ses references metier, client ou Stripe afin d'acceder rapidement a son detail.

Criteres d'acceptation :

- recherche paginee et combinable avec les filtres principaux ;
- prise en charge des commandes consolidees et des achats historiques sans commande ;
- resultat limite aux donnees necessaires a l'identification.

### PRD-480 - Consulter la synthese d'un achat

En tant qu'operateur support, je veux comprendre en un coup d'oeil ce qui a ete commande, par qui, sur quel canal et dans quel etat.

Criteres d'acceptation :

- identite, contexte, lignes, montants et jalons sont consolides ;
- le statut global est accompagne du detail des statuts sources ;
- les liens vers les objets BackOffice existants sont proposes.

### PRD-481 - Suivre le paiement et son cout Stripe

En tant que responsable finance, je veux connaitre le cout Stripe reel de chaque paiement afin de mesurer le net effectivement encaisse.

Criteres d'acceptation :

- montant paye, frais, net, taux effectif et commissions Localeo sont distingues ;
- la source Balance Transaction et la date de synchronisation sont identifiables ;
- une valeur inconnue reste `null` et genere une alerte au lieu d'etre assimilee a zero ;
- les references Stripe techniques sont protegees et repliees par defaut.

### PRD-482 - Suivre toutes les tentatives de paiement

En tant qu'operateur support, je veux distinguer les tentatives echouees, abandonnees et reussies afin d'expliquer le parcours de paiement sans fausser les montants.

Criteres d'acceptation :

- toutes les tentatives rattachees a la racine sont ordonnees ;
- une tentative affiche son statut, sa date et ses references ;
- seul le paiement faisant foi alimente les indicateurs financiers de l'achat.

### PRD-483 - Controler la generation des achats et instances

En tant qu'operateur exploitation, je veux comparer les quantites commandees aux achats et instances crees afin d'identifier une activation incomplete.

Criteres d'acceptation :

- les quantites attendues et obtenues sont visibles par ligne ;
- les incoherences generent des alertes stables ;
- les statuts de toutes les instances sont consolides.

### PRD-484 - Consulter l'apres-vente et les documents

En tant qu'operateur support, je veux retrouver remboursements, documents, communications et objets BUM lies afin de traiter une demande sans changer d'outil de recherche.

Criteres d'acceptation :

- chaque objet expose son statut, son montant ou sa date pertinente et un lien ;
- les donnees de l'Epic 50 sont integrees lorsqu'elles existent ;
- aucune regle metier n'est dupliquee dans la vision.

### PRD-485 - Parcourir la chronologie consolidee

En tant qu'operateur support, je veux reconstituer l'histoire complete de l'achat afin de diagnostiquer un incident.

Criteres d'acceptation :

- les evenements multi-sources sont ordonnes, pagines et filtres ;
- chaque evenement indique sa source et sa ressource ;
- les donnees personnelles et payloads techniques sont masques selon les habilitations.

### PRD-486 - Identifier les anomalies actionnables

En tant que responsable exploitation, je veux disposer d'alertes explicites afin de prioriser les achats a regulariser.

Criteres d'acceptation :

- chaque alerte possede un code stable, une severite, une date et une ressource ;
- les alertes couvrent au minimum paiement, frais Stripe, reconciliation, instances, remboursements, documents et communications ;
- la vue propose un lien vers l'action existante quand elle existe.

### PRD-487 - Securiser, auditer et observer la Vision 360

En tant que responsable securite, je veux que la consultation des achats respecte les habilitations et soit tracable.

Criteres d'acceptation :

- acces reserve aux roles internes autorises ;
- coordonnees masquees par defaut et acces complet audite ;
- aucun secret ni payload Stripe brut n'est expose ;
- erreurs correlees et performances mesurees selon l'Epic 44.

## Contrats API proposes

| ID | Methode et chemin | Finalite |
| --- | --- | --- |
| ACH360-API-001 | `GET /internal/gestion-achats/vision-360/achats` | Rechercher commandes et achats historiques. |
| ACH360-API-002 | `GET /internal/gestion-achats/vision-360/achats/{achat_key}` | Charger la synthese consolidee ; `achat_key` accepte une reference metier ou un UUID resolu sans ambiguite. |
| ACH360-API-003 | `GET /internal/gestion-achats/vision-360/achats/{achat_key}/paiements` | Charger les tentatives et donnees financieres Stripe. |
| ACH360-API-004 | `GET /internal/gestion-achats/vision-360/achats/{achat_key}/chronologie` | Charger la chronologie paginee et filtree. |
| ACH360-API-005 | `GET /internal/gestion-achats/vision-360/achats/{achat_key}/alertes` | Charger les anomalies actionnables. |

## Decoupage propose

| Lot | Contenu | Dependances |
| --- | --- | --- |
| A0 | Vocabulaire, statut global, definitions financieres, habilitations et OpenAPI | Arbitrages P0 valides |
| A1 | Recherche et synthese commande/achat | Modeles achat et commande existants |
| A2 | Paiements, cout Stripe, tentatives et completude financiere | Epic 39 et Balance Transactions |
| A3 | Achats enfants, instances et controles de coherence | Epics 14 et 46 |
| A4 | Documents, remboursements, communications et objets BUM | Epics 20, 22 et 50 |
| A5 | Chronologie, alertes, audit, performance et documentation | Epic 44 |

## Registre d'arbitrage

Les arbitrages necessaires au demarrage ont ete valides le 25 aout 2026.

| ID | Point a arbitrer | Explication detaillee | Proposition la plus simple | Validation simple | Statut |
| --- | --- | --- | --- | --- | --- |
| ACH360-ARB-01 | Racine de la vision | Une commande Pro ou Animation regroupe plusieurs achats, tandis qu'un achat historique peut etre autonome. Il faut eviter deux interfaces incompatibles. | Utiliser une racine de lecture unifiee : `CommandeAchat` lorsqu'elle existe, sinon `AchatCoffret`; exposer un `root_type` explicite. | Valider un exemple B2C historique, un achat Pro et un lot Animation dans le meme contrat. | Valide le 25 aout 2026 |
| ACH360-ARB-02 | Paiement faisant foi | Plusieurs tentatives peuvent exister. Additionner toutes les lignes de paiement fausserait montant et frais. | Retenir l'unique paiement reussi rattache a la racine ; s'il y en a plusieurs, ne pas choisir silencieusement et lever une alerte critique. | Tester une tentative echouee puis reussie, puis le cas anormal de deux succes. | Valide le 25 aout 2026 |
| ACH360-ARB-03 | Frais Stripe manquants | Les frais peuvent ne pas etre disponibles au moment du webhook si la Balance Transaction n'est pas encore resolue. Zero signifierait a tort que Stripe n'a rien facture. | Conserver `null`, afficher `En attente de synchronisation` et alerter apres 24 heures ; reutiliser la reprise Stripe existante. | Valider le delai de 24 heures avec l'exploitation et simuler une donnee absente puis enrichie. | Valide le 25 aout 2026 |
| ACH360-ARB-04 | Net apres remboursement | Stripe peut traiter differemment frais initiaux et frais de remboursement. Une formule approximative ne doit pas etre presentee comme comptable. | Afficher separement paye, frais initiaux, net Stripe, remboursements et frais de remboursement ; ne pas exposer d'indicateur net consolide avant validation ulterieure de sa formule par la finance. | Faire valider un exemple de paiement, remboursement total et remboursement partiel par la finance avant d'ajouter cet indicateur. | Valide le 25 aout 2026 |
| ACH360-ARB-05 | Donnees personnelles | La recherche par email et telephone est utile au support mais augmente l'exposition des donnees. | Masquer par defaut ; affichage complet reserve a `ADMIN` et audite, sur le modele de la Vision 360 Client. | Reutiliser les tests d'habilitation et d'audit de l'Epic 37. | Valide le 25 aout 2026 |
| ACH360-ARB-06 | Actions disponibles | Une action depuis un agregat multi-sources augmente le risque d'agir sur la mauvaise racine. | MVP en lecture seule avec liens vers les actions existantes de reprise, remboursement ou renvoi. | Recette BackOffice sur les liens des trois parcours de reference. | Valide le 25 aout 2026 |

## Definition de termine

- une commande ou un achat historique est retrouvable depuis ses references metier, client et Stripe ;
- les montants paye, frais Stripe, net Stripe, remboursements et commissions sont distincts et sourcables ;
- les tentatives echouees ne faussent aucun indicateur financier ;
- les quantites commandees, achats enfants et instances sont reconciliables visuellement ;
- la chronologie et les alertes permettent d'expliquer les incidents principaux ;
- les listes sont paginees, les donnees personnelles protegees et les consultations sensibles auditees ;
- les contrats, regles de calcul, controles d'habilitation et alertes disposent de tests ;
- la documentation d'exploitation precise les sources, la fraicheur et les limites des indicateurs.

## Etat d'implementation

Les lots `A0` a `A5` du MVP backend sont implementes :

- migration `v179` et reprise prudente du montant brut des paiements historiques ;
- suivi explicite du montant paye, de la devise et de la completude des donnees financieres Stripe ;
- recuperation des Balance Transactions pour les achats unitaires et commandes de lots ;
- racine unifiee `COMMANDE` ou `ACHAT` et resolution par `rootKey`, reference metier ou reference Stripe ;
- recherche, synthese, tentatives de paiement, chronologie et alertes ;
- controle des quantites commandees, achats enfants et instances ;
- integration des remboursements, documents, demandes de facture et communications existantes ;
- masquage des coordonnees, restriction aux profils internes et audit des consultations completes ;
- cinq routes internes sous `/internal/gestion-achats/vision-360` ;
- entree BackOffice `Vision 360 achats` et detail financier ;
- readiness de schema et tests unitaires/de migration cibles.

Restent des validations de livraison et non des arbitrages produit : appliquer la migration sur une copie de production, executer la suite Python dans un environnement compatible, mesurer les budgets p95 et effectuer la recette des parcours B2C historique, Pro et Animation.
