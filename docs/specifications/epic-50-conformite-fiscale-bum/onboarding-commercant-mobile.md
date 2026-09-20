# Epic 50 - Onboarding commercant mobile

## Adresse du commerce obligatoire — 20 septembre 2026

L’[adresse postale de la fiche commerçant](../espace-commercant/adresse-postale.md)
est saisissable dans Onboard et requise pour valider ou revalider le dossier.
Le contrôle `POSTAL_ADDRESS_COMPLETE` ne peut pas être remplacé par une adresse
de facturation ou une commune de rattachement. Les vues ERP et le portail
Commerçant partagent cette source et sa validation.


## Pagination du portefeuille - 12 septembre 2026

`GET /internal/onboard/api/dossiers` conserve le champ `dossiers` et ajoute
`pagination: {page, taille, total}`. La page commence a 1; la taille par defaut
est 50, bornee entre 1 et 100. Le tri est `updated_at DESC, id DESC`.
Tous les filtres, y compris le code de blocage dans la checklist, et le
perimetre territorial sont appliques avant le total et la pagination SQL.
La liste charge uniquement les champs du resume, sans preparation financiere.

Localeo OnBoard affiche le total et les boutons Precedent/Suivant. Changer un
filtre revient a la premiere page; les requetes devenues inutiles sont annulees.
Les indicateurs globaux ne sont pas relus a chaque changement de page ou filtre,
mais sont actualises au chargement, au rafraichissement et apres les actions.

Les indicateurs agregent les snapshots en base en une lecture : compteurs
et moyennes, distribution des progressions, principaux blocages. Le calcul
conserve les controles non applicables, l'arrondi de chaque checklist, les
snapshots de rendez-vous et le perimetre d'autorisation.

## Modeles reutilisables visibles dans OnBoard - 8 septembre 2026

L'onglet Prestations & BUM distingue deux ensembles :

- **Modeles du commercant** : modeles ERP du commerce du dossier, y compris
  brouillons, actifs et archives, visibles sans aucun rattachement ni coffret.
  Afficher libelle, description, photo, statut, version, valeur TTC, commission,
  reversement et marge. Les montants sont en euros ; un taux historique absent
  reste explicitement non renseigne.
- **Prestations rattachees et diagnostic BUM** : copies appartenant a un coffret,
  avec les controles fiscaux et la vendabilite du coffret correspondant.

Le detail du dossier expose `modelesPrestation` separement de `prestations`.
La lecture reste limitee au commercant et au perimetre territorial autorise.
Aucun modele d'un autre commercant n'est inclus. La presence d'un modele ne
valide pas a elle seule les capacites BUM ou de publication d'un coffret.

Les actions Creer/Modifier un modele ouvrent l'atelier ERP canonique du commerce,
directement sur le formulaire choisi, sans imposer de coffret et sans dupliquer
les commandes. Un identifiant de modele absent du commerce affiche une erreur.
Les actions sont masquees si OnBoard est desactive ou le dossier termine.
Apres modification, reouvrir/recharger le dossier OnBoard pour relire les donnees.
Les modifications du modele ne se propagent pas aux prestations deja rattachees.

L'absence de coffret bloque seulement la creation d'une prestation rattachee,
avec une explication ; elle ne masque ni les modeles ni leur action de creation.

## Commission par prestation - decision du 7 septembre 2026

Voir la [regle commune](../epic-60-vision-360-commercialisation/commission-par-prestation.md). Dans le formulaire de
prestation, saisir la valeur TTC en euros et la commission Localeo en pourcentage.
Le reversement et la marge sont calcules et visibles avant enregistrement.
La confirmation de degradation de marge de coffret est retiree. Les versions
anterieures restent immuables ; une ancienne prestation sans taux exige une
saisie explicite lors de l'edition de ses nouvelles conditions.

## Objectif

### Correctif ANO-OB-01 - Photos des prestations

