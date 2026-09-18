# Epic 60 - Specifications fonctionnelles detaillees V1

> Statut : reference d'implementation, sur delegation explicite de l'utilisateur.
> Perimetre : PRD-561 a PRD-582. Les hypotheses H01-H08 remplacent les attentes
> de confirmation ; elles sont a reporter dans le rapport final.

## Correction metier du 7 septembre 2026

La [commission par prestation](commission-par-prestation.md) remplace les
regles historiques de marge cible de coffret/type. Les montants sont saisis en
euros, la commission en pourcentage, et le reversement est calcule par le serveur.
Les anciens arguments de confirmation de degradation restent sans effet pour
compatibilite ; le plafond absolu prix >= reversements reste applicable.

## 1. Decisions et hypotheses d'implementation

| ID | Decision prise sous delegation | Origine |
| --- | --- | --- |
| H01 | La file diagnostic est en lecture ; reevaluation POST seulement. Les mutations passent par les ateliers. | COM360-ARB-05 |
| H02 | Alertes a la perte de vendabilite, a l'indetermination, occurrences nouvelles si causes changees ; resolution automatique au retablissement. Pas de fausse perte lors du backfill. | COM360-ARB-06 |
| H03 | ADMIN : toutes les commandes ; EXPLOITATION : lecture et edition dans ses communes, publication comprise, aucune administration des secrets. Les autres roles n'accedent pas aux ateliers de referencement ; leurs fonctions existantes restent separees. Role absent refuse. | ERP-ARB-03, socle de session actuel |
| H04 | Retenir les gardes statut, prix positif, au moins une prestation active, commune publiee ; conserver les gardes commercants sur toutes les prestations et les flags BUM/Stripe existants. Le contenu indicatif manquant est un avertissement. | COM360-CON-02/03/04 |
| H05 | Fraicheur 20 minutes, traitement des demandes chaque minute, reconciliation complete par lots ; historique/alertes fermees 12 mois, idempotence 24 h. Aucun effacement des alertes ouvertes. | COM360-CON-07/09 |
| H06 | Premiere livraison de modele autonome par commercant ; rattachement par copie versionnee, sans propagation automatique. Pas de migration des prestations historiques en modeles. | ERP-ARB-02 |
| H07 | Les engagements existants empechent les retraits dangereux ; le traitement exceptionnel suit les parcours de fermeture/remboursement existants. Les versions vendues ne sont pas reaffectees. | ERP-ARB-12/15 |
| H08 | Bascule directe des entrees et ateliers ; fonctions SQLAdmin utiles reintegrees comme administration avancee avec permissions, anciennes interfaces de coffret/commercant remplacees. Pas de changement des API publiques hors garde canonique. | ERP-ARB-07 |

## 2. Acteurs et autorisations

### Organisation de la navigation — decision utilisateur du 6 septembre 2026

L'accueil expose directement Dashboard operationnel, Localeo Onboard et Localeo
Control. Le dashboard reste un ecran de pilotage autonome. Une entree `Visions 360`
regroupe coffrets, commercants, clients, achats, reversements, animations,
partenaires animation et couverture territoriale. Les fiches coffret/commercant
gardent une destination canonique commune avec les ateliers.

La section `Exploitation courante` regroupe les operations quotidiennes,
paiements/facturation, disponibilite du catalogue et Localeo Control. Le
`Referencement par objet` donne acces a Onboard, commercants/prestations,
coffrets et partenaires animation. L'`Administration par objet` conserve les
referentiels et outils de gestion avec recherche. La supervision technique
reste distincte : sante, batchs, configuration et audit.

Les profils sans droits ERP gardent l'accueil SQLAdmin existant ; le lien ERP
ne leur est pas propose. Une sous-route ERP inconnue ou un identifiant de fiche
mal forme produit 404, sans afficher une page de remplacement trompeuse.

### Controle des acces

L'identite vient exclusivement de la session serveur signee. ADMIN dispose
du perimetre global. EXPLOITATION dispose de `admin_commune_ids` explicites ;
liste vide = aucun acces. Toute ressource chargee et toute destination choisie
sont controlees : commercant, coffret, modele et prestation. Une ressource hors
perimetre produit 404, un role interdit 403, une session absente 401.
Une session historique sans role est incomplete : les API renvoient 401 et les
pages ERP redirigent vers `/admin/login` pour renouveler la session. Aucun role
ADMIN n'est deduit par defaut. La casse et les espaces du role sont normalises.

