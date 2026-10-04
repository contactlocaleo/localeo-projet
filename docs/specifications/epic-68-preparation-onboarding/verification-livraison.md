# E68 — Vérification et préparation de livraison

V1.2 du 3 octobre 2026. État : **En cours** dans le
[backlog](../../roadmap/en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md).
L'implémentation et ses vérifications locales sont décrites ci-dessous. Aucun
déploiement ni envoi réel n'est réalisé par cette livraison locale.

La recette suit exclusivement les sept étapes V1.2 du [parcours](README.md).
Les 31 critères restent exigibles, avec même compte commerçant, absence de dépôt
marchand, signature le jour J, copie signée déposée par Localeo après rendez-vous
et confirmation explicite avant chaque séquence de communication.
Les étapes servent de référence métier et de recette ; la vue courante regroupe
activation, confirmation des communications et suivi du dossier. Elles ne remplacent
pas les statuts métier ni les contrôles de finalisation.

## Correction ergonomique OnBoard du 3 octobre 2026

Constat utilisateur : la préparation du rendez-vous expose trop de saisies et le
bilan pilote alourdit le parcours quotidien. Le comportement attendu est une vue
centrée sur l'activation existante, la vérification et confirmation du mail de
préparation (avec SMS annoncé si prévu), puis le suivi du dossier. Les formulaires
de questions, prestations, actions, rendez-vous et fin de réunion restent accessibles
dans des détails à déplier. Un blocage reste visible sans ouvrir ces détails.
Activer un commerçant ne finalise pas son dossier et n'autorise aucun envoi implicite.

La revue porte aussi sur l'accueil et la création : recherche, statut et suivi
immédiatement accessibles, filtres avancés repliés, libellés explicites pour créer
ou retrouver un commerçant et planification différée dans le dossier. Vérifier
le traitement d'un dossier sur mobile et au clavier, sans champ désactivé de
rendez-vous à la création ni clé de configuration affichée à l'utilisateur.
Vérifier aussi l'ouverture sur « À faire et suivi », la navigation clavier entre
rubriques et le maintien de l'onglet après enregistrement dans le même dossier.
Les boutons « Vérifier le dossier », « Valider le dossier » et « Terminer le dossier »
doivent conserver les permissions et conditions des actions correspondantes.

La section « Bilan du pilote OnBoard » est supprimée du rendu ; les API de mesure
et l'historique sont conservés. Les permissions, confirmations par séquence et
contrôles de version/concurrence ne changent pas. Les sept étapes métier restent
la référence de contrôle, sans imposer sept formulaires principaux.

Impacts : rendu ERP/backend et guide canonique exporté. Pas de migration ni de
réparation de données, puisque la persistance ne change pas ; pas de changement
des contrats/API, du générateur ou des applications satellites. Le guide exporté
devra être inclus dans le bundle documentaire de la prochaine livraison.

Preuves locales exécutées le 3 octobre 2026 sur le backend `651df1b` avec les
modifications de cette correction :

- `node --test tests/frontend/test_onboard_progress.mjs tests/frontend/test_onboard_pagination.mjs tests/frontend/test_preparation_timezone.mjs` : **12 tests réussis**, aucun ignoré.
- `node tests/frontend/test_preparation_browser.mjs` : **5 scénarios réussis**,
  dont reprise explicite, lecture seule, réponses tardives et changement Teams/physique.
- `node tests/frontend/test_communications_simple_browser.mjs` : **6 scénarios réussis**,
  dont aperçu/annulation sans envoi, double clic, aperçu bloqué, réponse tardive
  et absence de relance automatique après résultat incertain.
- `node tests/frontend/test_onboard_simple_browser.mjs` : **2 scénarios complets réussis**,
  à 390 et 1280 pixels, sur le HTML et les scripts réels avec API simulée : filtres,
  création, onglets au clavier, maintien de la rubrique et changement de dossier.
- Captures navigateur examinées sur mobile et ordinateur ; aucun débordement
  horizontal dans les scénarios. Une revue indépendante a identifié un champ URL
  Teams masqué qui bloquait un rendez-vous physique : correction et test de régression
  exécutés avec succès.
- Contrôles documentaires : `python scripts/check_guidance.py --document docs/produit/formation/backend/guide-preparation-onboarding-commercant.md`
  et `python scripts/sync_documentation.py --check-sources` ; sources et liens valides.

Les fournisseurs sont simulés : aucun email/SMS réel ni aucune modification de base.
Les tests Python métier/API n'ont pas été relancés pour cette correction de rendu,
sans modification de leurs règles ou contrats. Aucun déploiement de cette correction
n'a été effectué ; les résultats historiques ci-dessous ne prouvent pas sa livraison.

## Correction du lien Teams facultatif — 3 octobre 2026

Sur la base backend `2cfcb10` avec cette correction locale, un rendez-vous Teams
peut être créé sans lien (champ absent, nul ou vide), puis complété ultérieurement.
`PreparationOnboarding` porte la règle commune aux commandes API/OnBoard ; une URL
fournie reste soumise au contrôle HTTPS et l'adresse physique reste obligatoire.
Le formulaire mentionne « facultatif ». Sans lien, le mail et l'ICS indiquent
qu'il reste à communiquer. Toute modification conserve le versionnement et les
confirmations des communications ; aucun envoi implicite.

