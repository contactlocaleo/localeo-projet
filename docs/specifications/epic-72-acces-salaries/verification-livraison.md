# E72 — Vérification et livraison

Ce document conserve la matrice de conception du 5 octobre et le bilan local des 7–8 octobre ci-dessous. Aucun déploiement ni envoi email réel n’a été effectué. Références : [parcours](README.md), [architecture et contrats](architecture-contrats.md), [backlog](../../roadmap/en-cours/epic-72-acces-salaries-validation-localeo-pro-backlog.md).

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
