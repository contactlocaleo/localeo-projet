# E73-WL — Suites du workshop Localeo Live du 18 novembre 2026

## Périmètre et décisions

Spécification du 18 novembre 2026, après adoption des six orientations puis
demande explicite des phases spécification et implémentation.
[Cadrage et 18 critères WL](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-live-20261118),
[audit](../../audits/marketplace/localeo-live-workshop-arbitrages-2026-11-18.md),
[décision utilisateur](../../../ateliers/ux-workshops/localeo-live/2026-11-18/validation/decisions.md).
État produit : E73 historiquement terminée ; extension suivie séparément.
B1/C1/D1/E1 P1 ; A1/F1 P2. Ni compteurs ni clôture historique modifiés.

Les [principes UX](../../produit/live/principes-ux.md) et les
[correctifs LIVE-COR du 18 novembre](localeo-live-entree-unique.md#correctifs-du-18-novembre-2026--carnet-découverte-et-notification)
restent applicables. Les 14 planches illustrent les orientations sans remplacer
la référence graphique validée : conserver en-tête/outils, trois onglets,
cartes blanches, symboles des moteurs et action verte ; pas de favoris ajoutés
ni filtres internes du carnet. La compacité concerne les repères du catalogue,
pas une refonte graphique du parcours personnel.

## Existant vérifié et écarts à réaliser

Sources applicatives dans `localeo-marketplace` :

| Orientation | Code lu et comportement existant | Delta retenu |
| --- | --- | --- |
| A1 | `LiveUnifiedCarnet.jsx` affiche un carnet vide, Parcours/Coffrets, découverte et récupération | Une phrase reliant animations dans le carnet, gains dans Mes lots et programme dans Découvrir ; aucune nouvelle action principale |
| B1 | `LiveApp.jsx`, `LiveSavedConfirmation.jsx` et tests `live-participation-confirmation` séparent réponse d'inscription, accès personnel et stockage ; incertitude réconciliée sans POST implicite | Recette des succès/échecs existants ; expliciter l'issue sans inscription pour un accès refusé, sans titre public ou identité inventés |
| C1 | `LiveLots.jsx`, détail du bon et tests `live-lots-unified` / `live-maquettes-habitant` portent état, consignes, échéance, récupération et relecture | Qualifier les états réels et corriger seulement un écart reproduit ; ne pas ajouter de transition, PIN ou contact non fourni |
| D1 | `LiveDiscovery.jsx` regroupe EN_COURS/A_VENIR, conserve pages/filtres/retours ; dates après les repères longs de `PublicAnimationEffort` ; `LiveCommunityScene` ne montre ses raccourcis que pour plus de trois animations réparties sur les deux périodes | Généraliser la navigation locale existante aux petits programmes et périodes vides/en erreur, dates plus haut, version concise des repères Juste Prix/Vitrines ; restrictions particulières conservées intégralement |
| E1 | LM-11 et tests existants couvrent mobile/focus/200 % ; contraste et clavier du QR refusé à mesurer sur application | Contrôles ciblés et corrections seulement si reproduites ; noms accessibles et issue sans inscription explicites |
| F1 | `LiveUnifiedCarnet.jsx` et `unifiedCarnet.mjs` conservent accès distincts, récupération, état inconnu et lecture bornée LIVE-COR | Rejouer reprise, carnet rempli, refus, mélange de gains/participations ; aucun nouveau stockage |

## Comportements et conception

### Programme et carnet vide — WL-01/02/09/10/11

Le carnet vide indique où retrouver animations, lots et programme avec un texte
court ; « Découvrir les animations » reste l'action principale.
Découvrir présente la navigation existante « Explorer les animations » avant les cartes,
avec deux liens textuels « En ce moment » et « Prochainement ». Activer
une commande focalise le titre de sa section et le place sous l'en-tête ;
aucune requête, filtre ou pagination n'est déclenché par ce déplacement.
Le raccourci n'est rendu que si les sections correspondantes existent : pas
de cible morte dans le programme entièrement vide, le mode anciennes idées,
la recherche trop courte ou les filtres non supportés. L'état vide d'une seule
période et son erreur restent atteignables. Les retours de fiche conservent les
mécanismes existants de restauration des pages, position et focus.

Chaque carte garde statut et pictogramme, titre, commune, type et dates avant
les explications. Si la commune n'est pas connue, elle est indiquée à préciser.
Les dates absentes ou invalides restent explicites selon les formateurs Paris.
Les repères du jeu des vitrines et du Juste Prix sont condensés pour le catalogue
seulement : réponse/estimation définitive, seuil publié, tolérance connue,
passage requis ou non, qualification sans gain automatique. La fiche conserve
la version détaillée, notamment modalités et révélation après clôture.
Les conditions particulières, âge, achat et public visé restent consultables
avant engagement ; aucune troncature de restriction et aucun seuil inventé.

**Ordre et bornes :** le backend trie déjà par date de début puis identifiant
(`recherche_animations_live.py`, requête paginée ; catalogue historique
`catalogue_animations_publiques.py`, tri statut/date/id). Le mode serveur
conserve cet ordre, ses pages de 12 et ses curseurs. Le repli ancien serveur
fusionne plusieurs communes : trier seulement la fenêtre déjà chargée par date
de début, dates inconnues en dernier, égalités stables ; annoncer la portée
« Animations chargées, par date de début » pour ne pas promettre un tri global.
Ne jamais charger toutes les pages pour satisfaire ce tri de présentation.

### Confirmation, reprise et lot — WL-03 à 08, WL-15 à 17

Conserver les mécanismes de confirmation et d'accès existants : réponse métier
confirmée avant annonce d'inscription ; accès enregistré distinct de celle-ci ;
relecture après incertitude sans nouvelle inscription silencieuse. Un refus
retire les capacités privées. L'écran QR invalide propose la récupération
existante et explique que le retour au carnet permet de découvrir si aucune
inscription n'existe. Aucun nouveau parcours d'inscription depuis un token
inconnu, aucune donnée personnelle révélée par ce token.

Un lot demeure dans sa nomenclature métier actuelle. Présenter ou fermer son
QR ne consomme rien ; « Marquer comme vu » reste local. La disponibilité fraîche
commande l'accès au bon, la relecture commande l'état remis ; une panne ne vaut
ni remise ni expiration. Les informations pratiques manquantes sont explicites.
Deux participations à la même animation gardent leurs identifiants et accès.

### Accessibilité et essais — WL-12/13/14/18

Contrôler noms/rôles, focus et parcours clavier de carnet/découverte/accès/lot,
320/390/430 px, texte 200 %, erreurs et contrastes des commandes essentielles
(texte normal 4,5:1, repères non textuels 3:1, cible locale 44 px). Ces mesures
sont une recette ciblée, pas une déclaration de conformité globale. Produire
des captures et mesurer les couleurs réellement calculées, y compris focus.
La structure accessible automatisée ne remplace pas une utilisation vocale.
Lecteur d'écran, clavier virtuel/appareil physique et essais habitants restent
des preuves humaines à distinguer des scénarios Chromium simulés.

Le contrôle applicatif a reproduit un contraste **2,27:1** sur le lien primaire
de récupération QR : texte `rgb(8,40,64)` sur `rgb(9,104,94)`, issu de la cascade
partagée des styles Coffrets/Live. Correction locale dans `live-carnet.css` :
texte blanc pour les actions primaires de `.live-add-page`, y compris survol et
focus ; fond existant conservé et cibles de 44 px. Le test mesure la cascade
réellement chargée, pas une palette théorique.

## Invariants, frontières et contrats

Le domaine backend Animation reste propriétaire des inscriptions, statuts,
qualifications et remises ; Commercialisation conserve les droits des coffrets.
API/ERP/batch/Pro ne sont pas modifiés. Les projections publiques sont produites
par les services de catalogue Animation et consommées par `services/api.js`,
`publicAnimations` et `LiveDiscovery`. Champs utilisés : `statut_public`,
`date_debut`, `date_fin`, `commune`, `regles_participation`, repères d'effort et
dotations publiques déjà normalisés. Aucun schéma, endpoint ni champ requis
nouveau ; contrats documentaires E41/E42 et consommateurs inchangés.

L'affichage ne décide ni ouverture d'inscription, ni clôture depuis une date,
ni éligibilité depuis un compteur. Pas de commande métier ajoutée ; annulation
des lectures, générations contre réponses tardives, permissions et idempotence
restent identiques. Aucun enrichissement des journaux, URLs ou Analytics.

## Impacts, données et livraison

| Sujet | Conclusion |
| --- | --- |
| Dépôts | Marketplace : composants/styles/tests ; Projet : spécification, bilan et index. Backend lu pour vérifier l'ordre des producteurs, sans modification prévue. Animation/Commerçant sans nouvelle entrée ni contrat à adapter. |
| Données et migration | Aucune nouvelle donnée persistée, clé ou migration ; accès, anciennes idées et consentements préservés. |
| Démonstration | Fixtures de parcours étendues dans Marketplace pour dates, périodes, restrictions et erreurs. Générateur backend inchangé : aucune nouvelle règle, colonne ou permission et données existantes suffisantes. Aucun peuplement réel. |
| Performance | Même nombre d'appels et bornes catalogue ; navigation locale sans réseau. Tri de la seule fenêtre héritée au plus 60 éléments par période, sans nouvelle jointure/SQL. Mesures N/10N du helper et contrôle du nombre d'appels prévus ; pas de nouvelle charge serveur/cadence justifiant campagne PostgreSQL. |
| Exploitation | Livraison du frontend par procédure habituelle, sans migration ni ordre backend imposé ; cache PWA et actualisation explicite existants. Vérifier après livraison les deux périodes, retours et QR refusé ; retour à l'artefact frontend précédent si régression. Aucun déploiement inclus. |

## Matrice de preuves et suivi

La matrice suivante fixe les preuves prévues ; les résultats effectivement
exécutés figurent au bilan ci-dessous. Les tests utilisent des fixtures isolées.

| Critères | Comportement / propriétaire | Preuves prévues | Impacts |
| --- | --- | --- | --- |
| WL-01/02 | Texte et programme / Live | `live-workshop-20261118.spec.cjs`, carnet vide à 320 px / 200 % | Documentation Live ; fixture vide ; pas de migration |
| WL-03/04/05 | Confirmation et reprise / domaine existant, UI Live | `live-participation-confirmation.spec.cjs`, QR et refus du test WL | Contrats conservés ; fixtures d'accès isolées |
| WL-06/07/08 | Lots et actions / domaine existant, UI Live | `live-lots-unified`, `live-maquettes-habitant`, `digital-lot` | Trois natures et états synthétiques ; aucune remise réelle |
| WL-09/10/11 | Programme / projection publique + Live | Tests WL, `live-discovery-continuity`, `live-iconography-discovery`, tests Node du tri et repères | Même pagination ; fixture multicommunes ; contrôle d'appels |
| WL-12/13/14/15 | Accessibilité et erreurs / Live | Tests WL clavier/ARIA/contraste/rendu ; suites lots/confirmation ; lecteur d'écran et appareil à qualifier séparément | Pas de conformité globale ; captures du runner |
| WL-16/17 | Reprise et accès distincts / Live | `live-unified-carnet`, `live-participation-confirmation`, `live-return-continuity` | Stockage existant ; refus et reprise sans effet externe |
| WL-18 | Compréhension / habitants | Missions réelles : découvrir une date, retrouver une inscription, expliquer où/quand/comment retirer ; consigner réponses et difficultés sans les suggérer | Essais humains non simulables par votes ; pas de seuil de réussite inventé |

## Note de reprise par lot

- WL-L0 : lecture des producteurs/consommateurs et recouvrements terminée ;
  aucune nouvelle règle ou modification d'API nécessaire.
- WL-L1/L2 : spécification et réalisation locales terminées.
- WL-L3 : recette automatisée terminée ; WL-18 et composantes humaines de
  WL-12/13 restent à qualifier séparément.
- Ressources : seul l'agent principal possède build/serveur/rapports, via le
  runner isolé Marketplace sur port 8196. Runner terminé, aucun processus de
  recette encore actif. Pas de base ni serveur distant.
- Prochain geste : qualification humaine WL-12/13/18 sur les parcours ci-dessous.
  La réalisation et ses preuves sont disponibles pour revue ; la publication
  Git autorisée est consignée ci-dessous, distincte du déploiement.

## Bilan d'exécution

### Réalisation locale

Deux dépôts modifiés : `localeo-marketplace` (interface, styles et tests) et
`localeo-projet` (sources canoniques, roadmap, audit et liens du workshop).
Base applicative inspectée : `db4dc57e6b2fd78f83a9d2981d181c0eb17c582d` ;
backend lu à `cddef3dc5ad59ec9c12c680fa4899a779e9f81ca`, sans modification.
Pas de changement métier, contrat, schéma, migration ou générateur ; les
justifications de la matrice d'impacts s'appliquent à la réalisation.

Le programme expose les deux périodes même pour un petit catalogue, remonte
dates et commune, condense les règles des deux jeux et trie la seule fenêtre
historique chargée. Le carnet vide relie les trois missions. L'issue QR refusé
est expliquée et son contraste corrigé. Les parcours lots/reprise existants
sont conservés après qualification ; aucun changement artificiel de statut.

### Tentatives et preuves

Artefacts conservés dans `localeo-marketplace/test-results/visual-runs/` ;
chaque dossier contient `run.json`, `results.json`, captures et traces.
Les reprises utilisent `--retry-of` ; leurs résultats ne s'additionnent pas.

| Tentative | Résultat et suite |
| --- | --- |
| `2026-11-18T14-06-22-266Z-LgOL6l` | 6/7 réussis. Fixture du QR refusé ne reconnaissant pas les paramètres de requête ; matcher corrigé sur le pathname. |
| `2026-11-18T14-07-30-330Z-I8Zj6D` | 6/7 réussis. Contraste applicatif 2,27:1 reproduit ; correction CSS locale blanc/vert. |
| `2026-11-18T14-08-26-882Z-X5qtbw` | 97/101 réussis. Deux tests attendent le flyer et deux les filtres du carnet retirés par LIVE-COR-03/06. Attentes alignées sur les règles canoniques, contrôles de retours et accès conservés. |
| `2026-11-18T14-14-53-678Z-rqPOkN` | **102/102 réussis**, aucun échec, skip ou flaky, 4,9 min. Inclut l'URL publique du QR jusqu'à la reprise après rechargement. Build de production isolé réussi, empreinte `fc634a351a6a9c1220579c7e96198716466fbd041cefc4e5060f53cd244a4ada`. |

La divergence des anciennes assertions a été vérifiée dans les sources
**HEAD avant ces modifications** : `LiveDiscovery.jsx` ne rendait déjà aucun
flyer et rendait quatre emplacements pour l'objectif quatre ;
`LiveUnifiedCarnet.jsx` utilisait déjà `filter = 'tout'` sans boutons de filtre.
Les assertions de pictogramme, quatre visites, absence de filtres et accès
simultanés animation/coffret les remplacent. L'assertion de commune sur chaque
carte correspond, elle, au nouveau critère WL-10. Aucun skip ajouté.

Contrôles complémentaires exécutés :

- `npm run test:security` : **318 réussites, aucun échec ni skip**, après ajout
  des frontières de seuil/tolérance. Tri stable, dates invalides, règle sans
  valeur inventée ; mesure du helper à N=60 et 10N=600 sous le budget de 100 ms
  (la borne UI demeure 60 par période, aucune charge SQL nouvelle).
- ESLint ciblé sur les composants/helpers/tests modifiés : réussi.
  `npm run lint` global échoue sur `EPERM scandir` du répertoire existant
  `output/bum-politique/pytest-approval-1`. Aucun ignore ajouté pour le masquer.
- Guides : 108 guides, 1 581 liens, aucun défaut ; contrôle des Markdown
  modifiés : 39 documents, 1 184 liens, aucun défaut après réparation de
  19 liens relatifs décalés dans l'archive du workshop.
- Sources exportées : 151 documents vérifiés. Contrats et exports inchangés.
- `git diff --check` : réussi dans les deux dépôts modifiés.

La commande exacte, les dix suites sélectionnées et le build testé sont
enregistrés dans le `run.json` final ; `results.json` porte les 102 résultats.
Le contraste calculé final sur la récupération QR est **6,66:1 normal,
6,85:1 focus et 8,12:1 survol**, cible **252 × 44 px**. L'animation CSS explique
les couleurs intermédiaires mesurées au focus/survol ; toutes dépassent 4,5:1.
Les captures programme 320/390/430, texte 200 %, carnet vide et QR refusé
sont conservées ; programme 390, programme/carnet 320 à 200 % et QR refusé
ont été examinés visuellement.

| Critères | Résultat local et preuves identifiables dans le passage final |
| --- | --- |
| WL-01/02 | Réussis : tests WL du carnet vide à 320 px/200 % et navigation nommée des périodes à 320/390/430 px. |
| WL-03/04/05 | Réussis sur fixtures : test WL-03/05 depuis l'URL publique jusqu'au même accès après reload ; suite `live-participation-confirmation` (moteurs, refus, stockage en panne, POST incertain, deux participants) et QR refusé WL. Scan optique et autre appareil réel non exécutés. |
| WL-06/07/08 | Réussis sur fixtures : `live-lots-unified` (trois natures, échéance/consignes absentes, accès exact et installation renouvelée), `digital-lot` (valide/remis/expiré/révoqué, refus 403 et réponse PIN perdue), `live-maquettes-habitant` vue 8 (présenter/fermer sans consommation, relecture après remise). |
| WL-09/10/11 | Réussis : tests WL des deux périodes, erreurs/vide, multicommunes et requêtes bornées ; `live-discovery-continuity` (pages, filtres, retours/focus), `live-iconography-discovery` (conditions et absence de faux vide), helper Node tri/dates/règles. |
| WL-12/13 | Partiels : clavier/noms/focus, 320/390/430 et 200 % contrôlés ; lecteur d'écran et clavier virtuel physique non exécutés. |
| WL-14 | Réussi sur les états ciblés : défaut QR reproduit puis corrigé, couleurs calculées normal/focus/survol et cible 44 px ; pas d'audit exhaustif de conformité. |
| WL-15 | Réussi : `live-registration-clarity` (saisie obligatoire, refus et contexte conservé), confirmations incertaines/stockage, erreur QR sans action d'ajout trompeuse. |
| WL-16/17 | Réussis sur fixtures : `live-unified-carnet` (états mixtes, prochaine action, archive, refus/inconnu, lectures bornées), deux participants de `live-participation-confirmation` et chaînes de retour de `live-return-continuity`. |
| WL-18 | Non exécuté : missions et entretiens avec habitants réels restant à organiser. |

### Portée de l'acceptation

La qualification porte sur Chromium local avec API simulées, sans transaction,
notification, inscription ou remise réelle. Les captures sont examinées sur
les parcours modifiés. Une revue indépendante sur extraits a conduit à ajouter
la chaîne QR publique/reprise et les frontières de valeurs ; cette revue ne
constitue ni une inspection autonome du dépôt ni une recette habitant.

WL-12/13 demeurent **partiels** : clavier, noms accessibles, petits écrans et
texte 200 % automatisés, mais lecteur d'écran et clavier virtuel sur appareil
physique non exécutés. WL-18 est **non exécuté** : aucune observation avec des
habitants réels et aucun gain de compréhension ou de temps revendiqué. Le
scan optique physique du QR et la reprise sur un autre appareil réel ne sont
pas prouvés par l'ouverture de son URL et les fixtures de récupération.
Les contrastes mesurés sont ceux des actions ciblées, sans certification de
conformité générale. Les réserves historiques E73 restent indépendantes.

Au terme de la recette locale, aucun commit, push ou déploiement n'avait été
effectué. L'extension reste ouverte pour la qualification humaine ; la clôture
historique E73 n'est pas modifiée.

### Publication Git autorisée le 18 novembre 2026

Après mise à jour de l'audit, l'utilisateur a demandé explicitement « commit
et push ». Marketplace : commit `29053df` publié sur `origin/main`, avec les
composants, styles et tests de cette réalisation. Le commit documentaire
associé conserve l'audit actualisé, le cadrage, la spécification et l'archive
du workshop Live du 18 novembre nécessaire aux références. Les dépôts restent
indépendants ; aucun déploiement ni opération sur les données demandé ou exécuté.
