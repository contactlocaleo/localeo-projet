# Sprint 1 - Securite immediate

## Objet

Ce sprint vise a reduire les risques critiques identifies lors de la revue securite/performance, sans elargir le perimetre a des refactors structurants. L'objectif est de supprimer les expositions les plus dangereuses avant toute nouvelle evolution fonctionnelle ou montee en charge.

## Objectif du sprint

- eliminer les secrets versionnes et les valeurs par defaut dangereuses ;
- supprimer les fuites de tokens via les URL et les logs ;
- reduire l'exposition des secrets dans le back-office ;
- durcir le minimum vital de l'authentification admin.

## Perimetre

### Inclus

- configuration secrete et validation de configuration ;
- redaction des logs et des traces d'audit ;
- suppression des tokens en query string ;
- durcissement minimal de SQLAdmin ;
- durcissement minimal de l'auth admin.

### Exclu

- migration Alembic et retrait de `create_all()` ;
- rate limiting global ;
- optimisation SQL et pagination catalogue ;
- cache HTTP ;
- refonte complete IAM / RBAC / 2FA.

## Definition of Done du sprint

- aucun secret reel n'est present dans le code versionne ;
- aucun token durable n'est genere dans une URL publique ;
- les logs applicatifs ne journalisent plus de donnees sensibles exploitables ;
- SQLAdmin n'affiche ni ne rend recherchables les secrets operationnels ;
- les credentials admin par defaut sont refuses ;
- une checklist de rotation post-fuite est documentee.

---

## Backlog Sprint 1

### US-S1-001 - Supprimer les secrets versionnes du code

- Etat : `Completee` 
- Implementation : `app/config.py`, `app/main.py` 
- Priorite : `Critique`
- Valeur : eliminer le principal risque de compromission immediate.

#### Description

En tant qu'exploitant, je veux supprimer toutes les valeurs secretes codees en dur pour que l'application ne transporte plus de secrets reutilisables dans le repository.

#### Cibles techniques

- `app/config.py`

#### Criteres d'acceptation

- aucune cle Stripe, Brevo, webhook secret ou secret de session admin n'est codee en dur ;
- les fallbacks autorises en local ne contiennent aucune valeur sensible reutilisable ;
- les variables critiques sont chargees depuis l'environnement uniquement ;
- une erreur de configuration claire est levee si un secret requis manque en environnement non dev.

#### Notes d'implementation

- introduire une distinction explicite entre mode local/dev et mode production ;
- eviter toute valeur par defaut qui ressemble a une vraie credentielle.

---

### US-S1-002 - Bloquer les credentials et secrets admin par defaut

- Etat : `Completee` 
- Implementation : `app/config.py` 
- Priorite : `Critique`
- Valeur : empecher une prise de controle triviale du back-office.

#### Description

En tant que responsable securite, je veux interdire les credentials admin et secrets de session par defaut afin que l'interface d'administration ne puisse pas etre exposee avec une configuration faible.

#### Cibles techniques

- `app/config.py`
- `app/infrastructure/admin/auth.py`

#### Criteres d'acceptation

- le mot de passe par defaut est refuse quel que soit le nom d'utilisateur ;
- le mot de passe admin respecte `LOCALEO_PASSWORD_MIN_LENGTH` (12 par defaut) ;
- hors developpement, le secret de session admin comporte au moins 32 caracteres ;
- les secrets de session par defaut sont refuses ;
- le demarrage echoue si l'admin est active avec une configuration faible ;
- le comportement est documente pour les environnements locaux.

#### Notes d'implementation

- conserver un demarrage simple en local, mais exiger un flag explicite si des valeurs de demonstration sont tolerees.

---

### US-S1-003 - Supprimer le management token des URL

- Priorite : `Critique`
- Valeur : empecher les fuites par logs, referers et historiques navigateur.

#### Description

En tant qu'utilisateur de l'espace commande, je veux que le `management_token` ne soit plus transporte dans l'URL afin qu'il ne fuite pas dans les journaux techniques ou les outils tiers.

#### Cibles techniques

- `app/config.py`
- `app/security/management_token.py`

#### Criteres d'acceptation

- l'URL de commande ne contient plus `management_token` ;
- le token est transmis par header `Authorization` ou `X-Management-Token` ;
- un plan de compatibilite transitoire est defini si le front actuel depend encore de l'URL ;
- la documentation d'integration front est mise a jour.

#### Notes d'implementation

- prevoir une migration progressive si le frontend de production consomme deja l'ancien format.

---

### US-S1-004 - Rediger les logs HTTP et erreurs

- Priorite : `Critique`
- Valeur : eviter la fuite de secrets dans l'observabilite et les exports logs.

#### Description

