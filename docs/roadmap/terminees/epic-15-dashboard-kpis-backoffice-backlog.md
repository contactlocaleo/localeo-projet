# Backlog Epic 15 - Dashboard KPI operationnel backoffice

## Perimetre

Epic source : `Epic 15. Dashboard KPI operationnel backoffice`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : creer dans le backoffice une vue de pilotage permettant d'identifier rapidement les blocages operationnels, les donnees incompletes, les achats a traiter, les coffrets en cours d'utilisation et les reversements a payer.

## Statut global

- Epic 15 : `Termine`
- Avancement : cadrage fonctionnel initial.

## Vision produit

Le dashboard doit etre une page d'exploitation quotidienne, pas un tableau analytique marketing. Il doit repondre a trois questions simples :

- Qu'est-ce qui bloque la mise en ligne ou l'exploitation ?
- Qu'est-ce qui attend une action backoffice ?
- Quels montants financiers restent a traiter ?

Chaque indicateur actionnable doit pointer vers la liste backoffice correspondante, idealement deja filtree.

## Sections attendues

### 1. Etat referencement

Objectif : detecter les donnees incompletes avant commercialisation.

KPI attendus :
- nombre de commercants par statut : `BROUILLON`, `REFERENCE`, `ACTIF`, `SUSPENDU`, `ARCHIVE` ;
- nombre de commercants non actifs : tous les statuts differents de `ACTIF` ;
- nombre de commercants inactifs ou bloques : `SUSPENDU`, `ARCHIVE` ;
- nombre de commercants sans acces commercant cree ;
- nombre de commercants avec invitation d'acces absente ou expiree ;
- nombre de commercants sans compte connecte Stripe ;
- nombre de commercants avec compte connecte Stripe non eligible ;
- nombre de coffrets par statut ;
- nombre de prestations coffret par statut.

Liens d'action recommandes :
- ouvrir la liste des commercants sans acces ;
- ouvrir la liste des commercants avec onboarding Stripe Connect incomplet ou bloque ;
- ouvrir les coffrets non actifs ;
- ouvrir les prestations non actives.

### 2. Etat commercialisation

Objectif : comprendre ce qui est publiable ou non dans le catalogue.

KPI attendus :
- coffrets actifs ;
- coffrets non actifs ;
- coffrets actifs avec au moins une prestation non active ;
- coffrets actifs avec au moins un commercant non actif ;
- prestations coffret actives ;
- prestations coffret non actives ;
- prestations avec montant de reversement nul ou manquant si ce cas est autorise techniquement ;
- prestations modifiees avec versions disponibles.

Regles de calcul :
- un coffret est commercialisable uniquement s'il est `ACTIVE` et si ses dependances commercant/prestations sont compatibles avec la publication ;
- une prestation coffret est commercialisable uniquement si elle est `ACTIVE` et rattachee a un commercant exploitable.

### 3. Etat paiement et achats

Objectif : suivre les achats et paiements client qui demandent une action ou une verification.

KPI attendus :
- achats coffrets par statut ;
- achats professionnels vs personnels ;
- achats payes ;
- achats non confirmes ou en attente de reconciliation ;
- paiements Stripe en attente ou non finalises ;
- achats professionnels avec instances non activees ;
- achats professionnels partiellement actives ;
- achats personnels avec instance active ;
- achats sans reference achat si ce cas existe encore.

Indicateurs operationnels :
- volume d'achats crees sur la periode courante ;
- volume d'achats payes sur la periode courante ;
- montant total paye sur la periode courante ;
- nombre d'achats necessitant une intervention.

### 4. Etat coffrets instances et utilisation des prestations

Objectif : suivre la vie des coffrets achetes et l'utilisation reelle des prestations.

KPI attendus :
- coffrets instances par statut : `EN_ATTENTE_ACTIVATION`, `ACTIVE`, `UTILISEE`, `EXPIREE`, `ANNULEE` selon les statuts existants ;
- coffrets instances actives ;
- coffrets instances en attente d'activation ;
- coffrets instances expirees ;
- coffrets instances annulees ;
- nombre total de prestations a consommer ;
- nombre total de prestations consommees ;
- taux global d'utilisation des prestations ;
- coffrets instances avec 0 prestation consommee ;
- coffrets instances partiellement consommees ;
- coffrets instances totalement consommees ;
- prestations a valider par commercant.

Regles de calcul :
- une prestation consommee correspond a `StatutPrestationCoffretInstance = VALIDEE` ;
- une prestation a consommer correspond a `StatutPrestationCoffretInstance = A_VALIDER` ;
- une instance totalement consommee a 0 prestation `A_VALIDER` et au moins une prestation `VALIDEE` ;
- une instance partiellement consommee a au moins une prestation `VALIDEE` et au moins une prestation `A_VALIDER`.

