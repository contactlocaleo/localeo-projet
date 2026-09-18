# Architecture applicative EPIC 23 - Gestion des batchs et ordonnancement

## Statut

- Version : retro-documentation v1
- Source backlog : [Epic 23 - Gestion batchs ordonnancement](../../../roadmap/terminees/epic-23-gestion-batchs-ordonnancement-backlog.md)
- Portee : architecture applicative d'inventaire, execution et supervision des batchs.
- Hors portee : specification technique detaillee des classes, schemas SQL exhaustifs et contrats API detailles.

## Objectif applicatif

Industrialiser les batchs Localeo avec une liste centralisee, un suivi d'execution, des politiques de retry et une supervision exploitable.

## Choix d'architecture

- Conserver les endpoints batch existants puis ajouter une couche de pilotage.
- Decrire chaque batch avec frequence, criticite, derniere execution et politique de reprise.
- Journaliser chaque execution.
- Rendre les batchs pilotables par l'exploitation.
- Alerter sur les echecs ou absences d'execution.
- L'intégration concrète d'APScheduler dans le service FastAPI est implémentée par
  l'[Epic 48](../../../roadmap/terminees/epic-48-apscheduler-ordonnancement-batchs-backlog.md).

## Objets manipules ou crees

- definition de batch
- execution de batch
- statut d'execution
- compteur traite / erreur
- politique de retry
- alerte batch
- endpoints batch proteges

## Vue applicative

```mermaid
flowchart LR
    Exploit["Exploitation"] --> Catalogue["Catalogue batchs"]
    Catalogue --> Runner["Execution batch"]
    Runner --> Journal["Journal execution"]
    Journal --> Supervision["Supervision et alertes"]
```

## Flux principaux

Voir la vue applicative ci-dessus ; aucun flux detaille complementaire n'est documente a ce niveau.

## Frontieres avec les autres domaines

- `exploitation` porte l'orchestration et la supervision.
- Chaque batch appelle les use cases du domaine metier concerne.
- L'ordonnancement ne doit pas porter de logique metier propre.

## Securite / audit / idempotence

- Les actions sensibles doivent etre protegees par les mecanismes d'acces existants.
- Les changements d'etat metier doivent etre auditables lorsque l'EPIC cree ou modifie une ressource.
- L'idempotence est requise pour les traitements relancables, integrations externes, batchs et notifications.

## Points ouverts

- Aucun point ouvert documente dans la retro-documentation initiale.
