# Registre des anomalies

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
