# E75 — Architecture et contrats

[Décisions](README.md) · [Parcours](parcours-regles.md) ·
[Preuves et livraison](verification-livraison.md).
Conception cible du 4 novembre 2026, selon l’[ADR domaine d’abord](../../architecture/decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md).
Les noms nouveaux ci-dessous sont des contrats à implémenter, pas des API déjà disponibles.

## Existant vérifié et écarts

Lecture du backend à `394a882` et des consommateurs du workspace le 4 novembre.
Les fichiers de code nommés dans ce document restent dans leur dépôt applicatif.
Cette exploration n’a exécuté aucun test ni accédé à une base.

| Producteur ou consommateur | Socle réel | Extension nécessaire |
| --- | --- | --- |
| Backend `app/domaine/animation_locale/moteurs/registre.py` et `services/registre_strategies_modeles_animation.py` | Registres fermés Passeport, Tombola locale, Chasse et Tombola publique | Modèle et stratégie `MOTS_CROISES`, contrat moteur `1.0`, compilation et projections explicites ; pas de repli vers Passeport |
| Backend `app/application/animation_locale/services/worker_generation_animation.py`, `contenu_generation.py`, `generation_animation.py` | Prompt, attente de traitement manuel, import JSON, validation et acceptation, reçus et worker à bail | Schéma de grille fermé, validateur déterministe, candidat versionné ; supprimer les branches « chasse sinon passeport » sur les chemins touchés |
| Backend `services/preparation_accompagnee.py`, domaine `entities/demande_preparation_accompagnee.py` | Accompagnement réservé à la chasse, délai de cinq jours, calendrier, validation terrain | Étendre à E75 explicitement ; approbation de contenu organisateur distincte de l’acceptation technique Localeo |
| Backend `services/publication_commandes.py`, `publication_animation.py` | Version d’agrégat, idempotence, compilation et débit transactionnel | Recontrôle de la grille, des accords, de l’approbation et de l’unité E75 |
| Backend `app/domaine/abonnements_plateforme/catalogue_modules.py`, `droit_module.py`, application `service_souscriptions.py` | Module chasse et unité PUBLICATION_CHASSE ; choix actuel chasse ou ANIMATION | Ajouter module MOTS_CROISES et unité PUBLICATION_MOTS_CROISES ; empêcher toute consommation implicite de crédits standards/chasse, y compris sur souscriptions historiques |
| Backend `services/jeu_animation.py`, `validations_animation.py`, domaine `moteurs/execution.py` | Commandes et attestations versionnées, reçus, sérialisation avec clôture | État de grille, validation irréversible de grille correcte, qualification cumulative et preuve par commerce |
| Backend `services/exploitation_animation.py`, `tirages_animation.py`, `tirages_libres.py` | Gel avec provenance, tirage coffrets et circuits lots libres distincts | Inclure la preuve E75 dans le gel ; adapter bilan sans traiter E75 comme Passeport |
| Animation `src/app/animationEngineRegistry.ts`, `generationContracts.ts`, `components/GenerationPreparationView.tsx`, `App.tsx` | Registre fermé et préparation réservée à la chasse ; API accompagnement et publication réutilisables | Assistant E75, aperçu grille, retours localisés, approbation versionnée, fiches et état de publication |
| Live `src/live/animationEngineRegistry.mjs`, `LiveAnimationGame.jsx`, `gameProtocol.mjs`, `gameDrafts.mjs` | Capacités annoncées, protocole de commandes, reçus 200/202/404 ; brouillons adaptés aux activités chasse | Renderer grille et mode par mot, commandes nouvelles, brouillons bornés spécifiques ; pas de réemploi du champ texte chasse de 80 caractères |
| Pro `src/features/animations/engineRegistry.js`, `contracts.js`, `missionPreparation.js`, `components/AnimationKitSection.jsx` | Scan d’une étape du commerce, reçus d’attestation, kit chasse | Capacité E75, fiche d’indices sans corrigé, accord portant sur sa version. Une étape d’attestation par commerce même si plusieurs définitions |

## Objets et propriétaires des invariants

