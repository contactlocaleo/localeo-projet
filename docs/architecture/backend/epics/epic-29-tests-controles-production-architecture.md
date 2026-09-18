# Architecture applicative EPIC 29 - Tests et controles de production

## Statut

- Version : retro-documentation v1
- Source backlog : [Epic 29 - Tests controles production](../../../roadmap/terminees/epic-29-tests-controles-production-backlog.md)
- Portee : architecture applicative de controles operables avant et apres mise en production.
- Hors portee : specification technique detaillee des classes, schemas SQL exhaustifs et contrats API detailles.

## Objectif applicatif

Mettre en place des controles permettant de detecter les incoherences fonctionnelles critiques en environnement de production ou preproduction.

## Choix d'architecture

- Separer les tests automatises de build des controles operationnels.
- Fournir des controles lisibles par l'exploitation.
- Verifier les invariants critiques sans modifier les donnees.
- Produire un resultat exploitable : succes, alerte, erreur, details.
- Proteger l'execution par droits internes.

## Objets manipules ou crees

- controle de production
- resultat de controle
- invariant fonctionnel
- rapport de controle
- statut `OK`, `WARNING`, `ERROR`
- endpoint interne de controle

## Vue applicative

```mermaid
flowchart LR
    Exploit["Exploitation"] --> Controle["Runner controles"]
    Controle --> Donnees["Lectures domaines"]
    Donnees --> Rapport["Rapport controles"]
    Rapport --> Alerte["Alerte / suivi"]
```

## Flux principaux

Voir la vue applicative ci-dessus ; aucun flux detaille complementaire n'est documente a ce niveau.

## Frontieres avec les autres domaines

- Les controles ne corrigent pas automatiquement les donnees.
- Chaque domaine reste proprietaire de ses invariants.
- Les corrections passent par des use cases explicites.

## Securite / audit / idempotence

- Les actions sensibles doivent etre protegees par les mecanismes d'acces existants.
- Les changements d'etat metier doivent etre auditables lorsque l'EPIC cree ou modifie une ressource.
- L'idempotence est requise pour les traitements relancables, integrations externes, batchs et notifications.

## Points ouverts

- Aucun point ouvert documente dans la retro-documentation initiale.