Les commandes exigent protection CSRF liee a la session et verification de
l'origine lorsqu'elle est fournie. Le nom de l'acteur ne peut etre fourni par
le formulaire. Les changements sont audites sans secrets Stripe ni contenu
contractuel dans les metadonnees. La consultation detaillee est auditee.
La connexion avec un cookie existant utilise le meme controle d'origine.
Derriere une terminaison TLS, HTTPS public vers HTTP interne est accepte seulement
si le navigateur declare `Sec-Fetch-Site: same-origin` et si l'hote et le port
publics correspondent. Aucun domaine tiers ni en-tete de proxy arbitraire ne
peut remplacer cette preuve. Les ports standards sont normalises.
Les listes, compteurs et liens appliquent les memes droits avant pagination.

Les pages internes ne sont pas mises en cache offline. Les textes sont
echappes et les destinations generees par l'application, jamais du HTML libre.

## 3. Navigation et presentation

Six rubriques : Mon activite, Commercants et catalogue, Operations, Finance,
Supervision, Referentiels et administration. Une ressource a une fiche unique.
Les fonctions d'achats, support, animation, finance, documents et supervision
existantes sont accessibles depuis leurs rubriques sans recreer leurs metiers.

L'accueil montre les prochaines actions du perimetre, les pertes d'offres et
les echeances de dossiers, puis les compteurs. Les trois actions principales
sont creer un commercant, creer un coffret et traiter une indisponibilite.
La recherche retrouve nom/UUID, sans pretendre a une reference metier inexistante.

These visuelle : espace de travail calme, fond clair, navigation bleu profond,
accent orange Localeo, tableaux denses lisibles et formulaires alignes.
Plan de contenu : entete de contexte/action, liste ou formulaire principal,
diagnostic/economie secondaire, historique replie. Pas de hero marketing.
Interactions : ouverture douce des onglets, focus explicite des champs et
retour de sauvegarde annonce ; animations reduites selon la preference systeme.

En cours de saisie : avertir avant sortie non sauvegardee. Apres refus : garder
la saisie et expliquer les champs/causes. Apres succes : afficher la ressource
et sa version. Une erreur ne doit jamais etre remplacee par un faux etat vide.

## 4. Dossier commercant : PRD-573, 575, 576

### Creation

Champs : nom (1-200 caracteres apres trim), commune existante autorisee,
type commercant existant, description (0-5000), contact nom/prenom (0-200),
email/telephone optionnels valides, image optionnelle par reference media.
La creation initialise BROUILLON. Elle cree/reutilise un seul dossier Onboard
pour le commercant. Aucun compte Stripe ni envoi d'invitation automatique.
Rechercher les doublons sur nom et commune et proposer d'ouvrir l'existant ;
ne jamais fusionner ou remplacer automatiquement un commercant.

### Edition et activation

L'edition exige la version attendue du referentiel. Un conflit produit 409
avec demande de rechargement, sans ecraser le travail concurrent. Les champs
Stripe ne sont pas des champs de saisie libre de l'atelier.

Le statut commercant reste distinct du cycle Onboard. Une activation exige
le controle des prerequis applicables ; un dossier incomplet affiche ses
actions correctives. Suspendre/archiver exige une analyse des prestations et
engagements. La commande refuse de casser des instances en cours ou une offre
active ; elle oriente vers le traitement existant. Aucune suppression physique.

### Onboard integre

Lire et modifier le meme dossier que Localeo Onboard. Conserver BROUILLON,
RDV_PLANIFIE, EN_COURS, A_COMPLETER, PRET_A_VALIDER, VALIDE, CLOTURE, ABANDONNE
et les transitions de domaine actuelles. Prochaine action, responsable,
echeance et notes sont repris ; le responsable textuel n'est pas une preuve
d'affectation a l'utilisateur connecte.

Presenter checklist et capacites courantes avec leur date : portail, offre,
BUM, facturation, reversement et acces. Un commercant sans vente n'est pas en
incident. COFFRET_PUBLIABLE Onboard ne remplace pas le verdict du coffret.
Diagnostic, validation/cloture et preparation financiere reutilisent les
commandes existantes. Une cloture de dossier ne ferme pas le commerce.

## 5. Modeles et prestations : PRD-574, 578

Un modele autonome appartient a un commercant et contient libelle (1-200),
description (1-5000), image facultative, valeur TTC et reversement conseille
en centimes dans les API, version et statut BROUILLON/ACTIVE/ARCHIVE.
L'IHM saisit la valeur en euros et le taux de commission Localeo ; le reversement
est calcule au centime. Le taux saisi est conserve sur le modele et sa copie. Les montants sont
entiers >= 0, valeur >= reversement ; ils ne representent pas un prix client
de coffret. Une edition exige la version attendue et incremente la version.

