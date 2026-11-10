# Localeo Live — retours de parcours et stabilité visuelle

Audit et correctifs du **10 novembre 2026**, à partir des retours habitant :
Mon carnet → participation renvoie vers Mes participations, « Messages » dépasse
de la cloche et plusieurs éléments se déplacent pendant le chargement.

## Périmètre et méthode

Analyse de `localeo-marketplace` sur la base `2a90fb0` avec les corrections locales
de ce rapport. Reproduction dans Chromium sur le build isolé, avec des accès
synthétiques distincts et des réponses API simulées, retardées ou refusées.
Contrôle visuel à 320, 360 et 390 pixels, avec libellés d’outils agrandis à 200 %.
La version distante TEST et son SHA ne sont pas attestés par cette recette.
Aucune donnée réelle, inscription, remise de lot ou validation de visite utilisée.

Cette passe complète l’[audit mobile du 9 novembre](localeo-live-carnet-bord-audit-mobile-2026-11-09.md)
et vérifie les attentes existantes E73-CN-02, CB04/07, LH-03/12 et FD-10 de la
[spécification E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md).
Les [principes UX](../../produit/live/principes-ux.md) gardent le carnet comme point
de repère et distinguent la simple consultation d’une nouvelle réussite.

## Constats et corrections

| Priorité | Cause reproduite ou vérifiée dans les sources | Correction |
| --- | --- | --- |
| P1 — Retour personnel | Les liens du carnet ne transmettaient pas leur origine. Le détail utilisait un libellé fixe et revenait réellement à `/live/animations`. La même rupture existait pour les coffrets, lots et favoris. | Contexte de retour commun : destination, libellé, filtre et repère de reprise. « Retour à mon carnet » rejoint le carnet ; l’ancienne liste reste la destination de ses propres ouvertures. |
| P1 — Détours | Les étapes participation → commerce, messages → participation et fiche → participation perdaient une partie de la chaîne. | Conserver l’étape précédente dans une chaîne bornée de métadonnées de navigation. La fermeture des messages revient à son origine ; un message ouvrant une participation propose le retour aux messages. |
| P1 — Bouton Messages | Une règle mobile de `live-carnet.css` imposait 44 px à tout bouton du bandeau. Le texte débordait dès la taille normale. Des sélecteurs de badge visaient également tous les `span` de la cloche. | Retirer la contrainte du bouton avec libellé, dimensionner selon son contenu et cibler uniquement le badge. Icône et texte restent dans la zone tactile, y compris à 200 %. |
| P1 — Filtrage du carnet | La clé du composant de gestion d’erreur dépendait de la route et de la recherche. Changer un filtre détruisait tout Live, perdait le focus et relançait les lectures. | Garder le shell monté ; réinitialiser seulement une erreur lors d’un changement de route. Un filtre local conserve ses données et le focus, sans nouvelle requête. |
| P1 — Premier chargement | Après IndexedDB, les cartes locales et tous les filtres apparaissaient avant les résumés ; la prochaine action s’insérait ensuite et les cartes changeaient de hauteur. | Ossature non interactive et une annonce de chargement, puis composition de la première lecture. En panne, afficher les accès locaux avec un état explicitement partiel. |
| P2 — Actualisation | L’état « ancien » et des filtres supplémentaires étaient ajoutés dès le départ du rafraîchissement, déplaçant les actions. | Conserver la composition pendant la relecture et appliquer les résultats ensemble. Un refus confirmé retire immédiatement les projections privées concernées. |
| P2 — Entrée et mouvements | Le chargement différé de Live utilisait le squelette des coffrets Marketplace. Plusieurs vues passives rejouaient une translation d’entrée. | Ossature propre à Live dès l’attente du module ; suppression des translations des listes et en-têtes passifs. Les effets de réussite confirmée restent distincts. |
| P2 — Lecture d’un objet | Une participation ciblée attendait la résolution de toutes les participations locales, puis était relue. La liste pouvait apparaître avant le détail. | Lire l’accès exact sans attendre les autres objets et garder le retour du détail visible pendant son chargement et en cas d’erreur. |

La revue de la conservation du shell a également couvert ses conséquences :
les écrans d’objets sont réinitialisés au changement de chemin pour ne pas
transporter un QR ou une saisie vers un autre objet ; les panneaux du shell
se ferment lors d’une navigation. Les messages sont invalidés après changement
des accès et retirés après refus d’une lecture, d’une pagination ou d’un accusé
de lecture. Un échec du stockage local après actualisation indique explicitement
« Dernier état connu » et retire la proposition de prochaine action.
La vue des participations relit également ses accès après ajout, remplacement
ou retrait sur l’appareil ; une réponse ancienne ne peut pas rétablir l’accès
précédent. Le détour découverte → fiche → participation → fiche → découverte
conserve les métadonnées publiques de filtres, pagination, position et focus.

