# Roadmap produit

## État global consolidé au 26 septembre 2026

Le tronc commun comprend 65 identifiants : 56 epics terminees, 5 a faire,
1 en cours, 2 abandonnees et 1 fusionnee. L'Epic 61 est absorbee par l'Epic 60.
Les documents sont ranges par etat dans l'[index de la roadmap](README.md).

| Etat | Epics |
| --- | --- |
| A faire | `EPIC-54`, `EPIC-58`, `EPIC-62`, `EPIC-64`, `EPIC-65` |
| En cours | `EPIC-55` |
| Termine | 56 epics : toutes les autres epics de `EPIC-01` a `EPIC-60`, et `EPIC-63`, hors `EPIC-05` et `EPIC-12` |
| Abandonne | `EPIC-05` : QR commercant remplace par l'Epic 10 ; `EPIC-12` : flux manuel decommissionne par l'Epic 39 |
| Fusionnee | `EPIC-61` dans `EPIC-60` ; non comptee comme terminee |

Les backlogs applicatifs sont désormais réunis avec leur EPIC commune, dans
un seul fichier par sujet. Trois identifiants applicatifs complètent ce tronc :

| Identifiant | Sujet | État |
| --- | --- | --- |
| [EPIC-MARKETPLACE-18](terminees/epic-marketplace-18-google-analytics-marketplace-backlog.md) | Google Analytics ; distinct de la page commerçant immersive 18 | Terminée (V1 livrée ; collecte suspendue MARKET-001) |
| [EPIC-MARKETPLACE-54](a-faire/epic-marketplace-54-harmonisation-identite-visuelle-marketplace-backlog.md) | Identité visuelle ; distinct du calendrier de l'Avent 54 | À faire (classement courant ; implémentation locale documentée, revue et recette attendues) |
| [EPIC-PRES-CONTENU-001](terminees/epic-animation-edition-prestations.md) | Édition directe des prestations ; le futur sas reste dans l'EPIC 62 | Terminée (parcours existant) |

Le total consolidé est de **68 identifiants : 58 terminés, 6 à faire, 1 en cours,
2 abandonnés et 1 fusionné**. L'ancien numéro local Marketplace 53 (pagination)
est rattaché à l'EPIC 57, sans ajouter d'identifiant ni le confondre avec la tombola.

En cas d'ecart avec un statut historique plus detaille, cette synthese et le
[suivi backlog](suivi-backlog.md) font foi. Les recettes d'environnement et
actions d'exploitation residuelles ne rouvrent pas une epic terminee.
Le classement du 15 septembre corrige les anciens libelles globaux des Epics
5 et 12 d'apres leurs decisions explicites. L'Epic 47 est terminee selon
la confirmation produit de l'utilisateur le 15 septembre 2026.

Derniere evolution suivie :

- [Epic 65 — Vues ERP audit, paiements et reversements](a-faire/epic-65-vues-erp-audit-paiements-reversements-backlog.md) :
  cadrage du 26 septembre 2026 ; trois vues intégrées, recherche, filtres et détail,
  accès ADMIN conservé ; paiements et reversements sous « Paiements et facturation ».
  Réutiliser les lectures et le suivi 360 existants, sans nouveau flux financier.
  [Spécification V1 disponible](../specifications/epic-65-vues-erp/README.md),
  hypothèses de périmètre explicites et implémentation à réaliser ; les epics 30, 39, 43, 44, 51 et 60
  conservent leur clôture historique.

- [Epic 64 - Parcours de retractation en ligne depuis le site](a-faire/epic-64-parcours-retractation-en-ligne-backlog.md) :
  priorite critique ; obligation applicable depuis le 19 juin 2026 aux nouveaux
  contrats de consommation en ligne ouvrant droit a retractation ; acces sans
  compte, declaration confirmee, preuve durable, instruction et articulation
  avec le moteur de remboursement existant ; cadrage initial, a developper.

- [Epic 63 - Initialiser une plateforme vivante pour une commune](terminees/epic-63-jeux-demonstration-communes-backlog.md) :
  principe directeur absolu : aucun impact sur le code applicatif ;
  les donnees s'adaptent aux applications existantes ;
  preparation, installation et restauration par script autonome hors ERP ;
  retour manuel a la base precedente et sauvegardes conservees 30 jours ;
  objectifs de generation en moins de 10 minutes hors sauvegarde/transferts et
  de cycle complet du Passeport en 30 minutes ;
  ecosysteme explorable avec historique, activite actuelle et actions a effectuer ;
  environ 10 commercants et 15 coffrets contenant chacun 2 a 3 prestations ;
  30 clients, 60 achats, 100 participants et 6 actualites sur 3 mois d'historique ;
  commune principale creee a partir du nom fourni et 3 communes voisines de test ;
  chaque voisine ajoute 2 commercants, 1 coffret de 2 a 3 prestations et 1 actualite ;
  Stripe de test, Brevo et Scaleway reellement connectes via les integrations existantes ;
  emails, SMS et notifications envoyes aux adresses et appareils internes autorises ;
  evolution de l'activite uniquement par les actions des presentateurs ;
  environ 10 animations fictives preparees et un cycle complet de Passeport
  commercant a jouer en direct, de la creation jusqu'au tirage et aux gains ;
  remplacement temporaire de la base de test, commune reelle et commerces/personnes
  fictifs ; animations en cours/cloturees avec consommation des lots, marketplace
  avec actualites et creation d'une animation en direct avec intervention d'un
  commercant ; referentiels preserves, sauvegarde et restauration controlees ;
  cadrage produit valide (16 decisions, 11 stories),
  [specification technique detaillee redigee](../specifications/epic-63-demonstrations-communes/README.md) ;
  outillage recentre avec tests PostgreSQL et restauration ; adaptations applicatives retirees ;
  [bilan de livraison](../specifications/epic-63-demonstrations-communes/livraison-recette.md),
  recette connectee requise avant la premiere demonstration.

- [Epic 62 - Validation des modifications de prestations](a-faire/epic-62-validation-modifications-prestations-backlog.md) :
  sas commercant, maintien de la version applicable, decision avec revalidation
  BUM et WebPush dans Localeo Support ; cadrage initial, a developper.

- [Epic 60 - BackOffice ERP, referencement et commercialisation 360](terminees/epic-60-vision-360-commercialisation-backlog.md) :
  diagnostic, alertes, ateliers commercant/coffret, navigation ERP et suivi
  des dossiers ; V1 implementee et testee, migration v218, bascule directe ; [dossier unifie](../specifications/epic-60-vision-360-commercialisation/README.md).
- Epic 61 : identifiant historique fusionne dans l'Epic 60 ; documents dedies
  supprimes sur demande utilisateur, stories et arbitrages conserves sous Epic 60.

## Objectif

Cette roadmap produit structure les evolutions autour de trois enjeux metier :
- mieux controler l'exposition du catalogue avant mise en ligne ;
- ouvrir un canal d'interaction plus direct avec les commercants ;
- proteger l'integrite des coffrets quand une prestation evolue ou doit etre retiree ;
- maintenir une capacite de secours exploitable quand le parcours nominal d'honorisation n'est plus disponible.

## Principes de priorisation

- `Critique` : risque direct de casse metier, incoherence catalogue ou non-respect d'une obligation legale applicable.
- `Elevee` : forte valeur produit ou operationnelle avec impact transverse.
- `Moyenne` : valeur nette mais non bloquante a court terme.

---

## Epic 1. Gouvernance du referencement commer?ant et prestation

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : permettre de referencer un commercant et ses prestations sans les rendre achetables tant qu'ils ne sont pas explicitement actifs.
- Pourquoi maintenant : c'est le prealable pour onboarder proprement des partenaires sans exposer un catalogue incomplet ou non valide.
- Statuts commercant cibles : `BROUILLON`, `REFERENCE`, `ACTIF`, `SUSPENDU`, `ARCHIVE`
- Statuts coffret cibles : `BROUILLON`, `REFERENCE`, `ACTIVE`, `SUSPENDU`, `ARCHIVE`
- Statuts prestation cibles : `BROUILLON`, `REFERENCE`, `ACTIVE`, `SUSPENDU`, `ARCHIVE`

### User Stories

1. `PRD-001` En tant qu'admin, je veux definir un statut sur un commercant afin de pouvoir le referencer sans l'exposer a l'achat tant qu'il n'est pas actif.
   - Statut : `Termine`
   - Resultat attendu : un commercant peut exister dans le back-office avec un statut distinct de sa disponibilite publique, parmi `BROUILLON`, `REFERENCE`, `ACTIF`, `SUSPENDU`, `ARCHIVE`.
   - Resultat attendu : tout commercant nouvellement cree est initialise par defaut au statut `BROUILLON`.

2. `PRD-002` En tant qu'admin, je veux que les prestations rattachees a un commercant inactif ne soient pas achetables sur la marketplace.
   - Statut : `Termine`
   - Resultat attendu : les prestations existent en gestion mais sont exclues du catalogue public tant que le commercant n'est pas actif.
   - Resultat attendu : la prestation porte son propre statut distinct du commercant.
   - Resultat attendu : un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas porter de prestations au statut `ACTIVE`, `BROUILLON` ou `REFERENCE`.

3. `PRD-003` En tant qu'admin, je veux activer un commercant et ses prestations de maniere controlee pour publier le catalogue au bon moment.
   - Statut : `Termine`
   - Resultat attendu : la bascule vers le statut actif rend le commercant eligible au catalogue selon les regles definies.
   - Resultat attendu : le coffret porte son propre statut distinct du commercant.
   - Resultat attendu : un coffret n'est activable que si le commercant associe est `ACTIF`.

4. `PRD-015` En tant qu'admin, je veux empecher l'activation d'un coffret pour un commercant qui n'est pas actif afin de garder un catalogue coherent.
   - Statut : `Termine`
   - Resultat attendu : un commercant `BROUILLON` ou `REFERENCE` ne peut pas avoir de coffret actif.

5. `PRD-016` En tant qu'admin, je veux bloquer la suspension ou l'archivage d'un commercant si cela casserait des coffrets deja en cours d'usage.
   - Statut : `Termine`
   - Resultat attendu : si au moins une prestation du commercant est rattachee a un coffret actif et qu'il existe au moins une coffret instance en cours, le systeme refuse le passage du commercant vers `SUSPENDU` ou `ARCHIVE` et explicite le motif.
   - Resultat attendu : une `coffret instance en cours` est une instance achetee, donc en statut `ACTIVE` ou `EN_ATTENTE_ACTIVATION`.

### Regles de gestion

- Un commercant est cree par defaut au statut `BROUILLON`.
- Le coffret porte un statut distinct du commercant.
- La prestation porte un statut distinct du commercant.
- Un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas avoir de prestations au statut `ACTIVE`, `BROUILLON` ou `REFERENCE`.
- Si au moins une prestation est rattachee a un coffret actif et qu'il existe au moins une coffret instance en cours, il est interdit de suspendre ou d'archiver le commercant concerne.
- Une `coffret instance en cours` est une instance achetee, donc en statut `ACTIVE` ou `EN_ATTENTE_ACTIVATION`.
- Un commercant au statut `BROUILLON` ou `REFERENCE` ne peut pas avoir de coffret actif.
- Un coffret est activable uniquement si le commercant associe est `ACTIF`.

### Decisions produit

- le statut du commercant est defini explicitement avec les etats `BROUILLON`, `REFERENCE`, `ACTIF`, `SUSPENDU`, `ARCHIVE`.
- le statut par defaut d'un commercant a la creation est `BROUILLON`.
- le coffret possede son propre statut metier distinct.
- la prestation possede son propre statut metier distinct.
- les transitions de statut du commercant doivent etre controlees par les dependances catalogue (prestations, coffrets actifs, coffrets instances en cours).
- la notion de `coffret instance en cours` couvre les instances achetees en `ACTIVE` ou `EN_ATTENTE_ACTIVATION`.

---

## Epic 2. Protection de l'integrite des coffrets

- Criticite : `Critique`
- Objectif : empecher qu'une prestation utilisee dans un coffret soit retiree ou invalidee de facon cassante.
- Pourquoi maintenant : c'est une regle d'integrite forte pour eviter les coffrets incoherents et les regressions catalogue.

### User Stories

1. `PRD-004` En tant qu'admin, je ne dois pas pouvoir invalider une prestation tant qu'elle est rattachee a au moins un coffret.


   - Statut : `Termine`
   - Resultat attendu : le systeme bloque l'invalidation et explique dans quels coffrets la prestation est encore utilisee.

2. `PRD-005` En tant qu'admin, je veux visualiser les dependances d'une prestation avant toute action de retrait ou d'invalidation.


   - Statut : `Termine`
   - Resultat attendu : la fiche prestation affiche les coffrets lies pour guider la decision.

3. `PRD-006` En tant qu'admin, je veux d'abord retirer une prestation des coffrets concernes avant de pouvoir l'invalider.


   - Statut : `Termine`
   - Resultat attendu : le workflow de retrait respecte les dependances existantes sans casser l'offre en cours.

4. `PRD-022` En tant qu'admin, je veux invalider une validation de prestation faite par erreur tant que le reversement n'est pas encore paye.
   - Statut : `Termine`
   - Resultat attendu : la prestation repasse a `A_VALIDER`, le mouvement de reversement associe est annule et la `coffret instance` est recalculée.
   - Resultat attendu : l'invalidation est refusee si le reversement associe est deja engage ou paye.
   - Resultat attendu : le montant du reversement associe a une prestation est porte par `PrestationCoffret`.

### Questions produit

- faut-il seulement bloquer l'invalidation ou aussi la suppression ?
- faut-il autoriser une invalidation differree planifiee apres retrait des coffrets ?

### Decisions produit actees

- L'invalidation d'une validation de prestation en erreur est autorisee en V1 uniquement si le reversement associe n'est pas encore paye.
- En V1, l'invalidation est autorisee uniquement si le mouvement de reversement associe est en statut `A_REVERSER`.
- Si le mouvement de reversement est `EN_COURS_DE_REVERSEMENT`, `REVERSE` ou `ANNULE`, l'invalidation est refusee.
- L'invalidation reouvre la prestation en `A_VALIDER`, annule le mouvement de reversement associe et recalcule le statut de la `coffret instance`.
- Une `coffret instance` invalidee partiellement redevient `ACTIVE` si au moins une prestation est de nouveau `A_VALIDER`.
- `PrestationCoffret` porte un `montant_reversement` saisi en gestion, distinct du prix du coffret client.

---

## Epic 3. Workflow de proposition de modification de prestation par le commercant

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre au commercant de proposer une evolution de sa prestation sans impacter le catalogue en production tant qu'elle n'est pas approuvee.
- Pourquoi maintenant : c'est la meilleure maniere d'ouvrir la collaboration commercant sans casser les coffrets existants.

### User Stories

1. `PRD-007` En tant que commercant, je veux proposer une modification de ma prestation sans modifier immediatement la version active.

   - Statut : `Termine`
   - Resultat attendu : la proposition est enregistree comme une demande distincte de la prestation publiee.

2. `PRD-008` En tant qu'admin, je veux relire et accepter ou refuser une proposition de modification de prestation avant qu'elle soit appliquee.

   - Statut : `Termine`
   - Resultat attendu : seule une validation admin rend la modification effective.

3. `PRD-009` En tant qu'utilisateur marketplace, je veux que la prestation actuellement en production reste disponible tant que la proposition n'est pas approuvee.

   - Statut : `Termine`
   - Resultat attendu : aucune rupture de coffret ni de fiche publique pendant la phase de validation.

4. `PRD-010` En tant qu'admin, je veux appliquer une proposition acceptee a la prestation cible de facon tracable.

   - Statut : `Termine`
   - Resultat attendu : historique clair entre version active, proposition, decision et date d'application.

### Questions produit

- une proposition acceptee remplace-t-elle directement la prestation ou cree-t-elle une nouvelle version ?
- quelles modifications sont autorisees : descriptif, prix, image, libelle, disponibilite, conditions ?

---

## Epic 4. Notifications commercant sur achat de coffret

- Criticite : `Moyenne`
- Statut : `Termine`
- Objectif : notifier les commercants participants lorsqu'un coffret est achete, selon leurs preferences.
- Pourquoi plus tard : forte valeur relationnelle et operationnelle, mais moins structurant que les regles d'integrite catalogue.

### User Stories

1. `PRD-011` En tant que commercant, je veux choisir si je souhaite etre notifie lorsqu'un coffret contenant ma prestation est achete.

   - Statut : `Termine`
   - Resultat attendu : chaque commercant peut activer ou desactiver la notification.

2. `PRD-012` En tant que commercant, je veux choisir mon canal de notification prefere entre email et SMS.

   - Statut : `Termine`
   - Resultat attendu : la preference de canal est stockee et exploitee au moment de l'achat.

3. `PRD-013` En tant qu'exploitant, je veux que seuls les commercants participants et opt-in soient notifies lors d'un achat.

   - Statut : `Termine`
   - Resultat attendu : les notifications respectent la composition du coffret et les preferences de contact.

4. `PRD-014` En tant que commercant, je veux recevoir une information utile sur l'achat sans exposer de donnees client non necessaires.

   - Statut : `Termine`
   - Resultat attendu : le contenu de notification reste utile, sobre et conforme.

### Questions produit

- notification a chaque achat ou digest periodique possible ?
- faut-il notifier uniquement a l'achat ou aussi a l'activation / a la consommation ?

---

## Epic 5. Session commercant securisee par QR code

- Criticite : `Critique`
- Statut : `Abandonne`
- Objectif historique : verifier le QR code commercant a l'ouverture de l'application commercant puis etablir une session courte, reutilisable et expirante pour securiser les actions commercant.
- Decision : ne pas implementer ce parcours ; le concept de `qr_commercant` est supprime du produit cible.
- Note produit : le concept de `qr_commercant` est abandonne avant production. Le modele de session, TTL, scopes et revocation reste conserve ; le facteur d'authentification initial devient le login / mot de passe dans l'Epic 10. Aucune migration n'est prevue car il n'existe pas de commercants actifs a migrer.

### User Stories historiques non ciblees

1. `PRD-017` En tant que commercant, je veux verifier ma carte commerçant a l'ouverture de l'application afin de prouver mon identite avant d'acceder aux fonctionnalites protegees.
   - Statut : `Termine`
   - Resultat attendu : le QR commerçant scanne est verifie et refuse s'il est invalide, inactif ou obsolete.
   - Resultat attendu : en cas de succes, le service retourne un resume d'identite du commercant utile a l'initialisation de la session et a l'affichage cote client.

2. `PRD-018` En tant que systeme, je veux creer une session commercant a duree de vie limitee apres verification du QR afin de reutiliser cette authentification sur les actions commercant.
   - Statut : `Termine`
   - Resultat attendu : une session commercant est emise avec un identifiant, un TTL, un lien explicite avec le commercant authentifie et des scopes autorises.

3. `PRD-019` En tant que backend, je veux exiger un ticket de session commercant valide pour les actions commercant sensibles afin de ne plus dependre uniquement du QR a chaque requete.


   - Statut : `Termine`
   - Resultat attendu : les actions commercant protegees refusent toute requete sans session valide ou sans scope autorise pour l'action demandee.

4. `PRD-020` En tant que commercant, je veux etre explicitement informe quand ma session a expire afin de pouvoir rescanner ma carte et rouvrir une session valide.


   - Statut : `Termine`
   - Resultat attendu : une exception metier `Session expiree` est levee lorsque le ticket de session n'est plus valide.

5. `PRD-021` En tant que systeme, je veux distinguer une session invalide d'une session expiree afin de renvoyer une erreur metier precise selon la nature du probleme.


   - Statut : `Termine`
   - Resultat attendu : si le ticket est invalide, le systeme leve une exception metier `Session invalide`.

### Regles de gestion

- Les regles ci-dessous sont conservees comme historique de cadrage de l'Epic 5, mais le parcours QR commercant n'est plus cible.
- Le QR commercant est verifie via un use case dedie, distinct du flux de validation de prestation.
- Une session commercant n'est emise que pour un QR de type `carte_commercant` valide et rattache a une carte active.
- Le ticket de session commercant porte un TTL explicite et une liste de scopes autorises.
- Toute action commercant protegee doit verifier la validite du ticket de session et la presence du scope requis avant execution.
- Si le ticket est expire, le systeme leve une exception metier `Session expiree`.
- Si le ticket est absent, inconnu, mal forme, revoque ou incoherent, le systeme leve une exception metier `Session invalide`.
- La session commercant doit pouvoir etre reutilisee pour des actions telles que validation de prestation, modification du contenu d'une prestation (`libelle`, `description`) et consultation des reversements.
- Chaque API commercant securisee doit declarer ou verifier explicitement le scope attendu.
- La session commercant ne remplace pas la transaction de validation : la transaction reste necessaire pour encadrer le scan d'un QR coffret client et l'acte ponctuel de validation d'une prestation.
- La transaction de validation doit etre ouverte par un commercant deja authentifie via sa session.

### Decisions produit actees

- Le ticket de session recommande en V1 est un `token opaque` aleatoire, persiste cote serveur.
- La premiere iteration utilise des scopes larges par domaine fonctionnel.
- La portee initiale des actions protegees est :
  - validation d'une prestation ;
  - modification du contenu d'une prestation (`libelle`, `description`) ;
  - consultation des reversements a venir ;
  - consultation du detail des reversements deja effectues.
- La strategie de revocation est :
  - revocation automatique a l'expiration du TTL ;
  - revocation forcee suite a deconnexion ;
  - revocation forcee suite a suspension du commercant.

---

## Epic 6. Montant de reversement sur prestation coffret

- Criticite : `Critique`
- Objectif : porter explicitement sur chaque `PrestationCoffret` le montant reverse au commercant afin de calculer correctement les mouvements financiers.
- Pourquoi maintenant : les reversements et les invalidations de validation de prestation doivent s'appuyer sur une source de verite metier stable, distincte du prix client du coffret.

### User Stories

1. `PRD-023` En tant qu'admin, je veux saisir un montant de reversement sur une `PrestationCoffret` afin de definir ce qui doit etre reverse au commercant lors de la consommation.
   - Statut : `Termine`
   - Resultat attendu : chaque `PrestationCoffret` porte un `montant_reversement` saisi en gestion.

2. `PRD-024` En tant que systeme, je veux utiliser le montant de reversement de la `PrestationCoffret` lors de la creation d'un mouvement de reversement afin de ne plus utiliser de montant fixe ou implicite.
   - Statut : `Termine`
   - Resultat attendu : tout `MouvementReversement` issu d'une validation de prestation reprend le `montant_reversement` de la prestation concernee.

3. `PRD-025` En tant qu'admin, je veux que l'invalidation d'une validation de prestation s'appuie sur ce montant de reversement afin de garder une coherence financiere.
   - Statut : `Termine`
   - Resultat attendu : l'invalidation controle et annule un mouvement de reversement base sur le `montant_reversement` de la prestation.

### Regles de gestion

- `PrestationCoffret` porte un `montant_reversement` obligatoire.
- Le `montant_reversement` est obligatoire a la creation d'une `PrestationCoffret`.
- Le `montant_reversement` est saisi en gestion.
- Le `montant_reversement` reste modifiable apres creation.
- Le `montant_reversement` est distinct du prix client du coffret.
- Le `montant_reversement` constitue la source de verite pour les mouvements de reversement lies a la prestation.
- Une prestation activable doit avoir un `montant_reversement` valide.

### Decisions produit actees

- Le `montant_reversement` est porte au niveau `PrestationCoffret`.
- Le montant est exprime en euros cote stockage actuel, avec la meme convention que les montants financiers deja presents.
- Le calcul des reversements ne doit plus reposer sur une valeur codee en dur au moment de la validation de prestation.

---

## Epic 7. Tokens de consultation achat et coffret instance

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : securiser la consultation du detail d'un achat et d'une `CoffretInstance` via des tokens opaques dedies, distincts du QR code metier.
- Pourquoi maintenant : il faut permettre a l'acheteur pro de gerer son achat et au beneficiaire d'une `CoffretInstance` de consulter uniquement son detail, sans exposer l'ensemble de l'achat ni reutiliser le `qr_token`.

### User Stories

1. `PRD-026` En tant qu'acheteur professionnel, je veux consulter le detail d'un achat via un `management_token` dedie afin d'acceder de facon securisee aux informations de gestion de mon achat.
   - Statut : `Termine`
   - Resultat attendu : le detail d'un achat est accessible uniquement avec un `management_token` valide, expire et revocable.

2. `PRD-027` En tant que beneficiaire d'une `CoffretInstance`, je veux consulter le detail de mon coffret via un `consultation_token` dedie afin d'acceder uniquement a mon instance.
   - Statut : `Termine`
   - Resultat attendu : le detail d'une `CoffretInstance` est accessible uniquement avec un `consultation_token` valide, expire et revocable.
   - Resultat attendu : le `consultation_token` permet aussi de consulter le statut des prestations associees a cette `CoffretInstance`.

3. `PRD-028` En tant que systeme, je veux generer et stocker de facon securisee les tokens de consultation achat et coffret instance afin de proteger les acces sans compte utilisateur.
   - Statut : `Termine`
   - Resultat attendu : les tokens bruts ne sont jamais stockes, seul leur hash est persiste avec leurs metadonnees de cycle de vie.

4. `PRD-029` En tant qu'admin, je veux pouvoir revoquer un `consultation_token` de `CoffretInstance` afin de couper un acces devenu indésiré ou obsolete.
   - Statut : `Termine`
   - Resultat attendu : un token revoque ne permet plus la consultation et le motif de revocation peut etre trace.

### Regles de gestion

- Le `management_token` reste porte par `AchatCoffret` et reserve aux usages de gestion de l'achat.
- Le `consultation_token` est porte par `CoffretInstance` et reserve a la consultation d'une seule instance.
- Le `consultation_token` protege la consultation du detail de la `CoffretInstance` et du statut de ses prestations associees.
- Le `qr_token` de consommation d'une `CoffretInstance` ne doit jamais etre reutilise comme token de consultation.
- Les tokens de consultation sont des tokens opaques aleatoires.
- Les tokens bruts ne sont jamais stockes en base ; seul leur hash est persiste.
- Les tokens de consultation portent un TTL explicite et peuvent etre revoques.
- Le `consultation_token` d'une `CoffretInstance` expire a la date d'expiration du coffret achete, majoree d'un nombre de jours configurable.
- Un `consultation_token` de `CoffretInstance` ne doit jamais donner acces aux autres `CoffretInstances` du meme achat.
- Si la `CoffretInstance` est liee a un achat `PARTICULIER`, le detail de consultation peut inclure les informations de l'achat utiles au beneficiaire.
- Si la `CoffretInstance` est liee a un achat `PROFESSIONNEL`, le detail de consultation ne doit pas exposer les informations globales de l'achat.
- Les APIs backend attendent le `consultation_token` et le `management_token` dans l'entete `Authorization`.
- Les liens email de consultation achat et `CoffretInstance` pointent vers le front applicatif avec le token en query param.
- Le front transforme ensuite le token recu en query param en entete `Authorization` lors des appels backend.

### Decisions produit actees

- Le `management_token` reste au niveau `AchatCoffret`.
- Un `consultation_token` dedie est ajoute au niveau `CoffretInstance`.
- La consultation d'une `CoffretInstance` beneficiaire doit etre securisee par ce `consultation_token` et non par le `management_token` achat.
- Les achats particuliers peuvent s'appuyer sur le `consultation_token` de la `CoffretInstance` plutot que sur un token achat dedie si le besoin principal est la consultation de l'instance.
- Le `management_token` et le `consultation_token` sont transportes au backend via l'entete `Authorization`.
- Les liens email pointent vers le front avec le token en query param, puis le front le retransmet au backend via `Authorization`.
- La duree de vie du `consultation_token` est calculee a partir de la date d'expiration de la `CoffretInstance`, augmentee d'un nombre de jours configurable.
- La regeneration d'un `consultation_token` revoque automatiquement l'ancien token, renvoie un nouveau mail de consultation et n'est disponible qu'en administration sur le detail de la `CoffretInstance`.
- Si un `consultation_token` est expire, le message attendu est `Token expire`.
- Si un `consultation_token` est revoque, le message attendu est `Token revoque`.
- Si une `CoffretInstance` issue d'un achat `PROFESSIONNEL` est consultee et que des informations d'achat globales sont demandees, le comportement attendu est de retourner `Information de l'achat non disponible`.

---

## Epic 8. Gestion des contacts et messages support

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : centraliser les demandes de contact consommateurs et commercants afin de traiter les questions marketplace, commandes, coffrets et usages commercants avec un suivi exploitable en back-office.
- Pourquoi maintenant : Localeo doit disposer d'un canal support structure, relie aux objets metier quand une reference est fournie, sans imposer de compte client consommateur ni exposer un portail de suivi public en V1.

### User Stories

1. `PRD-030` En tant que consommateur, je veux envoyer un message de contact depuis la marketplace afin de poser une question a Localeo.
   - Statut : `Termine`
   - Resultat attendu : le consommateur peut envoyer un message avec un email obligatoire, un motif obligatoire issu d'une liste administrable, un telephone optionnel et des references optionnelles d'achat, coffret, coffret instance, prestation ou paiement.
   - Resultat attendu : aucun portail de suivi public n'est expose en V1 ; la reponse se fait par email ou telephone.

2. `PRD-031` En tant que commercant, je veux envoyer un message a Localeo depuis l'application commercant afin de poser une question contextualisee.
   - Statut : `Termine`
   - Resultat attendu : l'API est protegee par une session commercant valide et le scope `commercant:message`.
   - Resultat attendu : le message est automatiquement rattache au `commercant_id` de la session.

3. `PRD-032` En tant qu'admin, je veux consulter les messages de contact dans SQLAdmin afin de les qualifier et suivre leur traitement.
   - Statut : `Termine`
   - Resultat attendu : SQLAdmin affiche les messages, leurs statuts, leurs references metier et leurs metadonnees d'audit.

4. `PRD-033` En tant qu'admin, je veux repondre a un message consommateur afin de preparer une reponse email.
   - Statut : `Termine`
   - Resultat attendu : une reponse admin prepare un email sortant a valider/envoyer via le flux email existant, sans envoi direct synchrone.

5. `PRD-034` En tant qu'admin, je veux repondre a un message commercant afin de poursuivre l'echange dans l'application commercant.
   - Statut : `Termine`
   - Resultat attendu : une reponse admin est ajoutee au fil applicatif visible dans l'application commercant, sans email sortant.

6. `PRD-035` En tant que systeme, je veux notifier le support interne par email a chaque nouveau message afin d'alerter l'equipe Localeo.
   - Statut : `Termine`
   - Resultat attendu : un `EmailSortant` est cree vers `LOCALEO_SUPPORT_CONTACT_EMAIL`, sans envoi direct synchrone.

7. `PRD-036` En tant qu'admin, je veux administrer les motifs de contact afin de piloter les motifs disponibles pour les consommateurs et commercants.
   - Statut : `Termine`
   - Resultat attendu : les motifs sont administrables, activables/desactivables, ordonnables et peuvent cibler consommateurs, commercants ou tous.

8. `PRD-037` En tant que commercant, je veux consulter mes fils de messages afin de suivre les reponses de Localeo.
   - Statut : `Termine`
   - Resultat attendu : un commercant authentifie peut consulter uniquement ses propres fils de discussion.

9. `PRD-038` En tant que commercant, je veux repondre dans un fil existant afin de poursuivre l'echange avec Localeo.
   - Statut : `Termine`
   - Resultat attendu : une reponse commercant cree un nouveau message dans le meme fil et repasse le fil en `NON_LU` cote admin.

10. `PRD-039` En tant qu'admin, je veux gerer les statuts de lecture et de traitement afin de piloter les demandes support.
   - Statut : `Termine`
   - Resultat attendu : les statuts `NON_LU`, `LU`, `OUVERT`, `EN_COURS`, `REPONDU`, `CLOTURE` sont exploitables en gestion.

### Regles de gestion

- Un message consommateur exige un `email_contact` valide.
- Le `telephone_contact` consommateur est optionnel.
- Le motif est obligatoire pour les consommateurs et les commercants.
- Les motifs sont portes par une liste administrable `MotifContact`, incluant un motif `AUTRE`.
- Un message consommateur peut porter une reference optionnelle d'achat, de coffret, de coffret instance, de prestation ou de paiement.
- Le consommateur ne dispose pas d'un suivi par lien ou token en V1.
- La reponse consommateur se fait uniquement par email ou telephone.
- La reponse commercant se fait uniquement via le fil de messages visible dans l'application commercant.
- Un message commercant exige une session commercant valide.
- Le scope commercant dedie est `commercant:message`.
- Un message commercant est toujours rattache au `commercant_id` de la session.
- Les messages commercants sont organises en fils de discussion consultables par le commercant concerne.
- Le premier message d'un fil de discussion est identifiable explicitement via `thread_root_message_id`.
- Le motif commercant est obligatoire et selectionne dans une liste configurable incluant `AUTRE`.
- Les statuts de lecture sont differencies cote admin et cote commercant.
- Le support interne est notifie par email a chaque nouveau message.
- L'adresse support est configuree par `LOCALEO_SUPPORT_CONTACT_EMAIL` et la notification cree un `EmailSortant`.
- Une reponse admin a un message consommateur ne part pas automatiquement : elle prepare un email sortant a valider/envoyer via le flux email existant.
- Une reponse admin a un message commercant n'envoie pas d'email : elle cree une reponse dans le fil applicatif.
- Les pieces jointes sont hors perimetre V1.
- Chaque message porte des metadonnees d'audit : source, date de creation, acteur, IP et user-agent quand disponibles.
- Le createur d'un message est type par le referentiel `ANONYME`, `COMMERCANT`, `LOCALEO`.
- Si une reference optionnelle est fournie et introuvable, la creation du message est refusee.

### Decisions produit actees

- L'email est obligatoire pour les messages consommateurs.
- Le motif est obligatoire pour tous les messages et provient d'une liste administrable.
- Le consommateur ne peut pas consulter de suivi via lien/token en V1.
- Le scope `commercant:message` est cree pour les usages messagerie commercant.
- Les reponses admin aux consommateurs preparent un email sortant, sans envoi direct automatique.
- Les reponses admin aux commercants restent dans le fil applicatif et n'utilisent pas l'email.
- La notification support interne utilise `LOCALEO_SUPPORT_CONTACT_EMAIL` et cree un `EmailSortant`.
- Les pieces jointes ne sont pas gerees en V1.
- Aucun champ `priorite` n'est ajoute en V1.
- La politique de retention est hors perimetre V1 et sera instruite plus tard.

---

## Epic 9. Mode secours telephonique pour l'honorisation d'une prestation

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre a un commercant d'honorer exceptionnellement une prestation via le support Localeo lorsqu'il ne peut pas utiliser son espace, le parcours QR client ou son reseau local.
- Pourquoi maintenant : sans procedure outillee, une indisponibilite technique peut bloquer une prestation legitime ou conduire a des validations manuelles non tracees.

### User Stories

1. `PRD-040` En tant que systeme, je veux generer un `verification_code` unique pour chaque `CoffretInstance` afin de permettre son identification a distance.
   - Statut : `Termine`
   - Resultat attendu : chaque `CoffretInstance` dispose d'un code court, lisible a l'oral, unique et searchable en back-office.

2. `PRD-041` En tant qu'operateur support, je veux retrouver une `CoffretInstance` a partir d'un `verification_code` dicte au telephone afin d'instruire rapidement une demande de secours.
   - Statut : `Termine`
   - Resultat attendu : le back-office permet une recherche directe sur `verification_code` avec affichage du statut et de la validite de l'instance.

