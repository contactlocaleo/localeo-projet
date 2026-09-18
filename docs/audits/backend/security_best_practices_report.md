# Audit des API non publiques et du risque d'usurpation de coffret

Date : 12 septembre 2026. Base examinee : copie de travail de `localeo-backend`, HEAD `8f2c2aa`, avec modifications locales preexistantes. Revue ciblee de l'authentification, des autorisations et du parcours QR des coffrets cadeaux.

## Etat apres implementation des lots 1 et 2

Les constats ci-dessous decrivent l'audit initial du 12 septembre 2026.
Les corrections et leur recette sont detaillees dans
[la validation des lots 1 et 2](../../../releases/backend/securite-lots1-2-validation.md).
Les constats 01, 02, 04 et 06 sont corriges dans le code. Le constat 05 est
traite par transports hors URL, codes a usage unique et sessions courtes ;
la desactivation effective du suivi Brevo et la verification des journaux
amont restent des operations de deploiement. Les quotas et alertes ont ete ajoutes.
Le risque de copie d'un bon au porteur (03) et le MFA relevent du lot 3.
Aucun deploiement en production n'a ete effectue pendant cette implementation.

## Synthese historique

Le backend dispose d'un socle de protection substantiel : sessions serveur revocables, permissions, controles de rattachement commercant/prestation, signature HMAC des QR, expiration et protections contre la double consommation. Cependant, **le nom `/protected` ne garantit pas l'authentification**, une ecriture de referentiel reste publique, et **la regeneration d'un QR ne neutralise pas sa copie**.

Le principal risque pour un coffret est le vol ou la copie d'un titre au porteur, davantage que la fabrication cryptographique d'un faux QR. Le serveur authentifie le commercant ; il ne prouve pas que la personne qui lui presente le QR est le beneficiaire legitime. Un lien de consultation vole donne egalement acces au QR.

Appreciation qualitative : protection des acces presente mais heterogene ; resistance a la falsification du QR satisfaisante sous reserve d'une cle secrete forte ; resistance a la copie et capacite de revocation individuelle insuffisantes. Cette revue ne constitue pas une certification de la production.

## Perimetre et methode

- Lecture des routeurs, des middlewares, des dependances d'acces, des cas d'usage achat/consultation/validation/regeneration et des modeles associes.
- Recherche statique des routes sans controle explicite, puis verification des protections heritees du routeur et du middleware. Les endpoints de login et de reset volontairement accessibles ne sont pas classes comme failles.
- Lecture ciblee de `localeo-marketplace` et `localeo-commercant` pour verifier le transport des tokens et les usages du catalogue.
- Execution de sept verifications locales avec le vrai `ServiceQr`, le vrai cas d'usage `OuvrirTransactionValidation` et la vraie entite `TransactionValidation`. Configuration synthetique et depots en memoire ; aucun appel a une base ni a un service externe.
- Lors de la revue initiale, aucun code applicatif modifie. Rapport et script de diagnostic uniquement. Les modifications concurrentes des autres fichiers ne sont pas celles de cet audit.

La configuration effectivement deployee, le filtrage reseau, le reverse proxy, les journaux des hebergeurs et les secrets reels n'ont pas ete inspectes. Lors de la revue initiale, la suite pytest et les tests HTTP/PostgreSQL existants n'avaient pas ete executes : l'interpreteur accessible ne dispose pas des dependances du projet. Les parcours Animation et ERP ont fait l'objet d'une revue des points d'entree et des mecanismes communs, pas d'une preuve exhaustive de toutes leurs autorisations metier.

## Protections existantes

| Surface | Controles observes | Limite principale |
|---|---|---|
| `/internal/*`, administration | Session admin signee et registre serveur de revocation ; restriction ADMIN ou perimetre ERP ; CSRF | L'acces reseau prive et un eventuel MFA externe ne sont pas verifies |
| API commercant sensibles | Bearer hache, expiration, revocation, scopes et statut commercant recontroles | Le token reste un secret au porteur ; trois routes catalogue echappent a l'authentification |
| API Animation | Session revocable, gestionnaire et partenaire actifs, habilitations actives et permission par commune | Couverture metier complete des endpoints non demontree par cet audit |
| API batch/finance | `X-API-KEY` hachee, comparaison constante, cle active, scope strict | Pas d'expiration native des cles ; permissions batch assez larges |
| Consultation achat/coffret | Token aleatoire, hachage, rattachement a la ressource, expiration et revocation | La consultation du coffret permet aussi de recuperer son QR |
| Validation d'une prestation | Session commercant, transaction de 60 s par defaut, rattachements verifies, controles de consommation | La transaction courte peut etre recreee avec le meme QR durable |
| Documentation | OpenAPI et Swagger non publics soumis a la session admin | Ne remplace pas la protection des routes elles-memes |

