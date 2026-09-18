# Backlog Epic 20 - Gestion des remboursements

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : gerer de bout en bout les remboursements lies a l'annulation d'un coffret paye, avec une tracabilite exploitable par le support et le back-office.
- Decision produit : un coffret ne peut pas etre partiellement rembourse.
- Decision produit : si l'annulation concerne un paiement valide, le systeme doit creer ou suivre une obligation de remboursement.
- Decision produit : l'annulation invalide la `CoffretInstance` et les prestations associees non consommees.
- Decision produit : en B2B, la granularite de remboursement MVP est la `CoffretInstance`, pas toute la commande multi-instances.
- Decision produit : le remboursement MVP est uniquement manuel / hors systeme, avec reference externe obligatoire a l'execution.
- Decision produit : le client est notifie automatiquement par email lors de l'annulation, puis lors du remboursement execute.
- Decision produit : la comptabilite MVP se limite a une trace operationnelle auditable, sans generation d'avoir comptable.
- Decision produit : aucun reversement partiel n'est gere ; si une prestation est consommee ou deja reversee, le remboursement standard est refuse en MVP.

## Probleme

Le backend sait aujourd'hui annuler une `CoffretInstance` avant consommation et tracer une reference externe de remboursement, mais il ne porte pas encore un workflow de remboursement complet.

Sans epic dediee, Localeo risque de melanger trois notions differentes :

- annulation metier du coffret ;
- remboursement financier du client ;
- tracabilite support/comptable de l'operation.

Le risque principal est operationnel : un client peut avoir un coffret annule sans remboursement suivi, ou un remboursement effectue hors systeme sans preuve exploitable dans le back-office.

## Perimetre MVP

- Creer un objet metier de remboursement rattache a l'achat, au paiement et a la `CoffretInstance`.
- Declencher un remboursement a traiter lorsqu'une `CoffretInstance` payee est annulee avant consommation.
- Interdire tout remboursement partiel d'un coffret.
- Refuser l'annulation/remboursement si une prestation associee est deja consommee.
- Suivre les statuts de remboursement depuis le back-office.
- Tracer l'operateur, le motif, le montant, la reference externe et les dates clefs.
- Exposer les remboursements a traiter dans le pilotage operationnel back-office.
- Envoyer un email automatique au client lors de l'annulation.
- Envoyer un email automatique au client lorsque le remboursement est marque `REMBOURSE`.

## Hors perimetre MVP

- Remboursement partiel d'un coffret.
- Remboursement automatique via PSP sans validation back-office.
- Gestion des chargebacks et litiges bancaires.
- Remboursement apres reversement commercant deja paye.
- Reversement partiel, compensation partielle ou recalcul financier partiel cote commercant.
- Avoirs comptables complets automatises.
- Compensation commerciale hors remboursement.

## User Stories

1. `PRD-105` En tant qu'operateur back-office, je veux qu'une annulation de coffret paye cree un remboursement a traiter afin de ne pas perdre le suivi financier client.
   - Statut : `Termine`
   - Resultat attendu : si le paiement est valide, l'annulation cree un remboursement en statut `A_TRAITER`.
   - Resultat attendu : si le paiement n'est pas valide, aucun remboursement financier n'est cree.

2. `PRD-106` En tant qu'operateur back-office, je veux suivre le statut d'un remboursement afin de savoir s'il est a traiter, en cours, execute, annule, refuse ou en echec.
   - Statut : `Termine`
   - Resultat attendu : les statuts cibles sont `A_TRAITER`, `EN_COURS`, `REMBOURSE`, `ANNULE`, `REFUSE`, `ECHEC`.
   - Resultat attendu : `ANNULE` designe une demande devenue non executable lors du controle final, tandis que `REFUSE` reste une decision operateur.
   - Resultat attendu : chaque changement de statut est date et audite.

3. `PRD-107` En tant que systeme, je veux interdire les remboursements partiels afin de respecter la regle produit du coffret indivisible.
   - Statut : `Termine`
   - Resultat attendu : le montant rembourse correspond toujours au montant client du coffret ou de l'instance ciblee.
   - Resultat attendu : aucune API ni action back-office ne permet de saisir un montant partiel.

