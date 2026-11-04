# E75 — Parcours et règles

[Spécification et décisions](README.md). Les arbitrages V1 sont validés par le
porteur produit le 4 novembre 2026. Les détails techniques ci-dessous les déclinent.

## Organisateur : un parcours guidé jusqu’à la publication

Une seule étape et une action principale sont mises en avant. Les étapes
terminées restent consultables et portent une coche avec un libellé accessible.
Les erreurs désignent l’élément à corriger et ouvrent sa section. Les tâches de
gestion, historiques techniques et exports ne concurrencent pas l’action attendue.

| Étape | Acteur, préconditions et action | Résultat ou refus observable |
| --- | --- | --- |
| 1. Vérifier mon module | Acheteur habilité sur la commune ; consulter offre, durée, prix, quota et droits acquis | Aucun droit créé par un paiement en attente. Module distinct ; crédit chasse ou quota standard non utilisé. Les actions d’achat restent fermées sans offre approuvée |
| 2. Préparer ma demande | Gestionnaire autorisé ; dates, thème, public, difficulté, contexte local, commerces souhaités et dotation | Enregistrement en brouillon ; résumé compact et éléments manquants localisés. Commerce hors périmètre, liste trop grande ou dates incohérentes refusés côté serveur |
| 3. Envoyer à Localeo | Demande complète selon le contrôle serveur ; envoi explicite | Même commande répétée = même demande. État et prochaine action visibles ; pas de crédit consommé à chaque tentative technique. Le délai n’est annoncé qu’avec un calendrier et une offre définis |
| 4. Vérifier ma grille | Localeo livre une proposition contrôlée ; organisateur consulte la version, les définitions et les affectations | Aperçu graphique et liste accessible ; accepter ou demander une correction motivée. Une version remplacée invalide l’approbation ; aucun ancien accord réutilisé |
| 5. Préparer les commerces | Accords et périmètres valides ; répartir les définitions, produire les fiches, confirmer les préparatifs | Visualiser les commerces requis et les accords manquants. Une fiche joueur ne contient pas de solution. La confirmation de préparation porte sur la révision exacte |
| 6. Publier | Version approuvée, règle de dotation satisfaite, droits/quota disponibles, dates et accords valides | Précontrôle puis confirmation récapitulant la consommation. Publication et débit uniques dans la même transaction. Retour « Animation publiée » avec lien Live et QR ; une erreur ne ressemble jamais à un succès |

Les états de préparation sont indépendants du statut de l’animation : une
proposition prête ne publie pas automatiquement. La suppression d’un commerce,
le changement d’une définition, d’une case ou d’une réponse après revue impose
une nouvelle vérification et une nouvelle approbation. Les ajustements non liés
au jeu suivent leurs règles existantes ; leur innocuité doit être démontrée.

## Localeo : produire et contrôler sans perdre les corrections

Le circuit retenu réutilise la préparation manuelle assistée : brief
→ prompt exporté → attente de réponse externe → import candidat → contrôles
déterministes → revue Localeo → proposition à l’organisateur. L’outil IA ne reçoit
ni contacts privés, ni identité des participants, ni secrets d’accès. Les contenus
externes restent des données ; aucune instruction intégrée au texte importé
ne peut déclencher une commande ou changer les permissions.

Chaque candidat garde un identifiant, l’empreinte du brief, la version de schéma,
sa provenance et le résultat des contrôles. Remplacer le candidat retenu est une
action explicite et versionnée. Un import invalide ou une nouvelle génération
n’efface ni le candidat précédent ni ses modifications humaines. Une préparation
prête ou une demande de complément utilise le suivi et l’outbox système E73 ;
elle n’active pas le module Communication participants.

Le contrôle de grille vérifie : dimensions et nombre de mots bornés, identifiants
uniques, coordonnées valides, direction horizontale/verticale, longueur normalisée,
cases noires, absence de chevauchement parallèle, croisements concordants,
numérotation stable par ordre des cases de départ, définition non vide, absence
de case blanche orpheline et connectivité du graphe des mots. Toute séquence
horizontale/verticale d’au moins deux cases blanches doit correspondre à une
entrée déclarée : pas de mot accidentel créé par deux voisins. La cohérence
géométrique ne prouve ni exactitude d’une définition ni adaptation au public :
Localeo puis l’organisateur les relisent.

La V1 fixe une solution canonique par mot. Les synonymes ne
sont pas automatiquement acceptés : ils peuvent contredire les croisements.
Les termes souhaités du brief sont des demandes, pas une garantie de placement ;
la proposition indique ceux qui n’ont pas été retenus et pourquoi.

## Habitant : jouer depuis Live

1. Un QR ou lien ouvre `/live/animations/{id}` sur le domaine Live de
   l’environnement. La fiche publique montre le thème, les dates, les lots et
   les commerces, puis une action principale « Commencer ma grille » ou
   « Reprendre ma grille ». Elle explique les deux conditions du tirage.
2. Le parcours d’inscription reprend celui de la chasse : identité, règlement
   versionné, déclaration d’un adulte et mécanismes d’accès personnel existants.
   Si une récupération d’accès est nécessaire, revenir à cette animation ; ne
   pas créer une seconde participation. Consentement de communication facultatif
   et installation PWA ne conditionnent pas le jeu.
3. La grille affiche les numéros et longueurs. Chaque mot indique où trouver sa
   définition ; les définitions sont sur les supports commerçants retenus en
   ARB-01, pas librement révélées par une API contournant le parcours physique.
   Le mode « Saisir par mot » permet de jouer sans manipuler une petite grille.
   Les supports offrent une lecture accessible sur place (mise en page lisible,
   document structuré et aide du commerçant). Leur diffusion numérique dans Live
   n’est pas ajoutée à cette V1.
