# E71-EVOL-06 — Niveau de qualification et priorité de prospection

Spécification cible du **6 novembre 2026**, complétant le cadrage du 5 novembre,
rattachée à l’[epic 71](README.md) et à ses
[critères stables](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md).
État produit conservé : **En cours**. Extension **spécifiée sous réserve des
arbitrages produit identifiés**. Implémentation locale du 6 novembre : domaine,
capture et calcul persistés, API, menu et carte PWA. Le potentiel prépondérant et
les seuils commune 5/10, EPCI 20/50 sont confirmés. Les profils restent versionnés ;
activation et preuves de capacité détaillées dans le [bilan](verification-livraison.md).

## 1. Demande et décision acquise

Ajouter une entrée **Qualification** dans le menu CRM : rechercher des prospects,
calculer leur niveau sur l’ensemble du résultat et identifier ceux à traiter en
priorité. Afficher les niveaux et leurs filtres dans les listes et sur la carte.

L’utilisateur choisit explicitement le 5 novembre : **priorité commerciale
combinant fiabilité, potentiel et maturité du projet**, plutôt qu’un simple taux
de remplissage de la fiche. Le niveau ne se limite donc pas à la qualité des six
blocs de qualification. Le 6 novembre, il précise **« Fort potentiel, même sans
projet engagé »** et refuse de retenir le barème proposé sans révision. La cible
donne donc la priorité au potentiel ; maturité et fiabilité restent des axes
secondaires visibles. Les seuils commune 5/10 et EPCI 20/50 sont ensuite
confirmés pour cette première version ; les durées restent une politique technique versionnée.
Aucun compte ou rôle supplémentaire n’est demandé.

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

1. **Rechercher** : réutiliser les filtres serveur des Prospects (texte, sous-type collectivité,
   département, potentiel, contacts, etc.) et ajouter niveau, état du calcul et
   objectif commercial. Conserver les filtres dans l’URL et les retours de fiche.
2. **Préparer le calcul** : afficher le nombre total, l’objectif/profil, la version
   de règle et la date de sélection. **Tous les résultats**, pas seulement la page
   visible, sont visés. Une sélection explicite d’IDs est possible comme variante
   bornée ; aucun « tout sélectionner » ambigu avec les 25 lignes de la page.
3. **Lancer le calcul** : action explicite « Calculer sur les X prospects », refus
   clair si zéro résultat ou profil non disponible. Un aperçu ne publie aucun résultat.
4. **Suivre** : progression persistante (en attente, en cours, terminé,
   partiellement terminé, interrompu ou échec), compteurs et bilan paginé.
   Quitter la page n’annule pas le travail ; un double clic retrouve le même lot.
5. **Décider** : liste triable par priorité, avec potentiel, maturité, fiabilité,
   qualité des données et motifs courts. « Pourquoi ce niveau ? » montre les faits
   retenus et les actions manquantes, avec liens vers les bons champs ou dossiers.

Lancement confirmé = périmètre figé, règle et autorité identifiées. Une saisie
postérieure qui ferait entrer un nouveau prospect dans la recherche ne l’ajoute
pas au lot. Les données changées depuis la préparation sont signalées en conflit,
pas calculées silencieusement avec une autre base. Le recalcul de résultats dont
le niveau fait lui-même partie des filtres ne doit ni déplacer le curseur du lot
ni en faire disparaître les unités restantes.

## 4. Priorité fondée d'abord sur le potentiel

### 4.1 Arbitrage et modèle proposé

**Arbitrage utilisateur du 6 novembre 2026 : « Fort potentiel, même sans projet
engagé ».** La proposition de moyenne pondérée 40/35/25 est **abandonnée en
l'état**, ainsi que ses seuils globaux 40/70, sa couverture minimale de 80 % et
l'obligation d'un contact décisionnel vérifié pour être prioritaire. Aucun de ces
anciens paramètres ne subsiste dans les contrats ou critères du modèle cible.

La traduction proposée est un **ordre lexicographique**, et non une moyenne :
potentiel d'abord, maturité ensuite, fiabilité enfin. Un potentiel fort connu
reste prioritaire sans dossier, budget, porteur ou contact ; un projet mûr à
potentiel moyen ne passe pas devant lui. Les inconnus restent visibles et ne
deviennent pas des zéros. Une forte priorité ne constitue ni permission de
solliciter ni probabilité de vente.

Profils initiaux proposés : ANIMATION_COMMUNE_1 et ANIMATION_EPCI_1, objectif
existant SOUSCRIPTION_ANIMATION, règle cible POTENTIEL_DABORD_1. Aucun profil
Coffrets ou commerce participant inventé : PROFIL_NON_DISPONIBLE. Les classements
restent par profil, sans rang global communes/EPCI non calibré.

### 4.2 Axe potentiel : seul déterminant du niveau de priorité

Fait retenu : nombre de commerces de la référence COMPTAGES adoptée, évaluation
CONFIRMEE et portée COMMUNE ou MEMBRES_NOUVELLE_AQUITAINE selon profil. Une portée
COUVERTURE_PROJET ne remplace pas le potentiel du territoire complet. La sélection
existante de projection_potentiel est conservée : terrain complet prioritaire,
sinon documentaire. Terrain périmé : potentiel à revalider, sans bascule silencieuse
vers un documentaire plus avantageux. Population et comptage global tous secteurs
ne remplacent pas le nombre de commerces. Ne pas additionner commune et EPCI.

Les seuils suivants sont **confirmés par l’utilisateur le 6 novembre 2026 pour
la première version** ; cette décision ne modifie pas la règle historique SEUILS_ANIMATION_1 :

