# Roadmap securite et performance

## Resume executif

L'audit du backend met en evidence plusieurs risques immediats :
- des secrets et identifiants par defaut sont versionnes dans le code (`app/config.py`);
- des tokens sensibles sont exposes dans les URL, les logs applicatifs et l'interface d'administration (`app/config.py`, `app/main.py`, `app/observability_http.py`, `app/audit.py`, `app/infrastructure/admin/admin.py`);
- le back-office repose sur un login mot de passe simple sans durcissement visible (`app/infrastructure/admin/auth.py`);
- plusieurs points de performance se degradent avec la volumetrie: filtres appliques en memoire, N+1 sur les coffrets avec prestations, absence de cache headers branches alors qu'un middleware existe deja (`app/application/use_cases/lister_coffrets.py`, `app/infrastructure/persistence/repositories/repositories_sqlalchemy.py`, `app/http_cache.py`, `app/main.py`);
- le schema SQL est cree au demarrage de l'application et la connexion SQLAlchemy reste peu durcie pour la production (`app/bootstrap.py`, `app/infrastructure/persistence/db.py`).

## Echelle de criticite

- `Critique` : a traiter immediatement avant exposition publique ou nouvelle montee en charge.
- `Elevee` : a planifier dans le prochain cycle.
- `Moyenne` : a traiter apres stabilisation des urgences.

---

## Epic 1. Eliminer les secrets versionnes et les defaults dangereux

- Criticite : `Critique`
- Pourquoi : le code embarque des cles Stripe/Brevo, un secret webhook, un secret admin de session et des credentials admin par defaut dans [`app/config.py`](../../../../localeo-backend/app/config.py).
- Impact : fuite de secrets, compromission d'environnements relies, prise de controle du back-office si les valeurs par defaut restent actives.

### User Stories prioritaires

1. `P0` En tant qu'exploitant, je veux supprimer toutes les valeurs secretes codees en dur pour que l'application refuse de demarrer si un secret requis manque en environnement de production.
   - Cible : [`app/config.py`](../../../../localeo-backend/app/config.py)
   - Critere d'acceptation : aucune cle ou secret reel ne reste dans le repo; les valeurs par defaut de prod sont interdites; un mode dev explicite est necessaire pour les fallbacks locaux.

2. `P0` En tant que responsable securite, je veux faire tourner et documenter une rotation complete des secrets deja exposes afin d'invalider toute fuite deja intervenue.
   - Cible : Stripe, Brevo, session admin, webhook Stripe
   - Critere d'acceptation : secrets regeneres, anciens secrets revoques, procedure de rotation documentee.

3. `P1` En tant qu'equipe backend, je veux centraliser la validation de configuration au boot pour detecter les mauvaises valeurs avant ouverture des routes.
   - Cible : [`app/config.py`](../../../../localeo-backend/app/config.py), [`app/main.py`](../../../../localeo-backend/app/main.py)
   - Critere d'acceptation : validation stricte des secrets, URLs front, mode dev/prod, et journalisation non verbale des erreurs de config.

---

## Epic 2. Supprimer les fuites de tokens dans les URL, logs et back-office

- Criticite : `Critique`
- Pourquoi : le lien de commande inclut `management_token` en query string dans [`app/config.py`](../../../../localeo-backend/app/config.py); les middlewares et handlers journalisent `request.url.query` dans [`app/observability_http.py`](../../../../localeo-backend/app/observability_http.py) et [`app/main.py`](../../../../localeo-backend/app/main.py); l'audit log derive un acteur a partir des tokens dans [`app/audit.py`](../../../../localeo-backend/app/audit.py); l'admin permet de rechercher des `token_activation` et `qr_token` dans [`app/infrastructure/admin/admin.py`](../../../../localeo-backend/app/infrastructure/admin/admin.py).
- Impact : exfiltration de tokens via logs applicatifs, APM, reverse proxies, captures d'ecran admin ou historiques de navigation.

### User Stories prioritaires

1. `P0` En tant qu'utilisateur de l'espace commande, je veux que les tokens de gestion ne transitent plus en query string afin qu'ils ne fuient pas dans les logs et les referers.
   - Cible : [`app/config.py`](../../../../localeo-backend/app/config.py), [`app/security/management_token.py`](../../../../localeo-backend/app/security/management_token.py)
   - Critere d'acceptation : usage du header `Authorization` ou `X-Management-Token`; aucun lien frontend ne contient de secret durable en URL.

2. `P0` En tant qu'exploitant, je veux que les logs HTTP et metier masquent les query strings, tokens d'activation, tokens de management, API keys et identifiers sensibles.
   - Cible : [`app/observability_http.py`](../../../../localeo-backend/app/observability_http.py), [`app/main.py`](../../../../localeo-backend/app/main.py), [`app/audit.py`](../../../../localeo-backend/app/audit.py)
   - Critere d'acceptation : politique de redaction centralisee, tests sur endpoints `/achats`, `/emails`, `/sms`, `/reversements`.

