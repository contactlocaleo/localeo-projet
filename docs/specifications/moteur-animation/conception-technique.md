# Moteur d’animation — lot de conception technique V1

Date : 19 septembre 2026. Statut : **conception de référence pour l’implémentation**, sans code métier, migration exécutée ni recette fonctionnelle livrés par ce document.

Ce lot concrétise les six sujets techniques identifiés après la [spécification fonctionnelle](localeo_animation_engine_spec.md). Il ne rouvre pas les arbitrages TRE-ARB-60 à TRE-ARB-91. Le [backlog EPIC 55](../../roadmap/en-cours/epic-55-chasse-tresor-commercante-backlog.md) conserve l’état produit **En cours**. Les noms et protocoles ci-dessous fixent la cible d’implémentation ; les exemples antérieurs restent des supports de conception et ne prouvent pas la présence de ces API.

## 1. Décisions et périmètre

| Sujet | Décision technique | Sections |
| --- | --- | --- |
| Contrats de production | Modèles backend fermés, exports automatiques, séparation génération/préparation/définition/projections ; registre par type/version. | 3 |
| Stockage et versions | Réutiliser Animation, configurations, participants, validations, demandes EPIC 56 et opérations ; ajouter les données d’exécution et de génération manquantes. | 4 |
| Concurrence et reprise | PostgreSQL : barrière commune par animation, verrou exclusif par participation, reçu idempotent dans la transaction métier et clôture exclusive. | 5 |
| API, droits et confidentialité | Étendre les routes existantes, permissions par action et périmètre, projections construites par liste de champs autorisés. | 6 |
| Médias et limites | Import autonome WebP/base64 contrôlé, limites distinctes média/document/commande ; aucune image future dans Live. | 7 |
| Exploitation et recette | Traitements PostgreSQL reprenables, purge quotidienne contrôlée, audit existant, bascule directe et livraison par parcours complets. | 8–9 |

Les trois moteurs V1 sont `PASSEPORT_COMMERCANT`, `TOMBOLA_LOCALE` et `CHASSE_TRESOR_COMMERCANTE`. Le dernier code est fixé pour l’implémentation. La génération automatique intégrée reste après le pilote : en V1, on produit le prompt, attend une exécution manuelle outillée puis importe le JSON complet. Aucun nouveau broker, moteur de workflow ou service IA pendant le jeu.

## 2. Ancrage dans le code existant

Inspection statique du workspace au 19 septembre 2026, sans import de `app.main`, chargement de secrets, accès à une base ni appel externe. Les chemins ci-dessous sont relatifs à la racine du dépôt nommé ; les nouveaux chemins de la section 3 sont explicitement des cibles.

| Dépôt / point d’entrée existant | Réemploi et adaptation nécessaires |
| --- | --- |
| Backend — `app/domaine/animation_locale/services/registre_strategies_modeles_animation.py` | `RegistreStrategiesModelesAnimation` connaît Passeport/Tombola. L’étendre en registre type/version ; ne pas ajouter de dispatch de chasse dans chaque route. |
| Backend — `app/domaine/animation_locale/entities/operation_animation.py` | Réutiliser `OperationAnimation` ; ses six états actuels ne décrivent pas l’attente humaine. Ajouter les phases de génération et les leases définis ci-dessous. |
| Backend — `AnimationOrm`, `ConfigurationAnimationOrm`, `ParticipantAnimationOrm`, `ValidationAnimationOrm` | Conserver identités, liens commerciaux et preuves ; la configuration est déjà JSONB. Les versions de progression et la coordination par participation sont à ajouter. |
| Backend — `ServiceDemandesParticipationCommercants` | Réutiliser les invitations EPIC 56, leurs notifications et décisions. Étendre le snapshot par commerçant avec alternatives, choix unique et confirmations versionnées. |
| Backend — `ServiceValidationsAnimation`, `ServiceTiragesAnimation` | Le verrou animation actuel sérialise les validations. Toutes les entrées rejoignent la barrière de la section 5 ; la clôture requalifie avant de figer. |
| Backend — `ServiceConservationAnimation` | Conserver les règles existantes participants/tokens ; ajouter les catégories de jeu et génération, leurs références utiles et gels. |
| Marketplace — `src/live/LiveApp.jsx`, `src/services/api.js`, `src/live/liveLibrary.js`, `public/live/sw.js` | Réutiliser accès personnels, carnet et shell ; remplacer la projection complète des commerces pour la chasse, isoler les saisies temporaires et exclure API/médias privés du cache PWA. |

Une table ou un helper portant un nom d’idempotence n’est pas une preuve d’atomicité : le contrôle de clé, la mutation, le reçu et l’outbox doivent partager la même UoW. Une liste d’opérations exécutables n’est pas un worker avec claim/reprise ; ce worker reste à réaliser.

## 3. Contrats de production et frontières

### 3.1 Source et exports

Le domaine `animation_locale` possède les règles et objets-valeur sans Pydantic, ORM, HTTP ni fournisseur. Les DTO Pydantic fermés appartiennent à une cible `app/application/animation_locale/contrats_moteur/`, réutilisée par API, ERP, import et export, distincte du fichier `contracts.py` existant. Les adaptateurs traduisent ces DTO en objets du domaine ; aucun endpoint ne devient le seul gardien d’un invariant.

Un générateur à créer dans `localeo-backend/scripts/documentation/` exporte les JSON Schema depuis ces modèles, sans bootstrap applicatif ni base. Il produit un manifeste `{type, contractVersion, schemaName, sha256}` et les schémas de génération, définition, commandes et projections. Les contrats OpenAPI documentaires restent dans le projet central ; les contrats embarqués restent auprès de leurs consommateurs. La CI compare les exports régénérés et les empreintes consommées. Aucun second schéma de production écrit à la main.

Le [schéma Latresne révision 8](contrats/reponse-generation-chasse.schema.json) reste un **document d’entrée** et une fixture à porter lors du premier lot. Son numéro de révision n’est pas `engineConfigVersion`. La maquette est un support UX, jamais la source du protocole backend.

### 3.2 Documents distincts

| Contrat cible | Contenu et propriétaire |
| --- | --- |
| `DemandeGenerationInput` | `animation_id` facultatif, `type`, `engine_contract_version`, paramètres d’initialisation autorisés et `brief`. Sans animation existante, création atomique d’un brouillon unique. Avec un brouillon, rattachement après contrôle de périmètre/version. |
| `BriefGenerationChasse` | `commercants[]`, `poi[]`, `nombreEtapes:{min,max}`, `dureeCibleMinutes`, `publicVise`, `difficulte`, `theme`. Le serveur photographie les lieux autorisés et faits utiles. Dates, minimum de commerçants, accords et checklist appartiennent à la préparation et ne deviennent pas des instructions créatives obligatoires. |
| `ResultatGenerationChasse` | Structure éditoriale issue de la révision 8 : titre, synopsis, durée estimée, difficulté, introduction, étapes ordonnées, conclusion, thème facultatif, `medias` obligatoire. Une position commerçante contient les missions candidates, sans mission choisie ni accord. |
| `PreparationChasse` | Révision de préparation, résultat source, ordre et identifiants stables des positions/missions/conditions, minimum de commerçants, références des décisions EPIC 56 et vérifications de préparation/POI. Les statuts de consentement sont lus depuis EPIC 56, jamais modifiables via ce JSON. |
| `DefinitionAnimationV1` | Enveloppe `schemaVersion`, `definitionVersion`, `type`, `engineConfigVersion`, `common`, `engineConfig`. Construction serveur ; uniquement les missions retenues. Elle ne contient pas les états de participants. |
| Projections | Quatre modèles distincts : public, participant, commerçant, organisateur. Une projection n’est ni le document éditorial ni une définition privée expurgée après sérialisation. |

Identifiants persistants en UUID ; identifiants locaux de défi opaques, chaînes de 1 à 64 caractères. Dates d’API ISO 8601 avec fuseau, normalisées en UTC ; durées en minutes entières positives. Pour le brief, `difficulte` reste une indication éditoriale courte (1–80 caractères) et `publicVise` un texte (1–500) : aucune nouvelle échelle métier obligatoire. `min >= 1`, `max >= min` ; un résultat hors fourchette déclenche l’avertissement déjà décidé, pas un échec de schéma ni un ajustement silencieux du brief. Pas de nombre d’étapes fixé par le schéma.

Le contrat générique de production remplace les noms de lieux comme clés par `lieu:{type:COMMERCANT|POI,id:UUID}` ou `null` pour le virtuel. Le schéma instancié pour une demande restreint les couples type/id aux lieux du brief. Les noms/adresses sont des faits fournis dans le prompt puis résolus depuis le snapshot autorisé, jamais des identités à deviner. Le portage de la fixture Latresne résout ses noms explicitement et refuse une correspondance absente/ambiguë ; aucune compatibilité de production historique n’est requise.

Tous les objets sont fermés (`extra=forbid`). En particulier, le résultat fournisseur ne reçoit ni propriétaire, dates opérationnelles, gains, règles de qualification, choix commerçant, permissions ni code exécutable. L’import fournit séparément `prompt_id`, `request_hash` et la réponse. Les contrôles de structure précèdent les contrôles du domaine et la relecture.

### 3.3 Assemblage déterministe

1. Importer une proposition valide en conservant son brut et sa provenance. Attribuer les UUID stables de préparation ; une révision qui conserve une mission conserve son identité, une nouvelle alternative reçoit une nouvelle identité.
2. Avant invitation, photographier pour chaque commerce la mission proposée et les engagements applicables. La version de confirmation porte sur les conditions stables de cette révision, jamais sur leur index dans un tableau.
3. Après stabilisation, retenir exactement la mission confirmée de chaque commerce conservé. Refuser les décisions obsolètes, prérequis manquants, invitations encore en attente ou minimum non atteint.
4. Compiler l’ordre en `startStepId`, une transition `SUCCESS/targetStepId` par étape non terminale et `transitions:[]` à la fin. Une seule position par identité de commerce. Préserver les dépendances explicites et vérifier qu’aucune suite ne dépend du code particulier d’une variante écartée.
5. Construire `common` depuis les paramètres serveur et les références autorisées ; appliquer la matrice défi/validation, les contrôles de thème/médias et la checklist. Attribuer une nouvelle version de configuration, son empreinte et le contrat moteur.
6. La commande de publication fige cette version. L’acceptation du résultat IA complète seulement le brouillon ; elle ne publie pas l’événement.

Le début/la finale sont des rôles distincts du lieu : `roles` vaut `[]`, `["START"]`, `["FINAL"]` ou `["START","FINAL"]`. Le compilateur les dérive de la première/dernière position ; une étape unique porte les deux. Il fixe `location` en `MERCHANT`, `POI` ou `VIRTUAL`, avec `refId` requis pour un lieu physique et nul pour le virtuel. Une position portant `FINAL` reçoit `Step.type=FINAL` ; les autres catégories suivent la matrice de la spécification, sans second choix indépendant du rôle. Un départ/finale physique conserve les obligations de son lieu ; un rôle narratif ne les efface pas. Le renderer est choisi par `challenge.type`. Les catégories éditoriales observation/recherche deviennent `SINGLE_CHOICE`, sans nouvelle primitive.

### 3.4 Module et versionnement

Étendre le registre existant avec un descripteur `(type, contractVersion)` et les références internes vers : validateurs de configuration, commandes, état, qualification, projections, capacités, préparation et génération facultative. Séparer le registre de fonctions métier pures et l’assemblage applicatif qui lui associe DTO/adaptateurs ; le domaine n’importe aucun renderer ou schéma Pydantic.

Interface métier cible : `valider_configuration`, `initialiser_etat`, `decider_commande`, `qualifier`, `calculer_impact_retrait`. Les entrées sont des faits immuables chargés par l’application ; la sortie est une décision et des intentions d’effets, jamais un commit, paiement ou envoi direct. Les constructeurs de projection appliquent les règles de visibilité exposées par le moteur et énumèrent leurs champs.

| Version | Usage |
| --- | --- |
| `schemaVersion="1.0"` | Contrat de l’enveloppe commune. |
| `engineConfigVersion="1.0"` | Contrat coordonné configuration/commandes/projections pour le type. Refuser une version absente du registre ; aucun repli sur Chasse. |
| `definitionVersion` | Version immuable du contenu accepté/publié ; liée à la version de configuration persistée. |
| `preparation_revision` | Retouches et engagements avant publication ; peut invalider seulement les accords affectés. |
| `revision_exploitation` | Retrait global, changement autorisé de dates/capacité, clôture ; ne réécrit pas le contenu publié. |
| `progression_version` | Toute mutation des acquis/essais/aides d’une participation ; utilisée pour les commandes concurrentes. |
| Prompt/résultat | Révision de prompt et identifiant de tentative distincts ; aucun écrasement d’une version acceptée. |

Les trois interfaces enregistrent leurs renderers avec la même version de contrat. L’ouverture du catalogue est conditionnée au déploiement coordonné des versions supportées ; aucune sélection de composant par nom fourni dans le JSON. Pas de migration d’une partie publiée vers une nouvelle version au milieu du jeu.

## 4. Modèle physique et workflows

### 4.1 Principes de persistance

Les noms SQL ci-dessous fixent les **ajouts cibles**, à introduire par nouvelles migrations, sans réécriture des migrations appliquées. UUID pour les identités, `timestamptz` pour les instants, `bigint` positif pour les révisions, JSONB pour les documents de configuration. Foreign keys explicites et suppressions `RESTRICT` sur provenance, preuves et versions utilisées ; pas de cascade depuis les essais vers participation/tirage.

`Animation` reste l’événement métier. Il n’est créé ni second agrégat commercial `AnimationInstance`, ni nouveau participant pour la chasse. `ConfigurationAnimation` conserve le JSON de préparation et le DSL accepté dans des clés distinctes typées de `parametres`; une version publiée ne s’édite plus. Une configuration peut référencer un template réutilisable ; le template conserve sa provenance et n’emporte jamais accords, tokens ou participations.

| Table cible / adaptation | Données et contraintes principales |
| --- | --- |
| `animation_coordinations` (ajout) | PK/FK `animation_id`, `revision_exploitation`, `preparation_revision`. Ligne créée avec toute animation et rétroremplie avant activation ; barrière de verrouillage, sans compteur de participants. |
| Configurations existantes | Ajouter discriminant moteur/version, empreinte du DSL et référence à la version publiée. Unicité `(animation_id,version)`. Le JSON de préparation et la définition restent privés. |
| Participants existants | Conserver identité/accès ; déclaration adulte et version de règlement/checklist référencées. Le comptage de capacité porte sur inscriptions uniques, pas les sessions. |
| `animation_executions` (ajout) | PK `participant_id`, FK animation/configuration jouable, `progression_version`, état spécifique typé, `started_at`, `completed_at`, `revision_exploitation_appliquee`. Une exécution par participation ; le détail Chasse est structuré dans les tables suivantes. |
| `animation_executions_etapes` (ajout) | UNIQUE `(participant_id,step_id)` ; dates de déblocage/QR/résolution/aide/confirmation, statut narratif, référence de preuve effective, compteur d’essais et ordre de présentation persistant. Les compteurs ne remplacent pas le contrôle de la preuve. |
| `animation_tentatives_defi` (ajout) | UUID, participant/étape/commande, réponse privée, résultat, date ; UNIQUE `(command_receipt_id)` pour une soumission. Index `(animation_id,created_at,id)` pour purge. |
| `animation_effets_participation` (ajout) | UNIQUE `(participant_id,definition_version,effect_key)` ; origine étape, type, provenance `REUSSITE` ou `DISPENSE`, date. Même clé pour l’effet acquis normalement ou fourni par dispense. |
| `animation_neutralisations_etapes` (ajout) | UNIQUE `(animation_id,definition_version,step_id)` ; motif, auteur, révision exploitation, date et dépendances à fournir. Pas de neutralisation individuelle V1. |
| `animation_qr_lieux` (ajout) | UUID opaque, animation, version publiée, étape, révision de QR, condensat du secret, activation/révocation. FK vers le lieu autorisé et UNIQUE sur la révision ; ne réutilise pas un QR participant. |
| Bibliothèque POI et éditions (ajouts) | `animation_poi` : partenaire, identité, adresse et faits ; `animation_poi_versions` : snapshot immuable ; `animation_poi_verifications` : animation, version POI, auteur/date, emplacement QR, observations, photo facultative, checklist versionnée. Publication lie la version vérifiée. |
| Demandes EPIC 56 existantes | Ajouter révision/snapshot de missions du commerce, identifiant de mission choisie, confirmations par ID et empreinte des engagements. Unicité de la demande courante par animation/commerce conservée, sans interdire les cycles historiques ; décisions auditables et historique des révisions. |
| Population de tirage existante | Compléter le snapshot de clôture par configuration/contrat moteur/révision exploitation et références de preuves nécessaires. L’appartenance figée ne dépend plus du détail des essais. |