| Objet / propriétaire dans `app/domaine` | Invariant et opérations |
| --- | --- |
| `animation_locale` : valeur `GrilleMotsCroises` | 5–25 mots, dimensions ≤15×15, mots de 2–15 lettres normalisées, géométrie et connectivité valides. Constructeur/validation pure sans ORM ni fournisseur ; erreurs avec coordonnées/identifiant de mot |
| `animation_locale` : préparation versionnée | Un candidat ne remplace le candidat retenu qu’explicitement. Empreinte de grille, définitions, commerces requis et règles ; toute modification pertinente invalide les approbations |
| `animation_locale` : animation et configuration publiée | Publication seulement après approbation du contenu par organisateur, terrain et accords requis ; définition privée publiée immuable et projection publique distincte |
| `animation_locale` : exécution personnelle | Réponses courantes, version de progression et preuve de grille correcte. Sauvegarder ne qualifie pas ; contrôler valide la grille si entièrement correcte. Après validation, aucune modification de réponse |
| `animation_locale` : politique de qualification E75 | Grille validée ET preuves effectives pour chaque commerce requis ET fenêtre ouverte lors de l’acquisition ; une chance. Recalcul après contrôle et après attestation via la même règle pure |
| `animation_locale` : exploitation/gel | Clôture et commandes coordonnées ; population figée avec version de grille et preuves. Retrait temporaire interdit les nouvelles mutations et le tirage ; reprise identique seulement avant clôture et avant échéance |
| `abonnements_plateforme` : catalogue, droits et consommation | Module/unité E75 propres, paiement confirmé ou octroi tracé, commune/période valides, dernier crédit atomique ; continuité E73 des engagements publiés |

L’application charge les faits autorisés, orchestre l’UoW, appelle ces règles,
persiste et alimente l’outbox. Les API, l’ERP et les batchs ne recalculent pas
eux-mêmes la géométrie, le droit ou l’éligibilité. Les adaptateurs portent SQL,
PDF et stockage privé. Les interfaces affichent les actions autorisées et les décisions
du serveur ; elles ne débloquent pas la publication sur un simple compteur local.
Le contrat de jeu nomme ce champ `actionsAutorisees` ; le suivi de préparation
utilise `allowedActions`. Conserver les noms propres à chaque projection.

## Flux, permissions et transactions

Préparation : `A_COMPLETER → EN_PREPARATION → PRETE`, avec attente de complément,
reprise ou annulation selon le circuit E73. Les statuts de tentative technique
restent distincts (`ATTENTE_TRAITEMENT_MANUEL`, import, contrôle, acceptation).
L’opérateur ERP habilité `animation.gerer` prépare dans son périmètre ; l’organisateur
approuve via ses droits de gestion sur la commune. Un rôle d’achat n’autorise pas
implicitement la validation d’un jeu. Pro et salariés ne voient que leurs indices
et leurs attestations, jamais la solution complète. La réception du lien public
ne donne aucun droit de gestion.

1. **Publication** : même orchestration ERP/Animation, vérification des permissions
   courantes, `expectedVersion` de l’animation (pas `configuration_version`), puis
   verrouillage de l’animation et des lignes de droit/consommation selon l’ordre
   partagé E73. Contrôler toutes les révisions, compiler, débiter et publier dans
   la même transaction. Unicité du reçu et de la consommation par animation/unité.
   Une erreur avant commit ne laisse ni publication ni débit ; réponse perdue
   après commit → lire le reçu. Événements/outbox transactionnels, pas d’envoi direct.
2. **Jeu et passage** : réutiliser l’ordre du service de jeu (coordination de
   l’animation, animation, participant, exécution). Vérifier token, versions et
   horloge serveur sous transaction ; sauvegarde, contrôle ou attestation, calcul
   de qualification et reçu atomiques. Pas de transaction ouverte pendant un
   appel réseau ou une préparation IA. Les mutations refusées ne modifient pas
   la progression. Le dernier passage et le dernier contrôle concurrents donnent
   une seule chance et un seul événement de qualification.
3. **Clôture** : même coordination ; refuser les mutations tardives, préparer
   une population exhaustive à partir de l’état gelé, puis la rendre visible
   atomiquement. Les lots de construction sont repris sans changer la date de
   coupure. Aucun tirage tant que le gel n’est pas complet. Les trois circuits de
   dotation consomment cette population, sans nouveau moteur de hasard.

