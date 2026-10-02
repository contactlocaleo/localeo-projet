# EPIC 70 — Valider une prestation depuis le téléphone du client

## Références et décisions

- Identifiant : **EPIC-70** ; cadrage et recadrage du **1er octobre 2026**.
- État : **À faire** ; priorité et livraison à planifier.
- Besoin : un commerçant sans téléphone disponible doit pouvoir valider une
  prestation depuis le téléphone connecté du client, sans matériel supplémentaire.
- **Solution retenue par l'utilisateur : PIN de validation dédié**, géré par le
  commerçant depuis son accès professionnel, avec validité, renouvellement et
  révocation ; contexte transactionnel et parcours client à implémenter.
- Phase réalisée : **cadrage**, pas une spécification détaillée ni une implémentation.
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

## Problème et résultat attendu

Le commerçant n'a pas de téléphone au comptoir, mais le client présente son coffret
sur son propre téléphone. Le commerçant doit pouvoir vérifier la prestation et
confirmer sa consommation sans se connecter à son espace professionnel sur cet appareil.

Parcours cible : **le client choisit, le commerçant lit et saisit son PIN, Localeo
valide une seule prestation et affiche le résultat**. Le commerçant prépare et gère
son PIN en amont depuis son accès commerçant habituel ; cette préparation n'impose
pas de téléphone professionnel disponible le jour de la prestation.

Acteurs : détenteur d'un droit d'accès au coffret, commerçant, éventuel collaborateur
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

## Périmètre fonctionnel retenu

### 1. Contexte transactionnel de validation

Le serveur prépare une demande limitée à **une prestation d'une instance de coffret,
son commerçant et un droit client vérifié**. L'identité du commerçant est dérivée
de la prestation, jamais choisie librement dans une requête client.

- Identifiant opaque, finalité dédiée, création, expiration, état et corrélation.
- Données métier figées pour la demande ; changement de prestation ou de coffret
  exige une nouvelle demande et une nouvelle saisie du PIN.
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

Le commerçant peut activer le mode, créer son PIN dédié, consulter son état et ses
dates, le remplacer, le révoquer et désactiver le mode depuis son accès authentifié.
**Le PIN de validation ne peut jamais gérer son propre cycle de vie.**

- PIN distinct du mot de passe professionnel ; règles de longueur, génération ou
  choix et exclusion des valeurs triviales à spécifier.
- Début de validité (immédiat par défaut proposé), date/heure de fin obligatoires,
  durée maximale à définir ; heure serveur de référence et affichage local explicite.
- **Proposition V1 : un seul PIN actif par commerce**, versionné. Le remplacement
  rend l'ancien inutilisable ; le renouvellement crée un nouveau PIN, sans prolonger
  silencieusement un secret potentiellement compromis.
- Consultation des métadonnées et de l'historique, pas récupération du PIN en clair.
  PIN oublié : remplacement après vérification de l'accès professionnel.
- Réauthentification récente pour créer/remplacer/activer ; modalités à spécifier
  sans réintroduire un matériel obligatoire. Révocation d'urgence facilement accessible.
- Aucun PIN en clair en base, logs, traces, analytics, notifications ou exports ;
  mécanisme de vérification adapté à un secret de faible entropie à concevoir.
- Révocation, expiration, remplacement, désactivation du mode ou suspension du
  commerçant contrôlés au moment de l'effet métier, y compris pour une demande déjà ouverte.
- Notification de changement sur un contact déjà vérifié, sans communiquer le PIN.

En cas de course entre révocation et validation, l'ordre des opérations doit être
déterministe : une validation déjà engagée définitivement conserve sa trace ; après
révocation effective, aucune nouvelle validation ne peut être autorisée par l'ancien PIN.
La révocation n'annule ni une consommation passée ni son mouvement de reversement.

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

Prévoir clavier mobile accessible, erreurs compréhensibles sans révéler le PIN,
expiration pendant la saisie, abandon, réseau interrompu et consultation du résultat.
La suppression du champ limite la rétention par Localeo ; elle ne garantit pas
l'absence de capture sur le téléphone client.

## Sécurité proportionnée et risque résiduel retenu

Le PIN autorise uniquement une validation de prestation du commerce avec un droit
client valable. Il ne donne accès ni au profil, ni au catalogue professionnel,
ni aux autres coffrets, ni aux messages, ni aux coordonnées de paiement,
ni aux remboursements, ni à la gestion des accès ou du PIN.

