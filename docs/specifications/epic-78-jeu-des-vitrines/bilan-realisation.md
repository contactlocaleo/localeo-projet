# E78 — Bilan de réalisation locale

Travail des **16 et 17 novembre 2026**, sur demande d’implémentation des quatre lots.
État **En cours** dans la [roadmap](../../roadmap/README.md). Le modèle reste
inactif ; le schéma Test est migré le 17 novembre comme détaillé ci-dessous,
sans attestation de déploiement applicatif. Les six stories,
seize critères et sept décisions de la [spécification](README.md) sont conservés.

## Résultat et propriétaires

Les quatre applications et le dépôt documentaire sont modifiés indépendamment.
Le domaine backend porte le choix unique, l’essai définitif, l’intersection avec
le passage du même commerce, la préparation versionnée et la reprise identique.
Les interfaces présentent les actions autorisées et les versions courantes.

- Backend : moteur/stratégie `JEU_VITRINES:1.0`, préparation privée, publication,
  réponses et preuves, qualification, incidents, clôture avec checkpoint,
  tirage existant, kits et générateur local. Migration additive `v323` : huit
  tables dédiées, modèle catalogue standard **inactif** ; aucune ancienne SQL modifiée.
- Animation et ERP : seuil/mode de passage explicites, approbation du contenu,
  contrôle de l’installation exacte, suivi participants, suspension de l’édition,
  contrôles de rétablissement et clôture reprenable.
- Pro : préparation dans l’invitation acceptée et la fiche animation, brouillon,
  proposition, correction, installation attestée, kit ; salarié exclu du contenu.
- Live/Marketplace : vitrines paginées, cible publique conservée, brouillons
  indépendants, revue puis réponse définitive, résultat immédiat, QR/PIN selon
  décision serveur, solution seulement après clôture effective.
- Projet : roadmap, spécifications fonctionnelles/ops et OpenAPI E41/E42.
  Les OpenAPI Animation/Pro et les trois manifestes moteur sont régénérés depuis
  le backend hors ligne, sans configuration opérateur.

Points d'entrée pour la revue, chemins relatifs à chaque dépôt :

| Dépôt | Fichiers principaux |
| --- | --- |
| Backend | `app/domaine/animation_locale/moteurs/vitrines.py`, `app/application/animation_locale/services/{vitrines,exploitation_vitrines}.py`, `app/api/vitrines_api.py`, `app/infrastructure/admin/vitrines_animation.html`, `sql/v323_jeu_vitrines.sql`, `scripts/demonstration/vitrines.py` |
| Animation | `src/app/components/{VitrinesPreparation,VitrinesExploitation,VitrinesParticipants}.tsx`, `src/app/hooks/useVitrinesCommand.ts`, `src/app/lib/vitrines.ts`, contrats `src/imports/moteur-animation/` |
| Pro | `src/features/animations/components/{VitrinePreparation.jsx,useVitrineNavigationGuard.js,vitrineMemory.js}`, pages invitation/animation et `queries.js`, contrats `api/` |
| Marketplace | `src/live/VitrinesGame.jsx`, `src/live/vitrineTarget.mjs`, accès/inscription/reprise Live et contrats `src/contracts/moteur-animation/` |
| Projet | Dossier canonique E78, backlog `docs/roadmap/en-cours/epic-78-jeu-des-vitrines-backlog.md`, roadmap/index, guides fonctionnels/ops et OpenAPI E41/E42 |

## Traçabilité des seize critères

