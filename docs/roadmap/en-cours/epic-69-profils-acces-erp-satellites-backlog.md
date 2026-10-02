# EPIC 69 — Profils et sécurisation des accès ERP et applications internes

## Synthèse

- Identifiant : **EPIC-69**, disponible après recherche dans la roadmap commune.
- Statut : **En cours** ; revue de clôture du 2 octobre 2026 bloquée par **CA-18** (traçabilité des refus internes).
- Décision du 1er octobre 2026 : créer une nouvelle epic pour ce besoin.
- Rôles retenus : **Lecteur, Backoffice, Finance**, cumul explicite **Backoffice + Finance**.
- Garde-fou : **admin historique conservé**, SQLAdmin et commandes financières
  engageant de l'argent réservés à cet admin en V1.
- Surfaces : ERP, Support, Atelier et autres satellites internes ; Control reste admin.
- Référencement : création par l'admin et invitation email pour initialiser le mot de passe.
- Phase : **V1.4, évolution des scopes globaux en cours**, 27 critères conservés ; aucun accès réel ouvert ni déploiement effectué.
- [Roadmap commune](../README.md) ; [index des spécifications](../../specifications/INDEX.md).
  [Dossier E69](../../specifications/epic-69-acces-internes/README.md) produit le
  1er octobre : architecture/contrats, permissions, guide backoffice et preuves
  attendues. V1.2 : invitation 24 h, récupération admin et matrice fixe validées ;
  Finance via Support existant ; BUM, activation déjà à zéro et annulation impayée
  non active ouvertes à Backoffice. Implémentation et preuves locales détaillées dans le
  [bilan de vérification](../../specifications/epic-69-acces-internes/verification-livraison.md) ; recette déployée attendue.

## Évolution E69-SCOPES-GLOBAUX-20261002 — 2 octobre 2026

Revue de clôture : preuves locales V1.4 disponibles, recherche utilisateurs
corrigée et recettée. Les refus d'accès ne portent pas encore systématiquement
l'auteur interne et le scope demandé dans l'audit ; **CA-18 reste partiel**.
Le [bilan](../../specifications/epic-69-acces-internes/verification-livraison.md)
détaille l'écart, le lot de commit à préparer et les prérequis de déploiement.
Statut et chemin conservés ; aucun critère supprimé ou réduit.

Intervention suivante du 2 octobre, sur demande utilisateur : **base de test
migrée v250 → v253**, sauvegarde et contrôles après migration effectués ;
compatibilité v252 corrigée pour une table de notes précréée par l'ORM. Aucun
déploiement applicatif, commit/push, ni changement de démo/production. CA-18
reste ouvert ; preuves et reprise dans le même bilan.

**Décision utilisateur :** habilitations par scopes nommés, comme les batchs,
sans contexte de commune. Les profils internes Lecteur, Backoffice, Finance et
Backoffice + Finance gardent les mêmes droits fonctionnels, valables sur
**toutes les communes**. Le domaine `identite_acces` en reste propriétaire.

Cette évolution V1.4 remplace **E69-D06** (portées territoriales par attribution)
et les attentes territoriales des critères existants, **sans renuméroter CA-01
à CA-27**. L'élargissement est explicite ; il ne donne ni SQLAdmin, ni commandes
d'argent, ni administration interne aux profils métier. L'admin historique est
conservé. Les identités/API keys de batch restent séparées des sessions humaines.

- **Critères modifiés :** CA-01/02/04/09/10/11/19/20/21/23/27 pour attribution,
  consultation/commandes toutes communes, migration globale et absence de
  sélection territoriale. CA-08/13/14/15/16/22 pour contexte `scopes`, compatibilité
  et retrait des droits fonctionnels. Les IDs et restrictions fonctionnelles
  restent inchangés.
- **Contrat :** nouvelles attributions `{role}` ; ancienne forme GLOBAL avec
  liste de communes vide acceptée en compatibilité, toute forme COMMUNES refusée.
  `scopes:list[str]` reprend les identifiants exacts de la matrice ;
  `capabilities` demeure un alias GLOBAL, sans contexte de communes.
- **Données :** migration additive `v253_scopes_internes_globaux.sql` après
  v251/v252, conversion en GLOBAL vide ; `version` et `authorizationVersion`
  incrémentées pour les seuls comptes modifiés. Sessions conservées, autorité
  relue à chaque requête ; aucun changement de secret, état ou profil.
- **Livraison :** migration avant nouveau backend, en fenêtre de maintenance
  suspendant les commandes internes. Anciennes lignes COMMUNES rejetées par le
  nouveau modèle, anciens formulaires à recharger. Aucune nouvelle variable
  d'environnement ; aucune exécution distante par cette évolution documentaire.
- **Impacts :** backend, ERP/satellites embarqués, contrats, fixtures, générateur,
  restauration et guide. Aucun changement des gestionnaires Animation ni des
  comptes commerçants ; les trois frontends publics gardent leur authentification.
- **Preuves :** bilan V1.3 et audit du 2 octobre conservés comme historiques,
  sans valider cette évolution. Le [bilan V1.4](../../specifications/epic-69-acces-internes/verification-livraison.md)
  distingue les nouveaux tests exécutés, le reste à compléter et la recette cible.

**État : en cours, sans clôture.** Aucun commit, push, déploiement, email réel
ou changement de compte réel n'est effectué par cette tâche documentaire.

## Provenance et traçabilité

Le cadrage avait été rattaché à tort à une évolution de l'EPIC 35. Sur correction
explicite de l'utilisateur, il est transféré ici sans changer les décisions métier.
L'EPIC 35 conserve son historique et renvoie vers cette source unique.

