# Captures du guide utilisateur Animation

## 22 novembre 2026 - iconographie de gestion

Les illustrations concernées sont reprises depuis le build synthétique
Animation, base `08aef5a` avec la nouvelle iconographie. La recette
`tests/browser/animation-guide.mjs` utilise des données fictives et un
dossier de captures isolé. Le chapitre Dotation précise le raccourci
**Lots** en configuration sur mobile.

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

## Ajout du 22 novembre 2026 — logistique des lots et remises

Les captures `lots-remises-1024.png` et `lots-remises-390.png` présentent la
liste globale **Lots et remises** : bénéficiaires, états, lieux de retrait,
utilisation des bons et coffrets et actions disponibles. Les données sont fictives ; aucun QR, PIN ou contact réel n'est
utilisé. Base Git Animation `9ba1e8c`, avec le correctif d'ergonomie du même lot.
La variante 1 024 px remplace la vue de remise par animation au chapitre 11 du
guide ; l'ancienne capture reste conservée. Les treize chapitres sont maintenus.
La zone bureau de 736 × 394 pixels cadre les en-têtes et les deux premières
lignes pour rester lisible dans le PDF. La capture mobile de 390 × 840 pixels
montre la première fiche, son retrait et son action, sans modifier le DOM.

La capture s'effectue avec le banc applicatif et les API simulées décrits plus
haut, dans le build isolé du guide sur `127.0.0.1:4182` :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/guide-animation-dist-current'
node scripts/build-pwa-tests.mjs
node tests/browser/animation-guide.mjs --only=lots-remises --captures-only
```

La génération et le
second build servent ensuite à relire toutes les pages du PDF et à vérifier la
copie servie depuis l'application. Les commandes et résultats de cette passe
sont consignés dans le
[bilan de livraison E73](../../../../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md).
Cette preuve locale ne constitue pas une recette sur appareil physique ni un
déploiement distant.

Passe exécutée : captures depuis `tmp/quality-build-oOShOO`, aucun appel
inconnu, aucune erreur navigateur ni écriture. Les treize pages du PDF ont été
rendues et relues ; la page 11 a été inspectée en détail. La copie embarquée
est identique au PDF canonique. Le build `tmp/quality-build-ZhDZiQ` a servi le
nouveau PDF : accès clavier, HTTP 200, contenu identique et aide disponible
avec assistance HTTP 503 vérifiés à 390/1024 px par le mode `--access-only`.

## Ajout du 22 novembre 2026 — parcours mobile first

`preparation-mobile-detail-390.png` illustre le chapitre 6 : sélecteur nommé,
étape Terrain et contrôles. Cadrage navigateur de 390 × 480 px, sans modification
du DOM ni retouche. `animations-mobile-390.png` conserve la preuve de l'entrée
Animations : première action visible à 390 × 844 sans défilement. La base Git
Animation est `bb20ac9` pour la capture de liste, complétée par le lot mobile.

Les captures proviennent de la vraie application avec API synthétiques,
origine `api.test.invalid`, données fictives et ports HTTP locaux éphémères :

```powershell
$env:ANIMATION_TEST_DIST = 'tmp/mobile-first-release-build'
node scripts/build-pwa-tests.mjs
node tests/browser/hunt-guided-workflow.mjs
$env:HUNT_GUIDE_CAPTURE_ONLY = '1'
node tests/browser/hunt-guided-workflow.mjs
Remove-Item Env:HUNT_GUIDE_CAPTURE_ONLY
$env:ANIMATION_TEST_DIST = 'tmp/mobile-push-build'
node scripts/build-pwa-tests.mjs
node tests/browser/mobile-first-lists.mjs
```

Sources des captures : `tmp/mobile-first-hunt-1795373098393` et
`tmp/mobile-first-lists-7sWASH` dans Animation (recette isolée dans
`tmp/mobile-push-o98dbd_h/localeo-animation`). Le mode de capture est annoncé
`captured` ; la recette Chasse distincte a réussi 5 scénarios / 166 contrôles
dans `tmp/mobile-first-hunt-1795373016340/report.json`. Les listes ont réussi
5 scénarios, y compris texte 200 %, dans leur propre rapport.

Le PDF comporte quinze pages. Elles ont toutes été rendues et relues, avec
inspection détaillée des chapitres 3 et 6, puis la copie embarquée a été
synchronisée et contrôlée. Les prévisualisations du lot isolé se trouvent dans
`tmp/mobile-push-guide`.
Cette recette locale ne qualifie ni appareils physiques ni environnement distant.

Le build de recette `tmp/mobile-push-build` embarque le PDF actualisé.
`tests/browser/animation-guide.mjs --access-only` a vérifié ses liens au clavier,
son contenu servi identique au canonique et l'accès avec assistance indisponible
à 390/1024 px. Rapports de requêtes dans `tmp/mobile-push-guide-access` (aucune
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

Le PDF mis à jour conserve treize chapitres et treize pages, rendues en PNG
dans `localeo-animation/tmp/threshold-guide-preview/pages` puis relues, avec
une inspection détaillée du chapitre 2. La génération et la synchronisation
utilisent les commandes de maintenance ci-dessus.
