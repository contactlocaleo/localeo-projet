# Epic 60 - Analyse des parcours ERP et du referencement

> Historique de conception. Etat realise et decisions deleguees : [rapport V1](rapport-developpement-v1.md), [specification detaillee](specifications-fonctionnelles.md), [contrats implementes](contrats-api.md).

> Iteration 2 : cette analyse est completee par la [revue produit](revue-produit-iteration-2.md).
> Le dossier Onboard et ses capacites sont desormais identifies comme socle
> a reutiliser ; les decisions sont consolidees dans le [cadrage V1](cadrage-v1.md).

> Statut : analyse de reference completee par le cadrage V1, pas une conception
> technique finalisee ni une implementation.
> Date : 2026-09-05.

## 1. Lecture du besoin

Le besoin depasse la creation de nouveaux formulaires : faire du back-office
un poste de travail qui guide les operations, montre ce qui manque et permet
d'agir dans le contexte d'une fiche metier. L'orientation ERP signifie ici
gestion integree et suivi d'activite Localeo, sans etendre implicitement le
produit a une comptabilite generale ou a un CRM complet.

Trois missions doivent se lire immediatement : preparer l'offre, exploiter
l'activite et superviser le systeme. Les tables de reference restent un outil
avance, tandis que les fiches commercant et coffret deviennent les points
d'entree des actions courantes.

Le [backlog unifie Epic 60](../../roadmap/terminees/epic-60-vision-360-commercialisation-backlog.md)
porte les stories et les lots. Cette analyse distingue demande utilisateur,
propositions d'amelioration et decisions restant ouvertes.

## 2. Existant a reutiliser et ecarts

| Socle examine | Reutilisation | Ecart a traiter |
| --- | --- | --- |
| Epic 27, Vision 360 commercant | Identite, prestations, activite, documents, notes, contact et alertes | Passer de consultation/navigation a creation et edition guidees |
| Epic 28, Vision 360 coffret et assistant reversements | Composition, calcul de marge, disponible, controle de degradation | Unifier le parcours de construction dans la fiche |
| Epic 60, conception de commercialisation | Verdict canonique, causes, traitements, alertes, reevaluation | Consommer le diagnostic dans l'atelier d'edition, sans l'y reimplementer |
| Epics 1 et 3 | Statuts, dependances, versions et moderation | Exposer ces transitions clairement dans les formulaires guides |
| Epics 38, 39 et 50 | Documents, Stripe Connect, onboarding et conformite BUM | Agreger une checklist d'aptitude avec liens vers les fonctions proprietaires |
| Epic 35 et sessions internes | Roles et perimetres | Inventorier les permissions d'ecriture et verifier les destinations reelles |
| `app/infrastructure/admin/admin.py` | Vues SQLAdmin et liens existants | Categories nombreuses ; melange de tables techniques, suivi metier et actions |
| `PrestationCoffret` | Propriete commercant, version, prix et reversement | `coffret_id` obligatoire : une prestation autonome n'est pas acquise dans ce modele |

Les syntheses historiques ne remplacent pas l'inventaire des routes/use cases
lors de la conception. En particulier, afficher une checklist ne doit pas
faire croire qu'un controle ou un workflow inexistant est deja implemente.

## 3. Organisation de navigation proposee

Une barre laterale stable avec peu de rubriques ; sous chaque rubrique,
quelques destinations orientees taches. Une fiche ne doit pas etre dupliquee
par rubrique : les liens ouvrent la meme fiche, avec l'onglet utile.

| Rubrique principale | Entrees proposees | Intention |
| --- | --- | --- |
| Mon activite | A traiter, dossiers en cours, echeances, raccourcis | Savoir quoi faire maintenant |
| Commercants et catalogue | Commercants, coffrets, prestations, disponibilite du catalogue | Referencer et preparer l'offre avec des parcours guides |
| Operations | Achats et clients, validations, support, animations, communications | Traiter l'activite quotidienne |
| Finance | Reversements, paiements, rapprochements, facturation | Preparer et controler les flux financiers |
| Supervision | Alertes transverses, sante, batchs, echecs de notification, audit | Detecter, diagnostiquer et reprendre les incidents |
| Referentiels et administration | Communes, typologies, politiques, documents de reference, acces, configuration | Gerer les tables et parametres avances selon habilitation |