Preuves : `app/main.py:345`, `app/main.py:379`, `app/security/admin_session.py:11`, `app/security/erp.py:7`, `app/security/erp.py:27`, `app/security/http.py:113`, `app/application/identite_acces/use_cases/verifier_session_commercant.py:22`, `app/application/identite_acces/use_cases/verifier_session_animation.py:13`, `app/security/api_keys.py:29`.

Le registre admin applique 15 minutes d'inactivite et 8 heures de duree absolue (`app/domaine/identite_acces/services/politique_session_admin.py:3`). La validation verifie bien le commercant et le coffret de la prestation (`app/application/exploitation/use_cases/valider_prestation.py:47`). Le service de consommation utilise un verrou sur l'instance et une mise a jour conditionnelle du droit (`app/application/exploitation/services/service_validation_prestation.py:53`, `:100`). Cela protege contre des doubles effets ; cela ne determine pas lequel de deux porteurs d'une copie est legitime.

## Constats de severite elevee

### 01 - La regeneration du QR ne revoque pas l'ancien

**Nature : defaut confirme par lecture et reproduction locale. Priorite P1.** Regle : autorisation de transaction et revocation d'un titre compromis.

Preuves :

- `app/infrastructure/securite/service_qr.py:53` signe uniquement `typ`, `aid`, `exp`, `kid`. Aucun identifiant aleatoire d'emission ou numero de version.
- `app/application/gestion_achats/use_cases/regenerer_qr_coffret_instance.py:69` renouvelle le token de consultation, puis `:74` regenere le QR avec le meme identifiant et la meme expiration.
- `app/application/exploitation/use_cases/ouvrir_transaction_validation.py:21` verifie la signature puis charge l'instance. Aucun controle d'egalite avec `instance.qr_token`, de version courante ou de revocation QR.

**Impact : apres signalement d'un QR vole, l'action de regeneration ne neutralise pas la copie et peut donner une fausse impression de securite.** A cle et expiration identiques, le nouveau QR est strictement identique. Meme si un autre QR est enregistre, l'ancien est encore accepte tant que sa signature et son expiration sont valides. Retirer globalement une cle du trousseau affecterait tous les coffrets qui en dependent.

Correction : ajouter une version QR ou un identifiant d'emission aleatoire par instance, le verifier contre l'etat serveur et l'incrementer a chaque regeneration/revocation. Lier aussi les transactions ouvertes a cette version et la recontroler lors de la consommation, afin de bloquer celles ouvertes avant la revocation. Effectuer rotation et invalidation dans une transaction atomique.

Mesure transitoire : en cas de fuite averee, bloquer la consommation du coffret via le parcours metier approprie et traiter sa reemission. Ne pas annoncer qu'une simple regeneration actuelle invalide la copie. Prevoir explicitement la migration des QR historiques : les accepter sans controle de version annulerait le benefice.

Limite de preuve : l'acceptation a l'ouverture a ete reproduite avec un depot factice. Les controles ulterieurs de statut/expiration/prestation restent applicables ; un coffret annule n'est pas declare consommable par cet audit.

### 02 - Creation de types de coffrets sans authentification

**Nature : defaut confirme statiquement. Priorite P1.** Regle : FASTAPI-AUTH-001 / autorisation des fonctions d'administration.

Route : `POST /public/commercialisation/types-coffrets`.

Preuves : `app/main.py:411` monte ce routeur sous `/public` ; `app/api/types_coffrets_api.py:10` et `:19` ne declarent aucune dependance de securite ; `creer_type()` appelle directement `CreerTypeCoffret.execute()`. Ce dernier ajoute le referentiel et effectue `uow.commit()` (`app/application/commercialisation/use_cases/creer_type_coffret.py:39`). Le middleware interne ne couvre pas cette route.

Impact : un appelant anonyme peut ajouter des types au referentiel, polluer le catalogue et provoquer des ecritures repetitives. Le cas d'usage impose une marge nulle : aucune modification arbitraire des commissions existantes n'est deduite.

