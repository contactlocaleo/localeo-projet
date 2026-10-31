# E73 — Suivi de réalisation locale

Début : **18 octobre 2026**. [Spécification](README.md), [backlog](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md), [matrice des 63 critères et preuves](verification-livraison.md). Objectif : les 38 US, dans les dix lots demandés. Les lignes ci-dessous ne valent pas acceptation tant que les preuves correspondantes ne sont pas enregistrées.

## 31 octobre 2026 — création des chasses et guidage du gestionnaire

Demande : alléger le récapitulatif, expliciter la prise en compte et rendre
Assistant et Configuration plus utiles. Bases Animation **69b3ef8**, Projet
**fc0b32d**, autres modifications locales conservées. La reproduction initiale
constate un brief plafonné à **630 px pour 1 070 px disponibles** ; le contrôle
de largeur échoue avant correction. Le récapitulatif réaffichait une longue
liste de textes et le message de réussite disparaissait lors de la navigation.
Les formulaires de Configuration étaient comprimés à côté du parcours.

Le brief et son pied d’actions occupent désormais la largeur disponible. Le
récapitulatif présente des repères illustrés, garde les contenus complets dans
des détails dépliables et propose des accès Modifier sans perte de saisie.
L’introduction Léo et la bibliothèque ne sont plus répétées au récapitulatif.
Après reçu confirmé, un accusé focalisé dans la fiche distingue demande de
préparation et brouillon réutilisé, avec accès direct à Configuration. Les
relectures auxiliaires ne conditionnent plus cet accusé. Une réponse perdue
reste incertaine jusqu’à recherche du reçu ; aucun renvoi automatique.
L’accusé n’est ni persisté ni partagé entre contextes.

Assistant place les points d’attention en premier, puis une prochaine action
concrète, son intervenant et des étapes illustrées ; aides et vérifications
acquises restent consultables à la demande. Configuration affiche une seule
rubrique en pleine largeur avec consigne, repère et groupes explicites pour
présentation, dates, règlement et lots. Les panneaux visités restent montés,
les saisies sont conservées et les protections financières et de publication
demeurent. Un enregistrement des paramètres confirmé dispose aussi de son
repère visible et de son focus. Les CSS sont ciblées à leur source.

Preuves locales : types, lint, build de production isolé et **249 tests Node**
réussis, sans test ignoré. **82 contrôles navigateur** de préparation/génération
passent à 1280/390 px, dont réponse perdue, reçu confirmé malgré quota indisponible,
édition depuis le récapitulatif et réutilisation de bibliothèque.
La recette Léo et les quatre parcours Assistant intégrés passent également.
Les **268 contrôles** de préparation intégrée et les **40 scénarios /
448 contrôles** de dotation passent, avec versions, conflits, refus et commandes
incertaines préservés. La recette de préparation vérifie aussi la pleine largeur,
le focus de confirmation des paramètres et Configuration à 320 px/texte 200 %.
Les fixtures devenues anciennes sont alignées sur les sélecteurs bornés déjà
consommés par l’application ; aucune assertion métier affaiblie.

Les bancs autonomes Assistant et récapitulatif/accusés passent chacun
**16 scénarios** à 1600/390/320 px, dont texte à 200 %, clavier, focus,
cibles tactiles, détails conservés et absence de mutation. L’assertion de
lecture verticale des modalités des lots échoue avant restriction du sélecteur
CSS et passe après. Captures inspectées sur mobile, bureau et texte agrandi.
Les tests utilisent uniquement des données synthétiques et bloquent le réseau
externe, sans configuration opérateur.

Périmètre : portail Animation et documentation canonique E73/E55. Critères
d’ergonomie précisés ; états de roadmap conservés. Sans impact sur contrats API,
domaine, migrations, données existantes, générateur ou configuration ops : les
commandes et validations restent celles existantes. Backend, Pro et Marketplace
inchangés par ce correctif. Recette hébergée non exécutée ; aucun commit, push
ni déploiement effectué.

## 31 octobre 2026 — harmonisation du centre de notifications Live

Demande : aligner le centre de notifications sur la charte des autres pages.
Bases Marketplace **1699216**, Projet **fc0b32d**, changements locaux précédents
conservés. Cause : styles historiques du centre répartis dans `live.css`,
angles droits, réglages contradictoires de titre/actions et notifications lues
rendues par une baisse globale d’opacité. La reproduction depuis
`/live/messages` constate aussi l’absence de nom accessible du dialogue avant
interaction clavier : le scénario échoue sur le centre nommé attendu.

Les styles du centre sont consolidés dans `live-inbox.css` et retirés de leurs
anciennes règles, y compris les branches partagées, sans ajout de `!important`.
Typographie Live, surfaces et actions arrondies, pictogrammes par catégorie,
titre et contenu hiérarchisés, mentions **Non lue / Lue** et compteur de
notifications non lues dans l’aperçu affiché. Les messages lus gardent leur
contraste. Le bouton Fermer reste dans une barre adhérente ; le dialogue possède
son nom accessible dès le rendu et le focus initial va à la fermeture.
Les états vide, chargement et erreur ont leur repère visuel et une annonce
accessible. Les contenus restent du texte échappé, avec retour à la ligne.

Lecture individuelle, marquage des messages affichés, curseurs, mémorisation
locale et garde de navigation interne gardent leurs implémentations existantes.
Pas de nouvelle lecture implicite ni de permission Push. Le compteur n’invente
pas de total des notifications distantes. Même centre sur Animation et Coffrets,
avec le fond de leur surface respective ; les autres pages sont conservées.

Preuves locales : **11 scénarios navigateur réussis**, dont les huit nouveaux
cas du centre, la messagerie directe existante, le parcours à 320 px/texte
200 % et le confinement clavier des dialogues Live. Couverture à 320/390/1280 px,
surface Coffrets, états vide/erreur, pagination en échec puis reprise du même
curseur, lecture individuelle et collective, navigation interne, absence de
lecture implicite et texte échappé. La fixture compte séparément la lecture du
badge de l’en-tête et celle du centre à l’ouverture. Les deux scénarios voisins
d’accord organisateur, réponse perdue et retrait passent également. Captures
avant/après lecture inspectées sur mobile et bureau, dont texte agrandi.
Build de production isolé du banc et lint réussis ; le lint exclut uniquement
les répertoires de travail locaux `output/**` et `tmp/**`, ignorés par Git et
inaccessibles sous Windows (même contrainte constatée au correctif précédent).
Contrôles des liens/sources documentaires et `git diff --check` réussis.

Périmètre : Marketplace/Live et documentation canonique. Sans impact sur
contrats API, domaine, migrations, données existantes, générateur ou
configuration d’exploitation : seule la présentation utilise les réponses
existantes. Backend, Pro et portail Animation inchangés par ce correctif.
Statut de roadmap conservé. Recette hébergée non exécutée ; aucun commit, push
ni déploiement effectué pour ce correctif.

## 31 octobre 2026 — bloc des communes plus graphique sur l’accueil Live

Demande : remplacer le résumé trop textuel des communes dans Accueil. Bases
Marketplace **1699216**, Projet **fc0b32d**, autres travaux locaux conservés.
Cause : `LiveDiscovery` joignait les noms par un séparateur dans un paragraphe,
avec un lien de modification, sans repères visuels individuels. Le scénario
avant correction échoue sur l’absence du titre/région **Mes communes** attendu
dans l’accueil à 320 px.

Le bloc affiche désormais un compteur des communes suivies et des accès
individuels avec pictogramme de localisation, nom complet et flèche de
navigation. **Modifier mes communes** reste distinct et rejoint la page
existante. Les styles sont corrigés à leur source dans `live-discovery.css`,
en retirant le traitement commun du paragraphe ; pas d’image de remplacement,
de carte supposée ni de nouvelle statistique d’activité. Le bandeau reste
après la scène communale et les priorités personnelles gardent leur place.

Le clic sur une commune ouvre `/live/decouvrir?commune=<id>` et conserve la
sélection locale ; ni écriture API ni demande de position supplémentaire.
Le parcours partagé, la limite de dix choix et la recherche pour la sélection
vide restent ceux existants. Icônes décoratives, noms accessibles explicites,
liens de 44 px minimum, repli des noms longs et mouvements réduits conservés.

Preuves locales : les **4 nouveaux scénarios navigateur** passent à
320/390/1280 px, dont texte à 200 %, noms longs, dix communes, clavier, contexte
partagé sans changement de sélection et accès à la gestion. Les **6 tests Node**
des communes suivies et de la concurrence bornée passent aussi. Captures
inspectées sur mobile et bureau. Build de production isolé du banc navigateur
réussi, sans fichiers d’environnement opérateur. Le lint passe avec
`npm run lint -- --ignore-pattern 'output/**' --ignore-pattern 'tmp/**'` :
l’appel sans exclusions échouait sur des répertoires de travail ignorés par Git
et inaccessibles sous Windows (`EPERM`), sans modification de leurs permissions
ni de la configuration ESLint. Contrôles documentaires et `git diff --check`
réussis.

La sélection de **29 scénarios navigateur** a d’abord donné 28 succès et une
expiration dans le test de pagination tardive en erreur de Mes participations.
Son rejeu isolé réussit. Cause de synchronisation identifiée dans le test :
l’attente du titre de page ne garantissait pas la fin de la première lecture ;
le mock de réponse retardée pouvait alors intercepter cette première lecture.
Le test attend désormais le bouton de pagination avant d’installer ce mock.
Les deux variantes retardées (succès/erreur) et les quatre nouveaux scénarios
sont rejoués ensemble : **6 succès**, sans modification ni retrait d’assertion.
Le code applicatif de pagination n’est pas modifié.

Périmètre : Marketplace/Live et documentation canonique. Aucun impact sur
les règles métier, contrats API, persistance, migrations, générateur ou
configuration d’exploitation : ce correctif présente les communes déjà
sélectionnées et réutilise les routes existantes. Pas de changement du statut
de roadmap, ni de modification du portail Animation, du backend ou de Pro.
Vérifications sur fixtures locales ; recette hébergée non exécutée. Aucun
commit, push ou déploiement demandé/effectué pour ce correctif.

## 31 octobre 2026 — iconographie et actions principales du portail Animation

Demande : mieux distinguer les rubriques de Localeo Animation et les actions
principales, face à une accumulation de textes et de boutons. Bases Animation
**69b3ef8**, Projet **fc0b32d**, avec conservation des travaux locaux sur les
modules actifs. Reproduction locale avant correction : l’assertion navigateur
d’un pictogramme de section dans l’assistant échoue avec `0 != 1`. Le menu avait
déjà ses icônes, sans traitement commun dans les espaces de travail.

Le composant partagé `SectionHeading` et sa feuille `section-heading.css`
associent un pictogramme Lucide au titre, avec description et actions éventuelles.
Repères appliqués aux espaces principaux et aux rubriques d’une animation :
assistant, publication, Live, terrain, validations, communication, tirage,
remise, flyer et bilan ; ainsi qu’abonnement, commandes, équipe, support,
imports, catalogue de coffrets, participants, bilans et finance. Les onglets
d’animation reprennent ces repères ; le sélecteur natif mobile reste nommé.
La communication illustre ses trois étapes sans ajouter un encadré supplémentaire.

Sur le tableau de bord, les animations nécessitant une action précèdent les
indicateurs et graphiques. Le bouton contrasté reprend le libellé serveur et sa
destination existante ; sans libellé, il affiche **Ouvrir l’animation**, avec un
nom accessible complet. Les autres actions de progression, création, devis et
invitation reçoivent un repère utile ; actualisation et retours restent
secondaires. Les autorisations, confirmations, gestionnaires de commande et
protections contre les doubles envois sont conservés.

Les icônes décoratives ne dupliquent pas les libellés accessibles ; titres,
identifiants, références de focus et ordre sémantique sont préservés. Le texte
et les actions se replient à petite largeur et à 200 %. La recette a repéré puis
fait corriger le débordement du bouton d’invitation avec son icône et une cible
tactile calculée à 41,25 px au lieu de 44 px dans le tableau de bord. Une marge
de défilement sur le retour commercial évite de rogner son bord et son focus
lors du retour après commande. Aucune assertion réduite ni scénario ignoré.

Preuves locales : **249 tests Node** réussis ; **40 scénarios** intégrés de
tableau de bord et rubriques (1600/390/320 px, texte 200 %), **70 scénarios / 994
assertions** Abonnement, **56 scénarios / 388 assertions** Compte et équipe,
**126 assertions** de récupération/invitation/changement de compte dans
l’application complète, **24 scénarios** de commande, **12 scénarios** de
communication, **8 scénarios / 104 assertions** de support et navigation Flyers
à 1280/320 px. API synthétiques, aucun fournisseur ni environnement opérateur
contacté ; les parcours de lecture et raccourcis ne déclenchent pas de mutation.
Captures bureau et mobile inspectées, dont zoom 200 %. Types, lint, build isolé,
contrôles documentaires et `git diff --check` réussis.

Périmètre de ce correctif : portail Animation et documentation canonique.
Les règles métier, critères fonctionnels, contrats API, migrations,
configuration d’exploitation et générateur de démonstration ne changent pas ;
aucun contrôle backend supplémentaire requis pour ces repères de présentation.
Marketplace/Live public et Pro ne sont pas modifiés par ce correctif. Roadmap
inchangée. Pas de recette hébergée, commit, push ou déploiement effectués.

## 31 octobre 2026 — proposer uniquement les modules non actifs

Demande : dans Abonnement de Localeo Animation, retirer les modules déjà actifs
du choix d'ajout. Bases Animation **69b3ef8**, backend **c1c57b0**, Projet
**fc0b32d**. Reproduction avant correctif : la case d'achat de Chasse au trésor
était présente malgré son droit actif ; le test navigateur échoue avec `1 != 0`.

Le portail filtre désormais **ACHAT_MODULES** avec la projection serveur
`modules_actifs`, toutes origines couvertes. Mes modules reste consultable,
renouvellement et changement de forfait conservent leurs parcours. Une sélection
devenue active après actualisation est supprimée du devis ; si tous les modules
sont actifs, un état vide explique l'absence de choix. L'ancienne API sans ce
champ reste compatible, avec attente explicite de lecture complète des droits
paginés avant de proposer l'ajout.

Le domaine `DroitModule.statut_effectif` reste propriétaire des dates/états.
Le repository émet une liste DISTINCT de codes officiels pour toutes les périodes
de la page ; le service de lecture l'ajoute aux projections simples et paginées.
Aucune règle d'achat/devis, quota, renouvellement, droit acquis ou habilitation
modifiée. Le test SQL observe **10 requêtes** pour 2 comme pour 25 périodes sur
10 000 droits : une lecture groupée supplémentaire, sans N+1. Aucun changement
de schéma SQL ni de données de démonstration ; fixtures navigateur adaptées aux
achats de modules inactifs. La fixture de commerce réelle est alignée sur sa
voisine pour créer `finished_at` de v279, sans affaiblir les assertions.

Preuves locales : **126 tests backend** réussis (PostgreSQL jetable, HTTP,
commerce et domaine), **623 contrôles d'architecture** réussis ; **70 scénarios
navigateur, 994 assertions** réussis à 1280/390/320 px et texte à 200 %. Ces
scénarios couvrent droits actifs hors première page, quatre origines, module
expiré, tous modules actifs, ancienne API paginée, activation pendant la visite,
renouvellement, achat et retours réseau incertains. Types, lint et build isolé
Animation réussis. La revue indépendante ne constate aucun défaut fonctionnel.
Les contrats E41 et E42 sont régénérés avec les générateurs existants depuis
l'export hors ligne ; le contrat embarqué Animation est actualisé. Cet instantané
embarqué était antérieur aux contrats canoniques : sa régénération complète
reprend aussi leurs changements précédents et les métadonnées de validation
du producteur courant, sans modification manuelle des schémas. La suite Node
complète Animation vérifie les consommateurs : **249 tests réussis**, aucun
ignoré, dont le contrat commercial additif. Contrôles des liens et des sources
exportées, ainsi que `git diff --check`, réussis ; captures mobiles inspectées.

Périmètre : backend, portail Animation et documentation canonique. Pas d'impact
fonctionnel sur Live, Marketplace ou Pro ; leurs champs inconnus restent sans
effet. État de roadmap inchangé. Aucun achat réel, commit, push ou déploiement ;
recette sur l'environnement hébergé non exécutée. Livraison : backend puis
portail, sans nouvelle configuration.

## 31 octobre 2026 — Mes lots dans le menu principal Live

Demande utilisateur : sortir **Mes lots** des sous-onglets de Mes participations
et placer son entrée entre **Mes participations** et **Mes communes**. Bases
Marketplace **8204c80**, projet **e730ee0**, avec les travaux locaux conservés.
La reproduction navigateur échoue sur les deux surfaces Live : le menu ne
contient que trois liens, sans Mes lots.

La navigation présente désormais **Accueil / Mes participations / Mes lots /
Mes communes**, avec un pictogramme cadeau pour les lots. La liste possède son
titre **Mes lots** ; cette entrée reste la seule active dans la liste et le
détail d'un bon. Le sous-onglet est retiré du carnet ; sur la surface Animation,
le bandeau devenu redondant avec un seul onglet est supprimé. Les deux rubriques
Coffrets/Participations restent disponibles sur la surface Coffrets. Le dock
conserve sa hauteur mesurée, les safe areas et le retour à la ligne des libellés.

Les URL `/live/lots` et `/live/lots/:id`, les capacités personnelles, le stockage
volontaire et les états/QR des bons restent inchangés. Périmètre : Marketplace
et documentation E73. Aucun impact contrat API, règle domaine, migration,
générateur de démonstration ou configuration d'exploitation : seul l'accès à
une page existante change. Aucun changement des statuts de roadmap ; vérification
locale uniquement, sans commit, push ni déploiement.

Preuves : **18 tests navigateur finaux réussis, aucun ignoré**, sur navigation
des deux surfaces, clavier, accès direct et rechargement, bons sauvegardés,
QR et refus sans capacité, participations distinctes et carnet importé sans
token. Les captures et assertions vérifient les quatre entrées sur une ligne
à 320/390/1280 px ; le texte à 200 % reste lisible et la dernière action ne
passe pas sous le dock. Les 12 tests du carnet et les six tests de navigation/
préférences ont également réussi avant l'ajustement final de répartition du
dock. Le contrôle de mot entier des participations cible désormais le menu
principal, le sous-onglet ayant été retiré. ESLint, contrôle des liens et des
sources exportées, ainsi que `git diff --check`, réussissent (codes de sortie 0).

## 31 octobre 2026 — Live comme espace de jeu local

Retour utilisateur : l'ensemble de Live doit évoquer une animation à vivre et
inciter à participer, au-delà de fiches éditoriales. Base Marketplace **8204c80**,
projet **e730ee0**, avec les correctifs locaux précédents conservés. Le test de
reproduction à 320 px constate que l'action du défi personnel a un ratio de
visibilité nul dans le premier écran, après le grand programme communal.

L'accueil place maintenant la priorité personnelle, puis ses deux suivantes au
maximum, avant le programme public. La carte principale devient un espace de
jeu navy/orange : anneau et étapes restantes contrastés, indicateurs métier
conservés, action de reprise ou récupération au premier plan. Sans priorité,
le rendez-vous communal ouvre l'accueil, avec Flyer, type de jeu, participants
et dotation connus, puis une action publique visible. Les cartes mettent leur
objectif et leur action avant les textes de détail.

Un helper de présentation partagé aligne les types Passeport/Tombola/Chasse de
l'accueil, du catalogue et de la fiche. L'objectif de validations n'est chiffré
que pour un Passeport explicite avec entier positif ; une chasse ne récupère
plus un récit de validations commerçantes provenant d'un ancien champ. Les
cartes continuent d'ouvrir la fiche publique et ses conditions ; elles ne créent
pas d'inscription implicite. Le libellé de participation respecte l'ouverture
serveur des inscriptions.

Le shell Animation reçoit un dock navy avec destination active orange, un
en-tête compact et un fond clair. Les cartes du carnet utilisent ses variables
de surface et d'espacement. Les styles de cartes et de scène sont remplacés
à leur source ; l'habillage de surface est centralisé, avec safe areas, hauteur
de dock mesurée, clavier, texte agrandi et mouvements réduits. Les parcours
Coffrets et les libellés/liens de navigation sont conservés.

Preuves initiales : **15 tests navigateur ciblés réussis** après correction,
incluant reprise visible dans le premier écran, rendez-vous public, 320/390/1280 px,
texte à 200 %, données partielles, erreurs/vide, bon accès personnel et reprise
des anciens accès par lots bornés. **Cinq tests Node réussis** sur présentation,
priorités/progression et transport du tableau de bord. ESLint sur les sources et
tests modifiés réussit. Les revues indépendantes du shell et des projections
publiques ne constatent pas de règle ou d'accès inventé. La campagne transversale
finale réussit : **75 tests navigateur, aucun ignoré**, sur accueil, découverte,
fiches, images, carnet, communes, navigation, préférences et liens personnels.
L'inspection à 200 % conduit à laisser le dock et les compteurs de périodes
revenir à la ligne entre boutons plutôt qu'à couper les mots. **Dix tests ciblés
rejoués passent** sur cet ajustement final ; ils vérifient aussi que la dernière
action reste au-dessus du dock après défilement au bas de la page.

Captures mobile, bureau et texte à 200 % inspectées ; aperçus conservés dans
`tmp/live-play-review/` du Marketplace (fichiers de travail ignorés). Les contrôles
documentaires réussissent : 96 guides, 1 081 liens sans erreur et 130 documents
exportés vérifiés. `git diff --check` passe dans les deux dépôts. Aucun test backend
relancé, ses règles et contrats n'étant pas modifiés.

Impacts : Marketplace/Live et documentation canonique E73. Aucun changement de
règle backend, contrat API, migration, générateur ou configuration : mêmes
objectifs, progressions, inscriptions et accès stockés. Aucune animation en temps
réel, score, classement ou compte à rebours synthétique. Aucun accès au TEST
partagé, commit, push ou déploiement ; recette hébergée non exécutée. L'état global
de l'epic reste inchangé.

## 31 octobre 2026 — fiche publique orientée jeu et défi

Retour utilisateur : une fiche d'animation plus graphique et immersive, orientée
jeux/challenge plutôt qu'éditorial. Base Marketplace **8204c80**, projet **e730ee0**,
avec les correctifs locaux précédents conservés. L'ancien en-tête plaçait le
long descriptif avant l'action et imposait un récit de passages commerçants aux
trois types d'animation. Le test initial constate l'absence du repère **Votre défi**.

La fiche publique présente maintenant le Flyer disponible, le statut, le type
de jeu, l'objectif et l'action autorisée avant les textes détaillés. Le passeport
explicitement identifié affiche son objectif positif configuré ; tombola et
chasse ont des invitations adaptées. Un type ou objectif inconnu reste générique,
sans progression personnelle ni faux zéro. Participants, gagnants et dotation
totale connus sont présentés par nombres et pictogrammes. Les dates, raccourcis
vers lots/adresses/conditions et volets de description/règlement restent lisibles
sur mobile. Les lots et adresses utilisent leurs médias réels, sinon un
pictogramme ; aucune photo de remplacement n'est choisie. La pagination des lots
reste volontaire, avec remplacement de page, retour et reprise après erreur.

Les anciens styles d'introduction et de bénéfice sont retirés de leurs sources,
y compris les surcharges éditoriales. La présentation est regroupée dans le
composant d'entrée de défi et sa feuille dédiée. Les gardes d'inscription restent
dans les parents existants. Lecture anonyme, provenance `source`, récupération
par e-mail, inscriptions multiples, QR et accès personnels sont conservés.

Preuves locales : **28 tests navigateur réussis** sur fiche, variantes, statuts,
images Flyer, inscription sans compte, lots externes, pagination, refus et
récupération. Les tests vérifient 320/390/1280 px, texte à 200 %, objectif connu
ou invalide, valeurs publiques inconnues, absence d'avancement inventé et
conservation du texte complet après ouverture des volets. Le parcours de test
ouvre aussi le volet existant **Lire le règlement complet** avant de vérifier
son texte ; l'assertion de contenu est conservée. Une revue indépendante des
champs et des garde-fous n'identifie pas de blocage ; les trois discriminants
canoniques sont utilisés. **20 scénarios ciblés passent** après le nettoyage des
styles et l'ajout des pictogrammes de lots/adresses ; ce rejeu inclut un nouveau
cas de média réel puis en échec. Au total, **29 scénarios distincts** sont vérifiés.
Trois rejeux à 320/390/1280 px confirment ensuite l'alignement final du bloc défi
et de l'action principale après retrait de leur contrainte de largeur arbitraire.
Captures à 320/390/1280 px et texte à 200 % inspectées. Les contrôles de liens et
de sources exportées réussissent : 96 guides, 1 081 liens sans erreur et
130 documents vérifiés. Aucun test backend relancé, ses règles et contrats
n'ayant pas changé.

Impacts : Marketplace/Live, consommateur public partagé et documentation canonique
E73. Aucun contrat, règle backend, migration, configuration ou générateur modifié :
la fiche présente les projections existantes et ne modifie aucune participation.
Aucun accès au TEST partagé, envoi réel d'e-mail, commit, push ou déploiement.
La recette hébergée reste non exécutée ; l'état global de l'epic ne change pas.

## 31 octobre 2026 — Mes communes : repères graphiques et accès aux animations

Retour utilisateur : rendre la section des communes plus graphique, dans la
continuité du carnet Live. Base Marketplace **8204c80**, projet **e730ee0**, avec
les correctifs locaux précédents conservés. La présentation existante associait
une liste de liens à plusieurs paragraphes, sans compteur ni repère visuel par
commune. Le scénario à 320 px constate l'absence du compteur avant correction.

**Mes communes** affiche maintenant le nombre de communes suivies dans ce
navigateur, un repère de localisation, le nom, le code postal disponible et une
coche de suivi. **Voir les animations** ouvre le contexte public existant ; le
retrait est secondaire, avec un bouton nommé pour la commune concernée. Recherche
et géolocalisation sont regroupées. Les explications de localisation restent
disponibles dans un volet natif. L'en-tête est compact sur mobile ; la liste
passe sur deux colonnes sur bureau. Aucun visuel territorial ni compteur
d'animations n'est inventé. Les styles des communes sont retirés de la feuille
de découverte et regroupés à leur source, sans superposition de correctifs.

Preuves locales : **33 tests navigateur réussis** sur communes, découverte,
navigation et préférences de notifications. Ils couvrent ajout/retrait et
persistance, borne de dix choix, absence de doublon, clavier, noms longs,
320/390/1280 px, texte à 200 %, stockage refusé, recherche vide/en erreur,
géolocalisation volontaire, refus, délai, service indisponible et réponse
tardive. Les coordonnées ne sont pas persistées ; les catégories de notification
et communes partagées restent indépendantes du suivi. **Six tests Node réussis**
sur normalisation, stockage et lectures bornées. ESLint sur les sources et le
nouveau test réussit. **Six scénarios navigateur rejoués passent** après le
compactage final de l'en-tête. Captures mobile, bureau et texte à 200 % inspectées.
Les contrôles documentaires réussissent : 96 guides, 1 081 liens sans erreur,
130 documents exportés vérifiés et `git diff --check` dans les deux dépôts.

