# Moteur d’animation — compte rendu d’implémentation

Branche commune : `feat-moteur-animation`, dans les cinq dépôts indépendants. Source de vérité : [spécification](localeo_animation_engine_spec.md), [conception technique](conception-technique.md) et [documents d’entrée](contrats/README.md). Ce suivi distingue code local vérifié, fonctionnalités raccordées et recette avant ouverture.

## 24 septembre 2026 — E55-UX-08 : sélections et navigation communes

Évolution [T6-UX08](conception-technique.md#t6-ux08--sélections-et-fil-dariane-communs-e55-ux-08)
de l’[epic 55](../../roadmap/en-cours/epic-55-chasse-tresor-commercante-backlog.md),
vérifiée localement sur les arbres de travail à partir d’Animation `ef5bbc7`
et Projet `b8ac7db`. Le statut de l’epic et sa recette terrain restent inchangés.

Les sélecteurs partagés remplacent les variantes de création/configuration.
Les fiches marchands s’ouvrent depuis les sélections et les prestations des
coffrets. Le catalogue marchand parcourt toutes les pages. Le fil d’Ariane
partagé reprend le Passeport sur bureau/mobile ; la Chasse conserve ses phases
de génération puis de préparation. Ses cinq premières rubriques de création
sont Modèle, Commune, Informations, Commerçants et Mission & règles, puis le
récapitulatif précède la demande explicite de proposition.

| Critères | Preuves exécutées dans `localeo-animation` | Résultat |
| --- | --- | --- |
| A, B, C | `node tests/browser/animation-selection.mjs` | Passeport à 390/1280 px : sélection clavier, inéligibilité, popins chargées à l’ouverture, erreur/réessai, focus, fiche marchand imbriquée, quantités et retours sans mutation. |
| A, B, D | `node tests/browser/animation-lots.mjs` | Tombola, détails et configuration : choix/quantités persistés, retrait des coffrets absents, concurrence paiement et verrous après paiement/publication ; mobile et bureau. |
| A, C, D | `node tests/browser/generation-preparation.mjs` | 34 contrôles à 390/1280 px ; brief guidé, réutilisation, confirmations et réconciliation préservés. |
| A, C, D | `node tests/browser/hunt-preparation.mjs` | 194 contrôles à 390/1280 px ; navigation, conservation des brouillons, commandes incertaines, financement et contrôles de préparation. |
| C, D | `node tests/browser/leo-assistant.mjs` | Trois modèles, entrée Passeport/Tombola manuelle et Chasse avec Léo, mobile/bureau. |
| D | `node --test tests/*.test.mjs` | 161 tests réussis, aucun échec ni test ignoré ; pagination, lecture seule, éligibilité, prix partiels et contrats inclus. |
| D | TypeScript, ESLint et `node scripts/build-generation-tests.mjs` | Réussis ; avertissement de bundle supérieur à 500 ko déjà présent avant cette évolution. |

Les captures de sélection, détail et navigation ont été inspectées aux deux
tailles. La revue indépendante de l’intégration a relevé un message vide
ambigu en consultation ; corrigé pour distinguer catalogue vide et absence
de sélection. Deux attentes anciennes de la recette lots ont été actualisées :
les sélections sont désormais des cases natives et une animation publiée
propose les paramètres d’exploitation, sans bouton de modification des lots.
Le réessai de deux fiches marchands attend chaque résultat avant le suivant.

Contrôles documentaires réussis : `check_guidance.py` et
`sync_documentation.py --check-sources` (117 sources). Dépôts modifiés :
`localeo-animation` et `localeo-projet`. Aucun contrat de commande, schéma,
permission, migration ou générateur modifié ; les autres applications sont
sans impact. Ces recettes utilisent des API simulées et ne constituent pas
une recette sur environnement déployé. Aucun commit, push ou déploiement
réalisé pour cette évolution.

### Complément E55-UX-08 — agencement des pages et fiche commerçant

Sur la base Animation `0d9f95c`, le passage à Commune dans la Chasse déplaçait
le fil d’Ariane sous l’aide Léo et dans une colonne plus étroite. Reproduction
navigateur avant correction à 1280 px : ordonnée 267 px au lieu de 149 px,
largeur 915 px au lieu de 1070 px ; le pied de navigation commun était absent.

`AnimationCreationLayout` est désormais utilisé par Passeport, Tombola et
Chasse : même en-tête, navigation immédiatement dessous, contenu centré et
défilant, commandes en bas. L’aide Léo et le quota sont dans le contenu. Le
formulaire Chasse reste associé à ses boutons de soumission par son ID natif,
avec validations et commandes explicites inchangées. La demande complémentaire
retire l’affichage et la saisie « Activité et particularités » lors de la
sélection ; adresse, popins et faits déjà enregistrés sont conservés.

La recette `leo-assistant.mjs` compare les positions et dimensions de la
navigation et du pied de page avant/après le choix de Chasse puis à l’étape
suivante, à 390/1280 px. Elle échouait avant le correctif et passe après.
`generation-preparation.mjs` passe 38 contrôles incluant l’absence du champ et
de textarea à la sélection, la génération et la révision. Les recettes
Passeport et lots/Tombola, les types, le lint et le build isolé vérifient les
parcours voisins. Captures mobile/bureau inspectées. API simulées, sans preuve
de déploiement. Impacts limités à Animation et documentation ; contrats,
permissions, migrations et générateur sans modification car seuls la
présentation et le champ de saisie local changent.

## État des lots

| Lot | État | Résultat et reste à faire |
| --- | --- | --- |
| T1 — Socle et contrats | Livré et vérifié localement | Registre des trois moteurs, modèles fermés et exports consommés, coordination SQL, exécutions, transaction commune des commandes historiques. Détails ci-dessous. |
| T2 — Générer et préparer | Livré et vérifié localement | Brouillon et quota atomiques, workflow manuel et worker, import complet/médias, ERP et préparation guidée. |
| T3 — Confirmer les missions | Livré et vérifié localement | Accords par mission, préparation vérifiée, QR, compilation et publication atomique ; interfaces Animation, Commerçant et ERP. |
| T4 — Jouer et reprendre | Livré et vérifié localement | Définition publiée, inscription adulte, projections filtrées, commandes/reçus, trois rendus Live, cinq activités et attestations commerçantes. |
| T5 — Exploiter et clôturer | Livré et vérifié localement | Retrait avec aperçu, continuité, correction des preuves, qualification effective, gel et indicateurs ; interfaces Animation, Live et ERP. |
| T6 — Conserver et ouvrir | Code livré et vérifié localement ; ouverture à effectuer | Conversion, conservation, paramètres publiés, recette transversale et procédure. Restent la conversion sur cible, le pilote humain et le déploiement. |

## T1 — Socle et contrats

### Réalisé

- Registre métier explicite `(type, contractVersion)` pour Passeport, Tombola et Chasse ; aucune substitution pour une version inconnue. Le domaine reste indépendant des frameworks.
- Modèles Pydantic fermés pour brief, génération, préparation, définition, commandes/reçus et quatre audiences. Export hors bootstrap de 13 schémas et d’un manifeste SHA-256, consommés et contrôlés dans les trois frontends.
- Validation des cinq activités, normalisations, chaîne linéaire, rôles départ/finale, références et règles de qualification. Fixture Latresne portée vers des UUID de lieux déterministes avec refus des correspondances inconnues.
- Migration additive `v235` : coordinations rétroremplies, exécution par participation, métadonnées et références de configuration ; clés étrangères interdisant le croisement d’animations.
- Coordination partagée pour les actions individuelles, exclusive pour les changements globaux ; verrou participant et relecture après attente. Le batch de statuts conserve `SKIP LOCKED`. Capacité calculée sous verrou, reprise d’un inscrit existant préservée.
- Service de commandes idempotentes : reçu, effets, audit et outbox partagent la transaction. Les services historiques rejoignent explicitement l’UoW ; leurs commits internes sont différés. Dix entrées HTTP sont raccordées, y compris la clôture.
- Adaptateur des permissions moteur aux sessions Animation/ERP et au périmètre de commune. Les permissions de génération de base sont dérivées des droits de création/modification existants.
- Contrat OpenAPI réellement exporté pour l’application Commerçant (494 routes), dossier créé par son exporteur ; guides du consommateur corrigés.

### Vérifications

Les tests backend passent par `scripts/validation/test_isolated.py`, sans `.env` opérateur, bootstrap, scheduler ni sortie réseau. PostgreSQL 18 tourne dans un cluster jetable local, avec schémas propres aux tests ; aucune base d’exploitation n’est utilisée.

- Commandes idempotentes et habilitations : 12 tests réussis ; la régression étendue donne 373 réussites et un échec préexistant sur le libellé accentué « Passeport commerçant ».
- Contrats et domaine moteur : 58 tests réussis, dont fixture Latresne et export CLI hors bootstrap.
- Persistance et concurrence : 77 tests ciblés réussis, dont 13 nouveaux tests PostgreSQL, deux anciens tests PostgreSQL exécutés et huit tests du domaine. Migration exécutée avec le helper officiel dans un schéma jetable, rétroremplissage vérifié.
- Architecture et recensements : 365 réussites ; seuls les deux échecs de recensement préexistants subsistent, sans nouvelle classe manquante.
- PostgreSQL : dernière place d’inscription, actions concurrentes sur des participations distinctes, attente/relecture, barrière de clôture, batch non bloquant, refus d’upgrade, reçu/effets atomiques, rollback et réconciliation.
- Animation : 3 tests de registre/manifeste, typecheck et ESLint ciblé réussis.
- Commerçant : 103 tests réussis (11 fichiers), dont consommateur OpenAPI et registres.
- Marketplace : 3 tests de registre/manifeste réussis.
- Exporteur `--check` : 14 fichiers conformes dans chacun des trois consommateurs.

### Limites et suite

Ce socle n’active pas encore un parcours de chasse. Les registres frontend seront raccordés aux projections versionnées en T4 ; aucun fallback sur les anciens DTO n’a été ajouté. Le décodage des WebP, le contrôle du document complet et le stockage privé appartiennent à T2 ; les engagements et le compilateur de publication à T3 ; les projections filtrées et la persistance du jeu à T4.

Les deux contrôles de recensement de tests ont une [dette identifiée avant cette évolution](../../architecture/transverse/controle-architecture.md#validation-du-18-septembre-2026). Aucune exclusion ni assertion affaiblie n’est ajoutée. La génération historique de flyer pendant la publication sera sortie de la transaction dans le raccordement T3 ; T1 assure son verrouillage et son reçu, pas encore cette séparation.

## T2 — Générer et préparer

### Réalisé

- Création atomique du brouillon et réservation du quota mensuel partenaire ; rejouer la demande retrouve le même brouillon. Dépôt, acceptation, révision, reprise, affectation et annulation disposent de versions et de reçus.
- Workflow manuel persistant, worker PostgreSQL avec claim/bail/CAS et reprises techniques ; les attentes humaines ne consomment ni tentative ni bail. Batch supervisé et planifié, deux tâches au maximum par processus.
- Prompt court, déterministe et exportable avec schéma contextualisé ; aucune invocation automatique d’un fournisseur IA en V1.
- Import JSON fidèle et borné, contrôle des cinq défis, décodage réel WebP, dimensions/poids/empreintes/références contrôlés. Brut et médias privés, base64 absent des JSONB ; export autonome réassemblé pour relecture.
- Bibliothèque POI avec éditions immuables ; snapshots autorisés, contexte périmé détecté. Templates acceptés privés, réutilisables dans la même commune sans quota, avec provenance et références protégées.
- Édition de préparation conservant les identités de missions/exigences, minimum de commerçants obligatoire pour Chasse et recontrôle des contenus/médias.
- Interface Animation guidée : brief, lieux, quota, opérations, édition des cinq activités, réconciliation, bibliothèque. ERP : file paginée, filtres, export/dépôt, relecture explicite, rapports, reprise, affectation et quota administrateur.
- Catalogue Chasse explicite, invitations implicites désactivées ; publication bloquée jusqu’aux contrôles et à la compilation T3. Migrations additives v236, v237 et v238.
- 39 fichiers de contrats générés, identiques dans les trois consommateurs ; OpenAPI réel de 546 routes, contrats documentaires EPIC 41/42 actualisés.

### Vérifications

- Contenus/catalogue et régressions associées : **118 tests réussis**.
- Workflow/persistance : **15 tests domaine et 22 tests PostgreSQL réussis** ; groupe élargi antérieur de **427 tests réussis**, incluant architecture et concurrence T1/T2.
- Raccordements root : **45 tests réussis** (API, POI, idempotence, ordonnanceur, budgets SQL et migrations v237/v238). Migration v236 exécutée par le helper officiel dans le groupe persistance. Une diagnostic Windows WMI a été émis durant une collecte, sans interruption de la suite ; le résultat pytest est 45 réussites, code 0.
- Revue indépendante API/ERP : **6 tests réussis** avec les services/projections réels, incluant UTC, export exact, scope et CSRF.
- Animation : **126 tests Node**, types, lint et build isolé réussis ; **20 contrôles navigateur** sur 1280/390 px. API simulée dans le navigateur, complétée par les tests de contrats HTTP réels. Le build conserve un avertissement de taille de chunk.
- ERP : parcours navigateur à 1280/390 px, relecture obligatoire, référence exacte de tentative, perte de réponse et reçu sans second POST ; absence de débordement et captures vérifiées. Harness `tests/browser/generation-erp.cjs` dans le backend, Playwright du workspace, API simulée.
- Marketplace : **3 tests** registre/manifeste réussis. Commerçant : **46 tests ciblés réussis** de contrats et registre après synchronisation.
- Recensements : **deux échecs préexistants**, huit anciennes classes et trois anciens use cases ; aucune nouvelle classe manquante. Aucun skip ni affaiblissement d’assertion ajouté. Le test d’ordonnanceur a été adapté explicitement au nouveau job couvert.

### Limites et suite

T3 complétera les accords, la checklist/les vérifications POI, le compilateur et la publication, ainsi que la modification de la configuration commune Chasse (nom/dates/coffrets/règlement) et l’ajout/suppression de positions dans l’éditeur. T2 permet la modification du contenu, des réponses et de l’ordre. Les images réelles de la fixture Latresne sont vérifiées ; aucun nouveau service IA distant n’est appelé.

Les écritures de stockage sont hors transaction SQL. Un échec ou rejeu peut laisser un objet privé non référencé ; la collecte de ces orphelins appartient à T6. Les objets attachés ont des parents et références explicites. Les vérifications locales ne constituent ni un déploiement ni le pilote humain.


## T3 — Confirmer les missions et publier

### Réalisé

- Missions alternatives privées par commerce, choix unique et confirmation exacte des exigences. Décisions, invitations, relances et annulations portent leurs versions et reçus ; une retouche propre à A conserve l’accord de B. Les listes ne contiennent aucun contenu de mission ni média.
- Relecture explicite de la préparation avant invitation, minimum choisi et échéance contrôlée. Aucun refus ne supprime automatiquement une position ; une demande envoyée encore en attente doit être traitée explicitement avant publication.
- Dossier organisateur versionné et audité : cinq rubriques de checklist, mise en place de chaque mission, vérification POI datée/responsable/emplacement/observations et photo privée facultative. Les contrôles périmés ne permettent pas la publication.
- QR préparés pour les commerces et POI, supports accessibles aux seuls organisateurs autorisés, token opaque signé et condensat persistant. Activation atomique avec la version publiée ; QR de lieu distinct du QR personnel et de l’attestation commerçante.
- Compilateur déterministe : une mission acceptée par commerce, identités stables, chaîne linéaire, cinq activités, présentation héritée, médias retenus et définition privée typée avec empreinte. L’édition POI est verrouillée pendant le figement ; provenance et liens conservés par FK.
- Publication avec recontrôle des accords, checklist, période, financement et abonnement sous coordination exclusive. Flyer rendu/stocké hors transaction, source comparée avant rattachement ; configuration, QR, reçu, quota, audit et notifications en base sont atomiques. Régénération de flyer avec version documentaire immuable.
- Migrations additives v239 (engagements) et v240 (dossier, vérifications et QR). Contrats fermés et projections séparées conservés.

### Vérifications

Les vérifications backend utilisent le runner isolé et PostgreSQL jetable. Aucun envoi réel ni déploiement n’est effectué. Les tests de navigateur utilisent une API simulée ; ils complètent les tests HTTP et SQL, sans se présenter comme une recette sur environnement déployé.

- Dossier, QR et bridge : 10 tests PostgreSQL réussis ; groupe dossier/API : 26 tests réussis. Complément domaine/bridge et édition T2 : 15 tests réussis. Ce dernier lancement a émis un diagnostic Windows WMI `0x8007000e` pendant la collecte, puis terminé avec code 0.
- Missions et frontières : 126 tests ciblés réussis, dont 14 PostgreSQL, 27 HTTP et deux preuves d’hydratation de médias après fermeture de la transaction.
- Régression backend élargie : 911 réussites au premier passage ; cinq fixtures/appels affectés par les nouveaux contrats ont été corrigés puis retestés. L’échec antérieur du titre « Passeport commerçant » accentué reste distingué.

Vérification finale ciblée : **151 tests backend réussis**, incluant domaine, contrats, API, migrations, dépôts PostgreSQL, missions, compilation, publication et flyer. Les groupes précédents se recoupent et ne s’additionnent pas.

- Architecture : **385 tests réussis**. Les recensements restent limités aux huit anciennes classes et trois anciens use cases documentés ; le nouveau port de préparation est couvert par des preuves SQL dédiées, sans exclusion.
- Animation : **132 tests Node réussis**, typecheck, lint et build isolé réussis ; **22 contrôles navigateur à 1280/390 px**, captures vérifiées. Sept contrôles de contrats et manifeste repassés après export. Avertissement de taille de chunk conservé.
- ERP : parcours ADMIN et lecture seule à 1280/390 px ; QR, mission, checklist, réponse perdue et réponse `202` réconciliés sans deuxième écriture. Captures vérifiées, aucun débordement ; harness `tests/browser/preparation-erp.cjs`.
- Commerçant : **54 tests ciblés réussis** après export ; parcours navigateur à 1280/390 px, choix de mission au clavier, confirmations et réponse perdue vérifiés pendant le lot.
- Marketplace : **3 tests** registre/manifeste réussis.
- **61 fichiers de contrats** identiques dans les trois consommateurs ; OpenAPI réel de **572 routes**, projections documentaires EPIC 41/42 synchronisées.

### Limites et suite

Le jeu, ses projections joueur et les trois rendus Live relèvent de T4 ; les retraits après publication passent par la neutralisation T5. L’ancien retrait Chasse est fermé jusqu’à ce raccordement. Les anciennes créations/régénérations internes de modèles historiques qui ne passent pas par la publication restent à aligner avant ouverture.

Les objets PDF/PNG préparés avant une transaction peuvent rester sans rattachement si celle-ci échoue. Leur collecte T6 doit vérifier l’absence de référence et attendre un âge minimal ; une réponse perdue ne justifie jamais une suppression immédiate. Les objets IA orphelins suivent la même obligation de réconciliation dans leur stockage propre.

Le contrôle automatique d’approbation a refusé l’octroi proposé du droit de publication d’événement aux comptes ERP ADMIN, faute d’autorisation explicitement établie. Aucun droit n’a été ajouté. La publication reste utilisable par le portail Animation avec sa permission existante ; l’ERP conserve préparation et publication du résultat IA selon ses droits actuels. Cette limite ne bloque pas le parcours de publication de l’événement.


## T4 — Jouer et reprendre

### Réalisé

- Publication des trois moteurs sur une définition figée ; accès, inscription et récupération utilisent sa configuration explicite. Déclaration adulte et version du règlement vérifiées pour Chasse, sans données enfant.
- Commandes joueur fermées, versions, clé stable, reçu et traces atomiques. Une mauvaise réponse valide compte comme tentative ; un payload invalide ne compte pas. Normalisation du mot/code et des associations pour l’empreinte, ordre conservé pour la remise en ordre.
- Migration v241 : état structuré des étapes, dates/ordres persistés, tentatives privées et effets uniques ; FK du reçu différée et contraintes de portée des preuves. Les GET n’initialisent aucun état en base.
- Projections par moteur construites avec des champs autorisés : contenu et image du défi après accès au lieu, résultats déjà ouverts uniquement, aucune solution ou destination future. Médias WebP hydratés hors transaction, budgets vérifiés avant publication et à la lecture.
- QR de lieu signé distinct de l’attestation personnelle ; rotation de signature contrôlée. Indice et aide après première erreur, sans preuve fictive. Une correction de preuve conserve les acquis ; sa régularisation reste explicite.
- Attestations commerçantes réautorisées et versionnées, limitées à leur étape actuelle ou passée à régulariser. Lecture de reçu, reprise explicite et résultat minimal ; mission/consigne du commerce issues de la définition publiée.
- Live : trois rendus, cinq activités au clavier, mobile et ordinateur, QR/caméra ou saisie, aides, progression et qualification distinctes. Les liens personnels par e-mail utilisent le même composant. Aucun calcul de réponse ou d’éligibilité dans le navigateur.
- Carnet IndexedDB limité aux accès/résumés autorisés ; nettoyage à la lecture et à l’import. Saisie temporaire de l’onglet sur 24 h, aucun envoi automatique ; QR de lieu seulement en mémoire. Images en BlobURL révoquées et service worker limité au shell.
- Reçus de préparation et génération T2/T3 décrits par des réponses typées dans OpenAPI, vérification des modèles à la réconciliation ; téléchargements privés décrits comme fichiers.

### Vérifications

Les scénarios SQL utilisent PostgreSQL jetable ; les navigateurs simulent les API. Les nombres des groupes se recoupent et ne s’additionnent pas.

- Runtime et frontières : **70 tests réussis**, dont PostgreSQL, deux appareils, même clé concurrente, rotation du QR/token, délai après verrou, rollback d’audit, perte de réponse, aide sans preuve et hydratation WebP hors transaction. Les cinq contrôles HTTP ont ensuite repassé après fermeture du DTO de réconciliation.
- Persistance : **13 tests PostgreSQL réussis**, migration v241, contraintes de portée, unicité des effets/tentatives et ordres/dates immuables.
- Attestations/publication classiques : groupes ciblés **38**, puis **17** réussites et un rejeu après correction/révocation vérifié. La suite élargie finale a réussi 120 tests et révélé quatre écarts, corrigés ensuite : fixture de récupération, identifiant d’étape et réponses OpenAPI non typées.
- Commerçant : **24 tests Vitest** et **7 tests Chromium** réussis, sortie 0 ; mobile 390 px et bureau 1280 px, réponse perdue, 202/404, reprise, conflit et anomalie. Capture mobile inspectée.
- Animation : **7 tests** registre/manifeste et contrats HTTP réussis après export.

- Couverture publique : **27 tests réussis**, dont WebP réel lu/décodé hors SQL, refus des références absentes et configuration publiée conservée malgré un brouillon plus récent. Le catalogue ne révèle aucun commerce futur et n’utilise que la couverture déclarée.
- Vérification finale contrats/ERP/architecture : **446 réussites**, les deux seuls échecs restant les recensements des huit classes et trois use cases préexistants. Les régressions de récupération, d’identifiant et d’OpenAPI ont été corrigées et revérifiées. Aucun skip ajouté.
- Live : **24 tests Node réussis** (dont vraie IndexedDB), lint et build isolé réussis. Navigateur : **14/14**, puis **8/8** après correction de l’enregistrement du contact, soit **19 scénarios distincts**, sorties 0 ; captures 390/1280 inspectées. La configuration alternative documentée sépare le serveur du runner pour éviter le blocage de fermeture Playwright Windows observé auparavant.
- **70 fichiers de contrats** identiques dans les trois consommateurs ; OpenAPI réel et projections documentaires EPIC 41/42 synchronisés. Les consoles ERP à périmètre sont disponibles sous `/internal/erp/animations/generations` et `/internal/erp/animations/preparation` ; les alias SQLAdmin restent ADMIN.
- Des démarrages Python ont émis le diagnostic WMI Windows `0x8007000e` puis poursuivi. Les résultats de sortie des groupes concernés sont indiqués séparément de ce diagnostic.


### Limites et suite

T5 complète le retrait global, les corrections après gel, les indicateurs et la clôture depuis les faits du moteur. T6 couvre la conservation et la conversion avant ouverture. La caméra réelle sur appareils et le pilote humain ne sont pas revendiqués par les simulations navigateur. Aucun envoi réel, déploiement ou ouverture publique n’est effectué.

## T5 — Exploiter et clôturer

### Réalisé

- Neutralisation globale d'une étape physique, avec aperçu calculé depuis les faits, empreinte, versions, motif et confirmation. Recontrôle sous barrière exclusive ; décision, révision, audit, notifications génériques Live et reçu atomiques. La dernière étape requise reste protégée.
- Dépendances de continuité préparées et compilées : objets et informations liés aux UUID stables des positions, consommateurs ultérieurs, contrôle des références. L'éditeur réutilise les seuls médias contrôlés. L'exécution fournit les éléments acquis/dispensés avec provenance sans divulguer le futur ; Live affiche le parcours adapté.
- Correction des preuves sous permission explicite, aperçu et verrou de participation. Annulation avant gel avec narration/objets conservés ; nouvelle attestation reliée à la preuve annulée. Après gel, anomalie séparée sans modification de la preuve, de la population ni du gain.
- Acceptation d'un retrait commerçant publiée dans la même transaction que la neutralisation. Aperçu lié à la demande, permissions cumulatives, reçu consultable. Le refus possède également un reçu consultable sans nouveau POST.
- Clôture commune versionnée, y compris l'ancien endpoint. Recalcul depuis définition publiée, résolution, preuves et dispenses ; matérialisation des parcours réellement changés ; population de tirage existante figée avec provenance et FK de protection. Exclusion des participants anonymisés conforme aux invariants existants.
- Liste organisateur recalculée avant filtre/pagination, sans écriture lors d'un GET ; après gel, lecture de la provenance figée. Faits groupés par animation, sans réponses privées. Métriques calculées depuis les traces structurées, y compris après purge future des essais détaillés.
- Interfaces Animation pour exploitation, correction, retrait et continuité ; console ERP `/internal/erp/animations/exploitation`. Actions conditionnées aux droits serveur, aucune extension des droits de clôture ERP. Réconciliation 200/202/404, renvoi explicite identique et nouvel aperçu après conflit.
- Migration additive `v242`, sans modification des historiques SQL. **82 fichiers de contrats** générés et identiques dans les trois consommateurs ; OpenAPI backend **597 chemins**, projection documentaire Live **45 chemins**.

### Vérifications

- Exploitation/continuité : **30 tests réussis** dans la suite finale (domaine/DTO, PostgreSQL et port), plus le scénario PostgreSQL d'édition de préparation. Qualification anonyme, filtres avant pagination, provenance du gel et rollback vérifiés. Les faits de **101 participants** sont chargés en trois requêtes sans lire les tentatives privées.
- Correction/retrait : **30 tests distincts réussis**, dont courses, replay, rollback, droits, empreintes, FK de régularisation, refus réconcilié et conservation du gel. Le correctif de l'aperçu anonymisé est couvert par la dernière exécution ciblée.
- HTTP et console ERP : **20 tests distincts réussis**, session/CSRF, commune, contrats fermés, confirmation booléenne exacte, corps borné, réconciliation et clôture historique raccordée.
- Contrats, réponses OpenAPI et architecture : **432 tests réussis**. Les diagnostics Windows WMI `0x8007000e` observés pendant certains imports n'ont pas empêché les suites correspondantes d'atteindre un résultat pytest vert, code 0.
- Console ERP : **6 scénarios Chromium** à 390/1280 px, avec API simulée, aperçu, permissions, correction après gel, réponse perdue, 404 puis renvoi identique et conflit d'aperçu. Captures mobile et ordinateur inspectées, aucun débordement horizontal.
- Retrait Animation : **8 scénarios Chromium** à 390/1280 px, navigation clavier, perte avant/après commit simulé, aperçu périmé et refus selon permissions ; types, lint et build isolé réussis.

- Animation : **137 tests Node réussis**, TypeScript, ESLint et build isolé réussis. Deux parcours navigateur complets à 390/1280 px couvrent exploitation, droits, correction, gel, trois moteurs et édition de la continuité ; captures inspectées.
- Marketplace Live : **8 tests Node** (jeu, carnet et contrats) et **9 scénarios Chromium** réussis, incluant les deux nouveaux scénarios de continuité et la régression des cinq activités ; ESLint réussi, captures inspectées. Les serveurs de recette ont été arrêtés après les contrôles.
- Commerçant : **44 tests de contrats réussis**. Une ancienne fixture d'attestation a été complétée avec les versions déjà transmises par les deux écrans réels ; aucune assertion n'a été supprimée.
- Documentation : **76 guides, 747 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées**.

### Limites et suite

Les tests de navigateur emploient une API simulée, complétée par les tests HTTP et PostgreSQL réels isolés. La charge vérifiée localement ne vaut pas mesure de production. Les corrections ne constituent jamais une dispense individuelle ; les résultats du tirage et les gains ne sont pas recalculés après gel. Le lot T6 reste consacré à la conservation, à la conversion et aux contrôles d'ouverture ; aucun environnement réel n'a été déployé ni purgé.

## T6 — Conservation, conversion et recette transversale

### Réalisé

- Conversion avant ouverture par CLI à cible explicite : simulation paginée de 50, manifeste fermé avec empreintes, une transaction par animation, application/rejeu contrôlés, journal et contrôle global de disponibilité. Les brouillons incomplets restent éditables ; une correction exige une nouvelle simulation. Toute publication détectée bloque la conversion. Aucun quota, génération, publication ou envoi n’est déclenché.
- Conservation quotidienne par catégories, simulations requises avant exécution, lots reprenables, curseurs, baux et exclusion des références utiles/gels. Les fichiers sont marqués avant suppression hors transaction ; une erreur laisse une reprise durable. Le registre des fichiers préparés couvre aussi un crash avant rattachement. Aucun inventaire global du stockage ni suppression de fichier inconnu.
- Échéances des contenus inutilisés, essais, accès et identités ; mois calendaires calculés en UTC. Archives nominatives réservées aux besoins encore actifs, tirages/substitutions tardifs depuis les preuves conservées, sans recréer de qualification ni envoyer au pseudonyme. Le besoin est réévalué jusqu’à suppression de l’archive ; la durée des preuves ne prolonge pas automatiquement les coordonnées.
- Batch `animations.conserver` à 03:30 UTC, simulation par défaut, supervision commune et signalement des erreurs/retards. Console ERP ADMIN de rapports et gels avec motifs, confirmation de levée et réconciliation. Le menu, les API bornées, le CSRF et les reçus sont raccordés ; aucun bouton de purge réelle.
- [Complément technique du registre interne](../../juridique/interne/registre-interne-moteur-animation-2026-09-19.md) : catégories, échéances, références utiles, archives, gels, reprises et sauvegardes. Les PDF juridiques restent les références documentaires existantes ; le complément décrit le code local vérifié et les contrôles avant activation.
- Paramètres opérationnels après publication : début/fin/fermeture/capacité séparés du DSL, historique append-only, CAS sur animation/définition/exploitation et audit des anciennes/nouvelles valeurs. Un résolveur commun alimente jeu, scan, inscription/reprise, catalogues/listes, calendrier, clôture, flyers et conservation. La prolongation réaligne les accès et reçus utiles sans réactiver les accès révoqués.
- Interfaces des paramètres dans Animation et ERP : horaires Europe/Paris, contrôles affectés, champs omis/null, motif, réouverture explicite et annonce des supports à rééditer. Les sessions ERP actuelles restent en lecture seule pour ces paramètres, car aucun droit `animation:modifier` n’a été ajouté.
- Recette PostgreSQL des services réels : préparation → accords → publication et QR → inscription → jeu et attestation → retrait/continuité → correction/régularisation → prolongation → clôture/gel → tirage → anomalie après gel → purge. Les preuves, acquis, compteurs, reçus utiles, population et gains restent inchangés par la purge.
- Correction des écarts révélés par cette recette : publication fondée sur les missions structurées choisies, application de la fin effective, échéances UTC, fichiers préparés avant transactions finales, lectures de contenus purgés et enveloppes d’erreurs conformes à l’OpenAPI. L’ancienne configuration publiée mène désormais aux paramètres du Live. Le retrait classique est pris en compte par les commerces autorisés effectifs, sans modification de la définition publiée ni suppression des preuves historiques.
- Migrations additives `v243`, `v244`, `v245`. **97 fichiers JSON** (96 schémas et manifeste) générés et identiques dans les trois consommateurs ; **608 chemins OpenAPI**, dont **45** dans la projection documentaire Live.

### Vérifications

Les commandes utilisent le lanceur backend isolé et PostgreSQL jetable local. Les recettes navigateur bloquent les accès externes et simulent les API ; elles complètent la recette transactionnelle, sans la remplacer.

Les groupes ci-dessous se recouvrent parfois ; leurs nombres ne constituent pas un total de tests distincts de l’EPIC.

- Conversion : **23 contrôles réussis**, domaine/CLI/PostgreSQL, manifeste, correction puis nouvelle simulation, concurrence et absence d’effets externes.
- Conservation : **54 contrôles distincts réussis** sur ce périmètre, dont migration réelle, pagination, gels, courses, incident SQL, suppression reprise après panne, écriture tardive, réimport et archives nécessaires aux gains.
- Paramètres et lecteurs : groupe final **22/22 réussi**, incluant filtre de dates sur la configuration publiée, support régénéré et retrait effectif dans les projections SQL ; **42/42 régressions des lecteurs réussies**. Expiration après prolongation, UTC, capacité, CAS, rollback et contrôles métier vérifiés.
- Recette transversale et publication : **68 cas backend distincts vérifiés** dans ce périmètre ; dernier groupe **11/11 réussi**, dont prolongation avec purge à la nouvelle fin +90 jours et conservation des preuves, de la population et des gains.
- Retrait classique : **6/6 nouveaux cas PostgreSQL**, puis **10/10 régressions après injection de l’adaptateur de flyer**. Seuil/minimum, population gelée, concurrence scan/retrait, preuves historiques, reçus réautorisés et qualification contrôlés. **33/33 contrôles existants** supplémentaires réussis sur API retrait, compilation/publication classiques et attestations T4.
- HTTP, erreurs et ordonnanceur : groupe **59/59 réussi** ; vérification complémentaire contrats/projections/OpenAPI/sécurité **79/79 réussie**, incluant refus CSRF sur l’ancienne purge et erreurs sans contenu privé.
- Architecture et recensements : exécution finale **414 réussites, 2 échecs préexistants**. Les huit anciennes classes et trois anciens use cases manquants sont inchangés ; aucune classe nouvelle non couverte. Un premier lancement a rencontré un refus d’accès au répertoire temporaire Windows ; relancé avec un répertoire temporaire propre du workspace, il ne conserve que cette dette antérieure. Aucun skip ni assertion affaiblie.
- Animation : **22 tests Node ciblés réussis**, TypeScript, ESLint et build isolé réussis. Recette navigateur à **390 et 1280 px** : entrée depuis la configuration publiée, capacité, CSRF, réponse perdue, réconciliation 202/404, renvoi identique, conflit, prolongation, réouverture et lecture seule. Captures inspectées, aucun débordement. Avertissement de taille du bundle conservé.
- ERP : **6 scénarios conservation, 6 paramètres et 6 régressions exploitation** réussis ; parcours génération à **390/1280 px** incluant le brut purgé. Les paramètres sont aussi testés avec fuseau navigateur Montréal. Captures inspectées ; permissions simulées distinguées des droits ERP réels.
- Commerçant : **47 tests de contrats réussis** et build isolé réussi. Marketplace/Live : **13 tests ciblés réussis**, ESLint et build isolé réussis ; fichiers publics de configuration inchangés.
- Contrats : régénération de référence hors bootstrap comparée en lecture seule, **97 fichiers conformes dans chaque consommateur**, OpenAPI **608/608/608/45 chemins** concordants pour Animation, Commerçant et les deux projections documentaires.
- Documentation : contrôles du projet central `check_guidance.py` et `sync_documentation.py --check-sources` ; les liens du complément de registre ont également été contrôlés avec l’index juridique et la procédure d’exploitation (38 liens locaux).

Certains imports Python ont émis le diagnostic WMI Windows `0x8007000e` puis poursuivi. Les résultats ci-dessus proviennent des sorties finales des lanceurs, et non des seules traces de démarrage.

### Décisions tracées

La [conception](conception-technique.md) porte les précisions CV01–CV06 (conversion), R01–R11 (conservation et documents), E01–E08 (exposition, planification et présentation) et QA01–QA03 (écarts de recette). Les contrôles opérationnels restent hors du prompt IA. Aucune évolution de droit ERP n’est implicite.

### Non exécuté ou non livré dans ce périmètre

- Déploiement, migrations/conversion sur une cible d’exploitation, activation d’une purge réelle et ouverture publique : procédures documentées, aucune exécution sur un environnement réel.
- Pilote humain, scans caméra sur appareils réels, validation du trajet et essai avec des familles : [fiche de recette préparée](recette-pilote.md), à exécuter sur la commune et la période retenues.
- Appel automatisé à un fournisseur IA : laissé au traitement manuel comme prévu pour la V1. Comparaison opérationnelle des fournisseurs non réalisée ici ; intégration après pilote, rallye à ordre libre et adaptation intercommunes restent les évolutions prévues.
- Élargissement du droit de publication ERP : non appliqué. La revue automatique d’approbation a refusé cet élargissement pendant T3, faute d’autorisation suffisamment explicite ; la publication reste accessible au rôle Animation qui possède déjà ce droit. Les droits de modification et de clôture ERP restent également inchangés.
- Dette de tests préexistante : deux contrôles de recensement restent en échec ; ils sont distingués des tests fonctionnels du moteur et des nouvelles classes couvertes.

La [procédure d’exploitation](exploitation-moteur.md) décrit les contrôles à réaliser avant ouverture. Les commits locaux ne constituent ni un push ni un déploiement.

## Correctif après T6 — Navigation ERP (19 septembre 2026)

- **Constat sur `cd4bb07` :** l’entrée des demandes de création n’était exposée que dans SQLAdmin, pas dans le workspace ERP principal. De plus, la route générique `/internal/erp/{page}/{identifiant}` interceptait les quatre consoles du moteur et renvoyait 404. Le nouveau test reproduisait neuf échecs sur dix avant correction.
- **Correction backend `09d1c11` :** lien **Animation → Demandes de création** dans le menu principal et sur la page Animation ; composition des routes précises des consoles avant les routes génériques du workspace. Décision tracée en **T6-QA04** dans la [conception](conception-technique.md). Les sessions, rôles et périmètres restent inchangés, avec conservation réservée à ADMIN. Aucun contrat métier ni migration supplémentaire.
- **Vérifications :** 35 tests HTTP ciblés réussis, dont les dix nouveaux cas de navigation, priorité des quatre consoles et refus d’accès. Recette Chromium `tests/browser/generation-erp.cjs` réussie à 390 et 1280 px depuis le menu principal, avec assets réels et API simulée ; lien de la page Animation, relecture, réponse perdue et réconciliation également vérifiés. Captures inspectées, aucun débordement horizontal.
- **Architecture :** 414 réussites et les deux échecs de recensement préexistants, concernant les mêmes huit anciennes classes et trois anciens use cases. Aucune assertion affaiblie ni exclusion ajoutée.
- **Contrats :** comparaison hors bootstrap des 97 fichiers embarqués dans chacun des trois consommateurs et des projections OpenAPI (608/608/608/45 chemins) ; contrats inchangés, hors métadonnée de version contenant le SHA du build.
- **Livraison :** commit local sur `feat-moteur-animation`, à pousser et déployer sur le backend. Cette correction ne réalise aucun déploiement ni opération sur une base. L’accès ADMIN historique `/admin/animations-generations` reste disponible dans le code antérieur.

## Correctif après T6 — Catalogue des trois types V1 (19 septembre 2026)

- **Constat vérifié sur la base de test :** le catalogue persistant ne contenait que `CHASSE_TRESOR_COMMERCANTE`. Passeport et Tombola étaient absents, sans suppression de leurs parcours dans Localeo Animation. La cause historique de l’absence de ces références n’est pas déterminée ; v238 ajoute seulement la Chasse et ne supprime aucun modèle.
- **Correction backend `2bb92b1` :** migration additive `v246_retablir_catalogue_animation.sql`, conforme à **T6-QA05** dans la [conception](conception-technique.md). Elle insère uniquement les deux fiches manquantes, avec les valeurs v187 et les corrections exactes v230. Les fiches existantes, y compris personnalisées ou désactivées, restent intactes. Aucun changement de règle, d’habilitation, de contrat API ou de code frontend.
- **Tests :** huit tests backend réussis via le lanceur isolé, dont trois scénarios PostgreSQL jetables : catalogue réduit à la Chasse, rejeu sans modification, conservation d’une fiche personnalisée désactivée. Six parcours de sélection vérifiés en Chromium à 390/1280 px dans le bundle local Animation, avec les références restaurées et une API simulée : Passeport/Tombola ouvrent le parcours manuel, Chasse ouvre la préparation guidée, l’option IA reste proposée pour Passeport. Captures inspectées ; aucune création réelle effectuée par cette recette.
- **Exécution sur test :** v246 appliquée par le lanceur officiel après sauvegarde locale des seules fiches du catalogue. Contrôle après application : les trois modèles sont actifs, la fiche Chasse est inchangée et aucune migration ne reste en attente. Compte rendu privé `v246-catalogue.json` dans le dossier de sauvegarde local de l’opérateur. Aucune animation, invitation, participation ou donnée personnelle modifiée.
- **Disponibilité :** recharger **Modèles** ou **Nouvelle animation** suffit sur l’environnement de test ; aucun redéploiement frontend nécessaire. Le commit local doit être poussé pour conserver le correctif dans l’historique distant et le diffuser aux autres environnements selon leur procédure. Aucun déploiement ni changement de production réalisé.

## Correctif après T6 — Retrait des cartes « Prochainement » (19 septembre 2026)

- À la demande utilisateur, suppression des deux cartes statiques « Chasse au trésor » et « Défi commerçants » sur **Modèles** et **Nouvelle animation**. Les trois modèles du catalogue backend restent proposés selon leur disponibilité. Décision **T6-QA06** ; commit Animation `07cd846`.
- TypeScript et ESLint réussis ; build isolé sans configuration opérateur réussi, avec l’avertissement préexistant de taille du bundle. Vérification Chromium des deux écrans à 390/1280 px : aucune carte « Prochainement », trois types disponibles, six parcours de sélection réussis avec API simulée. Captures relues. Aucun changement de contrat ou de base.
- Commit local sur `feat-moteur-animation`, à pousser puis déployer sur le frontend Animation. Aucun déploiement effectué. L’utilisateur confirme séparément que l’erreur « Modèle d’animation introuvable » ne se reproduit plus.

## Évolution après T6 — Léo, assistant de préparation (19 septembre 2026)

- **Animation `ed290d5` :** suppression du bouton « Préparer avec l’IA », badge « Assisté par Léo » sur la carte Chasse dans Modèles et Nouvelle animation, entrée dans le brief par Continuer. Icône SVG réutilisable : bulle souriante bleue et étincelle orange ; présentation explicite « Léo, votre assistant IA » au début du brief. Persona et portée tracés en **T6-UX01** dans la [conception](conception-technique.md).
- **Parcours conservés :** Passeport manuel par défaut, avec choix « Avec Léo, assistant IA » puis Continuer ; Tombola manuelle ; Chasse guidée. La sélection des modèles utilise des radios accessibles au clavier avec focus visible. Le badge ne déclenche aucune commande et les disponibilités viennent toujours du serveur. Les formulaires et traitements existants portent l’assistance ; aucune conversation ni intégration fournisseur supplémentaire.
- **Validation :** TypeScript, ESLint et build isolé réussis (avertissement de taille du bundle existant). Dix tests Node préparation/contrats réussis ; vingt contrôles de la recette génération réussis après adaptation de son entrée. Nouvelle recette `tests/browser/leo-assistant.mjs` réussie à 390/1280 px : badge, absence de l’ancien bouton, clavier, brief, Passeport manuel/assisté, Tombola et indisponibilité serveur. API simulées, captures inspectées, aucune création réelle.
- **Livraison :** README avec composants et commande de recette ; commit local sur `feat-moteur-animation`, à pousser et déployer sur Animation. Aucun changement backend, contrat, migration ou déploiement effectué.

## Décisions d’implémentation

Les précisions T1-D01 à T1-D04 sont inscrites dans la [conception technique, section 9.3](conception-technique.md#93-précisions-dimplémentation-t1--19-septembre-2026) : clés JSON, composition explicite des transactions, commits par dépôt concerné et noms du DSL. Les précisions T2-D01 à T2-D14 sont inscrites en section 9.4 de la conception : routes/reçus, interface, stockage privé/provenance, faits de lieux, import fidèle, images, templates, conservation, catalogue, ordonnanceur, identités et dépendances. Les précisions T3-D01 à T3-D10 sont inscrites en section 9.5 : engagements, compilation, dossier/QR, contrôles, publication et limites ERP. Les précisions T4-D01 à T4-D10 sont inscrites en section 9.6 : projections, traces, présentation, reçus, consentement et frontières de données. Aucun arbitrage fonctionnel n’est remplacé par ce compte rendu.

## Commits

Aucun push ni déploiement n’est inclus. Le commit documentaire central de chaque lot est identifiable par son message dans son historique ; il ne peut contenir sa propre empreinte.

| Lot | Backend | Animation | Commerçant | Marketplace/Live | Documentation centrale |
| --- | --- | --- | --- | --- | --- |
| T1 | `96bb488` | `d813be8` | `e57cbcd` | `5190106` | `docs(animation): documenter la livraison du socle T1` |

| T2 | `43f7495` | `58a34d2` | `cd2277d` | `6d05e35` | `docs(animation): documenter la livraison du lot T2` |

| T3 | `0655811` | `90ddcb9` | `baffe0e` | `9c3e568` | `docs(animation): documenter la livraison du lot T3` |

| T4 | `acee4dd` | `6792e26` | `d274260` | `16e4653` | `docs(animation): documenter la livraison du lot T4` |
| T5 | `4e7b1fc` | `81acd10` | `ea710ce` | `f92780c` | `docs(animation): documenter la livraison du lot T5` |
| T6 | `cd4bb07` | `cd03903` | `166a5f4` | `9f28154` | `docs(animation): documenter la livraison du lot T6` |

Contrôles documentaires T4 : 76 guides, 740 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

Contrôles documentaires T3 : 79 guides, 751 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

Contrôles documentaires T2 : 76 guides, 734 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

[Retour au dossier moteur](README.md).


## Correctif après T6 — Préparation du prompt bloquée dans l’ERP (19 septembre 2026)

- **Cause vérifiée :** demande de test en `PREPARATION_PROMPT`, aucun prompt et aucun claim ; ordonnanceur actif avec cron chaque minute, mais aucune exécution `animations.generer`. La pile HTTP réelle reproduit un `401 Admin session required` même avec une clé batch valide : le middleware de session interceptait les batchs moteur avant leur authentification par clé.
- **Correction T6-QA07, backend `3b893d4` :** exception limitée aux deux couples POST/chemin des batchs génération et conservation, avec contrôle existant de clé active `internal:batch`. Aucune extension des droits ERP. OpenAPI et ses quatre exports sont synchronisés ; pas de changement de DTO ou de migration. L’ERP explique l’attente technique et l’actualisation ; les actions restent fournies par le backend.
- **Preuves :** nouveau test HTTP passant par l’application complète, contrôle réel des clés sur SQLite isolée et doubles des traitements : 10 échecs reproduits avant correction, puis 17 cas réussis. Ensemble ciblé authentification/CSRF/session : **73 réussis**. Recette Chromium 390/1280 px : attente sans export/dépôt, actualisation vers les deux exports et le dépôt, relecture, reçu après réponse perdue et purge réussis. Contrôles architecture : **414 réussis, 2 échecs de recensement préexistants**, mêmes huit classes et trois use cases que le bilan précédent ; aucun affaiblissement.
- **Intervention test :** reprise ponctuelle du seul prompt en attente via `BatchRunner` et `WorkerGenerationAnimation` (`limit=1`), sans appel IA, dépôt, invitation ni publication. Le moteur a détecté un brouillon passé de version 1 à 2 après la demande et l’a placée en `OBSOLETE` (« Contexte à actualiser »), sans enregistrer de prompt. La demande reste à réviser dans l’ERP avec le brief relu ; cette intervention ne constitue pas une génération réussie.
- **Mise en service :** correctif local à pousser et déployer sur le backend. Après déploiement, créer la révision dans le détail de la demande puis actualiser après le passage du batch. Aucun déploiement réalisé et aucun résultat IA déposé pendant l’intervention. Les exports Animation/Commerçant reflètent seulement le contrat d’authentification ; leurs interfaces applicatives ne changent pas.

Contrats vérifiés : 97 DTO identiques dans chacun des trois consommateurs ; exports OpenAPI conformes (608 chemins Backend/Animation/Commerçant, 45 Live). Documentation : 76 guides et 755 liens contrôlés sans erreur, 117 sources exportables vérifiées.


## Évolution après T6 — Parcours ERP copier, vérifier, traiter (20 septembre 2026)

- **Backend `d1c3744` :** console réorganisée en liste de demandes nommées et détail en trois étapes. Prompt complet affiché et copiable avec son schéma ; contexte du gestionnaire lisible ; collage JSON ou import fichier ; rapport de conformité et aperçu des textes, missions commerçantes, consignes, défis, réponses attendues et médias. Enregistrement distinct puis relecture de la tentative serveur et bouton **Traiter la demande**. Les actions secondaires restent repliées. Décision utilisateur et portée tracées en **T6-UX02**, également intégrée à la section 8.7 de la spécification fonctionnelle et au guide d'exploitation.
- **Pré-vérification sans effet métier :** nouvel endpoint ERP `POST /operations/{id}/reponses/verifier`, avec les mêmes droits de dépôt, session/CSRF, périmètres, versions, prompt courant, purge et dépendances. Validateur réel hors transaction ; contexte relu après validation. Aucun fichier, tentative, consommation de quota, reçu ou transition. Messages de schéma fixes et explicites sans recopier de valeur saisie. Le dépôt et l'acceptation conservent leurs contrôles, reçus et commandes séparées.
- **Saisie et concurrence :** JSON original transmis sans effacer les clés dupliquées ; invalidation du rapport après changement de texte, version ou sélection. Saisie conservée lors de l'actualisation de la même demande, avertissement avant abandon au changement de demande, contenu uniquement en mémoire. Réponses tardives ignorées ; commandes incertaines réconciliées sans rejeu automatique. Actualisation des phases techniques bornée à deux minutes, suspendue dans un onglet masqué. Téléchargements, affectation, révision, annulation, historique et plafond conservés.
- **Contrats :** `animationName` ajouté aux projections courantes ; nullable par défaut pour relire les anciens reçus sans réécriture. 97 DTO conformes dans chacun des trois consommateurs ; OpenAPI 609 chemins complets et 45 chemins Live conformes. Commits de synchronisation : Animation `25ba394`, Commerçant `af55f9b`, Marketplace `1f0000c` ; aucune interface de ces applications n'a changé.
- **Tests backend :** **90 réussis** avec `scripts/validation/test_isolated.py` sur `tests/application/services/test_contenu_generation_t2.py`, `tests/application/services/test_verification_reponse_generation.py`, `tests/api/test_generation_animation_api_t2.py`, `tests/api/test_generation_animation_integration_review_t2.py`, `tests/api/test_verification_reponse_generation_api.py`. Cas réels de schéma/médias, absence d'écriture, versions/prompt révisés, droits/tenant, CSRF, doublons, nombres non finis, profondeur, compression, taille et anciens reçus. Contrôles d'architecture : **414 réussis, 2 échecs de recensement préexistants**, inchangés.
- **Recette UI :** `node tests/browser/generation-erp.cjs` réussi en Chromium 1280/390 px avec API simulée. Navigation depuis ERP, prompt en attente puis copie intégrale, contexte, collage/fichier, erreurs, aperçu des missions et réponses, rapport sans écriture, invalidation texte/version/sélection, réponses tardives, dépôt et reçu après réponse perdue, confirmation de relecture, traitement et purge. Captures relues, aucun débordement ni erreur JavaScript. Tests de contrats consommateurs : 10 Animation, 26 Commerçant et 3 Marketplace réussis. Guides/sources vérifiés ; aucune recette sur base d'exploitation ni opération sur la demande de test pendant cette évolution.
- **Livraison :** commits locaux sur `feat-moteur-animation`, à pousser. Déployer le backend `d1c3744` pour l'écran ERP et son endpoint ; aucune migration nécessaire. Pas de déploiement ni publication réalisés. Les anciennes demandes continuent d'utiliser leurs versions et phases existantes ; un contexte obsolète doit toujours être révisé par l'opérateur.


## Correction après T6 — Passeport manuel dans Localeo Animation (20 septembre 2026)

- **Animation `8d9436f` :** suppression du choix « Je prépare moi-même / Avec Léo, assistant IA » pour Passeport. Continuer ouvre directement sa création manuelle. Retrait du panneau de génération dans son onglet Configuration ; les formulaires métier existants restent disponibles. Léo conserve son badge et son parcours sur la Chasse. Décision utilisateur tracée en **T6-UX03**, qui remplace la présentation Passeport initiale de T6-UX01/T2-D02 dans Localeo Animation.
- **Portée :** interface Animation, README exécutable et documentation centrale. Aucun contrat, migration, historique de génération ni donnée de demande modifié. Les capacités backend historiques ne sont pas supprimées par cette correction d'interface.
- **Validation :** TypeScript (`tsc --noEmit`) et ESLint (`eslint src vite.config.ts`) réussis ; build isolé sans environnement opérateur via `node scripts/build-generation-tests.mjs` réussi, avertissement de bundle >500 Ko préexistant. Recette `node tests/browser/leo-assistant.mjs` réussie à 390/1280 px : absence des deux choix Passeport, ouverture manuelle, Léo Chasse, clavier, Tombola et modèle indisponible. Capture mobile relue, aucun débordement ni erreur JavaScript. Guides et sources exportables vérifiés sans erreur.
- **Livraison :** commit local sur `feat-moteur-animation`, à pousser puis déployer sur Localeo Animation ; aucune migration ou intervention backend nécessaire. Aucun déploiement réalisé.


## Corrections après T6 — Consultation des brouillons (20 septembre 2026)

- **Participants, backend `475d992` :** lecture autorisée d’une liste réellement vide en BROUILLON/CONFIGUREE sans définition publiée. Compteur réel contrôlé après les habilitations. Les routes par animation et la liste globale filtrée partagent le correctif. Données incohérentes, inscription, jeu, validations et exploitation restent soumis aux contrôles existants.
- **Configuration, Animation `07f4f3d` :** le dossier de vérifications n’est demandé qu’après la lecture réussie du parcours ; son absence affiche « Enregistrez d’abord le parcours pour préparer sa vérification ». Le brief, les dates, le règlement et les lots restent consultables. Les autres erreurs restent affichées. La préparation devient consultable à la lecture suivant son acceptation par l’ERP.
- **Validations et Live, Animation `07f4f3d` :** avant publication, affichage explicatif avec accès à Configuration. Aucun appel d’exploitation prématuré. Les écrans publiés gardent leurs contrôles et actions. Précision tracée en **T6-UX04**, sans contrat ou migration supplémentaire.
- **Preuves :** `tests/api/test_participants_brouillon.py` : **18 tests réussis**, dont les trois types d’animation, filtres/pagination, permissions/périmètres et refus des usages du jeu. Suite ciblée initiale participants/exploitation : 38 réussis avant ajout du dix-huitième cas. Architecture : 414 réussis et les 2 échecs de recensement préexistants déjà décrits. TypeScript, ESLint et build isolé réussis ; avertissement de bundle >500 Ko préexistant. `tests/browser/hunt-preparation.mjs` : **30 contrôles réussis** sur 1280/390 px, brouillon sans parcours puis génération acceptée, préparation, invitations, QR, vérifications et publication. `tests/browser/exploitation.mjs` réussi sur les deux tailles, correction/gel, droits, continuité et trois moteurs. Capture mobile relue.
- **Mise en service :** déployer ensemble les corrections backend et Animation. Aucun déploiement ni intervention sur base d’exploitation effectués pendant cette correction.

## Correction après T6 — Reçu unique des lots (20 septembre 2026)

- **Demande utilisateur T6-FIN01 :** un seul reçu de paiement pour l’ensemble des lots d’une commande d’animation. Mise à jour de la règle canonique EPIC 50, fonction 5, qui remplace l’affichage antérieur du consolidé accompagné de reçus par achat.
- **Correction backend `cceca57` :** la matérialisation ne génère plus de reçu par type de coffret. La liste et le téléchargement de la commande proposent le reçu consolidé avec toutes les lignes, quantités, montants et total. Les anciens reçus unitaires restent archivés et sont exclus de ce parcours ; les autres documents historiques restent accessibles. Snapshots BUM conservés. Les achats hors animation gardent leur fonctionnement et la confirmation email reste unique en cas de rejeu. La déclaration d’encodage du PDF est corrigée pour préserver les noms accentués des coffrets.
- **Preuves : 68 tests ciblés réussis.** 21 tests sur le reçu unique, PDF réel, archives, téléchargement, commandes impayées/autre animation, snapshots, rejeu et traitement de la commande ; 47 tests sur le paiement hors animation et la préparation des emails. Nouveau fichier : `tests/application/animation_locale/test_recu_unique_commande_lots.py`. `git diff --check` réussi. Aucun contrat API ni migration modifié. Le rendu détaillé du financement crédit/Stripe n’a pas été étendu par ce correctif.
- **Mise en service :** déployer le backend ; le filtrage s’applique aussi aux commandes déjà payées, sans supprimer de fichier ni régénérer leurs acquisitions. Aucun email réel, paiement réel ou déploiement effectué pendant les tests.


## Évolution transverse — Adresse postale du commerce (20 septembre 2026)

La demande utilisateur est implémentée selon la [spécification commune de
l’adresse](../espace-commercant/adresse-postale.md). Les décisions de périmètre
sont tracées : France, adresse de l’établissement distincte de l’adresse fiscale,
absence historique conservée sans valeur inventée, pas de validation externe de
l’existence du lieu ni de révocation des comptes actifs.

### Livraison

| Dépôt | Éléments livrés |
| --- | --- |
| Backend | Objet-valeur `AdressePostale`, normalisation postale, migration additive v247, persistance et projections ; modification de sa propre adresse avec version ; ERP, backoffice SQLAdmin et Onboard lisent et modifient la même fiche. |
| Backend — Onboard | Contrôle obligatoire `POSTAL_ADDRESS_COMPLETE` ; validation, revalidation et clôture bloquées sans adresse complète ; saisie en création et édition, conservation si champ omis, effacement explicite refusé. |
| Animation | Suppression de la saisie d’adresse propre à l’animation. Brief entrant `{id, faits}` par commerçant ; nom et adresse résolus côté serveur. Affichage de l’adresse de la fiche et blocage explicite si elle manque. Révision dans l’ERP adaptée. |
| Commerçant | Formulaire d’adresse dans le profil, disponible en préparation du compte ; enregistrement versionné, erreurs, conflit et relecture après réponse incertaine. |
| Marketplace / Live | Contrats du moteur régénérés. La projection backend du Passeport expose l’adresse canonique quand elle existe. Aucun changement du rendu ou stockage navigateur. |
| Projet central | Règle canonique, contrats API, Onboard, T2-D04 et T2-D14 mis à jour ; OpenAPI documentaire régénéré. |

Les snapshots historiques restent lisibles. Les prompts, résultats et parcours
déjà publiés conservent leur contenu ; un changement d’adresse pendant une
génération en attente est détecté comme contexte obsolète. Les nouveaux prompts
portent la provenance `FICHE_COMMERCANT`. Le schéma de réponse créative du LLM
reste inchangé.

### Preuves exécutées

Les tests Python utilisent `python scripts/validation/test_isolated.py`, sans
configuration opérateur. Les tests navigateur utilisent des API simulées et
des builds isolés. Les commandes sont exécutées à la racine du dépôt concerné.

| Vérification | Résultat |
| --- | --- |
| Backend : objet-valeur, use case, API, persistance et référencement (`test_adresse_postale_dedicated.py`, `test_mettre_a_jour_adresse_postale_commercant.py`, `test_adresse_postale_commercant_api.py`, `test_adresse_postale_commercant.py`, `test_referencement_use_cases.py`) | 63 tests réussis : normalisation, limites postales, droits, version et écritures concurrentes, null historique, refus d’effacement. |
| Backend : Onboard, ERP, droits et backoffice | Ensemble ciblé : 99 réussites ; fichier `tests/application/conformite_fiscale_bum/test_adresse_onboard_erp.py` : 22 réussites après deux preuves supplémentaires (rejet du null ERP et formulaire SQLAdmin réel). |
| Backend : génération et contrats | 112 tests réussis ; projection Live/Passeport : 6 réussites. Adresse serveur, refus d’adresse client ou manquante, changement de contexte et conservation du snapshot vérifiés. |
| PostgreSQL jetable | Migration v247 : 2 réussites. Suite `test_generation_animation_postgres.py` : 23 réussites puis dernier scénario de chasse illustrée réussi après adaptation de sa fixture au brief par références (24 scénarios couverts). |
| Architecture | 416 réussites ; les deux contrôles de recensement préexistants restent en échec, sur les mêmes huit classes et trois use cases documentés le 18 septembre. L’objet-valeur et le use case ajoutés possèdent leurs tests dédiés. Aucune exclusion ni assertion affaiblie. |
| Animation | `node --test tests/animation-engine-registry.test.mjs tests/generation-http-contracts.test.mjs tests/generation-preparation.test.mjs` : 13 réussites ; types, lint et build isolé réussis. Avertissement de taille de bundle supérieur à 500 ko déjà présent. |
| Animation / ERP — génération | Recette `tests/browser/generation-preparation.mjs` : 26 contrôles à 390/1280 px ; `tests/browser/generation-erp.cjs` réussi aux deux tailles. Révision sans adresse client vérifiée. |
| Commerçant | Vitest : contrats API et formulaire d’adresse, 34 réussites ; formulaire d’adresse et section contrat, 12 réussites. Playwright `tests/e2e/merchant-address.spec.js tests/e2e/workspaces.spec.js --workers=1` : 3 réussites, dont saisie à 390/1280 px. |
| ERP / Onboard | `node tests/browser/adresse-commercant-erp-onboard.cjs` réussi à 390/1280 px : création, édition, absence historique, invalidité, non-effacement et protections de session/version. Pagination JavaScript : 2 réussites. Formulaire SQLAdmin structuré réellement généré et contrôlé. |
| Marketplace | `node --test tests/security/animation-engine-registry.test.cjs tests/security/live-game.test.cjs` : 9 réussites. |
| Exports | 97 fichiers du moteur vérifiés dans chacun des trois consommateurs. OpenAPI Animation, Commerçant et EPIC 41 : 610 chemins conformes ; projection Live EPIC 42 : 45. Comparaison avec la génération backend isolée, hors métadonnée SHA de build. |

Captures des formulaires et de la préparation Animation inspectées sur mobile et
bureau. La suite métier complète et la CI distante ne sont pas annoncées comme
exécutées. Aucun message, email ou paiement réel n’a été envoyé par ces recettes.

### Mise en service

Appliquer **v247**, puis déployer le backend et les frontends correspondants.
Onboard, ERP et backoffice font partie du déploiement backend. Les nouveaux
frontends exigent le contrat mis à jour ; coordonner leur livraison.
Compléter les fiches historiques avant validation de leur onboarding ou nouvelle
génération qui les utilise. Aucun remplissage automatique n’est prévu.

Un commit local par dépôt modifié, sur `feat-moteur-animation`. Cette livraison
ne comprend ni push ni déploiement, et la migration n’a été exécutée que sur la
base de test jetable locale.


## Correctif — lecture de la préparation absente (20 septembre 2026)

Signalement : `GET /protected/animation-locale/animations/{id}/preparation`
retournait 404 pour un brouillon existant sans parcours enregistré. La projection
`PreparationPayload` prévoyait déjà un contenu nul, mais le service rejetait
cet état avant de construire la réponse. La précision est tracée en **T6-UX04**
dans la [conception technique](conception-technique.md#t6-ux04--consultation-dune-animation-en-preparation).

- **Backend :** consultation autorisée sans parcours en 200 (`revision: 0`,
  `sourceOperationId: null`, `preparation: null`). Vérification du partenaire,
  de la commune et de la permission avant cette réponse. Les commandes restent
  conditionnées à l'existence du parcours ; aucune donnée n'est créée par le GET.
- **Localeo Animation :** les vérifications attendent une préparation non nulle.
  Le brief et les paramètres restent consultables ; une nouvelle lecture après
  acceptation charge le parcours et ses contrôles habituels.
- **Contrats :** même DTO et mêmes schémas embarqués, sans migration. Livrer
  l'interface Animation avant le backend pour qu'elle gère la réponse vide.

Vérifications locales :

| Contrôle | Résultat |
| --- | --- |
| API : `test_preparation_animation_lecture.py`, `test_generation_animation_api_t2.py`, `test_generation_animation_integration_review_t2.py` avec le lanceur isolé | 36 réussites : lecture répétée sans parcours, parcours existant, inconnue, autre partenaire/commune, absence de permission, édition refusée sans parcours. Ports mémoire, aucune base distante. |
| Architecture et recensement | 416 réussites ; deux échecs préexistants de recensement des classes du domaine et des use cases, déjà documentés dans le contrôle d'architecture. Aucun changement de ces classes ni de ces contrôles. |
| Animation : TypeScript, ESLint, `scripts/build-generation-tests.mjs` | Réussis ; avertissement existant sur la taille du bundle supérieur à 500 ko. Build sans environnement opérateur. |
| Animation : `tests/browser/hunt-preparation.mjs` | 30 contrôles réussis, API simulée à 390/1280 px : brouillon sans alerte ni vérification prématurée, parcours accepté, invitations, QR, vérifications et publication. |
| Documentation | Liens et sources exportées vérifiés. |

Livraison sur `feat-moteur-animation` ; déployer Localeo Animation avant le backend. Le push Git ne constitue pas une vérification du déploiement.
Le 500 précédemment signalé sur `validation-publication` n'a pas été reproduit
dans le diagnostic métier ; ce correctif du 404 ne constitue pas une résolution
confirmée de ce second incident.


## Correctif — validation du brouillon sans lots (20 septembre 2026)

La trace complémentaire du 500 `validation-publication` identifie
`KeyError: 'lots'`. Un brouillon créé par `ServiceGenerationAnimation._parametres`
ne contient pas encore cette clé. Quand aucune commande ne couvre les lots,
`ServicePublicationAnimation.valider` appelle le contrôle d'éligibilité qui
accédait directement à `config["lots"]`. Ce scénario a été reproduit par la route
HTTP avec les paramètres issus du générateur.

Le backend lit désormais la sélection facultative avec `config.get("lots") or []`,
comme les autres contrôles de financement et d'éligibilité des lots. La lecture
retourne le rapport **200**, avec `valide: false` et les blocages existants.
Les coffrets et commerçants sélectionnés restent contrôlés ; la commande de
publication reste refusée en **422** sur cette route historique tant que la
configuration est incomplète. Aucun état, lot, paiement ou parcours n'est créé
par cette correction. La précision est intégrée à **T6-UX04**.

Vérifications avec le lanceur isolé, sans base distante ni configuration opérateur :

- `tests/api/test_validation_publication_brouillon.py` : huit scénarios couvrent
  lots absents, nuls ou vides, deux consultations successives sans mutation,
  publication refusée, sélections inéligibles et refus d'accès hors droits ou
  périmètre. Route réelle, services de validation/financement réels et ports
  mémoire ; authentification injectée et droit d'abonnement simulé.
- Avec `tests/api/test_publication_api_t3.py` et
  `tests/application/animation_locale/test_financement_lots_animation.py` :
  **25 tests réussis**.
- Architecture et recensement : **416 réussites, deux échecs préexistants**
  des contrôles de recensement, déjà documentés. Aucun ajout de skip ni exclusion.
- Guide et sources documentaires : vérifiés.

Livraison sur `feat-moteur-animation` par commits séparés dans `localeo-backend`
et `localeo-projet`, sans nouveau schéma, contrat frontend ni migration. Le
backend de test répondait encore `1.0.0+0cb250c` pendant le diagnostic : il doit
recevoir ce correctif pour que la résolution soit effective à distance. Le push
ne constitue pas une vérification du déploiement ; aucune recette distante de ce
correctif n’a été effectuée.


## Optimisation — requêtes de configuration partagées (20 septembre 2026)

Plusieurs composants du même écran chargeaient indépendamment les modèles,
les commerçants éligibles et la préparation. La mutualisation des GET simultanés
du transport ne supprimait pas les lectures lancées après la fin de la première.
La décision est tracée en **T6-UX05**.

- Le détail Animation fournit son modèle au formulaire de configuration.
- Le bloc financier de la Chasse ne consulte plus les commerçants, qui restent
  chargés par le brief.
- L'éditeur transmet sa lecture du parcours aux vérifications. La sauvegarde
  confirmée partage aussi une seule relecture. Une actualisation explicite
  consulte le serveur ; les changements des paramètres communs relancent les
  contrôles concernés. Les erreurs, reprises et saisies en cours sont conservées.
- État en mémoire limité à l'écran, invalidation de session/commune du transport
  conservée et réponses tardives écartées. Aucun cache persistant, changement de
  contrat API, répétition automatique de commande ou migration.

Preuves locales, sans configuration opérateur ni backend distant :

| Vérification | Résultat |
| --- | --- |
| `tests/browser/hunt-preparation.mjs` | 60 contrôles à 390/1280 px : un GET par endpoint ciblé à l'ouverture, relecture unique après sauvegarde, actualisation, erreur/reprise et échec initial ; invitations, QR, checklist et publication conservés. |
| `tests/browser/generation-preparation.mjs` | 26 contrôles à 390/1280 px : création et préparation avec Léo, composant également utilisé hors de l'écran partagé. |
| Tests Node ciblés : `http-context`, `hunt-preparation`, `generation-preparation`, `generation-http-contracts` | 18 réussites ; contexte périmé, déconnexion, contrats et commandes idempotentes. |
| TypeScript, ESLint, build navigateur isolé | Réussis ; avertissement existant de taille du bundle supérieur à 500 ko. |

Une exécution navigateur a été interrompue par `ERR_NETWORK_IO_SUSPENDED` sur
le serveur local ; la recette finale a ensuite abouti. Les attentes réseau et
d'affichage du test sont explicites, sans masquer les erreurs ni assouplir les
compteurs de requêtes.

Livraison sur `feat-moteur-animation` par commits séparés dans
`localeo-animation` et `localeo-projet`. Le correctif backend `KeyError: 'lots'`
est livré dans son propre commit. Déployer le frontend pour appliquer
l'optimisation sur l'environnement de test ; le push ne constitue pas une
vérification du déploiement et aucune recette distante n’a été effectuée.

## 23 septembre 2026 — T6-UX06 : préparation guidée et traitement ERP

Défaut signalé : après réception de la proposition, le gestionnaire ne sait pas
où il en est ni quelle action réaliser dans la configuration. Le code local
empilait parcours, paramètres, terrain, financement et publication. Dans l'ERP,
les trois blocs restaient affichés ensemble malgré le repère d'étapes.
La version distante signalée n'a pas été consultée. Base locale : Animation
`45100bb`, backend `94f33bb`, projet `7c085fa`, avec les changements de ce correctif.

Correction décrite par T6-UX06 dans la [conception](conception-technique.md) et
le [guide d'usage](exploitation-moteur.md) :

- Animation : six étapes navigables, une visible à la fois, état du parcours,
  action attendue, aide et retour aux rubriques. Les invitations sont intégrées.
- Les formulaires déjà ouverts restent montés pour conserver leurs saisies.
  Une visite ne vaut pas validation. Les modifications non enregistrées du
  parcours, des paramètres et du terrain sont signalées et empêchent de publier.
- Les commandes incertaines conservent leur résolution visible ; la navigation
  ne provoque aucune écriture. Le retour de paiement ouvre le suivi financier
  tout en conservant la lecture partagée du parcours.
- La relecture des conditions de publication invalide immédiatement toute
  confirmation précédente, y compris si la nouvelle lecture échoue.
- ERP : **Générer → Importer → Valider**, dépôt par texte ou fichier visible,
  reprise et actualisation du contexte accessibles près du blocage. La
  pré-vérification, l'enregistrement et la transmission après relecture restent
  explicites ; la transmission complète le brouillon et ne le publie pas.

Preuves locales avec données synthétiques et API simulées pour le navigateur :

| Vérification | Résultat |
| --- | --- |
| Reproduction avant correction | Le test exigeant la navigation « Étapes de configuration » échoue sur l'interface antérieure, qui ne la contient pas. |
| `node --test tests/*.test.mjs` dans Animation | 143 tests réussis, aucun échec ni test ignoré. |
| Types TypeScript et ESLint Animation | Réussis. |
| `node scripts/build-generation-tests.mjs` | Build isolé réussi ; avertissement de taille du bundle supérieur à 500 ko, également observé avant modification. |
| `node tests/browser/hunt-preparation.mjs` | 106 contrôles à 1280/390 px : étapes, lecture seule, saisies conservées, absence d'écriture de navigation, lectures partagées, invitations, QR, contrôles terrain, reçus perdus, publication, erreur/reprise, retour de paiement et saisies non enregistrées. |
| `node tests/browser/generation-preparation.mjs` | 26 contrôles à 1280/390 px. L'attente de relecture cible désormais le titre de l'aperçu chargé ; l'ancien sélecteur pouvait prendre le titre de phase avant la fin du GET. |
| `node tests/browser/exploitation.mjs` | Réussi à 1280/390 px : exploitation, correction/gel, droits, continuité et trois moteurs. |
| `node tests/browser/generation-erp.cjs` dans le backend | Réussi à 1280/390 px : panneaux exclusifs, saisie conservée, reprise visible, validation sans écriture, dépôt, réconciliation et relecture obligatoire. |
| Lanceur backend isolé : `test_generation_animation_api_t2.py`, `test_verification_reponse_generation_api.py`, `test_generation_animation_integration_review_t2.py` | 29 tests réussis. |
| Captures mobile et bureau | Inspectées ; aucun débordement horizontal dans les recettes. |
| Revue indépendante | Droits, saisies, retours de paiement et confirmations relus ; les risques identifiés de retour financier masqué et de confirmation périmée ont été corrigés. |

Impacts : aucune modification de contrat API, de règle métier backend, de schéma
persistant ou de générateur de démonstration. Les fixtures conservent leurs
données ; les parcours navigateur sont adaptés à la nouvelle navigation. Aucune
génération sur environnement réel, migration, réparation de données ni opération
de paiement réelle n'a été exécutée. Les sources canoniques d'usage et de
conception sont mises à jour. `check_guidance.py` contrôle 85 documents et 831
liens sans erreur ni avertissement ; `sync_documentation.py --check-sources`
valide les 117 sources exportées. Les vérifications `git diff --check` passent
dans les trois dépôts modifiés.

Ces preuves locales ne constituent ni une recette humaine sur le terrain ni
une vérification des environnements déployés. Commit, push et déploiement restent
des opérations distinctes de cette correction.

## 24 septembre 2026 — T6-UX07 : configuration visuelle du parcours de Chasse

Défaut signalé : l'éditeur imbriqué rend difficile la lecture de l'enchaînement
et la configuration d'une étape. Reproduction locale sur la base Animation
`92da72f` : la recette exigeant la navigation « Étapes du parcours » échoue,
car l'éditeur précédent ne la propose pas. Base documentaire : `ad704a1`.

La correction décrite dans la [conception](conception-technique.md) remplace
l'édition générique des étapes par une liste ordonnée et le détail de l'étape
sélectionnée. Le [guide d'usage](exploitation-moteur.md) explique la navigation,
l'édition des activités, les missions alternatives et l'aperçu joueur.

- Les déplacements conservent l'étape sélectionnée et le focus clavier.
- Les champs joueur, l'activité et les préparatifs privés sont regroupés.
- Les corrections se configurent à partir des libellés des réponses.
- Les suppressions d'étapes ou de missions et les remplacements d'activités
  nécessitent une confirmation explicite.
- Les cinq types d'activité disposent d'un aperçu interactif local, accessible
  aussi en lecture seule. L'indice et la correction sont ouverts à la demande.
- Les IDs, champs non édités et médias partagés restent conservés ; les essais
  et la mission consultée ne deviennent ni réponses ni choix métier enregistrés.

La revue indépendante a identifié un état d'aperçu conservé après suppression
d'une étape virtuelle suivie d'une activité identique. La réinitialisation de
l'essai a été corrigée. Les recettes ont également révélé des noms accessibles
de menus contenant le texte de leurs options ; les libellés ont été explicités.

Preuves locales :

| Vérification | Résultat |
| --- | --- |
| `node --test tests/*.test.mjs` | 153 tests réussis, aucun échec ni test ignoré ; déplacement, sélection, IDs et références des activités couverts. |
| Types TypeScript et ESLint Animation | Réussis. |
| `node scripts/build-generation-tests.mjs` | Build isolé réussi ; avertissement préexistant de bundle supérieur à 500 ko. |
| `node tests/browser/hunt-preparation.mjs` | 194 contrôles réussis à 1280/390 px : sélection et déplacement, alternatives, cinq aperçus, ajout/retrait d'association, confirmation de retrait, sauvegarde des IDs, lecture seule et réinitialisation après suppression de deux activités identiques. Les contrôles existants de préparation et de publication restent actifs. |
| `node tests/browser/generation-preparation.mjs` | 30 contrôles réussis à 1280/390 px ; le test ouvre explicitement la présentation globale avant son édition. |
| `node tests/browser/exploitation.mjs` | Réussi à 1280/390 px : exploitation, correction/gel, droits, continuité et trois moteurs. |
| Captures mobile et bureau | Navigation, édition bureau, aperçu et lecture seule inspectés ; absence de débordement horizontal contrôlée. Les captures supplémentaires des champs sur mobile sont prévues par le script mais n'ont pas été exécutées. |
| Revue indépendante | Identités, médias, alternatives, lecture seule et préservation des corrections relus ; défaut de réinitialisation d'aperçu corrigé. |

Les contrôles documentaires `check_guidance.py` et
`sync_documentation.py --check-sources` vérifient respectivement 85 guides,
833 liens locaux et 117 sources exportées. `git diff --check` passe dans les
deux dépôts modifiés.

Impacts : `localeo-animation` et les sources canoniques `localeo-projet`.
Aucun changement d'API, de domaine backend, de schéma persistant ou de données
de démonstration. Aucun environnement distant n'a été modifié. Les preuves
navigateur utilisent des données synthétiques et une API simulée ; elles ne
valident pas le rendu de Localeo Live ni une recette terrain. Commit, push et
déploiement restent distincts de cette correction.