Rattacher exige un coffret et un commercant autorises, la version du modele
selectionne et la version du coffret. Le resultat est une prestation de
coffret BROUILLON avec provenance (modele, version) et conditions copiees.
Le meme modele ne peut etre rattache deux fois au meme coffret par accident.
Une nouvelle version du modele ne modifie aucun rattachement existant.

Une prestation rattachee est editable dans les deux ateliers avec version
attendue, valeur TTC, reversement, libelle, description, image et statut.
La propriete commercant/coffret est immuable pour cette commande. Chaque
modification cree un instantane de version et invalide le diagnostic BUM
selon les regles existantes ; les instantanes des achats ne changent pas.
Les propositions commercant en attente restent gerees par la moderation
existante, sans remplacement par une edition automatique.

Les changements de reversement verrouillent le coffret puis calculent le
disponible sans compter deux fois la prestation editee. Total des reversements
hors SUSPENDU/ARCHIVE <= prix. Aucune marge cible de coffret ou de type ne limite une prestation ; sa marge
est la difference entre sa valeur TTC et son reversement calcule. Valeur TTC >= reversement.
Le retrait/archive d'une prestation utilisee par des instances en cours est
refuse ; aucun effacement ou deplacement des engagements historiques.

## 6. Dossier coffret : PRD-577, 579, 580

Champs : nom 1-200, commune autorisee, code type existant, prix en centimes
strictement positif, duree de validite de 1 a 3650 jours, promesse garantie
et contenu indicatif 0-10000 caracteres, image optionnelle. Creation BROUILLON.
Le diagnostic explique les manques, sans rendre obligatoires a la creation
toutes les donnees de mise en vente.

Edition exige une version attendue ; verifier marge et dependances avant
diminution du prix ou retrait. Le changement de commune est refuse en presence
de prestations ou achats : pas de reaffectation territoriale implicite.

L'economie reutilise les calculs Epic 28 : prix, valeur des prestations,
reversements reserves, somme des marges des prestations, ecart prix/valeur et
solde prix moins reversements. Aucun taux cible n'est configure sur le coffret.
Les chiffres sont en centimes en API et formates en euros a l'ecran. Les frais
externes non integres sont indiques ; aucune affirmation de marge nette.

Deux actions distinctes :

1. Verifier la mise en vente : simuler le statut cible ACTIVE via le meme
   diagnostic, sans sauvegarder le coffret ni modifier BUM ou les commercants.
2. Mettre en vente : verrouiller, comparer version, recharger les faits,
   verifier transition et diagnostic cible, appliquer ACTIVE dans la transaction
   puis invalider/reevaluer le suivi. Refus = aucun effet partiel.

Une simulation favorable perime des qu'une source change. La publication
n'active pas les prestations/commercants. Retirer des nouvelles ventes est une
transition explicite et auditee ; elle n'annule pas les achats existants.
La suppression physique est absente de l'atelier.

## 7. Diagnostic canonique : PRD-561 a 564, 570

Les controles sont ceux de la conception technique, completes sans arret au
premier echec. Ils possedent code stable, famille, severite, PASSED/FAILED/UNKNOWN,
applicabilite, ressource et traitement. UNKNOWN obligatoire prime sur FAILED ;
sinon echec bloquant = NON_VENDABLE, sinon VENDABLE. Les gardes desactivees ou
dependantes d'une source absente sont non applicables, jamais des succes fictifs.

La liste publique, le detail et le nouvel achat consomment le meme moteur,
avec faits courants. La projection n'autorise jamais un paiement. Les erreurs
techniques ne rendent pas une offre vendable ; les motifs internes ne sont
pas exposes aux clients. La reprise Checkout durable conserve son contrat.

La file ouvre NON_VENDABLE, pertes d'offres avant preparations, puis severite,
date recente et UUID. Filtres : commune, type, statut, verdict, famille, code,
commercant, recherche nom/UUID et anciennete. Pagination 25, maximum 100.
Une cause partagee compte une fois par ressource ; les impacts par coffret
restent accessibles. Les succes sont replies ; chaque cause ouvre l'atelier
ou la fonction specialisee autorisee.

