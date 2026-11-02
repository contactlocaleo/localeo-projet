# E72 — Vérification et livraison

## Reprise de clôture sur tests — 1er novembre 2026

**Décision E72-DEC-CLOTURE-TESTS :** le porteur produit demande une clôture fondée
sur les tests unitaires, d'intégration et fonctionnels. Pilote, messagerie réelle,
appareil physique et hébergement sont suivis séparément et ne bloquent pas la
clôture. Les 22 critères et leurs comportements attendus sont conservés.

**Verdict : epic 72 Terminée le 1er novembre 2026, sur la base des tests.**
Les résultats ci-dessous complètent et remplacent, pour les points vérifiés,
les réserves de la revue historique conservée plus bas.

Bases : projet `9204f8a`, backend `7f131d3`, Pro `78c3237`, avec les modifications
locales de cette reprise. Python 3.14, PostgreSQL 18 jetable sur `127.0.0.1:16472`,
Chromium local. Aucun fichier `.env` opérateur, email réel ou base d'exploitation
utilisé. Marketplace/Live et l'application organisateur Animation sont inchangées.

### Preuves renouvelées

Les commandes Python partent du backend via `scripts/validation/test_isolated.py`.
Pour C2/C3/C5 : ajouter
`--postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:16472/localeo_audit_test`.
Cette URL désigne exclusivement l'instance jetable de la revue, pas une cible à
réutiliser sans préparation. La capacité locale de verrous a été portée à 512
pour les créations/suppressions parallèles de schémas de plus de 400 tables.

| Réf. | Commande / périmètre | Résultat |
| --- | --- | --- |
| C1 | `python scripts/validation/test_isolated.py tests/domain/identite_acces/test_acces_salaries_dedicated.py tests/domain/identite_acces/test_conservation_salaries.py tests/application/identite_acces/test_option_salaries_indisponible.py tests/api/test_salaries_e72.py tests/api/test_historique_salarie_e72.py tests/infrastructure/test_segments_audit_salaries.py tests/unit/test_salaries_email_configuration.py tests/unit/test_demonstration_salaries.py -q` ; contrôles requis `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py` | **44 tests de comportement et 623 contrôles d'architecture réussis**. |
| C2 | `python scripts/validation/test_isolated.py tests/security/test_cloture_iam_salaries_e72.py tests/security/test_iam_salaries_e72.py tests/security/test_conservation_salaries_postgres.py tests/security/test_migration_salaries_bootstrap_e72.py -q --tb=short` | **39 réussites**, 290,51 s : 18 compléments IAM, 14 IAM existants, 4 conservation et 3 migrations. |
| C3 | `python scripts/validation/test_isolated.py tests/security/test_cloture_validations_salaries_e72.py tests/security/test_validations_salaries_e72.py tests/security/test_animation_salaries_e72.py -q --tb=short` | **39 réussites**, 173,35 s : 25 compléments, 10 Coffret et 4 Animation existants. |
| C4 | `python scripts/validation/test_isolated.py tests/api/test_salaries_e72_cloture.py tests/application/use_cases/test_identite_acces_use_cases.py::TestVerifierSessionCommercant tests/application/use_cases/test_acces_preparation_commercant.py -q --tb=short` | **128 réussites** : 101 couples route/méthode interdits au salarié, 5 profils ERP, 4 injections et 18 régressions session/préparation. |
| C5 | `python scripts/validation/test_isolated.py tests/security/test_audit_refus_salaries_e72.py -q --tb=short` ; complément CA-19 rejoué séparément avec `-k test_refus_roles_erp` | **7 cas distincts réussis en deux passages (6 + 1)** : audit après rollback, isolation du commerce, refus de capacité et de lien, secrets absents, identité conservée lorsque l'ouverture globale est fermée ; Lecteur/Finance, cible existante/inconnue, requête anonyme et usurpation d'acteur refusée, corrélation et absence de création d'option. |
| C6 | Pro : `node node_modules/vitest/vitest.mjs run --config scripts/audits/vitest-e72.config.mjs --maxWorkers=2` | **128 réussites dans 12 fichiers**, 48,88 s : salariés, sessions, navigation et contrats consommés. Aucun `.env` opérateur chargé. |
| C7 | Pro : `node node_modules/@playwright/test/cli.js test tests/e2e/e72-closure.spec.js tests/e2e/employees.spec.js tests/e2e/employee-confirmation.spec.js tests/e2e/employee-management-ux.spec.js tests/e2e/employee-invitation-ux.spec.js --workers=2` | **34 réussites**, 49,6 s ; build isolé réussi. Confirmation Animation, ANOMALIE, reprise après rechargement sans rejeu, invitation et récupération publiques, navigation et gestion salariées. |
| C8 | Backend : `node tests/browser/acces-commercant-erp.cjs` | **Réussi à 390 et 1280 px** : confirmation, indisponibilité technique, conflit de version, reprise et refus de rôle. |
| C9 | Comparaison des JSON E41 canonique et Pro embarqué, références résolues récursivement et titres exclus | **14 chemins, 15 opérations, 21 schémas transitifs cohérents** : accès salariés/option, historiques et reçu Coffret. Aucun contrat à régénérer. |

Les exécutions finales terminées ci-dessus n'ont aucun skip. Les premiers passages
ont rencontré des erreurs de capacité du PostgreSQL jetable, deux préparations
de fixtures Animation et un montage de route HTTP ne transmettant pas ses
substitutions de dépendances. Les préparations ont été corrigées sans affaiblir
les assertions ; les rejeux C2/C3/C4 passent. Les avertissements SQLAlchemy sur
les métadonnées cycliques et `datetime.utcnow()` restent visibles ; le build Pro
signale l'import statique/dynamique de `ValidationHistory.jsx`.

Les tests frontend/ERP simulent API et caméra ; ils ne prouvent pas un téléphone
physique ou un service hébergé. Les tests de validation Animation contrôlent la
réconciliation du moteur pour compter les effets transactionnels ; les variantes
d'éligibilité rétablissent explicitement le vrai garde Chasse. Aucune simulation
n'est présentée comme un parcours complet du moteur. Les courses de retrait
observent l'attente PostgreSQL avec `pg_blocking_pids` avant libération du verrou.

### Matrice d'acceptation actualisée

Les propriétaires, spécifications, guides et impacts D/I/F/O restent ceux de la
matrice exhaustive ci-dessous. Cette table porte le verdict courant par critère.

| Critère | Preuve comportementale déterminante | Verdict |
| --- | --- | --- |
| E72-CA-01 | C4 : champs d'identité/rôle injectés refusés, contexte dérivé du principal ; C2/C5 : isolation persistée et autre commerce refusé. | Vérifié par tests |
| E72-CA-02 | C2 : connexion refusée avant acceptation, hash et activation ensuite ; C7 : connexion distincte, aucune session implicite. | Vérifié par tests |
| E72-CA-03 | C2 : invitation de 24 h juste avant/à/après échéance, annulation, rejeu et acceptation concurrente unique. | Vérifié par tests |
| E72-CA-04 | C2 : renvoi idempotent, ancien lien refusé, annulation bloquant acceptation et worker, envoi incertain non rejoué ; C7 : état et actions. | Vérifié par tests |
| E72-CA-05 | C2 : registre normalisé, collisions concurrentes entre commerces et principal/salarié, un seul rattachement sans écrasement. | Vérifié par tests |
| E72-CA-06 | C4/C6/C7 : capacités fermées, arrivée au scan, navigation limitée et URL interdites. | Vérifié par tests |
| E72-CA-07 | C3 : attribution salariée, validation Coffret et mouvement uniques, DTO minimal ; C7 : confirmation et reprise. | Vérifié par tests |
| E72-CA-08 | C3 : participation, terrain, calendrier, clôture, participant et garde Chasse ; C6/C7 : confirmation, ANOMALIE et reçu. | Vérifié par tests |
| E72-CA-09 | C4 : 101 couples route/méthode refusés par la vraie politique ; C3/C5 : autre commerce et historique exclus, sans effet. | Vérifié par tests |
| E72-CA-10 | C3 : QR invalide/expiré/révoqué, commerce suspendu, aucun nouvel effet ; droit consommé refusé ou reçu idempotent selon le cœur partagé. | Vérifié par tests |
| E72-CA-11 | C3 : courses deux salariés et salarié/PIN Coffret, principal/salarié Animation, effet unique ; C6/C7 : reçu sans nouvelle mutation. | Vérifié par tests |
| E72-CA-12 | C3 : deux ordres révocation/validation Coffret et Animation, refus après retrait, effets antérieurs conservés. | Vérifié par tests |
| E72-CA-13 | C4 : gestion salariés/PIN et autres fonctions interdites ; C3 : appels directs au service PIN refusés. | Vérifié par tests |
| E72-CA-14 | C1/C3/C6 : projection minimale, filtres, pagination, archives et autre commerce exclus ; aucun droit financier. | Vérifié par tests |
| E72-CA-15 | C2/C3 : traces nominales et attribution ; C5 : refus contextualisés persistés après rollback, corrélation et absence de secrets. | Vérifié par tests |
| E72-CA-16 | C2 : reset 1 h aux bornes, usage unique concurrent, sessions du seul salarié invalidées, principal/collègue préservés ; C6/C7 : récupération et purge locale. | Vérifié par tests |
| E72-CA-17 | C2 : migrations et collisions de reprise, récupération/initialisation du principal vers préparation après v258, droits conservés sans salarié implicite. | Vérifié par tests |
| E72-CA-18 | C6/C7 : mobile, refus caméra, saisie manuelle, interruption et reprise sans faux succès ni double effet. Appareil physique séparé selon la décision produit. | Vérifié par tests |
| E72-CA-19 | C2 : option inactive à l'initialisation ; C4 : Admin/Backoffice/cumul autorisés, Lecteur/Finance seuls refusés, CSRF ; C5 : refus ERP audité avec acteur vérifié et commerce relu, aucune option créée. | Vérifié par tests |
| E72-CA-20 | C2 : six invitations, acceptations et connexions réelles aux services, six identités/sessions distinctes. | Vérifié par tests |
| E72-CA-21 | C2 : deux ordres désactivation/invitation/acceptation ; C3 : retrait/validation, liens annulés, principal et preuves conservés. | Vérifié par tests |
| E72-CA-22 | C2 : réactivation puis nouveau login, anciennes sessions/liens refusés, révocation individuelle conservée, nouvelle invitation utilisable. | Vérifié par tests |

