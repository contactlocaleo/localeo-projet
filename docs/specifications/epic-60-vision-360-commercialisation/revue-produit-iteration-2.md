# Epic 60 - Revue produit, iteration 2

> Historique de conception. Etat realise et decisions deleguees : [rapport V1](rapport-developpement-v1.md), [specification detaillee](specifications-fonctionnelles.md), [contrats implementes](contrats-api.md).

> Statut : revue historique ; decisions consolidees dans le [cadrage V1](cadrage-v1.md).
> La proposition de coexistence est remplacee par une bascule directe (ERP-ARB-07).
> Sources : code et documentation du depot examines le 2026-09-05.
> Les decisions acquises du registre sont preservees ; aucun nouvel arbitrage
> n'est considere valide par la demande de revue.

## 1. Orientation proposee pour Localeo

Le back-office doit aider a preparer une offre locale, la rendre achetable,
tenir les engagements envers les acheteurs puis traiter les exceptions.
Sa valeur ne se mesure pas au nombre de formulaires regroupes mais au nombre
de dossiers menes a terme et au temps de retablissement d'une offre.

La cible reste un ERP d'activite Localeo : dossier commercant, dossier coffret,
operations, finance et supervision coherents. Le chemin directeur est :

`Referencer -> Preparer l'offre -> Verifier -> Publier -> Honorer -> Suivre`.

Le parcours doit fonctionner pour un commercant sans coffret, un coffret en
preparation, une offre active et un partenaire qui quitte le dispositif.
Les fonctions financieres et operationnelles existantes restent reutilisees.

## 2. Constats qui changent la premiere analyse

| Constat verifie | Source locale | Consequence pour l'epic |
| --- | --- | --- |
| Onboard dispose deja de dossiers, diagnostic, edition du referentiel et prestations, invitations et preparation financiere | `app/application/conformite_fiscale_bum/service_onboarding_commercant.py` | Integrer ces commandes dans le dossier 360, inventorier leurs validations ; ne pas creer un second onboarding |
| Les statuts de preparation et les capacites sont deja definis dans le domaine | `app/domaine/conformite_fiscale_bum/onboarding.py` | Retirer la proposition de nouveau cycle A_COMPLETER/BLOQUE/PRET_A_ACTIVER ; reutiliser le cycle existant et afficher la qualite des donnees a part |
| Prochaine action, responsable et echeance sont deja persistes | `DossierOnboardingCommercantOrm` dans `epic50_models.py` | PRD-576 devient une integration, pas la creation d'un systeme de taches |
| Le responsable de prochaine action est un texte | Meme modele | Ne pas proposer une file « Mes dossiers » fondee sur une identite fiable avant d'avoir defini l'affectation nominative |
| Les prestations de coffret portent coffret, commercant et version | `PrestationCoffretOrm` et `PrestationCoffretVersionOrm` | Distinguer une offre preparatoire reutilisable des conditions vendues ; pas de deplacement d'une ligne utilisee vers un autre coffret |
| La rentabilite distingue marge sur prix et commission sur valeur des prestations | `ConsulterRentabiliteCoffret` | Afficher deux concepts differents, sans presenter une marge nette ou un revenu encaisse fictif |
| La validation Onboard exige actuellement checklist et toutes les capacites | `verifier_validation_onboarding` | Exposer les capacites sans assouplir cette regle implicitement ; une validation par perimetre demande un arbitrage distinct |

Il s'agit de capacites presentes dans le code, pas d'une preuve de disponibilite
sur chaque environnement ni d'une qualification de tous les chemins d'acces.

## 3. Dossier unique et aptitude par capacite

Reutiliser les statuts Onboard : BROUILLON, RDV_PLANIFIE, EN_COURS,
A_COMPLETER, PRET_A_VALIDER, VALIDE, CLOTURE, ABANDONNE. Conserver les
transitions et motifs existants. Un dossier cloture n'implique pas que ses
capacites restent acquises pour toujours : leur observation doit etre datee.

Trois informations distinctes dans la fiche : statut du commercant, etape du
dossier Onboard et capacites courantes. Les capacites existantes comprennent
PORTAIL_VISIBLE, PRESTATION_PUBLIABLE, COFFRET_PUBLIABLE, BUM_READY,
COMMISSION_BILLABLE, INVOICE_REQUEST_READY, PAYOUT_READY et PORTAL_ACCESS_READY.
Leurs libelles operateur doivent preciser la source et la portee.

