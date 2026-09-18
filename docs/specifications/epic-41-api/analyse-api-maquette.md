# EPIC 41 - Analyse API de la maquette Animation locale

> Consolidation documentaire du 18 septembre 2026 : analyse de cadrage des maquettes V1/V2, commune aux anciennes copies Backend et Animation. Les écarts et travaux proposés ci-dessous sont historiques ; ils ne remplacent ni le [contrat implémenté](openapi.json) ni le statut de la [roadmap](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md).

## 1. Objet

Ce document rapproche la maquette Figma Make `livrables/design/animation/localeo-animation-maquette-v2.zip` des APIs necessaires pour le backend `localeo-backend`. La V1 reste conservee comme historique ; la V2 est la reference fonctionnelle courante.

Il compare les besoins deduits de la maquette avec :

- la specification fonctionnelle existante : [fonctionnelle.md](../../produit/specification-fonctionnelle.md) ;
- le DCT EPIC 41 : [epic-41-animation-locale-dct.md](dct.md) ;
- le backlog EPIC 41 : [epic-41-plateforme-animation-locale-mvp-backlog.md](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md).

## 2. Sources analysees

- Archive maquette de reference : `livrables/design/animation/localeo-animation-maquette-v2.zip`.
- Archive precedente comparee : `livrables/design/animation/localeo-animation-maquette-v1.zip`.
- Fichier principal analyse dans l'archive : `src/app/App.tsx`.
- Brief inclus dans l'archive : `src/imports/pasted_text/localeo-partner-ux-brief.md`.

La maquette est une application React/Vite statique. Elle ne contient pas d'appel HTTP reel (`fetch`, `axios` ou client API). Les besoins API sont donc deduits des ecrans, donnees mockees, filtres, boutons et etats affiches.

## 3. Synthese

La maquette confirme que le DCT EPIC 41 couvre deja les commandes et projections principales :

- creation, modification, publication et cloture d'une animation ;
- workflow ;
- live ;
- dashboard de performance ;
- tirage ;
- envoi de gains ;
- suivi de consommation des coffrets gagnes ;
- flyer ;
- bilan ;
- droit d'acces plateforme.

La maquette fait apparaitre des besoins API supplementaires ou a preciser :

- vues globales partenaire hors fiche animation : participants, validations, tirages, flyers, bilans, coffrets gagnes ;
- endpoints de lecture detailles pour participants, validations, tirage, gains, audit et configuration ;
- endpoints d'export CSV ;
- endpoints d'eligibilite pour les commercants et coffrets selectionnables lors de la creation ;
- endpoint de contexte portail pour la barre haute : commune active, communes habilitees, abonnement, notifications ;
- endpoint d'abonnement plus riche que le simple `droit-acces` ;
- parcours support partenaire ;
- contrat exact des filtres, tris, pagination et masquage des donnees personnelles.

La specification fonctionnelle actuelle ne contient pas encore de section fonctionnelle EPIC 41. Elle couvre seulement des briques core reutilisables :

- referentiels villes, commercants et coffrets ;
- instances de coffret et consultation ;
- validation terrain coffret ;
- contacts support ;
- gestion documentaire ;
- timeline support ;
- audit et back-office.

Il faut donc ajouter une section fonctionnelle dediee a `Animation locale` dans `fonctionnelle.md` ou creer une specification fonctionnelle EPIC 41 dediee, puis la relier au document general.

### Apports fonctionnels de la V2

La V2 ne cree pas de nouvelle surface metier majeure, mais rend les parcours critiques executables et precise leurs contrats :

- les notifications et alertes ouvrent directement l'animation dans l'onglet concerne (`live` ou `tirage`) ;
- l'action recommandee du workflow redirige vers la prochaine etape actionnable ;
- la cloture demande une confirmation explicite, arrete inscriptions et validations, fige la population eligible et est presentee comme irreversible ;
- la publication aboutit a un etat de succes confirmant l'activation, la generation du QR d'inscription et son envoi aux commercants participants ;
- les telechargements et regenerations de flyers, les exports CSV et les actions sur les gains produisent un retour de succes explicite ;
- les acces abonnement et support sont relies depuis la barre de navigation et la fiche abonnement.