Les 22 critères `E35-PROF-01` à `E35-PROF-22` deviennent `E69-CA-01` à
`E69-CA-22`, avec correspondance par suffixe identique. De même, `E35-ARB-01` à
`04` deviennent `E69-ARB-01` à `04`. Les références de cadrage
`E35-PROFILS-20260928`, `E35-SATELLITES-20261001` et `E35-FINANCE-20261001`
restent des repères de provenance ; le suivi courant est désormais E69.

## Références et cadrage

### Références et résultat attendu

- Demande du 28 septembre 2026 : proposer trois profils simples dans le backoffice
  Localeo, en séparant les fonctions métier des fonctions techniques/exploitation.
- Décisions du 1er octobre : conserver l'admin historique, protéger ERP et satellites,
  ajouter Finance aux rôles métier et permettre le cumul Backoffice + Finance.
- Phase historique initiale : **cadrage et spécification de conception**, sans changement de comptes ni de droits à cette étape.
- Rattachement : nouvelle **EPIC 69**, demandée explicitement par l'utilisateur le
  1er octobre 2026. L'[EPIC 35](../terminees/epic-35-profils-backoffice-differencies-backlog.md)
  et son [architecture historique](../../architecture/backend/epics/epic-35-profils-backoffice-differencies-architecture.md)
  constituent des antécédents ; leur clôture ne prouve pas la livraison de ce besoin.
- Acteurs : admin historique attribuant les accès, Backoffice gérant les opérations
  courantes, Finance suivant les dossiers financiers et Lecteur consultant l'activité.

Le besoin est une différence de responsabilité compréhensible à la connexion :
un lecteur peut consulter un coffret et son suivi de ventes sans le modifier ;
un opérateur Backoffice peut gérer le coffret et les opérations métier associées ;
Finance suit les paiements, reversements, factures et anomalies sans modifier le
catalogue ni engager de mouvement d'argent. Seul l'Admin accède aux outils techniques, à l'exploitation et à la
gestion des accès internes. L'accès ne dépend pas seulement du menu emprunté.

**Point de départ historique, vérifié par lecture ciblée du backend local `9b9cba3`, sans recette
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

| Capacité | Lecteur | Backoffice | Finance | Admin historique |
| --- | --- | --- | --- | --- |
| Consulter le cœur métier : listes, recherche, indicateurs et détails | Oui, toutes communes et selon masquage | Oui, toutes communes et selon masquage | Seulement les informations nécessaires au suivi financier | Oui |
| Gérer commerçants, onboarding, catalogue, animations, Support et Atelier | Non | Oui, par les parcours métier | Non | Oui |
| Consulter paiements, reversements, factures et justificatifs existants | Lecture métier autorisée | Lecture métier utile au traitement courant | Oui, avec exports financiers autorisés | Oui |
| Qualifier et suivre un dossier ou une anomalie financière | Non | Traitement courant du support, sans décision financière | Oui, via les actions de suivi existantes, sans écriture comptable brute | Oui |
| Exécuter un remboursement ou une autre commande financière engageant de l'argent | Non | Non | Non | Oui, selon les règles existantes |
| Ouvrir SQLAdmin, outils techniques, exploitation ou administration des comptes | Non | Non | Non | Exclusivement |

Les droits donnent accès aux opérations existantes ; ils ne contournent ni les
invariants métier, ni les confirmations, l'audit, l'idempotence ou les conditions
d'éligibilité. Backoffice et Finance peuvent documenter une demande de remboursement
dans un dossier existant ; son exécution reste réservée à l'admin. Aucun rôle
métier ne peut modifier directement les écritures financières ou forcer un statut PSP.
L'Admin conserve ses capacités actuelles ; ce cadrage ne crée pas un accès
supplémentaire aux secrets ni des fonctions de modification absentes du produit.

Les profils décrivent des scopes fonctionnels globaux. La migration V1.4 élargit
explicitement les anciennes attributions territoriales à toutes les communes.
Les nouvelles attributions sont globales sans choix territorial ; la portée
fonctionnelle reste exactement celle du profil prédéfini.

### Frontière métier / technique à décliner par action

Classification proposée pour préparer la matrice exhaustive :

| Périmètre | Traitement cible |
| --- | --- |
| Référencement des territoires, commerçants, prestations, coffrets et commercialisation | Cœur métier : lecture Lecteur, gestion Backoffice/Admin. |
| Achats, bénéficiaires, service client, validations et abonnements | Lecture métier sur toutes les communes ; gestion courante Backoffice/Admin. Les commandes engageant de l'argent restent Admin seules. |
| Paiements, factures, justificatifs, reversements et anomalies financières | Finance consulte, exporte et suit les dossiers autorisés ; Lecteur et Backoffice conservent la lecture métier nécessaire. Remboursements et autres commandes financières sensibles réservés à Admin ; aucune modification brute des montants, écritures ou états Stripe. |
| Animations et partenaires, médias éditoriaux, documents métier | Cœur métier pour leurs parcours opérateur ; les comptes clients/commerçants/partenaires ne sont pas assimilés aux comptes d'administration interne. |
| Configuration d'environnement, logs, diagnostic technique, supervision, Localeo Control, ordonnancement, batchs, files techniques, reprises de webhooks, sauvegardes, migrations, jeux de démonstration | Technique/exploitation : Admin uniquement. |
| Gestion des utilisateurs et habilitations du backoffice, sessions internes et clés d'accès | Administration interne : Admin uniquement. |
| Audit global et traces techniques, dont la vue Audit de l'EPIC 65 | Admin uniquement. L'historique métier utile d'un dossier reste consultable sous une projection limitée. |
| Notifications et documents | Lire une pièce existante ou l'historique métier relève de la consultation ; envoyer, régénérer ou publier constitue une action métier. Rejouer un transport, inspecter un payload ou paramétrer un fournisseur relève de l'exploitation. |

