# Specification backend - Carnet Localeo Live persistant et partage entre appareils

> Statut : conception a valider. Cette evolution complete l'Epic 42 sans introduire de compte client. Elle n'est pas implementee dans les lots backend B0 a B8.

## 1. Objectif

Le backend doit permettre a un utilisateur de :

- persister la configuration de son carnet Localeo Live ;
- retrouver les memes passeports/coffrets et participations Animation sur plusieurs appareils ;
- appairer un nouvel appareil depuis un appareil deja autorise ;
- recuperer le carnet lorsqu'aucun ancien appareil n'est disponible ;
- revoquer un appareil perdu ou vole ;
- conserver une experience sans compte, sans email obligatoire et sans mot de passe Localeo.

Le carnet est une identite technique pseudonyme. Il ne constitue pas un profil client et ne doit pas etre utilise pour rapprocher automatiquement des achats, inscriptions ou personnes.

## 2. Principes structurants

1. Une `InstallationLocaleoLive` continue de representer un navigateur ou une PWA installee.
2. Un `CarnetLocaleoLive` represente la bibliotheque partagee.
3. Plusieurs installations peuvent etre rattachees au meme carnet.
4. Chaque installation conserve son propre secret technique et peut etre revoquee independamment.
5. Un token de consultation Coffret ou un token Participant sert de preuve lors de l'ajout initial d'une ressource.
6. Le token brut n'est jamais stocke dans le carnet, recopie vers un autre appareil, journalise ou place dans un evenement.
7. L'association validee `carnet-ressource` devient l'autorisation de consultation pour les appareils membres du carnet.
8. La recuperation sans appareil existant utilise une passkey WebAuthn associee au carnet, et non au profil d'une personne.
9. Les abonnements WebPush, permissions systeme, secrets d'installation et etats de lecture restent propres a chaque appareil.
10. L'activation de la synchronisation est explicite. La bibliotheque locale historique reste utilisable tant que l'utilisateur ne l'active pas.

## 3. Donnees partagees et donnees locales

| Donnee | Portee cible | Observation |
| --- | --- | --- |
| Coffrets/passeports ajoutes | Carnet partage | Association creee apres validation du token de consultation. |
| Participations Animation | Carnet partage | Association creee apres validation du token participant. |
| Animations favorites | Carnet partage | Ressource publique, sans preuve personnelle. |
| Libelle, ordre et archivage d'une ressource | Carnet partage | Versionnes avec le carnet. |
| Secret d'installation | Appareil | Un secret distinct par installation, stocke uniquement sous forme de hash au backend. |
| Credential local de protection des QR | Appareil | Ne participe ni a l'appairage ni a la recuperation du carnet. |
| Abonnement WebPush | Appareil | Endpoint et consentement propres au navigateur. |
| Preferences de notification | Appareil | Ne sont pas imposees aux autres appareils. |
| Inbox et etat lu/non lu | Appareil | Les evenements peuvent etre distribues a chaque appareil actif. |
| Passkey de recuperation | Carnet | Cle publique et metadonnees WebAuthn uniquement. |

## 4. Modele de donnees cible

### 4.1 `localeo_live_carnets`

| Attribut | Type indicatif | Regle |
| --- | --- | --- |
| `id` | UUID | Identifiant opaque non devinable. |
| `statut` | Enum | `INITIALISATION`, `ACTIF`, `SUSPENDU`, `SUPPRIME`. |
| `revision` | BigInt | Incremente a chaque changement partage. |
| `date_creation` | DateTime UTC | Date de creation. |
| `date_modification` | DateTime UTC | Derniere modification fonctionnelle. |
| `date_derniere_activite` | DateTime UTC | Sert a la retention. |
| `date_suppression` | DateTime UTC nullable | Suppression logique avant purge. |

Le carnet ne contient ni nom, ni email, ni telephone, ni adresse postale.

### 4.2 `localeo_live_carnets_installations`