4. `PRD-108` En tant que support Localeo, je veux voir le remboursement rattache a l'achat, au paiement et a la `CoffretInstance` afin de repondre rapidement a un client.
   - Statut : `Termine`
   - Resultat attendu : la fiche achat et la fiche `CoffretInstance` affichent le statut de remboursement, le montant, le motif et la reference externe.

5. `PRD-109` En tant qu'operateur back-office, je veux marquer un remboursement externe comme execute afin de tracer les remboursements faits hors systeme.
   - Statut : `Termine`
   - Resultat attendu : l'operateur renseigne une reference externe obligatoire et une date d'execution.
   - Resultat attendu : le remboursement passe en statut `REMBOURSE`.
   - Resultat attendu : le passage a `REMBOURSE` invalide la `CoffretInstance`, renseigne les informations d'annulation et rend les prestations restantes inutilisables.

6. `PRD-110` En tant que systeme, je veux annuler automatiquement une demande de remboursement devenue non eligible afin d'eviter une perte financiere et une incoherence avec les reversements.
   - Statut : `Termine`
   - Resultat attendu : l'eligibilite est recontrolee juste avant le passage a `REMBOURSE`.
   - Resultat attendu : si la `CoffretInstance` est expiree, deja utilisee, deja annulee ou dans un statut non remboursable, la demande passe a `ANNULE` avec motif trace.
   - Resultat attendu : si au moins une prestation associee est `VALIDEE`, la demande passe a `ANNULE` avec motif trace.
   - Resultat attendu : une demande `ANNULE` ou `REFUSE` ne peut plus etre marquee `REMBOURSE`.

7. `PRD-111` En tant qu'exploitant, je veux piloter les remboursements a traiter afin de ne pas laisser de dossiers clients sans action.
   - Statut : `Termine`
   - Resultat attendu : le dashboard back-office affiche les remboursements `A_TRAITER` et `ECHEC`.
   - Resultat attendu : les listes back-office permettent de filtrer par statut, date, montant, motif et reference achat.

8. `PRD-123` En tant que client, je veux recevoir un email lors de l'annulation de mon coffret afin de comprendre que le coffret n'est plus utilisable.
   - Statut : `Termine`
   - Resultat attendu : l'email indique la reference d'achat, la `CoffretInstance` annulee et le statut du remboursement si applicable.

9. `PRD-124` En tant que client, je veux recevoir un email lorsque le remboursement est execute afin d'avoir une confirmation de traitement.
   - Statut : `Termine`
   - Resultat attendu : l'email indique la reference d'achat, la date d'execution et la reference externe du remboursement si disponible.

## Regles de gestion

- Un coffret ne peut pas etre partiellement rembourse.
- Un remboursement porte sur une `CoffretInstance` entiere.
- En B2B, une commande multi-instances peut donner lieu a plusieurs remboursements, un par `CoffretInstance` annulee eligible.
- L'annulation d'une `CoffretInstance` payee cree un remboursement a traiter.
- L'annulation d'une `CoffretInstance` non payee ne cree pas de remboursement financier.
- L'annulation invalide la `CoffretInstance` et les statuts de prestations associes encore `A_VALIDER`.
- L'annulation est refusee si au moins une prestation associee est deja `VALIDEE`.
- L'annulation/remboursement standard est refuse si la prestation a deja donne lieu a un reversement execute ou non annulable.
- Aucun reversement partiel n'est cree pour compenser une annulation tardive.
- Le montant du remboursement est calcule par le backend, jamais saisi librement.
- La reference externe devient obligatoire quand un remboursement hors systeme est marque `REMBOURSE`.
- Le passage a `REMBOURSE` rend la `CoffretInstance` inutilisable : statut `ANNULE`, date/motif/commentaire d'annulation et reference externe de remboursement sont renseignes.
- Lors du passage a `REMBOURSE`, toutes les prestations restantes non `VALIDEE` de l'instance passent a `ANNULEE`.
- L'eligibilite du remboursement est recontrolee au dernier moment, au moment de l'execution back-office.
- Si l'instance est expiree, deja utilisee, deja annulee, dans un statut non remboursable ou si au moins une prestation est `VALIDEE`, la demande de remboursement passe a `ANNULE` avec motif dans `motif_echec`/`commentaire_interne`.
- `ANNULE` est une annulation automatique de la demande devenue non executable ; `REFUSE` est reserve au refus manuel operateur.
- Un remboursement `REMBOURSE`, `ANNULE`, `REFUSE` ou `ECHEC` ne peut pas etre supprime.
- Un remboursement `ANNULE` ou `REFUSE` ne peut pas etre execute ulterieurement.
- Toute transition de statut produit un evenement d'audit.
- Le mode d'execution MVP est `HORS_SYSTEME`.
- Aucun appel PSP de remboursement n'est effectue en MVP.
- Le client recoit un email automatique lors de l'annulation.
- Le client recoit un email automatique lors du passage du remboursement a `REMBOURSE`.