### Correctifs et limites de livraison

L'anomalie **E72-CLOT-20261101-AUDIT** est corrigée : capture d'un contexte typé
issu des objets vérifiés, persistance hors de la transaction métier annulée,
conservation du contexte d'authentification pour les refus ultérieurs. Les routes
du moteur propagent désormais le refus salarié vers son handler dédié au lieu
de le convertir en erreur de saisie 422. L'API conserve les refus d'autorisation
403 attendus ; aucun droit supplémentaire ni contournement ajouté.
Le refus de rôle ERP produit `acces_salarie.option.refus` : lecture seule de la
cible existante pour l'audit, acteur vérifié, aucun chargement créateur d'option,
aucune cible attribuée à un anonyme ou à un identifiant inconnu. Les contrôles
d'authentification, de capacité, de CSRF et d'origine restent inchangés.
Les revues indépendantes finales n'identifient pas de défaut résiduel dans ce lot.

Décompte sans doubles exécutions : **795 tests/contrôles backend isolés**
(623 architecture, 44 comportement, 128 HTTP/session), **85 tests PostgreSQL**
(39 IAM/conservation/migration, 39 validation, 7 audit), **128 tests Pro** et
**34 scénarios navigateur Pro**, plus le script ERP exécuté sur deux formats.
Après le dernier complément CA-19, les 623 contrôles d'architecture, les 110
nouveaux tests HTTP et les 3 tests API salariés existants ont été renouvelés
ensemble : **736 réussites**, non ajoutées au décompte unique. Le complément
PostgreSQL CA-19 renforcé a été rejoué avec succès en 18,95 s.

Les correctifs Pro de nettoyage de session et d'UX invitation/gestion salariés
sont inclus dans la base testée `78c3237`. Cette reprise ajoute leurs preuves et
celles de la confirmation Animation/récupération ; aucun code fonctionnel Pro
supplémentaire n'a été nécessaire. La dette **E72-CLOT-20261101-LISTE** reste
documentée : lecture SQL non bornée de la liste de gestion, sans changement de
pagination ni de volumes dans cette reprise d'audit. Elle ne constitue pas un
nouveau critère de clôture ; sa correction et sa mesure restent à planifier.

Les migrations v258/v259 et le générateur n'ont pas changé. C1/C2 renouvellent les
preuves ciblées ; les rapports de génération complète historiques sont conservés
comme tels, sans prétendre avoir régénéré un environnement réel. Aucun secret,
nouvelle variable ou configuration distante n'est créé par ce correctif.

Le tableau **Configuration et mise en service à préparer** de la revue historique
reste la référence opératoire : migrations compatibles, trousseau privé commun
API/worker, origine Pro HTTPS, ouverture technique, conservation et bundle ERP.
Ces opérations et la recette déployée n'entrent pas dans le verdict de clôture
selon E72-DEC-CLOTURE-TESTS. Livraison recommandée : backend/worker puis Pro,
publication de la révision documentaire, activation ERP explicite par commerce.
Le drapeau global n'active aucun commerce. Conserver les tables et attributions
en reprise ; aucun rollback destructif n'est prescrit.

Lots préparés, sans indexation, commit, push ni déploiement : backend (audit et
tests, message proposé `fix(e72): tracer les refus et completer les preuves`),
Pro (tests et configuration isolée, `test(e72): couvrir les parcours salaries`),
projet (bilan, guides et classement après succès des contrôles documentaires).

Clôture documentaire : backlog unique déplacé dans `roadmap/terminees`, liens
entrants et index actualisés ; 63 epics terminées et 3 en cours sur les
78 identifiants suivis. `check_guidance.py` réussit, ainsi que
`check_guidance.py --changed --all-markdown` et le contrôle explicite du backlog
déplacé (95 guides, 1 080 liens, aucune erreur). Les **134 sources exportées**
sont vérifiées ; bundle local dans `localeo-backend/tmp/e72-closure-final-20261101-docs`,
**135 entrées distribuées contrôlées**, manifeste compris, par
`scripts/documentation/check_documentation_snapshot.py --manifest tmp/e72-closure-final-20261101-docs/documentation.snapshot.json --source ../localeo-projet`.
Le lecteur réel `resolve_ops_document('formation/acces-salaries.md')` résout
l'alias et retrouve la notice actualisée. Ce bundle vient de l'arbre local,
pas d'une révision publiée ; le régénérer après le futur commit documentaire.
`git diff --check` réussit dans les trois dépôts modifiés. Le serveur PostgreSQL
jetable a été arrêté après les tests. Les travaux d'onboarding préexistants et
`debug.log` restent hors du lot de clôture.

Ce document conserve les bilans historiques et la revue de clôture du 1er novembre ci-dessous. La migration TEST du 8 octobre est attestée dans sa section ; elle ne prouve pas la recette fonctionnelle. Aucun déploiement, envoi réel ou changement de configuration distante n’est effectué pendant cette revue. Références : [parcours](README.md), [architecture et contrats](architecture-contrats.md), [backlog](../../roadmap/terminees/epic-72-acces-salaries-validation-localeo-pro-backlog.md).

## Correctif UX salariée — 9 octobre 2026

**E72-CORR-20261009-UX**, base Pro `03005fd` et changements locaux : le salarié
utilisait un en-tête et un menu dédiés, distincts du cadre de l’accès commerçant.
La correction réutilise les composants communs d’en-tête, de navigation mobile
et latérale et de menu du compte. Le scanner et l’historique reprennent les styles
opérationnels. Les destinations restent limitées aux capacités salariées ; aucun
chargement de profil ou de finance n’est ajouté. Les états de session, refus,
reprise incertaine et confirmation explicite restent applicables.

La revue indépendante du shell ne relève pas d’écart de permissions ou de
régression du principal. Les liens juridiques du pied de page restent accessibles
par les routes publiques. Preuves locales : **38 tests unitaires** réussis (navigation et compte principal/
salarié, session et caméra) et **13 scénarios navigateur** réussis, dont sept
salariés et six de non-régression de l’en-tête principal. Les scénarios salariés
contrôlent le scanner et l’historique à 320, 390 et 1 280 pixels, les deux entrées
autorisées, le compte réduit, l’absence d’appels de gestion et de débordement
horizontal, ainsi que l’arrivée automatique sur le scanner. Sources :
`tests/e2e/employees.spec.js`, tests de navigation, compte et salariés dans Pro.
Après ajustement de l’espacement du panneau scanner, les trois scénarios
responsive sont réexécutés avec succès. Builds production et navigateur réussis.
Captures locales contrôlées dans `localeo-commercant/tmp/employee-shared-shell-final/`.
La caméra est simulée dans les tests ; aucune recette sur appareil physique
ou environnement de test déployé n’est revendiquée.

Périmètre : Pro et documentation. Aucun contrat API, schéma SQL, paramètre de
configuration, donnée ou scénario du générateur ne change ; aucune migration ou
nouvelle génération nécessaire. Backend, Marketplace et Animation inchangés.
Aucun déploiement ni recette distante effectué pour ce correctif.

## Correctif ERP — 8 octobre 2026

Sur le test exécutant `1.0.0+07942f4`, cinq refus d’activation
`OPTION_SALARIES_INACTIVE` sont relevés dans l’audit entre 11:33 et 11:46 UTC.
L’ouverture technique globale est fermée. Le statut 403 faisait également traiter
ce refus par l’ERP comme une session expirée.

Correction locale : statut 409 pour cette seule activation techniquement
indisponible, conservation du code d’erreur par le client ERP, message explicite et
session conservée. Aucun contournement de l’option globale ou des permissions.
Les tests reproduisent l’échec avant correction puis vérifient le refus sans
transaction, la lecture et la désactivation toujours possibles, et le parcours
ERP mobile/ordinateur avant puis après ouverture technique.

Preuves : 473 tests Python réussis (architecture obligatoire, orchestration ciblée
et API E72), scénario navigateur `tests/browser/acces-commercant-erp.cjs` réussi
en 390 et 1280 pixels. Pas de migration ni de modification du générateur : aucune
donnée, transition métier ou structure persistée ne change. Pro, Marketplace et
Animation ne consomment pas cette commande ERP ; aucun changement requis.

