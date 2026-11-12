# Backlog Epic 60 - BackOffice ERP, referencement et commercialisation 360

## Évolution du 12 novembre 2026 — UX quotidienne et productivité

Référence **E60-EVOL-UX-20261112** : [audit ERP](../../audits/backend/localeo-erp-ux-productivite-2026-11-12.md)
et [spécification des six lots](../../specifications/epic-60-vision-360-commercialisation/ux-productivite.md).
L'audit de code/documentation a été suivi d'une demande d'implémentation.
Les six lots sont réalisés dans le backend et vérifiés localement sur fixtures
navigateur, API et PostgreSQL jetable ; les preuves et réserves sont dans le
[bilan d'acceptation](../../specifications/epic-60-vision-360-commercialisation/ux-productivite.md#bilan-dacceptation-local).
**CA-20 reste ouvert**, ainsi que la recette TEST, l'observation humaine et les
mesures de capacité. Aucun gain humain ni déploiement n'est annoncé. La clôture V1
ci-dessous et les identifiants PRD/COM360/ERP-ARB restent inchangés.

| Critère ajouté | Résultat observable attendu | Lot / constat d'audit |
| --- | --- | --- |
| E60-UX-CA-01 | Depuis une recherche Disponibilité/Coffrets/Commerçants, ouvrir une fiche puis revenir restitue l'origine, les filtres, le tri et la page ; une origine interdite utilise un parent autorisé. | L01 / 01 |
| E60-UX-CA-02 | Le retour restaure le focus et la position de la ligne si elle existe ; sinon un repère utile des résultats. Arrivée directe, actualisation et nouvel onglet gardent un retour cohérent. | L01 / 01 |
| E60-UX-CA-03 | Une fiche Utilisateur possède une destination UI stable ; son retour conserve la page et les filtres, sans exposer un compte interdit. | L01 / 13 |
| E60-UX-CA-04 | Une panne temporaire de vérification au retour dans l'onglet propose une reprise, avec saisie masquée en mémoire ; seule la même identité avec droits revalidés peut la retrouver, dans les délais de session. | L02 / 02 |
| E60-UX-CA-05 | 401, refus 403 et CSRF sont distingués ; aucun droit retiré ni aucune donnée interdite n'est restauré, aucune commande n'est rejouée automatiquement. | L02 / 03 |
| E60-UX-CA-06 | Des réponses d'onglets reçues en ordre inverse ne peuvent afficher ni rendre actives les données/actions d'un ancien panneau. | L02 / 10 |
| E60-UX-CA-07 | Un bloc d'accueil indisponible garde une erreur et une reprise locales ; les autres blocs et accès autorisés restent disponibles. | L02 / 04 |
| E60-UX-CA-08 | Un refus de saisie conserve les valeurs et identifie les champs/causes ; un conflit de version propose une reprise explicite sans écrasement. | L03 / 09 |
| E60-UX-CA-09 | Une réponse perdue après enregistrement se résout avec la même clé et le même payload ; une intention n'a pas deux effets, y compris sur les ressources préparées et notifications. | L03 / 08 |
| E60-UX-CA-10 | Après succès, ressource/résultat et prochaine étape sont compréhensibles ; enregistrer n'entraîne ni publication, ni validation fiscale, ni envoi supplémentaire. | L03 / 06, 09 |
| E60-UX-CA-11 | Dossiers à reprendre et alertes précèdent les compteurs à l'accueil ; les applications restent accessibles et le profil Finance ne reçoit pas de données catalogue supplémentaires. | L04 / 04 |
| E60-UX-CA-12 | La file indique son périmètre d'équipe, prochaine action, responsable et échéance, avec absences explicites ; aucune attribution personnelle n'est déduite d'un nom libre. | L04 / 04 |
| E60-UX-CA-13 | « Aller à une fonction » retrouve au clavier les seules destinations ERP autorisées, sans requête globale sur les données métier. | L06 / 14 |
| E60-UX-CA-14 | La recherche catalogue distingue critères courants/avancés et résume les filtres actifs ; réinitialisation/effacement conserve une sémantique API identique et remet page 1. | L05 / 05 |
| E60-UX-CA-15 | Un commerce se sélectionne par nom et commune dans une recherche paginée de 25 résultats ; les réponses périmées sont ignorées et l'UUID reste la valeur de contrat. | L05 / 05 |
| E60-UX-CA-16 | Statuts, verdicts et familles ont des libellés français et tons adaptés, sans confondre brouillon, échec, fiscalité et disponibilité. | L05 / 07 |
| E60-UX-CA-17 | La fiche coffret propose une progression compacte et une aide dépliable ; les contrôles serveur et conséquences BUM restent explicites près des actions concernées. | L05 / 06 |
| E60-UX-CA-18 | Les onglets disposent de relations accessibles complètes, d'un focus clavier cohérent et d'états chargement/vide/erreur ; recette à 320/390/1280 px et texte 200 %. | L06 / 11 |
| E60-UX-CA-19 | La reconnexion peut ramener à une route ERP validée après contrôle des droits ; aucun secret/saisie dans l'URL, aucun retour privé repris par une identité différente. | L01 / 12 |
| E60-UX-CA-20 | Un bilan avant/après mesure réussite sans aide, durée, retours et ressaisies sur les mêmes tâches ; aucun gain n'est annoncé sans mesure ni nouvelle télémétrie sensible. | L04 / transversal |

Les impacts, invariants, contrats, scénarios de refus et limites restent dans
la spécification. Dépôts modifiés : backend ERP et projet documentaire ; les
trois frontends n'ont pas de contrat modifié. Pas de migration ni changement du
générateur : aucune donnée métier ou permission nouvelle. Les fixtures couvrent
les nouveaux états ; la représentativité des données TEST et les gains restent
à observer avec les utilisateurs.

## Livraison V1 — 6 septembre 2026

- Statut : `Termine` pour le développement des 22 stories PRD-561 à PRD-582.
- Spécifications détaillées, interfaces ERP, migration v218 et tests livrés.
- 22 décisions utilisateur et 3 hypothèses complémentaires consolidées sous délégation.
- Bascule directe des anciens ateliers ; procédure de déploiement documentée.
- [Rapport de développement et couverture des stories](../../specifications/epic-60-vision-360-commercialisation/rapport-developpement-v1.md).
- La mesure des gains UX humains avant/après reste une observation après mise en service.

Le cadrage ci-dessous conserve les besoins initiaux. Les spécifications fonctionnelles,
les contrats API et le rapport V1 portent le comportement effectivement livré.

## Fusion des Epics 60 et 61

Decision utilisateur : fusionner les deux epics. L'Epic 60 devient la
reference unique ; l'identifiant 61 reste reserve pour les liens historiques.
Les stories PRD-561 a PRD-582 et les identifiants COM360-* et ERP-ARB-* sont
conserves, avec leurs validations acquises et les hypotheses de livraison tracees.

Le perimetre reunit diagnostic de vendabilite, alertes, atelier coffret
(creation, edition, composition et rentabilite), dossier commercant
(referencement, prestations et aptitude), navigation ERP et suivi d'activite.
La file de diagnostic reste une consultation avec reevaluation ; les ecritures
metier passent par les ateliers dedies au sein de cette meme epic.

La livraison V1 couvre le diagnostic, les commandes de creation/edition, les permissions
et les modeles d'offre. Les contrats effectifs sont documentes dans le dossier unifie.

## Synthese du volet diagnostic

- Criticité : `Haute`
- Statut : `Termine`
- Objectif : permettre à l'exploitation de connaître immédiatement l'état de
  vendabilité de chaque coffret, de comprendre tous ses blocages et d'accéder
  au traitement approprié avant qu'une offre disparaisse silencieusement de la
  Marketplace.
- Domaine principal : `commercialisation`.
- Surfaces MVP : backend, API interne, BackOffice et alertes Localeo Control.
- Dépendances : Epics 1, 15, 27, 28, 33, 35, 39, 44 et 50.

Voir [la spécification fonctionnelle et technique](../../specifications/epic-60-vision-360-commercialisation/README.md)
et [le registre des arbitrages](../../specifications/epic-60-vision-360-commercialisation/registre-arbitrages.md).

## Problème

La vendabilité est aujourd'hui le résultat de contrôles répartis entre le
catalogue, le référencement, Stripe Connect et la conformité BUM. Un coffret
peut ainsi être qualifié fiscalement `VALIDATED` tout en restant exclu de la
Marketplace pour une promesse garantie absente, un commerçant non actif ou un
compte Stripe Connect incomplet.

L'état final n'est pas présenté comme une information opérationnelle de premier
niveau. L'opérateur découvre souvent l'anomalie depuis la Marketplace, puis doit
inspecter plusieurs écrans pour comprendre sa cause.

## Résultat attendu

La Vision 360 Commercialisation fournit :

- une synthèse globale des coffrets vendables et non vendables ;
- une file de traitement ouverte par défaut sur les coffrets bloqués ;
- un diagnostic exhaustif, codé et hiérarchisé pour chaque coffret ;
- l'état des prestations, commerçants, comptes Stripe, qualification BUM,
  données contractuelles, commune et publication ;
- un raccourci de traitement pour chaque cause ;
- une alerte lorsqu'un coffret passe de vendable à non vendable ;
- une date de dernière évaluation et une réévaluation manuelle ;
- une chronologie des changements de vendabilité.

## Perimetre MVP du volet diagnostic

### Pilotage global

- afficher les KPI `Vendables`, `Non vendables`, `Indéterminés`,
  `Nouveaux blocages` et `Blocages critiques` ;
- ventiler les blocages par famille : catalogue, contenu contractuel, BUM,
  commerçant, Stripe Connect, commune et incident technique ;
- filtrer par commune, type de coffret, statut de coffret, famille de blocage,
  code de blocage, commerçant et ancienneté ;
- rechercher par nom, référence ou UUID du coffret ;
- trier en priorité les blocages critiques les plus récents.

### Fiche 360 d'un coffret

- afficher un verdict unique `VENDABLE`, `NON_VENDABLE` ou
  `INDETERMINE` ;
- expliquer chaque blocage avec un libellé opérateur, sa source, sa sévérité,
  sa date d'apparition et la ressource concernée ;
- distinguer clairement le statut fiscal de la vendabilité finale ;
- afficher les contrôles réussis afin d'éviter une analyse par déduction ;
- proposer un lien vers l'écran permettant de traiter le problème ;
- permettre une réévaluation idempotente sans modifier les données métier ;
- afficher la réponse attendue de l'API Marketplace pour la commune concernée.

### Alertes

- créer une alerte lors d'une transition `VENDABLE -> NON_VENDABLE` ;
- créer une alerte distincte lorsqu'un diagnostic devient
  `INDETERMINE` ;
- dédupliquer les alertes tant que l'empreinte des blocages ne change pas ;
- résoudre automatiquement l'alerte lorsque le coffret redevient vendable ;
- rendre l'alerte visible dans le BackOffice et Localeo Control ;
- réserver les notifications WebPush et email à une option paramétrable.

## Hors perimetre du volet diagnostic

- modification en masse des coffrets depuis la Vision 360 ;
- correction automatique de données contractuelles ou fiscales ;
- activation automatique d'un commerçant ou d'un compte Stripe ;
- duplication des règles de vendabilité dans le frontend ;
- remplacement de la Vision 360 Coffret de l'Epic 28 dédiée à la rentabilité ;
- exposition publique des raisons internes de blocage.

## User Stories

### PRD-561 - Consulter la synthèse de vendabilité

En tant que responsable commercialisation, je veux connaître le nombre de
coffrets vendables et non vendables afin de mesurer la disponibilité réelle du
catalogue.

Critères d'acceptation :

- les KPI sont calculés avec le même diagnostic canonique que la Marketplace ;
- chaque KPI est filtrable par commune et type de coffret ;
- la date de dernière évaluation est visible.

### PRD-562 - Prioriser les coffrets non vendables

En tant qu'opérateur exploitation, je veux ouvrir directement la liste des
coffrets bloqués afin de traiter les pertes de disponibilité.

Critères d'acceptation :

- la vue est ouverte par défaut sur `NON_VENDABLE` ;
- les résultats sont paginés, filtrables et triés par sévérité puis ancienneté ;
- chaque ligne affiche le premier blocage et le nombre total de blocages.

### PRD-563 - Comprendre le verdict d'un coffret

En tant qu'opérateur, je veux voir tous les contrôles réussis et échoués afin de
comprendre sans ambiguïté pourquoi un coffret est ou n'est pas vendable.

Critères d'acceptation :

- la qualification `VALIDATED` n'est jamais présentée comme synonyme de
  vendabilité ;
- les blocages possèdent un code stable, une famille et un libellé explicite ;
- un diagnostic incomplet produit `INDETERMINE`, jamais `VENDABLE`.

### PRD-564 - Traiter un blocage

En tant qu'opérateur, je veux accéder au bon écran depuis le blocage afin de
réduire le temps de remise en vente.

Critères d'acceptation :

- chaque code connu possède une cible de traitement ;
- le lien ouvre la ressource et, lorsque possible, la section concernée ;
- l'absence de traitement automatisé est indiquée explicitement.

### PRD-565 - Être alerté d'une perte de vendabilité

En tant que responsable exploitation, je veux être alerté lorsqu'un coffret
disparaît du catalogue afin d'agir avant un signalement externe.

Critères d'acceptation :

- la transition et les causes sont datées et historisées ;
- une cause inchangée ne produit pas plusieurs alertes ouvertes ;
- le retour à `VENDABLE` résout l'alerte et conserve son historique.

### PRD-566 - Réévaluer la vendabilité

En tant qu'opérateur, je veux relancer le diagnostic après une correction afin
de vérifier immédiatement la remise en vente.

Critères d'acceptation :

- la réévaluation réutilise exclusivement le service canonique ;
- l'action est idempotente, auditée et ne modifie aucune donnée métier ;
- le nouveau verdict et la réponse Marketplace attendue sont rafraîchis.

### PRD-567 - Suivre l'historique

En tant que support, je veux consulter les changements de vendabilité afin
d'expliquer quand et pourquoi une offre a disparu puis réapparu.

Critères d'acceptation :

- la chronologie expose ancien et nouveau verdict, empreinte des causes et
  déclencheur ;
- les événements sont paginés et ordonnés du plus récent au plus ancien ;
- les données sensibles Stripe ne sont pas exposées.

### PRD-568 - Contrôler la couverture territoriale

En tant que responsable commercialisation, je veux identifier les communes
publiées sans coffret vendable afin de détecter les trous de catalogue.

Critères d'acceptation :

- la synthèse expose les communes publiées avec zéro coffret vendable ;
- un lien ouvre les coffrets bloqués de la commune ;
- une commune non publiée est distinguée d'une commune sans offre vendable.

### PRD-569 - Sécuriser la Vision 360

En tant que responsable sécurité, je veux réserver cette vision aux profils
internes habilités et auditer les réévaluations.

Critères d'acceptation :

- accès réservé à `ADMIN` et `EXPLOITATION` ;
- aucune donnée personnelle ou secret Stripe n'est exposé ;
- les consultations détaillées et réévaluations sont auditables.

### PRD-570 - Garantir la cohérence avec la Marketplace

En tant que Product Owner, je veux un test de parité entre la Vision 360 et les
routes publiques afin qu'un coffret annoncé vendable soit réellement visible.

Critères d'acceptation :

- les tests couvrent chaque code de blocage et leurs combinaisons ;
- un test d'intégration compare le verdict avec
  `GET /public/commercialisation/coffrets` ;
- toute nouvelle règle de vendabilité exige un code, un libellé et une cible de
  traitement avant livraison.

## Lots du volet diagnostic

| Lot | Contenu | Dépendances |
| --- | --- | --- |
| C0 | Vocabulaire, codes, sévérités, parité du diagnostic et OpenAPI | Arbitrages P0 |
| C1 | Projection courante, recalcul événementiel et batch de réconciliation | Epics 44 et 48 |
| C2 | API de synthèse, recherche et détail 360 | C0, C1 |
| C3 | Interface BackOffice et raccourcis de traitement | C2, Epic 35 |
| C4 | Alertes BackOffice et Localeo Control, résolution automatique | C1, Localeo Control |
| C5 | Chronologie, couverture territoriale, tests de parité et exploitation | C1 à C4 |

## Definition de termine du volet diagnostic

- aucun coffret non vendable ne disparaît silencieusement de la Marketplace ;
- la liste des coffrets bloqués est accessible en un clic depuis le BackOffice ;
- chaque exclusion possède au moins un code stable et un motif intelligible ;
- chaque code connu indique une action ou une procédure de traitement ;
- les transitions de vendabilité produisent des alertes dédupliquées ;
- le verdict 360 et le comportement des routes publiques sont couverts par un
  test de parité ;
- les performances p95 respectent 500 ms pour la liste et 800 ms pour le
  détail sur le volume de référence ;
- la sécurité, l'audit, l'OpenAPI et la procédure opérationnelle sont livrés.



## Volet ERP et referencement (issu de l'Epic 61)

## Iteration 2 - parcours directeur et priorites

Le parcours directeur est `Referencer -> Preparer l'offre -> Verifier ->
Publier -> Honorer -> Suivre`. La [revue produit](../../specifications/epic-60-vision-360-commercialisation/revue-produit-iteration-2.md)
challenge le cadrage initial a partir du code Localeo. Ses recommandations
sont desormais consolidees selon les decisions utilisateur dans le cadrage V1.

- Integrer le dossier, les commandes et les capacites Onboard existants ;
  ne pas recreer un processus parallele ni une table de taches.
- Distinguer diagnostic courant et verification de l'etat cible avant mise
  en vente ; un brouillon peut etre pret a activer sans etre deja vendable.
- Distinguer preparation normale et perte de disponibilite, en conservant
  NON_VENDABLE comme ouverture par defaut de la file diagnostic.
- Analyser separement les consequences sur les ventes futures et les achats
  deja engages, y compris lors d'un archivage ou retrait.
- Livrer un parcours vertical complet en priorite ; la refonte exhaustive
  des menus ne conditionne pas sa premiere recette.

Les 22 stories sont conservees et precisees, sans nouvelle numerotation.

## Demande et resultat attendu

L'operateur doit pouvoir accomplir une tache metier sans reconstruire un
parcours entre des tables CRUD. Il dispose de deux ateliers principaux :

- **Dossier commercant** : creer ou modifier le commercant, preparer et
  modifier ses prestations, verifier son aptitude a rejoindre l'ecosysteme,
  traiter les pieces et actions manquantes puis suivre son activite.
- **Dossier coffret** : creer ou modifier le coffret, composer ses prestations,
  mesurer sa rentabilite et sa vendabilite, traiter les blocages puis publier
  par une action explicite et controlee.

La navigation distingue gestion operationnelle, supervision et referentiels.
L'accueil expose les taches et actions frequentes plutot qu'un catalogue de
tables. Les fonctions existantes restent accessibles selon les habilitations.

## Perimetre MVP retenu pour specification

- Accueil de travail, navigation par missions, recherche et actions rapides.
- Dossier commercant unifie : identite, offre, preparation, documents,
  habilitations, prochaine action et acces a l'activite 360 existante.
- Creation et edition guidees avec brouillons reprenables, validations de
  champs et controle des consequences avant activation.
- Creation et edition de prestations dans le contexte du commercant ;
  selection et rattachement depuis le coffret, sans duplication involontaire.
- Dossier coffret unifie : informations, composition, reversements et marge,
  diagnostic de vendabilite Epic 60, preparation et publication.
- Diagnostic d'aptitude commercant par dimensions, sans confusion entre
  dossier complet, compte Stripe pret, statut ACTIF et offre vendable.
- Suivi leger du referencement : responsable habilite, prochaine action,
  echeance, notes existantes et files des dossiers a reprendre.
- Separation visuelle et fonctionnelle des referentiels avances et des
  outils de supervision ; remplacement des anciennes destinations et mise a jour des liens internes.

## Hors perimetre initial

- ERP comptable general, achats fournisseurs, stocks physiques ou paie.
- CRM de prospection complet, automatisation de campagnes et relances massives.
- Refonte des applications publiques ou du portail commercant.
- Remplacement des regles fiscales, financieres, de publication ou d'acces.
- Activation automatique, correction automatique de conformite ou migration
  automatique de prestations deja vendues.
- Remplacement de FastAPI/SQLAdmin ou ajout d'une stack frontend sans decision.

## User Stories initiales

| ID | Besoin | Criteres d'acceptation initiaux |
| --- | --- | --- |
| PRD-571 | Ouvrir un espace de travail oriente actions | L'accueil expose dossiers a reprendre, echeances et actions autorisees ; compteur et liste de destination ont le meme perimetre |
| PRD-572 | Naviguer par mission | Gestion, supervision et referentiels sont separes ; nouveaux parcours remplaçant les anciens sans coexistence ; liens internes actualises ; une ressource garde une fiche canonique |
| PRD-573 | Creer ou modifier un commercant depuis sa fiche 360 | Creation en BROUILLON, sauvegarde et reprise possibles ; validations explicites ; aucune publication implicite |
| PRD-574 | Creer ou modifier une prestation depuis le commercant | Proprietaire preselectionne et controle ; version active preservee jusqu'a validation selon les regles existantes ; coffrets affectes visibles |
| PRD-575 | Diagnostiquer l'aptitude du commercant | Reutiliser les capacites Onboard ; chaque dimension affiche etat, motif, source, date et action ; absence de vente n'est pas un incident ; information inconnue jamais assimilee a une validation |
| PRD-576 | Piloter le dossier de referencement | Meme dossier et cycle Onboard depuis toutes les entrees ; prochaine action, responsable et echeance existants exposes ; cloture/abandon distincts du statut commercant ; aucune affectation nominative supposee a partir d'un texte |
| PRD-577 | Creer ou modifier un coffret depuis sa fiche 360 | Parcours informations, composition, economie et controles ; brouillon reprenable ; modification concurrente detectee |
| PRD-578 | Composer le coffret depuis les offres commercants | Rattachement avec provenance/version et conditions propres selon ERP-ARB-02 ; aucune propagation silencieuse ; effets du retrait separes entre ventes futures et engagements existants |
| PRD-579 | Voir la rentabilite pendant la composition | Calcul canonique Epic 28 ; marge sur prix, commission theorique et flux reels distingues ; frais non integres explicites ; plafond absolu respecte et degradation autorisee confirmee/auditee |
| PRD-580 | Verifier puis publier le coffret | Diagnostic courant distinct de la simulation cible ACTIVE ; recontrole des sources, droits et version lors de la commande atomique ; conflit sans activation partielle ; aucune activation implicite des autres ressources |
| PRD-581 | Acceder rapidement aux actions courantes | Creer commercant/coffret, reprendre un dossier, traiter un blocage, retrouver un achat et preparer les reversements sont accessibles selon les droits |
| PRD-582 | Securiser et mesurer les nouveaux parcours | Cloisonnement territorial, permissions par action, audit, CSRF et non-regression ; mesure du temps de parcours et des abandons |

## Lots du volet ERP

| Lot | Contenu | Condition de sortie |
| --- | --- | --- |
| E0 | Inventaire des menus, parcours observes, permissions et arbitrage modele de prestation | Cartographie ancien/nouveau et scenarios de recette valides |
| E1 | Navigation et accueil de travail, raccourcis vers fonctions existantes | Toutes les fonctions utiles reintegrees dans la nouvelle console, aucun contournement de droits |
| E2 | Dossier commercant et suivi de preparation | Creation/reprise/edition et diagnostic explicable utilisables |
| E3 | Offre commercant et composition coffret | Modele de prestation tranche, versions et rattachements proteges |
| E4 | Dossier coffret, economie et integration Epic 60 | Creation -> controles -> publication recettee sans duplication de regles |
| E5 | Harmonisation, accessibilite, formation et mesure | Recette transverse, aide operationnelle et indicateurs de parcours livres |

Les lots C0-C5 et E0-E5 appartiennent a la meme Epic 60. Le diagnostic
peut etre developpe et recette avant les ateliers, sans clore l'epic ni
maintenir deux interfaces en production. Les anciennes Epics
27 et 28 restent terminees ; leurs enrichissements sont suivis ici.

## Definition de termine cible

- Un nouvel operateur peut referencer un commercant et preparer un coffret
  depuis les parcours guides sans devoir connaitre les noms des tables.
- Il retrouve sans ambiguite ses dossiers incomplets et leur prochaine action.
- Chaque refus de publication/activation explique sa cause et le traitement.
- Rentabilite et vendabilite restent distinctes et coherentes avec leurs
  moteurs canoniques ; les achats existants conservent leurs engagements.
- Les menus sont adaptes aux permissions sans que masquer un bouton remplace
  une autorisation serveur ; les anciennes interfaces sont retirees lors de la bascule.
- La recette couvre creation, modification, reprise, concurrence, droits,
  publication et retour aux parcours operationnels.
- Les gains de temps sont mesures sur un protocole de parcours avant/apres.


## Pilotage et definition de termine unifies

- [Analyse des parcours ERP](../../specifications/epic-60-vision-360-commercialisation/analyse-parcours-erp.md).
- [Registre unique des arbitrages](../../specifications/epic-60-vision-360-commercialisation/registre-arbitrages.md).
- [Plan de livraison unifie](../../specifications/epic-60-vision-360-commercialisation/plan-livraison-unifie.md).
- Dependances consolidees : Epics 1, 3, 15, 27, 28, 33, 35, 38, 39, 44, 48 et 50.
- L'epic est terminee lorsque les deux definitions de termine sont satisfaites
  et que le parcours referencement -> composition -> controles -> publication
  -> suivi est recette de bout en bout.
