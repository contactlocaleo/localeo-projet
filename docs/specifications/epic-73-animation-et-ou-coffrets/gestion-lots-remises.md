# Gestion centralisée des lots et remises — E73-EVO-GESTION-LOTS

## Statut, demande et périmètre

Demande du **14 novembre 2026**, spécification préparée le **15 novembre 2026**, rattachée au
[backlog E73](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md)
et à la [roadmap](../../roadmap/README.md). **Trois lots implémentés ; qualification
GL-16 partielle** au 15 novembre 2026 : dépassement du budget de synthèse à
forte volumétrie. Les résultats sont détaillés dans le
[bilan de vérification](verification-livraison.md).
La clôture historique de l’epic 73 et ses 63 critères restent conservés.

Demande : depuis **Suivre l’activité → Lots et remises**, retrouver et traiter
les lots de plusieurs animations sans chercher leur fiche, connaître ce qui
reste à distribuer, retirer ou utiliser, et rappeler les bénéficiaires par
e-mail et/ou WebPush. Les coffrets sont inclus dans le besoin.

Le socle couvre les trois natures de gains d’animation : **lots externes,
bons numériques et coffrets gagnés**, dans l’organisation et la commune actives.
Il inclut les animations clôturées, terminées et archivées. La consultation
globale ne donne aucun droit nouveau de remise, de consommation ou de réouverture.
Les droits et les commandes existants restent propriétaires de ces opérations.

### Arbitrages confirmés le 15 novembre 2026

| Référence | Décision utilisateur | Portée |
| --- | --- | --- |
| GL-DEC-01 | Demande acquise : entrée dans Suivre l’activité, gestion directe des lots, indicateurs et rappels e-mail/WebPush ; inclusion des coffrets | Socle de l’évolution |
| GL-ARB-01 | Confirmé : uniquement les coffrets gagnés dans les animations | Les achats hors animation sont exclus de cette évolution |
| GL-ARB-02 | Confirmé : rappels manuels individuels et groupés, sur sélection explicite | Aucune relance automatique programmée |
| GL-ARB-03 | Confirmé : rappels possibles après fin/archivage pour les lots encore utilisables ou à retirer ; au moins 48 heures entre deux rappels au même bénéficiaire pour la même animation | Exception ciblée au gel terminal et cadence commune aux canaux |

Les trois arbitrages sont levés par les réponses utilisateur du 15 novembre.
Les sections ci-dessous décrivent la cible retenue, à implémenter et vérifier.
La confirmation de ces choix ne constitue ni une implémentation ni une activation.

## Correctif du 15 novembre 2026 — Tirages séparés des gains

La demande explicite du 15 novembre recentre l’ancienne vue globale **Tirages
et gains** sur les seuls tirages. Elle s’intitule **Tirages** et conserve son
adresse `/tirages`. La vision Coffrets de cette page est décommissionnée. Dans
les vues globales, le suivi des gains, leur distribution, leur remise et leur
consommation relèvent de **Lots et remises**, quelle que soit la nature de la
dotation.
La préparation des coffrets dans une animation et les autres consommateurs des
contrats historiques restent disponibles.

Ce correctif est rattaché à **E73-EVO-GESTION-LOTS**, sans nouvelle epic ni
réouverture de la clôture historique. Il remplace explicitement l’ancienne
consigne de maintenir la vue globale Tirages et gains. Il ne change ni les
règles d’éligibilité et de tirage, ni les confirmations, l’idempotence ou les
droits des commandes existantes. **GL-16 reste partiel** pour la synthèse Lots
et remises ; cette correction ne constitue pas sa qualification.

### Lecture et parcours retenus

La lecture additive `GET /protected/animation-locale/lectures-globales/tirages`
renvoie une page de tirages dans l’organisation et la commune actives, toutes
natures de dotation confondues. Les paramètres `limit` (25 par défaut),
`cursor`, `recherche`, `groupe` et `animation_id` sont appliqués par le serveur.
La réponse contient `items`, `nextCursor`, `hasMore` et `observedAt`. Le curseur
est lié au contexte et aux filtres ; le tri suit la création et l’identifiant
de l’animation. La sélection précède la limite. Aucun comptage global ni offset
profond n’est ajouté. Le navigateur ne recharge pas toutes les animations ou
toutes les pages pour les classer.

| Filtre présenté | Groupe API | Fait observable et action |
| --- | --- | --- |
| Prêts à être effectués | `PRET` | Le serveur propose l’action `TIRER`. Un statut clôturé seul ne suffit pas à déclarer un tirage prêt. |
| À venir | `A_VENIR` | Tirage non confirmé qui n’est pas prêt : état réel à venir, en attente, en préparation ou bloqué conservé, avec son motif lorsqu’il est disponible. Aucun nouveau lancement n’est proposé pendant une préparation ou un blocage. |
| Effectués | `EFFECTUE` | Confirmation de tirage enregistrée et datée. Une demande en cours ou une opération simplement acceptée ne vaut pas tirage effectué. |

La liste montre l’animation, son état de tirage et les dates utiles. L’action
ouvre l’onglet **Tirage** de la fiche Animation existante ; elle n’exécute pas
le tirage depuis la liste globale. Les animations terminées et archivées
ouvrent un résumé de tirage en lecture seule, relu avec `animation_id` sur
la même projection bornée, sans charger les gains ni les commandes interactives. Les commandes continuent à relire leurs
conditions actuelles, même si la lecture globale est ancienne. Cette vue
n’affiche pas le suivi des gagnants, les envois, les remises ou la consommation
et ne lance aucune de ces opérations.

### Critères et impacts du correctif

- Les trois groupes sont accessibles, avec recherche et pagination serveur ;
  un changement d’organisation ou de commune ne conserve aucune donnée du
  contexte précédent.
- Les lots externes, les bons numériques et les coffrets sont couverts, sans
  réintroduire de filtre ou de panneau de suivi Coffrets dans Tirages.
- Un tirage en attente, en préparation ou bloqué reste visible dans À venir,
  avec son état réel ; seule une confirmation datée figure dans Effectués.
- Le groupe Prêts repose sur l’action serveur `TIRER` et l’ouverture de la fiche
  conserve les confirmations, les droits et l’idempotence existants.
- Le menu, les accès directs `/tirages`, le mobile, le clavier, le zoom et les
  états chargement/vide/erreur doivent être vérifiés. Lots et remises conserve le suivi
  et les actions de gains, y compris pour les coffrets.

