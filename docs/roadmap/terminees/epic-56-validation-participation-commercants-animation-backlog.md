# Backlog Epic 56 - Validation de la participation des commercants aux animations

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

### Évolution du 26 septembre 2026 — E56-UX-01, préparation commerçant simplifiée

Le statut historique **Terminée** reste inchangé. Cette évolution de présentation
concerne Localeo Commerçant et les missions de chasse de l’EPIC 55. Elle remplace
l’écran de confirmation supplémentaire de l’acceptation et les cases séparées
par préparatif, sans modifier les conditions de participation.

| Critère | Comportement attendu | Preuves ciblées |
| --- | --- | --- |
| E56-UX-01-A | Dates et mission immédiatement lisibles ; règlement, détails et guide accessibles à la demande, sans suppression des consignes | Pages invitation/animation, tests navigateur bureau et mobile |
| E56-UX-01-B | Mission unique présentée sans sélection inutile ; plusieurs propositions restent un choix explicite ; tous les préparatifs visibles, un accord global non précoché puis acceptation directe | `HuntInvitationDetail.test.jsx`, `hunt-missions.spec.js` |
| E56-UX-01-C | Après acceptation, kit et déclaration « Je suis prêt » distincts ; télécharger ou consulter ne déclare jamais prêt ; refus et retrait conservent leur confirmation | Tests kit et participation, `animation-kit.spec.js` |
| E56-UX-01-D | Un clic pendant une commande ne la répète pas ; résultat incertain relu avant renvoi ; changement de mission ou conflit remet le consentement à zéro | Tests commande, invitation et kit |

