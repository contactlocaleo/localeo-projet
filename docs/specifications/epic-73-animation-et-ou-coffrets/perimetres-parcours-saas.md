# E73 — Périmètres commerçants et parcours SaaS

## Évolution du 11 novembre 2026 — E73-EVO-HABILITATIONS-ERP

Demande : permettre à Localeo de comprendre, ajouter et retirer les habilitations
d’un utilisateur Animation depuis l’ERP. Cette évolution complète la gestion
d’équipe existante sans changer la clôture historique de l’epic.

**Existant vérifié.** La fiche Accès Animation propose des cases de permissions
historiques par commune. Le serveur refuse ce circuit dès qu’un responsable
d’équipe est actif. La console interne expose seulement validation initiale et
récupération de responsabilité, alors que le portail sait modifier les membres.
La fiche est centrée sur l’organisation principale et ne rend pas les autres
appartenances compréhensibles.

**Cible.** Depuis Animations → Équipes et contrats → Accès Animation, rechercher
un utilisateur, ouvrir ses habilitations et sélectionner son organisation.
Présenter rôle, statut de l’appartenance, communes, permissions du rôle et
autorisations complémentaires Acheter, Importer des commerçants, Communiquer.
Les permissions `animation:*` des équipes sont définies par le rôle ; elles ne
deviennent pas une seconde liste libre concurrente. Les autorisations du
responsable sont automatiques et expliquées. Ajouter/retirer une capacité
consiste à modifier le rôle ou les trois autorisations ; les communes et la
suspension/révocation se gèrent sur cette même appartenance.

Les modules souscrits, leurs quotas et l’état du compte demeurent des conditions
distinctes. Un droit personnel n’active aucun module payant. La création d’une
identité ou d’une nouvelle relation d’équipe conserve son circuit d’invitation ;
cette évolution gère les appartenances déjà existantes, y compris inactives.
Les accès historiques restent consultables et modifiables par leur commande
existante uniquement lorsque l’organisation n’est pas gérée par une équipe.

**Correctif du 11 novembre 2026 — responsable dans la liste des souscriptions.**
La liste ERP ajoute « Responsable identifié » : Oui si une appartenance active
de rôle Responsable existe dans l’organisation, sinon « Non · à identifier »
mis en évidence par un libellé, un badge et un repère visuel. Cette information
porte sur la désignation dans l’organisation, selon la même définition que le
mode de gestion d’équipe ; elle ne promet pas de droits effectifs sur une commune
ni la disponibilité du compte. Une ancienne réponse sans ce champ indique
« À vérifier », sans assimiler une information absente à un refus.
Pour les opérateurs disposant de `acces_externes.gerer`, « Identifier le
responsable » ouvre le parcours de vérification de la bonne organisation depuis
le gestionnaire de la souscription. Ce dernier est une cible de vérification,
sans nomination automatique. Les décisions et contrôles de responsabilité
existants restent obligatoires. Un périmètre ERP insuffisant sur l’équipe
reste refusé au serveur.
Le contrat de liste ajoute `responsableIdentifie` (booléen) et `gestionnaireId`
(identifiant du gestionnaire de souscription), sans nom ou email supplémentaire.
La projection utilise un `EXISTS` corrélé dans la requête de la page, conserve
25 lignes, recherche/statut/périmètre et deux requêtes SQL (total et page), sans
chargement de tous les membres ni N+1. La liste des commandes est inchangée.
Pas de migration ni modification des rôles ; budget local de lecture de 500 ms
p95 à vérifier sur N/10N, sans qualification du trafic de production.

**Correctif du 11 novembre 2026 — raccord depuis les modules.** Chaque module
de la souscription propose « Utilisateurs et autorisations », chargé à la demande
avec l’identifiant d’organisation fourni par la projection commerciale. La liste
d’équipe existante est paginée par 25, sans charger toutes les appartenances.
Elle distingue autorisation enregistrée, rôle, compte, appartenance et habilitation
sur la commune de cette souscription ; elle ne promet pas l’usage du module.
Le lien vers la fiche préselectionne cette organisation, même hors première page
ou différente de l’organisation principale, et conserve le retour aux modules.
Une lecture refusée ne bascule pas sur une autre organisation. L’opérateur doit
disposer de `acces_externes.gerer` ; le droit d’octroi commercial ne l’implique pas.
Les commandes de modification existantes, confirmations, motifs, versions et
reçus sont réutilisés. Aucun droit utilisateur n’est accordé par l’octroi du
module. Import/Communication gardent leur portée organisation et communes
attribuées ; la Chasse utilise les permissions Animation, sans autorisation
supplémentaire inventée. Les accès historiques sans appartenance ne sont pas
présentés comme absents : l’écran renvoie vers leur circuit existant.

**Invariants et propriétaires.** `EquipeOrganisation` porte la modification
Localeo explicite et motivée, avec les mêmes règles de délégation que le portail :
communes validées, rôles et autorisations connus, aucun retrait du dernier
responsable, aucune promotion directe au rôle responsable. Le transfert accepté
et la récupération assistée conservent leur circuit propre. Le service interne
contrôle périmètre ERP, version et reçu, puis synchronise seulement le membre
ciblé ; audit T1 avant/après et motif dans la même transaction. Les autres membres,
organisations, droits commerciaux et consommations restent inchangés. Les
restrictions deviennent effectives par les contrôles de session existants.
Une modification des seules autorisations complémentaires ne normalise pas les
permissions historiques du membre et ne supprime aucune échéance. Les bornes
existantes sont conservées ; un changement explicite de rôle adapte les
permissions à ce rôle, un ajout explicite de commune crée son habilitation.
La lecture distingue permissions du rôle et permissions effectives issues de
l’intersection avec les habilitations actives ; elle ne promet pas l’usage
d’un module du seul fait d’une autorisation personnelle.

**Contrats.** Lecture paginée interne des organisations du gestionnaire, incluant
les appartenances suspendues/révoquées :
`GET /internal/identite-acces/animation/gestionnaires/{id}/organisations`.
Pagination à curseur, `limit=25`, maximum 100 ; filtre de périmètre avant limite.
La sélection charge l’équipe interne existante avec `gestionnaireId`, qui peut
inclure la cible située hors de sa première page. La projection annonce le mode
de gestion, les permissions et les actions autorisées ; le navigateur ne déduit
pas un état global d’une page partielle.
La liste rend `items` (identifiant d’organisation `id`, `nom`,
`statutOrganisation`, rôle/statut/communes/autorisations de l’appartenance et
version) et `nextCursor`. L’équipe interne expose `modeGestion` (`EQUIPE` ou
`HISTORIQUE`), `nomOrganisation`, `statutOrganisation` et, pour le membre ciblé,
`statutCompte`, `permissionsRole`, `autorisationsEffectives`, `allowedActions`
et `habilitations` par commune (état, dates, permissions enregistrées et
`permissionsEffectives`). Les trois autorisations ne sont pas annoncées
effectives si aucune habilitation n’est active. Une organisation inactive reste
consultable, sans action de modification indisponible côté serveur.
Le détail historique identifie l’organisation de chaque habilitation afin que
le formulaire de l’organisation principale ne puisse pas modifier une autre
relation. Une organisation secondaire sans équipe validée renvoie vers la
vérification de responsabilité ; aucun repli vers la commande historique de
l’organisation principale. En cas de lecture du mode impossible, aucune
commande historique n’est proposée par défaut.

`PATCH /internal/identite-acces/animation/organisations/{id}/equipe/{membre_id}`
reçoit `expected_version`, `role`, `statut`, `communeIds` (1 à 100),
`autorisations` (ACHAT/IMPORT/COMMUNICATION) et `motif` obligatoire. Capacité
`acces_externes.gerer`, CSRF, clé d’idempotence et `Cache-Control: no-store`.
Cette capacité autorise les profils ERP déjà habilités, notamment Backoffice,
dans leur périmètre ; aucune élévation globale ni attribution automatique.
Le périmètre est revérifié avant tout rejeu ; aucune usurpation d’un responsable
portail. Refus 401/403/404, validation 422, conflit 409 conservent leurs sens.
Les réponses sont additives pour les consommateurs existants ; aucun changement
de contrat du portail Animation ni de ses commandes.

| Critère | Comportement observable | Preuves prévues |
| --- | --- | --- |
| HA-01 | Rechercher un utilisateur, voir ses organisations et choisir la cible, y compris inactive ; contexte utilisateur/organisation/communes toujours visible. | Navigation ERP, multi-organisations, état vide/erreur, pagination bornée. |
| HA-02 | Comprendre permissions de rôle, autorisations complémentaires et conditions commerciales séparées ; ne pas présenter une permission suspendue comme utilisable. | Projections domaine/API et affichage lecteur/gestionnaire/responsable. |
| HA-03 | Ajouter/retirer autorisations, changer rôle/communes/statut avec résumé, motif et confirmation ; succès visible sur la cible. | Domaine, service, HTTP, PostgreSQL et navigateur ; autres membres/organisations préservés. |
| HA-04 | Refuser promotion directe, perte du dernier responsable, commune non validée ou hors périmètre ; préserver les restrictions de délégation ERP. | Tests de refus directs, périmètre revérifié au rejeu, revue indépendante. |
| HA-05 | Conflit conservant la saisie ; réponse perdue reprise avec corps/clé identiques ; session expirée sans réaffichage privé ; audit atomique. | Tests de concurrence, répétition, échec et lecture/mutation tardives. |
| HA-06 | Accès historiques et validation/récupération de responsabilité restent disponibles dans leur contexte ; aucun formulaire historique envoyé pour une équipe gérée. | Non-régression ERP et refus serveur conservés. |
| HA-07 | Lisibilité 320/390/1280 px, clavier, actions explicites, cibles tactiles et états chargement/erreur ; aucun chargement exhaustif. | Recette navigateur et captures inspectées ; mesures requêtes/volume PostgreSQL. |

**Impacts et livraison.** Backend domaine/application/adaptateurs, ERP,
OpenAPI documentaire et guide ERP. Pas de nouvelle table, migration ou flag :
les appartenances, reçus et audits existants portent ces décisions. Le générateur
utilise les mêmes modèles et circuits ordinaires ; nouvelles fixtures synthétiques
pour multi-organisations et délégations. Animation, Pro et Live conservent leurs
contrats et contrôles courants ; aucune modification frontend attendue hors ERP.
Livrer le backend et sa documentation, puis recette sur TEST ; aucun changement
de permission réelle, envoi d’invitation ou déploiement implicite.

**Performance.** Réutiliser les lectures ciblées et verrous d’équipe, charger
seulement la cible de commande, paginer les appartenances en stockage sans N+1.
La nouvelle lecture vise au plus 100 appartenances et un nombre constant de
requêtes pour 25/100 résultats ; aucune recherche exhaustive côté navigateur.
Mesurer sur PostgreSQL jetable N/10N et accès concurrents avant activation :
budget local initial p95 inférieur à 500 ms, absence d’erreur hors conflits
attendus, attente bornée et aucune mutation d’un autre tenant. Les résultats et
limites seront consignés dans le bilan existant, sans prétendre qualifier une
capacité de production à partir d’une base locale.

## Évolution du 1er novembre 2026 — E73-EVO-ONBOARDING-ANIMATION-SIMPLE

Demande : simplifier le référencement et l’onboarding du commerçant destiné aux
animations, sans Stripe, contrat ni rendez-vous imposés. Cette décision remplace
l’obligation de convention Animation de DEC-53 et de la section 3.2 ; les critères
E73-CA-16/17/18 sont précisés, sans changement de statut de l’epic.

Le domaine `conformite_fiscale_bum` détermine les exigences à partir des produits
explicitement demandés. L’application transmet cette projection à OnBoard, ERP,
Pro et aux contenus de préparation. `referencement` reste propriétaire de
l’ouverture du produit ; un dossier simplifié n’active ni le commerce ni ses
droits. L’acceptation de chaque participation reste gouvernée par Animation.

| Critère de cette évolution | Comportement et preuve attendue |
| --- | --- |
| OA-01 — Référencement contextualisé | ERP et OnBoard proposent Animation, Coffrets ou les deux aux agents disposant du droit existant `commercants:perimetres_gerer`, en plus du droit de référencement. Le choix est enregistré atomiquement avec le commerce et son dossier ; aucune invitation ni activation supplémentaire n’est déclenchée. Sans ce droit, la fiche peut être créée selon le parcours historique puis qualifiée par une personne habilitée ; une requête avec choix explicite est refusée. |
| OA-02 — Animation seule | Identité, adresse/commune, contact et accès Pro vérifié restent exigés selon les règles existantes. Contrat/convention, signature, Stripe, finance, prestations Coffrets, rendez-vous, pack et bilan ne bloquent pas le dossier. La préparation guide vers les seules actions utiles. |
| OA-03 — Coffrets et complément | Coffrets seul ou ajouté conserve ses contrôles contractuels et financiers applicables. Le mixte exige la convention Coffrets, pas une seconde convention Animation. Ajouter Coffrets ne retire pas Animation ni ses engagements acquis ; preuves courantes et habilitations restent contrôlées par le serveur. |
| OA-04 — Continuité et cohérence | Dossiers existants explicitement Animation bénéficient de la règle sans effacer documents, rendez-vous ou audit. Produit non précisé reste prudent. Écrans, actions, réserves et communications n’imposent pas des obligations déclarées non applicables. Une simple lecture n’effectue aucun envoi ni activation. |

Précision du correctif **E73-ONBOARDING-SANS-RDV-20261101** : pour Animation
seule, ne pas afficher de date de rendez-vous ni présenter un ancien statut
`RDV_PLANIFIE` comme une étape à accomplir. La liste exclut ces dossiers du
filtre des rendez-vous non planifiés avant comptage et pagination. Les prochaines
actions automatiques de rendez-vous reconnues comme devenues inapplicables ne
doivent plus être proposées ni retenues par les filtres de suivi. Conserver les
valeurs historiques et les suivis manuels distincts ; aucune lecture ne les efface.