Un scan commerçant conserve une `ValidationAnimation` authentifiée, avec statut effectif/annulé et historique. Conserver l’unicité partielle d’une validation `VALIDEE` par participant/étape et l’unicité commerçant/clé existantes ; le domaine impose en plus une seule étape par commerce. Une régularisation crée une nouvelle preuve effective liée à celle annulée, sans effacer l’annulation ni attribuer un second effet.

### 4.2 Génération, prompts, templates et quota

| Table / responsabilité cible | Clés et index |
| --- | --- |
| Opérations existantes | Nouveau `type_operation=GENERATION_TEMPLATE`, `resource_type=ANIMATION`, `resource_id` = brouillon dès création. Ajouter `version`, `phase_attempts`, `lease_owner`, `lease_until`, `claim_version`, références prompt/tentative acceptée, opérateur affecté. Le statut de demande est celui de cette opération uniquement. |
| `animation_generation_prompts` | PK UUID, FK opération, UNIQUE `(operation_id,revision)` ; messages exacts, contexte, schéma, paramètres, versions et empreinte. Index `(operation_id,created_at)` ; brut immutable hors purge autorisée. |
| `animation_generation_reponses` | PK UUID, FK prompt, numéro de tentative, brut, empreinte, rapport de validation, auteur/date, provenance manuelle ; UNIQUE `(prompt_id,numero)` et `(prompt_id,sha256)` pour dédupliquer un même dépôt. Une correction crée une nouvelle tentative. |
| `animation_templates` / `animation_template_versions` | Identité de bibliothèque et versions immuables du contenu réutilisable, partenaire/type/contrat, source prompt/réponse ; UNIQUE `(template_id,version)`. Références explicites depuis configurations. Pas de données personnelles de participants. |
| `animation_quotas_generation` | PK `(partenaire_id,mois_paris)` ; plafond de période et auteur/date de modification. Aucune colonne « solde restant ». Paramètre partenaire pour les prochains mois ; snapshots des mois passés conservés. |
| `animation_usages_generation` | PK/FK `operation_id`, partenaire/mois d’origine, état `RESERVEE|CONSOMMEE|LIBEREE`, dates ; index `(partenaire_id,mois_paris,etat)`. Une ligne d’état effectif par demande, événements de transition dans l’audit. |

Création : sous verrou partenaire/quota, réserver et créer/rattacher le brouillon + opération + usage dans une seule transaction. Une demande indépendante peut viser le même brouillon ; elle a son quota propre et une version source. Sa finalisation exige que cette version soit encore courante. Il n’y a donc pas d’unicité « une seule demande pour toujours par animation » ; l’unicité garantit un brouillon par demande et un seul résultat appliqué par demande.

Mois calculé en `Europe/Paris` à la réservation, stocké comme premier jour civil du mois ; dates techniques en UTC. `disponible=max(0,plafond-count(CONSOMMEE)-count(RESERVEE))`. Un changement de plafond verrouille le partenaire puis les mois concernés dans l’ordre, modifie le mois courant et la valeur par défaut future, sans réécrire les périodes passées. Une demande acceptée le mois suivant consomme son mois d’origine. Ni attente prolongée, ni échec d’image, ni purge ne libère une réservation.

### 4.3 Machine d’état de génération

Étendre `StatutOperationAnimation` pour `GENERATION_TEMPLATE` avec les phases suivantes ; les anciens types gardent leur cycle actuel. Les serializers, compteurs ERP et prédicats `terminee` dispatchent par famille d’opération ; le dictionnaire de libellés actuel doit être mis à jour dans le même lot.

| Statut cible | Entrée / sortie autorisée |
| --- | --- |
| `PREPARATION_PROMPT` | Worker prépare les messages/schéma puis persiste une révision et passe en attente. Erreur technique : reprises bornées §8.1, puis `ECHEC_PREPARATION` si épuisées. |
| `ATTENTE_TRAITEMENT_MANUEL` | Export autorisé ; aucun worker ni délai d’expiration actif. Dépôt → `RESULTAT_DEPOSE`. |
| `RESULTAT_DEPOSE` | Worker contrôle la tentative courante → `RESULTAT_INVALIDE` ou `A_VALIDER`. Erreur technique : reprises bornées, puis `ECHEC_CONTROLE`, sans confondre panne et contenu invalide. |
| `RESULTAT_INVALIDE` | Erreurs localisées ; nouveau dépôt ou nouvelle révision de prompt, même réservation. |
| `A_VALIDER` | Relecture de la tentative exacte ; acceptation explicite → `RESULTAT_PUBLIE`. |
| `RESULTAT_PUBLIE` | Transaction d’acceptation : tentative figée + usage `CONSOMMEE` + reprise durable. Worker → `FINALISATION_INSTANCE`. |
| `FINALISATION_INSTANCE` | Compléter le même brouillon avec la préparation et la provenance → `TERMINEE`; échec → `ECHEC_FINALISATION`. Pas d’assemblage de missions non encore choisies en parcours public. |
| `ECHEC_FINALISATION` | Reprendre le résultat accepté sans nouvel appel ni décompte. Un conflit de contenu exige une résolution explicite, jamais l’écrasement du brouillon courant. |
| `ECHEC_PREPARATION` / `ECHEC_CONTROLE` | Non terminaux ; reprise explicite vers la phase correspondante sur la même demande, ou annulation. Aucune libération automatique du quota ni démarrage du délai de purge. |
| `OBSOLETE` | Aucun résultat applicable ; nouvelle révision de prompt explicite autorisée si non consommée, ou annulation. La réservation reste active tant qu’il n’y a ni acceptation ni annulation. |
| `ANNULEE` / `TERMINEE` | Terminaux. Annuler libère seulement une réservation non consommée. L’annulation ne supprime pas le brouillon ni le résultat accepté. |

Un nouveau dépôt n’écrase pas une tentative acceptée. L’acceptation compare `operation.version`, le prompt courant, `request_hash`, la tentative relue et la révision source. Une acceptation concurrente avec annulation a exactement un gagnant. Le contrôle hors transaction produit un rapport lié à ses empreintes ; la transaction d’acceptation revérifie qu’aucune dépendance n’a changé.

Empreintes documentaires : SHA-256 du JSON UTF-8 canonisé côté backend (`sort_keys=True`, séparateurs compacts, `ensure_ascii=False`, `allow_nan=False`) après conversion explicite des UUID/dates en chaînes. Conserver les octets exportés ; le navigateur ne reconstruit pas sa propre empreinte à partir d’un JSON reformaté. La réponse brute est conservée séparément du résultat normalisé.

## 5. Protocole transactionnel, idempotence et reprise

### 5.1 Ordre des verrous

Utiliser les transactions SQLAlchemy/PostgreSQL existantes, en isolation `READ COMMITTED` avec verrous explicites. Une transaction métier ne comporte aucun appel réseau, décodage d’image ou envoi de notification. Après acquisition d’un verrou, recharger les faits avec `populate_existing`/requête fraîche : un objet de l’identity map lu avant l’attente ne fait pas autorité.

Ordre total à respecter dans API, ERP, worker et batch :

1. Portée d’idempotence `(acteur stable, opération canonique, ressource, clé)` ; adapter le verrou transactionnel existant et sa contrainte unique. Pour toutes les commandes joueur, famille unique `COMMANDES_PARTICIPATION`, ressource = UUID de participation, action dans l’empreinte seulement : le GET par clé est ainsi non ambigu. Encoder famille/ressource dans la colonne `route` existante, sans la confondre avec l’URL du proxy.
2. Partenaire puis périodes de quota concernées, triées par `(partenaire_id,mois)` si la commande touche la génération ; utiliser le même ordre pour création de période et changement de plafond.
3. `animation_coordinations`, UUID triés : **`FOR SHARE` pour les commandes individuelles, `FOR UPDATE` pour les mutations globales**.
4. Ligne `Animation` si elle doit être modifiée ; aucun incrément de cette ligne à chaque réponse joueur.
5. Participants puis exécutions concernés, UUID triés, **`FOR UPDATE`** pour les écritures individuelles.
6. Demandes commerçantes, validations, opérations, artefacts parents : ordre fixe par famille puis UUID. Références de dépendance/gels sous le verrou de leur artefact parent.
7. Écritures enfants, reçu idempotent, audit et outbox ; un commit unique.

Interdire les upgrades partagé → exclusif et les acquisitions inverses. Déterminer le mode de coordination avant le premier verrou. Les recherches d’identifiants préalables sont possibles sans mutation ; relire les faits ensuite. Le claim d’un worker se termine avant la transaction métier et ne garde pas son verrou d’opération en prenant une coordination.

| Action | Coordination et effet |
| --- | --- |
| Réponse, aide, QR de lieu, attestation/régularisation commerçante | Animation partagée + participation exclusive. Deux participations différentes avancent simultanément ; deux appareils d’une même participation se sérialisent. |
| Inscription / suppression autorisée de participation | Animation exclusive, recomptage de capacité et contrôle de l’inscription existante. Le rejeu/reprise retrouve l’identité existante avant de tester une nouvelle place. |
| Retouche de préparation, décision EPIC 56, publication, modification d’exploitation, retrait global, annulation | Animation exclusive. Les décisions restent atomiques avec la révision et les dépendances qui justifient l’action. |
| Clôture / tirage | Animation exclusive ; clôture requalifie et fige, tirage lit uniquement le snapshot figé. |
| Purge d’un artefact | Verrou de son opération si concernée, puis parent d’artefact ; jamais acquisition ultérieure de la coordination animation. Les commandes créant une dépendance respectent le même ordre et verrouillent ce parent. |

La barrière doit remplacer les prises de verrou incompatibles dans `validations_animation`, `participants_animation`, `tirages_animation`, `gestion_animations`, `publication_animation`, `synchronisation_statuts_animation` et toutes les décisions/retraits EPIC 56. Un ancien chemin ERP ou batch qui écrit sans cette barrière invalide la garantie ; sa migration est un critère de livraison du socle, pas une amélioration ultérieure.

### 5.2 Contrat de commande

`POST /public/localeo-live/participations/{id}/commandes` : Bearer personnel existant, `Idempotency-Key` UUID opaque (validation commune 8–128 caractères). Corps fermé :

```json
{
  "engineContractVersion": "1.0",
  "definitionVersion": 3,
  "expectedProgressionVersion": 7,
  "expectedExploitationRevision": 2,
  "action": "SUBMIT_ANSWER",
  "payload": {"stepId": "22222222-2222-4222-8222-222222222222", "answer": {"type": "SINGLE_CHOICE", "choiceId": "choix-opaque"}}
}
```

L’identifiant d’acteur vient de l’accès authentifié, jamais du corps. Pour le joueur, acteur stable = participation, indépendant de la rotation du token ; pour le commerçant/ERP, identité authentifiée. L’empreinte inclut ressource, action, versions et payload normalisé, mais aucun header d’accès. Réordonner les paires d’association pour l’empreinte ; conserver l’ordre pour `ORDERING`. Pour une saisie, appliquer le profil `TEXTE`/`CODE` de la définition immuable visée, sans contrôle d’état courant avant recherche du reçu. Pour le QR, hacher le token exact dans la préimage éphémère, sans conserver ni journaliser ce token ; résoudre/contrôler activation et révocation seulement pour une commande nouvelle. Un rejeu exact reste donc possible après rotation/révocation du QR initial, sous réserve de l’accès personnel courant.

| Action | Payload fermé et effet |
| --- | --- |
| `START_GAME` | `{}` ; initialise le début de jeu, uniquement dans la période et pour l’inscrit. GET reste une lecture. |
| `SCAN_QR` | `{stepId,qrToken}` ; preuve d’accès au lieu de l’étape atteignable, jamais attestation commerçante. |
| `SUBMIT_ANSWER` | `{stepId,answer}` ; union discriminée : `choiceId`, `pairs:[{leftId,rightId}]`, `orderedIds`, ou `text` selon le défi. Contrat des bornes/normalisations en §4.6.3 de la spécification. |
| `CONTINUE` | `{stepId}` ; confirme un contenu INFORMATION, sans remplacer les autres conditions. |
| `REQUEST_HINT` | `{stepId}` ; indice après une première mauvaise réponse valide. |
| `REQUEST_HELP` | `{stepId}` ; résolution avec aide après première erreur, sans pénalité ni preuve fictive. |

La progression vers le successeur est calculée quand toutes les conditions sont réunies. Le bouton de maquette `NEXT` est une transition d’affichage du résultat, pas une permission de débloquer une étape. `RECONCILE` devient la lecture du reçu puis de la participation. `MERCHANT_PROOF` reste une simulation : la production utilise la route d’attestation authentifiée. Aucune commande joueur `CONFIRM_INTERACTION` ne crée une preuve.

Succès HTTP 200 : `{commandId,outcome,stepId,progressionVersion,exploitationRevision,replayed,correlationId}` (`stepId` nul pour START_GAME). `outcome` est fermé (`STARTED`, `PLACE_VALIDATED`, `ANSWER_CORRECT`, `ANSWER_INCORRECT`, `CONTENT_CONFIRMED`, `HINT_OPENED`, `HELP_APPLIED`, `ALREADY_APPLIED`) avec le résultat minimal approprié. Le reçu ne conserve ni solution complète, ni média, ni projection privée à rejouer plus tard. Après un reçu, le client relit la participation et son `dernierResultat` serveur ; il ne régresse jamais vers une version plus ancienne. Les aides déjà demandées restent consultables pour l’étape concernée selon §6.3, même si son achèvement a immédiatement débloqué la suivante.

Une mauvaise réponse est un 200 traité, avec une tentative et une nouvelle version ; un payload invalide est un 422 sans tentative ni ouverture d’aide. Les refus métier après normalisation peuvent avoir un reçu de refus avec leur code stable, sans effet métier. Authentification invalide, JSON illisible et payload structurellement invalide ne réservent pas de clé durable.

### 5.3 Algorithme atomique et résultats incertains

Après authentification et validation de structure :

