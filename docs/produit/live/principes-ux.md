# Principes directeurs UX de Localeo Live

**Référence de conception et de revue — 9 novembre 2026.** À appliquer à toute
évolution de l’expérience habitant, sur le domaine Live et ses parcours servis
depuis une autre origine. Cette référence pérennise l’orientation demandée :
un carnet de bord digital personnel, simple, immersif et incitatif au quotidien.

Les spécifications [E42](../../specifications/epic-42-localeo-live/README.md) et
[E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md)
portent les comportements détaillés et leurs critères d’acceptation. Les principes
ci-dessous guident leurs évolutions ; ils ne valent pas preuve de déploiement.
La navigation courante est définie par E73-EVO-LIVE-CARNET-BORD : **Mon carnet /
Mes lots / Découvrir**, avec les communes accessibles depuis Découvrir. Les
tampons sont définis par E73-EVO-LIVE-TAMPONS. Les compositions plus anciennes
restent historiques.

## Référence obligatoire du 17 novembre 2026 — maquettes validées

**L’UX de Localeo Live doit être revue pour se conformer strictement aux
maquettes validées dans l’[audit UX habitant du 17 novembre 2026](../../audits/marketplace/localeo-live-ux-habitant-maquettes-2026-11-17.md).**
Les deux planches conservées dans ce rapport fixent la composition, la hiérarchie
des informations, les actions, les confirmations, la navigation et la direction
artistique de la prochaine mise en conformité. Elles constituent une référence
de conception obligatoire, pas une simple source d’inspiration. La recette
doit comparer le rendu aux maquettes et vérifier les parcours ; toute divergence
doit être identifiée et faire l’objet d’un arbitrage explicite.

**Arbitrage du 18 novembre 2026 :** l’en-tête Localeo et ses outils Messages
et Menu sont conservés au-dessus du contenu. Leur présence et la hauteur
supplémentaire, absentes des planches, sont explicitement acceptées par le
demandeur et complètent la référence de conformité.

La navigation reste **Mon carnet / Mes lots / Découvrir**. La consultation d’une
commune et sa mémorisation sont distinctes. La reprise personnelle reste visible
même dans un carnet rempli. Dans une participation en cours, progression et
action utile précèdent le suivi du tirage ; après achèvement ou résultat, la
priorité s’adapte aux faits confirmés. Les vues de validation incertaine et
confirmée représentent des états d’un même écran. Pour un lot, disponibilité,
consignes pratiques et action adaptée précèdent les éléments secondaires ;
« Marquer comme vu » conserve un effet local distinct de la remise ou consommation.