La gestion documentaire reste aussi accessible dans chaque dossier. L'envoi
d'une communication appartient aux operations ; les echecs techniques d'envoi
a la supervision. Les coffrets bloques restent dans la file commercialisation,
avec un raccourci depuis la supervision, sans seconde file divergente.

Les six rubriques sont validees ; leur organisation detaillee est a tester sur les
missions reelles. Ne pas deplacer toutes les tables dans six sous-menus aussi
longs que le menu actuel : montrer d'abord les parcours et placer les vues
avancees dans un niveau secondaire, avec des libelles comprehensibles.

Barre globale : recherche, contexte territorial explicite, aide et menu Creer.
Ne pas imposer un filtre annuel global aux dossiers de referencement ; les
periodes restent propres aux indicateurs d'activite et au contexte Animation.

Actions rapides recommandees : Nouveau commercant, Nouveau coffret, Reprendre
un dossier, Traiter un coffret bloque, Rechercher un achat, Preparer les
reversements. Les actions privilegiees dependent du role et des usages mesures.

## 4. Parcours commercant

### 4.1 Creation et reprise

1. **Identifier** : rechercher un commercant existant avant creation ; proposer
   les rapprochements sur nom, commune et identifiants professionnels deja
   disponibles. Un rapprochement suggere ne fusionne jamais automatiquement.
2. **Creer un brouillon** : saisir le minimum reellement requis par le domaine,
   puis sauvegarder ; ne pas imposer les pieces de publication des la creation.
3. **Completer le dossier** : coordonnees, interlocuteur, profil public,
   documents et informations contractuelles selon les regles applicables.
4. **Preparer l'offre** : creer ou editer les prestations, photos, description,
   valeur, conditions et versions ; voir les coffrets deja concernes.
5. **Verifier l'aptitude** : lire les controles, traiter les manques, verifier
   acces commercant, Stripe et conformite dans leurs ecrans proprietaires.
6. **Valider et activer** : presenter les consequences et executer une action
   explicite soumise aux droits et invariants serveur.
7. **Suivre l'activite** : retrouver ventes, validations, reversements et support
   dans la Vision 360 existante, avec les alertes et prochaines actions.

La fiche conserve un entete permanent : identite, statut metier, preparation,
responsable, prochaine action. Onglets proposes : Synthese, Referencement,
Prestations, Documents et acces, Activite, Historique. Les onglets doivent
regrouper les fonctions existantes sans perdre la communication et les notes.

### 4.2 Diagnostic d'aptitude

Le mot « sante » recouvre preparation et exploitation. Afficher ces deux
dimensions separement : un nouveau commercant sans ventes n'est pas malade,
et un commercant ACTIF peut avoir un compte Stripe devenu indisponible.

| Dimension | Ce que l'operateur doit comprendre | Nature initiale |
| --- | --- | --- |
| Identite et referencement | Champs requis, statut et coherence territoriale | Controles metier existants |
| Offre | Prestations preparees/actives, versions a valider, utilisations dans des coffrets | Preparation et eligibilite distinctes |
| Profil public | Description, medias et publication | Qualite editoriale, bloquante seulement si une regle l'exige |
| Documents et conformite | Pieces requises selon le cas, etats de verification et diagnostic applicable | Regles documentaires/BUM existantes, pas de validation juridique inventee |
| Stripe Connect | Compte lie, capacites, exigences et derniere synchronisation | Aptitude financiere selon les gardes actives |
| Acces et preparation operationnelle | Acces cree, invitation et prise en main si informations disponibles | Checklist de demarrage ; ne pas inventer une preuve de formation |
| Activite et incidents | Support, validations, reversements et notifications en anomalie | Sante operationnelle distincte de l'admission |

Recommandation revisee : reutiliser les statuts et capacites du domaine
Onboard, sans nouveau cycle persistant. BROUILLON, RDV_PLANIFIE, EN_COURS,
A_COMPLETER, PRET_A_VALIDER, VALIDE, CLOTURE et ABANDONNE restent les etapes
de dossier ; elles ne remplacent ni statut commercant ni verdict coffret.
Les informations inconnues/perimees sont des qualites de diagnostic distinctes.
Les capacites de portail, offre, facturation et reversement sont presentees
avec leurs prerequis. La validation actuelle exige toutes les capacites :
aucun assouplissement implicite par cette nouvelle interface.