La creation et l'edition utilisent un selecteur de fichier avec apercu, jamais
une reference technique a saisir. Le remplacement est facultatif : sans fichier,
la photo existante reste conservee. PNG, JPEG, GIF et WebP sont acceptes dans
la limite configuree, exposee par `GET /internal/onboard/api/dossiers` dans
`imageMaxSizeBytes`. Le serveur valide toujours le contenu reel et le quota.
Le navigateur refuse les types/tailles invalides avant de creer la prestation
et bloque les doubles soumissions. Si la prestation est enregistree mais que
sa photo est refusee, le message distingue ces deux resultats ; l'operateur
reprend l'ajout de photo sur la prestation creee sans la recreer.

### Correctif ANO-OB-02 - Adresses de preparation financiere

La case "Utiliser la meme adresse pour le siege et l'exploitation" est cochee
si l'adresse d'exploitation est absente ou identique. Une adresse existante
distincte reste independante par defaut. Quand la case est cochee, rue,
complement, code postal, ville et pays sont repris en direct du siege ; les
champs d'exploitation sont en lecture seule. Decocher permet une saisie
distincte et restaure l'adresse independante precedemment saisie dans ce
formulaire. Sans adresse independante precedente, la copie courante reste
disponible comme point de depart.
La commande envoie les deux adresses completes, sans nouveau champ metier de
partage. Le complement d'exploitation est preserve. Le versionnement du profil,
les consentements de commission et les controles fiscaux restent applicables.

Ajouter une application interne mobile permettant a l'equipe Localeo de
finaliser l'inscription d'un commercant pendant un rendez-vous terrain. Le nom
definitif valide est **Localeo OnBoard** (`BUM-ARB-42`).

L'application guide le commercial, collecte les informations et preuves
manquantes, puis restitue une matrice de capacites. Elle doit permettre de
savoir, sans interpretation manuelle, si le commercant est pret a :

- apparaitre dans le portail et sur les surfaces publiques autorisees ;
- publier ses prestations et les rattacher a un coffret ;
- satisfaire les controles et preuves BUM ;
- recevoir les reversements nets et les factures de commission Localeo ;
- recevoir et traiter les demandes de facture de prestation ;
- se connecter a son espace commercant.

## Positionnement produit

Localeo OnBoard est une application interne distincte du BackOffice et de
l'espace Commercant. Elle est concue pour un usage tactile sur le telephone
d'un membre de l'equipe Localeo pendant un rendez-vous.

Elle n'est pas une nouvelle source de verite. Elle appelle les cas d'usage du
backend et affiche les donnees canoniques du referentiel commercant, des
prestations, de la conformite BUM, de Stripe Connect, de la facturation et de
l'identite-acces. Toute correction effectuee depuis l'application est donc
immediatement visible dans les autres surfaces autorisees.

Elle n'est pas davantage une source contractuelle : les clauses et engagements
BUM opposables figurent dans la convention de partenariat signee. OnBoard
collecte les informations utiles, controle la completude du dossier et prepare
le recapitulatif contractuel soumis au commercant.

## Parcours cible

```text
Preparation du rendez-vous
  -> ouverture ou reprise du dossier
  -> identification du commercant
  -> collecte des informations et documents
  -> configuration des prestations
  -> controles BUM et financiers
  -> invitation et test d'acces
  -> diagnostic final
  -> validation ou liste des actions restantes
```

Le dossier suit le cycle :

```text
BROUILLON -> RDV_PLANIFIE -> EN_COURS -> PRET_A_VALIDER -> VALIDE -> CLOTURE
                                |
                                +-> A_COMPLETER -> EN_COURS
```

Un dossier peut etre abandonne avec un motif. Sa cloture ne supprime aucune
preuve et ne publie rien implicitement.

## Checklist versionnee

La checklist est versionnee et constitue une vue guidee des donnees
canoniques. Chaque item possede un code stable, une categorie, une condition
d'applicabilite, un caractere obligatoire ou recommande, une source de preuve,
une date de validite eventuelle et les capacites qu'il bloque.

### Identite et referencement

- raison sociale, nom commercial, SIREN/SIRET et forme juridique ;
- adresse, coordonnees, geolocalisation et commune de rattachement ;
- representant legal et contacts operationnel, facturation et connexion ;
- verification des doublons avant toute creation ;
- informations publiques necessaires a la fiche commercant.