### 5. Etat reversement

Objectif : piloter les montants dus aux commercants et les operations de paiement.

KPI attendus :
- montant total a reverser ;
- nombre de commercants a payer ;
- nombre de mouvements `A_REVERSER` ;
- montant total des mouvements `A_REVERSER` ;
- reversements `EN_PREPARATION` ;
- montant total des reversements `EN_PREPARATION` ;
- paiements de reversement `A_INITIER` ;
- paiements de reversement `EN_COURS_MANUEL` ;
- montant total des paiements `EN_COURS_MANUEL` ;
- paiements de reversement `EXECUTE` sur la periode ;
- paiements de reversement en echec ;
- lots de paiement `PREPARE`, `EXPORTE`, `CLOTURE`, `ANNULE` ;
- mouvements deja reverses accessibles via la vue dediee.

Regles de calcul :
- le montant a reverser prioritaire correspond a la somme des mouvements en statut `A_REVERSER` ;
- les reversements en preparation ne doivent pas etre additionnes deux fois avec les mouvements `A_REVERSER` ;
- les mouvements `REVERSE` sont consideres clotures et exclus des montants a traiter ;
- les paiements `EN_COURS_MANUEL` correspondent aux virements exportes mais pas encore confirmes.
- le nombre de commercants a payer correspond au nombre de commercants distincts portant au moins un mouvement `A_REVERSER` ou un reversement/paiement encore non cloture selon la section affichee.

### 6. Etat exploitation emails et SMS

Objectif : detecter les messages sortants qui demandent une action technique ou operationnelle.

KPI emails attendus :
- emails `A_ENVOYER` ;
- emails `EN_COURS_ENVOI` ;
- emails envoyes mais non delivres selon le statut disponible ;
- emails `ECHEC_TEMPORAIRE` ;
- emails `ECHEC_DEFINITIF` ;
- emails bloques par nombre de tentatives ou prochaine planification future ;
- emails planifies en retard.

KPI SMS attendus :
- SMS `A_ENVOYER` ;
- SMS `EN_COURS_ENVOI` ;
- SMS envoyes mais non delivres selon le statut disponible ;
- SMS `ECHEC_TEMPORAIRE` ;
- SMS `ECHEC_DEFINITIF` ;
- SMS bloques par nombre de tentatives ou prochaine planification future ;
- SMS planifies en retard.

Regles de calcul :
- `A_ENVOYER` correspond a une action batch immediate si la date planifiee est vide ou depassee ;
- `ECHEC_TEMPORAIRE` correspond a un retry possible ;
- `ECHEC_DEFINITIF` correspond a une intervention ou une analyse manuelle ;
- les messages envoyes mais non delivres doivent etre distingues des messages jamais envoyes.

### 7. Etat support

Objectif : suivre la charge support et les demandes qui attendent une reponse.

KPI attendus :
- messages support non lus cote admin ;
- messages support non traites ;
- messages support `EN_COURS` ;
- messages support clotures sur la periode ;
- messages par cible : consommateur, commercant ;
- messages par motif ;
- demandes de facturation ouvertes ;
- demandes avec derniere reponse client/commercant plus recente que la derniere reponse admin ;
- delai du plus ancien message ouvert.

Regles de calcul :
- une demande support ouverte est une conversation non cloturee ;
- une demande non lue est une demande dont le statut de lecture admin indique une lecture manquante ;
- la priorite d'affichage doit favoriser les demandes non lues, non traitees et anciennes.

## User Stories detaillees

### `PRD-074` Etat referencement


Statut : `Termine`

En tant qu'operateur backoffice, je veux visualiser l'etat du referencement afin d'identifier les entites qui bloquent la mise en production.

Resultats attendus :
- le dashboard affiche les volumes de commercants par statut ;
- le dashboard affiche les commercants sans acces commercant ;
- le dashboard affiche les commercants sans compte connecte Stripe eligible ;
- le dashboard affiche les coffrets et prestations non actifs ;
- chaque indicateur actionnable ouvre la liste backoffice correspondante.

### `PRD-075` Etat commercialisation


Statut : `Termine`

En tant qu'operateur backoffice, je veux savoir quels coffrets et prestations sont effectivement commercialisables.

Resultats attendus :
- le dashboard distingue les coffrets actifs des coffrets non actifs ;
- le dashboard signale les coffrets actifs dont une dependance n'est pas exploitable ;
- le dashboard signale les prestations non actives ou incompletes ;
- le dashboard expose les incoherences sous forme d'alertes.

### `PRD-076` Etat paiement et achat


