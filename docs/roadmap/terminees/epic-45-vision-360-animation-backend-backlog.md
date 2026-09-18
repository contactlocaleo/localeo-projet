# Backlog Epic 45 - Vision 360 Animation backend

## Synthese

- Criticite : `Haute`
- Statut : `Termine`.
- Objectif : fournir au back-office Localeo une vue 360 consolidee d'une animation, couvrant sa situation courante, son historique, ses performances et ses alertes operationnelles.
- Vocabulaire : `Vision 360 Animation` designe une vue interne centree sur tous les aspects utiles d'une animation. La periode d'analyse est un filtre et ne definit pas le nom du produit.
- Domaine fonctionnel : `animation_locale`.
- Surface initiale : backend et API interne ; l'interface back-office sera traitee dans un lot ulterieur.
- Epic source : Epic 41 pour les animations, participants, validations, tirages, gains, abonnements, tenants et audits.

## Probleme

Les donnees d'une animation existent mais sont reparties entre la fiche, le pilotage live, les participants, les validations, les operations, les tirages, les gains, les emails et les audits. Un operateur support ou exploitation ne dispose pas d'un point d'entree unique pour comprendre rapidement :

- qui porte l'animation et sur quel territoire ;
- ou elle se situe dans son cycle de vie ;
- si sa configuration et sa publication sont coherentes ;
- combien de participants sont inscrits et progressent ;
- quels incidents ou actions restent a traiter ;
- quels tirages, gagnants et gains ont ete produits ;
- quelles communications et operations techniques ont echoue ;
- comment ses performances se comparent a ses animations precedentes.

## Positionnement par rapport a l'Epic 41

- Le `pilotage live` sert a conduire une animation en cours, avec des donnees recentes.
- Le `bilan` sert a restituer le resultat d'une animation cloturee.
- Le `dashboard de performance` compare plusieurs animations d'un gestionnaire.
- La `Vision 360 Animation` est une surface interne support/exploitation centree sur une animation, navigable sur toute sa chronologie et capable de consolider les signaux des trois vues precedentes.
- Les calculs et projections existants sont reutilises ; cette epic ne cree pas une seconde source de verite analytique.

## Perimetre MVP backend

- Rechercher une animation par reference, nom, partenaire, commune, statut ou periode.
- Retourner une synthese d'identite : reference, nom, modele, partenaire, commune, abonnement, statut et workflow.
- Exposer la configuration courante et son historique de versions, avec les changements critiques.
- Exposer les KPI sur une periode explicite et bornee : inscriptions, participants actifs/termines/qualifies, validations, taux de completion, abandons, tirages et gains.
- Exposer les series temporelles journalieres necessaires aux graphiques sans effectuer les calculs dans le frontend.
- Exposer les participants et validations recents sous forme paginee, en appliquant le masquage des donnees personnelles selon l'habilitation.
- Exposer la chronologie consolidee : creation, configuration, publication, inscriptions, validations, cloture, tirages, gains, communications, operations et audits pertinents.
- Exposer les alertes et anomalies actionnables avec severite, code stable, date, objet concerne et lien de resolution.
- Exposer les tirages, gagnants, coffrets attribues et etat de consommation des gains.
- Exposer le potentiel financier restant des gains, les coffrets entierement non consommes proches expiration, le delai de premiere consommation, les commercants participants effectifs sans validation et la repartition du montant reinjecte par commercant.
- Exposer la sante des communications et traitements : emails, operations planifiees, echecs temporaires/definitifs et dernieres reprises.
- Fournir des liens techniques vers les ressources back-office existantes sans dupliquer leurs actions metier.
- Auditer les consultations contenant des donnees personnelles et les futures actions sensibles.

## Hors perimetre MVP

- Modification directe des donnees depuis l'agregat de consultation.
- Duplication des tables metier dans un datamart propre a la vision.
- Scoring predictif, recommandation automatique ou intelligence artificielle.
- Export nominatif massif des participants.
- Comparaison avancee entre partenaires ou communes.
- Acces public, participant ou gestionnaire partenaire a la vue interne.
- Conservation de donnees nominatives au-dela des regles de l'Epic 41.