3. `PRD-042` En tant qu'operateur support, je veux verifier l'identite du commercant appelant avec une procedure minimale afin de limiter les usages abusifs du mode secours.
   - Statut : `Termine`
   - Resultat attendu : l'operateur controle plusieurs informations commercant issues du dossier, sans carte ni QR commercant, et consigne ce controle dans une trace d'audit.

4. `PRD-043` En tant qu'operateur support, je veux autoriser ou refuser une prestation en mode secours apres verification afin de traiter les incidents sans sortir du cadre operatoire.
   - Statut : `Termine`
   - Resultat attendu : une decision `AUTORISE`, `REFUSE` ou `A_CONTROLER` est enregistree avec motif, operateur et prestation cible explicite.

5. `PRD-044` En tant qu'administrateur, je veux disposer d'un historique des validations secours afin d'auditer ces usages exceptionnels.
   - Statut : `Termine`
   - Resultat attendu : les decisions du mode secours sont historisees et distinguables des validations nominales.

6. `PRD-045` En tant qu'exploitant, je veux documenter la procedure de secours pour le commercant et le support afin d'uniformiser la gestion des incidents.
   - Statut : `Termine`
   - Resultat attendu : une procedure claire, documentee et exploitable existe pour chaque acteur.

### Regles de gestion

- Le mode secours est reserve aux situations exceptionnelles d'indisponibilite ou d'incident declare.
- Une `CoffretInstance` porte un `verification_code` dedie, court, unique et lisible a l'oral.
- Le `verification_code` sert a identifier une `CoffretInstance` mais n'est pas un secret.
- L'identification du commercant repose sur plusieurs informations de verification, pas sur un seul element.
- Aucun element issu de la carte, du QR ou du concept `qr_commercant` n'est utilise pour identifier le commercant.
- Une decision `AUTORISE` cible explicitement un `statut_prestation_coffret_instance_id` et passe par un use case dedie de mode secours.
- Une decision `REFUSE` ou `A_CONTROLER` ne produit aucun effet de consommation.
- Une decision en mode secours est toujours tracee avec operateur, motif, `CoffretInstance` et resume de verification commercant.
- En cas de doute, la decision par defaut est `REFUSE` ou `A_CONTROLER`.

### Decisions produit actees

- Le mode retenu en V1 est un mode secours telephonique assiste par le support Localeo.
- Le support utilise un `verification_code` porte par la `CoffretInstance` pour retrouver le coffret sans scan.
- Le mode secours couvre les incidents cote commercant, parcours QR client ou reseau local, pas une indisponibilite totale du backend Localeo.
- Les validations secours sont auditees dans un journal dedie.

---

## Epic 10. Authentification commercant par login / mot de passe

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : remplacer l'authentification initiale du commercant par QR code par une authentification login / mot de passe, avec mot de passe oublie et mise a jour du mot de passe.
- Pourquoi maintenant : l'application etant encore en phase de developpement, le concept de `qr_commercant` peut etre decommissionne totalement sans procedure de migration.
- Backlog detaille : [docs/roadmap/terminees/epic-10-authentification-commercant-login-password-backlog.md](terminees/epic-10-authentification-commercant-login-password-backlog.md)

### User Stories

1. `PRD-046` En tant que commercant, je veux me connecter avec mon login et mon mot de passe afin d'acceder a mon espace sans scanner de QR commercant.
   - Statut : `Termine`
   - Resultat attendu : un commercant `ACTIF` peut ouvrir une session commercant avec un login et un mot de passe valides.
   - Resultat attendu : la session emise conserve le contrat actuel `session_token`, `expires_at`, `scopes` et resume commercant.
   - Resultat attendu : le hash du mot de passe utilise `bcrypt`.

2. `PRD-047` En tant que commercant, je veux demander une reinitialisation de mot de passe lorsque je l'ai oublie afin de recuperer mon acces sans support.
   - Statut : `Termine`
   - Resultat attendu : une demande de mot de passe oublie prepare un email de reinitialisation via l'outbox, sans permettre d'enumerer les logins existants.

3. `PRD-048` En tant que commercant, je veux definir un nouveau mot de passe depuis un lien de reinitialisation afin de finaliser la recuperation de mon compte.
   - Statut : `Termine`
   - Resultat attendu : un token opaque, expire et a usage unique permet de definir un nouveau mot de passe.
   - Resultat attendu : les sessions existantes du commercant sont revoquees apres reinitialisation.

4. `PRD-048A` En tant que nouveau commercant, je veux initialiser mon premier mot de passe depuis un lien afin d'activer mon acces sans mot de passe temporaire.
   - Statut : `Termine`
   - Resultat attendu : un lien d'initialisation opaque, expire et a usage unique permet de definir le premier mot de passe.

5. `PRD-049` En tant que commercant connecte, je veux mettre a jour mon mot de passe afin de maintenir la securite de mon acces.
   - Statut : `Termine`
   - Resultat attendu : la mise a jour exige une session valide, le mot de passe courant et un nouveau mot de passe conforme.
   - Resultat attendu : toutes les sessions commercant sont revoquees apres changement.

6. `PRD-050` En tant qu'exploitant, je veux decommissionner le `qr_commercant` afin de ne conserver que le login / mot de passe pour l'acces applicatif commercant.
   - Statut : `Termine`
   - Resultat attendu : les nouveaux commercants disposent d'un identifiant d'acces unique et d'un lien d'initialisation.
   - Resultat attendu : le QR commercant, ses endpoints et ses cartes associees sont retires du produit cible, sans impact sur le QR coffret client.

### Regles de gestion

- Le login commercant est unique.
- L'identifiant recommande en V1 est l'email de contact du commercant, normalise en minuscules.
- Le mot de passe brut n'est jamais stocke ni journalise.
- Le hash de mot de passe utilise `bcrypt`.
- Une authentification reussie cree une session commercant opaque, avec TTL et scopes, selon le mecanisme existant.
- Un commercant `SUSPENDU` ou `ARCHIVE` ne peut pas ouvrir de nouvelle session.
- Le mot de passe oublie renvoie une reponse generique, que le login existe ou non.
- Les tokens d'initialisation et de reinitialisation sont opaques, hashes en base, expirables et a usage unique.
- La mise a jour ou reinitialisation du mot de passe revoque toutes les sessions existantes du commercant.
- L'onboarding commercant utilise un lien d'initialisation, sans mot de passe temporaire.
- Le rate limiting du login et du mot de passe oublie est applicatif.
- Les actions commercant protegees restent controlees par `Authorization: Bearer <session_token>` et par les scopes.
- Le QR coffret client reste utilise pour la validation terrain d'une `CoffretInstance`.
- Aucune procedure de migration QR commercant vers login / mot de passe n'est prevue.

### Decisions produit actees

- Hashage des mots de passe : `bcrypt`.
- Cout bcrypt : `LOCALEO_BCRYPT_ROUNDS=12`.
- Politique mot de passe : 12 caracteres minimum, rejet du login/email et d'une denylist locale minimale de mots de passe faibles, enrichissable ensuite.
- Duree des liens : maximum acceptable 24h ; initialisation 24h, reinitialisation 1h en valeur recommandee.
- Changement ou reinitialisation de mot de passe : revocation de toutes les sessions.
- Decommissionnement QR commercant : suppression complete.
- Onboarding commercant : lien d'initialisation.
- Back-office : voir etat d'acces, envoyer lien d'initialisation, reinitialiser, verrouiller, deverrouiller.
- Rate limiting : applicatif, stocke dans une table dediee, 5 echecs login / 15 minutes / login + IP et 5 demandes reset / 15 minutes / login + IP.
- Verrouillage compte : 5 echecs consecutifs, deverrouillage admin uniquement en V1.
- Audit : `auth.login.success`, `auth.login.failed`, `password.reset.requested`, `password.reset.succeeded`, `password.init.requested`, `password.init.succeeded`, `auth.login.updated`, `account.locked`, `account.unlocked`.

---

## Epic 11. Espace commercant et informations contact

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : permettre au commercant authentifie de consulter ses informations de commerce et de contact, puis de mettre a jour les donnees de contact autorisees.
- Pourquoi maintenant : l'Epic 10 introduit un espace commercant authentifie ; il devient naturel de donner au commercant un minimum d'autonomie sur ses informations operationnelles.
- Backlog detaille : [docs/roadmap/terminees/epic-11-espace-commercant-informations-contact-backlog.md](terminees/epic-11-espace-commercant-informations-contact-backlog.md)

### User Stories

1. `PRD-051` En tant que commercant authentifie, je veux consulter mon profil commercant afin de verifier les informations connues par Localeo.
   - Statut : `Termine`
   - Resultat attendu : `GET /commercants/me` retourne uniquement les informations du commercant rattache a la session.

2. `PRD-052` En tant que commercant authentifie, je veux modifier mes informations de contact afin de garder mes donnees operationnelles a jour.
   - Statut : `Termine`
   - Resultat attendu : `PATCH /commercants/me/contact` permet de modifier les champs autorises sans exposer de donnees d'authentification.

3. `PRD-053` En tant qu'exploitant, je veux encadrer les modifications sensibles afin de proteger le catalogue, le login et les donnees de referencement.
   - Statut : `Termine`
   - Resultat attendu : les champs sensibles ne sont pas modifiables par le commercant en V1 et restent controles par le back-office.

4. `PRD-054` En tant qu'exploitant, je veux auditer les consultations et modifications du profil commercant afin de faciliter le support et les controles.
   - Statut : `Termine`
   - Resultat attendu : les actions `merchant.profile.viewed` et `merchant.contact.updated` sont tracees sans secret.

### Regles de gestion

- Le profil consulte est toujours celui du commercant rattache a la session.
- Le `commercant_id` ne doit jamais venir du corps de requete pour les endpoints `/commercants/me`.
- Les champs directement modifiables en V1 sont les donnees de contact operationnelles.
- Le `contact_email` n'est pas modifiable par le commercant en V1.
- Les champs structurants `nom`, `ville_id`, `type_commercant_id`, `image_uri` et `statut` restent controles par le back-office en V1.
- La `description` reste controlee par le back-office en V1.
- Les modifications sont auditees.

### Decisions actees

- Les informations sensibles ne sont pas modifiables par le commercant en V1.
- Aucun workflow de proposition de modification n'est prevu en V1.
- La consultation du profil reste autorisee pour un commercant `SUSPENDU` disposant encore d'une session valide.
- La modification des contacts est refusee pour un commercant `SUSPENDU` ou `ARCHIVE`.
- Aucune notification support/admin n'est envoyee lors d'une modification de contact.
- Aucun email de confirmation n'est envoye au commercant apres modification.

---

## Epic 12. Traitement des reversements et export des paiements

- Criticite : `Haute`
- Statut : `Abandonne`
- Objectif historique : permettre a l'exploitation de prendre les `Reversement` prets, generer les `PaiementReversement` associes, exporter un fichier exploitable pour un paiement manuel en banque et confirmer ensuite l'execution. Cette cible est remplacee par l'EPIC 39 : les nouveaux flux conservent `PaiementReversement`, mais son execution est alimentee exclusivement par Stripe Connect, sans export bancaire manuel, fallback manuel ni retrocompatibilite operationnelle.
- Pourquoi maintenant : le socle de reversement existe deja, mais il manque le traitement operationnel du dernier kilometre pour passer des mouvements prepares a des paiements reels et tracables.
- Backlog detaille : [docs/roadmap/abandonnees/epic-12-traitement-reversements-export-paiements-backlog.md](abandonnees/epic-12-traitement-reversements-export-paiements-backlog.md)

### User Stories

1. `PRD-055` En tant qu'operateur exploitation, je veux lister les `Reversement` eligibles au paiement afin d'identifier rapidement les reversements traitables.
   - Statut : `Termine`
   - Resultat attendu : le back-office expose les reversements `EN_PREPARATION` avec compte connecte Stripe eligible, montant total et nombre de lignes.

2. `PRD-056` En tant qu'operateur exploitation, je veux generer les `PaiementReversement` a initier afin de figer les paiements a traiter sans risque de doublon.
   - Statut : `Termine`
   - Resultat attendu : chaque reversement selectionne produit un paiement `A_INITIER`, rattache a son reversement et idempotent.

3. `PRD-057` En tant qu'operateur exploitation, je veux exporter un lot de paiements en `CSV` afin de saisir ou importer facilement les virements dans ma banque.
   - Statut : `Termine`
   - Resultat attendu : un fichier exportable contient les informations bancaires et montants necessaires pour chaque paiement.

4. `PRD-058` En tant qu'operateur exploitation, je veux confirmer l'execution manuelle d'un paiement de reversement afin d'aligner le systeme avec les virements reels.
   - Statut : `Termine`
   - Resultat attendu : le paiement passe a `EXECUTE`, le reversement a `PAYE` et ses mouvements a `REVERSE` apres confirmation.

5. `PRD-059 bis` En tant que commercant, je veux etre notifie lorsqu'un paiement de reversement est valide afin de savoir qu'un virement va m'etre verse.
   - Statut : `Termine`
   - Resultat attendu : la notification est declenchee uniquement apres confirmation `EXECUTE` du paiement, sans doublon en cas de rejeu.
   - Resultat attendu : le message indique le montant, la reference de paiement si disponible et la date de confirmation, sans exposer de donnees client ni de detail bancaire complet.

6. `PRD-059` En tant qu'exploitant, je veux tracer les echecs ou incidents de paiement de reversement afin de reprendre proprement le traitement.
   - Statut : `Termine`
   - Resultat attendu : un paiement peut etre marque `ECHEC` avec un motif sans perdre la tracabilite.

### Regles de gestion

- Un `Reversement` n'est eligible au paiement que s'il est en statut `EN_PREPARATION`.
- Le mode V1 `MANUEL_BANQUE` est historique et decommissionne par l'EPIC 39.
- Le systeme cible ne doit plus generer de paiement manuel avant execution bancaire effective.
- Le format d'export V1 `CSV` n'est plus un livrable operationnel cible.
- Le passage a `PAYE` doit etre derive des operations Stripe Connect et de leur synchronisation.
- Un meme `Reversement` ne doit jamais donner lieu a un double paiement actif.
- Les etapes de preparation, export, execution et echec sont auditees.

### Decisions actees

- Le dernier kilometre de paiement des reversements est traite par Stripe Connect.
- Les lots d'export bancaire manuel sont decommissionnes.
- La tracabilite cible repose sur les references Stripe, les campagnes bimensuelles, les webhooks et l'audit applicatif.
- Decision EPIC 39 : le mode manuel banque est decommissionne pour les nouveaux flux ; les objets restent, mais sont requalifies autour des operations Stripe.

---

## Epic 13. Generation des reversements commercants

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : permettre a l exploitation de generer des `Reversement` coherents a partir des `MouvementReversement` en attente, avant toute phase de paiement. Cette cible devient historique avec l'EPIC 39 : les nouveaux flux conservent `MouvementReversement` et `Reversement`, mais leur execution donne lieu a des transfers Stripe.
- Pourquoi maintenant : la chaine financiere est plus lisible et mieux pilotable si la preparation des reversements est explicite et distincte de leur paiement.
- Backlog detaille : [docs/roadmap/terminees/epic-13-generation-reversements-commercants-backlog.md](terminees/epic-13-generation-reversements-commercants-backlog.md)

### User Stories

1. `PRD-060` En tant qu operateur exploitation, je veux lister les mouvements eligibles au reversement afin d identifier ce qui peut etre agrege.
   - Statut : `Termine`
   - Resultat attendu : les mouvements `A_REVERSER` sont visibles, regroupables par commercant et totalisables.

2. `PRD-061` En tant qu operateur exploitation, je veux generer un reversement pour un commercant afin de preparer une unite payable coherente.
   - Statut : `Termine`
   - Resultat attendu : un `Reversement` en `EN_PREPARATION` et ses `LigneReversement` sont crees, puis les mouvements passent en `EN_COURS_DE_REVERSEMENT`.

3. `PRD-062` En tant qu operateur exploitation, je veux generer les reversements en lot pour plusieurs commercants afin d accelerer la preparation financiere.
   - Statut : `Termine`
   - Resultat attendu : plusieurs reversements peuvent etre crees en une operation, un par commercant.

4. `PRD-063` En tant qu exploitant, je veux garantir l idempotence de la generation afin d eviter les doublons de reversement.
   - Statut : `Termine`
   - Resultat attendu : un mouvement deja rattache a un reversement ne peut pas etre regroupe une seconde fois.

5. `PRD-064` En tant qu exploitant, je veux auditer la generation des reversements afin de tracer la preparation financiere.
   - Statut : `Termine`
   - Resultat attendu : les generations reussies et les echecs sont traces.

### Regles de gestion

- La generation des reversements est distincte du paiement des reversements.
- Un reversement est genere par commercant.
- Dans la cible EPIC 39, l'eligibilite au transfer repose sur le compte connecte Stripe et ses capacites, plus sur un compte bancaire gere par Localeo.
- Le reversement cree passe en `EN_PREPARATION`.
- Les mouvements integres passent en `EN_COURS_DE_REVERSEMENT`.
- L Epic 13 alimentait historiquement l Epic 12 ; dans la cible EPIC 39, elle alimente les campagnes Stripe Connect.

### Decisions actees

- La preparation des reversements est un maillon metier explicite.
- `CreerReversementCommercant` devient le coeur fonctionnel de cette etape.
- La generation en lot multi commercants est dans le perimetre V1.
- Decision EPIC 39 : la generation interne reste possible comme projection metier, mais l'execution manuelle banque est remplacee par Stripe Connect.

---

## Epic 14. Documents d'achat et facturation du coffret

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : generer un recu de paiement a l'achat puis permettre la generation a la demande des documents fiscaux sous-jacents d'un coffret multi commercants.
- Pourquoi maintenant : le modele d'intermediation Localeo impose de distinguer clairement recu client, factures commercants et facture Localeo pour rester coherent juridiquement et operable.
- Backlog detaille : [docs/roadmap/terminees/epic-14-documents-achat-et-facturation-coffret-backlog.md](terminees/epic-14-documents-achat-et-facturation-coffret-backlog.md)

### User Stories

1. `PRD-065` En tant que client, je veux recevoir un recu de paiement a l'achat afin d'avoir un justificatif immediat.
   - Statut : `Termine`
   - Resultat attendu : un recu PDF simple est genere des validation du paiement et rattache a la `CoffretInstance`.

2. `PRD-066` En tant que client, je veux que le mail d'envoi du QR code m'indique comment demander mes factures afin de savoir quoi faire sans surcharge documentaire immediate.
   - Statut : `Termine`
   - Resultat attendu : le recu est joint au mail et le pied du mail oriente vers le formulaire de contact avec la reference d'achat.

3. `PRD-067` En tant qu'operateur back-office, je veux generer le pack facture d'un coffret paye afin de produire les documents fiscaux detaillees sur demande.
   - Statut : `Termine`
   - Resultat attendu : le systeme produit une facture par prestation commercant et une facture Localeo de frais de service, assemblees dans un `ZIP`.

4. `PRD-068` En tant qu'operateur back-office, je veux lancer cette generation depuis la fiche de la `CoffretInstance` afin de traiter rapidement les demandes client.
   - Statut : `Termine`
   - Resultat attendu : une action dediee apparait uniquement si le paiement est valide.

5. `PRD-069` En tant qu'exploitant, je veux auditer la generation des documents afin de tracer qui a emis quoi et quand.
   - Statut : `Termine`
   - Resultat attendu : la generation du recu et du pack facture produit des evenements d'audit dedies.

6. `PRD-070` En tant que systeme, je veux faire apparaitre la TVA Localeo uniquement lorsqu'elle est applicable afin d'emettre une facture Localeo correcte.
   - Statut : `Termine`
   - Resultat attendu : le traitement TVA est fige a l'achat et restitue a l'identique a chaque regeneration.

7. `PRD-071` En tant que systeme, je veux mentionner le mandat de facturation Localeo sur les factures commercants afin de rendre explicite le role de Localeo.
   - Statut : `Termine`
   - Resultat attendu : chaque facture commercant comporte une mention homogene "au nom et pour le compte".

8. `PRD-072` En tant qu'exploitant, je veux collecter les donnees de facturation via le formulaire de contact afin de completer les informations client strictement necessaires a l'emission documentaire.
   - Statut : `Termine`
   - Resultat attendu : un motif `demande de facturation` ajoute les champs `nom`, `prenom` et `adresse de facturation`, rattaches a la reference d'achat.

9. `PRD-073` En tant qu'operateur back-office, je veux annuler une `CoffretInstance` avant consommation afin de tracer un remboursement hors systeme et fiabiliser le traitement client.
   - Statut : `Termine`
   - Resultat attendu : l'action d'annulation est disponible depuis la fiche de la `CoffretInstance`, avec affichage des informations de paiement utiles et audit dedie.

### Decisions actees

- Le recu de paiement est le seul document envoye automatiquement au client a l'achat.
- Les factures detaillees restent generees a la demande depuis le back-office en V1.
- Le pack facture assemble les factures dans un `ZIP`.
- La facture Localeo porte uniquement les frais de service.
- Les factures commercants portent la mention de mandat de facturation Localeo.
- La collecte des donnees de facturation client se fait via le formulaire de contact en V1.
- L'annulation d'une `CoffretInstance` avant consommation est tracee depuis le back-office.
- Un coffret ne peut pas etre partiellement rembourse : l'annulation/remboursement porte sur le coffret ou l'instance entiere avant consommation.
- L'annulation invalide la `CoffretInstance` et les prestations associees encore non consommees.

---

## Epic 20. Gestion des remboursements

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : gerer de bout en bout les remboursements lies a l'annulation d'un coffret paye, avec une tracabilite exploitable par le support et le back-office.
- Pourquoi maintenant : l'annulation d'un coffret paye cree une obligation financiere client ; sans workflow dedie, le back-office peut annuler l'usage sans garantir le suivi du remboursement.
- Backlog detaille : [docs/roadmap/terminees/epic-20-gestion-remboursements-backlog.md](terminees/epic-20-gestion-remboursements-backlog.md)

### User Stories

1. `PRD-105` En tant qu'operateur back-office, je veux qu'une annulation de coffret paye cree un remboursement a traiter afin de ne pas perdre le suivi financier client.
   - Statut : `Termine`
   - Resultat attendu : si le paiement est valide, l'annulation cree un remboursement en statut `A_TRAITER`.
   - Resultat attendu : si le paiement n'est pas valide, aucun remboursement financier n'est cree.

2. `PRD-106` En tant qu'operateur back-office, je veux suivre le statut d'un remboursement afin de savoir s'il est a traiter, en cours, execute, annule, refuse ou en echec.
   - Statut : `Termine`
   - Resultat attendu : les statuts cibles sont `A_TRAITER`, `EN_COURS`, `REMBOURSE`, `ANNULE`, `REFUSE`, `ECHEC`.
   - Resultat attendu : `ANNULE` designe une demande devenue non executable lors du controle final, tandis que `REFUSE` reste une decision operateur.

3. `PRD-107` En tant que systeme, je veux interdire les remboursements partiels afin de respecter la regle produit du coffret indivisible.
   - Statut : `Termine`
   - Resultat attendu : le montant rembourse correspond toujours au montant client du coffret ou de l'instance ciblee.

4. `PRD-108` En tant que support Localeo, je veux voir le remboursement rattache a l'achat, au paiement et a la `CoffretInstance` afin de repondre rapidement a un client.
   - Statut : `Termine`
   - Resultat attendu : la fiche achat et la fiche `CoffretInstance` affichent le statut de remboursement, le montant, le motif et la reference externe.

5. `PRD-109` En tant qu'operateur back-office, je veux marquer un remboursement externe comme execute afin de tracer les remboursements faits hors systeme.
   - Statut : `Termine`
   - Resultat attendu : l'operateur renseigne une reference externe obligatoire et une date d'execution.
   - Resultat attendu : le client recoit un email automatique de confirmation du remboursement execute.
   - Resultat attendu : le passage a `REMBOURSE` invalide la `CoffretInstance` et rend les prestations restantes inutilisables.

6. `PRD-110` En tant que systeme, je veux annuler automatiquement une demande de remboursement devenue non eligible afin d'eviter une perte financiere et une incoherence avec les reversements.
   - Statut : `Termine`
   - Resultat attendu : l'eligibilite est recontrolee juste avant le passage a `REMBOURSE`.
   - Resultat attendu : si la `CoffretInstance` est expiree ou si au moins une prestation associee est `VALIDEE`, la demande passe a `ANNULE` avec motif trace.
   - Resultat attendu : une demande `ANNULE` ou `REFUSE` ne peut plus etre marquee `REMBOURSE`.
   - Resultat attendu : aucun reversement partiel n'est cree pour compenser une annulation tardive.

7. `PRD-111` En tant qu'exploitant, je veux piloter les remboursements a traiter afin de ne pas laisser de dossiers clients sans action.
   - Statut : `Termine`
   - Resultat attendu : le dashboard back-office affiche les remboursements `A_TRAITER` et `ECHEC`.

8. `PRD-123` En tant que client, je veux recevoir un email lors de l'annulation de mon coffret afin de comprendre que le coffret n'est plus utilisable.
   - Statut : `Termine`
   - Resultat attendu : l'email indique la reference d'achat, la `CoffretInstance` annulee et le statut du remboursement si applicable.

9. `PRD-124` En tant que client, je veux recevoir un email lorsque le remboursement est execute afin d'avoir une confirmation de traitement.
   - Statut : `Termine`
   - Resultat attendu : l'email indique la reference d'achat, la date d'execution et la reference externe du remboursement si disponible.

### Decisions produit actees

- Un coffret ne peut pas etre partiellement rembourse.
- La granularite B2B du remboursement est la `CoffretInstance`.
- Si l'annulation concerne un paiement valide, le systeme doit creer ou suivre une obligation de remboursement.
- L'annulation invalide la `CoffretInstance` et les prestations associees encore non consommees.
- Le remboursement MVP est uniquement manuel / hors systeme, mais il doit etre represente par un objet metier auditable.
- Le montant du remboursement doit etre calcule par le backend, pas saisi librement par un operateur.
- Le client recoit un email automatique lors de l'annulation et lors du remboursement execute.
- La comptabilite MVP se limite a une trace operationnelle auditable, sans generation d'avoir comptable.
- Aucun reversement partiel n'est gere ; si une prestation est consommee ou deja reversee, le remboursement standard est refuse en MVP.
- Le passage a `REMBOURSE` rend la `CoffretInstance` inutilisable et passe les prestations restantes non consommees a `ANNULEE`.
- L'eligibilite est recontrolee au moment de l'execution : instance expiree, deja utilisee, deja annulee, non remboursable ou prestation `VALIDEE` entrainent le passage de la demande a `ANNULE` avec motif trace.

---

## Epic 21. Expiration automatique des coffrets

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : fournir un batch operable qui expire automatiquement les `CoffretInstance` arrivees a echeance et un batch separe de relance email avant expiration.
- Pourquoi maintenant : sans materialisation automatique de l'expiration, des coffrets expires peuvent rester visibles comme consommables, fausser l'encours commercant et compliquer le support ; sans relance preventive, Localeo augmente le risque de coffrets non consommes et de demandes support tardives.
- Backlog detaille : [docs/roadmap/terminees/epic-21-expiration-automatique-coffrets-backlog.md](terminees/epic-21-expiration-automatique-coffrets-backlog.md)

### User Stories

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

5. `PRD-116` En tant que support Localeo, je veux voir qu'une instance ou une prestation a expire automatiquement afin d'expliquer le statut a un client ou un commercant.
   - Statut : `Termine`
   - Resultat attendu : une trace d'audit indique date d'execution, operateur/systeme, nombre d'instances expirees et nombre de prestations expirees.

6. `PRD-116B` En tant que systeme, je veux relancer automatiquement par email les beneficiaires dont le coffret expire dans `N` jours afin de reduire les coffrets non consommes.
   - Statut : `Termine`
   - Resultat attendu : un batch separe cree un email outbox pour les `CoffretInstance` eligibles.
   - Resultat attendu : `N` est configurable par exploitation, avec une valeur par defaut MVP de 7 jours.
   - Resultat attendu : la relance est idempotente par instance, date d'expiration et `N`.

7. `PRD-116C` En tant que support admin, je veux prolonger manuellement une `CoffretInstance` expiree afin de traiter un geste commercial ou un incident support.
   - Statut : `Termine`
   - Resultat attendu : seul un admin peut prolonger une instance.
   - Resultat attendu : le nombre de jours de prolongation est saisi depuis le back-office.
   - Resultat attendu : une instance expiree redevient `ACTIVE` si elle avait deja ete activee, sinon `EN_ATTENTE_ACTIVATION`.

### Decisions produit a cadrer

- Une `CoffretInstance` est eligible si `date_expiration < now`.
- Le statut `CoffretInstance` cible reste `EXPIRE`; aucune migration vers `EXPIREE` n'est prevue pour les instances.
- Les statuts d'instance expirables sont `ACTIVE` et `EN_ATTENTE_ACTIVATION`.
- Les prestations restantes `A_VALIDER` passent en `EXPIREE`.
- Les prestations deja `VALIDEE`, `ANNULEE` ou `EXPIREE` ne sont pas modifiees.
- Le batch doit etre idempotent, relancable et auditable.
- Le MVP doit proposer un `dry_run` pour exploitation.
- La frequence cible du batch d'expiration en MVP est le declenchement manuel via API batch.
- Le batch de relance avant expiration est separe du batch d'expiration.
- La valeur par defaut de `N` est 7 jours.
- La fenetre de relance est de 48 heures, soit `[now + 7 jours ; now + 7 jours + 48h]` par defaut.
- La frequence cible du batch de relance en MVP est le declenchement manuel via API batch.
- Le batch de relance cree des emails dans l'outbox ; l'envoi reste porte par le batch email existant.
- L'idempotence des emails de relance et d'information a expiration repose sur `relances_expiration_coffrets`.
- Le scope `internal:batch` existe deja et protege les routes batch.
- Les routes batch sont exposees sous `/protected`, conformement aux batchs existants.
- Le client recoit un email de relance avant expiration et un email d'information a expiration.
- Le support peut prolonger manuellement une `CoffretInstance` apres expiration.
- La prolongation support est reservee aux admins, avec saisie du nombre de jours dans le back-office.
- Apres prolongation, toutes les prestations `EXPIREE` rattachees a l'instance redeviennent `A_VALIDER`.
- Les batchs supportent `dry_run`.
- Le lancement MVP se fait par API batch uniquement, sans action UI de lancement dans le back-office.
- Les emails MVP utilisent des templates HTML dedies via `ServicePreparationEmail`.
- Les tests MVP sont des verifications manuelles.

---

## Epic 22. Timeline support achat et coffret

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir une vue support chronologique permettant de reconstituer l'histoire complete d'un achat, d'une `CoffretInstance`, d'un paiement, d'un email, d'un SMS ou d'une validation de prestation.
- Pourquoi maintenant : les logs correles et les audits existent partiellement, mais le support a besoin d'une vue metier consolidee pour diagnostiquer rapidement les cas client au lancement.
- Backlog detaille : [docs/roadmap/terminees/epic-22-timeline-support-backlog.md](terminees/epic-22-timeline-support-backlog.md)

### User Stories

1. `PRD-117` En tant que support Localeo, je veux consulter la timeline d'un achat afin de comprendre rapidement tout le parcours client.
   - Statut : `Termine`
   - Resultat attendu : la timeline affiche les evenements de l'achat dans l'ordre chronologique.

2. `PRD-118` En tant que support Localeo, je veux consulter la timeline d'une `CoffretInstance` afin de comprendre son activation, son usage, son expiration ou son annulation.
   - Statut : `Termine`
   - Resultat attendu : la timeline affiche creation, activation, validation de prestation, annulation et expiration si disponibles.

3. `PRD-119` En tant que support Localeo, je veux voir les emails et SMS rattaches a un achat afin de repondre aux cas "je n'ai rien recu".
   - Statut : `Termine`
   - Resultat attendu : la timeline affiche les emails et SMS avec destinataire masque, statut, date d'envoi et provider message id si disponible.

4. `PRD-120` En tant qu'operateur support, je veux retrouver une timeline via plusieurs identifiants afin de ne pas bloquer quand le client ne donne pas la bonne reference.
   - Statut : `Termine`
   - Resultat attendu : recherche par `achat_id`, `reference_achat`, `coffret_instance_id`, email client, telephone client masque, `transaction_id` ou `provider_message_id`.

5. `PRD-121` En tant qu'operateur support, je veux voir les identifiants techniques utiles sans exposer de secrets afin de transmettre un dossier exploitable aux developpeurs.
   - Statut : `Termine`
   - Resultat attendu : la timeline expose les identifiants utiles et masque les tokens, QR et secrets.

6. `PRD-122` En tant que responsable exploitation, je veux que les evenements critiques soient audites afin de garantir une trace durable hors logs techniques.
   - Statut : `Termine`
   - Resultat attendu : les evenements critiques proviennent de `evenements_audit` quand disponibles.

### Decisions produit a cadrer

- La timeline est une vue interne support/back-office, pas une vue client.
- Le MVP agrege les tables existantes plutot que de creer une table materialisee.
- Les donnees sensibles doivent etre masquees.
- La recherche par email/telephone doit etre arbitree au regard du RGPD.
- Les evenements reconstruits doivent etre distinguables des evenements audites.

---

## Epic 23. Gestion des batchs et ordonnancement

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : industrialiser l'execution des batchs Localeo avec un inventaire centralise, un ordonnancement fiable, une supervision exploitable et des garde-fous de production.
- Pourquoi maintenant : les batchs email, SMS, expiration, relance et purge existent deja, mais leur declenchement reste manuel ou externe. Avant production, Localeo doit garantir que les traitements critiques tournent a la bonne frequence, sans double execution, avec des traces consultables par l'exploitation.
- Backlog detaille : [docs/roadmap/terminees/epic-23-gestion-batchs-ordonnancement-backlog.md](terminees/epic-23-gestion-batchs-ordonnancement-backlog.md)

### User Stories

1. `PRD-125` En tant qu'exploitant, je veux consulter l'inventaire des batchs disponibles afin de savoir quels traitements doivent etre planifies.
   - Statut : `Termine`
   - Resultat attendu : chaque batch affiche son nom, son endpoint, son scope de securite, ses parametres, sa criticite et sa frequence cible.

2. `PRD-126` En tant qu'exploitant, je veux voir la derniere execution de chaque batch afin de detecter rapidement un traitement en retard.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche date de debut, date de fin, statut, duree, acteur et compteurs principaux.

3. `PRD-127` En tant que systeme, je veux journaliser chaque execution batch dans une table dediee afin de conserver une trace exploitable hors logs techniques.
   - Statut : `Termine`
   - Resultat attendu : chaque execution porte un `batch_code`, un statut, les dates, les compteurs, les erreurs et une correlation technique.

4. `PRD-128` En tant que systeme, je veux empecher deux executions concurrentes d'un meme batch afin d'eviter les doubles envois ou traitements incoherents.
   - Statut : `Termine`
   - Resultat attendu : un verrou logique ou base de donnees bloque un second lancement si une execution est deja en cours.

5. `PRD-129` En tant qu'exploitant, je veux lancer manuellement un batch depuis le back-office afin de reprendre un traitement apres incident.
   - Statut : `Termine`
   - Resultat attendu : le lancement manuel reste reserve aux admins autorises.
   - Resultat attendu : les batchs sensibles proposent un `dry_run` quand applicable.

