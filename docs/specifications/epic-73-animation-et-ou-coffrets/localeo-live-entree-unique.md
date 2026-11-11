# E73 — Localeo Live, entrée unique des animations

## Correctif du 11 novembre 2026 — date dans Mon inscription

Le détail personnel d'une animation affiche **Date d’inscription** dans la
section dépliable **Mon inscription**, avec l'e-mail déjà présent. La valeur
provient uniquement de `inscrit_at` du contrat privé existant ; la date d'ajout
au carnet ne la remplace jamais. L'instant est affiché en date et heure de
Paris, avec la mention du fuseau et une balise `time`. Une valeur absente ou
invalide donne **Date non disponible**. Le rafraîchissement et les refus
d'accès gardent leurs protections existantes.

Principes LIVE-UX-02/05/07/08 : information personnelle regroupée, ouverture
volontaire, clavier et lisibilité mobile. Marketplace seul change son rendu ;
aucune règle métier, API, migration, flag, donnée ou générateur à modifier.
Le producteur backend expose déjà la date d'inscription enregistrée.

Preuves locales (base Marketplace `8ad9b12`, correctif **`6c64ff1`**) : absence reproduite avant
correction dans `test-results/visual-runs/2026-11-11T10-44-13-931Z-jsY7Di/`,
puis **4 scénarios réussis** dans `2026-11-11T10-44-51-420Z-2bOer4/` : tombola
publique à 320 px, chasse à 390 px, passeport à 1 280 px, date absente/invalide.
Navigateur réglé sur Los Angeles, heure de Paris vérifiée en hiver (changement
de jour) et en été, ouverture au clavier et date conservée après actualisation.
Les captures finales de la section complète sont inspectées dans
`2026-11-11T10-45-56-758Z-6U1S1R/` (**3 reprises réussies** des mêmes cas de
rendu). Aucun débordement ni commande de jeu implicite. Les **2 tests Node**
du formateur Paris et le lint des fichiers JavaScript touchés réussissent ;
builds isolés, sans API ni donnée réelle. Recette :

```console
node scripts/run-visual-tests.cjs --port 8195 tests/visual/live-participation-mobile-flow.spec.cjs --grep "Date de mon inscription"
node --test tests/security/paris-dates.test.cjs
node node_modules/eslint/bin/eslint.js src/live/LiveAnimationGame.jsx tests/visual/live-participation-mobile-flow.spec.cjs
```

## Correctif du 11 novembre 2026 — résultat sur la vignette du carnet

**Mon carnet** présente les animations personnelles non archivées et les
coffrets conservés ; les cartes de lots et le filtre Lots sont retirés de cette
vue. **Mes lots** conserve tous les gains, leurs détails, l'acquittement
« J’ai vu ce lot » et le compteur de nouveaux gains. Un lot n'est ni supprimé
ni marqué comme vu lors de ce changement de rubrique. Un ancien lien de filtre
Lots ne doit pas réintroduire les lots ni produire un carnet artificiellement vide.

La vignette de chaque participation donne priorité au `resultat_tirage` personnel
du tableau de bord, avant le statut de qualification :

- `GAGNANT` : trophée accompagné de **Gagnant** ; l'accès au détail de la
  participation reste à sa place. Le gain se consulte dans Mes lots.
- `NON_GAGNANT` : pictogramme de résultat sans gain, accompagné de
  **Vous n’avez pas gagné cette fois-ci**.
- `NON_QUALIFIE` après réalisation : **Hors tirage** ; `REMPLACE`, `ANNULE`
  et `SANS_TIRAGE` restent distincts. Une date annoncée, une clôture ou
  l'absence de récompense dans une fenêtre paginée ne prouve aucun résultat.
- Sans résultat confirmé, les états de participation et de qualification
  existants restent utilisés. Une actualisation échouée signale le dernier état
  connu ; un refus d'accès purge la projection personnelle.

Cette précision complète LS-06/08 et remplace les anciennes compositions
mixtes du carnet concernant les lots. Principes LIVE-UX-01/02/04/05/06/07/08 :
un objet à sa place, résultat explicite par texte et icône, lecture mobile et
accès personnels préservés. Le propriétaire du résultat reste
`resultat_personnel_tirage` dans le domaine backend ; le tableau privé expose
déjà les faits nécessaires, pour Coffrets et tirages libres confirmés.
Marketplace seul change sa présentation. Aucun contrat, règle d'attribution,
migration, flag ou format de démonstration modifié ; aucune reprise de données.

### Preuves du correctif

Base Marketplace `35414d5`, correctif **`8ad9b12`**. La reproduction
Node échoue avant correction sur les lots visibles et la qualification qui
masque le résultat, puis réussit. La revue indépendante du consommateur
confirme priorité du résultat personnel, refus prioritaire, exclusion des lots
avant pagination et maintien des accès et de Mes lots.

La recette synthétique `test-results/visual-runs/2026-11-11T10-29-07-051Z-VYTwEe/`
donne **30 scénarios réussis** (notifications et stabilité du chargement), avec
build isolé, sans API réelle ni fichier d'environnement opérateur. Les captures
`carnet-results-{320,390,1280}.png` montrent Gagnant/trophée et le résultat sans
gain/ticket barré ; la première action reste accessible à 320 px. Le badge,
l'acquittement explicite et l'archivage sont également couverts.

La recette adjacente audit/retours/carnet
`test-results/visual-runs/2026-11-11T10-31-09-405Z-iu7qdK/` conserve **34 réussites
et deux échecs d'attentes historiques** : ancien libellé d'annuaire et favori
encore recherché dans le carnet. Les cibles sont adaptées aux parcours actuels,
puis seules ces deux épreuves sont rejouées avec succès dans
`test-results/visual-runs/2026-11-11T10-37-16-430Z-oTZ152/`. Au total, **66
scénarios distincts validés**, sans modification supplémentaire du bundle
applicatif, identique entre les recettes. Les processus sont arrêtés et les
ports 8192/8193/8194 libérés.

Les **27 tests Node ciblés** du carnet, des dates et des accès réussissent,
puis la suite élargie donne **276 réussites, aucun échec**. Cette suite a
d'abord rencontré sept échecs de fixture VM : `live-personal-refresh.test.cjs`
ne fournissait plus `subscribeSeenRewards` au hook `useLiveRewards`. La
comparaison à HEAD confirme le défaut antérieur, sans dépendance aux sources
du carnet modifiées. La fixture exécute désormais le vrai port `liveRewardSeen`
sur stockage simulé durable et événements ; les assertions vérifient aussi
l'acquittement, sa persistance et l'absence de collecte du lot. Aucun hook ni
assertion métier neutralisé. Traces `security-suite-final.log` puis
`security-suite-repaired.log` dans le run ci-dessus. L'ancienne attente
d'historique après résultat est mise en accord avec le maintien jusqu'à
archivage, en vérifiant aussi le résultat affiché.
Commande de la suite Node élargie : `node scripts/run-security-tests.cjs`.

Le lint ciblé `node node_modules/eslint/bin/eslint.js src tests scripts *.cjs
*.mjs` et le contrôle de diff réussissent. `npm run lint` global reste bloqué
par `EPERM` sur le répertoire local d'artefacts
`output/bum-politique/pytest-approval-1`, sans modification de ses droits ni
ajout d'exclusion au correctif.

Le producteur inchangé est vérifié par **55 tests réussis**, sans base réelle :

```console
py -3.14 scripts/validation/test_isolated.py tests/domain/animation_locale/test_resultats_annonces_tirage.py tests/application/animation_locale/test_tableau_de_bord_live.py tests/api/test_localeo_live_tableau_rappels.py -q --tb=short
```

La vérification de l'environnement TEST après livraison reste à réaliser ;
ces preuves locales ne constituent ni un déploiement ni un tirage réel.

## Correctif du 11 novembre 2026 — messages de l'organisation dans le détail

Une entrée unique **Messages de l’organisation** ouvre directement la liste
filtrée sur l’animation consultée. Elle remplace le lien de réglage des alertes
et l’entrée de nouvelles dupliquée. La liaison personnelle de la participation
est vérifiée avant de permettre l’ouverture ; son échec propose un réessai,
sans changer les choix de messages ni demander de permission navigateur.

LS-04 s’applique dès le premier rendu, en pagination, après erreur et au réessai :
aucun message d’une autre animation ne s’affiche automatiquement. Le vide
indique **Aucun message pour cette animation** ; la consultation ne marque rien
comme lu. Les commandes de lecture existantes et le retour à la participation
exacte restent disponibles. La vue filtrée n’affiche aucune gestion d’activation
des notifications ; la catégorie Animations et les alertes de l’appareil se
gèrent depuis Réglages. La messagerie globale conserve son accès aux réglages.

Principes LIVE-UX-02, 05, 07 et 08 : contenu attendu, une seule entrée, clavier,
mobile et retour prévisible. Correction Marketplace uniquement ; API, règles
de lecture, consentements, migration, flags et générateur sans impact : les
contrats et données existants fournissent déjà la liste filtrée. Les preuves
figurent dans le [bilan](verification-livraison.md).

## Correctif du 11 novembre 2026 — avancement homogène des animations

La frise visuelle de la tombola devient le suivi commun des participations :
**Inscrit → Qualifié → Tirage → Résultat**, pour les tombolas locale/publique,
le passeport et la chasse, y compris ses activités de défi. Elle apparaît une
seule fois dans le bloc principal et remplace le bloc « Qualification à
compléter ». Cette précision étend LS-02 sans changer les règles de qualification.

- Les quatre étapes gardent les mêmes pictogrammes, dimensions et repères
  d'étape courante/acquise. Le détail explicite « À compléter », « À vérifier »,
  « Hors tirage », « Annulé » ou « Sans tirage » selon les faits serveur.
- L'aide de qualification cite les visites du passeport ou l'étape de chasse
  autorisée ; un parcours clôturé ne propose pas une validation impossible.
  Régularisation et absence de tirage restent explicites.
- Les visites tamponnées, le QR, les défis et leurs protections restent en
  place. Aucun second jeu de tampons ni progression déduite de la frise.
- La date annoncée, l'agenda, le résultat confirmé et l'accès aux lots restent
  accessibles au même endroit. Pendant la revalidation ou après une panne,
  l'ancien état est signalé et les actions sensibles attendent confirmation.
  Un refus d'accès retire les données personnelles.

Critères de recette : un seul suivi à quatre étapes pour chaque moteur ; aucun
bloc « Qualification à compléter » ; qualification et gain uniquement confirmés
par le serveur, y compris à 100 % ; statuts terminaux/inconnus distincts ; rendus
320/390/1280 px et texte à 200 %, clavier, retours et fraîcheur des actions.
Principes LIVE-UX-02 à 07 appliqués. Marketplace seul change sa présentation ;
aucun contrat API, migration, flag, règle backend ou format de démonstration
modifié. Les données générées gardent leurs états et leurs accès. Preuves dans
le [bilan de livraison](verification-livraison.md).

## Évolution du 11 novembre 2026 — simplicité, E73-EVO-LIVE-SIMPLICITE

Retours directs après les lots PA : symboles d'animation et de confirmation peu
explicites, bloc « À vous de jouer » redondant, détail tombola trop textuel et
rupture de composition entre les onglets Animations et Commerçants. La demande
autorise leur correction et simplification. Les nouvelles restent strictement
limitées à l'animation consultée, selon la précision utilisateur du même jour.
La clôture historique E73 et les réserves de recette hébergée sont conservées.

### Décisions et critères observables

| Critère | Comportement attendu | Preuve prévue |
| --- | --- | --- |
| LS-01 | Ticket ajouré pour la tombola, livret pour le passeport, personne pour la participation, coche cerclée pour une confirmation. Magasin réservé au commerce/visite ; trophée réservé au gain. Icônes accompagnées d'un libellé, mêmes traits et alignements. | Rendu des cartes, découverte et confirmations à 320/390 px ; noms accessibles et cas sans confirmation. |
| LS-02 | Le détail tombola montre un seul workflow Inscrit → Qualifié → Tirage → Résultat. Étape courante et étapes acquises sont distinguées par forme, icône et libellé, pas uniquement par couleur. Le dernier état devient Gagnant ou Non gagnant uniquement sur résultat confirmé. | Projections non qualifiée, qualifiée/en attente, gagnante, non gagnante, hors tirage, annulée et inconnue ; revalidation/refus. |
| LS-03 | Le PIN devient un accès compact et volontaire ; ses explications se déplient. Les préférences de messages deviennent un contrôle secondaire court, avec consentement et retrait explicites. Le détail participation n'affiche plus les alertes de l'appareil, qui restent dans Réglages. | Ouverture/fermeture du PIN, contrôle de fraîcheur, autorisation/retrait/échec de préférence et absence de modification implicite. |
| LS-04 | « Messages de l’organisation » ouvre uniquement les messages de cette animation, dès le premier rendu et lors de la pagination ; retour vers la participation d'origine. Un vide ou un échec ne bascule pas sur les nouvelles globales ni vers la gestion des notifications. | Deux animations ayant des messages, entrée ciblée/retour/pagination et absence de fuite d'un ancien contexte. |
| LS-05 | Découvrir conserve son en-tête, sa sélection communale et ses onglets quand l'habitant passe à Commerçants. Seul le contenu sous les onglets change. Le périmètre réellement recherché reste explicite, y compris en entrée directe et avec plusieurs communes suivies. | Changement d'onglet et retour mobile, commune/périmètre stable, filtres et liens directs, attente/erreur sans disparition du shell. |
| LS-06 | Suppression du bloc autonome « À vous de jouer » / « Ma prochaine action » dans Mon carnet. Chaque objet garde son action à sa place. Dans Mes lots, le titre devient « Lots à utiliser » et les gains restent accessibles. | Carnet rempli et vide, actions des objets/retours/filtre, lots disponibles et aucune action dupliquée en bandeau. |
| LS-07 | Le passeport fusionne progression et visites dans un seul bloc : un compteur confirmé et une seule collection de tampons liés aux commerçants, avec leurs noms, états et dates disponibles. Le QR reste prioritaire et le lien vers les commerçants est intégré au bloc principal, sans section isolée. | Passeport partiel/terminé/inconnu, tampons non dupliqués, ouverture d'une visite, QR et annuaire puis retour. |
| LS-08 | Les animations du carnet sont les inscriptions personnelles aux animations non archivées par l’organisateur. Clôture, annulation, fin de parcours ou tirage terminé ne retirent pas la vignette ; leur état reste explicite et les actions respectent les droits et fenêtres backend. Seul `ARCHIVEE` retire l’animation de cette vue sans supprimer les accès ni les gains. Favoris et simples suivis publics restent dans Découvrir. L'état de participation, les tampons et le cycle de l'animation sont distincts ; aucun archivage n’est déduit d’une date, d’une panne ou d’une projection absente. Précision utilisateur du 11 novembre 2026, remplaçant le filtre antérieur « non clôturées ». | Clôturée avec résultat gagnant/non gagnant, annulée, parcours terminé, archivage confirmé au rafraîchissement et cache local ; ancien serveur/échec sans faux archivage ; favoris exclus, gains et accès conservés après archivage. |
| LS-09 | Chaque lot propose « Voir l’animation », vers la participation exacte lorsqu'elle est connue, avec retour au contexte Mes lots. Consignes et accès au bon restent disponibles. | Plusieurs participants de la même animation, lien public de repli, retours/focus/pagination et absence de capacité dans l'URL de navigation. |
| LS-10 | Chaque vignette d'animation du carnet propose ses nouvelles et un compteur exact des nouvelles non lues lorsqu'il est disponible. L'ouverture ne montre que cette animation. Marquer un message ou les messages affichés comme lus met à jour le compteur après confirmation serveur ; un échec conserve le non-lu et permet de réessayer. Un compteur inconnu n'est pas présenté comme zéro. | Deux animations et deux installations, pagination au-delà de 25, droits révoqués, lecture répétée/échouée et retour au carnet ; budget de requêtes borné par page. |
| LS-11 | Le menu bas Mes lots indique les gains disponibles encore non vus sur cet appareil. « J’ai vu ce lot » acquitte explicitement un gain, décrémente le badge et mémorise ce repère après stockage réussi. Ouvrir la liste, une animation ou les consignes ne vaut pas acquittement. Ce geste n'utilise ni ne remet le lot. | Deux gains puis décrément unitaire, rechargement, nouvel onglet, stockage refusé, nouveau gain ultérieur, pagination et accès refusé ; nombre partiel ou indisponible signalé honnêtement. |
| LS-12 | Le menu secondaire propose le libellé exact « Retrouver mon carnet » et ouvre le parcours de récupération existant ; le retour conserve le point d'entrée. | Menu depuis Carnet, Lots et Découvrir, ouverture et retour mobile/clavier. |
| LS-13 | Une date de tirage annoncée par l'organisateur apparaît directement dans la vignette du carnet, avec repère calendrier et date/heure de Paris. Elle reste visible avant qualification, sans promettre une participation au tirage. Un tirage réalisé ou annulé ne conserve pas une annonce à venir ; une date passée seule ne vaut jamais résultat. L'ajout ne masque pas l'action de la première vignette derrière le menu à 320×568. | Annonce qualifiée/non qualifiée, changement/retrait de date, résultat/annulation, date absente/invalide, état local périmé, rendu mobile et absence de lecture détail par carte. |

Le workflow présente les états existants : `NON_QUALIFIE` après un tirage est
« Hors tirage », jamais « Non gagnant » ; annulation, remplacement et absence de
tirage restent distincts. Une collection complète, un chargement ou un accès
local ne confirme ni qualification ni gain. Les anciennes attentes de bandeau
prioritaire PA/CB et du magasin comme symbole de passeport sont remplacées par
LS-06 et LS-01 ; leurs preuves historiques ne sont pas réécrites.

### Impacts et responsabilité

