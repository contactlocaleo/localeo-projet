# Epic 36 - Fermeture commercant et remplacement des prestations achetees

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre a Localeo de gerer la sortie d'un commercant de l'aventure Localeo lorsque des prestations ont deja ete achetees mais ne sont pas encore executees, en remplacant les prestations impactees par des prestations similaires sans degradation pour le client.
- Decision contexte : les clauses contractuelles encadrent les modalites de fermeture, mais l'exploitation doit disposer d'un outil operationnel pour proteger l'experience client quand des prestations restent a honorer.
- Decision MVP : traiter en back-office les fermetures commercant avec desactivation du commercant, blocage des coffrets devenus incoherents, identification des prestations achetees non executees, choix d'une prestation de remplacement ou generation d'un remboursement, puis notification email des clients impactes.
- Decision statut : un commercant ferme porte le statut `FERME`.
- Decision modele : la fermeture est portee par une table dediee `fermetures_commercants`, et le commercant porte aussi le statut exploitable `FERME`.
- Decision acces commercant : apres fermeture, l'acces a l'application commercant est bloque totalement.
- Decision remplacement : la similarite de prestation est validee manuellement par l'operateur back-office.
- Decision finance : tout remplacement augmentant la valeur reversee exige une validation finance obligatoire avant execution.
- Decision notification MVP : email seul, pas de SMS obligatoire.
- Decision cas multiple : si un coffret contient plusieurs prestations du meme commercant ferme, chaque prestation impactee est traitee avec les memes regles de remplacement ou remboursement.
- Decision remboursement partiel : le montant propose est calcule au prorata simple du nombre de prestations non consommees concernees, avec possibilite d'ajustement back-office avant validation.
- Decision remboursement MVP : l'operation cree une demande de remboursement back-office `A_TRAITER`, sans execution PSP automatique.
- Hors scope MVP : arbitrage juridique automatique, remplacement multi-prestations complexe et workflow commercant autonome.

## Probleme

Un commercant peut sortir du dispositif Localeo alors que certains clients ont achete un coffret contenant une prestation chez ce commercant, sans l'avoir encore consommee. Sans outil dedie, l'exploitation doit traiter manuellement les cas, avec un risque de rupture d'experience client, d'erreur de reversement, de manque de tracabilite et de communication incomplete.

## Risque business

- Des clients peuvent se presenter chez un commercant qui ne fait plus partie du reseau Localeo.
- Une prestation achetee mais non executable peut degrader la confiance client.
- Le support peut devoir compenser au cas par cas sans vision exhaustive des clients impactes.
- Le remplacement non trace peut creer des incoherences de reversement ou de reporting.

## Risque technique

- Les prestations achetees sont snapshottees dans les instances de coffrets et ne doivent pas etre modifiees comme un simple catalogue courant.
- Un remplacement doit preserver l'historique de la prestation initiale et le lien vers la prestation de substitution.
- Les statuts de prestation deja valides, annules, expires ou rembourses ne doivent pas etre remplaces a tort.
- L'envoi email doit etre idempotent et rattache a une operation de fermeture/replacement auditable.
- Les reversements doivent tenir compte de la prestation finalement executee sans perdre la trace de l'engagement initial.

## Perimetre MVP

- Ajouter une action back-office de fermeture operationnelle d'un commercant.
- Desactiver le commercant lui-meme afin de le rendre invisible sur le site, masquer toutes ses prestations publiques et bloquer les nouvelles ventes.
- Rendre non achetables les coffrets contenant une prestation du commercant desactive tant que le coffret n'a pas ete mis a jour et recalcule.
- Identifier les prestations achetees non executees impactees par ce commercant.
- Permettre la selection d'une prestation de remplacement similaire.
- Permettre la generation d'un remboursement client lorsqu'aucune prestation de substitution acceptable n'est disponible.
- Remplacer les prestations impactees dans les instances de coffrets eligibles.
- Conserver la trace de la prestation initiale, de la prestation de remplacement, de l'operateur et du motif.
- Envoyer un email de notification a tous les clients impactes.
- Afficher un recapitulatif avant validation definitive.
- Rendre l'operation idempotente pour eviter les doubles remplacements et doubles emails.
- Exposer l'historique de remplacement dans la timeline support et les vues back-office utiles.
- Respecter le pattern Unit of Work pour chaque use case.

## Hors perimetre MVP

- Choix automatique de la meilleure prestation de remplacement.
- Validation client du remplacement.
- Notification SMS obligatoire.
- Workflow commercant pour demander lui-meme sa fermeture.
- Gestion contractuelle complete des penalites ou compensations.

## User Stories

