# Backlog Epic 5 - Session commercant securisee par QR code

## Perimetre

Epic source : `Epic 5. Session commercant securisee par QR code`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : verifier le QR code commercant a l'ouverture de l'application commercant, emettre une session commercant a duree de vie limitee et reutiliser ce ticket pour proteger les actions commercant sensibles.

## Statut global

- Epic 5 : `Abandonne` ; classement clarifie le 15 septembre 2026.
- Avancement : cadrage annule ; ne pas implementer les modeles, use cases, repositories et APIs dedies au `qr_commercant`.

Note produit : le concept de `qr_commercant` est abandonne et ne doit pas etre implemente comme mecanisme d'authentification. Le modele de session commercant reste conserve, mais l'authentification initiale est portee par le login / mot de passe de l'Epic 10. Le QR coffret client reste hors perimetre de ce remplacement.

Comme l'application est encore en phase de developpement et qu'il n'existe pas de commercants actifs, aucune procedure de migration QR commercant vers login / mot de passe n'est prevue.

Le reste de ce document est conserve comme trace de cadrage precedente et ne constitue plus une cible d'implementation.

## Regles de gestion consolidees

- Le QR commercant est verifie par un use case dedie.
- Seul un QR de type `carte_commercant` valide et rattache a une carte active permet d'ouvrir une session commercant.
- Une session commercant possede un identifiant, une date de creation, une date d'expiration, un TTL explicite et des scopes autorises.
- Toute action commercant protegee doit verifier le ticket de session et le scope requis avant execution.
- Si la session a expire, le systeme leve une exception metier `Session expiree`.
- Si la session est absente, inconnue, mal formee, revoquee ou incoherente, le systeme leve une exception metier `Session invalide`.
- Le ticket de session commercant est reutilisable pour les actions commercant sensibles de la fenetre de validite.
- Chaque API commercant securisee doit etre associee a un scope dedie.
- La session commercant ne remplace pas la transaction de validation metier.
- La transaction de validation reste necessaire pour encadrer le scan d'un QR coffret client et la consommation d'une prestation precise.
- Une transaction de validation doit etre ouverte par un commercant deja authentifie via une session valide et portant le scope adequat.

## Flux cible recommande

1. Le commercant scanne son `qr_commercant`.
2. Le backend verifie le QR et initialise une `session_commercant`.
3. Le client commercant utilise le `session_token` pour appeler les APIs commercant protegees.
4. Lorsqu'un client presente son QR coffret, le commercant authentifie ouvre une `transaction_validation`.
5. La validation effective d'une prestation exige :
   - une `session_commercant` valide ;
   - le scope adequat ;
   - une `transaction_validation` valide et non expiree ;
   - une prestation rattachée au commercant et a la coffret instance de la transaction.

## Impacts sur les APIs existantes

- L'ouverture de session commercant devient une nouvelle surface dediee, distincte de la validation de prestation.
- `ouvrir_transaction_validation` doit devenir une API protegee par session commercant.
- `valider_prestation` doit evoluer pour s'appuyer sur la session commercant et la transaction de validation.
- A terme, le QR commercant ne doit plus etre necessaire sur chaque appel de validation de prestation : il sert a ouvrir la session, pas a authentifier chaque requete.

## Perimetre V1 des APIs securisees

- `POST /commercant/session/ouvrir`
  - role : verifier le `qr_commercant` et ouvrir une session commercant
  - scope requis : aucun, car point d'entree d'authentification
- `POST /validation/ouvrir-transaction`
  - role : ouvrir une transaction de validation apres scan du QR coffret client
  - scope requis : `commercant:validation`
- `POST /validation/valider-prestation`
  - role : valider effectivement une prestation dans une transaction ouverte
  - scope requis : `commercant:validation`
- `GET /reversements/commercant`
  - role : consulter les reversements a venir et le detail des reversements deja effectues
  - scope requis : `commercant:reversement`
- `GET /commercant/me`
  - role : consulter le profil et les informations de session du commercant courant
  - scope requis : `commercant:profil`