Producteur concerné : backend, projection de lecture sur les faits du domaine.
Consommateur concerné : Localeo Animation ; contrat documentaire E41 et copie
embarquée à mettre à jour ensemble. Les contrats historiques sont conservés
pour leurs autres lecteurs. Aucun changement de règle de tirage, migration,
batch, donnée historique ou générateur de démonstration n’est nécessaire :
le contrat est une lecture additive des états déjà existants. Les fixtures
ciblées couvrent les états et dotations ci-dessus. Le
[bilan du correctif](verification-livraison.md#correctif--vue-tirages-recentrée-sur-les-tirages-15-novembre-2026)
distingue les preuves exécutées des contrôles encore à produire ; aucune
activation d’environnement n’est attestée par cette spécification.

## Correctif du 22 novembre 2026 — Prioriser la logistique des retraits

La page **Lots et remises** doit permettre de préparer les retraits sans ouvrir
chaque dossier, tout en gardant une vision de l'utilisation des bons et des
coffrets. La présentation évolue dans Localeo Animation ; les lectures, les
commandes et leurs contrôles serveur restent inchangés.

### Repérer le travail et son contexte

La synthèse distingue **Retraits et distribution** (Lots externes à retirer,
Coffrets à distribuer) et **Utilisation des bons et coffrets** (Bons à utiliser,
Coffrets à utiliser). Ces quatre compteurs sont des raccourcis de filtre, pas
des sélections de bénéficiaires ni des commandes. Leur état choisi est visible
et annoncé ; **Tous les lots** permet de revenir à l'ensemble des états.

La synthèse conserve une vue d'ensemble de tous les types et états, même quand
la liste affiche une tâche précise. Elle prend en compte l'animation, la
recherche, le lieu de remise et l'échéance, mais omet les filtres de tâche
`nature`, `etat` et `rappel_possible`. Sa portée est expliquée à l'écran :
« Vue d'ensemble : tous les types de lots et tous les états. Animation,
recherche, lieu et échéance restent pris en compte. » Les compteurs portent sur
l'ensemble du périmètre serveur, jamais seulement sur les lignes visibles.
Une synthèse indisponible reste indisponible ; elle n'est pas remplacée par zéro.

Choisir un compteur applique l'état correspondant et retire les filtres de
nature ou de rappel qui pourraient le contredire. **Tous les lots** retire ces
trois filtres de tâche. Dans les deux cas, les critères de contexte sont
conservés, la pagination reprend au début et la sélection de rappel est purgée
selon les règles existantes. Le filtre opérationnel choisi reste compréhensible
près de la liste, y compris lorsque les filtres avancés sont repliés. Les
raccourcis n’ouvrent pas automatiquement ce volet : sa position reste conservée.

### Lire une ligne pour agir

Le tableau compare cinq colonnes : sélection, bénéficiaire et lot (avec
l'animation), statut et consommation, retrait et échéance (avec le dernier
rappel), puis actions. Les informations de dossier et les limites de qualité
restent consultables. Les coordonnées de retrait et les dates utiles sont
proches ; une donnée manquante est indiquée sans reconstitution. Sur mobile,
chaque valeur conserve son libellé et les actions restent accessibles.

L'état principal dépend de la nature du gain : retrait pour un lot externe,
utilisation pour un bon, distribution et consommation pour un coffret. Lorsque
les quantités sont fiables, un coffret indique les prestations utilisées sur
le total et celles qui restent ; sinon, la consommation est indéterminée, sans
division ni zéro inventé. Distribution, remise et consommation restent des
faits distincts : un envoi n'atteste pas le retrait, une prestation consommée
ne signifie pas que tout le coffret l'est.

L'action principale autorisée ressort sur la ligne ; détail, dossier et actions
secondaires demeurent accessibles. Aucun bouton n'ajoute une consommation au nom
du commerçant. Les confirmations, versions, clés d'idempotence et reprises de
résultats incertains sont conservées. Une lecture locale maintient formulaire,
filtres et focus ; elle ne remonte pas une page entière en chargement.

### Impacts et preuves attendues

Ce correctif précise **GL-01, GL-03, GL-04 et GL-15** : vérifier les quatre
raccourcis et leur remise à zéro, les filtres de contexte conservés, les
compteurs indépendants de la page, les données inconnues, les trois natures de
gains et les actions conditionnelles. Recette bureau/mobile, clavier et texte
agrandi, relecture locale, pagination et retour au dossier sont nécessaires.
Les preuves exécutées sont consignées dans le [bilan](verification-livraison.md).
**GL-16 reste partiel** ; cette retouche ne qualifie pas la capacité de la synthèse.

Le guide Animation et ses captures sont affectés. Le guide Commerçant est sans
impact : ses écrans et procédures de validation ne changent pas. Aucun changement
de contrat API, backend, règle métier, migration, batch, exploitation ou générateur
de démonstration n'est nécessaire ; seules les données fictives de recette sont
adaptées aux états présentés. Aucun déploiement ni réparation de données n'est
attesté par ce correctif.

## Existant vérifié et écart

Sources locales examinées : backend `0c0c4028`, Animation `8afc492`,
Marketplace/Live `6980e41`, Pro `bdc9a54`, projet `d96bda1`.
Ces versions décrivent le code disponible, pas son déploiement.

| Source | Comportement actuel | Évolution nécessaire |
| --- | --- | --- |
| [Navigation Animation](../../../../localeo-animation/src/app/App.tsx), `NAV_GROUPS`, `MENU_PATHS` | Suivre l’activité contient Participants, Validations, Tirages et gains, Flyers, Bilans ; l’ancien menu propose aussi Coffrets à gagner | Lots et remises est l’entrée globale. À la demande du 15 novembre, retirer le menu Coffrets à gagner et rediriger `/coffrets` vers `/lots-remises` ; conserver la sélection des coffrets dans la préparation des animations, les tirages et les autres liens |
| Même source, `GainsAnimTab`, et [client API](../../../../localeo-animation/src/app/api.ts) | Gains, consommation et dossier de fin consultés par animation ; lecture globale `/gains/coffrets/consommation` disponible, client parcourant plusieurs pages | Lecture globale multi-natures, bornée, incluant les coffrets attribués sans instance ; aucun chargement de toutes les animations ou pages |
| [Productivité AP-18 à AP-20](ux-productivite-organisateur.md#l6--gains-et-fin-danimation) | Retour contextualisé, référence de dossier fournie par le serveur, accès ciblé et commandes versionnées | Réutiliser ces parcours dans le détail global, sans navigation obligatoire vers l’animation |
| [Dotation et remise](dotation-lots.md) | Attribution, remise externe, bons QR/PIN, distribution et consommation Coffrets ; un e-mail envoyé n’est pas une remise | Projeter séparément attribution, distribution, consommation et résolution du dossier |
| [Fin et archives](fin-animation-archives.md#correctif-du-14-novembre-2026--retrait-dun-lot-externe-après-clôture-du-dossier) | Retrait exceptionnel d’un lot externe clôturé autorisé après fin/archivage, avec motif et preuve ; autres commandes gelées | Exposer la même action dans la vue globale ; ajouter l’exception ciblée de rappel confirmée par GL-ARB-03 |
| [Notifications de gains par SMS](dotation-lots.md#évolution-du-11-novembre-2026--notifications-de-gains-par-sms) et [communication](modules-souscriptions-import-communication.md) | Renvoi de gain avec e-mail/SMS distinct des campagnes Live/WebPush, de leurs permissions et de leurs quotas | Un rappel e-mail/WebPush ne peut pas appeler aveuglément un renvoi qui ajoute un SMS ou une campagne à audience générale |

Producteurs confirmés dans le backend :

- [ServiceTiragesAnimation](../../../../localeo-backend/app/application/animation_locale/services/tirages_animation.py),
  `envoyer` et `relancer` : distribution ciblée déjà disponible, activation de
  l’instance et préparation e-mail/SMS ; relance actuelle sans filtrage des
  prestations restantes. Les deux commandes refusent fin/archivage. La route
  `envoyer` reçoit actuellement une clé sans la transmettre à `envoyer` ; un
  rejeu peut créer une nouvelle opération. Le reçu durable de distribution
  annoncé ci-dessous est donc une adaptation à réaliser, pas une preuve acquise.
- [ServiceTiragesLibres](../../../../localeo-backend/app/application/animation_locale/services/tirages_libres.py),
  `agir(SUIVI)` et `AttributionLotLibre.suivre` : remise externe ordinaire.
  [ServiceFinAnimation](../../../../localeo-backend/app/application/animation_locale/services/fin_animation.py)
  porte attestation et retrait exceptionnel ; leurs droits ne sont pas identiques.
- [API de consommation globale](../../../../localeo-backend/app/api/animation_locale_api.py)
  et `TiragesAnimationRepository.lister_consommation_gains_page` : seulement les
  gains avec instance, pagination historique par page/offset.
- [Projection de suivi produits ERP](../../../../localeo-backend/app/infrastructure/persistence/repositories/suivi_produits_lecture.py)
  et [bilans](../../../../localeo-backend/app/infrastructure/persistence/repositories/lectures_bilans_animation_repository.py) :
  faits réutilisables, autorisations ERP non transposables au portail organisateur.
- [RelancerCoffretsInstancesAvantExpiration](../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py) :
  batch d’expiration qui écrit à l’acheteur, pas nécessairement au bénéficiaire.
  Il reste distinct ; ne pas le brancher sur la nouvelle sélection de gagnants.

## Parcours organisateur

**Entrée.** La page `/lots-remises` affiche « Lots et remises », l’organisation,
la commune active et la portée « Gains des animations, archives incluses ».
Elle est accessible depuis le menu de bureau et **Plus → Suivre l’activité**
sur mobile. Aucun choix préalable d’animation n’est obligatoire.

**Pilotage.** Un résumé daté précède les filtres et la liste. Les quatre repères
principaux sont **Lots externes à retirer**, **Bons à utiliser**, **Coffrets à
distribuer**, **Coffrets à utiliser**. Chaque valeur ouvre son filtre. Les coffrets
à utiliser distinguent « jamais utilisés » et « utilisation commencée ».
Un récapitulatif secondaire permet de consulter remis/consommés, clôturés,
expirés, remplacés et unités encore sans gagnant. Les nombres ne proviennent
jamais de la seule page affichée ; une mesure indisponible n’est pas zéro.

**Liste.** Une ligne représente un gain courant, identifié par le bénéficiaire,
le lot, sa nature, l’animation et son état, le lieu de retrait si connu, les
dates utiles, la distribution/consommation, le dossier et le dernier rappel.
Filtres serveur : nature, état opérationnel, animation facultative, commerce
de remise lorsqu’applicable, échéance avant une date, présence d’un rappel
possible. Recherche par début de nom du bénéficiaire ou référence ; saisie
privée conservée en mémoire, pas dans une URL ou un stockage persistant.
Le filtre Animation réutilise un sélecteur paginé, archives comprises.
Depuis la simplification du 15 novembre, les filtres sont alignés à gauche :
Animation et Recherche restent visibles, les autres critères sont
repliables dans « Filtres avancés » avec un compteur de critères actifs.
Fermer ce volet ne modifie pas les filtres. Depuis le correctif du 22 novembre,
la tâche sélectionnée reste aussi visible près de la liste ; les raccourcis
appliquent les règles de contexte décrites plus haut.

**Intervenir.** L’action principale autorisée apparaît sur la ligne :
« Enregistrer la remise », « Distribuer le coffret », « Envoyer un rappel »
ou « Voir le détail ». Le détail conserve le contexte de liste et présente
l’historique, les données autorisées et les actions secondaires. Remise,
attestation et retrait exceptionnel s’effectuent dans ce détail ou sa fenêtre
de confirmation, sans imposer l’ouverture de la fiche Animation. Cette fiche
reste un lien secondaire. Aucun bouton ne peut consommer une prestation Coffret
ni un bon QR/PIN au nom du commerçant.

**Après action.** Résultat confirmé visible près de la cible, relecture du gain
et invalidation du résumé, maintien des filtres et de la position lorsque
possible. Si la ligne sort du filtre, annoncer pourquoi et rendre le focus à
la ligne suivante ou au titre de liste. Un conflit impose relecture et nouvelle
confirmation ; une réponse perdue impose vérification du reçu.

Chaque bloc visible possède son **Actualiser** à droite du titre. L’actualisation
ne perd pas une saisie, une sélection ou une commande incertaine ; elle est
différée ou explicitement protégée pendant la confirmation. Liste et résumé
ont leurs erreurs locales. Les actions non autorisées sont absentes ou
accompagnées du motif serveur utile, sans invitation à un formulaire impossible.

## Unités et états des indicateurs

Une attribution remplacée reste historique et ne compte plus dans les gains
courants. Un bon associé à un gain est le même gain, pas une deuxième ligne.
Une instance Coffret vaut **un coffret** ; ses prestations constituent une
autre unité. Aucun total ne mélange gains, prestations et stock sans gagnant.

| Indicateur / état | Définition observable |
| --- | --- |
| Lots externes à retirer | Attribution courante confirmée, remise non effective, dossier non clôturé, sans refus actif. Un refus ou une clôture apparaît dans À examiner, pas dans la file normale de retrait |
| Bons à utiliser | Bon attribué courant, utilisable selon son domaine, ni consommé ni expiré/révoqué ; la remise est sa consommation effective |
| Coffrets à distribuer | Gain Coffret courant confirmé sans mise à disposition confirmée ; séparer distribution en attente, en cours, échec et dossier clôturé. Une instance distribuée devenue expirée/utilisée ne revient pas dans cette file. Un gain déclaré envoyé dont l’instance manque est À examiner ; absence d’instance ne signifie pas consommation nulle |
| Coffrets à utiliser | Instance acquise encore utilisable, avec au moins une prestation restant utilisable ; distinguer aucune consommation et consommation partielle. Une fermeture du dossier Animation ne révoque pas l’instance |
| Coffret remis / réception attestée | Preuve de remise du dossier de fin, indépendante de l’état de consommation ; e-mail ou création d’instance ne valent pas cette preuve |
| Remis / entièrement consommés | Lot externe avec remise effective ; bon avec consommation ; coffret dont toutes les prestations de l’instance sont effectivement consommées. Une prestation annulée ou expirée n’est pas une prestation consommée |
| Expirés / révoqués / clôturés / à examiner | États explicites et motifs ; un dossier clôturé n’est jamais transformé en Remis par cette projection. Consommation partielle sans droit restant affichée distinctement |
| Sans gagnant | Quantité publiée non attribuée, calculée selon le domaine, agrégée par animation/nature ; unité physique, aucun faux bénéficiaire ni possibilité de rappel |
| Indéterminé | Instance/projection non disponible, prestations inconnues ou aucun total fiable ; pas de classement à partir d’une division par zéro |

Les quatre compteurs principaux sont des populations de travail identifiées,
pas des pourcentages d’une somme unique. Les états secondaires de distribution,
dossier et consommation peuvent se recouvrir ; l’écran ne les additionne pas.
Depuis le correctif du 22 novembre, le résumé reprend les filtres de contexte
de la liste, hors pagination et filtres de tâche (`nature`, `etat`,
`rappel_possible`), afin de garder visibles les quatre populations de travail.
Le serveur rend la portée, la date d’observation et la couverture. Une donnée
projetée ancienne ne permet jamais une action que les faits actuels refusent.

## Rappels — règles retenues

### Cible, contenu et canaux

Un rappel porte uniquement sur un droit acquis d’un bénéficiaire : retrait du
lot externe encore attendu, bon encore utilisable, coffret distribué dont une
prestation reste utilisable. Un coffret non distribué appelle d’abord sa commande
de distribution. Un lot sans gagnant, remplacé, externe refusé/clôturé, déjà
remis, bon consommé/expiré/révoqué est exclu. Le retrait exceptionnel reste
possible au guichet sans constituer une autorisation de rappeler un dossier clos.
Un coffret avec dossier Animation clos mais instance encore utilisable peut
rester éligible à un rappel de consommation : ce sont deux décisions distinctes.

Action individuelle ou **Rappeler la sélection (n)** : sélection explicite de
1 à 100 gains au plus, limitée à la page visible. Changer de filtre, page,
commune ou identité la purge avec annonce. Aucune sélection vide ne signifie
« tous ». L’aperçu distingue gains choisis, bénéficiaires, messages par canal
et exclusions. Plusieurs gains d’une même personne dans une même animation
sont regroupés dans un seul rappel ; deux personnes partageant une adresse
ne sont jamais fusionnées sur ce seul critère.

Chaque ligne présente une case. Si le rappel n’est pas autorisé par le serveur,
elle est désactivée et le motif figure avec le statut, visible aussi sur mobile.
Après actualisation, un lot devenu inéligible est retiré de la sélection avec annonce.

Choix explicite **E-mail**, **Notification sur le téléphone (WebPush)**, ou
les deux, avec aperçu. Aucun SMS supplémentaire et aucun canal de remplacement
silencieux. Si seul WebPush est choisi et qu’aucun appareil n’est éligible,
expliquer l’absence de destinataire ; proposer de choisir l’e-mail, sans l’envoyer.
Le détail d’aptitude des appareils n’est pas exposé à l’organisateur.

Le message est un modèle de service contextualisé, sans texte promotionnel
libre. Exemple externe : « Votre lot [nom] vous attend chez [lieu] !
[Organisation] de [commune] vous invite à consulter les modalités pour venir
le retirer. » Exemple Coffret : « Profitez encore de votre coffret [nom] offert
par [organisation] : découvrez les prestations qu’il vous reste à utiliser. »
Une échéance n’est citée que si elle est réellement portée par le droit.
Les variables sont échappées ; le texte court Push reste lisible. Aucun PIN,
QR de consommation, adresse e-mail ou lien porteur de secret dans le Push.
Le clic retrouve le lot après la preuve personnelle requise, y compris si
l’animation est archivée et n’apparaît plus dans la découverte.

L’e-mail transactionnel réutilise la politique d’identité/coordonnées des gains,
sans enrichissement de contact. Le WebPush exige la liaison personnelle valide,
le réglage Animations et l’abonnement actif de l’appareil au moment du dépôt et
du transport. Il s’appuie sur une notification personnelle Live ; choisir
WebPush n’active jamais un abonnement. Le retrait de permission et la rupture
de liaison sont revérifiés avant émission. Les campagnes organisateur, leurs
audiences et leur quota ne sont pas utilisées pour contourner ces conditions.

Le nouveau sous-type `RAPPEL_GAIN` relève du réglage **ANIMATION** pour sa
diffusion Live/WebPush ; il ne reprend pas implicitement les autorisations des
notifications initiales `GAIN`/`COFFRET`. Le destinataire est le bénéficiaire
du gain, jamais l’acheteur d’une commande par défaut. Les notifications initiales,
leurs SMS et les batchs d’expiration existants restent distincts : la cadence
retenue porte sur les nouveaux rappels, pas sur tous les messages historiques.
La coexistence doit être visible dans le diagnostic ; cette évolution ne
change pas la politique des relances d’achat.

### Fréquence, confirmation, terminal et résultats

Décision GL-ARB-03 : **48 heures minimum**, par bénéficiaire et animation, tous
canaux confondus. La réservation commence au commit de l’intention de rappel,
pas à son ouverture ; une intention déjà en attente bloque un doublon même
avec une autre clé. Un échec de transport se reprend sur cette intention,
sans créer un nouvel envoi. Une préparation sans aucun destinataire éligible
ne réserve pas ce délai. Le premier e-mail d’attribution ne devient pas un
rappel et le rappel ne redémarre pas le délai métier de remplacement du gagnant.

La confirmation montre les cibles, canaux, exclusions et l’échéance du prochain
rappel autorisé. L’aperçu est borné, signé/référencé, valable cinq minutes,
lié à la sélection et au contexte ; il n’envoie rien et ne réserve rien.
La commande revérifie versions, droits, coordonnées, canaux et fréquence.
Si l’aperçu a changé, `409` et nouvel aperçu, sans envoi partiel caché.
L’intention acceptée fige la sélection ; le worker ne l’élargit jamais.

GL-ARB-03 ajoute à la cible de FA-04 une exception limitée au rappel
transactionnel des droits encore valides après `TERMINEE`/`ARCHIVEE`.
Elle ne rouvre ni les campagnes, ni la distribution d’un nouveau coffret,
ni les modifications de lot ou de gagnant. Cette exception est spécifiée,
non implémentée ; le code courant conserve son gel jusqu’à sa livraison.

Résultats distincts : demande enregistrée, préparation en cours, exclu avec
motif, déposé dans la file e-mail, publié dans Live, Push en attente,
accepté par le fournisseur, échec reprenable, résultat fournisseur incertain.
« Envoyé » n’est ni réception ni lecture, et aucun de ces états ne prouve une
remise ou une consommation. Une consommation/remise intervenue avant le
dernier contrôle de transport annule l’envoi encore révocable ; après acceptation
fournisseur, on ne promet pas de retirer un message déjà parti.

## Propriétaires et invariants

| Propriétaire | Responsabilité |
| --- | --- |
| Domaine `animation_locale`, attribution libre / bon / gain Coffret et politique de fin existants | Attribution courante, remise, révocation, distribution, gel terminal, preuves et remplacement. La nouvelle page appelle les mêmes commandes que la fiche |
| Domaine Coffrets et ses prestations | Validité, consommation partielle/totale, expiration et droits acquis ; aucune mutation par la projection Animation |
| Nouveau service de domaine pur de rappel de gain, dans `animation_locale` | Éligibilité du droit, regroupement par bénéficiaire/animation, canaux demandés, cadence et exception terminale arbitrée ; reçoit des faits par ports, sans ORM, réseau ou configuration runtime |
| Domaine Live / notification existant | Preuve personnelle, réglages, liaison et admissibilité de la diffusion sur chaque appareil |
| Application | Autoriser organisation/commune/cible, charger les faits, orchestrer les propriétaires, UoW, versions, reçus et intentions ; construire la projection de lecture, pas une règle de remise concurrente |
| Adaptateurs | SQL borné et indexé, outbox, fournisseurs et ordonnanceur existants ; traduire états transport sans inventer une décision métier |
| Interface | Présenter capacités/refus et aperçu, confirmations, reprise, accessibilité et contexte ; aucun calcul local d’autorisation ou de total exhaustif |

Lecture permise selon l’habilitation effective ; coordonnées selon les droits
existants et les règles de conservation. Une capacité de gestion ne se déduit
ni de l’entrée de menu, ni de la possession d’une référence. Chaque cible
d’une sélection est contrôlée dans le tenant actif ; référence extérieure
non révélée. Un lecteur ne lance ni remise, ni distribution, ni rappel.
L’expiration commerciale n’efface pas les droits acquis : réutiliser les
décisions existantes de continuité, sans créer un nouveau module payant.

| Action | Habilitation à vérifier côté serveur |
| --- | --- |
| Lire liste, résumé, détail et suivi | `animation:lire` sur organisation et commune active ; coordonnées limitées au contrat de lecture autorisé |
| Remise externe ordinaire / distribution Coffret | `animation:envoyer_gain` et règles de la commande existante |
| Attester la remise / forcer le retrait d’un externe clos | `animation:modifier` et politique de fin existante |
| Nouveau rappel externe ou Coffret | `animation:envoyer_gain`, droit acquis et politique de rappel ; aucun pouvoir supplémentaire de modification du lot |
| Nouveau rappel de bon numérique | `animation:tirer`, comme son renvoi existant, plus politique de rappel ; aucune permission de consommation |

Le même aperçu peut donc annoncer des exclusions par nature pour un acteur
partiellement habilité. Les capacités sont produites par le serveur et relues
à la confirmation ; aucun rôle nominal ne remplace ces contrôles effectifs.

Commandes de remise existantes : mêmes versions, confirmation, motif requis,
clé et transaction. La distribution Coffret nécessite le complément de reçu
décrit au contrat ; ses garanties ne sont pas assimilées à celles de remise.
`FORCER_RETRAIT` reste réservé au lot externe courant avec
dossier clos dans les états autorisés ; il ne s’applique jamais au Coffret
ou au bon. Une preuve de clôture antérieure reste conservée.

Rappel accepté : réservation de cadence, intention, références de cibles et
reçu sont atomiques. Unicités pour la commande et chaque destinataire/canal ;
rejeu même clé/même contenu rend le même reçu, même clé/autre contenu refuse.
Deux clés concurrentes ne réservent pas deux rappels dans la même fenêtre.
Ordre de verrous commun : coordination existante, animations triées par ID,
puis cibles et réservations dans un ordre stable. Aucun verrou conservé pendant
un appel fournisseur. Révocation d’habilitation avant préparation : suspendre
les cibles non déposées et tracer, sans continuer sous un privilège ancien.
Reprise du worker : mêmes intentions et mêmes identifiants de messages.
Le transport externe ne garantit pas exactement une livraison en cas de réponse perdue.

La diffusion WebPush vers plusieurs appareils est elle aussi bornée : capture
exacte des identifiants éligibles par un `INSERT SELECT` dans la transaction
de confirmation, sans hydratation Python et sous délai SQL de 3 secondes ;
préparation de cette capture persistée en pages par clé de 100 maximum, puis
traitement de 25 intentions appareil au plus par lot, avec curseur et reprise.
Ne pas réutiliser un chargement exhaustif des installations d’un bénéficiaire.
Cette précision technique du 15 novembre évite qu’un appareil ancien réactivé
pendant la préparation entre après coup dans l’audience confirmée. Le coût SQL
de la capture reste proportionnel au nombre d’appareils ; le dépassement du
délai annule toute la confirmation et produit une indisponibilité temporaire,
sans audience tronquée ni réservation partielle. Mesurer séparément la capture
et le traitement paginé avec 10 puis 1 000 installations.
Unicité `(rappel, bénéficiaire, installation, canal)` ; notification Live et
transport partagent une référence de source stable. Chaque appareil est
revérifié avant transport, sans élargir la capture après confirmation. Le détail
des appareils reste réservé à la supervision autorisée ; côté organisateur,
un appareil accepté et un autre en échec donnent **Partiellement envoyé** pour
le canal Push, aucune acceptation donne Échec/Exclu selon les raisons, et un
appareil encore en traitement maintient En cours avec les succès déjà connus.

## Contrats cibles et compatibilité

Les routes ci-dessous sont implémentées dans le contrat Animation authentifié,
préfixe `/protected/animation-locale`, et vérifiées avec leurs consommateurs.
Le contrat généré décrit le code local ; il ne prouve pas son déploiement.

| Route cible | Contenu et garanties |
| --- | --- |
| `GET /lectures-globales/lots` | `items`, `next_cursor`, `has_more`, `observed_at`, `couverture`, capacités ; `limit=25`, maximum 100, filtres décrits plus haut. Une ligne contient référence opaque, animation nom/état/ID, nature, identité autorisée, lot, états distincts, quantités pertinentes, échéances, dernier rappel, actions avec motifs, références de commandes/dossier et versions |
| `GET /lectures-globales/lots/synthese` | Compteurs typés par unité et nature, portée des filtres, observation et couverture. Lecture indépendante de la pagination ; ne renvoie pas la liste des bénéficiaires |
| `GET /lectures-globales/lots/{reference}` | Détail ciblé et capacités actuelles ; historique paginé séparément, borné comme la liste. Aucun token habitant, QR/PIN ni secret fournisseur dans la réponse organisateur |
| `GET /lectures-globales/lots/{reference}/historique` | Événements autorisés de remise, dossier et rappels, 25/100, curseur lié à la cible ; mêmes exclusions de secrets |
| `GET /animations/{animation_id}/gains/{gain_id}/distribution/commandes/{cle}` | Nouveau lecteur autorisé du reçu durable de distribution ; partage la même intention que la route `envoyer` adaptée ci-dessous |
| `POST /rappels-lots/apercu` | Références/versions explicites, canaux ; retourne identifiant d’aperçu, expiration, bénéficiaires dédupliqués, contenus et exclusions bornés, aucune émission |
| `POST /rappels-lots` | Aperçu + confirmation + `Idempotency-Key`, CSRF/session ; `202` pour intention durable, opération et lien de reçu ; aucun nombre de succès transport inventé |
| `GET /rappels-lots/commandes/{cle}` | Reçu autorisé ; absence, traitement en cours et résultat confirmé distincts, sans exécution implicite |
| `GET /rappels-lots/{id}` et `GET /rappels-lots/{id}/resultats` | Suivi agrégé et résultats paginés, références et états explicites par destinataire/canal ; protection du tenant et des coordonnées |

Le détail expose une référence de dossier de fin, pas une référence reconstruite
dans le navigateur. Actions de remise/distribution réutilisent leurs contrats
existants et des composants partageables, notamment
`POST /animations/{animation_id}/gains/{gain_id}/envoyer` pour le Coffret et
`POST /animations/{animation_id}/gains-libres/{gain_id}/suivi-externe` pour le
lot externe. Conserver portée/version/clé et reçu propres à chaque commande ;
aucun envoi global depuis une ligne, aucun endpoint générique de mutation d’état.

**Adaptation de distribution nécessaire dans L2 :** transmettre et consommer
réellement `Idempotency-Key` dans une commande applicative qui réautorise acteur,
organisation et commune sous le verrou métier existant, enregistre un reçu
stable avec la distribution et ses intentions de notification dans la même
transaction. Même clé : même opération ; autre contenu : conflit ; une seconde
clé sur un gain déjà distribué ne reprogramme pas la notification initiale.
Le renvoi volontaire reste une commande distincte. Exposer une version du gain
et la faire fournir par le nouveau client (`expected_version`) ; version
obsolète refusée avant effet. Le corps reste optionnel pour les anciens clients
de `envoyer`, qui passent néanmoins par les mêmes recontrôles et verrous, sans
affaiblir le domaine. La réponse `OperationAnimation` reste compatible ; le
nouveau lecteur de reçu distingue absent/en cours/confirmé. Tester également
la course ancienne entrée/nouveau parcours pour garantir une seule distribution.

Erreurs documentées : `401/403` et purge du contexte ; `404` cible inaccessible
ou reçu absent, avec codes distincts ; `409` version/aperçu/cadence obsolète,
`422` sélection/canal/limite invalide ; `429` saturation et `Retry-After` sans
rejeu automatique d’écriture ; `503` dépendance indisponible. Un curseur invalide
possède un code distinct d’un conflit de mutation. Les droits sont relus avant
la restitution d’un reçu. Un résultat incertain garde sa clé en mémoire et
requiert une réconciliation explicite ; absence de reçu n’est pas un succès.

Liste : tri immuable `(attribue_at DESC, reference DESC)`, curseur opaque
versionné lié au tenant, aux habilitations, aux filtres et au tri, durée
30 minutes ; navigation vivante, pas promesse d’instantané exhaustif.
Accès/filtrage avant limite, `limit+1` racines puis enrichissement groupé.
Une modification d’état peut retirer une ligne du filtre : reprise annoncée.
Les filtres privés et références sélectionnées restent dans la mémoire de
l’onglet ; purge après changement d’organisation, commune, session ou droits.

Producteur : backend, schémas applicatifs et routes fines. Source documentaire
[OpenAPI E41](../epic-41-api/openapi.json), générateur backend
`scripts/documentation/generate_epic41_openapi.py`, consommateur embarqué
`localeo-animation/src/imports/openapi.json`. Vérifier aussi les composants
partagés de l’[OpenAPI E42](../epic-42-localeo-live/openapi.json), générés par
`generate_epic42_openapi.py`, et le lecteur Live du nouveau type personnel.
Les routes existantes et leurs clients restent compatibles ; ne pas modifier
la pagination des anciennes lectures. Le maintien initial de `Tirages et gains`
est remplacé par le [correctif explicite du 15 novembre](#correctif-du-15-novembre-2026--tirages-séparés-des-gains) :
la page `/tirages` devient Tirages et décommissionne sa vision Coffrets, sans
supprimer les contrats historiques des autres consommateurs. Le nouveau
consommateur n’utilise pas `collectPages` pour les listes Lots et remises ou
Tirages.

La notification personnelle nouvelle requiert contrat de type/action ciblée
et tests du clic dans Live. Elle ne dépend pas de la présence de l’animation
dans le carnet. Si le lecteur ne sait pas rendre ce type, il doit être livré
avant activation de la diffusion. Pro conserve sa validation de bon et de
prestation, avec tests de non-régression, sans nouvelle interface organisateur.

## Données, performance et reprise

Migrations additives `v319` pour les index de lecture, `v320` pour les
intentions de rappel, leurs cibles, réservations de fréquence, reçus et traces
par canal, et `v321` pour l’index de l’historique des rappels par gain.
Contraintes d’unicité effectives en base et index
des tâches en attente/échéances/baux. Aucune migration ne convertit un dossier
clos en lot remis, ne distribue un coffret, ne change une expiration ou n’envoie
un rappel historique. Les anciens gains sans contact ou mesure fiable restent
consultables avec leur limite explicite.

Consolidation réalisée par projection SQL des racines courantes. La synthèse
pré-agrège les 17 faits utilisés par les règles du domaine, par animation
autorisée ayant une racine de la branche, puis classe et additionne ces groupes.
La liste enrichit seulement les racines de sa page quand les filtres le permettent.
Aucun de ces parcours ne charge tous les gains détaillés en Python. Compteurs et
stock sont calculés dans une même requête et un même instantané PostgreSQL,
avec date de calcul et couverture explicites. Les décisions de remise restent
liées à leur référence et à leur empreinte courante. La projection n’est jamais
l’autorité des commandes ; les expirations utilisent la date courante du domaine.

Ce choix de réalisation remplace la préférence initiale pour un agrégat
persisté et sa reconstruction par lots de 500. Il évite un retard de projection
et reste soumis aux mêmes budgets. Les mesures sur 10 000 puis 100 000 gains
sont consignées dans le bilan ; la croissance des données étrangères dépasse
encore le budget de synthèse. Une extension au-delà de cette enveloppe doit être remesurée ;
si le calcul dépasse le budget interactif, préparer une projection persistée
et une reconstruction durable, sans transférer l’autorité des commandes.

| Parcours | Bornes, accès/index et transactions | Budget de conception et preuves à produire |
| --- | --- | --- |
| Liste/détail | 25/100 gains ; index organisation, commune, nature/état, date attribution et clé ; recherche préfixe normalisée indexée ; pagination des enfants ; 12 requêtes SQL maximum par page, enrichissement groupé | N=10 000 puis 10N=100 000 gains du tenant, croissance séparée des autres tenants et de l’historique ; 25 puis 100 lignes, page profonde ; p95 ≤ 800 ms, p99 ≤ 1 500 ms hors réseau client |
| Synthèse | Agrégation SQL des faits courants par périmètre ; filtres côté stockage, classement commun au domaine après regroupement, pas d’hydratation des gains ; même instantané pour les compteurs et le stock | p95 ≤ 500 ms, p99 ≤ 1 000 ms ; date de calcul et couverture, sans retard de projection persistée ; tests des valeurs inconnues et des filtres |
| Aperçu/confirmation | 100 gains maximum ; lecture groupée, cibles triées, verrou bref ; aucune communication réseau dans l’UoW | p95 ≤ 1 s, p99 ≤ 2 s ; contention deux opérateurs/mêmes gagnants et consommation concurrente ; rollback aucune intention partielle |
| Traitement rappel | Réserver au plus 25 bénéficiaires par lot, une transaction par bénéficiaire/animation ; capture SQL exacte sous 3 s, préparation des installations par pages de 100 puis 25 intentions appareil/lot ; parallélisme initial 2, baux 60 s ; équité entre organisations, reprise durable et temporisée | Mesurer débit, âge de file et mémoire à N/10N, y compris un bénéficiaire avec 10 puis 1 000 installations synthétiques ; mémoire processus supplémentaire ≤ 128 Mio ; fournisseur simulé lent/en panne, reprise après commit et double worker |
| Interface | Une page visible, maximum cinq pages de contexte en mémoire, pas de préchargement exhaustif ; suivi de l’opération ouverte uniquement, au plus huit lectures sur deux minutes, suspendu si onglet masqué | Bureau 1280 px, mobile 320/390 px, texte 200 % ; mémoire et DOM bornés, retour page/focus, refus/erreur/attente sans faux succès |

Charge mixte cible initiale : 20 sessions, dont 10 sur la même organisation,
lectures à 5 requêtes/s au total, commandes et deux workers actifs. Mesurer aussi
des paliers jusqu’à saturation, récupération, plans PostgreSQL réels, lignes
parcourues, verrous/pool et taille des réponses. À saturation : attente bornée
ou refus explicite, aucun worker par destinataire. Les budgets ci-dessus sont
des **objectifs mesurés localement, avec GL-16 encore partiel** : la synthèse
dépasse 500 ms p95 après croissance étrangère. Les rapports et limites sont
consignés dans le [bilan](verification-livraison.md), selon
[la convention de volumétrie](../../architecture/transverse/performance-volumetrie.md)
avant activation ; un index présent ou une page limitée ne constitue pas cette preuve.

## Critères et matrice de traçabilité

La matrice ci-dessous définit les preuves attendues. Les résultats des passes
de réalisation sont consignés dans la [vérification de livraison](verification-livraison.md),
avec leurs rapports et limites ; ils ne sont pas déduits des anciennes preuves
de remise.

| Critère | Comportement / propriétaire | Preuve attendue | Documentation, démonstration et exploitation |
| --- | --- | --- | --- |
| GL-01 | Entrée Lots et remises dans Suivre l’activité, commune/organisation visibles, sans sélection obligatoire d’animation | Navigateur bureau/mobile, lecteur/gestionnaire, lien direct et retour | Guide Animation et navigation ; fixture deux animations |
| GL-02 | Liste globale des trois natures, y compris Coffret sans instance et archives, gains courants distincts des remplacés | API/SQL : trois natures, deux communes/organisations, archive et ancien gagnant ; aucune fuite | E41, projection et données historiques |
| GL-03 | Compteurs exacts selon leurs unités, filtrés par contexte et datés, indépendants de la pagination et des filtres de tâche ; aucune assimilation clôture/remise/e-mail/consommation | Domaine des faits et tests de projection : partiel, zéro inconnu, expiré, révoqué, refus, gain/bon doublon, stock sans gagnant ; navigateur : quatre populations encore visibles après choix d'une tâche | Définitions ci-dessus ; fixture de chaque état, portée expliquée et couverture de projection |
| GL-04 | Filtres/recherche/pagination serveur bornés, sans chargement de toutes les animations, bénéficiaires ou pages | API et PostgreSQL N/10N, curseur périmé/autre tenant, 25/100, plans et absence N+1 | E41 ; index et mesures de capacité |
| GL-05 | Remise externe et attestation par les commandes existantes, directement dans la nouvelle section | Domaine/application/API et navigateur : succès, annulation, motif, version, rollback et relecture | Dotation/fin ; scénario synthétique, audit existant |
| GL-06 | Retrait exceptionnel d’un lot externe clos après archivage ; aucun élargissement à QR/PIN/Coffret | Non-régression du correctif du 14 novembre et navigateur depuis la liste globale | FA-04, historique et règles existantes conservés |
| GL-07 | Distribution Coffret ciblée quand autorisée, commande rendue idempotente avec reçu durable ; aucun faux consommé ni envoi global depuis une ligne | Domaine/application et PostgreSQL : instance/opération/intention uniques, échec/rejeu, deux clés et course ancien/nouveau client ; navigateur réponse perdue, refus après gel | Adaptation ciblée de `envoyer` et lecteur de reçu additif ; fixture non distribué et opération incertaine |
| GL-08 | Aperçu de rappel manuel individuel/groupé explicite, 1–100 gains, regroupement bénéficiaire/animation, zéro ne veut pas Tous | Domaine/API/navigateur : doublons, adresse partagée, changement page/filtre/commune, 101 refusé ; aucune programmation automatique | GL-ARB-02 confirmé ; modèles de rappel et guide |
| GL-09 | Choix e-mail/WebPush respecté, canaux indisponibles expliqués, aucun SMS ni e-mail de secours implicite ; diffusion multi-appareils bornée et dédupliquée | Préparation/transport simulés, préférences et preuve Live, liaison retirée, endpoint expiré, reprise entre pages d’installations et acceptation/échec partiels | Contrats Live, charte e-mail, coûts/supervision par canal |
| GL-10 | Rappel uniquement pour le droit encore exerçable ; recontrôle avant préparation et transport | Refus/remplacement/remise/consommation/expiration entre aperçu et exécution ; Coffret partiel et dossier clos | Invariant nouveau, fixtures d’interleaving, état Exclu tracé |
| GL-11 | Minimum 48 heures entre rappels par bénéficiaire/animation, tous canaux confondus ; exception terminale limitée aux droits encore exerçables, sans remise ni nouvelle attribution | Domaine et PostgreSQL : avant/à 48 heures, deux clés, terminal, campagne ordinaire toujours gelée | GL-ARB-03 confirmé ; cible FA-04 complétée, exploitation à actualiser à la réalisation |
| GL-12 | Idempotence/reçu et rollback ; mêmes intentions au rejeu, permissions revérifiées | PostgreSQL : course, réponse perdue, panne après commit, autre contenu même clé, accès révoqué | E41, unicités, reprise et diagnostic |
| GL-13 | Suivi exact par canal, succès partiel et échec visibles ; aucun succès annoncé sur acceptation seule | Workers doubles, fournisseur simulé, état incertain, réconciliation UI | Supervision existante, alertes et procédure de reprise |
| GL-14 | Notification humaine et accès au bon lot, aussi pour une animation archivée ; aucun secret dans le Push | Rendu e-mail/texte, contrat Live, clic après reconnexion, accès étranger refusé | Charte e-mail ; lecteur Live et liens personnels autorisés |
| GL-15 | Résultat, actualisation par bloc, retour/focus, saisies et sélection protégés | Navigateur 320/390/1280, 200 %, clavier ; erreurs locales, tardives, 403 et conflit | AP-18/20 ; checklist UX adaptée, pas de stockage privé durable |
| GL-16 | Budgets et saturation maîtrisés, commande réelle toujours autorisée sur les faits courants | Charge mixte et N/10N, mémoire/SQL/locks ; mesures comparées aux objectifs | E59 et rapport de capacité ; bloque l’activation si non vérifié |
| GL-17 | Migration additive, reprise et coexistence sans réémission historique ni conversion des états | Migration aller/reprise sur base jetable ; ancien client/nouveau backend ; canaux désactivés | Registre démonstration/restauration et procédures de livraison |
| GL-18 | Aucun contournement de périmètre, rôle, continuité ou consommation Pro/Coffrets | Domaine/API : lecteur, autre organisation/commune, droits retirés ; non-régression QR/PIN et prestations | Contrats partagés, conservation et supervision ERP existante |

Les règles de [pages de gestion](../../architecture/transverse/conventions-backoffice.md#ux-des-pages-de-gestion-erp)
ERP-UX-02 à 09 et 11/12 servent de checklist de parcours : cible, action, portée,
comparaison, confirmation, continuité et états accessibles. Cette évolution
ne crée pas de page SQLAdmin ; aucune refonte de l’ERP n’est nécessaire.

## Lots de réalisation, impacts et livraison

| Lot | Critères et dépendances | Périmètre réalisé et à vérifier |
| --- | --- | --- |
| L1 — Vue globale et indicateurs | GL-01 à 04, GL-15/16/18 ; gains d’animation uniquement selon GL-ARB-01 | Projection, compteurs, contrats, menu/liste et preuves |
| L2 — Remises et distribution depuis la liste | GL-05 à 07, GL-12/15/18 ; dépend L1 et commandes existantes | Réutiliser formulaires de remise, compléter idempotence/version/reçu de distribution, non-régressions |
| L3 — Rappels et livraison complète | GL-08 à 14, GL-16/17/18 ; dépend L1 ; rappels manuels selon GL-ARB-02/03 confirmés | Politique, persistance, canaux, lecteur Live, supervision, capacité, documentation/démo |

Applications : **backend** (domaine/application, lecture, outbox, migrations),
**Animation** (navigation et travail global), **Marketplace/Live** (type de
notification et accès personnel), **Pro** (consommateur à préserver, pas de
nouvel écran prévu), **projet** (sources canoniques). Les achats Coffrets hors
animation sont exclus selon GL-ARB-01. Les parcours ERP de supervision des
e-mails/Push existants sont réutilisés ; ajouter leurs références de rappel,
résultats et diagnostic sans créer une deuxième console d’envoi.

Démonstration : fixtures couvrant les trois natures, plusieurs animations,
archives, consommations partielles, sans instance, gain clos puis retrait
exceptionnel, coordonnées/Push absents et erreur transport. Faire évoluer le
générateur et le registre/restaurateur avec les nouvelles tables et clés ;
neutraliser les transports, aucune émission réelle ni génération distante
implicite. Ne pas rejouer des gains anciens pour créer des rappels.

Exploitation documentée dans les guides canoniques : éligibilité et fréquence,
modèles, traitements existants et nouveaux branchements, âge des files,
reprise d’une intention précise, résultats incertains, purge/conservation
alignées sur les dossiers et traces de gain. La lecture courante ne demande
aucune reconstruction de projection persistée.
Les secrets de lien ne doivent pas apparaître dans les journaux ou la vue globale.

Ordre de livraison prévu : migrations additives v319, v320 et v321, backend
compatible, contrats générés et leurs consommateurs, interface/lecteur Live,
validation de capacité et configuration des canaux, puis ouverture
des rappels. Désactiver l’admission de nouveaux rappels permet une reprise
opérationnelle ; ne pas supprimer des intentions ou messages déjà engagés.
Le rollback d’interface ne supprime pas la nouvelle persistance. Aucun déploiement,
envoi, mutation TEST ou changement de quota n’est demandé par la spécification.

## Réalisation et vérification

Les trois lots sont implémentés ; GL-16 reste partiel après les mesures locales.
Critères, contrats,
propriétaires, impacts et preuves attendues sont identifiés ; les trois
arbitrages produit sont confirmés. L1/L2 prolongent les parcours acquis ; L3
porte les rappels manuels, la cadence de 48 heures et l’exception terminale.
Les achats hors animation et rappels automatiques sont hors périmètre.
Le bilan sépare les preuves réussies, les reprises après échec et les contrôles
restants. Le statut historique de l’epic et ses bilans sont conservés.

Revue indépendante en lecture seule par le profil `localeo-contract-reviewer` :
deux constats intégrés à la conception, reçu/idempotence de distribution Coffret
à compléter (GL-07/12) et diffusion multi-appareils à borner (GL-09/13/16).
Ils sont traités par la commande de distribution avec reçu et par la capture
SQL exacte suivie d’une préparation paginée des installations. L’exploration préalable a aussi
confirmé la séparation nécessaire avec les SMS de gain et rappels à l’acheteur.

Contrôles documentaires finaux du 15 novembre, sur la base projet `d96bda1` et les
modifications locales de cette évolution : `py -3.14 scripts/check_guidance.py`,
**98 guides, 1 273 liens, zéro erreur ni avertissement** ; contrôle ciblé
`--changed --all-markdown`, **13 guides, 658 liens, zéro erreur ni avertissement** ;
`py -3.14 scripts/sync_documentation.py
--check-sources`, **150 sources vérifiées** ; `git diff --check`, réussi.
Ces contrôles ne valident pas les comportements métier.
Les preuves métier, PostgreSQL, navigateurs et capacité sont raccordées dans
le bilan de réalisation. Aucune recette déployée ni émission réelle n’est
effectuée dans cette implémentation.