6. `PRD-130` En tant qu'exploitant, je veux recevoir une alerte quand un batch critique echoue ou ne tourne pas dans sa fenetre attendue afin d'intervenir avant impact client.
   - Statut : `Termine`
   - Resultat attendu : les echecs des batchs critiques remontent dans un dashboard ou un canal d'alerte configure.

7. `PRD-131` En tant que systeme, je veux exposer un endpoint de health batch afin que l'infrastructure puisse superviser les traitements planifies.
   - Statut : `Termine`
   - Resultat attendu : l'endpoint retourne les batchs en retard, en echec et les derniers compteurs utiles.

8. `PRD-132` En tant qu'exploitant, je veux documenter l'ordonnancement de production afin de configurer cron, Cloud Scheduler, GitHub Actions ou tout autre ordonnanceur sans ambiguite.
   - Statut : `Termine`
   - Resultat attendu : la documentation fournit les frequences, les URLs, les scopes, les timeouts, les limites et l'ordre de lancement recommande.

9. `PRD-133` En tant que responsable exploitation, je veux distinguer les batchs automatiques, manuels et de reprise afin de ne pas automatiser un traitement qui doit rester sous controle humain.
   - Statut : `Termine`
   - Resultat attendu : chaque batch porte une strategie d'execution cible : automatique, manuel, reprise, ou back-office uniquement.

10. `PRD-134` En tant que responsable securite, je veux que les endpoints batch soient proteges, limites et audites afin de reduire le risque d'abus ou de declenchement non autorise.
    - Statut : `Termine`
    - Resultat attendu : les endpoints batch utilisent `internal:batch` ou un scope plus precis.
    - Resultat attendu : les lancements batch sont rate-limites et auditables.

### Decisions produit a cadrer

- Les batchs critiques doivent etre automatises avant mise en production.
- Les batchs doivent rester declenchables manuellement pour reprise d'incident.
- Les executions batch doivent etre historisees hors logs techniques.
- Les batchs d'envoi email/SMS conservent le modele outbox.
- Les batchs critiques doivent avoir une frequence cible, un timeout et une politique de retry documentes.
- Une purge d'activites locales doit etre exposee en endpoint batch si elle devient automatisee.
- Les endpoints batch restent sous `/protected` et scope `internal:batch`.

---

## Epic 24. Optimisation de la couche domaine DDD

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : clarifier la couche domaine Localeo en separant explicitement les entites metier, value objects, repositories et exceptions metier selon des conventions DDD lisibles.
- Pourquoi maintenant : la couche domaine grossit avec les achats, coffrets, reversements, remboursements, contacts, batchs et profils commercants. Sans structure plus explicite, les objets metier deviennent difficiles a retrouver, nommer, tester et faire evoluer.
- Backlog detaille : [docs/roadmap/terminees/epic-24-optimisation-couche-domaine-ddd-backlog.md](terminees/epic-24-optimisation-couche-domaine-ddd-backlog.md)

### User Stories

1. `PRD-135` En tant que developpeur, je veux trouver chaque entite metier dans un fichier dedie afin de comprendre rapidement le domaine.
   - Statut : `Termine`
   - Resultat attendu : chaque entite principale est exposee depuis `app.domaine.entities`.

2. `PRD-136` En tant que developpeur, je veux trouver chaque value object dans un fichier dedie afin de distinguer clairement les types metier des primitives.
   - Statut : `Termine`
   - Resultat attendu : chaque value object est expose depuis `app.domaine.value_objects`.

3. `PRD-137` En tant que developpeur, je veux avoir un package repositories avec une classe ou un protocole par repository afin de clarifier les ports de persistence du domaine.
   - Statut : `Termine`
   - Resultat attendu : chaque repository domaine a un fichier dedie.

4. `PRD-138` En tant que developpeur, je veux avoir un package exceptions avec une classe par exception metier afin de rendre les erreurs domaine explicites.
   - Statut : `Termine`
   - Resultat attendu : chaque exception metier a son propre fichier.

5. `PRD-139` En tant que responsable technique, je veux une cartographie des objets domaine afin de savoir quels concepts existent et ou ils sont definis.
   - Statut : `Termine`
   - Resultat attendu : une documentation liste entites, value objects, repositories et exceptions.

6. `PRD-140` En tant que developpeur, je veux des conventions de nommage domaine afin d'eviter les classes generiques ou ambiguës.
   - Statut : `Termine`
   - Resultat attendu : les fichiers utilisent le nom metier en snake_case et les classes un nom metier explicite.

7. `PRD-141` En tant que mainteneur, je veux migrer tous les imports domaine en une seule passe afin d'atteindre directement la structure cible.
   - Statut : `Termine`
   - Resultat attendu : aucun import applicatif ne pointe encore vers les anciens modules domaine a la fin de la migration.

8. `PRD-142` En tant que mainteneur, je veux supprimer les anciens modules fourre-tout une fois la migration terminee afin d'eviter deux sources de verite.
   - Statut : `Termine`
   - Resultat attendu : les anciens modules ne contiennent plus de definitions metier ni de facades de compatibilite durables.

9. `PRD-143` En tant que developpeur, je veux que la couche domaine reste independante de FastAPI, SQLAlchemy et des providers externes afin de conserver une architecture propre.
   - Statut : `Termine`
   - Resultat attendu : les packages domaine ne dependent pas de l'infrastructure.

10. `PRD-144` En tant que responsable qualite, je veux des tests de non-regression sur les objets domaine afin de securiser la migration.
    - Statut : `Termine`
    - Resultat attendu : les value objects, exceptions et entites critiques sont testes.

11. `PRD-145` En tant que mainteneur, je veux gerer explicitement les noms publics du domaine afin d'eviter les ruptures d'import non maitrisees.
    - Statut : `Termine`
    - Resultat attendu : les renommages publics retenus sont documentes et appliques partout dans la meme passe.

12. `PRD-146` En tant que developpeur, je veux une strategie de refactoring one-shot des imports afin de supprimer immediatement les anciens chemins.
    - Statut : `Termine`
    - Resultat attendu : les anciens chemins d'import ne sont plus utilises apres la migration.

### Decisions produit a cadrer

- La migration ne doit pas changer le comportement fonctionnel.
- Les endpoints API, schemas base et workflows metier restent stables.
- La migration est one-shot : aucun ancien import n'est conserve volontairement.
- Tous les renommages publics sont acceptes si tous les imports consommateurs sont migres dans la meme passe.
- Tout renommage de classe publique doit etre applique dans tous les imports consommateurs dans la meme passe.
- Le package cible des value objects est `value_objects`, pas `value_objets`.
- Les repositories du domaine restent des ports ; les implementations SQLAlchemy restent dans l'infrastructure.

---

## Epic 25. Couche de tests fonctionnels domaine et application

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : mettre en place une suite de tests fonctionnels automatisee pour les entites, value objects, use cases et services applicatifs.
- Pourquoi maintenant : apres le decoupage DDD de l'Epic 24, les regles metier sont plus localisables. Il faut maintenant les verrouiller par des tests lisibles avant de poursuivre les evolutions produit.
- Backlog detaille : [docs/roadmap/terminees/epic-25-tests-fonctionnels-domaine-application-backlog.md](terminees/epic-25-tests-fonctionnels-domaine-application-backlog.md)
- Plan detaille des tests : [docs/roadmap/terminees/epic-25-tests-fonctionnels-domaine-application-backlog.md](terminees/epic-25-tests-fonctionnels-domaine-application-backlog.md)

### User Stories

1. `PRD-147` En tant que developpeur, je veux une structure `tests/` claire par couche afin d'identifier rapidement ou placer un test.
   - Statut : `Termine`
   - Resultat attendu : les dossiers `tests/domain`, `tests/application/use_cases`, `tests/application/services` existent.

2. `PRD-148` En tant que developpeur, je veux tester les value objects afin de verrouiller les invariants de base.
   - Statut : `Termine`
   - Resultat attendu : les value objects critiques sont couverts.

3. `PRD-149` En tant que developpeur, je veux tester les entites domaine critiques afin de securiser les transitions metier.
   - Statut : `Termine`
   - Resultat attendu : les entites avec methodes metier sont couvertes en priorite.

4. `PRD-150` En tant que developpeur, je veux des fakes de repositories et Unit of Work afin de tester les use cases sans base de donnees.
   - Statut : `Termine`
   - Resultat attendu : un `FakeUnitOfWork` et des repositories fake couvrent les tests application.

5. `PRD-151` En tant que responsable produit, je veux une matrice UC -> tests afin de savoir quels parcours metier sont securises.
   - Statut : `Termine`
   - Resultat attendu : chaque UC de la specification fonctionnelle est rattache a un test cible ou a une justification hors perimetre.

6. `PRD-152` En tant que developpeur, je veux tester les use cases achat/paiement afin de reduire le risque de regression sur le revenu.
   - Statut : `Termine`
   - Resultat attendu : initialisation paiement, validation paiement, achat particulier et achat professionnel sont couverts.

7. `PRD-153` En tant que developpeur, je veux tester les use cases tokens/activation/consultation afin de securiser les parcours beneficiaires.
   - Statut : `Termine`
   - Resultat attendu : management token, activation token, consultation token, expiration et revocation sont couverts.

8. `PRD-154` En tant que developpeur, je veux tester les use cases commercants et validation terrain afin de securiser l'usage en boutique.
   - Statut : `Termine`
   - Resultat attendu : authentification, session, transaction de validation, validation prestation et mode secours sont couverts.

9. `PRD-155` En tant que support, je veux tester les use cases messages, timeline, documents et remboursements afin de fiabiliser le back-office d'exploitation.
   - Statut : `Termine`
   - Resultat attendu : creation/reponse message, timeline, documents achat et annulation/remboursement sont couverts.

10. `PRD-156` En tant qu'exploitant, je veux tester les services email/SMS/batchs afin de limiter les regressions d'exploitation.
    - Statut : `Termine`
    - Resultat attendu : reservation, transitions de statut, retry, echec et verrou batch sont couverts.

11. `PRD-157` En tant que finance, je veux tester les use cases reversements afin de securiser les montants dus aux commercants.
    - Statut : `Termine`
   - Resultat attendu : mouvement, campagne Stripe, paiement reversement, webhook transfer et reprise/echec Stripe sont couverts.

12. `PRD-158` En tant que responsable qualite, je veux executer la suite de tests avec une commande stable afin de l'integrer a la CI.
    - Statut : `Termine`
    - Resultat attendu : `pytest` lance les tests fonctionnels domaine/application.

### Decisions produit a cadrer

- Les tests MVP couvrent domaine et application, pas les routes HTTP ni SQLAdmin.
- Les providers externes sont remplaces par fakes ou stubs.
- La matrice de couverture se base sur les UC-01 a UC-31 de la specification fonctionnelle.
- Le cahier de test backoffice reste la reference de recette UI ; seuls les invariants applicatifs associes sont automatises dans cette Epic.

---

## Epic 29. Jeu de donnees de test pour recette

- Criticite : `Moyenne`
- Statut : `Termine`
- Objectif : disposer d'une commune de test, d'un commercant de test et de coffrets de test afin de verifier les parcours principaux sans melanger ces donnees avec le catalogue reel.
- Pourquoi maintenant : l'approche initiale de tests controles en production est trop complexe. Un petit jeu de donnees de test, clairement marque et exclu des surfaces publiques, suffit pour les besoins de recette manuelle.
- Backlog detaille : [docs/roadmap/terminees/epic-29-tests-controles-production-backlog.md](terminees/epic-29-tests-controles-production-backlog.md)
- Decision : pas de mode test production complexe en MVP ; le besoin est couvert par des donnees de test identifiables et stables.

### User Stories

1. `PRD-197` En tant qu'operateur Localeo, je veux identifier une commune comme donnee de test afin de l'utiliser pour la recette sans la confondre avec une commune reelle.
   - Statut : `Termine`
   - Resultat attendu : une commune peut etre marquee test.

2. `PRD-198` En tant qu'operateur Localeo, je veux identifier un commercant comme commercant de test afin de rejouer les parcours sans impacter un partenaire reel.
   - Statut : `Termine`
   - Resultat attendu : un commercant peut etre marque test et rattache a une commune de test.

3. `PRD-199` En tant qu'operateur Localeo, je veux identifier un coffret comme coffret de test afin de pouvoir tester le parcours achat et activation.
   - Statut : `Termine`
   - Resultat attendu : un coffret peut etre marque test et rattache a une commune de test.

4. `PRD-200` En tant qu'operateur Localeo, je veux rattacher uniquement des prestations de test aux coffrets de test afin d'eviter tout melange avec le catalogue reel.
   - Statut : `Termine`
   - Resultat attendu : le back-office signale ou refuse les associations mixtes test/reel.

5. `PRD-201` En tant que responsable produit, je veux exclure les donnees de test du catalogue public afin de ne pas les exposer aux visiteurs.
   - Statut : `Termine`
   - Resultat attendu : communes, commercants, coffrets et prestations de test ne sont pas retournes par les endpoints publics par defaut.

6. `PRD-202` En tant qu'exploitant, je veux exclure les donnees de test des KPIs reels afin de ne pas fausser les tableaux de bord.
   - Statut : `Termine`
   - Resultat attendu : les operations liees aux donnees test sont exclues des indicateurs business par defaut.

7. `PRD-203` En tant que finance, je veux que les validations issues d'un coffret de test ne produisent pas de reversement payable afin de proteger les exports financiers.
   - Statut : `Termine`
   - Resultat attendu : les mouvements issus de donnees test sont exclus des lots de paiement.

8. `PRD-204` En tant qu'operateur back-office, je veux generer ou retrouver rapidement le jeu de donnees de test afin de ne pas le reconstruire manuellement.
   - Statut : `Termine`
   - Resultat attendu : un script seed ou une action back-office cree les donnees manquantes de facon idempotente.

9. `PRD-205` En tant que testeur, je veux une fiche de recette indiquant quels parcours tester avec le commercant et les coffrets de test.
   - Statut : `Termine`
   - Resultat attendu : la documentation liste les parcours achat, activation, validation prestation, support et back-office.

10. `PRD-206` En tant que responsable securite, je veux eviter que les donnees de test envoient des communications a de vrais clients.
    - Statut : `Termine`
    - Resultat attendu : les emails et SMS generes depuis les parcours de test utilisent des destinataires explicitement controles.

### Decisions produit a cadrer

- Nom exact du marqueur : `is_test`, `usage` ou `mode_recette`.
- Tables exactes qui portent le marqueur en dur.
- Strategie pour les donnees derivees : champ persiste ou inference depuis le coffret/achat.
- Comportement des emails/SMS sur les parcours de test.

---

## Epic 30. Vision 360 reversements et paiements backoffice

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir au back-office finance une vision 360 dediee aux reversements et paiements afin de preparer, controler et suivre les campagnes de reversement faites deux fois par mois. Avec l'EPIC 39, la vision cible doit basculer vers les operations Stripe Connect et ne plus dependre des lots de paiement bancaire pour les nouveaux flux.
- Pourquoi maintenant : les Epics 12 et 13 outillent la generation et le paiement, mais l'exploitation bimensuelle a besoin d'une vue consolidee pour savoir quoi payer, quoi debloquer et quoi confirmer.
- Backlog detaille : [docs/roadmap/terminees/epic-30-vue-360-reversements-paiements-backlog.md](terminees/epic-30-vue-360-reversements-paiements-backlog.md)

### User Stories

1. `PRD-207` En tant qu'operateur finance, je veux ouvrir une vision 360 reversements et paiements afin de piloter les campagnes depuis un point d'entree unique.
   - Statut : `Termine`
   - Resultat attendu : une entree back-office dediee affiche une synthese par periode et des liens vers generation, paiements, lots et documentation.

2. `PRD-208` En tant qu'operateur finance, je veux filtrer la vue par campagne bimensuelle afin de travailler sur la bonne fenetre de traitement.
   - Statut : `Termine`
   - Resultat attendu : la page propose les deux campagnes du mois, avec dates ajustables et filtre partageable via l'URL.

3. `PRD-209` En tant qu'operateur finance, je veux voir la synthese financiere de la campagne afin de connaitre le montant a traiter et l'avancement.
   - Statut : `Termine`
   - Resultat attendu : un pipeline exclusif affiche les montants et volumes par etape ; les frais Stripe proviennent des paiements clients sources rattaches aux prestations, meme pour un achat anterieur a la campagne, et une donnee absente est affichee `A recuperer`.

4. `PRD-210` En tant qu'operateur finance, je veux lister les commercants a payer et leurs blocages afin de preparer la campagne sans navigation dispersee.
   - Statut : `Termine`
   - Resultat attendu : chaque commercant affiche `Montant du`, `Deja transfere`, `Reste a transferer`, etat du reversement, suivi du virement bancaire et lien vers la vision 360 commercant ; les references Stripe sont repliees dans un detail technique.

5. `PRD-211` En tant qu'operateur finance, je veux suivre les paiements et lots de la campagne afin de confirmer rapidement ce qui a ete execute en banque.
   - Statut : `Termine`
   - Resultat attendu : les lots, paiements `EN_COURS_MANUEL`, paiements `EXECUTE` et paiements `ECHEC` sont visibles et actionnables.

6. `PRD-212` En tant qu'operateur finance, je veux controler les notifications commercants apres paiement afin de verifier que les partenaires sont informes.
   - Statut : `Termine`
   - Resultat attendu : la vue signale notification creee, absente ou en echec pour les paiements `EXECUTE`.

7. `PRD-213` En tant qu'operateur finance, je veux exporter un recapitulatif de campagne afin de conserver un support de controle interne.
   - Statut : `Termine`
   - Resultat attendu : un export `CSV` reprend les montants dus, transferes et restants, les etats metier et les references techniques sans IBAN complet par defaut, avec audit des le MVP.

8. `PRD-214` En tant qu'operateur back-office, je veux voir les alertes finance dans le dashboard operationnel afin de ne pas manquer les actions urgentes entre deux campagnes.
   - Statut : `Termine`
   - Resultat attendu : les paiements a confirmer, paiements en echec et commercants bloques pointent vers la vision 360 reversements filtree.

### Decisions produit a cadrer

- La cadence cible est deux campagnes par mois, avec fenetres par defaut `1-15` et `16-fin de mois`.
- Le MVP ne cree pas de nouvelle table de campagne ; une campagne est un filtre de periode porte par l'URL et reconstitue depuis mouvements, reversements, lots, paiements, emails et audit.
- Les donnees de test ne sont pas encore identifiables techniquement ; leur exclusion automatique dependra du marqueur cible de l'Epic 29.
- L'export recapitulatif de campagne doit etre audite des le MVP.
- Toutes les user stories `PRD-207` a `PRD-214` sont retenues ; le MVP back-office est implemente.
- La vue consolide les donnees existantes sans remplacer les use cases des Epics 12 et 13.
- La vision 360 expose au maximum le statut d'eligibilite Stripe Connect et les references utiles ; l'export recapitulatif n'inclut pas d'IBAN complet par defaut.
- Decision EPIC 39 : les vues finance cible doivent lire `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` enrichis par les references Stripe, sans lots bancaires operationnels.
- L'IBAN complet ne doit plus etre expose pour un export bancaire de paiement ; Stripe Connect porte l'onboarding et le payout commercant.

---

## Epic 31. Annulation d'une validation de prestation backoffice

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre au back-office d'annuler une validation de prestation faite par erreur, tant que le reversement associe n'est pas engage ou paye.
- Pourquoi maintenant : une erreur de validation commercant cree aujourd'hui une prestation `VALIDEE`, une validation, un mouvement de reversement, des traces client et des effets d'activite sans action de correction controlee.
- Backlog detaille : [docs/roadmap/terminees/epic-31-annulation-validation-prestation-backoffice.md](terminees/epic-31-annulation-validation-prestation-backoffice.md)

### User Stories

1. `PRD-215` En tant qu'operateur back-office, je veux identifier les validations annulables afin de savoir si une erreur terrain peut encore etre corrigee.
   - Statut : `Termine`
   - Resultat attendu : le back-office affiche si la validation est annulable, le mouvement de reversement associe et le motif de blocage le cas echeant.

2. `PRD-216` En tant qu'operateur back-office, je veux annuler une validation avant reversement afin de remettre la prestation a disposition sans payer un commercant par erreur.
   - Statut : `Termine`
   - Resultat attendu : l'action est disponible depuis la fiche `ValidationPrestation`, la fiche `StatutPrestationCoffretInstance` et la vision 360 ; la prestation repasse a `A_VALIDER`, `date_validation` est videe, le mouvement passe a `ANNULE` et la `coffret instance` est recalculee.

3. `PRD-217` En tant que responsable exploitation, je veux que l'annulation soit auditee afin de conserver une trace claire d'une correction sensible.
   - Statut : `Termine`
   - Resultat attendu : l'action `purchase.prestation.validation.cancelled` trace acteur, motif, validation, prestation, coffret instance, mouvement et statuts avant/apres.

4. `PRD-218` En tant qu'operateur back-office, je veux neutraliser les effets connexes afin qu'une validation annulee ne continue pas d'apparaitre comme une prestation realisee.
   - Statut : `Termine`
   - Resultat attendu : l'activite locale est masquee totalement via le statut ou la visibilite existante, les feedbacks deja presents restent conserves, et le client est notifie par email uniquement.

5. `PRD-219` En tant qu'operateur support, je veux voir l'historique d'annulation afin de comprendre pourquoi une prestation est redevenue disponible.
   - Statut : `Termine`
   - Resultat attendu : timeline support, vision 360 commercant et vision 360 coffret affichent l'annulation et son motif back-office.

6. `PRD-220` En tant que responsable finance, je veux bloquer les annulations dangereuses afin de ne pas casser un reversement prepare, exporte ou paye.
   - Statut : `Termine`
   - Resultat attendu : l'annulation est refusee si le mouvement n'est plus `A_REVERSER` ou si un paiement associe est deja en cours ou execute.

7. `PRD-221` En tant que responsable finance, je veux preparer une regularisation manuelle hors MVP afin de traiter les erreurs detectees apres paiement.
   - Statut : `Termine`
   - Resultat attendu : les cas post-paiement sont marques non annulables et orientes vers une regularisation financiere future.

8. `PRD-222` En tant que commercant, je veux signaler une erreur de validation depuis mon application afin que le back-office puisse la corriger si les conditions finance le permettent.
   - Statut : `Termine`
   - Resultat attendu : le signalement est possible pendant 24h strictes, cree un message support `messages_contact` rattache a la validation via `validation_prestation_id`, notifie le support, cree une alerte prioritaire et ne modifie directement ni la prestation ni le mouvement de reversement.

### Decisions produit actees

- Le MVP autorise l'annulation uniquement lorsque le mouvement de reversement associe est `A_REVERSER`.
- Une validation annulee ne doit pas etre supprimee physiquement.
- Aucune colonne d'annulation dediee n'est ajoutee sur `validations_prestation` en MVP ; l'annulation s'appuie sur l'audit.
- Le mouvement de reversement est neutralise en statut `ANNULE`, pas supprime.
- La prestation redevient `A_VALIDER` si le coffret instance reste valide et non expire.
- `date_validation` est videe lors du retour a `A_VALIDER`.
- Une nouvelle validation par le meme commercant est autorisee apres annulation.
- L'action back-office est reservee aux admins back-office authentifies, avec motif obligatoire et audit.
- Une action d'annulation directe est aussi disponible via API commercant lorsque la validation appartient au commercant connecte.
- L'annulation directe API applique les memes regles finance/statut que le back-office.
- L'annulation directe API est limitee aux validations recentes de moins de `LOCALEO_VALIDATION_PRESTATION_API_ANNULATION_MAX_HOURS` heures, `24` par defaut.
- Aucun role fin back-office n'est ajoute en MVP pour cette action.
- L'action d'annulation est disponible depuis la fiche `ValidationPrestation`, la fiche `StatutPrestationCoffretInstance` et la vision 360.
- Le motif d'annulation est un texte libre obligatoire.
- Au-dela de la fenetre d'annulation directe API, le commercant doit signaler une erreur au back-office.
- Le signalement commercant ne modifie aucun statut metier tant qu'il n'est pas traite par le back-office.
- Le signalement commercant est limite aux validations recentes de moins de 24h.
- La fenetre de 24h est stricte apres `date_validation`, week-ends et jours feries inclus.
- Un signalement commercant notifie automatiquement l'equipe support.
- Un signalement commercant cree une alerte prioritaire dans le dashboard operationnel.
- Le client est notifie par email uniquement lorsqu'une validation est annulee.
- L'email client utilise le type `PRESTATION_VALIDATION_ANNULEE_CLIENT`.
- L'email client explique que la prestation redevient disponible, sans accuser le commercant.
- Le commercant fautif n'est pas notifie automatiquement lors de l'annulation back-office.
- Le commercant est notifie lorsqu'une demande de signalement est refusee par le back-office.
- L'email de refus commercant utilise le type `SIGNALEMENT_VALIDATION_REFUSE_COMMERCANT`.
- Le signalement commercant reutilise `messages_contact`, sans creer de table dediee en MVP.
- `messages_contact` porte un champ `validation_prestation_id` pour rattacher le signalement a la validation concernee.
- L'activite locale issue de la validation annulee est masquee totalement.
- Le masquage de l'activite locale utilise le statut ou la visibilite existante, sans champ dedie MVP.
- Les feedbacks deja presents restent conserves, sans traitement specifique en MVP.
- Le wording final des emails est laisse a l'implementation, sous reserve de rester neutre et non accusatoire.
- Les cas deja engages en reversement ou paiement sont hors perimetre MVP et doivent passer par une regularisation manuelle.
- La regularisation post-paiement reste hors MVP et sera cadree plus tard.

---

## Epic 32. Live tracking WebPush commercants

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre aux commercants qui activent le live tracking sur leur profil d'etre notifies par WebPush lorsqu'un achat confirme de coffret contient au moins une de leurs prestations actives.
- Pourquoi maintenant : les commercants ont besoin de signaux plus directs sur la valeur commerciale generee par Localeo ; le dashboard donne une lecture retrospective, mais le live tracking renforce l'engagement au moment de l'achat.
- Backlog detaille : [docs/roadmap/terminees/epic-32-live-tracking-webpush-commercants-backlog.md](terminees/epic-32-live-tracking-webpush-commercants-backlog.md)

### User Stories

1. `PRD-223` En tant que commercant, je veux activer le live tracking sur mon profil afin d'etre informe des achats de coffrets contenant mes prestations actives.
   - Statut : `Termine`
   - Resultat attendu : une preference explicite est disponible cote application commercant, portee par `profils_commercants` et desactivee par defaut si aucune decision n'existe.
   - Resultat attendu : l'activation commercant reste sans effet si le feature flag global `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED` est desactive.

2. `PRD-224` En tant qu'application commercant, je veux enregistrer un abonnement WebPush afin que le backend puisse notifier le device autorise.
   - Statut : `Termine`
   - Resultat attendu : l'abonnement est rattache au commercant authentifie et stocke avec endpoint, cles et statut actif.

3. `PRD-225` En tant qu'application commercant, je veux revoquer un abonnement WebPush afin d'arreter les notifications sur un device donne.
   - Statut : `Termine`
   - Resultat attendu : l'abonnement peut etre desactive sans supprimer l'historique d'envoi.

4. `PRD-226` En tant que systeme, je veux identifier les commercants concernes par un achat confirme afin de notifier uniquement les partenaires pertinents.
   - Statut : `Termine`
   - Resultat attendu : seuls les commercants actifs, opt-in, avec prestation active dans le coffret et abonnement actif sont eligibles.

5. `PRD-227` En tant que systeme, je veux creer une notification WebPush outbox lors d'un achat confirme afin de ne pas ralentir le parcours paiement.
   - Statut : `Termine`
   - Resultat attendu : une contrainte d'idempotence evite les doublons par type, commercant et achat.
   - Resultat attendu : aucune notification outbox n'est creee si le feature flag global est desactive.

6. `PRD-228` En tant que commercant, je veux recevoir une notification sobre et utile afin de comprendre qu'un coffret contenant mon offre vient d'etre achete.
   - Statut : `Termine`
   - Resultat attendu : le payload ne contient aucune donnee personnelle client, ni `achat_id`, ni `coffret_id`; il contient uniquement un deep link applicatif opaque.

7. `PRD-229` En tant qu'exploitant, je veux superviser les notifications WebPush afin de diagnostiquer les incidents de livraison.
   - Statut : `Termine`
   - Resultat attendu : les notifications WebPush sont visibles en back-office avec statut, tentatives et erreurs.

8. `PRD-230` En tant que responsable securite, je veux que les abonnements WebPush soient proteges afin d'eviter l'usurpation ou la fuite de donnees.
   - Statut : `Termine`
   - Resultat attendu : les APIs de gestion WebPush et de resolution du deep link exigent une session commercant valide et ne loggent pas les endpoints complets.
   - Resultat attendu : la reception technique d'une notification ne cree pas de session commercant.

9. `PRD-231` En tant que systeme, je veux nettoyer les abonnements invalides afin de limiter les echecs repetes.
   - Statut : `Termine`
   - Resultat attendu : un retour provider d'abonnement invalide desactive l'abonnement concerne.

10. `PRD-232` En tant que responsable produit, je veux cadrer les evenements notifiables afin d'eviter une surcharge de notifications.
    - Statut : `Termine`
    - Resultat attendu : le MVP couvre uniquement l'achat confirme d'un coffret contenant une prestation active du commercant.

### Decisions produit actees

- Le live tracking est opt-in cote commercant.
- La fonctionnalite est pilotable par feature flag backend `LOCALEO_FEATURE_LIVE_TRACKING_WEBPUSH_ENABLED`.
- Si le feature flag est desactive, aucune creation outbox ni aucun envoi WebPush n'est execute.
- La preference live tracking est portee par `profils_commercants`.
- Le canal cible MVP est WebPush, pilote par l'application commercant via ses abonnements.
- Le backend ne doit pas envoyer la notification directement depuis le parcours paiement ; il cree une outbox WebPush.
- Le batch WebPush est ordonnance automatiquement comme les batchs email/SMS, avec une route interne relancable pour reprise incident.
- L'evenement declencheur MVP est l'achat confirme, pas l'ouverture de checkout.
- Un commercant n'est notifie qu'une fois par achat, meme si plusieurs prestations du coffret lui appartiennent.
- Le payload push ne doit pas contenir de donnees personnelles client, ni `achat_id`, ni `coffret_id`; il contient uniquement un deep link applicatif opaque.
- La reception WebPush peut se faire hors session active ; au clic, l'application demande une authentification si necessaire avant de resoudre la reference opaque.
- Les abonnements invalides doivent etre desactives automatiquement.
- Les secrets des abonnements revoques ou invalides sont supprimes au plus tard sous 7 jours, idealement immediatement.
- Une trace non sensible d'abonnement revoque est conservee 90 jours, puis purgee ou anonymisee.
- Les notifications `webpush_sortants` sont conservees 90 jours pour support, audit et diagnostic, puis purgees ou anonymisees.
- Le tracking `OUVERT`, clic ou interaction push est retenu pour une V2, hors MVP.

---

## Epic 33. Recherche multi-scope marketplace

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir un service de recherche unique pour la barre de recherche marketplace, capable de retrouver une ville, un commercant, une prestation ou un coffret par son nom.
- Pourquoi maintenant : la marketplace doit permettre une navigation rapide quand le visiteur connait deja une ville, un commercant ou une offre, sans l'obliger a parcourir les listes.
- Backlog detaille : [docs/roadmap/terminees/epic-33-recherche-multiscope-marketplace-backlog.md](terminees/epic-33-recherche-multiscope-marketplace-backlog.md)

### User Stories

1. `PRD-233` En tant que visiteur marketplace, je veux rechercher une ville par son nom afin d'acceder rapidement a son catalogue local.
   - Statut : `Termine`
   - Resultat attendu : une ville publiable correspondant a la requete apparait dans les resultats de type `VILLE`.
   - Resultat attendu : les villes sont toujours presentees avant les autres scopes.

2. `PRD-234` En tant que visiteur marketplace, je veux rechercher un commercant par son nom afin d'acceder rapidement a sa fiche publique.
   - Statut : `Termine`
   - Resultat attendu : seuls les commercants publiables et visibles sur la marketplace sont retournes.
   - Resultat attendu : les commercants sont presentes apres les villes et avant les coffrets.

3. `PRD-235` En tant que visiteur marketplace, je veux rechercher un coffret par son nom afin d'acceder rapidement a l'offre correspondante.
   - Statut : `Termine`
   - Resultat attendu : seuls les coffrets actifs ou publiables sur la marketplace sont retournes.
   - Resultat attendu : les coffrets sont presentes apres les villes, les commercants et les prestations.

4. `PRD-235 bis` En tant que visiteur marketplace, je veux rechercher une prestation par son nom afin d'acceder rapidement a l'offre ou au coffret qui la porte.
   - Statut : `Termine`
   - Resultat attendu : seules les prestations actives et exposables sur la marketplace sont retournees.
   - Resultat attendu : les prestations sont presentees apres les commercants et avant les coffrets.

5. `PRD-236` En tant qu'application marketplace, je veux consommer un endpoint unique de recherche multi-scope afin d'alimenter une barre de recherche simple.
   - Statut : `Termine`
   - Resultat attendu : l'API accepte une requete texte et retourne une liste homogene de resultats types.
   - Resultat attendu : le contrat fournit une cible typee exploitable par le frontend, sans imposer l'URL finale.

6. `PRD-237` En tant que systeme, je veux appliquer une priorite de resultats par scope afin de garantir un ordre stable et comprehensible.
   - Statut : `Termine`
   - Resultat attendu : l'ordre global est toujours `VILLE`, puis `COMMERCANT`, puis `PRESTATION`, puis `COFFRET`.
   - Resultat attendu : a l'interieur de chaque scope, les resultats sont tries par pertinence puis par nom.

7. `PRD-238` En tant que systeme, je veux normaliser la recherche afin que les accents et la casse ne bloquent pas la decouverte.
   - Statut : `Termine`
   - Resultat attendu : `cafe`, `Cafe` et `CAFÉ` peuvent produire les memes correspondances.
   - Resultat attendu : la normalisation reste cote backend pour garder un comportement uniforme.

8. `PRD-239` En tant qu'exploitant, je veux que la recherche respecte strictement la visibilite publique afin de ne pas exposer de contenu non publie.
   - Statut : `Termine`
   - Resultat attendu : les villes, commercants, prestations et coffrets non publiables sont exclus.
   - Resultat attendu : les regles de statut existantes du catalogue sont reutilisees.

9. `PRD-240` En tant que responsable produit, je veux pouvoir faire evoluer les scopes de recherche sans casser l'IHM afin d'ajouter plus tard activites, suggestions ou nouveaux types de resultats.
   - Statut : `Termine`
   - Resultat attendu : le contrat API est extensible par `scope` sans changer la structure de base d'un resultat.

### Decisions produit actees

- Le service cible est public et consomme par la barre de recherche marketplace.
- L'ordre de priorite inter-scope est strict : `Ville`, puis `Commercant`, puis `Prestation`, puis `Coffret`.
- La recherche se fait par nom en MVP.
- La recherche doit ignorer la casse et les accents.
- Les entites non publiables doivent rester exclues, meme si leur nom correspond exactement a la requete.
- Le backend retourne une cible de navigation typee, mais pas les URLs finales de l'application frontend.
- Les scopes `Prestation` et `Coffret` sont tous les deux dans le MVP.

---