Présentation OnBoard **E73-ONBOARD-DOSSIER-UX-20261101** : afficher le périmètre
et les points nécessaires en tête, avec accès direct aux rubriques concernées.
Animation seule présente les coordonnées, l’accès Pro et les actions de
finalisation autorisées par le statut serveur. Les réglages de fonctions, le
récapitulatif et la réouverture restent dans une gestion secondaire dépliable.
Les commandes gardent leurs droits et effets existants ; enregistrer les saisies
avant de vérifier, finaliser ou rouvrir. Ne pas déduire une conformité actuelle
du seul statut clos ni rouvrir implicitement un dossier pour un complément.

Les parcours d’import gardent une demande à examiner, sans ouverture automatique.
Les supports Coffrets historiques restent utilisables ; un support Animation
ne réclame pas de convention ou de compte Stripe. Les droits, contrôles de version,
statuts terminaux et refus de sécurité restent applicables. Le passage d’Animation
seule à Coffrets est testé avec des preuves insuffisantes puis valides et périmées.

Impacts : backend (règles, services, API et projections), ERP/OnBoard et Pro
(référencement et préparation), contrats documentaires et guides. Aucun changement
de stockage n’est requis si les produits et faits existants suffisent ; vérifier
les modèles et le générateur avant de confirmer cette absence de migration.
Marketplace et gestion organisateur Animation n’ouvrent aucun droit commerçant.
Les preuves locales et les contrôles non exécutés seront consignés dans le
[suivi d’implémentation](suivi-implementation.md), séparément du bilan historique.

Décision du **30 octobre 2026 — E73-EVO-LIVE-UNIQUE** : les attentes de site
public des sections ci-dessous sont remplacées par
[Localeo Live comme entrée unique](localeo-live-entree-unique.md). Le domaine
`animations.localeo.city` sert Live ; la surface marketplace Animation est retirée,
avec compatibilité des anciens accès et reprise volontaire du carnet.
La gestion organisateur et les règles métier restent inchangées.

Spécification cible du 17 octobre 2026. Source des choix : [backlog E73](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md), notamment DEC-42, 51 à 59, 109 à 119, 125 à 134 et 138 à 144. Ce document couvre US11 à 13, US23 à 26, US29 à 33 et US35 ; il ne déclare ni leur implémentation ni leur déploiement. Les conventions communes, lots et modules sont décrits dans [architecture et contrats](architecture-contrats.md), [dotation et lots](dotation-lots.md) et [modules et souscriptions](modules-souscriptions-import-communication.md).

## 1. Existant vérifié et changements nécessaires

Lecture des producteurs et consommateurs locaux, sans appel d’environnement :

| Source réelle | Comportement observé et évolution E73 |
| --- | --- |
| [Scopes du portail commerçant](../../../../localeo-backend/app/domaine/identite_acces/acces_portail_commercant.py) | `ACTIF` ouvre aujourd’hui les scopes techniques validation, prestations, reversements, dashboard, messages et animation. Ces scopes ne sont pas des périmètres commerciaux. Ajouter un contrôle produit courant sans considérer un ancien jeton comme preuve d’acquisition. |
| [Checklist OnBoard](../../../../localeo-backend/app/application/conformite_fiscale_bum/service_onboarding_commercant.py) et [préparation de domaine](../../../../localeo-backend/app/domaine/conformite_fiscale_bum/preparation_onboarding.py) | Applicabilité déjà calculée selon `fonctions_visees`, finance et prestations effectivement rattachées ; prestations et coffrets ne sont pas des obligations générales pour finaliser un onboarding. Relier ces faits aux périmètres demandés et à leurs prérequis, conserver les validations documentaires et d’envoi E68. |
| [Navigation Pro](../../../../localeo-commercant/src/app/merchantNavigation.js) | Les salariés disposent de Scanner/Historique sous capacités ; les menus du principal dépendent surtout de drapeaux applicatifs. Ajouter les capacités produit issues du serveur au principal, sans élargir celles des salariés. |
| [Gestion des accès Animation](../../../../localeo-backend/app/application/identite_acces/services/gestion_acces_animation.py) et [modèles SQL](../../../../localeo-backend/app/infrastructure/persistence/models.py) | Email du gestionnaire unique, `partenaire_id` obligatoire sur le gestionnaire et la session, habilitations par commune ; création ERP refusée si email déjà connu. Cela ne permet pas encore l’invitation du même compte dans plusieurs organisations. Introduire les appartenances explicites, pas un second compte. Les imports ORM/FastAPI de ce service historique ne sont pas le modèle de placement des nouvelles règles. |
| [Service d’invitation](../../../../localeo-backend/app/application/identite_acces/services/service_invitation_animation.py), [API Animation](../../../../localeo-backend/app/api/animation_locale_api.py), [session navigateur](../identite-acces/session-animation.md) | Activation et sessions existent ; le transport portail reste cookie HttpOnly et CSRF, pas un nouveau Bearer dans le navigateur. Séparer acceptation d’appartenance, activation initiale et récupération du mot de passe. |
| [Portail](../../../../localeo-animation/src/app/App.tsx) et [client API](../../../../localeo-animation/src/app/api.ts) | Connexion présente, récupération affichée indisponible ; Documentation/FAQ désactivées ; contact support envoyé à l’entrée publique de contact consommateur. Créer les parcours privés d’équipe, de récupération et de suivi sans exposer les notes internes Support. |
| [Préparation](../../../../localeo-animation/src/app/components/GenerationPreparationView.tsx) | Opérations versionnées, états incertains, reprises et préparation existent. Compléter délai et assistance ; ne pas contourner le moteur E55 ou recommencer une génération pour relancer le support. |
| [Bilans existants](../../../../localeo-backend/app/application/animation_locale/services/bilans_exports_animation.py) | Participants, validations, gains et consommation Coffrets sont calculés ; certains agrégats monétaires sont liés aux prestations Coffrets. Les mesures de lots libres doivent rester séparées. Les exports d’animation ne constituent pas l’export complet de l’organisation. |
| [Routes Marketplace](../../../../localeo-marketplace/src/App.jsx), [Live](../../../../localeo-marketplace/src/live/LiveApp.jsx) | `/animations`, fiches, liens participants et `/live` coexistent avec Coffrets ; carnet local et sauvegarde/restauration personnelle existent. Un changement d’origine ne transporte ni ce stockage ni la permission navigateur. |

## 2. Propriétaires et invariants

Les nouvelles commandes passent par les use cases de leur domaine ; ERP, API, batch et interfaces ne réimplémentent pas la décision.

| Invariant | Propriétaire cible | Entrées et effets |
| --- | --- | --- |
| Un produit demandé n’est utilisable qu’après validation de ses prérequis ; retrait sans perte des engagements acquis | `referencement`, agrégat `PerimetresCommercant`, consommant les faits d’onboarding ; `identite_acces` intersecte avec l’habilitation personnelle | Commande ERP, validations QR/PIN, offres/participations, projections Pro/OnBoard ; historique et audit atomiques |
| Une invitation ne donne aucun accès avant acceptation et ne crée pas de souscription | `identite_acces`, `AppartenanceOrganisation`, `InvitationOrganisation` | ERP/portail, liens publics, traitements différés ; email via outbox |
| Une personne est réutilisable entre organisations ; ses droits sont ceux de son appartenance courante | `identite_acces`, identité existante et appartenance versionnée | Connexion, changement d’organisation/commune, chaque commande et lecture ; cache invalidé à changement de contexte |
| Retrait d’accès effectif dès la requête suivante, pas de suppression du dernier responsable sans transfert accepté | `identite_acces`, `EquipeOrganisation` et transfert | API équipe/ERP ; transactions sérialisées sur l’organisation, tâches en attente suspendues |
| Une nouvelle édition ne réutilise aucun engagement, participant, gain, secret ou paiement | `animation_locale`, création d’édition depuis configuration sélectionnée | Portail/ERP ; un nouveau brouillon et sa provenance, aucun email ni quota de génération automatique |
| Une mesure a une population, une période et une définition explicites | `animation_locale`, politique de mesure ; projection de bilan en application | Portail/ERP/export, sans chiffre d’affaires déduit d’un passage |
| Export et fermeture sont deux commandes distinctes ; les obligations ouvertes survivent à la fermeture commerciale | `animation_locale`, `DossierReversibiliteOrganisation` ; droits dans `identite_acces`, données par ports des domaines propriétaires | Responsable/ERP, génération privée, téléchargement, purge ; pas de suppression en cascade de gains/archives |
| Le délai d’assistance se mesure à partir de faits persistés, pas du navigateur | `animation_locale` pour préparation ; `support` pour première réponse | Demande, attente complément, livraison et réponse humaine ; notifications de service indépendantes du module Communication |

Les faits de continuité sont des références vérifiables aux engagements, pas un booléen global « accès conservé ». Une suspension administrative du commerce/organisation et une révocation personnelle priment toujours sur la continuité commerciale.

Précision d’implémentation du lot 02 : une nouvelle demande d’ouverture après retrait ne suspend pas cette continuité ciblée pendant la préparation. Pour une facture déjà due sur un engagement protégé, les commandes de dépôt/correction admises par l’agrégat financier restent accessibles sous leurs habilitations et sont projetées explicitement au consommateur. Le mode de consultation des règlements ne donne aucun droit de nouvel engagement commercial ni de création d’un mandat. Les lectures et les commandes financières conservent leurs propriétaires existants.

`EquipeOrganisation` est la frontière de cohérence des appartenances/délégations et du dernier responsable ; une appartenance possède une version mais ne contourne pas cette racine pour changer de rôle. Les identités globales et secrets d’invitation/reset restent distincts. `DossierReversibiliteOrganisation` porte les transitions propres à la demande ; le processus applicatif persistant coordonne export, engagements et fermeture entre domaines. Il ne contient pas les agrégats Animation, Souscription ou Identité et ne décide pas à leur place qu’un engagement est résolu. Ces frontières sont précisées dans l’[architecture transverse E73](architecture-contrats.md).

## 3. Périmètres Animation/Coffrets, OnBoard et Pro

### 3.1 État et commande ERP

Un commerce conserve son identité et son dossier. Pour chacun des produits `ANIMATION`, `COFFRETS`, stocker une entrée versionnée : `etat` (`NON_DEMANDE`, `A_PREPARER`, `ACTIF`, `RETIRE`), dates de demande/activation/retrait, auteur, motif et référence de validation des prérequis. Les demandes importées restent des demandes à examiner ; elles ne valent pas décision ERP. Le statut général du commerçant reste distinct.

Activation ERP autorisée seulement à un administrateur ou Backoffice avec permission dédiée `commercants:perimetres_gerer`. Le principal/salarié, un gestionnaire Animation et un Backoffice sans permission sont refusés, même par appel direct. `demander` positionne `A_PREPARER`, `activer` exige les prérequis validés, `retirer` bloque immédiatement les nouveaux engagements. Chaque commande exige `expected_version` et un motif non vide ; un conflit laisse l’état intact. La remise en activité suit de nouveau le contrôle de prérequis courant, sans recréer compte, salarié ou historique.

Au retrait, enregistrer dans la transaction le périmètre des engagements protégés, à partir des faits verrouillés : bons déjà attribués, participations déjà acceptées à une animation déjà publiée, prestations déjà engagées dans des coffrets vendus. Le retrait concurrent d’une affectation/publication/vente a un ordre de sérialisation déterministe : une opération ne peut pas être à la fois déclarée postérieure au retrait et admise comme engagement antérieur. Les corrections/prolongations autorisées du même engagement restent gouvernées par son agrégat ; elles ne créent pas un droit général de nouvelle affectation.

Pour Coffrets, cette capture couvre aussi les achats payés sans instance encore activée et les commandes reconnues payées dont les achats ne sont pas encore matérialisés. Une confirmation fournisseur inconnue en base au moment du retrait ne constitue pas une preuve déjà acquise : sa réception tardive ne doit pas créer un nouvel engagement contre le périmètre retiré. Le paiement reste à rapprocher dans le circuit existant, sans paiement fictivement annulé ni droit rétabli par le seul retour navigateur.

### 3.2 Checklist et contenus

La projection fournit `requirementLevel`, `status`, `applicable`, `applicabilityReason`, `product`, `evidenceRef`, `policyVersion` et la prochaine action. Aucune interface ne remplace un refus backend par une case cochée. Trois niveaux sont affichés séparément : accès au compte, ouverture du produit, finalisation du dossier.

| Élément | Animation seule | Coffrets seuls / ajout Coffrets |
| --- | --- | --- |
| Identité commune : nom, adresse, commune, type, responsable et coordonnées | Requis selon validation de profil existante ; réutilisation des données vérifiées | Réutilisation ; seuls compléments manquants demandés |
| Accès Pro initialisé/testé et sécurité du compte | Exigences E68 conservées, sans activation automatique par import | Identiques ; pas de second compte |
| Engagements et convention signée | Non applicable au référencement Animation seul depuis OA-02 ; acceptation des conditions de chaque animation dans son parcours propre | Convention adaptée au périmètre Coffrets ; pas de seconde convention Animation ; conserver les preuves antérieures |
| Informations Animation | Coordonnées, lieux et informations utiles à la participation ; acceptation par animation distincte de l’activation du produit | Applicables uniquement si Animation est aussi demandé |
| Description et fiche publique | Description recommandée, fiche Animation et rattachements aux animations | Présentation Coffrets seulement si ce périmètre est actif et si les offres sont publiables |
| Prestations, diagnostic fiscal BUM et qualification Coffret | Non applicables au seul produit Animation | Même conditionnalité E68 : suivi des prestations/coffrets réellement rattachés ; pas d’obligation artificielle de créer une prestation pour finaliser le dossier |
| Identité légale/fiscale, profil de facturation, commission, circuits de facturation | Ne pas réclamer ces pièces seulement au titre des reversements Coffrets | Exigences E68 selon fonctions financières effectivement visées ; montant, convention et facturation restent dans leurs parcours propriétaires |
| Compte bancaire/Stripe pour reversements | Non applicable au seul produit Animation | Requis lorsque reversement visé, conformément au contrat E68 ; ne bloque pas les fonctions Animation déjà acquises |
| Exigences par type de commerce | Appliquer les règles pertinentes et leur niveau, sans recopier une exigence exclusivement financière dans Animation | Conserver politique versionnée et justification d’applicabilité |

