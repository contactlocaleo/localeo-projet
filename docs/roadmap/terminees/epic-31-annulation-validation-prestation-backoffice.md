# Backlog Epic 31 - Annulation d'une validation de prestation backoffice

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre au back-office d'annuler une validation de prestation faite par erreur, sans casser la chaine achat, coffret, reversement, audit et notification.
- Epic source : `Epic 31. Annulation d'une validation de prestation backoffice`
- Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)
- Contexte : le besoin reprend et precise les anciennes intentions `PRD-022` et `PRD-025`, mais il merite une epic dediee car l'impact finance et audit est transverse.

## Probleme

Une validation de prestation peut etre faite par erreur par un commercant :
- mauvaise prestation selectionnee ;
- mauvais coffret client scanne ;
- double manipulation terrain ;
- erreur humaine lors d'un mode secours ;
- validation realisee avant que le client ne beneficie reellement de la prestation.

Aujourd'hui, une validation declenche plusieurs effets :
- la prestation passe en `VALIDEE` ;
- une `ValidationPrestation` est creee ;
- un `MouvementReversement` est cree en `A_REVERSER` ;
- une activite locale peut etre publiee ;
- un email client est prepare ;
- un audit est emis.

Sans action d'annulation controlee, la correction devient manuelle, risquee et potentiellement incoherente avec les reversements.

## Objectif operationnel

Permettre a un operateur habilite de corriger une validation erronnee tant que le reversement n'est pas engage de facon irreversible.

L'operateur doit pouvoir :
- identifier la validation ;
- comprendre son impact finance ;
- annuler la validation si elle est encore annulable ;
- tracer le motif ;
- restaurer l'etat exploitable du coffret ;
- neutraliser le mouvement de reversement associe ;
- conserver une piste d'audit claire.

Le commercant peut annuler directement une validation depuis son application uniquement dans une fenetre courte configurable. Au-dela de cette fenetre, il peut signaler une erreur de validation au back-office, qui decide et execute l'annulation apres controle.

## Perimetre MVP

### Cas autorise

L'annulation est autorisee uniquement si :
- la prestation est en statut `VALIDEE` ;
- une `ValidationPrestation` existe ;
- le mouvement de reversement associe existe ;
- le mouvement de reversement est encore en statut `A_REVERSER` ;
- aucun reversement, lot ou paiement n'a deja rendu ce mouvement irreversible.

### Effets metier attendus

Lorsqu'une validation est annulee :
- le statut prestation repasse a `A_VALIDER` ;
- `date_validation` est videe ;
- le mouvement de reversement associe passe a `ANNULE` ;
- la `coffret instance` est recalculee :
  - `ACTIVE` si au moins une prestation reste ou redevient `A_VALIDER` ;
  - `UTILISE` seulement si toutes les prestations restantes sont consommees ou fermees ;
- l'action est auditee ;
- l'activite locale issue de la validation est masquee ou neutralisee si elle existe ;
- les feedbacks deja presents restent conserves ;
- les emails rattaches a la validation sont traites selon leur statut.
- le client est notifie de l'annulation ;
- le commercant fautif n'est pas notifie automatiquement, mais l'action reste tracee cote back-office.

### Surface back-office

Le MVP doit exposer une action depuis au moins une surface :
- fiche `ValidationPrestation` ;
- fiche `StatutPrestationCoffretInstance` ;
- vision 360 commercant ;
- vision 360 coffret.

Decision MVP : l'action doit etre disponible depuis les trois surfaces suivantes :
- fiche `ValidationPrestation` ;
- fiche `StatutPrestationCoffretInstance` ;
- vision 360.

L'action doit demander :
- motif texte libre obligatoire ;
- commentaire interne optionnel ;
- confirmation explicite.

### Surface application commercant

