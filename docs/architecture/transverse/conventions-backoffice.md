# Conventions back-office

## Objectif

Le menu back-office doit refleter le decoupage fonctionnel du backend pour reduire l'ecart entre modele produit, code et exploitation.

## Domaines de navigation

- Referencement.
- Commercialisation.
- Gestion achats.
- Gestion reversement.
- Exploitation.
- Support.
- Profils.
- DAM.
- Documentaire.
- Identite et acces.
- Animation locale.

## Pilotage

Un raccourci transverse de pilotage global peut exister pour l'exploitation quotidienne.

Les vues specialisees doivent rester rattachees a leur domaine :

- reversements et paiements dans Gestion reversement ;
- clients, notes et contacts dans Support ;
- coffrets et prestations dans Commercialisation ;
- validations, transactions et incidents terrain dans Exploitation.

## Regles UX

- Un objet back-office doit etre accessible depuis le domaine qui porte sa responsabilite metier.
- Les duplications de vues doivent etre limitees a des raccourcis de pilotage.
- Les libelles de menu doivent rester proches des noms de domaines fonctionnels.

### Navigation Animation dans Localeo ERP

- Une entrée ouvre une fonctionnalité, avec une destination directe. Les
  rubriques regroupent les fonctions ; les actions « Nouveau » restent dans
  leur liste. Éviter plusieurs entrées vers des fragments d’une même page carrefour.
- L’en-tête fonctionnel réunit fil d’Ariane, titre, sous-titre et retour explicite.
  Une liste revient à l’espace Animation, un dossier à sa liste et un lot à son
  animation. L’arrivée directe utilise le même parent sans dépendre de l’historique.
- Reprendre les filtres d’un référent uniquement sur la même origine et le même
  parent. Ne pas contourner l’avertissement de saisie non enregistrée.
- Les destinations sont filtrées selon les habilitations. Un opérateur autorisé
  sur une console mais pas sur l’espace Animation revient à l’accueil ERP ; ne
  pas élargir ses droits pour fournir un retour.

Périmètre, compatibilité et preuves : [parcours E73](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md).

