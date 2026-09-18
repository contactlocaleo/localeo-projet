# Epic 38 - Gestion documentaire transverse

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : fournir un socle documentaire transverse pour publier les documents publics Localeo, rattacher les documents contractuels des commercants et tracer les documents generes pour les clients, sans stocker les binaires en base de donnees.
- Decision produit : les documents publics doivent etre disponibles depuis le site web et/ou l'application commercant selon un scope de publication explicite.
- Decision produit : sur le site public, les documents publics frequemment consultes doivent etre affiches en page HTML, avec un lien de telechargement en complement.
- Decision technique : la base stocke uniquement les metadonnees documentaires et une reference de stockage externe, jamais le binaire.
- Decision technique : le stockage production cible est Scaleway Object Storage compatible S3, region Paris.
- Decision operationnelle : les documents doivent etre gerables depuis le back-office, avec statut, dates de publication, remplacement de contenu et audit.
- Decision operationnelle : la publication d'un document public est une action directe realisee par un administrateur autorise, sans workflow de validation multi-etapes au MVP.
- Decision securite : les documents non publics sont soumis a droits d'acces, audit de consultation et telechargement via le backend uniquement.
- Decision securite : les documents publics PDF sont egalement servis via le backend au MVP, afin de garder un point unique de controle et d'audit.

## Probleme

Localeo doit mettre a disposition des documents publics comme les conditions generales, mentions legales et politiques RGPD, tout en conservant les documents contractuels des commercants et les documents clients produits lors des achats. Aujourd'hui, ces besoins sont disperses entre configuration, documents d'achat et surfaces back-office, sans referentiel documentaire transverse.

## Risque business

- Documents legaux publics non maitrisables sans intervention technique.
- Risque d'afficher une version obsolete de CGC, mentions legales ou politique RGPD.
- Difficultes a retrouver le contrat signe d'un commercant.
- Support client ralenti lorsqu'un justificatif ou une facture doit etre retrouve.
- Risque de melanger documents publics, documents contractuels et documents clients.

## Risque technique

- Stocker des binaires en base alourdirait les sauvegardes, migrations et performances.
- Les documents publics et prives n'ont pas les memes contraintes d'acces.
- Les factures clients sont deja partiellement cadrees par l'Epic 14 ; cette epic ne doit pas dupliquer la generation fiscale.
- Les contrats commercants peuvent contenir des donnees sensibles et doivent etre cloisonnes.
- Les remplacements de contenu doivent etre audites pour eviter qu'une mise a jour passe inapercue.

## Perimetre MVP

- Creer un referentiel documentaire transverse en back-office.
- Ajouter une entree back-office `Gestion documentaire`.
- Depuis `Gestion documentaire`, distinguer clairement :
  - documents publics ;
  - documents prives.
- Gerer les documents publics :
  - conditions generales client ou CGC ;
  - mentions legales ;
  - politique de confidentialite / RGPD ;
  - autres documents publics utiles.
- Afficher les documents publics du site sous forme de pages HTML quand le type s'y prete.
- Proposer un lien de telechargement en complement du rendu HTML.
- Lors de l'upload d'un PDF public, permettre de cocher une option `preparer HTML` qui genere une preview HTML modifiable avant sauvegarde, puis stocke le HTML valide comme document derive rattache.
- Associer chaque document public a un ou plusieurs scopes de diffusion :
  - `SITE_PUBLIC` ;
  - `APPLICATION_COMMERCANT` ;
  - `BACKOFFICE` ;
  - `CLIENT_APRES_ACHAT` si necessaire.
- Publier les documents publics par type et scope.
- Filtrer les documents publics par scope, type et statut.
- Mettre a jour un document public en remplacant le contenu du document existant.
- Publier/depublier un document sans redeployer l'application.
- Gerer les documents contractuels des commercants :
  - contrat signe ;
  - avenant ;
  - mandat ;
  - attestation ou justificatif administratif si necessaire.