## Epic 34. Localeo Control

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : mettre en place une petite PWA interne, servie par le backend, pour suivre en live et sur la journee l'activite Localeo, dont le CA genere et la marge Localeo associee.
- Pourquoi maintenant : l'exploitation a besoin d'une vue compacte et reactive sur les achats, le CA jour, la marge Localeo, les validations et demandes support sans devoir surveiller toutes les vues du back-office.
- Backlog detaille : [docs/roadmap/terminees/epic-34-pwa-exploitation-live-dashboard-backlog.md](terminees/epic-34-pwa-exploitation-live-dashboard-backlog.md)

### User Stories

1. `PRD-241` En tant qu'operateur Localeo, je veux ouvrir Localeo Control, une PWA d'exploitation authentifiee, afin de suivre l'activite sans passer par toutes les vues du back-office.
   - Statut : `Termine`
   - Resultat attendu : la page d'accueil backend affiche un lien `Localeo Control` en plus des liens Administration et Documentation API.
   - Resultat attendu : la PWA est servie par le backend sur une route interne protegee.
   - Resultat attendu : un utilisateur non authentifie est redirige vers l'authentification back-office ou refuse.

2. `PRD-242` En tant qu'operateur Localeo, je veux voir les indicateurs financiers et operationnels du jour afin de comprendre rapidement l'activite courante.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche le CA net genere sur la journee ou la periode selectionnee.
   - Resultat attendu : le dashboard affiche le montant des remboursements executes pris en compte.
   - Resultat attendu : le dashboard affiche le nombre de prestations remboursees sur la periode selectionnee.
   - Resultat attendu : le dashboard affiche la marge Localeo associee, nette des remboursements executes lorsque les donnees permettent le calcul.
   - Resultat attendu : le dashboard affiche les compteurs du jour pour achats confirmes, validations de prestation et demandes support.
   - Resultat attendu : les donnees sont calculees cote backend avec une fenetre jour explicite.

3. `PRD-243` En tant qu'operateur Localeo, je veux voir un flux live des evenements recents afin d'identifier ce qui vient de se passer.
   - Statut : `Termine`
   - Resultat attendu : le flux liste les evenements recents avec type, heure, libelle et cible back-office.
   - Resultat attendu : le flux est filtre sur la journee par defaut, avec bascule possible sur la semaine ou le mois.
   - Resultat attendu : le front peut rafraichir le flux sans recharger toute la page.

4. `PRD-244` En tant qu'operateur Localeo, je veux recevoir une notification WebPush lorsqu'un achat de coffret est confirme afin de suivre la dynamique commerciale en direct.
   - Statut : `Termine`
   - Resultat attendu : l'evenement achat confirme cree une notification interne eligible.
   - Resultat attendu : le payload WebPush reste sobre et ne contient pas de donnees personnelles client.

5. `PRD-245` En tant qu'operateur Localeo, je veux recevoir une notification WebPush lorsqu'une prestation est validee afin de suivre l'utilisation reelle des coffrets.
   - Statut : `Termine`
   - Resultat attendu : l'evenement validation de prestation cree une notification interne eligible.
   - Resultat attendu : la notification indique un libelle operationnel sans exposer de donnees sensibles.

6. `PRD-246` En tant qu'operateur Localeo, je veux recevoir une notification WebPush lorsqu'une demande support arrive afin de reagir rapidement.
   - Statut : `Termine`
   - Resultat attendu : une nouvelle demande support cree une notification interne eligible.
   - Resultat attendu : la notification permet d'ouvrir la cible back-office associee apres authentification.

7. `PRD-247` En tant qu'operateur Localeo, je veux activer ou desactiver mes abonnements WebPush internes afin de controler les notifications recues.
   - Statut : `Termine`
   - Resultat attendu : la PWA peut enregistrer, lister et revoquer un abonnement WebPush interne.
   - Resultat attendu : les abonnements sont rattaches a l'acteur back-office authentifie.

8. `PRD-248` En tant qu'operateur Localeo, je veux choisir les categories de notifications afin de limiter le bruit operationnel.
   - Statut : `Termine`
   - Resultat attendu : l'operateur peut activer/desactiver achat, validation prestation et support.
   - Resultat attendu : les preferences sont appliquees avant creation ou avant envoi des notifications.

9. `PRD-249` En tant que responsable securite, je veux que la PWA et ses notifications respectent les droits back-office afin de ne pas exposer l'exploitation a des tiers.
   - Statut : `Termine`
   - Resultat attendu : les APIs PWA exigent une session back-office valide.
   - Resultat attendu : la reception WebPush ne cree pas de session ; l'ouverture de detail exige une authentification valide.
   - Resultat attendu : les endpoints, secrets WebPush et payloads sensibles ne sont pas logges en clair.

10. `PRD-250` En tant qu'exploitant, je veux superviser les notifications internes afin de diagnostiquer les echecs d'envoi.
    - Statut : `Termine`
    - Resultat attendu : les notifications internes sortantes ont statut, tentatives, dates et erreur derniere.
    - Resultat attendu : les abonnements invalides sont desactives automatiquement.

### Decisions produit a cadrer

- La PWA est une surface interne d'exploitation, distincte de la marketplace et de l'application commercant.
- La page d'accueil backend expose un lien vers la PWA en plus des liens Administration et Documentation API.
- Les routes PWA et APIs associees exigent une session admin/back-office valide.
- Le live MVP utilise un polling incremental simple.
- Le flux live est filtre sur la journee par defaut et permet de choisir la semaine ou le mois.
- L'identite operateur reutilise l'utilisateur et la session SQLAdmin actuelle.
- Le CA affiche dans Localeo Control est net des remboursements executes : paiements Stripe confirmes sur la periode moins remboursements `REMBOURSE` dont la date d'execution est dans la meme periode.
- Le CA brut des paiements confirmes et le montant rembourse sur la periode restent disponibles dans le payload pour audit et controle.
- Le nombre de prestations remboursees correspond aux prestations rattachees aux `CoffretInstance` remboursees sur la periode, hors prestations deja `VALIDEE`.
- La marge Localeo correspond a la marge comptable reellement acquise, diminuee de la part de marge annulee par les remboursements executes lorsque le snapshot d'achat permet un prorata fiable.
- Le dashboard affiche le CA net, les remboursements executes et la marge Localeo nette.
- Les notifications WebPush internes sont opt-in par operateur.
- L'envoi WebPush interne est ordonnance automatiquement des le MVP.
- Les categories MVP sont `ACHAT_COFFRET_CONFIRME`, `PRESTATION_VALIDEE`, `DEMANDE_SUPPORT_CREEE`.
- Les abonnements WebPush internes sont separes des abonnements WebPush commercants.
- Le payload WebPush interne reste minimal et ne contient pas de donnees sensibles.

---

## Epic 35. Profils back-office differencies

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : remplacer l'acces SQLAdmin unique par une gestion de comptes back-office differencies, avec roles, profils et permissions adaptees aux usages support, exploitation, finance et administration.
- Pourquoi maintenant : les surfaces internes se multiplient et les actions sensibles doivent etre limitees et auditees par utilisateur nominatif.
- Backlog detaille : [docs/roadmap/terminees/epic-35-profils-backoffice-differencies-backlog.md](terminees/epic-35-profils-backoffice-differencies-backlog.md)

### User Stories

1. `PRD-251` En tant qu'administrateur, je veux creer un utilisateur back-office afin de donner un acces nominatif aux operateurs.
   - Statut : `Termine`
   - Resultat attendu : un utilisateur back-office porte login, nom, email, statut, roles et dates de cycle de vie.
   - Resultat attendu : le mot de passe est stocke uniquement sous forme de hash robuste.

2. `PRD-252` En tant qu'administrateur, je veux affecter des roles a un utilisateur afin de limiter ses acces au perimetre utile.
   - Statut : `Termine`
   - Resultat attendu : les roles MVP `ADMIN`, `EXPLOITATION`, `SUPPORT`, `FINANCE`, `LECTURE_SEULE` sont disponibles.
   - Resultat attendu : un utilisateur peut porter un ou plusieurs roles.

3. `PRD-253` En tant qu'operateur back-office, je veux me connecter avec mon compte personnel afin que mes actions soient tracees nominativement.
   - Statut : `Termine`
   - Resultat attendu : la connexion SQLAdmin utilise le referentiel utilisateurs back-office.
   - Resultat attendu : la session contient l'identite utilisateur et ses roles.

4. `PRD-254` En tant que responsable securite, je veux que les routes internes verifient les permissions afin de proteger les actions sensibles.
   - Statut : `Termine`
   - Resultat attendu : les routes `/internal/*` peuvent exiger une permission ou un role.
   - Resultat attendu : un acces non autorise retourne un refus explicite et audite.

5. `PRD-255` En tant qu'administrateur, je veux que les vues SQLAdmin respectent les roles afin d'eviter l'exposition inutile d'ecrans.
   - Statut : `Termine`
   - Resultat attendu : les vues SQLAdmin peuvent etre masquees ou refusees selon les roles.
   - Resultat attendu : les actions `create`, `edit`, `delete` peuvent etre limitees par profil.

6. `PRD-256` En tant que profil support, je veux acceder aux ecrans de support sans acceder aux actions finance ou configuration critique.
   - Statut : `Termine`
   - Resultat attendu : le role `SUPPORT` accede aux messages, timeline, mode secours et aides operationnelles.
   - Resultat attendu : le role `SUPPORT` ne peut pas modifier les configurations sensibles ni les paiements.

7. `PRD-257` En tant que profil finance, je veux acceder aux reversements, paiements et indicateurs financiers sans administrer tout le catalogue.
   - Statut : `Termine`
   - Resultat attendu : le role `FINANCE` accede aux vues reversements, paiements, remboursements et indicateurs financiers.
   - Resultat attendu : les actions non financieres sensibles restent refusees.

8. `PRD-258` En tant que profil exploitation, je veux acceder aux batchs, notifications et Localeo Control afin de piloter l'activite quotidienne.
   - Statut : `Termine`
   - Resultat attendu : le role `EXPLOITATION` accede au dashboard operationnel, batchs, Localeo Control, emails/SMS/WebPush sortants.
   - Resultat attendu : les actions de configuration critique restent reservees a `ADMIN`.

9. `PRD-259` En tant qu'auditeur, je veux retrouver l'utilisateur back-office a l'origine d'une action afin d'ameliorer la tracabilite.
   - Statut : `Termine`
   - Resultat attendu : les evenements d'audit sensibles portent `backoffice_user_id`, login et roles utiles.
   - Resultat attendu : les anciennes actions restent consultables meme si elles n'ont pas d'utilisateur nominatif.

10. `PRD-260` En tant qu'exploitant, je veux migrer depuis l'admin unique sans rupture afin de ne pas bloquer l'acces au back-office.
    - Statut : `Termine`
    - Resultat attendu : un utilisateur `ADMIN` initial peut etre cree depuis la configuration existante.
    - Resultat attendu : la migration documente comment retirer progressivement l'admin unique.

### Decisions produit a cadrer

- Le MVP conserve SQLAdmin comme surface back-office principale.
- Les roles MVP sont `ADMIN`, `EXPLOITATION`, `SUPPORT`, `FINANCE`, `LECTURE_SEULE`.
- Les permissions sont verifiees cote backend, pas seulement par masquage IHM.
- Les routes Localeo Control de l'Epic 34 exigent a minima `ADMIN` ou `EXPLOITATION`.
- Une migration depuis l'admin unique existant est obligatoire.

---

## Epic 36. Fermeture commercant et remplacement des prestations achetees

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre a Localeo de gerer la sortie d'un commercant lorsque des prestations ont deja ete achetees mais ne sont pas encore executees, en les remplacant par des prestations similaires sans impact operationnel pour le client.
- Pourquoi maintenant : meme si les clauses contractuelles encadrent les modalites de fermeture, le cas d'un commercant qui quitte Localeo avec des prestations achetees non executees doit etre traite de maniere outillee, tracable et orientee experience client.
- Backlog detaille : [docs/roadmap/terminees/epic-36-fermeture-commercant-remplacement-prestations-backlog.md](terminees/epic-36-fermeture-commercant-remplacement-prestations-backlog.md)

### User Stories

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

### Decisions produit a cadrer

- Une prestation deja validee, annulee, expiree ou rattachee a un achat rembourse ne doit pas etre remplacee.
- Le commercant ferme doit pouvoir etre desactive lui-meme, en plus de la desactivation commerciale de ses prestations.
- La desactivation du commercant masque son profil public sur le site et dans les APIs publiques.
- La desactivation du commercant masque toutes ses prestations sur le site, dans la recherche publique et dans les APIs publiques.
- La desactivation du commercant empeche toute nouvelle vente rattachee a ses prestations.
- Les coffrets contenant une prestation du commercant desactive ne sont plus achetables tant qu'ils n'ont pas ete mis a jour et recalcules pour rester coherents en prix, reversements et marge.
- Si aucune prestation de substitution acceptable n'est disponible, l'operateur doit pouvoir generer un remboursement pour les clients ayant une prestation en cours chez ce commercant.
- Le remboursement cree une notification email client via l'outbox.
- Le remboursement est cree comme demande back-office a traiter, sans execution PSP automatique dans le MVP.
- Le montant rembourse propose est calcule au prorata simple du nombre de prestations non consommees concernees, avec possibilite d'ajustement back-office avant validation.
- Le client ne doit pas avoir d'action obligatoire a effectuer pour beneficier du remplacement.
- Le QR ou code court existant doit rester utilisable si le support de validation reste rattache a l'instance de coffret.
- Les emails de notification sont crees dans l'outbox dans la meme transaction que le remplacement, puis envoyes par le batch email existant.
- Le remplacement doit conserver la prestation initiale et la prestation de remplacement pour audit, support et finance.
- La validation future doit reverser vers le commercant de remplacement.
- L'operation definitive doit respecter le pattern Unit of Work.
- La fermeture est portee par une table dediee `fermetures_commercants`, et le commercant porte aussi le statut exploitable `FERME`.
- La similarite de prestation est une decision manuelle de l'operateur back-office.
- Un remplacement augmentant la valeur reversee exige une validation finance obligatoire.
- La notification MVP est limitee a l'email, sans SMS obligatoire.
- Si un coffret contient plusieurs prestations du meme commercant ferme, chaque prestation impactee est traitee avec les memes regles de remplacement ou remboursement.
- Points ouverts : aucun point bloquant restant pour le MVP.

---

## Epic 37. Vision 360 client backoffice

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir au back-office une vision 360 d'un client afin de traiter rapidement les demandes clients : retrouver un client, comprendre ses coffrets, renvoyer un QR code, gerer un remboursement et visualiser la valeur generee.
- Pourquoi maintenant : les visions 360 commercant, coffret et reversements structurent deja le pilotage interne ; le support client a besoin du meme niveau de consolidation pour traiter les pertes de QR, questions sur coffrets, remboursements et incidents.
- Backlog detaille : [docs/roadmap/terminees/epic-37-vision-360-client-backoffice-backlog.md](terminees/epic-37-vision-360-client-backoffice-backlog.md)

### User Stories

1. `PRD-274` En tant qu'operateur back-office, je veux rechercher un client par nom, prenom ou telephone afin d'ouvrir rapidement sa vision 360.
   - Statut : `Termine`
   - Resultat attendu : la recherche accepte nom, prenom, email si disponible et telephone.
   - Resultat attendu : le telephone est normalise pour retrouver un client meme si le format saisi differe.

2. `PRD-275` En tant qu'operateur support, je veux consulter une fiche synthese client afin d'identifier rapidement la personne qui contacte Localeo.
   - Statut : `Termine`
   - Resultat attendu : la fiche affiche identite, coordonnees, premier achat, dernier achat, nombre de coffrets et niveau client.

3. `PRD-276` En tant qu'operateur support, je veux voir l'historique des coffrets du client afin de comprendre son parcours d'achat.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les coffrets achetes avec date, statut, ville, montant, destinataire et liens back-office.

4. `PRD-277` En tant qu'operateur support, je veux voir les coffrets en cours afin de traiter rapidement une demande active.
   - Statut : `Termine`
   - Resultat attendu : la vue isole les coffrets encore utilisables ou en attente d'activation.
   - Resultat attendu : chaque coffret en cours affiche expiration, prestations restantes, QR/code disponible et alertes.

5. `PRD-278` En tant qu'operateur support, je veux voir les dernieres prestations realisees afin de comprendre ce que le client a deja consomme.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche les dernieres validations avec date, coffret, prestation, commercant et statut.

6. `PRD-279` En tant qu'operateur support, je veux renvoyer un email avec le QR code d'un coffret en cours afin d'aider un client qui a perdu son mail.
   - Statut : `Termine`
   - Resultat attendu : l'action est disponible uniquement sur les coffrets en cours eligibles.
   - Resultat attendu : l'action cree un email sortant dans l'outbox et un audit.

7. `PRD-280` En tant qu'operateur support, je veux voir un niveau client base sur le nombre de coffrets achetes afin d'adapter le traitement relationnel.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche un niveau simple, par exemple `Nouveau`, `Regulier`, `Fidele`.

8. `PRD-281` En tant que responsable exploitation, je veux voir le CA genere par le client afin d'evaluer son importance economique.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche le CA global encaisse, la part Localeo disponible, les remboursements et le net client si disponible.

9. `PRD-282` En tant que responsable exploitation, je veux voir la repartition du CA client par commercant afin de comprendre quels partenaires ont beneficie de son activite.
   - Statut : `Termine`
   - Resultat attendu : la vue agrege les montants par commercant selon les sources disponibles.

10. `PRD-283` En tant qu'operateur support, je veux gerer un remboursement depuis un coffret de la fiche client afin de traiter une demande sans changer de contexte.
    - Statut : `Termine`
    - Resultat attendu : l'action reutilise le workflow de remboursement existant et affiche les motifs de refus.

11. `PRD-284` En tant qu'operateur support, je veux voir les communications envoyees au client afin de savoir ce qu'il a deja recu.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les derniers emails et SMS rattaches au client, dont QR renvoye, remboursement et communications libres.

12. `PRD-285` En tant qu'operateur support, je veux voir les demandes support rattachees au client afin de comprendre l'historique des echanges.
    - Statut : `Termine`
    - Resultat attendu : la vue liste les messages support et contacts rattaches aux coordonnees du client.

13. `PRD-286` En tant qu'operateur support, je veux acceder aux documents du client afin de repondre aux demandes de justificatifs.
    - Statut : `Termine`
    - Resultat attendu : la vue propose les liens vers recus, factures ou packs documents disponibles.

14. `PRD-287` En tant que responsable securite, je veux que la vision 360 client encadre les donnees personnelles afin de limiter les risques de fuite.
    - Statut : `Termine`
    - Resultat attendu : les recherches, consultations detaillees et actions sensibles sont auditees.
    - Resultat attendu : les roles non autorises ne peuvent pas consulter les donnees personnelles completes.

15. `PRD-288` En tant qu'operateur back-office, je veux naviguer depuis la vision 360 client vers tous les objets rattaches afin d'agir rapidement.
    - Statut : `Termine`
    - Resultat attendu : les achats, coffrets instances, validations, remboursements, emails/SMS, documents et messages support disposent de liens directs.

### Decisions produit a cadrer

- La vision 360 client est une surface interne support/exploitation.
- La recherche client accepte nom, prenom, email et telephone normalise.
- Le MVP cree une vraie table `clients`.
- La cle de consolidation client MVP est l'email.
- Le renvoi QR est reserve aux coffrets en cours eligibles et passe par l'outbox email avec le type dedie `RENVOI_QR_CLIENT`.
- La gestion de remboursement reutilise le workflow de remboursement existant.
- La notation client MVP est informative et basee sur le nombre de coffrets achetes : `Nouveau` pour 1 coffret, `Regulier` pour 2 a 3, `Fidele` pour 4 a 7, `Ambassadeur` a partir de 8.
- Les indicateurs financiers distinguent CA client, revenu Localeo disponible, reversements commercants, remboursements et net.
- La repartition CA par commercant distingue prestations achetees et prestations validees.
- Les donnees personnelles sont masquees ou limitees selon les roles back-office.
- Les coordonnees completes et l'initiation d'un remboursement sont reservees au role `ADMIN`.
- Les achats historiques sans email valide restent en `client non consolide` tant qu'un email valide n'est pas disponible.
- Les doublons apparents avec emails differents sont hors MVP ; le MVP peut afficher une suspicion de doublon sans fusion automatique.
- Aucune delegation a `SUPPORT` ou `FINANCE` n'est prevue en MVP pour les coordonnees completes et les remboursements.

---

## Epic 38. Gestion documentaire transverse

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : centraliser la gestion des documents publics, contractuels commercants et documents clients/achats, sans stocker les binaires en base de donnees.
- Pourquoi maintenant : Localeo doit publier des documents legaux a jour sur le site et l'application commercant, retrouver les contrats signes des partenaires et referencer les documents clients produits par les achats.
- Backlog detaille : [docs/roadmap/terminees/epic-38-gestion-documentaire-backlog.md](terminees/epic-38-gestion-documentaire-backlog.md)

### User Stories

1. `PRD-289` En tant qu'admin, je veux creer une fiche documentaire sans stocker le binaire en base afin de centraliser les metadonnees utiles.
   - Statut : `Termine`
   - Resultat attendu : la base stocke type, statut, scope, rattachements, URI ou cle de stockage, nom de fichier, MIME type, taille et hash.

2. `PRD-290` En tant qu'admin, je veux publier un document public par type et scope afin de maitriser les documents visibles sur le site et l'application commercant.
   - Statut : `Termine`
   - Resultat attendu : le document publie est expose selon ses scopes.

3. `PRD-291` En tant que visiteur du site, je veux consulter les documents publics applicables afin d'acceder aux informations legales a jour.
   - Statut : `Termine`
   - Resultat attendu : les routes publiques exposent uniquement les documents publies avec scope `SITE_PUBLIC`.
   - Resultat attendu : les documents publics frequemment consultes sont affiches en page HTML, avec un lien de telechargement en complement.

4. `PRD-292` En tant que commercant authentifie, je veux consulter les documents applicables a l'application commercant afin d'acceder aux conditions et informations qui me concernent.
   - Statut : `Termine`
   - Resultat attendu : l'application commercant expose uniquement les documents publies avec scope `APPLICATION_COMMERCANT`.

5. `PRD-293` En tant qu'operateur back-office, je veux rattacher un contrat signe a un commercant afin de retrouver rapidement les documents contractuels du partenaire.
   - Statut : `Termine`
   - Resultat attendu : un document contractuel peut etre rattache a `Commercant` et reste inaccessible publiquement.

6. `PRD-294` En tant qu'operateur back-office, je veux suivre le statut d'un document contractuel commercant afin de savoir s'il est attendu, recu, signe, expire ou archive.
   - Statut : `Termine`
   - Resultat attendu : le document porte un statut exploitable et des dates contractuelles quand elles s'appliquent.

7. `PRD-295` En tant que systeme documentaire, je veux referencer les documents clients generes lors d'un achat afin de les retrouver depuis les vues support.
   - Statut : `Termine`
   - Resultat attendu : les recus, factures et packs issus de l'Epic 14 creent ou mettent a jour des metadonnees documentaires.

8. `PRD-296` En tant qu'operateur support, je veux retrouver les documents d'un client ou d'un achat afin de repondre rapidement a une demande de justificatif.
   - Statut : `Termine`
   - Resultat attendu : les vues back-office pertinentes affichent les documents rattaches disponibles.

9. `PRD-297` En tant que responsable securite, je veux que les documents prives soient servis via une route controlee afin de ne pas exposer les URI de stockage internes.
   - Statut : `Termine`
   - Resultat attendu : les documents contractuels et clients sont telecharges via une route authentifiee et autorisee.

10. `PRD-298` En tant qu'admin, je veux archiver un document ou remplacer son contenu afin de maintenir les documents publies et contractuels.
    - Statut : `Termine`
    - Resultat attendu : une suppression fonctionnelle passe le document en `ARCHIVE`.

11. `PRD-299` En tant que responsable exploitation, je veux auditer les operations documentaires afin de tracer creation, publication, consultation et archivage.
    - Statut : `Termine`
    - Resultat attendu : chaque action sensible cree un evenement d'audit.

12. `PRD-300` En tant que responsable technique, je veux verifier l'integrite d'un document reference afin de detecter une incoherence entre metadata et stockage externe.
    - Statut : `Termine`
    - Resultat attendu : le hash et la taille permettent de signaler un document manquant ou altere.

13. `PRD-301` En tant qu'operateur back-office, je veux acceder a une entree `Gestion documentaire` afin de piloter tous les documents depuis une surface dediee.
    - Statut : `Termine`
    - Resultat attendu : la page distingue documents publics et documents prives.
    - Resultat attendu : la page donne une vision synthetique du nombre de documents par categorie, statut et anomalie.

14. `PRD-302` En tant qu'operateur back-office, je veux filtrer les documents publics par scope afin de verifier rapidement ce qui est expose sur chaque surface.
    - Statut : `Termine`
    - Resultat attendu : les filtres couvrent scope, type, statut et date de publication.

15. `PRD-303` En tant qu'admin, je veux mettre a jour un document public sans perdre l'historique afin de remplacer les CGC, mentions legales ou politiques RGPD proprement.
    - Statut : `Termine`
   - Resultat attendu : l'action de mise a jour remplace le contenu du document existant sans changer son identifiant ni ses rattachements.

16. `PRD-304` En tant qu'operateur back-office, je veux rechercher un client ou un commercant depuis les documents prives afin de retrouver rapidement ses documents.
    - Statut : `Termine`
    - Resultat attendu : les resultats separent clients et commercants puis affichent les documents rattaches par type et statut.

17. `PRD-305` En tant qu'operateur back-office, je veux ajouter ou mettre a jour un document prive client ou commercant afin de maintenir son dossier documentaire.
    - Statut : `Termine`
    - Resultat attendu : l'ajout ou la mise a jour conserve l'historique et n'expose jamais le document sur les surfaces publiques.

18. `PRD-306` En tant qu'operateur support ou exploitation, je veux acceder aux documents d'un client ou d'un commercant depuis sa vue 360 afin de ne pas changer de contexte.
    - Statut : `Termine`
    - Resultat attendu : les visions 360 client et commercant affichent un bloc documents et un lien vers la gestion documentaire filtree.

### Decisions produit a cadrer

- Les binaires documentaires ne sont jamais stockes en base de donnees.
- La base porte uniquement les metadonnees et une reference opaque vers le stockage externe.
- Les documents publics sont scopes par surface : `SITE_PUBLIC`, `APPLICATION_COMMERCANT`, `BACKOFFICE`, `CLIENT_APRES_ACHAT`.
- Les documents publics du site sont affiches en page HTML quand le type s'y prete, avec telechargement PDF ou fichier source en complement.
- Les documents contractuels commercants sont rattaches a `Commercant` et reserves aux profils autorises.
- Les documents clients/achats reutilisent les generations de l'Epic 14 et s'y rattachent sans redefinir les regles fiscales.
- Les documents prives sont servis via routes controlees avec audit de consultation.
- Les corrections de documents publics publies remplacent le contenu du document existant avec audit de l'operation.
- Le back-office expose une entree `Gestion documentaire` avec deux vues lisibles : documents publics et documents prives.
- Les documents publics sont filtrables par scope.
- Les documents prives sont accessibles par recherche client ou commercant.
- Les vues 360 client et commercant exposent un bloc documents et un raccourci vers la gestion documentaire filtree.

---

## Epic 39. Delegation des flux financiers a Stripe Connect

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : deleguer a Stripe Connect toute la chaine paiement et reversement Localeo, depuis le paiement client jusqu'au transfer commercant apres validation QR, en conservant les objets internes de paiement/reversement comme projections metier alimentees par Stripe, tout en conservant l'audit et la conformite PSP du modele cible.
- Pourquoi maintenant : la chaine actuelle de paiement et reversement doit evoluer vers Stripe Connect pour fiabiliser l'execution financiere, limiter les operations manuelles et garantir que les commercants ne sont transferes qu'apres validation effective d'une prestation.
- Decision commercialisation : un coffret n'est vendable que si tous les commercants rattaches a ses prestations disposent d'un compte connecte Stripe Express eligible ; si l'eligibilite se degrade apres achat, le reversement est bloque jusqu'a regularisation Stripe.
- Decision economique : Localeo gere les tarifs Stripe Connect et porte les frais Stripe, y compris les frais mensuels par compte actif.
- Decision calendrier : les campagnes bimensuelles de reversement sont executees le 1er et le 15 de chaque mois a 22h00.
- Backlog detaille : [docs/roadmap/terminees/epic-39-stripe-connect-psp-backlog.md](terminees/epic-39-stripe-connect-psp-backlog.md)

### User Stories

1. `PRD-307` En tant qu'operateur back-office, je veux creer ou rattacher un compte connecte Stripe a un commercant afin de le rendre eligible aux reversements PSP.
   - Statut : `Termine`
   - Resultat attendu : un commercant porte un `stripe_account_id` unique et la creation est idempotente.
   - Implementation : `2026-07-14` - creation idempotente, rattachement back-office d'un compte `acct_...` existant avec controle d'unicite et journalisation.

2. `PRD-308` En tant que commercant, je veux finaliser mon onboarding Stripe Connect afin de pouvoir recevoir les reversements Localeo.
   - Statut : `Termine`
   - Resultat attendu : le backend genere un lien d'onboarding et synchronise les capacites Stripe utiles.
   - Resultat attendu : une documentation detaillee du processus d'onboarding commercant Stripe Connect est produite et couvre parcours, pre-requis, statuts, blocages, reprises et responsabilites Localeo/commercant/Stripe.
   - Implementation : `2026-07-14` - synchronisation API et webhook `account.updated`, action back-office de synchronisation, procedure operationnelle [docs/ops/exploitation/onboarder-commercant-stripe-connect.md](../exploitation/exploitation/onboarder-commercant-stripe-connect.md).

2B. `PRD-308B` En tant que responsable commercialisation, je veux bloquer la vente d'un coffret contenant une prestation d'un commercant non eligible Stripe Connect afin d'eviter de vendre des prestations non reversables.
   - Statut : `Termine`
   - Resultat attendu : publication et vente verifient l'eligibilite Stripe Connect de tous les commercants des prestations du coffret.
   - Resultat attendu : un coffret contenant une prestation rattachee a un commercant non eligible Stripe Connect est non vendable jusqu'a regularisation.
   - Implementation : `2026-07-14` - blocage paiement/publication, motif detaille par prestation/commercant, indicateur back-office et reevaluation dynamique apres synchronisation Stripe.

3. `PRD-309` En tant que systeme de paiement, je veux initialiser les paiements client selon le modele `separate charges and transfers` afin que le paiement soit traite par Stripe Connect sur le compte plateforme Stripe Localeo.
   - Statut : `Termine`
   - Resultat attendu : le PaymentIntent est cree cote plateforme et aucun transfer automatique n'est cree au paiement.
   - Implementation : `2026-07-14` - Checkout cree le PaymentIntent cote plateforme sans `transfer_data`, `destination` ni `application_fee_amount`.

4. `PRD-310` En tant que systeme, je veux associer chaque paiement a un `transfer_group` stable `achat:{achat_id}` afin de relier la charge Stripe a l'achat et aux futurs transfers.
   - Statut : `Termine`
   - Resultat attendu : le `transfer_group` est persiste des l'initialisation du paiement au format canonique `achat:{achat_id}` et reutilise pour les transfers associes.
   - Implementation : `2026-07-14` - `transfer_group` canonique force dans Checkout, PaymentIntent et projection `Paiement`.

5. `PRD-311` En tant que systeme, je veux conserver les references Stripe du paiement d'origine afin de supporter reversements, remboursements, support et rapprochement.
   - Statut : `Termine`
   - Resultat attendu : Checkout Session, PaymentIntent, Charge et Customer sont conserves quand disponibles.
   - Implementation : `2026-07-14` - persistance Checkout Session, PaymentIntent, Charge, Customer et enrichissement par reconciliation Stripe expansee.

6. `PRD-312` En tant que systeme de validation, je veux rendre un montant transferable uniquement apres validation QR et eligibilite Stripe Connect afin que le commercant soit reverse apres execution effective de la prestation et compte connecte conforme.
   - Statut : `Termine`
   - Resultat attendu : la validation QR cree l'obligation metier de reversement.
   - Resultat attendu : si le compte connecte Stripe est eligible, le mouvement devient transferable pour une campagne bimensuelle.
   - Resultat attendu : si le compte connecte Stripe est incomplet ou bloque, le mouvement passe en `BLOQUE_ONBOARDING_STRIPE` et n'entre pas en campagne.
   - Implementation : `2026-07-14` - mouvement `TRANSFERABLE` uniquement si Stripe Connect est eligible, blocage onboarding sinon, aucun transfer immediat, idempotence par statut de prestation validee.

7. `PRD-313` En tant que responsable finance, je veux que les transfers utilisent `source_transaction` quand c'est possible afin de rattacher le reversement a la charge client d'origine.
   - Statut : `Termine`
   - Resultat attendu : le backend conserve la charge Stripe d'origine et applique un fallback explicite si `source_transaction` n'est pas utilisable.
   - Implementation : `2026-07-14` - les campagnes Stripe transmettent `source_transaction` quand la charge d'origine est disponible et rendent le `transfer_group` canonique obligatoire pour le transfer.

8. `PRD-314` En tant que systeme, je veux synchroniser les webhooks Stripe afin de suivre paiement, onboarding, transfer, remboursement et echec.
   - Statut : `Termine`
   - Resultat attendu : les webhooks sont verifies par signature et traites de maniere idempotente.
   - Implementation : `2026-07-14` - webhook Stripe Connect signe, idempotent par event id, synchronisant onboarding, paiement, transfer, remboursement et echecs avec journal `operations_stripe`.

9. `PRD-315` En tant qu'operateur finance, je veux voir les paiements et transfers Stripe dans la vision finance afin de suivre ce qui est en attente, execute, rembourse ou en echec.
   - Statut : `Termine`
   - Resultat attendu : les vues finance affichent commercant, prestation, montant, `transfer_group`, references Stripe et statut.
   - Implementation : `2026-07-14` - Vision 360 finance enrichie avec frais PSP, commissions, controles avocat/finance/exploitation, trace Stripe et export CSV exploitable.

10. `PRD-316` En tant que responsable exploitation, je veux pouvoir rejouer ou reprendre un paiement ou transfer en echec sans doubler un flux financier afin de securiser les incidents Stripe.
   - Statut : `Termine`
   - Resultat attendu : chaque operation Stripe porte une cle d'idempotence metier et un transfer deja reussi ne peut pas etre recree.
   - Implementation : `2026-07-14` - reprise idempotente avec reutilisation du `PaiementReversement` en echec et de la cle `stripe:transfer:mouvement:{mouvement_id}` ; les transfers deja demandes ou confirmes ne sont pas rappeles.

11. `PRD-317` En tant que support Localeo, je veux gerer les remboursements Stripe en tenant compte des transfers deja effectues afin de traiter proprement les annulations et incidents client.
   - Statut : `Termine`
   - Resultat attendu : un remboursement avant transfer et une demande post-transfer traitee comme litige sont distingues.
   - Resultat attendu : les contraintes Stripe sont visibles dans le back-office et le lien paiement -> remboursement -> transfer reste auditable.
   - Implementation : `2026-07-14` - le back-office distingue refund Stripe avant transfer, blocage par references Stripe manquantes et litige post-transfer ; chaque decision est visible sur le remboursement et tracee dans `operations_stripe`.