1. Ouvrir la transaction, verrouiller la portée idempotente. Si un reçu existe, même empreinte → résultat initial sans mutation ; autre empreinte → 409. Recontrôler l’accès avant toute restitution.
2. Prendre la coordination et la participation dans l’ordre défini, relire définition/état/preuves. Comparer les versions et lire l’heure serveur **après l’attente des verrous**. À `endsAt` ou après, une nouvelle action de jeu est refusée même si elle est partie du téléphone avant.
3. Réconcilier la progression avec la révision d’exploitation, faire décider le domaine. Persister une seule fois essais, preuve/effets, qualification, version, reçu, audit et intentions d’envoi.
4. Commit ; l’envoi des emails/push reste asynchrone. Une panne HTTP après commit est récupérable par le reçu. Un rollback ne laisse ni tentative, ni chance, ni reçu de succès.

Conserver les reçus des commandes de participation jusqu’à l’expiration de l’accès (fin + 90 jours), sans réponses brutes. Pour les opérations de génération, conserver les métadonnées de rejouabilité tant que la demande est active ou son résultat utile, puis selon la politique de ses preuves ; la purge du brut n’efface pas les contraintes d’unicité métier. Les heures/durées de conservation ne se prolongent pas à chaque consultation.

`GET …/commandes/{cle}` prend brièvement le verrou de la même portée avant de conclure : reçu → 200 ; commande transactionnelle encore en cours → 202 `EN_COURS`; absence constatée après verrou → 404 `COMMANDE_NON_ENREGISTREE`. L’absence ne prouve pas qu’un ancien paquet réseau ne peut plus arriver. La nouvelle soumission **explicite** réutilise donc la même clé et le même contenu si la commande reste identique ; après changement de contenu/version, elle emploie une nouvelle clé et le contrôle de version empêche deux mutations concurrentes sur l’ancien état. Aucun POST de reprise automatique.

Si la lecture elle-même échoue, rester en état « validation non confirmée ». Ne jamais afficher une bonne réponse, une preuve ou une étape acquise sur le seul état local. Des réponses HTTP arrivées dans le désordre sont comparées par versions de progression/exploitation ; les anciennes sont ignorées pour l’affichage courant.

### 5.4 Retrait, correction et gel

La neutralisation est une décision globale persistée sous verrou exclusif, avec aperçu d’impact, motif, empreinte de l’aperçu et révision attendue. Recalculer le retrait sur l’ensemble des étapes encore requises ; refuser la suppression de la dernière. Une décision périmée exige un nouvel aperçu. Aucun basculement vers la deuxième mission après publication.

La réconciliation avec les retraits est déterministe : donner les objets indispensables seulement à l’arrivée à la position retirée (immédiatement pour un participant déjà arrivé/passé), sans doublon ni révélation future. Les lectures construisent l’état effectif sur la révision courante ; les écritures matérialisent les effets sous verrou participant. Une qualification stockée sur une ancienne révision n’est jamais utilisée seule par les métriques, l’ERP ou la clôture. Pas de transaction de retrait qui verrouille tous les participants en sens inverse.

Une correction de preuve avant clôture retire la qualification si nécessaire, mais conserve défis résolus, objets et progression. Le scan de régularisation cible une étape déjà atteinte et sa preuve annulée. Après gel, seule une anomalie séparée est enregistrée : aucune mutation du snapshot, nouvelle chance ou réouverture.

La clôture prend la barrière exclusive après les commandes individuelles déjà engagées, relit l’heure et les obligations de la révision courante, recalcule les qualifications puis fige la population et sa provenance dans une transaction. Un seul snapshot par clôture/version, protégé par unicité. Le tirage existant lit ce snapshot, pas un recalcul des essais. Tester charge et durée sur PostgreSQL avant ouverture ; si la transaction échoue, aucun gel partiel n’est rendu visible et aucune notification de clôture n’est envoyée.

## 6. API, habilitations et projections

### 6.1 Routes existantes et extensions

Les chemins ci-dessous sont ceux du backend ; `/api` reste un préfixe éventuel de proxy frontend. Les alias exploratoires `/api/live/game-sessions` de la spécification ne créent pas de second circuit.

| Route | Statut et contrat cible |
| --- | --- |
| `GET /public/animation-locale/animations` et `/{id}` | Existantes ; builder public par type, chasse sans liste de lieux. |
| `POST /public/animation-locale/animations/{id}/inscriptions` et `/inscriptions/renvoyer-lien` | Existantes ; même participant/circuit de récupération. Ajouter déclaration adulte explicite de chasse et référence du règlement accepté. |
| `GET /public/localeo-live/participations/{id}` et `/{id}/qrcode` | Existantes ; Bearer personnel correspondant exactement à l’ID. Le secret d’installation Live ne donne pas ce droit. |
| `POST /public/localeo-live/participations/{id}/commandes`, `GET …/commandes/{cle}` | Nouvelles ; §5, sans nouvelle identité de session de jeu. |
| `GET /public/localeo-live/participations/{id}/etapes/{step_id}/resultat` | Nouvelle ; résultat déjà atteint et contenus explicitement ouverts à cette participation, sans nouvelle aide ni exposition d’une étape future. |
| `POST /protected/animation-locale/commercants/me/participants/resoudre` | Existante ; uniquement l’étape attestable par ce commerce ou une régularisation autorisée. Aucun parcours futur. |
| `POST /protected/animation-locale/validations` | Existante ; seule entrée d’attestation commerçante, raccordée au moteur et au protocole commun. |
| `/protected/animation-locale/animations/{id}/configuration` et `/validation-publication` | Existantes ; contrat versionné et contrôles communs, pas de PUT direct sur le DSL publié. |
| `POST /protected/animation-locale/animations/{id}/generations` | Nouvelle ; demande sur brouillon existant. `POST /protected/animation-locale/generations` couvre création atomique d’un brouillon et de sa première demande. Réponse 202 avec liens opération/animation. |
| `GET /protected/animation-locale/operations/{id}` | Existante ; état de génération, versions, prochaine action autorisée, erreurs et lien vers le même brouillon. |
| Sous `/protected/animation-locale/operations/{id}` | Nouvelles : `GET /prompts/{prompt_id}/export?format=json|texte`, `POST /reponses`, `POST /reponses/{reponse_id}/accepter`, `POST /reviser-prompt`, `/reprendre`, `/annuler`, `/affectation`. |
| Sous `/protected/animation-locale/animations/{id}/etapes/{step_id}` | Nouvelles : `POST /neutralisation/apercu` sans mutation, `POST /neutralisation` avec motif/empreinte d’aperçu/versions attendues. |
| Routes EPIC 56 de demandes de participation | Existantes ; acceptation Chasse enrichie, autres types inchangés. |

Les mutations de préparation/opération/neutralisation portent `expectedVersion` (version de leur agrégat), plus les révisions de contexte utilisées, et la clé idempotente. L’acceptation d’un résultat référence exactement la tentative prévisualisée. Les nouvelles listes de génération/exploitation sont paginées par curseur stable `(created_at,id)`, `limit=50`, maximum 100 ; filtres autorisés par partenaire, commune, type, phase, opérateur et ancienneté. Les listes existantes, notamment EPIC 56 en `page/page_size`, conservent leur contrat. Aucun brut/base64 dans les listes.

Le formulaire ERP utilise les mêmes use cases et politiques d’autorisation ; ses handlers SQLAdmin ne modifient pas directement les statuts. L’ERP peut être une entrée autorisée d’une création initiale sans ouvrir une seconde API métier à comportement divergent.

### 6.2 Droits par action

Réutiliser sessions/CSRF de Localeo Animation, session ERP et Bearer commerçant. Conserver les permissions existantes `animation:lire`, `creer`, `modifier`, `publier`, `cloturer`, `tirer`, `exporter`, `gerer_participations_commercants`. Toute décision vérifie partenaire propriétaire, commune autorisée et ressource ; hors périmètre → 404 suivant la convention existante.

| Permission cible supplémentaire | Attribution dans les profils et portée |
| --- | --- |
| `animation:generer` | Organisateur habilité à créer/modifier, dans ses communes ; permet initier/réviser/annuler une demande non acceptée. |
| `animation:generation_lire` | Organisateur de l’animation et opérateur de traitement autorisé ; détail et export privé du prompt/résultat. |
| `animation:generation_deposer` | Profil opérateur de génération ; dépôt/correction. |
| `animation:generation_accepter` | Profil opérateur de génération habilité ; accepter/reprendre. Distinct de `animation:publier`, cumul autorisé sans second approbateur imposé. |
| `animation:neutraliser_etape` | Profil organisateur exploitant et support ERP habilité, sur leur périmètre ; aperçu + application. |
| `animation:regulariser_preuve` | Support ERP habilité pour correction/anomalie ; les nouvelles attestations restent soumises aux droits commerçants existants. |
| `animation:quota_generation_modifier` | Administration ERP uniquement ; cible partenaire explicite, motif obligatoire. Aucun droit implicite pour le partenaire lui-même. |
| `animation:exploitation_lire` | Exploitant ERP pour rapports de traitements/purge ; filtrage de périmètre. |

Les profils sont des regroupements de permissions existantes et nouvelles, attribués via les mécanismes d’habilitation actuels. Une migration ne donne pas automatiquement un droit de publication/régularisation à tous les lecteurs. Le commerçant utilise `commercant:animation` pour décider et `commercant:validation` pour attester, sur son commerce uniquement.

L’adaptateur applicatif `ContexteAutoriseAnimation` unifie identité, permissions, partenaire cible, communes autorisées et corrélation. Il est construit depuis la session Animation ou depuis `contexte_erp`, jamais depuis les champs du corps. La session ERP expose actuellement `ADMIN`/`EXPLOITATION` et non un `ContexteAnimation` : appliquer la traduction explicite suivante pour les **nouveaux** droits, en conservant le comportement des droits existants.

| Source d’habilitation | Attribution initiale des nouvelles permissions | Périmètre |
| --- | --- | --- |
| Session Animation avec `creer` et `modifier` | `generer`, `generation_lire` ; les lecteurs simples n’acquièrent ni dépôt ni acceptation. | Partenaire de session et communes habilitées, dont la commune active. |
| Profil Animation exploitant, attribué explicitement | Ajoute `neutraliser_etape` au profil organisateur. Aucune déduction depuis le seul droit `lire`. | Même périmètre Animation. |
| ERP `ADMIN` | Toutes les nouvelles permissions du tableau, par table de traduction explicite. | Portée globale déjà autorisée ; partenaire/animation cible explicites et cohérents. |
| ERP `EXPLOITATION` | `generation_lire`, `generation_deposer`, `generation_accepter`, `exploitation_lire`. Ni changement de quota, ni correction de preuve, ni neutralisation accordés implicitement. | Seulement `commune_ids` de la session ; un ensemble vide n’est pas global. Résolution du partenaire depuis la ressource autorisée. |

Les handlers ERP conservent `verifier_csrf` (`X-CSRF-Token`) ; ils n’usurpent pas une session partenaire pour appeler une route protégée. L’acteur ERP d’audit reste `admin:<admin_username>` vérifié ; pour la colonne UUID d’idempotence existante, dériver un UUIDv5 stable avec `NAMESPACE_URL` et `localeo:erp:<admin_username>` normalisé comme la session. Aucun UUID aléatoire par requête, aucun username fourni librement. Les autres acteurs gardent leurs identifiants existants ; tester séparément chaque adaptation de contexte.

Acceptation Chasse : corps fermé `{expectedVersion,presentedRevision,presentedHash,missionId,confirmedRequirementIds[]}`. Toutes et seulement les conditions de la mission choisie sont confirmées ; refuser IDs étrangers, doublons, deux choix, date dépassée et version périmée. Comparer une empreinte des engagements **par commerce**, incluant les dépendances communes pertinentes (dates/règlement). Une retouche propre à A n’invalide pas B. L’acceptation atteste la capacité à préparer ; la checklist avant publication atteste la préparation vérifiée.

### 6.3 Projections et UI

| Audience | Champs autorisés / interdits |
| --- | --- |
| Public | Identité, type/version, titre, période, présentation/thème de couverture relus, durée/difficulté/public, nombre d’étapes, inscription et gains publics autorisés. Pour la chasse : aucun commerce/POI futur, coordonnée, solution ou préparatif. |
| Participant | Identité de sa participation, versions, statut, progression/objets autorisés, étape courante, actions permises, preuves à régulariser déjà connues. Lieu courant nommé/adressé dès déblocage ; défi, illustration d’étape et aides uniquement après leurs conditions d’accès. Futur = compteur, sans tableau détaillé. |
| Commerçant | Sa demande et ses alternatives privées avant choix ; mission retenue et consignes/supports après stabilisation ; participant minimal et action d’attestation autorisée. Aucun contenu des autres commerces ni destination suivante. |
| Organisateur / ERP | Préparation complète, variantes, solutions et contrôles selon permissions ; le rapport d’audit ne contient pas de copie de ces textes. Aperçu privé explicite. |

Le constructeur participant **Chasse** émet une union d’états `AVANT_DEBUT`, `A_DEMARRER`, `SE_RENDRE_SUR_PLACE`, `DEFI_DISPONIBLE`, `ATTENTE_ATTESTATION`, `ETAPE_TERMINEE`, `REGULARISATION_REQUISE`, `PARCOURS_TERMINE`, `FERME`, avec `allowedActions`. Passeport et Tombola conservent leurs projections et calculs propres. Ces états sont des projections dérivées, pas de nouvelles sources de statut commercial. Pour chaque état, les champs de contenu absents sont réellement omis ; un `null` ne masque pas un objet déjà sérialisé.

`currentStep` contient au plus `{id,title,roles,location,content,playerInteraction,challenge,presentation,proofState}` selon l’accès. `content` énumère `introduction`, `instruction`, `information`, `accessibleAlternative`, `hint` et `resolutionHelp` selon les droits acquis ; `playerInteraction` exclut la consigne commerçante. `challenge` exclut le bloc de correction. `presentation` est le thème résolu et les médias accessibles, sans `promptGeneration`. Après première erreur, l’action d’indice/aide devient disponible ; son texte n’est transmis qu’après la demande correspondante.

Les exécutions d’étape conservent la provenance du résultat et les dates d’ouverture de l’indice/aide. La projection `dernierResultat:{stepId,outcome,successMessage,hint,resolutionHelp,grantedObjects}` reconstruit les champs autorisés depuis cette exécution et la définition jouée ; le même résultat est consultable par la route d’étape ci-dessus. Cela permet d’expliquer une résolution aidée après progression automatique, y compris au rafraîchissement. Les solutions non demandées, consignes privées et autres étapes restent absentes. L’historique détaillé est chargé à la demande, jamais préchargé dans son entier.

Le carnet IndexedDB conserve ses accès/résumés actuels, pas la projection narrative complète dans `detail`. `sessionStorage` conserve uniquement la saisie et le descripteur minimal de commande incertaine, clé `(participation,definitionVersion,stepId)`, expiration **24 heures après la dernière édition**, sans prolongation par simple lecture. Retirer après validation confirmée, obsolescence ou expiration. Pas de token, réponse serveur, solution ou base64 ajouté à ce stockage. Si indisponible : repli mémoire et information sur la perte possible au rafraîchissement. Une commande incertaine ne devient jamais automatiquement un échec à l’expiration du brouillon : relecture serveur obligatoire.

API privée : `Cache-Control: no-store`; pas de préchargement des étapes futures. Le service worker conserve seulement ses ressources publiques autorisées. Images base64 converties en Blob en mémoire puis URL objet révoquée au changement d’écran ; pas de stockage de média de jeu dans IndexedDB. Clavier/lecteur d’écran pour associer et réordonner, textes alternatifs disponibles avec leur contenu. Aucun GPS requis ; le lien cartographique externe contient seulement la destination actuellement autorisée.

### 6.4 Erreurs

