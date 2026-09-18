# Specifications fonctionnelles - Localeo Backend

> Mise a jour du 7 septembre 2026 : [commission par prestation et saisie en euros](../specifications/epic-60-vision-360-commercialisation/commission-par-prestation.md). Cette decision remplace les anciennes regles de marge cible par coffret/type.

## 1. Objet

Ce document decrit les fonctions metier actuellement portees par `localeo-backend`.

La spécification fonctionnelle et technique propre au portail partenaire est
disponible dans [Localeo Animation](animation/etat-application-backend.md).

Le backend couvre une marketplace locale de coffrets digitaux multi-prestations :

- catalogue public : villes, commercants, profils publics, coffrets, prestations, images ;
- achat : parcours particulier et professionnel, paiement Stripe, activation et consultation ;
- usage terrain : session commercant, QR client, validation de prestation, mode secours ;
- relation client : messages support, timeline support, documents d'achat, remboursements ;
- notifications : outbox email/SMS, relances, synchronisation provider ;
- reversements : mouvements, reversements et paiements de reversement alimentes par Stripe Connect ; les lots de paiement manuel et exports CSV sont decommissionnes par l'EPIC 39 ;
- back-office : referencement, moderation, exploitation, audit, batchs.

Les URLs indiquees sont les URLs applicatives vues par `app/main.py` apres prefixe `/public`, `/protected`, `/admin/api` ou `/internal`.

## 2. Acteurs

- Client particulier : achete un coffret pour lui-meme, recoit un QR et un lien de consultation.
- Client professionnel : achete plusieurs coffrets, gere l'attribution et l'activation des beneficiaires via un token de gestion.
- Beneficiaire : active ou consulte une instance de coffret.
- Commercant : se connecte par login/mot de passe, consulte son espace et valide des prestations.
- Operateur back-office : gere le catalogue, les achats, le support, les notifications, les remboursements et les reversements.
- Systeme : execute les batchs, les relances, les expirations et les synchronisations provider.

## 3. Catalogue public

### UC-01 - Lister et consulter les villes

- APIs : `GET /public/villes`, `GET /public/villes/{ville_id}`
- But : alimenter la navigation marketplace.

Exigences :

- retourner les villes referencees avec nom, code postal et image ;
- permettre une recherche par debut de nom ;
- retourner une erreur de ressource introuvable si l'identifiant n'existe pas.

### UC-02 - Lister les types de commercants et de coffrets

- APIs : `GET /public/types-commercants`, `GET /public/types-coffrets`
- But : fournir les referentiels de filtrage et de configuration catalogue.

Exigences :

- retourner les libelles et identifiants ;
- pour les types de coffrets, exposer le code et la marge minimale de rentabilite ;
- les creations de types sont des fonctions d'administration et ne doivent pas etre exposees publiquement en production.

### UC-03 - Lister et consulter les commercants

- APIs : `GET /protected/commercants`, `GET /protected/commercants/{commercant_id}`
- But : exposer les fiches commercants au front ou aux outils autorises.

Exigences :

- filtrer par ville et type ;
- retourner statut, contacts utiles, description, image et vignette ;
- ne pas exposer les donnees d'authentification.

### UC-04 - Profils publics commercants

- APIs publiques : routes de `public_router` dans `profils_commercants_api.py`, prefixees par `/public/commercants`.
- APIs admin : `/admin/api/profils-commercants/*`
- But : publier des pages commercants enrichies, moderees et versionnees.

Exigences :

- gerer un profil par commercant ;
- creer des versions brouillon ;
- soumettre, approuver, refuser, dupliquer, masquer et republier ;
- calculer un score de completion editorial ;
- verifier liens et photos ;
- exposer publiquement uniquement les contenus approuves et publies ;
- conserver les motifs de refus et commentaires internes pour le back-office.

### UC-05 - Lister et consulter les coffrets