La [matrice de recette](verification-livraison.md#matrice-de-traçabilité) conserve
les exigences complètes. Les preuves ci-dessous établissent le périmètre exécuté ;
elles ne remplacent pas les réserves de capacité et d’intégration indiquées plus bas.
Les chemins de tests sont relatifs au dépôt cité.

| Critère | Implémentation / preuve observable exécutée |
| --- | --- |
| E78-CA-01 | Registres domaine et trois consommateurs explicites ; modèle ANIMATION standard inactif en v323 ; tests migration et registres. |
| E78-CA-02 | K et booléen stricts, 1..100 vitrines, politiques explicites ; tests domaine bornes/erreurs et publication réelle dans la démo. |
| E78-CA-03 | `PropositionVitrine`, routes privées fermées, 2..6 choix/une solution ; tests domaine/API et éditeur Pro, salarié sans accès aux actions. Aucun média inventé. |
| E78-CA-04 | Approbation puis installation puis contrôle de versions exactes ; changement invalide la préparation. Tests PostgreSQL et recettes Pro/Animation/ERP. |
| E78-CA-05 | `vitrine=<stepId>` dans accès/inscription/reprise ; courriel limité aux cibles de la définition, QR public sans solution/token. Tests cible, courriel et kit. |
| E78-CA-06 | Période/phase serveur relues sous coordination ; suspension ferme réponses et passages, conflit 409. Tests domaine/PostgreSQL/API et Live suspendu. |
| E78-CA-07 | `SUBMIT_ANSWER` / `SINGLE_CHOICE`, résultats `INTRUDER_FOUND`/`INTRUDER_NOT_FOUND` ; revue/modifier/annuler sans écriture prouvés au navigateur. |
| E78-CA-08 | Unicités PostgreSQL, deux clés concurrentes, rejeu même reçu après fin, commande incertaine conservée. Tests SQL et navigateurs Live/Pro/Animation/ERP. |
| E78-CA-09 | Brouillons par participation/définition/vitrine, pages annulées ou ignorées si obsolètes ; relecture courante après reçu ancien. Recettes réseau/identité/version. |
| E78-CA-10 | Même commerce, réponse/passage dans les deux ordres, mauvaise réponse non qualifiante, une chance au seuil. Tests domaine/SQL ; PIN E78 transmet cible et versions au composant commun. |
| E78-CA-11 | Écritures fermées dès demande de clôture, lots bornés, rollback/checkpoint/restauration et révélation effective. Test de démo étendu au tirage/remise externe ; autres dotations non revendiquées comme recette E78. |
| E78-CA-12 | Préparation filtrée avant LIMIT, enrichissements groupés, pages bornées en octets sans saut, compteurs datés et curseurs signés. Recettes pagination et N/10N/maximum exécutées ; capacité privée encore non mesurée. |
| E78-CA-13 | Suspension UUID distincte de la révision globale ; contrôle concurrent périmé refusé puis relecture explicite, premier constat conservé, reprise à dernière révision, ancien cycle refusé. Contenu/dispositif/K/mode/dates figés. Tests domaine/SQL et exploitation UI. |
| E78-CA-14 | Droits/session courants dans transaction, suivi seul accepté, clôture humaine réautorisée sous verrou ; projections publiques sans solution, erreurs bornées et kit séparé. Tests API/SQL/kit et contrats. |
| E78-CA-15 | Recettes navigateur 320/390/1280, focus, radios, cibles tactiles, annulation et erreurs. Captures inspectées ; pas de recette avec lecteur d’écran humain revendiquée. |
| E78-CA-16 | Suites ciblées, architectures, consommateurs, démo/restauration et mesures N/10N distinctes. Résultats et réserves de campagne ci-dessous ; aucun succès déduit d’un simple import. |

## Preuves exécutées et rapports

Bases du travail : Projet `da50bb3`, backend `9805eec3`, Marketplace `d2b637f`,
Animation `d5c045c`, Pro `8453252c`. Les documents E78 déjà présents avant la
demande sont préservés. Les artefacts locaux sont ignorés par Git ; ils décrivent
un arbre de travail, sans prétendre correspondre à un commit E78 publié.

Backend, via `py scripts/validation/test_isolated.py` et PostgreSQL jetable local :

- **113 tests ciblés et 743 contrôles d’architecture/recensement réussis** dans
  le dernier passage élargi : **861 succès, quatre échecs de doubles historiques**,
  quatre avertissements de dépréciation, 74,63 s ; rapport
  `.artifacts/e78-replay-20261117T000803Z.xml`. Il inclut aussi les quatre tests
  PostgreSQL communs des dotations et cinq tests applicatifs coffrets.
  Les quatre échecs coffrets sont reproduits à l'identique sur `9805eec3` dans
  `tmp/replies-baseline-20261116/tmp/e78-tous-lots-baseline-20261117.xml` : le double
  utilisait encore les anciennes écritures exhaustives de population/gel.
  Ses ports sont alignés sur l'en-tête et les lots courants, avec vérification
  des membres et des comptes ; **les cinq tests coffrets repassent en 6,67 s**,
  sans modifier leurs assertions ni le produit, rapport
  `.artifacts/e78-coffrets-ports-final-20261117.xml`. Ce résultat est un rejeu
  séparé ; les 865 cas ne sont pas présentés comme une passe unique verte.
  Le passage précédent de 855 succès reste dans `.artifacts/e78-replay-20261116T233449Z.xml`.
  Le précédent passage de 107 tests est conservé dans `.artifacts/e78-focused-verified.xml` :
  domaine/SQL/API E78, progression Passeport, cible courriel, kit, PIN Animation
  et salariés. Cela inclut conflit entre deux contrôles concurrents puis relecture,
  premier constat conservé, ancien cycle, révocation pendant l’attente du verrou,
  garde d’origine avant token et conservation refusée pendant la clôture.
  Les derniers passages ajoutent les pages UTF-8/curseurs multi-communes et deux incidents
  du même cycle : le contrôle du premier ne couvre pas le second, qui bloque la reprise.
  Contrôles d’architecture via la commande obligatoire du guide backend ;
  passage antérieur conservé dans `.artifacts/e78-architecture-verified.xml`.
- **17 tests API et pagination réussis** après la dernière revue, rapport
  `.artifacts/e78-page-cursors-final.xml` : champs privés par défaut inclus dans
  le budget UTF-8, 100 brouillons parcourus sans omission, curseurs de préparation
  et de bilan bornés même avec 100 communes ERP. Le défaut était reproduit sur
  les deux routes avant correction ; l’empreinte du périmètre conserve le refus
  d’un curseur après changement des habilitations.
- Dossier d'exploitation : le test aux bornes a reproduit **1 328 516 octets**
  avec 100 incidents, 100 commerces et textes UTF-8 maximaux, rapport
  `.artifacts/e78-incidents-budget-before-20261117.xml`. La borne technique de
  dix incidents par suspension garde la projection sous 256 000 octets dans
  le dernier passage ; les constats privés complets restent conservés.
- Contrats : E41 **1 197 chemins**, E42 **91 chemins** ; les OpenAPI embarqués
  sont générés depuis le même runtime isolé. **120 exports moteur conformes**
  dans chaque consommateur. Rapport backend `.artifacts/e78-contracts.log`.
- ERP : `node tests/browser/vitrines-erp.cjs`, **6 scénarios réussis**, 320/1280,
  fuseau navigateur Los Angeles, contrôles droits/revue/CSRF/reçu courant,
  cibles sur deux pages, restauration et checkpoint. La dernière passe vérifie
  aussi la conservation de la décision pendant un conflit, le verrouillage des
  filtres et de la pagination pendant la revue, le retour du focus et les textes
  agrandis à 200 %. Rapport/captures `localeo-backend/tmp/vitrines-erp-g9YXLC/`.

Consommateurs :

- Marketplace : `npm run test:security`, **301 réussis** sur la première passe.
  `node scripts/run-visual-tests.cjs tests/visual/e78-vitrines.spec.cjs --port 8179 --workers=1` :
  **5 réussis** dans la dernière passe, incluant PIN ciblé sans réponse consommée,
  textes aux bornes à 320 px et polices effectivement doublées ; rapport
  `test-results/visual-runs/2026-11-16T23-47-04-844Z-C4itkh/`.
  La première recette de texte agrandi a reproduit un lien « Voir ce commerce »
  de 19 px de haut ; le style commun lui donne désormais une cible d'au moins
  44 px. Les cinq scénarios passent après correction, puis le cas agrandi seul
  repasse avec une capture de confirmation inspectée dans
  `test-results/visual-runs/2026-11-16T23-48-56-850Z-Gh4S9s/`.
- Pro : **646 tests dans les 89 fichiers source et 5 tests de configuration
  réussis**, aucun skip (`vitest run --dir src --maxWorkers=2`, puis `--dir config`).
  Rapports `test-results/e78-unit-src-final.log` et `e78-config-final.log`.
  La découverte initiale globale, très lente dans les répertoires temporaires,
  a été arrêtée puis remplacée par cette sélection complète des tests applicatifs.
  Build isolé réussi ; **5 recettes navigateur**
  à 320/390/1280, invitation et fiche, attestation, reçu ancien/état courant,
  contenu salarié masqué. Rapports `test-results/results.json` et
  `tmp/quality-build-R2laXw/`.
  Après revue UX, **104 tests ciblés dans neuf fichiers réussis** : navigation
  SPA/navigateur, reprise de la même intention, mémoire privée bornée, purge à
  l’invalidation de session, composant E78 et pages hôtes. Build Pro réussi et
  **9 scénarios navigateur réussis**, dont retour natif, reprise après 503 et
  textes à 200 %. Quatre tests DOM écartent les réponses tardives de lecture,
  reçu et mutation après purge de session, avant même le démontage du composant.
  Rapports `tmp/e78-ui-final-20261117T000737Z/{unit.log,build.log,browser-02/report.json}`.
- Animation : **354 tests réussis**, aucun skip, types/lint et build isolé réussis ; **11 scénarios navigateur**
  à 320/1280, correction, contrôle, pagination, incident/reprise/clôture,
  état incertain, ancien reçu, droits retirés et réponse tardive. Rapport
  `tmp/e78-vitrines-browser-mR8iLg/report.json`.
  Après correction du retour du focus, **15 tests ciblés et 13 scénarios
  navigateur réussis**, types/lint/build isolé réussis ; textes à 200 % mesurés.
  Rapports `tmp/e78-ui-corrections-20261117/` et
  `tmp/e78-vitrines-browser-r2JNmk/report.json`.

Les dernières recettes navigateur utilisent Chromium et des API synthétiques.
L'agrandissement est appliqué par CSS et contrôlé par les tailles calculées,
sans revendiquer une recette sur appareil physique ni avec lecteur d'écran humain.
La revue UX indépendante finale ne relève plus de défaut concret sur les
corrections de navigation/reprise/purge Pro, focus Animation et décision ERP ;
elle s'appuie sur le code, les tests et les captures, sans les réexécuter.

La [checklist ERP-UX](../../architecture/transverse/conventions-backoffice.md#ux-des-pages-de-gestion-erp)
est appliquée au parcours E78 :

| Règles | Preuves de la recette ERP et limites |
| --- | --- |
| 01/02/03/05 | Console de dossier nommé avec commune, organisation et état ; actions près de leur cible, consultation séparée des décisions ; préparation/exploitation/lecture à 1280 et 320 px. Recherche des homonymes du sélecteur commun non rejouée. |
| 04/11 | Liste bornée à 25 et sélection de 26 commerces sur deux pages ; pagination protégée pendant revue, états/actions issus des DTO. Parcours complet des curseurs externes et participants non exercé par ces six cas ; SQL et volumétrie vérifiés séparément. |
| 06/07/08/09 | Annulation sans écriture et retour du focus ; motif conservé après 409, abandon/relecture explicites ; CSRF/idempotence, reçu ancien puis état courant, participants vides et expiration. Renvoi exact après 404, 403 tardif et réponse tardive après expiration ne sont pas revendiqués par cette recette ERP. |
| 10/12 | Socle ERP partagé, longs textes, polices calculées ×2, boutons E78 d'au moins 44 px et captures inspectées ; guides et bilan mis à jour. ERP à 390 px, lecteur d'écran humain et appareil physique non rejoués. |

Démo ciblée finale : **4 scénarios réussis en 174,09 s**, quatre avertissements
connus, rapport backend `tmp/e78-demo-focused-20261117-04/results.xml` et
`console.log`. Trois scénarios E78 étendus : Noël/Pâques avec cinq commerces et
seuil de trois, les deux modes de passage, préparation incomplète/contrôle
obsolète, seuil atteint/impossible, salarié activé puis révoqué, réponses et
passages dans les deux ordres, deux communes, annulation et nouveau brouillon
sans transfert. La clôture commune refuse le gel partiel puis accepte la même
audience complète. Le quatrième scénario historique vérifie génération,
restauration, rappels et rejeux avec les mêmes délais SQL avant/après transaction.
La **campagne canonique fraîche passe ses 14 cas en 771,59 s**, zéro échec ni
skip, onze avertissements SQLAlchemy de réflexion. Rapports
`tmp/e78-demo-20261117-03/results.xml` et `tmp/e78-demo-20261117-03-console.log`.
Elle inclut le cycle complet dump/install/restore, les échecs de reset simulés et
les changements de schéma ; les corrections des fixtures historiques sont donc
rejouées dans la suite intégrale.

Scénario minimal antérieur : **1 scénario complet réussi**, rapport backend
`tmp/e78-demo-focused-20261117-03/results.xml` (68,70 s). Création/préparation et
publication réelles, bonne et mauvaise réponse, transfert/restauration des huit
tables, rétablissement, clôture en trois lots de taille 1, audience d’un seul
éligible, tirage LIBRE/EXTERNE et remise déclarée, reçus rejoués. Aucun envoi de
gain email/SMS exécuté. Les trois dotations ne sont pas déclarées qualifiées par
cette seule preuve. Unitaires helper/runner : **37 réussis** ; registre démo et
Juste Prix : **27 réussis**.

Documentation : `py scripts/check_guidance.py --changed --all-markdown` :
**17 documents, 590 liens, zéro erreur/avertissement** ;
`py scripts/sync_documentation.py --check-sources` : **151 sources vérifiées**.
`git diff --check` réussit dans chacun des cinq dépôts. Rapports finaux dans
Projet `.artifacts/codex/e78/` : `guidance-final-*`, `sources-final-*` et
`workspace-*`, horodatés en UTC.

Capacité locale, rapports backend `.artifacts/epic78-performance/`, synthèse
finale `synthese-capacite-banc2-20261117.json` avec empreintes des sources :

| Participants / vitrines | Lecture personnelle p95 | Première lecture | Clôture complète | Delta RSS clôture |
| --- | --- | --- | --- | --- |
| N = 1 000 / 20 | 22,62 ms | 224,40 ms | 1,79 s | 12,03 Mio |
| 10N = 10 000 / 20 | 25,70 ms | 41,69 ms | 18,31 s | 6,94 Mio |
| Maximum = 10 000 / 100 | 168,47 ms | 111,75 ms | 84,70 s | 9,23 Mio |

Rapports définitifs `n-1000-vitrines-20-20261117T000055.json`,
`n-10000-vitrines-20-20261117T000149.json` et
`n-10000-vitrines-100-20261117T000525.json` ; **3 tests réussis en 282,09 s**,
log `n10n-max100-bootstrap-isole-internes-20261117.log`. Synthèse
`synthese-capacite-20261117.json`. Le ratio p95 10N/N est de **1,136**.
Ces mesures N/10N/maximum précèdent le dernier changement des modes de verrou
du garde HTTP ; elles ne sont pas présentées comme rejouées après ce changement.
Lecture : **8 SQL et 7 objets ORM** constants ; pages de 7 884 octets à 20 vitrines,
maximum **245 780 octets**, pic Python **14 907 391 octets**, delta RSS requête
maximal **7 520 256 octets**. Le maximum contient un million de réponses réelles.
Latences et allocations sont mesurées séparément ; douze lectures par taille,
caches disque non purgés. La première lecture n'est donc pas une preuve à froid.

Chaque clôture persiste ses audits, actualise les statistiques et crée réellement
**1 000 / 10 000 / 10 000 notifications Live** ; RSS échantillonné toutes les 20 ms.
Les plans `ANALYZE BUFFERS` vérifient 20/20/100 accès par `commercants_pkey`,
60/60/300 buffers, sans scan des 10 000 commerces étrangers. Les filtres rare/vide,
pages 25/100 et parcours sans omission sont mesurés.

**15 contrôles fonctionnels réussis en 16,54 s**, rapport
`controle-bearer-verrous-plan-isole-20261117.log` : vrai Bearer/révocations,
verrou transactionnel après commit/rollback/savepoint avec attente concurrente,
plans et clôture réelle. Les rapports `sql-http-bootstrap-isole-20261117.json`
et `sql-http-multiworkers-bootstrap-isole-20261117.json` comptent **8 SQL en
lecture et 20 en écriture, INSERT d'audit inclus**. Le coût de 21 SQL avant
suppression du verrou redondant est conservé dans
`sql-http-audit-21-avant-optimisation-20261117.json`.

Avant l'optimisation des modes de verrou, le contrôle de latence E55 à huit
processus/50 appels par seconde échouait : p99 **118,52 ms** pour un seuil de
100 ms, contre **154,42 ms** sur la base antérieure, elle aussi en échec.
Rapports `guards-quiet.log` et `guards-baseline-final.log` conservés.
Après correction, **les deux variantes E55 passent en 20,97 s**, sans modifier
les seuils. La recette à 400 autorisations mesure **p95 12,35 ms/p99 74,65 ms**
(budgets 30/100 ms), sur 7,989 s ; la saturation autorise exactement **60 des
400 tentatives**, sur 1,502 s. Sa latence p95/p99 est de **39,17/150,41 ms**,
sans appliquer à cette variante les budgets de la recette nominale. Rapport
`banc2-e55-deux-variantes-verrous-optimises-20261117.log` et deux JSON dans
`tmp/e55-impl-limiteur-charge/`, identifiés par ce log.
L'autre échec de cette tentative, l'attente du démarrage du thread dans le test
de purge, est corrigé sans toucher ses assertions opérationnelles : attente
d'amorçage de deux secondes, reprise/verrou inchangés. Le même test
`test_cle_personnelle_purgee_pendant_attente_reprend_une_fois_sans_upgrade`
repasse explicitement dans `banc2-calibration-4ports-20261117.log` ; il ne fait
pas partie du lot des quinze contrôles cité plus haut.

Lanceur reproductible : `scripts/validation/test_vitrines_capacity_isolated.py`.
Il neutralise explicitement dotenv avant les imports parent et Windows spawn,
vérifie son identité dans chaque worker, purge PG* et borne les connexions à la
base jetable et à la boucle locale. Revu indépendamment. Les essais antérieurs
avec effets internes neutralisés, ou avec le seul flag dotenv ignoré par la
version installée, sont conservés et ne constituent pas les mesures finales.

**Charge soutenue non qualifiée.** Le premier smoke TCP isolé avec client séparé
et quatre processus serveur a lancé **391 des 500 requêtes prévues sur 5 secondes** :
313 lectures et 78 écritures, toutes HTTP 200. Les p95 atteignent **3 342/3 376 ms**,
les p99 **4 621/4 153 ms** ; avec le vidage, 48,81 lectures/s et 12,16 écritures/s.
Rapport `charge-mixte-4-workers-5s-20261117T000711.json` ; log
`smoke-tcp-4workers-bootstrap-isole-20261117.log` : **1 succès, 1 échec**.
Le budget SQL est tenu, le débit et les latences ne le sont pas. Fenêtre de
**900 s, pointe 2× pendant 60 s et clôture simultanée non exécutées** après cet
échec. Le maximum échantillonné de neuf attentes de verrou et 0,254 s d'âge de
transaction provient du préchauffage, avant la phase ; pendant celle-ci, une
seule observation montre deux attentes et 10,7 ms. Aucun deadlock ni fichier
temporaire PostgreSQL. Le p95 mesure l'appel HTTP complet, sans lui ajouter le
retard de départ ni le vidage ; le retard de départ proche d'une seconde est
mesuré séparément. Les 391 soumissions sur cinq secondes représentent environ
78,2/s ; les débits lecture/écriture cités plus haut incluent le vidage de 6,412 s.
Temps I/O, attente exacte du pool et graphe des bloqueurs non instrumentés.
La cause résiduelle reste non isolée, sans attribution au seul matériel.

La relecture a identifié un biais du banc court : préchauffage de 20 threads,
puis nouveau pool de 100 threads et clients, sans préchauffage des POST. Le banc
corrigé conserve le même pool et 100 clients HTTP directs, préchauffe GET/POST
avec des participants réservés, enregistre les observations brutes sans secrets
et mesure le CPU sur une fenêtre commune. La revue indépendante ne relève pas
de défaut bloquant de cette méthode ; seuils, authentification et gardes restent
inchangés. Sa première calibration sur une route de contrôle sans SQL échoue
dès le préchauffage : **196 réponses 200 et quatre expirations à 20 s**, avant
toute phase de charge E78. Rapport `prechauffage-echec-20261117T003118.json`, log
`banc2-calibration-tcp4-20261117.log` : **un succès, un échec**. Cela établit un
problème de transport du banc à isoler, sans l'attribuer au domaine E78.
La comparaison avec quatre serveurs sur quatre ports distincts passe ensuite
ses **trois contrôles en 47,06 s** : purge, budget HTTP/Bearer et calibration.
Cette dernière termine **1 000/1 000 requêtes sans SQL** sur cinq secondes,
800 GET/200 POST ; p95 **4,26/4,51 ms**, p99 au plus 5,20 ms. Les 100 clients
et 100 threads sont effectivement utilisés, 25 clients et 250 appels par PID.
CPU serveur/client **2,28/1,97 s** sur la même fenêtre de 5,002 s. Rapport
`calibration-generateur-4-workers-5s-20261117T004021.json`, log
`banc2-calibration-4ports-20261117.log`. Le correctif de nettoyage des processus,
y compris démarrage partiel en échec, est relu indépendamment. La calibration
valide le générateur de charge.

Le passage nominal réel de **30 s sur quatre ports reste en échec** :
**2 562/3 000 requêtes soumises**, 2 050 GET et 512 POST, toutes HTTP 200,
budgets SQL 8/20 tenus. p95 lecture/écriture **3 302,40/1 417,01 ms**, p99
**5 009,58/2 068,13 ms**. Le temps serveur jusqu'aux en-têtes est presque identique
(p95 **3 269,98/1 409,43 ms**) et l'attente de thread p95 inférieure à 2,65 ms ;
l'écart ne provient donc pas principalement de la préparation client du banc.
CPU serveur/générateur **79,64/6,67 s** sur une fenêtre commune de **31,056 s**,
incluant 30,019 s de phase et 1,035 s de vidage. Jusqu'à **56 connexions PostgreSQL
en attente de verrou** et une transaction âgée de **5,447 s** sont observées en
phase ; cet âge n'est pas une durée de verrou. Aucun deadlock ni fichier
temporaire. Rapport `charge-mixte-4-workers-30s-20261117T004210.json`, observations
brutes associées et log `banc2-nominal30s-4ports-20261117.log`.

La capture ciblée suivante localise **1 057 attentes de verrou tuple sur le seul
contrôle global `limitation_lectures_live_controle`**, et aucune attente advisory
ou métier non accordée échantillonnée. Rapport diagnostique
`charge-mixte-4-workers-30s-20261117T004604.json` et log
`banc2-diagnostic-verrous30s-4ports-20261117.log`. Les relevés d'activité et de
verrous sont successifs, pas atomiques ; l'instrumentation amplifie la charge
et ses latences ne sont pas une référence de capacité. La revue indépendante
confirme que le garde d'origine modifie le compteur global sous `FOR UPDATE`,
en opposition avec le `FOR SHARE` du garde personnel. Le chemin d'origine déjà
allouée passe à `FOR NO KEY UPDATE` et le chemin personnel existant à
`FOR KEY SHARE`, compatibles entre eux ; le compteur global reste exact entre
origines. Politique, purge et allocation restent sous `FOR UPDATE`. La clé est
relue, l'horloge suit le verrou ; une clé disparue provoque rollback puis une
seule reprise exclusive. Aucun changement de politique, de seuil ou de domaine.
La revue indépendante couvre tous les writers, les décisions personnelles
indépendantes du compteur global et l'absence d'upgrade. **21 tests fonctionnels
passent en 40,35 s** (`banc2-compatibilite-verrous-fonctionnel-20261117.log`),
puis la preuve renforcée de **quatre origines distinctes**
face au même plafond global repasse : somme des compteurs exactement 31.

Ce changement ne suffit pas à qualifier E78 : le nominal réel suivant soumet
**2 192/3 000 requêtes**, 1 754 GET (1 674 HTTP 200 et **80 HTTP 503**) et
438 POST tous HTTP 200. p95 GET/POST **3 930,95/2 299,45 ms**, temps serveur
jusqu'aux en-têtes **3 854,80/2 156,80 ms**, SQL 8/20 ; maximum 55 connexions
en attente et transaction âgée de 5,026 s. Rapport
`charge-mixte-4-workers-30s-20261117T005104.json`, log
`banc2-nominal30s-4ports-verrous-optimises-20261117.log`. La campagne de 900 s
et la pointe ne sont pas lancées après cet échec. La dernière revue confirme
que les sauvegardes clé/contrôle sont déjà groupées : trois instructions SQL,
puis COMMIT. Aucune suppression simple et sûre n'est identifiée ; la relecture
fraîche après attente protège notamment une clé créée pendant cette attente.
Une fusion exige un protocole supplémentaire et des preuves dédiées ; elle
n'est pas entreprise comme une optimisation spéculative dans ce lot.
Le graphe détaillé précède le changement de modes ; aucune cause unique n'est
affirmée pour la contention résiduelle du dernier nominal.

Limites : Windows local quatre cœurs/huit threads, client/serveurs/PostgreSQL
sur la même machine, une origine NAT pour les 100 clients de transport, politique de garde
de laboratoire documentée sans changement des limites produit. PostgreSQL 55451
conserve `fsync=on`, `synchronous_commit=on`, `full_page_writes=on`, 128 Mio de
`shared_buffers` et `max_connections=100`, relevés hors phase sans changement
dans `reglages-postgres-20261117.json`. Le corpus étranger
contient 100 communes, 100 animations et 10 000 commerces ; réponses étrangères
et versions historiques non peuplées. Capacité privée ERP/Pro/Animation,
publication et exports non mesurés. Le premier arrêt du PG 55451 est conservé
dans `arret-postgres-20261117.json` ; après les reprises du banc, son arrêt final
est vérifié dans `arret-postgres-banc2-20261117.json`. Les quatre derniers PID
serveur sont absents et leurs écoutes fermées, rapport
`controle-workers-tcp-banc2-20261117.json`. Aucune charge ni serveur de recette
ne reste actif. La démo complète est réussie ; ses deux
clusters jetables 55449/55450 sont arrêtés, ports libres. Son état final vérifié
est un builder vide et le modèle E78 inactif.

## Réserves et mise en service

La campagne backend élargie finale intermédiaire a produit **2 260 succès et
62 échecs** (`.artifacts/e78-backend-final.xml`, 571 s). La comparaison des
identifiants exacts à `9805eec3` retrouve **55 échecs identiques** ; les sept
nouveaux échecs ont été corrigés puis rejoués avec succès dans les 107 tests :
six doubles de résolution de progression attendaient la ville dans le contrat
du service et une route manquait encore sa garde d’origine lors du chargement
de cette campagne. Aucune assertion affaiblie. Le détail comparatif est dans
Projet `.artifacts/codex/e78/failure-comparison.json`. La suite globale n’est donc
pas annoncée verte. Un autre échec d’attestation (fixture sans `definition.type`)
est reproduit séparément sur la base antérieure, sans correction hors périmètre.

La première campagne avait aussi révélé une liste de moteurs attendue et des
permissions ERP génériques élargies à tort ; corrigées. Les erreurs initiales
de prérequis `pg_trgm` ont été résolues dans la seule base jetable.

L’activation reste bloquée par la qualification de charge soutenue. Le budget SQL se mesure avec authentification et
limiteurs communs inclus ; les chiffres de service seuls ne qualifient pas la
charge HTTP. Le smoke conserve les 100 clients TCP et le garde commun ;
ils partagent une origine NAT locale, sans contournement des adresses IP.
Les lectures tournent sur 100 participants et les écritures sur un pool de
2 000 identités Bearer pour créer de nouvelles réponses ; 100 autres participants
sont réservés au préchauffage. Ce sont 100 requêtes simultanées au maximum,
sans prétendre reproduire exactement 100 identités participantes fixes.
La campagne longue attendue (15 minutes, 80 lectures/s, 20 écritures/s et pointe 2×)
reste distincte des preuves produites. Les dotations sont vérifiées par composition :
gel E78 puis tirage/remise externe dans la démo, cinq cas applicatifs coffrets et
quatre cas PostgreSQL communs externe/numérique/trois natures. Cela ne constitue
pas trois recettes E78 de bout en bout. Aucun pilote externe n’est ajouté comme
condition de clôture implicite.

Impacts : aucun nouveau tarif, quota commercial, secret, délai de conservation ou
fournisseur IA ; dotations existantes réutilisées. Tables E78 inscrites au registre
de démonstration et à la conservation, sans transfert automatique vers une autre
édition. Aucun fichier de données de démo ou secret déplacé dans Projet.

Livraison : migration additive et backend inactif, contrats puis trois frontends
compatibles, contrôles et activation explicite après qualification. En incident,
conserver données et checkpoint ; suspendre l’édition, rétablir le même dispositif
ou annuler. Les [instructions ops](../../exploitation/technique/configurer-epic-73.md#jeu-des-vitrines-e78--modèle-standard-inactif)
décrivent le batch et la console.

## Publication Git et schéma Test — 17 novembre 2026

Sur demande explicite de commit, push et mise à jour de la base Test, les quatre
applications sont committées et poussées sur `origin/main` :

| Dépôt | Commit publié |
| --- | --- |
| Backend | `146b578a8866edf8b810fdd1b349ba43db076b6c` |
| Animation | `a4f45e931e531740d2f41196cb29f3e3c5bcb29d` |
| Pro | `24b1deb92e725e3640795333b542ef6b041cfed6` |
| Marketplace | `2d22b79d4bcf5b7ef2b49c80153b547326f1eac7` |

La documentation est publiée dans le commit portant ce bilan. Les arbres
applicatifs sont propres après push. Lors de la préparation, le contrôle de
l'index détecte des espaces terminaux dans la nouvelle SQL v323 et une ligne
vide finale dans le DTO E78 ; ces deux nettoyages de présentation ne modifient
aucun comportement ni contrat. La SQL nettoyée est celle exécutée sur Test.

Cible : environnement **Test partagé**, configuration explicite `.env.test`,
isolée de `.env.local` et comparée aux cibles Production/Démo avant écriture.
La base passe de **322 à 323**, via le runner canonique
`scripts/database/apply_migrations.py` : seule `v323_jeu_vitrines.sql` était
en attente. Les données et les profils installés sont conservés.

Sauvegarde préalable au format custom : **82 854 160 octets**, archive relue par
`pg_restore --list`, empreinte SHA-256
`9c5bc51310976f403bffd5b007ee953dc55e15f4e08c1d960835b6ae0304b3e4`.
Le reçu et l'archive restent dans le stockage opérateur privé du backend :
`demonstrations/prive/operations/e78-schema-20261117T064917Z/receipt.json` et
`before.dump`. La lisibilité de l'archive est vérifiée, sans revendiquer sa
restauration sur une autre cible pendant cette opération.

Après migration : **huit tables E78 présentes**, contraintes validées, checksum
v323 conforme et **aucune migration restante** au dry-run. Empreinte de la SQL :
`8d969bc7c5643a660d3eddbee25139399b890cdd4e7dbf6714c8923bf62d4c5e`.
Le catalogue contient `JEU_VITRINES`, version 1, **actif=false**. La qualification
de charge reste ouverte ; cette mise à jour de schéma ne vaut ni activation du
jeu ni recette applicative distante.

## Évolution du 17 novembre 2026 — préparation guidée

**E78-EVO-PREPARATION-UX**, critères [PU-01 à PU-08](parcours-regles.md#évolution-du-17-novembre-2026--préparation-guidée).
Implémentation locale dans Pro et Animation, documentation dans Projet ; bases
respectives `24b1deb`, `3ba1776`, `e45f001`, avec modifications de travail.
Les critères historiques et l’état En cours restent inchangés.

Pro ajoute une section dédiée, la liste paginée des participations acceptées et
le parcours par invitation. Le jeu des vitrines affiche une étape à la fois,
avec navigation libre, revue public/privé, sauvegarde et proposition explicites,
puis installation et attente du contrôle. Les anciens liens restent valides
avec une lecture continue des étapes. Chasse, Juste Prix et autres animations
réemploient leurs missions, produits et kits avec des repères de préparation.

Animation regroupe la page en tâches de l’organisation, attentes des commerçants
et préparations prêtes. Chaque commerce présente les trois états de préparation
et la prochaine tâche avec son acteur. Le contenu privé est dépliable et repris
dans la confirmation. Les compteurs concernent uniquement la page ; aucune
lecture supplémentaire par commerce ni collecte de toutes les pages.

| Critères | Vérification exécutée le 17 novembre | Résultat |
| --- | --- | --- |
| PU-01/02/05/08 | Pro : `npm test -- src/features/animations src/app src/features/perimetres` | **253 tests réussis, 36 fichiers** : listes, pagination, invitations, droits, session, navigation et composants existants. Les erreurs synthétiques de `errorDiagnostics.test.jsx` sont attendues dans cette suite réussie. |
| PU-01 à 04/08 | Pro : `npm run test:e2e -- tests/e2e/e78-vitrines.spec.js --workers=2 --output=tmp/preparation-ux-compact-results` | **14 scénarios réussis**, 320/390/1280 px : entrée dédiée, continuation/focus, sauvegarde explicite, approbation/installation existantes, refus salarié sur les deux accès, retour liste et restauration du brouillon, retour navigateur, commande incertaine et texte 200 % sur le parcours continu. |
| PU-06/07/08 | Animation : `node tests/browser/e78-vitrines.mjs` | **16 scénarios réussis**, rapport `tmp/e78-vitrines-browser-GrJ93B/report.json` : répartition 2 tâches / 2 attentes / 1 prête, acteur et motif, contenu privé, approbation/contrôle, pagination, droits, contexte tardif, conflit, reçu et renvoi explicite. Rendus 320/390/1280 px, texte 200 % sur 320 px. |
| PU-06/07/08 et préservation | Animation : `pnpm typecheck`, `pnpm lint`, `pnpm test`, `node scripts/build-check.mjs` | Types, lint et build réussis ; **354 tests réussis, aucun échec ou skip**. Build isolé `tmp/quality-build-ptwkwH`. Avertissement de taille de bundle conservé. |
| Code livré Pro | `node scripts/build-check.mjs` après l’itération visuelle | **Build réussi**, sortie isolée `tmp/quality-build-T40RfL`. Avertissement d’import dynamique/statique de ValidationHistory conservé. |
| Documentation | `py scripts/check_guidance.py`, `py scripts/check_guidance.py --changed --all-markdown`, `py scripts/sync_documentation.py --check-sources` | Contrôles réussis, aucun lien local en erreur ; **151 sources exportées vérifiées**. Le lanceur `py` est utilisé car l’alias `python` du shell renvoie au Microsoft Store. |

Les captures Pro d’entrée et de revue ainsi que les captures Animation de la
répartition ont été inspectées sur bureau/mobile. Une itération a réduit
l’espace avant les étapes Pro. La recette précédente de 14 scénarios et son
rapport sont conservés sous `tmp/preparation-guided-acceptance-results/` ; les
captures des premières recettes de 12 scénarios sont aussi conservées dans les
dossiers de test. Le dernier rapport Pro est copié auprès des captures finales.

La revue indépendante à partir de la description a demandé trois vérifications :
perte de saisie lors du démontage, première page sans participation acceptée et
validation native de champs masqués. Le retour dédié avec annulation/confirmation
et restauration est couvert par la recette ; le cas page vide/page suivante par
le test `AnimationPreparationPage.test.jsx`. Aucun `required`/`pattern` ni formulaire
HTML soumis n’est ajouté : le brouillon incomplet et les refus métier serveur
restent couverts par les tests de préparation existants. Cette revue n’a pas pu
inspecter les sources directement ; la revue de code et des captures a été faite
par l’agent principal.

Sans impact sur les contrats/API, le domaine, l’ERP, Live, les schémas, les
migrations et le générateur : les producteurs existants sont réutilisés, aucun
champ ni droit n’est ajouté. Aucun test backend/démo ou charge n’est relancé pour
cette présentation. Les preuves sont locales et synthétiques ; recette sur
appareil réel, déploiement, activation et qualification de capacité restent
distincts. Ces preuves précèdent les commits et push demandés ensuite le
17 novembre 2026 dans les dépôts concernés. Aucun déploiement n’est réalisé.

## Correctif du 22 novembre 2026 — clarifier la préparation Commerçant

Plan « Clarifier la préparation des animations dans Localeo Commerçant »,
critères [PU-01 à PU-05](parcours-regles.md#évolution-du-17-novembre-2026--préparation-guidée).
Bases propres : Backend `640d2cc2`, Commerçant `294393f`, Projet `518e426`.
Les preuves ci-dessous portent sur ces bases avec les modifications du correctif.
Code committé et poussé : Backend `8c74b666`, Commerçant `327e500`.

La liste précédente filtrait les invitations déjà paginées et ne donnait pas
leur avancement réel. Deux lectures dédiées exposent désormais le même résumé
de préparation avec les métadonnées actuelles : filtre de cycle de vie en SQL
avant pagination, 50 lignes par défaut, 100 au maximum, chargements groupés.
Une date passée ne déplace pas une animation ouverte dans l’historique.
Chaque ligne présente état, prochaine action et acteur. Le détail sépare étape
consultée et étape attendue, maintient les éditeurs montés et relit les faits
après une commande confirmée. Il masque les repères d’état actuel pendant une
lecture ou un résultat incertain. Les retours de chargement et validation de
Commerçant sont harmonisés à leur emplacement existant.

La revue indépendante a identifié l’annulation réelle d’une animation : elle
annule aussi la demande acceptée. Le filtre inclut cette ancienne acceptation
dans l’historique, sans inclure une invitation jamais acceptée. Le test SQL
exécute la transition de domaine et vérifie liste, détail et refus. La recette
clavier a aussi détecté un focus demandé avant le commit de l’étape URL ; il
attend désormais son affichage effectif. Les assertions de focus restent actives.
Sur mobile, le détail Vitrines évite de répéter le rappel de prochaine action
déjà présenté dans le résumé serveur.

| Périmètre | Contrôle exécuté | Résultat |
| --- | --- | --- |
| Backend, projection/API/architecture | Lanceur isolé : nouveaux tests `test_preparations_commercant*`, API de suivi existante, `tests/architecture`, classes dédiées et couverture des use cases | **800 réussis** ; après ajout de la borne repository 100, les **5 tests SQL** sont repassés. Filtre avant pagination, résumé partagé, toutes familles de jeu, date passée, isolation, refus et absence de contenu privé. |
| Frontière salariés | Même lanceur avec `tests/api/test_salaries_e72_cloture.py`, nouveaux tests et suivi existant | **156 réussis**, dont refus des nouvelles routes au salarié. 113 avertissements `datetime.utcnow` dans les tests existants, sans échec. |
| Lectures bornées | Tests repository SQL réels sur SQLite en mémoire | **10 requêtes pour 1 ou 50 lignes** ; limite 100 indépendante de HTTP, pas de contenu produit privé ni secret QR sélectionné. Aucune preuve PostgreSQL revendiquée. |
| Commerçant, composants et contrats | `npx vitest run` sur page de préparation, Vitrines, guards, Juste Prix, kit, normalisation, validation et deux fichiers de contrats API, `--maxWorkers=2` | **168 tests réussis, 18 fichiers**. Puis **33 tests de contrats** réussis après ajout des deux nouvelles lectures et **35 tests page/Vitrines** réussis après la dernière simplification visuelle. |
| Parcours préparation | `npm run test:e2e -- tests/e2e/animation-preparation-guided.spec.js tests/e2e/e78-vitrines.spec.js --workers=2` | **19 scénarios réussis** : 320/390/1280 px, navigation clavier/focus, retour paginé, historique, accès direct/refus, brouillons, reçu incertain, absence de double commande et de confirmation au téléchargement. Axe sans violation sur liste et détail ; texte 200 % avec débordement contrôlé. |
| Retours communs et sécurité scanner | `tests/e2e/validation-merchant-ux.spec.js` et `tests/e2e/validation-security.spec.js`, même commande Playwright | **15 scénarios réussis** : coffret, confirmation, refus avant ouverture, conflit, origine interdite, relecture échouée puis reprise sans rejouer, secret de réinitialisation. Le test de couleur d’avertissement suit la nouvelle palette ; ses assertions de refus et d’absence de commande restent identiques. |
| Build et contrat | `node scripts/build-check.mjs`, `py -3.14 scripts/export-openapi.py` | Dernier build isolé réussi : `tmp/quality-build-Qt0S3L` ; contrat embarqué régénéré hors réseau depuis `8c74b666`, **1216 routes**. Avertissement d’import statique/dynamique `ValidationHistory` conservé. Aucun script `lint` ou `typecheck` n’est défini dans Commerçant. |
| Guide Commerçant | Capture Chromium synthétique, génération/rendu PDF, `guide:sync`, `guide:check`, capture `--check-guide` | **12 pages et 12 captures** ; toutes les pages inspectées, détails des pages 7/8 relus. Quatre images affectées renouvelées. PDF embarqué identique ; HTTP 200, clavier et Axe sans violation à 390/1440 px, même avec assistance HTTP 503. |
| Documentation | `py -3.14 scripts/check_guidance.py --changed --all-markdown`, `py -3.14 scripts/sync_documentation.py --check-sources` | Liens sans erreur ; **155 sources exportées vérifiées**. Contrats canoniques E41/E42 régénérés par leurs générateurs officiels. |

La suite globale `npm test` a été tentée puis interrompue : un timeout a été
observé dans `ValidationHistory.test.jsx`, et le fichier Node
`tests/release-receipt.test.cjs` est également collecté par Vitest comme fichier
sans test. Ces fichiers et la configuration de sélection sont inchangés ; la
cause du timeout n’est pas qualifiée ici. La commande prévue pour le reçu,
`npm run test:release-receipt`, réussit ses **2 tests Node**. Une seconde
sélection large n’a pas abouti non plus avant interruption. Aucun succès global
n’est annoncé ; les suites ciblées ci-dessus sont terminées et réussies.

Les rapports, captures et rendus de travail restent dans le dépôt applicatif :
`test-results/`, `tmp/preparation-guided/`, `tmp/preparation-guide/pdf-pages/`
et `tmp/guide-refresh-merchant-capture/`. Les sources et illustrations publiées
du guide restent canoniques dans Projet, avec une copie PDF embarquée dans Pro.

Sans migration, nouvelle configuration ou changement des commandes métier.
Les données et commandes du générateur de démonstration sont inchangées ; ses
fixtures de recette UI ont été adaptées. Sans impact sur Marketplace/Live,
Animation ou son guide : leurs écrans et procédures ne changent pas. Le backend
doit être livré avant le nouveau consommateur Commerçant. Les contrôles sont
locaux et synthétiques, sans base PostgreSQL ni appareil physique ; aucun
déploiement ni changement de données réelles n’est réalisé. Les commits et
push sont séparés dans Backend, Commerçant et Projet conformément à la demande.

### Complément du 22 novembre — confirmation et accueil Pro

Le signalement concerne une déclaration **Je suis prêt**, suivie d’un affichage
« En cours » et d’une étape 3 sans nouvelle validation possible. Dans l’arbre
local, le statut de l’animation et l’étape courante pouvaient entretenir cette
ambiguïté ; une déclaration disparaissait aussi de l’affichage lorsque le suivi
était ensuite désactivé. Trois nouveaux tests ont d’abord échoué sur ces
affichages, avant correction. Le cas distant exact n’a pas été consulté.

Le détail et la liste identifient maintenant **Animation : En cours** et
**Préparation : confirmée**, avec date de déclaration. Une finalisation
confirmée est **Terminée**, sans « Étape actuelle ». Un prérequis encore
incomplet conserve sa priorité et sa prochaine action, avec la déclaration
antérieure visible. La disponibilité de **Je suis prêt** reste décidée par le
serveur ; une indisponibilité est expliquée sans contourner ses règles.

L’accueil ne sélectionne plus les seules déclarations possibles parmi les
invitations. Son bloc dédié sépare les actions du commerçant et les attentes
de l’organisateur, par pages de cinq, depuis le filtre serveur `triage`.
L’ordre et l’acteur de la projection sont communs au résumé et à la sélection
SQL ; compte et filtre précèdent la pagination. La revue indépendante a relevé
la conversion des dates naïves selon le fuseau PostgreSQL : elles sont désormais
interprétées en UTC comme dans le domaine, les offsets explicites étant préservés.

Versions de référence de ce complément : Backend `b7edf6e4`, Commerçant
`643a90a4`, Projet `b8b62180`, avec modifications locales. Les arbres comportent
aussi des travaux parallèles de pilotage et d’iconographie, préservés ; les
preuves ci-dessous ne constituent pas leur recette exhaustive.

Preuves déjà terminées :

- Backend, lanceur isolé : **880 tests réussis, aucun échec, erreur ou skip**,
  dont 108 ciblés et 772 contrôles d’architecture/recensement. Les 75 cas
  repository couvrent SQLite et PostgreSQL local (38/37), avec fuseau de session
  `Europe/Paris`, dates naïves/offsets, configuration effective, révisions et
  neutralisations QR, sélection au-delà de cinquante animations, isolation et
  filtre/compte avant pagination. Rapport backend :
  `.artifacts/preparation-triage-pg-tu1upsam/pytest.xml` ; `result.json` confirme
  `exit_code=0` et `stopped=true`. Cluster PostgreSQL 11 jetable port 33378 arrêté,
  sans contact avec une base installée. Cette preuve ne qualifie pas une charge
  soutenue en production.
- Composants, guidage, kit, cache et accueil : **74 tests réussis dans 7 fichiers**,
  avec `node node_modules/vitest/vitest.mjs run --pool=threads --maxWorkers=1 --testTimeout=20000`
  et sélection de `AnimationPreparationPage`, `AnimationKitSection`,
  `VitrinePreparation`, `preparationContracts`, `preparationQueries`,
  `MerchantPreparationsHome` et `MerchantHomePage`. Le délai de 20 secondes est
  propre à cette exécution locale ; la configuration des tests reste inchangée.
- Parcours `preparation-status.spec.js` et `suivi-animation.spec.js` : **8 réussis**,
  à 390/1280 px, clavier et texte 200 %, confirmation persistante après retour,
  absence de double commande, téléchargement sans déclaration, sans suivi,
  actualisation échouée puis reprise et révocation. Zéro violation Axe sur le
  détail avec texte agrandi. Port isolé 4183 et build distinct pour
  ne pas réutiliser le serveur 4173 d’une autre tâche.
- Contrat consommé : **33 tests réussis** après export isolé de **1222 routes**.
  Contrat E41 régénéré par son générateur officiel ; aucune nouvelle structure
  de réponse ni nouvelle commande. Les autres consommateurs gardent leurs contrats.
- Guide Commerçant : **12 pages rendues et relues**, captures affectées
  actualisées, copie embarquée synchronisée. Navigation, clavier, PDF HTTP 200
  identique, assistance HTTP 503, absence de débordement et Axe vérifiés à
  390/1440 px. Empreinte canonique/embarquée/servie stable après coédition :
  `c7a4bd22c0e3d9bf7cb7a437045d4278298d9d6a2e618339e83413c2dae501d0`.
- Documentation : contrôle global des guides sans erreur ni avertissement,
  **155 sources exportées vérifiées** ; contrôles ciblés des trois sources
  du guide également réussis.

Rapports et captures Pro : `tmp/preparation-status-reports/`,
`tmp/preparation-status-results-final/`, `tmp/preparations-guide-final-pdf/`,
`tmp/preparations-guide-proof-{before,after}.json` et
`tmp/guide-refresh-merchant-capture/verification.json`. Les essais initiaux ont
rencontré des timeouts de démarrage de workers et des dépassements de cinq
secondes sur cet hôte chargé ; aucun skip ni assertion affaiblie n’a été ajouté.

Sans migration, nouveau paramètre opérateur, réparation de données ou génération
sur un environnement installé. Le guide Animation n’est pas affecté par ce lot,
qui ne change pas ses écrans ni procédures. Backend à livrer avant Pro. Aucun
déploiement manuel n’est effectué pour ce complément.

Publication Git du **22 novembre 2026**, après demande explicite : Backend
`c68e0100` et Commerçant `e27ffec` committés puis poussés sur `origin/main`, dans
cet ordre. La documentation et le guide sont publiés dans un commit Projet
séparé. Seul l’ajout du paramètre généré `triage` est indexé dans les contrats
OpenAPI E41 et Pro ; les exports complets comportent aussi des modifications
de pilotage et de génération étrangères à ce lot, conservées localement.
Les autres travaux locaux Animation, pilotage et iconographie ne sont pas
inclus dans ces commits. Les preuves ci-dessus restent celles de la recette
locale ; aucun résultat de déploiement distant n’est revendiqué.

## Évolution du 26 novembre 2026 — lisibilité de la préparation Pro

[E78-EVO-PREPARATION-LISIBLE](parcours-regles.md#évolution-du-26-novembre-2026--lisibilité-de-la-préparation-pro)
porte sur la fiche guidée dans Commerçant et sa documentation dans Projet.
La recette locale utilise Commerçant `b8f5e47` avec le diff de l’évolution,
Chromium et des API simulées.

| Critère | Réalisation et preuve |
| --- | --- |
| PL-01 | `PreparationOverview` affiche les états serveur, le motif disponible et la prochaine action. Les parcours `preparation-status.spec.js` et `e78-vitrines.spec.js` distinguent correction, approbation, déclaration, installation et contrôle. |
| PL-02 | `PreparationProgress` sépare l’étape à traiter de celle consultée et coche les faits confirmés. La suite navigateur couvre la navigation et l’absence de confirmation au téléchargement. Le test composant vérifie l’historique annulé sans étape active. |
| PL-03 | Les éditeurs, les consignes de mission et le kit utilisent des volets natifs fermés au départ. Les scénarios Vitrines et Juste Prix vérifient l’ouverture, la saisie, le choix de l’intrus et la relecture publique et privée. |
| PL-04 | Les parcours passent par les liens directs et le clavier, avec conservation du brouillon, de l’étape et du focus pendant la relecture. La recette inspecte le détail à 320, 390 et 1 280 px et contrôle le texte agrandi à 320 px. La revue indépendante a identifié deux cas de lectures concurrentes. Les tests d’éditeur couvrent désormais réponse tardive et conflit conservé jusqu’à la vérification explicite. |

Sur demande d’actualisation, la fiche relit le résumé et l’invitation, suivis
pour Vitrines et Juste Prix d’une lecture de l’éditeur déjà autorisé. Les
lectures de liste et leur pagination gardent leur contrat et leur coût.
La préparation et ses commandes restent sous la responsabilité du backend.
Le périmètre utilise les données, droits, migrations, configuration et jeu de
démonstration existants.

Le [guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md)
a deux captures actualisées. Ses 17 pages ont été rendues et relues. La copie
embarquée est identique au PDF canonique, et son accès depuis **Aide et contact**
a été vérifié à 390 et 1 440 px, y compris avec le support indisponible.
Le guide Animation porte sur les gestes de l’organisateur et reste applicable
aux écrans Animation utilisés pour l’approbation et le contrôle.

Exécutions locales du 26 novembre 2026

- Playwright a validé les **42 scénarios** des sept suites `preparation-status`,
  `animation-preparation-guided`, `e78-vitrines`, `juste-prix-product`,
  `suivi-animation`, `animation-kit` et `merchant-guide`. Rapport dans
  `localeo-commercant/tmp/preparation-pro-final-report/results.json`.
- Vitest a validé les **51 tests ciblés** de `VitrinePreparation`,
  `JustePrixProduct` et `AnimationPreparationPage`.
- La suite Vitest complète a validé **773 tests dans 102 fichiers** avec
  `npm test -- --exclude 'tmp/**' --reporter=dot --silent`. Les copies
  temporaires de dépôts dans `tmp` sont exclues de la collecte. Lors du
  passage précédent, lancé en parallèle de Chromium, le scénario salarié
  « Révoquer cet accès » a dépassé son délai de cinq secondes. Les cinq tests
  de son fichier ont réussi isolément avant la dernière exécution complète.
- Le build Vite de recette, `npm run guide:check` et la vérification
  `--check-guide --verify-only` ont réussi. Les 16 destinations du sommaire
  et les 16 liens de retour du PDF ont été vérifiés.
- `scripts/check_guidance.py` et `scripts/sync_documentation.py --check-sources`
  ont validé les liens de Projet et les 155 sources exportées.
