# E71 — Vérification et livraison

[Spécification V1](README.md), [backlog canonique](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md). **Implémentation locale et vérification en cours**. Le bilan ci-dessous distingue les tests réalisés des réserves. Aucun import réel ni envoi fournisseur. Les sections historiques de spécification restent datées. La carte reste en V1 sur confirmation utilisateur ; CSV standard seul et report de CA-24 (import spécifique Gironde) sont également confirmés.

## E71-EVOL-10 — implémentation des six lots, 12 novembre 2026

Périmètre autorisé après l’audit : L1 à L6, commit/push et migration TEST seulement
si nécessaire. Backend de départ `25224e0` ; dépôt documentaire `f8923a7` avec les
spécifications E71 et E73 locales préservées. Les travaux E73 de clôture automatique
restent distincts de cette livraison. Epic **En cours**, 83 critères actifs,
CA-24 reporté ; aucune clôture globale déduite de cette recette ciblée.
Code backend enregistré dans le commit `fab8850` ; documentation et contrat sont
livrés dans le dépôt indépendant `localeo-projet`.

| Lot / critères | Comportement livré | Preuves exécutables et limites |
| --- | --- | --- |
| L1 — continuité/navigation, CA-07/15/19/22 | Retour contextualisé, même recherche/page/position ; noms de prospects sur actions/dossiers ; Suivi recherchable ; cinq entrées mobiles et filtres repliés | `tests/browser/crm-productivite.cjs`, recettes historiques `crm.cjs`/`crm-correctifs.cjs` ; recherche page 3, retour explicite/navigateur, clavier, 320/390/1280 px |
| L2 — fiche/journée, CA-78 et CA-04/05/06/21/22 | MOI/ÉQUIPE, groupes disjoints et référence serveur signée ; contact/action/interaction en tête ; lectures et réessais indépendants ; suite facultative après succès | `test_productivite_postgres.py`, `test_productivite_http.py`, `crm-productivite.cjs` : portée, dates Paris/DST, pagination, 409, réponse perdue/même clé, révocation et sélection contact conservée |
| L3 — agenda, CA-80 et CA-62 à 73 | Contexte d’agenda, raccourci Aujourd’hui, semaine partielle explicite, report assisté avec responsable fixe et rappel relatif | Tests domaine/application/API/PostgreSQL rendez-vous et `crm-agenda.cjs` : 60 RDV, report chevauchant son ancien créneau, conflit/version, date/page après retour, texte 200 % |
| L4 — cibles/preuves, CA-79 et CA-15/16/17/18/19/20/34 | Contacts au-delà de 25, références recherchables sans saisie UUID, rattachements lisibles et preuve de gain sélectionnée | `test_references_lisibles_postgres.py`, `crm-selecteurs.cjs` : contact n°26 conservé après retour page 1, refus d’une cible obsolète, opposition explicite, preuve inéligible et conflit ; cause du refus TEST historique encore non établie |
| L5 — traitements, CA-81/82/83 et CA-08 à 12/41 à 59 | Suivi GET visible borné, source/counters réels ; revue page précédente et appliquer/continuer ; évaluation exacte ; recalcul explicite IDS=1 et bilan nommé | `crm-import-progress.cjs`, `crm-actualisations.cjs`, `crm-priorite.cjs`, `crm-qualification-productivite.cjs`, API bilan et tests PostgreSQL imports/priorité ; aucune commande réelle ni fournisseur interrogé |
| L6 — carte/recette, CA-84 et CA-13/23/50/54/55/74 à 77 | Marqueurs accessibles partagés, filtres compatibles/viewport conservés, omissions explicites, profils Commune/EPCI distincts | `crm-carte-axes.cjs`, `crm-priorite.cjs` et recettes quotidiennes ; protocole avant/après conservé dans la spécification, aucune amélioration chiffrée d’usage réel revendiquée |

Passages Python :

- **743 réussites**, 48 avertissements de l’adaptateur datetime SQLite :
  architecture, recensements domaine/use cases, protection des ressources PWA
  et routes CRM. `scripts/validation/test_isolated.py` avec Python 3.14.
- **78 réussites PostgreSQL** dans le groupe final des projections/prospection,
  qualification et générateur ; rapport privé backend
  `tmp/crm-ux-backend-pg/projections-verified.xml`. Puis **5 réussites** pour
  l’import HTTP/source/verrou et les derniers contrôles de journée/API :
  `projections-import-followup.xml`. Base PostgreSQL 18 jetable locale uniquement.
- Rendez-vous : 36 tests domaine/application/navigation, 14 API/PostgreSQL
  ciblés ; le test de performance historique RDV n’a pas été relancé. API bilan
  de priorité : 3 tests isolés réussis. Ces passages sont distincts, leurs
  nombres ne sont pas additionnés aux groupes pouvant couvrir les mêmes tests.
- Retour après reconnexion : **64 tests réussis** sur la navigation agenda/carte
  et la frontière PWA, dont les nouveaux cas de filtres, curseurs, `/plus` et
  redirections anonymes ; 4 avertissements datetime SQLite.

Mesure locale Aujourd’hui : 100 puis 1 000 tâches synthétiques, 17 puis 19
requêtes, 87 puis 132 ms ; pages ≤25, totaux exacts. La cardinalité ne déclenche
aucune lecture par tâche. Cette mesure ne constitue pas une charge concurrente
Render et ne lève pas les réserves historiques de capacité.

Les recettes navigateur servent les véritables modules du shell avec des
réponses HTTP synthétiques. Elles ne prouvent pas le déploiement sur TEST ni
une session sur téléphone physique. Les captures locales sont contrôlées pour
la lisibilité, le reflow et les erreurs de dialogue ; les rapports privés ne
sont pas exportés dans ce dépôt documentaire.

Revue indépendante des règles et contrats : aucune élévation de droit ni
contournement de preuve constaté. Les constats de revue UI ont été corrigés :
instant des badges aligné sur la journée serveur, erreurs de dialogue visibles
après reflow mobile, libellé Aujourd’hui non coupé, contexte conservé après refus
du retour navigateur, boîte de saisie réutilisable après panne de contexte et
message explicite lors d’un changement de droits. Les retours après connexion
restent limités aux routes et paramètres CRM autorisés.

Contrôles documentaires : 97 guides et 1 229 liens ; variante des documents
modifiés, 19 documents et 672 liens ; zéro erreur/avertissement. Les 150 sources
exportées sont valides. Les avertissements Git de conversion CRLF/LF ne sont pas
des erreurs de contenu. Les mesures d’usage avant/après et la recette sur appareil
physique restent à réaliser, sans instrumentation d’activité ajoutée.

Contrats : OpenAPI V1.6 régénérée hors ligne (**81 chemins, 139 schémas**), routes
et DTO lisibles, droits inchangés. Backend/PWA et sources canoniques seuls
affectés ; Animation, Marketplace et Pro ne consomment pas ces API. Générateur
inchangé et test de compatibilité exécuté ; sa fixture historique a été alignée
sur les migrations d’agenda déjà requises, sans assertion supprimée.

**Base TEST : aucune migration à appliquer pour E71-EVOL-10.** Les colonnes et
contraintes nécessaires existent avec v311/v312, dont l’application précédente
est documentée ci-dessous. Aucun SQL, import, envoi ou changement de droits TEST
n’a été réalisé pour cette implémentation. Le refus UX-15 rencontré pendant
l’audit demeure une réserve TEST : les mêmes lectures passent avec ADMIN et
lecteur nominatif en recette HTTP, et les erreurs 401/403 sont désormais
distinguées, sans prétendre avoir identifié la cause de l’incident historique.

## E71-EVOL-10 — audit et spécification UX, 12 novembre 2026

