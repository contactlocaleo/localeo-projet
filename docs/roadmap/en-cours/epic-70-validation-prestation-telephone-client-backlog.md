# EPIC 70 — Valider une prestation ou une animation depuis le téléphone du client

## Références et décisions

- Identifiant : **EPIC-70** ; cadrage et recadrage du **1er octobre 2026**, extension du **5 octobre 2026**.
- État : **En cours** ; implémentation et vérification locales le 7 octobre 2026, sans déploiement.
- Besoin : un commerçant sans téléphone disponible doit pouvoir valider une
  prestation de coffret ou une action terrain d'animation depuis le téléphone connecté
  du client, sans matériel supplémentaire, y compris en cas de panne de son mobile.
- **Solution retenue par l'utilisateur : PIN de validation dédié**, géré par le
  commerçant depuis son accès professionnel, avec validité, renouvellement et
  révocation ; contexte transactionnel et parcours client à implémenter.
- Phase : spécification V1 puis implémentation du 7 octobre ; résultats et limites dans le bilan de livraison.
- [Spécification canonique](../../specifications/epic-70-validation-pin/README.md), [architecture et contrats](../../specifications/epic-70-validation-pin/architecture-contrats.md), [matrice des preuves](../../specifications/epic-70-validation-pin/verification-livraison.md).
- [Roadmap](../README.md), [validation actuelle](../../specifications/validation-prestations/README.md),
  [contrats de validation](../../specifications/validation-prestations/contrats-api.md).

Le besoin initial demandait une sécurité équivalente au parcours courant. Après
comparaison, l'utilisateur retient un compromis fondé sur des **droits strictement
limités et des conséquences de compromission bornées**, sans prétendre empêcher la
capture du PIN sur un téléphone tiers. Les pistes de boîtier, carte cryptographique
ou écran indépendant sont écartées du périmètre retenu car trop contraignantes.

Ce périmètre prolonge le cadrage de cette epic. Il ne rouvre pas l'[EPIC 2](../terminees/epic-2-invalidation-validation-prestation-v1-backlog.md)
et ne remplace pas le [secours téléphonique E9](../terminees/epic-9-mode-secours-telephonique-honorisation-prestation-backlog.md).
Le QR commerçant historique reste abandonné ; aucune réactivation de ses contrats.

**Extension demandée le 5 octobre 2026 :** la validation terrain d'animation entre
dans le périmètre. Cette décision remplace explicitement l'exclusion Animation du
1er octobre ; elle n'autorise pas l'administration des animations. Les accès
salariés nominatifs sont cadrés séparément dans l'[EPIC 72](../en-cours/epic-72-acces-salaries-validation-localeo-pro-backlog.md).

## Problème et résultat attendu

Le commerçant n'a pas de téléphone au comptoir, ou rencontre un problème technique,
mais le client présente son coffret ou sa participation à une animation sur son
propre téléphone. Le commerçant doit pouvoir vérifier l'action attendue et
confirmer sa consommation sans se connecter à son espace professionnel sur cet appareil.

Parcours cible : **le client choisit, le commerçant lit et saisit son PIN, Localeo
valide une seule prestation ou action terrain et affiche le résultat**. Le commerçant prépare et gère
son PIN en amont depuis Localeo Pro avec son accès principal ; cette préparation n'impose
pas de téléphone professionnel disponible le jour de la prestation.

Acteurs : détenteur d'un droit d'accès au coffret ou participant à une animation, commerçant, éventuel collaborateur
autorisé et support habilité. Un PIN partagé établit une autorisation au niveau du
commerce ; il ne prouve pas quel salarié l'a saisi.

## Existant à réutiliser

La revue initiale du code local, sans test ni connexion à un environnement, a relevé :

- [Authentification commerçant](../../../../localeo-backend/app/application/identite_acces/use_cases/authentifier_commercant_par_mot_de_passe.py) :
  compte, mot de passe et session professionnelle aux droits plus larges que la validation.
