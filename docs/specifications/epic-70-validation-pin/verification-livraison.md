# E70 — Preuves attendues et préparation de livraison

Références : [architecture](architecture-contrats.md), [périmètre V1](README.md),
[34 critères canoniques](../../roadmap/terminees/epic-70-validation-prestation-telephone-client-backlog.md).
Ce document conserve le plan de vérification initial et le bilan d'implémentation
locale du 7 octobre ci-dessous. Aucune recette sur un environnement réel ni
activation du canal n'a été effectuée.

## Clôture sur tests — 2 novembre 2026

**Décision E70-DEC-CLOTURE-TESTS** : à la demande explicite de l'utilisateur,
la clôture repose sur les tests unitaires, d'intégration et fonctionnels. Les
preuves de pilote, d'appareil réel, de fournisseur et d'hébergement ne constituent
plus un préalable à cette clôture. Les **34 critères métier sont conservés** ;
CA-16 est vérifié par les parcours navigateur et la démonstration synthétique,
avec les guides et leur lecteur. Les comptes rendus historiques plus bas restent
datés et ne portent pas le verdict courant.

**Verdict : Terminée**, les 34 critères sont vérifiés sur les preuves ci-dessous.
Aucun commit, push, activation ou déploiement n'est réalisé par cette clôture.
Bases : backend `7f131d3`, Marketplace
`bb8b585`, Pro `78c3237`, Animation `d607cb9`, projet `9204f8a`, complétées
par les différences locales. Les travaux
E72 et E76 préexistants sont préservés et ne constituent pas un lot E70.

### Correctifs et compléments

- **CA-04** : le backend fournit `coffret_instance_id`, référence UUID non
  secrète ; le client l'affiche avant saisie et dans le reçu, distinctement de
  l'identifiant de validation. Le champ optionnel est synchronisé dans les
  contrats E41/E42 et les instantanés Pro/Animation. Aucun nouveau droit.
- **CA-33** : l'audit des refus conserve commerce, cible, parent, animation,
  mode, version, motif et corrélation après rollback et après purge de la
  demande. Les effets métier refusés restent annulés. Le compteur des mauvais
  PIN et son blocage restent persistés, sans doubler la trace de refus.
- La revue indépendante identifie aussi un succès externe écrit avant le commit.
  Le correctif diffère les seuls segments `pin_validation.*` jusqu'au commit
  extérieur, écarte les savepoints annulés et fournit une reprise idempotente
  depuis SQL en cas de panne du fichier après commit. Un test reproduit le faux
  succès avant correction. Il n'est pas annoncé d'atomicité SQL/fichier.
- Les tests PostgreSQL complètent les substitutions, droits courants, incidents,
  blocage global, scan principal/salarié, et réconciliation du moteur réel.
  Pour une chasse, le PIN atteste la présence commerçante ; la réponse au défi
  reste une action distincte du joueur.
- Les migrations réelles **v256/v257** sont appliquées deux fois sur schéma
  pré-E70 puis sur schéma initialisé par ORM : aucun PIN ni activation implicite,
  sessions/droits conservés et validation QR effective après migration.
- Compatibilité du jeu de démonstration, distincte du correctif métier E70 :
  les signataires fictifs de convention utilisent le format structuré du
  représentant légal. Le scénario de finalisation teste aussi le refus sans
  bilan de préparation, puis renseigne RDV/bilan par les commandes normales
  avant `VALIDE`. Aucune règle OnBoard n'est neutralisée, aucun dossier n'est
  finalisé d'office dans le jeu ; l'essai est annulé après vérification.

### Périmètre des preuves

Les fichiers ci-dessous sont relatifs à `localeo-backend`, sauf mention du
frontend. Les suites PostgreSQL utilisent uniquement `127.0.0.1:16472`, rôle
synthétique `audit_test`, base `localeo_audit_test`, avec schémas éphémères.
Le générateur utilise deux clusters jetables distincts, ports 16473/16474.
Les lanceurs interdisent le chargement des `.env` et les transports externes.
Les API des tests navigateur sont simulées ; les assertions d'effets métier
proviennent des tests PostgreSQL. Ces preuves complémentaires ne sont pas
présentées comme un parcours traversant des applications hébergées.

| Lot | Commande / fichiers | Résultat |
| --- | --- | --- |
| I — isolé | `scripts/validation/test_isolated.py`, domaine PIN/session/commerce/conservation, API PIN/ERP/Bon, réauthentification/actions Animation, segments, générateur PIN, architecture/classes/couverture use cases et exploitation/email | **779 réussis**, aucun ignoré, 49,38 s ; 1 avertissement `datetime.utcnow()` de fixture |
| I2 — après correction des segments | Même lanceur, architecture/classes/couverture et audit/API/réauthentification ciblés ; rapports `tmp/e70-final-audit-20261102/isolated-retry.*` | **665 réussis**, aucun ignoré, 34,33 s ; ce lot recoupe I et n'est pas additionné à ses 779 contrôles. Premier lancement : erreur de handle stdin Windows dans un sous-processus Git ; rejeu identique avec stdin `DEVNULL`, aucune assertion modifiée |
| P — PostgreSQL existant | Coffret, Animation, Bon, concurrence, notifications, conservation, salariés/périmètres, moteur et transport interne | **104 réussis**, aucun ignoré : 22 dans le lot audit final et 82 dans le lot intégré final |
| C — compléments intégrés | `tests/security/test_cloture_pin_e70.py` | **31 cas distincts validés**, dont ouverture sans session/transaction, support audité et historique ; un prérequis de fixture v257 manquant a été corrigé puis les 4 cas affectés/renforcés rejoués avec succès |
| A — audit et référence | `tests/security/test_cloture_audit_pin_e70.py`, puis suites Coffret/Animation ; rapports `tmp/e70-final-audit-20261102/postgres.*` | **35 réussis** : 13 nouveaux audit/référence et 22 existants Coffret/Animation, aucun ignoré, 229,01 s. Les 22 existants appartiennent au lot P, sans double comptage |
| M — migrations | `tests/security/test_cloture_migrations_pin_e70.py` | **2 réussis**, aucun ignoré, 40,46 s |
| D — démonstration/restauration | Lanceur temporaire `tmp/e70-final-demo-20261102/run_full.py`, isolation et `RequiredScenarios` du runner canonique, trois modules dataset/lifecycle/reset sur ports 16473/16474 déjà migrés | **10 cas distincts vérifiés** : 9 réussis dans la suite globale (902,47 s), puis le cas de relations corrigé et rejoué avec succès (209,93 s, `relations.xml`). Premier échec : signataire fictif dans l'ancien format ; fixture ensuite rendue déterministe sur le dossier avec préparation active. Les 10 tests unitaires préparation/PIN passent (5,88 s, `unit.xml`). Le cas PIN génération/restauration ciblé a aussi réussi en 120,21 s. La suite globale n'a pas été entièrement rejouée après correction |
| F — client navigateur | Marketplace : `pin-validation-coffret-closure.spec.cjs`, `pin-validation.spec.cjs`, `pin-validation-feedback.spec.cjs`, `pin-validation-bon-feedback.spec.cjs`, configuration `playwright.desktop.config.cjs`, 1 worker | **26 réussis** : 9 nouveaux Coffret (Live/QR/détail, 390/1280 px) et 17 Animation/Bon ; aucun ignoré |
| N — client stockage/transport | Marketplace : `node --test` sur `pin-recovery.test.cjs`, `service-worker.test.cjs`, `analytics-transport.test.cjs`, `request-deadline.test.cjs` | **27 réussis**, aucun ignoré |
| U — Pro unités/contrats | `node node_modules/vitest/vitest.mjs run --config scripts/audits/vitest-e70.config.mjs --maxWorkers=2` | **71 réussis**, 6 fichiers, 44,77 s, aucun ignoré |
| B — Pro navigateur | `node node_modules/@playwright/test/cli.js test tests/e2e/pin-validation.spec.js --workers=1 --output=tmp/e70-closure-pro` | **3 réussis**, 23,3 s : gestion à 390/1280 px et réponse de génération perdue, reload, relecture et remplacement explicite |
| E — ERP navigateur | `node tests/browser/pin-validation-erp.cjs` | Réussi à 390/1280 px : état sans secret, motif, révocation, timeout/relecture et refus Lecteur |
| L — documentation et lecteur | `test_ops_markdown_viewer.py`, `test_documentation_snapshot.py` ; liens, sources et bundle | **34 réussis, 2 ignorés** (création de symlinks non autorisée sur Windows), 69,70 s. Bundle `tmp/e70-cloture-20261102-docs` : 134 exports, 135 entrées distribuées et leurs empreintes vérifiées ; alias ERP `formation/validation-par-pin.md` résolu avec le guide et la reprise d'audit |

Les builds isolés Pro et Marketplace intégrés aux runners navigateur réussissent.
L'avertissement Pro sur l'import statique/dynamique de `ValidationHistory`
reste visible. Les avertissements PostgreSQL sur le cycle FK profils et les
horloges de fixture ne sont pas des scénarios ignorés. Les reproductions avant
correctif CA-04/33 donnent trois échecs attendus ; elles ne sont pas additionnées
aux succès, pas plus que les reprises de fixtures et relances ciblées.

Les lots PostgreSQL finaux représentent **150 cas distincts validés** : P104,
C31, A13 nouveaux et M2. Le rapport `tmp/e70-final-integration-20261102/results.xml`
contient 114 succès et un échec de fixture en 794,38 s ; la vraie migration v257
crée la table SQL-only `preuves_consommation_pin` nécessaire au test d'historique.
Le rapport `ca01-ca12-recheck-v257.xml` prouve ensuite les quatre cas rejoués en
57,99 s (27 autres non sélectionnés, pas ignorés). Les assertions CA-01/12 sont
renforcées ; aucune assertion métier n'est supprimée. Les relances interrompues
avant production d'un rapport final ne servent pas de preuve de succès.

Après reclassement : `check_guidance.py` réussit sur 94 guides et 1 068 liens ;
le contrôle des documents modifiés réussit sur 24 guides et 564 liens, sans
erreur ni avertissement. Les 134 sources exportées, le bundle régénéré et ses
135 entrées distribuées sont vérifiés. Les trois clusters PostgreSQL locaux
utilisés pour les preuves sont arrêtés ; aucune base TEST hébergée n'est touchée.

### Rapprochement des 34 critères

Le propriétaire reste le domaine `identite_acces` pour le PIN et les sessions,
`exploitation` pour la consommation, `animation_locale` pour l'attestation et
la progression. `ServiceValidationPin` orchestre les mêmes règles que les
parcours QR ; les interfaces affichent les décisions serveur. Les documents
de référence sont le [contrat](architecture-contrats.md) et la
[notice Pro/client/ERP](guide-utilisation-exploitation.md).

