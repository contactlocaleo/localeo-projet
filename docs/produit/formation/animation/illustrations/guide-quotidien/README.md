# Captures du guide utilisateur Animation

## Parcours organisateur du 25 novembre 2026

Les images du pilotage des priorités, de la publication, du suivi, de la revue de clôture mobile et du tirage illustrent les gestes 2, 11, 14, 17 et 18. Elles proviennent du portail sur la base `658836e` avec les modifications locales E85 et des données fictives. Les captures utilisent le build de test isolé, les scénarios `tests/browser/dashboard-pilotage-guide.mjs` et `tests/browser/animation-guide.mjs --only=publication,cloture,tirage,suivi --captures-only`. La capture pleine largeur de Participants provient du scénario Participants de `tests/browser/animation-workspace-ux.mjs`, à 1600 px. Les tests vérifient les lectures simulées et l’absence d’écriture.

## Points d’attention de l’Assistant du 25 novembre 2026

`assistant-1024.png` et `assistant-390.png` montrent un règlement manquant et
un avertissement sur la présentation, ainsi que les liens vers leurs rubriques.
La capture de bureau figure dans le geste **Vérifier puis publier**.
Elle provient de l’interface Animation sur la base `3189f02`, avec cette
évolution et des réponses API fictives.

Depuis `localeo-animation`, générer la capture et vérifier les destinations
au clavier et au clic sur un serveur local à port éphémère.

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/assistant-attention-guide-dist'
$env:ANIMATION_GUIDE_CAPTURE_ROOT = 'tmp/assistant-attention-captures'
node scripts/build-generation-tests.mjs
node tests/browser/animation-guide.mjs --only=assistant --captures-only
```

## Choix des commerces pendant la création du 25 novembre 2026

`selection-reseau-creation.png` illustre le geste **Choisir les commerces à
solliciter**. La case de restriction à la commune est décochée. Les noms de
commune sous les établissements permettent de repérer un adhérent extérieur.
La capture utilise l’écran de création de Localeo Animation sur la base
`3189f02`, avec le filtre du réseau et des commerces fictifs.

Depuis `localeo-animation`, la recette utilise un build isolé, des réponses
API simulées et un serveur HTTP local sur port éphémère.

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/selection-reseau-guide-dist'
$env:ANIMATION_BROWSER_ARTIFACTS = 'tmp/selection-reseau-guide-captures'
node scripts/build-generation-tests.mjs
node tests/browser/po-creation-continuite.mjs
```

Le scénario `merchant-network` produit `network-guide-1280.png` dans le
répertoire des captures. Ce cadrage du formulaire à 1 280 px est repris
sous le nom `selection-reseau-creation.png`.

## Pagination du réseau de commerçants du 25 novembre 2026

`commercants-1280.png` montre la deuxième page d’un réseau fictif de
27 commerces. La capture provient du parcours **Commerçants** sur la base
`6236a43` avec la pagination enrichie. La recette ouvre la deuxième page
depuis la première et contrôle le compteur à 1 280 et 390 px.

