# EPIC 41 - Expression de besoin UX - Plateforme partenaire Animation locale

Document d'entree pour generer une maquette Figma Make de la plateforme partenaire dediee aux animations locales Localeo.

## Objectif de la maquette

Concevoir une application web partenaire, SaaS B2B, permettant a un organisateur ou partenaire habilite de creer, gerer, piloter et mesurer ses animations locales, sans intervention nominale de Localeo.

La maquette doit montrer une experience operationnelle, dense, claire et rassurante. Ce n'est pas une landing page marketing : le premier ecran doit etre l'application utilisable.

## Contexte produit

Localeo met a disposition des communes, partenaires locaux, associations de commercants ou offices de tourisme une plateforme permettant de lancer des animations locales autour des commercants d'une commune.

Le MVP porte le modele `Passeport commercant` :
- un participant scanne un QR d'inscription ;
- il saisit email, nom, prenom et telephone ;
- il recoit un QR participant par email ;
- il valide des etapes chez des commercants via scan du QR participant par l'application commercant ;
- s'il atteint les criteres de qualification, il devient eligible a un tirage au sort ;
- les lots a gagner sont obligatoirement des coffrets Localeo actifs de la commune de l'animation ;
- a l'envoi du gain, une instance de coffret est creee et activee automatiquement.

Localeo supervise la plateforme, mais ne cree pas les animations a la place du partenaire. Le partenaire doit etre autonome.

## Utilisateur cible principal

Gestionnaire d'animation :
- partenaire, collectivite, association de commercants ou office de tourisme ;
- peut etre habilite sur une ou plusieurs communes ;
- doit selectionner explicitement la commune active avant de creer ou gerer une animation ;
- peut creer, configurer, publier, piloter, cloturer, lancer un tirage, envoyer les gains, consulter le bilan et exporter ;
- ne peut pas administrer globalement tous les tenants, modifier les abonnements ou corriger exceptionnellement hors perimetre Localeo.

## Contraintes de contexte

- Tenant fonctionnel MVP : la commune.
- Une animation appartient a une seule commune.
- Les animations multi-communes sont hors MVP.
- L'acces a la plateforme est payant via abonnement Stripe Billing actif, rattache a un partenaire, une commune et une formule.
- Si l'abonnement expire pendant une animation publiee ou en cours, l'animation va a son terme, mais les nouvelles actions payantes peuvent etre bloquees.
- Les donnees personnelles participant ne doivent pas apparaitre dans les vues agregees.
- Les actions impossibles doivent expliquer la raison du blocage.
- Les actions sensibles demandent confirmation : publication, cloture, tirage, envoi des gains.

## Direction UX

La plateforme doit ressembler a un outil de pilotage professionnel :
- navigation laterale claire ;
- barre haute avec selection de commune active, statut d'abonnement, notifications et profil ;
- tableaux lisibles et filtrables ;
- indicateurs de performance utiles ;
- workflow visible pour comprendre rapidement ou en est chaque animation ;
- actions contextualisees selon le statut ;
- peu de decoration, priorite a la lisibilite ;
- tons sobres, usage mesure de la couleur pour statuts, alertes et actions ;
- logo Localeo visible mais discret.

Eviter :
- hero marketing ;
- illustrations decoratives non fonctionnelles ;
- cartes trop nombreuses sans hierarchie ;
- effets visuels qui nuisent a la lecture ;
- jargon technique backend.

## Navigation principale attendue

Menu lateral :
- Tableau de bord
- Animations
- Modeles
- Coffrets a gagner
- Participants
- Validations
- Tirages et gains
- Flyers
- Bilans
- Abonnement
- Support

Barre haute :
- selecteur de commune active ;
- badge statut abonnement : Actif, Acces limite, Expire, Suspendu ;
- bouton aide/support ;
- notifications ;
- menu utilisateur.

## Ecrans MVP a maquetter

### 1. Tableau de bord de performance

But : permettre au gestionnaire de mesurer l'efficacite de ses animations.