- [API validation](../../../../localeo-backend/app/api/validation_api.py) et
  [ouverture de transaction](../../../../localeo-backend/app/application/exploitation/use_cases/ouvrir_transaction_validation.py) :
  session commerçant et QR client, transaction liée au commerce/coffret/empreinte QR,
  durée courte (60 secondes par défaut observées, pas une durée imposée à E70).
- [Validation](../../../../localeo-backend/app/application/exploitation/use_cases/valider_prestation.py) :
  contrôles du commerce, du coffret et du droit, puis
  [service commun de consommation](../../../../localeo-backend/app/application/exploitation/services/service_validation_prestation.py)
  avec transition conditionnelle et effet de reversement idempotent.
- [Secours](../../../../localeo-backend/app/application/exploitation/use_cases/traiter_validation_secours.py) :
  procédure opérateur avec motif et décision, pas un libre-service client.

Le [code lisible du QR](../../specifications/validation-prestations/identifiant-qr.md)
identifie le coffret dans son parcours existant ; il n'authentifie pas le commerçant.
Le [référentiel commerçant](../../specifications/espace-commercant/README.md) confirme
l'abandon de l'ancienne carte QR commerçant.

Réutiliser les règles de consommation et de reversement ; ne pas créer un second
moteur de validation. Le droit client requis doit être cartographié précisément :
une référence publique ou un identifiant de coffret seul ne suffit pas.
Pour l'animation, réutiliser les règles du [moteur d'animation](../../specifications/moteur-animation/localeo_animation_engine_spec.md),
notamment éligibilité, progression et récompenses : le PIN permet exactement les mêmes
validations terrain que le scan QR commerçant, avec les mêmes conditions et effets,
sans administration. La spécification cartographiera les contrats et droits participant correspondants.

## Périmètre fonctionnel retenu

### 1. Contexte transactionnel de validation

Le serveur prépare une demande limitée à **une prestation d'une instance de coffret,
son commerçant et un droit client vérifié**. L'identité du commerçant est dérivée
de la prestation, jamais choisie librement dans une requête client.
Pour une animation, la demande lie **un participant, une animation, une action
terrain et un commerce autorisé**. Le serveur contrôle ce rattachement ; le PIN
ne permet ni de désigner librement un commerce ni de choisir une autre finalité.

- Identifiant opaque, finalité dédiée, création, expiration, état et corrélation.
- Demande valable 5 minutes dès sa création pour saisir le PIN et confirmer ;
  après expiration, nouvelle demande nécessaire, sans consommation ni passage validé.
- Données métier figées pour la demande ; changement de prestation ou de coffret
  exige une nouvelle demande et une nouvelle saisie du PIN ; même règle pour tout
  changement de participant, animation ou action terrain.
- Aucun effet de consommation, réservation exclusive ou reversement lors de la
  simple ouverture ; limiter les créations abusives de demandes.
- Contrôle à la confirmation du droit client toujours valable, de l'éligibilité
  métier, de l'état du commerçant et du PIN courant.
- Vérification du PIN et consommation dans une opération orchestrée cohérente ;
  aucun ticket de connexion professionnelle émis après un « PIN correct ».
- Résultat terminal et reprise après timeout sans nouvelle consommation ; consultation
  limitée au détenteur du droit client concerné, même après expiration du PIN.
- Concurrence maîtrisée entre parcours normal, parcours PIN, double clic et appareils.

États fonctionnels à préciser dans la spécification : demande en attente,
validée, expirée ou annulée ; refus et blocage des tentatives distincts du succès.
Une demande courte ne rend pas le PIN lui-même à usage unique.

### 2. Gestion du PIN depuis l'espace commerçant

Le commerçant principal peut, depuis Localeo Pro, activer le mode, créer son PIN dédié, consulter son état et ses
dates, le remplacer, le révoquer et désactiver le mode depuis son accès authentifié.
**Le PIN de validation ne peut jamais gérer son propre cycle de vie.**
L'accès salarié limité de l'EPIC 72 ne peut pas gérer le PIN du commerce.