Depuis `localeo-animation` :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/merchant-pagination-build'
$env:ANIMATION_GUIDE_CAPTURE_ROOT = 'tmp/merchant-pagination-guide-captures'
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --only=commercants --captures-only
```

## Lancement du traitement d’un import du 25 novembre 2026

`import-traitement-1024.png` montre un lot fictif confirmé, ses compteurs et
le bouton **Lancer le traitement**. La capture est issue de l’application
Animation sur la base `e35e1ba` complétée par l’action de lancement. La recette
exécute le même contrôle dans Chromium à 390 px et 1 024 px.

Depuis `localeo-animation` :

```powershell
$env:ANIMATION_TEST_SUPPORT = 'true'
$env:ANIMATION_TEST_DIST = 'tmp/import-traitement-guide-build'
$env:ANIMATION_GUIDE_CAPTURE_ROOT = 'tmp/import-traitement-guide-captures'
$env:ANIMATION_GUIDE_ARTIFACTS = 'tmp/import-traitement-guide-capture-report'
node scripts/build-generation-tests.mjs
node tests/browser/animation-guide.mjs --only=import-traitement --captures-only
```

Copier la capture à 1 024 px dans ce dossier, puis suivre la
[procédure commune](../../../../../organisation/maintenance-guides-utilisateurs.md)
pour régénérer et synchroniser le PDF. Après reconstruction du build local,
le scénario `node tests/browser/animation-guide.mjs --access-only` vérifie le
lien du guide et les octets servis à 390 et 1 024 px.

Les captures E84 du 24 novembre 2026 montrent la liste **Commerçants** dans
son rendu du 24 novembre (`commercants-1024.png`) et un import fictif dont
les lignes portent sur Valmont et Beaulieu.

## Import des commerçants du 24 novembre 2026

`import-colonnes-1024.png` montre la reconnaissance du séparateur et les cinq
champs obligatoires. `import-apercu-1024.png` montre les résultats de deux
lignes, dont une catégorie à résoudre. Les captures proviennent de
l’application Animation sur la base `15d3bab` avec la mise à jour de l’import,
dans Chromium et avec des données fictives. La même recette contrôle le rendu
à 390 px et la lecture des exemples sans commande d’écriture.

Depuis `localeo-animation` :

```powershell
$env:ANIMATION_TEST_SUPPORT = 'true'
$env:ANIMATION_TEST_DIST = 'tmp/import-guide-build'
$env:ANIMATION_GUIDE_CAPTURE_ROOT = 'tmp/import-guide-captures'
$env:ANIMATION_GUIDE_ARTIFACTS = 'tmp/import-guide-report'
node scripts/build-generation-tests.mjs
node tests/browser/animation-guide.mjs --only=import-colonnes,import-apercu --captures-only
```

Copier les captures à 1024 px dans ce dossier, régénérer le PDF et vérifier
la copie embarquée selon la [procédure commune](../../../../../organisation/maintenance-guides-utilisateurs.md).

Les 20 pages rendues dans `tmp/import-guide-pdf-final` ont été relues. Après
synchronisation, refaire le build et relancer le scénario sans
`--captures-only` pour vérifier les liens au clavier et les octets du PDF
servi, y compris quand l’assistance est indisponible. Les rapports de la
passe finale à 390 et 1024 px sont dans `tmp/import-guide-final-report`.

## Historique des interventions du 24 novembre 2026

Les captures `interventions-1024.png` et `interventions-390.png` montrent la modification d’une animation en brouillon et le suivi d’un import de vingt lignes. Elles utilisent Chromium, des données fictives et la révision Animation `77e2db2` avec l’évolution E76.

```powershell
$env:ANIMATION_TEST_SUPPORT='true'
$env:ANIMATION_TEST_DIST='tmp/e76-animation-history-guide/dist'
$env:ANIMATION_GUIDE_ARTIFACTS='tmp/e76-animation-history-guide/capture-report'
$env:ANIMATION_GUIDE_CAPTURE_ROOT='tmp/e76-animation-history-guide/captures'
node scripts/build-generation-tests.mjs
node tests/browser/animation-guide.mjs --only=interventions --captures-only
```

Copier les deux captures dans le dossier d’illustrations. Régénérer et vérifier le guide Animation selon la [procédure commune](../../../../../organisation/maintenance-guides-utilisateurs.md).

## Historique des interventions du 23 novembre 2026

Captures Chromium de la rubrique **Interventions de Localeo** avec des données fictives sur la base Git `4852017` et les modifications E76. Les vues de 1024 et 390 pixels montrent le suivi du lot de vingt lignes.

```powershell
$env:ANIMATION_TEST_SUPPORT='true'
$env:ANIMATION_TEST_DIST='tmp/e76-guide/dist'
$env:ANIMATION_GUIDE_ARTIFACTS='tmp/e76-guide/recette'
node scripts/build-generation-tests.mjs
node tests/browser/animation-guide.mjs --only=interventions --captures-only
```

## 23 novembre 2026 - sélecteur de période du tableau de bord

`pilotage-indicateurs-1024.png` et `pilotage-indicateurs-390.png` montrent le
sélecteur de période et les indicateurs avec des données fictives. Depuis
Animation, sur la base `e3957eb` complétée par la retouche du tableau de bord :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/pilotage-text-20261123-build'
$env:ANIMATION_GUIDE_CAPTURE_ROOT = 'tmp/pilotage-text-guide-captures'
New-Item -ItemType Directory -Force $env:ANIMATION_GUIDE_CAPTURE_ROOT | Out-Null
node scripts/build-pwa-tests.mjs
node tests/browser/dashboard-pilotage-guide.mjs
```

