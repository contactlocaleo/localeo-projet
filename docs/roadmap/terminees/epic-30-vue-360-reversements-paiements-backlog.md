# Backlog Epic 30 - Vision 360 reversements et paiements backoffice

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir au back-office une vision 360 dediee aux reversements et paiements afin de preparer, controler et suivre les campagnes de reversement faites deux fois par mois.
- Epic source : `Epic 30. Vision 360 reversements et paiements backoffice`
- Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)
- Cadence cible : deux campagnes de reversement par mois.
- Fenetres par defaut : campagne 1 du `1` au `15`, campagne 2 du `16` a la fin du mois.

## Probleme

La chaine de reversement est couverte par plusieurs surfaces :
- mouvements de reversement ;
- generation de reversements ;
- reversements en preparation ;
- lots de paiement ;
- paiements de reversement ;
- export CSV ;
- confirmation ou echec manuel ;
- audit et notifications commercants.

Pour une exploitation finance bimensuelle, ces informations restent dispersees. L'operateur doit reconstituer manuellement :
- les montants dus ;
- les commercants prets a etre payes ;
- les commercants bloques ;
- les paiements deja exportes mais non confirmes ;
- les echecs ou anomalies ;
- les notifications commercants creees apres paiement.

## Objectif operationnel

Permettre a un operateur finance de repondre rapidement a quatre questions :
- que doit-on reverser sur la prochaine campagne ?
- qu'est-ce qui bloque avant preparation du lot ?
- quels paiements sont en cours, exportes, executes ou en echec ?
- quels commercants ont ete notifies apres validation du paiement ?

## Perimetre MVP

### Vue campagne bimensuelle

La page doit afficher une periode de traitement cible :
- periode courante proposee automatiquement ;
- deux campagnes par mois : `1-15` et `16-fin de mois` par defaut ;
- dates ajustables manuellement ;
- sauvegarde optionnelle du filtre dans l'URL.

Decision MVP : une campagne est un filtre de periode, pas une nouvelle entite persistante.

Implications :
- aucune table `campagne_reversement` n'est creee en MVP ;
- les lots de paiement existants restent les objets metier persistants de regroupement ;
- l'URL doit porter `date_debut`, `date_fin` et le raccourci de campagne selectionne ;
- les exports recap utilisent la periode filtree et non un identifiant de campagne ;
- l'historique d'une campagne est reconstitue depuis mouvements, reversements, lots, paiements, emails et audit.

### Synthese financiere

Indicateurs attendus :
- montant total des mouvements `A_REVERSER` ;
- montant total des reversements `EN_PREPARATION` ;
- montant total des paiements `A_INITIER` ;
- montant total des paiements `EN_COURS_MANUEL` ;
- montant total des paiements `EXECUTE` sur la periode ;
- montant total des paiements `ECHEC` ;
- nombre de commercants concernes ;
- nombre de commercants bloques.

Decision MVP : les donnees de test ne sont pas encore identifiables techniquement dans le modele courant. La vue ne peut donc pas les exclure automatiquement tant que le marqueur cible de l'Epic 29 n'est pas livre.

Implications :
- l'exclusion automatique des donnees de test n'est pas un critere bloquant du MVP Epic 30 ;
- si des donnees de test peuvent polluer la campagne, la vue doit afficher un avertissement d'exploitation ;
- l'exclusion par defaut devra etre ajoutee lorsque le marqueur de donnees test sera disponible.

### File de traitement

La vue doit presenter une lecture par etape :
1. mouvements a agreger ;
2. reversements generables ;
3. reversements eligibles au paiement ;
4. paiements prepares ;
5. lots exportes ;
6. paiements a confirmer ;
7. paiements executes ;
8. paiements en echec.

Chaque etape doit exposer :
- volume ;
- montant ;
- lien d'action vers la page existante ;
- liste courte des cas prioritaires.

### Vision commercant

Pour chaque commercant concerne, la vue doit afficher :
- nom ;
- commune ;
- compte connecte Stripe eligible ou blocage ;
- titulaire du compte si disponible ;
- IBAN masque si necessaire, au format indicatif `FR76....1234` ;
- montant a reverser ;
- nombre de mouvements ;
- reversement ouvert si disponible ;
- paiement ouvert si disponible ;
- statut de notification email apres paiement ;
- lien vers la vision 360 commercant.

### Blocages et anomalies