## Contrat API cible

Les chemins sont proposes et doivent etre confirmes par arbitrage :

| ID | Methode et chemin | Finalite |
| --- | --- | --- |
| AN360-API-001 | `GET /internal/animation-locale/vision-360/animations` | Rechercher et filtrer les animations. |
| AN360-API-002 | `GET /internal/animation-locale/vision-360/animations/{animation_id}` | Charger la synthese consolidee. |
| AN360-API-003 | `GET /internal/animation-locale/vision-360/animations/{animation_id}/chronologie` | Charger la chronologie paginee et filtree. |
| AN360-API-004 | `GET /internal/animation-locale/vision-360/animations/{animation_id}/indicateurs` | Charger les KPI et series sur une periode bornee. |
| AN360-API-005 | `GET /internal/animation-locale/vision-360/animations/{animation_id}/participants` | Charger les participants pagines et masques selon habilitation. |
| AN360-API-006 | `GET /internal/animation-locale/vision-360/animations/{animation_id}/alertes` | Charger les alertes et anomalies actionnables. |

Les reponses doivent partager :

- un `generated_at` et la periode effectivement appliquee ;
- des identifiants UUID et codes metier stables ;
- des listes paginees, jamais non bornees ;
- des montants avec devise lorsqu'un gain possede une valeur ;
- des dates ISO 8601 en UTC ;
- un `correlationId` sur les erreurs selon l'Epic 44.

## User Stories

### PRD-405 - Rechercher une animation

En tant qu'operateur Localeo, je veux rechercher une animation afin d'ouvrir rapidement sa Vision 360.

Resultats attendus :

- la recherche accepte reference, nom, partenaire et commune ;
- les filtres statut et periode sont combinables ;
- les resultats sont pagines et limites aux perimetres autorises.

### PRD-406 - Consulter la synthese consolidee

En tant qu'operateur, je veux comprendre l'identite et l'etat de l'animation en un coup d'oeil.

Resultats attendus :

- la synthese expose partenaire, commune, abonnement, modele, configuration et workflow ;
- les prochaines actions et blocages sont explicites ;
- aucune donnee n'est dupliquee dans une nouvelle source de verite.

### PRD-407 - Analyser les indicateurs dans le temps

En tant que responsable exploitation, je veux analyser les indicateurs et leur evolution afin d'evaluer l'animation.

Resultats attendus :

- les periodes predefinies couvrent 7, 30, 90 et 365 jours ainsi qu'une periode personnalisee bornee ;
- les KPI et series utilisent les memes definitions que le pilotage et le bilan de l'Epic 41 ;
- les indicateurs economiques et d'usage des gains reutilisent les definitions opposables de l'Epic 41 et indiquent devise, horizon et taille d'echantillon ;
- le fuseau et les bornes de periode sont explicites.

### PRD-408 - Parcourir la chronologie complete

En tant que support, je veux parcourir les evenements de l'animation afin de reconstruire son histoire.

Resultats attendus :

- la chronologie consolide workflow, participants, validations, operations, communications, tirages, gains et audits pertinents ;
- elle est paginee et filtrable par type, severite et periode ;
- chaque evenement pointe vers sa ressource source quand elle est consultable.

### PRD-409 - Consulter participants et progression

En tant qu'operateur habilite, je veux consulter les participants et leur progression afin de traiter les demandes de support.

Resultats attendus :

- les participants sont pagines et recherchables selon les droits ;
- les coordonnees sont masquees par defaut et l'acces complet est audite ;
- inscription, progression, qualification, QR et statut de gain sont distingues.

### PRD-410 - Superviser tirages et gains

En tant qu'operateur, je veux suivre les tirages et gains afin d'identifier ce qui reste a attribuer ou envoyer.

Resultats attendus :