12. `PRD-318` En tant que responsable finance, je veux suivre les frais Stripe afin d'analyser la rentabilite reelle des paiements et reversements.
   - Statut : `Termine`
   - Resultat attendu : les calculs distinguent montant client, montant reverse, frais PSP et marge Localeo.
   - Resultat attendu : une simulation documentee couvre le cas `49 EUR`, deux reversements de `21 EUR` et commission Localeo brute de `7 EUR`, avec frais Stripe estimes et commission nette.
   - Implementation : `2026-07-14` - conservation des references de balance transaction Stripe et des montants de frais/net exposes sur les paiements client, transfers Stripe Connect et remboursements ; calcul de commission Localeo brute et nette estimee ; exposition back-office et Vision 360 finance.
   - Validation runtime : `2026-07-14` - rendu HTML et export CSV verifies par donnees Stripe simulees pour frais PSP, commission brute, commission nette et net transfer.

13. `PRD-366` En tant que responsable juridique et finance, je veux qualifier le role de Localeo dans le modele Stripe Connect afin de limiter le risque d'exercice non autorise d'une activite de prestataire de services de paiement.
   - Statut : `Termine`
   - Resultat attendu : le role Localeo, le besoin eventuel d'enregistrement ACPR et les ecarts contractuels sont documentes.

14. `PRD-367` En tant que responsable finance, je veux prouver que les fonds destines aux commercants ne transitent pas par les comptes bancaires propres Localeo afin de reduire le risque lie au mandat d'encaissement historique.
   - Statut : `Termine`
   - Resultat attendu : les flux paiement, balance Stripe, transfer, payout et compte bancaire sont cartographies.

15. `PRD-368` En tant que responsable juridique, je veux documenter le mecanisme de cantonnement, segregation ou protection des fonds applicable chez Stripe afin de qualifier le risque de perte des creances commercants.
   - Statut : `Termine`
   - Resultat attendu : les elements Stripe et les risques residuels sont references dans un dossier de conformite.

16. `PRD-369` En tant que responsable produit, je veux aligner les documents contractuels et les libelles produit avec le modele PSP cible afin d'eviter une contradiction entre le fonctionnement reel et les engagements contractuels.
   - Statut : `Termine`
   - Resultat attendu : CGV, contrat commercant, mandat existant, factures, mentions back-office et annexes sont audites et corriges si necessaire.

17. `PRD-370` En tant que responsable produit et technique, je veux requalifier les objets internes de paiement/reversement afin qu'ils soient alimentes par Stripe et ne pilotent plus d'operations manuelles.
   - Statut : `Termine`
   - Resultat attendu : `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` sont conserves et enrichis par les references Stripe.
   - Resultat attendu : les nouveaux flux ne creent plus de lots de paiement ni d'exports bancaires manuels.
   - Resultat attendu : les donnees et parcours de reversement manuel sont supprimes, l'application n'etant pas en production.
   - Implementation : `2026-07-14` - les routes et actions de generation/export/confirmation bancaire manuelle restent decommissionnees ; les libelles operationnels residuels sont requalifies en transfers Stripe Connect et les objets visibles du back-office sont des projections Stripe.

### Decisions produit a cadrer

- Le PSP cible est Stripe Connect.
- Le modele cible est `separate charges and transfers`, pas `destination charges`.
- Les comptes connectes Stripe sont rattaches aux commercants.
- Chaque paiement client porte un `transfer_group` stable au format canonique `achat:{achat_id}`.
- Aucun transfer commercant n'est cree au moment du paiement client.
- Les transfers Stripe sont crees uniquement apres validation QR de la prestation.
- `source_transaction` doit etre utilise quand Stripe le permet pour rattacher le transfer a la charge d'origine.
- Les remboursements Stripe doivent distinguer les cas avant et apres transfer commercant.
- Les frais Stripe doivent etre conserves quand ils sont disponibles pour alimenter la rentabilite.
- Les objets internes `Paiement`, `MouvementReversement`, `Reversement` et `PaiementReversement` restent dans le modele cible comme projections metier Stripe.
- Les lots et exports bancaires manuels sont completement decommissionnes de la cible operationnelle.
- Les references Stripe, statuts synchronises, cles d'idempotence et evenements d'audit sont conserves sur ces objets internes et dans le journal evenementiel.
- Les flux manuels banque historiques sont supprimes, l'application n'etant pas en production.
- Les fonds clients destines aux commercants ne doivent pas transiter par un compte bancaire propre Localeo dans le modele cible.
- La qualification juridique du modele Stripe Connect, le besoin eventuel d'enregistrement ACPR et le mecanisme de protection des fonds doivent etre valides avant mise en production.
- Tout fallback manuel banque sur des fonds commercants est interdit dans la cible.

---

## Epic 40. Organisation du backend par domaines fonctionnels

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : reorganiser les objets du backend Localeo par domaines fonctionnels visibles dans `app/domaine`, `app/application`, les paths API, les tags OpenAPI et le menu back-office, tout en conservant `app/infrastructure` transverse.
- Pourquoi maintenant : le backend est deja clarifie par type technique, mais les entites, repositories, services et use cases restent difficiles a lire par contexte metier a mesure que les domaines Localeo se multiplient.
- Backlog detaille : [docs/roadmap/terminees/epic-40-domaines-fonctionnels-backend-backlog.md](terminees/epic-40-domaines-fonctionnels-backend-backlog.md)

### User Stories

1. `PRD-319` En tant que developpeur, je veux une cartographie des objets backend par domaine fonctionnel afin de comprendre rapidement ou se trouve chaque responsabilite.
   - Statut : `A faire`
   - Resultat attendu : chaque entite, repository, service applicatif et use case a un domaine cible.

2. `PRD-320` En tant qu'architecte, je veux valider le decoupage cible afin d'eviter qu'`exploitation` devienne un domaine fourre-tout.
   - Statut : `A faire`
   - Resultat attendu : les domaines `identite_acces`, `documentaire` et `animation_locale` sont retenus.
   - Resultat attendu : `TypeCoffretConfig`, `IdentifiantCommercant` et les tokens de consultation ont une affectation actee.
   - Resultat attendu : le rattachement du QR coffret et du feedback prestation est acte avant implementation.

3. `PRD-321` En tant que developpeur, je veux que `app/domaine` soit organise par domaines fonctionnels afin de lire le modele metier par contexte.
   - Statut : `A faire`
   - Resultat attendu : les entites et repositories sont deplaces dans les packages fonctionnels cibles.

4. `PRD-322` En tant que developpeur, je veux que les use cases applicatifs soient rassembles par domaine afin de retrouver rapidement les workflows.
   - Statut : `A faire`
   - Resultat attendu : `app/application/use_cases` n'est plus un package plat.

5. `PRD-323` En tant que developpeur, je veux que les services applicatifs soient rattaches a leur domaine fonctionnel afin d'eviter les services transverses mal delimites.
   - Statut : `A faire`
   - Resultat attendu : les services de session, audit, documents, profils, activites locales, SMS, email et batchs ont un domaine cible.

6. `PRD-324` En tant que mainteneur, je veux conserver l'infrastructure transverse afin de ne pas dupliquer les adapters techniques par domaine.
   - Statut : `A faire`
   - Resultat attendu : `app/infrastructure` reste le point d'integration SQLAlchemy, providers externes, stockage, admin, email, SMS et paiement.

7. `PRD-325` En tant que mainteneur, je veux des regles d'import inter-domaines afin d'eviter les dependances circulaires.
   - Statut : `A faire`
   - Resultat attendu : les imports autorises et interdits sont documentes.

8. `PRD-326` En tant que developpeur, je veux migrer les imports sans facade durable afin de ne pas conserver deux organisations concurrentes.
   - Statut : `A faire`
   - Resultat attendu : les anciens imports plats sont remplaces.

9. `PRD-327` En tant que responsable qualite, je veux des tests de non-regression sur la reorganisation afin de verifier qu'aucun comportement ne change.
   - Statut : `A faire`
   - Resultat attendu : compilation Python, tests d'import et tests applicatifs critiques passent.

10. `PRD-328` En tant que responsable technique, je veux mettre a jour la documentation architecture afin que le decoupage soit compris et maintenu.
   - Statut : `A faire`
   - Resultat attendu : la documentation explique les domaines, leurs responsabilites et les regles de dependance.

11. `PRD-329` En tant que mainteneur, je veux une strategie de migration one-shot coordonnee afin de basculer directement vers l'organisation cible.
   - Statut : `A faire`
   - Resultat attendu : le plan de bascule one-shot est documente par domaine, dependance et consommateur impacte.
   - Resultat attendu : la livraison cible laisse le code compilable, les consommateurs mis a jour et aucune double source de verite durable.

12. `PRD-330` En tant qu'operateur back-office, je veux que le menu d'administration soit organise selon les domaines fonctionnels afin de retrouver les ecrans avec le meme vocabulaire que le backend.
   - Statut : `A faire`
   - Resultat attendu : les categories SQLAdmin reprennent les domaines cibles, avec exceptions transverses explicites.

13. `PRD-331` En tant qu'integrateur frontend/API, je veux que le domaine fonctionnel soit visible dans le path de chaque endpoint afin de comprendre immediatement le contexte metier de l'API appelee.
   - Statut : `A faire`
   - Resultat attendu : les routes canoniques suivent la convention `/{surface}/{domaine}/{ressource}`.

14. `PRD-332` En tant que mainteneur, je veux migrer directement les anciens paths vers les paths canoniques afin de ne pas conserver deux contrats API concurrents.
   - Statut : `A faire`
   - Resultat attendu : les anciens paths ne sont pas conserves comme aliases et les consommateurs sont mis a jour dans la meme livraison.

15. `PRD-333` En tant qu'integrateur API, je veux que chaque operation du contrat OpenAPI porte le domaine fonctionnel comme tag afin de filtrer et lire la documentation selon le meme decoupage que le backend.
   - Statut : `A faire`
   - Resultat attendu : le premier tag OpenAPI de chaque operation metier est le domaine fonctionnel.
   - Resultat attendu : les contrats `/openapi/public.json`, `/openapi/protected.json` et `/openapi/internal.json` exposent chacun uniquement leur surface API.

### Decisions actees

- Le decoupage fonctionnel doit etre visible dans `app/domaine` et `app/application`.
- L'infrastructure reste transverse.
- Le domaine `identite_acces` est retenu pour sessions, tokens, API keys, rate limit, authentification et identifiants commercants.
- Le domaine `documentaire` est retenu et reste distinct du DAM images/media.
- Le domaine `animation_locale` est integre comme enveloppe cible, l'implementation fonctionnelle etant portee par l'Epic 41.
- `TypeCoffretConfig` est classe dans `commercialisation`.
- Aucun domaine `qr` n'est cree : le `qr_token` de `CoffretInstance` et son cycle de vie sont rattaches a `gestion_achats`.
- Les usages de scan et de validation terrain du QR coffret sont rattaches a `exploitation`.
- `QrToken` reste un value object partage entre `gestion_achats` et `exploitation`.
- La signature, verification cryptographique et gestion des cles QR restent dans `infrastructure/securite`.
- `FeedbackPrestation` est rattache a `exploitation` comme signal operationnel post-prestation.
- Une passerelle peut creer un `MessageContact` ou une alerte `support` si un feedback exige un traitement humain, sans deplacer l'objet source.
- Les value objects partages ne doivent pas etre dupliques par domaine.
- Le menu back-office doit reprendre le vocabulaire fonctionnel cible.
- Les vues SQLAdmin restent dans l'infrastructure, mais leurs categories doivent etre alignees sur les domaines.
- Les paths API canoniques doivent contenir le domaine fonctionnel apres la surface (`/public`, `/protected`, `/internal`, `/admin/api`).
- Les tags OpenAPI doivent porter le domaine fonctionnel comme tag principal de chaque operation metier.
- Les surfaces API sont exposees dans trois contrats OpenAPI dedies : `/openapi/public.json`, `/openapi/protected.json` et `/openapi/internal.json`.
- Les documentations interactives dediees sont exposees via `/docs/public`, `/docs/protected` et `/docs/internal`.
- Les anciens paths API ne sont pas conserves comme aliases.
- Les routes publiques migrent en une seule fois.
- La migration est one-shot.
- Les comportements fonctionnels des APIs et les schemas SQL ne changent pas pendant cette reorganisation.

### Points restants a trancher

- Aucun point bloquant restant a ce stade.

---

## Epic 41. Plateforme d'animation locale MVP

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : concevoir et developper un MVP exploitable du `Passeport commercant`, tout en posant un socle generique minimal pour creer, configurer, publier, piloter, cloturer et analyser des animations territoriales.
- Pourquoi maintenant : Localeo peut s'appuyer sur ses briques core existantes, mais doit eviter de construire chaque animation comme un cas specifique non reutilisable.
- Domaine fonctionnel cible : `animation_locale`
- Animation de reference MVP : `Passeport commercant`
- Backlog detaille : [docs/roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md](terminees/epic-41-plateforme-animation-locale-mvp-backlog.md)

### User Stories

1. `PRD-334` En tant que gestionnaire d'animation, je veux consulter le catalogue des modeles d'animations afin de choisir le bon format pour une animation locale.
   - Statut : `A faire`
   - Resultat attendu : le catalogue expose au moins le modele `Passeport commercant`.

2. `PRD-335` En tant que gestionnaire d'animation, je veux creer une animation a partir d'un modele afin de lancer une animation territoriale sans developpement specifique.
   - Statut : `A faire`
   - Resultat attendu : une animation est creee en statut `BROUILLON` avec modele, gestionnaire, organisateur, tenant commune et dates.
   - Resultat attendu : un gestionnaire d'animation ne peut gerer que les animations rattachees a ses tenants communes.
   - Resultat attendu : Localeo n'est pas le canal nominal de creation des animations.

3. `PRD-336` En tant que gestionnaire d'animation, je veux configurer les regles du Passeport commercant afin de definir comment les participants progressent et se qualifient.
   - Statut : `A faire`
   - Resultat attendu : les regles de validation, seuil de qualification et contraintes de dates sont configurables.

4. `PRD-337` En tant que gestionnaire d'animation, je veux selectionner les commercants participants afin de definir les lieux ou etapes de l'animation.
   - Statut : `A faire`
   - Resultat attendu : les commercants sont selectionnes depuis le referentiel core sans duplication.

5. `PRD-338` En tant que gestionnaire d'animation, je veux publier une animation configuree afin de la rendre accessible aux participants.
   - Statut : `A faire`
   - Resultat attendu : une animation non valide ne peut pas etre publiee.

6. `PRD-339` En tant que gestionnaire d'animation, je veux gerer les partenaires contributeurs d'une animation afin de suivre leurs contributions et statistiques.
   - Statut : `A faire`
   - Priorite : `Extension a challenger`
   - Resultat attendu : un partenaire contributeur peut etre invite, accepter l'invitation et etre rattache a l'animation.

7. `PRD-340` En tant que gestionnaire d'animation, je veux gerer des groupes de participants afin d'organiser les participants par classe, equipe, partenaire ou segment.
   - Statut : `A faire`
   - Priorite : `Extension a challenger`
   - Resultat attendu : un participant peut etre rattache a un ou plusieurs groupes selon les regles de l'animation.

8. `PRD-341` En tant que participant, je veux m'inscrire a une animation afin de participer au Passeport commercant.
   - Statut : `A faire`
   - Resultat attendu : l'inscription cree un participant rattache a l'animation.

9. `PRD-342` En tant que participant, je veux consulter ma progression afin de savoir quelles etapes il me reste a valider.
   - Statut : `A faire`
   - Resultat attendu : la progression affiche les etapes validees, restantes et le statut de qualification.

10. `PRD-343` En tant que commercant participant, je veux valider une etape d'un participant afin de certifier sa visite ou action dans mon commerce.
   - Statut : `A faire`
   - Resultat attendu : la validation est rattachee a l'animation, au participant, au commercant et a l'etape.
   - Resultat attendu : la validation terrain se fait par scan du QR participant depuis l'application mobile commercant, qui doit evoluer pour gerer les animations.

11. `PRD-344` En tant que systeme, je veux appliquer des controles anti-fraude MVP afin de limiter les validations abusives.
   - Statut : `A faire`
   - Resultat attendu : les validations trop frequentes, hors dates ou hors commercants eligibles sont refusees ou signalees.

12. `PRD-345` En tant que systeme, je veux qualifier automatiquement les participants afin de constituer la population eligible aux tirages.
   - Statut : `A faire`
   - Resultat attendu : les regles de qualification sont appliquees apres chaque validation et a la cloture.

13. `PRD-346` En tant que gestionnaire d'animation, je veux configurer les coffrets a gagner afin de preparer les recompenses de l'animation.
   - Statut : `A faire`
   - Resultat attendu : chaque lot a gagner reference obligatoirement un coffret Localeo actif de la commune de l'animation.
   - Resultat attendu : les lots libres, lots externes et lots hors commune sont exclus du MVP.
   - Resultat attendu : les lots portent coffret reference, libelle d'affichage, quantite et statut.
   - Resultat attendu : les coffrets offerts en gain sont achetes par le partenaire apres acceptation des commercants, avant publication, et imputes au budget de l'animation.
   - Resultat attendu : le partenaire contributeur est gere seulement si l'extension partenaire est activee.

14. `PRD-347` En tant que systeme, je veux cloturer automatiquement une animation afin de bloquer les nouvelles participations et figer les eligibles.
   - Statut : `A faire`
   - Resultat attendu : la cloture bloque inscriptions et validations nouvelles.

15. `PRD-348` En tant que gestionnaire d'animation, je veux realiser un tirage au sort afin d'attribuer les lots aux participants qualifies.
   - Statut : `A faire`
   - Resultat attendu : le tirage peut etre lance depuis la plateforme partenaire lorsque l'animation est terminee ou cloturee.
   - Resultat attendu : le tirage est bloque tant que la population eligible n'est pas figee.
   - Resultat attendu : le tirage utilise une population eligible tracee.

16. `PRD-349` En tant que gagnant, je veux etre notifie de mon gain afin de connaitre le lot et les modalites de remise.
   - Statut : `A faire`
   - Resultat attendu : les gagnants sont notifies par email et notification push lorsque les canaux sont disponibles et les preferences applicables.
   - Resultat attendu : le push gagnant s'appuie sur l'application Localeo participant avec opt-in et abonnement push actif.
   - Resultat attendu : si le participant dispose d'un abonnement push actif, une notification push est creee avec un contenu sobre et un lien vers le detail de l'animation ou du gain.
   - Resultat attendu : si le canal push n'est pas disponible, l'email collecte a l'inscription sert de canal de repli.
   - Resultat attendu : le systeme evite les doublons de notification pour un meme gain et un meme canal.

17. `PRD-350` En tant que gestionnaire d'animation, je veux consulter le bilan d'une animation afin de mesurer son impact territorial.
   - Statut : `A faire`
   - Resultat attendu : le bilan expose participants total, participants ayant termine l'animation, validations, qualifies, lots, taux de completion et statistiques par commercant et commune tenant.
   - Resultat attendu : les statistiques partenaire contributeur sont gerees seulement si l'extension partenaire est activee.

18. `PRD-351` En tant que gestionnaire d'animation, je veux exporter le bilan afin de partager les resultats avec les partenaires et financeurs.
   - Statut : `A faire`
   - Resultat attendu : un export est disponible et audite.

19. `PRD-352` En tant que responsable technique, je veux que le domaine animation locale soit separe de la marketplace afin d'ajouter de nouveaux modeles sans casser le core commercialisation.
   - Statut : `A faire`
   - Resultat attendu : les objets `animation_locale` ne dupliquent pas communes, commercants, coffrets ou utilisateurs.
   - Resultat attendu : les dependances au core passent par des ports/services explicites.
   - Resultat attendu : le moteur separe le socle generique, la definition de modele et les strategies metier propres a chaque modele.
   - Resultat attendu : les use cases generiques de creation, publication, inscription, workflow, tirage, gains, bilan et dashboard ne contiennent pas de logique metier codee en dur pour le `PASSEPORT_COMMERCANT`.
   - Resultat attendu : une registry permet de retrouver la definition et la strategie d'un modele depuis son code.
   - Resultat attendu : l'ajout d'un nouveau modele doit passer par une nouvelle definition et une nouvelle strategie, sans modifier les invariants communs du moteur.

20. `PRD-353` En tant qu'integrateur API, je veux que les APIs Animation locale respectent les conventions de l'Epic 40 afin de garder des paths et tags OpenAPI coherents.
   - Statut : `A faire`
   - Resultat attendu : les paths canoniques portent `/animation-locale` et le tag OpenAPI principal est `Animation locale`.

21. `PRD-354` En tant que participant, je veux m'inscrire simplement a une animation depuis un QR contextualise afin de participer sans creer de compte.
   - Statut : `A faire`
   - Resultat attendu : le QR d'inscription ouvre une page deja contextualisee avec l'animation.
   - Resultat attendu : le participant saisit email, nom, prenom, telephone et valide les consentements requis.
   - Resultat attendu : le participant recoit par email une confirmation reprenant les informations de l'animation et son QR participant personnel directement dans le message, distinct du QR coffret.

22. `PRD-355` En tant que participant, je veux une application mobile pour suivre mes animations locales afin de retrouver facilement mes participations et mon QR.
   - Statut : `A faire`
   - Resultat attendu : l'application affiche les animations en cours de la commune, les animations auxquelles je suis inscrit et mon historique.
   - Resultat attendu : pour chaque animation, je peux consulter le detail, la progression et mon QR participant.

23. `PRD-356` En tant qu'operateur Localeo, je veux une vision live des animations de la plateforme afin de superviser l'activite sans etre en charge de creer ou animer les animations.
   - Statut : `A faire`
   - Resultat attendu : la vision live affiche les animations publiees, en cours, cloturees ou en anomalie.
   - Resultat attendu : la vision live affiche les inscriptions, validations, qualifications, tirages recents et alertes operationnelles.
   - Resultat attendu : les actions Localeo restent limitees a la supervision, au support et a l'administration exceptionnelle.

24. `PRD-357` En tant que gestionnaire d'animation, je veux travailler dans le tenant de ma commune afin de ne voir et gerer que les animations de mon perimetre.
   - Statut : `A faire`
   - Resultat attendu : un tenant commune reference une commune du referentiel.
   - Resultat attendu : une animation MVP appartient a un seul tenant commune.
   - Resultat attendu : un gestionnaire peut etre habilite sur plusieurs tenants communes.
   - Resultat attendu : le portail impose une selection explicite du tenant commune actif avant creation ou gestion.
   - Resultat attendu : les droits de creation, modification, publication, cloture, tirage et export sont controles par tenant commune.
   - Resultat attendu : le role `GESTIONNAIRE_ANIMATION` autorise le cycle nominal : creer, configurer, modifier une animation non publiee, publier, suivre le live, cloturer, lancer le tirage, envoyer les gains, consulter le bilan et exporter.
   - Resultat attendu : apres publication, les modifications critiques sont bloquees ou passent par une depublication/action explicite selon le statut.
   - Resultat attendu : le gestionnaire ne peut pas modifier les abonnements, acceder a la supervision globale, corriger exceptionnellement une animation hors perimetre ou administrer tous les tenants.
   - Resultat attendu : les listes publiques et l'application mobile participant filtrent les animations par commune.
   - Resultat attendu : Localeo peut agreger la vision live et filtrer par commune.

25. `PRD-358` En tant qu'organisateur ou partenaire, je veux acceder a la plateforme d'animation via un abonnement actif afin que l'usage de la plateforme soit payant et controle.
   - Statut : `A faire`
   - Resultat attendu : un abonnement plateforme Stripe Billing est rattache a une formule, un partenaire donne et une commune donnee.
   - Resultat attendu : le gestionnaire peut consulter son abonnement : formule, statut, dates, perimetre couvert et limitations d'acces.
   - Resultat attendu : le statut d'abonnement actif conditionne l'acces aux fonctions payantes du portail partenaire.
   - Resultat attendu : si l'abonnement expire alors qu'une animation est publiee ou en cours, l'animation va a son terme avant cloture des acces.
   - Resultat attendu : sans abonnement actif, les nouvelles actions payantes hors finalisation d'animation en cours sont bloquees ou degradees selon une regle produit explicite.
   - Resultat attendu : les parcours publics participant et les QR d'animations deja publiees ne sont pas interrompus automatiquement avant la fin de l'animation.
   - Resultat attendu : Localeo peut consulter et modifier l'abonnement pour comprendre les blocages d'acces, corriger un statut, prolonger une periode, changer une formule ou intervenir en support.
   - Resultat attendu : chaque modification d'abonnement est auditee avec acteur, date, ancienne valeur, nouvelle valeur et motif.

26. `PRD-359` En tant qu'organisateur, je veux suivre en live l'etat d'une animation afin de piloter son deroulement sans attendre le bilan final.
   - Statut : `A faire`
   - Resultat attendu : la vue live est accessible depuis la fiche animation de la plateforme partenaire.
   - Resultat attendu : la vue live affiche le statut de l'animation, la periode, le nombre total de participants, le nombre de participants ayant termine l'animation, les inscriptions, les validations recentes, la progression globale et les participants qualifies.
   - Resultat attendu : la vue live affiche les alertes utiles a l'organisateur et les actions disponibles selon le statut et les droits.
   - Resultat attendu : l'organisateur ne voit que les animations de ses tenants communes habilites.
   - Resultat attendu : les donnees live sont rafraichies selon un mecanisme simple MVP, par exemple polling incremental.

27. `PRD-360` En tant que vainqueur, je veux recevoir un coffret deja active lorsque mon gain est envoye afin de pouvoir l'utiliser sans action manuelle supplementaire.
   - Statut : `A faire`
   - Resultat attendu : les coffrets utilisables comme gains ont ete achetes par le partenaire apres acceptation des commercants, avant publication, et appartiennent au budget de l'animation.
   - Resultat attendu : seuls les coffrets actifs de la commune de l'animation peuvent etre configures et envoyes en gain.
   - Resultat attendu : lorsqu'un gain est envoye, le systeme cree une `CoffretInstance` rattachee au gagnant.
   - Resultat attendu : la `CoffretInstance` est automatiquement activee au moment de l'envoi du gain.
   - Resultat attendu : la `CoffretInstance` porte une origine `GAIN_ANIMATION` et reference l'animation, le tirage, le gain et le participant gagnant.
   - Resultat attendu : l'envoi du gain est idempotent et ne peut pas creer plusieurs `CoffretInstances` pour le meme gain.
   - Resultat attendu : l'activation est auditee et visible dans la supervision Localeo et le support.
   - Resultat attendu : la notification gagnant contient les informations utiles pour acceder au coffret active.

28. `PRD-361` En tant qu'organisateur, je veux suivre la consommation des coffrets envoyes aux vainqueurs afin de mesurer l'usage reel des lots distribues.
   - Statut : `A faire`
   - Resultat attendu : la plateforme partenaire liste les coffrets envoyes aux vainqueurs.
   - Resultat attendu : chaque ligne affiche la `CoffretInstance`, le vainqueur, le statut du coffret, la date d'activation, la date d'expiration et le niveau de consommation.
   - Resultat attendu : le detail expose l'identite du gagnant, les commercants, les dates de validation, les prestations restantes et les donnees personnelles masquees selon les droits autorises.
   - Resultat attendu : des alertes signalent les coffrets non consommes, proches expiration, expires ou incoherents.
   - Resultat attendu : les donnees de consommation sont lues depuis `gestion_achats` sans dupliquer les statuts ni les validations.
   - Resultat attendu : l'organisateur ne voit que les coffrets issus des animations de ses tenants communes habilites.

29. `PRD-362` En tant que responsable produit et conformite, je veux appliquer une politique de conservation et d'anonymisation des donnees d'animation afin de limiter l'exposition des donnees personnelles apres l'animation.
   - Statut : `A faire`
   - Resultat attendu : les donnees nominatives participant, email, nom, prenom et telephone, sont conservees jusqu'a fin d'animation + 12 mois puis anonymisees.
   - Resultat attendu : les QR participants, tokens et liens de consultation sont revoques ou supprimes au plus tard fin d'animation + 3 mois.
   - Resultat attendu : les validations detaillees sont conservees 24 mois, puis les references participant nominatives sont anonymisees.
   - Resultat attendu : les tirages et gains sont conserves 5 ans avec donnees participant pseudonymisees lorsque la donnee nominative n'est plus necessaire.
   - Resultat attendu : les exports CSV generes sont supprimes automatiquement apres 90 jours maximum.
   - Resultat attendu : les traces de notification email/push sont conservees 12 mois, puis purgees ou anonymisees techniquement.
   - Resultat attendu : les logs d'audit et de securite lies a l'animation sont conserves 24 mois.
   - Resultat attendu : l'anonymisation supprime email, telephone, nom et prenom, remplace le participant par un identifiant non reversible et conserve uniquement les indicateurs utiles.

30. `PRD-363` En tant que gestionnaire d'animation, je veux generer un flyer PDF contenant le QR et les informations de l'animation afin de disposer d'un support de communication pret a partager.
   - Statut : `A faire`
   - Resultat attendu : le flyer PDF est genere lors de la publication a partir de la configuration et des commercants participants figes, puis peut etre regenere tant que l'animation reste publiee.
   - Resultat attendu : le flyer reprend la charte et le logo Localeo dans un gabarit standard.
   - Resultat attendu : le flyer contient au minimum le nom de l'animation, la commune, les dates, l'organisateur ou partenaire, un court texte de presentation, le QR d'inscription et l'URL d'inscription.
   - Resultat attendu : le QR du flyer est le QR d'inscription public de l'animation et ne contient aucun droit gestionnaire.
   - Resultat attendu : le gestionnaire peut previsualiser, telecharger et regenerer le PDF depuis la plateforme partenaire.
   - Resultat attendu : si les informations publiques ou le QR d'inscription changent avant publication, le PDF existant est marque a regenerer ou remplace lors de la regeneration.
   - Resultat attendu : le PDF partage avant ouverture de l'animation dirige vers une page publique contextualisee qui respecte le statut et la fenetre d'inscription.
   - Resultat attendu : la generation, le telechargement et le remplacement du flyer sont audites.
   - Resultat attendu : le binaire PDF et ses metadonnees sont geres via le domaine `documentaire` ou le service documentaire retenu, sans stockage direct en base `animation_locale`.

31. `PRD-364` En tant que gestionnaire d'animation, je veux visualiser rapidement l'etat d'une animation dans son workflow global afin de savoir ou elle en est et quoi faire ensuite.
   - Statut : `A faire`
   - Resultat attendu : la liste des animations affiche un indicateur de workflow lisible pour chaque animation.
   - Resultat attendu : la fiche animation affiche un workflow global comprenant au minimum : brouillon, configuration, prete a publier, publiee, en cours, cloturee, tirage a lancer, gains a envoyer, bilan disponible, archivee ou annulee.
   - Resultat attendu : l'etape courante, les etapes terminees, les etapes restantes et l'etape suivante attendue sont visibles rapidement.
   - Resultat attendu : les blocages sont visibles avec une raison actionnable : configuration incomplete, abonnement inactif, periode non ouverte, QR non disponible, participants non eligibles, tirage bloque, gains non envoyes ou bilan indisponible.
   - Resultat attendu : les actions affichees dependent du statut, des droits `GESTIONNAIRE_ANIMATION`, du tenant commune actif et de l'abonnement.
   - Resultat attendu : la vue workflow est derivee des statuts, transitions et invariants du domaine ; elle ne cree pas une seconde source de verite.
   - Resultat attendu : Localeo peut voir la meme information en supervision, agregee et filtrable par commune.

32. `PRD-365` En tant que gestionnaire d'animation, je veux consulter un dashboard de performance afin de mesurer l'efficacite de mes animations et comparer leurs resultats.
   - Statut : `A faire`
   - Resultat attendu : le dashboard est accessible depuis la plateforme partenaire dediee.
   - Resultat attendu : le dashboard ne montre que les animations des tenants communes habilites du gestionnaire.
   - Resultat attendu : le dashboard est filtrable par periode, tenant commune, modele d'animation, statut et animation.
   - Resultat attendu : le dashboard affiche les indicateurs globaux : nombre d'animations creees, publiees, en cours, terminees, cloturees et archivees.
   - Resultat attendu : le dashboard affiche les indicateurs de participation : inscrits, participants ayant termine, taux de completion, progression moyenne, participants qualifies et taux de qualification.
   - Resultat attendu : le dashboard affiche les indicateurs terrain : validations totales, validations par animation, validations par commercant participant et validations recentes.
   - Resultat attendu : le dashboard affiche les indicateurs de gains : tirages realises, gagnants, coffrets envoyes, coffrets actifs, coffrets consommes, partiellement consommes, expires et taux de consommation.
   - Resultat attendu : le dashboard permet de comparer plusieurs animations sur les principaux indicateurs MVP.
   - Resultat attendu : les donnees personnelles participant sont exclues des vues agregees ; tout acces au detail nominatif reste limite aux ecrans autorises.
   - Resultat attendu : Localeo peut consulter une vue de performance agregee et filtrable en supervision, sans devenir le gestionnaire des animations.

### Decisions de cadrage

- La plateforme d'animation locale est un nouveau domaine metier distinct de la marketplace.
- Le MVP porte un moteur generique, pas une collection de jeux.
- Le `Passeport commercant` est le premier modele de reference.
- Le moteur separe socle generique, definition de modele, registre et strategie metier par modele ; `PASSEPORT_COMMERCANT` est la premiere strategie, pas le fonctionnement code en dur du moteur.
- Le MVP inclut une plateforme partenaire dediee en self-service pour creer et gerer les animations.
- La plateforme partenaire dediee est la surface produit principale des organisateurs et partenaires ; Localeo n'est pas en charge de creer les animations.
- L'organisateur dispose dans la plateforme partenaire d'une vision live de ses animations pour suivre l'etat, les inscriptions, les validations, la progression, les qualifications, les alertes et les actions disponibles.
- Le gestionnaire doit voir rapidement ou se situe chaque animation dans le workflow global : creation, configuration, publication, animation en cours, cloture, tirage, envoi des gains, bilan et archivage.
- Le gestionnaire dispose d'un dashboard de performance pour mesurer et comparer ses animations sur ses tenants communes habilites.
- Le back-office Localeo conserve une supervision live et des droits d'administration exceptionnels.
- Localeo dispose d'une vision live des animations de la plateforme pour superviser l'activite, detecter les blocages et intervenir en support, sans animer ni creer les animations.
- Le gestionnaire d'animation, organisateur ou partenaire habilite, est dans le coeur MVP ; les partenaires contributeurs/sponsors et groupes sont hors coeur MVP sauf besoin client confirme.
- Le participant MVP ne cree pas de compte ; il s'inscrit depuis un QR d'inscription contextualise avec email, nom, prenom et telephone, puis recoit un email de confirmation avec les informations de l'animation et le QR participant integre.
- Le MVP inclut une application mobile participant pour consulter les animations en cours de la commune, ses inscriptions actives, son historique, le detail d'une animation et son QR participant.
- Les gagnants sont notifies par email et push ; le push impose une application Localeo participant avec opt-in et abonnement push.
- Le tenant fonctionnel MVP est la commune ; il reference une commune du referentiel et porte le perimetre des animations, des droits gestionnaire et des vues participant.
- Une animation MVP appartient a un seul tenant commune ; les animations multi-communes ou territoires composes sont reportes hors MVP.
- Un gestionnaire peut etre habilite sur plusieurs communes des le MVP, avec selection explicite du tenant commune actif.
- Le role MVP `GESTIONNAIRE_ANIMATION` couvre le cycle nominal par tenant commune : creation, configuration, modification avant publication, publication, suivi live, cloture, tirage, envoi des gains, bilan et export.
- Les droits Localeo restent separes : supervision globale, support, correction exceptionnelle, administration tous tenants et modification des abonnements plateforme.
- L'acces a la plateforme partenaire est payant et conditionne par un abonnement Stripe Billing actif, par formule, pour un partenaire donne et une commune donnee.
- Si un abonnement expire alors qu'une animation est publiee ou en cours, l'animation va a son terme avant cloture des acces ; les nouvelles actions payantes peuvent etre bloquees.
- La gestion commerciale des abonnements plateforme doit rester transverse ; `animation_locale` consomme un droit d'acces actif.
- Lorsque l'animation est terminee ou cloturee, le gestionnaire peut lancer un tirage au sort depuis la plateforme partenaire, sur une population eligible figee.
- Les lots a gagner sont obligatoirement des coffrets Localeo actifs de la commune de l'animation ; ils font partie du budget de l'animation et sont achetes par le partenaire avant publication. Depuis l'Epic 56, leur selection et leur achat interviennent apres les acceptations commercants afin de garantir qu'ils contiennent une prestation active d'un participant.
- L'envoi d'un gain au vainqueur cree et active automatiquement la `CoffretInstance` du coffret gagne, rattachee au gain d'animation.
- L'organisateur peut suivre la consommation des coffrets envoyes aux vainqueurs depuis la plateforme partenaire, sans dupliquer les regles `gestion_achats`.
- Le flyer PDF de communication est genere lors de la publication, apres gel des commercants participants ; aucun flyer n'est disponible avant publication.
- Les donnees nominatives participant sont conservees jusqu'a fin d'animation + 12 mois, les QR/tokens jusqu'a fin + 3 mois, les validations detaillees 24 mois, les tirages/gains 5 ans sous forme pseudonymisee, les exports 90 jours maximum et les traces de notification 12 mois.
- La validation MVP utilise le QR participant scanne depuis l'application mobile commercant, qui devra evoluer pour gerer les animations ; ce QR reste distinct du QR coffret.
- Le moteur consomme les donnees core Localeo sans les dupliquer.
- Les concepts de modele, animation, participant, etape, validation, lot, tirage et bilan doivent rester generiques.
- L'assistant IA de generation d'animations est hors MVP.