Contenu :
- filtres : periode, commune, modele, statut, animation ;
- KPI principaux : animations publiees, en cours, terminees, inscrits, participants ayant termine, taux de completion, participants qualifies, coffrets envoyes, taux de consommation ;
- graphique de progression des inscriptions et validations ;
- comparaison des animations ;
- top commercants par validations ;
- alertes de sous-performance : faible inscription, absence de validation, tirage non lance, gains non envoyes, coffrets non consommes ;
- liste courte des animations necessitant une action.

Regle importante :
- aucune donnee personnelle participant dans ce dashboard.

### 2. Liste des animations

But : retrouver rapidement les animations et comprendre leur etat.

Contenu :
- recherche ;
- filtres : statut, commune, modele, periode, alertes ;
- tableau avec colonnes : nom, commune, modele, periode, statut, workflow, inscrits, termines, validations, alertes, action suivante ;
- indicateur de workflow visible sur chaque ligne ;
- actions rapides : ouvrir, modifier, publier, cloturer, lancer tirage, voir bilan selon statut.

Etats a prevoir :
- aucune animation ;
- animation bloquee par abonnement ;
- animation avec configuration incomplete ;
- animation en cours ;
- animation terminee avec tirage a lancer.

### 3. Catalogue des modeles

But : choisir le type d'animation a creer.

Contenu :
- carte modele `Passeport commercant` ;
- description du fonctionnement ;
- prerequis : commune, commercants participants, dates, coffrets actifs de la commune, regles de qualification ;
- bouton creer une animation ;
- modeles futurs visibles comme indisponibles ou "bientot" : rallye, chasse au tresor, quiz.

### 4. Assistant de creation d'animation

But : guider le gestionnaire de bout en bout.

Etapes :
1. Choisir le modele.
2. Choisir la commune tenant active.
3. Renseigner les informations publiques : nom, description, organisateur, dates, visuel si disponible.
4. Selectionner les commercants participants.
5. Configurer les regles du passeport : seuil de validation, dates, contraintes.
6. Choisir les coffrets a gagner parmi les coffrets actifs de la commune.
7. Generer ou previsualiser le flyer PDF.
8. Recapitulatif et verification avant publication.

Contraintes UX :
- afficher un resume permanent de l'animation en cours de creation ;
- signaler les prerequis manquants ;
- empecher la publication tant que la configuration n'est pas valide ;
- expliquer clairement les blocages.

### 5. Fiche animation - Vue workflow

But : voir en quelques secondes ou se situe l'animation dans le cycle global.

Onglets de fiche :
- Workflow
- Live
- Configuration
- Participants
- Validations
- Tirage
- Gains et coffrets
- Flyer
- Bilan
- Audit

Workflow minimum :
- Brouillon
- Configuration
- Prete a publier
- Publiee
- En cours
- Cloturee
- Tirage a lancer
- Gains a envoyer
- Bilan disponible
- Archivee
- Annulee

La vue doit afficher :
- etape courante ;
- etapes terminees ;
- etapes restantes ;
- action suivante recommandee ;
- blocages actionnables ;
- actions disponibles selon les droits et l'abonnement.

### 6. Fiche animation - Vue live

But : piloter une animation en cours.

Contenu :
- statut et periode ;
- inscrits total ;
- participants ayant termine ;
- progression globale ;
- validations recentes ;
- participants qualifies ;
- alertes : absence de validations, QR en erreur, email non envoye, cloture proche ou en retard ;
- actions disponibles : modifier si autorise, cloturer, lancer tirage, exporter.

### 7. Participants et validations

But : suivre la participation sans exposer inutilement les donnees personnelles.

Contenu :
- liste des participants avec donnees masquees par defaut ;
- statut de progression ;
- nombre de validations ;
- statut qualifie/non qualifie ;
- filtres : progression, qualifie, date inscription ;
- liste des validations : date, commercant, etape, resultat, anomalie.

Contraintes :
- les informations nominatives ne sont visibles que dans les contextes autorises ;
- dans les vues agregees, utiliser des donnees anonymisees ou masquees.

### 8. Tirage et gains

But : lancer le tirage puis envoyer les coffrets aux gagnants.