Réutiliser [architecture E68](../epic-68-preparation-onboarding/architecture-contrats.md) et [communications](../epic-68-preparation-onboarding/communications-supports.md) : aperçu du pack, destinataire confirmé, génération/envoi traçables, pas d’envoi silencieux lors d’un changement de périmètre. Les rendez-vous, questions et supports montrent les seuls sujets pertinents ; les réglages globaux demeurent dans Administration OnBoard. L’ajout Coffrets ouvre le complément dans Pro tout en laissant Animation opérationnel.

Contrat réalisé au lot 02 : le détail OnBoard expose `sections` pour l’applicabilité, `produitsVises`, `conventionsProduits`, `complementProduit` et `canEditPreparation`. Sur un dossier `CLOTURE`, un produit `A_PREPARER` autorise uniquement les rubriques déclarées dans `complementProduit.editableSections`. Le complément conserve le statut clos et les preuves antérieures ; il ne rouvre pas globalement le dossier. Sans complément, les rubriques restent en lecture seule. Un dossier abandonné reste non modifiable. Le rattachement explicite d’une convention ne vaut ni signature ni activation du produit.

### 3.3 Capacités et gestes Pro

La réponse de contexte expose des `capabilities` avec `mode` (`NORMAL`, `CONTINUITE`, `LECTURE`, `PREPARATION`), produits, cibles ou filtre de lecture, et motifs de refus. Ces capacités servent à présenter l’UX ; le serveur recharge l’état courant pour chaque appel. Le calcul intersecte statut commerce, produit, engagement ciblé, session personnelle, rôle et option salariés E72. Ne pas transformer les scopes techniques du jeton en preuve d’activation produit.

| Situation | Navigation / validations |
| --- | --- |
| Principal Animation seule | Accueil et activité Animation, Scanner, Animations, page publique Animation, compte/aide ; préparation si demandée. Prestations, reversements et fonctions Coffrets masqués. Accès salariés/PIN restent soumis aux règles E72/E70. |
| Principal mixte | Fonctions des deux produits, clairement nommées ; historique filtrable par nature et canal, sans mélanger lot libre et prestation Coffret. |
| Salarié | Arrivée directe sur Scanner ; menu Scanner/Historique uniquement selon E72. Aucun écran de paramétrage PIN, finance, produit ou équipe organisatrice. Les droits du commerce bornent les validations possibles. |
| Animation retiré | Pas de nouvelle participation/affectation. Passages possibles jusqu’à clôture pour participations acceptées avant retrait sur animations déjà publiées ; bons déjà attribués honorables selon leur validité. Historique autorisé en lecture. |
| Coffrets retiré | Prestations antérieurement engagées dans des coffrets vendus honorables selon validité ; règlements consultables par les rôles habilités. Aucun nouveau référencement de prestation/engagement commercial. |
| Suspension/révocation personnelle | Continuité refusée ; pas de droit implicite pour le salarié ni de contournement par PIN. |

Précision du correctif **E73-PRO-MENUS-ANIMATION-20261101** : dès qu’un commerce
est explicitement revu (`revue=VALIDEE`), la projection des menus Pro utilise ses
produits actifs, sa préparation et sa continuité, même avant la bascule de sa
commune. Le repli de présentation Animation+Coffrets reste réservé aux commerces
non revus dans une commune non basculée. Le navigateur continue de présenter
les capacités du serveur, sans les déduire des scopes techniques ni d’un nom de
produit local. Cette projection ne bascule aucune commune et ne modifie pas les
autorisations historiques d’admission, de création PIN ou de lecture des
notifications. Après livraison, la revalidation de session actualise les menus.

Un commerce Animation peut participer à une animation dotée de Coffrets sans fournir lui-même de prestation Coffrets. Au scan, le serveur renvoie la nature, le commerce autorisé, l’état et l’action disponible ; le refus est expliqué sans laisser un bouton de validation actif. Les confirmations de remise/consommation restent celles du dossier [lots](dotation-lots.md). Une erreur réseau garde le résultat incertain jusqu’à relecture ; une couleur ou un toast n’est pas une preuve de validation.

### 3.4 ERP, Support, CRM et Atelier — US24

Fiche commerçant et filtres ERP/Support : produits demandés/actifs/retirés, prérequis manquants et continuité limitée visibles séparément du statut général. Historique avec auteur/motif/date sans secret PIN ni token. OnBoard sélectionne les exigences ; Pro présente les capacités ; aucun de ces lecteurs ne recalcule l’ouverture.

Fiche Animation, préparation Atelier, tirage, bilans et exports portent `dotation` et le mode libre ; une ligne libre n’alimente ni instance Coffret, ni montant acheté, ni reversement ou commission Coffret. Les indicateurs « lots à remettre » distinguent remise déclarée externe, consommation numérique et prestations Coffrets. Le support peut retrouver la chaîne lot/attribution/bon/validation sous son habilitation, sans réattribuer par édition SQL.

Le CRM E71 qualifie Animation seule/Coffrets seuls/ensemble et renvoie au parcours métier. Les preuves de conversion restent celles d’E71 : une étiquette CRM n’active aucun produit, module ou compte. Les exports incluent le périmètre et la nature de dotation, et omettent les colonnes Coffrets sans objet au lieu d’y inscrire un montant libre fictif. La lecture d’une archive financière reste distincte de l’historique salarié.

## 4. Organisation, identité et équipe

### 4.1 Données et isolation

Conserver `PartenaireAnimation` comme identité métier d’organisation ; introduire `AppartenanceOrganisation(id, gestionnaireId, partenaireId, role, statut, version)` avec unicité `(gestionnaireId, partenaireId)`. L’identité de connexion conserve son ID existant et son email normalisé unique ; elle n’appartient plus exclusivement au partenaire historique. Les habilitations communales se rattachent à l’appartenance et aux communes préalablement validées par Localeo. Les sessions portent le contexte actif vérifié, pas une habilitation permanente.

Ajouter `RattachementCommuneOrganisation` (`DEMANDE`, `VALIDE`, `REFUSE`, `RETIRE`) avec décision Localeo et preuves de vérification d’identité/autorité. L’inscription en autonomie ne donne aucun accès communal. Un domaine d’email, un nom de mairie ou un SIRET déclaré ne valent pas vérification. Localeo assiste la récupération du dernier responsable après contrôle tracé, sans nouvelle organisation.

Changer d’organisation choisit explicitement une appartenance active, puis une commune autorisée. Une réponse lente de l’ancien contexte est ignorée par le frontend ; caches et formulaires privés sont invalidés. Le serveur contrôle ensemble identité, appartenance, commune, permission et état de l’objet sur chaque requête. Une ressource d’un autre tenant répond 404 ; l’utilisateur n’obtient pas ses métadonnées.

### 4.2 Profils et permissions complémentaires

| Profil | Pouvoirs de base | Compléments |
| --- | --- | --- |
| Responsable | Organisation/équipe, rattachements demandés, transfert de responsabilité ; export complet et fermeture réservés à ce rôle | Achat, gestion des autorisations Import/Communication et communes dans la limite des rattachements validés. Être responsable ne remplace pas une souscription ou un prérequis produit. |
| Gestionnaire | Préparer, exploiter et suivre les animations qui lui sont attribuées ; permissions métier E55/E56 conservées | Achat, Import commerçants et Communication attribués explicitement et indépendamment. |
| Lecteur | Consultation dans les communes/animations autorisées, sans mutation métier | Une délégation complémentaire, si explicitement accordée par le responsable, autorise seulement son parcours dédié ; elle ne change pas le profil ni ne donne le droit de publier ou tirer. |

Les pouvoirs sensibles internes Localeo (catalogue, cadeaux, remboursement, périmètre commerçant, neutralisation/contrôles) ne sont jamais dérivés d’un profil organisateur. Le responsable ne peut déléguer une commune non validée ou une permission interne. L’ajout ultérieur d’une commune à l’organisation ne l’ajoute à aucun collaborateur automatiquement. L’achat d’un module ne donne aucune permission à l’équipe.

### 4.3 Invitations, mot de passe et transfert

`InvitationOrganisation` porte organisation, email normalisé, rôle, communes et autorisations proposées, auteur, hash du secret, expiration, version, état (`EN_ATTENTE`, `ACCEPTEE`, `REMPLACEE`, `REVOQUEE`, `EXPIREE`). Validité **7 jours**, usage unique. Le renvoi invalide l’invitation précédente dans la même transaction ; l’email est préparé en outbox après validation, avec nom de l’organisation, rôle et durée. Aucune donnée d’un autre tenant dans l’email.

À l’acceptation, recontrôler le droit de l’invitant et les rattachements actuels. Email déjà associé : demander connexion au compte correspondant puis acceptation explicite ; ne pas changer son mot de passe ou ses autres appartenances. Email nouveau : initialisation selon la politique de mot de passe existante, puis acceptation. Une course entre deux acceptations produit une seule appartenance. Invitations expirées/remplacées/révoquées ne donnent aucun droit ; une invitation ne peut pas changer de destinataire après émission.

Récupération publique : réponse uniforme 202 pour email connu/inconnu, limitation de fréquence et contenu sans fuite d’existence ; lien **1 heure**, usage unique, finalité `REINITIALISATION` distincte d’une invitation. Réinitialisation et changement connecté appliquent la politique existante, révoquent les anciennes sessions du compte, invalident les anciens liens de récupération et exigent une reconnexion explicite. Le changement connecté vérifie le mot de passe courant. Secrets dans corps POST, jamais dans logs/analytics ; nettoyer l’URL après lecture et ne pas mettre en cache les pages sensibles.

Transfert de responsabilité : le responsable désigne un collaborateur actif ; invitation de transfert dédiée, acceptation authentifiée par celui-ci, vérification des deux appartenances puis bascule atomique. L’ancien reste responsable jusqu’à acceptation ; le dernier responsable ne peut se révoquer ni être rétrogradé avant succès. Le transfert peut être annulé tant qu’il n’est pas accepté ; une nouvelle proposition invalide la précédente. Une date d’expiration technique de la proposition n’efface jamais le responsable actuel.

Révocation/modification prend effet dès la requête suivante. Une tâche non commencée qui nécessite le droit retiré passe en suspension ; une tâche déjà engagée conserve sa continuité contrôlée, sans permettre à l’acteur révoqué de consulter, relancer ou étendre sa cible. La mutation d’équipe et l’invalidation de contexte sont atomiques ; les workers revérifient le contexte de service et les autorisations de diffusion applicables.

### 4.4 Présentation de Compte et équipe

Précision UX du **31 octobre 2026** : la page occupe la largeur de travail,
alignée à gauche. Trois accès internes explicites permettent de rejoindre
**Équipe**, **Mes organisations** et **Mon compte** sans changer de contexte ni
perdre l’état d’une commande. L’équipe de l’organisation courante vient en
premier ; **Inviter un collaborateur**, selon l’action autorisée par le serveur,
est le bouton principal de son en-tête. Les collaborateurs et les invitations
constituent deux sections distinctes ; actualisation, pagination et modification
d’un accès sont secondaires.

Un transfert de responsabilité à suivre précède les listes. Son acceptation
reste accessible au successeur autorisé, y compris sans rôle Responsable.
Les formulaires d’invitation et d’accès, puis les confirmations de révocation,
renvoi et transfert, s’ouvrent avant les listes avec focus et défilement vers le
contenu utile. Annuler rend le focus à l’action d’origine sans écriture. Une
confirmation sensible masque la saisie concurrente ; succès, refus et résultat
incertain sont présentés dans des messages titrés et contrastés. Une écriture
incertaine exige toujours une relecture puis le renvoi explicite du même corps
avec la même clé ; refermer une rubrique ne détruit pas cet état.

**Mes organisations** indique l’organisation courante et propose séparément
l’ouverture d’une autre appartenance active. **Mon compte** présente l’identité
connectée et le changement de mot de passe à la demande, avec reconnexion
annoncée. **Données et opérations sensibles**, réservé au responsable courant,
regroupe à la demande l’export et la fermeture, qui conservent leurs confirmations
et effets distincts. Les composants restent montés au repli pour préserver
leurs saisies et reprises. Le compte sans organisation conserve les seuls accès
organisations/sécurité, sans lecture d’équipe ni de réversibilité. Cette
présentation ne modifie aucun rôle, contrat ou invariant des sections précédentes.

### 4.5 Parcours du gestionnaire interne ERP

Précision UX du **31 octobre 2026** : ces parcours concernent l'opérateur interne
Localeo, sous ses habilitations existantes ; ils ne donnent aucun nouveau droit
au gestionnaire d'une organisation.

- **Nouvelle souscription** : partenaire et communes, forfait et droits réels,
  premier gestionnaire et accès, puis facturation et revue. Une confirmation
  explicite précède la création ; modifier une saisie invalide la revue.
  L'accès au dossier créé est direct. Gratuité activée et paiement attendu
  restent distingués ; l'invitation attend l'activation selon les règles serveur.
- **Exploitation** : statut et accès « En cours » visibles dès les filtres
  principaux, contexte conservé, pilotage avant les lots. Les liens vers
  exploitation et préparation terrain sont soumis aux capacités internes ;
  aucune action supplémentaire n'apparaît dans la surface Support.
- **Support** : demandes à traiter et échéances visibles, puis réponse au
  demandeur en action principale. Notes privées et suivi interne sont distincts.
  Les compteurs portent sur la page chargée, sans total global inventé. Une
  demande clôturée expose son historique et n'est plus comptée en retard ouvert.

Les confirmations, refus et résultats incertains sont lisibles et focalisés.
Consultation, annulation et ouverture d'une rubrique n'envoient aucune commande.
Permissions, contrôle de version, CSRF, clés d'idempotence et reprises après
réponse perdue restent ceux du serveur. Présentation alignée à gauche, largeur
disponible et lecture mobile/texte agrandi vérifiées, sans surcharge CSS globale.