Reproduction avant correction : quatre cas de domaine refusés avec `ENTREE_INVALIDE`
et formulaire navigateur invalide sans lien. Après correction :

- `test_preparation_onboarding.py`, `test_service_preparation_onboarding.py`,
  `test_communications_preparation.py`, `test_preparation_onboarding_api.py` et
  `test_preparation_supports.py`, via `scripts/validation/test_isolated.py` :
  **100 tests réussis**, dont ajout ultérieur du lien, aperçu/ICS sans lien et absence d'envoi.
- `node tests/frontend/test_preparation_browser.mjs` : **5 scénarios réussis**,
  dont création sans lien sur mobile et ordinateur.
- `tests/architecture`, `tests/domain/test_domain_dedicated_classes.py` et
  `tests/application/use_cases/test_use_case_business_test_coverage.py`, via le
  même lanceur isolé : **453 tests réussis**.

Impact : backend/OnBoard, rendu des communications et documentation canonique.
Pas de migration ni de configuration supplémentaire : le champ est déjà stocké
dans l'état JSON. Contrat assoupli sans nouvelle route ; les jeux de démonstration
avec lien restent valides et aucun changement du générateur n'est nécessaire.
Applications satellites inchangées : le champ reste disponible avec la même forme.
Aucun déploiement ni envoi réel effectué pour cette correction.

## Mail de préparation et première connexion intégrée — 3 octobre 2026

Demande utilisateur : clarifier le mail et intégrer la création du mot de passe
au parcours de préparation, sans invitation opérateur distincte. Le pack présente
trois étapes : créer son mot de passe, préparer le rendez-vous et connaître son
déroulement. Le bouton principal sans secret ouvre la demande de lien personnel ;
le lien secondaire ouvre directement la préparation des comptes déjà configurés.
Le mail personnel affiche « Créer mon mot de passe » avant les autres informations.

La confirmation explicite du PACK prépare l'identifiant manquant dans la même
transaction, sans mot de passe ni email d'invitation. Le POST marchand existant de
demande de lien produit INITIALISATION pour un premier accès avec retour
`/preparation`, sinon le parcours de récupération existant. Réponse générique,
limites de fréquence, jetons personnels et retour local autorisé sont conservés.
L'ouverture du mail ou du lien ne crée aucun accès et n'envoie rien.

Déploiement requis : backend et application Commerçant ensemble, avec le bundle
documentaire actualisé. Pas de nouvelle variable ni migration ; les modèles de
liens et durées d'identité existants sont réutilisés. La file d'envoi email doit
fonctionner pour remettre le lien demandé par le commerçant. Les intentions
préparées avec l'ancien texte doivent être revues puis confirmées avec le nouveau
contenu. Les emails déjà remis ne changent pas ; un ancien dossier sans compte
peut utiliser l'invitation explicite existante ou une nouvelle confirmation du pack.

La revue indépendante a contrôlé le périmètre de confirmation, l'absence de secret
dans l'aperçu, la non-réaffectation de compte et les refus significatifs. La
consommation concurrente et la révocation des tokens d'initialisation frères
restent une limite préexistante du parcours d'identité, hors de cette correction.
La concurrence PostgreSQL réelle n'est pas attestée par les tests SQLite.

Preuves locales (backend `2cfcb10`, commerçant `74a797a`, avec modifications) :

- Architecture, recensements et rendu email : **491 tests Python réussis**
  (`tests/architecture`, recensements domaine/use cases, `test_preparation_email_copy.py`
  et `test_service_preparation_email.py`, via le lanceur isolé).
- Accès et communications : **89 tests ciblés réussis**, couvrant provisionnement
  à la confirmation seulement, mot de passe existant conservé, compte verrouillé,
  conflit de login, rollback et collision injectée, HTTP générique, demande et
  première création effective du mot de passe. Les **5 tests PostgreSQL** adaptés
  n'ont pas été exécutés faute d'URL de base jetable ; ils ne sont pas comptés
  comme réussis. Les deux écarts de revue (compte verrouillé et collision SQL)
  sont corrigés et la relecture indépendante le confirme.
- Commerçant : **37 tests Vitest réussis** (accès préparation, routes mot de passe,
  retour de récupération, préparation et disponibilité de session) ; **4 parcours
  Playwright réussis** avec création, retour après connexion, récupération et
  première connexion mobile/ordinateur ; `build:test` réussi.
- Le serveur de test géré par Playwright se bloquait à la fermeture sous Windows :
  les mêmes quatre scénarios ont été relancés dans le mode documenté
  `LOCALEO_E2E_EXTERNAL_SERVER=1`, avec sortie zéro puis arrêt du serveur local.
- Aperçus HTML synthétiques examinés à 390 et 1000 pixels, sans débordement ;
  bouton visible avant les pièces et les prestations, sans secret dans le pack.
- Documentation : 90 guides, 944 liens, zéro erreur/avertissement ; 122 sources
  exportables vérifiées. Aucun email réel, commit, push ou déploiement effectué.

