# E77 — Parcours et règles

Lire les [décisions V1](README.md) et les
[critères canoniques](../../roadmap/en-cours/epic-77-juste-prix-local-backlog.md).
Tous les comportements ci-dessous sont des cibles à implémenter.

## Évolution du 22 novembre 2026 — Limiter les mauvaises réponses et rendre les étapes invalides visibles

Périmètre commun E77 Juste Prix et E78 Intrus des vitrines. Cette évolution
remplace l'essai unique des décisions initiales pour les nouvelles configurations ;
les définitions déjà publiées et leurs réponses terminales ne sont pas réécrites.

L'organisateur choisit **Mauvaises réponses maximum par étape**, entier **1 à 10**,
proposé à **1**, dans la création ou la configuration du brouillon. La règle est
annoncée avant inscription et figée à publication. Une bonne réponse termine le
jeu de l'étape. Une mauvaise réponse confirmée consomme un essai ; avant le maximum,
l'habitant peut répondre à nouveau. La dernière mauvaise réponse invalide l'étape.
Un scan ou un PIN ne peut plus la rattraper ; le serveur refuse cette validation.
Un passage antérieur reste une preuve, sans convertir l'échec en réussite.

**Choix utilisateur confirmé : conserver la qualification si le seuil reste
atteint.** Une étape invalide ne compte pas dans ce seuil mais n'élimine pas
automatiquement la participation. **Non qualifiable** apparaît uniquement si les
étapes encore possibles ne permettent plus d'atteindre le seuil. Exemple : seuil
3 sur 5, une étape invalide laisse 4 étapes possibles ; trois invalides rendent
le seuil impossible. Trois étapes comptabilisées et une invalide conservent la
qualification et l'unique chance au tirage.

Live affiche le solde serveur **réponses restantes**, puis un tampon **Invalide**
avec croix et texte à épuisement, distinct du tampon vide et de l'étape validée.
Le détail terminal restitue la réponse personnelle définitive et ses dates
disponibles ; les essais précédents restent masqués. Le carnet, la frise et le
détail reprennent l'impossibilité globale issue du serveur, jamais d'une page
partielle. Aucune solution avant clôture, aucun indice plus/moins sur un prix.
QR/PIN et passages des autres étapes restent disponibles selon leurs conditions.

Le domaine `animation_locale` porte budget et transitions. La configuration
`regles.nombre_mauvaises_reponses_max` est compilée en `engineConfig.maxWrongAnswers` ;
son absence historique vaut 1 et ne rouvre pas les échecs. Vitrines conserve
`ONE_CONFIRMED_ANSWER` pour l'historique et utilise `LIMITED_WRONG_ANSWERS` pour
la nouvelle règle. Le seuil et la chance unique ne changent pas.
`EtatEtapeMoteur.erreurs` reste persisté dans le JSON de l'exécution ; les lignes
de réponses définitives conservent leur unicité participant/commerce.

Les lectures personnelles exposent `mauvaisesReponses`, `reponsesRestantes`,
`etapeInvalide`, `reponseDefinitive`, `reponseAutorisee` ; le résumé global expose
`qualificationBloquee` et `etapesInvalides`. Le contrat généré précise les
enveloppes. Le client ne décrémente jamais localement et n'invente pas un état
actuel après refus ou erreur de relecture. Verrous, versions, reçus idempotents,
retour `etape`, pagination, focus, brouillons et reprises incertaines sont conservés.

| Critère de l'évolution | Preuve attendue |
| --- | --- |
| E77/E78-ESSAIS-01 | Bornes 1/3/10, refus hors bornes, gel publié, historique sans paramètre à 1 |
| E77/E78-ESSAIS-02 | Erreur puis succès, dernier essai correct, épuisement et refus ultérieur |
| E77/E78-ESSAIS-03 | Rejeu, concurrence du dernier essai, version obsolète, coupure puis reçu sans double débit |
| E77/E78-ESSAIS-04 | Passage avant/après, refus scan/PIN sur invalide, autres étapes, clôture/suspension |
| E77/E78-ESSAIS-05 | Seuil atteint malgré invalide, encore atteignable ou impossible ; carnet/détail cohérents et pagination |
| E77/E78-ESSAIS-06 | Isolation, solutions privées jusqu'à clôture, réponse finale/date, essais précédents masqués |
| E77/E78-ESSAIS-07 | 320/390/1280 px, clavier, texte 200 %, refus/erreur/reprise, navigation et brouillons |
| E77/E78-ESSAIS-08 | Contrats canoniques/embarqués, guides Animation/Commerçant et contrôles de livraison |

