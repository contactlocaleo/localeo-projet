# EPIC 71 — CRM de prospection

Version de conception : **V0.3 — 9 octobre 2026**. Source : [backlog E71](../../roadmap/a-faire/epic-71-crm-prospection-animation-coffrets-pro-backlog.md), critères **E71-CA-01 à 24** conservés. L'état produit reste **À faire** dans la [roadmap](../../roadmap/README.md).

Cette spécification détaille une cible ; elle ne constate ni implémentation, ni import réel, ni validation des propositions de cadrage. Les décisions utilisateur du 9 octobre sur gain, droits et conversion sont intégrées ci-dessous ; les autres propositions restent identifiées. Le fichier privé Gironde a été relu le 9 octobre pour E71-EVOL-02 ; il n’a été ni modifié ni copié dans Git.

## Évolution E71-EVOL-01 — import mensuel

Demande utilisateur du 9 octobre : réception mensuelle du classeur Gironde, chargement simple et gestion des deltas préservant les modifications CRM. [Parcours détaillé](import-carte.md) : profil mémorisé, comparaison à trois versions par champ, conflits explicites, aucune suppression des absents, reprise idempotente. Cette décision précise ARB-01 et CA-08 à 12/24 ; elle ne tranche pas les autres arbitrages.

## Évolution E71-EVOL-02 — deux destinations distinctes

Décision du 9 octobre : import structuré exclusivement depuis **Pipeline qualifié** ; les 33 colonnes de **Coffrets & élus 2026** alimentent une section dédiée de chaque fiche commune CRM, avec rattachement confirmé et deltas mensuels par champ. Autres onglets exclus. [Analyse et mapping complets](import-carte.md). Classeur relu sans modification le 9 octobre.

## Lecture

| Document canonique | Contenu |
| --- | --- |
| [Parcours et règles](parcours-regles.md) | Acteurs, étapes, tâches, opposition, UX et indicateurs |
| [Architecture et contrats](architecture-contrats.md) | Existant vérifié, agrégats, API cible, droits, concurrence et intégrations |
| [Import et carte](import-carte.md) | Mapping Gironde, rapprochement, reprise, localisation et limites techniques |
| [Vérification et livraison](verification-livraison.md) | Traçabilité des 24 critères, tests à produire, données, conservation et activation |

## Acquis et périmètre

Acquis du cadrage : prospection Animation, commerçants partenaires et **coffrets achetés par entreprises/CSE** ; tâches et rappels internes ; import XLSX contrôlé ; carte de France et historique. Aucun message externe, compte, commande ou abonnement ne découle d'un import. « Pro » ne désigne pas les accès salariés E72.

Le backend et son ERP constituent le périmètre applicatif direct. Les parcours OnBoard, Animation et Achats sont des destinations métier, pas des bases CRM. Les interfaces publiques Animation, Commerçant et Marketplace n'exposent pas les prospects et ne nécessitent pas de nouveau contrat en V1 proposée. Une création métier intégrée supplémentaire doit être conçue avant son développement.

## Décisions restant à prendre

Chaque ligne distingue **décision validée** et **proposition restante**. Les choix techniques bornés de la conception peuvent être affinés avec des mesures ; les règles métier ne peuvent pas être choisies silencieusement pendant l'implémentation.

| ID du backlog | Proposition de cette version | Partie bloquée / décision attendue |
| --- | --- | --- |
| E71-ARB-01 | XLSX seul en V1 ; mapping explicite par onglet et exceptions de ligne ; 10 Mio compressés et 10 000 lignes métier par lot comme cible technique initiale | Valider colonnes/enrichissements et volume réel ; CSV reste hors contrat proposé ; import réel interdit tant que le mapping pilote n'est pas approuvé |
| E71-ARB-02 | **Acquis** : achats de coffrets entreprises/CSE | Aucun arbitrage sur le sens de Pro |
| E71-ARB-03 | **Acquis** : rappels internes ; proposer une file ERP calculée, sans résumé email V1 | Confirmer l'absence de résumé email ; la file et les échéances peuvent être conçues indépendamment |
| E71-ARB-04 | **Gain validé le 9 octobre** : référencement accepté + dossier OnBoard lié ; souscription Animation activée payée/gratuite ; commande Pro payée. Trois axes retenus | Parcours d’étapes détaillé proposé ; adaptation des preuves canoniques et décision d’acceptation explicite décrites dans l’architecture |
| E71-ARB-04b | Complément proposé : une seule opportunité gagnée par preuve de vente | Décider l’unicité inter-affaires, distincte de l’idempotence sur une même opportunité |
| E71-ARB-05 | **Validé le 9 octobre** : Backoffice consulte/gère/importe ; Lecteur consulte fiches/contacts ; Finance sans accès implicite ; admin corrections sensibles/oppositions ; droits métier additionnels pour conversion | Ajouter les scopes et contrôles E69 ; aucun accès SQLAdmin implicite |
| E71-ARB-06 | Carte communale ; une commune principale facultative par organisation ; liste utilisable partout, vues Outre-mer distinctes si couverture retenue | Confirmer Outre-mer, multi-sites et volume/utilisateurs ; choisir fournisseur, licence et contrat de couverture avant carte exploitable |
| E71-ARB-07 | Opposition organisation/contact, par canal et axe ou globale ; levée admin motivée avec preuve ; conservation configurable par catégories | Valider la portée d'opposition et les durées/déclencheurs de purge CRM avec le responsable de politique Localeo ; pas de durée inventée par analogie avec les achats |
| E71-ARB-08 | **Validé le 9 octobre** : rattacher un objet existant ou ouvrir son parcours actuel puis rattacher le résultat ; aucune création automatique CRM | Reprise de lien et droits métier à implémenter ; aucune transaction inter-domaines atomique promise |

## Préparation de l'implémentation

La conception indépendante couvre séparation des objets, absence d'effets externes implicites, provenance, concurrence, contrôle d'import, navigation ERP et matrice de tests. **L'epic complète n'est pas encore prête à implémenter** : ARB-07 conditionne opposition/conservation, ARB-01/06 le pilote import/carte ; les étapes détaillées et limites techniques restent proposées. Gain, droits et profondeur de conversion sont décidés. Un socle technique peut être préparé derrière une option désactivée, sans importer de contacts réels ni figer les règles en attente.

Ordre proposé : domaine et droits → portefeuille/historique/tâches → import → carte et rattachements → démonstration et recette. Livrer le portefeuille seul ne clôture pas les 24 critères.
