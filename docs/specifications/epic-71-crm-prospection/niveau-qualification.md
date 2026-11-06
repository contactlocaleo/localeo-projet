# E71-EVOL-06 — Niveau de qualification et priorité de prospection

Cadrage du **5 novembre 2026**, rattaché à l’[epic 71](README.md) et à ses
[critères stables](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md).
État produit conservé : **En cours**. Cette extension est **à spécifier puis à
implémenter** ; les propositions de barème ci-dessous ne sont pas des règles livrées.

## 1. Demande et décision acquise

Ajouter une entrée **Qualification** dans le menu CRM : rechercher des prospects,
calculer leur niveau sur l’ensemble du résultat et identifier ceux à traiter en
priorité. Afficher les niveaux et leurs filtres dans les listes et sur la carte.

L’utilisateur choisit explicitement le 5 novembre : **priorité commerciale
combinant fiabilité, potentiel et maturité du projet**, plutôt qu’un simple taux
de remplissage de la fiche. Le niveau ne se limite donc pas à la qualité des six
blocs de qualification. Les pondérations, seuils et durées proposés ne sont pas
encore arbitrés. Aucun compte ou rôle supplémentaire n’est demandé.

L’[actualisation E71-EVOL-05](actualisation-qualification.md) recherche des faits
récents dans des sources externes ; E71-EVOL-06 utilise les faits **déjà adoptés**
pour aider à la décision commerciale. Calculer n’enrichit ni ne vérifie les
informations et ne lance pas implicitement l’actualisation externe.

## 2. Existant vérifié et responsabilités

Le domaine Prospection possède déjà le classement territorial
`SEUILS_ANIMATION_1`, les évaluations sourcées et références indépendantes, les
contacts vérifiés et la qualification des projets Animation. Le dossier commercial
possède sa priorité manuelle `NORMALE`/`HAUTE` et son étape. **Aucun score composite
de qualification commerciale n’existe actuellement.**

Repères backend examinés : `app/domaine/prospection/qualification.py`,
`app/domaine/prospection/regles.py`, `app/api/prospection_qualification_filtres.py`,
`app/infrastructure/persistence/prospection_filtres.py`,
`app/infrastructure/persistence/prospection_core.py`,
`app/infrastructure/pwa/crm/crm.js` et `app/security/crm.py`.

Le classement territorial actuel mesure un nombre de commerces ; il n’est ni une
probabilité d’achat ni le nouveau niveau. La carte actuelle agrège tous les types
de prospects par INSEE de localisation, avec une couleur unique et au plus 500
groupes. Elle ne représente pas leur couverture commerciale.

Le futur service de domaine Prospection possède le barème pur et versionné, les
motifs et l’admissibilité des faits. L’application capture la sélection, orchestre
les commandes et la reprise ; les adaptateurs portent persistance, ordonnanceur
et lectures projetées ; la PWA affiche les résultats sans recalcul local des règles.

## 3. Parcours Qualification

1. **Rechercher** : réutiliser les filtres serveur des Prospects (texte, type,
   département, potentiel, contacts, etc.) et ajouter niveau, état du calcul et
   objectif commercial. Conserver les filtres dans l’URL et les retours de fiche.
2. **Préparer le calcul** : afficher le nombre total, l’objectif/profil, la version
   de règle et la date de sélection. **Tous les résultats**, pas seulement la page
   visible, sont visés. Une sélection explicite d’IDs est possible comme variante
   bornée ; aucun « tout sélectionner » ambigu avec les 25 lignes de la page.
3. **Lancer le calcul** : action explicite « Calculer sur les X prospects », refus
   clair si zéro résultat ou profil non disponible. Un aperçu n’écrit aucun score.
4. **Suivre** : progression persistante (en attente, en cours, terminé,
   partiellement terminé, interrompu ou échec), compteurs et bilan paginé.
   Quitter la page n’annule pas le travail ; un double clic retrouve le même lot.
