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

### UX des pages de gestion ERP

Ces règles s’appliquent à toute création ou évolution d’un écran métier ERP,
y compris les consoles Animation et les vues administratives spécifiques
ouvertes depuis l’ERP. Elles complètent le gabarit, la typographie et la navigation
décrits ci-dessous. Les formulaires techniques standard de SQLAdmin conservent
leur gabarit ; les tâches quotidiennes doivent privilégier un parcours métier
compréhensible et contextualisé.

La spécification retient les règles applicables au parcours et prévoit leurs
preuves. Une adaptation nécessaire est expliquée dans la spécification ou le
compte rendu du correctif, avec sa conséquence observable ; elle ne déclenche
pas une nouvelle procédure d’approbation. Une petite retouche ne demande pas
la refonte des écrans voisins ni l’exécution de toutes les recettes ERP.

#### ERP-UX-01 — Choisir une structure selon la tâche

Une page doit permettre de comprendre ce qui est géré, son état et l’action
utile. Une suite de textes, liens ou formulaires sans hiérarchie ne constitue
pas une page de gestion aboutie. Choisir le modèle qui correspond à la tâche :

| Modèle | Ordre de lecture attendu |
| --- | --- |
| Accueil de travail | Périmètre → dossiers à examiner → accès aux listes complètes → fonctions regroupées et décrites |
| Liste de gestion | Objectif → recherche et filtres → résultats comparables → actions de ligne → pagination |
| Fiche dossier | Identité et état → prochaine étape → sections métier → historique et détails techniques |
| Formulaire de décision | Cible et portée → saisie utile → conséquences et revue → confirmation adaptée → résultat |
| Console de diagnostic | Cible → symptôme et état → faits utiles → procédure et intervention autorisée → détails techniques |

Un accueil sans projection fiable des dossiers à traiter reste un répertoire
de tâches décrites. Un aperçu de file reste court et donne accès à la liste
complète ; sa taille ne devient pas un total de dossiers.

#### ERP-UX-02 — Identifier le dossier avant toute intervention

Le titre d’une fiche porte son nom métier. Organisation, commune, référence
utile et état restent proches du titre selon l’objet concerné. Une sélection
autorisée par nom et contexte évite le copier-coller d’UUID dans les parcours
courants ; les références techniques restent consultables et copiables en détail.
Distinguer les homonymes. Si l’identité manque, l’indiquer sans la reconstituer.
Changer de cible invalide l’ancien nom, l’aperçu et la confirmation associés.

#### ERP-UX-03 — Rendre les actions visibles et explicites

Mettre en avant l’action utile à l’état confirmé du dossier, lorsqu’elle peut
être déterminée. Grouper les secondaires par intention et séparer les opérations
rares ou sensibles. « Actualiser » reste un utilitaire. Placer les actions de
page dans l’en-tête, celles de section ou de ligne auprès de leur cible et les
validations de formulaire auprès de la saisie. Les filtres restent auprès des
résultats. L’export de la liste principale de Finance/Audit utilise la zone
d’actions de page ; l’export propre à une section reste auprès de son tableau.
Dans les deux cas, le libellé précise la portée, notamment « Exporter cette page ».

Utiliser un verbe et un résultat : « Examiner le blocage », « Ouvrir la commande »,
« Confirmer la préparation prête ». Un lien navigue ; un bouton agit sur la page
ou déclenche une commande. Un filtre de consultation ne définit jamais
implicitement la portée d’une commande globale. Un traitement collectif exige
une sélection explicite quand le domaine autorise ce mode de traitement.

#### ERP-UX-04 — Faciliter la comparaison et atteindre tous les résultats

Privilégier tableaux ou listes structurées pour comparer des dossiers. Conserver
identité, état, information discriminante et accès au dossier ; distinguer une
liste de catalogue d’une file de blocages. Présenter filtres actifs, résumé fiable
et pagination dans les deux sens. Une limite de recherche est annoncée et permet
de préciser la recherche ou de poursuivre la consultation.

Ne pas inventer un total ou un numéro de page à partir d’un curseur. Verrouiller
la pagination pendant une lecture, ignorer les réponses obsolètes et annoncer
les nouveaux résultats sans perdre le focus. Un lien tel que « Tous les coffrets »
doit ouvrir le périmètre annoncé. Préserver les légendes des valeurs sur mobile.

#### ERP-UX-05 — Distinguer consultation et édition

Une fiche lisible précède l’édition explicite de la section choisie. Éviter un
formulaire ouvert pour chaque ligne ou mesure. Un profil en lecture consulte les
informations sans pouvoir commencer une saisie vouée à un refus prévisible.
Présenter les actions selon les capacités effectives ; le serveur revérifie
toujours droits, périmètre et transitions. Une perte de droit en cours de travail
produit un refus explicite, sans affaiblir le contrôle.

