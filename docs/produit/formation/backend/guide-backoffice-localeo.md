# Guide de formation au back-office Localeo

## Objet

Ce document sert de guide de formation pour une personne qui doit prendre en charge le back-office Localeo.

Il documente :
- la structure du menu ;
- le role de chaque ecran ;
- les actions disponibles ;
- les points d'attention operatoires ;
- les parcours metier les plus frequents.

Le document est base sur le back-office SQLAdmin expose par `app/infrastructure/admin/admin.py`.

## Perimetre

Le back-office Localeo sert a piloter :
- le referencement des villes, commercants, coffrets et prestations ;
- les achats, paiements et coffrets instances ;
- les reversements commercants ;
- l'exploitation terrain et support ;
- les traces d'envoi email/SMS et l'audit.

## Conventions generales

### Navigation

Le menu est organise par categories :
- `Gestion referencement`
- `Gestion commercialisation`
- `Gestion Achats / Paiements`
- `Gestion reversement`
- `Exploitation`
- `Support`

### Comportement standard des vues

Selon les ecrans, l'operateur dispose ou non des actions standard SQLAdmin :
- `Creer`
- `Modifier`
- `Supprimer`
- consultation detail
- recherche
- actions de masse

Quand une vue est en lecture seule, cela signifie en pratique :
- pas de creation manuelle ;
- pas de suppression manuelle ;
- pas de correction directe hors cas explicitement prevu.

### Principe operatoire

Regle generale :
- utiliser d'abord les actions metier dediees ;
- eviter les modifications directes de statut si une action metier existe deja ;
- verifier l'audit et les traces d'envoi apres une action sensible.

## Parcours metier a connaitre en priorite

Les parcours a maitriser en premier sont :
1. gerer le referencement d'un commercant ;
2. verifier un achat et son paiement ;
3. diagnostiquer une `Coffret instance` ;
4. traiter un mode secours ;
5. generer un reversement ;
6. preparer et cloturer un paiement de reversement ;
7. traiter un message de contact ;
8. consulter l'audit.

## 1. Gestion referencement

### 1.1 `Ville`

Role :
- gerer le referentiel des villes rattachees aux commercants et coffrets.

Donnees principales :
- nom ;
- code postal ;
- image URI.

Actions disponibles :
- creer une ville ;
- modifier une ville ;
- rechercher par nom, code postal ou image.

Point d'attention :
- ce referentiel alimente les ecrans commercants et coffrets. Une erreur ici se propage aux fiches metier.

### 1.2 `Type commercant`

Role :
- gerer le referentiel des types de commercants.

Donnees principales :
- libelle.

Actions disponibles :
- creer ;
- modifier ;
- rechercher.

Usage :
- a utiliser avant creation ou mise a jour d'un commercant si le type n'existe pas encore.

### 1.3 `Type coffret`

Role :
- definir les types de coffrets commercialises.

Donnees principales :
- code ;
- libelle ;
- marge minimum pourcent.

Actions disponibles :
- creer ;
- modifier ;
- rechercher.

Regle importante :
- le code est normalise automatiquement.

Point d'attention :
- ce referentiel influence la logique de marge et de rentabilite.

### 1.4 `Commercant`

Role :
- fiche principale de gestion d'un commercant.

Donnees principales :
- nom ;
- ville ;
- type ;
- description ;
- statut ;
- contacts ;
- image.

Actions standard :
- creer ;
- modifier ;
- consulter le detail ;
- rechercher.

Actions metier disponibles :
- `Envoyer lien initialisation acces`
- `Reinitialiser acces`
- `Verrouiller acces`
- `Deverrouiller acces`

Usage des actions :
- `Envoyer lien initialisation acces` : premier demarrage du compte commercant ;
- `Reinitialiser acces` : renvoi d'un lien de reset mot de passe ;
- `Verrouiller acces` : blocage manuel d'un acces ;
- `Deverrouiller acces` : reouverture du compte apres blocage ou serie d'echecs.

Regles metier controlees par l'ecran :
- un commercant `BROUILLON` ou `REFERENCE` ne peut pas avoir de coffret actif ;
- un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas garder des prestations incompatibles ;
- un commercant en cours d'exploitation ne peut pas etre suspendu si des coffrets actifs ont des instances en cours.

