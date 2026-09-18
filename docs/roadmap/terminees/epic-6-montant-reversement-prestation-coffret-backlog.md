# Backlog Epic 6 - Montant de reversement sur prestation coffret

## Perimetre

Epic source : `Epic 6. Montant de reversement sur prestation coffret`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : ajouter sur chaque `PrestationCoffret` un `montant_reversement` servant de base au calcul des mouvements de reversement commercant.

## Statut global

- Epic 6 : `Termine`
- Avancement : specification produit et technique prete pour implementation.

## Regles de gestion consolidees

- Chaque `PrestationCoffret` doit porter un `montant_reversement`.
- Le `montant_reversement` est obligatoire des la creation d'une `PrestationCoffret`.
- Le `montant_reversement` est saisi en gestion.
- Le `montant_reversement` reste modifiable apres creation.
- Le `montant_reversement` est distinct du prix client du coffret.
- Le `montant_reversement` est la source de verite pour les mouvements de reversement lies a la consommation de la prestation.
- Une validation de prestation cree un `MouvementReversement` base sur le `montant_reversement` de la `PrestationCoffret`.
- Une invalidation de validation de prestation controle et annule un mouvement base sur ce montant.

## Flux cible recommande

1. L'admin cree ou modifie une `PrestationCoffret`.
2. Il renseigne un `montant_reversement`.
3. Lors d'une validation de prestation :
   - le backend charge la `PrestationCoffret` ;
   - lit son `montant_reversement` ;
   - cree le `MouvementReversement` avec ce montant.
4. Lors d'une invalidation de validation :
   - le backend retrouve le mouvement cree ;
   - verifie sa coherence avec le `montant_reversement` de la prestation ;
   - l'annule si les conditions V1 sont remplies.

## Evolutions de modele recommandees

### `PrestationCoffret`

Ajouter :
- `montant_reversement`

Contraintes :
- non nul des la creation ;
- valeur positive ou nulle selon la politique metier retenue ;
- modifiable en back-office ;
- visible dans SQLAdmin.

## Use cases impactes

- `ValiderPrestation`
  - utilise `prestation_coffret.montant_reversement` pour creer le mouvement de reversement.
- `InvaliderValidationPrestation`
  - verifie la coherence du mouvement a annuler avec le `montant_reversement` de la prestation.

## Erreurs metier recommandees

- `MontantReversementRequis`
- `MontantReversementInvalide`
- `PrestationSansMontantReversement`

## Surfaces recommandees

### V1

- SQLAdmin sur `PrestationCoffret`
- use cases de validation et d'invalidation

### Hors perimetre V1

- edition commercant du `montant_reversement`
- historique des changements de montant

## Criteres d'acceptation

1. Une `PrestationCoffret` peut porter un `montant_reversement`.
2. Le champ est editable dans SQLAdmin.
3. La creation d'une prestation sans `montant_reversement` est refusee.
4. `ValiderPrestation` cree un mouvement de reversement base sur ce montant.
5. L'invalidation d'une validation retrouve un mouvement coherent avec ce montant.

## Backlog priorise

### Story `PRD-023` - Saisir un montant de reversement sur une prestation

Priorite : `P0`
Statut : `Termine`

Valeur metier : disposer d'une base explicite et pilotable pour la remuneration commercant.

Criteres d'acceptation :
- `PrestationCoffret` porte un `montant_reversement`.
- Le champ est visible et editable en gestion.
- La creation d'une prestation sans ce champ est refusee.
- Le champ reste modifiable apres creation.
- Les validations de coherence sont appliquees.

### Story `PRD-024` - Utiliser le montant de reversement dans les mouvements financiers

Priorite : `P0`
Statut : `Termine`

Valeur metier : garantir que les reversements utilisent une regle metier explicite.

Criteres d'acceptation :
- la creation d'un `MouvementReversement` reprend le `montant_reversement` de la prestation ;
- aucun montant fixe code en dur n'est encore utilise dans `ValiderPrestation`.

### Story `PRD-025` - Rendre l'invalidation coherente avec le montant de reversement

Priorite : `P1`
Statut : `Termine`

Valeur metier : garder une coherence financiere lors de l'annulation d'une validation de prestation.

Criteres d'acceptation :
- l'invalidation verifie la coherence entre prestation et mouvement financier ;
- le mouvement annule correspond bien au montant de reversement de la prestation.

## Chantiers transverses

### BX-EP6-01 - Evolution du modele et de la persistence

Priorite : `P0`

Livrables :
- champ domaine `montant_reversement` ;
- colonne ORM associee ;
- migration SQL.

### BX-EP6-02 - Surface SQLAdmin

Priorite : `P0`

Livrables :
- affichage du `montant_reversement` ;
- edition du `montant_reversement` ;
- validations de saisie.

### BX-EP6-03 - Impacts use cases financiers

Priorite : `P0`

Livrables :
- mise a jour de `ValiderPrestation` ;
- preparation du branchement avec `InvaliderValidationPrestation`.

## Ordre recommande de livraison

1. `PRD-023`

   - Statut : `Termine`
2. `PRD-024`
   - Statut : `Termine`
3. `PRD-025`
   - Statut : `Termine`

## Proposition de tickets implementables

- `EP6-T01` Ajouter `montant_reversement` au modele `PrestationCoffret`.
- `EP6-T02` Ajouter la colonne ORM et la migration SQL correspondante.
- `EP6-T03` Exposer `montant_reversement` dans SQLAdmin.
- `EP6-T04` Ajouter les validations de saisie sur `montant_reversement`.
- `EP6-T05` Utiliser `montant_reversement` dans `ValiderPrestation`.
- `EP6-T06` Brancher la coherence `montant_reversement` dans `InvaliderValidationPrestation`.
