# E73 — Suivi de réalisation locale

Début : **18 octobre 2026**. [Spécification](README.md), [backlog](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md), [matrice des 63 critères et preuves](verification-livraison.md). Objectif : les 38 US, dans les dix lots demandés. Les lignes ci-dessous ne valent pas acceptation tant que les preuves correspondantes ne sont pas enregistrées.

## 1er novembre 2026 — homogénéité de Localeo Animation avec Localeo Pro

**Attendu :** reprendre les principes visuels et de navigation de l’espace
connecté Pro dans Animation. Référence inspectée : Pro **6c7489e** ; application
corrigée : Animation **df71e72 + modifications locales**. Les changements de
clôture et le correctif backend de publication présents dans le workspace sont
préservés. Cette tâche ne modifie pas Localeo Pro ni le backend.

**Écarts établis par comparaison des sources et corrigés :**

| Sujet | Animation avant correction | Alignement livré dans les sources |
| --- | --- | --- |
| Typographie | Plus Jakarta Sans / chiffres Geist et chargement Google Fonts | DM Sans locale avec licence ; titres et corps opérationnels de la même famille. |
| Structure | Barre supérieure blanche, identité dans la colonne de menu | Bandeau bleu commun, identité et commune visibles ; navigation bureau de 224 px. |
| Navigation | Quatorze entrées non regroupées ; menu mobile via bouton dans le header | Trois groupes métier ; trois accès mobiles directs + Plus ; sélection commune liste/détail. |
| Actions | Tailles variables, actions bleues et orange concurrentes, suppression groupée avant création | Socle 44 px, rayon commun, création principale ; suppression groupée dans Autres actions, confirmation conservée. |
| Titres et rubriques | Hiérarchie et sélection propres à Animation | En-têtes, retours, titres, onglets et rubriques de fiche alignés sur les composants opérationnels Pro. |
| Feedback et listes | Palette différente et plusieurs traitements de pagination | Palette sémantique Pro, pagination compacte, focus et annonces conservés. Les tableaux/fiches et filtres responsive existants restent utilisés. |
| Accès compte | Icône Paramètres ouvrant Abonnement | Raccourci explicitement nommé Compte et équipe ouvrant ce parcours. |

Les règles CSS communes sont modifiées à leur source ; le cadre d’application
possède une feuille dédiée et les anciennes règles contradictoires de header
dans les styles mobile/PWA sont retirées. Les polices historiques de la page
publique Pro et ses parcours de prestations/paiements ne sont pas copiés.

**Vérification :** comparaison indépendante de Pro, revue du cadre corrigé,
tests navigateur avec API synthétiques et inspection des captures. Deux écarts
détectés pendant la recette sont corrigés : le bandeau au zoom 200 % et le
menu dont le pied de compte comprimait les rubriques. Le panneau mobile défile
désormais entièrement, avec titre de navigation compact et fermeture accessible.
Le contraste Installer sur le bandeau bleu est corrigé avec le mode sombre
existant du composant PWA. Installation et mise à jour sont testées ensemble.
Le banc Abonnement a aussi détecté une confirmation partiellement masquée
au zoom 200 % : la marge de défilement supplémentaire du cadre est retirée,
en conservant le focus et le défilement du composant de confirmation. Le
parcours d’achat rejoué passe ses **128 assertions sur quatre formats**.

Les rapports et captures restent sous `localeo-animation/tmp/pro-alignment/`
et dans les répertoires temporaires des bancs existants. Contrôles exécutés :

- Types TypeScript et ESLint : succès ; **295 tests Node réussis**, aucun échec
  ni skip (`tmp/pro-alignment-unit.log`).
- Builds isolés de l’application et de la PWA : succès, sans configuration
  opérateur ; police locale incluse dans le bundle.
- `animation-workspace-ux.mjs` : **40 parcours** d’espaces métier, puis
  **8 parcours** de rubriques (`WORKSPACE_CASE=navigation`) réussis.
- `WORKSPACE_CASE=shell` : **8 parcours** du cadre de 320 à 1600 px, dont
  texte 200 %, réussis : destinations conservées, garde annulant la navigation,
  historique, focus, menu défilant, sélection du détail et PWA simultanées.
- `workspace-primitives.mjs` : **188 contrôles** ;
  `feedback-consistency.mjs` : **220 contrôles** ;
  `list-pagination-ux.mjs` : **20 parcours** ;
  `finance-workspace-ux.mjs` : **187 contrôles**, tous réussis.
- `account-app.mjs` : **126 assertions** réussies, notamment récupération,
  invitations et changement de compte avec reprise de déconnexion.
- `modules.mjs` : **994 assertions sur 70 scénarios** réussies (achat,
  renouvellement, modules actifs, facturation, consentements, conflits et
  réponses perdues), dont le parcours d’achat ciblé cité plus haut.
- Vérification documentaire : **96 guides, 1 130 liens**, zéro erreur ni
  avertissement ; **132 sources exportées** vérifiées. `git diff --check` propre.

Les effectifs des bancs ne sont pas des critères d’acceptation supplémentaires.
Le smoke historique `mobile-smoke.mjs` reçoit le nouveau libellé de menu,
mais n’a pas été exécuté dans cette tâche ; les nouveaux parcours intégrés
couvrent cette navigation. Les contrôles utilisent Chromium local et des API
simulées, sans prétendre couvrir tous les navigateurs ou les données de TEST.

