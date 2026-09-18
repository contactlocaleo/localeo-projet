# Espace de travail commerçant

Cette déclinaison reprend des principes de navigation professionnelle
de Localeo Animation. Les projets restent indépendants : aucun import, paquet,
asset ou lien de compilation vers le dépôt Animation, aucune nouvelle dépendance npm.

## Périmètre

- Navigation latérale à partir de 1024 px ; raccourcis Accueil, Scanner, Activité
  et menu Plus en dessous. Le menu utilise un dialogue HTML natif.
- Accueil compact : scanner, tâches à traiter, synthèse et accès à la gestion.
- Reversements : tableau à partir de 768 px, fiches avec détails dépliables en dessous.
- Prestations : liste et détail côte à côte sur bureau, accès au détail avec
  déplacement du focus sur mobile, retour à la liste et recherche. La confirmation
  avant abandon des modifications et les restrictions d'édition sont conservées.
- Activité : synthèse, indicateurs, tendances et ventilation par prestation ;
  filtres repliables sur mobile.
- Animations : lignes compactes, invitations, détail de la mission et du règlement,
  confirmation de la décision, notifications et pagination.
- Facturation : navigation de rubrique, listes filtrables, montants, détails des
  demandes et formulaires, y compris Chorus Pro quand la fonction est activée.
- Page publique : état de publication, complétion, formulaire et aperçu côte à côte
  sur grand écran, disposition verticale sur mobile.
- Compte : coordonnées en premier, puis paiements et notifications. Contact,
  historique des demandes et changement de mot de passe adoptent les mêmes repères.
- Cadre commun de l'espace connecté. La connexion et la préparation du compte
  conservent leur présentation et leur parcours.

Les routes, les contrôles de session et les contrats API sont conservés.
Le menu respecte les indicateurs d'activation Animation et Facturation.
Les versions affichées dans les reversements sont celles à l'achat, avec une
mention explicite lorsque la donnée n'existe pas.

## Organisation du code

- `src/app/merchantNavigation.js` : groupes de navigation et reconnaissance des routes.
- `src/app/MobileNavigation.jsx` : navigation bureau et dialogue mobile.
- `src/app/ApplicationFrame.module.css` : disposition du cadre connecté.
- `src/features/dashboard/MerchantHomePage.jsx` : accueil extrait de `App.jsx`.
- `src/features/payouts/ReversementsActionWorkspace.jsx` : écran extrait de
  `ActionWorkspaces.jsx`, avec ses propres styles.
- `src/features/payouts/PayoutMovements.jsx` : modèle explicite des champs utilisé
  par les deux présentations, sans analyser le HTML ni refaire les requêtes.
- `src/app/BusinessWorkspace.module.css` : primitives visuelles propres à Commerçant
  (titres, formulaires, listes, filtres, actions et états). Aucun partage interprojet.
- `src/app/ResponsiveFilters.jsx` : repli natif des filtres sur mobile. Les valeurs
  restent dans l'état de la page métier et sont conservées lors d'un redimensionnement.
- Modules CSS par domaine dans `features/workspaces`, `features/dashboard`,
  `features/animations` et `features/finance` : disposition spécifique aux écrans.
- `src/features/workspaces/PasswordUpdateWorkspace.jsx` : formulaire extrait de
  `ActionWorkspaces.jsx`, avec les mêmes règles de validation et de reconnexion.

Les nouveaux styles utilisent CSS Modules. Les sélecteurs globaux des zones
migrées ont été retirés. Pour une évolution future, modifier le module concerné
plutôt qu'ajouter une surcharge en fin de `src/styles.css`.
Les actions de formulaire restent dans le flux pour ne masquer aucun champ.
Les messages utilisent une palette commune : vert pour une réussite confirmée,
rouge pour une erreur, jaune pour un avertissement et bleu pour une information
ou une opération en cours. Le fond opaque, la bordure et l'icône décorative gardent
le contraste sur les pages claires et sombres ; le texte porte toujours le sens.
`src/app/FeedbackMessage.jsx` fournit les annonces `status` ou `alert` pour les
nouveaux messages. Les classes existantes `menu-alert` et `scan-feedback` utilisent
la même palette dans `src/styles.css`, sans dépendance ajoutée.
L'acceptation d'une participation et l'accusé de réception d'une demande de facture
ont un retour explicite. Un conflit de version est un avertissement, un échec est
une erreur. Le mandat Chorus n'est confirmé en vert qu'après relecture de l'état attendu.
Les appels API et décisions métier restent dans leurs composants et services existants.
Le message de réussite d'une modification de prestation reste affiché après le
rechargement de la liste ; il est effacé au changement de sélection ou de saisie.

## Vérification

`npm run build`, `npm test` et `npm run test:e2e`.

`tests/e2e/operational-ux.spec.js` contrôle les largeurs 360, 390, 768, 1024 et
1440 px, les débordements, le scanner au premier écran, le menu au clavier,
le retour de focus, les détails de reversement et l'accessibilité axe.
Les captures sont générées dans `test-results/`. Les données de ces tests sont
synthétiques ; les tests ne réalisent aucun paiement réel.

`tests/e2e/business-ux.spec.js` parcourt 16 écrans métier à 390, 1024 et 1440 px,
contrôle les débordements, les classes de styles manquantes, les erreurs JavaScript
et l'accessibilité axe. Il vérifie aussi la sélection et l'enregistrement d'une
prestation sur mobile, la protection des modifications en cours, la conservation
des filtres au redimensionnement et les sauvegardes du compte et de la page publique.
Le build synthétique active l'édition des prestations pour exercer ce parcours ;
le réglage de production reste inchangé.

Sur Windows, si l'arrêt automatique du serveur Playwright reste en attente,
construire avec `node scripts/build-browser-tests.mjs`, lancer
`node scripts/serve-browser-tests.mjs` dans un terminal séparé, puis exécuter les
tests avec `LOCALEO_E2E_EXTERNAL_SERVER=1`. Arrêter ce serveur après les tests.

Deux attentes antérieures ont été remises en cohérence avec l'application : le
test de chargement des polices vérifie DM Sans et Oswald ; le build synthétique
autorise explicitement l'origine des QR de test. La configuration de production
n'est pas modifiée.

Cette validation automatisée utilise Chromium. Le comportement de la caméra et
du clavier sur de vrais appareils iOS et Android reste à vérifier avant une diffusion large.
