# Registre des anomalies — Marketplace

Registre consolidé depuis `localeo-marketplace/docs/anos/anos.md` et l'ancienne
note libre `localeo-marketplace/docs/ano.md`. Tous les signalements sont conservés.
La réorganisation ne constate aucune correction et ne modifie aucun statut métier.
Les accents et formulations des anciennes notes sont normalisés sans changer leur sens.

## Signalement identifié

### Correctif du 14 novembre 2026 — annonce de publication plus humaine

La notification de nouvelle animation présentait une succession de libellés
« Organisateur », « Commune », « Animation », puis un message générique.
Cause sur Backend `f67d3d16` : le contexte de lecture partagé était préfixé
indistinctement à toutes les notifications d'animation, y compris les annonces
automatiques de publication. La reproduction de la lecture affiche cet ancien
format avant correction et échoue sur la phrase attendue.

Les annonces `ANIMATION_PUBLICATION` deviennent une phrase avec l'organisation,
la commune, l'animation et « Inscrivez-vous pour y participer ! ». Les noms
publics sont chargés une seule fois par page, puis présentés selon l'événement.
La même formulation couvre l'ancienne API de notifications, le centre unifié
des messages et le transport WebPush après sa dernière revalidation. Elle
s'applique aux annonces déjà présentes dans le centre sans réécrire le journal
ni les renvoyer. Les autres événements et messages rédigés restent inchangés.
Attendu fonctionnel dans la [spécification Live](../../specifications/epic-42-localeo-live/frontend-pwa.md#annonce-dune-nouvelle-animation--formulation-du-14-novembre-2026).

Vérifications locales :

- **40 tests backend réussis** : présentation, API, union SQL réelle compilée,
  journal intact, clé source interne absente du DTO, refus d'une autre
  installation, transport revalidé sur deux abonnements, absence de doublon,
  budget UTF-8 et autres messages. Commande via le lanceur isolé avec
  `tests/api/test_localeo_live_notifications_contexte.py`,
  `tests/application/services/test_presentation_notifications.py`,
  `tests/application/animation_locale/test_notifications_localeo_live_animation.py`,
  `tests/application/services/test_diffusion_messages_organisateur.py` et
  `tests/infrastructure/test_payload_webpush.py`.
- **724 contrôles backend d'architecture et de couverture réussis**, via
  `tests/architecture`, `tests/domain/test_domain_dedicated_classes.py` et
  `tests/application/use_cases/test_use_case_business_test_coverage.py`.
- **8 scénarios navigateur réussis** : `tests/visual/live-inbox-ux.spec.cjs`,
  phrase rendue à 320/390/1280 px et texte 200 %, lecture, clavier, liens et
  états d'erreur. Build isolé et API simulées ; captures mobile et bureau
  inspectées. Rapport Marketplace
  `test-results/visual-runs/2026-11-14T20-06-59-108Z-hEiyif`.
- ESLint du scénario modifié : réussi.

Dépôts affectés : Backend (présentation), Marketplace (recette uniquement) et
documentation canonique. Contrats publics, permissions, ciblage, préférences,
schéma, données de démonstration et exploitation : sans impact, puisque seul
le corps présenté change. Aucune migration, modification de donnée historique,
notification réelle, recette native sur téléphone ou déploiement manuel.

Versions : Backend `2360920d0849aebcb0a9e1402103a027b7e57974`, recette
Marketplace `6980e41c9bf4ff013f904e7785542ec709ce2ae8`.

### ANO-MPL-E77-INSCRIPTION — Échec de vérification après inscription confirmée

Signalé le **14 novembre 2026** dans Localeo Live : l'e-mail de confirmation est
reçu, mais l'écran indique que la participation n'a pas pu être vérifiée.
Le formulaire ignorait le reçu d'accès déjà confirmé et imposait deux lectures
personnelles avant tout ajout au carnet. Une panne de lecture après le POST
reproduit exactement le message sur Marketplace `9e07097`.

Correction : mémoriser l'accès du reçu `CONFIRMEE` pour l'animation demandée,
puis afficher la confirmation du carnet. Une erreur de stockage conserve le
reçu en mémoire et réessaie uniquement cet ajout. La consultation du jeu reste
soumise à une lecture serveur fraîche ; un refus ne donne aucun accès aux
produits, QR ou commandes. Les reçus historiques et la tombola en attente
conservent leur parcours distinct.

Preuves et limites dans le [bilan E77](../../specifications/epic-77-juste-prix-local/bilan-realisation.md#correctif-live--conserver-linscription-confirmée-14-novembre-2026).
**Correctif du parcours vérifié localement** ; la cause technique de la lecture
privée échouée sur l'environnement signalé n'est pas reproduite. Aucun accès
personnel distant, nouvelle inscription réelle, réparation de données ou
déploiement manuel effectué.

### Correctif du 11 novembre 2026 — reconnaître une inscription dans Découvrir

**Cause locale** : `LiveDiscovery` présentait le catalogue public sans index des
participations locales. La fiche savait reprendre un accès mais n’affichait pas
de repère explicite. La route du formulaire ne vérifiait pas ces accès et pouvait
proposer une nouvelle saisie malgré une participation dans Mon carnet.

**Correction** : badge avec pictogramme **Déjà inscrit**, action vers la ressource
précise et garde du formulaire, y compris en lien direct. Plusieurs accès restent
distincts ; une installation seule donne un moyen de récupération, pas un accès
personnel. Favoris publics exclus, lectures privées bornées sans création
d’installation, contexte de retour conservé, brouillon maintenu pendant les
relectures. L’unicité backend reste la protection métier contre les doublons.

Rattachement : précision FD-03 dans la
[conception Live](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md).
Résultats, version locale et limites dans la
[vérification E73](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md).
Périmètre : Marketplace/Live et documentation ; aucun contrat, droit, schéma,
générateur ou paramètre d’exploitation changé, aucun déploiement distant.

### Correctif du 11 novembre 2026 — formulaires d’inscription homogènes

La demande harmonise les formulaires actuels de passeport, chasse, tombola
commerçante et tombola publique : **nom, prénom, e-mail et téléphone obligatoires**.
La tombola publique utilisait un formulaire e-mail seul et son API refusait les
champs supplémentaires. Reproduction rouge navigateur et HTTP, puis correction
du composant partagé et de la validation/persistance des commandes actuelles.
Identité confirmée non remplaçable par une nouvelle saisie publique ; anciens
liens de confirmation et API historiques conservés dans leur périmètre propre.

Rattaché à [E74 / CA-07](../../specifications/epic-74-tombola-publique/README.md#harmonisation-des-inscriptions--11-novembre-2026)
et à la précision de CN-ARB-02. Les
[preuves et limites](../../specifications/epic-74-tombola-publique/verification.md#correctif-du-11-novembre-2026--formulaire-homogène)
distinguent tests backend, recette mobile/ordinateur, contrats, lint ciblé et
lint global indisponible. Démonstration adaptée aux coordonnées explicites ;
aucune donnée historique inventée, migration, campagne ni livraison sur TEST.

### Signalement du 11 novembre 2026 — récupération du carnet et choix des participations

**À reproduire sur la version concernée.** L’habitant signale que toutes les
animations retrouvées sont ajoutées, malgré un choix limité. Il confirme que
son carnet était vide avant la récupération et que les éléments non choisis
apparaissent dans **Mon carnet**. Adresse, version servie et mode de sélection
restent à confirmer ; aucune cause distante ni correction produit démontrée.

Sur Marketplace `3a38530` et Backend `d90a0af`, la confirmation du lien restitue
les candidats bornés sans les rattacher à une installation. Le bouton par
participation ne stocke et ne rattache que cette ressource. Deux nouveaux
scénarios avec trois participations, dont deux à une même animation, vérifient
le stockage vide avant choix, l’ajout d’une seule ressource, les appels de
liaison limités à celle-ci, le retour dans Mon carnet et le rechargement.
Ils réussissent à 390 et 1280 px sur un bundle isolé avec API simulée.
La variante renvoyant les trois participations dans le tableau serveur, même
pour les ressources non ajoutées, réussit aussi aux deux formats : les résumés
supplémentaires ne créent aucune entrée locale ni vignette dans Mon carnet.
Rapport `test-results/visual-runs/2026-11-11T19-40-29-882Z-it3svA`.

Lecture publique seule de `test-live.localeo.city` : les assets
`LiveApp-B8AN-YpT.js` et `liveParticipation-oBJ8rH6b.js` conservent un ajout et
une liaison par ressource, sans sauvegarde de tous les candidats dans la
confirmation. La fusion des résumés ne crée pas non plus de participation.
Empreintes et copies temporaires dans
`localeo-marketplace/tmp/carnet-recovery-deployed/` ; cette lecture ne prouve
ni l’origine utilisée par l’habitant, ni la version mise en cache dans sa PWA.

Preuves : `tests/visual/live-carnet-recovery.spec.cjs`, **7 scénarios réussis**,
rapport Marketplace `test-results/visual-runs/2026-11-11T19-24-00-535Z-1GAXdZ` ;
**2 tests Node réussis**, ESLint du fichier modifié réussi ; **28 tests backend
réussis**, rapport `localeo-backend/tmp/carnet-selection-diagnostic.xml`.
La revue indépendante de confirmation, liaison et lecture du tableau privé
n’identifie aucun rapprochement implicite par adresse e-mail.

Attendu canonique : ajout volontaire par ressource, [E73 / CN-10, §10.5](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md#105-arbitrages-du-9-novembre-et-contrat-de-récupération-retenu).
Code produit, contrats, permissions, générateur, migrations et configuration
inchangés ; seuls les tests de régression et le présent suivi sont ajoutés.
Aucune suppression d’accès existant, intervention sur des données utilisateur,
réparation ni recette personnelle sur TEST effectuée. Le signalement reste ouvert.

### ANO-MPL-E73-LIVE-DOTATION — Bilan redondant et lots annoncés peu visibles

Signalé le **11 novembre 2026**. Mon bilan de parcours répétait les informations
de progression et ne permettait pas de comprendre les lots prévus depuis la carte.
Le carnet, la participation et la fiche publique présentent désormais un résumé
statique ; **Les lots à gagner** ouvre les descriptions et pages publiques.
Les gains acquis restent dans Mes lots. Contrats et acceptation dans les
[critères LDOT](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#correctif-du-11-novembre-2026--lots-annoncés-dans-le-carnet).
Corrigé et vérifié localement ; preuves et limites dans le bilan associé. Aucun déploiement.

### Correction du 10 novembre 2026 — Participation, lots et découverte mobile

Prolongement du carnet dans la participation : action QR remontée et vérification
neutre, gains avant les détails. Chargements partagés dans Live, faux vide de
facture supprimé, états anciens distingués des droits confirmés. Mes lots retrouve
la carte et l’historique après relecture bornée ; Découvrir rend recherche,
favoris et partage visibles et compose son programme initial sans insertion
tardive. Typographie et sections alignées sur Pro à la demande de l’utilisateur.

Voir [l’audit et ses preuves](../../audits/marketplace/localeo-live-mobile-participation-lots-decouverte-2026-11-10.md).
Correction locale du frontend ; aucun contrat, migration, flag ou déploiement
TEST au titre de cette intervention.

### Correction du 10 novembre 2026 — Retours Live et stabilité du carnet

Le parcours Mon carnet → participation revenait à l’ancienne liste ; les autres
objets et détours perdaient aussi leur origine. Le bouton Messages était contraint
à 44 px et le changement de filtre reconstruisait tout Live. Les phases locales
puis distantes du chargement déplaçaient plusieurs zones du carnet.

Correction dans Marketplace/Live : contexte de retour borné, filtre et reprise
conservés, largeur des outils adaptée au texte, shell persistant et chargement
initial composé. Les actualisations conservent les cartes jusqu’au résultat ;
les refus et changements d’accès invalident les lectures privées concernées.
Voir l’[audit, les preuves et limites](../../audits/marketplace/localeo-live-parcours-stabilite-2026-11-10.md).
Sans modification de contrat API, migration ou changement de configuration. Correctif local ;
aucun déploiement TEST au titre de cette intervention.

### ANO-MPL-E73-LIVE-05 — Commerçants difficiles à retrouver depuis une animation

Signalé le **6 novembre 2026**. Les partenaires se trouvaient après les lots dans
la fiche publique ; leurs liens ouvraient la fiche Marketplace centrée sur les
coffrets. Les parcours personnels ne proposaient pas d'accès direct aux horaires.

Correction locale : entrée **Commerçants** dans l'en-tête de l'accueil Live,
raccourci contextualisé depuis les animations classiques et leurs parcours,
annuaire recherché/paginé et fiche pratique dans Live. Adresse, horaires publiés
et itinéraire précèdent les animations associées. Retours et filtres conservés,
informations manquantes explicites, aucun téléphone interne exposé. Les lieux
cachés des chasses restent exclus ; leur étape autorisée conserve son itinéraire.

Le backend fournit deux lectures publiques bornées et reprend la visibilité du
catalogue existant. Les retraits acceptés et les profils non publiés sont respectés.
Voir les critères, contrats, preuves et limites dans le
[complément E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#commerçants-partenaires--accès-pratique-depuis-live).
Statut : **corrigé et vérifié localement**. Tests backend et PostgreSQL isolé,
contrats, architecture et 22 scénarios navigateur distincts réussis après les
ajustements de densité mobile et de retour au parcours. Aucun déploiement TEST,
migration ou notification réelle au titre de cette correction.

### ANO-MPL-E73-LIVE-04 — QR participant accessible avant le début

Signalé le **5 novembre 2026**. Le carnet et les vues de jeu activaient
« Présenter mon QR » sur la seule présence d’un token personnel. Le service
`ServiceParticipantsAnimation.qr_png` résolvait l’accès mais ne contrôlait pas la
période ; les contrôles existaient uniquement lors du scan/validation commerçant.
L’inscription anticipée était donc confondue avec le droit de présenter le QR.

Correction locale : capacité serveur `presentation_qr` dans le détail personnel,
réutilisation de `Animation.autoriser_scan` et de la politique de préparation pour
la génération sur les deux URL QR. Live affiche une action grisée **Bientôt
ouvert**, avec la date effective en heure de Paris, et conserve l’accès à la
participation. Une préparation bloquée après le début indique une indisponibilité,
sans inventer une ouverture future. Aucun QR ni identifiant de remplacement lors
d’un refus métier ; les anciennes entrées e-mail `#qr` ne contournent pas ce contrôle.

Les actualisations et changements de route invalident les lectures QR en attente.
Un rafraîchissement global ne peut pas rouvrir une ancienne réponse après réception
d’une indisponibilité. Les QR des lots, bons numériques, Coffrets et lieux gardent
leurs règles ; aucun token d’inscription révoqué ou participant supprimé.

Reproduction backend avant correction : cinq refus attendus manquants, deux cas
ouverts réussis. Tests de domaine/applicatifs/HTTP et projections, refus de
préparation et bornes début inclus/fin exclue vérifiés localement. Les preuves
et impacts sont détaillés dans le [correctif E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#correctif-du-5-novembre-2026--qr-participant-à-louverture).
Schémas et empreintes des trois consommateurs synchronisés pour ce payload ;
aucune migration, configuration distante ou publication réelle.
Statut : **corrigé localement**, déploiement non réalisé.

### ANO-MPL-E73-LIVE-03 — Entrée locale dans Live avec rechargement complet

Reproduit le **30 octobre 2026** par le test existant F12 de
`desktop-layout.spec.cjs` : le marqueur de session de navigation disparaît en
ouvrant Live depuis la marketplace. Les liens de navigation étaient des
ancres HTML même lorsque Live est sur la même origine. Le rechargement détruit
le contexte en mémoire au lieu de rejoindre l'application dans la navigation.

Correction locale des entrées de menu, pied de page et accueil avec le lien
du routeur : transition interne conservée sur la même origine, navigation vers
le domaine configuré lorsque l'origine est différente. Les assertions F12
(pas de rechargement, un enregistrement du service worker, saisie conservée
sur `controllerchange`) restent inchangées. Résultat du rejeu dans le suivi E73.

### ANO-MPL-E73-LIVE-02 — Navigation des communes et réglages concurrents

Signalé le **30 octobre 2026** après la bascule locale vers Live. Découvrir
répète la marque de l'en-tête ; un raccourci icône duplique son entrée de
navigation. Réglages conserve un second sélecteur de commune, distinct du suivi
multiple de Mes communes. L'ouverture des réglages synchronise l'ancien choix
unique, et l'initialisation peut mémoriser une première commune par défaut.

Correction locale : marque uniquement dans l'en-tête de Découvrir, suppression
du raccourci redondant de la surface Animation, boussole et repère géographique
avec libellés visibles. Réglages lit ses préférences sans écriture implicite ;
les actions de notifications utilisent la sélection explicite de Mes communes.
L'ancien accès `?focus=city` rejoint cet écran. Aucun choix par défaut ajouté.

Reproduction navigateur rouge sur le raccourci redondant avant correction ;
rejeux et contrôles de catégories, refus réseau et communes multiples/vide dans
`live-navigation-ux.spec.cjs` et les scénarios Live de `desktop-layout.spec.cjs`.
Les nouveaux indicateurs relèvent de l'évolution
[E73-EVO-LIVE-UX](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md),
pas d'une régression des anciens compteurs. Les résultats et limites sont dans
le [suivi E73](../../specifications/epic-73-animation-et-ou-coffrets/suivi-implementation.md).

### ANO-MPL-E73-LIVE-01 — Reprise du carnet après inscription et stockage refusé

Reproduit le **30 octobre 2026**, pendant E73-EVO-LIVE-UNIQUE, avec le scénario
`live-carnet.spec.cjs` « inscription et enregistrement avec stockage à reprendre ».
Une inscription confirmée par le serveur est suivie d'un échec de la transaction
IndexedDB du carnet. L'écran affiche l'erreur technique au lieu de proposer de
reprendre uniquement l'enregistrement local.

Cause : la lecture du carnet utilise une transaction de nettoyage en écriture.
Son échec interrompt aussi la prévisualisation du reçu personnel, alors que ce
dernier est valide. Le correctif limite le caractère bloquant de cette lecture
indicative ; la lecture serveur reste obligatoire et l'écriture du carnet garde
son erreur explicite et sa reprise. Aucun nouveau POST d'inscription au réessai.
Le test conserve ses assertions sur l'unique inscription, le reçu, le carnet et
le QR ; le résultat de rejeu est consigné dans le
[suivi E73](../../specifications/epic-73-animation-et-ou-coffrets/suivi-implementation.md).
Correction locale ; aucun changement de contrat, migration, données métier,
fournisseur, rôle ou déploiement. La synchronisation de compte reste hors périmètre.

| Identifiant | Périmètre | Description | Suivi conservé |
| --- | --- | --- | --- |
| ANO-MPL-01 | Global | Les animations en cours et à venir ne s'affichent pas sur la Marketplace, notamment sur l'environnement de recette. | À valider |

Origine : registre `docs/anos/anos.md` de Marketplace. Aucune date de signalement
ni preuve de validation n'y était fournie.

## Signalements historiques à qualifier

Ces notes proviennent de `docs/ano.md` de Marketplace, sans identifiant, date,
statut ni preuve de résolution. Elles ne sont pas déclarées corrigées, ni rattachées
automatiquement à une anomalie existante sur la seule ressemblance de leur libellé.

| Repère documentaire | Périmètre indiqué ou incertain | Signalement conservé | Qualification manquante |
| --- | --- | --- | --- |
| Note libre 1 | Marketplace — vue résumé | Présence d'un bloc vide sous le QR code. | Écran exact, version, reproduction et état de résolution. |
| Note libre 2 | Application mobile commerçant — validation d'une prestation | Lorsqu'aucune prestation ne peut être validée par le commerçant, afficher : « Aucune prestation de ce coffret n'est consommable dans votre commerce ». | Signalement historique commerçant non qualifié ; aucun identifiant ou état de résolution connu. |
| Note libre 3 | Consultation d'un coffret consommé — application à préciser | Problème de consultation du coffret consommé. | La note suit le bloc « Application mobile », sans désigner clairement l'écran ni l'application. Aucun comportement attendu ou résultat de reproduction n'est donné. |

Le signalement commerçant est conservé ici pour maintenir la provenance de la note
initiale. Il pourra être transféré ou relié au registre Commerçant après qualification,
sans créer une seconde copie normative de l'anomalie.

## Points à préciser

- Identifier les écrans et les versions concernés par les trois notes historiques.
- Préciser le périmètre de la consultation du coffret consommé.
- Rapprocher les signalements des corrections existantes uniquement sur preuve ;
  aucune clôture n'est déduite de cette migration documentaire.
