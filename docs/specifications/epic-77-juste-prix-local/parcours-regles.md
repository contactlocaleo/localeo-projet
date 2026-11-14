# E77 — Parcours et règles

Lire les [décisions V1](README.md) et les
[critères canoniques](../../roadmap/en-cours/epic-77-juste-prix-local-backlog.md).
Tous les comportements ci-dessous sont des cibles à implémenter.

## Préparer et approuver — CA-01 à 05

L'organisateur habilité choisit « Le Juste Prix Local » dans le catalogue standard.
Le type technique cible est `JUSTE_PRIX_LOCAL`, contrat `1.0`. La souscription,
les droits et le quota standard de publication E73 sont contrôlés par le serveur ;
aucun module payant supplémentaire n'est exigé. L'animation reste un brouillon
tant que les prérequis de publication ne sont pas tous satisfaits.

L'assistant conserve ses rubriques communes : identité/dates/règlement, commerces,
produits, règles, dotation, récapitulatif/publication. Il affiche une prochaine
action issue des contrôles serveur. Choisir explicitement seuil, tolérance et
passage requis ou non ; ne pas publier sur des valeurs implicites.

Le commerçant principal ayant accepté la participation E56 propose **son** produit :
nom, description, unité/format et prix TTC en euros, avec visuel DAM facultatif.
Les salariés de validation ne peuvent ni préparer ni modifier ce contenu. Un
accord commerçant ne vaut pas approbation du produit. Une proposition incomplète
peut être enregistrée comme brouillon, mais ne peut être proposée ni validée.

| État produit | Action autorisée | Résultat |
| --- | --- | --- |
| À compléter | Commerçant enregistre puis propose un contenu complet | Proposé avec révision |
| Proposé | Organisateur approuve la révision lue | Validé pour cette seule révision |
| Proposé | Organisateur demande une correction motivée | À corriger, commentaire visible au commerce |
| À corriger | Commerçant corrige et repropose | Proposé avec nouvelle révision |
| Proposé ou Validé, avant publication | Commerçant modifie sa proposition | À compléter, approbation invalidée ; reproposition explicite |
| Validé | Publication de l'animation | Copie immuable dans la version jouée |
| Tout état après publication | Tentative d'édition du produit joué | Refus ; procédure d'incident |

L'organisateur approuve ou refuse, sans modifier le prix à la place du commerce.
Dans « Produits et prix proposés », chaque proposition présente directement
« Accepter la proposition » et « Demander une correction ». La seconde action
ouvre une fenêtre avec choix du motif (nom/description, unité/format, prix TTC,
visuel ou autre) et précisions facultatives ; « Autre motif » exige un texte.
Annuler ou fermer la fenêtre n’envoie aucune décision. Le motif lisible est
transmis au commerçant par le contrat existant, avec la révision affichée.
Deux onglets concurrents produisent un conflit de révision, jamais l'approbation
d'une version non consultée. La publication reverrouille et revérifie les révisions.
Un commerce non prêt doit être complété ou exclu explicitement du brouillon ;
pas d'exclusion silencieuse. Après exclusion, revérifier le seuil et les accords.

Le récapitulatif montre N commerces retenus, un produit approuvé par commerce,
les prix privés, la tolérance commune, le seuil entier 1..N, les passages, les
dates, le règlement et la dotation. Les contrôles E56/E73 restent applicables.
Les prix du magasin et les modifications ultérieures de sa fiche ne changent
jamais la référence publiée.

## Participer dans Live — CA-06 à 10 et 14

La fiche publique annonce avant inscription : produit à deviner, seuil,
tolérance commune, passage requis ou non, période et dotation. Elle ne contient
pas les prix de référence. Le QR public d'animation ou de commerce ouvre Live,
avec retour vers l'animation et son annuaire ; il ne donne aucun accès personnel
et ne prouve pas un passage. Les URL et paramètres ne contiennent jamais de prix.

Réutiliser l'identité, les coordonnées obligatoires (nom, prénom, e-mail,
téléphone), le règlement, la déclaration d'adulte et la récupération d'accès du
socle Live/Passeport. L'inscription crée la participation, sans qualifier le joueur.
Un lien personnel valide reste nécessaire pour lire ses réponses et commander.
Ne pas confondre installation, favori, inscription, qualification et gain.