1. `PRD-261` En tant qu'operateur back-office, je veux desactiver un commercant et declarer sa fermeture operationnelle afin de bloquer les nouvelles ventes et preparer le traitement des prestations restantes.
   - Statut : `Termine`
   - Resultat attendu : le commercant porte le statut `FERME`, visible en back-office.
   - Resultat attendu : le profil public du commercant n'est plus visible sur le site ni retourne par les APIs publiques.
   - Resultat attendu : l'acces applicatif commercant est bloque totalement.
   - Resultat attendu : les prestations du commercant ne sont plus visibles sur le site, dans la recherche publique, ni exposables a de nouvelles ventes.
   - Resultat attendu : la fermeture porte motif, date d'effet, commentaire interne et operateur.

2. `PRD-262` En tant qu'operateur back-office, je veux voir les prestations achetees non executees impactees afin d'evaluer le volume client a traiter.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les instances de coffrets contenant une prestation du commercant en statut encore executable.
   - Resultat attendu : les prestations deja validees, annulees, expirees ou remboursees sont exclues.
   - Resultat attendu : les clients impactes sont dedoublonnes pour la notification.

3. `PRD-263` En tant qu'operateur back-office, je veux choisir une prestation de remplacement similaire afin de maintenir la promesse client.
   - Statut : `Termine`
   - Resultat attendu : seules les prestations actives et selectionnees manuellement par l'operateur sont selectionnables.
   - Resultat attendu : l'operateur visualise l'ecart de valeur, ville, type de prestation et commercant.
   - Resultat attendu : un remplacement augmentant la valeur reversee reste bloque tant qu'une validation finance n'est pas enregistree.
   - Resultat attendu : le remplacement ne peut pas pointer vers une prestation du commercant ferme.

4. `PRD-264` En tant qu'operateur back-office, je veux simuler l'operation avant validation afin de verifier les clients, coffrets et prestations impactes.
   - Statut : `Termine`
   - Resultat attendu : la simulation retourne le nombre de prestations impactees, clients impactes et emails a creer.
   - Resultat attendu : la simulation liste les coffrets rendus non achetables tant qu'ils n'ont pas ete remis a jour.
   - Resultat attendu : aucune donnee n'est modifiee pendant la simulation.

5. `PRD-265` En tant que systeme, je veux appliquer le remplacement aux prestations achetees eligibles afin que le client puisse utiliser une prestation equivalente.
   - Statut : `Termine`
   - Resultat attendu : chaque statut de prestation d'instance cible reference la prestation de remplacement.
   - Resultat attendu : le snapshot client affiche la nouvelle prestation executable.
   - Resultat attendu : l'historique conserve la prestation initiale et la raison du remplacement.

6. `PRD-266` En tant que client impacte, je veux recevoir un email clair afin de comprendre que ma prestation a ete remplacee sans action de ma part.
   - Statut : `Termine`
   - Resultat attendu : un email est cree pour chaque client impacte.
   - Resultat attendu : l'email indique la prestation initiale, la prestation de remplacement, le nouveau commercant et le fait que le QR/code existant reste utilisable si applicable.
   - Resultat attendu : l'email reste sobre et ne mentionne pas de detail contractuel interne.

7. `PRD-267` En tant qu'operateur support, je veux consulter l'historique complet d'un remplacement afin de repondre a un client ou verifier une operation.
   - Statut : `Termine`
   - Resultat attendu : la timeline support affiche fermeture, remplacement et notification email.
   - Resultat attendu : les vues back-office indiquent clairement qu'une prestation a ete remplacee.

8. `PRD-268` En tant que responsable finance, je veux que le remplacement conserve une base fiable de reversement afin de payer le bon commercant apres execution.
   - Statut : `Termine`
   - Resultat attendu : la validation future reverse vers le commercant de remplacement.
   - Resultat attendu : la prestation initiale reste visible pour audit et analyse de l'operation.

9. `PRD-269` En tant que responsable qualite, je veux que l'operation soit idempotente afin d'eviter les doubles remplacements ou doubles emails.
   - Statut : `Termine`
   - Resultat attendu : une meme prestation d'instance ne peut etre remplacee qu'une seule fois dans une operation active.
   - Resultat attendu : un relancement technique ne recree pas les emails deja crees.

10. `PRD-270` En tant qu'auditeur, je veux tracer toutes les decisions de fermeture et remplacement afin de disposer d'une preuve exploitable.
    - Statut : `Termine`
    - Resultat attendu : l'audit porte commercant ferme, prestation initiale, prestation de remplacement, operateur, motif, date et nombre d'impacts.
    - Resultat attendu : l'operation est consultable meme apres archivage du commercant.

