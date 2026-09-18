# Architecture applicative EPIC 12 - Traitement des reversements et export paiements

## Statut

- Version : retro-documentation v1 - decommissionnee par EPIC 39
- Source backlog : [Epic 12 - Traitement reversements export paiements](../../../roadmap/abandonnees/epic-12-traitement-reversements-export-paiements-backlog.md)
- Portee : architecture historique du traitement manuel des reversements, conservee uniquement pour comprehension et audit.
- Hors portee : specification technique detaillee des classes, schemas SQL exhaustifs et contrats API detailles.

## Objectif applicatif

Documenter l'ancien flux manuel de preparation, export et confirmation des
paiements de reversement commercant. Ce flux est completement decommissionne par
l'EPIC 39 et ne doit pas etre conserve comme fallback ni comme retrocompatibilite
operationnelle.

## Choix d'architecture

- Separer les mouvements a reverser de leur paiement effectif.
- Regrouper les reversements dans des lots exportables.
- Supprimer le flux banque manuel des modes d'execution cibles.
- Exiger une confirmation explicite du paiement execute.
- Auditer export, confirmation et erreurs de paiement.

## Objets manipules ou crees

- `MouvementReversement`
- `Reversement`
- `LigneReversement`
- `LotPaiementReversement`
- `PaiementReversement`
- export de paiement
- statut de traitement

## Vue applicative

```mermaid
flowchart LR
    BO["Back-office finance"] --> Selection["Selection mouvements"]
    Selection --> Lot["LotPaiementReversement"]
    Lot --> Export["Export paiement"]
    Export --> Banque["Execution banque manuelle<br/>historique"]
    Banque --> Confirmation["Confirmation paiement<br/>historique"]
    Confirmation --> Paiement["PaiementReversement"]
```

## Flux principaux

Voir la vue applicative ci-dessus ; aucun flux detaille complementaire n'est documente a ce niveau.

## Frontieres avec les autres domaines

- `gestion_reversement` porte le cycle financier commercant.
- L'infrastructure porte uniquement la generation technique des exports.
- EPIC 39 remplace ce mode historique par Stripe Connect et supprime toute
  execution manuelle operationnelle.

## Securite / audit / idempotence

- Les actions sensibles doivent etre protegees par les mecanismes d'acces existants.
- Les changements d'etat metier doivent etre auditables lorsque l'EPIC cree ou modifie une ressource.
- L'idempotence est requise pour les traitements relancables, integrations externes, batchs et notifications.

## Points ouverts

- Aucun point ouvert documente dans la retro-documentation initiale.
