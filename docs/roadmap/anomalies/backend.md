# Registre des anomalies

Publication Git du **1er novembre 2026**, après les contrôles locaux décrits
ci-dessous : backend `daff81c` (contrainte des droits) et `7f131d3` (en-têtes et
connexion), Animation `d607cb9`, Pro `a946ee2`, Marketplace/Live `bb8b585`,
committés et poussés sur `main`. Cette publication complète les constats locaux
des trois anomalies du 1er novembre ; elle ne prouve pas leur déploiement
applicatif. La correction SQL v286 a été appliquée sur TEST comme indiqué
ci-dessous ; la migration catalogue v285 y reste en attente.

## ANO-INTERNE-CHARTE-CRM-20261104 — Harmonisation des espaces de gestion

- **Demande / constat** : prendre Localeo CRM comme référence pour ERP, Ops,
  OnBoard, Support et Atelier. Les écrans mélangeaient actions orange/bleues,
  navigation sombre, rayons et titres divergents, avec un bloc de styles Ops
  en ligne doublonné par sa feuille CSS.
- **Correction locale**, sur backend `b9304c9` : palette CRM partagée dans
  `app-header.css`, également consommée par CRM ; actions principales vertes
  avec texte blanc, secondaires blanches, navigation ERP claire et état actif
  vert doux. Champs, listes, panneaux, onglets, focus et typographie harmonisés
  dans les feuilles propriétaires. Styles Ops consolidés dans `ops.css`.
  Les connexions internes et consoles historiques ERP reprennent les mêmes
  tokens. La largeur de travail de Support et Atelier n'est plus plafonnée.
- **Parcours préservés** : menu hiérarchique ERP, priorités P1/P2/P3 Ops,
  dossiers OnBoard, recherche/support et préparation Atelier. Aucun changement
  de liens, permissions, confirmations, commandes métier ou contrats API.
  Sans impact migration, données de démonstration ou configuration serveur :
  ce correctif ne modifie que la présentation et ses preuves.
- **Preuves locales** : recettes navigateur `erp-page-template` (24 scénarios),
  `erp-menu-ux` (35), `crm` (sept vues sur six largeurs), `header-mobile`
  (six applications, huit largeurs et texte/zoom 200 %), `admin-shell` (8),
  `connexion-interne`, `shell-navigation`, `epic65-finance-erp`, `ops-alert-priorities` (12),
  `onboard-dossier-ux` (24), `onboard-administration` (7),
  `epic73-support-organisations-ux`, `support-loading`, `atelier-assiste-erp`,
  `atelier-pwa` et `preparation-erp` réussies. Captures PC/mobile inspectées.
  L'assertion de titre Atelier du test d'en-tête passe volontairement de
  16,8 à 18 px pour vérifier la nouvelle charte, sans retirer ses contrôles
  de débordement, focus ou cibles tactiles.
  Les fixtures navigateur Support et Atelier servent maintenant le vrai SVG
  avec son type MIME et vérifient son chargement avant capture.
- **Contrôles Python** : 668 tests architecture/recensement/API Ops/PWA CRM
  réussis au premier passage ; le test Git isolé restant a rencontré
  `WinError 6` dans la capture Windows, puis réussi avec sortie fichier et
  `-s`, sans modification de l'assertion. Sept tests de rendu Ops réussis.
  Quatre avertissements de dépréciation de l'adaptateur datetime SQLite.