La correction/révocation autorisée d’une preuve commerçante doit recalculer
l’éligibilité avant gel, sans effacer la preuve de grille correcte. Après gel,
appliquer les règles d’exploitation existantes de contestation, pas une réécriture
silencieuse de la population ou des gagnants. Le retrait temporaire E75 est un
état d’exploitation à ajouter si nécessaire : il ne change ni version publiée,
ni date limite, ni crédit. Une nouvelle édition après annulation possède un nouvel
identifiant et exige un nouveau crédit ou un octroi explicitement motivé.

## Identité, commerce et conditions acquises

Reprendre le contrat d’inscription chasse et non celui d’E74 : prénom, nom,
e-mail, téléphone selon les validations du contrat chasse, acceptation du règlement
versionné et déclaration d’un adulte. `participants_animation.py` normalise
l’e-mail par trim/minuscules et recherche l’unicité dans l’animation ; conserver
ce comportement, sans suppression des alias `+` ni fusion de comptes supposée.
Une inscription doublon n’émet pas de jeton personnel sur la seule connaissance
de l’adresse ; récupération par le mécanisme d’accès existant. Pas de nouvelle
étape de vérification d’e-mail ajoutée par E75.

Prix catalogue 19 000 centimes HT, EUR, durée 12 mois, quota de 5 publications.
Le module suit le terme de la souscription E73 : achat en cours de période avec
prix et quota proratisés, quantité arrondie au supérieur selon la règle existante,
pas de prolongation implicite de la souscription. Essai/cadeau : mécanismes chasse
transposés explicitement à la nouvelle unité (essai un crédit, durée maximale
existante de 14 jours dans le terme ; cadeau borné au terme et quota calculé).
Les limites explicites d’un octroi tracé priment sur ses valeurs par défaut.
Aucune attribution automatique aux clients existants ou au forfait Premium.
Les conditions acquises sont versionnées ; les expirations suivent la continuité
E73 pour les animations engagées, sans autoriser une nouvelle publication.

L’accompagnement conserve les cinq jours ouvrés, qualification de complétude,
attente de complément et calendrier versionné E73. Aucune nouvelle clé fournisseur
IA n’est nécessaire. Les reprises techniques gardent la même demande et ne
consomment pas de nouveau crédit de publication. Le plafond technique de
générations partenaire/mois existant inclut E75 : pas de quota commercial de
« corrections » ajouté au produit. Échecs/coûts sont suivis séparément des usages.

## Contrat de données cible

Les schémas fermés rejettent les propriétés inconnues. Les variantes E75 sont
discriminées par `type=MOTS_CROISES` et `engineContractVersion=1.0`.

| DTO | Champs et bornes essentielles | Exposition |
| --- | --- | --- |
| Brief E75 | thème ≤200 caractères, contexte ≤4000, public/difficulté éditoriaux ≤100 chacun, langue `fr`, mots souhaités ≤25, commerces sélectionnés 1–25, dates/commune par contrat commun | Organisateur/ERP autorisés |
| Candidat/grille privée | `schemaVersion`, largeur/hauteur 2–15, masque de cases, 5–25 entrées `{id, numero, ligne, colonne, direction, reponse, definition, commercantId}` ; coordonnées zéro-indexées ; définition ≤500 caractères ; réponse normalisée 2–15 lettres ; provenance et empreinte calculées serveur | Préparation privée, jamais contrat public |
| Projection publique | type/version, titre/dates/commune, accès Live, modalités, dotation et commerces selon publication ; aucune solution, saisie personnelle ou définition terrain | Catalogue et fiche publique |
| Projection joueur | versions protocole, masque/numéros/directions/longueurs, références des commerces, ses cases saisies, progression, grille validée ou non, passages requis/validés, qualification et actions permises | Accès personnel, `no-store` ; aucune solution distincte de ses propres réponses |
| Projection commerçant / fiche | animation, révision/empreinte, ses définitions/numéros et consignes d’attestation, état d’accord ; une seule étape d’attestation par commerce | Commerce ou salarié autorisé selon action ; pas de corrigé |
| Rapport de contrôle | code, chemin de champ/mot/case, message corrigible ; aucun dump de la proposition dans une erreur publique | Préparation autorisée |