| Profil | Potentiel faible | Potentiel intermédiaire | Potentiel fort | Justification et limite |
| --- | --- | --- | --- | --- |
| Commune | 0–4 commerces | 5–9 | Au moins 10 | Frontières 5/10 confirmées pour le profil commune |
| EPCI | 0–19 commerces | 20–49 | Au moins 50 | Frontières 20/50 confirmées pour le total intercommunal ; ne prouvent pas sa répartition entre communes |

La concentration du potentiel sur quelques communes d'un EPCI reste affichée
comme limite de preuve si elle est connue ; aucune répartition géographique
n'est déduite d'un total. Les deux profils peuvent être implémentés avec ces seuils.
Avertissement de calibration : le seuil communal de 10, repris de la prospection
territoriale existante, pourrait classer trop de communes dans FORT et donc peu
les distinguer. Mesurer la distribution du portefeuille permettra une éventuelle
révision explicite et versionnée, sans changer les seuils approuvés ni ajouter
silencieusement un classement par population ou nombre brut.
Aucun opérateur UI ne peut modifier ces seuils au fil d'une recherche.

| Niveau de priorité | Règle proposée | Repère graphique |
| --- | --- | --- |
| PRIORITAIRE | Potentiel FORT connu et courant | Étoile et vert |
| A_QUALIFIER | Potentiel INTERMEDIAIRE connu et courant | Progression et bleu |
| A_EXPLORER | Potentiel FAIBLE connu et courant | Boussole et orange |
| POTENTIEL_A_VERIFIER | Aucun potentiel admissible ou potentiel inconnu | Point d'interrogation et contour pointillé |
| NON_CALCULE | Aucun résultat pour l'objectif/profil/règle | Tiret gris |
| A_RECALCULER | Axe potentiel historique invalidé par fait/règle/temps ; changement d'un axe secondaire seul sans effet sur ce niveau | Horloge, ancien niveau explicitement historique |

L'absence de maturité/fiabilité ne déclenche jamais POTENTIEL_A_VERIFIER : seul
l'axe potentiel le détermine. Zéro commerces prouvé donne FAIBLE ; aucun comptage
donne INCONNU, jamais FAIBLE. Une erreur technique reste séparée et n'efface pas
le résultat précédent. Libellés, pictogrammes et légende doublent les couleurs.

### 4.3 Axes secondaires : départager et guider, sans bloquer la priorité

Les règles ci-dessous sont proposées pour rendre le départage reproductible ;
elles ne constituent pas une nouvelle exigence de dossier ou de contact.

| Axe | État proposé et règle | Départage dans un potentiel identique |
| --- | --- | --- |
| Maturité | STRUCTURE : besoin IDENTIFIE, porteur effectif CONFIRME, calendrier futur documenté et budget CONFIRME positif du même dossier | Premier |
| Maturité | BESOIN_IDENTIFIE : besoin IDENTIFIE documenté, sans réunir les quatre conditions STRUCTURE | Deuxième ; afficher les faits manquants ou négatifs |
| Maturité | BESOIN_ABSENT : absence de besoin explicitement attestée | Troisième ; n'efface pas le potentiel |
| Maturité | INCONNUE : besoin non établi ; SANS_DOSSIER : aucun projet admissible | Valeur de rang null, après les maturités connues ; distinguer les deux libellés, sans zéro métier |
| Fiabilité | ETAYEE : identité, territoire, provenance du comptage et contact tous vérifiés/courants | Première |
| Fiabilité | PARTIELLE : au moins un de ces blocs vérifié, sans contradiction courante | Deuxième |
| Fiabilité | A_REVALIDER : contradiction explicite courante d'un bloc | Troisième |
| Fiabilité | INCONNUE : aucun bloc exploitable | Rang null, sans zéro |

L'ordre entre maturités/fiabilités est une recommandation de tri secondaire à
valider, pas une valeur pondérée. Les coordonnées accessibles publiquement ne
certifient pas un contact décisionnel, un consentement ou un portage effectif.
Un contact fiable exige statut VERIFIE, version courante, coordonnées exploitables,
nature PERSONNE/SERVICE et rôle DECIDEUR/PORTEUR_OPERATIONNEL. Un accueil/relais
vérifié est montré comme tel, sans satisfaire ce bloc de fiabilité. L'absence
de contact ou de projet est une action suggérée, pas un motif de rétrogradation
d'un potentiel fort. Le nombre de contacts et la longueur des notes n'ajoutent rien.

Exemples obligatoires : commune avec 12 commerces admissibles, sans dossier et
sans contact → PRIORITAIRE ; commune avec 8 commerces et projet STRUCTURE/contact
vérifié → A_QUALIFIER, après la première ; même potentiel fort avec projet
STRUCTURE → devant le fort potentiel sans dossier ; potentiel inconnu avec projet
STRUCTURE → POTENTIEL_A_VERIFIER. Aucun résultat sur 100 n'est présenté.

### 4.4 Preuves, fraîcheur et inconnus

Le domaine reçoit calcule_le, jour UTC pour preuves datées : mêmes faits/règle/
instant donnent le même résultat. Seuls les faits adoptés sont lus, sans analyse
de notes ou appel externe. Proposition de fraîcheur : potentiel 180 jours ;
identité/territoire 365 jours ; besoin/porteur/calendrier/budget/contact 90 jours.
Date terrain = controle_terrain_date ; documentaire = date_observation, bornée
aussi par source_date si présente (la plus ancienne). Preuve de durée D admissible
pour 0 <= jour_calcul − date <= D, expiration à 00:00 UTC le jour date + D + 1.
Dates futures de preuve refusées ; une donnée incohérente historique est inconnue.
Le calendrier devient passé le lendemain du début et invalide sa contribution.