#### ERP-UX-06 — Réduire l’effort de saisie

Grouper les champs par étape métier, expliquer les données requises et placer
l’aide détaillée dans une section progressive. Donner un titre et le focus à
l’éditeur ouvert. Fournir Enregistrer et Annuler ; après annulation, restituer
le focus au déclencheur encore présent ou à un repère pertinent.

Localiser les erreurs près des champs et conserver les valeurs en cas de refus
récupérable. Saisir les montants dans l’unité comprise par le gestionnaire,
indiquer devise et portée, convertir exactement les euros en centimes. Appliquer
la [convention des dates](affichage-dates.md) sans confondre date civile et instant.

#### ERP-UX-07 — Faire comprendre une décision et son résultat

Pour une commande sensible, montrer la cible nommée, la portée réelle, le montant
ou la période utiles, les conséquences et, pour une modification de conditions,
l’ancienne et la nouvelle valeur. La confirmation désigne l’opération ; une URL
technique ne suffit pas. Annuler n’envoie aucune commande.

Conserver confirmations, CSRF, version, audit et idempotence existants. Distinguer
décision, exécution et état confirmé. Un résultat incertain ne devient ni succès
ni échec certain : utiliser le reçu et les règles de reprise existants, sans
créer une seconde intention ni rejouer automatiquement une commande.

#### ERP-UX-08 — Préserver la continuité du travail

Le retour à une liste conserve les filtres, la page, le contexte de sélection
et le focus quand ils sont disponibles. Une arrivée directe dispose d’un parent
structurel autorisé. Réutiliser le mécanisme commun ; reprendre un parent
uniquement sur la même origine et le périmètre attendu. Après annulation d’une
sortie, le retour reste utilisable.

Avant changement de cible, filtre, page, section ou actualisation, protéger la
saisie non enregistrée : la conserver quand l’action le permet ou demander son
abandon. Une nouvelle version serveur ne doit pas être écrasée silencieusement.
Les brouillons privés restent en mémoire de l’onglet et sont purgés à expiration
ou changement d’identité. Ne pas recopier dossiers ou recherches sensibles dans
un stockage durable ou une URL partageable pour assurer le retour.

#### ERP-UX-09 — Traiter les états incomplets et les erreurs localement

Prévoir chargement, vide, absence de résultat, accès refusé, erreur de lecture,
conflit et résultat incertain selon le parcours. Une absence de donnée n’est pas
un zéro. Une erreur locale conserve les autres sections, les filtres et les
saisies autorisées ; elle propose une nouvelle tentative ciblée. Une réponse
tardive après expiration ne réaffiche aucune donnée privée.

Présenter états et causes dans un vocabulaire métier français, avec une suite
possible. Conserver les codes sources dans les détails utiles au diagnostic ;
un code inconnu reste explicite. Ne pas assimiler livraison, réception et lecture
d’une notification, ni transformer une installation technique en identité habitant.

#### ERP-UX-10 — Réutiliser des composants accessibles et denses

Employer les composants et styles partagés du gabarit ERP ; les consoles doivent
charger le même socle. Tableaux pour comparer, sections pour comprendre, formulaires
pour modifier : ne pas remplacer systématiquement les listes par des cartes.
Éviter les surcharges par écran qui réintroduisent des espacements ou contrôles
incohérents.

Conserver titres sémantiques, libellés visibles, noms accessibles, focus perceptible
et navigation clavier. Viser des cibles tactiles d’au moins 44 px pour les commandes
principales et fréquentes. Les liens en ligne et contrôles denses gardent une zone
activable et un espacement suffisants ; justifier les adaptations dans la recette.
La règle de 44 px du menu partagé reste applicable. La couleur seule ne porte
pas un état. Sur petit écran et avec texte agrandi, conserver contexte, légendes
et accès aux actions ; contenir le défilement d’un tableau dans sa propre zone.
Respecter la réduction des mouvements et les règles typographiques ci-dessous.

#### ERP-UX-11 — Afficher des faits fiables avec des lectures bornées

Le domaine reste propriétaire des décisions et de l’éligibilité ; l’interface
présente les faits et actions autorisés par les contrats. Ne pas inventer compteur,
affectation personnelle, urgence, délai ou gain de productivité. Relier un indicateur
à sa liste lorsqu’elle existe, en conservant le même périmètre.