- PIN généré automatiquement par Localeo, distinct du mot de passe professionnel ;
  6 chiffres, sans suites simples ni répétitions telles que `123456` ou `111111`.
- Activation immédiate à la génération, date/heure de fin obligatoires,
  durée de 7 jours par défaut, configurable de 1 à 30 jours par jours entiers.
  Heure serveur de référence et affichage local explicite.
- **Un seul PIN actif par commerce**, commun aux coffrets et animations, versionné. Le remplacement
  rend l'ancien inutilisable ; le renouvellement crée un nouveau PIN, sans prolonger
  silencieusement un secret potentiellement compromis.
- Consultation des métadonnées et de l'historique, pas récupération du PIN en clair.
  PIN perdu : invalidation et régénération faciles depuis Localeo Pro après vérification
  de l’accès professionnel ; ancien PIN immédiatement inutilisable, nouveau PIN valable
  7 jours par défaut, durée configurable dans la limite de 30 jours.
  En cas de blocage ou d’accès impossible, le support habilité peut invalider le PIN
  et aider à récupérer l’accès professionnel, sans jamais consulter le PIN ; intervention auditée.
- Création ou remplacement : vérification du mot de passe principal datant de
  15 minutes maximum ; sinon, nouvelle saisie du mot de passe requise.
  Invalidation seule sans cette étape supplémentaire depuis une session principale connectée.
- Dans l’ERP, Admin et Backoffice peuvent invalider un PIN ; Lecteur et Finance
  seuls sont exclus. Intervention tracée, sans consultation du PIN.
- Aucun PIN en clair en base, logs, traces, analytics, notifications ou exports ;
  mécanisme de vérification adapté à un secret de faible entropie à concevoir.
- Révocation, expiration, remplacement, désactivation du mode ou suspension du
  commerçant contrôlés au moment de l'effet métier, y compris pour une demande déjà ouverte.
- Alerte de changement ou de blocage du PIN dans Localeo Pro et par email au
  commerçant principal sur son contact vérifié, sans communiquer le PIN.

En cas de course entre révocation et validation, l'ordre des opérations doit être
déterministe : une validation déjà engagée définitivement conserve sa trace ; après
révocation effective, aucune nouvelle validation ne peut être autorisée par l'ancien PIN.
La révocation n'annule ni une consommation passée ni son mouvement de reversement.
Elle n'annule pas non plus une progression ou une récompense d'animation déjà acquise.

### 3. Parcours sur le téléphone du client

1. Le client ouvre son coffret avec un droit d'accès valable et choisit une
   prestation éligible : « Faire valider par le commerçant ».
2. Localeo prépare la demande et affiche le nom du commerce, la prestation, la
   référence du coffret et l'effet de la validation, sans données professionnelles.
3. Le client tend son téléphone. Le commerçant lit le récapitulatif, saisit son
   PIN dédié dans un champ masqué et confirme « Valider cette prestation ».
4. Le serveur effectue les contrôles puis la consommation unique et ses effets
   métier habituels. Aucun succès n'est affiché avant confirmation serveur.
5. Le téléphone affiche le reçu limité : résultat, prestation, date et référence.
   Le commerce retrouve la validation et son mode dans son historique.
6. Le champ PIN est vidé après soumission/abandon ; aucune sauvegarde applicative
   du PIN, aucun accès professionnel et aucune autorisation générale ne persistent.

Pour l'animation, le participant ouvre son parcours avec le droit requis et choisit
l'action terrain éligible. Le récapitulatif présente l'animation, l'action, le commerce
et l'effet attendu sur sa progression/récompense. Le commerçant confirme cette seule
action avec son PIN ; le serveur applique les règles habituelles et fournit le reçu.
Aucune création, publication, configuration ou gestion des participants n'est exposée.

Prévoir clavier mobile accessible, erreurs compréhensibles sans révéler le PIN,
expiration pendant la saisie, abandon, réseau interrompu et consultation du résultat.
La suppression du champ limite la rétention par Localeo ; elle ne garantit pas
l'absence de capture sur le téléphone client.

## Sécurité proportionnée et risque résiduel retenu