La [spécification](../../specifications/epic-56-validation-participation-commercants-animation/README.md#e56-ux-01--préparation-commerçant-simplifiée-26-septembre-2026)
porte les impacts et le bilan de cette évolution. La clôture initiale ne vaut
pas preuve de ce nouveau périmètre.

### Bilan initial

- Criticite : `Haute`.
- Statut : `Termine`.
- Objectif : obtenir l'accord explicite de chaque commercant avant de le rendre participant et visible dans une animation, lui fournir les informations et supports necessaires, puis mesurer l'avancement des reponses.
- Dependances : Epics 41, 42, 46, 47, 49 et socles email, notification commercant, WebPush, documentaire et lots.

Voir [le cadrage fonctionnel](../../specifications/epic-56-validation-participation-commercants-animation/README.md), [la conception technique](../../specifications/epic-56-validation-participation-commercants-animation/conception-technique.md) et [le registre des arbitrages](../../specifications/epic-56-validation-participation-commercants-animation/registre-arbitrages.md).

## Contexte existant

Le socle Animation permet deja :

- de selectionner des commercants dans la configuration d'une animation via `commercant_ids` ;
- de notifier l'application commercant lors de la publication ;
- d'emettre une WebPush lorsqu'une souscription existe ;
- de generer, versionner et telecharger un flyer d'animation ;
- de commander des coffrets comme lots d'une animation.

En revanche, un commercant configure est aujourd'hui considere comme inclus sans avoir donne son accord. Il n'existe ni demande de participation, ni decision acceptee ou refusee, ni relance, ni mesure du taux d'acceptation. Le telechargement du flyer est reserve au parcours partenaire et l'eligibilite d'un lot n'est pas reliee aux commercants ayant effectivement accepte.

## Regle directrice

Un commercant selectionne est d'abord un **commercant sollicite**. Il ne devient un **commercant participant** qu'apres acceptation explicite dans l'application commercant.

Les projections publiques, les controles de validation chez le commercant, les missions et l'eligibilite des lots doivent utiliser les participations acceptees, et non plus la seule liste configuree par le partenaire.

## Parcours cible

1. Le partenaire selectionne les commercants qu'il souhaite inviter et finalise les informations utiles de l'animation : presentation, dates, reglement et metadonnee de mission commercant.
2. Localeo cree une demande de participation par commercant et envoie un email ainsi qu'une notification dans l'application commercant, completee par une WebPush si elle est disponible.
3. Le lien ouvre la demande dans l'application commercant apres authentification.
4. Le commercant consulte l'animation, le reglement applicable et sa mission, puis accepte ou refuse.
5. Localeo Animation restitue l'etat de chaque demande et permet une relance sur les memes canaux.
6. Seuls les commercants ayant accepte sont affiches comme participants et peuvent intervenir dans le parcours de l'animation.
7. Chaque coffret choisi comme lot contient au moins une prestation active d'un commercant participant ayant accepte.
8. Une fois l'animation publiee, le commercant accepte peut telecharger et imprimer le flyer de l'animation.

## Arbitrages integres

Les arbitrages fonctionnels du MVP sont valides et deviennent des regles de l'Epic :

- l'envoi est une action manuelle depuis le brouillon, disponible uniquement lorsque la presentation, le reglement, la mission et les dates sont complets ;
- la publication est bloquee tant qu'une demande envoyee reste en attente ;
- une animation exige au moins un commercant accepte, en plus des minima eventuellement imposes par son type ;
- avant publication, toute modification substantielle du reglement, de la mission ou des dates annule les demandes concernees et impose un nouvel envoi ; la prolongation deja autorisee de la date de fin d'une animation en cours conserve les participants et les notifie ;
- le commercant peut retirer son accord de maniere autonome avant publication ; apres publication, le retrait est pilote par le partenaire avec controle des impacts et audit ;
- une demande peut etre relancee manuellement au maximum trois fois, avec un delai minimal de 24 heures entre deux relances ;
- le motif de refus est facultatif, limite en longueur et reserve au partenaire et au backoffice ;
- email et notification applicative sont systematiques ; la WebPush est ajoutee lorsqu'elle est disponible ;
- le lien recu ouvre la demande, mais une session commercant authentifiee est indispensable pour accepter ou refuser ;
- aucun flyer, y compris sous forme d'apercu, n'est accessible au commercant avant la publication de l'animation ;
- chaque coffret-lot contient au moins une prestation active d'au moins un commercant accepte, sans obligation de representer tous les participants ;
- les lots peuvent rester vides pendant la preparation et l'envoi des invitations ; ils deviennent obligatoires pour leur achat et la publication ;
- l'eligibilite du lot est controlee a la selection, a l'achat ou reservation et a la publication ;
- les participants des animations deja publiees sont repris comme acceptes, tandis que les brouillons suivent le nouveau workflow ;
- la Marketplace n'expose que les commercants acceptes ;
- une decision apres la date limite est refusee, sauf si le partenaire prolonge cette date avant publication.

## Responsabilites par surface

### Backoffice / backend Localeo

- ajouter la mission commercant aux metadonnees versionnees de l'animation, au meme niveau que les `regles`, et l'exposer dans les contrats de consultation et de modification ;
- conserver cette metadonnee comme source de verite : une demande de participation ne porte qu'un instantane de la version presentee et ne possede pas sa propre mission editable ;
- introduire une demande de participation distincte de la configuration brute de l'animation ;
- porter son cycle de vie : `A_ENVOYER`, `EN_ATTENTE`, `ACCEPTEE`, `REFUSEE` et `ANNULEE` ;
- enregistrer le commercant, l'animation, la reference ou l'instantane de la version d'animation presentee (incluant reglement et mission), les dates d'envoi et de reponse, les relances et les canaux utilises ;
- garantir qu'une seule demande active existe par couple animation/commercant et rendre envoi, relance et reponse idempotents ;
- emettre l'email et la notification applicative, puis une WebPush lorsque le commercant est abonne ;
- securiser le lien profond vers l'application commercant sans exposer de jeton de decision reutilisable ;
- n'autoriser l'acceptation ou le refus qu'au commercant authentifie concerne ;
- produire la liste des participants effectifs a partir des seules demandes acceptees ;
- appliquer cette liste aux API publiques, aux validations terrain, aux missions et aux controles de publication ;
- verifier a la selection, a l'achat/reservation et a la publication que chaque lot contient au moins une prestation active d'un commercant ayant accepte ;
- exposer un acces securise au flyer courant pour les commercants acceptes ;
- calculer les compteurs et taux d'acceptation par animation ;
- auditer creation, envoi, relance, acceptation, refus, annulation et acces au flyer ;
- fournir au backoffice interne une supervision des demandes en anomalie, des echecs de diffusion et des incoherences entre participants et lots.

Le backend reste la source de verite. Une modification du frontend ou de `commercant_ids` ne peut pas transformer directement un commercant en participant.

### Localeo Animation

- permettre au partenaire de selectionner les commercants a solliciter pendant la preparation de l'animation ;
- permettre de renseigner et consulter la mission via la metadonnee de l'animation exposee par le backend, sans dupliquer cette information dans la demande ;
- imposer une presentation, un reglement disponible et une metadonnee de mission suffisamment precise avant le premier envoi ;
- afficher, pour chaque commercant, le statut de la demande, les dates d'envoi et de reponse, le nombre de relances et les eventuels echecs de canal ;
- distinguer clairement les commercants sollicites des participants ayant accepte ;
- permettre de relancer une demande en attente par email et notification, avec WebPush eventuelle, au plus une fois toutes les 24 heures et dans la limite de trois relances ;
- permettre d'annuler une sollicitation tant qu'elle n'est pas acceptee ;
- afficher les metriques : sollicites, en attente, acceptes, refuses, taux de reponse et taux d'acceptation ;
- empecher la publication lorsqu'une demande envoyee est encore en attente, lorsqu'aucun commercant n'a accepte ou lorsque le minimum propre au type d'animation n'est pas atteint ;
- filtrer la selection des lots pour ne proposer que des coffrets contenant une prestation active d'au moins un commercant accepte ;
- expliquer quel commercant rend chaque lot eligible et signaler toute perte d'eligibilite ;
- rendre visibles l'etat de generation du flyer et les commercants qui peuvent y acceder apres publication.

### Application commercant

- afficher les nouvelles demandes de participation dans un espace distinct des animations deja acceptees ;
- ouvrir la bonne demande depuis l'email, la notification ou la WebPush, apres authentification ;
- presenter avant decision : organisateur, commune, dates, description, reglement et sa version, mission precise, contraintes pratiques et contact du partenaire ;
- permettre d'accepter ou de refuser la demande et de confirmer explicitement la decision ;
- proposer un motif de refus facultatif, restitue au partenaire ;
- refuser une decision recue apres la date limite tant que le partenaire ne l'a pas prolongee ;
- permettre de retirer son acceptation avant la publication ;
- afficher la date et l'etat de la decision ;
- apres acceptation, faire apparaitre l'animation dans l'espace actif du commercant ;
- permettre de consulter, telecharger et imprimer le flyer courant uniquement apres publication ;
- signaler la disponibilite d'une nouvelle version du flyer ou une modification imposant une nouvelle decision.

### Marketplace

La Marketplace ne porte aucune action d'acceptation. Son role est limite a la projection publique :

- ne retourner et ne presenter comme participants que les commercants ayant accepte ;
- ne jamais exposer une demande en attente, un refus, un motif de refus ou une relance ;
- ne publier que des lots conformes a la regle de rattachement aux commercants participants ;
- invalider les projections et caches publics lorsque la liste figee des participants change avant publication.

### Hors surface : Localeo Live

Aucune nouvelle action n'est demandee dans Localeo Live. Les parcours existants doivent toutefois recevoir du backend la liste des participants acceptes et refuser toute validation rattachee a un commercant non participant.

## User Stories

### PRD-533 - Selectionner les commercants a solliciter

En tant que partenaire, je veux selectionner les commercants auxquels proposer une animation sans les rendre immediatement participants.

### PRD-534 - Preparer les metadonnees de participation

En tant que partenaire, je veux completer la presentation, le reglement et la mission portes par l'animation afin que la demande presente les informations de reference au commercant.

### PRD-535 - Envoyer la demande sur les canaux commercant

En tant que systeme, je veux envoyer un email et une notification applicative, ainsi qu'une WebPush lorsqu'elle est disponible, avec un lien vers l'application commercant.

### PRD-536 - Consulter la demande

En tant que commercant, je veux comprendre l'animation, son reglement et ma mission avant de me prononcer.

### PRD-537 - Accepter ou refuser

En tant que commercant, je veux accepter ou refuser explicitement une demande de participation depuis mon application.

### PRD-538 - Restituer les decisions

En tant que partenaire, je veux connaitre l'etat et la date de reponse de chaque commercant.

### PRD-539 - Relancer une demande

En tant que partenaire, je veux relancer un commercant encore en attente sur les memes canaux sans creer une seconde participation.

### PRD-540 - Construire la liste effective des participants

En tant que systeme, je veux considerer comme participants uniquement les commercants ayant accepte.

### PRD-541 - Mettre le flyer a disposition

En tant que commercant participant, je veux telecharger et imprimer le flyer courant de l'animation.

### PRD-542 - Controler l'eligibilite des lots

En tant que partenaire, je veux choisir uniquement des coffrets contenant au moins une prestation active d'un commercant participant.

### PRD-543 - Mesurer l'acceptation

En tant que partenaire, je veux connaitre les volumes, le taux de reponse et le taux d'acceptation des demandes.

### PRD-544 - Superviser et auditer

En tant qu'operateur Localeo, je veux retrouver les demandes, diffusions, decisions, relances et incoherences afin de traiter les incidents.

## Regles metier minimales

- la selection d'un commercant ne vaut jamais acceptation ;
- la mission est une metadonnee versionnee de l'animation, portee par le backend au meme titre que les `regles` ;
- la demande reference la version de mission presentee mais ne constitue jamais sa source de verite ;
- une acceptation est nominative, datee, authentifiee et rattachee a une version des informations presentees ;
- avant publication, une modification substantielle du reglement, de la mission ou des dates annule les demandes concernees et exige une nouvelle decision ;
- la prolongation de la date de fin d'une animation en cours conserve le snapshot des participants, regenere le flyer et les notifie ;
- une relance complete la demande existante, ne cree pas une nouvelle participation, respecte un delai de 24 heures et un maximum de trois relances ;
- un commercant refuse ou en attente n'est visible ni comme participant ni comme point de validation public ;
- une demande envoyee encore en attente bloque la publication ;
- au moins un commercant doit avoir accepte, sous reserve d'un minimum superieur propre au type d'animation ;
- une decision recue apres la date limite est refusee si cette date n'a pas ete prolongee avant publication ;
- le retrait est autonome avant publication puis controle et audite apres publication ;
- chaque lot doit contenir au moins une prestation active appartenant a un commercant ayant accepte ;
- les lots ne sont obligatoires qu'apres recueil des acceptations, pour la commande et la publication ;
- la conformite d'un lot est controlee a la selection, a l'achat ou reservation et a la publication ;
- le flyer commercant est derive du document versionne de l'animation et non d'un fichier depose librement dans la demande ;
- aucun flyer commercant n'est disponible avant la publication ;
- toutes les transitions sensibles sont journalisees.

## Metriques MVP

- nombre de commercants sollicites ;
- nombre et part des demandes en attente ;
- nombre de demandes acceptees et refusees ;
- taux de reponse = `(acceptees + refusees) / demandes envoyees` ;
- taux d'acceptation = `acceptees / (acceptees + refusees)` ;
- nombre total de relances et demandes en echec de diffusion.

Les divisions par zero retournent `0` et les taux sont calcules par le backend sur le meme perimetre que les compteurs.

## Hors perimetre MVP

- acceptation depuis un lien public sans authentification ;
- signature electronique contractuelle ;
- SMS ou messagerie instantanee ;
- negociations et commentaires en fil de discussion ;
- creation ou modification du flyer par le commercant ;
- choix d'un lot par le commercant ;
- affichage public des refus et motifs ;
- comparaison des taux d'acceptation entre partenaires.

## Definition de termine

- un commercant selectionne n'est jamais public ni operationnel avant son acceptation ;
- email et notification applicative sont traces, la WebPush restant conditionnee a une souscription ;
- le commercant prend sa decision dans son application apres consultation des informations requises ;
- Localeo Animation affiche les decisions, permet les relances et restitue les metriques ;
- le flyer devient telechargeable par chaque commercant accepte uniquement apres publication ;
- aucun lot non rattache a une prestation active d'un commercant accepte ne peut etre publie ;
- les controles serveur sont couverts par des tests de droits, d'idempotence, de concurrence et de non-regression ;
- le journal d'audit permet de reconstituer le cycle complet d'une demande.