Conserver `ApiErrorResponse` (`code`, `detail`, `correlationId`, alias historique `request_id`). Ajouter des violations structurées facultatives `{path,code,message}` sans valeur d’entrée. La liste n’inclut ni bonne réponse, token, texte brut de prompt ni base64.

| HTTP / code stable cible | Traitement UI |
| --- | --- |
| 401 / 410 accès absent ou expiré | Circuit de récupération existant ; aucune inscription supplémentaire implicite. |
| 403 permission insuffisante / 404 hors périmètre | Action indisponible ; pas d’information sur une autre participation. |
| 409 `IDEMPOTENCY_CONFLICT` | Même clé, autre empreinte ; pas de mutation. |
| 409 `VERSION_OBSOLETE`, `CONTEXTE_OBSOLETE` | Relire l’état / refaire l’aperçu ; aucune fusion silencieuse. |
| 409 `ETAPE_HORS_ORDRE`, `ACTION_INDISPONIBLE`, `ANIMATION_FERMEE` | Afficher le contexte courant autorisé, jamais la prochaine solution. |
| 422 `REPONSE_INVALIDE`, `MEDIA_INVALIDE`, `DEFINITION_INVALIDE` | Erreurs localisées ; pas de tentative joueur pour un payload invalide. |
| 413 `DOCUMENT_TROP_VOLUMINEUX` | Taille reçue/plafond technique, sans corps recopié. |
| 429 | Limiteur existant, `Retry-After`; pas de retry d’écriture automatique. |
| 503 `TRANSACTION_INDISPONIBLE` | Verrou/traitement indisponible ; réconciliation si résultat HTTP incertain. |

## 7. Médias, validation et budgets

### 7.1 Résultat autonome et stockage privé

Le contrat d’échange conserve **toutes les illustrations candidates en `medias[].base64` dans le JSON final**, avant choix des commerçants. L’adaptateur textuel dérive le sous-contrat éditorial sans octets ; l’exécution manuelle outillée produit les images, les encode puis assemble un seul résultat. Le backend V1 importe ce résultat et le contrôle ; il ne simule pas un appel d’image ni un coût fournisseur.

Le JSON brut autonome est conservé comme artefact privé via le stockage documentaire existant (`app/infrastructure/storage/document_storage.py`, derrière un port applicatif dédié). Les prompts/messages sont du texte en base ; les lignes de réponses référencent le brut privé et un contenu éditorial normalisé JSONB. Les WebP décodés peuvent être dédupliqués dans ce même stockage privé, avec une table `animation_medias` (UUID, partenaire, ID logique, SHA-256, format, dimensions, octets, document privé). `animation_references_medias` relie explicitement chaque média à ses versions de réponse/template/configuration. Les octets ne sont pas recopiés dans chaque ligne d’exécution.

L’export autorisé réassemble systématiquement le JSON autonome avec base64 ; cette organisation interne ne remplace pas le contrat demandé par des URL. La projection Live peut embarquer uniquement les médias accessibles sous la même forme. Ne pas enregistrer ces images narratives dans le catalogue public `media_assets` ni les servir via `/public/images` : publier une animation n’autorise pas ses images futures.

Écriture d’artefact : préparer un fichier privé temporaire, vérifier son empreinte, puis enregistrer référence et dépendance en transaction. Un rollback laisse un candidat au nettoyage, jamais un lien publié cassé. Les clés de stockage sont générées côté serveur, sans chemin fourni par le JSON. Déduplication dans le périmètre autorisé ; l’existence d’un hash d’un autre partenaire n’est pas révélée. La lecture/purge vérifie aussi les références utiles du brut et des médias extraits.

### 7.2 Pipeline de contrôle

1. Borner le flux avant chargement JSON, refuser les clés dupliquées, nombres non finis et structure trop profonde. Le body d’import n’est jamais repris dans une erreur ni loggé.
2. Valider le schéma du type/version et les références du brief. Vérifier les limites textuelles avant rendu.
3. Pour chaque média unique : décoder la base64 canonique stricte, contrôler que le réencodage est identique, décoder réellement le WebP statique dans un adaptateur borné. Pas de SVG, WebP animé, fichier tronqué ni simple validation du suffixe.
4. Comparer MIME réel, dimensions autorisées, ratio 16:9, longueur binaire, `octets`, SHA-256, longueur base64 et poids UTF-8 de l’objet compact. Toutes les références, y compris missions non encore sélectionnées, doivent être satisfaites ; aucun orphelin ni ID contradictoire.
5. Faire valider au domaine les références, l’héritage et les règles de présentation à partir du résultat technique de décodage. Le domaine ne dépend pas de Pillow/libwebp. Relecture : lisibilité PC/mobile, fidélité illustrative, absence de solution/lieu futur et cohérence après retouche d’une mission.
6. Produire un rapport immuable lié aux empreintes et à la version des validateurs. Une nouvelle réponse invalide n’efface pas les médias valides précédents. Un résultat incomplet reste non acceptable ; l’opérateur peut réimporter les médias corrigés dans un JSON complet ou retirer explicitement une illustration facultative avec ses références.

L’encodeur de l’outillage descend de 960×540 à 768×432 puis 640×360 en ajustant la qualité ; s’il n’obtient pas une image lisible dans le budget, régénérer/simplifier. Il ne tronque jamais une chaîne base64. La pipeline automatique fournisseur éventuelle réutilisera ces contrôles après le pilote, sans ajouter de réservation de génération par image.

### 7.3 Paramètres techniques initiaux

Ces valeurs fixent des limites d’intégration, configurables côté exploitation et documentées dans les modèles de configuration sans secret. Ce ne sont ni un nombre imposé d’étapes ni de nouveaux quotas commerciaux. Une modification de limite ne modifie pas silencieusement un contenu publié.

| Paramètre / valeur initiale | Application et refus |
| --- | --- |
| Média JSON ≤ **60 000 octets** ; cible 50 000 | Taille compacte UTF-8, métadonnées comprises ; règle contractuelle TRE-ARB-91, non relevée par une simple configuration d’exploitation. |
| WebP ≤ 44 000 octets ; base64 ≤ 58 668 caractères | Un seul visuel par ID, résolution 960×540 / 768×432 / 640×360. |
| Import complet ≤ **8 000 000 octets** | Taille du body décodé, contrôlée au proxy et dans l’API même sans Content-Length ; refuser Content-Encoding compressé pour cet import V1. Ne pas accepter un JSON compact puis exporter un fichier dépassant cette limite sans signalement. |
| Texte éditorial total hors base64 ≤ **512 000 octets UTF-8** | Propositions, variantes, aides et descriptions incluses ; pas de troncature automatique. |
| Chaîne éditoriale ≤ 20 000 caractères ; titre ≤ 200 ; ID local ≤ 64 | Les bornes plus strictes d’une activité, d’une mission EPIC 56 ou du brief restent prioritaires. Profondeur JSON maximum 32. |
| Commande joueur ≤ **16 384 octets** | Contrôle avant parsing ; `TEXT_INPUT` garde sa borne 80 points de code/32 caractères CODE. |
| Lecture Live ≤ **256 000 octets** | Budget d’une projection avec uniquement les images autorisées ; tester avec les textes maximaux. En cas de dépassement détecté en préparation, corriger la présentation plutôt que couper une consigne en jeu. |
| Saisie temporaire : 24 h ; polling opération 2 s puis 5 s | Polling seulement au premier plan, pause si hors ligne ; relecture immédiate au retour. Aucun polling d’écriture. |
| Limiteur : 30 commandes/min/participation ; 5 imports/min/opérateur | Réutiliser `appliquer_rate_limit_public` et le dispositif protégé, en complément des limites existantes ; clé stable, jamais token brut. Paramètres ajustables sur mesures du pilote. |
| Verrous HTTP : attente max 3 s ; traitement SQL ordinaire max 15 s | Retour contrôlé et réconciliation ; pas de retry automatique d’une mutation dont le résultat est inconnu. Clôture/purge sont des opérations suivies avec budgets dédiés, pas une requête Live longue. |
| Contrôle d’un import : budget 30 s ; 2 tâches par worker | CPU/décodage hors transaction. Une saturation conserve une opération visible et reprenable ; aucun succès partiel. |

L’export lisible pour copier un prompt ne compte pas comme un import de résultat. Les transports volumineux restent privés ; les listes et reçus n’embarquent jamais le JSON complet. Les seuils métier de publication et le quota de 10 générations/mois restent séparés de ces protections techniques.

## 8. Exploitation, conservation et bascule

### 8.1 Worker et reprises

Étendre le traitement d’opérations du backend, sans présenter `lister_executables` comme un worker déjà disponible. Claim en transaction courte par `FOR UPDATE SKIP LOCKED`, bail initial 120 s, renouvellement toutes les 30 s si nécessaire et `claim_version` croissante. Maximum deux tâches simultanées par processus. Le verrou SQL de claim est relâché après commit, avant toute prise des verrous métier ; le bail reste actif jusqu’au rattachement/échec. Une annulation ou révision gagne contre un résultat tardif grâce au contrôle du statut/version/claim au rattachement.

Seuls `PREPARATION_PROMPT`, `RESULTAT_DEPOSE`, `RESULTAT_PUBLIE` et `FINALISATION_INSTANCE` sont exécutables automatiquement, **dans tous les cas avec bail absent/expiré et échéance `prochaine_execution_at` atteinte**. Le claim recontrôle atomiquement ces conditions. Les états d’attente humaine, invalidité, validation humaine et obsolescence ne consomment ni thread ni tentative. Les erreurs techniques transitoires conservent la phase et planifient au plus trois reprises par phase avec délais 30 s, 120 s, 600 s ; après épuisement, passer respectivement en `ECHEC_PREPARATION`, `ECHEC_CONTROLE` ou `ECHEC_FINALISATION`, puis reprise explicite. Ces échecs ne terminent pas la demande pour conservation/quota. Une erreur de contenu n’est pas un échec réseau à retenter. Les compteurs de tentative sont techniques par phase ; le quota métier reste attaché à la demande.

La file ERP est **Animations → Demandes de création**, liste filtrée et fiche. Afficher état métier, bail/tentative technique si erreur, opérateur affecté, ancienneté, prochaine action autorisée, mois de réservation, brouillon lié, révisions et rapports. « Publier le résultat » montre la tentative exacte et reste distinct de « Publier l’animation ». Le dépassement de délai d’une attente humaine est un indicateur, jamais une annulation automatique.

Audit commun (`evenements_audit`) : catégories `ANIMATION_GENERATION`, `ANIMATION_MISSION`, `ANIMATION_JEU`, `ANIMATION_PREUVE`, `ANIMATION_NEUTRALISATION`, `ANIMATION_QUALIFICATION`, `ANIMATION_PURGE`, `ANIMATION_CONVERSION`. Enregistrer acteur, périmètre, ressource, action, résultat, date serveur, versions avant/après, ID de commande/opération et `correlationId`. Aucun token, QR brut, réponse brute, prompt ou base64 dans l’audit. Réutiliser les outbox emails/webpush pour les notifications, écrites dans la transaction d’origine.

Métriques issues des faits persistés : inscriptions uniques, débuts/fins de parcours, passages actuellement `VALIDEE`, aides, tentatives, neutralisations, erreurs, durée et files bloquées. Historique des annulations et anomalies après clôture séparés des passages valides. Agrégats calculés en requête V1, sans table de solde/compteur métier concurrente ; toute optimisation future reste reconstruisible.

### 8.2 Conservation et purge

Conserver les politiques existantes participants/notifications (12 mois selon registre), tokens (fin + 90 jours), preuves de tirage/gain et archives. Le code actuel utilise notamment 365 jours pour l’usage nominatif ; son alignement calendaire avec le registre doit être vérifié dans le lot conservation sans le remplacer par les nouvelles durées de jeu.

Pour les catégories nouvelles, une « journée » de délai technique représente 24 h après l’instant UTC persisté : `terminated_at + 30 days` pour un brut de génération devenu inutile ; `animation.ends_at + 90 days` pour le détail des essais. Une prolongation autorisée de fin recalcule l’échéance des essais ; l’heure du navigateur et la dernière consultation n’interviennent pas.

Ajouter `animation_gels_conservation` (cible précise, motif, auteur, dates/levée), les liens de dépendance utiles, et `animation_purge_runs`/`animation_purge_items` (politique, catégorie, curseur, résultat par item, compteurs, erreurs). Les seules métadonnées ne constituent pas une autorisation d’effacer les preuves conservées ; qualifier chaque catégorie.

Traitement quotidien à **03:30 UTC**, lot initial **100 objets**, transactions par objet ou petit groupe homogène, reprise par `(eligible_at,id)`. Une exécution quotidienne est elle-même identifiée de façon unique par politique/date/catégorie ; le mécanisme d’exploitation empêche deux propriétaires actifs sur le même lot.

1. Sélectionner des candidats, sans considérer une demande en attente/invalide/reprise comme terminée.
2. Verrouiller l’opération si pertinente puis chaque parent d’artefact dans l’ordre §5.1. Relire échéance, état, références de template/configuration, gels et usages probatoires. Une commande réutilisant un contenu ou posant un gel doit prendre ce même verrou avant son lien.
3. Si protégé : compter une exclusion motivée et reconsidérer à une prochaine exécution. Sinon marquer `PURGE_EN_COURS` sur l’artefact et écrire l’intention de suppression dans la transaction. Ce marquage est le point de non-retour : toute nouvelle référence **ou pose de gel** sur ce contenu est refusée explicitement (« purge déjà engagée »). Un gel accepté avant le marquage interdit celui-ci ; aucun gel accepté ne peut être ignoré par une suppression externe.
4. Pour le stockage externe, supprimer hors transaction puis enregistrer `PURGE` ; « déjà absent » est un succès idempotent. Une panne conserve la tâche et le marqueur, jamais un faux succès. Retirer les copies actives/export temporaires gérés du même périmètre.
5. Conserver les métadonnées minimales nécessaires et le rapport sans brut ; supprimer les essais indépendamment des reçus minimaux/preuves/qualifications. Aucun effet sur le quota ou la population figée. Les sauvegardes suivent leur rotation et une restauration réapplique les suppressions dues.

Rapport ERP : identifiant/politique, heures, catégories, examinés/supprimés/exclus/erreurs, motifs et prochain curseur. Alerte d’exploitation sur échec ou exécution quotidienne absente, sans données brutes. Mode simulation avant activation. Mettre à jour le registre interne et éprouver ces traitements avant livraison ; ce dossier ne modifie ni le PDF juridique ni une base d’exploitation.

### 8.3 Conversion et ouverture

Convertisseur dans le backend, nouvelles migrations SQL seulement via `scripts/database/apply_migrations.py`. Attribuer leur numéro lors de l’implémentation, sans modifier les SQL/checksums historiques.

Ajouter un journal `animation_conversions` : source/configuration, version convertisseur, empreinte source/cible, résultat, dates, erreurs, UNIQUE `(source_configuration_id,converter_version,source_hash)`. Simulation d’abord ; conversion par lots de 50 animations, une transaction par animation, coordination exclusive et contrôle d’empreinte après verrou. Une reprise compare la cible existante ; un changement de source devient un conflit visible, jamais un écrasement.

Conserver IDs, missions, paramètres valides et provenance des brouillons ; signaler tout écart. Aucun appel IA, quota de génération, publication, email, paiement ou tirage pendant la conversion. Inventorier explicitement les données de démonstration sans suppression implicite. Vérifier sur la cible l’absence d’animation publiée avant la bascule ; si ce prérequis déclaré n’est pas vrai, arrêter la procédure et rendre l’écart visible, sans inventer une migration de parties actives.