Correction : reserver l'ecriture a une route interne avec role adapte et protection CSRF pour la session admin. Conserver la lecture publique. Refuser l'ancien POST public et verifier les consommateurs avant retrait.

Verification restante : confirmer en preproduction le refus anonyme et le succes autorise. Aucun POST n'a ete envoye a la production. Un filtrage amont eventuel pourrait reduire l'exposition effective ; il ne figure pas dans le code examine.

### 03 - Un QR copie reste un titre au porteur utilisable

**Nature : risque architectural confirme, distinct du defaut de regeneration. Priorite P1 pour un objectif anti-usurpation fort.**

Preuves : `app/api/validation_api.py:44` exige la session du commercant et le QR, sans preuve du beneficiaire. `app/application/exploitation/use_cases/ouvrir_transaction_validation.py:36` cree une nouvelle transaction a chaque presentation. `app/config.py:373` fixe sa duree par defaut a 60 s. `app/api/coffret_instances_api.py:129` et `app/application/gestion_achats/use_cases/consulter_detail_qr_coffret_instance_par_token.py:12` autorisent la recuperation du QR avec le token de consultation.

Scenario : une capture d'ecran, un email transfere ou un lien de consultation vole permet de presenter le vrai QR a un commercant legitime avant le beneficiaire. Le commercant n'a pas besoin d'etre complice. Un commercant malveillant qui a scanne le QR peut aussi conserver sa copie ; les controles existants limitent sa consommation a ses propres prestations.

La signature empeche de modifier l'identifiant ou l'expiration sans connaitre la cle. Elle ne distingue pas deux copies identiques. L'idempotence empeche plusieurs debits du meme droit ; elle n'empeche pas que le premier debit soit frauduleux. L'ouverture de plusieurs transactions n'est pas en soi une faille pour un coffret multi-prestations : le risque est l'absence de preuve fraiche du beneficiaire.

Correction cible : separer le droit de consulter du droit d'autoriser une consommation. Exiger une confirmation du beneficiaire liee au coffret, au commercant et a la prestation ; generer un jeton court, a usage unique et controle cote serveur. Un QR dynamique emis sur simple presentation du meme lien durable vole ne resout pas entierement le probleme : la delivrance du jeton doit elle-meme demander une preuve appropriee.

Si le produit doit rester un bon papier transmissible sans verification du beneficiaire, une partie du risque de copie est inherente a ce choix. Le gerer explicitement par revocation, code secret separe et controle renforce selon le risque.

## Constats de severite moyenne

### 04 - Routes `/protected` anonymes exposant les contacts commercants

**Nature : exposition confirmee statiquement ; caractere prive des coordonnees a confirmer fonctionnellement. Priorite P1/P2 selon les donnees.** Regles : FASTAPI-AUTH-001 et FASTAPI-RESP-001.

Routes GET : `/protected/referencement/commercants`, `/protected/referencement/commercants/page`, `/protected/referencement/commercants/{commercant_id}`.

Preuves : `app/api/commercants_api.py:82`, `:86`, `:99`, `:347` ; montage sans dependance globale dans `app/main.py:451`. La projection inclut nom, prenom, email et telephone du contact principal (`app/api/schemas.py:77`, `app/application/referencement/use_cases/lister_commercants.py:29`, `app/application/referencement/use_cases/consulter_detail_commercant.py:36`).

Impact : collecte anonyme des coordonnees des commercants actifs et facilitation du phishing ou de l'usurpation lors d'un appel support. Les commercants non actifs sont deja filtres ; aucune exposition de mots de passe n'est constatee.

Nuance essentielle : la marketplace utilise volontairement ces routes pour son catalogue (`../localeo-marketplace/src/services/api.js:450`). L'absence d'authentification du catalogue a donc une raison fonctionnelle. L'anomalie est la confusion de contrat et, si ces champs sont operationnels, leur publication avec le catalogue.

Correction : creer une projection publique minimale sous `/public`, avec uniquement les contacts explicitement destines au public ; conserver les coordonnees operationnelles derriere une autorisation. Adapter la marketplace dans le meme lot. Ne pas simplement ajouter une authentification a la route actuelle, ce qui casserait la navigation publique.

### 05 - Secrets durables encore transportes dans des URL

**Nature : surfaces de fuite confirmees ; aucune fuite reelle demontree. Priorite P2, liee aux constats 01 et 03.** Regle : FASTAPI-AUTH-002.

Preuves :