## Traçabilité des 31 critères

La table définit les scénarios attendus. Le bilan d'exécution ci-dessous indique
les tests réellement exécutés et les validations de terrain encore attendues.
Documentation : P = [parcours](README.md), A = [architecture](architecture-contrats.md),
C = [communications](communications-supports.md), G =
[guide backoffice](../../produit/formation/backend/guide-preparation-onboarding-commercant.md).

| Critère | Comportement / propriétaire | Scénario de preuve prévu | Documentation / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| E68-CA-01 | Agenda OnBoard complet et messages cohérents | T01 : confirmation puis pack/rappel, même date/lieu ; répétition sans doublon | P, A, C | Teams + physique | Ordonnanceur et ICS |
| E68-CA-02 | Identité : préparation avant activation, propriété | T02 : BROUILLON/REFERENCE, connexion/reprise, autre marchand refusé ; ACTIF+dossier repris via route explicite conservant ses droits | A : scope et API me | Comptes avant activation et actif repris | Renouveler session existante |
| E68-CA-03 | Support Stripe fidèle au contrat | T03 : revue éditoriale + rendu mobile ; coût Localeo/commission distincts, absence de garanties absolues | C et support public | Aucun mouvement réel | Support approuvé/versionné |
| E68-CA-04 | Documents : préparation guidée sans dépôt marchand | T04 : liste applicable, pièce réutilisée, consigne rendez-vous/canal sécurisé existant, aucun upload ; pièce à apporter non reçue/non vérifiée ; finalisation refusée si preuve requise absente | A, G | Pièce à préparer/valide/remplacée | Contrôles internes existants, pas de nouveau stockage préparatoire |
| E68-CA-05 | PDF avant J, signature le jour J, dépôt interne après rendez-vous | T05 : PDF lisible/imprimable du bon commerçant, refus d'accès au contrat voisin, GET sans effet, lecture explicite, signature jour J et upload interne par gestionnaire habilité ; copie absente/non vérifiée bloque finalisation, signataire incorrect, version imprimée périmée, remise Teams en attente | A, C, ARB-05 | Contrat courant/périmé, copie signée attendue/reçue/vérifiée | Pas de date/signataire par défaut ; aucun upload marchand |
| E68-CA-06 | Commercialisation : contribution sans coffret | T06 : proposer/corriger sans rattachement ; offre applicable protégée | A API propositions | Aucune offre + brouillon | Compatibilité E60/E62 |
| E68-CA-07 | OnBoard : revue de version et conditions | T07 : revue autorisée et motivée ; accord/refus marchand distinct de soumission, habilitation, version/conditions/date ; modification périme l'accord | A, ARB-06 | Offre à corriger/revue/refusée | Auteur et version auditables |
| E68-CA-08 | Fiscalité : réserves explicites | T08 : REVIEW_REQUIRED reste en attente, aucun effet qualification coffret | A, G | Réserve fiscale | Qualification conserve ses droits |
| E68-CA-09 | Exploitation : états exacts par canal | T09 : accepté/livré/incertain/simulé, tentatives et destinataire ; ouverture ne confirme rien | A, G | Échecs et simulation | Polling et supervision |
| E68-CA-10 | Questions : réponse puis résolution | T10 : réponse interne ne ferme pas, confirmation/reprise marchand, autre dossier refusé ; qualification bloquante tracée sans résolution implicite | A API questions | Questions ouvertes/répondues | Affectation et retard |
| E68-CA-11 | Coordination : relances bornées | T11 : réessais certains plafonnés, incertitude bloquée, même clé sans nouvel effet | A, G | Silence et retries | Reprise dédiée, pas générique |
| E68-CA-12 | Rendez-vous : report/annulation/tardif | T12 : avant/après remise, conservation des bonnes preuves, invalidation des mauvaises | A, C | RDV reporté et annulé | Correction et pas d'envoi obsolète |
| E68-CA-13 | OnBoard : revue et maintien adapté | T13 : réserve bloque prêt mais maintien adapté possible ; aucun accès gagné | P, A, G | Stripe en attente | Motif et prochaine action |
| E68-CA-14 | Réunion : quatre phases | T14 : recette chronométrée et cohérence mail/PDF/guide ; dépassement enregistré | C, G | Agenda 10/15/10/25 | Durée réelle, pas de contrôle omis |
| E68-CA-15 | Autonomie sans effet financier | T15 : mobile, connexion personnelle, exercice isolé et aide trouvée ; aucun achat/validation réel | G, P | Scénario démonstration isolé | Mode exercice explicite |
| E68-CA-16 | Bilan/finalisation : preuves actuelles | T16 : tenu+Stripe incomplet, absent, preuve perdue après VALIDE, clôture sans coffret | A, G | Incomplet/absent/sans offre | Pas de clôture/abandon automatique |
| E68-CA-17 | Mesure : dénominateurs explicites | T17 : agrégats sur cohorte connue avec données manquantes/reports, minutes backoffice ; API conservée sans tableau pilote dans OnBoard | A, G | Cohorte déterministe | Aucun zéro imputé, historique conservé |
| E68-CA-18 | Référencement : dossier unique atomique | T18 : ERP/OnBoard/SQLAdmin, rollback et créations simultanées ; même dossier sans email implicite | A producteurs | Marchand nouveau/existant | Migration sans campagne massive |
| E68-CA-19 | Agenda : 60 min et fuseau | T19 : Teams sans lien accepté et ajout ultérieur versionné ; URL fournie non HTTPS et adresse physique absente refusées, date ambiguë/inexistante, rendu UTC/local | A, C | Changement d'heure | Anciennes dates naïves à reprendre |
| E68-CA-20 | Checklist : faits actuels et action utile | T20 : activation, confirmation du mail et suivi repérables ; détails repliés accessibles ; sept étapes métier préservées sans sept formulaires principaux ; pièce à apporter distincte de reçue ; progression historique != prêt actuel | A, G | Dossier sans date et pièce attendue au rendez-vous | Version des faits source |
| E68-CA-21 | Actions humaines seules saisissables | T21 : auteur/date/résultat, preuve auto non modifiable, non applicable justifié | A API actions | Appel réalisé | Audit et contrôle des mutations |
| E68-CA-22 | File OnBoard et autorisations | T22 : filtres, pagination, tri stable, Lecteur/Backoffice/Finance/admin et toutes communes | A, G | Plusieurs référents | Scopes E69, aucun périmètre commune |
| E68-CA-23 | Calendrier préparatoire sans autorisation implicite | T23 : échéance J−7→A_CONFIRMER sans appel fournisseur, silence/retard visibles ; horaire/fenêtre, rattrapage avant J, regroupement, politique modifiée invalidant l'accord | A, ARB-01 | RDV demain/ce jour, intention ancienne sans accord | Aucune autorisation créée par migration/batch |
| E68-CA-24 | SMS autorisé et dépendant du résultat mail | T24 : pack approuvé + acceptation→nominal ; sans accord→aucun ; échec certain→secours à confirmer séparément ; incertain→aucun, bounce tardif→humain | A, C | Table complète, secours confirmé/non confirmé | Aucun nominal+secours automatique |
| E68-CA-25 | Confirmation explicite du pack complet | T25 : aperçu email/mobile/corps/PJ/fenêtre, confirmer/annuler/fermer, POST sans droit→403, aperçu périmé→409, double clic et validations concurrentes sans doublon ; zéro/plusieurs offres, deux PJ, versions et mobile | C, A | Pack en attente/approuvé, prix absent/nom long | Preuve auteur/date/empreinte ; aucun envoi sans accord |
| E68-CA-26 | Autorisation, concurrence et figement | T26 : modifications destinataire/contenu/PJ/RDV/politique invalidant l'accord avant remise ; deux workers, changement après mail avant SMS sans réémission mail, crash après acceptation, polling répété, reprise manuelle confirmée | A tentative/remise | Fournisseur simulé à fautes, ancien client sans confirmation | Contrôle serveur commun API/batch, réessais inchangés bornés |
| E68-CA-27 | Réception explicite authentifiée | T27 : GET/préfetch sans effet, POST idempotent, ancien pack et mauvais propriétaire refusés | A API reception | Ancien/nouveau pack | Pas de preuve par ouverture |
| E68-CA-28 | Consignes de pièces et contrat accessibles en amont | T28 : email et espace sans dépôt E68, liste personnalisée/consigne, contrat accessible ou manque signalé, lien récupérable ; pas de pièce sensible demandée par email | C, A | Pièce déjà fournie ou à apporter | Aucun jeton ancien recyclé |
| E68-CA-29 | ICS stable et versionné | T29 : parse ICS, UID stable, SEQUENCE croissante, report/CANCEL, lieu/UTC/durée | A, C | Teams→physique | Pas de synchronisation promise |
| E68-CA-30 | Rappel à confirmer et contact humain | T30 : J−1 futur, rappel sans accord distinct→aucun envoi même si pack autorisé ; accord valide→rappel ; regroupement, pas de validation/retour→action affectée | A, C, ARB-08 | Silence du gestionnaire/commerçant et RDV passé | Horaires et supervision file A_CONFIRMER |
| E68-CA-31 | Guide réellement accessible ERP | T31 : entrée aide+lien dossier, alias borné, profils réels, bundle sans dépôt voisin, guide manquant | G, A route dédiée | Lecteur/Backoffice/Finance | Manifeste + lecteur + recette cible |