## 5. Site Animation dédié et continuité Live

### 5.1 Deux expériences adaptées à leurs usages

Exigence du **18 octobre 2026** : privilégier la simplicité d’apprentissage et l’accessibilité, avec deux compositions distinctes. La plateforme organisateur adopte les codes d’une **application de gestion** ; le site public Animation ceux d’un **site de communication et de découverte**. Ils partagent identité visuelle, vocabulaire, composants accessibles et règles métier, sans imposer le même squelette de page. L’origine publique demeure `animations.localeo.city` ; l’évolution du 30 octobre précise séparément l’origine de gestion `gestion-animations.localeo.city` (§5.4).

| Dimension | Plateforme organisateur | Site public Animation |
| --- | --- | --- |
| Intention | Comprendre ce qui est à faire, gérer et vérifier le résultat d’une action | Comprendre l’offre, découvrir une animation et savoir comment participer |
| Structure | Navigation persistante, organisation/commune courantes explicites, titre et emplacement stables des actions, fil de retour liste → fiche → action | En-tête simple, navigation courte, contenus éditoriaux hiérarchisés, visuels utiles et appels à l’action lisibles |
| Accueil | Synthèse utile : prochaines actions, blocages, animations en cours ; éviter l’accumulation de compteurs sans action possible | Promesse compréhensible, animations par commune/date, explication du fonctionnement, accès participant et entrée « Organiser une animation » distincts |
| Contenus | Listes filtrables et paginées, statuts nommés, fiches structurées ; onglets seulement pour des ensembles cohérents | Fiches avec dates, lieu, principe du jeu, commerces, lots/modalités et bouton de participation ; aucune connexion exigée pour découvrir les contenus publics |
| Navigation | Rubriques stables : animations, commerçants, lots, communication, puis modules/souscription, équipe et aide selon droits ; retour conserve filtres et page | Parcours découvrir → comprendre → participer → retrouver mon parcours ; accès Live repérable, sans menus de gestion exposés au visiteur |
| Densité | Informations utiles à la tâche, détails secondaires à la demande ; formulaires regroupés et assistant pour la première création | Lecture progressive, titres explicites, texte court et images accompagnées d’un contenu compréhensible sans elles |

Le retour d’un utilisateur client va à l’accueil de sa plateforme ; un retour ERP n’apparaît que dans un contexte opérateur interne autorisé. « Voir le site public » et « Accéder à mon espace de gestion » annoncent clairement le changement d’espace. Les outils quotidiens ne changent pas de place selon la dotation ; seuls les contenus/étapes utiles sont adaptés. Une fonctionnalité non souscrite est présentée dans le catalogue de modules avec sa condition d’accès, sans multiplier les impasses dans les tâches courantes.

Précision du **31 octobre 2026**, correctif d’affichage du portail organisateur :
Assistant, Live, Préparation terrain, Validations, Communication, Tirage, Gains
et remise, Flyer et Bilan occupent la largeur de travail disponible, avec contenu
aligné à gauche. Les champs, aperçus de documents et dialogues conservent leurs
dimensions utiles ; retirer les plafonds des conteneurs à leur source, sans
empiler de surcharges CSS.

Les points d’attention de l’assistant précèdent les étapes à faire ; les étapes
déjà vérifiées restent consultables à la demande. La prochaine action figure dans l’en-tête, à côté du statut,
et ouvre son parcours depuis les rubriques de gestion,
avec retour au début utile du contenu, y compris sur mobile. Elle ne confirme
aucune transition. Les confirmations, droits, versions et clés d’idempotence
des parcours existants sont conservés. La communication rend explicites les
trois étapes brouillon, vérification des destinataires et confirmation de
diffusion ; module, autorisation ou fenêtre indisponibles restent expliqués.

Pour la **Configuration d'une chasse en préparation**, le parcours guidé
remplace le bandeau générique « Action suivante » : il présente les cinq étapes
numérotées et leur continuation, sans proposer simultanément un saut vers la
publication. Les actions générales restent disponibles dans les autres
rubriques de la fiche.

Précision du **31 octobre 2026**, création et préparation des chasses : le brief
et son pied d’actions exploitent toute la largeur disponible. Le récapitulatif
met en avant commune, dates, commerces et nombre d’étapes avec pictogrammes ;
présentation complète, sélection des lieux et modalités des lots se déplient
à la demande. Les accès Modifier conservent les saisies et permettent de revenir
au récapitulatif déjà visité si tous les éléments requis sont complets.

Un reçu serveur confirmé conduit à un accusé visible et focalisé sur la fiche,
avec **Suivre ma préparation** ou **Configurer mon animation** pour un parcours
réutilisé. Une panne de lecture auxiliaire ne masque pas cette confirmation.
Une réponse perdue exige toujours la recherche du reçu avant tout succès annoncé.
Cet accusé reste en mémoire et est limité à l’animation et au contexte courants.

L’assistant affiche une prochaine action concrète parmi les actions fournies
par le serveur, son intervenant et les étapes restant à traiter ; les aides
secondaires et vérifications acquises restent accessibles à la demande.
Un point commun à plusieurs étapes n’est affiché qu’une fois dans la synthèse,
avec sa gravité serveur et ses rubriques concernées. Les codes connus et leurs
libellés produits correspondent au même point ; aucune fusion approximative de
messages distincts. Un accès principal ouvre la première étape concernée dotée
d’une action serveur, avec les autres accès disponibles en détail. Les messages
restent uniques lorsque les étapes sont dépliées. Une prochaine étape déjà
entièrement représentée dans la synthèse n’est pas répétée en action prioritaire.
Le statut précis, l’intervenant, l’aide et l’accès Support restent consultables
pour chaque étape ; les compteurs d’étapes restent distincts du nombre de points.
Les points sont identifiables par trois repères concordants : blocage en rouge
avec pictogramme d’alerte et **À corriger avant publication**, avertissement en
orange avec triangle et **À vérifier**, information commune en bleu avec
pictogramme d’information. Fond et liseré distinguent chaque point ; le texte
de sévérité reste explicite sans perception de la couleur. Les erreurs de
lecture de l’assistant gardent leur annonce accessible et un repère rouge.
Pour une chasse, **Ouvrir — Informations et dates** rejoint directement
**Configuration → Organisation et lots → Calendrier**, sans ouvrir le financement. La
navigation ne vaut ni enregistrement ni validation de l’échéance.
Configuration affiche une seule rubrique à la fois, en pleine largeur, avec
consigne et repère de progression. Les panneaux visités gardent leurs saisies
et les blocages liés aux commandes incertaines. Paramètres, dates, règlement et
dotation ont des groupes explicitement nommés ; leur enregistrement reste
distinct, sans validation ni publication par simple navigation.

Précision du **31 octobre 2026**, guidage des validations Chasse : l'ordre
conseillé devient **Parcours → Organisation et lots → Commerces → Terrain →
Publication**. Enregistrer la relecture du parcours conduit à Organisation et
lots après confirmation, sans sauter directement aux invitations. Les étapes
affichent **Validée**, **À compléter**, **À vérifier**, **À enregistrer** ou
**Sans objet** depuis la projection de préparation ; les visites ne valent
aucune validation. Un contrôle absent ou indisponible ne conserve aucune coche.
Les contrôles restants de l'étape courante précèdent les détails, avec accès
au détail des validations. Les blocages généraux restent visibles même à 100 %.

Organisation et lots présente successivement **Présentation, Calendrier,
Règlement, Lots et remise**, une section visible. La navigation de saisie
n'enregistre rien ; la commande complète des paramètres garde son bouton et
son accusé. Les lots ne s'ouvrent qu'après enregistrement confirmé des
paramètres ; la dotation garde son enregistrement distinct. La confirmation
terrain de l'édition rejoint Terrain, avec ses QR publics et le suivi des
commerçants. QR et confirmation terrain ne peuvent être engagés en parallèle
pendant une commande non résolue. Les reçus et saisies restent montés dans les
étapes visitées ; publication et paiement conservent leurs confirmations.
Le pied du guide reste dans le flux sur mobile et texte agrandi pour laisser
le contenu consultable ; sur grand écran il reste accessible au défilement.

Refonte du **1er novembre 2026 — E73-UX-GUIDE-PUBLICATION** : l’Assistant
présente une seule étape développée, une consigne courte et une action
principale issue des actions serveur. La sélection d’une autre étape change
uniquement la consultation ; elle ne valide rien. Les étapes acquises, aides,
support et actions secondaires se déplient au besoin. Les points d’attention
restent dédupliqués et identifiables par texte, couleur et pictogramme ; le
premier est visible, les autres sont accessibles en détail. Un message partagé
ne doit jamais faire disparaître la prochaine action utile. Le suivi remplace
la préparation pour une animation déjà publiée ou terminée.

La chasse conserve les cinq étapes **Parcours → Organisation et lots →
Commerces → Terrain → Publication** dans un guide unique. Une étape seulement
occupe l’espace de travail ; les statuts proviennent des validations serveur,
jamais des visites. Dans Organisation et lots, Présentation, Calendrier,
Règlement puis Lots se succèdent sans seconde barre permanente. Les paramètres
facultatifs et la gestion des modifications restent secondaires. Continuer dans
les deux premières rubriques ne sauvegarde rien ; le passage du règlement aux
lots attend la confirmation de la commande complète des paramètres. La dotation
garde son enregistrement distinct. Le raccourci vers Commerces n’apparaît pas
avant l’étape Lots et reste bloqué par une saisie non enregistrée.

L’Assistant rejoint directement la bonne tâche : calendrier, règlement, lots,
parcours, commerces ou contrôle final. Ces liens ne déclenchent ni financement
ni publication. La barre générique Action suivante est retirée de l’Assistant,
comme du guide de configuration Chasse ; annulation et clôture restent dans
les actions secondaires avec leurs confirmations. Un parcours existant ne
présente plus une nouvelle génération au même niveau que sa validation.
Le contrôle final affiche une synthèse, les détails des refus et une seule
action de publication, suivie de sa confirmation explicite. Les brouillons,
versions, habilitations, reçus et commandes incertaines gardent leurs protections.

Contre-revue du **1er novembre 2026** : les neuf éléments de l’Assistant sont
des **contrôles**, distincts des cinq étapes du guide Chasse. La prochaine
action précède le choix secondaire **Changer de point à traiter**, replié.
Consulter un contrôle acquis affiche **Point déjà vérifié**, sans demander de
le refaire ni afficher une attente. **Reprendre la prochaine action** ramène
au contrôle recommandé, y compris lorsqu’un seul contrôle reste à traiter ;
cette reprise ne déclenche aucune commande. La sélection place le focus sur
le titre du contrôle. Les accès aux informations acquises restent dans les
actions secondaires. Après publication, leur consultation conserve le suivi.
Le contrôle **Identité de l’animation** concerne son nom et sa présentation,
et ouvre sa configuration ; il ne désigne pas le compte du gestionnaire.

Précision du **31 octobre 2026**, navigation de la fiche Animation : remplacer
la rangée défilante des quinze onglets par quatre espaces. Seules les
sous-rubriques de l’espace courant sont présentées sur ordinateur.

| Espace | Rubriques |
| --- | --- |
| Préparer | Assistant, Configuration, Invitations, Préparation terrain |
| Piloter | Live, Participants, Validations, Publication et clôture |
| Communiquer | Communication, Actualités selon habilitation, Flyer, Liens et QR de diffusion |
| Résultats | Fin et archivage, Tirage, Gains et remise, Bilan, Audit |

Précision du **11 novembre 2026** : l’action suivante rejoint le statut
dans l’en-tête. La barre des quatre espaces garde la même position dans
Préparer, Piloter, Communiquer et Résultats, y compris sur mobile et avec
le texte agrandi. Le guide conserve son action propre sans doublon ; les
actions secondaires sont regroupées dans « Autres actions sur l’animation ».

Les groupes et sous-rubriques utilisent la largeur disponible et reviennent
à la ligne si nécessaire ; aucun défilement horizontal ni libellé coupé.
Sur mobile, un seul sélecteur reprend les mêmes groupes. Icônes et libellés
restent associés, avec états actifs explicites et cibles de 44 px minimum.
L’espace actif découle de la rubrique ouverte, y compris par lien direct,
ancien alias, rechargement ou Action suivante. Changer d’espace ouvre sa première
rubrique ; cliquer l’espace déjà actif conserve la rubrique courante.

Chaque changement conserve le garde de sortie existant : si la navigation est
refusée, groupe, rubrique, URL et saisies restent inchangés. L’habilitation
Actualités reste contrôlée et l’accès direct interdit reste expliqué.
Le chargement différé d’une rubrique garde la navigation et les actions
affichées ; aucune écriture ni transition n’est exécutée par le menu.

### Identification et détail d’une participation — 11 novembre 2026

Dans les gagnants, le suivi des gains (Coffrets, lots externes, bons numériques)
et les listes de participants, l’e-mail autorisé remplace l’identifiant comme
libellé principal cliquable. Les noms disponibles restent secondaires ; une
adresse absente utilise un libellé neutre. L’identifiant technique est consultable
dans le détail, sans servir de nom de personne. La tombola publique garde son
adresse complète déjà autorisée par sa liste dédiée ; les autres moteurs
conservent le masquage des coordonnées existant.

Le clic ouvre une fenêtre **Détail de la participation**, en lecture seule :
coordonnées autorisées, date d’inscription en heure de Paris, état effectif,
progression, validations, confirmation e-mail si pertinente et référence.
Lecture ciblée au clic, sans collecter toutes les participations : habilitation
`animation:lire`, organisation, commune et animation vérifiées côté serveur.
Les faits du moteur ou la provenance gelée restent la source de l’état ;
aucun recalcul ni enregistrement métier dans l’interface. Aucune exposition
de PIN, QR, token ou secret d’accès habitant.