11. `PRD-271` En tant que responsable catalogue, je veux que les coffrets contenant une prestation d'un commercant desactive soient rendus non achetables tant qu'ils n'ont pas ete mis a jour afin de proteger l'integrite de leur composition et de leur prix.
    - Statut : `Termine`
    - Resultat attendu : tout coffret actif contenant une prestation du commercant desactive est suspendu ou masque a l'achat.
    - Resultat attendu : le coffret redevient achetable uniquement apres retrait/remplacement de la prestation et recalcul de coherence prix/reversements/marge.

12. `PRD-272` En tant qu'operateur back-office, je veux pouvoir generer un remboursement lorsqu'aucune prestation de substitution n'est possible afin de traiter les clients ayant une prestation en cours chez le commercant ferme.
    - Statut : `Termine`
    - Resultat attendu : l'operation identifie les clients/coffrets instances eligibles au remboursement.
    - Resultat attendu : le remboursement est cree via le mecanisme de remboursement existant ou une demande de remboursement tracable.
    - Resultat attendu : les clients impactes recoivent un email de notification de remboursement.

13. `PRD-273` En tant que client impacte sans substitution possible, je veux recevoir un email clair afin de comprendre que la prestation ne peut plus etre honoree et qu'un remboursement est initie.
    - Statut : `Termine`
    - Resultat attendu : l'email indique la prestation concernee, le motif operationnel, le montant ou le perimetre rembourse et le delai attendu.
    - Resultat attendu : l'email reste sobre et ne mentionne pas de detail contractuel interne.

## Regles de gestion

- Une prestation deja validee ne peut pas etre remplacee.
- Le commercant ferme doit pouvoir etre desactive lui-meme, en plus de la desactivation commerciale de ses prestations.
- Un commercant desactive pour fermeture ne doit plus etre expose publiquement sur le site, la marketplace, les pages publiques ou les APIs publiques.
- Les prestations d'un commercant desactive ne doivent plus etre visibles sur le site, dans la recherche publique, dans les pages coffrets ou dans les APIs publiques.
- Un commercant desactive pour fermeture ne doit plus permettre de nouvelles ventes sur ses prestations.
- Tout coffret contenant une prestation du commercant desactive devient non achetable tant qu'il n'a pas ete mis a jour.
- Un coffret impacte redevient achetable uniquement apres retrait ou remplacement de la prestation et recalcul de coherence prix, reversements et marge.
- Une prestation annulee, expiree ou rattachee a un achat rembourse ne doit pas etre remplacee.
- Une prestation de remplacement doit etre active et exploitable commercialement.
- Une prestation de remplacement ne peut pas appartenir au commercant ferme.
- La similarite de prestation est une decision manuelle de l'operateur back-office, a partir des informations affichees.
- Un remplacement qui augmente la valeur reversee exige une validation finance explicite avant execution.
- Le remplacement ne doit pas invalider le QR ou le code court si le support de validation reste rattache a l'instance de coffret.
- Le client ne doit pas avoir d'action obligatoire a effectuer pour beneficier du remplacement.
- Si aucune prestation de substitution acceptable n'est disponible, le traitement cible est un remboursement des clients ayant une prestation en cours chez ce commercant.
- Le remboursement doit etre tracable et rattache a l'operation de fermeture.
- Le remboursement est cree comme demande back-office a traiter, sans execution PSP automatique dans le MVP.
- Le montant rembourse propose est calcule au prorata simple : montant du coffret divise par le nombre total de prestations du coffret, multiplie par le nombre de prestations non consommees concernees.
- Le montant propose peut etre ajuste par le back-office avant validation de la demande de remboursement.
- Les emails de notification de remboursement sont crees dans l'outbox dans la meme transaction que la demande de remboursement.
- Si un coffret contient plusieurs prestations du meme commercant ferme, chaque prestation en cours est traitee individuellement avec les memes regles.
- Une operation de fermeture doit produire un recapitulatif avant execution.
- L'operation definitive doit etre transactionnelle via Unit of Work.
- Les emails de notification sont crees dans l'outbox dans la meme transaction que le remplacement.
- L'envoi effectif des emails reste pilote par le batch email existant.

## Modele cible

### Fermeture commercant

Table cible : `fermetures_commercants`

- `id`
- `commercant_id`
- `statut`
- `motif`
- `date_effet`
- `desactiver_commercant`
- `bloquer_acces_commercant`
- `commentaire_interne`
- `created_by`
- `created_at`
- `validated_by`
- `validated_at`

### Coffret impacte

Evolution cible possible des coffrets :

- ajout d'un statut de suspension commerciale si le statut actuel ne couvre pas le cas ;
- ajout d'un motif `COMMERCANT_DESACTIVE` ou equivalent selon le referentiel ;
- tracabilite du blocage automatique et du deblocage apres mise a jour.

Les coffrets impactes ne doivent plus etre achetables jusqu'a remise en coherence de la composition et du prix.

### Commercant

Evolution cible de `commercants` :

