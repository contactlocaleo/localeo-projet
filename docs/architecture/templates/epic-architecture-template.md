# Architecture applicative EPIC XX - Nom

## Statut

- Version :
- Source backlog :
- Portee :
- Hors portee :

## Objectif applicatif

Ce que l'architecture doit permettre.

## Choix d'architecture

Decisions structurantes prises pour repondre a l'EPIC.

## Objets manipules ou crees

Objets metier, projections, tokens, evenements, documents, batchs, etc.

## Modele de domaine

### Agregats et entites

Pour chaque agregat modifie, indiquer sa racine, les objets qu'il protege et les operations metier exposees.

### Invariants et transitions

Lister les regles qui doivent rester vraies quel que soit le point d'entree, puis identifier leur porteur :
entite, objet-valeur ou service de domaine pur. Decrire les transitions de statut autorisees et refusees.

### Responsabilites applicatives

Limiter cette section au chargement des objets, au controle du perimetre d'acces, a la transaction, aux ports,
a la persistance et aux effets secondaires. Toute regle metier conservee dans cette couche doit etre justifiee.

Verification obligatoire : la conception respecte
l'[ADR domaine d'abord](../decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md).

## Vue applicative

Diagramme Mermaid : surfaces, use cases, domaines, dependances.

## Flux principaux

1 a 3 flux Mermaid maximum, seulement si utile.

## Frontieres avec les autres domaines

Ce que l'EPIC possede, consomme ou ne doit pas dupliquer.

## Securite / audit / idempotence

Seulement si concerne.

## Points ouverts

Decisions restantes, risques, arbitrages futurs.