Limite : correctif non déployé et configuration Render non modifiée lors de ce
contrôle, l’accès au tableau de bord nécessitant une connexion. La recette réelle
d’activation reste à effectuer après ouverture technique selon le
[guide d’exploitation](guide-utilisation-exploitation.md#activation-erp-indisponible).

## Clarification des variables — 8 octobre 2026

Sur la base backend `d7a9e63`, les variables d’ouverture et de chiffrement des
invitations adoptent le préfixe `LOCALEO_PRO_ACCESS_SALARIES_` et les clés remplacent
`REMISE` par `INVITATION_ENCRYPTION`. L’API, le traitement email, la démonstration
et leurs fixtures utilisent les nouveaux noms. L’URL dédiée salariés est supprimée :
les liens d’invitation et de récupération réutilisent l’origine HTTPS du modèle
d’initialisation du responsable, sans en reprendre le chemin ni les paramètres.

Preuves locales : 493 tests réussis, incluant contrôles d’architecture obligatoires,
API, option ERP, démonstration unitaire et composition email. Après ajout du contrôle
du drapeau actif/inactif, les 17 tests de configuration email réussissent. Les
tests vérifient le chiffrement réel avec les nouvelles variables, les deux chemins
salariés, le fragment du jeton et le refus des origines invalides.

Aucune migration SQL ni modification des routes frontend : seule la configuration
des consommateurs backend change. La fixture d’intégration du jeu de démonstration
est renommée ; génération complète PostgreSQL non réexécutée pour ce changement.
Le [guide](guide-utilisation-exploitation.md#renommage-de-configuration--8-octobre-2026)
décrit la bascule des variables en conservant les clés et identifiants existants.
Configuration distante, commit, push et déploiement non effectués pour ce lot.

## Correctif CORS connexion Pro — 9 octobre 2026

Sur le test `1.0.0+0a0057c`, reproduction sans identifiants du précontrôle
`OPTIONS /protected/identite-acces/commercants/auth/login` : origine
`https://test-commercant.localeo.city`, méthode POST et en-têtes
`content-type,x-localeo-pro-contract` donnent 400 `Disallowed CORS headers`.
L’origine est acceptée ; l’en-tête de compatibilité E72 manque dans la liste backend.
Le navigateur bloque donc la connexion avant toute vérification du mot de passe.

Le premier correctif CORS (479 tests réussis) est remplacé avant publication par
l’arbitrage du 9 octobre : suppression de l’en-tête de compatibilité, aucune
ancienne version déployée n’étant à prendre en charge. Pro ne l’envoie plus ;
login et validation de session backend n’exigent plus ce marqueur. Les contrôles
serveur du compte, du mot de passe, de l’option, du commerce et des générations de
session restent en place. Aucun ajout manuel CORS nécessaire pour le nouveau client.
Les tests de précontrôle couvrent les en-têtes réellement utilisés et maintiennent
les refus des origines et en-têtes inconnus. Aucun impact SQL, données de
démonstration ou schéma OpenAPI (l’en-tête était lu directement dans la requête).
Backend et Pro doivent être livrés ensemble ; pas de déploiement effectué ici.

Preuves après suppression : 482 tests backend réussis (architecture obligatoire,
API et CORS), puis les 14 tests de sécurité salariés exécutés séparément sur
PostgreSQL jetable réussissent, sans skip. Pro : 19 tests session/salariés réussis.
Le précontrôle couvre POST login et GET validation de session. Les contrôles
documentaires et des 122 sources exportées passent. Aucune connexion réelle ni
livraison distante réalisée ; modifications locales non committées.

## Matrice exhaustive des critères

### E72-EVOL-20261009-ACCUEIL — contextualisation et scan immédiat

Critères précisés sans renumérotation : **CA-01/02** (email d’initialisation),
**CA-06** (arrivée directement au scan), **CA-18** (autorisation/refus caméra et
reprise). CA-07/08/11/12/15/16 restent à préserver : confirmation explicite,
unicité, révocation, secrets et récupération distincte.

Le worker transmet le nom du commerce et l’échéance persistée au composeur,
sans modifier le stockage chiffré. HTML échappé et texte décrivent le rattachement,
les droits, le mot de passe personnel, la connexion au scanner et l’aide. Les
invitations déjà en attente bénéficient du nouveau contenu lors de leur remise.
La destination salariée reste `/validation`. Le formulaire de connexion perdait
les champs `acteur`, `capacites` et `option_salaries_active` avant de transmettre
la session : leur conservation corrige le détour initial par le parcours principal.
La session et la route courante sont vérifiées avant montage du scanner, afin
d’éviter une double ouverture de caméra pendant les transitions de connexion.
La caméra est ouverte à l’entrée si autorisée et si aucune validation incertaine
n’attend une relecture.

Backend : **467 contrôles d’architecture**, **21 tests unitaires email** et
**4 tests PostgreSQL ciblés** réussis. Ils couvrent nom malveillant échappé,
échéance réelle, finalités initialisation/reset, propagation du contexte serveur,
envoi hors transaction, non-persistance des secrets, clé absente et remise
incertaine non rejouée. Aperçu synthétique mobile à 390 px inspecté, ressources
externes bloquées ; aucun email réel envoyé. Revue indépendante code/tests sans
écart identifié sur le périmètre email et caméra.

Pro : **24 tests Vitest** et **6 scénarios navigateur** réussis après correction
de la transmission d’identité à la connexion. Ils vérifient attente de la
vérification serveur, ouverture caméra unique sans clic, QR Coffret/Animation sans
confirmation automatique, refus/réessai, décodeur absent, arrêt des pistes et
résultats/permissions tardifs ignorés. Le flux vidéo est simulé ; la capture mobile
atteste l’écran d’arrivée, pas une lecture physique de caméra.
Le header salarié, distinct de celui du responsable, est également compacté
selon la demande mobile précédente : marque/commerce sur une ligne, menu clavier
avec historique/récupération/déconnexion, contrôles à 320 et 390 px. Les autres
travaux locaux sur les headers PWA restent conservés séparément.

Impacts : backend et Pro concernés ; pas de route ni DTO OpenAPI modifié, aucune
migration SQL/configuration supplémentaire. Marketplace et Animation ne consomment
pas le parcours salarié. Générateur sans changement de données ou d’habilitation :
ses comptes utilisent les mêmes flux ; fixtures email adaptées au contexte du
composeur. Pas de génération réelle, commit, push ou déploiement pour ce lot.
L’autorisation caméra reste celle du navigateur ; sans API de décodage QR prise
en charge, le repli manuel reste nécessaire. La recette sur appareils physiques
reste distincte des simulations locales.

Les lignes suivantes sont les scénarios de référence ; leurs preuves locales figurent dans le bilan ci-dessous. Les codes D/I/F/O désignent les impacts détaillés après la matrice, pas une preuve de succès.

| Critère | Propriétaire/comportement | Preuve prévue et refus déterminant | Impacts |
| --- | --- | --- | --- |
| E72-CA-01 | Identité, invitation commerce courant | Domaine + API principal A ; commerce injecté B/role arbitraire refusés ; worker email fictif | D1/I1/F1/O1 |
| E72-CA-02 | Identité, activation | Invitation valide, mot de passe conforme ; rien avant consommation atomique, connexion distincte | D1/I1/F1/O1 |
| E72-CA-03 | Identité, token unique 24 h | Horloge juste avant/à/après expiration ; annulé/utilisé ; deux transactions acceptent le même lien : un succès | D1/I1/F1/O1 |
| E72-CA-04 | Identité/outbox, renvoi | Ancienne génération refusée ; retry même clé ; email échec/reprise ; worker après annulation sans réactiver | D1/I1/F1/O1 |
| E72-CA-05 | Identité, email unique | Casse/espaces ; principal existant ; même/autre commerce ; invitations concurrentes inter-tables, aucun rôle ou hash remplacé | D1/I1/F1/O1 |
| E72-CA-06 | Identité/Pro, navigation | Playwright mobile login salarié vers scanner ; URL et menu principal refusés ; historique seul autre écran métier | D2/I2/F2/O2 |
| E72-CA-07 | Exploitation, validation | Domaine/API Coffret par salarié, acteur individuel et commerce distincts, reversement unique ; DTO sans données financières | D2/I3/F2/O2 |
| E72-CA-08 | Animation, passage | QR commerce participant, calendrier/service/étape éligibles ; acteur individuel ; administration inaccessible | D2/I3/F2/O2 |
| E72-CA-09 | Identité, isolation | Matrice exhaustive routes commerçantes : autre commerce, IDs altérés, finance/Chorus/documents/messages/PIN ; nouvelle route refusée par défaut | D2/I2/F3/O2 |
| E72-CA-10 | Exploitation/Animation, refus | QR invalide, expiré, droit consommé, commerce suspendu ; aucune consommation/progression/récompense | D2/I3/F2/O2 |
| E72-CA-11 | Exploitation/Animation, concurrence | Double clic, deux salariés, principal et PIN ; un effet ; reçu après timeout ; aucun retry automatique frontend | D2/I3/F2/O2 |
| E72-CA-12 | Identité + domaine consommateur | Deux ordres réels validation/révocation avec verrous ; session ouverte, transaction ouverte ; refus après commit révocation | D1/I3/F3/O2 |
| E72-CA-13 | Identité, gestion interdite | Appels directs invitation/PIN/configuration/rôle depuis salarié ; 403, sans effet ni secret | D1/I2/F3/O2 |
| E72-CA-14 | Projection historique | Tous auteurs/modes de A seulement ; filtres/pagination bornés, résultat ancien sans auteur ; pas montant/client/email/export | D2/I2/F2/O2 |
| E72-CA-15 | Identité/audit | Événements nominals et refus ; acteur vérifié ; recherche de secrets dans logs/outbox/erreurs/DTO ; rétention par catégorie | D3/I1/F3/O3 |
| E72-CA-16 | Identité/session/Pro | Reset 1 h aux bornes/rejeu/concurrence, révoque seul salarié ; suspension/révocation inchangées ; caches nettoyés ; token URL nettoyé | D1/I1/F3/O1 |
| E72-CA-17 | Identité, migration principal | Reprise base ancienne, login/reset/préparation E68 inchangés ; pas salarié implicite ; principal garde droits ; collision email arrête migration | D3/I1/F1/O4 |
| E72-CA-18 | Pro, mobile/reprise | Caméra refusée, clavier, lecteur écran, réseau interrompu ; réponse incertaine puis reçu, aucun faux succès/hors ligne | D2/I3/F2/O2 |
| E72-CA-19 | Identité/ERP, option | Valeur false initiale ; Admin/Backoffice et combinaison Backoffice+Finance autorisés ; Lecteur/Finance seuls/API Pro refusés ; CSRF/version | D1/I1/F4/O4 |
| E72-CA-20 | Identité, sans plafond | Activer un sixième puis plusieurs comptes sans réservation invitation ; contrôles de débit ne deviennent pas quota produit | D1/I1/F1/O1 |
| E72-CA-21 | Identité + validation | Désactivation concurrente acceptation/invitation/confirmation ; sessions bloquées, invitations annulées atomiquement ; principal préservé | D1/I3/F4/O4 |
| E72-CA-22 | Identité, réactivation | Nouveau login non révoqué accepté ; ancien token/session/invitation refusés ; révoqué exclu ; pas restauration version ancienne | D1/I1/F4/O4 |

**D1** : notices responsable/salarié, récupération et guide ERP ; **D2** : scanner/historique et présentation onboarding E68 ; **D3** : audit, politique de données et livraison. **I1** : contrats identité/ERP ; **I2** : session/capacités et DTO minimaux ; **I3** : validation/reçu/attribution.

## Démonstration et fixtures

Le générateur reste dans backend `scripts/demonstration/`, avec ses instructions locales. Adapter `generator.py`, les producteurs d'accès, `table_registry.json`, vérification, nettoyage/restauration et rapport d'accès ; ne pas déposer de données générées dans le projet documentaire.

- **F1** : responsable A, au moins six salariés actifs, autre commerce B, invitations valides/24 h expirées/annulées/utilisées et erreur de remise ; emails fictifs, aucun envoi réel.
- **F2** : validations Coffret/Animation par principal, deux salariés et PIN lorsque E70 installée ; validation historique sans auteur, droits consommés, calendrier fermé, service indisponible. E72 seule utilise fixtures de mode PIN sans requérir sa mise en production.
- **F3** : salarié révoqué, reset valide/une heure expiré/utilisé, commerce suspendu, session avant changement de mot de passe, tentative d'API interdite. Secrets uniquement dans artefacts d'accès protégés prévus par le générateur, jamais le rapport public.
- **F4** : option désactivée, activation, désactivation avec invitations/sessions ouvertes, réactivation et salarié révoqué conservé ; profils ERP autorisés/refusés.

Les vérificateurs de démonstration attestent permissions et relations, pas seulement l'existence des lignes. Ajouter tests du registre de tables/reset et des générations de session ; aucune génération sur environnement réel au titre de cette spécification.

## Exploitation et compatibilité

- **O1 — Email et assistance** : lien Pro sur origine autorisée, template échappé, email sans mot de passe, expiration à partir de création serveur ; état de remise récupérable, renvoi explicite. Assistance : vérifier l'identité via procédures existantes, orienter vers responsable ; ne jamais lire token ou créer un mot de passe pour le salarié.
- **O2 — Validation** : surveiller refus d'autorisation, conflits et reçus en attente ; corrélation par IDs sans QR. Une panne ne déclenche pas validation différée. Les règles de scan et finance existantes restent propriétaires de leurs effets.
- **O3 — Données** : implémenter et tester le [rattachement commun de conservation](../identite-acces/conservation-validations-acces.md), vérifié sur l'Annexe A le 7 octobre. Contrôler les dates qualifiées, archives, gels, secrets, anti-rejeu et toutes les copies SQL/JSONL ; ne pas confondre existence de la règle documentaire et purge livrée.
- **O4 — Déploiement** : préflight collisions login, sauvegarde selon procédure existante, migration additive, backend compatible principal, régénération contrat Pro, frontend compatible, recette pilote puis activation ERP. Désactivation globale d'exploitation empêche nouvelles activations si rollback nécessaire ; désactiver les options et sessions salariées avant revenir à un backend ne connaissant pas ces identités. Conserver tables/attributions ; aucun downgrade destructif ni réutilisation de session historique.

À l'implémentation : tests de domaine sans ORM, application avec ports factices, intégration concurrence PostgreSQL isolée et API avec profils ; tests Vitest contrats/session/navigation, Playwright mobile/scanner/acceptation/reset ; runner isolé backend et commandes locales des README. Compléter par contrôles d'architecture concernés, sans présenter build/import comme preuve d'autorisation. Regénérer OpenAPI documentaire et embarqué depuis producteurs effectifs, puis tests des consommateurs.

## État historique de préparation — 5 octobre

La conception fonctionnelle, les contrats cibles et la matrice de preuves couvrent les 22 critères. Aucun code applicatif, migration ou test métier E72 n'est livré avec ces documents. Le rattachement de conservation à sa source existante est établi le 7 octobre ; les traitements correspondants et leurs tests restent requis avant livraison. Les collisions éventuelles de login sont une condition de préflight à mesurer, pas une décision de fusion implicite. Dates/priorité de livraison restent dans la roadmap.

## Contrôles documentaires réalisés

Le 5 octobre, revue indépendante des contrats E70/E72 puis revue ciblée après
correction des notifications, chemins, ordre des verrous, résolution invitation
et formulation de la révocation individuelle : aucune incohérence bloquante
restante relevée dans ce périmètre. La résolution du lien doit être testée sans
consommation du token, et la remise email doit être testée sans secret en clair
dans l’outbox générale, avec suppression de sa charge chiffrée après remise ou expiration.

Contrôle Node de 292 liens locaux sur 13 documents : aucune cible manquante.
Matrices : 34/34 critères E70 et 22/22 critères E72, sans manque ni doublon.
`git diff --check` réussi. `python scripts/check_guidance.py --changed` non exécuté :
Python absent de l’environnement accessible. Le contrôle de remplacement ne valide
ni les ancres ni les lecteurs. Aucun export documentaire modifié, aucun contrat
OpenAPI généré ou test applicatif exécuté. Lors du contrôle du 5 octobre, le PDF Annexe A n’avait pas pu être extrait. Son extraction du 7 octobre et le rattachement commun lèvent cette limite documentaire.

## Contrôle documentaire du rattachement — avant implémentation

Annexe A extraite et rattachement commun établi ; revue indépendante ciblée sans
incohérence bloquante relevée. Contrôle Node : 94 liens locaux sur 10 documents,
aucune cible manquante ; matrices inchangées, 34/34 critères E70 et 22/22 E72,
sans doublon. `git diff --check` réussi. `python scripts/check_guidance.py`
non exécuté : Python introuvable. Le contrôle de remplacement ne vérifie ni les
ancres ni les consommateurs. Aucun fichier exporté modifié ; aucune purge,
migration, activation de job ou test applicatif exécuté.


## Bilan d’implémentation locale — 8 octobre 2026

E70 a été publiée avant le début de l’implémentation E72. L’état reste **En cours** :
les preuves locales ne constituent ni une activation ERP réelle ni une recette de
production. Backend/ERP, Localeo Pro et documentation sont les dépôts concernés.
Marketplace et partenaire Animation ne reçoivent pas de nouvelle identité ; leur
contrat de jeu reste inchangé. L’attribution passe par les cœurs métier existants.

| Critères | Réalisation et preuves locales |
| --- | --- |
| CA-01 à 05, 16, 17, 19 à 22 | Domaine `acces_salaries`, service `GestionSalaries`, API et registre partagé. 14 scénarios PostgreSQL IAM réussis : migration complète et collision avant reprise, renommage principal/collision/rollback/suppression, liens uniques et acceptation concurrente, idempotence, six accès sans plafond, option/epoch, reset isolé et header de compatibilité. |
| CA-06, 09, 13, 18 | Liste fermée de capacités côté serveur, scanner salarié séparé des chargements de profil/finance, refus des URL Pro interdites. Tests API d’isolation et navigateur mobile/desktop ; le test du vérificateur refuse également une opération inconnue avec un scope de validation. |
| CA-07, 10 à 12, 14, 21 | `test_validations_salaries_e72.py` : 10 scénarios PostgreSQL réussis, dont les deux ordres validation/révocation, relecture après retrait de droits, attribution et initiateur, reçu d’une validation gagnée par PIN, refus de gestion PIN directe et exclusion des archives. |
| CA-08, 10 à 12, 14 | `test_animation_salaries_e72.py` : 4 scénarios PostgreSQL réussis, attribution salariée, principal/salarié concurrents, reçu refusé après suspension, validation révoquée sans progression et sortie de l’historique à fin d’usage courant. |
| CA-14, 15 | Projection historique paginée (20 par défaut, maximum 100), tous modes, filtre tenant exclusivement serveur ; aucun montant, client nominatif, secret ou export. 3 tests API/projection réussis ; archives Coffret exclues et échéance Animation évaluée par la politique existante. |
| CA-06, 16, 18 | Pro : lot initial de 35 tests ciblés réussi, puis fichier salariés enrichi au lien fragment réel (12 tests réussis). 3 Playwright réussis avec code de sortie 0 : 390/1280 px, reprise après réponse perdue et invitation `#token=` nettoyée sans session implicite. Build navigateur isolé réussi. |
| Contrats / compatibilité | OpenAPI E41 et embarqué Pro régénérés offline depuis 728 routes. 60 tests Pro de contrats réussis. 46 tests exploitation/API et 7 tests scan Animation réussis ; 18 scénarios de préparation Animation inchangés réussis. Les doubles de tests transmettent désormais la session vérifiée, sans retirer d’assertion métier. |
| Architecture | 467 contrôles obligatoires réussis : frontières, classes du domaine et couverture des use cases. |
| ERP / support | 3 tests API réussis ; parcours navigateur ERP à 390/1280 px pour activation/désactivation, contrôles de droits et version, avec régression des accès existants. |

La revue indépendante a corrigé le registre lors d’un changement de login, le
reset principal qui ne doit pas révoquer les salariés et les métadonnées de session
après rafraîchissement. Les régressions correspondantes sont testées. Le PIN reste
une identité partagée du commerce ; aucune validation PIN n’invente un auteur salarié.

Migrations **258 puis 259** après E70. Configuration, clés, worker, qualification de
fin de relation, conservation et reprise sont décrits dans le
[guide d’utilisation et d’exploitation](guide-utilisation-exploitation.md).
Aucune clé, invitation réelle ou donnée client n’est incluse dans les livrables.

Contexte : backend de base `776e852`, Pro `81c9b21`, projet `73cbce9`, modifications
locales E72 ; Python 3.12.10 et dépendances verrouillées, PostgreSQL18 jetable et
Chromium. Les comptes/mails de test sont fictifs. Recette pilote, configuration
opérateur, ordonnancement et activation par commerce restent des actions de mise
en service, non effectuées par cette implémentation.

La remise email est vérifiée hors transaction et en concurrence : un second worker
ne transforme pas une remise récente en échec ; une configuration invalide produit
un échec distinct d’une invitation annulée. Les deux régressions PostgreSQL passent.
Le conflit du registre de login partagé est traduit en erreur métier 409, y compris
pour le parcours principal E68, avec rollback testé. Les refus sont audités sans secret.

Conservation et démonstration : 26 tests ciblés réussis (conservation E70/E72,
segments d’audit, fixtures), dont la concurrence de purge sur deux commerces d’une
même Animation et le reçu d’idempotence principal conservé comme marqueur expiré.
Les 116 tests unitaires du générateur passent. Le résultat de la recette PostgreSQL
complète du générateur est consigné ci-dessous après son exécution.

Revue finale indépendante : les défauts de concurrence email et purge sont levés.
Le marqueur de commande purgée retire aussi l’empreinte de l’email, remplacée par
une constante ; les quatre tests PostgreSQL de conservation E72 repassent.
Contrôles documentaires : `check_guidance.py` réussi (92 guides, 968 liens),
`sync_documentation.py --check-sources` réussi (122 documents), puis contrôle
Markdown de l’index préparé réussi (16 documents, 305 liens). `git diff --check`
et la vérification de l’index Git réussissent. Les modifications E71 de l’utilisateur
restent hors des commits E72.


### Démonstration — résultat final

Le runner officiel a exécuté `tests/integration/test_demo_dataset.py`,
`tests/integration/test_demo_lifecycle.py` et
`tests/integration/test_demo_reset_schema.py` sur deux instances PostgreSQL jetables.
Premier passage : **6 réussites, 1 échec** en 493,79 s ; l’échec portait exclusivement
sur une attribution Animation salariée manquante dans la fixture. Le générateur
corrigé est revérifié par
`test_salaries_scenarios_generated_and_restored_without_public_secrets` :
**1 réussite en 58,25 s, code de sortie 0**. Aucun échec restant dans ce périmètre.
Ce second contrôle ciblé ne représente pas une seconde exécution de tout le runner.

Sont vérifiés : six salariés actifs sans plafond, attributions Coffret/Animation,
liens d’invitation et reset dans leurs différents états, sessions invalides,
absence de secrets publics, sauvegarde/installation/reset/restauration, registre
partagé et hashguard des sources applicatives. Les avertissements SQLAlchemy du
runner ne sont pas des skips. Le répertoire temporaire a été redirigé vers
`.artifacts/` pour contourner le refus d’accès du répertoire temporaire Windows,
sans modifier les assertions ni les garde-fous d’isolation.

Commande de référence sur instances explicitement jetables :
`python scripts/validation/run_demo_compatibility_tests.py --disposable-postgres 127.0.0.1:55439,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"`.
Aucune base de démonstration partagée ou de production n’a été modifiée.

### Commits applicatifs E72

- Backend/ERP : `d11bc74` (après E70 `776e852`).
- Localeo Pro : `eb7f8bc` (après E70 `81c9b21`).
- Documentation : commit E72 portant ce bilan ; les modifications E71 restent locales.

Les commits et leur publication sont distincts de l’application des migrations,
du déploiement et de l’activation de l’option. Ces opérations ne sont pas réalisées.


## Migration de la base de test — 8 octobre 2026

Sur demande explicite, les migrations 256 à 259 ont été appliquées à la cible
configurée par `.env.test`, contrôlée distincte de la production. Le gestionnaire
officiel ne signale plus aucune migration en attente. Le contrôle final confirme
le registre de tous les identifiants principaux, les deux déclencheurs actifs et
zéro option salariés activée. Aucune génération de données ni invitation envoyée.

La première tentative a appliqué 256/257 puis annulé 258 sur `42P07` : le bootstrap
avait déjà créé les six tables salariées vides, sans les nouvelles colonnes des
tables existantes ni les defaults SQL et CHECK attendus. La correction de
compatibilité complète ce schéma sans supprimer de données. Les empreintes LF/CRLF
de la version initiale 258 sont explicitement reconnues par le gestionnaire : une
base déjà migrée ne rejoue pas cette migration, et le contrôle d’intégrité subsiste.

Reproduction locale : nominal réussi, précréation ORM en échec avant correction.
Après correction : **15 tests réussis**, dont bootstrap partiel/complet, préservation
d’une session salariée et de comptes révoqués, defaults et CHECK, refus des
collisions et compatibilité du gestionnaire. Revue indépendante sans blocage restant.
Les migrations 258/259 ont ensuite réussi sur la cible de test, avec contrôle final.
Contrats API et interfaces inchangés ; les scénarios de migration couvrent également
la création nominale utilisée par le générateur. Aucun accès à la production.

La sauvegarde locale complète proposée avant opération a été refusée par le
contrôle automatique, car elle aurait copié des données potentiellement sensibles
hors du périmètre demandé. Aucune copie n’a été créée. Les migrations ont été
exécutées dans les transactions du gestionnaire ; aucune restauration n’a été faite.
Ce résultat prouve la migration de test, pas une recette fonctionnelle à distance
ni l’activation des fonctionnalités.

## Historique des validations exploitable — 1er novembre 2026

**PRO-HISTORIQUE-UX-20261101**, correctif demandé sur Localeo Pro `/validations`.
Base Pro **`0c8499e` avec modifications locales**, documentation **`9c74a33`
avec modifications locales**. Le scénario E70 de remplacement PIN déjà modifié
reste préservé et hors du présent correctif.

Constat : formulaire vertical emprunté à la gestion PIN, codes de type/mode et
résultat peu lisibles, référence longue toujours visible, absence de réinitialisation
et de distinction entre filtres saisis et appliqués. Trois nouveaux tests
reproduisent ces manques avant correction. La source est `ValidationHistory.jsx`,
commune au responsable et au salarié ; l'API du flux fonctionne déjà par curseurs.

La page réutilise le template `BusinessWorkspace` et les badges communs, avec
un module CSS local dédié remplaçant l'emprunt des styles PIN. Header, lien scanner
selon capacités, filtres type/mode/dates compacts, pictogrammes, résultat en badge,
date/auteur lisibles et référence dépliable structurent la consultation. Une
anomalie, une annulation ou un résultat inconnu n'est jamais présenté comme succès.
Le retrait de l'import de la page de gestion PIN ne modifie pas ses commandes.

**Aujourd’hui** et **7 derniers jours** appliquent des journées civiles de Paris,
y compris lors des changements d'heure. **Réinitialiser** revient à la première
page ; **Actualiser** relit le curseur courant. Le résumé indique uniquement le
nombre d'éléments de cette page. Les résultats restent filtrés par le serveur,
25 par page, sans téléchargement global ni recherche locale pouvant masquer
des éléments non chargés. Les libellés de pagination restent accessibles malgré
les flèches ; le focus rejoint les résultats après filtrage/navigation.

Preuves locales :

- **84 tests Vitest réussis**, sortie 0, aucun skip, dont les 15 tests de
  l'historique, le contrat embarqué et les formateurs :
  `npm test -- src/features/employees/ValidationHistory.test.jsx src/lib/api/contracts.test.js src/lib/formatters.test.js`.
  Reset/curseurs, filtres saisis/appliqués, statuts, droits scanner, erreurs/reprise,
  session remplacée et réponses incompatibles sont vérifiés.
- **9 scénarios Chromium réussis**, sortie 0, aucun skip :
  `npm run test:e2e -- tests/e2e/validation-history.spec.js --workers=1 --output=tmp/pro-validation-history-verified`.
  Responsable/salarié à 320/1280 pixels, parcours de filtres/détails/reset à
  390/1280 pixels, état vide et dates depuis New York/Los Angeles (minuit Paris
  et journées de 23/25 heures). Toutes les lectures sont simulées et bornées,
  aucune validation ni mutation réelle n'est exécutée.
- Axe ne relève aucune violation sur la région historique testée à 390/1280 pixels.
  Captures des deux formats inspectées ; marges, référence longue et absence
  de débordement contrôlées. Les libellés sans espace peuvent revenir à la ligne.
  Ce contrôle ne remplace pas une recette sur téléphone physique ou lecteur d'écran.

Le premier passage navigateur après refonte révèle quatre échecs de sélection
du filtre Type : son label englobait les options du select. Le label est séparé
et explicitement associé à son champ ; les assertions existantes sont conservées.
Le rejeu complet réussit, puis est renouvelé après l'ajustement des marges.
Après ajustement de la largeur du bouton Actualiser, les deux scénarios de
présentation 390/1280 pixels sont à nouveau exécutés avec succès (sortie 0),
avec captures et Axe : même commande avec
`--grep 'validations exploitables' --output=tmp/pro-validation-history-layout`.
La revue indépendante ne relève pas de régression des curseurs, droits ou statuts ;
ses demandes de preuve sur les périodes rapides et les libellés longs sont traitées.
Le build navigateur est isolé, sans `.env` opérateur ni appel à une cible métier.
L'avertissement de découpage du module importé à la fois statiquement et
dynamiquement reste signalé, sans empêcher le build ni les tests.

Impacts : **Pro et documentation** (spécification E72 et guide commerçant).
Aucun changement backend, DTO/contrat embarqué, règle métier, migration,
configuration, donnée ou générateur. Aucun test PostgreSQL n'est nécessaire à
ce changement de présentation ; les tests backend des correctifs E70 précédents
ne sont pas annoncés comme rejoués. Les accès ne gagnent aucun droit financier,
client nominatif, export ou commande de validation.

La correction reste locale, sans recette hébergée, commit, push ou déploiement.
Les contrôles `check_guidance.py` (94 guides, 1 050 liens),
`check_guidance.py --changed --all-markdown` (12 documents, 196 liens),
`sync_documentation.py --check-sources` (130 documents) et `git diff --check`
réussissent. Aucun fichier de configuration public ou guide PDF généré n'est modifié.


## Évolution des états du scan Coffret — 9 octobre 2026

**PRO-SCAN-20261009-ETATS**, base Pro `66be333` et changements locaux.
Le [parcours commun](../validation-prestations/scan-commercant.md#lisibilité-du-résultat-coffret--9-octobre-2026)
précise E72-CA-07/09/11/18 : disponibilité verte, absence de prestation rouge,
prestation déjà validée et confirmation serveur bleues, attente et résultat
incertain explicités. Les deux profils utilisent une présentation commune,
avec texte et icône. Les états non reconnus ne proposent pas de validation.

La source active du responsable est `src/ActionWorkspaces.jsx` ; le composant
homonyme sous `src/features/validation/` n’est pas son point d’entrée. Le salarié
conserve `EmployeeScanner` et sa projection limitée. Le reçu du responsable
conserve l’attente de rafraîchissement et le contrôle du résultat serveur.
Le scan ne valide jamais implicitement et les données financières ou fonctions
du responsable ne sont pas exposées au salarié.

Impacts : Pro et documentation uniquement. Ni contrat backend, configuration,
migration, données de démonstration ni droits ajoutés. Tests navigateur avec
réponses simulées ; aucune validation métier ou invitation réelle envoyée.
Aucun commit, push ou déploiement pour ce lot.

Preuves unitaires : **48 tests réussis**, dont le parcours à plusieurs prestations,
la désactivation des commandes pendant l’envoi et la relecture d’un résultat
incertain confirmant la prise en compte sans renvoyer la commande. La revue
indépendante ne relève pas de nouveau droit ni de succès prématuré ; le message
contradictoire « à valider » pour un état indisponible a été retiré.

Preuves navigateur : **37 scénarios réussis, sortie 0**, dont 16 cas couvrant
les deux profils à 320/390 pixels et les états disponible, déjà validé, absent
et expiré, avec vérification des couleurs, de la visibilité de l’action et de
l’absence de débordement. Les scénarios existants couvrent également le reçu,
la reprise et le scan salarié. Un premier lancement avait terminé les scénarios
mais bloqué à l’arrêt du serveur ; le résultat retenu provient de la relance
avec serveur indépendant, terminée normalement.

Après harmonisation finale des styles de cartes et badges, les 16 scénarios
responsive sont réexécutés avec succès ; build production réussi. Les captures
finales sont dans `localeo-commercant/tmp/coffret-states-final/` (non versionné).
Inspection visuelle à 320/390 pixels : actions lisibles, états cohérents entre
résumé et prestation. Vérifications documentaires et `git diff --check` réussis.
La recette sur téléphone physique et la vérification d’un déploiement restent
non exécutées ; les scénarios locaux utilisent Chromium et des réponses simulées.

## Revue de clôture — 1er novembre 2026

**Verdict : clôture bloquée ; E72 reste En cours, avec ses 22 critères et son
backlog au même emplacement.** Les réserves ne sont pas levées par les bilans
locaux antérieurs. En particulier, le refus générique perd des attributs d’audit
exigés par CA-15. Plusieurs variantes intégrées restent à prouver. La pagination
après chargement complet est une dette technique préexistante, sans nouveau
critère de clôture ajouté par cette revue. La recette pilote
demandée dans le backlog et le bilan de mise en service n’est pas attestée.
La présente revue ne réduit aucun critère pour permettre une clôture.

### Révisions et périmètre de la revue

Bases Git examinées : documentation `f0b735e`, backend/ERP `4f0cfdc`,
Localeo Pro `23c754a`, Marketplace `6c1aaac`, Animation `04dc06c`.
Les modifications locales de cette revue concernent la documentation, trois
fichiers Pro et la fixture PostgreSQL Animation E72. Marketplace et Animation
restent inchangés. Python 3.14.3, PostgreSQL 18 jetable et Chromium local ;
aucune base métier, invitation réelle ou configuration distante utilisée.
Les comptes et secrets des tests sont synthétiques.

Deux revues indépendantes du backend/contrats/exploitation et une revue Pro/ERP
rapprochent les exigences des producteurs et consommateurs. Elles distinguent
les défauts de code des assertions absentes. Une absence de preuve ci-dessous
ne signifie pas qu’un contournement a été reproduit.

### Preuves de cette revue

Les identifiants suivants sont locaux à ce bilan ; les commandes partent du
dépôt indiqué. Les sorties temporaires ne sont pas des livrables versionnés.

| Référence | Commande ou contrôle | Résultat et portée |
| --- | --- | --- |
| P1 — backend isolé | `python scripts/validation/test_isolated.py tests/domain/identite_acces/test_acces_salaries_dedicated.py tests/domain/identite_acces/test_conservation_salaries.py tests/application/identite_acces/test_option_salaries_indisponible.py tests/api/test_salaries_e72.py tests/api/test_historique_salarie_e72.py tests/infrastructure/test_segments_audit_salaries.py tests/unit/test_salaries_email_configuration.py tests/unit/test_demonstration_salaries.py -q --tb=short --basetemp=.artifacts/pytest-e72-closure-isolated` | **44 réussites**, aucun skip. Domaine, option ERP, projections minimales, email et démonstration unitaire. |
| P2 — PostgreSQL jetable | `python scripts/validation/test_isolated.py tests/security/test_iam_salaries_e72.py tests/security/test_animation_salaries_e72.py tests/security/test_conservation_salaries_postgres.py tests/security/test_migration_salaries_bootstrap_e72.py -q --tb=short --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:16462/localeo_audit_test --basetemp=.artifacts/pytest-e72-closure-postgres` | Premier passage : **24 réussites, 1 échec**, aucun skip. Fixture historique Animation non alignée sur la v280. Après correction : **25 réussites**, aucun skip, en 148,77 s ; 36 avertissements SQLAlchemy/dates conservés. |
| P3 — Pro unitaire | `npm test -- src/features/employees src/app/useMerchantSession.test.jsx src/app/merchantNavigation.test.js src/features/session/api.test.js src/features/session/passwordResetReturn.test.js src/lib/api/contracts.test.js` | Premier passage : 95 réussites et 2 échecs de test historique Lot. Après correction du montage et du nettoyage : **98 réussites dans 10 fichiers**, aucun skip. Les 8 tests du hook repassent après renforcement final de l’assertion de conservation pendant une session valide. |
| P4 — Pro navigateur | `npm run test:e2e -- tests/e2e/employees.spec.js tests/e2e/validation-history.spec.js --workers=1 --output=tmp/e72-closure-pro` | **16 réussites**, aucun skip, avant correction du nettoyage local : 7 salariés et 9 historique. API et caméra simulées ; formats 320/390/1280 px selon scénario. |
| P5 — Pro après nettoyage | `npm run test:e2e -- tests/e2e/employees.spec.js --workers=1 --output=tmp/e72-closure-pro-after-cleanup` | **7 réussites**, aucun skip ; renouvellement des scénarios salariés affectés, sans les additionner comme de nouveaux scénarios à P4. |
| P6 — ERP navigateur | `node tests/browser/acces-commercant-erp.cjs` dans le backend | Réussi à **390/1280 px** : commandes, confirmation, conflit, verrouillage et refus de rôle. Échanges simulés ; pas d’activation réelle. |
| R1 — preuve réutilisée | `tests/security/test_validations_salaries_e72.py`, 10 scénarios PostgreSQL dans la vérification E70 du 1er novembre, antérieure à cette revue | Attribution Coffret, effet unique, reçu gagné par PIN, deux ordres révocation/validation, droits courants, refus de gestion PIN, périmètre historique et archives. Fichier et code correspondant inchangés sur la base backend examinée ; **non réexécutés** ici. |
| R2 — architecture réutilisée | 623 contrôles d’architecture réussis dans la vérification E70 du 1er novembre | Sources applicatives Python inchangées depuis ce contrôle ; seule une fixture est ajustée ici. **Non réexécutés** pour cette revue. |
| R3 — démonstration/migration historiques | Sections « Démonstration — résultat final » et « Migration de la base de test » ci-dessus | Le générateur complet avait donné 6 réussites/1 échec, puis le scénario corrigé 1 réussite ; pas de second runner complet revendiqué. Migration TEST du 8 octobre attestée ; aucune migration distante réexécutée aujourd’hui. P1/P2 renouvellent seulement leurs sous-ensembles ciblés. |

Les avertissements de compilation navigateur sur un module importé à la fois
statiquement et dynamiquement restent visibles. Ils ne sont pas des skips.
La caméra et les échanges réseau simulés ne prouvent pas un usage sur téléphone
physique, un lecteur d’écran ou la disponibilité d’un service hébergé.

### Matrice des 22 critères réexaminés

Les sources fonctionnelles restent le [backlog](../../roadmap/terminees/epic-72-acces-salaries-validation-localeo-pro-backlog.md),
le [parcours](README.md), les [contrats](architecture-contrats.md) et le
[guide salarié/ERP/ops](guide-utilisation-exploitation.md). La colonne documentaire
désigne la section du guide qui porte le comportement attendu ; elle ne constitue
pas une preuve d’exécution.

| Critère | Propriétaire et comportement examiné | Preuve exécutée ou réutilisée | Documentation / exploitation | Verdict et action restante |
| --- | --- | --- | --- | --- |
| E72-CA-01 | `GestionSalaries.inviter`, commerce et acteur dérivés du principal ; schéma strict d’invitation | P1 email contextualisé ; P2 invitation idempotente/collision | Responsable ; ERP | **Partiel** : prouver par les routes l’injection commerce/rôle et un principal d’un autre commerce. |
| E72-CA-02 | Acceptation atomique du lien, hash du mot de passe, session individuelle | P2 résolution/acceptation puis connexion et mauvais mot de passe ; P4 lien fragment nettoyé | Salarié | **Partiel** : assertion explicite de refus de connexion avant acceptation manquante. |
| E72-CA-03 | `verifier_lien_salarie` et verrouillage de l’acceptation | P1 borne d’expiration ; P2 une seule acceptation concurrente et refus du rejeu | Responsable ; Salarié | **Partiel** : cas intégrés de l’invitation 24 h avant/à/après échéance et après annulation à compléter. |
| E72-CA-04 | `agir` / `_emettre`, annulation des anciens liens et charge de remise chiffrée | P2 worker, concurrence, configuration invalide et envoi incertain | Responsable ; Préparer une ouverture | **Partiel** : renvoi réussi puis ancien lien refusé, annulation puis refus acceptation/remise, répétition de clé de renvoi. |
| E72-CA-05 | Registre de login Pro normalisé et contrainte globale | P2 collision, idempotence, changement de login principal, rollback et suppression | Responsable | **Partiel** : compléter collisions concurrentes entre types et responsable d’un autre commerce. |
| E72-CA-06 | Capacités fermées côté serveur et navigation Pro réduite au scanner/historique | P1 opération inconnue/finance refusées ; P3/P4/P5 navigation, URLs interdites et scanner initial | Salarié | **Vérifié localement** pour le parcours et les capacités prévus. |
| E72-CA-07 | Cœur Coffret existant, identité salariée et session courante | R1 attribution, reçu, transaction et validation uniques ; P3/P4 confirmation explicite/reprise | Salarié | **Vérifié localement**, avec R1 réutilisée explicitement. |
| E72-CA-08 | `ServiceValidationsAnimation`, auteur et règles du moteur commun | P2 attribution, reçu, option retirée, salarié révoqué, concurrence principal/salarié | Salarié | **Partiel** : compléter toute la matrice calendrier/participation/éligibilité et confirmation Animation dans Pro, notamment résultat ANOMALIE et reprise. Le scénario navigateur actuel résout le QR sans confirmer. |
| E72-CA-09 | Vérificateur de session et capacités serveur, périmètre du commerce | P1 refus fermés ; P2/P3/P4 et R1 isolation ciblée | Salarié ; ERP | **Partiel** : matrice HTTP exhaustive des routes interdites et identifiants d’un autre commerce, sans effet métier. Aucun contournement constaté dans les cas testés. |
| E72-CA-10 | Contrôles du cœur Coffret/Animation et droits revérifiés avant effet | P2 salarié révoqué sans progression ; R1 droits retirés avant confirmation/reçu | Salarié | **Partiel** : relier ou compléter QR invalide/expiré/consommé et commerce suspendu pour les deux parcours salariés. |
| E72-CA-11 | Idempotence et verrous métier communs | P2 concurrence principal/salarié Animation, effet unique ; R1 reçu gagné par PIN ; P4 timeout/relecture Coffret | Salarié | **Partiel** : deux salariés concurrents Coffret et course réelle salarié/PIN à prouver ; une relecture après PIN ne prouve pas cette course. |
| E72-CA-12 | Verrous session/compte et révocation avant confirmation | R1 deux ordres concurrents Coffret ; P2 révocation Animation avant effet | Responsable ; Salarié | **Partiel** : ordre concurrent démontré sur Coffret, pas la course Animation complète. Validations antérieures préservées dans les cas contrôlés. |
| E72-CA-13 | Opérations salariées fermées et gestion réservée au principal | R1 refus directs état/création/révocation PIN ; P3/P4 navigation interdite | Responsable ; Salarié | **Partiel** : compléter par API les commandes invitation/rôle/configuration et lecture PIN dans la matrice CA-09. |
| E72-CA-14 | Projection historique minimale, tenant serveur, bornes et archives | P1 DTO exact/no-store ; P2 limite d’usage courant Animation ; R1 autre commerce/archives ; P3/P4 curseurs, filtres et présentation | Salarié ; contrats ancien historique et flux | **Vérifié localement** sur les cas reliés. Aucun export, montant, client nominatif ou secret ajouté. |
| E72-CA-15 | Audit des opérations nominales et refus | P1 segments/conservation ; P2 succès nominaux ; inspection de `handle_acces_salarie` dans `app/main.py` | ERP ; Conservation et reprise | **Non satisfait** : le refus générique écrit `acteur="requete"`, sans commerce ni cible, même pour certains refus contextualisables. Corriger la capture du contexte vérifié et prouver sa persistance après rollback, sans secret. |
| E72-CA-16 | Reset salarié, génération de sécurité et purge locale à fermeture de session | P1 borne 1 h ; P2 reset sous option suspendue sans réactivation ; P3/P5 nettoyage local corrigé | Salarié | **Partiel** : reset actif avec session ouverte, expiration/rejeu intégrés, isolation entre deux salariés et formulaire public demande/reset Pro manquent. La purge du contexte Lot est corrigée, pas ces autres variantes. |
| E72-CA-17 | Migrations 258/259, registre et sessions du principal | P2 migration/bootstrap/collision, session principale conservée ; R3 test historique | Préparer une ouverture | **Partiel** : relier une preuve complète récupération principal E68 après migration ; ne pas déduire cette couverture du seul login/refresh. |
| E72-CA-18 | Scanner mobile, caméra refusée, réseau interrompu et reçu | P3/P4/P5 caméra simulée, 320/390/1280 px, absence de succès implicite et de reprise hors ligne | Salarié | **Partiel** pour l’acceptation finale : preuves locales disponibles ; recette pilote explicitement demandée dans le backlog non attestée. Aucun appareil physique ou lecteur d’écran annoncé comme testé. |
| E72-CA-19 | Option ERP par défaut inactive, commandes réservées Admin/Backoffice | P1 schéma strict/CSRF/refus ; P6 Admin et rôle refusé ; P2 défaut inactif | ERP ; Activation ERP indisponible | **Partiel** : compléter la matrice API Admin/Backoffice/Lecteur/Finance et rôles combinés ; CA-15 empêche aussi l’acceptation de l’audit des refus. |
| E72-CA-20 | Absence de quota métier | P2 six invitations sans plafond puis acceptation concurrente d’une autre ; R3 six actifs générés | Responsable | **Partiel** : le test IAM ne prouve pas cinq actifs puis activation effective du sixième et connexions distinctes. La génération de six lignes actives ne remplace pas ce parcours API. Dette de lecture bornée distinguée ci-dessous. |
| E72-CA-21 | Désactivation sous verrous, epoch et annulation des liens, principal préservé | P2 anciennes sessions refusées ; R1 confirmation après retrait refusée | ERP | **Partiel** : annulation des invitations en attente/préservation du principal et courses désactivation avec invitation, acceptation et validation à compléter. |
| E72-CA-22 | Réactivation sans résurrection d’une ancienne session ou d’un révoqué | P1 compte révoqué toujours refusé ; P2 ancienne session refusée après réactivation | ERP | **Partiel** : cycle complet nouvelle connexion active, révoqué refusé, ancien lien annulé refusé et nouvelle invitation utilisable. |

### Anomalies et corrections de cette revue

- **E72-CLOT-20261101-AUDIT** — réserve CA-15/19 : l’orchestration nominale
  renseigne acteur/commerce/cible ; le handler générique `AccesSalarieRefuse`
  ne les reprend pas. La correction devra préserver un contexte vérifié y
  compris lorsque la vérification refuse l’accès, sans faire confiance aux
  identifiants fournis librement. Ajouter une preuve persistée de refus après
  rollback, avec corrélation et absence de jeton/mot de passe/QR. **Non corrigé** :
  correction d’audit transverse à traiter avant clôture, sans réécrire CA-15.
- **E72-CLOT-20261101-LISTE** — dette technique préexistante au regard de la
  [convention performance](../../architecture/transverse/performance-volumetrie.md) :
  `GestionSalaries.lister` appelle `RepositorySalaries.comptes().all()` puis
  découpe la liste en Python. Pour chaque compte affiché, toutes les invitations
  sont également chargées. La page HTTP bornée ne prouve donc pas une lecture
  SQL bornée ; l’absence de quota accroît ce risque. Ce chemin n’est pas modifié
  par cette revue ; la convention du 18 octobre vise les nouvelles évolutions
  et les chemins qu’elles modifient. Cette dette ne constitue donc pas, à elle
  seule, un blocage supplémentaire de clôture. **Non corrigé** : lors d’une
  prochaine évolution de ce chemin, déplacer
  pagination et décompte en base, récupérer les dernières invitations en lot,
  puis prouver la borne de lectures/requêtes sur un volume représentatif.
  Aucun ralentissement distant ni incident de production n’est inventé.
- **E72-CLOT-20261101-SESSION** — partie technique de CA-16 **corrigée localement** :
  `clearStoredMerchantSession` retire désormais aussi
  `localeo-bon-lot-recovery`. Ce stockage ne contenait ni Bearer ni secret QR,
  et son propriétaire était déjà contrôlé ; il restait néanmoins présent après
  déconnexion/expiration. Reproduction ciblée avant correction : 5 échecs et
  3 réussites du hook ; après correction : 8 réussites. Les tests conservent
  les préférences et stockages étrangers et la reprise pendant une session valide.
- **Fixtures de preuve corrigées** : le test `BonLotHistory` monte le routeur
  requis par la page actuelle et vérifie séparément type, mode et statut de chaque
  ligne, sans confondre une remise annulée avec un lot remis. La fixture
  `salarie_animation` installe la section Animation de la vraie v280 avec
  `installer_projection`, comme les tests du flux E73. Ni assertion métier,
  résultat attendu, skip ou migration de production modifié.

### Contrats, documentation et publication locale

Les 13 chemins E72 et les schémas transitifs des contrats documentaires E41
et embarqués Pro sont comparés statiquement : pas de divergence sémantique
relevée. La différence de nom de référence `PageValidations` est liée à la
collision de noms des schémas générés. P3 exécute les assertions du consommateur ;
aucune régénération des contrats n’est nécessaire à cette revue.

Le contrat courant du flux `/validations-flux` est ajouté à la documentation
d’architecture en conservant l’ancien `/validations`, encore servi. Les
paragraphes de conservation reflètent les traitements effectivement présents.
Le guide backoffice et sa référence ops relient la notice E72, désormais exportée
sous **`docs/ops/formation/acces-salaries.md`**. Cela corrige sa disponibilité
dans un bundle sans créer une notice concurrente.

Bundle local préparé avec
`python scripts/sync_documentation.py --output ../localeo-backend/tmp/e72-cloture-20261101-docs` :
**132 exports**. Le contrôle backend
`python scripts/documentation/check_documentation_snapshot.py --manifest tmp/e72-cloture-20261101-docs/documentation.snapshot.json --source ../localeo-projet`
vérifie **133 entrées distribuées**, manifeste compris, et leurs sources.
Un appel au lecteur réel `resolve_ops_document('formation/acces-salaries.md')`
confirme l’alias, le contenu et le lien relatif depuis le guide backoffice.
Ce bundle ignoré par Git n’est ni sélectionné sur un serveur ni publié dans l’ERP.

### Configuration et mise en service à préparer

Aucune variable, permission, migration, règle métier ou donnée de démonstration
n’est modifiée par le nettoyage Pro et la correction de fixture. Les exigences
existantes suivantes restent nécessaires à la livraison ; leurs valeurs distantes
et leur ordonnancement ne sont pas vérifiés pendant cette revue.

| Composant / cible | Action | Valeur attendue ou défaut | Source / contrôle |
| --- | --- | --- | --- |
| Backend / cible autorisée | Vérifier l’historique du runner avant migration | v258 puis v259 après E70 ; migrations ultérieures requises par la version déployée, dont v280 pour le flux courant | `sql/v258_acces_salaries.sql`, `sql/v259_conservation_salaries.sql`, `sql/v280_historique_validations_cibles.sql` ; aucune collision de login ni migration requise manquante. La migration TEST du 8 octobre reste une preuve historique. |
| API et worker email | Configurer l’ouverture technique | `LOCALEO_PRO_ACCESS_SALARIES_ENABLED=false` par défaut ; passage à `true` seulement pour l’ouverture décidée | `app/config.py` ; le flag ne crée ni n’active aucun commerce. |
| API et worker email | Provisionner le même trousseau privé et la clé active hors Git | `LOCALEO_PRO_ACCESS_SALARIES_INVITATION_ENCRYPTION_KEYS_JSON` et `LOCALEO_PRO_ACCESS_SALARIES_INVITATION_ENCRYPTION_ACTIVE_KEY` ; aucun secret dans ce bilan | Conserver les anciennes clés nécessaires aux charges en attente ; vérifier composition/remise et effacement de la charge sans exposer le lien. |
| API / Pro | Vérifier l’origine HTTPS des liens et les routes directes | `LOCALEO_FRONT_COMMERCANT_PASSWORD_INIT_URL_TEMPLATE`, origine Pro de la cible ; test attendu selon le guide : `https://test-commercant.localeo.city` | Invitation et récupération salariées en fragment ; routes directes et rechargement, connexion puis scanner. Aucun en-tête de compatibilité à réintroduire. |
| Traitement email | Vérifier le worker salarié composé par le batch existant | Configuration fournisseur existante, fréquence et supervision cible à attester | État de remise lisible ; pas de rejeu automatique d’une remise fournisseur incertaine. |
| Conservation / audit | Configurer cible explicite, stockage partagé et ordonnancement surveillé | `LOCALEO_CONSERVATION_DATABASE_URL`, `LOCALEO_AUDIT_EXTERNAL_JSONL_PATH` ; valeurs privées non publiées, fréquence cible à renseigner | `scripts/database/conserver_acces_salaries.py --limit 100` simule par défaut ; `--apply` sur cible autorisée seulement ; rapport et segments persistants. |
| Documentation / ERP | Publier un bundle depuis le futur commit documentaire et sélectionner cette révision | Alias `formation/acces-salaries.md` et empreintes cohérentes | Régénérer le bundle après commit ; contrôle snapshot puis ouverture de la notice dans l’ERP déployé. Le bundle local ne remplace pas cette étape. |
| ERP / commerce pilote | Activer explicitement l’option avec un rôle autorisé après résolution des réserves d’acceptation | Inactive par défaut ; Admin ou Backoffice | Recette invitation, connexion salariée, scan Coffret/Animation, reçu après interruption, historique, reset, révocation, désactivation/réactivation, et principal inchangé. |

Ordre : résoudre les réserves d’acceptation et renouveler leurs preuves, préparer le backend
et les migrations de la version retenue, publier/sélectionner le bundle
documentaire, livrer backend/worker puis Pro, vérifier la santé et les liens,
puis effectuer l’activation explicite et la recette pilote autorisée.
En reprise, désactiver l’option et les sessions avant de retirer un backend
connaissant ces identités ; préserver les tables, preuves et attributions.
Après restauration, réappliquer les retraits dus avant retour au trafic.
Aucun rollback destructif ou restauration non éprouvée n’est promis.

### Lots de commit préparés, sans indexation ni publication

| Dépôt | Fichiers de la revue | Message proposé |
| --- | --- | --- |
| `localeo-commercant` | `src/app/useMerchantSession.js`, son test et `src/features/employees/BonLotHistory.test.jsx` ; preuves P3/P5 | `fix(pro): nettoyer les reprises privees a la fermeture de session` |
| `localeo-backend` | `tests/security/test_animation_salaries_e72.py` ; fixture seule, preuve P2 | `test(e72): aligner la fixture historique Animation sur le flux courant` |
| `localeo-projet` | Index roadmap, backlog et trois documents de spécification E72, deux guides backoffice, `documentation.exports.json` ; contrôles documentaires et lecteur | `docs(e72): consigner la revue de cloture et publier la notice salaries` |

Les trois lots sont un **bilan/correctif**, pas une clôture. Aucun déplacement
de backlog, changement de compteur d’état, commit, push ou déploiement réalisé.
Les critères métier et contrats applicatifs restent inchangés. Les sorties de
travail et le bundle demeurent hors des commits.

Contrôles documentaires de cette revue : `python scripts/check_guidance.py`
réussi (94 guides, 1 054 liens), `python scripts/check_guidance.py --changed --all-markdown`
réussi (7 documents, 102 liens), `python scripts/sync_documentation.py --check-sources`
réussi (132 exports), et `git diff --check` réussi dans les trois dépôts modifiés.
Les preuves P1/P2/P3/P4/P5/P6 sont locales et n’attestent pas la recette pilote.