Chaque mot a exactement un commerce d’indice ; chaque commerce retenu porte au
moins un mot. Les commerces des lots peuvent être différents. Un changement de
commerçant ou de fiche invalide l’accord correspondant et l’approbation de
l’organisateur. Les QR imprimés pointent vers Live ou l’accès de passage existant,
jamais vers une API contenant les réponses.

## Commandes et erreurs

Étendre les familles existantes sous leurs préfixes effectivement montés,
sans créer d’API parallèle : `generation_animation_api.py`,
`jeu_animation_api.py`, publication commune et validation Pro/PIN. Les routes
Live `/public/localeo-live/participations/{participation_id}/commandes` et leur reçu
conservent Bearer, `Idempotency-Key` et l’enveloppe versionnée.

Nouvelles actions joueur : `SAVE_CROSSWORD` avec `payload.cells`, liste de
`{row,column,value}` de 225 positions maximum, uniques et non noires ; une lettre
normalisée ou chaîne vide. La liste représente les cases modifiées ; l’omission
ne supprime pas les autres. `CHECK_CROSSWORD` sans réponses dans son payload
contrôle la dernière progression confirmée. Pour une saisie par mot, le client
normalise puis envoie le patch de cellules correspondant ; le serveur revalide
chaque lettre. Pas d’écriture automatique à chaque frappe.

L’enveloppe conserve `engineContractVersion`, `definitionVersion`,
`expectedProgressionVersion`, `expectedExploitationRevision`. Maximum HTTP
16 384 octets ; clé idempotente 8–128 caractères. Même clé/même commande retourne
le même reçu ; même clé/corps différent est un conflit. Une commande perdue ne
change pas de clé. Reçu 202 = en cours ; 404 = résultat non confirmé, pas invitation
à rejouer avec une nouvelle clé. Le client conserve le brouillon et permet une
reprise explicite de la même commande.

Après authentification et contrôle des droits courants, rechercher d’abord le
reçu de la même cible/clé et vérifier l’identité du corps. S’il existe, restituer
ce résultat immuable même si le jeu a été fermé, retiré ou annulé depuis ; aucune
mutation, nouvelle chance ou nouvelle qualification n’est alors créée. Des droits
révoqués ne sont pas rétablis par la présence du reçu. Sans reçu enregistré, une
commande nouvelle ou jusque-là non enregistrée doit satisfaire l’état courant
du jeu et la date limite sous verrou ; elle est refusée après fermeture/retrait.
Le même principe vaut pour les attestations commerçantes et leurs reçus.

Le reçu décrit le résultat au moment de la commande, pas l’état actuel de
l’animation ni de l’éligibilité après une annulation ou une correction de preuve.
Après réconciliation, Live relit la projection courante et ne remplace jamais une
projection plus récente par celle d’un reçu ancien. La preuve de grille reste
consultable dans l’historique ; un nouveau `CHECK_CROSSWORD` après fermeture ou
retrait est refusé, même si la grille avait déjà été validée.

Résultats métier nouveaux à ajouter aux unions : `GRILLE_ENREGISTREE`,
`GRILLE_INCOMPLETE`, `GRILLE_A_CORRIGER`, `GRILLE_VALIDEE`. La qualification est
un champ serveur distinct : `GRILLE_VALIDEE` seule ne signifie pas tirage acquis.
Une sauvegarde ne révèle aucun feedback de justesse. Un contrôle erroné n’indique
ni emplacement ni nombre de lettres correctes. Tant que le jeu est ouvert,
recontrôler une grille validée retourne sa preuve sans nouvel effet métier ;
tenter de la modifier refuse `GRILLE_DEJA_VALIDEE` (409).

Les anciennes entrées `REQUEST_HINT`, `REQUEST_HELP` et
`GET /public/localeo-live/participations/{participation_id}/etapes/{step_id}/resultat`
ne doivent pas permettre d’obtenir une définition terrain ou une solution E75.
Les actions d’aide non prises en charge sont refusées explicitement ; une lecture
de résultat éventuelle reste limitée aux états et propres réponses du participant.

