# Epic 8. Gestion des contacts et messages support

## Statut

`Termine`

## Objectif

Centraliser les demandes de contact consommateurs et commercants dans un modele de messagerie support exploitable par l'administration Localeo.

Le but est de couvrir :
- les questions marketplace ;
- les questions sur une commande, un coffret, une coffret instance, une prestation ou un paiement ;
- les demandes commercants depuis l'application commercant ;
- les reponses admin, sans envoi direct automatique en V1.

## Problemes a resoudre

- Les demandes support ne sont pas structurees autour des objets metier Localeo.
- Les consommateurs doivent pouvoir contacter Localeo sans compte utilisateur.
- Les commercants doivent pouvoir contacter Localeo depuis une session authentifiee.
- Les reponses et statuts doivent etre consultables et pilotables en back-office.
- Les echanges commercants doivent pouvoir former un fil visible cote application commercant.

## Perimetre V1

- Creation d'un message consommateur depuis la marketplace.
- Creation d'un message commercant depuis l'application commercant.
- Consultation des messages et fils dans SQLAdmin.
- Reponse admin aux consommateurs via preparation d'un email sortant a valider/envoyer.
- Reponse admin aux commercants via le fil applicatif visible dans l'application commercant.
- Consultation et reponse d'un fil par le commercant authentifie.
- Gestion des statuts de lecture et de traitement.
- Audit minimal : source, acteur, IP, user-agent, dates.

## Hors perimetre V1

- Pieces jointes.
- Portail de suivi consommateur.
- Token de suivi consommateur.
- Messagerie temps reel.
- Notifications push.
- Envoi direct synchrone d'une reponse admin.
- Envoi d'email pour les reponses aux messages commercants.
- Politique de retention des messages de contact.

## Modele cible

### `MessageContact`

Champs recommandes :
- `id`
- `thread_id`
- `thread_root_message_id`
- `parent_message_id`
- `type_emetteur` : `ANONYME` | `COMMERCANT` | `LOCALEO`
- `source` : `MARKETPLACE` | `APP_COMMERCANT` | `ADMIN`
- `commercant_id` nullable
- `motif_contact_id`
- `motif_libelle_saisi` nullable, utilise uniquement si le motif selectionne est `AUTRE`
- `message`
- `email_contact`
- `telephone_contact`
- `reference_achat_id`
- `reference_coffret_id`
- `reference_coffret_instance_id`
- `reference_prestation_id`
- `reference_paiement_id`
- `statut_lecture_admin` : `NON_LU` | `LU`
- `statut_lecture_commercant` : `NON_LU` | `LU`
- `statut_traitement` : `OUVERT` | `EN_COURS` | `REPONDU` | `CLOTURE`
- `created_by_type` : `ANONYME` | `COMMERCANT` | `LOCALEO`
- `created_by_id` nullable
- `ip_creation` nullable
- `user_agent` nullable
- `date_creation`
- `date_lecture_admin` nullable
- `date_lecture_commercant` nullable
- `date_derniere_reponse` nullable

Notes :
- `thread_id` identifie le fil de discussion ;
- `thread_root_message_id` identifie explicitement le premier message du fil ;
- pour le premier message d'un fil, `thread_root_message_id = id` et `parent_message_id = null` ;
- pour une reponse, `thread_root_message_id` reste celui du premier message et `parent_message_id` reference le message auquel on repond directement quand cette information est disponible.

### `MotifContact`

Champs recommandes :
- `id`
- `code`
- `libelle`
- `type_cible` : `CONSOMMATEUR` | `COMMERCANT` | `TOUS`
- `actif`
- `ordre_affichage`
- `date_creation`
- `date_modification`

Regles :
- les motifs sont administrables via SQLAdmin ;
- la liste active est utilisee par les formulaires marketplace et application commercant ;
- un motif `AUTRE` doit exister ;
- si le motif selectionne est `AUTRE`, un libelle ou detail complementaire peut etre fourni par l'utilisateur.