| Critère | Comportement observable et preuves | Documentation / exploitation |
| --- | --- | --- |
| E70-CA-01 | C : ouverture/relecture sans consommation, mouvement ou notification ; P : aucun accès Pro créé | Demande bornée par droit client |
| E70-CA-02 | I API stricte et Bearer ; C substitutions parent/cible/droit/demande refusées sans essai PIN | Référence publique insuffisante |
| E70-CA-03 | I domaine ; P états absent, futur, expiré, révoqué, bloqué ; C suspension/fermeture canal/clé absente | Contrôle courant à confirmation |
| E70-CA-04 | A référence serveur ; F récapitulatif et confirmation explicite, trois accès Coffret et reçu | Référence distincte du secret et du reçu |
| E70-CA-05 | I extra champs/finalité refusés ; C substitutions ; P commerce/étape/versions | Cible immuable, nouvelle demande |
| E70-CA-06 | I durée cinq minutes ; C annulation ; P expiration/rejeu ; F abandon/reprise | Reçu protégé par droit courant |
| E70-CA-07 | P barrières et connexions PostgreSQL, QR/PIN et plusieurs PIN : un effet/validation/mouvement | Verrou commun par commerce |
| E70-CA-08 | C droit consommé, instance annulée/expirée, commerce suspendu ; P cœur commun QR/PIN | Aucune dérogation métier |
| E70-CA-09 | I secrets filtrés ; N stockage/cache/analytics/transport ; F abandon et champ effacé ; B reload | Risque de capture sur appareil tiers déclaré |
| E70-CA-10 | F réponse perdue/reload/GET sans POST rejoué ; P reçu après expiration et concurrence | Vérifier le résultat avant nouvelle demande |
| E70-CA-11 | I séparation gestion/client ; C PIN connu sans droit, instance/participant étrangers ; P commerce étranger | PIN borné, pas authentifiant Pro |
| E70-CA-12 | I API Admin/Backoffice/CSRF versus Lecteur/Finance ; C révocation globale E69 ; E assistance sans secret | Motif, audit et portée E69 globale |
| E70-CA-13 | A contexte SQL/segments et refus ; P acteur/version/corrélation ; F reçu PIN/QR/ANOMALIE | Pas d'identité salariée inventée |
| E70-CA-14 | F erreurs, expiration, blocage, temps serveur, réponse perdue ; N transport borné | Internet requis, alternatives selon droits |
| E70-CA-15 | C scan principal malgré incident PIN, scan salarié malgré blocage/révocation ; P périmètres | Suspension métier reste opposable |
| E70-CA-16 | F/B/E nominal-refus-reprise mobile/PC, D jeu/restauration, L notice et lecteur | E70-DEC-CLOTURE-TESTS : pilote externe hors gate |
| E70-CA-17 | I durée/format/reauth et rôles ; P génération unique et session principale ; U/B gestion | Secret affiché une fois, reauth ≤15 min |
| E70-CA-18 | I bornes 1/7/30 jours et refus ; P avant début/fin serveur ; F délai/heure | Aucun calcul de validité métier dans l'UI |
| E70-CA-19 | P générations concurrentes, remplacement et version monotone ; B remplacement explicite | Ancien code inutilisable |
| E70-CA-20 | P demande antérieure/révocation, reçu conservé ; C historique acquis conservé | Révocation sans annulation rétroactive |
| E70-CA-21 | P verrous réels rotation/révocation/suspension contre validation | Effet acquis avant changement seulement |
| E70-CA-22 | I support non générateur ; P aucun rejeu du secret ; B réponse perdue et remplacement | Aucun code récupérable |
| E70-CA-23 | I/P DTO/logs/emails sans secret ; U/B GET et reload ; N stockage | Notification sans code, no-store |
| E70-CA-24 | C cinq erreurs multi-demandes, rotation, borne quinze minutes sans prolongement et fin fenêtre ; P concurrence | Blocage global, QR conservé |
| E70-CA-25 | M migrations réelles répétées, données/droits/sessions conservés, QR consommable ; D restauration | Aucun PIN ni activation par migration |
| E70-CA-26 | P notification Pro unique, outbox/email transactionnel, panne/reprise même intention ; C anomalie sans faux succès | Remise fournisseur réelle non attestée |
| E70-CA-27 | C rotation token Coffret avant/après succès et droit participant étranger ; P révocation ; F droit retiré | Pas de consultation du reçu par ancien droit |
| E70-CA-28 | C clé absente/canal fermé, support, historique après révocation sans nouveau mouvement ; P conservation | Notice incident et références sans secret |
| E70-CA-29 | C moteur Passeport réel : qualification/progression ; Chasse : preuve puis réponse distincte ; P équivalence QR/PIN | PIN atteste, ne résout pas le défi |
| E70-CA-30 | C début/fin/clôture/anonymisation/token retiré/commerçant retiré/Chasse inaccessible ; P versions | Éligibilité actuelle du moteur |
| E70-CA-31 | C participant étranger ; P cible/étape/commerce/versions substitués | Versions et droit participant obligatoires |
| E70-CA-32 | P concurrence Animation QR/PIN ; C rejeu normal/ANOMALIE, une progression/notification au plus | Pas de double qualification/remise |
| E70-CA-33 | A audit complet, refus après rollback, purge réelle demande sans perte de contexte ; P conservation | Audit habilité, SQL et segments contrôlés |
| E70-CA-34 | I/P refus gestion salarié ; U URL directe refusée sans chargement ; C scan salarié toujours possible | PIN partagé distinct de l'accès nominatif |

### Livraison à préparer

| Composant | Action | Configuration / contrôle |
| --- | --- | --- |
| Backend et workers | Livrer les correctifs ; migrations v256/v257 déjà requises, aucune nouvelle migration E70 | Vérifier schéma et audit succès/refus/reprise |
| Backend | Ouvrir explicitement le canal si souhaité | `LOCALEO_PRO_PIN_VALIDATION_ENABLED=false` par défaut ; configurer `LOCALEO_PIN_VALIDATION_KEYS_JSON` et `LOCALEO_PIN_VALIDATION_ACTIVE_KEY` dans le coffre de l'environnement ; clé active présente, valeur UTF-8 ≥32 octets, aucune valeur secrète dans Git |
| Pro | Livrer gestion PIN et tests complémentaires après backend | Principal seulement ; salarié ne gère jamais le PIN ; reprise après réponse perdue |
| Marketplace/Live | Livrer l'affichage de référence après backend | Trois accès Coffret, détail Animation, confirmation puis reçu, mobile et PC |
| Contrats Animation | Publier l'instantané partagé avec le nouveau champ optionnel | Aucun écran de gestion Animation modifié, aucun nouveau paramètre |
| Documentation ERP | Regénérer le bundle au commit retenu et sélectionner cette révision dans le déploiement | Alias `formation/validation-par-pin.md`, empreintes et lecteur ; le bundle local n'est pas une publication hébergée |
| Exploitation | Conserver les jobs d'envoi et de conservation existants ; surveiller l'audit et les reprises | Santé puis création/refus/reçu avec données de recette ; fermer le canal en incident sans annuler les droits déjà consommés ni supprimer les clés encore nécessaires |

Lots à examiner séparément : backend `fix(pin): préserver le contexte des refus et compléter les preuves E70` ;
Marketplace `fix(pin): afficher la référence du coffret avant confirmation` ;
Pro `test(pin): couvrir la reprise après génération incertaine` ;
Animation `chore(contracts): aligner DemandePin sur la référence coffret` ;
projet `docs(epic70): consigner la clôture sur tests et la livraison`.
L'index Git n'est pas modifié ; isoler les hunks E70 des travaux E72/E76 et
des documents d'onboarding déjà présents.

## 1. Matrice de couverture initiale

Chaque ligne désigne un scénario de référence ; le bilan ci-dessous distingue les preuves locales des contrôles de mise en service. Dans la colonne
documents, « contrat » renvoie à l'architecture de ce dossier ; les notices Pro,
client et support suivent les parcours du README. Les données restent fictives.

| Critère | Comportement et propriétaire | Scénario de référence | Documentation / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| E70-CA-01 | Demande liée au droit, `exploitation` + `identite_acces` | API droit cs1. valide, cible correcte, aucun effet à l'ouverture | DTO demande Coffret | Coffret actif, droit cible | Vérifier canal fermé par défaut |
| E70-CA-02 | PIN sans droit client insuffisant | Appels sans Bearer, référence publique, autre instance et droit révoqué | Autorisations client | Deux coffrets de détenteurs distincts | Refus sans oracle ni secret |
| E70-CA-03 | État PIN/commerce courant | Domaine puis API : absent, désactivé, expiré, révoqué, bloqué, commerce suspendu | Métadonnées et erreurs | PIN dans chaque état | Reprise par principal/support |
| E70-CA-04 | Confirmation explicite | Navigateur mobile : recap, saisie, effet unique, reçu | Notice téléphone client | Coffret éligible | Ne pas confondre présence et preuve PIN |
| E70-CA-05 | Cible immuable | Falsifier instance/droit/commerce/finalité ; refus sans effet | Schéma strict confirmation | Demandes A/B | Diagnostic corrélé |
| E70-CA-06 | Demande 5 min et résultat terminal | Horloge à 4:59.999 et 5:00 ; annulation/rejeu, reçu après succès | États demande | Demande expirée/succès | Ne pas purger le reçu au délai de saisie |
| E70-CA-07 | Consommation unique tous canaux | PostgreSQL deux connexions : QR/PIN, double clic, plusieurs appareils ; compter validation et mouvement | Cœur commun / locks | Même droit concurrent | Invariant sans skip PostgreSQL |
| E70-CA-08 | Règles Coffret inchangées | Droit consommé, expiré, coffret inactif ; comparer QR et PIN | Réutilisation domaine | États métier refusés | Aucun contournement financier |
| E70-CA-09 | Pas de secret conservé | Espions logs/outbox/analytics, stockage navigateur et cache SW ; retour arrière/abandon | Confidentialité | PIN sentinelle synthétique | Réponse no-store ; risques tiers expliqués |
| E70-CA-10 | Reprise après timeout | Serveur committe, réponse perdue, GET sans nouvelle saisie, PIN expiré | DTO résultat | Succès avec interruption | Aucun replay automatique mutation |
| E70-CA-11 | Portée limitée d'un PIN capturé | Essayer accès Pro, autre commerce et absence droit client | Matrice de droits | Deux commerces | Notice risque résiduel |
| E70-CA-12 | Support habilité et audit | Admin/Backoffice succès, Lecteur/Finance seuls refus ; même ancienne session ; trace | Scope `acces_externes.gerer` | Quatre profils ERP | Motif, corrélation, aucun PIN lisible |
| E70-CA-13 | Audit de succès/refus | Assertions acteur PIN, commerce, cible, version, horodatage ; absence identité salarié prétendue | ActeurValidation | Trace QR vs PIN | Recherche support autorisée |
| E70-CA-14 | Indisponibilité sans faux succès | Réseau absent, blocage, expiration pendant saisie, erreur serveur | Messages et alternatives | Simulation coupure | QR/E9 selon droits habituels |
| E70-CA-15 | Canaux indépendants | Désactivation/blocage PIN puis scan principal et salarié ; suspension commerce refuse tous | États mode | Commerce multi-canaux | Fermeture E70 sans désactiver QR |
| E70-CA-16 | Guides et démonstration | Recette mobile principal/client/support nominal-refus-reprise, lecteur de guides | README et notices à intégrer E68/ERP | Scénario end-to-end fictif | Recette cible distincte des tests locaux |
| E70-CA-17 | Génération et reauth | Domaine 6 chiffres, suites/repetitions ; API à 15 min et au-delà, salarié refusé | Routes gestion | PIN affiché une fois | Perte de réponse → remplacer, pas récupérer |
| E70-CA-18 | Durée serveur | 1/7/30 jours, 0/31/fraction refusés ; timezone/DST ; début inclus et fin exclusive | Date/heure fin | Horloge fixe | Pas de dépendance au batch d'expiration |
| E70-CA-19 | Remplacement | Deux générations concurrentes, version monotone, ancien code inutilisable, pas même code généré | Idempotency-Key gestion | PIN remplacé | Clé serveur versionnée |
| E70-CA-20 | Révocation après ouverture | Ouvrir, révoquer sans reauth supplémentaire, confirmer : refus ; succès antérieur conservé | DELETE gestion | Demande antérieure | Aucune annulation rétroactive |
| E70-CA-21 | Révocation/validation concurrentes | Barrières PostgreSQL aux locks puis commit ; aucun effet après révocation effective | Ordre commun de locks | Version obsolète | Tests de deadlock/retry contrôlé |
| E70-CA-22 | Perte et support | Remplacement principal, récupération accès ; pas de lecture par support ni client | Parcours incident | Accès Pro oublié | Invalidation tracée par ERP |
| E70-CA-23 | Métadonnées seulement | DTO/export/logs/audit/réponse de rejeu génération sans secret ; clé serveur absente | EtatPin et PinGenere | Sentinelles PIN/hash | Redaction, restrictions de logs |
| E70-CA-24 | Essais cumulés | 5 erreurs réparties en 15 min, 5e bloque ; essais bloqués ne prolongent pas ; borne +15 min ; remplacement ne contourne pas | ProtectionEssaisPin | Plusieurs appareils | Alerte unique par épisode, scan préservé |
| E70-CA-25 | Migration inactive | Base antérieure puis migration additive ; aucun PIN, modes absents, scans inchangés | Migration | Commerce ancien et nouveau | Ne pas appliquer aux environnements réels pendant tests |
| E70-CA-26 | Notifications fiables | Succès unique Pro seulement ; changement/blocage Pro+email ; panne transport/rejeu sans doublon ni nouvel effet | Catégories/clé de déduplication | Faux transport email | Reprise outbox et marquage Pro sans secret |
| E70-CA-27 | Droit client courant | Révocation/rotation consultation ou token participant entre ouverture et confirmation/GET | Vérification dans UoW | Droit changé | Aucun retour de résultat à un tiers |
| E70-CA-28 | Incident et historique | Révoquer puis consulter trace/signalement ; aucun remboursement automatique | Procédure support | Validation litigieuse | Préserver preuves et droits financiers |
| E70-CA-29 | Attestation même métier QR | Même participant/étape via QR et PIN en tests séparés : mêmes règles/versions/effets ; succès/ANOMALIE distincts | Cœur Animation dans UoW | Passeport/chasse compatibles | Pas d'API d'administration client |
| E70-CA-30 | Refus Animation | Calendrier, service communal, commerce absent, participant révoqué, état inéligible | Erreurs moteur existantes | Chaque refus métier | Aucune progression ni récompense |
| E70-CA-31 | Substitution Animation | Changer participant/animation/étape/versions/finalité après ouverture | Cible typée immuable | Deux participations | Recréer demande après changement |
| E70-CA-32 | Concurrence Animation | QR/PIN simultanés avec verrous réels, une attestation effective et une réconciliation | Locks animation/participant | Deux connexions PostgreSQL | ANOMALIE ne devient pas VALIDEE au rejeu |
| E70-CA-33 | Audit Animation | Date, cible, mode, version PIN, motif et corrélation sans token | Audit / conservation | Trace Animation | Politique reçus distincte de l'audit |
| E70-CA-34 | Pas de gestion PIN salarié | Toutes routes gestion/reauth par salarié et PIN seul refusées, y compris payload forgé | Contrat E72 | Salarié activé/révoqué | Vérifier routes au-delà des menus |