**Un PIN capturé reste réutilisable pendant sa validité avec d'autres droits de
coffret accessibles à l'attaquant, pour les prestations de ce même commerce.**
Le contexte transactionnel ne supprime pas cette portée. Le client ne reçoit
aucun reversement du seul fait de la validation ; les effets suivent le compte
du commerçant et les règles existantes. Des validations sans prestation réelle,
contestations et corrections financières restent possibles.

L'utilisateur retient ce compromis de périmètre ; le parcours n'est pas présenté
comme une preuve de présence, de réalisation effective ou d'identité individuelle.
La capture du PIN et l'affichage trompeur sur un appareil tiers restent des risques
documentés. Les critères initiaux de non-capture et d'écran indépendant sont donc
remplacés explicitement par des limites de droits et des contrôles vérifiables.

Protections incluses dans le cadrage :

- Limitation des tentatives par commerce/version du PIN et demande, complétée par
  des contrôles réseau ; ouvrir une nouvelle demande ne remet pas le compteur à zéro.
- Blocage du canal PIN avec diagnostic et récupération maîtrisée, sans bloquer
  automatiquement l'accès professionnel ou la validation normale.
- Révocation rapide, durée bornée, suivi des échecs et volumes inhabituels.
- Audit sans secret et notification/récapitulatif au commerçant ; les alertes
  servent à détecter les abus, pas à autoriser la consommation a posteriori.
- Procédure de contestation et d'investigation via le support existant ; aucune
  annulation automatique d'argent par simple clic « contester ».

À préciser : seuils de volume/valeur et réaction (alerte ou blocage), fréquence des
notifications, conservation et prise en charge d'une compromission. Aucun gel
automatique de reversements n'est ajouté implicitement.

Référence de conception : [OWASP, autorisation des transactions](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html).
Séparer authentification et finalité, borner les demandes et vérifier côté serveur
les données autorisées ; cette référence ne certifie pas le compromis Localeo.

## Exclusions et découpage

V1 : prestations d'instances de coffrets, une prestation par demande, backend
joignable, aucun matériel ni installation de l'application commerçant sur le
téléphone client. Le client équipé est une condition de ce mode, pas une obligation
pour tous les clients de Localeo.

Exclus : validation offline, validation par lots, participations Animation,
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
le cycle de vie et les cas limites : **28 critères**.