4. Le joueur saisit ses réponses et retrouve sa dernière sauvegarde confirmée.
   Deux indicateurs distincts montrent « Grille remplie » et « Commerces visités ».
   Remplie ne signifie pas correcte ; un compteur de lettres ne vaut pas
   qualification. Les corrections restent possibles tant que l’animation est
   ouverte et que la grille n’a pas été validée correcte.
5. Chez le commerçant, scan dans Pro ou mécanisme PIN E70 autorisé sur le téléphone
   du participant. Le serveur vérifie l’acteur, le périmètre Animation, l’étape,
   les dates et les droits salariés. Un QR public localise une étape ; il ne
   constitue jamais sa preuve de passage.
6. « Vérifier ma grille » évalue la version sauvegardée côté serveur. En cas
   d’erreur, le message distingue grille incomplète, grille à corriger et passages
   manquants, sans donner de lettre correcte. Si toutes les conditions sont
   réunies, « Tu participes au tirage » apparaît avec sa date lorsqu’elle est connue.
   Aucune promesse de lot gagné avant le résultat réel.
7. La participation reste dans « Mes participations » ; les gains rejoignent
   « Mes lots » via les circuits E73. Les notifications système existantes annoncent
   les résultats. Aucune campagne supplémentaire n’est déduite de l’inscription.

La consultation et les droits réels restent séparés : connaître l’UUID d’une
animation ne donne accès ni aux réponses personnelles ni à un ticket de tirage.
Le navigateur ne reçoit pas de table de solutions, de hash de chaque mot facile
à deviner, ni de réponse brute du fournisseur IA.

## Sauvegarde, évaluation et états limites

La normalisation est identique au contrôle de préparation et au jeu :
trim, conversion `œ/Œ → OE` et `æ/Æ → AE`, décomposition Unicode, retrait des diacritiques, majuscules,
retrait des espaces et traits d’union ; le résultat doit être `[A-Z]+`.
L’apostrophe ou tout autre caractère restant est refusé avec une aide explicite,
pas supprimé silencieusement. Le brief évite ces réponses en V1. Exemple :
`Saint-Émilion` devient `SAINTEMILION`. Les longueurs et croisements portent sur
cette représentation ; le libellé humain original est conservé côté préparation.
`cœur`, `CŒUR` et `coeur` donnent tous `COEUR` ; `æ` et `Æ` donnent `AE`.
Ces équivalences sont identiques à l’import, dans la saisie par mot et au contrôle
serveur ; une ligature occupe deux cellules après normalisation.

Le client propose une saisie cohérente entre cases croisées. Une commande par mot
ne peut pas écraser silencieusement une réponse croisée : le client annonce les
cases modifiées et soumet la grille résultante avec sa révision attendue.

| Situation | Comportement cible |
| --- | --- |
| Réseau coupé avant accusé | Saisie locale marquée « À enregistrer » ; ne pas annoncer une qualification hors ligne |
| Réponse perdue après commit | Même clé/reçu retrouve le résultat ; pas de nouvelle chance ni nouvelle validation |
| Réponse perdue puis fermeture ou retrait | Le reçu déjà enregistré reste consultable sous les droits courants, sans mutation ; il atteste un résultat passé. Une nouvelle commande est refusée et l’écran affiche aussi l’état courant du jeu |
| Deux onglets/appareils | Révision attendue obligatoire ; conflit explicite, recharger la version serveur et conserver le brouillon local pour comparaison, jamais écrasement au dernier arrivant |
| Grille correcte, dernier passage ensuite | Le domaine recalcule la qualification après le passage avec la preuve de grille correcte ; pas besoin d’un second clic de contrôle pour obtenir sa chance |
| Dernier passage, grille correcte ensuite | Même règle, une seule qualification malgré les commandes concurrentes |
| Modification après succès de grille | Refus serveur GRILLE_DEJA_VALIDEE ; la grille reste consultable et les passages manquants peuvent encore être attestés. Aucun retour involontaire à une grille incorrecte |
| Date limite atteinte | Horloge serveur faisant autorité ; refus d’une nouvelle sauvegarde ou attestation même préparée hors ligne auparavant ; lecture de l’historique conservée |
| Clôture concurrente | Les commandes sont ordonnées avec la clôture ; seule une qualification acquise avant la fermeture figure dans la population figée |
| Animation annulée | Pas de nouvelle chance, pas de tirage ; historique et motif accessibles conformément aux droits |
| Erreur dans une grille publiée | Aucun remplacement silencieux ; signalement et traitement explicite selon ARB-07, sans modification arbitraire des gagnants |

## Principes d’interface communs

Mobile d’abord : fonctionnement à 320 px et zoom 200 %, cibles tactiles d’au moins
44 px, pas de page débordant horizontalement. Une grande grille peut disposer
d’un zoom local accompagné du mode par mot entièrement utilisable au clavier et
au lecteur d’écran. Focus visible, direction annoncée, numéros/longueurs associés
aux champs, erreurs proches des champs et état de sauvegarde annoncé sans bruit
à chaque lettre. La lecture des supports imprimés et leur équivalent accessible
doivent être prévus dans la validation terrain.

Progression visuelle, pictogrammes nommés et célébration courte du succès ; pas de
couleur seule, de compte à rebours inventé, de lot illustré par défaut ou d’animation
obligatoire. Respecter la réduction des mouvements. Retour et actualisation dans
le header suivent les composants Live existants. Animation et Pro conservent leur
charte de gestion, avec une action principale et les actions secondaires regroupées.