5. **Décider** : liste triable par niveau/score, avec potentiel, maturité, fiabilité,
   qualité des données et motifs courts. « Pourquoi ce niveau ? » montre les faits
   retenus et les actions manquantes, avec liens vers les bons champs ou dossiers.

Lancement confirmé = périmètre figé, règle et autorité identifiées. Une saisie
postérieure qui ferait entrer un nouveau prospect dans la recherche ne l’ajoute
pas au lot. Les données changées depuis la préparation sont signalées en conflit,
pas calculées silencieusement avec une autre base. Le recalcul de résultats dont
le niveau fait lui-même partie des filtres ne doit ni déplacer le curseur du lot
ni en faire disparaître les unités restantes.

## 4. Modèle de calcul proposé, à valider

### Trois axes explicables

| Axe | Poids proposé | Exemples de faits admissibles et limites |
| --- | --- | --- |
| Potentiel | 40 points | Comptage et classement de référence pour commune/EPCI, portée et méthode cohérentes ; volume commercial propre à l’objectif pour les autres profils. Une grande population seule ne prouve pas le potentiel. |
| Maturité du projet | 35 points | Besoin confirmé, porteur effectif, calendrier exploitable et budget documenté ; étape du même dossier en complément. Un libellé d’étape, une note ou un accord verbal ne valent pas ces preuves. |
| Fiabilité des informations | 25 points | Identité/territoire cohérents, provenance datée, coordonnées et interlocuteur vérifiés dans leur version actuelle ; fraîcheur distincte de la date du dernier import ou clic. |

Recommandation de restitution : score sur 100, détail des points par axe, niveau
et couverture des données. Ce score **n’est pas une probabilité de conversion**.
Ne pas multiplier les points pour plusieurs contacts similaires ou plusieurs
observations du même fait. Ne pas récompenser la longueur des notes.

Pour un premier profil **Animation — collectivités**, les seuils existants de
comptage peuvent informer l’axe potentiel ; commune et EPCI restent deux portées
distinctes. La répartition exacte des points à l’intérieur des axes, les preuves
minimales, les seuils propres à l’objectif et la durée de validité de chaque fait
doivent être établis avant implémentation du profil. Pas de classement fourni
sans ces règles : les chiffres 40/35/25 sont une **proposition**, pas un arbitrage.

### Niveaux et états recommandés

| Restitution proposée | Sens | Repère graphique |
| --- | --- | --- |
| Non calculé | Aucun résultat pour l’objectif et la règle choisis | Gris, tiret |
| À explorer | Données suffisamment évaluées, score inférieur à 40 | Orange, boussole |
| À qualifier | Données suffisamment évaluées, score de 40 à 69 | Bleu, progression |
| Prioritaire | Score d’au moins 70, avec conditions de fiabilité satisfaites | Vert, étoile |
| Données insuffisantes | La couverture ne permet pas de conclure | Contour pointillé, point d’interrogation |
| À recalculer | Résultat historique dont les faits/règle/validité ont changé | Horloge et ancien niveau explicitement historique |

Les couleurs doivent respecter la charte et le contraste ; libellé, pictogramme
et légende restent disponibles. **Erreur de calcul** est un état technique du
lot/unité ; elle n’est pas un niveau faible et n’efface pas un résultat précédent.

Valeur inconnue, preuve absente, non-applicabilité et fait négatif démontré sont
distincts. Ne pas attribuer zéro définitif au potentiel ou à la maturité faute
de données : exposer les points acquis, les points non évaluables et la couverture.
Une proposition est d’exiger **80 % de couverture**, un interlocuteur vérifié et
un potentiel exploitable pour afficher « Prioritaire » ; ces seuils restent à
arbitrer. Sans dossier, maturité inconnue : **aucun dossier créé automatiquement**.

### Objectifs et dossiers multiples

