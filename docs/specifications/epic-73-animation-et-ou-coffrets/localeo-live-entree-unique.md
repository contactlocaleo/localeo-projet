# E73 — Localeo Live, entrée unique des animations

Évolution **E73-EVO-LIVE-UNIQUE**, demandée le **30 octobre 2026**.
L'epic 73 reste **En cours**. Les 63 critères initiaux et leurs résultats de
recette restent conservés ; les critères ci-dessous sont complémentaires.

## Décision et comportement attendu

En tant qu'habitant, découvrir les animations des communes choisies, s'inscrire
et retrouver ses participations dans un seul espace, Localeo Live, à
`https://animations.localeo.city`. En TEST : `https://test-animations.localeo.city`.
Le portail organisateur reste `gestion-animations.localeo.city`.

Cette décision remplace la surface publique marketplace Animation mise en place
par E73-EVO-DOMAINES et E73-EVO-UX-PUBLIC. Elle conserve le domaine décidé, les
données et les règles métier. Le même dépôt `localeo-marketplace` fournit Live
et Coffrets, sur leurs services respectifs ; aucun nouveau référentiel ni dépôt.
`LOCALEO_PUBLIC_SURFACE=ANIMATION` désigne désormais l'entrée Live. L'ancien
paramètre `surface=animations` ouvre aussi la transition vers Live.

**Arbitrage confirmé par l'utilisateur le 30 octobre : aucun nouveau compte
habitant.** Les communes sont mémorisées sur l'appareil ; leur association à un
compte ne s'applique que si un mécanisme existant la permet. L'installation
anonyme Live n'est pas un compte. Aucune synchronisation de compte n'est ajoutée.
Les contrôles existants des liens personnels, QR, PIN et WebAuthn restent en place.

Hors périmètre initial : refonte Coffrets, changement des règles d'animation,
catalogue ou base de participations distincts et recommandations personnalisées.
Le complément **E73-EVO-LIVE-ACCUEIL-RAPPELS** ci-dessous ajoute l'accueil
personnel et deux rappels facultatifs ; il remplace l'exclusion initiale des
nouvelles notifications pour ces deux seuls usages.

## Parcours et priorité mobile