Les autres refus suivent l’enveloppe commune avec code/corrélation : 401 accès
absent, 403 périmètre/droit refusé, 404 cible inaccessible, 409 version obsolète,
jeu fermé/retiré ou quota épuisé selon contrat modules ; 422 grille/cellule/brief
invalide ; 413 corps trop grand ; 429 limitation avec délai de reprise. Réutiliser
les codes existants quand le sens est identique. Les nouveaux codes de retrait
et de grille doivent être ajoutés aux mappings HTTP, pas remonter en 500/CORS.

Approbation organisateur à ajouter à la famille préparation : animation,
`expectedVersion`, révision de préparation, empreinte calculée serveur et
confirmation explicite. Même protocole reçu/idempotence ; une approbation ancienne
ne valide jamais un candidat concurrent. Le précontrôle de publication est
informatif ; tous les invariants sont revérifiés lors de la commande finale.

## Sources de contrats et compatibilité

Producteurs : `app/application/animation_locale/contrats_moteur/` (definition,
generation, commandes, projections et préparation), registres domaine et API.
Le générateur backend `scripts/documentation/export_moteur_animation_contracts.py`
exporte schémas/manifeste/empreintes sans bootstrap ; l’étendre, ne pas fabriquer
manuellement une empreinte. Les OpenAPI documentaires restent dans
[E41](../epic-41-api/openapi.json) et [E42](../epic-42-localeo-live/openapi.json),
générés par `generate_epic41_openapi.py` et `generate_epic42_openapi.py`.

Consommateurs à synchroniser : Animation `src/imports/openapi.json` et
`src/imports/moteur-animation/` ; Live `src/contracts/moteur-animation/` ;
Pro `api/localeo-openapi.json` et `api/moteur-animation/`. Le contrat OpenAPI Pro
utilise son générateur `localeo-commercant/scripts/export-openapi.py`, distinct
des exports documentaires E41/E42 ; ne pas le remplacer par une copie de ceux-ci.
Leurs registres fermés
et tests d’empreintes doivent être étendus ensemble. Aucun export n’est régénéré
pendant cette phase de spécification : il représenterait à tort une API livrée.

Ajouter une variante ne rend pas les anciens clients compatibles. Ils continuent
de déclarer leurs `moteurs_supportes` ; le serveur filtre les catalogues et refuse
explicitement un accès direct incompatible. Live et Pro ne déclarent E75 qu’une
fois renderer, commandes et reçus pris en charge. Clés de cache liées à la version
et aux capacités. Les autres types restent en `1.0`, avec fixtures historiques.

## Persistance et confidentialité

Migration additive à numéro attribué lors de l’implémentation : nouvelle valeur
modèle/module/unité dans les contraintes réellement présentes ; grille privée
versionnée, approbations et lien vers configuration publiée, exécution personnelle
et preuve de grille correcte, indice par commerce et retrait temporaire. Étendre
les tables du moteur lorsque leur contrat le permet ; ne pas créer une seconde
table d’identité ou de tirage. Audit des FKs et règles de suppression : pas de
cascade supprimant une preuve ou un gain pour contourner un conflit.

Unicités : candidat `(animation_id,revision)`, approbation `(animation_id,empreinte,
acteur_id)`, exécution par participation/configuration publiée, consommation par
animation/unité et reçu par acteur/cible/clé. Index de listes et travaux dans le
document de performance. Les empreintes incluent tout ce qui influence le jeu.

Solutions/imports privés : stockage privé et endpoints autorisés seulement ; pas
de réponse IA, de grille corrigée ou de token dans logs, analytics, carnet exporté,
service worker, PDF public ou message d’erreur. Brouillons locaux limités à ses
saisies, indexés par participant et version, expiration 24 h comme le socle Live,
effacés à suppression de l’accès ; jamais synchronisés comme preuve de réussite.
Conservation/purge E55 : étendre explicitement les nouveaux objets et exceptions
de gel, sans nouvel archivage illimité. Restauration isolée vérifie grille privée,
preuves, accès, index et reçus ; aucun envoi réel durant les tests.
