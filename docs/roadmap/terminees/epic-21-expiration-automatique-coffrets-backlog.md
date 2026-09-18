# Backlog Epic 21 - Expiration automatique des coffrets

## Synthese

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : fournir un batch operable qui expire automatiquement les `CoffretInstance` arrivees a echeance et les prestations restantes non consommees.
- Decision produit : une instance expiree ne doit plus permettre la validation de prestations.
- Decision produit : les prestations restantes en `A_VALIDER` passent en `EXPIREE` lorsque l'instance expire.
- Decision produit : le statut exact d'une `CoffretInstance` expiree reste `EXPIRE`.
- Decision produit : le client recoit un email de relance avant expiration et un email d'information a expiration.
- Decision produit : le support peut prolonger manuellement une instance apres expiration.
- Decision technique : le traitement doit etre idempotent, relancable et auditable.
- Decision technique : aucune migration `EXPIRE` vers `EXPIREE` n'est faite pour `CoffretInstance`; on garde la convention code existante `EXPIRE`.
- Decision technique MVP : le batch d'expiration est declenche manuellement via API batch.
- Decision technique MVP : le batch de relance avant expiration est declenche manuellement via API batch.
- Decision technique MVP : la relance avant expiration utilise `N = 7 jours` par defaut.
- Decision technique MVP : la fenetre de relance est de 48 heures, soit `[now + 7 jours ; now + 7 jours + 48h]` par defaut.
- Decision technique MVP : le scope `internal:batch` existe deja et protege les routes batch.
- Decision technique MVP : les routes batch sont exposees sous `/protected/...`, conformement aux batchs existants.
- Decision technique MVP : l'idempotence des emails de relance et d'information a expiration repose sur une table dediee `relances_expiration_coffrets`.
- Decision technique MVP : les tests automatises sont reportes ; verification manuelle MVP uniquement.

## Probleme

Le backend verifie deja l'expiration au moment de certains usages, mais il ne materialise pas automatiquement l'expiration dans les statuts metier.

Sans batch d'expiration, Localeo garde des `CoffretInstance` et des prestations en apparence consommables alors que leur date d'expiration est depassee. Cela fausse le support, les dashboards, l'encours commercant, les exports et les decisions d'annulation/remboursement.

## Risque business

- Un commercant peut croire qu'une prestation reste a honorer alors que le coffret est expire.
- Le support peut traiter un dossier sur un statut incoherent.
- Les dashboards affichent un encours trop eleve.
- Une validation terrain peut etre refusee a l'usage, mais trop tard dans le parcours client.

## Risque technique

- Incoherence entre `coffrets_instances.date_expiration`, `coffrets_instances.statut` et `statuts_prestation_coffret_instance.statut`.
- Calculs d'encours plus complexes car ils doivent toujours interpreter la date d'expiration a la volee.
- Reprises manuelles difficiles si aucun job ne trace ce qu'il a expire.

## Perimetre MVP

- Ajouter un use case de batch d'expiration.
- Identifier les `CoffretInstance` expirables.
- Passer les instances expirees au statut `EXPIRE`.
- Passer les prestations restantes `A_VALIDER` au statut `EXPIREE`.
- Ne jamais modifier les prestations deja `VALIDEE` ou `ANNULEE`.
- Ne jamais modifier les instances deja `UTILISE`, `ANNULE` ou `EXPIRE`.
- Exposer une API interne ou action back-office operable.
- Retourner un resume d'execution.
- Auditer chaque execution.
- Ajouter un batch separe de relance avant expiration, charge d'envoyer un email aux clients dont le coffret expire dans `N` jours.
- Rendre `N` configurable automatiquement par configuration d'exploitation, sans modification de code.
- Ajouter une prolongation manuelle support depuis le back-office, reservee aux admins.
- Ajouter l'idempotence dediee pour les emails de relance avant expiration et les emails d'information a expiration.

## Hors perimetre MVP

- Notification commercant automatique.
- Prolongation commerciale de validite.
- Politique de remboursement automatique a expiration.
- Archivage definitif des instances anciennes.
- Action UI de lancement des batchs depuis le back-office.
- Tests automatises complets.

## User Stories

