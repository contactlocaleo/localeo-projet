# Backlog Epic 1 - Gouvernance du referencement commercant et prestation

## Perimetre

Epic source : `Epic 1. Gouvernance du referencement commercant et prestation`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : cadrer les evolutions metier, techniques et back-office pour piloter le statut d'un commercant, la disponibilite de ses prestations et l'activation des coffrets dans un catalogue coherent.

## Statut global

- Epic 1 : `Termine`
- Avancement : statuts metier, persistence, filtres catalogue publics et principaux controles SQLAdmin implementes ; couverture de tests et consolidation finale encore a completer.

## Regles de gestion consolidees

- Un commercant peut etre dans l'un des statuts `BROUILLON`, `REFERENCE`, `ACTIF`, `SUSPENDU`, `ARCHIVE`.
- Tout commercant cree est initialise par defaut au statut `BROUILLON`.
- Le coffret porte un statut distinct du commercant.
- La prestation porte un statut distinct du commercant.
- Un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas avoir de prestations au statut `ACTIVE`, `BROUILLON` ou `REFERENCE`.
- Si au moins une prestation est rattachee a un coffret actif et qu'il existe au moins une coffret instance en cours, il est interdit de suspendre ou d'archiver le commercant concerne.
- Une `coffret instance en cours` est une instance achetee, donc en statut `ACTIVE` ou `EN_ATTENTE_ACTIVATION`.
- Un commercant au statut `BROUILLON` ou `REFERENCE` ne peut pas avoir de coffret actif.
- Un coffret est activable uniquement si le commercant associe est `ACTIF`.

## Decisions actees

- Le statut initial par defaut d'un commercant est `BROUILLON`.
- Le coffret dispose d'un statut metier propre.
- La prestation dispose d'un statut metier propre.
- La notion de `coffret instance en cours` couvre les instances achetees `ACTIVE` et `EN_ATTENTE_ACTIVATION`.

## Backlog priorise

### Story `PRD-001` - Definir et normaliser le statut commercant

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre le referencement progressif d'un commercant sans exposition prematuree.

Criteres d'acceptation :
- Un commercant ne peut prendre que les statuts `BROUILLON`, `REFERENCE`, `ACTIF`, `SUSPENDU`, `ARCHIVE`.
- Le statut est visible dans le back-office sur la liste et la fiche detail commercant.
- Toute creation de commercant initialise le statut `BROUILLON` par defaut.
- Toute tentative d'enregistrer un statut invalide est refusee avec un message explicite.

Taches :
- Introduire ou centraliser l'enum/metier de statut commercant.
- Aligner modele domaine, ORM, validations admin et serialization API.
- Ajouter les messages d'erreur metier et les badges UI admin.
- Ajouter tests unitaires et tests d'integration sur les transitions valides et invalides.

Definition of done :
- Le back-office ne permet plus de persister un statut hors referentiel.
- Les APIs et vues detail exposent un statut coherent.
- La creation d'un commercant initialise `BROUILLON` sans traitement manuel complementaire.

### Story `PRD-002` - Bloquer l'exposition des prestations d'un commercant inactif

Priorite : `P0`
Statut : `Termine`

Valeur metier : empecher l'achat de prestations rattachees a un commercant non actif.

Criteres d'acceptation :
- Une prestation rattachee a un commercant non `ACTIF` n'apparait pas comme achetable sur la marketplace.
- La prestation possede un statut distinct, pilotable metierement.
- Un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas conserver de prestations aux statuts `ACTIVE`, `BROUILLON` ou `REFERENCE`.
- Le systeme explique la contrainte lors d'un changement de statut commercant ou d'une mise a jour de prestation incompatible.

Taches :
- Introduire ou centraliser le statut metier de prestation.
- Identifier le point de filtrage catalogue pour exclure les prestations non achetables.
- Ajouter la validation metier lors du passage d'un commercant vers `SUSPENDU` ou `ARCHIVE`.
- Ajouter les tests de non exposition cote catalogue et back-office.

Definition of done :
- Une prestation d'un commercant non actif ne peut plus etre achetee ni exposee par erreur.
- Le statut prestation est visible et exploitable dans les surfaces d'administration et d'API necessaires.

### Story `PRD-003` - Activer un commercant et ses prestations de maniere controlee

Priorite : `P0`
Statut : `Termine`

Valeur metier : rendre la publication du catalogue pilotable et reversible.

Criteres d'acceptation :
- Le passage d'un commercant a `ACTIF` ne rend eligible le catalogue que si les preconditions definies sont satisfaites.
- Les prestations et coffrets relies suivent les regles de publication prevues.
- Le coffret possede un statut distinct, pilotable metierement.
- Le back-office donne un retour explicite en cas d'echec d'activation.

Taches :
- Introduire ou centraliser le statut metier de coffret.
- Definir la commande ou le workflow de changement de statut commercant.
- Ajouter les prechecks de coherence avant activation.
- Exposer les blocages fonctionnels dans l'admin.
- Ajouter tests d'activation reussie et refusee.

Definition of done :
- L'activation d'un commercant suit un workflow determine et verifiable.
- Le statut coffret est visible et exploitable dans les surfaces d'administration et d'API necessaires.

### Story `PRD-015` - Interdire les coffrets actifs pour un commercant en brouillon ou reference

Priorite : `P0`
Statut : `Termine`