## Modele de donnees cible

### Table `remboursements_achat`

- `id`
- `achat_id`
- `coffret_instance_id`
- `paiement_id`
- `montant`
- `devise`
- `statut`
- `motif`
- `commentaire_interne`
- `mode_execution` : `HORS_SYSTEME` en MVP, `PSP` en evolution.
- `reference_remboursement_externe`
- `provider_refund_id`
- `demande_par`
- `traite_par`
- `date_demande`
- `date_execution`
- `date_echec`
- `motif_echec`
- `created_at`
- `updated_at`

### Contraintes recommandees

- Unicite fonctionnelle sur `coffret_instance_id` pour empecher deux remboursements concurrents sur la meme instance.
- `montant > 0`.
- `reference_remboursement_externe` obligatoire si `statut = REMBOURSE` et `mode_execution = HORS_SYSTEME`.
- Index sur `statut`, `date_demande`, `achat_id`, `coffret_instance_id`, `paiement_id`.

## Workflows cibles

### Annulation d'un coffret non paye

1. L'operateur demande l'annulation.
2. Le backend verifie qu'aucune prestation n'est consommee.
3. La `CoffretInstance` passe a `ANNULE`.
4. Les prestations associees `A_VALIDER` passent a `ANNULEE`.
5. Aucun remboursement n'est cree.

### Annulation d'une CoffretInstance payee

1. L'operateur demande l'annulation.
2. Le backend verifie que le paiement est valide et qu'aucune prestation n'est consommee.
3. La `CoffretInstance` passe a `ANNULE`.
4. Les prestations associees `A_VALIDER` passent a `ANNULEE`.
5. Le backend cree un remboursement `A_TRAITER` du montant total.
6. Le dossier apparait dans la file back-office des remboursements.
7. Le client recoit un email d'annulation.

### Annulation B2B multi-instances

1. L'operateur selectionne une `CoffretInstance` precise.
2. Le backend applique les memes controles que pour le B2C.
3. Si l'instance est eligible, seul le coffret instance cible est annule.
4. Le backend cree un remboursement pour cette `CoffretInstance` uniquement.
5. Les autres instances de la commande restent inchangees.

### Traitement manuel du remboursement

1. L'operateur ouvre un remboursement `A_TRAITER`.
2. Il effectue le remboursement hors systeme.
3. Il renseigne la reference externe.
4. Au moment de l'action "marquer rembourse", le backend recontrole l'eligibilite de la `CoffretInstance`.
5. Si l'instance est toujours eligible, le remboursement passe a `REMBOURSE`.
6. La `CoffretInstance` passe a `ANNULE` et les prestations restantes non consommees passent a `ANNULEE`.
7. L'audit conserve l'operateur, la date et la reference.
8. Le client recoit un email de confirmation de remboursement.
9. Si l'instance n'est plus eligible, la demande passe a `ANNULE` avec un motif exploitable et aucun email de remboursement execute n'est envoye.