Ces ajouts confirment le besoin de reponses de commande portant au minimum le nouvel etat, la prochaine action, les identifiants de ressources produites et un statut de traitement exploitable par l'interface. Les liens profonds restent une responsabilite frontend, mais les projections `NotificationPortailAnimation`, `VueWorkflowAnimation` et `AnimationListItem` doivent fournir `animation_id`, `action_cible` et, lorsque pertinent, `onglet_cible`.

## 4. Inventaire des ecrans de la maquette

| Surface | Ecran / onglet | Besoin backend principal |
| --- | --- | --- |
| Portail partenaire | Barre haute | Contexte utilisateur, commune active, communes habilitees, abonnement, notifications. |
| Portail partenaire | Tableau de bord | KPIs agreges, courbes, top commercants, alertes, animations a action. |
| Portail partenaire | Animations | Liste filtrable, workflow, statut, action suivante. |
| Portail partenaire | Catalogue des modeles | Modeles disponibles, prerequis, disponibilite selon formule. |
| Portail partenaire | Assistant creation | Creation brouillon, configuration, commercants eligibles, coffrets eligibles, publication. |
| Fiche animation | Workflow | Cycle de vie, etape courante, blocages, actions disponibles. |
| Fiche animation | Live | KPIs live, progression, validations recentes, alertes. |
| Fiche animation | Actualites | Liste, brouillon, programmation, publication, masquage et suivi de diffusion Localeo Live. |
| Fiche animation | Configuration | Lecture et modification encadree de la configuration. |
| Fiche animation | Participants | Liste masquee, filtres, progression, qualification. |
| Fiche animation | Validations | Liste filtrable, anomalies, commercant, participant reference. |
| Fiche animation | Tirage | Eligibles, lots, confirmation, lancement, resultats. |
| Fiche animation | Gains et coffrets | Gains envoyes, consommation, expiration, alertes. |
| Fiche animation | Flyer | Apercu, statut, telechargement PDF, regeneration. |
| Fiche animation | Bilan | KPIs, resultats par commercant, export. |
| Fiche animation | Audit | Evenements d'audit chronologiques. |
| Portail partenaire | Coffrets a gagner | Vue globale de consommation des coffrets gagnes. |
| Portail partenaire | Participants | Vue globale multi-animations, masquee. |
| Portail partenaire | Validations | Vue globale multi-animations, export. |
| Portail partenaire | Tirages et gains | Vue globale des tirages par animation. |
| Portail partenaire | Flyers | Vue globale des flyers et actions de regeneration/telechargement. |
| Portail partenaire | Bilans | Vue globale des bilans, comparaison et export global. |
| Portail partenaire | Abonnement | Formule, statut, commune couverte, droits inclus, limitations. |
| Portail partenaire | Support | Documentation, FAQ, contact support. |

## 5. Matrice API par ecran

### 5.1 Contexte portail

| Besoin maquette | API proposee | Statut DCT | Rapprochement specification fonctionnelle |
| --- | --- | --- | --- |
| Charger la commune active, les communes habilitees, le partenaire, le statut d'abonnement et les notifications. | `GET /protected/animation-locale/contexte-portail` | A ajouter. Le DCT a `tenant-communes` et `droit-acces`, mais pas d'endpoint agrege. | Non couvert. `identite_acces` et support existent mais pas le contexte portail animation. |
| Lister les communes habilitees. | `GET /protected/animation-locale/tenant-communes` | Couvert. | Les villes existent dans la spec core, mais pas les habilitations animation. |
| Consulter le droit d'acces plateforme. | `GET /protected/animation-locale/droit-acces` | Couvert. | Non couvert dans la spec fonctionnelle actuelle. |
| Consulter les notifications portail. | `GET /protected/animation-locale/notifications` | A ajouter ou rattacher a une API notification transverse. | Notifications/outbox existent comme mecanisme, pas comme inbox portail. |