Le detail expose date, fraicheur, dernier verdict connu, controles et reponse
Marketplace attendue. Une projection invalidee ou de plus de 20 minutes est
INDETERMINE pour le pilotage ; elle ne prouve pas une panne du public. Aucun
GET ne modifie les donnees de diagnostic ou de catalogue, hormis l'audit de lecture.

## 8. Suivi durable : PRD-565 a 567

Toute modification de source pertinente demande une reevaluation durable dans
la transaction source. Plusieurs demandes se regroupent sans perdre la derniere
revision. Un travailleur ne publie pas un resultat plus ancien que les sources.
Le batch de reconciliation couvre aussi les mutations hors application.

Le hash exclut dates, textes et ordre de lecture ; il inclut version des regles,
flags pertinents et causes codees. Meme diagnostic : date d'evaluation actualisee,
aucune nouvelle transition ni notification. Cause persistante : detectedAt
conserve. Disparition puis retour : nouvelle occurrence.

| Transition | Effet |
| --- | --- |
| Initial -> VENDABLE | Initialisation sans alerte |
| Initial -> NON_VENDABLE | Preparation visible, aucune perte inventee |
| Tout -> INDETERMINE | Alerte technique ouverte/actualisee |
| VENDABLE -> NON_VENDABLE | Episode de perte, alerte critique |
| NON_VENDABLE -> NON_VENDABLE identique | Pas de doublon |
| Causes changees dans episode | Historiser nouvelle occurrence ; debut episode conserve |
| INDETERMINE -> NON_VENDABLE | Fermer incident technique ; maintenir/ouvrir episode metier si vendable auparavant |
| Tout -> VENDABLE | Resoudre les alertes ouvertes |
| Rechute apres resolution | Nouvel episode meme si causes identiques |

Reevaluation manuelle : cle Idempotency-Key 1-128 ASCII, scope acteur/coffret,
conservation 24 h ; replay retourne resultat initial sans nouveaux effets.
Autre requete avec meme cle = conflit. Nouvelle correction = nouvelle cle.
Limite 10 nouveaux calculs/minute/acteur ; permissions recontrolees au replay.

Chronologie paginee, ancien/nouveau verdict, delta des causes, source, date,
version et correlation. Les secrets et donnees personnelles Stripe sont exclus.
Les notifications optionnelles passent par outbox avec deduplication ; leur
echec n'annule pas le diagnostic. BackOffice et Control affichent les memes
alertes autorisees ; WebPush/email ne contiennent qu'une invitation a consulter.

## 9. Synthese, territoires et mesures : PRD-568, 571, 581

Total = vendables + non vendables + indetermines au meme instant et sur le
meme perimetre. Les familles peuvent se recouper. Les nouveaux blocages sont
les pertes observees sur 24 heures ; un brouillon n'est pas une perte.
Les compteurs sont calcules avant pagination ; projections absentes incluses
dans INDETERMINE. Les communes sans coffret restent visibles.

Couverture : non publiee, sans coffret, disponible, aucune offre vendable
connue (incertitude), aucune offre vendable (certain). Le filtre type s'applique
aux compteurs et liens. Les indicateurs sont dates et le retard de batch visible.

Mesurer duree de diagnostic, age de demandes, dernier tour complet, changements
et retablissement ; jamais un label metrique par UUID. Mesurer temps de parcours
et erreurs via des evenements d'action minimises. Objectifs de reference : p95
liste <= 500 ms, detail <= 800 ms ; volume et environnement mesures dans le rapport.

## 10. Erreurs, reprise et recette de sortie : PRD-569, 582

401 session, 403 permission/CSRF, 404 ressource absente ou hors perimetre,
409 version/idempotence/dependances, 422 saisie, 429 limite, 503 incident de
source/persistance. L'API expose correlationId et message utile sans trace.

La recette doit couvrir les 22 stories, notamment creation/reprise Onboard,
modele rattache a deux coffrets, prix/refus de marge, simulation BROUILLON,
conflit avant publication, fermeture avec engagements, causes partagees,
replay concurrent, batch interrompu, scopes, CSRF, XSS et retrait des anciennes
interfaces. Tests de domaine sans ORM, use cases, PostgreSQL et TestClient.
Les dependances providers utilisent des fakes ; aucune base de production.

La migration est additive, les sources historiques restent intactes. Les
anciennes entrees de coffret/commercant sont remplacees directement ; toutes
les fonctions utiles sont reintegrees avant bascule. Aucun maintien de deux
interfaces d'edition en parallele. La recette et le rapport final distinguent
tests executes, hypotheses, limites d'environnement et actions de deploiement.


