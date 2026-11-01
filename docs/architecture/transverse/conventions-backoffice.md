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

### Gabarit des pages Localeo ERP

Harmonisation du **31 octobre 2026** : les pages métier ERP utilisent la même
structure, dans le shell principal, les consoles Animation et les vues
administratives spécifiques ouvertes depuis l'ERP.

1. **En-tête d'application** : identité ERP et menu Applications commun ; pas
   de deuxième marque Localeo ou de commandes métier dans ce menu.
2. **Menu ERP** : une source partagée, destinations filtrées par les droits,
   rubrique courante ouverte et une seule entrée active. Sur mobile, bouton
   **Rubriques ERP**, ouverture explicite et fermeture avec Échap, même après
   déplacement du focus dans le contenu.
3. **Repérage de page** : fil d'Ariane et un seul retour explicite, puis titre
   unique, description et actions contextualisées. Une arrivée directe conserve
   un parent structurel ; elle ne dépend pas de l'historique du navigateur.
4. **Actions** : action de page dans la zone prévue à côté du titre, secondaires
   à la suite. Création sur l'accueil ou la liste concernée seulement.
   Actualisation et exports de Finance/Audit utilisent cette zone ; les
   confirmations et validations de formulaires restent auprès de leur saisie.
5. **Contenu** : aligné à gauche sur la largeur disponible, marges et typographie
   communes, tableaux débordants contenus dans leur propre zone. Les champs et
   textes peuvent garder une largeur de lecture adaptée à leur usage.

Implémentation partagée : `page-layout.js`, `page-layout.css` et
`erp-navigation.js` dans le backend. La navigation Animation réutilise ce
gabarit et conserve ses parents spécifiques. Les règles de menu sont limitées
à sa classe ; aucune règle globale `nav` ne doit recolorer un fil d'Ariane ou
une navigation métier. Modifier la source commune plutôt qu'empiler des
surcharges dans chaque écran.

Les retours Finance/Audit conservent leurs filtres privés, leur pagination et
leur focus sans recopier les recherches sensibles dans une URL partagée. Les
paramètres d'un parent ne sont repris que depuis son URL de même origine.
Les protections des saisies non enregistrées, permissions, CSRF, versions,
confirmations et clés d'idempotence sont conservées. Une réponse de navigation
arrivée après expiration de session ne doit pas réafficher les liens privés.

Instances utilise le gabarit ERP sans modifier son habillage Support autonome.
Les pages d'action d'instance conservent leur menu contextuel Support, avec
la même géométrie et un seul en-tête. Ops, Support, OnBoard, Atelier et les
écrans de connexion restent des applications ou parcours distincts ; leurs
menus ne sont pas remplacés par celui de l'ERP. Les formulaires techniques
standard de SQLAdmin gardent le gabarit de cet outil ; les vues spécifiques
enveloppées par le backend partagent le gabarit ERP.

Preuves et limites du correctif : [vérification des vues ERP](../../specifications/epic-65-vues-erp/verification-livraison.md#harmonisation-du-gabarit-erp--31-octobre-2026).

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

### Lisibilité du menu ERP — 1er novembre 2026

Le menu partagé distingue **Pilotage**, **Animations locales**, **Activité
quotidienne**, **Catalogue et commerçants** et **Administration**. Les rubriques
fonctionnelles sont séparées visuellement et repliables. Animation conserve
ses quatre sous-rubriques, également repliables : Animations, Équipes et
contrats, Offre et modules, Pilotage. La page courante ouvre tous ses parents ;
l’accueil Animation ouvre aussi la première sous-rubrique pour exposer ses
accès principaux.

Chaque lien garde un libellé visible et reçoit une icône SVG décorative locale,
sans police ni chargement extérieur. Une couleur contrastée et le repère
`aria-current` identifient la destination active. Les liens conservent leurs
URL et leur filtrage par habilitation ; les rubriques sans destination
autorisée disparaissent. Un accès à une fonction Animation reste visible même
si l’opérateur n’a pas accès à sa vue d’ensemble.

Les groupes utilisent les éléments natifs `details`/`summary` : Entrée ou
Espace pour ouvrir, Tab pour les liens visibles. Sur mobile, **Rubriques ERP**
reste accessible pendant le défilement du menu ; Échap ferme le menu et rend
le focus au bouton. Cibles d’au moins 44 px et textes agrandis sont préservés.
Ces principes concernent le menu ERP partagé et ses consoles historiques,
sans remplacer les menus contextuels Support ni le menu technique SQLAdmin.

Preuves : [vérification du menu ERP](../../specifications/epic-65-vues-erp/verification-livraison.md#lisibilité-du-menu-erp--1er-novembre-2026).