## User Stories

### `PRD-030` Creer un message consommateur

- En tant que consommateur, je veux envoyer un message de contact depuis la marketplace afin de poser une question a Localeo.
- Statut : `Termine`

Criteres d'acceptation :
- `email_contact` est obligatoire et valide ;
- `message` est obligatoire et non vide ;
- `motif_contact_id` est obligatoire et doit referencer un motif actif applicable aux consommateurs ;
- la liste des motifs inclut un motif `AUTRE` ;
- `telephone_contact` est optionnel ;
- les references `achat_id`, `coffret_id`, `coffret_instance_id`, `prestation_id`, `paiement_id` sont optionnelles ;
- si une reference optionnelle est fournie et introuvable, le message est refuse ;
- le message est cree en statut lecture `NON_LU` et traitement `OUVERT` ;
- la source est `MARKETPLACE` ;
- les metadonnees d'audit disponibles sont stockees ;
- aucun token de suivi consommateur n'est genere.

### `PRD-031` Creer un message commercant

- En tant que commercant, je veux envoyer un message a Localeo depuis l'application commercant afin de poser une question contextualisee.
- Statut : `Termine`

Criteres d'acceptation :
- l'API exige une session commercant valide ;
- l'API exige le scope `commercant:message` ;
- le message est rattache au `commercant_id` de la session ;
- `message` est obligatoire et non vide ;
- `motif_contact_id` est obligatoire et doit referencer un motif actif applicable aux commercants ;
- la liste des motifs inclut un motif `AUTRE` ;
- une reference de coffret instance ou de prestation peut etre fournie ;
- si une reference optionnelle est fournie et introuvable, le message est refuse ;
- le message cree un nouveau `thread_id` si aucun fil n'est indique.
- le premier message du fil est identifiable via `thread_root_message_id`.

### `PRD-032` Consulter les messages dans SQLAdmin

- En tant qu'admin, je veux consulter les messages de contact dans SQLAdmin afin de les qualifier et suivre leur traitement.
- Statut : `Termine`

Criteres d'acceptation :
- SQLAdmin affiche la liste des messages ;
- la liste permet de filtrer par type emetteur, source, statut lecture, statut traitement et date ;
- la fiche detail affiche le message, ses references metier, les coordonnees et l'audit ;
- la fiche detail affiche les reponses du meme fil.

### `PRD-033` Repondre a un message consommateur depuis SQLAdmin

- En tant qu'admin, je veux repondre a un message consommateur afin de preparer une reponse email.
- Statut : `Termine`

Criteres d'acceptation :
- la reponse Localeo cree un nouveau message dans le meme fil avec `type_emetteur = LOCALEO` ;
- la reponse Localeo passe le fil en `REPONDU` ou met a jour `date_derniere_reponse` ;
- un email sortant est prepare via le flux email existant ;
- l'email n'est pas envoye directement de maniere synchrone ;
- la reponse est visible dans le fil SQLAdmin.

### `PRD-034` Repondre a un message commercant depuis SQLAdmin

- En tant qu'admin, je veux repondre a un message commercant afin de poursuivre l'echange dans l'application commercant.
- Statut : `Termine`

Criteres d'acceptation :
- la reponse Localeo cree un nouveau message dans le meme fil avec `type_emetteur = LOCALEO` ;
- aucun email sortant n'est prepare ;
- la reponse est visible dans le fil SQLAdmin ;
- la reponse est visible dans le fil consultable depuis l'application commercant ;
- le fil passe en `NON_LU` cote commercant via `statut_lecture_commercant`.

### `PRD-035` Notifier le support interne par email

- En tant que systeme, je veux notifier le support interne a chaque nouveau message afin d'alerter l'equipe Localeo sans depender uniquement de SQLAdmin.
- Statut : `Termine`