Les preuves croisées comprennent le garde des appels directs et des anciens
frontends, les scans normaux et les effets du mode secours existant. Un build,
un import ou une inspection OpenAPI ne prouvent aucun de ces invariants.

## 2. Organisation des tests à produire

- Backend domaine : politiques PIN, transitions demande, fenêtre glissante,
  état effectif, expiration UTC, valeurs interdites ; ports simulés, aucune base.
- Application : UoW et événement résultat, persistance des erreurs malgré réponse
  HTTP négative, aucun commit intermédiaire, notification seulement sur effet réel.
- Adaptateurs/PostgreSQL : contraintes, CAS, verrouillage croisé QR/PIN, révocation
  des droits, outbox et migrations depuis l'état antérieur. Toute absence de base
  jetable est un contrôle non exécuté, pas un skip faisant preuve de succès.
- API : DTO stricts, corps/headers, scopes ERP/Pro, CSRF ERP, refus des accès salariés,
  statut d'erreur et relecture. Génération offline des contrats, sans config opérateur.
- Marketplace/Pro : tests des appels et de la reprise ; parcours navigateur mobile,
  caméra refusée pour alternative QR, compte à rebours accessible, clavier et erreur.
- Animation partenaire : non-régression des listes et détails de validation, catégorie
  ANOMALIE et périmètre territorial existants ; aucun rôle supplémentaire.

Commandes de référence à utiliser lors de l'implémentation depuis le dépôt concerné :

```text
# Backend : nouveaux tests nommés lors de l'implémentation, via le runner isolé
python scripts/validation/test_isolated.py tests/architecture -q
# Commerçant : suites ciblées puis commandes locales de contrat/build
npm test
# Marketplace : helpers/contrats puis parcours navigateur ciblés
npm run test:security
```

Ces commandes ne sont pas présentées comme exécutées. Ajouter les chemins des
tests E70 créés au bilan et exécuter les scénarios de concurrence avec PostgreSQL.
Ne pas lancer les suites contre une base ni des services d'exploitation.

## 3. Démonstration et documentation

Le générateur reste dans `localeo-backend/scripts/demonstration`, selon ses
instructions locales. Ajouter PIN fictifs à états actif/expiré/révoqué/bloqué,
coffret et participant, deux commerces, principale/salarié, profils ERP, demande
en attente et réponse perdue. Tester restauration, références et absence de secret
dans les journaux du générateur ; aucune notification réelle ni donnée d'accès dans
ce dépôt documentaire. Les sorties privées demeurent dans le stockage opérateur.

Documents à intégrer pendant implémentation : notice principal (préparer, durée,
affichage unique, oubli), aide client (tendre téléphone, résultat, reprise), guide
ERP (invalidation, motif, absence de lecture), onboarding E68 (exercice sans consommation),
configuration serveur (clé, fermeture du canal), diagnostic et reprise notifications.
Le présent dossier est la conception canonique ; les guides exportés ne doivent
pas annoncer E70 disponible avant implémentation. S'ils changent, ajouter le contrôle
des sources et des lecteurs ERP via `documentation.exports.json`.

## 4. Livraison et exploitation prévues

1. Implémenter et tester le [rattachement commun de conservation](../identite-acces/conservation-validations-acces.md) : catégories, dates sourcées, purge SQL/JSONL, archivage minimal, gels et anti-rejeu. Le rattachement à l'Annexe A et le CLI E70 sont livrés ; leur ordonnancement en exploitation reste à configurer.
2. Migrations additives sur base jetable, contrôle des comptes/mouvements antérieurs,
   sauvegarde/reprise documentées. Réserver les numéros de migration au moment de coder.
3. Déployer backend avec canal E70 fermé et clé versionnée provisionnée ; valider
   les tests de contrat et les anciens scans, puis Pro et Marketplace/Live compatibles.
4. Recette cible autorisée séparément : principal génère, client valide, reçu,
   notification, invalidation puis refus ; Animation idem sans effet métier fictif.
5. Ouvrir le canal uniquement après validation du parcours complet. Consigner versions
   des applications et révision documentaire, sans confondre publication et recette.
6. Incident : fermer le canal PIN, préserver QR/E9, invalider la version compromise,
   consulter audit selon habilitation, reprendre les notifications ; aucune annulation
   financière implicite. Contrôler aussi accès client révoqué, clé manquante et timeout.

## 5. État historique au stade de spécification (5 octobre)

| Contrôle | État au stade de spécification |
| --- | --- |
| Lecture des producteurs/consommateurs | Réalisée sur les sources locales citées, sans exécution applicative |
| Couverture documentaire | 34 critères rattachés à des scénarios attendus ; pas de résultat métier acquis |
| Revue indépendante de contrats | Réalisée puis revue ciblée après corrections : notifications PIN distinctes, chemins complets, verrouillage commun, résolution invitation et absence de règle irréversible implicite ; aucune incohérence bloquante restante relevée dans ce périmètre |
| Liens et diff | Contrôle Node local : 292 liens sur 13 documents, aucune cible manquante ; 34/34 et 22/22 critères présents sans doublon dans les matrices E70/E72 ; `git diff --check` réussi |
| Tests métier, API, PostgreSQL, navigateur | Non exécutés : fonctionnalité à implémenter |
| Migrations, emails et déploiement | Non réalisés |
| Conservation générale | Rattachement documentaire établi le 7 octobre : [rattachement commun de conservation](../identite-acces/conservation-validations-acces.md) ; implémentation et tests des traitements requis avant mise en service |

La conception n'accorde ni preuve de présence physique ni garantie d'absence de
capture sur un appareil client. Les restrictions, révocations et délais décrits
sont les garanties à implémenter et à tester. La planification de livraison reste
ouverte ; l'état produit demeure À faire.

Contrôle standard `python scripts/check_guidance.py --changed` tenté le 5 octobre :
non exécuté, interpréteur `python` introuvable ; recherche des lanceurs usuels sans
résultat. Le contrôle Node vérifie les cibles locales, pas les ancres ni les lecteurs
ERP. Aucun fichier source de `documentation.exports.json` modifié ; pas de nouveau
bundle ni de contrat OpenAPI généré. Lors du contrôle du 5 octobre, le PDF Annexe A n’avait pas pu être extrait. Cette limite documentaire est levée par son extraction du 7 octobre et le rattachement commun ; les délais E41 ne sont pas étendus aux audits ordinaires E70/E72.

## Contrôle documentaire du rattachement — avant implémentation

Annexe A extraite et rattachement commun établi ; revue indépendante ciblée sans
incohérence bloquante relevée. Contrôle Node : 94 liens locaux sur 10 documents,
aucune cible manquante ; matrices inchangées, 34/34 critères E70 et 22/22 E72,
sans doublon. `git diff --check` réussi. `python scripts/check_guidance.py`
non exécuté : Python introuvable. Le contrôle de remplacement ne vérifie ni les
ancres ni les consommateurs. Aucun fichier exporté modifié ; aucune purge,
migration, activation de job ou test applicatif exécuté.


## 6. Bilan d’implémentation locale — 7 octobre 2026

État **En cours**. Le backend, Localeo Pro et Marketplace portent le parcours
PIN ; Animation reçoit le contrat moteur partagé. Migrations additives **256 et
257**, canal fermé par défaut. Aucun déploiement, email réel ou purge de données
réelles n’a été exécuté. Les preuves suivantes complètent le plan initial.

| Critères / périmètre | Preuves exécutées et résultat |
| --- | --- |
| CA-01 à 15, 17 à 24, 27 à 33 | Tests domaine/API PIN et tests PostgreSQL `test_validation_pin_coffret_e70.py`, `test_validation_pin_animation_e70.py` : droits courants, révocation, horloge après verrous, QR/PIN concurrents, rollback, attribution et reprise. 11 scénarios PostgreSQL Coffret et 7 Animation réussis ; 6 scénarios QR Animation existants réussis. |
| CA-17 à 24 | `test_pin_validation_dedicated.py` et tests API : génération, exclusions, durée, réauthentification, compteur partagé, secret à affichage unique et remplacement après retrait d’une ancienne clé expirée. |
| CA-04, 09, 10, 14, 22, 26 | Pro : 2 parcours Playwright réussis (390 et 1280 px), tests de gestion/notifications/navigation réussis. Marketplace : 4 parcours Playwright et 105 tests de sécurité réussis, build isolé réussi ; contexte changé et réponse perdue couverts. |
| CA-13, 23, 26, 28, 33 — conservation | 18 tests réussis, dont 7 PostgreSQL, dans `test_conservation_validations_dedicated.py`, `test_segments_audit_pin.py`, `test_conservation_pin_postgres.py` : plafonds calendaires, preuves minimales, gels, lots progressifs, segments SQL/JSONL et anti-rejeu. |
| Non-régression / architecture | 460 contrôles obligatoires d’architecture, classes domaine et couverture des use cases réussis ; 40 tests des use cases exploitation réussis. La fixture SMS fournit désormais les champs obligatoires du domaine, sans assouplir d’assertion. |
| Contrats partagés | Exports OpenAPI offline E41/E42/Pro régénérés. Schéma `actions_validation_pin` propagé aux trois consommateurs ; 34 contrôles Pro et 3 contrôles de registre par autre frontend réussis. |
| CA-15, 34 — salarié réel | Garde de rôle présent dans E70 ; preuve de bout en bout avec les nouveaux comptes salariés à réaliser dans E72, après publication E70. |

La revue indépendante a conduit à corriger la progression des lots de purge,
les reçus Animation après suppression du participant, la classification des audits
métier PIN, le remplacement après expiration d’une ancienne clé et le retrait des
traces de génération. Les corrections disposent de preuves ciblées.

Les guides opérationnels sont dans [Utilisation et exploitation](guide-utilisation-exploitation.md).
Avant ouverture : provisionner les clés hors dépôt, appliquer les migrations avec
le runner habituel, ordonnancer et surveiller la conservation, vérifier les copies
externes et sauvegardes, puis effectuer la recette réelle principal/client/support.
Les traitements E70 ne remplacent pas les politiques historiques des écritures
comptables Coffret. Aucune conformité déployée n’est déduite des tests locaux.


Contexte des preuves : Python 3.12.10 avec dépendances verrouillées, PostgreSQL 18
local jetable, navigateurs Chromium ; arbres de travail issus de backend
`760a5c9`, Pro `4785603`, Marketplace `4e948f1`, Animation `cac5eb4` et documentation
`08c51d8`. Les migrations et générateurs n’ont utilisé aucun environnement métier.
La régénération des contrats reprend aussi `avancement-preparation.schema.json`,
déjà publié par le producteur et manquant dans les deux copies Pro/Marketplace.


Complément final : 19 tests API du support et deux scripts navigateur ERP
(`tests/browser/pin-validation-erp.cjs`, `tests/browser/acces-commercant-erp.cjs`)
réussis à 390/1280 px. La révocation se fait depuis l’onglet Accès du commerce,
avec motif, confirmation, capacité et CSRF ; une réponse perdue impose une lecture
avant nouvelle action.

Démonstration : 16 tests unitaires et les 6 scénarios du runner
`python scripts/validation/run_demo_compatibility_tests.py` réussis sur PostgreSQL18,
aucun skip (438,59 s). L’invocation utilise un `--basetemp` local distinct pour
contourner les permissions du dossier temporaire historique ; le runner et ses
gardes restent inchangés. Migrations depuis zéro, génération PIN, intégrité des
relations, garde des sources, installation/reset/restauration sont vérifiés. Les
trois tables de conservation sont classées `replace` et leurs références restaurées.
Trois avertissements de réflexion SQLAlchemy `dialect_options`, sans échec.


Contrôles documentaires finaux : `check_guidance.py` (92 guides, 965 liens, aucune
erreur), puis contrôle du lot Git `--staged --changed --all-markdown` (14 documents,
282 liens, aucune erreur) ; `sync_documentation.py --check-sources` (122 documents)
et `git diff --cached --check` réussis. Commits applicatifs E70 : backend `776e852`,
Pro `81c9b21`, Marketplace `fa616e6`, Animation `f3dc2e2`.


