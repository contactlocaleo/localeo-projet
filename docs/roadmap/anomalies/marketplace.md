# Registre des anomalies — Marketplace

Registre consolidé depuis `localeo-marketplace/docs/anos/anos.md` et l'ancienne
note libre `localeo-marketplace/docs/ano.md`. Tous les signalements sont conservés.
La réorganisation ne constate aucune correction et ne modifie aucun statut métier.
Les accents et formulations des anciennes notes sont normalisés sans changer leur sens.

## Signalement identifié

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