`COFFRET_PUBLIABLE` dans Onboard reste un indicateur de preparation : seul le
diagnostic canonique du coffret determine sa vendabilite finale. Un partenaire
sans vente ni coffret peut etre en cours de referencement sans incident.

Une donnee inconnue ou perimee est affichee comme telle, en dehors du cycle
persistant. Ne pas convertir silencieusement un booleen historique en preuve
de controle recent. Proposer une prochaine action par controle, mais conserver
la prochaine action humaine tant qu'un operateur ne la remplace pas.

## 4. Publication : eliminer le blocage circulaire

Exiger VENDABLE sur un coffret BROUILLON avant de permettre son activation
rendrait le parcours impossible : COFFRET_NOT_ACTIVE est precisement un
blocage. Distinguer le diagnostic courant de la verification de l'etat cible.

Le bouton « Verifier la mise en vente » evalue explicitement un etat cible
ACTIVE et les seuls changements demandes, via le meme moteur de domaine.
Il presente une simulation, les controles et les ressources qui doivent encore
etre activees. Il ne sauvegarde pas et ne valide pas une qualification BUM.

Le bouton « Mettre en vente » recharge les donnees, verifie version attendue,
droits, transition et diagnostic de l'etat cible, puis applique la commande
atomiquement. En cas de conflit ou blocage, aucune activation partielle. Une
simulation favorable n'est pas un droit permanent de publier.

Activer un coffret n'active pas implicitement ses commercants ou prestations.
Les commandes de publication futures restent distinctes des sept API de
diagnostic deja concues. Leur idempotence et leur contrat sont a detailler.

## 5. Files de travail : ne pas transformer les brouillons en incidents

Conserver le defaut NON_VENDABLE de COM360-ARB-04. Ajouter un motif de file
distinct du verdict : preparation normale, perte de disponibilite observee,
incident technique, retrait volontaire. Tous les brouillons restent trouvables
mais ne doivent pas remplir la premiere page des incidents critiques.

Proposition a valider : dans la file NON_VENDABLE, prioriser les pertes sur
offres precedemment vendables, puis les dossiers de preparation selon leur
echeance. Conserver le tri severite/recence a l'interieur de chaque groupe.
Le changement du tri COM360-CON-06 sera applique seulement apres arbitrage.

Les compteurs explicitent leur population : catalogue total, offres actives,
offres perdues, preparation et donnees inconnues. Une preparation en attente
n'est pas une vente perdue. Un retrait volontaire d'une offre active reste
trace comme transition ; ne pas supprimer les alertes de COM360-ARB-06 sans
decision sur leur traitement.

Pour une politique BUM ou un compte commercant affectant plusieurs coffrets,
conserver une alerte par coffret mais regrouper visuellement les causes communes
avec le nombre de coffrets touches. Ne pas multiplier les corrections a faire.
Une erreur commune ne prouve pas a elle seule une causalite : afficher la
ressource source du controle, pas une explication generee sans preuve.

## 6. Offre, promesse et engagements vendus

La preparation d'une prestation avant choix du coffret reste une capacite cible
utile. Proposer un modele de saisie commercant sans creer au MVP un catalogue
vivant qui propagerait automatiquement ses modifications. Lors du rattachement,
creer une prestation propre au coffret avec provenance/version explicite.
La semantique de duplication et le traitement des mises a jour restent a
trancher dans ERP-ARB-02 ; aucune migration des lignes existantes par defaut.

Les descriptions publiques doivent distinguer promesse garantie et contenu
indicatif conformement a la documentation BUM du depot. Une composition
technique ne devient pas automatiquement une garantie client. Le perimetre
des gardes nouvelles NO_ACTIVE_PRESTATION et des prestations inactives doit
etre qualifie avant activation ; aucune interpretation fiscale nouvelle ici.

Avant suspension, retrait ou modification, afficher deux analyses : effet
sur les ventes futures et effet sur les achats/instances deja engages. Les
instantanes, versions et regles de fermeture existants restent les references
pour les droits des beneficiaires. Proposer une orientation vers le traitement
de fermeture/substitution/remboursement existant, jamais un bouton generique
de suppression qui efface cette obligation.

Archiver un dossier de preparation, archiver un commercant et retirer une
offre sont trois actions differentes. La cloture/abandon Onboard garde son
motif et son historique ; elle ne suspend pas silencieusement le commercant.
L'archivage metier conserve les controles de dependance et n'efface ni achats,
preuves documentaires, audit ou reversements. Les durees de retention restent
celles des politiques de donnees applicables et ne sont pas fixees par un menu.