Ouvrir seulement après conversion complète du périmètre retenu, alignement backend/Animation/Commerçant/Marketplace et recette. Aucun ancien moteur maintenu en parallèle. Un retour technique avant ouverture utilise les sauvegardes et la procédure de déploiement ; il ne supprime pas les traces de conversion. Les modalités de déploiement effectif suivent une demande distincte.

## 9. Lots d’implémentation et preuves de sortie

Le dossier fige les choix techniques ; l’existence des fichiers ne prouve pas les garanties. Livrer les parcours verticalement après un socle minimal, avec tests métier, adaptateurs et consommateurs.

| Lot | Réalisation | Preuves de sortie exigées |
| --- | --- | --- |
| T1 — Socle et contrats | Registre trois types/versions, modèles fermés, exports, clés/versionnage, coordination et reçus atomiques ; raccordement de toutes les écritures existantes. | Domaine sans framework ; type/version inconnu refusé ; diff d’exports contrôlé ; tests PostgreSQL de dernière place et commandes simultanées. |
| T2 — Générer et préparer | Brouillon atomique, quota, opérations/worker, prompts, import complet, médias, ERP et préparation guidée. | Deux réservations pour la dernière place : une seule ; même demande/rejeu : même brouillon ; résultat invalide non acceptable ; attente humaine sans lease active ni expiration ; timeout après acceptation sans seconde consommation. |
| T3 — Confirmer les missions | Alternatives, snapshots propres aux commerces, corps d’acceptation, checklist, assemblage et publication. | A/B indépendants ; deux confirmations concurrentes sur anciennes versions refusées ; minimum et demandes en attente contrôlés ; publication vs décision/retrait déterministe ; une seule mission dans le DSL. |
| T4 — Jouer et reprendre | Inscription commune, trois renderers, cinq défis de chasse, preuves/QR, indices/aides, projections et carnet. | Parcours complets des trois moteurs ; QR POI distinct de preuve commerçante ; aide sans preuve ; absence de lieux/solutions futurs dans tous les canaux ; clavier/mobile ; deux appareils et perte de réponse avant/après commit. |
| T5 — Exploiter et clôturer | Retrait global, correction/régularisation, qualification, gel, tirage existant, audit, métriques. | Retrait de dernière étape refusé ; retrait/réussite sans double objet ; correction/scan/clôture avec résultat cohérent ; pas de modification du snapshot après gel ; panne outbox sans rollback d’un jeu confirmé. |
| T6 — Conserver et ouvrir | Purge, registre interne, conversion, jeux de fixtures, contrôles des dépôts et pilote. | Course purge/réutilisation/gel ; reprise de suppression stockage ; aucune preuve de gain supprimée ; conversion rejouable sans effet externe ; exports frontends alignés ; recette complète avant ouverture. |

### 9.1 Matrice des courses à automatiser

| Course / panne | Assertion observable |
| --- | --- |
| Même clé/même payload, deux requêtes | Un reçu, une tentative au maximum, même résultat métier. |
| Même clé/autre payload | 409, aucun second effet. |
| Deux clés/même version, même participation | Une mutation puis conflit de version ; deux participations distinctes ne se bloquent pas mutuellement sur le jeu. |
| Réponse perdue après commit / lecture de reçu avant arrivée tardive | Réconciliation, puis éventuel nouvel envoi explicite cohérent ; aucun retry silencieux ou double tentative. |
| Dernier scan vs clôture | Seul l’ordre transactionnel décide ; aucune preuve validée après le gel ne modifie sa population. |
| Retrait vs réussite, deux retraits concurrents | Effets uniques, provenance conservée, au moins une étape globalement requise. |
| Dernière place d’inscription / quota génération | Une seule nouvelle inscription/réservation ; récupération d’une identité existante ne prend pas de place. |
| Acceptation résultat vs annulation/révision | Consommation ou libération cohérente ; aucun résultat tardif appliqué. |
| Expiration de lease vs ancien worker | Seul le propriétaire de la version de claim courante peut rattacher son résultat. |
| Purge vs référence utile ou gel | Une référence utile conservée, ou un contenu déjà marqué à purger refusé à la réutilisation ; jamais de référence vers un brut supprimé sans statut explicite. |
| Import image mensonger | Base64, dimensions, poids réel, hash, références ou décodage invalide : refus localisé ; pas de résultat complet fictif. |

### 9.2 Vérifications et limites de ce lot de conception

À exécuter pour ce lot documentaire : contrôle des guides et liens des documents modifiés, sources exportées, relecture des six sujets contre le code, contrôle du diff. Aucun test métier, PostgreSQL, navigateur, import fournisseur ou mesure de charge n’est revendiqué ici.

Dette préexistante identifiée par lecture : `localeo-commercant/api/localeo-openapi.json` attendu par ses consommateurs/tests est absent du workspace. T1/T3 doivent le produire depuis le générateur backend avec les autres contrats embarqués, sans fabriquer une copie divergente. Les helpers HTTP actuels qui lisent/mémorisent l’idempotence dans des UoW séparées doivent être remplacés pour les mutations raccordées au moteur.

Les points encore à vérifier par l’exécution sont les performances du gel/neutralisation, l’absence de deadlocks, les budgets de projection maximaux, la recette accessibilité et la conservation réelle. Les logistiques du pilote (commune, participants, dates), la comparaison fournisseur et le rallye après V1 restent suivis séparément ; ils ne constituent pas des contrats techniques laissés ouverts par ce dossier.

### 9.3 Précisions d’implémentation T1 — 19 septembre 2026

- **T1-D01 — Clés de configuration :** `parametres.preparation_chasse` conserve la préparation ; `parametres.definition_animation` conserve le DSL assemblé. Les colonnes et révisions décrites en section 4 restent leur enveloppe. La capacité provient de `common.registration.maxParticipants`, sans seconde clé concurrente.
- **T1-D02 — Transaction composée :** un service applicatif commun injecte explicitement une factory d’UoW jointe aux services historiques concernés. Leurs commits internes sont différés ; une erreur/annulation interne interdit le commit extérieur. Le reçu idempotent, les effets métier, l’audit et l’outbox sont validés ensemble. Aucune session ambiante, aucune mutation de factory globale, aucun déplacement de règle métier dans une route.
- **T1-D03 — Historique Git :** chaque lot produit un commit dans chaque dépôt effectivement modifié, relié dans le compte rendu central. Les cinq historiques restent indépendants ; aucun commit vide imposé à une application non concernée par un lot.

- **T1-D04 — Noms du DSL des défis :** `ASSOCIATION.leftItems/rightItems`, `validation.expected:[{leftId,rightId}]` ; `ORDERING.items` et `validation.expected` (IDs ordonnés) ; `TEXT_INPUT.normalization` et `validation.expected` (variantes). Les textes d’aide sont `content.hint` et `content.resolutionHelp`. Ce mapping des champs éditoriaux français vers le DSL conserve les règles et normalisations de la section 4.6.3 de la spécification.

### 9.4 Précisions d’implémentation T2 — 19 septembre 2026

- **T2-D01 — Routes complémentaires et reprise :** `GET /protected/animation-locale/generations/quota`, `GET /generations` (filtres et curseur), `GET /generations/commandes/{cle}` complètent la création. Pour les opérations : `GET /operations/{id}/reponses/{reponse_id}/export` réassemble le JSON privé autonome ; `GET /operations/{id}/commandes/{cle}` réconcilie une mutation. La préparation utilise `GET|PUT /animations/{id}/preparation` et `GET /animations/{id}/preparation/commandes/{cle}`. La bibliothèque de lieux utilise `GET|POST /poi`, `PUT /poi/{id}`, `GET /poi/commandes/{cle}` et `GET /poi/{id}/commandes/{cle}`. Ces suffixes partagent le préfixe Animation ci-dessus ; leurs variantes internes ERP réutilisent les mêmes use cases et `contexte_erp`/CSRF. Portées : `GENERATION_CREATE:{partenaire}:{commune}`, `GENERATION_OPERATION:{operation}`, `PREPARATION_ANIMATION:{animation}`, `POI_CREATION:{partenaire}:{commune}`, `POI_ANIMATION:{poi}` ; l’action appartient à l’empreinte. Lecture d’un reçu : 200 `CONFIRMEE`, 202 `EN_COURS`, 404 `COMMANDE_NON_ENREGISTREE`. L’absence ne permet toujours aucun nouvel envoi automatique. Les listes nouvelles utilisent un curseur `(created_at,id)`, 50 éléments par défaut, 100 au maximum.
- **T2-D02 — Édition et parcours organisateur :** intégrer la préparation guidée à la création et à l’onglet configuration existants, dans un composant dédié. Chasse suit ce parcours ; Passeport propose la préparation par génération ; Tombola conserve sa configuration manuelle. Le suivi distingue les phases humaines des anciennes opérations automatiques. L’édition transmet `{expectedVersion,resultat,minimumCommercants}` (minimum obligatoire pour Chasse), pas une préparation arbitraire : UUID stables, liens de provenance et demandes EPIC 56 restent construits côté serveur. Le minimum est opérationnel et ne pollue pas le prompt. Les actions de traitement sont énumérées et filtrées par phase et droits (`EXPORTER_PROMPT`, `EXPORTER_REPONSE`, `DEPOSER_REPONSE`, `ACCEPTER_REPONSE`, `REVISER_PROMPT`, `REPRENDRE`, `ANNULER`, `AFFECTER`).
- **T2-D03 — Parents d’artefacts :** ajouter `animation_generation_artefacts` pour référencer le JSON brut et les documents médias privés, leurs empreintes et leur état `ACTIF|PURGE_EN_COURS|PURGE`. Les réponses/templates/configurations conservent des références explicites ; aucun base64 n’est stocké dans leurs JSONB. `OperationAnimation.generation_context` contient les données privées de la demande et de sa version source ; le statut reste exclusivement celui de l’opération. La création initialise directement le brouillon par les entités/repositories du domaine, après les contrôles d’accès et d’abonnement existants ; elle n’emprunte pas la normalisation des anciens modèles ni n’envoie prématurément les invitations.
- **T2-D04 — Faits de lieux :** la bibliothèque POI conserve une identité partenaire/commune et des éditions immuables `{nom,adresse,faits,responsable}`. Une édition ne vaut jamais vérification pour une chasse ; celle-ci reste distincte en T3. Le modèle commerçant actuel ne comporte pas d’adresse de visite : pour cette édition, l’organisateur renseigne l’adresse et les faits utiles du brief. Le serveur vérifie l’identité autorisée, la commune et le commerçant actif, résout son nom du référentiel puis photographie les compléments avec leur provenance organisateur. Il n’invente pas d’adresse depuis le nom de la commune et n’utilise pas une adresse fiscale. Pour un POI, le snapshot provient de son édition autorisée. Le responsable du POI reste hors du prompt créatif.
- **T2-D05 — Import fidèle :** le navigateur transmet le texte JSON original du fichier dans l’enveloppe d’import, sans parse/sérialisation intermédiaire qui effacerait des clés dupliquées. Le transport commun garde cookies, CSRF et interdiction des retries d’écriture. Le serveur borne le flux avant parsing, refuse les encodages HTTP compressés pour cet import et applique le parseur strict puis les modèles fermés. Toute sortie privée est `no-store` ; les erreurs ne recopient ni valeurs d’entrée ni base64.


- **T2-D06 — Illustrations à la génération :** une nouvelle `InitialisationGeneration` porte `assets:[]` et une couverture nulle. Le résultat importé apporte ses illustrations contrôlées. Cette restriction ne modifie ni le DSL commun ni les templates réutilisés, qui gardent leurs médias privés. Police et couleurs restent configurables.
- **T2-D07 — Bibliothèque de templates :** `GET /templates`, `POST /operations/{id}/templates` et `POST /templates/{version_id}/reutilisations` permettent la sauvegarde explicite d’un résultat accepté et sa réutilisation dans la même commune, sans quota de génération. Ajouter `ENREGISTRER_TEMPLATE` aux actions permises après acceptation. Portées de reçus `TEMPLATE_CREATE:{operation}` et `TEMPLATE_REUSE:{version}` ; lectures sous les mêmes ressources via `/commandes/{cle}`. Le template accepté est immuable ; un brouillon cible existant exige sa version attendue.
- **T2-D08 — Reçus durables :** les commandes de génération, préparation et templates ont `expires_at=NULL` pendant leur utilité, au lieu d’une expiration arbitraire. La conservation T6 calcule l’échéance quand les parents deviennent éligibles, sans supprimer la rejouabilité d’une demande active.
- **T2-D09 — Catalogue et publication :** enregistrer explicitement Chasse dans le catalogue et le registre avec une stratégie de préparation. L’édition n’envoie aucune invitation implicite EPIC 56. La publication est fermée tant que T3 n’a pas assemblé et vérifié la préparation ; aucun repli vers les règles Passeport.
- **T2-D10 — Ordonnancement :** le batch `animations.generer` est planifié chaque minute par l’ordonnanceur existant, avec surcharge cron habituelle, deux tâches au maximum par processus, supervision HTTP de 120 secondes et rattrapage de démarrage après dix minutes. Les phases humaines ne sont jamais revendiquées par ce worker. Les transactions courtes de génération et de bibliothèque appliquent `lock_timeout=3s` et `statement_timeout=15s` ; stockage et décodage restent hors transaction.
- **T2-D11 — Identités de préparation :** au premier import, les UUID sont dérivés du résultat source. Aux éditions suivantes, conserver les positions par identité de lieu et occurrence, les missions par identifiant local et les exigences par texte exact ; une nouvelle exigence reçoit une nouvelle identité. Les écrans virtuels sont repérés par leur index avant publication : leur déplacement peut changer leur UUID, sans affecter les accords commerçants. La définition publiée fige tous ces identifiants.
- **T2-D12 — Quota administré :** la mutation interne `/partenaires/{id}/quota-generation` dispose d’une lecture `/commandes/{cle}` dans la portée `GENERATION_QUOTA:{partenaire}`. Le changement exige le droit ERP dédié et un motif ; il ne modifie pas rétroactivement les demandes déjà consommées.
- **T2-D13 — Provenance explicite :** ajouter `ConfigurationAnimation.preparation_response_id` comme FK `RESTRICT` vers la tentative source privée. La finalisation, l’édition et la réutilisation la renseignent ; la purge peut ainsi protéger une réponse utile sans dépendre de l’interprétation d’un identifiant dans JSONB.


- **T2-D14 — Dépendances du prompt :** recontrôler les commerçants actifs/autorisés et les éditions POI au dépôt, à l’acceptation, à la finalisation et à la réutilisation. Une nouvelle édition POI rend le contexte obsolète : le prompt doit être révisé explicitement. Le snapshot antérieur reste consultable ; aucun résultat n’écrase silencieusement les faits actualisés.



### 9.5 Décisions d’implémentation T3 — 19 septembre 2026

