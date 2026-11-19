# E73 — Gestion autonome des commerçants Animation

Évolution du **18 novembre 2026 — E73-EVO-AUTONOMIE-COMMERCANTS**.
Spécification et implémentation demandées ; la clôture historique E73 est conservée.
Le bilan ci-dessous distingue les preuves locales de la mise en service.

## Besoin et changement de règle

Le gestionnaire habilité gère les commerces exclusivement Animation de sa
commune depuis Animation : créer, consulter, modifier, ouvrir ou retirer le
périmètre Animation et inviter le responsable dans Pro. Aucune validation
Localeo, KYC, Stripe, information de facturation, convention Coffrets ou
rendez-vous d'onboarding ne conditionne ces opérations.

Avant cette évolution : `MerchantReferenceRequests` transmet une demande ;
`DemandesReferencement.decider` dans le backend exige une décision ERP et crée
seulement un brouillon, sans accès. Cette évolution remplace ce détour pour les
commerces Animation seule : WA-07/08, DEC-54/99 et OA-01/02 sont précisés dans
ce périmètre. Les anciennes demandes restent consultables ; leur état ne vaut
pas activation. Les imports conservent leurs droits commerciaux et contrôles
de rapprochement ; leurs fiches Animation peuvent ensuite être gérées ici.

La gestion du réseau, l'accès personnel Pro et l'accord pour chaque animation
restent trois faits distincts. La création n'accepte aucune participation et
n'envoie aucun email. L'invitation Pro est une action explicite ; le responsable
initialise lui-même son accès. Aucun rôle ERP n'est attribué au gestionnaire.

## Parcours et règles

- Rubrique **Commerçants**, liste paginée et recherche dans la commune active ;
  accès également depuis la sélection d'un commerce manquant. Formulaire court :
  nom, adresse, catégorie, SIRET et email ; contact, téléphone et description
  facultatifs. Le SIRET identifie le commerce, sans demande de justificatif KYC.
- Création atomique d'une fiche active et du seul produit Animation, utilisable
  immédiatement dans la sélection des animations. Coffrets reste fermé même
  lorsque la commune utilise encore le mode historique de périmètres.
- Fiches existantes explicitement qualifiées Animation seule : modification et
  ouverture sans validation Localeo. Une fiche non qualifiée, mixte ou Coffrets
  n'est jamais requalifiée automatiquement. Suspension globale prioritaire.
- Modification versionnée, sans changer la commune. Les collisions de nom dans
  la commune, email ou SIRET sont refusées sans révéler une fiche hors périmètre.
  Changer l'email de contact ne transfère jamais un compte Pro existant.
- Retrait réversible du produit Animation, avec confirmation : plus de nouveaux
  engagements ; historique, participations acceptées aux animations publiées et
  bons déjà attribués conservés selon le mécanisme de continuité E73. Il ne s'agit
  pas d'une suppression physique ni d'une suspension globale du commerçant.
- Invitation et renvoi réservés à un accès non initialisé, non verrouillé et au
  contact déjà lié s'il existe. Aucun changement de mot de passe ou de login d'un
  compte initialisé par l'organisateur. Expiration, récupération personnelle et
  révocation conservent leurs circuits existants.
- Ajouter Coffrets suit le parcours habituel avec ses prérequis ; Animation
  reste disponible. Les modifications de données communes d'un commerce devenu
  mixte sortent du présent droit de gestion Animation seule.

## Propriétaires et contrat

`referencement` porte l'éligibilité à la gestion autonome et l'ouverture du
produit ; `Commercant` porte les données communes et son activation ;
`identite_acces` conserve le compte, les tokens et la vérification personnelle.
`animation_locale` conserve les accords de participation. Les services orchestrent
les transactions, les adaptateurs persistent, les interfaces présentent.

API additive sous `/protected/referencement/commercants-animation` : liste
`GET` (recherche, curseur, 25 par défaut, 100 maximum), création `POST`, détail
`GET /{id}`, modification `PATCH /{id}`, commandes `POST /{id}/{action}` pour
`activer`, `retirer`, `inviter`, et reçu `GET /recus/{cle}`. Catégories fournies
par `GET /categories`. Session Animation/CSRF et permission courante
`animation:gerer_participations_commercants`, commune serveur et organisation
active contrôlées avant action et avant rejeu. Les DTO portent les actions
disponibles, versions de fiche et de périmètre, état Animation et accès Pro.
Réponses privées sans cache ; aucune URL/token d'invitation dans les réponses.

