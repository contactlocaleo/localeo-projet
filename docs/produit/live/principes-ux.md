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

## LIVE-UX-01 — Le carnet de bord est le centre de l’expérience

L’habitant retrouve ses animations, ses coffrets, ses lots et ce qu’il peut faire
ensuite. Le carnet raconte ce qu’il a commencé, accompli et peut poursuivre.
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

## LIVE-UX-09 — Partager la lisibilité de Localeo Pro

**Orientation précisée le 10 novembre 2026.** Reprendre la typographie et les
sections de [Localeo Pro](../../architecture/transverse/identite-entetes-applications.md#charte-des-espaces-de-gestion-internes--référence-crm) :
police système, corps et actions 14 px, titres 25 / 18 / 15 px, titre principal
23 px sur mobile à taille de texte standard. Employer des unités relatives
pour conserver l’agrandissement du texte ; les champs mobiles restent à 16 px
et les cibles tactiles à 44 px minimum.

Sections blanches bordées, angles de 12 px, actions de 9 px, fond clair
`#f5f7f9`, texte `#183243`, secondaire `#526575`, action `#09685e` et bordure
`#d8e1e7` forment la base commune. Le carnet conserve sa tranche, ses tampons,
ses tickets et les couleurs sémantiques utiles. Les menus métier de Pro ne
remplacent pas les trois rubriques habitantes.

Dans une participation, placer progression confirmée et prochaine action avant
historique et détails secondaires. Dans Mes lots, privilégier le gain, son état
et son retrait plutôt que de grands compteurs. Dans Découvrir, rendre visibles
la recherche et « Pour plus tard », même sans favori ; « Garder » et « Partager »
associent une icône à un verbe. La sauvegarde d’une idée ne vaut pas inscription.

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

## Application aux évolutions futures

### Première participation et continuité

L'entrée explique en une phrase ce que l'habitant peut vivre. La découverte
présente le parcours, son bénéfice réel et l'effort avant l'engagement. Une
première visite sans carnet propose d'abord de découvrir ; la récupération
s'adresse explicitement à qui a déjà participé. La confirmation nomme l'objet
acquis et ouvre son prochain geste, puis Mon carnet. Une panne propose une
reprise compréhensible sans répéter l'inscription.

Le même vert d'action et les mêmes sections accompagnent ces étapes. Le livret
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
Les animations du carnet correspondent aux inscriptions personnelles encore
ouvertes ; les favoris appartiennent à Découvrir et les gains restent dans
Mes lots après clôture. Distinguer état de participation, progression et cycle
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