- APIs : `GET /public/coffrets`, `GET /public/coffrets/{coffret_id}`
- But : alimenter les pages de vente.

Exigences :

- filtrer par ville et type ;
- exposer nom, type, ville, image, prix, duree de validite ;
- exposer les prestations actives quand demande ;
- ne proposer a l'achat que les coffrets eligibles au catalogue ;
- considerer comme non vendable un coffret contenant une prestation rattachee a un commercant sans compte connecte Stripe eligible.

### UC-06 - Images et bibliotheque media

- APIs : `POST /public/images`, `GET /public/images/{image_id}`, `GET /public/images/{image_id}/meta`
- But : stocker et servir les medias utilises par les fiches.

Exigences :

- limiter la taille des images ;
- stocker le binaire dans `media_assets` ;
- servir les images actives avec headers de cache ;
- rattacher les objets metier par `image_uri`.

Point de vigilance go-live :

- l'upload public doit etre protege avant production ;
- les SVG ne doivent etre autorises qu'avec une strategie de sanitation explicite.

## 4. Achat et paiement

### UC-07 - Initialiser un paiement

- API : `POST /public/gestion-achats/paiements/initialiser`
- Use cases : `CreerAchatEtInitialiserPaiement`, `InitialiserPaiement`
- But : creer un achat et obtenir une URL Stripe Checkout.

Exigences :

- verifier que le coffret existe et est achetable ;
- supporter `PARTICULIER` et `PROFESSIONNEL` ;
- prendre en compte la quantite ;
- calculer le montant total depuis le prix du coffret ;
- creer un `AchatCoffret` en `PAYMENT_PENDING` ;
- appeler Stripe Checkout ;
- accepter une cle d'idempotence HTTP ;
- retourner `achat_id`, `checkout_url`, type client, quantite et donnees de contact pro.

### UC-08 - Valider un paiement Stripe

- API : `POST /public/stripe/webhook`
- Use case : `ValiderPaiement`
- But : transformer un evenement Stripe signe en achat confirme.

Exigences :

- verifier la signature Stripe ;
- dedupliquer par identifiant d'evenement ;
- traiter `checkout.session.completed` pour confirmer le paiement ;
- traiter `checkout.session.expired` en passant l'achat de `PAYMENT_PENDING` a `PAYMENT_FAILED`, sans regresser un achat deja confirme ;
- ignorer les autres evenements non pertinents ;
- refuser les evenements incomplets ;
- marquer l'achat `PAYMENT_CONFIRMED` ;
- creer le paiement interne ;
- creer les instances de coffret ;
- creer les notifications email/SMS ;
- publier les activites locales associees ;
- generer documents et snapshots utiles a la facturation.

### UC-09 - Achat particulier

Exigences :

- creer immediatement des `CoffretInstance` actives ;
- generer QR client, code de verification et token de consultation ;
- creer les statuts de prestations ;
- envoyer email et SMS de confirmation via outbox ;
- joindre le document d'achat quand disponible.

### UC-10 - Achat professionnel

Exigences :

- creer des `CoffretInstance` en `EN_ATTENTE_ACTIVATION` ;
- generer un `management_token` opaque, stocke uniquement sous forme hashee ;
- envoyer l'email de commande validee ;
- permettre l'attribution des beneficiaires et l'envoi de liens d'activation ;
- limiter l'acces aux informations globales d'achat via le token de gestion.

## 5. Gestion d'achat et activation

### UC-11 - Consulter un achat

- APIs : `GET /protected/achats/{achat_id}`, `GET /protected/achats/{achat_id}/coffrets-instances`
- Auth : `Authorization: Bearer <management_token>` ou `X-Management-Token`

Exigences :

- verifier le token de gestion ;
- exposer le statut d'achat, la quantite, le montant et les instances rattachees ;
- ne pas exposer les secrets bruts stockes.

### UC-12 - Consulter et gerer une instance d'achat

