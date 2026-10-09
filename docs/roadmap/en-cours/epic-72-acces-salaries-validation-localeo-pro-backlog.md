# EPIC 72 — Accès salariés limités à la validation dans Localeo Pro

## Références

- **EPIC-72**, créée le **5 octobre 2026**, état **En cours** ; priorité et livraison à planifier.
- Besoin exprimé : permettre aux salariés d'un commerce de valider des prestations de coffrets et des passages Animation sur leur mobile personnel, sans partager le compte principal ni disposer des autres droits de Localeo Pro.
- Identifiant recherché dans la documentation et les namespaces de la roadmap : aucune EPIC 72 préexistante relevée.
- [EPIC 70 — PIN sur le téléphone client](epic-70-validation-prestation-telephone-client-backlog.md) : parcours complémentaire, distinct de l'identité individuelle du salarié. Son extension Animation est demandée le même jour.
- [Scanner Coffret/Animation](../../specifications/epic-41-api/application-commercant.md), [validation des prestations](../../specifications/validation-prestations/README.md), [espace commerçant](../../specifications/espace-commercant/README.md).
- [EPIC 69](../terminees/epic-69-profils-acces-erp-satellites-backlog.md) : référence pour les invitations, sans réutiliser implicitement les rôles internes ERP ni rouvrir cette epic terminée.
- [EPIC 68](../en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md) : expliquer ces possibilités pendant l'onboarding, sans en faire une obligation d'activation.

- [Spécification V1 du 5 octobre 2026](../../specifications/epic-72-acces-salaries/README.md), [architecture et contrats](../../specifications/epic-72-acces-salaries/architecture-contrats.md), [matrice des 22 critères](../../specifications/epic-72-acces-salaries/verification-livraison.md). Aucun code livré par cette spécification.

## Problème et résultat attendu

Le besoin décrit des commerces employant des salariés sans flotte mobile d'entreprise. Le responsable doit pouvoir déléguer la validation quotidienne en conservant seul l'administration du commerce. Ce cadrage traduit le besoin ; il ne prétend pas constater l'absence de toute brique technique après audit du code.

Le responsable saisit l'email du salarié dans Localeo Pro. Le salarié reçoit une invitation, définit son propre mot de passe, se connecte sur son téléphone et accède directement à « Scanner un QR ». Il confirme la prestation ou le passage proposé et obtient un résultat serveur. Son identité et le commerce sont tracés séparément. L'installation d'une PWA et la possession d'un téléphone professionnel ne sont pas imposées.

## Périmètre

### Évolution PRO-SCAN-20261009-ETATS