Quand utiliser cet ecran :
- creation d'un nouveau commercant ;
- mise a jour des informations de contact ;
- changement de statut ;
- gestion d'acces support.

### 1.5 `Acces commercant`

Role :
- vue de consultation des identifiants d'acces commercant.

Donnees principales :
- login ;
- date de configuration du mot de passe ;
- nombre d'echecs ;
- date de verrouillage ;
- derniere connexion.

Actions disponibles :
- aucune action directe ;
- lecture seule.

Usage :
- diagnostic d'acces ;
- verification qu'un mot de passe a bien ete initialise ;
- verification des blocages de compte.

### 1.6 `Motif contact`

Role :
- gerer les motifs proposes dans les formulaires de contact.

Donnees principales :
- code ;
- libelle ;
- cible ;
- actif ;
- ordre.

Actions disponibles :
- creer ;
- modifier ;
- activer ou desactiver via edition.

Usage :
- pilotage fonctionnel des formulaires support et commercant.

Point d'attention :
- l'ordre pilote l'affichage ;
- la desactivation masque le motif sans supprimer l'historique des messages existants.

### 1.7 `Image`

Role :
- bibliotheque des images utilisees par le referencement.

Donnees principales :
- apercu ;
- nom ;
- slug ;
- URI ;
- type MIME ;
- taille ;
- statut.

Actions disponibles :
- creer une image ;
- modifier les metadonnees ;
- consulter l'apercu.

Regles importantes :
- le fichier est obligatoire a la creation ;
- seuls certains types sont acceptes ;
- la taille maximale est controlee.

Quand utiliser cet ecran :
- preparer ou corriger un asset image ;
- verifier qu'une image est bien stockee et exploitable.

## 2. Gestion commercialisation

### 2.1 `Coffret`

Role :
- gerer les offres coffrets vendues sur Localeo.

Donnees principales :
- nom ;
- type de coffret ;
- statut ;
- ville ;
- image ;
- prix ;
- duree de validite ;
- prestations rattachees.

Actions standard :
- creer ;
- modifier ;
- consulter le detail ;
- rechercher.

Action metier disponible :
- `Consulter rentabilite`

Usage de l'action :
- ouvre la page interne de synthese rentabilite du coffret.

Regles metier :
- un coffret `ACTIVE` ne peut contenir que des commercants actifs ;
- le type de coffret doit exister dans le referentiel.

Quand utiliser cet ecran :
- creation d'une offre ;
- activation d'un coffret ;
- verification de sa composition ;
- consultation de sa rentabilite.

### 2.2 `Prestation coffret`

Role :
- gerer les prestations qui composent les coffrets.

Donnees principales :
- libelle ;
- montant de reversement ;
- statut ;
- description ;
- image ;
- coffret ;
- commercant.

Actions standard :
- creer ;
- modifier ;
- consulter ;
- rechercher.

Regles metier :
- une prestation `ACTIVE` doit appartenir a un coffret `ACTIVE` ;
- une prestation `ACTIVE` doit etre rattachee a un commercant `ACTIF` ;
- le montant de reversement est controle pour garantir la coherence economique du coffret ;
- une prestation incompatible avec le statut du commercant est refusee.

Quand utiliser cet ecran :
- ajout d'une prestation a une offre ;
- correction du montant de reversement ;
- changement de statut d'une prestation.

## 3. Gestion Achats / Paiements

### 3.1 `Achat coffret`

Role :
- suivre les achats clients et leur etat de paiement.

Donnees principales :
- coffret ;
- email client ;
- telephone ;
- nom entreprise ;
- nom contact ;
- montant ;
- statut ;
- type client ;
- quantite ;
- date de creation ;
- date de paiement ;
- etat d'activation des instances generees.

Actions disponibles :
- consultation ;
- recherche ;
- `Relancer reconciliation paiement`

Usage de l'action :
- a utiliser pour relancer la reconciliation Stripe d'achats non confirmes ;
- utile en cas de webhook manquant ou de decalage entre Stripe et Localeo.