- **Limites** : vérifications sur sources locales et API simulées, pas de
  validation authentifiée de TEST. Les empreintes PWA incluent déjà les
  ressources modifiées. Correctif backend enregistré dans le commit `32106fd` ;
  sa publication Git ne constitue pas une vérification du déploiement sur TEST.
  La [charte canonique](../../architecture/transverse/identite-entetes-applications.md#charte-des-espaces-de-gestion-internes--référence-crm)
  définit les valeurs communes.

## ANO-BE-RECHERCHE-LOGIN-20261103 — Retrouver un commerce par son accès Pro

- **Attendu / observé** : la liste ERP doit retrouver un commerce depuis son
  login Pro ; la requête ne cherchait que dans `commercants.nom`. Reproduction
  locale sur backend `aadb55f` : cinq cas échouent sur les résultats attendus
  pour un login complet, partiel, en majuscules ou comportant `+`.
- **Correction** : le champ devient « Rechercher par nom ou login ». Le serveur
  combine le nom et l’existence d’un identifiant Pro correspondant, sans distinction
  de casse, avec suppression des espaces périphériques. `%`, `_` et `\` restent
  du texte littéral ; `+` est préservé. Le login n’est pas ajouté aux données de
  liste, et une simple adresse de contact sans accès initialisé n’est pas assimilée
  à un identifiant. La recherche n’inclut pas les logins salariés.
- **Frontières et coût** : projection de lecture dans `ServiceAtelierErp`, sans
  nouvelle règle métier. Le filtre de communes autorisées reste appliqué avant
  comptage/pagination, ainsi que les filtres commune et produit. Sous-requête
  `EXISTS` corrélée sur l’identifiant unique du commerce : pas de doublon, collecte
  complète en mémoire ou requête supplémentaire par ligne. Le contrat `query`
  et la réponse existante sont conservés ; aucune migration d’index requise pour
  cette extension de la recherche textuelle existante.
- **Preuves** : 11 tests SQL/API réussis dans `test_erp_recherche_commercants.py`,
  dont filtres, droits de commune, pagination, absence de doublon et caractères
  littéraux. La fixture SQLite a été complétée pour la lecture réelle des
  périmètres déjà utilisée par le service, sans neutraliser ses contrôles.
  16 scénarios navigateur réussis à 320/1280 px et texte agrandi, avec API simulée,
  contrôle du login transmis, clavier et axe. Capture mobile inspectée.
  627 tests d’architecture/recensement réussis ; le premier lancement avait
  rencontré `WinError 50` lors de `git init` dans un test, résolu par exécution
  sans capture pytest et redirection des sorties vers un fichier local.
- **Impacts** : backend/ERP et [guide de formation](../../produit/formation/backend/guide-backoffice-localeo.md).
  Aucun changement de mot de passe, accès, permission, données, générateur ou
  configuration d’exploitation. Correctif local, non déployé sur TEST.

## ANO-BE-CONNEXION-ERP-20261101 — Connexion interne hors charte ERP

Signalement du 1er novembre 2026 : la connexion interne conserve une ancienne
palette verte, un nom sans symbole et une présentation distincte de l’ERP.
La page de choix du mot de passe partage cette ancienne feuille de style.

Correction locale dans le backend : signature statique Localeo ERP, symbole et
tokens de `app-header.css` réutilisés ; fond clair, en-tête bleu nuit, action
principale orange, champs lisibles et aide secondaire repliable. Le formulaire
propose l’affichage volontaire des mots de passe, un état d’attente et des retours
erreur/succès contrastés avec focus et annonce accessibles. Sans JavaScript,
l’action reste désactivée et un message explique le prérequis ; aucun secret ne
doit partir dans une query string. Connexion, initialisation et réinitialisation
conservent les API, CSRF, confidentialité du fragment et absence d’autoconnexion.

Seuls `app-header.css` et `header-mark.svg` rejoignent les ressources publiques
exactement autorisées par les deux contrôles HTTP. Aucun chargement du contexte
ERP ni du script d’en-tête authentifié sur les formulaires publics. Le lien
d’évitement commun se masque selon sa hauteur réelle pour rester invisible hors
focus même avec le texte agrandi.

Vérifications locales : 124 tests API/surfaces/sessions et 623 contrôles
d’architecture réussis ; parcours navigateur E69 à 390/1280 px rejoué avec succès.
Contrôle dédié à 320/390/1280 px et texte 200 % : logo chargé, absence de débordement,
clavier, cibles tactiles, visibilité des mots de passe, attente, erreurs 401/429,
connexion réussie, confirmation, purge du fragment et retour à la connexion.
Initialisation et réinitialisation vérifiées ; sans JavaScript, bouton désactivé
et message de prérequis visible (contrôlé via le nœud `noscript` et capture).
Captures inspectées ; tests des cinq en-têtes partagés rejoués après correction
du lien d’évitement. Le premier contrôle de succès avait une fixture HTML sans
charset ; l’encodage de cette seule fixture a été corrigé, sans changer l’assertion.

Périmètre : présentation backend et documentation transverse. Aucun invariant,
permission métier, contrat de données, migration ou générateur modifié. Travaux
locaux préexistants conservés ; aucun commit, push ou déploiement pour ce correctif.

## ANO-BE-ACCES-DROITS-20261101 — Compte interne complet refusé en 409

Reproduit sur TEST le 1er novembre 2026 : création nominative Backoffice +
Finance avec les sept autorisations dédiées, refus `COMPTE_INTERNE_CONFLIT`,
corrélation `LOC-2b82fa47-343f-45a6-b037-5c529f8a2adc`. La contrainte PostgreSQL
`ck_utilisateur_autorisations_dediees` issue de v275 ne connaissait que quatre
codes ; le domaine et l’API en proposent sept. La transaction a annulé le
compte et son invitation, sans création partielle.

Correction : migration additive au suivi `v286_autorisations_internes_completes.sql`,
remplaçant cette CHECK par une liste fermée de sept codes et une longueur maximale
de sept. Aucun octroi automatique, changement de rôle ou modification des comptes
préexistants. Le domaine reste propriétaire des combinaisons de profils et droits.
La readiness exige la nouvelle contrainte nommée. API, consommateurs et générateur
conservent leurs contrats ; aucun nouveau droit ni scénario fonctionnel à ajouter.

Preuves sur PostgreSQL 18 isolé : ancien DDL refusé avec la contrainte attendue,
migration réelle puis création réussie et rejeu sans double invitation ; droits
préexistants conservés, codes inconnus, JSON invalide, trop de valeurs et profils
incompatibles refusés. 52 tests migration/readiness/API/runner et 634 contrôles
architecture/service comptes réussis, sans skip. Base backend `b66a5a8` avec
correctif local ; aucun commit ni push dans cette opération.

Application ciblée sur TEST réalisée après sauvegarde complète et lecture intégrale
de l’archive, sans exercice de restauration. Le runner a d’abord vérifié toutes les
empreintes, puis appliqué uniquement v286 depuis une copie privée des sources
excluant v285. Vérification : CHECK validée, empreinte enregistrée, deux comptes
préexistants conservés avant création du nouvel accès ; rejeu API **201**, puis
lecture **200** avec les deux profils et les sept autorisations, invitation en file.
Empreinte v286 : `9dfb8edc75f0247b7345d476dc840bbf6d822fe43c83b6317c2927f75d1b5e7b`.
Les preuves et la sauvegarde restent dans les opérations privées du backend.

Limites : v285 (catalogue Premium) reste explicitement en attente ; ne pas annoncer
une mise à niveau complète du schéma. La nouvelle garde readiness n’est pas encore
déployée. La création des accès ne prouve ni la réception des emails ni la première
connexion de leurs bénéficiaires. Une prochaine livraison doit inclure v286 avant
le code de readiness correspondant.

## ANO-TRANSVERSE-HEADER-20261101 — Identités divergentes dans les huit applications

Signalement du 1er novembre 2026 : homogénéiser l’identité dans les en-têtes de
Pro, Animation, ERP, OnBoard, Live, Ops, Support et Atelier.

Constat local : logo absent des cinq outils internes, tailles et polices
différentes, séparateur backend, sous-titres Pro/Animation et nom ou symbole
masqués sur certains petits écrans. Plusieurs générations de règles CSS
redéfinissaient les mêmes éléments ; Live conservait notamment une règle
globale imposant sa police éditoriale au nom de l’application.

Correction dans les quatre dépôts applicatifs : symbole SVG identique,
fond bleu nuit, marque blanche et nom orange, police système et dimensions
communes. Les actions peuvent passer à la ligne pour garder le nom lisible.
Les règles de marque sont consolidées à leur source, avec un composant Live
partagé entre ses entrées et le header commun aux cinq outils backend.
La [convention transverse](../../architecture/transverse/identite-entetes-applications.md)
porte les valeurs et les règles d’accessibilité.

Bases locales : backend `b66a5a8`, commerçant `10374cc`, Animation `255629b`,
Marketplace/Live `6c1aaac`, avec modifications de travail. Aucun déploiement
ni vérification authentifiée de TEST dans ce correctif.

Impacts : présentation et ressources statiques uniquement ; aucun contrat API
métier, invariant, migration, droit ou donnée de démonstration modifié.
Le SVG backend est autorisé par sa route statique existante et entre dans
l’empreinte PWA. Live conserve son symbole dans le cache public et inclut son
contenu dans l’empreinte du build ; les réponses privées restent exclues.

Vérifications locales : tests d’en-têtes mobile/bureau, clavier, actions PWA,
session et texte agrandi ; captures inspectées. Backend : 623 contrôles
d’architecture, 21 tests HTTP/PWA, menu/permissions, lifecycle quatre PWA,
24 scénarios de gabarit ERP et 261 contrôles du guide ERP réussis.
Le contrôle final backend couvre 40 variantes normales, 10 variantes de texte
à 200 % et 5 variantes de zoom ; gabarit ERP rejoué après l’ajustement rem.
Animation : types, lint, build isolé, 18 tests ciblés et 10 formats navigateur
réussis. Pro : 36 tests ciblés, 7 scénarios navigateur et build isolé réussis.
Live : 16 tests de cache/mise à jour et 16 scénarios navigateur d’en-tête et
d’installation réussis ; build isolé de production et lint ciblé réussis.
Le badge TEST final reprend la capsule de Pro ; les 7 cas navigateur 320/390/1280
et texte agrandi sont rejoués avec succès après cet ajustement.

Limite indépendante : `live-animation-surface.spec.cjs` présente deux échecs
sur ses attentes d’onglets secondaires (Mes participations / Mes lots).
Même résultat reproduit sur HEAD `6c1aaac` dans un worktree isolé : 2 réussites,
2 échecs. Ces attentes ne sont pas modifiées par l’harmonisation des en-têtes.

## ANO-BE-E73-RECHERCHE-PROJECTION — Recherche globale indisponible sur TEST

Signalement du **30 octobre 2026**, corrélation fournie
`LOC-0a04e2ae-880a-4d6f-bbb6-f436722d6809`. Reproduction publique sans
authentification sur `test-api.localeo.city` :
`GET /public/commercialisation/recherche?q=animation` répond **503**,
`CATALOGUE_ANIMATION_EN_PREPARATION`
(`LOC-37da267c-e494-4b91-a4cf-ba448b4af398`). Même refus avec les termes
`Latresne` et `coffret`. La liste
`GET /public/animation-locale/animations?page_size=1` répond **200**
(`LOC-6d6affd5-24ea-4719-bbfc-975e3a70dc33`).

Dans le backend local `3a6f930`, ce code est exclusivement levé par
`ServiceCatalogueAnimationsPubliques.suggestions` lorsqu'une animation du
périmètre public possède `nom_recherche = NULL`. La migration `v276` ajoute la
projection et ses index sans remplir l'historique ; la reprise bornée existante
reste une étape d'exploitation nécessaire. Les nouveaux compteurs publics ne
déclenchent pas ce code. La base et les journaux privés de TEST n'ont pas été
consultés : le nombre de lignes concernées, leur provenance et le SHA déployé
restent à constater sur le service.

La [procédure de reprise](../../exploitation/exploitation/parcours-plateforme-animation.md#réparer-catalogue_animation_en_preparation)
précise désormais les commandes de simulation et d'application par lots dans
le Shell du backend concerné, puis le contrôle de recherche HTTP 200. Le garde
503 est conservé pour éviter des résultats incomplets. Aucun changement de
contrat, règle métier, participation, schéma ou migration n'est requis ; aucune
preuve ne permet d'attribuer les lignes historiques au générateur.

**Reprise distante non exécutée** : l'erreur reproduite reste à lever sur TEST
avec l'outil de maintenance. Les modifications locales concernent la procédure,
ce suivi et le test PostgreSQL du retour de la recherche après reprise complète.

Preuves locales sur `3a6f930` avec les deux assertions supplémentaires :
**19 tests réussis**, incluant une vraie base PostgreSQL jetable, le refus
initial et après reprise partielle, le retour des résultats après reprise
complète, la simulation sans écriture, la conservation des versions/dates et
le contrat HTTP 503. La base locale a été arrêtée après vérification.
**620 contrôles d'architecture réussis**. Les guides, leurs liens et les
130 sources exportées sont validés ; `git diff --check` réussit dans les deux
dépôts touchés. Test enregistré dans le commit backend `baa559c`, à la demande
de l'utilisateur. Aucun déploiement ou réparation distante vérifié.

## ANO-BE-E73-CORS-COFFRETS — Origine Coffrets TEST absente du CORS

Signalement du **30 octobre 2026** depuis `https://test-coffrets.localeo.city`.
Reproduction HTTP publique, sans authentification, sur
`https://test-api.localeo.city/public/commercialisation/coffrets/page?avec_prestations=false&page_size=8` :
GET 200 sans `Access-Control-Allow-Origin`, préflight OPTIONS 400 pour cette
origine, contre OPTIONS 200 avec origine autorisée pour `test-marketplace`.
Corrélations : GET `LOC-bbfbe2cc-46be-4299-9de1-6be8935b5084`, OPTIONS refusé
`LOC-7b4c09d1-05e8-4fbc-83b9-6236a727751b`.

Cause démontrée : l'origine exacte n'est pas autorisée dans la réponse du
backend TEST. Le profil d'exemple backend et la liste du guide de configuration
omettaient également ce domaine. Correction locale : ajout de cette seule
origine, en conservant les origines existantes, sans joker ni élargissement des
origines de session du portail organisateur. Le middleware et les règles métier
ne changent pas ; aucun schéma, migration, donnée ou générateur affecté.

Test de reproduction local : GET Coffrets 200 sans en-tête autorisé avant
correction du profil (une réussite historique, un échec sur la nouvelle origine).
`tests/api/test_marketplace_cors.py` vérifie le profil versionné, GET et
préflight, ancienne/nouvelle origine, refus des origines inconnues, ressemblantes
et HTTP. **22 tests CORS réussis** après correction du profil, incluant les
contrôles Animation et Pro voisins. Les journaux sont dans
`localeo-backend/tmp/cors-coffrets-*.log`. Liens documentaires et 130 sources
exportées vérifiés ; `git diff --check` réussi dans les deux dépôts touchés.

**Configuration distante restant à appliquer** : ajouter
`https://test-coffrets.localeo.city` à `LOCALEO_CORS_ALLOW_ORIGINS` du service
qui sert `test-api.localeo.city`, sans supprimer les valeurs présentes, puis
redémarrer/redéployer et rejouer GET/OPTIONS. La lecture HTTP n'a pas consulté
les variables ou journaux privés de l'hébergeur. Profil et tests enregistrés dans
le commit backend `c25d202`, à la demande de l'utilisateur après validation.
Aucune modification de la configuration distante.

## Correction du 30 octobre 2026 — navigation Animation ERP

Demande utilisateur : une entrée de menu par fonctionnalité, en-têtes et retours
harmonisés. L’audit des sources constate trois entrées vers la même page
`/internal/erp/animation` avec des fragments, des destinations répétées, trois
modules reconstruisant leurs titres hors du shell et quatre consoles autonomes
avec des en-têtes différents. « Offres et tarifs » utilise également un shell
historique sans retour métier.

Correction rattachée à **E73-EVO-UX-ERP** : 17 destinations fonctionnelles
directes, classées en quatre rubriques ; accueil récapitulatif cohérent avec les
droits ; en-tête fonctionnel et retour structurel partagés. Les offres globales
restent distinctes du catalogue par commune. Les anciennes routes, favoris et
vues techniques demeurent disponibles. Conservation réservée à ADMIN, rendu
Support, règles métier et API conservés.

La revue a détecté une impasse pour les opérateurs ayant seulement
`animation.gerer` : les consoles leur proposaient un retour vers un espace
interdit. Trois reproductions échouent avant correction puis réussissent ; le
retour utilise maintenant l’accueil ERP dans ce contexte, sans élargir les
permissions. La lecture des captures a aussi révélé que les nouveaux groupes
de menu n’héritaient pas du style des liens directs : test rouge sur affichage
en ligne, puis correction des lignes et cibles tactiles de 44 px.

Preuves, périmètre des dépôts et limites : [suivi E73](../../specifications/epic-73-animation-et-ou-coffrets/suivi-implementation.md).
Aucun changement de données, migration, générateur ou droits ; aucun commit,
push ou déploiement.

## ALL
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-ALL-02 | Global | Il est difficile de comprendre ce qu'il est necessaire pour qu'un coffret soit commercialisable, peux tu améliorer l'aide sur cette partie das les IHMs et améliorer l'UX concernant le référecemet d'un nouveau coffret et prestation | Corrigée - tests navigateur et accès ERP OK |

## ONBOARD
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-OB-01 | OnBoard | Ajouter un composant de téléversement d’image plutôt qu’une saisie de référence d’image. | Corrigée - téléversement et reprise testés |
| ANO-OB-02 | OnBoard | Il faut simplivier la saisie de l'onglet Finance en appliquat par exemple la même adresse par défaut partout (en cochant: utiliser la même adresse) | Corrigée - adresse commune et adresse distincte testées |


## ERP
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-ERP-01 | ERP | Revoir l’UX pour rendre l’interface responsive. | Corrigée - validée à 320, 390, 768 et 1280 px |
| ANO-ERP-02 | ERP | Rempalcer la saisie d'une reference d'image par un vrai composant d'upload. | Corrigée - quatre formulaires et contrôles upload testés |
| ANO-ERP-03 | ERP | Sur l'ihm de composition d'un coffret, lorsque l'on recherche un commercant, des résultats sont trouvés mais ils n'affichemets. il faudrait affichier les prestations non vendables en on selectionnables en plus de ceux vendable. | Corrigée - recherche, motifs et recontrôle serveur validés |



## Recette automatisée E73 — 23 octobre 2026

Suivi selon le [cycle de correctif](../../organisation/cycle-correctif.md), pour
la campagne TEST `e73-20261022-e856fb`, backend initialement déployé `4be06ef`,
puis `3720a08` constaté sur API et BackOffice, et lanceur local.
Les références RM sont celles de la recette ; les rapports et accès restent privés.
Un défaut du lanceur ne constitue pas, à lui seul, une anomalie du produit.

| Référence | Attendu et échec reproduit | Cause et correction | Vérification / état |
| --- | --- | --- | --- |
| RM-08-01 — harnais des essais principaux | La lecture initiale puis la vérification des essais UI doivent reconnaître le module effectivement accordé, même en présence d'un cadeau du même module. | **Défauts du harnais privé** : garde `require` absente du contexte initial, sélecteur ambigu entre essai et cadeau, attente du chargement manquante et libellé Communication supposé au lieu du libellé réel du catalogue. Gardes rétablies ; carte Essai unique attendue et comparée au catalogue effectif. | **Corrigés et rejoués** : trois octrois UI distincts HTTP 201, une seule référence par module ; commandes déjà acceptées rapprochées sans nouvel octroi. Quatorze jours, quotas, historique, lecture client et absence de commande/facture/paiement supplémentaires vérifiés. Erreurs initiales conservées dans `essais-principaux-ui-clone-prive.json`. Parcours principal partiel, aucun succès complet RM-08-01 déclaré. |
| RM-24-02 — état de l'opération de régénération dans le harnais | Après une régénération acceptée, le harnais doit relire le résultat avant de télécharger le PDF. | **Défaut d'oracle privé** : attente de l'état domaine `REUSSIE` alors que l'API le traduit explicitement en `SUCCEEDED`. L'opération était déjà réussie et son document version 2 existait. | **Corrigé et rejoué** : état API canonique vérifié ; commande journalisée réutilisée localement, lectures et téléchargement poursuivis sans nouveau POST de régénération. PDF rendu, QR décodé et nouvel export vérifiés ; rapprochement privé conservé. Aucun worker supplémentaire ni écriture directe de statut. |
| RM-24-02 — libellé de dotation du flyer exporté | Le média d'une animation LIBRE EXTERNE d'un lot doit annoncer ce lot et ses consignes. Le PDF du clone initial annonce des coffrets digitaux ; rendu initial conservé. | **Écart de version confirmé** : la base `3720a08` précède les travaux utilisateur du flyer. Quatre modules relus de ces travaux sont sélectionnés dans un overlay privé ; le service reprend uniquement la projection de contenu, sans intégrer les évolutions d'illustration. Aucun fichier utilisateur modifié. | **Parcours principal rejoué sur le clone** : 52 tests passent sans skip, dont décodage des QR après installation de dépendances QA privées. Régénération normale : visuel « 1 LOT À GAGNER », un commerce et consignes externes ; QR réel du PDF rendu décodé vers l'URL canonique. Un nouvel export contient le même PDF, manifeste et droits vérifiés, anciennes archives inchangées. Index privé `exports-clone-flyer-principal-sceau.json`. Les anciennes métadonnées GET restent hors de cet overlay ; RM-24 n'est pas intégralement validé, notification Brevo 401 et variantes restantes conservées. Aucun déploiement sur TEST partagé. |
| RM-24-02 — reçu de création documentaire | Le dépôt ERP d'un PDF synthétique transmissible doit retourner son document et ses rattachements. Sur le clone isolé, le POST documentaire renvoie **500** après création persistée du document et de son rattachement ; corrélation `LOC-df0058c0-3921-4d2e-ac37-0d42fdf8e18b`. | **Défaut produit reproduit** : après commit et refresh des scalaires, le use case ferme sa session sans charger `rattachements` ; leur sérialisation API déclenche `DetachedInstanceError`. Chargement explicite de cette relation dans la session existante, sans changer le contrat, les droits, le scan documentaire ni les transitions. | **Corrigée localement et rejouée sur le clone isolé** : deux reproductions PostgreSQL échouent avant patch avec/sans rattachement ; les trois tests ciblés passent après, dont incident stockage sans écriture partielle. Les FK document/source et rattachement/document sont réelles ; 670 contrôles architecture/application/accès API/sécurité upload passent. Le document déjà committé est réconcilié par GET normal, sans dépôt répété. Un nouveau spécimen distinct, scanné CLEAN par ClamAV local réel, obtient ensuite **HTTP 200** avec son document et son rattachement sérialisés ; preuve privée `exports-clone-correctif-rejeu-http.json`. Aucun déploiement sur TEST partagé ; cette preuve ne valide pas toute la recette RM-24-02. |
| RM-10-01 — consignes du second lot | Le harnais doit remplir deux lots externes ; il attend indéfiniment le second textarea alors que le premier a déjà été rempli. | **Défaut du sélecteur de test** : le nom accessible du label enveloppant le textarea peut inclure son contenu saisi. Sélection du rôle textbox avec le préfixe stable de l'intitulé ; aucun champ produit ni règle assoupli. | **Corrigé et rejoué sur le clone** : échec `run-1792787584279-47ba` avant création serveur ; `run-1792787672542-dd44` intégralement réussi, A×2/B×1, zéro refusé, ordre B/A/A et brouillon relu. Les 54 tests Node du module passent. |
| RM-16-04 — libellés de refus du harnais | Après l'import UI réussi, vérifier le refus sans droit échoue malgré l'absence de dépôt. | **Défaut d'oracle/attente** : attendre la fin du chargement des droits et reconnaître aussi les messages explicites AUTORISATION_REQUISE et MODULE_NON_OUVERT. Les refus serveur et l'absence de formulaire restent exigés. | **Corrigé et rejoué** : deux étapes d'import conservées, quatre contrôles navigateur/API de refus réussis dans `import-ui-refus-clone-rapport.json` ; aucune recréation du lot terminé. Les 64 tests Node features/core passent. |
| RM-16-04 — compteurs des propositions d'import | Un aperçu de cinq lignes contient deux créations valides, une mise à jour et deux erreurs non sélectionnables ; « Créations proposées » doit annoncer deux. Sur le clone isolé, l'API annonce quatre créations, dont les lignes EMAIL_INVALIDE et SIRET_INVALIDE. | **Défaut produit reproduit** : la projection SQL compte les propositions sans leur état. Filtrage des créations, mises à jour et inchangés sur PRETE/CONFIRMEE/REUSSIE ; les totaux, erreurs, conflits et sélections restent indépendants. Aucun contrat, droit ou plan d'import assoupli. | **Corrigée localement et rejouée sur le clone isolé** : huit échecs ciblés avant patch, puis cinq tests PostgreSQL avec FK réelles et 634 contrôles d'architecture/API passent. Le même aperçu annonce ensuite **2 créations / 1 mise à jour / 2 erreurs** ; sa confirmation limitée aux trois lignes valides atteint TERMINE_PARTIEL, avec trois succès uniques, deux lignes écartées, rapport téléchargé et relectures stables. Rapport privé `variantes-import-clone-rapport.json`, aperçu initial et journal conservés. Aucun correctif déployé sur TEST partagé ; le rejeu API ne prouve pas l'interface navigateur complète. |
| RM-06-02 | Les trois modules sont sélectionnables ; délai dépassé sur le libellé singulier « Chasse au trésor ». | Le catalogue affiche « Chasses au trésor ». Sélecteurs fondés sur le libellé exact du catalogue par code ; assertions de prix, durée et capacités conservées. | **Corrigée** : 28 tests Node commerciaux passent, rejeu TEST `run-1792768742029-444b` entièrement réussi. |
| RM-02-02 | Après acceptation, le nouveau gestionnaire doit pouvoir se reconnecter ; la fixture restait PLANIFIE. Puis attente erronée d'un message de module absent au lieu du refus de délégation Import. | L'identité et l'appartenance ACTIVE sont désormais relues avant de marquer le compte ACTIF. Le contrôle Import attend le refus explicite d'autorisation. Reprise sur identité déjà acceptée, sans nouvelle invitation. | **Corrigée pour ces défauts** : premier échec `run-1792769379860-752b`, rejeu `run-1792769657431-9361` : quatre étapes réussies, variantes déconnexion/paiement encore bloquées. 22 tests Node comptes passent. |
| RM-02-03 | Après acceptation depuis un autre navigateur, inviter/renvoyer doit conserver un suivi exploitable ; délai dépassé sur « Modification confirmée ». | **Défaut du lanceur** : son GET équipe ne rafraîchissait pas la version conservée dans React après l'acceptation externe. Clic sur **Actualiser l'équipe** et attente de sa réponse avant l'invitation suivante ; contrôle de concurrence conservé. | **Corrigée pour ce défaut** : régression reproduite avant correction, 23 tests Node comptes réussis après. Rejeu `run-1792772077493-1a33` : trois étapes réussies, appartenances A/B, renvoi ancien lien refusé/nouveau accepté et changement vers un compte existant. Scénario partiel uniquement faute de destinataire et de lien réellement expiré de plus de sept jours. |
| RM-16-01 / RM-16-05 — mapping | Le mapping CSV doit permettre de choisir Nom commercial ; délai dépassé sur le label exact avant aperçu. | **Défaut du lanceur** : sélecteur de mapping corrigé d'après le nom accessible réel des listes de colonnes. | **Corrigée et rejouée** : RM-16-01 réussi dans `run-1792770510590-ff8a`. Après réconciliation de V1 et traitement réel de V2 **TERMINE avec une mise à jour**, RM-16-05 réussit dans `run-1792774394870-77f5`, preuves antérieures reliées par empreinte et valeurs relues sans répéter la création ou la confirmation d'import. |
| RM-16-02 — taille frontière | Le fichier de 2 000 000 octets doit tester la borne de taille, sans rencontrer une autre limite du parseur. | **Défaut de fixture** : environ deux millions de lignes vides remplacées par des lignes d'espacement de 7 000 octets, tailles frontières exactes conservées. | **Corrigée et rejouée sur TEST** : 8 tests avec le vrai parseur et 30 tests Node réussis ; `run-1792772585337-3eed` entièrement réussi, six étapes et inventaire ERP inchangé, sans confirmation d'import. |
| RM-19-01 | Support doit permettre une demande liée au brouillon A1 ; aucun bouton de création après chargement. | **Défaut produit reproduit** : le garde des sessions navigateur Animation omettait `/protected/support/organisations/...`. Lecture authentifiée refusée 403 « Route de session Animation refusée. », corrélation `LOC-c93eb896-88b8-4e8f-b7d2-cfc655a0636a`. Correctif borné aux chemins existants de demandes, messages et reçus ; isolation, origines et CSRF conservés. Un sélecteur relatif de FAQ a aussi été corrigé dans le lanceur. | **Corrigée, déployée et rejouée sur TEST** : `/sante.version=1.0.0+3720a08` sur API et BackOffice ; `run-1792772538662-5ec2` entièrement réussi. 192 tests transport/session/import et 618 contrôles d'architecture réussis ; revue indépendante OK. Les trois rapports d'échec précédents restent conservés. Message public, statut email et réception effective restent distingués. |
| RM-20-01 / RM-20-03 — dates d'édition | Les dates UTC de la fixture doivent correspondre aux jours Paris choisis dans le vrai formulaire. Écart de 1 ms à la fin de période. | **Défaut de fixture** : fin inclusive `22:59:59.999Z` opposée à la borne exclusive `23:00:00.000Z` produite par le frontend. Validation précoce ajoutée, sans modifier le contrat produit. | **Corrigée et rejouée sur TEST** : `run-1792774003896-55cb` réussit entièrement les deux scénarios ; vrais jours Paris/UTC du formulaire vérifiés. |
| RM-20-01 / RM-20-03 — comparaison et refus A2 | Le retour de source doit être comparé sans dépendre de l'ordre des clés JSON ; le refus intercommune doit suivre le vrai contrat backend. L'ancien passage `run-1792773143259-e84c` attendait à tort 409 au lieu de 422 et échouait sur l'ordre des clés d'objets identiques. | **Défauts d'oracles du lanceur** : `JSON.stringify` remplacé par `isDeepStrictEqual`, sans suppression de clé ni conversion de type, ordre des tableaux toujours strict. Contrôle A2 sur HTTP **422**, code `COMMUNE_EDITION_DIFFERENTE` et violation de chemin `communeId`, selon la route existante. Aucun contrat produit modifié. | **Corrigées et rejouées sur TEST** : 94 tests public-operations réussis, revue indépendante OK ; `run-1792774003896-55cb` entièrement réussi pour RM-20-01 et RM-20-03. Anciennes éditions/sources et journaux conservés ; nouveaux brouillons, conflit et perte contrôlée de réponse rapprochés sans doublon. |
| RM-16-05 — relecture Description | Après traitement réel de V2, relire la description persistée sans relancer l'import. Trois étapes réussissent, la quatrième dépasse le délai sur `getByLabel('Description', exact: true)`. | **Défaut de sélecteur du lanceur** : le label enveloppant le textarea contient aussi son texte, ce qui invalide la recherche exacte. Sélecteur corrigé sans remise à zéro des données ni du worker. | **Corrigée et rejouée sur TEST** : `run-1792774394870-77f5`, verdict `REUSSI_AUTOMATIQUE` ; empreinte des trois étapes antérieures, relecture UI et aperçu non confirmé prouvent les valeurs finales et l'absence de doublon. |
| RM-20-02 — refus de publication | La tentative sur un brouillon incomplet doit être refusée selon le contrat historique, sans changer source, participants, gains ou commande. Le lanceur attendait à tort 409. | **Défaut d'oracle du lanceur** : la route retourne 422 et son détail exact ; comportement confirmé par `tests/api/test_validation_publication_brouillon.py`, huit tests réussis. Diagnostic distant : `legacyDetailMatches`, `sourceUnchanged`, `validationUnchanged` vrais. Oracle corrigé et contrôles avant/après renforcés, sans modifier le produit. | **Corrigée pour ce défaut, scénario encore partiel** : `run-1792774637562-4cb7` réussit l'étape implémentée, puis termine **BLOQUE** sur sa couverture restante ; 96 tests Node public-operations passent. Aucun échec courant ni succès intégral RM-20-02 déclaré. |
| RM-25-05 — reprise des sessions commerçants historiques | Après restauration vérifiée du snapshot TEST du 23 octobre à 20 h 08, le rejeu du journal indépendant échoue avec `RESTAURATION_VERSION_MANQUANTE` ; le garde conserve la réouverture bloquée. | **Défaut produit reproduit** : deux révocations de sessions principales exportent légitimement `security_version: null`, conformément au modèle et à la migration v258 ; le lecteur exigeait un entier positif. Le correctif accepte uniquement un NULL explicite sur une colonne nullable, applique toujours la révocation et préserve un éventuel compteur cible plus récent. Champs absents, compteurs invalides et NULL obligatoires restent refusés. Journal original conservé intact. | **Corrigée localement et rejouée sur le clone isolé** : reproduction en échec avant correction ; **4 tests PostgreSQL et 9 tests unitaires réussis**, sans skip. Le journal original est rejoué complètement, la fermeture des capacités termine et les **4 assertions HTTP de maintien du garde passent**. Correctif appliqué au clone sur base `3720a08`, avec empreintes ; aucun commit, push ou déploiement du correctif sur TEST partagé. RM-25-05 reste partiel faute de preuve hébergée complète. |
| RM-25-05 — vérificateur HTTP local | Les assertions doivent suivre les droits sauvegardés et les contrats réels. La première sonde précédait l'écoute du serveur ; le premier rejeu attendait uniquement A1 et un refus B1 en 403. | **Défauts de lancement/oracles** : attente du démarrage effectif ; périmètre exact lu dans le manifeste, qui autorise ce gestionnaire sur **A1 et A2** ; refus B1 attendu **404**, selon `AnimationHorsTenant`. Le nom des routes et les compteurs d'échecs du vérificateur sont également corrigés. Aucun droit ni contrat produit modifié. | **Corrigés et rejoués** : quatre assertions du garde puis **15 assertions après réouverture** passent, ancienne session refusée, reconnexion, identité, communes et permissions conservées, B1 refusée sans changer le contexte, équipe étrangère refusée et nouvelle session fermée. Rapports antérieurs conservés ; les variantes de rôles sont suivies dans le compte rendu de recette. |
| RM-25-05 — reçu du rejeu QR d'un coffret | Après reprise, le premier scan et la validation d'une prestation restaurée réussissent ; répéter la même confirmation doit retourner le même reçu sans deuxième consommation. Le rejeu renvoie HTTP **500** sur `/protected/exploitation/validation/valider-prestation`. | **Défaut produit reproduit** : `ServiceValidationPrestation._resultat_validation_deja_traitee` omet `coffret_instance_id` et `statut_prestation_coffret_instance_id`, obligatoires dans le schéma de réponse. Correction du producteur depuis l'occurrence persistée, sans rendre les champs optionnels et sans changer les autorisations ou les effets financiers. | **Corrigée localement et rejouée** : quatre reproductions ciblées échouent avant correction et passent après ; 665 tests ciblés et d'architecture passent. Sur le clone, les parcours QR et PIN totalisent **20 contrôles réussis**, dont rejeux renvoyant le même reçu et une seule validation persistée. Rapports initiaux conservés ; revue indépendante favorable. Aucun déploiement sur TEST partagé ; RM-25-05 reste partiel. |
| RM-12 / RM-25-05 — attribution numérique et clés étrangères | Le worker du tirage LIBRE NUMÉRIQUE doit créer ses attributions et bons dans la même transaction. Sur le clone, INDEXATION passe puis CLASSEMENT échoue sur `bons_lots_attribution_id_fkey`. | **Défaut produit reproduit** : l'attribution ORM n'est pas encore insérée quand le bon dépendant est flushé. Le repository flushe désormais le parent avant d'exposer son identifiant aux producteurs de bons/envois, sans commit intermédiaire. La fixture PostgreSQL historique omettait les FK ; les nouvelles reproductions rétablissent les trois contraintes de production. | **Corrigée localement et rejouée** : deux reproductions PostgreSQL échouent avant patch puis passent, avec trois bons, rejeu sans doublon et incident après le deuxième bon suivi d'un rollback intégral/reprise ; 618 contrôles d'architecture passent et revue indépendante favorable. La même opération réelle du clone atteint ensuite **CONFIRMEE**, son email est préparé dans l'outbox sans envoi fournisseur. Aucun correctif déployé sur TEST partagé. |

Les prérequis absents (convention, appareil, campagne publiée, ancienneté réelle,
calendrier, réservation de charge/restauration) sont des **blocages de recette**,
pas des anomalies produit démontrées. La couverture du lanceur reste de 27 parcours
complets et 103 partiels ; un numéro référencé ne prouve pas une réussite TEST.

Bilan avant l'exercice de restauration : **12 réussites complètes et 118
blocages**. Le nouvel échec de reprise RM-25-05 a été corrigé et rejoué sur le
clone isolé, comme décrit ci-dessus ; il ne modifie pas les douze succès
antérieurs. Le [tableau des 130 RM](../../specifications/epic-73-animation-et-ou-coffrets/automatisation-recette.md#état-détaillé-des-130-scénarios)
relie chaque verdict à son rapport privé. Les gardes des nouveaux lots A/B/C et
des neuf derniers scénarios restent actifs : leurs fixtures absentes sont
constatées avant l'action métier. Cela ne constitue pas une validation des
118 comportements bloqués ni l'achèvement de la recette.

Les dernières vérifications locales sont **356 tests Node du harnais sans skip**,
**8 tests Python primaires de publication** et **10 tests PostgreSQL locaux
isolés** réussis. Elles ne remplacent ni conventions et essais sur appareils,
ni paiements/lots/animations réels du jeu, ni anciennetés de sept/trente jours,
ni restauration représentative hébergée avec sauvegarde de configuration et
journal de révocations, ni charge réservée à 10 000 participants avec budgets,
ni avis humains du pilote.

Valeurs de suivi proposées : **À traiter**, **En cours**, **À valider**, **Corrigée**.

### RM-22-01 — liste ERP des animations et lots inaccessible

La lecture normale de `/internal/erp/api/suivi-animations` renvoie 404 sur
le clone. La route générique d'interface `/internal/erp/{page}/{identifiant}`
est enregistrée avant cette API et intercepte sa requête. Les routeurs de suivi
ERP et Support sont désormais enregistrés avant cette interface générique,
sans changement de contrat, de droits, de règles métier ni de migration.

**Corrigée localement, rejeu du clone en attente** : la reproduction utilisant
les routes réelles de `app.main` échoue en ERP avant correction ; le témoin
Support passe. Les deux passent ensuite, ainsi que **622 contrôles**
d'architecture, domaine, application et API de suivi. Les premiers essais
de montage du test échouaient dans leur préparation et ne constituent pas
la reproduction produit. Test : `tests/api/test_suivi_produits_application_routing.py`.
Aucun déploiement sur TEST partagé ; RM-22-01 reste partiel.

### RM-25-01/02 — accès nominatif aux périmètres commerçants

Sur le clone isolé, deux opérateurs fictifs BACKOFFICE créés par les commandes
normales, avec le droit dédié `commercants:perimetres_gerer`, se connectent par
les formulaires réels. La lecture des périmètres renvoie pourtant **403**,
« Interface réservée à l'administrateur historique » ; corrélation
`LOC-8845c8b6-fef1-4171-83c5-8cbfe51f0d78`.

Les six fonctions de `perimetres_commercants_api` manquent au catalogue fermé
et leur surface n'est pas reconnue par le middleware. Le correctif classe les
trois lectures sous `metier.consulter`, les trois commandes sous le droit dédié,
et reconnaît uniquement une route installée de ce module avec sa capacité
déclarée. Les contrôles de commune, CSRF, version et métier restent portés par
les gardes et services existants ; aucune permission technique n'est ajoutée.

**Corrigée localement et parcours principal rejoué sur le clone** : avant correction, les
régressions isolées reproduisent douze échecs et quatre refus attendus réussis.
Après correction, **87 tests d'accès ERP**, dont les dix-huit contrôles ciblés
des périmètres, et **618 contrôles architecture/domaine/application** passent.
La suite élargie compte 144 succès et deux échecs d'audit de création d'offres
préexistants, reproduits aussi en neutralisant en mémoire les seuls ajouts de
ce correctif ; aucune assertion affaiblie. JUnit privés
`correctif-perimetres-apres-tests.xml` et
`baseline-audit-sans-correctif-perimetres.xml`.
Le rapport privé
`revue-bascule-deux-operateurs-ui-rapport.json` présente désormais vingt contrôles
principaux réussis : deux opérateurs nominatifs distincts, formulaires de revue,
auteurs et motifs, refus de bascule incomplète et conservation des engagements.
L'échec navigateur/API initial après neuf contrôles reste archivé. Aucun
déploiement sur TEST partagé ni succès complet de ces deux scénarios n'est
revendiqué : jonction des jeux et variantes restantes demeurent partielles.

Ce correctif d'adaptateur ne change ni contrat API, règle de domaine, migration,
générateur ni droits accordés aux comptes ; les frontières de session et les
gardes métier existantes restent vérifiées par les tests ciblés.

### RM-22-01 — état et date d'un bon numérique confirmé dans le suivi ERP

Le parcours principal du suivi doit présenter le même état que la remise
normale. Sur le clone isolé, le bon `7e14143c…`, consommé normalement, est
présenté **NON_ATTRIBUE** par le suivi alors que `BonsLotsRepository` et le
domaine `BonLot` donnent **CONSOMME**. Le diagnostic initial en transaction de
lecture seule est conservé dans `diagnostic-suivi-principal-avant-correctif.json`.

Le bon est préparé avant le scellement avec `attributed_at = NULL` ; sa date
effective vient du marqueur `TirageLibre.confirmed_at`. La projection du suivi
lit seulement la colonne du bon et omet les conditions de visibilité du lecteur
canonique. Le suivi réutilise désormais cette requête dans une sous-requête
bornée, puis laisse `BonLot` calculer état et expiration. La date projetée est
la date effective du bon, ou celle de confirmation si elle est absente ; une
date propre au bon reste prioritaire. Avant confirmation, le suivi ne présente
ni identifiant du bon ni date d'attribution. Les transitions, droits et contrats
restent inchangés et la lecture d'une page conserve deux requêtes SQL.

**Corrigée localement et rejouée sur le clone isolé** : deux régressions
reproduisent l'état erroné avant correction, puis deux assertions distinctes
reproduisent la date prématurée ou incorrecte avant son correctif. Les
**10 tests PostgreSQL finaux** et **620 contrôles d'architecture, domaine,
application et API** passent. La fixture historique référence désormais la
même opération confirmée pour le bon et son attribution ; les nouveaux tests
utilisent les commandes normales de préparation, confirmation et consommation.
Le diagnostic après correction donne **CONSOMME** dans le domaine comme dans
le suivi ; le navigateur vérifie ce même bon dans ERP et Support.

Preuves privées : `diagnostic-suivi-principal-lecture-seule.json` après correction,
`suivi-lots-ui-clone-rapport.json` pour les **14 contrôles UI réussis**,
dont les trois natures de dotation, la recherche par nom, la fiche et ses
identifiants, deux pages filtrées LIBRE/commune et les CSV correspondant
exactement à la seconde page dans ERP et Support. Aucun déploiement de ce
correctif sur TEST partagé. **RM-22-01 reste principal partiel et n'est pas barré** :
la comparaison complète entre applications et profils territoriaux reste à vérifier.

### RM-22-01 — projection historique du filtre de recherche

Le défaut distinct du filtre de nom est un prérequis de maintenance : le champ
`nom_recherche` historique est NULL. Le normaliseur, ses producteurs ordinaires
et la reprise bornée `scripts/maintenance/reprendre_recherche_animations.py`
existent ; aucune réécriture de nom ou de statut métier n'est nécessaire.

**Prérequis repris et rejoué sur le clone isolé**, sans nouveau correctif de
recherche : la maintenance canonique a normalisé **13 lignes NULL**, avec
contrôle des champs métier inchangés. L'animation auparavant présente sans
recherche mais absente du filtre est ensuite retrouvée par la recherche normale
et par le navigateur. Preuves privées : `reprise-index-recherche-clone-preuve.json`,
diagnostics avant/après et `suivi-lots-ui-clone-rapport.json`. Cette maintenance
n'a pas été appliquée à TEST partagé et ne clôture pas RM-22-01 ; les limites de
comparaison entre applications et profils territoriaux demeurent.

### RM-10-02/03 — suivi externe : non-remise et intervention Localeo

**Non-remise corrigée sur le clone ; intervention Localeo en écriture restante.** La [recette RM-10-02](../../specifications/epic-73-animation-et-ou-coffrets/recette-metier.md#rm-10-02), étape 5, exige de distinguer une non-remise explicitement déclarée d’un état « Non renseigné ». Le [contrat de dotation](../../specifications/epic-73-animation-et-ou-coffrets/dotation-lots.md) reprend cette distinction dans « Contact/remise externe ». Lors du diagnostic initial, projection et contrats API/Live ne proposaient que NON_RENSEIGNEE et REMISE_DECLAREE ; un refus explicite existant restait affiché comme inconnu. Une correction de remise seule ne prouve pas une non-remise.

La [recette RM-10-03](../../specifications/epic-73-animation-et-ou-coffrets/recette-metier.md#rm-10-03), étapes 1 et 5 et résultat attendu, exige aussi une intervention attribuée à un acteur Localeo habilité. La seule commande de suivi identifiée est la route organisateur protégée `POST /protected/animation-locale/animations/{id}/gains-libres/{gain_id}/suivi-externe` ; les entrées ERP/Support de suivi sont en lecture seule. Aucune entrée normale Localeo en écriture n’a permis d’exécuter cette étape. Aucun profil, scope ou chemin ERP n’a été créé pour contourner cette absence.

Correction du 24 octobre : `AttributionLotLibre.statut_remise_externe` distingue la remise active, le refus explicite existant (`NON_REMIS`), puis l'absence de déclaration. Aucun événement supplémentaire ni réinterprétation des contacts/incidents/corrections. Le repository lit cette propriété, les deux contrats externes API/Live admettent le nouvel état ; Animation et Live l'affichent distinctement. Les contrats OpenAPI canoniques et consommés, le schéma Live et son manifeste sont synchronisés sur cet ajout uniquement. Aucun effet sur les états des bons numériques, les permissions ou les règles de remplacement.

Preuves : reproduction PostgreSQL rouge (`NON_RENSEIGNEE` au lieu de `NON_REMIS`) et refus réel en UI avant correction. Puis 45 tests domaine/PostgreSQL, 618 contrôles d'architecture et couverture, neuf tests Animation de contrat/helper, sept tests Marketplace de helper/manifeste, 30 contrôles navigateur Animation à 1280/320 px et cinq scénarios navigateur Marketplace réussis. Build isolé, TypeScript et lint Animation, lint Marketplace ciblé réussis. Le même refus du clone est relu après installation à 1280/320 px : `NON_REMIS`, un seul événement et même version. Revue indépendante sans défaut bloquant. Preuves privées `non-remis-principal-clone-prive.json`, préparation et installation des seuls modules dans `non-remis-preparation-candidat-20261024` et des consommateurs dans `non-remis-frontends-candidat-20261024`.

Sans migration ni réparation : les refus sont déjà persistés et leur état se projette à la lecture ; aucun historique n'est réécrit. Le générateur conserve ses faits existants et utilise la projection partagée ; une génération complète supplémentaire n'a pas été exécutée pour ce correctif. L'entrée Localeo en écriture et ses capacités restent à traiter séparément ; aucun rôle n'a été créé pour contourner cette limite. Le code n'est pas déclaré déployé sur TEST partagé.

Complément de rejeu : le lien personnel conservé lors de l'inscription réelle du même gagnant permet douze contrôles Live sur les deux origines du clone et à 1280/320 px. API et interface affichent `NON_REMIS` avec le refus expliqué, sans action QR/PIN/Coffret dans la section du gain. Aucun POST transmis ; l'initialisation technique d'installation éventuellement tentée est bloquée par le harnais et n'est pas présentée comme une absence de tentative. Les 98 contrats moteur embarqués sont conformes au générateur. Index privé figé `non-remis-correctif-preuves-20261024/index.json` ; preuve Live `non-remis-live-principal-clone-preuves-figees.json`.

Preuves privées initiales conservées : `externe-remise-clone-preuves-figees.json` (SHA-256 `bf7535bcc088b258624dccf4610cc1cadb5f2cad00c0bcbd1f47186c6e42bec4`) et couverture par étape dans `externe-remise-clone-couverture.json`. Le parcours gestionnaire et les refus commerçant/salarié sont vérifiés ; le correctif distinct d’affichage de l’auteur est décrit dans [les anomalies Animation](animation.md). RM-10-02/03 restent partiels ; la réception email externe demeure une limite d’exécution séparée.

### RM-22-02 — fournisseur Animation seul proposé pour une prestation Coffrets

**Reproduite le 24 octobre et corrigée sur le clone isolé le 29 octobre 2026.**
Dans la composition d’un Coffret brouillon, la recherche trouve le commerce
Animation seul et active « Créer une prestation ». La commande normale visant
ce fournisseur est pourtant refusée 403 `PERIMETRE_NON_OUVERT` ; version et
prestations du Coffret restent inchangées. La protection métier fonctionne,
mais la projection de recherche ne fournit pas son résultat à l’interface.

L’ouverture Coffrets reste calculée par `produit_ouvert` dans le domaine et
lue par le repository partagé ; l’ERP doit présenter ce résultat sans déduire
une habilitation des seuls états affichés, notamment pour préserver le mode
historique. Preuves privées : `finances-dotation-principal-clone-prive.json`
et `finances-dotation-principal-fournisseur-avant.png`. Le test navigateur
`atelier-fournisseurs-perimetres.cjs` reproduit le bouton actif avant correction.

La recherche ERP expose maintenant `coffretsOuvert`, calculé par la lecture
groupée du repository et la règle de domaine existante. La composition filtre
les nouveaux fournisseurs et conserve ce filtre après une nouvelle recherche,
y compris avec un formulaire modifié. Les prestations existantes gardent leur
fournisseur verrouillé. Les diagnostics de rattachement classique et assisté
reçoivent aussi ce fait ; leurs admissions, versions et contrôles restent actifs.

Rejeu réel du 29 octobre : huit contrôles, commerce Animation seul refusé dans
l’interface à 320/1280 px, fournisseur historique toujours proposé, nouvelle
tentative serveur refusée 403 sans prestation ni changement de version.
Preuve `fournisseurs-correctif-rejeu-prive.json`. Les 28 contrôles navigateur ERP
passent. Trois régressions PostgreSQL ont été reproduites avant correction puis
vérifiées après ; le lot complémentaire intégration/application compte 25 succès.
L’ancienne fixture SQLite a reçu les trois tables de périmètres manquantes,
sans modification d’assertions ; son erreur initiale reste conservée.
La revalidation application du 29 octobre compte 37 succès avec les tests d’Audit.
Lecture groupée et frontières de commune revues indépendamment. Sans migration,
nouveau droit ou changement de paiement ; contrat ERP enrichi d’un booléen de
lecture, consommé par son interface. Aucun déploiement sur TEST partagé.

### RM-14-02 — auteur de gestion d’un bon présenté comme commerçant

**Reproduite le 24 octobre et corrigée sur le clone isolé le 29 octobre 2026.** Les prolongations
effectuées normalement par le gestionnaire apparaissent dans l’Audit avec
l’auteur « Commercant ». Le champ `commercant_id` de l’événement désigne le
commerce de remise du bon ; il ne prouve pas l’identité de l’auteur.
`ServiceAuditAnimation` l’utilisait pourtant pour choisir ce libellé.

Les cinq commandes de gestion de bon doivent conserver l’auteur gestionnaire
enregistré ; les consommations par principal, salarié ou PIN restent
commerçantes. Un auteur absent ou non identifié ne doit pas recevoir de rôle
inventé. Les tests de reproduction donnent huit échecs et sept succès avant
correction ; preuve privée `audit-auteur-reproduction.xml` et relecture des
trois événements de `prolongations-principales-clone-completude-scellee.json`.

La projection utilise maintenant l’auteur enregistré et le contexte fermé des
commandes de gestion/consommation. Elle ne relit pas les droits actuels pour
réécrire l’histoire et n’expose aucun identifiant ou secret. Les auteurs absents
restent non identifiés. Le rejeu relit les mêmes trois prolongations : auteur
Gestionnaire dans l’API et l’interface ; les deux consommations conservent
Commercant. Échéance, version et quatre autres bons strictement inchangés ;
aucune prolongation rejouée. Preuve
`prolongations-principales-clone-auteur-apres-correctif-prive.json`.
Les 633 contrôles Audit/architecture/domaine/couverture passent le 29 octobre.
Sans migration, modification d’événement, permission, schéma ou consommateur.