### Documents et engagements contractuels

La proposition minimaliste distingue les documents televerses, les informations
obligatoires et les preuves fournies par un systeme tiers :

| Code | Element | Regle MVP | Preuve |
| --- | --- | --- | --- |
| `MERCHANT_CONTRACT_SIGNED` | Contrat commercant signe | Toujours obligatoire | PDF ou photographies, version, date, signataires et qualite du representant |
| `LEGAL_REGISTRATION_VERIFIED` | Immatriculation de l'entreprise | Toujours obligatoire | SIREN/SIRET verifies ; extrait RNE ou Kbis recent seulement si la verification automatique est insuffisante |
| `COMMISSION_ACCEPTED` | Commission Localeo | Toujours obligatoire | Clause du contrat ou acceptation distincte versionnee, taux ou montant applicable |
| `BUM_CONTRACT_CLAUSES_ACCEPTED` | Clauses BUM de la convention | Obligatoire pour les prestations concernees | Convention et recapitulatif contractuel signes, version, date et signataire |
| `BANK_AND_PAYOUT_READY` | Coordonnees de reversement | Obligatoire avant reversement | Compte Stripe Connect avec charges et payouts actifs ; RIB seulement pour le fallback valide ou si Finance l'exige |
| `BILLING_PROFILE_COMPLETE` | Profil fiscal et de facturation | Toujours obligatoire | SIRET, adresse, regime et TVA intracommunautaire si applicable, contact facturation |
| `CHORUS_MANDATE_SIGNED` | Mandat de depot Chorus Pro | Conditionnel aux factures publiques deposees par Localeo | Mandat signe, version, perimetre et date |
| `REGULATED_ACTIVITY_EVIDENCE` | Autorisation, licence, diplome ou assurance | Conditionnel au type de prestation | Document, autorite emettrice, numero et expiration |
| `PUBLICATION_RIGHTS_CONFIRMED` | Droits sur textes, marques et medias | Obligatoire si non couvert par le contrat principal | Clause contractuelle ou autorisation distincte |

Les pieces d'identite du representant ne sont pas collectees par defaut dans
Localeo : une verification realisee par Stripe Connect est reutilisee lorsqu'elle
suffit. Une copie n'est demandee que si une obligation validee l'impose.

La liste exacte, les conditions et les durees restent configurables et soumises
a validation Juridica/Finance (`BUM-ARB-45`). Le code client ne fige jamais une
liste susceptible d'evoluer.

### Prestations et publication

- prestations creees avec intitule, description, prix ou valeur contractuelle,
  conditions et informations publiques obligatoires ;
- donnees factuelles collectees pour le diagnostic interne de chaque prestation ; le commercant ne qualifie ni la prestation ni le coffret
  concernee et reprises dans le recapitulatif contractuel ;
- screening execute et anomalies explicites ;
- contenus, medias et promesse garantie complets ;
- diagnostic de vendabilite sans blocage ;
- rattachement au coffret vise, avec publication par une action explicite et
  habilitee seulement lorsque tous les controles sont satisfaits.

### Finance et facturation

- profil fiscal et profil de facturation complets ;
- commission applicable affichee et acceptee, avec snapshot de la preuve ;
- compte Stripe Connect pret a recevoir les reversements lorsqu'il est requis ;
- coordonnee de reception des factures de commission Localeo ;
- coordonnee et canal de reception des demandes de facture de prestation ;
- capacite a deposer une facture et a suivre son traitement dans l'espace
  Commercant ;
- mandat et donnees Chorus Pro lorsque le contexte l'exige.

### Acces commercant

- email de connexion confirme avec le commercant ;
- invitation envoyee ou regeneree sans exposer son token au commercial ;
- activation du compte constatee ;
- test de connexion realise pendant le rendez-vous par le commercant sur son
  propre telephone (`BUM-ARB-48`) ;
- procedure de recuperation expliquee et contact de support confirme.

Le membre de l'equipe Localeo ne choisit, ne saisit ni ne conserve le mot de
passe du commercant.