Statut : `Termine`

En tant qu'operateur backoffice, je veux suivre les achats et paiements afin d'identifier les traitements en attente.

Resultats attendus :
- le dashboard affiche les achats par statut ;
- le dashboard distingue les achats professionnels et personnels ;
- le dashboard affiche les achats payes mais non totalement actives ;
- le dashboard affiche les paiements en attente ou a reconciler.

### `PRD-077` Etat coffrets instances et utilisation


Statut : `Termine`

En tant qu'operateur backoffice, je veux suivre l'utilisation des prestations afin de connaitre l'etat reel des coffrets achetes.

Resultats attendus :
- le dashboard affiche les coffrets instances par statut ;
- le dashboard affiche le total des prestations consommees et a consommer ;
- le dashboard affiche les instances non consommees, partiellement consommees et totalement consommees ;
- le dashboard permet d'ouvrir les instances concernees.

### `PRD-078` Etat reversement


Statut : `Termine`

En tant qu'operateur backoffice, je veux connaitre le montant a reverser et le nombre de commercants a payer afin de piloter les paiements commercants.

Resultats attendus :
- le dashboard affiche le montant total a reverser ;
- le dashboard affiche le nombre de commercants a payer ;
- le dashboard affiche les mouvements a reverser ;
- le dashboard affiche les reversements en preparation ;
- le dashboard affiche les paiements en cours de traitement ;
- le dashboard affiche les paiements exportes en attente de confirmation ;
- le dashboard affiche les lots de paiement ouverts.

### `PRD-079` Etat exploitation emails et SMS


Statut : `Termine`

En tant qu'operateur backoffice, je veux suivre les emails et SMS sortants afin d'identifier les envois a lancer, non delivres ou en erreur.

Resultats attendus :
- le dashboard affiche les emails a envoyer ;
- le dashboard affiche les emails non delivres ou en erreur ;
- le dashboard affiche les SMS a envoyer ;
- le dashboard affiche les SMS non delivres ou en erreur ;
- chaque indicateur ouvre la liste backoffice des emails ou SMS concernes.

### `PRD-080` Etat support


Statut : `Termine`

En tant qu'operateur support, je veux suivre l'etat des demandes support afin de prioriser les messages entrants.

Resultats attendus :
- le dashboard affiche les messages non lus ;
- le dashboard affiche les conversations non traitees ou en cours ;
- le dashboard distingue les demandes consommateur et commercant ;
- le dashboard affiche les demandes par motif ;
- le dashboard met en evidence la plus ancienne demande ouverte.

## UX backoffice attendue

- Une entree de menu dediee dans le backoffice : `Dashboard operationnel`.
- Une page unique decoupee en sections :
  - Referencement ;
  - Commercialisation ;
  - Paiements et achats ;
  - Coffrets instances ;
  - Reversements ;
  - Exploitation emails et SMS ;
  - Support.
- Des cartes KPI compactes avec :
  - valeur principale ;
  - libelle ;
  - niveau d'alerte : information, attention, critique ;
  - lien vers la liste source quand applicable.
- Les montants doivent etre affiches en EUR.
- Les dates et periodes doivent utiliser le fuseau horaire operationnel configure.

## Criteres d'acceptation globaux

- Le dashboard est accessible uniquement aux administrateurs authentifies.
- Le dashboard ne modifie aucune donnee.
- Les KPI sont calcules depuis la base courante.
- Chaque KPI financier indique explicitement le statut metier pris en compte.
- Chaque KPI d'exploitation indique explicitement le statut email/SMS pris en compte.
- Les volumes affiches correspondent aux listes backoffice ouvertes depuis les liens.
- Les sections restent lisibles meme si certains volumes sont a 0.
- Les erreurs de calcul d'une section ne doivent pas rendre toute la page inutilisable ; la section en erreur doit l'indiquer clairement.

## Hors perimetre V1

- Graphiques temporels avances.
- Export Excel ou PDF du dashboard.
- Alerting automatique par email.
- Personnalisation des KPI par utilisateur.
- Comparaison multi-periodes.

## Questions ouvertes

- Faut-il filtrer les KPI par ville, type de coffret ou periode ?
- Quelle periode par defaut retenir pour les achats et paiements : jour, semaine, mois ?
- Faut-il distinguer `montant a reverser` et `montant deja prepare en reversement` dans deux cartes separees ou dans une synthese financiere unique ?
- Faut-il ajouter une alerte si un commercant actif n'a pas de compte connecte Stripe eligible ?
- Quels statuts exacts doit-on considerer comme `non delivre` pour les emails et SMS selon les retours Brevo ?
- Faut-il afficher un SLA support cible par type de motif ?
