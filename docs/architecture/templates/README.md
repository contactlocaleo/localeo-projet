# Templates d'architecture

## Modèles disponibles

- [Conception d'une EPIC](epic-architecture-template.md) : structure de référence lorsqu'un document de conception est nécessaire.
- [ADR](adr-template.md) : structure d'une décision d'architecture datée et argumentée.

## Utilisation

Enrichir d'abord le dossier de [spécification canonique](../../specifications/INDEX.md) du sujet. Un template n'impose ni document supplémentaire pour une petite correction, ni copie concurrente d'une conception existante. Conserver un lien vers les architectures historiques encore utiles et vers les ADR applicables.

Le document doit rendre lisibles les responsabilités, les objets manipulés, les invariants, les contrats et les preuves attendues. Adapter le niveau de détail au changement ; les sections sans objet doivent rester explicites plutôt qu'être remplies artificiellement.

Préférer Mermaid pour des diagrammes lisibles dans le dépôt ; PlantUML reste possible lorsqu'il répond à un besoin de représentation plus complexe. Garder les modèles cohérents avec les [conventions transverses](../transverse/README.md).
