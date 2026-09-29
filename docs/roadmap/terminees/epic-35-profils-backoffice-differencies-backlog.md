# Backlog Epic 35 - Profils back-office differencies

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : remplacer l'acces SQLAdmin unique par une gestion de comptes back-office differencies, avec roles, profils et permissions adaptees aux usages support, exploitation, finance et administration.
- Decision contexte : l'Epic 34 reutilise la session SQLAdmin actuelle en MVP ; cette epic porte l'evolution vers des profils back-office differencies.
- Decision MVP : introduire des utilisateurs back-office applicatifs, sans remettre en cause immediatement les ecrans SQLAdmin existants.
- Hors scope MVP : SSO entreprise, federation d'identite, MFA obligatoire, gestion fine champ par champ.

**Évolution cadrée le 28 septembre 2026 :** trois profils Lecteur, Backoffice et
Admin, décrits dans la section `E35-PROFILS-20260928` ci-dessous. Le statut
**Terminé** porte sur le périmètre historique ; cette évolution reste à spécifier
et à implémenter. Les stories historiques ne constituent pas sa preuve de livraison.

## Probleme

Le back-office actuel repose sur un identifiant administrateur unique configure par variables d'environnement. Ce modele convient au demarrage, mais il ne permet pas de distinguer les responsabilites, limiter les actions sensibles, tracer clairement l'acteur humain ni appliquer des droits differencies selon les profils.

## Risque business

- Des operateurs peuvent acceder a des zones ou actions qui ne correspondent pas a leur mission.
- Les actions sensibles sont moins maitrisables si tous les utilisateurs partagent le meme niveau d'acces.
- L'audit perd de la valeur si l'identite back-office n'est pas rattachee a un utilisateur distinct.
- Les surfaces internes comme Localeo Control ou les vues finance ont besoin de droits differencies.

## Risque technique

- SQLAdmin ne fournit pas automatiquement une gestion de roles applicatifs complete.
- Une migration trop large peut casser l'acces admin existant.
- Les routes `/internal/*` et les vues SQLAdmin doivent partager un controle d'acces coherent.
- Les permissions doivent rester simples pour eviter une matrice impossible a maintenir.

## Perimetre MVP

- Creer un referentiel `utilisateurs_backoffice`.
- Creer un referentiel de roles/profils back-office.
- Gerer les roles MVP :
  - `ADMIN`
  - `EXPLOITATION`
  - `SUPPORT`
  - `FINANCE`
  - `LECTURE_SEULE`
- Remplacer l'authentification admin unique par une authentification utilisateur back-office.
- Conserver une compatibilite de migration depuis `LOCALEO_ADMIN_USERNAME` / `LOCALEO_ADMIN_PASSWORD`.
- Stocker en session l'identite utilisateur et ses roles.
- Controler l'acces aux routes `/admin`, `/internal/*` et aux APIs internes sensibles.
- Appliquer les permissions aux vues/actions principales SQLAdmin.
- Auditer les connexions, deconnexions, echecs et actions sensibles avec `backoffice_user_id`.
- Documenter la matrice de permissions MVP.

## Hors perimetre MVP

- SSO OAuth/OIDC/SAML.
- MFA obligatoire.
- Delegation temporaire de droits.
- Droits par champ ou par ligne metier.
- Gestion multi-tenant.
- Workflow complet de validation de creation utilisateur.

## User Stories

1. `PRD-251` En tant qu'administrateur, je veux creer un utilisateur back-office afin de donner un acces nominatif aux operateurs.
   - Statut : `Termine`
   - Resultat attendu : un utilisateur back-office porte login, nom, email, statut, roles et dates de cycle de vie.
   - Resultat attendu : le mot de passe est stocke uniquement sous forme de hash robuste.

2. `PRD-252` En tant qu'administrateur, je veux affecter des roles a un utilisateur afin de limiter ses acces au perimetre utile.
   - Statut : `Termine`
   - Resultat attendu : les roles MVP `ADMIN`, `EXPLOITATION`, `SUPPORT`, `FINANCE`, `LECTURE_SEULE` sont disponibles.
   - Resultat attendu : un utilisateur peut porter un ou plusieurs roles.