1. `PRD-112` En tant que systeme, je veux expirer automatiquement les `CoffretInstance` dont la date d'expiration est depassee afin d'aligner le statut metier avec la realite d'usage.
   - Statut : `Termine`
   - Resultat attendu : les instances eligibles passent en `EXPIRE`.
   - Resultat attendu : le traitement ignore les instances deja finales.

2. `PRD-113` En tant que systeme, je veux passer les prestations restantes non consommees en `EXPIREE` afin d'empecher toute consommation tardive.
   - Statut : `Termine`
   - Resultat attendu : les statuts de prestation `A_VALIDER` rattaches a une instance expiree passent en `EXPIREE`.
   - Resultat attendu : les statuts `VALIDEE`, `ANNULEE` et deja `EXPIREE` ne sont pas modifies.

3. `PRD-114` En tant qu'exploitant, je veux lancer le batch d'expiration depuis une route interne ou le back-office afin de pouvoir reprendre le traitement en cas d'incident.
   - Statut : `Termine`
   - Resultat attendu : une route interne protegee ou une action back-office lance le traitement.
   - Resultat attendu : le resultat affiche les compteurs d'instances et prestations traitees.

4. `PRD-115` En tant qu'exploitant, je veux que le batch soit idempotent afin de pouvoir le relancer sans double effet.
   - Statut : `Termine`
   - Resultat attendu : relancer le batch sur la meme periode ne modifie pas a nouveau les lignes deja expirees.
   - Resultat attendu : les compteurs distinguent candidats, traites et ignores.

5. `PRD-116` En tant que support Localeo, je veux voir qu'une instance ou une prestation a expire automatiquement afin d'expliquer le statut a un client ou un commercant.
   - Statut : `Termine`
   - Resultat attendu : une trace d'audit indique date d'execution, operateur/systeme, nombre d'instances expirees et nombre de prestations expirees.
   - Resultat attendu : les fiches back-office affichent les statuts `EXPIRE` de facon explicite.

6. `PRD-116B` En tant que systeme, je veux relancer automatiquement par email les beneficiaires dont le coffret expire dans `N` jours afin de reduire les coffrets non consommes et les demandes support tardives.
   - Statut : `Termine`
   - Resultat attendu : un batch separe identifie les `CoffretInstance` actives ou en attente d'activation dont `date_expiration` tombe dans la fenetre cible.
   - Resultat attendu : `N` est lu depuis l'env var `COFFRET_EXPIRATION_REMINDER_DAYS`, avec une valeur par defaut MVP de 7 jours.
   - Resultat attendu : l'email est cree dans l'outbox `emails_sortants` et envoye par le batch email existant.
   - Resultat attendu : le traitement est idempotent et ne renvoie pas plusieurs fois la meme relance pour la meme instance et la meme echeance.

7. `PRD-116C` En tant que support admin, je veux prolonger manuellement une `CoffretInstance` expiree afin de traiter un geste commercial ou un incident support.
   - Statut : `Termine`
   - Resultat attendu : seul un admin peut prolonger une instance.
   - Resultat attendu : le nombre de jours de prolongation est saisi depuis le back-office.
   - Resultat attendu : une instance expiree redevient `ACTIVE` si elle avait deja ete activee, sinon `EN_ATTENTE_ACTIVATION`.
   - Resultat attendu : la prolongation est auditee dans `evenements_audit`.

## Regles de gestion

- Une `CoffretInstance` est eligible si `date_expiration < now`.
- Les statuts cibles d'instance expirables sont `ACTIVE` et `EN_ATTENTE_ACTIVATION`.
- Les statuts finaux `UTILISE`, `ANNULE` et `EXPIRE` ne sont pas modifies par le batch.
- Une prestation restante est eligible si son statut est `A_VALIDER` et si son instance est expiree.
- Une prestation `VALIDEE` reste `VALIDEE`.
- Une prestation `ANNULEE` reste `ANNULEE`.
- Une prestation `EXPIREE` reste `EXPIREE`.
- Le batch doit etre idempotent.
- Le batch doit pouvoir etre execute avec un `dry_run`.
- Le batch doit retourner des compteurs exploitables.
- En MVP, le batch est declenche manuellement via API batch.
- Le statut cible d'une instance expiree est `EXPIRE`.
- Un email d'information a expiration est cree pour le client lorsque l'instance expire.
- Le statut code existant `EXPIRE` est conserve pour `CoffretInstance`.
- L'email d'information a expiration doit etre idempotent via `relances_expiration_coffrets`.