Le PIN autorise uniquement une validation de prestation du commerce ou d'action
terrain d'animation autorisée, avec un droit client/participant valable.
Il ne donne accès ni au profil, ni au catalogue professionnel,
ni aux autres coffrets, ni aux messages, ni aux coordonnées de paiement,
ni aux remboursements, ni à la gestion des accès ou du PIN.

**Un PIN capturé reste réutilisable pendant sa validité avec d'autres droits de
coffret ou participant accessibles à l'attaquant, pour les prestations ou actions
terrain autorisées à ce même commerce.**
Le contexte transactionnel ne supprime pas cette portée. Le client ne reçoit
aucun reversement du seul fait de la validation ; les effets suivent le compte
du commerçant et les règles existantes. Des validations sans prestation réelle,
contestations et corrections financières restent possibles.
Pour l'animation, une validation abusive peut également déclencher une progression
ou une récompense prévue par ses règles ; cet effet doit être visible et traçable.

L'utilisateur retient ce compromis de périmètre ; le parcours n'est pas présenté
comme une preuve de présence, de réalisation effective ou d'identité individuelle.
La capture du PIN et l'affichage trompeur sur un appareil tiers restent des risques
documentés. Les critères initiaux de non-capture et d'écran indépendant sont donc
remplacés explicitement par des limites de droits et des contrôles vérifiables.

Protections incluses dans le cadrage :

- Après 5 saisies incorrectes en 15 minutes pour un même commerce, blocage du
  canal PIN pendant 15 minutes, tous téléphones et demandes confondus ; une nouvelle
  demande ne remet pas le compteur à zéro. Contrôles réseau complémentaires à concevoir.
- Déblocage automatique après 15 minutes, sans prolongation par les tentatives
  pendant le blocage ; un PIN expiré ou invalidé reste inutilisable.
  L’accès professionnel et le scan QR restent disponibles selon leurs règles habituelles.
- Révocation rapide, durée bornée et suivi des échecs ; aucune nouvelle alerte de volume
  inhabituel ni seuil de volume/valeur spécifique au PIN en V1. Les règles métier
  Animation communes au QR restent applicables, notamment le résultat ANOMALIE.
- Audit sans secret et notification dans Localeo Pro au commerçant à chaque validation
  par PIN réussie, coffret ou animation, sans email de validation ; les alertes
  servent à détecter les abus, pas à autoriser la consommation a posteriori.
- Chaque tentative de validation PIN, pour un coffret ou une animation, porte
  une date serveur, le commerce, la cible métier, le résultat et son motif,
  le mode PIN, la version du moyen et une corrélation exploitable par le support.
  Les consultations suivent les habilitations ; le PIN partagé n'identifie pas le salarié.
- Procédure de contestation et d'investigation via le support existant ; aucune
  annulation automatique d'argent par simple clic « contester ».

Conservation : reprendre les durées existantes de Localeo pour les validations et
événements de sécurité, sans durée propre à E70 ; leur adéquation et les sources
applicables seront vérifiées pendant la spécification. La procédure technique de
prise en charge d’une compromission reste à détailler. Aucun gel automatique de
reversements n’est ajouté implicitement.

Référence de conception : [OWASP, autorisation des transactions](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html).
Séparer authentification et finalité, borner les demandes et vérifier côté serveur
les données autorisées ; cette référence ne certifie pas le compromis Localeo.

## Exclusions et découpage

V1 étendue le 5 octobre : prestations d'instances de coffrets et actions terrain
d'animation, une seule prestation ou action par demande, backend
joignable, aucun matériel ni installation de l'application commerçant sur le
téléphone client. Le client équipé est une condition de ce mode, pas une obligation
pour tous les clients de Localeo.

Exclus : validation offline, validation par lots, administration des animations,
QR commerçant statique autorisant une validation, session professionnelle sur le
téléphone client, nouveaux transferts/remboursements ou changement du bénéficiaire
des fonds. Le secours E9 et le parcours normal restent disponibles selon leurs règles.