Chargement, refus et panne sont distincts. Après fermeture, le focus revient
à l’e-mail, sans quitter la page ou perdre filtres et pagination. Une réponse
tardive après fermeture ne rouvre pas la fenêtre. Une réponse d’une autre
animation/participation est refusée ; aucune donnée précédente n’est
conservée dans le détail après un échec.

### 5.2 Lisibilité, actions et accessibilité communes

- Les espaces de gestion partagent la même composition d’en-tête : retour explicite lorsqu’un parent existe, pictogramme et titre, description courte, contexte de commune/organisation, actions principales et secondaires identifiables. Le contenu utilise la largeur disponible et reste aligné à gauche ; les formulaires et dialogues conservent une largeur de lecture adaptée. Les gardes de sortie et les blocages d’une commande en cours restent dans le parcours appelant.
- Les rubriques courtes utilisent des onglets avec sélection visible et navigation clavier ; les flèches déplacent le focus et Entrée/Espace demandent l’ouverture. Les menus regroupés des animations et les sélecteurs des rubriques plus nombreuses conservent leurs fonctions et protections. Aucun menu n’impose un défilement horizontal. Les filtres ne sont pas présentés comme des onglets : leur sélection est annoncée, ils se replient sur mobile et la sélection principale de l’animation reste accessible.
- Les listes réutilisent les contrôles de pagination, les tableaux sur bureau et les fiches sur mobile. Chargement, absence de résultat et échec ont des états distincts, accompagnés d’un pictogramme et d’un texte. Les erreurs, avertissements, informations et succès suivent la même palette dans les pages et notifications. Un résultat incertain regroupe le diagnostic et la vérification proposée dans un seul avertissement, sans répétition automatique de la commande ni annonce de succès. Le focus n’est déplacé qu’aux points de retour déjà prévus par le parcours.
- Dans Localeo Animation, un pictogramme cohérent relie les rubriques de navigation aux titres des espaces et aux sections utiles (animation, terrain, communication, lots, bilan, abonnement, équipe, support). Il accompagne toujours un libellé ; les icônes décoratives sont masquées aux lecteurs d’écran. Un composant et une feuille de style partagés assurent le même traitement, sans multiplier les encadrés ni les surcharges CSS.
- Le tableau de bord présente les animations nécessitant une action avant les indicateurs et graphiques. Leur bouton principal reprend l’action recommandée par le serveur ; sans libellé disponible, il propose « Ouvrir l’animation ». Ce raccourci ouvre le parcours existant sans exécuter de transition. Les actions principales sont contrastées et accompagnées d’un repère utile ; actualisation, retours et options secondaires restent discrets et explicitement nommés.
- Une action principale identifiable par étape ; verbes concrets et vocabulaire utilisateur (« Créer une animation », « Publier », « Lot remis »). Pas de code technique, nom d’agrégat ou statut interne brut dans le parcours.
- Toujours distinguer brouillon enregistré, opération acceptée/en cours, succès confirmé et échec. Une réponse `202` affiche une progression, jamais une réussite anticipée. Après réponse perdue, consulter l’opération existante ; pas de nouveau tirage ou paiement suggéré à l’aveugle.
- Erreur à proximité du champ avec explication et correction possible ; récapitulatif accessible pour les formulaires longs. Préserver la saisie après erreur, signaler les changements non enregistrés et annoncer l’enregistrement effectif. Les confirmations sensibles indiquent l’objet et la conséquence ; les actions ordinaires n’ajoutent pas de confirmation inutile.
- Navigation complète au clavier, ordre de focus logique et focus visible ; lien d’évitement vers le contenu. Les fenêtres et menus gèrent entrée/sortie du focus, fermeture et retour au déclencheur, sans piège clavier. Les changements de page et résultats importants sont annoncés aux technologies d’assistance.
- Champs avec libellés persistants, instructions et erreurs associés ; boutons d’icône avec nom accessible, structure de titres et tableaux sémantiques. Aucun sens porté uniquement par couleur, icône, survol ou image ; les statuts comportent un texte, les images informatives une alternative utile.
- Cibles de conception : contraste texte courant d’au moins 4,5:1, grands textes et éléments graphiques utiles d’au moins 3:1 ; contrôles tactiles principaux visant 44 × 44 pixels CSS. Vérifier les états désactivés, survolés et focalisés séparément, sans considérer une couleur de marque comme preuve de lisibilité.
- À 320 pixels CSS et avec texte agrandi à 200 %, conserver contenu et actions sans défilement horizontal de toute la page. Une table réellement bidimensionnelle peut avoir son défilement local signalé ; fournir un accès lisible aux informations essentielles. Sur mobile, menu repliable nommé, header compact, aucune action essentielle masquée. La préférence d’un header sur une ligne ne justifie jamais une troncature empêchant l’usage au zoom.
- Respecter la réduction des animations ; aucun carrousel automatique ou effet visuel indispensable à la compréhension. Chargements, états vides et indisponibilités indiquent la prochaine action ; absence de Push ou refus de permission ne bloque pas la lecture/participation déjà autorisée.

#### Référence UX commune Pro / Animation — 1er novembre 2026

À la demande de l’utilisateur, **l’espace connecté Localeo Pro** devient la
référence de présentation pour Localeo Animation. La référence porte sur les
composants opérationnels de Pro (`ApplicationFrame`, `BusinessWorkspace`,
`MerchantNavigation`), et non sur ses écrans publics ou les styles historiques
de sa page d’accueil. Les menus et gestes restent ceux du rôle organisateur.

| Élément | Convention commune |
| --- | --- |
| Identité | Police DM Sans distribuée localement, corps 16 px, titres de la même famille ; fond gris bleuté, surfaces blanches, texte bleu foncé. |
| Cadre | Bandeau bleu foncé et navigation latérale de 224 px sur bureau ; contenu aligné à gauche et largeur de travail disponible. Le sélecteur de commune reste explicite. |
| Menu | Pictogrammes avec libellés, regroupements Organiser / Suivre l’activité / Mon organisation, sélection signalée par texte, fond et repère orange. Toutes les anciennes destinations restent accessibles. |
| Mobile | Accueil, Animations, Validations et Plus en bas de l’écran, sans recouvrir le contenu. Plus ouvre les autres rubriques avec focus contenu, Échap, retour au déclencheur et fermeture au changement de page ou au passage bureau. Le panneau défile intégralement au zoom et sur petit écran. |
| Pages et actions | Retour contextuel, titre et contexte avant les actions ; action principale bleue, commandes secondaires bordées, contrôles de 44 px minimum et rayon de 6 px. La suppression groupée des brouillons est secondaire et conserve sa confirmation. |
| Rubriques | Onglets avec sélection bleue soulignée ; les groupes de la fiche animation et le sélecteur mobile conservent leur organisation sans défilement horizontal. |
| Listes et formulaires | Tableaux sur bureau, fiches et filtres repliables sur mobile ; pagination compacte avec libellés accessibles, bornes et chargement conservés. Champs utilisables au toucher et focus visible orange. |
| Retours | Palette Pro commune pour information, succès, avertissement et erreur, avec pictogramme, texte et annonces accessibles. Un résultat incertain ne devient jamais un succès de présentation. |

La barre mobile utilise le même registre de destinations que le menu complet.
Les gardes de saisie, autorisations, confirmations, clés d’idempotence et états
serveur restent portés par leurs composants et services existants. Animation
conserve son sélecteur de commune, ses rubriques de publication et son menu
mobile avec gestion explicite du focus ; aucun parcours propre au commerçant
n’est importé. La police et sa licence sont embarquées sans appel Google Fonts.
Le [suivi de réalisation](suivi-implementation.md) porte la comparaison,
les vérifications et les limites du correctif.

#### Navigation Animation dans Localeo ERP — 30 octobre 2026

**E73-EVO-UX-ERP**, complément de l’US24 demandé pour simplifier l’ERP : une
entrée de menu ouvre une fonctionnalité identifiable, sans passer par une
section d’une même page carrefour. Les liens sont regroupés visuellement en
Animations, Équipes et contrats, Offre et modules, Pilotage. La vue d’ensemble
présente les mêmes fonctions disponibles ; les actions « Nouveau » restent
dans la liste concernée. Les anciennes routes et les favoris à fragment restent
résolubles. Les vues SQLAdmin historiques gardent leurs accès existants, sans
dupliquer la consultation des animations dans le menu métier.

| Critère ajouté | Comportement et preuve attendue |
| --- | --- |
| E73-EVO-UX-ERP-01 | Liens directs uniques vers les 17 fonctions existantes ; rubriques et liens filtrés selon les habilitations, une seule entrée active sur liste et détail. Tests Node sur le menu réellement servi et navigateur administrateur/opérateur |
| E73-EVO-UX-ERP-02 | Même structure fonctionnelle : fil d’Ariane, titre, sous-titre et un retour explicite. Liste → espace Animation, détail → liste, lot → animation. Reprendre les filtres seulement depuis le même parent sur la même origine ; l’arrivée directe n’exige aucun historique navigateur. Tests de navigation, refus de référent hostile, mobile et clavier |
| E73-EVO-UX-ERP-03 | Souscriptions, commandes, accès et consoles gardent formulaires, commandes, droits, conflits et reprise après résultat incertain ; conservation réservée à ADMIN, rendu Support inchangé. Rejouer les parcours des modules et les contrôles de session/routage |

Les 17 fonctions sont : animations et lots, demandes de création, préparation
des chasses, préparations accompagnées, exploitation des jeux, messages
participants, demandes d’organisation, accès partenaires, souscriptions,
commandes d’abonnement, offres et tarifs, catalogue commercial, modules souscrits, remboursements,
pilotage économique, fermeture des organisations, conservation des animations.
La checklist terrain des chasses reste distincte du service accompagné ; la
consultation des lots ne remplace pas les commandes d’exploitation du jeu.
Les offres globales SQLAdmin restent distinctes du catalogue tarifaire par
commune ; leur accès administrateur n’est pas supprimé ni ouvert aux autres profils.

Le changement est porté par la présentation ERP, propriétaire de sa navigation.
Aucune règle métier ne migre vers les vues ; domaine, API, données, migrations,
générateur et autres frontends restent inchangés. Deux assets ERP de présentation
supplémentaires sont servis avec `Cache-Control: no-store` sous la session
existante. Les commandes continuent d’être autorisées et auditées par leurs
services backend. Livraison backend nécessaire pour rendre ces sources visibles
sur TEST ; les preuves locales ne valent pas déploiement.

### 5.3 Validation des parcours avant généralisation

Avant de décliner tous les écrans, réaliser et examiner deux parcours représentatifs : **organisateur**, de la liste à la création puis au contrôle de publication ; **visiteur**, de la découverte à l’inscription puis au retour dans Live. Étendre ensuite la même grammaire aux lots, imports, campagnes, achats et équipe. La revue porte sur le squelette et les états réels (vide, attente, refus, erreur, succès), pas uniquement sur une maquette nominale.

La recette associe contrôles automatisés d’accessibilité et vérifications manuelles clavier, lecteur d’écran, zoom et mobile. Faire essayer les deux parcours à des personnes peu familières de Localeo, observer erreurs et hésitations sans leur dicter les actions, puis corriger les obstacles. Ces essais sont à organiser pendant la réalisation ; aucune conformité complète ni validation utilisateur n’est acquise par cette spécification. Voir les preuves UX du [plan de vérification](verification-livraison.md).

Séquence confirmée le 18 octobre : validation initiale par **Localeo**, corrections, puis validation avec la **première commune pilote, Martignas-sur-Jalle**, avant généralisation. Préparer les scénarios organisateur et participant pour ces deux étapes ; les personnes et créneaux de recette seront organisés lors de la réalisation.

### Évolution du 30 octobre 2026 — découverte et carnet Animation

**E73-EVO-UX-PUBLIC**, complément de CA23–24 demandé après ouverture de
`test-animations.localeo.city`. Le site invite à découvrir et participer aux
animations ; il reprend l’identité Coffrets (bleu profond, orange, papier,
DM Sans/Oswald, photographies et boutons) avec une navigation propre à cet usage.

| Critère ajouté | Comportement observable | Preuve prévue |
| --- | --- | --- |
| E73-EVO-UX-PUBLIC-01 | « Autour de moi » demande la position uniquement après clic ; sélection de la commune réellement identifiée, pas de la première commune proche ; refus, délai, résolution indisponible et commune hors réseau laissent le choix manuel accessible | Navigateur : permission simulée, commune absente de la synthèse, refus, délai, panne et réponse tardive après choix manuel |
| E73-EVO-UX-PUBLIC-02 | Commune et filtres avant la sélection éditoriale ; identité visuelle commune aux Coffrets, navigation Animation, accès au carnet ; mobile et clavier sans débordement, mouvements réduits respectés | Navigateur à 320/1440 px et texte 200 %, captures et contrôle visuel |
| E73-EVO-UX-PUBLIC-03 | Sur la surface ANIMATION, Live masque l’onglet Coffrets et ouvre les animations par défaut, y compris après une ancienne sélection Coffrets ; les accès directs, ajouts, données du carnet et gains Coffrets restent utilisables | Navigateur sur les deux surfaces et parcours direct vers un coffret |

La résolution utilise le contrat existant `POST /public/referencement/villes/proches/accueil`
d’E52 et uniquement son `contexte.communeOrigine` / `localisationStatut`. Le
frontend ne recalcule ni distances ni rattachements. Coordonnées en mémoire
pendant la requête, jamais dans URL, stockage, clés de cache ou Analytics ;
annulation à la sortie et priorité au choix manuel sur une réponse tardive.
Une commune hors réseau est nommée sans la remplacer par une commune voisine.
La page n’affiche pas les widgets marchands de cette projection. Une seule
résolution par action, pas d’appel par commune ; catalogue paginé à 20 conservé.

Présentation seulement : aucun changement des règles de participation,
qualification, gain, permission ou consentement ; leurs propriétaires backend
restent inchangés. API, migrations, données et générateur sans modification.
Les fixtures navigateur simulent les états de géolocalisation ; la permission
et la précision réelles sur téléphone restent à vérifier sur l’hébergement HTTPS.
Déploiement du frontend séparé, sans nouveau paramètre ; vérifier que
`Permissions-Policy` conserve `geolocation=(self)`.