### Regles de relance avant expiration

- Le batch de relance est separe du batch d'expiration.
- Une `CoffretInstance` est eligible a la relance si son statut est `ACTIVE` ou `EN_ATTENTE_ACTIVATION`.
- Une `CoffretInstance` est eligible si sa `date_expiration` est comprise dans la fenetre `[now + N jours ; now + N jours + 48h]` par defaut.
- `N` est lu depuis l'env var `COFFRET_EXPIRATION_REMINDER_DAYS`, avec une valeur par defaut MVP de 7 jours.
- La fenetre d'execution doit eviter les trous si le batch est lance avec retard.
- Le batch doit etre idempotent par `coffret_instance_id`, `date_expiration` et `N`.
- Les instances `UTILISE`, `ANNULE` et `EXPIRE` ne sont jamais relancees.
- L'email doit rappeler la date d'expiration, le coffret, la reference client et le lien de consultation ou d'activation disponible.
- Le batch doit accepter un `dry_run`.
- Le batch doit retourner les compteurs `candidats`, `emails_crees`, `deja_relances`, `ignores` et `erreurs`.
- En MVP, le batch de relance est declenche manuellement via API batch.

### Regles de prolongation support

- La prolongation manuelle est reservee aux admins.
- Le nombre de jours de prolongation est saisi dans le back-office.
- Une prolongation met a jour `date_expiration`.
- Si l'instance etait `EXPIRE` et possede une `date_activation`, son statut redevient `ACTIVE`.
- Si l'instance etait `EXPIRE` sans `date_activation`, son statut redevient `EN_ATTENTE_ACTIVATION`.
- Toutes les prestations `EXPIREE` rattachees a l'instance prolongee redeviennent `A_VALIDER`.
- La prolongation doit etre auditee dans `evenements_audit` avec admin, ancien statut, nouveau statut, ancienne date d'expiration et nouvelle date d'expiration.

### Contenu email MVP

- Email de relance avant expiration :
  - type email : `RELANCE_EXPIRATION_COFFRET_INSTANCE` ;
  - objet propose : `Votre coffret Localeo expire bientot` ;
  - contenu : nom du coffret, reference achat, date d'expiration, lien de consultation ou d'activation disponible, rappel que les prestations restantes ne seront plus utilisables apres expiration.
  - rendu MVP : template HTML dedie via `ServicePreparationEmail`.
- Email d'information a expiration :
  - type email : `INFORMATION_EXPIRATION_COFFRET_INSTANCE` ;
  - objet propose : `Votre coffret Localeo a expire` ;
  - contenu : nom du coffret, reference achat, date d'expiration, statut des prestations restantes, invitation a contacter le support en cas de question.
  - rendu MVP : template HTML dedie via `ServicePreparationEmail`.

## Modele de donnees cible

Le MVP peut fonctionner sans nouvelle table si l'audit central `evenements_audit` est suffisant.

Option recommandee si besoin d'historique operable plus riche :

### Table `executions_batch_expiration_coffrets`

- `id`
- `date_execution`
- `mode` : `DRY_RUN` ou `EXECUTION`
- `declenche_par`
- `cutoff_at`
- `instances_candidates`
- `instances_expirees`
- `prestations_candidates`
- `prestations_expirees`
- `erreur`
- `metadata`

### Idempotence emails expiration

### Table `relances_expiration_coffrets`

- `id UUID PRIMARY KEY`
- `type_relance TEXT NOT NULL` : `AVANT_EXPIRATION` ou `A_EXPIRATION`
- `coffret_instance_id UUID NOT NULL REFERENCES coffrets_instances(id)`
- `achat_id UUID NOT NULL REFERENCES achats_coffret(id)`
- `date_expiration TIMESTAMP NOT NULL`
- `reminder_days INTEGER NULL` pour `A_EXPIRATION`
- `email_sortant_id UUID NULL REFERENCES emails_sortants(id)`
- `statut TEXT NOT NULL` : `A_CREER`, `EMAIL_CREE`, `IGNOREE`, `ERREUR`
- `date_creation TIMESTAMP NOT NULL`
- `erreur TEXT NULL`
- `metadata JSONB NULL`
- contrainte unique sur `(coffret_instance_id, date_expiration, type_relance, reminder_days)`
- index sur `coffret_instance_id`, `achat_id`, `type_relance`, `statut`, `date_creation`, `email_sortant_id`

