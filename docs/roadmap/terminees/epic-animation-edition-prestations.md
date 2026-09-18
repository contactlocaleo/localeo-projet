# Epic - Animer / modifier le contenu de mes prestations

> État de classement : **Terminée**. Identifiant conservé : `EPIC-PRES-CONTENU-001`. Le parcours d’édition directe existe dans la [spécification de la version actuelle](../../specifications/espace-commercant/README.md) et dans le [constat de l’EPIC 62](../a-faire/epic-62-validation-modifications-prestations-backlog.md) ; le futur sas de validation reste porté par cette dernière.

## Epic

**ID**  
EPIC-PRES-CONTENU-001

**Nom**  
Animer / modifier le contenu de mes prestations

**Objectif**  
Permettre au commerçant de piloter le contenu visible de ses prestations depuis son espace commerçant, afin de garder une offre claire, attractive et à jour.

**Valeur métier**
- Donner plus d'autonomie au commerçant sur son offre.
- Réduire la dépendance au support pour les mises à jour simples.
- Améliorer la qualité éditoriale des prestations visibles côté client.
- Renforcer la fraîcheur commerciale des contenus diffusés dans l'écosystème Localeo.

**Définition of done de l'epic**
- Le commerçant peut consulter la liste de ses prestations.
- Il peut ouvrir le détail d'une prestation.
- Il peut modifier les champs autorisés du contenu.
- Les changements sont enregistrés et visibles après rechargement.
- Les cas d'erreur, de verrouillage métier et d'accès non autorisé sont gérés.

## Périmètre fonctionnel

**Inclus**
- Liste des prestations du commerçant connecté.
- Consultation du détail d'une prestation.
- Édition du contenu métier autorisé.
- Validation de formulaire.
- Sauvegarde avec confirmation de succès.
- Gestion des erreurs métier et techniques.

**Exclus dans cette version**
- Édition en masse.
- Gestion avancée des médias.
- Workflow de validation éditoriale multi-acteurs.
- Programmation de publication.
- Historique détaillé avant / après.

## Règle métier d'éditabilité

Seules les prestations dans les statuts suivants sont éditables :
- `ACTIVE`
- `BROUILLON`
- `REFERENCE`

Toute prestation dans un autre statut est consultable si le produit l'autorise, mais non modifiable.

## Hypothèses produit MVP

Les champs modifiables au MVP sont :
- nom / libellé commercial
- description

Les champs suivants sont visibles mais non modifiables au MVP :
- montant reversé au commerçant

Les champs suivants restent hors MVP sauf décision explicite :
- rattachement du commerçant
- tarification structurante côté pack
- reversements
- données techniques internes

## User stories

### PRES-CONT-US-001 - Voir la liste de mes prestations
**Priorité**  
P1

**User story**  
En tant que commerçant, je veux voir la liste de mes prestations afin de choisir rapidement celle que je souhaite mettre à jour.

**Critères d'acceptation**
- La liste affiche uniquement les prestations du commerçant connecté.
- Chaque ligne affiche au minimum le nom, le statut et un indicateur d'éditabilité.
- Une action `Voir / modifier` est disponible sur les prestations autorisées.

### PRES-CONT-US-002 - Consulter le détail d'une prestation
**Priorité**  
P1

**User story**  
En tant que commerçant, je veux consulter le détail d'une prestation afin de vérifier son contenu avant modification.

**Critères d'acceptation**
- Le détail affiche les champs utiles au parcours d'édition.
- Les champs non modifiables sont identifiés comme tels ou absents.
- L'écran permet d'entrer en mode édition si la prestation est modifiable.

### PRES-CONT-US-003 - Modifier le contenu autorisé d'une prestation
**Priorité**  
P1

**User story**  
En tant que commerçant, je veux modifier le contenu de ma prestation afin qu'il reflète mon offre réelle.

**Critères d'acceptation**
- Le formulaire est prérempli avec les données existantes.
- Le commerçant peut modifier uniquement le nom et la description.
- Le montant reversé est affiché à titre informatif, sans possibilité de modification.
- Les contraintes de longueur, de format et de complétude sont appliquées.

### PRES-CONT-US-004 - Enregistrer mes modifications
**Priorité**  
P1

**User story**  
En tant que commerçant, je veux enregistrer mes modifications afin qu'elles soient prises en compte par le système.

**Critères d'acceptation**
- Un bouton `Enregistrer` est disponible.
- En cas de succès, un message de confirmation est affiché.
- Les données modifiées sont visibles après rechargement.

### PRES-CONT-US-005 - Bloquer l'édition non autorisée
**Priorité**  
P1

**User story**  
En tant que système, je veux empêcher l'édition d'une prestation non autorisée afin de garantir la cohérence métier et la sécurité d'accès.

**Critères d'acceptation**
- Une prestation non éditable ne peut pas être enregistrée.
- Seules les prestations `ACTIVE`, `BROUILLON` ou `REFERENCE` peuvent être modifiées.
- L'API refuse la modification si la prestation n'appartient pas au commerçant connecté.
- Un message compréhensible est affiché côté front.

### PRES-CONT-US-006 - Gérer les erreurs de validation
**Priorité**  
P1

**User story**  
En tant que système, je veux contrôler les données saisies avant sauvegarde afin d'éviter les incohérences.

**Critères d'acceptation**
- Les champs obligatoires sont vérifiés.
- Les formats invalides sont refusés.
- Les messages d'erreur sont exploitables par l'utilisateur.

### PRES-CONT-US-007 - Annuler une modification en cours
**Priorité**  
P2

**User story**  
En tant que commerçant, je veux annuler mes changements non sauvegardés afin de revenir à l'état précédent.

**Critères d'acceptation**
- Une action `Annuler` ou `Retour` est disponible.
- Les données non enregistrées ne sont pas persistées.
- Une confirmation peut être demandée si le formulaire a été modifié.

### PRES-CONT-US-008 - Historiser la dernière mise à jour
**Priorité**  
P2

**User story**  
En tant que support ou administrateur, je veux connaître la date et l'auteur de la dernière modification afin de faciliter le suivi.

**Critères d'acceptation**
- La date de dernière modification est conservée.
- L'auteur de la modification est identifiable.
- Ces informations sont accessibles au minimum côté back-office ou logs.

## Découpage suggéré par lots

## Lot 1 - Consultation et édition MVP
- PRES-CONT-US-001 - Voir la liste de mes prestations
- PRES-CONT-US-002 - Consulter le détail d'une prestation
- PRES-CONT-US-003 - Modifier le contenu autorisé d'une prestation
- PRES-CONT-US-004 - Enregistrer mes modifications
- PRES-CONT-US-005 - Bloquer l'édition non autorisée
- PRES-CONT-US-006 - Gérer les erreurs de validation

## Lot 2 - Confort d'usage
- PRES-CONT-US-007 - Annuler une modification en cours

## Lot 3 - Traçabilité
- PRES-CONT-US-008 - Historiser la dernière mise à jour

## Open questions

- Le statut de visibilité est-il géré par le commerçant ou par un workflow interne ?
- Une prestation peut-elle être désactivée si elle est déjà liée à des packs vendus ?
- Faut-il distinguer contenu public, contenu opérationnel et contenu interne ?