- `PATCH /prestations/{prestation_id}/contenu`
  - role : modifier le contenu editable d'une prestation commercant
  - champs autorises : `libelle`, `description`
  - champs explicitement exclus : `prix`
  - scope requis : `commercant:prestation`

## Contraintes sur la transaction de validation

- La `transaction_validation` doit etre liee au commercant authentifie qui l'a ouverte.
- Le modele de transaction doit permettre de verifier que le `commercant_id` de la session correspond au `commercant_id` de la transaction.
- Une transaction ouverte par un commercant ne peut pas etre reutilisee par un autre commercant.
- La validation d'une prestation doit verifier simultanement :
  - la session commercant ;
  - le scope ;
  - la transaction ;
  - la coherence entre session, transaction et prestation cible.

## Decisions a instruire

## Recommandation d'architecture pour le ticket de session

- Choix recommande V1 : `token opaque` aleatoire, persiste cote serveur.
- Le client transporte uniquement un `session_token`.
- Le backend verifie en source de verite serveur :
  - l'existence de la session ;
  - la correspondance du token ;
  - la date d'expiration ;
  - la revocation eventuelle ;
  - les scopes ;
  - le `commercant_id` associe.

### Pourquoi ce choix

- La revocation est simple a gerer.
- La distinction `Session invalide` / `Session expiree` est naturelle.
- Le controle des scopes reste centralise.
- Le comportement est plus facile a faire evoluer qu'un token signe stateless.
- Ce choix est mieux adapte a une V1 securisee qu'un JWT si aucune contrainte forte de stateless n'existe.

### Structure recommandee cote serveur

- `id`
- `token_hash`
- `commercant_id`
- `scopes`
- `date_creation`
- `date_expiration`
- `date_revocation`
- `last_used_at` optionnel

### Transport recommande cote client/API

- Le `session_token` est transporte dans le header `Authorization`.
- Le format retenu est : `Authorization: Bearer <session_token>`.
- Le token reste un token opaque cote client, meme s'il est transporte avec un schema `Bearer`.

### TTL de session recommande

- Le TTL de session commercant en V1 est configurable via une variable d'environnement.
- La valeur est lue par le backend au runtime et appliquee a la creation de session.

### Usage de `last_used_at`

- `last_used_at` n'est pas utilise en V1.
- La V1 s'appuie uniquement sur `date_creation`, `date_expiration` et `date_revocation`.
- Le champ peut etre ajoute plus tard si un besoin de traçabilite fine ou d'expiration glissante apparait.

### Comportement client apres revocation en cours de session

- En cas de revocation d'une session en cours, le client doit afficher le motif de revocation.
- Le client doit ensuite demander une re-authentification du commercant.

## Referentiel initial recommande de scopes

- `commercant:session`
- `commercant:profil`
- `commercant:validation`
- `commercant:prestation`
- `commercant:reversement`
- `commercant:carte`

### Recommandation d'emission initiale

Scopes emis par defaut a l'ouverture de session :
- `commercant:session`
- `commercant:profil`
- `commercant:validation`
- `commercant:prestation`
- `commercant:reversement`
- `commercant:carte`

### Strategie de progression recommandee

- V1 : scopes larges par domaine fonctionnel pour limiter la complexite d'implementation.
- V2 : migration prevue vers des scopes plus fins, par exemple :
  - `commercant:prestation:read`
  - `commercant:prestation:write`
  - `commercant:validation_prestation:write`
  - `commercant:reversement:read`

## Backlog priorise

### Story `PRD-017` - Verifier un QR commercant a l'ouverture de l'application

Priorite : `P0`
Statut : `Termine`

Valeur metier : authentifier rapidement le commercant avant acces a l'application.