- Rattacher un document contractuel a un commercant, avec statut et dates utiles.
- Rechercher un client ou un commercant depuis la gestion documentaire pour afficher rapidement ses documents prives.
- Ajouter un document prive depuis la fiche documentaire d'un client ou d'un commercant.
- Mettre a jour un document prive existant en conservant l'historique documentaire.
- Referencer les documents clients issus des achats :
  - recu ;
  - facture ;
  - pack documentaire ;
  - avoir futur si le produit l'introduit.
- Reutiliser les documents d'achat de l'Epic 14 comme producteur de documents clients, sans redefinir les regles de generation fiscale.
- Stocker uniquement les metadonnees en base :
  - type ;
  - scope ;
  - statut ;
  - version ;
  - proprietaire metier ;
  - URI ou cle de stockage ;
  - nom de fichier ;
  - type MIME ;
  - taille ;
  - hash ;
  - dates ;
  - acteur createur/modificateur.
- Telecharger ou consulter les documents via une route controlee.
- Servir les documents prives par le backend uniquement, sans exposer d'URL directe de stockage aux utilisateurs.
- Servir les documents publics PDF via le backend, sans exposer directement l'URL Scaleway.
- Limiter les uploads a 2 Mo par defaut, avec valeur configurable.
- Accepter uniquement PDF et HTML au MVP, avec liste MIME configurable.
- Auditer les creations, publications, remplacements, telechargements et suppressions logiques.
- Ajouter un acces aux documents rattaches depuis les vues 360 client et commercant.

## Hors perimetre MVP

- Stockage du binaire en base de donnees.
- Signature electronique integree.
- Redaction collaborative ou editeur juridique avance.
- Archivage legal certifie.
- Coffre-fort numerique qualifie.
- Workflow complet de validation juridique multi-etapes.
- Facturation electronique B2B obligatoire.
- Generation automatique des contrats commercants.
- Envoi automatique massif des documents publics aux utilisateurs deja inscrits.

## User Stories

1. `PRD-289` En tant qu'admin, je veux creer une fiche documentaire sans stocker le binaire en base afin de centraliser les metadonnees utiles.
   - Statut : `Termine`
   - Resultat attendu : la fiche contient type, titre, statut, version, scope, proprietaire, URI de stockage, nom de fichier, MIME type, taille et hash.
   - Resultat attendu : le binaire est stocke hors base et uniquement reference par une cle ou URI technique.

2. `PRD-290` En tant qu'admin, je veux publier un document public par type et scope afin de maitriser les documents visibles sur le site et l'application commercant.
   - Statut : `Termine`
   - Resultat attendu : le document publie est expose selon ses scopes.
   - Resultat attendu : une mise a jour de contenu conserve le meme identifiant documentaire.

3. `PRD-291` En tant que visiteur du site, je veux consulter les documents publics applicables afin d'acceder aux informations legales a jour.
   - Statut : `Termine`
   - Resultat attendu : les routes publiques exposent uniquement les documents publies avec scope `SITE_PUBLIC`.
   - Resultat attendu : les documents non publies, archives ou reserves au back-office ne sont pas accessibles publiquement.
   - Resultat attendu : les documents publics frequemment consultes sont affiches en page HTML, avec version/date d'application visibles.
   - Resultat attendu : un lien de telechargement reste disponible en complement quand un fichier source ou PDF existe.
   - Resultat attendu : le telechargement public du PDF passe par le backend.

4. `PRD-292` En tant que commercant authentifie, je veux consulter les documents applicables a l'application commercant afin d'acceder aux conditions et informations qui me concernent.
   - Statut : `Termine`
   - Resultat attendu : l'application commercant expose uniquement les documents publies avec scope `APPLICATION_COMMERCANT`.
   - Resultat attendu : l'acces respecte la session commercant et les droits existants.
   - Resultat attendu : le commercant authentifie peut consulter ses propres documents prives rattaches.
   - Resultat attendu : le commercant authentifie ne peut ni voir ni telecharger les documents prives d'un autre commercant.

5. `PRD-293` En tant qu'operateur back-office, je veux rattacher un contrat signe a un commercant afin de retrouver rapidement les documents contractuels du partenaire.
   - Statut : `Termine`
   - Resultat attendu : un document contractuel peut etre rattache a `Commercant`.
   - Resultat attendu : les documents contractuels ne sont jamais exposes sur les routes publiques.