3. `PRD-253` En tant qu'operateur back-office, je veux me connecter avec mon compte personnel afin que mes actions soient tracees nominativement.
   - Statut : `Termine`
   - Resultat attendu : la connexion SQLAdmin utilise le referentiel utilisateurs back-office.
   - Resultat attendu : la session contient l'identite utilisateur et ses roles.

4. `PRD-254` En tant que responsable securite, je veux que les routes internes verifient les permissions afin de proteger les actions sensibles.
   - Statut : `Termine`
   - Resultat attendu : les routes `/internal/*` peuvent exiger une permission ou un role.
   - Resultat attendu : un acces non autorise retourne un refus explicite et audite.

5. `PRD-255` En tant qu'administrateur, je veux que les vues SQLAdmin respectent les roles afin d'eviter l'exposition inutile d'ecrans.
   - Statut : `Termine`
   - Resultat attendu : les vues SQLAdmin peuvent etre masquees ou refusees selon les roles.
   - Resultat attendu : les actions `create`, `edit`, `delete` peuvent etre limitees par profil.

6. `PRD-256` En tant que profil support, je veux acceder aux ecrans de support sans acceder aux actions finance ou configuration critique.
   - Statut : `Termine`
   - Resultat attendu : le role `SUPPORT` accede aux messages, timeline, mode secours et aides operationnelles.
   - Resultat attendu : le role `SUPPORT` ne peut pas modifier les configurations sensibles ni les paiements.

7. `PRD-257` En tant que profil finance, je veux acceder aux reversements, paiements et indicateurs financiers sans administrer tout le catalogue.
   - Statut : `Termine`
   - Resultat attendu : le role `FINANCE` accede aux vues reversements, paiements, remboursements et indicateurs financiers.
   - Resultat attendu : les actions non financieres sensibles restent refusees.

8. `PRD-258` En tant que profil exploitation, je veux acceder aux batchs, notifications et Localeo Control afin de piloter l'activite quotidienne.
   - Statut : `Termine`
   - Resultat attendu : le role `EXPLOITATION` accede au dashboard operationnel, batchs, Localeo Control, emails/SMS/WebPush sortants.
   - Resultat attendu : les actions de configuration critique restent reservees a `ADMIN`.

9. `PRD-259` En tant qu'auditeur, je veux retrouver l'utilisateur back-office a l'origine d'une action afin d'ameliorer la tracabilite.
   - Statut : `Termine`
   - Resultat attendu : les evenements d'audit sensibles portent `backoffice_user_id`, login et roles utiles.
   - Resultat attendu : les anciennes actions restent consultables meme si elles n'ont pas d'utilisateur nominatif.

10. `PRD-260` En tant qu'exploitant, je veux migrer depuis l'admin unique sans rupture afin de ne pas bloquer l'acces au back-office.
    - Statut : `Termine`
    - Resultat attendu : un utilisateur `ADMIN` initial peut etre cree depuis la configuration existante.
    - Resultat attendu : la migration documente comment retirer progressivement l'admin unique.

## Regles de gestion

- Un utilisateur back-office desactive ne peut plus se connecter.
- Un utilisateur doit avoir au moins un role actif pour acceder au back-office.
- `ADMIN` dispose de tous les droits MVP.
- `LECTURE_SEULE` ne peut pas executer d'action destructive ou de modification.
- Les permissions sont verifiees cote backend, pas seulement par masquage IHM.
- Toute action sensible doit conserver un audit avec l'identite back-office quand elle existe.
- Les routes Localeo Control de l'Epic 34 exigent a minima `ADMIN` ou `EXPLOITATION`.

## Modele cible

### Utilisateur back-office

Table cible : `utilisateurs_backoffice`

- `id`
- `login`
- `email`
- `nom_affiche`
- `password_hash`
- `statut`
- `roles`
- `created_at`
- `updated_at`
- `last_login_at`
- `disabled_at`
- `disabled_reason`

### Permissions

MVP possible : permissions derivees des roles en code, documentees dans une matrice.