## Tests à préparer dans les applications

### Recette du processus complet V1.2 en sept étapes

Le même commerçant et le même dossier traversent les sept étapes. Les fournisseurs
sont simulés pour les tests ; chaque validation est réalisée par le profil habilité.

| Étape du processus | Actions et résultat observable attendus | Critères principaux |
| --- | --- | --- |
| 1. Référencer et ouvrir le dossier | Créer puis rouvrir : un dossier, référent/checklist/prochaine action ; pas d'envoi ni d'activation implicite | CA-18/20/21/22 |
| 2. Planifier le rendez-vous | Saisir rendez-vous complet d'une heure, calendrier cohérent ; préparer puis confirmer seulement son email, sans autoriser le pack | CA-01/19/29 |
| 3. Préparer et confirmer les communications | J−7 : A_CONFIRMER sans appel fournisseur ; aperçu réel, validation du pack mail/SMS, deux supports et récapitulatif prestations ; suivi par canal | CA-03/09/23/24/25/26 |
| 4. Accompagner la préparation | Initialiser/reprendre le même compte, confirmer réception, télécharger/imprimer le contrat, poser/résoudre une question, examiner propositions/accord, suivre Stripe et pièces sans upload marchand | CA-02/04/05/06/07/08/10/27/28 |
| 5. Faire le point avant J | Consigner maintien/adaptation/report, actions et réserves ; préparer puis confirmer distinctement le rappel J−1 ; aucun envoi obsolète | CA-11/12/13/30 |
| 6. Conduire le rendez-vous | Phases 10/15/10/25, version et signataire contrôlés avant signature jour J, pratique sans paiement/consommation réelle ; autonomie et durée observées | CA-14/15 et CA-05 |
| 7. Enregistrer et finaliser | Gestionnaire déposant et contrôlant la copie signée ; bilan/actions ; refus tant qu'une preuve obligatoire manque, succès sur preuves actuelles, capacités commerciales distinctes | CA-16 et CA-04/05 |

