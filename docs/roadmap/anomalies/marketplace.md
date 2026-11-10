# Registre des anomalies — Marketplace

Registre consolidé depuis `localeo-marketplace/docs/anos/anos.md` et l'ancienne
note libre `localeo-marketplace/docs/ano.md`. Tous les signalements sont conservés.
La réorganisation ne constate aucune correction et ne modifie aucun statut métier.
Les accents et formulations des anciennes notes sont normalisés sans changer leur sens.

## Signalement identifié

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