- tirages, gagnants, coffrets attribues et consommation sont relies ;
- le montant potentiel restant, les expirations proches et la repartition du montant reinjecte sont reconciliables prestation par prestation ;
- les echecs ou incoherences sont exposes sous forme d'alertes ;
- la vue reutilise les actions metier existantes et ne declenche aucun tirage a la consultation.

### PRD-411 - Identifier les anomalies actionnables

En tant que responsable exploitation, je veux voir les anomalies prioritaires afin de traiter rapidement les blocages.

Resultats attendus :

- chaque alerte possede un code, une severite, une date, un statut et une ressource ;
- les alertes couvrent configuration, abonnement, workflow, communications, operations, tirages et gains ;
- les regles sont testables et ne dependent pas de libelles libres.

### PRD-412 - Securiser et exploiter l'API interne

En tant que responsable securite, je veux que la Vision 360 respecte les habilitations et soit observable.

Resultats attendus :

- les routes sont reservees aux roles internes autorises ;
- le tenant et la commune ne peuvent pas etre contournes par un identifiant direct ;
- les donnees personnelles, consultations sensibles, erreurs et performances sont auditees ou journalisees selon leur finalite.

## Decoupage propose

| Lot | Contenu | Dependances |
| --- | --- | --- |
| B0 | Contrats, vocabulaire, habilitations, definitions des KPI et OpenAPI | Arbitrages AN360-ARB-01 a 18 valides |
| B1 | Recherche et synthese consolidee | Epic 41, referentiels partenaire/commune/abonnement |
| B2 | KPI et series temporelles sur des periodes bornees | Pilotage et bilan Epic 41 |
| B3 | Chronologie multi-sources | Audit, operations, emails, tirages et gains |
| B4 | Participants, progression et protection des donnees | Politique RGPD Epic 41, profils back-office |
| B5 | Alertes, performances, cache court et observabilite | Epic 44 |
| B6 | Tests de contrat, integration, charge et documentation d'exploitation | Lots B0 a B5 |

## Arbitrages valides

