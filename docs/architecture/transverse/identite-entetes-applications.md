# Identité des en-têtes Localeo

## Périmètre

Localeo Pro, Animation, ERP, OnBoard, Live, Ops, Support et Atelier utilisent
la même signature dans leur en-tête principal. Le nom de l’application permet
de se repérer ; ses actions et sa navigation restent adaptées à son public.
Les favicons et icônes d’installation ne sont pas remplacés par cette correction.

## Signature commune

| Élément | Règle |
| --- | --- |
| Fond de l’en-tête | Bleu nuit `#123247` |
| Symbole | SVG Localeo `header-mark.svg`, identique dans les quatre dépôts applicatifs, sans ombre ajoutée |
| Dimensions du symbole | 40 × 40 px ; 36 × 36 px jusqu’à 600 px ; proportions conservées |
| Espacement symbole / texte | 10 px |
| Marque | `Localeo`, blanc, suivie du nom de l’application |
| Nom de l’application | Pro, Animation, ERP, OnBoard, Live, Ops, Support ou Atelier ; orange `#f5ad6e`, sans italique ni séparateur |
| Police de la signature | `system-ui, -apple-system, "Segoe UI", sans-serif` ; graisse 800, interligne 1,15, approche −0,02 em |
| Taille du texte | 1,25 rem ; 1,125 rem jusqu’à 600 px (20 et 18 px à taille de texte standard) |
| Environnement | Conserver le repère TEST ou autre environnement lorsqu’il existe, en capsule discrète blanche ; placé sous le nom sur mobile dans Pro et Live |
| Sous-titre | Aucun sous-titre dans le bloc de marque |

Le symbole porte un texte alternatif vide : le nom accessible du lien ou du
bouton annonce déjà l’application et le retour à l’accueil. Conserver les
destinations existantes et les protections contre l’abandon d’une saisie.

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

Les cinq outils internes du backend partagent `app-header.js` et
`app-header.css`. Pro utilise son `ApplicationFrame`, Animation son shell et
Live un composant `LiveBrand`, réutilisé à son entrée publique. Les copies du
SVG restent locales à chaque application pour préserver leurs déploiements
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
