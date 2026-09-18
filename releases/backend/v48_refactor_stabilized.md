# Localeo V48 - Stabilisation du refactoring AchatCoffret

Cette version prolonge la V47 pour aligner les couches principales sur le nouveau modèle :

## Renommages stabilisés
- Coffret prestation commerciale -> Coffret
- Prestation catalogue -> Prestation coffret
- CoffretClient supprimé
- PrestationCoffretClient -> StatutPrestationCoffretInstance

## Ancre unique
AchatCoffret devient l'ancre unique pour :
- le paiement
- les statuts des prestations instance
- les transactions de validation
- les validations de prestations

## Couches réalignées
- protocols repositories
- mappers ORM <-> domaine
- repositories SQLAlchemy
- unit of work
- principaux use cases paiement / validation / consultation
- principales routes API