| Critère | Acteur / préconditions | Action | Résultat observable et refus |
| --- | --- | --- | --- |
| E70-CA-01 | Client disposant du droit requis, prestation éligible | Préparer la validation | Demande bornée sur ce seul téléphone, commerce déduit de la prestation ; aucune consommation, réservation exclusive ou session pro créée |
| E70-CA-02 | Client connaissant le commerce mais sans PIN valable | Confirmer ou falsifier le commerce | Refus serveur, y compris avec QR/référence publique ; le PIN ne dispense pas du droit client |
| E70-CA-03 | Commerce suspendu, mode désactivé, PIN absent, non encore valable, expiré, bloqué ou révoqué | Soumettre le PIN | Refus sans effet métier, état courant contrôlé à la confirmation |
| E70-CA-04 | Demande en attente et PIN valable | Lire, saisir le PIN et confirmer | Récapitulatif explicite sur le téléphone, validation de cette prestation ; connaissance du PIN tracée, aucune prétention de preuve indépendante de l'écran |
| E70-CA-05 | Demande préparée pour une prestation | Changer commerce, instance, prestation ou finalité | Refus de substitution ; nouvelle demande et nouvelle saisie requises, aucune capacité générale après contrôle du PIN |
| E70-CA-06 | Demande expirée, annulée ou déjà validée | Rejouer une requête | Aucune nouvelle consommation ; reçu existant accessible uniquement avec le droit client requis |
| E70-CA-07 | Deux appareils, double clic ou validation normale concurrente | Consommer le même droit | Une seule consommation et un seul effet métier de reversement, résultat cohérent |
| E70-CA-08 | PIN valable mais droit déjà consommé, expiré ou coffret non utilisable | Confirmer | Mêmes refus métier que le parcours normal ; aucune éligibilité contournée |
| E70-CA-09 | Succès, refus, retour arrière ou abandon | Inspecter l'application et reprendre | Aucun PIN conservé par Localeo dans stockage/logs/analytics, champ vidé, aucune session professionnelle ; la capture par un appareil malveillant reste un risque déclaré |
| E70-CA-10 | Timeout après soumission ou reprise après expiration du PIN | Consulter le résultat | État serveur accessible avec le droit client, sans nouvelle saisie pour relire un succès acquis ni double consommation |
| E70-CA-11 | PIN compromis et droits clients contrôlés | Tenter un autre usage | Aucun accès professionnel, aucune prestation d'un autre commerce ni validation sans droit client ; réutilisation possible dans le périmètre jusqu'à expiration/révocation explicitement documentée |
| E70-CA-12 | Opérateur habilité face à une compromission | Diagnostiquer et révoquer selon ses droits | Trace de l'intervention et refus des usages futurs ; aucun affichage du PIN ni droit opérateur ajouté implicitement |
| E70-CA-13 | Validation acceptée ou refusée | Consulter reçu et audit | Commerce, prestation, mode PIN, version du moyen et corrélation ; pas de PIN ni de secret client, pas d'attribution à un salarié non identifié |
| E70-CA-14 | PIN indisponible/bloqué, demande expirée ou réseau interrompu | Tenter le parcours | Refus/reprise compréhensibles, aucune validation offline ou par défaut ; accès aux alternatives existantes sans contournement |
| E70-CA-15 | Commerce utilisant la validation normale | Activer, désactiver ou bloquer le mode PIN | Validation normale et authentification professionnelle préservées, hors suspension métier du commerce |
| E70-CA-16 | Commerçant et opérateur pilote | Suivre les guides et réaliser nominal/refus/reprise | Notice commerçant et guide ERP expliquent préparation, validité, révocation, risques et incidents ; recette mobile et démonstration couvrent les cas |
| E70-CA-17 | Commerçant authentifié avec vérification récente | Créer/activer son PIN | Opération limitée à son commerce, secret conforme à la politique et validité explicite ; impossible avec le seul PIN ou un accès client |
| E70-CA-18 | PIN avec début et fin de validité | Valider aux limites temporelles | Heure serveur fait foi, refus avant le début et dès la fin ; dates affichées sans ambiguïté, durée maximale appliquée |
| E70-CA-19 | PIN actif ou expiré | Remplacer/renouveler | Nouveau PIN/version et nouvelle validité ; ancien PIN inutilisable, aucune réactivation silencieuse d'un secret ancien |
| E70-CA-20 | Demande ouverte avant révocation ou désactivation | Révoquer puis confirmer | Ancien PIN refusé malgré la demande préexistante ; les validations déjà réalisées ne sont pas annulées |
| E70-CA-21 | Révocation/remplacement/suspension et validation simultanés | Exécuter les deux opérations | Ordre cohérent et vérifiable ; aucune validation autorisée par une ancienne version après révocation effective, ni effet partiel |
| E70-CA-22 | PIN oublié, client ou session pro insuffisante | Demander récupération/remplacement | Aucun renvoi ni lecture du PIN actuel ; remplacement via accès professionnel vérifié ou procédure support contrôlée, jamais via le seul coffret |
| E70-CA-23 | Commerçant ou opérateur consultant les données | Consulter/exporter état et historique | Métadonnées autorisées seulement ; secret non récupérable en clair, aucune émission dans logs, notifications ou exports |
| E70-CA-24 | Tentatives réparties sur plusieurs demandes/adresses | Essayer des PIN ou créer massivement des demandes | Limites cumulées effectives, blocage du seul canal PIN et récupération définie ; nouvelle demande ne remet pas les essais à zéro |
| E70-CA-25 | Mode non activé ou désactivé | Migrer les comptes ou créer un coffret | Aucun PIN prédéfini ni activation automatique ; aucun changement des droits ou du parcours normal |
| E70-CA-26 | Changement du PIN ou validation réussie | Notifier et mettre à jour l'historique | Destinataire professionnel vérifié, contenu sans secret ; échec/rejeu de notification ne consomme pas à nouveau la prestation |
| E70-CA-27 | Droit client révoqué/rotaté depuis l'ouverture, ou simple identifiant public | Confirmer/consulter une demande | Contrôle serveur du droit actuel ; refus sans consommation ni divulgation du résultat |
| E70-CA-28 | Commerçant constatant une validation litigieuse | Signaler l'incident et révoquer le PIN | Référence exploitable par le support ; historique préservé, aucune annulation ou opération financière automatique non autorisée |

## Propriétaires et preuves à préparer

- Domaine `identite_acces` : cycle de vie/version du PIN, validité, habilitations,
  limitation des tentatives et révocation ; adaptateur de stockage/vérification du secret.