Complément E72 du 8 octobre : les tests PostgreSQL d’identité salariée couvrent
maintenant l’attribution et le refus de gestion PIN par un salarié, y compris un
appel direct au service. Le reçu Coffret mémorise aussi une validation gagnée par
un autre canal pour permettre sa relecture sans double consommation. Les preuves
et limites sont dans le [bilan E72](../epic-72-acces-salaries/verification-livraison.md).

## Correctif du 9 octobre — diagnostic du refus de création dans Localeo Pro

Signalement test : HTTP 409 sur `/protected/identite-acces/commercants/moi/reauthentification`. Dans les sources examinées, le contrôle d’ouverture refuse la réauthentification avec `PIN_INDISPONIBLE` lorsque `LOCALEO_PRO_PIN_VALIDATION_ENABLED` est faux ; lecture d’état et révocation restent possibles. Le corps de réponse du serveur test est demandé pour confirmer ce diagnostic, aucune configuration distante n’a été lue/modifiée.

Défaut frontend reproduit : `PIN_INDISPONIBLE` était masqué par un message générique invitant à actualiser. Localeo Pro affiche désormais un message d’indisponibilité et la possibilité du scan QR, sans contourner la réauthentification ni rejouer la génération. Test dédié initialement rouge puis corrigé ; vérification PIN ciblée exécutée dans le dépôt Commerçant. Configuration à vérifier par l’opérateur : `LOCALEO_PRO_PIN_VALIDATION_ENABLED=true`, puis trousseau `LOCALEO_PIN_VALIDATION_KEYS_JSON` et identifiant `LOCALEO_PIN_VALIDATION_ACTIVE_KEY` cohérents pour la génération. Aucune clé réelle dans les logs/documentation. Pas de migration, contrat API ou générateur de démonstration modifié ; pas de déploiement effectué.

## Correctif du 11 octobre — refus de réauthentification et droits de gestion

Signalement : `ACTION_INTERDITE` lors de la création d’un PIN. Ce code seul ne permet pas d’attribuer le refus distant : le service peut refuser le mot de passe (ou un identifiant absent/verrouillé), mais les contrôles de commerce et de session principale emploient aussi ce code. La requête exacte en erreur reste à confirmer ; aucun journal distant ni compte réel n’a été consulté.

Défaut d’interface reproduit sur la base Commerçant `a81ce8d` : un 403 de réauthentification était systématiquement présenté comme une action réservée au responsable. Le message situe désormais le refus pendant la vérification d’identité et invite à vérifier le mot de passe du compte connecté, puis à contacter Localeo si le refus persiste. Un refus lors de la génération conserve le message d’autorisation. Aucun contrôle serveur n’est modifié ; aucune génération n’est envoyée après un échec de réauthentification, le mot de passe est effacé et la relecture reste obligatoire.

Preuve : test de régression rouge avant correction (message de droits incorrect), puis `npm.cmd test -- --run src/features/pinValidation` : **15 tests réussis dans 3 fichiers**. Modification limitée au consommateur Pro et au présent suivi ; contrats API, règles métier, schéma et générateur de démonstration inchangés. La disparition du refus sur l’environnement distant n’est pas établie. Aucun déploiement effectué.

Diagnostic complémentaire : l’utilisateur confirme le refus sur `/reauthentification`, y compris immédiatement après une reconnexion réussie avec le mot de passe commerçant. La revue du parcours principal et de la connexion unifiée salariée ne montre pas de transformation différente du mot de passe. Le test isolé `tests/application/test_reauthentification_pin.py` vérifie la réauthentification avec un vrai hash bcrypt, puis les refus pour mot de passe incorrect, compte verrouillé et identifiant absent : **4 tests réussis**. Il utilise des doubles de persistance ; il ne reproduit pas l’environnement distant. Les contrôles architecture/domaine/couverture donnent **467 tests réussis** après utilisation d’un répertoire temporaire explicite dans `.artifacts` (premier lancement : 452 réussis et 15 erreurs de préparation des fixtures temporaires). La trace serveur `pin_validation.reauthentification`, phase `failure`, motif `IDENTIFIANTS_INVALIDES`, associée à la corrélation de la tentative, reste à examiner pour confirmer la branche exécutée. Aucun changement du comportement backend n’est justifié à ce stade.

La ligne serveur fournie pour `LOC-98083f3b-b725-4ff7-b7c0-d222fdc86b6a` confirme seulement le POST de réauthentification en 403. Ajout d’un diagnostic technique `pin_validation.reauthentification.refusee` avec corrélation, étape et motif catégorisé, sans données d’identité ni secret ; l’audit métier et la réponse publique restent inchangés. Régression reproduite avant instrumentation (absence de diagnostic), puis vérification de huit cas applicatifs : succès, quatre refus d’identifiants et trois étapes de contrôle d’accès. Suite ciblée API/domaine/application et contrôles architecture/couverture : **511 tests réussis, 3 avertissements de dépréciation**. Ce complément corrige l’absence de diagnostic, pas une cause distante démontrée ; une nouvelle tentative après livraison reste nécessaire. Aucune migration, modification de contrat ou donnée de démonstration requise. Pas de déploiement effectué.

## Revue de clôture du 1er novembre 2026

### Verdict et versions examinées

**Clôture bloquée ; état En cours conservé.** La demande initiale « 70N » est
confirmée par l'utilisateur comme **epic 70**. Les 34 critères restent inchangés,
sans déplacement du backlog ni modification des compteurs de roadmap.
Les revues indépendantes backend et consommateurs complètent les contrôles
ci-dessous ; elles ne remplacent pas une exécution.

Arbres examinés : backend **ecfc9f1**, Pro **0c8499e**, Marketplace **6c5dd04**,
documentation **9c74a33**. Les corrections Live locales déjà présentes dans
Marketplace et les deux documents E73 sont conservées et étrangères au lot E70.
Les seuls changements backend de cette revue concernent deux fixtures/scénarios
de test ; aucune règle PIN, API ou donnée métier n'est modifiée.

### Écarts empêchant la clôture

1. **CA-03/18 — refus avant le début non satisfait lors de la revue initiale,
   corrigé ensuite localement.** Dans la version initialement examinée,
   `app/domaine/identite_acces/pin_validation.py`, `PinValidationCommerce.etat`
   contrôle l'expiration mais pas `now < generated_at` ; `autoriser` accepte ce
   PIN comme `ACTIF`. Reproduction pure le 1er novembre, sortie **1** : création
   à une date future d'une minute puis appel à `autoriser` à l'heure antérieure.
   La génération nominale est immédiate ; cela ne démontre pas une exploitation
   du cas sur TEST, mais contredit la borne explicitement prévue par CA-18.
   Le correctif et ses nouvelles preuves figurent à la fin du présent bilan ;
   ce constat historique n'est plus une réserve ouverte sur la borne de début.
2. **CA-04/14 — informations temporelles client partielles lors de la revue,
   corrigées ensuite localement.** Le composant initial
   `src/components/PinValidation.jsx` ne présente ni délai issu de `expires_at`
   et `server_time`, ni heure de reprise issue de `blocked_until` après un
   blocage. Il affiche « réessayez plus tard ». Le backend fournit les champs,
   mais les quatre tests navigateur existants ne les vérifient pas. Le refus
   serveur n'est pas neutralisé ; l'écart porte sur le parcours attendu.
   Le correctif CA-04/13/14 ci-dessous lève cette réserve de présentation.
3. **CA-13 — reçu visuel incomplet lors de la revue, corrigé ensuite
   localement.** Commerce et cible restent visibles, mais
   le résultat client se limite à un message générique, sans date ni référence
   de validation présentées. Les données du reçu API et l'audit ne prouvent pas
   cet affichage prévu par la spécification. L'audit serveur n'est pas déclaré
   absent pour cette raison. Le correctif ci-dessous présente ces informations
   et conserve le reçu jusqu'à sa fermeture explicite.
4. **CA-19/21/26 — preuves manquantes lors de la revue, complétées ensuite
   localement.** Ajouter les générations concurrentes,
   les courses confirmation contre révocation/remplacement/suspension du PIN,
   puis la création et la reprise des emails de changement/blocage. Les courses
   de révocation de **salarié** E72 et la révocation PIN **séquentielle** ne
   prouvent pas ces courses PIN ; la déduplication d'une notification Pro ne
   prouve pas la reprise d'un transport email. La section CA-19/21/26 en fin de
   bilan apporte les nouvelles exécutions et distingue l'intention unique de la
   remise physique par le fournisseur.
5. **CA-16 et mise en service — recette pilote non attestée.** Le bilan et la
   roadmap exigent encore le parcours principal/client/support sur la cible
   prévue. Aucun scénario confirmé par l'utilisateur ni rapport hébergé ne
   permet de lever cette réserve. L'ancien refus distant de réauthentification
   du 11 octobre n'est pas réputé résolu par un test isolé réussi.

Reproduction minimale **avant le correctif** de la borne avant génération, depuis le backend, sans
configuration ni service externe :

```python
from datetime import datetime, timedelta
from app.domaine.identite_acces.pin_validation import PinValidationCommerce, DureePinValidation

now = datetime(2026, 11, 1, 12)
pin = PinValidationCommerce()
pin.remplacer(now + timedelta(minutes=1), DureePinValidation())
pin.autoriser(now)  # Avant correctif : pas de RefusPin ; après : PIN_INDISPONIBLE.
```

Ces écarts nécessitent une correction et de nouvelles preuves. Aucune exigence
n'est réduite pour obtenir une clôture ; les règles métier ne sont pas changées
silencieusement dans cette phase.

### Contrôles réellement exécutés

Les codes ci-dessous servent à rapprocher les critères, sans annoncer la
couverture exhaustive d'un critère sur la seule présence d'un test.

| Référence | Commande / contexte | Résultat de cette revue |
| --- | --- | --- |
| B | Lanceur isolé backend, Python 3.14 : `test_pin_validation_dedicated.py`, `test_session_validation_e70.py`, `test_commercant_validation_e70.py`, `test_conservation_validations_dedicated.py`, `test_reauthentification_pin.py`, `test_actions_pin_animation_e70.py`, `test_pin_validation_e70.py`, `test_pin_validation_erp_e70.py`, `test_segments_audit_pin.py`, `test_demonstration_pins_validation.py` ; répertoire `.artifacts/pytest-e70-closure` | **76 réussis**, aucun ignoré ; un avertissement `datetime.utcnow` dans le test API |
| A | `python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q`, répertoire temporaire dédié | **623 réussis**, aucun ignoré |
| P | PostgreSQL 18.3 nouvellement initialisé, local et jetable ; `test_validation_pin_coffret_e70.py`, `test_validation_pin_animation_e70.py`, `test_conservation_pin_postgres.py`, `test_validations_salaries_e72.py`, `test_perimetres_validations_postgres.py`, `test_attestations_moteur_postgres_t4.py` via le lanceur isolé et son `--postgres-test-url` explicite | Premier passage : **22 réussis, 24 erreurs de fixture**. Après premier correctif d'import : **45 réussis, 1 échec d'attente**, aucun skip. Graphe FK complet chargé ensuite et scénario d'historique corrigé/rejoué seul : **1 réussi**, aucun skip. Les détails ci-dessous distinguent ces passages ; aucune suite agrégée finale n'est annoncée |
| M | Marketplace : `npx playwright test --config=playwright.desktop.config.cjs tests/visual/pin-validation.spec.cjs`, serveur/build isolés, sortie `tmp/e70-closure-pin` | **4 réussis**, sortie 0 : réponse perdue et reçu, PIN incorrect effacé, création retrouvée avec même clé, droit expiré |
| N | Marketplace : `node --test tests/security/pin-recovery.test.cjs` | **1 réussi**, aucun ignoré : reprise sans PIN conservé |
| C | Pro : `npm test -- src/features/pinValidation src/features/employees/EmployeeAccess.test.jsx src/lib/api/contracts.test.js src/app/merchantNavigation.test.js` | **69 réussis**, six fichiers, aucun ignoré |
| V | Pro : `npm run test:e2e -- tests/e2e/pin-validation.spec.js --workers=1 --output=tmp/e70-closure-pro-pin` | **2 réussis**, 390/1280 px, build sans `.env`, API simulées. Réauthentification, génération, masquage et révocation ; malgré le titre du scénario, aucun remplacement n'y est exécuté |
| E | Backend : `node tests/browser/pin-validation-erp.cjs` | Script réussi sur 390/1280 px : état sans secret, motif, révocation, réponse perdue/relecture et refus Lecteur |
| H | Rapports des 7–8 octobre conservés dans le présent bilan | Preuves **historiques réutilisées**, non réexécutées : migrations complètes et six scénarios de compatibilité/restauration du générateur ; ne prouvent pas une recette actuelle déployée |
| D | `check_guidance.py`, puis `check_guidance.py --changed --all-markdown` et `sync_documentation.py --check-sources` | **94 guides / 1 050 liens**, puis **7 documents modifiés / 160 liens** ; aucune erreur ni avertissement. **130 sources exportables** vérifiées ; `git diff --check` réussi dans les deux dépôts modifiés |