Chaque résultat est lié à `(prospect, objectif commercial, profil, version de règle,
dossier éventuel)` ; la synthèse est une projection des résultats admissibles.
La recherche choisit parmi les objectifs existants : Animation/souscription,
Coffrets/partenariat commerçant ou Coffrets/achat entreprise-CSE. Le profil dépend
ensuite du type réel ; le potentiel d’une commune n’est pas celui d’un établissement.
Un éventuel profil de commerce participant à une animation reste **futur et non
disponible**, à cadrer séparément : ce besoin n’ajoute pas implicitement un nouvel
objectif au domaine ou au CSV actuel.
Les premiers profils effectivement livrables doivent être annoncés ; les autres
sont « Profil non disponible », jamais calculés avec le barème collectivité.

S’il existe plusieurs projets admissibles, calculer chaque projet séparément et
présenter comme synthèse le meilleur résultat **d’un même dossier actif**,
identifié à l’écran, avec départage déterministe. Ne pas prendre le porteur d’un
dossier, le budget d’un autre et la date d’un troisième. Les critères de recherche
portant sur le dossier doivent tous porter sur ce même dossier ; la synthèse
ne choisit pas un dossier hors de la sélection. Projets gagnés, perdus ou clos
restent historiques et ne créent pas une nouvelle priorité de prospection.
L’ordre exact de départage et les étapes admissibles restent à spécifier par profil.

Le lot fige les prospects et leurs dossiers admissibles pour l’objectif. Les
résultats par dossier sont conservés séparément ; les filtres de lecture choisissent
ensuite les candidats admissibles, sans écraser une synthèse générale avec un score
propre à une recherche. Une vue sans filtre dossier considère tous les candidats ;
une vue filtrée ne reprend pas le meilleur dossier extérieur au filtre. Les
compteurs distinguent prospects uniques et dossiers évalués. Un candidat pertinent
non calculé interdit de présenter la synthèse comme exhaustive.

## 5. Carte, filtres et cohérence des lectures

- Même objectif, version de règle active, filtres et état des résultats dans
  Qualification, Prospects et Carte. Filtrage serveur avant pagination/agrégation ;
  pas de téléchargement exhaustif ni de classification en JavaScript.
- Les scores de profils différents ne sont pas comparables par défaut : regrouper
  par profil ou trier dans un même profil/modèle. Un ordre global exigerait une
  calibration commune validée ; ni commerce ni EPCI n’est favorisé par une échelle
  différente. La légende rappelle le profil ; en vue mixte non calibrée, les
  groupes présentent la répartition par profil/niveau, pas un rang global.
- Pour une recherche **Collectivités → Communes**, la pastille au centre communal
  reprend uniquement le niveau du prospect commune identifié par cet INSEE.
  Le popup montre nom, niveau, score détaillable et date ; une autre organisation
  située dans cette commune ne lui prête pas son niveau.
- Si la recherche inclut plusieurs types/prospects par centre, utiliser une
  pastille unie si leurs niveaux/états sont identiques, sinon une **pastille
  segmentée avec répartition et effectif**, puis liste paginée au clic. Aucun
  maximum, moyenne ou niveau territorial inventé. Des doublons communaux non
  rapprochés ne sont pas fusionnés automatiquement pour la couleur.
- Un EPCI est identifié comme EPCI, même si son siège partage le centre communal.
  Son niveau n’est pas appliqué à toutes ses communes membres ; aucune addition
  des scores ou comptages EPCI/communes. Le filtre par niveau porte sur les
  prospects ; les groupes et compteurs sont recalculés sur les seuls retenus.
- Filtre multi-niveaux et filtres d’état séparés, incluant non calculé, données
  insuffisantes et à recalculer. L’utilisateur peut combiner « Prioritaire » avec
  « sollicitable » ; une opposition reste toujours visible et bloquante.
- Une carte limitée/tronquée doit l’indiquer et demander un affinement ; les
  prospects non localisés restent accessibles en liste avec leur niveau.
  Mobile : légende compacte, filtres accessibles, retour liste/carte conservé.

## 6. Invariants, historique et droits

Le calcul lit les références adoptées et les états **effectifs** des contacts et
porteurs. Ni observation « à examiner », ni ancien porteur vérifié dans une autre
version, ni centre communal approximatif ne devient une preuve commerciale.
La présence de coordonnées publiques ne certifie pas un décideur ou un consentement.