Evolution possible : table `permissions_backoffice` et table de liaison role/permission si la matrice devient trop grande.

## APIs et integration cible

- Adapter `AdminAuthBackend` pour charger les utilisateurs back-office.
- Ajouter helpers de controle :
  - `require_backoffice_session`
  - `require_backoffice_role`
  - `require_backoffice_permission`
- Adapter les routes `/internal/*` sensibles.
- Surcharger `is_accessible` / `is_visible` sur les vues SQLAdmin critiques.
- Ajouter une page SQLAdmin de gestion des utilisateurs back-office reservee a `ADMIN`.

## Lots d'implementation

### Lot 1 - Modele et migration

- Ajouter modele ORM `UtilisateurBackoffice`.
- Ajouter bootstrap/migration de table.
- Initialiser un utilisateur `ADMIN` depuis la configuration actuelle.

### Lot 2 - Authentification

- Adapter `AdminAuthBackend`.
- Stocker `backoffice_user_id`, `admin_username` et `roles` en session.
- Conserver une procedure de reprise admin en cas de mauvaise configuration.

### Lot 3 - Permissions routes internes

- Ajouter helpers de securite back-office.
- Proteger routes `/internal/*` et batchs sensibles.
- Auditer les refus d'acces.

### Lot 4 - Permissions SQLAdmin

- Ajouter une base de vue SQLAdmin permissionnee.
- Masquer/refuser les vues selon roles.
- Limiter create/edit/delete sur les vues critiques.

### Lot 5 - Gestion utilisateurs

- Ajouter vue SQLAdmin reservee `ADMIN`.
- Permettre creation, desactivation, changement de roles et reinitialisation mot de passe.

### Lot 6 - Documentation et tests

- Documenter la matrice de permissions.
- Ajouter guide exploitation migration admin unique.
- Tester login, refus, roles et audit.

## Definition of Done

- Les utilisateurs back-office nominaux existent.
- Les roles MVP sont disponibles et documentes.
- SQLAdmin utilise les comptes back-office pour authentifier les operateurs.
- Les routes internes sensibles verifient les roles ou permissions.
- Les vues/actions SQLAdmin critiques sont controlees par profil.
- Les actions sensibles sont auditees avec l'utilisateur back-office.
- La migration depuis l'admin unique est documentee et testee.

## Points arbitres restants

- Confirmer si le MVP impose seulement des roles en code ou une table de permissions administrable.
- Confirmer si le mot de passe oublie back-office est inclus au MVP ou traite dans une V2.
- Confirmer si la MFA est une V2 ou une exigence des le premier deploiement production.

## Évolution E35-PROFILS-20260928 — Lecteur, Backoffice et Admin

### Références et résultat attendu

- Demande du 28 septembre 2026 : proposer trois profils simples dans le backoffice
  Localeo, en séparant les fonctions métier des fonctions techniques/exploitation.
- Phase réalisée : **cadrage uniquement**, sans changement de comptes ni de droits.
- Rattachement : ce besoin prolonge directement l'EPIC 35. Réutiliser son backlog
  et son [architecture canonique](../../architecture/backend/epics/epic-35-profils-backoffice-differencies-architecture.md),
  sans créer une seconde epic de gestion des profils ni rouvrir sa clôture historique.
- Acteurs : administrateur attribuant les accès, opérateur Backoffice réalisant
  les opérations métier et Lecteur consultant l'activité.

Le besoin est une différence de responsabilité compréhensible à la connexion :
un lecteur peut consulter un coffret et son suivi de ventes sans le modifier ;
un opérateur Backoffice peut gérer le coffret et les opérations métier associées ;
seul l'Admin accède également aux outils techniques, à l'exploitation et à la
gestion des accès internes. L'accès ne dépend pas seulement du menu emprunté.