- APIs :
  - `GET /protected/achats/{achat_id}/coffrets-instances/{coffret_instance_id}`
  - `GET /protected/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`
  - `POST /protected/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/envoyer-lien-activation`
  - `POST /protected/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/activer`

Exigences :

- verifier l'appartenance de l'instance a l'achat ;
- accepter selon le cas un management token, un token d'activation ou une session commercant ;
- enregistrer l'email beneficiaire ;
- respecter le cooldown de renvoi du lien d'activation ;
- activer une instance uniquement si elle est en attente ;
- generer QR, date d'activation, date d'expiration, statuts de prestations et token de consultation.

### UC-13 - Consultation par token

- APIs : `GET /protected/coffrets-instances/{coffret_instance_id}`, `/prestations`, `/qrcode`
- Auth : `Authorization: Bearer <consultation_token>`

Exigences :

- verifier hash, expiration et revocation du token ;
- permettre au beneficiaire de consulter l'etat du coffret et ses prestations ;
- pour un achat particulier, exposer les informations d'achat utiles au beneficiaire ;
- pour un achat professionnel, ne pas exposer les informations globales de l'achat.

Point de vigilance go-live :

- les liens front contenant des tokens en query string sont fonctionnels mais sensibles ; ils doivent etre rediges des logs et remplaces a terme par un mecanisme moins exposant.

## 6. Espace commercant et validation terrain

### UC-14 - Authentifier un commercant

- API : `POST /protected/commercants/auth/login`
- Use case : `AuthentifierCommercantParMotDePasse`

Exigences :

- normaliser le login ;
- verifier le hash bcrypt ;
- appliquer un rate limit par login + IP ;
- verrouiller le compte apres echecs repetes ;
- creer une session opaque avec TTL et scopes ;
- retourner le token de session et le resume du commercant.

### UC-15 - Gerer mot de passe et sessions commercant

- APIs :
  - `POST /protected/commercants/auth/mot-de-passe-oublie`
  - `POST /protected/commercants/auth/initialiser-mot-de-passe`
  - `POST /protected/commercants/auth/reinitialiser-mot-de-passe`
  - `POST /protected/commercants/me/mot-de-passe`
  - `GET /protected/commercants/session/valider`
  - `POST /protected/commercants/session/{session_id}/invalider`

Exigences :

- utiliser des tokens opaques d'initialisation/reinitialisation stockes hashes ;
- appliquer TTL et consommation unique ;
- auditer les demandes et changements sensibles ;
- permettre la revocation explicite d'une session.

### UC-16 - Profil et contact commercant

- APIs :
  - `GET /protected/commercants/me`
  - `PATCH /protected/commercants/me/contact`

Exigences :

- retourner uniquement le commercant rattache a la session ;
- permettre la modification encadree de `contact_nom`, `contact_prenom`, `contact_telephone` ;
- refuser la modification des champs sensibles ;
- refuser les modifications pour un commercant suspendu ou archive ;
- auditer consultation et modification.

### UC-17 - Prestations et reversements cote commercant

- APIs :
  - `GET /protected/commercants/{commercant_id}/prestations`
  - `GET /protected/commercants/{commercant_id}/prestations/{prestation_id}`
  - `PATCH /protected/commercants/me/prestations/{prestation_id}`
  - `GET /protected/commercants/{commercant_id}/reversements/mouvements/a-reverser`
  - `GET /protected/commercants/{commercant_id}/reversements/mois/{nb_mois}`

Exigences :

- verifier que `commercant_id` correspond a la session ;
- exposer uniquement les prestations du commercant ;
- limiter la modification de prestation a libelle et description ;
- exposer mouvements a reverser et historique de reversements sans donnees client non necessaires.

### UC-18 - Validation terrain nominale

- APIs :
  - `POST /protected/validation/ouvrir-transaction`
  - `POST /protected/validation/valider-prestation`

Exigences :