**Complément du 21 novembre 2026 — vignettes évocatrices :** les participations
prennent la forme d'une page reliée, les gains d'un cadeau personnel et le
programme de feuillets datés. La famille Papier doux, les actions principales
vertes et la hiérarchie des informations restent la référence. Ce complément
précise les maquettes sans créer de calendrier navigable ni de nouvel état métier :
[E73-EVO-LIVE-VIGNETTES et critères VP-01 à VP-05](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#e73-evo-live-vignettes).

Les textes et valeurs de démonstration ne créent aucune règle métier. Chaque
déclinaison utilise les données, conditions et droits réels, préserve les états
inconnus/refusés et reste accessible sur petit écran et avec texte agrandi.
Les dispositions datées ci-dessus précisent la prochaine cible UX ; les règles
métier existantes restent portées par les spécifications et le domaine backend.
La validation de conception ne vaut ni implémentation ni essai habitant réussi.

La demande de mise en œuvre est suivie dans **E73-EVO-LIVE-MAQUETTES** :
[critères LM-01 à LM-11, réalisation et preuves](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-17-novembre-2026--maquettes-habitant).
Dans le passeport, choisir un commerce prépare la visite ; présenter son QR
ne valide rien à lui seul. « Vérifier la validation » relit la preuve de ce
commerce. Dans Mes lots, le bon est présenté après lecture de son état et sa
fermeture relit le résultat ; « Marquer comme vu » garde uniquement un repère
dans ce navigateur. Les essais habitants restent une preuve distincte.

## LIVE-UX-01 — Le carnet de bord est le centre de l’expérience

L’habitant retrouve ses animations et ses coffrets dans Mon carnet, et ses gains
dans Mes lots. La vignette de l'animation signale le résultat personnel confirmé
avec une icône et un libellé : Gagnant ou « Vous n’avez pas gagné cette fois-ci ».
Les cartes de lots restent dans Mes lots. Le carnet raconte ce qu’il a commencé,
accompli et peut poursuivre.
La découverte locale nourrit ce carnet et reste facilement accessible.
Chaque écran répond rapidement à trois questions : « Où en suis-je ? »,
« Qu’ai-je à retrouver ? », « Que puis-je faire maintenant ? ».

## LIVE-UX-02 — Les objets personnels restent faciles à retrouver

Conserver des repères explicites et stables pour les animations, coffrets et lots.
Les lots disponibles et leur action d’utilisation ou de retrait sont identifiables
sans parcourir les règles d’un jeu. Les détails, le QR et la récupération d’un
accès restent accessibles depuis l’objet concerné. Deux participations à la même
animation conservent chacune leur identité, leur progression et leurs accès.
Toute simplification de navigation doit préserver cette facilité à retrouver
ses objets, y compris dans un carnet rempli et sur un autre appareil.

## LIVE-UX-03 — Donner envie par une collection visuelle et réelle

Le suivi des animations prend la forme d’un carnet à compléter : tampons encrés
pour les validations confirmées, empreintes vides pour ce qui reste à accomplir,
compteur court et exact. Les marques acquises rendent le chemin parcouru tangible ;
les places restantes donnent envie de continuer. Une date réelle peut enrichir
le souvenir d’une visite. La texture papier et les détails de carnet soutiennent
la lecture, avec une composition sobre et cohérente avec l’identité Localeo.

Un long parcours conserve un aperçu borné, explicitement présenté comme tel,
et son compteur exact. Tant que l’objectif n’est pas atteint, l’aperçu conserve
une empreinte vide. Une progression inconnue reste indiquée comme telle.

## LIVE-UX-04 — Adapter les repères à chaque expérience

| Expérience | Représentation attendue |
| --- | --- |
| Passeport commerçant | Tampons des visites validées, date réelle disponible et accès au QR avant la liste des visites. |
| Chasse | Progression visuelle et prochaine étape autorisée ; les lieux et indices futurs restent masqués. |
| Tombola | Ticket de participation et état confirmé ; la représentation ne suggère pas un parcours de visites. |
| Coffret | Prestations restantes et consommées, accès à leur utilisation et validité. |
| Lot | Nature du gain, disponibilité confirmée et action pour l’utiliser ou le retirer. |

Le motif visuel traduit le fonctionnement réel du jeu. Un type inconnu utilise
un repère générique. Un carnet rempli ne suffit pas à annoncer une qualification
ou un gain : leurs états sont distincts et confirmés par le backend.

## LIVE-UX-05 — Privilégier l’iconographie et une prochaine action claire

Associer un pictogramme reconnaissable à un libellé court ; réserver les textes
longs aux détails consultables volontairement. Les conditions nécessaires à une
décision restent visibles au bon moment. Mettre en avant une action principale
par contexte : reprendre, présenter son QR, découvrir une étape ou retirer un lot.
Employer des verbes concrets et des encouragements brefs, fondés sur l’état réel.
Les tampons décoratifs se distinguent des commandes ; une action essentielle
reste compréhensible avec son libellé et son nom accessible.

## LIVE-UX-06 — Récompenser les acquis avec justesse

Une nouvelle validation peut produire un effet de tampon et une gratification
brève, à partir du reçu confirmé de l’action. Le rechargement ou la simple lecture
d’un ancien acquis conserve une présentation stable. Les effets respectent la
réduction des mouvements et laissent l’action suivante disponible.

L’envie vient des découvertes, de la collection et des progrès réels. Points,
séries quotidiennes, classements ou récompenses supplémentaires exigent une
évolution métier explicite et spécifiée ; ils ne se déduisent pas du décor.
Les états de chargement, de progression inconnue, de refus et d’expiration restent
distincts. Une donnée locale ancienne ne confirme ni droit, ni validation, ni lot.

## LIVE-UX-07 — Concevoir pour un usage quotidien sur téléphone

Préserver une hiérarchie visuelle courte, des zones tactiles d’au moins 44 px,
des contrastes lisibles et une lecture possible sans couleur ni animation seule.
La navigation basse ne masque pas l’action principale. À 320 et 390 px de large,
le carnet reste utilisable sans débordement horizontal ; le zoom et le texte
agrandi restent possibles. L’illustration accompagne la progression sans repousser
le premier geste utile sous une longue introduction.

**Agencement précisé le 21 novembre 2026.** Utiliser 12 px de marge extérieure
sous 390 px, puis 16 px, en évitant les encadrements et marges intérieures
imbriqués. Sur bureau, adapter les colonnes jusqu'à une largeur de 1 240 px ;
les formulaires restent limités à 640 px. Le texte agrandi peut réorganiser les
blocs et les compteurs : conserver leurs valeurs et libellés plutôt que forcer
une ligne au prix d'un débordement ou d'une troncature.

## LIVE-UX-08 — Préserver le chemin et les repères pendant l’attente

Un objet ouvert depuis Mon carnet revient à Mon carnet, avec son filtre et un
repère de reprise. Le libellé du retour annonce sa destination réelle. Un détour
par les messages, les commerces ou une fiche conserve l’étape précédente ; un
lien direct propose un retour explicite. Les métadonnées de navigation ne
contiennent ni accès personnel ni projection métier.

Conserver l’en-tête, la navigation et les données déjà affichées lors d’un filtre
local ou d’une actualisation. Au premier chargement, présenter une ossature
non interactive et une annonce courte, sans faux vide ni succession d’actions
provisoires. Éviter l’insertion tardive d’un bloc au-dessus d’une action disponible
et les translations d’entrée sur une simple consultation. Tester avec réponses
retardées, erreur, retour clavier et texte agrandi, pas seulement une page chargée.
Un refus confirmé reste prioritaire sur la conservation visuelle des données.
La conservation du bandeau ne doit pas conserver le QR, la saisie ou le panneau
d’un autre objet lors d’un changement de page.

Le même langage de chargement couvre les listes, détails, messages, commerces,
coffrets, inscriptions, récupération et documents Live. Une vérification en
cours ne signifie pas « indisponible ». Une actualisation échouée distingue le
dernier état connu du droit actuellement confirmé. Les QR, codes et actions
sensibles attendent cette confirmation. Une commande conserve son formulaire
et son résultat explicite ; elle n’est jamais relancée pour masquer une attente.

## LIVE-UX-09 — Partager la marque Marketplace avec une composition compacte

**Orientation révisée le 21 novembre 2026.** La référence visuelle de Live est
la Marketplace ; cette décision remplace l'alignement sur Localeo Pro du
10 novembre pour les polices, couleurs et finitions, tout en conservant sa
lisibilité compacte : corps et actions 14 px, titres 25 / 18 / 15 px, titre
principal 23 px sur mobile à taille de texte standard. Employer des unités
relatives ; les champs mobiles restent à 16 px et les cibles tactiles à 44 px.

DM Sans porte le texte courant, les contrôles et la navigation ; Oswald porte
la marque et les titres courts de page ou section. Réutiliser les polices
auto-hébergées de la Marketplace. Fond papier `#f6f5f1`, encre `#082840`, surfaces
blanches, secondaire `#586873` et séparateurs `#d7d9d8` constituent la base.
Les actions principales sont orange `#f28a2e` avec texte encre ; les actions
secondaires et liens restent encre. Le vert distingue les validations réussies,
jamais une nouvelle famille de commandes. Cartes à 4 px, panneaux à 6 px et
boutons à 4 px reprennent les tokens Marketplace ; les silhouettes de tickets,
tampons, badges et repères de progression restent propres au carnet.

La [signature publique](../../architecture/transverse/identite-entetes-applications.md#signature-publique-marketplace-live-et-e-mails--21-novembre-2026)
reprend le pictogramme Marketplace sans déformation, le bandeau encre et la
marque blanche avec « Live » identifié ; TEST reste visible. Conserver le
carnet, ses trois destinations et la prochaine action immédiatement accessible.
Les chartes de Pro, Animation et des outils internes restent inchangées.

Dans une participation, placer progression confirmée et prochaine action avant
historique et détails secondaires. Dans Mes lots, privilégier le gain, son état
et son retrait plutôt que de grands compteurs. Dans Découvrir, rendre visible
la recherche et garder un partage public nommé. **Arbitrage du 18 novembre :**
retirer l’ajout « Garder pour plus tard » ; les anciennes idées restent accessibles
si elles existent, sans être assimilées à une inscription. Retirer les filtres
internes du carnet, conserver les coffrets et les animations dans la même liste.
L’état de l’animation se place en tête de vignette avec son pictogramme ; l’état
personnel reste distinct. Les trois rubriques partagent leur ligne orange en tête, selon l’orientation du 21 novembre.
Les [correctifs canoniques](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#correctifs-du-18-novembre-2026--carnet-découverte-et-notification)
précisent les lectures et la composition des cartes selon les maquettes validées.

## LIVE-UX-10 — Des pictogrammes utiles et de l'espace pour agir

**Orientation précisée le 10 novembre 2026.** Une carte s'organise autour de
l'objet, d'un état utile, d'une progression éventuelle et d'une action principale.
L'icône de couverture accompagne l'identité ; elle ne réserve pas une colonne
vide à côté de toute la progression et du bouton. Utiliser la largeur disponible
avant d'augmenter la hauteur. Conserver les marqueurs du carnet et un seul cadre
expressif de tampons ou ticket.

Les pictogrammes utilitaires partagent un dessin et un sens : carnet, parcours,
boîte pour coffret, cadeau pour lot, ticket pour bon, QR pour présenter son code.
La coche indique un fait accompli confirmé ; expiration, annulation et refus ont
un repère distinct et leur libellé. Les icônes de navigation et gestes essentiels
restent accompagnées de mots courts. Une illustration ou un état local n'accorde
jamais de droit. Les règles, conditions et incertitudes nécessaires ne se retirent
pas pour raccourcir un écran.

Retirer les répétitions de l'objectif, du compteur et des précautions avant de
compresser la police ou les espaces. Viser 8 px dans un groupe, 12–16 px entre
groupes, 16 px entre cartes et 24 px entre sections, adaptés au premier viewport.
Les cartes visent 16 px de marge intérieure à 390 px, 12 px à 320 px. Les cibles
restent au moins 44 px, le corps/actions 14 px. Le premier geste utile reste
visible dans les cas nominaux ; titre long et texte agrandi gardent leur accès.

Un état vide confirmé dispose d'une invitation illustrée et d'une action ; des
compteurs zéro et phrases équivalentes ne remplacent pas cette orientation.
Lecture incomplète, refus et panne restent distincts. Les comportements et
preuves sont définis par [E73-EVO-LIVE-ICONOGRAPHIE](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-10-novembre-2026--iconographie-et-respiration-e73-evo-live-iconographie).

## LIVE-UX-11 — Composer les fiches et parcours à partir du premier geste mobile

**Orientation du 21 novembre 2026.** Les deux fiches publiques d'animation,
Agenda et Live, partagent cette hiérarchie : retour ; état et commune ; titre ;
objectif et dates ; compteurs publics ; conditions essentielles ; action
principale et récupération d'accès ; « Comment jouer ? » ; lots ; lieux
partenaires ; informations complémentaires et règlement. Viser 8 px entre
le retour et le premier contenu, sans ajouter d'espace pour une information
absente. Placer le visuel officiel après l'action principale ; un visuel absent
ou défaillant ne réserve pas un grand emplacement vide.

Présenter les participants, gagnants et lots dans une rangée commune de cellules
équilibrées à taille de texte standard : pictogramme et nombre, puis libellé,
avec séparateurs discrets. Masquer une mesure inconnue, conserver un zéro connu,
ne calculer aucun chiffre métier manquant dans l'interface. Après clôture,
employer « Lots prévus ». Les libellés peuvent occuper deux lignes et la rangée
se réorganise avec texte agrandi. Les cartes de catalogue gardent leur propre
présentation compacte ; la fiche ne répète pas les mêmes statistiques ailleurs.

Le badge d'état associe couleur et texte ; dates, tampons, pictogrammes et étapes
numérotées structurent l'information sans remplacer les consignes. Les conditions
nécessaires à l'inscription précèdent toujours l'action. Supprimer les raccourcis
redondants « Les lots » et « Les conditions » : présenter l'aperçu dans sa section,
avec « Voir tous les lots » si nécessaire, et un volet « Conditions et règlement ».
Le règlement reste également accessible depuis les conditions essentielles.
Les actions s'adaptent à la situation réelle : inscription, reprise, choix d'une
participation ou récupération d'accès ; champs, consentements et erreurs restent
complets et proches de leur contexte.

Dans Découvrir, réunir titre et actualisation sur une ligne, placer la recherche
dans l'en-tête des résultats et regrouper commune, catégories et périodes sans
répétitions. Dans le carnet et les coffrets, rapprocher identité, progression et
prochaine action ; une dotation inconnue prend une ligne sobre. Dans une
participation, progression et action utile précèdent les détails secondaires,
avec un QR accessible et correctement dimensionné même pour un identifiant long.
Dans Mes lots, compacter état et échéance, mutualiser les explications communes
et donner un traitement secondaire à l'historique ; les avertissements propres
à un lot restent visibles. Dans les messages, intégrer l'icône dans l'en-tête
pour rendre sa largeur au corps ; compacter les filtres et distinguer date,
animation et organisateur sans retirer le contenu.

La recette compare les rendus avant/après à 320, 390 et 1 280 px, complétés à
768 px pour les colonnes, puis avec texte à 200 %. Dans le cas nominal à
390 × 844 px, l'action principale reste visible au-dessus de la navigation
basse ; les titres longs et petits écrans gardent un défilement utilisable.
Les mesures absentes, grandes valeurs, dates, visuels défaillants et états
ouverts, futurs, clôturés ou indisponibles font partie des variantes. Préserver
chargement, refus, erreurs, saisies, filtres, navigation et restauration du focus.
La [recette E73](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#optimisation-mobile-live--21-novembre-2026)
distingue la cible de conception des preuves réellement exécutées.

## Application aux évolutions futures

### Première participation et continuité

L'entrée explique en une phrase ce que l'habitant peut vivre. La découverte
présente le parcours, son bénéfice réel et l'effort avant l'engagement. Une
première visite sans carnet propose d'abord de découvrir ; la récupération
s'adresse explicitement à qui a déjà participé. La confirmation nomme l'objet
acquis et ouvre son prochain geste, puis Mon carnet. Une panne propose une
reprise compréhensible sans répéter l'inscription.

Le même orange d'action et les mêmes sections accompagnent ces étapes. Le livret
désigne le passeport, le ticket la tombola, le magasin un commerce ou une visite,
le parcours la chasse, la boussole Découvrir et l'épingle la localisation.
Une participation confirmée utilise une coche cerclée et son libellé ; le
trophée désigne un gain. Les tampons gardent une silhouette lisible à petite taille ; leur
interactivité repose sur des informations effectivement disponibles et utiles.
La mesure de l'adhésion distingue inscription confirmée, ajout d'accès et
progression ; elle conserve consentement, suspension et minimisation existants.
Voir [E73-EVO-LIVE-PARTICIPATION](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-10-novembre-2026--participation-e73-evo-live-participation).

Précision du 11 novembre : le carnet privilégie l'action de chaque objet et
évite un bandeau « À vous de jouer » qui la duplique. Le suivi de chaque animation
présente inscription, qualification, tirage et résultat dans un workflow visuel
unique, avec les mêmes repères pour passeport, chasse et tombola. Ce suivi
remplace le bloc textuel de qualification ; les tampons et activités restent
propres à chaque expérience, sans qualification ou résultat inventé.
Les onglets de Découvrir partagent un en-tête et une sélection de
communes stables. Les réglages de l'appareil restent dans Réglages ; la catégorie
Animations y pilote aussi les messages des organisateurs, sans accord individuel.
Dans le passeport, les visites tamponnées portent la progression : une seconde
rangée de tampons synthétiques ne la répète pas. Le lien vers les commerces
reste dans ce bloc principal, avec le QR et les informations de visite.
Les animations du carnet correspondent aux inscriptions personnelles non
archivées par l'organisateur ; les favoris appartiennent à Découvrir et les gains
restent dans Mes lots, y compris après clôture ou archivage. Distinguer état de
participation, progression et cycle
de l'animation. Une vignette donne accès à ses nouvelles non lues, avec reçu
de lecture confirmé. Le badge Mes lots représente les gains non encore vus,
acquittés par « J’ai vu ce lot » ; il ne représente jamais des retraits restant
à effectuer. Préciser la portée locale du repère et les compteurs incomplets.
La récupération « Retrouver mon carnet » reste dans le menu secondaire.
Une date de tirage annoncée est visible sur la vignette de l'animation, avec
repère calendrier et heure de Paris. Elle ne signifie ni qualification ni
résultat ; retrait de l'annonce, résultat et annulation actualisent ce repère.
Voir [E73-EVO-LIVE-SIMPLICITE](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-11-novembre-2026--simplicité-e73-evo-live-simplicite).


Lors du cadrage ou de la conception d’une évolution Live, référencer les principes
`LIVE-UX` concernés dans les critères ou la note de conception. Lors de la revue,
vérifier leur traduction dans les écrans touchés. Une dérogation se documente
dans la spécification avec son motif et son effet sur le parcours ; un changement
d’orientation durable actualise aussi la présente référence.

Pour un changement visuel du carnet ou de la navigation, contrôler un carnet
rempli avec participation en cours, coffret partiellement utilisé et lot disponible,
puis les états vide et indisponible. Vérifier l’accès au lot et à la prochaine
action sur mobile. Pour un suivi de jeu, couvrir les moteurs touchés, les états
zéro/partiel/terminé/inconnu, la lisibilité et le mouvement réduit. Réutiliser les
tests et captures ciblés ; adapter leur étendue au changement. Une retouche
documentaire seule se vérifie par ses liens et sa cohérence.

Ces principes concernent la présentation et ses preuves. Les règles de validation,
les permissions, les contrats API et les états produit gardent leurs propriétaires
et leurs spécifications. Leur inscription ici n’exige aucune migration, activation
ops ou modification du générateur de démonstration.

## LIVE-UX-12 — Une iconographie illustrative et distinctive

**Décision du 21 novembre 2026 — E73-EVO-LIVE-ICONOGRAPHIE-PREMIUM.**
L’iconographie est une exigence majeure de qualité de Live. Une simple
substitution de pictogrammes génériques ne suffit pas : les objets doivent
être reconnaissables, soignés et cohérents aux tailles réellement utilisées.

La famille vectorielle locale reprend papier, encre et orange de la signature
Marketplace. Le vert reste réservé aux validations réussies. Deux niveaux de
détail partagent une même silhouette : compact pour navigation et commandes,
illustratif pour objets et états vides. Les libellés des destinations et gestes
essentiels restent visibles ; aucune information ne dépend de la couleur seule.

Ticket à souche pour tombola, livret pour passeport, carte pliée pour chasse,
vignette au coin décollé pour collection, empreinte encrée pour tampon,
cadeau avec ruban pour Mes lots, carnet relié pour Mon carnet, boussole pour
Découvrir, boîte à couvercle pour coffret et coupon vertical pour bon numérique.
Le coupon ne reprend pas le ticket de tombola, le carnet ne reprend pas le
passeport, le coffret reste distinct du cadeau. Les repères génériques ne
prétendent pas connaître un type d’animation absent.

Les tampons pleins représentent uniquement une validation confirmée ; les
empreintes à compléter et les états inconnus restent distincts. Les flyers
personnalisés, textes, droits et actions gardent leur rôle. La refonte
n’ajoute ni mouvement décoratif ni nouvel état métier.

La direction retenue est **Papier doux, finition 02** : coins arrondis,
papier crème, accent abricot et encre adoucie. Coutures, chants et gravures
enrichissent les formats illustratifs ; les commandes compactes restent lisibles.
Les repères communs du Marketplace utilisent les mêmes dessins et les mêmes
distinctions entre objets, sans remplacer leurs visuels personnalisés.

La recette compare la planche vectorielle et les écrans réels avant/après,
à 320/390/1280 px, avec texte agrandi, navigation clavier et états dégradés.
La reconnaissance par des habitants nécessite un essai distinct. Voir les
[critères IP-01 à IP-06](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#e73-evo-live-iconographie-premium)
et les [preuves locales](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#iconographie-premium-21-novembre-2026).