**Existant vérifié par lecture ciblée du backend local `9b9cba3`, sans recette
déployée :** l'[authentification interne](../../../../localeo-backend/app/infrastructure/admin/auth.py)
utilise un couple administrateur configuré et copie rôle/communes en session.
Aucun référentiel de comptes internes individuels ni écran d'attribution n'a été
identifié dans cette exploration. Les gardes [ERP](../../../../localeo-backend/app/security/erp.py)
admettent `ADMIN` et `EXPLOITATION`, avec communes limitées pour ce dernier ; les
[interfaces historiques](../../../../localeo-backend/app/security/backoffice.py)
restent ADMIN seules. Il n'existe pas de séparation générale lecture/écriture
dans le garde ERP. Le [registre des sessions](../../../../localeo-backend/app/infrastructure/persistence/admin_sessions.py)
porte notamment la révocation, mais pas le profil individuel demandé.

La [Vision 360 Achats](../../../../localeo-backend/app/api/vision_360_achats_api.py)
distingue déjà des lectures métier des données techniques réservées à ADMIN.
D'autres routeurs métier, comme les
[souscriptions Animation](../../../../localeo-backend/app/api/souscriptions_animation_erp_api.py),
réservent actuellement lectures et commandes à ADMIN. La
[navigation ERP](../../../../localeo-backend/app/infrastructure/erp/erp.js)
regroupe des opérations métier sous « Exploitation courante ». Ces faits
imposent une classification par capacité et une gestion effective des comptes ;
ajouter simplement un rôle accepté au garde ERP ouvrirait aussi ses mutations.

Le statut historique de l'EPIC 35 reste celui de la roadmap, mais ne prouve pas
que ses comptes nominatifs et cinq rôles sont tous disponibles dans le code
examiné. La spécification doit traiter cet écart, sans prendre les anciennes
stories terminées comme prérequis techniques acquis.

### Matrice cible demandée

| Capacité | Lecteur | Backoffice | Admin |
| --- | --- | --- | --- |
| Consulter le cœur métier : listes, recherche, indicateurs et détails | Oui | Oui | Oui |
| Créer, modifier, publier et exécuter les actions métier autorisées par le domaine | Non | Oui, tous les droits métier | Oui |
| Voir et utiliser les rubriques techniques et d'exploitation | Non | Non | Oui |
| Administrer les comptes, profils et permissions internes | Non | Non | Oui |

« Tous les droits » donne accès aux opérations existantes ; cela ne contourne
ni les invariants métier, ni les confirmations, l'audit, l'idempotence ou les
conditions d'éligibilité. Par exemple, un Backoffice peut demander un remboursement
par le parcours métier, sans pouvoir modifier directement les écritures financières.
L'Admin conserve ses capacités actuelles ; ce cadrage ne crée pas un accès
supplémentaire aux secrets ni des fonctions de modification absentes du produit.

Les profils décrivent des capacités. Les périmètres territoriaux ou d'organisation
déjà attribués restent une dimension distincte : aucune migration ne les élargit
silencieusement. La portée globale par défaut des nouveaux comptes sera explicitée
en spécification.

### Frontière métier / technique à décliner par action

Classification proposée pour préparer la matrice exhaustive :

| Périmètre | Traitement cible |
| --- | --- |
| Référencement des territoires, commerçants, prestations, coffrets et commercialisation | Cœur métier : lecture Lecteur, gestion Backoffice/Admin. |
| Achats, bénéficiaires, service client, validations, remboursements, paiements, facturation, reversements et abonnements | Cœur métier : lecture Lecteur, opérations Backoffice/Admin selon les règles existantes. Les outils de maintenance des flux restent distincts. |
| Animations et partenaires, médias éditoriaux, documents métier | Cœur métier pour leurs parcours opérateur ; les comptes clients/commerçants/partenaires ne sont pas assimilés aux comptes d'administration interne. |
| Configuration d'environnement, logs, diagnostic technique, supervision, Localeo Control, ordonnancement, batchs, files techniques, reprises de webhooks, sauvegardes, migrations, jeux de démonstration | Technique/exploitation : Admin uniquement. |
| Gestion des utilisateurs et habilitations du backoffice, sessions internes et clés d'accès | Administration interne : Admin uniquement. |
| Audit global et traces techniques, dont la vue Audit de l'EPIC 65 | Proposition : Admin uniquement. L'historique métier utile d'un dossier reste consultable sous une projection limitée. |
| Notifications et documents | Lire une pièce existante ou l'historique métier relève de la consultation ; envoyer, régénérer ou publier constitue une action métier. Rejouer un transport, inspecter un payload ou paramétrer un fournisseur relève de l'exploitation. |