Criteres d'acceptation :
- Un use case dedie permet de verifier un `qr_commercant`.
- Le QR est refuse s'il n'est pas de type `carte_commercant`.
- Le QR est refuse si la carte commercant correspondante n'est pas active.
- La reponse retourne au minimum un resume d'identite du commercant authentifie et les metadonnees utiles a l'initialisation de session.
- Le resume de retour reste limite a un profil leger adapte au front, et non a un objet commercant complet.

Taches :
- Introduire un use case `ValiderQrCommercant`.
- Reutiliser `ServiceQr` pour verifier signature et structure du token.
- Verifier l'existence d'une carte active via le repository de cartes commercant.
- Definir le payload de sortie minimal pour le front commercant, incluant les informations d'identite utiles du commercant.

Definition of done :
- Le QR commercant peut etre valide en dehors du flux de validation de prestation.
- Les erreurs metier sont explicites et exploitables cote front.
- Un endpoint applicatif permet d'exposer ce controle au front commercant.

### Story `PRD-018` - Creer une session commercant a TTL limite

Priorite : `P0`
Statut : `Termine`

Valeur metier : eviter de rescanner le QR a chaque action tout en conservant une fenetre de confiance courte.

Criteres d'acceptation :
- Une session commercant est creee apres validation du QR.
- La session contient un identifiant de ticket, un commercant associe, une date d'expiration et des scopes.
- Le TTL est configurable.
- Le ticket de session est retourne au client pour reutilisation sur les actions commercant.

Taches :
- Introduire le modele domaine de session commercant.
- Definir persistence ORM et repository de session.
- Ajouter la configuration du TTL de session commercant.
- Definir la liste de scopes emise a l'ouverture de session.
- Implementer le use case d'initialisation de session.

Definition of done :
- Une session commercant peut etre creee, persistee et relue de maniere fiable.
- La date d'expiration est calculee automatiquement a la creation.

### Story `PRD-019` - Exiger un ticket de session commercant sur les actions protegees

Priorite : `P0`
Statut : `Termine`

Valeur metier : securiser de maniere homogene les operations commercant sensibles.

Criteres d'acceptation :
- Les actions commercant ciblees refusent une requete sans ticket de session.
- Le ticket est verifie avant execution de l'action.
- Le scope requis pour l'API doit etre present dans la session.
- La session doit correspondre au commercant attendu pour l'action.
- Le controle est reutilisable sur plusieurs use cases/API commercant.
- Les APIs de validation de prestation doivent continuer a verifier la transaction de validation en plus de la session.

Taches :
- Definir un service ou use case de verification de session commercant.
- Definir un mecanisme de verification de scope sur la session commercant.
- Integrer ce controle sur les actions commercant prioritaires.
- Factoriser le mecanisme d'extraction du ticket dans les APIs protegees.
- Adapter `ouvrir_transaction_validation` pour exiger une session commercant valide.
- Adapter `valider_prestation` pour utiliser la session commercant a la place du QR commercant, tout en conservant le controle de transaction.
- Ajouter les tests d'autorisation et de non regression.

Definition of done :
- Les actions commercant prioritaires sont protegees par le ticket de session.
- Les acces non autorises, sans scope ou incoherents sont refuses avant traitement metier.
- Le flux de validation de prestation conserve une double protection : session commercant + transaction de validation.

### Story `PRD-020` - Lever une exception `Session expiree`

Priorite : `P0`
Statut : `Termine`

Valeur metier : rendre explicite la necessite de rescanner la carte quand la session n'est plus valide.

Criteres d'acceptation :
- Si la date d'expiration est depassee, le systeme leve une exception metier `Session expiree`.
- La session expiree ne permet aucune action commercant protegee.
- La reponse API associee est coherente et exploitable cote front.

Taches :
- Introduire l'exception metier dediee.
- Ajouter la verification d'expiration dans le controle de session.
- Mapper l'exception sur les surfaces API concernees.
- Ajouter les tests sur sessions expirees et bords de TTL.

Definition of done :
- Une session expiriee est detectee de facon deterministe.
- Le front peut distinguer une session invalide d'une session expiree.

### Story `PRD-021` - Lever une exception `Session invalide`