Découpage de travail : contexte transactionnel et invariants communs ; gestion du
PIN et contrôle serveur ; interface client ; gestion des incidents, documentation
et démonstration. L'ouverture du mode exige que ces éléments forment un parcours complet.

## Critères d'acceptation

Les identifiants CA-01 à CA-16 sont conservés et recadrés selon la décision PIN.
CA-04, CA-09 et CA-11 ne demandent plus une preuve indépendante de l'écran ni une
non-capture impossible à garantir sur un téléphone tiers. CA-17 à CA-28 complètent
le cycle de vie et les cas limites. CA-29 à CA-34 couvrent l'extension Animation
et la séparation avec les accès salariés : **34 critères**. Les critères transverses
de gestion du PIN, refus, protection des secrets et reprise s'appliquent aux deux parcours.

| Critère | Acteur / préconditions | Action | Résultat observable et refus |
| --- | --- | --- | --- |
| E70-CA-01 | Client disposant du droit requis, prestation éligible | Préparer la validation | Demande bornée sur ce seul téléphone, commerce déduit de la prestation ; aucune consommation, réservation exclusive ou session pro créée |
| E70-CA-02 | Client connaissant le commerce mais sans PIN valable | Confirmer ou falsifier le commerce | Refus serveur, y compris avec QR/référence publique ; le PIN ne dispense pas du droit client |
| E70-CA-03 | Commerce suspendu, mode désactivé, PIN absent, non encore valable, expiré, bloqué ou révoqué | Soumettre le PIN | Refus sans effet métier, état courant contrôlé à la confirmation |
| E70-CA-04 | Demande en attente et PIN valable | Lire, saisir le PIN et confirmer | Récapitulatif explicite sur le téléphone, validation de cette prestation ; connaissance du PIN tracée, aucune prétention de preuve indépendante de l'écran |
| E70-CA-05 | Demande préparée pour une prestation | Changer commerce, instance, prestation ou finalité | Refus de substitution ; nouvelle demande et nouvelle saisie requises, aucune capacité générale après contrôle du PIN |
| E70-CA-06 | Demande expirée après 5 minutes, annulée ou déjà validée | Rejouer une requête | Aucune nouvelle consommation ; reçu existant accessible uniquement avec le droit client requis |
| E70-CA-07 | Deux appareils, double clic ou validation normale concurrente | Consommer le même droit | Une seule consommation et un seul effet métier de reversement, résultat cohérent |
| E70-CA-08 | PIN valable mais droit déjà consommé, expiré ou coffret non utilisable | Confirmer | Mêmes refus métier que le parcours normal ; aucune éligibilité contournée |
| E70-CA-09 | Succès, refus, retour arrière ou abandon | Inspecter l'application et reprendre | Aucun PIN conservé par Localeo dans stockage/logs/analytics, champ vidé, aucune session professionnelle ; la capture par un appareil malveillant reste un risque déclaré |
| E70-CA-10 | Timeout après soumission ou reprise après expiration du PIN | Consulter le résultat | État serveur accessible avec le droit client, sans nouvelle saisie pour relire un succès acquis ni double consommation |
| E70-CA-11 | PIN compromis et droits clients contrôlés | Tenter un autre usage | Aucun accès professionnel, aucune prestation d'un autre commerce ni validation sans droit client ; réutilisation possible dans le périmètre jusqu'à expiration/révocation explicitement documentée |
| E70-CA-12 | Opérateur habilité face à une compromission | Diagnostiquer et révoquer selon ses droits | Admin/Backoffice autorisés à invalider, Lecteur/Finance seuls refusés ; intervention tracée et usages futurs refusés, aucun affichage du PIN |
| E70-CA-13 | Validation acceptée ou refusée | Consulter reçu et audit | Commerce, prestation, mode PIN, version du moyen et corrélation ; pas de PIN ni de secret client, pas d'attribution à un salarié non identifié |
| E70-CA-14 | PIN indisponible/bloqué, demande expirée ou réseau interrompu | Tenter le parcours | Refus/reprise compréhensibles, aucune validation offline ou par défaut ; accès aux alternatives existantes sans contournement |
| E70-CA-15 | Commerce utilisant la validation normale | Activer, désactiver ou bloquer le mode PIN | Validation normale et authentification professionnelle préservées, hors suspension métier du commerce |
| E70-CA-16 | Commerçant et opérateur pilote | Suivre les guides et réaliser nominal/refus/reprise | Notice commerçant et guide ERP expliquent préparation, validité, révocation, risques et incidents ; recette mobile et démonstration couvrent les cas |
| E70-CA-17 | Commerçant principal authentifié, mot de passe vérifié depuis 15 minutes maximum | Créer/activer son PIN | Opération limitée à son commerce, secret de 6 chiffres généré automatiquement, sans suites simples ni répétitions, un seul PIN actif commun aux deux parcours et validité explicite ; impossible avec le seul PIN ou un accès client |
| E70-CA-18 | PIN avec début et fin de validité | Valider aux limites temporelles | Heure serveur fait foi, refus avant le début et dès la fin ; dates affichées sans ambiguïté, activation immédiate, 7 jours par défaut, durée de 1 à 30 jours entiers, refus hors de ces bornes |
| E70-CA-19 | PIN actif ou expiré | Remplacer/renouveler | Nouveau PIN/version et nouvelle validité ; ancien PIN inutilisable, aucune réactivation silencieuse d'un secret ancien |
| E70-CA-20 | Demande ouverte avant révocation ou désactivation | Révoquer puis confirmer | Ancien PIN refusé malgré la demande préexistante ; les validations déjà réalisées ne sont pas annulées |
| E70-CA-21 | Révocation/remplacement/suspension et validation simultanés | Exécuter les deux opérations | Ordre cohérent et vérifiable ; aucune validation autorisée par une ancienne version après révocation effective, ni effet partiel |
| E70-CA-22 | PIN oublié, client ou session pro insuffisante | Demander récupération/remplacement | Aucun renvoi ni lecture du PIN actuel ; invalidation/régénération faciles via Localeo Pro ; support habilité autorisé à invalider et aider à récupérer l’accès, sans consulter le PIN, avec audit ; jamais via le seul coffret |
| E70-CA-23 | Commerçant ou opérateur consultant les données | Consulter/exporter état et historique | Métadonnées autorisées seulement ; secret non récupérable en clair, aucune émission dans logs, notifications ou exports |
| E70-CA-24 | Tentatives réparties sur plusieurs demandes/adresses | Essayer des PIN ou créer massivement des demandes | 5 erreurs en 15 minutes par commerce bloquent le seul canal PIN 15 minutes, tous appareils/demandes confondus ; déblocage automatique sans prolongation par les essais pendant le blocage ; aucun rétablissement d’un PIN expiré/révoqué, scan préservé |
| E70-CA-25 | Mode non activé ou désactivé | Migrer les comptes ou créer un coffret | Aucun PIN prédéfini ni activation automatique ; aucun changement des droits ou du parcours normal |
| E70-CA-26 | Changement du PIN ou validation réussie | Notifier et mettre à jour l'historique | Chaque succès PIN Coffret/Animation produit une notification dans Localeo Pro pour le commerçant, sans email de validation ; changements et blocages notifiés dans Localeo Pro et par email au principal, contenu sans secret ; échec/rejeu sans double notification de succès ni nouvelle consommation |
| E70-CA-27 | Droit client révoqué/rotaté depuis l'ouverture, ou simple identifiant public | Confirmer/consulter une demande | Contrôle serveur du droit actuel ; refus sans consommation ni divulgation du résultat |
| E70-CA-28 | Commerçant constatant une validation litigieuse | Signaler l'incident et révoquer le PIN | Référence exploitable par le support ; historique préservé, aucune annulation ou opération financière automatique non autorisée |
| E70-CA-29 | Participant disposant du droit requis, animation et action terrain éligibles, commerce autorisé | Préparer puis confirmer avec son PIN valable | Demande liée à ce participant, cette animation, cette action et ce commerce ; effet identique au parcours terrain normal, reçu serveur et aucune administration accessible |
| E70-CA-30 | Participant sans droit actuel, animation/action inéligible ou commerce non autorisé | Ouvrir ou confirmer une demande avec un PIN valable | Refus selon les règles du moteur d'animation, sans progression ni récompense ; réévaluation des droits et de l'éligibilité à la confirmation |
| E70-CA-31 | Demande Animation ouverte | Substituer participant, animation, action, commerce ou finalité coffret | Refus serveur ; nouvelle demande et nouvelle saisie nécessaires, aucun transfert d'autorisation entre finalités |
| E70-CA-32 | Validation QR et PIN concurrentes, plusieurs appareils, double clic ou rejeu | Valider la même action terrain | Une seule progression et aucun double octroi de récompense ; reprise et reçu cohérents avec le résultat acquis |
| E70-CA-33 | Validation Animation acceptée ou refusée | Consulter les traces autorisées | Date, commerce, participant selon habilitation, animation/action, mode PIN, version du moyen, résultat/motif et corrélation auditables ; aucun secret ni attribution à un salarié non identifié |
| E70-CA-34 | Accès salarié limité de l'EPIC 72 ou seule connaissance du PIN | Créer, renouveler, révoquer ou consulter les paramètres du PIN du commerce | Refus serveur ; gestion réservée au commerçant principal authentifié et à l'assistance explicitement habilitée |