- verifier la session commercant et le scope `commercant:validation` ;
- verifier le QR client signe ;
- ouvrir une transaction courte ;
- verifier que la prestation appartient au commercant ;
- empecher les doubles validations ;
- creer `ValidationPrestation` ;
- creer un mouvement de reversement ;
- marquer l'instance `UTILISE` si toutes les prestations sont consommees ;
- produire un email de confirmation.

### UC-19 - Mode secours telephonique

- Exposition : pages internes back-office `Mode secours`
- Use case : `TraiterValidationSecours`

Exigences :

- identifier une instance via le back-office et son code de verification ;
- imposer une prestation cible, une decision, un motif et un resume de verification ;
- accepter `AUTORISE`, `REFUSE`, `A_CONTROLER` ;
- reutiliser la logique nominale quand la decision est `AUTORISE` ;
- conserver une trace `ValidationSecours` et un evenement d'audit.

## 7. Support, facturation et relation client

### UC-20 - Messages de contact

- APIs :
  - `GET /public/contacts/motifs`
  - `POST /public/contacts/consommateur/messages`
  - routes commercants de messagerie sous `/protected/commercants`

Exigences :

- collecter email, telephone optionnel, message et references metier ;
- limiter la longueur du message ;
- verifier les references fournies ;
- creer un fil support ;
- notifier le support via outbox email ;
- permettre la reponse admin ou commercant selon le type de fil.

### UC-21 - Demande de facturation et documents d'achat

Exigences :

- collecter les informations de facturation strictement necessaires ;
- lier la demande a l'achat ;
- generer et historiser les documents d'achat ;
- conserver snapshots et lignes de facturation pour stabiliser le contenu documentaire.

### UC-21B - Gestion documentaire transverse

Le back-office doit permettre de gerer un referentiel documentaire transverse.

Documents publics :

- types initiaux : `CGC`, `CGV`, `CGU`, `MENTIONS_LEGALES`, `POLITIQUE_CONFIDENTIALITE`, `POLITIQUE_RGPD`, `CONDITIONS_UTILISATION`, `CONDITIONS_COMMERCANTS` ;
- scopes initiaux : `SITE_PUBLIC`, `APPLICATION_COMMERCANT`, `BACKOFFICE`, `CLIENT_APRES_ACHAT` ;
- une seule version publiee est autorisee par couple type/scope ;
- publier une nouvelle version archive l'ancienne version publiee ;
- les documents publics du site peuvent etre consultes en HTML quand une version HTML publiee existe ;
- le PDF ou fichier source reste telechargeable en complement via backend.

Documents prives :

- rattachement a une ressource metier : `COMMERCANT`, `CLIENT`, `ACHAT_COFFRET`, `COFFRET_INSTANCE` ;
- consultation et telechargement uniquement via backend ;
- audit des consultations ;
- depuis l'application commercant, un commercant authentifie ne voit que les documents prives rattaches a son propre compte.

Back-office :

- entree dediee `Gestion documentaire` ;
- upload PDF ou HTML ;
- limite d'upload par defaut : 2 Mo, configurable ;
- types MIME MVP : PDF et HTML, configurables ;
- option `Version HTML` lors de l'upload d'un PDF public ;
- generation d'une preview HTML editable avant sauvegarde ;
- sauvegarde de la version HTML comme document derive rattache au PDF source.

Retention :

- contrats commercants expires : conservation minimum 5 ans apres fin de relation commerciale ;
- anciennes versions de documents legaux publics : conservation minimum 10 ans apres depublication ;
- factures et documents comptables : conservation 10 ans a partir de la cloture de l'exercice concerne ;
- aucune purge automatique n'est activee au MVP.

### UC-22 - Timeline support

- Exposition : `Timeline support` dans SQLAdmin et `/internal/support/timeline`
- Use case : `ConsulterTimelineSupport`

Exigences :