**Impacts :** présentation Animation et documentation canonique seulement.
Aucun contrat API, invariant métier, schéma, migration, variable d’exploitation
ou jeu de démonstration à modifier. Les données de recette sont synthétiques ;
la navigation ne déclenche aucune commande métier. Les adaptations au contexte
organisateur sont explicites dans la [spécification](perimetres-parcours-saas.md#référence-ux-commune-pro--animation--1er-novembre-2026).
Aucun commit, push ou déploiement effectué ; les preuves locales ne constituent
pas une validation de la version actuellement servie sur TEST.

## 1er novembre 2026 — refus de publication masqué par une erreur 500/CORS

Signalement sur `test-gestion-animations.localeo.city`, POST vers
`test-backoffice.localeo.city/protected/animation-locale/animations/{id}/publier`.
La trace fournie porte `LOC-f1a4c67b-cdf9-4194-a5f5-420e7bbb735b`,
`ErreurModules`, le 1er novembre à 16:43:41 UTC. La santé distante et le HEAD
local indiquent le backend **590e38b** ; le correctif ci-dessous reste local.
Les travaux non commités de clôture sont préservés.

**Cause démontrée.** `ErreurModules` porte un code et un statut métier, mais
la publication du portail n’avait pas de gestionnaire pour cette exception.
Elle arrivait au gestionnaire générique 500 ; cette réponse, produite en dehors
du middleware CORS, n’avait plus les en-têtes autorisant le portail à la lire.
L’origine est déjà autorisée sur TEST : prévol avec `X-Animation-CSRF` réussi
(200), lecture de session sans connexion refusée (401) avec CORS correct.
Aucune publication réelle n’a été rejouée pour diagnostiquer l’incident.

**Correction.** Le gestionnaire HTTP conserve désormais `ErreurModules.status`
et son `code`, avec corrélation et absence de cache. La frontière du moteur
ERP intercepte également cette classe avant `ValueError`, qui la transformait
en 422 générique. Pour une autre exception inattendue après admission du
transport navigateur Animation, le gestionnaire 500 réutilise uniquement la
politique CORS déjà validée ; réponse générique, `no-store`, origines refusées
et absence d’accès au cookie administrateur conservées.

La souscription, l’acquisition du module, sa disponibilité et le quota restent
contrôlés par leurs propriétaires au moment de la publication, sous transaction.
La trace tronquée ne donne pas le code précis du refus TEST : aucun quota épuisé,
module absent ou défaut de configuration n’est déduit du seul nom d’exception.
Le correctif rend ce motif accessible ; il ne transforme pas un refus légitime
en publication ni ne modifie les droits du client.

**Preuves.** La reproduction avec la pile réelle de middlewares et la route
de publication échoue avant correction : sept refus typés deviennent 500,
et un 500 technique perd CORS (**8 échecs, 5 réussites**, rapport
`tmp/e73-publication-modules-before.xml`). Après correction, **122 tests
réussissent**, sans skip (`tmp/e73-publication-cors-after.xml`) : refus modules,
500 générique sans fuite, origine publique/inconnue/nulle refusée, transport
historique sans nouveaux credentials, sessions/CSRF et publication.
Les **14 tests API**, dont trois nouveaux refus ERP 403/409/422, passent
(`tmp/publication-erp-erreurs-modules.xml`) ; ces effectifs se recouvrent.

La suite publication existante a révélé un test dépendant du calendrier : sa
date de fin au 31 octobre est passée au jour de l’exécution. Son horloge est
figée au 15 octobre, sans retirer le contrôle réel ; les **43 tests** concernés
passent (`tmp/publication-metier-horloge-stable.xml`). Une revue indépendante
confirme le maintien des origines, des droits et des contrôles métier.

Les **643 contrôles complémentaires** d’architecture, de couverture des cas
d’usage, d’observabilité et de contrats des modules passent sans skip
(`tmp/e73-publication-architecture.xml`).

**Impacts.** Backend et ce suivi documentaire uniquement pour ce correctif.
Le format d’erreur existant `detail/code/correlationId/request_id` est conservé ;
les consommateurs peuvent lire le refus sans modifier leur transport.
Aucune migration, donnée à réparer, variable, modification du générateur ou
nouvelle origine CORS. Déployer le backend corrigé avant de rejouer depuis
le portail ; vérifier le reçu existant avant une nouvelle commande si son
résultat est incertain. Le succès d’une publication de cette animation TEST
n’est pas attesté. Aucun commit, push ni déploiement effectué dans cette tâche.

## 1er novembre 2026 — clôture fondée sur les tests

**E73-DEC-CLOTURE-TESTS**, décision explicite de l’utilisateur : les conditions
de clôture sont les tests ; pilote, validation humaine et opérations d’activation
sont suivis séparément. L’epic est **Terminée** après la revue des 63 critères et
extensions, avec preuves exécutées/réutilisées, versions et limites détaillées
dans le [bilan unique](verification-livraison.md#revue-technique-du-1er-novembre-2026).
Les constats historiques « En cours » ci-dessous décrivent leurs dates propres.

Deux défauts de harnais corrigés : requête authentifiée réelle du catalogue ERP
(et refus sans lecture pour trois autres rôles), puis banc SaaS aligné sur le
guide Assistant sans perdre ses neuf contrôles. La revue CA-63 ajoute une
preuve intégrée de véritable dump/restauration E73, journal externe,
effacements/révocations, refus de réouverture avant purge, reprise idempotente
et accès après restauration. Elle passe avec SCRAM et rejoint le job PostgreSQL.
Aucun code applicatif n’a dû être modifié pour obtenir ces résultats.

Les preuves renouvelées incluent 123 tests PostgreSQL, deux tests de compteurs
d’import, dix scénarios du générateur/restauration au schéma v285, le nouveau
test intégré CA-63, 623 contrôles d’architecture, les suites domaine/API et les
parcours Animation, Live et contrats Pro. Les effectifs se recouvrent : le bilan
les présente par suite, sans total artificiel. Tous les clusters créés pour
cette revue sont arrêtés ; rapports conservés hors Git dans les applications.

La recette historique conserve **40/130 scénarios entièrement validés et 90
partiels**. Aucune nouvelle recette hébergée, réception fournisseur, validation
pilote ou mesure RPO/RTO n’est inventée. Aucun commit, push ni déploiement par
cette clôture ; les lots proposés et prérequis d’activation sont dans le bilan.

## 31 octobre 2026 — configuration Chasse guidée par les validations

Demande : réduire l'accumulation de blocs et rendre explicites l'ordre, les
actions de validation et les étapes acquises. Bases Animation **f21e4fe** et
Projet **607e27c**, travaux locaux précédents conservés. Deux reproductions
échouent avant correctif : aucune coche **Validée** malgré les contrôles serveur
validés, et cinq groupes de paramètres visibles simultanément.

Configuration devient un parcours de cinq étapes : Parcours, Organisation et
lots, Commerces, Terrain, Publication. Une seule étape est visible, avec son
état, sa consigne et les contrôles utiles ; les détails sont dépliables. Le
bouton de relecture confirmée poursuit vers Organisation, avant les commerces.
Les paramètres se saisissent en quatre sous-étapes, sans enregistrement lors
de la navigation. Les lots attendent la confirmation des paramètres modifiés.
Le bandeau générique d'action suivante laisse place à la continuation du guide
pendant cette configuration, avec les actions générales accessibles ailleurs
dans la fiche. Les étapes visitées restent montées : saisies, confirmations et
vérification des reçus sont conservées.

`useHuntPreparationProgress` partage une seule lecture d'avancement entre le
guide et ses contrôles. Les coches exigent les contrôles serveur tous `VALIDE` ;
un total nul, une lecture indisponible, une visite ou une saisie ne les produit
pas. Les réponses tardives sont ignorées. Les blocages généraux restent
accessibles même lorsque tous les contrôles de rubrique sont valides. La
confirmation terrain de l'édition est déplacée de Parcours vers Terrain,
actualise les validations après succès et partage le verrou de navigation avec
la préparation QR. Une commande incertaine empêche d'engager l'action sœur.

Preuves locales, API synthétiques et réseaux externes bloqués :

| Vérification | Résultat |
| --- | --- |
| Suite Node, dont présentation des états et liens entrants | **269 tests réussis** |
| `hunt-parameters-guidance.mjs` : quatre largeurs/zooms, commande complète, saisies, reçus et champs cachés | **224 contrôles réussis** |
| `hunt-guided-workflow.mjs` : validations serveur, navigation, brouillons, erreur/chargement et blocages à 100 % | **3 parcours, 78 contrôles réussis** |
| `hunt-preparation.mjs` : parcours complet, paramètres, invitations, QR, terrain, publication et réponses perdues | **288 contrôles réussis** |
| `hunt-progress.mjs` : lecture unique, contexte, réponses tardives et absence de fausse progression | **114 contrôles réussis** |
| `assisted-preparation.mjs` : service et confirmation terrain, révision et droits révoqués | **18 scénarios, 234 contrôles réussis** |
| `animation-status-alerts.mjs` : maintien du contexte après préparation, deux modèles et sept statuts | **70 écrans réussis** |

Types, lint et build isolé réussis. Captures bureau/mobile et 320 px avec texte
à 200 % inspectées. Les tests historiques sont adaptés à l'oracle demandé
(étapes numérotées avec `aria-current=step`, contrôles dans le guide et nouveau
point de continuation), en conservant leurs assertions de versions, corps,
quantités, droits, absence d'écriture à la navigation et reprise sans doublon.
La revue indépendante a identifié le verrou croisé QR/terrain, corrigé puis
couvert dans les deux sens, y compris réponse perdue et reçu confirmé.

Impacts : interface Animation et spécification canonique E55-UX-09/10 et E73.
Aucune règle métier, route, DTO, migration, donnée de démonstration ou
configuration d'exploitation ne change ; backend, ERP, Live, Pro et marketplace
ne nécessitent aucun changement pour ce guidage. Les tests backend ne sont
pas rejoués pour cette présentation des contrôles existants. Aucune action
sur TEST, aucun commit, push ou déploiement.

## 31 octobre 2026 — alertes contextualisées selon le statut de l'animation

Défaut : une animation clôturée affichait encore **Statut non publiable** et
**Date fin passée** comme points à corriger. Bases Backend **41bb279**,
Animation **f21e4fe**, Projet **607e27c**, travaux locaux précédents conservés.
La reproduction avant correction produit **21 échecs backend** et **6 échecs
Node** : le diagnostic de publication était projeté sans tenir compte des
étapes déjà marquées sans objet, avec une jauge de préparation encore active.

Les projections Assistant et Avancement ne présentent les contrôles avant
publication qu'en `BROUILLON`/`CONFIGUREE`. Les cinq autres statuts donnent un
suivi informatif, des étapes de préparation sans anciens messages et aucune
jauge. Le portail s'appuie sur `PUBLICATION.NON_APPLICABLE` et
`NON_MODIFIABLE`, y compris face à une ancienne réponse contenant encore des
erreurs. L'accès au suivi est conservé. Les contrôles bruts, les transitions,
les droits et les alertes de tirage/gains/incidents restent inchangés.
Les écrans Configuration Passeport et Chasse cessent aussi d'afficher le
bilan avant publication après cette phase.

Preuves locales : **79 tests backend ciblés réussis**, dont **62** sur
Assistant/Avancement (sept statuts, API protected/internal, lecture sans
mutation), et **623 contrôles d'architecture réussis**. **264 tests Node
réussis**, types, lint et build isolé réussis. Le banc
`assistant-guidance-ux.mjs` passe **44 scénarios** à 1600/390/320 px, dont
texte à 200 %, absence des anciens diagnostics dans les détails, clavier et
navigation sans écriture ; `hunt-progress.mjs` passe **114 contrôles**.
Captures mobile et texte agrandi inspectées.
Le banc intégré `animation-status-alerts.mjs` valide **70 écrans**, soit les
configurations et workflows des deux modèles sur les sept statuts à
1280/390 px, ainsi que la rubrique Publication des chasses. Il vérifie par
le réseau l'absence de contrôle avant publication hors préparation et la
conservation des alertes de tirage/remise. `hunt-preparation.mjs` passe
**276 contrôles** : le parcours de publication, sa réponse perdue et son reçu
restent fonctionnels. Les composants de publication restent montés lors du
changement de statut pour conserver leur accusé ou la vérification d'un reçu ;
leurs anciens contrôles sont remplacés par le suivi informatif. Une réponse
de lecture tardive ne peut rétablir les diagnostics devenus sans objet.

Contrôle PostgreSQL complémentaire sur une base locale jetable : **7 succès,
1 échec préexistant** dans
`test_publication_validation_readonly_postgres.py::test_refus_tardif_apres_debit_ne_commit_aucun_quota`.
Sa fixture UoW ne fournit pas `reversibilite`, désormais demandé par la commande ;
elle échoue avant d'atteindre le scénario de débit. Ce test et le service de
publication ne sont pas modifiés par ce correctif. Les trois variantes du
diagnostic brut conservent bien `STATUT_NON_PUBLIABLE` sans commit ; les tests
de financement conservent aussi le refus `DATE_FIN_PASSEE`. Le premier appel
PostgreSQL, sans l'option dédiée du runner, a ignoré les huit tests ; seul le
rejeu avec `--postgres-test-url` est compté ci-dessus.

Impacts : backend, portail Animation et présente spécification ; aucun
changement des schémas, règles métier, migrations, données de démonstration,
secrets ou configuration d'exploitation. ERP partage les projections de
lecture ; Live, Pro et marketplace ne consomment pas ces diagnostics de
préparation. Aucune mise en production ni modification de TEST.

## 31 octobre 2026 — pagination et navigation des listes moins textuelles

Demande : alléger les commandes de navigation des listes du portail Animation.
Bases Animation **f21e4fe**, Projet **607e27c**, avec correctifs locaux précédents
conservés. La reproduction sur `JourneyPagination` échoue avant correction :
le bouton affiche encore « Suivante — validations » au lieu d'un pictogramme.
Les implémentations de pagination et leurs libellés étaient répétés dans les
listes, imports, préparations, campagnes, lots et historiques.

`ListPagination` et `ListPageButton` portent désormais la présentation commune.
Les flèches remplacent les longs textes ; la position devient **1 / 3** quand
le total est connu et **1** pour une page à curseur sans total. Retour au début,
page précédente/suivante et ajout de résultats ont des pictogrammes distincts.
Les noms accessibles historiques et les infobulles gardent le sens des actions,
avec cibles d'au moins 44 px, focus visible et boutons natifs désactivés.
Les callbacks, promesses retournées, conditions de chargement, filtres et
curseurs restent inchangés ; aucun faux bouton de dernière page n'est ajouté.

Le raccordement couvre les listes globales et leurs sélecteurs, préparations,
imports, bilans/comparaisons, positions des gains, campagnes, actualités,
lots/bons numériques, lots/gains libres, équipe/organisations, modules et audit.
Les parcours de création et les actions métier conservent leurs libellés et
leurs confirmations. Les feuilles CSS restent inchangées : la présentation
est définie une seule fois dans les composants communs.

Preuves ciblées : **20 parcours navigateur** des cinq variantes de pagination,
à 1280/390/320 px dont texte à 200 %, avec clavier, bornes, attente, clics
répétés et absence de soumission de formulaire. **258 tests Node réussis**,
aucun ignoré ; types, lint et build isolé de l'application réussis. Captures
bureau et texte agrandi inspectées. Deux revues indépendantes ont contrôlé
callbacks, bornes, retours de promesse et distinction des curseurs ; les deux
retours textuels de l'équipe repérés en revue ont été harmonisés.

Vérifications des consommateurs, API synthétiques et réseau externe bloqué :

| Banc navigateur | Scénarios réussis | Contrôles comptés par le banc |
| --- | ---: | ---: |
| `list-pagination-ux.mjs` | 20 | bornes, clavier, attente, cibles et clics répétés |
| `global-read.mjs` | 4 | 60 |
| `animation-read-filter-ux.mjs` | 16 | recherche, pagination et contexte de sélection |
| `campaigns.mjs` | 36 | 684 |
| `assisted-preparation.mjs` | 18 | 234 |
| `dotation.mjs` | 40 | 448 |
| `digital-prizes.mjs` | 12 | 116 |
| `organisation-access.mjs` | 56 | 388 |
| `modules.mjs` | 70 | 994 |
| `saas-journey.mjs`, ciblages `global`, `comparison`, `support` | 12 | 138 |

Soit **284 scénarios navigateur réussis** sur ces parcours. Le contrôle de
comparaison a aussi révélé un débordement à 320 px/texte à 200 % du bouton
**Nouvelle édition** ; sa largeur et son retour à la ligne sont corrigés à la
source, sans modifier sa garde de navigation. Le même scénario passe ensuite.
Le premier lancement Organisation a échoué techniquement lors d'une capture ;
la relance identique réussit. Le banc des lots numériques signale des sélecteurs
commerçants non simulés, sans requête externe ; il ne prouve pas ces lectures.

Limite distincte : la suite SaaS complète s'arrête sur le premier scénario
Assistant, qui attend neuf éléments `ol > li` et en trouve huit. Le même échec
est reproduit dans un banc ignoré injectant `JourneyUi.tsx` depuis `HEAD`, sans
la nouvelle pagination. Cette dette de test préexistante n'est ni masquée ni
affaiblie ; les douze scénarios SaaS ciblés ci-dessus ont été exécutés
séparément. Le débordement de Nouvelle édition a également été reproduit avec
les sources `HEAD` avant correction. Documentation : liens sans erreur ni
avertissement et 130 sources exportées vérifiées.

Impacts : portail Animation et documentation E73. Aucun changement de contrat
API, règle métier, permission, migration, donnée, générateur ou configuration
d'exploitation ; Pro, Marketplace et backend ne sont pas modifiés pour cette
demande. Statuts de roadmap conservés. Pas de recette hébergée, commit, push
ou déploiement effectué.

## 31 octobre 2026 — Validations : recherche et choix de l'animation

Demande : rendre la recherche et la sélection d'une animation intuitives sur
la page **Validations** du portail Animation. Bases Animation **f21e4fe** et
Projet **607e27c**, avec changements locaux ; travaux précédents conservés.
La reproduction navigateur constate le choix masqué dans un `details`, une
recherche à soumettre puis une longue liste de boutons. Le nouveau contrôle
visible attendu est absent avant correction. Ce parcours est partagé avec
**Participants**, qui bénéficie du même correctif.

Le choix **Animation** est désormais visible et ouvre un sélecteur recherchable.
La recherche serveur par nom est temporisée de 250 ms ; elle charge au plus
une page de 25 éléments et commence à l'ouverture seulement. Référence et
période distinguent les résultats homonymes. Une sélection applique le filtre
et ferme le sélecteur ; le nom et la référence restent affichés. L'action
**Toutes les animations** retire directement ce filtre. Recherche, sélection
et pagination des validations restent distinctes. Réinitialisation, clavier,
Échap, retour du focus, attente, absence de résultat et nouvelle tentative
après erreur sont conservés ou explicités. Les réponses obsolètes sont écartées.

La vérification à 320 px et texte agrandi révèle aussi une mauvaise utilisation
du tableau mobile : la date était prise pour une case de sélection et les
colonnes précédant le nom du participant disparaissaient. Une option explicite
`mobileSelectable=false` conserve ces colonnes et retire les faux contrôles
de sélection des lectures globales, sans modifier les valeurs par défaut des
autres tableaux. Leurs contrôles réels de sélection restent testés.

Preuves locales : **16 scénarios navigateur du sélecteur** à 1280/390/320 px,
dont texte à 200 %, et **4 scénarios Participants/Validations** avec leurs
60 contrôles. Composants et transport HTTP réels, API synthétique locale et
réseau externe bloqué ; aucune écriture. **254 tests Node réussis**, aucun
ignoré, types, lint et build isolé de l'application réussis. Captures inspectées
sur bureau, mobile et texte agrandi ; revue indépendante sans défaut bloquant.

Périmètre : portail Animation et documentation E73. Réutilisation des composants
et styles existants, sans surcharge CSS globale. Contrats API, permissions,
contexte de commune, calculs métier et données inchangés : le filtre utilise
les lectures existantes. Aucun impact sur migrations, générateur, configuration
d'exploitation, Pro, Marketplace ou statuts de roadmap. Aucune recette hébergée,
opération de commit, push ou déploiement réalisée pour ce correctif.

## 31 octobre 2026 — suppression d'un participant : dépendances moteur

Anomalie signalée : `RestrictViolation` sur
`animation_executions_participant_id_fkey` lors de la suppression d'un
**participant**. Bases Backend **41bb279**, Projet **607e27c**, avec correctif
local ; la version hébergée concernée n'est pas identifiée. Cause reproduite
sur PostgreSQL 18 jetable : le repository supprimait les messages puis le
participant, sans retirer son exécution. Les cas inscription et chasse
échouent sur la FK restrictive du moteur ; le cas sans exécution réussit.

Le repository retire désormais tentatives et effets, étapes, puis exécution
avant le participant, dans la même transaction et sous le verrou existant.
Les cascades conservent leur responsabilité sur tokens, validations et mesures.
Les contraintes restrictives, reçus, preuves de tirage, populations figées et
gains restent conservés. La règle ARB-60, les contrôles de tenant et de droit,
le verrou animation et l'audit sans données de contact restent inchangés.

Preuves ciblées : suppression sans exécution, inscription et chasse avec
preuve, tentative et effet ; conservation d'un autre participant, des reçus,
de l'animation et de sa configuration ; rejeu introuvable. Les migrations
v241/v242/v283 sont appliquées dans les fixtures PostgreSQL : les compteurs
participants, validations et progression passent de deux à un. Les messages
et les diffusions en attente/incertaines sont nettoyés sans perte des totaux
historiques. Une FK de population figée provoque un refus qui restaure
messages, compteurs, exécution, étapes, tentatives et effets. Les refus
applicatifs population figée et gain disposent de cas distincts.

Validation finale : **99 tests ciblés réussis**, aucun ignoré, via
`scripts/validation/test_isolated.py --postgres-test-url` sur une nouvelle
base locale jetable. Groupes : messages organisateur, exécution chasse,
moteur, conservation PIN et SaaS Live, compteurs v283, performance messages,
service participants, repositories Animation et accès API. La fixture de
conservation PIN inclut désormais la table des gels SaaS requise par le
nettoyage des reçus ; ses huit tests passent. Les imports des fixtures
consommatrices ont été adaptés. **623 contrôles d'architecture réussis**
avec le groupe prescrit par la matrice transverse. Documentation : liens
sans erreur ni avertissement et **130 sources exportées vérifiées**.

Impacts : backend et spécifications canoniques EPIC 41/E73. Aucun changement
du contrat HTTP ni des consommateurs Animation, Live, Pro ou Marketplace ;
aucune migration nouvelle, reprise de données ou configuration d'exploitation
nécessaire, car le schéma existant suffit. Le générateur de démonstration
reste inchangé : le défaut est dans la suppression, pas la génération des
participants. Roadmap inchangée. Aucune suppression sur TEST, recette hébergée,
opération de commit, push ou déploiement réalisée pour ce correctif.

## 31 octobre 2026 — assistant : alertes identifiables par couleur et pictogramme

Demande : rendre les alertes et avertissements immédiatement reconnaissables.
Bases Animation **0d45d5e**, Projet **83a7738**, correctifs locaux précédents
conservés. Cause : toute la synthèse utilisait le même fond ambre, tandis que
les lignes ne distinguaient leur gravité que par le texte. La reproduction
navigateur constate **un seul fond pour trois types**, au lieu de trois repères.

Chaque point possède désormais son fond, son liseré et son pictogramme :
rouge/alerte pour un blocage, orange/triangle pour un avertissement,
bleu/information pour un point commun informatif. Les libellés explicites
conservent le sens sans perception des couleurs ; les icônes décoratives
restent masquées aux lecteurs d’écran. Une erreur de lecture bénéficie aussi
du repère rouge tout en conservant `role=alert`. Les styles sont modifiés à
leur source, sans nouvelle couche globale ni changement de classement.

Preuves locales : **24 scénarios Assistant** réussis à 1600/390/320 px,
dont texte à 200 %, blocage/avertissement/information ensemble, trois formes
distinctes et contraste calculé des messages et libellés **≥ 4,5:1** sur leur
fond effectif. Le test de reproduction passe après correction. Les quatre
parcours Assistant dans l’application complète passent également, sans écriture
API. Captures inspectées sur bureau, mobile et texte agrandi. Types, lint,
build isolé et **253 tests Node** réussis, aucun ignoré.

Périmètre : portail Animation et documentation E73. Aucun changement de
contrat API, gravité métier, règle, migration, générateur ou configuration ops :
la couleur présente la catégorie déjà calculée par le rendu, sans ajouter de
blocage. Backend, Pro et Marketplace inchangés ; statuts de roadmap conservés.
Recette hébergée non exécutée ; aucun commit, push ni déploiement effectué.

## 31 octobre 2026 — assistant : points communs et actions sans répétition

Demande : éviter les alertes répétées, notamment l’échéance de réponse des
commerçants, et rendre l’assistant plus accessible. Bases Animation **0d45d5e**,
Projet **83a7738** ; correctif local précédent de navigation conservé.
Cause confirmée par lecture du producteur : `projeter_assistant` rattache
`DATE_LIMITE_REPONSE_COMMERCANTS_INVALIDE` à DATES, COMMERCANTS et PUBLICATION,
puis expose le code dans la synthèse de publication. Le frontend rendait
séparément chacune de ces listes. La reproduction navigateur échoue avec
**3 occurrences du même message pour une seule attendue**.

La présentation regroupe désormais chaque point dans une synthèse, avec sa
gravité serveur, un accès principal et les autres rubriques concernées à la
demande. Les codes et leurs représentations textuelles connues sont rapprochés ;
les textes distincts et contrôles inconnus restent conservés, sans rapprochement
approximatif. Le message ne réapparaît pas dans les étapes dépliées. Une prochaine
action déjà entièrement couverte par cette synthèse n’est pas dupliquée ; les
autres étapes, statuts, intervenants, aides et accès Support restent accessibles.
Les compteurs sont explicitement des **étapes**, distinctes des points uniques.

Pour une chasse, le raccourci Dates ouvre directement **Configuration →
Organisation et lots** via `preparation=organisation`. Ce choix de rubrique
n’ouvre pas le financement et ne prouve aucun paiement ; les retours de paiement
restent distincts. Les gardes de navigation et toutes les validations serveur
sont conservés. Le propriétaire du contrôle d’échéance reste
`PolitiqueParticipationPublicationAnimation` ; la publication recharge et
revérifie ses faits. Aucun calcul de validité de date n’est ajouté à l’assistant.
Les alertes utiles aux validations de chaque autre parcours restent présentes.

Preuves locales : **20 scénarios navigateur Assistant** réussis à 1600/390/320 px,
dont texte à 200 %, messages communs et distincts, aides, Support, états prêt/
attente/refus puis reprise, clavier et absence de toute mutation ou stockage.
Les **253 tests Node** passent, aucun ignoré, dont les nouveaux contrôles de
regroupement et de distinction entre ouverture Dates et retour de paiement.
Les **276 contrôles** de préparation intégrée passent à 1280/390 px, dont accès
direct au champ de date, financement fermé et absence de commande par navigation.
Les **40 parcours** voisins d’espaces/tableau de bord et **8 parcours** de
navigation groupée passent également. Types et lint réussis ; build isolé réussi
avec avertissement non bloquant Vite sur le chunk principal, environ 500,1 kB.
Captures inspectées sur mobile, bureau et texte agrandi. La revue indépendante
a fait préserver l’aide et le badge de la prochaine étape, et cette aide est
exercée au navigateur. Fixtures synthétiques, sans configuration opérateur.

Périmètre : portail Animation et documentation E73. Aucun changement de règle
métier, contrat API, schéma, migration, générateur ou configuration ops : seul
le rendu et le choix de rubrique évoluent. Backend, Pro et Marketplace inchangés ;
pas de tests backend rejoués pour cette présentation. États de roadmap conservés.
Recette hébergée non exécutée ; aucun commit, push ni déploiement effectué.

## 31 octobre 2026 — navigation de la fiche Animation sans défilement horizontal

Demande : rendre toutes les rubriques accessibles dans la largeur disponible
et réduire le nombre d’onglets simultanés. Bases Animation **0d45d5e**, Projet
**83a7738**. Cause démontrée : une rangée de 14 boutons, 15 avec Actualités,
combinait `whitespace-nowrap` et `overflow-x-auto`. À 1600 px, le test mesure
**1430 px de contenu pour 1390 px disponibles** et échoue sur le dépassement.

`AnimationDetailNavigation` remplace cette rangée par **Préparer, Piloter,
Communiquer, Résultats**, avec au plus quatre sous-rubriques visibles. Grille
et libellés reviennent à la ligne sans masquer de contenu ni créer de zone
défilante. Icônes, libellés et états actifs restent associés. Le mobile garde
un seul sélecteur, organisé par groupes. Le groupe actif dérive de la rubrique,
sans nouvelle variable d’URL ni mémorisation distincte ; les changements passent
par `selectTab` et son garde existant. Le chargement différé est contenu dans
la zone de travail afin de conserver navigation et actions visibles.

Preuves locales : la reproduction passe après correction. Les **8 parcours
navigateur** dédiés passent à 768/1024/1280/1600 px et sur mobile 390/320 px,
dont texte à 200 % à 1280 et 320 px. Ils contrôlent les quatre groupes,
sous-rubriques, géométrie interne, cibles de 44 px, ordre Tab, activation Entrée,
focus dans la navigation ou le titre de destination, chargement différé retenu
par une barrière de test, Action suivante, ancien alias, rechargement et
habilitation Actualités présente/absente. Refuser la sortie d’objectifs modifiés
conserve groupe, rubrique, URL et saisie ; un garde annulé sans dialogue est
également respecté. Aucune écriture API dans ces scénarios.

Les **40 parcours** existants de tableau de bord et rubriques passent, ainsi
que la création/dotation (2 scénarios, 24 contrôles), l’accès Flyer depuis la
liste (1280/320 px) et la clôture avec confirmation (1280/390 px). Types, lint,
build isolé et **249 tests Node** réussis, aucun ignoré. Captures inspectées
à 768/1600 px et texte agrandi à 1280 px ; tests avec données synthétiques,
sans configuration opérateur ni accès aux services réels. La revue indépendante
ne relève aucun défaut fonctionnel ; ses demandes de preuve clavier et garde
annulé sont intégrées au banc.

Périmètre : portail Animation et documentation E73. Sans impact sur contrats API,
règles métier, migrations, générateur ou configuration d’exploitation : seule
la navigation change, sans nouvelle commande ni permission. Backend, Pro et
Marketplace inchangés ; états de roadmap conservés. Recette hébergée non
exécutée ; aucun commit, push ni déploiement effectué pour ce correctif.

## 31 octobre 2026 — création des chasses et guidage du gestionnaire

Demande : alléger le récapitulatif, expliciter la prise en compte et rendre
Assistant et Configuration plus utiles. Bases Animation **69b3ef8**, Projet
**fc0b32d**, autres modifications locales conservées. La reproduction initiale
constate un brief plafonné à **630 px pour 1 070 px disponibles** ; le contrôle
de largeur échoue avant correction. Le récapitulatif réaffichait une longue
liste de textes et le message de réussite disparaissait lors de la navigation.
Les formulaires de Configuration étaient comprimés à côté du parcours.

Le brief et son pied d’actions occupent désormais la largeur disponible. Le
récapitulatif présente des repères illustrés, garde les contenus complets dans
des détails dépliables et propose des accès Modifier sans perte de saisie.
L’introduction Léo et la bibliothèque ne sont plus répétées au récapitulatif.
Après reçu confirmé, un accusé focalisé dans la fiche distingue demande de
préparation et brouillon réutilisé, avec accès direct à Configuration. Les
relectures auxiliaires ne conditionnent plus cet accusé. Une réponse perdue
reste incertaine jusqu’à recherche du reçu ; aucun renvoi automatique.
L’accusé n’est ni persisté ni partagé entre contextes.

Assistant place les points d’attention en premier, puis une prochaine action
concrète, son intervenant et des étapes illustrées ; aides et vérifications
acquises restent consultables à la demande. Configuration affiche une seule
rubrique en pleine largeur avec consigne, repère et groupes explicites pour
présentation, dates, règlement et lots. Les panneaux visités restent montés,
les saisies sont conservées et les protections financières et de publication
demeurent. Un enregistrement des paramètres confirmé dispose aussi de son
repère visible et de son focus. Les CSS sont ciblées à leur source.

Preuves locales : types, lint, build de production isolé et **249 tests Node**
réussis, sans test ignoré. **82 contrôles navigateur** de préparation/génération
passent à 1280/390 px, dont réponse perdue, reçu confirmé malgré quota indisponible,
édition depuis le récapitulatif et réutilisation de bibliothèque.
La recette Léo et les quatre parcours Assistant intégrés passent également.
Les **268 contrôles** de préparation intégrée et les **40 scénarios /
448 contrôles** de dotation passent, avec versions, conflits, refus et commandes
incertaines préservés. La recette de préparation vérifie aussi la pleine largeur,
le focus de confirmation des paramètres et Configuration à 320 px/texte 200 %.
Les fixtures devenues anciennes sont alignées sur les sélecteurs bornés déjà
consommés par l’application ; aucune assertion métier affaiblie.

Les bancs autonomes Assistant et récapitulatif/accusés passent chacun
**16 scénarios** à 1600/390/320 px, dont texte à 200 %, clavier, focus,
cibles tactiles, détails conservés et absence de mutation. L’assertion de
lecture verticale des modalités des lots échoue avant restriction du sélecteur
CSS et passe après. Captures inspectées sur mobile, bureau et texte agrandi.
Les tests utilisent uniquement des données synthétiques et bloquent le réseau
externe, sans configuration opérateur.

Périmètre : portail Animation et documentation canonique E73/E55. Critères
d’ergonomie précisés ; états de roadmap conservés. Sans impact sur contrats API,
domaine, migrations, données existantes, générateur ou configuration ops : les
commandes et validations restent celles existantes. Backend, Pro et Marketplace
inchangés par ce correctif. Recette hébergée non exécutée ; aucun commit, push
ni déploiement effectué.

## 31 octobre 2026 — harmonisation du centre de notifications Live

Demande : aligner le centre de notifications sur la charte des autres pages.
Bases Marketplace **1699216**, Projet **fc0b32d**, changements locaux précédents
conservés. Cause : styles historiques du centre répartis dans `live.css`,
angles droits, réglages contradictoires de titre/actions et notifications lues
rendues par une baisse globale d’opacité. La reproduction depuis
`/live/messages` constate aussi l’absence de nom accessible du dialogue avant
interaction clavier : le scénario échoue sur le centre nommé attendu.

Les styles du centre sont consolidés dans `live-inbox.css` et retirés de leurs
anciennes règles, y compris les branches partagées, sans ajout de `!important`.
Typographie Live, surfaces et actions arrondies, pictogrammes par catégorie,
titre et contenu hiérarchisés, mentions **Non lue / Lue** et compteur de
notifications non lues dans l’aperçu affiché. Les messages lus gardent leur
contraste. Le bouton Fermer reste dans une barre adhérente ; le dialogue possède
son nom accessible dès le rendu et le focus initial va à la fermeture.
Les états vide, chargement et erreur ont leur repère visuel et une annonce
accessible. Les contenus restent du texte échappé, avec retour à la ligne.

Lecture individuelle, marquage des messages affichés, curseurs, mémorisation
locale et garde de navigation interne gardent leurs implémentations existantes.
Pas de nouvelle lecture implicite ni de permission Push. Le compteur n’invente
pas de total des notifications distantes. Même centre sur Animation et Coffrets,
avec le fond de leur surface respective ; les autres pages sont conservées.

Preuves locales : **11 scénarios navigateur réussis**, dont les huit nouveaux
cas du centre, la messagerie directe existante, le parcours à 320 px/texte
200 % et le confinement clavier des dialogues Live. Couverture à 320/390/1280 px,
surface Coffrets, états vide/erreur, pagination en échec puis reprise du même
curseur, lecture individuelle et collective, navigation interne, absence de
lecture implicite et texte échappé. La fixture compte séparément la lecture du
badge de l’en-tête et celle du centre à l’ouverture. Les deux scénarios voisins
d’accord organisateur, réponse perdue et retrait passent également. Captures
avant/après lecture inspectées sur mobile et bureau, dont texte agrandi.
Build de production isolé du banc et lint réussis ; le lint exclut uniquement
les répertoires de travail locaux `output/**` et `tmp/**`, ignorés par Git et
inaccessibles sous Windows (même contrainte constatée au correctif précédent).
Contrôles des liens/sources documentaires et `git diff --check` réussis.

Périmètre : Marketplace/Live et documentation canonique. Sans impact sur
contrats API, domaine, migrations, données existantes, générateur ou
configuration d’exploitation : seule la présentation utilise les réponses
existantes. Backend, Pro et portail Animation inchangés par ce correctif.
Statut de roadmap conservé. Recette hébergée non exécutée ; aucun commit, push
ni déploiement effectué pour ce correctif.

## 31 octobre 2026 — bloc des communes plus graphique sur l’accueil Live

Demande : remplacer le résumé trop textuel des communes dans Accueil. Bases
Marketplace **1699216**, Projet **fc0b32d**, autres travaux locaux conservés.
Cause : `LiveDiscovery` joignait les noms par un séparateur dans un paragraphe,
avec un lien de modification, sans repères visuels individuels. Le scénario
avant correction échoue sur l’absence du titre/région **Mes communes** attendu
dans l’accueil à 320 px.

Le bloc affiche désormais un compteur des communes suivies et des accès
individuels avec pictogramme de localisation, nom complet et flèche de
navigation. **Modifier mes communes** reste distinct et rejoint la page
existante. Les styles sont corrigés à leur source dans `live-discovery.css`,
en retirant le traitement commun du paragraphe ; pas d’image de remplacement,
de carte supposée ni de nouvelle statistique d’activité. Le bandeau reste
après la scène communale et les priorités personnelles gardent leur place.

Le clic sur une commune ouvre `/live/decouvrir?commune=<id>` et conserve la
sélection locale ; ni écriture API ni demande de position supplémentaire.
Le parcours partagé, la limite de dix choix et la recherche pour la sélection
vide restent ceux existants. Icônes décoratives, noms accessibles explicites,
liens de 44 px minimum, repli des noms longs et mouvements réduits conservés.

Preuves locales : les **4 nouveaux scénarios navigateur** passent à
320/390/1280 px, dont texte à 200 %, noms longs, dix communes, clavier, contexte
partagé sans changement de sélection et accès à la gestion. Les **6 tests Node**
des communes suivies et de la concurrence bornée passent aussi. Captures
inspectées sur mobile et bureau. Build de production isolé du banc navigateur
réussi, sans fichiers d’environnement opérateur. Le lint passe avec
`npm run lint -- --ignore-pattern 'output/**' --ignore-pattern 'tmp/**'` :
l’appel sans exclusions échouait sur des répertoires de travail ignorés par Git
et inaccessibles sous Windows (`EPERM`), sans modification de leurs permissions
ni de la configuration ESLint. Contrôles documentaires et `git diff --check`
réussis.

La sélection de **29 scénarios navigateur** a d’abord donné 28 succès et une
expiration dans le test de pagination tardive en erreur de Mes participations.
Son rejeu isolé réussit. Cause de synchronisation identifiée dans le test :
l’attente du titre de page ne garantissait pas la fin de la première lecture ;
le mock de réponse retardée pouvait alors intercepter cette première lecture.
Le test attend désormais le bouton de pagination avant d’installer ce mock.
Les deux variantes retardées (succès/erreur) et les quatre nouveaux scénarios
sont rejoués ensemble : **6 succès**, sans modification ni retrait d’assertion.
Le code applicatif de pagination n’est pas modifié.

Périmètre : Marketplace/Live et documentation canonique. Aucun impact sur
les règles métier, contrats API, persistance, migrations, générateur ou
configuration d’exploitation : ce correctif présente les communes déjà
sélectionnées et réutilise les routes existantes. Pas de changement du statut
de roadmap, ni de modification du portail Animation, du backend ou de Pro.
Vérifications sur fixtures locales ; recette hébergée non exécutée. Aucun
commit, push ou déploiement demandé/effectué pour ce correctif.

## 31 octobre 2026 — iconographie et actions principales du portail Animation

Demande : mieux distinguer les rubriques de Localeo Animation et les actions
principales, face à une accumulation de textes et de boutons. Bases Animation
**69b3ef8**, Projet **fc0b32d**, avec conservation des travaux locaux sur les
modules actifs. Reproduction locale avant correction : l’assertion navigateur
d’un pictogramme de section dans l’assistant échoue avec `0 != 1`. Le menu avait
déjà ses icônes, sans traitement commun dans les espaces de travail.

Le composant partagé `SectionHeading` et sa feuille `section-heading.css`
associent un pictogramme Lucide au titre, avec description et actions éventuelles.
Repères appliqués aux espaces principaux et aux rubriques d’une animation :
assistant, publication, Live, terrain, validations, communication, tirage,
remise, flyer et bilan ; ainsi qu’abonnement, commandes, équipe, support,
imports, catalogue de coffrets, participants, bilans et finance. Les onglets
d’animation reprennent ces repères ; le sélecteur natif mobile reste nommé.
La communication illustre ses trois étapes sans ajouter un encadré supplémentaire.

Sur le tableau de bord, les animations nécessitant une action précèdent les
indicateurs et graphiques. Le bouton contrasté reprend le libellé serveur et sa
destination existante ; sans libellé, il affiche **Ouvrir l’animation**, avec un
nom accessible complet. Les autres actions de progression, création, devis et
invitation reçoivent un repère utile ; actualisation et retours restent
secondaires. Les autorisations, confirmations, gestionnaires de commande et
protections contre les doubles envois sont conservés.

Les icônes décoratives ne dupliquent pas les libellés accessibles ; titres,
identifiants, références de focus et ordre sémantique sont préservés. Le texte
et les actions se replient à petite largeur et à 200 %. La recette a repéré puis
fait corriger le débordement du bouton d’invitation avec son icône et une cible
tactile calculée à 41,25 px au lieu de 44 px dans le tableau de bord. Une marge
de défilement sur le retour commercial évite de rogner son bord et son focus
lors du retour après commande. Aucune assertion réduite ni scénario ignoré.

Preuves locales : **249 tests Node** réussis ; **40 scénarios** intégrés de
tableau de bord et rubriques (1600/390/320 px, texte 200 %), **70 scénarios / 994
assertions** Abonnement, **56 scénarios / 388 assertions** Compte et équipe,
**126 assertions** de récupération/invitation/changement de compte dans
l’application complète, **24 scénarios** de commande, **12 scénarios** de
communication, **8 scénarios / 104 assertions** de support et navigation Flyers
à 1280/320 px. API synthétiques, aucun fournisseur ni environnement opérateur
contacté ; les parcours de lecture et raccourcis ne déclenchent pas de mutation.
Captures bureau et mobile inspectées, dont zoom 200 %. Types, lint, build isolé,
contrôles documentaires et `git diff --check` réussis.

Périmètre de ce correctif : portail Animation et documentation canonique.
Les règles métier, critères fonctionnels, contrats API, migrations,
configuration d’exploitation et générateur de démonstration ne changent pas ;
aucun contrôle backend supplémentaire requis pour ces repères de présentation.
Marketplace/Live public et Pro ne sont pas modifiés par ce correctif. Roadmap
inchangée. Pas de recette hébergée, commit, push ou déploiement effectués.

## 31 octobre 2026 — proposer uniquement les modules non actifs

Demande : dans Abonnement de Localeo Animation, retirer les modules déjà actifs
du choix d'ajout. Bases Animation **69b3ef8**, backend **c1c57b0**, Projet
**fc0b32d**. Reproduction avant correctif : la case d'achat de Chasse au trésor
était présente malgré son droit actif ; le test navigateur échoue avec `1 != 0`.

Le portail filtre désormais **ACHAT_MODULES** avec la projection serveur
`modules_actifs`, toutes origines couvertes. Mes modules reste consultable,
renouvellement et changement de forfait conservent leurs parcours. Une sélection
devenue active après actualisation est supprimée du devis ; si tous les modules
sont actifs, un état vide explique l'absence de choix. L'ancienne API sans ce
champ reste compatible, avec attente explicite de lecture complète des droits
paginés avant de proposer l'ajout.

Le domaine `DroitModule.statut_effectif` reste propriétaire des dates/états.
Le repository émet une liste DISTINCT de codes officiels pour toutes les périodes
de la page ; le service de lecture l'ajoute aux projections simples et paginées.
Aucune règle d'achat/devis, quota, renouvellement, droit acquis ou habilitation
modifiée. Le test SQL observe **10 requêtes** pour 2 comme pour 25 périodes sur
10 000 droits : une lecture groupée supplémentaire, sans N+1. Aucun changement
de schéma SQL ni de données de démonstration ; fixtures navigateur adaptées aux
achats de modules inactifs. La fixture de commerce réelle est alignée sur sa
voisine pour créer `finished_at` de v279, sans affaiblir les assertions.

Preuves locales : **126 tests backend** réussis (PostgreSQL jetable, HTTP,
commerce et domaine), **623 contrôles d'architecture** réussis ; **70 scénarios
navigateur, 994 assertions** réussis à 1280/390/320 px et texte à 200 %. Ces
scénarios couvrent droits actifs hors première page, quatre origines, module
expiré, tous modules actifs, ancienne API paginée, activation pendant la visite,
renouvellement, achat et retours réseau incertains. Types, lint et build isolé
Animation réussis. La revue indépendante ne constate aucun défaut fonctionnel.
Les contrats E41 et E42 sont régénérés avec les générateurs existants depuis
l'export hors ligne ; le contrat embarqué Animation est actualisé. Cet instantané
embarqué était antérieur aux contrats canoniques : sa régénération complète
reprend aussi leurs changements précédents et les métadonnées de validation
du producteur courant, sans modification manuelle des schémas. La suite Node
complète Animation vérifie les consommateurs : **249 tests réussis**, aucun
ignoré, dont le contrat commercial additif. Contrôles des liens et des sources
exportées, ainsi que `git diff --check`, réussis ; captures mobiles inspectées.

Périmètre : backend, portail Animation et documentation canonique. Pas d'impact
fonctionnel sur Live, Marketplace ou Pro ; leurs champs inconnus restent sans
effet. État de roadmap inchangé. Aucun achat réel, commit, push ou déploiement ;
recette sur l'environnement hébergé non exécutée. Livraison : backend puis
portail, sans nouvelle configuration.

## 31 octobre 2026 — Mes lots dans le menu principal Live

Demande utilisateur : sortir **Mes lots** des sous-onglets de Mes participations
et placer son entrée entre **Mes participations** et **Mes communes**. Bases
Marketplace **8204c80**, projet **e730ee0**, avec les travaux locaux conservés.
La reproduction navigateur échoue sur les deux surfaces Live : le menu ne
contient que trois liens, sans Mes lots.

La navigation présente désormais **Accueil / Mes participations / Mes lots /
Mes communes**, avec un pictogramme cadeau pour les lots. La liste possède son
titre **Mes lots** ; cette entrée reste la seule active dans la liste et le
détail d'un bon. Le sous-onglet est retiré du carnet ; sur la surface Animation,
le bandeau devenu redondant avec un seul onglet est supprimé. Les deux rubriques
Coffrets/Participations restent disponibles sur la surface Coffrets. Le dock
conserve sa hauteur mesurée, les safe areas et le retour à la ligne des libellés.

Les URL `/live/lots` et `/live/lots/:id`, les capacités personnelles, le stockage
volontaire et les états/QR des bons restent inchangés. Périmètre : Marketplace
et documentation E73. Aucun impact contrat API, règle domaine, migration,
générateur de démonstration ou configuration d'exploitation : seul l'accès à
une page existante change. Aucun changement des statuts de roadmap ; vérification
locale uniquement, sans commit, push ni déploiement.

Preuves : **18 tests navigateur finaux réussis, aucun ignoré**, sur navigation
des deux surfaces, clavier, accès direct et rechargement, bons sauvegardés,
QR et refus sans capacité, participations distinctes et carnet importé sans
token. Les captures et assertions vérifient les quatre entrées sur une ligne
à 320/390/1280 px ; le texte à 200 % reste lisible et la dernière action ne
passe pas sous le dock. Les 12 tests du carnet et les six tests de navigation/
préférences ont également réussi avant l'ajustement final de répartition du
dock. Le contrôle de mot entier des participations cible désormais le menu
principal, le sous-onglet ayant été retiré. ESLint, contrôle des liens et des
sources exportées, ainsi que `git diff --check`, réussissent (codes de sortie 0).

## 31 octobre 2026 — Live comme espace de jeu local

Retour utilisateur : l'ensemble de Live doit évoquer une animation à vivre et
inciter à participer, au-delà de fiches éditoriales. Base Marketplace **8204c80**,
projet **e730ee0**, avec les correctifs locaux précédents conservés. Le test de
reproduction à 320 px constate que l'action du défi personnel a un ratio de
visibilité nul dans le premier écran, après le grand programme communal.

L'accueil place maintenant la priorité personnelle, puis ses deux suivantes au
maximum, avant le programme public. La carte principale devient un espace de
jeu navy/orange : anneau et étapes restantes contrastés, indicateurs métier
conservés, action de reprise ou récupération au premier plan. Sans priorité,
le rendez-vous communal ouvre l'accueil, avec Flyer, type de jeu, participants
et dotation connus, puis une action publique visible. Les cartes mettent leur
objectif et leur action avant les textes de détail.

Un helper de présentation partagé aligne les types Passeport/Tombola/Chasse de
l'accueil, du catalogue et de la fiche. L'objectif de validations n'est chiffré
que pour un Passeport explicite avec entier positif ; une chasse ne récupère
plus un récit de validations commerçantes provenant d'un ancien champ. Les
cartes continuent d'ouvrir la fiche publique et ses conditions ; elles ne créent
pas d'inscription implicite. Le libellé de participation respecte l'ouverture
serveur des inscriptions.

Le shell Animation reçoit un dock navy avec destination active orange, un
en-tête compact et un fond clair. Les cartes du carnet utilisent ses variables
de surface et d'espacement. Les styles de cartes et de scène sont remplacés
à leur source ; l'habillage de surface est centralisé, avec safe areas, hauteur
de dock mesurée, clavier, texte agrandi et mouvements réduits. Les parcours
Coffrets et les libellés/liens de navigation sont conservés.

Preuves initiales : **15 tests navigateur ciblés réussis** après correction,
incluant reprise visible dans le premier écran, rendez-vous public, 320/390/1280 px,
texte à 200 %, données partielles, erreurs/vide, bon accès personnel et reprise
des anciens accès par lots bornés. **Cinq tests Node réussis** sur présentation,
priorités/progression et transport du tableau de bord. ESLint sur les sources et
tests modifiés réussit. Les revues indépendantes du shell et des projections
publiques ne constatent pas de règle ou d'accès inventé. La campagne transversale
finale réussit : **75 tests navigateur, aucun ignoré**, sur accueil, découverte,
fiches, images, carnet, communes, navigation, préférences et liens personnels.
L'inspection à 200 % conduit à laisser le dock et les compteurs de périodes
revenir à la ligne entre boutons plutôt qu'à couper les mots. **Dix tests ciblés
rejoués passent** sur cet ajustement final ; ils vérifient aussi que la dernière
action reste au-dessus du dock après défilement au bas de la page.

Captures mobile, bureau et texte à 200 % inspectées ; aperçus conservés dans
`tmp/live-play-review/` du Marketplace (fichiers de travail ignorés). Les contrôles
documentaires réussissent : 96 guides, 1 081 liens sans erreur et 130 documents
exportés vérifiés. `git diff --check` passe dans les deux dépôts. Aucun test backend
relancé, ses règles et contrats n'étant pas modifiés.

Impacts : Marketplace/Live et documentation canonique E73. Aucun changement de
règle backend, contrat API, migration, générateur ou configuration : mêmes
objectifs, progressions, inscriptions et accès stockés. Aucune animation en temps
réel, score, classement ou compte à rebours synthétique. Aucun accès au TEST
partagé, commit, push ou déploiement ; recette hébergée non exécutée. L'état global
de l'epic reste inchangé.

## 31 octobre 2026 — fiche publique orientée jeu et défi

Retour utilisateur : une fiche d'animation plus graphique et immersive, orientée
jeux/challenge plutôt qu'éditorial. Base Marketplace **8204c80**, projet **e730ee0**,
avec les correctifs locaux précédents conservés. L'ancien en-tête plaçait le
long descriptif avant l'action et imposait un récit de passages commerçants aux
trois types d'animation. Le test initial constate l'absence du repère **Votre défi**.

La fiche publique présente maintenant le Flyer disponible, le statut, le type
de jeu, l'objectif et l'action autorisée avant les textes détaillés. Le passeport
explicitement identifié affiche son objectif positif configuré ; tombola et
chasse ont des invitations adaptées. Un type ou objectif inconnu reste générique,
sans progression personnelle ni faux zéro. Participants, gagnants et dotation
totale connus sont présentés par nombres et pictogrammes. Les dates, raccourcis
vers lots/adresses/conditions et volets de description/règlement restent lisibles
sur mobile. Les lots et adresses utilisent leurs médias réels, sinon un
pictogramme ; aucune photo de remplacement n'est choisie. La pagination des lots
reste volontaire, avec remplacement de page, retour et reprise après erreur.

Les anciens styles d'introduction et de bénéfice sont retirés de leurs sources,
y compris les surcharges éditoriales. La présentation est regroupée dans le
composant d'entrée de défi et sa feuille dédiée. Les gardes d'inscription restent
dans les parents existants. Lecture anonyme, provenance `source`, récupération
par e-mail, inscriptions multiples, QR et accès personnels sont conservés.

Preuves locales : **28 tests navigateur réussis** sur fiche, variantes, statuts,
images Flyer, inscription sans compte, lots externes, pagination, refus et
récupération. Les tests vérifient 320/390/1280 px, texte à 200 %, objectif connu
ou invalide, valeurs publiques inconnues, absence d'avancement inventé et
conservation du texte complet après ouverture des volets. Le parcours de test
ouvre aussi le volet existant **Lire le règlement complet** avant de vérifier
son texte ; l'assertion de contenu est conservée. Une revue indépendante des
champs et des garde-fous n'identifie pas de blocage ; les trois discriminants
canoniques sont utilisés. **20 scénarios ciblés passent** après le nettoyage des
styles et l'ajout des pictogrammes de lots/adresses ; ce rejeu inclut un nouveau
cas de média réel puis en échec. Au total, **29 scénarios distincts** sont vérifiés.
Trois rejeux à 320/390/1280 px confirment ensuite l'alignement final du bloc défi
et de l'action principale après retrait de leur contrainte de largeur arbitraire.
Captures à 320/390/1280 px et texte à 200 % inspectées. Les contrôles de liens et
de sources exportées réussissent : 96 guides, 1 081 liens sans erreur et
130 documents vérifiés. Aucun test backend relancé, ses règles et contrats
n'ayant pas changé.

Impacts : Marketplace/Live, consommateur public partagé et documentation canonique
E73. Aucun contrat, règle backend, migration, configuration ou générateur modifié :
la fiche présente les projections existantes et ne modifie aucune participation.
Aucun accès au TEST partagé, envoi réel d'e-mail, commit, push ou déploiement.
La recette hébergée reste non exécutée ; l'état global de l'epic ne change pas.

## 31 octobre 2026 — Mes communes : repères graphiques et accès aux animations

Retour utilisateur : rendre la section des communes plus graphique, dans la
continuité du carnet Live. Base Marketplace **8204c80**, projet **e730ee0**, avec
les correctifs locaux précédents conservés. La présentation existante associait
une liste de liens à plusieurs paragraphes, sans compteur ni repère visuel par
commune. Le scénario à 320 px constate l'absence du compteur avant correction.

**Mes communes** affiche maintenant le nombre de communes suivies dans ce
navigateur, un repère de localisation, le nom, le code postal disponible et une
coche de suivi. **Voir les animations** ouvre le contexte public existant ; le
retrait est secondaire, avec un bouton nommé pour la commune concernée. Recherche
et géolocalisation sont regroupées. Les explications de localisation restent
disponibles dans un volet natif. L'en-tête est compact sur mobile ; la liste
passe sur deux colonnes sur bureau. Aucun visuel territorial ni compteur
d'animations n'est inventé. Les styles des communes sont retirés de la feuille
de découverte et regroupés à leur source, sans superposition de correctifs.

Preuves locales : **33 tests navigateur réussis** sur communes, découverte,
navigation et préférences de notifications. Ils couvrent ajout/retrait et
persistance, borne de dix choix, absence de doublon, clavier, noms longs,
320/390/1280 px, texte à 200 %, stockage refusé, recherche vide/en erreur,
géolocalisation volontaire, refus, délai, service indisponible et réponse
tardive. Les coordonnées ne sont pas persistées ; les catégories de notification
et communes partagées restent indépendantes du suivi. **Six tests Node réussis**
sur normalisation, stockage et lectures bornées. ESLint sur les sources et le
nouveau test réussit. **Six scénarios navigateur rejoués passent** après le
compactage final de l'en-tête. Captures mobile, bureau et texte à 200 % inspectées.
Les contrôles documentaires réussissent : 96 guides, 1 081 liens sans erreur,
130 documents exportés vérifiés et `git diff --check` dans les deux dépôts.

Impacts : Marketplace/Live et documentation canonique E73 uniquement. Contrats,
règles backend, migrations, configuration et générateur sans changement : mêmes
API et mêmes données locales. Aucune écriture distante, aucun commit, push ou
déploiement. La recette hébergée n'est pas exécutée et l'état global de l'epic
reste inchangé.

## 31 octobre 2026 — participations regroupées dans leur page dédiée

Retour utilisateur : la section **Mes autres participations** alourdit l'accueil
et doit rejoindre **Mes participations**, en conservant sa présentation graphique.
Base Marketplace **8204c80**, projet **e730ee0**, avec changements locaux de ce
correctif. La cause est locale : l'accueil affichait toutes les pages du tableau
de bord tandis que la page dédiée ne lisait que le carnet de l'appareil.

L'accueil conserve au plus trois priorités et le lien **Toutes mes participations**.
La page dédiée réunit carnet et accès liés à l'installation, dédupliqués par
identifiant de participation, sans fusionner les inscriptions à une même animation.
Elle reprend anneaux, étapes restantes, compteurs à pictogrammes et images Flyer
disponibles, sans illustration de remplacement. Les compteurs du carnet sont
explicitement limités à cet appareil ; ceux des accès distants à la page chargée.
Une progression absente ou incohérente reste sans anneau. Qualification et gain
restent issus du serveur, indépendamment du pourcentage.

La pagination et la liaison explicite des anciens accès sont déplacées avec
leurs bornes existantes : 50 éléments par page, 50 liaisons par action, deux
requêtes simultanées. Sans accès personnel, la récupération demande l'e-mail
d'inscription ; elle ne choisit pas une autre inscription et ne crée aucun QR.
Le cas d'un carnet importé sans token dispose du même parcours. Les composants
de carte et d'anneau sont partagés ; les anciens styles de barre sont retirés.

Preuves locales : **42 tests navigateur réussis**, couvrant accueil limité à
trois priorités, récupération, inscriptions multiples, QR distincts, carnet sans
token, pagination, réponses tardives, liaison bornée, erreurs réseau et stockage,
rendus à 320/390/1280 px et texte agrandi à 200 %. **10 tests Node réussis**, dont
progression inconnue et séparation progression/qualification. ESLint sur les
sources et tests modifiés réussi. Les anciens scénarios de récupération ont été
adaptés à la fiche publique actuelle et au DTO de jeu actuel, en conservant les
assertions e-mail et QR.

L'inspection des captures révèle ensuite un mot « participations » coupé à
320 px : le style des lots imposait trois colonnes même lorsque deux onglets
étaient présents. Une assertion de plage de texte reproduit la coupure avant
correction (deux lignes au lieu d'une). La règle fixe est supprimée ; les onglets
utilisent leur contenu et peuvent revenir à la ligne entre les liens.
**Cinq tests navigateur rejoués réussissent** sur cette correction finale,
notamment le mot entier à 320 px et à 200 %, les QR et les rubriques du carnet.
Captures finales mobile et bureau inspectées. Les contrôles documentaires passent :
96 guides, 1 081 liens locaux, aucune erreur et 130 documents exportés vérifiés.

Impacts : Marketplace/Live et documentation canonique E73. Sans changement de
contrat, règle backend, migration, configuration ou générateur : les projections
existantes sont utilisées et les accès stockés conservés. Aucun appel au TEST
partagé ni envoi réel d'e-mail. Aucun commit, push ou déploiement ; la recette
hébergée reste non exécutée. L'état global de l'epic est inchangé.

## 31 octobre 2026 — Mon Live : priorité au visuel

Retour utilisateur : privilégier le graphique aux longs textes. Sur la base
Marketplace **7d9e0fc** avec les correctifs précédents conservés, le contrôle
navigateur reproduit une image limitée à **130 px** de haut sur mobile, avant
correction. L'ouverture utilise désormais toute la largeur pour l'image Flyer
choisie, avec un titre local compact ; les paragraphes d'ambiance redondants
sont retirés. Aucun visuel de remplacement n'est ajouté.

Participants, gagnants, lots et périodes sont repérés par des pictogrammes
d'interface, avec leurs valeurs et libellés conservés. La progression personnelle
est un anneau chiffré accessible, associé aux étapes validées/restantes. Le
pourcentage ne confère ni qualification ni gain. Les descriptions et conditions
des cartes restent disponibles dans un volet natif **En bref**, sans troncature
ni perte de l'accès à la fiche complète. Les règles d'accès, priorités, communes
et données API restent inchangées. Les styles ont été remplacés à leur source,
notamment la composition du bandeau et la barre devenue anneau.

Preuves locales : première campagne de **39 tests navigateur**, avec **38 succès**
et un défaut de présentation des pictogrammes dans les valeurs numériques à
200 %. Les pictogrammes ont été déplacés dans les libellés ; l'assertion de
nombre sur une seule ligne est conservée. **12 tests ciblés rejoués avec succès**
sur le correctif final : compteurs connus/inconnus et zoom 200 %, clavier,
mouvements réduits, reprise personnelle, rendu 320/390/1280 px, image pleine
largeur, anneau accessible, ouverture/fermeture des descriptions et conditions,
panne et programme vide. Captures inspectées dans les sorties Playwright locales.
ESLint sur `src` et les tests modifiés, contrôles de liens et **130 documents
exportés** réussis. Aucun test backend relancé : ses règles et contrats n'ont
pas changé pour ce complément de présentation.

Impacts : Marketplace/Live et spécification graphique E73. Aucun changement
backend, contrat, migration, générateur ou configuration : seules les projections
existantes sont présentées autrement. Aucun accès au TEST partagé, commit, push
ou déploiement ; vérification hébergée non exécutée.

## 31 octobre 2026 — un accueil Mon Live ancré dans la vie des communes

Retour utilisateur : accueil trop institutionnel et figé, activité communale
insuffisamment mise en avant. Base Marketplace **7d9e0fc**, correctif Flyer et
autres travaux locaux conservés. L'ancien écran empilait d'abord participations,
messages de service et informations du carnet avant la découverte publique.
Le test de reproduction constate l'absence de l'ouverture locale attendue avant
correction ; les règles de priorisation ne sont pas remises en cause.

Correction de présentation : accroche contextualisée par les communes réellement
consultées, animation en cours à rejoindre (sinon prochaine), image personnalisée
du Flyer seule, nombre public de participants de cette animation. Les accès
**En ce moment** et **Prochainement** indiquent les nombres de l'aperçu chargé ;
la pagination et les erreurs rendent explicitement cet aperçu partiel. Aucun
compteur d'habitants uniques, nouvelle activité récente ou temps réel n'est
inventé. Les communes suivies ne sont pas modifiées par la consultation.

Le raccourci **Mes défis à reprendre** est visible dès l'en-tête lorsque des
priorités existent. Il rejoint la première priorité et ses deux suivantes,
avant les cartes publiques ; les autres informations du carnet suivent le
programme. Les indicateurs, progressions, liens personnels et limites de page
restent ceux des projections existantes. **Actualiser** recharge aussi le
catalogue, sans requête supplémentaire par carte ni parcours exhaustif des
pages. L'indisponibilité propose une relance ; elle ne se confond plus avec le
programme vide. Les mouvements d'entrée et de survol sont désactivés lorsque
la réduction des animations est demandée.

La revue indépendante a fait ajouter la reprise directe sur mobile, distinguer
la panne du vide et porter la marge de défilement sur les titres réellement
ciblés par les ancres. Les styles de l'en-tête et de la priorité ont été modifiés
à leur source, sans nouvelle couche de surcharge ; le bloc local possède sa
feuille de style dédiée.

Preuves finales : **39 tests Playwright réussis**, dont six nouveaux scénarios
sur l'accueil communal à 320/390/1280 px, texte agrandi à 200 %, navigation par
ancres sans masquage sous l'en-tête, actualisation du programme, aperçu partiel,
absence d'image et reprise après panne. Les parcours existants de tri personnel,
pagination bornée, réponses tardives, accès exacts, sélection des communes,
préférences et illustrations Flyer restent verts. Le test de réponses retardées
libère désormais ses requêtes en `finally`, sans changer ses assertions ; une
exécution initiale bloquée a été interrompue avant rejeu ciblé puis complet.
**10 tests Node** de tableau de bord/communes réussis ; ESLint sur `src` et les
trois fichiers de tests concernés réussi. Le runner navigateur reconstruit
l'application hors configuration privée ; captures inspectées dans
`localeo-marketplace/test-results/desktop/`. Liens documentaires et **130 sources
exportées** vérifiés sans erreur.

Impacts : Marketplace/Live et [spécification E73-HOME-01/06](localeo-live-entree-unique.md#critères-et-preuves-attendues).
Backend, contrats API, règles métier, migrations, générateur, DNS et configuration
sans changement pour ce correctif : les données publiques et personnelles
existantes sont réutilisées. Aucun accès au TEST partagé, notification réelle,
commit, push ou déploiement ; recette hébergée non exécutée.

## 31 octobre 2026 — illustration du Flyer dans les blocs Live

Attendu : la présentation d'une animation utilise l'image personnalisée choisie
dans **Flyer**, sinon aucune illustration. Reproduction locale sur marketplace
**7d9e0fc** et backend **586a51f**, avec les travaux précédents conservés : le test
navigateur attend l'image Flyer mais reçoit une vignette éditoriale historique.
Sans vignette, Live choisissait une photo Localeo de remplacement. En amont,
`visuel_url` annonçait des assets génériques ou l'aperçu généré du flyer, au lieu
de l'illustration personnalisée.

Correction : les cartes de découverte et l'en-tête de fiche Live consomment
strictement `visuel_url`, sans alias historique ni illustration de remplacement.
L'absence d'image ou l'échec de chargement supprime le bloc visuel ; titre,
statut, dates et inscription restent lisibles, sans colonne vide. Le backend
projette l'illustration personnalisée du Flyer, chargée par une route dédiée
publique sans cache, après contrôle de visibilité et sélection du dernier
document du type exact rattaché à l'animation. Les archives sont exclues après
classement pour ne pas restaurer une ancienne image ; taille et SHA256 sont
contrôlés hors transaction SQL. Le chemin historique `/visuel`, les illustrations
de jeu et le rendu PDF gardent leurs règles existantes.

Preuves frontend : test de reproduction en échec avant correction, puis **11
tests Playwright réussis**, dont six cas à 320/1280 px (image choisie, absente,
introuvable), parcours découverte vers fiche, inscription accessible, aucune
requête vers les illustrations historiques, aucun débordement et contenu sur
toute la largeur sans image. Non-régression des indicateurs publics et de
l'inscription sans compte incluse ; captures inspectées dans
`localeo-marketplace/test-results/desktop/`. **10 tests Node** de carnet,
tableau de bord et transport réussis. ESLint sur `src` et le nouveau test réussi ;
`npm run lint` global bloqué par des répertoires de sortie temporaires refusés
par Windows (`EPERM`), sans modification de leurs droits.

Preuves backend : **37 tests application/API/OpenAPI/sécurité réussis** et
**22 tests PostgreSQL isolés réussis**, sans échec ni skip. Les six nouveaux cas
SQL couvrent le dépôt réel, le remplacement et le retrait, ainsi que les refus
sur document archivé, mauvais scope, catégorie, MIME ou type documentaire.
Les tests existants d'illustration Flyer et de provenance des couvertures de
chasse restent verts. Le cluster local de test a été arrêté après exécution.
Les **623 contrôles d'architecture** réussissent sur le correctif final.
La revue indépendante a fait aligner le tri sur la sélection canonique du Flyer
(`updated_at` décroissant), sans autre défaut établi. Une animation devenue
non publique peut conserver une URL dans sa projection personnelle ; le binaire
public est alors refusé et Live masque l'image, sans exposer de document privé.

Impacts : backend, Marketplace/Live, spécifications Flyer/Live et contrats
OpenAPI canoniques E41/E42. Aucun schéma de données ni migration, nouveau droit,
paramètre ou champ obligatoire ; le générateur peut toujours produire une
animation sans image personnalisée. Aucun accès aux données TEST, aucun commit,
push ni déploiement. La recette hébergée reste à exécuter après livraison du
backend puis de Live selon le [guide d'exploitation](../../exploitation/technique/configurer-epic-73.md).

## 31 octobre 2026 — 403 sur le lien d'édition d'une offre

Signalement : `/admin/offre-plateforme-orm/edit/9bfa4730-176d-4f14-9ffa-052add702709`
renvoie 403 malgré une connexion administrateur. Base backend **586a51f** et
modifications locales précédentes conservées. Cause démontrée dans les sources :
`OffrePlateformeAdmin` interdit volontairement l'édition ORM depuis le catalogue
versionné, mais **Offres et tarifs** proposait encore un lien « Modifier » vers
cette édition interdite. Le test de rendu a reproduit ce lien avant correction.
La session distante et l'existence de l'offre signalée n'ont pas été consultées.

Correction : **Publier une nouvelle version** ouvre le catalogue commercial
existant avec `offre_id`. Le choix de la commune et la pagination conservent
l'offre cible ; seule cette offre est présentée pour l'édition. La nouvelle
version reste soumise à l'action autorisée par le serveur, au motif, à la
confirmation, à la version attendue et à l'idempotence existants. L'interface
précise la portée des futurs achats dans toutes les communes. L'ancien GET
d'édition redirige en 303 avec `no-store` après contrôle ADMIN historique et
validation de l'UUID. Aucune écriture ORM n'est réactivée ; les versions et
conditions acquises restent protégées. Une offre absente ou non publiée est
signalée sans publication implicite.

Preuves locales : **4 tests Python ciblés réussis** (rendu corrigé, interdictions
ORM conservées, redirection ADMIN, refus anonyme/profil métier/compte nominatif,
identifiant invalide et POST non redirigé, API de création protégée), **623
contrôles d'architecture réussis**. `node tests/browser/offre-version-navigation.cjs` :
**3 parcours** à 1280/320 px et texte 200 %, depuis la liste vers la publication
ciblée en seconde page, aucun POST avant confirmation, même offre/version dans
la commande et refus lecteur. Le libellé accessible du sélecteur Commune est
explicite. `node tests/browser/epic73-modules-erp.cjs` réussit à 320/1280 px :
versions, octrois, conflits, remboursements et dates Paris conservés.
Captures dans `.artifacts/offres-catalogue/` du backend.

Impacts : backend ERP et [parcours canonique du catalogue](modules-souscriptions-import-communication.md#3-catalogue-et-droits-acquis).
Pas de changement de règle métier, contrat de publication, calcul de droits,
migration, configuration ou générateur : le correctif relie la lecture et le
formulaire de publication déjà existants. Aucune donnée, offre réelle ou
souscription modifiée ; recette hébergée non exécutée. Aucun commit, push ou
déploiement effectué.

## 31 octobre 2026 — parcours du gestionnaire interne ERP

Retour utilisateur : simplifier la nouvelle souscription (partenaire, droits,
accès), l'exploitation des animations en cours et les demandes de support.
Base backend **586a51f**, travaux locaux des autres dépôts conservés. Les
reproductions ont montré un ordre de formulaire incohérent, des actions utiles
peu visibles et une réponse support peu distinguée des opérations internes.

Correction de présentation, sans modification des règles métier :

- Référencement en quatre étapes ordonnées, contenu du forfait lisible, revue
  et confirmation explicites avant création. Modification de saisie : revue
  invalidée. Dossier créé directement accessible, gratuité et paiement attendu
  distingués, invitation toujours conditionnée par l'activation.
- Suivi des animations : filtres prioritaires et raccourci « En cours »,
  conservation du contexte, pilotage avant les lots et liens vers les consoles
  autorisées. Aucun indicateur de dates d'animation absent de l'API n'est inventé.
- Support : demandes à traiter et échéances repérables, réponse principale,
  notes privées et suivi interne séparés, messages titrés et focalisés. Les
  compteurs indiquent leur portée limitée à la page. La revue a reproduit puis
  corrigé une demande clôturée comptée en retard ouvert : son détail présente
  désormais l'historique, sans nouvelle échéance de réponse.

Preuves locales :

- `tests/infrastructure/admin/test_referencement_animation_ux.py` : deux
  reproductions rouges avant correction, vertes après ; tests API/navigation
  ciblés conservés. `tests/browser/gestionnaire-souscription-ux.cjs` :
  **63 contrôles** à 1280/320 px et texte 200 %, sans création à la consultation.
  **17 tests Python** ciblés réussis ; régressions checkout, équipes et accès
  internes réussies. Navigation ERP : **26 contrôles** réussis.
- `tests/browser/epic73-operations-ux.cjs`, suivi produits, exploitation et
  préparation : **26 scénarios** réussis ; profils gestionnaire, lecture et
  Support, 1280/320 px et texte 200 %, droits et contexte vérifiés.
- Les deux bancs `epic73-support-organisations*.cjs` passent, dont demande
  clôturée sans première réponse avec ancien indicateur de retard. Réponse,
  note privée, conflit, reçu incertain, relecture et rejeu explicite avec même
  clé/corps vérifiés. **12 tests Node et 14 tests API/navigation** réussis.
- Contrôles backend obligatoires : **623 tests** d'architecture, classes du
  domaine et couverture des use cases réussis. Captures locales dans
  `.artifacts/gestionnaire-ux/`, `tmp/operations-ux-captures/` et
  `.artifacts/e73-support-organisations-ux/` du backend.

Impacts : backend ERP et [présentation canonique des parcours](perimetres-parcours-saas.md#45-parcours-du-gestionnaire-interne-erp).
Contrats, domaine, permissions, migrations et générateur sans impact pour cette
réorganisation : seules les actions existantes sont présentées différemment.
CSRF, version, idempotence, confirmation et résultats incertains conservés.
Styles corrigés à leur source et limités à ces écrans. Recette hébergée non
exécutée ; aucun compte, invitation ou paiement réel créé.

## 31 octobre 2026 — forfait Premium ajouté après confirmation des conditions

Cause reproduite : `v215` et le catalogue de références ne définissaient que
Découverte et Essentielle. L'utilisateur confirme **1 490 € HT, 12 mois,
animations illimitées, accompagnement par défaut et aucun module payant inclus**.
Le modèle retenu est l'accompagnement standard de la plateforme autonome,
sans nouvelle prestation clé en main. Les [conditions canoniques](modules-souscriptions-import-communication.md#catalogue-initial-et-unités)
et la présentation historique E47 sont actualisées, sans changer les statuts.

Depuis `v265`, le portail lit `versions_catalogue_modules` : une offre historique
seule ne suffit pas. La nouvelle migration **v285** ajoute donc Premium aux
deux sources et les références incluent ses conditions. Elle ne réécrit aucune
vente acquise ni version publiée ; une offre personnalisée, inactive ou retirée
est préservée. La publication générique après création ERP/provisionnement reste
un sujet distinct ; cette correction publie uniquement Premium.

Preuves locales :

- Référence absente : test rouge avant correction ; **48 tests de références**
  réussis ensuite, dont prix, durée, quota et absence des trois modules payants.
- **6 tests PostgreSQL isolés** réussis : publication effective par le service
  de catalogue, idempotence, préservation des conditions acquises et des offres
  existantes/personnalisées/inactives/retirées. Devis réel de renouvellement :
  149 000 centimes HT, 178 800 TTC sous TVA synthétique 20 %, une seule ligne
  forfait, 12 mois et aucun module ; aucun droit activé par le seul devis.
- Portail Animation : **4 scénarios navigateur, 52 assertions**, à 1280/390/320 px
  et texte 200 %. Premium apparaît depuis le catalogue serveur, la demande de
  devis porte son code sans module et aucune commande n'est confirmée sans
  consentement. Le prix est calculé côté domaine, pas dans le navigateur.
- Revue indépendante de la migration et des invariants : aucun écart bloquant.
- Contrat HTTP du consommateur : **2 tests** réussis. Documentation finale :
  **98 guides, 1 158 liens**, aucune erreur ; **130 sources exportées**
  vérifiées, `git diff --check` réussi dans les trois dépôts modifiés.
  Le serveur PostgreSQL jetable a été arrêté après les vérifications.

Impacts : références et migration backend ; spécifications et exploitation ;
tests du consommateur Animation. Aucun nouveau contrat, droit de module,
paramètre d'environnement ou ajustement du générateur nécessaire : le forfait
réutilise les capacités standard existantes. Les anciennes migrations restent
inchangées. Migration préparée et vérifiée localement uniquement ; **TEST non
migré vers v285**, aucun fournisseur de paiement sollicité. Aucun commit, push
ou déploiement effectué pour ces deux correctifs.

## 31 octobre 2026 — hiérarchie de Compte et équipe

Retour utilisateur : actions difficiles à hiérarchiser. Base Animation
**4ef51b2** avec les autres modifications locales conservées. Reproduction dans
le navigateur : la rubrique export/fermeture précédait les collaborateurs et
le bouton d’invitation ; les trois champs de mot de passe restaient toujours
ouverts, et la page était centrée sous un plafond `max-w-5xl`. Le nouveau
contrôle d’ordre échouait avant correction pour cette raison.

Correction : équipe courante en premier et invitation principale dès son
en-tête ; actualisation et modification d’un accès secondaires. Collaborateurs
et invitations sont séparés. Un transfert à suivre remonte avant les listes,
y compris pour son successeur non responsable. Les accès rapides **Équipe**,
**Mes organisations** et **Mon compte** placent le focus dans leur section sans
changer le contexte. L’organisation courante est nommée et les autres disposent
d’une ouverture explicite. Mot de passe et opérations sensibles sont à la
demande ; les composants restent montés au repli pour préserver leur état.

Saisies et confirmations s’ouvrent avant les listes, avec focus et défilement.
Annuler rend le focus au déclencheur sans écriture ; une confirmation de
révocation masque la saisie concurrente. Les retours d’équipe réutilisent le
message contrasté commun à Abonnement ; ils rappellent qu’une invitation ou une
proposition de transfert attend l’acceptation de son destinataire. La revue indépendante a relevé un nom
accessible qui omettait « Ouvrir cette organisation » : il inclut désormais
ce libellé visible, le nom de l’organisation et le rôle. Les deux contrôles de
changement d’organisation dans l’application ont été adaptés et rejoués.

Preuves locales :

- `node tests/browser/organisation-access.mjs` : **56 scénarios, 388 assertions**,
  1280/390/320 px et texte à 200 %. Ordre invitation/opérations sensibles,
  invitation, lecture seule, édition, révocation d’autrui/de soi, renvoi/révocation
  d’invitation, acceptation du transfert par le successeur, annulations sans
  mutation, focus clavier, pagination indépendante, mot de passe et reprise
  après réponse perdue avec corps et clé identiques. Le repli des opérations
  sensibles conserve la confirmation d’export sans envoyer de commande.
- `node tests/browser/account-app.mjs` : **16 parcours, 126 assertions**,
  application réelle à 1280/320 px, largeur du contenu, absence de lectures
  métier pour identité seule, acceptation d’invitation, changement de contexte,
  récupération/changement du mot de passe et reconnexion, déconnexion à réessayer.
- `node tests/browser/reversibilite-catalogue.mjs` : **12 scénarios,
  100 assertions**, export et reprise incertaine, téléchargement privé, fermeture
  accompagnée, refus et catalogue. Aucun fournisseur réel sollicité.
- **244 tests Node réussis**, aucun ignoré ; types, lint, builds application et
  PWA isolés réussis, sans environnement opérateur. Captures dans
  `tmp/organisation-access/` et `tmp/generation-browser-dist/` du dépôt Animation ;
  bureau, mobile et zoom inspectés.
- Revue indépendante : droits/actions serveur, identité seule, accès du
  successeur, montage persistant, version et clé de commande, pagination et
  annulation préservés. Aucun changement des invariants du domaine
  `identite_acces` ou de la réversibilité.
- Documentation : **96 guides, 1100 liens**, aucune erreur ; **130 sources
  exportées** vérifiées et `git diff --check` réussi dans les deux dépôts.

Impacts : Animation et documentation canonique uniquement ;
[présentation du parcours](perimetres-parcours-saas.md#44-présentation-de-compte-et-équipe)
actualisée. Aucun contrat, calcul de droits, migration, générateur, donnée ou
paramètre d’exploitation modifié : la correction organise les actions existantes
et conserve leurs contrôles serveur. Styles corrigés dans le composant, sans
nouvelle surcharge CSS. État de l’epic inchangé ; aucun email ou changement
d’accès réel, commit, push ou déploiement effectué. Recette hébergée non exécutée.

## 31 octobre 2026 — hiérarchie et confirmations de la page Abonnement

Retour utilisateur : actions sans hiérarchie et confirmations peu lisibles.
Base Animation **4ef51b2**, avec les autres travaux locaux conservés. Cause
observée dans le navigateur : renouvellement et facturation étaient placés
après tous les droits et usages, dans la même rangée de boutons secondaires ;
les messages de confirmation n’avaient ni mise en évidence ni déplacement du
focus. Le bouton d’arrêt à échéance suggérait une démarche inutile en l’absence
de renouvellement automatique. Le test ciblé échouait bien sur sa présence.

Correction locale : résumé forfait/état/échéance en tête, renouvellement
principal, ajout de modules et changement de forfait secondaires. Modules acquis,
usages, catalogue, facturation et commandes sont séparés. Le devis remplace le
choix pendant sa revue ; l’acceptation des conditions et le total TTC sont
repérables. Les confirmations/erreurs sont titrées, contrastées, annoncées et
ramenées dans la zone visible avec focus. Facturation et demande de remboursement
peuvent être annulées sans écriture ; la demande de remboursement reste distincte
de sa décision et de son exécution. Le paiement est l’action principale du suivi
de commande, sans activation déduite du retour navigateur. Les notifications
antérieures sont effacées lors d’une nouvelle vérification explicite.

Le portail explique l’expiration sans renouvellement automatique et retire le
bouton d’arrêt. Les anciennes demandes restent affichées. La clarification est
dans [la spécification commerciale](modules-souscriptions-import-communication.md#5-achat-renouvellement-facturation-et-remboursement)
et **RM-07-05**, dont la numérotation et les preuves historiques sont conservées.
Le contrat serveur `/arret` n’est pas retiré. Les invariants restent dans le
domaine `abonnements_plateforme` ; aucun calcul de montant, droit ou transition
n’a été ajouté à l’interface.

Preuves locales :

- `node tests/browser/modules.mjs` : **52 scénarios intégrés, 784 assertions**,
  à 1280/390/320 px et texte 200 %. Achat, renouvellement actif/expiré, seuls
  modules achetés précochés, changement de forfait, facturation initiale/modifiée,
  annulation sans écriture, remboursement, ancien arrêt lisible, période future,
  lecteur, indisponibilité, conflit, pagination et compteur incertain. Devis et
  confirmations visibles/focalisés ; commande au clavier et aucune écriture
  avant confirmation. Retours réseau perdus et reprise avec la même clé vérifiés.
  Quatre rejeux ciblés Achat (**128 assertions**) ajoutent un contrôle du cadrage
  complet de la confirmation de paiement dans la zone de contenu de l’application,
  à chacune des quatre tailles/variantes, au-delà du seul focus.
- `node tests/browser/commercial-order-ux.mjs` : **24 scénarios** dans le
  composant réel avec API synthétique : paiement/remboursement, focus et annulation,
  refus des actions serveur/Achat, lien non HTTPS absent et reprise idempotente.
  Un manque de largeur à 320 px/200 % a été reproduit puis corrigé à la source :
  confirmation empilée avec largeur bornée et totaux en colonne. Contrôle du
  débordement dans le panneau, pas seulement dans la fenêtre.
- **244 tests Node réussis**, aucun ignoré ; TypeScript et lint réussis.
  Builds application et PWA isolés réussis, sans environnement opérateur ni
  fournisseur de paiement. Captures dans `tmp/modules-browser/` et
  `tmp/commercial-order-ux/` du dépôt Animation ; bureau/mobile/zoom inspectés.
- Revue indépendante : autorisation Achat et actions serveur, versions,
  acceptation, conditions de renouvellement et reprise incertaine préservées.
- Documentation : **97 guides, 1133 liens, aucune erreur**, **130 sources
  exportées** vérifiées ; `git diff --check` réussi dans les deux dépôts.

Impacts : Animation et documentation canonique uniquement. Pas de contrat,
backend, migration, générateur, donnée ni configuration d’exploitation à changer :
il s’agit de présentation des parcours existants, avec compatibilité des anciens
arrêts. Les styles sont corrigés dans les composants, sans surcharge CSS ajoutée.
État de l’epic inchangé. Aucune validation sur le site hébergé, aucun paiement
réel, commit, push ou déploiement effectué pour ce correctif.

## 31 octobre 2026 — correctif d’affichage de Localeo Animation

Retour utilisateur : espaces centrés et trop étroits dans neuf rubriques,
avertissements de l’assistant tardifs et action suivante peu accessible.
Base Animation **4ef51b2**, avec les modifications locales ci-dessous ; état de
l’epic inchangé. Les preuves de migration TEST de la section suivante sont
conservées et ne valent pas déploiement de ce correctif frontend.

Cause reproduite : à 1600 px, le conteneur Assistant occupait **960 px sur
1390 disponibles**, avec décalage de 215 px. Communication était plafonnée à
1080 px sur un écran de 1920 px. Les contraintes `mx-auto max-w-*` étaient dans
les composants. Elles sont retirées à leur source, sans ajout ni surcharge de
fichier CSS ; les champs, dialogues et aperçus conservent leurs bornes utiles.
La correction couvre Assistant, Live et ses événements, Préparation terrain,
Validations, Communication, Tirage/Gains libres et leur détail, Flyer et Bilan.
Les variantes Coffrets, déjà en pleine largeur, sont conservées.

L’assistant présente d’abord erreurs et avertissements, puis les étapes à faire ;
les étapes vérifiées sont repliables. La barre **Action suivante** reste accessible
depuis les rubriques et ouvre le parcours existant, avec focus et défilement vers
le début utile. La clôture conserve son aperçu, ses droits et sa confirmation.
La communication présente brouillon → destinataires → confirmation, avec action
de création en tête, conditions à la demande et refus visibles. Le lien **Voir
Mes modules** ouvre `/abonnement` seulement depuis la liste sans brouillon ;
aucun achat ni activation ne se déclenche.

Preuves locales :

- **244 tests Node réussis**, aucun ignoré ; TypeScript et lint réussis.
- **32 parcours navigateur** dans `animation-workspace-ux.mjs` : huit rubriques,
  1600/390/320 px et 320 px avec texte 200 %, hauteur 740 px. Largeur réelle,
  alignement, ordre des alertes, contenu du Flyer, absence d’écriture et visibilité
  complète du bouton avant clic après défilement. Le titre de la rubrique cible
  reste visible après navigation ; le test ne se repose pas sur l’auto-scroll du
  clic Playwright. Une troncature du CTA au zoom a été reproduite puis corrigée
  dans le bouton, avec libellé repliable.
- **12 scénarios UX Communication** à 1920/390/320 px, module actif/absent,
  autorisation manquante et période fermée ; lien vers les modules seulement
  depuis la liste et aucune écriture API.
- Régressions Communication : **36 scénarios, 684 assertions** ; Assistant :
  deux scénarios mobile/bureau ; Exploitation : deux parcours complets à
  1280/390 px, correction/retrait/clôture, refus et reprise du même reçu.
  Préparation terrain à 1280/390 px et navigation Flyer à 1280/320 px réussies.
  Bons numériques : **12 scénarios, 116 assertions** ; ce banc signale des
  sélecteurs synthétiques non simulés, renvoyés en 404, sans requête fournisseur
  ni erreur JavaScript. Leur couverture propre reste celle des tests de contrats.
- Build application et build PWA isolés réussis, sans fichier d’environnement
  opérateur. Captures dans `tmp/animation-workspace-ux/` et `tmp/communication-ux/`
  du dépôt Animation ; captures bureau, mobile et zoom inspectées.

Deux adaptations de bancs ont été nécessaires : le test juridique isolé ne
simulait pas le titre d’environnement déjà importé par la page ; le scénario
Exploitation attendait un ancien libellé de validation et ignorait le passage
actuel vers Commerces. Ces écarts sont constatés dans le HEAD initial ; les
assertions métier sont conservées, avec retour explicite vers Parcours et DTO
terrain simulé. La revue indépendante a fait corriger le défilement mobile réel
et confirme la conservation des droits et confirmations.

Le skill `localeo-corriger` précise désormais la simplicité des IHM Animation,
la priorité des alertes/actions et la correction des styles à leur source.
Sa validation `quick_validate.py` réussit, avec PyYAML chargé depuis un
répertoire temporaire isolé. Contrôles documentaires : **96 guides, 1098 liens,
aucune erreur**, **130 sources exportées** vérifiées et `git diff --check` réussi.
Impacts : projet et Animation uniquement ; aucun contrat, backend, schéma,
générateur ou paramètre d’exploitation modifié par ce correctif visuel.
La recette hébergée reste à effectuer après livraison. Aucun commit, push ou
déploiement effectué pour ce correctif.

## 31 octobre 2026 — migration du TEST partagé en v284

Migration demandée et exécutée sur la cible du profil privé backend `.env.test`,
initialement en v283. Le runner officiel a confirmé puis appliqué uniquement
`v284_e73_priorites_rappels_live.sql`, depuis backend `586a51f`, avec checksum
`d1242486cf1cf15eef4e8104aca93582f9444ec954b17d1e7b8f48df00140f61`.
Une seconde simulation ne trouve plus aucune migration en attente.

Sauvegarde PostgreSQL complète créée avant l'action : **54 935 984 octets**,
archive intégralement relue par `pg_restore` sans connexion à une base, sans
restauration en place. Archive, empreinte SHA-256 et reçus avant/après conservés
hors Git dans le backend :
`demonstrations/prive/operations/migration-v284-test-20261031T082158Z-5a702630/`.

Les trois nouvelles tables, trois index valides, référence nullable au token,
clé étrangère `ON DELETE SET NULL` et curseur initial sont vérifiés en SQL.
Aucun token historique déduit. Les effectifs installations, suivis, notifications
et participants sont identiques avant/après.

Contrôles HTTP sur `https://test-backoffice.localeo.city` : `/sante` **200**,
version **1.0.0+586a51f** ; readiness protégée **READY**, **134 contrôles**, aucun
objet manquant ; configuration publique Live **200** et catalogue public borné
à un résultat **200**. Aucun redémarrage n'a été nécessaire. Les préférences et
les traitements de rappel n'ont pas été activés par cette opération ; la recette
sur appareils et la réception réelle des Web Push restent distinctes.

## Accueil et rappels du 30 octobre 2026 — E73-EVO-LIVE-ACCUEIL-RAPPELS

Demande : un accueil personnel mobile donnant priorité aux participations presque
terminées ou bientôt échues, et deux rappels Web Push facultatifs.
Les [critères et contrats](localeo-live-entree-unique.md) complètent E73 ; son
statut global reste **En cours**. Bases Git : projet `55ef32a`, backend `baa559c`,
Marketplace `feb5d0e`, avec les modifications locales de cette évolution.
Réalisation enregistrée dans backend `586a51f` et Marketplace `7d9e0fc`.

L'accueil **Mon Live** conserve `/live/decouvrir`, la découverte publique et le
carnet existant. Les indicateurs proviennent du domaine ; l'interface ne déduit
ni qualification ni gain. La première priorité, les deux suivantes et les autres
participations se limitent à la page chargée, au plus 50 éléments ; les pages se
remplacent, avec état partiel explicite. Le lien personnel retrouve l'identifiant
exact du carnet, sans substituer le token d'une autre participation.

Les préférences `RAPPEL_PRESQUE_TERMINE` et `RAPPEL_FIN_PROCHE` sont indépendantes
et désactivées par défaut. La première exige une étape restante pour le Push ;
le seuil de 80 % concerne uniquement l'accueil. La seconde utilise l'échéance
effective dans les 72 heures. Préparation et transport revalident les droits et
états ; les réservations durables empêchent le réarmement par purge de l'inbox.
Une réservation annulée avant livraison reste consommée : aucun envoi effectif
ni réception ne peut être déduit du seul compteur de préparation.

| Critères | Preuves locales exécutées |
| --- | --- |
| E73-HOME-01/03 | Parcours navigateur mobile/bureau, visiteurs et carnet, ordre stable et entrées distinctes ; trois pages/150 ressources, au plus 50 cartes rendues. |
| E73-HOME-02 | Politique pure et tests dédiés : commencement, 80 %, une étape, 72 h, borne exacte de fin, inconnus et états terminaux ; régressions du moteur et des projections. |
| E73-HOME-04 | Tests API et transport réel du client : secret en en-tête, refus croisé, no-store, annulation ; ancien backend et erreur réseau explicites. PostgreSQL : token exact, expiré, révoqué, absent ou supprimé. |
| E73-HOME-05 | Navigateur : reprise de l'entrée exacte, absence sans substitution, actualisation explicite des accès avec refus partiels ; régressions carnet et Coffrets. |
| E73-HOME-06 | Captures inspectées à 320 px et texte agrandi à 200 % ; tests 320/390/1280 px, Tab puis Entrée vers le bon accès et cibles tactiles. Styles calculés sous mouvements réduits : transition de 0,2 s ramenée à 0,01 ms par la règle globale existante. |
| E73-ALERTE-01 | API, domaine et navigateur : défaut false, opt-ins indépendants, retrait, conservation des catégories/communes omises par un ancien client ; aucune demande automatique de permission. |
| E73-ALERTE-02 | Une étape, échéance effective, fusion des motifs et digest multi-participations ; texte de date en heure de Paris, été/hiver. |
| E73-ALERTE-03 | PostgreSQL : migration rejouable, deux workers concurrents, réservation unique, rollback et purge de l'inbox sans réarmement. |
| E73-ALERTE-04 | Domaine, application et worker simulé : fenêtre Paris 09–20, été/hiver, attente, préférence retirée et revalidation avant transport. |
| E73-ALERTE-05 | Lot borné et curseur durable, simulation et transport fournisseur simulé ; test SQL de pagination 50+5 et lectures groupées. |

Résultats vérifiés, sans additionner les suites qui se recouvrent :

- **786 tests backend réussis sur les sources figées** dans la passe finale
  unifiée : architecture et recensements des classes/cas d'usage, nouveaux
  domaine/application/API, registre démo, moteur/projections et régressions
  Web Push, catégories, notifications Coffrets/Animation, schema readiness,
  anciennes API et UI Live, inscription et notifications d'actualités.
- **11 cas PostgreSQL réussis**, aucun ignoré, dans
  `test_rappels_live_postgres_e73.py`, avec PostgreSQL 18 jetable local. La
  migration finale est rejouée deux fois et les deux index de clés étrangères
  sont introspectés. Après regroupement des contextes : **12 SELECT
  pour 1, 10 et 50 animations distinctes**, préparation active ou inactive.
  Tests de parité avec la lecture ordinaire et pagination inclus ; ce cas ne
  prouve pas la capacité ou la latence d'une population hébergée en charge mixte.
- **129 tests frontend `test:security` réussis**, aucun ignoré. Les contrôles
  transport du tableau de bord et helpers de tri/progression y sont inclus.
- **49 scénarios navigateur distincts réussis** au fil des lots, dont quatorze
  nouveaux. Passe finale de quatorze scénarios réussie après correction de la
  pagination et des réponses tardives pendant une actualisation ; les échecs intermédiaires d'assertions UI ont été corrigés et
  rejoués. Build PWA isolé et ESLint sur sources/tests/scripts/configuration
  réussis. Le lint global reste empêché par un refus local `EPERM` dans
  `output/bum-politique/pytest-approval-1` ; aucune permission n'a été changée.

Les nouveaux registres suivent le remplacement/restauration du générateur.
**14 tests du registre réussis**, dont conservation des réservations après purge
de l'inbox et restauration des dépendances, inclus dans les 786 tests.
Le runner complet de compatibilité a exécuté dix scénarios : **neuf réussis**,
dont dump, installation, échec injecté, reset après changement de schéma et
restauration exacte ; le dixième a échoué uniquement sur la comparaison des
empreintes sources, un fichier API ayant été édité pendant son exécution.
Après gel de `app/templates/sql` et application de la migration finale sur le
builder jetable, ce scénario complet a été **rejoué avec succès** (157,74 s),
sans affaiblir l'assertion. Les dix scénarios disposent donc d'une réussite,
obtenue en deux passes. Les sept avertissements du premier passage et celui du
rejeu concernent la réflexion SQLAlchemy `dialect_options`, sans échec de lecture
ou de restauration. Les sorties sont dans les répertoires `tmp/live-rappels-demo-*`
du backend et les captures dans `test-results/live-game` de Marketplace.

La revue indépendante des contrats a conduit à lier le token exact, préserver
les préférences omises par un ancien client, revalider chaque abonnement avant
transport et conserver un tag stable. Sa dernière lecture ne relève plus de
réserve. Les lectures de contexte sont groupées entre animations et l'indicateur
d'accès à actualiser utilise `EXISTS` ; aucun comptage global des suivis n'est
nécessaire. Les tests de parité vérifient configuration effective, préparation,
retrait commerçant et neutralisation de chasse, avec les règles ordinaires.

Les contrats OpenAPI E41 et E42 sont générés hors ligne, avec réponses typées du
tableau et de la préparation batch et configuration additive. Trois dépôts sont modifiés : projet, backend,
Marketplace. Animation et Pro n'ont aucun nouveau parcours ni commande.
La migration additive `v284_e73_priorites_rappels_live.sql` précède backend puis
frontend. Les anciens suivis ne sont pas rattachés arbitrairement à un token :
**Actualiser mes accès** utilise les seuls tokens du carnet, sans réinscription
ni opt-in. Les [consignes d'exploitation](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrivent les deux batchs, leur simulation et leur activation.

La recette HTTPS sur TEST, les permissions/abonnements de véritables appareils,
la réception Web Push et les mesures de charge mixte restent à exécuter après
livraison. Six parcours complémentaires `RM-LIVE-HOME-01` à `03` et
`RM-LIVE-RAPPEL-01` à `03` sont préparés dans la [recette métier](recette-metier.md),
sans barrer ni valider leur recette hébergée. Les contrôles documentaires finaux
réussissent : 94 guides, 1 043 liens locaux, aucune erreur ; 130 sources exportées
vérifiées. `git diff --check` réussit dans les trois dépôts. Les deux clusters
PostgreSQL jetables et le serveur navigateur de test sont arrêtés.
Aucun fournisseur réel, environnement partagé ou navigateur utilisateur
n'a été sollicité pendant la validation. Les commits applicatifs sont poussés
sur `origin/main` à la demande de l'utilisateur après cette validation locale ;
aucune action directe de déploiement n'est exécutée.

## Complément UX du 30 octobre 2026 — E73-EVO-LIVE-UX

Demande : simplifier la navigation et donner envie de participer grâce à la
dynamique réelle des animations. [Critères UX et sémantique des chiffres](localeo-live-entree-unique.md#complément-ux-du-30-octobre-2026--e73-evo-live-ux).
Bases de validation : Marketplace `0a2de86`, backend `245f7d8`, documentation
`69e7e84`, avec les modifications décrites ci-dessous. Réalisation enregistrée
dans Marketplace `feb5d0e` et backend `3a6f930` ; le profil CORS Coffrets TEST
est enregistré séparément dans le backend `c25d202`.
Le statut global E73 reste En cours.

- Marque conservée dans l'en-tête, rappel retiré du contenu Découvrir ;
  raccourci icône redondant supprimé en surface Animation. Boussole Découvrir
  et repère Mes communes avec leurs libellés ; marque vers la découverte.
- Recherche de commune retirée de Réglages ; anciens liens `?focus=city`
  conservés par accès à Mes communes. Pas de première commune choisie
  automatiquement. Les préférences de notification sont lues à l'ouverture,
  sans PUT implicite. Une sélection vide explicite reste distincte d'une
  préférence locale absente ou inaccessible, qui conserve les communes serveur.
- Cartes illustrées avec statut, défi configuré et trois métriques publiques :
  inscriptions présentes, gagnants courants distincts et unités de dotation.
  Les valeurs inconnues ou invalides ne deviennent pas zéro. Le total de lots
  n'est ni le nombre de types, ni le stock restant. Aucun faux flux d'activité,
  classement, taux de gain ou progression personnelle n'est inventé.
- Nouvelle lecture backend groupée sur les identifiants visibles de la page,
  maximum 50, une instruction SQL supplémentaire, sans lecture par carte.
  Le compteur d'inscrits et les états d'attribution restent ceux du backend ;
  aucun contact, token, nom de participant ou donnée personnelle n'est publié.
  Contrat OpenAPI additif `dynamique`, champs optionnels non négatifs ou nulls.

La revue indépendante vérifie notamment les attributions remplacées, suppléants,
tirages libres non confirmés, quantités Coffrets et null contre zéro. Les
retours ont aussi couvert les grands nombres sur mobile et la conservation des
communes serveur sans choix local explicite. La reproduction de navigation est
rouge avant correction (`tmp/live-ux-navigation-reproduction.log`). Le premier
test de case de notification exigeait une modification immédiate : les traces
montrent le PUT 200 correct ; le scénario attend désormais l'état confirmé,
avec conservation des assertions de contenu et du refus 503.

Validation backend : **20 tests ciblés réussis** dans
`tmp/live-dynamique-final.log`, dont 50 identifiants lus en une instruction,
et **620 contrôles d'architecture réussis** dans
`tmp/live-dynamique-architecture.log`. Une suite plus large conserve **29
réussites et un échec OpenAPI préexistant** : la route binaire
`GET /protected/animation-locale/animations/{animation_id}/flyer/illustration`
n'est pas recensée dans la liste binaire du test global des response models.
L'échec est reproduit sur le HEAD initial `245f7d8` dans une copie isolée,
preuve `tmp/live-dynamique-baseline-api.log` ; aucune assertion ou exclusion
affaiblie. Le test de coût PostgreSQL est adapté à une lecture supplémentaire
fixe et bornée, sans être déclaré exécuté sur PostgreSQL.

Le test F12 existant révèle aussi
[ANO-MPL-E73-LIVE-03](../../roadmap/anomalies/marketplace.md) : les entrées locales
dans Live rechargeaient le document complet. Les liens du routeur conservent
la navigation interne, tout en acceptant le domaine configuré lorsqu'il est
externe. F12 repasse avec les mêmes contrôles de mémoire, de service worker et
de saisie. Le scénario historique de catalogue attendait les anciens sélecteurs,
routes et informations de gain dans la découverte : il est adapté au catalogue
public, et ses assertions de gagnant, lot, QR personnel et historique sont
conservées dans le détail autorisé et Mes participations (`LiveCatalogContinuity`).

Le contrat E41 est limité aux deux schémas concernés (55 lignes ajoutées).
L'export complet hors ligne révèle une dérive historique plus large et reste
dans les sorties de travail ; elle n'est pas incorporée à cette évolution.
Les vérifications navigateur couvrent **40 scénarios distincts** sur plusieurs
lots : découverte et métriques, communes, stockage absent/corrompu/vide,
notifications (401/503 et reprise), anciens Coffrets, avis et sauvegarde,
dialogues et continuité des accès personnels. Journaux Marketplace :
`tmp/live-ux-restants-reprise1.log` (23 réussites),
`tmp/live-ux-integration-finale.log` (quatre scénarios d'avis et reprise réussis,
puis un échec de chargement initial rejoué dans le lot suivant),
`tmp/live-ux-notifications-regression.log` (11 réussites et les deux écarts
ci-dessus), `tmp/live-ux-derniers-rejeux.log` (six réussites après correction et
adaptation). Des reprises sont nécessaires après des dépassements du délai de
chargement initial ; aucune assertion de comportement ni délai n'est affaibli.
La revue des captures à 200 % fait passer les métriques de colonnes fixes à des
blocs qui se répartissent selon leur contenu, afin de garder les grands nombres
lisibles. Le défi dit « validations à réaliser », sans laisser croire qu'un
passage suffit pour une tombola avec achat confirmé. La chasse ne publie pas ce
seuil numérique. **125 tests Node réussis**, journal `tmp/live-ux-security.log`.
Le dernier rejeu des quatre scénarios de dynamique passe sur le libellé et le
CSS finaux (`tmp/live-ux-dynamique-finale.log`), y compris trois milliards d'unités
en dotation à 390 px et texte 200 %, sans morceler les nombres. Captures relues
dans `tmp/live-ux-preuves/`. ESLint sources et tests touchés réussi ; contrôles
documentaires : 97 guides, 1 069 liens locaux, aucune erreur, et 130 sources
exportées vérifiées. `git diff --check` réussi dans les trois dépôts modifiés.
Les échecs et reprises de harnais restent dans les sorties privées de travail.
Les tests navigateur utilisent un build isolé et des fixtures, sans trafic réel.
Les tests SQL utilisent une base jetable : les plans PostgreSQL et la tenue en
charge restent à mesurer avant activation. Le cache public existant
(60 secondes, puis stale-while-revalidate 300 secondes) est conservé : les
compteurs ne constituent pas une promesse de temps réel.

Impacts : backend, Marketplace et contrat canonique E41 ; pas de migration,
nouveau rôle, nouveau compte, permission, fournisseur ou paramètre. Les règles
de participation et les données existantes sont conservées ; les fixtures
évoluent sans génération de démonstration réelle. Pas de changement ERP, Pro,
portail organisateur ou batch. Les commits sont créés à la demande de
l'utilisateur après validation ; aucun déploiement ni mutation du TEST partagé
pour ce complément. Aucun scénario historique de recette barré.

## Évolution locale du 30 octobre 2026 — E73-EVO-LIVE-UNIQUE

Demande : [Live comme entrée unique](localeo-live-entree-unique.md), à
`animations.localeo.city`, avec une UX mobile d'abord. Arbitrage utilisateur :
aucun nouveau compte habitant ; suivi des communes sur l'appareil.

Implémentation dans `localeo-marketplace`, commit `0a2de86` (base `8d42619`) :
navigation basse Découvrir / Mes participations / Mes communes ; sélection
multiple persistée, GPS volontaire et repli manuel, contexte de commune partagé
sans remplacement silencieux des préférences. Catalogue public séparé en deux
périodes, pages indépendantes et deux lectures concurrentes, résultats progressifs,
erreurs partielles et sélection temporaire en cas de stockage refusé.

L'ancien catalogue et `surface=animations` quittent l'interface marketplace.
La configuration choisit l'origine Live ; seuls les contextes publics autorisés
sont repris. Les liens des menus, cartes, recherche, agenda et présentation
Animation utilisent cette destination. L'inscription réutilise son formulaire
et ses commandes sous le scope `/live/`, avec maintien des liens personnels.
Avant changement d'origine avec un carnet, la reprise volontaire conserve les
identifiants et accès sans effacement ni nouvelle inscription. L'assistant
conserve aussi la fiche/inscription, commune et source jusqu'à la destination.

La fiche reste consultable publiquement si l'enrichissement d'une installation
existante échoue. Aucun nouveau contrat, compte, rôle, schéma, migration SQL,
référentiel, notification ou recommandation. Pas de changement backend, ERP,
batch, Pro ou portail organisateur ; les modèles d'anciens liens restent acceptés.
Les fixtures frontend couvrent les données existantes sans génération réelle.

Le test de stockage bloqué a reproduit et permis de corriger
[ANO-MPL-E73-LIVE-01](../../roadmap/anomalies/marketplace.md) : la lecture locale
indicative du carnet ne doit pas masquer un reçu personnel valide. L'inscription
reste unique et le réessai ne porte que sur l'écriture locale. Les assertions
de succès, reçu et QR sont conservées. Les attentes de navigation remplacées
sont adaptées à cette décision produit ; les assertions de dates des coffrets
utilisent le format français existant du rendu, avec la même échéance précise.

Revue indépendante : stockage refusé et rendu progressif corrigés, contexte
conservé dans l'assistant, règles de capacité/origine et autorisations serveur
préservées. L'en-tête mobile conserve la marque et les actions utiles ; l'action
d'installation reste dans les réglages. Les captures à 320/390 px servent à
vérifier l'absence de débordement et les cibles tactiles, pas une tenue en charge.
La revue visuelle à 200 % a révélé des libellés tronqués dans le menu bas :
hauteur adaptable et réserve mesurée sous le contenu corrigent ce défaut.
Le test contrôle désormais les limites complètes des libellés et la réserve.

| Critères | Preuves locales et limites |
| --- | --- |
| LIVE-01/02/03/06/11 | `live-discovery-unique.spec.cjs`, `live-followed-communes.test.cjs` : lecture publique, communes, périodes, pagination, GPS, stockage, contexte, mobile. |
| LIVE-04/05/08 | `live-carnet.spec.cjs`, `live-animation-surface.spec.cjs`, sauvegarde/import : inscription et reprise, plusieurs participations, QR, actualisation, anciens Coffrets. |
| LIVE-09/10 | `live-entry-redirects.spec.cjs`, `live-entry-routing.test.cjs` : anciennes entrées, contexte, destination autorisée, assistant et liens directs. |
| LIVE-07/12 | Fallback SPA et build locaux contrôlés ; DNS/TLS, domaines hébergés, installation PWA réelle et recette de bascule à exécuter avant activation. |

Validation finale : **53 tests navigateur réussis** en une seule série séquentielle
sur l'arbre final (`tmp/live-unique-validation-complete.log`, 7,1 minutes),
**125 tests Node de sécurité** et **13 tests serveur** réussis ; ESLint sur les
sources et tests touchés réussi. Les scénarios couvrent géolocalisation et replis,
320/390 px, texte à 200 %, navigation clavier, réduction des mouvements,
détail public sans installation disponible, inscription sans nouveau compte,
stockage refusé, avis personnels, export/import du carnet, anciens accès
Coffrets et liens directs vers Live. Deux séries parallèles ont dépassé le délai
de cinq secondes sur le chargement initial ; la reprise utilise le worker unique
prévu par la configuration du dépôt, sans changer les assertions ni les délais.
La revue indépendante des hauteurs et des liens est favorable.

Contrôles documentaires : **97 guides, 1 065 liens locaux, aucune erreur** ;
**130 sources exportées vérifiées**. `git diff --check` réussi dans les deux dépôts.
Les journaux sont conservés dans `localeo-marketplace/tmp/` et les captures
relues dans `tmp/live-unique-preuves/` (sorties locales ignorées par Git).

Les tests utilisent un build isolé, des API simulées et un garde réseau ; ils
ne constituent pas une recette sur les domaines hébergés. Aucun scénario
historique de recette n'est barré par ces tests d'évolution. Le statut E73 reste
**En cours**. Les commits et leur push sont demandés séparément après cette
validation. Aucun déploiement n'est effectué ; le clone métier figé reste inchangé.

## Correction locale du 30 octobre 2026 — E73-EVO-UX-ERP

Demande : une entrée par fonction dans Animation ERP, en-têtes et retours
harmonisés. Réalisation dans `localeo-backend`, base `3720a08` avec travaux
locaux préexistants conservés, et dans cette documentation. Les autres
applications ne sont pas modifiées par cette intervention.

| Critère | Résultat et preuve |
| --- | --- |
| E73-EVO-UX-ERP-01 | 17 destinations directes classées en Animations / Équipes et contrats / Offre et modules / Pilotage ; actions Nouveau dans leurs listes, accueil récapitulatif et anciens fragments conservés. `animation-navigation.test.mjs` vérifie le menu réellement servi et ses destinations ; le navigateur vérifie droits, entrée active et demandes d’organisation distinctes des accès |
| E73-EVO-UX-ERP-02 | `animation-navigation.js` fournit les en-têtes du shell et des trois modules autonomes ; quatre consoles et Offres et tarifs utilisent la même structure et CSS. Retour liste/espace, détail/liste, lot/animation ; filtres seulement depuis parent de même origine. Captures relues à 320/1280 px ; liens du menu et retours principaux visant 44 px. La saisie reste protégée lors du retour (annulation du départ conserve le champ) |
| E73-EVO-UX-ERP-03 | Session, droits, lecture seule, CSRF, idempotence, conflits et reprise après réponse perdue conservés ; rendu Support inchangé. Retour des consoles vers l’accueil ERP si la consultation de l’espace Animation n’est pas autorisée ; trois tests rouges avant correction puis réussis, conservation toujours refusée hors ADMIN |

Revue indépendante intégrée : accès aux offres globales rétabli comme fonction
distincte du catalogue par commune ; impasse des opérateurs spécialisés corrigée.
Lecture des captures : liens imbriqués initialement affichés en ligne, test de
reproduction échoué (`inline` au lieu de `block`) puis réussi après correction
CSS. Les anciennes assertions de libellé de retour ont été adaptées à la
hiérarchie explicitement demandée, sans supprimer les contrôles clavier,
de largeur, de données ou de permissions.

Validation sur l’arbre final :

- **767 tests Python réussis**, code 0, via `scripts/validation/test_isolated.py` :
  architecture/domaine/couverture, navigation des consoles, shell équipe et assets,
  accès internes, nouveaux tests `test_animation_console_navigation.py` et suites
  `test_admin_specific_ui_system.py` / `test_animation_locale_admin.py`.
- **4 tests Node réussis** dans `tests/frontend/animation-navigation.test.mjs` :
  fonctions actives, menus, parents et refus de référents hostiles.
- `tests/browser/animation-navigation-erp.cjs` : **26 contrôles réussis** sur
  320/1280 px, menu, navigation, capacités, formulaire modifié et retours.
- Les quatre suites `generation-erp.cjs`, `preparation-erp.cjs`,
  `exploitation-erp.cjs`, `conservation-erp.cjs` passent avec **18 parcours**,
  y compris les retours et leur cible tactile, les refus et les reprises.
- Huit suites navigateur adjacentes passent : `epic73-suivi-produits.cjs`
  (ERP et Support), `epic73-reversibilite.cjs`, `epic73-pilotage-economique.cjs`,
  `epic73-checkout-erp.cjs`, `epic73-modules-erp.cjs`, `equipes-animation-erp.cjs`,
  `epic73-preparations-service.cjs`, `epic73-sollicitations.cjs`.

Les effectifs de tests, contrôles et parcours sont distincts et ne s’additionnent
pas. Vérifications navigateur sur fixtures sans appel externe, base réelle ni
envoi de message. Les quatre suites consoles utilisent leur HTML réel et les
nouveaux tests Python utilisent les vrais renderers ; la page des offres est
couverte sur son rendu HTML/échappement, sans recette d’une édition réelle.

Pas de modification de domaine, contrat OpenAPI, données, migration ou
générateur : présentation et navigation uniquement. Les assets supplémentaires
sont servis dans le backend avec session et `no-store`, sans nouveau réglage.
Les exports documentaires doivent accompagner une livraison backend autonome.
La recette connectée après livraison reste à effectuer ; aucune conformité
complète d’accessibilité ni validation terrain n’est déduite de ces tests.
Aucun commit, push ou déploiement réalisé.

## Évolution locale du 30 octobre 2026 — E73-EVO-UX-PUBLIC

Retours sur le site public TEST : ajout de la géolocalisation volontaire,
reprise des codes visuels Coffrets et navigation Live centrée sur les animations.
Les critères et l’analyse UX sont dans les [parcours canoniques](perimetres-parcours-saas.md).
Périmètre modifié : `localeo-marketplace` et documentation `localeo-projet`.
Bases respectives `70d7128` et `6e46edd`, avec travaux locaux préexistants conservés.

| Critère | Réalisation et preuve |
| --- | --- |
| E73-EVO-UX-PUBLIC-01 | `AnimationLocationPicker` utilise le contexte territorial E52 dans un POST annulable, sans mise en cache des coordonnées ; refus, délai, indisponibilité, commune hors réseau, précision approximative, absence de GPS et réponses tardives couverts par `animation-discovery.spec.cjs`. La revue indépendante a identifié un callback périmé pouvant écraser les filtres et un message périmé après retour navigateur : corrigés avec callback courant et réconciliation du message, scénarios ajoutés |
| E73-EVO-UX-PUBLIC-02 | En-tête bleu profond, orange et typographies partagées, commune/filtres avant les animations sur ANIMATION, trois étapes de présentation ; composition du catalogue Coffrets conservée. Captures 320/1440 px relues, correction du lien d’évitement et des numéros d’étapes sur mobile ; clavier et texte 200 % couverts par le scénario existant `animation-saas-public.spec.cjs` |
| E73-EVO-UX-PUBLIC-03 | `LiveCarnetHeader`, `liveStore` et état vide adaptés ; `live-animation-surface.spec.cjs` couvre les deux surfaces, les rubriques mémorisées, le lien direct et l’ajout d’un ancien Coffret avec conservation en IndexedDB. Aucun effacement de carnet |

Reproduction initiale : le scénario GPS échoue sur l’absence du bouton avant
correction. Les premières passes ont aussi révélé une association de libellé
à préciser et deux routes de fixture manquantes pour la lecture d’un Coffret ;
markup et fixtures corrigés sans assouplir les assertions ni le blocage réseau.
Une passe élargie avec délai local réduit à 30 secondes a affiché 29 succès et
un dépassement sur la reprise d’avis ; le rejeu avec le délai habituel de
90 secondes du projet a confirmé ce scénario et les 17 autres de cette passe
(18 succès, code 0). Les passes se recoupent et ne s’additionnent pas.

Bilan navigateur : **32 scénarios distincts réussis** dans les cinq fichiers
`animation-discovery`, `live-animation-surface`, `animation-saas-public`,
`animation-source-merchant` et `discovery-premium` (`tests/visual/*.spec.cjs`).
Dernière passe après conservation explicite de la composition Coffrets : les
11 scénarios découverte réussissent (code 0), dont les deux courses GPS, le
retour navigateur et le catalogue Coffrets. Les 18 scénarios de la passe
précédente incluent les tests de satisfaction, de reprise et de conservation
des anciens accès. Les 13 autres couvrent diffusion, commerce et découverte
Coffrets. Aucun test ignoré. Contrôles documentaires : 98 guides, 1130 liens
locaux et 130 sources exportées vérifiés sans erreur ; diffs sans erreur.

Autres contrôles : deux tests Node surface/reprise/commande personnelle et
13 tests serveur réussis (codes 0) ; build Vite isolé des `.env` exécuté par les
parcours navigateur. ESLint sur `src` et les deux nouveaux fichiers de tests
réussi. `npm run lint` global n’a pas pu parcourir des dossiers temporaires
locaux (`output/bum-politique/pytest-approval-1`, puis `tmp/address-architecture`,
erreurs `EPERM`) ; aucun changement d’ACL, suppression ou exclusion permanente.

Lecture distante sans mutation : le site TEST sert la surface ANIMATION avec
API `https://test-api.localeo.city`. OPTIONS du POST territorial depuis cette
origine publique répond 200 avec `Access-Control-Allow-Origin` exact. Aucun
POST de position réelle envoyé. La permission GPS réelle, la résolution sur
téléphone et la version déployée après livraison restent à recetter.

Pas de changement backend, OpenAPI, migration, données ni générateur : la
projection territoriale et les règles de participation/gain sont réutilisées.
Pas de collecte Analytics supplémentaire ; stockage et accès personnels
préservés. Les recommandations de confirmation d’inscription, de prochaine
action et de mise en scène des acquis du jeu sont une analyse, pas une
implémentation déclarée terminée. Le fil d’actualités Live et ses filtres
existants, dont Coffrets, restent inchangés. Aucun commit, push ou déploiement.

## Évolution locale du 30 octobre 2026 — E73-EVO-DOMAINES

Décision acceptée : site public `animations.localeo.city`, portail organisateur
`gestion-animations.localeo.city`, marketplace Coffrets conservée sur un autre
service. Équivalents TEST : `test-animations`, `test-gestion-animations` et
`test-marketplace`. Cette évolution remplace le profil TEST qui réutilisait
l’accueil de la marketplace. Les preuves de recette antérieures restent
historiques ; aucun nouveau déploiement n’est revendiqué.

| Critères complémentaires | Sources / résultat local | Preuves exécutées |
| --- | --- | --- |
| E73-EVO-DOMAINES-01 | Quatre profils Marketplace Coffrets/public, deux profils gestion, exemples et guides distincts ; défaut local Coffrets conservé | 8 tests Marketplace configuration/surface/reprise et 5 tests build-environment Animation ; quatre lectures HTTP locales `app-config.js` et deux validations de profils de gestion |
| E73-EVO-DOMAINES-02 | Compléments backend production/TEST pour templates publics, portail, origines exactes et retours de paiement ; aucune règle métier modifiée | 98 tests `tests/security/test_animation_browser_session.py` dont contrôle des deux profils : public refusé malgré son autorisation CORS générale ; 618 contrôles architecture/domaine/couverture |
| E73-EVO-DOMAINES-03 | Contrôle de build Pro autorise le site public exact ; API/Marketplace/Coffrets historiques conservés, gestion et origines TEST refusées en production | 50 tests unitaires Pro ciblés ; 6 tests navigateur `validation-security.spec.js` avec nouveaux QR, anciens QR et refus sans appel de résolution |
| E73-EVO-DOMAINES-04 | Harnais E73 sépare `publicAnimation` de `marketplace` ; clone historique 18776 compatible, 18778 explicite ; aucune réécriture de campagne privée | 363 tests Node E73 puis 114 ciblés après correction de l’allowlist RM-X-03, qui bloquait la nouvelle origine dans ses contextes de fuseau ; test d’abord en échec puis réussi. Suites recoupées, effectifs non additionnables |

Commandes reproductibles :

- Backend : `python scripts/validation/test_isolated.py tests/security/test_animation_browser_session.py -q` ; contrôles architecture selon le guide backend ; dernier ciblé Node : `node --test tests/frontend/recette-e73-public-operations.test.mjs tests/frontend/recette-e73-core.test.mjs tests/frontend/recette-e73-isolated.test.mjs` (114 succès).
- Marketplace : `node --test tests/security/public-config.test.cjs tests/security/animation-surface-satisfaction.test.cjs tests/security/library-backup.test.cjs`.
- Gestion : `node --test tests/build-environment.test.mjs`.
- Pro : `npm test -- src/lib/api/productionConfig.test.js src/lib/api/demoConfig.test.js src/features/animations/model.test.js src/features/animations/publicOrigins.test.js` ; `npm run test:e2e -- tests/e2e/validation-security.spec.js`.

Le lot Node complet de 363 succès a été exécuté avant le dernier ajout RM-X-03 ;
il compte désormais 364 tests, sans nouveau passage intégral après ce ciblé.
Sous PowerShell, son lancement développe explicitement les fichiers :

```powershell
$recetteTests = @(rg --files tests/frontend | Where-Object { $_ -match 'recette-e73-.*\.test\.mjs$' })
node --test @recetteTests
```

Revue indépendante : contrôle de la séparation des origines et des profils,
compatibilité des anciens QR et clones ; correction de l’allowlist de fuseau et
ajout des retours de paiement explicites à la procédure de bascule. Le défaut
était dans le harnais, aucun invariant métier n’a été changé.
Sans impact sur les schémas OpenAPI, les migrations SQL, les rôles, les
générateurs ou les données de démonstration : les URL consomment les templates
existants, et aucune nouvelle donnée ni permission n’est requise.

**Reste à livrer** : DNS/TLS, association aux services, injection des profils,
reconstruction/déploiement et recette hébergée des nouveaux domaines, anciens
liens personnels et carnets. Aucun build de livraison, commit, push ou
déploiement effectué pour cette évolution. Les validations locales ne prouvent
pas que les domaines pointent déjà vers les services cibles.

## Restrictions et état initial

Implémentation, bases jetables locales, tests isolés et commits locaux uniquement. **Aucun push, pipeline distant, déploiement, migration/configuration de test/démo/production, envoi réel ou paiement réel.** Les vérifications humaines et hébergées restent des étapes futures explicites. Ne pas confondre commits et livraison.

**Ancienne consigne du 19 octobre 2026 : terminer le lot 09 puis s'arrêter, sans
commencer le lot 10.** Elle a été remplacée par la reprise ci-dessous. Les réserves
« à réaliser au lot 10 » dans les bilans antérieurs décrivent leur état à cette date ;
le bilan du lot 10 indique leur traitement et les limites encore présentes.

**Reprise autorisée le 19 octobre 2026 : implémenter le lot 10 et terminer le
travail local de l'epic.** Cette nouvelle demande remplace l'arrêt précédent ;
les interdictions de push et de déploiement restent applicables. Les recettes
humaines et preuves sur l'hébergement cible ne sont pas autorisées par cette reprise.

| Dépôt / branche | HEAD initial | Travaux préexistants à préserver |
| --- | --- | --- |
| Projet / main | `cc9991dd3679075e232f53844362405acfdc77a2` | Spécification E73 et règles associées à committer séparément ; modification étrangère `docs/specifications/moteur-animation/suivi-implementation.md` exclue |
| Backend / main | `31807b633932c2a53bb64714e978359683f9cfe1` | Aucun changement suivi |
| Animation / main | `08863e8202a3caad3c886918b0543cd2f260aec3` | README, App.tsx, ExploitationView.tsx, tests/browser/exploitation.mjs : conservation et staging sélectif requis |
| Commerçant / main | `19f7a20ebedae79f50453aefbf48c9724ed28eb1` | Aucun changement |
| Marketplace / main | `4186e44e8320a9c016d678da3f28583849452867` | Aucun changement |

## Plan et statut des lots

| Lot | US / portée | Dépôts prévus | État / preuves / commits |
| --- | --- | --- | --- |
| 00 | Sources, référence initiale, protocole UX et suivi | Projet ; lecture des quatre applications | Sources et contrôles de référence : commit Projet `be776b1` ; matérialisation des squelettes UX poursuivie dans les lots applicatifs |
| 01 | US25–26 comptes, équipe, organisation, récupération, transfert | Backend, Animation, Projet | Implémenté et vérifié localement pour CA50–53 ; backend `45d0b56` et preuve complémentaire `a17e3f4`, Animation `05c0561`, Projet `9519696` ; limites de conservation et recette hébergée ci-dessous |
| 02 | US11–13 ; parties US24/36, périmètres et onboarding | Backend/ERP/OnBoard, Commerçant, Animation, Projet | Implémenté et vérifié localement pour les produits existants ; Backend `261ebdc` et raccord asset `59d89d0`, Pro `bc9d1ac`, Animation `7cab528`, Projet `afd77cd` ; branches numériques et exploitabilité reprises aux lots 05/10 |
| 03 | US03,14–17,27–28 ; souscriptions/modules/finance | Backend, Animation, Pro (contrat), Projet | Implémenté et vérifié localement ; Backend `4f3a3b1`, Animation `79903e3`, Pro `8212252`, Projet `6a3d747` ; activation des modules futurs aux lots 06/07/08 |
| 04 | US01–02,04 ; branche externe US07–08 | Backend, Animation, Marketplace/Live, Pro (contrat), Projet | Implémenté et vérifié localement ; Backend `7502282`, Animation `d0b92f7`, Marketplace `1473e05`, Pro `30aeed3`, sources dans le commit documentaire lot 04 ; branche numérique au lot 05 |
| 05 | US05–10 ; complément numérique US07–08 | Backend, Animation, Commerçant, Marketplace/Live, Projet | Parcours implémentés et vérifiés localement ; commits et limites de conservation/performance ci-dessous ; aucune mise en service |
| 06 | US19–20 ; import/deltas/reprise | Backend, Animation, Projet | Implémenté et vérifié localement ; Backend `bb4e1e8`, Animation `955fb94`, sources dans le commit documentaire du lot 06 ; preuves et limites ci-dessous |
| 07 | US18,30 ; chasse et préparation accompagnée | Backend, Animation, Projet | Implémenté et vérifié localement ; Backend `44c6429`, Animation `8979893`, Projet `7f80a6c` ; recette humaine et hébergement non exécutés |
| 08 | US21–22 ; communication participants | Backend, Animation, Marketplace/Live, Projet | Implémenté et vérifié localement : campagnes, préférences Live, quotas, fréquence et alertes internes ; consolidation conservation/restauration au lot 10 |
| 09 | US23,29,31–33 ; parcours/site/assistance/bilans | Backend, Animation, Marketplace/Live, Projet | Implémenté et vérifié localement ; Backend `76103d7`, Animation `eb3def9`, Marketplace `70d7128`, sources dans le commit documentaire du lot 09 ; démonstration complète : dix réussites |
| 10 | US34–38 ; finalisation US24, exploitabilité/pilote | Backend/ERP/Support/Ops, Animation, Projet ; vérification Pro/Live et démonstration | Implémentation et contrôles locaux terminés : Backend `7f74166`, Animation `da86e39` et `3801cc5`, sources dans le commit documentaire lot 10 ; recette humaine et preuves hébergées non exécutées |

Les US partagées ne sont acquises qu’après toutes leurs branches. Reprendre les identifiants CA du plan de vérification, sans en changer la portée. Chaque bilan de lot doit enregistrer fichiers/contrats, migrations, fixtures, commandes, résultats, revue, limites et commits par dépôt. Si nécessaire, subdiviser un lot en incréments explicitement non terminaux ; aucune validation par simple présence d’un fichier.

## Préparation UX et capacité

Le squelette gestion et le squelette communication ainsi que leurs parcours de référence sont définis dans [les parcours SaaS, section 5](perimetres-parcours-saas.md). Les premières réalisations doivent matérialiser organisation/commune, navigation stable, états vides/erreurs et continuité des formulaires. Prévoir une revue locale du parcours organisateur liste → création → contrôle de publication et du parcours visiteur découverte → inscription → Live avant généralisation. La recette humaine suit Localeo puis Martignas-sur-Jalle ; elle n’est pas encore réalisée.

Capacité : 10 communes, 10 000 participants au total, 10 utilisateurs actifs simultanément ; paliers et distributions concentrées décrits par E73-PERF-01 à 08. Les tests hébergés, RPO 4 h/RTO 8 h sur hébergement représentatif et ouverture du pilote restent **non exécutés**. Les essais locaux n’en constituent pas une preuve de livraison.

## Dépendances et contrôles initiaux

E55, E68, E70 et E72 restent dans leur état produit propre. Les contrats et implémentations réels sont relus pour chaque lot dépendant ; leur existence ne prouve pas une disponibilité hébergée. E71 reste une epic indépendante ; adapter les projections nécessaires sans réaliser implicitement tout le CRM.

- Documentation : `check_guidance.py` ciblé : 102 guides, 1 181 liens, zéro erreur/avertissement ; `sync_documentation.py --check-sources` : 122 documents vérifiés ; `git diff --check` réussi.
- Backend : `scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q --basetemp .artifacts/e73-baseline-20261018-01 --tb=short` : **467 réussites**. Le premier essai sans répertoire temporaire explicite comptait 452 réussites et 15 erreurs de permission du répertoire Windows temporaire ; la reprise isolée dans le workspace les résout sans modifier les assertions.
- Animation : baseline frontend confiée au lot 01 ; résultat à consigner.
- PostgreSQL : inventaire local en lecture seule ; aucune connexion à une base d’exploitation.

## Journal de réalisation

### Lot 00 — Préparation

Lecture des instructions, inventaire des cinq dépôts et répartition des responsabilités. Backend lot 01 et frontend lot 01 confiés à des agents distincts, sans permission de commit/push ; intégration et commits par l’agent principal. Inventaire de tests PostgreSQL confié en lecture seule. Aucun changement applicatif déclaré validé à ce stade.

### Lot 01 — Comptes et équipes

Périmètre : US25–26 / E73-CA-50 à 53. Le domaine `EquipeOrganisation` possède les changements d’appartenances, délégations et responsabilité ; les services orchestrent transactions, identité globale, invitations et projections. Le portail comporte les parcours compte, équipe, choix d’organisation/commune et récupération d’accès. L’ERP permet la vérification des demandes et la récupération assistée avec preuve et motif. Les listes équipe, invitations et demandes sont paginées en SQL ; les contrôles de responsabilité utilisent une lecture ciblée de la racine et du nombre de responsables.

Les nouvelles routes sont intégrées à la liste explicite du middleware navigateur Animation : contrôle d’origine, prévol CORS, cookie, CSRF et séparation des routes ERP. Une session d’identité seule peut accepter une invitation sans recevoir de données d’organisation. La perte du contexte d’une session complète continue de produire un refus.

Migrations préparées : `v260_e73_equipes_organisations.sql` et `v261_reinitialisation_mot_de_passe_animation.sql`. Le générateur local produit les appartenances et rattachements synthétiques ; le registre d’export/restauration inclut les six nouvelles tables. Les invitations et récupérations réelles n’ont pas été envoyées. Une future reprise des comptes historiques nécessite la vérification explicite de leurs responsabilités et rattachements ; aucune responsabilité n’est déduite automatiquement.

Preuves réellement exécutées :

| Contrôle | Commande / preuve | Résultat |
| --- | --- | --- |
| Transport navigateur, mot de passe, API et persistance | `scripts/validation/test_isolated.py tests/security/test_animation_browser_session.py tests/security/test_mot_de_passe_animation_postgres.py tests/api/test_animation_password_api.py tests/application/identite_acces/test_gestion_mot_de_passe_animation.py tests/application/identite_acces/test_gestion_acces_animation_reset.py tests/domain/identite_acces/test_mot_de_passe_animation.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp .artifacts/e73-password-final-01 --tb=short` | **130 réussites**, deux avertissements de dépréciation Starlette/httpx |
| Migrations complètes, rejeu et démonstration/restauration | `scripts/validation/test_isolated.py tests/integration/test_data015_migrations.py tests/security/test_demo_equipes_animation_postgres.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_migrations_test --basetemp .artifacts/e73-migrations-final-01 --tb=short` | **4 réussites** ; avertissement SQLAlchemy de réflexion `dialect_options` |
| Régression frontend Animation | `npm.cmd test` | **181 réussites**, zéro échec et zéro test ignoré ; types et lint réussis |
| Navigateur ERP | `node tests/browser/equipes-animation-erp.cjs` | Réussi à 390 et 1 280 px : lecture, preuve obligatoire, CSRF/idempotence, erreurs 409, issue réseau incertaine et relecture, absence de débordement |
| Navigateur portail | `node tests/browser/organisation-access.mjs` et `node tests/browser/account-app.mjs` | 111 assertions de composants et 48 assertions dans App ; API synthétique locale, formats mobile et bureau |
| Contrats embarqués et build isolé | Export hors ligne `generate_epic41_openapi.py`, copie consommateur Animation ; `node --test tests/generation-http-contracts.test.mjs tests/publication-http-contracts.test.mjs` ; `node scripts/build-generation-tests.mjs` | 749 routes exportées, 5 tests réussis, build réussi sans fichier opérateur ; avertissement de chunk principal 839,83 ko, à traiter dans la maîtrise des chargements du lot 09 |
| Pagination et plans SQL équipe | `scripts/validation/test_isolated.py tests/security/test_equipes_animation_performance_postgres.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp .artifacts/e73-team-perf-02 -q -s --tb=short` | **2 réussites**, 10 103 appartenances dont 6 002 dans une organisation ; requêtes réelles capturées puis `EXPLAIN ANALYZE BUFFERS`, aucun réglage forçant un index |

Les pages d’équipe initiale, suivante et après 5 000 membres utilisent `idx_equipe_animation_membres_page`, avec limite 26 et curseur SQL, sans `OFFSET`. Mesures ponctuelles à chaud : 0,037 / 0,067 / 0,040 ms pour ces requêtes, coûts estimés 4,31 / 4,38 / 6,85. La liste d’organisations utilise `idx_equipe_animation_organisations_page` ; PostgreSQL choisit librement une lecture séquentielle de la petite table des 102 organisations pour une jointure, sans balayage des appartenances. La projection complète utilise neuf requêtes pour des pages de 1 ou 100 membres, avec respectivement 3 ou 102 membres hydratés au maximum. Ces mesures caractérisent la lecture locale et ne prouvent ni le trafic simultané ni un engagement de temps de réponse.

Revue indépendante : les premiers 42 tests métier/HTTP/PG passaient, mais deux scénarios supplémentaires ont révélé une acceptation après suspension globale de l’auteur et une récupération vers un successeur suspendu. Les corrections et tests persistés ont été vérifiés indépendamment : `test_equipes_animation_postgres.py -k 'invitation_refuse_auteur_suspendu or recuperation_refuse_identite_suspendue'`, runner PostgreSQL local, répertoire `.artifacts/e73-review-corrections-01` : **2 réussites, 14 désélections**. Une course changement d’organisation/révocation de session a également été corrigée et revérifiée sur PostgreSQL : la session révoquée reste inutilisable, même après écriture d’une ancienne projection. Les interfaces portail et ERP ont été relues séparément de leurs auteurs.

Le PostgreSQL utilisé est un cluster créé pour cette tâche sur boucle locale, avec deux bases jetables distinctes. Le runner désactive la configuration opérateur et les effets externes. Ces preuves ne concernent aucune base partagée.

Contrôles finaux backend, préfixe commun `.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`, suffixe commun `-q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp <répertoire indiqué> --tb=short` :

| Fichiers / répertoire temporaire | Résultat |
| --- | --- |
| `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/domain/identite_acces/test_equipe_organisation_dedicated.py tests/application/services/test_equipes_animation.py tests/api/test_equipes_animation_api.py tests/security/test_equipes_animation_postgres.py tests/api/test_acces_animation_erp.py tests/security/test_animation_browser_session.py` ; `.artifacts/e73-team-final` | **620 réussites**, avant ajout de la preuve T1 |
| `tests/security/test_equipes_animation_postgres.py tests/application/services/test_equipes_animation.py tests/api/test_equipes_animation_api.py` ; `.artifacts/e73-team-audit-final` | **25 réussites**, après ajout de la preuve T1 |
| `tests/security/test_generation_animation_postgres.py` ; `.artifacts/e73-team-generation-final` | **24 réussites** : tâches non commencées suspendues, reprise contrôlée et régressions de génération |
| `tests/security/test_animation_finance_tenant.py` ; `.artifacts/e73-team-finance-final` | **4 réussites**, zéro skip après raccordement du test à la variable du runner isolé ; le premier essai ignoré faute de variable historique ne constituait pas une preuve |
| `tests/security/test_session_animation_revocation_race.py` ; `.artifacts/e73-session-race-01` (sans `--tb=short`) | **1 réussite**, vraie révocation concurrente et ancienne projection ; preuve durable ajoutée au commit complémentaire `a17e3f4` |

Les suites se recouvrent : leurs nombres ne sont pas additionnés en un total de tests distincts. Les contrôles frontend des 15 appels compte/équipe contre l’OpenAPI passent dans `tests/organisation-http-contracts.test.mjs` (3 tests). Le scénario `tests/browser/animation-lots.mjs` couvre lecteur avec/sans Achat à 320/1 280 px. Le scénario `tests/browser/generation-preparation.mjs` couvre la suspension explicite sans polling ni reprise automatique (70 contrôles à 390/1 280 px). Les 4 hunks préexistants « Clôturer » d’App.tsx restent exclus du commit ; types et build isolé ont aussi réussi sur une copie de l’index Git dans `tmp/e73-lot1-staged`, indépendante de ces modifications.

Conservation : classification T1/T8 et dates sources documentées dans l’architecture ; audit minimal des changements d’habilitation implémenté. Le raccordement des purges et la preuve de leur reprise après restauration restent une obligation du lot 10 avant mise en service. Les recettes humaines Localeo puis Martignas-sur-Jalle et tout contrôle hébergé restent non exécutés. Aucun push ni déploiement.

### Lot 02 — Périmètres commerçants

Le domaine Référencement porte la décision produit, distincte du statut général du commerce. Les migrations locales préparées sont `v262_e73_perimetres_commercants.sql` et `v263_autorisations_dediees_internes.sql`. Les commandes ERP imposent version, motif et idempotence ; le rôle Backoffice ne suffit pas sans autorisation dédiée. Le générateur prépare des racines `A_REVOIR`, sans suggérer ni activer automatiquement les produits des commerces existants. Son registre classe les décisions, preuves d’engagement et reçus avec le jeu métier.

OnBoard utilise une preuve de convention explicitement rattachée à chaque produit et un support Animation seule. Les onglets financiers et prestations suivent l’applicabilité projetée par le serveur. L’ERP distingue revue individuelle et bascule communale ; son historique se charge sur demande, par pages SQL de 25. Les anciennes mutations ORM directes SQLAdmin Commerçant/Prestation sont fermées au profit des parcours transactionnels ERP, avec liens explicites.

Premières preuves exécutées par l’intégration (ne constituent pas encore la validation finale du lot) :

| Contrôle | Commande / résultat |
| --- | --- |
| ERP/OnBoard mobile et bureau | `node tests/browser/epic73-perimetres.cjs` : réussi à 320/1 280 px, revue sans présélection, consultation seule, rattachement de convention sur dossier clos, conflit avec saisie conservée, historique paginé et confirmation de bascule communale |
| Régressions OnBoard | `node tests/browser/onboard-administration.cjs` : 7 scénarios réussis ; `node tests/browser/epic69-onboard.cjs` : Lecteur/Backoffice, scopes, actualisation de droits et purge de session réussis |
| Autorisation dédiée ERP | `node tests/browser/epic69-acces-internes.cjs` : réussi à 390/1 280 px ; l’autorisation n’est jamais attribuée implicitement par le changement de rôle |
| Générateur/registre | Runner isolé, `tests/unit/test_demonstration_registry.py tests/integration/test_demo_perimetres_commercants.py`, base locale jetable, `.artifacts/e73-demo-scopes-01` : **10 réussites** |
| Pagination et index historique | Runner isolé, `tests/security/test_historique_perimetres_postgres.py -q -s`, base locale jetable, `.artifacts/e73-history-perf-01` : **1 réussite**, 10 000 décisions dont 6 000 concentrées sur un commerce ; deux pages distinctes, 26 lignes SQL maximum, absence de chargement des snapshots et d’OFFSET ; `EXPLAIN ANALYZE BUFFERS` utilise `ix_historique_perimetres_commerce_date` (0,076 et 0,093 ms ponctuels) |
| Administration et adresses | `.artifacts/e73-admin-boundary-01` : 24 réussites, 1 échec de double de session incomplet dans le test de modification d’adresse ERP ; correction du double confiée au propriétaire, résultat de reprise à enregistrer |
| Sources documentaires | `sync_documentation.py --check-sources` via Python isolé : 123 documents vérifiés |

La revue a identifié puis fait corriger les frontières suivantes : continuité pendant une redemande, lecture ERP sans grant de gestion, Stripe depuis une URL directe, filtrage SQL des historiques/notifications avant pagination et compléments sur dossier clos. Les corrections sont intégrées et vérifiées par les preuves ci-dessous. La recette humaine et la bascule pilote ne sont pas exécutées.

Vérifications complémentaires de l’intégration :

- `tests/infrastructure/admin/test_perimetres_mutations_erp.py tests/application/conformite_fiscale_bum/test_adresse_onboard_erp.py`, runner isolé et `.artifacts/e73-admin-boundary-02` : **24 réussites** ; le double ERP incomplet est corrigé sans changer les assertions.
- `tests/integration/test_data015_migrations.py`, base locale exclusive `localeo_audit_migrations_test`, `.artifacts/e73-migrations-lot02` : **3 réussites**, migrations complètes et rejeu jusqu’à v263. L’indexation supplémentaire de pagination est vérifiée séparément après stabilisation.
- `node tests/browser/epic73-perimetres.cjs` rejoué après ajout du complément : réussi à 320/1 280 px ; dossier clos sans complément en lecture, complément Coffrets avec seuls champs autorisés modifiables, statut `CLOTURE` conservé.
- Contrats Animation, `node --test tests/organisation-http-contracts.test.mjs tests/generation-http-contracts.test.mjs tests/publication-http-contracts.test.mjs` : **8 réussites** sur l’export intermédiaire de 756 routes.
- `check_guidance.py` : **94 guides, 1 000 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources` : **123 documents vérifiés**.

Dette backend reproduite indépendamment sur le commit antérieur au lot `a17e3f4`, extrait dans un répertoire temporaire sans configuration opérateur : `test_missions_medias_t3.py`, `test_modification_animation_en_cours.py`, `test_tirage_tous_lots_animation.py` sous `tests/application/animation_locale`, runner isolé, `.artifacts/e73-lot02-baseline-failures` : **9 échecs et 2 réussites**. Les deux premiers échecs sont des doubles sans `configurations_animation`, trois concernent l’ancien parcours de modification après publication remplacé par la commande versionnée, quatre des doubles sans `coordinations_animation`. Les mêmes neuf échecs sont observés dans la passe large du lot ; aucun skip ni affaiblissement d’assertion. Ces scénarios doivent être repris dans les lots qui modifient effectivement les parcours Animation/tirage.

Pro est enregistré localement dans `bc9d1ac` ; le contrat Animation synchronisé dans `7cab528` conserve tous les travaux utilisateur préexistants hors index. Preuves Pro : suite unitaire intermédiaire **487 réussites**, ciblés finance/reset **24**, pagination finale **11**, contrats OpenAPI finaux **46** ; recette navigateur **28/28** puis **16/16** avec curseur à 320/1 280 px ; build isolé réussi. Les suites se recouvrent et ne constituent pas un total à additionner. La recette complète a donné **106 réussites et 7 échecs**, tous reproduits sur le HEAD antérieur `19f7a20` (`business-ux`/`merchant-contract`) ; une dernière suite unitaire complète interrompue après ralentissement n’est pas comptée comme verte. Son timeout de récupération de mot de passe passe ensuite dans la reprise ciblée sans modification de l’assertion.

La portée de ce lot couvre CA15–19 et CA26 pour les produits existants, ainsi que les branches Coffrets/passages des CA20–22. Les bons numériques et leur continuité restent à compléter au lot 05 ; les vues transverses et la restauration complète des CA25/27 restent au lot 10. Aucun de ces critères partagés n’est déclaré acquis dans son intégralité sur la seule preuve du lot 02.

Preuves backend complémentaires, préfixe commun `.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`, suffixe `-q --basetemp <répertoire> --tb=short` ; les scénarios PostgreSQL ajoutent explicitement l’URL locale jetable déjà documentée :

| Contrôle / fichiers | Résultat |
| --- | --- |
| Architecture, application Animation et périmètres ; `.artifacts/e73-perimetres-final-01` | **702 réussites**, dont architecture ; 6 doubles nouveaux et 3 erreurs de fixture corrigés puis repris ci-dessous, 9 échecs préexistants reproduits sur référence |
| `tests/security/test_perimetres_validations_postgres.py`, régressions application catalogue chasse, financement lots, avertissement lots/participants, suivi préparation, supports commerce chasse, paiements individuels/lots et scénario commission ERP ; `.artifacts/e73-perimetres-final-02` | **80 réussites** après correction des doubles, dont vrais QR/PIN PostgreSQL et refus sous suspension |
| `tests/api/test_perimetres_commercants_api.py tests/domain/referencement/test_perimetres_commercant.py tests/application/use_cases/test_initialiser_paiement.py tests/application/use_cases/test_stripe_connect_onboarding.py` ; `.artifacts/e73-perimetres-last-01` | **42 réussites**, dont transport HTTP assemblé avec refus métier 403 et refus avant fournisseur |
| Domaine et PG périmètres après alignement du conflit sur `CONFLIT_VERSION` ; `.artifacts/e73-conflict-contract-01` | **21 réussites** |
| OnBoard, droits et finance ; `.artifacts/e73-onboard-finance-final-01`, puis compléments `.artifacts/e73-complement-01` | Respectivement **678** puis **210 réussites** ; suites partiellement communes, avant finitions de pagination |
| `tests/security/test_facturation_continuite_postgres.py tests/security/test_onboarding_produits_postgres.py`, avec API de dépôt et tests curseur/complément/détail groupé ; `.artifacts/e73-final-finance-context-01` | **7 scénarios PG réussis**, 32 tests réussis au total, un double E50 obsolète corrigé et repris dans la ligne suivante |
| `tests/application/conformite_fiscale_bum/test_service_preparation_onboarding.py tests/application/conformite_fiscale_bum/test_curseur_factures.py tests/api/test_facturation_continuite_upload.py tests/security/test_grouped_invoice_detail.py` ; `.artifacts/e73-final-finance-context-02` | **26 réussites** : complément, curseur lié au contexte, refus de lecture directe et droits avant stockage |
| `tests/api/test_facturation_continuite_upload.py` ; `.artifacts/e73-final-chorus-01` | **11 réussites**, y compris les trois routes Chorus marchandes |
| Migrations complètes jusqu’à `v264_pagination_factures_commercant.sql`, même test DATA015 ; `.artifacts/e73-migrations-lot02-final` | **3 réussites**, aucune base partagée |
| Domaine périmètres, Stripe Connect, paiements individuels/lots et validations PostgreSQL ; `.artifacts/e73-perimetres-final-boundaries-01` | **65 réussites** après séparation des lectures historiques et des validations résiduelles ; appels fournisseur hors verrou métier |
| Attestations moteur PostgreSQL et salariés E72 ; `.artifacts/e73-perimetres-recus-final-01`, puis reçu après retrait sans engagement `.artifacts/e73-perimetres-recu-clos-final` | **11 réussites**, puis **1 réussite** supplémentaire pour la lecture historique d’une animation close |

Les deux listes de factures marchandes conservent leur tableau JSON et annoncent la page suivante dans `X-Next-Cursor` (exposé au navigateur), avec `limit=25`, maximum 100. Le curseur est lié au commerce, à la famille, au tri et à la version. Les actions sont calculées en lectures groupées, sans cache de droits persistant. Sur 10 000 demandes simples et 10 000 groupées : 9/10 requêtes constantes pour 2 ou 51 racines lues ; plans réels indexés sans forçage, mesures ponctuelles 0,229/0,565 ms. Les anciennes listes acheteur/Animation conservent leur contrat et leur dette de pagination, sans nouveau calcul marchand par ligne ; cette dette doit être traitée dans les lots finance/parcours concernés. Ces mesures ne démontrent pas les dix utilisateurs simultanés ni la charge mêlée du lot 10.

Raccord complémentaire : le module `perimetres-commercants.js` était absent de la liste des fichiers servis par le shell ERP. Le commit local `59d89d0` l’ajoute ; `tests/api/test_erp_perimetres_asset.py`, runner isolé, `.artifacts/e73-lot02-asset` : **1 réussite**, chargement HTTP et cache privé vérifiés. Cette preuve complète la recette navigateur qui intercepte les fichiers locaux.

### Lot 03 — Souscriptions et modules (en cours)

L’accès au catalogue est réservé aux administrateurs. Les anciennes écritures directes SQLAdmin d’offre sont fermées au profit de versions explicites. Les autorisations `abonnements:modules_octroyer` (Backoffice) et `abonnements:remboursements_decider` (Finance) sont attribuées séparément ; aucun changement de profil ne les attribue implicitement. La migration `v267_autorisations_modules_internes.sql` étend seulement les codes permis, sans accorder de droit.

Premières preuves, sans validation finale du lot :

- `tests/application/test_autorisations_dediees_internes.py tests/domain/identite_acces/test_acces_interne_dedicated.py`, runner isolé `.artifacts/e73-lot03-grants-02` : **36 réussites**.
- `tests/api/test_offres_animation_erp.py tests/security/test_acces_internes_surfaces.py tests/infrastructure/admin/test_catalogue_versionne_erp.py tests/api/test_erp_perimetres_asset.py`, `.artifacts/e73-lot03-admin-02` : **72 réussites**. La première passe avait 71 réussites et une attente Backoffice obsolète ; E73 restreint désormais cette création aux administrateurs, avec assertion de refus avant SQL.
- `node tests/browser/epic69-acces-internes.cjs` : réussi à 390/1 280 px après extension des autorisations dédiées.
- `node tests/browser/epic73-modules-erp.cjs` : réussi à 320/1 280 px sur réponses synthétiques locales : octroi versionné, dates Paris avec navigateur réglé à New York, conflit et saisie conservée, historique borné, catalogue versionné, décision de remboursement sans retrait implicite.

Les contrôles de droits/quota/paiement, migrations complètes et contrats réels restent en cours. Les trois modules seront proposés à l’achat seulement après réalisation et vérification de leurs parcours dans les lots 06/07/08 ; leur présence au catalogue n’atteste pas leur disponibilité.

Contrôles supplémentaires de l'intégration (lot encore en cours) :

- `tests/integration/test_comptes_internes_postgres.py`, `.artifacts/e73-lot03-grants-pg` : **8 réussites** ; persistance des grants et retrait sur session existante.
- `tests/application/test_souscriptions_regressions.py`, `.artifacts/e73-lot03-e47-regressions-04` : **38 réussites** ; activation commerciale séparée de l'identité, rollback et replay, invitation explicite après habilitation, réinitialisation d'une heure. La fixture a été raccordée aux tables E73 ; un doublon de fonction qui masquait un test a été retiré.
- `tests/integration/test_demo_modules_abonnements.py tests/unit/test_demonstration_registry.py tests/api/test_erp_perimetres_asset.py tests/api/test_modules_dates_contract.py`, `.artifacts/e73-lot03-demo-03`, PostgreSQL local : **12 réussites**. Le premier essai métier a détecté l'absence de reprise des débits dans le générateur ; correction par le service normal, sans validation automatique de la reprise.
- `tests/integration/test_data015_migrations.py`, `.artifacts/e73-lot03-migrations-01`, base exclusive `localeo_audit_migrations_test` : **3 réussites**, migrations complètes jusqu'à v267, rejeu et atomicité.
- `node tests/browser/epic73-modules-erp.cjs` : nouvelle réussite à 320/1 280 px incluant perte de réponse puis reprise avec exactement la même clé/corps, et confirmation motivée des conditions historiques ; formats d'unités alignés sur les vrais DTO.
- Première passe architecture/application intégrée, `.artifacts/e73-lot03-integration-01` : **533 réussites, 3 échecs**. Deux régressions de transition d'expiration après 30 jours sont renvoyées au propriétaire du service ; le troisième échec détecte le nom/format des déclarations de classes de tests dédiées. Correction en cours, aucune assertion supprimée ou affaiblie.

Le contrat hors ligne contient à cette étape **786 routes** ; il est recopié dans
les consommateurs Animation et Pro, sans prétendre à leur livraison. Les
anciennes éditions directes du catalogue ne constituent plus un chemin de mutation.

Recette Animation : **183 tests Node réussis**, types/lint/build isolé réussis,
**484 assertions dans 36 scénarios navigateur** à 320/1 280 px. Le navigateur
réglé à New York vérifie les heures affichées à Paris ; les scénarios couvrent
expiration sans abonnement courant, période future, quota/historique paginés,
premières coordonnées de facturation, perte de réponse et reprise explicite.
Les quatre hunks préexistants « Clôturer » restent intacts et exclus du futur commit.
La revue frontend/producer a détecté puis fait corriger les dates sans fuseau et
le calcul « déjà acheté » dépendant de la première page des droits.

`tests/security/test_commerce_animation_browser.py`, runner isolé
`.artifacts/e73-commerce-browser-real-01` : **4 réussites** avec la vraie pile
cookie/CORS/CSRF et une session révoquée ; refus avant appel métier. Le service
commercial est simulé dans cette preuve de transport, séparée des preuves SQL.

Pro : **42 tests de contrats réussis** avec
`node node_modules/vitest/vitest.mjs run src/lib/api/contracts.test.js src/lib/api/preparation.contract.test.js --config tmp/e73-lot03-vitest.config.mjs --maxWorkers=2`.
La configuration jetable impose `envDir:false` et des valeurs publiques synthétiques.
Le premier lancement avec la configuration Vite habituelle n'est pas retenu
comme preuve d'isolation. Seul le contrat embarqué Pro est modifié dans ce lot.

Contrôles documentaires intermédiaires : `check_guidance.py` **94 guides,
1 000 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources`
**123 sources vérifiées**. Le lot reste en cours : revue des nouveaux octrois
sur conditions historiques, suspension sur plusieurs périodes et raccordement
du Checkout ERP historique à une intention durable, sans appel fournisseur
sous verrou métier.

Après corrections, `.artifacts/e73-lot03-integration-02` réunit architecture,
couverture des classes métier/use cases, régressions E47, démonstration SQL et
contrat des dates : **539 réussites**, deux dépréciations `utcfromtimestamp`
préexistantes dans le parcours Checkout historique. Les échecs d'expiration
de la première passe sont corrigés ; les classes de tests dédiées sont détectées
par le contrôle sans modifier celui-ci. Le test périmètres du lot 02 est renommé
`test_perimetres_commercant_dedicated.py`, avec ses assertions conservées.

Finalisation du lot 03 :

- Migrations complètes et rejeu jusqu'à **v268**, base locale exclusive,
  `.artifacts/e73-lot03-migrations-02` : **3 réussites** (68,13 s).
- Finance, droits assemblés, factures, API et worker : runner isolé PostgreSQL,
  `.artifacts/e73-commerce-final-01` ; fichiers
  `tests/security/test_commerce_droits_integration_postgres.py`,
  `test_checkout_erp_async_postgres.py`, `test_commerce_abonnements_postgres.py`,
  tests domaine commande/devis/prorata/avoirs, traitement commerce, gateway et
  webhooks Stripe : **56 réussites** (38,54 s), trois dépréciations.
  Deux anciens échecs de fixture supposaient un rôle interne ADMIN nommé
  inexistant ; les scénarios corrigés prouvent le refus Finance et suspension,
  sans élargir la permission historique `finance.executer`.
- `node tests/browser/epic73-checkout-erp.cjs` : **réussi à 320/1 280 px**,
  intention durable, attente explicite et lien visible après confirmation.
- `node tests/browser/epic73-modules-erp.cjs` : **réussi à 320/1 280 px** avec
  compteur divergent ; le libellé mobile ajouté par CSS empêchait la recherche
  accessible exacte du test, désormais ciblée sur la cellule Disponible avec
  assertion exacte « Indisponible ». Aucune assertion métier retirée.
- Animation : **502 assertions dans 38 scénarios navigateur**, types/lint/build
  isolé réussis ; `tests/modules-http-contracts.test.mjs` **2 réussites** après
  export final. Les nombres remplacent les comptages intermédiaires recouvrants.

Les lectures de quotas sont vérifiées avec 10 000 droits et 10 000 consommations,
sans recompter le journal. Les listes de commandes/remboursements sont vérifiées
sur 10 000 lignes chacune avec plans PostgreSQL et curseurs. Ces preuves ne
constituent pas encore le test de trafic transverse du lot 10. Les fournisseurs
restent simulés, les modules futurs indisponibles et la recette humaine non exécutée.

Dernière suite core : `test_modules_plateforme_postgres.py`,
`test_modules_plateforme_api.py`, `test_modules_acquis_dedicated.py`,
`test_souscriptions_regressions.py`, `test_verification_droit_plateforme.py`,
runner isolé et PostgreSQL local `.artifacts/e73-core-final-08` : **66 réussites**
(18,86 s), quatre dépréciations. La revue indépendante finale des compteurs et
du Checkout ERP n'a trouvé aucun nouvel écart concret ; c'est une revue de code
et des tests persistés, distincte de leur exécution par les auteurs/intégrateur.

Une copie de l'index Animation dans `tmp/e73-lot03-staged` exclut les quatre
hunks utilisateur : `npm.cmd run typecheck` et le build isolé y réussissent.
Le chunk principal de 863,29 ko conserve la dette de découpage identifiée pour
le lot 09. Les contrôles finaux de documentation donnent **94 guides,
1 000 liens, zéro erreur/avertissement**, **123 sources vérifiées**.

Limites opératoires préparées : un compteur divergent exige le service motivé
de contrôle/reconstruction, sans écran supplémentaire dans ce lot ; un second
paiement concurrent portant sur une période devenue incompatible reste à
rapprocher, sans créditer deux droits. Aucun fournisseur réel, worker distant,
push ni livraison n'a été utilisé. Le lot 03 est enregistré localement ; les
branches de continuité import/chasse/messages seront complétées avec leurs
opérations réelles dans les lots 06 à 08.

### Lot 04 — Animation et lots externes

Le domaine `ConfigurationDotation` possède le choix et son gel ; le domaine
d'attribution libre possède le suivi et les conditions de remplacement. Les
lots externes n'entraînent aucun achat, activation ou reversement Coffrets.
Le [protocole de tirage libre](tirage-libre-protocole.md) décrit la préparation
privée bornée et sa confirmation. Les écrans présentent séparément attribution,
envoi de l'email et déclaration de remise. Les bons numériques restent
indisponibles jusqu'au lot 05.

Premières preuves locales, complétées par les vérifications finales plus bas :

- Backend : `tests/security/test_gains_live_projection_postgres.py` et
  `tests/api/test_localeo_live_animations_inscription.py`, runner isolé,
  PostgreSQL local, `.artifacts/e73-lot04-live-04` : **7 réussites** (6,44 s).
  La projection de catalogue ne lit que les participations des animations de
  la page. Sur 10 000 participations et 10 000 gains, 3 requêtes constantes
  pour 1 ou 25 racines, sous-requêtes limitées et index réel ; mesure ponctuelle
  0,139 ms pour la projection de gain. Aucun gain privé n'est exposé avant
  confirmation, ni à un autre participant. Ce contrôle ne prouve pas le trafic
  simultané du lot 10.
- Générateur : `test_demo_dotations_animation.py` et
  `test_demonstration_registry.py`, runner isolé PostgreSQL,
  `.artifacts/e73-lot04-demo-01` : **10 réussites** (3,23 s). Le premier brouillon
  synthétique utilise deux lignes de lots externes et trois unités ; les
  historiques publiés conservent une dotation Coffrets explicite et gelée par
  le domaine. Le registre classe les neuf tables du lot comme données du jeu
  à remplacer, sans importer les anciens gagnants. La génération transverse
  complète reste à réaliser au lot 10.
- Marketplace : `node --test tests/security/animation-gain.test.cjs
  tests/security/library-backup.test.cjs` : **5 réussites**. Nature inconnue
  refusée, ancien gain Coffret compatible, absence de coordonnées/consignes
  privées dans le carnet IndexedDB et ses exports.
- Marketplace : ESLint ciblé et build Vite en mode isolé réussis. Le lint global
  rencontre un **EPERM de lecture** dans
  `output/demo-generation/pytest-bum-registry` ; aucune suppression de ce
  répertoire de travail ni modification des règles de lint.
- Navigateur Marketplace : contrat public de détail existant et
  `tests/visual/external-animation-gain.spec.cjs`, serveur local isolé :
  **3 scénarios réussis** (19,8 s), dont accès gagnant direct à 320/1 280 px,
  heure de Paris malgré navigateur New York, actualisation au clavier,
  remise déclarée puis attribution remplacée et refus de nature inconnue.
  Le gain précède la progression de jeu et aucun QR de lot Coffret n'est
  fabriqué pour une remise externe.

Les migrations complètes, la revue indépendante, les contrats et les contrôles
du parcours organisateur/tirage ont ensuite été exécutés comme suit.

Preuves de finalisation avant enregistrement :

| Contrôle | Résultat réel / artefact |
| --- | --- |
| Domaine, architecture, contrats moteur, projection Live et générateur ciblé | Runner isolé, `tests/architecture`, recensement domaine/use cases, `test_gains_live_projection_postgres.py`, API Live, dotation de démonstration, registre et `test_contrats_moteur_t1.py` ; `.artifacts/e73-lot04-integration-02` : **545 réussites** (39,61 s) |
| Configuration, publication, génération, jeu, financement et anciens tirages | Suite core sur quinze fichiers, `.artifacts/e73-lot04-core-final-12` : **161 réussites**, deux avertissements de dépendances ; inclut paiement Coffrets tardif à rapprocher sans émission d’instances |
| Conservation d’identité | `tests/security/test_conservation_postgres_t6.py`, `.artifacts/e73-lot04-conservation-02` : **18 réussites** (57,8 s) ; gains ouverts et réserve préservent l’archive, remise puis purge de l’identité sans effacer la preuve |
| Migrations complètes et rejeu | `test_data015_migrations.py`, base locale exclusive, `.artifacts/e73-lot04-migrations-02` : **3 réussites** (42,8 s), jusqu’à v271 incluant index réserve et compteur BIGINT |
| Animation | **191 tests Node**, **416 assertions dans 38 scénarios navigateur** à 320/1 280 px, régression chasse Coffrets **254 contrôles** à 390/1 280 px ; types, lint, build isolé et deux tests de contrats HTTP réussis |
| Marketplace | `npm run test:security` : **112 réussites** ; ESLint ciblé et build isolé réussis ; `external-animation-gain.spec.cjs` : **5 scénarios réussis** (34,8 s), lien email, reprise/expiration, pagination publique et états Live à 320/1 280 px |
| Pro, contrats consommateurs | Quatre fichiers Vitest contrat API/préparation/registre moteur/animations : **63 réussites** (13,71 s, export final) ; aucun parcours de consommation de lot externe ajouté |

Ces suites se recouvrent ; leurs nombres ne forment pas un total de tests distincts.
Les revues croisées ont fait corriger les curseurs malformés (400), l’ordre commun
de lecture/réservation des suppléants et le total BIGINT des unités. Le carnet Live
refuse une version inconnue et préserve les discriminants inconnus après stockage
et réimport ; il ne les requalifie jamais en Coffrets.

Le tirage a été mesuré avec 10 000 candidats et 1 000 lignes de lots : une tranche
de 500 attributions utilise 16 lectures SQL et environ 2,5 Mo de mémoire. Le
scellement externe produit deux écritures, indépendamment de la réserve. Les
plans utilisent les index de population et de classement, sans tri aléatoire ni
chargement intégral. Une dotation de trois milliards d’unités avec un participant
ne matérialise qu’une attribution. Cela ne démontre pas encore la charge
simultanée transverse du lot 10.

Les contrats générés E41/Live et les trois consommateurs moteur sont synchronisés.
Le [guide organisateur](../../produit/formation/animation/guide-animation-preproduction.md)
et la [procédure de tirage](../../exploitation/exploitation/gerer-tirages-libres-animation.md)
décrivent les états et reprises. La liste globale reste nommée **Tirages Coffrets** ;
les lots libres se suivent depuis chaque animation, avant unification au lot 09.
Le traitement effectif reste désactivé par défaut. Les recettes humaines et toute
activation hébergée restent non exécutées.

Dette étayée : `test_modification_animation_en_cours.py` donne **3 échecs et
1 réussite** (3,81 s) sur les sources du HEAD antérieur `4f3a3b16`, dans une copie
isolée. Les 2 032 fichiers app/scripts/tests et la configuration pytest sont
contrôlés contre l’archive Git (`.artifacts/e73-lot04-baseline-proof.json`).
Ces tests attendent encore le PATCH direct de `date_fin` après publication et
deux anciens messages ; le domaine exige désormais la commande versionnée des
paramètres d’exploitation. Le lot 04 ne modifie ni ces tests ni cette règle.

Revue SQL complémentaire : le plan de la deuxième page de suppléants parcourait
10 000 candidats par semi-jointure malgré le `LIMIT` apparent. La sonde scalaire
corrélée, bornée et indexable corrige ce parcours. Le test avec les pages initiale,
suivante et au rang 9 000 vérifie maintenant les requêtes réelles : une ligne
sondée et 26 lignes de page, aucun candidat filtré, tri final de 26 lignes,
32 à 33 buffers. Les temps ponctuels sont de 0,19 à 0,46 ms, sans forcer le
planificateur. Le plan fautif est conservé dans
`.artifacts/e73-tirage-libre-reserve-plans-avant-correction.json`.

La copie de l’index Animation `tmp/e73-lot04-staged` passe types et build isolé,
sans les quatre hunks utilisateur « Clôturer ». Le chunk principal de 907,80 ko
reste à découper au lot 09. Les commits d’interfaces du lot 04 sont locaux :
Animation `d0b92f7`, Marketplace `1473e05`, Pro `30aeed3`.

Après cette correction SQL, la revue indépendante a réexécuté
`test_attribution_lot_libre_dedicated.py`, `test_email_lot_externe.py` et
`test_tirages_libres_postgres.py` : **28 tests distincts réussis**, dont 16
PostgreSQL en 84,13 s (`tmp/e73-lot04-audit-pg-final-03`), deux avertissements
Starlette/AnyIO, aucun skip. Les trois plans de réserve sont conservés dans
`.artifacts/e73-tirage-libre-reserve-plans.json`. Le premier essai interrompu
pendant la récupération du PostgreSQL local ne vaut pas validation ; seuls
les résultats terminés sont retenus.

Compatibilité de démonstration complète :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot04-demo-compatibility-20261018-resume` : **7 réussites**
en 586,51 s, trois modules obligatoires, zéro skip, quatre avertissements de
réflexion SQLAlchemy. Les cycles installation, panne injectée, restauration et
reset utilisent uniquement les deux clusters jetables de cette tâche. XML et
log sont conservés dans le répertoire indiqué et son fichier `.log` voisin.
Les garde-fous du runner passent **31 tests** (0,35 s). Les ports locaux peuvent
être fournis explicitement et doivent être distincts ; le répertoire de sortie
doit être neuf dans `tmp/`, aucun résultat antérieur n’est effacé.

Le commit backend `7502282` clôt le travail applicatif local du lot 04. Les
générations transverses des dix lots, la charge simultanée, les recettes humaines
et les preuves d’hébergement restent à réaliser selon leur lot. Aucun push,
envoi fournisseur ou déploiement n’a eu lieu.

### Lot 05 — Bons numériques (en cours)

Le lot 04 documentaire est enregistré dans `87badb3`. Avant le lot numérique,
`tests/api/test_pin_validation_e70.py` passe **14 tests** (4,40 s, trois
dépréciations), runner isolé `tmp/e73-lot05-pin-baseline-01`.

Le protocole de préparation privée/scellement est étendu aux bons numériques
dans [tirage-libre-protocole.md](tirage-libre-protocole.md). `BonLot` possède la
validité, la consommation unique, la rotation, la révocation et la correction.
Les canaux QR/PIN partagent ce cœur ; le service de tirage conserve la politique
de population et remplacement. L'ordre de verrou a été précisé en faveur de
l'ordre E70 existant (demande avant cible), sans changer les règles produit.
Les preuves exécutées ci-dessous complètent ce protocole ; la finalisation du
flux d’historique et du cycle complet de démonstration reste en cours.

Périmètre réalisé : CA30 (modèles/version/exemplaires), CA31 (affectation et
libération explicite), branche numérique CA32/33 (tirage, attribution, email et
bon), CA34/35 (QR et PIN), CA36 (cycle et incidents). Les compléments CA15/19–22
réutilisent les périmètres courants et les acteurs principal/salarié, avec
continuité limitée au bon attribué. Cela ne clôt pas US24/36–38 ni l’epic entière.

Le bon appartient à `animation_locale`. Les capacités de consultation, la
signature QR et le rendu email sont des adaptateurs ; le PIN E70 orchestre la
même transition de remise. Une consommation active unique subsiste sous deux
scans salariés ou QR/PIN concurrents. Une correction conserve la preuve initiale
et n’autorise pas le rejeu d’une ancienne demande à consommer de nouveau.
Les gardes du commerce précèdent les verrous de demande/cible ; la suspension
et la révocation personnelle restent prioritaires sur toute continuité.

La migration `v272` crée onze tables numériques, les références et contraintes
d’exclusivité ainsi que les index. L’origine de lien existante est réutilisée.
Les clés QR et flags de workers sont documentés sans secret dans le modèle de
configuration et la [procédure des bons numériques](../../exploitation/exploitation/gerer-bons-numeriques-animation.md).
Les trois branches de dotation restent explicites et exclusives.

### Preuves locales du lot 05

Toutes les commandes Python ci-dessous utilisent
`.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`
depuis le backend, avec `--basetemp` neuf. Les tests SQL utilisent exclusivement
`127.0.0.1:55473/localeo_audit_test` ou la base de migrations jetable dédiée.
Les suites se recouvrent : leurs nombres ne sont pas un total de tests distincts.

| Contrôle | Résultat réel |
| --- | --- |
| Architecture, recensement domaine et use cases | `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py`, `tmp/e73-lot05-architecture-final-02` : **519 réussites** (10,02 s) |
| Inventaire, BonLot, ports, crypto et choix de dotation | 28 réussites initiales ; après correction des métadonnées des huit types dédiés, **21 réussites** domaine/registre/crypto, sans exclusion de contrôle |
| PG inventaire/remise, conservation numérique et Animation, API inventaire | `test_inventaire_bons_postgres.py`, `test_conservation_bons_numeriques_e73.py`, `test_conservation_postgres_t6.py`, `test_inventaire_bons_lots_e73.py` : **32 réussites** (120,08 s), `tmp/e73-lot05-inventaire-conservation-03` |
| Compléments inventaire et droits | Génération 251 unités en 100/100/51, reprises concurrentes, isolation de reçus, libération de surplus : **3 réussites** (10,48 s) ; lecture Lecteur sans commande, isolation/rejeu : **3 réussites** (9,94 s) |
| Tirage numérique, email, accès personnel et scellement | **51 tests uniques réussis** : suite principale 50/50 (279,66 s), puis 15/15 sur les tirages après ajout du contrôle de budget avant chaque page, dont un nouveau test ; `tmp/e73-lot05-w2-final` et `tmp/e73-lot05-w2-budget-final` |
| PIN numérique | `test_pin_bons_lots_postgres.py` : **9 réussites** (65,03 s), `tmp/e73-lot05-pin-pg-03` : courses QR/PIN principal/salarié, correction/rejeu, rotation, rollback de notification, PIN bloqué mais QR autorisé, retrait et suspension |
| Transport API PIN | `test_pin_bon_lot_e73.py test_pin_validation_e70.py` : **22 réussites** (11,93 s), `tmp/e73-lot05-pin-transport-02` |
| Régression PIN Coffrets/Animation/salariés | Suite initiale : 19 réussites, deux échecs sur le formatage SQL de l’historique ; correction puis reprise des trois cas concernés : **3 réussites** (65,36 s), `tmp/e73-lot05-pin-regressions-02` ; 21 tests distincts finalement validés |
| Migration complète et rejeu | `test_data015_migrations.py` jusqu’à v272 : **3 réussites** (83,40 s), avant l’ajout éventuel des index du flux d’historique ; contrôle final à compléter |
| Animation | **197 tests Node réussis** après copie des contrats ; types, lint et build isolé réussis ; navigateur **38 scénarios/416 assertions** de régression lot 04 et **10 scénarios/100 assertions** numériques à 320/1 280 px |
| Localeo Pro | QR bons et contrats : **60 tests ciblés distincts** validés, build et quatre scénarios navigateur réussis avant passage de l’historique au flux ; complément à enregistrer |
| Live, stockage et discriminants | `node --test tests/security/library-backup.test.cjs tests/security/animation-gain.test.cjs` : **8 réussites** (8,76 s), restauration d’accès propre à chaque bon, aucun QR/consigne/coordonnée privée persisté |
| Live, navigateur | `digital-lot.spec.cjs` : **4 scénarios réussis** en production locale après correction de contraste ; même suite **4 réussites sous React StrictMode** avant retouche de présentation, capacité de fragment préservée ; 320/1 280 px, heure de Paris malgré navigateur New York, états terminaux, réseau indisponible, PIN dont la réponse est perdue |
| Live, analyse et build | ESLint ciblé réussi et Vite isolé réussi ; la limite préexistante du lint global sur le répertoire de travail EPERM reste celle du lot 04 |
| Générateur ciblé | **14 tests PG/registre** (6,57 s), puis **6 tests unitaires** ; deux modèles, cinq exemplaires, trois affectés et deux disponibles, aucun bon/QR/email prématuré ; onze tables classées `replace` |

Le scellement numérique a été mesuré avec 10 000 candidats, 1 000 bons et
120 commerces : **37 requêtes, deux écritures finales, environ 716 Ko de mémoire**,
au plus seize lectures par tranche préparatoire. Les gardes de commerce sont
prises seulement au scellement, par pages de cent ; délai de verrou de trois
secondes et budget de vingt secondes avec rollback/reprise testés. Ce n’est
pas encore la preuve de charge simultanée transverse du lot 10.

Deux revues indépendantes ont contrôlé les branches tirage/bon et PIN/droits.
Elles ont conduit à corriger les reçus inter-organisations, les actions proposées
aux Lecteurs et le calcul UTC des quatre-vingt-dix jours d’historique Animation.
Six tests de frontière échouaient avant correction (changement d’heure,
configuration/date/surcharge). Le flux par curseur est désormais intégré dans
Pro ; ses **19 tests PostgreSQL/API** passent, sans skip (83,67 s), puis les
quatre tests API repassent après contrôle des dates HTTP extrêmes (3,60 s).
L’ancienne route reste compatible avec un offset limité à 10 000.

Le cycle complet de démonstration a révélé **quatre échecs et trois réussites**
sur une clé étrangère modèle/version lors de la génération. Ce défaut a été
reproduit et corrigé ; le cycle final passe **7 tests** en 557,78 s, avec quatre
avertissements SQLAlchemy de réflexion `dialect_options`, sans skip.
Le runner `scripts/validation/run_demo_compatibility_tests.py` a utilisé
uniquement les clusters jetables `127.0.0.1:10407` et `127.0.0.1:55448`, avec
sortie `tmp/e73-lot05-demo-compatibility-20261018-final03` : génération,
dump/installation, échec contrôlé, restauration et reset. Le refus initial
sur une base jetable non vide a été résolu en recréant seulement cette base,
après vérification de son répertoire local et de l’absence de connexions.
Aucun environnement partagé n’a été contacté.

Le besoin nominatif du gain numérique est raccordé à la conservation existante :
remise/révocation ferment ce besoin, correction le réouvre ; un engagement
expiré mais non résolu et les autres gains/gels conservent leur effet propre.
La purge physique bornée des capacités et contextes expirés/révoqués sera
raccordée au dispositif commun au **lot 10, avant ouverture**. Les preuves
humaines, le transport réel et l’hébergement restent non exécutés.

Compléments de finalisation :

- PIN numérique/API E70 et contrats moteur relancés après les corrections :
  `test_pin_bons_lots_postgres.py test_pin_bon_lot_e73.py
  test_pin_validation_e70.py test_contrats_moteur_t1.py`,
  `tmp/e73-lot05-root-pin-final-04` : **51 réussites** (36,18 s), trois
  avertissements de dépréciation, zéro skip.
- Le défaut de clé étrangère est reproduit avec les contraintes réelles dans
  `test_modele_generation_et_unites_meme_uow_respectent_vraies_cles_etrangeres`.
  `sauver_modele()` persiste maintenant la version avant l’opération suivante,
  sans commit intermédiaire ; le test passe (**1 réussite**, 5,20 s). Le
  générateur ne contourne aucune contrainte.
- Après ajout des cinq index du flux Pro dans v272 : migrations/rejeu et
  générateurs OpenAPI, `tmp/e73-lot05-migrations-contrats-final-03` :
  **11 réussites** (54,82 s). E41 expose 828 routes, E42 en expose 55 ; copie
  consommateur Animation/Pro effectuée, quatre contrats Pro réussis.
- Live : le scénario de changement de bon ignore la réponse tardive du précédent
  et masque immédiatement son QR. La suite finale sous React StrictMode passe
  **5 scénarios**, dont 320/1 280 px et les états de remise. Les callbacks du carnet
  sont également liés au bon courant. Le serveur passe **13 tests**, dont le
  fallback SPA du lien personnel avec `no-store`. Les fermetures Playwright
  Windows nécessitent l’arrêt du seul serveur local créé par le test après
  exécution réussie ; aucun service distant ou autre processus n’est arrêté.
- Pro : **67 tests unitaires** puis 27 revalidés après la normalisation d’erreur,
  **11 scénarios navigateur** (six nouveaux/Paris et cinq régressions), build
  isolé et quatre contrats finaux réussis. Les filtres suivent les journées
  Europe/Paris même depuis New York, y compris les transitions de 23/25 heures.

- Pro, relecture d’un résultat incertain : identité du bon et de l’opération
  vérifiées ensemble ; aucun rejeu avec le contexte d’un autre bon. **17 tests
  unitaires et quatre scénarios navigateur** passent après ce durcissement.
- Architecture finale : même commande que ci-dessus,
  `tmp/e73-lot05-architecture-final-03` : **519 réussites** (15,46 s).
- Régression des passages salariés E72 : remplacement du test d’une méthode
  privée supprimée par les lectures SQL avant/à l’échéance, avec contrôle du
  maintien des preuves. Échec reproduit puis fichier entier
  `test_animation_salaries_e72.py` : **4 réussites**, aucun skip (9 s),
  `tmp/e73-lot05-historique-salarie-final`.
- Animation : copie isolée HEAD + seuls fichiers du lot 05 dans
  `tmp/e73-lot05-staged`, sans configuration opérateur ni modifications
  préexistantes « Clôturer » : types, lint, build et **huit tests de contrats**
  réussis ; manifestes d’empreintes conservés dans les artefacts locaux.

### Performance de l’historique et limites à solder au lot 10

Le nouveau flux effectue six requêtes repository constantes, sans `COUNT` ni
`OFFSET`. Les essais avec 30 000 occurrences, une page profonde à 27 000,
des filtres de mode et collisions de date/UUID entre types utilisent les index
avec au plus 26 occurrences par branche pour une page de 25. La rétention
des bons s’appuie sur une borne calendaire indexée exacte de cinq ans,
y compris les années bissextiles. Avec 10 000 bons expirés : aucune occurrence
lue ni jointure, environ 0,52 ms dans la mesure locale.

**Exception transitoire E73-PERF-02/04 à solder au lot 10 avant ouverture :**
la sélection des anciennes validations Coffrets/Animation dépend encore de
l’expiration portée par leurs objets parents. Les plans avec 10 000 occurrences
expirées lisent 10 000 validations et interrogent leurs archives/surcharges
(environ 38 ms Coffrets et 206 ms Animation). La réponse et le nombre de requêtes
sont bornés, mais ce travail SQL augmente avec les archives. Le lot 10 doit
raccorder un filtrage indexable à la politique canonique d’expiration, puis
rejouer ces plans ; ne pas présenter le flux comme une preuve de coût constant
pour tous les historiques. Les plans sont enregistrés dans
`.artifacts/e73-historique-flux-performance.json` et
`.artifacts/e73-historique-flux-expiration.json` du backend.

Commits locaux du lot 05 : backend `1cd9564`, Animation `2eee756`, Pro `63b64bc`,
Marketplace/Live `8e54957` ; sources dans le commit documentaire du lot 05.
Les seules modifications étrangères à ce lot sont
préservées hors index. Aucun push ni déploiement.

### Lot 06 — Import et protection des corrections locales

Périmètre : US19–20 / CA42–45, avec consommation des droits du lot 03.
Le domaine Référencement porte le lot d’import, les résolutions et la
provenance à trois versions. L’application orchestre une transaction par
ligne, avec le référencement et OnBoard ; le portail expose les décisions
et la progression. Le transport reste dans le namespace d’import, distinct
des mutations ERP. La [procédure d’import](../../exploitation/exploitation/importer-commercants-animation.md)
décrit les commandes et contrôles vérifiés localement.

Première preuve d’intégration :
`scripts/validation/test_isolated.py tests/security/test_imports_browser_e73.py
tests/security/test_animation_browser_session.py -q --tb=short
--basetemp tmp/e73-lot06-browser-root-01` : **118 réussites** (14 s), deux
avertissements de dépréciation, aucun skip. Dépôt multipart avec origine,
cookie/CSRF, lecture privée et refus des routes Référencement/ERP étrangères.
Cette preuve de transport ne valide pas encore le traitement métier complet.


Parcours intégrés : source Excel/CSV privée, flux stable, mapping explicite,
aperçu et rapprochement email avec contrôle d’identité, choix champ par champ,
import partiel, commandes idempotentes et reprise des seules lignes restantes.
Les créations passent par Référencement et OnBoard : brouillon à vérifier,
sans compte, invitation, périmètre actif ni participation. Les corrections
SIRET/commune sont décidées dans l’ERP ; un déplacement de commune rend la
fiche opaque à l’ancien import. Une incohérence avec le profil financier
courant bloque les nouveaux usages concernés, sans modifier les documents
émis. Après demande ERP, le mapping est figé pour préserver sa preuve ; un
nouveau dépôt dans le même flux permet de corriger les colonnes.

La migration locale `v273_imports_commercants.sql` crée les sept tables et les
index des flux/plans/provenances/vérifications, et accepte une catégorie
absente uniquement pour une fiche en brouillon. L’ouverture reste désactivée
par défaut (`LOCALEO_IMPORTS_COMMERCANTS_APPLY=false`) ; le catalogue ne propose
pas l’achat d’un parcours fermé. Le middleware borne aussi le corps multipart
avant parsing, indépendamment de Content-Length ; parseur, stockage et SQL
du dépôt s’exécutent hors boucle ASGI.

Revue croisée : correction d’un reçu créé avant la disponibilité effective du
fichier. Le client conserve fichier et clé jusqu’à disponibilité confirmée ;
panne avant/après stockage puis reprise explicite ne crée pas de second lot.
Les contrôles de version, les gels de conservation, la reprise après premier
traitement et les mises à jour de commune ont fait l’objet de cas PostgreSQL.
Les gels sont exclus de la sélection des purges puis revérifiés sous verrou,
pour ne pas bloquer les opérations suivantes. Les sources et instantanés de
travail sont purgés après trente jours ; provenance et audit restent distincts.

Preuves finales disponibles (préfixe backend :
`.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py` ;
les suites se recouvrent, leurs totaux ne s’additionnent pas) :

| Contrôle | Résultat local |
| --- | --- |
| Domaine import, API et rejet ERP/remapping | **38 réussites**, `tmp/e73-lot06-core-final-06.xml` ; dépôt hors boucle ASGI inclus |
| Changement de commune bout en bout | **1 réussite**, `tmp/e73-lot06-core-commune-07.xml` ; adresse atomique et confidentialité après déplacement |
| Référencement/OnBoard, corrections ERP, domaine/API/assets | **23 réussites**, `tmp/e73-lot06-preparation-final-03.log` ; concurrence et correction de commune incluses |
| Raccord fiscal et facture assistée existante | **23 réussites**, `tmp/e73-lot06-fiscal-coherence-01.log` ; snapshots inchangés et usages incohérents refusés |
| Garde-fous architecture, recensement, transport navigateur, limites multipart, parseur adversarial et readiness catalogue | **576 réussites**, `tmp/e73-lot06-architecture-final-03` ; deux avertissements de dépendances, aucun skip |
| Migration depuis la base vide, rejeu et compatibilité modèles | **3 réussites**, `tmp/e73-lot06-migrations-final-04` ; PostgreSQL jetable uniquement |
| Animation, copie HEAD + seuls fichiers du lot 06 | **206 tests Node**, types/lint/build réussis ; **22 scénarios navigateur, 292 assertions**, 320/1 280 px ; pas de configuration opérateur ni des changements préexistants Clôturer dans la copie |
| ERP vérifications d’import | Navigateur réussi à 320/1 280 px : motif, lecture seule, CSRF/idempotence, réponse perdue réconciliée, textes échappés |
| Sources et liens documentaires | **94 guides / 1 001 liens**, zéro erreur/alerte ; **126 sources exportées** vérifiées |

Performance : une prévisualisation de **100 lignes parmi 10 000 commerces**
utilise **trois requêtes groupées**, avec candidats bornés et enrichissement par
clé ; aucun balayage de la table des commerces dans le plan mesuré. Les pages
d’imports de 1 et 100 éléments prennent toutes deux **13 requêtes**, avec pics
mémoire Python d’environ 454 et 664 ko. La page profonde après 9 000 imports
utilise un Index Scan de 26 lignes, sans OFFSET. Ces mesures locales ne valent
pas preuve de capacité hébergée. Artefacts backend :
`.artifacts/e73-import-preparation-performance.json` et
`.artifacts/e73-imports-pagination-performance.json`.

Le chunk import Animation est chargé séparément (40,82 ko). L’avertissement
sur le bundle principal de 934,60 ko reste rattaché au lot 09. Pro et Live ne
consomment aucune nouvelle route d’import et ne reçoivent aucun accès implicite ;
aucune modification fonctionnelle n’y est nécessaire pour ce lot. La recette
humaine Localeo/Martignas-sur-Jalle et les essais d’hébergement restent à faire.

Derniers contrôles : **16 tests PostgreSQL complets du noyau import réussis**
(311,03 s, `tmp/e73-lot06-core-proof.md` dans le backend) ; **10 tests des
exports OpenAPI réussis**, `tmp/e73-lot06-contracts-final` (72,37 s).
Les exports canoniques E41/E42 comportent respectivement 844 et 55 routes ;
E42 conserve ses routes Live et reçoit seulement les schémas communs actualisés.
La copie embarquée Animation est synchronisée. Les fins de lignes et espaces
terminaux SQL sont normalisés sans changement sémantique.

Générateur et restauration complète : **7 tests réussis**, quatre avertissements
SQLAlchemy de réflexion, 855,49 s. Commande exécutée dans le backend :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot06-demo-complete-01`. Deux imports synthétiques passent
par les services, conservent une correction locale puis purgent leurs sources
avant export. Le wrapper transactionnel du générateur restaure ses budgets
SQL après chaque sous-transaction ; les limites runtime restent inchangées.
Les premiers essais incomplets ne servent pas de preuve finale.

Commits locaux du lot 06 : Backend `bb4e1e8`, Animation `955fb94`, sources dans
le commit documentaire du lot 06. Les changements préexistants
Clôturer/Exploitation/README restent hors commit ; les fichiers de préparation
du lot 07 sont exclus du commit backend du lot 06. Aucun push ni déploiement.

### Lot 07 — Chasse et préparation accompagnée

Périmètre : US18/30, CA46/57. La chasse conserve son quota dédié, consommé à
publication et non à la demande, au complément ou à la reprise technique. Le
suivi accompagné distingue complétude, préparation, complément attendu,
préparation prête, reprise et annulation. La cible de cinq jours ouvrés repose
sur un calendrier Localeo explicite et figé ; une attente suspend ce décompte.
Le portail présente cible initiale, estimation révisée et retard séparément.
L’ERP permet le traitement sans dépendre de l’Atelier Coffrets. Les messages de
service passent par l’outbox email ordinaire, indépendamment du futur module
Communication participants.

La validation terrain est une preuve de l’animation, de sa révision et de son
empreinte. Une modification pertinente l’invalide ; un modèle réutilisé ne la
transporte pas à la nouvelle édition. Les sessions et habilitations courantes
sont revérifiées avant les commandes et reçus. Le catalogue commercial et les
anciennes commandes de forfait contenant la chasse consomment la même
disponibilité technique injectée : ouverture explicite et calendrier valide.

Migration locale : `v274_preparation_accompagnee.sql`, suivi/événements/terrain,
projections et index des sélecteurs, opérations et tentatives. Les reprises de
données incohérentes échouent atomiquement avec un diagnostic ; elles ne
créent aucun droit ni service historique fictif. La surveillance des retards
est bornée, simulée par défaut, et indépendante de l’ouverture de nouvelles
demandes. Elle écrit une alerte unique par demande/version d’échéance, sans
modifier la version métier à chaque passage. Ops lit au plus 26 références
et affiche une borne `25+` si nécessaire.

La [procédure de préparation accompagnée](../../exploitation/exploitation/preparer-chasse-accompagnee.md)
décrit les responsabilités, le calendrier et les configurations préparées :
`LOCALEO_PREPARATIONS_ACCOMPAGNEES_APPLY`,
`LOCALEO_PREPARATIONS_ACCOMPAGNEES_ALERTES_APPLY`,
`LOCALEO_CALENDRIER_SERVICE_JSON`. Aucune valeur d’horaire métier ni ouverture
d’environnement n’a été imposée.

Preuves exécutées à ce stade, sans additionner les suites qui se recouvrent :

| Contrôle | Résultat local |
| --- | --- |
| Architecture, recensements, domaine, application et API | **621 réussites**, 31,96 s ; `tmp/e73-lot07-architecture-final18.xml`. La passe précédente avait 15 erreurs de préparation du répertoire Windows global, résolues par le répertoire isolé du dépôt sans changer les assertions |
| Génération E55, suivi accompagné, conservation et pagination PostgreSQL | **53 réussites**, 194,77 s ; `tmp/e73-lot07-pg-final16.xml` |
| Préparation historique et contrôle de publication terrain | **38 réussites**, `tmp/e73-lot07-publication15.xml` |
| Exports OpenAPI documentaires | **10 réussites**, 76,66 s ; `tmp/e73-lot07-contracts-final-01`. E41 : 876 chemins ; E42 : 55. E41 embarqué Animation identique au canonique après normalisation des fins de ligne |
| Calendrier, surveillance, disponibilité catalogue et régression tableau Ops | **29 réussites**, `tmp/e73-lot07-root-final-02` |
| Disponibilité injectée dans les commandes de forfait et régressions souscriptions | **43 réussites**, quatre avertissements de dépréciation ; `tmp/e73-lot07-readiness-regression-01` |
| Migration complète depuis une base vide, rejeu et modèles | **3 réussites**, 78,46 s ; `tmp/e73-lot07-migrations-final-03` |
| Reprise de projections historiques et rollback sur incohérence | **2 réussites**, `tmp/e73-lot07-reprise-01` |
| Surveillance concurrente et lecture Ops avec historique volumineux | **2 réussites**, `tmp/e73-lot07-surveillance-pg-03` |
| Sélecteurs PostgreSQL | **3 réussites** ; 26 plans sur 10 000 lieux, 10 000 modèles et 10 000 commerces ; deux requêtes par page, aucun balayage séquentiel des catalogues |
| Portail Animation, copie HEAD + seuls fichiers du lot | **212 tests Node**, types/lint/build réussis ; suivi **18 scénarios/234 assertions**, génération **74**, préparation chasse **258**, mobile/bureau et affichage Paris |
| ERP préparation et génération | Recettes navigateur 320/1 280 px et 390/1 280 px réussies ; action accessible sans Atelier Coffrets |
| Sonde du générateur synthétique | **1 réussite**, 85,09 s ; vérification globale du jeu, droits client/lecteur, complément réel et absence de débit de publication |

Les performances des opérations ont été éprouvées avec 10 000 opérations du
tenant, 10 000 opérations antérieures d’autres tenants et 10 000 tentatives :
pages 1/100 en deux requêtes, sans plan forcé et sans chargement des gros
résultats. Le détail borne ses tentatives à 25 et fournit la suite paginée.
La surveillance a également été mesurée avec 10 000 archives, 10 000 demandes
en attente et 201 actives, sur les index partiels de file et d’Ops. Artefacts :
`.artifacts/e73-preparation-pagination-performance.json`,
`.artifacts/e73-selecteurs-performance.json` et
`.artifacts/e73-preparations-alertes-performance.json`.

Revue croisée : corrections des contrats de curseur, de la revalidation de
session, du lien d’email vers la route réelle du portail et de deux dépendances
vers l’infrastructure. Les reprises automatiques E55 ne sont pas bloquées dès
la première erreur transitoire ; leurs dates historiques sans fuseau sont
écrites et comparées en UTC. Les sources du générateur préservent l’ordre
global des verrous et emploient une période annuelle cohérente avec les droits.

La revue indépendante des raccords de surveillance et de disponibilité n’a
relevé aucun défaut bloquant (`tmp/e73-lot07-revue-root-w2.md` dans le backend).
Les contrôles documentaires passent : **94 guides / 1 003 liens**, aucune erreur
ni alerte, et **127 sources exportées**. Le premier contrôle d’export a détecté
un identifiant de bundle utilisant le chemin source ; il a été corrigé vers
le namespace documentaire `docs/ops`, sans déplacer la source canonique.

Générateur et restauration : la suite complète a réussi **7 scénarios sur 8**
(360,05 s, quatre avertissements de réflexion SQLAlchemy,
`tmp/e73-lot07-demo-complete-02`). Le huitième a identifié un contrôle de fixture
qui comptait les versions de configuration comme des animations distinctes.
La correction vérifie toutes les versions, dix animations avec chacune un
visuel cohérent et dix visuels distincts. Elle conserve les contrôles stricts
de neutralisation des emails et emploie de vraies sessions synthétiques pour
les lectures produit désormais protégées. Ce seul scénario a été rejoué avec
succès : **1 réussite**, 56,50 s, un avertissement de réflexion,
`tmp/e73-lot07-demo-relations-reprise-01.log`. Les sept scénarios non modifiés,
dont export/restauration, n’ont pas été rejoués inutilement. Aucun échec n’est
masqué. Une ligne vide finale de v274 a été supprimée au contrôle Git, sans
modifier son SQL ; aucune base partagée n’a été touchée.

Commits locaux du lot 07 : Backend `44c6429`, Animation `8979893`, sources dans
le commit documentaire du lot 07. Aucun push ni déploiement.
Pro et Marketplace ne consomment pas ces nouvelles routes. Les deux sélecteurs
historiques exhaustifs restant dans App et le bundle principal Animation sont
suivis aux lots 09/10. La conservation physique des nouvelles familles reste
à prouver au lot 10. Recette humaine et hébergement : non exécutés.

### Lot 08 — Communication participants

Périmètre : US21–22, CA47–49. Le portail propose préparation, aperçu,
programmation, confirmation, rapport et reprise d'une campagne. Les quatre
groupes restent limités à une animation. L'état de traitement, le dépôt Live
et le résultat Push sont distincts. Les dates sont affichées en Europe/Paris.
Les formulaires préservent les propositions et réconcilient une réponse perdue
par reçu avant toute répétition explicite de la même commande.

Le domaine possède les transitions et décisions de fenêtre, préférence,
sollicitation et audience. L'application capture puis prépare une audience
durable par lots, débite un crédit au premier dépôt Live et reprend sans
modifier audience ou compteur. Le transport est séparé, avec baux et intentions
durables ; les fournisseurs sont simulés dans toutes les preuves. Une campagne
sans destinataire autorisé ne consomme aucun crédit.

La préférence organisateur est explicite et indépendante du consentement
historique aux notifications. Le message est disponible sans installation Push,
puis peut être lu après liaison personnelle vérifiée d'un carnet. Les listes
fusionnent des pages bornées et n'exposent aucun endpoint ou secret. Un retrait
de préférence, de droit ou une suspension reste contrôlé côté serveur.

L'ERP permet de consulter le réglage communal et les alertes, puis de les
modifier avec l'autorisation dédiée `animation:sollicitation_gerer`, un motif et
une version. La configuration initiale reste 1 message/24 h et un seuil à 3×.
Les alertes sont regroupées par commune/période, avec un email interne à leur
ouverture ; ni reprise ni clôture ne remettent la fréquence à zéro. Une garde
partagée du réglage empêche sa modification concurrente pendant la décision.

Migration `v275_campagnes_organisateur.sql` : 23 tables dédiées, index de listes,
files et purges, nouvelles dates effectives Animation et permission ERP sans
octroi automatique. Le backfill exige des preuves de publication et de clôture,
dont un gel de population pour cette dernière. L'absence de preuve conserve une
fenêtre à vérifier. La migration n'active aucun module ni worker.

Preuves root déjà exécutées (runner backend isolé ; suites recouvrantes) :

| Contrôle | Résultat local |
| --- | --- |
| ERP PostgreSQL/API/configuration | **24 réussites**, `tmp/e73-lot08-root-pg04.xml` : CAS, concurrence, rollback email/alerte, grant/session révoqués dans la composition réelle, garde tenant contre suspension |
| Disponibilité commerciale et configuration finale | **13 réussites**, `tmp/e73-lot08-readiness02.xml` ; trousseau, emails internes, VAPID et flags des deux workers requis pour les nouveaux usages |
| Exécuteur campagnes | **8 réussites**, `tmp/e73-lot08-execution.xml` ; simulation sans claim/écriture et budget avant le lot suivant |
| Migration vide/rejeu/atomicité/modèles et reprise historique | **4 réussites**, 62,44 s, `tmp/e73-lot08-migrations02.xml` ; PostgreSQL local jetable, schéma final des 23 tables |
| Réponses HTTP Animation | **11 réussites**, `tmp/e73-lot08-responses02.xml` ; deux réponses antérieures complétées dans OpenAPI sans changer leur JSON |
| ERP mobile/bureau | `node tests/browser/epic73-sollicitations.cjs` réussi à 320/1 280 px : 404 du reçu puis renvoi de même clé, attente202, CAS409 avec proposition reprise et confirmation, pagination, lecture seule, texte échappé et Paris |
| Chargement réel du module ERP | **6 réussites**, deux avertissements de dépréciation, `tmp/e73-lot08-assets03.xml` : contrôle HTTP de la page et du module `sollicitations.js` ; ajout de ce fichier à la liste d'assets autorisés, oubli non détectable par la recette navigateur servie sur des fixtures |
| Campagnes : domaine, PostgreSQL, HTTP réel, HMAC et performance | **54 réussites**, 182,49 s, `tmp/e73-lot08-pg12.xml` ; débit concurrent du dernier crédit, rollback du premier dépôt, audience figée et fenêtre après démarrage |
| Participants et synchronisation existants | **8 réussites**, `tmp/e73-lot08-legacy01.xml` |
| Derniers cas campagnes et recensement | **33 réussites**, `tmp/e73-lot08-target14.xml` : 30 tests domaine, recensement complet et roundtrip UTC sous fuseau SQL Europe/Paris ; reprise du cas de fixture signalé dans `final13` |
| Architecture et API antérieures | **586 réussites** dans `tmp/e73-lot08-architecture02.xml` et un échec de déclaration de preuve ; ce dernier est corrigé et rejoué dans `target14`, sans skip ni exclusion |
| Exports documentaires et contrat Live | **10 réussites**, `tmp/e73-lot08-contracts03.xml` ; E41 **896 routes**, E42 **60 routes** |
| Live, préférences, transport, concurrence et purge | Ensemble de **47 tests distincts** validés au fil des suites W2 : 17 PostgreSQL, 11 domaine, 9 API, 9 transport/CLI et 1 performance ; détails dans la note locale backend `tmp/e73-lot08-preuves-w2.md` |
| Animation, seuls fichiers du lot dans une copie du HEAD | **220 tests Node**, types/lint/build réussis ; **36 scénarios navigateur / 684 assertions**, 320/1 280 px et fuseau Los Angeles ; trois contrats campagnes rejoués après l'export définitif |
| Marketplace / Live | **113 tests de sécurité**, lint ciblé réussi, **12 scénarios navigateur** (neuf antérieurs et trois nouveaux) ; les trois nouveaux rejoués avec code natif 0 après un avertissement de l'enveloppe PowerShell |
| Accessibilité Live additionnelle | **1 scénario réussi**, 21,3 s : 320 px et texte agrandi à 200 %, navigation clavier, accord/retrait/lecture/fermeture sans débordement ; le débordement du titre constaté à la première passe a été corrigé, captures inspectées |
| Démonstration et cycle complet sauvegarde/transfert/restauration | **9 réussites**, aucun échec ni skip, 509,77 s, `tmp/e73-lot08-demo-complete02/results.xml` ; scénario Communication avec les deux flags finaux ; six avertissements SQLAlchemy de réflexion. L'exécution précédente interrompue ne constitue pas une preuve |

La page profonde d'alertes parmi **20 000 lignes** (10 000 dans la commune et
10 000 ailleurs) utilise l'index communal et lit 26 lignes pour une page de 25,
sans OFFSET ni balayage de l'autre commune. Une première assertion avait détecté
l'emploi de l'index global ; le curseur inclut désormais la commune dans la
comparaison, sans forcer le plan ni affaiblir le test. Artefact local backend :
`.artifacts/e73-sollicitation-performance.json`.

Campagnes : sur **10 communes et 10 000 participants**, les pages de 1 et 100
éléments utilisent chacune 20 requêtes. Dix lecteurs simultanés ont pris de
0,191 à 1,039 s par lecture sur le poste local ; la capture de 1 000 participants
a pris 0,260 s. Les index sont vérifiés sans forçage du plan. Messagerie :
10 000 messages personnels, 10 000 notifications historiques et 10 000
participants ; deux pages et leurs cent faits exigent cinq requêtes, sans
balayage des grandes tables. Ces mesures ciblées ne démontrent ni le mélange
de parcours du lot 10 ni la capacité de l'hébergement cible.

Le chunk Communication est chargé à la demande (36,32 ko ; gzip 9,91 ko).
L'avertissement sur le bundle principal Animation reste pris en charge au lot
09. Le commit local Animation est `08f4d98` ; il contient seulement les 21
fichiers vérifiés, avec les quatre hunks Clôturer et les autres modifications
utilisateur préexistantes laissés hors index.

Marketplace : commits locaux `0fa79e4`, puis `c16bb30` pour le correctif
320 px/texte à 200 %, sans réécriture d'historique. Son lint global rencontre
un refus d'accès Windows dans le répertoire historique de sortie
`output/demo-generation/pytest-bum-registry` ; le lint des sources et des tests
touchés a réussi, sans ajout d'exclusion pour masquer ce refus.

Backend : commit local `2cda9d6`, 92 fichiers explicitement indexés. La commande
finale `run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot08-demo-complete02` a terminé avec le code 0. La base
de construction jetable a été recréée avant cette exécution après le retrait
d'espaces de fin de ligne dans v275 ; aucune empreinte de migration appliquée
n'a été contournée. Les sources et l'index sont restés figés pendant la preuve.

La revue indépendante a corrigé la fenêtre +30 jours dans les reprises et la
projection du rapport pour ne pas restituer de compteur technique hors contrat.
Les contrôles globaux ont également révélé deux réponses anciennes non décrites
(batch d'exemplaires et demande de mot de passe), désormais modélisées. Les
premiers contrôles de recensement ont signalé des classes sans preuve dédiée ;
leurs résultats ne sont pas présentés comme une suite verte.

La [procédure Communication](../../exploitation/exploitation/communiquer-participants-animation.md)
décrit réglages, préférences, workers, rotations de clés et reprise. Les contenus
des messages suivent la politique Live existante ; le raccord transversal aux
gels/purges et la preuve après restauration des nouvelles familles restent au
lot 10. Les essais utilisateurs Localeo/Martignas et toute capacité hébergée sont
non exécutés. Aucun fournisseur réel ni environnement partagé n'a été utilisé.

### Lot 09 — Parcours, site, assistance et mesure

Les parcours sont implémentés et vérifiés localement ; les contrôles communs,
la démonstration complète et les commits applicatifs sont terminés. Le
[guide opératoire](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrit l'assistant, les éditions, les bilans, la recherche et le support privé.
Cette réalisation locale ne vaut pas mise en service ni clôture de l'epic.

Le support utilise le stockage Contact commun pour les messages et un canal privé
exclu des anciennes listes, détails et exports SQLAdmin. La portée de la demande,
les réponses et les notes internes relèvent de `DemandeSupportOrganisation` ; les
notes ne constituent pas une première réponse. Les droits courants sont contrôlés
avant lecture, écriture et réconciliation de reçu. Une réponse et son intention
email sont atomiques ; un échec de préparation annule l'ensemble.

L'assistant consulte les propriétaires des règles sans publier, modifier les
statuts ni consommer de crédit. La disponibilité du module est injectée depuis la
composition ; l'application ne lit pas un adaptateur de configuration. Un brouillon
peut être préparé avec un droit actif et un quota de publication épuisé.

Preuves exécutées par l'intégration :

- Support domaine et PostgreSQL : **20 réussites**, `tmp/e73-lot09-support-pg04.xml`.
- HTTP privé, ancien SQLAdmin et CLI de réconciliation : **9 réussites**, deux
  avertissements de dépréciation, `tmp/e73-lot09-support-http02.xml`. Le premier
  essai HTTP avait quatre réussites et un échec de fixture sans session Starlette ;
  cette fixture a été corrigée puis rejouée, sans changement d'assertion.
- Assistant, disponibilité et régression publication : **15 réussites**, deux
  avertissements, `tmp/e73-lot09-assistant01.xml`. Le contrôle PostgreSQL du quota
  sans écriture a également réussi dans `tmp/e73-lot09-support-http01.xml`.
- Support navigateur : commande `node tests/browser/epic73-support-organisations.cjs`
  réussie à 320 et 1 280 px, avec agrandissement effectif de chaque texte à 200 %,
  reçus 404/202, rechargement, conflit de version, pagination, notes et lecture seule.
  Captures locales inspectées ; dernier ajustement des libellés de succès rejoué
  avec le code 0 : réponse, note interne et changement de statut restent distincts.
- Migration depuis base vide, rejeu, atomicité et correspondance de tous les modèles :
  **3 réussites**, 221,45 s, `tmp/e73-lot09-migrations01.xml`, PostgreSQL local jetable
  `localeo_audit_migrations_test`. Aucun SQL appliqué à un environnement partagé.
- Premier contrôle d'architecture : 563 réussites, 15 erreurs de permissions du
  répertoire temporaire Windows et un échec de déclaration des preuves de quatre
  classes. Les déclarations ont été corrigées ; reprise avec `--basetemp` dédié :
  **586 réussites**, 44,52 s, deux avertissements, `tmp/e73-lot09-architecture02.xml`.
  Cette reprise vérifie aussi les routes HTML et le chargement réel du module Support.
- Régression Support et recherche publique temporairement indisponible : **65
  réussites**, 52,10 s, deux avertissements, `tmp/e73-lot09-support-regression01.xml` ;
  HTTP 503 explicite, sans cache ni détail interne, lorsque la projection manque.
- Architecture et recensement final après correction de publication : **580
  réussites**, 17,25 s, `tmp/e73-lot09-architecture-final.xml`.
- Contrats OpenAPI, export documentaire et réponses Animation : **21 réussites**,
  29,85 s, `tmp/e73-lot09-contracts-final.xml` ; E41 **925 routes**, E42 **62 routes**.
  Le contrat runtime final est recopié en LF auprès du consommateur Animation.

La revue indépendante a relevé une validation de publication historique susceptible
de synchroniser un statut après le débit du quota. Le contrôle est désormais sans
écriture : **16 tests PostgreSQL** prouvent la lecture pure, le rollback du débit et
le refus des reçus/commandes après révocation. Les fixtures T3 gardent leurs assertions,
avec une dotation explicite et un journal de débit réellement transactionnel. La
dernière régression HTTP brouillon/bilan a **14 réussites** après correction de huit
fixtures utilisant l'ancien appel de génération ; les assertions de refus restent
inchangées. Les entrées ERP conservent leur contrôle d'identité à l'entrée de requête.

Valorisation : **29 tests domaine/API/PostgreSQL**, puis **46 contrôles de
réconciliation/moteur/bilan** et **11 contrôles API historiques** réussis dans des
suites qui se recouvrent. La parité Coffrets est vérifiée sur PostgreSQL : deux
instances, deux prestations consommées sur trois, 20 euros et gagnants distincts.
Les mesures de progression restent indisponibles quand leur couverture est incomplète.

Performances locales, sans forçage du plan PostgreSQL :

- Bilans : **10 communes, 10 000 participants, 10 lecteurs simultanés** ; une requête
  d'agrégation pour une ou dix éditions, aucune population hydratée, pic mémoire
  observé 113 759 octets, p95 710 ms et maximum 714 ms. Artefact backend
  `.artifacts/e73-lot09-valorisation-performance.json`.
- Support : **20 100 demandes**, page profonde à 19 000, six filtres ; une requête
  et au plus 26 objets pour 25 résultats, plans indexés, 10 à 29 ms observés.
  Artefact `.artifacts/e73-lot09-support-performance.json`.
- Sélecteur Coffrets : **20 000 coffrets**, quatre requêtes pour une page de 25
  comme de 100 ; parité de couverture prouvée par six cas PostgreSQL. Artefact
  `.artifacts/e73-coffrets-selecteur-performance.json` et `tmp/e73-lot09-coffrets04.xml`.
- Recherche publique : **10 005 animations**, deux requêtes, tri/visibilité avant
  limite et plans indexés ; trois cas PostgreSQL réussis. L'ancien test de classement
  en mémoire a été adapté à la frontière SQL puis les **17 tests** ont réussi dans
  `tmp/e73-lot09-search-unit-final.xml`, après un échec de compilation du double SQL.

Animation : **230 tests Node**, trois contrats HTTP rejoués sur l'export final,
types/lint/build réussis sur une copie ne contenant pas les changements préexistants.
**26 scénarios navigateur / 293 assertions**, 320/1 280 px et texte 200 %, auxquels
s'ajoutent les régressions sélection et lots/configuration. La recette de création
vérifie désormais l'arrivée dans l'Assistant avant d'ouvrir la Configuration ; les
assertions de paiement, quantités et droits sont conservées. Les filtres du bilan
global sont préservés au retour, avec deux scénarios supplémentaires réussis.
Le bundle principal est ramené à **498,18 ko / 127,89 ko gzip** par chargement différé.

Marketplace/Live : **115 tests de sécurité**, **13 tests serveur**, lint ciblé et
build isolé réussis ; **10 scénarios navigateur**, puis une reprise mobile après
le dernier ajustement de la synthèse des communes. Les deux surfaces partagent le
socle et la valeur par défaut reste Coffrets. Aucun domaine n'est créé ni configuré.

La migration **v276** prépare les huit tables Support/Valorisation, leurs index,
le motif Support privé et la projection de recherche publique. La reprise de
recherche est une commande explicite, bornée et simulée par défaut ; aucune
configuration opérateur ni donnée d'exploitation n'est modifiée ici.

La démonstration a d'abord refusé une base de construction non vide. Après
vérification de la cible locale jetable et de l'absence d'animations/commerces,
cette seule base a été recréée. La passe suivante a été interrompue après cinq
échecs : le scénario ajoutait des objectifs sur une nouvelle édition dont l'UUID
ne respectait pas l'ordre des coordinations déjà verrouillées par le générateur.
Le scénario règle désormais les objectifs sur le brouillon historique déjà
verrouillé et conserve l'édition nouvellement créée vierge. Le produit et ses
contrôles de verrous ne sont pas assouplis. La reprise ciblée réussit : **1 test**,
77,06 s, `tmp/e73-lot09-demo-target01.xml`, avec rechargement des huit tables.
Les unités du générateur et son registre comptent **23 réussites**, aucun skip.
Ces passes intermédiaires ne remplacent pas le résultat du runner complet.

Le runner complet a ensuite réussi sur les sources finales : **10 réussites**,
aucun échec ni skip, **571,16 s**, sept avertissements SQLAlchemy de réflexion
`dialect_options`, code de sortie 0. Artefact backend :
`tmp/e73-lot09-demo-complete03/results.xml`. Commande :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot09-demo-complete03`, avec le runtime Python local isolé.
Elle couvre les scénarios métier, le transfert, la reprise après interruption
et la restauration de la base d'origine jetable. Aucun fournisseur réel ni
environnement partagé n'a été utilisé.

Contrôles documentaires finaux : **98 guides, 1 085 liens, zéro erreur ni
avertissement** ; **129 documents exportables** vérifiés. Les contrats E41/E42,
le contrat embarqué Animation et le guide opératoire sont synchronisés.

Commits locaux applicatifs : Backend **`76103d7`** (94 fichiers), Animation
**`eb3def9`** (30 fichiers), Marketplace **`70d7128`** (21 fichiers). Les quatre
modifications préexistantes Clôturer d'`App.tsx`, ainsi que le README, la vue
Exploitation et son test, restent hors commit Animation. Le suivi moteur
préexistant du dépôt Projet reste également exclu. Aucun push ni déploiement.

À la fin du lot 09, les pages de sélection et suggestions publiques sont bornées ;
la vue Coffrets globale et ses totaux historiques restent alors à traiter dans le
lot 10. Cette réserve est reprise ci-dessous après l'autorisation de poursuivre. Les recettes
humaines et hébergées restent non exécutées ; ces mesures ne constituent pas le
test de charge mixte ni une garantie de capacité sur l'hébergement cible.

### Lot 10 — Exploitation, réversibilité et consolidation

Reprise explicitement autorisée le **19 octobre 2026**. Le lot complète le
pilotage économique interne (US34), la réversibilité et la fermeture accompagnée
(US35), les lectures ERP/Support (US24), la conservation et les outils de reprise.
La [prise en main par lot](prise-en-main-par-lot.md) décrit les accès des dix lots ;
le [guide opératoire](../../exploitation/exploitation/exploiter-saas-animation.md)
décrit les traitements préparés, leurs paramètres et les étapes de mise en service
qui restent à exécuter séparément.

**Comportements implémentés.** Le suivi économique distingue faits constatés,
estimations et données indisponibles. Les corrections sont historisées, les
budgets déclenchent des alertes internes à 80/100 %, sans effet commercial.
Les mesures archivées ne peuvent pas être réactivées par une nouvelle
valorisation ; les marges restent indisponibles tant qu'aucun rapprochement
comparable des revenus n'est établi.

L'export est demandé par le responsable, capturé dans un instantané cohérent,
assemblé par segments et téléchargé après nouvelle vérification des droits.
Il contient CSV, médias transmissibles, manifeste et guide, jamais les secrets
QR/PIN, mots de passe, notes internes ni données d'une autre organisation.
La fermeture interdit les nouveaux usages, inventorie les engagements selon
leurs états métier réels et exige leur résolution. Seules les préparations
accompagnées disposent en V1 d'une reprise interne effective ; aucun bouton de
transfert fictif n'est présenté pour les autres engagements.

L'ERP et le Support disposent d'**Animations et lots**, de listes et CSV de page
avec contrôle courant du périmètre communal. Les vues globales Participants,
Validations et Coffrets du portail utilisent désormais des pages serveur et
des synthèses distinctes. L'historique Pro ne parcourt plus toutes les preuves
expirées pour constituer une page. Les compteurs SQL sont des projections de
lecture transactionnelles, jamais une autorité pour qualifier ou tirer un gagnant.

La conservation rattache les familles aux durées existantes, traite gels,
copies SQL/JSONL/Live et fichiers privés, et conserve une preuve minimale.
Une date de fin absente est signalée, sans repli sur une date de création.
La reprise exige un journal indépendant et ferme les capacités restaurées,
y compris sessions internes et QR de bons, avant réouverture. Le lot et ses
droits commerciaux ne sont pas révoqués par cette fermeture technique.

**Migrations locales préparées et vérifiées :** v277 coûts, v278 réversibilité,
v279 conservation/reprise, v280 projection d'historique Pro, v281 index ERP/Support,
v282 pages globales, v283 compteurs de lecture. Le rejeu depuis une base vide,
l'atomicité, la correspondance des modèles et la disponibilité des colonnes/index
requis passent : **3 tests**, 51,45 s, `tmp/e73-lot10-migrations-final.xml`.
Aucune base partagée n'a été migrée.

**Contrôles transverses.** Architecture, recensement des classes de domaine,
couverture des use cases, Ops, ERP, batchs et readiness : **640 réussites**, deux
avertissements de dépréciation Starlette/AnyIO, 30,53 s,
`tmp/e73-lot10-final-architecture02.xml`. Le premier appel avec un chemin de test
inexistant n'a exécuté aucun test ; il a été corrigé, sans retrait de contrôle.
Les contrats canoniques E41/E42 et le contrat embarqué Animation ont été
régénérés hors ligne (985/62/985 chemins). Contrats API et registre démo :
28 réussites ; les quatre erreurs initiales d'accès au répertoire temporaire
Windows sont résolues par un répertoire local explicite, avec **8 réussites**
du fichier de tests documentaires complet au second passage. Les comptes de
ces suites se recouvrent et ne doivent pas être additionnés.

**Portail.** **233 tests Node**, zéro échec ou skip ; les deux nouveaux tests
rejouent les contrats HTTP fermés du producteur. Types, lint ciblé et compilation
réussissent sur le candidat isolant les changements préexistants. Le bundle
principal vaut 480,48 ko / 124,76 ko gzip. Navigateur : **12 scénarios / 100
assertions** export/fermeture/catalogue et **4 scénarios / 60 assertions** listes
globales, à 320/1 280 px, texte 200 %, clavier, fuseau Paris depuis un navigateur
réglé Los Angeles, réponse perdue et refus d'accès. Commit local Animation :
**`da86e39`**. Les quatre modifications Clôturer d'App.tsx, le README, la vue
Exploitation et son test restent hors de ce commit.

**Périmètre de performance.** Les nouvelles pages hydratent un volume borné et
les projections évitent les scans complets de participants/passages. La recherche
textuelle conserve un agrégat SQL exact sur les correspondances : son coût n'est
pas constant. Les agrégats acquisition/satisfaction/gains ont leurs propres
volumétries ; un essai à 100 000 participants ne prouve pas leur croissance.
La revue a aussi confirmé au HEAD du lot 09 les chargements historiques complets
de l'index Animation, des vues Tirages/Flyers et des participants d'une fiche.
Ils ne sont pas présentés comme corrigés ni comme couverts par les mesures des
nouvelles pages globales. La spécification n'impose pas une refonte générale de
ces lecteurs historiques ; leur dette reste à traiter avant de leur annoncer
les mêmes garanties de volume.

Les preuves finales de conservation, réversibilité, charge avec workers et
compatibilité démonstration sont consolidées ci-dessous après leur exécution.

**Réversibilité et lectures ERP/Support : 75 réussites**, aucun skip ou échec,
140,94 s, deux dépréciations Starlette/AnyIO,
`tmp/e73-lot10-portal-final02.xml`. Les contre-preuves couvrent notamment les
états terminaux réels des producteurs (tirages, gains Coffrets, remboursements),
les bons expirés encore prolongeables, la portée actuelle de l'opérateur, les
gels concurrents de fichiers/captures et le nettoyage borné de 103 segments par
pages de 25. Les quatre CSV et le ZIP ont leurs contrats binaires explicites.

**Conservation : 41 scénarios distincts finalement réussis**, aucun skip ni
échec restant, après déduplication des XML `e73-conservation14`, `date16`, `17`,
`18` et `19` sous `tmp/`. Le premier passage comptait 30 réussites et dix erreurs
de préparation liées au répertoire temporaire Windows. La reprise locale a aussi
corrigé deux fixtures : date historique UTC écrite naïve dans une colonne sans
fuseau, et sélection de l'email de renvoi par son identifiant d'opération plutôt
que du premier email du bon. Le test conserve le refus du QR/lien ancien, le code
d'erreur réel et l'acceptation du bon réémis. Le code de reprise traite explicitement
les dates UTC sans offset, sans dépendre du fuseau de l'hôte ou de PostgreSQL.
La revue indépendante des contrôles de conservation, des permissions du bilan
et du transfert/restauration démo est consignée dans les rapports de travail ;
ses constats ont donné lieu aux corrections et contre-preuves, sans skip ajouté.

**Démonstration complète : 10 réussites**, aucun échec ni skip, **729,58 s**,
sept avertissements SQLAlchemy de réflexion `dialect_options`,
`tmp/e73-lot10-demo-complete01/results.xml`. Le runner migre jusqu'à v283,
génère les scénarios des lots précédents, transfère les données, simule une
interruption, reprend puis restaure la base d'origine. Le registre classe les
24 nouvelles tables ; les quatre projections déclenchées par triggers sont
restaurées après leurs sources. Les contrôles locaux de purge et de reprise ne
sont pas transférés avec un jeu, mais le dump complet vérifie leur empreinte ;
altérer le verrou de reprise dans la base d'essai fait refuser sa réutilisation.
Les **63 tests ciblés** du registre, des reprises et du runner passent également
(`tmp/e73-lot10-demo-units-final.xml`). Aucun service fournisseur ni base partagée
n'a été appelé. Après cette passe, seules les fins de ligne/espaces finaux du SQL
v277 généré et du module d'index de conservation ont été normalisés, avec contrôle
d'identité du contenu hors espaces ; le rejeu de migrations est vérifié à nouveau.

**Cœur coûts/lectures : 43 réussites**, deux dépréciations, 42,60 s. La dernière
contre-preuve purge réellement une mesure puis tente sa recollecte pendant et
après la transaction : aucune mesure, tête, valorisation ou projection n'est
recréée. La vérification du reçu d'effacement partage les verrous de la purge.
Le bilan réutilise seulement les permissions vérifiées dans sa transaction :
une nouvelle requête après révocation perd les actions puis l'accès de lecture.

**Charge locale et limites.** Le bilan Gestionnaire corrigé passe : un test,
22,68 s, p95 364 ms / p99 374 ms pour un budget p95 de 900 ms. À nombre
d'animations affichées fixe, les populations ne sont pas hydratées.
Le banc de services applicatifs/PostgreSQL, avec un worker de coûts et dix
acteurs, donne les résultats suivants (millisecondes, p95) :

| Participants / distribution | Bilan | Participants | Validations | Remise |
| --- | ---: | ---: | ---: | ---: |
| 10 000 équilibrés | 462 | 537 | 465 | 603 |
| 10 000 concentrés | 393 | 372 | 252 | 620 |
| 100 000 équilibrés | 407 | 578 | 542 | 639 |
| 100 000 concentrés | 416 | 397 | 387 | 513 |

Les budgets restent 900/700/700/1 000 ms. L'essai 10 000 équilibrés initial
partageait le CPU avec un build ; le rejeu est isolé. Le premier 100 000 équilibré
atteignait 707 ms pour les validations ; une vérification isolée unique donne
542 ms. Les résultats initiaux sont conservés. À vingt acteurs, plusieurs budgets
sont dépassés (jusqu'à 1 497 ms pour une remise) : cette capacité supplémentaire
**n'est pas acquise**. Huit actions par acteur, pause de 20 ms : ces essais courts
ne démontrent pas un débit soutenu de production.

Le scénario **E73-PERF-08 à cinq workers réels** passe : **un test, 119,14 s**,
aucun échec/skip (`tmp/e73-lot10-workers-performance-final02.xml`). Dix communes,
10 000 participants, dix acteurs, import/campagne/export/tirage/coûts démarrés
ensemble, sans charge extérieure. Les p95/p99 sont respectivement : bilan
463/514 ms, participants 575/583 ms, validations 482/534 ms, remise 779/877 ms.
Zéro erreur ; 80 actions pendant une phase de 16,993 s, soit 4,71 actions/s ;
pic RSS 147 Mio, 15 connexions de pool et six sessions en attente de verrou au
maximum observé (ce dernier indicateur n'est pas une durée d'attente).

L'export termine en 16,97 s, le tirage en 5,63 s dont 102 ms pour le scellement.
Après 18 tours de reprise, 89,39 s, les comptes finaux sont vérifiés : **100
commerces importés, 1 000 messages Live, 100 attributions, 700 faits de coûts**
sans doublon, et archive disponible de **10 000 participants** segmentés par 100.
Le premier essai échouait parce que la fixture omettait les modèles de dossiers
de souscription ; l'ajout des modèles réels corrige la fixture sans changement
du produit, ni allègement du volume ou des budgets. Son XML et ses mesures brutes
restent conservés.

Limites : le trafic passe par les services applicatifs et PostgreSQL locaux,
sans HTTP/proxy ni fournisseurs externes. La campagne prépare ses destinataires
pendant la charge ; les dépôts Live sont effectués au drainage. Le tirage porte
sur une autre commune de la même organisation. Le scénario à cinq workers ne
porte que sur 10 000 participants/dix acteurs ; les paliers supérieurs ci-dessus
ont seulement un worker de coûts. Les preuves ne sont pas un SLA hébergé.
Les artefacts détaillés sont conservés dans `.artifacts/e73-charge-workers-locale.json`
et `.artifacts/e73-charge-mixte-locale-matrice-finale-brute.json` du backend,
avec les replays et diagnostics ; ils ne sont pas ajoutés au dépôt documentaire.

**Contrôle final des candidats commités.** Après normalisation des espaces du
SQL v277, le rejeu complet, les modèles et le contrôle de readiness passent à
nouveau : **3 tests, 42,71 s**, `tmp/e73-lot10-migrations-final02.xml`. Cette
modification purement textuelle ne justifie pas de rejouer les douze minutes du
cycle de démonstration déjà réussi.

Le complément d'annulation des lectures passe ses **17 tests ciblés**, dont huit
nouveaux, et son lint. L'ensemble du portail compte désormais **241 tests Node
réussis**, zéro échec/skip, 31,14 s (`tmp/e73-lot10-node-final02.log`). Types,
lint du candidat et build passent sans charger de configuration opérateur ; le
bundle principal est de 480,48 ko / 124,75 ko gzip. Les parcours navigateur sont
rejoués après ce complément : **4 scénarios / 60 assertions** pour les lectures
globales et **12 scénarios / 100 assertions** pour export/fermeture/catalogue.
Les signaux interrompent effectivement les GET et leur lecture JSON/ZIP,
préservent les autres abonnés d'une requête dédupliquée et ne réessayent pas
une lecture annulée. Les écritures déjà parties restent suivies ; aucun arrêt
universel d'un SQL serveur déjà engagé n'est revendiqué.

**Bilan local final.** Les dix lots sont implémentés, avec les contrôles,
contre-preuves et limites consignés dans ce journal. Les parcours accessibles
par lot sont décrits dans la [prise en main](prise-en-main-par-lot.md), les
opérations dans le [guide SaaS](../../exploitation/exploitation/exploiter-saas-animation.md).
Le lot 10 est enregistré localement dans Backend **`7f74166`**, Animation
**`da86e39`** et **`3801cc5`**, puis dans son commit documentaire. Le complément
Animation isole la correction d'annulation détectée lors de la revue finale.
Pro et Marketplace ne nécessitent pas de nouveau changement de code dans ce
lot : les contrats QR/PIN/Live restent compatibles et sont contrôlés côté
producteur ; les adaptations antérieures sont dans leurs commits par lot.

L'epic reste **En cours dans la roadmap produit**, car l'acceptation humaine
Localeo puis Martignas-sur-Jalle, les branches de recette hébergées et la preuve
RPO **4 h** / RTO **8 h** ne sont pas exécutées. Les CA28/63 ne sont pas acquis
par des tests locaux. Les limites de charge à vingt acteurs et des lecteurs
historiques sont maintenues ci-dessus. Aucun push, pipeline distant, déploiement,
migration partagée ou envoi fournisseur réel n'a été effectué. Les travaux
préexistants exclus sont conservés dans leurs arbres de travail.

## Correctif du 22 octobre 2026 — module de stockage absent de la livraison

Le démarrage Render signalé échoue à l'import de
`app.infrastructure.storage.reversibilite` depuis l'API de réversibilité.
Le commit backend `7f74166` ne contient pas ce fichier, alors que sa copie locale
permettait aux tests de passer : la règle générale `storage/` du `.gitignore`
excluait également les nouveaux adaptateurs Python du stockage applicatif.

La règle conserve l'exclusion des données de stockage et ouvre uniquement les
sources `.py` de `app/infrastructure/storage/`. L'adaptateur existant
`reversibilite.py` devient ainsi livrable avec le correctif, sans modification de
sa logique. Les archives privées, caches, sauvegardes et fichiers `.env` restent
ignorés. Un test d'architecture exerce ces décisions avec Git dans un dépôt
temporaire ; il échoue sur l'adaptateur avant correction et passe ensuite.

Vérification locale : **618 tests réussis** pour l'architecture, le recensement
des classes de domaine et cas d'usage, et le contrat HTTP de réversibilité.
L'absence du module et l'erreur `ModuleNotFoundError` sont également reproduites
depuis une archive Git du commit, sans les fichiers locaux non versionnés.
Après ajout du seul adaptateur manquant dans cette archive, **5 tests réussissent**
(`tests/api/test_reversibilite_organisations_api.py` et
`tests/api/test_observability_errors.py`), incluant le chargement de `app.main`
et la génération OpenAPI. Les journaux privés sont dans
`.artifacts/storage-delivery-fnup7vta/` du backend. Tous ces tests utilisent
`scripts/validation/test_isolated.py` ; les contrôles documentaires
`check_guidance.py` et `sync_documentation.py --check-sources` réussissent aussi.
Deux avertissements de dépréciation FastAPI/Starlette restent
visibles ; ils ne constituent pas l'erreur de livraison.

Impacts : backend (contenu livré et exclusion Git) et ce suivi documentaire.
Aucune modification des contrats API, permissions, règles de conservation,
interfaces ou données de démonstration ; aucune migration supplémentaire.
La vérification isolée bloque les connexions et les envois externes. Aucun
commit, push ou redéploiement n'est réalisé par ce correctif local.

## Correctif du 22 octobre 2026 — invitation ouverte sous le compte de l’invitant

Lors de RM-02-02, l’invitation a été ouverte avec Mathilde, qui l’avait envoyée.
Ce scénario attend la création du compte destinataire ; l’acceptation avec un
compte déjà connecté relève de RM-02-03 et exige l’identité invitée. Le domaine
backend conserve cette vérification. L’écran ne montrait pas l’identité connectée
et ne permettait pas de changer de compte, ce qui rendait le refus peu exploitable.

Localeo Animation affiche maintenant le nom et l’email du compte connecté,
explique le choix et propose **Changer de compte**. Cette action réutilise la
déconnexion serveur existante, puis propose la connexion du destinataire ou la
création de son premier accès. L’invitation reste uniquement en mémoire dans
l’onglet ; son secret n’est pas réintroduit dans l’URL ou les stockages navigateur.
Un échec de déconnexion conserve l’écran de reprise et bloque la suite jusqu’à
confirmation serveur. Le message de refus indique aussi comment reprendre.
La réponse `MOT_DE_PASSE_REQUIS` fournie ensuite pendant la recette confirme
le cas d’un destinataire nouveau : l’interface explique spécifiquement qu’il
faut changer de compte puis créer le premier accès et définir le mot de passe.
Le code imbriqué dans `detail.code` est lu sans afficher le détail technique brut.

Preuve locale sur Animation `f0251a5` avec correctif : le banc navigateur
`tests/browser/account-app.mjs` échoue avant correction sur l’absence de l’email
connecté, puis réussit **124 assertions** à 1280/320 px, dont changement de compte,
création, reconnexion du destinataire, absence d’acceptation prématurée et reprise
d’une déconnexion échouée. Le complément reproduit aussi le 422
`MOT_DE_PASSE_REQUIS` avant de créer le compte : le test échoue sur le message
générique, puis confirme l’explication précise et la reprise sans nouvelle invitation.
API simulées, trafic externe bloqué ; ce banc ne prouve
pas la réparation d’une invitation hébergée. Le banc adjacent
`tests/browser/organisation-access.mjs` réussit **111 assertions / 24 scénarios**
à 1280/390/320 px. Les **18 tests Node ciblés** de
contrats organisation/session et d’expiration réussissent, ainsi que TypeScript,
ESLint et le build PWA isolé (`scripts/build-pwa-tests.mjs`). `pnpm` est absent
du PATH ; types et lint sont exécutés avec les binaires locaux via Node 24.14.0,
sans installation ni modification du verrou. Les captures du parcours sont dans
`tmp/generation-browser-dist/invitation-account-*.png` du dépôt Animation.
Les contrôles documentaires `check_guidance.py` (96 guides, 0 erreur) et
`sync_documentation.py --check-sources` (130 documents) réussissent également.

Impacts : interface Animation et recette RM-02-02/03 ; aucun changement du
contrat d’acceptation, de la règle métier ou du générateur, qui émet déjà les
invitations attendues. Aucune migration ni nouvelle configuration. Aucun accès
à l’environnement de test, envoi d’email, commit, push ou déploiement effectué.

Point de publication du **23 octobre 2026** : le correctif des invitations décrit
ci-dessus a été commité et poussé séparément dans `localeo-animation`, sur `main`,
sous **`4ee90c2`**. Le contenu exact du commit a été vérifié dans une copie isolée
de l’index : TypeScript, ESLint, build Vite isolé, **18 tests Node**, **124 assertions**
du parcours compte et **111 assertions / 24 scénarios** d’accès organisation réussis.
Les modifications de flyers sont restées locales et ne font pas partie de ce
commit. Le push n’atteste pas la version déployée ni la recette hébergée.

## Évolution du 22 octobre 2026 — E73-EVO-FLYER

Réalisation locale des [flyers contextualisés](flyers-contextualises.md), critères
ajoutés **E73-CA-FLYER-01 à 05**. Base lue : backend `5aed284`, Animation
`f0251a5`, projet `6d25510`, avec conservation des travaux locaux antérieurs
(invitation organisateur, configuration et automatisation de recette).

La charte de rendu passe à `LOCALEO_ANIMATION_MARKETPLACE_V5`. Le domaine prépare
la promesse Coffrets / lots externes / bons numériques, le nombre d'exemplaires
et de commerçants effectivement participants. Le compteur des lots libres vient
de la dotation, sans chargement de ses exemplaires ; une participation publiée
utilise sa liste figée sans requête inutile sur les invitations. Les faits et
l'identité de l'image participent à l'empreinte du rendu et sont revérifiés avant
rattachement. L'ancienne accroche automatique Coffrets est adaptée aux lots
libres ; une accroche personnalisée reste conservée.

Les commandes d'image portent la version de l'animation et une clé d'idempotence.
Le normalisateur est injecté depuis la composition infrastructure ; il vérifie
le contenu réel, les dimensions, la taille et retire les métadonnées. Le document
privé d'illustration est versionné indépendamment de la couverture publique et
de la configuration publiée. Le retour au défaut réutilise le visuel historique
de l'animation, sinon la photo embarquée. L'intention de stockage existante
couvre également une image préparée mais non rattachée après conflit.

Dans **Localeo Animation → animation → Flyer**, `FlyerWorkspace` propose les
deux compteurs, le contexte de dotation, le choix d'image avec aperçu,
l'enregistrement, le retour au défaut, la génération et le téléchargement.
Un fichier choisi doit être enregistré ou abandonné avant génération. Un PDF
obsolète reste explicitement identifié comme précédent. Le menu global Flyers
ouvre directement cet onglet et affiche « PDF disponible » sans prétendre
calculer la fraîcheur de chaque document ; le compteur et le filtre trompeurs
« à actualiser / à régénérer » y ont été retirés. Le détail vérifie sa fraîcheur.

| Critères | Preuves locales exécutées |
| --- | --- |
| FLYER-01/02 | Tests de contenu et de service, PostgreSQL dotations externe/numérique et participation effective ; rendu réel des trois modes |
| FLYER-03 | Tests image et PostgreSQL remplacement/retrait/version documentaire, navigateur aperçu/enregistrement/retour au défaut ; PDF final inspecté |
| FLYER-04 | Validation raster/volume/dimensions/animation/EXIF, refus lecteur/autre tenant, contrat HTTP réel et actions UI masquées |
| FLYER-05 | Rejeu et clé réutilisée, verrou/version, conflit après stockage avec intention d'orphelin, changement d'image/dotation/acceptation durant préparation, réconciliation navigateur et état périmé |

**Résultats sur l'arbre local final :**

- **61 tests backend ciblés réussis, aucun ignoré**, dont neuf cas PostgreSQL
  dans `tests/security/test_illustration_flyer_postgres.py`. Le complément couvre
  `test_flyer_prepare_postgres_t3.py`, les tests domaine de contenu et leur
  recensement dédié, `tests/application/services/test_flyer_animation.py`, les
  tests infrastructure du renderer et de l'illustration, et
  `tests/api/test_animation_locale_flyer_cache.py`.
- **624 contrôles réussis** : `tests/architecture`, recensements des classes de
  domaine/cas d'usage et tests de `PolitiqueParticipationPublicationAnimation`.
- **184 assertions navigateur réussies** pour les trois modes à 320/1280 px,
  avec lecteur, double clic, conflit de version, réponse perdue/récupération du
  reçu et actualisation pendant `EN_COURS`. Le parcours application complet
  depuis la liste Flyers passe aux deux largeurs, y compris l'absence de fausse
  synthèse de fraîcheur.
- **12 tests Node ciblés réussis** : dix tests mutation/pagination existants et
  deux tests `flyer-http-contracts.test.mjs` vérifiant le producteur OpenAPI et
  les requêtes réelles du client. TypeScript, lint et build PWA isolé réussis.
- PDF A4 et aperçu PNG des trois modes inspectés ; QR décodés avec l'URL exacte
  dans les six livrables. Les outils QA optionnels déjà présents dans
  `tmp/kit-qa/deps` ont été chargés pour exécuter les deux tests de décodage
  initialement ignorés, sans installation ni modification des dépendances.

Les tests backend utilisent `scripts/validation/test_isolated.py`, le runtime
Python local et uniquement PostgreSQL jetable sur `127.0.0.1:55473`, base
`localeo_audit_test`, avec schémas isolés. Les deux avertissements restants sont
des dépréciations FastAPI/Starlette. Les échantillons PDF/PNG et leur vérification
QR sont dans `.artifacts/flyers-e73/` du backend ; les captures UI dans
`tmp/flyer-personnalisation/` d'Animation. Ces fichiers de travail ne sont pas
déplacés dans le dépôt documentaire.

La revue indépendante a conduit à corriger le retour à l'illustration historique,
la conservation des fichiers préparés, l'injection du normalisateur, la lecture
inutile des invitations publiées et la présentation de fraîcheur dans la liste.
Les contrats sont générés hors ligne dans `epic-41-api/openapi.json` et les
routes/schémas concernés synchronisés dans le contrat embarqué Animation.
Les contrôles documentaires finaux réussissent : `check_guidance.py` (94 guides,
1 018 liens, aucune erreur), `sync_documentation.py --check-sources` (130 documents)
et `git diff --check` dans les trois dépôts concernés.

**Impacts et limites :** trois dépôts modifiés pour cette évolution : backend,
Animation et projet. Aucune migration, nouvelle variable, conversion de données
ni modification du formulaire Pro/Marketplace. Le générateur peut conserver
l'absence d'image dédiée ; les nouvelles fixtures locales couvrent les trois
dotations, sans génération distante. Les PDF historiques ne changent qu'après
régénération. Le corps JSON est lu par le framework avant validation de sa
longueur ; la borne HTTP du proxy reste applicable, distincte des contrôles
base64/image. La recette hébergée RM-FLYER-01 à 05 reste à exécuter. Aucun commit,
push ni déploiement effectué ; l'état global de l'epic reste inchangé.

## Correctif du 31 octobre 2026 — Live mobile, priorité aux interactions

Demande : optimiser Live sur téléphone comme espace de participation et de jeu.
Le test de reproduction démontre que l'action d'inscription sort du viewport
pendant la consultation des lots. La sélection de dix communes ajoute aussi
une longue liste avant le catalogue ; les bons sont présentés comme une liste
administrative répétitive.

La fiche publique conserve désormais son unique action principale au-dessus de
la navigation basse, avec mesure dynamique et espace réservé, puis revient dans
le flux sur écran bas. Les raccourcis lots/adresses/conditions remontent avant
les détails ; la récupération est nommée **Retrouver mon inscription**. La
provenance du lien et la distinction inscription/récupération sont conservées.
L'accueil présente une priorité dominante et deux suivantes compactes avec
anneaux réels ; **Les défis locaux** rejoint directement le programme. Le choix
des communes se déplie à la demande. Les cartes de découverte sont plus compactes.

**Mes lots** présente les bons personnels avec pictogrammes de récompense,
titre, dernier état connu explicitement local et action de consultation large.
L'état du bon exact est toujours vérifié à son ouverture. Les QR, accès sensibles,
consentements, inscriptions et reçus ne sont pas modifiés. Les lots non numériques
conservent leurs parcours existants ; aucun score ou gain supposé n'est ajouté.

Vérifications sur Marketplace/Live de base `0455fcc` et projet `607e27c`,
avec les modifications locales conservées :

- `npm run test:security` : **131 tests Node réussis**, aucun ignoré.
- ESLint réussi sur tous les fichiers JavaScript suivis et les deux nouveaux
  scénarios navigateur. Le lanceur global `npm run lint` rencontre un `EPERM`
  dans le dossier de travail `output/bum-politique/pytest-approval-1` ; le
  contrôle par liste Git couvre les sources sans modifier ses permissions.
- Build Vite/PWA isolé réussi via `scripts/serve-visual-tests.cjs`, sans
  charger les fichiers opérateur ni réécrire la configuration publique.
- **113 scénarios navigateur vérifiés** à 320/390/1280 px et autres formats
  de l'en-tête, avec texte agrandi à 200 % et écran bas. La campagne initiale
  donne 111 réussites et deux attentes de fixture erronées sur le bootstrap ;
  après correction de ce scénario, le fichier complet d'enrichissement est
  rejoué : **14 réussites**, aucun ignoré. Les autres sources restent identiques.
  Couverture : fiche publique, refus et dégradation, inscription complète,
  sauvegarde après erreur, récupération et inscriptions multiples, lots,
  communes, pagination et réponses tardives, navigation et conservation du
  parcours Coffrets. Les deux nouveaux bancs sont
  `tests/visual/live-mobile-actions.spec.cjs` et
  `tests/visual/live-lots-mobile.spec.cjs` ; ils incluent des contrôles de
  visibilité, cibles tactiles, séparation action/navigation et absence de
  mutation métier avant l'action explicite.
  Captures mobile et texte agrandi relues, conservées dans
  `localeo-marketplace/tmp/live-mobile-ux-2026-10-31/` hors versionnement.
- Revue indépendante : gardes et accès conservés ; aucune mutation introduite
  par les raccourcis, l'ouverture des communes ou la consultation des lots.
- `check_guidance.py` : **94 guides**, aucune erreur ;
  `sync_documentation.py --check-sources` : **130 documents** vérifiés.

La recette d'enrichissement personnel de la fiche a été remise en accord avec
le chargement déjà présent sur HEAD : GET public puis enrichissement facultatif
par une installation existante, sans renouvellement imposé par la fiche.
L'ancienne fixture omettait le GET public et attendait ce renouvellement.
Les nouveaux cas exigent le maintien de la fiche sur erreur privée 401/503,
l'absence de secret dans la lecture publique, la conservation du carnet et
de l'installation et les vrais refus publics 404/503 avec possibilité de réessayer.
Le scénario sans installation simule un refus 503 du bootstrap technique
anonyme de la coque Live : cette unique tentative ne bloque pas la fiche
publique et n'enregistre aucune installation, inscription ou autre mutation
métier. Ce bootstrap, déjà présent sur HEAD et distinct d'un compte, reste
inchangé ; son absence n'est pas une condition de consultation publique.

Impacts limités à Marketplace/Live et à la documentation canonique
[entrée unique](localeo-live-entree-unique.md#parcours-et-priorité-mobile).
Pas de changement backend, API, persistance, migration, variable de configuration
ni générateur : les données et commandes existantes sont réutilisées. Les
parcours Marketplace Coffrets et les applications Animation/Pro ne nécessitent
pas d'adaptation. Aucune opération sur un environnement hébergé, commit, push
ou déploiement réalisé ; la vérification sur TEST reste à faire après livraison.

## Correctif du 1er novembre 2026 — cohérence des espaces Localeo Animation

Demande : retrouver les mêmes repères de présentation, navigation, listes et
retours d’action sur le parcours de gestion. Sur la base Animation `f504b48`
et projet `e2ba317`, les pages composaient différemment les composants communs :
retours et contexte déplacés, contraintes de largeur propres à plusieurs pages,
onglets Finance en défilement horizontal et erreurs parfois réduites à un texte
isolé. La reproduction d’un résultat incertain constatait deux régions vivantes
pour le même diagnostic et sa consigne de vérification.

`WorkspaceHeader` réutilise `SectionHeading` : retour, icône, titre, description,
contexte puis actions suivent le même ordre sur mobile. Les espaces principaux,
création, détail, communication, compte/équipe, abonnement, support, imports,
catalogue, participants/validations, finance, flyers et bilans reprennent cette
composition. Les pages de gestion utilisent la largeur disponible ; les
dialogues gardent une largeur de lecture adaptée.

`WorkspaceTabs` présente les rubriques courtes sans défilement horizontal,
avec activation manuelle au clavier et sélection contrôlée. Le sélecteur du
bilan et les quatre espaces de navigation d’une animation gardent leur
fonctionnement. Les filtres secondaires se replient sur mobile ; le choix
principal de l’animation reste visible. Les filtres Flyers annoncent leur
sélection. Les listes gardent tableaux/fiches mobiles et pagination partagés.

`FeedbackMessage` et `ListState` unifient chargement, vide, erreur, avertissement,
information et confirmation, y compris les notifications et retours de commandes.
Un résultat incertain regroupe diagnostic et vérification explicite dans un seul
avertissement. Les points de focus prévus par les parcours restent volontaires.
Les contrôles ont aussi reproduit puis corrigé l’entrée clavier d’une sélection
désactivée/absente, des champs mobiles restant à 16 pixels avec texte agrandi et
une action Finance « Actualiser » de 15 pixels de haut sur bureau. Le minimum
mobile est désormais `max(16px, 1rem)` ; la règle commune des actions d’en-tête
garantit 44 pixels sur tous les formats, sans surcharge spécifique à Finance.

Preuves locales, API synthétiques et configuration isolée sans fichier opérateur :

- `npm run test` : **290 tests réussis**, aucun ignoré. Le test de conversion
  Paris conserve ses assertions ; son chargeur Node neutralise seulement
  l’import CSS ajouté par le composant partagé.
- Types, ESLint et build isolé `node scripts/build-generation-tests.mjs` réussis.
- Nouveaux bancs : `feedback-consistency.mjs` **220 contrôles**,
  `workspace-primitives.mjs` **188 contrôles**, `finance-workspace-ux.mjs`
  **187 contrôles**. Composants réels, clavier, gardes refusées/acceptées,
  états, ordre contexte/actions, cibles tactiles, 1280/390/320 pixels et texte
  à 200 %.
- Parcours rejoués : espaces de l’animation **40 cas** et navigation **8 cas**,
  abonnement/modules **70 scénarios / 994 assertions**, compte/équipe
  **56 / 388**, campagnes **36 / 684**, imports **22 / 292**,
  support/bilans/éditions **26 / 293**, lectures globales **4 / 60**,
  communication **12 scénarios**, sélecteur d’animation **16 scénarios** et
  accès Flyers/notifications **2 formats**. Refus, saisies, réconciliation
  après réponse perdue et clés existantes restent vérifiés.
- Création/préparation : **82 contrôles navigateur réussis** à 1280/390 pixels.
  Le banc conserve les assertions de conflit, saisie et réutilisation ; il suit
  le guide à cinq étapes déjà présent sur la base (`aria-current="step"`, puis
  Organisation et lots après le parcours, accès explicite à Terrain pour lire
  sa vérification), au lieu d’attendre l’ancienne composition de la page.
- Le banc support/bilan compte toutes les étapes de l’assistant, dont la
  prochaine action hors liste ; l’ancien comptage de neuf éléments `li` omettait
  cette présentation déjà présente sur la base. Les tests mobiles ouvrent les
  filtres secondaires avant usage. La fixture de notifications fournit la
  pagination attendue par le vrai collecteur.
- Captures relues sur bureau, mobile et texte agrandi ; sorties sous
  `localeo-animation/tmp/`, hors versionnement. Revue indépendante des primitives,
  états et écarts résiduels intégrée.
- Ancien `mobile-smoke.mjs` non démarré : son installation dédiée
  `tmp/mobile-qa/playwright` est absente. Cette limite reste distincte des bancs
  ciblés exécutés ; aucune configuration opérateur n’a été chargée.
- Contrôles documentaires : **94 guides** et **130 documents exportables**
  vérifiés ; contrôle ciblé des deux sources modifiées : **96 documents**,
  1 111 liens, aucune erreur ni avertissement.

Impacts : présentation dans `localeo-animation` et principes canoniques en
[section 5.2](perimetres-parcours-saas.md#52-lisibilité-actions-et-accessibilité-communes).
Aucun changement de règle métier, contrat API, données, droits, migration,
configuration ni générateur : commandes, versions et protections restent dans
les mêmes producteurs et appelants. Backend, Marketplace/Live et Pro ne
nécessitent pas d’adaptation. L’état de la roadmap reste inchangé.
Recette hébergée, essai avec utilisateurs et contrôle manuel par lecteur d’écran
restent à effectuer ; les preuves locales ne valent pas déploiement.

## Correctif du 1er novembre 2026 — audit Live pour un habitant peu familier du numérique

Audit expert sur le frontend Marketplace/Live de base `9cead02`, avec données
synthétiques locales et spécification canonique, sans essai impliquant de vrais
habitants. Le projet documentaire est sur `e2ba317` avec les travaux antérieurs
conservés, notamment l’harmonisation indépendante de Localeo Animation.

Les reproductions initiales échouent sur huit attentes observables : titre de
récupération incohérent avec son déclencheur, absence de reprise du détail
personnel en panne, retour public direct vers le carnet, recherche de commune
impossible à rejouer sans nouvelle saisie, faux bouton de choix communal,
programme vide présenté comme sélection absente, obligations peu explicites
dans le formulaire et refus sans focus. Les captures et traces avant correction
restent dans `localeo-marketplace/tmp/live-habitant-audit-before/`.

Les [principes et corrections](localeo-live-entree-unique.md#audit-dusage-du-1er-novembre-2026--habitant-peu-familier-du-numérique)
conservent l’univers graphique et les interactions existantes. Les reprises
utilisent les mêmes lectures, communes et accès personnels. Le retrait du carnet
devient secondaire dans l’erreur ; la récupération par e-mail se distingue de
l’inscription et guide la suite. Le formulaire annonce les quatre coordonnées
obligatoires et le consentement facultatif, focalise son erreur et nomme le
réessai avec le même corps et la même clé après résultat incertain.

Revue indépendante : identité exacte conservée lors du réessai, retours et
provenance maintenus, aucune inscription implicite ni nouveau consentement.
Le retour au champ e-mail après **Utiliser une autre adresse** a été ajouté à
la suite de cette revue. Les nouvelles recettes sont
`live-habitant-access.spec.cjs`, `live-habitant-communes.spec.cjs` et
`live-registration-clarity.spec.cjs` ; les assertions historiques suivent le
nouveau volet **Pas encore inscrit ?** et le libellé du réessai, en conservant
les exigences sur la saisie, les clés, les refus et l’absence de faux succès.

La relecture de la capture publique a aussi montré **Mes participations**
active avant inscription. Le repère de navigation rattache désormais fiche
publique et formulaire à **Accueil**, tout en conservant la rubrique des accès
personnels, anciens ajouts au carnet et lots. L’assertion du nouveau banc
contrôle la fiche, l’entrée en inscription et le détail personnel après reprise.

Impacts : frontend `localeo-marketplace` et documentation centrale uniquement.
Pas de règle métier, contrat, compte, donnée, migration, configuration DNS/TLS,
générateur ou nouveau fournisseur ; aucune génération réelle nécessaire.
L’installation anonyme et le rattachement existant d’un accès après lecture
réussie restent distincts d’une nouvelle inscription. Les tests contrôlent le
participant et le Bearer exacts de ce rattachement, sans l’assimiler à une
nouvelle commande de participation. Aucun changement backend, Pro ou Animation
pour ce correctif. L’état de l’epic et de la roadmap reste inchangé.

Vérifications :

- `npm run test:security` : **131 tests réussis**, aucun ignoré.
- Build de production isolé réussi via `scripts/serve-visual-tests.cjs`, sans
  lecture de fichiers opérateur ni réécriture des configurations publiques.
- ESLint réussi sur tous les fichiers JavaScript suivis et les trois nouveaux
  bancs. Le lanceur global `npm run lint` rencontre le même `EPERM` dans
  `output/bum-politique/pytest-approval-1` que lors de la précédente recette ;
  le contrôle par liste Git évite ce dossier de travail sans changer ses droits
  ni la configuration ESLint.
- La campagne navigateur porte sur les communes, le catalogue et ses erreurs,
  la fiche publique, les formulaires, la récupération et les inscriptions
  multiples, les QR personnels, les lots, la reprise de jeu et la surface
  Coffrets conservée. Les nouveaux bancs couvrent aussi quatre coordonnées
  requises, consentements, refus `422`, réponse `503` ou accès absent, réessai
  avec le même corps et la même clé, focus et texte agrandi à 200 %.
- **94 scénarios ciblés vérifiés** au total, sans additionner les rejeux :
  campagne de 85 cas avec 83 réussites et deux attentes de recette corrigées,
  puis **21 réussites** sur les fichiers rejoués et neuf cas complémentaires.
  Le scénario historique ouvre désormais le volet **Pas encore inscrit ?** ;
  l’autre attend le rattachement asynchrone existant avec son participant et son
  Bearer exacts, au lieu d’en vérifier la présence avant la fin de l’effet.
  Aucune assertion sur le corps, l’identité ou les mutations n’est retirée.
- Après le dernier ajustement de navigation, **15 scénarios rejoués avec
  succès** : récupération, reprise personnelle, fiche publique puis inscription,
  rubrique Lots sur les deux surfaces et accès mobile à l’action principale.
  Ce sont des cas déjà comptés dans les 94, pas 15 cas supplémentaires.
- Contrôles documentaires : **96 documents**, **1 089 liens**, aucune erreur
  ni avertissement ; **130 sources exportables** vérifiées.
- Captures avant/après relues dans `localeo-marketplace/tmp/`, hors
  versionnement. Aucun appel à un fournisseur ou environnement métier réel.

Cette recette locale ne remplace pas un essai avec des habitants peu familiers
du numérique, ni un contrôle manuel par lecteur d’écran et dans une PWA installée.
Aucun commit, push ou déploiement exécuté ; vérification hébergée à réaliser
après livraison. Les résultats de l’harmonisation de Localeo Animation restent
distincts de ce correctif Live.

## Simplification de Mes participations — 1er novembre 2026

Demande : supprimer la distinction technique **Mes accès liés** et réunir les
participations dans une liste compréhensible. Base Marketplace **6c5dd04** et
documentation **9c74a33**, avec corrections locales. La reproduction navigateur
échoue avant correction : trois inscriptions attendues dans la liste, seulement
les deux locales présentes ; la troisième se trouve dans le bloc séparé.

`LiveAnimations` présente désormais les deux sources dans **Mes animations**,
sans doublon par identifiant exact de participation et sans section technique
vide. **Retrouver mon inscription** reprend le formulaire e-mail existant pour
les entrées sans accès personnel. Les cartes gardent anneaux, pictogrammes et
actions adaptées ; les compteurs du carnet restent explicitement limités à
l'appareil. Deux inscriptions à la même animation conservent leurs propres
tokens, QR, e-mails et états. Le composant de section séparée et ses styles
devenus inutiles sont supprimés.

Une action commune **Actualiser mes participations** conserve la liaison
volontaire des anciens accès : lots de 50, deux requêtes simultanées au maximum,
échecs partiels visibles et aucun effacement du carnet. Aucun rattachement
implicite, nouvelle inscription, token ou consentement n'est créé. La pagination
remplace uniquement les résultats distants ; les entrées locales et les
commandes restent disponibles même après déduplication d'une page entière.
Une actualisation pendant une pagination peut annuler la lecture précédente ;
ni son succès ni son erreur tardifs ne doivent remplacer l'état courant.

Les états de chargement et d'erreur ne sont pas présentés comme une absence
d'inscription. Les contrats API et la persistance restent inchangés ; pas de
migration, de modification backend, de générateur ou de paramètre d'exploitation
nécessaire pour cette correction de présentation. Les autres applications
restent hors périmètre.

Preuves locales :

- **38 scénarios navigateur réussis**, aucun ignoré :
  `live-participations-unified.spec.cjs` (7 nouveaux),
  `live-participations-graphics.spec.cjs`, `live-carnet-readd.spec.cjs`,
  `live-home-accesses.spec.cjs`, `live-home.spec.cjs` et
  `live-habitant-access.spec.cjs`. Deux participations à la même animation,
  token absent, récupération e-mail, QR exact, lot de 50/concurrence 2/refus,
  pagination, réponses tardives, chargement/panne et vide confirmés.
- Le scénario historique de réajout attend désormais l'inscription distante
  présente dans sa fixture, au lieu de l'ancien écran vide trompeur. Les
  assertions de droits, e-mails, tokens, QR et conservation du carnet restent
  vérifiées. Les anciens tests de pagination utilisent les nouveaux libellés.
- **131 tests Node** et ESLint ciblé réussis. Build de production isolé par le
  serveur Playwright, sans lecture des `.env` ni réécriture de la configuration
  publique. Captures bureau/mobile et texte 200 % relues dans
  `localeo-marketplace/tmp/live-unified-final/`, hors versionnement.
- Documentation : **96 guides, 1 089 liens**, aucune erreur ni avertissement ;
  **130 sources exportables** vérifiées. `git diff --check` réussi.

Fixtures synthétiques uniquement ; aucun appel métier distant. Recette hébergée,
PWA installée et essai avec des habitants non exécutés. Pas de commit, push ou
déploiement exécuté pour ce correctif.

## 1er novembre 2026 — Onboarding commerçant Animation simplifié

Référence **E73-EVO-ONBOARDING-ANIMATION-SIMPLE**, critères **OA-01 à OA-04**
de la [spécification canonique](perimetres-parcours-saas.md). Évolution locale de
CA-16/17/18, remplaçant la convention Animation obligatoire, sans clôture d’E73.
Arbres de travail avec modifications antérieures conservées : projet `9c74a33`,
backend `ecfc9f1`, Pro `0c8499e`. Aucun commit, push ni déploiement pour ce lot.

| Critère | Résultat local et preuves |
| --- | --- |
| OA-01 | Création ERP/OnBoard avec Animation, Coffrets ou mixte, atomicité du commerce/dossier/produits/audit et rollback sur échec. Choix explicite réservé à `commercants:perimetres_gerer` et à sa portée communale, après relecture de l’autorité et avant rejeu. Omission/null et empreinte ERP historiques conservés. Tests `test_referencement_produits.py`, `test_referencement_produits_postgres.py`, navigateurs ERP/OnBoard. |
| OA-02 | Identité/adresse/contact et accès Pro testé conservés ; contrat, Stripe, prestations Coffrets, rendez-vous, pack et bilan non applicables à Animation seule. Finalisation réelle sans ces éléments, sans ouverture du produit ni email implicite : `test_onboarding_animation_simple.py`, `test_onboarding_produits_postgres.py`. |
| OA-03 | Convention Coffrets uniquement en mixte, validation actuelle puis preuve périmée ; exigences Coffrets restaurées lors de l’ajout. Fonctions souhaitées conservées au stockage puis filtrées dynamiquement. Tâches humaines à nouveau visibles après ce changement, avec statut et notes conservés. Tests domaine, PostgreSQL et navigateur `epic73-perimetres.cjs`. |
| OA-04 | Dossiers historiques sans produit explicite inchangés ; données et preuves acquises conservées. Préparation Pro/OnBoard, emails et PDF contextualisés. Communication Animation facultative, sans rendez-vous, aperçu distinct de l’accord. Ajout Coffrets ou changement de destinataire invalide le message avant envoi ; calendriers/rappels sans rendez-vous refusés. Tests communications, rendu, Pro et navigateurs. |

Le domaine `conformite_fiscale_bum` porte l’applicabilité ; `referencement` reste
propriétaire de l’ouverture du produit. Les règles d’habilitation, de version,
de suspension, de participation et d’envoi E68 demeurent applicables. Les
projections exposent `sections`, `conventionsRequises` et `exigences` ; la version
des preuves des produits explicites devient `PRODUITS_E73_V2`.

Réalisations par dépôt :

- **Backend** : règles, préparation/finalisation, commandes de création et garde
  de qualification, API, ERP/OnBoard, communication et support Animation.
- **Pro** : préparation courte guidée par la projection serveur ; aide secondaire,
  étapes utiles et absence des sections contractuelles/financières non applicables.
- **Projet** : décision, critères, contrats, recette F04, guides et exploitation.
  Les deux champs de création des instantanés OpenAPI E41/E42 sont alignés sur les
  modèles API par export hors ligne ciblé ; les autres opérations sont conservées.
- **Marketplace/Live et portail organisateur** : sans changement pour ce lot ;
  ils ne qualifient pas l’onboarding commerçant.

Preuves exécutées localement sur les modifications courantes :

- **881 tests backend isolés réussis**, aucun ignoré : architecture ; domaine
  onboarding/produits/préparation/communications ; orchestration ; contrats et
  permissions API ; référencement ; adresse ; démonstration préparation/adresse.
  Commande `scripts/validation/test_isolated.py`, Python 3.14, sans `.env`, réseau
  fournisseur ni base externe. Les contrôles de rendu/PDF ajoutent **6 succès**.
- **22 tests PostgreSQL réussis**, aucun ignoré, sur PostgreSQL 18.3 local jetable :
  10 créations/rollback, 4 onboarding/complément/preuve périmée, 5 communications
  concurrentes/crash/relecture et 3 imports sans ouverture implicite. Passage commun
  final après correction de l’applicabilité des tâches : **88,10 s**. Les 14
  avertissements concernent le tri des FK cycliques profils/versions de la fixture ;
  ils ne sont pas des tests ignorés. Aucune base d’exploitation utilisée.
- **39 tests Vitest Pro** et **8 scénarios E2E Pro réussis** : préparation,
  contrat et reprise après authentification ; Animation en 320/1280 px avec axe.
  Captures mobile/bureau relues dans `localeo-commercant/tmp/`, hors versionnement.
- Navigateurs backend réussis : `epic73-perimetres.cjs` (320/1280 px),
  `epic69-onboard.cjs`, `adresse-commercant-erp-onboard.cjs` (390/1280 px),
  **2 scénarios** `test_onboard_simple_browser.mjs` et **8 scénarios**
  `test_communications_simple_browser.mjs`, dont Animation facultatif à deux tailles.
  Le parcours E73 a été rejoué après le dernier ajustement de libellés partagés.

Les fixtures SQLite émulent fidèlement `jsonb_typeof` pour conserver le CHECK
du modèle. Les fixtures PostgreSQL de communications fournissent les vraies
tables de commune et de périmètres pour conserver les verrous ; les fixtures
navigateur chargent le véritable module de dates. Aucune contrainte, assertion
de refus ou garde métier n’a été supprimée pour obtenir ces succès.

Deux revues indépendantes ont relevé puis fait corriger la permission de
qualification initiale et les tâches restant masquées après ajout Coffrets.
Les refus d’habilitation et les deux statuts humains conservés disposent de
tests dédiés. Les compléments de revue sur l’aperçu Animation devenu obsolète
ont également été couverts avant confirmation et avant traitement.

Pas de migration, table, variable ou permission nouvelle. Le générateur garde
ses dossiers historiques non qualifiés et sa demande de revue ; il n’active pas
les produits. Les tests préparation/adresse de son adaptateur passent ; génération
complète, transfert/dump/restauration et fournisseurs réels non exécutés pour
cette évolution. Les données et moyens de contact des tests sont synthétiques.

La [configuration de livraison](../../exploitation/technique/configurer-epic-73.md)
précise l’ordre backend puis Pro et la nouvelle approbation du support Animation
si un envoi facultatif est utilisé. Un ancien aperçu/une ancienne empreinte ne
valident pas un contenu modifié. Recette hébergée et appareils PWA installés
non exécutés ; les scénarios de recette existants ne sont pas barrés à ce titre.

## Correctif Animation seule sans rendez-vous — 1er novembre 2026

**E73-ONBOARDING-SANS-RDV-20261101**, complément OA-02/OA-04 de la
[spécification](perimetres-parcours-saas.md). La règle de domaine permettait déjà
la finalisation sans rendez-vous, mais OnBoard/ERP exposaient encore des libellés
et une date historiques. La liste conservait aussi les anciennes prochaines
actions RDV et incluait Animation seule dans le filtre `NON_PLANIFIE`.
Bases locales backend `ecfc9f1` et projet `9c74a33`, avec les travaux antérieurs
conservés ; version hébergée non inspectée pour ce correctif.

La projection du domaine reste propriétaire de l’applicabilité. La liste expose
désormais `sections` et `produitsVises`, lus par lots bornés ; l’adaptateur SQL
applique les mêmes faits avant filtres, total et pagination. Les commandes de
préparation enregistrent la provenance de leur prochaine action dans le JSON
existant. Les lectures masquent un index RDV devenu inapplicable sans effacer
les données enregistrées ni recalculer toute la préparation pour chaque ligne.
OnBoard et la fiche ERP masquent la date inapplicable et présentent un ancien
`RDV_PLANIFIE` comme **En préparation**. Coffrets, mixte et produit non qualifié
gardent leur parcours existant. L’aide à la création ne demande plus de rendez-vous
par défaut.

Preuves locales exécutées :

- Reproductions initialement rouges : ancien RDV visible en fiche Animation et
  prochaine action « Fixer le rendez-vous » remontant dans la liste PostgreSQL.
- **5 nouveaux tests PostgreSQL réussis** dans
  `tests/security/test_onboarding_rendez_vous_animation_postgres.py` : cohérence
  liste/détail/filtres/pagination, conservation des suivis manuels divergents,
  provenance des commandes, comparaison SQL/domaine sur 33 combinaisons et absence
  d’écriture par lecture. Une page de 1 ou 8 dossiers utilise les mêmes 5 SELECT.
- **227 régressions réussies** sur domaine/application onboarding/préparation et
  preuves PostgreSQL existantes ; **623 contrôles d’architecture réussis**.
  Lanceur backend `scripts/validation/test_isolated.py`, PostgreSQL 18.3 local
  jetable, sans base d’exploitation ni fournisseur externe.
- Navigateurs réussis : `epic73-perimetres.cjs` (320/1280 px, ancien statut/date,
  contrôles détaillés et retour Coffrets), `epic69-onboard.cjs` (création et droits),
  `commercants-erp-ux.cjs` (16 scénarios 320/1280 px, axe et texte 200 %).

Limite historique explicite : sans provenance enregistrée, seule l’action
standard **Fixer le rendez-vous**, préparation active, responsable attendu et
échéance absente est attribuée à l’ancien index automatique. Une saisie manuelle
strictement identique est indiscernable ; les autres actions historiques ambiguës
sont conservées. Les commandes futures permettent cette attribution par leur
identifiant et les valeurs indexées. Aucune modification des dates, statuts ou
audits historiques n’est effectuée par consultation.

Dépôts modifiés pour ce correctif : **backend** et **projet**. Pro consomme déjà
les exigences qui masquent le RDV et ne nécessite pas de nouvelle modification ;
Marketplace et portail organisateur ne portent pas cet onboarding. Contrat de
liste enrichi de façon additive, sans nouveau schéma de stockage, variable,
permission ni migration. Générateur inchangé : ses dossiers non qualifiés restent
prudents ; les états synthétiques qualifiés/historiques sont couverts ci-dessus,
sans génération complète supplémentaire. Aucun email, réparation de données,
commit, push ni déploiement ; recette hébergée restant à exécuter après livraison.

## Dossier OnBoard : priorités et gestion secondaire — 1er novembre 2026

**E73-ONBOARD-DOSSIER-UX-20261101**, complément de présentation OA-02/OA-04,
sans changement de statut de l’epic. Bases backend `ecfc9f1` et projet `9c74a33`,
avec les travaux antérieurs conservés. Les rubriques non applicables étaient
déjà retirées pour Animation seule, mais l’en-tête présentait activation, ouverture
des produits, récapitulatif et finalisation au même niveau ; la préparation courte
répétait ses raccourcis et sa vérification.

Le dossier indique maintenant son périmètre et présente les points à compléter
avant les opérations secondaires. Un raccourci ouvre la bonne rubrique et place
le focus sur son titre. Animation seule garde coordonnées, accès Pro et action
de finalisation autorisée par le statut serveur, sans contrat, Stripe, prestations
ou rendez-vous. Questions et réserves précèdent les communications facultatives ;
l’avancement de préparation est dépliable. Les onglets illustrés gardent leurs
noms, les flèches/Home/End et leurs relations ARIA, sans défilement horizontal.

**Gestion du dossier** regroupe les réglages de fonctions, le lien vers les
périmètres ERP, le récapitulatif et la réouverture motivée. La rubrique est repliée
par défaut et accessible depuis un raccourci discret d’en-tête. Une activation
de commerçant autorisée reste disponible, y compris sur dossier clos, sans
confondre activation du compte et ouverture du produit. Les dossiers terminaux
sans complément ne relancent pas les anciennes étapes et n’affichent pas de fausse
conformité ; leurs contrôles restent consultables. Le complément produit garde
ses autorisations sans réouverture du dossier historique.

Les commandes de vérification, validation, clôture et réouverture refusent de
remplacer une saisie non enregistrée. Aucun contrat serveur, refus d’habilitation,
statut ou contrôle de version n’est modifié. Le CSS est corrigé dans ses règles
existantes : anciennes présentations retirées, largeur disponible utilisée et
onglets lisibles sur deux colonnes mobiles.

Preuves locales exécutées :

- **20 nouveaux scénarios navigateur réussis**, `node
  tests/browser/onboard-dossier-ux.cjs`, 320/1280 px : périmètres Animation,
  Coffrets, mixte et non qualifié ; priorités ; gestion secondaire ; focus et
  clavier ; cycle vérifier/valider/terminer ; activation avec version/clé/CSRF ;
  refus dirty et conflit conservant les saisies ; terminaux, compléments et
  consultation seule. Axe sans violation sur les surfaces auditées ; texte 200 %
  sans débordement. Reproduction initiale rouge sur l’absence de gestion séparée.
- Régressions réussies : `epic69-onboard.cjs` (droits, scope et purge de session),
  `epic73-perimetres.cjs` (Animation/mixte, complément et conflits à 320/1280 px),
  `adresse-commercant-erp-onboard.cjs` (création/édition à 390/1280 px),
  `test_onboard_simple_browser.mjs` (**2 parcours**) et
  `test_preparation_browser.mjs` (**5 parcours** versionnés/permissions/réponses
  tardives et communications). Les fixtures de préparation chargent maintenant
  le vrai module partagé de dates, requis lors du retour d’un rendez-vous ; le
  libellé d’aide de création attendu est aligné sur sa contextualisation précédente.
- Captures mobile/bureau examinées dans `localeo-backend/tmp/onboard-dossier-ux/`,
  hors versionnement. La revue indépendante a fait corriger puis couvrir la
  fausse conformité terminale et l’activation précédemment retirée à ces dossiers.

Impacts : backend (présentation OnBoard et tests) et projet (guide et suivi).
Pas de changement Python, API, migration, permissions, données ou configuration ;
pas de nouveau contrôle métier dans l’interface. Le générateur et les autres
applications ne consomment pas cette présentation : aucun changement nécessaire.
Les règles de domaine restent couvertes par le lot précédent, sans nouvelle
exécution complète de sa suite pour ce correctif visuel. Aucun service réel,
email, commit, push ou déploiement ; vérification hébergée, PWA installée et
lecteur d’écran manuel non exécutés.

## Menus Pro adaptés à Animation seule — 1er novembre 2026

**E73-PRO-MENUS-ANIMATION-20261101**, correctif E73-CA-19. Bases backend
`4f0cfdc`, Pro `23c754a`, projet `f0b735e`, avec les travaux locaux précédents
préservés. Cause reproduite : `PerimetresCommercant.capacites` ouvrait les deux
produits avant la bascule communale, y compris après une qualification explicite
Animation seule. Pro filtrait déjà ses menus et ses liens directs par ces
capacités ; un correctif uniquement visuel aurait conservé une projection fausse.

Le domaine distingue maintenant la projection Pro des gardes d’autorisation.
`projection_pro_dans_uow`, utilisée par la connexion et la validation de session,
demande les capacités de présentation : produits actifs pour un commerce revu,
préparation et continuité conservées. Un commerce non revu en zone non basculée
garde sa présentation historique. Une simple demande `A_PREPARER` n’affiche pas
les fonctions opérationnelles d’un produit actif. Aucun choix ou activation de
produit n’est calculé dans le navigateur.

Animation seule ne présente plus Prestations, Reversements, Facturation, le
tableau de bord financier ou Mon contrat. Scanner, Animations, fiche publique,
compte, historique, notifications et aide restent soumis aux capacités courantes.
Le PIN Animation et les accès salariés restent disponibles lorsqu’ils sont
autorisés. Les deux produits actifs conservent leurs rubriques ; une ancienne
activité Coffrets retirée garde les consultations et engagements protégés
prévus. Les routes Coffrets absentes des capacités sont refusées dans Pro avant
chargement des données financières.

La revue indépendante a détecté que `capacites` servait aussi de garde PIN et
de filtre des notifications générales. Le paramètre `projection_pro=False`
conserve exactement leur comportement précédent ; seul le producteur de session
demande `True`. Un cas de régression vérifie la revue sans aucun produit encore
actif : préparation seule dans Pro, autorisation PIN et notifications historiques
conservées avant bascule. Ni `autoriser`, ni `filtre_lecture`, ni les décisions
de bascule ne changent. La revue finale ne relève pas de défaut concret restant.

Preuves locales exécutées, sans skip :

- Reproduction initiale : **5 échecs et 14 réussites**, domaine et projection
  de session ; échecs sur l’exposition Coffrets avant bascule, pas sur une
  indisponibilité d’environnement.
- Backend : **653 tests réussis**, dont 623 contrôles d’architecture/couverture,
  26 tests domaine/projection et 4 tests API. Commande :
  `python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/domain/referencement/test_perimetres_commercant_dedicated.py tests/application/referencement/test_projection_pro_perimetres.py tests/api/test_perimetres_commercants_api.py -q --tb=short --basetemp=.artifacts/pytest-pro-animation-navigation-final`.
  Matrice Animation/Coffrets/mixte, avant/après bascule, principal/salarié,
  préparation additive, non-revu et retrait avec continuité. Aucun PostgreSQL
  ni fournisseur réel requis par cette correction de calcul/projection.
- Pro : **37 tests Vitest réussis** :
  `npm test -- src/app/merchantNavigation.test.js src/features/perimetres src/app/MobileNavigation.test.jsx src/app/MerchantSessionHeader.test.jsx src/features/session/api.test.js`.
- Pro navigateur : **18 scénarios réussis**,
  `npm run test:e2e -- tests/e2e/perimetres.spec.js --workers=1 --output=tmp/pro-animation-navigation`.
  Animation seule avant/après bascule à 320/1280 px, menus desktop/mobile,
  compte sans contrat, PIN disponible, refus des liens directs sans appel
  financier, préparation additive, mixte, salarié, erreur de vérification et
  continuité financière. API/caméra simulées ; captures des deux formats
  contrôlées dans `localeo-commercant/tmp/e73-animation-*-false.png`.
  Le build navigateur est isolé des fichiers `.env` opérateur ; l’avertissement
  d’import statique/dynamique de l’historique reste visible, sans empêcher le test.

Impacts : backend (règle de projection et orchestration), tests Pro et
documentation canonique. Le code de présentation Pro consomme déjà correctement
les décisions serveur. La structure des DTO et contrats OpenAPI reste identique ;
seule la présence des codes de capacités est corrigée. Pas de nouvelle migration,
permission, variable ou changement de données. Le générateur prépare des racines
non revues et ne sérialise pas ces capacités : aucun changement nécessaire,
ni génération complète revendiquée. Marketplace et portail organisateur
Animation ne consomment pas cette projection commerçante.

Livraison : déployer le backend corrigé ; après rechargement ou navigation,
la revalidation de session actualise les menus sans imposer de nouvelle connexion
ni de bascule communale. Vérifier sur la cible le périmètre explicitement revu,
les menus et les liens directs. Aucune réparation distante, migration, invitation,
activation, commit, push ou déploiement effectué pendant ce correctif.

Contrôles documentaires réussis : `check_guidance.py` (94 guides, 1 054 liens),
`check_guidance.py --changed --all-markdown` (10 documents, 179 liens),
`sync_documentation.py --check-sources` (132 sources) et `git diff --check`
dans les trois dépôts concernés. Aucun état d’epic ni compteur de roadmap modifié.

## Guide Assistant et publication des chasses — 1er novembre 2026

**E73-UX-GUIDE-PUBLICATION**, correction du parcours organisateur, en priorité
Chasse au trésor. Bases Animation `04dc06c` et projet `a1f8201`, puis modifications
locales. La présentation cumulait la barre Action suivante, les alertes avec
leurs propres boutons, les tâches, deux navigations de préparation et les actions
de formulaire. Les états backend étaient préservés mais leur hiérarchie rendait
la prochaine action difficile à identifier.

L’Assistant affiche maintenant une étape développée avec sa consigne, son
intervenant et un seul appel principal provenant du serveur. Les autres étapes,
les éléments acquis, l’aide et le support restent accessibles à la demande.
Le premier point d’attention est visible, les suivants sont repliés ; leurs
messages complets et leurs contextes restent disponibles. Un diagnostic partagé
ne supprime plus la prochaine action. Les animations sorties de préparation
ouvrent leur suivi, sans revenir au formulaire de publication.

La Configuration Chasse conserve un guide **Parcours → Organisation et lots →
Commerces → Terrain → Publication**, avec état courant et validations serveur.
Sur ordinateur les étapes sont regroupées dans un rail ; sur mobile elles
restent compactes, nommées pour les technologies d’assistance, sans défilement
horizontal. Une seule étape occupe la zone de travail. Les contrôles détaillés,
options de continuité et nouvelle génération d’un parcours existant se déplient
au besoin ; la validation du parcours reste l’action principale.

Organisation et lots propose quatre écrans successifs. Les rubriques ne forment
plus une seconde barre permanente. Présentation et Calendrier permettent de
continuer sans écriture ; le Règlement demande l’enregistrement complet des
paramètres avant les Lots. Les réglages facultatifs sont secondaires. Une
confirmation serveur ou la relecture du reçu permet la continuation ; un timeout
ne devient jamais un succès. La dotation conserve sa commande distincte. Le
raccourci Commerces reste absent avant les Lots et bloqué par un brouillon.

Les liens de l’Assistant ouvrent directement le calendrier, le règlement, les
lots, le parcours, les commerces ou la publication. Les retours de paiement
restent distincts. Le contrôle final privilégie la synthèse et la confirmation
explicite ; les refus et avertissements détaillés se déplient. Un brouillon
explique son blocage sans le présenter comme un défaut d’habilitation.
Annulation et clôture gardent leurs confirmations dans les actions secondaires.

Preuves locales, avec API et données synthétiques :

| Contrôle exécuté | Résultat / portée |
| --- | --- |
| `node --test tests/assistant-presentation.test.mjs` | Reproduction utile : 8 réussites et 1 échec sur une prochaine action supprimée par la déduplication ; après correction, 9 réussites. Aucun état ou action serveur réécrit. |
| `node --test tests/preparation-workflow.test.mjs` puis avec `tests/assistant-navigation.test.mjs` | Reproduction : 3 réussites/1 échec, un lien Commerces revenait au Parcours ; les 7 tests de navigation passent après correction. Un défaut de comparaison entre contextes VM des nouveaux tests est corrigé dans le montage, sans modifier les destinations attendues. |
| `pnpm test` | 294 tests Node réussis, aucun skip ; contrats consommés, règles de présentation, idempotence et reprise. |
| `node tests/browser/assistant-guidance-ux.mjs` | 48 scénarios réussis : attentes, prêt avec/sans action serveur, alertes partagées, erreurs, statuts publiés/terminaux, clavier et absence de mutation ; 1600/390/320 px et texte 200 %. |
| `node tests/browser/hunt-parameters-guidance.mjs` | 268 contrôles réussis : une rubrique visible, navigation sans écriture, champ invalide masqué/replié retrouvé, PUT complet, version/clé, réponse perdue et reçu sans nouvel envoi, droits, blocages et dotation ; 1280/390/320 px et texte 200 %. |
| `node tests/browser/hunt-preparation.mjs` | 288 contrôles réussis : parcours intégré, financement, commerces, terrain, confirmations, publication, idempotence, reçus et saisies. Les anciennes assertions de structure ont été adaptées aux menus secondaires et au nouveau CTA Assistant, sans retirer les assertions métier. |
| `node tests/browser/hunt-guided-workflow.mjs` | 3 parcours et 87 contrôles réussis après les derniers ajustements : états serveur, validations absentes/périmées retirées, brouillons conservés entre étapes, publication bloquée par la saisie, aucune écriture implicite ; 1280/390/320 px, texte 200 %. |
| `node tests/browser/animation-workspace-ux.mjs` | 40 parcours réussis : largeur, alignement, priorités, unicité du CTA Assistant, barre générique conservée dans les autres rubriques et absence de mutation. |
| Même banc avec `WORKSPACE_CASE=navigation` | 8 parcours réussis : groupes, liens directs, alias, rechargement, focus, droits, sortie avec saisie, contenu différé et destination du suivi après publication. |

Les deux premiers passages des bancs Chasse intégrés échouaient sur les anciens
accès directs à des actions désormais repliées ; les scénarios passent par les
contrôles visibles du nouveau parcours et conservent leurs assertions de
validation, versions, clés et effets. Le banc guidé est renouvelé après repli
de la génération secondaire et clarification du message de brouillon.

`node scripts/build-generation-tests.mjs` construit l’application complète avec
configuration synthétique et fichiers `.env` désactivés. Le build PWA production
isolé `node scripts/build-pwa-tests.mjs` réussit également, avec service worker
généré. Ces builds ne contactent pas une API métier et ne publient aucun site.
Captures bureau/mobile/texte 200 % inspectées dans les répertoires temporaires
Assistant, paramètres, guide Chasse et workspace ; aucun média fictif ajouté.

La revue indépendante ne relève pas de contournement : changements d’étape
bloqués pendant une commande, brouillons conservés, publication conditionnée
par ses droits et ses validations, réponses anciennes ignorées. L’interface
choisit une destination ou une présentation ; elle ne remplace aucune décision
de domaine. Le service de préparation, l’assistance Localeo et la vérification
terrain restent distincts et leurs attentes ne sont pas maquillées en validation.

Impacts : **Animation et documentation projet**. Les composants et feuilles
existants sont corrigés à leur source ; une feuille dédiée remplace le rendu
inline de Publication. Aucun changement de contrat API, backend, permission,
règle métier, migration, configuration, stockage ou générateur. Les autres
applications n’utilisent pas ces composants. Pas de test PostgreSQL requis par
ce périmètre de présentation. Aucun compte réel, message, paiement, publication,
commit, push ou déploiement effectué ; la recette hébergée, PWA installée et
lecteur d’écran manuel restent non exécutés. Le statut de l’epic reste inchangé.

Contrôles finaux : `pnpm typecheck` et `pnpm lint` réussis ; `pnpm test`
renouvelé après les derniers changements, **294 réussites, zéro échec et zéro
skip**. `check_guidance.py` réussit (94 guides, 1 054 liens),
`check_guidance.py --changed --all-markdown` réussit (3 documents, 104 liens),
`sync_documentation.py --check-sources` vérifie 132 sources. `git diff --check`
réussit dans Animation et projet. Aucun artefact temporaire n’est versionné.

## Contre-revue du nouvel Assistant — 1er novembre 2026

Suite à la demande de challenger **E73-UX-GUIDE-PUBLICATION**, revue de l’arbre
local Animation (base `04dc06c` avec la refonte non commitée), du producteur
`assistant_animation.py` et de parcours synthétiques représentatifs. La revue
porte sur le guidage du gestionnaire et la reprise de tâche, sans modifier les
règles de publication ni l’état de la roadmap.

Défauts démontrés et corrigés :

- Avec un seul contrôle restant, consulter un contrôle acquis faisait perdre
  l’accès direct à la prochaine action. **Reprendre la prochaine action** ramène
  maintenant au contrôle recommandé, sans appel API ni commande.
- Un contrôle acquis affichait **À faire maintenant**, une consigne de travail
  ou une attente faute d’action. Il devient **Point déjà vérifié** ; son accès
  aux informations reste secondaire. Cela concerne aussi une animation publiée,
  dont le producteur conserve réellement Identité et Commune acquises.
- **Identité de l’animation** contrôle le nom de l’animation, alors que le front
  décrivait les accès de l’équipe et ouvrait `/compte`. Le texte est corrigé et
  le code du contrôle accompagne l’action serveur dans le callback local :
  Identité ouvre la configuration, directement Présentation pour une chasse en
  préparation. Le même code d’action pour Préparation des modèles manuels ouvre
  leur configuration. Les autres usages de l’action gardent leur destination.
- Les neuf contrôles étaient présentés comme des étapes, en concurrence avec
  les cinq étapes du guide Chasse. Le compteur distingue désormais les
  **contrôles**. Le sélecteur est replié après l’action principale et la sélection
  déplace le focus sur le titre du point consulté. Les attentes sans action
  sont explicitement titrées **En attente d’une intervention**.

Reproductions avant correction : le nouveau banc navigateur échoue sur
l’absence du bouton de reprise ; le test de destination Identité échoue sur
`/compte` au lieu de la présentation. Les assertions passent après correction.
La revue indépendante confirme la conservation des décisions/actions serveur
et l’absence de mutation implicite. Les sélecteurs des recettes existantes
suivent le nouveau contrôle replié, sans retirer les assertions métier.

Contrôles exécutés : **13 tests unitaires** Assistant/destinations, **48 scénarios
navigateur** Assistant, **12 scénarios de contre-revue** et **40 parcours intégrés**
workspace réussis ;
`pnpm typecheck`, `pnpm lint`, build complet isolé
`node scripts/build-generation-tests.mjs` et `git diff --check` réussis.
Les API sont synthétiques, les fichiers opérateur `.env` sont désactivés et
aucun réseau métier réel n’est utilisé. Captures bureau/mobile/texte 200 %
inspectées ; pas de débordement horizontal constaté.

Le banc `assistant-resume-ux.mjs` couvre 1600/390/320 pixels (texte à 200 % sur
320), avec libellés réels, Identité manquante, une ou plusieurs actions restantes
et état publié. Il vérifie aussi le code du contrôle transmis par le callback
depuis l’action principale ou secondaire. Les 48 scénarios et les 4 parcours
intégrés Assistant sont renouvelés après harmonisation finale des libellés
« contrôles ». Les contrôles documentaires réussissent : 94 guides/1 054 liens,
3 documents modifiés/104 liens et 132 sources exportées vérifiées.

Impacts : **Animation et documentation projet**. Le contexte additionnel est
interne au callback React ; aucun changement du contrat API, du backend, des
permissions, des données, des migrations, du générateur ou de la configuration
d’exploitation. Les règles serveur et confirmations restent propriétaires.
Tests utilisateurs avec gestionnaires réels, recette distante et lecteur
d’écran manuel non exécutés. Aucun commit, push ni déploiement dans ce correctif.

## E73-PRO-SCAN-ANIMATION — ouverture du périmètre sur TEST, 1er novembre 2026

Signalement : « Commercant Thibaut Animation Seul » ne voit pas le scanner QR
dans Localeo Pro. Diagnostic ciblé sur TEST : commerce globalement `ACTIF`,
revue `VALIDEE`, mais produit `ANIMATION=A_PREPARER` (version 2),
`COFFRETS=NON_DEMANDE`. Le seul prérequis Animation manquant est
`PORTAL_ACCESS_READY` : test d’accès Pro non confirmé dans OnBoard. La
projection Pro retire intentionnellement le scanner lorsque le produit revu
n’est pas actif ; le menu et l’accueil savent déjà présenter le scanner pour
Animation seule. L’activation globale et l’ouverture du produit sont distinctes.

Après confirmation explicite de la connexion réussie par le demandeur :

- Confirmation via `POST /internal/onboard/api/dossiers/{id}/acces/test-confirme`
  (HTTP 200), avec l’audit métier existant.
- Relecture des prérequis Animation : valides, aucun manquant.
- Activation via `POST /internal/referencement/commercants/{id}/perimetres/ANIMATION/activer`
  (HTTP 200), version attendue, motif et clé d’idempotence.
- Relecture HTTP et PostgreSQL en lecture seule : `ANIMATION=ACTIF`, version 3,
  preuve de validation et activation au **2026-11-01 17:24:34 UTC** ; Coffrets
  reste non demandé et la bascule communale reste inchangée.

Preuves locales : **41 tests backend réussis** sur le domaine des périmètres,
la projection Pro et l’accès de préparation. Les **4 scénarios Playwright** de
`tests/e2e/perimetres.spec.js` « Animation seule » passent, à 320 et 1280 pixels,
avec et sans bascule communale. Assertions renforcées : scanner dans l’accueil,
la navigation et la barre mobile, ouverture effective de `/validation`, absence
de commande métier à l’ouverture, refus des liens Coffrets conservés. Les API de
ces scénarios navigateur sont simulées ; ils ne prouvent pas un scan caméra réel
avec la session du commerçant sur TEST. Une reconnexion Pro renouvelle les
capacités et les droits d’une ancienne session de préparation.

Impacts : tests **Commerçant**, suivi **Projet** et configuration métier de ce
seul commerce **TEST**. Aucun changement de code applicatif, de règle métier,
de contrat, de migration, de générateur ou d’offre ; aucun déploiement nécessaire.
Les scripts et le résultat opérateur restent dans `localeo-backend/tmp/`, ignoré
par Git, sans identifiants de connexion dans le rapport. Aucun commit ni push
effectué dans cette intervention.

## E73-UX-DEFILEMENT — un seul défilement du contenu Animation, 1er novembre 2026

Demande clarifiée : supprimer le défilement extérieur ou imbriqué, en conservant
l’accès à tout le contenu. Sur la base Animation `9b0eb7a`, le scénario navigateur
échoue avant correction sur la zone défilante propre à la liste. La fiche et la
création possèdent également des conteneurs défilants internes. Sur mobile, les
libellés invisibles des fiches peuvent en outre agrandir le document faute de
contenant positionné dans la zone de contenu.

Correction à la source : `#app-main` porte le défilement vertical et contient
les éléments positionnés ; liste, fiche, création et détails de préparation
suivent le flux. Les anciennes exceptions CSS mobiles sont retirées. Le chargement
progressif écoute le défilement principal et conserve son bouton manuel. Les
boutons de création restent accessibles en bas et le changement d’étape revient
au début. La barre Action suivante reste fixe sur écran d’au moins 800 px de
hauteur ; en dessous, elle suit le contenu afin de ne pas le recouvrir au zoom.
Les fenêtres et menus superposés restent défilants lorsque nécessaire.

Preuves : scénario avant/après avec 35 animations, accès clavier au dernier
élément, navigation vers l’action suivante et création sur huit formats de
320 à 1600 px, dont texte à 200 %. Recettes complémentaires du cadre partagé,
des rubriques, de la création Léo et des détails de préparation. Les captures
restent dans les répertoires temporaires du dépôt Animation ; les API sont
simulées, sans configuration opérateur ni appel métier distant.

Résultats : **8 parcours défilement**, **8 parcours cadre partagé**, **40 parcours
rubriques**, recette Léo à **390/1280 px** et **114 contrôles de préparation**
réussis. Les **295 tests unitaires**, TypeScript, ESLint et le build isolé
`scripts/build-generation-tests.mjs` passent. Captures bureau et mobile à 200 %
inspectées. Contrôles documentaires : 2 guides/77 liens et 132 sources exportées
vérifiés ; `git diff --check` réussit dans les deux dépôts.

Impacts : **Animation et documentation Projet**, présentation uniquement.
Aucun changement de contrat API, permission, règle métier, données, migration
ou générateur. Les contrôles ne prouvent pas le rendu sur TEST ou sur une PWA
installée. Aucun commit, push ou déploiement demandé dans cette intervention.

## E73-UX-GESTION — ergonomie commune Pro et Animation, 1er novembre 2026

Audit demandé des deux applications de gestion, sur PC et mobile. Les constats,
corrections et preuves sont centralisés dans le
[rapport d’ergonomie Pro et Animation](../../audits/ergonomie-gestion-pro-animation-2026-11-01.md).
Les bases testées sont Pro `6c7489e` et Animation `9b0eb7a`, avec les changements
locaux conservés. La roadmap et les critères de clôture restent inchangés.

Corrections : navigation clavier et mobile au zoom, accès au menu Compte en
paysage, reprise explicite des lectures en erreur, confirmations salariés
contextualisées, fenêtres Animation avec confinement et restitution du focus,
commandes nommées, filtres accessibles et alertes lisibles. L’abandon du motif
de refus d’un retrait commerçant n’envoie désormais aucune décision.

Les tests utilisent des API synthétiques ; ils vérifient également l’absence
d’écriture après abandon, les traitements en cours et les droits conservés.
Les captures PC, mobile et texte agrandi ont été inspectées. Les résultats
détaillés et les contrôles non exécutés figurent dans le rapport commun.

Impacts : **Commerçant, Animation et documentation Projet**. Les règles métier
et les contrats restent au backend ; aucune migration, configuration opérateur
ou modification du générateur n’est nécessaire. Aucun déploiement ni essai sur
appareil physique n’est inclus ; les travaux restent locaux.