Écritures avec clé d'idempotence, empreinte et versions attendues ; reprise avec
la même clé et le même corps, aucune répétition automatique. Les droits sont
revérifiés, les réponses tardives invalidées lors d'un changement de contexte.
Audit avant/après et email en file dans la même transaction. Liste filtrée avant
pagination, sans chargement exhaustif ; recherche et saisie restent montées.

## Critères et traçabilité

| Critère | Résultat observable | Preuve prévue et impacts |
| --- | --- | --- |
| GCA-01 | Créer un commerce Animation actif sans validation Localeo ni dossier d'onboarding | Domaine, transaction PostgreSQL et parcours Animation ; API et guide |
| GCA-02 | Ni Stripe/KYC/facturation/contrat demandés ; Coffrets fermé même en mode communal historique | Refus domaine/API et capacités Pro ; source de périmètres partagée |
| GCA-03 | Liste/recherche/détail/édition limités aux commerces Animation seule de la commune | Droits révoqués, autres communes, mixte et fiches non qualifiées ; adaptateurs et UI |
| GCA-04 | Modification versionnée, collision sans fuite, aucun transfert d'accès Pro par changement de contact | Tests conflits, identité et API ; audit et données existantes |
| GCA-05 | Invitation explicite/reprise sans double email ; compte initialisé ou verrouillé protégé | Transaction/outbox et domaine d'accès ; aucune notification réelle de recette |
| GCA-06 | Retrait puis réactivation, sans effacer historique ou engagements protégés | Domaine et PostgreSQL ; continuité et refus de suspension globale |
| GCA-07 | Création et activation n'acceptent aucune animation ; ajout Coffrets conserve ses contrôles | Non-régression participation/périmètres/Pro |
| GCA-08 | Double clic, réponse perdue, version obsolète et perte de droits ne produisent aucun effet supplémentaire | Idempotence, concurrence, rollback, lecture de reçu autorisée |
| GCA-09 | Mobile/clavier, filtres/saisie/focus conservés, succès/refus/incertain compréhensibles | Recette navigateur 390/1280 px, petits écrans et zoom ; consommateurs des libellés |
| GCA-10 | Sources et contrats synchronisés ; lectures bornées ; migration et démonstration examinées | OpenAPI producteur/embarqué, tests adaptateurs, mesures N/10N, liens et exports |
| GCA-11 | Distinguer dernier mail d'initialisation, mot de passe défini et au moins une connexion réussie | Projection des preuves existantes, absence d'historique explicite, aucun secret exposé ; détail ci-dessous |

## Correctif du 19 novembre 2026 — suivi de l'accès Pro

Le seul résumé « invité / initialisé » ne permettait pas au gestionnaire de
savoir où en était le nouveau commerçant. La liste présente désormais trois
étapes indépendantes, actualisables avec la liste sans perdre recherche,
saisie ni focus :

- **Mail de création du mot de passe** : dernier email d'initialisation de ce
  commerce, destinataire réel, demande et/ou envoi daté, attente, en cours,
  envoyé, livré, ouverture signalée, échec temporaire/définitif ou annulation.
  « Envoyé » indique explicitement que la livraison n'est pas confirmée.
  Livraison/ouverture sont des signaux du service email, sans preuve de lecture
  humaine. Aucun envoi retrouvé reste distinct d'un échec ou d'une livraison.
- **Mot de passe** : défini ou pas encore défini, avec la date de configuration
  lorsqu'elle existe ; la présence historique d'un mot de passe sans date
  n'invente pas de date. Cette étape ne prouve aucune connexion.
- **Connexion à Pro** : « Connecté au moins une fois » seulement si une dernière
  connexion réussie est enregistrée, avec cette dernière date ; sinon « Aucune
  connexion enregistrée ». Il ne s'agit pas de la date de première connexion.
  Le verrouillage courant est signalé séparément et ne supprime pas l'historique.

Le champ additif `suivi_acces` des fiches expose `email_initialisation`
(`statut`, `destinataire`, `cree_le`, `envoye_le`), `mot_de_passe_defini`,
`mot_de_passe_defini_le`, `derniere_connexion_le` et `acces_verrouille`.
Il peut être absent/null dans les anciens reçus : l'interface indique alors
un suivi indisponible et propose l'actualisation, sans inventer une étape.
Les dates API sont UTC et l'affichage utilise l'heure de Paris.