## Propriétaires et preuves à préparer

- Domaine `identite_acces` : cycle de vie/version du PIN, validité, habilitations,
  limitation des tentatives et révocation ; adaptateur de stockage/vérification du secret.
- Domaine de validation `exploitation` : demande, consommation et refus communs ;
  règles du coffret et du reversement restent chez leurs propriétaires actuels.
- Domaine d'animation : éligibilité et droit participant, commerce autorisé,
  progression et récompenses ; aucun second moteur spécifique au PIN.
- Application : contrôle du droit client, orchestration atomique des contrôles et
  de l'effet, idempotence, notifications via mécanismes existants.
- Entrées : API espace commerçant (gestion), API client (demande/confirmation/reçu),
  ERP/support (incident autorisé). Pas de règle dupliquée dans les écrans ou batchs.

La spécification devra couvrir tests de domaine aux bornes temporelles, contrats
d'accès/refus, concurrence PostgreSQL, révocation du droit client et du PIN,
absence de secrets dans les traces, reprise réseau et recette mobile, ainsi que
concurrence QR/PIN Animation sans double progression ou récompense.
Ces preuves sont attendues, **pas exécutées à ce stade**.

## Impacts à instruire

| Sujet | Impact et dépendance |
| --- | --- |
| Backend | Concerné : PIN, contexte transactionnel, contrôle des droits client/participant, consommation commune et règles Animation, audit et notifications ; aucune nouvelle règle de calcul du reversement |
| Application Commerçant | Concernée : gestion du PIN, dates/états, révocation, oubli et historique ; accès professionnel nécessaire à la préparation |
| Marketplace / Localeo Live | Concerné : choix de prestation ou action terrain Animation, passage du téléphone, saisie PIN, refus, reçu et reprise ; droits client/participant requis à cartographier |
| ERP / Support | Concernés : état du mode/PIN sans secret, incidents et révocation selon habilitations ; lien avec [EPIC 69](../terminees/epic-69-profils-acces-erp-satellites-backlog.md), aucun rôle supplémentaire implicite |
| Animation | Concernée : contrats de validation terrain, éligibilité, commerce autorisé, progression/récompense et audit ; vérifier les consommateurs et vues de suivi concernés, sans ouvrir l'administration au porteur du PIN |
| Contrats API | Concernés : gestion authentifiée du PIN et finalité client distinctes ; sources canoniques ici, contrats embarqués/générateurs dans les dépôts consommateurs |
| Persistance / migrations | Concernées : vérificateur du PIN, version/dates/état, compteurs, demandes et audit ; aucune activation rétroactive ni PIN par défaut |
| Démonstration | Concernée : PIN fictifs, coffret et animation, droits participant et commerce autorisé/refusé, dates actives/expirées, révocation en cours de demande, blocage, concurrence QR/PIN, doublon et timeout ; aucun secret réel ou envoi externe |
| Documentation / exploitation | Concernées : guide ERP publié via le circuit documentaire, notice commerçant, oubli/compromission, suivi des anomalies et procédure de contestation |
| Onboarding | Dépendance [EPIC 68](../en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md) : préparation facultative du PIN et explication des risques, exercice sans consommation réelle |
| Accès salariés | Coordination [EPIC 72](../en-cours/epic-72-acces-salaries-validation-localeo-pro-backlog.md) : même règle de validation métier, identité nominative seulement via l'accès salarié ; ce rôle ne gère pas le PIN partagé |
| Déploiement | À spécifier : ordre backend/interfaces, activation maîtrisée, retour au parcours normal et compatibilité des versions ; aucun déploiement réalisé |