Impacts : Marketplace/Live et documentation canonique E73 uniquement. Contrats,
règles backend, migrations, configuration et générateur sans changement : mêmes
API et mêmes données locales. Aucune écriture distante, aucun commit, push ou
déploiement. La recette hébergée n'est pas exécutée et l'état global de l'epic
reste inchangé.

## 31 octobre 2026 — participations regroupées dans leur page dédiée

Retour utilisateur : la section **Mes autres participations** alourdit l'accueil
et doit rejoindre **Mes participations**, en conservant sa présentation graphique.
Base Marketplace **8204c80**, projet **e730ee0**, avec changements locaux de ce
correctif. La cause est locale : l'accueil affichait toutes les pages du tableau
de bord tandis que la page dédiée ne lisait que le carnet de l'appareil.

L'accueil conserve au plus trois priorités et le lien **Toutes mes participations**.
La page dédiée réunit carnet et accès liés à l'installation, dédupliqués par
identifiant de participation, sans fusionner les inscriptions à une même animation.
Elle reprend anneaux, étapes restantes, compteurs à pictogrammes et images Flyer
disponibles, sans illustration de remplacement. Les compteurs du carnet sont
explicitement limités à cet appareil ; ceux des accès distants à la page chargée.
Une progression absente ou incohérente reste sans anneau. Qualification et gain
restent issus du serveur, indépendamment du pourcentage.

La pagination et la liaison explicite des anciens accès sont déplacées avec
leurs bornes existantes : 50 éléments par page, 50 liaisons par action, deux
requêtes simultanées. Sans accès personnel, la récupération demande l'e-mail
d'inscription ; elle ne choisit pas une autre inscription et ne crée aucun QR.
Le cas d'un carnet importé sans token dispose du même parcours. Les composants
de carte et d'anneau sont partagés ; les anciens styles de barre sont retirés.

Preuves locales : **42 tests navigateur réussis**, couvrant accueil limité à
trois priorités, récupération, inscriptions multiples, QR distincts, carnet sans
token, pagination, réponses tardives, liaison bornée, erreurs réseau et stockage,
rendus à 320/390/1280 px et texte agrandi à 200 %. **10 tests Node réussis**, dont
progression inconnue et séparation progression/qualification. ESLint sur les
sources et tests modifiés réussi. Les anciens scénarios de récupération ont été
adaptés à la fiche publique actuelle et au DTO de jeu actuel, en conservant les
assertions e-mail et QR.

