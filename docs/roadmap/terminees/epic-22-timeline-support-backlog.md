# Backlog Epic 22 - Timeline support achat et coffret

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir une vue support chronologique permettant de reconstituer l'histoire complete d'un achat, d'une `CoffretInstance`, d'un paiement, d'un email, d'un SMS ou d'une validation de prestation.
- Decision produit : la timeline support doit etre exploitable par un operateur non technique.
- Decision technique : la timeline s'appuie d'abord sur les traces existantes (`evenements_audit`, achats, paiements, emails, SMS, validations, statuts de prestation) avant de creer une nouvelle table dediee.
- Decision operationnelle : chaque evenement affiche doit porter au minimum une date, un type, un statut, une ressource rattachee et les identifiants utiles au support.

## Probleme

Le backend possede deja plusieurs sources de traces : achats, paiements, emails sortants, SMS sortants, validations, audit et logs correles. Mais ces informations sont dispersees.

Quand un client contacte le support, l'operateur doit aujourd'hui naviguer entre plusieurs ecrans et tables pour comprendre ce qui s'est passe : paiement confirme ou non, coffret cree ou non, email envoye ou en echec, SMS transmis, prestation deja validee, annulation, remboursement ou expiration.

Sans timeline support, Localeo augmente le temps de resolution, le risque d'erreur support et la difficulte a expliquer un incident client ou commercant.

## Risque business

- Support lent sur les cas sensibles : debit client, coffret non recu, QR invalide, prestation deja consommee.
- Risque de repondre au client avec une information incomplete.
- Risque de remboursement manuel injustifie faute de preuve rapide.
- Image de marque degradee au lancement si les incidents simples ne sont pas diagnostiques rapidement.

## Risque technique

- Les investigations reposent trop sur les logs techniques.
- Les traces metier restent partielles si elles ne sont pas consolidees.
- Les equipes support et produit dependent des developpeurs pour comprendre un dossier.
- Les incidents paiement/email/SMS sont plus difficiles a rapprocher d'un achat.

## Perimetre MVP

- Creer un use case de consultation de timeline support.
- Agreger les evenements par `achat_id`.
- Agreger les evenements par `coffret_instance_id`.
- Inclure les evenements d'audit metier.
- Inclure les paiements et webhooks connus.
- Inclure les emails sortants et leurs statuts.
- Inclure les SMS sortants et leurs statuts.
- Inclure les validations de prestation et mouvements de reversement si disponibles.
- Inclure les annulations, remboursements et expirations quand les epics associees sont implementees.
- Exposer une route interne protegee.
- Ajouter un affichage back-office lisible depuis la fiche achat et la fiche `CoffretInstance`.

## Hors perimetre MVP

- Moteur de recherche full-text global.
- Export PDF d'un dossier support.
- Vue client publique de la timeline.
- Analyse automatique de cause racine.
- Alerting temps reel.
- Retention avancee ou archivage long terme.

## User Stories

1. `PRD-117` En tant que support Localeo, je veux consulter la timeline d'un achat afin de comprendre rapidement tout le parcours client.
   - Statut : `Termine`
   - Resultat attendu : la timeline affiche les evenements de l'achat dans l'ordre chronologique.
   - Resultat attendu : chaque evenement porte un libelle metier comprehensible.

2. `PRD-118` En tant que support Localeo, je veux consulter la timeline d'une `CoffretInstance` afin de comprendre son activation, son usage, son expiration ou son annulation.
   - Statut : `Termine`
   - Resultat attendu : la timeline affiche creation, activation, validation de prestation, annulation et expiration si disponibles.
   - Resultat attendu : les prestations associees sont identifiables.

3. `PRD-119` En tant que support Localeo, je veux voir les emails et SMS rattaches a un achat afin de repondre aux cas "je n'ai rien recu".
   - Statut : `Termine`
   - Resultat attendu : la timeline affiche les emails et SMS avec destinataire masque, statut, date d'envoi et provider message id si disponible.
   - Resultat attendu : les erreurs d'envoi sont visibles.

4. `PRD-120` En tant qu'operateur support, je veux retrouver une timeline via plusieurs identifiants afin de ne pas bloquer quand le client ne donne pas la bonne reference.
   - Statut : `Termine`
   - Resultat attendu : recherche par `achat_id`, `reference_achat`, `coffret_instance_id`, email client, telephone client masque, `transaction_id` ou `provider_message_id`.
   - Resultat attendu : les recherches sensibles restent reservees au back-office.

5. `PRD-121` En tant qu'operateur support, je veux voir les identifiants techniques utiles sans exposer de secrets afin de transmettre un dossier exploitable aux developpeurs.
   - Statut : `Termine`
   - Resultat attendu : la timeline expose `request_id`, `achat_id`, `paiement_id`, `transaction_id`, `coffret_instance_id`, `validation_id`, `email_id`, `sms_id`.
   - Resultat attendu : tokens, cles d'idempotence completes, QR et secrets ne sont jamais affiches.

6. `PRD-122` En tant que responsable exploitation, je veux que les evenements critiques soient audites afin de garantir une trace durable hors logs techniques.
   - Statut : `Termine`
   - Resultat attendu : les evenements critiques proviennent de `evenements_audit` quand disponibles.
   - Resultat attendu : la timeline distingue les evenements reconstruits depuis les tables metier et les evenements audites.

## Regles de gestion