Criteres d'acceptation :
- l'adresse de destination est configuree par `LOCALEO_SUPPORT_CONTACT_EMAIL` ;
- la notification cree un `EmailSortant` ;
- l'email n'est pas envoye directement de maniere synchrone ;
- la notification contient le type d'emetteur, le motif, un extrait du message et les references metier disponibles.

### `PRD-036` Administrer les motifs de contact

- En tant qu'admin, je veux administrer la liste des motifs de contact afin de piloter les motifs affiches aux consommateurs et commercants.
- Statut : `Termine`

Criteres d'acceptation :
- SQLAdmin permet de creer, modifier, desactiver et ordonner les motifs ;
- chaque motif cible `CONSOMMATEUR`, `COMMERCANT` ou `TOUS` ;
- au moins un motif actif `AUTRE` est disponible ;
- les APIs de creation refusent un motif inexistant, inactif ou non applicable au type d'emetteur.

### `PRD-037` Consulter les fils commercants

- En tant que commercant, je veux consulter mes fils de messages afin de suivre les reponses de Localeo.
- Statut : `Termine`

Criteres d'acceptation :
- l'API exige une session commercant valide ;
- l'API exige le scope `commercant:message` ;
- le commercant ne voit que ses propres fils ;
- les messages du fil sont retournes dans l'ordre chronologique ;
- l'ouverture peut marquer les reponses Localeo comme lues cote commercant via `statut_lecture_commercant`.

### `PRD-038` Repondre dans un fil commercant

- En tant que commercant, je veux repondre dans un fil existant afin de poursuivre l'echange avec Localeo.
- Statut : `Termine`

Criteres d'acceptation :
- l'API exige une session commercant valide ;
- l'API exige le scope `commercant:message` ;
- le fil doit appartenir au commercant authentifie ;
- la reponse cree un nouveau message dans le fil ;
- le fil repasse en `NON_LU` cote admin via `statut_lecture_admin` ;
- `date_derniere_reponse` est mise a jour.

### `PRD-039` Gerer les statuts de lecture et de traitement

- En tant qu'admin, je veux gerer les statuts de lecture et de traitement afin de piloter les demandes support.
- Statut : `Termine`

Criteres d'acceptation :
- un message ou fil peut passer de `NON_LU` a `LU` cote admin ;
- un message ou fil peut passer de `NON_LU` a `LU` cote commercant ;
- un fil peut passer de `OUVERT` a `EN_COURS`, `REPONDU` ou `CLOTURE` ;
- les transitions sont tracees ;
- les statuts sont visibles dans SQLAdmin.

## APIs cibles

### Marketplace

`POST /contacts/consommateur/messages`

Body :
- `email_contact`
- `telephone_contact?`
- `motif_contact_id`
- `motif_libelle_saisi?`
- `message`
- `achat_id?`
- `coffret_id?`
- `coffret_instance_id?`
- `prestation_id?`
- `paiement_id?`

Protection :
- publique en V1 ;
- rate limiting / captcha a envisager cote front ou gateway ;
- pas de token de suivi.

### Application commercant

`POST /commercants/{commercant_id}/messages`

Protection :
- `Authorization: Bearer <session_token>` ;
- scope `commercant:message` ;
- le `commercant_id` de l'URL doit correspondre au commercant de la session.

Body :
- `motif_contact_id`
- `motif_libelle_saisi?`
- `message`
- `coffret_instance_id?`
- `prestation_id?`

`GET /commercants/{commercant_id}/messages`

Protection :
- `Authorization: Bearer <session_token>` ;
- scope `commercant:message` ;
- le `commercant_id` de l'URL doit correspondre au commercant de la session.

`GET /commercants/{commercant_id}/messages/{thread_id}`

Protection :
- `Authorization: Bearer <session_token>` ;
- scope `commercant:message` ;
- le `commercant_id` de l'URL doit correspondre au commercant de la session ;
- le fil doit appartenir au commercant de la session.

`POST /commercants/{commercant_id}/messages/{thread_id}/reponses`