Contenu :
- population eligible figee ;
- nombre de participants eligibles ;
- coffrets disponibles comme gains ;
- bouton lancer tirage, bloque si l'animation n'est pas terminee/cloturee ;
- resultats du tirage ;
- liste des gagnants ;
- action envoyer gain ;
- statut d'envoi ;
- creation automatique de la CoffretInstance ;
- notification email/push.

Regles :
- les lots sont uniquement des coffrets actifs de la commune ;
- confirmation obligatoire avant lancement du tirage et envoi des gains ;
- idempotence visible : un gain envoye ne doit pas pouvoir creer deux coffrets.

### 9. Gains et consommation des coffrets

But : mesurer si les coffrets gagnes sont utilises.

Contenu :
- liste des coffrets envoyes ;
- gagnant ;
- statut coffret ;
- date activation ;
- date expiration ;
- prestations consommees/restantes ;
- dernieres validations ;
- alertes : non consomme, proche expiration, expire, incoherent.

### 10. Flyer PDF

But : fournir un support de communication partageable.

Contenu :
- apercu du flyer ;
- nom animation ;
- commune ;
- dates ;
- organisateur ;
- texte court ;
- QR inscription public ;
- URL inscription ;
- logo et charte Localeo ;
- bouton telecharger ;
- bouton regenerer si informations modifiees ;
- statut : a jour / a regenerer.

Regles :
- le QR du flyer est le QR d'inscription public ;
- aucun QR participant ni token gestionnaire ;
- les actions de generation, telechargement et remplacement sont auditees.

### 11. Bilan et export

But : mesurer le resultat final d'une animation.

Contenu :
- participants total ;
- participants ayant termine ;
- validations ;
- qualifies ;
- taux de completion ;
- lots/coffrets envoyes ;
- consommation des coffrets ;
- statistiques par commercant ;
- export CSV.

### 12. Abonnement et acces

But : comprendre le droit d'acces a la plateforme.

Contenu :
- formule ;
- commune couverte ;
- statut abonnement ;
- dates ;
- limitations ;
- message si acces limite ;
- actions bloquees avec raison.

Etats :
- actif ;
- expire ;
- suspendu ;
- resilie ;
- acces limite pendant animation publiee ou en cours.

## Etats et messages a maquetter

Messages de blocage :
- abonnement inactif ;
- tenant commune non habilite ;
- action reservee Localeo ;
- animation non modifiable dans son statut courant ;
- coffret non eligible car hors commune ou inactif ;
- tirage impossible car population eligible non figee ;
- flyer a regenerer ;
- QR non disponible ;
- aucune donnee sur la periode filtree.

Etats transverses :
- chargement ;
- vide ;
- erreur ;
- succes ;
- acces refuse ;
- confirmation action sensible ;
- action en cours ;
- action deja realisee.

## Donnees exemple pour la maquette

Commune active :
- Ville de Valmont

Gestionnaire :
- Claire Martin
- Office de tourisme de Valmont

Animations :
- Passeport commercant - Ete 2026
- Rallye vitrines - brouillon, modele futur non actif
- Passeport gourmand - cloture, tirage a lancer

Commercants :
- Maison Lenoir
- Atelier des Saveurs
- Librairie du Centre
- Le Comptoir Local

Coffrets :
- Coffret Decouverte Valmont
- Coffret Gourmand Valmont
- Coffret Bien-etre Valmont

KPI exemple :
- 4 animations publiees
- 812 inscrits
- 486 participants ayant termine
- 60 % taux de completion
- 1 934 validations
- 214 participants qualifies
- 45 coffrets envoyes
- 38 % taux de consommation coffrets

## Prompt pret a copier dans Figma Make

