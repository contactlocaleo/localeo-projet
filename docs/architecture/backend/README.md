# Architecture applicative

Ce repertoire regroupe les decisions d'architecture applicative du backend Localeo.

## Organisation

- [Architectures par EPIC](epics/README.md) : un dossier applicatif par initiative produit ou technique.
- [Architecture transverse](../transverse/README.md) : conventions communes, decoupage solution, API, back-office et securite.
- [ADR](../decisions/README.md) : decisions d'architecture ponctuelles, datees et tracables.
- [Templates](../templates/README.md) : modeles a utiliser pour creer ou reprendre une documentation d'architecture.

## Regles d'usage

- Une EPIC significative doit avoir un document dans `epics/`.
- Les documents EPIC decrivent l'architecture applicative et les objets manipules, sans descendre dans le detail d'implementation des classes.
- Les choix transverses partages par plusieurs EPIC doivent etre documentes dans `transverse/`.
- Une decision structurante et reversible ou discutable doit etre formalisee en ADR.
- Les nouveaux documents EPIC doivent partir du template [epic-architecture-template.md](../templates/epic-architecture-template.md).