## Workflow cible

1. Le batch calcule `now` ou un `cutoff_at` fourni.
2. Il identifie les instances `ACTIVE` ou `EN_ATTENTE_ACTIVATION` avec `date_expiration < cutoff_at`.
3. Il identifie les prestations `A_VALIDER` associees.
4. En `dry_run`, il retourne les compteurs sans modifier les donnees.
5. En execution, il passe les instances candidates a `EXPIRE`.
6. En execution, il passe les prestations candidates a `EXPIREE`.
7. Il cree un email d'information a expiration pour le client si aucune trace `A_EXPIRATION` n'existe deja dans `relances_expiration_coffrets`.
8. Il persiste une trace d'audit.
9. Il retourne un resume d'execution.

### Workflow relance avant expiration

1. Le batch lit `N` depuis `COFFRET_EXPIRATION_REMINDER_DAYS` ou utilise 7 jours par defaut.
2. Il calcule la fenetre cible de relance sur 48 heures.
3. Il identifie les instances `ACTIVE` ou `EN_ATTENTE_ACTIVATION` qui expirent dans cette fenetre.
4. Il ignore les instances deja relancees pour la meme date d'expiration et le meme `N`.
5. En `dry_run`, il retourne les compteurs sans creer d'email.
6. En execution, il cree un email outbox `RELANCE_EXPIRATION_COFFRET_INSTANCE`.
7. Il audite l'execution avec les compteurs.
8. Le batch email existant se charge ensuite de l'envoi effectif.

## API / Back-office cible

### Route interne

- `POST /protected/coffrets-instances/expiration/batch`
- Protegee par scope `internal:batch`.
- Parametres :
  - `dry_run`
  - `cutoff_at`
  - `limit`
- Reponse :
  - `cutoff_at`
  - `dry_run`
  - `instances_candidates`
  - `instances_expirees`
  - `prestations_candidates`
  - `prestations_expirees`
  - `ignored`

### Route interne relance avant expiration

- `POST /protected/coffrets-instances/expiration/reminders/batch`
- Protegee par scope `internal:batch`.
- Parametres :
  - `dry_run`
  - `reminder_days` optionnel, sinon configuration par defaut
  - `window_hours`, defaut 48
  - `limit`
- Reponse :
  - `reminder_days`
  - `window_start`
  - `window_end`
  - `dry_run`
  - `instances_candidates`
  - `emails_crees`
  - `deja_relances`
  - `ignored`
  - `erreurs`

### Back-office

- Pas d'action UI de lancement des batchs en MVP ; lancement via API batch uniquement.
- Action admin de prolongation manuelle depuis une `CoffretInstance`.
- Carte dans le dashboard operationnel back-office :
  - instances expirees a traiter ;
  - prestations restantes a expirer ;
  - relances d'expiration a envoyer ;
  - derniere execution du batch.

## Lots d'implementation

### Lot 1 - Use case batch

- Ajouter `ExpirerCoffretsInstances`.
- Implementer `dry_run`.
- Implementer les compteurs.
- Garantir l'idempotence.

### Lot 2 - Persistence atomique

- Utiliser des `UPDATE ... WHERE statut IN (...) AND date_expiration < cutoff`.
- Utiliser une transaction unique par execution.
- Eviter les boucles ligne par ligne si le volume augmente.

### Lot 3 - API interne et back-office

- Ajouter les routes internes protegees par scope `internal:batch`.
- Ajouter l'action back-office de prolongation manuelle.
- Afficher le resume d'execution.

### Lot 4 - Audit et exploitation

- Ajouter l'evenement `coffret_instance.expiration_batch`.
- Ajouter l'evenement `coffret_instance.expiration_reminder_batch`.
- Ajouter l'evenement `coffret_instance.expiration_extended`.
- Ajouter l'email client d'information a expiration.
- Documenter la frequence recommandee.
- Ajouter la procedure d'exploitation.