- `app/config.py:274` genere par defaut un lien avec `?consultation_token=...`.
- `app/security/consultation_token.py:20` donne a ce token une validite jusqu'a l'expiration du coffret plus 30 jours par defaut (`app/config.py:329`).
- `app/api/validation_api.py:46` accepte encore le QR en query string, bien que ce transport soit marque obsolete.
- `app/api/qr_api.py:54` accepte le QR dans `?token=...` pour l'image PNG.

Impact : le lien initial ou les appels historiques peuvent exposer un secret aux journaux HTTP de l'hebergement, aux outils de suivi ou a une copie du lien. Le vol du token de consultation permet la recuperation du QR pendant sa validite.

Protections presentes : la marketplace retire les secrets de l'adresse apres lecture (`../localeo-marketplace/src/pages/CoffretInstancePage.jsx:399`, `../localeo-marketplace/src/services/sensitiveUrl.js:18`) et sert `Referrer-Policy: no-referrer` (`../localeo-marketplace/server.cjs:54`). Cela reduit les fuites ulterieures, sans effacer la requete initiale deja recue par le serveur. Le frontend commercant envoie deja le QR dans le JSON (`../localeo-commercant/src/appSupport.jsx:445`).

Correction : supprimer le fallback query du scan apres verification des anciens clients ; rendre les images via corps/header ou generation locale. Pour les liens email, preferer un code d'echange court et utilisable une fois, transmis en fragment puis echange par POST. Une simple migration du secret durable vers le fragment reduit les fuites HTTP, mais ne remplace ni expiration courte ni revocation. Desactiver les suivis de clics sur ces liens et verifier la redaction aux differents niveaux d'hebergement.

### 06 - La politique `no-store` manque les vraies routes achat/coffret

**Nature : defaut de correspondance de chemin confirme statiquement. Priorite P2.** Regle : protection des reponses sensibles.

Preuve : `app/security/http.py:163` teste `path.startswith(("/gestion-achats/", "/admin", "/internal"))`. Or les routes achat/coffret sont montees sous `/protected/gestion-achats/` et le QR public sous `/public/gestion-achats/` (`app/main.py:426`, `:461`, `:462`). Les reponses des handlers de consultation examines n'ajoutent pas elles-memes `no-store`. Le PNG impose meme `Cache-Control: private, max-age=3600` (`app/api/qr_api.py:84`).

Impact : la protection explicite contre la conservation locale des QR et donnees personnelles n'est pas appliquee comme prevu. Cela ne prouve pas qu'un CDN partage deja ces donnees : un navigateur et un cache partage ont des regles differentes, et le header Authorization limite deja certains caches partages.

Correction : appliquer `Cache-Control: no-store` aux vrais chemins de consultation, de QR et d'emission de tokens ; conserver le cache des seuls contenus publics non sensibles. Ajouter un test HTTP sur les routes reelles, et pas uniquement sur le middleware a la racine.

## Renforcements complementaires

| Priorite | Mesure | Preuve / raison |
|---|---|---|
| P1 | MFA pour l'administration, idealement passkey/SSO, et identites nominatives | `app/infrastructure/admin/auth.py:94` accepte le couple global username/password sans second facteur applicatif. Roles et communes proviennent de la configuration. Un MFA amont reste a verifier. |
| P1 | Valider les cles QR au demarrage | `app/config.py:603` verifie la presence, pas la robustesse. Refuser les valeurs de demonstration et les secrets faibles ; generer au moins 32 octets aleatoires. Aucun secret de production n'a ete examine. |
| P2 | Limiter scans, ouvertures de transactions et echecs par commercant, instance et IP | Pas de quota visible dans `app/api/validation_api.py:44` ni dans le cas d'usage d'ouverture. Le rate limit d'authentification existe, mais ne couvre pas tous ces appels. Ajouter detection et alertes sur usages incompatibles ou repetitifs. |
| P2 | Ajouter expiration et rotation des cles API ; une cle par integration | `app/infrastructure/persistence/models.py:1325` ne contient pas d'expiration ; `app/security/api_keys.py:48` controle active/scope. Scinder `internal:batch` si les integrations n'ont besoin que de quelques actions. |
| P2 | Restreindre l'exposition de l'administration et des integrations | Verifier l'acces prive/VPN ou une passerelle d'identite pour admin ; allowlist ou mTLS selon les integrations serveur. Les navigateurs commercants et clients ont besoin d'API joignables avec authentification applicative. CORS et le prefixe de route ne sont pas un pare-feu. |
| P2 | Durcir le secours telephonique | Le `verification_code` sert a retrouver le coffret ; ce n'est pas une preuve du beneficiaire. Il est affiche avec le QR (`app/application/gestion_achats/use_cases/consulter_detail_qr_coffret_instance.py:39`). Imposer un rappel au numero deja reference et, selon le risque, une confirmation du beneficiaire. La procedure actuelle se fonde en partie sur des informations de contact connues (`docs/ops/exploitation/valider-prestation-mode-secours.md:40`). |