## Lots d'implementation

### Lot 1 - Modele remboursement

- Ajouter le modele domaine `RemboursementAchat`.
- Ajouter le modele ORM et la migration SQL.
- Ajouter les statuts de remboursement.
- Ajouter les contraintes d'unicite et d'integrite.

### Lot 2 - Use case annulation avec remboursement

- Adapter le use case d'annulation pour creer un remboursement si le paiement est valide.
- Centraliser le calcul du montant remboursable.
- Garantir l'idempotence pour eviter les doubles remboursements.

### Lot 3 - Back-office remboursement

- Ajouter une liste des remboursements.
- Ajouter une fiche detail.
- Ajouter les actions `marquer en cours`, `marquer rembourse`, `refuser`, `marquer en echec`.
- Recontroler l'eligibilite au moment de `marquer rembourse` et annuler automatiquement la demande si elle n'est plus executable.
- Invalider la `CoffretInstance` et les prestations restantes lorsque le remboursement est marque `REMBOURSE`.
- Afficher le remboursement depuis les fiches achat et `CoffretInstance`.

### Lot 4 - Audit et support

- Ajouter les evenements `REMBOURSEMENT_CREE`, `REMBOURSEMENT_EN_COURS`, `REMBOURSEMENT_EXECUTE`, `REMBOURSEMENT_REFUSE`, `REMBOURSEMENT_ECHEC`.
- Ajouter les informations utiles au support client.
- Ajouter les filtres operationnels dans le dashboard back-office.

### Lot 5 - Tests

- Tester l'annulation d'un coffret non paye.
- Tester l'annulation d'un coffret paye.
- Tester le refus si prestation consommee.
- Tester l'interdiction du remboursement partiel.
- Tester l'idempotence de creation du remboursement.
- Tester les transitions de statut.
- Tester le statut `ANNULE` lorsqu'une demande n'est plus eligible au moment de l'execution.
- Tester l'invalidation de la `CoffretInstance` apres passage a `REMBOURSE`.
- Tester le passage des prestations restantes a `ANNULEE` apres passage a `REMBOURSE`.
- Tester l'impossibilite d'executer une demande `ANNULE` ou `REFUSE`.
- Tester le remboursement B2B par `CoffretInstance`.
- Tester l'email automatique d'annulation.
- Tester l'email automatique de remboursement execute.
- Tester le refus si une prestation est deja reversee ou non annulable.

## Criteres d'acceptation MVP

- Annuler une `CoffretInstance` payee cree un remboursement `A_TRAITER`.
- Annuler une `CoffretInstance` non payee ne cree pas de remboursement.
- Aucune action ne permet de rembourser partiellement un coffret.
- Une `CoffretInstance` avec une prestation `VALIDEE` ne peut pas etre annulee/remboursee.
- Les prestations associees encore `A_VALIDER` passent a `ANNULEE`.
- Le remboursement est visible depuis le back-office avec son statut, son montant et son motif.
- Le passage a `REMBOURSE` exige une reference externe en mode manuel.
- Le passage a `REMBOURSE` annule la `CoffretInstance` et la rend inutilisable.
- Une demande de remboursement dont l'instance a expire ou dont au moins une prestation a ete consommee depuis la demande passe a `ANNULE` avec motif.
- Les transitions sont auditees.
- Le remboursement MVP est cree en mode `HORS_SYSTEME`.
- Une commande B2B peut etre remboursee instance par instance.
- Le client recoit un email lors de l'annulation.
- Le client recoit un email lors du remboursement execute.
- Aucun avoir comptable n'est genere en MVP.
- Aucun reversement partiel n'est cree.

## Decisions actees

- Granularite B2B : remboursement par `CoffretInstance`.
- Mode MVP : remboursement uniquement manuel / hors systeme.
- Notification client : email automatique lors de l'annulation et lors du remboursement execute.
- Comptabilite : simple trace operationnelle auditable.
- Reversements : pas de reversement partiel ; si une prestation est consommee ou deja reversee, le remboursement standard est refuse en MVP.