Les tests n'utilisent ni compte réel, ni envoi fournisseur, ni base d'exploitation.
Les réponses API des navigateurs sont simulées. La recette matérielle/PWA
installée et les scénarios hébergés ne sont pas transformés en réussites.

Le problème de préparation PostgreSQL vient du graphe des bons E73 :
`acces_bons_lots.bon_id` référence `bons_lots`, qui dépend à son tour des tirages
libres et de la dotation. La fixture ERP charge maintenant explicitement ces
trois modules ; son exécution ne dépend plus de leur import par un autre fichier
collecté. Le test isolé avait encore reproduit la référence d'attribution
manquante après le premier import ; le graphe complet lève cette erreur.

L'autre échec concernait `test_historique_exclut_archive_et_autre_commerce` :
un UUID de commerce inexistant était attendu comme historique vide, alors que
le contrôle de périmètre le refuse avec `COMMERCE_INTROUVABLE`. Le scénario
crée désormais un second commerce réel, vérifie son historique vide **avant**
l'archivage de celui du premier, vérifie séparément le refus 404 d'un identifiant
absent, puis conserve les assertions d'exclusion de l'archive. Le rejeu isolé
réussit ; aucune assertion d'isolation n'est retirée. Les avertissements de cycles
SQLAlchemy des profils et de `datetime.utcnow` restent rapportés, sans skip.

### Rapprochement des 34 critères

La spécification et la matrice initiale restent la cible. « Local » ci-dessous
désigne seulement les comportements explicitement vérifiés ; « Partiel » ou
« Non vérifié » interdit de déclarer le critère complet acquis. Le guide
utilisateur/exploitation et les contrats du dossier s'appliquent à chaque ligne ;
les actions de livraison sont détaillées dans la section suivante.

| Critère | Code / comportement observé | Preuves | Verdict et reste à vérifier |
| --- | --- | --- | --- |
| E70-CA-01 | `ServiceValidationPin.creer_demande`, droit et cible | B, P Coffret | Partiel : ajouter l'assertion explicite d'absence d'effet à l'ouverture |
| E70-CA-02 | Droit client courant avant comparaison du PIN | B, P Coffret | Partiel : élargir la matrice d'accès falsifiés ; aucun droit créé par le PIN |
| E70-CA-03 | État courant de `PinValidationCommerce` | B et correctif CA-03/18 ci-dessous | Borne de début corrigée localement ; fermeture globale conditionnée aux autres réserves |
| E70-CA-04 | DTO commerce/cible/effet, confirmation masquée et délai serveur | M et correctif CA-04/13/14 ci-dessous | Partiel : délai, expiration et reprise vérifiés localement ; référence du coffret avant saisie demandée au parcours canonique mais absente du DTO/récapitulatif client. La référence de validation au reçu est distincte. |
| E70-CA-05 | DTO strict et cible attachée à la demande | B, P | Partiel : matrice de substitutions Coffret complète à vérifier |
| E70-CA-06 | Demande 5 minutes, résultat terminal et relecture | B, P, M | Local pour expiration/relecture ; annulation intégrée à compléter |
| E70-CA-07 | Cœur commun Coffret et mouvement unique | P Coffret | Local : concurrence QR/PIN et un seul mouvement dans le rejeu ; preuve historique distinguée |
| E70-CA-08 | Conditions Coffret communes au QR | P, tests métier historiques | Partiel : refus consommé/expiré/inactif à rapprocher sur le canal PIN |
| E70-CA-09 | HMAC, `no-store`, champ vidé, stockage de reprise sans PIN | B, M, N, C, V | Local pour confidentialité des contrats et du navigateur testés |
| E70-CA-10 | Reçu courant après réponse perdue | P, M | Local pour reprise et absence de seconde confirmation |
| E70-CA-11 | Gestion principale et HMAC lié commerce/version | B, C | Partiel : parcours intégré des réutilisations d'un PIN capturé à compléter |
| E70-CA-12 | Invalidation ERP sous habilitation, motif et CSRF | B, E | Local Admin/Backoffice et refus Lecteur/Finance ; périmètre territorial à compléter |
| E70-CA-13 | Acteur PIN/audit ; reçu client commerce/cible/date/référence/mode/résultat | B, P, M et correctif ci-dessous | Réserve de présentation levée localement ; compléter les preuves détaillées d'audit prévues en CA-33 |
| E70-CA-14 | Codes de refus, alternatives et reprise explicite | B, M, C et correctif ci-dessous | Local : heure de reprise en heure de Paris, sans confirmation automatique ; recette distante non exécutée |
| E70-CA-15 | Cœur QR conservé, acteur salarié distinct | P, C | Partiel : séquence blocage PIN puis QR principal/salarié à compléter |
| E70-CA-16 | Guide, démonstration et parcours mobile | B, M, V, E, H | Partiel : recette pilote/cible et démonstration complète actuelle non attestées |
| E70-CA-17 | Génération et réauthentification principale | B, C, V, P | Local pour exclusions, bornes de durée et affichage unique |
| E70-CA-18 | `generated_at`, `expires_at`, horloge injectée | Correctif CA-03/18 ci-dessous | Bornes de validité corrigées et vérifiées localement ; recette cible distincte |
| E70-CA-19 | Version et remplacement, relecture sans secret | B, C, P et complément CA-19/21/26 ci-dessous | Local : concurrence clés identiques/distinctes et remplacement Pro réellement exécuté à 390/1280 pixels |
| E70-CA-20 | Révocation après ouverture | P Coffret, E | Preuve séquentielle ; ne vaut pas preuve de course CA-21 |
| E70-CA-21 | Ordre commun de verrous PIN | Complément CA-19/21/26 ci-dessous | Local : deux ordres de commit observés sous contention réelle, sur Coffret/Animation/Bon ; suspension ERP selon engagements courants |
| E70-CA-22 | Remplacement par principal, invalidation par support | B, C, E | Local sur commandes ; récupération du compte et incident pilote à confirmer |
| E70-CA-23 | Métadonnées, hash, audit et notifications assainis | B, P, V et complément CA-19/21/26 | Local : la réserve email est levée par `_verifier_alerte` dans `test_pin_notifications_postgres_e70.py` : objet, texte, HTML et notification Pro sans PIN, token ni vérificateur, génération et blocage. Ne prouve pas la remise fournisseur. |
| E70-CA-24 | Fenêtre partagée et blocage sans prolongation | B, P Animation | Partiel : plusieurs demandes/appareils et remplacement pendant blocage à compléter |
| E70-CA-25 | Migrations 256/257 additives et mode fermé | H, P conservation | Migration complète depuis état antérieur non rejouée dans cette revue |
| E70-CA-26 | Notification Pro et outbox dans l'UoW | P, C et complément CA-19/21/26 ci-dessous | Local : intentions corrélées sans secret, rollback, rejeu et reprise après panne avant acceptation ; remise externe après crash non garantie |
| E70-CA-27 | Droit courant à la confirmation et au reçu | P Coffret/Animation | Partiel : compléter les variantes rotation/confirmation, au-delà de la relecture après révocation |
| E70-CA-28 | Invalidation, historique et conservation | B, P, E | Partiel : parcours complet de traitement d'incident à confirmer |
| E70-CA-29 | Cœur Animation `dans_uow` commun QR/PIN | P Animation/T4 | Partiel : effets nominaux et attribution vérifiés ; résultat `ANOMALIE` et rejeu non prouvés avec le moteur complet. Les doubles de vérification des étapes et réconciliation ne prouvent pas toutes les définitions. |
| E70-CA-30 | Réévaluation du moteur et périmètres commerçants | P Animation/périmètres | Partiel : calendrier/commune/commerce/participant à couvrir sur chaque refus PIN prévu |
| E70-CA-31 | Cible et versions Animation figées | B, P Animation | Partiel : matrice intégrée de substitutions à compléter |
| E70-CA-32 | Attestation unique QR/PIN et double confirmation | P Animation | Local pour les courses présentes ; n'inclut pas les courses CA-21 |
| E70-CA-33 | Audit Animation et conservation distincte | B, P conservation et revue statique actualisée | Partiel : l'autorisation produit en confirmation précède les blocs d'audit E70 ; refus de droit courant sans version PIN, cibles retrouvables par jointure aux demandes/validations tant qu'elles sont conservées. Production et conservation d'une trace de refus complète restent à prouver/corriger. |
| E70-CA-34 | Garde principal et routes salariées interdites | B, C, P salariés | Local : lecture/génération/révocation salariées refusées en PostgreSQL ; réauthentification salariée directe refusée avant lookup du mot de passe et commit dans `test_diagnostic_preserve_les_refus_avant_verification_du_mot_de_passe`, étape `autorisation`. |

### Configuration et ordre de livraison à préparer

Ces actions sont dérivées du code et du [guide opérationnel](guide-utilisation-exploitation.md).
Elles ne sont pas exécutées dans cette revue. La cible et ses références privées
restent à renseigner ; aucune valeur de secret n'est requise dans ce dossier.

| Composant / cible | Action et valeur attendue | Contrôle / reprise |
| --- | --- | --- |
| Backend, avant ouverture | Vérifier les migrations **256 puis 257**, dans la chaîne existante ; appliquer seulement celles absentes avec `scripts/database/apply_migrations.py` | État et empreintes du runner ; ne pas rejouer manuellement un SQL déjà appliqué |
| Backend | `LOCALEO_PRO_PIN_VALIDATION_ENABLED=false` par défaut ; activation maîtrisée après correction et validation des prérequis | Canal indisponible si fermé, QR préservé ; fermeture du flag en incident |
| Backend, stockage privé | Provisionner `LOCALEO_PIN_VALIDATION_KEYS_JSON` et `LOCALEO_PIN_VALIDATION_ACTIVE_KEY`, cohérents ; garder les anciennes clés tant que leurs PIN sont valides | Génération/refus avec clé absente, remplacement ; aucune clé dans les frontends ou rapports |
| Audit et conservation | Même chemin `LOCALEO_AUDIT_EXTERNAL_JSONL_PATH` pour API/maintenance ; `LOCALEO_CONSERVATION_DATABASE_URL` explicitement fourni au CLI | `conserver_validations_pin.py --limit 100` simule ; application autorisée séparément, gels et copies externes vérifiés |
| Exploitation | Configurer fréquence et surveillance de la conservation selon les échéances existantes ; fréquence cible à renseigner par l'opérateur | Vérifier rapports, retards, gels, sauvegardes et réapplication des retraits après restauration |
| Backend puis Pro et Marketplace/Live | Livrer des versions compatibles avec les mêmes DTO et `actions_validation_pin` ; conserver les scopes et contrats des salariés E72 | Contrats embarqués, garde de rôle et parcours QR/PIN ; aucun nouveau flag frontend introduit |
| Documentation backend/ERP | Publier la révision documentaire du futur commit E70 et vérifier son bundle/empreinte avec le lecteur | La présence de la source dans le workspace n'est pas une publication ERP ; bundle non versionné |
| Recette cible | Principal génère, client valide Coffret et Animation, reçu/notification, erreur/blocage, révocation puis refus, support ; confirmer le diagnostic de réauthentification | Consigner versions, cible, résultats et corrélations expurgées avant ouverture générale |

Une fermeture du canal ne supprime aucune validation, table additive ou preuve.
Aucun downgrade destructif ni rollback financier n'est promis. L'ordonnancement
et la configuration à venir ne sont pas les seuls motifs de blocage : les
écarts de critères et de preuves ci-dessus restent à résoudre.

### Lots de commit préparés, sans indexation

- **localeo-projet** : présent bilan, README E70, backlog E70 et note de roadmap.
  Message proposé : `docs(e70): consigner les écarts de clôture et la recette actualisée`.
- **localeo-backend** : imports du graphe dotation/tirages/bons dans la fixture
  ERP et scénario d'isolation d'historique salarié avec second commerce réel.
  Message proposé : `test(e70): fiabiliser les fixtures PostgreSQL des validations`.
- **Marketplace / Pro / Animation** : pas de changement E70 à committer dans
  cette revue. Les modifications locales Live/E73 sont hors de ces lots.

