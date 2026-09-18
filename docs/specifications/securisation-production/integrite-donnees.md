# Corrections de l'audit d'integrite des donnees

Reference : [audit du 6 septembre 2026](../../audits/backend/audit-integrite-donnees-preproduction-2026-09-06.md).
Ce document consigne les regles corrigees et la recette de chaque constat.

## DATA-001 - Confirmation asynchrone du remboursement incomplete

L'administration et le webhook finalisent le remboursement dans la meme
orchestration applicative : annulation des droits restants, restitution du credit
eligible, audit et email en outbox. Les consommations passees restent historisees.
Un remboursement confirme ne regresse pas sur un evenement pending/failed ancien.
Les replays n'ajoutent pas d'email. Le verrou du remboursement serialise les
confirmations ; aucun commit intermediaire ne separe ces effets.

Exploitation : une confirmation retardee se traite par webhook ; ne pas fabriquer
un second remboursement pour reparer une projection. Les dossiers historiques
deja REMBOURSE doivent etre controles pour reperer des instances encore actives.

Recette : pending puis succeeded, succeeded puis pending/failed, replay succeeded,
droits annules et conservation d'une consommation historique.

Validation DATA-001 : 27 tests passes, dont un scenario PostgreSQL reel avec
confirmation differee, replay et evenements desordonnes ; 1 avertissement
SQLAlchemy preexistant sur les relations cycliques des profils.

## DATA-002 - Credit expire ignore lors de la confirmation d'un achat mixte

La confirmation exige montant Stripe + credit attendu = total de l'achat.
La part credit vient de la demande Checkout durable, jamais de la seule presence
d'une reservation encore ACTIVE. Le credit attendu exige une reservation active,
non expiree et du meme montant, puis une capture effective avant confirmation.

Un paiement tardif insuffisamment finance est enregistre avec le statut
RECONCILIATION_REQUIRED et un evenement d'audit ; aucun droit nouveau n'est cree.
Les webhooks financiers suivants ne suppriment pas cet incident. L'achat demeure
en attente de confirmation. Les reservations restent limitees a 30 minutes :
une session Checkout encore ouverte ne prolonge pas le credit. Ce choix traite
explicitement le paiement tardif au lieu d'accorder des droits sans financement.

Exploitation : examiner purchase.financing.reconciliation_required, comparer la
part Stripe recue, la demande initiale et le registre de credit. Ne pas forcer le
statut de l'achat en SQL ; rembourser la part encaissee via la procedure finance
si le financement ne peut pas etre regularise. Ne jamais reutiliser une ancienne
reservation deja liberee ou capturee pour une nouvelle confirmation.

Recette : credit absent, expire (y compris encore ACTIVE), libere, capture,
montant incorrect, paiement integral et preservation de l'incident par webhook.


Validation DATA-002 : 36 tests passes, dont PostgreSQL (paiement partiel bloque
et incident conserve apres projection financiere).

## DATA-003 - Remboursement mixte calcule sur le total brut

Le montant de la demande reste le total commercial rembourse. L'appel Stripe
utilise exclusivement la part monetaire de l'instance, apres deduction des lots
de credit effectivement captures. Les centimes restants sont affectes selon
l'ordre UUID des instances, comme lors de la restitution des lots de credit.
Un achat integralement en credit ne declenche aucun appel de remboursement Stripe.
Sa reference locale credit-refund est distincte d'une reference fournisseur re_.
Une ventilation historique absente ou incoherente bloque l'execution.

Exploitation : rapprocher le total rembourse, la part Stripe et la restitution
de credit ; ne pas assimiler la reference locale credit-refund a un mouvement
bancaire. Les echeances initiales des lots restitues restent appliquees.

Recette : action administrative reelle avec paiement mixte 60/40, paiement 100 %
credit sans appel fournisseur, et repartition de montants non divisibles en cents.

Validation DATA-003 : 20 tests passes, dont quatre scenarios PostgreSQL et les
tests de la passerelle Stripe ; avertissements cycliques SQLAlchemy preexistants.


## DATA-004 - Transfer Stripe externe avant persistance durable

La campagne valide en base les identifiants locaux et l'intention (requete
complete, cle Stripe, date initiale) avant l'appel fournisseur. Une interruption
laisse le mouvement EN_CAMPAGNE reprenable avec les memes parametres, meme si le
referentiel change. Le webhook peut retrouver le paiement par son identifiant.
La reprise automatique est limitee a 23 heures depuis la premiere demande.
Une intention historique absente ou trop ancienne exige un rapprochement ; une
nouvelle cle ne doit jamais masquer un resultat fournisseur inconnu.

