# Clés d’accès dans Localeo Pro

Spécification du 24 novembre 2026. Le [backlog de l’EPIC 83](../../roadmap/en-cours/epic-83-cles-acces-localeo-pro-backlog.md) porte le périmètre produit. Les clés d’accès s’appuient sur le parcours de l’[EPIC 10](../../roadmap/terminees/epic-10-authentification-commercant-login-password-backlog.md) et les accès salariés de l’[EPIC 72](../epic-72-acces-salaries/README.md). La [roadmap commune](../../roadmap/README.md) porte les états produit.

Les titulaires et les salariés peuvent ajouter une clé d’accès personnelle et se reconnecter sans saisir leur email ni leur mot de passe. L’appareil ou le gestionnaire de clés présente le moyen de confirmation disponible. La connexion par mot de passe et la récupération par email restent proposées. Le backend ouvre la session Pro habituelle et applique les droits actuels du compte.

Le login actuel `POST /protected/identite-acces/commercants/auth/login` sert les deux rôles. La PWA applique le même traitement de session et dirige les salariés vers le scanner. Pour les titulaires en préparation, les droits du portail restent établis à partir du statut du commerce et du périmètre courant. Le lot concerne Pro, le domaine Identité et accès du backend et l’administration de la bascule dans Ops.

## Parcours

- **Se connecter avec une clé d’accès** apparaît avant le formulaire lorsque la fonctionnalité est active et que le navigateur prend WebAuthn en charge. Le texte explique le bénéfice et la confirmation par le visage, l’empreinte ou le code de l’appareil. L’annulation, l’expiration et l’erreur laissent le formulaire utilisable.
- Après une connexion par mot de passe, proposer la création quand le compte n’a aucune clé et que le navigateur est compatible. Le titulaire voit l’invitation à l’accueil ou en préparation et le salarié près de l’entrée du scanner. L’invitation se présente sans prise de focus. **Plus tard** la masque pour ce compte dans le navigateur. Le menu du compte donne accès à **Mes clés d’accès**.
- Sur la page de gestion, **Créer ma clé d’accès** explique la confirmation attendue et recommande un appareil ou un gestionnaire que la personne contrôle. La connexion par mot de passe datant de moins de cinq minutes suffit. Sinon, la page demande le mot de passe actuel. L’écran de réussite indique le bouton à choisir à la prochaine connexion et propose le retour à l’activité.
- Chacun gère ses propres clés, identifiées par leur nom et leur date d’ajout. Le retrait demande le mot de passe actuel et ferme les sessions ouvertes avec cette clé. La réinitialisation du mot de passe par email retire toutes les clés et ferme les sessions du compte concerné. Une modification ordinaire du mot de passe et une réinitialisation par email restent deux actions distinctes.
- L’interface donne la priorité au résultat serveur. Un retour incertain après création ou retrait mène à une relecture de **Mes clés d’accès** avant toute nouvelle tentative. Lorsque la page de gestion est ouverte depuis le portail salarié, le retour mène au scanner ou à l’historique selon le chemin d’origine. Les protections mobiles, clavier, en-tête et maintien du focus s’appliquent aussi à la page Ops.

## Invariants et contrat

Le domaine **Identité et accès** borne l’usage à l’identité propriétaire et à l’état courant du compte. Le propriétaire d’une clé est l’identifiant stable du titulaire ou l’accès salarié, y compris si l’adresse de connexion change. Le domaine porte la transition de l’état Pro, la liaison des challenges à leur génération et la validité des sessions ouvertes par clé. L’application orchestre les vérifications et les transactions avec les ports de persistance et de cryptographie. La bibliothèque WebAuthn vérifie la preuve cryptographique dans l’adaptateur.

La vérification de session et le calcul des droits réutilisent les règles de Pro. Le titulaire conserve ses destinations habituelles, le salarié retrouve son scanner et les accès salariés existants. Une session support ne peut pas gérer les clés. Le parcours salarié reste soumis au compte actif, au statut du commerce, à l’option salariés et aux versions de sécurité déjà utilisées. La connexion par clé n’établit aucune vérification du mot de passe pour les opérations PIN.

L’inscription exige une clé découvrable et une vérification de l’utilisateur. Le backend contrôle l’origine exacte, le RP ID, la signature et la vérification utilisateur. Un challenge à usage unique expire dès que cinq minutes se sont écoulées. Présenter un challenge d’inscription depuis une autre session, même du même compte, est refusé. La session d’origine garde son challenge jusqu’à son utilisation, son expiration ou son invalidation. L’assertion de connexion doit correspondre à la clé et au handle opaque de son propriétaire. Le contrôle final sous verrou tient compte du droit courant, de la révocation et de la désactivation concurrentes. La consommation du challenge et l’émission d’une session sont atomiques. La vérification du mot de passe courant pour inscrire ou retirer une clé est limitée séparément. Les refus de connexion restent génériques et les limites de tentative WebAuthn sont distinctes de celles du mot de passe. Les réponses de gestion se limitent aux champs nécessaires à l’interface.

