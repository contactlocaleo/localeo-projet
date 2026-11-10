# Registre des anomalies

## ANO-ANI-CHARTE-CRM-20261104 — Alignement sur la charte de gestion CRM

La palette, la navigation, les composants de formulaire et la hiérarchie
typographique de Localeo Animation sont harmonisés avec Localeo Pro sur la
référence CRM. Le [suivi commun](../../audits/ergonomie-gestion-pro-animation-2026-11-01.md#harmonisation-sur-localeo-crm--4-novembre-2026)
conserve les constats, corrections, impacts et preuves locales. Les transitions,
droits et confirmations d’animation restent inchangés ; aucun déploiement réalisé.

### Correction du 10 novembre 2026 - Focus du sélecteur de commune

- **Observé et cause** : un clic sur « Commune active » affichait un contour
  orange à l'intérieur du champ du bandeau bleu. Reproduction locale sur la
  base Animation `89c7f6e` : Chromium applique `:focus-visible` au sélecteur
  natif même au clic ; la règle commune de `actions.css` ajoutait alors un
  contour ocre de 3 px autour du seul `select`.
- **Correction** : dans `application-frame.css`, le repère de focus est porté
  par le champ complet `.commune-picker`, en blanc sur bleu, sur 2 px. Le
  contour intérieur est retiré dans ce seul contexte. Le clavier conserve un
  repère visible, qui disparaît en quittant le champ ; la sélection native et
  la commande de changement de commune sont inchangées.
- **Preuves locales** : `pnpm typecheck`, `pnpm lint` et
  `node scripts/build-generation-tests.mjs` réussis. Le scénario existant
  `WORKSPACE_CASE=shell` de `animation-workspace-ux.mjs`, complété pour cette
  recette par le clic, Tab, l'ouverture au clavier, Échap et la sortie du
  champ, passe sur dix formats de 320 à 1600 px, paysage et texte à 200 %.
  Styles calculés et absence de mutation vérifiés ; captures PC/mobile
  examinées dans `localeo-animation/tmp/commune-picker-focus/`, non versionnées.
- **Impacts** : CSS de présentation dans Animation et suivi documentaire ici.
  Aucun contrat API, règle métier, droit, migration, générateur de démonstration
  ou paramètre d'exploitation modifié. Version distante non vérifiée et
  déploiement non effectué.

### Correction du 10 novembre 2026 - Alignement des actions des modèles

- **Observé et cause** : dans le catalogue **Modèles**, le bouton « Créer une
  animation » suivait directement le contenu variable de chaque vignette. Une
  description, un badge ou des prérequis supplémentaires décalait donc l'action
  par rapport à la vignette voisine. La reproduction locale sur la base
  Animation `89c7f6e` mesure un écart de 57 px entre deux boutons d'une même
  rangée.
- **Correction** : chaque vignette devient une colonne occupant toute la hauteur
  de sa cellule de grille et son action, disponible ou désactivée, est repoussée
  en bas. Les contenus restent libres de grandir ; les boutons d'une même rangée
  conservent le même niveau. Sur mobile, les vignettes restent empilées.
- **Preuves locales** : le scénario navigateur `leo-assistant.mjs` utilise deux
  contenus de hauteurs différentes et contrôle l'alignement exact à 1280 px,
  ainsi que le parcours et le rendu à 390 px. Le scénario échoue avant correction
  avec les positions `338,44` et `281,39` px, puis réussit après correction. Les
  captures PC et mobile ont été examinées dans
  `localeo-animation/tmp/leo-browser-captures/`, non versionnées.
- **Impacts** : mise en page et test ciblé dans Animation, sans changement de
  comportement, contrat API, règle métier, droit, migration, démonstration ou
  exploitation. Version distante non vérifiée et déploiement non effectué.

### Correction du 10 novembre 2026 - En-tête et navigation du détail

- **Observé et cause** : le détail d'une animation séparait le retour, le nom,
  la commune, les dates et le statut sur plusieurs niveaux verticaux. Sur
  ordinateur, quatre onglets d'espaces étaient suivis d'une seconde rangée de
  sous-onglets de même apparence. Cette hiérarchie consommait de la hauteur et
  rendait les deux niveaux de navigation difficiles à distinguer.
- **Correction** : le contexte de l'animation est réuni dans un en-tête compact,
  sur la même ligne que le retour à la liste lorsque la largeur le permet. Une
  seule barre de navigation présente les quatre espaces **Préparer**, **Piloter**,
  **Communiquer** et **Résultats**, puis un sélecteur libellé pour la rubrique de
  l'espace actif. Sur mobile, le sélecteur groupé unique est conservé. Les droits,
  liens directs, alias, gardes de sortie et chargements différés restent inchangés.
- **Preuves locales** : le scénario navigateur
  `WORKSPACE_CASE=navigation` échoue avant correction sur l'absence du nouvel
  en-tête compact. Après correction, huit formats de 320 à 1600 px, dont le
  texte à 200 %, valident la géométrie de l'en-tête, la barre unique, les cibles
  tactiles, le clavier, les habilitations et l'absence de débordement ou de
  mutation API. Les captures PC, tablette, mobile et zoom ont été examinées dans
  `localeo-animation/tmp/animation-workspace-ux/`, non versionnées.
- **Impacts** : présentation, navigation locale et tests dans Animation ; aucun
  contrat API, règle métier, droit, migration, donnée de démonstration ou
  paramètre d'exploitation modifié. Version distante non vérifiée et déploiement
  non effectué.

## ANO-ANI-HEADER-COMPTE-20261103 — Espace réservé aux rubriques du menu

- **Observé** : dans le shell connecté de Localeo Animation, les documents,
  l’identité, l’organisation, la version et les actions de compte/déconnexion
  occupaient un pied de menu non rétractable, réduisant la hauteur des rubriques.
  Cause confirmée dans `Sidebar` et `.app-navigation__account`, sur la base
  applicative `4116e0e` ; aucune observation de version distante revendiquée.
- **Correction** : déplacement dans le menu « Mon compte et documents » de
  l’en-tête. Identité compacte sur PC, initiales sur petit écran, identité
  complète à l’ouverture. Les documents s’ouvrent dans un autre onglet pour
  préserver la saisie ; l’accès Compte et équipe garde la protection de navigation,
  et la déconnexion appelle le parcours serveur existant. Le menu latéral ne
  conserve que les rubriques. Styles corrigés à la source, règles du pied retirées.
- **Preuves locales** : TypeScript et ESLint réussis ; 297 tests Node réussis,
  aucun ignoré ; build isolé réussi avec avertissement de taille de bundle.
  Le scénario navigateur `WORKSPACE_CASE=shell` vérifie dix formats PC/mobile,
  paysage et texte à 200 %, les bornes de largeur, le clavier et le focus,
  les liens, la garde de saisie et la déconnexion avec API simulée. Captures dans
  `localeo-animation/tmp/pro-alignment/`, non versionnées.
- **Impacts** : présentation seule dans `localeo-animation` et documentation
  dans `localeo-projet`. Réutilisation du contexte déjà chargé par l’en-tête ;
  pas de contrat API, permission, règle métier, migration ou donnée de démonstration
  modifiés. Aucun nouveau paramètre d’exploitation. Déploiement non effectué.

## ALL
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-ANI-01 | inscription | Erreur « Failed to fetch » après « Tout envoyer » dans l’onglet Invitations, alors que les invitations sont bien envoyées et visibles après actualisation. | Corrigé côté interface : vérification de l’état serveur après une perte de réponse, sans nouvel envoi automatique. Validation en environnement réel à effectuer. |
| ANO-ANI-02 | facturation | La demande facturation porte sur un identifiant de commande qui n'est pas disponible (uuid), une demande de facturation doit porté sur une animations (ces lots). Chaque demande doit être consultable pour voir si l'ensemble des factures relatibes aux lots d'animation sont disponible ou sinon il doit être possible de consulter l'état des demandes et de les relancers. Un état général sur le dossier doit permettre de savoir si il est complet (toutes les factures sont recues) ou non | Interface corrigée et testée. Complément backend de relance et de complétude préparé et testé ; autorisation explicite requise pour son application après refus du contrôle automatique. Voir docs/specifications/ano-ani-02-facturation-animation.md. |
| ANO-ANI-03 | Origine API HTTPS explicite obligatoire. lors du build pour déploiement dans Re,der | A corriger |

## Correction du 30 octobre 2026 — découverte publique et carnet Animation

Retour utilisateur sur `test-animations.localeo.city`, confirmé configuré
`LOCALEO_PUBLIC_SURFACE=ANIMATION` par lecture publique de `app-config.js`.
L’accueil spécifique utilisait une liste sans commande de géolocalisation,
un en-tête vert distinct des codes Coffrets, et Live conservait son onglet
Coffrets ainsi que cette rubrique comme destination mémorisée par défaut.

Correction dans `localeo-marketplace` : géolocalisation volontaire via le
service E52 existant, commune réellement résolue et choix manuel préservé ;
identité bleu/orange/papier partagée, filtres avant la mise en avant ; onglet
Coffrets masqué et entrée Live adaptée à la surface ANIMATION. Les données,
liens directs et ajouts Coffrets restent conservés. Aucun changement backend,
de schéma ou de droit, ni migration ou réparation de données nécessaire.

L’extension et l’analyse UX sont rattachées à **E73-EVO-UX-PUBLIC** dans les
[parcours canoniques](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md).
La reproduction initiale constate l’absence du bouton dans le navigateur avant
correction. Les preuves finales et les limites de livraison sont consignées
dans le [suivi](../../specifications/epic-73-animation-et-ou-coffrets/suivi-implementation.md).
Les propositions de confirmation d’inscription et d’immersion du jeu restent
distinctes de cette correction. Aucun déploiement distant effectué.

## Correction du 29 septembre 2026 — icônes PWA

- Attendu : conserver la famille graphique Live/OnBoard sans fond sombre autour du marqueur Animation.
- Cause : `scripts/export-pwa-icons.ps1` ajoutait un fond opaque sombre à tous les exports PWA, alors que le logo source et le favicon étaient déjà transparents.
- Correction locale : exports 192/512 transparents ; Apple 180 et maskable 512 sur fond blanc, avec leurs marges conservées ; fond de lancement du manifeste blanc.
- Preuves : contrôle visuel des exports Apple, dimensions et transparence des quatre exports ; `node --test tests/pwa.test.mjs tests/pwa-lifecycle.test.mjs` (9 succès) ; `node scripts/build-pwa-tests.mjs` réussi, avec avertissement de taille du bundle.
- Impact limité aux ressources statiques et à leur export : aucun contrat API, règle métier, migration ou générateur de démonstration modifié. Déploiement et vérification sur appareils iOS/Android non effectués ; le renouvellement des icônes déjà installées dépend du système.

## Correction du 23 octobre 2026 — descriptions des lots engagés (RM-11-03)

- Attendu : après modification de la description courante d’un modèle, pouvoir relire la description initiale des exemplaires et de la dotation engagés, conformément à [RM-11-03](../../specifications/epic-73-animation-et-ou-coffrets/recette-metier.md#rm-11-03).
- Reproduction : sur le clone isolé, le gestionnaire A1 affecte des exemplaires puis modifie la description du modèle. Le backend conserve correctement les descriptions initiales ; les lignes de stock et de dotation ne les affichaient pas.
- Cause et correction locale : `DigitalPrizeAssignments` et `DigitalPrizeInventory` présentent désormais respectivement `snapshot.description` et `unit.description` lorsqu’elles existent, comme texte React échappé, avec retours à la ligne et mots longs. Aucune description n’est reconstruite depuis le modèle courant.
- Preuves : scénario navigateur rouge avant correction, puis 16 contrôles réussis à 1280/320 px, dont l’absence d’interprétation HTML ; six tests adjacents de contrats et commandes réussis. Build isolé sans configuration opérateur réussi. Vérifications TypeScript et ESLint réussies. Rejeu sur les mêmes objets du clone réussi après installation coordonnée des deux composants : descriptions initiales visibles dans les deux lignes, description courante distincte et snapshots API préservés. Les cinq étapes RM-11-03 sont reliées à des preuves privées figées et contrôlées par empreinte. Aucun commit, push ou déploiement sur TEST partagé.
- Impacts : présentation seule dans Localeo Animation ; API et règle de conservation backend inchangées, sans migration ni réparation de données. Le générateur et ses exports fournissent déjà ces descriptions ; aucun nouveau paramètre d’exploitation.

## Correction du 24 octobre 2026 — auteur du suivi des gains externes (RM-10-03)

- Attendu : relire l’auteur et la date des événements de contact, réponse, déclaration de remise et correction dans le suivi du gain, selon la [recette métier E73](../../specifications/epic-73-animation-et-ou-coffrets/recette-metier.md).
- Reproduction : sur une animation externe dédiée du clone, les quatre événements sont enregistrés par les vrais formulaires. Leur API fournit l’identifiant de l’auteur, mais les lignes de l’historique n’affichent que le type, la date et le motif. La déclaration et sa correction restent correctement conservées côté backend.
- Correction locale : `ExternalGainFollowup` présente désormais `acteur` comme texte React échappé, avec un libellé explicite et des mots longs repliables. L’interface ne reconstitue ni identité ni habilitation.
- Preuves : scénario navigateur rouge avant correction, puis 24 contrôles réussis à 1280/320 px ; parcours adjacent de réponse perdue réussi. Build isolé, TypeScript et ESLint réussis. Après installation coordonnée du seul composant sur le clone, dix contrôles de relecture réussissent à 1280/320 px sur les quatre mêmes événements : auteurs et dates conservés, états inchangés et aucune nouvelle commande métier. Les preuves privées sont figées et contrôlées par empreinte.
- Impacts : affichage seul ; contrat API, règles métier, permissions, migrations et générateur inchangés puisque l’auteur existe déjà dans chaque événement. La réception email externe, la distinction documentaire « Non remis » et l’entrée Localeo en écriture restent des limites distinctes de ce correctif ; aucun nouvel état ni rôle n’a été ajouté.