Copier les deux captures `pilotage-indicateurs` depuis le dossier de sortie.

## Palette bleu nuit et orange du 22 novembre 2026

Les illustrations de cette édition reprennent le fond papier, les actions bleues,
la navigation pêche et les pictogrammes métier à accent orange de Pro et Animation.
Les parcours et les états métier sont conservés. Les captures montrent la vraie
application avec des données fictives et des API synthétiques, sans accès externe.

Build : `localeo-animation/tmp/charte-animation-20261122`. Captures générales :
`tmp/charte-animation-guide-20261122` ; Pilotage :
`tmp/charte-animation-pilotage-guideA4bB56` ; Juste Prix :
`tmp/juste-prix-products-2E0an8` ; préparation mobile :
`tmp/charte-animation-hunt-guide` ; maximum d'essais :
`tmp/attempts-guides-captures-4pJnQ0` ; seuil : `tmp/threshold-report-1IwSvs`.
Le cadrage du seuil est une capture seule, sans exécution de commandes métier.
Le banc des essais passe par le sélecteur réel « Règles » sur téléphone avant de
capturer le champ, afin de respecter la navigation mobile existante.

Commandes depuis Animation : `node scripts/build-pwa-tests.mjs`,
`node tests/browser/animation-guide.mjs --captures-only`,
`node tests/browser/dashboard-pilotage-guide.mjs`,
`node tests/browser/juste-prix-products.mjs --guide-captures`,
`node tests/browser/wrong-answer-guide.mjs` et le mode
`HUNT_GUIDE_CAPTURE_ONLY=1` de `hunt-guided-workflow.mjs`.
La génération PDF utilise `py -3.14 scripts/generate-animation-guide.py
--preview-dir tmp/charte-animation-guide-pdf`, puis `npm run guide:sync` et
`npm run guide:check`. Cette passe locale ne constitue pas un déploiement.

Les seize pages ont été rendues dans `tmp/charte-animation-guide-pdf` et relues
sur deux planches intégrales, avec la page 11 inspectée à sa taille de rendu.
Le PDF canonique et sa copie embarquée partagent l'empreinte SHA-256
`e8d25ff6de5cec507f2b65004360287793586373023fb67774006893410c329d`.
Après reconstruction du même build, `animation-guide.mjs --access-only` a
vérifié l'accès clavier, l'ouverture du guide, le type PDF et les octets servis
à 390 et 1024 px, y compris quand l'assistance est indisponible. Les rapports
`tmp/charte-animation-guide-access-final/requests-390.json` et
`requests-1024.json` ne contiennent aucune requête inconnue, erreur navigateur
ou écriture.

La recette du cadre (`WORKSPACE_CASE=shell node
tests/browser/animation-workspace-ux.mjs`) a réussi dix parcours dans
`tmp/charte-animation-shell-complete/report.json` : 320, 390, 768, 1024, 1280
et 1600 px, paysage 844 px, texte à 200 % sur 320, 1280 et 844 px.
Navigation, clavier, notifications, compte et protection des saisies sont
vérifiés sans mutation API. Les attentes de l'ancienne couleur du bandeau ont
été remplacées par le bleu nuit ; les attentes de visibilité après navigation
attendent le rendu React et la fixture de lecture de l'équipe est explicite.

## Iconographie de gestion du 22 novembre 2026

Les captures de Pilotage, Commerçants, Préparation, Configuration, Publication,
Communication, Suivi, Juste Prix, Bilan et Aide ont été refaites dans le frontend
React, base `08aef5a` avec les évolutions locales. L’extrait du tableau **Lots et
remises** a lui aussi été reproduit et reste identique. Les deux captures
recadrées sur les champs de seuil et de nombre d’essais gardent leurs repères.
Les textes et les seize chapitres de l’édition Pilotage sont repris.

