# Moteur d’animation — compte rendu d’implémentation

Branche commune : `feat-moteur-animation`, dans les cinq dépôts indépendants. Source de vérité : [spécification](localeo_animation_engine_spec.md), [conception technique](conception-technique.md) et [documents d’entrée](contrats/README.md). Ce suivi distingue code local vérifié, fonctionnalités raccordées et recette avant ouverture.

## État des lots

| Lot | État | Résultat et reste à faire |
| --- | --- | --- |
| T1 — Socle et contrats | Livré et vérifié localement | Registre des trois moteurs, modèles fermés et exports consommés, coordination SQL, exécutions, transaction commune des commandes historiques. Détails ci-dessous. |
| T2 — Générer et préparer | Livré et vérifié localement | Brouillon et quota atomiques, workflow manuel et worker, import complet/médias, ERP et préparation guidée. |
| T3 — Confirmer les missions | À réaliser | Alternatives, engagements versionnés, confirmations, checklist, assemblage et publication. |
| T4 — Jouer et reprendre | À réaliser | Projections privées, commandes persistées, trois renderers et cinq défis, QR/preuves et reprise. |
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


## Décisions d’implémentation

Les précisions T1-D01 à T1-D04 sont inscrites dans la [conception technique, section 9.3](conception-technique.md#93-précisions-dimplémentation-t1--19-septembre-2026) : clés JSON, composition explicite des transactions, commits par dépôt concerné et noms du DSL. Les précisions T2-D01 à T2-D14 sont inscrites en section 9.4 de la conception : routes/reçus, interface, stockage privé/provenance, faits de lieux, import fidèle, images, templates, conservation, catalogue, ordonnanceur, identités et dépendances. Aucun arbitrage fonctionnel n’est remplacé par ce compte rendu.

## Commits

Aucun push ni déploiement n’est inclus. Le commit documentaire central de chaque lot est identifiable par son message dans son historique ; il ne peut contenir sa propre empreinte.

| Lot | Backend | Animation | Commerçant | Marketplace/Live | Documentation centrale |
| --- | --- | --- | --- | --- | --- |
| T1 | `96bb488` | `d813be8` | `e57cbcd` | `5190106` | `docs(animation): documenter la livraison du socle T1` |

| T2 | `43f7495` | `58a34d2` | `cd2277d` | `6d05e35` | `docs(animation): documenter la livraison du lot T2` |

Contrôles documentaires T2 : 76 guides, 734 liens locaux, aucune erreur ni avertissement ; 117 sources exportées vérifiées.

[Retour au dossier moteur](README.md).