Le carnet mène à la liste paginée des commerces. La fiche produit montre le
contenu approuvé, son visuel réel s'il existe et « Votre estimation en euros ».
Sans visuel, utiliser une composition typographique et un pictogramme générique.
Pas d'image de produit inventée. La saisie accepte virgule ou point et au plus
deux décimales ; elle refuse négatifs, exposants et précision excédentaire sans
arrondi silencieux. Clavier décimal sur mobile ; une estimation de 0 € est valide.
Bornes techniques : voir [architecture](architecture-contrats.md).

« Vérifier mon estimation » ouvre le récapitulatif produit/commerce/montant,
avec « Modifier » et « Confirmer définitivement ». La confirmation explique
l'unique réponse. Annuler n'envoie rien ; modifier avant confirmation reste libre.
La soumission serveur pendant `[début, fin[` en statut jouable enregistre
définitivement l'estimation, correcte **ou incorrecte**, et retourne le résultat.
Avant début, pendant suspension ou après fermeture : refus sans réponse créée.
Un formulaire ouvert avant la fin ne prolonge pas le droit de jouer.

Une mauvaise réponse affiche « Prix non trouvé — réponse définitive enregistrée » ;
aucun bouton Réessayer, indice plus/moins ou correction de la saisie. Une bonne
réponse affiche « Prix trouvé » puis la prochaine action autorisée. Une panne
affiche « Vérification de l'enregistrement nécessaire » : lire le reçu puis la
participation ; ne pas annoncer un échec ni créer une autre clé automatiquement.
Après résultat inconnu, un renvoi explicite garde exactement la commande initiale.

Le serveur garde la réponse, le résultat et les faits de progression. Recharger
ou récupérer son carnet sur un autre appareil retrouve la même participation.
Une saisie non confirmée n'est pas une réponse définitive ; aucune promesse de
conservation entre appareils. Un stockage navigateur indisponible n'empêche ni
l'ouverture par lien personnel ni une participation serveur confirmée.

## Réussite, passages et qualification — CA-09 à 13

Pour une estimation E, une référence P et une tolérance commune T exprimées en
centimes entiers : **correcte si `abs(E - P) <= T`**. T=0 exige l'égalité.
Exemple : P=1250, T=50 ; 1200 et 1300 réussissent, 1199 et 1301 échouent.
Le client ne reçoit pas P avant la révélation autorisée.

| Bonne réponse définitive | Passage confirmé du même commerce | Sans passages requis | Avec passages requis |
| --- | --- | --- | --- |
| Non / pas de réponse | Non ou Oui | Ne compte pas | Ne compte pas |
| Oui | Non | Compte | Prix trouvé, passage à valider |
| Oui | Oui | Compte une fois | Compte une fois |

Si requis, le passage peut précéder ou suivre la réponse, avant fermeture. Pro
réutilise scan authentifié et validation PIN E70 sur téléphone habitant ; salarié
seulement si E72 l'habilite effectivement. Le contrôle porte sur la participation,
la version, l'étape et le commerce courant. Un QR public, une validation pour une
autre animation ou une attestation d'achat étrangère ne vaut pas passage.
Une preuve E77 doit être confirmée pendant la période jouable de cette édition,
après sa publication, avec sa configuration et son commerce retenu. Aucune
validation tardive par PIN ou Pro n'est autorisée après la fin. La révocation
d'un salarié/PIN interdit ses actions futures, sans effacer ses passages déjà
confirmés. E77 n'ajoute pas de commande de retrait individuel d'une preuve ni
de disqualification rétroactive ; un incident suit la procédure ci-dessous.
Un mauvais prix reste définitif malgré une visite. Sans passages requis, ne pas
présenter de validation E77 comme nécessaire ni proposer une commande de passage
E77 inutile ; aucune mutation des règles des autres moteurs.

X est le nombre de commerces distincts qui comptent. À X >= seuil, qualification
serveur et une seule chance ; X au-delà du seuil n'ajoute pas de chance. La
progression affiche X/seuil et peut mentionner N commerces disponibles ; ne pas
remplacer le seuil par N. « Toutes vos réponses sont enregistrées » ne signifie
pas nécessairement « Qualifié ». Si le seuil est devenu impossible pour ce joueur,
conserver les réponses et expliquer l'état, sans nouvel essai ni baisse du seuil.