Appliquer la [convention performance](performance-volumetrie.md) : recherche et
pagination serveur, bornes explicites, enrichissement groupé et lectures utiles
à la tâche. Ne pas charger tout un annuaire pour afficher une sélection ou lancer
une requête par ligne pour obtenir les noms. Les détails lourds se chargent à la
demande. Une amélioration de présentation ne prouve pas une amélioration de capacité.

#### ERP-UX-12 — Vérifier les parcours et entretenir les références

Reporter les preuves et limites dans la spécification ou le compte rendu existant.
Adapter le guide utilisateur aux libellés, menus et destinations livrés. Pour une
évolution de parcours, utiliser cette checklist sur les comportements concernés :

- [ ] Acteur, tâche, modèle de page, identité et portée sont identifiés.
- [ ] L’action utile est visible ; consultation, édition et opérations sensibles sont distinctes.
- [ ] Une arrivée directe et le parcours liste → dossier → retour fonctionnent, avec plusieurs pages si applicable.
- [ ] Les saisies résistent aux erreurs et aux navigations concernées ; annulation et reprise sont vérifiées.
- [ ] Les profils autorisé et restreint, les états vide/erreur/conflit et l’expiration sont couverts selon le changement.
- [ ] Le rendu est inspecté sur bureau, à 320/390 px et avec texte à 200 % ; clavier, focus, noms accessibles et libellés longs sont vérifiés sur le parcours modifié.
- [ ] Les lectures restent bornées et les mutations conservent leurs protections ; les recettes isolent les services réels.
- [ ] Les composants partagés, liens, aide et documentation sont cohérents ; les contrôles non exécutés restent explicites.

Réutiliser les recettes existantes et ajouter une preuve comportementale ciblée
pour une nouvelle interaction ou une régression. Une retouche rédactionnelle
simple ne requiert pas une nouvelle suite de tests. Une capture ne prouve pas
l’interactivité ; un contrôle automatisé ne remplace pas une recette au lecteur
d’écran, sur appareil physique ou avec des gestionnaires. Mesurer les gains réels
avant de les chiffrer.

Ces règles pérennisent les enseignements de l’[audit du 13 novembre 2026](../../audits/backend/localeo-erp-ux-pages-gestion-2026-11-13.md).
Le [bilan E60](../../specifications/epic-60-vision-360-commercialisation/ux-productivite.md#réalisation-et-bilan)
conserve la réalisation et les preuves datées ; il ne remplace pas ces conventions
pour les évolutions futures.

### Typographie des applications de gestion

Repères actualisés le **4 novembre 2026**, communs à Pro, Animation, ERP, Support,
Atelier, Ops, OnBoard et CRM, selon la [charte de référence CRM](identite-entetes-applications.md#charte-des-espaces-de-gestion-internes--référence-crm).
La typographie sert à parcourir rapidement des tâches, listes
et formulaires ; elle doit laisser les données et l'action principale visibles.

- Titres de page : 25 px, 23 px sur mobile, semi-gras (600), à la taille de texte standard
  du navigateur. Vérifier leur lisibilité au zoom et à l'agrandissement du texte.
  Les pages de gestion n'utilisent pas les grands titres promotionnels de la marketplace.
- Titres de section : 18 px ; sous-sections et cartes : 15 px, avec une
  adaptation à la densité du composant. Le niveau sémantique reste indépendant
  de la taille.
- Texte courant : base de 14 px. Les commandes, listes, tableaux et libellés
  peuvent rester à 14–16 px selon leur densité, avec une action principale
  identifiable par sa présentation et son placement. Conserver 16 px pour les
  champs sur mobile ; ne pas réduire les cibles tactiles avec la taille du texte.
- Utiliser la police système sans empattement pour les espaces de gestion,
  y compris Pro et Animation. Aucun chargement d’une nouvelle police n’est
  nécessaire. Les polices des contenus personnalisables restent distinctes.
- Réserver l'emphase aux états importants, montants et indicateurs ; éviter
  de mettre tous les titres, onglets et libellés en gras fort. Les compteurs
  et codes nécessaires à une opération gardent leur taille utile.
- Alléger le texte ne réduit pas les cibles tactiles, les pictogrammes, le
  contraste, le focus ni les confirmations. Vérifier le petit écran, les
  libellés longs et l'agrandissement du texte sur les parcours concernés.

La [signature des en-têtes](identite-entetes-applications.md) garde ses propres
règles : la marque n'est pas un titre de page. Les styles sont corrigés dans
leurs tokens et composants sources, sans multiplier les surcharges par écran.
Les formulaires techniques SQLAdmin conservent leur gabarit propre.
Constats et preuves : [audit typographique des applications de gestion](../../audits/typographie-applications-gestion-2026-11-03.md).

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
   Actualisation et exports de page de Finance/Audit utilisent cette zone ; les
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