Protection :
- `Authorization: Bearer <session_token>` ;
- scope `commercant:message` ;
- le `commercant_id` de l'URL doit correspondre au commercant de la session ;
- le fil doit appartenir au commercant de la session.

## SQLAdmin

Vue `Messages contact` :
- liste des messages ;
- filtres statut lecture, statut traitement, type emetteur, source, motif, date ;
- filtres de lecture separes cote admin et cote commercant ;
- detail du message ;
- detail des references metier ;
- detail audit ;
- affichage du fil.

Actions recommandees :
- `Marquer comme lu` ;
- `Marquer comme non lu` ;
- `Passer en cours` ;
- `Cloturer` ;
- `Repondre consommateur` : prepare un email sortant ;
- `Repondre commercant` : ajoute une reponse au fil applicatif.
- Vue `Motifs contact` administrable.

## Regles de securite

- Les messages consommateurs ne sont pas consultables publiquement apres depot.
- Les messages commercants sont cloisonnes par `commercant_id`.
- Les endpoints commercants exigent le scope `commercant:message`.
- Les references optionnelles doivent etre validees si elles sont renseignees.
- Une reference optionnelle renseignee mais introuvable bloque la creation du message.
- Les logs ne doivent pas exposer de contenu sensible au-dela d'un extrait controle.
- Les donnees de contact doivent etre visibles uniquement en back-office et dans les traitements support consommateur.
- Les reponses aux commercants ne doivent pas utiliser les coordonnees email/telephone : le canal de reponse est l'application commercant.
- Une protection anti-abus est a prevoir pour le formulaire public marketplace.

## Decisions actees

- Pour un message consommateur, `email_contact` est obligatoire.
- Le motif est obligatoire pour les consommateurs et les commercants.
- Les motifs sont portes par une table administrable `MotifContact`.
- Le motif `AUTRE` doit etre disponible.
- Le consommateur ne dispose pas d'un suivi via lien ou token en V1.
- La reponse consommateur se fait par email ou telephone.
- La reponse commercant se fait via le fil applicatif dans l'application commercant.
- Le scope commercant dedie est `commercant:message`.
- Une reponse admin a un message consommateur prepare un email sortant a valider/envoyer via le flux email existant.
- Une reponse admin a un message commercant ajoute une reponse dans le fil applicatif, sans email.
- Les pieces jointes sont hors perimetre V1.
- Le motif commercant est obligatoire et selectionne dans une liste configurable incluant `AUTRE`.
- Aucun champ `priorite` n'est ajoute en V1.
- Les statuts de lecture sont differencies entre cote admin et cote commercant.
- Le support interne est notifie par email a chaque nouveau message.
- L'adresse de notification support est configuree par `LOCALEO_SUPPORT_CONTACT_EMAIL`.
- La notification support cree un `EmailSortant` et n'est pas envoyee directement.
- La politique de retention est hors perimetre V1 et sera instruite plus tard.

## Decisions a instruire

`Aucune decision bloquante identifiee pour la V1.`

## Ordre d'implementation recommande

1. Ajouter le modele domaine `MotifContact`, les enums associees et la vue SQLAdmin d'administration des motifs.
2. Ajouter le modele domaine `MessageContact` et les enums associees.
3. Ajouter ORM, migration SQL, mapper et repository pour motifs et messages.
4. Ajouter la configuration `LOCALEO_SUPPORT_CONTACT_EMAIL`.
5. Implementer la notification support interne par creation d'un `EmailSortant`.
6. Implementer `CreerMessageContactConsommateur`.
7. Implementer `CreerMessageContactCommercant`.
8. Ajouter la vue SQLAdmin liste/detail des messages.
9. Implementer `RepondreMessageContactConsommateurAdmin` avec preparation d'email sortant.
10. Implementer `RepondreMessageContactCommercantAdmin` avec reponse dans le fil applicatif.
11. Implementer les APIs commercants de consultation et reponse de fil.
12. Ajouter les actions de statut lecture/traitement dans SQLAdmin.