Le MVP expose une action destructive limitee cote application commercant :
- endpoint API `POST /protected/validation/validations/{validation_prestation_id}/annuler` ;
- motif texte libre obligatoire ;
- commentaire optionnel ;
- verification que la validation appartient au commercant connecte ;
- application des memes regles finance et statut que l'annulation back-office ;
- annulation autorisee uniquement si la validation date de moins de `LOCALEO_VALIDATION_PRESTATION_API_ANNULATION_MAX_HOURS` heures ;
- valeur par defaut de la fenetre : `24` heures ;
- audit avec acteur `commercant:{commercant_id}` ;
- notification client identique a l'annulation back-office.

Le MVP conserve aussi une action non destructive cote application commercant :
- bouton ou action `Signaler une erreur de validation` ;
- motif texte libre obligatoire ;
- commentaire optionnel ;
- rattachement a la validation ou au statut prestation concerne ;
- creation d'un message support via `messages_contact` ;
- rattachement technique du message support via `validation_prestation_id` ;
- signalement autorise uniquement sur une validation recente de moins de 24h ;
- notification automatique de l'equipe support ;
- creation d'une alerte prioritaire dans le dashboard operationnel ;
- aucun changement direct du statut prestation ;
- aucun changement direct du mouvement de reversement ;
- audit ou trace de la demande.

Le signalement ne remplace pas l'annulation back-office. Il sert a porter la demande au support lorsque l'annulation directe n'est plus possible ou doit etre controlee.

## Hors perimetre MVP

- Annulation directe par le commercant hors fenetre configurable.
- Annulation d'une validation deja rattachee a un mouvement `EN_COURS_DE_REVERSEMENT`.
- Annulation d'une validation deja reversee ou payee.
- Compensation comptable automatique.
- Generation automatique d'un avoir.
- Remboursement client automatique.
- Notification automatique du commercant fautif.
- Regularisation post-paiement.

## Regles de gestion

- Une validation annulee ne doit pas etre supprimee physiquement.
- Le systeme doit conserver la `ValidationPrestation` pour audit et historique.
- L'annulation doit etre refusee si le mouvement de reversement n'est pas `A_REVERSER`.
- L'annulation doit etre refusee si le mouvement est deja rattache a un reversement non annulable.
- Le mouvement de reversement doit etre neutralise par statut `ANNULE`, pas supprime.
- La prestation redevient consommable uniquement si le coffret instance reste valide et non expire.
- `date_validation` est videe lorsque la prestation repasse a `A_VALIDER`.
- La `ValidationPrestation` existante reste conservee, sans colonne d'annulation dediee ; la trace d'annulation repose sur l'audit.
- Une nouvelle validation par le meme commercant est autorisee apres annulation si la prestation est de nouveau validable.
- L'action doit etre reservee aux admins back-office authentifies.
- Aucun role fin back-office n'est ajoute en MVP pour cette action.
- Le commercant peut signaler une erreur, mais ne peut pas annuler directement une validation.
- Une demande commercant ne modifie aucun statut metier tant qu'elle n'est pas traitee par le back-office.
- Le signalement commercant est limite aux validations recentes de moins de 24h.
- La fenetre de 24h est stricte apres `date_validation`, week-ends et jours feries inclus.
- Un signalement commercant notifie automatiquement l'equipe support.
- Un signalement commercant cree une alerte prioritaire dans le dashboard operationnel.
- Le motif d'annulation est obligatoire.
- Le motif d'annulation est un texte libre obligatoire.
- Le client doit etre notifie par email uniquement lorsqu'une validation est annulee.
- L'email client utilise le type `PRESTATION_VALIDATION_ANNULEE_CLIENT`.
- L'email client explique que la prestation redevient disponible, sans accuser le commercant.
- Le commercant fautif n'est pas notifie automatiquement lors de l'annulation back-office.
- Le commercant est notifie lorsqu'une demande de signalement est refusee par le back-office.
- L'email de refus commercant utilise le type `SIGNALEMENT_VALIDATION_REFUSE_COMMERCANT`.
- Le signalement commercant reutilise le modele `messages_contact`, sans table dediee en MVP.
- `messages_contact` doit porter un champ `validation_prestation_id` pour rattacher le signalement a la validation concernee.
- L'activite locale deja publiee issue de la validation annulee est masquee totalement.
- Le masquage de l'activite locale utilise le statut ou la visibilite existante, sans champ dedie MVP.
- Les feedbacks deja presents restent conserves, sans traitement specifique en MVP.
- L'audit doit contenir avant/apres : statut prestation, statut mouvement, statut coffret instance.
- Les donnees client ne doivent pas etre exposees au-dela des surfaces back-office existantes.