La projection réutilise les faits des domaines `identite_acces` et `exploitation`.
Elle sélectionne le dernier email `INITIALISATION_ACCES_COMMERCANT`, rattaché
par `source_type=COMMERCANT` et identifiant de commerce, avec un ordre total
date/identifiant. Un autre email, une récupération de mot de passe, le changement
du contact ou une ancienne invitation livrée ne remplace pas la preuve du dernier
envoi. Jointure bornée à un email par commerce, index existant `source_id`, aucune
requête supplémentaire par ligne. Les droits de commune et l'idempotence restent
ceux de GCA-03/05/08 ; aucun corps d'email, lien, token, hash ou diagnostic
fournisseur privé n'est exposé.

Impacts : Backend, Animation et contrat E41 canonique/embarqué. Pro et
Marketplace n'ont pas de changement de contrat consommé ; les écritures
d'authentification restent existantes. Sans migration ni réparation de données :
les faits sont déjà persistés. Sans changement de générateur/restauration :
aucune nouvelle donnée stockée ; les fixtures de recette couvrent ces états.
L'exploitation conserve les traitements d'envoi et de remontée des statuts
existants ; un fournisseur sans confirmation laisse la livraison non confirmée.
Aucun envoi réel ni déploiement n'est impliqué par les preuves locales.

Preuves locales du correctif sur Backend `ef913e85`, Animation `d71be34` et
Projet `dd14e11`, plus modifications non commitées :

- Reproduction API avant correction : échec sur l'absence de `suivi_acces`.
  Après correction, runner isolé backend sur `tests/architecture`,
  `tests/domain/test_domain_dedicated_classes.py`,
  `tests/application/use_cases/test_use_case_business_test_coverage.py`,
  `tests/api/test_gestion_commercants_animation_api.py` et
  `tests/application/use_cases/test_identite_acces_use_cases.py` : **789 réussis**.
- `tests/security/test_gestion_commercants_animation_postgres.py`, via le même
  runner avec PostgreSQL 18 local jetable explicite : **11 réussis**, sans skip.
  Envoi/mot de passe/connexion indépendants, dernier renvoi en échec malgré
  ancienne livraison, autre commerce/récupération ignorés, destinataire conservé,
  permissions, idempotence et lecture N/10N sans requête par ligne vérifiés.
- Animation : types et lint réussis, **391 tests Node réussis**, build isolé
  `tmp/quality-build-DvxSDQ` réussi (avertissement de bundle > 500 ko).
  `tests/browser/merchant-network.mjs` : API synthétique, 1280/390/320 px,
  texte 200 %, états d'accès, conservation de saisie/focus et purge sur 403.
  Rapport et captures examinées dans Animation :
  `tmp/merchant-network-1795071372399/report.json`.
  Le premier essai avait des accents altérés dans les assertions ajoutées au
  banc ; encodage corrigé, assertions conservées et recette rejouée avec succès.
- OpenAPI exporté hors ligne puis normalisé par le générateur E41 ; contrat
  embarqué identique. Guides et 151 sources exportées contrôlés sans erreur.
  Pas de recette connectée ni d'appareil physique ; aucune preuve de livraison
  d'un email réel produite par cette recette.

## Impacts et lots

1. Backend : domaine, commandes autonomes, persistance minimale de l'identité
   déclarée hors dossier d'onboarding, audit et contrats ; tests métier et API.
2. Animation : rubrique réseau et entrée depuis la sélection, formulaire,
   commandes, reprise et recette visuelle. Aucun module Import payant imposé.
3. Intégration : accès Pro existant, catalogue/éligibilité, non-régressions,
   contrats embarqués, migration, documentation et démonstration.

Pro et Marketplace/Live consomment les mêmes faits de produit : vérifier le
refus Coffrets et la continuité Animation sans ajouter de règle dans ces UI.
ERP/OnBoard conservent l'onboarding Coffrets et les demandes historiques. Le
nouveau parcours ne crée pas de dossier à faire valider. L'ajout Coffrets doit
pouvoir ouvrir son dossier ultérieurement. Les imports CRM ne créent toujours
pas un commerce opérationnel.

La migration est additive et ne convertit aucune fiche existante. Les fixtures
doivent couvrir un commerce autonome sans onboarding ; vérifier sauvegarde et
restauration des nouvelles données dans le générateur backend. Aucun jeu réel
ni secret déplacé. Livrer migration/backend avant le frontend ; OpenAPI
documentaire canonique dans Projet et copie consommée dans Animation.

## Bilan local du 18 novembre 2026