- rechercher par achat, instance, paiement, email, SMS ou reference ;
- agreger achats, paiements, validations, emails, SMS, remboursements et audit ;
- fournir une vue chronologique utile au support.

### UC-23 - Remboursements achat

Exigences :

- creer une demande de remboursement depuis le back-office ;
- suivre statut, motif, montant et donnees utiles au support ;
- marquer le remboursement execute, refuse ou en echec ;
- produire l'email de remboursement execute quand applicable ;
- auditer les actions.

## 8. Feedbacks et activites locales

### UC-24 - Feedback post-prestation

- APIs : `GET /public/feedbacks-prestation/{token}`, `POST /public/feedbacks-prestation/{token}`
- Back-office : `Feedback prestation`

Exigences :

- creer un token de feedback apres validation de prestation ;
- permettre une note et un commentaire ;
- demander l'autorisation de publication ;
- soumettre un feedback une seule fois ;
- moderer avant exposition publique ;
- exposer des agregats publics anonymises.

### UC-25 - Feed d'activite locale

- APIs : `GET /public/activites-locales`, `GET /public/activites-locales/agregats`
- Back-office : `Activite locale`

Exigences :

- publier des signaux anonymises apres achat, activation ou validation ;
- supporter visibilite publique/back-office/masquee ;
- purger ou basculer les activites selon la retention configuree ;
- ne pas exposer de donnees personnelles client.

## 9. Notifications et batchs

### UC-26 - Outbox email

- APIs :
  - `POST /protected/emails/batch/envoyer`
  - `POST /protected/emails/batch/synchroniser-statuts`
  - `POST /protected/emails/{email_id}/relancer`

Exigences :

- reserver les emails avant envoi ;
- envoyer via Brevo ou mode dev ;
- gerer succes, echec temporaire, echec definitif, annulation ;
- synchroniser les statuts provider ;
- permettre la relance manuelle.

### UC-27 - Outbox SMS

- APIs :
  - `POST /protected/sms/batch/envoyer`
  - `POST /protected/sms/batch/synchroniser-statuts`
  - `POST /protected/sms/{sms_id}/relancer`

Exigences :

- reserver les SMS avant envoi ;
- attendre l'email associe quand le parcours l'exige ;
- envoyer via Brevo SMS ou mode dev ;
- synchroniser les statuts provider ;
- permettre la relance manuelle.

### UC-28 - Expiration et relances de coffrets

- APIs :
  - `POST /protected/coffrets-instances/expiration/batch`
  - `POST /protected/coffrets-instances/expiration/reminders/batch`
- Back-office : `Batchs exploitation`

Exigences :

- expirer les instances arrivees a echeance ;
- creer un email d'information d'expiration ;
- creer des relances avant expiration dans une fenetre configuree ;
- garantir l'idempotence via `relances_expiration_coffrets`.

### UC-28B - Supervision et ordonnancement des batchs

- APIs :
  - `GET /protected/maintenance/batchs`
  - `GET /protected/maintenance/batchs/executions`
  - `GET /protected/maintenance/batchs/health`
  - `POST /protected/maintenance/sessions-commercant/purger`
  - `POST /protected/maintenance/activites-locales/purger`
- Back-office : lancement manuel des batchs d'exploitation.

Exigences :

- inventorier les batchs operables et leurs frequences cibles ;
- historiser chaque execution dans `executions_batch` ;
- empecher les executions concurrentes via `verrous_batch` ;
- exposer un health operationnel des batchs critiques ;
- tracer les parametres sans secrets et les compteurs fonctionnels.

## 10. Reversements et finance commercant

### UC-29 - Mouvements de reversement

Exigences :

- creer un mouvement a la validation d'une prestation ;
- calculer le montant depuis `montant_reversement` ;
- rattacher le mouvement au commercant, a la prestation et a l'instance ;
- rendre le mouvement transferable sans executer immediatement le transfer ou paiement commercant ;
- suivre les statuts `A_REVERSER`, `EN_REVERSEMENT`, `REVERSE`.