Les [conventions actuelles de navigation](../../architecture/transverse/conventions-backoffice.md)
rangent notamment des validations et incidents terrain dans « Exploitation ».
Le nom d'un menu ne suffit donc pas à classifier une capacité. Reclasser les
opérations métier nécessaires, sans exposer leur console technique aux trois
profils métier. Appliquer cette séparation aux vues mixtes, indicateurs, résultats
de recherche, liens, exports et données chargées en arrière-plan.

Pour le Lecteur, consulter ne doit déclencher aucune mutation métier, même si
une route actuelle utilise GET : pas de recalcul persisté, synchronisation Stripe,
création de document, envoi ou relance. La gestion de sa session et la traçabilité
de ses consultations restent possibles. Les exports de données métier existantes
sont des lectures sous les mêmes scopes fonctionnels et règles de masquage ; leur liste
exacte et le traitement des exports générés seront précisés. Aucun export brut
technique ni lien donnant implicitement une capacité d'action n'est admis.

### Habilitations, sessions et transition

**Invariant cible :** un Lecteur ne peut provoquer aucune écriture métier ;
Finance agit seulement sur le suivi financier autorisé ; Backoffice et Finance,
même cumulés, n'exécutent aucune commande engageant de l'argent en V1.
Aucun rôle métier ne peut lire ni commander une fonction technique,
d'exploitation ou d'administration interne, quelle que soit l'entrée utilisée.
Le domaine `identite_acces` porte la politique de capacités ; l'application la
fait appliquer avant toute lecture sensible ou commande. ERP, SQLAdmin, API,
exports et traitements déclenchés par un humain doivent partager cette politique.
Un traitement automatique conserve son identité de service et ne devient pas
une manière de contourner le profil de son demandeur.

La navigation n'affiche que les rubriques autorisées et propose un accueil métier
aux rôles concernés. Une URL directe ou un appel construit manuellement
est refusé côté serveur sans charger les données interdites. Aucune nouvelle
rubrique non classifiée n'est ouverte par défaut aux profils métier.

**Attribution retenue :** compte nominatif Lecteur, Backoffice, Finance ou cumul
explicite Backoffice + Finance. Lecteur représente la consultation seule ; il
n'est pas ajouté comme un rôle masquant les droits d'un autre profil. Le cumul
est affiché et audité, avec ses capacités effectives ; il n'accorde jamais les
privilèges de l'admin historique. La création d'autres administrateurs n'est pas
demandée. Seul l'admin attribue ou retire les rôles ; aucune auto-attribution.
Chaque scope accordé vaut pour toutes les communes. Le cumul est l'union des
scopes fonctionnels B et F ; il n'ajoute aucune fonction réservée à l'admin.
Aucun contexte territorial ni choix de communes n'est associé au compte interne.

L'historique décrit cinq rôles cumulables : `ADMIN`, `EXPLOITATION`, `SUPPORT`,
`FINANCE`, `LECTURE_SEULE`. L'existence réelle de comptes portant ces rôles doit
être vérifiée ; leur conversion vers les nouveaux rôles demande un inventaire
et une correspondance explicite, avec prévisualisation des gains/pertes de droits.
Ne pas transformer automatiquement un EXPLOITATION en Admin ni SUPPORT/FINANCE
en Backoffice. Conserver les Admin existants et un accès de reprise vérifiable ;
empêcher une transition supprimant le dernier administrateur actif utilisable.
Le nom historique `FINANCE` ne prouve pas l'équivalence avec la cible : inventorier
et retirer explicitement les éventuelles commandes d'argent héritées. Aucun
ancien rôle ne subsiste comme permission cachée après la transition.

Une baisse de droits ou une désactivation est prise en compte dès la requête
protégée suivante, y compris dans les autres onglets et avec un ancien formulaire
déjà ouvert. Prévoir l'invalidation ou la réévaluation des sessions, ainsi que la
revalidation des actions différées. La durée ou le mécanisme de cache ne doit pas
permettre de conserver temporairement une permission révoquée.

### Dépendances et décisions à faire évoluer

- [EPIC 60 — ERP](../terminees/epic-60-vision-360-commercialisation-backlog.md) : accueil,
  navigation, scopes et commandes métier ; les rôles historiques ne suffisent
  pas à définir automatiquement les nouveaux rôles et leur cumul autorisé.
- [EPIC 65 — Audit, paiements, reversements](../en-cours/epic-65-vues-erp-audit-paiements-reversements-backlog.md) :
  sa spécification V1.1 conserve un accès ADMIN exclusif (`E65-D02`). La nouvelle
  cible doit ouvrir les lectures métier paiements/reversements à Lecteur, Backoffice
  et Finance sur toutes les communes, tout en maintenant Audit global et commandes
  d'argent côté Admin. Mettre à jour ses
  contrats et preuves pendant la spécification de cette évolution ; ne pas
  déclarer ses anciens tests de refus suffisants pour la nouvelle cible.
- [EPIC 51 — Vision 360 Achats](../terminees/epic-51-vision-360-achats-backoffice-backlog.md) :
  préserver les protections des données personnelles ; les révélations aujourd'hui
  réservées à ADMIN doivent faire l'objet d'un arbitrage explicite, et non d'une
  exposition par le seul accès à un écran métier.
- [EPIC 66 — Atelier](../terminees/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md)
  et [EPIC 67 — Communautés](../a-faire/epic-67-communautes-communes-coffrets-intercommunaux-backlog.md) :
  appliquer les scopes fonctionnels globaux aux futurs parcours, sans
  modifier les règles métier de composition des coffrets ou communautés.

### Périmètre et exclusions

Inclus : classification des capacités, trois rôles métier et cumul Backoffice +
Finance, admin historique conservé, comptes internes nominatifs et leur
administration, ajout des comptes métier à l'accès configuré et migration des
comptes existants le cas échéant, ERP et SQLAdmin encore accessibles, protections serveur et
contrats internes, sessions, visibilité des données et exports, documentation et
recette de chaque profil. L'inventaire couvre les actions métier financières,
sans modifier leurs règles ou ajouter de nouvelles opérations financières.