Implémentation dans Backend et Animation, documentation canonique dans Projet.
Réalisation initiale sur des arbres non commités, basés sur Backend
`94d64b824e44`, Animation `fe23313d3853` et Projet `5787f2a91ade`.
Les opérations TEST et Git ensuite autorisées sont distinguées ci-dessous.
La gestion est partagée entre les gestionnaires habilités de la commune,
y compris lorsque l'organisation créatrice est différente : décision utilisateur
du 18 novembre. La provenance de création reste tracée, sans droit de propriété
exclusif ni ouverture d'accès hors commune.

| Critères | Code et preuves exécutées | Résultat local |
| --- | --- | --- |
| GCA-01/02/07 | `GestionCommercantsAnimation`, `PerimetresCommercant.controle_produits`, test PostgreSQL `test_gestion_commercants_animation_postgres.py` et domaine `test_gestion_animation_autonome.py` | Création concurrente unique sans onboarding, facturation, accès ni email ; Coffrets refusé même en mode communal historique ; demande Coffrets ERP possible, activation refusée sans ses prérequis et dossier ouvrable ensuite |
| GCA-03/04/08 | Repository communal, gardes d'identité partagées avec Import, versions et reçus ; même suite PostgreSQL | Hors commune, mixte, permission révoquée, collision, version obsolète et rejeu vérifiés ; deux organisations voient la même fiche, une seule modification concurrente aboutit |
| GCA-05 | Invitation explicite dans la transaction, `IdentifiantCommercant.verifier_initialisation`, verrou d'accès ; tests PostgreSQL et `test_identite_acces_use_cases.py` | Rejeu sans double email, changement de contact sans transfert de compte, rollback après outbox, deux liens concurrents donnant une seule initialisation ; ancien lien refusé sur compte initialisé/verrouillé |
| GCA-06/07 | Domaine/repository de périmètres, tests `test_perimetres_commercants_postgres.py`, `test_perimetres_validations_postgres.py`, projection Pro | Retrait/réactivation, droits acquis ciblés, suspension prioritaire, historique et refus de nouveaux droits vérifiés |
| GCA-09 | `MerchantNetworkWorkspace`, fenêtre contextuelle ; `tests/browser/merchant-network.mjs` et `wa-reference-vues.mjs` | Parcours à 1280/390/320 px, zoom texte 200 %, reprise après réponse perdue, liste en erreur préservant saisie/focus, purge sur 403, retour au sélecteur et absence du bouton sans permission ; captures examinées |
| GCA-10 | OpenAPI E41 et copie `src/imports/openapi.json`, migration `v327`, registre démonstration, test N/10N | Contrats identiques ; migration appliquée sur PostgreSQL 18 jetable ; 3 requêtes par page de 25 à 101 et 1001 commerces, maxima sur 5 lectures de 53,4 et 64,1 ms ; curseurs sans doublons et plan `EXPLAIN ANALYZE` exécuté |

Commandes backend via `py scripts/validation/test_isolated.py`, Python 3.14,
avec `--postgres-test-url` explicite pour les schémas jetables :

- Suite ciblée GCA/API/session/registre : **143 réussis** ; domaine et anciennes
  demandes : **27 réussis**. Les contrôles d'architecture, couverture métier,
  accès, API GCA et registre renouvelés après les derniers changements donnent
  **839 réussis**, sans skip (`.artifacts/gca-architecture-final.txt`).
- Suite transactionnelle GCA finale : **9 réussis**, sans skip ; relevés N/10N
  dans `.artifacts/gca-final-postgres.txt`.
- Deux preuves complémentaires réussies : création sans aucune demande de
  participation et restauration de l'identité/provenance avec son périmètre
  immédiat (`.artifacts/gca-creation-restore-final.txt`). Le test de transfert
  du registre utilise SQLite ; il complète la compatibilité PostgreSQL.
- Suite élargie périmètres/Import/Pro/accès : **97 réussis, 2 échecs**.
  Les deux échecs Import sont reproduits sur le SHA de départ dans un worktree
  isolé : fixture de collision avec adresse vide (refus de création avant
  collision), et purge d'artefact après levée de gel (0 au lieu de 1).
  Aucun test ni assertion affaibli ; rapports `.artifacts/gca-regressions.txt`
  et `.artifacts/gca-baseline-tests.txt`. Ces défauts préexistants ne sont pas
  déclarés corrigés par cette évolution.