## 7. Economie et couverture utiles a l'operateur

Afficher prix client, reversements reserves, marge theorique sur prix, marge
cible, valeur indicative des prestations et commission theorique distinguees.
Exemple de lecture du calcul actuel : prix 100, reversements 70, valeur des
prestations 120 donnent marge sur prix 30 et commission theorique 50 ; ces
deux chiffres ne s'additionnent pas comme un revenu acquis de 80.

Les frais Stripe non integres et autres couts ne sont pas supposes nuls. La
marge reelle et le cash encaisse restent issus du suivi financier existant,
avec periode et sources. Une recommandation economique ne rend pas invalide
une degradation de marge explicitement autorisee par l'Epic 28.

La couverture territoriale distingue absence d'offre, indisponibilite connue
et incertitude. A terme, la concentration sur un commercant peut suggerer une
action commerciale, sans inventer un score de risque bloquant au MVP.

## 8. MVP plus concret, sans retirer les besoins demandes

Livrer d'abord un parcours vertical complet : commercant -> offre -> coffret
-> economie -> verification cible -> mise en vente -> diagnostic et alerte.
Cette priorite ne retire ni la creation autonome d'offre cible ni la navigation
ERP ; elle evite d'attendre la refonte de toutes les rubriques pour valider la
valeur du parcours principal.

Reutiliser Onboard et les vues 360, limiter la nouvelle persistance au besoin
prouve (diagnostic, demande durable, eventualite du modele de saisie d'offre).
Pas de seconde table de dossiers, second moteur de checklist ou moteur de
workflow generique. Extraction des composants d'interface progressive.

Les six rubriques de menu restent une hypothese, a tester. La page d'accueil
doit montrer les trois prochaines actions prioritaires et leurs motifs avant
les KPI globaux. Elle ne masque pas les autres dossiers. Sans affectation
nominative fiable, l'appeler « A traiter dans mon perimetre » plutot que
pretendre afficher « Mes dossiers ». Eviter d'ajouter roles ou comptes sur la
seule base du statut termine historique de l'Epic 35 ; verifier le runtime.

## 9. Recette et mesures supplementaires

| Cas critique | Resultat attendu | Stories existantes |
| --- | --- | --- |
| Reprendre un dossier Onboard depuis 360 puis retourner dans Onboard | Meme identifiant, etape, notes et prochaine action ; aucune copie divergente | PRD-573, 575, 576 |
| Commercant sans coffret et sans vente | Preparation explicable, aucune fausse alerte d'exploitation | PRD-575, 576 |
| Coffret BROUILLON conforme pour l'etat cible | Simulation favorable possible, verdict courant non vendable preserve | PRD-563, 580 |
| Source changee entre simulation et publication | Refus ou recalcul avant effet, pas d'activation partielle | PRD-580, 582 |
| Nouvelle prestation modele rattachee a deux coffrets | Conditions independantes, pas de propagation silencieuse lors d'une edition | PRD-574, 578 |
| Catalogue avec 100 brouillons et une perte de vente recente | Perte identifiable, brouillons accessibles, compteurs de populations explicites | PRD-561, 562, 571 |
| Une source bloque dix coffrets | Dix impacts persistants, traitement source regroupe, autorisations respectees | PRD-564, 565, 581 |
| Retrait d'offre avec instances en cours | Impacts distincts, dependances controlees et orientation vers traitement des engagements | PRD-574, 578, 580 |
| Cout externe non connu et degradation de marge autorisee | Chiffres qualifies, aucun faux net ni interdiction nouvelle | PRD-579 |
| Cloturer/abandonner un dossier | Motif et historique, aucun changement implicite du statut commercant | PRD-576, 582 |

Mesurer temps median et p90 par etape, temps actif operateur distinct du delai
d'attente commercant/provider, delai de resolution d'une perte d'offre,
abandons/reprises et erreurs de publication. Relever les valeurs de depart
avant de fixer un objectif ; les temps de reponse techniques du diagnostic
restent des criteres separes des gains UX.

## 10. Arbitrages les plus urgents

ERP-ARB-08 (reutilisation Onboard), ERP-ARB-09 (publication cible),
ERP-ARB-10 (files), ERP-ARB-12 (engagements) et l'affinement ERP-ARB-02
conditionnent la conception des ateliers. La matrice de droits ERP-ARB-03 et
les regles d'aptitude ERP-ARB-04 restent ouvertes. Voir le
[registre mis a jour](registre-arbitrages.md) pour chaque proposition et son etat.