## User Stories

### Story `PRD-215` - Identifier les validations annulables

Priorite : `P0`
Statut : `Termine`

Valeur metier : eviter les corrections manuelles en montrant clairement quelles validations peuvent encore etre annulees.

Criteres d'acceptation :
- le back-office indique si une validation est annulable ;
- le motif de non-annulabilite est affiche ;
- les statuts finance bloquants sont visibles ;
- le lien vers le mouvement de reversement associe est disponible.

### Story `PRD-216` - Annuler une validation avant reversement

Priorite : `P0`
Statut : `Termine`

Valeur metier : corriger une erreur de validation sans generer de reversement indu.

Criteres d'acceptation :
- un operateur habilite peut annuler une validation `VALIDEE` dont le mouvement est `A_REVERSER` ;
- la prestation repasse a `A_VALIDER` ;
- `date_validation` est videe ;
- le mouvement passe a `ANNULE` ;
- la `coffret instance` est recalculee ;
- la prestation peut etre revalidee ensuite, y compris par le meme commercant si les controles metier sont satisfaits ;
- l'action est refusee si les conditions ne sont pas remplies.

### Story `PRD-217` - Auditer l'annulation de validation

Priorite : `P0`
Statut : `Termine`

Valeur metier : conserver une trace exploitable d'une correction sensible.

Criteres d'acceptation :
- l'action `purchase.prestation.validation.cancelled` est emise ;
- l'audit contient l'acteur, le motif, la validation, la prestation, le coffret instance et le mouvement ;
- l'audit contient les statuts avant/apres ;
- les echecs d'annulation sont egalement audites.

### Story `PRD-218` - Neutraliser les effets connexes

Priorite : `P1`
Statut : `Termine`

Valeur metier : eviter qu'une validation annulee continue d'apparaitre comme une prestation realisee.

Criteres d'acceptation :
- l'activite locale issue de la validation est masquee, annulee ou marquee non publiee ;
- les feedbacks deja presents restent conserves ;
- les emails sortants non envoyes lies a la validation peuvent etre annules ;
- un email client d'annulation est cree ;
- l'email client indique que la prestation redevient disponible, sans attribuer la faute au commercant ;
- le wording final des emails est defini a l'implementation, dans le respect des decisions produit ;
- les effets deja envoyes restent traces mais non supprimes.

### Story `PRD-219` - Afficher l'historique d'annulation

Priorite : `P1`
Statut : `Termine`

Valeur metier : permettre au support de comprendre pourquoi une prestation est redevenue disponible.

Criteres d'acceptation :
- la timeline support affiche l'annulation ;
- la vision 360 commercant affiche les validations annulees ;
- la vision 360 coffret affiche les validations annulees ;
- le motif interne est visible uniquement back-office.

### Story `PRD-220` - Bloquer les annulations finance dangereuses

Priorite : `P0`
Statut : `Termine`

Valeur metier : eviter de casser un reversement deja prepare, exporte ou paye.

Criteres d'acceptation :
- l'annulation est refusee si le mouvement est `EN_COURS_DE_REVERSEMENT` ;
- l'annulation est refusee si le mouvement est `REVERSE` ;
- l'annulation est refusee si un paiement de reversement associe est `EN_COURS_MANUEL` ou `EXECUTE` ;
- le message d'erreur oriente vers une regularisation manuelle.

### Story `PRD-221` - Prevoir une regularisation manuelle hors MVP

Priorite : `P2`
Statut : `Termine`

Valeur metier : traiter les erreurs detectees apres paiement sans modifier brutalement l'historique financier.

Criteres d'acceptation :
- les cas post-paiement sont identifies comme non annulables ;
- le back-office indique qu'une regularisation manuelle est necessaire ;
- une future epic ou story de compensation financiere peut reprendre ce cas.