| Attribut | Type indicatif | Regle |
| --- | --- | --- |
| `id` | UUID | Identifiant technique de l'association. |
| `carnet_id` | UUID FK | Carnet rejoint. |
| `installation_id` | UUID FK | Installation Localeo Live. |
| `role` | Enum | `PROPRIETAIRE` ou `MEMBRE`. |
| `libelle_appareil` | Texte nullable | Libelle choisi par l'utilisateur, sans collecte automatique intrusive. |
| `statut` | Enum | `ACTIF`, `REVOQUE`. |
| `date_rattachement` | DateTime UTC | Date de rattachement. |
| `date_derniere_activite` | DateTime UTC | Dernier acces au carnet. |
| `date_revocation` | DateTime UTC nullable | Date de revocation. |

Contraintes :

- unicite de l'installation active dans un carnet ;
- une installation ne peut appartenir qu'a un carnet partage actif a la fois ;
- un carnet actif conserve au moins un proprietaire, sauf pendant une recuperation atomique ;
- une installation revoquee ne peut plus lire ou modifier le carnet.

### 4.3 `localeo_live_carnets_ressources`

| Attribut | Type indicatif | Regle |
| --- | --- | --- |
| `id` | UUID | Identifiant de l'entree du carnet. |
| `carnet_id` | UUID FK | Carnet proprietaire. |
| `type_ressource` | Enum | `COFFRET`, `PARTICIPATION`, `ANIMATION_FAVORITE`. |
| `ressource_id` | UUID | Identifiant du domaine source. |
| `statut` | Enum | `ACTIVE`, `ARCHIVEE`, `INDISPONIBLE`, `SUPPRIMEE`. |
| `libelle_personnalise` | Texte nullable | Valeur partagee facultative. |
| `ordre` | Entier nullable | Ordre partage facultatif. |
| `ajoutee_par_installation_id` | UUID nullable | Audit technique. |
| `preuve_reference` | Identifiant/hash opaque nullable | Reference non reversible de la preuve validee, utilisable pour propager expiration ou revocation. |
| `date_validation_preuve` | DateTime UTC nullable | Date de validation du token initial. |
| `date_creation` | DateTime UTC | Date d'ajout. |
| `date_modification` | DateTime UTC | Derniere modification. |

Contrainte d'unicite : `(carnet_id, type_ressource, ressource_id)`.

Le token brut et une version chiffree reversible du token sont interdits dans cette table. Une reference opaque ou un hash non reversible peut etre conserve uniquement pour appliquer le cycle de vie de la preuve initiale.

### 4.4 `localeo_live_carnets_credentials`

Cette table porte les passkeys de recuperation verifiees par le backend.

| Attribut | Type indicatif | Regle |
| --- | --- | --- |
| `id` | UUID | Identifiant interne. |
| `carnet_id` | UUID FK | Carnet recuperable. |
| `credential_id` | Binaire/texte base64url | Identifiant WebAuthn unique. |
| `public_key` | Binaire | Cle publique COSE ; aucune cle privee. |
| `sign_count` | BigInt | Compteur WebAuthn lorsque disponible. |
| `transports` | JSON | Indications de transport declarees par le client. |
| `backup_eligible` | Bool nullable | Information WebAuthn disponible. |
| `backup_state` | Bool nullable | Information WebAuthn disponible. |
| `statut` | Enum | `ACTIF`, `REVOQUE`. |
| `date_creation` | DateTime UTC | Date d'enregistrement. |
| `date_derniere_utilisation` | DateTime UTC nullable | Derniere recuperation. |
| `date_revocation` | DateTime UTC nullable | Revocation. |

Plusieurs passkeys peuvent proteger un meme carnet. Le backend ne suppose pas qu'elles appartiennent juridiquement a une meme personne.

### 4.5 `localeo_live_carnets_appairages`

| Attribut | Type indicatif | Regle |
| --- | --- | --- |
| `id` | UUID | Identifiant de la demande. |
| `carnet_id` | UUID FK | Carnet cible. |
| `cree_par_installation_id` | UUID FK | Appareil initiateur. |
| `demande_par_installation_id` | UUID FK nullable | Nouvel appareil apres resolution. |
| `token_hash` | Texte | Hash du secret d'appairage, jamais le secret brut. |
| `code_saisie_hash` | Texte | Hash du code temporaire saisissable sur un appareil sans camera. |
| `code_controle_hash` | Texte nullable | Verification visuelle, non suffisante comme preuve. |
| `statut` | Enum | `OUVERT`, `EN_ATTENTE_CONFIRMATION`, `CONFIRME`, `EXPIRE`, `REVOQUE`. |
| `date_expiration` | DateTime UTC | Duree cible : dix minutes. |
| `date_utilisation` | DateTime UTC nullable | Consommation unique. |