- **T3-D01 — Relecture explicite :** `preparation_reviewed_revision` est une référence privée adjacente à la préparation. Seul « Enregistrer et valider la préparation », avec minimum de commerçants explicitement choisi, la renseigne. Import et réutilisation restent à relire ; une modification des paramètres communs impose une nouvelle relecture avant invitation. Aucune approbation Localeo supplémentaire.
- **T3-D02 — Compilation :** assembler exclusivement les positions retenues et la mission acceptée de chacune. Conserver les identités, dériver START/FINAL et les transitions SUCCESS de l’ordre validé. Le public vient du brief ; la présentation hérite du thème, puis de la position et de la mission. Une mission sans dialogue utilise l’interaction NONE, sans retirer l’attestation commerçante. Aucun collectible absent de l’éditorial n’est inventé et aucun refus ne retire automatiquement une étape.
- **T3-D03 — Vérifications :** un dossier privé possède sa propre version CAS et un historique auteur/date. La checklist couvre les versions de configuration, préparation et règlement ; la vérification d’une mission couvre son empreinte propre. La vérification POI couvre édition, position/contenu, dates, QR/révision et emplacement. Confirmer un contrôle n’incrémente pas la configuration et n’invalide pas les autres confirmations.
- **T3-D04 — Supports QR :** préparer les QR de tous les lieux physiques, commerces compris, conformément au défi sur place et à l’exemple joueur de la spécification. Les activer uniquement lors de la publication. Le QR opaque porte un UUID et une signature HMAC avec clé dédiée ; seul son condensat est persisté. Le GET organisateur autorisé restitue le support fonctionnel PNG, distinct des illustrations WebP. Une référence POI et son édition ou une référence commerçant, jamais les deux, identifie la destination. Configurer `LOCALEO_ANIMATION_QR_LIEU_SECRET` et son identifiant `LOCALEO_ANIMATION_QR_LIEU_KEY_ID` avant ouverture ; aucun secret de participant/coffret n’est réutilisé.
- **T3-D05 — Commandes de préparation :** exposer paramètres communs, dossier, checklist, missions, POI et supports QR sous `/animations/{id}/preparation`. Scopes de reçus `PARAMETRES_PREPARATION:{id}` et `VERIFICATIONS_PREPARATION:{id}`, action incluse dans l’empreinte ; les reçus n’embarquent ni média ni secret. La photo POI facultative référence un document privé rattaché à l’animation. Le corps commun fermé contient présentation, dates, inscription, lots, règlement et échéance des réponses, sans règles d’un autre moteur.
- **T3-D06 — Réponses commerçantes :** corps Chasse versionnés et fermés ; scope de reçu `DEMANDE_PARTICIPATION:{demandeId}`, action comprise dans l’empreinte, réautorisation du commerce à chaque accès/rejeu. Le reçu ne contient que demande, animation, version et statut ; le détail privé se recharge après confirmation. Les listes restent des métadonnées, sans alternatives ni base64. Les engagements sont versionnés par commerce.
- **T3-D07 — Publication et flyer :** photographier les faits autorisés en lecture SQL, rendre et stocker le flyer hors transaction, puis recontrôler source/version sous verrou avant rattachement documentaire et publication atomique. Le POST de publication porte `expectedVersion` et une clé explicite ; GET `/animations/{id}/publication/commandes/{cle}` réconcilie sa réponse. Le financement conserve le circuit et les contrôles existants ; une commande de lots engagée interdit sa modification silencieuse.

Ces choix précisent les adaptateurs et la persistance des invariants déjà retenus. La publication ne résout pas automatiquement les demandes sans réponse ni les préparatifs manquants.

- **T3-D08 — Gestion des invitations :** relance et annulation utilisent la portée de reçu `DEMANDE_PARTICIPATION_GESTION:{demandeId}`, l’action et la version attendue. La lecture est `/animations/{animationId}/demandes-participation/{demandeId}/commandes/{cle}`. L’envoi ciblé conserve `confirmer_version_configuration` et `demande_ids`, portée `DEMANDES_PARTICIPATION_ENVOI:{animationId}` ; le reçu se lit sous `/animations/{animationId}/demandes-participation/commandes/{cle}`. Annuler une invitation reste explicite et ne retire pas une position du parcours. Le traitement d’un retrait après publication relève de la neutralisation T5.
- **T3-D09 — Dates et provenance :** refuser dès l’édition une fin antérieure au début, une fermeture d’inscription après la fin ou une échéance commerçante passée/après début. Pour l’échéance, conserver le jour civil Europe/Paris d’EPIC 56. La publication recontrôle la période et la fermeture effective. Les QR/contrôles POI possèdent des FK liant animation, position et édition ; la configuration publiée conserve sa provenance et seulement les références médias du parcours retenu. Les documents de flyer publiés restent immuables, une régénération crée une nouvelle version documentaire.
- **T3-D10 — Habilitations de publication :** conserver `animation:publier` du portail Animation. La traduction ERP ADMIN de la section 6.2 n’inclut pas automatiquement cet ancien droit. L’octroi proposé a été rejeté par le contrôle automatique d’approbation pour autorisation insuffisamment explicite ; aucun octroi n’a été effectué. Les comptes ERP actuels peuvent préparer selon leurs droits et sont orientés vers un compte Animation habilité pour publier l’événement. La validation/publication du résultat IA reste celle de T2 ; elle n’est pas la publication de l’événement. La surface interne de publication refuse un contexte dépourvu du droit requis.

[Retour au moteur d’animation](README.md).


### Exploitation des supports QR (T3)

Le backend attend `LOCALEO_ANIMATION_QR_LIEU_SECRET` (au moins 32 octets) et `LOCALEO_ANIMATION_QR_LIEU_KEY_ID` pour signer les QR de lieu. La clé est dédiée, fournie par le stockage de secrets de l’environnement ; aucune valeur opérateur n’est versionnée. Une absence de clé bloque la création/lecture des supports. Une rotation doit préparer de nouveaux supports et les faire installer avant activation ; changer simplement la clé rend les anciens supports inutilisables. Le condensat persistant protège l’identité du support ; ni les listes ni les reçus n’exposent le token. L’édition courante des POI est verrouillée par identifiants triés pendant la compilation publiée.


### 9.6 Précisions d’implémentation T4 — 19 septembre 2026

- **T4-D01 — Lecture Live :** conserver une enveloppe fermée de participation (référence, inscription, identité publique de l’animation, résumé de progression et URL du QR personnel) et porter la projection versionnée dans `jeu`. Les champs français des DTO T1 restent canoniques ; `etatVue` expose les états dérivés de la section 6.3, `themeVisuel` porte le thème autorisé. Les champs de contenu indisponibles sont omis. Le point d’entrée historique par token retourne cette même enveloppe ; il ne produit plus un tableau de toutes les étapes. Aucun accès d’installation ne remplace le Bearer personnel.
- **T4-D02 — Exécution et traces :** conserver l’agrégat T1 comme photographie cohérente de l’état métier et matérialiser étapes, ordres, dates, preuves effectives, tentatives et effets dans les tables structurées T4, dans la même transaction. L’état ne contient aucune réponse saisie ; celles-ci restent dans les tentatives privées. La FK vers le reçu de commande est différée jusqu’au commit et unique par soumission. Les lectures n’initialisent ni exécution ni ordre en base.
- **T4-D03 — Présentation stable :** ordonner les propositions par SHA-256 de participation/version/étape/colonne/identifiant local, indépendamment du bloc de correction, puis conserver cet ordre dès le déblocage. Cela permet une lecture stable sans écrire lors d’un GET, y compris après réconciliation d’un retrait. Les ordres et dates déjà acquis ne sont pas écrasés.
- **T4-D04 — Reçus joueur :** le `commandId` est l’UUID du reçu durable ; la portée reste `COMMANDES_PARTICIPATION:{participationId}` et l’acteur stable est la participation. L’échéance est celle de l’accès personnel, pas la date de consultation. Un rejeu renvoie le même résultat et identifiant avec `replayed=true`, après authentification courante. Les refus métier ne sont pas conservés en V1 ; une mauvaise réponse valide est un résultat traité. Une commande déjà appliquée sans nouvel effet ne change pas la version de progression.
- **T4-D05 — Attestations commerçantes :** le résolveur personnel ne retourne que l’étape attestable par le commerce connecté et les versions attendues. Les attestations portent version de contrat/définition/progression/exploitation ; portée de reçu `ATTESTATIONS_PARTICIPATION:{participationId}`, acteur commerçant. Lecture `/protected/animation-locale/commercants/me/participants/{id}/attestations/commandes/{cle}`. Pour conserver l’unicité historique commerce/clé de la preuve, sa clé technique est dérivée de participation et clé de commande ; aucun QR brut n’est persisté.
- **T4-D06 — Définition jouée et inscription :** la publication compile aussi Passeport et Tombola dans le DSL versionné. L’accès joueur et l’inscription utilisent explicitement la configuration publiée, jamais le dernier brouillon. Pour Chasse, le corps d’inscription ajoute `declaration_adulte=true` et `reglement_version` égal à la version présentée ; conserver date de déclaration, version et FK de la configuration acceptée. Aucun champ enfant ni date de naissance n’est ajouté.
- **T4-D07 — Budget et confidentialité :** vérifier avant publication une borne conservatrice de la plus grande projection autorisée (couverture, étape courante, dernier résultat, objets et régularisations) ; refuser une présentation trop lourde sans couper ses textes. Le runtime borne aussi la réponse à 256 000 octets. Sélectionner les références médias autorisées en transaction, puis lire/décoder hors transaction. Les erreurs n’incluent ni valeurs saisies ni données privées. Le filtre public par commerce exclut Chasse et le flyer privé n’est pas un visuel public de secours.
- **T4-D08 — Carnet et reprises :** le carnet utilise une liste de champs autorisés pour les accès/résumés, y compris lors de lecture d’une ancienne entrée ou d’un import. Ni image ni projection narrative n’y est conservée. Une commande de scan incertaine garde seulement sa clé/descripteur dans l’onglet, jamais le QR brut ; après rafraîchissement, consulter d’abord son reçu puis scanner explicitement de nouveau si nécessaire. La qualification s’affiche exclusivement depuis le résultat serveur, jamais depuis le seul pourcentage.

Ces précisions conservent les invariants de la spécification ; T5 raccorde neutralisation, correction après gel et exploitation, T6 la conservation et la conversion avant ouverture.


- **T4-D09 — Données absentes et régularisation :** une adresse absente du référentiel Passeport reste absente de sa projection (`adresse` facultative), sans fabriquer de lieu. Les dates de preuves sont converties en UTC en conservant leur instant. Un QR signé avec une ancienne clé ne valide plus une nouvelle commande ; un reçu déjà acquis reste consultable/rejouable après authentification courante. Le scan d’une étape passée est accepté seulement pour une preuve commerçante à régulariser, sans rejouer son défi ni recréer ses effets.


- **T4-D10 — Entrée ERP et modèles de réponse :** les consoles à périmètre sont disponibles sous `/internal/erp/animations/generations` et `/internal/erp/animations/preparation`, avec la session ERP et les droits T2/T3. Les alias SQLAdmin restent réservés à ADMIN selon la politique historique ; aucun droit de publication d’événement n’est ajouté. Les reçus de consultation sont typés avec le résultat de leur commande, et leurs modèles sont vérifiés avant réponse ; un export brut téléchargeable est décrit comme fichier, sans passer pour une projection JSON publique.


### 9.7 Précisions techniques T5 — 19 septembre 2026


- **T5-D01 — Aperçu de retrait :** `expectedVersion` désigne la révision d'exploitation ; `definitionVersion`, `stepId`, `previewHash`, `motif` (1 à 2 000 caractères) et `confirmer: true` sont obligatoires. L'empreinte couvre définition, révision et faits des participations, pas seulement les compteurs. Une inscription ou progression concurrente rend donc l'aperçu obsolète. L'application prend la barrière exclusive, recalcule, compare et inscrit décision, audit, notifications Live et reçu dans la même transaction. Le retrait ne modifie pas individuellement toutes les exécutions.
- **T5-D02 — Continuité préparée :** `engineConfig.continuityElements`, facultatif et vide par défaut, déclare les dépendances. Chaque élément porte `id`, `sourceStepId` et `consumerStepIds`. `COLLECTIBLE` référence un `collectibleId` existant attribué uniquement par la source ; `INFORMATION` porte `title` et `content`, textes préparés distincts des aides optionnelles du défi. Chaque consommateur suit strictement la source dans la chaîne. Le moteur fournit l'information à l'achèvement normal ou à l'arrivée à la position dispensée ; aucun LLM n'intervient en jeu. Les éléments sans consommateur et dépendances cycliques, futures, absentes ou dupliquées sont refusés.
- **T5-D03 — Provenance de dispense :** un effet conserve sa clé unique et sa provenance initiale. Les nouveaux effets dispensés portent la décision globale et sa révision ; ces références sont protégées par FK. La projection ne montre que les éléments déjà acquis, avec leur origine. `parcoursAdapte` informe tous les inscrits sans révéler une étape future. Les notifications Live utilisent le même message générique et n'embarquent ni lieu, ni solution.
- **T5-D04 — Gel :** la clôture existante fige les qualifications calculées depuis la définition publiée, les résolutions, preuves effectives et neutralisations sous la barrière exclusive. Les statuts de participation ne suffisent pas. La population utilisée par le tirage reste la population existante ; des tables de provenance la lient à la configuration, à la révision d'exploitation, aux faits de chaque participation et aux preuves référencées. Aucun second tirage ni nouvelle chance n'est créé. La clôture est atomique avec ses notifications ; un rollback ne laisse aucun gel partiel.
- **T5-D05 — Anomalies après gel :** une anomalie référence population, preuve, participation, auteur, date et motif, avec des FK de portée et suppressions `RESTRICT`. Elle ne modifie ni preuve gelée, ni population, ni gain. La purge T6 doit respecter ces protections et supprimer les traces éligibles dans l'ordre des dépendances.
- **T5-D06 — Commandes et habilitations :** reçu de retrait sous `NEUTRALISATIONS_ANIMATION:{animation}` et permission `animation:neutraliser_etape` ; clôture sous `CLOTURE_MOTEUR:{animation}` et permission existante `animation:cloturer`. La clôture compare `expectedVersion` à la version de l'animation et `expectedExploitationRevision` à la coordination. Aucun droit ERP existant n'est élargi implicitement.

### T5-D02 — préparation exploitable

`SavePreparationInput` et la préparation privée acceptent `collectibles` et `continuityElements` optionnels. Omission préserve les valeurs ; une liste vide les efface explicitement. Les références utilisent les UUID stables de positions ; la suppression ou permutation d’une position source/consommatrice rejette les dépendances devenues orphelines. La compilation produit les actions d’attribution aux sources déclarées et ne consulte jamais le LLM pendant le jeu. Les objets sans déclaration de source restent des définitions non attribuées ; aucune attribution implicite. Les illustrations réutilisent exclusivement les médias contrôlés.

### Précisions T5 — correction des preuves et retrait des missions