La vue doit remonter explicitement :
- commercant sans compte connecte Stripe eligible ;
- montant non positif ;
- mouvement deja rattache a un reversement incoherent ;
- reversement sans ligne ;
- paiement en echec ;
- paiement exporte mais non confirme ;
- notification commercant absente ou en echec apres paiement `EXECUTE`.

## Hors perimetre MVP

- execution bancaire automatique ;
- rapprochement bancaire automatique ;
- format SEPA XML ;
- comptabilite analytique avancee ;
- creation d'une nouvelle source de verite financiere ;
- modification des regles de generation et de paiement deja portees par les Epics 12 et 13.

## Regles de gestion

- La vision 360 reversements s'appuie sur les donnees existantes et ne remplace pas les use cases de generation ou de paiement.
- Les deux campagnes mensuelles sont une aide d'exploitation, pas une contrainte bloquante : un operateur habilite peut ajuster les dates.
- Une campagne MVP est un filtre de periode, pas une entite persistante.
- Les montants doivent etre exprimes en EUR avec 2 decimales.
- Les lignes de test ne sont pas exclues automatiquement en MVP car elles ne sont pas encore identifiables techniquement.
- Lorsque le marqueur de donnees test de l'Epic 29 sera disponible, les lignes de test devront etre exclues par defaut.
- Les donnees bancaires completes ne doivent plus etre affichees pour un paiement manuel ; Stripe Connect porte l'onboarding et le payout.
- Dans la vision 360, le compte bancaire est limite a `actif oui/non`, titulaire et IBAN masque si necessaire.
- Dans l'export recapitulatif de campagne, l'IBAN complet n'est pas inclus par defaut.
- L'IBAN complet n'est plus reserve a un export bancaire de paiement : ce flux est decommissionne par l'EPIC 39.
- La vue doit distinguer `a reverser`, `en preparation`, `en cours de paiement`, `paye` et `en echec`.
- Les actions critiques restent auditees par les use cases existants.

## User Stories

### Story `PRD-207` - Ouvrir une vision 360 reversements et paiements

Priorite : `P0`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : donner a l'exploitation finance un point d'entree unique pour piloter les campagnes de reversement.

Criteres d'acceptation :
- une entree back-office `Vision 360 reversements` est disponible pour les operateurs habilites ;
- la page affiche une synthese par periode ;
- la periode par defaut correspond a la campagne bimensuelle courante ;
- la page propose des liens vers les campagnes Stripe, paiements reversement, operations Stripe et documentation.

### Story `PRD-208` - Filtrer par campagne bimensuelle

Priorite : `P0`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : travailler naturellement sur les deux fenetres de traitement mensuelles.

Criteres d'acceptation :
- l'operateur peut choisir la premiere ou la seconde campagne du mois ;
- les dates de debut et fin restent modifiables ;
- le filtre s'applique aux mouvements, reversements, paiements et lots quand une date pertinente existe ;
- le filtre est visible et partageable via l'URL.

### Story `PRD-209` - Afficher la synthese financiere de la campagne

Priorite : `P0`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : connaitre rapidement le montant a traiter et l'etat d'avancement.

Criteres d'acceptation :
- la page affiche un pipeline exclusif `a preparer`, `en cours chez Stripe`, `transfere aux commercants` et `en echec` ;
- chaque prestation apparait dans une seule etape, avec son montant et son volume ;
- le bloc economique rattache les paiements clients aux prestations de la campagne, meme si l'achat initial est anterieur a la periode filtree ;
- les frais Stripe d'encaissement proviennent du paiement client source et ne sont pas deduits des frais techniques du transfer Connect ;
- une valeur Stripe absente est affichee comme `A recuperer`, et non comme `0,00 EUR` ;
- les montants de test ne sont pas exclus automatiquement tant que le marqueur de donnees test n'existe pas ;
- chaque indicateur pointe vers la liste detaillee correspondante.

### Story `PRD-210` - Lister les commercants a payer et leurs blocages

Priorite : `P0`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : savoir quels commercants peuvent etre integres a la prochaine campagne et lesquels doivent etre corriges.

Criteres d'acceptation :
- la vue liste les commercants avec `Montant du`, `Deja transfere` et `Reste a transferer` ;
- chaque ligne affiche un etat metier lisible du reversement et le suivi distinct du virement bancaire Stripe ;
- les references et statuts techniques Stripe sont ranges dans un detail deplie a la demande ;
- les blocages sont visibles sans ouvrir plusieurs fiches ;
- un lien ouvre la vision 360 commercant.

### Story `PRD-211` - Suivre les paiements et lots de la campagne

Priorite : `P0`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : piloter le passage de la preparation au paiement confirme.

