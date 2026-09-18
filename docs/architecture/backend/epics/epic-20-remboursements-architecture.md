# Architecture applicative EPIC 20 - Gestion des remboursements

## Statut

- Version : retro-documentation v1
- Source backlog : [Epic 20 - Gestion remboursements](../../../roadmap/terminees/epic-20-gestion-remboursements-backlog.md)
- Portee : architecture applicative du remboursement operationnel MVP.
- Hors portee : specification technique detaillee des classes, schemas SQL exhaustifs et contrats API detailles.

## Objectif applicatif

Gerer de bout en bout les remboursements lies a l'annulation d'un coffret paye, avec une trace exploitable par le support et le back-office.

## Choix d'architecture

- Traiter le remboursement MVP comme une obligation operationnelle suivie, pas comme une execution PSP automatique.
- Refuser le remboursement partiel standard en MVP.
- Invalider la `CoffretInstance` et les prestations non consommees lors de l'annulation.
- Distinguer demande, validation support et execution externe.
- Notifier le client aux etapes importantes.

## Objets manipules ou crees

- `AchatCoffret`
- `Paiement`
- `CoffretInstance`
- `StatutPrestationCoffretInstance`
- remboursement ou demande de remboursement
- reference externe d'execution
- email de notification client

## Vue applicative

```mermaid
flowchart LR
    Support["Support / back-office"] --> Annulation["Annulation coffret"]
    Annulation --> Instance["CoffretInstance invalidee"]
    Annulation --> Remboursement["Obligation remboursement"]
    Remboursement --> Execution["Execution externe manuelle"]
    Execution --> Notification["Email client"]
```

## Flux principaux

Voir la vue applicative ci-dessus ; aucun flux detaille complementaire n'est documente a ce niveau.

## Frontieres avec les autres domaines

- `gestion_achats` porte l'annulation et l'etat de l'instance.
- `support` porte le traitement operationnel client.
- EPIC 39 peut remplacer l'execution manuelle par une execution Stripe lorsque le PSP est actif.

## Securite / audit / idempotence

- Les actions sensibles doivent etre protegees par les mecanismes d'acces existants.
- Les changements d'etat metier doivent etre auditables lorsque l'EPIC cree ou modifie une ressource.
- L'idempotence est requise pour les traitements relancables, integrations externes, batchs et notifications.

## Points ouverts

- Aucun point ouvert documente dans la retro-documentation initiale.