Le MFA pour les acces sensibles est coherent avec les recommandations [OWASP sur l'authentification multifacteur](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html). Le controle par endpoint, la protection des secrets en transit et la limitation des abus sont egalement recommandes dans [OWASP REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html).

## Parcours anti-usurpation recommande

1. Le beneficiaire active/reclame son coffret avec un lien a usage unique et une verification du canal deja enregistre. Le transfert d'un cadeau doit faire l'objet d'un parcours explicite qui revoque les anciens droits.
2. Chez le commercant, le scan identifie le coffret et la prestation ; une transaction en attente est liee au commercant connecte, au droit a consommer et a la version courante du coffret.
3. Le beneficiaire confirme sur son appareil le commercant et la prestation. Selon le niveau de risque, utiliser une session beneficiaire recente, une passkey ou un code envoye au canal verifie. Un code ne doit pas etre envoye a une adresse fournie par le demandeur de la consommation.
4. Le serveur delivre ou valide une autorisation a usage unique, de courte duree, par exemple 60 a 120 secondes. La consommer atomiquement avec le droit et le mouvement financier. Une capture ancienne doit etre inutilisable ; deux demandes simultanees ne doivent produire qu'un seul effet.
5. En cas de perte, revoquer le lien, la version QR et les transactions en attente. Notifier le beneficiaire apres consommation et fournir un moyen rapide de signaler une operation inconnue.

Le lien de consultation seul ne doit pas permettre d'approuver ce parcours. Le QR dynamique ne doit pas pouvoir etre continuellement renouvelle par le voleur du lien initial. Un code secret imprime a cote du QR ne constitue pas une verification independante. Meme un jeton court et unique reste expose a un relais en temps reel : la confirmation visible du commercant et de la prestation reduit ce risque.

Ce parcours adapte aux coffrets les principes d'autorisation liee a l'operation, a duree limitee et a usage unique exposes par [OWASP Transaction Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html). Les durees proposees et le choix du second canal sont des recommandations de conception pour Localeo, pas des exigences normatives.

## Ordre d'execution et validation

Premier lot : fermer le POST public de referentiel ; rendre la revocation/regeneration QR effective, y compris sur les transactions deja ouvertes ; ajouter des tests de refus anonyme et d'ancien QR. Deuxieme lot : separer les projections publiques/privees du catalogue, corriger les transports URL et `no-store`, ajouter quotas et alertes. Troisieme lot : faire evoluer ensemble backend, marketplace et application commercant vers l'autorisation du beneficiaire et le MFA admin.

Tests a exiger lors des corrections : ancien QR refuse apres rotation ; transaction ouverte avant rotation refusee ; mauvais commercant/prestation refuse ; token de consultation insuffisant pour consommer ; confirmation expiree ou deja consommee refusee ; deux validations concurrentes sans double effet ; parcours cadeau/papier/secours conserves avec garanties explicites ; refus anonyme des fonctions internes ; catalogue public depourvu de contacts operationnels.

Le diagnostic initial comportait sept verifications, dont quatre reproduisaient
volontairement les faiblesses. Ce resultat historique ne signifiait pas sept
controles de securite reussis. Apres correction, le script
[output/security/reproduce_coffret_auth.py](../../../../localeo-backend/output/security/reproduce_coffret_auth.py)
lance les tests de regression securises, avec le runner isole du projet.
Commande : `python output/security/reproduce_coffret_auth.py`, depuis un
interpreteur disposant des dependances de `requirements.txt`.

Le diagnostic initial ne prouvait pas une consommation frauduleuse en production.
Les nouveaux tests HTTP et PostgreSQL verifient les refus, la revocation,
l'usage unique et la concurrence. Le bilan detaille distingue tests executes,
tests ignores et activation en production. Aucune donnee reelle ni aucun secret
n'est inclus dans les livrables.
