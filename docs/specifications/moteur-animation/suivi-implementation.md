# Moteur d’animation — compte rendu d’implémentation

Branche commune : `feat-moteur-animation`, dans les cinq dépôts indépendants. Source de vérité : [spécification](localeo_animation_engine_spec.md), [conception technique](conception-technique.md) et [documents d’entrée](contrats/README.md). Ce suivi distingue code local vérifié, fonctionnalités raccordées et recette avant ouverture.

## État des lots

| Lot | État | Résultat et reste à faire |
| --- | --- | --- |
| T1 — Socle et contrats | Livré et vérifié localement | Registre des trois moteurs, modèles fermés et exports consommés, coordination SQL, exécutions, transaction commune des commandes historiques. Détails ci-dessous. |
| T2 — Générer et préparer | Livré et vérifié localement | Brouillon et quota atomiques, workflow manuel et worker, import complet/médias, ERP et préparation guidée. |
| T3 — Confirmer les missions | Livré et vérifié localement | Accords par mission, préparation vérifiée, QR, compilation et publication atomique ; interfaces Animation, Commerçant et ERP. |
| T4 — Jouer et reprendre | Livré et vérifié localement | Définition publiée, inscription adulte, projections filtrées, commandes/reçus, trois rendus Live, cinq activités et attestations commerçantes. |
| T5 — Exploiter et clôturer | À réaliser | Neutralisation, correction, qualification, population figée, audit et indicateurs. |
| T6 — Conserver et ouvrir | À réaliser | Purge/conversion, contrôles croisés et préparation de recette. Le pilote humain et le déploiement effectif restent des opérations distinctes. |

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

Contrôles documentaires T4 : 76 guides, 740 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

Contrôles documentaires T3 : 79 guides, 751 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

Contrôles documentaires T2 : 76 guides, 734 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

[Retour au dossier moteur](README.md).
