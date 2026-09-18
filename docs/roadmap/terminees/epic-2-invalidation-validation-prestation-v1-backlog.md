# Backlog Epic 2 - Invalidation d'une validation de prestation V1

## Perimetre

Epic source : `Epic 2. Protection de l'integrite des coffrets`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : permettre d'invalider une validation de prestation faite par erreur, uniquement tant que le reversement associe n'est pas encore paye.

## Statut global

- Epic 2 - extension V1 invalidation validation : `Termine`
- Avancement : specification produit et technique prete pour implementation.

## Regles de gestion consolidees

- Une `ValidationPrestation` ne peut etre invalidee que si elle est actuellement active.
- Un motif d'invalidation est obligatoire.
- L'invalidation n'est autorisee en V1 que si le mouvement de reversement associe est en statut `A_REVERSER`.
- Si le mouvement de reversement associe est `EN_COURS_DE_REVERSEMENT`, `REVERSE` ou `ANNULE`, l'invalidation est refusee.
- L'invalidation remet la prestation a l'etat `A_VALIDER`.
- L'invalidation annule le mouvement de reversement associe.
- L'invalidation recalcule le statut de la `coffret instance`.
- Si la `coffret instance` etait `UTILISE` et qu'au moins une prestation redevient `A_VALIDER`, elle repasse `ACTIVE`.
- Si la `coffret instance` est deja `EXPIRE`, elle reste `EXPIRE`.
- `PrestationCoffret` doit porter un `montant_reversement` saisi en gestion.
- Le mouvement de reversement cree lors d'une validation de prestation utilise le `montant_reversement` de la `PrestationCoffret` et non une valeur en dur.
- Les donnees historiques ne sont pas supprimees physiquement : l'invalidation est logique et tracable.

## Flux cible recommande

1. Un admin selectionne une `ValidationPrestation` a invalider.
2. Le systeme verifie l'etat de la validation et du mouvement de reversement associe.
3. Si les preconditions sont satisfaites :
   - la validation passe a `INVALIDE` ;
   - la prestation repasse a `A_VALIDER` ;
   - le mouvement de reversement passe a `ANNULE` ;
   - le statut de la `coffret instance` est recalcule.
4. Le systeme enregistre le motif d'invalidation et l'acteur.

## Evolutions de modele recommandees

### `PrestationCoffret`

Ajouter :
- `montant_reversement`

Regles :
- montant obligatoire pour toute prestation activable ;
- montant saisi en gestion ;
- montant distinct du prix du coffret client ;
- montant utilise comme source de verite pour les mouvements de reversement.

### `ValidationPrestation`

Ajouter :
- `statut` : `VALIDEE` | `INVALIDE`
- `date_invalidation: datetime | None`
- `motif_invalidation: str | None`
- `invalidee_par: str | None`

### `MouvementReversement`

Reutiliser le statut existant :
- `ANNULE`

Ajout optionnel V1 :
- `date_annulation: datetime | None`
- `motif_annulation: str | None`

## Use case recommande

### `InvaliderValidationPrestation`

Entree :
- `validation_prestation_id`
- `motif`
- `acteur_id`
- `acteur_type`

Sequence :
1. Charger la `ValidationPrestation`.
2. Verifier qu'elle existe et qu'elle est invalidable.
3. Charger le `StatutPrestationCoffretInstance` associe.
4. Charger la `PrestationCoffret` associee.
5. Charger le `MouvementReversement` lie via `origine_validation_prestation_id`.
6. Verifier que le mouvement est bien en statut `A_REVERSER`.
7. Verifier la coherence du mouvement avec le `montant_reversement` de la `PrestationCoffret`.
8. Marquer la validation `INVALIDE`.
9. Enregistrer `date_invalidation`, `motif_invalidation`, `invalidee_par`.
10. Repasser la prestation a `A_VALIDER`.
11. Passer le mouvement de reversement a `ANNULE`.
12. Recalculer le statut de la `coffret instance`.
13. Commit.

Sortie :
- `validation_prestation_id`
- `statut_validation`
- `statut_prestation_coffret_instance`
- `statut_coffret_instance`
- `statut_mouvement_reversement`
- `motif`

## Regles de recalcul de `CoffretInstance`

- Si `coffret_instance.statut == EXPIRE`, conserver `EXPIRE`.
- Sinon, s'il existe au moins une prestation en `A_VALIDER`, positionner la `coffret instance` a `ACTIVE`.
- Sinon, positionner la `coffret instance` a `UTILISE`.

## Erreurs metier recommandees