Navigation basse initiale : **Découvrir**, **Mes participations**, **Mes communes**.
Le complément Accueil/Rappels remplace le premier libellé par **Accueil**, sans
changer son URL `/live/decouvrir` ni supprimer la découverte publique.
Depuis le correctif du **31 octobre 2026**, la navigation comporte quatre entrées,
dans cet ordre : **Accueil**, **Mes participations**, **Mes lots**, **Mes communes**.
**Mes lots** ouvre directement `/live/lots` avec son propre titre de page et
remplace le sous-onglet du carnet. La destination reste active dans le détail
d'un bon ; les URL personnelles et les accès enregistrés sont conservés.
Découvrir présente les animations publiques **En ce moment** et **Prochainement**.
Une fiche montre titre, commune, dates, description, conditions et action autorisée.
Sa présentation sert l'entrée dans le jeu : type d'animation, **Votre défi** et
action de participation précèdent les textes détaillés. Pour un passeport
explicitement identifié, un objectif de validations positif configuré est mis
en chiffres ; tombola et chasse conservent des invitations adaptées à leur type.
Un type inconnu reste générique. Aucun avancement personnel, classement ni gain
n'est déduit de cette fiche publique. Les compteurs de `dynamique` connus sont
accompagnés de pictogrammes, avec une mention de dotation totale pour les lots.
Les récompenses et adresses participantes restent consultables avec leurs liens
existants. Description, conditions et règlement sont accessibles dans des volets
ouvrables, avec raccourcis depuis l'en-tête. Les actions d'inscription, de reprise
et de récupération gardent leurs autorisations et leur contexte de provenance.
Les cartes et l'en-tête de fiche reprennent exclusivement l'image personnalisée
configurée dans **Flyer**, lorsqu'elle existe et que le serveur l'autorise.
Sans image, après retrait ou si elle ne charge pas, le contenu reste lisible
sans illustration de remplacement ni colonne vide. La couverture du jeu et
les illustrations de ses étapes ne servent pas de repli. Voir le
[contrat Flyer](flyers-contextualises.md#règles-de-conception-et-contrats).
L'inscription réutilise le formulaire existant sous `/live/animations/:id/inscription`.
Les participations et lots personnels conservent leurs accès dans le carnet.

Conception mobile d'abord : écran de référence 320–390 px, pas de débordement
horizontal, champs à 16 px, actions tactiles d'au moins 44 px, navigation à portée
du pouce et marge de sécurité PWA. Pas d'accueil marketing avant les tâches.
États de chargement, vide, erreur, stockage refusé et réseau indisponible explicites.
Le clavier, le focus, le texte agrandi à 200 % et la réduction des animations
restent utilisables. Les libellés de navigation peuvent revenir à la ligne.

Précision UX mobile du **31 octobre 2026** : Live privilégie les interactions
et la progression réelle. Sur la fiche publique, l'action principale unique
(inscription ouverte ou accès aux participations existantes) reste accessible
pendant le défilement sur téléphone, au-dessus de la navigation basse. Sa
position suit la hauteur réelle de cette navigation, y compris avec du texte
agrandi ; un espace est réservé pour accéder au bas de la page. Sur un écran
de faible hauteur, l'action reste dans le flux pour préserver la lecture.
Les raccourcis vers lots, adresses et conditions précèdent les informations
détaillées. La récupération est nommée **Retrouver mon inscription**, distincte
de l'inscription ; les accès personnels et le contexte de provenance sont conservés.

L'accueil conserve une priorité dominante et deux suivantes compactes, avec
anneaux, étapes restantes et actions de reprise. Un raccourci **Les défis locaux**
permet de rejoindre le programme sans parcourir ces priorités. Le résumé
**Mes communes** affiche son compteur puis **Choisir une commune** : les liens
individuels et la modification se déplient à la demande, sans repousser le
catalogue derrière dix communes. La sélection initiale, lorsqu'elle est vide,
conserve la recherche et la géolocalisation volontaire.

**Mes lots** présente les bons numériques enregistrés sur l'appareil avec
pictogrammes de récompense, titre et action large **Consulter mon bon**.
Le **dernier état connu** reste explicitement local, vérifié par le serveur
à l'ouverture du bon exact. Aucun score, gain, statut disponible ni nouveau
total n'est déduit de cette présentation. Le vide propose la découverte et
l'aide pour ajouter un bon reçu par e-mail. Les autres natures de gains
conservent leurs parcours existants dans la participation.

La recherche ajoute ou retire des communes sans changer les inscriptions. Une
commune partagée par URL constitue un contexte de consultation : son ouverture
ne modifie pas silencieusement les communes suivies. Le suivi exige une action.

**Mes communes** privilégie les repères graphiques : nombre de communes suivies
sur ce navigateur, pictogramme de localisation, nom, code postal disponible et
état de suivi. Chaque commune propose **Voir les animations**, avec un retrait
secondaire nommé explicitement pour les lecteurs d'écran. Recherche et
**Autour de moi** sont regroupés ; les détails d'utilisation de la position
restent accessibles à la demande. Le compteur ne représente ni un nombre
d'animations ni un score : la borne reste de dix communes. Aucune carte, photo
ou statistique territoriale n'est inventée. La même présentation sert la page
dédiée et la sélection initiale intégrée à Découvrir, avec états vide et erreurs.

## Audit d’usage du 1er novembre 2026 — habitant peu familier du numérique

L’audit expert parcourt la découverte, le choix d’une commune, l’inscription,
la reprise d’un accès personnel et les lots sur téléphone. Il conserve le Live
immersif existant : repères visuels et actions de participation avant les
explications secondaires. Il ne constitue pas un essai avec de vrais habitants.

| Situation | Obstacle constaté | Comportement corrigé |
| --- | --- | --- |
| Recherche de commune indisponible | « Réessayez » sans moyen de relancer le même texte | Bouton **Réessayer la recherche**, saisie conservée et aucune sélection automatique |
| Lien communal invalide | **Choisir une commune** efface le contexte sans ouvrir le choix lorsque des communes sont déjà suivies | Accès réel à **Mes communes**, sans modifier la sélection enregistrée |
| Programme vide après sélection | Le bandeau demande encore de choisir une commune | Chargement, vrai vide et indisponibilité distingués ; **Modifier mes communes** sur le vrai vide, réessai sur panne |
| Détail personnel en panne | Le retrait du carnet est l’action proposée dans l’erreur | **Réessayer** reprend le même accès ; conservation locale expliquée, retrait secondaire dans les options |
| Fiche publique ouverte directement | Le retour aux animations mène au carnet personnel | Retour par défaut à la découverte ; provenance et retour contextuel existants prioritaires |
| Navigation avant inscription | **Mes participations** apparaît active sur une fiche publique | Fiche et inscription restent rattachées à **Accueil** ; les accès personnels, ajouts au carnet et lots conservent leur rubrique |
| Retrouver une inscription | Titre « Ajouter une inscription » et nouvelle inscription en concurrence avec la récupération | Titre **Retrouver mon inscription**, e-mail et action principale uniques ; nouvelle inscription sous **Pas encore inscrit ?** |
| Suite de récupération par e-mail | Étape suivante peu explicite | **Vérifiez votre boîte e-mail**, courriers indésirables, ouverture du dernier lien puis ajout au carnet ; réponse conditionnelle conservant la confidentialité |
| Inscription refusée ou non confirmée | Champs requis peu explicites et erreur éloignée du focus ; action identique avant/après réponse incertaine | Quatre champs obligatoires annoncés, notifications **Facultatif**, erreur focalisée, **Réessayer la même inscription** sans nouvelle clé ni modification du corps conservé |

Principes retenus : une tâche et une action principale identifiables, mêmes
termes que la navigation, textes courts donnant une prochaine action réelle,
saisies préservées après erreur et retrait séparé de la reprise. La fermeture
rend le focus au déclencheur ; **Utiliser une autre adresse** revient au champ
e-mail. Mobile, clavier et texte agrandi restent utilisables. Le GPS et
l’installation de l’application restent facultatifs ; aucun compte habitant
ni nouvelle étape de connexion n’est ajouté.

L’interface possède ces corrections de présentation. Règles d’inscription,
participations, consentements, tokens et contrats restent dans leurs producteurs
existants ; aucune donnée ni migration n’est créée. Les preuves locales et les
limites de l’audit figurent dans le [suivi d’implémentation](suivi-implementation.md).

## Critères ajoutés et preuves

Les numéros 01 à 12 reprennent les CA1 à CA12 fournis par l'utilisateur.

| Critère | Résultat observable et preuve attendue |
| --- | --- |
| E73-EVO-LIVE-01 | Catalogue et détail consultables sans compte, y compris sans carnet local ; aucune permission personnelle déduite de la consultation. |
| E73-EVO-LIVE-02 | Recherche et sélection de plusieurs communes, persistance locale, modification et stockage refusé ; aucun compte nouveau selon l'arbitrage confirmé. |
| E73-EVO-LIVE-03 | Deux périodes, seuls résultats publics retournés par le producteur, pagination et état vide permettant de modifier les communes. |
| E73-EVO-LIVE-04 | Fiche vers inscription ou participation, même contexte d'animation et code de diffusion ; conservation des mécanismes d'accès existants, aucun nouvel écran de connexion fictif. |
| E73-EVO-LIVE-05 | Même participation et historique après reprise volontaire du carnet, sans création de compte, doublon métier ou effacement de l'origine. |
| E73-EVO-LIVE-06 | `/live/decouvrir?commune=<UUID>` partageable ; `/live/animations/:id` et anciens liens personnels fonctionnels. |
| E73-EVO-LIVE-07 | Domaine HTTPS dédié, même backend, accès directs et actualisation ; vérification DNS/TLS et hébergée distincte des tests locaux. |
| E73-EVO-LIVE-08 | Anciens liens personnels et QR conservés ; aucune redirection globale des capacités ni utilisation du secret d'installation d'une autre origine. |
| E73-EVO-LIVE-09 | Ancien catalogue et `surface=animations` quittent l'interface marketplace, contexte commune/animation conservé ; reprise du carnet proposée avant sortie d'origine. |
| E73-EVO-LIVE-10 | Navigation Animation de la marketplace vers Live ; parcours Coffrets et anciens `/live/*` conservés. |
| E73-EVO-LIVE-11 | Découverte, communes, inscription et carnet utilisables à 320/390 px et en PWA ; safe-area et accès au clavier. |
| E73-EVO-LIVE-12 | Recette de bascule : domaine, lecture anonyme, inscription, reprise des accès, historique, redirections et non-régression Coffrets. Aucune mise en service déclarée sur la seule base d'un build. |

## Complément UX du 30 octobre 2026 — E73-EVO-LIVE-UX

Retour utilisateur après la première version : supprimer le rappel de marque
au-dessus de Découvrir, clarifier son icône et conserver **Mes communes** comme
unique écran de gestion. Les anciens accès Réglages `?focus=city` ouvrent cet
écran ; les réglages de carnet et notifications restent disponibles. Leur
ouverture ne remplace ni ne synchronise implicitement une commune par défaut.

La découverte présente la dynamique et le défi de chaque animation, en priorité
mobile, sans faux classement, probabilité de gain ou activité simulée.

| Critère ajouté | Comportement attendu |
| --- | --- |
| E73-EVO-LIVE-UX-01 | Marque conservée dans l'en-tête, sans rappel dans le contenu Découvrir ; boussole et libellé Découvrir, repère cartographique pour Mes communes ; suppression du raccourci icône redondant de la surface Animation. |
| E73-EVO-LIVE-UX-02 | Recherche et modification des communes dans Mes communes ; aucun second sélecteur dans Réglages ; catégories de notification et Push conservent exactement les communes choisies, y compris une sélection vide. |
| E73-EVO-LIVE-UX-03 | Cartes avec l'image personnalisée du Flyer si disponible, sinon sans illustration : statut serveur, défi configuré s'il existe, nombres publics de participants, gagnants et unités en dotation. Zéro confirmé distinct d'une valeur inconnue ; ancien backend compatible sans compteurs. |
| E73-EVO-LIVE-UX-04 | À 320/390 px, pas de débordement, liens tactiles et données lisibles ; texte agrandi, clavier et réduction des mouvements préservés. |

Contrat additif catalogue/détail : `dynamique` avec `nombre_participants`,
`nombre_gagnants`, `nombre_lots_a_gagner`, entiers non négatifs ou valeurs
inconnues nulles. Participants = inscriptions présentes, tous statuts confondus,
selon le compteur métier existant. Gagnants = participants disposant d'une
attribution courante, hors suppléants et attributions remplacées ; pour les lots
libres, le tirage doit être confirmé, selon les projections de bilan.
Lots = nombre total d'unités de la dotation, pas nombre de catégories de lots,
ni stock restant. Cette portée est indiquée sur la carte. Aucune identité,
capacité personnelle ou donnée de contact n'est publiée.

Le backend fournit cette projection de lecture groupée pour la page publique
autorisée ; aucun appel par carte et aucun calcul métier côté interface. Le
frontend omet les valeurs absentes, négatives ou non entières sans les convertir
en zéro. Le défi reprend le nombre de validations configuré sans fabriquer une
progression personnelle. Les compteurs sont ceux de la lecture, sans promesse
de mise à jour en temps réel. L'ancien champ `nombre_lots` reste compatible.

Impacts : backend et contrat OpenAPI documentaire additifs, consommateur Live
et fixtures adaptés ; pas de migration, nouveau compte, permission, commande
métier, tâche, fournisseur ou configuration DNS. Les données de démonstration
existantes alimentent les mêmes lectures ; pas de génération réelle nécessaire.
La validation hébergée et les mesures PostgreSQL de volumétrie restent distinctes
des tests isolés. Les preuves sont consignées dans le suivi d'implémentation.

## Évolution du 30 octobre 2026 — E73-EVO-LIVE-ACCUEIL-RAPPELS

Demande acceptée : un accueil personnel mobile et deux rappels personnels
facultatifs, pour terminer un parcours et agir avant sa fermeture. Cette
évolution remplace le premier onglet Découvrir par **Accueil**, conserve ses URL
et le catalogue public et étend le périmètre antérieurement exclu des nouveaux
rappels personnalisés. Aucun compte habitant n'est créé. L'EPIC 73 reste
**En cours** ; les critères et preuves historiques ne sont pas réécrits.

### Parcours et décisions retenues

**US-LIVE-ACCUEIL.** En tant que participant, voir immédiatement les parcours
proches de leur objectif ou de leur échéance et reprendre le bon accès personnel.
Depuis le correctif UX du **31 octobre 2026**, l'accueil ouvre sur le défi personnel
prioritaire lorsqu'il existe, afin de rendre son action visible dès l'arrivée
sur mobile. La vie des communes suivies vient ensuite, ou ouvre l'accueil en
l'absence de priorité : accroche contextualisée, animation à rejoindre avec l'image
personnalisée du Flyer si disponible, nombre réel de participants à cette
animation et accès directs aux périodes. Les nombres d'animations sont ceux
de l'aperçu chargé, dédupliqués par période ; pagination et erreurs sont
signalées comme un aperçu partiel. Aucune somme d'habitants uniques, activité
instantanée ou illustration par défaut n'est inventée. Une indisponibilité
totale propose de réessayer ; le vrai vide propose de modifier les communes.

Une priorité personnelle principale et deux suivantes compactes sont présentées
avant le programme communal. Un raccourci **Mes défis à reprendre**
dans l'en-tête y mène directement, même sur mobile. L'accueil ne présente plus
de section **Mes autres participations**, de pagination ni de liaison des accès.
Le lien **Toutes mes participations** rejoint `/live/animations`.
Cette page réunit le carnet local et les participations liées à l'installation,
avec déduplication par identifiant exact de participation ; deux inscriptions
à la même animation restent distinctes. Les accès distants absents du carnet
proposent **Retrouver mon accès**, qui ouvre le formulaire e-mail existant sans
créer ni substituer un token. Une entrée importée sans accès utilisable propose
aussi une récupération explicite ; elle ne permet pas de présenter un QR.

**Mes participations** reprend les images Flyer disponibles, les pictogrammes,
les anneaux et les étapes validées/restantes. Les nombres du carnet portent sur
les entrées présentes sur l'appareil ; les accès distants sont comptés **sur
cette page**, sans fabriquer un total global. Les gains et qualifications
conservent leurs statuts serveur, indépendamment du pourcentage. Une progression
absente ou incohérente n'est pas représentée par un anneau à zéro. La pagination
distante remplace la page précédente, au plus 50 éléments par page ; les anciens
accès se relient uniquement sur action explicite, par lots de 50 et avec deux
requêtes concurrentes au plus. Un échec de synchronisation laisse le carnet
local utilisable, avec ses informations conservées et l'état d'erreur visible.
Sur l'accueil, **Actualiser** recharge participations et catalogue, avec annulation des
anciennes lectures et sans parcourir toutes les pages implicitement.
Les visiteurs sans carnet disposent d'abord de la découverte. La navigation
comporte quatre entrées : Accueil, Mes participations, Mes lots, Mes communes.

Complément graphique du **31 octobre 2026** : privilégier l'image du Flyer en
pleine largeur plutôt qu'un grand panneau de texte. Limiter l'ouverture à un
titre local, une animation et des repères chiffrés avec pictogrammes et libellés.
La progression personnelle prend la forme d'un anneau chiffré, accompagné du
nombre d'étapes validées et restantes ; elle ne vaut ni qualification ni gain.
Les descriptions et conditions des cartes restent accessibles dans **En bref**,
sans être tronquées ; la fiche complète et son inscription restent accessibles.
Sans image configurée, conserver la présentation structurée sans illustration
de remplacement. Les pictogrammes d'interface restent décoratifs pour les aides
techniques ; les valeurs, libellés et noms accessibles portent l'information.

Sur l’**Accueil**, le résumé des communes suivies prend la forme d’un bandeau
graphique **Mes communes** : compteur de communes, repères de localisation et
noms complets sur des accès individuels à leurs animations. Le bouton
**Modifier mes communes** rejoint la gestion existante. Consulter une commune
ouvre son contexte partagé sans changer les communes suivies ; le compteur
porte sur cette sélection locale, jamais sur une activité supposée. Les dix
choix restent accessibles sans défilement horizontal, y compris avec des noms
longs et du texte agrandi. Sans commune suivie, conserver la recherche et la
géolocalisation volontaire existantes. Aucun fond de carte, photo ou statistique
supplémentaire n’est nécessaire pour ce résumé.

La direction visuelle de Live est un **espace de jeu local** : navigation basse
en dock avec destination active contrastée, défi personnel sur surface sombre,
anneau et étapes restantes au premier plan, action de reprise ou de récupération
explicite. Le rendez-vous communal associe Flyer, type de jeu, participants et
dotation connus à une action **Découvrir et participer** si les inscriptions sont
ouvertes, sinon une consultation. Les cartes mettent l'objectif et l'action avant
les textes détaillés. Passeport, tombola et chasse utilisent les mêmes libellés
de type dans l'accueil, le catalogue et la fiche ; seul un passeport explicite
présente un objectif public de validations. Les participations disposent de
surfaces distinctes pour lire leur progression et accéder à leur QR.

Cet habillage est limité à la surface Animation et conserve les parcours
Coffrets. La sensation de jeu repose sur les objectifs configurés et les
progressions réelles, sans points, classement, compte à rebours ni activité en
temps réel inventés. Les mouvements accompagnent l'entrée ou l'action ; le
réglage de réduction des animations les supprime. Les textes restent complets
à 200 %, les cibles tactiles et les marges de sécurité PWA sont conservées.

Le **centre de notifications** reprend la typographie, les couleurs, les
pictogrammes et les actions arrondies de Live. Les catégories et dates précèdent
le titre, l’animation éventuelle et le message complet. Les mentions **Non lue /
Lue** restent lisibles sans dépendre d’une couleur ou d’une baisse d’opacité.
Le compteur concerne uniquement les messages affichés, y compris après
pagination ; il ne prétend pas donner le total distant. La fermeture reste
accessible pendant le défilement et le dialogue est nommé dès son ouverture,
y compris depuis `/live/messages`. Chargement, absence de nouvelles, erreur et
pagination conservent leurs états explicites. Consulter le centre ne marque
aucun message comme lu et ne demande pas de permission Push ; la lecture d’un
message, le marquage des messages affichés et leurs destinations gardent les
commandes existantes. Ce composant partagé reste utilisable sur Live Coffrets.

Un parcours est « presque terminé » s'il est commencé, encore accessible et
incomplet, avec une étape restante ou une progression confirmée d'au moins 80 %.
Le nombre requis provient de l'objectif métier effectif, jamais du nombre de
commerces disponibles. « Derniers jours » signifie une échéance effective de
participation dans les 72 heures à venir, encore strictement future, avec des
étapes manquantes et une participation encore autorisée. Les deux indications
peuvent coexister sur une seule entrée. Une progression inconnue ou une erreur
de lecture ne devient pas zéro, une urgence ou une qualification.

Les priorités de la page sont triées : deux indications réunies, fin proche,
presque terminé, autres parcours ; puis échéance la plus proche et identifiant
stable. La page annonce explicitement une suite lorsqu'elle est partielle ;
aucun compteur ou classement global n'est déduit d'une page. Deux inscriptions
distinctes à une même animation gardent leurs accès et progressions distincts.
Le même identifiant de participation n'est pas présenté plusieurs fois.

**US-LIVE-RAPPELS.** En tant que participant, choisir deux rappels automatiques
indépendants, distincts des campagnes organisateur et sans quota commercial :

- **Mes parcours presque terminés** : une étape réellement restante sur un
  parcours commencé ; le seuil d'affichage de 80 % ne déclenche pas ce Push.
- **Mes animations qui se terminent bientôt** : échéance effective dans
  les 72 heures, participation encore possible, objectif incomplet.

Une participation terminée, annulée, inaccessible ou dont l'accès est révoqué
ne reçoit pas de rappel. Un parcours achevé en attente de régularisation ou
de qualification n'est pas réinterprété comme des étapes restant à jouer.
Les neutralisations et adaptations du parcours suivent les projections métier
existantes. Une qualification ou un gain reste exclusivement confirmé par le
backend ; le pourcentage ne les accorde pas.

Un seul rappel logique de chaque type par participation et installation,
avec au plus un rappel personnel par jour civil et installation. Les deux
types d'une même participation sont fusionnés ; plusieurs participations
éligibles peuvent être regroupées dans ce rappel quotidien. Aucun troisième
rappel à 24 heures n'est ajouté. La purge de la boîte de réception ne réarme
pas les rappels. Les doublons de transport éventuels réutilisent le même tag.

La préparation et l'envoi sont limités à **09 h incluses–20 h exclues, heure
de Paris**, avec gestion des changements été/hiver. Les états, préférences,
liens de suivi et échéances sont revérifiés juste avant l'envoi. Une attente
hors créneau ne prolonge pas le droit de participer ni une échéance dépassée.
Le transport peut répéter une remise après un incident réseau ; l'unicité
garantie porte sur le rappel logique et sa réservation durable.

Les préférences `RAPPEL_PRESQUE_TERMINE` et `RAPPEL_FIN_PROCHE` sont
**false par défaut**, y compris pour les installations existantes. Elles se
gèrent séparément dans Réglages ; ni l'inscription ni l'ouverture de l'accueil
ne demande la permission navigateur. Un refus de Push ne bloque pas l'accueil,
les participations ou la messagerie. Les catégories et communes antérieures
sont préservées. La préférence des campagnes organisateur reste indépendante.

### Architecture et contrats

Le domaine `animation_locale` possède la politique de priorisation et de rappel.
Il consomme la progression du moteur, ses preuves et son calendrier effectif ;
il ne dépend ni de l'ORM, ni du navigateur, ni du fournisseur Web Push.
L'application charge les faits, contrôle les accès et orchestre les transactions.
Le repository borne les lectures et écrit les réservations ; les interfaces
présentent les décisions, sans recalculer les seuils métier en JavaScript.

Lecture additive : `GET /public/localeo-live/installations/{id}/tableau-de-bord`,
avec `X-Localeo-Live-Secret` et `Cache-Control: private, no-store`. La réponse
expose `generated_at`, `items`, `count` de la page et `next_cursor`. Chaque item
contient `participation_id`, `animation_id`, `nom`, `commune:{id,nom}`, `type`,
`statut_participation`, `date_fin`, `progression:{total,validees,restantes,pourcentage}`,
`commencee`, `terminee`, `disponible`, `indicateurs:{presque_terminee,fin_proche}`
et un `deeplink`. La page est bornée à 50 participations, sans parcours exhaustif
implicite des pages ou chargement global préalable en mémoire. Seuls les suivis
autorisés de l'installation authentifiée sont consultables, même hors catalogue
public. Aucun token, e-mail, identité ou solution privée n'est exposé.

Le lien commun est `/live/animations?participation=<UUID>` : il ouvre uniquement
l'entrée locale portant cet identifiant. Un carnet absent propose la reprise
de l'accès ; aucune autre participation à la même animation n'est substituée.
Un digest de plusieurs participations ouvre Mes participations.

Les anciens suivis ne prouvent pas quel token personnel a été validé. Une
migration ajoute la référence nullable au token effectivement présenté, sans
rattachement historique heuristique. Le tableau et les rappels exigent une
capacité encore valide ; la réponse distingue les accès à actualiser par
`acces_a_actualiser` (indicateur entier 0 ou 1, sans comptage exhaustif). Depuis
le carnet local, une action explicite **Actualiser
mes accès** relie les participations avec leurs propres tokens existants,
par lots de 50 et deux requêtes concurrentes au plus. Les échecs partiels sont
visibles. Ni nouveau token, ni inscription, ni autorisation de rappel ne sont
créés par cette opération ; un token révoqué reste refusé.

Les deux catégories sont ajoutées au contrat de préférences existant. La
configuration publique expose `rappels_participations_disponibles: true` ; un
ancien backend sans ce champ conserve ses réglages et son catalogue. Un tableau
indisponible conserve les accès du carnet et propose une actualisation, sans
simuler l'absence de participations.

La préparation utilise un traitement batch protégé, borné, simulable par défaut,
destiné à un passage toutes les 15 minutes. Un curseur durable ou explicitement
reprenable évite de retraiter indéfiniment les premières installations. Les
réservations installation/jour et participation/type sont atomiques, uniques et
indépendantes de la rétention de l'inbox. Le verrou d'installation coordonne
préférences et rappels concurrents. La notification réutilise l'outbox et les
claims de transport existants, sans nouvelle intégration fournisseur.

### Critères et preuves attendues

| Critère ajouté | Résultat observable et preuve prévue |
| --- | --- |
| E73-HOME-01 | Accueil de jeu local : priorité personnelle et action visibles d'abord sur mobile, trois priorités au maximum, puis vie des communes suivies ; visiteur sans priorité vers découverte et participation publique. Image Flyer seule, aperçu partiel explicite, accès aux périodes, type de jeu cohérent et compteurs à pictogrammes. Autres participations et pagination sur Mes participations ; navigation et anciens liens conservés. |
| E73-HOME-02 | Indicateurs calculés par le domaine, frontière 80 %, une étape, 72 h, commencement et objectif effectif ; inconnus et états terminaux exclus. |
| E73-HOME-03 | Tri explicite, absence de doublon par participation, plusieurs accès à la même animation indépendants, pagination et état partiel. |
| E73-HOME-04 | Secret d'installation, refus croisé, aucune donnée sensible et aucune réponse personnelle mise en cache ; ancien backend et erreurs explicites. |
| E73-HOME-05 | Reprise exacte depuis l'accueil ou Push, accès absent sans substitution, parcours terminés/qualification/gains conservés. |
| E73-HOME-06 | 320/390 px et bureau, clavier, cibles tactiles, texte agrandi, mouvements réduits ; aucune nouvelle permission automatique. |
| E73-ALERTE-01 | Deux préférences opt-in indépendantes, défaut false neuf/existant, retrait effectif sans altérer les autres catégories ou communes. |
| E73-ALERTE-02 | Une étape restante pour le Push, fin dans 72 h, fusion des deux types et regroupement de participations ; aucun rappel après terminaison. |
| E73-ALERTE-03 | Un type/participation/installation et un rappel/jour, deux workers concurrents, rollback, purge inbox, reprise après incident sans doublon logique. |
| E73-ALERTE-04 | Créneau Paris 09–20, été/hiver, expiration pendant attente, revalidation préférences/accès/progression juste avant transport. |
| E73-ALERTE-05 | Batch borné, simulation sans écriture/envoi, progression du curseur, fournisseur simulé ; recette réelle distincte. |

| Impact | Décision et preuve à produire |
| --- | --- |
| Backend / API / batch | Domaine pur, lecture privée, catégories additives, registre durable, refus et concurrence ; tests isolés et PostgreSQL jetable. |
| Marketplace / Live | Accueil et réglages, mêmes carnet/communes ; contrats et parcours Playwright sur API simulées. |
| ERP / Animation / Pro | Pas de nouvel écran ni de commande : les nouvelles fonctionnalités sont destinées aux habitants dans Live. |
| Données / migration | Migration additive du registre et des index, anciennes préférences sans opt-in implicite ; restauration et introspection du générateur à examiner. |
| Documentation / exploitation | Contrat canonique, guide Live, batch, cadence, limites de transport et ordre backend avant frontend à actualiser. |

Budgets locaux : page de 50 suivis maximum, aucun enrichissement HTTP personnel
par carte, deux lectures frontend concurrentes au plus, préparation de 100
installations maximum par lot et absence de transaction englobant l'envoi réseau.
Les tests vérifient les bornes, accès/index et reprises ; les mesures hébergées
de latence et de charge mixte restent une vérification d'activation distincte.
Les preuves locales exécutées et les limites de recette hébergée sont consignées
dans le [suivi d'implémentation](suivi-implementation.md), sous la référence
**E73-EVO-LIVE-ACCUEIL-RAPPELS**. Elles ne clôturent pas toute l'EPIC 73.

## Invariants, contrats et conservation

Le backend reste propriétaire de la visibilité publique, des dates et autorisations
d'inscription, des progressions, attributions, consommations et historiques.
L'interface groupe les projections existantes et n'accorde aucun droit supplémentaire.
Réutiliser `fetchPublicAnimations`, `fetchPublicAnimation`, `searchVilles`, le
formulaire d'inscription et les contrats de participation existants. Aucun nouveau
contrat OpenAPI n'est annoncé pour une association à un compte inexistante.

Le catalogue est borné : au plus dix communes suivies et deux lectures concurrentes,
pagination indépendante par commune et période, détection des curseurs répétés,
annulation des anciennes recherches et déduplication par animation. Une erreur
partielle ne devient pas un résultat complet vide. Ces bornes d'interface ne
constituent pas une mesure de capacité serveur ; avant activation, mesurer sur
1 puis 10 communes les requêtes, latences, volumes et erreurs en charge mixte.
Budget cible de navigation : interactions locales immédiates, état de chargement
visible sans attendre la dernière commune ; les résultats restent consultables
si une autre commune échoue. La tenue en charge hébergée reste à prouver.

Le carnet est en IndexedDB par origine. Un DNS ne peut pas migrer ce stockage.
Conserver `/live/reprise-carnet` sur l'ancien domaine : export privé puis import
volontaire sur le nouveau, validation et fusion transactionnelles existantes,
mêmes identifiants et capacités, sans nouvelle inscription. Aucun token ajouté à
une URL de transition. L'ancien carnet reste présent. Les anciens liens personnels
restent servis lorsque leur redirection ne peut préserver l'accès sans risque.

## Impacts et ordre de livraison de la bascule initiale

Ce tableau concerne **E73-EVO-LIVE-UNIQUE**. Le complément Accueil/Rappels
ci-dessus ajoute ensuite une migration backend, un contrat de lecture et un
traitement batch ; son ordre de livraison et ses impacts priment pour ces ajouts.

| Périmètre | Impact et vérification |
| --- | --- |
| Marketplace / Live | Routes, navigation, découverte multi-communes et sélection locale, inscription sous scope `/live/`, transition de l'ancien catalogue ; tests Node et navigateur mobile/bureau. |
| Backend / ERP / batchs | Aucun changement de règle, schéma ou commande métier prévu ; mêmes endpoints publics et privés. Les liens générés continuent à être acceptés par les routes de compatibilité. |
| Portail Animation / Pro | Aucun nouveau parcours métier ; liens publics et QR existants conservés. Les origines publiques dédiées déjà prévues restent applicables. |
| Données / migrations | Pas de migration SQL ni duplication de participation ; reprise locale du carnet explicite. Pas de synchronisation de compte ou de secret d'installation entre origines. |
| Démonstration | Réutiliser communes, animations et participations synthétiques existantes ; adapter les scénarios de navigation, sans régénérer des données réelles. |
| Exploitation | Deux services publics conservés, même API ; DNS/TLS du service Live, cache et PWA, maintien des anciens accès et reprise de carnet avant retrait de toute ancienne origine. |

Préparer le bundle et ses tests, déployer le même backend compatible et le frontend
Live sur TEST, configurer le domaine dédié et vérifier TLS. Contrôler ensuite les
douze parcours et la reprise du carnet avec un utilisateur de recette. Mettre à
jour les liens marketplace et générés après cette vérification. Ne pas retirer
l'ancien hébergement des accès personnels ni sa page de reprise du carnet.
Le repli conserve le même backend et les données ; rétablir le bundle précédent
et ses origines sans effacer de carnet. Un service worker précédent doit toujours
permettre l'ouverture des anciens accès. Commit, push et déploiement sont séparés.

## Suivi des preuves

Les résultats réels et limites sont consignés dans le
[suivi d'implémentation](suivi-implementation.md). Les 130 scénarios historiques
de [recette métier](recette-metier.md) conservent leurs statuts ; cette évolution
ajoute ses propres parcours de bascule et n'est pas validée par leurs anciens succès.