En tant qu'exploitant, je veux masquer les query strings et les donnees sensibles dans les logs HTTP et les handlers d'erreur afin que les journaux ne deviennent pas une surface d'exfiltration.

#### Cibles techniques

- `app/observability_http.py`
- `app/main.py`

#### Criteres d'acceptation

- `request.url.query` n'est plus journalise brut ;
- les routes sensibles ne loggent pas de tokens, secrets, API keys ou donnees de gestion ;
- la politique de redaction est centralisee et reutilisable ;
- des tests couvrent au minimum `/achats` et `/paiements`.

#### Notes d'implementation

- preferer une fonction commune de sanitation plutot qu'une redaction dispersee.

---

### US-S1-005 - Rediger les logs d'audit et identifiants derives

- Priorite : `Critique`
- Valeur : eviter qu'un log d'audit revele une partie exploitable d'un token.

#### Description

En tant que responsable conformite, je veux que les logs d'audit n'exposent pas de derive de tokens ou d'API keys afin que les traces sensibles restent conformes et non reutilisables.

#### Cibles techniques

- `app/audit.py`

#### Criteres d'acceptation

- l'acteur derive d'un token n'expose plus de prefixe exploitable ;
- les API keys et management tokens ne sont jamais journalises en clair ni partiellement ;
- les informations d'audit restent suffisantes pour investiguer un incident sans divulgation secrete.

#### Notes d'implementation

- remplacer les prefixes de secrets par des identifiants techniques non reversibles ou des libelles de source.

---

### US-S1-006 - Retirer l'exposition des secrets dans SQLAdmin

- Etat : `Completee`
- Implementation : `app/infrastructure/admin/admin.py`

- Priorite : `Critique`
- Valeur : empecher l'exposition accidentelle des secrets par consultation back-office.

#### Description

En tant qu'administrateur, je veux que SQLAdmin n'affiche ni ne rende recherchables les tokens et hashes sensibles afin de limiter les fuites via l'interface d'administration.

#### Cibles techniques

- `app/infrastructure/admin/admin.py`

#### Criteres d'acceptation

- `token_activation`, `qr_token` et `key_hash` ne sont plus affiches ni recherchables ;
- les vues Email/SMS ne presentent que les informations necessaires a l'exploitation ;
- les colonnes sensibles restantes sont justifiees explicitement.

#### Notes d'implementation

- revoir les `column_searchable_list`, `column_details_list` et `form_columns`.

---

### US-S1-007 - Journaliser et cadrer les echecs d'authentification admin

- Etat : `Completee`
- Implementation : `app/infrastructure/admin/auth.py`

- Priorite : `Elevee`
- Valeur : preparer le durcissement ulterieur et faciliter la detection d'abus.

#### Description

En tant qu'exploitant, je veux tracer proprement les echecs de login admin et les decisions d'authentification afin d'ameliorer la detection d'attaques et le support incident.

#### Cibles techniques

- `app/infrastructure/admin/auth.py`

#### Criteres d'acceptation

- les echecs et succes d'auth admin sont journalises sans mot de passe ni secret ;
- les logs sont structurables par IP, utilisateur et horodatage ;
- le format est compatible avec un futur rate limit.

#### Notes d'implementation

- rester minimal : observabilite d'abord, throttling au sprint suivant.

---

### US-S1-008 - Documenter la rotation des secrets exposes

- Priorite : `Elevee`
- Valeur : traiter l'impact du risque deja materialise, pas seulement sa cause.

#### Description

En tant que responsable securite, je veux documenter et executer une rotation des secrets deja exposes afin de neutraliser les credentielles qui ont pu fuiter.

#### Cibles techniques

- documentation d'exploitation
- inventaire des secrets Stripe, Brevo, webhook et admin

#### Criteres d'acceptation

- la liste des secrets a faire tourner est etablie ;
- une procedure de rotation est redigee ;
- les anciens secrets sont identifies comme a revoquer ;
- la verification post-rotation est definie.

#### Notes d'implementation

- cette US peut produire un document ops plutot qu'un changement applicatif uniquement.

---

## Ordre recommande dans le sprint

1. `US-S1-001`
2. `US-S1-002`
3. `US-S1-003`
4. `US-S1-004`
5. `US-S1-005`
6. `US-S1-006`
7. `US-S1-007`
8. `US-S1-008`

## Risques du sprint

- impact front si l'espace commande depend actuellement du token en query string ;
- risque de faux positifs si la redaction des logs est trop agressive ;
- besoin de coordination ops pour la rotation reelle des secrets.

## Sorties attendues

- code durci sur la configuration, les logs et l'admin ;
- documentation de rotation des secrets ;
- base propre pour un Sprint 2 centre sur rate limiting, docs exposure, base de donnees et performance catalogue.