Les URL de retour sont limitées aux routes et paramètres internes prévus.
Les tokens, fragments et projections personnelles ne sont pas recopiés dans ce
contexte. Un accès direct sans origine conserve un retour utilisable. Aucun
retour ne sélectionne une autre participation à la même animation.

## Preuves locales

Les tests de reproduction échouaient sur la cloche aux trois largeurs, la
requête supplémentaire après changement de filtre et l’absence d’annonce
pendant la lecture initiale différée. Les tests corrigés vérifient :

- `live-loading-stability.spec.cjs` : module lent, première lecture lente ou
  en erreur, géométrie des cartes pendant actualisation, filtre local, messages
  invalidés après changement des accès ou refus, stockage indisponible,
  fermeture des panneaux à la navigation, changement de coffret et dimensions des outils ;
- `live-return-continuity.spec.cjs` : participation/carnet, lot/carnet,
  détours commerces et messages, favori/fiche/participation, erreurs et accès exact ;
- `live-return-navigation.test.cjs` : routes autorisées, absence de secrets et
  profondeur bornée du contexte, métadonnées publiques de découverte ;
- `live-return-access-refresh.spec.cjs` : ajout, remplacement, retrait et nouvelle
  tentative après un accès absent, avec réponse retardée de l’ancien accès ;
- les suites existantes carnet, lots, messages, découverte et retours complètent
  la vérification des comportements adjacents.

Trois échecs de `live-context-return.spec.cjs` ont été reproduits sur le commit
initial `2a90fb0`, dans un checkout isolé : mock ignorant les paramètres de la
requête de détail, cinquième carte déjà visible sur ordinateur et sélecteur de
vedette retiré. Les fixtures utilisent désormais le chemin exact de l’API, une
liste assez longue pour tester un vrai défilement et les liens des cartes
actuelles à la souris comme au clavier. Les exigences de position et de focus
sont conservées ; le sélecteur communal est ouvert avant de tester ses options.
Les attentes de `live-lots-navigation.spec.cjs` ont aussi été alignées sur les
trois rubriques déjà en place : Mon carnet, Mes lots et Découvrir.

Résultats finaux :

- **43 scénarios sur le dernier build** : les six suites `live-loading-stability`,
  `live-return-continuity`, `live-context-return`, `live-lots-navigation`,
  `live-return-access-refresh` et `live-participations-navigation` ont été lancées
  avec `node node_modules/@playwright/test/cli.js test --config=playwright.desktop.config.cjs`,
  deux workers isolés et un délai maximal de 30 secondes. 42 succès dans le
  lancement commun ; le dernier scénario avait une fixture sans capacité de
  recherche par type. Après ajout de cette capacité et de sa réponse simulée,
  il réussit seul sur le même build (**1/1**), sans changement du code applicatif.
- **58 scénarios adjacents réussis** dans les suites carnet, audit mobile,
  messages et fluidité, lors du contrôle élargi. Aucun skip ajouté ; les échecs
  des parcours concernés ont été corrigés et repris dans les 43 scénarios ci-dessus.
- `npm run test:security` : **235/235** ; après le dernier complément du helper,
  `node --test tests/security/live-return-navigation.test.cjs` : **4/4**.
- ESLint sur `src` et les tests modifiés : **succès** ; `git diff --check` :
  **succès**. La commande globale `npm run lint` rencontre un `EPERM` en parcourant
  des sorties de travail protégées sous `output/` puis `tmp/` ; ces répertoires
  n’ont pas été supprimés et leurs permissions n’ont pas été modifiées.
- `python scripts/check_guidance.py` : **97 guides, 1 169 liens, aucun écart** ;
  `python scripts/sync_documentation.py --check-sources` : **148 documents vérifiés**.

Les captures de travail restent dans `localeo-marketplace/tmp/live-ux-verified/`
et `tmp/live-ux-final/`, hors versionnement ; la reprise du détour filtré est dans
`tmp/live-ux-context-detour/`. L’examen visuel confirme le libellé
Messages contenu dans le bouton, le carnet en attente et le carnet chargé.
La recette n’est pas une mesure de performance sur téléphone physique ou réseau
mobile réel. Le délai réseau lui-même n’est pas supprimé.

## Impacts et livraison

- **Applications** : présentation, navigation et cycle de vie dans Marketplace/Live.
  Backend, Commerçant et Animation ne changent pas.
- **Domaine et API** : aucun contrat ni calcul métier modifié. Les états et QR
  restent confirmés par leurs lectures autorisées ; aucune nouvelle commande.
- **Données, migrations et démonstration** : sans objet, les accès existants restent
  dans leur stockage et les preuves utilisent des fixtures isolées.
- **Documentation** : présent audit, suivi d’anomalie et principes UX transverses ;
  aucune nouvelle epic ni modification du statut de clôture.
- **Exploitation** : aucun flag ni procédure de reprise de données. Livraison
  du frontend nécessaire ; recette distante à faire après cette livraison.

Ce rapport décrit des corrections locales, pas un déploiement sur TEST.