Recommandation : conserver `tenant-communes` et `droit-acces` pour les ecrans detailles, mais ajouter `contexte-portail` pour eviter plusieurs appels au chargement de l'application.

### 5.2 Tableau de bord

| Besoin maquette | API proposee | Statut DCT | Rapprochement specification fonctionnelle |
| --- | --- | --- | --- |
| KPIs : animations publiees, inscrits, completion, qualifies, validations, coffrets envoyes, consommation. | `GET /protected/animation-locale/dashboard-performance` | Couvert. | Le dashboard operationnel existe cote back-office, mais pas pour animation locale. |
| Courbe inscriptions/validations par semaine. | Meme endpoint, bloc `series`. | A preciser dans schema `DashboardPerformanceAnimationResponse`. | Non couvert. |
| Top commercants par validations. | Meme endpoint, bloc `top_commercants`. | A preciser. | Les commercants existent, mais pas leur scoring animation. |
| Alertes d'actions : tirage non lance, gains non envoyes, faible consommation. | Meme endpoint, bloc `alertes_action`. | A preciser. | Non couvert. |
| Filtres periode, commune, modele, statut, animation. | Query params : `commune_id`, `periode_debut`, `periode_fin`, `modele_code`, `statut`, `animation_id`. | A preciser. | Non couvert. |

### 5.3 Liste des animations

| Besoin maquette | API proposee | Statut DCT | Rapprochement specification fonctionnelle |
| --- | --- | --- | --- |
| Liste filtrable des animations de la commune active. | `GET /protected/animation-locale/communes/{commune_id}/animations` | Couvert. | Non couvert. |
| Recherche texte, filtres statut/modele/periode/alerte. | Query params sur la route liste. | A preciser. | Non couvert. |
| Afficher workflow step, action suivante, alertes, compteurs. | Inclure une projection `AnimationListItemResponse`. | Partiellement couvert. | Non couvert. |
| Ouvrir une fiche animation. | `GET /protected/animation-locale/animations/{animation_id}` | Couvert. | Non couvert. |

### 5.4 Catalogue des modeles

| Besoin maquette | API proposee | Statut DCT | Rapprochement specification fonctionnelle |
| --- | --- | --- | --- |
| Lister modeles disponibles et futurs. | `GET /protected/animation-locale/modeles` | A ajouter. Le DCT a seulement `GET /public/animation-locale/modeles`. | Non couvert. |
| Afficher prerequis et disponibilite selon abonnement/formule. | `GET /protected/animation-locale/modeles?commune_id=...` | A ajouter ou enrichir `modeles`. | Non couvert. |
| Bloquer les modeles non disponibles. | Champ `available`, `unavailable_reason`. | A preciser. | Non couvert. |

Recommandation : garder une route publique pour les modeles consultables hors portail, mais ajouter une route protegee contextualisee par tenant et abonnement.

### 5.5 Assistant de creation

| Etape maquette | API proposee | Statut DCT | Rapprochement specification fonctionnelle |
| --- | --- | --- | --- |
| Choisir le modele. | `GET /protected/animation-locale/modeles` | A ajouter. | Non couvert. |
| Choisir la commune active. | `GET /protected/animation-locale/tenant-communes` | Couvert. | Les villes existent, pas les tenants habilites. |
| Creer un brouillon. | `POST /protected/animation-locale/animations` | Couvert. | Non couvert. |
| Saisir informations publiques. | `PATCH /protected/animation-locale/animations/{animation_id}` | Couvert. | Non couvert. |
| Selectionner commercants participants. | `GET /protected/animation-locale/communes/{commune_id}/commercants-eligibles` | A ajouter. | Les commercants sont couverts par `GET /protected/commercants`, mais pas l'eligibilite animation. |
| Configurer les regles. | `PATCH /protected/animation-locale/animations/{animation_id}` | Couvert. | Non couvert. |
| Selectionner coffrets a gagner. | `GET /protected/animation-locale/communes/{commune_id}/coffrets-eligibles` | A ajouter. | Les coffrets sont couverts par `GET /public/coffrets`, mais pas l'eligibilite lot. |
| Apercu flyer avant publication. | `GET /protected/animation-locale/animations/{animation_id}/flyer/preview` | A ajouter. | Gestion documentaire couvre les documents, pas le flyer animation. |
| Recapitulatif et verification avant publication. | `GET /protected/animation-locale/animations/{animation_id}/validation-publication` | A ajouter ou inclure dans workflow. | Non couvert. |
| Publier l'animation. | `POST /protected/animation-locale/animations/{animation_id}/publier` | Couvert. | Non couvert. |