Contrôles transverses : CA-31 ouvre le guide depuis l'ERP livré avec son bundle ;
CA-17 produit un bilan pilote à partir des dossiers et données effectivement mesurés.
Ils ne créent pas une huitième étape.

Ce scénario assemble les 31 critères sans remplacer leurs refus et reprises.
Les lots partiels ne valent pas livraison du processus. Les adaptateurs et
fixtures doivent couvrir ce fil avant toute recette avec envois réellement autorisés.

### Preuves ciblées et non-régression

T01/T12 doivent
prouver que l'accord du pack seul n'autorise ni confirmation du rendez-vous,
ni avis de report ou d'annulation ; leur propre validation est nécessaire,
y compris via les batchs. T26 doit tenter une relance générique email/SMS sur
un message E68 et constater le refus, aucun clone et aucun appel fournisseur.
Les fixtures distinguent A_CONFIRMER, autorisé, accord périmé et émission engagée ;
aucun message réel n'est envoyé pour ces scénarios.

Backend, runner isolé prévu par ses instructions locales :

- Domaine : étendre `tests/domain/conformite_fiscale_bum/test_onboarding.py`, ajouter
  politique calendrier, transitions de préparation et fraîcheur des preuves avec horloge figée.
- Application : étendre les tests d'accès préparation, onboarding contrat/progression/
  sans coffret ; ajouter orchestration d'ouverture commune, contributions, questions
  et consignes documentaires sans dépôt marchand.
- Communications : étendre email/SMS batch et fournisseur, avec faux transport capable
  de timeout avant/après acceptation, réponse illisible, crash et résultat de livraison tardif.
- Persistance : vrais tests PostgreSQL isolés pour unicité/conflits, deux workers,
  modification concurrente du rendez-vous/contact et frontière de remise. SQLite ou un
  mock ne suffit pas à prouver les verrous ni la reprise après perte de connexion.
- Adaptateurs : PDF, ICS, source documentaire et conservation ; contrôles existants
  des pièces et stockage des PJ figées, sans pipeline de téléversement marchand ;
  test `tests/infrastructure/test_documentation.py` et autorisations E69 de la route guide.
- Architecture : frontière domaine/application et contrats OpenAPI générés.

Commerçant : Vitest sur `MerchantPreparation`, contrats API, connexion/reprise,
checklist/questions et erreurs version ; Playwright mobile sur préparation complète,
refus croisés et navigation après initialisation. L'ERP reçoit une recette avec
profils Lecteur/Backoffice/Finance/admin, navigation clavier et messages d'erreur.

Ne pas charger `.env.test` ou appeler app.main avec configuration d'exploitation
pour lancer ces preuves. Utiliser DB et fournisseurs isolés, aucune notification réelle.

## Migration, démonstration et recette cible

1. Les valeurs calendaires et la grille de revue sont validées. Approuver les supports ;
   appliquer la conservation des pièces, questions et messages selon le registre existant.
2. Migrations additives backend fournies et rejouées sur PostgreSQL jetable : structures, index, versions et contraintes ;
   garder les dossiers historiques inactifs pour E68. Reprendre les dates naïves seulement
   après validation du fuseau. Tester upgrade sur copie isolée et réexécution prévue par l'outil.
3. Adaptation de `onboarding.py` : sans date, Teams/physique, question bloquante,
   annulation. Les autres refus et incertitudes sont couverts par les fixtures de
   tests ; ils ne sont pas tous ajoutés au jeu de démonstration partagé.
   IDs déterministes, restauration cohérente, aucune émission réelle.
4. Livrer le backend additif, bundle documentaire et supports rendus ; livrer le contrat
   et frontend Commerçant, puis activer le parcours sur une cohorte explicitement choisie.
   Renouveler les anciennes sessions par connexion, sans élévation silencieuse.
5. Vérifier sur cible : deux canaux de test autorisés, mail/PJ/ICS réels, accès préparatoire,
   reprise, guide depuis les deux entrées ERP et finalisation avec contrôle des réserves.