3. `P0` En tant qu'admin, je veux que les secrets operationnels ne soient ni visibles ni recherchables dans SQLAdmin.
   - Cible : [`app/infrastructure/admin/admin.py`](../../../../localeo-backend/app/infrastructure/admin/admin.py)
   - Critere d'acceptation : suppression des colonnes et recherches sur `token_activation`, `qr_token`, `key_hash`, corps complets d'emails/SMS si non necessaires.

4. `P1` En tant que responsable conformite, je veux definir une matrice de donnees sensibles par flux de log pour empecher toute regression.
   - Critere d'acceptation : liste blanche/liste rouge documentee + tests automatises de redaction.

---

## Epic 3. Durcir l'authentification et l'exposition du back-office

- Criticite : `Elevee`
- Pourquoi : l'auth admin se limite a une comparaison directe `username/password` dans [`app/infrastructure/admin/auth.py`](../../../../localeo-backend/app/infrastructure/admin/auth.py), avec des defaults faibles dans [`app/config.py`](../../../../localeo-backend/app/config.py); le back-office est branche sans autre garde visible dans [`app/main.py`](../../../../localeo-backend/app/main.py).
- Impact : brute force, prise de controle si credentials faibles, surface d'attaque elevee sur `/admin`.

### User Stories prioritaires

1. `P1` En tant qu'exploitant, je veux imposer des credentials admin forts et uniques pour interdire les valeurs par defaut au demarrage.
   - Cible : [`app/config.py`](../../../../localeo-backend/app/config.py), [`app/infrastructure/admin/auth.py`](../../../../localeo-backend/app/infrastructure/admin/auth.py)
   - Critere d'acceptation : blocage si `admin/change-me` ou secret de session par defaut.

2. `P1` En tant qu'administrateur, je veux une authentification admin durcie avec hashage de mot de passe, limitation de tentatives et eventuellement 2FA pour reduire le risque de compromission.
   - Cible : [`app/infrastructure/admin/auth.py`](../../../../localeo-backend/app/infrastructure/admin/auth.py)
   - Critere d'acceptation : mot de passe non stocke en clair, journalisation des echecs, rate limiting par IP/compte.

3. `P1` En tant qu'architecte securite, je veux proteger `/admin`, `/docs`, `/openapi.json` et les endpoints internes par environnement ou allowlist pour reduire la surface publique.
   - Cible : [`app/main.py`](../../../../localeo-backend/app/main.py)
   - Critere d'acceptation : docs desactivees ou restreintes en prod; routes admin/internal reservees aux environnements ou reseaux autorises.

---

## Epic 4. Ajouter des controles anti-abus et des garde-fous HTTP

- Criticite : `Elevee`
- Pourquoi : aucune limitation de debit, aucun `TrustedHostMiddleware`, aucune politique CORS explicite, et aucun plafond de payload visible pour les routes publiques sensibles.
- Impact : brute force, enumeration, deni de service applicatif, exposition par mauvais `Host` ou mauvaise conf proxy.

### User Stories prioritaires

1. `P1` En tant qu'exploitant, je veux activer du rate limiting sur `/paiements/initialiser`, `/achats/*`, `/validation/*`, `/admin/login` et les batches internes pour freiner les abus.
   - Cible : routes publiques et sensibles
   - Critere d'acceptation : quotas par IP/acteur, seuils differencies et reponses explicites `429`.

2. `P1` En tant qu'infra, je veux filtrer les `Host` attendus et definir une politique proxy/CORS explicite afin d'eviter les comportements implicites.
   - Cible : [`app/main.py`](../../../../localeo-backend/app/main.py)
   - Critere d'acceptation : `TrustedHostMiddleware` ou equivalent, CORS strict uniquement si besoin, documentation des headers proxy de confiance.

3. `P2` En tant qu'equipe backend, je veux borner la taille des requetes entrantes et normaliser les timeouts amont/aval pour limiter les effets de charge anormale.
   - Cible : webhooks, uploads images, endpoints batch
   - Critere d'acceptation : limites documentees et appliquees au niveau app ou reverse proxy.

---

## Epic 5. Sortir la gestion du schema et durcir l'acces base de donnees

- Criticite : `Elevee`
- Pourquoi : le bootstrap cree les tables via `Base.metadata.create_all()` a chaque demarrage dans [`app/bootstrap.py`](../../../../localeo-backend/app/bootstrap.py), et l'engine SQLAlchemy reste configure sans options de resilience visibles dans [`app/infrastructure/persistence/db.py`](../../../../localeo-backend/app/infrastructure/persistence/db.py).
- Impact : demarrages plus lents, risque de comportements non maitrises en production, difficulte a scale horizontalement, connexions zombie ou cassees non gerees proprement.

### User Stories prioritaires

1. `P1` En tant qu'exploitant, je veux sortir la creation/migration du schema du runtime applicatif et la confier a un pipeline de migration dedie.
   - Cible : [`app/bootstrap.py`](../../../../localeo-backend/app/bootstrap.py)
   - Critere d'acceptation : plus de `create_all()` au demarrage de l'API; migrations versionnees et procedure de rollout documentee.