L'index Git n'est pas modifié. Aucun commit, push, déploiement, migration sur
une cible métier, envoi réel ou purge d'exploitation n'est effectué.

## Correctif CA-03/18 — 1er novembre 2026

À la suite de la revue ci-dessus, la demande de correctif porte sur la borne
de début du PIN. Le défaut est reproduit dans le domaine : `autoriser()`
acceptait une version dont `generated_at` était dans le futur, ainsi qu'une
version active sans date de début. Le contrôle de fin existait déjà.

La règle appartient à `PinValidationCommerce`, dans `identite_acces` :
**`generated_at <= now < expires_at`**, avec l'horloge UTC du serveur.
Avant le début, ou sans début renseigné, elle refuse `PIN_INDISPONIBLE` / 409.
Les appels existants à l'ouverture et à la confirmation l'appliquent aux
prestations Coffret, aux étapes Animation et aux remises de bons lots ; la
projection de disponibilité des bons applique aussi ce contrôle. Le refus
précède comparaison cryptographique, décompte des essais et effet métier.

Les quatre états de métadonnées et le choix conservateur de l'ancien
vérificateur lors d'un remplacement restent inchangés. Un reçu terminal déjà
acquis demeure accessible sous les droits courants ; le correctif ne revalide
pas rétroactivement son PIN et ne produit pas un second effet.

### Preuves du correctif

Versions locales : backend **`ecfc9f1` avec différences non committées**,
documentation **`9c74a33` avec différences non committées**. Les corrections de
fixtures de la revue précédente et les travaux Live/E73 présents sont préservés.
Une revue indépendante en lecture du domaine et des nouveaux scénarios n'a
relevé aucun défaut bloquant ; elle ne remplace pas les exécutions ci-dessous.

- **Reproduction avant correction** : 4 échecs et 12 succès sur les 16 nouveaux
  cas du domaine. Les trois durées 1/7/30 jours avant génération et le début
  absent échouaient pour absence du refus attendu.
- **Après correction, domaine/API/application/architecture** : **698 succès**,
  aucun skip. Commande depuis le backend :

  ```console
  python scripts/validation/test_isolated.py tests/domain/identite_acces/test_pin_validation_dedicated.py tests/api/test_pin_validation_e70.py tests/api/test_pin_validation_erp_e70.py tests/application/test_reauthentification_pin.py tests/application/services/test_actions_pin_animation_e70.py tests/api/test_pin_bon_lot_e73.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q --basetemp=.artifacts/pytest-e70-ca0318-isolated
  ```

- **Démonstration** : **8 succès**, aucun skip avec
  `python scripts/validation/test_isolated.py tests/unit/test_demonstration_pins_validation.py -q --basetemp=.artifacts/pytest-e70-ca0318-demo`.
  Aucune génération de données sur une cible métier.
- **PostgreSQL jetable local 18.3** : le premier passage donne 27 succès et
  7 échecs. Les sept nouveaux cas passent ; les échecs existants Animation
  révèlent une fixture utilisant `datetime.now()` local avec un service UTC,
  donc un PIN artificiellement futur. La fixture emploie désormais
  `utc_now_naive()`, sans retirer ni assouplir d'assertion. Le rejeu complet
  donne **34 succès**, aucun skip, en 109,14 secondes, avec la commande :

  ```console
  python scripts/validation/test_isolated.py tests/security/test_validation_pin_coffret_e70.py tests/security/test_validation_pin_animation_e70.py tests/security/test_pin_bons_lots_postgres.py -q --tb=short --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:16452/localeo_audit_test --basetemp=.artifacts/pytest-e70-ca0318-pg-replay
  ```

  Cette URL vise uniquement le cluster jetable de cette vérification,
  sur boucle locale ; elle ne désigne aucun environnement métier.
  Les 30 avertissements concernent le cycle ORM préexistant des profils
  commerçants et les usages dépréciés de `datetime.utcnow()` dans les fixtures.

Les nouveaux tests du domaine couvrent début moins une microseconde, début
inclus, fin moins une microseconde, fin exclue et après fin pour 1/7/30 jours,
ainsi que l'absence de début. Les sept nouveaux scénarios PostgreSQL couvrent
ouverture et confirmation pour les trois effets, sans écriture métier,
notification de succès ou essai incorrect lors du refus ; puis succès au début
exact et conservation du reçu après retour d'horloge. Le septième vérifie la
projection du bon indisponible avant le début et le QR préservé.
Le contenu de l'audit du refus n'est pas une nouvelle preuve de ces scénarios ;
son chemin existant reste inchangé et les réserves d'audit de la revue subsistent.

Contrôles documentaires : `python scripts/check_guidance.py` (94 guides,
1 050 liens), `python scripts/check_guidance.py --changed --all-markdown`
(8 documents, 176 liens) et `python scripts/sync_documentation.py --check-sources`
(130 sources) réussis, sans erreur ni avertissement documentaire.
`git diff --check` réussit dans les deux dépôts concernés.

### Impacts et livraison

Deux dépôts modifiés pour ce correctif : backend (domaine et tests) et projet
(spécification, bilan et suivi). Aucun champ ni enum API modifié, le code 409
existe déjà : pas de contrat embarqué à régénérer ni de modification frontend.
Pas de migration, nouvelle variable, clé, permission ou configuration fournisseur.
Le générateur produit déjà un début cohérent ; ses tests passent sans adaptation.
Aucune réparation de données ni mise en service n'est effectuée.

Lot backend proposé pour la correction :
`fix(e70): refuser les PIN avant leur date de generation`.
Les changements de fixtures de la revue précédente restent identifiables
séparément ; les changements Live/E73 ne font pas partie du correctif.
La publication du backend corrigé et de la révision documentaire devra suivre
la procédure de livraison existante. Aucun commit, push ou déploiement dans
cette demande. **E70 reste En cours** : les autres réserves des 34 critères
ne sont pas levées par cette correction ciblée.

## Correctif client CA-04/13/14 — 1er novembre 2026

La demande suivante traite les trois réserves de présentation de la revue.
Cause vérifiée : le DTO commun aux Coffrets, Animation et bons lots expose
déjà `expires_at`, `server_time`, `validated_at`, `validation_id`, `resultat`
et `mode_effectif`, mais `PinValidation.jsx` ne les présente pas. L'erreur
`PIN_BLOQUE` fournit `blocked_until`. De plus, l'actualisation immédiate du
parent peut supprimer l'action devenue inéligible et démonter son reçu avant
lecture. Aucun défaut du producteur API ni changement de règle métier n'est
nécessaire pour ces réserves.

### Comportements corrigés

- **CA-04** : temps restant ancré sur `server_time` et `expires_at`, décrémenté
  avec l'horloge monotone du navigateur. L'heure civile du téléphone ne sert
  pas à calculer le délai. À zéro, saisie et confirmation sont désactivées ;
  **Vérifier le résultat** relit la même demande. Seul le serveur peut la
  déclarer expirée ou fournir son reçu. Une demande conservée après rechargement
  est relue avant saisie ; son délai n'est pas prolongé. Une nouvelle demande
  repart avec un champ vide.
- **CA-13** : dialogue de reçu avec commerce, cible, résultat, date en heure
  de Paris, référence et mode effectif. Un succès acquis par QR est indiqué
  **QR** ; une anomalie n'est pas annoncée comme une progression confirmée.
  Pour une ancienne remise, l'avertissement historique reste visible même si
  le bon a changé d'état. L'actualisation du parent est déclenchée après
  **Terminer et actualiser** ou Échap, afin de laisser le reçu lisible.
  Le dialogue est modal, accessible au clavier et adapté à la largeur mobile.
- **CA-14** : heure de reprise provenant de `blocked_until`, affichée en heure
  de Paris. Le blocage suspend la saisie jusqu'à une vérification explicite ;
  aucune confirmation n'est renvoyée au terme du délai. Une date absente est
  signalée sans remplacement inventé. Après une réponse perdue, même à délai
  écoulé, la lecture du résultat reste la reprise proposée. Le QR conserve ses
  règles et aucun succès hors ligne n'est simulé.

### Vérifications et périmètre

Arbre vérifié : Marketplace **`6c5dd04` avec différences non committées**,
documentation **`9c74a33` avec différences non committées**. Les travaux Live/E73,
la revue E70 et le correctif backend CA-03/18 déjà présents sont conservés.

Avant correction, les trois nouveaux scénarios de reproduction échouent
précisément sur l'absence du décompte, du dialogue de reçu et de l'heure de
reprise. Le premier passage après correction trouve un écart de focus clavier
dans les trois variantes de reçu ; il est corrigé sans modifier l'attendu.
La revue indépendante relève aussi une saisie conservée après expiration puis
nouvelle demande : le champ est désormais effacé et ce chemin est testé.

- **14 scénarios Chromium réussis**, aucun skip, sortie 0 en 50,5 secondes :

  ```console
  npx playwright test --config=playwright.desktop.config.cjs tests/visual/pin-validation.spec.cjs tests/visual/pin-validation-feedback.spec.cjs --output=tmp/e70-feedback-final
  ```

  Ils couvrent 390/1280 pixels, téléphone réglé en 2040 et dates serveur en
  2026, fuseau navigateur Tokyo, délai/expiration, nouvelle saisie vide,
  rechargement sans prolongation, reçus PIN/QR/ANOMALIE, dates absentes,
  navigation Tab/Échap, blocage et réponse perdue. Capture mobile du reçu
  inspectée visuellement ; référence longue sans débordement horizontal.
- **3 tests Node réussis**, aucun skip, sortie 0 :
  `node --test tests/security/pin-recovery.test.cjs tests/security/paris-dates.test.cjs`.
  Ils vérifient reprise sans secret et affichage Paris depuis Los Angeles/Tokyo.
- **8 scénarios Chromium bons lots réussis**, aucun skip, sortie 0 en 36 secondes :

  ```console
  npx playwright test --config=playwright.desktop.config.cjs tests/visual/pin-validation-bon-feedback.spec.cjs tests/visual/digital-lot.spec.cjs --output=tmp/e70-feedback-bons
  ```

  Reçu PIN retenu jusqu'à fermeture, état courant actualisé ensuite, remise
  historique explicitement distinguée, réponse perdue relue en mode QR sans
  seconde confirmation, accès personnel et affichage 320/1280 pixels.
  Le scénario existant de reprise numérique ferme désormais le reçu avant
  d'attendre l'actualisation du bon ; ses assertions d'effet unique sont conservées.
- Le serveur Playwright reconstruit l'artefact de production de manière isolée,
  sans `.env` opérateur, sans réécriture de configuration publique et sans API
  réelle. Aucun build standard chargeant la configuration opérateur n'est lancé.

Ce correctif modifie **localeo-marketplace** (composant partagé, styles et tests)
et **localeo-projet** (guide, bilan et suivi). Le domaine et l'API restent les
propriétaires de la validité, du blocage, des droits, de l'effet et du reçu ;
aucun contrôle serveur n'est retiré. Aucun contrat embarqué ni DTO ne change,
donc pas de régénération OpenAPI, migration, nouvelle variable ou adaptation
du générateur. Les suites backend du correctif précédent ne sont pas annoncées
comme rejouées pour cette modification de présentation. Les preuves détaillées
d'audit et la recette pilote restent distinctes de ces tests navigateur simulés.

Contrôles finaux réussis : ESLint ciblé sur le composant et les trois fichiers
de scénarios modifiés/ajoutés ; `git diff --check` dans les deux dépôts ;
`check_guidance.py` (94 guides, 1 050 liens),
`check_guidance.py --changed --all-markdown` (9 documents, 177 liens) et
`sync_documentation.py --check-sources` (130 documents).
La relecture indépendante finale ne relève plus de défaut bloquant.

Lot proposé : `fix(e70): afficher le delai le recu et la reprise PIN`.
Les modifications Live/E73 déjà présentes restent hors de ce lot.
Aucun commit, push, déploiement ou recette distante n'est effectué.
**E70 reste En cours**, avec les autres réserves du bilan conservées.

## Complément CA-19/21/26 — 1er novembre 2026

La demande traite les preuves absentes relevées à la clôture. Les nouveaux
scénarios ont confirmé la sérialisation du PIN et révélé un défaut de sélection
des emails à reprendre selon le fuseau de PostgreSQL. Le correctif concerne
`EmailSortantRepositorySqlAlchemy.lister_a_envoyer`, ainsi que deux nouveaux
fichiers de tests backend :
[concurrence](../../../../localeo-backend/tests/security/test_pin_concurrence_e70.py)
et [notifications](../../../../localeo-backend/tests/security/test_pin_notifications_postgres_e70.py).
Le correctif métier CA-03/18 et les correctifs client CA-04/13/14 déjà présents
restent conservés, sans être présentés comme de nouveaux changements de ce lot.