Priorite : `P0`
Statut : `Termine`

Valeur metier : distinguer clairement un ticket non exploitable d'une session simplement expiree.

Criteres d'acceptation :
- Si le ticket est absent, inconnu, mal forme, revoque ou ne correspond pas au commercant attendu, le systeme leve `Session invalide`.
- Une session invalide ne permet aucune action commercant protegee.
- La reponse API associee permet au front de differencier `Session invalide` de `Session expiree`.

Taches :
- Introduire l'exception metier dediee `Session invalide`.
- Definir les cas exacts mappes sur `Session invalide`.
- Ajouter la verification correspondante dans le controle de session commercant.
- Mapper l'exception sur les surfaces API concernees.

Definition of done :
- Les erreurs de session sont distinguees de facon deterministe entre invalidite et expiration.
- Le front peut adapter son comportement selon le type d'erreur renvoye.

## Chantiers transverses

### BX-EP5-01 - Modele et persistence de session commercant

Priorite : `P0`

Livrables :
- dataclass domaine `SessionCommercant` ;
- table ORM associee ;
- repository de creation, lecture, expiration et eventuelle revocation ;
- support de persistence des scopes.
- evolution du modele `TransactionValidation` pour porter le `commercant_id` de l'auteur de l'ouverture.

### BX-EP5-02 - Configuration et secrets

Priorite : `P0`

Livrables :
- configuration du TTL de session ;
- decision sur le format du ticket ;
- referentiel ou convention de nommage des scopes ;
- si necessaire, secret de signature dedie.

### BX-EP5-03 - Surfaces API et front commercant

Priorite : `P1`

Livrables :
- endpoint d'ouverture de session commercant ;
- schema OpenAPI de session ;
- convention de transport du ticket sur les APIs commercant ;
- declaration du scope requis par endpoint commercant securise.

### BX-EP5-04 - Couverture de tests

Priorite : `P0`

Livrables :
- tests unitaires use cases et expiration ;
- tests integration persistence ;
- tests d'autorisation sur endpoints commercant.

## Dependances

- Existence d'un QR commercant versionne et verifiable.
- Repositories de carte commercant deja utilises dans le flux de validation.
- Clarification du perimetre des actions commercant a proteger en premiere iteration.

## Ordre recommande de livraison

1. `PRD-017`


   - Statut : `Termine`
2. `PRD-018`

   - Statut : `Termine`
3. `PRD-020`

   - Statut : `Termine`
4. `PRD-021`

   - Statut : `Termine`
5. `PRD-019`

   - Statut : `Termine`
6. `BX-EP5-01`, `BX-EP5-02`, `BX-EP5-04` en continu
7. `BX-EP5-03` selon calendrier d'exposition API/front

## Proposition de tickets implementables

- `EP5-T01` Ajouter le modele domaine et ORM `SessionCommercant`.
- `EP5-T02` Ajouter le repository de session commercant.
- `EP5-T03` Introduire la config TTL de session commercant.
- `EP5-T03B` Definir le referentiel de scopes commercant.
- `EP5-T04` Implementer le use case `ValiderQrCommercant`.
- `EP5-T05` Implementer le use case `InitialiserSessionCommercant`.
- `EP5-T06` Introduire l'exception metier `Session expiree`.
- `EP5-T07` Introduire l'exception metier `Session invalide`.
- `EP5-T08` Implementer le controle reutilisable `VerifierSessionCommercant`.
- `EP5-T09` Ajouter la verification de scope sur la session commercant.
- `EP5-T10` Faire evoluer `TransactionValidation` pour stocker le `commercant_id` ayant ouvert la transaction.
- `EP5-T11` Proteger la validation de prestation par session commercant + scope dedie.
- `EP5-T12` Proteger la consultation des reversements commercant par session + scope dedie.
- `EP5-T13` Proteger les futures actions de modification de prestation par session + scope dedie.
- `EP5-T14` Documenter le contrat d'authentification commercant, les scopes, le TTL et les erreurs de session.