Animation : `pnpm typecheck`, `pnpm lint`, **391 tests réussis sans skip** et
build isolé final `tmp/quality-build-Q1SF4n` ; avertissement de bundle supérieur à
500 ko conservé. Recettes synthétiques sans appel à un fournisseur réel :
`tmp/merchant-network-1795017113700/report.json` et
`tmp/wa-reference-vues-1795017125258/report.json`.
La correction du focus du dialogue et la visibilité du résultat incertain et
des confirmations dans la fenêtre mobile sont vérifiées sur le dernier build.

Projet : contrôle des guides et du nouveau document sans erreur ni avertissement,
et **151 sources exportées vérifiées**. Empreinte SHA-256 commune aux contrats :
`e823e5efec8c402d844a3ca87db8032d6fd6b482149418e78ed14ed6f58b40ae`.
Pro et Marketplace restent sans modification : les autorisations produits sont
centralisées dans le backend. Les **16 tests Pro de navigation et de contrat**
(`merchantNavigation.test.js`, `features/perimetres/contracts.test.js`) passent,
y compris Animation seule avec bascule communale désactivée. Leurs parcours
complets en navigateur ne sont pas rejoués. La recette sur appareils physiques et l'environnement cible restent
à effectuer après livraison. La revue indépendante a porté sur la conception,
les agents de revue n'ayant pas eu accès aux outils de lecture du dépôt.

La compatibilité complète génération/transfert/restauration a réussi sur
deux clusters PostgreSQL 18 jetables : **14 tests réussis sans skip**, en
1042 secondes, avec `scripts/validation/run_demo_compatibility_tests.py` et
les clients PostgreSQL 18. Génération, visibilité par les lecteurs usuels,
installation, échec injecté, reprise et restauration du jeu original sont
exécutés. Rapport : `tmp/gca-demo-compat-utf8-20261118/results.xml` dans Backend.
Onze avertissements SQLAlchemy de réflexion `dialect_options` restent visibles ;
ils ne sont pas des échecs. Le premier essai sur un cluster initialisé SQL_ASCII
a échoué avant les tests ; il a été remplacé par ces clusters UTF-8, sans changement
applicatif ni affaiblissement des contrôles.
Le registre classe `fiches_commercants_animation` comme donnée métier à remplacer
avec son jeu, sans reprendre l'identité d'un jeu précédent comme référentiel.

## Migration TEST et publication Git autorisées le 18 novembre 2026

Demande utilisateur explicite : migrer la base de test, committer et pousser
les changements des trois dépôts concernés. Le schéma TEST a reçu uniquement
`v327_commercants_animation_autonomes.sql` le **18 novembre à 18 h 15,
Europe/Paris**, avec le runner canonique, après contrôle des empreintes et
vérification que la cible diffère des bases production et démonstration.

- Sauvegarde complète préalable : **85 745 327 octets**, contrôlée par
  `pg_restore --list` et décodage complet sans exécution SQL. Aucun essai de
  restauration dans une autre base pour cette opération.
- Reçu, empreintes et sauvegarde conservés dans Backend, hors Git :
  `demonstrations/prive/gca-release-20261118T171323Z/migration-result.json`
  et `database.dump` voisin.
- Après migration : aucune migration restante ; empreinte conforme, clé
  primaire, deux clés étrangères, deux index valides et colonne immédiate
  non nullable avec défaut `false` vérifiés. Aucun ancien périmètre n'a été
  converti en contrôle immédiat.
- Service local de contrôle du schéma sur TEST : **READY**. Contrôles HTTP
  après migration : `/sante` **200, OK**, readiness **200, READY, 229 contrôles**
  (`.artifacts/gca/test-http-after.json` dans Backend). Le premier appel
  readiness avant migration avait expiré ; la lecture après migration réussit.
- Le backend répond encore avec `1.0.0+94d64b8` à ce contrôle : la migration
  ne prouve pas le déploiement de la fonctionnalité. Aucun parcours métier
  distant ni envoi d'invitation réelle exécuté.

La publication porte sur Projet, Backend et Animation ; le backend épingle
la révision documentaire de cette livraison pour son prochain build autonome.
Les références finales et la vérification des branches distantes sont
consignées après publication dans le reçu local Projet
`.artifacts/codex/gca/publication.json`. Les preuves fonctionnelles ci-dessus
restent celles du code testé ; les contrôles documentaires et du bundle sont
renouvelés pour la publication. Le profil workspace consolidé n'est pas
réexécuté pour cette opération ; les deux échecs Import préexistants restent
documentés. Le déploiement des applications et la recette distante restent
distincts de la migration et du push.