Recommandation : ajouter deux endpoints d'eligibilite propres a `animation_locale`. Ils encapsulent les regles "actif", "commune", "modele", "abonnement" sans exposer au frontend la logique croisee `referencement` + `commercialisation`.

### 5.6 Fiche animation

| Onglet | API proposee | Statut DCT | Rapprochement specification fonctionnelle |
| --- | --- | --- | --- |
| Header fiche animation. | `GET /protected/animation-locale/animations/{animation_id}` | Couvert. | Non couvert. |
| Workflow. | `GET /protected/animation-locale/animations/{animation_id}/workflow` | Couvert. | Non couvert. |
| Live. | `GET /protected/animation-locale/animations/{animation_id}/live` | Couvert. | Non couvert. |
| Evenements live. | `GET /protected/animation-locale/animations/{animation_id}/live/evenements` | Couvert. | Timeline support existe mais pas live animation. |
| Actualites. | `GET/POST /protected/animation-locale/animations/{animation_id}/actualites` et commandes de publication/masquage. | A ajouter - evolution `EP41-T51`. | Reutilise `activites_locales` avec `animation_id`; affichage Live sous le filtre `Animations`. |
| Configuration. | `GET /protected/animation-locale/animations/{animation_id}/configuration` | A ajouter ou inclure dans `GET animation`. | Non couvert. |
| Participants. | `GET /protected/animation-locale/animations/{animation_id}/participants` | A ajouter. | Non couvert. |
| Validations. | `GET /protected/animation-locale/animations/{animation_id}/validations` | A ajouter. Le DCT couvre seulement `POST validations`. | La validation terrain coffret existe, mais pas la liste animation. |
| Tirage. | `GET /protected/animation-locale/animations/{animation_id}/tirages` | A ajouter. Le DCT couvre seulement `POST tirages`. | Non couvert. |
| Gains. | `GET /protected/animation-locale/animations/{animation_id}/gains` | A ajouter ou utiliser une route interne existante aussi en protected. | Non couvert. |
| Flyer. | `GET /protected/animation-locale/animations/{animation_id}/flyer` | Couvert. | Gestion documentaire utile pour le stockage. |
| Bilan. | `GET /protected/animation-locale/animations/{animation_id}/bilan` | Couvert. | Non couvert. |
| Audit. | `GET /protected/animation-locale/animations/{animation_id}/audit` | A ajouter ou exposer une projection support/audit. | Timeline support existe en internal, pas en protected partenaire. |

### 5.7 Actions sensibles