6. `PRD-294` En tant qu'operateur back-office, je veux suivre le statut d'un document contractuel commercant afin de savoir s'il est attendu, recu, signe, expire ou archive.
   - Statut : `Termine`
   - Resultat attendu : le document porte un statut exploitable.
   - Resultat attendu : les dates de signature, debut d'effet, fin d'effet et expiration sont disponibles quand elles s'appliquent.

7. `PRD-295` En tant que systeme documentaire, je veux referencer les documents clients generes lors d'un achat afin de les retrouver depuis les vues support.
   - Statut : `Termine`
   - Resultat attendu : les recus, factures et packs issus de l'Epic 14 creent ou mettent a jour des metadonnees documentaires.
   - Resultat attendu : le document client est rattache a `AchatCoffret`, et optionnellement a `CoffretInstance` et `Client`.

8. `PRD-296` En tant qu'operateur support, je veux retrouver les documents d'un client ou d'un achat afin de repondre rapidement a une demande de justificatif.
   - Statut : `Termine`
   - Resultat attendu : les vues back-office pertinentes affichent les documents rattaches disponibles.
   - Resultat attendu : les liens respectent les droits et auditent les consultations.

9. `PRD-297` En tant que responsable securite, je veux que les documents prives soient servis via une route controlee afin de ne pas exposer les URI de stockage internes.
   - Statut : `Termine`
   - Resultat attendu : les documents contractuels et clients sont telecharges via une route authentifiee.
   - Resultat attendu : les URLs directes de stockage ne sont pas affichees aux utilisateurs non autorises.
   - Resultat attendu : le telechargement des documents prives passe par le backend, qui verifie les droits, trace l'acces et streame le contenu depuis le stockage externe.

10. `PRD-298` En tant qu'admin, je veux archiver ou remplacer un document sans supprimer son historique afin de conserver une trace des versions publiees et contractuelles.
    - Statut : `Termine`
    - Resultat attendu : une suppression fonctionnelle passe le document en `ARCHIVE`.
    - Resultat attendu : l'historique des versions reste consultable par le back-office autorise.

11. `PRD-299` En tant que responsable exploitation, je veux auditer les operations documentaires afin de tracer creation, publication, consultation et archivage.
    - Statut : `Termine`
    - Resultat attendu : chaque action sensible cree un evenement d'audit avec acteur, document, action, date et contexte.

12. `PRD-300` En tant que responsable technique, je veux verifier l'integrite d'un document reference afin de detecter une incoherence entre metadata et stockage externe.
    - Statut : `Termine`
    - Resultat attendu : le hash et la taille sont stockes en metadonnees.
    - Resultat attendu : une verification technique peut signaler un document manquant ou altere.

13. `PRD-301` En tant qu'operateur back-office, je veux acceder a une entree `Gestion documentaire` afin de piloter tous les documents depuis une surface dediee.
    - Statut : `Termine`
    - Resultat attendu : une entree back-office dediee est disponible pour les profils autorises.
    - Resultat attendu : la page distingue immediatement documents publics et documents prives.
    - Resultat attendu : la page donne une vision synthetique du nombre de documents par categorie, statut et anomalie.

14. `PRD-302` En tant qu'operateur back-office, je veux filtrer les documents publics par scope afin de verifier rapidement ce qui est expose sur chaque surface.
    - Statut : `Termine`
    - Resultat attendu : les filtres couvrent scope, type, statut et date de publication.
    - Resultat attendu : la liste identifie clairement les documents publies et archives.

15. `PRD-303` En tant qu'admin, je veux mettre a jour le contenu d'un document public afin de remplacer les CGC, mentions legales ou politiques RGPD proprement.
    - Statut : `Termine`
    - Resultat attendu : l'action de mise a jour ouvre une popup d'upload sur le document existant.
    - Resultat attendu : l'identifiant, les scopes, les rattachements et le statut du document sont conserves.
    - Resultat attendu : les metadonnees techniques fichier, MIME type, taille, hash et cle de stockage sont recalculees.