Quand utiliser cet ecran :
- verifier qu'un achat a bien ete paye ;
- identifier les achats en anomalie ;
- confirmer la creation des `Coffret instances`.

Point d'attention :
- ne pas utiliser la relance de reconciliation sans motif. C'est une action de reprise, pas une action quotidienne systematique.

### 3.2 `Coffret instance`

Role :
- suivre chaque instance creee a partir d'un achat.

Donnees principales :
- verification code ;
- achat ;
- coffret ;
- email beneficiaire ;
- statut ;
- dates creation / activation / expiration ;
- etat du token d'activation ;
- etat du QR ;
- etat du lien de consultation.

Actions metier disponibles dans le detail :
- `Renvoyer le mail de confirmation`
- `Renvoyer le mail d'activation` si l'instance est en attente d'activation
- `Regenerer QR code`
- `Regenerer lien de consultation`
- `Revoquer lien de consultation`
- `Mode secours`

Usage des actions :
- renvoi email : support client ou reprise d'envoi ;
- regeneration QR : si le QR est perdu ou doit etre remplace ;
- regeneration consultation : si le lien n'est plus accessible ;
- revocation consultation : si le lien doit etre invalide ;
- mode secours : traitement telephonique d'une validation en incident.

Quand utiliser cet ecran :
- support beneficiaire ;
- diagnostic d'un QR ;
- verification de validite ;
- preparation d'un traitement mode secours.

Point d'attention :
- c'est l'ecran pivot pour l'exploitation terrain d'un coffret deja vendu.

### 3.3 `Paiement`

Role :
- suivi technique des paiements d'achat.

Donnees principales :
- achat ;
- provider ;
- status ;
- transaction id ;
- date de creation.

Actions disponibles :
- consultation ;
- recherche.

Usage :
- diagnostic de paiement ;
- recoupement avec Stripe et avec `Achat coffret`.

### 3.4 `Statut prestation coffret instance`

Role :
- suivre, prestation par prestation, l'etat de consommation d'une `Coffret instance`.

Donnees principales :
- coffret instance ;
- prestation ;
- commercant ;
- statut.

Actions disponibles :
- consultation ;
- recherche ;
- modification du statut si necessaire via edition admin.

Usage :
- verifier quelles prestations restent a valider ;
- diagnostiquer une incoherence de consommation ;
- identifier la bonne prestation cible en mode secours.

Point d'attention :
- une modification manuelle doit rester exceptionnelle et traçable.

## 4. Gestion reversement

Cette categorie couvre tout le cycle financier commercant :
- mouvements dus ;
- generation des mouvements transferables ;
- campagnes bimensuelles Stripe Connect ;
- transfers Stripe ;
- suivi des statuts et echecs Stripe.

Les anciens paiements manuels sont decommissionnes. Le pilotage cible est
documente dans [Piloter les reversements Stripe Connect](../../../exploitation/exploitation/piloter-reversements-stripe-connect.md).

### 4.1 `Compte bancaire commercant` decommissionne

Role :
- objet decommissionne dans la cible EPIC 39.

Decision EPIC 39 :
- Stripe Connect porte l'onboarding financier et le payout commercant ;
- les comptes bancaires geres dans Localeo ne sont plus utilises pour executer
  des virements ou reversements ;
- les donnees historiques de reversement manuel peuvent etre supprimees,
  l'application n'etant pas en production.

Donnees principales :
- commercant ;
- IBAN ;
- titulaire ;
- actif ;
- date de creation.

Actions disponibles dans la cible :
- consultation d'audit si necessaire ;
- aucune action de paiement manuel.

Usage :
- aucun usage operationnel cible.

Point d'attention :
- un commercant sans compte connecte Stripe eligible apparait bloque dans les campagnes de reversement Stripe Connect.

### 4.2 `Compte reversement commercant`

Role :
- vue technique du compte de reversement du commercant.

Donnees principales :
- commercant ;
- date de creation.

Actions disponibles :
- consultation uniquement.

Usage :
- verifier l'existence du compte technique de reversement ;
- diagnostic financier.

### 4.3 `Mouvement reversement`

Role :
- suivre les mouvements unitaires dus au commercant apres validation de prestation.

