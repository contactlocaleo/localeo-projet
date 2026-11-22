# Identité des en-têtes Localeo

## Périmètre

Localeo Pro, Animation, ERP, OnBoard, Ops, Support, Atelier et CRM utilisent
la même signature dans leur en-tête principal. Le nom de l’application permet
de se repérer ; ses actions et sa navigation restent adaptées à son public.
Les favicons et icônes d’installation ne sont pas remplacés par cette correction.

Depuis le 21 novembre 2026, Marketplace, Live et e-mails transactionnels
partagent la signature publique décrite ci-dessous. Elle remplace pour Live
l'ancienne signature commune aux applications de gestion.

## Signature commune des applications de gestion

| Élément | Règle |
| --- | --- |
| Fond de l’en-tête | Bleu nuit `#123247` |
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
Le nom Live est sans italique, en orange clair `#ffd8b5`, comme le nom de produit
Marketplace. DM Sans porte les contrôles et les libellés utilitaires.

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
OnBoard, Support et Atelier, ainsi qu’à Localeo Pro et Localeo Animation.
Le bandeau de marque bleu nuit reste commun ;
les actions de travail utilisent le vert pétrole. Les tokens `--localeo-*`
de `app-header.css` sont la source partagée des applications internes, consommée
également par CRM. Pro et Animation déclinent ces mêmes valeurs dans leurs
tokens locaux, sans dépendance d’exécution entre dépôts.

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
Depuis le 21 novembre, elle adopte la signature publique Marketplace et conserve
sa composition compacte, son carnet, ses tampons, ses tickets et sa navigation.
Voir [LIVE-UX-09](../../produit/live/principes-ux.md#live-ux-09--partager-la-marque-marketplace-avec-une-composition-compacte).

Dans Pro et Animation, conserver les rubriques et raccourcis adaptés au métier,
le retour au contexte précédent, les confirmations et les états de chargement.
La navigation claire distingue la rubrique active avec un fond vert doux et
son repère accessible. Les états succès, attention et erreur restent sémantiques :
un avertissement ne prend pas la couleur de l’action principale. Les contenus
personnalisables d’une animation, dont le flyer, gardent leurs propres couleurs.
Les champs mobiles conservent une taille lisible de 16 px ; le corps de travail
à 14 px ne doit pas réduire les cibles tactiles, la signature ni le zoom du texte.

Les preuves locales et limites sont dans le
[suivi d’harmonisation](../../roadmap/anomalies/backend.md#ano-interne-charte-crm-20261104--harmonisation-des-espaces-de-gestion).

### Iconographie de gestion Pro et Animation

Les deux applications utilisent le même dessin pour une même fonction. Les
silhouettes distinguent en particulier le calendrier de la checklist de
préparation, le scan QR du clavier PIN, les participants de l’équipe et le lot
du coffret. Le registre SVG est livré localement dans chaque application pour
préserver leurs déploiements indépendants.

- Repères métier à 24–32 px : contour et aplat vert pétrole discret, sur la
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