6. En incident : désactiver la politique de programmation/remise E68,
   conserver rapprochement et historique. Ne pas annuler une tentative déjà engagée comme
   si elle n'avait jamais été remise. Pas de downgrade destructif des nouvelles preuves.

### Configuration de la version implémentée, sans valeurs secrètes

| Paramètre | Existant ou cible | Action de livraison |
| --- | --- | --- |
| `LOCALEO_FEATURE_MERCHANT_ONBOARDING_ENABLED` | Existant | Vérifier le socle OnBoard ; ce flag seul n'autorise pas la campagne E68 |
| Activation et version politique E68 | Ligne versionnée `politique_preparation_onboarding` | `active=false` au déploiement initial ; paramètres validés ci-dessous, aperçu des intentions affectées |
| `url_preparation` | Champ de la politique E68 | Origine HTTPS Commerçant et chemin `/preparation` ; aucune URL ERP/admin ni jeton de dossier |
| `LOCALEO_FRONT_COMMERCANT_PASSWORD_INIT_URL_TEMPLATE`, `LOCALEO_FRONT_COMMERCANT_PASSWORD_RESET_URL_TEMPLATE` | Existants | Vérifier les routes Commerçant du bon environnement ; ne pas réutiliser `LOCALEO_ERP_URL` |
| `LOCALEO_PASSWORD_INIT_TOKEN_TTL_HOURS`, `LOCALEO_PASSWORD_RESET_TOKEN_TTL_MINUTES` | Existants | Garder la politique d'accès distincte des 7 jours de préparation ; récupération disponible |
| `BREVO_EMAIL_API_KEY`, `BREVO_SMS_API_KEY` / fallback `BREVO_API_KEY`, expéditeurs | Existants | Vérifier canaux et expéditeurs autorisés sans exposer les valeurs ; rapprochement activé |
| `EMAIL_DEV_MODE`, `SMS_DEV_MODE` | Existants | Simulation dans preuves locales/démo ; affichage explicite, interdiction de mélanger simulation et canal réel dans une campagne |
| `LOCALEO_DOCUMENTATION_ROOT` | Existant | Bundle exporté et contrôlé, comprenant guide et sources des supports ; pas de dépendance à un dépôt voisin en release |
| Supports approuvés/version/empreinte | Champs de la politique E68, sources documentaires exportées | Deux PDF rendus et vérifiés localement ; approbation éditoriale encore requise ; campagne bloquée si absent/non approuvé |
| Stockage privé documentaire | Existant, pas de dépôt préparatoire marchand nouveau | Préserver contrôles internes et conservation des pièces existantes/PJ figées ; aucune configuration d'upload E68 requise |
| Ordonnanceur et supervision | Batch `onboarding.preparation` ajouté au catalogue existant | Toutes les deux minutes : préparation, remise autorisée et rapprochement ; aucun double ordonnanceur |

Les nouveaux réglages E68 sont persistés dans la politique ; aucune nouvelle clé
secrète `.env` n'est introduite. Cette table ne modifie aucun environnement.

## Historique : vérification documentaire avant implémentation

Contrôles exécutés le 3 octobre 2026 sur la consolidation préalable au code :

- Revue indépendante du parcours, des contrats, des communications, du guide et
  de la recette : 31 critères et invariants préservés, sept étapes cohérentes.
  Les deux précisions relevées (action de rappel à l'étape 5 et portée du contrat
  Commerçant) sont intégrées. Cette revue ne vaut pas validation applicative.
- `check_guidance.py --document` sur le backlog : **91 guides, 972 liens,
  0 erreur, 0 avertissement** ; `--changed --all-markdown` : **16 guides,
  286 liens, 0 erreur, 0 avertissement**.
- `sync_documentation.py --check-sources` : **122 sources vérifiées** ; bundle
  local ignoré `.artifacts/epic68-v12/documentation` généré puis contrôlé par
  `--check` : **122 documents vérifiés**.
- Contrôleur backend du snapshot : **123 documents distribués et sources
  canoniques vérifiés** ; lecteur réel `resolve_ops_document` : **3 alias E68
  lus avec succès**, racine fixée au bundle V1.2 sans charger l'application.
- `git diff --check` : succès. Aucun code applicatif modifié.

Les anciens résultats documentaires sont archivés dans l'historique du
[backlog](../../roadmap/en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md) ;
ils ne constituent pas une preuve de l'état courant.

Cette ancienne consolidation documentaire ne constituait pas une validation métier.
L'état courant est **En cours**, avec le bilan d'implémentation ci-dessous.

## Implémentation V1.2 et preuves locales — 3 octobre 2026

Dépôts modifiés : **backend** (domaine, application, API, ERP, migrations,
ordonnanceur et démonstration), **Commerçant** (même compte, parcours et reprise)
et **projet** (sources canoniques et exports). Animation et Marketplace ne sont
pas consommateurs de ces nouvelles routes ; aucun changement requis dans ces dépôts.