Les [conventions actuelles de navigation](../../architecture/transverse/conventions-backoffice.md)
rangent notamment des validations et incidents terrain dans « Exploitation ».
Le nom d'un menu ne suffit donc pas à classifier une capacité. Reclasser les
opérations métier nécessaires, sans exposer leur console technique aux deux
profils métier. Appliquer cette séparation aux vues mixtes, indicateurs, résultats
de recherche, liens, exports et données chargées en arrière-plan.

Pour le Lecteur, consulter ne doit déclencher aucune mutation métier, même si
une route actuelle utilise GET : pas de recalcul persisté, synchronisation Stripe,
création de document, envoi ou relance. La gestion de sa session et la traçabilité
de ses consultations restent possibles. Les exports de données métier existantes
sont des lectures sous les mêmes périmètres et règles de masquage ; leur liste
exacte et le traitement des exports générés seront précisés. Aucun export brut
technique ni lien donnant implicitement une capacité d'action n'est admis.

### Habilitations, sessions et transition

**Invariant cible :** un Lecteur ne peut provoquer aucune écriture métier ;
un Lecteur ou Backoffice ne peut lire ni commander une fonction technique,
d'exploitation ou d'administration interne, quelle que soit l'entrée utilisée.
Le domaine `identite_acces` porte la politique de capacités ; l'application la
fait appliquer avant toute lecture sensible ou commande. ERP, SQLAdmin, API,
exports et traitements déclenchés par un humain doivent partager cette politique.
Un traitement automatique conserve son identité de service et ne devient pas
une manière de contourner le profil de son demandeur.

La navigation n'affiche que les rubriques autorisées et propose un accueil métier
aux deux profils concernés. Une URL directe ou un appel construit manuellement
est refusé côté serveur sans charger les données interdites. Aucune nouvelle
rubrique non classifiée n'est ouverte par défaut aux profils métier.

Proposition d'administration : **un profil produit explicite par compte**, parmi
les trois choix demandés. L'implémentation peut réutiliser des permissions, mais
ne doit pas additionner des anciens rôles cachés qui rendent un Lecteur écrivain
ou un Backoffice exploitant. Seul l'Admin attribue ou change le profil ; les
opérateurs ne peuvent pas modifier leurs propres habilitations.

L'historique décrit cinq rôles cumulables : `ADMIN`, `EXPLOITATION`, `SUPPORT`,
`FINANCE`, `LECTURE_SEULE`. L'existence réelle de comptes portant ces rôles doit
être vérifiée ; leur conversion éventuelle vers trois profils demande un inventaire
et une correspondance explicite, avec prévisualisation des gains/pertes de droits.
Ne pas transformer automatiquement un EXPLOITATION en Admin ni SUPPORT/FINANCE
en Backoffice. Conserver les Admin existants et un accès de reprise vérifiable ;
empêcher une transition supprimant le dernier administrateur actif utilisable.
Les anciens rôles ne sont plus un quatrième profil caché après la transition.

Une baisse de droits ou une désactivation est prise en compte dès la requête
protégée suivante, y compris dans les autres onglets et avec un ancien formulaire
déjà ouvert. Prévoir l'invalidation ou la réévaluation des sessions, ainsi que la
revalidation des actions différées. La durée ou le mécanisme de cache ne doit pas
permettre de conserver temporairement une permission révoquée.

### Dépendances et décisions à faire évoluer

- [EPIC 60 — ERP](epic-60-vision-360-commercialisation-backlog.md) : accueil,
  navigation, périmètres et commandes métier ; les rôles historiques ne suffisent
  pas à définir automatiquement les trois nouveaux profils.