## Clôturer, révéler et tirer — CA-15 à 17

À la fin de période, aucune nouvelle estimation ou visite n'est acceptée, même
si le batch de clôture n'a pas encore tourné. La clôture métier réussie fige
l'audience qualifiée ; la date dépassée seule ne publie pas le corrigé. Les prix
exacts deviennent consultables **aux participants autorisés**, par produit dans
Live pour tous les commerces de l'édition, qu'ils aient reçu une estimation ou
non, après clôture confirmée. Pas de catalogue public de prix ni d'envoi dans
les supports, et pas de révélation pendant une suspension ou une annulation.
Un tirage en attente n'empêche pas cette consultation après clôture.

Réutiliser le tirage existant, la déduplication d'audience et les règles de lots.
Le tirage vérifie une photographie cohérente de qualification E77 et refuse
une population en reconstruction. Les reprises ne créent pas un second tirage.
Mon carnet affiche le résultat personnel, Mes lots le lot et son retrait, avec
les droits de remise/consommation habituels. Aucun gain n'est attribué lors de
l'estimation ou du franchissement du seuil.

Produit indisponible, prix erroné ou commerce retiré après publication : incident
motivé et suspension si nécessaire. Les réponses, preuves et versions sont
conservées. Le diagnostic permet une reprise **identique**, ou une annulation
puis un brouillon de nouvelle édition corrigée. Aucun prix, tolérance, seuil,
mode de passage ou ensemble de commerces joué n'est révisé ; aucune neutralisation
de commerce héritée de la chasse. Pas de transfert automatique des chances,
réponses ou accords vers l'édition suivante. Les échéances communes restent
appliquées ; la reprise ne rouvre pas une période terminée. Ni crédit, remboursement,
notification commerciale ni prolongation automatique ne découle de cet incident.

## Suivre et superviser — CA-18 à 19

L'organisateur voit ses propositions privées et leurs révisions, puis des
indicateurs agrégés/datés : réponses, prix trouvés, passages manquants, qualifiés,
tirages et lots remis. Les lignes de participation exposent statut, progression
et accès au dossier autorisé ; le montant estimé nominatif n'est pas nécessaire
au pilotage et n'est exposé dans aucun bilan ni export organisateur E77.
Le commerçant ne voit que sa
proposition et les validations permises, jamais le carnet ni les réponses des
autres. L'ERP applique ses profils existants, sans accorder à Lecteur un droit
de mutation ; les commandes sensibles de support restent aux droits existants
qui les autorisent. Chaque refus serveur prime sur une action encore visible.

Le parcours ERP reste dans Animation : liste/file de préparation → dossier →
section ou action explicite → retour à la liste. Tableau comparatif paginé pour
les propositions, fiche lisible avant édition, identité/commune/état visibles,
approbation sur version et motif pour refus/incident. Préserver filtres, curseurs,
focus et saisies ; une arrivée directe fournit un parent structurel autorisé.
Pas d'édition des tables techniques pour contourner les commandes métier.

| Règles UX | Application et recette future |
| --- | --- |
| ERP-UX-01 à 04 | File/dossier/action séparés, cible et portée explicites, pagination navigable et indicateurs reliés à la même population |
| ERP-UX-05 à 08 | Consultation avant édition, Enregistrer/Annuler, euros et heures de Paris, confirmation avec version, retour et protection des saisies |
| ERP-UX-09 à 12 | Vide/inconnu/erreur/conflit distincts, contrôles locaux, composants communs, lectures bornées, checklist bureau/mobile et documentation |
| LIVE-UX-01 à 06 | Mon carnet/Mes lots/Découvrir, prix trouvé et passage distincts, compteur confirmé, aucune récompense simulée ; animation brève seulement sur nouveau reçu |
| LIVE-UX-07 à 10 | 320/390 px, cibles 44 px, clavier/focus/texte 200 %, mouvement réduit, retour au carnet et annuaire, chargement stable et pictogrammes libellés |

Les [conventions ERP](../../architecture/transverse/conventions-backoffice.md#ux-des-pages-de-gestion-erp)
et [principes Live](../../produit/live/principes-ux.md) s'appliquent sans dérogation.
La recette couvre aussi attente réseau, réponse tardive d'un autre participant,
expiration, changement de commune et carnet rempli avec coffret et lot disponible.