Depuis `localeo-animation`, avec les API synthétiques et Chromium :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/management-icon-final-build'
$env:ANIMATION_GUIDE_CAPTURE_ROOT = 'tmp/management-icon-guide-png'
node scripts/build-pwa-tests.mjs
node tests/browser/dashboard-pilotage-guide.mjs
node tests/browser/juste-prix-products.mjs --guide-captures
node tests/browser/animation-guide.mjs --captures-only --only=commercants,preparation,configuration,publication,communication,suivi,lots-remises,bilan,aide
node tests/browser/animation-guide.mjs --captures-only --only=publication,aide
py -3.14 scripts/generate-animation-guide.py --preview-dir tmp/management-icon-guide-pdf
npm run guide:sync
npm run guide:check
```

Les captures bureau du guide sont produites à 1024 px. La recette groupée
s’arrête sur Dotation à 390 px. Les captures mobiles de Publication et Aide
sont produites par la relance ciblée. Les rapports de ces deux exécutions sont
dans `tmp/management-icon-guide-report-final` et
`tmp/management-icon-guide-access-captures`. Les vues mobiles et bureau de
Pilotage et Juste Prix proviennent de leurs propres recettes synthétiques.

Les seize pages du PDF ont été rendues et relues. Le nouveau build
`tmp/management-icon-guide-final-build` inclut le PDF synchronisé. La recette
`node tests/browser/dashboard-pilotage-guide.mjs --access-only` a vérifié
les liens, le clavier et le PDF effectivement servi à 390 et 1024 px, y compris
quand l’assistance est indisponible. Le rapport est
`tmp/dashboard-pilotage-guides-captures-UGpOIw/provenance.json`.

## Évolution du 22 novembre 2026 - pilotage unifié des animations

Les captures `pilotage-indicateurs-1024.png`, `pilotage-resultats-1024.png` et
`pilotage-priorites-1024.png`, avec leurs variantes `390`, remplacent les vues
du tableau de bord dans les trois premiers chapitres. Elles montrent la vraie
interface React avec une commune et des chiffres fictifs, sans donnée privée.

Le guide distingue choix de période et indicateurs, résultats par animation et
export CSV, puis priorités et rappels personnels. Cette édition comporte
**seize chapitres**, avec une page par chapitre afin de conserver la lisibilité.
Les captures historiques ci-dessous restent conservées comme archives de leur
édition ; elles ne décrivent pas le tableau de bord courant.

Depuis `localeo-animation`, avec Chromium et les dépendances du générateur :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/dashboard-pilotage-guides-build'
node scripts/build-pwa-tests.mjs
node tests/browser/dashboard-pilotage-guide.mjs
py -3.14 scripts/generate-animation-guide.py --preview-dir tmp/dashboard-pilotage-guides-pdf
npm run guide:sync
npm run guide:check
node scripts/build-pwa-tests.mjs
node tests/browser/dashboard-pilotage-guide.mjs --access-only
```

Le premier build et la capture utilisent une API locale simulée vers
`api.test.invalid`, une horloge pédagogique au 22 novembre 2026 à midi UTC et
un port HTTP éphémère. Les fichiers `provenance.json` des rapports
`localeo-animation/tmp/dashboard-pilotage-guides-captures-*` conservent le
chemin exact du build, les largeurs et les requêtes inconnues éventuelles.
Le second build incorpore le PDF final pour vérifier son accès et ses octets.
Ces recettes locales ne prouvent aucun déploiement distant.

Passe intégrée exécutée sur Animation `54efabe`, après reprise des évolutions
de préparation mobile et d'iconographie de `main` (`5acced0`) : captures du
build `tmp/dashboard-pilotage-integrated-build`, rapport
`tmp/pilotage-integrated-guide-captures-3aGLnh`. Les trois zones sont prises
à **1 024 et 390 px**, sans retouche du DOM, erreur navigateur, requête inconnue
ni écriture. Les rappels sont dépliés par une action réelle dans l'interface.
Les **seize pages** du PDF ont été rendues et relues, avec inspection détaillée
des premiers chapitres et de la création mobile. Le build intégré sert
la copie PDF finale synchronisée : HTTP 200, type PDF, contenu identique au canonique, accès
clavier et nouvel onglet vérifiés à 1 024 et 390 px, y compris avec l'assistance
en HTTP 503. Rapport d'accès :
`tmp/pilotage-integrated-guide-access-QbgulY/provenance.json`.