- **T5-C01 — Correction contrôlée :** le support muni de `animation:regulariser_preuve` lit un aperçu avant toute correction. La confirmation porte la version de définition, la version de progression, la révision d’exploitation, l’empreinte de l’aperçu, un motif de 5 à 2 000 caractères et `confirmer: true`. Après la barrière animation partagée / participation exclusive, l’application relit ces faits. Un aperçu devenu périmé ne permet aucune mutation. Le reçu `CORRECTION_PREUVE:{validationId}`, propre à l’acteur, conserve le résultat initial ; l’ancien endpoint d’annulation applique ce même contrat.
- **T5-C02 — Narration conservée et provenance :** une correction avant gel annule seulement la preuve effective et recalcule l’éligibilité. Elle conserve résolutions, objets, dates et parcours déjà accomplis, avec une seule nouvelle version de progression. Un scan de régularisation autorisé crée une nouvelle preuve liée par `regularise_validation_id` à la dernière preuve annulée du même participant, de la même animation, étape et commerce. La preuve annulée reste conservée. La clé et la transaction empêchent toute double preuve effective.
- **T5-C03 — Correction après gel :** l’aperçu indique explicitement `ANOMALIE_APRES_GEL` et la qualification figée. La confirmation ajoute une anomalie distincte rattachée à la population et à la preuve ; elle ne modifie ni validation, ni progression, ni qualification, ni population de tirage. Une clôture survenue entre aperçu et confirmation impose un nouvel aperçu.
- **T5-C04 — Retrait commerçant publié :** accepter le retrait d’une mission Chasse exige les permissions `animation:gerer_participations_commercants` et `animation:neutraliser_etape`. L’aperçu global de neutralisation est lié à la version de la demande. Le reçu `RETRAIT_MISSION:{demandeId}` englobe dans une même transaction la neutralisation, la décision de retrait et les notifications. La définition publiée et la mission choisie restent figées. Le refus du retrait conserve son circuit existant et ne neutralise aucune étape.
- **T5-C05 — Contrats de lecture :** les aperçus et reçus de correction se lisent sous `/animations/{animationId}/validations/{validationId}/correction/{apercu|commandes/{cle}}`, et la correction se confirme par POST sur `/correction`. Le retrait expose `/animations/{animationId}/demandes-participation/{demandeId}/retrait/apercu`, `/retrait/accepter` et `/retrait/commandes/{cle}`. Le statut de reçu suit le protocole commun : confirmé, en cours, ou commande non enregistrée. Aucune réponse ambiguë n’est présentée comme une réussite.


### Précisions complémentaires T5 — interfaces et exploitation

- **T5-D07 — Transport et budget global :** les commandes d'exploitation utilisent des DTO fermés et le transport borné à 16 384 octets. Les aperçus relisent leurs faits à la confirmation ; les reçus se consultent après authentification courante. La clôture réutilise l'opération suivie existante, avec un budget SQL dédié de 60 secondes et 3 secondes d'attente de verrou ; la reprise consulte le reçu avant tout renvoi explicite. Les anciennes routes d'annulation de preuve exigent les mêmes versions, empreinte, motif, confirmation et permission `regulariser_preuve`.
- **T5-D08 — Parcours des interfaces :** l'onglet de suivi conserve les métriques serveur et les actions autorisées. Toute entrée de clôture mène à la confirmation versionnée. Les corrections nécessitent l'action `CORRIGER_PREUVE`, attribuée selon le droit explicite ; aucun droit `modifier` ne suffit. Un aperçu périmé est fermé et doit être redemandé explicitement. La continuité se prépare avec les positions déjà enregistrées ; la suppression d'une dépendance est explicite. Live ne montre que les éléments acquis et l'avis générique de parcours adapté.
- **T5-D09 — Indicateurs :** les tentatives proviennent des compteurs structurés d'étapes, les erreurs de l'état métier et les annulations/anomalies de leurs traces ; la purge des réponses détaillées ne remet pas ces indicateurs à zéro. Les générations en échec, obsolètes ou invalides sont distinguées des attentes humaines. Durée moyenne calculée sur départ/fin connus, absente si aucune durée n'est mesurable. Ces agrégats n'ajoutent aucun compteur métier persistant.


- **T5-D10 — Liste organisateur effective :** la liste des participants calcule la qualification depuis les faits groupés et le domaine avant de filtrer statut/qualifié et paginer. Une neutralisation différée apparaît donc immédiatement, sans matérialisation lors d’un GET. Après clôture, qualification et progression proviennent de la provenance gelée ; les anomalies ultérieures ne les changent pas. Recherche et pagination conservent leur périmètre partenaire/commune. Les faits sont chargés par animation, jamais par tentative ni par réponse privée.


- **T5-D11 — Exclusion des participations anonymisées :** préserver les invariants déjà portés par `ParticipantAnimation.devenir_gagnant` (refus de `ANONYMISE`) et `appliquer_resultat_moteur` (statut conservé), ainsi que la conservation des identités en §8.2. Avant gel, une participation `ANONYMISE` ne compte pas parmi les éligibles et ne peut entrer dans une nouvelle population, même si ses preuves utiles demeurent conservées. Sa progression reste traçable. Après gel, l’appartenance historique n’est pas réécrite à l’occasion d’une anonymisation.

- **T5-C06 — Reçu du refus :** le POST de refus conserve son circuit et sa portée historique. Son reçu se lit sur `/animations/{animationId}/demandes-participation/{demandeId}/retrait/refuser/commandes/{cle}` avec la seule permission de gestion des participations ; l’application vérifie aussi que le résultat mémorisé appartient exactement à cette animation et à cette demande. La neutralisation n’est pas requise pour refuser un retrait. Le motif de décision est conservé dans l’audit.


- **T5-D12 — Console ERP et clôture historique :** `/internal/erp/animations/exploitation` présente les agrégats, les étapes et les aperçus de correction/retrait. Les actions suivent exclusivement `allowedActions` et restent contrôlées côté application ; aucun nouveau droit de clôture ERP n'est attribué. L'ancien POST `/animations/{id}/cloturer` exige désormais le même `CloturerMoteurInput` et produit le même reçu que `/exploitation/cloture` ; aucune entrée HTTP sans versions ne permet de contourner le gel. Un résultat réseau incertain bloque les autres commandes jusqu'à consultation du reçu ou renvoi explicite du même corps et de la même clé.

### 9.8 Précisions techniques T6 — conversion avant ouverture

- **T6-CV01 — Conservation des brouillons :** conversion en place de l’enveloppe moteur sous la coordination exclusive de l’animation. Les UUID d’animation/configuration/positions/missions, paramètres, dates de création et références de provenance restent inchangés. Les colonnes de type/version moteur sont renseignées ; un DSL présent est validé et son empreinte est vérifiée ou complétée. Aucun DSL, date, adresse, accord ou contenu manquant n’est inventé. Les compilateurs de publication T3/T4 restent responsables de l’assemblage final.
- **T6-CV02 — Résultats distincts :** `CONVERTIE` signifie que l’enveloppe et la structure existante sont compatibles. `INCOMPLET` conserve un brouillon éditable mais bloque l’ouverture du périmètre tant que ses manques sont présents. Type/version inconnu, DSL invalide ou incohérence d’empreinte produit un écart explicite sans conversion destructive. Les contrôles de publication opérationnels demeurent séparés des contrôles de structure du convertisseur.
- **T6-CV03 — Simulation et reprise :** un manifeste JSON fermé/versionné contient au plus 50 animations, leurs configurations courantes, empreintes source/cible, résultats attendus et un inventaire explicite des démonstrations. L’application compare le manifeste aux faits relus sous verrou et recalcule la cible ; elle n’applique jamais des paramètres fournis par le manifeste. Une empreinte changée produit un conflit. Un journal unique `(source_configuration_id, converter_version, source_hash)` conserve résultat et empreintes ; une reprise de la même conversion vérifie aussi la cible existante.
- **T6-CV04 — Maintenance avant ouverture :** exécuter le CLI dans la fenêtre de maintenance avant ouverture. Contrôler globalement l’absence de publication avant chaque lot, la recontrôler dans chaque transaction et sous la coordination exclusive de l’animation cible, puis effectuer un audit global de préparation à l’ouverture. Une publication découverte interrompt la procédure et bloque l’ouverture ; aucune migration de partie active ni nouvelle barrière globale de publication n’est introduite. Une transaction par animation, lots de 50 maximum ; les transactions achevées et leur journal restent rejouables après interruption.
- **T6-CV05 — CLI explicite :** `scripts/database/convert_animation_moteur.py --simulate --all-drafts [--after UUID] --report fichier.json`, ou sélection répétée `--animation-id UUID`. Application : `--apply --manifest simulation.json --report resultat.json`. Audit final : `--verify-readiness --report audit.json`. Les démonstrations sont signalées par `--demo-animation-id UUID`, sans suppression. L’URL PostgreSQL vient uniquement de `LOCALEO_CONVERSION_DATABASE_URL`, jamais d’un `.env` ni d’un argument journalisé. Pas de migration automatique : appliquer v243 par le runner SQL habituel. Codes sortie 0 réussite, 2 écart bloquant, 1 incident technique ; rapports sans paramètres privés, réponses ni médias.

### Précisions T6 — conservation et suppression reprenable

- **T6-R01 — Exécution et accès :** un service applicatif unique gère la simulation, les lots quotidiens de 100 objets, les reprises, les gels et les rapports. La surface ERP conserve une session `ADMIN` explicite ; aucun droit de conservation n’est déduit d’une permission de modification ou de quota. Le traitement automatique utilise un contexte système distinct. L’ancien endpoint de purge délègue au même workflow.
- **T6-R02 — Échéances :** les catégories de génération inutile, essais et tokens suivent respectivement 30 jours après terminaison effective et 90 jours après la fin serveur applicable. Le retrait nominatif courant et les notifications suivent 12 mois calendaires, calculés sur l’instant UTC de référence avec rabattement au dernier jour du mois si nécessaire. Une consultation ne change aucune échéance. Les reçus joueur expirés sont supprimés après leurs éventuelles tentatives ; les reçus d’exploitation et preuves conservées ne sont pas assimilés à ces reçus joueur.
- **T6-R03 — Fichiers préparés :** enregistrer l’intention de chaque écriture de génération ou de flyer avant le `put`, avec périmètre, clé contrôlée et bail de préparation. Le rattachement acquiert le même verrou et refuse `PURGE_EN_COURS` ou `PURGE`. Un fichier resté sans rattachement après un crash devient candidat après expiration du bail et 30 jours depuis sa préparation, sous recontrôle des références et gels. Les artefacts antérieurs déjà inventoriés en base sont contrôlés selon leurs dépendances ; aucun fichier inconnu du stockage n’est supprimé par un inventaire global du bucket.
- **T6-R04 — Suppression :** le marquage transactionnel et l’intention persistée précèdent toute suppression externe. La suppression hors transaction considère « déjà absent » comme un succès, puis finalise le résultat. Une erreur laisse le marqueur et la tâche reprenable. Poser un gel ou ajouter une référence après le marquage est explicitement refusé. Les copies gérées et métadonnées éditoriales devenues inutiles sont retirées sans recopier le brut dans les rapports.
- **T6-R05 — Preuves et identité :** le retrait de l’usage nominatif courant conserve les identifiants stables et les liens probatoires. Les coordonnées encore nécessaires aux lots ou litiges sont isolées dans une archive à accès restreint, avec motif et échéance ou gel ; elles ne figurent plus dans les listes opérationnelles. Les purges de jeu ne suppriment ni population figée, ni tirage, ni gain, ni preuve liée, ni pièce comptable.
- **T6-R06 — Reprise et rapports :** un lot est identifié par politique, date UTC, catégorie et mode simulation/exécution. Le propriétaire dispose d’un bail renouvelable ; deux propriétaires ne traitent pas simultanément le même lot. Les éléments déjà marqués sont repris avant de continuer le curseur `(eligible_at,id)`. Les exclusions sont réexaminées lors d’une exécution suivante. Le rapport paginé expose uniquement identifiants, dates, compteurs, raisons et codes d’erreur ; aucune clé de stockage, identité personnelle ou contenu brut.
- **T6-CV06 — Correction explicite après conversion incomplète :** une nouvelle simulation d’une configuration corrigée peut être appliquée, y compris si son UUID n’a pas changé, dès lors que son empreinte source correspond exactement à la configuration relue sous verrou. Le journal conserve une nouvelle trace par empreinte source, sans modifier les traces précédentes. Un ancien manifeste reste en conflit lorsque sa cible a changé. La reprise recherche la trace de sa source exacte ; l’audit d’ouverture recherche celle dont la cible correspond à la configuration courante et revalide cette configuration.


### Précisions T6 — exploitation et vérification

- **T6-E01 — Activation :** le batch `animations.conserver` passe par le lanceur supervisé existant. `LOCALEO_ANIMATION_CONSERVATION_APPLY=false` par défaut maintient la simulation ; l'activation reste une configuration d'exploitation distincte après simulation et validation des rapports. Le corps du batch peut imposer explicitement son mode sous l'authentification `internal:batch`. Aucun bouton ERP ne lance une purge réelle.
- **T6-E02 — Planification :** une tâche quotidienne à `30 3 * * *`, explicitement en UTC, traite les catégories par lots initiaux de 100. L'horaire reste configurable via le mécanisme d'ordonnanceur existant. Une timezone propre à cette tâche empêche une configuration globale différente de déplacer son heure UTC ; les autres tâches gardent leur timezone actuelle.
- **T6-E03 — Supervision :** les rapports sont persistés même en cas d'erreur. Si un rapport comporte une erreur, le batch est signalé en échec dans la supervision commune ; son rapport détaillé permet la reprise. Le contrôle de santé existant signale également l'absence d'exécution ou un retard de plus de 26 heures. Les rapports et gels sont consultables dans une console ERP réservée au rôle ADMIN existant, sans contenu brut ni clé de stockage.
- **T6-E04 — Actions ERP :** pose et levée de gel sont des commandes identifiées et réconciliables, avec motif obligatoire ; la levée demande une confirmation explicite. La consultation des rapports/gels ne modifie aucune échéance. Une réponse réseau incertaine conserve la même clé et le même corps en mémoire jusqu'à lecture du reçu ou renvoi explicite. Les commandes sont bornées à 16 384 octets et les paramètres de pagination sont bornés.
- **T6-E05 — Contrat des erreurs :** le contrôle croisé aligne les réponses d'erreur OpenAPI des routes moteur sur l'enveloppe effectivement utilisée (`code`, `detail`, corrélation et violations sans valeurs fournies). Un modèle fermé commun remplace la description FastAPI générique de l'erreur de validation ; les modèles spécifiques déjà déclarés par une route restent prioritaires. Les consommateurs peuvent ainsi distinguer un reçu confirmé d'une erreur sans dépendre d'un schéma documentaire différent du transport.


### Précisions de recette transversale T6

- **T6-QA01 — Publication et missions structurées :** une Chasse préparée est évaluée sur les missions choisies et les accords liés à ses positions par le contrôle d’assemblage. La politique de participation reçoit explicitement le résultat de ce contrôle ; elle ne réclame pas en plus l’ancienne mission globale `mission_commercant`. Le minimum de commerçants provient de la préparation. Les contrôles des attentes, des refus conservés dans le parcours, des échéances, des accords et des vérifications restent obligatoires. Les autres moteurs conservent la validation de leur mission globale. La recette PostgreSQL traverse ce contrôle réel avant publication ; elle ne le remplace pas par un résultat simulé.
- **T6-R07 — Activation et pagination :** une purge réelle exige une simulation terminée de la même politique et catégorie. Un run inachevé est repris avant d’en ouvrir un nouveau, même après changement de date UTC ; un lot de 100 avance donc jusqu’à terminer une population plus grande. Tous les candidats restent recontrôlés sous verrou avant l’exécution réelle.
- **T6-R08 — Archive nominative limitée au besoin :** conformément au registre interne Annexe A V1 page 5 repris dans la spécification détaillée §11.3, les coordonnées sortent des listes courantes après 12 mois. La durée de cinq ans vise les preuves nécessaires des tirages, attributions et remises, et ne constitue pas une durée autonome des coordonnées. Seuls les besoins de population gelée, de gain, de suppléance ou de gel ciblé énumérés en T6-R09 justifient l’archive nominative ; sa nécessité est réexaminée quotidiennement et sa disparition la rend supprimable. Une lecture interne limitée au traitement d’un gain évite tout envoi au pseudonyme. Aucun endpoint général n’expose ces identités. Les preuves pseudonymisées restent séparées.