Exclus : nouvel annuaire/SSO, éditeur de rôles personnalisés, refonte des profils
des applications publiques, commerçant et partenaire, nouvelles fonctionnalités
métier, suppression de l'audit et accès direct à l'infrastructure. Aucun compte,
secret, configuration ou droit de production n'est modifié au cadrage. Aucune
MFA n'est ajoutée par ce cadrage ; son éventuelle inclusion reste à arbitrer.

Découpage proposé : inventaire et matrice ; politique partagée et transition des
comptes/sessions ; interfaces et lecteurs ; recette complète et migration opérée.
Un menu simplifié seul ne constitue pas une livraison de cette évolution.

### Critères d'acceptation de l'évolution

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E69-CA-01 | Admin historique, compte métier à créer ou modifier | Attribuer les rôles | Choix explicites Lecteur, Backoffice, Finance ou Backoffice + Finance ; rôles et capacités effectifs visibles, modification auditée. Aucun cumul caché ni attribution du privilège admin historique via ce formulaire. |
| E69-CA-02 | Lecteur authentifié | Rechercher et consulter les dossiers et indicateurs métier | Consultations fonctionnellement autorisées sur toutes les communes ; aucun menu ou contenu technique/exploitation. |
| E69-CA-03 | Lecteur, URL/formulaire/API connu | Tenter création, édition, suppression, publication, remboursement, génération ou envoi | Refus serveur, aucune mutation métier ni effet externe, même par ancienne URL, action en masse ou lecture avec effet de bord. |
| E69-CA-04 | Backoffice, données métier éligibles | Gérer catalogue, onboarding, achats, support, animations et Atelier | Opérations courantes et trois actions ARB-06 autorisées : BUM du coffret, activation déjà à 0 €, annulation impayée non active ; scopes B globaux et règles métier conservés. Autres commandes d'argent refusées même avec Finance. |
| E69-CA-05 | Tout rôle métier, y compris Backoffice + Finance | Ouvrir un écran/API technique ou exploiter un lien profond | Refus serveur sans divulgation, y compris toute vue historique SQLAdmin, ses actions et exports, même portant sur des objets métier ; aucune action sur batchs, configuration ou files techniques. |
| E69-CA-06 | Admin historique | Parcourir métier, exploitation, SQLAdmin et administration après transition | Accès historique conservé et reprise vérifiable, sans dépendance à l'attribution d'un rôle métier ; opérations métier toujours soumises aux règles et protections habituelles. |
| E69-CA-07 | Tout rôle métier, seul ou cumulé | Modifier un profil ou appeler l'administration interne | Refus sans modification de compte ou de droits ; aucun accès obtenu par paramètres envoyés par le navigateur. |
| E69-CA-08 | Compte rétrogradé ou désactivé, plusieurs onglets ouverts | Réutiliser une session ou soumettre un ancien formulaire | Nouveaux droits appliqués dès la requête suivante ; aucune commande ou lecture interdite avec les anciennes permissions. |
| E69-CA-09 | Comptes et rôles historiques inventoriés | Préparer et exécuter la conversion | Correspondance explicite, différences contrôlées et Admin préservé ; V1.4 convertit les attributions en GLOBAL vide avec versions adaptées ; aucun élargissement fonctionnel ni perte du dernier accès Admin utilisable. |
| E69-CA-10 | Rôle métier, dossier avec pièces et données sensibles | Consulter ou exporter les données autorisées | Mêmes scopes fonctionnels globaux et même masquage que l'écran ; Finance n'obtient que les pièces nécessaires au suivi financier, aucun document d'identité ou dossier complet par accès indirect ; aucune génération métier, secret, payload technique ou capacité d'action transmise. |
| E69-CA-11 | Chaque profil, vues paiements/reversements/audit disponibles | Ouvrir la vue puis une action liée | Lecture financière autorisée sur toutes les communes pour les trois rôles métier ; audit global et commandes d'argent à Admin seul. Suivi financier spécialisé à Finance/Admin. Refus et liens cohérents avec la matrice actualisée de l'EPIC 65. |
| E69-CA-12 | Interface ERP/SQLAdmin sur ordinateur ou petit écran | Naviguer avec clavier et liens enregistrés | Accueil et navigation adaptés, actions interdites absentes, refus explicite sur ancien lien ; aucune redirection forcée vers une rubrique interdite. |
| E69-CA-13 | Commande différée ou module nouvellement intégré | Vérifier l'autorisation avant exécution | Politique partagée et capacité explicitement classifiée ; aucune autorisation par défaut ni contournement via compte de service. |

### Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Backend et domaine propriétaire | **Concerné :** `identite_acces`, chargement et contrôle de session, ERP, SQLAdmin, services de projection et commandes. Les domaines métier conservent leurs règles ; l'autorisation n'est pas réimplémentée par écran. |
| API et consommateurs | **Concerné :** authentification interne, profil/capacités, refus, projections et exports ; contrats documentaires canoniques et tests consommateurs. **À examiner :** lecteurs internes ou anciennes interfaces fondés sur un rôle nominal. |
| Autres applications | **Sans évolution fonctionnelle demandée** de Marketplace/Live, Commerçant et Animation : leurs profils utilisateurs restent propres. **À examiner :** routes ou permissions partagées afin d'éviter une régression de leurs sessions. |
| Persistance et comptes existants | **Concerné :** représentation du profil, normalisation globale v253, versions d'autorisation/compte, sessions, migration nominative et audit. Procédure de retour à vérifier sans rétablir des permissions révoquées par défaut. |
| Générateur et fixtures | **Concerné :** profils des accès test/démo, jeux par rôle, sessions périmées et comptes historiques cumulant des rôles ; export/import/restauration à vérifier. Aucun identifiant ni donnée réelle ajouté à cette documentation. |
| Documentation fonctionnelle | **Concernée :** guide backoffice, matrice d'accès, conventions de navigation, architecture EPIC 35 et spécification EPIC 65 ; identifier clairement les tâches de chaque profil. |
| Exploitation et livraison | **Concerné :** inventaire avant migration, reprise Admin, invalidation des sessions, audit des changements/refus, ordre de livraison commun serveur/interfaces et recette après migration. Aucune preuve de production à ce stade. |