Le retrait et la réinitialisation par email ferment les sessions concernées dans la même transaction que la révocation des clés. Une réinitialisation du titulaire cible le titulaire. Une réinitialisation salariée cible cet accès salarié. Une inscription engagée dans une session fermée par cette opération ne peut plus être finalisée. Le traitement du verrouillage du mot de passe du titulaire suit le [parcours EPIC 10](../identite-acces/authentification-commercant.md). Le statut du commerce et l’éligibilité des salariés continuent d’être contrôlés à la connexion. Les événements journalisent la décision, l’acteur, l’heure et le résultat, avec les identifiants internes nécessaires, sans mot de passe, challenge, signature ou jeton.

Le backend produit l’[OpenAPI canonique](../epic-41-api/openapi.json), et Pro exporte les opérations WebAuthn dans son contrat embarqué. Les routes de session mot de passe conservent leur contrat. Un ancien frontend continue à offrir ce mode de connexion après migration du backend. Un nouveau frontend considère la fonctionnalité indisponible si la lecture publique échoue, notamment en HTTP 404 sur un backend antérieur ou HTTP 503 en cas d’indisponibilité. Le formulaire mot de passe reste accessible. Les réponses WebAuthn et les réponses d’état utilisent `Cache-Control: no-store`.

| Accès | Routes sous `/identite-acces/commercants/auth/passkeys` | Résultat |
| --- | --- | --- |
| `/public` | `GET /etat` | `{enabled, origin}`. La PWA vérifie aussi que l’origine configurée correspond à celle du navigateur. |
| `/public` | `POST /connexion/options` | Requête `{}`, réponse `{challenge_id, options}` sans compte demandé. |
| `/public` | `POST /connexion/verifier` | Requête `{challenge_id, credential}`, réponse `InitialiserSessionCommercantPayload` identique au login par mot de passe pour ce rôle, dont `commercant.id`, l’acteur et la projection des droits. |
| `/protected`, session personnelle | `GET` sur la collection | `{keys}`, chaque entrée contient `{id, name, created_at}`. |
| `/protected`, session personnelle | `POST /inscription/options` | Requête `{password?}`, réponse `{challenge_id, options}`. |
| `/protected`, session personnelle | `POST /inscription/verifier` | Requête `{challenge_id, credential, name?}`, réponse `{id, name, created_at}`. |
| `/protected`, session personnelle | `POST /{id}/retirer` | Requête `{password}`, réponse `{revoked_current_session}`. |

La session personnelle absente ou expirée et la preuve WebAuthn refusée donnent un HTTP 401. Le code `PASSKEY_VERIFICATION_FAILED` distingue un challenge expiré ou une preuve refusée d’une session invalide. Le formulaire d’inscription garde la session dans le premier cas. Le mot de passe à demander (`PASSWORD_REQUIRED`) ou refusé (`PASSWORD_INVALID`) donne un HTTP 403. Une clé tierce et une clé inconnue donnent le même HTTP 404. Une fonctionnalité indisponible donne un HTTP 503 (`PASSKEY_UNAVAILABLE`). Une limite de tentatives atteinte donne un HTTP 429 avec `Retry-After`.

Les commandes Ops sous `/internal/ops/passkeys` exigent une session administrateur et la protection CSRF. La commande `POST` reçoit `{enabled, version}`. Un conflit donne un HTTP 409. La bascule et son audit sont validés ensemble. Après un conflit ou un résultat réseau incertain, relire l’état effectif avant toute nouvelle confirmation.

## État d’exploitation

La migration additive conserve les comptes et sessions existants et initialise l’état à **Désactivé**. Le réglage persistant PostgreSQL est indépendant par environnement. Les challenges et les sessions ouvertes par clé sont rattachés à une génération de l’état. Désactiver invalide les challenges en cours et révoque en base les sessions ouvertes par clé. Les API Pro protégées refusent ces sessions à leur prochaine requête sur n’importe quelle instance. Les sessions par mot de passe restent valides. Les clés enregistrées restent disponibles pour un retrait par mot de passe. Une réactivation permet de les réutiliser lors d’une nouvelle connexion et ne rouvre aucune ancienne session, y compris après un redémarrage du backend.

Le contrôle transactionnel de validation relit la session sous verrou et applique la même règle WebAuthn que le contrôle HTTP. Il refuse une session d’une génération obsolète ou une origine devenue indisponible, même si la session ne porte pas encore de date de révocation. La validation et la bascule Ops se départagent sur la ligne de session. Le retrait d’une clé prend la garde partagée sur l’état avant de verrouiller les sessions, y compris lorsque la connexion par clé est arrêtée.