- La timeline est en lecture seule.
- La timeline est reservee aux routes internes/back-office.
- Les evenements sont tries par date croissante par defaut.
- Chaque evenement doit avoir un `type_evenement`, un `libelle`, une `date_evenement`, une `phase` ou un `statut`.
- Les donnees sensibles doivent etre masquees : tokens, QR, cles API, idempotency key complete, telephone complet si non necessaire.
- Les erreurs d'envoi email/SMS doivent etre visibles mais sans exposer de contenu sensible.
- Les evenements reconstruits doivent etre clairement distinguables des evenements audites.
- Une timeline vide doit retourner un etat explicite, pas une erreur technique.

## Sources de donnees MVP

### Achats

- `achats_coffret`
- Evenements attendus :
  - achat initialise ;
  - paiement en attente ;
  - paiement confirme ;
  - achat annule si disponible.

### Paiements

- `paiements`
- `paiement_events`
- Evenements attendus :
  - webhook recu ;
  - webhook ignore ;
  - paiement confirme ;
  - doublon webhook.

### Coffrets instances

- `coffrets_instances`
- `statuts_prestation_coffret_instance`
- Evenements attendus :
  - instance creee ;
  - instance activee ;
  - instance utilisee ;
  - instance annulee ;
  - instance expiree.

### Emails / SMS

- `emails_sortants`
- `sms_sortants`
- Evenements attendus :
  - message prepare ;
  - message envoye ;
  - message delivre ;
  - message en echec ;
  - message annule.

### Validation prestation

- `validations_prestation`
- `mouvements_reversement`
- Evenements attendus :
  - prestation validee ;
  - mouvement de reversement cree ;
  - feedback demande si disponible.

### Audit

- `evenements_audit`
- Evenements attendus :
  - actions sensibles ;
  - transitions metier critiques ;
  - annulation/remboursement/expiration quand disponibles.

## API / Back-office cible

### Route interne

- `GET /internal/support/timeline`
- Parametres possibles :
  - `achat_id`
  - `reference_achat`
  - `coffret_instance_id`
  - `transaction_id`
  - `provider_message_id`
  - `email_client`
  - `telephone_client`

### Reponse cible

- `contexte`
  - `achat_id`
  - `reference_achat`
  - `coffret_instance_id`
  - `email_client_masque`
  - `telephone_client_masque`
- `evenements`
  - `date_evenement`
  - `type_evenement`
  - `libelle`
  - `phase`
  - `statut`
  - `ressource_type`
  - `ressource_id`
  - `request_id`
  - `metadata_support`

### Back-office

- Ajouter un lien `Timeline support` depuis :
  - fiche achat ;
  - fiche `CoffretInstance` ;
  - fiche paiement ;
  - fiche email/SMS.
- Afficher une vue chronologique simple avec filtres :
  - tous ;
  - paiement ;
  - coffret ;
  - notification ;
  - prestation ;
  - support/audit.

## Lots d'implementation

### Lot 1 - Contrat timeline

- Ajouter les schemas de reponse.
- Definir les types d'evenements.
- Definir les regles de masquage.

### Lot 2 - Use case agregateur

- Ajouter `ConsulterTimelineSupport`.
- Resoudre le contexte depuis les identifiants fournis.
- Agreger achats, paiements, instances, statuts, emails, SMS, validations et audit.
- Trier et normaliser les evenements.

### Lot 3 - API interne

- Ajouter `support_api.py` ou route interne equivalente.
- Proteger par session admin.
- Retourner une erreur metier claire si aucun critere n'est fourni.

### Lot 4 - Back-office

- Ajouter les liens depuis les fiches metier.
- Ajouter une page HTML interne lisible.
- Ajouter les filtres de categorie.

### Lot 5 - Tests

- Tester timeline par `achat_id`.
- Tester timeline par `coffret_instance_id`.
- Tester inclusion paiement/email/SMS.
- Tester masquage des donnees sensibles.
- Tester ordre chronologique.
- Tester absence de resultat.

## Criteres d'acceptation MVP

- Le support peut ouvrir une timeline depuis un achat.
- Le support peut ouvrir une timeline depuis une `CoffretInstance`.
- Les evenements paiement, instance, email/SMS et validation apparaissent dans l'ordre chronologique.
- Les identifiants techniques utiles sont visibles.
- Les secrets et tokens ne sont pas affiches.
- La route est protegee par session admin.
- Les evenements issus de l'audit sont inclus.
- Une timeline peut etre utilisee sans consulter directement la base ou les logs techniques.

## Points a arbitrer

- Recherche par email/telephone : autorisee en MVP ou reservee a une V2 pour limiter l'exposition RGPD.
- Niveau de detail des erreurs provider email/SMS.
- Necessite ou non d'une table materialisee `timeline_support_events`.
- Retention des evenements affiches.
- Export du dossier support.
- Mention client-facing : la timeline reste interne ou certaines lignes peuvent etre reutilisees dans une reponse client.

## Decisions MVP actees

- Recherche par `email_client` et `telephone_client` autorisee en MVP.
- Route cible unique : `GET /internal/support/timeline`.
- Les evenements reconstruits et audites doivent etre fusionnes quand une correspondance fiable est possible.
- Les metadonnees provider email/SMS sont affichees apres masquage des donnees sensibles.
- Les points d'entree back-office MVP sont : achat, `CoffretInstance`, paiement, email et SMS.
- Tests MVP : verification manuelle.
- Pas de table materialisee `timeline_support_events` en MVP.