- [EPIC 65 — Audit, paiements, reversements](../a-faire/epic-65-vues-erp-audit-paiements-reversements-backlog.md) :
  sa spécification V1.1 conserve un accès ADMIN exclusif (`E65-D02`). La nouvelle
  cible doit ouvrir les lectures métier paiements/reversements au Lecteur et au
  Backoffice, tout en maintenant Audit global côté Admin. Mettre à jour ses
  contrats et preuves pendant la spécification de cette évolution ; ne pas
  déclarer ses anciens tests de refus suffisants pour la nouvelle cible.
- [EPIC 51 — Vision 360 Achats](epic-51-vision-360-achats-backoffice-backlog.md) :
  préserver les protections des données personnelles ; les révélations aujourd'hui
  réservées à ADMIN doivent faire l'objet d'un arbitrage explicite, et non d'une
  exposition par le seul accès à un écran métier.
- [EPIC 66 — Atelier](../en-cours/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md)
  et [EPIC 67 — Communautés](../a-faire/epic-67-communautes-communes-coffrets-intercommunaux-backlog.md) :
  appliquer les capacités métier et les périmètres aux futurs parcours, sans
  rouvrir les règles de composition ou créer de droits intercommunaux implicites.

### Périmètre et exclusions

Inclus : classification des capacités, trois profils, comptes internes nominatifs
et leur administration, transition depuis l'accès configuré et migration des
comptes existants le cas échéant, ERP et SQLAdmin encore accessibles, protections serveur et
contrats internes, sessions, visibilité des données et exports, documentation et
recette de chaque profil. L'inventaire couvre les actions métier financières,
sans modifier leurs règles ou ajouter de nouvelles opérations financières.

Exclus : nouvel annuaire/SSO/MFA, éditeur de rôles personnalisés, refonte des profils
des applications publiques, commerçant et partenaire, nouvelles fonctionnalités
métier, suppression de l'audit et accès direct à l'infrastructure. Aucun compte,
secret, configuration ou droit de production n'est modifié au cadrage.

Découpage proposé : inventaire et matrice ; politique partagée et transition des
comptes/sessions ; interfaces et lecteurs ; recette complète et migration opérée.
Un menu simplifié seul ne constitue pas une livraison de cette évolution.

### Critères d'acceptation de l'évolution

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E35-PROF-01 | Admin, compte à créer ou modifier | Attribuer un profil | Trois choix explicites Lecteur/Backoffice/Admin ; profil effectif visible et modification auditée. Aucun cumul caché donnant plus de droits. |
| E35-PROF-02 | Lecteur authentifié | Rechercher et consulter les dossiers et indicateurs métier | Consultations autorisées dans son périmètre ; aucun menu ou contenu technique/exploitation. |
| E35-PROF-03 | Lecteur, URL/formulaire/API connu | Tenter création, édition, suppression, publication, remboursement, génération ou envoi | Refus serveur, aucune mutation métier ni effet externe, même par ancienne URL, action en masse ou lecture avec effet de bord. |
| E35-PROF-04 | Backoffice, données métier éligibles | Gérer catalogue, achats, support, animation et finance | Toutes les opérations métier classifiées sont accessibles ; règles du domaine, confirmations et audit conservés, aucune édition brute contournant ces règles. |
| E35-PROF-05 | Lecteur ou Backoffice | Ouvrir un écran/API technique ou exploiter un lien profond | Refus serveur sans divulgation, y compris SQLAdmin, exports et données de composants mixtes ; aucune action sur batchs, configuration ou files techniques. |
| E35-PROF-06 | Admin existant | Parcourir métier, exploitation et administration | Capacités actuelles conservées ; opérations métier toujours soumises aux règles et protections habituelles. |
| E35-PROF-07 | Lecteur ou Backoffice | Modifier un profil ou appeler l'administration interne | Refus sans modification de compte ou de droits ; aucun accès obtenu par paramètres envoyés par le navigateur. |
| E35-PROF-08 | Compte rétrogradé ou désactivé, plusieurs onglets ouverts | Réutiliser une session ou soumettre un ancien formulaire | Nouveaux droits appliqués dès la requête suivante ; aucune commande ou lecture interdite avec les anciennes permissions. |
| E35-PROF-09 | Comptes et rôles historiques inventoriés | Préparer et exécuter la conversion | Correspondance explicite, différences contrôlées, Admin et périmètres préservés ; aucun élargissement silencieux ni perte du dernier accès Admin utilisable. |
| E35-PROF-10 | Lecteur, dossier avec pièces et données sensibles | Consulter ou exporter des données métier | Même périmètre et même masquage que l'écran ; aucune génération métier, secret, payload technique ou capacité d'action transmise. |
| E35-PROF-11 | Chaque profil, vues paiements/reversements/audit disponibles | Ouvrir la vue puis une action liée | Lecture financière autorisée aux trois profils, actions métier à Backoffice/Admin ; audit global à Admin seul. Refus et liens cohérents avec la matrice actualisée de l'EPIC 65. |
| E35-PROF-12 | Interface ERP/SQLAdmin sur ordinateur ou petit écran | Naviguer avec clavier et liens enregistrés | Accueil et navigation adaptés, actions interdites absentes, refus explicite sur ancien lien ; aucune redirection forcée vers une rubrique interdite. |
| E35-PROF-13 | Commande différée ou module nouvellement intégré | Vérifier l'autorisation avant exécution | Politique partagée et capacité explicitement classifiée ; aucune autorisation par défaut ni contournement via compte de service. |

### Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Backend et domaine propriétaire | **Concerné :** `identite_acces`, chargement et contrôle de session, ERP, SQLAdmin, services de projection et commandes. Les domaines métier conservent leurs règles ; l'autorisation n'est pas réimplémentée par écran. |
| API et consommateurs | **Concerné :** authentification interne, profil/capacités, refus, projections et exports ; contrats documentaires canoniques et tests consommateurs. **À examiner :** lecteurs internes ou anciennes interfaces fondés sur un rôle nominal. |
| Autres applications | **Sans évolution fonctionnelle demandée** de Marketplace/Live, Commerçant et Animation : leurs profils utilisateurs restent propres. **À examiner :** routes ou permissions partagées afin d'éviter une régression de leurs sessions. |
| Persistance et comptes existants | **Concerné :** représentation du profil, rôles historiques, périmètres, versions/révocation des sessions, migration nominative et audit. Besoin de SQL et procédure de retour à préciser sans rétablir des permissions révoquées par défaut. |
| Générateur et fixtures | **Concerné :** profils des accès test/démo, jeux par rôle, sessions périmées et comptes historiques cumulant des rôles ; export/import/restauration à vérifier. Aucun identifiant ni donnée réelle ajouté à cette documentation. |
| Documentation fonctionnelle | **Concernée :** guide backoffice, matrice d'accès, conventions de navigation, architecture EPIC 35 et spécification EPIC 65 ; identifier clairement les tâches de chaque profil. |
| Exploitation et livraison | **Concerné :** inventaire avant migration, reprise Admin, invalidation des sessions, audit des changements/refus, ordre de livraison commun serveur/interfaces et recette après migration. Aucune preuve de production à ce stade. |

### Arbitrages de spécification et preuves attendues

Les trois profils et leur distinction métier/technique sont demandés. Restent à
préciser, sans réduire leurs principes :

1. La classification exhaustive des écrans/actions mixtes, des exports et de
   l'historique métier, avec l'audit global proposé comme réservé à Admin.
2. La correspondance nominative des rôles actuels vers les trois profils et la
   portée territoriale par défaut des nouveaux comptes ; aucun cumul hérité implicite.
3. Les champs personnels nécessaires au Lecteur et au Backoffice, et les permissions
   de révélation aujourd'hui réservées à ADMIN dans les visions 360.

La spécification prolonge l'architecture canonique de l'EPIC 35 selon le
[cycle d'epic](../../organisation/cycle-epic.md). Relier E35-PROF-01 à E35-PROF-13
aux preuves : politique pure d'autorisation, tests de refus applicatifs sans effet
métier, contrats des API/exports, parcours navigateur par profil, révocation
multi-onglets et migration sur fixtures isolées. Les contrôles documentaires de ce
cadrage ne valent ni ces tests, ni une implémentation, ni une recette déployée.