16. `PRD-304` En tant qu'operateur back-office, je veux rechercher un client ou un commercant depuis les documents prives afin de retrouver rapidement ses documents.
    - Statut : `Termine`
    - Resultat attendu : la recherche accepte nom, email, telephone, nom de commerce et identifiant interne selon le type de cible.
    - Resultat attendu : les resultats separent clients et commercants pour eviter une erreur de rattachement.
    - Resultat attendu : ouvrir un resultat affiche les documents prives rattaches, classes par type et statut.

17. `PRD-305` En tant qu'operateur back-office, je veux ajouter ou mettre a jour un document prive client ou commercant afin de maintenir son dossier documentaire.
    - Statut : `Termine`
    - Resultat attendu : l'ajout rattache le document a la bonne ressource metier.
    - Resultat attendu : la mise a jour conserve l'historique de l'ancien document ou de l'ancienne version.
    - Resultat attendu : les documents prives ne sont jamais exposes sur les surfaces publiques.

18. `PRD-306` En tant qu'operateur support ou exploitation, je veux acceder aux documents d'un client ou d'un commercant depuis sa vue 360 afin de ne pas changer de contexte.
    - Statut : `Termine`
    - Resultat attendu : la vision 360 client affiche un bloc documents avec les documents clients/achats disponibles et un lien vers la gestion documentaire filtree.
    - Resultat attendu : la vision 360 commercant affiche un bloc documents avec contrats, avenants, mandats et documents utiles.
    - Resultat attendu : les actions de consultation et telechargement respectent les droits et sont auditees.

## Regles de gestion

- Le binaire d'un document n'est jamais stocke en base de donnees.
- La base stocke uniquement des metadonnees et une reference de stockage externe.
- Une reference de stockage doit etre opaque pour les utilisateurs finaux.
- Le provider de production est `SCALEWAY_OBJECT_STORAGE`, region Paris.
- Le bucket de production cible est `localeo-archives`.
- Le prefixe applicatif cible est `/archives`.
- La taille maximale d'upload par defaut est 2 Mo et doit etre configurable.
- Les types MIME acceptes au MVP sont PDF et HTML, et doivent etre configurables.
- Un document public doit avoir au moins un scope de diffusion.
- Un document public publie peut etre mis a jour par remplacement de son contenu depuis le back-office.
- La mise a jour conserve le meme identifiant documentaire et fait l'objet d'un audit.
- Les documents publics legaux depublies doivent etre conserves au moins 10 ans apres leur depublication.
- Les documents publics legaux ne font pas l'objet d'une purge automatique au MVP.
- Un document contractuel commercant est toujours rattache a un `Commercant`.
- Un document contractuel commercant expire est archive fonctionnellement et conserve au moins 5 ans apres la fin de la relation commerciale.
- Les factures et documents comptables rattaches a un achat sont conserves 10 ans a partir de la cloture de l'exercice concerne.
- Les factures et documents comptables ne font pas l'objet d'une purge automatique au MVP.
- Un document client est rattache a un `AchatCoffret` quand il concerne un achat.
- Un document prive peut etre rattache a un `Client` ou a un `Commercant` selon sa cible.
- Les documents clients generes par l'Epic 14 restent produits par les use cases de facturation existants.
- Les documents prives exigent une authentification et une autorisation explicites.
- Depuis l'application commercant, un commercant authentifie ne peut consulter que les documents prives rattaches a son propre compte commercant.
- Un document prive rattache a un autre commercant ne doit jamais etre visible ni telechargeable depuis sa session.
- Les consultations de documents prives sont auditees.
- Les documents publics du site sont consultables en HTML par defaut quand le type s'y prete.
- Le telechargement du fichier source PDF reste disponible en complement du HTML.
- Le contenu HTML genere depuis un PDF passe par une etape de preview modifiable avant sauvegarde.
- Le contenu HTML valide depuis la preview est stocke comme un document rattache au document source, avec sa propre cle de stockage et ses propres metadonnees.
- Les documents prives restent servis par telechargement ou previsualisation controlee, jamais par une page publique.
- Les documents archives ne sont plus proposes dans les surfaces publiques ou commercants.
- Les metadonnees doivent permettre de retrouver le fichier dans le stockage externe, verifier son integrite et afficher un libelle comprehensible.

