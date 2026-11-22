# E78 — Parcours et règles

Spécification du 15 novembre 2026. Lire les
[décisions et la portée](README.md) et les
[critères canoniques](../../roadmap/en-cours/epic-78-jeu-des-vitrines-backlog.md).
Les sept arbitrages sont résolus par les réponses utilisateur du même jour,
consignées dans le backlog. Les comportements ci-dessous sont les cibles à réaliser.

## Évolution du 17 novembre 2026 — préparation guidée

**E78-EVO-PREPARATION-UX** étend les parcours existants, sans remplacer les
seize critères historiques ni les décisions E78-DEC-03 à 07. La préparation
était présentée comme un formulaire dans la fiche/invitation Pro et une liste
peu hiérarchisée dans Animation. La cible rend explicites la tâche, son acteur
et les attentes entre proposition, approbation, installation et contrôle.

Applications : **Pro**, **Animation** et **Projet**. Pro réutilise aussi les kits
E55/E56 et le produit E77 dans sa nouvelle section ; leurs règles restent celles
de leurs spécifications. Le domaine backend E78 reste propriétaire des révisions,
droits, approbations, installations, contrôles et barrières de publication.

| Critère ajouté | Résultat observable et comportements préservés |
| --- | --- |
| PU-01 | Le compte principal accède à « Préparation des animations » depuis la navigation Pro et à « Préparation » dans l’espace Animation. « En cours et à venir » présente par défaut les demandes courantes acceptées, y compris avant publication avec le repère « À préparer » ; « Historique » rassemble les animations clôturées, terminées, archivées ou annulées. Chaque ligne expose état de préparation, prochaine tâche et acteur depuis une lecture serveur groupée. Le filtre s’applique avant pagination et total ; une date de fin dépassée ne clôture pas une animation. Filtre et page sont conservés dans l’URL, position et focus restaurés au retour. |
| PU-02 | Le parcours dédié rappelle animation, état courant, commune, dates et mission, puis prochaine action et étapes. Une invitation jamais acceptée conserve son parcours de décision, sans accès au contenu de préparation. Les salariés ne gagnent aucun droit de contenu. Une actualisation conserve navigation, formulaire, filtre et focus ; refus, conflit et lecture incertaine ne confirment aucun avancement. |
| PU-03 | Pour une vitrine, quatre étapes numérotées guident le commerçant : prévoir l’intrus et sa mise en place ; préparer emplacement, consigne et QCM ; relire puis enregistrer/proposer ; installer puis faire contrôler. Une étape est affichée à la fois ; les liens permettent de consulter librement les autres étapes. L’étape métier à traiter ou en attente est distinguée de l’étape consultée. Les changements d’étape déplacent le focus sans enregistrer ni perdre la saisie ou les commandes incertaines. Les accès historiques conservent leurs droits propres. |
| PU-04 | La revue distingue la future présentation publique des informations privées, notamment la bonne réponse. Brouillon incomplet autorisé, envoi explicite de la version enregistrée, commentaire de correction et invalidation après modification sont conservés. La prochaine tâche et son acteur distinguent contenu approuvé, installation attestée et contrôle de cette version ; « Prête » provient exclusivement de `materiel.pret`. |
| PU-05 | Les autres animations proposent trois étapes guidées mission → produit/supports → finalisation, avec les composants E55/E56/E77 existants. Produit approuvé, support disponible et préparation déclarée restent des faits distincts ; ni la consultation ni le téléchargement ne cochent une préparation. Sans suivi, « Suivi de préparation non activé » est explicite. Téléchargement de kit, déclaration « Je suis prêt » et proposition de produit gardent leurs droits et commandes, y compris leurs refus après échéance. Aucun nouveau moteur ou suivi obligatoire. |
| PU-06 | Dans Animation, la page distingue « À traiter par l’organisation », « En attente des commerçants » et « Prêtes ». Chaque commerce affiche la prochaine tâche et son acteur, les trois états contenu/installation/contrôle et le commentaire de correction éventuel. « Prête » provient exclusivement du fait serveur `materiel.pret`. |
| PU-07 | Le contenu privé est consultable à la demande et dans la confirmation d’approbation/contrôle. Les actions restent contraintes par les habilitations et `allowedActions`. Confirmation terrain, motif de correction, révisions, reçus, conflit et absence de rejeu automatique restent inchangés. Les compteurs sont explicitement limités aux 25 éléments au maximum de la page. |
| PU-08 | Parcours clavier et rendus 320/390/1280 px vérifiés, dont texte agrandi côté Animation. Chargement, erreur/reprise, refus, lecture seule et contexte obsolète ne deviennent jamais un état prêt. Les anciens liens et la mémoire privée limitée à la session restent fonctionnels. |

