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

Acceptation Chasse : corps fermé `{expectedVersion,presentedRevision,presentedHash,missionId,confirmedRequirementIds[]}`. Toutes et seulement les conditions de la mission choisie sont confirmées ; refuser IDs étrangers, doublons, deux choix, date dépassée et version périmée. Comparer une empreinte des engagements **par commerce**, incluant les dépendances communes pertinentes (dates/règlement). Une retouche propre à A n’invalide pas B. L’acceptation atteste la capacité à préparer ; depuis E55-UX-11, aucune checklist organisateur ne constitue un prérequis de publication. La déclaration commerçante « prêt » demeure une étape distincte lorsque le suivi est actif.

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

Les prompts Chasse et Passeport de version `1.1` exigent explicitement la génération réelle d'au minimum une couverture adaptée au thème et au public, référencée dans `themeVisuel.illustrationCouverture` et embarquée dans `medias`. Une description ou un `promptGeneration` seul ne suffit pas ; l'outil d'images et l'encodage WebP sont requis dans la même demande. Un outil indisponible ou un média manquant doit être signalé comme un échec, jamais comme un résultat terminé. Les illustrations supplémentaires restent facultatives. Cette exigence concerne les consignes des nouveaux prompts et leurs révisions ; le schéma et le validateur d'import `1.0` conservent leur compatibilité avec les anciens résultats sans illustration. Les prompts déjà enregistrés restent immuables et nécessitent une révision explicite pour bénéficier de la nouvelle consigne.

Le JSON brut autonome est conservé comme artefact privé via le stockage documentaire existant (`app/infrastructure/storage/document_storage.py`, derrière un port applicatif dédié). Les prompts/messages sont du texte en base ; les lignes de réponses référencent le brut privé et un contenu éditorial normalisé JSONB. Les WebP décodés peuvent être dédupliqués dans ce même stockage privé, avec une table `animation_medias` (UUID, partenaire, ID logique, SHA-256, format, dimensions, octets, document privé). `animation_references_medias` relie explicitement chaque média à ses versions de réponse/template/configuration. Les octets ne sont pas recopiés dans chaque ligne d’exécution.

L’export autorisé réassemble systématiquement le JSON autonome avec base64 ; cette organisation interne ne remplace pas le contrat demandé par des URL. La projection Live peut embarquer uniquement les médias accessibles sous la même forme. Ne pas enregistrer ces images narratives dans le catalogue public `media_assets` ni les servir via `/public/images` : publier une animation n’autorise pas ses images futures.

Écriture d’artefact : préparer un fichier privé temporaire, vérifier son empreinte, puis enregistrer référence et dépendance en transaction. Un rollback laisse un candidat au nettoyage, jamais un lien publié cassé. Les clés de stockage sont générées côté serveur, sans chemin fourni par le JSON. Déduplication dans le périmètre autorisé ; l’existence d’un hash d’un autre partenaire n’est pas révélée. La lecture/purge vérifie aussi les références utiles du brut et des médias extraits.

### 7.2 Pipeline de contrôle

1. Borner le flux avant chargement JSON, refuser les clés dupliquées, nombres non finis et structure trop profonde. Le body d’import n’est jamais repris dans une erreur ni loggé.
2. Valider le schéma du type/version et les références du brief. Vérifier les limites textuelles avant rendu. Le rapport conserve le code, le chemin et l'explication des erreurs métier de cohérence, même lorsqu'elles sont encapsulées par le validateur de schéma. Pour une mission commerçante, le chemin identifie l'étape et la mission candidate. Ne jamais restituer les valeurs rejetées ni le contexte technique des autres exceptions. Les variantes de réponse TEXTE doivent être distinctes après normalisation ; les prompts rappellent que casse, accents et espaces superflus sont déjà neutralisés.
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
- **T2-D04 — Faits de lieux :** la bibliothèque POI conserve une identité partenaire/commune et des éditions immuables `{nom,adresse,faits,responsable}`. Une édition ne vaut jamais vérification pour une chasse ; celle-ci reste distincte en T3. Depuis la décision du 20 septembre 2026, le serveur résout le nom et l’adresse depuis la [fiche commerçant](../espace-commercant/adresse-postale.md), après contrôle de l’identité, du périmètre et du statut. L’organisateur fournit les faits utiles à la mission et la référence du commerce, sans adresse dupliquée. Une adresse absente bloque la génération ; aucune déduction depuis la commune ou l’adresse fiscale. Les snapshots historiques conservent leur provenance et leur contenu. Pour un POI, le snapshot provient de son édition autorisée et son responsable reste hors du prompt créatif.
- **T2-D05 — Import fidèle :** le navigateur transmet le texte JSON original du fichier dans l’enveloppe d’import, sans parse/sérialisation intermédiaire qui effacerait des clés dupliquées. Le transport commun garde cookies, CSRF et interdiction des retries d’écriture. Le serveur borne le flux avant parsing, refuse les encodages HTTP compressés pour cet import et applique le parseur strict puis les modèles fermés. Toute sortie privée est `no-store` ; les erreurs ne recopient ni valeurs d’entrée ni base64.


- **T2-D06 — Illustrations à la génération :** une nouvelle `InitialisationGeneration` porte `assets:[]` et une couverture nulle. Le résultat importé apporte ses illustrations contrôlées. Cette restriction ne modifie ni le DSL commun ni les templates réutilisés, qui gardent leurs médias privés. Police et couleurs restent configurables.
- **T2-D07 — Bibliothèque de templates :** `GET /templates`, `POST /operations/{id}/templates` et `POST /templates/{version_id}/reutilisations` permettent la sauvegarde explicite d’un résultat accepté et sa réutilisation dans la même commune, sans quota de génération. Ajouter `ENREGISTRER_TEMPLATE` aux actions permises après acceptation. Portées de reçus `TEMPLATE_CREATE:{operation}` et `TEMPLATE_REUSE:{version}` ; lectures sous les mêmes ressources via `/commandes/{cle}`. Le template accepté est immuable ; un brouillon cible existant exige sa version attendue.
- **T2-D08 — Reçus durables :** les commandes de génération, préparation et templates ont `expires_at=NULL` pendant leur utilité, au lieu d’une expiration arbitraire. La conservation T6 calcule l’échéance quand les parents deviennent éligibles, sans supprimer la rejouabilité d’une demande active.
- **T2-D09 — Catalogue et publication :** enregistrer explicitement Chasse dans le catalogue et le registre avec une stratégie de préparation. L’édition n’envoie aucune invitation implicite EPIC 56. La publication est fermée tant que T3 n’a pas assemblé et vérifié la préparation ; aucun repli vers les règles Passeport.
- **T2-D10 — Ordonnancement :** le batch `animations.generer` est planifié chaque minute par l’ordonnanceur existant, avec surcharge cron habituelle, deux tâches au maximum par processus, supervision HTTP de 120 secondes et rattrapage de démarrage après dix minutes. Les phases humaines ne sont jamais revendiquées par ce worker. Les transactions courtes de génération et de bibliothèque appliquent `lock_timeout=3s` et `statement_timeout=15s` ; stockage et décodage restent hors transaction.
- **T2-D11 — Identités de préparation :** au premier import, les UUID sont dérivés du résultat source. Aux éditions suivantes, conserver les positions par identité de lieu et occurrence, les missions par identifiant local et les exigences par texte exact ; une nouvelle exigence reçoit une nouvelle identité. Les écrans virtuels sont repérés par leur index avant publication : leur déplacement peut changer leur UUID, sans affecter les accords commerçants. La définition publiée fige tous ces identifiants.
- **T2-D12 — Quota administré :** la mutation interne `/partenaires/{id}/quota-generation` dispose d’une lecture `/commandes/{cle}` dans la portée `GENERATION_QUOTA:{partenaire}`. Le changement exige le droit ERP dédié et un motif ; il ne modifie pas rétroactivement les demandes déjà consommées.
- **T2-D13 — Provenance explicite :** ajouter `ConfigurationAnimation.preparation_response_id` comme FK `RESTRICT` vers la tentative source privée. La finalisation, l’édition et la réutilisation la renseignent ; la purge peut ainsi protéger une réponse utile sans dépendre de l’interprétation d’un identifiant dans JSONB.


- **T2-D14 — Dépendances du prompt :** recontrôler les commerçants actifs/autorisés et les éditions POI au dépôt, à l’acceptation, à la finalisation et à la réutilisation. Une nouvelle édition POI ou une modification de l’adresse issue de la fiche commerçant rend le contexte obsolète : le prompt doit être révisé explicitement. Le snapshot antérieur reste consultable ; aucun résultat n’écrase silencieusement les faits actualisés.



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