## Typologie documentaire cible

### Documents publics

Types initiaux :

- `CGC`
- `CGV`
- `CGU`
- `MENTIONS_LEGALES`
- `POLITIQUE_CONFIDENTIALITE`
- `POLITIQUE_RGPD`
- `CONDITIONS_UTILISATION`
- `CONDITIONS_COMMERCANTS`

Scopes initiaux :

- `SITE_PUBLIC`
- `APPLICATION_COMMERCANT`
- `BACKOFFICE`
- `CLIENT_APRES_ACHAT`

### Documents commercants

Types initiaux :

- `CONTRAT_COMMERCANT_SIGNE`
- `AVENANT_COMMERCANT`
- `MANDAT`
- `JUSTIFICATIF_ADMINISTRATIF`
- `ATTESTATION`

Statuts initiaux :

- `ATTENDU`
- `RECU`
- `SIGNE`
- `ACTIF`
- `EXPIRE`
- `ARCHIVE`

### Documents clients / achats

Types initiaux :

- `RECU_ACHAT`
- `FACTURE_CLIENT`
- `FACTURE_COMMERCANT`
- `FACTURE_LOCALEO`
- `PACK_FACTURES`

Note : le contenu et les regles fiscales des factures restent portes par l'Epic 14. L'Epic 38 fournit le socle transverse de referencement, consultation, droits et stockage externe.

## Modele cible

### Document

Table cible indicative : `documents`

Champs cibles :