| ID | Arbitrage | Priorite | Proposition | Validation / amendement |
| --- | --- | --- | --- | --- |
| AN360-ARB-01 | Population utilisatrice | P0 | Limiter le MVP aux roles internes `ADMIN` et `EXPLOITATION`; masquer les donnees pour les autres profils. | Valide le 2026-08-19 |
| AN360-ARB-02 | Profondeur historique | P0 | Proposer 7, 30, 90 et 365 jours, tout en respectant les durees de conservation plus courtes des donnees nominatives. | Valide le 2026-08-19 |
| AN360-ARB-03 | Niveau de donnees personnelles | P0 | Masquer par defaut ; permettre l'affichage complet uniquement a `ADMIN`, avec audit de la consultation. | Valide le 2026-08-19 |
| AN360-ARB-04 | Fraicheur des donnees | P1 | Calcul a la demande avec cache court de 60 secondes pour les agregats lourds ; pas de cache long pour chronologie et participants. | Valide le 2026-08-19 |
| AN360-ARB-05 | Actions depuis la vision | P1 | Consultation et liens uniquement au MVP ; reutiliser les use cases existants pour toute action. | Valide le 2026-08-19 |
| AN360-ARB-06 | Comparaison | P1 | Reporter la comparaison interanimations apres le MVP ; centrer la premiere version sur une animation. | Valide le 2026-08-19 |
| AN360-ARB-07 | Export | P2 | Exclure l'export nominatif ; envisager plus tard un export agrege CSV/PDF. | Valide le 2026-08-19 |
| AN360-ARB-08 | Identifiant de recherche | P0 | Ajouter a l'animation une reference metier immutable et unique au format `ANIM-XXXXXXXX`, en complement de l'UUID. | Valide le 2026-08-19 |
| AN360-ARB-09 | Definitions des KPI | P0 | Reutiliser strictement les definitions et calculs du pilotage et du bilan de l'Epic 41 pour participant actif, abandon, progression, completion, qualification, validation et gain envoye. | Valide le 2026-08-19 |
| AN360-ARB-10 | Cloisonnement territorial | P0 | `ADMIN` voit toute la plateforme ; `EXPLOITATION` ne voit que les communes auxquelles son profil est habilite ; aucun acces partenaire au MVP. | Valide le 2026-08-19 |
| AN360-ARB-11 | Contrat des routes | P0 | Retenir le prefixe `/internal/animation-locale/vision-360` et les six endpoints `AN360-API-001` a `AN360-API-006`. | Valide le 2026-08-19 |
| AN360-ARB-12 | Taxonomie des alertes | P1 | Utiliser des codes stables et une severite pour les alertes de configuration, abonnement, workflow, communication, operation, tirage et gain. | Valide le 2026-08-19 |
| AN360-ARB-13 | Contenu de la chronologie | P1 | Consolider workflow, inscriptions, validations, communications, operations, tirages, gains et audits, avec filtres par type et periode. | Valide le 2026-08-19 |
| AN360-ARB-14 | Pagination | P1 | Utiliser une pagination par curseur pour chronologie et participants, et une pagination page/taille pour la recherche d'animations. | Valide le 2026-08-19 |
| AN360-ARB-15 | Association a l'abonnement | P1 | Afficher l'abonnement applicable au couple partenaire-commune au moment courant, sans creer de rattachement redondant sur l'animation. | Valide le 2026-08-19 |
| AN360-ARB-16 | Budget de performance | P1 | Cibler moins de 500 ms pour synthese/recherche et moins de 1,5 s pour les agregats sur 365 jours ; ajouter des index avant toute projection dediee. | Valide le 2026-08-19 |
| AN360-ARB-17 | Conservation de la chronologie | P2 | Respecter la conservation de chaque source ; ne jamais reconstituer une donnee deja anonymisee. | Valide le 2026-08-19 |
| AN360-ARB-18 | Liens back-office | P2 | Retourner types et identifiants de ressources ; laisser le frontend construire les URL pour eviter un couplage a SQLAdmin. | Valide le 2026-08-19 |
| AN360-ARB-19 | Definition des indicateurs economiques et d'usage | P0 | Utiliser les gains envoyes non suppleants et leurs prestations courantes ; sommer les montants de reversement snapshots en centimes, compter uniquement les commercants ayant accepte leur invitation, retenir 30 jours par defaut pour l'expiration et accompagner toute moyenne de son echantillon. | Valide par ajout au perimetre le 2026-08-28 |

## Definition de termine

- les contrats OpenAPI sont valides et versionnes ;
- les calculs reutilisent les regles de l'Epic 41 et possedent des tests de non-regression ;
- toutes les listes sont paginees et les periodes bornees ;
- les habilitations, le cloisonnement territorial et le masquage sont testes ;
- les requetes lourdes possedent des budgets de performance mesures ;
- les consultations sensibles sont auditees et les erreurs correlables ;
- la documentation d'exploitation decrit les sources, la fraicheur et les limites de chaque indicateur.

## Etat d'implementation

Les lots B0 a B6 sont implementes cote backend :

- reference metier `ANIM-XXXXXXXX`, migration de rattrapage et index de lecture ;
- recherche paginee et synthese consolidee ;
- KPI, series temporelles et cache court de 60 secondes ;
- chronologie et participants pagines par curseur ;
- masquage des coordonnees, consultation complete reservee a `ADMIN` et audit ;
- alertes de configuration, abonnement, operations, notifications et gains ;
- routes internes et cloisonnement communal du role `EXPLOITATION` ;
- contrat OpenAPI, tests de service, de routes et de migration, documentation d'exploitation.

L'extension `AN360-ARB-19` est specifiee mais n'est pas encore implementee : le service, les modeles de reponse et les tests doivent encore exposer les cinq indicateurs de `consommation_financiere` et le parametre `horizon_expiration_jours`.

La compilation syntaxique est validee. L'execution de `pytest`, la migration sur PostgreSQL et les mesures de charge doivent etre realisees dans l'environnement Python applicatif partage.