L'inspection des captures révèle ensuite un mot « participations » coupé à
320 px : le style des lots imposait trois colonnes même lorsque deux onglets
étaient présents. Une assertion de plage de texte reproduit la coupure avant
correction (deux lignes au lieu d'une). La règle fixe est supprimée ; les onglets
utilisent leur contenu et peuvent revenir à la ligne entre les liens.
**Cinq tests navigateur rejoués réussissent** sur cette correction finale,
notamment le mot entier à 320 px et à 200 %, les QR et les rubriques du carnet.
Captures finales mobile et bureau inspectées. Les contrôles documentaires passent :
96 guides, 1 081 liens locaux, aucune erreur et 130 documents exportés vérifiés.

Impacts : Marketplace/Live et documentation canonique E73. Sans changement de
contrat, règle backend, migration, configuration ou générateur : les projections
existantes sont utilisées et les accès stockés conservés. Aucun appel au TEST
partagé ni envoi réel d'e-mail. Aucun commit, push ou déploiement ; la recette
hébergée reste non exécutée. L'état global de l'epic est inchangé.

## 31 octobre 2026 — Mon Live : priorité au visuel

Retour utilisateur : privilégier le graphique aux longs textes. Sur la base
Marketplace **7d9e0fc** avec les correctifs précédents conservés, le contrôle
navigateur reproduit une image limitée à **130 px** de haut sur mobile, avant
correction. L'ouverture utilise désormais toute la largeur pour l'image Flyer
choisie, avec un titre local compact ; les paragraphes d'ambiance redondants
sont retirés. Aucun visuel de remplacement n'est ajouté.

Participants, gagnants, lots et périodes sont repérés par des pictogrammes
d'interface, avec leurs valeurs et libellés conservés. La progression personnelle
est un anneau chiffré accessible, associé aux étapes validées/restantes. Le
pourcentage ne confère ni qualification ni gain. Les descriptions et conditions
des cartes restent disponibles dans un volet natif **En bref**, sans troncature
ni perte de l'accès à la fiche complète. Les règles d'accès, priorités, communes
et données API restent inchangées. Les styles ont été remplacés à leur source,
notamment la composition du bandeau et la barre devenue anneau.

Preuves locales : première campagne de **39 tests navigateur**, avec **38 succès**
et un défaut de présentation des pictogrammes dans les valeurs numériques à
200 %. Les pictogrammes ont été déplacés dans les libellés ; l'assertion de
nombre sur une seule ligne est conservée. **12 tests ciblés rejoués avec succès**
sur le correctif final : compteurs connus/inconnus et zoom 200 %, clavier,
mouvements réduits, reprise personnelle, rendu 320/390/1280 px, image pleine
largeur, anneau accessible, ouverture/fermeture des descriptions et conditions,
panne et programme vide. Captures inspectées dans les sorties Playwright locales.
ESLint sur `src` et les tests modifiés, contrôles de liens et **130 documents
exportés** réussis. Aucun test backend relancé : ses règles et contrats n'ont
pas changé pour ce complément de présentation.

Impacts : Marketplace/Live et spécification graphique E73. Aucun changement
backend, contrat, migration, générateur ou configuration : seules les projections
existantes sont présentées autrement. Aucun accès au TEST partagé, commit, push
ou déploiement ; vérification hébergée non exécutée.

## 31 octobre 2026 — un accueil Mon Live ancré dans la vie des communes

Retour utilisateur : accueil trop institutionnel et figé, activité communale
insuffisamment mise en avant. Base Marketplace **7d9e0fc**, correctif Flyer et
autres travaux locaux conservés. L'ancien écran empilait d'abord participations,
messages de service et informations du carnet avant la découverte publique.
Le test de reproduction constate l'absence de l'ouverture locale attendue avant
correction ; les règles de priorisation ne sont pas remises en cause.

Correction de présentation : accroche contextualisée par les communes réellement
consultées, animation en cours à rejoindre (sinon prochaine), image personnalisée
du Flyer seule, nombre public de participants de cette animation. Les accès
**En ce moment** et **Prochainement** indiquent les nombres de l'aperçu chargé ;
la pagination et les erreurs rendent explicitement cet aperçu partiel. Aucun
compteur d'habitants uniques, nouvelle activité récente ou temps réel n'est
inventé. Les communes suivies ne sont pas modifiées par la consultation.

Le raccourci **Mes défis à reprendre** est visible dès l'en-tête lorsque des
priorités existent. Il rejoint la première priorité et ses deux suivantes,
avant les cartes publiques ; les autres informations du carnet suivent le
programme. Les indicateurs, progressions, liens personnels et limites de page
restent ceux des projections existantes. **Actualiser** recharge aussi le
catalogue, sans requête supplémentaire par carte ni parcours exhaustif des
pages. L'indisponibilité propose une relance ; elle ne se confond plus avec le
programme vide. Les mouvements d'entrée et de survol sont désactivés lorsque
la réduction des animations est demandée.

La revue indépendante a fait ajouter la reprise directe sur mobile, distinguer
la panne du vide et porter la marge de défilement sur les titres réellement
ciblés par les ancres. Les styles de l'en-tête et de la priorité ont été modifiés
à leur source, sans nouvelle couche de surcharge ; le bloc local possède sa
feuille de style dédiée.

Preuves finales : **39 tests Playwright réussis**, dont six nouveaux scénarios
sur l'accueil communal à 320/390/1280 px, texte agrandi à 200 %, navigation par
ancres sans masquage sous l'en-tête, actualisation du programme, aperçu partiel,
absence d'image et reprise après panne. Les parcours existants de tri personnel,
pagination bornée, réponses tardives, accès exacts, sélection des communes,
préférences et illustrations Flyer restent verts. Le test de réponses retardées
libère désormais ses requêtes en `finally`, sans changer ses assertions ; une
exécution initiale bloquée a été interrompue avant rejeu ciblé puis complet.
**10 tests Node** de tableau de bord/communes réussis ; ESLint sur `src` et les
trois fichiers de tests concernés réussi. Le runner navigateur reconstruit
l'application hors configuration privée ; captures inspectées dans
`localeo-marketplace/test-results/desktop/`. Liens documentaires et **130 sources
exportées** vérifiés sans erreur.

Impacts : Marketplace/Live et [spécification E73-HOME-01/06](localeo-live-entree-unique.md#critères-et-preuves-attendues).
Backend, contrats API, règles métier, migrations, générateur, DNS et configuration
sans changement pour ce correctif : les données publiques et personnelles
existantes sont réutilisées. Aucun accès au TEST partagé, notification réelle,
commit, push ou déploiement ; recette hébergée non exécutée.

## 31 octobre 2026 — illustration du Flyer dans les blocs Live

Attendu : la présentation d'une animation utilise l'image personnalisée choisie
dans **Flyer**, sinon aucune illustration. Reproduction locale sur marketplace
**7d9e0fc** et backend **586a51f**, avec les travaux précédents conservés : le test
navigateur attend l'image Flyer mais reçoit une vignette éditoriale historique.
Sans vignette, Live choisissait une photo Localeo de remplacement. En amont,
`visuel_url` annonçait des assets génériques ou l'aperçu généré du flyer, au lieu
de l'illustration personnalisée.

Correction : les cartes de découverte et l'en-tête de fiche Live consomment
strictement `visuel_url`, sans alias historique ni illustration de remplacement.
L'absence d'image ou l'échec de chargement supprime le bloc visuel ; titre,
statut, dates et inscription restent lisibles, sans colonne vide. Le backend
projette l'illustration personnalisée du Flyer, chargée par une route dédiée
publique sans cache, après contrôle de visibilité et sélection du dernier
document du type exact rattaché à l'animation. Les archives sont exclues après
classement pour ne pas restaurer une ancienne image ; taille et SHA256 sont
contrôlés hors transaction SQL. Le chemin historique `/visuel`, les illustrations
de jeu et le rendu PDF gardent leurs règles existantes.

Preuves frontend : test de reproduction en échec avant correction, puis **11
tests Playwright réussis**, dont six cas à 320/1280 px (image choisie, absente,
introuvable), parcours découverte vers fiche, inscription accessible, aucune
requête vers les illustrations historiques, aucun débordement et contenu sur
toute la largeur sans image. Non-régression des indicateurs publics et de
l'inscription sans compte incluse ; captures inspectées dans
`localeo-marketplace/test-results/desktop/`. **10 tests Node** de carnet,
tableau de bord et transport réussis. ESLint sur `src` et le nouveau test réussi ;
`npm run lint` global bloqué par des répertoires de sortie temporaires refusés
par Windows (`EPERM`), sans modification de leurs droits.

Preuves backend : **37 tests application/API/OpenAPI/sécurité réussis** et
**22 tests PostgreSQL isolés réussis**, sans échec ni skip. Les six nouveaux cas
SQL couvrent le dépôt réel, le remplacement et le retrait, ainsi que les refus
sur document archivé, mauvais scope, catégorie, MIME ou type documentaire.
Les tests existants d'illustration Flyer et de provenance des couvertures de
chasse restent verts. Le cluster local de test a été arrêté après exécution.
Les **623 contrôles d'architecture** réussissent sur le correctif final.
La revue indépendante a fait aligner le tri sur la sélection canonique du Flyer
(`updated_at` décroissant), sans autre défaut établi. Une animation devenue
non publique peut conserver une URL dans sa projection personnelle ; le binaire
public est alors refusé et Live masque l'image, sans exposer de document privé.

Impacts : backend, Marketplace/Live, spécifications Flyer/Live et contrats
OpenAPI canoniques E41/E42. Aucun schéma de données ni migration, nouveau droit,
paramètre ou champ obligatoire ; le générateur peut toujours produire une
animation sans image personnalisée. Aucun accès aux données TEST, aucun commit,
push ni déploiement. La recette hébergée reste à exécuter après livraison du
backend puis de Live selon le [guide d'exploitation](../../exploitation/technique/configurer-epic-73.md).

## 31 octobre 2026 — 403 sur le lien d'édition d'une offre

Signalement : `/admin/offre-plateforme-orm/edit/9bfa4730-176d-4f14-9ffa-052add702709`
renvoie 403 malgré une connexion administrateur. Base backend **586a51f** et
modifications locales précédentes conservées. Cause démontrée dans les sources :
`OffrePlateformeAdmin` interdit volontairement l'édition ORM depuis le catalogue
versionné, mais **Offres et tarifs** proposait encore un lien « Modifier » vers
cette édition interdite. Le test de rendu a reproduit ce lien avant correction.
La session distante et l'existence de l'offre signalée n'ont pas été consultées.

Correction : **Publier une nouvelle version** ouvre le catalogue commercial
existant avec `offre_id`. Le choix de la commune et la pagination conservent
l'offre cible ; seule cette offre est présentée pour l'édition. La nouvelle
version reste soumise à l'action autorisée par le serveur, au motif, à la
confirmation, à la version attendue et à l'idempotence existants. L'interface
précise la portée des futurs achats dans toutes les communes. L'ancien GET
d'édition redirige en 303 avec `no-store` après contrôle ADMIN historique et
validation de l'UUID. Aucune écriture ORM n'est réactivée ; les versions et
conditions acquises restent protégées. Une offre absente ou non publiée est
signalée sans publication implicite.

Preuves locales : **4 tests Python ciblés réussis** (rendu corrigé, interdictions
ORM conservées, redirection ADMIN, refus anonyme/profil métier/compte nominatif,
identifiant invalide et POST non redirigé, API de création protégée), **623
contrôles d'architecture réussis**. `node tests/browser/offre-version-navigation.cjs` :
**3 parcours** à 1280/320 px et texte 200 %, depuis la liste vers la publication
ciblée en seconde page, aucun POST avant confirmation, même offre/version dans
la commande et refus lecteur. Le libellé accessible du sélecteur Commune est
explicite. `node tests/browser/epic73-modules-erp.cjs` réussit à 320/1280 px :
versions, octrois, conflits, remboursements et dates Paris conservés.
Captures dans `.artifacts/offres-catalogue/` du backend.

Impacts : backend ERP et [parcours canonique du catalogue](modules-souscriptions-import-communication.md#3-catalogue-et-droits-acquis).
Pas de changement de règle métier, contrat de publication, calcul de droits,
migration, configuration ou générateur : le correctif relie la lecture et le
formulaire de publication déjà existants. Aucune donnée, offre réelle ou
souscription modifiée ; recette hébergée non exécutée. Aucun commit, push ou
déploiement effectué.

## 31 octobre 2026 — parcours du gestionnaire interne ERP

Retour utilisateur : simplifier la nouvelle souscription (partenaire, droits,
accès), l'exploitation des animations en cours et les demandes de support.
Base backend **586a51f**, travaux locaux des autres dépôts conservés. Les
reproductions ont montré un ordre de formulaire incohérent, des actions utiles
peu visibles et une réponse support peu distinguée des opérations internes.

Correction de présentation, sans modification des règles métier :

- Référencement en quatre étapes ordonnées, contenu du forfait lisible, revue
  et confirmation explicites avant création. Modification de saisie : revue
  invalidée. Dossier créé directement accessible, gratuité et paiement attendu
  distingués, invitation toujours conditionnée par l'activation.
- Suivi des animations : filtres prioritaires et raccourci « En cours »,
  conservation du contexte, pilotage avant les lots et liens vers les consoles
  autorisées. Aucun indicateur de dates d'animation absent de l'API n'est inventé.
- Support : demandes à traiter et échéances repérables, réponse principale,
  notes privées et suivi interne séparés, messages titrés et focalisés. Les
  compteurs indiquent leur portée limitée à la page. La revue a reproduit puis
  corrigé une demande clôturée comptée en retard ouvert : son détail présente
  désormais l'historique, sans nouvelle échéance de réponse.

Preuves locales :

- `tests/infrastructure/admin/test_referencement_animation_ux.py` : deux
  reproductions rouges avant correction, vertes après ; tests API/navigation
  ciblés conservés. `tests/browser/gestionnaire-souscription-ux.cjs` :
  **63 contrôles** à 1280/320 px et texte 200 %, sans création à la consultation.
  **17 tests Python** ciblés réussis ; régressions checkout, équipes et accès
  internes réussies. Navigation ERP : **26 contrôles** réussis.
- `tests/browser/epic73-operations-ux.cjs`, suivi produits, exploitation et
  préparation : **26 scénarios** réussis ; profils gestionnaire, lecture et
  Support, 1280/320 px et texte 200 %, droits et contexte vérifiés.
- Les deux bancs `epic73-support-organisations*.cjs` passent, dont demande
  clôturée sans première réponse avec ancien indicateur de retard. Réponse,
  note privée, conflit, reçu incertain, relecture et rejeu explicite avec même
  clé/corps vérifiés. **12 tests Node et 14 tests API/navigation** réussis.
- Contrôles backend obligatoires : **623 tests** d'architecture, classes du
  domaine et couverture des use cases réussis. Captures locales dans
  `.artifacts/gestionnaire-ux/`, `tmp/operations-ux-captures/` et
  `.artifacts/e73-support-organisations-ux/` du backend.

Impacts : backend ERP et [présentation canonique des parcours](perimetres-parcours-saas.md#45-parcours-du-gestionnaire-interne-erp).
Contrats, domaine, permissions, migrations et générateur sans impact pour cette
réorganisation : seules les actions existantes sont présentées différemment.
CSRF, version, idempotence, confirmation et résultats incertains conservés.
Styles corrigés à leur source et limités à ces écrans. Recette hébergée non
exécutée ; aucun compte, invitation ou paiement réel créé.

## 31 octobre 2026 — forfait Premium ajouté après confirmation des conditions

Cause reproduite : `v215` et le catalogue de références ne définissaient que
Découverte et Essentielle. L'utilisateur confirme **1 490 € HT, 12 mois,
animations illimitées, accompagnement par défaut et aucun module payant inclus**.
Le modèle retenu est l'accompagnement standard de la plateforme autonome,
sans nouvelle prestation clé en main. Les [conditions canoniques](modules-souscriptions-import-communication.md#catalogue-initial-et-unités)
et la présentation historique E47 sont actualisées, sans changer les statuts.

Depuis `v265`, le portail lit `versions_catalogue_modules` : une offre historique
seule ne suffit pas. La nouvelle migration **v285** ajoute donc Premium aux
deux sources et les références incluent ses conditions. Elle ne réécrit aucune
vente acquise ni version publiée ; une offre personnalisée, inactive ou retirée
est préservée. La publication générique après création ERP/provisionnement reste
un sujet distinct ; cette correction publie uniquement Premium.

Preuves locales :

- Référence absente : test rouge avant correction ; **48 tests de références**
  réussis ensuite, dont prix, durée, quota et absence des trois modules payants.
- **6 tests PostgreSQL isolés** réussis : publication effective par le service
  de catalogue, idempotence, préservation des conditions acquises et des offres
  existantes/personnalisées/inactives/retirées. Devis réel de renouvellement :
  149 000 centimes HT, 178 800 TTC sous TVA synthétique 20 %, une seule ligne
  forfait, 12 mois et aucun module ; aucun droit activé par le seul devis.
- Portail Animation : **4 scénarios navigateur, 52 assertions**, à 1280/390/320 px
  et texte 200 %. Premium apparaît depuis le catalogue serveur, la demande de
  devis porte son code sans module et aucune commande n'est confirmée sans
  consentement. Le prix est calculé côté domaine, pas dans le navigateur.
- Revue indépendante de la migration et des invariants : aucun écart bloquant.
- Contrat HTTP du consommateur : **2 tests** réussis. Documentation finale :
  **98 guides, 1 158 liens**, aucune erreur ; **130 sources exportées**
  vérifiées, `git diff --check` réussi dans les trois dépôts modifiés.
  Le serveur PostgreSQL jetable a été arrêté après les vérifications.

Impacts : références et migration backend ; spécifications et exploitation ;
tests du consommateur Animation. Aucun nouveau contrat, droit de module,
paramètre d'environnement ou ajustement du générateur nécessaire : le forfait
réutilise les capacités standard existantes. Les anciennes migrations restent
inchangées. Migration préparée et vérifiée localement uniquement ; **TEST non
migré vers v285**, aucun fournisseur de paiement sollicité. Aucun commit, push
ou déploiement effectué pour ces deux correctifs.

## 31 octobre 2026 — hiérarchie de Compte et équipe

Retour utilisateur : actions difficiles à hiérarchiser. Base Animation
**4ef51b2** avec les autres modifications locales conservées. Reproduction dans
le navigateur : la rubrique export/fermeture précédait les collaborateurs et
le bouton d’invitation ; les trois champs de mot de passe restaient toujours
ouverts, et la page était centrée sous un plafond `max-w-5xl`. Le nouveau
contrôle d’ordre échouait avant correction pour cette raison.

Correction : équipe courante en premier et invitation principale dès son
en-tête ; actualisation et modification d’un accès secondaires. Collaborateurs
et invitations sont séparés. Un transfert à suivre remonte avant les listes,
y compris pour son successeur non responsable. Les accès rapides **Équipe**,
**Mes organisations** et **Mon compte** placent le focus dans leur section sans
changer le contexte. L’organisation courante est nommée et les autres disposent
d’une ouverture explicite. Mot de passe et opérations sensibles sont à la
demande ; les composants restent montés au repli pour préserver leur état.

Saisies et confirmations s’ouvrent avant les listes, avec focus et défilement.
Annuler rend le focus au déclencheur sans écriture ; une confirmation de
révocation masque la saisie concurrente. Les retours d’équipe réutilisent le
message contrasté commun à Abonnement ; ils rappellent qu’une invitation ou une
proposition de transfert attend l’acceptation de son destinataire. La revue indépendante a relevé un nom
accessible qui omettait « Ouvrir cette organisation » : il inclut désormais
ce libellé visible, le nom de l’organisation et le rôle. Les deux contrôles de
changement d’organisation dans l’application ont été adaptés et rejoués.

Preuves locales :

- `node tests/browser/organisation-access.mjs` : **56 scénarios, 388 assertions**,
  1280/390/320 px et texte à 200 %. Ordre invitation/opérations sensibles,
  invitation, lecture seule, édition, révocation d’autrui/de soi, renvoi/révocation
  d’invitation, acceptation du transfert par le successeur, annulations sans
  mutation, focus clavier, pagination indépendante, mot de passe et reprise
  après réponse perdue avec corps et clé identiques. Le repli des opérations
  sensibles conserve la confirmation d’export sans envoyer de commande.
- `node tests/browser/account-app.mjs` : **16 parcours, 126 assertions**,
  application réelle à 1280/320 px, largeur du contenu, absence de lectures
  métier pour identité seule, acceptation d’invitation, changement de contexte,
  récupération/changement du mot de passe et reconnexion, déconnexion à réessayer.
- `node tests/browser/reversibilite-catalogue.mjs` : **12 scénarios,
  100 assertions**, export et reprise incertaine, téléchargement privé, fermeture
  accompagnée, refus et catalogue. Aucun fournisseur réel sollicité.
- **244 tests Node réussis**, aucun ignoré ; types, lint, builds application et
  PWA isolés réussis, sans environnement opérateur. Captures dans
  `tmp/organisation-access/` et `tmp/generation-browser-dist/` du dépôt Animation ;
  bureau, mobile et zoom inspectés.
- Revue indépendante : droits/actions serveur, identité seule, accès du
  successeur, montage persistant, version et clé de commande, pagination et
  annulation préservés. Aucun changement des invariants du domaine
  `identite_acces` ou de la réversibilité.
- Documentation : **96 guides, 1100 liens**, aucune erreur ; **130 sources
  exportées** vérifiées et `git diff --check` réussi dans les deux dépôts.

Impacts : Animation et documentation canonique uniquement ;
[présentation du parcours](perimetres-parcours-saas.md#44-présentation-de-compte-et-équipe)
actualisée. Aucun contrat, calcul de droits, migration, générateur, donnée ou
paramètre d’exploitation modifié : la correction organise les actions existantes
et conserve leurs contrôles serveur. Styles corrigés dans le composant, sans
nouvelle surcharge CSS. État de l’epic inchangé ; aucun email ou changement
d’accès réel, commit, push ou déploiement effectué. Recette hébergée non exécutée.

## 31 octobre 2026 — hiérarchie et confirmations de la page Abonnement

Retour utilisateur : actions sans hiérarchie et confirmations peu lisibles.
Base Animation **4ef51b2**, avec les autres travaux locaux conservés. Cause
observée dans le navigateur : renouvellement et facturation étaient placés
après tous les droits et usages, dans la même rangée de boutons secondaires ;
les messages de confirmation n’avaient ni mise en évidence ni déplacement du
focus. Le bouton d’arrêt à échéance suggérait une démarche inutile en l’absence
de renouvellement automatique. Le test ciblé échouait bien sur sa présence.

Correction locale : résumé forfait/état/échéance en tête, renouvellement
principal, ajout de modules et changement de forfait secondaires. Modules acquis,
usages, catalogue, facturation et commandes sont séparés. Le devis remplace le
choix pendant sa revue ; l’acceptation des conditions et le total TTC sont
repérables. Les confirmations/erreurs sont titrées, contrastées, annoncées et
ramenées dans la zone visible avec focus. Facturation et demande de remboursement
peuvent être annulées sans écriture ; la demande de remboursement reste distincte
de sa décision et de son exécution. Le paiement est l’action principale du suivi
de commande, sans activation déduite du retour navigateur. Les notifications
antérieures sont effacées lors d’une nouvelle vérification explicite.

Le portail explique l’expiration sans renouvellement automatique et retire le
bouton d’arrêt. Les anciennes demandes restent affichées. La clarification est
dans [la spécification commerciale](modules-souscriptions-import-communication.md#5-achat-renouvellement-facturation-et-remboursement)
et **RM-07-05**, dont la numérotation et les preuves historiques sont conservées.
Le contrat serveur `/arret` n’est pas retiré. Les invariants restent dans le
domaine `abonnements_plateforme` ; aucun calcul de montant, droit ou transition
n’a été ajouté à l’interface.

Preuves locales :

- `node tests/browser/modules.mjs` : **52 scénarios intégrés, 784 assertions**,
  à 1280/390/320 px et texte 200 %. Achat, renouvellement actif/expiré, seuls
  modules achetés précochés, changement de forfait, facturation initiale/modifiée,
  annulation sans écriture, remboursement, ancien arrêt lisible, période future,
  lecteur, indisponibilité, conflit, pagination et compteur incertain. Devis et
  confirmations visibles/focalisés ; commande au clavier et aucune écriture
  avant confirmation. Retours réseau perdus et reprise avec la même clé vérifiés.
  Quatre rejeux ciblés Achat (**128 assertions**) ajoutent un contrôle du cadrage
  complet de la confirmation de paiement dans la zone de contenu de l’application,
  à chacune des quatre tailles/variantes, au-delà du seul focus.
- `node tests/browser/commercial-order-ux.mjs` : **24 scénarios** dans le
  composant réel avec API synthétique : paiement/remboursement, focus et annulation,
  refus des actions serveur/Achat, lien non HTTPS absent et reprise idempotente.
  Un manque de largeur à 320 px/200 % a été reproduit puis corrigé à la source :
  confirmation empilée avec largeur bornée et totaux en colonne. Contrôle du
  débordement dans le panneau, pas seulement dans la fenêtre.
- **244 tests Node réussis**, aucun ignoré ; TypeScript et lint réussis.
  Builds application et PWA isolés réussis, sans environnement opérateur ni
  fournisseur de paiement. Captures dans `tmp/modules-browser/` et
  `tmp/commercial-order-ux/` du dépôt Animation ; bureau/mobile/zoom inspectés.
- Revue indépendante : autorisation Achat et actions serveur, versions,
  acceptation, conditions de renouvellement et reprise incertaine préservées.
- Documentation : **97 guides, 1133 liens, aucune erreur**, **130 sources
  exportées** vérifiées ; `git diff --check` réussi dans les deux dépôts.

Impacts : Animation et documentation canonique uniquement. Pas de contrat,
backend, migration, générateur, donnée ni configuration d’exploitation à changer :
il s’agit de présentation des parcours existants, avec compatibilité des anciens
arrêts. Les styles sont corrigés dans les composants, sans surcharge CSS ajoutée.
État de l’epic inchangé. Aucune validation sur le site hébergé, aucun paiement
réel, commit, push ou déploiement effectué pour ce correctif.

## 31 octobre 2026 — correctif d’affichage de Localeo Animation

Retour utilisateur : espaces centrés et trop étroits dans neuf rubriques,
avertissements de l’assistant tardifs et action suivante peu accessible.
Base Animation **4ef51b2**, avec les modifications locales ci-dessous ; état de
l’epic inchangé. Les preuves de migration TEST de la section suivante sont
conservées et ne valent pas déploiement de ce correctif frontend.

Cause reproduite : à 1600 px, le conteneur Assistant occupait **960 px sur
1390 disponibles**, avec décalage de 215 px. Communication était plafonnée à
1080 px sur un écran de 1920 px. Les contraintes `mx-auto max-w-*` étaient dans
les composants. Elles sont retirées à leur source, sans ajout ni surcharge de
fichier CSS ; les champs, dialogues et aperçus conservent leurs bornes utiles.
La correction couvre Assistant, Live et ses événements, Préparation terrain,
Validations, Communication, Tirage/Gains libres et leur détail, Flyer et Bilan.
Les variantes Coffrets, déjà en pleine largeur, sont conservées.

L’assistant présente d’abord erreurs et avertissements, puis les étapes à faire ;
les étapes vérifiées sont repliables. La barre **Action suivante** reste accessible
depuis les rubriques et ouvre le parcours existant, avec focus et défilement vers
le début utile. La clôture conserve son aperçu, ses droits et sa confirmation.
La communication présente brouillon → destinataires → confirmation, avec action
de création en tête, conditions à la demande et refus visibles. Le lien **Voir
Mes modules** ouvre `/abonnement` seulement depuis la liste sans brouillon ;
aucun achat ni activation ne se déclenche.

Preuves locales :

- **244 tests Node réussis**, aucun ignoré ; TypeScript et lint réussis.
- **32 parcours navigateur** dans `animation-workspace-ux.mjs` : huit rubriques,
  1600/390/320 px et 320 px avec texte 200 %, hauteur 740 px. Largeur réelle,
  alignement, ordre des alertes, contenu du Flyer, absence d’écriture et visibilité
  complète du bouton avant clic après défilement. Le titre de la rubrique cible
  reste visible après navigation ; le test ne se repose pas sur l’auto-scroll du
  clic Playwright. Une troncature du CTA au zoom a été reproduite puis corrigée
  dans le bouton, avec libellé repliable.
- **12 scénarios UX Communication** à 1920/390/320 px, module actif/absent,
  autorisation manquante et période fermée ; lien vers les modules seulement
  depuis la liste et aucune écriture API.
- Régressions Communication : **36 scénarios, 684 assertions** ; Assistant :
  deux scénarios mobile/bureau ; Exploitation : deux parcours complets à
  1280/390 px, correction/retrait/clôture, refus et reprise du même reçu.
  Préparation terrain à 1280/390 px et navigation Flyer à 1280/320 px réussies.
  Bons numériques : **12 scénarios, 116 assertions** ; ce banc signale des
  sélecteurs synthétiques non simulés, renvoyés en 404, sans requête fournisseur
  ni erreur JavaScript. Leur couverture propre reste celle des tests de contrats.
- Build application et build PWA isolés réussis, sans fichier d’environnement
  opérateur. Captures dans `tmp/animation-workspace-ux/` et `tmp/communication-ux/`
  du dépôt Animation ; captures bureau, mobile et zoom inspectées.

Deux adaptations de bancs ont été nécessaires : le test juridique isolé ne
simulait pas le titre d’environnement déjà importé par la page ; le scénario
Exploitation attendait un ancien libellé de validation et ignorait le passage
actuel vers Commerces. Ces écarts sont constatés dans le HEAD initial ; les
assertions métier sont conservées, avec retour explicite vers Parcours et DTO
terrain simulé. La revue indépendante a fait corriger le défilement mobile réel
et confirme la conservation des droits et confirmations.

Le skill `localeo-corriger` précise désormais la simplicité des IHM Animation,
la priorité des alertes/actions et la correction des styles à leur source.
Sa validation `quick_validate.py` réussit, avec PyYAML chargé depuis un
répertoire temporaire isolé. Contrôles documentaires : **96 guides, 1098 liens,
aucune erreur**, **130 sources exportées** vérifiées et `git diff --check` réussi.
Impacts : projet et Animation uniquement ; aucun contrat, backend, schéma,
générateur ou paramètre d’exploitation modifié par ce correctif visuel.
La recette hébergée reste à effectuer après livraison. Aucun commit, push ou
déploiement effectué pour ce correctif.

## 31 octobre 2026 — migration du TEST partagé en v284

Migration demandée et exécutée sur la cible du profil privé backend `.env.test`,
initialement en v283. Le runner officiel a confirmé puis appliqué uniquement
`v284_e73_priorites_rappels_live.sql`, depuis backend `586a51f`, avec checksum
`d1242486cf1cf15eef4e8104aca93582f9444ec954b17d1e7b8f48df00140f61`.
Une seconde simulation ne trouve plus aucune migration en attente.

Sauvegarde PostgreSQL complète créée avant l'action : **54 935 984 octets**,
archive intégralement relue par `pg_restore` sans connexion à une base, sans
restauration en place. Archive, empreinte SHA-256 et reçus avant/après conservés
hors Git dans le backend :
`demonstrations/prive/operations/migration-v284-test-20261031T082158Z-5a702630/`.

Les trois nouvelles tables, trois index valides, référence nullable au token,
clé étrangère `ON DELETE SET NULL` et curseur initial sont vérifiés en SQL.
Aucun token historique déduit. Les effectifs installations, suivis, notifications
et participants sont identiques avant/après.

Contrôles HTTP sur `https://test-backoffice.localeo.city` : `/sante` **200**,
version **1.0.0+586a51f** ; readiness protégée **READY**, **134 contrôles**, aucun
objet manquant ; configuration publique Live **200** et catalogue public borné
à un résultat **200**. Aucun redémarrage n'a été nécessaire. Les préférences et
les traitements de rappel n'ont pas été activés par cette opération ; la recette
sur appareils et la réception réelle des Web Push restent distinctes.

## Accueil et rappels du 30 octobre 2026 — E73-EVO-LIVE-ACCUEIL-RAPPELS

Demande : un accueil personnel mobile donnant priorité aux participations presque
terminées ou bientôt échues, et deux rappels Web Push facultatifs.
Les [critères et contrats](localeo-live-entree-unique.md) complètent E73 ; son
statut global reste **En cours**. Bases Git : projet `55ef32a`, backend `baa559c`,
Marketplace `feb5d0e`, avec les modifications locales de cette évolution.
Réalisation enregistrée dans backend `586a51f` et Marketplace `7d9e0fc`.

L'accueil **Mon Live** conserve `/live/decouvrir`, la découverte publique et le
carnet existant. Les indicateurs proviennent du domaine ; l'interface ne déduit
ni qualification ni gain. La première priorité, les deux suivantes et les autres
participations se limitent à la page chargée, au plus 50 éléments ; les pages se
remplacent, avec état partiel explicite. Le lien personnel retrouve l'identifiant
exact du carnet, sans substituer le token d'une autre participation.

Les préférences `RAPPEL_PRESQUE_TERMINE` et `RAPPEL_FIN_PROCHE` sont indépendantes
et désactivées par défaut. La première exige une étape restante pour le Push ;
le seuil de 80 % concerne uniquement l'accueil. La seconde utilise l'échéance
effective dans les 72 heures. Préparation et transport revalident les droits et
états ; les réservations durables empêchent le réarmement par purge de l'inbox.
Une réservation annulée avant livraison reste consommée : aucun envoi effectif
ni réception ne peut être déduit du seul compteur de préparation.

| Critères | Preuves locales exécutées |
| --- | --- |
| E73-HOME-01/03 | Parcours navigateur mobile/bureau, visiteurs et carnet, ordre stable et entrées distinctes ; trois pages/150 ressources, au plus 50 cartes rendues. |
| E73-HOME-02 | Politique pure et tests dédiés : commencement, 80 %, une étape, 72 h, borne exacte de fin, inconnus et états terminaux ; régressions du moteur et des projections. |
| E73-HOME-04 | Tests API et transport réel du client : secret en en-tête, refus croisé, no-store, annulation ; ancien backend et erreur réseau explicites. PostgreSQL : token exact, expiré, révoqué, absent ou supprimé. |
| E73-HOME-05 | Navigateur : reprise de l'entrée exacte, absence sans substitution, actualisation explicite des accès avec refus partiels ; régressions carnet et Coffrets. |
| E73-HOME-06 | Captures inspectées à 320 px et texte agrandi à 200 % ; tests 320/390/1280 px, Tab puis Entrée vers le bon accès et cibles tactiles. Styles calculés sous mouvements réduits : transition de 0,2 s ramenée à 0,01 ms par la règle globale existante. |
| E73-ALERTE-01 | API, domaine et navigateur : défaut false, opt-ins indépendants, retrait, conservation des catégories/communes omises par un ancien client ; aucune demande automatique de permission. |
| E73-ALERTE-02 | Une étape, échéance effective, fusion des motifs et digest multi-participations ; texte de date en heure de Paris, été/hiver. |
| E73-ALERTE-03 | PostgreSQL : migration rejouable, deux workers concurrents, réservation unique, rollback et purge de l'inbox sans réarmement. |
| E73-ALERTE-04 | Domaine, application et worker simulé : fenêtre Paris 09–20, été/hiver, attente, préférence retirée et revalidation avant transport. |
| E73-ALERTE-05 | Lot borné et curseur durable, simulation et transport fournisseur simulé ; test SQL de pagination 50+5 et lectures groupées. |

Résultats vérifiés, sans additionner les suites qui se recouvrent :

- **786 tests backend réussis sur les sources figées** dans la passe finale
  unifiée : architecture et recensements des classes/cas d'usage, nouveaux
  domaine/application/API, registre démo, moteur/projections et régressions
  Web Push, catégories, notifications Coffrets/Animation, schema readiness,
  anciennes API et UI Live, inscription et notifications d'actualités.
- **11 cas PostgreSQL réussis**, aucun ignoré, dans
  `test_rappels_live_postgres_e73.py`, avec PostgreSQL 18 jetable local. La
  migration finale est rejouée deux fois et les deux index de clés étrangères
  sont introspectés. Après regroupement des contextes : **12 SELECT
  pour 1, 10 et 50 animations distinctes**, préparation active ou inactive.
  Tests de parité avec la lecture ordinaire et pagination inclus ; ce cas ne
  prouve pas la capacité ou la latence d'une population hébergée en charge mixte.
- **129 tests frontend `test:security` réussis**, aucun ignoré. Les contrôles
  transport du tableau de bord et helpers de tri/progression y sont inclus.
- **49 scénarios navigateur distincts réussis** au fil des lots, dont quatorze
  nouveaux. Passe finale de quatorze scénarios réussie après correction de la
  pagination et des réponses tardives pendant une actualisation ; les échecs intermédiaires d'assertions UI ont été corrigés et
  rejoués. Build PWA isolé et ESLint sur sources/tests/scripts/configuration
  réussis. Le lint global reste empêché par un refus local `EPERM` dans
  `output/bum-politique/pytest-approval-1` ; aucune permission n'a été changée.

Les nouveaux registres suivent le remplacement/restauration du générateur.
**14 tests du registre réussis**, dont conservation des réservations après purge
de l'inbox et restauration des dépendances, inclus dans les 786 tests.
Le runner complet de compatibilité a exécuté dix scénarios : **neuf réussis**,
dont dump, installation, échec injecté, reset après changement de schéma et
restauration exacte ; le dixième a échoué uniquement sur la comparaison des
empreintes sources, un fichier API ayant été édité pendant son exécution.
Après gel de `app/templates/sql` et application de la migration finale sur le
builder jetable, ce scénario complet a été **rejoué avec succès** (157,74 s),
sans affaiblir l'assertion. Les dix scénarios disposent donc d'une réussite,
obtenue en deux passes. Les sept avertissements du premier passage et celui du
rejeu concernent la réflexion SQLAlchemy `dialect_options`, sans échec de lecture
ou de restauration. Les sorties sont dans les répertoires `tmp/live-rappels-demo-*`
du backend et les captures dans `test-results/live-game` de Marketplace.

La revue indépendante des contrats a conduit à lier le token exact, préserver
les préférences omises par un ancien client, revalider chaque abonnement avant
transport et conserver un tag stable. Sa dernière lecture ne relève plus de
réserve. Les lectures de contexte sont groupées entre animations et l'indicateur
d'accès à actualiser utilise `EXISTS` ; aucun comptage global des suivis n'est
nécessaire. Les tests de parité vérifient configuration effective, préparation,
retrait commerçant et neutralisation de chasse, avec les règles ordinaires.

Les contrats OpenAPI E41 et E42 sont générés hors ligne, avec réponses typées du
tableau et de la préparation batch et configuration additive. Trois dépôts sont modifiés : projet, backend,
Marketplace. Animation et Pro n'ont aucun nouveau parcours ni commande.
La migration additive `v284_e73_priorites_rappels_live.sql` précède backend puis
frontend. Les anciens suivis ne sont pas rattachés arbitrairement à un token :
**Actualiser mes accès** utilise les seuls tokens du carnet, sans réinscription
ni opt-in. Les [consignes d'exploitation](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrivent les deux batchs, leur simulation et leur activation.

La recette HTTPS sur TEST, les permissions/abonnements de véritables appareils,
la réception Web Push et les mesures de charge mixte restent à exécuter après
livraison. Six parcours complémentaires `RM-LIVE-HOME-01` à `03` et
`RM-LIVE-RAPPEL-01` à `03` sont préparés dans la [recette métier](recette-metier.md),
sans barrer ni valider leur recette hébergée. Les contrôles documentaires finaux
réussissent : 94 guides, 1 043 liens locaux, aucune erreur ; 130 sources exportées
vérifiées. `git diff --check` réussit dans les trois dépôts. Les deux clusters
PostgreSQL jetables et le serveur navigateur de test sont arrêtés.
Aucun fournisseur réel, environnement partagé ou navigateur utilisateur
n'a été sollicité pendant la validation. Les commits applicatifs sont poussés
sur `origin/main` à la demande de l'utilisateur après cette validation locale ;
aucune action directe de déploiement n'est exécutée.

## Complément UX du 30 octobre 2026 — E73-EVO-LIVE-UX

Demande : simplifier la navigation et donner envie de participer grâce à la
dynamique réelle des animations. [Critères UX et sémantique des chiffres](localeo-live-entree-unique.md#complément-ux-du-30-octobre-2026--e73-evo-live-ux).
Bases de validation : Marketplace `0a2de86`, backend `245f7d8`, documentation
`69e7e84`, avec les modifications décrites ci-dessous. Réalisation enregistrée
dans Marketplace `feb5d0e` et backend `3a6f930` ; le profil CORS Coffrets TEST
est enregistré séparément dans le backend `c25d202`.
Le statut global E73 reste En cours.

- Marque conservée dans l'en-tête, rappel retiré du contenu Découvrir ;
  raccourci icône redondant supprimé en surface Animation. Boussole Découvrir
  et repère Mes communes avec leurs libellés ; marque vers la découverte.
- Recherche de commune retirée de Réglages ; anciens liens `?focus=city`
  conservés par accès à Mes communes. Pas de première commune choisie
  automatiquement. Les préférences de notification sont lues à l'ouverture,
  sans PUT implicite. Une sélection vide explicite reste distincte d'une
  préférence locale absente ou inaccessible, qui conserve les communes serveur.
- Cartes illustrées avec statut, défi configuré et trois métriques publiques :
  inscriptions présentes, gagnants courants distincts et unités de dotation.
  Les valeurs inconnues ou invalides ne deviennent pas zéro. Le total de lots
  n'est ni le nombre de types, ni le stock restant. Aucun faux flux d'activité,
  classement, taux de gain ou progression personnelle n'est inventé.
- Nouvelle lecture backend groupée sur les identifiants visibles de la page,
  maximum 50, une instruction SQL supplémentaire, sans lecture par carte.
  Le compteur d'inscrits et les états d'attribution restent ceux du backend ;
  aucun contact, token, nom de participant ou donnée personnelle n'est publié.
  Contrat OpenAPI additif `dynamique`, champs optionnels non négatifs ou nulls.

La revue indépendante vérifie notamment les attributions remplacées, suppléants,
tirages libres non confirmés, quantités Coffrets et null contre zéro. Les
retours ont aussi couvert les grands nombres sur mobile et la conservation des
communes serveur sans choix local explicite. La reproduction de navigation est
rouge avant correction (`tmp/live-ux-navigation-reproduction.log`). Le premier
test de case de notification exigeait une modification immédiate : les traces
montrent le PUT 200 correct ; le scénario attend désormais l'état confirmé,
avec conservation des assertions de contenu et du refus 503.

Validation backend : **20 tests ciblés réussis** dans
`tmp/live-dynamique-final.log`, dont 50 identifiants lus en une instruction,
et **620 contrôles d'architecture réussis** dans
`tmp/live-dynamique-architecture.log`. Une suite plus large conserve **29
réussites et un échec OpenAPI préexistant** : la route binaire
`GET /protected/animation-locale/animations/{animation_id}/flyer/illustration`
n'est pas recensée dans la liste binaire du test global des response models.
L'échec est reproduit sur le HEAD initial `245f7d8` dans une copie isolée,
preuve `tmp/live-dynamique-baseline-api.log` ; aucune assertion ou exclusion
affaiblie. Le test de coût PostgreSQL est adapté à une lecture supplémentaire
fixe et bornée, sans être déclaré exécuté sur PostgreSQL.

Le test F12 existant révèle aussi
[ANO-MPL-E73-LIVE-03](../../roadmap/anomalies/marketplace.md) : les entrées locales
dans Live rechargeaient le document complet. Les liens du routeur conservent
la navigation interne, tout en acceptant le domaine configuré lorsqu'il est
externe. F12 repasse avec les mêmes contrôles de mémoire, de service worker et
de saisie. Le scénario historique de catalogue attendait les anciens sélecteurs,
routes et informations de gain dans la découverte : il est adapté au catalogue
public, et ses assertions de gagnant, lot, QR personnel et historique sont
conservées dans le détail autorisé et Mes participations (`LiveCatalogContinuity`).

Le contrat E41 est limité aux deux schémas concernés (55 lignes ajoutées).
L'export complet hors ligne révèle une dérive historique plus large et reste
dans les sorties de travail ; elle n'est pas incorporée à cette évolution.
Les vérifications navigateur couvrent **40 scénarios distincts** sur plusieurs
lots : découverte et métriques, communes, stockage absent/corrompu/vide,
notifications (401/503 et reprise), anciens Coffrets, avis et sauvegarde,
dialogues et continuité des accès personnels. Journaux Marketplace :
`tmp/live-ux-restants-reprise1.log` (23 réussites),
`tmp/live-ux-integration-finale.log` (quatre scénarios d'avis et reprise réussis,
puis un échec de chargement initial rejoué dans le lot suivant),
`tmp/live-ux-notifications-regression.log` (11 réussites et les deux écarts
ci-dessus), `tmp/live-ux-derniers-rejeux.log` (six réussites après correction et
adaptation). Des reprises sont nécessaires après des dépassements du délai de
chargement initial ; aucune assertion de comportement ni délai n'est affaibli.
La revue des captures à 200 % fait passer les métriques de colonnes fixes à des
blocs qui se répartissent selon leur contenu, afin de garder les grands nombres
lisibles. Le défi dit « validations à réaliser », sans laisser croire qu'un
passage suffit pour une tombola avec achat confirmé. La chasse ne publie pas ce
seuil numérique. **125 tests Node réussis**, journal `tmp/live-ux-security.log`.
Le dernier rejeu des quatre scénarios de dynamique passe sur le libellé et le
CSS finaux (`tmp/live-ux-dynamique-finale.log`), y compris trois milliards d'unités
en dotation à 390 px et texte 200 %, sans morceler les nombres. Captures relues
dans `tmp/live-ux-preuves/`. ESLint sources et tests touchés réussi ; contrôles
documentaires : 97 guides, 1 069 liens locaux, aucune erreur, et 130 sources
exportées vérifiées. `git diff --check` réussi dans les trois dépôts modifiés.
Les échecs et reprises de harnais restent dans les sorties privées de travail.
Les tests navigateur utilisent un build isolé et des fixtures, sans trafic réel.
Les tests SQL utilisent une base jetable : les plans PostgreSQL et la tenue en
charge restent à mesurer avant activation. Le cache public existant
(60 secondes, puis stale-while-revalidate 300 secondes) est conservé : les
compteurs ne constituent pas une promesse de temps réel.

Impacts : backend, Marketplace et contrat canonique E41 ; pas de migration,
nouveau rôle, nouveau compte, permission, fournisseur ou paramètre. Les règles
de participation et les données existantes sont conservées ; les fixtures
évoluent sans génération de démonstration réelle. Pas de changement ERP, Pro,
portail organisateur ou batch. Les commits sont créés à la demande de
l'utilisateur après validation ; aucun déploiement ni mutation du TEST partagé
pour ce complément. Aucun scénario historique de recette barré.

## Évolution locale du 30 octobre 2026 — E73-EVO-LIVE-UNIQUE

Demande : [Live comme entrée unique](localeo-live-entree-unique.md), à
`animations.localeo.city`, avec une UX mobile d'abord. Arbitrage utilisateur :
aucun nouveau compte habitant ; suivi des communes sur l'appareil.

Implémentation dans `localeo-marketplace`, commit `0a2de86` (base `8d42619`) :
navigation basse Découvrir / Mes participations / Mes communes ; sélection
multiple persistée, GPS volontaire et repli manuel, contexte de commune partagé
sans remplacement silencieux des préférences. Catalogue public séparé en deux
périodes, pages indépendantes et deux lectures concurrentes, résultats progressifs,
erreurs partielles et sélection temporaire en cas de stockage refusé.

L'ancien catalogue et `surface=animations` quittent l'interface marketplace.
La configuration choisit l'origine Live ; seuls les contextes publics autorisés
sont repris. Les liens des menus, cartes, recherche, agenda et présentation
Animation utilisent cette destination. L'inscription réutilise son formulaire
et ses commandes sous le scope `/live/`, avec maintien des liens personnels.
Avant changement d'origine avec un carnet, la reprise volontaire conserve les
identifiants et accès sans effacement ni nouvelle inscription. L'assistant
conserve aussi la fiche/inscription, commune et source jusqu'à la destination.

La fiche reste consultable publiquement si l'enrichissement d'une installation
existante échoue. Aucun nouveau contrat, compte, rôle, schéma, migration SQL,
référentiel, notification ou recommandation. Pas de changement backend, ERP,
batch, Pro ou portail organisateur ; les modèles d'anciens liens restent acceptés.
Les fixtures frontend couvrent les données existantes sans génération réelle.

Le test de stockage bloqué a reproduit et permis de corriger
[ANO-MPL-E73-LIVE-01](../../roadmap/anomalies/marketplace.md) : la lecture locale
indicative du carnet ne doit pas masquer un reçu personnel valide. L'inscription
reste unique et le réessai ne porte que sur l'écriture locale. Les assertions
de succès, reçu et QR sont conservées. Les attentes de navigation remplacées
sont adaptées à cette décision produit ; les assertions de dates des coffrets
utilisent le format français existant du rendu, avec la même échéance précise.

Revue indépendante : stockage refusé et rendu progressif corrigés, contexte
conservé dans l'assistant, règles de capacité/origine et autorisations serveur
préservées. L'en-tête mobile conserve la marque et les actions utiles ; l'action
d'installation reste dans les réglages. Les captures à 320/390 px servent à
vérifier l'absence de débordement et les cibles tactiles, pas une tenue en charge.
La revue visuelle à 200 % a révélé des libellés tronqués dans le menu bas :
hauteur adaptable et réserve mesurée sous le contenu corrigent ce défaut.
Le test contrôle désormais les limites complètes des libellés et la réserve.

| Critères | Preuves locales et limites |
| --- | --- |
| LIVE-01/02/03/06/11 | `live-discovery-unique.spec.cjs`, `live-followed-communes.test.cjs` : lecture publique, communes, périodes, pagination, GPS, stockage, contexte, mobile. |
| LIVE-04/05/08 | `live-carnet.spec.cjs`, `live-animation-surface.spec.cjs`, sauvegarde/import : inscription et reprise, plusieurs participations, QR, actualisation, anciens Coffrets. |
| LIVE-09/10 | `live-entry-redirects.spec.cjs`, `live-entry-routing.test.cjs` : anciennes entrées, contexte, destination autorisée, assistant et liens directs. |
| LIVE-07/12 | Fallback SPA et build locaux contrôlés ; DNS/TLS, domaines hébergés, installation PWA réelle et recette de bascule à exécuter avant activation. |

Validation finale : **53 tests navigateur réussis** en une seule série séquentielle
sur l'arbre final (`tmp/live-unique-validation-complete.log`, 7,1 minutes),
**125 tests Node de sécurité** et **13 tests serveur** réussis ; ESLint sur les
sources et tests touchés réussi. Les scénarios couvrent géolocalisation et replis,
320/390 px, texte à 200 %, navigation clavier, réduction des mouvements,
détail public sans installation disponible, inscription sans nouveau compte,
stockage refusé, avis personnels, export/import du carnet, anciens accès
Coffrets et liens directs vers Live. Deux séries parallèles ont dépassé le délai
de cinq secondes sur le chargement initial ; la reprise utilise le worker unique
prévu par la configuration du dépôt, sans changer les assertions ni les délais.
La revue indépendante des hauteurs et des liens est favorable.

Contrôles documentaires : **97 guides, 1 065 liens locaux, aucune erreur** ;
**130 sources exportées vérifiées**. `git diff --check` réussi dans les deux dépôts.
Les journaux sont conservés dans `localeo-marketplace/tmp/` et les captures
relues dans `tmp/live-unique-preuves/` (sorties locales ignorées par Git).

Les tests utilisent un build isolé, des API simulées et un garde réseau ; ils
ne constituent pas une recette sur les domaines hébergés. Aucun scénario
historique de recette n'est barré par ces tests d'évolution. Le statut E73 reste
**En cours**. Les commits et leur push sont demandés séparément après cette
validation. Aucun déploiement n'est effectué ; le clone métier figé reste inchangé.

## Correction locale du 30 octobre 2026 — E73-EVO-UX-ERP

Demande : une entrée par fonction dans Animation ERP, en-têtes et retours
harmonisés. Réalisation dans `localeo-backend`, base `3720a08` avec travaux
locaux préexistants conservés, et dans cette documentation. Les autres
applications ne sont pas modifiées par cette intervention.

| Critère | Résultat et preuve |
| --- | --- |
| E73-EVO-UX-ERP-01 | 17 destinations directes classées en Animations / Équipes et contrats / Offre et modules / Pilotage ; actions Nouveau dans leurs listes, accueil récapitulatif et anciens fragments conservés. `animation-navigation.test.mjs` vérifie le menu réellement servi et ses destinations ; le navigateur vérifie droits, entrée active et demandes d’organisation distinctes des accès |
| E73-EVO-UX-ERP-02 | `animation-navigation.js` fournit les en-têtes du shell et des trois modules autonomes ; quatre consoles et Offres et tarifs utilisent la même structure et CSS. Retour liste/espace, détail/liste, lot/animation ; filtres seulement depuis parent de même origine. Captures relues à 320/1280 px ; liens du menu et retours principaux visant 44 px. La saisie reste protégée lors du retour (annulation du départ conserve le champ) |
| E73-EVO-UX-ERP-03 | Session, droits, lecture seule, CSRF, idempotence, conflits et reprise après réponse perdue conservés ; rendu Support inchangé. Retour des consoles vers l’accueil ERP si la consultation de l’espace Animation n’est pas autorisée ; trois tests rouges avant correction puis réussis, conservation toujours refusée hors ADMIN |

Revue indépendante intégrée : accès aux offres globales rétabli comme fonction
distincte du catalogue par commune ; impasse des opérateurs spécialisés corrigée.
Lecture des captures : liens imbriqués initialement affichés en ligne, test de
reproduction échoué (`inline` au lieu de `block`) puis réussi après correction
CSS. Les anciennes assertions de libellé de retour ont été adaptées à la
hiérarchie explicitement demandée, sans supprimer les contrôles clavier,
de largeur, de données ou de permissions.

Validation sur l’arbre final :

- **767 tests Python réussis**, code 0, via `scripts/validation/test_isolated.py` :
  architecture/domaine/couverture, navigation des consoles, shell équipe et assets,
  accès internes, nouveaux tests `test_animation_console_navigation.py` et suites
  `test_admin_specific_ui_system.py` / `test_animation_locale_admin.py`.
- **4 tests Node réussis** dans `tests/frontend/animation-navigation.test.mjs` :
  fonctions actives, menus, parents et refus de référents hostiles.
- `tests/browser/animation-navigation-erp.cjs` : **26 contrôles réussis** sur
  320/1280 px, menu, navigation, capacités, formulaire modifié et retours.
- Les quatre suites `generation-erp.cjs`, `preparation-erp.cjs`,
  `exploitation-erp.cjs`, `conservation-erp.cjs` passent avec **18 parcours**,
  y compris les retours et leur cible tactile, les refus et les reprises.
- Huit suites navigateur adjacentes passent : `epic73-suivi-produits.cjs`
  (ERP et Support), `epic73-reversibilite.cjs`, `epic73-pilotage-economique.cjs`,
  `epic73-checkout-erp.cjs`, `epic73-modules-erp.cjs`, `equipes-animation-erp.cjs`,
  `epic73-preparations-service.cjs`, `epic73-sollicitations.cjs`.

Les effectifs de tests, contrôles et parcours sont distincts et ne s’additionnent
pas. Vérifications navigateur sur fixtures sans appel externe, base réelle ni
envoi de message. Les quatre suites consoles utilisent leur HTML réel et les
nouveaux tests Python utilisent les vrais renderers ; la page des offres est
couverte sur son rendu HTML/échappement, sans recette d’une édition réelle.

Pas de modification de domaine, contrat OpenAPI, données, migration ou
générateur : présentation et navigation uniquement. Les assets supplémentaires
sont servis dans le backend avec session et `no-store`, sans nouveau réglage.
Les exports documentaires doivent accompagner une livraison backend autonome.
La recette connectée après livraison reste à effectuer ; aucune conformité
complète d’accessibilité ni validation terrain n’est déduite de ces tests.
Aucun commit, push ou déploiement réalisé.

## Évolution locale du 30 octobre 2026 — E73-EVO-UX-PUBLIC

Retours sur le site public TEST : ajout de la géolocalisation volontaire,
reprise des codes visuels Coffrets et navigation Live centrée sur les animations.
Les critères et l’analyse UX sont dans les [parcours canoniques](perimetres-parcours-saas.md).
Périmètre modifié : `localeo-marketplace` et documentation `localeo-projet`.
Bases respectives `70d7128` et `6e46edd`, avec travaux locaux préexistants conservés.

| Critère | Réalisation et preuve |
| --- | --- |
| E73-EVO-UX-PUBLIC-01 | `AnimationLocationPicker` utilise le contexte territorial E52 dans un POST annulable, sans mise en cache des coordonnées ; refus, délai, indisponibilité, commune hors réseau, précision approximative, absence de GPS et réponses tardives couverts par `animation-discovery.spec.cjs`. La revue indépendante a identifié un callback périmé pouvant écraser les filtres et un message périmé après retour navigateur : corrigés avec callback courant et réconciliation du message, scénarios ajoutés |
| E73-EVO-UX-PUBLIC-02 | En-tête bleu profond, orange et typographies partagées, commune/filtres avant les animations sur ANIMATION, trois étapes de présentation ; composition du catalogue Coffrets conservée. Captures 320/1440 px relues, correction du lien d’évitement et des numéros d’étapes sur mobile ; clavier et texte 200 % couverts par le scénario existant `animation-saas-public.spec.cjs` |
| E73-EVO-UX-PUBLIC-03 | `LiveCarnetHeader`, `liveStore` et état vide adaptés ; `live-animation-surface.spec.cjs` couvre les deux surfaces, les rubriques mémorisées, le lien direct et l’ajout d’un ancien Coffret avec conservation en IndexedDB. Aucun effacement de carnet |

Reproduction initiale : le scénario GPS échoue sur l’absence du bouton avant
correction. Les premières passes ont aussi révélé une association de libellé
à préciser et deux routes de fixture manquantes pour la lecture d’un Coffret ;
markup et fixtures corrigés sans assouplir les assertions ni le blocage réseau.
Une passe élargie avec délai local réduit à 30 secondes a affiché 29 succès et
un dépassement sur la reprise d’avis ; le rejeu avec le délai habituel de
90 secondes du projet a confirmé ce scénario et les 17 autres de cette passe
(18 succès, code 0). Les passes se recoupent et ne s’additionnent pas.

Bilan navigateur : **32 scénarios distincts réussis** dans les cinq fichiers
`animation-discovery`, `live-animation-surface`, `animation-saas-public`,
`animation-source-merchant` et `discovery-premium` (`tests/visual/*.spec.cjs`).
Dernière passe après conservation explicite de la composition Coffrets : les
11 scénarios découverte réussissent (code 0), dont les deux courses GPS, le
retour navigateur et le catalogue Coffrets. Les 18 scénarios de la passe
précédente incluent les tests de satisfaction, de reprise et de conservation
des anciens accès. Les 13 autres couvrent diffusion, commerce et découverte
Coffrets. Aucun test ignoré. Contrôles documentaires : 98 guides, 1130 liens
locaux et 130 sources exportées vérifiés sans erreur ; diffs sans erreur.

Autres contrôles : deux tests Node surface/reprise/commande personnelle et
13 tests serveur réussis (codes 0) ; build Vite isolé des `.env` exécuté par les
parcours navigateur. ESLint sur `src` et les deux nouveaux fichiers de tests
réussi. `npm run lint` global n’a pas pu parcourir des dossiers temporaires
locaux (`output/bum-politique/pytest-approval-1`, puis `tmp/address-architecture`,
erreurs `EPERM`) ; aucun changement d’ACL, suppression ou exclusion permanente.

Lecture distante sans mutation : le site TEST sert la surface ANIMATION avec
API `https://test-api.localeo.city`. OPTIONS du POST territorial depuis cette
origine publique répond 200 avec `Access-Control-Allow-Origin` exact. Aucun
POST de position réelle envoyé. La permission GPS réelle, la résolution sur
téléphone et la version déployée après livraison restent à recetter.

Pas de changement backend, OpenAPI, migration, données ni générateur : la
projection territoriale et les règles de participation/gain sont réutilisées.
Pas de collecte Analytics supplémentaire ; stockage et accès personnels
préservés. Les recommandations de confirmation d’inscription, de prochaine
action et de mise en scène des acquis du jeu sont une analyse, pas une
implémentation déclarée terminée. Le fil d’actualités Live et ses filtres
existants, dont Coffrets, restent inchangés. Aucun commit, push ou déploiement.

## Évolution locale du 30 octobre 2026 — E73-EVO-DOMAINES

Décision acceptée : site public `animations.localeo.city`, portail organisateur
`gestion-animations.localeo.city`, marketplace Coffrets conservée sur un autre
service. Équivalents TEST : `test-animations`, `test-gestion-animations` et
`test-marketplace`. Cette évolution remplace le profil TEST qui réutilisait
l’accueil de la marketplace. Les preuves de recette antérieures restent
historiques ; aucun nouveau déploiement n’est revendiqué.

| Critères complémentaires | Sources / résultat local | Preuves exécutées |
| --- | --- | --- |
| E73-EVO-DOMAINES-01 | Quatre profils Marketplace Coffrets/public, deux profils gestion, exemples et guides distincts ; défaut local Coffrets conservé | 8 tests Marketplace configuration/surface/reprise et 5 tests build-environment Animation ; quatre lectures HTTP locales `app-config.js` et deux validations de profils de gestion |
| E73-EVO-DOMAINES-02 | Compléments backend production/TEST pour templates publics, portail, origines exactes et retours de paiement ; aucune règle métier modifiée | 98 tests `tests/security/test_animation_browser_session.py` dont contrôle des deux profils : public refusé malgré son autorisation CORS générale ; 618 contrôles architecture/domaine/couverture |
| E73-EVO-DOMAINES-03 | Contrôle de build Pro autorise le site public exact ; API/Marketplace/Coffrets historiques conservés, gestion et origines TEST refusées en production | 50 tests unitaires Pro ciblés ; 6 tests navigateur `validation-security.spec.js` avec nouveaux QR, anciens QR et refus sans appel de résolution |
| E73-EVO-DOMAINES-04 | Harnais E73 sépare `publicAnimation` de `marketplace` ; clone historique 18776 compatible, 18778 explicite ; aucune réécriture de campagne privée | 363 tests Node E73 puis 114 ciblés après correction de l’allowlist RM-X-03, qui bloquait la nouvelle origine dans ses contextes de fuseau ; test d’abord en échec puis réussi. Suites recoupées, effectifs non additionnables |

Commandes reproductibles :

- Backend : `python scripts/validation/test_isolated.py tests/security/test_animation_browser_session.py -q` ; contrôles architecture selon le guide backend ; dernier ciblé Node : `node --test tests/frontend/recette-e73-public-operations.test.mjs tests/frontend/recette-e73-core.test.mjs tests/frontend/recette-e73-isolated.test.mjs` (114 succès).
- Marketplace : `node --test tests/security/public-config.test.cjs tests/security/animation-surface-satisfaction.test.cjs tests/security/library-backup.test.cjs`.
- Gestion : `node --test tests/build-environment.test.mjs`.
- Pro : `npm test -- src/lib/api/productionConfig.test.js src/lib/api/demoConfig.test.js src/features/animations/model.test.js src/features/animations/publicOrigins.test.js` ; `npm run test:e2e -- tests/e2e/validation-security.spec.js`.

Le lot Node complet de 363 succès a été exécuté avant le dernier ajout RM-X-03 ;
il compte désormais 364 tests, sans nouveau passage intégral après ce ciblé.
Sous PowerShell, son lancement développe explicitement les fichiers :

```powershell
$recetteTests = @(rg --files tests/frontend | Where-Object { $_ -match 'recette-e73-.*\.test\.mjs$' })
node --test @recetteTests
```

Revue indépendante : contrôle de la séparation des origines et des profils,
compatibilité des anciens QR et clones ; correction de l’allowlist de fuseau et
ajout des retours de paiement explicites à la procédure de bascule. Le défaut
était dans le harnais, aucun invariant métier n’a été changé.
Sans impact sur les schémas OpenAPI, les migrations SQL, les rôles, les
générateurs ou les données de démonstration : les URL consomment les templates
existants, et aucune nouvelle donnée ni permission n’est requise.

**Reste à livrer** : DNS/TLS, association aux services, injection des profils,
reconstruction/déploiement et recette hébergée des nouveaux domaines, anciens
liens personnels et carnets. Aucun build de livraison, commit, push ou
déploiement effectué pour cette évolution. Les validations locales ne prouvent
pas que les domaines pointent déjà vers les services cibles.

## Restrictions et état initial

Implémentation, bases jetables locales, tests isolés et commits locaux uniquement. **Aucun push, pipeline distant, déploiement, migration/configuration de test/démo/production, envoi réel ou paiement réel.** Les vérifications humaines et hébergées restent des étapes futures explicites. Ne pas confondre commits et livraison.

**Ancienne consigne du 19 octobre 2026 : terminer le lot 09 puis s'arrêter, sans
commencer le lot 10.** Elle a été remplacée par la reprise ci-dessous. Les réserves
« à réaliser au lot 10 » dans les bilans antérieurs décrivent leur état à cette date ;
le bilan du lot 10 indique leur traitement et les limites encore présentes.

**Reprise autorisée le 19 octobre 2026 : implémenter le lot 10 et terminer le
travail local de l'epic.** Cette nouvelle demande remplace l'arrêt précédent ;
les interdictions de push et de déploiement restent applicables. Les recettes
humaines et preuves sur l'hébergement cible ne sont pas autorisées par cette reprise.

| Dépôt / branche | HEAD initial | Travaux préexistants à préserver |
| --- | --- | --- |
| Projet / main | `cc9991dd3679075e232f53844362405acfdc77a2` | Spécification E73 et règles associées à committer séparément ; modification étrangère `docs/specifications/moteur-animation/suivi-implementation.md` exclue |
| Backend / main | `31807b633932c2a53bb64714e978359683f9cfe1` | Aucun changement suivi |
| Animation / main | `08863e8202a3caad3c886918b0543cd2f260aec3` | README, App.tsx, ExploitationView.tsx, tests/browser/exploitation.mjs : conservation et staging sélectif requis |
| Commerçant / main | `19f7a20ebedae79f50453aefbf48c9724ed28eb1` | Aucun changement |
| Marketplace / main | `4186e44e8320a9c016d678da3f28583849452867` | Aucun changement |

## Plan et statut des lots

| Lot | US / portée | Dépôts prévus | État / preuves / commits |
| --- | --- | --- | --- |
| 00 | Sources, référence initiale, protocole UX et suivi | Projet ; lecture des quatre applications | Sources et contrôles de référence : commit Projet `be776b1` ; matérialisation des squelettes UX poursuivie dans les lots applicatifs |
| 01 | US25–26 comptes, équipe, organisation, récupération, transfert | Backend, Animation, Projet | Implémenté et vérifié localement pour CA50–53 ; backend `45d0b56` et preuve complémentaire `a17e3f4`, Animation `05c0561`, Projet `9519696` ; limites de conservation et recette hébergée ci-dessous |
| 02 | US11–13 ; parties US24/36, périmètres et onboarding | Backend/ERP/OnBoard, Commerçant, Animation, Projet | Implémenté et vérifié localement pour les produits existants ; Backend `261ebdc` et raccord asset `59d89d0`, Pro `bc9d1ac`, Animation `7cab528`, Projet `afd77cd` ; branches numériques et exploitabilité reprises aux lots 05/10 |
| 03 | US03,14–17,27–28 ; souscriptions/modules/finance | Backend, Animation, Pro (contrat), Projet | Implémenté et vérifié localement ; Backend `4f3a3b1`, Animation `79903e3`, Pro `8212252`, Projet `6a3d747` ; activation des modules futurs aux lots 06/07/08 |
| 04 | US01–02,04 ; branche externe US07–08 | Backend, Animation, Marketplace/Live, Pro (contrat), Projet | Implémenté et vérifié localement ; Backend `7502282`, Animation `d0b92f7`, Marketplace `1473e05`, Pro `30aeed3`, sources dans le commit documentaire lot 04 ; branche numérique au lot 05 |
| 05 | US05–10 ; complément numérique US07–08 | Backend, Animation, Commerçant, Marketplace/Live, Projet | Parcours implémentés et vérifiés localement ; commits et limites de conservation/performance ci-dessous ; aucune mise en service |
| 06 | US19–20 ; import/deltas/reprise | Backend, Animation, Projet | Implémenté et vérifié localement ; Backend `bb4e1e8`, Animation `955fb94`, sources dans le commit documentaire du lot 06 ; preuves et limites ci-dessous |
| 07 | US18,30 ; chasse et préparation accompagnée | Backend, Animation, Projet | Implémenté et vérifié localement ; Backend `44c6429`, Animation `8979893`, Projet `7f80a6c` ; recette humaine et hébergement non exécutés |
| 08 | US21–22 ; communication participants | Backend, Animation, Marketplace/Live, Projet | Implémenté et vérifié localement : campagnes, préférences Live, quotas, fréquence et alertes internes ; consolidation conservation/restauration au lot 10 |
| 09 | US23,29,31–33 ; parcours/site/assistance/bilans | Backend, Animation, Marketplace/Live, Projet | Implémenté et vérifié localement ; Backend `76103d7`, Animation `eb3def9`, Marketplace `70d7128`, sources dans le commit documentaire du lot 09 ; démonstration complète : dix réussites |
| 10 | US34–38 ; finalisation US24, exploitabilité/pilote | Backend/ERP/Support/Ops, Animation, Projet ; vérification Pro/Live et démonstration | Implémentation et contrôles locaux terminés : Backend `7f74166`, Animation `da86e39` et `3801cc5`, sources dans le commit documentaire lot 10 ; recette humaine et preuves hébergées non exécutées |

Les US partagées ne sont acquises qu’après toutes leurs branches. Reprendre les identifiants CA du plan de vérification, sans en changer la portée. Chaque bilan de lot doit enregistrer fichiers/contrats, migrations, fixtures, commandes, résultats, revue, limites et commits par dépôt. Si nécessaire, subdiviser un lot en incréments explicitement non terminaux ; aucune validation par simple présence d’un fichier.

## Préparation UX et capacité

Le squelette gestion et le squelette communication ainsi que leurs parcours de référence sont définis dans [les parcours SaaS, section 5](perimetres-parcours-saas.md). Les premières réalisations doivent matérialiser organisation/commune, navigation stable, états vides/erreurs et continuité des formulaires. Prévoir une revue locale du parcours organisateur liste → création → contrôle de publication et du parcours visiteur découverte → inscription → Live avant généralisation. La recette humaine suit Localeo puis Martignas-sur-Jalle ; elle n’est pas encore réalisée.

Capacité : 10 communes, 10 000 participants au total, 10 utilisateurs actifs simultanément ; paliers et distributions concentrées décrits par E73-PERF-01 à 08. Les tests hébergés, RPO 4 h/RTO 8 h sur hébergement représentatif et ouverture du pilote restent **non exécutés**. Les essais locaux n’en constituent pas une preuve de livraison.

## Dépendances et contrôles initiaux

E55, E68, E70 et E72 restent dans leur état produit propre. Les contrats et implémentations réels sont relus pour chaque lot dépendant ; leur existence ne prouve pas une disponibilité hébergée. E71 reste une epic indépendante ; adapter les projections nécessaires sans réaliser implicitement tout le CRM.

- Documentation : `check_guidance.py` ciblé : 102 guides, 1 181 liens, zéro erreur/avertissement ; `sync_documentation.py --check-sources` : 122 documents vérifiés ; `git diff --check` réussi.
- Backend : `scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q --basetemp .artifacts/e73-baseline-20261018-01 --tb=short` : **467 réussites**. Le premier essai sans répertoire temporaire explicite comptait 452 réussites et 15 erreurs de permission du répertoire Windows temporaire ; la reprise isolée dans le workspace les résout sans modifier les assertions.
- Animation : baseline frontend confiée au lot 01 ; résultat à consigner.
- PostgreSQL : inventaire local en lecture seule ; aucune connexion à une base d’exploitation.

## Journal de réalisation

### Lot 00 — Préparation

Lecture des instructions, inventaire des cinq dépôts et répartition des responsabilités. Backend lot 01 et frontend lot 01 confiés à des agents distincts, sans permission de commit/push ; intégration et commits par l’agent principal. Inventaire de tests PostgreSQL confié en lecture seule. Aucun changement applicatif déclaré validé à ce stade.

### Lot 01 — Comptes et équipes

Périmètre : US25–26 / E73-CA-50 à 53. Le domaine `EquipeOrganisation` possède les changements d’appartenances, délégations et responsabilité ; les services orchestrent transactions, identité globale, invitations et projections. Le portail comporte les parcours compte, équipe, choix d’organisation/commune et récupération d’accès. L’ERP permet la vérification des demandes et la récupération assistée avec preuve et motif. Les listes équipe, invitations et demandes sont paginées en SQL ; les contrôles de responsabilité utilisent une lecture ciblée de la racine et du nombre de responsables.

Les nouvelles routes sont intégrées à la liste explicite du middleware navigateur Animation : contrôle d’origine, prévol CORS, cookie, CSRF et séparation des routes ERP. Une session d’identité seule peut accepter une invitation sans recevoir de données d’organisation. La perte du contexte d’une session complète continue de produire un refus.

Migrations préparées : `v260_e73_equipes_organisations.sql` et `v261_reinitialisation_mot_de_passe_animation.sql`. Le générateur local produit les appartenances et rattachements synthétiques ; le registre d’export/restauration inclut les six nouvelles tables. Les invitations et récupérations réelles n’ont pas été envoyées. Une future reprise des comptes historiques nécessite la vérification explicite de leurs responsabilités et rattachements ; aucune responsabilité n’est déduite automatiquement.

Preuves réellement exécutées :

| Contrôle | Commande / preuve | Résultat |
| --- | --- | --- |
| Transport navigateur, mot de passe, API et persistance | `scripts/validation/test_isolated.py tests/security/test_animation_browser_session.py tests/security/test_mot_de_passe_animation_postgres.py tests/api/test_animation_password_api.py tests/application/identite_acces/test_gestion_mot_de_passe_animation.py tests/application/identite_acces/test_gestion_acces_animation_reset.py tests/domain/identite_acces/test_mot_de_passe_animation.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp .artifacts/e73-password-final-01 --tb=short` | **130 réussites**, deux avertissements de dépréciation Starlette/httpx |
| Migrations complètes, rejeu et démonstration/restauration | `scripts/validation/test_isolated.py tests/integration/test_data015_migrations.py tests/security/test_demo_equipes_animation_postgres.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_migrations_test --basetemp .artifacts/e73-migrations-final-01 --tb=short` | **4 réussites** ; avertissement SQLAlchemy de réflexion `dialect_options` |
| Régression frontend Animation | `npm.cmd test` | **181 réussites**, zéro échec et zéro test ignoré ; types et lint réussis |
| Navigateur ERP | `node tests/browser/equipes-animation-erp.cjs` | Réussi à 390 et 1 280 px : lecture, preuve obligatoire, CSRF/idempotence, erreurs 409, issue réseau incertaine et relecture, absence de débordement |
| Navigateur portail | `node tests/browser/organisation-access.mjs` et `node tests/browser/account-app.mjs` | 111 assertions de composants et 48 assertions dans App ; API synthétique locale, formats mobile et bureau |
| Contrats embarqués et build isolé | Export hors ligne `generate_epic41_openapi.py`, copie consommateur Animation ; `node --test tests/generation-http-contracts.test.mjs tests/publication-http-contracts.test.mjs` ; `node scripts/build-generation-tests.mjs` | 749 routes exportées, 5 tests réussis, build réussi sans fichier opérateur ; avertissement de chunk principal 839,83 ko, à traiter dans la maîtrise des chargements du lot 09 |
| Pagination et plans SQL équipe | `scripts/validation/test_isolated.py tests/security/test_equipes_animation_performance_postgres.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp .artifacts/e73-team-perf-02 -q -s --tb=short` | **2 réussites**, 10 103 appartenances dont 6 002 dans une organisation ; requêtes réelles capturées puis `EXPLAIN ANALYZE BUFFERS`, aucun réglage forçant un index |

Les pages d’équipe initiale, suivante et après 5 000 membres utilisent `idx_equipe_animation_membres_page`, avec limite 26 et curseur SQL, sans `OFFSET`. Mesures ponctuelles à chaud : 0,037 / 0,067 / 0,040 ms pour ces requêtes, coûts estimés 4,31 / 4,38 / 6,85. La liste d’organisations utilise `idx_equipe_animation_organisations_page` ; PostgreSQL choisit librement une lecture séquentielle de la petite table des 102 organisations pour une jointure, sans balayage des appartenances. La projection complète utilise neuf requêtes pour des pages de 1 ou 100 membres, avec respectivement 3 ou 102 membres hydratés au maximum. Ces mesures caractérisent la lecture locale et ne prouvent ni le trafic simultané ni un engagement de temps de réponse.

Revue indépendante : les premiers 42 tests métier/HTTP/PG passaient, mais deux scénarios supplémentaires ont révélé une acceptation après suspension globale de l’auteur et une récupération vers un successeur suspendu. Les corrections et tests persistés ont été vérifiés indépendamment : `test_equipes_animation_postgres.py -k 'invitation_refuse_auteur_suspendu or recuperation_refuse_identite_suspendue'`, runner PostgreSQL local, répertoire `.artifacts/e73-review-corrections-01` : **2 réussites, 14 désélections**. Une course changement d’organisation/révocation de session a également été corrigée et revérifiée sur PostgreSQL : la session révoquée reste inutilisable, même après écriture d’une ancienne projection. Les interfaces portail et ERP ont été relues séparément de leurs auteurs.

Le PostgreSQL utilisé est un cluster créé pour cette tâche sur boucle locale, avec deux bases jetables distinctes. Le runner désactive la configuration opérateur et les effets externes. Ces preuves ne concernent aucune base partagée.

Contrôles finaux backend, préfixe commun `.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`, suffixe commun `-q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test --basetemp <répertoire indiqué> --tb=short` :

| Fichiers / répertoire temporaire | Résultat |
| --- | --- |
| `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/domain/identite_acces/test_equipe_organisation_dedicated.py tests/application/services/test_equipes_animation.py tests/api/test_equipes_animation_api.py tests/security/test_equipes_animation_postgres.py tests/api/test_acces_animation_erp.py tests/security/test_animation_browser_session.py` ; `.artifacts/e73-team-final` | **620 réussites**, avant ajout de la preuve T1 |
| `tests/security/test_equipes_animation_postgres.py tests/application/services/test_equipes_animation.py tests/api/test_equipes_animation_api.py` ; `.artifacts/e73-team-audit-final` | **25 réussites**, après ajout de la preuve T1 |
| `tests/security/test_generation_animation_postgres.py` ; `.artifacts/e73-team-generation-final` | **24 réussites** : tâches non commencées suspendues, reprise contrôlée et régressions de génération |
| `tests/security/test_animation_finance_tenant.py` ; `.artifacts/e73-team-finance-final` | **4 réussites**, zéro skip après raccordement du test à la variable du runner isolé ; le premier essai ignoré faute de variable historique ne constituait pas une preuve |
| `tests/security/test_session_animation_revocation_race.py` ; `.artifacts/e73-session-race-01` (sans `--tb=short`) | **1 réussite**, vraie révocation concurrente et ancienne projection ; preuve durable ajoutée au commit complémentaire `a17e3f4` |

Les suites se recouvrent : leurs nombres ne sont pas additionnés en un total de tests distincts. Les contrôles frontend des 15 appels compte/équipe contre l’OpenAPI passent dans `tests/organisation-http-contracts.test.mjs` (3 tests). Le scénario `tests/browser/animation-lots.mjs` couvre lecteur avec/sans Achat à 320/1 280 px. Le scénario `tests/browser/generation-preparation.mjs` couvre la suspension explicite sans polling ni reprise automatique (70 contrôles à 390/1 280 px). Les 4 hunks préexistants « Clôturer » d’App.tsx restent exclus du commit ; types et build isolé ont aussi réussi sur une copie de l’index Git dans `tmp/e73-lot1-staged`, indépendante de ces modifications.

Conservation : classification T1/T8 et dates sources documentées dans l’architecture ; audit minimal des changements d’habilitation implémenté. Le raccordement des purges et la preuve de leur reprise après restauration restent une obligation du lot 10 avant mise en service. Les recettes humaines Localeo puis Martignas-sur-Jalle et tout contrôle hébergé restent non exécutés. Aucun push ni déploiement.

### Lot 02 — Périmètres commerçants

Le domaine Référencement porte la décision produit, distincte du statut général du commerce. Les migrations locales préparées sont `v262_e73_perimetres_commercants.sql` et `v263_autorisations_dediees_internes.sql`. Les commandes ERP imposent version, motif et idempotence ; le rôle Backoffice ne suffit pas sans autorisation dédiée. Le générateur prépare des racines `A_REVOIR`, sans suggérer ni activer automatiquement les produits des commerces existants. Son registre classe les décisions, preuves d’engagement et reçus avec le jeu métier.

OnBoard utilise une preuve de convention explicitement rattachée à chaque produit et un support Animation seule. Les onglets financiers et prestations suivent l’applicabilité projetée par le serveur. L’ERP distingue revue individuelle et bascule communale ; son historique se charge sur demande, par pages SQL de 25. Les anciennes mutations ORM directes SQLAdmin Commerçant/Prestation sont fermées au profit des parcours transactionnels ERP, avec liens explicites.

Premières preuves exécutées par l’intégration (ne constituent pas encore la validation finale du lot) :

| Contrôle | Commande / résultat |
| --- | --- |
| ERP/OnBoard mobile et bureau | `node tests/browser/epic73-perimetres.cjs` : réussi à 320/1 280 px, revue sans présélection, consultation seule, rattachement de convention sur dossier clos, conflit avec saisie conservée, historique paginé et confirmation de bascule communale |
| Régressions OnBoard | `node tests/browser/onboard-administration.cjs` : 7 scénarios réussis ; `node tests/browser/epic69-onboard.cjs` : Lecteur/Backoffice, scopes, actualisation de droits et purge de session réussis |
| Autorisation dédiée ERP | `node tests/browser/epic69-acces-internes.cjs` : réussi à 390/1 280 px ; l’autorisation n’est jamais attribuée implicitement par le changement de rôle |
| Générateur/registre | Runner isolé, `tests/unit/test_demonstration_registry.py tests/integration/test_demo_perimetres_commercants.py`, base locale jetable, `.artifacts/e73-demo-scopes-01` : **10 réussites** |
| Pagination et index historique | Runner isolé, `tests/security/test_historique_perimetres_postgres.py -q -s`, base locale jetable, `.artifacts/e73-history-perf-01` : **1 réussite**, 10 000 décisions dont 6 000 concentrées sur un commerce ; deux pages distinctes, 26 lignes SQL maximum, absence de chargement des snapshots et d’OFFSET ; `EXPLAIN ANALYZE BUFFERS` utilise `ix_historique_perimetres_commerce_date` (0,076 et 0,093 ms ponctuels) |
| Administration et adresses | `.artifacts/e73-admin-boundary-01` : 24 réussites, 1 échec de double de session incomplet dans le test de modification d’adresse ERP ; correction du double confiée au propriétaire, résultat de reprise à enregistrer |
| Sources documentaires | `sync_documentation.py --check-sources` via Python isolé : 123 documents vérifiés |

La revue a identifié puis fait corriger les frontières suivantes : continuité pendant une redemande, lecture ERP sans grant de gestion, Stripe depuis une URL directe, filtrage SQL des historiques/notifications avant pagination et compléments sur dossier clos. Les corrections sont intégrées et vérifiées par les preuves ci-dessous. La recette humaine et la bascule pilote ne sont pas exécutées.

Vérifications complémentaires de l’intégration :

- `tests/infrastructure/admin/test_perimetres_mutations_erp.py tests/application/conformite_fiscale_bum/test_adresse_onboard_erp.py`, runner isolé et `.artifacts/e73-admin-boundary-02` : **24 réussites** ; le double ERP incomplet est corrigé sans changer les assertions.
- `tests/integration/test_data015_migrations.py`, base locale exclusive `localeo_audit_migrations_test`, `.artifacts/e73-migrations-lot02` : **3 réussites**, migrations complètes et rejeu jusqu’à v263. L’indexation supplémentaire de pagination est vérifiée séparément après stabilisation.
- `node tests/browser/epic73-perimetres.cjs` rejoué après ajout du complément : réussi à 320/1 280 px ; dossier clos sans complément en lecture, complément Coffrets avec seuls champs autorisés modifiables, statut `CLOTURE` conservé.
- Contrats Animation, `node --test tests/organisation-http-contracts.test.mjs tests/generation-http-contracts.test.mjs tests/publication-http-contracts.test.mjs` : **8 réussites** sur l’export intermédiaire de 756 routes.
- `check_guidance.py` : **94 guides, 1 000 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources` : **123 documents vérifiés**.

Dette backend reproduite indépendamment sur le commit antérieur au lot `a17e3f4`, extrait dans un répertoire temporaire sans configuration opérateur : `test_missions_medias_t3.py`, `test_modification_animation_en_cours.py`, `test_tirage_tous_lots_animation.py` sous `tests/application/animation_locale`, runner isolé, `.artifacts/e73-lot02-baseline-failures` : **9 échecs et 2 réussites**. Les deux premiers échecs sont des doubles sans `configurations_animation`, trois concernent l’ancien parcours de modification après publication remplacé par la commande versionnée, quatre des doubles sans `coordinations_animation`. Les mêmes neuf échecs sont observés dans la passe large du lot ; aucun skip ni affaiblissement d’assertion. Ces scénarios doivent être repris dans les lots qui modifient effectivement les parcours Animation/tirage.

Pro est enregistré localement dans `bc9d1ac` ; le contrat Animation synchronisé dans `7cab528` conserve tous les travaux utilisateur préexistants hors index. Preuves Pro : suite unitaire intermédiaire **487 réussites**, ciblés finance/reset **24**, pagination finale **11**, contrats OpenAPI finaux **46** ; recette navigateur **28/28** puis **16/16** avec curseur à 320/1 280 px ; build isolé réussi. Les suites se recouvrent et ne constituent pas un total à additionner. La recette complète a donné **106 réussites et 7 échecs**, tous reproduits sur le HEAD antérieur `19f7a20` (`business-ux`/`merchant-contract`) ; une dernière suite unitaire complète interrompue après ralentissement n’est pas comptée comme verte. Son timeout de récupération de mot de passe passe ensuite dans la reprise ciblée sans modification de l’assertion.

La portée de ce lot couvre CA15–19 et CA26 pour les produits existants, ainsi que les branches Coffrets/passages des CA20–22. Les bons numériques et leur continuité restent à compléter au lot 05 ; les vues transverses et la restauration complète des CA25/27 restent au lot 10. Aucun de ces critères partagés n’est déclaré acquis dans son intégralité sur la seule preuve du lot 02.

Preuves backend complémentaires, préfixe commun `.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`, suffixe `-q --basetemp <répertoire> --tb=short` ; les scénarios PostgreSQL ajoutent explicitement l’URL locale jetable déjà documentée :

| Contrôle / fichiers | Résultat |
| --- | --- |
| Architecture, application Animation et périmètres ; `.artifacts/e73-perimetres-final-01` | **702 réussites**, dont architecture ; 6 doubles nouveaux et 3 erreurs de fixture corrigés puis repris ci-dessous, 9 échecs préexistants reproduits sur référence |
| `tests/security/test_perimetres_validations_postgres.py`, régressions application catalogue chasse, financement lots, avertissement lots/participants, suivi préparation, supports commerce chasse, paiements individuels/lots et scénario commission ERP ; `.artifacts/e73-perimetres-final-02` | **80 réussites** après correction des doubles, dont vrais QR/PIN PostgreSQL et refus sous suspension |
| `tests/api/test_perimetres_commercants_api.py tests/domain/referencement/test_perimetres_commercant.py tests/application/use_cases/test_initialiser_paiement.py tests/application/use_cases/test_stripe_connect_onboarding.py` ; `.artifacts/e73-perimetres-last-01` | **42 réussites**, dont transport HTTP assemblé avec refus métier 403 et refus avant fournisseur |
| Domaine et PG périmètres après alignement du conflit sur `CONFLIT_VERSION` ; `.artifacts/e73-conflict-contract-01` | **21 réussites** |
| OnBoard, droits et finance ; `.artifacts/e73-onboard-finance-final-01`, puis compléments `.artifacts/e73-complement-01` | Respectivement **678** puis **210 réussites** ; suites partiellement communes, avant finitions de pagination |
| `tests/security/test_facturation_continuite_postgres.py tests/security/test_onboarding_produits_postgres.py`, avec API de dépôt et tests curseur/complément/détail groupé ; `.artifacts/e73-final-finance-context-01` | **7 scénarios PG réussis**, 32 tests réussis au total, un double E50 obsolète corrigé et repris dans la ligne suivante |
| `tests/application/conformite_fiscale_bum/test_service_preparation_onboarding.py tests/application/conformite_fiscale_bum/test_curseur_factures.py tests/api/test_facturation_continuite_upload.py tests/security/test_grouped_invoice_detail.py` ; `.artifacts/e73-final-finance-context-02` | **26 réussites** : complément, curseur lié au contexte, refus de lecture directe et droits avant stockage |
| `tests/api/test_facturation_continuite_upload.py` ; `.artifacts/e73-final-chorus-01` | **11 réussites**, y compris les trois routes Chorus marchandes |
| Migrations complètes jusqu’à `v264_pagination_factures_commercant.sql`, même test DATA015 ; `.artifacts/e73-migrations-lot02-final` | **3 réussites**, aucune base partagée |
| Domaine périmètres, Stripe Connect, paiements individuels/lots et validations PostgreSQL ; `.artifacts/e73-perimetres-final-boundaries-01` | **65 réussites** après séparation des lectures historiques et des validations résiduelles ; appels fournisseur hors verrou métier |
| Attestations moteur PostgreSQL et salariés E72 ; `.artifacts/e73-perimetres-recus-final-01`, puis reçu après retrait sans engagement `.artifacts/e73-perimetres-recu-clos-final` | **11 réussites**, puis **1 réussite** supplémentaire pour la lecture historique d’une animation close |

Les deux listes de factures marchandes conservent leur tableau JSON et annoncent la page suivante dans `X-Next-Cursor` (exposé au navigateur), avec `limit=25`, maximum 100. Le curseur est lié au commerce, à la famille, au tri et à la version. Les actions sont calculées en lectures groupées, sans cache de droits persistant. Sur 10 000 demandes simples et 10 000 groupées : 9/10 requêtes constantes pour 2 ou 51 racines lues ; plans réels indexés sans forçage, mesures ponctuelles 0,229/0,565 ms. Les anciennes listes acheteur/Animation conservent leur contrat et leur dette de pagination, sans nouveau calcul marchand par ligne ; cette dette doit être traitée dans les lots finance/parcours concernés. Ces mesures ne démontrent pas les dix utilisateurs simultanés ni la charge mêlée du lot 10.

Raccord complémentaire : le module `perimetres-commercants.js` était absent de la liste des fichiers servis par le shell ERP. Le commit local `59d89d0` l’ajoute ; `tests/api/test_erp_perimetres_asset.py`, runner isolé, `.artifacts/e73-lot02-asset` : **1 réussite**, chargement HTTP et cache privé vérifiés. Cette preuve complète la recette navigateur qui intercepte les fichiers locaux.

### Lot 03 — Souscriptions et modules (en cours)

L’accès au catalogue est réservé aux administrateurs. Les anciennes écritures directes SQLAdmin d’offre sont fermées au profit de versions explicites. Les autorisations `abonnements:modules_octroyer` (Backoffice) et `abonnements:remboursements_decider` (Finance) sont attribuées séparément ; aucun changement de profil ne les attribue implicitement. La migration `v267_autorisations_modules_internes.sql` étend seulement les codes permis, sans accorder de droit.

Premières preuves, sans validation finale du lot :

- `tests/application/test_autorisations_dediees_internes.py tests/domain/identite_acces/test_acces_interne_dedicated.py`, runner isolé `.artifacts/e73-lot03-grants-02` : **36 réussites**.
- `tests/api/test_offres_animation_erp.py tests/security/test_acces_internes_surfaces.py tests/infrastructure/admin/test_catalogue_versionne_erp.py tests/api/test_erp_perimetres_asset.py`, `.artifacts/e73-lot03-admin-02` : **72 réussites**. La première passe avait 71 réussites et une attente Backoffice obsolète ; E73 restreint désormais cette création aux administrateurs, avec assertion de refus avant SQL.
- `node tests/browser/epic69-acces-internes.cjs` : réussi à 390/1 280 px après extension des autorisations dédiées.
- `node tests/browser/epic73-modules-erp.cjs` : réussi à 320/1 280 px sur réponses synthétiques locales : octroi versionné, dates Paris avec navigateur réglé à New York, conflit et saisie conservée, historique borné, catalogue versionné, décision de remboursement sans retrait implicite.

Les contrôles de droits/quota/paiement, migrations complètes et contrats réels restent en cours. Les trois modules seront proposés à l’achat seulement après réalisation et vérification de leurs parcours dans les lots 06/07/08 ; leur présence au catalogue n’atteste pas leur disponibilité.

Contrôles supplémentaires de l'intégration (lot encore en cours) :

- `tests/integration/test_comptes_internes_postgres.py`, `.artifacts/e73-lot03-grants-pg` : **8 réussites** ; persistance des grants et retrait sur session existante.
- `tests/application/test_souscriptions_regressions.py`, `.artifacts/e73-lot03-e47-regressions-04` : **38 réussites** ; activation commerciale séparée de l'identité, rollback et replay, invitation explicite après habilitation, réinitialisation d'une heure. La fixture a été raccordée aux tables E73 ; un doublon de fonction qui masquait un test a été retiré.
- `tests/integration/test_demo_modules_abonnements.py tests/unit/test_demonstration_registry.py tests/api/test_erp_perimetres_asset.py tests/api/test_modules_dates_contract.py`, `.artifacts/e73-lot03-demo-03`, PostgreSQL local : **12 réussites**. Le premier essai métier a détecté l'absence de reprise des débits dans le générateur ; correction par le service normal, sans validation automatique de la reprise.
- `tests/integration/test_data015_migrations.py`, `.artifacts/e73-lot03-migrations-01`, base exclusive `localeo_audit_migrations_test` : **3 réussites**, migrations complètes jusqu'à v267, rejeu et atomicité.
- `node tests/browser/epic73-modules-erp.cjs` : nouvelle réussite à 320/1 280 px incluant perte de réponse puis reprise avec exactement la même clé/corps, et confirmation motivée des conditions historiques ; formats d'unités alignés sur les vrais DTO.
- Première passe architecture/application intégrée, `.artifacts/e73-lot03-integration-01` : **533 réussites, 3 échecs**. Deux régressions de transition d'expiration après 30 jours sont renvoyées au propriétaire du service ; le troisième échec détecte le nom/format des déclarations de classes de tests dédiées. Correction en cours, aucune assertion supprimée ou affaiblie.

Le contrat hors ligne contient à cette étape **786 routes** ; il est recopié dans
les consommateurs Animation et Pro, sans prétendre à leur livraison. Les
anciennes éditions directes du catalogue ne constituent plus un chemin de mutation.

Recette Animation : **183 tests Node réussis**, types/lint/build isolé réussis,
**484 assertions dans 36 scénarios navigateur** à 320/1 280 px. Le navigateur
réglé à New York vérifie les heures affichées à Paris ; les scénarios couvrent
expiration sans abonnement courant, période future, quota/historique paginés,
premières coordonnées de facturation, perte de réponse et reprise explicite.
Les quatre hunks préexistants « Clôturer » restent intacts et exclus du futur commit.
La revue frontend/producer a détecté puis fait corriger les dates sans fuseau et
le calcul « déjà acheté » dépendant de la première page des droits.

`tests/security/test_commerce_animation_browser.py`, runner isolé
`.artifacts/e73-commerce-browser-real-01` : **4 réussites** avec la vraie pile
cookie/CORS/CSRF et une session révoquée ; refus avant appel métier. Le service
commercial est simulé dans cette preuve de transport, séparée des preuves SQL.

Pro : **42 tests de contrats réussis** avec
`node node_modules/vitest/vitest.mjs run src/lib/api/contracts.test.js src/lib/api/preparation.contract.test.js --config tmp/e73-lot03-vitest.config.mjs --maxWorkers=2`.
La configuration jetable impose `envDir:false` et des valeurs publiques synthétiques.
Le premier lancement avec la configuration Vite habituelle n'est pas retenu
comme preuve d'isolation. Seul le contrat embarqué Pro est modifié dans ce lot.

Contrôles documentaires intermédiaires : `check_guidance.py` **94 guides,
1 000 liens, zéro erreur/avertissement** ; `sync_documentation.py --check-sources`
**123 sources vérifiées**. Le lot reste en cours : revue des nouveaux octrois
sur conditions historiques, suspension sur plusieurs périodes et raccordement
du Checkout ERP historique à une intention durable, sans appel fournisseur
sous verrou métier.

Après corrections, `.artifacts/e73-lot03-integration-02` réunit architecture,
couverture des classes métier/use cases, régressions E47, démonstration SQL et
contrat des dates : **539 réussites**, deux dépréciations `utcfromtimestamp`
préexistantes dans le parcours Checkout historique. Les échecs d'expiration
de la première passe sont corrigés ; les classes de tests dédiées sont détectées
par le contrôle sans modifier celui-ci. Le test périmètres du lot 02 est renommé
`test_perimetres_commercant_dedicated.py`, avec ses assertions conservées.

Finalisation du lot 03 :

- Migrations complètes et rejeu jusqu'à **v268**, base locale exclusive,
  `.artifacts/e73-lot03-migrations-02` : **3 réussites** (68,13 s).
- Finance, droits assemblés, factures, API et worker : runner isolé PostgreSQL,
  `.artifacts/e73-commerce-final-01` ; fichiers
  `tests/security/test_commerce_droits_integration_postgres.py`,
  `test_checkout_erp_async_postgres.py`, `test_commerce_abonnements_postgres.py`,
  tests domaine commande/devis/prorata/avoirs, traitement commerce, gateway et
  webhooks Stripe : **56 réussites** (38,54 s), trois dépréciations.
  Deux anciens échecs de fixture supposaient un rôle interne ADMIN nommé
  inexistant ; les scénarios corrigés prouvent le refus Finance et suspension,
  sans élargir la permission historique `finance.executer`.
- `node tests/browser/epic73-checkout-erp.cjs` : **réussi à 320/1 280 px**,
  intention durable, attente explicite et lien visible après confirmation.
- `node tests/browser/epic73-modules-erp.cjs` : **réussi à 320/1 280 px** avec
  compteur divergent ; le libellé mobile ajouté par CSS empêchait la recherche
  accessible exacte du test, désormais ciblée sur la cellule Disponible avec
  assertion exacte « Indisponible ». Aucune assertion métier retirée.
- Animation : **502 assertions dans 38 scénarios navigateur**, types/lint/build
  isolé réussis ; `tests/modules-http-contracts.test.mjs` **2 réussites** après
  export final. Les nombres remplacent les comptages intermédiaires recouvrants.

Les lectures de quotas sont vérifiées avec 10 000 droits et 10 000 consommations,
sans recompter le journal. Les listes de commandes/remboursements sont vérifiées
sur 10 000 lignes chacune avec plans PostgreSQL et curseurs. Ces preuves ne
constituent pas encore le test de trafic transverse du lot 10. Les fournisseurs
restent simulés, les modules futurs indisponibles et la recette humaine non exécutée.

Dernière suite core : `test_modules_plateforme_postgres.py`,
`test_modules_plateforme_api.py`, `test_modules_acquis_dedicated.py`,
`test_souscriptions_regressions.py`, `test_verification_droit_plateforme.py`,
runner isolé et PostgreSQL local `.artifacts/e73-core-final-08` : **66 réussites**
(18,86 s), quatre dépréciations. La revue indépendante finale des compteurs et
du Checkout ERP n'a trouvé aucun nouvel écart concret ; c'est une revue de code
et des tests persistés, distincte de leur exécution par les auteurs/intégrateur.

Une copie de l'index Animation dans `tmp/e73-lot03-staged` exclut les quatre
hunks utilisateur : `npm.cmd run typecheck` et le build isolé y réussissent.
Le chunk principal de 863,29 ko conserve la dette de découpage identifiée pour
le lot 09. Les contrôles finaux de documentation donnent **94 guides,
1 000 liens, zéro erreur/avertissement**, **123 sources vérifiées**.

Limites opératoires préparées : un compteur divergent exige le service motivé
de contrôle/reconstruction, sans écran supplémentaire dans ce lot ; un second
paiement concurrent portant sur une période devenue incompatible reste à
rapprocher, sans créditer deux droits. Aucun fournisseur réel, worker distant,
push ni livraison n'a été utilisé. Le lot 03 est enregistré localement ; les
branches de continuité import/chasse/messages seront complétées avec leurs
opérations réelles dans les lots 06 à 08.

### Lot 04 — Animation et lots externes

Le domaine `ConfigurationDotation` possède le choix et son gel ; le domaine
d'attribution libre possède le suivi et les conditions de remplacement. Les
lots externes n'entraînent aucun achat, activation ou reversement Coffrets.
Le [protocole de tirage libre](tirage-libre-protocole.md) décrit la préparation
privée bornée et sa confirmation. Les écrans présentent séparément attribution,
envoi de l'email et déclaration de remise. Les bons numériques restent
indisponibles jusqu'au lot 05.

Premières preuves locales, complétées par les vérifications finales plus bas :

- Backend : `tests/security/test_gains_live_projection_postgres.py` et
  `tests/api/test_localeo_live_animations_inscription.py`, runner isolé,
  PostgreSQL local, `.artifacts/e73-lot04-live-04` : **7 réussites** (6,44 s).
  La projection de catalogue ne lit que les participations des animations de
  la page. Sur 10 000 participations et 10 000 gains, 3 requêtes constantes
  pour 1 ou 25 racines, sous-requêtes limitées et index réel ; mesure ponctuelle
  0,139 ms pour la projection de gain. Aucun gain privé n'est exposé avant
  confirmation, ni à un autre participant. Ce contrôle ne prouve pas le trafic
  simultané du lot 10.
- Générateur : `test_demo_dotations_animation.py` et
  `test_demonstration_registry.py`, runner isolé PostgreSQL,
  `.artifacts/e73-lot04-demo-01` : **10 réussites** (3,23 s). Le premier brouillon
  synthétique utilise deux lignes de lots externes et trois unités ; les
  historiques publiés conservent une dotation Coffrets explicite et gelée par
  le domaine. Le registre classe les neuf tables du lot comme données du jeu
  à remplacer, sans importer les anciens gagnants. La génération transverse
  complète reste à réaliser au lot 10.
- Marketplace : `node --test tests/security/animation-gain.test.cjs
  tests/security/library-backup.test.cjs` : **5 réussites**. Nature inconnue
  refusée, ancien gain Coffret compatible, absence de coordonnées/consignes
  privées dans le carnet IndexedDB et ses exports.
- Marketplace : ESLint ciblé et build Vite en mode isolé réussis. Le lint global
  rencontre un **EPERM de lecture** dans
  `output/demo-generation/pytest-bum-registry` ; aucune suppression de ce
  répertoire de travail ni modification des règles de lint.
- Navigateur Marketplace : contrat public de détail existant et
  `tests/visual/external-animation-gain.spec.cjs`, serveur local isolé :
  **3 scénarios réussis** (19,8 s), dont accès gagnant direct à 320/1 280 px,
  heure de Paris malgré navigateur New York, actualisation au clavier,
  remise déclarée puis attribution remplacée et refus de nature inconnue.
  Le gain précède la progression de jeu et aucun QR de lot Coffret n'est
  fabriqué pour une remise externe.

Les migrations complètes, la revue indépendante, les contrats et les contrôles
du parcours organisateur/tirage ont ensuite été exécutés comme suit.

Preuves de finalisation avant enregistrement :

| Contrôle | Résultat réel / artefact |
| --- | --- |
| Domaine, architecture, contrats moteur, projection Live et générateur ciblé | Runner isolé, `tests/architecture`, recensement domaine/use cases, `test_gains_live_projection_postgres.py`, API Live, dotation de démonstration, registre et `test_contrats_moteur_t1.py` ; `.artifacts/e73-lot04-integration-02` : **545 réussites** (39,61 s) |
| Configuration, publication, génération, jeu, financement et anciens tirages | Suite core sur quinze fichiers, `.artifacts/e73-lot04-core-final-12` : **161 réussites**, deux avertissements de dépendances ; inclut paiement Coffrets tardif à rapprocher sans émission d’instances |
| Conservation d’identité | `tests/security/test_conservation_postgres_t6.py`, `.artifacts/e73-lot04-conservation-02` : **18 réussites** (57,8 s) ; gains ouverts et réserve préservent l’archive, remise puis purge de l’identité sans effacer la preuve |
| Migrations complètes et rejeu | `test_data015_migrations.py`, base locale exclusive, `.artifacts/e73-lot04-migrations-02` : **3 réussites** (42,8 s), jusqu’à v271 incluant index réserve et compteur BIGINT |
| Animation | **191 tests Node**, **416 assertions dans 38 scénarios navigateur** à 320/1 280 px, régression chasse Coffrets **254 contrôles** à 390/1 280 px ; types, lint, build isolé et deux tests de contrats HTTP réussis |
| Marketplace | `npm run test:security` : **112 réussites** ; ESLint ciblé et build isolé réussis ; `external-animation-gain.spec.cjs` : **5 scénarios réussis** (34,8 s), lien email, reprise/expiration, pagination publique et états Live à 320/1 280 px |
| Pro, contrats consommateurs | Quatre fichiers Vitest contrat API/préparation/registre moteur/animations : **63 réussites** (13,71 s, export final) ; aucun parcours de consommation de lot externe ajouté |

Ces suites se recouvrent ; leurs nombres ne forment pas un total de tests distincts.
Les revues croisées ont fait corriger les curseurs malformés (400), l’ordre commun
de lecture/réservation des suppléants et le total BIGINT des unités. Le carnet Live
refuse une version inconnue et préserve les discriminants inconnus après stockage
et réimport ; il ne les requalifie jamais en Coffrets.

Le tirage a été mesuré avec 10 000 candidats et 1 000 lignes de lots : une tranche
de 500 attributions utilise 16 lectures SQL et environ 2,5 Mo de mémoire. Le
scellement externe produit deux écritures, indépendamment de la réserve. Les
plans utilisent les index de population et de classement, sans tri aléatoire ni
chargement intégral. Une dotation de trois milliards d’unités avec un participant
ne matérialise qu’une attribution. Cela ne démontre pas encore la charge
simultanée transverse du lot 10.

Les contrats générés E41/Live et les trois consommateurs moteur sont synchronisés.
Le [guide organisateur](../../produit/formation/animation/guide-animation-preproduction.md)
et la [procédure de tirage](../../exploitation/exploitation/gerer-tirages-libres-animation.md)
décrivent les états et reprises. La liste globale reste nommée **Tirages Coffrets** ;
les lots libres se suivent depuis chaque animation, avant unification au lot 09.
Le traitement effectif reste désactivé par défaut. Les recettes humaines et toute
activation hébergée restent non exécutées.

Dette étayée : `test_modification_animation_en_cours.py` donne **3 échecs et
1 réussite** (3,81 s) sur les sources du HEAD antérieur `4f3a3b16`, dans une copie
isolée. Les 2 032 fichiers app/scripts/tests et la configuration pytest sont
contrôlés contre l’archive Git (`.artifacts/e73-lot04-baseline-proof.json`).
Ces tests attendent encore le PATCH direct de `date_fin` après publication et
deux anciens messages ; le domaine exige désormais la commande versionnée des
paramètres d’exploitation. Le lot 04 ne modifie ni ces tests ni cette règle.

Revue SQL complémentaire : le plan de la deuxième page de suppléants parcourait
10 000 candidats par semi-jointure malgré le `LIMIT` apparent. La sonde scalaire
corrélée, bornée et indexable corrige ce parcours. Le test avec les pages initiale,
suivante et au rang 9 000 vérifie maintenant les requêtes réelles : une ligne
sondée et 26 lignes de page, aucun candidat filtré, tri final de 26 lignes,
32 à 33 buffers. Les temps ponctuels sont de 0,19 à 0,46 ms, sans forcer le
planificateur. Le plan fautif est conservé dans
`.artifacts/e73-tirage-libre-reserve-plans-avant-correction.json`.

La copie de l’index Animation `tmp/e73-lot04-staged` passe types et build isolé,
sans les quatre hunks utilisateur « Clôturer ». Le chunk principal de 907,80 ko
reste à découper au lot 09. Les commits d’interfaces du lot 04 sont locaux :
Animation `d0b92f7`, Marketplace `1473e05`, Pro `30aeed3`.

Après cette correction SQL, la revue indépendante a réexécuté
`test_attribution_lot_libre_dedicated.py`, `test_email_lot_externe.py` et
`test_tirages_libres_postgres.py` : **28 tests distincts réussis**, dont 16
PostgreSQL en 84,13 s (`tmp/e73-lot04-audit-pg-final-03`), deux avertissements
Starlette/AnyIO, aucun skip. Les trois plans de réserve sont conservés dans
`.artifacts/e73-tirage-libre-reserve-plans.json`. Le premier essai interrompu
pendant la récupération du PostgreSQL local ne vaut pas validation ; seuls
les résultats terminés sont retenus.

Compatibilité de démonstration complète :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot04-demo-compatibility-20261018-resume` : **7 réussites**
en 586,51 s, trois modules obligatoires, zéro skip, quatre avertissements de
réflexion SQLAlchemy. Les cycles installation, panne injectée, restauration et
reset utilisent uniquement les deux clusters jetables de cette tâche. XML et
log sont conservés dans le répertoire indiqué et son fichier `.log` voisin.
Les garde-fous du runner passent **31 tests** (0,35 s). Les ports locaux peuvent
être fournis explicitement et doivent être distincts ; le répertoire de sortie
doit être neuf dans `tmp/`, aucun résultat antérieur n’est effacé.

Le commit backend `7502282` clôt le travail applicatif local du lot 04. Les
générations transverses des dix lots, la charge simultanée, les recettes humaines
et les preuves d’hébergement restent à réaliser selon leur lot. Aucun push,
envoi fournisseur ou déploiement n’a eu lieu.

### Lot 05 — Bons numériques (en cours)

Le lot 04 documentaire est enregistré dans `87badb3`. Avant le lot numérique,
`tests/api/test_pin_validation_e70.py` passe **14 tests** (4,40 s, trois
dépréciations), runner isolé `tmp/e73-lot05-pin-baseline-01`.

Le protocole de préparation privée/scellement est étendu aux bons numériques
dans [tirage-libre-protocole.md](tirage-libre-protocole.md). `BonLot` possède la
validité, la consommation unique, la rotation, la révocation et la correction.
Les canaux QR/PIN partagent ce cœur ; le service de tirage conserve la politique
de population et remplacement. L'ordre de verrou a été précisé en faveur de
l'ordre E70 existant (demande avant cible), sans changer les règles produit.
Les preuves exécutées ci-dessous complètent ce protocole ; la finalisation du
flux d’historique et du cycle complet de démonstration reste en cours.

Périmètre réalisé : CA30 (modèles/version/exemplaires), CA31 (affectation et
libération explicite), branche numérique CA32/33 (tirage, attribution, email et
bon), CA34/35 (QR et PIN), CA36 (cycle et incidents). Les compléments CA15/19–22
réutilisent les périmètres courants et les acteurs principal/salarié, avec
continuité limitée au bon attribué. Cela ne clôt pas US24/36–38 ni l’epic entière.

Le bon appartient à `animation_locale`. Les capacités de consultation, la
signature QR et le rendu email sont des adaptateurs ; le PIN E70 orchestre la
même transition de remise. Une consommation active unique subsiste sous deux
scans salariés ou QR/PIN concurrents. Une correction conserve la preuve initiale
et n’autorise pas le rejeu d’une ancienne demande à consommer de nouveau.
Les gardes du commerce précèdent les verrous de demande/cible ; la suspension
et la révocation personnelle restent prioritaires sur toute continuité.

La migration `v272` crée onze tables numériques, les références et contraintes
d’exclusivité ainsi que les index. L’origine de lien existante est réutilisée.
Les clés QR et flags de workers sont documentés sans secret dans le modèle de
configuration et la [procédure des bons numériques](../../exploitation/exploitation/gerer-bons-numeriques-animation.md).
Les trois branches de dotation restent explicites et exclusives.

### Preuves locales du lot 05

Toutes les commandes Python ci-dessous utilisent
`.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py`
depuis le backend, avec `--basetemp` neuf. Les tests SQL utilisent exclusivement
`127.0.0.1:55473/localeo_audit_test` ou la base de migrations jetable dédiée.
Les suites se recouvrent : leurs nombres ne sont pas un total de tests distincts.

| Contrôle | Résultat réel |
| --- | --- |
| Architecture, recensement domaine et use cases | `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py`, `tmp/e73-lot05-architecture-final-02` : **519 réussites** (10,02 s) |
| Inventaire, BonLot, ports, crypto et choix de dotation | 28 réussites initiales ; après correction des métadonnées des huit types dédiés, **21 réussites** domaine/registre/crypto, sans exclusion de contrôle |
| PG inventaire/remise, conservation numérique et Animation, API inventaire | `test_inventaire_bons_postgres.py`, `test_conservation_bons_numeriques_e73.py`, `test_conservation_postgres_t6.py`, `test_inventaire_bons_lots_e73.py` : **32 réussites** (120,08 s), `tmp/e73-lot05-inventaire-conservation-03` |
| Compléments inventaire et droits | Génération 251 unités en 100/100/51, reprises concurrentes, isolation de reçus, libération de surplus : **3 réussites** (10,48 s) ; lecture Lecteur sans commande, isolation/rejeu : **3 réussites** (9,94 s) |
| Tirage numérique, email, accès personnel et scellement | **51 tests uniques réussis** : suite principale 50/50 (279,66 s), puis 15/15 sur les tirages après ajout du contrôle de budget avant chaque page, dont un nouveau test ; `tmp/e73-lot05-w2-final` et `tmp/e73-lot05-w2-budget-final` |
| PIN numérique | `test_pin_bons_lots_postgres.py` : **9 réussites** (65,03 s), `tmp/e73-lot05-pin-pg-03` : courses QR/PIN principal/salarié, correction/rejeu, rotation, rollback de notification, PIN bloqué mais QR autorisé, retrait et suspension |
| Transport API PIN | `test_pin_bon_lot_e73.py test_pin_validation_e70.py` : **22 réussites** (11,93 s), `tmp/e73-lot05-pin-transport-02` |
| Régression PIN Coffrets/Animation/salariés | Suite initiale : 19 réussites, deux échecs sur le formatage SQL de l’historique ; correction puis reprise des trois cas concernés : **3 réussites** (65,36 s), `tmp/e73-lot05-pin-regressions-02` ; 21 tests distincts finalement validés |
| Migration complète et rejeu | `test_data015_migrations.py` jusqu’à v272 : **3 réussites** (83,40 s), avant l’ajout éventuel des index du flux d’historique ; contrôle final à compléter |
| Animation | **197 tests Node réussis** après copie des contrats ; types, lint et build isolé réussis ; navigateur **38 scénarios/416 assertions** de régression lot 04 et **10 scénarios/100 assertions** numériques à 320/1 280 px |
| Localeo Pro | QR bons et contrats : **60 tests ciblés distincts** validés, build et quatre scénarios navigateur réussis avant passage de l’historique au flux ; complément à enregistrer |
| Live, stockage et discriminants | `node --test tests/security/library-backup.test.cjs tests/security/animation-gain.test.cjs` : **8 réussites** (8,76 s), restauration d’accès propre à chaque bon, aucun QR/consigne/coordonnée privée persisté |
| Live, navigateur | `digital-lot.spec.cjs` : **4 scénarios réussis** en production locale après correction de contraste ; même suite **4 réussites sous React StrictMode** avant retouche de présentation, capacité de fragment préservée ; 320/1 280 px, heure de Paris malgré navigateur New York, états terminaux, réseau indisponible, PIN dont la réponse est perdue |
| Live, analyse et build | ESLint ciblé réussi et Vite isolé réussi ; la limite préexistante du lint global sur le répertoire de travail EPERM reste celle du lot 04 |
| Générateur ciblé | **14 tests PG/registre** (6,57 s), puis **6 tests unitaires** ; deux modèles, cinq exemplaires, trois affectés et deux disponibles, aucun bon/QR/email prématuré ; onze tables classées `replace` |

Le scellement numérique a été mesuré avec 10 000 candidats, 1 000 bons et
120 commerces : **37 requêtes, deux écritures finales, environ 716 Ko de mémoire**,
au plus seize lectures par tranche préparatoire. Les gardes de commerce sont
prises seulement au scellement, par pages de cent ; délai de verrou de trois
secondes et budget de vingt secondes avec rollback/reprise testés. Ce n’est
pas encore la preuve de charge simultanée transverse du lot 10.

Deux revues indépendantes ont contrôlé les branches tirage/bon et PIN/droits.
Elles ont conduit à corriger les reçus inter-organisations, les actions proposées
aux Lecteurs et le calcul UTC des quatre-vingt-dix jours d’historique Animation.
Six tests de frontière échouaient avant correction (changement d’heure,
configuration/date/surcharge). Le flux par curseur est désormais intégré dans
Pro ; ses **19 tests PostgreSQL/API** passent, sans skip (83,67 s), puis les
quatre tests API repassent après contrôle des dates HTTP extrêmes (3,60 s).
L’ancienne route reste compatible avec un offset limité à 10 000.

Le cycle complet de démonstration a révélé **quatre échecs et trois réussites**
sur une clé étrangère modèle/version lors de la génération. Ce défaut a été
reproduit et corrigé ; le cycle final passe **7 tests** en 557,78 s, avec quatre
avertissements SQLAlchemy de réflexion `dialect_options`, sans skip.
Le runner `scripts/validation/run_demo_compatibility_tests.py` a utilisé
uniquement les clusters jetables `127.0.0.1:10407` et `127.0.0.1:55448`, avec
sortie `tmp/e73-lot05-demo-compatibility-20261018-final03` : génération,
dump/installation, échec contrôlé, restauration et reset. Le refus initial
sur une base jetable non vide a été résolu en recréant seulement cette base,
après vérification de son répertoire local et de l’absence de connexions.
Aucun environnement partagé n’a été contacté.

Le besoin nominatif du gain numérique est raccordé à la conservation existante :
remise/révocation ferment ce besoin, correction le réouvre ; un engagement
expiré mais non résolu et les autres gains/gels conservent leur effet propre.
La purge physique bornée des capacités et contextes expirés/révoqués sera
raccordée au dispositif commun au **lot 10, avant ouverture**. Les preuves
humaines, le transport réel et l’hébergement restent non exécutés.

Compléments de finalisation :

- PIN numérique/API E70 et contrats moteur relancés après les corrections :
  `test_pin_bons_lots_postgres.py test_pin_bon_lot_e73.py
  test_pin_validation_e70.py test_contrats_moteur_t1.py`,
  `tmp/e73-lot05-root-pin-final-04` : **51 réussites** (36,18 s), trois
  avertissements de dépréciation, zéro skip.
- Le défaut de clé étrangère est reproduit avec les contraintes réelles dans
  `test_modele_generation_et_unites_meme_uow_respectent_vraies_cles_etrangeres`.
  `sauver_modele()` persiste maintenant la version avant l’opération suivante,
  sans commit intermédiaire ; le test passe (**1 réussite**, 5,20 s). Le
  générateur ne contourne aucune contrainte.
- Après ajout des cinq index du flux Pro dans v272 : migrations/rejeu et
  générateurs OpenAPI, `tmp/e73-lot05-migrations-contrats-final-03` :
  **11 réussites** (54,82 s). E41 expose 828 routes, E42 en expose 55 ; copie
  consommateur Animation/Pro effectuée, quatre contrats Pro réussis.
- Live : le scénario de changement de bon ignore la réponse tardive du précédent
  et masque immédiatement son QR. La suite finale sous React StrictMode passe
  **5 scénarios**, dont 320/1 280 px et les états de remise. Les callbacks du carnet
  sont également liés au bon courant. Le serveur passe **13 tests**, dont le
  fallback SPA du lien personnel avec `no-store`. Les fermetures Playwright
  Windows nécessitent l’arrêt du seul serveur local créé par le test après
  exécution réussie ; aucun service distant ou autre processus n’est arrêté.
- Pro : **67 tests unitaires** puis 27 revalidés après la normalisation d’erreur,
  **11 scénarios navigateur** (six nouveaux/Paris et cinq régressions), build
  isolé et quatre contrats finaux réussis. Les filtres suivent les journées
  Europe/Paris même depuis New York, y compris les transitions de 23/25 heures.

- Pro, relecture d’un résultat incertain : identité du bon et de l’opération
  vérifiées ensemble ; aucun rejeu avec le contexte d’un autre bon. **17 tests
  unitaires et quatre scénarios navigateur** passent après ce durcissement.
- Architecture finale : même commande que ci-dessus,
  `tmp/e73-lot05-architecture-final-03` : **519 réussites** (15,46 s).
- Régression des passages salariés E72 : remplacement du test d’une méthode
  privée supprimée par les lectures SQL avant/à l’échéance, avec contrôle du
  maintien des preuves. Échec reproduit puis fichier entier
  `test_animation_salaries_e72.py` : **4 réussites**, aucun skip (9 s),
  `tmp/e73-lot05-historique-salarie-final`.
- Animation : copie isolée HEAD + seuls fichiers du lot 05 dans
  `tmp/e73-lot05-staged`, sans configuration opérateur ni modifications
  préexistantes « Clôturer » : types, lint, build et **huit tests de contrats**
  réussis ; manifestes d’empreintes conservés dans les artefacts locaux.

### Performance de l’historique et limites à solder au lot 10

Le nouveau flux effectue six requêtes repository constantes, sans `COUNT` ni
`OFFSET`. Les essais avec 30 000 occurrences, une page profonde à 27 000,
des filtres de mode et collisions de date/UUID entre types utilisent les index
avec au plus 26 occurrences par branche pour une page de 25. La rétention
des bons s’appuie sur une borne calendaire indexée exacte de cinq ans,
y compris les années bissextiles. Avec 10 000 bons expirés : aucune occurrence
lue ni jointure, environ 0,52 ms dans la mesure locale.

**Exception transitoire E73-PERF-02/04 à solder au lot 10 avant ouverture :**
la sélection des anciennes validations Coffrets/Animation dépend encore de
l’expiration portée par leurs objets parents. Les plans avec 10 000 occurrences
expirées lisent 10 000 validations et interrogent leurs archives/surcharges
(environ 38 ms Coffrets et 206 ms Animation). La réponse et le nombre de requêtes
sont bornés, mais ce travail SQL augmente avec les archives. Le lot 10 doit
raccorder un filtrage indexable à la politique canonique d’expiration, puis
rejouer ces plans ; ne pas présenter le flux comme une preuve de coût constant
pour tous les historiques. Les plans sont enregistrés dans
`.artifacts/e73-historique-flux-performance.json` et
`.artifacts/e73-historique-flux-expiration.json` du backend.

Commits locaux du lot 05 : backend `1cd9564`, Animation `2eee756`, Pro `63b64bc`,
Marketplace/Live `8e54957` ; sources dans le commit documentaire du lot 05.
Les seules modifications étrangères à ce lot sont
préservées hors index. Aucun push ni déploiement.

### Lot 06 — Import et protection des corrections locales

Périmètre : US19–20 / CA42–45, avec consommation des droits du lot 03.
Le domaine Référencement porte le lot d’import, les résolutions et la
provenance à trois versions. L’application orchestre une transaction par
ligne, avec le référencement et OnBoard ; le portail expose les décisions
et la progression. Le transport reste dans le namespace d’import, distinct
des mutations ERP. La [procédure d’import](../../exploitation/exploitation/importer-commercants-animation.md)
décrit les commandes et contrôles vérifiés localement.

Première preuve d’intégration :
`scripts/validation/test_isolated.py tests/security/test_imports_browser_e73.py
tests/security/test_animation_browser_session.py -q --tb=short
--basetemp tmp/e73-lot06-browser-root-01` : **118 réussites** (14 s), deux
avertissements de dépréciation, aucun skip. Dépôt multipart avec origine,
cookie/CSRF, lecture privée et refus des routes Référencement/ERP étrangères.
Cette preuve de transport ne valide pas encore le traitement métier complet.


Parcours intégrés : source Excel/CSV privée, flux stable, mapping explicite,
aperçu et rapprochement email avec contrôle d’identité, choix champ par champ,
import partiel, commandes idempotentes et reprise des seules lignes restantes.
Les créations passent par Référencement et OnBoard : brouillon à vérifier,
sans compte, invitation, périmètre actif ni participation. Les corrections
SIRET/commune sont décidées dans l’ERP ; un déplacement de commune rend la
fiche opaque à l’ancien import. Une incohérence avec le profil financier
courant bloque les nouveaux usages concernés, sans modifier les documents
émis. Après demande ERP, le mapping est figé pour préserver sa preuve ; un
nouveau dépôt dans le même flux permet de corriger les colonnes.

La migration locale `v273_imports_commercants.sql` crée les sept tables et les
index des flux/plans/provenances/vérifications, et accepte une catégorie
absente uniquement pour une fiche en brouillon. L’ouverture reste désactivée
par défaut (`LOCALEO_IMPORTS_COMMERCANTS_APPLY=false`) ; le catalogue ne propose
pas l’achat d’un parcours fermé. Le middleware borne aussi le corps multipart
avant parsing, indépendamment de Content-Length ; parseur, stockage et SQL
du dépôt s’exécutent hors boucle ASGI.

Revue croisée : correction d’un reçu créé avant la disponibilité effective du
fichier. Le client conserve fichier et clé jusqu’à disponibilité confirmée ;
panne avant/après stockage puis reprise explicite ne crée pas de second lot.
Les contrôles de version, les gels de conservation, la reprise après premier
traitement et les mises à jour de commune ont fait l’objet de cas PostgreSQL.
Les gels sont exclus de la sélection des purges puis revérifiés sous verrou,
pour ne pas bloquer les opérations suivantes. Les sources et instantanés de
travail sont purgés après trente jours ; provenance et audit restent distincts.

Preuves finales disponibles (préfixe backend :
`.artifacts/python-e70/runtime/python.exe scripts/validation/test_isolated.py` ;
les suites se recouvrent, leurs totaux ne s’additionnent pas) :

| Contrôle | Résultat local |
| --- | --- |
| Domaine import, API et rejet ERP/remapping | **38 réussites**, `tmp/e73-lot06-core-final-06.xml` ; dépôt hors boucle ASGI inclus |
| Changement de commune bout en bout | **1 réussite**, `tmp/e73-lot06-core-commune-07.xml` ; adresse atomique et confidentialité après déplacement |
| Référencement/OnBoard, corrections ERP, domaine/API/assets | **23 réussites**, `tmp/e73-lot06-preparation-final-03.log` ; concurrence et correction de commune incluses |
| Raccord fiscal et facture assistée existante | **23 réussites**, `tmp/e73-lot06-fiscal-coherence-01.log` ; snapshots inchangés et usages incohérents refusés |
| Garde-fous architecture, recensement, transport navigateur, limites multipart, parseur adversarial et readiness catalogue | **576 réussites**, `tmp/e73-lot06-architecture-final-03` ; deux avertissements de dépendances, aucun skip |
| Migration depuis la base vide, rejeu et compatibilité modèles | **3 réussites**, `tmp/e73-lot06-migrations-final-04` ; PostgreSQL jetable uniquement |
| Animation, copie HEAD + seuls fichiers du lot 06 | **206 tests Node**, types/lint/build réussis ; **22 scénarios navigateur, 292 assertions**, 320/1 280 px ; pas de configuration opérateur ni des changements préexistants Clôturer dans la copie |
| ERP vérifications d’import | Navigateur réussi à 320/1 280 px : motif, lecture seule, CSRF/idempotence, réponse perdue réconciliée, textes échappés |
| Sources et liens documentaires | **94 guides / 1 001 liens**, zéro erreur/alerte ; **126 sources exportées** vérifiées |

Performance : une prévisualisation de **100 lignes parmi 10 000 commerces**
utilise **trois requêtes groupées**, avec candidats bornés et enrichissement par
clé ; aucun balayage de la table des commerces dans le plan mesuré. Les pages
d’imports de 1 et 100 éléments prennent toutes deux **13 requêtes**, avec pics
mémoire Python d’environ 454 et 664 ko. La page profonde après 9 000 imports
utilise un Index Scan de 26 lignes, sans OFFSET. Ces mesures locales ne valent
pas preuve de capacité hébergée. Artefacts backend :
`.artifacts/e73-import-preparation-performance.json` et
`.artifacts/e73-imports-pagination-performance.json`.

Le chunk import Animation est chargé séparément (40,82 ko). L’avertissement
sur le bundle principal de 934,60 ko reste rattaché au lot 09. Pro et Live ne
consomment aucune nouvelle route d’import et ne reçoivent aucun accès implicite ;
aucune modification fonctionnelle n’y est nécessaire pour ce lot. La recette
humaine Localeo/Martignas-sur-Jalle et les essais d’hébergement restent à faire.

Derniers contrôles : **16 tests PostgreSQL complets du noyau import réussis**
(311,03 s, `tmp/e73-lot06-core-proof.md` dans le backend) ; **10 tests des
exports OpenAPI réussis**, `tmp/e73-lot06-contracts-final` (72,37 s).
Les exports canoniques E41/E42 comportent respectivement 844 et 55 routes ;
E42 conserve ses routes Live et reçoit seulement les schémas communs actualisés.
La copie embarquée Animation est synchronisée. Les fins de lignes et espaces
terminaux SQL sont normalisés sans changement sémantique.

Générateur et restauration complète : **7 tests réussis**, quatre avertissements
SQLAlchemy de réflexion, 855,49 s. Commande exécutée dans le backend :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot06-demo-complete-01`. Deux imports synthétiques passent
par les services, conservent une correction locale puis purgent leurs sources
avant export. Le wrapper transactionnel du générateur restaure ses budgets
SQL après chaque sous-transaction ; les limites runtime restent inchangées.
Les premiers essais incomplets ne servent pas de preuve finale.

Commits locaux du lot 06 : Backend `bb4e1e8`, Animation `955fb94`, sources dans
le commit documentaire du lot 06. Les changements préexistants
Clôturer/Exploitation/README restent hors commit ; les fichiers de préparation
du lot 07 sont exclus du commit backend du lot 06. Aucun push ni déploiement.

### Lot 07 — Chasse et préparation accompagnée

Périmètre : US18/30, CA46/57. La chasse conserve son quota dédié, consommé à
publication et non à la demande, au complément ou à la reprise technique. Le
suivi accompagné distingue complétude, préparation, complément attendu,
préparation prête, reprise et annulation. La cible de cinq jours ouvrés repose
sur un calendrier Localeo explicite et figé ; une attente suspend ce décompte.
Le portail présente cible initiale, estimation révisée et retard séparément.
L’ERP permet le traitement sans dépendre de l’Atelier Coffrets. Les messages de
service passent par l’outbox email ordinaire, indépendamment du futur module
Communication participants.

La validation terrain est une preuve de l’animation, de sa révision et de son
empreinte. Une modification pertinente l’invalide ; un modèle réutilisé ne la
transporte pas à la nouvelle édition. Les sessions et habilitations courantes
sont revérifiées avant les commandes et reçus. Le catalogue commercial et les
anciennes commandes de forfait contenant la chasse consomment la même
disponibilité technique injectée : ouverture explicite et calendrier valide.

Migration locale : `v274_preparation_accompagnee.sql`, suivi/événements/terrain,
projections et index des sélecteurs, opérations et tentatives. Les reprises de
données incohérentes échouent atomiquement avec un diagnostic ; elles ne
créent aucun droit ni service historique fictif. La surveillance des retards
est bornée, simulée par défaut, et indépendante de l’ouverture de nouvelles
demandes. Elle écrit une alerte unique par demande/version d’échéance, sans
modifier la version métier à chaque passage. Ops lit au plus 26 références
et affiche une borne `25+` si nécessaire.

La [procédure de préparation accompagnée](../../exploitation/exploitation/preparer-chasse-accompagnee.md)
décrit les responsabilités, le calendrier et les configurations préparées :
`LOCALEO_PREPARATIONS_ACCOMPAGNEES_APPLY`,
`LOCALEO_PREPARATIONS_ACCOMPAGNEES_ALERTES_APPLY`,
`LOCALEO_CALENDRIER_SERVICE_JSON`. Aucune valeur d’horaire métier ni ouverture
d’environnement n’a été imposée.

Preuves exécutées à ce stade, sans additionner les suites qui se recouvrent :

| Contrôle | Résultat local |
| --- | --- |
| Architecture, recensements, domaine, application et API | **621 réussites**, 31,96 s ; `tmp/e73-lot07-architecture-final18.xml`. La passe précédente avait 15 erreurs de préparation du répertoire Windows global, résolues par le répertoire isolé du dépôt sans changer les assertions |
| Génération E55, suivi accompagné, conservation et pagination PostgreSQL | **53 réussites**, 194,77 s ; `tmp/e73-lot07-pg-final16.xml` |
| Préparation historique et contrôle de publication terrain | **38 réussites**, `tmp/e73-lot07-publication15.xml` |
| Exports OpenAPI documentaires | **10 réussites**, 76,66 s ; `tmp/e73-lot07-contracts-final-01`. E41 : 876 chemins ; E42 : 55. E41 embarqué Animation identique au canonique après normalisation des fins de ligne |
| Calendrier, surveillance, disponibilité catalogue et régression tableau Ops | **29 réussites**, `tmp/e73-lot07-root-final-02` |
| Disponibilité injectée dans les commandes de forfait et régressions souscriptions | **43 réussites**, quatre avertissements de dépréciation ; `tmp/e73-lot07-readiness-regression-01` |
| Migration complète depuis une base vide, rejeu et modèles | **3 réussites**, 78,46 s ; `tmp/e73-lot07-migrations-final-03` |
| Reprise de projections historiques et rollback sur incohérence | **2 réussites**, `tmp/e73-lot07-reprise-01` |
| Surveillance concurrente et lecture Ops avec historique volumineux | **2 réussites**, `tmp/e73-lot07-surveillance-pg-03` |
| Sélecteurs PostgreSQL | **3 réussites** ; 26 plans sur 10 000 lieux, 10 000 modèles et 10 000 commerces ; deux requêtes par page, aucun balayage séquentiel des catalogues |
| Portail Animation, copie HEAD + seuls fichiers du lot | **212 tests Node**, types/lint/build réussis ; suivi **18 scénarios/234 assertions**, génération **74**, préparation chasse **258**, mobile/bureau et affichage Paris |
| ERP préparation et génération | Recettes navigateur 320/1 280 px et 390/1 280 px réussies ; action accessible sans Atelier Coffrets |
| Sonde du générateur synthétique | **1 réussite**, 85,09 s ; vérification globale du jeu, droits client/lecteur, complément réel et absence de débit de publication |

Les performances des opérations ont été éprouvées avec 10 000 opérations du
tenant, 10 000 opérations antérieures d’autres tenants et 10 000 tentatives :
pages 1/100 en deux requêtes, sans plan forcé et sans chargement des gros
résultats. Le détail borne ses tentatives à 25 et fournit la suite paginée.
La surveillance a également été mesurée avec 10 000 archives, 10 000 demandes
en attente et 201 actives, sur les index partiels de file et d’Ops. Artefacts :
`.artifacts/e73-preparation-pagination-performance.json`,
`.artifacts/e73-selecteurs-performance.json` et
`.artifacts/e73-preparations-alertes-performance.json`.

Revue croisée : corrections des contrats de curseur, de la revalidation de
session, du lien d’email vers la route réelle du portail et de deux dépendances
vers l’infrastructure. Les reprises automatiques E55 ne sont pas bloquées dès
la première erreur transitoire ; leurs dates historiques sans fuseau sont
écrites et comparées en UTC. Les sources du générateur préservent l’ordre
global des verrous et emploient une période annuelle cohérente avec les droits.

La revue indépendante des raccords de surveillance et de disponibilité n’a
relevé aucun défaut bloquant (`tmp/e73-lot07-revue-root-w2.md` dans le backend).
Les contrôles documentaires passent : **94 guides / 1 003 liens**, aucune erreur
ni alerte, et **127 sources exportées**. Le premier contrôle d’export a détecté
un identifiant de bundle utilisant le chemin source ; il a été corrigé vers
le namespace documentaire `docs/ops`, sans déplacer la source canonique.

Générateur et restauration : la suite complète a réussi **7 scénarios sur 8**
(360,05 s, quatre avertissements de réflexion SQLAlchemy,
`tmp/e73-lot07-demo-complete-02`). Le huitième a identifié un contrôle de fixture
qui comptait les versions de configuration comme des animations distinctes.
La correction vérifie toutes les versions, dix animations avec chacune un
visuel cohérent et dix visuels distincts. Elle conserve les contrôles stricts
de neutralisation des emails et emploie de vraies sessions synthétiques pour
les lectures produit désormais protégées. Ce seul scénario a été rejoué avec
succès : **1 réussite**, 56,50 s, un avertissement de réflexion,
`tmp/e73-lot07-demo-relations-reprise-01.log`. Les sept scénarios non modifiés,
dont export/restauration, n’ont pas été rejoués inutilement. Aucun échec n’est
masqué. Une ligne vide finale de v274 a été supprimée au contrôle Git, sans
modifier son SQL ; aucune base partagée n’a été touchée.

Commits locaux du lot 07 : Backend `44c6429`, Animation `8979893`, sources dans
le commit documentaire du lot 07. Aucun push ni déploiement.
Pro et Marketplace ne consomment pas ces nouvelles routes. Les deux sélecteurs
historiques exhaustifs restant dans App et le bundle principal Animation sont
suivis aux lots 09/10. La conservation physique des nouvelles familles reste
à prouver au lot 10. Recette humaine et hébergement : non exécutés.

### Lot 08 — Communication participants

Périmètre : US21–22, CA47–49. Le portail propose préparation, aperçu,
programmation, confirmation, rapport et reprise d'une campagne. Les quatre
groupes restent limités à une animation. L'état de traitement, le dépôt Live
et le résultat Push sont distincts. Les dates sont affichées en Europe/Paris.
Les formulaires préservent les propositions et réconcilient une réponse perdue
par reçu avant toute répétition explicite de la même commande.

Le domaine possède les transitions et décisions de fenêtre, préférence,
sollicitation et audience. L'application capture puis prépare une audience
durable par lots, débite un crédit au premier dépôt Live et reprend sans
modifier audience ou compteur. Le transport est séparé, avec baux et intentions
durables ; les fournisseurs sont simulés dans toutes les preuves. Une campagne
sans destinataire autorisé ne consomme aucun crédit.

La préférence organisateur est explicite et indépendante du consentement
historique aux notifications. Le message est disponible sans installation Push,
puis peut être lu après liaison personnelle vérifiée d'un carnet. Les listes
fusionnent des pages bornées et n'exposent aucun endpoint ou secret. Un retrait
de préférence, de droit ou une suspension reste contrôlé côté serveur.

L'ERP permet de consulter le réglage communal et les alertes, puis de les
modifier avec l'autorisation dédiée `animation:sollicitation_gerer`, un motif et
une version. La configuration initiale reste 1 message/24 h et un seuil à 3×.
Les alertes sont regroupées par commune/période, avec un email interne à leur
ouverture ; ni reprise ni clôture ne remettent la fréquence à zéro. Une garde
partagée du réglage empêche sa modification concurrente pendant la décision.

Migration `v275_campagnes_organisateur.sql` : 23 tables dédiées, index de listes,
files et purges, nouvelles dates effectives Animation et permission ERP sans
octroi automatique. Le backfill exige des preuves de publication et de clôture,
dont un gel de population pour cette dernière. L'absence de preuve conserve une
fenêtre à vérifier. La migration n'active aucun module ni worker.

Preuves root déjà exécutées (runner backend isolé ; suites recouvrantes) :

| Contrôle | Résultat local |
| --- | --- |
| ERP PostgreSQL/API/configuration | **24 réussites**, `tmp/e73-lot08-root-pg04.xml` : CAS, concurrence, rollback email/alerte, grant/session révoqués dans la composition réelle, garde tenant contre suspension |
| Disponibilité commerciale et configuration finale | **13 réussites**, `tmp/e73-lot08-readiness02.xml` ; trousseau, emails internes, VAPID et flags des deux workers requis pour les nouveaux usages |
| Exécuteur campagnes | **8 réussites**, `tmp/e73-lot08-execution.xml` ; simulation sans claim/écriture et budget avant le lot suivant |
| Migration vide/rejeu/atomicité/modèles et reprise historique | **4 réussites**, 62,44 s, `tmp/e73-lot08-migrations02.xml` ; PostgreSQL local jetable, schéma final des 23 tables |
| Réponses HTTP Animation | **11 réussites**, `tmp/e73-lot08-responses02.xml` ; deux réponses antérieures complétées dans OpenAPI sans changer leur JSON |
| ERP mobile/bureau | `node tests/browser/epic73-sollicitations.cjs` réussi à 320/1 280 px : 404 du reçu puis renvoi de même clé, attente202, CAS409 avec proposition reprise et confirmation, pagination, lecture seule, texte échappé et Paris |
| Chargement réel du module ERP | **6 réussites**, deux avertissements de dépréciation, `tmp/e73-lot08-assets03.xml` : contrôle HTTP de la page et du module `sollicitations.js` ; ajout de ce fichier à la liste d'assets autorisés, oubli non détectable par la recette navigateur servie sur des fixtures |
| Campagnes : domaine, PostgreSQL, HTTP réel, HMAC et performance | **54 réussites**, 182,49 s, `tmp/e73-lot08-pg12.xml` ; débit concurrent du dernier crédit, rollback du premier dépôt, audience figée et fenêtre après démarrage |
| Participants et synchronisation existants | **8 réussites**, `tmp/e73-lot08-legacy01.xml` |
| Derniers cas campagnes et recensement | **33 réussites**, `tmp/e73-lot08-target14.xml` : 30 tests domaine, recensement complet et roundtrip UTC sous fuseau SQL Europe/Paris ; reprise du cas de fixture signalé dans `final13` |
| Architecture et API antérieures | **586 réussites** dans `tmp/e73-lot08-architecture02.xml` et un échec de déclaration de preuve ; ce dernier est corrigé et rejoué dans `target14`, sans skip ni exclusion |
| Exports documentaires et contrat Live | **10 réussites**, `tmp/e73-lot08-contracts03.xml` ; E41 **896 routes**, E42 **60 routes** |
| Live, préférences, transport, concurrence et purge | Ensemble de **47 tests distincts** validés au fil des suites W2 : 17 PostgreSQL, 11 domaine, 9 API, 9 transport/CLI et 1 performance ; détails dans la note locale backend `tmp/e73-lot08-preuves-w2.md` |
| Animation, seuls fichiers du lot dans une copie du HEAD | **220 tests Node**, types/lint/build réussis ; **36 scénarios navigateur / 684 assertions**, 320/1 280 px et fuseau Los Angeles ; trois contrats campagnes rejoués après l'export définitif |
| Marketplace / Live | **113 tests de sécurité**, lint ciblé réussi, **12 scénarios navigateur** (neuf antérieurs et trois nouveaux) ; les trois nouveaux rejoués avec code natif 0 après un avertissement de l'enveloppe PowerShell |
| Accessibilité Live additionnelle | **1 scénario réussi**, 21,3 s : 320 px et texte agrandi à 200 %, navigation clavier, accord/retrait/lecture/fermeture sans débordement ; le débordement du titre constaté à la première passe a été corrigé, captures inspectées |
| Démonstration et cycle complet sauvegarde/transfert/restauration | **9 réussites**, aucun échec ni skip, 509,77 s, `tmp/e73-lot08-demo-complete02/results.xml` ; scénario Communication avec les deux flags finaux ; six avertissements SQLAlchemy de réflexion. L'exécution précédente interrompue ne constitue pas une preuve |

La page profonde d'alertes parmi **20 000 lignes** (10 000 dans la commune et
10 000 ailleurs) utilise l'index communal et lit 26 lignes pour une page de 25,
sans OFFSET ni balayage de l'autre commune. Une première assertion avait détecté
l'emploi de l'index global ; le curseur inclut désormais la commune dans la
comparaison, sans forcer le plan ni affaiblir le test. Artefact local backend :
`.artifacts/e73-sollicitation-performance.json`.

Campagnes : sur **10 communes et 10 000 participants**, les pages de 1 et 100
éléments utilisent chacune 20 requêtes. Dix lecteurs simultanés ont pris de
0,191 à 1,039 s par lecture sur le poste local ; la capture de 1 000 participants
a pris 0,260 s. Les index sont vérifiés sans forçage du plan. Messagerie :
10 000 messages personnels, 10 000 notifications historiques et 10 000
participants ; deux pages et leurs cent faits exigent cinq requêtes, sans
balayage des grandes tables. Ces mesures ciblées ne démontrent ni le mélange
de parcours du lot 10 ni la capacité de l'hébergement cible.

Le chunk Communication est chargé à la demande (36,32 ko ; gzip 9,91 ko).
L'avertissement sur le bundle principal Animation reste pris en charge au lot
09. Le commit local Animation est `08f4d98` ; il contient seulement les 21
fichiers vérifiés, avec les quatre hunks Clôturer et les autres modifications
utilisateur préexistantes laissés hors index.

Marketplace : commits locaux `0fa79e4`, puis `c16bb30` pour le correctif
320 px/texte à 200 %, sans réécriture d'historique. Son lint global rencontre
un refus d'accès Windows dans le répertoire historique de sortie
`output/demo-generation/pytest-bum-registry` ; le lint des sources et des tests
touchés a réussi, sans ajout d'exclusion pour masquer ce refus.

Backend : commit local `2cda9d6`, 92 fichiers explicitement indexés. La commande
finale `run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot08-demo-complete02` a terminé avec le code 0. La base
de construction jetable a été recréée avant cette exécution après le retrait
d'espaces de fin de ligne dans v275 ; aucune empreinte de migration appliquée
n'a été contournée. Les sources et l'index sont restés figés pendant la preuve.

La revue indépendante a corrigé la fenêtre +30 jours dans les reprises et la
projection du rapport pour ne pas restituer de compteur technique hors contrat.
Les contrôles globaux ont également révélé deux réponses anciennes non décrites
(batch d'exemplaires et demande de mot de passe), désormais modélisées. Les
premiers contrôles de recensement ont signalé des classes sans preuve dédiée ;
leurs résultats ne sont pas présentés comme une suite verte.

La [procédure Communication](../../exploitation/exploitation/communiquer-participants-animation.md)
décrit réglages, préférences, workers, rotations de clés et reprise. Les contenus
des messages suivent la politique Live existante ; le raccord transversal aux
gels/purges et la preuve après restauration des nouvelles familles restent au
lot 10. Les essais utilisateurs Localeo/Martignas et toute capacité hébergée sont
non exécutés. Aucun fournisseur réel ni environnement partagé n'a été utilisé.

### Lot 09 — Parcours, site, assistance et mesure

Les parcours sont implémentés et vérifiés localement ; les contrôles communs,
la démonstration complète et les commits applicatifs sont terminés. Le
[guide opératoire](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrit l'assistant, les éditions, les bilans, la recherche et le support privé.
Cette réalisation locale ne vaut pas mise en service ni clôture de l'epic.

Le support utilise le stockage Contact commun pour les messages et un canal privé
exclu des anciennes listes, détails et exports SQLAdmin. La portée de la demande,
les réponses et les notes internes relèvent de `DemandeSupportOrganisation` ; les
notes ne constituent pas une première réponse. Les droits courants sont contrôlés
avant lecture, écriture et réconciliation de reçu. Une réponse et son intention
email sont atomiques ; un échec de préparation annule l'ensemble.

L'assistant consulte les propriétaires des règles sans publier, modifier les
statuts ni consommer de crédit. La disponibilité du module est injectée depuis la
composition ; l'application ne lit pas un adaptateur de configuration. Un brouillon
peut être préparé avec un droit actif et un quota de publication épuisé.

Preuves exécutées par l'intégration :

- Support domaine et PostgreSQL : **20 réussites**, `tmp/e73-lot09-support-pg04.xml`.
- HTTP privé, ancien SQLAdmin et CLI de réconciliation : **9 réussites**, deux
  avertissements de dépréciation, `tmp/e73-lot09-support-http02.xml`. Le premier
  essai HTTP avait quatre réussites et un échec de fixture sans session Starlette ;
  cette fixture a été corrigée puis rejouée, sans changement d'assertion.
- Assistant, disponibilité et régression publication : **15 réussites**, deux
  avertissements, `tmp/e73-lot09-assistant01.xml`. Le contrôle PostgreSQL du quota
  sans écriture a également réussi dans `tmp/e73-lot09-support-http01.xml`.
- Support navigateur : commande `node tests/browser/epic73-support-organisations.cjs`
  réussie à 320 et 1 280 px, avec agrandissement effectif de chaque texte à 200 %,
  reçus 404/202, rechargement, conflit de version, pagination, notes et lecture seule.
  Captures locales inspectées ; dernier ajustement des libellés de succès rejoué
  avec le code 0 : réponse, note interne et changement de statut restent distincts.
- Migration depuis base vide, rejeu, atomicité et correspondance de tous les modèles :
  **3 réussites**, 221,45 s, `tmp/e73-lot09-migrations01.xml`, PostgreSQL local jetable
  `localeo_audit_migrations_test`. Aucun SQL appliqué à un environnement partagé.
- Premier contrôle d'architecture : 563 réussites, 15 erreurs de permissions du
  répertoire temporaire Windows et un échec de déclaration des preuves de quatre
  classes. Les déclarations ont été corrigées ; reprise avec `--basetemp` dédié :
  **586 réussites**, 44,52 s, deux avertissements, `tmp/e73-lot09-architecture02.xml`.
  Cette reprise vérifie aussi les routes HTML et le chargement réel du module Support.
- Régression Support et recherche publique temporairement indisponible : **65
  réussites**, 52,10 s, deux avertissements, `tmp/e73-lot09-support-regression01.xml` ;
  HTTP 503 explicite, sans cache ni détail interne, lorsque la projection manque.
- Architecture et recensement final après correction de publication : **580
  réussites**, 17,25 s, `tmp/e73-lot09-architecture-final.xml`.
- Contrats OpenAPI, export documentaire et réponses Animation : **21 réussites**,
  29,85 s, `tmp/e73-lot09-contracts-final.xml` ; E41 **925 routes**, E42 **62 routes**.
  Le contrat runtime final est recopié en LF auprès du consommateur Animation.

La revue indépendante a relevé une validation de publication historique susceptible
de synchroniser un statut après le débit du quota. Le contrôle est désormais sans
écriture : **16 tests PostgreSQL** prouvent la lecture pure, le rollback du débit et
le refus des reçus/commandes après révocation. Les fixtures T3 gardent leurs assertions,
avec une dotation explicite et un journal de débit réellement transactionnel. La
dernière régression HTTP brouillon/bilan a **14 réussites** après correction de huit
fixtures utilisant l'ancien appel de génération ; les assertions de refus restent
inchangées. Les entrées ERP conservent leur contrôle d'identité à l'entrée de requête.

Valorisation : **29 tests domaine/API/PostgreSQL**, puis **46 contrôles de
réconciliation/moteur/bilan** et **11 contrôles API historiques** réussis dans des
suites qui se recouvrent. La parité Coffrets est vérifiée sur PostgreSQL : deux
instances, deux prestations consommées sur trois, 20 euros et gagnants distincts.
Les mesures de progression restent indisponibles quand leur couverture est incomplète.

Performances locales, sans forçage du plan PostgreSQL :

- Bilans : **10 communes, 10 000 participants, 10 lecteurs simultanés** ; une requête
  d'agrégation pour une ou dix éditions, aucune population hydratée, pic mémoire
  observé 113 759 octets, p95 710 ms et maximum 714 ms. Artefact backend
  `.artifacts/e73-lot09-valorisation-performance.json`.
- Support : **20 100 demandes**, page profonde à 19 000, six filtres ; une requête
  et au plus 26 objets pour 25 résultats, plans indexés, 10 à 29 ms observés.
  Artefact `.artifacts/e73-lot09-support-performance.json`.
- Sélecteur Coffrets : **20 000 coffrets**, quatre requêtes pour une page de 25
  comme de 100 ; parité de couverture prouvée par six cas PostgreSQL. Artefact
  `.artifacts/e73-coffrets-selecteur-performance.json` et `tmp/e73-lot09-coffrets04.xml`.
- Recherche publique : **10 005 animations**, deux requêtes, tri/visibilité avant
  limite et plans indexés ; trois cas PostgreSQL réussis. L'ancien test de classement
  en mémoire a été adapté à la frontière SQL puis les **17 tests** ont réussi dans
  `tmp/e73-lot09-search-unit-final.xml`, après un échec de compilation du double SQL.

Animation : **230 tests Node**, trois contrats HTTP rejoués sur l'export final,
types/lint/build réussis sur une copie ne contenant pas les changements préexistants.
**26 scénarios navigateur / 293 assertions**, 320/1 280 px et texte 200 %, auxquels
s'ajoutent les régressions sélection et lots/configuration. La recette de création
vérifie désormais l'arrivée dans l'Assistant avant d'ouvrir la Configuration ; les
assertions de paiement, quantités et droits sont conservées. Les filtres du bilan
global sont préservés au retour, avec deux scénarios supplémentaires réussis.
Le bundle principal est ramené à **498,18 ko / 127,89 ko gzip** par chargement différé.

Marketplace/Live : **115 tests de sécurité**, **13 tests serveur**, lint ciblé et
build isolé réussis ; **10 scénarios navigateur**, puis une reprise mobile après
le dernier ajustement de la synthèse des communes. Les deux surfaces partagent le
socle et la valeur par défaut reste Coffrets. Aucun domaine n'est créé ni configuré.

La migration **v276** prépare les huit tables Support/Valorisation, leurs index,
le motif Support privé et la projection de recherche publique. La reprise de
recherche est une commande explicite, bornée et simulée par défaut ; aucune
configuration opérateur ni donnée d'exploitation n'est modifiée ici.

La démonstration a d'abord refusé une base de construction non vide. Après
vérification de la cible locale jetable et de l'absence d'animations/commerces,
cette seule base a été recréée. La passe suivante a été interrompue après cinq
échecs : le scénario ajoutait des objectifs sur une nouvelle édition dont l'UUID
ne respectait pas l'ordre des coordinations déjà verrouillées par le générateur.
Le scénario règle désormais les objectifs sur le brouillon historique déjà
verrouillé et conserve l'édition nouvellement créée vierge. Le produit et ses
contrôles de verrous ne sont pas assouplis. La reprise ciblée réussit : **1 test**,
77,06 s, `tmp/e73-lot09-demo-target01.xml`, avec rechargement des huit tables.
Les unités du générateur et son registre comptent **23 réussites**, aucun skip.
Ces passes intermédiaires ne remplacent pas le résultat du runner complet.

Le runner complet a ensuite réussi sur les sources finales : **10 réussites**,
aucun échec ni skip, **571,16 s**, sept avertissements SQLAlchemy de réflexion
`dialect_options`, code de sortie 0. Artefact backend :
`tmp/e73-lot09-demo-complete03/results.xml`. Commande :
`scripts/validation/run_demo_compatibility_tests.py --disposable-postgres
127.0.0.1:10407,127.0.0.1:55448 --pg-bin-dir "C:/Program Files/PostgreSQL/18/bin"
--output-dir tmp/e73-lot09-demo-complete03`, avec le runtime Python local isolé.
Elle couvre les scénarios métier, le transfert, la reprise après interruption
et la restauration de la base d'origine jetable. Aucun fournisseur réel ni
environnement partagé n'a été utilisé.

Contrôles documentaires finaux : **98 guides, 1 085 liens, zéro erreur ni
avertissement** ; **129 documents exportables** vérifiés. Les contrats E41/E42,
le contrat embarqué Animation et le guide opératoire sont synchronisés.

Commits locaux applicatifs : Backend **`76103d7`** (94 fichiers), Animation
**`eb3def9`** (30 fichiers), Marketplace **`70d7128`** (21 fichiers). Les quatre
modifications préexistantes Clôturer d'`App.tsx`, ainsi que le README, la vue
Exploitation et son test, restent hors commit Animation. Le suivi moteur
préexistant du dépôt Projet reste également exclu. Aucun push ni déploiement.

À la fin du lot 09, les pages de sélection et suggestions publiques sont bornées ;
la vue Coffrets globale et ses totaux historiques restent alors à traiter dans le
lot 10. Cette réserve est reprise ci-dessous après l'autorisation de poursuivre. Les recettes
humaines et hébergées restent non exécutées ; ces mesures ne constituent pas le
test de charge mixte ni une garantie de capacité sur l'hébergement cible.

### Lot 10 — Exploitation, réversibilité et consolidation

Reprise explicitement autorisée le **19 octobre 2026**. Le lot complète le
pilotage économique interne (US34), la réversibilité et la fermeture accompagnée
(US35), les lectures ERP/Support (US24), la conservation et les outils de reprise.
La [prise en main par lot](prise-en-main-par-lot.md) décrit les accès des dix lots ;
le [guide opératoire](../../exploitation/exploitation/exploiter-saas-animation.md)
décrit les traitements préparés, leurs paramètres et les étapes de mise en service
qui restent à exécuter séparément.

**Comportements implémentés.** Le suivi économique distingue faits constatés,
estimations et données indisponibles. Les corrections sont historisées, les
budgets déclenchent des alertes internes à 80/100 %, sans effet commercial.
Les mesures archivées ne peuvent pas être réactivées par une nouvelle
valorisation ; les marges restent indisponibles tant qu'aucun rapprochement
comparable des revenus n'est établi.

L'export est demandé par le responsable, capturé dans un instantané cohérent,
assemblé par segments et téléchargé après nouvelle vérification des droits.
Il contient CSV, médias transmissibles, manifeste et guide, jamais les secrets
QR/PIN, mots de passe, notes internes ni données d'une autre organisation.
La fermeture interdit les nouveaux usages, inventorie les engagements selon
leurs états métier réels et exige leur résolution. Seules les préparations
accompagnées disposent en V1 d'une reprise interne effective ; aucun bouton de
transfert fictif n'est présenté pour les autres engagements.

L'ERP et le Support disposent d'**Animations et lots**, de listes et CSV de page
avec contrôle courant du périmètre communal. Les vues globales Participants,
Validations et Coffrets du portail utilisent désormais des pages serveur et
des synthèses distinctes. L'historique Pro ne parcourt plus toutes les preuves
expirées pour constituer une page. Les compteurs SQL sont des projections de
lecture transactionnelles, jamais une autorité pour qualifier ou tirer un gagnant.

La conservation rattache les familles aux durées existantes, traite gels,
copies SQL/JSONL/Live et fichiers privés, et conserve une preuve minimale.
Une date de fin absente est signalée, sans repli sur une date de création.
La reprise exige un journal indépendant et ferme les capacités restaurées,
y compris sessions internes et QR de bons, avant réouverture. Le lot et ses
droits commerciaux ne sont pas révoqués par cette fermeture technique.

**Migrations locales préparées et vérifiées :** v277 coûts, v278 réversibilité,
v279 conservation/reprise, v280 projection d'historique Pro, v281 index ERP/Support,
v282 pages globales, v283 compteurs de lecture. Le rejeu depuis une base vide,
l'atomicité, la correspondance des modèles et la disponibilité des colonnes/index
requis passent : **3 tests**, 51,45 s, `tmp/e73-lot10-migrations-final.xml`.
Aucune base partagée n'a été migrée.

**Contrôles transverses.** Architecture, recensement des classes de domaine,
couverture des use cases, Ops, ERP, batchs et readiness : **640 réussites**, deux
avertissements de dépréciation Starlette/AnyIO, 30,53 s,
`tmp/e73-lot10-final-architecture02.xml`. Le premier appel avec un chemin de test
inexistant n'a exécuté aucun test ; il a été corrigé, sans retrait de contrôle.
Les contrats canoniques E41/E42 et le contrat embarqué Animation ont été
régénérés hors ligne (985/62/985 chemins). Contrats API et registre démo :
28 réussites ; les quatre erreurs initiales d'accès au répertoire temporaire
Windows sont résolues par un répertoire local explicite, avec **8 réussites**
du fichier de tests documentaires complet au second passage. Les comptes de
ces suites se recouvrent et ne doivent pas être additionnés.

**Portail.** **233 tests Node**, zéro échec ou skip ; les deux nouveaux tests
rejouent les contrats HTTP fermés du producteur. Types, lint ciblé et compilation
réussissent sur le candidat isolant les changements préexistants. Le bundle
principal vaut 480,48 ko / 124,76 ko gzip. Navigateur : **12 scénarios / 100
assertions** export/fermeture/catalogue et **4 scénarios / 60 assertions** listes
globales, à 320/1 280 px, texte 200 %, clavier, fuseau Paris depuis un navigateur
réglé Los Angeles, réponse perdue et refus d'accès. Commit local Animation :
**`da86e39`**. Les quatre modifications Clôturer d'App.tsx, le README, la vue
Exploitation et son test restent hors de ce commit.

**Périmètre de performance.** Les nouvelles pages hydratent un volume borné et
les projections évitent les scans complets de participants/passages. La recherche
textuelle conserve un agrégat SQL exact sur les correspondances : son coût n'est
pas constant. Les agrégats acquisition/satisfaction/gains ont leurs propres
volumétries ; un essai à 100 000 participants ne prouve pas leur croissance.
La revue a aussi confirmé au HEAD du lot 09 les chargements historiques complets
de l'index Animation, des vues Tirages/Flyers et des participants d'une fiche.
Ils ne sont pas présentés comme corrigés ni comme couverts par les mesures des
nouvelles pages globales. La spécification n'impose pas une refonte générale de
ces lecteurs historiques ; leur dette reste à traiter avant de leur annoncer
les mêmes garanties de volume.

Les preuves finales de conservation, réversibilité, charge avec workers et
compatibilité démonstration sont consolidées ci-dessous après leur exécution.

**Réversibilité et lectures ERP/Support : 75 réussites**, aucun skip ou échec,
140,94 s, deux dépréciations Starlette/AnyIO,
`tmp/e73-lot10-portal-final02.xml`. Les contre-preuves couvrent notamment les
états terminaux réels des producteurs (tirages, gains Coffrets, remboursements),
les bons expirés encore prolongeables, la portée actuelle de l'opérateur, les
gels concurrents de fichiers/captures et le nettoyage borné de 103 segments par
pages de 25. Les quatre CSV et le ZIP ont leurs contrats binaires explicites.

**Conservation : 41 scénarios distincts finalement réussis**, aucun skip ni
échec restant, après déduplication des XML `e73-conservation14`, `date16`, `17`,
`18` et `19` sous `tmp/`. Le premier passage comptait 30 réussites et dix erreurs
de préparation liées au répertoire temporaire Windows. La reprise locale a aussi
corrigé deux fixtures : date historique UTC écrite naïve dans une colonne sans
fuseau, et sélection de l'email de renvoi par son identifiant d'opération plutôt
que du premier email du bon. Le test conserve le refus du QR/lien ancien, le code
d'erreur réel et l'acceptation du bon réémis. Le code de reprise traite explicitement
les dates UTC sans offset, sans dépendre du fuseau de l'hôte ou de PostgreSQL.
La revue indépendante des contrôles de conservation, des permissions du bilan
et du transfert/restauration démo est consignée dans les rapports de travail ;
ses constats ont donné lieu aux corrections et contre-preuves, sans skip ajouté.

**Démonstration complète : 10 réussites**, aucun échec ni skip, **729,58 s**,
sept avertissements SQLAlchemy de réflexion `dialect_options`,
`tmp/e73-lot10-demo-complete01/results.xml`. Le runner migre jusqu'à v283,
génère les scénarios des lots précédents, transfère les données, simule une
interruption, reprend puis restaure la base d'origine. Le registre classe les
24 nouvelles tables ; les quatre projections déclenchées par triggers sont
restaurées après leurs sources. Les contrôles locaux de purge et de reprise ne
sont pas transférés avec un jeu, mais le dump complet vérifie leur empreinte ;
altérer le verrou de reprise dans la base d'essai fait refuser sa réutilisation.
Les **63 tests ciblés** du registre, des reprises et du runner passent également
(`tmp/e73-lot10-demo-units-final.xml`). Aucun service fournisseur ni base partagée
n'a été appelé. Après cette passe, seules les fins de ligne/espaces finaux du SQL
v277 généré et du module d'index de conservation ont été normalisés, avec contrôle
d'identité du contenu hors espaces ; le rejeu de migrations est vérifié à nouveau.

**Cœur coûts/lectures : 43 réussites**, deux dépréciations, 42,60 s. La dernière
contre-preuve purge réellement une mesure puis tente sa recollecte pendant et
après la transaction : aucune mesure, tête, valorisation ou projection n'est
recréée. La vérification du reçu d'effacement partage les verrous de la purge.
Le bilan réutilise seulement les permissions vérifiées dans sa transaction :
une nouvelle requête après révocation perd les actions puis l'accès de lecture.

**Charge locale et limites.** Le bilan Gestionnaire corrigé passe : un test,
22,68 s, p95 364 ms / p99 374 ms pour un budget p95 de 900 ms. À nombre
d'animations affichées fixe, les populations ne sont pas hydratées.
Le banc de services applicatifs/PostgreSQL, avec un worker de coûts et dix
acteurs, donne les résultats suivants (millisecondes, p95) :

| Participants / distribution | Bilan | Participants | Validations | Remise |
| --- | ---: | ---: | ---: | ---: |
| 10 000 équilibrés | 462 | 537 | 465 | 603 |
| 10 000 concentrés | 393 | 372 | 252 | 620 |
| 100 000 équilibrés | 407 | 578 | 542 | 639 |
| 100 000 concentrés | 416 | 397 | 387 | 513 |

Les budgets restent 900/700/700/1 000 ms. L'essai 10 000 équilibrés initial
partageait le CPU avec un build ; le rejeu est isolé. Le premier 100 000 équilibré
atteignait 707 ms pour les validations ; une vérification isolée unique donne
542 ms. Les résultats initiaux sont conservés. À vingt acteurs, plusieurs budgets
sont dépassés (jusqu'à 1 497 ms pour une remise) : cette capacité supplémentaire
**n'est pas acquise**. Huit actions par acteur, pause de 20 ms : ces essais courts
ne démontrent pas un débit soutenu de production.

Le scénario **E73-PERF-08 à cinq workers réels** passe : **un test, 119,14 s**,
aucun échec/skip (`tmp/e73-lot10-workers-performance-final02.xml`). Dix communes,
10 000 participants, dix acteurs, import/campagne/export/tirage/coûts démarrés
ensemble, sans charge extérieure. Les p95/p99 sont respectivement : bilan
463/514 ms, participants 575/583 ms, validations 482/534 ms, remise 779/877 ms.
Zéro erreur ; 80 actions pendant une phase de 16,993 s, soit 4,71 actions/s ;
pic RSS 147 Mio, 15 connexions de pool et six sessions en attente de verrou au
maximum observé (ce dernier indicateur n'est pas une durée d'attente).

L'export termine en 16,97 s, le tirage en 5,63 s dont 102 ms pour le scellement.
Après 18 tours de reprise, 89,39 s, les comptes finaux sont vérifiés : **100
commerces importés, 1 000 messages Live, 100 attributions, 700 faits de coûts**
sans doublon, et archive disponible de **10 000 participants** segmentés par 100.
Le premier essai échouait parce que la fixture omettait les modèles de dossiers
de souscription ; l'ajout des modèles réels corrige la fixture sans changement
du produit, ni allègement du volume ou des budgets. Son XML et ses mesures brutes
restent conservés.

Limites : le trafic passe par les services applicatifs et PostgreSQL locaux,
sans HTTP/proxy ni fournisseurs externes. La campagne prépare ses destinataires
pendant la charge ; les dépôts Live sont effectués au drainage. Le tirage porte
sur une autre commune de la même organisation. Le scénario à cinq workers ne
porte que sur 10 000 participants/dix acteurs ; les paliers supérieurs ci-dessus
ont seulement un worker de coûts. Les preuves ne sont pas un SLA hébergé.
Les artefacts détaillés sont conservés dans `.artifacts/e73-charge-workers-locale.json`
et `.artifacts/e73-charge-mixte-locale-matrice-finale-brute.json` du backend,
avec les replays et diagnostics ; ils ne sont pas ajoutés au dépôt documentaire.

**Contrôle final des candidats commités.** Après normalisation des espaces du
SQL v277, le rejeu complet, les modèles et le contrôle de readiness passent à
nouveau : **3 tests, 42,71 s**, `tmp/e73-lot10-migrations-final02.xml`. Cette
modification purement textuelle ne justifie pas de rejouer les douze minutes du
cycle de démonstration déjà réussi.

Le complément d'annulation des lectures passe ses **17 tests ciblés**, dont huit
nouveaux, et son lint. L'ensemble du portail compte désormais **241 tests Node
réussis**, zéro échec/skip, 31,14 s (`tmp/e73-lot10-node-final02.log`). Types,
lint du candidat et build passent sans charger de configuration opérateur ; le
bundle principal est de 480,48 ko / 124,75 ko gzip. Les parcours navigateur sont
rejoués après ce complément : **4 scénarios / 60 assertions** pour les lectures
globales et **12 scénarios / 100 assertions** pour export/fermeture/catalogue.
Les signaux interrompent effectivement les GET et leur lecture JSON/ZIP,
préservent les autres abonnés d'une requête dédupliquée et ne réessayent pas
une lecture annulée. Les écritures déjà parties restent suivies ; aucun arrêt
universel d'un SQL serveur déjà engagé n'est revendiqué.

**Bilan local final.** Les dix lots sont implémentés, avec les contrôles,
contre-preuves et limites consignés dans ce journal. Les parcours accessibles
par lot sont décrits dans la [prise en main](prise-en-main-par-lot.md), les
opérations dans le [guide SaaS](../../exploitation/exploitation/exploiter-saas-animation.md).
Le lot 10 est enregistré localement dans Backend **`7f74166`**, Animation
**`da86e39`** et **`3801cc5`**, puis dans son commit documentaire. Le complément
Animation isole la correction d'annulation détectée lors de la revue finale.
Pro et Marketplace ne nécessitent pas de nouveau changement de code dans ce
lot : les contrats QR/PIN/Live restent compatibles et sont contrôlés côté
producteur ; les adaptations antérieures sont dans leurs commits par lot.

L'epic reste **En cours dans la roadmap produit**, car l'acceptation humaine
Localeo puis Martignas-sur-Jalle, les branches de recette hébergées et la preuve
RPO **4 h** / RTO **8 h** ne sont pas exécutées. Les CA28/63 ne sont pas acquis
par des tests locaux. Les limites de charge à vingt acteurs et des lecteurs
historiques sont maintenues ci-dessus. Aucun push, pipeline distant, déploiement,
migration partagée ou envoi fournisseur réel n'a été effectué. Les travaux
préexistants exclus sont conservés dans leurs arbres de travail.

## Correctif du 22 octobre 2026 — module de stockage absent de la livraison

Le démarrage Render signalé échoue à l'import de
`app.infrastructure.storage.reversibilite` depuis l'API de réversibilité.
Le commit backend `7f74166` ne contient pas ce fichier, alors que sa copie locale
permettait aux tests de passer : la règle générale `storage/` du `.gitignore`
excluait également les nouveaux adaptateurs Python du stockage applicatif.

La règle conserve l'exclusion des données de stockage et ouvre uniquement les
sources `.py` de `app/infrastructure/storage/`. L'adaptateur existant
`reversibilite.py` devient ainsi livrable avec le correctif, sans modification de
sa logique. Les archives privées, caches, sauvegardes et fichiers `.env` restent
ignorés. Un test d'architecture exerce ces décisions avec Git dans un dépôt
temporaire ; il échoue sur l'adaptateur avant correction et passe ensuite.

Vérification locale : **618 tests réussis** pour l'architecture, le recensement
des classes de domaine et cas d'usage, et le contrat HTTP de réversibilité.
L'absence du module et l'erreur `ModuleNotFoundError` sont également reproduites
depuis une archive Git du commit, sans les fichiers locaux non versionnés.
Après ajout du seul adaptateur manquant dans cette archive, **5 tests réussissent**
(`tests/api/test_reversibilite_organisations_api.py` et
`tests/api/test_observability_errors.py`), incluant le chargement de `app.main`
et la génération OpenAPI. Les journaux privés sont dans
`.artifacts/storage-delivery-fnup7vta/` du backend. Tous ces tests utilisent
`scripts/validation/test_isolated.py` ; les contrôles documentaires
`check_guidance.py` et `sync_documentation.py --check-sources` réussissent aussi.
Deux avertissements de dépréciation FastAPI/Starlette restent
visibles ; ils ne constituent pas l'erreur de livraison.

Impacts : backend (contenu livré et exclusion Git) et ce suivi documentaire.
Aucune modification des contrats API, permissions, règles de conservation,
interfaces ou données de démonstration ; aucune migration supplémentaire.
La vérification isolée bloque les connexions et les envois externes. Aucun
commit, push ou redéploiement n'est réalisé par ce correctif local.

## Correctif du 22 octobre 2026 — invitation ouverte sous le compte de l’invitant

Lors de RM-02-02, l’invitation a été ouverte avec Mathilde, qui l’avait envoyée.
Ce scénario attend la création du compte destinataire ; l’acceptation avec un
compte déjà connecté relève de RM-02-03 et exige l’identité invitée. Le domaine
backend conserve cette vérification. L’écran ne montrait pas l’identité connectée
et ne permettait pas de changer de compte, ce qui rendait le refus peu exploitable.

Localeo Animation affiche maintenant le nom et l’email du compte connecté,
explique le choix et propose **Changer de compte**. Cette action réutilise la
déconnexion serveur existante, puis propose la connexion du destinataire ou la
création de son premier accès. L’invitation reste uniquement en mémoire dans
l’onglet ; son secret n’est pas réintroduit dans l’URL ou les stockages navigateur.
Un échec de déconnexion conserve l’écran de reprise et bloque la suite jusqu’à
confirmation serveur. Le message de refus indique aussi comment reprendre.
La réponse `MOT_DE_PASSE_REQUIS` fournie ensuite pendant la recette confirme
le cas d’un destinataire nouveau : l’interface explique spécifiquement qu’il
faut changer de compte puis créer le premier accès et définir le mot de passe.
Le code imbriqué dans `detail.code` est lu sans afficher le détail technique brut.

Preuve locale sur Animation `f0251a5` avec correctif : le banc navigateur
`tests/browser/account-app.mjs` échoue avant correction sur l’absence de l’email
connecté, puis réussit **124 assertions** à 1280/320 px, dont changement de compte,
création, reconnexion du destinataire, absence d’acceptation prématurée et reprise
d’une déconnexion échouée. Le complément reproduit aussi le 422
`MOT_DE_PASSE_REQUIS` avant de créer le compte : le test échoue sur le message
générique, puis confirme l’explication précise et la reprise sans nouvelle invitation.
API simulées, trafic externe bloqué ; ce banc ne prouve
pas la réparation d’une invitation hébergée. Le banc adjacent
`tests/browser/organisation-access.mjs` réussit **111 assertions / 24 scénarios**
à 1280/390/320 px. Les **18 tests Node ciblés** de
contrats organisation/session et d’expiration réussissent, ainsi que TypeScript,
ESLint et le build PWA isolé (`scripts/build-pwa-tests.mjs`). `pnpm` est absent
du PATH ; types et lint sont exécutés avec les binaires locaux via Node 24.14.0,
sans installation ni modification du verrou. Les captures du parcours sont dans
`tmp/generation-browser-dist/invitation-account-*.png` du dépôt Animation.
Les contrôles documentaires `check_guidance.py` (96 guides, 0 erreur) et
`sync_documentation.py --check-sources` (130 documents) réussissent également.

Impacts : interface Animation et recette RM-02-02/03 ; aucun changement du
contrat d’acceptation, de la règle métier ou du générateur, qui émet déjà les
invitations attendues. Aucune migration ni nouvelle configuration. Aucun accès
à l’environnement de test, envoi d’email, commit, push ou déploiement effectué.

Point de publication du **23 octobre 2026** : le correctif des invitations décrit
ci-dessus a été commité et poussé séparément dans `localeo-animation`, sur `main`,
sous **`4ee90c2`**. Le contenu exact du commit a été vérifié dans une copie isolée
de l’index : TypeScript, ESLint, build Vite isolé, **18 tests Node**, **124 assertions**
du parcours compte et **111 assertions / 24 scénarios** d’accès organisation réussis.
Les modifications de flyers sont restées locales et ne font pas partie de ce
commit. Le push n’atteste pas la version déployée ni la recette hébergée.

## Évolution du 22 octobre 2026 — E73-EVO-FLYER

Réalisation locale des [flyers contextualisés](flyers-contextualises.md), critères
ajoutés **E73-CA-FLYER-01 à 05**. Base lue : backend `5aed284`, Animation
`f0251a5`, projet `6d25510`, avec conservation des travaux locaux antérieurs
(invitation organisateur, configuration et automatisation de recette).

La charte de rendu passe à `LOCALEO_ANIMATION_MARKETPLACE_V5`. Le domaine prépare
la promesse Coffrets / lots externes / bons numériques, le nombre d'exemplaires
et de commerçants effectivement participants. Le compteur des lots libres vient
de la dotation, sans chargement de ses exemplaires ; une participation publiée
utilise sa liste figée sans requête inutile sur les invitations. Les faits et
l'identité de l'image participent à l'empreinte du rendu et sont revérifiés avant
rattachement. L'ancienne accroche automatique Coffrets est adaptée aux lots
libres ; une accroche personnalisée reste conservée.

Les commandes d'image portent la version de l'animation et une clé d'idempotence.
Le normalisateur est injecté depuis la composition infrastructure ; il vérifie
le contenu réel, les dimensions, la taille et retire les métadonnées. Le document
privé d'illustration est versionné indépendamment de la couverture publique et
de la configuration publiée. Le retour au défaut réutilise le visuel historique
de l'animation, sinon la photo embarquée. L'intention de stockage existante
couvre également une image préparée mais non rattachée après conflit.

Dans **Localeo Animation → animation → Flyer**, `FlyerWorkspace` propose les
deux compteurs, le contexte de dotation, le choix d'image avec aperçu,
l'enregistrement, le retour au défaut, la génération et le téléchargement.
Un fichier choisi doit être enregistré ou abandonné avant génération. Un PDF
obsolète reste explicitement identifié comme précédent. Le menu global Flyers
ouvre directement cet onglet et affiche « PDF disponible » sans prétendre
calculer la fraîcheur de chaque document ; le compteur et le filtre trompeurs
« à actualiser / à régénérer » y ont été retirés. Le détail vérifie sa fraîcheur.

| Critères | Preuves locales exécutées |
| --- | --- |
| FLYER-01/02 | Tests de contenu et de service, PostgreSQL dotations externe/numérique et participation effective ; rendu réel des trois modes |
| FLYER-03 | Tests image et PostgreSQL remplacement/retrait/version documentaire, navigateur aperçu/enregistrement/retour au défaut ; PDF final inspecté |
| FLYER-04 | Validation raster/volume/dimensions/animation/EXIF, refus lecteur/autre tenant, contrat HTTP réel et actions UI masquées |
| FLYER-05 | Rejeu et clé réutilisée, verrou/version, conflit après stockage avec intention d'orphelin, changement d'image/dotation/acceptation durant préparation, réconciliation navigateur et état périmé |

**Résultats sur l'arbre local final :**

- **61 tests backend ciblés réussis, aucun ignoré**, dont neuf cas PostgreSQL
  dans `tests/security/test_illustration_flyer_postgres.py`. Le complément couvre
  `test_flyer_prepare_postgres_t3.py`, les tests domaine de contenu et leur
  recensement dédié, `tests/application/services/test_flyer_animation.py`, les
  tests infrastructure du renderer et de l'illustration, et
  `tests/api/test_animation_locale_flyer_cache.py`.
- **624 contrôles réussis** : `tests/architecture`, recensements des classes de
  domaine/cas d'usage et tests de `PolitiqueParticipationPublicationAnimation`.
- **184 assertions navigateur réussies** pour les trois modes à 320/1280 px,
  avec lecteur, double clic, conflit de version, réponse perdue/récupération du
  reçu et actualisation pendant `EN_COURS`. Le parcours application complet
  depuis la liste Flyers passe aux deux largeurs, y compris l'absence de fausse
  synthèse de fraîcheur.
- **12 tests Node ciblés réussis** : dix tests mutation/pagination existants et
  deux tests `flyer-http-contracts.test.mjs` vérifiant le producteur OpenAPI et
  les requêtes réelles du client. TypeScript, lint et build PWA isolé réussis.
- PDF A4 et aperçu PNG des trois modes inspectés ; QR décodés avec l'URL exacte
  dans les six livrables. Les outils QA optionnels déjà présents dans
  `tmp/kit-qa/deps` ont été chargés pour exécuter les deux tests de décodage
  initialement ignorés, sans installation ni modification des dépendances.

Les tests backend utilisent `scripts/validation/test_isolated.py`, le runtime
Python local et uniquement PostgreSQL jetable sur `127.0.0.1:55473`, base
`localeo_audit_test`, avec schémas isolés. Les deux avertissements restants sont
des dépréciations FastAPI/Starlette. Les échantillons PDF/PNG et leur vérification
QR sont dans `.artifacts/flyers-e73/` du backend ; les captures UI dans
`tmp/flyer-personnalisation/` d'Animation. Ces fichiers de travail ne sont pas
déplacés dans le dépôt documentaire.

La revue indépendante a conduit à corriger le retour à l'illustration historique,
la conservation des fichiers préparés, l'injection du normalisateur, la lecture
inutile des invitations publiées et la présentation de fraîcheur dans la liste.
Les contrats sont générés hors ligne dans `epic-41-api/openapi.json` et les
routes/schémas concernés synchronisés dans le contrat embarqué Animation.
Les contrôles documentaires finaux réussissent : `check_guidance.py` (94 guides,
1 018 liens, aucune erreur), `sync_documentation.py --check-sources` (130 documents)
et `git diff --check` dans les trois dépôts concernés.

**Impacts et limites :** trois dépôts modifiés pour cette évolution : backend,
Animation et projet. Aucune migration, nouvelle variable, conversion de données
ni modification du formulaire Pro/Marketplace. Le générateur peut conserver
l'absence d'image dédiée ; les nouvelles fixtures locales couvrent les trois
dotations, sans génération distante. Les PDF historiques ne changent qu'après
régénération. Le corps JSON est lu par le framework avant validation de sa
longueur ; la borne HTTP du proxy reste applicable, distincte des contrôles
base64/image. La recette hébergée RM-FLYER-01 à 05 reste à exécuter. Aucun commit,
push ni déploiement effectué ; l'état global de l'epic reste inchangé.