Le contrôle de disponibilité couvre le schéma et l’origine configurée. Pro relit l’état à l’entrée et au retour visible de l’application. Une bascule n’a besoin ni d’une variable de build ni d’un déploiement. La [procédure d’exploitation](../../exploitation/exploitation/localeo-ops.md#authentification-localeo-pro) fixe les valeurs cibles, l’ordre configuration → migration → backend → Pro et les contrôles d’activation et d’arrêt.

## Données et coût

Conserver les clés publiques et leur compteur dans une collection bornée à dix clés par compte, triée par date et identifiant. La création est sérialisée par identité. Indexer l’identifiant de credential, le propriétaire et l’expiration des challenges. Purger les challenges expirés par lots. Les recherches d’état et d’assertion ont une cardinalité fixe. Contrôler la génération sur le chemin des sessions ouvertes par clé et mesurer le coût des vérifications et de la concurrence avec la bascule sur données synthétiques N/10N avant l’activation. Le générateur fournit les comptes de test. Les clés de recette sont créées dans le navigateur de test.

## Critères et preuves attendues

| Critère | Preuve attendue | Impact associé |
| --- | --- | --- |
| CL-01 · Découverte et création | Parcours du titulaire et du salarié, activation récente ou saisie du mot de passe, report et retour à l’activité | Guide Commerçant illustré, gestion des clés et invitations |
| CL-02 · Connexion et droits | Clé découvrable, compte correct, accès scanner salarié, préparation titulaire et PIN toujours soumis au mot de passe | API Pro, tests de session et d’autorisation |
| CL-03 · Refus et récupération | Origine incorrecte, challenge expiré ou rejoué en parallèle, retrait, réinitialisation ciblée, inscription présentée depuis une autre session et compte révoqué pendant le flux | Migration, tests PostgreSQL et contrats |
| CL-04 · Bascule d’exploitation | Inscription et connexion refusées pendant l’arrêt, challenges précédents invalidés, retrait par mot de passe disponible et ancienne session par clé refusée par les API et la validation métier après réactivation. Chaque cible a son propre état. | Tests de domaine et PostgreSQL, contrôle rôle et CSRF, configuration Render et recette du domaine servi |
| CL-05 · Appareils | Authentificateur virtuel Playwright, puis navigateur et PWA sur iPhone Safari et Android Chrome, annulation et indisponibilité | Comptes de test, captures et guide Pro |
| CL-06 · Compatibilité de livraison | Backend livré en premier avec état désactivé. Ancien Pro fonctionnel et nouveau Pro utilisable en cas d’état indisponible | Contrats canonique et embarqué, sauvegarde et procédure Ops |

### Preuves locales

Le 25 novembre 2026, la recette ciblée a réussi 24 tests backend, dont neuf sur PostgreSQL jetable, 142 tests de contrat frontend et sept scénarios Chromium. Les 791 contrôles backend d’architecture et de session ont également réussi.

- Le [test PostgreSQL](../../../../localeo-backend/tests/security/test_passkeys_pro_postgres.py) installe la migration sur une base jetable. Il couvre la création et la connexion avec une preuve cryptographique, la concurrence sur un même challenge, l’expiration à cinq minutes, le refus d’une inscription depuis une autre session, la bascule, le contrôle transactionnel de validation, le retrait à l’arrêt et les réinitialisations par rôle.
- La [recette Pro](../../../../localeo-commercant/tests/e2e/passkeys.spec.js) couvre Chromium, l’authentificateur virtuel et le retour au mot de passe, y compris en HTTP 404 et 503 sur la lecture de l’état. Les [contrats consommateurs](../../../../localeo-commercant/src/features/passkeys/contract.test.js) contrôlent les sept échanges. Les [tests Ops](../../../../localeo-backend/tests/api/test_ops_passkeys_api.py) vérifient l’accès administrateur, le CSRF et le traitement HTTP.
- Sur PostgreSQL 18 local, les plans d’exécution utilisent les index attendus pour la liste et la purge à 1 000 et 10 000 entrées synthétiques. Ils lisent dix clés et verrouillent quatre challenges expirés au maximum par requête de création. La latence de bout en bout sous charge et la contention sur une cible de livraison restent à mesurer.
- Le [guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md) couvre l’activation, la connexion et le retrait. Il a été rendu depuis les captures Chromium sur données synthétiques, puis vérifié dans le build. Le guide Animation couvre une identité et une connexion indépendantes.

La recette sur appareils iPhone et Android et la bascule sur TEST, DEMO et PROD sont à réaliser sur les cibles avant leur activation utilisateur.