### Invariants et preuves ajoutées

- **CA-19** : `PinValidationCommerce.remplacer` reste propriétaire de la
  nouvelle version et de sa validité. Deux générations concurrentes, avec clés
  distinctes, produisent deux versions successives et des secrets différents ;
  seul le dernier code est utilisable. Avec la même clé, une seule génération
  et une seule notification sont enregistrées ; le rejeu ne réaffiche pas le
  secret. Les tests vérifient les lignes persistées et les empreintes effectives.
  Le scénario navigateur Pro, auparavant limité à générer/masquer/invalider,
  exécute désormais aussi le remplacement avec réauthentification, nouvelle
  clé, version 2 et secret différent, puis masquage et invalidation au clavier.
- **CA-21** : la garde est prise par `RepositoryPinValidation.commerce`,
  via le repository des périmètres, avant lecture du PIN et effet. La suspension
  ERP passe par `ServiceAtelierErp.statut_commercant` et sa garde commerce.
  Le banc retient le premier verrou et observe **`pg_blocking_pids`** sur la
  seconde connexion avant de libérer : il démontre une attente PostgreSQL,
  au-delà d'un simple départ simultané de deux threads.
  Révocation principale, révocation support et remplacement sont testés dans
  les deux ordres face à une confirmation Coffret, Animation et Bon lot.
  Si le changement gagne, aucun nouvel effet ; si la validation gagne, son
  occurrence et son reçu restent uniques. Après remplacement, un ancien code
  bien formé donne `PIN_INCORRECT` et compte un essai ; après révocation il est
  indisponible avant comparaison.
- La **suspension ERP réellement permise** est testée sur Animation et Bon lot,
  dans les deux ordres. Après son commit, `COMMERCE_INACTIF` / 403 refuse la
  confirmation ; aucun nouvel effet n'est créé. La suspension d'un commerce
  avec offres/engagements Coffret reste interdite par `verifier_retrait` : deux
  scénarios vérifient ce refus concurrent `ERP_COMMITMENTS_EXIST`, sans contourner
  la règle pour fabriquer un commerce suspendu. Après suspension, une relecture
  par confirmation peut aussi être refusée par le périmètre courant ; cela ne
  supprime pas l'occurrence déjà acquise.
- **CA-26** : génération, révocation et cinquième erreur produisent une
  notification Pro et une intention email corrélées, sans PIN, token ou
  vérificateur dans leur contenu. Les rejeux conservent les mêmes identifiants.
  Les essais déjà bloqués ne créent pas de nouvelle alerte. Une panne d'écriture
  outbox annule ensemble le changement et la notification ; au cinquième essai,
  elle conserve les quatre erreurs antérieures avant reprise de la transaction.
  Le vrai `LancerBatchEmails`, avec transport exclusivement factice, conserve
  la même intention après panne avant acceptation, puis la marque envoyée après
  reprise, sans nouvelle intention ni nouvel effet métier. Un succès PIN Coffret
  ou Animation produit une notification Pro unique sans email PIN au principal ;
  l'email client Coffret `PRESTATION_UTILISEE`, commun au métier QR, est préservé.

### Exécutions et limites

Base locale PostgreSQL **18.3 jetable**, `127.0.0.1:16452`, base
`localeo_audit_test`, schémas uniques par fixture. Aucun service métier, compte
réel, transport fournisseur ou configuration opérateur n'est sollicité.
Versions de base : backend **`ecfc9f1`**, projet **`9c74a33`**, avec différences
locales non committées ; les travaux Live/E73 restent hors du lot.

Exécutions initiales : 8 scénarios génération/Coffret réussis, puis 16 scénarios
Animation/Bon lot réussis. Au premier passage des notifications, 2 succès et
8 échecs proviennent tous d'une attente incorrecte du nouveau test : les pièces
jointes absentes sont persistées comme **`[]`**, pas `None`. L'assertion exige
désormais exactement cette liste vide ; aucun contrôle de secret, d'atomicité
ou de déduplication n'est retiré. Ce premier passage ne démontre pas un défaut
de production. Le passage commun suivant donne **68 succès et 2 échecs** sur
70 scénarios en 317,69 secondes : les 26 cas de concurrence, les 34 régressions
Coffret/Animation/Bon et huit cas de notifications réussissent ; les deux reprises
transport échouent sur `ValueError("Email non réservable")`.

### Défaut CA-26 reproduit puis corrigé

`date_planifiee` est stocké comme `timestamp` UTC sans offset, alors que
`func.now()` PostgreSQL produit un instant zoné. Leur comparaison interprète la
date UTC dans le fuseau de la session SQL. En heure de Paris, une reprise prévue
dans cinq minutes peut être sélectionnée immédiatement ; le domaine refuse
alors légitimement sa réservation et le batch échoue. À l'ouest d'UTC, la
sélection peut au contraire retarder un email déjà dû.

Une reproduction ciblée avec `TimeZone=Europe/Paris` confirme l'échec avant
correction, sans affaiblir le garde `peut_reserver_envoi`. L'adaptateur capture
désormais un unique `utc_now_naive()` et l'utilise pour les échéances et les
réservations abandonnées. La colonne reste comparée à une borne constante,
avec pagination et `FOR UPDATE SKIP LOCKED` préservés. Le domaine continue de
vérifier la réservation : aucune règle métier n'est déplacée ou contournée.
Les six scénarios génération/blocage × UTC/Paris/Los Angeles contrôlent la
non-sélection avant échéance puis la reprise du même email après échéance.
Ils configurent uniquement le fuseau de leurs transactions de test, sans
modifier le serveur ou demander une nouvelle configuration de déploiement.

Le correctif de sélection s'applique au **batch email générique**, au-delà des
seuls messages PIN. Les régressions d'exploitation et du transport des accès
internes sont donc ajoutées aux vérifications. La comparaison analogue du
repository SMS reste hors de ce lot ; aucun test ni correctif SMS n'est annoncé.

Contrôle isolé initial, **706 succès**, aucun skip, sortie 0 en 21,67 secondes,
avant le correctif du repository ; une exécution élargie après correction
renouvelle les preuves concernées :

```console
python scripts/validation/test_isolated.py tests/domain/identite_acces/test_pin_validation_dedicated.py tests/api/test_pin_validation_e70.py tests/api/test_pin_validation_erp_e70.py tests/application/test_reauthentification_pin.py tests/application/services/test_actions_pin_animation_e70.py tests/api/test_pin_bon_lot_e73.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/unit/test_demonstration_pins_validation.py -q --basetemp=.artifacts/pytest-e70-ca192126-isolated
```

Après correction du repository, **762 succès**, aucun skip, sortie 0 en
24,02 secondes, en ajoutant les régressions du batch et de sa règle de réservation :

```console
python scripts/validation/test_isolated.py tests/domain/identite_acces/test_pin_validation_dedicated.py tests/api/test_pin_validation_e70.py tests/api/test_pin_validation_erp_e70.py tests/application/test_reauthentification_pin.py tests/application/services/test_actions_pin_animation_e70.py tests/api/test_pin_bon_lot_e73.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/unit/test_demonstration_pins_validation.py tests/application/use_cases/test_exploitation_use_cases.py tests/domain/exploitation/entities/test_reservation_envoi.py tests/domain/exploitation/entities/test_email_sortant.py -q --basetemp=.artifacts/pytest-e70-ca192126-after
```

Les **six reprises transport** génération/blocage × UTC/Paris/Los Angeles
réussissent après correction, sortie 0, aucun skip en 53,22 secondes :

```console
python scripts/validation/test_isolated.py tests/security/test_pin_notifications_postgres_e70.py -q --tb=short -k panne_transport --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:16452/localeo_audit_test --basetemp=.artifacts/pytest-e70-ca26-timezone-after
```

Le rejeu complet des notifications et les régressions PostgreSQL du transport
des accès internes donnent ensuite **16 succès**, aucun skip, sortie 0 en
101,06 secondes :

```console
python scripts/validation/test_isolated.py tests/security/test_pin_notifications_postgres_e70.py tests/integration/test_e69_transport_interne.py -q --tb=short --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:16452/localeo_audit_test --basetemp=.artifacts/pytest-e70-ca26-regression-after
```

Les 26 tests de concurrence et les 34 régressions des trois parcours réussis
dans le passage commun précédent ne sont pas rejoués après ce seul changement
du sélecteur email : ils ne passent pas par cette méthode. Ils restent des
preuves exécutées distinctes, sans qualifier de vert le passage initial à
deux échecs. Les six reprises ciblées se recouvrent avec les 16 succès finaux.
Les avertissements conservés concernent le cycle ORM historique des profils
commerçants et les appels dépréciés à `datetime.utcnow()` des fixtures ; aucun
skip ni assouplissement d'assertion métier n'est utilisé.

**Localeo Pro** : deux scénarios Chromium réussis (390 et 1280 pixels), sortie 0
en 14,8 secondes, API simulée et build navigateur isolé (`configFile:false`,
`envDir:false`) :

```console
npm run test:e2e -- tests/e2e/pin-validation.spec.js --workers=1 --output=tmp/e70-ca19-pro-pin
```

La version de base Pro est **`0c8499e`**, avec ce seul scénario modifié.
Ces preuves d'interface ne remplacent pas la contention réelle du backend.

Contrôles documentaires et différences : `check_guidance.py` (94 guides,
1 050 liens), `check_guidance.py --changed --all-markdown` (9 documents,
179 liens), `sync_documentation.py --check-sources` (130 documents) et
`git diff --check` des trois dépôts réussis. Les liens ajoutés vers les tests
restent des références de sources ; aucun artefact privé n'est copié ici.

Le transport de test échoue **avant acceptation**. L'unicité de l'intention
outbox ne garantit pas une remise physique exactement une fois après acceptation
fournisseur suivie d'un crash : le batch générique ne transmet pas de clé
d'idempotence fournisseur. Cette limite est conservée ; aucune garantie plus
forte ni recette distante n'est déduite des scénarios locaux.

La revue indépendante du domaine, des entrées, du correctif UTC et des deux
fichiers de tests ne relève pas de défaut bloquant dans le périmètre annoncé. Les doubles du
moteur de jeu restent ceux des fixtures d'attestation existantes : PostgreSQL,
verrous, UoW, occurrences et progression sont réels, mais ces tests ne remplacent
pas une recette de toutes les définitions de jeux.

### Impacts et lot examinable

Trois dépôts concernés : **localeo-backend** pour le correctif de sélection et
les preuves, **localeo-commercant** pour le scénario navigateur de remplacement,
**localeo-projet** pour le bilan, le guide et le suivi. Aucun contrat, DTO,
code frontend, schéma SQL, migration, configuration ou générateur modifié.
Les tests du générateur sont inclus, sans génération sur une cible métier.
Pour corriger une cible hébergée, publier le backend corrigé et la révision
documentaire correspondante ; aucune migration ou modification de fuseau SQL
n'est requise. Vérifier ensuite qu'un email futur n'est pas pris par le batch,
puis que l'intention due est traitée une seule fois. Les tests Pro seuls ne
nécessitent pas de livraison de l'application commerçant.

Messages de lots proposés : backend
`fix(e70): fiabiliser la reprise UTC des notifications et prouver les concurrences PIN`,
Pro `test(e70): verifier le remplacement du PIN dans le navigateur`,
projet `docs(e70): actualiser les preuves CA19 CA21 et CA26`.
L'index n'est pas modifié ; aucun commit, push ou déploiement n'est effectué.
**E70 reste En cours**, avec ses autres critères partiels et la recette cible
non attestée. Les critères ne sont ni réduits ni supprimés pour conclure ce lot.

## Reprise de clôture après les correctifs — 1er novembre 2026

### Décision et périmètre réellement vérifié

Nouvelle demande « 70N », interprétée comme **E70** conformément à la précision
antérieure de l’utilisateur. **Clôture non prononcée : E70 reste En cours.**
Les 34 critères sont conservés, sans déplacement du backlog ni changement des
compteurs. Les correctifs précédents sont réexaminés ; leurs succès ne lèvent
pas automatiquement les autres critères partiels de la matrice.

Bases et branches examinées : backend **`ecfc9f1`**, Marketplace **`6c5dd04`**,
Pro **`0c8499e`**, projet **`9c74a33`**, tous sur `main`, avec différences locales
non committées et index initialement vides. Les travaux Live, OnBoard et E73
restent conservés et distincts. Aucun nouvel invariant PIN, API, schéma SQL ou
comportement métier n’est modifié pendant cette reprise.
Le portail organisateur Animation **`04dc06c`**, `main` propre, est seulement
revu comme consommateur des contrats ; aucun test de son interface n’est annoncé.