---

## Epic 42. Localeo Live grand public

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : creer une application grand public `Localeo Live` dediee aux utilisateurs finaux, pour decouvrir l'activite locale, consulter ses coffrets, suivre ses animations, recevoir ses notifications et retrouver ses QR.
- Pourquoi maintenant : le nom `Localeo Live` porte mieux une experience publique de proximite, d'activite locale et de participation qu'une console interne d'exploitation. La creation de cette application impose de clarifier la marque et de renommer l'application interne actuelle.
- Prerequis : l'actuelle PWA interne `Localeo Live` doit etre renommee `Localeo Control` avant l'ouverture du chantier grand public.
- Domaine fonctionnel cible : `experience_publique`
- Backlog detaille : [docs/roadmap/terminees/epic-42-localeo-live-grand-public-backlog.md](terminees/epic-42-localeo-live-grand-public-backlog.md)

### User Stories

1. `PRD-371` En tant qu'operateur Localeo, je veux renommer l'application interne actuelle `Localeo Live` en `Localeo Control` afin de liberer le nom `Localeo Live` pour l'application grand public.
   - Statut : `Termine`
   - Resultat attendu : les libelles visibles de la PWA interne, la page d'accueil backend, les manifestes, les titres, les documentations et les notifications internes utilisent `Localeo Control`.
   - Resultat attendu : les routes techniques existantes peuvent etre conservees temporairement si necessaire, mais les libelles publics et operationnels ne doivent plus exposer `Localeo Live` pour la console interne.

2. `PRD-372` En tant que responsable produit, je veux definir l'identite produit de `Localeo Live` grand public afin de cadrer clairement sa promesse et ses limites.
   - Statut : `A faire`
   - Resultat attendu : une expression de besoin decrit cible, proposition de valeur, parcours principaux, exclusions MVP et articulation avec marketplace, portail partenaire, application commercant et `Localeo Control`.

3. `PRD-373` En tant qu'utilisateur grand public, je veux installer ou ouvrir `Localeo Live` sur mobile afin d'acceder rapidement a mes contenus Localeo.
   - Statut : `A faire`
   - Resultat attendu : l'application est pensee mobile first et installable en PWA ou deployable en application mobile selon arbitrage technique.

4. `PRD-374` En tant qu'utilisateur, je veux consulter mes coffrets et QR depuis `Localeo Live` afin de retrouver facilement mes achats ou cadeaux.
   - Statut : `A faire`
   - Resultat attendu : un coffret accessible par token, compte ou lien securise peut etre affiche dans l'application.

5. `PRD-375` En tant que participant, je veux suivre mes animations locales dans `Localeo Live` afin de voir ma progression, mon QR participant et mes gains.
   - Statut : `A faire`
   - Resultat attendu : les participations issues de l'Epic 41 sont consultables dans l'application.

6. `PRD-376` En tant qu'utilisateur local, je veux decouvrir les activites, animations, commercants et coffrets autour de moi afin de participer a la vie locale.
   - Statut : `A faire`
   - Resultat attendu : l'application propose une entree par commune ou localisation choisie.

7. `PRD-377` En tant qu'utilisateur, je veux recevoir des notifications utiles afin de ne pas rater une validation, une animation, un gain, une expiration ou une actualite locale importante.
   - Statut : `A faire`
   - Resultat attendu : les notifications grand public sont separees techniquement et fonctionnellement des notifications `Localeo Control` et commercants.

8. `PRD-378` En tant qu'utilisateur, je veux creer ou retrouver un profil leger afin de synchroniser mes coffrets, animations et preferences entre appareils.
   - Statut : `Amende - sans compte au MVP`
   - Resultat attendu : l'utilisateur sauvegarde localement ses liens de coffrets et de participations proteges par token.
   - Resultat attendu : aucun compte ni synchronisation multi-appareils n'est implemente au MVP.

9. `PRD-379` En tant que responsable conformite, je veux que `Localeo Live` respecte les exigences RGPD, consentements et minimisation afin de limiter les risques sur une application grand public.
   - Statut : `A faire`
   - Resultat attendu : les donnees collectees, finalites, bases legales, durees de conservation, consentements push/geolocalisation et droits utilisateur sont documentes.

10. `PRD-380` En tant que responsable produit, je veux mesurer l'usage de `Localeo Live` afin de piloter l'adoption sans compromettre la vie privee.
    - Statut : `A faire`
    - Resultat attendu : les indicateurs MVP distinguent installations/ouvertures, consultations de coffrets, inscriptions animations, validations vues, notifications opt-in et interactions avec contenus locaux.

11. `PRD-403` En tant que beneficiaire consultant le detail securise de mon coffret, je veux l'ajouter directement a Localeo Live afin de ne pas recopier son lien.
    - Statut : `A faire - evolution frontend`
    - Resultat attendu : la vue detaillee propose un CTA d'ajout ou d'ouverture dans Localeo Live et l'email peut proposer un raccourci complementaire.
    - Resultat attendu : le token est transfere temporairement par `sessionStorage` sur la meme origine, avec fallback par fragment nettoye immediatement, puis verifie avant sauvegarde locale.
    - Resultat attendu : l'ajout du coffret ne vaut jamais consentement au suivi ou au WebPush.

### Decisions de cadrage

- `Localeo Live` devient le nom reserve a l'application grand public.
- L'actuelle PWA d'exploitation interne devient `Localeo Control`.
- `Localeo Control` reste une surface interne authentifiee, reservee aux profils back-office autorises.
- `Localeo Live` vise les utilisateurs finaux : acheteurs, beneficiaires de coffrets, participants a des animations locales, gagnants et visiteurs interesses par la vie locale.
- Le MVP fonctionne sans compte client, par tokens opaques sauvegardables localement sur l'appareil.
- Les notifications push grand public sont distinctes des WebPush internes `Localeo Control` et des notifications commercants.
- Les animations locales de l'Epic 41 sont un cas d'usage structurant, mais l'application ne doit pas etre limitee a ce seul domaine.
- La PWA est integree a `localeo-marketplace` sous `/live`, avec manifeste et service worker dedies.
- Le feed reutilise `activites_locales`; les news sont creees manuellement et scopees sur zero, une ou plusieurs villes du referentiel existant.
- La commune est selectionnee manuellement au MVP, sans geolocalisation.
- Les publications editoriales sont creees, programmees, publiees et moderees depuis le backend/back-office.
- La vue detaillee d'un coffret constitue un point d'entree prioritaire vers son ajout volontaire dans la bibliotheque Localeo Live.

---

## Epic 43. Suivi des virements bancaires Stripe Connect

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : prolonger le suivi des reversements Stripe Connect jusqu'au virement vers le compte bancaire du commercant, en distinguant transfer vers le solde Stripe et virement bancaire.
- Pourquoi maintenant : l'EPIC 39 confirme les Transfers vers les comptes connectes, mais Localeo ne suit pas encore les payouts bancaires, leurs regroupements, leurs dates d'arrivee ni leurs echecs tardifs.
- Prerequis : EPIC 39 Stripe Connect et payouts automatiques des comptes Express actifs.
- Domaine fonctionnel cible : `gestion_reversement`
- Backlog detaille : [docs/roadmap/terminees/epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md](terminees/epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md)
- Architecture : [docs/architecture/epics/epic-43-suivi-payouts-stripe-connect-architecture.md](../architecture/backend/epics/epic-43-suivi-payouts-stripe-connect-architecture.md)

### User Stories

1. `PRD-381` En tant qu'operateur technique, je veux recevoir les evenements payout des comptes connectes afin de suivre le versement bancaire apres le transfer Stripe.
   - Statut : `A faire`
   - Resultat attendu : le webhook Connect accepte et verifie les evenements `payout.created`, `payout.updated`, `payout.paid`, `payout.failed`, `payout.canceled` et `payout.reconciliation_completed`.
   - Resultat attendu : `account.external_account.updated` complete `account.updated` et une version Stripe API v1 commune est epinglee sur le backend et la destination d'evenements.

2. `PRD-382` En tant que responsable finance, je veux disposer d'une projection locale des payouts Stripe afin de connaitre leur montant, leur destination masquee et leur statut.
   - Statut : `A faire`
   - Resultat attendu : une entite `PayoutStripe` idempotente conserve les references, montants, statuts, dates et echecs utiles sans coordonnees bancaires completes.
   - Resultat attendu : statut Stripe et statut de rapprochement sont stockes separement.

3. `PRD-383` En tant que systeme de rapprochement, je veux conserver la reference `destination_payment` du Transfer afin de relier le credit du compte connecte au reversement Localeo.
   - Statut : `A faire`
   - Resultat attendu : le port, le gateway et la projection de Transfer conservent la reference `py_...` exposee par Stripe.

4. `PRD-384` En tant que systeme, je veux projeter les webhooks payout de maniere idempotente et independante de leur ordre afin de conserver un etat bancaire coherent.
   - Statut : `A faire`
   - Resultat attendu : les doublons sont ignores et un `payout.failed` tardif peut corriger une projection precedemment `paid`.

5. `PRD-385` En tant que responsable finance, je veux rapprocher chaque payout automatique des transfers qu'il contient afin de justifier les montants verses en banque.
   - Statut : `A faire`
   - Resultat attendu : les balance transactions filtrees par payout sur le compte connecte sont rapprochees de `destination_payment`, puis des paiements de reversement.

6. `PRD-386` En tant que commercant, je veux distinguer le transfer vers mon compte Stripe du versement vers ma banque afin de comprendre ou se trouvent mes fonds.
   - Statut : `A faire`
   - Resultat attendu : l'API existante expose de facon additive une liste `virements_bancaires`, des codes publics `VIREMENT_*`, la date d'arrivee estimee et un motif d'echec public lorsqu'ils sont disponibles.

7. `PRD-387` En tant qu'application commercant, je veux afficher la chronologie du reversement jusqu'au compte bancaire afin de donner une information claire au partenaire.
   - Statut : `A faire`
   - Resultat attendu : l'interface distingue reversement transmis a Stripe, virement bancaire a venir, en cours, effectue et en echec, sans afficher `payout`, `paid`, `failed`, `rapprochement` ou `po_...`.

8. `PRD-388` En tant qu'operateur finance ou support, je veux superviser les payouts et leurs echecs afin de traiter les incidents bancaires sans confondre transfer et payout.
   - Statut : `A faire`
   - Resultat attendu : le back-office et les routes protegees par `internal:finance` recherchent et affichent payouts, reversements rapproches, dates, destination masquee, statut et cause d'echec.
   - Resultat attendu : les anomalies sont persistantes, les alertes critiques sont envoyees par email a la finance/support et les echecs sont notifies au commercant par email et WebPush activee.

9. `PRD-389` En tant que responsable exploitation, je veux pouvoir reconciler les payouts manquants ou incomplets sans creer de nouveau flux financier afin de reparer les projections locales.
   - Statut : `A faire`
   - Resultat attendu : une reprise idempotente enrichit les anciens transfers et rapproche les payouts recents sans creer de Transfer ou Payout.
   - Resultat attendu : les batchs audites couvrent le rattrapage, le controle nocturne et la purge quotidienne avec `dry_run` selon les durees de conservation actees.

10. `PRD-390` En tant que responsable qualite, je veux tester les parcours payout nominaux et en echec afin de securiser le passage en production.
    - Statut : `A faire`
    - Resultat attendu : les tests couvrent regroupement, desordre, doublon, echec tardif, transaction inconnue, plusieurs tentatives et isolation des comptes connectes.

### Decisions de cadrage

- Les payouts automatiques Stripe sont conserves ; Localeo ne cree pas un payout manuel par reversement dans le MVP.
- `Reversement.statut = PAYE` signifie que le transfer vers le solde Stripe connecte est confirme.
- Le stockage distingue le statut Stripe du payout et le statut de rapprochement Localeo ; l'API commercant calcule des codes publics `VIREMENT_*`.
- Un payout peut regrouper plusieurs reversements et un reversement peut connaitre plusieurs tentatives apres echec.
- Le rapprochement utilise `destination_payment` et les balance transactions Stripe, jamais le montant seul.
- Les coordonnees bancaires completes restent chez Stripe.
- La table d'association payout/paiement de reversement devient la source de verite ; `PaiementReversement.stripe_payout_id` est migre puis supprime sans double ecriture durable.
- Un payout `paid` conserve son statut Stripe tandis que son rapprochement evolue de `EN_ATTENTE` ou `EN_COURS` vers `RAPPROCHE`, `NON_RAPPROCHE` ou, sans detail exploitable pour un payout manuel ou instantane, `NON_RAPPROCHABLE`.
- Le rattrapage s'execute toutes les 6 heures sur 14 jours, avec un controle nocturne sur 90 jours et un backfill initial depuis le premier Transfer Connect.
- L'absence de payout est alertee a J+2 puis J+5 ouvrables apres la date attendue, avec des seuils de repli J+7/J+10 lorsque le calendrier est indisponible et aucune alerte pour un calendrier manuel.
- Un `payout.failed` tardif ne retrograde pas le reversement `PAYE`, mais declenche une alerte critique et une information commercant sans nouveau flux automatique.
- Les informations financieres normalisees sont conservees 10 ans apres cloture d'exercice, le payload minimise et le detail technique 13 mois, et `trace_id.value` 5 ans en acces restreint, sous validation juridique et DPO.
- Le backend, la destination Connect et les tests utilisent une version Stripe API v1 commune et epinglee ; les payouts ne dependent pas des evenements Accounts v2.
- Le vocabulaire commercant est `virement bancaire` ; `payout` et les identifiants `po_...` restent techniques.
- Restent a confirmer avant production : durees de conservation par le juridique/DPO, seuils par la finance et taxonomie des motifs d'echec par le produit/support.

---

## Epic 44. Observabilite et logs des Use Cases

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : journaliser chaque invocation de Use Case dans un format
  correlable et exploitable, sans exposer de secrets ou de donnees personnelles
  inutiles.
- Pourquoi maintenant : l'exploitation doit pouvoir retrouver rapidement quel
  traitement applicatif a ete execute, avec quelle issue et quelle duree, quel
  que soit son point d'entree HTTP, back-office, webhook ou batch.
- Domaine fonctionnel cible : transverse `observabilite`.
- Backlog detaille :
  [docs/roadmap/terminees/epic-44-observabilite-logs-use-cases-backlog.md](terminees/epic-44-observabilite-logs-use-cases-backlog.md)
- Architecture :
  [docs/architecture/epics/epic-44-observabilite-logs-use-cases-architecture.md](../architecture/backend/epics/epic-44-observabilite-logs-use-cases-architecture.md)

### User Stories

1. `PRD-391` En tant qu'exploitant, je veux disposer d'un log pour chaque appel
   de Use Case afin de savoir quels traitements applicatifs ont reellement ete
   executes.
   - Statut : `Termine backend`
   - Resultat attendu : toute methode publique `execute`, synchrone ou
     asynchrone, emet un evenement de debut puis exactement un evenement de
     succes ou d'echec.
   - Resultat attendu : un identifiant unique relie le debut et la fin sans
     modifier le comportement du Use Case.

2. `PRD-392` En tant qu'exploitant, je veux un schema de log stable et structure
   afin de rechercher et agreger les executions sans analyser des messages
   libres.
   - Statut : `Termine backend`
   - Resultat attendu : les evenements exposent un schema versionne incluant
     Use Case, domaine, evenement, issue et duree.
   - Resultat attendu : le format de production est exploitable comme JSON
     structure.

3. `PRD-393` En tant que support technique, je veux suivre une execution de bout
   en bout afin de retrouver tous les logs associes a une meme action.
   - Statut : `Termine backend`
   - Resultat attendu : les contextes HTTP, batch, webhook et back-office
     propagent leurs identifiants de correlation.
   - Resultat attendu : les appels imbriques portent un identifiant parent.

4. `PRD-394` En tant que responsable securite et conformite, je veux que les
   logs soient minimises afin qu'ils ne deviennent pas une source de fuite de
   donnees.
   - Statut : `Termine backend`
   - Resultat attendu : secrets, tokens, mots de passe, QR, signatures, IBAN et
     payloads provider complets ne sont jamais journalises.
   - Resultat attendu : les identifiants metier utiles sont exposes par liste
     blanche et couverts par des tests de redaction.

5. `PRD-395` En tant qu'exploitant, je veux distinguer les succes, erreurs
   metier et erreurs techniques afin de prioriser correctement les incidents.
   - Statut : `Termine backend`
   - Resultat attendu : l'issue est qualifiee par un code stable et un niveau de
     log adapte.
   - Resultat attendu : les exceptions techniques conservent une stack trace
     assainie et sont relancees.

6. `PRD-396` En tant que responsable exploitation, je veux mesurer la duree des
   Use Cases afin d'identifier les lenteurs et regressions.
   - Statut : `Termine backend`
   - Resultat attendu : chaque evenement terminal contient `duration_ms`.
   - Resultat attendu : volumes, taux d'echec et percentiles de duree sont
     agregeables par Use Case.

7. `PRD-397` En tant que responsable qualite, je veux empecher l'ajout d'un Use
   Case non journalise afin de conserver une couverture complete dans le temps.
   - Statut : `Termine backend`
   - Resultat attendu : un inventaire et un test de contrat garantissent la
     couverture de tous les Use Cases eligibles.
   - Resultat attendu : l'instrumentation reste idempotente apres rechargement.

8. `PRD-398` En tant qu'exploitant, je veux piloter le niveau des logs sans
   redeployer le code afin d'adapter la verbosite au contexte.
   - Statut : `Termine backend`
   - Resultat attendu : `LOCALEO_USE_CASES_LOG_LEVEL` pilote le namespace
     canonique `localeo.use_cases.*`.
   - Resultat attendu : le diagnostic detaille est separe du contrat nominal et
     aucun niveau ne permet d'exposer des secrets.

9. `PRD-399` En tant qu'operateur, je veux rechercher les logs par identifiant
   et Use Case afin de diagnostiquer rapidement un incident.
   - Statut : `A finaliser - configuration Better Stack et Render`
   - Resultat attendu : un outil centralise permet une recherche par
     `request_id`, correlation, invocation, Use Case, issue et periode.
   - Resultat attendu : des dashboards et alertes couvrent erreurs et lenteurs.

10. `PRD-400` En tant qu'equipe d'exploitation, je veux une procedure de lecture
    et de recette afin d'utiliser le nouveau dispositif de maniere homogene.
    - Statut : `A finaliser - recette environnement partage`
    - Resultat attendu : schema, niveaux, champs, recherche et diagnostic sont
      documentes.
    - Resultat attendu : une recette verifie les contextes, issues, correlations
      et la redaction des secrets.

11. `PRD-401` En tant qu'utilisateur ou operateur support, je veux que chaque
    erreur contienne un `correlationId` afin de transmettre une reference unique
    et retrouver les logs associes.
    - Statut : `Backend termine - applications clientes a adapter`
    - Resultat attendu : toute reponse HTTP 4xx ou 5xx contient un
      `correlationId` non vide, y compris les erreurs de validation, securite,
      route inexistante et erreurs techniques inattendues.
    - Resultat attendu : la valeur est identique dans la reponse, le header et
      les logs ; sur HTTP elle correspond au `request_id` interne existant.
    - Resultat attendu : les erreurs de batch et du back-office rendent aussi
      leur correlation visible a l'operateur.
    - Resultat attendu : les references generees par Localeo suivent le format
      reconnaissable `LOC-<UUID>` et les interfaces affichent `Reference erreur`,
      une consigne de communication au support et une action de copie.

12. `PRD-402` En tant que developpeur, je veux que la journalisation soit
    pilotee par un utilitaire transverse afin de garantir un format et un
    contexte homogenes sur tous les points d'entree.
    - Statut : `Termine backend`
    - Resultat attendu : une facade unique gere schema, formatage, niveaux,
      durees, redaction, troncature, emission et contexte de correlation.
    - Resultat attendu : les adaptateurs HTTP, webhook, batch et back-office
      fournissent leur contexte sans reconstruire les champs communs.
    - Resultat attendu : le `User-Agent` est assaini et borne, et tout
      `correlationId` entrant est valide avant d'etre propage.
    - Resultat attendu : l'instrumentation des Use Cases utilise la facade et
      une panne de journalisation ne modifie jamais le traitement metier.

### Decisions actees

- L'exigence couvre chaque invocation de Use Case public.
- L'instrumentation est centralisee autour des methodes `execute`, pas ajoutee
  manuellement dans chaque classe.
- Chaque invocation emet `use_case.started`, puis exactement un evenement
  `use_case.succeeded` ou `use_case.failed`.
- Le namespace canonique est `localeo.use_cases.*`.
- Les logs completent l'audit persistant et les evenements metier sans les
  remplacer.
- Les arguments et resultats complets sont interdits dans les logs nominaux de
  production.
- Une panne du collecteur ne doit pas interrompre un traitement metier.
- Toute erreur expose un `correlationId` communicable au support ; sur HTTP il
  correspond au `request_id` interne et n'introduit pas un second identifiant.
- Le format, le contexte, le `correlationId`, le `User-Agent`, la redaction et
  l'emission sont pilotes par l'utilitaire transverse d'observabilite.
- Better Stack Telemetry en region Allemagne est le collecteur cible, alimente
  par un Log Stream Render ; l'application reste independante du fournisseur.
- Le format est JSON structure en test, preproduction et production ; le local
  peut conserver un rendu texte avec les memes champs.
- La retention cible est de 14 jours en test, 30 jours en preproduction et
  90 jours en production.
- Le seuil lent nominal est de 2 000 ms. Les alertes couvrent le p95, le taux
  d'echec technique et le premier echec definitif des flux critiques.
- Les identifiants metier suivent une liste blanche ; les donnees personnelles,
  secrets et payloads complets sont interdits.
- L'exploitation et les responsables techniques accedent aux logs assainis ;
  le support recherche par `correlationId` et les autres profils utilisent des
  vues agregees selon leurs habilitations.
- `correlationId` est canonique ; `request_id` reste un alias deprecie et
  strictement egal jusqu'a une version majeure de l'API.
- OpenTelemetry est reporte en phase 2, avec `trace_id` et `span_id` reserves
  comme champs optionnels.
- Le forfait Better Stack et la validation DPO de la retention restent des
  validations de mise en production non bloquantes pour l'implementation.

---

## Epic 45. Vision 360 Animation backend

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : fournir au back-office une vision 360 consolidee d'une animation, de son etat courant a son historique, ses performances et ses alertes.
- Positionnement : vision 360 interne centree sur une animation, complementaire du pilotage live, du bilan et du dashboard multi-animations de l'Epic 41.
- Domaine fonctionnel cible : `animation_locale`.
- Backlog detaille : [docs/roadmap/terminees/epic-45-vision-360-animation-backend-backlog.md](terminees/epic-45-vision-360-animation-backend-backlog.md).

### User Stories

1. `PRD-405` Rechercher une animation par reference, nom, partenaire, commune, statut et periode.
2. `PRD-406` Consulter sa synthese consolidee et son workflow.
3. `PRD-407` Analyser ses KPI et series temporelles sur une periode maximale de 365 jours.
4. `PRD-408` Parcourir sa chronologie multi-sources paginee.
5. `PRD-409` Consulter ses participants et leur progression selon les habilitations.
6. `PRD-410` Superviser les tirages, gagnants, gains et coffrets attribues.
7. `PRD-411` Identifier les anomalies actionnables a partir de codes stables.
8. `PRD-412` Securiser, auditer et observer les API internes de la Vision 360.

### Decisions de cadrage actees

- reutiliser les donnees et calculs de l'Epic 41 sans creer de seconde source de verite ;
- borner les agregats a 365 jours et toutes les listes par pagination ;
- masquer les donnees personnelles par defaut et auditer leur consultation complete ;
- reserver le MVP aux profils internes habilites ;
- conserver les actions metier dans les use cases existants ; la Vision 360 fournit des liens et non des mutations directes.
- ajouter une reference metier immutable `ANIM-XXXXXXXX` en complement de l'UUID ;
- autoriser `ADMIN` sur toute la plateforme et cloisonner `EXPLOITATION` sur ses communes habilitees ;
- retenir `/internal/animation-locale/vision-360` pour les six endpoints internes ;
- utiliser une pagination par curseur pour chronologie et participants, et page/taille pour la recherche ;
- viser moins de 500 ms pour recherche/synthese et moins de 1,5 s pour les agregats annuels.

---

## Epic 46. Paiement professionnel des lots Animation

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : permettre au partenaire organisateur de payer en une fois, via Stripe, tous les coffrets constituant les lots d'une animation, puis de les reserver sans activation jusqu'a leur attribution.
- Positionnement : extension de l'Epic 41, reposant sur `gestion_achats`, les documents d'achat, Stripe Checkout, Stripe Connect et le webhook Stripe.
- Epic detaillee : [docs/roadmap/terminees/epic-46-paiement-lots-animation.md](terminees/epic-46-paiement-lots-animation.md).
- Conception : [docs/specifications/epic-46-paiement-lots-animation/README.md](../specifications/epic-46-paiement-lots-animation/README.md).

### User Stories

1. Creer une commande professionnelle multi-lignes et un checkout Stripe unique pour tous les lots configures.
2. Confirmer le paiement par webhook et materialiser idempotemment les achats enfants et les instances reservees.
3. Interdire la publication tant que la couverture financiere et le stock reserve ne sont pas complets.
4. Consulter depuis l'animation le recu consolide et le dossier de facturation de la commande.
5. Attribuer une instance reservee et l'activer uniquement lors de l'envoi irreversible du gain.
6. Cloturer pour figer les eligibles, puis attribuer tous les lots achetes lors du tirage.
7. Reprendre et reconcilier les echecs sans double debit, double stock ni double activation.

### Livraison backend du 21 aout 2026

- migration `v173_epic46_commandes_lots_animation.sql` et readiness associee ;
- commande multi-lignes, checkout Stripe unique, webhook idempotent et reconciliation ;
- publication conditionnee par les instances reservees, tirage de tous les lots et activation a l'envoi ;
- documents depuis l'animation, remboursement total avant publication et vues SQLAdmin de support ;
- contrat OpenAPI Animation regenere. La recette Stripe Test, la validation comptable/juridique et le frontend restent a finaliser.

### Decisions de cadrage actees

- une seule commande et un seul checkout Stripe par version de configuration ;
- commande et lignes possedees par `gestion_achats`, avec paiement unique resolvable depuis chaque achat enfant ;
- acheteur professionnel identifie par le partenaire organisateur et snapshot de facturation fige ;
- retrait direct du financement Animation par ligne, non deploye en production, sans couche de compatibilite ;
- remboursement total uniquement avant publication et sans instance activee au MVP ;
- `EUR`, 20 lignes et 100 instances maximum, avec plafond monetaire configurable ;
- desactivation commerciale non bloquante apres paiement, mais regularisation obligatoire pour un blocage legal, fraude ou securite ;
- cloture et gel des eligibles avant tirage ; attribution de tous les lots obligatoire lors du tirage ; association de l'instance lors de l'envoi du gain.

---

## Epic 47. Souscription et paiement de l'abonnement partenaire Animation

- Criticite : `Critique`
- Statut : `Termine` - cloture produit confirmee le 15 septembre 2026.
- Objectif : compléter le référencement d'un partenaire par une souscription
  tarifée, un paiement Stripe ou une gratuité auditée, puis activer les droits
  Animation uniquement après validation financière.
- Positionnement : évolution du domaine transverse `abonnements_plateforme` et
  du parcours **Animations locales > Référencer un partenaire**.
- Backlog détaillé :
  [docs/roadmap/terminees/epic-47-souscription-abonnement-partenaire-animation-backlog.md](terminees/epic-47-souscription-abonnement-partenaire-animation-backlog.md).
- Conception :
  [docs/specifications/epic-47-souscription-abonnement-partenaire-animation/README.md](../specifications/epic-47-souscription-abonnement-partenaire-animation/README.md).

### Offres initiales

- `DECOUVERTE` : 390 € HT, une animation clé en main ;
- `ESSENTIELLE` : 708 € HT, accès plateforme pendant un an et animations
  illimitées ;
- prix catalogue administrable et prix propre à chaque souscription ;
- remise, majoration ou gratuité justifiée et auditée.

### User Stories

1. `PRD-415` Paramétrer les offres, prix catalogue, durées et quotas.
2. `PRD-416` Choisir l'offre pendant le référencement du partenaire.
3. `PRD-417` Définir et justifier un prix négocié.
4. `PRD-418` Accorder une gratuité sans paiement fictif.
5. `PRD-419` Générer ou reprendre un lien Stripe Checkout.
6. `PRD-420` Envoyer la demande de paiement par l'outbox email.
7. `PRD-421` Activer exclusivement après webhook Stripe confirmé.
8. `PRD-422` Inviter le premier utilisateur après activation.
9. `PRD-423` Contrôler le quota Découverte et la durée Essentielle.
10. `PRD-424` Piloter et reprendre les souscriptions depuis le back-office.
11. `PRD-425` Recetter et documenter le parcours.
12. `PRD-426` Intégrer les abonnements encaissés au suivi du CA dans le
    dashboard opérationnel et Localeo Control.

### Décisions de cadrage actées

- séparer la souscription commerciale en attente de l'abonnement actif ;
- conserver le catalogue comme prix de référence et snapshoter le prix négocié ;
- ne jamais activer depuis la redirection navigateur Stripe ;
- ne créer aucune transaction Stripe pour une gratuité ;
- envoyer l'invitation portail après activation ;
- appliquer le prix au couple partenaire + commune et créer une souscription
  distincte pour chaque commune ;
- afficher les abonnements encaissés HT et TTC séparément du CA coffrets, avec
  une affectation directe à la commune et sans double comptage global ;
- retenir au MVP un paiement prépayé sans renouvellement automatique ;
- rendre la date de fin visible et signaler les expirations prochaines dans le
  back-office et Localeo Animation ;
- consommer le crédit Découverte à la première publication réussie pendant sa
  période de validité de douze mois.

---

## Epic 48. Ordonnancement des batchs avec APScheduler

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : automatiser les batchs Localeo avec APScheduler en réutilisant le
  catalogue, les verrous, l'historique et la supervision de l'Epic 23.
- Hébergement : scheduler intégré au lifespan du service FastAPI existant sur
  Render, avec un leader unique élu par lease PostgreSQL.
- Backlog détaillé :
  [docs/roadmap/terminees/epic-48-apscheduler-ordonnancement-batchs-backlog.md](terminees/epic-48-apscheduler-ordonnancement-batchs-backlog.md).
- Conception :
  [docs/specifications/epic-48-apscheduler-ordonnancement-batchs/README.md](../specifications/epic-48-apscheduler-ordonnancement-batchs/README.md).

### User Stories

1. `PRD-427` Héberger l'ordonnanceur dans FastAPI avec un leader unique.
2. `PRD-428` Structurer les planifications et configurer leurs fréquences par environnement.
3. `PRD-429` Déclencher les endpoints HTTP protégés.
4. `PRD-430` Enregistrer les jobs APScheduler idempotemment.
5. `PRD-431` Empêcher les exécutions concurrentes.
6. `PRD-432` Gérer les retards et redémarrages.
7. `PRD-433` Gérer le cycle de vie du scheduler avec le lifespan FastAPI.
8. `PRD-434` Superviser le leader et son heartbeat.
9. `PRD-435` Présenter les planifications dans le back-office.
10. `PRD-436` Configurer et sécuriser l'ordonnanceur.
11. `PRD-437` Tester l'ordonnancement avec une horloge contrôlée.
12. `PRD-438` Déployer et basculer sans double ordonnanceur.

### Décisions de cadrage actées

- ne pas créer de service Render supplémentaire ;
- intégrer `BackgroundScheduler` au lifespan FastAPI ;
- élire un seul leader par lease PostgreSQL, même avec plusieurs workers ou
  pendant le recouvrement d'un déploiement ;
- configurer les fréquences avec une variable d'environnement par batch et un
  défaut applicatif validé ;
- appeler les endpoints HTTP `/protected` avec une clé API `internal:batch`,
  sans invocation directe des use cases par APScheduler ;
- conserver `BatchRunner`, `executions_batch` et `verrous_batch` comme socle ;
- exiger une instance Render toujours active pour garantir les échéances.

---

## Epic 49. Visibilite des animations dans la Marketplace

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : exposer les animations publiques eligibles sur l'accueil, les pages
  ville, commercant et coffret ainsi que dans un catalogue Marketplace dedie.
- Regle structurante : l'eligibilite est calculee par le backend a partir de
  l'animation, de sa configuration, de la ville existante et de l'abonnement du
  couple `(partenaire_id, commune_id)` ; le frontend ne la reconstruit jamais.
- Backlog detaille :
  [docs/roadmap/terminees/epic-49-animations-marketplace-backlog.md](terminees/epic-49-animations-marketplace-backlog.md).
- Conception :
  [docs/specifications/epic-49-animations-marketplace/README.md](../specifications/epic-49-animations-marketplace/README.md).

### User Stories

1. `PRD-439` Centraliser l'eligibilite publique des animations.
2. `PRD-440` Creer le catalogue public territorial.
3. `PRD-441` Afficher les animations sur la page ville.
4. `PRD-442` Afficher les animations liees sur la page commercant.
5. `PRD-443` Afficher les animations liees sur la page coffret.
6. `PRD-444` Afficher une synthese territoriale sur l'accueil.
7. `PRD-445` Stabiliser les contrats publics de liste et de synthese.
8. `PRD-446` Couvrir qualite, accessibilite, SEO et mesure.
9. `PRD-447` Ajouter les animations a la recherche Marketplace.