Exploitation : controler Stripe et ses metadonnees avant toute regularisation
historique. Le lancement d'une campagne ne recree pas un transfer au-dela du
delai. La confirmation par webhook reste possible sans limite de 23 heures.

Recette : arret du processus apres acceptation fournisseur, restauration de la
seule transaction validee, reprise identique et tests des limites temporelles.

Validation DATA-004 : 33 tests passes (panne apres acceptation, commit refuse, reprise et webhooks).

## DATA-005 - Validation et remboursement simultanes incompatibles

Consommation, annulation de consommation et remboursement verrouillent la meme
instance avant de verifier leurs preconditions. Un remboursement EN_COURS gele
les consommations ; ce statut est valide en base avant l'appel Stripe et survit
a une panne. Seul le resultat fournisseur peut liberer ce gel. Le formulaire
CRUD ne modifie plus les etats financiers ni ne supprime une demande.
Les campagnes reverrouillent chaque mouvement avant de preparer son transfer ;
l'annulation verrouille aussi ce mouvement et refuse une intention deja engagee.

Exploitation : apres timeout fournisseur, rapprocher le remboursement en cours.
Ne pas forcer un echec administratif pour rendre les droits consommables.
Recette : contention reelle PostgreSQL sur l'instance, puis refus de consommation
apres persistance du remboursement en cours, sans validation ni reversement cree.

Validation DATA-005 : 24 tests passes, dont cinq scenarios PostgreSQL et la contention reelle.

## DATA-006 - Reversement calcule depuis la prestation courante

Le libelle et les conditions financieres de la consommation viennent de la
version referencee par le droit vendu. Le reversement, la valeur brute et la
commission utilisent ce meme instantane ; une edition du catalogue ne les change
pas. Une version absente, y compris un numero historique NULL, bloque avant toute
validation. Aucun repli silencieux sur la version courante n'est autorise.

Exploitation : inventorier les droits dont la version est absente avant activation.
Reconstituer uniquement depuis les preuves de vente et les archives de versions,
avec une correction de donnees auditee ; ne pas recopier les montants courants.
Recette : achat en version 1 a 20 EUR, catalogue version 2 a 30 EUR, consommation
et dette de 20 EUR ; version introuvable refusee sans modification du droit.

Validation DATA-006 : 10 tests passes, dont la consommation complete sur PostgreSQL avec catalogue modifie.

## DATA-007 - Prestation reouverte mais impossible a revalider

Chaque consommation est une occurrence distincte. L'annulation date cette
occurrence et conserve son mouvement annule. Un index unique partiel interdit
deux occurrences actives pour le meme droit. Les nouveaux mouvements portent
une cle par occurrence. La transaction QR reference son occurrence ; le rejeu
exige le meme commercant, le meme droit et une occurrence non annulee.
Une ancienne transaction annulee ne peut pas rejouer le succes d'une nouvelle.

Migration v219 : suppression de l'ancienne unicite globale, datation de reprise
des occurrences dont le mouvement est deja ANNULE, ajout des index et du lien
transaction. Cette date de reprise ne pretend pas remplacer la date d'audit
historique. Les transactions historiques sans association exigent un nouveau
scan ; aucune association n'est inventee.
Recette : validation, rejeu, annulation, refus ancien rejeu, nouvelle validation,
refus seconde occurrence active en SQL et refus annulation d'une ancienne occurrence.

Validation DATA-007 : 51 tests passes ; migration depuis ancienne unicite et cycle complet testes sur PostgreSQL.

## DATA-008 - Restrictions ERP contournables par des acces historiques

Les interfaces historiques sans filtrage territorial sont reservees a ADMIN :
SQLAdmin, routes internes hors ERP, moderation de profils, documentaire, DAM et
APIs reutilisant la dependance administrative. La session doit porter un role
explicite et une identite. Les visions achats et animation utilisent le meme
contexte territorial que l'ERP ; une session ancienne ne devient jamais ADMIN
par defaut. Les redirections d'anciens ateliers gardent les controles ERP.

Arbitrage de securisation : EXPLOITATION conserve les parcours ERP limites aux
communes affectees. FINANCE, SUPPORT et LECTURE_SEULE ne recoivent aucun acces
implicite aux anciens ecrans globaux. Cette restriction prime sur les intentions
anciennes de la matrice EPIC 35 tant que ces ecrans n'appliquent pas un perimetre
serveur. Pour les operations globales, utiliser un compte ADMIN autorise ; ne pas
elargir un role en session pour contourner un refus. Reconnexion des sessions
sans role obligatoire.
Recette : refus HTTP des anciennes actions pour chaque role restreint, y compris
une commune explicite, preservation des autorisations territoriales ERP.