L’analyse UX recommande ensuite une confirmation d’inscription suivie d’une
prochaine action claire, et une mise en scène des seuls acquis réels du jeu
(étape courante, visites confirmées, objets autorisés). Ces recommandations
ne créent ni points, ni classement, ni récompense, ni révélation d’étape future.
Une progression à 100 % ne vaut pas qualification. Le suivi distingue ces
recommandations de la tranche implémentée.

#### Analyse UX du parcours public

Analyse du 30 octobre sur les écrans et sources Marketplace/Live ; elle ne
remplace pas une observation d’utilisateurs sur le terrain. La direction
visuelle est celle d’un rendez-vous local vivant : photographies des lieux et
des participants, fond papier, titres de caractère et une seule couleur
d’action. L’accueil oriente, la fiche donne envie et explique, Live accompagne.
Les apparitions et survols restent courts et se désactivent en mode mouvements
réduits, conformément à la [recommandation W3C](https://www.w3.org/WAI/WCAG22/Techniques/css/C39.html).
La [géolocalisation navigateur](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition)
nécessite HTTPS et l’accord de l’utilisateur ; elle n’est pas un prérequis de participation.

| Moment | Friction observée dans les sources | Réponse UX et état de cette tranche |
| --- | --- | --- |
| Arriver | Identité verte différente des Coffrets, liste de rendez-vous sans orientation territoriale immédiate | Palette et typographies communes, promesse courte et commune avant les animations : implémenté localement |
| Trouver près de soi | Sélecteur après la mise en avant ; aucune géolocalisation sur cet accueil | « Autour de moi », choix manuel, filtres avant les résultats, pas de substitution de commune : implémenté localement |
| Comprendre | Visuel, dates et règles disponibles ; bénéfice générique fondé sur les passages commerçants, même pour les autres jeux | Priorité suivante : expliquer « Ce que je vais vivre » selon le moteur et les règles réellement exposées ; conserver une formulation neutre quand l’information manque |
| S’inscrire | L’appel « S’inscrire et suivre » et la marque Live mêlent plusieurs intentions | Priorité suivante : un verbe principal « Participer » ; expliquer séparément le carnet. Ne supprimer aucun champ contractuel sans étude métier |
| Commencer | L’inscription peut enchaîner directement sur Live | Priorité suivante : confirmation explicite puis prochaine action (« Continuer mon parcours », présenter son QR ou attendre le départ selon l’état serveur) ; aucune étape de permission Push imposée |
| Revenir | Onglet Coffrets visible et pouvant être la rubrique mémorisée par défaut | Onglet masqué sur ANIMATION et entrée Live adaptée ; anciens accès et données conservés : implémenté localement |
| Carnet vide | Le texte oriente surtout vers le scan chez un commerçant alors que l’inscription web existe | Priorité suivante : accès découverte et récupération de l’inscription clairement distingués du simple suivi d’une animation |
| Progresser | Le moteur expose déjà étape courante, activités, objets et acquis ; ceux-ci peuvent être mieux mis en scène | Proposition d’immersion : chemin des seules étapes autorisées, tampons pour visites confirmées, feedback bref de réussite annoncé aussi en texte ; pas de classement, de points inventés ni de futures énigmes dévoilées |

Mesures proposées pour une future évaluation, sans nouvelle collecte activée :
temps pour trouver une animation pertinente, compréhension de la prochaine
action, réussite de l’inscription et capacité à retrouver son parcours. Tester
un nouveau visiteur, un participant qui revient, un refus GPS, une commune sans
animation et un téléphone en connexion dégradée. Les recommandations suivantes
restent à concevoir et vérifier ; l’immersion complète n’est pas déclarée livrée.

### 5.4 Origines et continuité des parcours

**Décision du 11 novembre 2026 — E73-EVO-LIVE-DOMAINE.** La cible est désormais
un seul service/build Marketplace en `COFFRETS`, avec domaine Live ouvrant
`/live/carnet` par entrée React compatible Static Site ; règle HTTP Node
facultative. Le portail reste distinct. Les
[critères LD-01 à LD-05](localeo-live-entree-unique.md#évolution-du-11-novembre-2026--entrée-live-par-domaine-e73-evo-live-domaine)
remplacent ci-dessous la topologie à deux services publics de E73-EVO-DOMAINES-01
et son exigence de compatibilité historique. Les décisions datées suivantes
restent l'historique ; aucune migration n'est requise, rien n'étant en production.

Le dépôt Marketplace demeure le socle partagé : configuration de surface `ANIMATION` pour `animations.localeo.city`, composants et contrats communs, aucune copie indépendante du moteur. Accueil spécialisé : découvrir les animations, commune, fiches des commerces participants, rejoindre son parcours et ouvrir Live ; aucun achat Coffret requis. Le site Coffrets conserve ses propres parcours et liens existants. Une fiche Animation ne présente pas un commerce comme fournisseur de prestations Coffrets sans ce produit.

**Décision du 30 octobre 2026 — E73-EVO-DOMAINES.** Les sites suivants doivent
coexister sur des services distincts, avec des configurations indépendantes :

| Usage | Production | TEST | Application / surface |
| --- | --- | --- | --- |
| Site public des animations | `https://animations.localeo.city` | `https://test-animations.localeo.city` | `localeo-marketplace`, `LOCALEO_PUBLIC_SURFACE=ANIMATION` |
| Gestion des organisateurs | `https://gestion-animations.localeo.city` | `https://test-gestion-animations.localeo.city` | `localeo-animation` |
| Marketplace Coffrets | Adresse Coffrets existante, notamment `https://coffrets.localeo.city` | `https://test-marketplace.localeo.city` | `localeo-marketplace`, `LOCALEO_PUBLIC_SURFACE=COFFRETS` |

Le profil TEST du 22 octobre qui basculait l’accueil de la marketplace vers
Animation est remplacé. Les deux déploiements publics partagent les sources,
mais ni leur configuration d’accueil ni leur stockage navigateur. Le harnais
de recette distingue explicitement origine publique Animation et marketplace ;
les anciennes preuves et configurations privées de clone restent conservées.

| Critère complémentaire | Comportement à vérifier | Preuve ciblée |
| --- | --- | --- |
| E73-EVO-DOMAINES-01 | Accueil Coffrets et découverte Animation accessibles simultanément sur deux origines, sans bascule de la marketplace | Profils séparés, résolution de configuration et lectures HTTP locales des deux surfaces ; recette hébergée après livraison |
| E73-EVO-DOMAINES-02 | Liens de compte/service dirigés vers la gestion ; liens publics/participants vers le site public ; la surface publique n’obtient aucun droit de session de gestion | Templates backend distincts, contrôle d’origine exact et tests transport/session ; aucun wildcard |
| E73-EVO-DOMAINES-03 | Pro reconnaît les QR du nouveau site public et les origines historiques configurées ; domaine de gestion, domaines hostiles et TEST en production refusés | Contrôle de build Pro, classification et parcours navigateur |
| E73-EVO-DOMAINES-04 | Anciennes participations, QR, emails et carnets conservés ; changement de portail sans transfert silencieux de session/stockage/Push | Profils de transition, tests de sauvegarde/reprise et refus d’origines ; recette des anciens accès sur hébergement |

Ces critères complètent CA23–24 et les parcours de compte sans modifier leurs
IDs ni les 63 critères initiaux. Le backend reste propriétaire de l’identité,
des permissions et de la validation des QR ; aucune règle métier ni donnée ne
migre pour ce changement de domaines. Les schémas OpenAPI, données de démo et
générateurs de documents ne changent pas ; leurs URL dépendent des templates
existants. Les opérateurs doivent appliquer les nouveaux profils aux futures
préparations ; aucune réécriture des liens distribués ou des campagnes privées.

Les anciens domaines `animation.localeo.city` / `test-animation.localeo.city`
peuvent rester des alias de la gestion pendant une transition explicitement
configurée. Ajouter alors ces origines exactes à la liste de session du portail,
les retirer après validation des anciens liens et informer les utilisateurs
qu’une reconnexion peut être requise. Pas de redirection globale des routes
personnelles vers le site public. Conserver les origines QR historiques dans
Pro et les services nécessaires à la lecture des anciens liens ; la nouvelle
origine ne modifie ni ne prolonge leurs droits.

Les retours de paiement Animation (achat de lots et souscription) utilisent
aussi l’origine de gestion : mettre à jour leurs valeurs explicites. Les
sessions de paiement déjà créées gardent leurs anciens retours ; conserver
l’accès à ces chemins pendant leur transition. Les retours Coffrets et les
webhooks backend ne changent pas.

DNS, certificats TLS, association des domaines aux services, configuration des
origines et déploiement restent des opérations de livraison distinctes. Profils
versionnés et procédure : [configuration E73](../../exploitation/technique/configurer-epic-73.md).

Conserver les identifiants métier des animations/participations/commerces. Les anciennes routes `/animations`, `/animations/{id}`, `/animations/participants/{token}`, liens courts et QR distribués restent résolubles. Les pages publiques sans secret peuvent rediriger vers la route canonique. Une route contenant un accès personnel doit d’abord entrer dans son traitement existant de lecture/nettoyage, avec `Referrer-Policy: no-referrer`, absence d’analytics sur le secret et absence de cache ; ne pas copier un token dans une URL de suivi ou une redirection arbitraire.

Le carnet Live est local : déployer d’abord sur l’ancienne origine un écran de reprise visible qui conserve la lecture du carnet existant et utilise la sauvegarde/restauration personnelle existante. Présenter les éléments à reprendre, les erreurs/accès expirés et l’action explicite de restauration sur la nouvelle origine ; ne pas effacer l’ancien carnet avant vérification. Les deux origines peuvent rester utilisables pendant la transition. Un lien de participation reçu par email reste une voie de récupération sans recréer l’inscription ; pas de promesse de synchronisation serveur d’un carnet uniquement local.

Ne pas transférer automatiquement une subscription Web Push. Sur la nouvelle origine, vérifier la capacité du navigateur et sa permission, puis proposer facultativement l’activation et l’association à l’accès participant déjà vérifié ; un refus laisse participation et inbox utilisables. Les anciennes subscriptions suivent leur cycle de désabonnement/expiration et la déduplication serveur de notification ; elles ne justifient ni double inbox ni double campagne. Manifeste, service worker et installation PWA sont propres à l’origine ; leur cache ne contient pas les données privées. Le portail organisateur garde sa session sur le backend et ses origines exactes CORS/CSRF ; le domaine public ne reçoit pas pour autant un droit de session organisateur.

La recette couvre anciens liens/QR/PWA, retour d’email, carnet Coffrets et Animation, refus Push, stockage indisponible, accès expiré et absence de doublon. DNS/TLS, origines, URL canonique publique et liens email sont des paramètres de livraison, sans domaine ni envoi réellement activé par cette spécification.

## 6. Première animation, préparation, aide et nouvelle édition

### 6.1 Assistant et assistance

L’assistant présente les faits serveur dans l’ordre : identité/commune autorisée, offre et type accessibles, informations/dates, commerçants/accords, préparation du contenu, choix explicite de dotation et lots, règlement, contrôle de publication. Pour chaque étape : état acquis/manquant/non applicable, blocage précis, action et acteur attendu. Réutiliser les données déjà saisies. Les trois dotations ont leur parcours : Coffrets conserve commande/réservation ; libre externe décrit lots/responsable ; libre numérique prépare modèles/exemplaires/affectation. Le guide n’active ni module ni périmètre et n’appelle pas une commande de publication pour « tester » sa disponibilité.

La chasse est accompagnée à distance en V1. Étendre la demande de préparation existante avec `completeAt`, intervalles `attenteClient`, `targetDueAt`, `calendarVersion`, `revisedEstimateAt` et références aux opérations E55. États de service lisibles : `A_COMPLETER`, `EN_PREPARATION`, `ATTENTE_COMPLEMENT`, `PRETE`, `ECHEC_A_REPRENDRE`, `ANNULEE`. `EN_RETARD` est un indicateur calculé, pas une transition masquant l’état réel. L’échéance cible est **5 jours ouvrés de traitement** depuis la demande complète ; suspendre le compteur uniquement pendant l’attente d’une information indispensable, avec raison visible, puis reprendre le temps restant. Conserver toutes les périodes et les changements d’estimation ; ne pas réinitialiser le délai à chaque relance.

Le calendrier de service est versionné côté serveur, en Europe/Paris, avec jours ouvrés et fermetures explicitement configurés ; échéance exacte affichée au client. Une configuration manquante bloque l’annonce d’une échéance calculée, pas l’accès à la demande. Les dates/heures sont stockées en UTC ; les dates civiles et changements d’heure ne sont pas traités comme un nombre aveugle d’heures UTC.

Email au demandeur et notification portail pour complément requis ou préparation prête ; aucun crédit Communication consommé. Au dépassement, une alerte Ops par demande/version d’échéance, état visible et relance sur la même demande. Localeo renseigne une nouvelle estimation. Préparer scénario, étapes, énigmes et paramétrage à distance ; l’organisateur contrôle le parcours sur place et valide les contenus avant publication. Aucun déplacement terrain inclus. Échec/reprise ne débite pas une nouvelle génération ou une nouvelle chasse ; les contrôles de version, de bibliothèque et de publication E55 restent obligatoires.

### 6.2 Support

Aide contextuelle réelle et FAQ accessibles depuis chaque étape, versions alignées sur les produits et droits ; pas de lien actif vers une page vide. Liste privée de demandes avec état, date et auteur de la dernière réponse. À la création, enregistrer organisation, commune et animation éventuelle après vérification, sans se fier à un identifiant saisi dans un message public.

Les réponses visibles client et notes internes sont des catégories distinctes. Le client ne reçoit ni notes internes, ni messages d’une autre organisation, ni pièces privées hors droit. Cible de première réponse humaine **2 jours ouvrés** selon le même calendrier de service ; l’accusé automatique ne ferme pas l’attente. Aucun délai de résolution implicite. Les échanges restent sur la même demande ; refus/retrait de droit bloque lecture et ajout. Relier le service `support` existant par use case, sans dupliquer un stockage de contact libre exposé publiquement.

### 6.3 Nouvelle édition

Commande depuis une animation lisible, vers **la même commune uniquement**, même si l’acteur est habilité ailleurs. Le gestionnaire sélectionne les sections réutilisées (textes, visuels autorisés, scénario/paramètres) et fournit les nouvelles dates. Créer un nouveau brouillon avec ID propre, source/version sélectionnée et liste des éléments à revalider. Recontrôler droits du type/module, droits de réemploi et médias ; aucun quota de génération consommé du seul fait de copier.

Les références de commerçants peuvent être présentées comme candidats à reconfirmer, jamais comme accords acquis. Dotation, exemplaires, achats, réserve, règlement et conditions sont à revalider ; ne copier ni participant, consentement, gain, QR, paiement, consommation, population figée ni preuve d’accord. Une modification de la source après prévisualisation provoque un conflit, pas une copie silencieusement différente. Une réponse perdue se réconcilie par reçu d’idempotence, sans second brouillon.

## 7. Objectifs, acquisition et satisfaction

Les objectifs facultatifs sont enregistrés dans la version de configuration avant publication ; après publication, valeurs de référence immuables et affichées comme objectifs, pas comme résultats. Les données de mesure suivantes sont séparées des montants Coffrets existants :

| Mesure | Définition et limite |
| --- | --- |
| Inscrits | Participants métier distincts de l’animation ; une reprise de session n’est pas une inscription supplémentaire. |
| Parcours commencé | Premier événement de progression valide du moteur ; pour une tombola sans étape de jeu, inscription admissible comme début avec définition affichée. Pas une simple vue de page. |
| Parcours terminé | Condition de complétion du moteur, distincte du statut de gagnant ; gel/éligibilité réutilisent les faits E55. |
| Passages | Validations valides distinctes chez les commerçants, après corrections/annulations ; canal QR/PIN ne crée pas deux passages. |
| Gagnants | Bénéficiaires effectifs distincts ; suppléants non mobilisés et attributions remplacées séparés, non additionnés. |
| Lots remis | Libre numérique : consommation effective non annulée ; libre externe : déclaration tracée ; Coffrets : indicateurs existants de consommation, identifiés comme tels. Ne pas confondre email envoyé et remise. |
| Progression non terminée | Inscrits/commencés sans complétion à la date d’observation ; libeller « non terminé », pas « abandon certain ». |

Chaque réponse fournit date d’observation, fenêtre, unité, population, définition/version et état de disponibilité (`MESURE`, `NON_COLLECTE`, `NON_APPLICABLE`). `null` signifie absence de mesure, jamais zéro. Une édition est comparable si commune, moteur/type, définition et fenêtre sont comparables ; sinon afficher les écarts et empêcher une variation trompeuse. L’historique ne reçoit pas de valeurs inventées pour les mesures nouvelles.

Dans les vignettes du Bilan, l’unité technique `NOMBRE` n’est pas affichée ;
la valeur et son libellé restent visibles. Les autres unités sont conservées.

Le Bilan privilégie une lecture visuelle : pictogramme Lucide stable et libellé
visible par indicateur, chiffres mis en avant, grille aérée et séparateurs
simples. L’objectif reste chiffré ; une barre représente le réalisé uniquement
si la mesure est disponible et l’objectif positif. Un dépassement remplit la
barre sans plafonner la valeur affichée. Aucun pourcentage de conversion n’est
déduit entre des indicateurs de populations différentes.

La fraîcheur et l’état de l’édition sont résumés ; une couverture incomplète
reste visible. Période, définitions et populations sont regroupées dans
« Comprendre les indicateurs », dépliable au clavier. Les notes sont présentées
avec étoiles fractionnaires et valeur sur cinq, accompagnées du nombre de
réponses facultatives ; aucune étoile remplie n’est affichée sans note.
Les Coffrets, objectifs figés, origines d’inscription, avis et exports reprennent
ces repères. Icônes décoratives masquées aux lecteurs d’écran, libellés et
états textuels conservés, mobile et agrandissement à 200 % pris en compte.

Les bilans utilisent des agrégations SQL ou projections incrémentales datées, sans hydrater tous les participants, passages ou gains pour calculer leurs totaux. Les commentaires, sources détaillées et historiques sont des listes paginées en base ; la moyenne et le total ne sont pas recalculés à chaque page de commentaires. Regrouper les enrichissements nécessaires, sans requête par gain/prestation. Les mesures de requêtes/mémoire font croître les participants à nombre d’animations affichées constant ; les méthodes historiques de bilan en mémoire ne prouvent pas cette capacité.

Les sources de diffusion sont des codes publics opaques d’animation, accompagnés d’un libellé défini par le gestionnaire (« affiche mairie », etc.). Lien/QR transmet le code jusqu’à l’inscription de cette animation ; enregistrer le code valide présenté lors de cette inscription, sans réattribution ultérieure lors d’une visite. Code inconnu/absent ou autre animation → `INCONNUE`, pas rejet d’inscription ni accès supplémentaire. Pas de cookie publicitaire intersites ou association à des habitudes de navigation. Le QR de diffusion est distinct du QR personnel de validation.

Leur gestion est dans **Communiquer → Liens et QR de diffusion**, immédiatement
après **Flyer**, et demeure consultable en lecture seule après terminaison.
Chaque support affiche clics sur le lien, ouvertures via le QR et inscriptions
attribuées. Les deux premiers sont des ouvertures HTTP agrégées, non des
personnes uniques ni une preuve de scan physique ; répétitions et robots peuvent
être comptés. Aucun visiteur, IP ou agent utilisateur n’est enregistré dans ces
compteurs. La date `collecteDepuis` annonce le début effectif de mesure ; une
mesure absente reste « Non collecté », distincte de zéro.

Les nouveaux liens et PNG de QR passent par
`GET /public/animation-locale/diffusion/{code}?canal=LIEN|QR` : visibilité publique
du catalogue revérifiée, incrément atomique, puis redirection 303 non mise en
cache vers l’inscription Live configurée. La destination ne vient jamais du
client. Une animation archivée ou non visible n’ouvre pas ce parcours. La
vérification serveur déclare les capacités serveur, y compris tombola publique.
Les anciens liens directs et QR continuent d’attribuer les inscriptions, mais
leurs ouvertures ne sont pas mesurées ; remplacer les liens et retélécharger les
QR par support pour cette mesure. Le QR générique du flyer ne fournit pas de
ventilation par support. La migration v310 démarre les compteurs existants à
zéro et date la collecte sans reconstituer l’historique.

Questionnaire Live après clôture, facultatif : une réponse par participation, note entière 1 à 5 et commentaire texte facultatif (borne technique 2 000 caractères, rendu échappé). Une seconde écriture de la même réponse remplace son contenu sous version plutôt que d’ajouter une voix. Rejeter avant clôture, note hors intervalle ou accès à une autre participation. Aucun message automatique supplémentaire. Bilan organisateur : moyenne, nombre de réponses et commentaires, sans identité ni identifiant participant, email, token ou horodatage fin permettant de relier une réponse. Cela ne prétend pas rendre anonyme un commentaire où le répondant se nomme ; ne pas enrichir le texte avec son identité. Données sources soumises à la conservation des participations ; agrégats réellement non identifiants séparés.

Le PDF du Bilan présente les résultats, les objectifs lorsqu’ils existent,
la performance des liens et QR par support, la satisfaction avec commentaires,
puis l’audit de l’animation. Le **taux de satisfaction** vaut le nombre de notes
4 ou 5 divisé par le nombre de réponses, exprimé en pourcentage ; sans réponse,
il est non collecté. Ce dénominateur volontaire est explicité, sans prétendre
représenter tous les inscrits. L’audit fournit date, action, rôle et résultat,
sans coordonnées d’auteur ni métadonnées libres.

L’export garde le droit `animation:exporter` et le périmètre organisation/commune.
Résultats, sources, avis et audit proviennent d’un même instantané PostgreSQL
`REPEATABLE READ` ; lectures SQL par curseur puis rendu PDF hors transaction.
Chaque liste détaillée est bornée à 10 000 lignes. Au-delà, refus 422 explicite
`EXPORT_DIFFERE_REQUIS`, jamais un PDF tronqué ; aucun export différé automatique
n’est créé par ce correctif. Texte échappé, tableaux multipages et polices
embarquées préservent commentaires, accents et lignes longues.

## 8. Réversibilité et fermeture

### 8.1 Export complet

Seul le responsable courant peut demander l’export ou télécharger l’archive ; permission non délégable. Un gestionnaire avec `animation:exporter` conserve ses exports métier mais ne reçoit pas ce droit global. Demande idempotente, vérification de responsabilité à chaque consultation/téléchargement et au démarrage de la préparation. Un transfert de responsable change les droits de lecture sans rendre le lien accessible à l’ancien responsable.

États : `DEMANDE`, `EN_PREPARATION`, `DISPONIBLE`, `ECHEC_REPRENABLE`, `EXPIRE`, `ANNULE`. Inclus sans frais ; échéance cible **5 jours ouvrés** depuis demande valide, préparation accompagnée admise. L’archive est un instantané cohérent à une borne serveur `snapshotAt`, avec version de format, fichiers CSV UTF-8, médias transmissibles et guide. Relances/reprises conservent le dossier ; la génération d’une nouvelle archive ne remplace pas silencieusement un contenu déjà annoncé.

Le job capture les données transmissibles dans une source privée immuable et un manifeste durable : version de format, borne de capture, segments/IDs, références de versions des médias, tailles/empreintes, progression et erreurs. La capture utilise un instantané cohérent de base, puis la production CSV et la copie des médias s’effectuent hors transaction métier, en flux et par lots bornés. Les versions de médias référencées restent stables pendant l’assemblage ; fichier disparu ou modifié = écart visible, jamais substitution silencieuse. Mesurer la durée de l’instantané et son effet sur la maintenance PostgreSQL ; pour une capture trop longue, définir une autre source versionnée démontrant la même cohérence avant activation. Un simple `snapshotAt` et des pages de données courantes ne suffisent pas.

Reprise par segment/objet terminé et empreinte, sans dupliquer les lignes ni recharger tout le ZIP/CSV en mémoire. Une capture interrompue avant scellement est invalide : elle est recommencée avec une nouvelle borne annoncée dans le même dossier, sans mélanger les instants. Une capture scellée se réutilise jusqu’à succès ou abandon ; publication de l’archive uniquement après manifeste complet vérifié. Borner mémoire, espace temporaire et concurrence des exports ; capacité insuffisante met le travail en attente/échec reprenable, sans archive tronquée. Les captures et copies privées sont purgées au plus tard avec l’archive, ou lors de leur abandon/remplacement, suivant les obligations de conservation applicables. Le helper historique construisant tout le CSV en mémoire ne doit pas être réutilisé pour cet export organisation.

Contenu : organisation et rattachements autorisés ; données de ses animations/configurations, commerçants participants sous droit de transmission, participations transmissibles, lots, attributions et état de remise, engagements ouverts, documents clients transmis et médias dont le droit de réemploi est établi. Chaque CSV utilise des IDs stables et références documentées ; aucune donnée étrangère si un commerce est partagé entre organisations. Prévenir l’exécution de formules à l’ouverture des CSV, inventorier noms/taille/empreinte des médias, neutraliser les chemins d’archive et publier les omissions avec leur catégorie/motif. Ne pas exporter secrets, hashes de mots de passe, sessions, tokens/QR d’accès actifs, notes internes, coûts/marges internes, données d’autres organisations ou archives restreintes sans finalité de transmission. Exporter l’état d’un bon ne recrée pas un secret de consommation.

Disponibilité **30 jours après `availableAt`**, borne exclusive `expiresAt`. Stockage privé ; téléchargement via route authentifiée, sans URL permanente publique ; recontrôler responsable et état lors de la délivrance. Notification de disponibilité sans archive jointe ni secret dans l’email. À expiration, accès refusé et purge physique reprenable de l’archive/copies gérées ; conserver seulement le reçu nécessaire selon sa catégorie. Les données métier ne sont pas supprimées par cette purge. L’expiration d’une archive n’interdit pas une nouvelle demande valide.

### 8.2 Fermeture accompagnée

Commande distincte réservée au responsable, confirmation effective par Localeo après contrôle. À la demande validée, organisation `FERMETURE_EN_COURS` : nouveaux usages bloqués, historique et accès nécessaires aux seuls engagements ouverts conservés. Le dossier liste animation publiée, tirage/gain à traiter, bon non remis, commande/remboursement/document ou autre obligation ouverte et son domaine propriétaire ; l’absence de ligne ne peut provenir d’un filtre de l’écran.

Chaque engagement doit être résolu ou transféré explicitement à un responsable habilité qui accepte la prise en charge, avec référence, auteur et preuve. Un transfert de traitement n’autorise pas un changement de gagnant, de commerce de remise ou de propriété financière : les commandes métier dédiées restent nécessaires. Aucun transfert inter-tenant global par modification d’une FK. Si un transfert de l’engagement n’est pas supporté, maintenir sa continuité jusqu’à résolution ; ne pas le déclarer réglé.

Confirmation Localeo verrouille le dossier, revérifie l’absence d’engagement non pris en charge, enregistre date effective, auteur/motif et information de conservation communiquée au responsable, puis ferme les appartenances de cette organisation et ses accès résiduels. Une tâche concurrente créant une nouvelle obligation est interdite pendant fermeture ; une validation d’engagement encore admise reste sérialisée. Les accès des personnes à d’autres organisations restent intacts. La confirmation n’efface pas les preuves de tirage, remise, facturation ou contentieux ; elle ne supprime pas globalement les comptes d’identité partagés. La demande d’export seule n’ouvre jamais ce processus.

## 9. Contrats HTTP cibles et effets

Les routes suivantes sont **à implémenter**, sauf extensions explicitement signalées. Préfixes conformes aux domaines ; modèles camelCase pour les nouvelles projections, paramètres des routes existantes conservés lors d’une extension. Toute écriture protégée par cookie suit CSRF et origine exacte. `Idempotency-Key` et empreinte du corps sont obligatoires pour les commandes à effet (invitation, transfert, duplication, export, fermeture, changement de périmètre, relance) ; `expected_version` pour mutation d’un agrégat existant. Le reçu doit être consultable par son acteur encore autorisé dans le même tenant ; le rejeu ne contourne pas la révocation. Les secrets d’activation/reset utilisent leur consommabilité atomique, pas une restitution de secret par reçu.

| Opération cible | Corps essentiel / réponse | Contrôles et refus |
| --- | --- | --- |
| `GET /internal/referencement/commercants/{id}/perimetres` ; `POST .../perimetres/revue` ; `POST .../perimetres/{produit}/{demander,activer,retirer}` | Revue : `{produitsDemandes, motif, expected_version}` ; commande produit : `{motif, expected_version}` → produits, prérequis, continuité et version | Routes retenues au lot 02 : lecture métier bornée à la commune ; actions uniquement avec `commercants:perimetres_gerer` ; CSRF et reçu d’idempotence ; aucun état/preuve fourni par le client |
| `GET /internal/referencement/communes/{id}/perimetres/revue` ; `POST .../basculer` | Nombre de commerces restant à revoir ; `{motif, expected_version}` pour bascule | Sérialisation avec création/déplacement et admissions ; aucun commerce sans revue ; bascule locale seulement dans les tests isolés |
| `POST /internal/onboard/api/dossiers/{id}/conventions-produits` | `{produit, documentId, documentVersion, expectedVersion, motif, couvertureConfirmee:true}` → dossier et preuves par produit | Convention effectivement rattachée, signée et vérifiée ; couverture explicite pour chaque produit, y compris pièce mixte. Complément possible sur dossier clos sans réouverture globale ; refus si abandonné |
| `GET /internal/referencement/commercants/{id}/perimetres/historique` | `{items, nextCursor}` ; `pageSize` 25 par défaut, 100 maximum, curseur opaque lié au commerce et à sa commune | Lecture sous habilitation métier et commune courante ; tri date/ID décroissant, pagination SQL, aucun chargement des snapshots avant/après dans la page |
| Extension contexte Pro existant et projections OnBoard | `produits`, `capabilities`, `preparation`, `continuite`, version ; liens de préparation autorisés | Recontrôle backend indépendamment des champs projetés ; pas de déduction financière par interface |
| `POST /public/identite-acces/animation/organisations/demandes` | `{organisation, responsable, communesDemandees}` → 202 et référence de demande | Aucune habilitation ; contrôle Localeo distinct et limité à ses droits ERP |
| `GET /protected/identite-acces/animation/organisations` ; `PUT .../organisation-active` | Liste des appartenances ; `{organisationId, communeId?}` → contexte actualisé | 403 `APPARTENANCE_INACTIVE`, 404 contexte hors droit ; contexte serveur et CSRF renouvelés si requis |
| `GET /protected/identite-acces/animation/organisations/{id}/equipe` ; `POST .../invitations` | `{email, role, communeIds, autorisations, expected_version}` → 201 invitation sans token | Responsable, délégation bornée ; 409 invitation courante incompatible, 403 `DELEGATION_INTERDITE` |
| `POST .../invitations/{id}/renvoyer` et `/revoquer` | `{expected_version}` → état/version et email préparé si renvoi | Invalidation atomique ancien lien ; aucun accès avant acceptation |
| `POST /public/identite-acces/animation/invitations/accepter` | `{token, motDePasseInitial?}` ; compte existant : session du destinataire exigée | 410 `INVITATION_INACTIVE`, 403 `DESTINATAIRE_INCORRECT` ; réutilisation de l’identité, pas de reset implicite |
| `PATCH .../organisations/{id}/equipe/{membreId}` | `{role, communeIds, autorisations, statut, expected_version}` → appartenance | 409 `DERNIER_RESPONSABLE`, 403 hors délégation ; tâches en attente concernées suspendues |
| `POST .../organisations/{id}/transferts-responsabilite` puis `POST .../{transfertId}/accepter` | `{successeurId, expected_version}` puis version → nouveau responsable | Acceptation par successeur actif ; 409 version/état changé ; ancien responsable conservé jusqu’au commit |
| `POST /public/identite-acces/animation/mot-de-passe/demandes` ; `/reinitialisations` | `{email}` → 202 uniforme ; `{token,motDePasse}` → 204 | 410 lien inactif, politique mot de passe et rate limit ; toutes anciennes sessions du compte révoquées |
| `POST /protected/identite-acces/animation/mot-de-passe/changement` | `{motDePasseActuel,nouveauMotDePasse}` → 204 | Mauvais secret : refus générique, aucune modification ; reconnexion après succès |
| Extension `GET /protected/animation-locale/animations/{id}/validation-publication` | Étapes/manquants/acteur attendu ; aucune écriture | Réutiliser diagnostic E55 ; droits, dotation et périmètres à jour |
| Extension lecture préparation E55 ; `POST /protected/animation-locale/animations/{id}/preparation/relances` | `{operationId,expected_version,message?}` → même demande et suivi service | 409 opération hors animation ; pas de nouveau crédit ni génération |
| `GET/POST /protected/support/organisations/{id}/demandes` ; `GET/POST .../{demandeId}/messages` | `{communeId,animationId?,motif,message}` → thread public client, état, délai | Contrôle appartenance/commune ; liste paginée ; notes internes jamais dans schéma client |
| `POST /protected/animation-locale/animations/{id}/editions` | `{expected_version,communeId,dateDebut,dateFin,sections}` → 201 nouveau brouillon, provenance et revalidations | 422 `COMMUNE_EDITION_DIFFERENTE`, 409 source modifiée, 403 contenu non réutilisable |
| Extension bilan existant ; `PUT .../animations/{id}/objectifs` ; `POST .../{id}/sources-diffusion` | Objectifs versionnés ; `{libelle}` → code/lien de diffusion public | Objectifs figés à publication ; sources rattachées à une seule animation ; permissions métier |
| `GET /protected/animation-locale/animations/{animation_id}/participants/{participant_id}` | `ParticipantDetailAnimationPayload` : identité autorisée, inscription, état/progression et validations ; `Cache-Control: private, no-store` | `animation:lire`, tenant/commune/animation contrôlés ; absent, anonymisé ou hors animation : 404 ; export CSV existant préservé |
| `PUT /public/animation-locale/participants/{id}/satisfaction` | Accès personnel dans mécanisme protégé existant ; `{note,commentaire?,expected_version}` → réponse sans identité publique | 409 animation non clôturée ; 422 note invalide ; aucune notification auto |
| `POST /protected/animation-locale/organisations/{id}/exports` ; `GET .../exports/{exportId}` ; `/archive` | `{format: CSV_MEDIAS}` → 202 dossier/échéance ; état/manifest puis téléchargement privé | 403 `RESPONSABLE_REQUIS` ; 410 `EXPORT_EXPIRE` ; aucune fermeture implicite |
| `POST /protected/animation-locale/organisations/{id}/fermeture` ; confirmation `/internal/animation-locale/organisations/{id}/fermeture/confirmer` | `{motif,expected_version}` → dossier et engagements ; confirmation versionnée | Responsable pour demande, Localeo habilité pour confirmation ; 409 `ENGAGEMENTS_NON_RESOLUS` ; accès autres organisations inchangés |

Les listings nouveaux utilisent curseur opaque et taille par défaut 25, maximum 100, ordre déterministe date/ID ; le curseur est lié aux filtres et au tenant. Une page vide n’est pas un 404. Les routes existantes gardent leur pagination tant que leurs consommateurs n’ont pas été migrés. Erreurs structurées : `code`, `detail` lisible, corrélation, version courante si autorisée ; pas de token, contenu privé ni destinataire étranger. `401` session absente/expirée, `403` permission connue refusée, `404` ressource hors périmètre, `409` concurrence/état, `410` lien/artefact expiré, `422` saisie, `429` limitation. Réponse perdue → lecture d’état/reçu avant nouvelle écriture.

Outbox transactionnelle pour invitations, service préparation, réponses support et disponibilité export. Un même événement métier ne crée qu’un envoi/notification logique ; les retries conservent l’ID et ne consomment pas de quota Communication. Échec fournisseur visible dans le dossier, sans annoncer une livraison réussie.

## 10. Migration, conservation et preuves attendues

Migration additive : tables de périmètres, appartenances/invitations, rattachements, dossiers de service/réversibilité et mesures ; conserver les IDs, références de sessions et audits. Reprendre le partenaire historique comme appartenance existante uniquement lorsque l’association est prouvée ; validation explicite du responsable et des communes, sans déduire ce rôle d’une permission large historique. Modifier les résolveurs d’identité avant de retirer l’exclusivité historique `gestionnaire.partenaire_id`. Les sessions portant un contexte historique valide continuent sous contrôle courant ou demandent une reconnexion explicite ; aucune appartenance étrangère inférée d’un email.

Les périmètres de **chaque commerce sont revus et saisis manuellement**, sans proposition automatique (DEC-109). Avant la bascule d’une commune pilote, recenser les engagements existants et les contrôles qui les protègent. Les commerces non revus restent dans le fonctionnement antérieur de la zone non basculée ; aucun `NULL` ne devient implicitement Animation+Coffrets, ni un retrait silencieux. Dans la zone basculée, toute mutation exige une décision enregistrée. Ne pas mélanger ancienne et nouvelle politique pour une même commande. L’extension aux autres communes suit les preuves de la première.

Conservation : réutiliser le [registre moteur](../../juridique/interne/registre-interne-moteur-animation-2026-09-19.md) et les [catégories accès/validations](../identite-acces/conservation-validations-acces.md). Coordonnées participantes courantes : fin effective +12 mois calendaires ; preuves de tirage/attribution/remise : circuit probatoire cinq ans ; pièces comptables : dix ans depuis clôture de l’exercice ; génération brute devenue inutile : 30 jours après terminaison/annulation, sous contrôle des références utiles/gels. Les audits ordinaires ne deviennent pas des preuves conservées indéfiniment. Les données d’équipe suivent finalité d’accès/habilitation et fin de relation qualifiée, non une simple suspension d’option. Secrets inutiles retirés avec marqueurs anti-rejeu non authentifiants si nécessaires. Les demandes/échanges support suivent la catégorie Support du registre existant ; l’export ne leur attribue pas une nouvelle durée globale. La nouvelle archive téléchargeable a sa propre échéance explicite de 30 jours ; sa purge n’efface pas les sources. Satisfaction nominative/pseudonymisée rattachée à la participation, sans prolongation par consultation du bilan.

Les retraits dus sont réappliqués après restauration avant réouverture ; la continuité des engagements n’est pas une conservation générale de tous les secrets. Les fichiers privés restent hors base et hors dépôt documentaire. Les simulations et contrôles de gels/purge précèdent toute activation réelle ; le dispositif de reprise global et ses objectifs **4 h de perte maximale / 8 h de reprise** sont dans [vérification et livraison](verification-livraison.md).

| Preuves à produire (non exécutées par cette spécification) | CA |
| --- | --- |
| Domaine pur : ouverture avec prérequis, retrait concurrent d’affectation, continuité sur objets antérieurs et refus de suspension ; mêmes refus API/ERP/scan/PIN | 15 à 22 |
| OnBoard/Pro navigateur : Animation seule/mixte, ajout Coffrets incomplet, salarié scan direct, liens directs, téléphone étroit, chargement/erreur et aucun menu financier interdit | 16 à 22 |
| Anciennes routes/QR/carnet, sauvegarde puis restauration nouvelle origine, permission Push refusée, inbox maintenue, pas de perte des Coffrets présents dans Live | 23, 24 |
| ERP/Support/CRM/Atelier : trois dotations, filtres et exports exacts ; aucune somme ni instance Coffret créée pour libre ; conversion CRM sans activation | 25 |
| Invitations/reset : avant/à/après échéance, double acceptation, renvoi concurrent, compte existant multi-organisations, anti-énumération, révocation sessions et autre compte inchangé | 50 à 52 |
| Équipe PostgreSQL : deux révocations concurrentes du dernier responsable, transfert/acceptation/course retrait, permission retirée pendant tâche, isolation tenant après changement et réponse lente | 53 |
| Assistant et préparation : trois dotations, délai 5 jours ouvrés, attentes multiples, changement d’heure, relance/reprise sans débit, validation terrain obligatoire et alertes dédupliquées | 56, 57 |
| Support : refus note interne/autre organisation, première réponse humaine vs accusé, calendrier 2 jours ouvrés, réponse visible persistée et retry sans doublon | 58 |
| Édition : même commune, source modifiée, refus copie intercommune même habilitée, aucun secret/engagement copié, un brouillon après réponse perdue | 59 |
| Mesures : données absentes vs zéro, QR/PIN doublons, annulation consommation, remplacements gagnants, source inconnue, objectif figé, enquête facultative et notes invalides, bilan sans identité | 60 |
| Export/fermeture : responsable seul, transfert pendant préparation/téléchargement, échéance 30 jours, archive limitée/transmissible, CSV hostile, fermeture concurrente d’obligation, autres organisations préservées, purge archive sans sources | 62 |

Adapter les fixtures du générateur : commerce Animation seul/mixte/retiré avec engagements, salarié limité, même gestionnaire sur deux organisations et communes distinctes, invitation expirée, préparation en attente/retard, trois dotations, enquête/bilan sans collecte, export expiré et fermeture avec gain ouvert. Les données de démonstration ne constituent pas une preuve déployée. Les contrats documentaires et embarqués Animation/Pro/Marketplace doivent être générés et testés ensemble lors de l’implémentation ; aucun JSON de production n’est réécrit manuellement à ce stade.