- **T6-QA02 — Paramètres d’exploitation après publication :** une commande dédiée sous coordination exclusive modifie uniquement début, fin, fermeture des inscriptions et capacité. Une table append-only `animation_parametres_exploitation` rattache chaque décision à l’animation, à sa configuration publiée et à la révision d’exploitation ; conserver valeurs précédentes/nouvelles, motif, auteur et contrôles. Le DSL, son empreinte, les étapes, les accords et les acquis ne sont pas réécrits. Un résolveur commun superpose ces seules valeurs en lecture pour jeu, scan, inscription, projections, calendrier, clôture et conservation. La fin effective sert aussi au recalcul des expirations des accès personnels et reçus minimaux de participation/attestation, sans réactiver un accès révoqué.
  - Contrat fermé `POST /animation-locale/animations/{id}/exploitation/parametres` : `expectedVersion`, `definitionVersion`, `expectedExploitationRevision`, `motif`, puis champs facultatifs `startsAt`, `endsAt`, `closesAt`, `maxParticipants`. L’omission préserve ; `closesAt:null` suit la fin et `maxParticipants:null` retire le plafond. Toute réouverture d’une fenêtre déjà fermée exige en plus `rouvrirInscriptions:true` strict. Le reçu est relisible sous `/parametres/commandes/{cle}`, portée `PARAMETRES_EXPLOITATION:{id}`. La permission existante `animation:modifier` suffit, dans le périmètre autorisé. La lecture utilise `animation:exploitation_lire` ; les profils ERP sans `animation:modifier` restent en lecture seule, sans droit implicite supplémentaire. Les projections SQL existantes du catalogue et de l’espace commerçant réutilisent le résolveur de persistance ; les autres services passent par le port de l’UoW. Aucun accès SQL n’est ajouté au domaine ni au résolveur applicatif.
  - Comparer les instants serveur à la période effective, indépendamment d’un statut de démarrage encore non synchronisé. Avant début : changements cohérents des quatre paramètres ; après début : début immuable et fin non raccourcie. Fin atteinte, clôture, annulation, archivage ou population gelée : aucune réouverture. Une baisse de capacité conserve les inscrits ; une prolongation conserve une fermeture explicite et ne réouvre pas implicitement les inscriptions.
  - Réutiliser les contrôles serveurs de financement/coffrets, commerces/accords et préparation applicables. Un changement de période exige les confirmations `horaires` et `accord_lieux` ; un changement de capacité exige `accessibilite` et `consignes`. Seule la réunion des rubriques affectées est demandée (`confirme:true` strict et `detail` non vide), conservée avec la décision et sa période cible. Une modification de fermeture seule ne demande aucune confirmation terrain. La projection `requiredVerifications` expose cette correspondance à l’interface. Une prolongation conserve les accords selon EPIC 56 ; cette reconfirmation de faisabilité ne remplace pas une acceptation commerçante manquante. Le déplacement du début reste dans l’intervalle présenté dans un accord accepté (`contenu_snapshot.date_debut/date_fin`) ; sortir de cet intervalle bloque la commande, sans fabriquer une nouvelle acceptation. La fermeture seule ne requalifie ni les accords ni le financement. Le contrôle postpublication ne repasse pas par le changement d’état de publication ni la préparation de nouveaux QR.
  - Les écritures historiques de configuration refusent les paramètres d’une animation publiée et orientent vers cette commande, pour imposer le même CAS, motif et contrôles depuis toute entrée. La régénération du flyer utilise les paramètres effectifs et reste une action documentaire distincte, avec préparation hors transaction. Les notifications signalent le changement et la nécessité de rééditer les supports déjà distribués.
- **T6-R09 — Tirage ou substitution tardifs :** le besoin nominatif couvre aussi le membre éligible d’une population déjà figée sans tirage réalisé, un gain à envoyer/en échec et le suppléant encore mobilisable tant qu’un gain du même tirage reste à traiter. L’attribution issue de cette population ou la substitution d’un gain existant conserve le statut `ANONYMISE` du participant ; elle ne crée aucune nouvelle éligibilité. Une archive manquante bloque explicitement le traitement tardif. Seule une copie d’envoi reçoit les coordonnées archivées, sans réécriture de la participation. Après disparition du besoin et des gels, l’archive devient purgeable ; une relance dépourvue de coordonnées disponibles est refusée.


- **T6-E06 — Saisie des paramètres publiés :** les interfaces présentent seulement les champs et vérifications proposés par le serveur. Elles transmettent les champs effectivement modifiés, le motif et les versions relues ; une valeur omise est conservée et une valeur vide autorisée devient `null` (fermeture suivant la fin, capacité illimitée). Les horaires sont saisis dans le fuseau Europe/Paris de l’animation ; une heure absente ou répétée au changement saisonnier demande un horaire non ambigu. Les contrôles serveur restent déterminants. Une réouverture demande une action explicite ; une réponse incertaine interdit un nouvel envoi automatique et permet la consultation du reçu. La réédition des supports déjà distribués est signalée après changement de période.
- **T6-R10 — Flyers des retraits classiques :** les droits et reçus du retrait Passeport/Tombola restent identiques. Préparer le flyer avant le helper transactionnel d’idempotence, puis recontrôler version de demande et empreinte de la source avant de rattacher ses métadonnées dans la transaction du retrait. Un rejeu déjà confirmé retrouve son reçu sans générer de fichier ; une préparation abandonnée reste inventoriée et purgeable. Aucun rendu ni stockage externe n’est exécuté sous verrou métier.
- **T6-R11 — Réimport et écriture tardive :** un import ultérieur des mêmes octets peut créer un nouvel artefact, sans réactiver la clé supprimée. La déduplication ne pointe vers le nouvel artefact que si l’ancien est purgé et ne possède plus de référence utile. Une écriture préparée qui termine après son marquage est refusée au rattachement et maintient une intention de suppression reprenable. Les reçus expirés de jeu et d’attestation sont traités après leurs essais ; les reçus de correction, neutralisation et gel restent dans leur circuit probatoire distinct.


- **T6-E07 — Ancienne entrée de conservation :** l’endpoint interne historique de purge conserve sa portée ADMIN et délègue au même service de conservation. Comme les autres mutations ERP, il exige aussi le jeton CSRF et une origine cohérente ; ce chemin ne doit pas permettre d’exécuter les suppressions par une session seule. Le batch machine reste distinct sous `internal:batch`.

- **T6-QA03 — Retrait classique et commerces effectifs :** conformément à la conception EPIC 56 §14 et à la spécification moteur §4.3–4.4, un retrait accepté d’un Passeport ou d’une Tombola cesse d’autoriser le commerce. Le résolveur commun lit les commerces de la définition publiée et retranche les décisions historiques `ANNULEE` avec `retrait_decision=ACCEPTEE` ; une demande en attente ou refusée ne change rien. Cette liste effective s’applique aux projections, scans, reçus réautorisés, progression, qualification et futur gel. Elle est une copie de lecture : définition publiée, empreinte, version et seuil matérialisé — y compris celui d’origine automatique — restent inchangés. Les preuves antérieures restent persistées avec leur statut et leur provenance ; seules les preuves des commerces encore autorisés comptent, sans dispense ni nouvelle attestation.
  - Avant acceptation, vérifier le minimum de commerces, le seuil Passeport toujours atteignable et l’absence de clôture/gel. Sous la coordination exclusive d’animation, recontrôler la demande et le flyer préparé, enregistrer la décision/configuration historique EPIC 56, avancer la révision d’exploitation et réconcilier les qualifications des participations. Une population gelée reste inchangée. La préparation et la régénération du flyer utilisent les commerces et dates effectifs ; le stockage reste hors transaction et le rattachement conserve son contrôle de version. Aucune règle de qualification n’est ajoutée à l’API ni à l’interface.

- **T6-E08 — Entrée des paramètres publiés :** dans Animation, le bouton de la configuration publiée ou en cours mène à l’onglet Live et à ses paramètres d’exploitation. Le formulaire historique reste réservé aux brouillons et coffrets autorisés avant publication ; il ne propose plus de prolongation par le PATCH de configuration, désormais refusé par le backend. Les droits et champs modifiables restent ceux de la projection serveur dédiée.

- **T6-QA04 — Navigation ERP après déploiement :** le lien « Animation → Demandes de création » doit être présent dans le menu principal de l’espace de travail ERP et sa page Animation, en complément de l’entrée SQLAdmin. Les consoles `/internal/erp/animations/{generations,preparation,exploitation,conservation}` sont composées dans le routeur UI avant ses routes génériques, afin qu’elles ne soient pas interceptées comme des identifiants d’objet. Les contrôles de session, rôle et périmètre restent ceux des consoles et des API ; la conservation reste réservée à ADMIN. Ce raccordement corrige un défaut de navigation du commit T6, sans nouveau droit ni contrat métier.

- **T6-QA05 — Catalogue incomplet :** les trois types V1 restent proposés depuis le catalogue persistant. Si les fiches Passeport ou Tombola manquent après initialisation/reprise de données, une migration additive restaure uniquement ces entrées avec les valeurs historiques de v187 corrigées orthographiquement par v230. Un modèle existant, même désactivé ou personnalisé, reste intact ; aucun repli frontend ni réactivation implicite. La migration est rejouable et ne touche ni animations, ni invitations, ni droits.

- **T6-QA06 — Catalogue visible (demande utilisateur) :** retirer les deux cartes statiques « Prochainement » — « Chasse au trésor » et « Défi commerçants » — de la page Modèles et du choix de modèle de Nouvelle animation. Présenter seulement les fiches renvoyées par le catalogue backend ; le modèle actif Chasse au trésor commerçante reste disponible avec Passeport et Tombola. Aucun changement des données ni des droits.

- **T6-UX01 — Léo, assistant IA (demande utilisateur) :** Léo incarne l’assistance à la préparation dans Localeo Animation. Le bouton générique « Préparer avec l’IA » est retiré ; la carte Chasse au trésor commerçante porte la mention « Assisté par Léo » dans le catalogue et le choix de modèle. Le bouton « Continuer » ouvre la préparation guidée existante. Le Passeport suit le parcours manuel, sans choix de mode ni accès Léo, conformément à la correction T6-UX03 du 20 septembre 2026. Tombola garde sa configuration manuelle.
  - Identité proposée : petite bulle souriante bleu Localeo `#0B3D63` avec une étincelle orange `#ED7D21`, réalisée en SVG et toujours accompagnée du nom. La mention reste informative ; la sélection du modèle et du mode est accessible au clavier. Le repère se retrouve au début du brief guidé.
  - Voix : française, chaleureuse et concise, vouvoiement ; Léo explique la préparation et invite à relire/ajuster la proposition. Son identité d’assistant IA est explicite. Les états d’attente, quotas, erreurs et commandes existants restent la source du comportement. Cette première présence accompagne le parcours livré, sans ajouter de conversation, fournisseur automatique ou nouveau droit.


### T6-QA07 — Accès des batchs de génération au middleware HTTP

Le traitement `animations.generer` prévu par T2-D10 doit atteindre son endpoint `POST /internal/animation-locale/generations/traiter` avec la clé active `internal:batch`, sans session ERP. La même règle s'applique à `POST /internal/animation-locale/conservation/executer` ; sa simulation par défaut et son activation explicite restent celles de T6. Le middleware de session laisse passer uniquement ces couples méthode/chemin vers leur dépendance de contrôle de clé existante. Une clé absente, invalide, révoquée ou d'un autre scope reste refusée. Aucune autre route ERP n'est ouverte par cette exception ; OpenAPI décrit la clé et non une session pour ces deux batchs.

En `PREPARATION_PROMPT`, l'ERP explique que le prompt est en attente du traitement automatique et propose d'actualiser. L'export et le dépôt restent pilotés par `allowedActions`, puis deviennent accessibles en `ATTENTE_TRAITEMENT_MANUEL`. Une panne technique ne doit pas être contournée par un changement direct de statut, une nouvelle demande ou un dépôt sans prompt.


### T6-UX02 — Traitement guidé des demandes dans l’ERP

À la demande utilisateur, la console présente une liste de demandes nommées et un détail en trois étapes : **Prompt**, **Vérification de la réponse**, **Traitement**. Le titre vient du brouillon courant (`animationName` dans la projection). Ce champ accepte `null` dans les anciens reçus persistés pour préserver leur relecture/rejeu ; les listes et détails courants le renseignent systématiquement. Les états et prochaines actions sont en français ; identifiants, affectation, révision, annulation, quota et filtres avancés restent accessibles dans des sections secondaires repliées. Le contexte renseigné par le gestionnaire est lisible dans le détail.

1. Sélectionner une demande affiche automatiquement son prompt complet depuis l'export texte serveur : messages et schéma JSON attendu inclus. Le bouton **Copier le prompt complet** copie exactement ce texte ; les téléchargements restent disponibles. Aucun prompt n'est reconstruit ni inventé dans le navigateur si sa préparation est encore en attente ou son contenu purgé.
2. Coller le JSON de réponse, ou importer un fichier, puis **Vérifier la réponse**. Le nouvel endpoint ERP `POST /internal/animation-locale/operations/{id}/reponses/verifier` reçoit la même enveloppe que le dépôt et rend le rapport du validateur existant. Il exige session, CSRF, droit de dépôt, périmètre, phase, versions et prompt courant. Il contrôle schéma, cohérence métier et médias, sans créer de tentative, fichier, consommation de quota ni transition. Le transport garde le texte JSON original et les contrôles de doublons, taille, profondeur et encodage ; aucune valeur d'entrée sensible n'est recopiée dans les erreurs serveur.
3. Un rapport conforme affiche un aperçu et permet **Enregistrer la réponse**. Le dépôt durable conserve ses contrôles et son traitement serveur. Après contrôle conforme, l'opérateur relit la tentative enregistrée, confirme sa relecture et choisit **Traiter la demande** ; cette commande accepte la réponse et complète le même brouillon. Elle ne publie pas l'animation au public. Aucune acceptation automatique ni nouvelle permission n'est introduite.

Une modification du texte, du prompt, de la version source ou de la demande invalide la pré-vérification. Les réponses tardives d'une autre sélection ou d'un ancien contrôle sont ignorées ; l'actualisation d'une même demande conserve la saisie. Un changement de sélection avertit avant d'abandonner une réponse non enregistrée. Les saisies restent en mémoire, jamais dans le stockage navigateur. Les lectures des phases techniques peuvent être actualisées automatiquement de façon bornée ; aucune écriture n'est rejouée automatiquement. Une réponse de mutation perdue exige toujours la consultation du reçu avant toute suite, avec la même clé et le même corps en cas de renvoi explicite. L'interface se réorganise sur mobile, conserve navigation clavier, focus visible, libellés et annonces accessibles.


### T6-UX03 — Passeport manuel dans Localeo Animation

La demande utilisateur du 20 septembre 2026 remplace le choix manuel/assisté de T6-UX01 et la proposition de génération Passeport dans l'interface décrite par T2-D02. Le Passeport commerçant n'est pas proposé comme animation pilotable par l'IA : supprimer le choix « Je prépare moi-même / Avec Léo, assistant IA » à la sélection du modèle ; **Continuer** ouvre directement sa création manuelle. L'onglet Configuration conserve ses formulaires métier et retire également le panneau de génération Passeport. La Chasse conserve le badge et le parcours Léo ; la Tombola conserve son parcours manuel.

Cette correction vise les entrées de Localeo Animation. Les contrats et données historiques de génération Passeport ne sont ni supprimés ni modifiés ; elle n'introduit pas de migration ou de mutation de demande existante. La capacité technique décrite en section 4.3.3 ne constitue plus une fonctionnalité offerte à l'organisateur dans cette interface.