### Arbitrages de spécification et preuves attendues

La décision E69-FINANCE-20261001 retient trois rôles métier, le cumul Backoffice +
Finance, les commandes d'argent réservées à l'admin en V1 et le maintien de
l'admin historique. Restent à préciser :

1. La classification exhaustive des écrans/actions mixtes, des exports et de
   l'historique métier, avec l'audit global réservé à Admin.
2. La correspondance nominative des rôles actuels vers les nouvelles attributions et la
   profils globaux des nouveaux comptes et conversion v253 explicitement décidée ; aucun cumul hérité implicite.
3. Les champs personnels nécessaires à chaque rôle, notamment Finance, et les permissions
   de révélation aujourd'hui réservées à ADMIN dans les visions 360.

La [spécification V1.4](../../specifications/epic-69-acces-internes/README.md) suit le
[cycle d'epic](../../organisation/cycle-epic.md). Relier E69-CA-01 à E69-CA-27
aux preuves : politique pure d'autorisation, tests de refus applicatifs sans effet
métier, contrats des API/exports, parcours navigateur par profil, révocation
multi-onglets et migration sur fixtures isolées. Les contrôles documentaires de ce
cadrage ne valent ni ces tests, ni une implémentation, ni une recette déployée.

## Complément E69-SATELLITES-20261001 — ERP et applications internes

### Demande acquise et répartition retenue

La demande initiale de deux rôles est complétée par l'ajout de Finance, accepté
dans E69-FINANCE-20261001, avec maintien de l'admin actuel comme garde-fou.
L'accès aux vues historiques SQLAdmin
reste **exclusivement réservé à cet admin**, y compris lorsque les vues concernent
des objets métier. Support, Atelier et les autres applications internes doivent
être protégés au même titre que l'ERP. Leur URL autonome ne constitue pas une
exception aux droits.

Ce besoin reprend le cadrage initialement rattaché à E35-PROFILS-20260928.
La décision explicite de créer l'EPIC 69 remplace ce rattachement ; l'EPIC 35
reste terminée et ne porte plus le suivi de ces travaux. Le présent complément est un cadrage, sans
changement de compte, de configuration ou d'autorisation réelle.

**V1 retenue : Lecteur, Backoffice et Finance, à côté de l'admin historique.**
Backoffice regroupe les usages quotidiens : préparer un commerçant, répondre
au support, gérer une animation et composer un coffret. Finance est spécialisé
dans le suivi financier. Une personne peut recevoir explicitement Backoffice +
Finance, sans obtenir l'administration ni l'exécution de mouvements d'argent.

| Périmètre | Lecteur | Backoffice | Finance | Admin historique |
| --- | --- | --- | --- | --- |
| ERP : dossiers, catalogue, indicateurs | Consulter sur toutes les communes | Consulter et gérer via les parcours métier | Informations de contexte nécessaires aux dossiers financiers seulement | Accès conservé |
| Support : dossiers et échanges | Consulter les informations nécessaires, masquées selon les droits | Répondre, qualifier et suivre les demandes | Suivi des seuls dossiers financiers, sans accès général aux échanges | Accès conservé |
| Atelier : projets et coffrets existants | Consulter les contenus autorisés | Composer, demander une génération IA, modifier et créer via le parcours métier | Aucun accès au module ; références du coffret accessibles dans le dossier financier si nécessaires | Accès conservé |
| Onboarding et animations côté opérateur | Suivre l'avancement | Préparer les dossiers, communiquer et réaliser les actions métier autorisées | Aucun droit de gestion | Accès conservé |
| Paiements, reversements, factures et justificatifs | Lecture métier limitée aux données nécessaires | Lecture métier utile au traitement courant | Consultation, exports autorisés, qualification et suivi des anomalies | Actions actuelles conservées |
| Remboursements et autres commandes financières engageant de l'argent | Refus | Refus, même avec Finance | Refus, même avec Backoffice | Exécution selon règles métier existantes |
| Comptes internes, habilitations, outils techniques et Localeo Control | Aucun accès | Aucun accès | Aucun accès | Accès conservé |
| Toutes les vues et actions historiques SQLAdmin | Aucun accès | Aucun accès | Aucun accès | Accès exclusif |

Un Lecteur ne lance pas une génération IA, un envoi, une synchronisation ou une
création de document sous prétexte de consultation. L'accès en lecture d'Atelier
doit être conçu explicitement : si un écran ne sait pas séparer lecture et
commande, il reste fermé au Lecteur tant que cette séparation n'est pas livrée.
Un besoin métier disponible uniquement dans SQLAdmin doit recevoir un parcours
métier protégé avant d'être proposé à Backoffice ; aucun accès SQLAdmin de secours
n'est donné aux rôles métier.

Finance peut retrouver un paiement et sa facture, consulter un justificatif existant,
exporter les données autorisées et qualifier une anomalie dans un parcours de suivi
existant. Une annotation ou un état de traitement interne ne modifie jamais la
vérité du paiement, le montant dû, les écritures ou l'état Stripe. Le suivi utilise les tickets/notes Support existants, avec adaptation du rattachement
pour les dossiers sans instance ; cette epic ne crée ni nouveau workflow comptable
ni nouvelle commande de remboursement.

L'émission d'un avoir, l'annulation d'une facture, la modification d'un montant dû,
le déclenchement ou la reprise d'un transfert sont classés parmi les commandes
financières sensibles à réserver à l'admin lorsqu'elles existent. La génération
d'un export de données existantes reste distincte d'une émission de pièce métier.

### Décisions et paramètres restant à préciser

| Référence | Proposition | Conséquence et décision attendue |
| --- | --- | --- |
| E69-ARB-01 | **Résolu :** Lecteur, Backoffice et Finance ; cumul explicite Backoffice + Finance | Décision E69-FINANCE-20261001 remplaçant la proposition de deux rôles et le rôle unique par compte. Pas de cumul caché ni d'élévation vers Admin. |
| E69-ARB-02 | **Principe résolu :** remboursements et autres commandes financières sensibles à l'admin en V1 | Remplace « tous les droits métier » de Backoffice ; E69-CA-04/11 actualisés. Inventaire exact des commandes et actions de suivi Finance à produire avant implémentation. |
| E69-ARB-03 | **Résolu : matrice fixe en V1**, sans personnalisation supplémentaire par module | Décision utilisateur ; cumul Backoffice + Finance conservé ; V1.4 remplace les périmètres par des scopes fonctionnels globaux. |
| E69-ARB-04 | **Résolu : invitation 24 h, récupération déclenchée par l'admin**, initialisation par l'utilisateur | Parcours E69-INVITATION-20261001 ; limites techniques de renvoi à finaliser, sessions selon politique existante. MFA hors périmètre ; ne pas distribuer le compte admin comme compte collectif. |

**E69-ARB-05 — Résolu : option A.** Finance dispose de consultation/export et de
demandes via le Support existant. Réutiliser tickets, notes et états de traitement,
sans workflow financier dédié. Adapter leurs rattachements aux dossiers sans
instance de coffret et leurs projections avant de déclarer CA-19 couvert.

**E69-ARB-06 — Résolu : ouvrir les trois actions au Backoffice.** Qualification ou
suspension BUM d'un coffret, activation d'une souscription dont le montant est déjà
zéro, annulation d'une commande impayée non active. Admin conserve ces actions ;
Finance seul n'en dispose pas. Les règles métier, confirmations, versions, audit
et scope fonctionnel Backoffice restent obligatoires, sur toutes les communes. Aucun droit de remboursement,
de remise à zéro d'un prix positif ou d'annulation de facture n'est ajouté.

Les rôles, leur cumul autorisé, les restrictions financières et les contraintes
admin historique/SQLAdmin/satellites sont acquis. L'inventaire détaillé des droits,
les paramètres techniques et la classification fine restent à préciser. Récupération
administrée et matrice fixe sont validées ; aucune MFA n'est ajoutée.

### Critères supplémentaires et preuves attendues

Les identifiants E69-CA-01 à 18 sont conservés et alignés sur Finance et les
restrictions retenues. E69-CA-19 à 22 couvrent Finance et le cumul de rôles.
Les critères suivants complètent le périmètre à réaliser.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E69-CA-14 | Non connecté ou rôle insuffisant, URL de Support/Atelier connue | Ouvrir directement le satellite, appeler ses API ou télécharger une pièce | Authentification et capacité contrôlées côté serveur avant restitution ; aucun contournement par URL, fichier, export ou entrée PWA. |
| E69-CA-15 | Lecteur dans Atelier ou Support | Tenter génération IA, création de coffret, réponse ou envoi | Refus sans mutation ni appel externe ; consultations autorisées toujours disponibles selon la matrice. |
| E69-CA-16 | Utilisateur désactivé ou rétrogradé avec ERP et satellite ouverts | Réutiliser les sessions puis demander une commande différée | Nouveaux droits appliqués dès la prochaine requête protégée et revalidés avant exécution ; pas de droits conservés dans un autre onglet ou une PWA. |
| E69-CA-17 | Admin historique, indisponibilité du référentiel des nouveaux comptes métier | Utiliser l'accès de reprise | Accès historique utilisable selon la procédure testée ; la panne n'ouvre aucun accès anonyme ou métier à SQLAdmin et aucune rétrogradation silencieuse de la protection. |
| E69-CA-18 | Chaque rôle sur ERP, Support et Atelier | Réaliser une action autorisée, puis tenter une action refusée | Auteur et contexte de sécurité traçables sans secret ; guide opérateur décrivant les droits et procédure de reprise admin, recette par rôle et par entrée. |
| E69-CA-19 | Finance seul, dossier financier fonctionnellement autorisé | Consulter paiement, reversement, facture et justificatif ; exporter et ouvrir/compléter une demande financière via tickets/notes Support existants | Données nécessaires et tickets/notes financiers accessibles avec ou sans instance, après adaptation du rattachement ; aucun accès général au catalogue, onboarding, Support ou Atelier ; suivi distinct des écritures et états PSP. |
| E69-CA-20 | Backoffice, Finance ou cumul des deux, commande financière connue | Tenter remboursement, transfert, avoir, annulation de facture ou autre commande financière réservée via écran, API, alias ou commande différée | Refus serveur avant mutation ou appel PSP ; mêmes règles pour chaque entrée. Les trois actions métier ARB-06 sont ouvertes à B/B+F via leurs scopes B globaux, jamais à F seul ; Admin conserve ses droits existants. |
| E69-CA-21 | Admin attribuant Backoffice + Finance à un compte | Afficher les droits puis utiliser les deux fonctions | Union explicite des scopes métier globaux, audit du cumul ; aucun contexte de communes, accès SQLAdmin, administration ou commande d'argent. |
| E69-CA-22 | Compte Backoffice + Finance, plusieurs sessions ouvertes | Retirer Finance puis réutiliser un ancien écran ou export | Capacités Finance retirées dès la prochaine requête protégée et avant exécution différée ; Backoffice reste utilisable avec ses seules lectures/actions, aucun téléchargement spécialisé par un ancien lien contournant la révocation. |
| E69-CA-23 | Admin historique, nouvel utilisateur interne | Renseigner identité, email et profils globaux puis créer et inviter | Un compte nominatif en attente d'initialisation et une invitation tracée ; email préparé sans mot de passe ; doublon d'email normalisé ou répétition de commande sans double compte ni double invitation logique ; même opération refusée aux rôles métier. |
| E69-CA-24 | Invitation ERP valide, compte autorisé | Ouvrir le lien puis définir et confirmer le mot de passe | La simple ouverture ne consomme pas le lien ; validation conforme à la politique de mot de passe, empreinte stockée et consommation atomique du lien ; première connexion possible avec les droits courants uniquement ; aucun accès ERP/satellite avant initialisation. |
| E69-CA-25 | Lien expiré, déjà utilisé, remplacé, falsifié ou destiné à Animation | Soumettre l'initialisation, y compris simultanément | Refus sans modification de mot de passe ni de droits ; au plus une consommation réussie ; message de reprise sans exposer l'existence ou le détail d'un autre compte. |
| E69-CA-26 | Admin, invitation en attente, expirée ou email en échec | Consulter le suivi puis renvoyer explicitement l'invitation | État compte/invitation distinct de l'état mail ; nouveau lien remplaçant l'ancien, sans nouveau compte ni changement des rôles ; échec ou résultat fournisseur incertain visible et reprise contrôlée sans rafale ni renvoi aveugle. |
| E69-CA-27 | Invitation non utilisée, compte modifié ou désactivé | Changer profils ou email, annuler l'invitation puis tenter l'ancien lien | Droits lus à leur état courant lors de l'initialisation ; désactivation/annulation ou changement d'email invalide l'ancien lien et neutralise l'envoi obsolète ; aucune réactivation ou élévation de droits par le lien. |

Propriétaire de la politique : domaine `identite_acces`, appliqué par les services
avant lectures/commandes. ERP et satellites présentent les capacités ; aucune
copie indépendante de la règle dans leurs menus. Les tests à produire couvrent
les URL directes, données, commandes, sessions périmées, effets externes interdits
et la reprise admin ; ils ne sont pas exécutés par ce cadrage.

### Impacts du complément

**Constat historique de cadrage, avant l'implémentation E69 du 1er octobre :**
ce paragraphe conserve le point de départ ; l'état courant est décrit dans le
[bilan V1.3](../../specifications/epic-69-acces-internes/verification-livraison.md).
L'[authentification interne](../../../../localeo-backend/app/infrastructure/admin/auth.py)
utilise toujours le compte configuré ; SQLAdmin vérifie le rôle `ADMIN`, sans
identifier séparément un compte historique. Le [garde ERP](../../../../localeo-backend/app/security/erp.py)
admet `ADMIN` et `EXPLOITATION`, sans distinction générale lecture/commande.
[Support](../../../../localeo-backend/app/api/support_ui.py) et
[Atelier](../../../../localeo-backend/app/security/atelier.py) réutilisent ce
contrôle et les périmètres territoriaux. Certaines entrées Support historiques
restent toutefois protégées par le garde admin ; l'inventaire doit distinguer
ces parcours et les alias. [Control](../../../../localeo-backend/app/api/pwa_exploitation_api.py)
reste admin. Le [registre de sessions](../../../../localeo-backend/app/infrastructure/persistence/admin_sessions.py)
gère expiration/révocation mais ne fournit pas encore le référentiel nominatif
et les habilitations attendues. Ces constats ne constituent pas un audit de
sécurité complet ni une preuve de comportement en production.

- **Backend/ERP et satellites concernés :** authentification, politique commune,
  gardes des pages/API, téléchargements, commandes et sessions ; Support et Atelier
  explicitement inclus, Control réservé à l'admin. Inventorier les autres surfaces
  internes et leurs entrées avant de déclarer la couverture complète.
- **Contrats et données concernés :** comptes nominatifs, rôles et cumul effectifs,
  capacités, contrats consommateurs, révocation ; migration sans remplacer
  l'accès historique ; V1.4 étend explicitement la portée territoriale, sans ajouter de fonctions.
- **Applications publiques et partenaires :** pas de nouveau rôle demandé pour
  les clients, commerçants ou organisateurs. Vérifier l'isolation des sessions et
  les routes partagées ; un rôle interne ne devient pas une identité commerçant.
- **Démonstration concernée :** comptes fictifs Lecteur, Backoffice, Finance et
  Backoffice + Finance, satellites, retrait d'un rôle, désactivation et refus
  SQLAdmin/commandes financières ; aucun secret historique dans les exports.
- **Documentation et exploitation concernées :** matrice par module/action,
  guide d'attribution, récupération et révocation, recette de reprise admin,
  inventaire des comptes et procédure de bascule. Guide ERP à publier via le
  mécanisme documentaire existant lors de la livraison.

La spécification V1 de l'EPIC 69 confronte l'architecture E35 historique au code
réel. Ses API sont décrites comme cibles à implémenter ; les droits actuels et
les contrats exposés ne sont pas modifiés par cette rédaction.

### Décision E69-FINANCE-20261001

Le 1er octobre 2026, l'utilisateur demande la rédaction sur la base de la
proposition ajoutant Finance. Sont retenus : suivi financier courant et exports,
commandes engageant de l'argent réservées à l'admin en V1, cumul explicite
Backoffice + Finance, exclusivité SQLAdmin et maintien de l'admin historique.
Les matrices et critères précédents sont actualisés sans modifier les stories
historiques terminées. Cette étape comptait 22 critères, à spécifier et
implémenter ; aucune attribution réelle, migration ou livraison n'a été effectuée.

## Référencement E69-INVITATION-20261001 — Nouvel utilisateur interne

### Parcours retenu

La demande complète l'epic : un administrateur référence un nouvel utilisateur
et lui envoie un email pour définir son mot de passe, sur le modèle du parcours
Animation. Dans la V1 actuelle, cette fonction appartient à l'admin historique ;
elle ne permet pas de créer un autre admin ou d'ouvrir une inscription publique.

1. Depuis la gestion des utilisateurs internes, l'admin renseigne nom, prénom,
   email et profils globaux autorisés, sans sélectionner de communes. Un récapitulatif indique les
   droits qui seront accordés, notamment le cumul Backoffice + Finance.
2. L'action **« Créer et inviter »** crée le compte en attente d'initialisation
   et prépare l'email associé. L'admin ne choisit ni ne reçoit le mot de passe.
   Un email déjà associé à un compte interne renvoie l'admin vers sa fiche ;
   aucune fusion ou réactivation automatique, même si le compte est désactivé.
3. Le destinataire reçoit un email Localeo indiquant l'origine de l'invitation,
   l'accès ERP concerné, la durée du lien, le contact en cas de difficulté et le
   bouton **« Définir mon mot de passe »**. Aucune donnée financière ni secret
   d'administration n'y figure. Le lien vise l'environnement ERP de l'invitation.
4. Le lien ouvre un formulaire de définition et confirmation du mot de passe.
   Une ouverture ou un aperçu par un outil de messagerie ne consomme pas le lien.
   La validation vérifie le compte, le lien et la politique de mot de passe,
   puis consomme le lien une seule fois. L'utilisateur peut ensuite se connecter
   à l'ERP ; ses scopes fonctionnels courants déterminent les satellites accessibles sur toutes les communes.
5. L'admin suit sur la fiche les invitations et les états du compte. Il peut
   renvoyer une invitation ou l'annuler ; le nouveau lien remplace l'ancien.
   L'envoi, l'initialisation et la première connexion restent trois événements
   distincts : un email envoyé ne prouve ni sa réception ni l'utilisation du compte.

Le compte non initialisé n'obtient aucune session métier exploitable. La seule
surface accessible par le lien est l'initialisation, pas les données ERP. Un compte
désactivé ne peut pas être réactivé par une invitation. Pour un compte déjà
initialisé, orienter vers la récupération du mot de passe, à détailler séparément,
plutôt que réutiliser silencieusement le parcours de création.

### Réutilisation du parcours Animation et limites

Lecture locale, sans envoi réel ni test d'activation :

- [Gestion des accès Animation](../../../../localeo-backend/app/application/identite_acces/services/gestion_acces_animation.py) :
  création nominative, contrôle des doublons d'email, préparation d'un email en
  file d'envoi et audit ; la création partenaire n'est pas un compte interne ERP.
- [Invitation Animation](../../../../localeo-backend/app/application/identite_acces/services/service_invitation_animation.py) :
  empreinte du jeton, expiration de 24 h, remplacement de l'invitation précédente,
  usage unique, politique de mot de passe et contrôles concurrents.
- [Email d'accès](../../../../localeo-backend/app/infrastructure/email/acces_animation.py) :
  rendus HTML/texte et explication du lien à usage unique.

Réutiliser les composants adaptés de génération, stockage d'empreinte, politique
de mot de passe, rendu et file email. La politique du compte interne reste dans
`identite_acces` ; l'application orchestre création/invitation et notification.
Ne pas copier les dépendances ORM du service Animation comme architecture cible,
ni attribuer les rôles ou sessions Animation au compte ERP. Un même email peut
exister dans deux populations sans fusion d'identité ni reconnaissance croisée
de leurs jetons. La durée de **24 h est validée par l'utilisateur**.

### Suivi, reprises et impacts

La fiche distingue compte en attente, utilisable ou désactivé ; invitation en
attente, utilisée, expirée ou annulée ; email préparé, pris en charge, livraison
connue/inconnue ou échec. Les libellés définitifs seront précisés. La création et
la programmation de l'email doivent rester cohérentes après échec transactionnel.
Un échec de transport conserve le compte et rend une reprise possible sans doublon.
Un changement d'adresse invalide l'invitation précédente avant un nouvel envoi ;
un mail déjà parti ne peut pas être retiré, mais son lien devient inutilisable.

Les jetons bruts et mots de passe sont exclus des listes, journaux et audits ;
le lien d'activation n'est présent que dans les supports nécessaires à sa remise,
avec accès restreint et conservation à définir. L'audit conserve l'admin auteur,
le compte cible, l'action et son résultat. Les renvois sont bornés ; les délais,
limites, parcours de récupération et protections contre les tentatives restent
à préciser, sans exposer le référentiel des comptes aux visiteurs anonymes.

- **Contrats/données :** invitation interne, expiration, révocation et consommation
  atomique, unicité de compte, identité de l'admin et état d'envoi ; aucun jeton ERP
  accepté par une API partenaire, aucun rôle fixé par le formulaire public.
- **Interfaces :** gestion utilisateurs réservée admin, suivi/renvoi, page ERP de
  définition du mot de passe et messages de reprise. Aucune mutation de l'admin
  historique par ce nouveau parcours.
- **Documentation/exploitation :** guide créer/inviter/renvoyer/annuler, diagnostic
  des emails, configuration de l'URL de l'environnement et procédure de récupération.
- **Démonstration et preuves :** comptes en attente, activés, expirés et désactivés ;
  email capturé en test, doublon de création, double clic, concurrence d'activation,
  changement d'email/rôle et refus croisé Animation/ERP. Tests à produire, aucun
  compte réel créé ni message envoyé pendant ce cadrage.

Ce complément ajoute E69-CA-23 à 27, sans renuméroter les 22 critères précédents.