Le niveau ne change **jamais** priorité manuelle, étape, opposition, archivage,
tâche, responsable, donnée de qualification ou preuve de gain. Aucune sollicitation,
invitation, compte, animation, commande ou dossier n’est créé. « Prioritaire »
signifie à examiner commercialement, pas autorisé à contacter en toute circonstance.

Conserver pour chaque calcul règle/version, objectif, profil, date, acteur/lot,
faits et versions de dépendance, références retenues, contributions, inconnus,
motifs et dossier choisi. Historique paginé, correction par nouveau calcul.
Une mutation pertinente ou expiration rend le résultat à recalculer ; la lecture
vérifie les dépendances courantes, sans afficher un ancien vert comme actuel en
attendant un batch. Nouvelle règle = anciens résultats explicitement obsolètes,
pas de mélange silencieux de modèles dans un tri ou une carte.

Les dépendances incluent **l’ensemble des dossiers et contacts candidats** de
l’objectif, leur admissibilité, type/étape/état et versions, pas seulement le
dossier retenu. L’ajout d’un meilleur projet, la fermeture d’un autre candidat ou
la modification d’un contact invalide la synthèse concernée. Clés de cache et
curseurs incluent aussi filtres de dossier, objectif, règle et autorité ; un
changement de filtre ne recycle pas une synthèse d’un contexte différent.

Lecture : `crm.consulter`. Préparation/lancement/arrêt/reprise : `crm.gerer`, avec
CSRF et droits courants relus à chaque unité. Le droit importer ne suffit pas.
Une future modification de règle générale relèverait de `crm.administrer` ; pas
d’éditeur libre de scoring en V1 proposée. Révocation = arrêt des unités restantes,
aucun droit transmis par un identifiant de lot ou curseur.

## 7. Contrats, capture et limites techniques à détailler

Contrats futurs : préparation de sélection et compte exact ; lancement 202 avec
jeton de préparation/idempotence/version de règle ; progression et bilan paginés ;
arrêt/reprise ; détail du résultat ; filtres/tri et répartition cartographique.
Ils n’existent pas encore et ne sont pas ajoutés au JSON OpenAPI du code actuel.
Revoir les curseurs, totaux datés, retour après authentification, menu et cache PWA.

Capturer durablement les IDs et versions d’entrée depuis une sélection cohérente,
pas par un simple curseur vivant ou une borne d’ID. Si la capture dépasse le
budget interactif, préparation asynchrone avec date d’instantané explicite avant
confirmation. Revalider faits et droits dans la transaction de publication par
prospect. Unité atomique, aucun demi-score ; lot à succès partiels explicites.
Déduplication par lot/unité/règle et jeton de bail, reprise après crash, arrêt
entre unités, historique des unités déjà validées conservé.

Bornes structurelles proposées : lectures 25 résultats par défaut, 100 maximum ;
traitement en paquets de 100 prospects maximum sans hydrater leur historique ;
500 groupes cartographiques au maximum, résultats et segments bornés ; 1 lot actif
par acteur et objectif, 2 workers au maximum pour ce nouveau travail. Les chiffres
doivent être confirmés par capacité, avec plafond d’audience, durée maximale,
budgets SQL/mémoire, timeout, équité et baux précisés avant activation. Saturation
visible, aucun thread par prospect ni appel réseau de qualification dans ce batch.

Prévoir table de lots/unités et résultats versionnés, index de sélection et de
lecture par objectif/règle/niveau/état/score avec départage ID, unicité de publication,
résumés par axes et dépendances invalidables sans N+1. Les index et projections
exacts nécessitent les plans de requête. Reprendre les principes de reprise des
imports sans utiliser leur autorisation, leur source ou leurs tables comme lot
de qualification. Ordonnanceur et console de supervision accueillent ce batch
avec progression, conflits et âge de file, sans contacts ou notes dans les logs.

