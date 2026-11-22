# Identité des en-têtes Localeo

## Périmètre

Localeo Pro, Animation, ERP, OnBoard, Ops, Support, Atelier et CRM utilisent
la même signature dans leur en-tête principal. Le nom de l’application permet
de se repérer ; ses actions et sa navigation restent adaptées à son public.
Les favicons et icônes d’installation ne sont pas remplacés par cette correction.

Depuis le 21 novembre 2026, Marketplace, Live et e-mails transactionnels
partagent la signature publique décrite ci-dessous. Elle remplace pour Live
l'ancienne signature commune aux applications de gestion.

Depuis le 22 novembre 2026, Pro et Animation reprennent les couleurs bleu nuit,
orange et papier de la marque publique, selon la déclinaison de gestion
décrite plus bas. Leur symbole, leur typographie et leur composition restent
ceux des applications de gestion.

## Signature commune des applications de gestion

| Élément | Règle |
| --- | --- |
| Fond de l’en-tête | Bleu nuit `#123247` pour les outils internes ; `#082840` pour Pro et Animation |
| Symbole | SVG Localeo `header-mark.svg`, identique dans les quatre dépôts applicatifs, sans ombre ajoutée |
| Dimensions du symbole | 40 × 40 px ; 36 × 36 px jusqu’à 600 px ; proportions conservées |
| Espacement symbole / texte | 10 px |
| Marque | `Localeo`, blanc, suivie du nom de l’application |
| Nom de l’application | Pro, Animation, ERP, OnBoard, Ops, Support, Atelier ou CRM ; orange `#f5ad6e`, sans italique ni séparateur |
| Police de la signature | `system-ui, -apple-system, "Segoe UI", sans-serif` ; graisse 800, interligne 1,15, approche −0,02 em |
| Taille du texte | 1,25 rem ; 1,125 rem jusqu’à 600 px (20 et 18 px à taille de texte standard) |
| Environnement | Conserver le repère TEST ou autre environnement lorsqu’il existe, en capsule discrète blanche ; placé sous le nom sur mobile dans Pro |
| Sous-titre | Aucun sous-titre dans le bloc de marque |

Le symbole porte un texte alternatif vide : le nom accessible du lien ou du
bouton annonce déjà l’application et le retour à l’accueil. Conserver les
destinations existantes et les protections contre l’abandon d’une saisie.

## Signature publique Marketplace, Live et e-mails — 21 novembre 2026

La référence est la Marketplace et ses tokens, pas la charte CRM. Le bandeau
est encre `#082840`, la marque blanche en Oswald et le nom de surface reste
identifié (« Localeo Live » dans Live, catégories conservées dans les e-mails).
Le nom Live est sans italique. Le nom de produit Marketplace est en orange
clair `#ffd8b5` et Live reprend le ton Pro et Animation `#f5ad6e` depuis le
22 novembre. DM Sans porte les contrôles et les libellés utilitaires.

Le pictogramme est `public/icons/localeo-coffret-icon.png` dans le frontend et sa
copie `app/infrastructure/email/templates/localeo.png` dans le backend : rapport
1:1, rendu sans étirement ni fond ajouté. Live conserve 40 × 40 px, 36 × 36 px
jusqu'à 600 px ; la Marketplace conserve sa boîte d'image avec `object-fit:
contain` et les e-mails leur affichage 32 × 32 px. La signature Live reste à
1,25 rem, puis 1,125 rem sur mobile ; le repère TEST n'est pas supprimé.

Live inclut ce PNG dans son précache public et son empreinte de build. Le logo
reste disponible hors connexion ; les protections des API et accès personnels
du service worker restent applicables.

Les destinations et noms accessibles sont conservés. Les e-mails gardent leurs
replis typographiques et leur composition compatible messagerie selon la
[charte e-mail](charte-emails-localeo.md). Cette orientation ne change pas les
signatures de Pro, Animation ou des outils internes, ni les icônes PWA.

## Mobile et accessibilité

- Le nom et le symbole restent visibles : ni troncature ni disparition pour
  gagner de la place. Autoriser un retour à la ligne si nécessaire.
- Les actions de l’en-tête gardent une cible tactile d’au moins 44 × 44 px.
  Leur groupe peut passer sur une seconde ligne sur un écran étroit.
- Le retour à l’accueil fonctionne au clavier avec un focus visible.
- Vérifier les largeurs 320, 390 et 1280 px, l’agrandissement du texte et le
  zoom. Les éléments fixes tiennent compte d’une hauteur d’en-tête variable.
- L’identité ne modifie pas les droits, les menus autorisés, les confirmations
  PWA, les badges de notification ni les comportements de session.

## Mise en œuvre et maintenance