## Onboarding independant du catalogue - 8 septembre 2026

Un commercant peut etre onboarde et valide sans prestation rattachee a un coffret.
La presentation contractuelle et la qualification BUM des coffrets relevent de
la preparation du catalogue par Localeo, pas des conditions d'onboarding du commercant.

Les controles PRESTATIONS_CONFIGURED, BUM_DATA_SCREENED,
BUM_COFFRETS_VALIDATED et COFFRET_PRESENTATION_READY sont non applicables sans
rattachement. Avec un rattachement et une fonction visee correspondante, ils
restent visibles comme recommandations non bloquantes. Les obligations propres
au commercant (identite, convention, finance et acces selon les fonctions visees)
restent bloquantes.

Les capacites catalogue restent calculees sur les faits : un dossier valide ne
rend pas un coffret publiable ni une commission facturable. La validation du
dossier n'exige pas PRESTATION_PUBLIABLE, COFFRET_PUBLIABLE, BUM_READY ou
COMMISSION_BILLABLE ; les controles de publication et de facturation restent
applicables dans leurs parcours respectifs. La checklist passe a ONBOARD_2026_03
et est recalculee au prochain diagnostic ou a la validation.

## Matrice de capacites

Un pourcentage global ne suffit pas. Le backend calcule separement :

| Capacite | Condition minimale |
| --- | --- |
| `PORTAIL_VISIBLE` | Referencement et donnees publiques valides |
| `PRESTATION_PUBLIABLE` | Prestation complete et commercant eligible |
| `COFFRET_PUBLIABLE` | Vendabilite, rattachement et qualification BUM valides |
| `BUM_READY` | Profil fiscal, convention signee, donnees factuelles et decision coffret requis |
| `COMMISSION_BILLABLE` | Identite de facturation, commission et preuve contractuelle completes |
| `INVOICE_REQUEST_READY` | Contact, acces et workflow de demande de facture operationnels |
| `PAYOUT_READY` | Onboarding Stripe Connect et exigences de reversement satisfaits |
| `PORTAL_ACCESS_READY` | Invitation active ou compte active et test de connexion constate |

Chaque capacite expose `READY`, `BLOCKED` ou `NOT_APPLICABLE`, ainsi que les
codes d'items bloquants. Le client ne peut jamais forcer un statut `READY`.

## Acces au portail avant activation - 8 septembre 2026

Les commercants `BROUILLON` et `REFERENCE` disposant d'un identifiant et d'un mot
de passe valide peuvent se connecter et demander un email de reinitialisation.
Leurs sessions portent uniquement `commercant:session` et `commercant:profil`.
Ces droits permettent de tester l'acces, de modifier le mot de passe et les
coordonnees, et de consulter, initialiser ou synchroniser Stripe Connect.
La configuration Stripe ne vaut pas activation commerciale par Localeo.

Validation de prestations, prestations commerciales, reversements, dashboard,
messages et animation restent sans autorisation dans cette session. Le statut
courant est controle a chaque requete : une ancienne session plus permissive
ne contourne pas un retour en preparation. Apres activation, une nouvelle
connexion est necessaire pour obtenir les droits commerciaux. Les comptes
suspendus ou archives ne peuvent toujours pas ouvrir de nouvelle session.
La compatibilite de consultation du profil d'une session suspendue est conservee.

Localeo Commercant affiche un accueil de preparation, avec Stripe Connect et
les liens vers le profil et le mot de passe, sans charger les donnees commerciales.
Les liens directs commerciaux reviennent a cet accueil. Les retours et reprises
du parcours Stripe restent utilisables. Le test d'acces peut ensuite etre confirme
par l'operateur OnBoard avant la cloture du dossier. Aucun statut commercant n'est
modifie automatiquement par ce test.

## Aptitudes courantes et reouverture du dossier

La fiche commercant ERP distingue l'etat historique du dossier (progression,
statut et cloture) de ses aptitudes courantes. Le champ `aptitudesActuelles` est
recalcule en lecture, meme apres cloture, sans modifier les snapshots du dossier,
sa version ni sa date de cloture. Les causes et responsables sont affiches pour
chaque aptitude non acquise ; les liens ouvrent le bon onglet OnBoard ou le
coffret concerne. Un modele seul ne remplace pas une prestation rattachee.

