# Adaptation mobile de Localeo Animation

L'application conserve son interface de bureau. Sous 768 px, les tableaux métier
deviennent des listes de fiches : identité, deux informations prioritaires,
détails dépliables et actions. Les cellules et les gestionnaires d'événements
proviennent du même rendu React ; aucun appel API spécifique au mobile n'est ajouté.
Les tableaux intégrés doivent utiliser `ResponsiveTable`. Les cellules partagées
doivent être des éléments `td` ou des fragments React, comme `participantIdentityCells`.
Le composant prend en charge les lignes de chargement et les états vides avec `colSpan`.

Les filtres sont dépliables sur téléphone. Le menu latéral devient un tiroir sous
1024 px ; il ferme l'accès au contenu sous-jacent et gère le focus et Échap.
Les rubriques de l'animation et les étapes de création disposent de sélecteurs
mobiles. Les boutons précédent/suivant de création restent hors de la zone de
défilement. Les formulaires, factures, montants et actions passent sur plusieurs
lignes lorsque nécessaire.

Les contrôles tactiles ont une hauteur minimale de 44 px et les champs mobiles
utilisent une police de 16 px. Les fenêtres et la hauteur de l'application suivent
`visualViewport` pour tenir compte de l'espace disponible lorsque le clavier
s'affiche. Les graphiques chronologiques conservent un défilement horizontal
local pour garder leurs axes lisibles. Les animations du menu respectent la
préférence de réduction des mouvements.

## Vérification automatisée

Les tests de composants font partie de `npm test` : conservation des coordonnées
masquées, des libellés, des actions désactivées, des sélections, des états vides et
des tableaux de bureau.

La recette navigateur utilise des réponses API synthétiques. Toutes les requêtes
externes sont interceptées : aucun compte réel, envoi, achat ou suppression serveur.
Elle parcourt 27 vues aux largeurs 320, 390, 768 et 1440 px, puis vérifie les
interactions du menu, le chargement de lignes supplémentaires, les détails et
confirmations, les sélections, l'édition d'actualité, la facturation, le paiement
avec une hauteur réduite et les huit étapes de création.

Installer l'outil de recette dans le dossier temporaire, sans changer les
dépendances de l'application :

```sh
npm install --prefix tmp/mobile-qa --no-audit --no-fund playwright@1.63.0
node tmp/mobile-qa/node_modules/playwright/cli.js install chromium
npm run dev -- --host 127.0.0.1
```

Dans un second terminal, à la racine du dépôt :

```sh
node tests/browser/mobile-smoke.mjs
```

Le serveur doit écouter sur `127.0.0.1:5173`. Pour utiliser un Chromium déjà
installé, définir `PLAYWRIGHT_CHROMIUM_EXECUTABLE` avec son chemin absolu.
Le rapport et les captures sont écrits dans `tmp/mobile-qa/`.

## Recette sur appareils physiques

La simulation Chromium et une fenêtre de hauteur réduite ne remplacent pas un
essai sur Safari iOS et Chrome Android. Vérifier le clavier réel, les zones sûres,
les sélecteurs de dates, les téléchargements PDF/CSV, la lecture du QR et le retour
depuis Stripe dans l'environnement de test avant mise en production.