Criteres d'acceptation :
- la vue affiche les lots de paiement rattaches a la periode ;
- chaque lot affiche statut, nombre de paiements, montant, date d'export et fichier exporte ;
- les paiements `EN_COURS_MANUEL` sont mis en evidence comme a confirmer ;
- les paiements `ECHEC` sont mis en evidence comme a traiter.

### Story `PRD-212` - Controler les notifications commercants apres paiement

Priorite : `P1`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : verifier que les commercants sont informes quand un virement est valide.

Criteres d'acceptation :
- la vue affiche le statut de notification pour les paiements `EXECUTE` ;
- les notifications absentes ou en echec sont signalees ;
- le lien vers l'email sortant est disponible si l'email existe ;
- l'absence d'email de contact commercant est distinguee d'un echec technique.

### Story `PRD-213` - Exporter un recapitulatif de campagne

Priorite : `P1`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : conserver un support de controle interne pour chaque campagne.

Criteres d'acceptation :
- l'operateur peut exporter un recapitulatif `CSV` de la campagne ;
- l'export reprend les colonnes metier `montant_du`, `montant_deja_transfere`, `montant_restant_a_transferer`, `etat_reversement` et `virement_bancaire` ;
- les references techniques Stripe restent disponibles apres les colonnes metier ;
- l'export n'inclut pas d'IBAN complet par defaut ;
- l'export est audite.

Audit attendu :
- action : `reversement.campaign.summary.exported` ;
- ressource_type : `campagne_reversement_filtre` ;
- metadata minimale : `date_debut`, `date_fin`, `raccourci_campagne`, `nb_commercants`, `nb_reversements`, `nb_paiements`, `montant_total`, `hash_export_contenu`, `taille_export_octets`.

### Story `PRD-214` - Ajouter les alertes finance au dashboard operationnel

Priorite : `P1`
Statut : `Termine`
Statut implementation : `MVP implemente`

Valeur metier : ne pas rater les actions finance urgentes entre deux campagnes.

Criteres d'acceptation :
- le dashboard operationnel signale les paiements reversement a confirmer ;
- le dashboard signale les paiements en echec ;
- le dashboard signale les commercants bloques pour absence de compte connecte Stripe eligible ;
- chaque alerte pointe vers la vision 360 reversements filtree.

## Decisions actees

- La vue cible est une vue back-office finance, complementaire aux Epics 12, 13, 15 et 27.
- La cadence cible est deux campagnes par mois.
- Les fenetres par defaut sont `1-15` et `16-fin de mois`.
- Le MVP ne cree pas de nouvelle table de campagne ; une campagne est un filtre de periode.
- Les donnees de test ne sont pas encore identifiables techniquement ; leur exclusion automatique est dependante de l'Epic 29.
- L'export recapitulatif de campagne doit etre audite des le MVP.
- Toutes les user stories `PRD-207` a `PRD-214` sont retenues dans le perimetre cible ; le MVP back-office est implemente.
- La vision 360 expose au maximum le statut d'onboarding Stripe Connect et les references Stripe utiles ; elle ne doit plus exposer d'IBAN complet pour export bancaire.
- Les actions de generation, export et confirmation bancaire manuelles sont decommissionnees par l'EPIC 39 ; la vision cible suit les campagnes et transfers Stripe Connect.

## Priorisation retenue

- Toutes les stories de l'Epic 30 sont retenues dans le perimetre cible.
- Le MVP back-office des stories `PRD-207` a `PRD-214` est implemente.
- Les priorites `P0` et `P1` servent uniquement a ordonner la livraison.
- Le premier lot recommande couvre `PRD-207` a `PRD-211`.
- Le second lot recommande couvre `PRD-212` a `PRD-214`.
- Les donnees bancaires completes ne doivent pas etre exposees dans les exports recap par defaut.

## Proposition de tickets implementables

- `EP30-T01` Ajouter la route et l'entree back-office `Vision 360 reversements`.
- `EP30-T02` Implementer le calcul de campagne bimensuelle courante.
- `EP30-T03` Agreger les KPI mouvements, reversements, paiements et lots.
- `EP30-T04` Construire la table commercants a payer et blocages.
- `EP30-T05` Ajouter le suivi des lots et paiements a confirmer.
- `EP30-T06` Afficher le statut des notifications commercants.
- `EP30-T07` Ajouter l'export recapitulatif de campagne.
- `EP30-T08` Ajouter les alertes finance vers le dashboard operationnel.
- `EP30-T09` Ajouter les tests applicatifs des agregats finance.