### Story `PRD-222` - Signaler une erreur de validation depuis l'application commercant

Priorite : `P1`
Statut : `Termine`

Valeur metier : permettre au commercant de remonter rapidement une erreur sans lui donner le pouvoir de modifier directement la chaine financiere.

Criteres d'acceptation :
- le commercant peut signaler une erreur sur une validation recente ;
- une validation recente signifie moins de 24h apres validation ;
- le signalement exige un motif ;
- le signalement cree un message support `messages_contact` rattache a la validation ;
- le rattachement technique utilise `validation_prestation_id` ;
- le signalement notifie automatiquement l'equipe support ;
- le signalement cree une alerte prioritaire dans le dashboard operationnel ;
- le signalement ne change pas le statut de la prestation ;
- le signalement ne change pas le statut du mouvement de reversement ;
- le back-office peut ensuite annuler ou refuser la demande ;
- en cas de refus, le commercant est notifie.

## Decisions actees

- `date_validation` est videe lors du retour a `A_VALIDER`.
- Aucune colonne d'annulation dediee n'est ajoutee sur `validations_prestation` en MVP ; l'annulation s'appuie sur l'audit.
- Le motif d'annulation est un texte libre obligatoire.
- Le client est notifie par email uniquement lorsqu'une validation est annulee.
- L'email client utilise le type `PRESTATION_VALIDATION_ANNULEE_CLIENT`.
- L'email client explique que la prestation redevient disponible, sans accuser le commercant.
- Le commercant fautif n'est pas notifie automatiquement ; l'action est seulement tracee cote back-office.
- Le commercant est notifie lorsqu'une demande de signalement est refusee par le back-office.
- L'email de refus commercant utilise le type `SIGNALEMENT_VALIDATION_REFUSE_COMMERCANT`.
- Une nouvelle validation par le meme commercant est autorisee apres annulation.
- Le droit MVP d'annulation est `admin back-office authentifie`.
- Aucun role fin back-office n'est ajoute en MVP pour cette action.
- Le signalement commercant est limite aux validations recentes de moins de 24h.
- La fenetre de 24h est stricte apres `date_validation`, week-ends et jours feries inclus.
- L'equipe support est notifiee automatiquement lorsqu'un commercant signale une erreur.
- Le signalement commercant cree une alerte prioritaire dans le dashboard operationnel.
- Le signalement commercant reutilise `messages_contact`, sans creer de table dediee en MVP.
- `messages_contact` porte un champ `validation_prestation_id` pour rattacher le signalement a la validation concernee.
- L'activite locale deja publiee issue de la validation annulee est masquee totalement.
- Le masquage de l'activite locale utilise le statut ou la visibilite existante, sans champ dedie MVP.
- Les feedbacks deja presents restent conserves, sans traitement specifique en MVP.
- Le wording final des emails est laisse a l'implementation, sous reserve de rester neutre et non accusatoire.
- La regularisation post-paiement reste hors MVP et sera cadree plus tard.

## Proposition de tickets implementables

- `EP31-T01` Ajouter le service applicatif d'annulation de validation.
- `EP31-T02` Ajouter les controles finance sur mouvement, reversement, lot et paiement.
- `EP31-T03` Recalculer le statut de `CoffretInstance` apres annulation.
- `EP31-T04` Ajouter l'audit `purchase.prestation.validation.cancelled`.
- `EP31-T05` Ajouter l'action back-office avec motif obligatoire.
- `EP31-T06` Neutraliser activite locale et emails non envoyes.
- `EP31-T07` Afficher l'historique dans timeline support et visions 360.
- `EP31-T08` Ajouter le signalement non destructif cote application commercant via `messages_contact`.
- `EP31-T09` Ajouter `validation_prestation_id` a `messages_contact`.
- `EP31-T10` Ajouter l'alerte dashboard support pour les signalements commercants.
- `EP31-T11` Ajouter les notifications client et refus commercant.
- `EP31-T12` Ajouter les tests domaine/application/back-office.