Cette passe utilise les checkouts propres `localeo-animation-pilotage-1795371720466`
et `localeo-projet-pilotage-1795371720466`. La racine documentaire est transmise
au banc par `ANIMATION_GUIDE_PROJECT_ROOT` et au générateur par `--project-root`.
Le PDF est ensuite copié explicitement vers `public/guides` et le dossier
`guides` du build servi, sans reconstruire ni modifier son JavaScript.
Les chapitres et illustrations hors pilotage conservent les évolutions mobiles
et iconographiques déjà livrées dans Projet `89b97ed`. Les nouvelles captures
du pilotage utilisent également cette iconographie. La numérotation des seize
chapitres reste continue. Les aperçus relus sont dans
`tmp/pilotage-integrated-guide-pdf` ; le PDF canonique, la copie embarquée et
le fichier servi partagent le SHA-256
`e8a8b59eb7fc435c805b1d043a0f9c73da3f00aa3f139f393d45e3c1273e5413`.
Le préfixe de rapport est fourni au banc par `ANIMATION_GUIDE_ARTIFACTS` afin
d'isoler cette passe des autres recettes.

La modification concerne l'espace organisateur. Le guide Commerçant est sans
impact : ses parcours de scanner, préparation et activité ne changent pas.

## Ajout du 22 novembre 2026 - maximum de mauvaises réponses

Les captures `mauvaises-reponses-1280.png` et `mauvaises-reponses-390.png`
montrent la section réelle **Réponses des participants** dans la configuration
d'un Juste Prix Local en brouillon. Le maximum de trois mauvaises réponses est
un exemple fictif ; le même réglage existe pour le Jeu des vitrines. Base Git
Animation `d72bb29`, avec les modifications du plan « Limiter les mauvaises
réponses et rendre les étapes invalides visibles ». Aucun écran n'est redessiné.

Le chapitre 4 explique le réglage de 1 à 10, sa fixation à la publication,
l'épuisement des essais, le tampon invalide et le maintien de la qualification
si le seuil est atteint. Cette édition comporte **quinze chapitres et pages**.
Les quinze pages ont été rendues et relues, dont la nouvelle page 4 en détail.

Depuis `localeo-animation`, avec Chromium installé :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/attempts-animation-build'
node scripts/build-pwa-tests.mjs
node tests/browser/wrong-answer-guide.mjs
py -3.14 scripts/generate-animation-guide.py --preview-dir tmp/attempts-guides-animation-pdf
npm run guide:sync
npm run guide:check
$env:ANIMATION_TEST_DIST = 'tmp/attempts-guides-build-animation'
node scripts/build-pwa-tests.mjs
$env:ANIMATION_GUIDE_ARTIFACTS = 'tmp/attempts-guides-access-animation'
node tests/browser/animation-guide.mjs --access-only
```

Le banc de capture utilise un port éphémère, l'origine `api.test.invalid` et des
API simulées, sans écriture métier ni accès réel. Sa provenance est dans
`localeo-animation/tmp/attempts-guides-captures-fgQu40/provenance.json`.
La recette d'accès utilise le port 4182 : lien visible et accessible au clavier,
ouverture dans un nouvel onglet, HTTP 200, type PDF et contenu identique au
canonique, y compris avec l'assistance en erreur. La copie PDF embarquée est
identique au canonique. Ces preuves concernent un build local synthétique,
sans démontrer un déploiement distant.

## Ajout du 22 novembre 2026 — tableau de bord quotidien

Les captures `tableau-de-bord-1024.png`, `tableau-de-bord-390.png` et
`alertes-tableau-de-bord-1024.png`, `alertes-tableau-de-bord-390.png` montrent
le tableau de bord React réel, sur base Animation `bd64dcc` avec l'évolution
E73-EVO-DASHBOARD-JOUR du même lot. L'API est simulée, les chiffres sont fictifs
et l'horloge pédagogique reste fixée au 21 novembre 2026 à midi UTC. Aucun
compte ou accès utilisable n'est exposé. Les deux premiers chapitres séparent
l'activité de la gestion des rappels pour garder les caractères et captures
lisibles ; cette édition comporte **quatorze chapitres**.

Depuis `localeo-animation` :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/dashboard-guide-build'
$env:ANIMATION_GUIDE_ARTIFACTS = 'tmp/dashboard-guide-captures-final'
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --captures-only --only=tableau-de-bord
py -3.14 scripts/generate-animation-guide.py --preview-dir tmp/dashboard-guide-preview-final
npm run guide:sync
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --access-only
npm run guide:check
```