Donnees principales :
- compte reversement ;
- commercant ;
- validation d'origine ;
- montant ;
- statut ;
- reversement rattache ;
- date de mouvement.

Actions disponibles :
- consultation ;
- acces page `Gerer le reversement` au niveau de la page.

Usage :
- verifier qu'une validation de prestation a bien produit un mouvement ;
- expliquer le montant agrege d'un reversement ;
- diagnostiquer un blocage amont.

### 4.4 `Reversement`

Role :
- suivre les reversements agreges par commercant.

Donnees principales :
- commercant ;
- compte bancaire ;
- montant total ;
- statut ;
- date de creation.

Actions disponibles :
- consultation ;
- detail ;
- depuis le detail :
  - `Gerer le reversement`
  - `Gerer le paiement`

Usage :
- verifier qu'un reversement a ete cree ;
- controler son montant ;
- basculer vers les pages de pilotage.

### 4.5 `Ligne reversement`

Role :
- detail ligne par ligne d'un reversement.

Donnees principales :
- reversement ;
- mouvement ;
- montant.

Actions disponibles :
- consultation uniquement.

Usage :
- justifier la composition d'un reversement ;
- auditer la chaine mouvement -> reversement.

### 4.6 `Paiement reversement`

Role :
- suivre l'execution Stripe d'un reversement.

Donnees principales :
- reversement ;
- montant ;
- statut ;
- date execution ;
- references Stripe ;
- motif echec.

Actions disponibles :
- consultation ;
- detail.

Usage :
- suivre les transfers Stripe ;
- comprendre un echec Stripe ;
- rattacher le paiement a une campagne bimensuelle.

### 4.7 `Lot paiement reversement` decommissionne

Role :
- objet decommissionne par EPIC 39.

Donnees principales :
- statut ;
- mode execution ;
- format export ;
- created_by ;
- date creation ;
- date export ;
- fichier export nom ;
- commentaire.

Actions disponibles :
- aucune action cible.

Usage :
- aucun usage operationnel cible ;
- suppression des donnees pre-production ;
- aucun export CSV bancaire ;
- aucun virement manuel.

### 4.8 Page interne `Vision 360 reversements et paiements`

Acces :
- bouton `Vision 360 reversements et paiements` depuis les ecrans de reversement ;
- URL `/internal/reversements/vue-360`

Role :
- page unifiee de pilotage des campagnes Stripe Connect et des paiements de reversement.

Fonctions disponibles :
- voir la liste des commercants eligibles ;
- voir les commercants bloques et la raison ;
- controler les mouvements transferables ;
- lancer la campagne Stripe Connect ;
- suivre les transfers Stripe ;
- acceder aux projections `Reversement` et `PaiementReversement` ;
- exporter le recapitulatif CSV de la periode filtree.

Quand utiliser cet ecran :
- exploitation financiere reguliere ;
- reprise apres validations accumulees ;
- diagnostic des blocages de reversement.

### 4.9 Lancement d'une campagne Stripe Connect

Acces :
- bouton `Lancer campagne Stripe` depuis la vue 360 ;
- action `POST /internal/reversements/campagnes-stripe/lancer`.

Role :
- creer les transfers Stripe pour les mouvements transferables ou en reprise d'echec.

Resultat :
- les transfers acceptes passent en attente de confirmation Stripe ;
- les echecs restent visibles dans la vue 360 et peuvent etre repris apres correction ;
- l'idempotence empeche de recreer un transfer deja demande ou confirme.

### 4.10 Documentation reversements

Acces :
- documentation operationnelle associee a la vue 360 des reversements.

Role :
- fournir la procedure operatoire detaillee.

## 5. Exploitation

### 5.1 `Transaction validation`

Role :
- suivre les transactions terrain de validation d'une `Coffret instance`.

Donnees principales :
- coffret instance ;
- date ouverture ;
- date expiration ;
- statut.

Actions disponibles :
- consultation ;
- recherche.

Usage :
- diagnostic d'une validation en cours ou expiree ;
- verification de la fenetre de validation.

### 5.2 `Session commercant`

Role :
- suivre les sessions ouvertes cote commercant.

Donnees principales :
- commercant ;
- etat ;
- scopes ;
- dates creation / expiration / revocation.

