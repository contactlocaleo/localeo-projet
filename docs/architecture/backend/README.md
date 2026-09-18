# Architecture du backend

Ce répertoire conserve les descriptions et décisions d'architecture du backend Localeo. Les règles et contrats partagés avec les interfaces restent dans les [spécifications canoniques par fonctionnalité](../../specifications/INDEX.md).

## Repères

- [Architectures par EPIC](epics/README.md) : conceptions et synthèses existantes, avec leur portée historique.
- [Architecture transverse](../transverse/README.md) : conventions communes, couches, API, back-office et sécurité.
- [ADR](../decisions/README.md) : décisions structurantes, datées et traçables.
- [Templates](../templates/README.md) : structures de conception et de décision à utiliser selon le besoin.

## Faire évoluer la conception

Pour une nouvelle initiative, enrichir d'abord la spécification canonique du sujet : règles, invariants, contrats, applications concernées et preuves attendues. Réutiliser son dossier et ses identifiants d'arbitrage. Ne pas créer systématiquement un document concurrent dans `epics/`.

Une conception longue déjà présente ici peut rester sa référence d'architecture, avec un lien explicite depuis la spécification. Son ancienneté ne prouve ni le statut produit courant ni le déploiement ; consulter la [roadmap commune](../../roadmap/README.md) pour le suivi.

Les choix applicables à plusieurs sujets relèvent des [conventions transverses](../transverse/README.md). Une décision structurante se trace dans une ADR reliée au sujet. Les documents décrivent responsabilités, objets, transitions et contrats ; ils ne doivent pas recopier un catalogue de classes que le code maintient déjà.