La consommation et le rattachement sont atomiques. Un appairage expire ou deja utilise produit une erreur metier sans reveler le carnet cible.

Le secret QR et le code de saisie donnent acces a la meme invitation mais utilisent des formats adaptes :

- le secret QR conserve une forte entropie et est transporte dans le fragment du lien ;
- le code de saisie utilise douze caracteres Base32 non ambigus, affiches en trois groupes de quatre, par exemple `K7MP-4T9Q-W2DX` ;
- le code expire apres dix minutes, est insensible a la casse et aux separateurs, et n'est jamais journalise ;
- cinq saisies invalides au maximum sont acceptees pour une invitation ; au-dela, elle est revoquee ;
- le rate limiting combine invitation, installation de destination et signal reseau disponible, sans fingerprinting ;
- meme avec un code correct, le rattachement exige la confirmation finale sur un appareil proprietaire.

### 4.6 Challenges WebAuthn

Les challenges d'enregistrement et de recuperation sont aleatoires, a usage unique, lies a l'operation et expires rapidement. Ils peuvent etre stockes dans une table technique ou un cache partage compatible avec le deploiement multi-instance.

## 5. Roles et autorisations

| Operation | Membre | Proprietaire | Passkey de recuperation |
| --- | --- | --- | --- |
| Lire le carnet | Oui | Oui | Non, avant recuperation. |
| Ajouter/archiver une ressource | Oui | Oui | Non. |
| Creer un appairage | Non par defaut | Oui | Non. |
| Lister les appareils | Oui | Oui | Non. |
| Revoquer son propre appareil | Oui | Oui | Non. |
| Revoquer un autre appareil | Non | Oui | Apres recuperation. |
| Ajouter/revoquer une passkey | Non | Oui | Apres recuperation. |
| Supprimer le carnet | Non | Oui | Apres recuperation. |

La possibilite d'autoriser les membres a creer un appairage reste un arbitrage produit. Le modele initial la reserve aux proprietaires.

## 6. Parcours backend

### 6.1 Activation du carnet partage

1. Une installation authentifiee demande l'activation de la synchronisation.
2. Le backend cree un carnet `INITIALISATION` et rattache l'installation comme `PROPRIETAIRE`.
3. Le backend emet les options WebAuthn d'enregistrement d'une passkey recuperable.
4. La PWA cree la passkey avec `residentKey=required`, `userVerification=required` et `attestation=none`.
5. Le backend verifie l'attestation et enregistre la cle publique.
6. Le carnet passe a `ACTIF`.
7. La PWA presente ses ressources locales ; chaque token est valide par son domaine puis immediatement oublie.
8. Les associations carnet-ressource sont creees de maniere idempotente.

Un carnet reste en `INITIALISATION` pendant une duree bornee s'il n'obtient aucun credential de recuperation. Il est ensuite purge.

### 6.2 Ajout d'une ressource

- `COFFRET` : validation du token de consultation par `gestion_achats` ;
- `PARTICIPATION` : validation du token participant par `animation_locale` ;
- `ANIMATION_FAVORITE` : verification de l'existence et de la visibilite publique de l'animation.

Apres validation, le backend stocke l'association et emet une nouvelle revision du carnet. Un token invalide, expire ou revoque n'est jamais transforme en autorisation de carnet.

La lecture ulterieure utilise l'appartenance au carnet. Les domaines sources restent responsables du statut metier de la ressource et du cycle de vie de la preuve initiale. Une ressource ou une preuve expiree, annulee, revoquee ou supprimee devient `INDISPONIBLE` sans reutiliser le token initial.

### 6.3 Appairage d'un nouvel appareil