Actions disponibles :
- consultation ;
- `Revoquer la session`

Usage :
- support d'authentification ;
- coupure d'acces en cas d'incident.

### 5.3 `Validation commercant`

Role :
- historique des validations metier nominales.

Donnees principales :
- coffret instance ;
- statut prestation ;
- commercant ;
- date validation.

Actions disponibles :
- consultation.

Usage :
- preuve d'utilisation d'une prestation ;
- recoupement avec reversement et support.

### 5.4 `Validation secours`

Role :
- historique des validations traitees en mode secours.

Donnees principales :
- date creation ;
- secours request id ;
- decision ;
- statut execution ;
- coffret instance ;
- commercant ;
- operateur admin ;
- motif incident ;
- commentaire ;
- validation metier ;
- erreur execution.

Actions disponibles :
- consultation.

Usage :
- audit d'un traitement telephonique ;
- verification du motif et de la decision prise ;
- recoupement avec la prestation et le commercant.

### 5.5 `Lien court`

Role :
- suivre les liens courts emis par le systeme.

Donnees principales :
- token ;
- type lien ;
- actif ;
- dates creation / expiration / derniere utilisation ;
- nombre d'utilisations.

Actions disponibles :
- consultation uniquement.

Usage :
- diagnostic d'un lien partage ;
- verification d'expiration.

### 5.6 `Email sortant`

Role :
- pilotage et diagnostic des emails sortants.

Donnees principales :
- type email ;
- destinataire ;
- objet ;
- statut ;
- provider statut ;
- dates d'envoi ;
- source type / source id ;
- erreurs eventuelles.

Actions disponibles :
- consulter ;
- modifier le statut ;
- `Supprimer la selection`
- `Passer a A_ENVOYER`
- `Passer a EN_COURS_ENVOI`
- `Passer a ENVOYE`
- `Passer a DELIVRE`
- `Passer a OUVERT`
- `Passer a ECHEC_TEMPORAIRE`
- `Passer a ECHEC_DEFINITIF`
- `Passer a ANNULE`

Usage :
- supervision des envois ;
- correction operatoire ;
- reprise manuelle de file d'envoi.

Point d'attention :
- ces actions changent directement l'etat de suivi. Elles doivent etre reservees au support ou a l'exploitation.

### 5.7 `Sms sortant`

Role :
- pilotage et diagnostic des SMS sortants.

Donnees principales :
- type SMS ;
- destinataire ;
- statut ;
- provider statut ;
- dates d'envoi ;
- source type / source id ;
- erreur eventuelle.

Actions disponibles :
- consulter ;
- modifier le statut ;
- `Supprimer la selection`
- `Passer a A_ENVOYER`
- `Passer a EN_COURS_ENVOI`
- `Passer a ENVOYE`
- `Passer a DELIVRE`
- `Passer a ECHEC_TEMPORAIRE`
- `Passer a ECHEC_DEFINITIF`
- `Passer a ANNULE`

Usage :
- supervision des SMS transactionnels ;
- reprise ou correction manuelle.

### 5.8 `API key`

Role :
- gerer les cles API internes.

Donnees principales :
- label ;
- prefix ;
- scope ;
- active ;
- dates creation / derniere utilisation.

Actions disponibles :
- creer ;
- modifier ;
- supprimer.

Usage :
- gestion de credentiel applicatif ;
- revue des cles actives.

Point d'attention :
- ne pas modifier sans comprendre l'usage de la cle et son scope.

### 5.9 `Evenement audit`

Role :
- journal d'audit central du back-office et des actions sensibles.

Donnees principales :
- date evenement ;
- action ;
- phase ;
- acteur ;
- commercant id ;
- achat id ;
- coffret instance id ;
- path ;
- request id ;
- metadonnees.

Actions disponibles :
- consultation uniquement.

Usage :
- audit de securite ;
- diagnostic fonctionnel ;
- preuve d'une action admin.

Ecran a consulter systematiquement apres :
- mode secours ;
- relance de paiement ;
- generation de reversement ;
- cloture de paiement reversement ;
- operations sensibles d'acces commercant.

## 6. Support

### 6.1 `Message contact`