La [vérification E77](verification-livraison.md) consigne les preuves de ce lot.
Cette évolution ne modifie pas le statut des epics ni leurs bilans historiques.

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

### Correctif du 22 novembre 2026 — approbation et lisibilité

La fiche Animation expose les permissions effectives dans la commune active,
y compris lorsque le membre dispose du seul droit spécialisé d'approbation.
Elle ne présente pas les permissions brutes d'autres communes. Les commandes
conservent leur contrôle serveur des droits, de l'état et de la révision.

La section compare commerce, produit, description, unité/format et prix TTC.
Les repères visibles sont **À compléter**, **À examiner**, **À corriger** et
**Approuvé**. Les compteurs portent explicitement sur la page courante, limitée
à 25 propositions ; ils ne décrivent pas un total global. Les actions sont
placées sur chaque proposition à examiner. La consultation seule indique sa
raison, notamment après publication ou en l'absence de droit effectif.
L'actualisation reste locale et préserve la navigation et le focus. Un résultat
incertain appelle une vérification, sans répétition automatique de la décision.

La recette couvre deux commerces ayant accepté et proposé un produit, le droit
spécialisé seul, une autre commune, la lecture seule, l'approbation et la
correction motivée, le conflit de révision et le résultat incertain, sur mobile
et bureau au clavier. Le guide Animation et ses captures sont actualisés.
Le guide Commerçant est sans impact : proposition, correction et nouvelle
soumission restent identiques dans son application. Aucun changement de règle
métier, de forme du contrat API, de migration, de générateur de démonstration
ou de procédure d'exploitation n'est requis.

Le récapitulatif montre N commerces retenus, un produit approuvé par commerce,
les prix privés, la tolérance commune, le seuil entier 1..N, les passages, les
dates, le règlement et la dotation. Les contrôles E56/E73 restent applicables.
Les prix du magasin et les modifications ultérieures de sa fiche ne changent
jamais la référence publiée.

### Évolution du 26 novembre 2026 — commerces sans proposition soumise

**E77-CA-18a.** Dans **Produits et prix proposés**, l’organisateur voit le nombre
de commerces participants sans proposition soumise pour toute l’animation.
Parmi les commerces configurés dont l’invitation courante est acceptée, le
compteur inclut les commerces sans fiche et ceux dont la proposition est à
compléter. Les propositions à examiner, approuvées ou à corriger sont déjà
reçues. Les trois compteurs d’état restent propres à la page affichée.
**Actualiser** relit le compteur avec la liste, en conservant la partie et le
focus. Zéro est affiché lorsque le serveur le confirme.

Le backend ajoute l’entier `commercants_sans_proposition` à la réponse privée
`GET /protected/animation-locale/animations/{animation_id}/juste-prix/produits`,
sous le droit de consultation existant. Le total est indépendant du curseur,
de la taille de page et du filtre de statut. Un portail mis à jour qui reçoit
encore l’ancienne réponse affiche la liste seule. Le calcul en base s’appuie
sur les invitations courantes et les statuts existants. Les transitions de
proposition et d’approbation, les données stockées et la configuration
d’exploitation ne nécessitent aucune adaptation. Le générateur de démonstration
fournit déjà les données utilisées par le calcul.

Les tests couvrent l’absence de fiche, le brouillon, les autres statuts, les
commerces hors périmètre et la consultation sur plusieurs pages. La recette
Animation couvre le total, son actualisation, les réponses d’une ancienne API
et le rendu mobile et bureau. [Preuves de vérification](verification-livraison.md#vérification-du-compteur-e77-ca-18a-le-26-novembre-2026).

Le guide Animation explique le compteur. Le guide Commerçant continue de décrire
les gestes de préparation et d’envoi dans Pro. [Guide Animation](../../produit/formation/animation/guide-quotidien-animation.md).

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

Après un reçu d'inscription `CONFIRMEE`, Live conserve directement dans le
carnet l'accès personnel renvoyé pour cette animation. Une panne de lecture
ultérieure ne remet pas en cause l'inscription confirmée. Si le stockage local
échoue, l'écran rappelle cette confirmation et propose de réessayer uniquement
l'ajout au carnet ; le lien reçu par e-mail permet de retrouver l'accès.
L'ouverture du jeu vérifie toujours les droits et l'état courant sur le serveur.

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