| Action maquette | API proposee | Statut DCT | Exigences |
| --- | --- | --- | --- |
| Cloturer. | `POST /protected/animation-locale/animations/{animation_id}/cloturer` | Couvert, contrat precise par la V2. | Confirmation frontend, audit, idempotence ; arret des inscriptions/validations et gel atomique de la population eligible. Retourner le statut et la prochaine action. |
| Lancer tirage. | `POST /protected/animation-locale/animations/{animation_id}/tirages` | Couvert. | Cle d'idempotence obligatoire, population eligible figee. |
| Envoyer gain. | `POST /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/envoyer` | Couvert. | Cree et active `CoffretInstance`, notifie gagnant, idempotent. |
| Publier. | `POST /protected/animation-locale/animations/{animation_id}/publier` | Couvert, contrat precise par la V2. | Activation, generation du QR d'inscription et diffusion aux commercants tracees ; retour partiel possible si la diffusion est asynchrone. |
| Regenerer flyer. | `POST /protected/animation-locale/animations/{animation_id}/flyer/regenerer` | Couvert. | Remplace le flyer courant sans UX de version et retourne le statut de generation. |
| Telecharger flyer. | `GET /protected/animation-locale/animations/{animation_id}/flyer/download` | A ajouter. | Peut rediriger vers document securise ou streamer le PDF. |
| Exporter validations. | `GET /protected/animation-locale/validations/export.csv` | A ajouter. | Export CSV, suppression selon politique de conservation. |
| Exporter bilan. | `GET /protected/animation-locale/animations/{animation_id}/bilan/export.csv` | A ajouter. | CSV MVP. |
| Exporter tous les bilans. | `GET /protected/animation-locale/bilans/export.csv` | A ajouter. | Respect des filtres et tenant commune. |

### 5.8 Vues globales du menu

| Ecran global | API proposee | Statut DCT | Commentaire |
| --- | --- | --- | --- |
| Coffrets a gagner. | `GET /protected/animation-locale/gains/coffrets/consommation` | A ajouter. Le DCT a seulement la vue par animation. | Vue globale multi-animations de consommation des coffrets gagnes. |
| Participants. | `GET /protected/animation-locale/participants` | A ajouter. | Donnees personnelles masquees par defaut. |
| Validations. | `GET /protected/animation-locale/validations` | A ajouter. | Filtres animation, commercant, resultat, periode. |
| Tirages et gains. | `GET /protected/animation-locale/tirages` | A ajouter. | Liste des animations avec eligibles, tirage, gagnants, actions. |
| Flyers. | `GET /protected/animation-locale/flyers` | A ajouter. | Liste des flyers avec statut `ok` ou `a_regenerer`. |
| Bilans. | `GET /protected/animation-locale/bilans` | A ajouter. | Comparaison d'animations et export global. |
| Abonnement. | `GET /protected/animation-locale/abonnement` | A ajouter ou enrichir `droit-acces`. | La maquette affiche formule, statut, partenaire, dates, droits inclus et limitations. |
| Support. | `GET /protected/support/animation-locale/ressources` et `POST /protected/support/animation-locale/messages` | A ajouter cote domaine support, pas dans `animation_locale`. | La specification fonctionnelle couvre le contact consommateur, pas le support partenaire. |

## 6. APIs consolidees recommandees

### 6.1 Protected partenaire

Routes deja presentes dans le DCT et confirmees par la maquette :

- `GET /protected/animation-locale/tenant-communes`
- `GET /protected/animation-locale/droit-acces`
- `GET /protected/animation-locale/communes/{commune_id}/animations`
- `POST /protected/animation-locale/animations`
- `GET /protected/animation-locale/animations/{animation_id}`
- `PATCH /protected/animation-locale/animations/{animation_id}`
- `GET /protected/animation-locale/animations/{animation_id}/workflow`
- `GET /protected/animation-locale/animations/{animation_id}/live`
- `GET /protected/animation-locale/animations/{animation_id}/live/evenements`
- `GET /protected/animation-locale/dashboard-performance`
- `POST /protected/animation-locale/animations/{animation_id}/publier`
- `POST /protected/animation-locale/animations/{animation_id}/cloturer`
- `POST /protected/animation-locale/animations/{animation_id}/validations`
- `POST /protected/animation-locale/animations/{animation_id}/tirages`
- `POST /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/envoyer`
- `GET /protected/animation-locale/animations/{animation_id}/gains/coffrets/consommation`
- `GET /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/coffret-consommation`
- `GET /protected/animation-locale/animations/{animation_id}/flyer`
- `POST /protected/animation-locale/animations/{animation_id}/flyer/regenerer`
- `GET /protected/animation-locale/animations/{animation_id}/bilan`

