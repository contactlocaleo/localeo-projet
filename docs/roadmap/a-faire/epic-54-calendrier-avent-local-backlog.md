# Backlog Epic 54 - Calendrier de l'Avent local

## Synthese

- Criticite : `Moyenne`.
- Statut : `A developper - arbitrages et conception technique a finaliser`.
- Objectif : organiser une animation saisonniere unique composee de journees autonomes, chacune mettant en avant un commercant et donnant lieu a un tirage d'un coffret Localeo.
- Modele cible : `CALENDRIER_AVENT_LOCAL`.
- Dependances : Epics 41, 42, 46, 47, 48 et 49.

Voir [le cadrage fonctionnel](../../specifications/epic-54-calendrier-avent-local/README.md) et [le registre des arbitrages](../../specifications/epic-54-calendrier-avent-local/registre-arbitrages.md).

## Proposition MVP

- une animation composee de 12 ou 24 journees configurables ;
- une inscription globale au calendrier ;
- un commercant principal et un coffret a gagner par jour ;
- une visite validee par scan du QR participant, sans achat obligatoire ;
- une participation maximum par personne et par jour ;
- un tirage automatique quotidien avec reprise manuelle ;
- un gain maximum par personne sur l'ensemble du calendrier ;
- notification quotidienne soumise aux preferences Localeo Live.

## Responsabilites par surface

### Backoffice / backend Localeo

- enregistrer le modele et la notion generique de manche ou journee d'animation ;
- porter les statuts, horaires, populations eligibles, tirages et gains par journee ;
- executer ouverture, cloture et tirage par batch de maniere idempotente ;
- reserver les lots par journee et garantir qu'un coffret n'est attribue qu'une fois ;
- appliquer la regle de gain maximum et selectionner un suppleant si necessaire ;
- superviser le calendrier, les retards de traitement et les notifications.

### Localeo Animation

- proposer le modele Calendrier dans le catalogue ;
- configurer les informations globales puis les 12 ou 24 cases ;
- associer date, contenu, commercant et lot a chaque case ;
- controler la completude avant publication ;
- visualiser les journees futures, ouvertes, cloturees, tirees et distribuees ;
- relancer manuellement une cloture, un tirage ou un envoi en echec ;
- consulter un bilan global et par journee.

### Marketplace

- promouvoir le calendrier sur les surfaces de la commune ;
- afficher son principe, sa periode, les commercants et les lots publiables ;
- mettre en avant la case du jour sans reveler les contenus futurs ;
- rediriger vers Localeo Live pour participer et suivre le calendrier.

### Localeo Live

- afficher une grille de 12 ou 24 cases avec leurs etats ;
- ouvrir uniquement la case du jour selon l'heure Europe/Paris ;
- presenter le commercant, le contenu et le lot du jour ;
- afficher le QR participant et confirmer sa validation quotidienne ;
- notifier l'ouverture selon les preferences, puis le resultat et le gain ;
- conserver l'historique des cases participees et gagnees.

### Application commercant

- afficher la ou les journees concernant le commercant ;
- scanner le QR et creer une validation rattachee a la bonne journee ;
- refuser les scans hors plage ou dupliques ;
- afficher le nombre de visites validees pour la journee ;
- rester utilisable si le commercant participe a plusieurs animations simultanees.

## User Stories

### PRD-507 - Declarer le modele Calendrier

En tant que produit Localeo, je veux un modele distinct compose de journees afin d'eviter de creer 24 animations independantes.

### PRD-508 - Configurer les informations globales

En tant que gestionnaire, je veux definir la periode, le reglement et la presentation du calendrier.

### PRD-509 - Configurer les cases

En tant que gestionnaire, je veux associer a chaque jour une plage, un contenu, un commercant et un lot.

### PRD-510 - Controler la completude

En tant que systeme, je veux bloquer la publication si une journee obligatoire est incomplete ou sans lot reserve.

### PRD-511 - Decouvrir le calendrier

En tant que visiteur, je veux trouver le calendrier depuis la Marketplace sans voir le contenu des cases futures.

### PRD-512 - S'inscrire une seule fois

En tant que participant, je veux une inscription valable pour toutes les journees.

### PRD-513 - Ouvrir la case du jour

En tant que participant, je veux consulter dans Localeo Live la case active et le commercant mis en avant.

### PRD-514 - Valider une visite quotidienne

En tant que commercant, je veux scanner le participant pour l'inscrire au tirage de la journee.

### PRD-515 - Cloturer une journee

En tant que systeme, je veux figer automatiquement la population eligible a l'heure configuree.

### PRD-516 - Realiser le tirage quotidien

En tant que systeme, je veux attribuer le lot du jour de maniere idempotente et auditable.

### PRD-517 - Notifier le resultat et envoyer le gain

En tant que gagnant, je veux etre informe puis recevoir mon coffret.

### PRD-518 - Piloter les journees

En tant que partenaire, je veux identifier les cases incompletes, traitements en retard et gains restant a envoyer.

### PRD-519 - Mesurer les performances

En tant que partenaire ou operateur, je veux comparer visites, participants et gains par jour et par commercant.

## Hors perimetre MVP

- contenu video ou jeu interactif dans chaque case ;
- achat obligatoire ou montant minimum ;
- plusieurs tirages ou plusieurs commercants par jour ;
- participation par geolocalisation ou QR statique affiche en boutique ;
- ouverture adaptee au fuseau propre de chaque participant ;
- calendrier couvrant plusieurs communes.

## Definition de termine

- une seule animation porte toutes ses journees sans duplication ;
- chaque case suit un cycle autonome et auditable ;
- les automatismes sont idempotents et peuvent etre repris manuellement ;
- les contenus futurs restent masques ;
- un participant ne peut etre valide qu'une fois par jour ni gagner au-dela de la limite ;
- les cinq surfaces disposent des fonctions correspondant a leur responsabilite.