1. Le proprietaire cree une invitation a usage unique.
2. Le backend retourne le secret uniquement dans la reponse de creation.
3. La PWA construit un lien `/live/appairer#code=...`, son QR et un code de saisie temporaire.
4. Le nouvel appareil cree sa propre installation, puis transmet dans le corps de la requete de resolution soit le secret lu dans le fragment, soit le code saisi manuellement.
5. Le backend cree une demande `EN_ATTENTE_CONFIRMATION` et retourne un code de controle non sensible aux deux appareils.
6. Le proprietaire confirme la demande.
7. Le backend consomme l'invitation et rattache le nouvel appareil comme `MEMBRE` dans une transaction unique.
8. Le nouvel appareil recupere le snapshot courant du carnet.

Le secret d'appairage n'apparait ni dans un chemin API, ni dans une query string, ni dans les logs.

Un PC sans camera ouvre directement `/live/appairer`, saisit le code temporaire affiche sur le mobile, puis suit le meme parcours de controle visuel et de confirmation. L'installation de la PWA sur le PC peut etre proposee apres le rattachement et ne constitue pas un prerequis.

### 6.4 Recuperation sans ancien appareil

1. Le nouvel appareil cree une installation et son secret propre.
2. Il demande un challenge de recuperation sans fournir d'identifiant client.
3. Le navigateur selectionne une passkey decouvrable et produit une assertion WebAuthn.
4. Le backend retrouve le carnet par `credential_id`, verifie challenge, origine, RP ID, signature et verification utilisateur.
5. Dans une transaction, il rattache la nouvelle installation comme `PROPRIETAIRE`.
6. Il retourne la liste des anciens appareils sous une forme non sensible afin de proposer leur revocation.
7. L'utilisateur peut revoquer tous les anciens appareils ou seulement l'appareil perdu.

La recuperation est impossible si aucune passkey n'a ete enregistree ou n'est disponible. Un code de recuperation a forte entropie peut etre ajoute comme secours apres arbitrage ; il doit alors etre stocke uniquement sous forme de hash, limite en tentatives et remplace apres utilisation.

### 6.5 Revocation d'un appareil

La revocation :

- desactive immediatement l'association appareil-carnet ;
- revoque les abonnements WebPush de l'installation ;
- invalide ou fait tourner son secret d'installation ;
- conserve une trace technique pendant la duree de retention ;
- n'efface pas les ressources du carnet partage.

## 7. Contrats API cibles

Les chemins restent sous `/public/localeo-live`. Tous les endpoints lies a une installation utilisent `X-Localeo-Live-Secret` et verifient que l'identifiant du chemin correspond a cette installation.

### 7.1 Carnet et synchronisation

| Methode | Chemin cible | Usage |
| --- | --- | --- |
| `POST` | `/installations/{installation_id}/carnet` | Initialiser l'activation du carnet partage. |
| `GET` | `/installations/{installation_id}/carnet` | Obtenir le snapshot partage et sa revision. |
| `GET` | `/installations/{installation_id}/carnet/ressources` | Lister les ressources et leurs projections minimales. |
| `POST` | `/installations/{installation_id}/carnet/ressources` | Ajouter une ressource apres validation de sa preuve. |
| `PATCH` | `/installations/{installation_id}/carnet/ressources/{entree_id}` | Modifier libelle, ordre ou archivage. |
| `DELETE` | `/installations/{installation_id}/carnet/ressources/{entree_id}` | Retirer la ressource du carnet pour tous les appareils. |

La lecture retourne un `ETag` derive de la revision et accepte `If-None-Match`. Les commandes acceptent une cle d'idempotence. Les modifications concurrentes utilisent la revision attendue ou `If-Match` et retournent `409` en cas de conflit.

### 7.2 Appairage et appareils