Routes a ajouter ou a preciser :

- `GET /protected/animation-locale/contexte-portail`
- `GET /protected/animation-locale/modeles`
- `GET /protected/animation-locale/communes/{commune_id}/commercants-eligibles`
- `GET /protected/animation-locale/communes/{commune_id}/coffrets-eligibles`
- `GET /protected/animation-locale/animations/{animation_id}/configuration`
- `GET /protected/animation-locale/animations/{animation_id}/validation-publication`
- `GET /protected/animation-locale/animations/{animation_id}/participants`
- `GET /protected/animation-locale/animations/{animation_id}/validations`
- `GET /protected/animation-locale/animations/{animation_id}/tirages`
- `GET /protected/animation-locale/animations/{animation_id}/gains`
- `GET /protected/animation-locale/animations/{animation_id}/audit`
- `GET /protected/animation-locale/animations/{animation_id}/flyer/download`
- `GET /protected/animation-locale/animations/{animation_id}/bilan/export.csv`
- `GET /protected/animation-locale/participants`
- `GET /protected/animation-locale/validations`
- `GET /protected/animation-locale/validations/export.csv`
- `GET /protected/animation-locale/tirages`
- `GET /protected/animation-locale/gains/coffrets/consommation`
- `GET /protected/animation-locale/flyers`
- `GET /protected/animation-locale/bilans`
- `GET /protected/animation-locale/bilans/export.csv`
- `GET /protected/animation-locale/abonnement`
- `GET /protected/animation-locale/notifications`

### 6.2 Public participant

La maquette fournie couvre le portail partenaire. Les APIs publiques participant deja prevues dans le DCT restent necessaires pour le parcours QR et l'application participant :

- `GET /public/animation-locale/modeles`
- `GET /public/animation-locale/communes/{commune_id}/animations`
- `GET /public/animation-locale/animations/{animation_id}`
- `GET /public/animation-locale/animations/{animation_id}/inscription`
- `POST /public/animation-locale/animations/{animation_id}/inscriptions`
- `GET /public/animation-locale/participants/{participant_token}/animations`
- `GET /public/animation-locale/participants/{participant_token}/historique`
- `GET /public/animation-locale/participants/{participant_token}/animations/{animation_id}`
- `GET /public/animation-locale/participants/{participant_token}/animations/{animation_id}/qr`
- `GET /public/animation-locale/participants/{participant_token}/progression`

### 6.3 Internal Localeo

Les routes internes du DCT restent coherentes avec le besoin de supervision Localeo, meme si la maquette analysee est orientee partenaire :

- `GET /internal/animation-locale/live`
- `GET /internal/animation-locale/communes/{commune_id}/live`
- `GET /internal/animation-locale/dashboard-performance`
- `GET /internal/animation-locale/animations/{animation_id}/workflow`
- `GET /internal/animation-locale/communes/{commune_id}/droit-acces`
- `GET /internal/animation-locale/live/evenements`
- `GET /internal/animation-locale/live/alertes`
- `GET /internal/animation-locale/animations`
- `POST /internal/animation-locale/animations/{animation_id}/cloturer`
- `POST /internal/animation-locale/animations/{animation_id}/tirages`
- `GET /internal/animation-locale/animations/{animation_id}/gains`
- `GET /internal/animation-locale/animations/{animation_id}/gains/coffrets/consommation`

## 7. Rapprochement avec la specification fonctionnelle existante