Marketplace présente les projections backend, conserve les accès,
les refus, l'idempotence et le consentement. Backend ajoute au tableau de bord
privé `statut_animation` (statut du domaine) et `nouvelles_non_lues` (compteur
autorisé par animation). Les champs sont additifs et facultatifs : null ou absent
signifie inconnu. Le compteur est groupé pour la page, jamais une requête par
carte. Les lectures utilisent les reçus existants de la messagerie ; aucune
nouvelle transition de participation ou de remise. Le repère « vu » d'un lot
est un état d'interface local distinct, conservé dans IndexedDB et synchronisé
entre vues/onglets après écriture réussie. Projet porte cette spécification,
la [conception §16](localeo-live-adhesion-conception.md#16-simplicité--e73-evo-live-simplicite),
les principes et le bilan. Pas de migration, flag ou nouvelle donnée de
démonstration : les faits déjà générés alimentent les projections, et les
fixtures de tests couvrent les nouveaux états de lecture. Le contrat OpenAPI
canonique est régénéré depuis le backend. Animation et Pro ne consomment pas
ces champs privés et ne sont pas modifiés. Livrer le backend puis Marketplace ;
l'ancienne API reste lisible avec états et compteurs à vérifier.
Aucun appel métier réel ni activation Analytics. Validation
locale puis recette de l'environnement déployé distincte ; aucun commit,
push ou déploiement implicite. Principes LIVE-UX-01/02/04/05/07/08/10 appliqués.

## Évolution du 10 novembre 2026 — participation, E73-EVO-LIVE-PARTICIPATION

Demande : mettre en œuvre les huit lots du plan accepté après l'audit UX en
conversation (source Marketplace `0a327a2`, parcours locaux avec API simulée).
Cette extension conserve la clôture historique E73, les critères antérieurs et
le suivi des réserves PM-R06/LA-16/LP (PM-R06 corrigé localement au lot 5).
Les résultats propres à chaque lot sont dans le
[bilan](verification-livraison.md#évolution--e73-evo-live-participation-10-novembre-2026),
les choix techniques dans la [conception](localeo-live-adhesion-conception.md#15-participation--e73-evo-live-participation).

Les publics sont l'habitant nouveau, l'habitant revenant avec ses accès et
l'habitant ayant perdu son carnet local. Aucun compte habitant n'est créé.
Téléphone obligatoire pour l'inscription classique, tombola publique par e-mail
seul ; récupération des participations et lots associés par vérification e-mail,
coffrets par les accès et la récupération déjà disponibles.

| Lot / critères | Comportement observable et refus significatifs | Preuves prévues |
| --- | --- | --- |
| 0 — PA-00 | Chaque constat du rapport est relié ci-dessous à une cible, un propriétaire, une preuve et ses impacts ; aucun ancien bilan n'est requalifié | Contrôles documentaires et revue de traçabilité |
| 1 — PA-01 | Carnet, Découvrir, lots, inscription et récupération partagent typographie Pro, sections blanches bordées, action verte, navigation active cohérente ; états d'alerte gardent texte et repère | Captures 320/390/1280, contraste/focus et texte 200 % |
| 1 — PA-02 | Magasin = passeport, parcours = chasse, boussole = Découvrir, épingle = localisation ; noms accessibles incluent « Messages » et « Garder » ; tampons compacts lisibles sans détails parasites | Vérification des moteurs, clavier et noms accessibles |
| 2 — PA-03 | Après ajout confirmé, présenter l'objet exact et l'action « Ouvrir mon passeport », « Commencer mon parcours », « Voir mon ticket » ou « Ouvrir mon coffret », puis « Voir mon carnet » ; installation facultative secondaire | Inscription classique jusqu'au détail personnel et retour carnet ; deux participants d'une même animation |
| 2 — PA-04 | Le retour annonce la destination réelle et conserve le contexte ; anciens liens ciblés et anciennes listes restent servis ; aucune capacité dans les métadonnées de navigation | Liens directs, retour navigateur, détours messages/lots |
| 2 — PA-05 | Tombola : « Inscription enregistrée » confirme la participation ; le prochain geste explique l'accès par le lien e-mail sans présenter un ticket local inexistant | Succès et réouverture, e-mail différé, préférence facultative |
| 3 — PA-06 | Lecture d'accès échouée temporairement : « Réessayer la vérification » réutilise l'accès en mémoire, sans inscription ; refus/expiration n'offrent pas d'action protégée ; erreur de stockage conserve une reprise locale distincte | 503 puis succès, 403, double clic, navigation pendant attente, stockage refusé |
| 3 — PA-07 | `/live/coffrets/ajouter` sans identifiant présente un guide utilisable : lien personnel récent, sauvegarde du carnet, émetteur ; renvoi disponible seulement avec identifiant connu | Entrée générique depuis récupération/lot, lien valide/incomplet, retour ; aucun renvoi inventé par e-mail seul |
| 4 — PA-08 | Première arrivée : invitation brève « Des animations près de chez vous. Un carnet pour suivre vos aventures. », commune/GPS volontaire, recherche et favoris visibles | Arrivée sans commune à 320/390 et bureau, état vide/erreur |
| 4 — PA-09 | Carte : identité, aperçu adapté au moteur, bénéfice réel, date/condition essentielle avant action ; « Voir le parcours », « Découvrir la chasse », « Voir la tombola » ; garder/partager restent secondaires | Trois moteurs, avec/sans flyer, conditions d'achat, inscription fermée ; une carte sur bureau |
| 4 — PA-10 | Catalogue/recherche exposent un aperçu public borné de dotations, compatible avec anciens clients ; aucune identité de gagnant/accès ni requête détail par carte ; absence de nom = repli honnête vers nombre/nature connus | Producteur, contrat, consommateur, refus d'exposition privée et budgets N/10N |
| 5 — PA-11 | Carnet : prochaine action confirmée dominante, objets actifs puis historique ; vide confirmé propose d'abord « Découvrir les animations », puis « Déjà participé ? Retrouver mon carnet » | Vide/rempli/partiel/indisponible, filtres, reprise exacte, mobile |
| 5 — PA-12 | Détail personnel : consulter les étapes déjà autorisées/validées et les informations utiles ; un compteur agrégé ne permet pas d'inventer un commerce ou de dévoiler une étape future | Passeport/chasse, zéro/partiel/terminé/inconnu, clavier et refus |
| 5 — PA-13 | Lots : gain/état/retrait avant détails ; chaque ouverture revient au contexte ; célébration seulement après reçu de validation, jamais au rechargement, compatible mouvement réduit | Bon/coffret/lot libre, détails volontaires et revalidation, confirmation puis rechargement |
| 6 — PA-14 | Mesurer entrée/catalogue/détail/formulaire/inscription confirmée/ajout/étape confirmée/lot ouvert avec taxonomie fermée ; aucun token, e-mail, identifiant métier ou URL personnelle | Tests de politique Analytics et événements de parcours |
| 6 — PA-15 | Première participation observée = visites connues sans accès de participation stocké initialement avec inscription serveur confirmée / visites connues sans accès de participation stocké initialement ayant affiché une entrée Live ; état illisible exclu et suivi séparément. Ce proxy par appareil ne certifie ni validité de tous les anciens accès ni première participation de la personne | Déduplication des succès/reprises, statut initial vide/présent/inconnu, segments programme/vide/sans commune |
| 6 — PA-16 | Identité éphémère par visite ; consentement, retrait et suspension Analytics inchangés ; aucune collecte activée par cette livraison | Tests de transport bloqué et absence de persistance de suivi |
| 7 — PA-17 | Recette intégrée 320×568, 390×844, 1280, clavier/texte 200 %/mouvement réduit : succès, incomplet, lent, erreur, refus, stockage, liens directs et retour | Suites ciblées, revue visuelle et preuves par lot ; corrections des deux sélecteurs obsolètes de choix de commune |
| 7 — PA-18 | Livraison reproductible par dépôt, contrats et migrations identifiés, procédure de retour et scénario humain six personnes préparés ; recette humaine/hébergée non confondue avec tests locaux | Bilan, versions, commandes/résultats et limites d'activation |

### Impacts et invariants de cette extension

Le domaine backend reste propriétaire de la participation, de la validation et
des droits de lots. Ces lots modifient leurs projections et leur présentation,
sans nouvelle transition, attribution ou validation. Les reprises ne relancent
pas les commandes ; les accès sont conservés uniquement dans leur stockage
personnel existant et nettoyés des URL conformément au contrat actuel.

| Périmètre | Responsabilité / impacts |
| --- | --- |
| Marketplace/Live, lots 1–7 | Présentation, contexte de retour, reprise, instrumentation fermée et tests simulés ; aucun nouveau droit ni compte |
| Backend, lot 4 | Projection publique bornée catalogue/recherche, dépôt de lecture groupé et tests isolés ; pas de modification d'inscription ni de schéma métier anticipée |
| Projet, lots 0–7 | Sources présentes, principes UX, contrats générés réellement modifiés, exploitation et bilan |
| Animation / Pro | Contrats embarqués régénérés et tests de consommateurs ; aucun parcours de gestion modifié. La régénération Pro rattrape un instantané ancien ; l'écart historique est décrit au bilan |
| Démonstration | Fixtures de parcours et de dotation publique ; pas de nouveau champ métier requis par le générateur, ni génération sur environnement réel |
| Exploitation | Commits locaux autorisés par lot ; aucune activation Analytics, migration de données ou publication implicite. Capacité hébergée et test humain à réaliser séparément |


**E73-EVO-LIVE-ICONOGRAPHIE — 10 novembre 2026** : spécification puis réalisation
des dix recommandations IA du [rapport iconographie et respiration](../../audits/marketplace/localeo-live-iconographie-aeration-mobile-2026-11-10.md).
Critères E73-IA-01 à 10 en fin de document ; preuves propres au bilan, clôture
historique et réserves PM/LA-16/LP conservées.

Le complément **E73-EVO-LIVE-PARCOURS-MOBILE** du 10 novembre 2026 intègre
le rapport participation/lots/découverte et la référence visuelle Localeo Pro.
Les **neuf critères PM-01 à PM-09** en fin de document précisent les parcours
déjà corrigés dans Marketplace `b9fb30d`. Recette déployée, téléphone physique
et axes complémentaires restent suivis séparément dans le bilan.

Le complément **E73-EVO-LIVE-CARNET-BORD** du 9 novembre 2026 applique les neuf
retours de l’audit mobile sur demande d’implémentation complète. Il remplace
CN-D01 par **Mon carnet / Mes lots / Découvrir**. Critères CB01 à CB09 en fin de
document ; preuves propres au bilan, sans rouvrir la clôture historique.

Les [principes directeurs UX de Localeo Live](../../produit/live/principes-ux.md)
s’appliquent au cadrage, à la conception et à la revue des évolutions de cette
expérience. Ils pérennisent le carnet de bord digital et la collection visuelle
des acquis ; les critères datés ci-dessous portent leurs comportements précis.

Le complément **E73-EVO-LIVE-TAMPONS** du 9 novembre 2026, en fin de document,
ajoute le suivi immersif demandé : carnet de tampons, progression réelle et
prochaine action. Il étend CN-04/05/14 sans changer les règles de validation.

Le complément du 9 novembre **E73-EVO-LIVE-CARNET**, en fin de document,
intègre l’audit PDF sur le carnet personnel unifié. Sa préparation documentaire
est distincte des réalisations LA/LH/FD et conserve la clôture historique E73.

Évolution **E73-EVO-LIVE-UNIQUE**, demandée le **30 octobre 2026**.
L’epic 73 est **Terminée techniquement le 1er novembre 2026**, selon
E73-DEC-CLOTURE-TESTS et le [bilan de clôture](verification-livraison.md).
Les 63 critères initiaux et leurs résultats de recette restent conservés ;
les critères initiaux de cette évolution sont complémentaires et inclus dans cette revue.
Les évolutions datées après la clôture ont leurs propres preuves : notamment
**E73-EVO-LIVE-ADHESION du 7 novembre 2026**, implémentation et vérification locales
suivies dans le [bilan](verification-livraison.md).

## Décision et comportement attendu

En tant qu'habitant, découvrir les animations des communes choisies, s'inscrire
et retrouver ses participations dans un seul espace, Localeo Live, à
`https://animations.localeo.city`. En TEST : `https://test-animations.localeo.city`.
Le portail organisateur reste `gestion-animations.localeo.city`.

Cette décision remplace la surface publique marketplace Animation mise en place
par E73-EVO-DOMAINES et E73-EVO-UX-PUBLIC. Elle conserve le domaine décidé, les
données et les règles métier. Le même dépôt `localeo-marketplace` fournit Live
et Coffrets, sur leurs services respectifs ; aucun nouveau référentiel ni dépôt.
`LOCALEO_PUBLIC_SURFACE=ANIMATION` désigne désormais l'entrée Live. L'ancien
paramètre `surface=animations` ouvre aussi la transition vers Live.

**Arbitrage confirmé par l'utilisateur le 30 octobre : aucun nouveau compte
habitant.** Les communes sont mémorisées sur l'appareil ; leur association à un
compte ne s'applique que si un mécanisme existant la permet. L'installation
anonyme Live n'est pas un compte. Aucune synchronisation de compte n'est ajoutée.
Les contrôles existants des liens personnels, QR, PIN et WebAuthn restent en place.

Hors périmètre initial : refonte Coffrets, changement des règles d'animation,
catalogue ou base de participations distincts et recommandations personnalisées.
Le complément **E73-EVO-LIVE-ACCUEIL-RAPPELS** ci-dessous ajoute l'accueil
personnel et deux rappels facultatifs ; il remplace l'exclusion initiale des
nouvelles notifications pour ces deux seuls usages.

## Parcours et priorité mobile

### Évolution du 3 novembre 2026 — continuité habitant (E73-EVO-LIVE-CONTINUITE)

L'audit produit et sa mise en œuvre sont demandés le 3 novembre 2026. Cette
évolution conserve la clôture historique E73 et le choix sans nouveau compte.
Elle couvre les critères complémentaires suivants ; les preuves exécutées
sont consignées dans le suivi de réalisation, distinctes des tests prévus ici.

| Critère | Comportement attendu | Preuves prévues |
| --- | --- | --- |
| LC01 | Une liste de participations vide propose de retrouver une inscription existante, avec lien personnel ou restauration du carnet ; aucune recherche publique par adresse e-mail ne révèle les inscriptions. | Navigateur : nouvel appareil, lien absent/invalide, récupération et sauvegarde. |
| LC02 | Le scan du lieu possède un décodage de secours indépendant de BarcodeDetector et une alternative utilisable sans caméra ; le QR personnel et le PIN commerçant gardent leurs rôles distincts. | Décodeur, caméra indisponible, photo et QR invalide. |
| LC03 | Le domaine distingue tirage en attente, effectué avec gain, effectué sans gain et annulation ; l'interface ne déduit jamais un résultat de l'absence de lot. | Domaine, API personnelle, affichage de chaque état. |
| LC04 | Le badge reflète les non-lus autorisés, sans acquittement à l'ouverture ; le retour dans Live actualise le compteur. | Pagination, lecture, fermeture sans lecture et retour au premier plan. |
| LC05 | Les choix des nouvelles dans Live restent accessibles sans Push ; autorisation de l'appareil et accord organisateur restent distincts, facultatifs et révocables. | Push refusé/non compatible, réglages et retrait d'accord. |
| LC06 | L'accueil présente une action prioritaire et un résumé compact des nouveaux gains, messages et résultats disponibles, fondés sur les données personnelles autorisées. | États vide/erreur/partiel, absence de compteurs inventés et mobile. |
| LC07 | Les campagnes peuvent guider vers la participation ou les lots du destinataire sans conférer un accès nouveau ; l'absence d'accès utilise la récupération existante. | Destinataires distincts, accès révoqué, liens personnels et refus. |
| LC08 | Le centre propose réessai, filtre des non-lus et sélection d'une animation ; une importance n'est présentée que si elle est explicitement fournie. | Échec initial, filtres/pagination et lectures conservées. |
| LC09 | Les états bloquants proposent une aide contextualisée, avec coordonnées publiques autorisées lorsqu'elles existent et une procédure explicite sinon. | Aucun contact inventé, contexte du lot/animation et mobile. |
| LC10 | Le lieu actuellement accessible propose un itinéraire si son adresse est connue ; aucune étape future cachée n'est révélée. | Parcours chasse/passeport, adresse absente et lien encodé. |
| LC11 | La découverte propose recherche, filtres et sélection « Pour plus tard » sur l'appareil, distincte d'une inscription ; le partage ne contient que l'URL publique. | Recherche bornée, pagination, stockage refusé, partage sans token. |
| LC12 | Une date de tirage planifiée reste informative, ne déclenche pas de tirage et ne confirme pas de gain ; Live la présente seulement si elle existe et permet son ajout volontaire à l'agenda. | Configuration autorisée, date invalide, concurrence, API, affichage/repli et agenda sans donnée personnelle. |

Les célébrations reposent uniquement sur une étape réellement validée ou une
qualification confirmée. Elles respectent la réduction des animations et ne
bloquent pas l'action suivante. Les filtres locaux portent explicitement sur
les animations chargées ; une suite disponible reste accessible même si aucun
élément chargé ne correspond. Les favoris enregistrent des références publiques,
sans token ni duplication de participation. Les messages et états personnels
restent hors cache public. La livraison coordonne producteurs backend et Live ;
la saisie de date et les actions organisateur impliquent aussi leur consommateur
de gestion. La revue de contrats et les tests isolés ne valent pas recette de
Push réel, de caméra physique ou étude auprès d'habitants.

L'annonce de tirage est modifiable depuis Animation et le suivi ERP par un
gestionnaire autorisé, avec version attendue et clé d'idempotence. La date doit
être future et ne pas précéder la fin de l'animation ; elle peut être retirée.
Le domaine interdit la modification après réalisation/confirmation ou annulation
du tirage, ou lorsque l'animation est annulée ou archivée. Le fichier d'agenda contient uniquement
le titre et la date annoncée, sans accès personnel ni alarme imposée. Il ne se
met pas à jour automatiquement : cette limite est indiquée lors du téléchargement.

Navigation basse initiale : **Découvrir**, **Mes participations**, **Mes communes**.
Le complément Accueil/Rappels remplace le premier libellé par **Accueil**, sans
changer son URL `/live/decouvrir` ni supprimer la découverte publique.
Depuis le correctif du **31 octobre 2026**, la navigation comporte quatre entrées,
dans cet ordre : **Accueil**, **Mes participations**, **Mes lots**, **Mes communes**.
**Mes lots** ouvre directement `/live/lots` avec son propre titre de page et
remplace le sous-onglet du carnet. La destination reste active dans le détail
d'un bon ; les URL personnelles et les accès enregistrés sont conservés.
Découvrir présente les animations publiques **En ce moment** et **Prochainement**.
Une fiche montre titre, commune, dates, description, conditions et action autorisée.
Sa présentation sert l'entrée dans le jeu : type d'animation, **Votre défi** et
action de participation précèdent les textes détaillés. Pour un passeport
explicitement identifié, un objectif de validations positif configuré est mis
en chiffres ; tombola et chasse conservent des invitations adaptées à leur type.
Un type inconnu reste générique. Aucun avancement personnel, classement ni gain
n'est déduit de cette fiche publique. Les compteurs de `dynamique` connus sont
accompagnés de pictogrammes, avec une mention de dotation totale pour les lots.
Les récompenses et adresses participantes restent consultables avec leurs liens
existants. Description, conditions et règlement sont accessibles dans des volets
ouvrables, avec raccourcis depuis l'en-tête. Les actions d'inscription, de reprise
et de récupération gardent leurs autorisations et leur contexte de provenance.
Les cartes et l'en-tête de fiche reprennent exclusivement l'image personnalisée
configurée dans **Flyer**, lorsqu'elle existe et que le serveur l'autorise.
Sans image, après retrait ou si elle ne charge pas, le contenu reste lisible
sans illustration de remplacement ni colonne vide. La couverture du jeu et
les illustrations de ses étapes ne servent pas de repli. Voir le
[contrat Flyer](flyers-contextualises.md#règles-de-conception-et-contrats).
L'inscription réutilise le formulaire existant sous `/live/animations/:id/inscription`.
Les participations et lots personnels conservent leurs accès dans le carnet.

Harmonisation du **3 novembre 2026** : la page personnelle ouverte par
**Commencer mon parcours** ou **Reprendre mon parcours** reprend les surfaces
arrondies, pictogrammes et commandes de retour/actualisation de Live. Le titre,
le nombre réel d'étapes terminées et la qualification fournie par le serveur
forment un aperçu commun ; l'étape active et son action précèdent les options.
**Mon inscription** et **Messages de l'organisateur** sont des volets secondaires
accessibles au clavier. Une décision de consentement non confirmée ouvre
automatiquement son volet, y compris après rechargement, sans renvoi implicite.
L'adresse absente reste explicitement indiquée dans le volet d'inscription.
Les thèmes configurés du jeu et des étapes restent prioritaires ; sans couleur
de surface explicite, leur fond sert de repli pour préserver le contraste.
Le scan du lieu, le QR personnel, le PIN, les gains et la satisfaction gardent
leurs composants et autorisations. Aucun score ni illustration fictifs ajoutés.

Complément du même jour : l'actualisation utilise une icône seule, placée sur
la même ligne que le titre (participations, parcours, bon et en-têtes existants).
Sa cible tactile reste de 44 px, avec nom accessible, infobulle, focus visible
et état de chargement. Le titre peut revenir à la ligne sans repousser l'icône
en dessous. Les actions explicites de réessai après erreur gardent leur texte.

Conception mobile d'abord : écran de référence 320–390 px, pas de débordement
horizontal, champs à 16 px, actions tactiles d'au moins 44 px, navigation à portée
du pouce et marge de sécurité PWA. Pas d'accueil marketing avant les tâches.
États de chargement, vide, erreur, stockage refusé et réseau indisponible explicites.
Le clavier, le focus, le texte agrandi à 200 % et la réduction des animations
restent utilisables. Les libellés de navigation peuvent revenir à la ligne.

Précision UX mobile du **31 octobre 2026** : Live privilégie les interactions
et la progression réelle. Sur la fiche publique, l'action principale unique
(inscription ouverte ou accès aux participations existantes) reste accessible
pendant le défilement sur téléphone, au-dessus de la navigation basse. Sa
position suit la hauteur réelle de cette navigation, y compris avec du texte
agrandi ; un espace est réservé pour accéder au bas de la page. Sur un écran
de faible hauteur, l'action reste dans le flux pour préserver la lecture.
Les raccourcis vers lots, adresses et conditions précèdent les informations
détaillées. La récupération est nommée **Retrouver mon inscription**, distincte
de l'inscription ; les accès personnels et le contexte de provenance sont conservés.

L'accueil conserve une priorité dominante et deux suivantes compactes, avec
anneaux, étapes restantes et actions de reprise. Un raccourci **Les défis locaux**
permet de rejoindre le programme sans parcourir ces priorités. Le résumé
**Mes communes** affiche son compteur puis **Choisir une commune** : les liens
individuels et la modification se déplient à la demande, sans repousser le
catalogue derrière dix communes. La sélection initiale, lorsqu'elle est vide,
conserve la recherche et la géolocalisation volontaire.

**Mes lots**, complété à la demande du **3 novembre 2026**, réunit désormais
les **coffrets, bons numériques et lots libres** gagnés via les participations
auxquelles l'installation possède un accès personnel valide. Cette demande
remplace la restriction antérieure aux seuls bons enregistrés sur l'appareil.
Les gains à utiliser, activer ou retirer et les gains en préparation précèdent
l'historique replié **Déjà utilisés ou retirés**, qui contient aussi les lots
expirés, annulés, refusés ou remplacés. L'état provient du serveur : un coffret
envoyé ne vaut pas coffret consommé, une remise libre doit être explicitement
déclarée, une qualification ne vaut pas attribution.

Pictogrammes par nature, compteurs des éléments affichés, cartes de récompense
et actions larges permettent une lecture rapide. **Nouveau** signifie que le
gain n'a pas encore été consulté sur cet appareil ; le clic sur sa consultation
ou l'ouverture de ses consignes mémorise seulement son identifiant localement.
Ce repère ne vaut ni retrait, ni consommation, ni écriture métier. Il reste
indépendant de l'état serveur et n'est pas affiché sur les gains historiques.

Les bons ajoutés localement restent visibles même sans suivi de participation.
Ils portent **Dernier état connu**, vérifié à l'ouverture du bon exact. Une
attribution serveur et un bon local de même identifiant ne sont affichés qu'une
fois, avec l'état serveur prioritaire. La liste ne délivre aucune capacité
personnelle : sans accès au bon enregistré, **Voir mon lot** reprend la
participation personnelle et son parcours existant. Le stockage du carnet
et la récupération par e-mail restent explicites.

**Mes prochains tirages** présente uniquement les participations explicitement
qualifiées par le moteur, dans le périmètre autorisé et encore en attente de
tirage selon la projection serveur. Aucun classement ni chance de gain n'est
inventé. Le modèle actuel ne prévoit pas de date de tirage planifiée :
**Date à annoncer** est affiché, sans utiliser la date de fin de l'animation
comme date de tirage. Les résultats gagnés ne sont jamais déduits d'un parcours
terminé à 100 %.

Gains et tirages possèdent des paginations indépendantes. Les compteurs restent
ceux des éléments affichés, sans promettre un total global. Une page de
tirages filtrée peut être vide tout en offrant une suite. Une panne laisse
les bons enregistrés accessibles et propose un réessai explicite, sans effacer
le carnet. L'actualisation garde son icône dans la ligne du titre.

La recherche ajoute ou retire des communes sans changer les inscriptions. Une
commune partagée par URL constitue un contexte de consultation : son ouverture
ne modifie pas silencieusement les communes suivies. Le suivi exige une action.

**Mes communes** privilégie les repères graphiques : nombre de communes suivies
sur ce navigateur, pictogramme de localisation, nom, code postal disponible et
état de suivi. Chaque commune propose **Voir les animations**, avec un retrait
secondaire nommé explicitement pour les lecteurs d'écran. Recherche et
**Autour de moi** sont regroupés ; les détails d'utilisation de la position
restent accessibles à la demande. Le compteur ne représente ni un nombre
d'animations ni un score : la borne reste de dix communes. Aucune carte, photo
ou statistique territoriale n'est inventée. La même présentation sert la page
dédiée et la sélection initiale intégrée à Découvrir, avec états vide et erreurs.

## Audit d’usage du 1er novembre 2026 — habitant peu familier du numérique

L’audit expert parcourt la découverte, le choix d’une commune, l’inscription,
la reprise d’un accès personnel et les lots sur téléphone. Il conserve le Live
immersif existant : repères visuels et actions de participation avant les
explications secondaires. Il ne constitue pas un essai avec de vrais habitants.

| Situation | Obstacle constaté | Comportement corrigé |
| --- | --- | --- |
| Recherche de commune indisponible | « Réessayez » sans moyen de relancer le même texte | Bouton **Réessayer la recherche**, saisie conservée et aucune sélection automatique |
| Lien communal invalide | **Choisir une commune** efface le contexte sans ouvrir le choix lorsque des communes sont déjà suivies | Accès réel à **Mes communes**, sans modifier la sélection enregistrée |
| Programme vide après sélection | Le bandeau demande encore de choisir une commune | Chargement, vrai vide et indisponibilité distingués ; **Modifier mes communes** sur le vrai vide, réessai sur panne |
| Détail personnel en panne | Le retrait du carnet est l’action proposée dans l’erreur | **Réessayer** reprend le même accès ; conservation locale expliquée, retrait secondaire dans les options |
| Fiche publique ouverte directement | Le retour aux animations mène au carnet personnel | Retour par défaut à la découverte ; provenance et retour contextuel existants prioritaires |
| Navigation avant inscription | **Mes participations** apparaît active sur une fiche publique | Fiche et inscription restent rattachées à **Accueil** ; les accès personnels, ajouts au carnet et lots conservent leur rubrique |
| Retrouver une inscription | Titre « Ajouter une inscription » et nouvelle inscription en concurrence avec la récupération | Titre **Retrouver mon inscription**, e-mail et action principale uniques ; nouvelle inscription sous **Pas encore inscrit ?** |
| Suite de récupération par e-mail | Étape suivante peu explicite | **Vérifiez votre boîte e-mail**, courriers indésirables, ouverture du dernier lien puis ajout au carnet ; réponse conditionnelle conservant la confidentialité |
| Inscription refusée ou non confirmée | Champs requis peu explicites et erreur éloignée du focus ; action identique avant/après réponse incertaine | Quatre champs obligatoires annoncés, notifications **Facultatif**, erreur focalisée, **Réessayer la même inscription** sans nouvelle clé ni modification du corps conservé |

Principes retenus : une tâche et une action principale identifiables, mêmes
termes que la navigation, textes courts donnant une prochaine action réelle,
saisies préservées après erreur et retrait séparé de la reprise. La fermeture
rend le focus au déclencheur ; **Utiliser une autre adresse** revient au champ
e-mail. Mobile, clavier et texte agrandi restent utilisables. Le GPS et
l’installation de l’application restent facultatifs ; aucun compte habitant
ni nouvelle étape de connexion n’est ajouté.

L’interface possède ces corrections de présentation. Règles d’inscription,
participations, consentements, tokens et contrats restent dans leurs producteurs
existants ; aucune donnée ni migration n’est créée. Les preuves locales et les
limites de l’audit figurent dans le [suivi d’implémentation](suivi-implementation.md).

## Audit d’usage du 2 novembre 2026 — continuité et actions

Cette passe suit le parcours d’un habitant : choisir une commune, découvrir
une animation, s’inscrire, reprendre son parcours et consulter un lot. Elle
complète l’audit précédent, sans remplacer les règles de participation. La
lecture des sources est complétée par des parcours navigateur isolés sur mobile
et PC ; il ne s’agit pas d’un essai auprès d’habitants réels.

| Priorité | Obstacle observé | Correction |
| --- | --- | --- |
| Haute | Retour de fiche perdant le filtre communal et la position de lecture | Provenance transmise par les cartes et la vedette ; retour à la commune consultée, restauration de la position et du focus lorsque le résultat est chargé. Le passage par l’inscription conserve cette provenance. |
| Haute | « Voir le détail » cache la reprise du jeu, derrière le QR | Action personnelle principale **Commencer mon parcours**, **Reprendre mon parcours** ou **Voir ma participation**, selon les données disponibles ; présentation du QR conservée séparément. |
| Haute | Détail personnel sans adresse, retour navigateur quittant la liste | Ouverture avec `?participation=` pour l’accès exact ; actualisation et historique du navigateur conservent la destination. Retour à la liste avec position et focus mémorisés temporairement. |
| Moyenne | Actualisation par icône seule ou boutons différents, sans retour visible dans le jeu | Composant commun avec icône et **Actualiser**, libellé accessible contextualisé, état **Actualisation…** et bouton désactivé pendant la lecture. Saisie de jeu conservée ; aucune commande métier rejouée. |
| Moyenne | « Mes animations », « carnet » et « Mes participations » désignent la même destination | **Mes participations** pour la destination ; composant de retour commun aux fiches, parcours et bons. « Carnet » reste utilisé pour expliquer la conservation locale. |
| Moyenne | « Ajouter une autre inscription » ouvre une récupération | **Retrouver une autre inscription**, distinct de l’action de nouvelle inscription. |
| Moyenne | À 200 % de texte, l’actualisation comprime le titre et les actions coupent leurs mots | En-tête et boutons passent sur des lignes distinctes lorsque la largeur manque ; le nombre dans l’anneau reste sur une ligne. |

L’esprit jeu repose sur les défis, les anneaux de progression, les lots et les
indicateurs réellement disponibles. Les appels publics emploient **Découvrir
l’animation** ; les actions personnelles disent ce qui va se passer. Une courte
apparition d’écran, sans déplacement des commandes, accompagne la navigation ;
elle est désactivée lorsque les mouvements sont réduits. Les contrôles conservent
une cible tactile de 44 px et un focus visible.

Les deux compléments de cet audit sont traités :

- La présentation vedette + carte compacte a été remplacée le 3 novembre par
  une seule carte complète par animation, pour libérer le premier écran.
  Le visuel Flyer, le défi et les compteurs restent dans cette carte ; le
  bandeau communal présente uniquement le contexte et l'aperçu des périodes.
- Au retour d’une fiche, les pages supplémentaires déjà consultées sont relues
  depuis l’API, avec ses curseurs courants, avant de restaurer position et focus.
  Le retour explicite, le retour navigateur et le rechargement dans la fiche
  conservent ce parcours. Seuls les repères de navigation (communes/périodes,
  nombre de pages, position et lien) sont mémorisés, pour dix entrées d’historique
  au maximum dans la session du navigateur ; aucune réponse du catalogue ni
  donnée personnelle n’est mise en cache par ce mécanisme.

Une erreur de pagination conserve les pages fraîchement obtenues et propose une
reprise des pages manquantes. Si l’animation a disparu du catalogue courant, le
focus revient au titre du programme. **Actualiser** et le changement de sélection
communale repartent de la première page. Le stockage indisponible conserve le
retour dans la session ouverte ; après rechargement, la provenance transmise
par le lien reste utilisable pour le retour explicite.

Impacts : présentation et navigation Marketplace/Live, documentation E73 ;
aucun contrat API, règle métier, droit, migration, paramètre d’exploitation ou
générateur modifié par ce correctif UX. Les images restent celles configurées,
les données personnelles et les consentements gardent leur traitement existant.
Les résultats et les limites de vérification figurent dans le
[suivi d’implémentation](suivi-implementation.md).

## Contre-audit du 2 novembre 2026 — validation du nouveau parcours

Cette revue expert contrôle l’arbre local Marketplace `bb8b585` complété des
correctifs UX précédents. Elle combine des scénarios navigateur isolés, des
captures et une lecture indépendante des parcours. Les API sont simulées :
elle ne valide ni le site TEST déployé ni l’usage avec de vrais habitants.

**Bilan :** le parcours courant est plus cohérent : quatre destinations stables,
actions de découverte/reprise distinctes, récupération d’inscription explicite,
carte vedette allégée et retour aux pages déjà parcourues. La nouvelle passe ne
remet pas en cause ces acquis. Elle a identifié les huit points ci-dessous.
L’audit initial ne modifiait pas le code ; leur prise en compte a ensuite été
demandée et implémentée dans le correctif décrit après ce tableau.

| Priorité | Constat et nature | Traitement recommandé et preuve attendue |
| --- | --- | --- |
| Haute | **Action masquée au clavier.** Dans Découvrir, Tab peut placer le focus sur un bouton derrière la navigation basse. Reproduit à 390×844 et 568×320 ; la capture montre l’action entièrement recouverte. | Réserver la zone visible lors du défilement vers le focus, en tenant compte des barres haute/basse et des actions fixes. Rejouer la tabulation complète, texte agrandi et écran bas ; le contrôle focalisé doit rester visible. Sources : `live.css`, `live-play-shell.css`, navigation commune. |
| Moyenne | **Animation disparue au retour.** Si l’animation de page 3 n’existe plus dans les réponses fraîches, le titre du programme reçoit le focus mais l’ancien scroll est conservé, loin du titre. Défaut reproduit. | Restaurer l’ancienne position seulement si le lien d’origine existe ; sinon montrer réellement le programme et expliquer son actualisation. Source : `LiveDiscovery.jsx`, effet de restauration. |
| Moyenne | **QR réaffiché par l’historique.** Détail → retour liste → Présenter mon QR → Avancer navigateur → Retour : la fenêtre QR réapparaît sans nouvelle action ni lecture. Défaut reproduit, sans preuve d’accès non autorisé. | Fermer la fenêtre et invalider sa lecture lors du changement de destination personnelle, tout en conservant les pages de la liste. Vérifier Back/Forward et absence de réouverture automatique. Source : état `qr` de `LiveAnimations.jsx`. |
| Moyenne | **Consigne contradictoire sur une fiche déjà enregistrée.** Lorsque l’enrichissement personnel manque, « Dans mon carnet ✓ » et « Ouvrir mes participations » peuvent coexister avec « Ajoutez-la au carnet ». Défaut rédactionnel reproduit. | Donner priorité à la présence locale pour la consigne ; garder une récupération distincte pour une autre inscription. Vérifier les combinaisons inscription connue, accès local et lecture d’enrichissement indisponible. Source : pied de fiche de `LiveAnimationDetail.jsx`. |
| Moyenne | **Panne de Mes lots sans réessai.** L’échec de lecture du carnet affiche une aide e-mail, mais aucune commande pour réessayer sur place. Lacune de récupération observée. | Ajouter une action de réessai à la lecture locale, sans effacer le carnet ; tester refus transitoire puis réussite et refus persistant. Source : `LiveLots.jsx`, lecture initiale. |
| Moyenne | **Portée de Mes lots ambiguë.** La liste contient les bons numériques enregistrés, alors que le vide dit « Retrouvez ici vos lots gagnés ». Les autres gains restent dans la participation ; le renvoi est caché sous l’aide e-mail. Optimisation de compréhension, pas un défaut du contrat de gains. | Préciser simplement « Vos bons enregistrés sur cet appareil » et rendre visible l’accès aux autres récompenses dans Mes participations. Ne pas déplacer ni dupliquer les gains sans évolution fonctionnelle distincte. Source : états vide/liste de `LiveLots.jsx`. |
| Basse | **Deux chemins au premier choix de commune.** Sans commune suivie, un bouton ouvre Mes communes alors que la recherche est déjà présente dans l’accueil. Optimisation de fluidité ; aucun blocage. | Faire du bouton un raccourci vers la recherche intégrée, avec focus dans le champ, puis garder Mes communes comme destination de gestion. Sources : `LiveCommunityScene.jsx` et `LiveDiscovery.jsx`. |
| Basse | **Repères de navigation invalides.** Une entrée de session volontairement corrompue avec `pages:{}` provoque un écran d’erreur ; Actualiser reproduit l’échec. Robustesse démontrée sur donnée injectée, pas défaut constaté en usage nominal. | Valider et ignorer les repères invalides, puis repartir de la première page. Tester structure erronée et stockage indisponible sans perdre les accès personnels. Sources : `liveDiscoveryNavigation.js`, `LiveDiscovery.jsx`. |

**Prise en compte des huit points :**

- Un traitement commun de la tabulation ajuste uniquement le défilement
  nécessaire pour révéler le contrôle devant les barres réellement visibles.
  Il mesure le conteneur extérieur même dans le formulaire d’inscription,
  respecte les actions fixes et celles dans le flux sur écran bas, et laisse
  les dialogues natifs ou ARIA gérer leur propre navigation. Les focus de
  retour programmatiques restent indépendants de ce traitement.
  Le piège de focus commun inclut les dialogues natifs ouverts et les éléments
  dépliables. L’inscription Live n’exécute plus la restauration différée de la
  marketplace, qui pouvait ramener en haut un formulaire déjà parcouru au clavier.
- Lorsque le lien d’origine n’est plus présent, focus et défilement reviennent
  ensemble au titre du programme ; une explication signale l’actualisation.
  Les repères de navigation sont validés depuis la session comme depuis l’état
  de l’historique, limités aux champs utiles et ignorés si leur structure est
  invalide. Ils ne remplacent jamais la lecture des données courantes.
- Tout changement de destination personnelle ferme le QR et invalide sa lecture
  en cours. Une nouvelle présentation explicite reste possible ; les pages de
  la liste et les accès personnels sont conservés.
- La présence locale prime dans la consigne de fiche : **Cette animation est
  enregistrée sur cet appareil. Retrouvez-la dans Mes participations.** Ce texte
  reste juste pour un ancien signet, sans promettre un accès personnel absent.
- Mes lots précise les bons numériques locaux, expose le lien vers les autres
  récompenses et permet de réessayer sa lecture. La réponse d’un écran quitté
  est ignorée ; le bouton est désactivé pendant la nouvelle lecture.
- Sans commune suivie, **Choisir mes communes** place le focus dans la recherche
  déjà affichée et la rend visible, sans changer de page. Si cette recherche
  n’est pas présente, notamment dans un contexte de lien communal invalide,
  le choix ouvre la page Mes communes.

Les tests et captures du correctif complètent les preuves initiales dans le
suivi. Le contrôle du focus s’appuie sur le principe de
[focus non entièrement masqué du W3C](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).
Les largeurs réduites sont examinées selon le principe de
[redistribution du contenu](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html),
sans prétendre à un audit exhaustif de conformité WCAG.

Les preuves, commandes et résultats distincts sont consignés dans le
[suivi d’implémentation](suivi-implementation.md). Aucun arbitrage métier,
contrat API, droit, migration ou générateur ne change dans cet audit.

## Nouvel audit du 2 novembre 2026 — après les huit corrections

Relecture depuis le point de vue d’un habitant, sur l’arbre local intégrant les
huit corrections précédentes. Le périmètre comprend la découverte, les communes,
les inscriptions et leur récupération, les participations, les lots et les
interactions de jeu. Les résultats exécutés sont consignés dans le
[suivi de réalisation](suivi-implementation.md#2-novembre-2026--nouvel-audit-live-après-les-huit-corrections).
Cet audit ne modifie pas le code de production et ne vaut pas recette du site déployé.

Le parcours courant conserve ses améliorations : une entrée directe dans les
animations, des actions de participation distinctes de la récupération, un carnet
unique et une navigation utilisable au clavier avec les barres fixes. Les huit
points précédents restent corrigés dans les scénarios rejoués. Aucune nouvelle
refonte visuelle générale n’est justifiée par les observations de ce passage.

Trois points restent à traiter, dans l’ordre recommandé :

| Priorité | Observation reproduite | Conséquence pour l’habitant | Optimisation proposée |
| --- | --- | --- | --- |
| P2 — lien personnel | Un lien personnel est validé (200), puis la lecture du contact échoue (503). L’écran « Garder ma participation » n’affiche que l’erreur, sans réessai. Une recharge après rétablissement du service fonctionne. | Une personne arrivant depuis son e-mail peut croire que son inscription ou son lien est invalide. | Ajouter **Réessayer la vérification**, un état occupé et une explication rassurante ; garder les contrôles d’accès et ignorer les réponses tardives. |
| P2 — commune partagée | Après un 503 sur la lecture de la commune passée en URL, **Actualiser** ne refait pas cette lecture. Le message invite pourtant à réessayer. Une recharge du navigateur conserve le filtre et réussit. | L’action proposée ne permet pas de reprendre ; changer de commune paraît être la seule solution. | Relancer aussi la commune lors de l’actualisation ou proposer **Réessayer cette commune**, sans modifier les communes suivies. |
| P3 — visibilité de l’incident personnel | Avec six animations publiques, l’avis d’échec des priorités personnelles commence à environ 3 126 px du haut sur un écran 390 × 844. Le bouton d’actualisation est en haut, sans réessai à proximité de l’avis. | L’accueil paraît normalement chargé alors que les défis personnels ont disparu temporairement ; il faut parcourir le catalogue pour comprendre. | Afficher un avis compact près de l’emplacement des défis personnels, avec réessai et accès au carnet, tout en laissant la découverte disponible. |

Ces défauts de reprise ne démontrent ni perte de données ni inscription dupliquée.
Les deux premiers ont un contournement par recharge de page ; le troisième
conserve l’accès à **Mes participations** dans la navigation. Les captures et
comptages de requêtes distinguent les observations des recommandations. Les
tests exploratoires constatant un défaut ne sont pas comptés comme une preuve
de conformité de ce comportement.

## Critères ajoutés et preuves

Les numéros 01 à 12 reprennent les CA1 à CA12 fournis par l'utilisateur.

| Critère | Résultat observable et preuve attendue |
| --- | --- |
| E73-EVO-LIVE-01 | Catalogue et détail consultables sans compte, y compris sans carnet local ; aucune permission personnelle déduite de la consultation. |
| E73-EVO-LIVE-02 | Recherche et sélection de plusieurs communes, persistance locale, modification et stockage refusé ; aucun compte nouveau selon l'arbitrage confirmé. |
| E73-EVO-LIVE-03 | Deux périodes, seuls résultats publics retournés par le producteur, pagination et état vide permettant de modifier les communes. |
| E73-EVO-LIVE-04 | Fiche vers inscription ou participation, même contexte d'animation et code de diffusion ; conservation des mécanismes d'accès existants, aucun nouvel écran de connexion fictif. |
| E73-EVO-LIVE-05 | Même participation et historique après reprise volontaire du carnet, sans création de compte, doublon métier ou effacement de l'origine. |
| E73-EVO-LIVE-06 | `/live/decouvrir?commune=<UUID>` partageable ; `/live/animations/:id` et anciens liens personnels fonctionnels. |
| E73-EVO-LIVE-07 | Domaine HTTPS dédié, même backend, accès directs et actualisation ; vérification DNS/TLS et hébergée distincte des tests locaux. |
| E73-EVO-LIVE-08 | Anciens liens personnels et QR conservés ; aucune redirection globale des capacités ni utilisation du secret d'installation d'une autre origine. |
| E73-EVO-LIVE-09 | Ancien catalogue et `surface=animations` quittent l'interface marketplace, contexte commune/animation conservé ; reprise du carnet proposée avant sortie d'origine. |
| E73-EVO-LIVE-10 | Navigation Animation de la marketplace vers Live ; parcours Coffrets et anciens `/live/*` conservés. |
| E73-EVO-LIVE-11 | Découverte, communes, inscription et carnet utilisables à 320/390 px et en PWA ; safe-area et accès au clavier. |
| E73-EVO-LIVE-12 | Recette de bascule : domaine, lecture anonyme, inscription, reprise des accès, historique, redirections et non-régression Coffrets. Aucune mise en service déclarée sur la seule base d'un build. |

## Complément UX du 30 octobre 2026 — E73-EVO-LIVE-UX

Retour utilisateur après la première version : supprimer le rappel de marque
au-dessus de Découvrir, clarifier son icône et conserver **Mes communes** comme
unique écran de gestion. Les anciens accès Réglages `?focus=city` ouvrent cet
écran ; les réglages de carnet et notifications restent disponibles. Leur
ouverture ne remplace ni ne synchronise implicitement une commune par défaut.

La découverte présente la dynamique et le défi de chaque animation, en priorité
mobile, sans faux classement, probabilité de gain ou activité simulée.

| Critère ajouté | Comportement attendu |
| --- | --- |
| E73-EVO-LIVE-UX-01 | Marque conservée dans l'en-tête, sans rappel dans le contenu Découvrir ; boussole et libellé Découvrir, repère cartographique pour Mes communes ; suppression du raccourci icône redondant de la surface Animation. |
| E73-EVO-LIVE-UX-02 | Recherche et modification des communes dans Mes communes ; aucun second sélecteur dans Réglages ; catégories de notification et Push conservent exactement les communes choisies, y compris une sélection vide. |
| E73-EVO-LIVE-UX-03 | Cartes avec l'image personnalisée du Flyer si disponible, sinon sans illustration : statut serveur, défi configuré s'il existe, nombres publics de participants, gagnants et unités en dotation. Zéro confirmé distinct d'une valeur inconnue ; ancien backend compatible sans compteurs. |
| E73-EVO-LIVE-UX-04 | À 320/390 px, pas de débordement, liens tactiles et données lisibles ; texte agrandi, clavier et réduction des mouvements préservés. |

Contrat additif catalogue/détail : `dynamique` avec `nombre_participants`,
`nombre_gagnants`, `nombre_lots_a_gagner`, entiers non négatifs ou valeurs
inconnues nulles. Participants = inscriptions présentes, tous statuts confondus,
selon le compteur métier existant. Gagnants = participants disposant d'une
attribution courante, hors suppléants et attributions remplacées ; pour les lots
libres, le tirage doit être confirmé, selon les projections de bilan.
Lots = nombre total d'unités de la dotation, pas nombre de catégories de lots,
ni stock restant. Cette portée est indiquée sur la carte. Aucune identité,
capacité personnelle ou donnée de contact n'est publiée.

Le backend fournit cette projection de lecture groupée pour la page publique
autorisée ; aucun appel par carte et aucun calcul métier côté interface. Le
frontend omet les valeurs absentes, négatives ou non entières sans les convertir
en zéro. Le défi reprend le nombre de validations configuré sans fabriquer une
progression personnelle. Les compteurs sont ceux de la lecture, sans promesse
de mise à jour en temps réel. L'ancien champ `nombre_lots` reste compatible.

Impacts : backend et contrat OpenAPI documentaire additifs, consommateur Live
et fixtures adaptés ; pas de migration, nouveau compte, permission, commande
métier, tâche, fournisseur ou configuration DNS. Les données de démonstration
existantes alimentent les mêmes lectures ; pas de génération réelle nécessaire.
La validation hébergée et les mesures PostgreSQL de volumétrie restent distinctes
des tests isolés. Les preuves sont consignées dans le suivi d'implémentation.

## Évolution du 30 octobre 2026 — E73-EVO-LIVE-ACCUEIL-RAPPELS

Demande acceptée : un accueil personnel mobile et deux rappels personnels
facultatifs, pour terminer un parcours et agir avant sa fermeture. Cette
évolution remplace le premier onglet Découvrir par **Accueil**, conserve ses URL
et le catalogue public et étend le périmètre antérieurement exclu des nouveaux
rappels personnalisés. Aucun compte habitant n'est créé. L’EPIC 73 restait alors
**En cours** ; les critères et preuves historiques ne sont pas réécrits.

### Parcours et décisions retenues

**US-LIVE-ACCUEIL.** En tant que participant, voir immédiatement les parcours
proches de leur objectif ou de leur échéance et reprendre le bon accès personnel.
Depuis le correctif UX du **31 octobre 2026**, l'accueil ouvre sur le défi personnel
prioritaire lorsqu'il existe, afin de rendre son action visible dès l'arrivée
sur mobile. La vie des communes suivies vient ensuite, ou ouvre l'accueil en
l'absence de priorité : accroche contextualisée, animation à rejoindre avec l'image
personnalisée du Flyer si disponible, nombre réel de participants à cette
animation et accès directs aux périodes. Les nombres d'animations sont ceux
de l'aperçu chargé, dédupliqués par période ; pagination et erreurs sont
signalées comme un aperçu partiel. Aucune somme d'habitants uniques, activité
instantanée ou illustration par défaut n'est inventée. Une indisponibilité
totale propose de réessayer ; le vrai vide propose de modifier les communes.

Une priorité personnelle principale et deux suivantes compactes sont présentées
avant le programme communal. Un raccourci **Mes défis à reprendre**
dans l'en-tête y mène directement, même sur mobile. L'accueil ne présente plus
de section **Mes autres participations**, de pagination ni de liaison des accès.
Le lien **Toutes mes participations** rejoint `/live/animations`.
Cette page réunit le carnet local et les participations liées à l'installation,
avec déduplication par identifiant exact de participation ; deux inscriptions
à la même animation restent distinctes. Depuis le correctif UX du **1er novembre
2026**, elles apparaissent dans une seule liste : aucun bloc **Mes accès liés**
ni compteur technique vide. Les accès distants absents du carnet
proposent **Retrouver mon inscription**, qui ouvre le formulaire e-mail existant sans
créer ni substituer un token. Une entrée importée sans accès utilisable propose
aussi une récupération explicite ; elle ne permet pas de présenter un QR.

**Mes participations** reprend les images Flyer disponibles, les pictogrammes,
les anneaux et les étapes validées/restantes. Les nombres du carnet portent sur
les entrées présentes sur l'appareil, sans fabriquer un total global à partir
d'une page distante. Les gains et qualifications
conservent leurs statuts serveur, indépendamment du pourcentage. Une progression
absente ou incohérente n'est pas représentée par un anneau à zéro. La pagination
distante remplace la page précédente, au plus 50 éléments par page ; les anciens
accès se relient uniquement sur action explicite, par lots de 50 et avec deux
requêtes concurrentes au plus. Un échec de synchronisation laisse le carnet
local utilisable, avec ses informations conservées et l'état d'erreur visible.
Une unique action **Actualiser mes participations**, lorsqu'il existe des
participations ou une lecture à reprendre, recharge la liste et propose la
liaison explicite des anciens accès utilisables. Un lot supplémentaire reste
une action volontaire **Actualiser les participations suivantes**. Aucun
rattachement n'est déclenché par le simple affichage de la page.
La pagination distante conserve les entrées locales ; ses commandes restent
disponibles même lorsqu'une page entière est déjà présente dans le carnet.
Le vide d'accueil n'est présenté qu'après confirmation de l'absence de résultats,
jamais pendant le chargement ou à la suite d'une erreur de lecture distante.
Sur l'accueil, **Actualiser** recharge participations et catalogue, avec annulation des
anciennes lectures et sans parcourir toutes les pages implicitement.
Les visiteurs sans carnet disposent d'abord de la découverte. La navigation
comporte quatre entrées : Accueil, Mes participations, Mes lots, Mes communes.

Complément graphique du **31 octobre 2026** : privilégier l'image du Flyer en
pleine largeur plutôt qu'un grand panneau de texte. Limiter l'ouverture à un
titre local, une animation et des repères chiffrés avec pictogrammes et libellés.
La progression personnelle prend la forme d'un anneau chiffré, accompagné du
nombre d'étapes validées et restantes ; elle ne vaut ni qualification ni gain.
Les descriptions et conditions des cartes restent accessibles dans **En bref**,
sans être tronquées ; la fiche complète et son inscription restent accessibles.
Sans image configurée, conserver la présentation structurée sans illustration
de remplacement. Les pictogrammes d'interface restent décoratifs pour les aides
techniques ; les valeurs, libellés et noms accessibles portent l'information.

Sur l’**Accueil**, les communes suivies prennent la forme d’une seule ligne
**Choisir une commune**, avec pictogramme et nombre de communes suivies. Elle
se déplie pour afficher les noms complets et les accès individuels, puis
**Modifier mes communes**. Consulter une commune ouvre son contexte partagé
sans changer la sélection. Les dix choix restent accessibles sans défilement
horizontal, y compris avec des noms longs et du texte agrandi. Sans commune
suivie, conserver la recherche et la géolocalisation volontaire existantes.

La direction visuelle de Live est un **espace de jeu local** : navigation basse
en dock avec destination active contrastée, défi personnel sur surface sombre,
anneau et étapes restantes au premier plan, action de reprise ou de récupération
explicite. Chaque carte du programme associe le Flyer configuré, le type de jeu et les
compteurs disponibles à une action **Découvrir l’animation**. La fiche expose
ensuite l’action autorisée selon le statut et les règles du serveur. Les cartes mettent l'objectif et l'action avant
les textes détaillés. Passeport, tombola et chasse utilisent les mêmes libellés
de type dans l'accueil, le catalogue et la fiche ; seul un passeport explicite
présente un objectif public de validations. Les participations disposent de
surfaces distinctes pour lire leur progression et accéder à leur QR.

Cet habillage est limité à la surface Animation et conserve les parcours
Coffrets. La sensation de jeu repose sur les objectifs configurés et les
progressions réelles, sans points, classement, compte à rebours ni activité en
temps réel inventés. Les mouvements accompagnent l'entrée ou l'action ; le
réglage de réduction des animations les supprime. Les textes restent complets
à 200 %, les cibles tactiles et les marges de sécurité PWA sont conservées.

Le **centre de notifications** reprend la typographie, les couleurs, les
pictogrammes et les actions arrondies de Live. Les catégories et dates précèdent
le titre, l’animation éventuelle et le message complet. Les mentions **Non lue /
Lue** restent lisibles sans dépendre d’une couleur ou d’une baisse d’opacité.
Le compteur concerne uniquement les messages affichés, y compris après
pagination ; il ne prétend pas donner le total distant. La fermeture reste
accessible pendant le défilement et le dialogue est nommé dès son ouverture,
y compris depuis `/live/messages`. Chargement, absence de nouvelles, erreur et
pagination conservent leurs états explicites. Consulter le centre ne marque
aucun message comme lu et ne demande pas de permission Push ; la lecture d’un
message, le marquage des messages affichés et leurs destinations gardent les
commandes existantes. Ce composant partagé reste utilisable sur Live Coffrets.

Un parcours est « presque terminé » s'il est commencé, encore accessible et
incomplet, avec une étape restante ou une progression confirmée d'au moins 80 %.
Le nombre requis provient de l'objectif métier effectif, jamais du nombre de
commerces disponibles. « Derniers jours » signifie une échéance effective de
participation dans les 72 heures à venir, encore strictement future, avec des
étapes manquantes et une participation encore autorisée. Les deux indications
peuvent coexister sur une seule entrée. Une progression inconnue ou une erreur
de lecture ne devient pas zéro, une urgence ou une qualification.

Les priorités de la page sont triées : deux indications réunies, fin proche,
presque terminé, autres parcours ; puis échéance la plus proche et identifiant
stable. La page annonce explicitement une suite lorsqu'elle est partielle ;
aucun compteur ou classement global n'est déduit d'une page. Deux inscriptions
distinctes à une même animation gardent leurs accès et progressions distincts.
Le même identifiant de participation n'est pas présenté plusieurs fois.

**US-LIVE-RAPPELS.** En tant que participant, choisir deux rappels automatiques
indépendants, distincts des campagnes organisateur et sans quota commercial :

- **Mes parcours presque terminés** : une étape réellement restante sur un
  parcours commencé ; le seuil d'affichage de 80 % ne déclenche pas ce Push.
- **Mes animations qui se terminent bientôt** : échéance effective dans
  les 72 heures, participation encore possible, objectif incomplet.

Une participation terminée, annulée, inaccessible ou dont l'accès est révoqué
ne reçoit pas de rappel. Un parcours achevé en attente de régularisation ou
de qualification n'est pas réinterprété comme des étapes restant à jouer.
Les neutralisations et adaptations du parcours suivent les projections métier
existantes. Une qualification ou un gain reste exclusivement confirmé par le
backend ; le pourcentage ne les accorde pas.

Un seul rappel logique de chaque type par participation et installation,
avec au plus un rappel personnel par jour civil et installation. Les deux
types d'une même participation sont fusionnés ; plusieurs participations
éligibles peuvent être regroupées dans ce rappel quotidien. Aucun troisième
rappel à 24 heures n'est ajouté. La purge de la boîte de réception ne réarme
pas les rappels. Les doublons de transport éventuels réutilisent le même tag.

La préparation et l'envoi sont limités à **09 h incluses–20 h exclues, heure
de Paris**, avec gestion des changements été/hiver. Les états, préférences,
liens de suivi et échéances sont revérifiés juste avant l'envoi. Une attente
hors créneau ne prolonge pas le droit de participer ni une échéance dépassée.
Le transport peut répéter une remise après un incident réseau ; l'unicité
garantie porte sur le rappel logique et sa réservation durable.

Les préférences `RAPPEL_PRESQUE_TERMINE` et `RAPPEL_FIN_PROCHE` sont
**false par défaut**, y compris pour les installations existantes. Elles se
gèrent séparément dans Réglages ; ni l'inscription ni l'ouverture de l'accueil
ne demande la permission navigateur. Un refus de Push ne bloque pas l'accueil,
les participations ou la messagerie. Les catégories et communes antérieures
sont préservées. La préférence des campagnes organisateur reste indépendante.

### Architecture et contrats

Le domaine `animation_locale` possède la politique de priorisation et de rappel.
Il consomme la progression du moteur, ses preuves et son calendrier effectif ;
il ne dépend ni de l'ORM, ni du navigateur, ni du fournisseur Web Push.
L'application charge les faits, contrôle les accès et orchestre les transactions.
Le repository borne les lectures et écrit les réservations ; les interfaces
présentent les décisions, sans recalculer les seuils métier en JavaScript.

Lecture additive : `GET /public/localeo-live/installations/{id}/tableau-de-bord`,
avec `X-Localeo-Live-Secret` et `Cache-Control: private, no-store`. La réponse
expose `generated_at`, `items`, `count` de la page et `next_cursor`. Chaque item
contient `participation_id`, `animation_id`, `nom`, `commune:{id,nom}`, `type`,
`statut_participation`, `date_fin`, `progression:{total,validees,restantes,pourcentage}`,
`commencee`, `terminee`, `disponible`, `indicateurs:{presque_terminee,fin_proche}`
et un `deeplink`. La page est bornée à 50 participations, sans parcours exhaustif
implicite des pages ou chargement global préalable en mémoire. Seuls les suivis
autorisés de l'installation authentifiée sont consultables, même hors catalogue
public. Aucun token, e-mail, identité ou solution privée n'est exposé.

Le lien commun est `/live/animations?participation=<UUID>` : il ouvre uniquement
l'entrée locale portant cet identifiant. Un carnet absent propose la reprise
de l'accès ; aucune autre participation à la même animation n'est substituée.
Un digest de plusieurs participations ouvre Mes participations.

Les anciens suivis ne prouvent pas quel token personnel a été validé. Une
migration ajoute la référence nullable au token effectivement présenté, sans
rattachement historique heuristique. Le tableau et les rappels exigent une
capacité encore valide ; la réponse distingue les accès à actualiser par
`acces_a_actualiser` (indicateur entier 0 ou 1, sans comptage exhaustif). Depuis
le carnet local, l'action explicite **Actualiser mes participations** relie les
participations avec leurs propres tokens existants,
par lots de 50 et deux requêtes concurrentes au plus. Les échecs partiels sont
visibles. Ni nouveau token, ni inscription, ni autorisation de rappel ne sont
créés par cette opération ; un token révoqué reste refusé.

Les deux catégories sont ajoutées au contrat de préférences existant. La
configuration publique expose `rappels_participations_disponibles: true` ; un
ancien backend sans ce champ conserve ses réglages et son catalogue. Un tableau
indisponible conserve les accès du carnet et propose une actualisation, sans
simuler l'absence de participations.

La préparation utilise un traitement batch protégé, borné, simulable par défaut,
destiné à un passage toutes les 15 minutes. Un curseur durable ou explicitement
reprenable évite de retraiter indéfiniment les premières installations. Les
réservations installation/jour et participation/type sont atomiques, uniques et
indépendantes de la rétention de l'inbox. Le verrou d'installation coordonne
préférences et rappels concurrents. La notification réutilise l'outbox et les
claims de transport existants, sans nouvelle intégration fournisseur.

### Critères et preuves attendues

| Critère ajouté | Résultat observable et preuve prévue |
| --- | --- |
| E73-HOME-01 | Accueil de jeu local : priorité personnelle et action visibles d'abord sur mobile, trois priorités au maximum, puis vie des communes suivies ; visiteur sans priorité vers découverte et participation publique. Image Flyer seule, aperçu partiel explicite, accès aux périodes, type de jeu cohérent et compteurs à pictogrammes. Autres participations et pagination sur Mes participations ; navigation et anciens liens conservés. |
| E73-HOME-02 | Indicateurs calculés par le domaine, frontière 80 %, une étape, 72 h, commencement et objectif effectif ; inconnus et états terminaux exclus. |
| E73-HOME-03 | Tri explicite, absence de doublon par participation, plusieurs accès à la même animation indépendants, pagination et état partiel. |
| E73-HOME-04 | Secret d'installation, refus croisé, aucune donnée sensible et aucune réponse personnelle mise en cache ; ancien backend et erreurs explicites. |
| E73-HOME-05 | Reprise exacte depuis l'accueil ou Push, accès absent sans substitution, parcours terminés/qualification/gains conservés. |
| E73-HOME-06 | 320/390 px et bureau, clavier, cibles tactiles, texte agrandi, mouvements réduits ; aucune nouvelle permission automatique. |
| E73-ALERTE-01 | Deux préférences opt-in indépendantes, défaut false neuf/existant, retrait effectif sans altérer les autres catégories ou communes. |
| E73-ALERTE-02 | Une étape restante pour le Push, fin dans 72 h, fusion des deux types et regroupement de participations ; aucun rappel après terminaison. |
| E73-ALERTE-03 | Un type/participation/installation et un rappel/jour, deux workers concurrents, rollback, purge inbox, reprise après incident sans doublon logique. |
| E73-ALERTE-04 | Créneau Paris 09–20, été/hiver, expiration pendant attente, revalidation préférences/accès/progression juste avant transport. |
| E73-ALERTE-05 | Batch borné, simulation sans écriture/envoi, progression du curseur, fournisseur simulé ; recette réelle distincte. |

| Impact | Décision et preuve à produire |
| --- | --- |
| Backend / API / batch | Domaine pur, lecture privée, catégories additives, registre durable, refus et concurrence ; tests isolés et PostgreSQL jetable. |
| Marketplace / Live | Accueil et réglages, mêmes carnet/communes ; contrats et parcours Playwright sur API simulées. |
| ERP / Animation / Pro | Pas de nouvel écran ni de commande : les nouvelles fonctionnalités sont destinées aux habitants dans Live. |
| Données / migration | Migration additive du registre et des index, anciennes préférences sans opt-in implicite ; restauration et introspection du générateur à examiner. |
| Documentation / exploitation | Contrat canonique, guide Live, batch, cadence, limites de transport et ordre backend avant frontend à actualiser. |

Budgets locaux : page de 50 suivis maximum, aucun enrichissement HTTP personnel
par carte, deux lectures frontend concurrentes au plus, préparation de 100
installations maximum par lot et absence de transaction englobant l'envoi réseau.
Les tests vérifient les bornes, accès/index et reprises ; les mesures hébergées
de latence et de charge mixte restent une vérification d'activation distincte.
Les preuves locales exécutées et les limites de recette hébergée sont consignées
dans le [suivi d'implémentation](suivi-implementation.md), sous la référence
**E73-EVO-LIVE-ACCUEIL-RAPPELS**. Elles ne clôturent pas toute l'EPIC 73.

## Invariants, contrats et conservation

Le backend reste propriétaire de la visibilité publique, des dates et autorisations
d'inscription, des progressions, attributions, consommations et historiques.
L'interface groupe les projections existantes et n'accorde aucun droit supplémentaire.
Réutiliser `fetchPublicAnimations`, `fetchPublicAnimation`, `searchVilles`, le
formulaire d'inscription et les contrats de participation existants. Aucun nouveau
contrat OpenAPI n'est annoncé pour une association à un compte inexistante.

Le catalogue est borné : au plus dix communes suivies et deux lectures concurrentes,
pagination indépendante par commune et période, détection des curseurs répétés,
annulation des anciennes recherches et déduplication par animation. Une erreur
partielle ne devient pas un résultat complet vide. Ces bornes d'interface ne
constituent pas une mesure de capacité serveur ; avant activation, mesurer sur
1 puis 10 communes les requêtes, latences, volumes et erreurs en charge mixte.
Budget cible de navigation : interactions locales immédiates, état de chargement
visible sans attendre la dernière commune ; les résultats restent consultables
si une autre commune échoue. La tenue en charge hébergée reste à prouver.

Le carnet est en IndexedDB par origine. Un DNS ne peut pas migrer ce stockage.
Conserver `/live/reprise-carnet` sur l'ancien domaine : export privé puis import
volontaire sur le nouveau, validation et fusion transactionnelles existantes,
mêmes identifiants et capacités, sans nouvelle inscription. Aucun token ajouté à
une URL de transition. L'ancien carnet reste présent. Les anciens liens personnels
restent servis lorsque leur redirection ne peut préserver l'accès sans risque.

## Impacts et ordre de livraison de la bascule initiale

Ce tableau concerne **E73-EVO-LIVE-UNIQUE**. Le complément Accueil/Rappels
ci-dessus ajoute ensuite une migration backend, un contrat de lecture et un
traitement batch ; son ordre de livraison et ses impacts priment pour ces ajouts.

| Périmètre | Impact et vérification |
| --- | --- |
| Marketplace / Live | Routes, navigation, découverte multi-communes et sélection locale, inscription sous scope `/live/`, transition de l'ancien catalogue ; tests Node et navigateur mobile/bureau. |
| Backend / ERP / batchs | Aucun changement de règle, schéma ou commande métier prévu ; mêmes endpoints publics et privés. Les liens générés continuent à être acceptés par les routes de compatibilité. |
| Portail Animation / Pro | Aucun nouveau parcours métier ; liens publics et QR existants conservés. Les origines publiques dédiées déjà prévues restent applicables. |
| Données / migrations | Pas de migration SQL ni duplication de participation ; reprise locale du carnet explicite. Pas de synchronisation de compte ou de secret d'installation entre origines. |
| Démonstration | Réutiliser communes, animations et participations synthétiques existantes ; adapter les scénarios de navigation, sans régénérer des données réelles. |
| Exploitation | Deux services publics conservés, même API ; DNS/TLS du service Live, cache et PWA, maintien des anciens accès et reprise de carnet avant retrait de toute ancienne origine. |

Préparer le bundle et ses tests, déployer le même backend compatible et le frontend
Live sur TEST, configurer le domaine dédié et vérifier TLS. Contrôler ensuite les
douze parcours et la reprise du carnet avec un utilisateur de recette. Mettre à
jour les liens marketplace et générés après cette vérification. Ne pas retirer
l'ancien hébergement des accès personnels ni sa page de reprise du carnet.
Le repli conserve le même backend et les données ; rétablir le bundle précédent
et ses origines sans effacer de carnet. Un service worker précédent doit toujours
permettre l'ouverture des anciens accès. Commit, push et déploiement sont séparés.

## Suivi des preuves

Les résultats réels et limites sont consignés dans le
[suivi d'implémentation](suivi-implementation.md). Les 130 scénarios historiques
de [recette métier](recette-metier.md) conservent leurs statuts ; cette évolution
ajoute ses propres parcours de bascule et n'est pas validée par leurs anciens succès.

## Audit du 3 novembre 2026 — accueil recentré sur les animations

Référence **E73-UX-ACCUEIL-ALLEGE**, complément de E73-HOME-01 et de la
continuité habitant. L'audit expert porte sur l'arbre local et des parcours
navigateur synthétiques ; il ne constitue pas un test auprès d'habitants réels.

| Priorité | Obstacle | Présentation retenue |
| --- | --- | --- |
| Haute | Le grand bloc « Ça se passe à… » repousse le programme et répète la première animation | Bandeau communal compact, compteurs des périodes chargées ; une seule carte par animation, avec son Flyer réel. |
| Haute | Recherche et filtres occupent l'accueil avant toute intention de recherche | Loupe nommée dans le header, panneau ouvert volontairement, saisie focalisée ; fermeture clavier et bouton explicite vers les résultats. |
| Haute | La sélection des communes ajoute un bloc avant les animations | Une ligne dépliable avec compteur et mêmes liens, sans changer les communes suivies. |
| Moyenne | Actions secondaires aussi présentes que l'accès à l'animation | Un bouton principal par carte ; « Pour plus tard » et « Partager » en pictogrammes nommés, cibles de 44 px et état de conservation explicite. |
| Moyenne | Des filtres fermés pourraient masquer des résultats sans explication | Résumé visible des filtres actifs, accès à leur modification et effacement avec restitution du focus. |

Les participations prioritaires, gains et messages conservent leur place.
La recherche reste limitée au programme chargé : ouvrir les filtres ne relit
pas le catalogue. Les pages supplémentaires, erreurs partielles, liens directs,
retours avec filtre/position/focus et types de jeu restent couverts. Les grands
textes ne sont pas tronqués et aucune image ou activité n'est inventée.

Impacts : frontend Marketplace/Live et documentation uniquement. Aucun contrat
API, invariant métier, droit, donnée de démonstration, migration ou paramètre
d'exploitation ne change. Une mise en service nécessitera la livraison du
frontend ; les résultats locaux sont consignés dans le suivi d'implémentation.


## Correctif du 3 novembre 2026 — entrées publiques et origine Live

Les liens publics d’inscription, flyers, QR, catalogue et confirmation tombola
utilisent l’origine dédiée configurée et les chemins `/live/animations/{id}`,
`/inscription` ou `/confirmation-email` selon leur fonction. L’inscription reste
absente lorsque le backend la ferme. Aucun changement des règles d’admission,
des participations ou de leurs accès déjà émis.

Sur l’ancien service Marketplace, `/live`, `/live/decouvrir` et les fiches ou
inscriptions publiques ouvrent le domaine Live configuré. Seuls les contextes
publics autorisés (animation, commune, source) sont repris. Les confirmations avec
secret, ajouts au carnet, participations personnelles, lots et reprise de carnet
restent sur leur origine. Un carnet non vide ou inaccessible propose sa sauvegarde
avant sortie ; aucun accès n’est transmis automatiquement entre domaines.
Les pages personnelles historiques partagent désormais l’habillage et l’en-tête
Live, tout en conservant les fonctions Coffrets nécessaires sur leur origine.

Constat sur TEST, en lecture publique : le 3 novembre, le service Marketplace
configurait encore son propre domaine comme destination des animations et l’API
renvoyait des chemins relatifs `/animations/{id}`. La
[procédure de configuration](../../exploitation/technique/configurer-epic-73.md#contrôle-des-liens-live-après-bascule)
détaille la valeur à corriger sur les services concernés. Cette observation ne
constitue ni une modification de configuration distante ni un déploiement.

Rattachement aux critères E73-EVO-LIVE-06/08/09/10/12. Contrats : mêmes champs et
paramètres, destinations publiques absolues ; aucune migration SQL ni réparation
de carnet. Les exemples de déploiement et le guide d’exploitation sont mis à jour.
Les tests utilisent des données synthétiques, sans email réel ; la production des
supports de démonstration reprend le même producteur de liens.


Preuves de ce correctif, bases backend `931cef4`, Marketplace `9be43e9` et
documentation `87b6da6`, avec modifications locales :

- Backend : 4 reproductions en échec avant correction (mail de confirmation,
  publication et projections résumé/détail), puis **225 tests ciblés réussis**
  via `scripts/validation/test_isolated.py` : 110 tests des services/API et
  115 tests de transport, CORS et profils. Le détail des nouveaux cas figure dans
  `tests/application/services/test_liens_publics_animation.py`,
  `test_flyer_animation.py` et `test_catalogue_animations_publiques.py` du backend.
  Contrôles d’architecture, classes de domaine et couverture des use cases :
  **637 succès**.
- Frontend : trois reproductions navigateur échouaient avant correction
  (/live sur ancien domaine, inscription sans changement d’origine, habillage
  historique différent). Les tests de routage et conservation des accès
  (`live-entry-routing.test.cjs`, `animation-surface-satisfaction.test.cjs`) :
  **7 succès** ; ESLint des fichiers modifiés : réussi.
- Playwright avec build isolé sans `.env`, API simulées :
  `live-entry-redirects.spec.cjs` et `live-animation-surface.spec.cjs`, **18 succès** ;
  `e74-tombola-email.spec.cjs`, **12 succès**. Les parcours vérifient ouverture
  directe/actualisation, contexte public, carnet conservé/exporté/repris,
  anciens accès Coffrets et confirmation tombola. Capture mobile de l’habillage
  historique inspectée, sans débordement horizontal.
- Deux assertions historiques cherchaient encore « Mes lots » parmi les onglets
  du carnet et des onglets Animation retirés : comparaison avec
  `HEAD:src/live/LiveCarnetHeader.jsx` confirmant cette divergence déjà présente.
  Elles vérifient maintenant l’entrée dédiée dans la navigation principale,
  l’absence de doublon et les liens Coffrets conservés. Une fixture HTML de
  redirection a aussi reçu son charset UTF-8 ; assertions de destination conservées.
- Revue indépendante ciblée des producteurs et consommateurs : aucun écart
  bloquant identifié, aucune migration implicite de capacité ou d’origine.
- Vérification documentaire : 98 guides, 1 124 liens locaux, zéro erreur ou
  avertissement ; 134 sources exportées vérifiées ; `git diff --check` réussi
  dans les trois dépôts modifiés.

Aucun commit, push, déploiement, email réel ou changement distant de configuration
réalisé dans cette phase. Les variables Animation de suivi/actualités restent à
aligner selon les exemples de déploiement ; l’origine Coffrets reste indépendante.

## Correctif du 5 novembre 2026 — QR participant à l’ouverture

Suivi : [ANO-MPL-E73-LIVE-04](../../roadmap/anomalies/marketplace.md#ano-mpl-e73-live-04--qr-participant-accessible-avant-le-début).
Cette correction précise l’action personnelle des critères E73-EVO-LIVE-04/05/08/11 ;
elle ne rouvre pas l’epic et ne modifie ni inscription ni éligibilité au tirage.

**Invariant :** l’accès personnel et l’inscription peuvent être consultés avant
l’animation, mais le QR de validation commerçant ne peut être présenté hors de
sa période autorisée. Début inclus, fin exclue et état compatible sont décidés
par `Animation.autoriser_scan` ; la préparation reste contrôlée par sa politique
existante. Les routes et la PWA ne recalculent pas les dates indépendamment.

Le détail personnel expose une capacité supplémentaire :

```json
{
  "presentation_qr": {
    "disponible": false,
    "motif": "ANIMATION_NON_DEMARREE",
    "ouvre_le": "2026-11-06T08:00:00Z"
  }
}
```

`motif` vaut `ANIMATION_NON_DEMARREE`, `ANIMATION_TERMINEE`,
`ANIMATION_INDISPONIBLE` ou null ; `ouvre_le` n’est fourni que pour le début futur
effectif. Une préparation non prête ne signifie pas automatiquement « à venir ».
L’ancienne `qr_url` reste présente et ne contient pas de token, mais les routes
`/public/localeo-live/participations/{id}/qrcode` et
`/public/animation-locale/participants/{token}/qrcode` refusent désormais la
génération non autorisée. Token, inscription et historique sont conservés.

Parcours :

- Carnet, passeport, tombola locale et chasse : action désactivée **Bientôt ouvert**
  avant le début, explication et date en heure de Paris lorsqu’elle est connue.
  L’utilisateur peut consulter sa participation ; aucun appel QR anticipé.
- À l’ouverture, une actualisation relit le serveur et permet l’action habituelle.
  L’horloge du téléphone ne décide pas du droit. Sans capacité (ancien serveur),
  repli prudent sur les états publics/jeu ; `PUBLIEE` et token seuls ne suffisent pas.
- Le chargement ne montre pas l’identifiant personnel. Un refus métier/accès du
  service QR ne déclenche pas le secours par code manuel ; actualiser la fiche.
  Les erreurs techniques restent distinctes des refus de période.
- Le lien e-mail `#qr` attend une lecture personnelle courante et ne contourne pas
  le refus. Une ouverture refusée n’est pas rejouée automatiquement à l’heure de début.
- Actualisation individuelle/globale, fermeture et navigation invalident les
  réponses QR retardées. La fenêtre dépend de la capacité courante, pas de la
  copie de participation au moment du clic.

Les QR de remise des lots (Coffrets/bons numériques), QR de lieu et d’inscription
restent distincts et inchangés. La tombola publique ne propose toujours pas de
QR commerçant. Les contrôles PIN déjà présents restent conservés.

Impacts : backend, PWA Live et schéma `ParticipationLivePayload` partagé. Le champ
est ajouté aux réponses ; le serveur actuel le produit toujours et la nouvelle
PWA accepte les anciens payloads. Les schémas fermés embarqués et empreintes
Marketplace, Animation et Pro sont alignés sur ce payload ; les deux modèles QR
des vues OpenAPI documentaires 41/42 et des consommateurs sont repris des exports
hors ligne. Les divergences historiques voisines (notamment CRM) ne sont pas
absorbées par cette correction. Aucun changement de version moteur de jeu,
migration SQL, donnée de démonstration, permission ou variable d’environnement.
Les fixtures synthétiques couvrent le nouveau DTO ; pas de génération sur TEST.

| Axe | Vérification locale et limite |
| --- | --- |
| Règle et API | `test_presentation_qr_participant.py`, `test_qr_participant_periode.py`, suites participants/préparation/PIN : 71 succès ; ancien comportement reproduit avec cinq refus manquants. Deux doubles historiques complétés, assertions conservées. |
| Contrats et projections | `test_contrats_moteur_t1.py`, `test_localeo_live_backend_api.py`, `test_projections_jeu_t4.py` : 34 succès ; modèles générés, empreintes et contrôles des consommateurs ciblés. |
| Architecture | Contrôles backend architecture, classes de domaine et couverture des use cases : 660 succès. |
| Présentation | Helpers QR, transport jeu et registre Marketplace : 13 succès ; ESLint ciblé réussi. Première campagne développement : 32 scénarios réussis (parcours, navigation et lots). Après revue : 17 scénarios réussis sur build de production isolé, dont dix QR (320/1280 px, ouverture, refus période/préparation, réponse tardive, actualisation globale et anciens liens e-mail) et sept de navigation. Aucun trafic métier réel ; les campagnes se recouvrent et ne s’additionnent pas. |
| Consommateurs | Animation : quatre tests registre/contrat publication réussis ; Pro : 34 tests contrats/registre réussis. Seuls les exports fermés et OpenAPI de ce payload changent dans ces deux dépôts, pas leur UI. |
| Données et exploitation | Aucun appel réel de QR/publication sur TEST et aucun envoi externe pour ce correctif ; pas de SQL ni migration. Livrer backend et PWA, avec contrats embarqués ; les anciens accès restent valides. Aucun déploiement attesté. |

## Commerçants partenaires — accès pratique depuis Live

Complément **E73-EVO-LIVE-COMMERCANTS**, demandé le **6 novembre 2026**, lié à
ANO-MPL-E73-LIVE-05. La clôture historique de l'epic reste conservée.

L'habitant doit pouvoir choisir où se rendre sans quitter Live pour le catalogue
Coffrets. L'entrée **Commerçants** apparaît à côté du titre de l'accueil, dans la
place déjà réservée à ses commandes ; la navigation basse à quatre entrées reste
lisible sur petit écran. L'annuaire dispose des entrées **Animations / Commerçants**.
Depuis une animation classique et son parcours personnel, **Les commerçants de
l'animation** ouvre directement sa liste filtrée. Les visites d'un passeport
proposent aussi **Adresse et horaires**.

| Critère | Comportement observable |
| --- | --- |
| LM01 | L'annuaire `/live/commercants` présente les commerçants actifs d'animations publiques en cours ou à venir, avec recherche par nom et filtre de commune. Une sélection explicite d'animation peut aussi consulter ses partenaires après clôture, si elle reste publiquement visible. |
| LM02 | `/live/commercants/:id` présente d'abord l'adresse, l'itinéraire et les horaires publiés, puis les animations publiques associées ; chaque animation rejoint sa fiche Live. Les contenus éditoriaux et informations d'accessibilité restent secondaires. |
| LM03 | Une adresse ou des horaires absents sont explicitement signalés. Aucune ouverture actuelle, distance, photo de remplacement, adresse ou donnée de contact n'est inventée. Les coordonnées opérationnelles ne deviennent pas publiques. |
| LM04 | Les filtres restent dans l'URL et le retour conserve le contexte animation, parcours ou liste. Après une erreur de page suivante, les résultats déjà chargés restent visibles et le réessai reprend cette page. Une réponse obsolète ne remplace pas un filtre plus récent. |
| LM05 | Aucun lieu futur d'une chasse n'est révélé par l'annuaire ni par le filtre commerçant du catalogue. La chasse conserve le lieu courant autorisé et son itinéraire ; aucune nouvelle fiche publique d'un lieu secret n'est créée. |
| LM06 | Sur mobile 320 px et bureau, les commandes restent accessibles et sans débordement horizontal. L'accès aux commerçants ne repousse pas la première action d'animation sous la navigation basse de l'accueil. |

### Contrat et responsabilité

Deux lectures sous `/public/animation-locale` :

- `GET /commercants` : filtres `commune_id`, `animation_id`, `q` (100 caractères
  maximum), `cursor` et `page_size` (25 par défaut, 100 maximum ; Live demande 12).
  Réponse `items`, `count` de la page, `pagination.page_size`,
  `pagination.next_cursor` et `has_more`. Aucun total global déduit du nombre chargé.
- `GET /commercants/{commercant_id}` : fiche d'un commerçant actif associé à une
  animation classique publiquement visible, y compris clôturée. Refus 404 hors
  de ce périmètre ; filtres facultatifs `commune_id` et `animation_id` conservés.

Chaque ligne expose `id`, `nom`, `adresse`, `commune`, `image_url` et
`horaires_texte`. La fiche ajoute `profil_publie`, `description`, `site_web_url`,
`acces_transport` et `accessibilite`. Ces contenus sont lus uniquement dans la
version publiée du profil. Aucun numéro de téléphone public n'existe actuellement
sur ce contrat : `contact_telephone`, destiné aux opérations, n'est pas utilisé.
Les liens de site acceptent HTTP(S) uniquement, sans identifiant intégré.

`ServiceCommercantsLive` compose une projection de lecture avec les prédicats
existants de `ServiceCatalogueAnimationsPubliques` : publication, commune,
abonnement, modèle, période et associations effectives, dont retraits acceptés.
Cette lecture SQL reprend la frontière du catalogue public existant ; elle ne
porte aucune nouvelle transition ni règle de validation. La règle de passage
reste dans le domaine et les accès QR conservent leur contrôle d'ouverture.
Le partage du prédicat commerçant évite une seconde règle d'appartenance.

La recherche et les associations sont filtrées en stockage. La pagination ordonnée
nom/identifiant charge au plus `page_size + 1` lignes, avec un curseur lié aux
filtres ; un curseur invalide est refusé en 422. Les profils sont joints dans la
même requête, sans requête par commerçant ni collecte exhaustive d'animations.
Les animations de la fiche utilisent le catalogue public existant filtré par
`commercant_id`, avec sa propre pagination.

### Impacts et vérification

- Backend et Marketplace/Live : nouvelle lecture et parcours. Sources OpenAPI
  documentaires E41/E42 et copies embarquées Animation/Pro synchronisées depuis
  l'export hors ligne, uniquement pour les deux routes et cinq modèles concernés.
  Aucun changement d'interface Pro ou Animation, ni du contrat moteur de jeu.
- Sans migration : les adresses et versions publiées existent déjà. Le générateur
  de démonstration n'a pas de nouveau champ obligatoire ; les preuves utilisent
  des fixtures synthétiques. Aucun jeu ni compte TEST modifié.
- Exploitation : livrer backend et PWA ensemble ; une API ancienne produit une
  indisponibilité explicite et un réessai, jamais une liste fictive. Aucune nouvelle
  variable, permission, tâche planifiée ou notification.
- Backend : 34 tests ciblés réussis, dont six scénarios PostgreSQL/HTTP réels sur
  une base locale jetable ; 660 contrôles d'architecture réussis. Rejeu final de
  deux scénarios de curseur mal typé et parité des filtres réussi, avec recouvrement
  de la campagne précédente. Un scénario supplémentaire vérifie une seule requête
  et au plus 26 lignes pour une page de 25 sur 102 commerces ; cette mesure locale
  ne constitue pas une recette de charge. Base jetable arrêtée après vérification.
- Présentation : `live-merchants.spec.cjs`, `live-home-density.spec.cjs` et
  `live-qr-opening.spec.cjs` couvrent 22 scénarios distincts. La première intégration
  repoussait l'action de l'accueil sous la navigation ; correction vérifiée sans
  affaiblir l'assertion. Dernières exécutions : 12 scénarios parcours/QR réussis,
  puis dix scénarios annuaire/accueil réussis après compaction. Build de production
  isolé, écrans 320/390/1280 px, captures mobiles et bureau, aucun trafic métier
  réel. ESLint ciblé réussi ; les cinq modèles et deux routes exportés concordent
  avec le générateur et leurs références se résolvent. Contrats consommateurs :
  quatre tests Animation et 34 tests Pro réussis. Les campagnes antérieures se
  recouvrent et ne s'additionnent pas.
- Limite : aucun succès distant ou déploiement TEST n'est déduit des preuves locales.

## Évolution du 7 novembre 2026 — adhésion habitant (E73-EVO-LIVE-ADHESION)

### Besoin, décision et portée

En tant qu’habitant, je veux comprendre immédiatement ce que je peux faire,
retrouver facilement mon parcours et ressentir mes progrès, afin de prendre
plaisir aux animations locales et de revenir lorsqu’un événement me concerne.

La demande du 7 novembre intègre les **13 recommandations A01 à A13** du
[rapport d’audit](../../audits/marketplace/localeo-live-adhesion-ux-ui-2026-11-07.md)
dans E73. Cette section est leur source de spécification, distincte du constat
daté d’audit. Le backlog canonique référence les critères **E73-LA-01 à 17**.
**État de l’évolution : trois lots implémentés localement, qualification de
charge LA-16 encore partielle ; preuves et limites au
[bilan](verification-livraison.md#réalisation-locale-de-lévolution).** La
[conception détaillée](localeo-live-adhesion-conception.md) fixe désormais les
contrats, les choix bornés de V1, les budgets et les tests des 13 recommandations.
La clôture historique d’E73 reste inchangée ; aucune preuve ancienne ne valide
ces nouveaux critères. Le périmètre ne modifie pas les règles des jeux.

Référence examinée : Marketplace/Live `e94201b`. L’audit du code et des scénarios
existants constitue le point de départ ; aucune recette visuelle connectée sur
TEST ni mesure d’adhésion n’est disponible. Le bénéfice attendu reste à mesurer.

Décisions de conception de cette évolution :

- **LA-D01 — Prochaine action** : étendre l’accueil personnel au parcours non
  urgent. Cela complète E73-EVO-LIVE-ACCUEIL-RAPPELS ; les deux indicateurs
  d’urgence existants restent décidés par le backend. Aucun nouveau rappel
  automatique n’est créé par ce changement d’ordre de présentation.
- **LA-D02 — Recherche complète** : remplacer, pour le programme public, la
  recherche limitée aux pages déjà chargées de LC11 par une recherche serveur
  paginée sur le périmètre sélectionné. Le filtre local reste adapté aux
  références « Pour plus tard » stockées sur cet appareil, sans les faire passer
  pour un catalogue exhaustif. LC11 conserve son identifiant et ses preuves historiques.
- **LA-D03 — Continuité sans compte** : guider e-mail, carnet et installation
  en réutilisant les mécanismes E42/E74 ; ne pas promettre une synchronisation.
  L’inscription directe E74 est conservée : le mail donne accès au suivi, il ne
  constitue pas une nouvelle étape de qualification.
- **LA-D04 — Ludique et utile** : valoriser les acquis confirmés, sans points
  fictifs, séries quotidiennes, classement social, urgence artificielle ni
  incitation à ouvrir l’application sans événement utile.
- **LA-D05 — Réemploi** : conserver les quatre entrées basses, la recherche en
  loupe, l’annuaire, les lots unifiés, l’agenda de tirage, les notifications,
  les retours et rafraîchissements partagés ; harmoniser leur orchestration.
- **LA-D06 — Options du rapport** : les 13 recommandations sont couvertes
  ci-dessous. La carte interactive, une récupération groupée par e-mail,
  la synchronisation multi-appareils, un score permanent et le partage d’un
  bilan personnel restent des pistes hors première réalisation. Le filtre
  « en famille » reste conditionné à une qualification explicite des données ;
  il ne sera pas déduit du modèle de jeu ou d’un texte libre.

### Critères complémentaires et parcours attendus

| Critère | Audit / priorité | Déclencheur et résultat attendu, y compris refus ou absence de donnée |
| --- | --- | --- |
| **E73-LA-01** | A01 / P1 | À l’ouverture de Mon Live, une participation disponible non terminée peut être proposée même sans indicateur d’urgence. Une seule action principale personnelle est mise en avant ; les autres restent accessibles sans répéter une grille complète. Un blocage opérationnel explicite concernant cette action est présenté avant elle. Sans accès personnel, proposer la récupération ; sans participation, présenter la découverte ; en erreur, conserver l’accès au carnet et ne pas annoncer un faux état vide. |
| **E73-LA-02** | A02 / P1 | Après succès confirmé d’une inscription tombola directe, montrer « Inscription enregistrée » et deux étapes visuelles pour retrouver le lien personnel puis ajouter au carnet. Le tirage n’est daté que si sa date publique est connue. Une réponse incertaine ou en cours ne devient pas un succès. Aucun token, donnée d’un inscrit préexistant, seconde chance ou nouvel e-mail n’est créé par le simple affichage de cet écran. |
| **E73-LA-03** | A03 / P1 | Depuis un carnet vide ou l’aide d’installation, « Retrouver mes participations sur ce téléphone » propose : lien disponible, lien perdu, changement de téléphone. Chaque choix utilise la récupération autorisée ou la sauvegarde existante. Import impossible, stockage refusé et accès expiré donnent une issue utile sans effacer le carnet existant ni réinscrire. L’installation est facultative ; aucune conservation inter-navigateurs automatique n’est promise. |
| **E73-LA-04** | A04 / P1 | Chaque carte de découverte présente nom, commune, période, promesse du défi et action principale ; au plus un indicateur de dynamique est mis en avant, les autres restent consultables dans la fiche. Favori et partage restent secondaires. La formulation concrète reflète la mécanique réelle : une validation n’est pas automatiquement une visite. Image du flyer seulement si configurée ; sinon pictogramme et composition graphique. Règlement, conditions et données complètes restent accessibles avant inscription. |
| **E73-LA-05** | A05 / P1 | Une recherche du programme trouve une animation publique autorisée même située au-delà de la première page, sans télécharger toutes les pages. Commune(s), texte, type et période sont filtrés côté serveur. « Aujourd’hui » et « Ce week-end » sont expliqués en dates de Paris. Les favoris ont un accès nommé visible lorsqu’ils existent, distinct des participations. Une animation devenue inaccessible est signalée à l’ouverture sans perdre silencieusement le favori. |
| **E73-LA-06** | A06 / P1 | Dans une participation, un indicateur de nouvelles ouvre la messagerie filtrée sur cette animation. Le non-lu ne disparaît pas par simple affichage d’un badge. Le parcours distingue accord organisateur, permission navigateur et préférences de rappels, avec des états compréhensibles et une modification volontaire. Le refus de push ne bloque ni participation ni messages autorisés dans Live ; aucune activation groupée implicite. |
| **E73-LA-07** | A07 / P2 | Une étape nouvellement confirmée déclenche un retour visuel bref, une progression exacte et la prochaine action autorisée. Un réaffichage, une réponse obsolète ou un reçu déjà traité ne rejoue pas une victoire comme un nouvel acquis. Mouvement réduit : équivalent statique. Sans résultat confirmé, aucune célébration ni progression supposée ; 100 % n’équivaut pas à une qualification. |
| **E73-LA-08** | A08 / P2 | Mes lots distingue utilisable/à retirer, nouveauté et historique pour Coffrets, bons numériques et lots libres externes. Chaque carte fournit l’action réelle : présenter le bon, ouvrir le coffret ou consulter les consignes de retrait. Lieu/échéance connus sont visibles avant les détails ; absence explicitée, date non inventée. Lots consommés, retirés, expirés ou révoqués ne sont pas promus comme utilisables ; un état ancien est revalidé à l’ouverture. |
| **E73-LA-09** | A09 / P2 | Une participation qualifiée montre le prochain tirage connu, l’agenda existant, le résultat lorsqu’il est publié et les nouvelles associées. Sans date, afficher « Date à annoncer ». Après résultat, proposer un prochain défi public dans les communes sélectionnées s’il existe, sinon un retour au programme. Réutiliser les notifications existantes et expliciter leur disponibilité, sans promettre ni envoyer un nouveau type d’alerte non pris en charge. |
| **E73-LA-10** | A10 / P2 | Accueil, découverte, fiche, parcours, lots, communes et messages partagent les mêmes styles de titre, actions, retour, rafraîchissement et états. Une couleur ou un pictogramme ne porte jamais seul une information métier. La personnalité locale vient des contenus publiés et de motifs/pictogrammes sobres ; aucun flux, nombre de présents ou visuel de lieu n’est simulé. Les styles partagés sont consolidés, sans empilement de surcharges par écran. |
| **E73-LA-11** | A11 / P2 | Depuis une étape ou un commerce connu et autorisé, l’habitant trouve adresse, horaires publiés, itinéraire et retour au même contexte de participation. Un lieu futur de chasse reste caché. Sans adresse/horaires, expliquer l’absence ; ne pas inférer « ouvert maintenant », distance ou temps de trajet. L’annuaire existant est réutilisé. |
| **E73-LA-12** | A12 / P2 | L’aide distingue inscription, jeu et retrait ; elle propose un contact d’organisation uniquement s’il est explicitement publiable et disponible. Sans contact public, conserver l’orientation vers les supports connus. Aucun téléphone privé de commerçant, membre d’équipe ou support interne n’est exposé ; aucun message n’est envoyé automatiquement. |
| **E73-LA-13** | A13 / P3 | Après fin d’animation, un bilan personnel compact présente les seuls acquis attestés, le résultat autorisé et l’avis facultatif existant, puis une suite locale pertinente. Ne pas assimiler non-gagnant à non-participant, ni absence de lot à résultat perdu. Si les faits nécessaires manquent, omettre la statistique ; aucune reconstitution narrative de lieux secrets. |
| **E73-LA-14** | Transverse / P1 | Aux formats 320 × 568, 390 × 844 et 1280 × 800, aucun défilement horizontal ; commande principale identifiable, cibles principales de 44 px minimum, focus visible et retour cohérent. Tester aussi zoom/texte à 200 %, clavier ouvert, lecteur d’écran et mouvement réduit. La navigation fixe ne masque ni champ focalisé ni action. |
| **E73-LA-15** | Transverse / P1 | Sur réseau lent, indisponible ou rétabli, distinguer chargement, données déjà connues, indisponibilité et vide réel. Annuler/ignorer une réponse devenue obsolète, préserver filtres et accès lors des retours, permettre un réessai explicite. Aucun POST métier rejoué automatiquement pour améliorer la fluidité ; aucun QR ou droit nouveau tiré d’un cache ancien. |
| **E73-LA-16** | Transverse / P1 | Les lectures ajoutées ou étendues respectent filtrage/pagination en stockage, bornes de page et de concurrence, absence de N+1 et isolation des accès. Les preuves de performance déclarent données, budgets, cache, trafic et saturation ; une mesure absente n’est pas un succès. Les scénarios avec plusieurs communes, participations, messages et lots simultanés complètent la fixture d’accueil simple. |
| **E73-LA-17** | Transverse / P2 | Le plan de mesure distingue découverte, inscription confirmée, ajout au carnet, reprise, étape, message et usage du lot. Les événements respectent la politique d’analytics et son consentement ; aucun e-mail, token, QR, identifiant personnel ou position précise ajouté. Une mesure de retour indique population et période réellement observables ; aucune fusion implicite d’appareils ni promesse de gain chiffré sans référence initiale. |

### Ordre de l’accueil et règles de présentation

Le bloc personnel est une aide à la décision, pas un nouveau moteur métier.
Ordre cible : information opérationnelle explicitement bloquante pour le parcours
concerné ; participation réunissant fin proche et presque terminée, puis fin proche
seule, puis presque terminée seule (ordre existant conservé) ; nouveau lot
encore utilisable ; participation ordinaire disponible à reprendre ; rendez-vous
de tirage qualifié. Au sein d’une catégorie, départager par échéance connue
croissante, puis identifiant stable ; une date absente vient après les dates connues.
Un lot déjà connu mais utilisable reste accessible par Mes lots et un signal
secondaire. Les indicateurs non prioritaires restent compacts ; l’habitant conserve
l’accès à toutes ses participations. Une information manquante ne crée pas d’urgence.
L’importance `URGENT` d’un message ne prouve pas un blocage et ne peut désactiver
une action de jeu. Le motif bloquant et la capacité refusée doivent provenir de
l’état ou de l’action autoritaire du moteur. La V1 exploite seulement les motifs
effectivement présents dans les lectures autorisées. Sinon, le message reste une
information mise en avant, sans changement de droits.

Cette hiérarchie précise la proposition ouverte de l’audit ; elle est une décision
de présentation de cette spécification, pas un constat du produit existant.
Les projections personnelles sont bornées : ne pas parcourir toutes les pages
du carnet distant pour choisir un gagnant de classement. **Décision LA-T01** :
50 suivis, 25 récompenses et 25 tirages au maximum dans les fenêtres initiales ;
classement uniquement sur ces candidats, « Parmi vos suivis chargés » si une
source est partielle/indisponible ou un accès local non lié. Pas de nouvelle
projection de classement global. Ne pas appeler cette sélection « dernière
activité ». Aucun nouvel historique de comportement personnel n’est requis.

Pour le catalogue, « Aujourd’hui » couvre la date civile courante à Paris.
« Ce week-end » couvre samedi 00:00 à lundi 00:00 ; samedi/dimanche, il s’agit
du week-end en cours, sinon du prochain. L’animation doit chevaucher cette fenêtre
et satisfaire les prédicats publics existants ; début inclus, fin exclue selon
les conventions des dates du catalogue. Le libellé présente les dates résolues.
Une période ne promet ni inscription ouverte ni commerce ouvert à cet instant.

### Propriétaires, contrats et compatibilité

Les règles de publication, scan et parcours restent dans le domaine Animation
et les politiques de moteur existantes. Les états de gain/remise restent dans
leurs propriétaires E73 ; les règles d’accès personnel et d’inscription restent
E42/E74. La présentation ne calcule ni qualification, ni validité de QR, ni
éligibilité à partir du pourcentage, des dates du téléphone ou d’un e-mail déclaré.
Les préférences et droits de communication existants gardent leur propriétaire ;
un nouveau point d’entrée UI n’autorise aucune campagne supplémentaire.

| Surface / producteur et consommateur | Réemploi et contrat cible détaillé dans la conception |
| --- | --- |
| Catalogue public : `ServiceCatalogueAnimationsPubliques` → client Live / LiveDiscovery | Le service sait filtrer en SQL mais la route/client ne l’exposent pas. LA-T02 retient une nouvelle route `/animations/recherche` sans total exhaustif, et un adaptateur Live dédié ; réemploi des prédicats publics, ancienne route inchangée. Paramètres, ordre, curseur et erreurs au §3.1 de la conception. |
| Tableau de bord : `ServiceTableauDeBordLive` → useLiveDashboard / LiveHome | Réutiliser progression, disponibilité, fin/résultat/date de tirage. Ordre actuel `ACTIVES_PUIS_HISTORIQUE_UUID` conservé ; classement local à la fenêtre déclaré selon LA-T01. Ni prochaine étape ni dernière activité ajoutées à ce DTO. |
| Participation / moteur / QR / PIN → jeu et commerçants | Réutiliser la prochaine action et les lieux déjà autorisés. Un DTO de prochaine action éventuel contient un identifiant et un contexte autorisés, jamais un lieu futur ni une règle réimplémentée. Les contrats moteurs fermés exigent alignement des copies embarquées si leur schéma change. |
| Messages / préférences → participation et messagerie | Filtre serveur par animation disponible ; nouvel indicateur booléen dédié par animation, basé sur EXISTS et mêmes accès, défini au §3.2. Pas de compteur global réinterprété. Publication, adaptation, clôture et résultat ont déjà des producteurs ; les réutiliser, ainsi que les rappels dédiés, sans doubler les envois. |
| Lots / tirages → Mes lots / accueil / bilan | `RecompenseLive` fournit nature, état, échéance, consignes, responsable et lien ; le détail du bon, sous accès personnel, fournit lieu de remise et actions disponibles. Ne pas produire un QR à partir du résumé. Le lot externe n’a pas d’adresse/échéance structurée : présenter les consignes existantes sans convertir le lot en bon ni extraire des droits du texte. |
| Contact de support public → aide Live | Nouveau contact facultatif dédié, publication explicite, sous-ressource de gestion versionnée et lectures publique/personnelle filtrées ; stockage et droits fixés aux §3.3/3.4. Aucun réemploi d’une coordonnée privée. Le repli sans contact ne remplace pas le développement du contact publiable. |
| Analytics → événements de parcours | Événements et enums fermés définis au §4.1 ; identité éphémère et collecte désactivée conservées. Pas de mesure de rétention inter-appareils ; tests transport désactivé/refus sans fournisseur réel. |

L’annuaire public exclut actuellement toutes les chasses. Pour LA-11, conserver
l’itinéraire du lieu déjà autorisé par le parcours ; une fiche plus complète de
ce lieu utilise la lecture personnelle dédiée du §3.4, pas le retrait de l’exclusion
de l’annuaire public. Le propriétaire moteur décide ce qui est révélé.

Les OpenAPI documentaires restent dans `localeo-projet` (E41/E42 et schémas
concernés), leurs générateurs dans le backend, les copies embarquées chez leurs
consommateurs. Aucun OpenAPI runtime n’est modifié par cette spécification ;
les contrats cibles précis sont dans la conception et devront être générés avec
leurs producteurs lors de l’implémentation. Live ancien et backend nouveau doivent conserver
leurs contrats existants ; un Live nouveau sur backend ancien désactive les
nouveaux filtres avec une explication, sans les ignorer silencieusement.

### Données, bornes et livraison

Le volet purement UI ne demande pas de migration : les inscriptions, gains,
consentements et carnets ne sont pas transformés. La table additive
`animation_contacts_publics` est requise. La recherche réutilise les index v276 ;
les mesures pourront imposer un index additionnel. Pas de migration des moteurs.
Le numéro de migration sera attribué au développement, sans modifier les SQL appliquées.
Les dates et doublons d’une navigation vivante doivent être traités explicitement.

Bornes de conception pour la recherche étendue : 10 communes sélectionnées au
maximum, texte 120 caractères au maximum, 12 résultats demandés par Live,
plafond serveur 50 conservé, lecture `limit + 1` racines et enrichissement groupé.
Curseur par clé lié aux filtres, à l’accès et à l’ordre total ; pas d’offset
profond, de chargement exhaustif ni de total global fictif. Deux requêtes de
catalogue au plus en vol dans Live ; recherche temporisée et requête précédente
annulée lors d’un changement de saisie. Cache LRU de 5 contextes, 5 pages de 12
par période et 120 cartes au maximum par contexte ; puis navigation par fenêtres
avec retour utilisable, selon la conception §3.1.

Pour les nouveaux chemins, les budgets p95/p99,
requêtes, mémoire/DOM et saturation sont fixés au §5 de la conception, selon
la [convention de performance](../../architecture/transverse/performance-volumetrie.md).
Ce sont des objectifs à mesurer, pas des résultats de conformité. Prévoir N/10N,
filtres rares/vides, première/page profonde,
caches froid/chaud et charge mêlant lecture, inscription et validation sur une
cible isolée. La revue documentaire ne remplace ni ces mesures ni les plans SQL.

Livrer le backend compatible et ses éventuelles migrations/readiness avant les
capacités Live qui en dépendent. Aucun nouveau flag, job, permission caméra,
permission push ou envoi n’est activé par ce document. Les composants UI
indépendants peuvent être livrés séparément après leurs tests. Le retour à un
ancien frontend doit conserver carnets et droits ; un stockage local additionnel
ne contient ni nouveau secret ni projection narrative. Les garde-fous du service
worker restent en place. Configuration, ordre exact et diagnostic de version
sont décrits au §4.3 de la conception et seront vérifiés dans le bilan à l’implémentation.

### Lots et matrice de traçabilité

Les critères transverses 14–17 s’appliquent à chaque lot concerné. La matrice
ci-dessous sert au suivi de cette évolution ; aucun registre concurrent n’est créé.
Cette matrice décrit les tests prévus ; leurs résultats réels et leurs limites
sont consignés au [bilan de réalisation](verification-livraison.md).

| Lot / critères | Propriétaire et comportement | Preuves prévues | Documentation / contrats | Fixtures / démonstration | Exploitation / état |
| --- | --- | --- | --- | --- | --- |
| **1 — Accompagner** : LA-01/02/03/04, accès favoris de 05, contextualisation existante de 06 | Live présente l’action ; domaine existant conserve inscription et droits. | Accueil non urgent/urgent/vide, trois participations + gain + message ; tombola succès/incertain/rejeu ; carnet absent/restauration refusée ; favoris ; retour et navigation mobile. Étendre les suites home, density, registration, recovery et messages existantes. | Cette section ; E74 inscription directe et E42 carnet par référence ; conception détaillée LA-T01. | Fixtures synthétiques sans compte réel, dont backend ancien, plus de 50 suivis et stockage refusé. Pas de génération TEST. | Fenêtres 50/25/25 et couverture partielle explicite ; aucune promesse de classement global. **Implémenté localement ; preuves et limites au bilan.** |
| **2 — Participer avec plaisir** : LA-07/08/10/11/12 | État confirmé par moteur/gains ; Live présente ; coordonnées uniquement publiées. | Succès vs reçu en cours, réponse tardive, mouvement réduit ; trois types de lots + révocation ; commerce connu/inconnu/secret ; aide sans contact public ; styles, clavier et zoom. | E73 dotation, LM01–06, E70 PIN préservés. Contact public versionné et lieu courant personnel définis au §3 de la conception. | États variés de lot, données absentes, chasse à lieux cachés, grand texte et image absente. Fixtures de contact et sauvegarde/restauration de la nouvelle table. | Migration additive contact public, droits ERP/Animation et readiness ; aucun nouvel envoi. **Implémenté localement ; preuves et limites au bilan.** |
| **3 — Revenir utilement** : recherche serveur LA-05, approfondissement 06, LA-09/13/17 | Catalogue et droits côté backend ; bilan personnel à partir des faits autorisés ; analytics soumis au choix existant. | Résultat au-delà de page 1, filtres/cursor invalides, intercommunes, bornes et plans SQL ; non-lu et refus push ; tirage sans date/perdant/gagnant ; bilan sans donnée ; absence d’analytics sans consentement. | Contrats cibles §3, budgets §5 et recette §6 de la conception. Générer OpenAPI et aligner les lecteurs lors de l’implémentation ; guides message/aide et configuration à actualiser. | N/10N et données étrangères, lettres accentuées, week-end/changement d’heure, résultats partiels ; fournisseurs simulés. | Contrats et attributs implémentés ; mesures courtes N/10N exécutées. **Qualification de charge LA-16 encore partielle.** |
| **Tous — LA-14/15/16** | Présentation, transport et adaptateurs ; domaine inchangé. | Navigateurs isolés aux trois dimensions, 200 %, réseau lent/refus, annulation des requêtes, confidentialité, droits révoqués ; tests API/DB réels pour lectures modifiées. | Sources canoniques, contrats embarqués et reader tests selon changements effectifs. | Aucun mail, push ou base partagé requis pour les tests automatisés. | Vérification de livraison distincte du pilote et des appareils physiques ; **non exécutée**. |

Les scénarios et mesures d’adhésion avec habitants du rapport sont un suivi
produit recommandé. Conformément à **E73-DEC-CLOTURE-TESTS**, ils ne remplacent
pas les tests automatisés et ne constituent pas une condition de clôture du
développement. Les limites de vérification d’une PWA sur appareil réel restent
déclarées avant activation ; aucun résultat externe n’est présumé.

### Préparation détaillée et preuve documentaire

La couverture fonctionnelle A01–A13 est intégrée. La demande de spécification
détaillée du 7 novembre fixe les choix LA-T01–07 dans la
[conception](localeo-live-adhesion-conception.md) : fenêtres d’accueil assumées,
recherche complète paginée, présence de messages, contact public dédié,
lieu courant autorisé, bornes, budgets et recette. Les options exclues ne
constituent pas des arbitrages cachés bloquant ce périmètre. La réalisation,
la migration et les contrats ont ensuite été développés dans les dépôts concernés.
Les résultats applicatifs figurent au [bilan](verification-livraison.md).

La phase de spécification seule ne lançait pas le développement. La demande
d’implémentation suivante du 7 novembre est suivie dans le
[bilan E73](verification-livraison.md) avec la référence E73-EVO-LIVE-ADHESION.
Elle n’autorise pas de migration TEST, campagne, commit, push ou déploiement.

Contrôles documentaires du 7 novembre 2026, base projet `7245005` et modifications
locales : couverture des **13 recommandations et 17 critères uniques** contrôlée
par extraction, liens locaux sans erreur ni avertissement, **148 sources exportées
vérifiées**, contrôle des espaces du diff réussi. Revue indépendante de contrats
en lecture seule : inventaire des écarts intégré ; ordre des indicateurs combinés
préservé et importance d’un message distinguée d’une capacité bloquante du moteur.
Ces résultats prouvent la cohérence documentaire, pas l’exécution des critères.

La revue de conception détaillée a également précisé l’indicateur de non-lu
après révocation, les permissions ERP de contact public, les codes de conflit
existants et les trois révisions nécessaires au lieu courant. Ces constats sont
intégrés dans les contrats et les scénarios de recette du complément technique.

## Évolution du 8 novembre 2026 — hiérarchie et fluidité (E73-EVO-LIVE-HIERARCHIE)

**Spécification puis implémentation locale demandées le 8 novembre.** Les huit recommandations
R01–R08 de l’[audit après déploiement](../../audits/marketplace/localeo-live-hierarchie-fluidite-2026-11-08.md)
sont couvertes ci-dessous et dans le §7 de la
[conception existante](localeo-live-adhesion-conception.md#7-hiérarchie-et-fluidité--e73-evo-live-hierarchie).
La clôture historique E73 reste inchangée ; LA-16 conserve ses réserves de
performance. Les preuves de l’évolution précédente ne valident pas celle-ci.

### Objectif et décisions

Habitant sans compte nouveau : comprendre immédiatement le territoire proposé,
repérer les animations ouvertes et futures, trouver les commerces, puis agir
sans perdre son repère pendant une actualisation. L’agrément repose sur la
composition, les vrais visuels et les réponses de l’interface ; aucun indicateur
d’activité, gain ou disponibilité n’est fabriqué.

- **LH-D01 :** contexte communal compact → une action personnelle si disponible
  → navigation Animations / Commerçants → programme En ce moment / Prochainement
  → aides secondaires. Le résumé autonome « Ça se passe… » est absorbé dans
  cette composition ; aucun bandeau supplémentaire n’est ajouté.
- **LH-D02 :** périodes distinctes par composition, pictogramme et accent ; mêmes
  libellés dans les raccourcis et les sections, sans grossissement général des
  textes. Couleurs et composants réutilisent la charte Live.
- **LH-D03 :** première lecture, revalidation et changement de contexte sont
  trois états différents ; une donnée conservée ne constitue aucun droit.
- **LH-D04 :** navigation basse à quatre destinations conservée. La navigation
  Animations / Commerçants remplace l’entrée compacte de l’accueil et reprend
  le même composant dans l’annuaire. L’aperçu optionnel de deux/trois commerces
  évoqué dans l’audit n’est pas ajouté à l’accueil : visibilité assurée par cette
  navigation, sans appel réseau ni bloc supplémentaire. Cette option est
  explicitement traitée, pas un préalable manquant aux huit recommandations.
- **LH-D05 :** seuls les flyers configurés illustrent les animations. Sans
  flyer, variante graphique compacte avec pictogramme, jamais photographie de
  remplacement. Photos réelles des commerces conservées dans leur propre vue.
- **LH-D06 :** correction de présentation des doublons d’adresse exacts, sans
  réécriture automatique des données TEST. Commune de participation et adresse
  postale ne sont pas assimilées. Noms de démonstration « TEST… » conservés.

Ces décisions précisent LA-01/04/10/14/15/16 et remplacent les attentes de
composition incompatibles, notamment le résumé autonome et les messages
d’attente multiples. Elles ne retirent aucun contrôle de droits, de fraîcheur,
de couverture partielle, de dates Europe/Paris ou de performance.

### Critères complémentaires et preuves prévues

La réalisation locale des critères **E73-LH-01 à E73-LH-12** est suivie dans le
[bilan](verification-livraison.md), avec les preuves et contrôles non exécutés.
Les références R désignent le rapport, les références LA l’évolution précédente.

| Critère | Source | Précondition, action et résultat observable |
| --- | --- | --- |
| **E73-LH-01** | Composition, R01/04/07 ; LA-01/10 | Ouvrir l’accueil avec/sans suivi personnel : ordre LH-D01, contexte communal lisible avant l’action, une seule action personnelle et aucune zone vide réservée durablement à une action inexistante. À 390 × 844, jeu nominal de titres courts et sans action personnelle : première proposition et CTA entièrement visibles au-dessus de la navigation basse ; avec action personnelle, son CTA est prioritaire. À 320 × 568, titres longs et zoom 200 %, tout reste atteignable sans troncature utile ni défilement horizontal. |
| **E73-LH-02** | R01 | Explorer les périodes : En ce moment et Prochainement possèdent un en-tête, un pictogramme et une séparation reconnaissables sans la couleur seule. Les raccourcis emploient ces noms, déplacent lecture et focus vers le bon titre sans masquage. Comptage des seuls résultats chargés, libellé de portée accessible, indication explicite de couverture partielle ; zéro n’est annoncé qu’après une lecture réussie. |
| **E73-LH-03** | R02 | Première ouverture sans données, réponse lente puis succès/vide/erreur : titre et cadre stables, ossature non interactive de la liste et une annonce accessible par zone indépendante. Aucun message de chargement répété dans un titre, une explication et une ligne supplémentaire. Le vrai vide et le zéro ne précèdent jamais la réponse. Erreur avec Réessayer, sans boucle de relance. |
| **E73-LH-04** | R02 ; LA-15 | Actualiser le même contexte ou revenir après 60 s : conserver la dernière lecture de cette zone, sa position et le focus ; indiquer une seule revalidation discrète. Au succès, remplacer atomiquement la fenêtre affichée selon la procédure bornée du §7.3 de la conception ; un élément effectivement retiré restitue l’ancre au prochain élément conservé, sinon au titre avec annonce. En panne, indiquer que les résultats conservés datent de la dernière réussite avec Réessayer. Les zones saines restent utilisables. Les contenus privés révoqués/refusés sont retirés immédiatement ; aucun QR ou acte métier n’est autorisé depuis une copie périmée. |
| **E73-LH-05** | R02 ; LA-05/15/16 | Changer rapidement commune, filtre, capacité, installation ou participation : résultats uniquement du contexte courant ; annuler les demandes dépassées et ignorer leurs réponses tardives. Une invalidation d’accès purge la zone privée. Focus/visibilitychange/clics concurrents ne dupliquent pas une revalidation. Curseurs restent attachés à leur contexte ; pagination invalide propose une reprise sans mélange ni boucle. |
| **E73-LH-06** | R03 | Depuis l’accueil ou l’annuaire, ouvrir Animations / Commerçants : même navigation à deux liens, état actif explicite, accès au clavier et zone tactile de 44 px. Conserver l’URL et le retour de la vue précédente ; la sélection des communes suivies n’est pas modifiée. Un filtre d’animation issu d’une fiche reste visible et retirable dans l’annuaire, sans exposer les lieux secrets. Aucun cinquième onglet de navigation basse. |
| **E73-LH-07** | R04 ; LA-04 | Lire une carte passeport, tombola ou chasse : titre/commune, promesse adaptée au moteur, période, un indicateur réel maximum, CTA Découvrir l’animation. L’effort est compréhensible avant le CTA ; aucun passage imposé à la tombola publique, aucun lieu secret révélé. Favori/partage sont secondaires, nommés et accessibles. Favori ne vaut pas inscription ; ouverture de fiche ne prétend pas lancer le jeu. |
| **E73-LH-08** | R05 | Lire des cartes avec flyer, sans flyer, image lente ou en erreur : visuel configuré uniquement ; variante sans photo avec pictogramme et accent cohérents. Le chargement/échec d’une image ne déplace pas les commandes de la carte déjà affichée. Aucun grand rectangle vide pour une animation sans flyer connu. Informations complètes accessibles même sans image. |
| **E73-LH-09** | R06 | Consulter et filtrer l’annuaire, ouvrir un commerce puis revenir : cadre, retours, recherche, rafraîchissement et navigation cohérents avec Live. Résultat compact nom/repère territorial, Horaires et animations et Y aller si adresse exploitable. Adresse complète dans le détail ; absence explicite d’horaires/adresse, pas de statut « ouvert maintenant » déduit de texte libre. Photos réelles ou pictogramme, résultats paginés et couverture affichée. |
| **E73-LH-10** | R06, qualité des données | Une adresse comportant des lignes logiques consécutives strictement identiques n’est présentée qu’une fois par ligne dans le détail ; casse et espaces normalisés pour comparer, ponctuation/signification conservées. Valeur source et destination d’itinéraire inchangées. Des segments différents ou une répétition à l’intérieur d’une même ligne ne sont pas supprimés. Ne jamais remplacer l’adresse par la commune de participation ; libeller ce rattachement distinctement. Si le doublon vient de la source, le diagnostic le consigne ; aucun correctif de données distant implicite. |
| **E73-LH-11** | R07 | Après une réponse vide réussie, Prochainement affiche un état compact et un seul lien Modifier mes communes ; aides de récupération secondaires, fraîcheur discrète. Une panne affiche un état d’erreur, pas une absence d’animation. Aucun horodatage de participation ni lien personnel redondant n’occupe l’accueil sans suivi connu ; une couverture incomplète reste signalée. |
| **E73-LH-12** | R08 ; LA-07/14 | Navigation, clic, retour de fiche et succès confirmé : retour visuel immédiat, transitions courtes, focus et position cohérents. Mouvement réduit supprime les effets non essentiels. Aucun carrousel automatique, clignotement ou célébration sur GET/refresh ; réussite uniquement selon reçu confirmé existant. Les contrôles et la navigation fixe ne masquent aucun CTA ciblé au clavier. |

### Matrice des responsabilités et impacts

| Critères | Propriétaire / contrat | Recette cible ; résultats de réalisation au bilan E73 | Documentation / fixtures / exploitation |
| --- | --- | --- | --- |
| LH-01/02/06/07/08/11/12 | Marketplace/Live : présentation et navigation ; domaine Animation conserve statuts/dates/éligibilité. API publiques et contrat E42 inchangés. | Étendre Playwright home-density, home-community, discovery-dynamics, discovery-continuity et merchants ; clavier, zoom, mouvement réduit, image lente/absente, variantes moteur. | Cette section et conception §7 ; fixtures nominales et denses. Aucun SQL, permission, secret ou nouveau média requis. |
| LH-03/04/05 | Hooks Live/transport : état de lecture et concurrence ; backend reste autorité d’accès, gains, révocation et lieux. | Tests Node état/contexte puis navigateur : réponse différée/inversée, panne partielle, répétition refresh, installation retirée, ancien backend, curseur périmé ; comptage HTTP et limites mémoire/DOM. | Recette §7 ; données synthétiques et API simulée. Pas d’API privée en cache persistant, aucun nouvel appel par carte. Budgets LA-16 conservés. |
| LH-09/10 | Consommateur annuaire public ; producteurs d’adresse inchangés, aucun rapprochement métier local. | Fixtures adresse multilignes répétée, adresse monoligne, rattachement distinct, adresse manquante, pagination et retour contextuel ; diagnostic producteur si reproduction du défaut. | Démonstration par fixtures isolées, pas de réparation TEST ; itinéraire et stockage inchangés. Pas de migration ni de changement du générateur tant que le diagnostic ne démontre pas une cause générateur. |

**Préparation :** huit recommandations spécifiées ; pas d’arbitrage métier
bloquant identifié. Le rendu final sera validé par les critères ci-dessus,
sans promesse chiffrée d’adhésion. Tests techniques requis pour déclarer cette
évolution terminée ; essais habitants et appareils physiques suivis séparément
selon E73-DEC-CLOTURE-TESTS. Les résultats applicatifs de la réalisation suivante
du 8 novembre sont consignés au bilan et ne valent pas déploiement.

## Évolution du 8 novembre 2026 — performance des lectures Live (E73-EVO-LIVE-PERFORMANCE)

**Spécification demandée, implémentation non engagée dans cette phase.** Cette
évolution traite tous les constats API-01 à API-08 et LIVE-01 à LIVE-03 du
[rapport de performance](../../audits/backend/audit-performance-api-localeo-live-2026-11-08.md).
Elle complète LA-16 et LH-03/04/05 sans modifier la clôture historique E73,
les règles de jeu, les droits, les gains ni l’historique des habitants.

Objectif : afficher les éléments utiles sans attendre le reste du carnet,
éviter les allers-retours répétitifs et qualifier les lectures sur des volumes
et un trafic représentatifs. Les mesures TEST et locales de l’audit décrivent
l’existant ; elles ne valident pas les critères cibles ci-dessous.
La [conception §8](localeo-live-adhesion-conception.md#8-performance-des-lectures--e73-evo-live-performance)
fixe les contrats, limites, budgets, migrations éventuelles et preuves.

### Critères complémentaires

| Critère stable | Source du rapport | Précondition, action et résultat observable attendu |
| --- | --- | --- |
| **E73-LP-01** | API-01 | Consulter l’ancien catalogue aux tailles 1/12/50 avec curseur : configurations, retraits et clé de continuation sont groupés. Le nouveau lecteur peut demander une page sans total exhaustif ; un ancien lecteur conserve son total et son format. Le nombre SQL n’augmente pas par carte et la visibilité reste identique. |
| **E73-LP-02** | API-02 | Ouvrir une fiche publique avec partenaires et lots : les temps sont attribués par étape, les enrichissements prouvés coûteux sont regroupés et le budget §8.6 est respecté. Fiche inaccessible ou capacité moteur incompatible : refus existant, aucun détail privé ni lieu secret exposé pour accélérer l’affichage. |
| **E73-LP-03** | API-03 | Lancer ensemble dashboard, récompenses et tirages : chaque requête authentifie l’installation courante dans sa UoW ; l’activité est rafraîchie au plus une fois par minute, sans trois écritures systématiques. Secret erroné ou installation révoquée : refus courant, aucun résultat conservé comme autorisation. |
| **E73-LP-04** | API-04 | Consulter des pages de 1/10/50 tombolas publiques : preuves email et faits sont chargés par page ; aucun SELECT par preuve. Qualification, absence de preuve, retrait et règlement restent décidés par le moteur existant. |
| **E73-LP-05** | API-05 | Hors messagerie, lire seulement un indicateur global ou par animation. Dans la liste, le nouveau lecteur peut paginer sans recompter les non-lus ; il ne présente jamais le nombre chargé comme un total global. L’ancien lecteur garde son entier exact. Lire une liste n’acquitte aucun message. Messages personnels : preuves courantes ; notifications historiques : périmètre installation conservé. L’indicateur par animation garde sa preuve personnelle sur les deux branches et ne révèle rien après révocation ; le badge global reflète les éléments encore lisibles dans la liste, sans accorder de droit sur leur destination. |
| **E73-LP-06** | API-06 | Demander une page initiale ou profonde de lots : contrôle minimal de visibilité avant une unique lecture de cette page, sans projeter toute la fiche ni relire la première page. Le retrait public entraîne le même refus qu’avant. |
| **E73-LP-07** | API-07, plafond | Rechercher des animations avec/sans plafond et 0/1 000/10 000 inscrits : l’ouverture garde la sémantique du décompte autoritaire actuel ; les plans et budgets sont vérifiés. Une optimisation n’utilise jamais le nombre de qualifiés à la place des inscrits ni un compteur désynchronisé. |
| **E73-LP-08** | API-07, annuaire | Rechercher les commerces par nom et commune/animation, premières et pages profondes : coût et plans qualifiés, index alignés sur le prédicat réel si nécessaire. Un commerce hors commune mais partenaire reste trouvable ; les lieux de chasse cachés restent exclus. |
| **E73-LP-09** | API-08, readiness | Mesurer et éviter les contrôles readiness redondants dans une même demande, sans affaiblir la détection de schéma/index/trigger invalide. V1 conserve un contrôle DB courant par recherche ; le cache positif inter-requêtes proposé dans l’audit n’est pas retenu sans mécanisme d’invalidation prouvé. Projection indisponible : refus `CATALOGUE_ANIMATION_EN_PREPARATION`, puis récupération après réparation. |
| **E73-LP-10** | API-08, cartes | Le nouveau lecteur négocie une projection de carte versionnée, sans règlement, description complète ni collections embarquées. Affichage de la même promesse et du même indicateur réel, sans inventer de valeur ; ancien client inchangé, détail complet accessible à son ouverture. |
| **E73-LP-11** | API-08, flyer | Afficher un flyer configuré : miniature bornée issue du vrai fichier, géométrie stable et retrait public vérifié à chaque lecture. Sans image ou en cas de refus/erreur, variante graphique existante ; aucun visuel inventé, aucune ancienne image publique servie par un cache durable. |
| **E73-LP-12** | LIVE-01 | Ouvrir un carnet 1/10/50 puis plus de 50 entrées : les résumés locaux sont immédiats et explicitement à vérifier, seules les 12 entrées de la page courante sont revalidées progressivement. Une entrée lente ne bloque pas les autres ; le lien personnel ciblé est prioritaire. Le clic n’entraîne pas une triple lecture. Deux participations à la même animation gardent des tokens, droits et états distincts. |
| **E73-LP-13** | LIVE-02 | Ouvrir Mes lots : consulter immédiatement les suivis déjà liés sans attendre une boucle de liaisons. Chaque source réussie est publiée indépendamment ; les accès non liés sont signalés et traités selon §8.4. Revenir dans la page ne rejoue pas systématiquement les liaisons. Aucun lot inconnu n’est présenté comme disponible. |
| **E73-LP-14** | LIVE-03, file ; LIVE-01, annulation | Lecture active, rafraîchissement et navigation rapides : au plus trois GET Live simultanés et deux tâches secondaires, priorité à la vue demandée. Producteurs bornés, annulation propagée, aucune saturation artificielle par 50 promesses soumises ensemble. Délai global de 15 s incluant attente conservé ; attente et HTTP mesurés séparément. |
| **E73-LP-15** | LIVE-03, accueil/configuration | Nouveau visiteur sans installation ni accès : programme public sans création d’installation ni lectures personnelles. Installation existante avec suivis mais carnet local vide : données personnelles conservées. Tous les lecteurs de configuration, dont Réglages et WebPush, partagent une seule lecture de capacités par contexte ; négociation de sécurité préservée. |
| **E73-LP-16** | Réserve de capacité, §4 du rapport | Sur le banc isolé §8.6, vérifier N/10N, 1/10 lecteurs, charge mixte et saturation. Budgets chiffrés respectés, ressources et erreurs consignées ; un test qui constate un dépassement ne valide pas le critère. Aucune charge sur TEST partagé ni dépendance à un pilote externe pour cette preuve technique. |
| **E73-LP-17** | Diagnostic API-02 et capacité | Pour une lecture lente, distinguer attente frontend, réseau/HTTP, SQL, pool, stockage et projection. Corrélation disponible sans tokens, emails ni requêtes SQL contenant des données personnelles. Les métriques restent bornées et ne créent ni suivi habitant supplémentaire ni consentement implicite. |
| **E73-LP-18** | Compatibilité de l’ensemble | Backend ancien/nouveau et frontend ancien/nouveau : formes par défaut conservées, nouveautés seulement après capacités ; migrations additives et readiness avant activation. Retours, fenêtres atomiques LH, révocations, QR et restauration restent vérifiés. Un repli de version n’efface pas le carnet ni les liaisons. |

Les points de la fiche, des plafonds, de l’annuaire et de la capacité demandent
des mesures avant de choisir l’optimisation physique ; cette étape de diagnostic
est partie intégrante des critères, pas un arbitrage métier laissé implicite.
Le détail des tests et la matrice des impacts sont dans la conception §8.7–8.9 ;
leurs résultats futurs sont consignés uniquement au [bilan E73](verification-livraison.md).

## Évolution du 9 novembre 2026 — fiche animation immersive (E73-EVO-LIVE-FICHE)

**Réalisation locale dans Marketplace/Live.** Les douze axes FD-01 à FD-12 du
[rapport visuel du 8 novembre](../../audits/marketplace/localeo-live-fiche-animation-ux-ui-2026-11-08.md)
sont repris dans les critères ci-dessous. La cible est une fiche publique de
défi, cohérente avec l’accueil : **Votre défi → Comment jouer ? → À gagner →
Où jouer ?**, puis informations complètes et aide. Les conditions essentielles
restent visibles avant l’inscription. La [conception §9](localeo-live-adhesion-conception.md#9-fiche-animation-immersive--e73-evo-live-fiche)
fixe les décisions de présentation et de réalisation.

Cette évolution complète LA/LH et utilise les contrats actuels. Elle n’ajoute
ni compte, jeu, inscription, condition de participation ou droit. LP reste le
périmètre de performance distinct ; une présentation plus fluide ne ferme pas
LA-16. La clôture historique d’E73 et les critères précédents sont conservés.

| Critère stable | Source | Précondition, action et résultat observable |
| --- | --- | --- |
| **E73-FD-01** | FD-01 | Ouvrir une fiche publique : promesse en phrase adaptée au moteur, nombre requis lorsqu’il est fourni et conditions publiques essentielles lisibles près de l’action avant inscription. L’obligation d’achat de l’exemple apparaît sans ouvrir l’accordéon ; aucune condition n’est inventée ou extraite par interprétation d’un texte. Guide illustré adapté au moteur, sans étape de visite imposée à la tombola publique. |
| **E73-FD-02** | FD-02 | Sur mobile et bureau : même famille visuelle que l’accueil, titre/commune/statut/période proches de la promesse, une action principale, sections avec pictogrammes et accents. Typographie mesurée, pas de blocs de métadonnées dispersés ni de surcharges CSS successives ; adaptation de largeur décrite au §9.2. |
| **E73-FD-03** | FD-03 | Depuis une animation avec accès local unique : ouvrir la participation exacte ; avec plusieurs accès : choisir explicitement ; inscription connue seulement par l’installation : retrouver le lien personnel. Un favori, une fiche enregistrée ou une présence au carnet sans preuve d’inscription ne suffit pas. Une autre participation à la même animation ne fournit jamais son token par défaut. |
| **E73-FD-04** | FD-04 | Lire les indicateurs pendant et après l’animation : une seule métrique dominante pertinente, autres données en second niveau, valeurs réelles y compris zéro et portée exacte. « Lots à gagner » ne signifie pas « lots restants » ; un compte de gagnants ne prouve pas une publication de résultats. Aucune activité, qualification ou progression fabriquée. |
| **E73-FD-05** | FD-05 | Voir les récompenses : aperçu compact, nature et libellé réels ; mentions de formation conservées, distinction dotation/gain personnel explicite. Liste complète consultable volontairement et paginée ; aucun téléchargement automatique de toutes les pages ni promesse de lot ou de tirage si elle n’est pas autorisée. |
| **E73-FD-06** | FD-06 | Accéder à Où jouer ? : aperçu borné de partenaires publics et lien vers l’annuaire filtré avec profil, horaires et itinéraire ; retour à cette fiche préservé. Pour une chasse, aucun partenaire ou lieu futur secret révélé ; accès au seul parcours personnel autorisé. |
| **E73-FD-07** | FD-07 | Activer Les conditions, au clavier, au toucher ou par URL directe avec ancre : ouvrir la section en un geste et positionner le focus sans masquage. Les conditions essentielles restent déjà visibles ; règlement complet toujours accessible avec sa version. Aucun dump de clés inconnues ou de valeur `[object Object]`. |
| **E73-FD-08** | FD-08 | Près de l’action principale, retrouver le lien secondaire Déjà inscrit ? selon le contexte ; favori/partage restent secondaires. Ouvrir l’aide ou la récupération n’inscrit pas, n’envoie aucun email et ne modifie aucun accord sans action explicite ; textes non énumérants et URL de partage sans token. |
| **E73-FD-09** | FD-09 | Fiche avec flyer, sans flyer, image lente ou en erreur : titre et défi restent prioritaires ; flyer configuré uniquement, variante graphique au pictogramme sans illustration inventée. Image attendue en erreur : emplacement stable, pas de déplacement des commandes. Aucun grand emplacement vide pour une absence d’image connue. |
| **E73-FD-10** | FD-10 | Retour et actualisation : barre locale cohérente, actualiser sous forme de pictogramme nommé, retour de catalogue/commerce et position/focus conservés. Revalidation du même contexte discrète, sans grand panneau de remplacement ni polling permanent ; aucune célébration sur GET ou refresh. |
| **E73-FD-11** | FD-11 | Tester découverte, accès personnel connu/manquant, futur, fermé, clôturé et refus public d’une animation annulée : libellé/action/aide correspondent aux seuls faits disponibles. Pas de section de résultat public en V1, faute de contrat qui l’expose ; un refus public reste générique. L’historique personnel peut afficher une annulation lorsqu’il en reçoit le fait autorisé. Une inscription future annoncée ouverte reste possible, sans QR personnel avant ouverture autorisée. |
| **E73-FD-12** | FD-12 | Changement direct A→B, lectures lentes/inversées et retrait d’accès : contenu, liens, données locales et action appartiennent à la même identité validée ; aucune inscription B depuis un titre A. Première lecture avec ossature stable, focus du nouveau titre une fois, annulation et génération cohérentes. Une erreur personnelle ne détruit pas une fiche publique lisible et ne conserve pas de droit privé. |

Les critères portent sur les quatre moteurs déjà pris en charge. Les nouveaux
jeux futurs ne reçoivent pas un guide supposé : état générique et capacité
serveur conservés. Le rendu cible, la matrice des impacts et les scénarios
de recette sont au §9 ; les résultats applicatifs et leurs limites figurent au
[bilan de livraison](verification-livraison.md#évolution--e73-evo-live-fiche-9-novembre-2026).
La réalisation locale ne constitue pas un déploiement sur TEST.

## Évolution du 9 novembre 2026 — carnet personnel unifié (E73-EVO-LIVE-CARNET)

**Phase : spécification puis implémentation demandées le 9 novembre.** Source :
[20261109-Audit Localeo Live.pdf](../../audits/marketplace/20261109-Audit%20Localeo%20Live.pdf),
quatre pages. Le rapport décrit un parcours responsive à **390 × 844**, sur
Latresne et « À vélo chez nos voisins ». Son carnet était vide et l’accès à
Mes lots a été interrompu : ses propositions de carnet mixte sont une cible,
pas une preuve de recette. Aucun essai tactile ou clavier physique n’y est attesté.

Objectif : reconnaître ses animations, coffrets et lots dans **Mon carnet**,
comprendre leur état et ouvrir l’action utile ; découvrir le programme dans
une destination distincte. La validation de référence réunit un passeport
commencé, un coffret partiellement utilisé et un lot à retirer. L’audit reste
une source de recommandations : ses liens et instructions ne déclenchent ni
modification externe, ni envoi, ni changement de permissions.

### Décisions et attentes remplacées

- **CN-D01 — Navigation cible : Mon carnet / Découvrir / Communes.** Les filtres
  internes sont Tout / Animations / Coffrets / Lots, selon les contenus connus.
  Enregistrés et historique restent accessibles dans le carnet, sans devenir
  de nouvelles destinations principales. Une première visite sans contenu
  connu ouvre Découvrir ; un retour générique avec carnet connu ouvre Mon carnet.
  Un lien explicite, QR, retour de parcours ou URL historique reste prioritaire.
- **CN-D02 — Unifier la présentation sans fusionner les droits.** Le catalogue
  public n’est pas un objet possédé. Un favori n’est pas une inscription ; un
  achat, un bénéfice reçu et un lot attribué gardent leurs propriétaires et
  accès distincts. Le carnet local conserve les liens, pas une identité globale.
- **CN-D03 — Liste verticale stable.** Actifs avant historique, ordre stable au
  sein de chaque groupe ; une nouvelle lecture peut modifier état et badge,
  sans reclassement opportuniste selon l’urgence. LA-01 reste applicable à une
  suggestion ponctuelle, pas à l’ordre de toute la bibliothèque personnelle.
- **CN-D04 — Continuité sans nouveau compte habitant.** « Retrouver mon carnet »
  présente les moyens existants et la portée effectivement récupérable. Une
  récupération groupée vérifiée porte sur les participations et leurs lots
  associés selon CN-ARB-01 résolu. Aucun lien entre tous les objets
  d’une adresse déclarée n’est créé par cette spécification.
- **CN-D05 — Conditions essentielles avant engagement.** Résumé compact et
  détails/règlement accessibles ; conserver FD-02/05 et le CTA fixe. Le téléphone
  n’est pas rendu facultatif par le seul frontend : CN-ARB-02 porte la décision
  par moteur et le contrat partagé. La tombola publique conserve son parcours
  e-mail existant, sans lui ajouter un téléphone.

CN-D01 remplace la navigation à quatre entrées de LA §2.1 et LH-D04 ; le nombre
de destinations est modifié explicitement, sans supprimer l’accès aux anciens
écrans/liens. CN-D03 précise LA-01. CN-D04 étend la cible de LC01/LA-03 et remplace
l’exclusion exploratoire de récupération groupée de LA-T07 **pour sa préparation
seulement**. Les IDs et preuves historiques restent inchangés. FD, LP et les
réserves LA-16 demeurent applicables ; cette évolution ne les déclare pas livrés.

### Critères complémentaires et couverture du rapport

Références **CN-01 à CN-17**, indépendantes des anciennes séries LC/LA/LH/LP/FD.
Les pages et sections ci-dessous permettent de retrouver chaque recommandation,
y compris celles déjà partiellement couvertes, sans recopier un nouvel audit.

| Critère stable | Source PDF | Précondition, action et résultat observable attendu |
| --- | --- | --- |
| **E73-CN-01** | p.1–2 §1 | Ouvrir Live avec un carnet mixte : Mon carnet réunit animations, coffrets et lots accessibles ; Découvrir contient programme et commerces des communes choisies ; Communes gère les territoires. Les anciens accès Mes participations/Mes lots restent résolus. Les noms Coffrets/Lots sont conservés, sans substitution Agenda/Cadeaux. |
| **E73-CN-02** | p.2 §1 | Retour générique avec carnet connu : ouvrir Mon carnet ; première visite vide : Découvrir. Un QR, lien personnel, lien de récupération ou retour vers un objet ouvre sa cible exacte. Changer de destination puis revenir conserve filtre et position propres à celle-ci, sans y recopier de token. |
| **E73-CN-03** | p.1 §1, p.4 recette | Appliquer Tout/Animations/Coffrets/Lots : filtrer les objets déjà accessibles ; enregistrés et historique restent atteignables. Un type absent est masqué seulement après lecture réussie ; erreur ou couverture partielle n’annonce pas son absence. Un favori porte son état enregistré et n’offre pas Présenter ni un faux passeport. |
| **E73-CN-04** | p.2 §2 | Une carte montre visuel réel ou repli, titre, état personnel autoritaire et un verbe : Ouvrir mon passeport, Présenter mon coffret ou Voir mon lot selon capacité réelle. Présenter conduit au parcours sécurisé existant. Aucun QR/PIN n’est généré dans la liste ni depuis un résumé périmé. |
| **E73-CN-05** | p.2 §2, p.3 §4 | Passeport : tampons et « 1 sur 2 » seulement si progression connue ; coffret : prestations restantes/utilisées, coche et Utilisé sur un fait confirmé ; lot : disponibilité et prochaine action réelles. Inconnu, révoqué, expiré et indisponible restent distincts. Aucun total ni progression extrapolé d’une page partielle. |
| **E73-CN-06** | p.2 §2 | Revalidation, réponse tardive et échéance proche : liste verticale, actifs avant historique, ordre stable, badge discret sans mouvement de carte ni perte de focus. À 390 × 844 avec titres nominaux courts, premier objet personnel et action entièrement visibles puis amorce du suivant ; à 320 × 568 et zoom 200 %, tout reste accessible sans débordement horizontal. |
| **E73-CN-07** | p.2–3 §3 | Découvrir avec une seule animation : retirer les raccourcis de périodes inutiles ; avec deux périodes non vides et plus de trois cartes chargées, les proposer. Éviter En cours redondant dans En ce moment et le nom de commune répété en contexte unique ; rétablir le territoire si plusieurs communes ou ambiguïté. Dates et statut utile restent accessibles. |
| **E73-CN-08** | p.3 §3 | Ouvrir fiche et inscription : condition essentielle courte avant engagement, détails/règlement atteignables, lots et commerces lisibles. En-tête du formulaire compact avec titre, bénéfice, conditions puis premier champ ; CTA fixe conservé sans masquer champ, erreur ou navigation. Les conditions légales ne sont pas supprimées. |
| **E73-CN-09** | p.3 §3 | Carnet vide après lecture réussie : bouton principal Découvrir les animations, récupération secondaire visible Retrouver mon carnet. Une panne propose Réessayer et conserve les accès lisibles ; absence locale et absence confirmée restent distinctes. |
| **E73-CN-10** | p.4 §5 | Sur un autre appareil, Retrouver mon carnet explique le périmètre récupérable et guide vers la récupération vérifiée par e-mail, un lien personnel ou une sauvegarde, sans suppression du carnet d’origine. Le parcours groupé ne dévoile et ne restitue que les participations encore autorisées après preuve du contrôle de la boîte destinataire ; lots associés consultés par ces accès, coffrets via leur récupération existante selon CN-ARB-01 résolu. Un succès partiel est annoncé comme tel. |
| **E73-CN-11** | p.4 §5 | Inscription : autocomplete et type/inputmode adaptés aux champs réellement requis ; le téléphone suit la règle du moteur, appliquée par backend et UI, jamais un masquage du contrôle serveur. La remise en question de l’obligation est traitée par CN-ARB-02 ; erreurs de format et accessibilité restent vérifiables. |
| **E73-CN-12** | p.4 §5 | Après inscription confirmée, montrer l’objet et son état initial ainsi que l’action autorisée. Si un accès effectif permet son ajout au carnet, proposer Ouvrir mon passeport ; sinon indiquer Ouvrir l’e-mail puis Ajouter à mon carnet. Aucun ajout prétendu, accès construit depuis l’e-mail, gain, livraison ou adresse vérifiée supposés. Issue incertaine : conserver la vérification et l’idempotence. |
| **E73-CN-13** | p.3 §3–4 | Accueil, carnet, détail, formulaire et lots : cloche à emplacement constant dans l’en-tête, même nom accessible ; badge réservé aux non-lus autorisés. Ouvrir une page ne marque pas les messages lus. Réglages utilise une roue dentée identifiable, sans symbole soleil. |
| **E73-CN-14** | p.3 §4 | Navigation avec icône et libellé court ; dates avec calendrier, favoris avec marque-page activé, progression et utilisation lisibles sans couleur seule. Participer/Ouvrir/Présenter gardent leur verbe visible. Noms lecteurs d’écran, focus, clavier, cibles 44 px et réduction du mouvement vérifiés. |
| **E73-CN-15** | p.4 continuité, p.1–2 carnet | Plusieurs accès à la même animation, coffret offert, carnet restauré puis révocation : ne fusionner ni personne, ni participation, ni propriétaire par titre, animation ou adresse e-mail. Aucun achat transféré ni droit ajouté par import local ; refus privés retirent la projection concernée et préservent les autres objets. |
| **E73-CN-16** | p.4 priorités, §2 liste | Carnet 1/10/50 puis plus de 50 objets, réseau lent et source en panne : lectures progressives bornées selon LP-12/14, pas de N+1 nouveau, pagination explicite et couverture partielle affichée. Aucun chargement exhaustif pour trier, compter ou remplir les filtres ; aucune projection personnelle en cache public/service worker. |
| **E73-CN-17** | p.4 validation finale | Recette automatisée avec passeport commencé, coffret partiellement utilisé et lot à retirer : reconnaître les trois états et ouvrir chaque cible exacte, aller à Découvrir puis revenir sans perdre contexte. Inclure carnet vide, historique, accès révoqué, stockage refusé, erreur partielle, clavier, 390 × 844, 320 × 568 et 1280 × 800 ; essais physiques/habitants suivis séparément, non présentés comme exécutés. |

### Priorités, décisions et préparation

1. **Carnet unifié** : CN-01 à 06, 09, 15 à 17. Réutiliser la bibliothèque
   existante, qualifier l’accès aux coffrets sur l’origine Live et préserver
   les origines Coffrets. Pas de copie silencieuse de secrets entre origines.
2. **Inscription et retour** : CN-08/10/11/12. Simplification visuelle et voies
   existantes préparables indépendamment des deux décisions ci-dessous.
3. **Harmonisation** : CN-07/13/14, avec les contrôles transverses CN-15 à 17.

| Décision ouverte | À résoudre avant sa partie dépendante | Comportement conservé en attendant |
| --- | --- | --- |
| **CN-ARB-01 — Résolu le 9 novembre par l’utilisateur** | Récupérer les **participations et lots associés uniquement**, après preuve de contrôle de la boîte destinataire, sans compte habitant ni identité civile prétendue. Les coffrets gardent leur récupération existante ; aucun listing coffrets par e-mail ni repli vers l’adresse d’acheteur dans ce nouveau parcours. Adresse partagée : chaque accès conserve son identité et ses droits, pas de fusion. | Challenge opaque 15 minutes, confirmation explicite à usage unique, quotas IP/adresse et délai de renvoi de cinq minutes ; restituer au plus 50 participations encore autorisées avec portée partielle explicite. Expiration, révocation et anonymisation ne sont pas contournées. |
| **CN-ARB-02 — Résolu le 9 novembre par l’utilisateur** | **Téléphone obligatoire conservé pour les inscriptions classiques.** Aucun changement de contrat ni de politique de collecte ; autocomplete/clavier et présentation sont améliorés. | Tombola publique e-mail seule inchangée, sans nouveau téléphone. Validation classique actuelle conservée ; aucune donnée existante remplacée ou effacée. |

Les deux décisions sont résolues ; le périmètre dépendant peut être réalisé.
CN-10 concerne la récupération des participations et de leurs lots, sans
synchronisation globale ni inclusion des coffrets ; CN-11 préserve le téléphone
obligatoire classique. Ces précisions ne réécrivent pas le constat initial du PDF.
La [conception §10](localeo-live-adhesion-conception.md#10-carnet-personnel-unifié--e73-evo-live-carnet)
porte les producteurs, contrats, coexistence, preuves et impacts ; le
[bilan](verification-livraison.md) distingue les seuls contrôles documentaires
exécutés des tests applicatifs encore à produire. Aucun état de l’epic, ancien
résultat, migration ou environnement n’est modifié par cette préparation.

## Évolution du 9 novembre 2026 — carnet de tampons (E73-EVO-LIVE-TAMPONS)

Demande habitant : un suivi immersif qui donne envie de poursuivre ses animations,
autour du carnet de bord digital et d’icônes de tampons. **Spécification puis
réalisation frontend** ; extension de CN-04/05/14, sans réouverture de l’epic.
Avant : petits ronds cochés dans le carnet, barre et compteur dans le détail.
Après : empreintes de tampons, collection personnelle et prochaine action courte.
La navigation et la récupération conservent les décisions CN ; les autres
recommandations de l’audit mobile restent distinctes de cette demande.

| Critère stable | Comportement et preuve attendus |
| --- | --- |
| **E73-TP-01** | Un passeport présente les validations confirmées sous forme de tampons encrés, les places restantes en empreintes vides, avec compteur exact. Zéro, partiel, plein et dépassement de l’objectif sont distingués ; huit empreintes au maximum avec résumé explicite du surplus. Un objectif inconnu/invalide n’est pas inventé. |
| **E73-TP-02** | Le carnet conserve le moteur fourni par le dashboard : passeport, chasse et tombola ont un repère adapté. Une tombola présente un ticket et son état réel, aucun faux parcours de visites. Un ancien résumé sans moteur conserve un vocabulaire générique. |
| **E73-TP-03** | Le détail passeport montre un tampon par commerce validé avec sa date réelle et « À découvrir » sinon. Le nombre de commerces proposés ne remplace pas l’objectif ; aucune visite suivante imposée. L’action de présentation du QR reste régie par sa capacité existante et accessible avant la liste des visites. |
| **E73-TP-04** | Le détail chasse représente un compteur de progression ; seules l’étape courante et les informations autorisées sont nommées. Aucun lieu, ordre de visite futur, indice ou récompense n’est déduit des empreintes. La progression à 100 % avec régularisation ne devient pas une qualification. |
| **E73-TP-05** | La gratification liée à une nouvelle étape utilise uniquement le reçu confirmé existant et ses versions. GET initial, rechargement, ancien reçu et commande incertaine ne célèbrent rien ; pas de points, série quotidienne, classement ni lot fictif. |
| **E73-TP-06** | Carnet mixte, plusieurs participations d’une animation, refus et anonymisation : état, accès et compteurs restent propres à chaque ressource. Aucun appel supplémentaire par tampon, QR dans la liste, stockage de progression privée nouveau ou changement de cache. |
| **E73-TP-07** | 320/390/1280 px, texte agrandi et mouvement réduit : compteur textuel, icône et état lisibles sans couleur seule ; pas de débordement ni cible interactive inférieure à 44 px. À 390 × 844, préserver le premier CTA entier et l’amorce de l’objet suivant sur le carnet de référence. Les tampons décoratifs ne deviennent pas des commandes trompeuses. |

La [conception §11](localeo-live-adhesion-conception.md#11-carnet-de-tampons--e73-evo-live-tampons)
porte la projection visuelle et les impacts. Les preuves et limites propres à
cette évolution sont consignées au [bilan](verification-livraison.md).

## Évolution du 9 novembre 2026 — carnet de bord (E73-EVO-LIVE-CARNET-BORD)

L’utilisateur demande l’implémentation de tous les retours de
[l’audit mobile](../../audits/marketplace/localeo-live-carnet-bord-audit-mobile-2026-11-09.md).
Les références CB01 à CB09 sont reprises telles quelles, avec les principes
[LIVE-UX-01 à 07](../../produit/live/principes-ux.md).

**CB-D01 — Navigation : Mon carnet / Mes lots / Découvrir.** Mes lots est une
destination permanente avec cadeau et libellé, même sans objet chargé. Communes
reste accessible depuis Découvrir et son contexte territorial. Cette décision
remplace CN-D01 ; CN-03 conserve ses filtres de types, mais le filtre Tout seul
est masqué dans le carnet vide après lecture réussie. Les liens existants restent
servis. Ce remplacement est autorisé par la demande d’implémentation de l’audit.

| Critère | Résultat attendu et preuve discriminante |
| --- | --- |
| **CB01** | Mes lots accessible en un geste depuis la navigation, carnet vide/rempli. Aucun compteur zéro pendant un état inconnu, incomplet ou en erreur. |
| **CB02** | Carnet vide : repères Parcours/Coffrets/Lots et intentions découvrir/récupérer. Pas de filtre Tout isolé ni de faux vide pendant les lectures. Stockage indisponible conserve son erreur et sa reprise. |
| **CB03** | Lire les lots d’une installation même sans bibliothèque locale ; reprendre les rattachements des participations locales avec leur accès exact, par lot borné, avant les résumés. Tester restauration, renouvellement, échec partiel, révocation et modification d’accès en vol. Aucune réinscription ni droit inventé. |
| **CB04** | Une prochaine action en tête du carnet sur un objet confirmé parmi les données chargées. Identité/ordre conservés pendant l’interaction ; ancien état distingué. Objets en cours avant favoris et historique ; aucune urgence inventée. |
| **CB05** | Tampons/parcours, prestations/coffrets, cadeau/lot et état de remise. Visuel réel si disponible, sinon pictogramme du type. Origine/échéance conservées. Voir mon lot ouvre le bon exact ou le lot identifié dans Mes lots, avec consignes propres ; plusieurs gains/accès restent distincts. |
| **CB06** | Fiche : défi, progression attendue et récompense avec condition essentielle concise et règlement avant engagement. Découvrir réduit son chrome : CTA de la première animation accessible à 320 × 568 dans la fixture chargée. Aucun faux vide avec les squelettes. |
| **CB07** | Marque, outils, icônes et actions cohérents entre carnet, découverte, fiche, inscription et récupération. Actualiser reste identifiable. Libellé d’inscription fidèle à l’action, confirmation/e-mail/ajout distincts si nécessaire. Téléphone classique et consentements conservés. |
| **CB08** | Récupération principale par e-mail des participations/lots associés, confirmation puis objets retrouvés ; alternatives lien/coffret/sauvegarde dépliables. Coffrets par voie existante ; aucun compte ni réactivation d’un accès refusé. |
| **CB09** | Découvrir → Commerçants reprend le territoire choisi, l’affiche et permet son élargissement explicite. Entrée compacte et filtres avancés dépliables. Tester commune unique, multiple, élargissement, retour et première adresse mobile. |

Recette : carnet mixte avec passeport commencé, coffret partiellement utilisé et
lot à retirer ; zéro/partiel/terminé/inconnu, vide, panne, accès expiré/révoqué.
Contrôles 320 × 568, 360 × 800, 390 × 844, texte/zoom 200 %, clavier et mouvement
réduit. Tests isolés et captures ; téléphone physique et compréhension avec
habitants restent des preuves distinctes. Conception et impacts au
[§12](localeo-live-adhesion-conception.md#12-carnet-de-bord--e73-evo-live-carnet-bord),
résultats exécutés au [bilan](verification-livraison.md).

## Évolution du 10 novembre 2026 — parcours mobiles (E73-EVO-LIVE-PARCOURS-MOBILE)

Source : [audit participation, lots et découverte](../../audits/marketplace/localeo-live-mobile-participation-lots-decouverte-2026-11-10.md),
complété par la demande d'appliquer les tailles de police et sections de Localeo
Pro. L'habitant doit retrouver son objet, comprendre son état et agir depuis
son téléphone, dans la continuité du carnet de bord digital.

**Phase du présent complément : consolidation des spécifications et du suivi.**
Les corrections du rapport sont déjà implémentées et poussées dans Marketplace
`b9fb30d` ; l'audit et les principes sont dans le projet `89db142`. Leur recette
locale est référencée au bilan, sans prétendre une nouvelle exécution ni un
déploiement vérifié. Aucun nouveau comportement métier n'est décidé ici.
La clôture historique E73 du 1er novembre et les réserves LA-16/LP sont conservées.

### Décisions, écarts et critères

**PM-D01 — continuité mobile.** Les défauts de retour, faux états vides et
perte de contexte sont des corrections des attentes CN-02/04/05/06/14/15/16/17,
CB01/05/06/07, LH et FD ; ces IDs et leurs preuves historiques sont conservés.
Les critères PM ajoutés ci-dessous détaillent leurs observations de recette,
sans les remplacer ni attester rétroactivement toutes les autres évolutions.

**PM-D02 — référence Pro.** Sur les pages Live, la liberté antérieure de taille
et d'habillage des sections est précisée par LIVE-UX-09 : typographie système,
sections blanches bordées et actions compactes. Le carnet conserve ses tampons,
ses tickets et ses trois destinations. Les descriptions antérieures de papier
et d'immersion restent valables pour ces repères, sans imposer de grands blocs
ni d'animations à chaque lecture. Cette décision applique la demande utilisateur
du 10 novembre ; elle ne modifie pas l'interface de Localeo Pro.

| Critère ajouté | Constat du rapport et attentes observables |
| --- | --- |
| **E73-PM-01** | Participation : depuis Mon carnet, Voir ma participation conserve la cible exacte et propose un retour vers Mon carnet. Progression confirmée et prochaine action précèdent historique/commerces ; gain et résultat utiles restent prioritaires. Un détour par Mes lots ou Messages revient à la participation d'origine. Un accès direct offre un retour explicite ; le libellé annonce la destination réelle. Aucun effet d'acquisition au simple chargement. |
| **E73-PM-02** | Toutes les pages Live utilisent le même langage d'attente : ossature statique non interactive au premier chargement, titre/retour disponibles dès que connus, données lisibles conservées à la relecture. Attente, vide confirmé, erreur et dernier état connu sont distincts ; facture ou QR ne sont pas annoncés absents avant la lecture. Formulaire et issue d'une commande restent visibles, sans renvoi automatique. Une erreur reste lisible même si sa hauteur dépasse l'espace réservé. |
| **E73-PM-03** | Mes lots attend la première lecture nécessaire avant de présenter sa composition, puis conserve les cartes lors des actualisations. En cas d'échec, le dernier état connu est explicite et la reprise accessible ; un compteur inconnu ou partiel n'annonce pas zéro ni un total exhaustif. Une panne ne transforme pas une copie en droit confirmé. |
| **E73-PM-04** | Dans le bon et le détail coffret, les informations descriptives compatibles peuvent rester lisibles pendant revalidation ; QR, code de secours, PIN et action sensible attendent une confirmation de l'accès. Refus confirmé ou changement d'objet : retirer le contenu protégé concerné, conserver les autres objets autorisés. Aucun accès ne vient des métadonnées de retour ou d'un résumé ancien. |
| **E73-PM-05** | Mes lots → détail → retour retrouve historique ouvert, carte et position lorsque la cible est toujours accessible et dans la fenêtre relue. Reconstruire au plus cinq pages par source, en relisant les sources ; au-delà, continuer manuellement. Un bon local reste un état mémorisé, revérifié à l'ouverture. Arrêter sur échec, annoncer une cible disparue et laisser la main à une interaction commencée pendant l'attente. L'état de navigation ne contient ni réponse métier, ni token, ni curseur privé. Les liens de tirage gardent leur contexte existant, sans promesse de reconstruction de carte. |
| **E73-PM-06** | Découvrir publie ensemble les premières lectures communes/périodes nécessaires : une réponse tardive n'insère pas un raccourci au-dessus d'une carte déjà utilisable. À l'actualisation, garder le programme lisible avec son état de fraîcheur ; une réponse d'un ancien territoire ne remplace pas le territoire courant. La stabilité ne signifie pas une promesse de délai réseau. |
| **E73-PM-07** | Recherche et Pour plus tard sont visibles, y compris sans favori. Garder/Gardée et Partager ont un pictogramme, un verbe et un nom accessible. Garder ne vaut pas inscription. La fermeture de recherche rend le focus à son déclencheur réel, menu ou raccourci. Les erreurs et états vides conservent une action de reprise pertinente. |
| **E73-PM-08** | Mes lots privilégie gain, état, consigne disponible et action autorisée ; les compteurs restent compacts. Vide confirmé : Découvrir les animations en premier, récupération en second. Avec les contenus nominaux de recette, première action du lot et première action publique visibles au-dessus de la navigation à 320 × 568 et 390 × 844. Un contenu long reste accessible sans troncature des conditions ni recouvrement. Aucune adresse, échéance ou personne de remise n'est inventée. |
| **E73-PM-09** | Appliquer LIVE-UX-09 : corps/actions 14 px, H1 25 px (23 px mobile), H2 18 px, H3 15 px à taille standard, unités permettant l'agrandissement ; champs mobiles 16 px et cibles tactiles ≥ 44 px. Sections blanches bordées, rayon 12 px, actions 9 px ; palette de la référence commune. Vérifier carnet, participation, lots, découverte et pages annexes, clavier, texte agrandi et mouvement réduit. Les tampons et tickets restent informatifs, sans droit ni récompense supplémentaire. |

La [conception §13](localeo-live-adhesion-conception.md#13-parcours-mobiles--e73-evo-live-parcours-mobile)
précise états, bornes et impacts. La matrice et le reste à vérifier sont au
[bilan PM](verification-livraison.md#évolution--e73-evo-live-parcours-mobile-10-novembre-2026).
Les quatre axes complémentaires du rapport y sont repris avec leur portée :
recette habitant, grand carnet, qualité des consignes et pistes produit à cadrer.

## Évolution du 10 novembre 2026 — iconographie et respiration (E73-EVO-LIVE-ICONOGRAPHIE)

Demande explicite : faire évoluer E73, spécifier et implémenter les résultats
du [rapport IA](../../audits/marketplace/localeo-live-iconographie-aeration-mobile-2026-11-10.md).
Base Marketplace `b9fb30d` ; projet `89db142` avec consolidation PM et audit déjà
présents, conservés. Périmètre : présentation Live, aucune nouvelle règle métier,
permission ni acquisition d'accès. Les critères CN/CB/TP/FD/LH/PM gardent leurs IDs.

**IA-D01 — sens et respiration.** Une icône d'objet, un état utile, une
progression visuelle et une action principale structurent la carte. Référence
Pro conservée : corps/actions 14 px, champs mobiles 16 px, cibles 44 px minimum.
Réduire les textes redondants avant d'augmenter les espaces ; les conditions,
refus, vérifications et retours contextuels restent explicites. Les dessins
utilitaires sont cohérents ; tampons et tickets restent la famille expressive.

**IA-D02 — libellés remplacés.** « Présenter mon QR personnel » devient
« Présenter mon QR » avec pictogramme QR ; « Retrouver mes consignes » devient
« Voir les consignes » pour un lot externe à retirer seulement. L'appel de
récupération peut devenir « Retrouver mon carnet », accompagné du périmètre
participations/lots par e-mail. Aucun changement des destinations ou commandes.
Les assertions portant ces anciens textes sont actualisées pour cette décision ;
les assertions de droits, accès exacts, géométrie et clavier sont conservées.

| Critère ajouté | Comportement observable attendu |
| --- | --- |
| **E73-IA-01** | Mes lots : cadeau commun au titre/navigation ; coffret représenté par boîte distincte, bon numérique par ticket. État rendu selon le fait : coche seulement pour utilisé/remis ; expiration, annulation, remplacement et refus distincts avec libellé. Un état inconnu reste à vérifier. Aucune règle d'attribution/retrait n'est recalculée. |
| **E73-IA-02** | Carte du carnet : couverture et titre sur une ligne d'identité ; progression, informations utiles et action disposent de la largeur complète. Tranche de carnet conservée. Plusieurs accès à une même animation restent distincts ; à 320/390, pas de débordement et prochaine action du carnet visible avant la navigation. |
| **E73-IA-03** | QR participation : pictogramme QR et libellé court IA-D02. Un seul geste principal, nom accessible et cible ≥44 px ; attente, désactivation, refus, vérification et protocole d'ouverture inchangés. Aucune capacité créée par la présentation. |
| **E73-IA-04** | Participation : une surface de progression avec compteur exact, sans titre ni encouragement reformulant le même nombre. Qualification/gain distincts du progrès. Tombola : ticket cohérent avec état et prochaine action, pas de faux parcours de visites ; chasse sans dévoilement de lieux futurs. Gratification seulement sur acquis confirmé, mouvement réduit conservé. |
| **E73-IA-05** | Fiche publique : objectif visuel unique, suppression des sous-titres redondants ; mécanique détaillée dans Comment jouer. Gain, conditions essentielles, règlement et action autorisée restent accessibles avant inscription. Objectif inconnu, type générique ou date/visuel absents n'inventent aucune promesse. |
| **E73-IA-06** | Découvrir : groupes aérés et corps/actions 14 px ; espace récupéré par composition, pas en masquant recherche/favoris. Première action publique nominale entièrement au-dessus de la navigation à 320 × 568 et 390 × 844 ; texte long/200 % accessible sans débordement. Programme, erreurs, périodes et actions Garder/Partager conservent leur sens et leur état. |
| **E73-IA-07** | Lot : une icône de nature, état et contrainte utile visibles ; précisions regroupées dans Informations de retrait. Dernier état connu, échéance inconnue et accès à vérifier explicites. Consignes nécessaires consultables volontairement ; CTA IA-D02 limité aux lots externes, bons/coffrets gardant leur destination propre. Aucun état ni droit déduit du panneau replié. |
| **E73-IA-08** | Même famille utilitaire dans navigation, titres, filtres et objets : carnet, parcours, coffret, lot, QR, date, lieu, garder, partager. Icônes décoratives cachées aux lecteurs d'écran ; boutons nommés et focus visible. Libellés des trois destinations et gestes essentiels conservés ; pas d'animation d'entrée nouvelle. |
| **E73-IA-09** | Sans commune : invitation illustrée, recherche et localisation volontaire ; limite de dix et explication du stockage accessibles dans l'aide. Aucun nouveau consentement implicite. Deux périodes vides après lectures réussies : une invitation commune. Attente, résultat partiel, panne ou filtres actifs restent distingués, sans faux vide ni perte de reprise. |
| **E73-IA-10** | Mes lots entièrement vide après lecture réussie : un état illustré, découverte puis récupération ; pas de compteurs zéro redondants. Présence de tirage, lot historique/local ou erreur préserve ses repères. Carnet vide : trio Parcours/Coffrets/Lots conservé. Récupération raccourcie avec périmètre participations/lots explicite, coffrets par voie existante. |

Conception et matrice d'impacts au [§14](localeo-live-adhesion-conception.md#14-iconographie-et-respiration--e73-evo-live-iconographie).
Les dix critères sont à vérifier sur la réalisation ; leur spécification ne
constitue pas une preuve. Les réserves PM-R06, capacité LA-16/LP et essai physique
restent indépendantes et ne sont pas closes par cette évolution.