Une cloture ne garantit pas toutes les aptitudes commerciales : les controles
catalogue peuvent etre prepares apres le referencement et les donnees evoluent.
`Actualiser les aptitudes` recharge les faits courants. Ce bouton ne reouvre pas
le dossier et ne remplace pas les diagnostics fiscaux des prestations.

Un dossier `CLOTURE` peut etre rouvert depuis OnBoard ou la fiche ERP. Le motif
est obligatoire et la version attendue est verifiee sous verrou. Le dossier
repasse `EN_COURS`, sa date de cloture courante est retiree et les controles sont
recalcules. L'audit `MERCHANT_ONBOARDING_REOPENED` conserve le motif, l'acteur,
la cloture precedente et ses snapshots. Le statut du commercant est inchange.
Il faut ensuite valider et cloturer de nouveau le dossier. Un dossier abandonne
ne peut pas etre rouvert par cette action.

Routes : `POST /internal/onboard/api/dossiers/{id}/reouvrir` (motif,
expectedVersion) et `POST /internal/erp/api/commercants/{id}/dossier/reouvrir`
(motif, expected_version). Les controles d'acces et de perimetre des routes
existantes s'appliquent. La commande ERP conserve son mecanisme d'idempotence.
Les liens OnBoard acceptent `?dossier=<id>&onglet=finance` (ou documents, acces,
prestations, referentiel, suivi) ; tout onglet inconnu est ignore.

## Depot et controle des documents signes

Le suivi distingue une convention absente (`Convention ou contrat a joindre`)
d'une convention recue mais non validee (`Convention recue : controles a terminer`).
Dans ce dernier cas, les controles manquants sont detailles par piece : antivirus,
lisibilite, date de signature, version contractuelle et signataires. Un document
avec antivirus `NOT_CONFIGURED` reste bloquant et invite a contacter l'exploitation lorsque `LOCALEO_FEATURE_DOCUMENT_ANTIVIRUS_ENABLED=true`. Avec `false`, le scan et ses blocages sont desactives ; les autres controles restent requis.
Une seule convention ou un seul contrat satisfaisant tous les controles suffit ;
les metadonnees de plusieurs documents ne sont pas combinees. Une convention validee
disparait des actions restantes et reste visible comme complete dans la checklist.
Pour un dossier deja diagnostique, utiliser `Recalculer` pour actualiser le suivi.

Depuis le telephone, l'utilisateur peut photographier plusieurs pages ou
selectionner un PDF, controler l'ordre et la lisibilite, renseigner la
categorie et la date de signature, puis confirmer l'envoi.

Le backend reutilise `DocumentOrm`, calcule une empreinte, controle type et
taille, analyse le contenu selon le dispositif antivirus disponible et lie la
preuve au commercant, au dossier, au type contractuel et a sa version. Les
documents sensibles ne sont jamais servis par une URL publique.

L'application ne conserve pas durablement les contrats dans sa galerie ou son
stockage local. Le MVP est exclusivement en ligne et ne propose aucun mode hors
ligne documentaire (`BUM-ARB-46`). Toute extension future devra definir le
chiffrement, l'effacement et les appareils autorises avant activation.

## Supervision commerciale

L'equipe peut rechercher les dossiers, les affecter a un commercial, preparer
un rendez-vous, reprendre une saisie, filtrer les dossiers bloques et produire
la liste des pieces ou actions restant a obtenir du commercant.

Le recapitulatif de fin de rendez-vous distingue :

- ce qui a ete valide pendant le rendez-vous ;
- ce que Localeo doit encore traiter ;
- ce que le commercant doit fournir ou confirmer ;
- les capacites deja ouvertes et celles encore bloquees ;
- la prochaine action, son responsable et son echeance.

## Garde-fous

- authentification par le profil `Localeo Admin`, qui conserve tous les droits
  BackOffice dans le MVP (`BUM-ARB-47`) ;