[Audit détaillé](../../audits/backend/localeo-crm-ux-productivite-2026-11-12.md) et
[matrice des six lots](ux-productivite.md#lots-dépendances-et-traçabilité).
V1.6 : CA-78 à 84 ajoutés, 83 actifs et CA-24 reporté ; epic En cours.
**Spécification seule : aucun changement applicatif ni test métier exécuté.**

- Lecture du backend `25224e0`, deux explorations indépendantes quotidiennes et
  agenda/qualification ; revue de contrats distincte de la validation documentaire.
- TEST en lecture seule : Aujourd’hui/rappel/fiche, recherche et retour, formulaire
  d’échange non soumis, liste Suivi et agenda vide ; bureau et émulation 320/390 px.
  Perte de recherche reproduite, coordonnées trop bas, lignes sans nom de prospect
  et navigation mobile encombrée constatées. Captures de session dans la conversation.
- Limite : détail du dossier interrompu par l’écran 401/403 « Accès à vérifier ».
  Cause non établie ; pas de reconnexion avec changement de droits ni gain tenté.
- Imports, actualisation, calcul, carte et agenda chargé : constats de code,
  sans mutation de données, interrogation de fournisseur ni notification réelle.
- Projections/DTO cibles, tests synthétiques nominaux/refus/concurrence et mesures
  de capacité restent à réaliser avec les lots. Une recette commerciale nominative,
  clavier/texte 200 % et appareil physique est prévue ; elle n’est pas acquise.

Les contrôles documentaires de cette phase ne valident pas les comportements
cibles. Les preuves des évolutions précédentes et des migrations restent ci-dessous.

La revue indépendante a fait préciser le report assisté (exclusion autorisée de
la seule occupation du RDV, curseur lié au contexte), le rappel par défaut à
l’heure du RDV sans désactivation de date ajoutée, la portée MOI et les groupes
disjoints, ainsi que la distinction refus d’accès/panne technique. Ces précisions
restent des contrats et scénarios à implémenter/tester, pas des résultats exécutés.

Contrôles documentaires exécutés depuis `localeo-projet`, base `f8923a7` avec les
modifications locales conservées et E71-EVOL-10 : `py -3.14 scripts/check_guidance.py`
(97 guides, 1 225 liens, zéro erreur/avertissement), variante
`--changed --all-markdown` (19 documents, 669 liens, zéro erreur/avertissement),
`py -3.14 scripts/sync_documentation.py --check-sources` (150 sources vérifiées)
et `git diff --check` réussis. Backend inchangé et propre pendant cet audit.
Ces résultats ne valent ni test de l’API cible, ni migration, ni livraison de l’UX.

## Migrations v311/v312 sur TEST — 12 novembre 2026

Exécution explicitement demandée après publication du backend `25224e0`.
La cible du profil privé TEST a été vérifiée, distincte de production ; le plan
du lanceur canonique ne contenait que `v311_crm_rendez_vous.sql`, puis
`v312_crm_rendez_vous_notifications.sql`. Les empreintes précédentes sont valides.

- Sauvegarde PostgreSQL complète au format custom avant migration :
  **73 154 692 octets** ; catalogue de l’archive vérifié avec `pg_restore --list`.
  Empreinte SHA-256 :
  `0721fd886ec18427d95ed957c2a56b6b4cfd95196cd424d54cbaefce7aacc3da`.
  Sauvegarde et rapports privés, ignorés par Git, dans le backend sous
  `tmp/migration-v311-v312-test-20261112/`. Pas de restauration réelle effectuée.
- Les deux migrations sont enregistrées ; contrôle des empreintes identiques
  aux fichiers versionnés, et nouveau plan vide. SHA-256 v311 :
  `e3865c4fa5c341144394360baedd24171be0532c8a444383e7a9fcf05efe3d40` ;
  v312 : `ee831b392314deddac33bcc91118587f604a4b4e4973a006ae74e292bb20fc55`.
- Colonnes, sept index et contraintes vérifiés, notamment la liaison différée
  tâche/rendez-vous et les unicités des notifications par type d’événement.
  Les compteurs CRM sont inchangés : **1 558 prospects, une tâche et aucune
  intention de rappel**. Aucun agenda, rendez-vous ou message n’a été créé.
- `/sante` répond **HTTP 200, OK**, version **`1.0.0+25224e0`**.
  La readiness protégée répond **HTTP 200, READY**, sans contrôle en échec ;
  elle contrôle effectivement les tables et index de l’agenda.

Aucun redémarrage manuel, changement de flag, recalcul ou envoi de notification.
Le parcours de réservation avec un compte CRM nominatif n’a pas été exécuté
sur TEST dans cette opération ; les recettes locales précédentes restent
distinctes des contrôles du schéma et de santé effectués ici.

## E71-EVOL-09 — carte par priorité ou responsable, 12 novembre 2026

Référence de livraison Git du 12 novembre : backend **`25224e0`**, regroupant
l’agenda E71-EVOL-08 et la carte E71-EVOL-09. Les migrations v311/v312 sont
appliquées sur TEST par l’opération distincte documentée ci-dessus.

Périmètre : [deux axes de lecture](import-carte.md#e71-evol-09--deux-axes-de-lecture-12-novembre-2026),
CA-74 à 77. Backend/PWA CRM et documentation seulement ; aucun changement des
trois frontends voisins. Les travaux locaux agenda et ERP antérieurs sont
conservés. Aucun déploiement, import réel ou recalcul de qualification.

La PWA propose **Colorer par : Priorité commerciale / Responsable du prospect**.
Les communes mixtes ont des segments proportionnels ; légende, fenêtre du point
et liste montrent les catégories et leurs effectifs. Un responsable non éligible
est nommé À réaffecter, un prospect sans responsable reste Non attribué. Les
24 responsables détaillés, le reliquat et les 500 communes sont bornés côté SQL.

| Critères | Preuves exécutées |
| --- | --- |
| CA-74 | Recette Leaflet réelle, données/tuiles synthétiques : sélection, URL, rechargement, passage à la liste puis retour navigateur ; axe, filtres, zoom et emprise conservés. Tests de retour de connexion sécurisé et multi-niveaux. |
| CA-75 | Tests PostgreSQL : six niveaux, profil non disponible, Commune/EPCI distincts, validité/génération/règle périmée, changement de profil, contexte de dossier, responsable prospect distinct de celui du dossier, révoqué et non attribué ; plafonds 24/500, exclusion de la 501e commune de la légende. HTTP : enum, DTO, refus d’accès et projection historique conservés. |
| CA-76 | Recette 320/390/1280 px, nom et effectif accessibles, ouverture clavier, couleurs UUID stables après tri/filtre, erreur/reprise, données obsolètes ignorées ; panne réelle de tuiles simulée HTTP503 puis configuration sans fond, deux axes encore lisibles dans la légende et les listes. Captures relues. |
| CA-77 | Répartition et totaux issus d’un même snapshot, une lecture SQL métier ; tests N/10N et lecture/réaffectation concurrentes ci-dessous. Contrôles d’architecture, de confidentialité des ressources et revue indépendante. |

Rapports locaux du backend, sans données réelles :

- **6 tests HTTP/PostgreSQL réussis** : `tmp/crm-map-core-tests.xml` ;
  **25 tests de compatibilité carte réussis** : `tmp/crm-map-core-legacy.xml`.
  **21 tests finaux Qualification/HTTP/PostgreSQL réussis**, sans skip :
  `tmp/crm-map-core-final.xml`. Ces groupes se recouvrent et ne s’additionnent pas.
- **38 tests réussis** de navigation carte/agenda et protection PWA :
  `tmp/crm-map/navigation-01.xml`. **25 tests réussis** de cycle PWA :
  `tmp/crm-map/lifecycle-01.xml`, dont changement de version après modification
  des modules carte, priorité et agenda. L’intégration ajoute le module agenda
  à l’empreinte, manquant dans la précédente évolution. Les avertissements
  SQLite concernent son adaptateur datetime déprécié.
- **700 contrôles réussis** d’architecture et de couverture domaine/use cases :
  `tmp/crm-map/architecture-01.xml`. Aucun changement de production après ce
  passage, hormis le centre Mercator couvert par la recette et la régression CRM.
- **Sept groupes de vérifications navigateur réussis** :
  `tmp/crm-map-ui-retour-fond-final.log`, captures `tmp/crm-map-ui-c32e0e23`.
  La première preuve de retour détectait un décalage d’emprise : le centre
  utilise désormais les coordonnées projetées Mercator au lieu d’une moyenne
  de latitudes. L’assertion d’égalité d’emprise n’a pas été relâchée.
- Régressions CRM, Agenda et Qualification réussies :
  `tmp/crm-map-ui-regression-crm.log`, `tmp/crm-map-ui-regression-agenda.log`,
  `tmp/crm-map-ui-regression-priorite.log`. CRM rejoué après correction du centre :
  `tmp/crm-map-ui-retour-regression-crm.log`.

**Capacité locale : trois tests finaux réussis**, PostgreSQL 18 jetable,
20 lectures par axe et filtre, trois dossiers par prospect, 40 responsables,
trois publications historiques de qualification. Une lecture SQL métier par
appel, hors réglages transactionnels existants. Mesures du repository et de SQL,
hors transport HTTP et rendu navigateur :

| Axe / filtre | p95 à 1 000 prospects | p95 à 10 000 prospects |
| --- | --- | --- |
| Priorité / général | 41,48 ms | 193,45 ms |
| Priorité / recherche rare | 8,15 ms | 14,89 ms |
| Priorité / étape Discussion | 64,67 ms | 378,05 ms |
| Responsable / général | 13,08 ms | 36,17 ms |
| Responsable / recherche rare | 7,74 ms | 14,07 ms |
| Responsable / étape Discussion | 22,27 ms | 56,22 ms |

Deux lecteurs de vingt appels chacun et vingt réaffectations simultanées passent
sans incohérence : p95 priorité **59,81 ms**, responsable **20,92 ms**.
Rapports `tmp/crm-map-core-performance.xml`,
`tmp/crm-map-core-performance-1000.json`,
`tmp/crm-map-core-performance-10000.json`, `tmp/crm-map-core-mixed.json`.
Ils conservent les durées et les plans normaux/préparés avec buffers ; les
lectures utilisent les projections, sans relire l’historique des résultats.

**Limite observée :** le premier passage à 10 000 prospects dépassait le budget
pour Priorité + Discussion (**4,48 s p95**). L’essai de diagnostic puis le passage
final réussissent sans changement SQL ni relâchement de seuil. La cause de cet
écart n’est pas établie ; d’autres contrôles locaux tournaient pendant une partie
du premier essai. Rapports initiaux conservés sous
`tmp/crm-map-core-performance-initial.xml` et
`tmp/crm-map-core-performance-initial-{1000,10000}.json`.
La mesure finale respecte la cible de 1 s ; elle ne garantit pas la capacité
hébergée ni l’absence de variabilité sous contention.

Le contrat OpenAPI canonique **1.5** est régénéré hors ligne (80 chemins,
128 schémas). Revue indépendante producteur/DTO/consommateur et URL : aucun
défaut bloquant ; les écarts de légende, d’aide et d’export ont été résolus.
Les preuves retour navigateur et fond indisponible ont été ajoutées à sa suite.
Contrôles documentaires : 97 guides et 1 218 liens sans erreur, puis 81 guides
et documents ciblés, 1 131 liens sans erreur ; 149 sources exportées vérifiées.
Les deux dépôts passent `git diff --check`.

Pas de migration ni de configuration propre à cette carte. Les migrations
v311/v312 de l’agenda restent nécessaires à la version backend globale. Aucun
nouvel objet métier pour le générateur ; fixtures synthétiques enrichies pour
les répartitions et les limites. Les capacités historiques à 100 000 prospects
et la charge hébergée ne sont pas garanties par les mesures locales de ce lot.
L’epic reste **En cours** ; seul le périmètre CA-74 à 77 est traité ici.

## E71-EVOL-08 — agenda et rendez-vous, 12 novembre 2026

**Implémentation locale vérifiée**, sans déploiement ni application des nouvelles
migrations sur TEST. Choix utilisateur : agenda intégré au CRM, validation de
prise en charge par le collaborateur désigné. Périmètre et critères dans la
[spécification rendez-vous](rendez-vous.md). L’epic reste **En cours**.

Contexte : backend `95b7db2` et projet `b43ffa9` avec changements locaux.
Les modifications antérieures de dialogue de session ERP et les traces de la
réparation v310 ont été conservées. Les trois frontends voisins ne consomment
pas les nouvelles API privées : aucune modification de ces dépôts.

Le domaine Prospection porte disponibilités, chevauchement, dates et transitions.
L’application réserve, synchronise l’action du prospect, l’audit, le reçu et les
intentions de notification dans une transaction. La PWA expose un agenda
jour/semaine, les disponibilités personnelles, la réservation depuis une fiche,
le suivi et les notifications personnelles. Un compte rendu rejoint l’historique
et permet de préparer la prochaine action avec le prospect déjà choisi.

| Critères | Comportement vérifié et preuves |
| --- | --- |
| CA-62/64 | Plages multiples, absences, absence de configuration, heure de Paris/DST, prochaines disponibilités calculées sur les réservations réelles. Tests domaine `test_rendez_vous_dedicated.py`, services et PostgreSQL ; parcours navigateur de configuration et recherche paginée. |
| CA-63/65/68 | Agenda filtrable, pagination SQL, fiche prospect, création/rejeu, action avec icône calendrier et état propre, ancien type de tâche conservé. Tests HTTP `test_crm_rendez_vous_api.py` et scénario `crm-agenda.cjs` ; anciennes suites CRM rejouées. |
| CA-66/67 | Confirmation réservée au responsable ; réalisation avec compte rendu ; report/transfert motivé, annulation, version périmée et reprise. Courses PostgreSQL sur même créneau, créneaux adjacents et absence ; conflit UI conserve la saisie. |
| CA-69/70 | Affectation et rappel distincts ; intention atomique, pas de doublon au rejeu, préférences et droits courants, flux privé et marquage lu. Tests domaine/application/API/SQL des rappels et `test_notifications_rendez_vous.py`. Le transport est simulé, aucune réception sur un appareil réel n’est attestée. |
| CA-71/72 | Compte rendu complet conservé, suivi prérempli, opposition/archivage, garde contre les commandes de tâche génériques, refus atomique du destinataire devenu inéligible. Tests services/HTTP/SQL, dont `test_crm_rendez_vous_destinataire.py` et restauration de la navigation après connexion. |
| CA-73 | Parcours mobile/ordinateur, texte à 200 %, clavier, erreurs et reprises, résultats obsolètes ignorés ; mesures SQL et concurrence locales ci-dessous. Les mesures de saturation et de capacité hébergée restent à réaliser avant activation à grande échelle. |

Résultats exécutés avec Python 3.14, PostgreSQL 18 jetable sur boucle locale et
données synthétiques. Les groupes se recouvrent : ils ne constituent pas un
total de tests distincts.

- **71 tests réussis** dans le groupe cœur final, domaine/application/SQL/HTTP,
  notifications et compatibilité des tâches ; rapport backend
  `tmp/crm-rdv-core-final.xml`. Deux courses renforcées avec deux écrivains et
  vingt lectures simultanées réussies ensuite : `tmp/crm-rdv-core-mixed.xml`.
- **82 tests réussis** dans la régression rappels/notifications :
  `tmp/crm-rdv-notifications-regression-2.xml`. **10 tests HTTP finaux réussis**
  après typage des réponses et intégration des permissions :
  `tmp/crm-rdv-root/api-final.xml`.
- **797 contrôles réussis** d’architecture, recensement domaine/use cases,
  readiness, démonstration et navigation de connexion :
  `tmp/crm-rdv-root/architecture-final.xml`. **26 tests de sécurité UI réussis** :
  `tmp/crm-rdv-ui-security-final.log`.
- **12 parcours navigateur réussis**, à 320/390/1280 px, texte à 200 %, focus et
  fermeture clavier ; erreur de réservation entièrement visible au-dessus du
  pied du dialogue. Rapport `tmp/crm-rdv-ui-livraison.log`, captures relues dans
  `tmp/crm-rdv-ui-73b842ad`. Les trois suites historiques `crm.cjs`,
  `crm-correctifs.cjs` et `crm-rappels.cjs` réussissent sur les sources finales
  (`tmp/crm-rdv-final-regression-*.log`). Ces parcours utilisent des réponses
  synthétiques ; les preuves producteur HTTP/SQL sont séparées.
- **35 tests réussis** de génération/transfert ciblé et non-régression de
  l’outillage : `tmp/crm-rdv-root/restore-helper-final.xml`. La génération réserve deux
  créneaux par les services ordinaires, dont un validé, sans transport externe.
  La restauration SQL reproduisait d’abord un échec de contrainte en coupant
  le lien circulaire tâche/rendez-vous (`restore-before.xml`). Le chargeur
  conserve désormais les FK initialement différées ; la transaction valide
  le lien complet et refuse une référence manquante avec rollback. Les
  contraintes ne sont ni désactivées ni affaiblies. Le helper de restauration
  de la recette complète contrôle les contraintes avant nettoyage, rétablit
  leur mode différé pendant le chargement puis les recontrôle immédiatement ;
  le test ciblé exerce ce même helper sur les tables CRM. Le transfert conserve
  agendas, états et notes ; la neutralisation des notifications restaurées
  et le registre des tables sont vérifiés. Un transfert complet de tous les
  domaines avec sauvegarde externe n’a pas été exécuté pour cette évolution.

Mesure locale finale : 100 membres, 100 puis 1 000 réservations sur le responsable
actif et autant d’historique hors période, vingt répétitions par lecture.

| Lecture service + SQL | p95 à 100 | p95 à 1 000 | Requêtes maximales |
| --- | --- | --- | --- |
| Prochaine disponibilité de l’équipe | 35,09 ms | 48,12 ms | 3 |
| Créneaux d’un membre | 8,98 ms | 47,88 ms | 3 |
| Page de rendez-vous | 8,73 ms | 10,06 ms | 1 |

Vingt réservations supplémentaires non conflictuelles, transaction, reçu et
commit compris : **p95 20,82 ms**, maximum 29,47 ms, 16 requêtes au plus.
Ce dernier budget compte une écriture ; la cible de dix requêtes concerne les
lectures de page. Mesures hors HTTP, session et transport ; le scénario de coût
de réservation n’inclut pas les notifications, qui sont vérifiées séparément.
Quatre plans `EXPLAIN (ANALYZE, BUFFERS)` réels sont conservés, sans forcer les
index. Rapports `tmp/crm-rdv-core-performance-final.json`, `.plans.json` et `.xml`.
Le test ciblé final réussit ; neuf autres tests sont désélectionnés sur ce passage,
et non comptés comme réussis. Ces mesures ne prouvent pas le débit soutenu,
la mémoire, la saturation du pool ni le p95 HTTP sur l’hébergement cible.

La revue indépendante a contrôlé invariants, autorisations, projections et
readiness. Les constats sont corrigés : une validation ou une simple note ne
révise plus le rappel, un changement de durée le révise ; le destinataire
inéligible produit un 409 sans invalider la session de l’appelant. L’horloge des
tests HTTP est figée. Les curseurs de disponibilité conservent les mêmes filtres
temporels entre deux pages, même lorsque le temps avance.

Contrat E71 **V1.4 régénéré : 80 chemins, 122 schémas**. Guides utilisateur,
exploitation, backlog et export documentaire actualisés. Contrôle des guides
et documents touchés : **103 documents, 1 357 liens, zéro erreur ni avertissement** ;
contrôle des **149 sources exportées** réussi, ainsi que `git diff --check`.
Appliquer **v311 puis
v312 avant le backend** selon le [guide d’exploitation](exploitation.md), puis
contrôler readiness, agenda et worker de rappels. Aucun nouveau fournisseur ni
secret : canaux externes sous flags CRM et préférences existants. Pas de commit,
push, envoi réel ou migration distante effectué pour cette demande.

## Correctif local — lancement manuel des batchs, 9 novembre 2026

Demande : pouvoir déclencher tous les batchs depuis **Batchs exploitation**.
Le catalogue contient 31 traitements, mais la page ne proposait que 12 actions
et les quatre batchs CRM étaient déclarés non manuels. Reproduction avant
correction : un POST manuel authentifié par session ADMIN et CSRF était refusé
avec `API key missing` sur la route technique.

Sur la base backend `39d03d8` avec changements locaux : les 31 batchs sont
autorisés manuellement ; les 19 nouveaux formulaires reprennent paramètres,
bornes et valeurs par défaut depuis le contrat HTTP réel. Les 12 parcours
historiques restent compatibles. La vue SQLAdmin utilise le contrat de son
application FastAPI parente, et non celui de l'application Starlette montée.

Les nouvelles actions appellent les mêmes endpoints, compositions et
`BatchRunner`, avec session ADMIN historique, CSRF et en-tête explicite
`X-Batch-Manual: 1`. Aucun secret de scheduler dans le navigateur ; clés et
scopes automatiques inchangés. L'acteur ERP est historisé, y compris dans les
traitements métier coffrets. Les flags désactivés, bornes de passage, simulations,
confirmation des lots CSV et verrous communs ne sont pas contournés. Les
routes voisines, autres scopes et comptes sans autorité restent refusés.

Preuves locales sous le runner isolé Python 3.14 :

- **116 tests réussis** sur batchs/ordonnanceur/HTTP et premières preuves
  manuelles, puis **18 tests manuels finaux réussis** couvrant notamment session
  expirée, profil refusé, CSRF/origine, en-tête seul insuffisant, autre scope,
  refus futur du catalogue, route interne et route protected, acteur persisté
  et verrou d'un passage automatique conservé.
- **30 tests réussis** de compatibilité des clés API et publication juridique.
- **683 contrôles réussis** d'architecture et recensement domaine/use cases.
- **7 tests UI finaux réussis**, dont catalogue complet, bornes Query/JSON,
  simulation, vraie route SQLAdmin montée et navigateur 320/1280 ; les 8 tests
  historiques payouts passent également. Les captures sont relues et les
  appels navigateur simulés, sans envoi fournisseur ni traitement réel.

Les groupes de tests peuvent se recouvrir et ne forment pas un total distinct.
Contrat E71 régénéré hors ligne ; guide d'exploitation commun et guides CRM/SaaS
actualisés. Aucune migration ni adaptation des données de démonstration ou
des trois frontends nécessaire. **Non déployé** ; aucun lancement sur TEST ou
production effectué par cette correction.

## Correctif local — diagnostic du format CSV, 9 novembre 2026

Incident signalé : `LOC-17f1b0aa-9721-48e8-ae53-18981fe0bfda`, message
« Utilisez le modèle CSV UTF-8 séparé par des points-virgules ». La référence
ne donne pas accès aux journaux distants ; le format sélectionné lors de cet
incident n'est pas établi. Reproduction locale avec les deux CSV préparés :
format 1 refusé avec ce message, format 2 accepté intégralement
(2 648 et 1 000 lignes). Aucun défaut UTF-8 ou de séparateur sur ces fichiers.

Le parseur signale désormais `FORMAT_2_REQUIS` si l'en-tête est valide en
format 2 mais incompatible avec le format 1 choisi. Le message HTTP 422 demande
de sélectionner **Format 2** puis de relancer l'analyse. Aucun basculement
automatique de format, aucune tolérance pour des colonnes inconnues, dupliquées
ou obligatoires absentes. Les erreurs de séparateur restent refusées.

Reproduction avant correction : le nouveau test de diagnostic échoue sur
`COLONNES_INVALIDES`. Après correction : **744 tests réussis** via le runner
isolé (architecture, recensements, qualification, parseur et API). Relecture
des deux fichiers réels : format 2 accepté, format 1 refusé avec le nouveau
diagnostic. Aucun import réel exécuté et aucune donnée prospect journalisée.

Impacts : backend, tests et documentation E71 ; forme de réponse HTTP et
en-têtes CSV inchangés. Aucun changement de schéma SQL ni du générateur de
démonstration pour ce diagnostic. Le correctif précédent du responsable
facultatif reste distinct et conserve sa migration v305. **Non déployé**.

## Correctif local — responsable d'import facultatif, 9 novembre 2026

Demande : importer les prospects et leurs éventuels dossiers sans devoir choisir
un responsable. Avant correction, le formulaire et l'API imposaient ce choix,
le traitement contrôlait aussi une valeur absente et le lot SQL était non nullable.
Reproduction HTTP avant correction : champ absent ou vide refusé avec 422
(`responsable_id` requis), champ renseigné accepté.

Correctif testé sur la base backend `1b3e27c` avec modifications locales :
choix **Non attribué** par défaut, API nullable, contrôle d'habilitation conservé
pour tout identifiant renseigné, migration additive **v305**. Les dossiers créés
sans responsable conservent `null`, sans affectation à l'importateur ; les
affectations existantes restent inchangées en UPSERT. Sources canoniques et
contrat OpenAPI régénéré dans `localeo-projet` ; aucun changement des colonnes CSV.

Preuves locales sous Python 3.14 et PostgreSQL 18 jetable :

- Runner isolé, architecture, recensements domaine/use cases, règles d'import et
  contrat HTTP du responsable facultatif : **774 tests réussis**.
- Sécurité PWA et pagination API des imports : **19 tests réussis** ; quatre
  avertissements de dépréciation de l'adaptateur datetime SQLite.
- Imports HTTP, persistance et qualification, hors test de volume : **46 tests
  réussis**. Formats 1/2, avec/sans dossier, confirmation, interruption/reprise,
  absence d'affectation automatique, refus d'un responsable non habilité et
  préservation des affectations au réimport couverts.
- `node --test tests/frontend/crm-import-responsable.test.mjs` : **1 test réussi**,
  formulaire réel envoyé avec choix vide puis explicite ; capture locale relue.
- Import de **10 000 lignes**, relancé seul : **1 test réussi**, dépôt
  **0,576 s**, aperçu **3,990 s**, total **84,043 s**, pic mémoire additionnel
  **11,0 Mio**. Le premier passage avec contrôles concurrents avait dépassé
  le budget du dépôt (**1,043 s** pour un seuil de 1 s) ; aucune assertion
  ni aucun seuil n'a été modifié.
- Revue indépendante du diff : aucun problème bloquant identifié. Contrôles de
  guides et des sources exportées réussis ; aucune ancienne migration modifiée.

Impacts : backend et documentation seulement ; les trois autres applications
ne consomment pas ce formulaire privé. Le générateur de démonstration conserve
ses affectations explicites et ne nécessite pas d'adaptation. Aucun rappel,
envoi, réparation de données ni import réel exécuté. **Non déployé** : appliquer
v305 avec le code avant d'utiliser le choix facultatif sur un environnement.

## Incident TEST — projection de classement absente, 6 novembre 2026

Trace : `UndefinedTable: relation "crm_priorite_configuration_projection"
does not exist` depuis `priorite_api.recherche` / `actualiser_ordre`, profil
`ANIMATION_EPCI_1`. Le backend `868ce6f` attend v299–v302, tandis que la cible
TEST contrôlée via `.env.test` était restée en **v298**, schéma `public`.
Le rejeu de la recherche avec le repository livré reproduit l'erreur PostgreSQL
**42P01** avant réparation ; le plan ne contient que les quatre migrations
attendues. Aucun changement du barème ni patch applicatif nécessaire.

Réparation sur TEST avec le runner canonique `scripts/database/apply_migrations.py` :
**v299_crm_revisions_qualification.sql**, **v300_crm_projection_ordre_priorite.sql**,
**v301_crm_compteurs_dossiers.sql**, **v302_crm_invalidations_actualisation.sql**,
appliquées dans cet ordre, avec vérification des empreintes historiques et
délais SQL/verrous bornés. Sauvegarde complète préalable au format PostgreSQL
personnalisé : **64 535 089 octets**, ACL conservées, empreinte SHA-256 enregistrée,
inventaire et lecture/décompression complète `pg_restore` réussis. Cette lecture
ne constitue pas une restauration effective de l'archive.

Vérifications réelles après migration :

- **v302**, zéro migration en attente ; **83 contrôles de schéma CRM** réussis,
  comprenant colonnes, index, vue, séquence, fonctions et triggers actifs.
- Recherche signalée réussie : **23 EPCI**. Recherche communes : **25 résultats**
  puis **25** sur la page suivante, sans identifiant commun entre les deux pages.
- Nombre de lignes et empreintes du contenu de toutes les tables CRM
  préexistantes inchangés. La colonne technique additive `ordre_creation` de
  v302 est exclue de la comparaison du contenu existant ; sa présence relève
  du contrôle de schéma. Aucun résultat de priorité historique réécrit.
- Les sondes de recherche utilisent le repository applicatif dans des
  transactions annulées, sans publication de calcul, commande métier, envoi
  d'e-mail ni modification de droits. Le parcours HTTP/navigateur authentifié
  n'a pas été rejoué. Production non accédée.

Sauvegarde et rapports privés backend :
`demonstrations/prive/operations/correctif-crm-projection-v302-20261106/`, hors
Git. Le [diagnostic d'exploitation](exploitation.md#configuration) précise le
cas v300 absent et le rattrapage complet v299–v302. Configurer sur Render TEST
`LOCALEO_SCHEMA_READINESS_ENFORCE=true` évite d'ouvrir les écrans sur une base
incomplète ; ce paramètre distant n'a pas été changé par cette opération.

## Correctifs de l’audit performance et sécurité — 6 novembre 2026

Corrections locales sur le backend `ccf71de` et son arbre de travail, avec les
modifications PWA préexistantes conservées. L’audit privé
`tmp/audits/crm-performance-securite-2026-11-06.md` identifie les écarts
CRM-AUD-01 à 08. Ces vérifications locales précèdent le commit et le push du
backend `868ce6f` ; elles n'ont accédé ni à TEST/production ni aux fournisseurs.
L'application ultérieure de v299 à v302 sur TEST et ses preuves sont consignées
dans la section d'incident ci-dessus. Les autres cibles suivent
l’[exploitation](exploitation.md).

| Écart | Correction et preuve locale |
| --- | --- |
| 01 — Révocation différée | Empreinte de référence capturée, journal de révocation relu sous verrou avant les effets ; ancienne référence nominative absente refusée. Tests du vrai adaptateur, bascule, concurrence et capture `REPEATABLE READ`. |
| 02 — Rattachements N+1 | Enrichissement groupé des seuls IDs de la page, droits courants conservés : **5 SELECT pour 25 comme pour 100 rattachements mixtes**, sous le budget de 6. |
| 03 — Tri de priorité global | Ordre transactionnel par générations/règles/échéances, meilleur candidat marqué et indexé. Les filtres de dossier partent aussi du flux ordonné, puis vérifient prospect/candidat par lookup avant la limite de page. Première page et continuation contrôlées au plan. |
| 04 — Agrégats des historiques | Révisions transactionnelles par organisation et EPCI : **4 SELECT pour deux pages**, sans agrégat obligatoire, à 1 000/10 000 évaluations et membres. Plans de page à 26 lignes ; les curseurs sont refusés après mutation pertinente. |
| 05 — Péremption exhaustive à l’adoption | Journal d’invalidation par cible ; décisions explicites, premier auteur/date de péremption et provenance conservés. À 100/10 000 anciens jobs : **25 requêtes dans les deux cas**, environ 49/38 ms pour l’adoption lors du passage dédié. Visibilité au commit, rollback et adoption concurrente testés. |
| 06 — Archivage/opposition exhaustifs en mémoire | Politique de sollicitation du domaine traduite en SQL groupé. À 100/10 000 tâches : **6 requêtes pour archiver, 8 pour opposer**, mémoire Python mesurée sans croissance proportionnelle aux tâches ; timeout de verrou sans effet partiel puis reprise vérifiés. Le travail SQL reste proportionnel aux effets nécessaires. |
| 07 — Carte et charge | Compteurs transactionnels des dossiers, dont `ouverts`, et agrégation cartographique adaptée. Le banc de lectures concurrentes à 100 000 prospects passe jusqu’à 20 lecteurs et au retour à 10 ; les limites ci-dessous restent ouvertes. |
| 08 — Capture avant refus | Au plus 10 001 IDs temporaires, comptages sentinelles avant JSON et attestations ciblées par cible/bloc courant. Refus avant le premier INSERT de faits pour 10 001 prospects, 101 contacts ou 51 dossiers. **100 contacts et 50 dossiers sont acceptés**, capturés puis publiés atomiquement en 50 résultats. |

Les deux anomalies de lecture relevées pendant la revue sont corrigées : un
dossier filtré sans projection conserve son état `NON_CALCULE`, et une échéance
franchie entre l’entretien et la page provoque un refus explicite plutôt qu’un
tri ancien. Le batch entretient les résultats même lorsque les nouveaux calculs
sont désactivés. Un test du meilleur candidat filtré, différent du meilleur
global, vérifie aussi que le repère `NON_CALCULE` ne masque pas un résultat
admissible existant.

Mesures PostgreSQL 18 local jetable, Python 3.14 sous Windows, statistiques
actualisées, fournisseurs remplacés par des doubles :

| Parcours | Mesure et portée |
| --- | --- |
| Priorité, 10 000 prospects / 30 000 projections | Page de 25 : **25,85 ms** ; page de 100 : **62,32 ms**. Trois lectures SQL avec résultats, deux si vide. Plans première page/continuation suivant l’index partiel du meilleur candidat. |
| Priorité avec filtre fréquent `etape=A_CONTACTER`, 1 000 prospects | Page de 25 : environ **24 ms** ; plan première page et continuation : **76 candidats parcourus**, lookup de prospect par clé, aucun scan séquentiel de toutes les organisations. Le plan initial parcourait 1 000 organisations et triait globalement ; la nouvelle assertion de borne a échoué avant correction, puis réussi sans assouplissement. |
| Carte, jeu complet et 20 lecteurs | **100 000 prospects, 300 000 dossiers, 600 000 tâches et 1 000 000 événements** ; carte p95/p99 **856/858 ms**, tableau **506/775 ms**. Budgets existants inchangés : carte 2/3 s, autres lectures 1/2 s. |
| Retour à 10 lecteurs sur le même jeu | Carte p95/p99 **869/883 ms**, tableau **285/305 ms**. Les paliers préalables 1/5/10 passent également. |

Le banc carte concerne les lectures, sans v300 ni projections de qualification
dans sa fixture ; le banc priorité vérifie séparément son propre chemin. Les
caches ne sont pas contrôlés froids/chauds. Ces passages ne démontrent pas une
charge mêlant écritures, imports, rappels, calculs et lectures, ni la mémoire et
la contention de tous ces traitements sur l’hébergement cible. La réserve de
capacité globale et ARB-07 restent ouvertes ; l’epic demeure en cours. Le dernier
correctif du plan avec filtre fréquent de dossier est vérifié à 1 000 prospects ;
son rejeu à 10 000 après correction n’a pas été exécuté.

Vérifications complémentaires exécutées : **671 contrôles d’architecture et de
recensement réussis**, puis **538 tests isolés** domaine,
application, API, readiness, démonstration et scheduler réussis ; **153 tests
PostgreSQL réussis** dans le lot transverse, puis correction d’une fixture
d’attestation qui omettait `dossier_id` et **29 tests de priorité réussis** au
rejeu final. Les **16 tests dédiés** aux révisions/invalidations passent, ainsi
que **7 restaurations** avec triggers actifs et séquence partagée. La chaîne
réelle **v147 à v302**, son rejeu idempotent, son dump et sa restauration passent
sur une seconde base locale initialement vide. Le backfill v300 est également
testé sur deux résultats calculés avant migration : JSON immuable conservé et
ordre fort potentiel avant faible potentiel. Le contrat OpenAPI des nouveaux
refus dispose d’un test dédié réussi.

Les rapports privés sont conservés dans `localeo-backend/tmp/` :
`crm-correctifs-postgres-final.xml`, `crm-priorite-fonctionnels-finaux.xml`,
`crm-priorite-bornes-backfill-final.xml`, `crm-correctifs-isoles-final.xml`,
`crm-correctifs-restauration-final.xml`, `crm-correctifs-migrations-completes-final.xml`
ainsi que `crm-correctifs-architecture-tty-final.xml` et
`priorite-qualification/lectures-*.json`. Les échecs initiaux de fixtures,
d’assertion de plan et de capture de descripteur Windows restent tracés dans
leurs rapports ; les assertions métier et de budget sont conservées.

Impacts : backend et documentation canonique modifiés ; contrats de refus
**429 `CLASSEMENT_EN_ACTUALISATION`**, **503 `REGLE_REMPLACEE`** et remise à zéro
des anciens curseurs explicités dans l’OpenAPI régénéré. Les formes des DTO et
du CSV restent identiques. La PWA conserve son traitement générique des erreurs ;
Pro, Animation et Marketplace ne consomment pas ces routes privées. Le transfert
de démonstration et la readiness suivent les nouveaux objets, index, triggers,
champs et la séquence partagée ; les guides précisent les privilèges DB, le pool
et la reprise. Aucun droit métier nouveau ni activation automatique.

## Correctif Qualification — liste des départements, 6 novembre 2026

Correction locale sur la base backend `ccf71de` : remplacement de la saisie
libre du département par une liste facultative avec numéro et nom. Les douze
départements de Nouvelle-Aquitaine sont fournis au module Qualification depuis
le même référentiel PWA que Prospects et Carte ; aucune liste concurrente.
« Tous les départements » retire le filtre.

Le test navigateur reproduit d'abord le champ libre (`INPUT` au lieu de
`SELECT`), puis `crm-priorite.cjs` et `crm.cjs` passent après correction : les
treize choix réels (tous + douze départements), préselection depuis l'URL,
changement/retrait du département, filtre envoyé au serveur, conservation des
autres critères et après actualisation, capture du calcul sur la recherche,
lecture seule et affichage PC/mobile 1280/320 sans débordement. Captures inspectées.

Pas de modification d'API, de barème ou de périmètre d'accès : le paramètre
`departement` reste inchangé. Sans migration, nouveau paramètre d'exploitation
ou impact sur les données de démonstration et les autres applications. Guide
utilisateur adapté ; correction locale, déploiement non exécuté.

## Correctif CRM — noms des auteurs dans l'historique, 6 novembre 2026

Sur le backend `834aa85`, l'historique affichait directement `auteur_id`, par
exemple `interne:<UUID>`. La fiche prospect et le détail d'un rappel partagent
ce rendu. La correction locale ajoute `auteur_nom` à la projection des échanges
et affiche le prénom/nom actuel ; `auteur_id` et les écritures d'audit restent
inchangés. Compte désactivé : nom conservé en lecture ; compte absent, identifiant
ancien invalide ou nom vide : « Utilisateur indisponible ». Les imports gardent
leur seule source visible, sans réintroduire leurs détails documentaires.

Preuves : `crm-correctifs.cjs` reproduit d'abord l'affichage fautif malgré un
nom disponible, puis réussit sur les deux historiques, le cas indisponible et
l'échappement HTML. Captures PC/mobile **1280/320** inspectées. `crm.cjs` réussit
également. **4 tests API/PostgreSQL** vérifient le champ additif, l'absence de
coordonnées supplémentaires, les UUID préfixés/historiques, comptes désactivés
ou absents, renommage sans modification des auteurs enregistrés, totaux et
pagination. Deux requêtes pour 25 comme pour 100 échanges, une seule pour une
page vide : pas de N+1 ni de chargement complet de l'annuaire.
**671 contrôles d'architecture/inventaire/couverture** réussissent.

Contrat OpenAPI et guides mis à jour. Sans migration ni impact sur les règles
métier, habilitations, batchs ou données de démonstration : seul l'enrichissement
de lecture change, sans colonne persistée nouvelle. Les autres applications
ne consomment pas ces routes CRM. Vérification locale ; déploiement non exécuté.

## Incident TEST — schéma de qualification absent, 6 novembre 2026

Trace signalée : `UndefinedTable: relation "crm_priorite_generations" does not
exist` depuis `priorite_api.recherche` / `RepositoryPriorite.page_resultats`.
Inspection en lecture seule de la cible TEST identifiée par `.env.test` : schéma
`public`, dernière migration v294, table absente ; seules v295–v298 en attente.
Le code livré attendait un schéma plus récent. Aucune modification du calcul
métier ni création manuelle isolée de la table n'est nécessaire.

Réparation effectuée sur TEST après sauvegarde complète PostgreSQL : archive
personnalisée de **64 127 415 octets**, empreinte SHA-256 enregistrée dans le
rapport privé, ACL conservées, inventaire et lecture/décompression complète
`pg_restore` réussis. Cette vérification ne constitue pas une restauration
effective de cette sauvegarde.

Le runner canonique `scripts/database/apply_migrations.py` a appliqué, dans
l'ordre, **v295_crm_actualisations.sql**, **v296_crm_priorite_commerciale.sql**,
**v297_crm_ordonnancement.sql** et **v298_crm_referentiels_qualification.sql**.
Les empreintes existantes ont été contrôlées ; aucune ancienne migration réécrite.

Vérification après correction, en lecture seule : **v298**, aucune migration
en attente, les **21 nouvelles tables** présentes, une génération par prospect
et la requête de recherche signalée réussie (**25 résultats**, page suivante
disponible). Les nombres de lignes de toutes les tables CRM préexistantes sont
inchangés. Aucun calcul, actualisation de source, envoi ou changement de droits
n'a été lancé. Le parcours navigateur authentifié n'a pas été rejoué.

Sauvegarde et rapports : répertoire privé backend
`demonstrations/prive/operations/correctif-crm-qualification-v298-20261106/`,
hors Git. Le runbook précise désormais que le refus de démarrage d'une base
incomplète dépend de `LOCALEO_SCHEMA_READINESS_ENFORCE` : activé par défaut en
production, mais à configurer explicitement sur TEST. Aucun paramètre Render
n'a été modifié lors de cette réparation.

## Correctif Rappels — filtre par journée avec calendrier, 6 novembre 2026

Ajout local d'un filtre facultatif **Date de l’action**. La saisie `date_action`
est validée par l'API (routes `/taches` et `/rappels`) et transmise au stockage ;
la journée Paris est filtrée avant les totaux et la pagination. La borne basse
est incluse, celle du lendemain exclue : aucun décalage lié au fuseau du navigateur
ou à une durée fixe de 24 heures. La colonne `due_at` n'est pas enveloppée dans
une fonction SQL ; le filtre peut réutiliser l'index des échéances ouvertes.
Ce filtre de lecture ne change aucune règle de programmation ou notification.

Preuves : les huit cas de contrat nouveaux échouent avant correction (paramètre
ignoré et dates invalides acceptées), puis la suite API complète passe :
**33 réussites**. Les **3 tests PostgreSQL** vérifient un jour d'hiver, les
journées de 23/25 heures, les deux bornes, la distinction action/rappel, le total
et deux pages, les filtres combinés et le refus d'un curseur d'une autre date.
`crm-correctifs.cjs` réussit : calendrier, date facultative, combinaison,
conservation après actualisation, retrait du filtre, PC/mobile 320/1280 et
captures inspectées. OpenAPI et guide utilisateur sont adaptés.
Les contrôles d'architecture, inventaire domaine et couverture des use cases
passent également : **671 réussites**, sans exclusion.

Pas de migration : les instants et index existants sont conservés. Aucun effet
sur les batchs, autorisations, données générées ou les autres applications ;
seule la PWA CRM consomme ce filtre optionnel, les anciens clients restent
compatibles. Vérification locale, aucun déploiement ou accès à TEST partagé.

## Correctif Rappels — liste facultative des responsables, 6 novembre 2026

Sur la base backend `acd386e` et documentation `4ba60dd`, correction locale du
filtre Responsable : le composant ajoutait une saisie et un bouton de recherche
en plus de la liste. Rappels conserve désormais la seule liste facultative,
avec **Tous les responsables** pour ne pas filtrer. Les pages suivantes restent
accessibles et complètent la liste sans retirer ses choix ni perdre la sélection.
Les formulaires d'affectation conservent leur recherche habituelle.

Preuve : `tests/browser/crm-correctifs.cjs` échoue avant correction sur la présence
du champ de recherche, puis réussit après correction. Vérifications : choix et
retrait du filtre, conservation après actualisation, chargement d'une page
suivante sans doublon, sélection conservée, clavier natif et absence de
débordement à 320 et 1280 px ; captures inspectées. Aucun changement d'API, règle
métier, droit, migration, générateur de démonstration ou configuration requis :
la correction concerne uniquement la présentation des filtres PWA.

## Bilan actuel — implémentation locale, 6 novembre 2026

**Les évolutions 05/06/07 sont raccordées du domaine jusqu'à la PWA. L'epic
reste en cours : les contrôles de capacité ne sont pas tous validés.** Ce bilan
remplace l'état du premier incrément conservé plus bas à titre historique.
Seuls `localeo-backend` et `localeo-projet` sont modifiés. Aucun commit, push,
déploiement ou accès aux données du TEST partagé n'est réalisé dans cette phase.

| Périmètre | Comportement implémenté et preuves | Limites d'activation / validation |
| --- | --- | --- |
| EVOL-05, CA-41–49 | Demande des six blocs, travail asynchrone avec baux/checkpoints/quotas, instantané de comparaison, sélection explicite et adoption atomique ; protections et versions revérifiées, valeurs absentes non destructrices, évaluations en BROUILLON. API authentifiée et PWA PC/mobile ; sources simulées et PostgreSQL réel jetable | Préparer les référentiels serveur selon le [guide dédié](referentiels-qualification.md). Les fichiers normalisés de population/compétences nécessitent une préparation opérateur. Aucun fournisseur réel ni donnée CRM réelle utilisé pour les tests |
| EVOL-06, CA-50–59 | Menu Qualification, capture exacte de la recherche sur toutes ses pages, lots arrêtables/reprenables, priorité au potentiel et validité par axe, liste/carte filtrables et explication du résultat, attestations explicites. Seuils acceptés : commune 5/10, EPCI 20/50 ; projet/contact facultatifs | Déploiement et activation non réalisés. Mesures ciblées N/10N réussies ; charge mixte complète et volumes maximaux non validés |
| EVOL-07, CA-60/61 | Action prévue le / Me rappeler le, calendrier et aides, erreur explicite et focus, report obligatoire prérempli, règles Paris/UTC et DST conservées | Vérifié localement ; pas de migration métier supplémentaire |
| Exploitation partagée | Batchs de préparation des référentiels, actualisation et qualification ; concurrence globale 2 traitements lourds, quotas réseau, renouvellement et fencing des baux, réautorisation avant acquisition/publication | Flags désactivés par défaut. Appliquer v295 à v298 avant activation ; v297 est aussi nécessaire au wrapper d'import existant |

Preuves exécutées (groupes pouvant se recouvrir, **ne pas additionner** leurs
effectifs comme un total de tests distincts) :

- Rejeu final des contrôles d'architecture, inventaire des classes domaine et
  couverture des use cases : **671 réussites** sans exclusion.

- **849 réussites** : architecture, classes domaine, couverture des use cases,
  domaines/services/worker et intégration PostgreSQL des fournisseurs/adoptions.
  Puis **22 réussites ciblées** après durcissement final des références figées
  et de la publication idempotente des fichiers.
- **40 réussites** : domaine/application/API/PostgreSQL de priorité, dont les
  attestations et l'invalidation ciblée lors d'une évolution territoriale.
  Après le dernier correctif d'attribution, **37 réussites ciblées** prouvent
  notamment qu'un recalcul ne réhabilite pas un ancien comptage, puis qu'une
  nouvelle adoption explicite permet de rétablir la priorité.
- **17 réussites** : worker et autorité interne ; sessions réelles valides,
  révoquées et versions d'habilitation changées, avant et après collecte.
- **17 réussites** : frontière PWA, routes privées et retour exact après
  connexion. Un test a détecté que le middleware perdait les paramètres de
  suivi du traitement ; corrigé puis rejoué avec succès. Les deux tests HTTP
  d'actualisation et les tests batchs sont également réussis.
- **19 réussites** : stockage, quotas de création et ordonnanceur PostgreSQL ;
  **64 réussites** : readiness, endpoints batchs et ordonnanceur applicatif.
- **2 mesures PostgreSQL réussies** pour les lectures de priorité à 1 000 puis
  10 000 organisations (3 000 puis 30 000 dossiers), captures exactes et au plus
  deux requêtes SQL par page. Ces mesures ne prouvent pas la charge mixte.
- **24 réussites** pour le générateur et la restauration, dont un véritable
  `pg_dump` / `pg_restore` du graphe synthétique v295–v298 et son transfert
  neutralisé. Snapshots, décisions, résultats, attributions et identités
  d'attestations sont conservés ; anciens baux refusés. La comparaison des
  instants est réalisée dans des sessions explicitement UTC.
- Navigateurs : `crm-actualisations.cjs`, `crm-priorite.cjs`, `crm.cjs`,
  `crm-qualification.cjs`, `crm-rappels.cjs` et `crm-correctifs.cjs` réussis.
  API simulées ; PC 1280 et mobile 320, captures inspectées, protection d'un
  champ volontairement vide, même clé après réponse incertaine, lecture seule,
  désactivation/archive, reprise du polling après coupure et attestations.

La revue indépendante a notamment corrigé la réautorisation des sessions
internes, le maintien des versions de référentiels lors d'une reprise, la
distinction entre résultat disponible et complet, les attestations d'absence
connue et les retours de connexion vers les nouveaux écrans. Les règles restent
dans le domaine ; les API et la PWA n'introduisent pas de barème concurrent.

Réserves explicites :

- Le test d'import de 10 000 lignes a dépassé deux fois son budget de 120 s,
  à 7 346 puis 4 375 groupes. Il reste un **échec**, sans assertion affaiblie ni
  skip ajouté. Ce test n'active ni les nouveaux triggers de priorité ni les
  nouveaux verrous d'ordonnancement ; l'origine du dépassement est examinée
  séparément et n'est pas qualifiée de dette préexistante sans preuve.
  Le profil court localise le coût dans les cinq requêtes par groupe du chemin
  d'import : lecture/verrouillage des faits et création/finalisation dominent,
  sans défaut d'index démontré. La suppression d'une double lecture peut être
  étudiée, mais ne prouve pas le respect du budget complet.
- Pas de validation de la charge mixte 20 lecteurs / 2 écritures, ni de la
  capacité maximale des référentiels régionaux et de l'actualisation en masse.
- Pas de collecte externe réelle ni d'application des migrations sur TEST.
  La politique de conservation des données réelles reste un prérequis
  d'activation explicité dans l'exploitation ; elle ne remplace aucun test.

Les contrats OpenAPI documentaires, guides fonctionnels et exploitation,
exports et readiness sont adaptés. Les trois autres dépôts applicatifs ne
consomment pas ces nouvelles routes CRM privées : sans impact de contrat sur
Pro, Animation et Marketplace.

Le registre du générateur classe les 21 nouvelles tables CRM. Un nouveau jeu
synthétique ne déclenche ni collecte ni envoi : il crée quatre slots libres.
Lors d'un rechargement, les autorités et traitements actifs sont neutralisés,
les slots libérés avec nouveaux jetons et les générations/attributions rétablies
après les triggers. Les identités d'attestations et leur séquence sont conservées.
Ces tests locaux ne constituent pas une restauration d'exploitation sur TEST.

Contrôles documentaires : **72 chemins / 100 schémas OpenAPI** exportés,
**148 sources** vérifiées ; **96 guides / 1 112 liens** et contrôle des documents
modifiés sans erreur. Les vérifications de whitespace Git sont réussies.

## Historique — premier incrément local, 6 novembre 2026

**Epic toujours en cours. La livraison complète des évolutions 05/06 n’est pas
réalisée.** Dépôts modifiés : backend (PWA et domaine/test) et projet (sources
canoniques). Aucun contrat consommé par Pro/Animation/Marketplace modifié.

| Périmètre | Résultat réel | Limite |
| --- | --- | --- |
| EVOL-07, CA-60/61 | Libellés Action prévue le / Me rappeler le sur formulaires, détail et listes ; aides accessibles, calendrier conservé, report prérempli obligatoire, erreur/focus et saisie conservée | Local uniquement, aucun déploiement ; mêmes routes, champs et règles, aucune migration |
| EVOL-05, fondations de CA-41/43/45/48 | Nouveau domaine pur `actualisation.py` : demandes, instantanés immuables, décisions de sélection, versions/protections et données absentes non destructrices | Aucun consommateur API/worker ; ADOPTEE autorise une sélection, ne prouve aucune écriture CRM. Les neuf critères ne sont pas validés dans leur ensemble |
| EVOL-06, CA-50–59 | Spécification révisée conservée | Aucun calcul ni menu livré ; seuils et méthode attendent les réponses produit |

Preuves exécutées sur cet incrément :

- `scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/domain/prospection/test_actualisation_dedicated.py -q -s` : **754 réussites**, dont **93 scénarios d’actualisation**. Le premier passage a révélé un inventaire de classes à corriger et une erreur Windows de lancement Git sous capture pytest ; inventaire corrigé et rejeu sans capture réussi, sans exclusion ni assertion affaiblie.
- `tests/application/test_crm_dates_actions.py` : **8 réussites**, vraie orchestration sur doubles de stockage ; création omise/avant/égale/après, report omis refusé, révision invalidée et responsable conservé.
- `tests/domain/prospection/test_rappels_dedicated.py` et `tests/api/test_crm_filtre_type_action.py` : **59 réussites** dans le premier groupe. Les quatre tests de `test_crm_rappels_api.py` initialement ignorés faute de PostgreSQL ont ensuite été exécutés sur base locale jetable : groupe avec `test_core_dedicated.py`, **32 réussites, aucun skip**.
- `tests/browser/crm-rappels.cjs` et `crm-correctifs.cjs` : réussis. API simulée ; calendrier clavier/mobile 320/1280, aides, erreurs, fuseau Paris depuis navigateur New York, heures DST invalides/ambiguës, conflit et rejeu de même clé. Capture mobile inspectée.
- Revue indépendante : hydratation terminale et contacts absents durcis puis retestés ; aucun constat résiduel confirmé dans cet incrément. Cette revue ne valide pas les contrats d’une API d’actualisation qui n’existe pas encore.

La base locale jetable a été arrêtée après les tests, comme à l’état initial.
Aucun accès à TEST partagé, fournisseur ou messagerie réelle. Le générateur de
démonstration, l’OpenAPI et les migrations ne changent pas : aucune route/donnée
persistée nouvelle exposée par cet incrément. Leur adaptation reste requise pour
la suite des évolutions 05/06.

Restant explicitement à développer : persistance, commandes atomiques d’adoption,
API/DTO, orchestration/réautorisation, baux et quotas partagés, adaptateurs et
référentiels des six blocs, menu de calcul et classement/carte, invalidations
par axe, interface de comparaison, migrations et tests de capacité/restauration.
Les seuils commune 5/10 et EPCI 20/50 et la base « établissements actifs de
proximité, six familles, SIRET unique » ont été confirmés pendant l’implémentation. Le
périmètre complet de première livraison reste les six blocs, sans report implicite.

## Conception V1.3 — preuves à produire, 6 novembre 2026

État à la fin de la phase de spécification : E71-EVOL-05/06/07 étaient spécifiées,
sans implémentation ni tests fonctionnels nouveaux. L’incrément local ci-dessous
actualise ce constat pour EVOL-07 et le domaine préparatoire EVOL-05. Les preuves historiques ci-dessous portent sur le socle et
E71-EVOL-04. Les critères restent au nombre de 61, dont CA-24 reporté.

| Critères | Preuves nouvelles prévues | Dépendances et effets à vérifier |
| --- | --- | --- |
| CA-41–49 | Matrice détaillée dans [Actualisation](actualisation-qualification.md) : D/A comparaison et adoption explicites, SQL concurrence/idempotence, API droits et échecs fournisseurs, UI aperçu partiel et erreurs | Sources simulées, identité exacte, aucune mutation avant adoption, conservation des corrections humaines ; six blocs requis dès la première livraison, qualification des méthodes/adaptateurs et conservation avant données réelles |
| CA-50–59 | Matrice détaillée dans [Qualification commerciale](niveau-qualification.md) : D priorité au potentiel/inconnus/absence de projet, SQL capture/reprise/invalidation, API carte/liste, UI compréhension des axes et niveaux | Profils versionnés, aucune action commerciale automatique ; ancien barème à revoir, seuils et profils à arbitrer, métriques N/10N et tests mixtes |
| CA-60–61 | UI création/édition/report/détail/Aujourd’hui/Rappels en PC et mobile, clavier et lecteur d’écran ; API/D UTC/Paris, DST, rappel absent à la création, effacement au report refusé, rappel après action refusé | [Contrat de saisie](parcours-regles.md#e71-evol-07--dates-des-actions-plus-explicites) ; conserver le calendrier et les règles actuelles, aucune migration ni nouveau canal |
| CA-07/13/35, régression | Même filtre en liste/carte/capture, plusieurs contacts/dossiers sans produit cartésien, total et pages, recherche par département, responsable prospect distinct du responsable de tâche | [Catalogue de filtres](parcours-regles.md#recherche-partagée--ca-0713355054) ; les nouveaux niveaux ne remplacent ni le classement du potentiel ni la priorité manuelle |

Jeu synthétique à étendre dans le générateur backend : commune et EPCI,
organisation non éligible au profil, contact devenu périmé, plusieurs dossiers,
source indisponible, résultat partiel, conflit après aperçu, opposition et
compte révoqué pendant un job. Tester reprise après crash et restauration sur
base jetable, sans fournisseur réel ni campagne commerciale. Mettre à jour le
guide utilisateur et l’exploitation lors de l’implémentation ; la documentation
actuelle ne doit pas annoncer ces boutons comme disponibles.

Les conditions de clôture restent des **tests unitaires, d’intégration,
fonctionnels et de capacité**. Un pilote commercial ou une validation externe
ne sont pas exigés. Une décision de barème/source/conservation non prise reste
une limite de conception ou d’activation, pas un test prétendument réussi.

### Arbitrages utilisateur reçus après la première revue, 6 novembre

- Actualisation : tous les blocs dès la première livraison. Ajouter au scénario
  CA-41/49 un succès applicable pour chacun des six blocs et une demande globale,
  plus une indisponibilité ponctuelle ; distinguer panne de source et fonction
  non développée. Les comptages et compétences ne sont plus un lot ultérieur.
- Classement : fort potentiel même sans projet engagé. L’ancien 40/35/25 et
  les barrières de couverture globale/contact ne sont pas des valeurs acceptées.
  CA-52/53 doit prouver qu’absence de dossier/budget/contact ne suffit pas à
  déclasser un potentiel démontré, tout en affichant les informations manquantes.
  Tester aussi fermeture du dernier dossier et expiration du contact : priorité
  conservée si le potentiel reste courant, seuls les axes secondaires devenus
  obsolètes perdent leur rôle de départage. Les seuils par profil restent à finaliser.

La revue ciblée après ces réponses a fait corriger la condition d’activation
des six blocs et la validité distincte des trois axes. Après relecture, aucun
défaut de contrat bloquant restant constaté. Les 10 documents / 221 liens et
147 sources ont été revérifiés sans erreur ; aucun test métier nouveau exécuté.

### Contrôles exécutés sur la spécification V1.3

Le 6 novembre 2026 : revue indépendante des contrats et comparaison aux
producteurs backend. Trois ambiguïtés corrigées : cible dossier des attestations,
empreinte de couverture réservée aux projets et enveloppe de concurrence commune
incluant les imports et la capture. Aucun défaut de contrat bloquant restant
constaté par cette revue statique ; les arbitrages produit explicités restent
ouverts.

Contrôles documentaires : `check_guidance.py --all-markdown --changed` a vérifié
**10 documents et 221 liens locaux, sans erreur ni avertissement** ;
`sync_documentation.py --check-sources` a vérifié **147 sources** ;
`git diff --check` est réussi. Seul `localeo-projet` est modifié. Aucun nouveau
test métier, appel fournisseur, générateur OpenAPI, migration ou déploiement
n’a été exécuté pour cette phase de spécification.

## Matrice de traçabilité

D = domaine pur ; A = application/UoW ; SQL = PostgreSQL jetable ; API = droits/contrats ; UI = navigateur. La matrice décrit les preuves attendues ; les résultats exécutés et leurs limites figurent dans le bilan d’implémentation en fin de document.

| Critères | Propriétaire et scénario de preuve | Documentation / contrat | Fixtures et exploitation |
| --- | --- | --- | --- |
| CA-01/02 | Organisation/dossier : D/A/API minimum, deux contacts/deux périmètres, deux campagnes, zéro conversion/envoi | Parcours fiche et contrat prospects/dossiers | Structure synthétique multi-périmètre, migration additive |
| CA-03 | Opportunité : D matrice des six étapes, pause/réexamen, perte/réouverture, preuve absente/invalide/valide pour chaque objectif ; deux dossiers/une preuve en SQL concurrent, annulation métier concurrente, rejeu et réouverture sans double comptage | Transitions, règles de gain et ARB-04b | OnBoard accepté, souscription active/gratuite, commande payée ; aucun paiement créé |
| CA-04 | Événement : D/A note/correction, dates distinctes, double clic et ajouts concurrents, XSS texte échappé | Chronologie, erreurs de formulaire | Notes synthétiques, logs sans contenu et purge selon politique |
| CA-05/06 | Tâche/rappel : D/A/API cycle, échéance Paris/UTC/DST, projection prochaine action ; terminer/report/réaffecter avant envoi | Aujourd'hui, Rappels et commandes | Tâches retard/jour/futur, horloge contrôlée, aucun fournisseur réel |
| CA-07/22 | Projections : API/UI filtres communs liste/suivi/carte, comptages distincts et datés, pagination SQL, zéro résultat/erreur | Recherche, indicateurs et carte | N/10N, mêmes filtres, une structure plusieurs dossiers |
| CA-08/09 | Lot : parser/A CSV UTF-8 BOM/sans BOM, guillemets/retours ligne, colonnes manquantes/dupliquées/inconnues, rejet XLSX, limites, groupe contradictoire atomique | Dictionnaire CSV et aperçu | Fixtures synthétiques ; formule non évaluée, exports neutralisés, zéro écrit avant confirmation |
| CA-10/11 | Identité/import : SQL mêmes clés, réordre, nom changé, homonymes, contact répété, lot concurrent et source différente, namespace avec espaces/casse normalisé et création de source explicite ; panne après commit/reprise ; deux créations sources A/B ou manuel/import avec barrières SQL, candidat apparu après décision de distinction, erreur de sérialisation sans création automatique | Clés stables et plan immuable | Aucune duplication, bail expiré et jeton ancien refusé, marqueur d'effacement manuel protégé |
| CA-12 | Lot : API sources/décisions/confirmation versionnée/arrêt/reprise, rapport interdit après révocation ; acteur de reprise, exclusions, INIT sans effet, états terminaux et bilan par groupe fidèle | Imports et runbook | Stockage privé, fichier abandonné/purge, enrichissement post-import préservé |
| CA-13/14/15 | Localisation/carte : INSEE obligatoire de Nouvelle-Aquitaine pour création/changement de localisation, refus hors région, conservation des anciennes fiches, homonymes et hors catalogue ; points agrégés, dépassement de 500 sans curseur, clic groupe et pagination 25/100 ; mobile/clavier/panne fournisseur | Carte interactive, saisie régionale et fallback liste | Douze départements, ancien hors région/sans commune ; aucun contact/note transmis au fournisseur, aucune ville commerciale créée |
| CA-16/17/18 | Rattachement : A/API droits métier, cible de mauvais prospect, répétition, reprise après création externe ; gain conforme | Liens OnBoard/Animation/Achats | Aucun accès/checkout/paiement provoqué par import ou statut |
| CA-19/29 | Identité : D/API/UI toutes combinaisons de rôles/droits, absence de grant implicite, lecture liste/fiche/dossier autorisée et mutations refusées au lecteur, cardinalité des rôles éligibles sans élargissement historique, DTO/menus/registre fermés, CSRF, accès direct, session expirée ; révocation pendant commande/lot/rejeu | ERP profils, contrat droits et PWA | Comptes synthétiques sans droit/lecture/gestion/import/admin, pas d'élargissement SQLAdmin |
| CA-20/21 | Opposition/version : D/SQL course planification-opposition, fermeture pendant batch, réimport/réactivation, contact ciblé vs autre contact, coordonnée opposée réutilisée comme structure, tâche structure sans contact ciblé, correction concurrente et idempotence corps divergent | Politique commune et 409/422 | Aucun rappel sollicitant après opposition avant remise transport, versions et histoire conservées |
| CA-23 | UI parcours documenté : installation → import → fiche/carte → note → rappel → rattachement | Guide CRM, modèle CSV et aide contextuelle | Scénarios automatisés synthétiques ; aucun compte rendu de pilote requis pour clôture |
| CA-24 | **Reporté** : ancien import Gironde/sections communales | Historique E71-EVOL-02, hors V1 actuelle | Pas de fixture Gironde obligatoire pour valider le nouveau CSV |
| CA-25 | PWA/UI manifest/scope/start_url, navigation profonde, retour après auth, offline, mise à jour réelle seulement ; inspection caches et changement de compte | Installation, confidentialité et cycle PWA commun | 360/390/1280 px, clavier, ServiceWorker sans données privées |
| CA-26 | Push : A/API/UI opt-in/refus/unsupported, ownership abonnement, 404/410, panne/réessai/issue incertaine, clic hors session ; report et droits retirés | Préférences, intention/délivrance et états transport | Transport simulé, multi-appareils, aucune fuite de contact sur écran verrouillé |
| CA-27 | Email : D/A outbox éligible, préférence off/on, responsable différent, tâche annulée après enqueue, révocation avant revendication ; aucune régression des autres emails | Charte, garde d'expédition, runbook | Fournisseur simulé, destinataire interne vérifié uniquement, adresse absente/non vérifiée refusée ; preuve E69 liée à email_version, reprise depuis invitation consommée seulement, changement d’adresse entre opt-in/enqueue/envoi, réactivation volontaire et non-régression E69 ; pas de rattrapage massif |
| CA-28 | Import : INIT sur existant ignore tout ; UPSERT complète vide non protégé/ajoute contact/dossier ; notes/statut/rappels/opposition inchangés, absents conservés | Mode et règles par champ | Exemple P0001/P0002, téléphone A→B puis source C garde B ; contexte initial unique |

Compléter les cas performance de l'[architecture](architecture-contrats.md) : pages 25/100 et profondes, lignes SQL réellement lues, mémoire, N/10N, trafic mixte et saturation, import et worker concurrents. Une bonne pagination UI ne prouve pas la pagination SQL.

## Tests et clôture

### E71-EVOL-04 — preuves et résultats

Extension de spécification du **4 novembre 2026**,
[règles et contrats](qualification-structuree.md). Les résultats historiques
ci-dessous ne couvrent pas ces champs nouveaux. Les onze critères ajoutés sont
implémentés localement ; les scénarios fonctionnels, intégration et capacité exécutés sont détaillés dans le bilan E71-EVOL-04 ci-dessous. Les réserves du socle restent conservées.

| Critère | Comportement / propriétaire | Preuves prévues | Documentation / contrat | Fixtures / démonstration | Exploitation / migration |
| --- | --- | --- | --- | --- | --- |
| CA-30 | Organisation : nature/activité/accueil | Domaine et API : sous-type incompatible, champ inconnu, absence, preuve manquante ; navigateur sections conditionnelles | Dictionnaire et projections organisation | Commune, EPCI, commerce, historique sans qualification | Colonnes facultatives ; pas de faux CONFIRME au backfill |
| CA-31 | Valeurs d’identité et ressemblance | Domaine/SQL : formats, préfixe SIREN/SIRET, identifiant contradictoire ; deux établissements d’un SIREN, concurrence multi-source, recherche exacte | Identité et rapprochement, API candidats | Même SIREN/deux SIRET, communes homonymes | Index non unique SIREN établissements, aucun objet ERP créé |
| CA-32 | Évaluation/classification | Domaine : seuils 0/4/5/9/10, absent, population/millésime, somme familles, cas incertains exclus ; SQL sélection de référence | Évaluation privée, filtres et règle SEUILS_ANIMATION_1 | DOCUMENTAIRE et NON_EVALUE, commune/EPCI | Projection courante cohérente avec la référence |
| CA-33 | Contrôle terrain et histoire | Domaine/API/SQL : triplet incomplet, zéro vérifié, dates futures, correction sans écrasement, deux sources, choix manuel ; navigateur comparaison et confirmation | États brouillon/confirmé, historique paginé | Révision corrigée, import source plus récent sans remplacement | Rétention/purge/restauration versions et preuves |
| CA-34 | Contact et fiabilité | Domaine/application : personne/service/accueil, date/preuve absentes, coordonnées modifiées, rôle général sans portage implicite ; API accès tiers | ContactPatch et résumé, règles de vérification | Accueil générique et porteur confirmé | Aucune preuve d’identité interne ou opt-in fabriqué |
| CA-35 | Projet Animation | Domaine/API : contact d’un tiers/obsolète, besoin sans résumé, budget inconnu/zéro/confirmé/ABSENT, HT/TTC et dates inversées ; F plusieurs projets | Sous-ressource dossier, protection UPSERT | Deux dossiers du même prospect, un Coffrets | Aucun paiement/gain/rappel ; versions/audit |
| CA-36 | Relations territoriales/compétences | Domaine/SQL/API : rattachement courant unique, remplacement daté, siège différent de membres, EPCI hors région référencé sans prospect, couverture par lots, nuance compétence | Appartenance, couverture, sources de compétences | EPCI multi-départements, membre historique, sources Sirene/BANATIC datées différemment | FK/index/purge ; aucun déplacement du point carte |
| CA-37 | Import format 2 | Parseur/plan/PostgreSQL : 85 colonnes connues et sous-ensembles, format 1 à 21 colonnes, dépendances, même evaluation_ref changé, reprises et protections ; F aperçu/choix de référence/bilan | Nouveau modèle 2 + contrat1 conservé | INIT/UPSERT nouveau/existant/opposé/archivé, contacts multiples | Un groupe atomique, ancien plan immuable et format explicite |
| CA-38 | Lectures et UX | SQL N/10N, filtres EXISTS même dossier/contact, pas de doublons/N+1 ; F 320/390/1280 px, clavier, erreurs/vide, filtres URL et carte cohérents | Projections et listes paginées | Plusieurs enfants concordants/non concordants | Budgets SQL/p95/p99/mémoire et confidentialité des tuiles |
| CA-39 | Orchestration/version/droits | Deux connexions : confirmation/référence/import concurrents ; protection modifiée après aperçu ; même clé corps différent ; droits révoqués ; aucun effet partiel | Erreurs 409/422, commandes et reçus privés | Lecture/gestion/import/admin séparés, notes ajoutées en parallèle | Verrous bornés, aucune requête externe dans transaction |
| CA-40 | Compatibilité et migration | Migration avant/après sur base jetable, contraintes/index, restauration et génération/rejeu, anciens payloads/pages ; OpenAPI/guides | Contrat généré et lecteurs CRM, limites de format | Scénario entièrement synthétique | Readiness, activation progressive et reprise documentée ; aucun rollback destructeur |

Suites à prolonger : `tests/domain/prospection/`,
`tests/integration/prospection/test_import_csv.py`, `test_imports_postgres.py`,
tests HTTP imports, `tests/security/test_crm_core_postgres.py` et recette
navigateur CRM. Ajouter des tests dédiés des nouvelles valeurs/agrégats sans
ORM, puis orchestration et PostgreSQL isolé ; appliquer les contrôles d’architecture
du backend. Aucun test ne réutilise les coordonnées réelles du classeur.

Revue indépendante `localeo-contract-reviewer` du 4 novembre : réalisée puis
corrections relues ; références séparées par clé territoriale/projet/bloc,
invalidation effective du portage lié au contact, confirmation sans comptage
pour population/compétences et matrice de portées intégrées. Aucun blocage résiduel
relevé dans la relecture ciblée. Gabarit 2 vérifié à 85 colonnes, préfixe des 21
colonnes du format 1 conservé.

Cas supplémentaires obligatoires CA-32/33/35/36/37/38/39 : deux couvertures de
projet d’un même prospect avec références distinctes ; couverture modifiée et
ancienne observation signalée obsolète ; population et compétences confirmables
sans comptage avec sources distinctes ; nouveau relevé BANATIC sans remplacement
du comptage retenu ; porteur confirmé devenu A_REVALIDER après changement ou
obsolescence du contact et exclu immédiatement du filtre CONFIRME.

Contrôles du 4 novembre exécutés sur l’arbre documentaire courant :

- `python scripts/check_guidance.py` : 96 guides, 1 099 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 12 documents, 213 liens, zéro erreur/avertissement (inclut les travaux E75 préservés).
- `python scripts/sync_documentation.py --check-sources` : 137 sources vérifiées.
- `git diff --check` : réussi.
- Lecture CSV standard : 85 en-têtes uniques, préfixe des 21 colonnes du format 1 identique, aucune ligne réelle ; chaque colonne nouvelle décrite dans le dictionnaire. CA-01 à 40 sans trou/doublon, CA-24 toujours reporté, 39 actifs.

Ces contrôles statiques ne prouvent pas un import applicatif ou une règle métier.
Implémentation, migration, import de données réelles, commit, push et déploiement
ne sont pas effectués par la présente demande de spécification.

### Conditions de clôture conservées et étendues

Suites cibles : `tests/domain/prospection/`, `tests/application/prospection/`, API, PostgreSQL jetable, parcours navigateur CRM et tests transport simulé. Utiliser le [runner isolé backend](../../../../localeo-backend/scripts/validation/test_isolated.py) et les contrôles d'architecture locaux. Aucun accès à TEST partagé, aucune notification réelle implicitement incluse dans les tests.

Pour la clôture : **tests unitaires, intégration et fonctionnels de tous les critères actifs**, avec migrations/restauration synthétique, droits, fournisseurs simulés, PWA, import/reprise et capacité. Aucun pilote commercial, contact de prospect, validation municipale ou compte rendu UX externe ne constitue un critère de clôture. Des tests prévus ou ignorés ne valent jamais réussite. Le critère reporté reste visible comme hors V1 ; l’E71 reste En cours tant que tous les critères actifs ne sont pas vérifiés.

Les conditions d'activation réelle restent distinctes : configuration des transports, politique de conservation, hébergement et attribution des droits. Une campagne de test locale ne prouve pas un envoi au fournisseur ou une livraison réelle sur tous les navigateurs.

## Conservation et audit : décision restante ARB-07

Aucune durée CRM n'a été établie dans cette tâche. Ne pas importer par analogie les durées de conservation des achats/PIN. Avant données réelles, rattacher à la politique Localeo : prospects/contacts, notes/tâches, oppositions/preuves, fichiers/staging/rapports, clés de rapprochement/protections, idempotence, abonnements/intention/délivrance.

Prévoir déclencheurs et durées par catégorie, stockage SQL/objets/caches/sauvegardes, suppression/anonymisation cohérente et preuve de dry-run. Une lecture interne ne prolonge pas automatiquement la conservation. La purge des clés de source doit empêcher une réimportation silencieuse d'une personne opposée : référence minimale ou mise en quarantaine à requalifier selon la politique retenue, pas recréation aveugle.

Logs techniques : IDs, codes, versions, comptages, durée et corrélation uniquement. Aucun nom de personne, e-mail, téléphone, note, valeur de cellule, URL d'abonnement push ou lien signé. Rapports/fichiers privés à accès contrôlé, aucune copie en Git ou fixture réelle. Le modèle CSV versionné contient seulement ses en-têtes.

## Documentation, démonstration et impacts prévus à la spécification

Le bilan d’implémentation plus bas précise les éléments désormais livrés et testés.

- Backend : domaine/API/migrations/worker, CRM et droits ERP, générateur et tests. Enregistrer domaine/tags/contrats à l'implémentation ; pas de fausse route publiée ici.
- Guides canoniques à livrer : prise en main CRM, import/reprise, configuration des droits et rappels, règles de gain/opposition/carte. Ajouter leur export à `documentation.exports.json` quand consommés et tester l'accès du lecteur. La présente conception n'est pas le manuel d'un écran disponible.
- Générateur backend : prospects synthétiques deux périmètres, contacts/homonymes, commune dense/non localisée/hors catalogue/Outre-mer, opposition, tâches, gains et import interrompu. Transports neutralisés. Étendre registre de tables, nettoyage, sauvegarde/restauration pour les nouvelles dépendances.
- Pro/Animation/Marketplace : pas de mutation des données ou nouvelles API publiques ; contrôler les liens consommateurs si leurs destinations sont changées. Les comptes et parcours de vente existants restent propriétaires de leurs règles.
- Geo : fonds/attribution/couverture à configurer et à tester ; aucune donnée CRM transmise au fournisseur, cache communal indépendant des villes marchandes.

## Livraison et reprise prévues

1. Appliquer ARB-04b confirmé (une preuve/un dossier) et tester sur fixtures ; arrêter conservation et paramètres de fournisseurs avant activation réelle.
2. Livrer migration additive/readiness, catalogue/DTO des droits, preuve de vérification d’adresse E69 et backend, fonctionnalités désactivées. Aucune preuve d’adresse créée à partir du seul état ACTIF. Ne pas réserver un numéro SQL dans cette spécification.
3. Livrer PWA CRM, routes privées, manifest/SW, contrats et guides ; configurer stockage, workers bornés, carte et canaux.
4. Exécuter la matrice locale et CI, migration/restauration sur base jetable, tests E69 et non-régression email ; aucune autorisation CRM ajoutée en masse.
5. Après autorisation d'exploitation distincte : vérifier HTTPS/installation, attribution d'un profil de recette, aperçu CSV, notification interne et transports configurés. Les tests déjà effectués restent distingués des observations de cible.
6. En incident : désactiver commandes/imports et producteurs de rappels ; interrompre proprement les lots, préserver groupes validés et états de remise. Ne pas supprimer les tables ni retirer un ancien message déjà remis au fournisseur.

Runbooks à produire : fichier invalide/doublon, résultat inconnu après timeout, conflit tardif, mauvais rattachement, droits retirés pendant lot, tâche annulée pendant envoi, backlog de notifications, panne carte, purge et restauration. Mesures : durée/état des lots, groupes rejetés/protégés/conflits, âge des files, échec/expiration/issue incertaine transport, conflits de version, temps SQL/mémoire, jamais contenu personnel.

## Historique — phase de spécification

Sources backend et documentation examinées en lecture ; nouvelle spécification et gabarit documentaire écrits. Revue indépendante des contrats effectuée puis corrections vérifiées : cible des tâches/oppositions, droits de lecture des dossiers, projection cartographique distincte, namespace d'import et cardinalité des droits E69. Aucune contradiction résiduelle identifiée dans ces corrections.

Contrôles documentaires exécutés le **3 novembre 2026**, dans `localeo-projet`, sur la base `7e09409` avec les modifications E71 locales :

- `python scripts/check_guidance.py` : 95 guides, 1 077 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 11 documents, 305 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 134 sources vérifiées.
- Lecture CSV standard du gabarit : 21 en-têtes uniques, concordance exacte avec le dictionnaire ; exemple documentaire : 2 prospects, 2 contacts et 3 dossiers distincts. Contrôle des identifiants : CA-01 à CA-29 sans trou ; seul CA-24 reporté, 28 actifs.
- Les quatre dépôts applicatifs restent propres et inchangés par cette phase. Les travaux locaux étrangers à E71 sont préservés ; aucun commit/push demandé pour cette spécification.

Ces contrôles valident la documentation, pas un import applicatif. **Tests CRM, migrations, import réel, envoi fournisseur et déploiement : non exécutés**, aucun code CRM implémenté par cette demande.

### Reprise et finalisation V1.1 du 3 novembre 2026

Relecture à la demande utilisateur sur base documentaire `3cdbf32` et travaux E71
locaux conservés. L’utilisateur confirme **CSV standard seul** et **une preuve de
gain pour un seul dossier**. Carte interactive maintenue ; aucune question métier
ouverte ne bloque désormais les développements sur données synthétiques.

La revue des producteurs identifie deux lacunes corrigées dans la conception :

1. `UtilisateurInterne.modifier` incrémente `email_version` sans retirer ACTIF :
   l’état actif ne prouve pas la vérification de la nouvelle adresse. Le fait
   versionné est porté par Identité interne, repris uniquement depuis une
   invitation consommée correspondante ; préférence et remise transport le vérifient.
2. Les clés par source ne protègent pas deux créations ressemblantes simultanées de
   sources différentes. Le contrôle de candidats et la création partagent désormais
   une transaction SERIALIZABLE sur toutes les entrées concernées ; décision
   devenue obsolète = réexamen explicite, jamais fusion ou retry aveugle.

Les contrats d’import explicitent aussi sources, décisions d’aperçu, confirmation
et reprise, acteurs, résultats par groupe et états terminaux. Les critères CA-03,
10/11/12/22/27/28 portent les preuves correspondantes. Les tests applicatifs restent
**à produire lors de l’implémentation** ; aucun résultat de revue ne les remplace.

La politique de conservation, le choix/configuration du fond cartographique et
les paramètres de transport restent des conditions d’activation avec données
réelles. Ils ne sont ni des pilotes obligatoires ni des preuves produit acquises.

Contrôles de finalisation exécutés sur cette V1.1 :

- Revue indépendante des contrats après correction : les deux lacunes ci-dessus
  sont levées ; aucune contradiction bloquante identifiée dans les sections relues.
- `python scripts/check_guidance.py` : 95 guides, 1 077 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 11 documents,
  305 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 134 documents vérifiés.
- `git -c core.safecrlf=false diff --check` : réussi.
- Contrôle CSV avec la bibliothèque standard Python : 21 colonnes uniques en
  concordance avec le dictionnaire ; exemple de 2 prospects, 2 contacts et 3 dossiers.
  Les 29 identifiants sont présents sans trou ni doublon dans le backlog et la
  matrice ; 28 actifs, CA-24 reporté.
- Les quatre dépôts applicatifs sont propres et inchangés. Seul le dépôt
  documentaire est modifié pour E71 ; les autres travaux locaux sont préservés.

Ces résultats sont documentaires. Aucun test produit CRM, aucune migration,
aucun import réel ni déploiement n’ont été exécutés. Aucun commit ou push n’est
réalisé dans cette phase de spécification.


## Implémentation locale — 3–4 novembre 2026

État roadmap : **En cours**. Le périmètre fonctionnel est implémenté dans le
backend (PWA `/internal/crm/`, domaine/application/persistence, API, droits ERP,
imports et rappels). La documentation canonique porte le [guide utilisateur](guide-utilisateur.md),
l’[exploitation](exploitation.md), le [contrat extrait](openapi.json) et le modèle CSV.
Les trois frontends publics/professionnels ne consomment pas ces nouveaux contrats ;
ils restent inchangés. Aucun sixième dépôt n’est créé.

### Preuves exécutées

Dernier passage consolidé sur les fichiers figés : **888 tests réussis en
84,22 s**, couvrant domaine, intégration, sécurité, PWA et architecture. Deux tests
de capacité import sont désélectionnés car mesurés séparément (aucun skip assimilé
à un succès). Les 28 avertissements concernent l’adaptateur datetime SQLite
déprécié ; aucun échec dans cette suite. La migration-restauration finale v292, index compris,
est rejouée avec succès en **42,47 s**. Les deux parcours Chromium CRM et rappels
sont rejoués avec succès après les corrections d’import et de navigation.
Les **13 tests de limite HTTP** passent également : import CRM de 10 Mio,
enveloppe multipart bornée, corps fragmenté ou taille déclarée erronée,
limite générale des autres routes conservée.

Commande de la suite consolidée, depuis le backend avec le runner isolé et
l’URL explicite du PostgreSQL jetable :

```console
python scripts/validation/test_isolated.py --postgres-test-url <postgresql-jetable> tests/domain/prospection tests/domain/identite_acces/test_crm_identite.py tests/application/test_crm_identite_preuve.py tests/api/test_crm_rappels_api.py tests/security/test_crm_core_postgres.py tests/integration/test_crm_rappels_postgres.py tests/integration/prospection tests/security/test_crm_pwa.py tests/security/test_crm_nominatif_postgres.py tests/unit/test_demonstration_crm.py tests/application/exploitation/test_schema_readiness.py tests/security/test_pwa_lifecycle.py tests/security/test_request_body_limits.py tests/unit/test_crm_agregats.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -k "not import_10000_lignes_budget_postgres and not profil_dix_groupes" -q --tb=short -s
```


- Tests domaine, PostgreSQL jetable et HTTP : créations atomiques, contacts et
  dossiers distincts, six étapes, pertes/pauses/réouvertures, preuves canoniques,
  attribution exclusive concurrente, idempotence, versions, notes/corrections,
  oppositions et invalidation des rappels.
- Imports : parseur strict, staging sans effet portefeuille, INIT/UPSERT,
  protection des champs effacés, plan immuable, rapprochement explicite,
  concurrence entre sources, droit retiré/reprise, panne atomique et rapport.
- Identité/rappels : droits sans grant implicite, preuve d’adresse liée à la
  version d’invitation, relecture avant remise, réaffectation, préférence,
  expiration appareil, issue transport incertaine et absence de verrou métier
  pendant le réseau. Le batch générique ne remet pas les e-mails CRM.
- **36 tests PWA/HTTP** réussis : activation fermée, routes profondes, retour de
  connexion contrôlé, ressources neutres, cache privé interdit, guide canonique,
  cycle partagé de mise à jour et conservation des autres PWA.
- Navigateur Chromium : création prospect+dossier, note conservée après 409 et
  rejeu de même clé, pause Paris→UTC, sept vues à **1440/1280/768/390/360/320 px**, absence de
  débordement horizontal/double défilement, révocation en cours de saisie,
  accès lecteur, aucun stockage local de données privées. Captures examinées
  dans le répertoire privé `tmp/crm-qa/` du backend.
- Worker/notifications navigateur : payload hostile ignoré, destination CRM
  fermée, nettoyage limité aux caches CRM, opt-out malgré canal désactivé,
  CSRF/idempotence et effacement de l’écran après un refus d’accès.
- **Migration complète et restauration réelle** : base vide → baseline v147 →
  v292 (189 entrées de journal), rejeu sans migration, jeu synthétique CRM,
  archive `pg_dump` custom, `pg_restore --clean --single-transaction`,
  vérification des données et nouveau rejeu. Test PostgreSQL 18 réussi,
  aucun schéma simulé et aucune ancienne migration réécrite.
- Générateur : scénario synthétique deux périmètres, note, tâche interne et
  sollicitation bloquée via les services ordinaires ; registre de 20 tables
  CRM, contrôle de schéma et neutralisation des traitements à la restauration.

Suites concernées dans le backend : `tests/domain/prospection/`,
`tests/domain/identite_acces/test_crm_identite.py`,
`tests/application/test_crm_identite_preuve.py`,
`tests/security/test_crm_core_postgres.py`, `tests/security/test_crm_pwa.py`,
`tests/api/test_crm_rappels_api.py`, `tests/integration/prospection/`,
`tests/integration/test_crm_rappels_postgres.py`,
`tests/integration/test_crm_migration_restauration.py`,
`tests/unit/test_demonstration_crm.py`, `tests/browser/crm.cjs` et
`tests/browser/crm-rappels.cjs`.

Les transports sont simulés. La base utilisée est exclusivement
`localeo_audit_test`/`localeo_audit_migrations_test` sur le cluster local jetable,
via `scripts/validation/test_isolated.py --postgres-test-url …`.

### Revues indépendantes et corrections intégrées

Les revues croisées ont corrigé : distinction liée aux candidats et versions,
contrôle des droits métier sur les preuves, refus du gain Coffrets à partir d’un
OnBoard Animation seule, normalisation import partagée, file bornée et curseurs
liés à l’autorité, garde des comptes nominatifs, accès documentaire, préservation
de la saisie et de la clé après résultat incertain, opt-out et recherche des
responsables. La dernière revue UI corrige également la référence de rapprochement,
la limite HTTP dédiée au CSV 10 Mio (enveloppe bornée, autres routes inchangées),
l’affichage des anomalies/lignes CSV, la pagination des sources, les commandes
réservées au confirmateur et le lien direct après connexion. Un test de registre
fermé couvre toutes les routes CRM nominatives. La charge mixte fonctionnelle
importe 200 structures pendant 40 ajouts de notes rejoués et des lectures concurrentes :
aucune note perdue ni import doublé.

Aucune donnée privée ni permission réelle n’a été utilisée.

### Capacité mesurée localement

**Projections finales : 23 tests réussis en 219,01 s**, dont les deux régimes
10N, avec 100 % des requêtes servies. L’attente des files fait partie du temps
mesuré. Deux cartes et un tableau peuvent s’exécuter simultanément par processus ;
aucun résultat privé n’est mis en cache. Les seuils initiaux restent inchangés.

| Jeu final, dix lecteurs | Carte p95 / p99 | Tableau p95 / p99 | Résultat |
| --- | --- | --- | --- |
| 10N frais | 1 449,73 / 1 501,10 ms | 557,85 / 619,93 ms | Tous les budgets respectés |
| 10N entretenu par VACUUM | 1 920,56 / 1 924,12 ms | 575,14 / 637,87 ms | Tous les budgets respectés |
| Retour à dix après vingt, frais | 1 591,12 ms p95 | 735,95 ms p95 | Tous les budgets respectés, fenêtre 4,44 s |
| Retour à dix après vingt, entretenu | 1 640,47 ms p95 | 726,13 ms p95 | Tous les budgets respectés, fenêtre 4,54 s |

À vingt lecteurs, carte et tableau dépassent les budgets (jeu entretenu :
2 800,30 et 1 615,58 ms p95) ; les listes et recherches restent sous leurs budgets.
Le dimensionnement vérifié est donc dix lecteurs sur cette cible locale, pas un
SLA HTTP de production. La marge de la carte reste réduite sur le régime entretenu. Les rapports finaux
`final-files-separees-frais.json`, `final-files-separees-etabli.json` et les plans
`final-crm-plans-*.json` figurent dans `tmp/e71-mesures-20261104/` du backend ;
`sources-files-separees-finales.json` conserve les empreintes des sources testées.

Les mesures intermédiaires ci-dessous expliquent les corrections et restent
conservées ; elles ne remplacent pas le rejeu final.

Les seuils des tests n’ont pas été modifiés pour obtenir ces résultats. Les premières
mesures dépassaient les budgets carte/import ; les index, projections SQL et échanges
par groupe ont été optimisés en conservant droits, SERIALIZABLE, atomicité et fencing.

- Import 10 000 lignes / 10 000 structures : dépôt **0,957 s** (hors upload),
  aperçu **3,909 s**, durée totale **86,988 s**, mémoire additionnelle **12 Mio**.
  Seuils respectifs : 1 s, 120 s total et 128 Mio. Autorité de fixture pour cette
  mesure ; authentification et révocation réelles couvertes séparément. Boucle de
  service hors HTTP/cadence d’ordonnanceur : ce résultat ne valide pas un cron lent.
- Portefeuille 100 000 prospects, 300 000 dossiers, 600 000 tâches et 1 million
  d’événements : dix lecteurs, 100 requêtes mixtes en **3,12 s**. p95 par opération :
  liste25 **77,54 ms**, liste100 **85,37 ms**, recherche **129,50 ms**,
  carte **1 265,16 ms**, tableau **568,08 ms**. Budgets respectés lors de ce passage seulement.
  Ces mesures portent sur la persistance, pas sur un SLA HTTP ou un hébergement réel.

- Avant la correction finale des agrégats, une campagne sur un jeu **fraîchement chargé**, après ANALYZE mais
  avant VACUUM, constate à dix lecteurs **1 110,88 ms** p95 au tableau de bord
  (budget 1 000 ms : **échec**) et **1 921,22 ms** à la carte (budget respecté).
  À vingt lecteurs, saturation : p95 liste100 **3 104 ms**, carte **3 729 ms**,
  tableau **2 679 ms**. Les paliers 1/5 passent. Le premier résultat favorable
  ne remplace pas ce contre-exemple ; le test nominal garde son assertion.
- Croissance indépendante de l’historique : 10 000 prospects et 1 million
  d’événements, historique paginé sans doublon ; médianes liste25/100
  **2,01 / 3,89 ms**, recherche **13,24 ms**, carte **37,49 ms**, tableau **12,02 ms**.
  Les projections ne lisent pas le journal des notes.

Artefacts synthétiques locaux : `tmp/e71-mesures-20261104/` dans le backend
(N, historique seul et 10N frais avec les paliers). Non versionnés, ils contiennent
les distributions et plans ; les chiffres et limites durables sont consignés ici.

- Toujours avant la correction finale, mesure après **VACUUM explicite** : 1/5 lecteurs respectent les budgets,
  mais à dix lecteurs la carte atteint **2 404,12 ms** p95 / **3 153,41 ms** p99 et
  le tableau **1 928,83 ms** p95 / **2 313,26 ms** p99. **Échec nominal confirmé**.
  Vingt lecteurs saturent les cinq opérations mesurées. Au retour immédiat à dix
  (fenêtre 8,07 s), carte **3 108,72 ms** p95 et tableau **1 472,57 ms** p95 :
  retour à la normale non démontré. EXPLAIN tableau avant/après VACUUM :
  **159,84 → 125,81 ms** ; carte **635,61 → 470,95 ms**. Les scans des agrégats
  (100 000 organisations / 300 000 dossiers) restent coûteux sous concurrence.
  Les artefacts `10N-etabli-vacuum-paliers-et-retour.json`, `plans-frais.json` et
  `plans-vacuum.json` complètent le répertoire indiqué plus haut.

- **Rappels — avant optimisation des préférences, cadence d’un passage/minute** :
  10 000 tâches, 20 000 intentions (internes et externes), 5 000 e-mails et
  5 000 push simulés, aucun annulé/incertain. Vidage en **270,237 s** (budget 600 s :
  respecté) mais 99 % préparées en **139,529 s** (budget 120 s : **échec**, +19,529 s).
  Les protections de révocation, timeout et équité sont conservées ; l’ancienne
  mesure favorable de 105,10 s ne valide pas ce dernier état. Dix tests fonctionnels
  supplémentaires passent : sessions administrateur, authentification et contention
  avec libération du slot. Revue indépendante des trois corrections terminée.
  RSS du processus pytest partagé : base **218,238 Mio**, pic **265,195 Mio**,
  delta **46,957 Mio**. Le delta inférieur à 64 Mio ne valide pas la limite absolue
  d’un worker dédié. Rapport final `tmp/crm-performance-rappels.json` ; rapport
  initial séparé `tmp/crm-performance-rappels-initial.json`.

### Optimisations ciblées et rejeu

Les préférences de rappel sont lues sous verrou une seule fois par transaction,
avec invalidation à la modification, au commit et au rollback. Aucun droit ni
fait d’autorité n’est conservé entre transactions. **28 tests ciblés réussissent**.
Le comparatif indicatif de 1 000 tâches (trois paires) réduit la médiane de
8,550 à 6,772 s ; ce petit jeu ne remplace pas le scénario de capacité.

Sur les **10 000 tâches**, avec un worker, même cadence de 60 s et mêmes contrôles,
la préparation de 99 % atteint **133,303 s** : le budget de 120 s reste dépassé.
Les 10 000 remises terminent en **256,138 s**, sous le budget de 600 s.
Dix tests de non-régression supplémentaires passent. RSS partagé : pic **258,54 Mio**,
delta **40,152 Mio** ; le budget absolu de 64 Mio n’est toujours pas validé.
Rapports locaux : `tmp/crm-performance-rappels.json` et comparaison conservée
`tmp/crm-performance-rappels-avant-optimisation-preferences.json`.

Une seconde mesure avec **deux workers** mais toujours 50 s d’admission donne
**128,780 s** pour 99 % des intentions commitées (échec 120 s), **261,650 s**
pour les 10 000 remises (réussite 600 s). Aucun doublon : 5 000 e-mails et
5 000 push simulés, aucun annulé/incertain. Le rapport est conservé sous
`tmp/crm-performance-rappels-deux-workers-admission50.json`.

Le dernier changement de concurrence compte les insertions réellement créées
(`RETURNING`) et réserve la préparation d’une tâche par un verrou transactionnel
non bloquant. Les contrôles d’autorité restent inchangés. La revue indépendante a
également corrigé le report entre sélection et relecture : aucun marqueur n’est
créé avant la nouvelle échéance, qui reste éligible ensuite. **29 tests ciblés**
réussissent sur cet état. La fenêtre d’admission passe ensuite à 58 s pour réduire
le temps inactif du passage, sans modifier les budgets de validation.

### Résultat final des rappels

**Deux workers, admission 58 s, cadence 60 s**, sur les mêmes 10 000 tâches :

- 99 % des intentions **commitées**, observées par une connexion indépendante :
  **124,666 s**, soit **échec du budget 120 s de 4,666 s**.
- 10 000 remises en **235,753 s**, sous le budget de 600 s, sur quatre passages.
- 5 000 e-mails et 5 000 push simulés ; **zéro doublon, annulation ou incertitude**.
- RSS du processus partagé : pic **133,629 Mio**, delta **23,613 Mio**. Ces valeurs
  ne valident pas un RSS absolu de 64 Mio par worker isolé.
- Les quatre tests fonctionnels ciblant contention/slots, concurrence,
  restitution du claim et report à une nouvelle échéance réussissent.

Rapport local conservé :
`tmp/crm-performance-rappels-deux-workers-admission58-final.json`.
Le délai de préparation reste une réserve explicite ; aucun seuil n’a été
modifié et le test de capacité reste en échec sur cette assertion. Les transports
réels, leurs quotas et latences ne font pas partie de cette mesure.

### Restant avant vérification intégrale

1. **CA-06/26/27 — préparation des rappels** : réduire la préparation de 99 %
   des intentions de **124,666 s à 120 s** sur le protocole final (deux workers,
   admission 58 s, cadence 60 s, 10 000 tâches). La remise respecte son budget.
   La réserve de préparation reste ouverte, sans changement d’assertion.
2. **Mémoire des rappels — dépassement de conception** : un processus Python
   neuf sur Windows, sans pytest ni FastAPI, atteint déjà **84,31 Mio RSS** à l’import de la
   composition (budget absolu 64 Mio), avant toute tâche. Étapes mesurées :
   Python 15,91 ; isolation/pilote PostgreSQL 34,65 ; SQLAlchemy 53,18 ; modèles
   ORM partagés 73,76 ; identité 76,50 Mio. Une composition dédiée plus légère
   et une mesure sur la cible Linux sont nécessaires ; aucun budget n’est
   réinterprété en mémoire additionnelle. Cette mesure ne contacte aucune base.
   Rapport et commande reproductible : `tmp/crm-memoire-worker-isole.json`
   dans le backend (artefact local synthétique, hors Git).
3. La charge mixte fonctionnelle import/notes/lectures est vérifiée, mais pas un
   protocole complet HTTP à 1/5/10/20 utilisateurs mêlant tous les transports,
   imports et rappels sur une cible dimensionnée. Les temps de persistance ne
   constituent pas une mesure de latence HTTP de bout en bout.

### Limites et activation

La couverture n’est pas déclarée intégralement clôturée tant qu’un budget ou un
scénario reste ouvert. Les conditions d’activation demeurent ARB-07 (conservation),
choix du fournisseur de tuiles, secrets VAPID/e-mail, planification des workers et
attribution explicite des droits. Aucun pilote ni validation UX externe n’est
exigé pour les tests produit. Aucun commit, push, déploiement ou migration TEST
n’est réalisé dans cette tâche.

### Contrôles documentaires finaux

- `python scripts/check_guidance.py` : 95 guides, 1 081 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 13 documents,
  374 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 137 sources vérifiées.
- Contrat CRM régénéré hors ligne : 41 chemins et 28 schémas, réponses 503 des
  agrégats incluses. `git diff --check` réussi dans les deux dépôts modifiés.
- Captures supplémentaires 360 et 1280 px examinées après le dernier parcours
  navigateur ; aucune correction d’interface supplémentaire nécessaire.

## Carte Nouvelle-Aquitaine — correctif du 4 novembre 2026

Demande : limiter la carte régionale et permettre de filtrer ses douze
départements. La carte nationale et ses raccourcis outre-mer ne correspondaient
plus au périmètre souhaité. Correction sur les changements locaux issus du
backend `32106fd` et du dépôt documentaire `17218a0`.

La projection SQL impose les départements de Nouvelle-Aquitaine avant agrégation,
indépendamment de l’emprise rectangulaire et du code postal. Le filtre département
et la région sont conservés en ouvrant la liste et sa pagination. La liste générale
reste nationale ; les fiches sans INSEE disposent d’un accès distinct tous territoires.
Le cadrage initial, le dézoom et le recentrage utilisent l’enveloppe régionale ou
départementale, y compris lorsqu’aucun prospect ne correspond aux filtres.

Preuves locales :

- **43 tests Python réussis** : API HTTP, PostgreSQL jetable, combinaisons de
  filtres, exclusion d’une commune hors région pourtant dans l’emprise, douze
  départements, compteurs, pagination, liaison des curseurs aux filtres,
  plafond de 500 groupes et portefeuille synthétique de 10 000 prospects.
- **652 contrôles d’architecture et de recensement validés** : 651 lors de la
  suite initiale ; le dernier test, affecté par la capture Windows de `git init`
  (`WinError 6`), réussit inchangé avec `-s`.
- `node tests/browser/crm.cjs` : parcours CRM réussi avec Leaflet réel et tuiles
  synthétiques locales. Sélection Gironde, transmission des filtres lors du zoom,
  dézoom borné, liens vers la liste et une commune, accès sans commune, état vide
  Charente, réinitialisation et repli sans fond cartographique vérifiés. Sept vues
  contrôlées de 320 à 1440 px ; captures régionales à 320 et 1280 px.
- Documentation : `python scripts/check_guidance.py` et
  `python scripts/sync_documentation.py --check-sources` réussissent.

Contrat OpenAPI canonique et guide utilisateur mis à jour. Générateur inchangé :
les nouveaux filtres sont des paramètres de lecture facultatifs, sans modification
du format des fiches ou de leur création. Aucune migration, réparation de données,
clé supplémentaire ni changement de fournisseur de tuiles. Les règles métier et
permissions restent inchangées. La campagne complète de charge à 100 000 prospects
et la vérification sur TEST ne sont pas rejouées ; les réserves antérieures de
performance des rappels restent ouvertes. Aucun commit, push ou déploiement dans
ce correctif.

## Correctif du 4 novembre 2026 — Saisie des prospects en Nouvelle-Aquitaine

La restriction de carte ne limitait pas les écritures. Le domaine Prospection
porte désormais la règle des douze départements : INSEE obligatoire pour toute
création et tout changement effectif de localisation. Les entrées manuelles et
imports INIT/UPSERT l'appliquent ; les fiches historiques hors région ou sans
commune conservent leur suivi et leurs contacts modifiables.

Le formulaire recherche puis sélectionne la commune. Les mutations manuelles
utilisent le référentiel local `crm_communes`, alimenté uniquement par les
réponses de la recherche serveur ; le réseau précède la transaction courte de
cache et reste absent des transactions métier. Les imports contrôlent hors
réseau le territoire déclaré par INSEE, sans certifier l'existence du code ni
la concordance de son libellé. Un ancien plan incompatible est recalculé puis
refusé avant toute mutation du groupe.

Preuves locales :

- Deux tests d'import ont reproduit les refus manquants avant correction.
  **72 scénarios distincts d'import réussis**, domaine/CSV/HTTP/PostgreSQL et
  charge mixte, dont 10 000 lignes. Création absente/hors région, conservation
  des localisations historiques, protections et plans devenus obsolètes couverts.
- **74 tests ciblés serveur réussis** (73 dans la suite finale, puis un test
  PostgreSQL supplémentaire) : domaine, application, HTTP, persistance réelle,
  carte, démonstration et charge mixte. Vérification spécifique de l'ordre
  recherche réseau avant SQL, du cache réel, du nom canonique, du code inconnu,
  de l'idempotence et des refus sans effet.
- **653 contrôles d'architecture et de recensement réussis** avec `-s` et sortie
  fichier pour éviter le problème Windows de capture subprocess ; assertions
  inchangées. PostgreSQL jetable arrêté après les contrôles.
- `node tests/browser/crm.cjs` réussi : commune requise, sélection régionale,
  absence de résultat, erreur de recherche sans perte de sélection, réponse
  périmée ignorée, modifications non géographiques de fiches historiques,
  INSEE sans nom conservé, localisation avec confirmation d'homonymes. Sept vues
  de 320 à 1440 px ; formulaires à 320/1280 px inspectés visuellement.
- Revue indépendante des règles/imports/cache et du formulaire ; les deux
  écarts détectés (sélection historique sans nom, confirmation d'homonymes)
  sont corrigés et couverts par les tests navigateur.
- Documentation : guides, liens des Markdown modifiés et sources exportées
  validés ; `git diff --check` réussi dans backend et projet.

**Réserve de charge distincte** : le banc PostgreSQL à 100 000 prospects dépasse
le budget carte de 2 s p95 (2,884 s base fraîche ; 3,819 s après vacuum). Les cas
à 10 000 passent ; listes et tableaux de bord passent à dix lecteurs. Le
correctif de saisie ne change pas la requête de lecture cartographique (seule la
constante des départements est partagée avec le domaine). Ces échecs restent
consignés, sans affaiblissement du seuil ni conclusion de validation complète
des performances. Ils ne constituent pas un refus fonctionnel de saisie.

CA-01/08/09/10/14 et documentation fonctionnelle/technique actualisés ; contrat
OpenAPI canonique régénéré, exemples CSV et fixtures du générateur de démonstration
adaptés. Aucune migration requise : colonnes et cache communal existent déjà.
Aucun import réel, envoi, réparation de données, commit, push ou déploiement TEST.
Les autres travaux locaux des dépôts sont conservés.

## Correctif du 4 novembre 2026 — Domaine dédié CRM

Demande : accéder directement à Localeo CRM via `crm.localeo.city` et
`test-crm.localeo.city`. Configuration `CRM_PUBLIC_ORIGIN` optionnelle et validée,
racine de l'hôte dédié vers `/internal/crm/`, navigation ERP basée sur l'URL du
contexte, identité CRM à la connexion et conservation de la destination après
authentification nominative ou administrateur historique. Les autres racines et
les accès historiques restent utilisables.

Contrôles locaux :

- **745 tests Python réussis** : 92 ciblés (domaine dédié, PWA CRM/Atelier,
  comptes internes et formulaire CRM), 653 architecture et recensements. Origine
  HTTPS stricte, hôte non autorisé/forgé, GET/HEAD, désactivation, permissions,
  session host-only, refus CSRF inter-origines, retour fermé et consommé une
  seule fois, ressources PWA vérifiés. Lanceur isolé, sans configuration privée.
- `node tests/browser/erp-home-applications.cjs` : **30 scénarios réussis**,
  URL dédiée dans tuile et menu, droits, repli historique et mobile.
- `node tests/browser/connexion-interne.cjs` : parcours nominatif, attente,
  erreurs, clavier et initialisation conservés à 320/390/1280 px ; huit cas
  supplémentaires de connexion CRM (accueil, fiche profonde, deux retours
  externes refusés, à 320 et 1280 px). Capture mobile CRM inspectée.
- `node tests/browser/crm.cjs` : parcours CRM et sept vues, 320 à 1440 px,
  réussis après modification de l'en-tête partagé.
- Revue indépendante des origines, retours, permissions et sessions sans
  anomalie bloquante. Contrôles documentaires et différences vérifiés.

Pas de migration SQL, de modification des permissions métier, du contrat
OpenAPI ou du générateur. Les trois autres frontends ne consomment pas ces API.
Les comptes et données restent communs ; les sessions, PWA installées et
abonnements WebPush restent liés à leur origine. Une connexion et une activation
volontaire des notifications sont nécessaires sur le nouveau domaine.

**Non exécuté** : ajout du domaine Render, DNS, certificat, variables opérateur,
recette distante et déploiement. Cible TEST documentée depuis le CNAME public du
backoffice observé le 4 novembre 2026 : `test-localeo-backend.onrender.com`.
La [procédure d'activation](exploitation.md#domaine-dédié) et le modèle sans
secrets permettent cette mise en service. Aucun commit ni push dans ce correctif.


## Bilan d’implémentation E71-EVOL-04 — 4 novembre 2026

La qualification structurée est implémentée dans **localeo-backend** ;
**localeo-projet** porte les spécifications, guides, modèles CSV et OpenAPI V1.2.
Les trois frontends Pro/Animation/Marketplace ne consomment pas ces données ;
aucune modification, migration ou permission nouvelle dans leurs dépôts.

| Critères | Preuves exécutables ajoutées ou prolongées |
| --- | --- |
| CA-30/31 | `tests/domain/prospection/test_qualification.py`, `tests/security/test_crm_qualification_postgres.py` : champs fermés, preuves, identité territoriale, SIREN/SIRET et établissements distincts |
| CA-32/33 | Mêmes suites + `tests/integration/prospection/test_qualification_http.py` : seuils/inconnus/zéro, terrain, confirmation immuable, révision, références distinctes et comparaison paginée |
| CA-34/35 | `tests/application/test_crm_qualification.py` et HTTP : chargement du contact courant, tiers refusé, porteur obsolète, preuve explicitement renouvelée, budget zéro, protections ciblées |
| CA-36 | PostgreSQL/HTTP : appartenance unique, membres, couverture par lots et obsolescence des références de projet, provenance population/compétences conservée |
| CA-37 | `tests/domain/prospection/test_import_qualification.py`, `tests/integration/prospection/test_import_qualification_postgres.py`, suites CSV/imports HTTP/PostgreSQL existantes : formats 1/2, groupe atomique, INIT/UPSERT, protection/reprise et choix de référence |
| CA-38/39 | HTTP réel + PostgreSQL : mêmes filtres liste/suivi/carte, critères sur un même enfant, aucun doublon, droits/CSRF/révocation/rejeu ; tests concurrence SQL et navigateurs |
| CA-40 | `tests/integration/prospection/test_qualification_restauration.py`, `tests/unit/test_demonstration_crm.py`, migration v293 et test générateur CRM core ; export OpenAPI et contrôles documentaires |

La recette navigateur `tests/browser/crm-qualification.cjs` teste les formulaires
progressifs et décisions d’import à 320 et 1280 px, saisie conservée en erreur,
clavier, filtres URL et références obsolètes. `crm.cjs` et `crm-rappels.cjs`
préservent les parcours du socle. Ces tests navigateur utilisent des API simulées ;
la suite HTTP qualification utilise les routes, domaine et PostgreSQL réels dans
un schéma jetable, avec session et CSRF, sans importer `app.main`.

La revue indépendante a identifié quatre écarts : action de localisation
contournant l’identité communale, effacement de sous-type/identifiant permettant
un contournement en deux commandes, projections de sortie ouvertes et fiabilité
dégradée sur coordonnées normalisées inchangées. Ils sont corrigés et couverts
par des tests domaine/HTTP ; les refus ne modifient ni version ni référence.
Le siège d’un EPCI reste modifiable. Aucun compte ou renseignement du classeur
réel n’a été copié dans les fixtures.

Les commandes et résultats finaux sont consignés après la vérification complète
ci-dessous. Les réserves antérieures de rappel, mémoire et carte à 100 000 ne
sont pas effacées par ces preuves fonctionnelles. **L’epic reste En cours** :
aucune clôture intégrale ni activation distante n’est annoncée.


### Exécutions finales de l’extension

Tests exécutés par le lanceur isolé du backend, sans chargement des fichiers
privés et sur PostgreSQL local jetable. `-s` et sortie fichier évitent le problème
Windows de capture subprocess ; aucune assertion désactivée.

- Groupe domaine/application/contrats/identité/readiness/PWA/démonstration :
  **292 réussis**, 4 tests API de rappels ignorés dans ce lancement sans URL
  PostgreSQL (à distinguer du résultat des tests exécutés).
- API qualification réelle, cœur CRM, carte régionale, contraintes et restauration
  de qualification : **41 réussis**. Ce lancement inclut le cycle de brouillon de
  couverture, confirmation et correction, et les non-régressions d’identité/sortie.
- Architecture et recensements : **658 réussis** ; contrôle supplémentaire du
  registre fermé des nouvelles routes réussi, soit **659** dans ce lancement.
- Lecteur documentaire privé : **14 réussis** après ajout du guide de qualification
  et du téléchargement de modèle 2, avec conservation de la liste fermée des liens.
- Imports CSV, domaine, HTTP et PostgreSQL : **104 réussis, 1 dépassement du budget**
  lors d’un lancement concurrent au chargement des 2 millions d’observations.
  Le format 1 préparé avant migration est réellement testé sur v291, puis rejoué
  après v293 en gardant son plan. Le cas chronométré de 10 000 groupes est à
  distinguer de l’import de charge format 2 à 100 groupes/10 000 lignes.
- Trois recettes navigateur réussies : `crm-qualification.cjs`, `crm.cjs` et
  `crm-rappels.cjs`. API simulées, contrôles 320–1440 px selon la suite ; captures
  locales examinées, saisie, clavier, défilement et états d’erreur vérifiés.

Les revues finales ont ajouté deux cas corrigés : empreinte de couverture capturée
au brouillon, et acquittement des nouvelles observations par bloc sans alerte
permanente sur les anciennes références. L’ordre de création/confirmation/choix
utilise `clock_timestamp()` sous le verrou d’organisation, et non la date métier.
Un test concurrent démarre avant le choix et insère après, sans masquer la nouvelle
observation. Les permissions de la purge SQL sont vérifiées après restauration :
les ACL sont conservées, pas d’EXECUTE PUBLIC restauré implicitement.

Le protocole de capacité est reproductible dans
`tests/security/test_crm_qualification_performance_postgres.py` : 10 000 puis
100 000 prospects, 20 observations par prospect, 20 clients maximum, demande de
20 lectures/s et 5 mutations/s pendant cinq secondes, avec import concurrent.
Ce test mesure la persistance/application locales, pas la latence HTTP complète
sur TEST. Les prochains résultats ci-dessous distinguent les essais et corrections.


### Capacité de la qualification — mesures et correction SQL

Premier essai N=10 000, 200 000 observations : lectures mixtes p95 **411,28 ms**,
p99 **511,89 ms** ; mutations p95 **412,94 ms**, p99 **479,08 ms** ; import 2 de
10 000 lignes regroupées en 100 prospects : **5,89 s**. Objectifs respectés.

À 100 000 prospects / 2 millions d’observations, l’essai initial échoue : filtre
combiné p95 **869,83 ms**, p99 **1 179,26 ms** ; charge mixte lecture p95 **7 715,09 ms**,
p99 **12 114,99 ms** et mutation p95 **2 101,77 ms**, p99 **11 002,10 ms**.
Ces échecs ne sont ni supprimés ni requalifiés en succès.

EXPLAIN révèle un parcours séquentiel avec tri sans filtre d’état et de nombreuses
sondes contacts avant LIMIT. v293 ajoute les index de pagination globale
`(updated_at DESC,id DESC)` et d’activité
`((qualification->>'famille_animation'),updated_at DESC,id DESC)`.
**ANALYZE** est nécessaire pour les statistiques d’expression ; la migration et
le chargement du banc l’exécutent. Aucun filtre ou seuil n’a été assoupli.

Mesure finale avec les modules courants, ces index et statistiques :

| Mesure | p95 | p99 | Objectif |
| --- | --- | --- | --- |
| Lectures sous charge mixte | 160,64 ms | 229,64 ms | 500 ms / 1 000 ms : réussi |
| Mutations sous charge mixte | 314,51 ms | 403,09 ms | 800 ms / 2 000 ms : réussi |
| Lecture filtrée séquentielle la plus lente | 22,22 ms | 53,10 ms | 500 ms / 1 000 ms : réussi |

Import 2 concurrent : **5,177 s**, toujours 10 000 lignes / 100 groupes. Le jeu
principal comporte 100 000 prospects et 2 millions d’observations ; 200 prospects
supplémentaires issus d’essais d’import précédents sont conservés dans la mesure
finale et signalés. Le chargement initial monolithique a été remplacé par des
transactions de fixture de 20 000 observations ; aucun trigger n’est désactivé.
Le processus du premier essai a été arrêté après chargement commité pour préserver
ce jeu ; la mesure finale utilise un processus neuf et les assertions de budget
courantes, puis le schéma jetable est supprimé. Cela n’est pas annoncé comme un
pytest intégral vert depuis le début du premier essai interrompu.

Limites : cinq secondes de trafic mixte, persistance/application locales,
statistiques à jour et cache PostgreSQL sollicité pendant les lectures répétées.
Pas de mesure HTTP de bout en bout, de transport réel ou de stabilité longue durée
sur la cible TEST. La mémoire RSS de l’extension n’est pas mesurée par ce banc.
Les réserves historiques carte/rappels/mémoire restent ouvertes ; elles ne sont
pas couvertes par les budgets de ces nouvelles listes de qualification.


### Derniers rejeux, restauration et limites restantes

- Le dépassement de l’import standard est rejoué **sans autre charge PostgreSQL** :
  **10 000 prospects distincts créés en 68,208 s** (budget 120 s), dépôt **0,823 s**
  (budget 1 s), aperçu **3,591 s**, pic mémoire additionnelle **18,6 Mio**.
  Les assertions de comptage, d’absence de doublons et de budget sont inchangées.
  Les **105 scénarios d’import** sont donc validés sur les exécutions décrites :
  104 dans la suite, puis ce cas chronométré isolé ; pas de suite initiale
  présentée comme entièrement verte sous contention.
- Les quatre cas API de rappels ignorés sans URL PostgreSQL sont rejoués avec la
  cible jetable : **4 réussis**. Le lancement avec l’import isolé donne
  **5 réussis en 73,41 s** (`tests/api/test_crm_rappels_api.py` et
  `test_import_10000_lignes_budget_postgres`). Aucun skip restant dans ce lancement.
- Dernier groupe qualification/restauration/générateur : **15 réussis sur PostgreSQL**,
  incluant acquittement de référence, ancien brouillon confirmé après sélection,
  course de transactions et préservation d’une appartenance partagée entre fiches.
  Le groupe complémentaire domaine/readiness/outillage de démonstration donne
  **199 réussites**. Ces groupes recouvrent d’autres tests déjà cités : ne pas
  additionner les chiffres pour annoncer un total de cas distincts.
- Chaîne complète des migrations **v147 → v293**, rejeu sans modification des
  empreintes, `pg_dump`/`pg_restore` PostgreSQL 18 et vérification des ACL privées :
  **1 réussi en 22,86 s**, dans `tests/integration/test_crm_migration_restauration.py`.
  L’exercice JSON et cet exercice dump sont complémentaires ; aucun ne restaure
  en place la base TEST partagée.

Rapport de charge final conservé hors Git dans le backend :
`tmp/e71-qualification-mesures-100k-final.json`. L’artefact temporaire original du
premier essai 10k n’est plus disponible ; les chiffres de cet essai proviennent
uniquement de sa sortie console, pas d’un fichier reconstruit. Le jeu de mesure
100k comprend 200 ajouts d’essais précédents puis 100 nouveaux prospects d’import.
La limite de 20 clients est un pool de 20 threads, avec le pool SQLAlchemy usuel
5 connexions + 10 débordements ; les attentes de connexion sont comprises dans
les durées. Il ne s’agit pas de 20 connexions permanentes ni d’une charge HTTP.

**État livré :** qualification, import 2, UX progressive, contrats, migration,
restauration, générateur et contrôles fonctionnels locaux disponibles.
**Réserves maintenues :** capacités historiques carte/rappels/mémoire du socle,
charge HTTP prolongée et mémoire complète de l’extension non vérifiées sur TEST.
ARB-07 demeure un préalable aux données réelles, sans empêcher les tests
synthétiques. L’epic reste **En cours** ; aucun commit, push, déploiement ou
application de v293 sur TEST dans cette demande.


Contrôles documentaires finaux : `check_guidance.py` **96 guides / 1 099 liens**,
`--all-markdown --changed` **16 documents / 238 liens**, zéro erreur/avertissement ;
`sync_documentation.py --check-sources` **145 sources** vérifiées. OpenAPI V1.2 :
**50 chemins, 62 schémas**. `git diff --check` réussi dans les deux dépôts modifiés.
Les travaux E75 préexistants sont préservés ; les trois autres dépôts restent
propres. La base PostgreSQL locale de cette tâche est arrêtée après les contrôles.

### Application de v293 sur TEST — 4 novembre 2026

Opération distincte de la vérification locale précédente, demandée explicitement
par l’utilisateur. La base TEST Render est identifiée avec le profil privé TEST,
distinct de la production. Le plan du runner ne contient que
`v293_crm_qualification.sql`, depuis une base en v292.

- Sauvegarde PostgreSQL 18 créée avant migration : **60 226 725 octets**,
  empreinte privée enregistrée et lecture complète par `pg_restore` réussie.
  Les ACL sont conservées. Aucune restauration en place n’est effectuée.
- Migration appliquée par `scripts/database/apply_migrations.py` avec verrouillage
  borné, transaction et suivi d’empreinte ; version **293**, aucune migration
  restante. Empreinte normalisée :
  `8f76052682967d147ff5d5e061b264a7edd28221562f2603f918cc89aed77c2c`.
- Objets, index valides, triggers actifs et colonne générée vérifiés ; le droit
  d’exécution PUBLIC de la purge reste retiré. Les compteurs des 20 tables CRM
  préexistantes et des quatre tables Live/participants contrôlées sont inchangés.
- Readiness du **code local courant contre TEST en lecture seule** : **175
  contrôles**, résultat READY. Avant publication du nouveau backend, le service
  distant répond aussi READY sur ses **165 contrôles** ; santé et configuration
  Live répondent HTTP 200, le CRM non authentifié redirige en HTTP 303.
- Rejeu ciblé avant publication : **91 tests réussis**, domaine qualification,
  import 2, orchestration, projections API et readiness. Guides : **96 guides /
  1 099 liens**, zéro erreur ; **145 sources documentaires** vérifiées.

Sauvegarde, plan et reçus privés dans le backend, sous
`demonstrations/prive/operations/migration-v293-test-20261104T212152Z-b4f3e70e/`.
Aucun prospect du fichier Excel n’est importé par cette opération. La migration
ne constitue pas une preuve de publication du code ni une recette authentifiée
du CRM après déploiement ; les réserves précédentes restent inchangées.

### Correctif de planification des imports — 4 novembre 2026

Un dépôt TEST restait en DEPOSE avec tous ses groupes NON_APPLIQUE : le worker
existait mais n’était inscrit ni au catalogue des batchs ni à sa planification.
L’extension locale ajoute `prospection.imports.traiter`, chaque minute, maximum
100 unités par passage, au catalogue partagé. La route appelle `BatchRunner` :
exécution attribuée à la clé technique, verrou, historique, durée, corrélation et
compteurs dans la console existante. Le CRM désactivé produit un passage inerte
tracé ; les erreurs techniques enregistrées omettent les cellules du fichier.

La confirmation appartient toujours à l’utilisateur : le worker prépare seulement
l’aperçu d’un dépôt, puis ne peut écrire les prospects qu’après confirmation et
revalidation de l’autorité du confirmateur. Aucun lot TEST n’est confirmé ou
appliqué par les tests de ce correctif.

Preuves ciblées : quatre échecs de reproduction (planification absente, aucune
exécution en supervision, état désactivé non inerte et erreur non historisée),
puis **22 tests réussis** HTTP/supervision/ordonnanceur. Le rendu serveur de la
console est vérifié en succès/échec, avec cron, compteurs et absence du contenu
privé. Sur PostgreSQL local jetable, **4 tests réussis** : worker périodique
attendant la confirmation, application unique, retrait de droit avant aperçu et
pendant l’import, parcours HTTP dépôt/aperçu/confirmation/bilan.

Le recensement de l’ordonnanceur attendait encore 25 planifications alors que
le HEAD avant correctif en déclarait 28 (comparaison AST du catalogue versionné).
L’assertion exacte est actualisée à **29**, avec présence explicite du nouveau
batch et rattrapages autorisés, sans réduire les contrôles de concurrence.

Le rejeu architecture/recensements/domaine imports et sécurité des batchs donne
**712 tests réussis**. Un premier passage relevait une fixture préexistante
incomplète dans `test_animation_batch_http.py` : le service de maintenance des
preuves e-mail de conservation n’était pas doublé et tentait une connexion
externe, refusée par le runner isolé. La route et le test étaient inchangés au
HEAD avant correctif. La fixture ajoute seulement ce double, et vérifie aussi
le compteur de maintenance retourné ; aucune assertion n’est retirée. Les
contrôles documentaires passent : **96 guides / 1 099 liens**, **145 sources**,
zéro erreur ; `git diff --check` passe dans les deux dépôts.

Sans migration, modification des droits, nouvelle table, nouveau secret ni impact
sur les frontends Pro/Animation/Live ou le générateur. Le contrat OpenAPI CRM
régénéré hors ligne reste identique au contrat canonique. Ce bilan distingue le
code local de son déploiement : aucun commit, push ou changement de configuration
TEST n’est réalisé dans cette demande.

### Correctif CSV — dossier commercial facultatif, 4 novembre 2026

Sur demande utilisateur, l’import ne doit pas ouvrir un dossier commercial
« Qualification… » pour chaque prospect. Le domaine des formats 1 et 2 exige
désormais seulement `prospect_ref` et `nom_prospect`, plus l’INSEE pour créer ou
modifier la localisation. Un dossier requiert sa référence et son périmètre
explicites ; les champs de dossier/projet sans référence sont refusés avec
`DOSSIER_REFERENCE_REQUISE`. Contacts, notes, observations et appartenance EPCI
restent indépendants. Les anciens CSV demandant un dossier gardent leur
comportement ; les plans, empreintes et écritures restent inchangés.

- Reproduction domaine : **27 échecs avant correction**, 62 cas existants réussis ;
  après correction, **193 tests du domaine Prospection réussis**.
- Groupe final architecture/recensements/domaine et sécurité du batch : **861
  réussis**. Ces tests recouvrent les 193 précédents : ne pas les additionner.
- PostgreSQL local jetable et vraie pile HTTP d’import : **38 réussis**, deux
  tests de volume explicitement non sélectionnés. Vérifiés en formats 1 et 2 :
  création fiche/contact/note sans dossier ni lien DOSSIER, INIT répété sans
  doublon, ajout ultérieur explicite en UPSERT. Le cas structuré conserve
  **44 commerces** et sa référence à 44 après une nouvelle observation à 45,
  l’appartenance, le contact et la note, sans dossier.
- Recette navigateur CRM réussie ; notice d’import et rendu contrôlés à
  **320/1280 px**, sans débordement horizontal. Les autres parcours existants
  du scénario navigateur restent couverts.
- Revue indépendante : aucun dossier implicite ni perte de qualification,
  autorité et protection des réimports conservées. Prospects et tableau de bord
  incluent les fiches sans dossier ; la carte compte zéro dossier et Suivi
  affiche seulement les dossiers ouverts explicitement. Les filtres de dossier
  excluent normalement les fiches sans dossier correspondant.

Le CSV prioritaire privé est réémis avec **800 prospects, 646 contacts, 800 notes,
1 754 observations et zéro dossier attendu** sur une base vide. Toutes les cellules
hors champs de dossier/projet sont comparées à l’export précédent et identiques,
notamment notes intégrales et compteurs de commerces. Source et références de
prospect/évaluation sont conservées. L’ancien export et le classeur restent
intacts ; les fichiers et leur notice demeurent hors Git.

Aucune migration, suppression de dossiers existants, modification des droits ni
impact sur les trois frontends publics/commerçants/organisateurs ou le générateur.
Le contrat HTTP ne change pas de forme ; les modèles gardent leurs 21/85 en-têtes
et le contrat CSV canonique décrit les nouvelles conditions. Aucun import TEST,
commit, push ni déploiement de ce correctif n’est réalisé dans cette demande.

## Correctif du 4 novembre 2026 — communes importées absentes de la carte

**Cause reproduite sur TEST :** 670 prospects conservaient leur code INSEE,
mais 666 n’avaient aucun centre dans `crm_communes`. La carte joignait ce cache,
alimenté seulement par une recherche manuelle de commune, sans rattrapage des
imports CSV. Aucun filtre ou dossier manquant n’expliquait cette absence.

Le batch d’import complète désormais ce cache public, y compris sans lot en
attente et pour les imports terminés. Traitement borné par département, réseau
hors transaction, code exact, cache existant préservé et échec d’un département
indépendant des suivants. Aucun prospect, note, contact, comptage, dossier ou
version n’est changé. La carte distingue attente géographique et INSEE absent.

Preuves locales sur l’arbre de travail basé sur backend `16fd210` :

- Reproduction du rattrapage avant implémentation : trois tests en échec pour
  résolveur absent. Après correction, l’import sans dossier passe de zéro point
  à un point ; rejeu sans appel réseau, aucune mutation métier.
- **79 tests réussis** : résolution/adapter, PostgreSQL jetable, cœur CRM,
  formats d’import, vraie pile HTTP et sécurité/supervision du batch. Puis
  **30 tests réussis** pour la résolution et les filtres carte API/PostgreSQL,
  dont le compteur avant bbox et les filtres de dossier. Ces groupes se recouvrent.
- **852 tests réussis** d’architecture, recensements et domaine Prospection.
- Navigateur CRM réussi, y compris localisation en attente à **320/1280 px**,
  sans débordement ; parcours et droits existants conservés. Captures locales
  privées. Revue indépendante : aucune réserve bloquante après correction de
  la stratégie de reprise ; aucune requête géographique pendant un verrou SQL.
- Guides et sources exportées vérifiés ; la réponse carte reste une projection
  objet libre dans l’OpenAPI. Ajout documenté de `geolocalisation_en_attente` et
  des compteurs batch `geographie`, consommés uniquement par CRM/supervision.

**Rattrapage TEST réalisé :** 666 centres ajoutés, zéro erreur ou code introuvable,
670 prospects localisables sur 668 codes INSEE distincts. Sauvegarde privée du
cache et empreintes des huit tables métier suivies avant/après identiques.
Lecture réelle de la projection SQL : zéro localisation en attente dans les
douze départements, aucun département tronqué, somme des prospects départementaux
égale à 670. Région : 500 communes affichées et `truncated=true`, plafond existant.
Les preuves privées sont dans le backend, sous
`demonstrations/prive/operations/crm-centres-communes-test-20261104T222331Z/`.
Ce contrôle SQL ne constitue pas une recette de session navigateur authentifiée
sur TEST ; la recette navigateur utilise des données fictives locales.

Aucune migration, droit nouveau, modification du CSV ou du générateur requise :
les données synthétiques disposent déjà de leurs centres et le schéma ne change
pas. Les trois autres frontends ne consomment pas cette projection CRM. Les
réserves de capacité historiques restent ouvertes ; aucun nouveau test de charge
à grande échelle n’a été exécuté pour ce correctif. Code backend/PWA et guides
modifiés localement, sans commit, push ni déploiement automatique.

## Correctif du 4 novembre 2026 — totaux et pagination des recherches CRM

Les listes ne donnaient que les flèches précédente/suivante : les API ne
fournissaient aucun total et les projections fermées ne déclaraient pas ces
informations. Trois reproductions PostgreSQL échouent avant correction faute
de prise en charge de l’option de comptage.

Les listes partagent désormais un résumé **26–50 sur 670 résultats** et un pied
**Page 2 sur 27 · 25 par page**, avec flèches à pictogrammes, intitulés accessibles
et cibles de 44 px. Zéro résultat, début/fin, ouverture directe d’un curseur,
erreur de chargement et total devenu ancien sont distingués. L’historique reste
inchangé après une erreur et les boutons sont neutralisés pendant la requête.

Le contrat additif `avec_total=true` retourne `total`, `position` et
`total_calcule_le` selon les mêmes filtres SQL que les lignes. Le curseur est
validé avant comptage ; aucune modification des droits ou des signatures. La
PWA demande le total une fois par recherche, puis conserve son repère daté
pendant la navigation keyset. Aucun `OFFSET`, parcours complet côté navigateur
ou comptage supplémentaire imposé aux consommateurs existants. Saturation et
timeout du comptage : 503 `CRM_LECTURE_SATUREE` ; délai SQL précédent rétabli
après succès. Les enfants de fiche, qualifications et imports sont couverts.

Preuves sur backend `16fd210` et changements locaux, avec les correctifs
précédents conservés :

- **57 tests réussis** dans le groupe final PostgreSQL/API/projections et mesures
  ciblées : total avant curseur, rang direct, tâches en ordre ascendant, filtres
  de territoire/dossier, absence de doublons de prospects, zéro et absence
  d’option, rejet du curseur avant comptage, timeout réel, restauration du délai
  SQL, imports/qualifications et compatibilité des filtres carte.
- **38 tests de compatibilité réussis** pour les API/transactions existantes
  d’import et de qualification ; trois anciens tests de budget/profilage non
  sélectionnés. Les nouvelles mesures dédiées ci-dessous sont exécutées.
- **853 tests réussis** d’architecture, recensements et domaine Prospection.
- Navigateur CRM final réussi : 51 résultats répartis sur trois pages,
  précédent/suivant, une seule demande de comptage malgré navigation et reprise
  après 503, absence de double clic pendant la latence, filtres zéro/un résultat,
  remise à zéro et curseur ouvert directement. Erreur initiale récupérable par
  actualisation ; passage de 51 à 76 résultats signalant le repère devenu ancien.
  Captures de résumé/pied à **320/1280 px** contrôlées, sans débordement ni double
  défilement ; notices d’import et état géographique antérieurs conservés.
- Mesures finales locales, cinq passages par recherche, PostgreSQL jetable :

| Prospects synthétiques | Tous avec total, max | Recherche avec total, max | Département avec total, max | Page suivante sans comptage |
| --- | --- | --- | --- | --- |
| 10 000 | 39,50 ms | 34,15 ms | 21,12 ms | 5,15 ms |
| 100 000 | 47,70 ms | 63,38 ms | 35,30 ms | 3,93 ms |

Les mesures incluent comptage et chargement de 25 résultats, sous le budget
local déclaré de 1 s. Plan `EXPLAIN ANALYZE/BUFFERS` conservé dans les rapports
de test privés. Il ne s’agit pas d’une charge concurrente en hébergement ni de
la levée des réserves de capacité historiques du CRM.

Revue indépendante : filtres/droits, option hors signature, défaut sans coût,
projections fermées et libération du sémaphore vérifiés ; remarque sur le timeout
résolue par restauration du délai précédent et test dédié. OpenAPI canonique
régénéré : 50 chemins, 62 schémas, ajouts optionnels seulement. Guides utilisateur,
contrat et diagnostic d’exploitation actualisés. Aucune migration, modification
du CSV ou du générateur, ni effet sur les trois autres frontends : projection de
lecture propre à CRM et données synthétiques existantes compatibles.

Aucun accès à TEST pour ce correctif, commit, push ou déploiement effectué.

## Correctif du 4 novembre 2026 — historique des imports réduit à la source

Les événements `IMPORT` présentaient tout le contexte documentaire du CSV dans
**Historique des échanges**, avec type, date et identifiant de l’importateur.
Ils affichent désormais uniquement **Source : …**, valeur du champ **Origine du
prospect**, ou **Non renseignée** si absent. Les notes, appels, e-mails et leurs
corrections gardent leur présentation. Le texte importé est conservé en base ;
aucune suppression, modification d’import ou extraction heuristique du texte.

Reproduction navigateur avant correction : absence du libellé de source attendu.
Après correction, scénario complet CRM réussi avec entrée importée volumineuse
et note manuelle : source seule, détail et auteur technique absents du DOM,
note manuelle et correction conservées. Source vide explicite et source contenant
du balisage affichée comme texte, sans élément HTML injecté. Captures vérifiées
à **320/1280 px**, sans débordement. Syntaxe JavaScript, `git diff --check`, guides
et 145 sources documentaires vérifiés.

Correctif de présentation dans le backend/PWA CRM et son guide canonique ; aucun
changement d’API, de règle métier, de schéma, de générateur ou des autres frontends.
Pas de rejeu Python/PostgreSQL nécessaire pour ce rendu JavaScript. Aucun accès
à TEST, commit, push ou déploiement réalisé ; travaux antérieurs conservés.