| Methode | Chemin cible | Usage |
| --- | --- | --- |
| `POST` | `/installations/{installation_id}/carnet/appairages` | Creer une invitation courte. |
| `POST` | `/appairages/resolution` | Presenter le secret QR ou le code de saisie depuis un nouvel appareil. |
| `GET` | `/installations/{installation_id}/carnet/appairages/{appairage_id}` | Suivre l'etat par interrogation bornee. |
| `POST` | `/installations/{installation_id}/carnet/appairages/{appairage_id}/confirmation` | Confirmer le nouvel appareil. |
| `DELETE` | `/installations/{installation_id}/carnet/appairages/{appairage_id}` | Annuler une invitation. |
| `GET` | `/installations/{installation_id}/carnet/appareils` | Lister membres et activite recente. |
| `DELETE` | `/installations/{installation_id}/carnet/appareils/{appareil_id}` | Revoquer un appareil. |

### 7.3 Passkeys et recuperation

| Methode | Chemin cible | Usage |
| --- | --- | --- |
| `POST` | `/installations/{installation_id}/carnet/passkeys/enregistrement/options` | Emettre les options d'enregistrement. |
| `POST` | `/installations/{installation_id}/carnet/passkeys/enregistrement/verification` | Verifier et enregistrer la cle publique. |
| `GET` | `/installations/{installation_id}/carnet/passkeys` | Lister les credentials sans information sensible. |
| `DELETE` | `/installations/{installation_id}/carnet/passkeys/{credential_id}` | Revoquer une passkey en conservant au moins un moyen de recuperation. |
| `POST` | `/recuperations/passkey/options` | Emettre un challenge sans identifiant de compte. |
| `POST` | `/recuperations/passkey/verification` | Verifier l'assertion et rattacher la nouvelle installation. |

Tous les corps, reponses et erreurs devront etre modelises dans OpenAPI avant implementation. Aucun modele ORM ne sera expose directement.

## 8. Synchronisation et conflits

- le backend est la source de verite pour un carnet partage actif ;
- chaque mutation incremente `revision` une seule fois dans la transaction ;
- les ajouts repetes sont dedupliques par contrainte d'unicite ;
- une suppression partagee retire la ressource de tous les appareils ;
- un client hors ligne conserve ses commandes dans une file locale, avec cle d'idempotence ;
- le backend refuse une modification basee sur une revision obsolete lorsque le contenu risque d'etre ecrase ;
- une resynchronisation complete reste possible a tout moment ;
- aucun token personnel ne figure dans les deltas ou snapshots.

Pour le premier lot, un snapshot complet avec `ETag` est suffisant compte tenu du faible volume attendu. Un endpoint de deltas par revision ne sera ajoute qu'apres mesure du besoin.

## 9. Securite

- secrets d'installation, d'appairage et de recuperation generes avec un generateur cryptographique ;
- secrets persistants stockes sous forme de hash ;
- challenges et invitations a usage unique avec expiration ;
- controle d'autorisation objet sur chaque acces carnet, ressource, appareil et credential ;
- rate limiting distinct pour activation, appairage, ajout par token et recuperation ;
- limitation a cinq codes de saisie invalides par invitation, avec revocation automatique et reponse ne permettant pas d'enumerer les invitations ;
- verification WebAuthn complete cote serveur : challenge, type, origine, RP ID, signature, `userVerification` et compteur lorsque pertinent ;
- aucune donnee biometrique transmise ou conservee par Localeo ;
- aucune enumeration de carnet a partir d'un `credential_id` inconnu ;
- payloads de logs limites aux identifiants techniques et statuts, sans secret, token ou contenu personnel ;
- QR personnels et projections sensibles servis avec `Cache-Control: no-store` ;
- alertes operationnelles sur echecs repetes de recuperation et appairages anormaux, sans fingerprinting.

La passkey de recuperation est differente du credential WebAuthn local utilise par la PWA pour verrouiller l'affichage d'un QR. La premiere est verifiee par le serveur ; le second reste une protection locale de l'appareil.

## 10. Migration de l'existant

1. Ajouter les nouvelles tables sans modifier le comportement des installations existantes.
2. Conserver les bibliotheques IndexedDB existantes en mode local.
3. Lors de l'activation explicite, creer un carnet et enregistrer une passkey de recuperation.
4. Reprendre les `SuiviRessourceLocaleoLive` deja verifies pour l'installation.
5. Demander au frontend de presenter temporairement les tokens des autres entrees locales afin de les valider et de creer les associations manquantes.
6. Ne supprimer les donnees locales historiques qu'apres confirmation d'un snapshot serveur complet.
7. Conserver une compatibilite de lecture avec les suivis par installation pendant une periode de migration bornee.