### Impacts et preuves de cette évolution

| Critères | Propriétaire et preuve prévue | Documentation / contrat | Démonstration / exploitation |
| --- | --- | --- | --- |
| PU-01/02/05 | Navigation/session Pro et pages de préparation ; tests composants/navigation et recette navigateur synthétique | Présent document, espace commerçant, guide commerçant et README Pro ; URLs internes ajoutées, transport/API inchangés | Fixtures de recette UI adaptées ; générateur sans impact : aucun champ, modèle ou droit nouveau. Livraison du frontend Pro seul compatible avec le backend E78 existant. |
| PU-03/04 | Présentation Pro ; tests VitrinePreparation, guards et recette E78 | Règles E78 conservées, revue privée/public explicitée | Aucune migration/configuration ; reprise des commandes par les reçus existants. |
| PU-06/07/08 | Présentation Animation ; recette `tests/browser/e78-vitrines.mjs`, types, lint, tests et build isolé | README Animation et présent document ; contrat embarqué conservé, aucune projection ajoutée | Regroupement local des seuls éléments lus : pas de GET par commerce ni collecte de pages. Pas de nouveau coût serveur, pagination 25 préservée ; pas de nouvelle qualification de capacité. |

Les bases Git avant travaux sont Projet `e45f001`, Pro `24b1deb`, Animation
`3ba1776` et backend `c44770f1` ; arbres initialement propres. Backend, ERP,
Marketplace/Live, migrations et exports OpenAPI ne sont pas modifiés : cette
évolution présente des faits et commandes existants. Les résultats exécutés et
limites sont consignés dans le [bilan de réalisation](bilan-realisation.md).
La réserve de capacité/activation E78 demeure indépendante.

### Correctif du 22 novembre 2026 — suivi des préparations Commerçant

Les critères PU-01 à PU-05 ci-dessus remplacent la cible initiale de liste
filtrée sur les invitations déjà chargées et de simples repères pour les autres
jeux. Le bilan du 17 novembre ci-dessus reste historique : ce correctif touche
désormais **Backend, Commerçant et Projet**.

Les lectures dédiées de préparation composent les faits des domaines existants,
avec les droits du compte principal : sélection des demandes courantes acceptées
(ou acceptées avant une annulation de l’animation),
filtre de cycle de vie avant pagination, métadonnées actuelles et résumé commun
liste/détail. Les instantanés présentés lors des invitations sont conservés.
Les propositions et supports sont lus en lot, sans GET de détail par ligne ni
contenu privé dans la liste. Les contrats canoniques et embarqués sont actualisés.

Le guidage distingue état métier et étape consultée, sans créer de preuve de
lecture, de téléchargement ou d’installation. Aucun changement des règles de
validation, de configuration ou de persistance ; aucune migration. Les fixtures
de recette changent, mais le générateur de démonstration conserve ses données
et commandes existantes. Livraison du backend avant le consommateur Commerçant.

Les chargements et confirmations de Commerçant sont harmonisés dans toute
l’application à leurs emplacements existants, sans nouvelles fenêtres bloquantes.
Succès confirmé, refus, résultat incertain et état courant indisponible restent
distincts. Les preuves attendues couvrent isolation et lectures bornées, filtres
et pagination, états de chaque jeu, brouillons et reprises sans double commande,
puis navigation clavier, texte agrandi et largeurs 320/390/1280 px.