Port local 4182 ; build et rapports séparés du banc fonctionnel quotidien.
Les captures remplacent seulement celles du tableau de bord et ajoutent les
rappels personnels. Les autres images conservent leur provenance ci-dessous.
Toutes les pages du PDF sont rendues et relues après génération ; la recette
d'accès vérifie la copie PDF servie, ses liens et l'absence d'écriture métier.

## Captures initiales du 21 novembre 2026

Captures du 21 novembre 2026 : application React réelle de `localeo-animation`,
base Git `292f036` avec les modifications du guide présentes dans le même lot.
Elles ne sont ni des maquettes dessinées, ni des captures d'un environnement de
production. Les noms « Valmont (exemple) », « Camille Exemple » et les contacts
`example.invalid` sont synthétiques.

Le banc `localeo-animation/tests/browser/animation-guide.mjs` sert un build isolé
sur `127.0.0.1:4182`, intercepte l'API vers `api.test.invalid` et utilise les
fixtures applicatives `saas-journey.mjs`, `dotation.mjs`, `activity-profile.mjs`
et `campaigns.mjs`. Chaque capture porte sur le titre et la zone utile d'un
véritable écran. La navigation et les composants ne sont pas redessinés.

Les vues sont prises à 1 024 px (zone utile d'environ 800 px) et 390 px ; l'heure
de référence est le 21 novembre 2026 à midi UTC, avec le fuseau Europe/Paris.
Le dossier conserve les variantes bureau/mobile des douze écrans, même lorsque
le PDF ne retient qu'une variante. Le guide utilise des états adaptés à chaque
chapitre : brouillon en préparation, animation en cours dont la fin prévue est
atteinte pour la clôture, animation clôturée pour les remises et le bilan.

Depuis `localeo-animation`, après installation des dépendances et de Chromium :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/guide-animation-dist-current'
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --captures-only
py -3.14 scripts/generate-animation-guide.py --preview-dir tmp/guide-refresh-animation-current/pdf-pages
npm run guide:sync
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --access-only
npm run guide:check
```

Le second build incorpore le PDF final. La recette complète vérifie aussi le
lien au clavier sur bureau et mobile, l'ouverture dans un nouvel onglet, le type
PDF servi et l'égalité avec le livrable canonique. Les requêtes inattendues, les
erreurs JavaScript et les écritures métier font échouer la recette. Les rapports
de capture restent dans `localeo-animation/tmp/guide-refresh-animation-current`.
Cette recette locale ne prouve pas un déploiement ou une recette sur appareil réel.

Le PDF est rendu intégralement en PNG et relu visuellement après génération.
Il faut recapturer les écrans affectés lorsqu'un parcours, un libellé, un état ou
une action change, puis régénérer et synchroniser le guide.

## Ajout du 22 novembre 2026 — produits du Juste Prix Local

Les captures `juste-prix-produits-1024.png` et `juste-prix-produits-390.png`
montrent le composant React réel **Produits et prix proposés**, cadré sur les
compteurs de la page et la première proposition à examiner d'un commerce fictif.
Base Git Animation `4960688`,
avec le correctif d'approbation et de présentation du même lot. Le guide retient
la variante 1 024 px dans son nouveau chapitre 5 ; la variante 390 px documente
la présentation mobile. Cette édition du guide comporte treize chapitres.

Depuis `localeo-animation`, avec les dépendances et Chromium installés :

```console
node tests/browser/juste-prix-products.mjs --guide-captures
```

Ce banc construit un build isolé, sert l'interface sur `127.0.0.1:8191` et simule les lectures et décisions
avec des données synthétiques. Il ne contacte pas un environnement de production.
Ces captures complètent celles du 21 novembre ; elles ne prouvent pas un
déploiement distant.

## Logistique des lots et remises — captures actualisées le 25 novembre 2026

Les captures `lots-remises-1024.png` et `lots-remises-390.png` présentent la
liste globale **Lots et remises** : bénéficiaires, états, lieux de retrait,
utilisation des bons et coffrets et actions disponibles. La recette utilise
des données fictives. Base Git Animation `4a86877` avec l’alignement de la
liste sur Tirages. Au chapitre « Organiser le tirage et les retraits »,
la capture bureau de 702 × 440 pixels cadre les en-têtes et les deux premières
lignes. La capture mobile de 390 × 772 pixels va du titre de liste au bas de
la première fiche, avec le lieu de retrait et l’action de remise.

La capture s'effectue avec le banc applicatif et les API simulées décrits plus
haut, dans le build isolé du guide sur `127.0.0.1:4182` :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/alignement-suivi-lots'
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --only=lots-remises --captures-only
```

Les 22 pages du guide versionné ont été rendues. La page 16, « Organiser
le tirage et les retraits », contient la nouvelle capture. Le texte, les
signets, les liens et les 21 autres pages correspondent au PDF de référence.
La copie embarquée dans Animation est identique au PDF canonique. L'accès
depuis l'application a été vérifié à 390 et 1 024 px.

Le [bilan de livraison E73](../../../../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md)
conserve les preuves de la première livraison. Passe du 22 novembre avec
l’ancien cadrage : captures depuis `tmp/quality-build-oOShOO`, aucun appel
inconnu, aucune erreur navigateur ni écriture. Les treize pages du PDF ont été
rendues et relues ; la page 11 a été inspectée en détail. La copie embarquée
est identique au PDF canonique. Le build `tmp/quality-build-ZhDZiQ` a servi le
nouveau PDF : accès clavier, HTTP 200, contenu identique et aide disponible
avec assistance HTTP 503 vérifiés à 390/1024 px par le mode `--access-only`.

## Ajout du 22 novembre 2026 — parcours mobile first

`preparation-mobile-detail-390.png` illustre le chapitre 7 : sélecteur nommé,
étape Terrain et contrôles. Cadrage navigateur de 390 × 480 px, sans modification
du DOM ni retouche. `animations-mobile-390.png` conserve la preuve de l'entrée
Animations : première action visible à 390 × 844 sans défilement. La base Git
Animation est `08aef5a`, complétée par le lot mobile first du répertoire de travail.

Les captures proviennent de la vraie application avec API synthétiques,
origine `api.test.invalid`, données fictives et ports HTTP locaux éphémères :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/mobile-first-release-build'
node scripts/build-pwa-tests.mjs
node tests/browser/hunt-guided-workflow.mjs
$env:HUNT_GUIDE_CAPTURE_ONLY = '1'
node tests/browser/hunt-guided-workflow.mjs
Remove-Item Env:HUNT_GUIDE_CAPTURE_ONLY
$env:ANIMATION_TEST_DIST = 'tmp/mobile-first-delivery-build'
node scripts/build-pwa-tests.mjs
node tests/browser/mobile-first-lists.mjs
```

Sources des captures : `tmp/mobile-first-hunt-1795373098393` et
`tmp/mobile-first-lists-AiyQ5s` dans Animation. Le mode de capture est annoncé
`captured` ; la recette Chasse distincte a réussi 5 scénarios / 166 contrôles
dans `tmp/mobile-first-hunt-1795373016340/report.json`. Les listes ont réussi
5 scénarios, y compris texte 200 %, dans leur propre rapport.

Le PDF comporte seize pages. Elles ont toutes été rendues et relues, avec
inspection détaillée des chapitres 4 et 7, puis la copie embarquée a été
synchronisée et contrôlée. Prévisualisations : `tmp/mobile-first-guide-preview`
et nouveau rendu du PDF final dans `tmp/mobile-first-guide-final-render`.
Cette recette locale ne qualifie ni appareils physiques ni environnement distant.

Le build final `tmp/mobile-first-verified-build` embarque le PDF actualisé.
`tests/browser/animation-guide.mjs --access-only` a vérifié ses liens au clavier,
son contenu servi identique au canonique et l'accès avec assistance indisponible
à 390/1024 px. Rapports de requêtes : `tmp/mobile-first-guide-access` (aucune
requête inconnue, erreur navigateur ou écriture).

## Ajout du 22 novembre 2026 - seuil de validation

La capture `seuil-validation-1280.png` cadre le champ réel **Seuil de validation**
dans la configuration d'un Passeport commerçant : six commerces fictifs
sélectionnés, choix de six validations. Base Git Animation `063c229`, avec
le correctif du seuil du même lot. Le guide utilise ce cadrage au chapitre 2 ;
l'ancienne illustration de l'Assistant reste conservée dans ce dossier.

Depuis `localeo-animation`, le banc utilise un build synthétique, l'origine
`api.test.invalid`, des API simulées et un port HTTP local alloué dynamiquement,
sans dotenv opérateur :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/threshold-build'
node scripts/build-pwa-tests.mjs
node tests/browser/qualification-threshold.mjs
```

La capture de référence provient de
`localeo-animation/tmp/threshold-report-16OWJ0/seuil-validation-1280.png`.
Elle mesure 1 006 × 94 pixels, sans modification du DOM, donnée personnelle,
QR ni secret. Le banc vérifie les trois jeux concernés à 320, 390 et 1 280 px
ainsi qu'à 1 280 px avec texte agrandi à 200 %. Cette recette locale ne prouve
pas un déploiement distant.

## Actualisation du 24 novembre 2026 - condition d’achat du Passeport

Le cadrage `achat-passeport-1280.png` montre le champ **Achat pour valider un
passage**, avec **Visite sans achat** sélectionné. Il provient de la
configuration d’un brouillon fictif à 1 280 px, sur la base
Animation `475e063` avec l’évolution locale de la condition d’achat. Le même
banc vérifie la modification au clavier et le choix pendant la création.

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/passport-purchase-build'
node scripts/build-pwa-tests.mjs
node tests/browser/qualification-threshold.mjs
```

Le fichier est produit dans le dossier `tmp/threshold-report-*` annoncé par
le scénario. Il cadre le champ réel sans modifier le DOM, avec des données
fictives, sans QR ni identifiant de participant.

Le PDF mis à jour conserve treize chapitres et treize pages, rendues en PNG
dans `localeo-animation/tmp/threshold-guide-preview/pages` puis relues, avec
une inspection détaillée du chapitre 2. La génération et la synchronisation
utilisent les commandes de maintenance ci-dessus.

## Ajout du 22 novembre 2026 - communication communale

Le chapitre **Informer les abonnés de la commune** utilise une capture du
formulaire réel de Localeo Animation avec des données fictives. Le cadrage
isole le message, le filtre personnalisé et le choix du lien dans la capture
bureau de 1 024 × 1 200 pixels. La capture provient du banc navigateur
Communication communale, depuis la sortie
`localeo-animation/tmp/communal-campaigns-browser/communication-communale-1024.png`.

Depuis `localeo-animation` :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/communal-campaigns-dist'
node scripts/build-generation-tests.mjs
node tests/browser/communication-communale.mjs
```

Le banc utilise des appels API simulés. Il vérifie l’accès, la rédaction,
les filtres combinés, l’aperçu, le reçu après perte de réponse et le bilan
au clavier sur ordinateur, ainsi que la création dans le menu mobile à
390 pixels et les refus sans module ou sans autorisation.

Les 17 pages du guide ont été rendues et relues. Après synchronisation et
reconstruction, `node tests/browser/animation-guide.mjs --access-only`
vérifie l’accès clavier à 390 et 1 024 pixels depuis le menu du compte et
**Support**. Le PDF reste accessible quand le support répond 503. Le fichier
servi en HTTP 200 est identique au PDF canonique.