### Conception initiale

- faire evoluer de maniere additive la liste et le detail deja consommes par
  Localeo Live ;
- ajouter une synthese publique utilisant strictement le meme predicat que la
  liste ;
- distinguer le statut public derive de l'indicateur d'inscription ouverte ;
- ne jamais dupliquer le concept de ville sous une nouvelle entite commune ;
- masquer les blocs contextuels lorsqu'ils sont vides ou indisponibles afin de
  ne jamais bloquer les parcours coffret.
- n'autoriser la visibilite publique que pour un abonnement strictement `ACTIF` ;
- utiliser `commune` comme terme metier pour l'unique referentiel stocke dans
  la table historique `villes`, sans duplication du concept ;
- limiter le lien coffret-animation aux coffrets presents dans les `lots` de la configuration publiee, avec la nature publique `LOT_A_GAGNER`.

---

## Epic 50. Politique BUM et conformite fiscale des coffrets

- Criticite : `Haute`
- Statut : `Termine cote produit et backend - activation conditionnee a la decision interne Localeo, aux controles Finance applicables et aux recettes externes`
- Objectif : ne commercialiser que des coffrets qualifies comme Bons a Usages
  Multiples, tracer cette qualification et distinguer acquisition, execution,
  reversement et facturation de la prestation, tout en guidant l'onboarding
  terrain des commercants depuis une application mobile interne.
- Regle structurante : une offre n'est publiable que si
  `taxQualification = MULTI_PURPOSE` et
  `qualificationStatus = VALIDATED`, quel que soit son type commercial Solo ou
  Multi.
- Backlog detaille :
  [docs/roadmap/terminees/epic-50-conformite-fiscale-bum-backlog.md](terminees/epic-50-conformite-fiscale-bum-backlog.md).
- Conception :
  [docs/specifications/epic-50-conformite-fiscale-bum/README.md](../specifications/epic-50-conformite-fiscale-bum/README.md).
- Specification fonctionnelle :
  [docs/specifications/epic-50-conformite-fiscale-bum/specification-fonctionnelle.md](../specifications/epic-50-conformite-fiscale-bum/specification-fonctionnelle.md).
- Conception technique :
  [docs/specifications/epic-50-conformite-fiscale-bum/conception-technique.md](../specifications/epic-50-conformite-fiscale-bum/conception-technique.md).
- Analyse de l'existant :
  [docs/specifications/epic-50-conformite-fiscale-bum/analyse-existant-impacts.md](../specifications/epic-50-conformite-fiscale-bum/analyse-existant-impacts.md).
- Workflow documentaire et facturation post-execution :
  [docs/specifications/epic-50-conformite-fiscale-bum/workflow-demandes-factures.md](../specifications/epic-50-conformite-fiscale-bum/workflow-demandes-factures.md).
- Factures de commission et d'abonnement Animation :
  [docs/specifications/epic-50-conformite-fiscale-bum/factures-localeo.md](../specifications/epic-50-conformite-fiscale-bum/factures-localeo.md).
- Onboarding commercant mobile :
  [docs/specifications/epic-50-conformite-fiscale-bum/onboarding-commercant-mobile.md](../specifications/epic-50-conformite-fiscale-bum/onboarding-commercant-mobile.md).

### User Stories

1. `PRD-448` Valider la politique BUM et ses formulations.
2. `PRD-449` Versionner et configurer les regles de screening.
3. `PRD-450` Completer le profil fiscal et l'attestation partenaire.
4. `PRD-451` Collecter le questionnaire d'eligibilite d'une prestation.
5. `PRD-452` Executer le screening d'eligibilite.
6. `PRD-453` Qualifier et historiser une prestation ou un coffret.
7. `PRD-454` Bloquer la publication des offres non conformes.
8. `PRD-455` Distinguer promesse garantie et contenu indicatif.
9. `PRD-456` Generer le justificatif d'acquisition BUM.
10. `PRD-457` Etendre le justificatif aux commandes Pro et Animation.
11. `PRD-458` Gerer les profils de facturation et types d'acheteur.
12. `PRD-459` Aligner le cycle financier sur la consommation.
13. `PRD-460` Identifier les consommations facturables.
14. `PRD-461` Creer des demandes de facture unitaires ou groupees.
15. `PRD-462` Notifier et permettre le traitement par le commercant.
16. `PRD-560` Assister le commercant dans l'emission de sa facture.
17. `PRD-463` Suivre les demandes cote Pro et Animation.
18. `PRD-464` Piloter la conformite fiscale dans le BackOffice.
19. `PRD-465` Detecter les modifications imposant une requalification.
20. `PRD-466` Couvrir securite, activation et non-regression.
21. `PRD-467` Collecter et valider les references Chorus Pro.
22. `PRD-468` Piloter le depot manuel des factures dans Chorus Pro.
23. `PRD-469` Mandater Localeo pour le depot des factures commercants.
24. `PRD-470` Creer l'aggregate commun de facture Localeo.
25. `PRD-471` Facturer la commission au commercant.
26. `PRD-472` Facturer la souscription au partenaire Animation.
27. `PRD-473` Generer les PDF de maniere idempotente.
28. `PRD-474` Calculer le credit des prestations non utilisees.
29. `PRD-475` Gerer le registre et les reservations de credit.
30. `PRD-476` Utiliser le credit dans les commandes Animation et Pro.
31. `PRD-477` Exposer le credit dans Animation et la Marketplace Pro.
32. `PRD-478` Regrouper les demandes de facture par achat Pro et commercant.
33. `PRD-551` Creer et reprendre un dossier d'onboarding terrain.
34. `PRD-552` Piloter une checklist versionnee et conditionnelle.
35. `PRD-553` Completer le referentiel commercant pendant le rendez-vous.
36. `PRD-554` Capturer et classer les documents signes.
37. `PRD-555` Finaliser les prestations et leur conformite BUM.
38. `PRD-556` Valider la preparation financiere et documentaire.
39. `PRD-557` Ouvrir et tester l'acces a l'espace Commercant.
40. `PRD-558` Calculer les capacites et cloturer le rendez-vous.
41. `PRD-559` Superviser le portefeuille d'onboarding commercial.

### Conception initiale

- traiter le questionnaire comme un screening, jamais comme un avis juridique ;
- versionner politique, regles, decisions et snapshots des donnees sources ;
- utiliser un garde-fou de publication unique pour tous les canaux ;
- produire un justificatif d'acquisition distinct d'une facture de prestation ;
- utiliser le nom valide `Localeo OnBoard` pour la PWA mobile interne, sans
  dupliquer les donnees du backend ;
- fonder la cloture du rendez-vous sur une checklist versionnee et une matrice
  de capacites calculee cote serveur ;
- ouvrir les demandes de facture uniquement apres consommation validee ;
- laisser au commercant l'emission et le calcul fiscal de sa facture en V1 ;
- lui proposer un assistant facultatif qui prepare le brouillon, puis exige sa
  verification et sa confirmation explicite avant numerotation et emission ;
- distinguer montant brut TTC facture par le commercant, commission Localeo separee et montant net reverse ;
- conserver la commission configurable existante, exprimee TTC, avec une cible de 15 % et extraction de la TVA due par Localeo ;
- emettre les factures Localeo depuis un snapshot fiscal immuable, avec une numerotation unique et un PDF generable a la demande de maniere idempotente ;
- gerer un credit d'achat B2B issu des prestations non utilisees des coffrets expires, porte par un registre immuable et consommable sur une future commande Animation ou Pro ;
- securiser son usage Pro sans compte permanent par code + OTP et regrouper les demandes de facture par achat et commercant ;
- initialiser automatiquement les coffrets techniques existants en
  `MULTI_PURPOSE / VALIDATED`, avec une trace de migration, puis activer les
  controles BUM avant toute premiere commercialisation.
- reutiliser un suivi BackOffice Chorus Pro commun pour les factures
  d'abonnement emises par Localeo et les factures de prestation deposees
  manuellement sous mandat pour les commercants ; reporter l'API en V2.

---

## Epic 52. Accueil Marketplace contextualise par geolocalisation

- Criticite : `Moyenne`
- Statut : `Termine`
- Objectif : contextualiser cinq widgets de l'accueil Marketplace avec les
  communes situees dans un rayon backend de 30 km, centre sur la position
  ponctuelle du visiteur ou sur une ville de preference.
- Backlog detaille :
  [docs/roadmap/terminees/epic-52-accueil-marketplace-geolocalise-backlog.md](terminees/epic-52-accueil-marketplace-geolocalise-backlog.md).
- Cadrage :
  [docs/specifications/epic-52-accueil-marketplace-geolocalise/README.md](../specifications/epic-52-accueil-marketplace-geolocalise/README.md).
- Registre des arbitrages :
  [docs/specifications/epic-52-accueil-marketplace-geolocalise/registre-arbitrages.md](../specifications/epic-52-accueil-marketplace-geolocalise/registre-arbitrages.md).

### User Stories

1. `PRD-488` Georeferencer les communes Localeo.
2. `PRD-489` Rechercher les communes proches.
3. `PRD-490` Demander la geolocalisation avec contexte.
4. `PRD-491` Contextualiser l'accueil autour de moi.
5. `PRD-492` Conserver une selection territoriale.
6. `PRD-493` Garantir un parcours de repli.
7. `PRD-494` Proteger la position de l'internaute.
8. `PRD-495` Superviser la couverture geographique.

### Conception initiale

- enrichir le referentiel historique `villes` avec code INSEE et coordonnees,
  alimentes depuis `geo.api.gouv.fr` puis conserves localement ;
- calculer cote backend une distance Haversine bornee par un rayon serveur ;
- proposer `AUTOUR_DE_MOI` par defaut apres consentement, avec un rayon de
  30 km configurable cote backend ;
- permettre `VILLE_PREFEREE` comme origine alternative du meme rayon et
  `AUCUNE` sans widget territorial ;
- contextualiser uniquement `Coffret du moment`, `Communes disponibles`,
  `Les animations a vivre pres de chez vous`, `En ce moment` et `Derniers
  coffrets ajoutes`, ou les masquer en mode `AUCUNE` ;
- ne pas appliquer ce contexte aux autres pages de la Marketplace ;
- ne stocker localement que le mode et l'eventuel `ville_id`, jamais les
  coordonnees exactes ;
- exclure du MVP geolocalisation IP, suivi continu, itineraire et carte
  obligatoire.

---

## Epic 53. Tombola locale des commercants

- Criticite : `Moyenne`
- Statut : `Termine`
- Objectif : qualifier une personne apres un achat valide chez un commercant
  participant, puis attribuer des coffrets Localeo lors d'un tirage final.
- Backlog detaille :
  [docs/roadmap/terminees/epic-53-tombola-locale-backlog.md](terminees/epic-53-tombola-locale-backlog.md).
- Cadrage et arbitrages :
  `docs/specifications/epic-53-tombola-locale/`.

### User Stories

1. `PRD-496` Declarer le modele Tombola locale.
2. `PRD-497` Configurer une tombola.
3. `PRD-498` Publier et rendre visible la tombola.
4. `PRD-499` S'inscrire a la tombola.
5. `PRD-500` Valider un achat.
6. `PRD-501` Calculer l'eligibilite.
7. `PRD-502` Cloturer et tirer les gagnants.
8. `PRD-503` Notifier les participants.
9. `PRD-504` Envoyer les gains.
10. `PRD-505` Piloter la tombola.
11. `PRD-506` Superviser la tombola.

---

## Epic 54. Calendrier de l'Avent local

- Criticite : `Moyenne`
- Statut : `A developper - arbitrages et conception technique a finaliser`
- Objectif : porter une animation unique composee de journees autonomes, avec
  un commercant, une population eligible, un tirage et un coffret par jour.
- Backlog detaille :
  [docs/roadmap/a-faire/epic-54-calendrier-avent-local-backlog.md](a-faire/epic-54-calendrier-avent-local-backlog.md).
- Cadrage et arbitrages :
  `docs/specifications/epic-54-calendrier-avent-local/`.

### User Stories

1. `PRD-507` Declarer le modele Calendrier.
2. `PRD-508` Configurer les informations globales.
3. `PRD-509` Configurer les cases.
4. `PRD-510` Controler la completude.
5. `PRD-511` Decouvrir le calendrier.
6. `PRD-512` S'inscrire une seule fois.
7. `PRD-513` Ouvrir la case du jour.
8. `PRD-514` Valider une visite quotidienne.
9. `PRD-515` Cloturer une journee.
10. `PRD-516` Realiser le tirage quotidien.
11. `PRD-517` Notifier le resultat et envoyer le gain.
12. `PRD-518` Piloter les journees.
13. `PRD-519` Mesurer les performances.

---

## Epic 55. Chasse au tresor commercante

- Criticite : `Moyenne`
- Statut : `En cours - arbitrages et conception technique à finaliser`
- Objectif : proposer un parcours d'enigmes ordonne chez des commercants,
  dont chaque validation debloque l'etape suivante jusqu'au tirage final.
- Backlog detaille :
  [docs/roadmap/en-cours/epic-55-chasse-tresor-commercante-backlog.md](en-cours/epic-55-chasse-tresor-commercante-backlog.md).
- Cadrage et arbitrages :
  [docs/specifications/moteur-animation/localeo_animation_engine_spec.md](../specifications/moteur-animation/localeo_animation_engine_spec.md).

### User Stories

1. `PRD-520` Declarer le modele Chasse au tresor.
2. `PRD-521` Construire le parcours.
3. `PRD-522` Rediger les enigmes.
4. `PRD-523` Controler la publication.
5. `PRD-524` Decouvrir la chasse au tresor.
6. `PRD-525` Commencer le parcours.
7. `PRD-526` Valider l'etape active.
8. `PRD-527` Debloquer l'etape suivante.
9. `PRD-528` Calculer la qualification.
10. `PRD-529` Cloturer et tirer les gagnants.
11. `PRD-530` Notifier et remettre les gains.
12. `PRD-531` Piloter le parcours.
13. `PRD-532` Superviser et analyser.

---

## Epic 56. Validation de la participation des commercants aux animations

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : recueillir et tracer l'accord explicite des commercants avant de
  les rendre participants d'une animation, leur fournir le flyer et garantir
  que les lots representent au moins un commercant ayant accepte.
- Backlog detaille :
  [docs/roadmap/terminees/epic-56-validation-participation-commercants-animation-backlog.md](terminees/epic-56-validation-participation-commercants-animation-backlog.md).
- Cadrage et arbitrages :
  `docs/specifications/epic-56-validation-participation-commercants-animation/`.
- Conception technique :
  [docs/specifications/epic-56-validation-participation-commercants-animation/conception-technique.md](../specifications/epic-56-validation-participation-commercants-animation/conception-technique.md).

### User Stories

1. `PRD-533` Selectionner les commercants a solliciter.
2. `PRD-534` Preparer les metadonnees de participation.
3. `PRD-535` Envoyer la demande sur les canaux commercant.
4. `PRD-536` Consulter la demande.
5. `PRD-537` Accepter ou refuser.
6. `PRD-538` Restituer les decisions.
7. `PRD-539` Relancer une demande.
8. `PRD-540` Construire la liste effective des participants.
9. `PRD-541` Mettre le flyer a disposition.
10. `PRD-542` Controler l'eligibilite des lots.
11. `PRD-543` Mesurer l'acceptation.
12. `PRD-544` Superviser et auditer.

---

## Epic 26. Communication libre backoffice

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : permettre au back-office d'envoyer une communication libre a un client, a un commercant ou a un destinataire libre, par email ou SMS, en reutilisant les outbox et services d'envoi existants.
- Pourquoi maintenant : les emails et SMS sortants sont deja historises et pilotes par batch ; le back-office doit pouvoir s'appuyer sur ce socle pour les communications ponctuelles sans sortir de Localeo.
- Backlog detaille : [docs/roadmap/terminees/epic-26-communication-libre-backoffice-backlog.md](terminees/epic-26-communication-libre-backoffice-backlog.md)

### User Stories

1. `PRD-159` En tant qu'operateur back-office, je veux acceder a une page de communication libre afin de contacter ponctuellement un client, un commercant ou un destinataire libre depuis Localeo.
   - Statut : `Termine`
   - Resultat attendu : une entree back-office dediee est disponible pour les profils autorises.

2. `PRD-160` En tant qu'operateur back-office, je veux rechercher un destinataire dans les referentiels client et commercant ou saisir un destinataire libre afin de contacter la bonne personne.
   - Statut : `Termine`
   - Resultat attendu : la recherche accepte nom, prenom, nom de commerce, email et telephone ; le mode libre accepte un libelle optionnel et une coordonnee valide.

3. `PRD-161` En tant qu'operateur back-office, je veux choisir entre email et SMS afin d'utiliser le canal adapte au besoin de communication.
   - Statut : `Termine`
   - Resultat attendu : le canal choisi est disponible seulement si la coordonnee correspondante existe et est valide.

4. `PRD-162` En tant qu'operateur back-office, je veux composer un email riche afin d'envoyer une communication claire et professionnelle.
   - Statut : `Termine`
   - Resultat attendu : l'email contient un objet obligatoire, un corps riche assaini et une version texte.

5. `PRD-163` En tant qu'operateur back-office, je veux ajouter une signature Localeo afin de garantir une coherence de marque sur les emails libres.
   - Statut : `Termine`
   - Resultat attendu : une option ajoute la signature standard maintenue cote application.

6. `PRD-164` En tant qu'operateur back-office, je veux composer un SMS court afin d'envoyer une information rapide au destinataire.
   - Statut : `Termine`
   - Resultat attendu : le SMS respecte les contraintes de longueur et de format du provider.

7. `PRD-165` En tant que responsable exploitation, je veux que chaque communication libre soit historisee comme les autres envois afin de conserver une trace auditable.
   - Statut : `Termine`
   - Resultat attendu : les communications creent des lignes `emails_sortants` ou `sms_sortants` avec un type dedie.

8. `PRD-166` En tant que responsable securite, je veux encadrer les communications libres afin d'eviter les abus, les fuites de donnees et les contenus dangereux.
   - Statut : `Termine`
   - Resultat attendu : l'acces est limite, les contenus HTML sont assainis et l'acteur back-office est audite.

### Decisions produit a cadrer

- La communication libre est une fonctionnalite support/exploitation, pas une solution de campagne marketing.
- Le destinataire MVP peut etre selectionne depuis un referentiel client/commercant ou saisi librement avec validation stricte de l'email ou du telephone.
- Les envois passent par les outbox existantes et les batchs d'envoi existants.
- La signature Localeo est optionnelle pour l'operateur, unique, et controlee par l'application.
- Les communications libres ne sont pas rattachees a une demande support, un achat ou une `CoffretInstance` dans le MVP.
- Aucun niveau de droits distinct entre lecture historique et creation n'est introduit pour le moment.
- Aucune politique de retention specifique n'est ajoutee pour le contenu libre email/SMS pour le moment.
- Les contenus libres sont des donnees sensibles et doivent respecter les regles de masquage et d'audit.

---

## Epic 27. Vision 360 commercant backoffice

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : fournir au back-office une vision 360 d'un commercant recherche par nom, regroupant referentiel, coffrets actifs, profil, activite commerciale, validations recentes, indicateurs financiers et alertes operationnelles.
- Pourquoi maintenant : les donnees commercant existent mais sont dispersees entre referentiel, catalogue, profil, achats, validations, reversements, feedbacks et activites ; une vision 360 accelere le support et le pilotage partenaires.
- Backlog detaille : [docs/roadmap/terminees/epic-27-vision-360-commercant-backoffice-backlog.md](terminees/epic-27-vision-360-commercant-backoffice-backlog.md)

### User Stories

1. `PRD-167` En tant qu'operateur back-office, je veux rechercher un commercant par nom afin d'ouvrir rapidement sa vision 360.
   - Statut : `Termine`
   - Resultat attendu : la recherche accepte le nom de commerce et retourne les commercants correspondants.

2. `PRD-168` En tant qu'operateur back-office, je veux consulter une fiche synthese du commercant afin d'identifier son etat operationnel en un coup d'oeil.
   - Statut : `Termine`
   - Resultat attendu : la fiche affiche statut, ville, type, contact, acces commercant et compte bancaire.

3. `PRD-169` En tant qu'operateur back-office, je veux voir les coffrets actifs du commercant afin de comprendre dans quelles offres il est actuellement vendu.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les coffrets actifs contenant au moins une prestation active du commercant.

4. `PRD-170` En tant qu'operateur back-office, je veux voir l'etat des prestations du commercant afin d'identifier les offres actives, en brouillon ou bloquees.
   - Statut : `Termine`
   - Resultat attendu : les prestations sont regroupees par statut.

5. `PRD-171` En tant qu'operateur back-office, je veux voir la derniere mise a jour du profil commercant afin de savoir si sa fiche publique est recente et publiee.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche le statut du profil, derniere soumission, derniere moderation, derniere publication et score de completion si disponible.

6. `PRD-172` En tant qu'operateur back-office, je veux voir les indicateurs d'activite du commercant par periode afin de mesurer rapidement son activite recente.
   - Statut : `Termine`
   - Resultat attendu : les periodes jour courant, 7 jours, 30 jours et annee en cours sont affichees.

7. `PRD-173` En tant qu'operateur back-office, je veux voir les dernieres validations du commercant afin de comprendre son activite terrain recente.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les dernieres validations avec date, coffret, prestation, statut et email client masque.

8. `PRD-174` En tant qu'operateur back-office, je veux voir les derniers achats contenant une prestation du commercant afin de comprendre la demande recente.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les derniers achats rattaches aux coffrets contenant une prestation du commercant.

9. `PRD-175` En tant qu'operateur back-office, je veux voir les signaux qualitatifs recents du commercant afin de reperer les retours clients et activites visibles.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche les derniers feedbacks et activites locales rattaches au commercant si disponibles.

10. `PRD-176` En tant que responsable exploitation, je veux voir les alertes operationnelles du commercant afin de traiter les blocages prioritaires.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les alertes de referencement, profil, coffrets, prestations, compte bancaire et activite.

11. `PRD-177` En tant que responsable produit, je veux que les indicateurs financiers soient clairement nommes afin d'eviter la confusion entre CA encaisse et reversement commercant.
    - Statut : `Termine`
    - Resultat attendu : CA encaisse commercant, montant reverse et montant a reverser sont affiches systematiquement quand les donnees sources existent.

12. `PRD-178` En tant qu'operateur back-office, je veux naviguer facilement depuis la vision 360 vers les objets du commercant afin d'agir ou de verifier un detail sans refaire une recherche.
    - Statut : `Termine`
    - Resultat attendu : les elements affiches proposent des liens directs vers leurs fiches back-office quand elles existent.

13. `PRD-179` En tant qu'operateur back-office, je veux voir les messages support et communications libres recentes du commercant afin de comprendre les derniers echanges avec Localeo.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les 20 derniers messages support et les 20 derniers emails/SMS de communication libre envoyes au commercant.

14. `PRD-180` En tant qu'operateur back-office, je veux filtrer les indicateurs sur une periode personnalisee afin d'analyser une fenetre commerciale ou support precise.
    - Statut : `Termine`
    - Resultat attendu : la vue accepte une date de debut et une date de fin.

15. `PRD-181` En tant qu'operateur back-office, je veux contacter le commercant depuis la vision 360 afin de passer rapidement de l'analyse a l'action.
    - Statut : `Termine`
    - Resultat attendu : un bouton ouvre la communication libre avec le commercant preselectionne.

16. `PRD-182` En tant qu'operateur back-office, je veux voir les documents et elements financiers du commercant afin de repondre aux questions de facturation ou reversement.
    - Statut : `Termine`
    - Resultat attendu : la vue expose les liens vers documents, reversements et paiements de reversement disponibles.

17. `PRD-183` En tant qu'operateur back-office, je veux voir les incidents et anomalies recentes du commercant afin de prioriser les corrections.
    - Statut : `Termine`
    - Resultat attendu : paiements en erreur, validations incoherentes, emails/SMS en erreur et reversements bloques ou en echec sont visibles.

18. `PRD-184` En tant qu'operateur back-office, je veux voir l'activite back-office recente du commercant afin de comprendre les dernieres interventions internes.
    - Statut : `Termine`
    - Resultat attendu : les derniers evenements d'audit rattaches au commercant sont visibles.

19. `PRD-185` En tant qu'operateur back-office, je veux ajouter des notes internes sur un commercant afin de conserver un contexte support ou commercial partage.
    - Statut : `Termine`
    - Resultat attendu : les notes internes affichent auteur, date et contenu et restent strictement back-office.

### Decisions produit a cadrer

- La vision 360 est une vue back-office interne, pas une vue commercant.
- La recherche MVP se fait par nom de commerce.
- La vue MVP est en lecture seule.
- La vue MVP sert de point d'entree de navigation vers les fiches back-office existantes.
- Les periodes standard sont aujourd'hui, 7 jours, 30 jours, annee civile en cours et periode personnalisee.
- Les donnees client exposees dans les listes recentes sont masquees.
- Les indicateurs financiers affichent systematiquement CA encaisse commercant, montant reverse et montant a reverser quand les donnees sources existent.
- Les messages support commercant et communications libres email/SMS sont inclus dans la V1.
- Les listes recentes sont limitees a 20 elements.
- Le bouton `Contacter ce commercant` ouvre la communication libre pre-remplie.
- Documents/facturation, anomalies recentes, activite back-office et notes internes sont inclus dans la V1.

---

## Epic 28. Calcul reversement coffret backoffice

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : faciliter le calcul du montant de reversement lors de la construction d'un coffret, en tenant compte du taux de marge applicable, du prix du coffret et des reversements deja configures sur les prestations rattachees.
- Pourquoi maintenant : les montants de reversement sont structurants pour la marge Localeo ; l'operateur doit pouvoir construire un coffret sans calcul manuel fragile ni risque de depasser le budget de reversement disponible.
- Backlog detaille : [docs/roadmap/terminees/epic-28-calcul-reversement-coffret-backoffice-backlog.md](terminees/epic-28-calcul-reversement-coffret-backoffice-backlog.md)

### User Stories

1. `PRD-186` En tant qu'operateur back-office, je veux acceder a un assistant de calcul depuis le champ de reversement d'une prestation afin de ne pas calculer manuellement le montant disponible.
   - Statut : `Termine`
   - Resultat attendu : un lien est visible a cote du champ `montant_reversement` quand un coffret est selectionne.

2. `PRD-187` En tant qu'operateur back-office, je veux voir le reversement disponible d'un coffret afin de choisir un montant compatible avec la marge attendue.
   - Statut : `Termine`
   - Resultat attendu : la page affiche prix du coffret, taux de marge, budget total de reversement, total deja affecte et disponible restant.

3. `PRD-188` En tant qu'operateur back-office, je veux que la prestation en cours d'edition soit exclue du total deja affecte afin de pouvoir modifier son montant sans double comptage.
   - Statut : `Termine`
   - Resultat attendu : le calcul du disponible exclut la prestation courante quand son identifiant est transmis.

4. `PRD-189` En tant que responsable financier, je veux interdire un total de reversements superieur au prix du coffret afin d'eviter une incoherence economique impossible.
   - Statut : `Termine`
   - Resultat attendu : la validation de la prestation refuse tout montant qui ferait depasser le prix total du coffret par la somme des reversements.

5. `PRD-190` En tant qu'operateur back-office, je veux valider le montant calcule afin de revenir au formulaire prestation avec le champ pre-rempli.
   - Statut : `Termine`
   - Resultat attendu : le formulaire prestation est rouvert avec `montant_reversement` pre-rempli.

6. `PRD-191` En tant qu'operateur back-office, je veux modifier le montant propose avant validation afin de choisir un reversement inferieur au disponible.
   - Statut : `Termine`
   - Resultat attendu : un montant inferieur ou egal au disponible est accepte.

7. `PRD-196` En tant que responsable produit, je veux pouvoir degrader explicitement la marge d'un coffret afin d'accepter ponctuellement un reversement superieur au disponible cible.
   - Statut : `Termine`
   - Resultat attendu : un montant superieur au reversement disponible cible est accepte uniquement apres confirmation explicite et dans la limite du prix du coffret.

8. `PRD-192` En tant que responsable produit, je veux une vision 360 coffret afin de piloter la performance et la rentabilite de chaque coffret.
   - Statut : `Termine`
   - Resultat attendu : une entree back-office `Vision 360 coffret` permet de rechercher et ouvrir un coffret.

9. `PRD-193` En tant qu'operateur back-office, je veux voir les prestations et commercants rattaches dans la vision 360 coffret afin de comprendre la composition du coffret.
   - Statut : `Termine`
   - Resultat attendu : chaque prestation affiche statut, commercant, montant de reversement et lien vers sa fiche.

10. `PRD-194` En tant que responsable exploitation, je veux voir les achats et validations du coffret afin de mesurer sa performance commerciale et terrain.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche achats recents, validations recentes, taux d'utilisation si calculable et liens vers les objets back-office.

11. `PRD-195` En tant que responsable financier, je veux identifier les coffrets a risque de marge afin de prioriser les corrections.
    - Statut : `Termine`
    - Resultat attendu : la vue signale les coffrets dont le disponible est negatif ou dont la marge theorique est insuffisante.

### Decisions produit a cadrer

- L'assistant de calcul est rattache a la creation ou modification d'une prestation coffret.
- Le plafond de reversement est calcule depuis le prix du coffret, le taux de marge applicable et les reversements deja configures.
- Le taux de marge applicable est celui configure sur le `type_coffret.marge_minimum_pourcent`.
- Le calcul prend en compte toutes les prestations rattachees au coffret, sauf les prestations suspendues ou archivees.
- Une prestation suspendue ou archivee ne reserve pas de disponible.
- Une prestation en cours d'edition doit etre exclue du total existant pour eviter le double comptage.
- La saisie d'un montant superieur au disponible cible peut etre autorisee uniquement avec confirmation explicite de degradation de marge.
- La somme totale des reversements ne doit jamais depasser le prix du coffret, meme en cas de degradation explicite de marge.
- La confirmation de degradation de marge se fait par checkbox.
- Une degradation de marge est historisee dans l'audit avec ancien/nouveau niveau de marge theorique.
- La page d'aide peut proposer des suggestions simples de repartition.
- Un avertissement specifique doit etre affiche quand des prestations suspendues ou archivees existent mais sont exclues du calcul.
- La vision 360 coffret est une vue de pilotage interne, en lecture seule dans le MVP.
- La vision 360 coffret est livree dans le meme lot MVP que l'assistant de calcul.
- Aucun point en suspens identifie a ce stade.

---

## Epic 15. Dashboard KPI operationnel backoffice

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : fournir au backoffice une vue consolidee des alertes et indicateurs operationnels sur le referencement, la commercialisation, les paiements, les achats, les coffrets instances, l'utilisation des prestations et les reversements.
- Pourquoi maintenant : les workflows backoffice se structurent autour de plusieurs statuts et dependances ; un dashboard devient necessaire pour detecter rapidement les blocages, les donnees incompletes et les operations financieres a traiter.
- Backlog detaille : [docs/roadmap/terminees/epic-15-dashboard-kpis-backoffice-backlog.md](terminees/epic-15-dashboard-kpis-backoffice-backlog.md)

### User Stories

1. `PRD-074` En tant qu'operateur back-office, je veux visualiser l'etat du referencement afin d'identifier les commercants, coffrets et prestations qui bloquent la mise en ligne.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche les commercants non actifs, inactifs, sans acces commercant et sans compte connecte Stripe eligible.

2. `PRD-075` En tant qu'operateur back-office, je veux visualiser l'etat de commercialisation afin de comprendre quels coffrets et prestations sont publiables ou non.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche les volumes par statut de coffret et de prestation coffret, avec mise en evidence des incoherences.

3. `PRD-076` En tant qu'operateur back-office, je veux suivre les paiements et achats afin de traiter les achats en attente et les activations incompletes.
   - Statut : `Termine`
   - Resultat attendu : le dashboard distingue les achats professionnels et personnels, leur statut de paiement et leur etat d'activation.

4. `PRD-077` En tant qu'operateur back-office, je veux suivre les coffrets instances et l'utilisation des prestations afin de savoir combien de prestations restent a consommer.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche les coffrets instances par statut, les prestations consommees, a consommer et les cas incoherents.

5. `PRD-078` En tant qu'operateur back-office, je veux suivre les reversements afin de connaitre le montant a reverser, le nombre de commercants a payer et les paiements de reversement a traiter.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche le montant total a reverser, le nombre de commercants a payer, les mouvements a reverser, les reversements en preparation, les paiements en cours et les lots de paiement ouverts.

6. `PRD-079` En tant qu'operateur back-office, je veux suivre l'etat d'exploitation des emails et SMS afin de detecter les messages a envoyer, non delivres ou en erreur.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche les volumes d'emails et SMS a envoyer, en cours, non delivres et en erreur.

7. `PRD-080` En tant qu'operateur support, je veux suivre l'etat des demandes support afin de prioriser les messages entrants et les dossiers en cours.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche les demandes support non lues, en cours, non traitees, par cible consommateur/commercant et par motif.

### Decisions produit a cadrer

- Le dashboard est une vue de pilotage backoffice, pas une vue analytique marketing.
- Les indicateurs doivent pointer vers les listes backoffice filtrees correspondantes quand une action est attendue.
- Les KPI doivent distinguer les alertes bloquantes des simples volumes informatifs.
- Les montants financiers doivent etre exprimes en EUR et coherents avec les statuts metier des reversements.
- Les KPI d'exploitation email/SMS et support font partie du dashboard V1 car ils correspondent a des actions quotidiennes backoffice.

---

## Epic 16. Feed d'activite locale marketplace

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : generer et exposer un feed d'activite locale anonymise autour des coffrets, des villes, des commercants et des prestations afin de rendre la marketplace plus vivante et plus rassurante.
- Pourquoi maintenant : les parcours d'achat gagnent en confiance lorsqu'ils montrent une activite locale recente, mais cette preuve sociale doit rester maitrisee, anonymisee et moderable.
- Backlog detaille : [docs/roadmap/terminees/epic-16-feed-activite-locale-marketplace-backlog.md](terminees/epic-16-feed-activite-locale-marketplace-backlog.md)

### User Stories

1. `PRD-081` En tant que visiteur marketplace, je veux voir une activite locale recente afin de percevoir que les coffrets sont reellement utilises autour de moi.
   - Statut : `Termine`
   - Resultat attendu : la page d'accueil affiche un feed public anonymise melant achats, activations, validations et nouveautes pertinentes.

2. `PRD-082` En tant que visiteur d'une page ville, je veux voir les activites rattachees a cette ville afin de comprendre la dynamique locale.
   - Statut : `Termine`
   - Resultat attendu : la page ville affiche uniquement les activites publiques rattachees a la ville.

3. `PRD-083` En tant que visiteur d'une page commercant, je veux voir des signaux d'activite lies a ce commercant afin de renforcer la confiance avant achat ou utilisation.
   - Statut : `Termine`
   - Resultat attendu : la page commercant affiche les activites publiques rattachees au commercant et a ses prestations.

4. `PRD-084` En tant que visiteur d'une page coffret, je veux voir des signaux d'activite lies a ce coffret afin d'evaluer sa popularite ou son usage recent.
   - Statut : `Termine`
   - Resultat attendu : la page coffret affiche les activites publiques rattachees au coffret sans exposer de donnees personnelles.