| Brique de la specification fonctionnelle | Reutilisation EPIC 41 | Ecart |
| --- | --- | --- |
| UC-01 a UC-05, referentiels villes, commercants, coffrets. | Source des communes, commercants participants et coffrets lots. | Ajouter la notion d'eligibilite animation : commune habilitee, commercant actif, coffret actif de la commune. |
| UC-11 a UC-13, achats et `CoffretInstance`. | Creation/activation automatique d'une instance de coffret gagnee et suivi consommation. | Ajouter un cas d'origine `GAIN_ANIMATION` et une vue de consommation rattachee a un gain. |
| UC-18, validation terrain nominale. | Inspiration pour le scan commercant et les controles anti-doublon. | Le QR animation est distinct du QR coffret ; il faut un flux de validation animation dedie ou une extension explicite de l'application commercant. |
| UC-20, messages de contact. | Base pour le support partenaire. | La maquette demande un support partenaire protege, pas seulement un contact consommateur public. |
| UC-21B, gestion documentaire. | Stockage du flyer PDF et metadonnees. | Ajouter un type/rattachement documentaire `ANIMATION` ou `FLYER_ANIMATION`. |
| UC-22, timeline support. | Reutilisable pour audit/supervision Localeo. | La maquette expose un onglet audit partenaire ; il faut definir le niveau visible cote partenaire. |
| Back-office. | Supervision Localeo. | La maquette n'est pas le back-office Localeo, mais un portail partenaire dedie. |

Conclusion : la specification fonctionnelle actuelle doit etre etendue. Elle ne suffit pas a contracter les parcours EPIC 41.

## 8. Ecarts principaux a traiter

### Ecart 1 - Vues globales partenaire non couvertes par le DCT

Le DCT couvre surtout les vues par animation. La maquette ajoute des vues globales :

- participants ;
- validations ;
- tirages ;
- flyers ;
- bilans ;
- coffrets gagnes.

Decision recommandee : ajouter ces endpoints au DCT, car ils structurent directement le menu du portail partenaire.

### Ecart 2 - Endpoints de lecture participants/validations/tirages/gains

Le DCT couvre certaines commandes (`POST validations`, `POST tirages`, `POST envoyer gain`) mais pas toujours les lectures necessaires :

- participants d'une animation ;
- validations d'une animation ;
- resultats de tirage ;
- gains d'une animation ;
- audit d'une animation.

Decision recommandee : ajouter les routes de lecture dediees, avec pagination et filtres.

### Ecart 3 - Eligibilite des commercants et coffrets

La creation ne peut pas simplement consommer les APIs core generiques. Elle doit afficher uniquement :

- les commercants eligibles de la commune ;
- les coffrets actifs de la commune utilisables comme lots.

Decision recommandee : exposer des vues d'eligibilite sous `animation_locale`.

### Ecart 4 - Abonnement plus riche que `droit-acces`

La maquette affiche formule, statut, commune couverte, renouvellement, facturation, partenaire, droits inclus et limitations.

Decision recommandee : conserver `droit-acces` pour les controles techniques, mais ajouter une projection `abonnement` pour l'ecran UX.

### Ecart 5 - Exports

La maquette montre :

- export validations ;
- export bilan d'une animation ;
- export global des bilans.

Decision recommandee : ajouter des routes CSV directes au MVP, avec traces d'export et suppression automatique selon la politique de conservation.

### Ecart 6 - Audit visible partenaire

La maquette expose un onglet `Audit` dans la fiche animation.

Decision recommandee : ajouter une projection audit partenaire limitee aux evenements de l'animation, sans donnees internes sensibles ni corrections back-office non publiables.

## 9. Schemas a completer

Schemas a ajouter au DCT :

- `ContextePortailAnimationResponse`
- `NotificationPortailAnimationResponse`
- `ModeleAnimationContextualiseResponse`
- `CommercantEligibleAnimationResponse`
- `CoffretEligibleAnimationResponse`
- `ConfigurationAnimationResponse`
- `ValidationPublicationAnimationResponse`
- `ParticipantAnimationListResponse`
- `ValidationAnimationListResponse`
- `TirageAnimationListResponse`
- `GainAnimationListResponse`
- `AuditAnimationResponse`
- `FlyerAnimationListResponse`
- `BilanAnimationListResponse`
- `AbonnementAnimationResponse`
- `ExportAnimationResponse`