### UC-30 - Generation de reversements

- API : `POST /protected/reversements`
- Back-office : pages internes de generation

Exigences :

- identifier les mouvements eligibles ;
- verifier l'eligibilite du compte connecte Stripe ;
- generer un reversement et ses lignes ;
- supporter la generation en lot par commercant ;
- conserver un pilotage Localeo bimensuel des reversements via Stripe Connect ;
- auditer la preparation.

### UC-31 - Paiement des reversements

- Back-office :
  - pilotage des campagnes bimensuelles Stripe Connect
  - suivi des transfers Stripe
  - reprise technique des echecs Stripe

Exigences :

- lister les reversements eligibles au paiement ;
- preparer une campagne bimensuelle multi-commercants ;
- creer un `PaiementReversement` par reversement ;
- creer les transfers Stripe uniquement lors d'une campagne bimensuelle pilotee par Localeo ;
- passer les transfers demandes a un statut en cours explicite ;
- synchroniser `EXECUTE` ou `ECHEC` depuis les statuts Stripe et les reprises techniques ;
- conserver l'historique des echecs et references Stripe.

Les lots de paiement manuel, exports CSV bancaires et confirmations bancaires
manuelles sont decommissionnes par l'EPIC 39.

## 11. Back-office

Le back-office SQLAdmin couvre :

- dashboard operationnel ;
- batchs exploitation ;
- timeline support ;
- referentiels : villes, types, commercants, coffrets, prestations ;
- profils commercants et versions ;
- achats, instances, paiements, remboursements, documents ;
- validations, sessions commercants et acces ;
- reversements, comptes bancaires, lots et paiements ;
- support : motifs, messages, liens courts ;
- emails, SMS, API keys, audit ;
- medias, activites locales, feedbacks.

Exigences transverses :

- toute route `/internal/*` doit exiger une session admin ;
- les actions sensibles doivent produire des traces d'audit ;
- les ecrans affichant IBAN, emails, telephones, tokens ou contenus de messages sont reserves a l'exploitation autorisee.

## 12. Regles transverses

### 12.1 Securite

- Les API internes batch utilisent `X-API-KEY` avec scope.
- Les sessions commercants utilisent `Authorization: Bearer <session_token>`.
- Les achats professionnels utilisent un management token.
- Les tokens bruts doivent etre stockes hashes quand ils sont persistants.
- Les routes publiques d'ecriture doivent etre justifiees, limitees et surveillees.

### 12.2 RGPD et privacy by design

- Les donnees personnelles sont limitees aux besoins achat, activation, support, facturation et reversement.
- Les activites locales et feedbacks publics doivent rester anonymises et moderes.
- Les emails, SMS, IP, user-agent, IBAN, messages support et documents d'achat sont des donnees sensibles a gouverner.
- La retention doit etre documentee et automatisee par type de donnee.
- Les exports et acces back-office doivent etre controles.

### 12.3 Observabilite

- Les actions sensibles doivent inclure `request_id`, acteur, ressource et phase.
- Les logs techniques ne doivent pas contenir de tokens bruts ni de query strings sensibles.
- Les evenements d'audit metier sont la source principale d'investigation fonctionnelle.

## 13. Points bloquants avant production

Les points suivants sont fonctionnellement identifies comme exigences de mise en production :

- proteger les endpoints publics d'ecriture non destines au public ;
- proteger l'upload image ;
- rediger les tokens et donnees personnelles des logs ;
- traiter le risque de tokens en URL ;
- ajouter une protection CSRF au back-office ;
- formaliser la retention RGPD des donnees sensibles ;
- retirer les secrets des fichiers suivis Git et les faire tourner.

## Correctifs Marketplace 2026-09-06

Voir [contrat des correctifs MARKET](../specifications/securisation-production/corrections-marketplace-2026-09-06.md).