### Lot 5 - Batch relance avant expiration

- Ajouter `RelancerCoffretsInstancesAvantExpiration`.
- Ajouter la configuration `COFFRET_EXPIRATION_REMINDER_DAYS`.
- Ajouter une fenetre de relance par defaut de 48 heures.
- Ajouter le type email `RELANCE_EXPIRATION_COFFRET_INSTANCE`.
- Ajouter le type email `INFORMATION_EXPIRATION_COFFRET_INSTANCE`.
- Ajouter les templates HTML dedies pour la relance avant expiration et l'information a expiration.
- Ajouter la table `relances_expiration_coffrets`.
- Creer les emails dans l'outbox sans envoi synchrone.
- Garantir l'idempotence par instance, date d'expiration et `N`.
- Exposer une route interne de lancement.
- Retourner un resume d'execution exploitable.

### Lot 6 - Verification manuelle MVP

- Verifier manuellement une instance active expiree.
- Verifier manuellement une instance en attente d'activation expiree.
- Verifier manuellement qu'une instance utilisee n'est pas modifiee.
- Verifier manuellement qu'une prestation `VALIDEE` n'est pas modifiee.
- Verifier manuellement qu'une prestation `A_VALIDER` passe en `EXPIREE`.
- Verifier manuellement l'idempotence.
- Verifier manuellement le `dry_run`.
- Verifier manuellement la relance d'une instance expirant dans `N` jours sur une fenetre 48h.
- Verifier manuellement qu'une instance deja relancee n'est pas relancee deux fois.
- Verifier manuellement qu'une instance `UTILISE`, `ANNULE` ou `EXPIRE` n'est pas relancee.
- Verifier manuellement que le batch de relance cree un email outbox sans envoi direct.
- Verifier manuellement la prolongation admin depuis le back-office.

## Criteres d'acceptation MVP

- Une instance active dont la date d'expiration est depassee passe a `EXPIRE`.
- Une instance en attente d'activation expiree passe a `EXPIRE`.
- Les prestations restantes `A_VALIDER` passent a `EXPIREE`.
- Les prestations deja `VALIDEE` restent `VALIDEE`.
- Les instances finales ne sont pas modifiees.
- Le batch peut etre relance sans double effet.
- Une execution est auditee.
- Le back-office ou une route interne permet de lancer le traitement et de lire les compteurs.
- Le batch separe de relance avant expiration cree un email outbox pour les instances eligibles.
- Le batch de relance est idempotent et parametrable via `N`.
- Le batch d'expiration cree un email d'information a expiration pour le client.
- Une prolongation manuelle apres expiration est possible pour le support.
- Les deux routes batch sont protegees par le scope `internal:batch`.
- Aucun bouton de lancement de batch n'est requis en MVP.

## Points a arbitrer

- Aucun point produit bloquant restant sur le MVP.

## Decisions actees

- Frequence cible du batch d'expiration : declenchement manuel seulement en MVP via API batch.
- Statut exact de `CoffretInstance` : on garde `EXPIRE`.
- Valeur par defaut de `N` pour la relance avant expiration : 7 jours.
- Fenetre de relance : 48 heures, soit `[now + 7 jours ; now + 7 jours + 48h]` par defaut.
- Frequence du batch de relance : declenchement manuel en MVP via API batch.
- Politique client : email de relance avant expiration et email d'information a expiration.
- Politique support : permettre une prolongation manuelle apres expiration.
- Prolongation support : admin uniquement, nombre de jours saisi depuis le back-office, retour a `ACTIVE` si l'instance avait ete activee sinon `EN_ATTENTE_ACTIVATION`.
- Securite API batch : scope `internal:batch`.
- Audit : `evenements_audit` suffit.
- Dry-run : requis sur les deux batchs.
- Back-office : API batch uniquement pour le lancement ; pas d'action UI de lancement de batch en MVP.
- Tests : verification manuelle MVP uniquement.
- Routes batch : exposees sous `/protected`, conformement aux batchs existants.
- Email MVP : templates HTML dedies via `ServicePreparationEmail`.
- Reactivation prestations apres prolongation : toutes les prestations `EXPIREE` rattachees a l'instance redeviennent `A_VALIDER`.