Les critères E72-CA-07/09/11/18 sont précisés sans changer leurs identifiants :
l’état de chaque prestation Coffret est visible par couleur, icône et texte,
avec action explicite seulement lorsque disponible, confirmation serveur et
résultat incertain distingués. L’évolution s’applique au salarié et au responsable.
Voir la [présentation commune du scan](../../specifications/validation-prestations/scan-commercant.md#lisibilité-du-résultat-coffret--9-octobre-2026).

### Correctif E72-CORR-20261009-UX

Demande du 9 octobre : reprendre pour le salarié le menu et le style de l’accès
commerçant. Les critères E72-CA-06/09/18 conservent leurs identifiants : shell
commun, navigation Scanner/Historique selon capacités, menu du compte limité à
la récupération et à la déconnexion, en-tête mobile sur une ligne. Aucun nouveau
droit ; les URL interdites restent refusées et le scanner s’ouvre directement.
Les preuves figurent dans le [bilan E72](../../specifications/epic-72-acces-salaries/verification-livraison.md).

### Évolution E72-EVOL-20261009-ACCUEIL

Demande du 9 octobre : contextualiser l’invitation et rendre le scan immédiatement
utilisable après connexion. État **En cours** et identifiants des 22 critères
conservés. E72-CA-01/02 sont précisés : l’email indique le commerce rattaché,
l’origine de l’invitation (responsable du commerce), les droits limités, la
création d’un mot de passe personnel, l’échéance réelle du lien et la suite du
parcours dans Localeo Pro. E72-CA-06/18 sont précisés : arrivée directe sur le
scanner, tentative d’ouverture de la caméra sans bouton intermédiaire ; refus ou
indisponibilité expliqués avec saisie manuelle et réessai. L’autorisation du
navigateur reste requise ; la confirmation métier n’est jamais automatique.
Un résultat incertain à relire reste prioritaire sur un nouveau scan.

L’enrichissement éditorial est une évolution ; l’arrivée directe au scanner
précise et corrige le parcours déjà attendu. Aucun droit, durée d’invitation,
quota, schéma SQL ou nouveau paramètre d’environnement n’est ajouté. Les preuves
sont rattachées au [bilan E72](../../specifications/epic-72-acces-salaries/verification-livraison.md).

Décisions utilisateur reportées le 5 octobre 2026 : l’option est sans plafond de
salariés et désactivée par défaut. Seul Localeo peut l’activer ou la désactiver
pour un commerce depuis l’ERP : Admin et Backoffice autorisés, Lecteur et Finance
seuls exclus, avec traçabilité des interventions. Cette activation prépare une monétisation future ;
aucun tarif ni mécanisme de facturation n’est décidé ici. Le plafond de cinq
salariés précédemment envisagé et le comptage des invitations sont abandonnés.

La désactivation suspend immédiatement tous les accès salariés, y compris les
sessions ouvertes, sans supprimer les comptes ni l’historique et sans affecter
le compte principal. La réactivation rétablit automatiquement les accès suspendus
par l’option, avec nouvelle connexion obligatoire ; les accès révoqués individuellement
restent révoqués. Toutes les invitations en attente sont annulées à la désactivation
et ne redeviennent jamais utilisables après réactivation ; de nouvelles invitations
sont nécessaires pour les salariés qui n’avaient pas encore accepté. Le serveur contrôle l’option pour inviter, accepter une invitation
et utiliser l’accès salarié ; la gestion de l’option n’est jamais ouverte au commerçant.

- Compte individuel rattaché au commerce du responsable, avec rôle fixe de validation ; aucun partage du mot de passe principal.
- Gestion par le responsable des invitations, de leur renvoi et annulation, de la liste des salariés et de la révocation d'un accès, notamment au départ d'un salarié.
- Invitation à usage unique valable 24 heures ; création du mot de passe avant première connexion. Renvoi possible après expiration ; aucun mot de passe envoyé par email.
- Scanner unique Coffret/Animation, récapitulatif minimal, confirmation et résultat. « Valider une animation » signifie valider un passage ou une étape autorisée chez ce commerce, jamais administrer l'animation.
- Historique de toutes les validations du commerce en lecture seule, quel que soit leur auteur ou leur mode, sans chiffres d’affaires, reversements, exports financiers ou données clients inutiles.
- Déconnexion et récupération autonome du mot de passe par email : lien à usage unique
  valable 1 heure. Le changement invalide les sessions ouvertes sans réactiver un
  accès révoqué ni contourner une option désactivée ; aucun droit de gestion commerciale.
- Révocation effective sur les sessions déjà ouvertes ; une suspension du commerce continue d'interdire la validation selon les règles métier existantes.
- Contrôle des permissions côté serveur sur chaque entrée ; masquer les autres menus ne suffit pas.

Exclus : catalogue, coordonnées du commerce, facturation, finance, remboursements, annulation de validations, messagerie commerciale, gestion des animations et participants, invitation d'autres salariés, configuration ou consultation du PIN du commerce. Aucun rôle personnalisable ni validation hors ligne. Un seul commerce par email en V1 : aucun cumul salarié de plusieurs commerces ni responsable d’un commerce et salarié d’un autre ; pas de rattachement automatique.

L'accès salarié peut être livré indépendamment du PIN E70 ; les deux modes réutilisent les mêmes règles de validation et doivent coexister sans doubles effets.

## Critères d'acceptation

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E72-CA-01 | Responsable authentifié de A, option activée | Inviter un email | Invitation rattachée à A, rôle limité ; aucun choix libre d'un autre commerce accepté par le serveur |
| E72-CA-02 | Destinataire d'une invitation valide | Ouvrir le lien et définir son mot de passe | Accès individuel activé après acceptation ; aucun droit avant finalisation, aucun secret du responsable partagé |
| E72-CA-03 | Invitation expirée après 24 h, annulée ou déjà utilisée | Accepter ou rejouer | Refus sans activation ni élévation de droits ; deux acceptations concurrentes ne créent pas deux accès |
| E72-CA-04 | Responsable et invitation en attente | Renvoyer ou annuler | Ancien lien inutilisable ; état visible et erreur d'envoi récupérable sans accès actif prématuré |
| E72-CA-05 | Email déjà invité ou lié à un compte | Réinviter | Pas de doublon ni d'écrasement de mot de passe/rôle ; refus d’un rattachement à un autre commerce, même si l’email y est responsable |
| E72-CA-06 | Salarié actif sur mobile personnel | Se connecter | Scanner accessible ; aucun menu métier supplémentaire hormis l’historique de toutes les validations du commerce en lecture seule |
| E72-CA-07 | Salarié et QR coffret valide | Confirmer la prestation | Validation pour son commerce selon les règles existantes ; identité salarié auditée et effets financiers habituels uniques |
| E72-CA-08 | Salarié et QR Animation | Confirmer un passage | Même contrôle de participation du commerce, disponibilité du service, calendrier et éligibilité que le parcours courant ; aucune gestion de l'animation |
| E72-CA-09 | Salarié de A | Modifier une requête ou appeler directement une route de B ou une fonction interdite | Refus serveur ; aucun profil, historique ou effet métier d'un autre commerce accessible |
| E72-CA-10 | QR invalide, droit consommé/expiré ou commerce suspendu | Tenter de valider | Refus métier identique au compte principal, sans consommation ni progression supplémentaire |
| E72-CA-11 | Double clic, retry, deux salariés ou modes QR/PIN concurrents | Valider le même droit | Un seul effet métier, reversement/progression/récompense non dupliqués selon le parcours ; résultat serveur consultable après timeout |
| E72-CA-12 | Responsable révoquant un accès avec session ou transaction ouverte | Salarié confirme après révocation effective | Refus ; ordre concurrence révocation/validation déterministe, validations antérieures conservées |
| E72-CA-13 | Salarié connecté | Accéder à la gestion des salariés ou du PIN, y compris par API | Refus ; aucun droit d'inviter, de modifier un rôle, de créer/remplacer/révoquer ou lire le PIN |
| E72-CA-14 | Salarié autorisé, option activée | Consulter ou modifier filtres/identifiants | Toutes les validations de son seul commerce en lecture seule, périmètre appliqué côté serveur, données minimales, aucun export financier ni accès indu |
| E72-CA-15 | Responsable et auditeur habilité | Consulter les traces | Invitation, acceptation, renvoi, révocation, validation et refus traçables : acteur, commerce, cible, date, mode, résultat et corrélation ; sans mot de passe, jeton d'invitation ou secret QR |
| E72-CA-16 | Salarié ayant oublié son mot de passe ou quittant son téléphone | Récupérer son accès ou se déconnecter | Réinitialisation autonome par email, lien à usage unique valable 1 heure ; lien expiré ou rejoué refusé, changement invalidant les sessions ouvertes ; aucune élévation, réactivation d’un accès révoqué ou contournement de l’option désactivée ; données privées retirées de l’interface locale |
| E72-CA-17 | Compte principal existant | Migrer puis utiliser Localeo Pro | Droits existants conservés ; aucun salarié créé implicitement et aucun PIN rendu accessible aux salariés |
| E72-CA-18 | Mobile, permission caméra refusée ou réseau interrompu | Scanner, confirmer et reprendre | Message actionnable, aucun faux succès ni validation différée hors ligne ; reprise sans double effet |
| E72-CA-19 | Commerce nouveau ou existant | Initialiser l’option puis tenter de l’activer depuis Localeo Pro ou par API non habilitée | Option désactivée par défaut ; activation/désactivation réservées à Localeo depuis l’ERP à Admin/Backoffice ; refus pour Lecteur/Finance seuls, avec acteur, commerce, date et résultat audités |
| E72-CA-20 | Option activée, cinq salariés déjà actifs | Inviter et activer un sixième salarié | Aucun plafond de salariés ni réservation de place par invitation ; contrôles d’identité et d’invitation conservés |
| E72-CA-21 | Salariés connectés, transaction ou invitation ouverte | Localeo désactive l’option | Invitations en attente annulées ; accès salariés et acceptation/invitation refusés immédiatement, même via session ouverte ; aucun effet après désactivation effective, ordre concurrent déterministe ; comptes, historique et accès principal préservés |
| E72-CA-22 | Option désactivée, accès suspendus et accès révoqué individuellement | Localeo réactive l’option | Accès suspendus par l’option rétablis automatiquement après nouvelle connexion ; anciennes sessions et invitations annulées inutilisables, nouvelles invitations nécessaires ; accès révoqué toujours refusé |

Les critères E72-CA-01 à E72-CA-18 sont conservés et précisés ; E72-CA-19 à E72-CA-22 couvrent l’option ERP, soit **22 critères**.

## Invariants et preuves attendues

Le domaine backend `identite_acces` porte l'identité, le rattachement, les habilitations, l’option par commerce et leur révocation. Le domaine d'exploitation conserve les règles de consommation ; le domaine Animation conserve celles des passages et de la progression. L'application orchestre invitation/email, session, contrôles et audit ; les interfaces présentent les capacités autorisées. Le placement précis sera vérifié lors de la spécification.

Entrées à couvrir : API de gestion responsable, acceptation/récupération, authentification, validation Coffret/Animation, lecture d'historique, gestion de l’option dans l’ERP, outils support et traitements de notifications. Aucun batch ni outil interne ne doit contourner le rattachement actif ou l’option activée.

Preuves prévues : tests de domaine pour les droits et transitions ; tests API de refus et isolation entre commerces ; concurrence, révocation et désactivation/réactivation de l’option sur sessions ouvertes ; contrats frontend ; parcours mobile invitation/scan/refus/reprise ; audit sans secrets, annulation définitive des invitations et réinitialisation à usage unique aux bornes d’une heure. Ces tests ne sont pas exécutés au stade du cadrage.

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Backend | Concerné : identités salariées, rattachements, rôle, invitations, sessions, audit et orchestration des validations existantes |
| Localeo Pro / `localeo-commercant` | Concerné : gestion par le responsable, acceptation, connexion et navigation salarié, scanner et historique de toutes les validations du commerce |
| Marketplace / Live | À examiner : liens d'acceptation et coexistence avec E70 ; aucune administration salariée demandée sur la surface client |
| `localeo-animation` | À examiner : consommation des traces et projections ; aucun nouveau rôle partenaire ni écran d'administration demandé |
| ERP / Support | Concernés : activation/désactivation de l’option par commerce réservée à Localeo, audit et diagnostic ; Admin/Backoffice autorisés, Lecteur/Finance seuls exclus |
| API et consommateurs | Concernés : distinguer acteur salarié et commerce, permissions et historique ; sources canoniques ici, générateurs et contrats embarqués auprès des applications |
| Persistance et migrations | Concernées : identité/rattachement, invitation, option désactivée par défaut, suspension distincte de la révocation et attribution des traces ; préserver les comptes principaux et l'auteur des validations historiques |
| Démonstration et fixtures | Concernées : responsable, deux salariés, autre commerce, invitation expirée après 24 h, six salariés actifs, option désactivée/réactivée, accès révoqué, QR Coffret/Animation ; emails fictifs sans envoi réel, générateur conservé dans le backend |
| Documentation fonctionnelle | Concernée : notice responsable/salarié, onboarding E68, distinction compte individuel et PIN partagé E70 |
| Exploitation et livraison | Concernées : envoi/reprise email, délivrabilité, expiration, perte de téléphone et départ salarié, diagnostic sans secrets, compatibilité et ordre de livraison à spécifier |
| Calculs financiers | Pas de nouvelle règle demandée : réutiliser les effets de consommation existants et prouver leur unicité |

## Arbitrages résolus

| Référence | Décision attendue | Portée |
| --- | --- | --- |
| E72-ARB-01 | **Résolu : toutes les validations du commerce, en lecture seule** | Sans données financières ni accès aux autres commerces |
| E72-ARB-02 | **Résolu : invitation valable 24 heures, renvoi possible après expiration** | Désactivation : invitations en attente annulées définitivement ; nouvelles invitations après réactivation, aucune acceptation lorsque l’option est désactivée |
| E72-ARB-03 | **Résolu : un seul commerce par email en V1** | Pas de cumul responsable/salarié entre commerces, ni de fusion automatique de comptes |
| E72-ARB-04 | **Résolu : aucun plafond ; option par commerce, désactivée par défaut et pilotée uniquement par Localeo depuis l’ERP** | Remplace le plafond de cinq et son comptage ; monétisation future prévue, sans tarif ni facturation décidés |
| E72-ARB-05 | **Résolu : désactivation immédiate, sessions ouvertes comprises ; comptes et historique conservés** | Compte principal préservé ; réactivation automatique des accès suspendus par l’option, nouvelle connexion obligatoire, révocations individuelles conservées |
| E72-ARB-06 | **Résolu : gestion ERP de l’option par Admin et Backoffice, avec audit ; Lecteur et Finance seuls exclus** | Contrôles côté serveur sur activation et désactivation |
| E72-ARB-07 | **Résolu : récupération autonome par email, lien à usage unique valable 1 heure** | Changement invalidant les sessions ouvertes, sans rétablir un accès révoqué ou contourner l’option désactivée |
| E72-ARB-08 | **Résolu : reprendre les durées existantes Localeo pour les validations et événements de sécurité** | Rattachement établi le 7 octobre ; aucune durée propre à E72, traitements et preuves locales livrés le 8 octobre |

La seconde série d’arbitrages utilisateur complète le cadrage. La spécification V1
définit la conception, les contrats et les preuves attendues. L’implémentation et
les preuves locales sont consignées dans le bilan ci-dessous ; les choix
fonctionnels recensés sont résolus.

La durée du PIN est fixée dans E70 à 7 jours par défaut, configurable jusqu’à 30 jours ; elle ne conditionne pas le cadrage de l'accès salarié.

## Implémentation et mise en service

La [spécification V1](../../specifications/epic-72-acces-salaries/README.md) traduit les arbitrages et relie les 22 critères aux preuves et consommateurs selon le [cycle d’epic](../../organisation/cycle-epic.md). Implémentation backend/ERP et Localeo Pro réalisée localement après publication E70 ; aucune invitation réelle ni activation en production.

Rattachement documentaire de conservation établi le **7 octobre 2026** sur l’Annexe A : voir les [catégories, dates et preuves communes E70/E72](../../specifications/identite-acces/conservation-validations-acces.md). La limite de source est levée ; les migrations 258/259, traitements et tests sont livrés localement. Leur application et l’ordonnancement sur la cible restent des opérations de mise en service.


Le [bilan du 8 octobre](../../specifications/epic-72-acces-salaries/verification-livraison.md)
relie les critères aux tests métier, PostgreSQL, API, navigateur, contrats et
conservation. Le [guide opérateur](../../specifications/epic-72-acces-salaries/guide-utilisation-exploitation.md)
détaille configuration, remise des liens, activation ERP et reprise. Statut
**En cours** conservé : la recette pilote et la mise en service ne sont pas exécutées.