- `statut` enrichi avec l'etat `FERME`.
- `date_desactivation`
- `motif_desactivation`
- `desactive_par`

La fermeture operationnelle est portee par la table dediee `fermetures_commercants`, et le commercant lui-meme porte l'etat exploitable `FERME` par la marketplace, les APIs publiques et l'application commercant.

Les filtres publics doivent traiter ce statut comme non visible pour :

- les pages commercant ;
- les pages coffret ;
- la recherche multi-scope ;
- les listes de prestations ;
- le feed d'activite publique si un lien direct vers le commercant ou la prestation serait expose.

### Remplacement prestation

Table cible possible : `remplacements_prestations_commercant`

- `id`
- `fermeture_commercant_id`
- `prestation_initiale_id`
- `prestation_remplacement_id`
- `statut`
- `motif`
- `created_by`
- `created_at`

### Impact instance

Table cible possible : `remplacements_prestations_instances`

- `id`
- `remplacement_id`
- `coffret_instance_id`
- `statut_prestation_instance_id`
- `prestation_initiale_snapshot`
- `prestation_remplacement_snapshot`
- `email_sortant_id`
- `statut_notification`
- `created_at`

### Remboursement fermeture

Table cible possible : reutiliser `remboursements_achat` si le modele couvre le cas, ou ajouter une table de liaison :

- `id`
- `fermeture_commercant_id`
- `coffret_instance_id`
- `statut_prestation_instance_id`
- `remboursement_achat_id`
- `montant_rembourse`
- `motif`
- `email_sortant_id`
- `created_at`

## APIs et integration cible

- Back-office :
  - lister les commercants eligibles a une fermeture operationnelle ;
  - creer une operation de fermeture ;
  - simuler les impacts ;
  - selectionner une prestation de remplacement ;
  - generer un remboursement si aucune substitution n'est possible ;
  - valider l'operation ;
  - consulter l'historique.
- Emails :
  - nouveau type `NOTIFICATION_REMPLACEMENT_PRESTATION`;
  - nouveau type `NOTIFICATION_REMBOURSEMENT_PRESTATION_COMMERCANT_FERME` ou libelle equivalent ;
  - template HTML et texte dedies ;
  - outbox email existante reutilisee.
- Support :
  - timeline achat/coffret enrichie avec les evenements de fermeture et remplacement.
- Finance :
  - validation future et reversement rattaches a la prestation de remplacement.

## Lots d'implementation

### Lot 1 - Cadrage modele et statuts

- Definir les statuts de fermeture et remplacement.
- Ajouter les tables de fermeture, remplacement et impacts.
- Ajouter les contraintes d'unicite/idempotence.

### Lot 2 - Detection des impacts

- Implementer la simulation.
- Exclure les prestations non eligibles.
- Calculer les clients et emails impactes.
- Identifier les coffrets a rendre non achetables.
- Identifier les prestations en cours eligibles a remboursement si aucune substitution n'est fournie.

### Lot 3 - Execution transactionnelle

- Implementer le use case de validation de fermeture/remplacement via Unit of Work.
- Suspendre ou masquer a l'achat les coffrets impactes.
- Mettre a jour les statuts de prestations d'instances.
- Creer les impacts et audits.

### Lot 4 - Notification client

- Ajouter template email HTML/texte pour remplacement.
- Ajouter template email HTML/texte pour remboursement.
- Creer les emails sortants dans l'outbox.
- Ajouter tests d'idempotence.

### Lot 4 bis - Remboursement sans substitution

- Reutiliser le moteur de remboursement existant si possible.
- Creer les demandes de remboursement rattachees a la fermeture commercant.
- Tracer le montant, le motif et l'email client.

### Lot 5 - Back-office et support

- Ajouter l'IHM back-office de simulation/validation.
- Ajouter l'historique dans les vues support et 360 commercant.
- Ajouter filtres et badges de remplacement.

### Lot 6 - Finance et reversement

- Verifier la validation future sur prestation de remplacement.
- Verifier le calcul de reversement vers le nouveau commercant.
- Documenter les cas limites.

## Points a cadrer

- Aucun point bloquant restant pour le MVP.

## Tests attendus

- Simulation sans modification des donnees.
- Exclusion des prestations deja validees.
- Exclusion des prestations annulees, expirees ou remboursees.
- Refus d'une prestation de remplacement inactive ou rattachee au commercant ferme.
- Coffret contenant une prestation du commercant desactive rendu non achetable.
- Coffret redevenu achetable uniquement apres mise a jour et recalcul coherent.
- Generation d'un remboursement si aucune substitution n'est possible.
- Creation d'un email de notification de remboursement.
- Execution idempotente.
- Creation d'un email par client impacte.
- Conservation de l'historique initial/remplacement.
- Validation future et reversement vers le commercant de remplacement.