- Domaine de validation `exploitation` : demande, consommation et refus communs ;
  règles du coffret et du reversement restent chez leurs propriétaires actuels.
- Application : contrôle du droit client, orchestration atomique des contrôles et
  de l'effet, idempotence, notifications via mécanismes existants.
- Entrées : API espace commerçant (gestion), API client (demande/confirmation/reçu),
  ERP/support (incident autorisé). Pas de règle dupliquée dans les écrans ou batchs.

La spécification devra couvrir tests de domaine aux bornes temporelles, contrats
d'accès/refus, concurrence PostgreSQL, révocation du droit client et du PIN,
absence de secrets dans les traces, reprise réseau et recette mobile.
Ces preuves sont attendues, **pas exécutées à ce stade**.

## Impacts à instruire

| Sujet | Impact et dépendance |
| --- | --- |
| Backend | Concerné : PIN, contexte transactionnel, contrôle des droits, consommation commune, audit et notifications ; aucune nouvelle règle de calcul du reversement |
| Application Commerçant | Concernée : gestion du PIN, dates/états, révocation, oubli et historique ; accès professionnel nécessaire à la préparation |
| Marketplace / Localeo Live | Concerné : choix de prestation, passage du téléphone, saisie PIN, refus, reçu et reprise ; droit client requis à cartographier |
| ERP / Support | Concernés : état du mode/PIN sans secret, incidents et révocation selon habilitations ; lien avec [EPIC 69](../en-cours/epic-69-profils-acces-erp-satellites-backlog.md), aucun rôle supplémentaire implicite |
| Animation | Hors validation de participations dans cette V1 ; contrôler la non-régression des consommateurs de services partagés |
| Contrats API | Concernés : gestion authentifiée du PIN et finalité client distinctes ; sources canoniques ici, contrats embarqués/générateurs dans les dépôts consommateurs |
| Persistance / migrations | Concernées : vérificateur du PIN, version/dates/état, compteurs, demandes et audit ; aucune activation rétroactive ni PIN par défaut |
| Démonstration | Concernée : PIN fictifs, dates actives/expirées, révocation en cours de demande, blocage, doublon et timeout ; aucun secret réel ou envoi externe |
| Documentation / exploitation | Concernées : guide ERP publié via le circuit documentaire, notice commerçant, oubli/compromission, suivi des anomalies et procédure de contestation |
| Onboarding | Dépendance [EPIC 68](epic-68-parcours-commercant-preparation-onboarding-backlog.md) : préparation facultative du PIN et explication des risques, exercice sans consommation réelle |
| Déploiement | À spécifier : ordre backend/interfaces, activation maîtrisée, retour au parcours normal et compatibilité des versions ; aucun déploiement réalisé |

## Arbitrages et propositions complémentaires

| Référence | Décision / proposition | Suite attendue |
| --- | --- | --- |
| E70-ARB-01 | **Résolu : parcours entièrement sur le téléphone client, sans dispositif supplémentaire** | Remplace l'orientation matérielle initiale |
| E70-ARB-02 | **Résolu : PIN dédié retenu et risque résiduel de capture borné par les droits accepté comme compromis produit** | Ne plus bloquer sur une équivalence anti-capture ; démontrer les restrictions, révocation et contrôles annoncés |
| E70-ARB-03 | V1 cadrée sur coffrets, une prestation par demande, en ligne | Animation et lots exclus ; extension distincte si demandée |
| E70-ARB-04 | Proposition V1 : un PIN par commerce ; gestion depuis l'accès commerçant et assistance habilitée | Confirmer le besoin de PIN par salarié ; ne pas attribuer une identité individuelle à un PIN partagé |
| E70-ARB-05 | Longueur/génération du PIN, durée maximale, durée de demande, tentatives et déblocage | Fixer les valeurs lors de la spécification selon risque et usage ; distinguer expiration du PIN et de la demande |
| E70-ARB-06 | Proposition : vérification récente de l'accès professionnel, renouvellement par remplacement | Définir récupération et permissions ERP ; aucune récupération via téléphone client |
| E70-ARB-07 | Alertes, seuils de volume/valeur, récapitulatif et conservation | Définir réaction et fréquence utiles sans multiplier les messages ; gel d'argent hors périmètre implicite |

La prochaine phase spécifie ces trois volets, les contrats et les preuves dans un
dossier canonique relié à l'index. Aucun dossier de spécification vide, compte réel,
migration appliquée, commit, push ou déploiement n'est créé par ce cadrage.