- `ValidationPrestationIntrouvable`
- `ValidationPrestationDejaInvalidee`
- `MotifInvalidationRequis`
- `InvalidationValidationImpossible`
- `ReversementDejaEngage`
- `ReversementDejaPaye`
- `MontantReversementInvalide`

## Surfaces recommandees

### V1

- use case applicatif dedie
- action SQLAdmin sur la fiche `ValidationPrestation`

### Hors perimetre V1

- API publique/front d'invalidation
- compensation financiere si reversement deja paye
- annulation d'un reversement deja execute

## Criteres d'acceptation

1. Une validation avec mouvement de reversement `A_REVERSER` peut etre invalidee.
2. La prestation repasse a `A_VALIDER`.
3. Le mouvement de reversement associe passe a `ANNULE`.
4. La `coffret instance` est recalculee correctement.
5. Une validation liee a un mouvement `EN_COURS_DE_REVERSEMENT` est refusee.
6. Une validation liee a un mouvement `REVERSE` est refusee.
7. Le motif d'invalidation est obligatoire et conserve.
8. `PrestationCoffret` porte un `montant_reversement` utilise lors de la creation du mouvement financier.
9. L'operation est tracable dans l'admin.

## Backlog priorise

### Story `PRD-022` - Invalider une validation de prestation en erreur avant reversement paye

Priorite : `P0`
Statut : `Termine`

Valeur metier : corriger une validation erronee sans casser la coherence de consommation ni la coherence financiere.

Criteres d'acceptation :
- L'invalidation est possible uniquement si le mouvement de reversement associe est `A_REVERSER`.
- La prestation repasse a `A_VALIDER`.
- La `ValidationPrestation` est marquee `INVALIDE`.
- Le mouvement de reversement est marque `ANNULE`.
- La `coffret instance` est recalculee.
- Un motif d'invalidation est obligatoire.
- `PrestationCoffret` porte un `montant_reversement` utilise lors de la creation du mouvement financier.

Taches :
- Enrichir `PrestationCoffret` avec `montant_reversement`.
- Enrichir le modele `ValidationPrestation`.
- Ajouter les colonnes ORM et migration SQL associees.
- Ajouter les methodes repository manquantes pour lecture/mise a jour de `ValidationPrestation`.
- Ajouter une lecture de `MouvementReversement` par `origine_validation_prestation_id`.
- Utiliser `montant_reversement` lors de la creation du mouvement de reversement a la validation.
- Implementer le use case `InvaliderValidationPrestation`.
- Ajouter une action SQLAdmin dediee sur `ValidationPrestation`.

Definition of done :
- L'admin peut invalider une validation eligible.
- Les etats metier et financiers sont remis en coherence.
- Les cas non eligibles sont refuses avec une erreur explicite.

## Chantiers transverses

### BX-EP2-01 - Evolution du modele de validation

Priorite : `P0`

Livrables :
- montant de reversement sur `PrestationCoffret` ;
- statut de validation ;
- date d'invalidation ;
- motif d'invalidation ;
- acteur d'invalidation.

### BX-EP2-02 - Evolution du modele de reversement

Priorite : `P0`

Livrables :
- creation des mouvements a partir du `montant_reversement` de la prestation ;
- recuperation du mouvement lie a une validation ;
- annulation logique du mouvement en V1.

### BX-EP2-03 - Surface SQLAdmin

Priorite : `P1`

Livrables :
- action `Invalider validation` ;
- saisie du motif ;
- affichage du statut d'invalidation.

## Ordre recommande de livraison

1. `BX-EP2-01`
2. `BX-EP2-02`
3. `PRD-022`
   - Statut : `Termine`
4. `BX-EP2-03`

## Proposition de tickets implementables

- `EP2-T00` Ajouter `montant_reversement` sur `PrestationCoffret`.
- `EP2-T01` Ajouter le statut logique d'une `ValidationPrestation`.
- `EP2-T02` Ajouter `date_invalidation`, `motif_invalidation`, `invalidee_par`.
- `EP2-T03` Ajouter les methodes repository `obtenir` et `mettre_a_jour` sur `ValidationPrestation`.
- `EP2-T04` Ajouter un acces `obtenir_par_validation` sur `MouvementReversement`.
- `EP2-T05` Utiliser `montant_reversement` lors de la creation du mouvement de reversement a la validation.
- `EP2-T06` Implementer le use case `InvaliderValidationPrestation`.
- `EP2-T07` Recalculer automatiquement le statut de la `CoffretInstance` apres invalidation.
- `EP2-T08` Ajouter l'action SQLAdmin sur `ValidationPrestation`.
- `EP2-T09` Documenter la regle d'invalidation V1 et ses limites.