Chaque controle doit avoir une source, une date, un motif et un lien/action.
Le score de completion peut guider la saisie, mais ne remplace jamais les
blocages ni les controles de domaine. La qualification fiscale d'un coffret
ne doit pas devenir un statut fiscal global du commercant.

### 4.3 Fonctions complementaires recommandees

| Proposition | Valeur attendue | Priorite proposee |
| --- | --- | --- |
| Sauvegarder et reprendre le brouillon | Eviter de recommencer lorsque des informations manquent | MVP |
| Prochaine action, responsable, echeance | Eviter les dossiers abandonnes entre deux interlocuteurs | MVP, suivi leger |
| Detection des doublons sans fusion automatique | Eviter des comptes et offres en double | MVP |
| Checklist contextualisee et liens de traitement | Expliquer ce qui manque sans naviguer entre tables | MVP |
| Apercu de la fiche publique | Verifier contenu et medias avant publication | MVP si apercu existant reutilisable |
| Resume des coffrets et achats affectes avant modification | Eviter de casser une offre ou un engagement vendu | MVP |
| Invitation/renvoi d'acces et contacter le commercant | Finaliser la preparation depuis le dossier | Reutiliser les actions existantes, envoi explicite et audite |
| Favoris et vues personnelles | Retrouver rapidement sa file de travail | Apres mesure des usages |
| Duplication d'un modele de prestation | Accelerer la saisie tout en preservant les versions | Apres arbitrage du modele d'offre |
| Relances automatiques et kanban | Pilotage avance du portefeuille | Lot ulterieur, ne pas imposer un CRM au MVP |

## 5. Parcours coffret

1. Creer ou retrouver le coffret depuis la liste ou un dossier commercant.
2. Saisir commune, type, contenu contractuel, prix, duree et medias ; enregistrer
   un brouillon sans le rendre publiquement achetable.
3. Rechercher les prestations par commercant, commune, statut et disponibilite ;
   selectionner, rattacher ou preparer une prestation dans le contexte choisi.
4. Ajuster les reversements en affichant le disponible et la marge theorique
   issus de l'Epic 28 ; distinguer les prestations exclues du calcul.
5. Afficher les controles de l'Epic 60 et leurs traitements ; verifier le
   contenu public avant de demander l'activation/publication.
6. Recontroler les donnees courantes cote serveur lors de l'action, confirmer
   les effets puis presenter le verdict final, la marge et les prochaines actions.

Onglets proposes : Synthese, Informations et presentation, Composition,
Economie, Commercialisation, Activite et historique. Entete : statut, verdict
de vendabilite, marge theorique et prochaine action. L'economie detaillee
separe marge theorique, marge cible et resultats reels ; ne pas appeler marge
nette un calcul qui ne comprend pas tous les frais.

En edition, marquer les chiffres issus de modifications non sauvegardees comme
simulation. La vendabilite canonique du coffret sauvegarde reste datee et
distincte. Une simulation ne constitue ni une qualification ni une publication.
La rentabilite positive n'annule jamais un blocage de vendabilite, et l'inverse.

## 6. Question structurante : prestation et rattachement

Dans `app/domaine/commercialisation/entities/prestation_coffret.py`,
`PrestationCoffret` porte un `coffret_id` obligatoire et un reversement propre
a ce contexte. On ne peut donc pas promettre sans evolution une bibliotheque
autonome d'offres commercants librement reutilisables.

Deux options a concevoir :

| Option | Avantage | Limite / consequence |
| --- | --- | --- |
| Creation contextuelle, coffret obligatoire | Evolution courte utilisant le modele actuel | Le referencement de l'offre ne peut pas preceder le choix d'un coffret |
| Modele de prestation commercant puis rattachement a un coffret | Preparation de l'offre independante et reutilisation controlee | Modele, versions, migration et compatibilite des usages a concevoir |