5. `PRD-085` En tant qu'admin, je veux moderer les activites affichees afin de masquer une activite non pertinente ou sensible.
   - Statut : `Termine`
   - Resultat attendu : le backoffice permet de consulter, masquer et reactiver les activites locales.

6. `PRD-086` En tant que systeme, je veux generer les activites locales depuis les evenements metier afin d'eviter des calculs lourds a chaque affichage marketplace.
   - Statut : `Termine`
   - Resultat attendu : une projection `activites_locales` est alimentee lors des evenements metier eligibles.

### Decisions produit a cadrer

- Le feed public ne doit jamais exposer de donnees personnelles client.
- Les activites sensibles ou negatives ne sont pas publiees en V1.
- Le feed public doit privilegier des formulations anonymisees et temporellement floutees.
- Le nom public du commercant peut apparaitre sur les activites de validation ou d'utilisation de prestation.
- Une activite locale est visible publiquement 45 jours par defaut, 90 jours pour les nouveautes catalogue et 14 jours pour les signaux agreges de popularite.
- Le regroupement automatique strict des evenements a faible volume est reporte en V2 ; en V1, le libelle doit surtout rester anonymise et temporellement floute.
- Les activites editoriales manuelles sont autorisees en V2 via le backoffice.
- Les libelles V1 sont generes depuis des templates fixes par type d'activite, avec fallbacks si la ville, le commercant ou le coffret sont absents.
- Le backoffice reste la source de moderation finale.

---

## Epic 17. Feedback client post-prestation

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : collecter un feedback simple apres chaque consommation de prestation afin d'ameliorer la qualite, detecter les irritants et afficher des signaux de satisfaction anonymises sur la marketplace.
- Pourquoi maintenant : l'Epic 16 anime la marketplace avec des signaux d'activite ; les feedbacks ajoutent une preuve qualitative, tout en donnant au backoffice une boucle d'amelioration continue.
- Backlog detaille : [docs/roadmap/terminees/epic-17-feedback-client-post-prestation-backlog.md](terminees/epic-17-feedback-client-post-prestation-backlog.md)

### User Stories

1. `PRD-087` En tant que client, je veux pouvoir donner mon avis juste apres avoir utilise une prestation afin de partager facilement mon ressenti.
   - Statut : `Termine`
   - Resultat attendu : l'email de prestation utilisee contient un lien de feedback avec note de 1 a 4.

2. `PRD-088` En tant que systeme, je veux verifier un token de feedback afin de garantir qu'un avis correspond a une prestation reellement consommee.
   - Statut : `Termine`
   - Resultat attendu : le token est opaque, expire, a usage unique et stocke uniquement sous forme de hash.

3. `PRD-089` En tant que client, je veux pouvoir ajouter un commentaire optionnel et choisir s'il peut etre reutilise publiquement de facon anonymisee.
   - Statut : `Termine`
   - Resultat attendu : la note est obligatoire, le commentaire est optionnel et l'autorisation de publication est explicite.

4. `PRD-090` En tant qu'admin, je veux moderer les commentaires client afin de maitriser ce qui peut etre affiche publiquement.
   - Statut : `Termine`
   - Resultat attendu : le backoffice permet d'approuver, refuser, masquer ou remettre a moderer un feedback.

5. `PRD-091` En tant que visiteur marketplace, je veux voir des signaux de satisfaction agreges afin de mieux choisir un coffret ou un commercant.
   - Statut : `Termine`
   - Resultat attendu : les pages commercant, coffret et prestation peuvent afficher note moyenne, volume d'avis et taux de satisfaction.

6. `PRD-092` En tant qu'operateur Localeo, je veux suivre les retours faibles afin de detecter les prestations ou partenaires a surveiller.
   - Statut : `Termine`
   - Resultat attendu : le backoffice permet de filtrer les notes 1 ou 2 et de remonter au commercant, a la prestation et a la validation source.

### Decisions produit a cadrer

- La collecte V1 est declenchee apres chaque `PRESTATION_VALIDEE`.
- La V1 ne cree pas de nouvel email : le feedback est integre au template existant `prestation_utilisee`.
- Le formulaire n'est pas integre directement dans l'email ; le bloc de feedback du mail pointe vers une page publique tokenisee.
- La notation cible est de 1 a 4 etoiles.
- Le token de feedback expire apres 30 jours en V1.
- Aucune relance automatique n'est envoyee en V1 si le client ne repond pas.
- Le commentaire est optionnel et limite en taille.
- Les agregats publics restent affichables meme avec un faible volume d'avis, a condition d'afficher le nombre d'avis.
- Les commentaires publics doivent etre autorises par le client, anonymises et moderes.
- Les notes peuvent alimenter des agregats publics meme si le commentaire n'est pas publie.
- Le feedback global de fin de coffret est reporte en V2.

---

## Epic 18. Page commercant immersive

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : transformer la fiche commercant en page publique et mobile plus humaine, plus immersive et plus actionnable, avec edition commercant encadree et moderation avant publication.
- Pourquoi maintenant : les Epics 11, 16 et 17 posent les bases du profil commercant, du feed d'activite et des feedbacks. La page commercant peut maintenant devenir une surface de confiance et de conversion pour la marketplace.
- Backlog detaille : [docs/roadmap/terminees/epic-18-page-commercant-immersive-backlog.md](terminees/epic-18-page-commercant-immersive-backlog.md)

### User Stories

1. `PRD-093` En tant que visiteur marketplace, je veux consulter une page commercant riche afin de comprendre l'univers du partenaire avant d'acheter ou d'utiliser un coffret.
   - Statut : `Termine`
   - Resultat attendu : la page affiche accroche, presentation, photos, specialites, ambiance, prestations et informations pratiques publiques.

2. `PRD-094` En tant qu'admin Localeo, je veux enrichir les informations publiques d'un commercant afin de rendre sa fiche plus humaine et differenciante.
   - Statut : `Termine`
   - Resultat attendu : le back-office permet de renseigner les champs editoriaux et de controler leur publication.

3. `PRD-095` En tant que commercant authentifie, je veux proposer des modifications de ma fiche depuis l'application mobile afin de garder ma presentation a jour.
   - Statut : `Termine`
   - Resultat attendu : les champs autorises sont modifiables ou soumis a moderation selon leur sensibilite, dans une version brouillon distincte de la version publiee.

4. `PRD-096` En tant qu'operateur Localeo, je veux moderer les contenus proposes par les commercants afin de garantir la qualite et la conformite des fiches publiques.
   - Statut : `Termine`
   - Resultat attendu : chaque proposition publique passe par un statut de moderation avant publication, et un refus ne modifie pas la version publiee.

5. `PRD-096 bis` En tant qu'operateur Localeo, je veux conserver une version publiee stable pendant qu'une future version est en approbation afin de ne pas degrader la page publique en cas de refus.
   - Statut : `Termine`
   - Resultat attendu : le systeme distingue version publiee, proposition en cours et historique ; le refus d'une proposition conserve le commercant actif et la fiche publiee existante.

6. `PRD-096 ter` En tant que commercant authentifie, je veux consulter l'etat de mes demandes de modification afin de savoir si ma fiche est en brouillon, en attente, approuvee ou refusee.
   - Statut : `Termine`
   - Resultat attendu : l'espace commercant affiche les demandes, leur statut, les dates importantes, les champs modifies et le motif de refus public si applicable.

7. `PRD-096 quater` En tant qu'operateur Localeo, je veux voir une alerte dans le dashboard operationnel lorsqu'une demande de publication de fiche commercant est en attente afin de ne pas laisser les propositions sans traitement.
   - Statut : `Termine`
   - Resultat attendu : le dashboard operationnel affiche un compteur d'alertes pour les demandes `A_MODERER` ou `EN_ATTENTE_RELECTURE` et pointe vers la vue de traitement.

8. `PRD-097` En tant qu'operateur Localeo, je veux connaitre le niveau de completion d'une fiche afin de prioriser les enrichissements.
   - Statut : `Termine`
   - Resultat attendu : le back-office et l'espace commercant affichent un score ou une checklist de completion calcule a la volee.

9. `PRD-097 bis` En tant qu'operateur Localeo, je veux bloquer la publication d'une fiche insuffisamment renseignee afin de garantir une experience publique coherente et qualitative.
   - Statut : `Termine`
   - Resultat attendu : la publication exige accroche, presentation, trois photos validees, au moins une specialite, une ambiance, une information pratique et une prestation active.

10. `PRD-097 ter` En tant que commercant authentifie, je veux generer un apercu de ma page commercant depuis l'application mobile afin de verifier le rendu avant soumission ou publication.
   - Statut : `Termine`
   - Resultat attendu : l'apercu est protege par session commercant, base sur la proposition active, expose sous forme de donnees JSON de preview, non indexable, sans lien public partageable et sans impact sur la version publique.

11. `PRD-098` En tant que visiteur marketplace, je veux voir des signaux de confiance rattaches au commercant afin d'etre rassure.
   - Statut : `Termine`
   - Resultat attendu : la page peut afficher activites publiques, feedbacks agreges et prestations recemment utilisees sans exposer de donnees client.

### Decisions produit a cadrer

- Les champs editoriaux publics doivent etre moderes avant publication.
- Seuls les champs modifiables et soumis a moderation sont versionnes en V1 ; les champs structurants sous controle Localeo restent dans `commercants` sans versioning initial.
- Le contenu editorial/moderable doit etre versionne : une version publiee validee reste servie publiquement pendant qu'une future version est `BROUILLON` ou `A_MODERER`.
- Les statuts de version sont fixes en V1 : `BROUILLON`, `A_MODERER`, `PUBLIEE`, `REFUSEE`, `ARCHIVEE`, `MASQUEE`.
- La granularite de versioning est la fiche editoriale complete : chaque version contient un snapshot complet des champs moderables, pas une version par attribut.
- Le refus d'une future version ne doit jamais desactiver le commercant, masquer la fiche publiee courante, ni modifier `Commercant.statut`.
- L'espace commercant doit permettre de consulter l'etat d'une demande de modification, son historique court et le motif de refus public le cas echeant.
- Le dashboard operationnel doit alerter lorsqu'une demande de publication de fiche commercant reste a traiter.
- La V1 mobile doit distinguer champs modifiables librement, champs soumis a moderation et champs non modifiables.
- La page marketplace publique n'est pas exposee tant qu'aucune version editoriale n'a ete approuvee ; le fallback minimal depuis `commercants` est reserve au back-office et a la preview authentifiee.
- Les photos de la page commercant doivent reutiliser la bibliotheque d'images existante : la version de fiche stocke des references `image_uri` et leur ordre, pas les fichiers.
- Toute photo proposee pour publication peut etre uploadee ou selectionnee en etat non publie, puis doit etre validee par un admin Localeo avant exposition publique.
- Les liens publics et reseaux sociaux proposes par un commercant sont verifies manuellement et valides par un admin Localeo avant publication, sans controle automatique en V1.
- Le score de completion de fiche est calcule a la volee et n'est pas persiste en V1.
- Le score de completion V1 est calcule sur 100 points : accroche, presentation, histoire ou mot du commercant, photos validees, image principale ou portrait, specialite, ambiance, information pratique et prestation active.
- Le score reste indicatif : la publication exige toujours les criteres obligatoires et les validations admin, meme si le score est eleve.
- Une fiche ne peut etre publiee que si elle atteint le seuil minimal : accroche, presentation, trois photos validees, specialite, ambiance, information pratique et prestation active.
- L'application commercant doit permettre de generer un apercu authentifie sous forme de donnees JSON de preview, base sur la proposition active et protege par session, sans URL web publique partageable en V1.
- Les donnees sensibles restent exclues de la page publique : email de login, telephone operationnel prive, donnees bancaires, support et audit.
- Les signaux issus des activites locales et feedbacks doivent respecter les regles d'anonymisation des Epics 16 et 17.
- Le stockage retenu est une table dediee `profils_commercants`, en complement des champs structurants existants dans `commercants`, avec une table de versions `profils_commercants_versions` pour les champs editoriaux/moderables.
- La table racine `profils_commercants` porte uniquement l'etat courant de publication, le lien unique vers `commercants`, les pointeurs `version_publiee_id` et `proposition_active_id`, les dates de publication/soumission/moderation/masquage et le motif de masquage.
- `profils_commercants` est initialise par migration massive pour les commercants existants en `NON_PUBLIE`, sans generation de version editoriale `PUBLIEE`, puis cree automatiquement a la creation de tout nouveau commercant.
- Les champs publics versionnes sont stockes en colonnes dediees, pas dans un objet JSON generique.
- La table `profils_commercants_versions` fige les colonnes de snapshot editorial suivantes : accroche, presentation longue, histoire, mot du commercant, specialites, ambiance, valeurs, labels/certifications, informations pratiques, liens publics verifies, references `image_uri`, statuts de verification, motif de refus, commentaire de decision et audit de creation/soumission/moderation/publication.
- Les differences entre versions ne sont pas stockees en V1 : elles sont calculees a la volee entre deux snapshots a partir d'une liste applicative de champs comparables.
- Les statuts de verification des liens et photos sont fixes en V1 : `A_VERIFIER`, `VALIDEE`, `REFUSEE`, `NON_REQUISE`.
- Une version `REFUSEE` reste immutable ; une resoumission cree une nouvelle version `BROUILLON` par duplication.
- L'unicite d'une version `PUBLIEE` active et d'une proposition active par commercant est d'abord un invariant domaine ; des index uniques partiels PostgreSQL peuvent servir de garde-fous techniques.
- Les droits V1 sont separes entre commercant authentifie, admin Localeo et public : le public lit uniquement les versions `PUBLIEE`.
- Les API back-office de gestion des profils commercants sont des API admin sous `/admin/api/profils-commercants`, couvrant liste, detail, versions, moderation, masquage, preview, verification manuelle et audit.
- Les payloads admin principaux sont explicites pour `PATCH brouillon`, `approuver`, `refuser`, `verifier-liens` et `verifier-photos`, avec erreurs standardisees et recalcul backend des criteres de publication a l'approbation.
- Le backlog d'implementation est decoupe en lots : migration/modele SQL, domaine, persistence/audit, API admin, API commercant, publication marketplace, dashboard et tests.
- Les evenements d'audit V1 sont `PROFIL_BROUILLON_CREE`, `PROFIL_SOUMIS_MODERATION`, `PROFIL_APPROUVE`, `PROFIL_REFUSE`, `PROFIL_MASQUE`, `PROFIL_REPUBLIE`.

---

## Epic 19. Dashboard operationnel commercant

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : permettre a un commercant de mesurer depuis son application l'activite et la valeur generees par Localeo : trafic, montant reverse, encours de prestations achetees non consommees et repartition par version de prestation.
- Pourquoi maintenant : les sessions commercants, les reversements, le versioning des prestations et les signaux d'activite permettent de fournir une lecture utile de la valeur Localeo cote partenaire.
- Backlog detaille : [docs/roadmap/terminees/epic-19-dashboard-operationnel-commercant-backlog.md](terminees/epic-19-dashboard-operationnel-commercant-backlog.md)

### User Stories

1. `PRD-099` En tant que commercant authentifie, je veux consulter un dashboard operationnel afin de mesurer l'activite apportee par Localeo.
   - Statut : `Termine`
   - Resultat attendu : le dashboard est accessible depuis l'application commercant et ne concerne que le commercant authentifie.

2. `PRD-100` En tant que commercant, je veux mesurer le trafic genere par Localeo afin de comprendre le volume d'opportunites apporte.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche prestations achetees, prestations consommees et signaux d'activite sans exposer de donnees client.

3. `PRD-101` En tant que commercant, je veux connaitre le montant de reversement genere par Localeo afin de suivre la valeur economique de ma participation.
   - Statut : `Termine`
   - Resultat attendu : le dashboard distingue montant potentiel, montant valide, montant a reverser et montant reverse.

4. `PRD-102` En tant que commercant, je veux voir l'encours des prestations achetees mais non consommees afin d'anticiper les passages clients a venir.
   - Statut : `Termine`
   - Resultat attendu : le dashboard affiche les prestations `A_VALIDER` globalement et par prestation.

5. `PRD-103` En tant que commercant, je veux voir la repartition par version de prestation afin de comprendre l'impact des evolutions de mon offre.
   - Statut : `Termine`
   - Resultat attendu : le dashboard expose les indicateurs par prestation et par numero de version quand plusieurs versions existent.

6. `PRD-104` En tant que commercant, je veux filtrer le dashboard sur une plage de dates afin d'analyser une semaine, un mois ou une periode personnalisee.
   - Statut : `Termine`
   - Resultat attendu : `date_debut` et `date_fin` filtrent les KPIs, les tableaux et les series temporelles ; par defaut, les filtres sont positionnes sur le mois courant.

### Decisions produit a cadrer

- Le dashboard commercant est une vue operationnelle, pas un outil comptable exhaustif.
- La valeur economique affichee au commercant correspond au montant reverse ; la source de verite financiere recommandee est le mouvement de reversement quand il existe.
- L'encours correspond aux prestations achetees en statut `A_VALIDER`.
- La repartition par version exige un snapshot `prestation_version` sur les statuts de prestation, avec une strategie explicite de fallback historique.
- L'API cible est `GET /protected/commercants/me/dashboard-operationnel`, protegee par session commercant.
- Les filtres de dates du dashboard sont positionnes par defaut sur le mois courant.
- Aucune donnee personnelle client ne doit etre exposee.

---

## Ordre recommande de mise en oeuvre

Priorite courante ajoutee le 13 septembre 2026 :
[Epic 64 - Parcours de retractation en ligne](a-faire/epic-64-parcours-retractation-en-ligne-backlog.md),
au titre de l'obligation deja applicable. La sequence ci-dessous conserve
l'ordre historique des autres livraisons.

1. Epic 1 - Gouvernance du referencement commercant et prestation
2. Epic 2 - Protection de l'integrite des coffrets
3. Epic 3 - Workflow de proposition de modification de prestation
4. Epic 4 - Notifications commercant sur achat de coffret
5. Epic 10 - Authentification commercant par login / mot de passe
6. Epic 11 - Espace commercant et informations contact
7. Epic 6 - Montant de reversement sur prestation coffret
8. Epic 13 - Generation des reversements commercants
9. Epic 12 - Traitement des reversements et export des paiements
10. Epic 14 - Documents d'achat et facturation du coffret
11. Epic 20 - Gestion des remboursements
12. Epic 21 - Expiration automatique des coffrets
13. Epic 22 - Timeline support achat et coffret
14. Epic 23 - Gestion des batchs et ordonnancement
15. Epic 48 - Ordonnancement des batchs avec APScheduler
16. Epic 24 - Optimisation de la couche domaine DDD
17. Epic 25 - Couche de tests fonctionnels domaine et application
18. Epic 29 - Jeu de donnees de test pour recette
19. Epic 26 - Communication libre backoffice
20. Epic 27 - Vision 360 commercant backoffice
21. Epic 28 - Calcul reversement coffret backoffice
22. Epic 30 - Vision 360 reversements et paiements backoffice
23. Epic 31 - Annulation d'une validation de prestation backoffice
24. Epic 32 - Live tracking WebPush commercants
25. Epic 33 - Recherche multi-scope marketplace
26. Epic 34 - Localeo Control
27. Epic 35 - Profils back-office differencies
28. Epic 36 - Fermeture commercant et remplacement des prestations achetees
29. Epic 37 - Vision 360 client backoffice
30. Epic 38 - Gestion documentaire transverse
31. Epic 39 - Delegation des flux financiers a Stripe Connect
32. Epic 40 - Organisation du backend par domaines fonctionnels
33. Epic 41 - Plateforme d'animation locale MVP
34. Epic 47 - Souscription et paiement de l'abonnement partenaire Animation
35. Epic 46 - Paiement professionnel des lots Animation
36. Epic 42 - Localeo Live grand public
37. Epic 49 - Visibilite des animations dans la Marketplace
38. Epic 43 - Suivi des virements bancaires Stripe Connect
39. Epic 15 - Dashboard KPI operationnel backoffice
40. Epic 16 - Feed d'activite locale marketplace
41. Epic 17 - Feedback client post-prestation
42. Epic 18 - Page commercant immersive
43. Epic 19 - Dashboard operationnel commercant
44. Epic 7 - Tokens de consultation achat et coffret instance
45. Epic 8 - Gestion des contacts et messages support
46. Epic 9 - Mode secours telephonique pour l'honorisation d'une prestation

## Proposition de sequencing produit

### Lot 1 - Catalogue robuste

- `PRD-001`
- `PRD-002`
- `PRD-003`
- `PRD-015`
- `PRD-016`
- `PRD-004`
- `PRD-005`
- `PRD-006`

### Lot 2 - Collaboration commercant encadree

- `PRD-007`
- `PRD-008`
- `PRD-009`
- `PRD-010`

### Lot 3 - Engagement commercant

- `PRD-011`
- `PRD-012`
- `PRD-013`
- `PRD-014`

### Lot 4 - Authentification commercant

- `PRD-046`
- `PRD-047`
- `PRD-048`
- `PRD-049`
- `PRD-050`

### Lot 4 bis - Autonomie profil commercant

- `PRD-051`
- `PRD-052`
- `PRD-053`
- `PRD-054`

### Lot 5 - Coherence financiere prestation

- `PRD-023`
- `PRD-024`
- `PRD-025`

### Lot 5 bis - Paiement operationnel des reversements

- `PRD-055`
- `PRD-056`
- `PRD-057`
- `PRD-058`
- `PRD-059 bis`
- `PRD-059`

### Lot 5 ter - Preparation des reversements

- `PRD-060`
- `PRD-061`
- `PRD-062`
- `PRD-063`
- `PRD-064`

### Lot 5 quater - Documents d'achat et facturation

- `PRD-065`
- `PRD-066`
- `PRD-067`
- `PRD-068`
- `PRD-069`
- `PRD-070`
- `PRD-071`
- `PRD-072`
- `PRD-073`

### Lot 5 quater bis - Gestion des remboursements

- `PRD-105`
- `PRD-106`
- `PRD-107`
- `PRD-108`
- `PRD-109`
- `PRD-110`
- `PRD-111`
- `PRD-123`
- `PRD-124`

### Lot 5 quater ter - Expiration automatique des coffrets

- `PRD-112`
- `PRD-113`
- `PRD-114`
- `PRD-115`
- `PRD-116`

### Lot 5 quinquies - Pilotage operationnel backoffice

- `PRD-074`
- `PRD-075`
- `PRD-076`
- `PRD-077`
- `PRD-078`
- `PRD-079`
- `PRD-080`

### Lot 5 sexies - Feed d'activite locale marketplace

- `PRD-081`
- `PRD-082`
- `PRD-083`
- `PRD-084`
- `PRD-085`
- `PRD-086`

### Lot 5 septies - Feedback client post-prestation

- `PRD-087`
- `PRD-088`
- `PRD-089`
- `PRD-090`
- `PRD-091`
- `PRD-092`

### Lot 5 octies - Dashboard operationnel commercant

- `PRD-099`
- `PRD-100`
- `PRD-101`
- `PRD-102`
- `PRD-103`
- `PRD-104`

### Lot 5 nonies - Communication libre backoffice

- `PRD-159`
- `PRD-160`
- `PRD-161`
- `PRD-162`
- `PRD-163`
- `PRD-164`
- `PRD-165`
- `PRD-166`

### Lot 5 decies - Vision 360 commercant backoffice

- `PRD-167`
- `PRD-168`
- `PRD-169`
- `PRD-170`
- `PRD-171`
- `PRD-172`
- `PRD-173`
- `PRD-174`
- `PRD-175`
- `PRD-176`
- `PRD-177`
- `PRD-178`
- `PRD-179`
- `PRD-180`
- `PRD-181`
- `PRD-182`
- `PRD-183`
- `PRD-184`
- `PRD-185`

### Lot 5 undecies - Calcul reversement coffret backoffice

- `PRD-186`
- `PRD-187`
- `PRD-188`
- `PRD-189`
- `PRD-190`
- `PRD-191`
- `PRD-192`
- `PRD-193`
- `PRD-194`
- `PRD-195`
- `PRD-196`

### Lot 5 duodecies - Jeu de donnees de test pour recette

- `PRD-197`
- `PRD-198`
- `PRD-199`
- `PRD-200`
- `PRD-201`
- `PRD-202`
- `PRD-203`
- `PRD-204`
- `PRD-205`
- `PRD-206`

### Lot 5 terdecies - Vision 360 reversements et paiements backoffice

- `PRD-207`
- `PRD-208`
- `PRD-209`
- `PRD-210`
- `PRD-211`
- `PRD-212`
- `PRD-213`
- `PRD-214`

### Lot 5 quaterdecies - Annulation d'une validation de prestation

- `PRD-215`
- `PRD-216`
- `PRD-217`
- `PRD-218`
- `PRD-219`
- `PRD-220`
- `PRD-221`
- `PRD-222`

### Lot 5 quindecies - Live tracking WebPush commercants

- `PRD-223`
- `PRD-224`
- `PRD-225`
- `PRD-226`
- `PRD-227`
- `PRD-228`
- `PRD-229`
- `PRD-230`
- `PRD-231`
- `PRD-232`

### Lot 5 sexdecies - Recherche multi-scope marketplace

- `PRD-233`
- `PRD-234`
- `PRD-235`
- `PRD-235 bis`
- `PRD-236`
- `PRD-237`
- `PRD-238`
- `PRD-239`
- `PRD-240`

### Lot 5 septdecies - Localeo Control

- `PRD-241`
- `PRD-242`
- `PRD-243`
- `PRD-244`
- `PRD-245`
- `PRD-246`
- `PRD-247`
- `PRD-248`
- `PRD-249`
- `PRD-250`

### Lot 5 octodecies - Profils back-office differencies

- `PRD-251`
- `PRD-252`
- `PRD-253`
- `PRD-254`
- `PRD-255`
- `PRD-256`
- `PRD-257`
- `PRD-258`
- `PRD-259`
- `PRD-260`

### Lot 5 novodecies - Fermeture commercant et remplacement des prestations achetees

- `PRD-261`
- `PRD-262`
- `PRD-263`
- `PRD-264`
- `PRD-265`
- `PRD-266`
- `PRD-267`
- `PRD-268`
- `PRD-269`
- `PRD-270`
- `PRD-271`
- `PRD-272`
- `PRD-273`

### Lot 5 vicesies - Vision 360 client backoffice

- `PRD-274`
- `PRD-275`
- `PRD-276`
- `PRD-277`
- `PRD-278`
- `PRD-279`
- `PRD-280`
- `PRD-281`
- `PRD-282`
- `PRD-283`
- `PRD-284`
- `PRD-285`
- `PRD-286`
- `PRD-287`
- `PRD-288`

### Lot 5 unvicesies - Gestion documentaire transverse

- `PRD-289`
- `PRD-290`
- `PRD-291`
- `PRD-292`
- `PRD-293`
- `PRD-294`
- `PRD-295`
- `PRD-296`
- `PRD-297`
- `PRD-298`
- `PRD-299`
- `PRD-300`
- `PRD-301`
- `PRD-302`
- `PRD-303`
- `PRD-304`
- `PRD-305`
- `PRD-306`

### Lot 5 duovicies - Delegation des flux financiers a Stripe Connect

- `PRD-307`
- `PRD-308`
- `PRD-309`
- `PRD-310`
- `PRD-311`
- `PRD-312`
- `PRD-313`
- `PRD-314`
- `PRD-315`
- `PRD-316`
- `PRD-317`
- `PRD-318`
- `PRD-366`
- `PRD-367`
- `PRD-368`
- `PRD-369`
- `PRD-370`

### Lot 5 tervicies - Organisation du backend par domaines fonctionnels

- `PRD-319`
- `PRD-320`
- `PRD-321`
- `PRD-322`
- `PRD-323`
- `PRD-324`
- `PRD-325`
- `PRD-326`
- `PRD-327`
- `PRD-328`
- `PRD-329`
- `PRD-330`
- `PRD-331`
- `PRD-332`
- `PRD-333`

### Lot 5 quatervicies - Plateforme d'animation locale MVP

- `PRD-334`
- `PRD-335`
- `PRD-336`
- `PRD-337`
- `PRD-338`
- `PRD-339`
- `PRD-340`
- `PRD-341`
- `PRD-342`
- `PRD-343`
- `PRD-344`
- `PRD-345`
- `PRD-346`
- `PRD-347`
- `PRD-348`
- `PRD-349`
- `PRD-350`
- `PRD-351`
- `PRD-352`
- `PRD-353`
- `PRD-354`
- `PRD-355`
- `PRD-356`
- `PRD-357`
- `PRD-358`
- `PRD-359`
- `PRD-360`
- `PRD-361`
- `PRD-362`
- `PRD-363`
- `PRD-364`
- `PRD-365`

### Lot 5 quinvicies - Localeo Live grand public

- `PRD-371`
- `PRD-372`
- `PRD-373`
- `PRD-374`
- `PRD-375`
- `PRD-376`
- `PRD-377`
- `PRD-378`
- `PRD-379`
- `PRD-380`
- `PRD-403`

### Lot 5 sexvicies - Suivi des virements bancaires Stripe Connect

- `PRD-381`
- `PRD-382`
- `PRD-383`
- `PRD-384`
- `PRD-385`
- `PRD-386`
- `PRD-387`
- `PRD-388`
- `PRD-389`
- `PRD-390`

### Lot 5 octovicies - Vision 360 Animation backend

- `PRD-405`
- `PRD-406`
- `PRD-407`
- `PRD-408`
- `PRD-409`
- `PRD-410`
- `PRD-411`
- `PRD-412`

### Lot 5 novovicies - Souscription partenaire Animation

- `PRD-415`
- `PRD-416`
- `PRD-417`
- `PRD-418`
- `PRD-419`
- `PRD-420`
- `PRD-421`
- `PRD-422`
- `PRD-423`
- `PRD-424`
- `PRD-425`
- `PRD-426`

### Lot 5 tricies - Ordonnancement APScheduler

- `PRD-427`
- `PRD-428`
- `PRD-429`
- `PRD-430`
- `PRD-431`
- `PRD-432`
- `PRD-433`
- `PRD-434`
- `PRD-435`
- `PRD-436`
- `PRD-437`
- `PRD-438`

### Lot 5 septvicies - Observabilite et logs des Use Cases

- `PRD-391`
- `PRD-392`
- `PRD-393`
- `PRD-394`
- `PRD-395`
- `PRD-396`
- `PRD-397`
- `PRD-398`
- `PRD-399`
- `PRD-400`
- `PRD-401`
- `PRD-402`

### Lot 6 - Consultation securisee achat et coffret instance

- `PRD-026`
- `PRD-027`
- `PRD-028`
- `PRD-029`

### Lot 7 - Support et messagerie

- `PRD-030`
- `PRD-031`
- `PRD-032`
- `PRD-033`
- `PRD-034`
- `PRD-035`
- `PRD-036`
- `PRD-037`
- `PRD-038`
- `PRD-039`

### Lot 8 - Continuite operationnelle de secours

- `PRD-040`
- `PRD-041`
- `PRD-042`
- `PRD-043`
- `PRD-044`
- `PRD-045`

## Resultat attendu a terme

- un catalogue publiable sans exposition prematuree ;
- des coffrets proteges contre les suppressions ou invalidations incoherentes ;
- un workflow d'evolution des prestations compatible avec la production ;
- une relation commercant plus proactive grace aux notifications parametrables ;
- un acces commercant securise par session courte apres authentification login / mot de passe ;
- un espace commercant permettant la consultation et la mise a jour encadree des informations de contact ;
- une base fiable pour les reversements commercants grace au `montant_reversement` porte par chaque prestation.
- un traitement des reversements historiquement outille par export bancaire manuel, desormais remplace par la cible Stripe Connect de l'EPIC 39.
- une gestion des remboursements complete et auditable, rattachee aux annulations de coffrets payes.
- une expiration automatique des coffrets permettant de fermer les instances arrivees a echeance et les prestations restantes.
- une consultation securisee des achats et `CoffretInstances` via des tokens dedies et cloisonnes par usage.
- une messagerie support structuree pour traiter les demandes consommateurs et commercants avec suivi back-office.
- un mode secours telephonique traçable pour honorer exceptionnellement une prestation lors d'un incident technique.
- un dashboard backoffice permettant de piloter les blocages de referencement, la commercialisation, les achats, l'utilisation des coffrets et les reversements a traiter.
- une communication libre backoffice permettant de contacter ponctuellement clients, commercants et destinataires libres par email ou SMS avec historique d'envoi.
- une vision 360 commercant backoffice permettant de comprendre rapidement le referentiel, l'activite, les coffrets, les validations et les alertes d'un partenaire.
- un assistant de calcul de reversement coffret et une vision 360 coffret permettant de proteger la marge Localeo pendant la construction et le pilotage des offres.
- une vision 360 reversements et paiements permettant de preparer et controler les campagnes de reversement deux fois par mois.
- une annulation back-office controlee des validations de prestation erronnees avant reversement paye.
- un live tracking WebPush commercant permettant de notifier les partenaires opt-in lors des achats confirmes de coffrets contenant leurs prestations actives.
- une recherche marketplace multi-scope permettant de retrouver rapidement une ville, un commercant, une prestation ou un coffret depuis une barre de recherche unique.
- Localeo Control, une PWA d'exploitation interne accessible depuis la page d'accueil backend, permettant de suivre l'activite Localeo en direct, le CA genere, la marge Localeo associee et de recevoir des alertes WebPush operationnelles.
- des profils back-office differencies permettant de limiter les acces SQLAdmin et routes internes par role, avec audit nominatif.
- une gestion de fermeture commercant permettant de masquer le commercant et ses prestations, bloquer les coffrets devenus incoherents, remplacer les prestations achetees non executees ou rembourser les clients si aucune substitution n'est possible, avec notification email et tracabilite complete.
- une vision 360 client permettant de retrouver rapidement un client, traiter ses demandes, consulter ses coffrets, renvoyer un QR code, gerer un remboursement et mesurer la valeur generee.
- une gestion documentaire transverse permettant de publier les documents publics, rattacher les contrats commercants et retrouver les documents clients/achats, sans stocker les binaires en base.
- une application `Localeo Live` grand public, distincte de `Localeo Control`, permettant aux utilisateurs finaux de consulter leurs coffrets, suivre leurs animations locales, recevoir des notifications utiles et decouvrir l'activite locale.
- un feed d'activite locale anonymise permettant de rendre la marketplace plus vivante sur les pages accueil, ville, commercant et coffret.
- une collecte de feedback post-prestation permettant de mesurer la satisfaction client, moderer les commentaires et afficher des signaux qualitatifs anonymises.
- un dashboard commercant permettant de suivre l'activite Localeo, l'encours, les montants et la repartition par version de prestation.
- une observabilite des Use Cases permettant de retrouver chaque invocation,
  son contexte, son issue et sa duree sans exposer de donnees sensibles.
- une Vision 360 Animation interne permettant de comprendre une animation depuis un point d'entree unique, d'en parcourir la chronologie et d'en analyser les indicateurs sur une periode bornee.
- un parcours de souscription partenaire Animation permettant de paramétrer les
  offres et prix, négocier ou offrir un abonnement, activer les droits après
  paiement Stripe et intégrer les abonnements encaissés au suivi du CA.
- un ordonnancement APScheduler embarqué dans le service FastAPI Render,
  protégé par une élection de leader PostgreSQL et réutilisant le socle de
  supervision des batchs existant.
- une Vision 360 Commercialisation permettant de connaître la vendabilité
  réelle des coffrets, d'être alerté lorsqu'une offre devient non vendable et
  d'accéder directement au traitement de chaque cause de blocage.