Les revues indépendantes rapprochent les assertions et les producteurs réels :
les réserves précises **CA-23** (contenu des emails sans secret) et **CA-34**
(réauthentification salariée refusée avant recherche du mot de passe) sont levées
localement. La matrice ci-dessus est actualisée à ces endroits, ainsi que pour
CA-04/29/33. Les autres lignes partielles restent telles quelles.

### Réserves maintenues et actions nécessaires

- **CA-04 — récapitulatif Coffret avant saisie.** L’étape 2 du parcours canonique
  demande la référence du coffret. `_dto` et `PinValidation.jsx` présentent le
  commerce, la cible et l’effet mais pas cette référence. La référence de la
  validation dans le reçu est une autre donnée. Le correctif délai/reçu demeure
  acquis ; il ne suffit pas à accepter ce parcours complet. Corriger le producteur
  et le consommateur, puis vérifier l’affichage avant confirmation sans divulgation.
- **CA-33 — audit des refus Animation.** Dans
  `app/application/exploitation/services/validation_pin.py`, le contrôle
  `autoriser_cible_dans_uow` précède les blocs d’audit E70 ; les refus de droit
  courant auditent sans version PIN. Dans `service_audit.py`, les événements
  requalifiés PIN ne conservent que version/demande/motif/action d’origine : les
  cibles restent joignables via demande/validation tant que ces lignes existent.
  Cette lecture ne prouve pas les traces requises après conservation distincte.
  Reproduire les refus de périmètre/droit et vérifier les champs persistés,
  l’absence de secret et la continuité d’audit après conservation ; traiter le
  correctif ciblé avant acceptation. Un journal HTTP ne remplace pas cette preuve.
- **Preuves intégrées encore partielles.** CA-01/02/05/06/08/11/12/15 demandent
  notamment ouverture sans effet, substitutions de cibles/droits, annulation,
  refus métier Coffret, PIN capturé, portée territoriale du support et maintien
  des scans principal/salarié. CA-24/27/28/29/30/31/32/33 gardent leurs variantes
  multi-demandes/rotation/incident et refus moteur Animation/`ANOMALIE` au rejeu.
  Les verrous et effets testés sont réels ; les doubles d’étapes/réconciliation
  ne remplacent pas la matrice complète du moteur. Pour CA-08, un résultat déjà
  acquis peut légitimement rendre son reçu sans nouveau mouvement : ne pas exiger
  un refus uniforme d’une cible consommée avec occurrence existante.
- **CA-25 et démonstration.** Migrations 256/257 et restauration restent des
  preuves historiques réutilisées, non réexécutées intégralement sur l’état actuel.
  Rejouer l’évolution depuis schéma antérieur avec comptes/droits préexistants,
  vérifier canal inactif et scans conservés. Le générateur fournit les états PIN
  et deux demandes Coffret ; une démonstration Animation complète reste à attester.
- **CA-16 et pilote.** Aucun rapport ni confirmation d’une recette cible
  principal/client/support n’atteste les parcours Coffret/Animation, nominal,
  refus, incident et reprise. La disponibilité des guides dans le workspace
  n’était pas une publication ERP ; les notices sont maintenant reliées et
  exportables, sans publication hébergée annoncée. Consigner cible, versions,
  révision documentaire et résultats expurgés avant ouverture générale.

Ces réserves sont des exigences de clôture du
[skill utilisé](../../../.agents/skills/localeo-cloturer-epic/SKILL.md), section
« Décider et appliquer la clôture » : « Une recette en environnement déployé est
requise lorsqu’elle fait partie des critères ; une preuve locale ne la remplace
pas. » Aucun correctif métier substantiel n’est ajouté silencieusement pour
transformer cette revue en acceptation.

### Contrôles de cette reprise

Tous les tests ci-dessous utilisent des données synthétiques et des transports
simulés, sans compte métier, configuration privée ou email fournisseur.

| Contrôle rejoué | Résultat et contexte |
| --- | --- |
| Backend isolé | **779 réussis**, aucun ignoré, 55,98 s : domaine PIN/demande/commerce/conservation, réauthentification, API PIN/ERP/Bon, actions Animation, segments audit, générateur PIN, architecture/classes/use cases et batch email/réservation. `scripts/validation/test_isolated.py -q --tb=short`, base temporaire `.artifacts/pytest-e70-closure-final-isolated`, Python 3.14. Avertissement de fixture `datetime.utcnow()` conservé. |
| PostgreSQL agrégé | **104 réussis**, aucun ignoré, **585,26 s**, sortie 0 : Coffret/Animation/Bon, concurrences, notifications, conservation, salariés/périmètres, attestations moteur et transport des accès internes. Base `localeo_audit_test`, PostgreSQL 18.3 local jetable, port **16462**, schémas uniques. **118 avertissements** de fixtures conservés : cycle FK des profils/versions et `datetime.utcnow()` déprécié. |
| Pro unité/contrats | **69 réussis**, six fichiers, 43,33 s, `npm test -- src/features/pinValidation src/features/employees/EmployeeAccess.test.jsx src/lib/api/contracts.test.js src/app/merchantNavigation.test.js`. Premier passage 68 succès/1 échec de contexte routeur dans le test d’historique ; ajout de `MemoryRouter`, puis passage complet vert sans modifier ses assertions. |
| Pro navigateur | **2 réussis**, 390/1280 px, 18,6 s, `npm run test:e2e -- tests/e2e/pin-validation.spec.js --workers=1 --output=tmp/e70-closure-final-pro-pin` : génération, remplacement réellement exécuté et révocation. Build isolé ; avertissement sur l’import à la fois statique/dynamique de l’historique, sans échec. |
| Marketplace navigateur | **17 réussis**, 2,3 min : `pin-validation.spec.cjs`, `pin-validation-feedback.spec.cjs`, `pin-validation-bon-feedback.spec.cjs`, configuration `playwright.desktop.config.cjs`, sortie `tmp/e70-closure-final-pin`. API simulées, délai/reçu/reprise et absence de succès implicite. |
| Marketplace stockage de reprise | **1 réussi**, `node --test tests/security/pin-recovery.test.cjs`, aucun ignoré. |
| ERP PIN | `node tests/browser/pin-validation-erp.cjs` réussi à 390/1280 px : métadonnées, motif, révocation, timeout/relecture et refus Lecteur. |
| Lecteur et intégrité documentaire | **8 tests lecteur réussis**, puis **34 réussis / 2 ignorés** dans `test_ops_markdown_viewer.py` et `test_documentation_snapshot.py`. Les deux contrôles de symlink ne sont pas exécutés : création non autorisée sur cette plateforme. Ils ne sont pas comptés parmi les succès. |
| Générateur de bundle documentaire | `python -m unittest discover -s tests -p test_sync_documentation.py` : **15 réussis / 1 ignoré**, création de symlink non autorisée. Bundle réel et nouveau lecteur vérifiés séparément ci-dessous. |

Commande PostgreSQL exécutée depuis le backend :

```console
python scripts/validation/test_isolated.py tests/security/test_validation_pin_coffret_e70.py tests/security/test_validation_pin_animation_e70.py tests/security/test_pin_bons_lots_postgres.py tests/security/test_pin_concurrence_e70.py tests/security/test_pin_notifications_postgres_e70.py tests/security/test_conservation_pin_postgres.py tests/security/test_validations_salaries_e72.py tests/security/test_perimetres_validations_postgres.py tests/security/test_attestations_moteur_postgres_t4.py tests/integration/test_e69_transport_interne.py -q --tb=short --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:16462/localeo_audit_test --basetemp=.artifacts/pytest-e70-closure-final-postgres
```

Le premier démarrage local sur l’ancien port 16452 a échoué à ouvrir sa socket ;
la reprise sur 16462 a permis cette exécution complète. Ce changement temporaire
ne modifie aucune configuration d’environnement métier. Le serveur jetable est
arrêté après les vérifications ; aucune base d’exploitation n’a été utilisée.

Contrôles documentaires : **94 guides / 1 052 liens**, puis **24 documents /
439 liens** avec `check_guidance.py --changed --all-markdown`, aucune erreur ni
avertissement ; **131 sources** avec `sync_documentation.py --check-sources`.
`git diff --check` réussit dans projet, backend, Pro et Marketplace. Ces contrôles
ne remplacent pas les trois scénarios de symlink non exécutés sur Windows.

Les alias d’export existants restent inchangés ; la notice E70 ajoute un alias.
Revue statique : 12 chemins PIN Pro/Animation/E41 et les intersections E42
concordent ; dix DTO PIN sont identiques dans les quatre instantanés examinés,
ainsi que `actions_validation_pin` et son schéma embarqué. Ce rapprochement ne
constitue pas une recette entre applications hébergées. La divergence d’enum de
remise de gain E73 relevée dans les contrats Live reste distincte du périmètre PIN.

### Documentation et publication préparées

Le guide de formation ERP et l’aide opérationnelle contiennent désormais la
notice PIN : acteur principal, assistance habilitée, motif, confidentialité,
relecture après réponse perdue et absence d’annulation financière implicite.
Le guide complet est ajouté au manifeste sous l’alias
**`formation/validation-par-pin.md`**, source canonique inchangée de dossier.
La disponibilité cible `/internal/docs/knowledge/formation/validation-par-pin.md`
reste à contrôler après publication. L’architecture ne dit plus que les
traitements de conservation sont à implémenter : ils sont réalisés localement ;
leur ordonnancement/surveillance et leurs copies externes restent à vérifier.

Un bundle de contrôle, non versionné, est préparé dans
`localeo-backend/tmp/e70-cloture-20261101-docs`. **131 exports et le manifeste**
sont vérifiés par empreintes contre les sources (**132 entrées distribuées**).
Le vrai lecteur résout le nouvel alias vers la notice du bundle. Ce contrôle
ne publie rien sur une cible hébergée ; le bundle de livraison devra être
généré depuis la révision documentaire du futur commit retenu.

### Lots préparés et exploitation

L’index n’est pas modifié. Le lot documentaire de cette reprise comprend le
présent bilan et la matrice, README/architecture E70, backlog/note de roadmap,
notices ERP et `documentation.exports.json`. Message proposé :
`docs(e70): actualiser la revue de cloture et publier la notice PIN`.
Ce message désigne un **bilan de clôture bloquée**, sans statut Terminée.

Dans Pro, un test historique de `EmployeeAccess.test.jsx` montait directement
`ValidationHistory` sans routeur alors que le composant utilise un lien depuis
la correction UX déjà présente. Le test reçoit `MemoryRouter`, avec les
assertions de filtrage/isolation inchangées ; aucune source applicative modifiée.
Ce hunk est à isoler des autres travaux Pro. Message proposé :
`test(pro): fournir le routeur au test historique des validations`.
Les correctifs E70 backend/Marketplace/Pro des sections précédentes restent des
lots séparés à isoler des fichiers mixtes OnBoard/Live/E73 ; cette reprise ne
stage ni ne commite leurs autres modifications.

Ordre et configuration préparés, **non exécutés** :

| Composant | Action de livraison | Valeur / contrôle attendu |
| --- | --- | --- |
| Backend | Appliquer les migrations manquantes avec le runner existant, sans réécrire leurs empreintes | 256 puis 257 dans la chaîne courante ; vérifier comptes/droits et scans |
| Backend | Garder le canal fermé jusqu’à acceptation | `LOCALEO_PRO_PIN_VALIDATION_ENABLED=false`, défaut actuel ; QR préservé |
| Backend / stockage privé | Provisionner le trousseau HMAC et la clé active | `LOCALEO_PIN_VALIDATION_KEYS_JSON`, `LOCALEO_PIN_VALIDATION_ACTIVE_KEY`, sans valeur secrète dans ce dossier |
| Backend puis Pro et Marketplace/Live | Livrer des révisions compatibles et les correctifs acceptés | Contrats PIN et `actions_validation_pin` cohérents ; contrôle droits et reprise |
| Documentation / ERP | Publier la révision documentaire future et son bundle contrôlé | Nouvelle notice PIN accessible, liens ERP réécrits, empreintes conformes |
| Conservation | Ordonnancer/surveiller le CLI selon les règles existantes ; simulation d’abord | `LOCALEO_AUDIT_EXTERNAL_JSONL_PATH` partagé et `LOCALEO_CONSERVATION_DATABASE_URL` explicite ; gels et copies vérifiés |
| Pilote | Rejouer les parcours et refus restants puis la recette cible | Références de cible/versions/résultats consignées avant ouverture |

En incident, fermer le canal et préserver QR, reçus, audit et effets acquis.
Aucun rollback de données ni remboursement implicite n’est promis. Aucun
commit, push, déploiement, migration sur une base métier, notification réelle
ou purge d’exploitation n’est réalisé pendant cette reprise.