Écart vérifié : besoin/calendrier n'ont pas de preuve datée propre et l'identité
n'a pas de confirmation globale. Proposition d'attestations liées à
(entité, bloc, empreinte des champs), avec constate_le, source_reference, auteur_id
et version. Blocs IDENTITE, TERRITOIRE, BESOIN, CALENDRIER, ABSENCE_PORTEUR,
ABSENCE_BUDGET, ABSENCE_CONTACT. Les preuves datées contact/porteur/budget/comptage
existantes sont réutilisées. Changement des faits rend l'attestation obsolète.
Import, calcul ou date de modification ne valent jamais vérification. E71-EVOL-05
peut fournir des preuves adoptées uniquement sur les faits effectivement contrôlés.

Besoin IDENTIFIE exige résumé et attestation ; ABSENT exige attestation. Porteur
CONFIRME exige personne/service actif, version liée et preuve de portage. Budget
CONFIRME exige EUR, base HT/TTC, montant et preuve ; montant zéro ou ABSENT ne
prouvent pas un projet financé. Calendrier exige début futur ou du jour, fin
cohérente si fournie et attestation ; pas de fenêtre commerciale de 180 jours
ajoutée au tri. Aucun prix d'offre n'est déduit du budget.

Une preuve absente/périmée, une portée incompatible ou une contradiction donnent
un fait INCONNU avec motif, jamais un zéro. Restituer les faits connus/inconnus
par axe, sans couverture minimale globale ni intervalle de score. Une incohérence
d'identité/territoire qui empêche d'attribuer le comptage au prospect rend le
potentiel inconnu ; l'absence d'un contact ne rend pas le comptage inconnu.

### 4.5 Plusieurs projets et synthèse

Un résultat conserve trois axes distincts, objectif/profil/règle et dossier
éventuel. Proposition de candidats de maturité : dossiers actifs Animation /
SOUSCRIPTION_ANIMATION aux étapes A_CONTACTER, DISCUSSION, PROPOSITION. PAUSE,
GAGNEE, PERDUE et archives restent historiques ; leur réouverture invalide la
synthèse. Leur absence n'empêche pas une nouvelle priorité fondée sur le potentiel.

Chaque projet est évalué séparément ; jamais besoin d'un dossier, porteur d'un
autre et budget d'un troisième. La synthèse choisit le meilleur axe de maturité
d'un même dossier admissible, à fiabilité prospect identique, puis UUID dossier
ASC pour départager. Sans candidat : dossier_id=null et maturité=SANS_DOSSIER,
potentiel et fiabilité restent évalués, aucun dossier créé.

Les filtres portant sur un dossier s'appliquent tous au même candidat. Filtre
dossier sans candidat : zéro prospect dans cette recherche, pas un dossier fictif.
Une vue filtrée ne choisit pas de projet extérieur à sa sélection. Conserver
résultats par dossier et synthèse contextualisée, sans écraser une synthèse globale
avec celle d'une recherche. Un candidat pertinent non calculé rend le **départage
de maturité** incomplet ; il ne retire pas une priorité issue d'un potentiel
courant déjà vérifié. Afficher cette limite et ne pas prétendre le tri secondaire
exhaustif.

Ordre serveur proposé, au sein du même profil/règle : potentiel fort/intermédiaire/
faible/inconnu, puis rang maturité (nulls last), puis fiabilité (nulls last), puis
organisation_id ASC. Le comptage brut explique la classe, mais n'introduit pas de
quatrième critère caché. Les comptes distinguent prospects, dossiers et inconnus.
Encodage technique proposé pour ce tri ascendant : rang_potentiel 0/1/2/3 dans
l'ordre indiqué ; rang_maturite 0 STRUCTURE, 1 BESOIN_IDENTIFIE, 2 BESOIN_ABSENT,
null INCONNUE/SANS_DOSSIER ; rang_fiabilite 0 ETAYEE, 1 PARTIELLE, 2 A_REVALIDER,
null INCONNUE. Ces rangs ne sont pas des notes et ne s'additionnent pas.

## 5. Carte, filtres et cohérence des lectures

- Même objectif, version de règle active, filtres et état des résultats dans
  Qualification, Prospects et Carte. Filtrage serveur avant pagination/agrégation ;
  pas de téléchargement exhaustif ni de classification en JavaScript.
- Les niveaux de profils différents ne sont pas comparables par défaut : regrouper
  par profil ou trier dans un même profil/modèle. Un ordre global exigerait une
  calibration commune validée ; ni commerce ni EPCI n’est favorisé par une échelle
  différente. La légende rappelle le profil ; en vue mixte non calibrée, les
  groupes présentent la répartition par profil/niveau, pas un rang global.
- Pour une recherche **Collectivités → Communes**, la pastille au centre communal
  reprend uniquement le niveau du prospect commune identifié par cet INSEE.
  Le popup montre nom, niveau, trois axes détaillables et date ; une autre organisation
  située dans cette commune ne lui prête pas son niveau.
- Si la recherche inclut plusieurs types/prospects par centre, utiliser une
  pastille unie si leurs niveaux/états sont identiques, sinon une **pastille
  segmentée avec répartition et effectif**, puis liste paginée au clic. Aucun
  maximum, moyenne ou niveau territorial inventé. Des doublons communaux non
  rapprochés ne sont pas fusionnés automatiquement pour la couleur.
- Un EPCI est identifié comme EPCI, même si son siège partage le centre communal.
  Son niveau n’est pas appliqué à toutes ses communes membres ; aucune addition
  des niveaux ou comptages EPCI/communes. Le filtre par niveau porte sur les
  prospects ; les groupes et compteurs sont recalculés sur les seuls retenus.