Les six outils internes du backend partagent `app-header.js` et
`app-header.css`. Pro utilise son `ApplicationFrame`, Animation son shell et
Live un composant `LiveBrand`, réutilisé à son entrée publique selon la signature
publique. Les copies du SVG des applications de gestion restent locales à chaque application pour préserver leurs déploiements
indépendants ; comparer leurs empreintes lors d’une modification du symbole.

Les formulaires publics de connexion interne et de choix du mot de passe
reprennent la signature statique **Localeo ERP**, la feuille `app-header.css`
et le même symbole. Ils ne chargent pas `app-header.js` ni le contexte de session
protégé. Seules ces ressources visuelles sont autorisées sans authentification,
par chemin exact. Le formulaire conserve ses protections et son aide secondaire.

Modifier les règles à leur source, retirer les anciennes variantes de marque
et éviter une succession de surcharges. Le SVG doit être servi par la route
statique autorisée et inclus dans la version des ressources lorsqu’une PWA
repose sur une empreinte de fichiers.

Cette convention concerne la présentation. Elle n’introduit aucun changement
de contrat API, de règle métier, de migration ou de données de démonstration.
Le suivi de correction et les preuves figurent dans le
[registre des anomalies backend](../../roadmap/anomalies/backend.md#ano-transverse-header-20261101--identités-divergentes-dans-les-huit-applications).

## Charte des espaces de gestion internes — référence CRM

Depuis le 4 novembre 2026, Localeo CRM sert de référence visuelle à ERP, Ops,
OnBoard, Support et Atelier. Pro et Animation ont partagé cette palette
jusqu'à la déclinaison bleu nuit et orange du 22 novembre 2026 ci-dessous.
Le bandeau de marque bleu nuit reste commun ;
les actions de travail utilisent le vert pétrole. Les tokens `--localeo-*`
de `app-header.css` sont la source partagée des applications internes, consommée
également par CRM. Pro et Animation conservent leurs tokens locaux, sans
dépendance d’exécution entre dépôts.

Dans l’ERP, l’identité de session et le nombre de communes accessibles sont
affichés dans le bandeau principal, sans bande intermédiaire au-dessus du
contenu. Sur mobile, cette information passe sur une ligne compacte du même
en-tête ; elle s’efface lorsque la session expire.

| Élément | Règle commune |
| --- | --- |
| Fond / texte / texte secondaire | `#f5f7f9` / `#183243` / `#526575` |
| Action principale | Vert `#09685e`, texte blanc, libellé explicite |
| Action secondaire / destructive | Blanc bordé / rouge distinct ; confirmations conservées |
| Navigation active | Fond `#e1f0ec`, texte `#07594f`, repère actif accessible |
| Typographie de travail | Police système, corps 14 px, titres 25 / 18 / 15 px ; titre principal 23 px sur mobile |
| Contours | Bordures `#d8e1e7`, panneaux 12 px, boutons 9 px, champs 7 px |
| Interaction | Cibles d’au moins 44 px, focus ocre `#b96913`, clavier et réduction des animations conservés |
| Hiérarchie | Titre et action de page repérables ; filtres regroupés, actions secondaires distinctes, erreurs proches du contexte |

Conserver la composition utile à chaque métier : navigation hiérarchisée ERP,
priorités d’alertes Ops, liste/dossier OnBoard, recherche Support, préparation
Atelier et suivi CRM. La cohérence ne consiste pas à imposer la barre mobile du
CRM à toutes les applications. Les alertes restent distinguées par leur libellé
et leur gravité, indépendamment de la couleur des actions.

Modifier les règles existantes plutôt qu’ajouter des surcharges successives.
Ops utilise sa feuille unique `ops.css`, sans ancien bloc de styles en ligne.
Les connexions internes consomment les mêmes tokens. Pro et Animation harmonisent
leur cadre, leurs composants de gestion et leurs formulaires d’accès. La surface
habitante Live a repris le 10 novembre 2026 la typographie et les sections de Pro.
Depuis le 21 novembre, elle reprend la signature publique Marketplace. Depuis
le 22 novembre, elle utilise la déclinaison de couleurs de Pro et Animation
dans sa composition compacte.
Voir [LIVE-UX-09](../../produit/live/principes-ux.md#live-ux-09--partager-la-marque-marketplace-avec-une-composition-compacte).

Dans Pro et Animation, conserver les rubriques et raccourcis adaptés au métier,
le retour au contexte précédent, les confirmations et les états de chargement.
La navigation claire distingue la rubrique active avec un fond pêche et
son repère accessible. Les états succès, attention et erreur restent sémantiques :
un avertissement ne prend pas la couleur de l’action principale. Les contenus
personnalisables d’une animation, dont le flyer, gardent leurs propres couleurs.
Les champs mobiles conservent une taille lisible de 16 px ; le corps de travail
à 14 px ne doit pas réduire les cibles tactiles, la signature ni le zoom du texte.

Les preuves locales et limites sont dans le
[suivi d’harmonisation](../../roadmap/anomalies/backend.md#ano-interne-charte-crm-20261104--harmonisation-des-espaces-de-gestion).

## Déclinaison Pro et Animation — 22 novembre 2026

**CHARTE-PRO-ANIMATION-20261122.** Décision utilisateur : rapprocher les deux
applications de la marque Localeo par leurs couleurs et leurs icônes.
Cette déclinaison remplace leur palette vert pétrole, sans changer les outils
internes, Marketplace ou Live. Les gabarits, polices, dimensions, parcours,
logos et icônes d'installation sont conservés.

| Usage | Valeur commune |
| --- | --- |
| Bandeau et texte principal | Bleu nuit `#082840` |
| Action principale et lien | Bleu Localeo `#0b3d63`, bouton à texte blanc |
| Survol de l'action principale | Bleu nuit `#082840` |
| Fond et surface | Papier `#f6f5f1` et blanc |
| Navigation active | Fond pêche `#f9eee2`, texte bleu nuit et repère orange foncé `#a85213` |
| Accent graphique | Orange `#f28a2e` |
| Petit texte orange et focus sur fond clair | Orange foncé `#a85213` |
| Focus dans le bandeau sombre | Orange vif `#f28a2e` |

**Extension à Localeo Live le 22 novembre 2026.** Live applique les mêmes
couleurs aux actions, liens, repères et surfaces, avec le texte secondaire
`#526575` et les bordures `#d8e1e7`. Le séparateur des trois rubriques reste
orange et le manifeste PWA associe le bandeau bleu nuit au fond papier.
La signature publique conserve son pictogramme, Oswald et DM Sans. Voir
[LIVE-UX-09](../../produit/live/principes-ux.md#live-ux-09--partager-la-marque-marketplace-avec-une-composition-compacte).

Séparer les tokens d'action, de navigation et d'accent des états métier.
Les succès, attentes, avertissements, erreurs et résultats incertains gardent
leurs libellés et leur gravité ; un aplat orange ne confirme aucune action.
Les couleurs personnalisées des animations et des flyers restent propres à
leur contenu. Modifier les règles propriétaires plutôt qu'empiler des surcharges.

### Critères et impacts

| Critère | Résultat observable et preuve attendue |
| --- | --- |
| CPA-01 | Palette commune dans les cadres, accueils, formulaires et écrans secondaires ; build des deux applications et captures réelles. |
| CPA-02 | Même pictogramme pour une même fonction, contour bleu et accent orange pour les repères métier ; actions compactes monochromes et registres locaux identiques. |
| CPA-03 | Contrastes texte/contrôle/focus, navigation clavier et absence de débordement à 320, 390 et 1280 px et texte 200 % ; états métier toujours explicites. |
| CPA-04 | Captures affectées des deux guides actualisées, PDF entièrement rendu et relu, copie embarquée synchronisée et lien servi vérifié. |

Propriétaires : composants et tokens de présentation des deux frontends ;
aucune règle métier déplacée du backend. Contrats API et consommateurs de
données, permissions, migrations, configuration serveur, requêtes et générateur
de démonstration : sans impact, car seuls styles et pictogrammes changent.
Les recettes utilisent des données fictives et des API simulées. Les applications
peuvent être livrées indépendamment, avec leurs ressources et PDF respectifs.

### Preuves locales du 22 novembre 2026

- **Pro, CPA-01/03** : build synthétique `node scripts/build-check.mjs`
  réussi (`tmp/quality-build-T4iMWu`). Recette Playwright ciblée
  `mobile-header`, `management-ergonomics`, `accessibility`, `home-mobile`
  et `validation-merchant-ux` : **26/26 scénarios réussis** ; rapport
  `tmp/charte-pro-test-reports-final-20261122/results.json`. Contrôle complémentaire
  accueil/scanner/formulaire à 320/390/1280 px et texte 100/200 % : **18/18**,
  aucune violation Axe ni débordement horizontal ; rapport
  `tmp/charte-pro-visual-final-20261122/verification.json`. Focus réel au clavier
  vérifié dans le bandeau, le menu compte et le dialogue d'installation :
  contrastes respectifs 6,09:1 et 5,41:1 ; rapport
  `tmp/charte-pro-focus-keyboard-final-20261122/verification.json`.
- **Pro, CPA-04** : douze captures actualisées, douze pages PDF rendues et
  relues, copies canonique/embarquée/servie identiques. Accès au clavier,
  assistance HTTP 503 et Axe sans violation à 390/1440 px sur le build final ;
  `tmp/charte-pro-guide-verify-snapshot-20261122-2/verification.json`. Dernier
  PDF contrôlé : SHA-256
  `37183d0e2eb3538a991b6d5ec0817c2b82e8409a2f454bb6de751a92b5adbbf3`,
  stable avant/après le contrôle (12 pages, 1 202 199 octets). Une autre tâche
  actualisait les préparations et le guide pendant ce lot : ses captures et
  libellés ont été conservés, le dernier PDF a été rendu et relu à nouveau.
  Les tentatives précédentes dont le PDF a changé sont distinguées dans la
  provenance ; elles ne sont pas comptées comme recette de cette édition. Les commandes
  complètes sont dans la [provenance des captures Commerçant](../../produit/formation/commercant/illustrations/guide-quotidien/README.md).
- **Animation, CPA-01/04** : types TypeScript et lint finaux réussis
  (`tsc --noEmit`, `eslint src vite.config.ts`), build synthétique final réussi
  dans `tmp/charte-animation-20261122`. Les seize pages du PDF ont été rendues
  et relues, puis la copie embarquée synchronisée ; son SHA-256 est
  `e8d25ff6de5cec507f2b65004360287793586373023fb67774006893410c329d`.
  `animation-guide.mjs --access-only` a vérifié HTTP, type, octets identiques,
  clavier et assistance indisponible à 390/1024 px ; rapports
  `tmp/charte-animation-guide-access-final/requests-{390,1024}.json` sans requête
  inconnue, erreur navigateur ou écriture. Commandes et captures dans la
  [provenance Animation](../../produit/formation/animation/illustrations/guide-quotidien/README.md).
- **Animation, CPA-03** : `animation-workspace-ux.mjs`, **10 profils réussis** ;
  rapport `tmp/charte-animation-shell-complete/report.json`. Navigation,
  clavier, menus, notifications, compte et protection des saisies vérifiés à
  320/390/768/1024/1280/1600 px, en paysage 844 px et texte 200 % à
  320/1280/844 px, sans erreur navigateur ni mutation API. Les attentes de
  couleur ont été adaptées à la décision ; les fixtures de lecture Équipe et
  l'attente de la navigation ont été complétées sans retirer les assertions.
- **CPA-02 et revue** : registres JSON Pro/Animation identiques (SHA-256
  `d5e0cef5c1c19ad66827a2023e2cf965cdce8eccdced5f4932b0ef9de6ec0561`). Revue
  indépendante de code et captures : focus sur fonds clairs/sombres, états
  positifs distincts de la navigation, distinction coffret/lot et bordures des
  champs vérifiés ; aucun défaut ouvert dans le périmètre relu.
- **Documentation** : `py -3.14 scripts/check_guidance.py` et son contrôle
  ciblé des documents touchés réussis ; `py -3.14 scripts/sync_documentation.py
  --check-sources` : 155 documents vérifiés. Les guides Commerçant et Animation
  ont tous deux été actualisés ; leurs parcours et libellés utiles ne changent
  pas du fait de ce lot visuel.

Les rapports sont locaux aux dépôts applicatifs et utilisent des API simulées.
Les travaux préexistants ont été conservés ; ces résultats ne qualifient pas un
appareil physique ou un environnement distant et n'attestent aucun déploiement.

### Iconographie de gestion Pro et Animation

Les deux applications utilisent le même dessin pour une même fonction. Les
silhouettes distinguent en particulier le calendrier de la checklist de
préparation, le scan QR du clavier PIN, les participants de l’équipe et le lot
du coffret. Le registre SVG est livré localement dans chaque application pour
préserver leurs déploiements indépendants.

- Repères métier à 24–32 px : contour bleu Localeo et aplat orange discret, sur la
  grille de dessin de 24 × 24. Choisir une couleur de contour lisible sur le
  fond du composant.
- Navigation compacte, actions et états à 16–20 px : tracé monochrome. Le
  pictogramme ne détermine ni la taille de la cible, ni le sens de l’action
  porté par son libellé.
- État confirmé, attente, attention, erreur et résultat incertain : coche,
  horloge, triangle, croix encerclée et point d’interrogation. Conserver le
  texte visible et la gravité propre à chaque état.
- Masquer l’icône aux technologies d’assistance lorsqu’elle accompagne un
  libellé. Une commande sans texte garde un nom accessible sur le contrôle.

Pour relire les SVG au réel, exécuter `node scripts/render-management-icons.mjs`
depuis [Localeo Animation](../../../../localeo-animation/README.md) avec son
Chromium Playwright. La planche PNG/SVG et l’aperçu HTML aux tailles d’usage
sont générés dans `tmp/iconographie-gestion/`. Comparer les registres des deux
dépôts après une évolution commune.
