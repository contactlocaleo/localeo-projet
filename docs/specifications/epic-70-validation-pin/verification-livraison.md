# E70 — Preuves attendues et préparation de livraison

Références : [architecture](architecture-contrats.md), [périmètre V1](README.md),
[34 critères canoniques](../../roadmap/en-cours/epic-70-validation-prestation-telephone-client-backlog.md).
Ce document conserve le plan de vérification initial et le bilan d'implémentation
locale du 7 octobre ci-dessous. Aucune recette sur un environnement réel ni
activation du canal n'a été effectuée.

## 1. Matrice de couverture

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
| E70-CA-18 | Durée serveur | 1/7/30 jours, 0/31/fraction refusés ; timezone/DST ; borne fin exclusive | Date/heure fin | Horloge fixe | Pas de dépendance au batch d'expiration |
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