Les nouveaux dossiers sont ouverts dans la transaction de référencement ; la
création SQLAdmin est désactivée au profit du référencement ERP. Les anciennes
préparations nécessitent une reprise explicite. Les commandes sont versionnées,
avec reçus d'idempotence persistés et verrou du dossier. Les sept étapes ERP
affichent les faits actuels, questions, revues, rendez-vous et bilan ; les
droits proviennent des scopes E69 globaux. La préparation commerçant utilise
le scope `commercant:preparation` et la route `/preparation`, sans téléversement.

Les preuves locales couvrent notamment :

- `test_preparation_onboarding.py`, `test_service_preparation_onboarding.py`
  et les tests OnBoard existants : transitions, propriété, signatures courantes,
  versions, réception explicite, questions, grille et refus, bilan et finalisation.
- `tests/security/test_preparation_onboarding_postgres.py` et
  `tests/security/test_communications_preparation_postgres.py` : PostgreSQL local
  jetable sur 127.0.0.1:55447, migrations rejouées, rollback, doubles commandes,
  conflits de versions, deux workers, tentative durable avant remise et crash
  après acceptation sans répétition automatique. Les simulations SQLite ne sont
  pas utilisées comme preuve des verrous PostgreSQL.
- `test_preparation_communications.py`, `test_communications_preparation.py`
  et `test_preparation_supports.py` : calendrier, confirmation, empreintes,
  états par canal, reprise, PDF déterministes et ICS. Les quatre pages des
  deux PDF ont été rendues et inspectées ; cela ne vaut pas approbation éditoriale.
- `test_preparation_onboarding_api.py` : 22 contrôles HTTP exécutés à ce stade,
  chemins, scopes, acteur serveur, version, idempotence, refus et contrat courant
  authentifié avec contrôle d'empreinte et `Cache-Control: no-store`.
- `test_preparation_documents.py` et `test_lien_preparation.py` : pas de date
  ni signataire inventé, version obligatoire, signature réellement renseignée,
  destination de reprise fixe sans altérer le jeton d'identité. Avec les contrôles
  du registre et des conventions de démonstration : 19 tests réussis.
- Commerçant : tests Vitest du parcours, des sessions et contrats ; scénarios
  Playwright 390/1280 px avec contrôle d'accessibilité, mutations et reprise après
  initialisation. ERP : `tests/frontend/test_preparation_browser.mjs` exécute les
  vrais scripts avec API interceptée, planification, revue, aperçu/confirmation,
  conflit et réponses tardives après changement de dossier.

La démonstration classe les quatre nouvelles tables et utilise les commandes
ordinaires pour des dossiers sans date, Teams, physique, question bloquante et
annulation. Aucun worker de remise ni autorisation d'envoi n'est invoqué par le
générateur. Une génération complète sur environnement partagé n'est pas exécutée.

### Résultats consolidés sur l'arbre de travail

Bases Git : backend `33face64569eee20ce64a8967cff9d61454e3860`, Commerçant
`38ff5ad32b1a4231de432d61474b00eb71cbf9c8`, projet
`6663d2fcb2065ba91e4aedd6b9ffdd6bbee9069a`, avec modifications locales non commitées.
Ces nombres décrivent des lots qui se recoupent ; ne pas les additionner.

| Lot exécuté | Résultat | Critères éclairés |
| --- | --- | --- |
| Noyau, API, E50, architecture et six scénarios PostgreSQL | 598 réussis ; unicité, rollback, versions, filtres et pagination réels | CA-02/04/05/06/07/08/10/13/16/17/18/19/20/21/22/27/28 |
| Communications, supports et cinq scénarios PostgreSQL | 40 réussis ; changement de contact entre mail et SMS, issue incertaine, reprise, déterminisme des PDF | CA-01/03/09/11/12/23/24/25/26/29/30, hors approbation éditoriale CA-03 |
| Dernier verrou documentaire et intégrations existantes | 52 réussis, dont deux ordres concurrents finalisation/rattachement sur PostgreSQL | CA-04/05/16/26 |
| Permissions ERP, guide depuis bundle, liens de récupération et métadonnées documentaires | 25 réussis | CA-02/05/22/28/31 |
| Démonstration, registre et conventions | 14 réussis ; deux passages et reprise le lendemain, 11 reçus inchangés, aucun transport/autorisation | CA-18/19/20/23/26 |
| Contrôles requis après les derniers correctifs : `tests/architecture`, `test_domain_dedicated_classes.py`, `test_use_case_business_test_coverage.py` | 453 réussis | Frontières et couverture structurelle ; ne remplacent pas les preuves métier |
| Vitest Commerçant | 72 réussis, 7 fichiers | Parcours, sessions, contrats et récupération |
| Navigateurs Commerçant | 4 scénarios validés, 390/1280 px, initialisation et récupération ACTIF | CA-02/05/07/10/20/27/28 ; accessibilité automatisée |
| Navigateurs ERP | 3 scénarios réussis, vrais scripts et API interceptée | CA-19/20/21/25/26 ; changement de dossier et réponse tardive |
| Node ERP existant et conversion de fuseau | 12 réussis | Non-régression pagination/progression et heures ambiguës/inexistantes |