- Filtre multi-niveaux et filtres d’état séparés, incluant non calculé, potentiel
  à vérifier et à recalculer. Une opposition reste toujours visible et bloquante.
  Un éventuel filtre cible « sans opposition structure » ne prouve pas le droit
  de solliciter un contact sur un canal : le contrôle intervient à chaque action.
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
faits et versions de dépendance, références retenues, états des axes, inconnus,
motifs et dossier choisi. Historique paginé, correction par nouveau calcul.
La validité est **par axe** : dépendances, génération et prochaine échéance
distinctes pour potentiel, maturité et fiabilité. `etat_priorite` dépend seulement
de la validité du potentiel et du profil/règle qui classe celui-ci. Un contact
expiré ou un dossier fermé ne retire pas le niveau PRIORITAIRE ni la couleur verte
d'un potentiel toujours courant. L'axe secondaire périmé affiche A_RECALCULER,
son rang est neutralisé à null avant le tri, sans présenter son ancienne valeur
comme actuelle. Ses faits historiques restent consultables.

Seul le potentiel périmé ou une modification de son profil/règle met la priorité
à recalculer. La lecture vérifie ces dépendances sans attendre le batch. Changer
uniquement une règle secondaire invalide cet axe ; les sous-versions de règles
par axe évitent une invalidation globale accidentelle. Le modèle de résultat
garde une version d'enveloppe pour la compatibilité, distincte de ces sous-versions.

Les dépendances incluent **l’ensemble des dossiers et contacts candidats** de
l’objectif, leur admissibilité, type/étape/état et versions, pas seulement le
dossier retenu. L’ajout d’un meilleur projet, la fermeture d’un autre candidat ou
la modification d’un contact invalide les axes secondaires concernés, jamais le
potentiel par défaut. Une preuve commune à plusieurs axes invalide exactement
ses axes dépendants. Clés de cache et
curseurs incluent aussi filtres de dossier, objectif, règle et autorité ; un
changement de filtre ne recycle pas une synthèse d’un contexte différent.

Lecture : `crm.consulter`. Préparation/lancement/arrêt/reprise : `crm.gerer`, avec
CSRF et droits courants relus à chaque unité. Le droit importer ne suffit pas.
Une future modification de règle générale relèverait de `crm.administrer` ; pas
d’éditeur libre de scoring en V1 proposée. Révocation = arrêt des unités restantes,
aucun droit transmis par un identifiant de lot ou curseur.

## 7. Contrats cibles, capture et limites techniques

Contrats implémentés localement : préparation de sélection et compte exact ; lancement 202 avec
jeton de préparation/idempotence/version de règle ; progression et bilan paginés ;
arrêt/reprise ; détail du résultat ; filtres/tri et répartition cartographique.
Ils figurent dans le JSON OpenAPI régénéré depuis le backend. Les curseurs,
totaux datés, retour après authentification et menu sont vérifiés ; la PWA ne
met pas en cache les réponses privées.

Capturer durablement les IDs et versions d’entrée depuis une sélection cohérente,
pas par un simple curseur vivant ou une borne d’ID. Si la capture dépasse le
budget interactif, préparation asynchrone avec date d’instantané explicite avant
confirmation. Revalider faits et droits dans la transaction de publication par
prospect. Unité atomique, aucun résultat incomplet publié ; lot à succès partiels explicites.
Déduplication par lot/unité/règle et jeton de bail, reprise après crash, arrêt
entre unités, historique des unités déjà validées conservé.