Le guide Commerçant est actualisé avec captures, PDF relu et copie embarquée.
Le guide Animation est sans impact : ses écrans et procédures de préparation
et de validation ne changent pas. Les résultats exécutés sont consignés dans
le [bilan du correctif](bilan-realisation.md#correctif-du-22-novembre-2026--clarifier-la-préparation-commerçant), séparément des preuves historiques.

## 1. Créer une édition — CA-01/02

Le gestionnaire habilité travaille dans son organisation et sa commune active.
Le type technique cible est `JEU_VITRINES`, contrat `1.0` ; il doit être déclaré
dans le catalogue et les capacités des consommateurs avant toute activation.
Un modèle absent ou commercialement indisponible ne peut pas être créé en
manipulant la requête. Le jeu est inclus au forfait standard organisateur,
avec les dotations existantes ; aucune option payante ni quota propre E78.
Les limites et droits communs de l'offre continuent de s'appliquer.

L'assistant distingue identité/thème, calendrier/règlement, commerces/vitrines,
règles de réponse et de gain, dotation, préparation puis revue de publication.
Il reprend les droits, dates et validations communes. Les horaires sont présentés
dans le fuseau de Paris ; les décisions utilisent des instants serveur.
Un thème est un contexte de jeu, pas une modification de ses règles.

Les commerces sont recherchés par nom et contexte, avec pagination serveur.
L'organisateur voit séparément invitation/accord E56, contenu à préparer,
approbation et mise en place physique. Une adhésion à l'animation ne rend pas
la vitrine prête. Une révision en attente ne devient pas implicitement approuvée.

## 2. Préparer une vitrine — CA-03/04/14

La préparation privée contient la consigne publique d'observation, la description
de l'intrus et la réponse attendue, les modalités de mise en place, l'emplacement
compréhensible de la vitrine et les informations pratiques nécessaires à l'accès.
La vitrine doit être identifiable ; la question distingue sans ambiguïté l'intrus
du décor. Le contenu est en texte simple échappé.

Chaque commerce dispose d'un défi QCM et
d'un intrus pour l'édition. Deux à six choix distincts décrivent des objets ;
exactement un choix est correct. Les choix sont identifiés indépendamment de leur
justesse et présentés dans un ordre stable. La solution privée n'est pas encodée
dans un nom d'ID, l'ordre des options, une classe CSS ou une description d'image.
Le bon libellé figure nécessairement parmi les options publiques : c'est son
marquage comme correct et le corrigé qui restent privés.

Une preuve photo de mise en place, si elle est fournie, reste privée et réservée
au contrôle. Ne pas la publier automatiquement comme illustration du jeu.
Une illustration publique doit être réellement fournie, autorisée et ne pas
dévoiler l'intrus ; son absence donne un rendu sobre, sans photographie inventée.
Le kit distingue instructions privées de placement et support public d'accès à Live.

### Responsabilités — ARB-03 résolu

Le commerçant principal accepté au titre d'E56 prépare **sa** vitrine dans Pro.
L'organisateur approuve la version proposée et confirme le contrôle terrain.
Les salariés disposant seulement du droit de validation E72 n'acquièrent aucun
droit d'édition de contenu. L'organisateur demande une correction au commerçant
au lieu de remplacer son contenu ; l'auteur et l'approbateur restent traçables.

| État du contenu cible | Déclencheur autorisé avant publication | Résultat |
| --- | --- | --- |
| À compléter | Préparateur enregistre un brouillon | Révision suivante ; aucune approbation ou disponibilité supposée |
| À compléter / À corriger | Préparateur propose un contenu complet | Proposé, révision identifiée |
| Proposé | Organisateur demande une correction motivée | À corriger ; commentaire limité au bon commerce |
| Proposé | Organisateur approuve la révision consultée | Approuvé pour cette seule révision |
| Proposé / Approuvé | Préparateur modifie un élément du défi | À compléter ; ancienne approbation et contrôle terrain invalidés |
| Tout état | Acteur sans droit ou révision obsolète | Refus, aucun écrasement ni validation d'un ancien contenu |

La mise en place est un fait distinct : auteur du constat, date, révision du
défi, emplacement et observations. Elle confirme que l'intrus prévu est visible,
identifiable et maintenu pendant la période annoncée. Une photo ne constitue
pas à elle seule cette confirmation. Le commerçant confirme l'installation,
puis l'organisateur réalise et confirme le contrôle terrain sur cette installation
et cette révision du contenu. Un changement de placement ou une nouvelle
attestation d'installation invalide le contrôle antérieur, même à contenu identique.

## 3. Approuver puis publier — CA-02/04

La revue rassemble règles publiques, commerces retenus, approbations exactes,
préparation matérielle et prérequis de dotation. Chaque blocage indique la
prochaine action et son acteur. Un contrôle incomplet, une ancienne révision,
une invitation non acceptée ou une condition de gain inatteignable empêchent
la publication. Il n'existe pas de bouton contournant ces contrôles dans l'ERP.

Publier fige une définition privée et sa projection publique, liée aux versions
approuvées et aux constats terrain. Une modification concurrente fait échouer
la publication, sans publication partielle. Les commandes de préparation ne
modifient plus le contenu joué. La correction d'une réponse publiée relève
du traitement d'incident décrit ci-dessous ; elle n'écrase jamais les réponses
déjà enregistrées.

La consigne indique qu'il faut observer la vitrine. Le QR/lien public ouvre
le jeu ou le défi ; il ne certifie ni visite, ni observation, ni réussite.

## 4. Découvrir et jouer dans Live — CA-05 à 09/15

Le catalogue, la fiche, le carnet et les QR orientent vers **Localeo Live**.
Un lien profond identifie l'animation et la vitrine, puis conserve cette cible
après inscription ou récupération de la participation. Un identifiant de
vitrine étrangère ne permet pas de lire ou modifier son défi.

La fiche rend lisibles thème, dates, commerces/adresses disponibles, règles
d'essais et de retour, condition de qualification, dotation et règlement avant
la première réponse. Les vitrines sont consultables dans une liste paginée et
un parcours libre ; aucun lieu futur caché de la chasse n'est réutilisé.
La participation et sa récupération réutilisent l'identité et le carnet existants.

Le joueur sélectionne un choix, voit
un récapitulatif indiquant le commerce et l'objet, puis confirme sa réponse
définitive. Changer de choix ou annuler avant confirmation n'envoie rien.
La commande serveur admet un choix de la version jouée uniquement pendant
`[début, fin[`, dans un statut jouable et avec les droits actuels.

Une réponse correcte **ou incorrecte** consomme l'unique essai. L'écran affiche
« Intrus trouvé » ou « Intrus non trouvé — réponse définitive enregistrée ».
Il ne propose pas de deuxième essai ni la solution d'un échec avant la révélation
autorisée. Une mauvaise réponse valide est un résultat enregistré, pas une
erreur de formulaire. La confirmation d'une réussite révèle logiquement que
le choix personnel est juste ; le corrigé général reste privé jusqu'à la clôture.

| Situation | État visible et action |
| --- | --- |
| Avant le début | Date d'ouverture ; consigne et conditions, aucune soumission active |
| Jouable, sans réponse | À découvrir ; sélectionner puis confirmer |
| Commande en cours | Enregistrement en cours ; empêcher le double clic |
| Réponse réseau perdue | Résultat à vérifier ; lire le reçu puis la participation |
| Réponse correcte confirmée | Résolue ; progression serveur et prochaine vitrine |
| Réponse correcte, passage requis encore absent | Intrus trouvé, passage à valider ; le commerce ne compte pas encore |
| Réponse incorrecte confirmée | Réponse définitive enregistrée ; aucune invitation à réessayer |
| Suspension ou incident | Motif public utile, réponse désactivée ; conserver les acquis confirmés |
| Après la fin mais clôture non terminée | Jeu terminé, résultats en préparation ; aucune réponse ni révélation anticipée |
| Clôture métier confirmée | Bilan et révélation des solutions ; gains distincts |
| Droit expiré / erreur / liste vide | États distincts, récupération ou nouvelle lecture ciblée, aucun faux zéro |

Un rejeu réseau réutilise la même intention, la même clé et le même contenu.
Le reçu confirmé prévaut sur une ancienne saisie locale. Recharger ou reprendre
sur un autre appareil retrouve la réponse serveur ; une sélection non soumise
n'est pas une promesse de synchronisation entre appareils.

## 5. Qualification et gains — CA-10/11

La règle est publique et versionnée. Le compteur de vitrines vues n'est pas le
compteur de bonnes réponses ; un QR n'ajoute aucune réussite. La qualification
est décidée par le domaine et ne découle jamais d'une jauge remplie côté client.

La décision utilisateur reprend les conditions du Juste Prix local. Pour N
vitrines publiées et un seuil K choisi par l'organisateur, exiger `1 <= K <= N`.
Le gestionnaire choisit explicitement **avec ou sans passages requis** avant
publication ; aucun défaut silencieux. K=N est possible, sans constituer un mode
différent. Le participant est qualifié quand X commerces distincts comptent et
`X >= K`. Une réussite supplémentaire n'ajoute ni ticket ni chance.

| Réponse définitive correcte | Passage confirmé du même commerce | Sans passages requis | Avec passages requis |
| --- | --- | --- | --- |
| Non / absente | Non ou oui | Ne compte pas | Ne compte pas |
| Oui | Non | Compte une fois | Intrus trouvé, passage à valider |
| Oui | Oui | Compte une fois | Compte une fois |

Si requis, le passage peut précéder ou suivre la réponse, pendant la période
jouable publiée. Pro réutilise le scan authentifié et la validation PIN E70 sur
le téléphone habitant ; un salarié agit seulement avec son habilitation E72
effective. La preuve appartient à la même participation, configuration, étape
et commerce. Un QR public, un passage d'une autre édition ou une preuve d'achat
étrangère ne compte pas. Un passage tardif ou pendant la suspension est refusé,
même si l'intrus a déjà été trouvé. Révoquer un salarié/PIN empêche ses actions
futures sans effacer les preuves valides déjà confirmées. Aucun retrait individuel
de preuve ni disqualification rétroactive n'est ajouté ; suivre le traitement
d'incident. Un passage ne corrige jamais une mauvaise réponse définitive.
Sans passage requis, ne pas proposer de commande Pro/PIN E78 inutile.

Live distingue les bonnes réponses, les passages manquants et X/K ; N reste le
nombre de vitrines disponibles. « Toutes les réponses enregistrées » ne signifie
pas « Qualifié ». Si le seuil devient impossible pour ce participant, conserver
ses faits et expliquer l'état sans nouvel essai ni baisse de K.

La clôture fige une audience complète avant tout tirage. Les lots, attributions,
bons et remises réutilisent leurs mécanismes existants. Une bonne
réponse ne constitue pas un gain ; la remise reste dans les parcours dédiés.
E78 ne crée ni nouvelle conservation nominative ni droit de contacter les joueurs.

## 6. Incident après publication — CA-13

Les faits sont consignés : vitrine concernée, motif, auteur, instant et version.
Un objet absent/déplacé, un commerce inaccessible ou une erreur de solution ne
permettent pas d'éditer silencieusement l'intrus, la bonne réponse ou le seuil.
Les anciennes réponses et leurs résultats restent auditables.

Suspendre l'édition pour arrêter les nouvelles
réponses et validations de passage ; informer les participants via l'état consulté et les mécanismes
système autorisés. Reprendre la même définition seulement si le même dispositif
est rétabli et contrôlé. Chaque incident identifie les vitrines affectées et sa
révision. Après rétablissement, l'organisateur consigne un **nouveau contrôle**
de ces vitrines, lié à la révision de cet incident, à la définition publiée et
à l'identifiant stable du cycle de suspension. Un contrôle antérieur à l'incident
ne suffit jamais. Un incident modifié ou une nouvelle suspension invalide ce
constat pour la reprise. Tous les incidents bloquants doivent être contrôlés ;
la commande de reprise vérifie ces faits sans modifier le contenu publié.
Un formulaire ancien est revérifié à la soumission.
Pendant la suspension, « Déclarer un autre incident » ajoute un signalement au
même cycle et à la même définition. Les constats des incidents précédents sont
conservés ; ils ne couvrent pas le nouvel incident, même s’il touche le même
commerce. Le dossier courant est borné techniquement à 10 incidents par cycle ;
à cette borne, rétablir le dispositif ou annuler l’édition. Une suspension
ultérieure, après reprise, ouvre un nouveau cycle.
Si l'erreur exige une nouvelle solution, annuler selon les droits du socle puis
créer une nouvelle édition ; aucune réponse ou chance n'est transférée implicitement.
Un report de fin suit son workflow existant, séparément, avec conséquences visibles.
La reprise exige une période encore ouverte `[début, fin[` ; un report éventuel
doit passer par ce workflow avant expiration et ne découle jamais de la reprise.
Une édition toujours suspendue à la fin ne peut être rouverte ni clôturée pour
contourner un incident : le gestionnaire procède à l'annulation puis, si nécessaire,
à une nouvelle édition. Les faits confirmés restent conservés selon leur politique.

Retirer ou neutraliser une vitrine publiée, modifier N/K, la solution ou le mode
de passage est exclu de cette version. Une impossibilité de rétablir le dispositif
conduit à l'annulation et à une nouvelle édition, sans transfert de réponses,
passages ou qualifications. La neutralisation d'une étape de chasse ne s'applique pas.

## 7. Gestion, kit et accessibilité — CA-12/14/15

Animation/ERP utilisent une liste de gestion comparable : commerce, accord,
contenu/révision, approbation et préparation matérielle ; filtres puis pagination.
La fiche affiche organisation, commune, édition et état, puis l'action utile.
La vue de bilan expose agrégats datés et listes autorisées, sans solution dans
les exports publics ni réponse nominative ajoutée au suivi par défaut.

Appliquer les [règles ERP](../../architecture/transverse/conventions-backoffice.md#ux-des-pages-de-gestion-erp) :
`ERP-UX-01/02/03` pour structure et contexte ; `04/11` pour comparaison,
pagination et faits fiables ; `05/06/08/09` pour édition, brouillons, retour,
erreurs et conflits ; `07/10/12` pour conséquences, accessibilité et recette.
Une action destructive ou sensible a une confirmation contextualisée ;
un filtre de liste ne définit jamais silencieusement sa portée.

Le kit privé contient le défi et les consignes de placement, avec révision.
Le flyer public contient nom/thème, accès au jeu et QR/lien public ; aucune
solution, preuve photo privée, donnée personnelle ou accès participant.
Un kit ancien est signalé comme tel et ne confirme aucune préparation actuelle.

Live applique les [principes UX](../../produit/live/principes-ux.md) : carnet
fondé sur les faits serveur, progression et qualification distinctes, une action
principale, retour conservé vers la bonne liste/carnet. Prévoir 320/390 px,
texte 200 %, cibles de 44 px, navigation clavier, radios nommés, focus dans
la confirmation et retour au déclencheur, annonces du résultat, réduction des
mouvements et états lisibles sans couleur seule. Une image ne contient jamais
la seule consigne utile. Les données publiques obsolètes ne réactivent pas une
commande lorsque la lecture de droits a échoué.