## 8. Impacts, preuves et préparation restante

Cette évolution remplace l’exclusion d’un score automatique déterministe pour ce
seul usage ; **scoring IA, probabilité de vente et pipeline personnalisable**
restent exclus. La priorité manuelle existante est conservée. CA-01 à 49 et le
report CA-24 restent stables ; **CA-50 à 59** sont ajoutés dans le backlog.

| Critères | Preuves à produire, non exécutées | Impacts et conditions de livraison |
| --- | --- | --- |
| 50/51 | Navigateur et intégration : recherche, total toutes pages, capture, changement de filtres, double clic ; zéro résultat | Menu Qualification, API privées, contrats, guide ; aucune audience déduite des seules lignes visibles |
| 52/53 | Domaine : scores déterministes, frontières et faits inconnus/périmés, sans dossier, multi-projets, profils distincts | Barèmes/domaines à finaliser ; fixtures synthétiques, aucun gain ou donnée source modifié |
| 54/55 | HTTP/PostgreSQL et navigateur PC/mobile : filtres communs, tri sans mélange de profils non calibrés, segments, commune/EPCI/commerce co-localisés, non-localisés, légende clavier | Carte et listes PWA, snapshots de requêtes et nouveaux index, pas de données privées envoyées aux tuiles |
| 56/57 | Domaine/application : règles remplacées, expiration, référence changée, contact obsolète, nouveau dossier meilleur ou candidat réouvert, concurrence, crash, rejeu et révocation | Résultats/historique/dépendances de tous les candidats, jobs durables, console, droits courants |
| 58/59 | Migration/restauration, contrats, charge mixte N/10N, SQL/DOM/mémoire, conservation et compatibilité CSV | Migration additive sans inventer un niveau, guide ops, générateur synthétique et mesures avant activation |

Livraison prévue dans le **backend/PWA CRM** et sources canoniques du projet.
Les trois frontends Pro/Animation/Marketplace ne consomment pas ces contrats
internes : aucun impact direct identifié. ERP réutilise ses droits CRM existants ;
pas de changement des comptes ou droits métier. Les CSV 1/2 restent acceptés ;
un score provenant d’un fichier ne doit pas remplacer le résultat calculé.
Les anciens prospects démarrent Non calculé, jamais à un niveau déduit de notes.

Avant implémentation dépendante : valider poids, seuils, couverture minimale,
conditions « Prioritaire », profils livrés et règles par objectif/type, preuves
et fraîcheur par dimension, synthèse de projets, budgets/volumes et conservation
ARB-07. Les décisions acquises sont l’entrée de menu, le calcul sur recherche,
la carte filtrable et la combinaison **potentiel + maturité + fiabilité** ; les
valeurs chiffrées restent des recommandations identifiées. Aucune de ces réserves
n’empêche le cadrage des écrans, de la sélection durable ou des refus d’accès.

Cette demande produit une conception ; aucun développement, migration ou calcul
réel sur TEST, commit, push ou déploiement n’est exécuté. Les preuves métier de
cette extension restent **à produire** ; les contrôles documentaires ne les remplacent pas.

## 9. Vérification de ce cadrage

Revue indépendante en lecture seule : objectifs existants conservés, invalidation
sur tous les candidats, synthèse filtrée distincte des résultats par dossier et
absence de tri entre profils non calibrés précisés. Aucun constat majeur restant
sur ce cadrage ; barème et budgets demeurent à finaliser comme indiqué ci-dessus.

Contrôles exécutés sur les sources locales, base projet `85c9dfd` avec travaux
E71-EVOL-05/06 : guides/liens **sans erreur ni avertissement**, **147 sources
exportées validées**, bundle local généré et vérifié par empreintes (**148
documents distribués**, manifeste compris), `git diff --check` réussi.
Seul `localeo-projet` est modifié ; backend produit inchangé. Aucun test du
nouveau comportement métier ou parcours navigateur n’a été exécuté, faute
d’implémentation : les tests de la section 8 sont uniquement prévus.