La seconde option est recommandee pour atteindre le parcours souhaite. Elle
ne signifie pas partager aveuglement une ligne mutable entre coffrets : le
rattachement doit conserver ses conditions et son reversement, avec une
version explicite. Une modification du modele ne doit pas modifier les droits
des achats existants ni les autres coffrets sans decision. Verifier d'abord
les eventuels concepts de prestation catalogue deja presents ailleurs dans
le depot avant de creer un nouvel agregat concurrent.

## 7. Principes UX et architecture

Decision V1 ERP-ARB-07 : remplacer directement les anciennes interfaces.
Le travail peut etre decoupe techniquement, sans coexistence utilisateur ;
reintegrer les fonctions utiles et actualiser tous les liens de la console.


- Meme structure d'entete, onglets, erreurs et actions dans les deux dossiers.
- Bouton principal lie a l'etape utile ; Enregistrer distinct d'Activer/Publier.
- Etapes reprenables, erreurs au niveau du champ, avertissement de sortie si
  saisie non sauvegardee, conflits d'edition signales sans ecrasement silencieux.
- Identite et commune toujours visibles ; choix territorial filtre recherche,
  compteurs et droits, sans reaffecter silencieusement une ressource.
- Afficher les consequences des actions sur les versions, coffrets et achats.
- Conserver les controles de domaine, les use cases et les transactions ; les
  formulaires guides ne doivent pas introduire un second chemin d'ecriture brut.
- Remplacer les anciennes interfaces par les nouveaux parcours lors d'une
  bascule directe ; reintegrer les fonctions avancees utiles dans la nouvelle
  console. Reutiliser templates, composants et services sans maintenir deux
  interfaces et sans imposer un nouveau framework.
- Accessibilite clavier, libelles explicites, etats sans dependance a la couleur,
  retours apres sauvegarde et usage sur petit ecran pour les actions pertinentes.
- Permissions serveur par lecture, modification, activation, finance et
  administration ; actions cachees/desactivees ne suffisent pas. Auditer les
  modifications et envois, proteger les POST et appliquer les droits territoriaux.

## 8. Articulation des volets de l'Epic 60

Les anciennes Epics 60 et 61 sont fusionnees sous l'Epic 60. Le volet
diagnostic porte disponibilite, alertes et reevaluation ; le volet ERP porte
les ateliers de creation, edition et preparation accessibles depuis les
traitements. Aucun diagnostic ni calcul financier n'est duplique.

La Vision 360 coffret de l'Epic 28 conserve son calcul de rentabilite et la
Vision 360 commercant de l'Epic 27 conserve son suivi d'activite. Leurs
enrichissements sont portes par cette epic unique. Les decisions COM360-ARB-*
et ERP-ARB-* sont reunies sans modification de leurs validations.

## 9. Arbitrages avant conception detaillee

Les propositions `ERP-ARB-01` a `ERP-ARB-15` et leurs decisions sont
centralisees dans le [registre des arbitrages](registre-arbitrages.md).
Ce registre est la reference pour les etats de validation ; les propositions
de la presente analyse ne constituent pas des decisions acquises.

## 10. Premiere evaluation et prochaines etapes

La valeur principale attendue est la reduction du temps de referencement et
des erreurs de preparation. Le risque principal est de changer simultanement
navigation, modele de prestation et regles de publication. Livrer d'abord les
parcours et integrations clairement identifies, apres arbitrage du modele
d'offre, permet de limiter ce risque.

Avant chiffrage : inventorier les menus/routes et droits actuels ; observer
trois parcours (nouveau commercant, nouveau coffret, modification d'offre
active) ; relever duree, changements d'ecran, erreurs et retours arriere.
Produire ensuite les maquettes des deux dossiers et de l'accueil, la matrice
de permissions, la conception des prestations et les contrats de commande.

Mesures proposees : temps median pour creer un brouillon puis atteindre l'etat
pret, nombre de changements d'ecran, dossiers sans prochaine action, erreurs
de publication et taux de reprise reussie. Les objectifs chiffres seront fixes
apres la mesure initiale ; aucun gain n'est affirme sans observation.

Recette minimale : creation, edition, abandon/reprise, conflit concurrent,
modification d'une prestation utilisee, composition et retrait, marge degradee,
blocage de publication, droits territoriaux, navigation historique et absence
de regression sur les achats deja engages.