Validation DATA-008 : 55 tests passes, dont 25 refus HTTP sur les routes historiques et les controles de session ERP.

## DATA-009 - Publication sensible par GET

La publication d'un profil, les batchs administratifs, la generation de recu
et les actions SQLAdmin exigent POST et la preuve d'origine du middleware CSRF.
GET n'execute plus ces commandes ; il affiche une confirmation avec formulaire
POST, pour conserver l'utilisabilite des liens existants. Le bouton de moderation
publie directement via formulaire POST. Les GET de consultation et de calcul
sans mutation (dont l'assistant de montant avant saisie) restent des lectures.
Les API de publication etaient deja en POST et conservent leurs protections.

Exploitation : adapter les automatisations utilisant les anciennes URL GET a un
appel POST autorise ; ne pas considerer la page de confirmation comme un resultat
de batch. Les appels sans preuve d'origine avec cookie sont refuses.
Recette : GET sans effet, POST d'origine hostile refuse, POST local autorise ;
inventaire des routes SQLAdmin garantissant POST sur chaque handler d'action.

Validation DATA-009 : 57 tests passes ; publication POST, origine hostile, confirmations et inventaire des actions SQLAdmin.

## DATA-010 - Suppression du fichier avant validation SQL

Le remplacement ecrit une nouvelle cle sans supprimer la precedente. L'audit
conserve les deux cles et empreintes. La suppression autorisee est logique en
base ; aucune commande documentaire ne supprime physiquement un objet avant ou
apres commit. Un rollback conserve donc le fichier encore reference par SQL.

Arbitrage : conserver les binaires surnumeraires est preferable a perdre une
preuve. Aucune purge automatique n'est activee par ce correctif. Surveiller le
volume du stockage ; une purge ulterieure doit rapprocher references en base,
audit, sauvegardes et retention documentaire, avec inventaire prealable. Ne pas
activer une expiration S3 globale sur ce prefixe.
Recette : rollback apres remplacement, rollback apres suppression, lecture de
l'original et absence de delete physique meme apres suppression logique validee.

Validation DATA-010 : 21 tests passes ; rollback SQL et lecture du binaire original verifies sur PostgreSQL.

## DATA-011 - Conservation documentaire non imposee

Le contenu d'un document publie, archive, signe, contractuel ou comptable est
immuable. Une correction exige un nouveau document ; une nouvelle version HTML
ne remplace plus un HTML probant. Les versions derivees recoivent un numero
croissant sous verrou de leur source. Les brouillons non probants restent editables.

La suppression logique d'une preuve exige son archivage et la fin de retention :
10 ans apres depublication pour le public, 5 ans apres fin de relation commerciale
pour un contrat, 10 ans apres cloture d'exercice pour une piece comptable.
En l'absence de date de depart fiable, la suppression est refusee. Les dates de
fin de relation et de cloture n'etant pas etablies dans ce referentiel, ces pieces
restent conservees. Aucune purge physique automatique n'est ajoutee (UC-21B).

Exploitation : archiver une preuve obsolete ; creer une nouvelle version corrigee.
Une date d'expiration de contrat ne prouve pas la fin de relation commerciale.
Recette : refus de remplacement avant toute ecriture de fichier, conservation
apres archivage, limites 5/10 ans et dates de depart manquantes.

Validation DATA-011 : 29 tests passes, dont immuabilite et retention appliquees par le service sur PostgreSQL.

## DATA-012 - Instance encore active apres les deux dernieres consommations

Le recalcul des droits restants et du statut de l'instance appartient a la meme
transaction que la validation, sous le verrou commun introduit par DATA-005.
Deux consommations de droits differents d'un meme coffret sont serialisees :
la seconde observe la premiere et passe l'instance a UTILISE sans droit restant.
Ce point reutilise la correction de concurrence DATA-005 ; aucun second mecanisme
de verrouillage n'est ajoute.

Recette dediee : deux connexions demarrent ensemble la consommation des deux
derniers droits ; deux validations et mouvements, aucun droit restant et une
instance UTILISE. Exploitation : les anciennes instances ACTIVE sans droit
restant doivent etre rapprochees avant de corriger leur projection historisee.

Validation DATA-012 : scenario PostgreSQL concurrent reussi et tests de l'entite coffret instance rejoues.

## DATA-013 - Plusieurs documents publics publies pour un meme type et scope

Tous les chemins (publication, creation directement publiee, HTML derive) passent
par la meme commande. Un verrou transactionnel documentaire serialise les
publications et l'acces aux sources. La publication archive les anciens documents
du meme type ayant au moins un scope commun, puis publie le nouveau dans la meme
transaction. L'archivage concerne le document entier en cas de scopes multiples.

La migration v220 ajoute une table de publications uniques (type, scope) tenue
par trigger : une ecriture SQL concurrente ou hors service ne contourne pas
l'unicite. Elle archive les anciens doublons selon date de publication puis UUID.
Une version HTML devient la publication active ; son fichier source reste
telechargeable comme complement tant que cette version est publique.

Exploitation : appliquer v220 avant utilisation et controler les publications
retenues apres reprise historique. Les autres versions restent archivees selon
DATA-011. Recette : deux publications simultanees, conflit SQL direct, creation
publiee et HTML derive avec acces au fichier source.

Validation DATA-013 : 33 tests passes ; concurrence PostgreSQL, contrainte SQL et reprise des doublons historiques verifies.

## DATA-014 - Outbox email et SMS non reservees atomiquement

La selection utilise FOR UPDATE SKIP LOCKED et valide les reservations avant
envoi. Une reservation EN_COURS_ENVOI sans identifiant fournisseur devient
reprenable apres 10 minutes. Le domaine controle delai, planification et plafond
de cinq tentatives. Un abandon a la cinquieme tentative passe en echec definitif.
Avant l'appel, le worker reverrouille le message et verifie qu'il possede encore
la reservation ; le verrou est conserve jusqu'a l'enregistrement de la reponse.
Les adaptateurs ont un timeout reseau de 20 secondes.

La livraison reste au moins une fois : une acceptation fournisseur dont la
reponse est perdue peut conduire a une relivraison. Le correctif empeche les
doubles envois par workers concurrents et les reservations bloquees indefiniment,
sans promettre une garantie exactement une fois absente du protocole fournisseur.
Exploitation : surveiller anciennete EN_COURS_ENVOI et echecs definitifs ; un
message portant deja une reference fournisseur est rapproche, jamais reenvoye.
Recette : deux connexions concurrentes, abandon puis reprise, verrou pendant
l'envoi et absence de second appel apres succes, pour email et SMS.

Validation DATA-014 : 52 tests passes ; reservation exclusive, reprise et envoi unique verifies sur PostgreSQL pour email et SMS.

## DATA-015 - Migrations non autonomes sur base vide

Le gestionnaire reconnait une base vide et applique le socle SQL fige
baseline_v147.sql, puis le rattrapage v147 et les migrations ulterieures. Le socle
cree les tables avant les cles etrangeres cycliques et inclut les prerequis
historiquement presents uniquement dans le bootstrap Python. Il ne depend pas
du modele ORM evolutif a l'execution. Son checksum est suivi comme les migrations.

Une base non vide sans socle reconnu est refusee ; le schema cible doit etre
public. Le dry-run n'ecrit rien. Les enveloppes BEGIN/COMMIT des anciens fichiers
sont retirees hors blocs SQL internes : le runner detient la transaction qui
associe le DDL et son enregistrement. Une migration en echec ne laisse ni son DDL
ni une marque de succes. Les migrations historiques restent inchangees ; les seeds
de test v148/v149 restent exclus par defaut.

Exploitation : utiliser scripts/database/apply_migrations.py, y compris sur base neuve,
avant de demarrer les workers. Ne pas regenerer ni modifier un socle applique.
Recette : base PostgreSQL vide, dry-run sans effet, migrations completes, conformite
de toutes les colonnes ORM chargees par l'application, second passage vide,
rollback d'un script contenant COMMIT puis erreur et refus d'un schema inconnu.

Validation DATA-015 : 10 tests passes, dont 2 sur PostgreSQL dedie initialement vide ; migrations, conformite ORM, rejouabilite et rollback verifies.

## DATA-016 - Referentiel documentaire contradictoire

L'architecture designe l'ADR EPIC 39 acceptee comme decision applicable :
reversements exclusivement Stripe Connect, aucun fallback bancaire manuel.
Les transfers plateforme-compte connecte et payouts vers la banque sont distincts.
La reconciliation operateur rapproche les operations Stripe ; elle ne cree pas
un virement manuel. Les anciens objets restent des archives non actionnables.
Le backlog EPIC 12 est deja explicitement historique et decommissionne.

Validation DATA-016 : la suite generale valide les parcours Stripe Connect et
le caractere non modifiable des vues transactionnelles ; les liens vers l'ADR
et la procedure d'exploitation ont ete verifies. Aucun changement de code requis.