## 11. Precisions de livraison V1

La qualification fiscale explicite est reservee a ADMIN. Les autres commandes
de l'atelier restent accessibles a EXPLOITATION dans ses communes. Le module
Onboard reutilise demeure soumis a ses flags fonctionnels existants ; la
procedure de livraison indique leur activation pour le parcours complet.

Les liens historiques redirigent vers la fiche canonique ; les anciens POST
CRUD sont refuses (410). Les fonctions specialisees sont repertoriees dans
la navigation avancee ADMIN. La chronologie fiscale reste distincte de la
vendabilite. Les mesures STARTED/SAVED/ABANDONED ne contiennent aucune saisie ;
le responsable de dossier demeure un texte operationnel, pas une habilitation.

Le retrait volontaire reste trace par le statut SUSPENDU/ARCHIVE et l'audit.
Les liens vers les ateliers existants preservent leurs controles propres.
Le compte rendu distingue mesures automatisees et gains UX a confirmer en usage.

## 12. Aide au referencement - ANO-ALL-02

La creation et la fiche coffret presentent un guide des cinq etapes jusqu'a
la vente. Les conditions BUM/Stripe sont expliquees comme conditionnelles aux
gardes actives. Le diagnostic canonique reste la source du verdict et distingue
les blocages des informations. Aucun controle metier n'est remplace par l'aide.
La creation ouvre la composition du brouillon ; enregistrer ou simuler ne
publie jamais. Les champs monetaires expliquent leur unite et le prix positif
est controle dans le formulaire comme dans l'API.

## 13. Usage responsive - ANO-ERP-01

Des 320 pixels, formulaires et listes restent accessibles sans debordement de
la page. Sur telephone, le menu est repliable avec etat accessible et fermeture
par Echap ; la deconnexion reste disponible dans le menu ouvert. Les tableaux
presentent leurs lignes en fiches avec libelles de colonnes. Les actions restent
tactiles (44 pixels minimum) et les champs evitent le zoom automatique mobile.
Sur tablette et bureau, le tableau et la navigation laterale sont conserves.

## 14. Photos dans l'atelier - ANO-ERP-02

Les formulaires commercant, coffret, modele et prestation remplacent l'URI
visible par un fichier avec apercu, conservation ou retrait explicite de la
photo. Le fichier est televerse a l'enregistrement ; le resultat DAM alimente
la commande metier. Un echec d'upload empeche cette commande. Si seule la
commande metier echoue, une nouvelle tentative reutilise l'asset deja cree.
Un abandon apres upload peut laisser un media non rattache dans le DAM ;
le retrait de la photo d'une fiche ne supprime jamais le fichier partage.

`POST /internal/erp/api/images` accepte un multipart `file` et `ville_id`.
La session ADMIN/EXPLOITATION, le CSRF, la commune autorisee, les limites DAM,
le quota et le contenu raster sont controles. L'ecriture et l'audit media
utilisent la transaction ERP. La reponse fournit `id`, `uri`, `size_bytes` et
`mime_type`. Le contexte fournit `imageMaxSizeBytes` pour l'aide du composant.

## 15. Recherche et disponibilite des sources - ANO-ERP-03

La composition affiche immediatement les commercants trouves, avec pagination
par 25. La selection charge les modeles de prestations, y compris les brouillons
et archives. Chaque ligne precise disponibilite, causes et acces a la correction.
Les reponses obsoletes d'une recherche precedente ne remplacent pas la courante.
La recherche actualise aussi les choix d'un formulaire de creation ouvert sans
effacer ses saisies ni changer silencieusement son commercant selectionne.

`GET /internal/erp/api/coffrets/{cid}/candidats?commercantId=UUID` retourne tous
les modeles du commercant autorise, avec `rattachable` et `blocages` (code/message).
Une source rattachable doit etre ACTIVE, appartenir a un commercant ACTIF de
la commune du coffret, ne pas etre deja rattachee, et respecter les montants et
le budget restant. Les controles Stripe du diagnostic canonique s'appliquent
lorsque cette garde est active. Une source indisponible reste visible mais
son bouton est desactive. La commande recontrole les memes regles sous verrou.

La disponibilite de la source ne garantit pas la vendabilite du coffret :
le rattachement cree toujours une prestation BROUILLON et n'exige pas que la
qualification BUM du coffret soit deja terminee. La creation directe d'une
prestation brouillon reste possible pour preparer l'offre. Une degradation
de marge conserve son mecanisme de confirmation explicite.