- `id`
- `type_document`
- `categorie` : `PUBLIC`, `COMMERCANT`, `CLIENT`, `ACHAT`, `INTERNE`
- `titre`
- `description`
- `statut`
- `scopes`
- `format_document` : `PDF`, `HTML`, `AUTRE`
- `document_source_id` : document source quand le document est une version derivee, par exemple HTML genere depuis PDF
- `storage_provider`
- `storage_region`
- `storage_bucket`
- `storage_key`
- `storage_uri`
- `filename`
- `mime_type`
- `taille_octets`
- `sha256`
- `date_publication`
- `date_depublication`
- `date_signature`
- `date_debut_effet`
- `date_fin_effet`
- `date_expiration`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`

### Rattachements documentaires

Table cible indicative : `document_rattachements`

Champs cibles :

- `id`
- `document_id`
- `resource_type`
- `resource_id`
- `role_document`
- `created_at`

Ressources cibles MVP :

- `Commercant`
- `AchatCoffret`
- `CoffretInstance`
- `Client` si l'Epic 37 est implementee

## APIs et surfaces cible

- Back-office :
  - acceder a une entree `Gestion documentaire` ;
  - basculer entre documents publics et documents prives ;
  - liste et recherche documents ;
  - filtrer les documents publics par scope, type et statut ;
  - rechercher un client ou un commercant pour consulter ses documents prives ;
  - creation de metadata documentaire ;
  - upload ou rattachement d'un fichier vers stockage externe ;
  - publication/depublication ;
  - rattachement a un commercant, achat, coffret instance ou client ;
  - consultation et telechargement controle.
- Site public :
  - consultation des documents publics publies pour `SITE_PUBLIC` ;
  - consultation HTML des documents publics quand un contenu HTML publie existe ;
  - lien de telechargement complementaire vers le PDF ou fichier source public autorise via le backend.
- Application commercant :
  - consultation des documents publics publies pour `APPLICATION_COMMERCANT` ;
  - consultation des documents contractuels et prives du commercant authentifie uniquement si les documents lui sont rattaches.
- Support :
  - acces depuis vision 360 client, achat et commercant vers les documents rattaches ;
  - lien depuis les vues 360 vers la gestion documentaire deja filtree.
- Stockage :
  - adaptateur de stockage local en developpement ;
  - adaptateur S3 compatible en production ;
  - provider cible production : Scaleway Object Storage ;
  - region cible : Paris ;
  - bucket cible : `localeo-archives` ;
  - prefixe applicatif cible : `/archives` ;
  - configuration par variables d'environnement : endpoint S3, region, bucket, access key, secret key, prefixe applicatif, taille maximale d'upload et types MIME autorises.

## Lots d'implementation

### Lot 1 - Socle metadata et stockage externe

- Creer le modele documentaire.
- Creer l'abstraction de stockage externe.
- Implementer un adaptateur S3 compatible pour Scaleway Object Storage.
- Stocker filename, MIME type, taille et hash.
- Ajouter une configuration de taille maximale d'upload, valeur par defaut 2 Mo.
- Ajouter une configuration des types MIME acceptes, valeur par defaut PDF et HTML.
- Interdire tout stockage binaire en base.

### Lot 2 - Back-office documentaire

- Ajouter l'entree back-office `Gestion documentaire`.
- Ajouter les vues documents publics et documents prives.
- Ajouter les filtres publics par scope, type, statut et version.
- Ajouter la recherche client/commercant pour les documents prives.
- Ajouter upload/rattachement fichier.
- Ajouter publication, archivage et remplacement de contenu.
- Ajouter filtres par categorie, type, statut, scope et ressource rattachee.

### Lot 3 - Documents publics

- Exposer les documents publics publies sur le site.
- Rendre les documents publics du site en pages HTML quand le type s'y prete.
- Generer une preview HTML lors de l'upload d'un PDF si l'admin coche l'option dediee.
- Permettre a l'admin de retoucher la preview HTML avant sauvegarde.
- Stocker le contenu HTML valide comme document rattache au PDF source.
- Ajouter un lien de telechargement complementaire via backend sur les pages HTML.
- Exposer les documents applicables dans l'application commercant.
- Garantir l'exposition des documents publies selon leurs scopes.

### Lot 4 - Documents contractuels commercants

- Rattacher contrats et avenants a un commercant.
- Gerer les statuts contractuels.
- Afficher les documents depuis la vision 360 commercant.
- Ajouter un raccourci depuis la vision 360 commercant vers la gestion documentaire filtree sur ce commercant.
- Auditer consultations et telechargements.

### Lot 5 - Documents clients et achats

- Brancher les documents generes par l'Epic 14 sur le referentiel documentaire.
- Afficher les documents depuis achat, coffret instance et vision 360 client.
- Ajouter un raccourci depuis la vision 360 client vers la gestion documentaire filtree sur ce client.
- Encadrer les droits de telechargement.

### Lot 6 - Securite, audit et exploitation

- Ajouter audit complet des actions documentaires.
- Ajouter controle d'acces par categorie et scope.
- Ajouter verification d'integrite par hash/taille.
- Documenter la configuration du stockage externe.

## Points ouverts

- Aucun point ouvert structurant au stade du cadrage MVP.

## Tests attendus

- Creation de metadata documentaire sans binaire en base.
- Upload/rattachement stocke une reference externe et calcule taille/hash.
- Publication d'un document public.
- Remplacement du contenu d'un document public conserve le meme identifiant et met a jour les metadonnees techniques.
- Generation d'une preview HTML depuis PDF quand l'option est cochee.
- Retouche puis sauvegarde du contenu HTML genere.
- Refus d'un upload depassant la taille maximale configuree.
- Refus d'un upload dont le type MIME n'est pas autorise.
- Route publique refuse un document non publie.
- Application commercant ne voit que les documents de scope commercant.
- Application commercant ne voit que les documents prives rattaches au commercant authentifie.
- Application commercant refuse l'acces aux documents prives rattaches a un autre commercant.
- Contrat commercant rattache visible depuis le back-office autorise.
- Document contractuel inaccessible publiquement.
- Document client rattache a un achat visible depuis le support autorise.
- Telechargement d'un document public PDF via backend.
- Telechargement d'un document prive via backend uniquement.
- Consultation de document prive auditee.
- Verification d'integrite signale un hash incoherent ou un fichier manquant.