Valeur metier : eviter les coffrets commercialisables alors que le commercant n'est pas encore actif.

Criteres d'acceptation :
- Un commercant `BROUILLON` ou `REFERENCE` ne peut pas avoir de coffret actif.
- Toute tentative d'activer un coffret rattache a un commercant non `ACTIF` est refusee.
- Le message d'erreur indique le commercant bloqueur et le statut attendu.

Taches :
- Utiliser le statut de coffret comme source de verite de l'activation catalogue.
- Ajouter la validation sur activation de coffret et sur changement de statut commercant.
- Ajouter controle dans l'admin et, si applicable, dans les use cases/API.
- Ajouter tests de regression sur activation de coffret.

Definition of done :
- Aucun coffret actif ne peut rester rattache a un commercant `BROUILLON` ou `REFERENCE`.

### Story `PRD-016` - Bloquer suspension et archivage si usage de coffrets en cours

Priorite : `P0`
Statut : `Termine`

Valeur metier : proteger les clients et l'integrite des coffrets deja vendus ou en cours d'usage.

Criteres d'acceptation :
- Si au moins une prestation du commercant est rattachee a un coffret actif et qu'il existe au moins une coffret instance en cours, le commercant ne peut pas passer a `SUSPENDU` ni `ARCHIVE`.
- Une `coffret instance en cours` est definie comme une instance achetee en statut `ACTIVE` ou `EN_ATTENTE_ACTIVATION`.
- Le refus indique au moins le nombre de coffrets/prestations/instances bloquantes, ou une liste exploitable en back-office.
- Si aucune instance en cours n'existe, la suspension ou l'archivage reste possible selon les autres regles.

Taches :
- Definir precisement la requete de controle des dependances entre commercant, prestations, coffrets et coffrets instances.
- Ajouter une verification transactionnelle dans le use case de changement de statut commercant.
- Ajouter une restitution lisible des dependances bloquantes dans l'admin.
- Ajouter tests unitaires, integration repository et cas de bord.

Definition of done :
- Le systeme refuse de casser une offre en cours d'utilisation.
- Le controle s'appuie explicitement sur les instances `ACTIVE` et `EN_ATTENTE_ACTIVATION`.

## Chantiers transverses

### BX-EP1-01 - Normalisation des statuts

Priorite : `P0`

Livrables :
- enum ou constantes metier pour statuts commercant ;
- enum ou constantes metier pour statuts coffret ;
- enum ou constantes metier pour statuts prestation ;
- documentation technique des transitions autorisees.

### BX-EP1-02 - Validations back-office

Priorite : `P0`

Livrables :
- messages d'erreur fonctionnels ;
- controles sur formulaires admin ;
- affichage des blocages et dependances.

### BX-EP1-03 - Adaptation persistence et requetes

Priorite : `P0`

Livrables :
- migration pour le statut coffret et le statut prestation ;
- changement du defaut de creation commercant vers `BROUILLON` ;
- repositories ou requetes de comptage des dependances ;
- optimisation SQL pour eviter les controles en memoire.

### BX-EP1-04 - Couverture de tests

Priorite : `P0`

Livrables :
- tests unitaires sur regles de transition ;
- tests d'integration repository/use cases ;
- tests de non regression admin ou API selon surface exposee.

### BX-EP1-05 - Documentation et rollout

Priorite : `P1`

Livrables :
- specification fonctionnelle mise a jour ;
- release note de la gouvernance catalogue ;
- guide court de reprise des donnees existantes si necessaire.

## Dependances

- Epic 2 pour les regles de protection de prestation deja rattachee a des coffrets.
- Definition metier detaillee des transitions autorisees pour les statuts coffret et prestation.

## Ordre recommande de livraison

1. `PRD-001` + `BX-EP1-01`


   - Statut : `Termine`
2. `PRD-002`

   - Statut : `Termine`
3. `PRD-015`

   - Statut : `Termine`
4. `PRD-016`

   - Statut : `Termine`
5. `PRD-003`

   - Statut : `Termine`
6. `BX-EP1-02`, `BX-EP1-03`, `BX-EP1-04` en continu
7. `BX-EP1-05` en cloture

## Proposition de tickets implementables

- `EP1-T01` Normaliser les statuts commercant dans le domaine, l'ORM et l'admin.
- `EP1-T02` Definir `BROUILLON` comme statut par defaut a la creation d'un commercant.
- `EP1-T03` Filtrer le catalogue pour exclure les prestations de commercants non actifs.
- `EP1-T04` Introduire ou formaliser le statut des prestations pour supporter les controles metier.
- `EP1-T05` Introduire ou formaliser le statut des coffrets pour supporter l'activation controlee.
- `EP1-T06` Bloquer l'activation d'un coffret si le commercant associe n'est pas `ACTIF`.
- `EP1-T07` Bloquer le passage d'un commercant a `SUSPENDU` ou `ARCHIVE` si prestations incompatibles.
- `EP1-T08` Bloquer suspension/archivage si coffret actif + coffret instance en cours (`ACTIVE` ou `EN_ATTENTE_ACTIVATION`).
- `EP1-T09` Afficher les motifs de blocage dans le back-office.
- `EP1-T10` Ajouter les tests unitaires et integration de l'epic.
- `EP1-T11` Documenter les regles de gestion et les transitions de statut.