Parametres transverses a standardiser :

- `commune_id`
- `animation_id`
- `periode_debut`
- `periode_fin`
- `modele_code`
- `statut`
- `alerte`
- `resultat`
- `commercant_id`
- `qualifie`
- `termine`
- `page`
- `page_size`
- `sort`

## 10. Priorisation MVP

### Priorite P0

- `GET /protected/animation-locale/contexte-portail`
- `GET /protected/animation-locale/dashboard-performance`
- `GET /protected/animation-locale/communes/{commune_id}/animations`
- `GET /protected/animation-locale/modeles`
- `GET /protected/animation-locale/communes/{commune_id}/commercants-eligibles`
- `GET /protected/animation-locale/communes/{commune_id}/coffrets-eligibles`
- `POST /protected/animation-locale/animations`
- `PATCH /protected/animation-locale/animations/{animation_id}`
- `POST /protected/animation-locale/animations/{animation_id}/publier`
- `GET /protected/animation-locale/animations/{animation_id}/workflow`
- `GET /protected/animation-locale/animations/{animation_id}/live`
- `GET /protected/animation-locale/animations/{animation_id}/participants`
- `GET /protected/animation-locale/animations/{animation_id}/validations`
- `POST /protected/animation-locale/animations/{animation_id}/cloturer`
- `POST /protected/animation-locale/animations/{animation_id}/tirages`
- `POST /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/envoyer`
- `GET /protected/animation-locale/animations/{animation_id}/flyer`
- `GET /protected/animation-locale/animations/{animation_id}/bilan`

### Priorite P1

- vues globales participants, validations, tirages, flyers, bilans, coffrets gagnes ;
- exports CSV ;
- audit partenaire ;
- abonnement detaille ;
- notifications portail.

### Priorite P2

- support partenaire dedie ;
- live avance par SSE/WebSocket ;
- exports asynchrones avec suivi de generation ;
- personnalisation avancee du flyer.

## 11. Recommandations documentaires

### Decisions d'integration validees apres cadrage d'implementation

- L'activation administrative auditee permet de developper et tester les droits d'acces avant la disponibilite des secrets Stripe ; Stripe test et ses webhooks sont raccordes ensuite.
- Les gabarits email et flyer sont versionnes et configurables. Des contenus et assets temporaires sont acceptes pendant le developpement, puis valides avant les recettes metier et visuelle.
- Les URLs et QR publics utilisent deux templates complets configurables, Animation et Participant ; le backend injecte seulement l'identifiant ou le token et HTTPS est requis avant recette de bout en bout.
- Le backend livre les contrats QR avant la premiere version de l'application commercant, qui integre directement les parcours Coffret et Animation sans retrocompatibilite.
- Les purges RGPD sont configurees et testees avec les durees actees ; la validation juridique est un prerequis de production.
- Les fichiers passent par l'abstraction `documentaire`, avec stockage local en developpement et stockage objet prive heberge, accessible de maniere protegee ou par URL signee courte.

1. Mettre a jour le DCT EPIC 41 avec les routes ajoutees dans ce document.
2. Ajouter une section `Animation locale` dans [docs/specifications/fonctionnelle.md](../../produit/specification-fonctionnelle.md) ou creer une specification fonctionnelle EPIC 41 dediee.
3. Decrire explicitement les vues globales du menu partenaire, car elles ne sont pas seulement des raccourcis UI : elles imposent des projections backend.
4. Decrire le masquage des donnees personnelles par ecran et par role.
5. Ajouter les endpoints d'export et leur politique de conservation.
6. Preciser le contrat d'idempotence des actions sensibles : publication, cloture, tirage, envoi gain, regeneration flyer.
7. Aligner les reponses de commande sur la V2 : nouvel etat, prochaine action, ressource produite et statut de traitement/notification.
8. Ajouter aux projections d'alerte et de workflow les cibles de navigation necessaires aux liens profonds de la V2.