Role :
- gerer les messages de contact entrants et les fils de discussion.

Donnees principales :
- thread id ;
- type emetteur ;
- motif ;
- commercant ;
- email et telephone ;
- references metier ;
- statut lecture admin ;
- statut lecture commercant ;
- statut traitement ;
- dates de lecture et reponse ;
- arborescence du thread.

Actions disponibles :
- modifier le message sur les champs de gestion ;
- `Marquer lu admin`
- `Marquer non lu admin`
- `Passer en cours`
- `Cloturer`

Usage :
- traitement support ;
- suivi des demandes clients et commercants ;
- priorisation des dossiers.

Bon usage :
- passer `EN_COURS` quand un operateur prend le sujet ;
- cloturer quand le dossier est termine ;
- conserver un statut de lecture coherent pour le relais entre operateurs.

## 7. Pages internes hors menu

Certaines actions ouvrent des pages internes qui ne sont pas des entrees directes du menu.

### `Consulter rentabilite`

Acces :
- depuis le detail d'un coffret.

Role :
- afficher la synthese de rentabilite d'un coffret.

### `Mode secours`

Acces :
- depuis le detail d'une `Coffret instance`.

Role :
- traiter une validation telephonique assistee support.

Donnees demandees :
- prestation cible ;
- decision ;
- motif incident ;
- resume de verification commercant ;
- commentaire optionnel.

Resultat :
- creation d'une `Validation secours` ;
- eventuelle validation metier associee selon la decision.

## 8. Parcours de formation recommande

### Niveau 1 - prise en main

Objectif :
- savoir se reperer ;
- savoir lire les ecrans ;
- ne pas faire d'action irreversible.

Ecrans a maitriser :
- `Commercant`
- `Coffret`
- `Achat coffret`
- `Coffret instance`
- `Paiement`
- `Message contact`
- `Evenement audit`

### Niveau 2 - support operationnel

Objectif :
- traiter les incidents courants.

Parcours a maitriser :
- relance reconciliation paiement ;
- renvoi d'email de confirmation ;
- regeneration QR ;
- regeneration / revocation du lien de consultation ;
- reinitialisation d'acces commercant ;
- consultation du mode secours ;
- traitement d'un message support.

### Niveau 3 - exploitation avancee

Objectif :
- prendre en charge les operations regulieres.

Parcours a maitriser :
- generation des reversements ;
- pilotage des campagnes Stripe Connect ;
- suivi des transfers Stripe ;
- reprise technique des echecs Stripe ;
- lecture de l'audit de bout en bout.

## 9. Check-list operatoire quotidienne

Chaque jour ouvré, verifier au minimum :
- les achats non confirmes ou en anomalie ;
- les `Coffret instances` en incident support ;
- les messages de contact non lus ;
- les emails ou SMS en echec ;
- les paiements reversement a cloturer ;
- l'audit sur les actions sensibles recentes.

## 10. Check-list avant action sensible

Avant toute action sensible, verifier :
- que la bonne ressource est ouverte ;
- que le statut courant est coherent avec l'action ;
- que la demande support ou le besoin metier est documente ;
- que l'action laisse une trace exploitable dans l'audit.

Actions sensibles typiques :
- deverrouiller un acces commercant ;
- relancer une reconciliation paiement ;
- utiliser le mode secours ;
- generer un reversement ;
- exporter un lot de paiement ;
- cloturer un paiement reversement.

## MARKET-002 - Assistance au retour de paiement

Un retour en attente ou impossible a verifier ne signifie pas un echec. Verifier l'achat dans le backoffice avant toute nouvelle demande de paiement. L'acces de retour expire apres 24 heures et ne permet ni gestion ni activation ; utiliser les liens dedies pour ces operations. Ne jamais demander de copier une capacite dans un ticket.

## Formation aux correctifs Marketplace MARKET-001 a MARKET-010

Les consignes de diagnostic, reprise de paiement et inscription, conditions Pro, continuite participant et livraison sont rassemblees dans le [guide de formation et recette Marketplace](../../../exploitation/guide-corrections-marketplace-2026-09-06.md). Ne pas demander un nouveau paiement lorsqu'un retour est seulement impossible a verifier.