Bornes structurelles : lectures 25 résultats par défaut, 100 maximum ;
traitement en paquets de 100 prospects maximum sans hydrater leur historique ;
500 groupes cartographiques au maximum, résultats et segments bornés ; 1 lot actif
par acteur et objectif, 1 worker de calcul au maximum dans une enveloppe commune
de 2 unités lourdes CRM (imports/actualisation/qualification). Capture et calcul
consomment la même place de la famille qualification ; les imports ne disposent
pas de deux places additionnelles. Voir l’[enveloppe commune](architecture-contrats.md#articulation-v13--implémentation-locale-du-6-novembre).
Les budgets ci-dessous doivent
être vérifiés par mesure avant activation. Saturation
visible, aucun thread par prospect ni appel réseau de qualification dans ce batch.

Prévoir table de lots/unités et résultats versionnés, index de sélection et de
lecture par objectif/règle/niveau/état/rangs des axes avec départage ID, unicité de publication,
résumés par axes et dépendances invalidables sans N+1. Les index et projections
exacts nécessitent les plans de requête. Reprendre les principes de reprise des
imports sans utiliser leur autorisation, leur source ou leurs tables comme lot
de qualification. Ordonnanceur et console de supervision accueillent ce batch
avec progression, conflits et âge de file, sans contacts ou notes dans les logs.

### 7.1 Contrat HTTP implémenté localement

Producteur : API privée backend Prospection ; consommateur : PWA CRM embarquée.
ERP expose les droits et son lien CRM sans recalculer. Le générateur documentaire
backend actualise le contrat canonique ; les routes et le consommateur PWA sont
vérifiés ensemble.

Préfixe /internal/prospection/qualification-commerciale :

| Route cible | Corps / résultat | Autorisation et effets |
| --- | --- | --- |
| GET /profils | Profils disponibles, objectifs/types compatibles, règle et dimensions | crm.consulter ; référentiel borné aux deux profils V1 |
| POST /preparations | Filtres canoniques, objectif/profil/règle ; 202 avec ID et URL de suivi | crm.gerer, CSRF, idempotence ; capture sans résultat publié |
| GET /preparations/{id} | État, snapshot_at, comptes prospects/candidats, empreinte, expires_at | Droits courants sur l'audience ; confirmation seulement à PRETE |
| POST /lots | preparation_id, empreinte_attendue ; 202 avec lot et URL de suivi | crm.gerer, CSRF/idempotence ; aucun remplacement des filtres au lancement |
| GET /lots/{id} et /lots/{id}/unites | Version/état/compteurs et bilan paginé | crm.consulter et périmètre courant ; aucun contact/note dans bilan global |
| POST /lots/{id}/arreter et /reprendre | version_attendue ; 202 ou 200 si déjà réalisé | crm.gerer, CSRF/idempotence, arrêt entre unités |
| GET /resultats/{id} | Faits minimaux/provenance, axes, inconnus et validité | crm.consulter sur prospect courant ; UUID seul insuffisant |

Sous le préfixe existant /internal/prospection, routes cibles complémentaires :
GET /organisations/{id}/historique-qualification (lecture paginée) et POST
/organisations/{id}/attestations-qualification (cible_type, cible_id, dossier_id
conditionnel, bloc, empreinte/version attendue, date, référence ; 201,
crm.gerer/CSRF/idempotence). La seconde atteste un fait
courant, sans le modifier ni lancer de calcul. Source HTTP(S) ou référence texte
validée selon la politique des preuves de qualification existante ; auteur serveur.

`GET /organisations/{id}/attestations-qualification/cibles?dossier_id=...`
retourne les cibles disponibles, leurs faits courants, version et empreinte
attendues, sous `crm.consulter`. La PWA présente ces faits avant l'attestation ;
elle ne reconstruit pas l'empreinte depuis son propre formulaire.
La réponse bornée, sans pagination, contient `items` avec `cible_type`, `cible_id`,
`dossier_id`, `bloc`, `version_attendue`, `empreinte_attendue` et
`faits: [{champ, valeur}]`. Sans dossier, seules les cibles organisation sont
proposées ; un dossier doit appartenir au même prospect et au périmètre Animation.
Le POST reprend exactement la cible/version/empreinte et ajoute `constate_le`
et `source_reference`.

IDENTITE/TERRITOIRE/ABSENCE_CONTACT exigent cible_type=ORGANISATION, cible_id égal
à l'ID de route, dossier_id absent. BESOIN/CALENDRIER/ABSENCE_PORTEUR/ABSENCE_BUDGET
exigent cible_type=DOSSIER, cible_id=dossier_id et un dossier Animation du prospect
de route accessible à l'acteur. La version attendue et l'empreinte sont celles de
la cible exacte, pas seulement de l'organisation. Relation ou bloc incompatible :
422 ; version/empreinte changée : 409 ; cible hors droits : 404. Aucune attestation
générique contact : sa confirmation garde le contrat de qualification contact
existant (ID et version du contact). ABSENCE_CONTACT porte sur la génération de
la collection de contacts ; tout ajout/mutation la rend obsolète.

Exemple de préparation, sans SQL libre ni filtre UI interprété localement :

~~~json
{"objectif":"SOUSCRIPTION_ANIMATION","profil":"ANIMATION_COMMUNE_1",
 "regle_version":"POTENTIEL_DABORD_1","selection":{"mode":"RECHERCHE",
 "filtres":{"sous_type_collectivite":"COMMUNE","departement":"33"}}}
~~~

Variante mode IDS : 1 à 100 UUID uniques autorisés, sans union implicite avec
les filtres. Clés inconnues, objectifs incompatibles ou filtre dossier incohérent
refusés. En-tête Idempotency-Key selon CRM : même clé/corps retrouve le résultat ;
autre corps sous la même clé → 409. L'identifiant de préparation ne porte aucun
droit et expire après 15 minutes à l'état PRETE.

La regle_version demandée identifie un manifeste immuable des sous-versions
potentiel/maturité/fiabilité, figé pour la capture et la publication. Un nouveau
manifeste qui ne change qu'une sous-version secondaire ne périme pas le potentiel
en lecture : comparer les sous-versions, pas seulement l'identifiant du manifeste.

Le DTO résultat contient id, organisation_id, dossier_id nullable,
objectif, profil, regle_version (manifeste capturé), version_enveloppe, calcule_le, etat_priorite
(NON_CALCULE/COURANT/A_RECALCULER/PROFIL_NON_DISPONIBLE), niveau et les trois axes
distincts de §4. Aucun etat global d'obsolescence ne commande la couleur.
Chaque axe contient valeur_metier, etat_validite (COURANT/A_RECALCULER/NON_CALCULE),
regle_version, generation_capturee, dependances_empreinte, prochaine_echeance,
rang_effectif nullable et faits avec état CONNU/INCONNU, motif, preuve/version.
Potentiel précise classe, valeur et base du comptage ;
maturité précise dossier_id et exhaustivite_departage ; fiabilité détaille ses
quatre blocs. Aucun champ score, score_min/max, poids ou couverture globale :
ils appartenaient à la proposition abandonnée, jamais livrée. Le niveau PRIORITAIRE
accepte maturite=SANS_DOSSIER et contact=INCONNU. Aucun texte libre de note dupliqué.
Un prospect NON_CALCULE n'a pas de faux résultat à zéro ; profil indisponible
explicitement indiqué. Le niveau et etat_priorite restent distincts ; un axe
secondaire obsolète est visible sans dégrader la priorité. Le bilan expose aussi
les axes à recalculer, pour ne pas masquer le besoin de mise à jour.

Erreurs : 401 session absente ; 403 droits révoqués ; 404 cible inexistante/hors
audience ; 409 REGLE_REMPLACEE, PREPARATION_EXPIREE, DONNEES_MODIFIEES,
VERSION_CONFLICT, IDEMPOTENCY_CONFLICT ou LOT_DEJA_ACTIF ; 422 SELECTION_VIDE,
PROFIL_NON_DISPONIBLE, FILTRES_INCOHERENTS, PREUVE_INVALIDE ou VOLUME_SELECTION_DEPASSE ;
429 capacité avec Retry-After ; 503 indisponibilité transitoire. Format d'erreur
CRM standard avec code/détail/corrélation. Un conflit d'une unité devient CONFLIT
dans le bilan, pas une erreur 500 générale ni un calcul sur de nouveaux faits.

### 7.2 Capture, transitions et concurrence

Préparation : EN_ATTENTE → CAPTURE_EN_COURS → PRETE / ECHEC / ANNULEE. Une
transaction PostgreSQL REPEATABLE READ matérialise par INSERT … SELECT audience,
candidats, contacts/provenances, faits et versions dans les tables de capture.
Compte exact et faits viennent du **même instantané**. Aucun curseur vivant, borne
d'UUID ou total compté hors de cet instantané ne convient. Capture asynchrone avec
snapshot_at ; transaction bornée à 10 secondes. Au dépassement de volume/durée :
rollback, ECHEC, invitation à affiner ; jamais PRETE sur une capture tronquée.
Le lancement revalide les droits et l'empreinte ; l'autorité de capture est auditée.

Lot : EN_ATTENTE → EN_COURS → TERMINE / PARTIEL / ECHEC ; arrêt explicite :
ARRET_DEMANDE → INTERROMPU. Révocation : INTERROMPU avec motif dédié. Unité :
EN_ATTENTE → EN_COURS → SUCCES / CONFLIT / REFUSE / ECHEC. Une unité est **un
prospect et tous ses candidats capturés**, publiés atomiquement ensemble. TERMINE
signifie toutes SUCCES ; PARTIEL mélange des succès et refus/conflits/échecs ;
ECHEC aucun succès et aucune unité restante. Compteurs mis à jour transactionnellement,
pas de scan du lot à chaque polling.

Avant publication : relire droits et jeton de dépendances (y compris ajout/retrait
de candidat), sous verrou du jeton prospect et des seules lignes nécessaires,
dans un ordre stable. Différence avec capture → CONFLIT, aucune publication.
Cette comparaison de publication couvre les trois vecteurs de dépendances :
le nouveau calcul est publié atomiquement pour tous ses axes. Un conflit du
nouveau calcul n'efface pas les axes encore valides du résultat antérieur.
Le temps de calcul est celui de capture ; toute prochaine_echeance franchie avant
publication (preuve, frontière de calendrier ou autre dépendance temporelle) →
CONFLIT, jamais publication d'un résultat déjà périmé. Bail 60 s, heartbeat 20 s,
jeton de fencing refusant la publication d'un ancien worker. Unicité
(lot_id,organisation_id) et (unite_id,dossier_cle) : la clé sans dossier est
explicite, pas un NULL SQL autorisant plusieurs lignes.

Reprise : unités non commencées et erreurs techniques réessayables seulement ;
3 reprises maximum, délais 5/30/120 s dispersés ; succès conservés. Conflits/refus
exigent une nouvelle préparation. Crash après commit retrouve SUCCES. Reprise
avec droits révoqués, règle remplacée ou faits expirés ne poursuit pas silencieusement.
L'arrêt ne supprime ni résultats ni historique. Aucun e-mail/WebPush émis.

### 7.3 Lectures, index et invalidation

Pagination serveur par clé, 25 par défaut/100 maximum ; curseur signé lié à
objectif/profil/règle, filtres, tri, contexte d'accès et version de contrat, TTL
15 min. Filtre ou autorité changé → refus et retour au début. Ordres : résultats
(rang_potentiel, rang_maturite NULLS LAST, rang_fiabilite NULLS LAST, organisation_id ASC)
dans un profil, rangs ascendants définis au §4 ;
unités organisation_id ASC ; historique (calcule_le DESC,id DESC). Nuls après
résultats calculés. Navigation courante annoncée vivante ; seule l'audience du
lot garantit l'exhaustivité. Total daté préparé/projeté, sans COUNT historique
obligatoire sur chaque page. Enrichir seulement les racines de la page par requêtes
groupées, sans N+1 ni jointure multipliant les racines avant LIMIT.

Filtres **nouveaux** Qualification/Prospects/Carte : objectif, profil,
qualification_niveaux[], qualification_etats[] (etat_priorite), axe_a_recalculer
optionnel et règles actives par axe. Tous utilisent le
même dossier candidat pour maturité et synthèse ; pas deux EXISTS séparés.
Le DTO carte porte effectif, répartition de niveaux par profil, troncature et
compteur non-localisés, jamais moyenne globale. Plafond 500 groupes.

Tables cibles : préparations/captures/lots/unités/résultats immuables, dépendances,
attestations et projections courantes. Index proposés :

- Unités (lot_id,etat,organisation_id) ; bail partiel (etat,bail_expire_le,id).
- Résultats (organisation_id,objectif,profil,regle_version,calcule_le DESC,id DESC).
- Projection (objectif,profil,regle_potentiel_version,etat_priorite,rang_potentiel,rang_maturite_effectif NULLS LAST,rang_fiabilite_effectif NULLS LAST,organisation_id).
- Dépendances (type_entite,entite_id,axe,resultat_id) ; échéances (axe,prochaine_echeance,organisation_id).
- Attestations (entite_id,bloc,version DESC) ; FK indexées, unicités lot actif/idempotence.

Valider les plans sur requêtes réelles ; la présence de ces index ne prouve pas
leur usage. Une mutation incrémente synchroniquement les générations des axes
affectés : dossier créé/retiré/réouvert → maturité ; contact → fiabilité et maturité
si porteur lié/candidat ; comptage/référence ou territoire d'attribution → potentiel
et fiabilité ; preuve → uniquement axes qui la consomment. Résultats/projections
conservent générations, sous-versions de règle et échéances par axe.

Avant filtre niveau/couleur, vérifier le potentiel ; avant tri secondaire, vérifier
maturité/fiabilité et neutraliser les rangs périmés. Le batch matérialise pour
accélérer ; la lecture détecte `now >= prochaine_echeance[axe]` même s'il est arrêté.
Le filtre « Prioritaire » conserve donc un prospect dont seul le contact a expiré.
Un référentiel territorial changé invalide les axes dépendants via sa génération
jointe ; ne pas attendre une édition manuelle. Le domaine produit états/rangs/
échéances par axe ; SQL contrôle accès/versions/temps sans recopier les règles.

### 7.3.1 Ordre de lecture projeté — correctif du 6 novembre

La migration v300 projette les rangs déjà produits par le domaine dans
`crm_priorite_ordre`. Aucun nouveau barème : les générations, versions de règles
et échéances déterminent uniquement si ces rangs peuvent encore être utilisés.
Les écritures de résultats et mutations entretiennent cette projection dans la
même transaction. Le meilleur candidat est marqué dans cette projection ; un
index partiel `(profil,rp,rm,rf,organisation_id)` sur `est_meilleur` permet de
suivre la page courante sans recalculer et trier le meilleur candidat de tout le
portefeuille. Les filtres de dossier sélectionnent leur meilleur candidat parmi
les seules projections du prospect, selon le même ordre. Un repère
`NON_CALCULE` permanent par prospect/profil conserve la
sémantique d’un dossier filtré qui n’a pas encore de résultat propre.

Le lecteur effectue un entretien borné de 100 lignes candidates échues, puis
vérifie l’absence de reliquat dans le même instantané SQL que la page. Si la
fraîcheur ne peut pas être garantie, il refuse par 429
`CLASSEMENT_EN_ACTUALISATION` ; aucun résultat périmé n’est présenté comme courant.
Le batch continue cet entretien par passages bornés même lorsque les nouveaux
calculs sont désactivés. Avec 50 candidats par prospect, 100 lignes ne signifient
pas 100 prospects. La cadence et le nombre de passages conditionnent la
disponibilité après une expiration massive.

Le chemin compte trois lectures SQL hors authentification : entretien, page
avec contrôle de fraîcheur, puis résultats immuables des seuls IDs affichés
(deux si la page est vide). Curseurs signés, filtres et droits restent vérifiés ;
un curseur de l’ancienne version de tri demande de relancer la recherche.

La capture fige d’abord au plus 10 001 IDs dans la transaction `REPEATABLE READ`.
La sentinelle refuse plus de 10 000 prospects avant de matérialiser les faits.
Les comptages d’enfants s’arrêtent à 101 contacts et 51 dossiers, avec plafond
global de 50 000 candidats. Les attestations sont lues par cible/bloc courant,
dernière version seulement, sans parcourir leur historique entier. Tous les
plafonds refusent la préparation entière, sans troncature ni publication partielle.

### 7.4 Budgets proposés et mesures requises

Ces objectifs **non mesurés** ne prouvent pas une capacité ; ne pas les relever
après un test insuffisant pour faire passer l'activation.

| Opération | Bornes et budget cible |
| --- | --- |
| Audience | 10 000 prospects, 50 000 candidats au total ; 50 dossiers et 100 contacts par prospect. Dépassement refuse toute la préparation, pas une troncature |
| Capture | Une capture à la fois, dans la place qualification partagée avec le calcul ; SQL/transaction 10 s, verrou 2 s ; insertion serveur sans hydratation globale ; file maximum 20 préparations |
| Travail | 1 worker calcul dans enveloppe globale 2 unités lourdes CRM ; acquisitions de 25 unités au plus ; 1 transaction/prospect, SQL 2 s, transaction 5 s ; RSS < 256 Mio/worker |
| Équité | Alternance acteurs entre paquets, 1 lot actif/acteur/objectif, 30 min de traitement par lot puis INTERROMPU reprenable ; pas de monopolisation des imports/rappels |
| Lecture | Au plus 6 requêtes SQL/page hors authentification constante ; p95 < 500 ms, p99 < 1 s hors réseau ; erreurs inattendues < 1 % |
| Carte | 500 groupes, p95 < 1 s ; aucune donnée privée envoyée au fournisseur de tuiles |
| PWA | 100 lignes DOM, 3 pages mémorisées maximum ; recherche annulable ; polling 5 s visible uniquement, arrêt si masquée/terminale/perte de droits, reprise à la visibilité après relecture des droits |

Jeu N : 1 000 prospects/3 000 dossiers ; 10N : 10 000/30 000, historique multiplié
séparément par 10 ; pages de 25 et 100, premières/profondes, filtres rares/vides,
prospects hors droits. Charge mixte : 20 lecteurs, 2 rédacteurs, imports/rappels
actifs, actualisation et calcul selon budget global, paliers jusqu'à saturation
et reprise. Mesurer SQL/plans/BUFFERS, lignes/octets, p50/95/99, RSS, pool/verrous,
débit/âge file, cache froid/chaud. Le travail exhaustif croît avec l'audience ;
mémoire et unités restent bornées. Tester aussi 50 dossiers/100 contacts, pas
uniquement la moyenne. Mesure sur base jetable, jamais TEST partagé implicitement.

## 8. Migration, impacts et preuves attendues

Migration additive à numéro attribué lors de l'implémentation : tables/index et
jetons de dépendance ; aucune réécriture de v294, aucune reprise de niveau depuis
CSV/notes. Anciennes données NON_CALCULE ; attestations absentes inconnues. CSV 1/2
inchangés, champs de scoring non importables ; aucun dossier automatique. Préserver
contacts/actions/oppositions. Tester migration sur copie jetable, idempotence du
runner, sauvegarde/restauration et anciennes commandes CRM. Désactiver calcul et
écrans avant retour à un ancien binaire ; aucun down destructif automatique.

Ordre de livraison : schéma additif, backend compatible ancien CRM, contrats,
PWA puis ordonnanceur après mesures. Supervision : lot, acteur interne, règle,
compteurs/âge/file/durée/conflits, sans coordonnées ni notes. ARB-07 doit définir
conservation des captures/résultats/audits avant données réelles ; l'implémentation
et les tests synthétiques restent possibles. Respecter suppression/anonymisation
des prospects ; l'historique de qualification n'autorise pas une conservation illimitée
des contacts. Aucun envoi ni nouveau canal de communication.

Livraison backend/PWA CRM et sources canoniques projet. Pro/Animation/Marketplace
ne consomment pas ces API internes, sans impact direct ; ERP réutilise ses droits.
Le socle CA-01 à 49 et CA-24 reporté restent inchangés. Les critères stables
CA-50 à 59 sont détaillés ci-dessous. **Matrice cible ; exécutions réelles et limites dans le bilan de vérification.**

| CA | Preuves comportementales à produire | Documentation / fixtures / exploitation |
| --- | --- | --- |
| 50 | Navigateur PC/mobile : menu Qualification, filtres URL, lecture seule, retour fiche, sélection toutes pages | Guide CRM, acteurs synthétiques lecteur/gestionnaire/révoqué |
| 51 | API/PG : capture cohérente pendant mutation, total exact, zéro résultat, plafond, expiration, double clic/rejeu, filtre sur niveau recalculé | Contrats capture/lots ; sélection département 33 et 100 IDs |
| 52 | Domaine pur : seuils proposés commune 4/5/9/10 et EPCI 19/20/49/50, dates D/D+1, zéro connu/inconnu, priorité sans projet/contact, absence de moyenne et de couverture bloquante | Table §4 comme oracle proposé ; temps figé et axes séparés |
| 53 | Fort potentiel sans dossier devant potentiel moyen/projet structuré ; départage à potentiel égal ; PAUSE/gagné/perdu, deux projets sans mélange, filtre sur même candidat, refus Coffrets | Commune/EPCI synthétiques ; aucun dossier créé ou barème commerce déduit |
| 54 | SQL/API : droits avant LIMIT, curseur changé/périmé, obsolescence avant filtre, synthèse filtrée ; navigateur filtres communs | Index/plans/DTO, comptes prospects distincts de candidats |
| 55 | Commune/EPCI/commerce colocalisés, segments/doublons, clavier/contraste/mobile, carte tronquée et non-localisés | Fixtures géographiques synthétiques, légende par profil |
| 56 | Invalidation par axe : fermeture du dernier dossier ou expiration contact conserve priorité/vert/filtre Prioritaire si potentiel inchangé, neutralise seulement les rangs secondaires ; expiration comptage retire le vert courant ; règle/référentiel changé, worker arrêté | Générations/échéances par axe et absence de mélange historique/courant |
| 57 | Crash avant/après commit, fencing concurrent, révocation, arrêt/reprise, retries, conflit sans demi-résultat | Supervision/reprise ; aucun doublon ou donnée privée dans logs |
| 58 | Niveau prioritaire sans changement d'étape/priorité manuelle/opposition/archivage/responsable ; sollicitation interdite reste interdite | Non-régression du socle, aucun envoi réel |
| 59 | Migration/restauration, anciens CSV, contrats/PWA, N/10N mixte §7.4, saturation/reprise | Générateur backend à enrichir, guides utilisateur/ops et rapport de capacité |

## 9. Préparation et arbitrages

Acquis : **fort potentiel prioritaire même sans projet engagé**, menu dédié,
calcul sur toute une recherche et carte filtrable. La moyenne 40/35/25 et ses
conditions de couverture/contact sont abandonnées en l'état ; elles ne constituent
plus une proposition à implémenter ni une question en attente.

La traduction proposée conserve trois axes non moyennés : potentiel puis maturité
puis fiabilité. Les seuils par profil sont confirmés (commune 5/10, EPCI 20/50).
Restent des politiques versionnées : fraîcheur, états et ordre des départages secondaires,
candidats de maturité et attestations. Le seuil EPCI est une nouvelle calibration,
distincte du classement territorial existant. Son absence de validation bloque
seulement l'activation du profil concerné ; elle ne remet pas en cause l'arbitrage
de priorité exprimé. Aucune nouvelle question utilisateur n'est créée ici.

Les attestations évitent d'inventer une fraîcheur. Elles accompagnent les blocs,
sans écran de notation ni points manuels. Une dimension sans preuve reste inconnue,
jamais fraîche via la date d'import/modification. Une fiabilité ou maturité
incomplète guide les prochaines actions sans retirer la priorité d'un potentiel
fort établi. E71-EVOL-05 fournit les preuves adoptées dans la limite des faits
réellement contrôlés, et non une preuve de projet commercial par inférence.

Contrats, captures, droits, pagination, migration et tests sont spécifiés ;
activation soumise à calibration du profil, mesures de capacité et conservation
ARB-07 pour données réelles. Les tests synthétiques restent possibles. Code
vérifié : qualification.py pour champs/statuts/versions, projection_potentiel
pour comptage, porteur_statut_effectif pour porteur, regles.py pour objectifs/
étapes et prospection_qualification_filtres.py pour filtres. Le nouveau classement
n'existe pas dans l'implémentation examinée.

Évolution documentaire seule : aucun code, calcul TEST, migration, commit, push
ou déploiement. Les contrôles documentaires ne prouvent ni comportement métier
ni capacité.