Le build optimisé servant aux tests navigateur utilise
`scripts/build-browser-tests.mjs`, configuration TEST explicite et chargement
`.env` désactivé. Aucun build avec configuration de production n'a été exécuté.
Les captures locales ignorées sont `localeo-commercant/tmp/preparation-390.png`,
`preparation-1280.png` et `localeo-backend/tmp/preparation-erp/erp-390.png`,
`erp-1280.png`. Elles ne constituent pas une recette sur environnement déployé.

Le verrou documentaire acquiert le dossier avant le document source et avant tout
flush, afin de sérialiser finalisation et nouveau rattachement. Les fichiers
`test_verrou_rattachement_documentaire.py` et
`test_rattachement_documentaire_preparation_postgres.py` portent cette preuve.
Deux avertissements de cycles de clés étrangères proviennent de la fixture ERP
documentaire existante ; aucun échec n'a été masqué. Le cluster PostgreSQL jetable
a été arrêté après les tests ; aucune migration de base partagée n'a été exécutée.

La revue indépendante a conduit à corriger les restrictions de l'ancien profil
Exploitation, l'arrêt des envois sur dossiers terminaux, les accords manquants,
la reprise après récupération d'accès, la confidentialité de la projection
marchande et les verrous documentaires/coordonnées. Les profils E69 gardent leurs
scopes globaux ; les données internes ne passent pas dans la projection publique.

Documentation finale : `check_guidance.py --changed --all-markdown` : **18 guides,
308 liens, zéro erreur/avertissement** ; contrôle transverse sans filtre :
**90 guides, 944 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources` :
**122 sources**. Bundle `.artifacts/epic68-v12/documentation` régénéré et contrôlé :
**122 exports**, puis lecteur backend : **123 documents distribués et sources
vérifiés**, manifeste inclus. Diff des trois dépôts sans erreur.

Limites de recette : ARB-07 (approbation des deux supports), réunion chronométrée,
exercice réel accompagné et mesure du pilote restent à réaliser sur une cible
déployée. Les tests locaux ne prouvent pas la délivrabilité réelle des fournisseurs
ni les délais et résultats d'une cohorte de commerçants. L'epic n'est pas clôturée.

## Configuration concrète de livraison

1. Appliquer les migrations additives `v254_epic68_preparation.sql` puis
  `v255_communications_preparation_onboarding.sql` avec le circuit normal de migration. Elles
   n'activent aucun ancien dossier ni aucune campagne.
2. Déployer le backend et le frontend Commerçant compatibles, avec le bundle
   documentaire contenant le guide et les deux sources de supports. Vérifier
   `LOCALEO_DOCUMENTATION_ROOT` et l'empreinte du bundle.
3. Vérifier `LOCALEO_FEATURE_MERCHANT_ONBOARDING_ENABLED`. Dans un dossier OnBoard,
   l'administrateur historique ouvre les paramètres des communications. La ligne
   `politique_preparation_onboarding` contient la politique versionnée, initialement
   `active=false` : `delai_pack_jours=7`, `fuseau=Europe/Paris`, `heure=10`,
   `fenetre_debut=9`, `fenetre_fin=18`, `revue_jours=2`, `contact_heures=48`,
   `rappel_jours=1`. Ce sont des paramètres de politique, pas des variables `.env`.
4. Renseigner `contact_localeo` et `url_preparation` (origine Commerçant de la cible,
   chemin `/preparation`, HTTPS, sans jeton). Prévisualiser puis approuver les deux
   supports par leur empreinte source ; une modification de source exige une
   nouvelle approbation. Enregistrer avec motif et vérifier les intentions affectées
   avant d'activer la politique.
5. Vérifier les modèles d'URL d'initialisation/récupération Commerçant, les TTL et
   expéditeurs Brevo existants. Garder `EMAIL_DEV_MODE` et `SMS_DEV_MODE` cohérents.
   Une simulation est affichée comme telle et ne vaut ni remise réelle ni réception.
   Les clés sont les paramètres existants du déploiement ; aucun secret nouveau
   propre à E68 n'est ajouté.
6. Vérifier le batch `onboarding.preparation`, enregistré dans l'ordonnanceur
   existant toutes les deux minutes, endpoint protégé par `internal:batch`.
   Les échéances créent des intentions à confirmer ; seules les séquences
   expressément autorisées sont remises. Toute issue inconnue reste à rapprocher.
7. Renouveler les anciennes sessions Commerçant par reconnexion pour obtenir le
   nouveau scope. Reprendre les dossiers historiques individuellement et vérifier
   le fuseau des anciennes dates. Tester les deux entrées du guide : dossier OnBoard
   et fiche commerçant ERP.

Arrêt d'urgence : désactiver la politique E68 ; conserver l'historique et le
rapprochement. Ne pas employer une relance email/SMS générique pour contourner une
incertitude. Une reprise exige preuve de non-remise et confirmation du contenu
toujours courant ; un changement de contenu exige une nouvelle intention.

## Livraison sur TEST du 3 octobre 2026

Le [reçu de livraison TEST](livraison-test.md) conserve les commits publiés, les
migrations exécutées, les contrôles sur la cible et le blocage documentaire
Render restant. Le code est déployé ; la livraison complète et la clôture ne sont
pas déclarées tant que ce blocage et la recette attendue ne sont pas levés.