## Arbitrages et paramètres restant à spécifier

Décisions utilisateur reportées le 5 octobre 2026, complétées par la seconde série
d’arbitrages question par question. Les choix fonctionnels recensés sont résolus ;
restent l’implémentation de la conception technique, les preuves et la planification.

| Référence | Décision / proposition | Suite attendue |
| --- | --- | --- |
| E70-ARB-01 | **Résolu : parcours entièrement sur le téléphone client, sans dispositif supplémentaire** | Remplace l'orientation matérielle initiale |
| E70-ARB-02 | **Résolu : PIN dédié retenu et risque résiduel de capture borné par les droits accepté comme compromis produit** | Ne plus bloquer sur une équivalence anti-capture ; démontrer les restrictions, révocation et contrôles annoncés |
| E70-ARB-03 | **Étendu le 5 octobre 2026 : coffrets et validation terrain Animation, une action par demande, en ligne** | Remplace l'exclusion Animation du 1er octobre ; lots et administration Animation restent exclus |
| E70-ARB-04 | **Résolu : un seul PIN actif par commerce, commun aux coffrets et animations** | Gestion dans Localeo Pro par le principal ; salariés sans droit de gestion, PIN partagé sans identité individuelle |
| E70-ARB-05 | **Résolu : PIN automatique de 6 chiffres sans suites simples/répétitions ; activation immédiate ; 1 à 30 jours entiers, 7 par défaut ; demande valable 5 minutes** | 5 erreurs en 15 minutes par commerce bloquent le PIN 15 minutes, tous appareils/demandes confondus ; déblocage automatique sans prolongation pendant le blocage, scan préservé |
| E70-ARB-06 | **Résolu : remplacement avec mot de passe principal vérifié depuis 15 minutes maximum ; invalidation seule sans étape supplémentaire en session principale** | Support autorisé à invalider et aider à récupérer l’accès, sans lecture du PIN ; Admin/Backoffice autorisés, Lecteur/Finance seuls exclus, interventions auditées |
| E70-ARB-07 | **Résolu : chaque succès dans Localeo Pro uniquement ; changements/blocages dans Localeo Pro et par email au principal, sans secret** | Pas de nouvelle alerte de volume propre au PIN en V1 ; règles Animation communes au QR conservées ; conservation selon les durées existantes Localeo, rattachement établi le 7 octobre, traitements à tester |

La spécification V1 relie les 34 critères aux contrats et preuves attendues. La
prochaine phase implémente ces comportements ; le rattachement des nouveaux journaux
et demandes aux durées existantes reste un prérequis de purge/mise en service.
Aucun compte réel, migration appliquée, commit, push ou déploiement réalisé.

Rattachement documentaire de conservation établi le **7 octobre 2026** sur l’Annexe A : voir les [catégories, dates et preuves communes E70/E72](../../specifications/identite-acces/conservation-validations-acces.md). La limite de source est levée ; migrations 256/257 et traitement E70 testés localement le 7 octobre. Ordonnancement et recette cible restent préalables à la mise en service.
