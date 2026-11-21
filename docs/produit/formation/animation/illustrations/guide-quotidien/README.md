# Captures du guide utilisateur Animation

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