```text
Creer une maquette haute fidelite d'une application web SaaS B2B appelee "Localeo - Plateforme partenaire", destinee a des collectivites, offices de tourisme et partenaires locaux qui creent et pilotent des animations locales autour des commercants d'une commune.

Ce n'est pas une landing page. Le premier ecran doit etre un dashboard applicatif utilisable.

Style attendu : interface professionnelle, sobre, claire, dense mais lisible, orientee pilotage operationnel. Utiliser une navigation laterale, une barre haute avec selecteur de commune active, badge de statut d'abonnement, notifications et profil utilisateur. Utiliser des tableaux, filtres, KPI cards, stepper workflow, alertes, modales de confirmation, onglets de fiche detail. Logo Localeo visible mais discret. Reprendre une charte Localeo generique, claire et moderne, sans hero marketing.

Contexte produit :
- le partenaire gere lui-meme ses animations ;
- Localeo supervise mais ne cree pas les animations a sa place ;
- le tenant fonctionnel est la commune ;
- le gestionnaire peut etre habilite sur plusieurs communes et doit selectionner une commune active ;
- l'acces depend d'un abonnement actif ;
- le modele MVP est le Passeport commercant ;
- les participants s'inscrivent via QR, valident des etapes chez des commercants et peuvent gagner des coffrets ;
- les lots sont uniquement des coffrets Localeo actifs de la commune ;
- les donnees personnelles participant sont masquees dans les vues agregees.

Creer les ecrans desktop suivants :
1. Tableau de bord de performance avec filtres periode/commune/modele/statut, KPI, graphiques, comparatif d'animations, top commercants et alertes de sous-performance.
2. Liste des animations avec recherche, filtres, indicateur workflow, statut, periode, participants, validations, alertes et action suivante.
3. Catalogue des modeles avec le modele Passeport commercant disponible et des modeles futurs inactifs.
4. Assistant de creation d'animation en plusieurs etapes : modele, commune, informations publiques, commercants, regles, coffrets a gagner, flyer, recapitulatif.
5. Fiche animation avec onglets Workflow, Live, Configuration, Participants, Validations, Tirage, Gains et coffrets, Flyer, Bilan, Audit.
6. Vue workflow d'une animation avec les etapes Brouillon, Configuration, Prete a publier, Publiee, En cours, Cloturee, Tirage a lancer, Gains a envoyer, Bilan disponible, Archivee/Annulee ; afficher etape courante, blocages, prochaine action et actions disponibles.
7. Vue live avec inscrits, participants ayant termine, validations recentes, progression, qualifies, alertes et actions.
8. Ecran tirage et gains : population eligible, coffrets disponibles, lancement du tirage, resultats, gagnants, envoi des gains et statut des notifications.
9. Ecran suivi de consommation des coffrets gagnes : coffret, gagnant, statut, activation, expiration, prestations consommees/restantes, alertes.
10. Ecran Flyer PDF avec apercu, QR inscription public, informations animation, statut a jour/a regenerer, telecharger, regenerer.
11. Ecran Bilan avec statistiques finales et export CSV.
12. Ecran Abonnement avec formule, statut, commune couverte, dates, limitations et actions bloquees.

Prevoir les etats UX : vide, chargement, acces refuse, abonnement inactif, action bloquee avec raison, confirmation action sensible, succes, erreur.

Utiliser des donnees exemple :
- Commune active : Ville de Valmont
- Gestionnaire : Claire Martin, Office de tourisme de Valmont
- Animation principale : Passeport commercant - Ete 2026
- Commercants : Maison Lenoir, Atelier des Saveurs, Librairie du Centre, Le Comptoir Local
- Coffrets : Coffret Decouverte Valmont, Coffret Gourmand Valmont, Coffret Bien-etre Valmont
- KPI : 4 animations publiees, 812 inscrits, 486 participants ayant termine, 60 % completion, 1 934 validations, 214 qualifies, 45 coffrets envoyes, 38 % consommation coffrets.

Priorites de design :
- comprendre rapidement ou en est chaque animation ;
- distinguer live, workflow, bilan et dashboard de performance ;
- rendre les blocages actionnables ;
- ne jamais exposer de donnees personnelles dans les vues agregees ;
- montrer clairement que le partenaire est autonome.
```

## Critere de relecture de la maquette

La maquette est satisfaisante si :
- le gestionnaire comprend en moins de 10 secondes ou creer une animation ;
- le tenant commune actif est toujours visible ;
- l'etat d'abonnement est visible ;
- la liste des animations permet de voir le workflow et l'action suivante ;
- le dashboard de performance n'affiche aucune donnee personnelle ;
- la fiche animation separe clairement workflow, live, tirage, gains, flyer et bilan ;
- les actions sensibles sont confirmees ;
- les blocages sont expliques ;
- le flyer montre clairement le QR d'inscription public.