2. `P1` En tant qu'equipe plateforme, je veux configurer l'engine SQLAlchemy avec `pool_pre_ping`, recyclage et bornes de pool pour stabiliser l'application sous charge.
   - Cible : [`app/infrastructure/persistence/db.py`](../../../../localeo-backend/app/infrastructure/persistence/db.py)
   - Critere d'acceptation : parametres de pool externes et adaptes a l'environnement.

3. `P2` En tant qu'equipe ops, je veux mesurer les temps DB et le taux de saturation des connexions afin de dimensionner l'infrastructure de facon fiable.
   - Critere d'acceptation : metriques pool SQL + tableaux de bord de base.

---

## Epic 6. Corriger les points chauds de performance sur le catalogue

- Criticite : `Moyenne`
- Pourquoi : `ListerCoffrets` applique `type_coffret` en memoire puis declenche une requete par coffret quand `avec_prestations=true` dans [`app/application/use_cases/lister_coffrets.py`](../../../../localeo-backend/app/application/commercialisation/use_cases/lister_coffrets.py); les repositories ne poussent pas ces filtres au SQL dans [`app/infrastructure/persistence/repositories/repositories_sqlalchemy.py`](../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py).
- Impact : latence et charge DB croissantes avec la volumetrie catalogue.

### User Stories prioritaires

1. `P2` En tant qu'utilisateur catalogue, je veux que les filtres `ville_id` et `type_coffret` soient executes en SQL pour eviter le sur-traitement en memoire.
   - Cible : [`app/application/use_cases/lister_coffrets.py`](../../../../localeo-backend/app/application/commercialisation/use_cases/lister_coffrets.py), [`app/infrastructure/persistence/repositories/repositories_sqlalchemy.py`](../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py)
   - Critere d'acceptation : le repository prend `type_coffret`; le use case ne refiltre plus en Python.

2. `P2` En tant qu'utilisateur catalogue, je veux que `avec_prestations=true` utilise un chargement groupe ou prefetch pour eliminer le N+1.
   - Cible : [`app/application/use_cases/lister_coffrets.py`](../../../../localeo-backend/app/application/commercialisation/use_cases/lister_coffrets.py)
   - Critere d'acceptation : nombre de requetes borne quelle que soit la taille de la liste.

3. `P2` En tant qu'equipe produit, je veux ajouter pagination, limites maximales et tri explicite sur les listings publics pour garder des temps de reponse predictibles.
   - Cible : `/villes`, `/commercants`, `/coffrets`
   - Critere d'acceptation : `limit/offset` ou pagination curseur, bornes par defaut et max.

---

## Epic 7. Activer les optimisations HTTP deja presentes et completer l'observabilite

- Criticite : `Moyenne`
- Pourquoi : un middleware de cache existe dans [`app/http_cache.py`](../../../../localeo-backend/app/http_cache.py) mais n'est pas branche dans [`app/main.py`](../../../../localeo-backend/app/main.py); l'observabilite trace les requetes mais sans politique de cache ni indicateurs de performance applicative utiles pour arbitrer.
- Impact : trafic inutile sur le catalogue, surcout reseau, manque de donnees fiables pour prioriser les vrais hot spots.

### User Stories prioritaires

1. `P2` En tant que front public, je veux recevoir des headers de cache corrects sur les endpoints catalogue pour reduire la charge serveur.
   - Cible : [`app/http_cache.py`](../../../../localeo-backend/app/http_cache.py), [`app/main.py`](../../../../localeo-backend/app/main.py)
   - Critere d'acceptation : middleware branche, tests sur `/villes`, `/commercants`, `/coffrets`, et `no-store` sur les routes sensibles.

2. `P2` En tant qu'equipe ops, je veux instrumenter les use cases et repositories les plus critiques avec des metriques de latence et de cardinalite pour piloter les optimisations.
   - Cible : catalogue, paiement, validation, batches email/SMS
   - Critere d'acceptation : p50/p95, volume par endpoint, nombre de requetes SQL par use case.

3. `P3` En tant qu'equipe backend, je veux nettoyer les logs verbeux non actionnables et standardiser les evenements utiles pour limiter le bruit et le cout d'ingestion.
   - Critere d'acceptation : format unique, niveaux de logs coherents, suppression des messages decoratifs.

---

## Ordre de mise en oeuvre recommande

1. Epic 1
2. Epic 2
3. Epic 3
4. Epic 4
5. Epic 5
6. Epic 6
7. Epic 7

## Quick wins a lancer immediatement

- Retirer et faire tourner toutes les cles exposees.
- Supprimer la journalisation des query strings et masquer les tokens dans tous les logs.
- Interdire les credentials admin par defaut.
- Enlever l'exposition des tokens et hashes dans SQLAdmin.
- Brancher le middleware de cache sur les routes publiques.