Une installation deja rattachee a un autre carnet partage ne peut pas rejoindre silencieusement un nouveau carnet. Une fusion explicite et transactionnelle est requise ou l'operation est refusee.

## 11. Retention et suppression

- une invitation expiree est purgee rapidement ;
- les challenges WebAuthn sont purges apres expiration ou utilisation ;
- les associations d'appareils revoques suivent la retention technique des installations ;
- un carnet inactif suit une duree a arbitrer et fait l'objet d'une suppression logique avant purge ;
- la suppression du carnet revoque tous ses appareils, passkeys et autorisations de ressources ;
- les donnees metier sources, comme un achat ou une participation, ne sont pas supprimees par la suppression du carnet ;
- l'utilisateur peut exporter une liste non sensible des ressources avant suppression, sans exporter les tokens.

## 12. Observabilite

Metriques minimales :

- carnets initialises, actifs et supprimes ;
- nombre d'appareils actifs par carnet sous forme agregee ;
- appairages crees, expires, confirmes et refuses ;
- recuperations reussies et echouees par cause technique ;
- ressources ajoutees, dedupliquees, devenues indisponibles et retirees ;
- conflits de revision et duree de synchronisation.

Aucune metrique ne doit permettre de reconstruire le contenu nominatif d'un carnet.

## 13. Tests d'acceptation backend

- une installation non membre ne peut pas lire un carnet en connaissant son UUID ;
- deux appareils membres recoivent le meme snapshot fonctionnel ;
- les secrets de chaque installation restent distincts ;
- la revocation d'un appareil n'affecte pas les autres ;
- un appairage expire, reutilise ou annule est refuse ;
- un PC sans camera peut demander l'appairage avec le code temporaire affiche sur le mobile ;
- un code de saisie incorrect est limite en tentatives et sa valeur n'apparait dans aucun log ;
- le nouvel appareil ne rejoint le carnet qu'apres confirmation du proprietaire ;
- un token Coffret ou Participant invalide ne cree aucune association ;
- aucun token brut n'est persiste ou journalise ;
- un ajout concurrent de la meme ressource produit une seule entree ;
- une passkey valide permet la recuperation sans ancien appareil ;
- une assertion rejouee, d'une autre origine ou avec un challenge expire est refusee ;
- la recuperation permet de revoquer les anciennes installations ;
- les preferences WebPush d'un appareil ne modifient pas celles des autres ;
- la suppression du carnet revoque tous les acces sans supprimer les objets metier sources.

## 14. Hors perimetre

- compte client avec email ou mot de passe ;
- rapprochement automatique par email, telephone ou moyen de paiement ;
- partage selectif d'une seule ressource avec une autre personne ;
- roles familiaux ou delegation permanente a un tiers ;
- synchronisation des permissions systeme et abonnements WebPush ;
- conservation ou transfert des tokens personnels bruts ;
- garantie contre la capture d'ecran d'un QR deja affiche.

## 15. Points a arbitrer avant implementation

1. Nombre maximal d'appareils actifs par carnet ; proposition : cinq.
2. Les membres peuvent-ils inviter un appareil ou seulement les proprietaires ; proposition : proprietaires uniquement.
3. Code de recuperation en secours de la passkey ; proposition : phrase a forte entropie, affichee une fois et renouvelee apres usage.
4. Fusion de deux carnets partages existants ; proposition : hors premier lot, avec refus explicite et conservation des deux carnets.
5. Suppression d'une ressource ; proposition : suppression partagee, avec simple archivage pour eviter les erreurs.
6. Duree de retention d'un carnet inactif ; proposition : notification apres 24 mois, purge apres 30 mois sans activite.
7. Possibilite d'avoir plusieurs proprietaires ; proposition : oui, afin d'eviter un appareil maitre unique.
8. Cycle de vie de l'autorisation carnet apres expiration ou revocation du token initial ; proposition : conserver une reference de preuve non reversible et rendre l'entree indisponible des que le domaine source invalide cette preuve.