Complément spécifié le **12 novembre 2026**, non implémenté :
[E73-EVO-CLOTURE-AUTO](../epic-73-animation-et-ou-coffrets/fin-animation-archives.md#évolution-du-12-novembre-2026--clôture-automatique-et-report-de-fin)
ajoute la clôture à échéance, un rapport organisateur et une intention Live/WebPush
aux changements effectifs de fin de T6-QA02. Les gardes de période, le DSL publié,
les accords et les acquis décrits ici sont conservés. La même coordination
sérialise report, jeu et clôture ; aucune réouverture après échéance n’est ajoutée.

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

À la demande utilisateur, la console présente une liste de demandes nommées et un détail en trois étapes : **Générer**, **Importer et contrôler**, **Relire et transmettre**. Le titre vient du brouillon courant (`animationName` dans la projection). Ce champ accepte `null` dans les anciens reçus persistés pour préserver leur relecture/rejeu ; les listes et détails courants le renseignent systématiquement. Les états et prochaines actions sont en français ; identifiants, affectation, révision, annulation, quota et filtres avancés restent accessibles dans des sections secondaires repliées. Le contexte renseigné par le gestionnaire est lisible dans le détail.

1. Sélectionner une demande affiche automatiquement son prompt complet depuis l'export texte serveur : messages et schéma JSON attendu inclus. Le bouton **Copier le prompt complet** copie exactement ce texte ; les téléchargements restent disponibles. Aucun prompt n'est reconstruit ni inventé dans le navigateur si sa préparation est encore en attente ou son contenu purgé.
2. Coller le JSON de réponse, ou importer un fichier, puis **Vérifier la réponse**. Le nouvel endpoint ERP `POST /internal/animation-locale/operations/{id}/reponses/verifier` reçoit la même enveloppe que le dépôt et rend le rapport du validateur existant. Il exige session, CSRF, droit de dépôt, périmètre, phase, versions et prompt courant. Il contrôle schéma, cohérence métier et médias, sans créer de tentative, fichier, consommation de quota ni transition. Le transport garde le texte JSON original et les contrôles de doublons, taille, profondeur et encodage ; aucune valeur d'entrée sensible n'est recopiée dans les erreurs serveur.
3. Un rapport conforme affiche un aperçu et permet **Enregistrer la réponse**. Le dépôt durable conserve ses contrôles et son traitement serveur. Après contrôle conforme, l'opérateur relit la tentative enregistrée, confirme sa relecture et choisit **Traiter la demande** ; cette commande accepte la réponse et complète le même brouillon. Elle ne publie pas l'animation au public. Aucune acceptation automatique ni nouvelle permission n'est introduite.

Une modification du texte, du prompt, de la version source ou de la demande invalide la pré-vérification. Les réponses tardives d'une autre sélection ou d'un ancien contrôle sont ignorées ; l'actualisation d'une même demande conserve la saisie. Un changement de sélection avertit avant d'abandonner une réponse non enregistrée. Les saisies restent en mémoire, jamais dans le stockage navigateur. Les lectures des phases techniques peuvent être actualisées automatiquement de façon bornée ; aucune écriture n'est rejouée automatiquement. Une réponse de mutation perdue exige toujours la consultation du reçu avant toute suite, avec la même clé et le même corps en cas de renvoi explicite. L'interface se réorganise sur mobile, conserve navigation clavier, focus visible, libellés et annonces accessibles.

Précision du 31 octobre 2026 : un encart **Votre prochaine action** guide
l'opérateur selon la phase, les droits et le service de préparation. Si la
demande reste à qualifier ou attend un complément, son accès au suivi du
service est prioritaire ; l'affectation seule ne vaut pas qualification et
aucune progression automatique n'est promise avant ce prérequis. Les états
de service existants et leurs commandes restent portés par leur page dédiée.

Le prompt reste chargé intégralement, avec copie immédiatement disponible ;
son texte et ses téléchargements se déplient à la demande. L'import de fichier
est prioritaire, le collage JSON reste accessible dans un volet secondaire.
Chaque étape distingue l'action courante, l'attente et l'acquis serveur ; une
pré-vérification locale conforme indique **À enregistrer**, jamais une étape
enregistrée. La fin de traitement confirme la transmission du parcours dans
le brouillon et rappelle que sa publication reste séparée. Le gestionnaire
peut poursuivre la préparation de la Chasse ou traiter une autre demande.


### T6-UX03 — Passeport manuel dans Localeo Animation

La demande utilisateur du 20 septembre 2026 remplace le choix manuel/assisté de T6-UX01 et la proposition de génération Passeport dans l'interface décrite par T2-D02. Le Passeport commerçant n'est pas proposé comme animation pilotable par l'IA : supprimer le choix « Je prépare moi-même / Avec Léo, assistant IA » à la sélection du modèle ; **Continuer** ouvre directement sa création manuelle. L'onglet Configuration conserve ses formulaires métier et retire également le panneau de génération Passeport. La Chasse conserve le badge et le parcours Léo ; la Tombola conserve son parcours manuel.

Cette correction vise les entrées de Localeo Animation. Les contrats et données historiques de génération Passeport ne sont ni supprimés ni modifiés ; elle n'introduit pas de migration ou de mutation de demande existante. La capacité technique décrite en section 4.3.3 ne constitue plus une fonctionnalité offerte à l'organisateur dans cette interface.


### T6-UX04 — Consultation d’une animation en préparation

La consultation du brouillon ne suppose pas de définition publiée. L’onglet Configuration conserve le brief, les paramètres et le financement avant la réception du parcours. Les contrôles terrain ne sont chargés qu’après lecture réussie de la préparation ; l’absence de parcours renvoie à son enregistrement, sans appel prématuré aux vérifications. Les autres erreurs de lecture restent visibles. Une nouvelle lecture après acceptation de la génération donne accès aux contrôles habituels.

Précision du 20 septembre 2026 : pour une animation existante dans le périmètre autorisé, `GET /animations/{animation_id}/preparation` retourne **200** avec `revision: 0`, `sourceOperationId: null` et `preparation: null` tant qu'aucun parcours n'est enregistré. Ce cas est déjà prévu par `PreparationPayload` ; il ne représente ni une préparation validée ni une autorisation de publier. Le client attend une préparation non nulle avant les vérifications. Les animations inexistantes ou hors périmètre restent en **404**, les permissions manquantes en **403**. Les commandes d'édition et leurs reçus continuent d'exiger une préparation existante. Aucun schéma, migration ou contrat embarqué supplémentaire n'est nécessaire.

La consultation `GET /animations/{animation_id}/validation-publication` doit également accepter un brouillon créé par la génération avant le choix des lots : une clé `lots` absente, nulle ou vide représente une sélection vide pour le contrôle d’éligibilité. Le rapport reste en **200** avec `valide: false` et les prérequis métier non satisfaits (préparation, participation, financement). Les commerçants et coffrets effectivement sélectionnés restent contrôlés. Aucune configuration n’est complétée ni enregistrée par cette lecture ; la publication reste refusée tant que les conditions requises ne sont pas remplies. Les droits, le périmètre, le contrat de réponse et les règles de financement restent inchangés.

Les onglets Validations et Live d’une animation avant publication présentent un état explicatif et un accès à Configuration ; ils ne demandent pas encore les données d’exploitation d’une définition publiée. Le statut serveur guide cette présentation, sans remplacer les autorisations backend. L’API des participants retourne une page vide pour une animation BROUILLON ou CONFIGUREE sans configuration publiée seulement si le compteur réel de participations est nul, après contrôle des droits et du périmètre. Une participation présente sans définition, ou une animation publiée sans définition, reste une incohérence signalée. Aucun parcours ni participant fictif n’est produit ; inscription, jeu et validation conservent leurs prérequis de publication. Aucun changement de contrat ou de migration.

### T6-UX05 — Lectures partagées dans la configuration

L'ouverture de la configuration d'une Chasse effectue une seule lecture des
modèles, des commerçants éligibles et de la préparation. Le détail transmet le
modèle au formulaire ; le bloc limité au financement ne charge pas le catalogue
des commerçants. L'éditeur et les vérifications consomment la même lecture du
parcours, conservée en mémoire uniquement pendant la présence de cet écran.

Une sauvegarde confirmée relit le parcours une fois et transmet cette version aux
vérifications. Une actualisation explicite relit le serveur ; les erreurs restent
visibles et peuvent être reprises. Les vérifications attendent une préparation
non nulle ; elles sont réévaluées après changement des paramètres communs.
Les réponses tardives d'un écran ou contexte quitté ne doivent pas rétablir ses
données. Aucun cache persistant ni délai de fraîcheur n'est introduit ; les
contrats backend, contrôles d'accès et commandes idempotentes restent inchangés.

### T6-FIN01 — Un reçu de paiement pour les lots de l’animation

La demande utilisateur du 20 septembre 2026 impose un seul reçu de paiement par commande de lots, quelle que soit la quantité ou la diversité des coffrets. Le reçu consolidé détaille toutes les lignes de la commande et le total. La règle antérieure de présentation de la répartition crédit/Stripe, si elle figure dans le snapshot, est conservée. La règle documentaire canonique est la [fonction 5 de la spécification Animation EPIC 50](../epic-50-conformite-fiscale-bum/localeo-animation.md#fonction-5---documents-dacquisition). Les acquisitions sous-jacentes gardent leurs données de traçabilité ; leurs anciens reçus unitaires restent archivés, mais ne sont plus proposés dans les documents de la commande d’animation. Les achats hors animation conservent leur comportement.

### T6-UX06 — Préparation guidée et traitement ERP par étapes

La correction demandée le 23 septembre 2026 traite la difficulté à identifier
l'action courante dans les formulaires de préparation existants. Elle réorganise
les interfaces de T2/T3 sans introduire de nouvel état métier, de permission,
de contrat API ou de migration.

Dans Localeo Animation, **Configuration** d'une Chasse présente six étapes :
**Parcours**, **Paramètres et lots**, **Commerces**, **Terrain**, **Financement**,
**Publication**. Une seule étape est affichée à la fois. Le gestionnaire voit
sa position, la tâche à réaliser et une aide contextualisée ; il peut revenir
aux étapes précédentes. Les participations restent accessibles depuis leur
onglet existant et sont également proposées dans le parcours guidé.

La navigation n'enregistre aucune donnée et ne confirme aucun contrôle métier.
Une étape consultée n'est pas déclarée terminée. Les saisies des étapes déjà
ouvertes restent en mémoire pendant la présence dans Configuration ; elles
doivent être enregistrées par leur commande explicite. Aucun stockage navigateur
de ces données n'est ajouté. Une commande en cours ou dont le résultat reste
incertain garde son écran de résolution accessible avant de poursuivre.
Les modifications non enregistrées sont signalées avec leur rubrique ; elles
empêchent la publication tant qu'elles ne sont pas résolues. Un retour de
paiement reconnu ouvre le financement et conserve la lecture partagée du
parcours ; le marqueur d'URL ne confirme jamais un paiement.

La réponse acceptée dans l'ERP rend le parcours disponible à l'organisateur.
Elle ne confirme ni les missions des commerces ni les vérifications terrain.
La publication exige toujours le contrôle serveur courant et sa confirmation
explicite. Les lectures partagées de T6-UX05, les versions attendues, les droits
et la réconciliation des reçus restent applicables.

Dans l'ERP, les trois étapes **Générer**, **Importer et contrôler**,
**Relire et transmettre** remplacent
l'affichage simultané des trois formulaires. La phase serveur indique l'étape
utile et l'action suivante ; la navigation permet la relecture sans mutation.
Le dépôt par fichier et le collage de JSON sont accessibles au même endroit.
La pré-vérification, l'enregistrement durable et la relecture avant transmission
au gestionnaire restent distincts. Une reprise autorisée ou une actualisation
nécessaire est proposée près du blocage ; l'historique conserve les opérations
secondaires. Aucun changement de phase ni envoi n'est déclenché par la navigation.

La [procédure d'usage](exploitation-moteur.md) décrit ces étapes. Les preuves
locales et leurs limites sont consignées dans le [suivi](suivi-implementation.md).

### T6-UX07 — Édition visuelle du parcours et aperçu d'une étape

La correction du 24 septembre 2026 complète le guidage de T6-UX06 dans sa
rubrique **Parcours**. L'éditeur générique imbriqué est remplacé, pour les
résultats contenant des étapes de Chasse, par une liste ordonnée et un panneau
de détail d'une seule étape. La liste présente titre, lieu et activité ; la
sélection de l'étape est un état d'interface, sans enregistrement implicite.
Les commandes de déplacement sont accessibles au clavier et conservent la
sélection. L'ajout ouvre la nouvelle étape ; un retrait exige une confirmation.

L'édition sépare le contenu destiné au joueur, l'activité et les préparatifs
privés du commerce. Les missions alternatives restent dans la même position
du commerce. Le sélecteur de mission sert à consulter ou modifier une
proposition ; il ne choisit pas la mission acceptée par le commerçant. Les
corrections des activités utilisent des libellés, des choix et des commandes de
réorganisation plutôt que des identifiants à saisir. Les identifiants existants
et les références des réponses sont conservés dans le contenu transmis.

Le mode **Aperçu joueur** simule la présentation de l'étape et de la mission
consultée : textes, illustration disponible, consigne et activité interactive.
Les consignes privées, préparatifs et lieux suivants ne sont pas injectés dans
cet aperçu. L'indice et la correction configurée peuvent être ouverts
explicitement par l'organisateur. Les cinq activités sont manipulables
localement ; aucune réponse, preuve, progression, acceptation ou correction
métier n'est envoyée au serveur. Le rendu publié demeure celui de Localeo Live ;
l'aperçu n'est pas une validation du jeu et le précise.

L'aperçu reste accessible en lecture seule, tandis que les commandes d'édition
suivent le droit existant. Aucun état d'interface, champ technique d'éditeur ou
essai de réponse n'est ajouté au JSON éditorial. L'enregistrement conserve son
contrat, ses versions attendues, la réconciliation des commandes et le contrôle
serveur. Les liens de continuité restent gérés par leurs identités serveur ;
une modification des étapes exige leur enregistrement avant édition de ces
liens, conformément à T5. Aucune migration ou évolution du générateur de
démonstration n'est nécessaire pour cette réorganisation de l'interface.

### T6-UX08 — Sélections et fil d’Ariane communs (E55-UX-08)

L’évolution du 24 septembre 2026 prend le Passeport commerçant comme référence
pour les trois modèles disponibles : Passeport, Tombola et Chasse. Les listes
disparates de commerçants et de coffrets deviennent des sélecteurs partagés,
en création comme en configuration : sélection explicite, éligibilité visible,
quantité et estimation des lots, boutons de consultation indépendants.
Le catalogue des commerçants est lu jusqu’à sa dernière page.

Le fil d’Ariane utilise le même composant : étapes numérotées reliées sur grand
écran, liste de navigation sur mobile, étape courante annoncée et navigation
au clavier. Les trois modèles partagent aussi la structure de la page de
création : en-tête, fil d’Ariane directement dessous, contenu de même largeur
qui défile séparément, et commandes de navigation en bas. L’aide Léo, le quota
et la bibliothèque de la Chasse restent dans le contenu ; ils ne déplacent
pas le fil d’Ariane à partir de l’étape Commune.
Les rubriques suivent les opérations réellement disponibles :
la Chasse recueille son brief avant génération, puis propose ses six rubriques
de préparation T6-UX06. Les coffrets restent configurés après création de son
brouillon. La navigation ne génère, n’enregistre et ne valide rien ; une étape
visitée n’est pas présentée comme une validation métier. Les saisies sont
conservées lors des retours et les commandes en cours ou incertaines bloquent
toujours la navigation concernée.

La fiche d’un commerçant s’ouvre dans une popin accessible sans changer la
sélection. Son contenu public est chargé à l’ouverture, avec chargement,
indisponibilité et réessai. La popin du coffret présente ses prestations,
descriptions et valeurs disponibles, et permet d’ouvrir la fiche du commerçant
associé. Échap ferme la popin et restitue le focus. Les champs absents ne sont
pas inventés, les réponses tardives après démontage sont ignorées et les
requêtes restent soumises à l’invalidation du contexte.

Les minima de sélection, seuils du Passeport, quantités, autorisations,
éligibilité et verrous financiers restent ceux des propriétaires existants.
Un coffret enregistré absent du catalogue reste visible et retirable lorsque
la modification est autorisée. Les détails restent consultables en lecture
seule. Les sélections de commerçants ne valent jamais acceptation.
À la demande de l’utilisateur du 24 septembre 2026, sélectionner un commerce
ne révèle plus le champ « Activité et particularités » et ne permet aucune
édition de sa fiche dans le brief. La consultation reste disponible en popin ;
l’adresse référentielle et son contrôle de complétude sont préservés. Les faits
existants d’une demande ou issus de la fiche restent transmis dans le contrat
actuel, sans être modifiés par un champ local.

Impacts : présentation et pagination dans `localeo-animation`, documentation
canonique ici ; contrats HTTP existants réutilisés, aucun changement des
commandes, permissions ou données persistées. Backend, Live et application
Commerçant sans modification ; migration et générateur de démonstration sans
objet car schémas, fixtures et règles métier inchangés. Déploiement frontend
compatible avec le backend courant, sans ordre coordonné supplémentaire.
Les preuves attendues couvrent navigation, sélection, consultation, refus et
conservation des saisies sur mobile et bureau, ainsi que la non-régression des
commandes de génération, de configuration et de paiement.

## Évolution du 24 septembre 2026 — kit commerçant et préparation du démarrage

Cette évolution prolonge EPIC 55 et le parcours d’invitation EPIC 56 sans modifier
leur bilan historique. Elle remplace la préférence de TRE-ARB-89 pour deux
alternatives par une seule proposition dans les nouveaux prompts Chasse.
Les critères et preuves propres à cette évolution sont suivis ci-dessous.

### Comportements attendus

- **E55-KIT-01 — Proposition unique.** Le prompt Chasse `1.2` demande exactement
  une mission par commerce ; son schéma exporté borne `missionsProposees` à un
  élément. Les résultats historiques à deux missions restent lisibles et
  importables. Un prompt déjà persisté reste immuable ; une révision explicite
  est nécessaire pour bénéficier de la nouvelle consigne.
- **E55-KIT-02 — Support joueur.** `supportAFournir` porte le texte destiné aux
  participants, accessible sur téléphone en scannant un QR de flyer. Ce texte
  exclut corrigés, consignes privées et lieux futurs. Les indices utiles au défi
  restent possibles. L’IA ne fabrique ni URL ni QR ; le backend produit ces
  supports depuis la mission retenue. Le marqueur explicite `supportAccessibleParQr: true` est nécessaire ;
  son absence conserve les anciens supports privés. Le QR de support reste distinct d’une
  preuve de présence : ouvrir une page ne valide pas une étape.
- **E55-KIT-03 — Kit privé.** Un commerçant dont l’invitation courante est acceptée
  télécharge depuis son application uniquement son kit : mode opératoire simple,
  flyer officiel de l’animation et supports de mission distincts. Depuis le
  correctif du 1er octobre 2026, `flyer-animation.pdf` est la copie binaire exacte
  du PDF officiel courant, s’il est publié et diffusable dans
  `APPLICATION_COMMERCANT` ; le kit ne le régénère pas et ne se replie pas sur
  une ancienne version si le document courant n’est pas diffusable.
  `support-mission.pdf` est ajouté uniquement lorsqu’un
  support public de mission est explicitement autorisé. Il peut préparer son
  commerce avant le lancement : avant publication ou sans flyer officiel
  disponible, le kit reste téléchargeable et le guide explique l’absence du
  flyer et la nécessité de télécharger à nouveau après publication. Aucun
  aperçu privé n’est inclus. Chaque téléchargement relit la version courante ;
  les ZIP déjà téléchargés restent inchangés. Le guide indique
  quoi télécharger, imprimer, installer, tester et comment accueillir les joueurs.
  Les autres commerçants et utilisateurs anonymes ne peuvent pas lire ce kit.
  Le support joueur applique une projection explicite, sans publication du kit.
- **E55-SUIVI-01 — Option à la création.** Les trois types d’animation proposent
  le suivi de préparation, désactivé par défaut. L’acceptation d’une invitation
  n’est jamais assimilée à une déclaration « prêt ». Les animations existantes
  conservent leur fonctionnement sans suivi.
- **E55-SUIVI-02 — Déclaration et suivi.** Seul le commerçant concerné, avec une
  invitation acceptée et encore participante, peut déclarer son commerce prêt.
  Le gestionnaire voit les déclarations datées et leur synthèse ; les répétitions
  ne produisent pas de doublon. Une invitation remplacée ne réutilise pas la
  déclaration précédente comme accord de préparation du nouveau contenu.
- **E55-SUIVI-03 — Barrière de démarrage.** Si le suivi est actif, tous les
  commerçants participants doivent être prêts avant ouverture effective du jeu.
  Le domaine backend applique cette règle au démarrage et aux accès joueurs,
  y compris lorsque la date de début est atteinte avec un statut `PUBLIEE`.
  Invitations refusées/annulées ne sont pas comptées comme participants ; les
  contrôles existants de consentement et minimum de commerces restent requis.
- **E55-SUIVI-04 — Forçage.** Le gestionnaire habilité peut lever explicitement
  la seule barrière de préparation, avec confirmation et motif tracé. Le forçage
  n’avance pas la date de début, ne publie pas un brouillon et ne contourne ni
  consentement, ni financement, ni contrôles terrain existants.

### Responsabilités et compatibilité

Le domaine Animation possède la règle d’ouverture. L’application charge les
invitations/déclarations, coordonne les écritures et l’audit ; les interfaces
présentent les décisions serveur. Le rendu des PDF, ZIP, QR et pages de support
appartient à l’infrastructure. La page de support dédiée ne modifie pas le moteur
Live et ne divulgue pas les autres étapes. Les médias privés ne deviennent pas
un catalogue public : seuls les éléments autorisés du support sont rendus.

La persistance du suivi est additive, avec défaut désactivé pour l’existant.
Livrer la migration et le backend avant les interfaces. Les prompts enregistrés,
accords et préparations historiques restent conservés. Les contrats canoniques
et embarqués des consommateurs sont exportés ensemble après implémentation.

### Matrice de traçabilité de l’évolution

| Critère | Propriétaire / comportement | Preuves prévues | Documentation / contrats | Fixtures / exploitation |
| --- | --- | --- | --- | --- |
| E55-KIT-01 | Service de préparation de prompt, aucune décision de consentement | Prompt déterministe, borne un, import historique conservé | Consigne 1.2, exemple documentaire identifié historiquement | Fixtures à deux missions conservées pour compatibilité ; aucune génération IA réelle |
| E55-KIT-02/03 | Projection applicative limitée ; adaptateur documents | Kit propre commerce, refus intercommerce, PDF imprimable/QR, public sans secrets ni mutation | API kit et support, guide commerçant | Artefacts locaux synthétiques ; aucun email ou document diffusé en environnement réel |
| E55-SUIVI-01/02 | Domaine et orchestration transactionnelle | Défaut sans suivi, déclaration acceptée, refus tiers/invitation non acceptée, répétition | Création et invitation, synthèse gestionnaire | Migration additive ; adaptation fixtures selon champs obligatoires |
| E55-SUIVI-03/04 | Domaine propriétaire de l’ouverture | Pas prêt refusé, tous prêts autorisé, forçage explicite tracé, dates et autres barrières préservées | Actions API et parcours Animation/Commerçant | Vérifier démarrage planifié et actions Live ; pas de déploiement implicite |

Les preuves locales ont été exécutées : le [suivi d’implémentation](suivi-implementation.md#e55-kit--e55-suivi--24-septembre-2026) consigne les commandes, résultats et limites. Cette validation locale ne vaut pas déploiement ni impression physique.

## E55-UX-09 — Préparation centrée sur le parcours (25 septembre 2026)

Direction validée par l'utilisateur : demander une génération, recevoir et
comprendre le parcours, configurer une étape à la demande, puis préparer le
lancement. Le gestionnaire n'intervient plus dans les échanges techniques avec
le générateur. Cette évolution remplace la navigation séquentielle T6-UX06 et
la hiérarchie initiale T6-UX07 ; elle conserve leurs règles métier.

### Critères et comportements

- **E55-UX-09-A** — Après le modèle, le brief commence sur Informations ; la
  commune active reste affichée et récapitulée. Aucun export/relecture de
  prompt ou requête, dépôt/import JSON, affectation opérateur ou acceptation de
  réponse technique n'est proposé dans Localeo Animation, même si la session
  possède les permissions correspondantes. Ces opérations restent dans l'ERP.
  L'attente, l'actualisation et la modification/annulation autorisée d'une
  demande sont formulées dans le vocabulaire du gestionnaire. La réception du
  résultat ERP rend directement le parcours consultable.
- **E55-UX-09-B** — Le parcours occupe la largeur disponible, sans conteneur
  central de largeur maximale. Étapes illustrées depuis leurs médias, numéros
  et liens montrent un ordre unique sans serpent ni défilement horizontal.
  Aucune étape n'est imposée à l'ouverture : la sélection ouvre l'aperçu joueur,
  puis Configurer donne accès à l'édition. L'inspecteur est latéral lorsque la
  largeur réelle le permet, avec retour au parcours sur petit écran. La
  fermeture rend le focus au déclencheur. Déplacement clavier, cinq activités,
  alternatives historiques et séparation des contenus privés sont conservés.
- **E55-UX-09-C** — Le parcours reste le support principal. Depuis le correctif
  du 31 octobre 2026, Configuration guide l'organisateur dans cinq étapes
  numérotées : Parcours, Organisation et lots, Commerces, Terrain, Publication.
  Une seule étape est visible ; retour et continuation explicites respectent
  cet ordre conseillé. Les autres étapes restent consultables sans validation
  implicite. La progression distingue les validations enregistrées du serveur,
  les contrôles restants, les prérequis à vérifier et les saisies non enregistrées.
  Le correctif E73 du 31 octobre 2026 remplace le panneau adjacent initial par
  une rubrique en pleine largeur, afin de préserver la lisibilité des formulaires
  ([présentation canonique](../epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md#51-deux-expériences-adaptées-à-leurs-usages)).
  Les panneaux visités restent montés et conservent leurs saisies.
  Le financement est accessible dans Organisation et lots, après les choix ;
  le gestionnaire est invité à attendre la stabilisation des participations.
  Toute saisie de paramètres non enregistrée empêche d'engager un paiement.
  Un retour du prestataire ouvre cette rubrique et son financement, sans
  attribuer de valeur probante à l'URL.
- **E55-UX-09-D** — Valider le parcours et continuer enregistre la relecture
  via la commande existante puis ouvre Organisation et lots après résultat
  confirmé, avant Commerces, depuis le correctif du 31 octobre 2026.
  Cela n'envoie aucune invitation. La sélection groupée ne concerne que les
  demandes à envoyer ; le gestionnaire peut retirer un destinataire et envoie
  explicitement le groupe avec son décompte. Un refus permet de revenir adapter
  le parcours. Le contrôle de publication se charge à l'ouverture ; les erreurs
  restent visibles, et publier exige toujours une confirmation explicite.
- **E55-UX-09-E** — Navigation, aperçu et sélection ne créent ni consentement,
  ni publication, ni paiement. Relecture du parcours même sans retouche,
  contrôles terrain, checklist et déclaration prêt restent distincts. Saisies
  non enregistrées bloquent la publication ; commandes en cours/incertaines
  conservent leur résolution accessible, sans répétition automatique. Permissions,
  clés et versions restent celles du backend. Les animations publiées ne sont
  pas présentées comme prêtes sur la seule base de leur réception ou visite.

L'allègement des attestations exige de définir la preuve et son propriétaire
de remplacement. Une prévision précise, avant sauvegarde, des commerces dont
l'accord sera invalidé nécessite une décision du domaine ou un contrat d'aperçu.
Ces deux extensions restent ouvertes, sans calcul local de consentement ni
suppression silencieuse d'un invariant. Aucun changement de domaine n'est
nécessaire pour le lot d'interface ci-dessus.

### Impacts et traçabilité

Sources de départ : Animation `48c05875a5c8c36820063becd7fbb20d8332f38c`,
backend `d106f273758b71de33167ae41cb66e2b67c391b9`, projet
`446fa7c48b01b24a5388aabebc7820f2a500fc0a`. Modifications utilisateur dans les
guides/skills du projet préservées. Le backend reste propriétaire de la
relecture (`revision_relue`), du consentement, du financement et de la publication.

| Critères | Preuves prévues | Documentation / contrats | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- |
| A | Génération simulée reçue de l'ERP, absence outils même avec droits, adresses/quota/reprise | Guide moteur ; commandes API inchangées | Adapter fixtures navigateur ; schéma générateur inchangé | Interface Animation seule ; ERP existant requis pour traiter les demandes |
| B | Desktop/mobile, largeur réelle, clavier, cinq activités, aucune écriture en aperçu | Conception et guide ; aucun export de contrat | Médias synthétiques locaux, aucun nouvel asset produit | Bundle frontend ; ni migration ni configuration supplémentaire |
| C | Saisies conservées, paiement bloqué avant sauvegarde, retour prestataire sans écriture | Guide d'exploitation moteur | Recettes API simulées, aucun paiement réel | Serveur seul autorité financière, aucun déploiement implicite |
| D, E | Destinataires exacts, relecture, réponse perdue, publication et droits | Contrats/reçus existants conservés | Invitations fictives ; générateur sans impact car données/états inchangés | ERP, Commerçant et Marketplace non modifiés ; aucun effet sur jeu publié |

Les résultats réels et limites figurent dans le suivi d'implémentation.

## E55-UX-10 — avancement de la préparation (26 septembre 2026)

Demande : montrer au gestionnaire ce qui reste à faire dans Parcours,
Organisation et lots, Commerces et Terrain. Le correctif du 31 octobre 2026
remplace la jauge adjacente par les états du parcours guidé, à partir de la
même projection serveur.
L'indicateur mesure les contrôles de préparation enregistrés, jamais les visites
de rubriques, le temps passé ni la publication effective.

### Critères d'acceptation

- **E55-UX-10-A** — Les cinq étapes sont numérotées, avec un état accessible.
  La coche verte **Validée** exige les contrôles applicables tous `VALIDE` ;
  une visite ou une sauvegarde partielle ne la produit pas. Un contrôle absent
  ou inconnu reste à actualiser/vérifier ; un total nul est **Sans objet**.
  Le contrôle final de publication demeure **À confirmer**, jamais publié sur
  la seule base de la progression. Sur mobile, numéros et pictogrammes gardent
  les cinq accès ; le titre et l'état de l'étape active sont lisibles en clair,
  avec états accessibles des autres étapes et sans défilement horizontal.
- **E55-UX-10-B** — Le détail présente les contrôles restant à effectuer et les
  messages serveur, avec accès à chaque rubrique et au bilan de publication.
  Un contrôle en attente d'un prérequis reste « à vérifier » et n'est jamais
  compté valide. Les contrôles non applicables sont exclus du total. Les
  blocages généraux restent visibles même si les préparatifs sont complets.
- **E55-UX-10-C** — Le bilan se relit à l'ouverture, après sauvegarde, lors du
  changement de rubrique et après résolution d'une action bloquante. Une
  actualisation manuelle permet de récupérer une réponse commerçant externe.
  Aucun polling d'attente humaine. Chargement, erreur et action en cours ne
  montrent aucun pourcentage périmé ; une réponse d'un ancien contexte est
  ignorée. Les saisies non enregistrées sont signalées et ne font pas progresser
  la jauge. Une erreur de lecture peut être réessayée sans mutation.
- **E55-UX-10-D** — Le serveur reste propriétaire des accords, vérifications,
  financement et conditions de publication. La lecture de progression est
  accessible avec `animation:generation_lire`, dans le tenant actif, sans
  exiger le droit de publier. Cent pour cent n'effectue aucune publication et
  ne contourne ni ses droits ni sa confirmation. Le bouton de publication
  conserve son contrôle serveur indépendant.

### Projection et contrat

`GET /protected/animation-locale/animations/{id}/preparation/avancement`
est une lecture privée sans effet de bord. Sa projection applicative réutilise
les anomalies de l'assemblage de Chasse et les évaluations de participation,
financement et publication ; elle ne crée pas de nouvelle règle métier.
Les validations métier restent dans leurs propriétaires existants du domaine.

Le contrat expose `animationId`, `version`, `statut`, `valide`, `valides`,
`total`, `pourcentage`, `rubriques` et `blocages`. Chaque rubrique possède des
contrôles nommés, un statut `VALIDE`, `A_FAIRE` ou `A_VERIFIER`, et des actions
décrites par `code`, `message`, `chemin`. Le pourcentage global est le rapport
des contrôles valides aux contrôles applicables, et non une moyenne des quatre
rubriques. Les anomalies inconnues ne disparaissent pas : elles restent des
blocages généraux. L'absence de préparation ne valide pas implicitement les
contrôles dépendants qui n'ont pas encore pu être évalués.

### Impacts et preuves prévues

| Périmètre | Impact et preuve |
| --- | --- |
| Backend | Projection et route privée ; tests préparation absente, partielle, complète, dépendances invalidées, droits/tenant et contrat ; garde-fous architecture. |
| Animation | Client API et jauge ; navigateur bureau/mobile, navigation sans écriture, erreurs, brouillons et réponses tardives ; types, lint et build isolé. |
| Contrats | Export canonique et contrat embarqué Animation synchronisés ; ajout compatible, aucune commande modifiée. |
| Documentation fonctionnelle et ops | Présente section, backlog, suivi et guide du moteur ; livrer le backend avant le frontend pour rendre la lecture disponible. |
| Marketplace, Commerçant, ERP | Aucun consommateur de la nouvelle lecture ; commandes et projections existantes conservées. |
| Migrations et démonstration | Sans impact : aucun stockage ni état métier ajouté ; fixtures synthétiques adaptées aux tests, générateur inchangé. |

Le statut de l'epic reste En cours. Les preuves exécutées et limites sont
consignées dans le suivi d'implémentation.

## E55-UX-11 — Terrain simplifié (26 septembre 2026)

Décision utilisateur : la préparation doit faire gagner du temps au gestionnaire
de collectivité ou d’association. Les fiches de vérification de chaque mission,
les formulaires de visite POI et les cinq rubriques commentées de la checklist
organisateur sont supprimés du parcours et des conditions de publication.
Deux blocs les remplacent, sans deux nouvelles attestations obligatoires.

### Critères et règles conservées

- **E55-UX-11-A — Deux blocs utiles.** « Supports à installer » donne accès aux
  QR des lieux physiques du parcours ; le gestionnaire peut préparer, consulter
  et télécharger le support utile. « Préparation des participants » affiche les
  déclarations des commerces lorsque le suivi est actif, avec détail à la demande.
  Aucun responsable, auteur/date de visite, observation ou validation par lieu
  n’est exigé. Les conseils horaires, accès, trajet et consignes restent facultatifs.
- **E55-UX-11-B — Publication cohérente.** L’absence ou l’obsolescence d’une
  vérification mission, POI ou checklist ne bloque plus la compilation ni la
  publication. Le domaine reste propriétaire des accords valides, minimum de
  commerces, demandes en attente, références/version des lieux, QR nécessaires,
  contenu jouable, règlement, dates et financement. Rien n’est accepté ni publié
  automatiquement. Les contrôles spécifiques d’une modification de période ou
  capacité après publication restent distincts ; ils ne doivent plus dépendre
  d’un ancien dossier de vérification prépublication.
- **E55-UX-11-C — Avancement utile.** La projection d’avancement retire les
  vérifications supprimées de ses contrôles et de son dénominateur. Elle ne les
  transforme pas en contrôles « validés ». Les QR requis continuent à alimenter
  Terrain ; une commande QR confirmée actualise le bilan. Le compteur de commerces
  prêts relève du suivi facultatif de démarrage et ne crée aucun nouveau blocage
  de publication ni double confirmation par le gestionnaire.
- **E55-UX-11-D — Droits et reprise.** Préserver les permissions, versions,
  idempotence et reçus des QR, ainsi que l’activation à la publication. Une réponse
  incertaine impose la réconciliation existante, jamais une répétition automatique.
  L’interface reste utilisable au clavier et sur mobile ; une erreur ne signifie
  ni « aucun support » ni « tous prêts ». Aucune ancienne saisie n’est effacée.

### Décisions remplacées et compatibilité

Cette section remplace la portée **bloquante avant publication** de T3-D03,
de la préparation vérifiée prévue par TRE-ARB-89 et de la checklist évoquée dans
E55-UX-09. T3-D04 (supports QR), les accords et E55-KIT/E55-SUIVI restent applicables.
Les observations/dossiers historiques et leurs commandes peuvent rester
consultables via les anciennes interfaces/API ; leur présence ne vaut plus
condition de publication. Aucun document de visite ni accord fictif n’est créé.

Le changement porte sur le domaine de compilation, ses faits applicatifs,
les consommateurs de l’évaluation après publication et la projection de jauge.
Les interfaces consomment ce résultat sans réimplémenter le choix des blocages.
Le DSL publié et les preuves des joueurs ne changent pas.

La suppression des fiches POI conserve la vérification automatique de leur QR :
`qr_correspond_au_lieu` dans le domaine exige identité et édition courantes,
en statut préparé avant publication et actif lors des contrôles applicables
après publication. Modifier un POI impose donc de préparer son nouveau support,
sans formulaire de visite. Les contrôles spécifiques `requiredVerifications`
des modifications de période/capacité restent inchangés.

### Matrice des impacts et preuves prévues

| Périmètre | Impact et preuve |
| --- | --- |
| Domaine backend | Publication sans anciens dossiers, données historiques obsolètes tolérées ; accords/QR et autres refus préservés. |
| Application backend | Assemblage et exploitation compatibles, projection sans jalons supprimés ; tests d’orchestration et garde-fous d’architecture. |
| Animation | Deux blocs, guide facultatif, QR et suivi existants ; tests navigateur mobile/bureau, erreurs, lecture seule et commande perdue ; types/lint/build isolé. |
| API et consommateurs | Formats et anciennes routes conservés ; changement de sémantique des contrôles de publication, sans champ obligatoire nouveau. Marketplace et Commerçant conservent leurs contrats et leurs règles de jeu/préparation. |
| Données et migrations | Aucun état stocké ajouté ou supprimé ; anciennes saisies conservées, aucune migration. |
| Démonstration | Générateur examiné : scénarios de moteurs classiques, aucune fabrication de fiche terrain Chasse ; pas de modification nécessaire. Tests isolés du générateur inclus dans la validation ciblée, aucune génération réelle exécutée. |
| Fonctionnel et exploitation | Guide gestionnaire, recette, backlog et présent document actualisés ; backend à livrer avant le frontend. |

Les preuves exécutées et les limites figurent dans le suivi d’implémentation.

## E55-UX-12 — Supports par responsable (26 septembre 2026)

Décision utilisateur : l’installation dans un commerce appartient au commerçant.
E55-UX-11-A/C exposait encore tous les QR dans Terrain, avec une préparation
manuelle gestionnaire. La cible supprime cette tâche pour les étapes commerçantes
et conserve les supports des lieux publics à la charge du gestionnaire.

### Critères et invariants

- **E55-UX-12-A — Gestionnaire.** « Supports des lieux publics » présente seulement
  les étapes POI. Sans POI, ce bloc est absent ; une lecture échouée reste une
  erreur visible. Le suivi facultatif des commerces reste accessible, sans
  nouvelle checklist ni attestation.
- **E55-UX-12-B — Commerçant.** Accepter une mission Chasse prépare dans la même
  transaction son QR de lieu. Le kit fournit `qr-lieu.pdf` pour sa propre étape,
  à scanner depuis Localeo Live. Depuis le correctif du 1er octobre 2026,
  `flyer-animation.pdf` reprend le flyer officiel d’inscription et
  `support-mission.pdf` porte l’URL du support public explicitement autorisé,
  lorsqu’il existe. Le guide de mission reste privé. Ces usages ne sont pas
  interchangeables. Télécharger plusieurs fois
  réutilise le support valide ; cela ne confirme jamais « Je suis prêt ».
- **E55-UX-12-C — Reprise.** Les accords historiques sans QR peuvent préparer
  leur support lors du clic « Télécharger mon kit », sans bouton technique
  supplémentaire. Une commande explicite, versionnée et idempotente réalise
  cette écriture ; les GET de métadonnées et de ZIP n’en effectuent aucune.
  Après résultat incertain, le frontend relit l’état ; il bloque la répétition
  jusqu’à réconciliation, conserve l’intention si elle reste valable et exige
  une nouvelle intention après conflit. Les réponses d’un ancien compte sont ignorées.
- **E55-UX-12-D — Cohérence.** Le domaine conserve l’accord courant, la mission
  choisie, le commerce et l’étape associés, les versions, le statut du QR et la
  configuration publiée applicable. Un QR d’un autre commerce ne doit jamais
  être livré. Refus, retrait accepté et accès étrangers restent interdits.
  L’activation à la publication est conservée ; aucun QR actif valide n’est
  remplacé au téléchargement. Les QR commerçants manquants alimentent Commerces
  (`QR_COMMERCANT_NON_PREPARE`), les POI Terrain (`QR_LIEU_NON_PREPARE`).

### Contrat et responsabilités

Sous `/protected/animation-locale/commercants/me/animations/{animationId}` :

| Opération | Contrat |
| --- | --- |
| `GET /kit` | Métadonnées existantes plus `qrLieuPret: boolean \| null` ; `null` hors mission Chasse, `false` si le support doit être préparé, `true` s’il est restituable. `version` reste la version de demande de participation. |
| `POST /kit/preparer` | Corps fermé `{expectedVersion}`, en-tête `Idempotency-Key` requis ; réponse `{animationId, version, qrLieuPret: true}`. Ne modifie pas la version de l’accord. |
| `GET /kit/download` | ZIP privé ; aucune écriture et refus si le QR requis ne peut pas être restitué. |

Le domaine décide de l’éligibilité et de la cohérence ; l’application orchestre
verrous, signature, persistance et rendu. Routes et interfaces ne recréent pas
ces règles. La décision, le QR et le reçu doivent réussir ou échouer ensemble.
L’ordre des verrous est animation puis demande, compatible avec publication et
édition. La commande historique vérifie également la définition effective d’une
animation publiée et les étapes neutralisées. Un changement de clé de signature
ne provoque aucune rotation silencieuse lors d’une lecture.

### Impacts et preuves

| Périmètre | Impact et preuve attendue |
| --- | --- |
| Backend domaine/application | Acceptation et QR atomiques, rejeu stable, mauvais compte/accord obsolète refusés, préparation historique avant/après publication, lectures pures, QR réel dans le PDF, jauge correctement attribuée. |
| Commerçant | Un téléchargement prépare au besoin le support ; double clic, réponse perdue, conflit, ancien compte et confirmation « prêt » indépendante ; tests unitaires et navigateur bureau/mobile. |
| Animation | Sélection POI seule, bloc absent sans POI, droits et erreurs conservés ; tests navigateur, types/lint/build. |
| Contrats/lecteurs | OpenAPI canonique et copies frontend actualisés ; aucune nouvelle commande joueur ni modification du DSL. Marketplace conserve les mêmes QR et règles de scan. |
| Stockage | Réutilisation des QR et reçus existants, aucune migration ni suppression d’historique. |
| Démonstration | Générateur classique sans mission Chasse : pas de nouvelle donnée obligatoire ; fixtures de tests adaptées, aucune génération réelle demandée. |
| Guides et exploitation | Répartition des rôles et distinction des supports documentées ; backend puis Commerçant avant Animation pour ne pas masquer le parcours historique sans remplacement disponible. |

Les preuves exécutées et limites figurent dans le suivi d’implémentation.

<a id="e55-audit-20261113"></a>
## Évolution du 13 novembre 2026 — fiabilité, parcours et capacité

**Conception à implémenter**, issue de l'audit Animation/ERP/Live du même jour.
Les [critères E55-A01 à A14 et OPT-01 à OPT-06](../../roadmap/en-cours/epic-55-chasse-tresor-commercante-backlog.md#e55-audit-20261113)
conservent leurs repères ; le [complément fonctionnel](localeo_animation_engine_spec.md#e55-audit-20261113)
décrit les résultats visibles. Les preuves antérieures sont un état de départ,
pas une validation de cette cible. Les anomalies relèvent de correctifs ciblés,
les extensions de contrat et études de leur propre lot.

### Propriétaires et invariants conservés

| Périmètre | Propriétaire / entrées | Invariant et refus à préserver |
| --- | --- | --- |
| A01 — inscription | Domaine `animation_locale`, protocole `reprise_inscription`, orchestration `ServiceParticipantsAnimation.inscrire` ; formulaire Live et route publique existants | Unicité animation/email normalisé, dates/capacité, déclaration adulte et règlement Chasse. Même intention incertaine : clé UUID v4 et empreinte identiques, reçu existant de 24 h ; pas de seconde place après panne du carnet. |
| A02/A03 — commandes et saisies | Domaine du service de préparation pour décisions/versions ; client HTTP ERP et composants pour état éphémère | Pas de transition sur une simple lecture, de double effet, de sauvegarde silencieuse ni de reprise avec un autre payload. Changement d'identité/commune invalide les réponses et données privées de l'ancien contexte. |
| A04 — limitation | Domaine/service `identite_acces` et adaptateurs HTTP/persistance | Limiter le coût avant accès personnel puis autoriser avant compteur personnel ; refus non révélateurs, compteur atomique, pas de clé persistante choisie par UUID arbitraire. |
| A05 — qualification et gel | Moteur `execution` et services d'exploitation/clôture ; API organisateur/ERP, traitements existants | La qualification et la population figée proviennent du domaine. Une projection SQL ne réinvente ni neutralisation, ni preuve, ni chance ; gel cohérent même sous scan/correction concurrents. |
| A07/A10/OPT-03 — lectures | Services de génération/catalogue, ports de lecture et adaptateurs ; ERP, Animation et Live | Droits avant filtre/limite, lecture sans mutation, liste bornée, métadonnées publiques issues de la définition publiée, aucune étape future privée. |
| A06/A08/A09/A11/A13/A14 | Interfaces et clients HTTP, sans nouvelle règle métier | Chargement/erreur/vide distincts, refus serveur prioritaires, interaction accessible ; pas d'aide débloquée par une erreur de formulaire ou de progression fabriquée localement. |

### A01 — inscription et accès temporaire sans carnet

Chemin actuel à couvrir de bout en bout : `LiveRegistrationGuard` et
`LiveAnimationDetail` → `AnimationRegistrationForm` →
`POST /public/animation-locale/animations/{id}/inscriptions` →
`/live/animations/ajouter/{token}` (`AddAnimation`) → jeu. Le dernier maillon
lit/écrit également IndexedDB : débloquer seulement le formulaire est insuffisant.

La cible réutilise le contrat d'inscription existant. L'absence de lecture du
carnet est un état technique distinct d'une participation reconnue. Après succès
serveur, l'ajout au carnet est tenté séparément ; son échec offre un accès
personnel temporaire en mémoire, selon le modèle déjà présent dans
`AnimationParticipantPage.jsx`, et une récupération par le lien personnel.
Ne pas annoncer « ajouté au carnet » si l'écriture a échoué, ni introduire un
second stockage persistant ou un nouveau token. Réutiliser les protections de
nettoyage d'URL, logs, session, non-cache et revalidation des accès.

Le point d'entrée temporaire reste dans `AddAnimation` : après résolution du
token par le serveur, « Participer sans enregistrer » construit en mémoire
l'entrée attendue par `LiveAnimationGame`, comme `AnimationParticipantPage`.
Aucune nouvelle route HTTP ni URL contenant un accès supplémentaire. Fermer
le jeu revient à l'aperçu vérifié ; quitter le composant ou changer de token/
contexte efface cet état. L'interface indique que le lien personnel permettra
de revenir, mais que le carnet ne retrouvera pas automatiquement cette entrée.
Un refus ou une expiration de l'accès retire immédiatement aperçu et jeu.
Les contrôles serveur habituels restent requis pour chaque action sensible.

| État | Action disponible / résultat |
| --- | --- |
| Lecture du carnet impossible, inscription non confirmée | Formulaire autorisé et récupération restent disponibles ; aucune participation déduite de l'erreur locale. |
| Inscription au résultat incertain | Réconciliation/reprise exacte ou récupération ; pas d'entrée de jeu construite depuis une hypothèse de succès. |
| Inscription ou accès personnel confirmé, écriture locale impossible | Accès temporaire explicite au même jeu ; réessayer l'enregistrement est indépendant et ne répète jamais l'inscription. |
| Enregistrement local confirmé | Accès habituel au carnet ; message de réussite uniquement après écriture. |
| Accès serveur refusé/expiré | Récupération autorisée par le protocole actuel ; aucun mode local contournant le refus. |

Le doublon serveur conserve le **409** ; le renvoi du lien conserve le **202
générique**, sans révéler l'inscription à un tiers, et envoie seulement à
l'adresse enregistrée. Une réponse perdue conserve la même intention dans la
limite du mécanisme actuel ; après perte de cette intention ou expiration du
reçu, proposer la récupération, sans recréer silencieusement une inscription.
La correction d'un composant partagé doit préserver Passeport et Tombola ;
elle n'étend pas la déclaration adulte Chasse ni le protocole spécifique de
vérification email Tombola publique E74.

### A02/A03/A06/A08 — états locaux et réconciliation

Dans l'ERP, `preparations-service.js` et `travail.js` doivent partager la
résolution de la commande exacte. Une confirmation de reçu vérifie contexte,
clé, ressource et enveloppe avant de libérer le verrou HTTP correspondant.
Un autre reçu, une réponse tardive ou un refus ne le libère pas. Les autres
commandes peuvent ensuite démarrer avec une nouvelle clé ; pas de remise à
zéro globale du verrou et pas de rejeu automatique. Le contrat serveur de
reçu n'est pas modifié par ce correctif.

Le client commun expose une résolution explicite de la commande en attente,
par exemple `confirmerRecu(commande, contexteRevision, recu)`. Sa signature
comprend chemin, méthode, payload canonique, clé d'idempotence et révision
d'accès ; le reçu doit provenir de la lecture réussie de cette même clé et
correspondre à l'opération et à sa préparation. L'appel consomme au plus le
verrou correspondant ; un GET quelconque ne nettoie jamais tous les verrous.
Une confirmation reçue suivie d'un échec de rafraîchissement libère la commande
confirmée et présente une erreur de lecture, sans recréer une incertitude.

Le module métier utilise le résultat `incertain` du client commun pour garder
ou retirer son état local, et non une approximation `status < 500`. Les cas
408, 429 et conflit d'idempotence doivent conserver une décision cohérente
entre les deux couches. Une validation locale avant envoi ne crée aucun verrou ;
une réponse de succès mal formée n'atteste pas le résultat et exige un reçu.

Le brief modifié est distinct de l'état serveur et de la réponse IA saisie.
Actualiser le suivi conserve les champs en cours ; changer de dossier,
paginer ou quitter déclenche la protection si la saisie serait perdue. Un
conflit de version conserve la saisie pour résolution explicite. Les gardes
de session conservent la priorité et ne doivent pas laisser visible un ancien
tenant. Pas de persistance privée supplémentaire dans Animation/ERP.

Les lectures indépendantes quota, suivi, résultat et préparation ne forment
pas une barrière unique. Une panne de quota interdit l'action dépendante sans
masquer le résultat autorisé. Les invitations conservent un état inconnu ou le
dernier état explicitement daté ; une réussite efface l'erreur. Un refus de
droits efface la donnée privée, même si une version précédente était visible.

### A07 — recherche serveur de la file ERP

Chaîne réelle : `generation_animation.html` →
`GET /{internal|protected}/animation-locale/generations` →
`ServiceGenerationAnimation.lister` → `lister_operations` du repository.
La pagination SQL existante est par `(created_at ASC, id ASC)`, défaut **50**,
maximum **100** ; elle est conservée pour les appels historiques.

Contrat cible additif : paramètre facultatif `q`, absent/vide = aucun filtre.
Réutiliser `normaliser_recherche` du domaine commercialisation : Unicode NFKD,
retrait des marques combinatoires, `casefold`, blancs internes regroupés et
blancs de bord retirés. Une requête textuelle normalisée contient de **3 à 120 caractères**.
Elle recherche une sous-chaîne du nom public de l'animation ou du code/libellé
de son type ; un UUID complet recherche l'identifiant exact de la demande.
Ne pas rechercher dans prompts, réponses, emails ou contenus privés. Une
recherche non vide trop courte/longue est signalée dans l'ERP et refusée en
**422** côté API ; aucune troncature silencieuse. Les accents ne sont donc pas
significatifs (`été` trouve `Été`). Cette décision remplace le choix provisoire
NFKC/accents significatifs de l'intégration du rapport et aligne la file sur
la recherche existante. Échapper `%`, `_` et `\` comme caractères littéraux
avant le prédicat SQL ; ils n'ouvrent pas une recherche par joker.

Tous les filtres existants et droits sont appliqués avant recherche et limite.
Lire au plus `limit + 1` racines, enrichir seulement la page ; la réponse reste
`PageGenerationPayload {items, nextCursor}`. L'ERP demande explicitement 25
résultats, déclenche la recherche à validation, réinitialise le curseur et
ignore les réponses anciennes. Il conserve un historique borné de curseurs,
sans concaténer toutes les pages de résultats en mémoire.

Un curseur versionné lie ordre, recherche normalisée, filtres et empreinte du
périmètre autorisé. Il n'accorde aucun droit ; les droits sont relus à chaque
page. Un curseur incompatible est refusé et l'interface propose de reprendre
la première page. Transition : anciens curseurs date/ID acceptés uniquement
sans `q` selon leur contrat historique, avec recontrôle du périmètre, puis
réémission au format courant ; une recherche avec ancien curseur est refusée.
L'interface réinitialise toujours la pagination au changement de filtre.

Réutiliser `AnimationOrm.nom_recherche`, son entretien sur écriture et sa
réparation paginée existante (`projection_recherche_animation.py`). La migration
existante `v276` fournit `pg_trgm`, l'index GIN des noms normalisés et l'index
des valeurs absentes : aucune seconde colonne ni second index équivalent.
Le code/libellé de type se résout dans le catalogue fini des types ; aucun
chargement exhaustif des animations pour ce filtre. Si la projection requise
manque dans le périmètre recherché, refuser explicitement la recherche en 503
jusqu'à réparation ; ne pas masquer des dossiers ni reconstruire pendant GET.

Conserver les index d'opérations par ressource, tenant/commune et `(created_at,
id)` ; vérifier leurs combinaisons avec le GIN par `EXPLAIN (ANALYZE, BUFFERS)`
à N/10N, recherche rare/sans résultat et plusieurs tenants. Un index additionnel
ne se justifie que par un plan insuffisant mesuré, avec migration additive.
Un `ILIKE` suivi de `LIMIT` sans preuve de plan ne clôt pas A07. La sous-chaîne
reste le comportement demandé, même si une recherche par préfixe serait moins coûteuse.

### A10 — informations publiques d'effort

`ProjectionPublique` possède déjà les agrégats camelCase, mais le catalogue
effectif retourne `AnimationPubliquePayload`, assemblé par
`catalogue_animations_publiques.py`. C'est ce producteur et les normalisations
Live qui doivent évoluer, pas seulement le schéma du moteur.

| Champ HTTP ajouté à `AnimationPubliquePayload` | Source publiée / sens |
| --- | --- |
| `duree_estimee_minutes: integer > 0 \| null` | `ProjectionPublique.dureeEstimeeMinutes`, `engineConfig.settings.estimatedDurationMinutes` ; estimation indicative. |
| `difficulte: string \| null` | `ProjectionPublique.difficulte`, `settings.difficulty` ; borne du type existant `Titre`, aucune nouvelle échelle inventée. |
| `public_vise: string \| null` | `ProjectionPublique.publicVise`, `settings.audience` ; borne du type existant `Texte`, texte rendu sans HTML exécutable. |
| `nombre_etapes: integer > 0 \| null` | `ProjectionPublique.nombreEtapes`, nombre d'étapes de la définition publiée, départ/finale inclus s'ils sont des étapes. |

Les quatre propriétés sont facultatives et nullables pour données anciennes,
ancien serveur et autres moteurs. Les champs camelCase du contrat moteur ne
sont pas renommés ; le mapping vers le catalogue est explicite et testé.
Le nombre annoncé décrit le parcours publié de référence, pas les étapes
restant à un joueur ni un recalcul client après neutralisation ; l'avis existant
de parcours adapté et la progression personnelle restent autoritaires dans le jeu.
Le catalogue utilise la configuration désignée par `configuration_publiee_id`,
déjà jointe dans sa requête. Projeter en SQL les scalaires JSON nécessaires
et le nombre d'étapes de cette définition, puis contrôler les types avec les
règles de `ProjectionPublique` : entier strict positif, `Titre` non vide de
200 caractères maximum, `Texte` non vide de 20 000 caractères maximum.
Une propriété absente/incompatible devient `null`, jamais une valeur devinée.
Le DTO reste petit : pas de chargement du DSL ou des médias complets par
résultat, ni de N+1. Pas de nouvelle table de métadonnées pour cet ajout.

Producteurs concernés : liste/détail publics Animation et entrées de découverte
Live réutilisant le catalogue. Consommateurs : `fetchPublicAnimations`,
`fetchPublicAnimation`, `normalizePublicAnimation`, découverte/fiche/inscription.
Les anciens payloads restent affichables sans valeurs fictives. Pas de
modification du DSL, de sa version ni des participations jouées pour ce seul ajout.

Les schémas Python restent la source exécutable. À l'implémentation, générer
hors ligne avec `scripts/documentation/generate_epic41_openapi.py` et
`generate_epic42_openapi.py` les contrats canoniques
[E41](../epic-41-api/openapi.json) et [E42](../epic-42-localeo-live/openapi.json),
puis synchroniser les contrats embarqués effectivement consommés et vérifier
leurs lecteurs. `export_moteur_animation_contracts.py` seul ne corrige pas le
catalogue. Cette phase ne modifie pas les JSON générés pour prétendre que
les nouveaux champs sont déjà servis.

### A04 — protection des lectures Live

Routes : `GET /public/localeo-live/participations/{id}` et
`/{id}/lieu-courant/pratique`. Le défaut observé est une création de fenêtre
par UUID avant autorisation, pas une fuite de données prouvée.

**Stockage retenu : PostgreSQL partagé**, avec transactions courtes ; aucune
autorité en mémoire de processus ni dépendance Redis ajoutée. La politique
pure appartient au domaine `identite_acces`, le service orchestre un nouveau
port `LimitationLecturesLiveRepository`. Le repository d'authentification
actuel ne porte pas atomiquement capacité/purge ; les limites LOGIN existantes
ne changent pas. Deux tables additives, avec identifiants de migration attribués
au moment de l'implémentation :

- `limitation_lectures_live_controle` : une ligne, version de politique,
  seuils/durées, capacités par catégorie, nombres alloués, fenêtre et consommation
  globales ; compteurs positifs, capacités strictement positives.
- `limitation_lectures_live_compteurs` : clé primaire `(categorie, cle_hash)`,
  début/fin de fenêtre et consommation. Catégories fermées `ORIGINE`,
  `PARTICIPATION_LECTURE`, `PARTICIPATION_PRATIQUE` ; index de purge sur
  `(fin_fenetre, categorie, cle_hash)`. Une ligne réutilisée par clé, sans
  historique des fenêtres ; les lignes expirées comptent dans la capacité
  jusqu'à suppression transactionnelle.

Protocole commun aux deux routes, sur tous les processus :

1. Avant autorisation, ouvrir une transaction, verrouiller la ligne de contrôle
   puis la clé d'origine, dans cet ordre. Lire l'horloge PostgreSQL après le
   verrou ; vérifier/consommer le budget global puis celui de l'origine.
   La clé d'origine ne dépend ni de la route, ni de l'UUID demandé, du Bearer
   ou de l'email. Un refus d'origine consomme le budget global ; retourner
   une décision, **committer avant de lever le refus HTTP**, sans rollback de
   la consommation. Les compteurs saturent au seuil, sans prolonger la fenêtre.
2. Autoriser le Bearer et la participation selon les règles actuelles. En cas
   de refus, aucun compteur personnel n'est créé. Hors limitation, les mêmes
   401/404/410 restent observables, sans oracle d'existence nouveau.
3. Après autorisation seulement, une seconde transaction suit le même ordre
   de verrous et consomme la clé `(participation autorisée, origine, route)`.
   Conserver le plafond personnel de **60 lectures par 900 secondes et par
   route**. Ne pas consommer deux fois le budget global dans cette phase.
4. Exécuter la lecture métier après libération des verrous du limiteur.
   Une indisponibilité du stockage, un verrou en timeout ou une politique
   absente/incohérente refuse la lecture en **503** ; aucun passage sans limite.

Une nouvelle clé exige une place libre dans sa catégorie. À saturation,
purger au plus **64** lignes expirées dans la transaction avant de réessayer ;
sinon **429**, sans éviction d'une fenêtre active. Les clés déjà allouées
restent utilisables dans leurs budgets. Le scheduler existant reçoit le batch
`live.lectures.purger` toutes les minutes, par transactions de **500** lignes
maximum, même ordre de verrous et décrément des allocations atomique. Un
redémarrage ne réinitialise pas les fenêtres. La mise à jour de politique
ne vide pas les compteurs ; abaisser une capacité sous l'allocation existante
est refusé. Un changement de durée s'applique aux prochaines fenêtres, sans
prolonger ou réouvrir celles en cours.

La réalisation expose une route interne POST authentifiée par `internal:batch`,
sans session ERP, et un CLI opérateur explicite. Ce batch technique ne déclare
pas de lancement manuel ERP ; son contrat de sécurité et son passage dans le
middleware complet sont vérifiés. La migration `v317` écrit la conversion de
catégorie en texte explicitement pour conserver une contrainte identique après
dump/restauration PostgreSQL, sans changer les catégories admises.

L'origine vient de `request.client.host` après traitement des seuls proxies
explicitement approuvés par ASGI ; ne pas lire arbitrairement `X-Forwarded-For`.
Normaliser IPv4 et IPv4 mappée IPv6, regrouper IPv6 par /64 ; origine absente/
invalide = une clé `UNKNOWN`. Les empreintes sont des données pseudonymes,
pas anonymes : conservation limitée aux fenêtres/purge, jamais de Bearer.
Les refus comportent `Cache-Control: no-store` ; **429** fournit `Retry-After`
jusqu'à la fenêtre bloquante, ou la prochaine expiration libérant une place
si la capacité empêche l'allocation. Une panne interne 503 ne révèle aucun
identifiant ni détail de participation.

Politique **de recette synthétique, à ne pas activer telle quelle en production** :
global 6 000/60 s, origine 600/60 s pour les deux routes ensemble, personnel
60/900 s par route, 1 024 origines et 4 096 clés personnelles au total.
Le registre de contrôle conserve une allocation personnelle commune aux deux
catégories pour tenir ce dernier plafond. Tester huit processus et 50 requêtes/s,
plusieurs origines, puis 50 familles derrière une IP effectuant chacune deux
lectures/minute/route (200/minute) : pas de refus anonyme sous ces budgets.
Le surcoût du garde vise p95 ≤ 30 ms, p99 ≤ 100 ms. La sérialisation courte
du contrôle est volontaire ; sa contention et son retour à la normale font
partie de la preuve, pas une capacité supposée.

Avant activation, l'exploitant renseigne les proxies de la cible, distribution
NAT, débit attendu, taille du pool, valeurs de politique et purge observée.
Aucune protection WAF externe n'est présumée. Le correctif et les preuves
locales ne dépendent pas de cette cible ; l'ouverture publique en dépend.

### A05 et OPT-03/04/05 — contrat de coût et capacité

Appliquer la [convention performance](../../architecture/transverse/performance-volumetrie.md).
**Décision : projection exacte synchrone pour les lectures de qualification ;
recalcul global borné sous la barrière exclusive existante.** Une projection
différée après succès du retrait contredirait T5-D10 (effet immédiatement
visible). Le travail global O(N) reste autorisé, avec mémoire bornée et budget
transactionnel mesuré. Le SQL filtre les résultats du domaine ; il ne recopie
pas ses règles de preuve, de neutralisation ou de qualification.

#### Projection et chemins d'écriture

Ajouter `animation_qualifications_lecture`, une ligne par participation Chasse,
avec clés participant/animation et périmètre, configuration/version de définition,
révision d'exploitation, version de progression et version du projecteur,
statut effectif, éligibilité, progression, validations effectives, dates de
début/fin, source courante ou population figée. Les clés restent contraintes
au même périmètre ; indexer les filtres/tri effectifs des lecteurs, sans placer
réponses, tokens ou DSL dans la projection. Une révision de progression stockée
est incrémentée atomiquement dans la même transaction si aucun numéro existant
ne couvre une transition. Les agrégats exacts par animation sont entretenus
par deltas de cette projection dans la même transaction.

L'orchestrateur appelle `provenance_qualification`, `qualifier_participation`
et les moteurs existants de `politique_exploitation.py` ; les statuts GAGNANT
et ANONYMISE conservent les règles de `ParticipantAnimation.appliquer_resultat_moteur`.
La table E73 `animation_mesures_participations`, réconciliée différemment et
incomplète pour progression/révision, ne remplace pas cette projection exacte.

| Entrée réelle | Mise à jour requise, dans la transaction métier |
| --- | --- |
| `ServiceParticipantsAnimation.inscrire` | Créer la projection initiale et son agrégat, sans deuxième inscription. |
| Jeu Live, `_persister` ; `validations_animation.valider_dans_uow` et réconciliation | Projeter après calcul du moteur : réponse, preuve, QR/PIN ou régularisation, pas après simple lecture. |
| `correction_preuve_animation.corriger` | Mettre à jour version/projection/agrégats avec la correction ; préserver les refus après gel. |
| Retrait accepté → `neutraliser_dans_uow` ; paramètres d'exploitation | Recalcul global sous barrière exclusive, sans résultat intermédiaire visible. Les chemins classiques de retrait gardent leur règle propre et sont couverts en non-régression. |
| `ServiceTiragesAnimation` : gel, constat/remplacement de gain | Basculer vers provenance figée ; statut courant mis à jour, sans réécrire l'éligibilité historique. |
| Suppression et `conservation_animation_repository.py` | Supprimer/anonymiser aussi les données dérivées dans la même transaction ; ni identité réintroduite par reconstruction, ni population historique recalculée. |

La lecture d'une qualification figée utilise la provenance de ce gel. Une
correction refusée ou une anomalie ultérieure n'altère pas cette provenance ;
le statut courant anonymisé et la qualification historique sont distincts.

#### Contrats de lecture et consommateurs effectifs

Réutiliser `/{protected|internal}/animation-locale/lectures-globales/participants`
et `ServiceLecturesGlobalesAnimation`. Animation utilise déjà ce lecteur dans
`GlobalReadWorkspace`, pour la liste globale et l'onglet Participants d'une
animation. Les anciens `/participants` ne sont pas leur producteur principal.
L'ERP exploitation n'a pas de liste de participants classique à migrer ; sa
liste Tombola publique dans `suivi-animations.js` conserve son lecteur dédié.
Le contexte des lectures globales exige un partenaire et une seule commune
active ; il n'est pas substitué aux lectures historiques d'un ERP multi-communes.

Contrat hybride : pour **Chasse**, `qualifie`, `termine`, `validations` viennent
de la projection exacte courante/gelée, `mesureCourante=true` seulement après
contrôle de sa version. Les autres moteurs gardent les mesures E73, leurs
`bool | null` et leur fraîcheur. Ajouts facultatifs aux items : `progression`
(nombre de même unité que `ParticipantAnimationPayload.progression`)
et `sourceQualification` (`COURANTE` ou `GELEE`) pour Chasse. Conserver le
masquage nom/email/téléphone et `allowedActions`, qui n'autorise pas à elle
seule une commande. Les données personnelles ne deviennent pas complètes
par réutilisation du DTO des anciennes routes.

Paramètres conservés : `limit=25` (1–100), `cursor` (2 048 caractères maximum),
`recherche` (160), `animation_id`, `qualifie`, `termine`, `moteurs_supportes`.
Pas d'ajout implicite de filtre `statut`. Recherche par **préfixe**, selon le
contrat de ce lecteur, sur référence/nom/prénom/email/téléphone ; ne pas la
confondre avec la sous-chaîne A07 des demandes. Tri `(inscrit_at DESC, id DESC)`.
Une seule requête choisit les faits persistés selon le moteur, applique droits,
filtres et curseur avant `limit + 1` ; enrichir uniquement la page.
Le contrôle de couverture Chasse s'effectue après droits/périmètre/animation,
mais **avant** les filtres `qualifie/termine` : un état non reconstruit ne doit
pas être exclu puis présenté comme une page complète. Refus 503 explicite.

Le `LATERAL limit + 1` actuel **par animation** doit disparaître : il ne borne
pas le coût quand le nombre d'animations augmente. Prévoir un accès global
indexé par périmètre et ordre, puis filtres de qualification ; si nécessaire,
porter les clés de périmètre sur le support de lecture commun des participants
des trois moteurs, entretenues transactionnellement avec contraintes de
cohérence vers animation/participant. Cette dénormalisation de clés ne porte
aucune nouvelle règle de qualification hors Chasse. Vérifier les index de
préfixe des identités autorisées et le plan de la page mixte, y compris
10N animations autorisées et étrangères ; pas de fusion de pages clientes.

Ajouter **`avec_synthese: boolean = true`** à cette seule famille participants,
dans la liste blanche API, son schéma, le service et le lecteur. Par défaut,
conserver `items/nextCursor/hasMore/synthese/allowedActions`, les entiers de
synthèse et leur sens ; les compteurs sélectionnent la même source par moteur
que la page, avec agrégats/COUNT séparés et aucun chargement de preuves.
`observedAt` reste la mesure courante la plus ancienne ; un éventuel `calculeeAt`
additionnel date le calcul, sans changer ce sens historique.

Avec `avec_synthese=false`, le serveur **omet `synthese`** et ne calcule aucun
total ; c'est le mode de la liste interactive cible. Adapter explicitement
`globalReadApi.ts` et les accès à la synthèse dans `GlobalReadWorkspace` pour
ce mode : un total absent est indisponible, jamais zéro ni `items.length`.
Les indicateurs séparés disponibles portent leur périmètre/date ; un filtre
sans indicateur correspondant laisse seulement la page visible. Ne pas lancer
automatiquement une deuxième lecture avec synthèse pour chaque changement
de filtre. `validations`, ses compteurs et `ProofCorrections` gardent leurs
contrats obligatoires ; un type commun rendu facultatif ne suffit pas.

Les curseurs lient ordre, filtres, périmètre courant et version de la sélection
hybride. À la bascule, refuser un curseur de l'ancienne sélection et proposer
la première page ; pas de réinterprétation silencieuse. Les refus suivent le
code de curseur invalide du lecteur existant. Recontrôler les droits à chaque
page, annuler les réponses obsolètes et vider les données au changement de
session/commune. La pagination n'est pas un instantané entre deux requêtes :
une mutation peut déplacer une ligne filtrée ; Actualiser reprend la première
page, tandis que retrait/gel gardent leurs propres garanties transactionnelles.

Les listes mixtes continuent d'inclure Passeport, Tombola locale et Chasse.
La Tombola publique conserve `/animations/{id}/participants-page` et ses
compteurs/états email ; sélection explicite dans le composant dédié. Nommer
le choix global « Parcours et tombolas locales » et indiquer où consulter les
tombolas publiques ; ne pas promettre une page unique de toutes les inscriptions.
La liste globale conserve la négociation `moteurs_supportes` : intersection
des capacités déclarées et serveur, éventuellement vide. Les lectures ciblées
qui appellent `verifier_capacite_lecture` conservent leur refus
`CLIENT_ANIMATION_INCOMPATIBLE`. Ne pas introduire ce refus dans les listes
par déduction ; aucun filtrage supplémentaire n'est réalisé dans le navigateur.

Les deux routes historiques `/participants` et `/animations/{id}/participants`
conservent `pagination.page/page_size/total`, recherche et qualification effective
des autres moteurs. Pour Chasse, la source exacte permet filtre/page SQL,
COUNT séparé et enrichissement borné ; pas de remplacement par une mesure E73
inconnue. L'offset profond et le total historique restent une exception de coût
à mesurer, sans certification de pagination constante pour ces anciens appels.
Dans l'onglet **Tirage**, supprimer `api.animations.participants`/`collectPages`
utilisé pour fabriquer `participantNames` : utiliser `participant_affiche`/
`participant_email` déjà servis avec les gains, ou enrichir les seuls résultats
affichés. `nombre_eligibles` provient du tirage, pas d'une liste collectée.

#### OPT-03 — invitations réellement paginées

Le producteur existant `/animations/{id}/demandes-participation` accepte déjà
`page/page_size` et filtres ; son endpoint `/synthese` reste indépendant.
L'écran remplace `demandesParticipationAll` par une seule page de 25 (100
maximum), sans préchargement exhaustif ni total déduit de la page. Conserver
les filtres et revenir à la première page quand ils changent. La sélection
groupée porte sur des identifiants explicites affichés, au plus une page ;
changer de filtre/page la réinitialise ou demande de l'abandonner. Ne pas
envoyer `demande_ids=null` pour signifier une sélection vide, ce qui pourrait
élargir les destinataires. La commande serveur garde ses contrôles de version
et ses droits EPIC 56.

Une réponse d'envoi perdue se résout par le reçu de commande existant
`/demandes-participation/commandes/{cle}`, avec même clé/contexte ; remplacer
la récupération actuelle qui parcourt toutes les invitations pour retrouver
les destinataires. Une lecture indisponible laisse le résultat incertain,
sans renvoi automatique. Les traitements de relance/annulation gardent leurs
propres reçus. La pagination frontend ne prouve pas à elle seule le coût SQL
du producteur : mesurer filtre/limite/total et supprimer toute hydratation
complète avant découpe si elle subsiste. Le contrat historique à numéro de
page reste conservé ; l'offset profond est mesuré et signalé séparément.

#### Retrait, aperçu, métriques et gel

La confirmation d'un retrait prend directement la barrière **exclusive**
existante de coordination animation (pas de promotion partagé → exclusif),
revalide version/aperçu et traite les faits par lots de **500 maximum**.
Chaque lot est projeté par le domaine puis libéré de l'ORM avant le suivant.
Neutralisation, projections, agrégats, audit et intentions de notification
sont committés ensemble. Une interruption/timeout annule tout ; aucun reçu
de succès ne décrit un retrait seulement partiellement propagé.

L'aperçu et `_empreinte_participations` deviennent un parcours ordonné avec
accumulateur de compteurs et empreinte incrémentale, sans collection complète.
Le domaine reçoit des faits itérables ou des accumulateurs métier dédiés,
pas une liste dont il déduit implicitement `len`. L'instantané de lecture est
cohérent ; la confirmation recontrôle l'empreinte sous barrière exclusive.
Conserver la sérialisation canonique actuelle, ou versionner explicitement
le format et refuser un ancien aperçu par `APERCU_OBSOLETE`, sans mutation.
Une participation, un scan ou une correction concurrente qui change le
résultat invalide l'aperçu selon les mêmes règles qu'aujourd'hui.

Le traitement complet comprend les notifications : remplacer les collectes
globales d'installations de `notifications_localeo_live.py` par pages de
destinataires distincts, au plus 500, et insertions groupées idempotentes des
intentions. Préserver préférences, autorisations et clés de dédoublonnage.
Aucun envoi réseau sous le verrou, aucune liste globale ou requête par
destinataire cachée dans le service appelé. L'outbox conserve sa livraison.

Les compteurs décisionnels lisent les agrégats exacts ; les statistiques
descriptives coûteuses utilisent des agrégats datés reconstruits par le batch
existant, à mémoire bornée. La date/source de mesure est exposée et une mesure
ancienne ne devient jamais une autorisation, une qualification ou le gel.
Le GET métriques ne réhydrate plus toutes les exécutions/preuves.

Le gel reste **une seule transaction** sous coordination exclusive. Les ports
de tirage séparent l'en-tête de population, déjà muni de `nombre_eligibles`
en SQL, de ses membres : créer/lire l'en-tête, ajouter un lot de membres,
preuves et provenances, finaliser compte/empreinte, lire une provenance ou
tester une appartenance. `ajouter_population` et sa relecture `_population`
ne doivent plus reconstituer tous les identifiants pour les clôtures directes
ou batch. Remplacer leurs `len(population.participant_ids)` par le compte
de l'en-tête, vérifié par le nombre inséré. Conserver unicité des membres,
contraintes de périmètre, version du gel et intégrité des provenances. Le
nouveau type d'en-tête ne passe pas par le `set` exhaustif de l'ancien DTO.

La sélection des gagnants utilise encore une liste complète dans le code
actuel. **Borner le gel ne prouve pas la capacité du tirage lui-même.** A05
n'autorise pas un nouvel algorithme aléatoire : A12 rejoue le tirage existant ;
L4 mesure séparément son coût au volume cible. Un dépassement bloque cette
ouverture et demande une conception préservant uniformité/chances, sans
substitution silencieuse d'un tirage par échantillonnage.

#### Reconstruction et bascule

Migration additive de projection, agrégats, révisions et état de reconstruction
par animation/version de projecteur (`A_CONSTRUIRE`, `EN_COURS`, `PRET`). Ne
pas dupliquer `nombre_eligibles`, déjà présent sur les populations. Les nouvelles
écritures alimentent la projection **avant** activation des lecteurs.
La reconstruction est un traitement explicite du backend, jamais un GET :
pages stables, lots de 500 maximum, reprise après dernière clé, aucune
notification, gain ou modification de preuve. Pour un gel existant, partir
des provenances figées et non des règles actuelles.

Pendant la reconstruction, chaque lot travaille sous la coordination existante
et vérifie configuration/révision/version de progression avant mise à jour ;
un résultat calculé sur une version ancienne ne remplace jamais un plus récent.
Un changement global de révision relance la couverture de cette animation.
La finalisation prend la barrière exclusive, traite les lignes manquantes/
obsolètes par lots, vérifie couverture et agrégats, puis publie `PRET` avec
la révision exacte dans le même commit. Les insertions/suppressions concurrentes
doivent donc participer à la même coordination. En cas de timeout, conserver
la reprise et aucun état `PRET` partiel ; ne pas valider sur le seul nombre de lignes.
Une lecture qui requiert une projection indisponible refuse explicitement
en 503 après contrôle des droits, plutôt que de servir un résultat faux ou
de revenir au chargement exhaustif. L'ouverture des nouveaux lecteurs exige
la couverture de toutes les animations de leur périmètre, y compris gelées.

Déployer schéma, producteurs compatibles et traitement de reconstruction,
contrôler la couverture, puis activer lecteurs/consommateurs. Le retour à un
ancien producteur exige de désactiver ces lecteurs et d'invalider `PRET` avant
réactivation ultérieure : un ancien binaire n'entretient pas la projection.
Conserver schéma et historiques, puis reconstruire ; pas de migration destructive.

| Opération | Borne structurelle cible | Preuve avant acceptation |
| --- | --- | --- |
| Participants en mode curseur sans synthèse | Page explicite 25, maximum 100 ; au plus `limit + 1` racines, enrichissements groupés sur cette page ; tri total et filtres d'accès en stockage | Pages initiales/profondes, 25/100 résultats, N = 1 000 puis 10N = 10 000, population et animations autorisées/étrangères croissant séparément ; SQL, lignes et objets hydratés bornés par page. |
| Invitations et anciens contrats à numéro de page | Une page 25, maximum 100, sans collecte cliente complète ; pagination/total conservés | Mesurer aussi COUNT et offset profond ; mémoire d'hydratation liée à la page, exception de coût historique explicitée. |
| Métriques et aperçu de retrait | Agrégats exacts ou datés explicitement ; aperçu par lots de 500 maximum, empreinte incrémentale ; ne pas retourner toutes les preuves | Mesure de fraîcheur/révision, exactitude des compteurs et comparaison après neutralisation ; p95/p99 et mémoire sous jeu concurrent. |
| Gel et conservation | Travail global proportionnel à la population autorisé, lots de 500 maximum ; pas de liste complète conservée dans l'ORM ou le driver | RSS maximale, temps et verrous à N/10N ; interruption/rollback et courses scan/correction/clôture. Aucun résultat de gel partiel visible. |
| Médias visibles du jeu | Références autorisées seulement ; éventuel cache borné par taille et version, aucun cache privé public ni préchargement futur | Lectures stockage, CPU de décodage, octets, mémoire à froid/chaud et invalidation ; l'étude OPT-04 précède le choix technique. |
| Éditeur Animation | Rendu progressif sans collecte exhaustive ; bundle/chargement mesurés | Temps de première action utile sur profil mobile explicite ; décision OPT-05 documentée avant découpage. |

Les lots ne changent pas l'atomicité : garder le gel dans la transaction et
les verrous existants avec mémoire bornée. Si les mesures imposent une
préparation persistée en plusieurs transactions, spécifier d'abord instantané,
révision, reprise et publication finale atomique ; ne pas introduire des
commits intermédiaires visibles pour gagner du temps.

#### Budgets initiaux de recette et limites de preuve

Les valeurs suivantes sont des **objectifs à vérifier**, ni mesures acquises,
ni engagements de service de production. Elles complètent E59 avant la
campagne ; on ne les augmente pas après observation pour obtenir du vert.

| Opération | p95 / p99 visés | Mémoire supplémentaire du worker |
| --- | --- | --- |
| Page participants/invitations, limite 25 puis 100 | 700 / 1 400 ms | RSS ≤ 32 MiB |
| Recherche ERP A07, 25 résultats | 1 000 / 2 000 ms | RSS ≤ 32 MiB |
| Métriques Chasse | 900 / 1 800 ms | RSS ≤ 32 MiB |
| Aperçu ou confirmation de retrait à 10 000 participants | 5 / 10 s chacune, notifications comprises pour confirmation | RSS ≤ 64 MiB |
| Gel à 10 000 participants | 10 / 20 s | RSS ≤ 64 MiB |

Pour toutes les opérations, mesurer séparément attente de pool, verrous et
temps transactionnel ; timeout/rollback ne compte pas comme succès rapide.
Le budget mémoire borne l'accumulation par nombre de participants, mais une
racine peut elle-même être grosse : ne pas charger l'historique complet des
tentatives, seulement les faits nécessaires au domaine, partager la définition
immuable de l'animation et libérer les lots. Vérifier le maximum réellement
accepté par les schémas/imports à l'implémentation ; aucune limite implicite
de huit étapes n'est ajoutée au produit. Éprouver séparément huit étapes puis
cent étapes, historique de tentatives élevé et configuration volumineuse ;
documenter l'enveloppe réellement couverte. Si un lot dépasse le budget,
réduire sa taille jusqu'à une participation ; une racine seule trop coûteuse
reste un échec de capacité à traiter, pas une qualification tronquée.

Jeu de charge : N = 1 000 puis 10N = 10 000 participants, 10 % qualifiés puis
90 %, tenants/animations/historiques hors filtre croissants indépendamment ;
pages initiales/profondes et recherches rares/absentes. Relever matériel,
versions, taille du pool et données. Référence initiale : 50 requêtes/s,
jusqu'à 100 utilisateurs concurrents, réparties en 60 % lectures joueur,
20 % commandes de jeu, 15 % pages et 5 % métriques ; retrait/gel isolés puis
en concurrence avec le jeu. Établir une phase stationnaire de cinq minutes
après échauffement ; mesurer au moins 100 exécutions isolées de chaque action
globale sur fixtures réinitialisées pour rendre p95/p99 interprétables.

Séparer refus métier attendus, 429 de scénarios adverses et erreurs inattendues
(objectif < 0,5 % hors attaque). Arrêter la campagne en cas d'erreurs inattendues
≥ 2 % pendant 30 s, p95 > deux fois le budget pendant 60 s, épuisement du pool,
charge non émise par le générateur ou effet externe inattendu. Mesurer
saturation et retour à la normale. La cible, sa politique A04 et sa distribution
NAT sont déclarées avant le test ; utiliser assez de participations/origines
pour que la limitation personnelle ne fausse pas la charge légitime.
Aucune valeur E74 ne valide la Chasse, aucun test partagé n'est implicite.
Un dépassement bloque la capacité concernée et L4, pas les correctifs indépendants.

### Matrice de traçabilité, impacts et livraison

Toutes les preuves ci-dessous sont **à produire après implémentation**.
Le [bilan d'audit](suivi-implementation.md#e55-audit-20261113) conserve séparément
les exécutions du 13 novembre et leurs échecs.

| Critères | Preuves prévues / comportements conservés | Fonctionnel, contrats et consommateurs | Fixtures / démonstration | Exploitation, données et livraison |
| --- | --- | --- | --- | --- |
| A01 | Stockage refusé avant inscription et après succès, accès temporaire réel au jeu, réponse perdue, deux onglets, doublon, lien expiré/récupération ; reprise exacte et pas de double place | Complément fonctionnel et guide Live ; contrat d'inscription inchangé ; frontend partagé testé sur autres moteurs sans modifier E74 | Fixtures navigateur panne IndexedDB/écriture ; aucune donnée de génération nouvelle | Aucune migration attendue ; consigne de récupération et limite de durée de l'accès temporaire ; pas de token dans les mesures |
| A02/A03 | Reçu confirmé puis nouvelle décision, reçu absent/étranger/refusé, conflit, changement de session ; brief conservé/abandon explicite | ERP `travail.js`/préparation/génération et Animation ; contrats métier existants | Recette `epic73-preparations-service.cjs`, génération ERP/Animation ; générateur sans nouveau champ | Pas de migration ; documenter reprise, ne pas inviter à contourner le verrou ou désactiver les protections |
| A04 | Variation UUID, IP, huit processus, fenêtres, caps/purge, panne/timeout ; aucun compteur personnel avant autorisation, seuil atomique, retour à la normale | Nouveau port identité, deux GET Live ; codes non révélateurs et 429 préservés | Doubles de ports puis PostgreSQL jetable ; aucun envoi réel | Deux tables PostgreSQL, politique et purge définies ci-dessus ; calibrage/proxies à vérifier avant activation |
| A05/A12 | Projection égale au domaine sur tous les chemins, reconstruction/reprise, page mixte et synthèse facultative ; retrait/gel atomiques ; N/10N et chaîne complète | Lecteur global hybride et consommateurs, anciennes routes préservées, nouveaux ports d'en-tête ; E41/copies à générer avec le code | UoW alignés sur `reversibilite`/`apercus_dotation_publique` ; reconstruction figée/anonymisée sans effet, tests concurrents réels | Migration additive projection/révisions/agrégats/index et protocole de bascule définis ; coût global et tirage à mesurer avant ouverture |
| A06/A08/OPT-01 | Panne quota isolée, invitations erreur/vide/succès, message unique, permissions retirées, acteur/délai connus ou inconnus | Animation et guidage ERP ; service accompagné existant, aucune nouvelle SLA | Fixtures de pannes et calendrier absent ; pas de mutation du générateur attendue | Guide de diagnostic et prochaine action ; pas de migration |
| A07/OPT-03 | Résultat hors première page, accents/jokers littéraux, filtres/droits, curseurs, réponses tardives ; invitations par page et reçu sans collecte complète | API génération E41/contrats embarqués concernés ; ERP/Animation ; EPIC 56 conservée pour accords | Historiques multi-pages/tenants et plans SQL ; projection normalisée reconstruite par outil existant | Réutiliser nom normalisé/GIN v276 ; contrôler réparation et plans, migration d'index additionnel seulement si justifiée ; backend puis consommateurs |
| A09/A11/A13/A14 | Clic réel sans occlusion, cinq activités, doublons expliqués, focus/annonce, texte à 200 % et clavier/toucher 320/390/1280 | Live et principes UX ; aucun changement du DSL, des aides, preuves ou chances | Recettes visuelles à API simulée puis cible ; aucune donnée de démo nouvelle requise | Pas de migration ; conserver accès sensibles revalidés et consigner limites des appareils |
| A10 | Champs facultatifs, définition publiée, données anciennes, autres moteurs, absence de secrets/futurs, aucun N+1 | Producteur catalogue, E41/E42, normalisations/rendus Live ; schéma moteur déjà présent | Fixtures anciennes et riches ; vérifier les projections du générateur, sans inventer de durée absente | Scalaires JSON de configuration publiée, pas de nouvelle table/migration métier ; backend puis Live, ancien serveur toléré |
| OPT-02/04/05/06 | Conception d'aperçu et décisions motivées de mesure ; temps/erreurs avant-après et pilote | Études dans ce dossier ; liens vers règles existantes, aucune collecte Analytics réactivée | Cas synthétiques et observations humaines ; pas de génération réelle implicite | Mesures agrégées/sans accès ou réponses ; aucun gain annoncé sans référence, configuration d'instrumentation examinée avant code |

Les interfaces Commerçant ne changent pas de comportement dans ce lot ; leur
contrat embarqué et la chaîne attestation/kit restent à vérifier si un export
partagé évolue. Les scripts/données de démonstration restent dans le backend.
Les migrations A04/A05 sont additives, conservent les historiques et
font l'objet d'une recette jetable. Les OpenAPI et bundles documentaires ne
seront générés/vérifiés qu'avec les producteurs correspondants.

### Préparation par lot et conditions restantes

La spécification de L1/L2 et de l'architecture A05 est exploitable pour
implémentation : états et refus, stockage A04, sources exactes A05, compatibilité
HTTP, reconstruction, recherche A07 et mapping A10 sont définis. A04 peut être
codé/testé avec sa politique de recette ; son calibrage cible précède activation.
Pour A05, commencer par les ports/projection et tous leurs producteurs, puis
reconstruction/lectures, retrait/gel et mesures. Ne pas basculer un lecteur
avant couverture, ni accepter la capacité avant les budgets mesurés.

A12 remet à niveau les preuves parallèlement aux correctifs et rejoue la chaîne
après intégration. OPT-02/04/05 sont des études bornées : leurs sorties sont
conception/décision motivée, pas une optimisation ou invalidation présumée.
OPT-06 fixe la référence de productivité avant modifications puis compare
après recette. Aucun critère n'est coché par cette spécification ; exports,
code, migrations, tests et mesures restent à produire.

Le pilote L4 reste dépendant d'une cible, de versions et d'acteurs identifiés,
de la conversion/permissions/conservation et des critères bloquants retestés.
Les observations humaines ne sont pas remplacées par les captures Chromium.
Les bilans et la [recette](recette-pilote.md#e55-audit-20261113) distinguent
clairement preuves locales, dettes, non-exécutions et opérations sur cible.

### Étude OPT-02 — aperçu des accords affectés

La lecture du code le 13 novembre confirme une invalidation sélective déjà
existante. `missions_commercantes.snapshot_commercant` construit les engagements
propres à chaque commerce ; `empreinte_engagements` exclut les identifiants
documentaires et conserve le contenu et les empreintes des images visibles.
`DemandeParticipationCommercantAnimation.renouvellement_missions_requis` décide
du renouvellement, puis `synchroniser_dans_uow` ferme l'ancien cycle et crée la
demande à envoyer. Un refus reste dans l'historique. Une simple nouvelle révision
de préparation ne suffit donc pas à renouveler tous les accords.

| Modification proposée | Conséquence actuelle à présenter dans un futur aperçu |
| --- | --- |
| Mission, conditions ou image visible d'un seul commerce | Renouvellement de son cycle déjà envoyé si son empreinte change ; les autres commerces restent inchangés |
| Nom, description, dates ou règlement repris dans chaque engagement | Plusieurs cycles peuvent changer ; calculer leurs empreintes au lieu de déduire le résultat du seul champ édité |
| Même image réimportée avec une autre clé documentaire | Empreinte stable : aucune nouvelle demande motivée par ce seul changement |
| Commerce retiré du parcours | Fermeture de son cycle ; aucun envoi automatique à un autre commerce |
| Commerce ajouté ou demande encore à envoyer | Nouvelle demande ou mise à jour de la préparation ; aucun accord existant inventé |
| Échéance de réponse | Règle propre `adapter_echeance_missions` : réduction refusée après envoi ; ne pas confondre avec les dates de l'animation |

Décision de cette étude : un aperçu utile doit réutiliser ces fonctions de
domaine dans un calcul sans écriture. Il présenterait les totaux et une liste
paginée « accord conservé / nouvelle invitation nécessaire / commerce retiré »,
avec la cause compréhensible et la prochaine action. Aucun message ne serait
envoyé à l'ouverture ou à la confirmation de cet aperçu ; l'envoi des invitations
resterait sa commande explicite.

Avant une future implémentation, extraire le calcul de synchronisation sans
dupliquer sa politique dans l'interface. L'aperçu doit être lié à la révision de
configuration et aux versions des demandes consultées ; la sauvegarde recalcule
les effets sous le verrou courant et refuse un aperçu devenu obsolète. Il faut
notamment tester une acceptation commerçant entre aperçu et sauvegarde, une image
identique réimportée, un changement concernant un seul commerce et un refus
historique. Cette étude n'ajoute ni route ni nouvelle règle d'invalidation ;
l'aperçu n'est pas annoncé disponible dans l'interface livrée.

### Études OPT-04/05/06 — mesures locales et décisions

Les mesures du 13 novembre portent sur l'arbre de travail de cette évolution,
sur Windows, avec fixtures synthétiques et sans service externe. Elles ne
constituent pas une référence de latence du stockage distant ni du terrain.

**Médias (OPT-04).** Sur un WebP de 43 794 octets en 640 × 360, l'hydratation
backend effectue 31 lectures et 31 décodages pour 31 appels, soit 1 357 614
octets relus. Premier appel applicatif : 414 ms ; parmi les 30 répétitions,
médiane 16,6 ms, p95 21,9 ms ; décodage seul médiane 13,7 ms, p95 18,1 ms.
Le pic d'allocations Python mesuré est 6 056 677 octets, sans le pic natif PIL.
Le premier appel inclut les initialisations ; le cache du système de fichiers
n'a pas été purgé. Le banc vérifie aussi absence de lecture d'un média non
sélectionné, refus du mauvais partenaire avant stockage et rejet d'une corruption.
Script et résultat locaux : backend `tmp/e55-impl-medias/`.

Dans Chromium, la même fixture produit deux décodages base64 initiaux puis un
par actualisation, de 0 à 0,2 ms au passage final. Une seule BlobURL reste active ;
les sept créations sont toutes révoquées à la sortie. La mémoire bitmap n'est
pas mesurée. Le coût prioritaire est donc à instruire côté backend et stockage,
sans attribuer la durée d'hydratation au seul navigateur.

Décision : conserver les contrôles privés et l'absence de cache supplémentaire
dans cette livraison. Une optimisation ultérieure devra mesurer le stockage
cible, puis comparer un cache de validation borné par octets, partenaire,
empreinte et version du décodeur. Elle devra encore relire l'autorisation de la
projection et vérifier révocation, corruption et invalidation ; aucun média
futur ne sera préchargé. Les résultats présents motivent cette piste, sans
démontrer un gain de bout en bout ni autoriser un cache public.

**Chargement Animation (OPT-05).** Trois parcours froids et trois chauds avant
et après, viewport mobile, CPU ralenti ×4 et réseau simulé, API interceptée :
médiane première action utile à froid 8 371 → 8 235 ms, à chaud 8 277 → 8 374 ms.
Les fichiers `before.json`, `after.json` et le protocole sont conservés dans
Animation `tmp/e55-impl-animation-performance/`. L'échantillon et l'écart ne
démontrent aucun gain ; aucun découpage supplémentaire n'est retenu sur cette
seule mesure. Le build production/PWA reste vérifié séparément. Un futur
découpage devra viser le code chargé avant la première action sur ce même
parcours et conserver les gardes de saisie/focus.

**Productivité (OPT-06).** L'audit préalable constitue la référence observable :
inscription bloquée sans carnet, décision ERP suivante bloquée après reçu,
saisie réinitialisée, recherche limitée à la page et liste d'invitations
collectée intégralement. Les recettes après correction observent respectivement
un seul POST d'inscription et un jeu temporaire, la décision suivante envoyée,
le texte conservé y compris après conflit, un résultat hors première page et
une seule page de 25 invitations. Ce sont des changements de comportement,
pas des minutes gagnées mesurées auprès d'utilisateurs.

Le pilote doit encore comparer le temps jusqu'à une demande traitée, les
ressaisies, retours entre applications et demandes d'aide pour chaque acteur.
Conserver même scénario/volume et noter les erreurs ou abandons, avec résultats
agrégés sans texte de réponse, accès personnel ni suivi Analytics. L'absence de
mesure humaine avant/après reste explicite : aucun pourcentage de productivité
ni réduction du temps de travail n'est revendiqué.

<a id="e55-evol-traitement-20261113"></a>
## E55-EVOL-TRAITEMENT-20261113 — Dossier ERP unique

### Écart et décision

Baseline du 13 novembre : backend `76d5dee9`, projet `14fdc14`, arbres propres.
La console de génération possède déjà liste, prompt, import, aperçu et reprise,
mais renvoie vers une autre fiche pour la qualification. L’import demande une
vérification puis un enregistrement distincts. La sélection du dossier vit en
mémoire, sans lien direct de reprise. Le parcours cible et ses dix critères sont
dans la [spécification fonctionnelle](localeo_animation_engine_spec.md#e55-evol-traitement-20261113).

Cette évolution unifie la présentation et l’enchaînement des commandes existantes.
Elle ne crée pas de troisième machine d’état. Les règles
[ERP-UX-01 à ERP-UX-12](../../architecture/transverse/conventions-backoffice.md#ux-des-pages-de-gestion-erp)
s’appliquent, en particulier identité, portée, saisies, état confirmé et reprise.

### Propriétaires, transitions et contrats préservés

`DemandePreparationAccompagnee` possède la qualification, le calendrier et le
suivi E73 ; `OperationAnimation` et les règles de génération possèdent prompt,
réponse, acceptation et finalisation E55. L’application coordonne ces agrégats ;
la console présente leurs `allowedActions` sans déduire une nouvelle permission.

Toutes les routes ci-dessous utilisent la base
`/internal/animation-locale/operations/{operation_id}` :

| Geste ERP | Contrat existant | Fait confirmé attendu |
| --- | --- | --- |
| Valider la demande | `POST /service-preparation/completer`, version du service | `A_COMPLETER → EN_PREPARATION` ; worker autorisé à préparer le prompt |
| Refuser avec motif | `POST /service-preparation/annuler`, version du service, motif de 3 à 2 000 caractères | Opération et service `ANNULEE`, réservation libérée, motif dans l’historique du service |
| Recevoir un complément historique | `POST /service-preparation/recevoir-complement`, version du service | Reprise du suivi existant sur la même demande |
| Récupérer le prompt | `GET /prompts/{prompt_id}/export?format=texte` | Lecture privée du prompt courant et de son contexte |
| Importer le résultat | `POST /reponses/verifier`, puis `POST /reponses` seulement si conforme | Contrôle consultatif puis dépôt du même document, `RESULTAT_DEPOSE` ; le worker confirme ensuite `A_VALIDER` ou `RESULTAT_INVALIDE` |
| Valider le traitement | `POST /reponses/{id}/accepter`, version opération/source, prompt et empreinte | `RESULTAT_PUBLIE` ; worker applique puis confirme `TERMINEE` et service `PRETE` dans la même transaction |
| Reprendre un échec autorisé | `POST /reprendre`, version opération | Même demande, même quota, phase de reprise décidée par le serveur |

Les reçus service (`/service-preparation/commandes/{cle}`) et génération
(`/commandes/{cle}`) restent distincts. Le verrou de commande dans la fiche est
commun : après un résultat incertain, les autres commandes attendent la
réconciliation. Le serveur lie le reçu à l’acteur, au type et au contenu dans son
espace de clés ; le navigateur vérifie l’enveloppe, la cible et l’intention encore
courante avant d’annoncer une réussite. Le reçu service expose directement
`operationId`, `operationCommandeId`, `servicePreparation` et `rejoue`, alors que
le reçu de génération expose `status: CONFIRMEE` et `result.operation`.
Un rejeu conserve la même clé et le même corps. La version du service ne
remplace pas la version de génération.

Le motif saisi reste lié à sa version initiale ; un rafraîchissement concurrent
ne doit pas le réautoriser avec une nouvelle version silencieusement. Droits,
communes, session, CSRF et conditions d’acceptation sont revérifiés au serveur.
Un changement de dossier invalide lectures tardives, aperçus et confirmations.

### Reprise, compatibilité et limites

Le lien `/internal/erp/animations/generations?operation_id={uuid}` sélectionne
directement le dossier autorisé, même absent de la page courante. Filtres et
curseurs structurés restent ceux de la liste, dans les métadonnées de navigation
liées à l’identité et aux droits. La recherche libre reste en mémoire de page ;
elle n’est pas sérialisée dans l’URL, `history.state` ou un stockage durable.
Un rechargement complet la réinitialise. Le retour à une entrée de navigation
encore disponible retrouve son contexte ; une arrivée nouvelle utilise le lien
canonique et les filtres disponibles. Aucun brief, fichier JSON ou motif privé
n’est ajouté à l’URL ou au stockage durable. Après rechargement, l’étape est
déduite de l’état confirmé. Une saisie non enregistrée reste protégée avant
sortie, changement de demande ou actualisation et est purgée à expiration.

La projection de liste ne comporte pas le suivi complet du service. Une phase
`PREPARATION_PROMPT` seule ne prouve donc pas la qualification : la liste invite
à ouvrir le dossier, dont la lecture détaillée fournit l’action exacte. Ne pas
annoncer une génération déjà en cours sur cette seule phase, ni charger chaque
détail pour enrichir toute la file.

Les dossiers historiques sans service de préparation conservent leur progression
autorisée ; aucune qualification passée n’est fabriquée. Les anciens liens de
préparation restent disponibles pour calendrier et suivi avancé, avec accès
explicite au dossier unique. Les outils terrain restent un parcours distinct.

Les traitements automatiques attendent le batch existant `animations.generer`.
La console affiche l’attente et relit le dossier ; elle ne lance pas le batch
global et ne promet pas une génération instantanée. Une reprise après simple
fermeture/rechargement est distincte d’un refus métier : après acceptation puis
modification du brouillon, `ECHEC_FINALISATION/CONTEXTE_OBSOLETE` peut interdire
la reprise simple. L’interface doit expliquer ce refus, sans créer de nouvelle
demande, réviser silencieusement le résultat accepté ou annoncer une fin réussie.

### Matrice d’impacts et preuves

| Critères | Responsabilité et preuve prévue | Impacts |
| --- | --- | --- |
| DG-01/04/07/10 | Console ERP : étapes, sélection directe, filtres, clavier, rendu mobile et texte 200 %, chargement après qualification | HTML/JS, navigation, guides ; aucun changement de règles ou schéma persistant |
| DG-02/03 | Commandes E73 existantes : droits, version, annulation atomique et motif ; recette UI inline et non-régressions domaine/API | Réutilisation des contrats existants, aucun nouvel email ; motif consultable après reprise |
| DG-05/06 | Chaînage contrôlé du contrôle consultatif/dépôt puis acceptation distincte ; JSON invalide, rejet, reçu incertain, état final réel | Même format JSON/médias, mêmes contrats et contrôles serveur ; aucune publication automatique |
| DG-08/09 | Complément, conflits, échecs, réponse perdue et purge privée ; tests des deux espaces de reçus | Aucune extension de droits ni reprise de contexte obsolète inventée |

Les listes gardent leur pagination serveur de 25/max 100 ; une arrivée directe
ajoute une lecture de dossier, sans parcourir les pages pour le retrouver.
L’historique est borné et paginé, les détails chargés selon le besoin. Le budget
d’import existant de 8 Mo et le polling borné sont conservés ; pas de nouvelle
projection SQL ou collecte d’annuaire. Aucun gain de capacité ou de temps n’est
déduit de cette simplification sans mesure dédiée.

Applications affectées : `localeo-backend` pour l’ERP et ses tests,
`localeo-projet` pour les sources canoniques. Live, Animation et Pro continuent
de lire les mêmes états et contrats ; leurs clients embarqués restent inchangés.
Aucune migration, configuration, nouvelle donnée de démonstration ni génération
réelle n’est nécessaire. Les fixtures UI couvrent les états existants. Les
contrats OpenAPI ne changent pas si l’implémentation reste dans ces bornes.

Les recettes génération et guidance, la nouvelle recette du dossier unifié,
la compatibilité préparation/navigation et les tests isolés des commandes E55/E73
sont reliés à leurs résultats dans le
[suivi de réalisation](suivi-implementation.md#e55-evol-traitement-20261113).
La recette déployée, le pilote
humain et les mesures de productivité restent distincts des tests locaux.