- architecture preparee pour introduire plus tard un role restreint sans
  modifier les invariants metier ;
- aucune suppression de preuve depuis l'application ;
- motif obligatoire pour ignorer ou invalider un item ;
- journalisation des lectures sensibles, modifications, validations et
  telechargements ;
- aucune publication, qualification BUM ou activation financiere deduite d'une
  simple case cochee ;
- confirmation explicite des actions a effet externe ;
- donnees et documents chiffres en transit, URL de telechargement courte et
  controlee apres autorisation ;
- limitation des donnees personnelles affichees sur les listes et l'ecran
  verrouille.

## Hors perimetre initial

- signature electronique qualifiee integree ;
- fonctionnement hors ligne complet avec stockage durable des documents ;
- creation autonome du dossier par le commercant dans Localeo OnBoard ;
- remplacement du BackOffice, de l'espace Commercant ou de Stripe Connect ;
- validation juridique automatique d'un document photographie ;
- publication en masse sans confirmation humaine.

## Criteres de succes

- un commercial peut preparer, conduire et cloturer un rendez-vous depuis un
  telephone sans utiliser SQLAdmin ;
- la checklist explique chaque blocage et identifie son responsable ;
- toutes les preuves sont versionnees, rattachees et auditables ;
- aucune donnee canonique n'est dupliquee dans l'application ;
- un dossier declare valide satisfait reellement les diagnostics serveur ;
- le commercant termine le rendez-vous avec un acces fonctionnel ou une action
  de suivi explicitement assignee ;
- les fonctions de publication, BUM, commission, reversement et demandes de
  facture restent bloquees individuellement tant que leurs prerequis manquent.
# Increments livres le 1er septembre 2026

- l'identite legale et fiscale saisie dans OnBoard enrichit le profil de
  facturation canonique : raison sociale, forme juridique, SIREN/SIRET,
  regime et numero de TVA, representant, siege et adresse d'exploitation ;
  version optimiste, unicite du SIRET et habilitation territoriale protegent
  l'enregistrement ;
- le dossier conserve les fonctions visees et la checklist
  `ONBOARD_2026_02:<politique BUM>` adapte chaque controle a ces fonctions ;
  obligatoire, recommande et non applicable sont distincts sans qu'une case
  client puisse constituer une preuve ;
- les preuves propres a un type de commercant sont des regles versionnees de
  la politique BUM active et non une liste figee dans la PWA ;
- le dialogue de preparation recherche et reprend un dossier existant ou cree
  atomiquement un brouillon commercant canonique avec son affectation et son
  rendez-vous ; les doublons de nom dans une commune et d'email sont refuses ;
- la creation terrain ne cree aucun token et n'envoie aucune invitation :
  l'ouverture de l'acces reste une action distincte et confirmee ;
- le referentiel commercant est modifiable depuis le dossier avec une version
  optimiste dediee ; un conflit impose de recharger avant de ressaisir ;
- les conventions, contrats, justificatifs et mandats peuvent etre televerses
  en PDF ou en capture JPEG/PNG multipage ; le type reel, les contenus PDF
  actifs, la taille et l'antivirus sont controles avant stockage. Version,
  date, signataires, pages et confirmation de lisibilite sont historises ;
- l'invitation a l'espace Commercant utilise le service d'initialisation
  existant : le token n'est jamais retourne a Localeo OnBoard ;
- l'etat d'activation, de verrouillage et de derniere connexion est restitue
  depuis les donnees canoniques d'identite et d'acces.
- les prestations peuvent etre creees ou corrigees avec leurs montants depuis
  OnBoard ; chaque enregistrement cree une version et toute correction remet
  en cause la qualification BUM courante des coffrets affectes ;
- le screening fiscal utilise la politique active et ne confere jamais au
  commercial le pouvoir de qualifier le coffret ;
- la preparation financiere reutilise le profil canonique, trace l'acceptation
  de la commission et restitue Stripe Connect en lecture seule ;
- la matrice de huit capacites, la validation, la cloture, les filtres de
  portefeuille, le recapitulatif sans document sensible et les indicateurs de
  pilotage sont calcules cote serveur.
