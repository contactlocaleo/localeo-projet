# E73 — Automatiser la recette métier sur TEST

Mise à jour du **30 octobre 2026**. Cible retenue : **environnement de test avec un nouveau jeu dédié**. Le lanceur et la préparation additive existent dans `localeo-backend/scripts/recette_e73`. La couverture des 130 scénarios du [plan métier](recette-metier.md) reste partielle : un scénario référencé au catalogue n’est pas nécessairement automatisé, et un parcours codé n’est pas encore une preuve de réussite distante.

## État concret et commandes

Évolution des domaines du 30 octobre : les nouvelles configurations du harnais
visent le portail `test-gestion-animations.localeo.city`, le site public
`test-animations.localeo.city` et Coffrets `test-marketplace.localeo.city`
séparément. Le clone privé conserve ses origines locales et ses preuves.
Les réussites ci-dessous ne constituent pas une recette des nouveaux domaines
hébergés ; voir [le bilan de l’évolution](suivi-implementation.md#évolution-locale-du-30-octobre-2026--e73-evo-domaines).

### Reprise des parcours principaux du 30 octobre 2026

#### Compléments essentiels : cohérence Live et absence de double comptage

**Le total reste 40/130 scénarios entièrement validés ; 90 restent non
intégralement couverts.** Ce passage complète des variantes de RM-21-03 et
RM-22-01 sur le clone isolé ; aucune nouvelle validation complète annoncée.

- **RM-22-01 : onze contrôles réussis** à 320/1280 px. Le reçu normal
  `inscrire-v4` (201) fournit le lien participant ; Live retrouve exactement
  les mêmes participant, animation, gain, bon et état CONSOMME que les
  projections ERP/Support, Animation et Pro déjà rapprochées. Aucun accès
  extrait de base ou d'outbox. Les initialisations techniques Live sont bloquées.
  L'accès Live légitime au gain Coffrets reste à préparer.
- **RM-21-03 : rescans responsable et salarié vérifiés.** Les deux bons déjà
  consommés sont reconnus avec les mêmes validation et version, sans bouton
  de nouvelle remise. Les sept compteurs sont rapprochés des données métier
  et affichés dans le bilan avant/après : 3 inscrits, 3 parcours commencés,
  3 terminés, 3 passages, 3 gagnants, 2 lots remis, 0 parcours non terminé.
  Aucune nouvelle consommation ni revenu déduit. Une relecture sans scan
  confirme tous les faits inchangés. Il s'agit de consommation de bons ;
  les nouvelles validations de parcours QR/PIN restent une variante distincte.
- **RM-21-03 : remplacement et bilan contemporain vérifiés** sur une autre
  cohorte externe dédiée, après REFUS synthétique par le formulaire normal.
  Douze contrôles groupés et 21 valeurs de bilan à trois stades confirment
  5 inscrits, 5 passages, 3 gagnants courants et 0 remise inchangés.
  Le premier suppléant est utilisé, l'ancienne attribution reste REMPLACE ;
  les deux autres gains et le second suppléant sont conservés. Reçu durable,
  auteur du refus, motif et versions concordent. Une commande REFUS et un
  remplacement acceptés, sans rejeu. Les validations de parcours QR/PIN et
  leurs rescans restent à couvrir ; RM-21-03 reste non barré.

Les incidents du harnais restent conservés : appel de viewport sur le mauvais
objet avant toute lecture Live, puis comparaison intégrale trop stricte des
réponses de bilan. Seuls `generated_at` et `mesures.observedAt` se renouvellent ;
les autres champs sont comparés strictement. Lors de la relecture, une tentative
GET de police Google par le portail a été bloquée. Ce blocage est tracé séparément
des commandes métier ; aucune absence de tentative externe n'est revendiquée.
Les échecs techniques initiaux ne sont ni supprimés ni transformés en succès.

Preuves privées :
`essentiels-rm2201-20261030c-live-numerique-reprise1-prive.json` et
`essentiels-rm2103-20261030c-rescan-qualification.json`, avec les instantanés
et incidents référencés. Revue indépendante de la provenance du reçu, des deux
acteurs Pro et de l'égalité des faits métier. Aucun correctif produit démontré
sur ces compléments ; aucun fichier applicatif ni TEST partagé modifié.
Le remplacement conserve quinze pièces dans
`essentiels-rm2103-20261030c-remplacement-preuves-figees.json` ; son premier
essai a été arrêté pour encodage du harnais, avant toute commande. La reprise
vérifie le même état initial avant d'agir. Synthèse privée de ce passage :
`passage-essentiel-20261030c-synthese.json`. Le backend réellement servi reste
`1.0.0+3720a08` avec les 21 correctifs figés revérifiés ; le nouveau HEAD des
applications poussé précédemment n'est pas déployé dans ce clone.

#### Nouveau passage essentiel : activation et concurrence

**Bilan courant : 40/130 scénarios entièrement validés ; 90 restent non
intégralement couverts.** RM-03-03 apporte une nouvelle validation complète
sur le clone isolé. Les bilans datés ci-dessous conservent leurs totaux historiques.

- **RM-03-03 : 33 contrôles de concurrence et 15 contrôles de relecture réussis.**
  Deux opérateurs internes distincts, connectés normalement et habilités,
  ouvrent les périmètres du même commerce synthétique à la version 2.
  La demande Animation du premier est acceptée, version 3 ; la demande
  Coffrets du second reste à la version 2 et reçoit **409 CONFLIT_VERSION**.
  Aucun écrasement ni événement supplémentaire. Le second écran affiche
  ensuite Animation « À préparer », Coffrets « Non demandé » et le bon auteur
  avec son motif dans l’historique. La commune était déjà basculée ; aucune
  commande de bascule n’a été envoyée.
- **RM-03-01 : 40 contrôles supplémentaires réussis ; scénario toujours partiel.**
  Connexion propriétaire normale, convention fictive scannée par ClamAV réel,
  revue/demande/activation Animation par Admin réussies sur un commerce
  HISTORIQUE ; faits Coffrets, prestations, modèles, engagements et reversements
  conservés. Un principal Pro reçoit 401 sur la lecture et la commande internes,
  sans effet métier. Sur une autre fixture, la convention est désormais qualifiée,
  mais l’activation reste correctement refusée 409 pour accès propriétaire absent.
  Le refus du Backoffice sans habilitation et le troisième commerce distinct
  de refus restent à couvrir. Signatures antivirus préexistantes anciennes :
  aucune fraîcheur supplémentaire revendiquée.

Les incidents du harnais sont conservés. Après le conflit, le premier navigateur
B a été fermé par le harnais à la suite d’un délai d’attente : le même opérateur
s’est reconnecté, les mêmes états et historiques ont été rapprochés à l’identique,
puis une saisie non envoyée a été reconstituée et abandonnée avec confirmation
native avant l’actualisation réelle. Il ne s’agit pas d’une session ininterrompue.
Les POST techniques `/internal/session` bloqués sont comptés séparément des
commandes métier : aucune commande métier rejouée pendant cette relecture.

Preuves privées : `essentiels-rm0301-admin-suite-20261030b-preuves/index.json`,
`essentiels-rm0303-20261030b-reprise2-index.json` et
`essentiels-rm0303-20261030b-relecture2-index.json` ; synthèse
`passage-essentiel-20261030b-synthese.json`. Les empreintes des 25 pièces
de ces trois index et les 21 correctifs figés du clone sont revérifiées.
Le backend testé reste la base `3720a085` avec ces correctifs ; les dernières
évolutions locales de navigation ERP ne sont pas installées dans ce clone.
Aucun fichier applicatif, rôle ou droit changé pour ce passage ; aucun appel
de fournisseur réel ni intervention sur TEST partagé.

#### Compléments essentiels après la préparation des domaines

- **RM-03-01 : vingt-six contrôles supplémentaires réussis.** Connexion réelle
  du propriétaire d’un commerce existant, convention explicitement fictive et
  scannée par ClamAV local réel, revue/demande/activation Animation par le
  Backoffice déjà habilité, auteurs et motifs vérifiés. Le mode HISTORIQUE et
  tous les faits Coffrets contrôlés restent conservés : ouverture, état,
  prestations, modèles, engagements, six reversements et capacités Pro. Le
  menu Pro est relu après chargement. Sur une nouvelle fixture Admin, demande
  acceptée puis activation refusée 409 sans effet pour convention et accès
  propriétaire manquants. Activation Admin, refus BO sans habilitation et
  décision depuis Pro non exécutés ; aucun profil moderne mixte ni succès
  intégral revendiqué. Antivirus réel avec témoin EICAR détecté, base de
  signatures préexistante de plus de sept jours : limite conservée.
- **RM-22-01 : sept contrôles supplémentaires réussis**, mêmes trois gains
  rapprochés entre ERP/Support et Animation, même consommation active relue
  dans Pro, et Live externe via un lien retenu d’inscription 201. Aucun objet
  remplacé dans le triplet de référence, aucune écriture métier. Live Coffret
  et numérique non prouvés par un accès légitime sur ces échantillons : partiel.
- **RM-18-03 : dix contrôles supplémentaires réussis**, participation transférée
  volontairement entre marketplace et site public Animation local distinct,
  même projection du gain relue après import. Sept exports contrôlés, second
  carnet initialement vide, empreinte de capacité conservée, réimport sans
  doublon et carnet d’origine intact. Aucune injection de stockage, aucun accès
  extrait de base/outbox. Les initialisations Live facultatives bloquées par le
  garde réseau ne bloquent pas cette reprise locale. Une seule participation
  dans le carnet : aucun bon autonome ou Coffret transféré revendiqué, ni ancien
  email/QR reçu. Fonctionnement avec installation Live disponible non vérifié.

Les incidents initiaux de harnais sont conservés : vocabulaires des projections
rapprochés selon leur contrat ; compteur des requêtes techniques bloquées
distingué des écritures métier transmises. Aucun défaut produit démontré sur ces
compléments. Preuves privées `essentiels-rm2201-preuves-20261030.json`,
`essentiels-rm1803-carnet-20261030-reprise2-prive.json` et
`essentiels-rm0301-preuves-finales/index.json` ; revues indépendantes de la
provenance, des faits Coffrets conservés et des empreintes. Le point privé
`passage-essentiel-20261030-synthese.json` rapproche **43 contrôles réussis** et
**41 pièces figées**, avec les 21 fichiers correctifs du clone revérifiés.
Aucun fichier applicatif, droit ou mode communal changé pendant ce passage,
aucun paiement ou email réel. **Le total reste 39/130 entièrement
validés** ; ces compléments n’ajoutent pas de scénario intégralement couvert.

Le clone et les interfaces locales sont redémarrés avec leurs protections
existantes. Le refus 503 du 29 octobre n’est plus reproduit : les connexions,
authentifications et lectures PostgreSQL nécessaires à ce passage réussissent.

**RM-22-02 est entièrement vérifié sur le clone et barré dans le plan métier.**
Treize contrôles rapprochent dans les vues ERP les quatre achats (179,60 €),
les trois mouvements de reversement (33,84 €) et leurs commissions constatées
(5,96 €) avec les faits indépendants. Les lots externes et numériques
n’ajoutent aucun montant Coffrets. Les huit contrôles fournisseur du 29 octobre
sont complétés par deux relectures courantes d’état, ouverture et portée.
Les faits financiers restent identiques avant/après ; aucune commande
financière, reprise de commission ou opération Stripe déclenchée.

RM-06-01 progresse avec dix contrôles : Passeport et Tombola ouverts sur la
base B1 sans option ; Chasse ouverte avec le droit acquis A2 ; droits et usages
inchangés. Plusieurs variantes distinctes par type restent indisponibles.
RM-14-02 progresse avec quatre contrôles de projection participant à 320/1280 px :
même bon valide, version 4 et échéance prolongée au 23 octobre 2027, depuis le
lien conservé dans un reçu réel d’inscription 201. Aucun accès extrait de base
ou d’outbox ; cela ne remplace pas la réception du lien personnel du bon ni
sa lecture détaillée et son QR. Ces deux scénarios restent partiels.

**RM-19-02 est également entièrement vérifié sur le clone et barré.** Le dossier
récent A conserve ses onze contrôles du 24 ; un dossier B ouvert le 23, sans
réponse et naturellement en retard le 30, apporte dix contrôles supplémentaires.
Chacun est lu par le client habilité de son organisation. Les deux calendriers
persistés expliquent les cibles distinctes du 27 octobre, à 17 h et 18 h Paris,
changement d’heure compris. Une note interne sur B conserve le retard et reste
invisible au client ; la réponse normale Support est unique et horodatée,
l’échéance initiale reste conservée. A est relu inchangé. Deux écritures de
recette seulement sur B : note interne puis réponse publique. La réponse
automatisée porte le type LOCALEO du contrat ; aucune réception email revendiquée.
Revue indépendante des six étapes sans écart bloquant. Deux incidents de
harnais avant toute commande restent consignés avec leurs preuves.

Le point privé `passage-principal-20261030-synthese.json` et le sceau
`rm2202-clone-preuves-completes-20261030.json` conservent 29 pièces avec
empreintes ; les 21 fichiers correctifs du clone ont été revérifiés.
Le complément `rm1902-clone-preuves-completes-20261030.json` conserve quinze
pièces Support et `passage-principal-20261030-seconde-synthese.json` porte le
total courant : **39 scénarios entièrement validés sur 130**, dont 27 sur le
clone et 12 antérieurement sur TEST partagé ; **91 restent non intégralement
validés**. Le premier point du 30, à 38 réussites, reste conservé.
Aucun nouveau correctif produit ni déploiement partagé ce jour.

### Reprise des parcours principaux du 29 octobre 2026

Les parcours prolongation de bon et bilan après remise/correction ont progressé :
17 contrôles de prolongation, plafond absolu et refus ; 42 valeurs de bilan
recoupées, lots remis 0 → 1 → 0 après remise puis correction normale.
Les variantes restantes maintiennent RM-14-02 et RM-21-03 partiels.

Deux anomalies reproduites ont été corrigées et rejouées sur le clone isolé :
fournisseur Animation seul proposé à tort pour une prestation Coffrets,
puis auteur de gestion d’un bon présenté comme commerçant de remise.
Huit contrôles fournisseur à 320/1280 px et cinq contrôles de relecture du même
bon passent ; aucun nouveau droit ni prolongation acceptée rejouée.
Le clone redémarré conserve les protections réseau et fournisseur, avec
21 fichiers correctifs vérifiés, dont quatre installés lors de cette reprise.
Les limites de réception email et de paiement externe restent inchangées.

Validation : 633 contrôles Audit/architecture/domaine/couverture, 37 tests
application et 28 contrôles navigateur ERP réussis le 29 octobre. Le lot
PostgreSQL/application complémentaire du 24 octobre comporte 25 succès ;
les erreurs initiales de fixture SQLite restent conservées et ont été
rejouées après ajout des seules tables manquantes, sans affaiblir les assertions.
Le [registre backend](../../roadmap/anomalies/backend.md) décrit les causes et
les impacts. Les preuves de progression ne changent pas le total de
**37 scénarios entièrement validés sur 130**.

Le point privé `passage-principal-20261029-synthese.json`, conservé dans le
dossier de campagne du backend, fige 19 pièces avec leurs empreintes et
revérifie 33 pièces antérieures ainsi que les 21 fichiers du clone.
Les suites de 633 et 37 tests se recoupent ; leurs effectifs ne s’additionnent pas.

En fin de reprise, le nouveau contrôle de session du catalogue est refusé
503 `RESTAURATION_REOUVERTURE_BLOQUEE`. Le diagnostic en lecture seule n’a pas
pu ouvrir une nouvelle connexion PostgreSQL : le fournisseur répond
`service temporarily unavailable`. Le verrou reste actif ; aucune donnée,
attestation ou configuration de protection n’a été modifiée pour le contourner.
Les rejeux fournisseur et auteur ci-dessus avaient terminé avec succès avant
ce blocage. La nouvelle relecture RM-06-01 du 29 octobre n’est pas validée.

### Priorité de passage du 24 octobre 2026

À la demande de l'opérateur, traiter d'abord les parcours principaux : création
et publication d'animation, participation, tirage, remise des gains, puis suivi
ERP/Support et export. Les variantes d'ancienneté, de concurrence, de charge
et de reprise après incident passent ensuite. Cette priorité ne transforme
pas un scénario partiel en réussite intégrale : seuls les RM entièrement
prouvés sont barrés dans la recette.

Les compléments de cette passe valident entièrement **RM-06-03** et
**RM-15-02** sur le clone : droit inclus effectivement utilisé sans nouvelle
acquisition, puis demande Chasse complète qualifiée normalement et échéance
portail/ERP concordante. Preuves privées
`droit-inclus-principal-clone-sceau-completude.json` et
`chasse-principal-clone-completude-scellee.json`. La seule capacité de
préparation accompagnée a été ouverte dans le clone ; ordonnanceur et alertes
globales restent fermés, aucune validation terrain n'est simulée.

La poursuite ajoute **RM-08-01 et RM-21-01 entièrement vérifiés** : trois essais
ajustés avec leurs refus et sans effet financier, puis comparaison réelle de
deux éditions clôturées normalement. Les six étapes de chaque scénario sont
reliées aux preuves privées `rm0801-principal-preuves-figees-20261024/index.json`
et `sources-diffusion-clone-objectifs-comparer-sceau-completude.json`.
La relecture visible de Finance et des trois motifs d’ajustement complète
RM-08-01 dans `rm0801-complement-ui-preuves-figees-20261024/index.json`, sans
modifier le premier index scellé.
Le point de contrôle privé `passage-principal-20261024-troisieme-synthese.json`
rapproche ces résultats : 37 réussites intégrales, dont 25 sur le clone,
71 empreintes d’artefacts et les 17 modules backend installés vérifiés.
Il conserve explicitement le statut de progression, sans recette globale achevée.

Le parcours principal de revue manuelle des commerces a été rejoué avec deux
opérateurs nominatifs distincts : **20 contrôles réussis**, auteurs et motifs
visibles, compteur communal relu et engagements conservés. La preuve privée
scellée reste qualifiée partielle pour RM-25-01/02 ; les variantes restantes
ne sont pas déclarées validées.

Le parcours principal d'export a produit une archive réellement téléchargée,
avec manifeste, empreintes et documents contrôlés. La notification de
disponibilité reste **en échec** : le transport normal a reçu **HTTP 401 de
Brevo**, une tentative et aucun identifiant fournisseur. Le compte Gmail
connecté a été revérifié (`demolocaleo@gmail.com`) et aucun message n'est reçu
sur l'alias de ce test. Aucun renvoi automatique ni modification des clés ;
le verrou et le journal privés de cette tentative sont conservés.

L’audit complémentaire des activations F03/F04 porte sur quatorze commerces
restaurés avec accès Pro vérifié : aucun n’est recevable pour une nouvelle
activation Animation. Leur seul prérequis manquant est `CONTRACT_DOCUMENTED` ;
le test d’accès est déjà confirmé. Le document déjà présent sur chaque dossier
ne vaut pas convention Animation qualifiée. Ce constat borné ne valide ni les
activations ni l’absence de tout autre candidat dans la base. Rapport privé
`sources-diffusion-clone-objectifs-audit-rm0304-synthese.json`, lectures seules,
aucune nouvelle attestation ni modification de périmètre.

Pour RM-05-01, une session et un menu Pro historiques ont été relus : quatre
contrôles, liens Compte, Animations, Prestations et Reversements présents.
Le mode `HISTORIQUE` et les deux périmètres `NON_DEMANDE` ne constituent pas un
profil mixte actif. Les trois profils modernes requis ne sont pas attestés
prêts ; leurs anciennes références de préparation dans le manifeste ne valent
pas nouvelle lecture ERP de leur état courant. Preuves privées
`branches-assistant-principal-inventaire-pro-rapport.json` et inventaire associé.
Aucun profil activé ni droit modifié, scénario non barré.

Résultats du passage principal dans le clone isolé :

| Références | Parcours principal effectivement vérifié | Couverture du scénario complet |
| --- | --- | --- |
| RM-03-01 | Connexion propriétaire réelle, convention fictive scannée et activation BO ; auteurs/motifs, faits Coffrets et menu Pro conservés. Nouvelle fixture Admin : demande acceptée puis activation prématurée refusée 409. | Vingt-six contrôles essentiels réussis ; mode HISTORIQUE conservé, activation Admin, BO sans habilitation et décision depuis Pro non exécutés ; scénario non barré. |
| RM-06-01 | Base B1 sans option : Passeport et Tombola ouverts ; droit Chasse acquis A2 utilisé. Droits, versions et usages inchangés, dix contrôles le 30 octobre. | Partiel ; plusieurs variantes distinctes par type non disponibles. Le blocage de connexion du 29 n’est plus reproduit. |
| RM-06-03 | Même responsable et mêmes permissions : Import accessible uniquement sur A1, refus réel sur A2 ; droit Animation INCLUS identifié, fonction ouverte et publication réussie, usage 0 à 1 sans nouvelle acquisition ni paiement. | **Complet sur le clone**, scénario barré ; six étapes et empreintes vérifiées. |
| RM-08-01 | Trois essais accordés puis ajustés par les formulaires ERP ; versions, auteur/motif et usages conservés. Fin hors base refusée 422 dans le formulaire et l’API, opérateur nominatif sans octroi refusé 403, commandes et factures inchangées. | **Complet sur le clone**, six étapes et dix artefacts figés ; revue indépendante. |
| RM-09-02 | Trois brouillons : six changements de branche persistés, assistants adaptés, blocages avec acteur/action et publication désactivée. Description externe corrigée ; une unité numérique créée, affectée et relue, sans doublon. | Douze contrôles principaux réussis ; Coffrets reste bloqué par le financement, scénario non barré. Aucun brouillon publié. |
| RM-10-02/03 | Contact, réponse, remise puis correction motivée ; auteurs conservés, refus commerçant/salarié. Refus explicite distinct de « non renseigné » après correctif domaine/projection/contrats/Animation/Live ; même événement relu à 1280/320 px. | Principal vérifié ; réception email et entrée Localeo en écriture restent à traiter. |
| RM-13-01/02 | Remises par responsable et salarié dans Pro, puis par PIN dans Live ; reçus, acteurs, dates et historiques contrôlés. | Partiel : QR saisi manuellement ; caméra et geste humain personnel du PIN non revendiqués. |
| RM-13-03 | Même bon déjà remis représenté, reçu initial retrouvé, une seule consommation et une seule notification logique. | **Complet sur le clone**, scénario barré. |
| RM-14-01/04 | Renvoi préparé par le produit et lien Live relu, ancien QR refusé après remplacement ; correction motivée d'une consommation, ancien reçu conservé et bon valide rouvert. Audits des trois actions relus. | Principaux partiels : réception email, bons expirés/révoqués et autres variantes non revendiqués. |
| RM-14-03 | Révocation motivée : QR refusé, demande PIN antérieure refusée, Live sans action, audit conservé et unité non libérée. | **Complet sur le clone**, scénario barré. |
| RM-14-02 | Trois prolongations jusqu’au plafond absolu de 365 jours, quatre refus et quatre autres bons inchangés ; motifs/auteurs relus. Projection participant du même bon valide/version 4/échéance prolongée vérifiée le 30 à 320/1280 px. | Dix-sept contrôles principaux, cinq de relecture et quatre de projection participant ; bon expiré, réception du lien personnel et lecture détaillée Live/QR non vérifiés. |
| RM-15-02 | Demande Chasse unique, brief complet et qualification ERP normale ; état et cible du 30 octobre, 17 h Paris concordants, calendrier versionné et responsabilités distance/terrain explicites. | **Complet sur le clone**, scénario barré ; quatorze contrôles, aucune validation terrain simulée. |
| RM-15-03 | Demande dédiée sans module Communication sur A2 : complément demandé dans l’ERP, délai affiché suspendu, réponse client persistée sur le même dossier et reprise de préparation ; historique, quotas et intention email contrôlés. | Douze contrôles principaux réussis ; variante A1, réception email, passage « prête » et attente sur des heures ouvrées non validés. |
| RM-17-01 | Quatre brouillons créés par les formulaires et aperçus calculés : ciblés 3/0/3/3, autorisés 0/0/0/0 avec les préférences intactes ; quota inchangé. Accès Pro responsable/salarié refusés. | Principal vérifié sur ce jeu, sept contrôles ; aucune diffusion, aperçus agrégés, variantes de populations, refus et fenêtres temporelles non entièrement couverts. |
| RM-17-02 | Nouvelle animation publiée, cinq profils réels : deux consentants sans Push reçoivent et lisent chacun le message unique ; opposé, sans accord explicite et simple abonné communal ne reçoivent aucun message de cette campagne. Un seul crédit débité, candidats exacts contrôlés. | Principal Live vérifié ; réception Push et contrôles de non-repli email/SMS non exécutés, scénario non barré. |
| RM-18-03 | Participation ajoutée depuis le reçu 201, export/import volontaire entre deux sites, réimport sans doublon, carnet d’origine conservé et même projection du gain relue. | Dix contrôles essentiels supplémentaires ; une seule participation, aucun bon autonome ou Coffret transféré ; anciens QR/emails et fonctionnement avec installation Live disponible non vérifiés, scénario non barré. |
| RM-19-02 | Dossier récent A et ancien B lu par chacun de leurs clients habilités : calendriers distincts, vrai retard maintenu après note interne puis réponse Support unique et horodatée ; échéances conservées et A inchangé. | **Complet sur le clone**, onze contrôles récents et dix sur l’ancien ; six étapes reliées et quinze pièces figées, scénario barré le 30 octobre. |
| RM-20-02 | Nouvelle édition sans les six familles d’objets de la source ; publication incomplète refusée et source conservée. | **Complet sur le clone**, scénario barré. |
| RM-21-01 | Objectifs 7/5/3 figés, modification refusée 409, publication sans objectifs relue ; deux éditions clôturées normalement et comparaison visible 0/4 inscrits, écart +4, fenêtres et couverture complètes. Zéro distinct d’absence de données. | **Complet sur le clone**, vingt-trois contrôles finaux, six étapes et empreintes vérifiées. |
| RM-21-02 | Sources mairie, commerce et inconnue : trois inscriptions distinctes, bilan et absence de suivi publicitaire contrôlés sur les parcours. | **Complet sur le clone**, scénario barré ; liens réels, sans lecture optique. |
| RM-21-03 | Quarante-deux valeurs du bilan recoupées avec les faits en lecture seule ; remise puis correction normale du gain externe dédié : 0 → 1 → 0 lot remis, autres indicateurs et gains conservés. | Principal partiel : bilans avant/après validation QR/PIN et remplacement non entièrement vérifiés. |
| RM-22-01 | Quatorze contrôles UI ERP/Support, puis sept comparaisons essentielles : mêmes trois gains dans Animation, même validation active du bon consommé dans Pro, Live externe via inscription 201. | Principal vérifié ; accès Live Coffret/numérique non établi sur ces échantillons et profils territoriaux encore partiels, scénario non barré. |
| RM-22-02 | Quatre achats 179,60 €, trois mouvements 33,84 € et commissions 5,96 € rapprochés dans les vues ERP ; libres exclus. Fournisseur Animation seul bloqué et refusé 403 ; fournisseur Coffrets autorisé conservé, état et portée relus. | **Complet sur le clone**, six étapes reliées, huit contrôles fournisseur, treize financiers et deux relectures courantes ; scénario barré le 30 octobre. |
| RM-23-01 | Huit contrôles : six postes et ventilation relus sur octobre et septembre dans l’ERP ; données non collectées explicites. Abonnement et Finance accessibles au client, lecture interne directe refusée 403. | Principal vérifié ; les six familles de mesures constatées/estimées/non valorisées sur deux mois ne sont pas toutes préparées, scénario non barré. |
| RM-24-01/02 | Flyer LIBRE régénéré, rendu visuel et QR contrôlés ; nouveau ZIP disponible contenant le même PDF, manifeste et accès responsable/ancien responsable/collaborateur/anonyme vérifiés. Anciennes archives intactes. | Partiel : notification refusée par Brevo 401 et variantes restantes non validées. |
| RM-25-01/02 | Deux opérateurs nominatifs, revues manuelles, auteurs et motifs, refus de bascule incomplète et engagements conservés. | Principal vérifié, vingt contrôles ; jonction des jeux et variantes restantes non validées. |

Les preuves restent privées : `essais-principaux-ui-clone-rapport.json`,
`rm1303-clone-preuves-completes.json`, `suivi-lots-ui-clone-rapport.json`,
`exports-clone-flyer-principal-sceau.json` et l'index de revue principale.
Les compléments sont reliés à `isolation-import-communes-clone-sceau-principal.json`,
`externe-remise-clone-couverture.json`, `edition-objets-clone-sceau-completude.json`,
`sources-diffusion-clone-objectifs-completude-scellee.json` et
`sources-diffusion-clone-completude-scellee.json` ; empreintes vérifiées.
Le passage Communication conserve ses reçus dans
`communication-principal-clone-brouillons-prive.json` : quatre créations et
quatre aperçus, sans démarrage. Index `communication-principal-clone-couverture.json`
et preuves figées `communication-principal-clone-preuves-figees.json` : sept
contrôles réussis, dont refus Pro responsable et salarié en lecture seule.
Le complément `communication-principal-clone-preuves-figees-v2.json` relie
explicitement la sélection à la source servie par le clone : comparaison
complète identique après normalisation des seules fins de ligne, empreintes
des octets LF/CRLF conservées séparément et première preuve inchangée.
Les préférences restent intactes : aucun destinataire autorisé à diffuser
dans ce jeu. RM-17-02 n'est pas exécuté par ce passage.
Les erreurs initiales de sélecteur et de
préfixe de route du harnais sont conservées ; l'intention bloquée avant serveur
a été rapprochée par lecture avant reprise.
Les erreurs de préparation du harnais sont conservées ; les commandes déjà
acceptées sont relues sans nouvel octroi ni nouvelle régénération.

Le complément Live de RM-17-02 est figé dans
`communication-live-principal-clone-preuves-figees.json` et son index de
couverture. Quatre inscriptions normales et un abonnement communal sans
participation ; accords explicites et retrait faits dans les interfaces.
Le worker normal est limité à l'UUID de cette campagne : quatre candidats
capturés exactement, deux créations Live et deux exclusions par préférence.
Les cinq carnets sont relus ; les deux messages ont été marqués lus puis
retrouvés avec les mêmes références. Quota 5/1/4 à 5/2/3, aucun Push tenté.
L'abonné communal garde son autre message, sans réception de cette campagne.

Le passage économique en lecture est conservé dans
`couts-principal-clone-rapport.json`, avec les captures et leurs empreintes.
Une seule mesure Support existe en octobre sur ce jeu ; septembre est sans
mesure. Les absences restent « Non collecté » et les coûts indisponibles ne
deviennent pas zéro. Les deux requêtes techniques de session ERP sont relevées
séparément ; aucune commande métier ni collecte n’a été lancée. Le premier
rapport du harnais, qui les comptait comme écritures métier, est conservé.

Le correctif du suivi externe est tracé dans le [registre Animation](../../roadmap/anomalies/animation.md).
Le test de reproduction échoue avant correction puis réussit : vingt-quatre
contrôles navigateur à deux largeurs et parcours adjacent de réponse perdue.
Build isolé, types et lint réussis. Le correctif installé dans le frontend
du clone porte sur un seul composant ; aucune modification de règle, de
permission ou de contrat API.

Le correctif distinct de non-remise est décrit dans le [registre backend](../../roadmap/anomalies/backend.md).
Le refus explicite persistant donne maintenant `NON_REMIS` ; contact, incident
et correction seule restent non renseignés. Domaine, projection et contrats
API/Live, schémas canoniques et consommés, présentations Animation/Live sont
alignés sans nouvel événement ni migration. Le même refus est relu à deux
largeurs dans Animation et sur les deux surfaces Live du clone ; aucune
nouvelle déclaration après installation. Preuves figées
`non-remis-correctif-preuves-20261024/index.json`, validations ciblées et revue
indépendante conservées ; email et intervention Localeo en écriture restent
hors de ce succès, RM-10-02/03 ne sont pas barrés.

Le lanceur lit les 130 identifiants et leurs étapes depuis la recette canonique, filtre par RM ou fonctionnalité, puis écrit un rapport HTML/JSON privé. Les origines des cinq applications sont limitées aux hôtes TEST explicites. Les contextes navigateur sont séparés par acteur ; les réponses métier ne sont pas remplacées. Les fichiers, mots de passe, cookies et liens restent sous `localeo-backend/demonstrations/prive/recette-e73/`, ignoré par Git. Aucun déploiement ni migration n’est effectué.

Depuis la racine de `localeo-backend`, avec Node et Playwright disponibles dans ce dépôt ou le dépôt Marketplace voisin, puis Python pour la préparation :

```powershell
# Une nouvelle campagne, hors ligne ; conserver ensuite son chemin affiché.
node scripts/recette_e73/cli.mjs init --mailbox <boite-controlee>
$recetteConfig = 'demonstrations/prive/recette-e73/<campagne>/config.json'
$recetteManifest = 'demonstrations/prive/recette-e73/<campagne>/manifest.json'

# Vérifier les hôtes, puis authentifier l’opérateur et lire les références.
node scripts/recette_e73/cli.mjs preflight --config $recetteConfig
node scripts/recette_e73/prepare-access.mjs $recetteConfig

# Plan sans effet distant, puis création/reprise additive explicitement demandée.
python scripts/recette_e73/seed.py --config $recetteConfig --output $recetteManifest
python scripts/recette_e73/seed.py --config $recetteConfig --output $recetteManifest --apply
node scripts/recette_e73/fixtures.mjs $recetteConfig

# Exécuter seulement les scénarios dont les données ont été préparées.
node scripts/recette_e73/cli.mjs list --select F02
node scripts/recette_e73/cli.mjs coverage --json
node scripts/recette_e73/cli.mjs run --config $recetteConfig --select RM-02-02 --execute
```

`prepare-access.mjs` lit uniquement les accès ERP dans le fichier privé `.env.test`, se connecte et enregistre sa session privée ; il ne crée pas de données métier. Il faut le relancer lorsque cette session expire. Les communes sont sélectionnées explicitement par `seed.commune_names` et doivent exister. Le seed journalise les commandes avant leur émission et conserve leurs clés de reprise ; ne pas supprimer ce journal pour contourner un refus. Une reprise du seed n’est pas un reset de la base. Les scénarios navigateur, eux, peuvent consommer ou modifier leurs objets : utiliser les références dédiées à chaque scénario et lire son dernier résultat avant de le relancer.

Le manifeste conserve les prérequis encore absents. Les comptes non activés sont bloqués avant connexion. Les lignes CSV/XLSX locales générées ne sont pas des commerces créés ; leurs identités sont synthétiques et ne constituent pas une vérification externe de SIRET. Le seed ne fabrique pas de dates, d’encaissements, d’acceptations ni de statuts d’onboarding.

Lorsque le frontend Animation utilise l’alias backend `test-backoffice`, renseigner
`animationApiOrigin: "https://test-backoffice.localeo.city"` dans la configuration
privée. Cette origine doit correspondre à celle de sa connexion réelle ; par
défaut, les contrôles utilisent `test-api`. Seuls ces deux hôtes TEST sont admis,
conformément à la [configuration des origines](../../exploitation/technique/configurer-epic-73.md).
Les lectures authentifiées utilisent le transport cookie explicite et les
écritures récupèrent le CSRF de cette même session. Les accès ERP et Pro gardent
leurs transports propres. Un cookie obtenu sur un hôte ne doit pas être copié
vers l’autre pour contourner une configuration incohérente.

### Invitations et lecture Gmail

L’opérateur a choisi une connexion Gmail autorisée pour lire les emails des alias de recette. L’installation et l’autorisation Google restent nécessaires avant toute lecture réelle. La présence d’une adresse dans la configuration ne suffit pas. La connexion de l’assistant ne fournit pas automatiquement des identifiants OAuth à un processus Node autonome : cette première intégration reste pilotée par l’assistant connecté, sans configuration CI permanente.

Les messages effectivement reçus sont exportés dans un fichier privé de la campagne, au format `{id, recipient, receivedAt, text, html}` (message, tableau ou enveloppe `messages`). L’import local valide le destinataire exact, la date, l’origine Animation TEST, l’unicité du lien et les doublons, puis produit les fichiers attendus par les tests :

```powershell
node scripts/recette_e73/inbox.mjs --config $recetteConfig --input 'demonstrations/prive/recette-e73/<campagne>/gmail-recus.json' --seed-invitations
python scripts/recette_e73/seed.py --config $recetteConfig --output $recetteManifest --apply
```

L’option `--seed-invitations` prépare les tokens réellement reçus pour les acteurs du seed ; elle ne les consomme pas et n’active aucun compte. Les invitations supplémentaires d’un même compte dans une autre organisation doivent être rattachées explicitement à la bonne opération. Ne jamais récupérer les tokens depuis les tables pour remplacer la réception Gmail. Ne pas transmettre les fichiers privés dans un rapport partageable.

Pour les scénarios de récupération, `inboxWaitMs` règle l’attente d’un import
réel pendant l’exécution : 15 secondes par défaut, au maximum cinq minutes.
La campagne accompagnée utilise trois minutes pour laisser agir le traitement
email puis le connecteur Gmail. Seuls les messages reçus après la nouvelle
demande sont retenus. Une expiration reste un blocage ; conserver le rapport et
préparer une nouvelle demande avant de rejouer le scénario.

### Première campagne TEST

Deux organisations synthétiques A/B ont été créées et leurs demandes validées par les parcours ERP ordinaires. Le **23 octobre**, la boîte Gmail a été vérifiée avant lecture ; les treize invitations reçues ont été acceptées par les API métier de TEST. Les douze comptes, leurs treize appartenances, leurs rôles, communes et délégations ont été relus ; les douze connexions ont été vérifiées. Aucune invitation du seed ne reste en attente. La limitation d’acceptation a été respectée, avec rapprochement distant des refus avant reprise. Les preuves et accès restent dans le dossier privé de campagne. Le compte `newManager`, réservé au scénario d’invitation, reste à inviter par ce parcours. Les références communales utilisées sont Latresne, Carignan-de-Bordeaux et Bouliac ; Martignas-sur-Jalle n’était pas présente dans les références TEST et aucune commune existante n’a été modifiée.

La première création de commerce a échoué avec HTTP 409 « Conflit de donnees : rechargez la ressource. ». La recherche bornée par préfixe de campagne ne retrouve aucun commerce. Le rejeu de la même commande avec la même clé conserve le refus ; corrélation `LOC-01d7f7d1-6475-4201-acf8-67f47e5b805a`. Sa cause SQL exacte reste à déterminer dans les logs serveur ; aucune contrainte n’a été contournée. Souscriptions, modules, commerces actifs, animations, participants et bons restent à préparer.

Nouvelle tentative demandée le **23 octobre 2026** : session ERP renouvelée,
inventaire paginé de la campagne relu, puis première création retentée avec le
même contenu et la même clé. Résultat : **HTTP 409 à nouveau**, aucun code
métier fourni par la réponse ; **zéro commerce avant et après**. Les six autres
créations n’ont pas été envoyées après ce refus. L’ancien journal a été archivé
dans `merchantRetryHistory` du manifeste privé ; le résultat courant est dans
`reprise-commerces.json`. Le code local ne mémorise que les commandes réussies
et annule la transaction sur erreur d’intégrité ; changer de clé sans diagnostic
ne constitue donc pas une résolution démontrée. La version hébergée exacte et
la contrainte serveur en cause restaient alors à confirmer.

Diagnostic du **23 octobre 2026** : la création de recette sans adresse reproduit
une violation de `ck_commercants_adresse_postale_objet` (migration v247).
Le schéma ERP inclut `adresse_postale=None` dans `model_dump()` ; le type ORM
`JSONB` sérialise cette valeur en JSON `null`. La contrainte accepte uniquement
un objet JSON ou un `NULL` SQL. Sa présence et cette différence ont été vérifiées
en lecture seule sur TEST, sans lire de données métier. L'insertion initiale
échoue avant l'initialisation des périmètres et d'OnBoard, puis toute la
transaction est annulée. Le gestionnaire ERP remplace l'erreur d'intégrité par
le message 409 générique, sans journaliser la contrainte. Le log de complétion
`LOC-6f16db04-f0e1-457b-9b63-ac604f918250` ne contient donc pas, à lui seul,
la preuve de l'exception SQL de cette requête précise.

Correctif **local, non déployé** : `JSONB(none_as_null=True)` pour l'adresse du
commerce. Aucun changement de contrat API, de migration ou de données TEST
n'est nécessaire ; les frontends et le générateur conservent le même format.
Les deux régressions (adresse omise ou explicitement nulle) échouent avant le
correctif et passent après. Le fichier de persistance comporte **9 tests réussis**,
dont la conservation d'une adresse structurée et le rejet des valeurs non objet.
Les contrôles d'architecture et de couverture requis passent : **618 tests**.
L'élargissement aux tests adresse API/application révèle **9 échecs de fixtures**
(attributs `ville_id` ou `perimetres_commercants` manquants) ; un cas représentatif
de chaque cause échoue aussi avec la déclaration ORM d'origine. Ils ne sont pas
comptés comme des succès. Les preuves techniques restent dans le dossier privé
de campagne (`diagnostic-contraintes-commerces.json`). La reprise de création
sur TEST reste à vérifier après déploiement ; aucune recette supplémentaire
n'est barrée sur la seule base de ces tests locaux.

Reprise demandée le **23 octobre 2026 à 14:54 UTC** après le commit local
`4be06ef` : session ERP renouvelée, première commande rejouée avec son contenu
et sa clé conservés. Nouveau **HTTP 409**, sans code métier ; **zéro commerce
avant et après**, les six autres créations non envoyées. La lecture de `/sante`
sur API et BackOffice TEST expose dans les deux cas `1.0.0+5aed284` : le correctif
`4be06ef` n'y est pas encore déployé. Le rapport privé `reprise-commerces.json`
et le manifeste ont été actualisés. Aucun push ni déploiement n'a été effectué.

Nouvelle reprise après push du correctif : `/sante` expose désormais
`1.0.0+4be06ef` sur l'API et le BackOffice TEST. Les **sept commerces ont été
créés puis relus avec succès**, avec les contenus et clés de reprise conservés :
`animation`, `coffrets`, `mixte`, `preparation`, `retrait`, `suspendu`, `remise`.
L'inventaire de campagne passe de **0 à 7**, avec une seule fiche par nom attendu.
Toutes les fiches sont à l'état **BROUILLON** ; ces noms décrivent leur cible
de recette et ne prouvent pas encore leurs périmètres ou statuts finaux.
Le blocage de création 409 est levé ; onboarding, périmètres et activations
restent à préparer par les parcours ordinaires. Le manifeste et le rapport
privé `reprise-commerces.json` enregistrent les sept résultats vérifiés.

Le premier passage du catalogue complet a produit **19 Bloqués et 111 Non automatisés, aucun succès métier automatique**. Ce rapport initial précède les compléments de scénarios suivants. Il reste conservé dans le dossier privé de campagne ; les réussites manuelles déjà déclarées dans la recette ne sont pas modifiées.

### Contrôles des brouillons après déblocage des créations

Le 23 octobre, le passage `run-1792768129878-749f` exécute RM-02-06 et F03 à
F05 : **14 cas restent bloqués**. La première étape de RM-02-06 réussit réellement
(sélection A puis B, contrôle des communes habilitées et refus de sélectionner A1
depuis B). La suite attend une animation A1 dédiée puis une récupération assistée
dont l'autorité doit être vérifiée. Aucun cas supplémentaire n'est barré.

L'audit ERP des sept commerces révèle `modeApplication=HISTORIQUE`,
`basculeCommune=false`, `revue=A_REVOIR`. La commune A1 contient **18 commerces à
revoir**, au-delà des sept objets de campagne. Aucune revue ni bascule communale
n'a été déduite automatiquement du nom de ces objets. Les prérequis Animation
réellement manquants sont l'adresse, la convention et le test d'accès commerçant.
Le diagnostic Coffrets comporte en plus ses exigences financières propres.
La preuve privée est conservée dans `audit-onboarding.json`.

Un contrôle API indépendant de cette bascule a été ajouté au backend :

```powershell
python scripts/recette_e73/controler_brouillon.py --config $recetteConfig --execute
```

Il ne cible que `commerce-preparation`, vérifie son nom, sa commune et son état
BROUILLON avant chaque commande, journalise l'intention avant l'effet, refuse une
fixture dont l'adresse est déjà préparée et ne relance pas une commande incertaine.
Le passage `controle-brouillon-20261023T151131310271.json` valide **8 variantes** :

| Variante API réelle | Résultat vérifié |
| --- | --- |
| Adresse explicitement nulle | 409, fiche et version inchangées |
| Code postal de quatre chiffres | 422, fiche et version inchangées |
| Pays BE | 422, fiche et version inchangées |
| Voie et lieu-dit absents | 422, fiche et version inchangées |
| Champ d'adresse inconnu | 422, fiche et version inchangées |
| Adresse FR structurée valide | 200, normalisation, version incrémentée et checklist adresse COMPLETE avec preuve |
| Modification depuis l'ancienne version | 409 pour version obsolète, adresse courante conservée |
| Adresse omise d'une modification ultérieure | 200, adresse conservée et relue depuis ERP |

L'adresse synthétique du commerce de préparation est désormais renseignée.
Aucune convention ni preuve d'accès n'a été créée par cette correction. Les autres
commerces restent inchangés. Ces contrôles techniques contribuent à la préparation
de F03/F04 sans valider RM-03-03 (deux opérateurs), RM-04-01 (engagements et accès)
ou RM-04-02 (activation puis vérification) dans leur totalité. Les **618 contrôles
d'architecture requis passent** après ajout de cet outil.

La base annuelle A1 a ensuite été préparée par le parcours administratif ordinaire
de commande gratuite : offre officielle **ESSENTIELLE**, montant proposé **0 €**,
motif de recette synthétique explicite et confirmation `OUI`, puis activation.
Une seule période **ACTIF**, avec conditions acquises **VALIDEE**, a été relue ;
la commande porte **GRATUITE_ACTIVEE**, sans paiement fournisseur ni checkout.
Les dates proviennent du serveur. Les preuves sont dans `base-gratuite.json`
et `base-modules.json`. Aucun module optionnel n'a été activé.

Le premier passage commercial `run-1792768618120-61f7` a révélé une fixture de
contexte à sélectionner et un sélecteur du lanceur trop strict sur « Chasse »
au lieu du libellé « Chasses au trésor ». Le lanceur utilise désormais le libellé
du catalogue par code module, tout en conservant les assertions indépendantes
de prix, capacité et durée. Les **28 tests Node commerciaux passent**.

Le nouveau rapport `run-1792768742029-444b` prouve **RM-06-02 entièrement réussi** :
trois devis annuels Chasse/Import/Communication, montants et capacités vérifiés,
aucune commande ni droit créé par leur consultation. Ce scénario est barré dans
la recette métier. **RM-06-01 reste partiel** : sa lecture du forfait, du quota
standard et du catalogue passe, les variantes Passeport/Tombola/Chasse restent à
exercer. La base A1 permet maintenant de poursuivre les préparations d'animations
et de modules ; les autres communes et les cas de paiement fournisseur n'ont pas
été préparés par cette activation gratuite.

### Nouveaux passages ciblés du 23 octobre

**Douze scénarios sont entièrement réussis sur TEST et barrés dans la recette :
RM-01-01, RM-01-02, RM-01-04, RM-02-05, RM-06-02, RM-16-01, RM-16-02, RM-16-05,
RM-19-01, RM-19-03, RM-20-01 et RM-20-03.** Les résultats
partiels, une commande acceptée ou des tests locaux ne complètent pas ce total.

| Scénario | Dernière preuve et limite |
| --- | --- |
| RM-02-02 | Le rejeu `run-1792769657431-9361` valide quatre étapes après correction de la reprise d'une identité déjà acceptée et du contrôle de délégation Import. Les variantes restantes maintiennent le scénario **partiel**, non barré. |
| RM-02-03 | Après acceptation dans un autre navigateur, la version d'équipe conservée par React devenait obsolète ; le GET du lanceur ne la rafraîchissait pas. Le lanceur utilise maintenant **Actualiser l'équipe** avant l'invitation suivante, sans désactiver le contrôle de concurrence ni rejouer automatiquement une commande. La régression échoue avant correction et les **23 tests Node comptes passent** après. Le rejeu `run-1792772077493-1a33` réussit trois étapes : appartenances A/B conservées, ancien lien renvoyé invalidé et nouveau accepté, changement vers un destinataire existant. **Seul le lien réellement expiré de plus de sept jours et son destinataire restent à préparer** ; le scénario reste partiel. |
| RM-16-01 | **Réussi automatiquement**, rapport `run-1792770510590-ff8a` : téléchargement du modèle, dépôts CSV/XLSX, feuille et mapping explicites, aperçus et absence d'écriture des commerces vérifiés. Le sélecteur de mapping du lanceur est corrigé ; scénario barré. |
| RM-16-02 | La fixture de 2 000 000 octets utilisait environ deux millions de lignes vides et rencontrait une limite de parsing étrangère à la borne métier visée. Elle utilise désormais des lignes d'espacement de 7 000 octets, tailles frontières conservées ; **8 tests avec le vrai parseur et 30 tests Node passent**. Le rejeu `run-1792772585337-3eed` est **réussi automatiquement** : six étapes, bornes 2 Mo/+1 octet et 100/101 lignes, XLSX/formule et inventaire ERP inchangé. Aucun import confirmé ; scénario barré. |
| RM-16-05 | **Réussi automatiquement**, `run-1792774394870-77f5`. Après réconciliation de V1 et traitement réel de V2 **TERMINE avec une mise à jour**, la reprise relie par empreinte les trois étapes antérieures réussies et vérifie les valeurs persistées dans l'interface, puis dans un aperçu non confirmé. Le sélecteur Description enveloppant est corrigé ; téléphone/contact locaux conservés, site V2 appliqué, description intacte et absence de doublon vérifiés. Aucun import terminé n'est rejoué ; scénario barré. |
| RM-19-01 | Défaut produit reproduit : le middleware navigateur Animation refusait les routes Support organisations avec HTTP 403 « Route de session Animation refusée. », corrélation `LOC-c93eb896-88b8-4e8f-b7d2-cfc655a0636a`. Le correctif **`3720a08`** autorise uniquement les chemins organisation/demandes, messages et reçus existants ; **192 tests transport/session/import et 618 contrôles d'architecture passent**, revue indépendante OK. Le déploiement est désormais constaté par `/sante.version=1.0.0+3720a08` sur API et BackOffice. Rejeu **réussi automatiquement** `run-1792772538662-5ec2` : aide, création liée au brouillon A1, réponses Support/client et relectures sans doublon. Scénario barré ; statut email distinct de sa réception. |
| RM-19-03 | **Réussi automatiquement**, `run-1792773007754-8aca` : demande A et réponse publique conservées, refus du dossier B et des notes internes depuis A, aucun repère synthétique privé divulgué après retour et rechargement. Le dossier B dédié et la note interne A ont été préparés par les API ordinaires, avec journal avant mutation ; le dossier A de RM-19-01 a été réutilisé. Scénario barré. |
| RM-20-01 / RM-20-03 | **Réussis automatiquement** dans `run-1792774003896-55cb`, après correction des oracles : dates exclusives, `isDeepStrictEqual` et refus A2 exact 422/code/violation. Les **94 tests public-operations passent**, revue indépendante OK. Création A1 et refus A2, conflit réel, reprise de saisie puis perte contrôlée de réponse après création et récupération du même reçu vérifiés ; source conservée, aucun doublon. Deux scénarios barrés. |
| RM-20-02 | L'ancien échec attendait à tort un 409 de publication ; la route historique retourne **422** avec son détail exact, confirmé par **8 tests Python** de `tests/api/test_validation_publication_brouillon.py`. Le diagnostic distant confirme `legacyDetailMatches`, `sourceUnchanged` et `validationUnchanged` à vrai. L'oracle et les contrôles avant/après participants, gains et commandes sont corrigés, sans modifier le produit. Rejeu `run-1792774637562-4cb7` : étape implémentée **réussie**, puis verdict **BLOQUE** car la couverture reste partielle (objets non exposés, accords/consentements et comparaison complète avec la source). Aucun échec courant ni succès intégral ; scénario non barré. |
| Prérequis publics | `run-1792774032413-0dee` contrôle **15 scénarios**, tous **BLOQUE** sur leurs prérequis. Ces passages remplacent leurs anciens verdicts non automatisés sans devenir des réussites ; les références et motifs sont détaillés dans le tableau des 130 RM. |

Les anomalies et leurs reprises sont reliées au [registre backend](../../roadmap/anomalies/backend.md#recette-automatisée-e73--23-octobre-2026).
La vérification finale du harnais donne **356 tests Node réussis, aucun skip**,
dont **96 tests public-operations** après le dernier correctif d'oracle.
Les **8 tests Python primaires de publication** et **10 tests d'intégration
PostgreSQL locale isolée** passent également. Ces contrôles locaux complètent
les rapports distants ; ils ne valident pas les variantes métier bloquées.
Pour le nouveau passage RM-20, le préparateur privé de troisième essai exige
les journaux des résultats déjà connus (création 201 confirmée, refus A2 422,
modification de source 200 et conflit 409), ainsi que l'absence d'essai après
perte de réponse. Il relit le reçu serveur de l'édition existante et ses sources
avant de créer deux nouveaux brouillons dédiés. Les anciens objets et archives
sont conservés ; seule une copie de configuration/manifeste reçoit les nouvelles
fixtures. Cette préparation ne constitue ni une nouvelle édition ni une
publication, et ne prouve pas le succès du rejeu.
Le tri des effets des 130 scénarios est conservé dans le fichier privé
`tri-effets-130.json` ; il ne constitue pas un rapport d'exécution.

Une **vérification de restauration locale isolée** passe : **10 tests, aucun
skip**, avec sept avertissements SQLAlchemy de réflexion. La preuve privée est
`localeo-backend/tmp/recette-e73-compatibilite-20261023T160335/results.xml`.
Elle ne constitue **pas une preuve de restauration hébergée ni de RPO/RTO** et
ne valide pas RM-25-03 ou RM-25-05. Aucun succès de charge ou de validation
humaine n'est déduit de ces passages. **L'ensemble des 130 scénarios n'a pas été
vérifié.**

### Blocages encore ouverts après qualification des 130 essais

Tous les RM disposent désormais d'un verdict issu d'un essai ou d'un contrôle
de prérequis. Les nouveaux lots A/B/C et les neuf derniers cas conservent leurs
fixtures absentes et échouent au garde préalable, avant toute action métier ;
aucun garde n'a été désactivé. **130 essais qualifiés ne signifient pas 130 tests
métier validés : 12 réussissent et 118 restent bloqués.**
La couverture du code comprend encore **103 parcours partiels sur 130** et
27 parcours complets ; même ces derniers ne réussissent sur TEST que si leurs
prérequis et toutes leurs assertions sont effectivement vérifiés. **La demande
de vérifier entièrement la recette n'est donc pas achevée.**

- **Jeu et accès commerçants** : références de scénarios, périmètres, conventions
  et preuves réelles d'accès sur appareil restent à préparer. A1 est encore en
  fonctionnement historique, avec 18 commerces à revoir dans la commune,
  au-delà du seul jeu dédié ; aucune bascule globale n'est déduite des tests.
- **Paiements, animations et lots** : commandes fournisseur TEST, confirmations
  authentiques, publications, populations synthétiques, accords, gains, bons,
  QR/PIN et variantes de continuité dédiées restent nécessaires.
- **Ancienneté et calendrier** : liens d'invitation réellement vieux de plus de
  sept jours, dossiers/exports aux échéances attendues et conservation de plus
  de trente jours ne sont pas fabriqués en changeant l'horloge.
- **Restauration hébergée** : cible TEST isolée représentative, sauvegarde de
  base/fichiers/configuration, journal de révocations/suppressions et exercice
  chronométré restent requis pour prouver les objectifs RPO/RTO. Les tests
  PostgreSQL locaux ne constituent pas cette preuve.
- **Charge et pilote** : population indépendante de 10 000 participants sur dix
  communes, dix acteurs, réservation et budgets de charge restent à préparer ;
  les avis UX Localeo puis commune pilote et leur décision demeurent humains.

Recherche des configurations et sauvegardes le **23 octobre 2026** : huit
profils opérateur privés ont été examinés. Ils déclarent le TEST partagé ou la
démo, avec des bases d'essai locales ; aucune application TEST hébergée isolée
n'y est identifiée. Le profil TEST existant est
`localeo-backend/demonstrations/prive/latresne/operator.json` : il ne doit pas
être utilisé comme cible isolée de remplacement.

Deux archives TEST historiques ont été contrôlées **hors réseau**, sans
restauration : manifestes scellés, empreintes des dumps, tailles et empreintes
des **59 fichiers** archivés, et lecture des catalogues avec `pg_restore --list`.
Les contrôles passent ; l'archive la plus récente retrouvée date du
**23 septembre 2026 à 00 h 16, Europe/Paris**. Elle correspond au journal du run
TEST mais ne prouve pas une sauvegarde récente ni le RPO de quatre heures.
Ces manifestes ne référencent pas le contrôle du journal indépendant de reprise ;
cela ne démontre pas l'absence d'un tel journal ailleurs.

La preuve privée est
`localeo-backend/demonstrations/prive/recette-e73/e73-20261022-e856fb/inventaire-restauration-20261023T175427.json`.
Les étapes identifiées alors étaient l'identification ou le provisionnement d'une cible
hébergée isolée, la sauvegarde cohérente récente base/fichiers/configuration et
le journal indépendant, puis l'exercice et ses contrôles avant réouverture.
À ce stade de la recherche, aucune ressource hébergée n'avait été créée ni
aucun service arrêté.

Préparation autorisée le **23 octobre 2026**, après désignation de TEST :
une base PostgreSQL distincte, `localeo_recette_e73_e856fb_20261023`, a été
créée sur l'instance TEST, avec connexions publiques retirées et dix connexions
maximum. La base partagée n'est pas remplacée. Une copie en ligne récente,
prise à **20 h 08 min 53 s, Europe/Paris**, contient **304 tables, 354 993
lignes contrôlées, un dump de 49 246 137 octets et 45 fichiers documentaires**. Le dump
utilise le même snapshot PostgreSQL exporté que les contrôles de lignes ;
le journal indépendant de suppressions/révocations est également exporté.

L'application isolée est préparée depuis l'archive exacte du commit déployé
`3720a08`, avec stockage privé local, fournisseurs désactivés, ordonnanceur et
workers arrêtés et garde de réouverture activé. Sa connexion à la seule
nouvelle base est vérifiée en lecture seule. La restauration est terminée :
les empreintes du schéma, des lignes et des contrôles de reprise correspondent
au snapshot sauvegardé sur les **304 tables**.

Les **45 documents** ont été remappés vers le stockage privé du clone ;
**11 imports actifs**, **20 références de fichiers Animation actifs** et
**74 médias binaires SQL** ont également été vérifiés. Les 42 préparations
Animation expirées sont consignées et exclues. Pour une référence image
relative hors DAM, la résolution locale n'est pas établie et le rendu reste
à vérifier ; cette référence existait déjà dans le snapshot. Aucune anomalie
produit n'est déduite de cette seule limite.

Le rejeu réel a révélé une anomalie du lecteur de journal sur deux anciennes
sessions commerçants dont le compteur nullable est nul. Elle est suivie dans
le [registre backend](../../roadmap/anomalies/backend.md#recette-automatisée-e73--23-octobre-2026).
Le correctif local est appliqué uniquement à l'application isolée, avec
empreintes de l'original et du fichier corrigé ; TEST partagé conserve sa
version. Le **journal original inchangé a ensuite été rejoué complètement**,
puis les anciennes capacités ont été fermées par les services propriétaires.
Les régressions passent : **4 cas PostgreSQL et 9 cas unitaires**, sans skip.
Les **4 assertions HTTP de blocage** passent avant réouverture. La reprise
technique du clone termine ensuite les **97 familles de conservation** et
les purges déléguées ; le service propriétaire autorise sa réouverture.
Le contrôle d'audit utilise le journal des opérations réellement réalisées
sur cette nouvelle cible, sans prétendre restaurer l'audit externe de TEST.
Après réouverture, l'ancien cookie capturé avant sauvegarde est refusé en
**401** et les connexions normales fonctionnent. Les cinq profils
gestionnaire A1/A2, lecteur A1, communication A1, import A1 et achat A1
retrouvent leurs communes et autorisations personnelles exactes ; les
permissions du gestionnaire correspondent aussi à la capture avant copie.
Les communes hors périmètre et l'équipe de l'organisation B restent
inaccessibles, sans changement du contexte, et les sessions créées pour la
preuve sont fermées. Le dernier passage représente **84 assertions HTTP
réussies sur cinq profils**, en plus des quatre assertions du garde.
L'index privé scellé `dossier-restauration-isolee.json` relie les sauvegardes,
empreintes, reçus et derniers rapports. L'API locale a été relancée pour
poursuivre les parcours, avec les correctifs locaux identifiés par empreintes.
Les **618 contrôles d'architecture**, **35 tests hors
réseau des outils et du correctif** et **4 régressions PostgreSQL** passent.

La copie est conservée sous
`localeo-backend/demonstrations/prive/recette-e73/e73-20261022-e856fb/copie-test-en-ligne-20261023T180854Z-f5581f74/`.
Elle a été prise pendant que TEST continuait à écrire : les séquences et
fichiers ne bénéficient pas d'un gel global. La configuration locale ne prouve
pas la configuration Render effective ; aucun chemin d'audit externe TEST
n'y est renseigné. Aucun export externe n'est présent dans cet inventaire.
Cette préparation ne constitue pas encore une preuve complète de reprise
hébergée. **RM-25-03/05 restent bloqués ; le bilan de 12 réussites et 118
blocages ne change pas.**

Les limites restantes sont la génération et la comparaison initiale du jeu
synthétique, les parcours participation/QR/PIN/remise avant et après reprise,
la restauration de l'audit externe TEST et de la configuration effective,
puis la preuve chronométrée sur une application et un stockage hébergés
représentatifs. Le clone PostgreSQL, les fichiers privés et les lanceurs sont
préparés pour poursuivre ; aucun nouveau succès intégral n'est ajouté à la
recette sur la seule base des contrôles HTTP.

Poursuite sur le clone le 23 octobre au soir : **20 contrôles QR/PIN de
coffrets restaurés passent**, y compris la consommation unique et le rejeu du
même reçu. Le défaut de réponse 500 au rejeu a été reproduit, corrigé dans le
producteur, puis vérifié ; les 665 tests ciblés et d'architecture passent.
Un lien de consultation réellement expiré reste refusé ; le parcours nominal
utilise un autre droit restauré encore valide, puis son renvoi normal par
l'outbox privée, sans prolonger artificiellement sa durée.

Une nouvelle animation LIBRE NUMÉRIQUE est créée par les commandes normales
du clone : publication, inscription, démarrage, attestation, clôture et tirage.
Le tirage initial a révélé une insertion de bon avant son attribution ; le
correctif de persistance est reproduit avec les clés étrangères PostgreSQL,
puis la même opération atteint **CONFIRMEE**. La lecture personnelle du bon,
le refus d'un jeton invalide et d'un autre commerce, la remise unique, le reçu
au rejeu et la disparition du QR après consommation sont vérifiés. Les emails
sont préparés dans l'outbox ; aucun transport fournisseur n'est attesté.

Les trois interfaces sont servies en HTTPS sur la boucle locale depuis leurs
archives Git propres. Le profil `RESTORATION_ISOLATED` exige les origines
locales exactes et l'empreinte du dossier scellé ; ses rapports sont distincts
de TEST partagé. **RM-01-04 est rejoué intégralement avec succès dans le
navigateur**, rapport `run-1792782524024-7082`. Une erreur initiale de certificat
du contexte de test a été corrigée dans le harnais. Ce rejeu confirme un cas
déjà validé ; il n'ajoute pas de nouvel identifiant aux douze réussites.
Les preuves API ne valent pas capture optique, avis humain, restauration
hébergée complète ou validation des autres variantes des cas concernés.

**Nouveau succès intégral sur le clone : RM-21-04.** Les dix contrôles du
parcours `rm2104-live-complet-clone-rapport.json` couvrent l'accès Live avant
clôture refusé, deux réponses distinctes après clôture (1 sans commentaire,
5 avec commentaire), les bornes 0/6, le troisième participant sans réponse,
le bilan organisateur à deux réponses et moyenne trois, les commentaires
anonymes visibles et les cinq canaux de notifications/outbox inchangés.
Les réponses sont enregistrées une seule fois ; la reprise après erreur du
sélecteur de rubrique et du transport cookie termine par des lectures.
Le cas est barré dans la recette avec sa cible explicite. Le bilan cumulé
comporte **37 identifiants réussis : 12 sur TEST partagé et 25 nouveaux
sur le clone**, et 93 sans succès intégral après les compléments ci-dessous. Cette couverture cumulée ne
constitue pas une recette intégrale d'une même version déployée.

Autres progrès sur le clone : les huit combinaisons LIBRE externe/numérique
et 0/2/3/5 éligibles atteignent réellement CONFIRMEE ; les gagnants, réserves,
bons et emails préparés sont comparés aux populations et à l'ordre des lots.
Les contrôles de concurrence du stock, de conservation des descriptions
engagées, de libération des surplus et de durées passent côté API.
L'import mixte atteint TERMINE_PARTIEL avec deux créations, une mise à jour
et deux erreurs ; son compteur erroné a été corrigé, testé puis rejoué sur
le même aperçu. Les créations restent BROUILLON avec OnBoard et demande
Animation, sans accès ni invitation automatiques. Les interfaces de ces
variantes restent à compléter avant validation intégrale de leurs RM.

Communication utilise désormais des clés propres au clone et les seuls
interrupteurs techniques nécessaires ; les **16 preuves runtime** confirment
le refus du réseau extérieur et de toute autre base, sans ordonnanceur ni
thread autonome. Un cadeau Communication est accordé par l'API ERP normale.
Quatre aperçus conservent le quota ; une campagne excluant l'unique personne
sans consentement termine SANS_DESTINATAIRE par le cas d'usage ciblé, sans
message Live, Push ou débit. Aucun transport fournisseur n'est lancé.
Le harnais comporte **359 tests Node réussis**, sans skip ; ces tests locaux
ne remplacent pas les parcours métier réels ci-dessus.

**RM-16-04 est également vérifié intégralement sur le clone.** Le navigateur
charge les cinq lignes, confirme seulement les trois prêtes avec accord
partiel et télécharge le rapport de la même opération terminée. Quatre
contrôles complémentaires vérifient les refus sans permission, sans module
et hors commune. Les lectures ERP et la transaction explicitement READ ONLY
portent sur les deux fiches de cet import UI, et prouvent BROUILLON, OnBoard,
demande Animation DEMANDEE, absence de compte, invitation, email et accord
automatiques. L'index `rm1604-clone-preuves-completes.json` vérifie les
empreintes et les mêmes identifiants dans les quatre rapports. Le rapport
initial du harnais conserve son échec de libellé ; seules les assertions de
refus ont été reprises, sans recréer les fiches. Le cas est barré avec sa
cible explicite, et ne vaut pas validation de cette correction sur TEST partagé.

Les parcours navigateur **RM-09-01 et RM-10-01 réussissent intégralement**
sur deux nouveaux brouillons du clone. Le premier vérifie l'absence de
présélection, le mode obligatoire et la persistance après retour arrière
(`run-1792787584279-47ba`). Le second vérifie A×2/B×1, le refus de zéro,
l'ordre B/A/A, le récapitulatif et le brouillon relu sans QR ni achat imposé
(`run-1792787672542-dd44`). Le premier essai RM-10-01 avait échoué sur le
sélecteur du second champ de consignes avant toute création serveur ; le
rejeu suit sa correction, sans assouplir les assertions métier.

### État détaillé des 130 scénarios

Instantané hors réseau du 2026-10-23T16:59 UTC : 52 rapports admissibles, uniquement les report.json des passages de campagne, namespace exact et environnement TEST. Aucun manifeste, configuration ou email lu.

**12 Réussis automatiques, 118 Bloqués, 0 Échec et 0 Non rejoué sur 130 essais qualifiés.** Les gardes de fixtures manquantes sont conservés ; une tentative bloquée avant action ne valide pas le comportement métier.

Le verdict et les étapes portent sur le dernier rapport de chaque RM. Le ratio compte les étapes réussies parmi celles enregistrées lors de ce passage, sans garantir les variantes restantes ; 0/0 signifie qu'aucune étape n'a été enregistrée. La couverture actuelle du code (complet ou partiel) ne prouve pas le succès TEST. Un ancien NON_AUTOMATISE devient NON_REJOUE seulement tant qu'aucun nouvel essai n'existe ; tous les RM ont maintenant un verdict qualifié.

Les références run-* désignent des rapports privés sans lien vers leur contenu. Une réussite entière antérieure distincte serait indiquée dans la dernière colonne, sans masquer un résultat plus récent. Les raisons sont abrégées et expurgées de comptes, sessions, liens reçus et identifiants d'objets.

| ID | État du dernier passage | Étapes réussies/total | Couverture du code | Rapport privé du dernier passage | Blocage ou précision |
| --- | --- | --- | --- | --- | --- |
| RM-01-01 | REUSSI_AUTOMATIQUE | 4/4 | Complet | run-1792741583828-647c | — |
| RM-01-02 | REUSSI_AUTOMATIQUE | 4/4 | Complet | run-1792741583828-647c | — |
| RM-01-03 | BLOQUE | 0/0 | Partiel | run-1792696129416-7b9c | Jeu accompagné resources.accounts.resetBoundaries requis. |
| RM-01-04 | REUSSI_AUTOMATIQUE | 2/2 | Complet | run-1792741151842-2e8d | — |
| RM-02-01 | BLOQUE | 0/0 | Partiel | run-1792769657431-9361 | Compte dédié pending requis dans le manifeste privé. |
| RM-02-02 | BLOQUE | 4/5 | Partiel | run-1792769657431-9361 | Validation accompagnée restante : incident réel de déconnexion puis reprise de l’invitation ; achat d’un module avec paiement TEST puis rele |
| RM-02-03 | BLOQUE | 3/4 | Partiel | run-1792772077493-1a33 | Compte dédié expiredRecipient requis dans le manifeste privé. |
| RM-02-04 | BLOQUE | 0/0 | Partiel | run-1792769657431-9361 | Jeu accompagné resources.accounts.scheduledCampaign requis. |
| RM-02-05 | REUSSI_AUTOMATIQUE | 4/4 | Complet | run-1792769657431-9361 | — |
| RM-02-06 | BLOQUE | 3/4 | Partiel | run-1792769657431-9361 | Validation humaine requise : perte d’accès préparée, demande légitime, vérification d’autorité puis récupération ERP, unicité de l’organisat |
| RM-03-01 | BLOQUE | 0/0 | Complet | run-1792768129878-749f | Préparer resources.onboarding.RM-03-01, dédié et rattaché à cette campagne. |
| RM-03-02 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-03-02, dédié et rattaché à cette campagne. |
| RM-03-03 | BLOQUE | 0/0 | Complet | run-1792768129878-749f | Préparer resources.onboarding.RM-03-03, dédié et rattaché à cette campagne. |
| RM-04-01 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-04-01, dédié et rattaché à cette campagne. |
| RM-04-02 | BLOQUE | 0/0 | Complet | run-1792768129878-749f | Préparer resources.onboarding.RM-04-02, dédié et rattaché à cette campagne. |
| RM-04-03 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-04-03, dédié et rattaché à cette campagne. |
| RM-04-04 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-04-04, dédié et rattaché à cette campagne. |
| RM-05-01 | BLOQUE | 0/0 | Complet | run-1792771129019-3d61 | features.proProfiles : trois commerces dédiés et au moins un complément produit réellement demandé requis. |
| RM-05-02 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-05-02, dédié et rattaché à cette campagne. |
| RM-05-03 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-05-03, dédié et rattaché à cette campagne. |
| RM-05-04 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-05-04, dédié et rattaché à cette campagne. |
| RM-05-05 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-05-05, dédié et rattaché à cette campagne. |
| RM-05-06 | BLOQUE | 0/0 | Partiel | run-1792768129878-749f | Préparer resources.onboarding.RM-05-06, dédié et rattaché à cette campagne. |
| RM-06-01 | BLOQUE | 0/1 | Partiel | run-1792771129019-3d61 | Nouvelle souscription sans module optionnel actif requise pour cette variante. |
| RM-06-02 | REUSSI_AUTOMATIQUE | 4/4 | Complet | run-1792768742029-444b | — |
| RM-06-03 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-06-03 et ses références dédiées avant ce parcours. |
| RM-06-04 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-06-04 et ses références dédiées avant ce parcours. |
| RM-07-01 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-07-01 et ses références dédiées avant ce parcours. |
| RM-07-02 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-07-02 et ses références dédiées avant ce parcours. |
| RM-07-03 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-07-03 et ses références dédiées avant ce parcours. |
| RM-07-04 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-07-04 et ses références dédiées avant ce parcours. |
| RM-07-05 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-07-05 et ses références dédiées avant ce parcours. |
| RM-07-06 | BLOQUE | 0/0 | Partiel | run-1792696129416-7b9c | Préparer resources.commercial.RM-07-06 et ses références dédiées avant ce parcours. |
| RM-08-01 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.commercial.RM-08-01 et ses références dédiées avant ce parcours. |
| RM-08-02 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.commercial.RM-08-02 et ses références dédiées avant ce parcours. |
| RM-08-03 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-08-03 et ses références dédiées avant ce parcours. |
| RM-08-04 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-08-04 et ses références dédiées avant ce parcours. |
| RM-08-05 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.commercial.RM-08-05 et ses références dédiées avant ce parcours. |
| RM-09-01 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | resources.features.creation exige merchantName, start, end, responseDeadline (dates Paris YYYY-MM-DD), commerce dédié et modèle Tombola disp |
| RM-09-02 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.lots.extended.RM-09-02 : cases. |
| RM-09-03 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.lots.extended.RM-09-03 : cases. |
| RM-09-04 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.lots.extended.RM-09-04 : cases. |
| RM-09-05 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.lots.extended.RM-09-05 : animationId, merchantRole. |
| RM-10-01 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | resources.features.creation exige merchantName, start, end, responseDeadline (dates Paris YYYY-MM-DD), commerce dédié et modèle Tombola disp |
| RM-10-02 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-10-02 : animationId, gainId, nonDeliveredGainId. |
| RM-10-03 | BLOQUE | 0/0 | Partiel | run-1792696129416-7b9c | Préparer resources.lots.externalFollowup avec animationId, gainId sur des objets synthétiques dédiés. |
| RM-11-01 | BLOQUE | 0/0 | Complet | run-1792752988203-1f31 | Préparer resources.lots.extended.RM-11-01 : animationId, model. |
| RM-11-02 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.lots.assignmentRace avec animations, modelId, modelLabel, units sur des objets synthétiques dédiés. |
| RM-11-03 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.lots.modelRevision avec inventoryAnimationId, engagedAnimationId, modelId, modelLabel, unitId, otherCommerceId, foreignMo |
| RM-11-04 | BLOQUE | 0/0 | Complet | run-1792752988203-1f31 | Préparer resources.lots.extended.RM-11-04 : animationId. |
| RM-11-05 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.lots.surplus avec animationId, inventoryAnimationId, modelId, modelLabel sur des objets synthétiques dédiés. |
| RM-12-01 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.lots.drawMatrix avec cases sur des objets synthétiques dédiés. |
| RM-12-02 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-12-02 : animationId. |
| RM-12-03 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-12-03 : cases. |
| RM-12-04 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-12-04 : animationId. |
| RM-12-05 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-12-05 : cases. |
| RM-12-06 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-12-06 : animationId, gainId, consumedGainId. |
| RM-12-07 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-12-07 : cases. |
| RM-13-01 | BLOQUE | 0/0 | Partiel | run-1792696129416-7b9c | Préparer resources.lots.qrConsumption avec vouchers sur des objets synthétiques dédiés. |
| RM-13-02 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.voucherJourneys.RM-13-02 et ses bons dédiés. |
| RM-13-03 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.lots.voucherJourneys.RM-13-03 et ses bons dédiés. |
| RM-13-04 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.lots.voucherJourneys.RM-13-04 et ses bons dédiés. |
| RM-13-05 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.voucherJourneys.RM-13-05 et ses bons dédiés. |
| RM-14-01 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.voucherJourneys.RM-14-01 et ses bons dédiés. |
| RM-14-02 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.extended.RM-14-02 : animationId, validId, expiredId, ceilingId, consumedId, revokedId. |
| RM-14-03 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.voucherJourneys.RM-14-03 et ses bons dédiés. |
| RM-14-04 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.voucherJourneys.RM-14-04 et ses bons dédiés. |
| RM-14-05 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.lots.voucherJourneys.RM-14-05 et ses bons dédiés. |
| RM-15-01 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.onboarding.RM-15-01, dédié et rattaché à cette campagne. |
| RM-15-02 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.onboarding.RM-15-02, dédié et rattaché à cette campagne. |
| RM-15-03 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.onboarding.RM-15-03, dédié et rattaché à cette campagne. |
| RM-15-04 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.onboarding.RM-15-04, dédié et rattaché à cette campagne. |
| RM-15-05 | BLOQUE | 0/0 | Partiel | run-1792774215736-b9fe | Préparer resources.onboarding.RM-15-05, dédié et rattaché à cette campagne. |
| RM-15-06 | BLOQUE | 0/0 | Partiel | run-1792774188513-edea | Préparer resources.onboarding.RM-15-06, dédié et rattaché à cette campagne. |
| RM-16-01 | REUSSI_AUTOMATIQUE | 5/5 | Complet | run-1792770510590-ff8a | — |
| RM-16-02 | REUSSI_AUTOMATIQUE | 6/6 | Complet | run-1792772585337-3eed | — |
| RM-16-03 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.onboarding.RM-16-03, dédié et rattaché à cette campagne. |
| RM-16-04 | BLOQUE | 0/0 | Partiel | run-1792696129416-7b9c | resources.features.partialImport.rows exige cinq lignes : deux créations valides, une mise à jour valide, deux invalides ; chacune contient  |
| RM-16-05 | REUSSI_AUTOMATIQUE | 2/2 | Complet | run-1792774394870-77f5 | — |
| RM-16-06 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.onboarding.RM-16-06, dédié et rattaché à cette campagne. |
| RM-16-07 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.onboarding.RM-16-07, dédié et rattaché à cette campagne. |
| RM-16-08 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.onboarding.RM-16-08, dédié et rattaché à cette campagne. |
| RM-17-01 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-01. |
| RM-17-02 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-02. |
| RM-17-03 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-03. |
| RM-17-04 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-04. |
| RM-17-05 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-05. |
| RM-17-06 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-06. |
| RM-17-07 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-07. |
| RM-17-08 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-08. |
| RM-17-09 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-09. |
| RM-17-10 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-10. |
| RM-17-11 | BLOQUE | 0/0 | Partiel | run-1792774156448-98aa | Préparer resources.communications.RM-17-11. |
| RM-18-01 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.discovery. |
| RM-18-02 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.merchant. |
| RM-18-03 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.legacyLinks. |
| RM-18-04 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.pushProfiles. |
| RM-19-01 | REUSSI_AUTOMATIQUE | 6/6 | Complet | run-1792772538662-5ec2 | — |
| RM-19-02 | BLOQUE | 0/0 | Complet | run-1792696129416-7b9c | Préparer resources.support.recent. |
| RM-19-03 | REUSSI_AUTOMATIQUE | 3/3 | Complet | run-1792773007754-8aca | — |
| RM-20-01 | REUSSI_AUTOMATIQUE | 4/4 | Complet | run-1792774003896-55cb | — |
| RM-20-02 | BLOQUE | 1/1 | Partiel | run-1792774637562-4cb7 | Couverture partielle RM-20-02 : relever les références des objets de la source puis créer l’édition dans ce scénario ; le parcours actuel in |
| RM-20-03 | REUSSI_AUTOMATIQUE | 4/4 | Complet | run-1792774003896-55cb | — |
| RM-21-01 | BLOQUE | 0/1 | Partiel | run-1792696129416-7b9c | resources.features.results exige animationId et metrics [{label,value}] du tableau de référence chiffré indépendant. |
| RM-21-02 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.acquisition. |
| RM-21-03 | BLOQUE | 0/1 | Partiel | run-1792696129416-7b9c | resources.features.results exige animationId et metrics [{label,value}] du tableau de référence chiffré indépendant. |
| RM-21-04 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.satisfaction. |
| RM-22-01 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.internalLots. |
| RM-22-02 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.supplierEligibility. |
| RM-22-03 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.commercialProjection. |
| RM-23-01 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.economics. |
| RM-23-02 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.budgetAlerts. |
| RM-23-03 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.budgetNonInterference. |
| RM-24-01 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.export. |
| RM-24-02 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.export. |
| RM-24-03 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.exportAccess. |
| RM-24-04 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.closure. |
| RM-24-05 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.closedOrganisation. |
| RM-25-01 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.perimeterReview. |
| RM-25-02 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.reviewRace. |
| RM-25-03 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.publicOperations.syntheticRecovery. |
| RM-25-04 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.pilotReview. |
| RM-25-05 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.publicOperations.hostedRecovery. |
| RM-25-06 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.blockedRecoveryReview. |
| RM-X-01 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.publicOperations.navigation. |
| RM-X-02 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.accessibility. |
| RM-X-03 | BLOQUE | 0/0 | Partiel | run-1792771129019-3d61 | Préparer resources.publicOperations.dates. |
| RM-X-04 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.publicOperations.recovery. |
| RM-X-05 | BLOQUE | 0/0 | Partiel | run-1792774032413-0dee | Préparer resources.publicOperations.isolation. |
| RM-X-06 | BLOQUE | 0/0 | Partiel | run-1792774273570-e980 | Préparer resources.publicOperations.volume. |

### Parcours actuellement raccordés

Les handlers ci-dessous exécutent des actions et assertions réelles lorsque leurs prérequis sont disponibles. Plusieurs sont encore partiels et terminent alors explicitement en `BLOQUE`. L’état initial du 22 octobre ne comportait aucune réussite sur TEST ; les nouveaux résultats sont distingués ci-dessous.

| Module de la suite | Identifiants raccordés | Complets / partiels côté code | Limites principales |
| --- | --- | --- | --- |
| `accounts.mjs` | F01 et F02, 10 cas | 4 / 6 | Gmail réel, états datés, déconnexion et autorité du demandeur. |
| `onboarding.mjs` | Compléments F03/04/05/15/16, 22 cas | 3 / 19 | Opérateurs nominatifs, pièces et preuves humaines préexistantes ; états dédiés. |
| `features.mjs` | RM-05-01 ; RM-09-01 ; RM-10-01 ; RM-16-01/02/04/05 ; RM-21-01/03 | 6 / 3 | Périmètres Pro et ERP, complément produit demandé, imports et références chiffrées indépendantes du bilan. |
| `commercial.mjs` | F06 à F08, 15 cas | 3 / 12 | Paiement confirmé, états temporels, incidents fournisseurs et profils ERP distincts. |
| `lots.mjs` | RM-10-03 ; RM-11-02/03/05 ; RM-12-01 ; RM-13-01 | 4 / 2 | Exemplaires, concurrence, versions, surplus et tirage. La saisie du contenu QR ne prouve pas sa capture optique. |
| `prize-journeys.mjs` | Compléments F09 à F12 et RM-14-02, 14 cas | 2 / 12 | Stocks, publication et clôture réelles du même jeu ; substitutions et prolongations encore partielles. |
| `voucher-journeys.mjs` | Compléments F13/F14, 8 cas | 0 / 8 | Réception réelle, consommation, PIN et attestations humaines. |
| `communications.mjs` | F17, 11 cas | 0 / 11 | Audience, quotas, programmation et annulation ; réception, appareils et incidents à prouver. |
| `public-operations.mjs` | F18/20/22 à F25, RM-21-02/04 et transverses, 32 cas | 2 / 30 | Éditions complètes côté code ; parcours publics, Live, bilans, exploitation et charge encore partiels. |
| `support.mjs` | F19, 3 cas | 3 / 0 | Échanges, échéances et confidentialité ; calendrier indépendant et dossiers synthétiques requis. |

Les **130 identifiants disposent d’un parcours intégré : 27 complets et 103 partiels côté code**. Cela ne vaut pas réussite des 130 tests métier. `coverage --json` produit, sans connexion distante, la matrice exhaustive par RM : module propriétaire, qualification, prérequis et travail restant. Les déclarations sont contrôlées contre la recette canonique ; un parcours déclaré partiel termine obligatoirement en `BLOQUE`, même si ses étapes implémentées passent. Les scripts refusent d’inventer un objet manquant ou de qualifier complet un parcours déclarant du travail restant.

Les parcours complets codés sont RM-01-01/02/04, RM-02-05, RM-03-01/03, RM-04-02, RM-05-01, RM-06-02, RM-08-01/02, RM-09-01, RM-10-01, RM-11-01/02/03/04/05, RM-12-01, RM-16-01/02/05, RM-19-01/02/03 et RM-20-01/03. Leur qualification décrit l’implémentation ; seul un rapport réel réussi permet de barrer un cas dans la recette.

Les états et UUID requis sont décrits par les métadonnées des modules et leurs champs `manifest.resources`. Les mutations journalisées refusent le rejeu après démarrage : examiner le résultat et l’état distant avant de préparer un nouveau jeu. Les sessions ERP nominatives se configurent dans `erpSessions[role] = {cookie, actorId}` ; chaque contexte vérifie son identité interne réelle avant navigation. Les tests exigeant deux opérateurs refusent deux rôles pointant vers la même identité.

Les mesures de charge RM-X-06 exigent une réservation TEST explicite, une fenêtre active, des acteurs dédiés, une population préparée et des budgets avant toute ouverture de session ; elles restent bornées en durée et en pagination. Les dossiers de restauration et de pilote sont lus avec empreintes et chronologies, sans déclencher une restauration ni attester une décision humaine. Les QR renouvelés pendant un parcours sont masqués et les erreurs de scanner ne conservent pas leur valeur.

Contrôles exécutés le 22 octobre : **94 tests Node de l’outillage réussis**, **664 tests Python ciblés et d’architecture réussis**, contrôle des guides sans erreur et **130 sources documentaires vérifiées**. Le passage distant actualisé conserve **33 Bloqués et 97 Non automatisés**. Les cinq hôtes TEST répondent HTTP 200 ; `/sante` annonce `release: V1`, sans SHA exploitable pour attester l’identité du code hébergé. Ces preuves locales et ces précontrôles ne constituent pas une validation métier de l’epic.

### Reprise du 23 octobre

Les corrections du lanceur portent sur le succès HTTP **201** de la création
de session, l’alias API et le transport cookie, l’ouverture des liens email dans
un nouveau document et les noms des nouvelles fixtures d’import. Les fixtures
déjà préparées restent conservées ; une campagne contenant les anciens noms
doit être adaptée explicitement avant les tests d’import. Aucun changement de
règle produit, de contrat API, de migration ou de déploiement n’est nécessaire
pour ces corrections d’outillage.

| Scénario exécuté sur TEST | Résultat observé |
| --- | --- |
| RM-01-01 | **Réussi automatiquement** : réponses connue/inconnue identiques, email réellement reçu et formulaire ouvert ; identité connue inchangée et aucune identité créée pour l’adresse inconnue. |
| RM-01-02 | **Réussi automatiquement** : lien consommé une seule fois, ancien mot de passe et deux anciennes sessions refusés ; nouveau mot de passe accepté, compte indépendant préservé. |
| RM-01-04 | **Réussi automatiquement** : preuve erronée sans effet ; changement confirmé, ancien mot de passe et anciennes sessions invalidés, autre compte préservé. |
| RM-02-06 | **Partiel, verdict du lanceur Bloqué** : changements explicites A/B et refus de sélectionner A1 depuis B vérifiés, contexte B/B1 inchangé après refus. L’accès à une animation de l’ancien contexte et la récupération assistée restent à vérifier avec leurs prérequis. |
| RM-02-05 | **Réussi automatiquement** : après le premier passage en échec conservé, un transfert inverse distinct sur T vérifie proposition, refus du départ, droits des deux sessions et responsable unique. L’audit de proposition et d’acceptation est rapproché par auteur, date et version. Le manifeste principal a été rapproché de l’état final réel. |
| RM-16-02 | **Ancien passage bloqué avant dépôt** : le module Import et les actions `DEPOSER`/`CREER_FLUX` n'étaient alors pas ouverts sur A1. Aucun dépôt ni création de commerce lors de ce passage ; voir les nouveaux passages ciblés pour le correctif de fixture et le rejeu restant. |

Références privées de cette reprise : `run-1792749126677-c07e` pour le transfert
réussi et `run-1792749171725-531c` pour le refus préalable de l’import. Les
rapports restent dans le dossier de la campagne ; ils ne sont pas exportés avec
cette documentation.

Les rapports JSON/HTML, les anciennes tentatives en échec ou bloquées et les
exports Gmail restent dans la campagne privée. Les mots de passe courants sont
actualisés dans son manifeste après confirmation ; avant un nouveau scénario
de changement, préparer un `nextPassword` distinct. La lecture Gmail reste
pilotée par l’assistant connecté : ce résultat ne constitue pas une intégration
email autonome pour la CI.

### Variantes complémentaires du 23 octobre

| RM | Compléments automatisés | Preuves encore nécessaires |
| --- | --- | --- |
| RM-03-01 | Demande puis activation par ADMIN et Backoffice nominatif ; refus du Backoffice non habilité et de Pro ; états inchangés après refus, auteurs et motifs exacts dans l’historique. | Parcours complet côté code ; trois commerces et sessions dédiés avec prérequis réellement validés. |
| RM-04-02 | Manque d’adresse explicite, activation refusée et Pro non opérationnel ; correction OnBoard, vérification serveur puis activation et écran Pro chargé. | Parcours complet pour ce prérequis précis ; conventions et test appareil doivent déjà avoir été réellement validés. Aucune attestation n’est produite par le lanceur. |
| RM-05-01 | Trois périmètres ERP rapprochés des identités Pro ; menus, liens directs refusés et fonctions autorisées chargées ; préparation accessible pour un complément effectivement demandé. | Parcours complet côté code ; trois commerces distincts et un complément en préparation à préparer dans la campagne. |
| RM-16-02 | Borne 100/101 lignes ; 2 000 000 octets et un octet de plus ; vides intercalés et en fin de fichier ; email invalide et véritable formule XLSX avec valeur en cache ; inventaire ERP paginé inchangé. Tailles, lignes et empreintes des fichiers sont journalisées avant dépôt. | **Réussi sur TEST** dans `run-1792772585337-3eed` après correction de la fixture de taille ; scénario barré. |
| RM-06-04 | Devis aux nouvelles conditions du catalogue et conservation des acquis précédents. | Publication administrateur, refus non administrateur et historique sur cible réservée. |
| RM-07-03 | Devis sur bases active et expirée, retrait explicite d’un module acheté, dates de renouvellement calendaires Paris et absence de conversion des essais/cadeaux. | Paiements authentiques, activation et pièces finales. |
| RM-07-04 | Devis de baisse au prochain terme, sans modification immédiate du forfait ni des usages. | Paiement, activation et rapprochement final des périodes et pièces. |
| RM-11-01 | Création du modèle, génération réelle de trois exemplaires uniques, contenu et commerce figés, absence de bon prématuré ; interruption de réponse après acceptation serveur puis consultation du même reçu sans deuxième génération. | Parcours complet côté code ; jeu dédié et exercice contrôlé requis sur TEST. |
| RM-11-04 | Durées 1/90/365, refus 0/366 ; publication et gel du même brouillon, checkpoint puis tirage après clôture réelle, échéance depuis l’attribution. | Parcours complet côté code ; reprendre seulement le checkpoint `ATTENTE_CLOTURE`, avec `resume` préparé après clôture réelle de la même animation. Les opérations incertaines ne sont jamais rejouées. |
| RM-12-05 | Refus conservé, suppléant comparé à une référence indépendante d’éligibilité et premier transport inchangé. | Préparation attestée de cette référence et preuve temporelle indépendante d’un renvoi ultérieur. |
| RM-12-07 | Deux demandes réelles de retirage avec/sans candidat ; maintien du tirage initial, population figée, exclusion des anciens gagnants et absence de candidat inventé. | Motifs/auteurs dans l’audit habilité et préparation réelle du candidat redevenu éligible. |
| RM-20-01 | Formulaire, dates et sections, confirmation et création journalisée ; inventaires complets A1/A2 avant/après, source inchangée et refus intercommune exact sans création cachée. | Parcours complet côté code ; source dédiée et même gestionnaire réellement habilité sur A1/A2 requis. |
| RM-20-02 | Contrôle des participants, gains, commandes et paiements non recopiés ; publication réellement refusée et brouillon inchangé. | Cas encore partiel : création depuis la source dans ce scénario, QR et autres capacités/accords/consentements non projetés à rapprocher sans inventer de preuve. |
| RM-20-03 | Source réellement modifiée dans une seconde session ; ancien formulaire refusé, saisie récupérable ; réponse coupée après création serveur et récupération du même reçu dans l’interface sans seconde écriture. | Parcours complet côté code ; source modifiable, dates préparées et accord d’exercice de perte de réponse requis. |
| RM-21-04 | Refus avant clôture et des notes 0/6, enregistrement Live de 1/5 avec/sans commentaire, participant sans réponse et variation de la moyenne. | Absence de notification automatique à rapprocher des traces autorisées. |
| RM-24-01 | Refus d’une demande collaborateur distinct, demande responsable par formulaire, jour cible Paris et suivi borné de la préparation. | Notification réellement reçue, téléchargement privé de l’archive et heure cible complète selon les cinq jours ouvrés. |

Les tests locaux de ces compléments exercent aussi des réponses erronées :
fiche modifiée pendant un aperçu, pagination instable, quatrième exemplaire,
commerce de modèle incorrect, ancien gagnant réintroduit, population changée,
prix ou période incohérents. Ils vérifient le lanceur et ne remplacent pas son
exécution sur les applications TEST. Les lignes conservant des variantes à
implémenter restent partielles ; aucun nouveau succès distant n’est déduit
des tests locaux, même pour un parcours complet côté code.

Le passage ciblé `run-1792752988203-1f31` contrôle les prérequis de RM-03-01,
RM-04-02, RM-05-01, RM-11-01 et RM-11-04 dans la campagne actuelle : **cinq
Bloqués avant toute action**, faute de références privées préparées pour ces
nouveaux parcours. Le refus HTTP 409 de création des commerces reste ouvert ;
ces cas demeurent non barrés dans la recette métier.

Le passage `run-1792753361199-3bb0` ajoute RM-20-01 et RM-20-03 : **deux
Bloqués avant toute action**, faute de sources d’édition préparées. Cette reprise
achève donc l’implémentation de sept anciens cas partiels, mais n’ajoute aucune
réussite métier distante aux quatre déjà consignées.

Le transport Communication distingue désormais les réponses contractuelles :
création 201, aperçu/annulation 200, envoi/programmation/reconfirmation/reprise
202. Un reçu 202 contenant la campagne et son opération est accepté comme reçu
de commande ; un corps `EN_COURS` reste bloquant et aucune livraison n’est
déduite de l’acceptation HTTP.

Validation locale : **323 tests Node réussis, aucun skip**, avec
`node --test tests/frontend/recette-e73-*.test.mjs`. Base backend
`5aed284`, complétée par les changements locaux du lanceur ; documentation sur
base `6e46edd`. Les cinq surfaces TEST répondent ; le backend annonce toujours
`V1`, sans SHA permettant de rapprocher précisément la version hébergée du code
local. Le catalogue complet n’a pas été rejoué ; les autres scénarios et les
réussites humaines gardent leurs résultats antérieurs. La préparation des
commerces, souscriptions, modules et animations reste nécessaire pour poursuivre
les parcours qui en dépendent.

## Résultat attendu

Exécuter un scénario par son identifiant RM, une fiche fonctionnelle ou toute la campagne. Chaque variante possède ses prérequis, ses actions et ses assertions observables. Un parcours passe uniquement si toutes ses assertions réussissent. Lancer une route API avec succès ne remplace pas la vérification de l’action dans l’application.

Le rapport conserve, par variante : identifiant de campagne, versions déployées connues, surface, rôle synthétique, objets du jeu, prérequis contrôlés, étape atteinte, observations, durée et verdict. Les résultats automatiques sont séparés des validations humaines ; RM-01-01 et RM-01-02 conservent leur réussite manuelle déjà déclarée.

## Nouveau jeu et séparation des données

- Une campagne reçoit un identifiant unique et un préfixe de noms `RECETTE-E73-<campagne>`.
- Préparer deux organisations A/B et trois rattachements communaux A1/A2/B1, les profils Responsable/Gestionnaire/Lecteur et les délégations Achat/Import/Communication distinctes.
- Préparer les commerces Animation, Coffrets, mixtes, salariés et cas de retrait/suspension, les trois dotations, souscriptions/modules, participants, bons et fichiers décrits dans la recette.
- Décliner les états incompatibles sur des objets différents ; conserver les identifiants créés dans un manifeste privé, afin de reprendre sans créer de doublons.
- L’utilisateur a désigné la boîte de recette. Sa valeur et les alias par campagne sont placés dans la configuration privée, jamais dans les sources de tests ou rapports versionnés.
- Préparer les ajouts par les interfaces et services métier existants. Ne pas modifier directement les statuts des tables de TEST pour fabriquer un succès.
- Le générateur de démonstration actuel est un outil de remplacement de jeu : son installation/reset ne doit pas être utilisée pour cette préparation additive. Aucun remplacement du jeu actuellement installé n’est demandé.
- Ne pas modifier les paramètres globaux, tarifs actifs ou permissions de comptes existants pour faire passer un test. Les variantes qui ne peuvent pas être isolées par leurs données restent bloquées sur la cible partagée.

## Socle d’exécution et compléments attendus

1. **Précontrôle** : vérifier les URL TEST, accès, versions, rôles, rattachements, modules, fournisseurs de test, stockage et workers utiles. Une permission absente n’est pas contournée.
2. **Préparation** : créer/retrouver le jeu de la campagne, vérifier chaque état attendu, puis produire son manifeste privé. Les secrets restent hors Git et hors rapport.
3. **Navigation réelle** : Playwright avec un contexte navigateur par acteur, mobile et ordinateur pour les parcours concernés. Utiliser les frontends et le backend réellement déployés, sans intercepter leurs réponses métier pour les remplacer par des succès simulés.
4. **Effets différés** : suivre les états réels avec délais bornés ; un email en file d’attente ne prouve pas sa réception et un paiement retourné dans le navigateur ne prouve pas son encaissement confirmé.
5. **Verdicts** : Réussi automatique, Échec, Bloqué (prérequis précis), Non exécuté ou À valider humainement. Un scénario dont une variante reste non exécutée n’est pas validé globalement.
6. **Rapports privés** : HTML et JSON, captures utiles après masquage, références de corrélation expurgées. Les traces navigateur brutes contenant cookies, mots de passe, PIN, QR ou liens d’invitation ne sont pas des pièces partageables.
7. **Reprise** : rejouer uniquement les scénarios sélectionnés sur leurs objets dédiés. Ne pas réinitialiser automatiquement toute la base.

L’outillage exécutable transversal et les configurations privées appartiennent à `localeo-backend` ; les helpers et sélecteurs propres à une application peuvent rester auprès de ses tests. Les cinq dépôts restent indépendants, sans mode de recette ajouté au produit. Le suivi exhaustif des versions hébergées, les captures masquées et la couverture complète des variantes restent à compléter ; le rapport actuel fournit les étapes réellement vérifiées et leurs motifs de blocage.

## Contrôles particuliers

**Emails.** Les invitations et réinitialisations doivent être envoyées aux alias contrôlés du jeu. Automatiser la récupération des liens exige un accès autorisé à la boîte ou un dispositif de réception de test. Une adresse email seule ne donne pas cet accès. En l’absence de lecture automatique, la récupération du lien reste assistée et le test est signalé comme tel. Ne pas extraire les secrets de la base pour remplacer la preuve de réception.

**Paiements et Push.** Utiliser uniquement les intégrations et destinataires de test. Distinguer état fournisseur, état applicatif, réception navigateur et lecture Live. La permission Push et la qualité sur appareil réel peuvent demander une vérification complémentaire.

**Temps.** Ne pas avancer l’horloge d’un environnement partagé. Utiliser des objets synthétiques préparés légalement dans leur cycle de vie, attendre la borne réelle ou exécuter la variante sur cible isolée avec horloge contrôlée. Le fuseau du navigateur peut être changé sans modifier l’horloge serveur.

**Incidents.** Une perte de réponse limitée au navigateur doit être déclenchée après prise en compte si c’est l’objet du test. Une requête annulée avant son traitement n’en apporte pas la preuve. Les arrêts de services, pannes fournisseur, restaurations et charge exigent une cible ou un créneau réservé.

**Humain.** Un script peut vérifier les champs et transitions, mais pas attester l’autorité d’un demandeur, la vérification sur le terrain ou l’avis UX de Localeo puis Martignas-sur-Jalle. Ne pas signer ces décisions à la place de leurs responsables.

## Inventaire des 130 scénarios

Les catégories désignent le mode cible, **pas une couverture déjà acquise** :

- **Navigateur** : interactions et assertions automatisables, sous réserve du jeu et des fournisseurs.
- **Préparation technique** : le navigateur est complété par des états datés, incidents, événements ou paramètres dédiés.
- **Part humaine** : automatisation des contrôles informatiques et résultat humain distinct.
- **Cible réservée** : scénario à isoler ou à exécuter dans un créneau explicitement réservé.

Cette table décrit la **cible de couverture**. Consulter les handlers de `scripts/recette_e73/scenarios` et le dernier rapport pour la couverture réelle ; un identifiant absent des handlers reçoit `NON_AUTOMATISE`, un parcours partiel ou privé d’un prérequis reçoit `BLOQUE`. Les tests unitaires des outils utilisent des doubles locaux et ne valident pas les applications hébergées.

| Test | Scénario de référence | Mode cible |
| --- | --- | --- |
| RM-01-01 | Demander une récupération avec l’email connu puis une adresse inconnue. | Navigateur |
| RM-01-02 | Utiliser un lien valide, définir le nouveau mot de passe, puis réutiliser le lien et tenter l’ancien mot de passe. | Navigateur |
| RM-01-03 | **Accompagné :** tester le lien avant puis à/après son échéance d’une heure. | Préparation technique |
| RM-01-04 | Changer le mot de passe connecté : d’abord avec une preuve d’identité erronée, puis correcte. | Navigateur |
| RM-02-01 | Déposer une demande d’organisation/communes, tenter d’utiliser A1 avant décision, puis faire valider le rattachement par Localeo. | Navigateur |
| RM-02-02 | Inviter un nouveau collaborateur Gestionnaire sur A1 ; accepter ; comparer à un Lecteur et à un Gestionnaire sans Achat/Import/Communication. | Navigateur |
| RM-02-03 | Inviter un email déjà associé à un compte, accepter avec ce compte ; renvoyer une autre invitation et essayer l’ancien lien ; essayer un lien expiré de 7 jours. | Préparation technique |
| RM-02-04 | Retirer une autorisation avec la session du collaborateur ouverte ; ajouter A2 à l’organisation sans l’ajouter au collaborateur ; tenter un lien direct hors droit. | Navigateur |
| RM-02-05 | Proposer un transfert de responsabilité ; tenter le départ du dernier responsable avant acceptation ; faire accepter le successeur actif. | Navigateur |
| RM-02-06 | **Accompagné :** simuler la perte des accès responsables et demander une récupération ; changer ensuite d’organisation avec le compte multi-organisations. | Part humaine |
| RM-03-01 | Faire demander/activer Animation par l’administrateur puis par le Backoffice habilité ; refaire sans habilitation et depuis Pro. | Navigateur |
| RM-03-02 | Ajouter Coffrets à un commerce Animation dont les compléments Coffrets sont incomplets ; terminer les prérequis puis activer. | Navigateur |
| RM-03-03 | **Accompagné :** deux opérateurs modifient la même fiche depuis des versions ouvertes avant la première modification. | Navigateur |
| RM-04-01 | Compléter identité, responsable, coordonnées et engagements Animation, sans prestations ni pièces bancaires Coffrets. | Navigateur |
| RM-04-02 | Omettre un prérequis Animation puis tenter l’activation ; le compléter et faire vérifier le dossier. | Navigateur |
| RM-04-03 | Demander ensuite Coffrets, y compris sur un dossier déjà clos ; vérifier les données et compléter les pièces propres au nouveau produit. | Navigateur |
| RM-04-04 | Préparer/envoyer les communications et conventions d’un dossier Animation seul puis mixte ; consulter leur suivi. | Navigateur |
| RM-05-01 | Ouvrir Pro avec chacun des trois périmètres ; parcourir menus et liens directs vers les fonctions absentes. | Navigateur |
| RM-05-02 | Connecter le salarié et scanner ; tenter administration, finances, gestion de droits et action d’un autre commerce. | Navigateur |
| RM-05-03 | Faire participer un commerce Animation seul à une animation dotée en coffrets et valider un passage. | Navigateur |
| RM-05-04 | Retirer Animation pendant une session ouverte ; tenter un nouvel engagement, un passage d’une participation déjà acceptée à une animation publiée et une remise de bon déjà attribué. | Navigateur |
| RM-05-05 | Retirer Coffrets avec une prestation déjà engagée dans un coffret vendu ; consulter règlement et historique, puis tenter un nouvel engagement. | Navigateur |
| RM-05-06 | Suspendre administrativement le commerce d’un jeu de continuité puis retenter QR/PIN. | Navigateur |
| RM-06-01 | Consulter forfait et modules d’une nouvelle souscription ; ouvrir les variantes de scénarios. | Navigateur |
| RM-06-02 | Vérifier les offres initiales et leur récapitulatif. | Navigateur |
| RM-06-03 | Avec le module acquis sur A1, tenter l’usage sur A2 ; consulter un droit inclus sans achat. | Navigateur |
| RM-06-04 | Modifier un prix/quota par l’administrateur ; consulter l’ancienne souscription puis préparer son renouvellement ; tenter la modification sans rôle administrateur. | Préparation technique |
| RM-07-01 | Préparer l’achat à six mois restants puis confirmer en mode test. | Préparation technique |
| RM-07-02 | Annuler/faire échouer un paiement ; revenir plusieurs fois sur le succès d’une autre commande ; **accompagné**, rejouer sa confirmation et tester un paiement tardif devenu incompatible. | Préparation technique |
| RM-07-03 | Renouveler avant puis après échéance ; examiner les modules repris au récapitulatif et en retirer un. | Préparation technique |
| RM-07-04 | Demander une montée en gamme en cours de période puis une baisse ; comparer échéance et usages déjà consommés. | Navigateur |
| RM-07-05 | Demander l’arrêt puis un remboursement de base ou module ; faire décider un montant partiel/total, et tenter un montant supérieur au solde remboursable. | Navigateur |
| RM-07-06 | Modifier les coordonnées de facturation avec Achat puis sans ; comparer ancienne facture et nouveau document ; ouvrir un document de B depuis A. | Navigateur |
| RM-08-01 | Accorder un essai de chaque module, puis ajuster durée/quota avec motif ; refaire sans habilitation. | Navigateur |
| RM-08-02 | Offrir les modules jusqu’à fin de base puis sur une durée plus courte. | Navigateur |
| RM-08-03 | Consommer sous un droit, ajouter un droit comparable puis laisser finir l’essai. | Préparation technique |
| RM-08-04 | **Accompagné :** répéter la fin des droits par expiration de module, retrait commercial anticipé, puis expiration de base. Tenter nouveaux usages et continuités. | Préparation technique |
| RM-08-05 | À expiration, ouvrir une campagne programmée non commencée puis renouveler le droit. | Préparation technique |
| RM-09-01 | Créer sans choisir la dotation, puis choisir Libre sans mode ; revenir en arrière dans le formulaire. | Navigateur |
| RM-09-02 | Choisir successivement les trois branches sur des brouillons sans engagement ; regarder l’assistant puis omettre un prérequis pertinent. | Navigateur |
| RM-09-03 | Publier une Libre/externe et une Libre/numérique correctement préparées sans commande Coffrets. | Navigateur |
| RM-09-04 | Engager une réservation/affectation puis essayer de changer de mode ; refaire après publication. | Navigateur |
| RM-09-05 | Acheter/consommer un coffret avec le commerce Coffrets seul ; exécuter publication, réservation/activation et envoi d’un gain d’animation Coffrets historique. | Navigateur |
| RM-10-01 | Créer « Lot A » quantité 2 puis « Lot B » quantité 1 ; saisir responsable/consignes et réordonner avant publication ; essayer quantité nulle. | Navigateur |
| RM-10-02 | Après attribution, lire l’email et le suivi avant toute réponse du gagnant. | Navigateur |
| RM-10-03 | Enregistrer contact, réponse puis remise déclarée ; corriger la déclaration avec motif ; essayer avec un simple commerçant/salarié. | Navigateur |
| RM-11-01 | Créer un modèle avec un seul commerce de remise, générer 3 exemplaires ; répéter la demande après une réponse incertaine accompagnée. | Préparation technique |
| RM-11-02 | Affecter un exemplaire à une animation ; tenter de l’affecter à la seconde, y compris depuis deux sessions simultanées. | Navigateur |
| RM-11-03 | Modifier la description du modèle après engagement ; essayer de changer le commerce de remise et d’utiliser un exemplaire de B1. | Navigateur |
| RM-11-04 | Choisir la durée 1, 90 puis 365 jours sur des brouillons ; essayer 0 et 366 ; publier et retenter l’édition. | Navigateur |
| RM-11-05 | Après attributions, libérer le surplus jamais attribué sur confirmation ; tenter la même chose avec un exemplaire attribué puis révoqué. | Navigateur |
| RM-12-01 | Préparer puis confirmer le tirage pour chacune des quatre populations (0, 2, 3 et 5 éligibles pour 3 lots). | Navigateur |
| RM-12-02 | Recharger, rejouer la confirmation ou reprendre après réponse perdue avec le référent. | Préparation technique |
| RM-12-03 | Lire l’email du gagnant et le bon numérique ; provoquer puis reprendre un échec d’envoi contrôlé. | Préparation technique |
| RM-12-04 | Retirer les droits du commerce numérique après publication mais avant tirage ; tenter la confirmation. | Navigateur |
| RM-12-05 | Tenter de remplacer un injoignable avant 14 jours sans refus ; enregistrer un refus explicite sur un autre gain ; remplacer après délai sur le premier. | Préparation technique |
| RM-12-06 | Remplacer un gagnant numérique non servi ; tester son ancien QR et ouvrir le nouveau bon du suppléant ; refaire avec un lot déjà consommé. | Navigateur |
| RM-12-07 | Épuiser la réserve puis demander explicitement un nouveau tirage de remplacement, avec puis sans candidat éligible non gagnant. | Navigateur |
| RM-13-01 | Scanner puis confirmer une remise avec le responsable ; répéter sur un autre bon avec le salarié. | Navigateur |
| RM-13-02 | Depuis le téléphone du gagnant, lancer la validation PIN et faire saisir le PIN par le commerce. | Part humaine |
| RM-13-03 | Rescanner/représenter un bon consommé puis consulter son historique. | Navigateur |
| RM-13-04 | Tester les variantes : autre commerce, bon expiré, révoqué, ancien QR, référence sans attribution et PIN bloqué. | Préparation technique |
| RM-13-05 | **Accompagné :** confirmer presque simultanément QR et PIN sur le même bon ; simuler une réponse réseau perdue après prise en compte puis rouvrir. | Préparation technique |
| RM-14-01 | Renvoyer un bon puis remplacer son QR ; comparer bénéficiaire, lot, échéance et tester l’ancien QR. | Navigateur |
| RM-14-02 | Prolonger avec motif un bon non consommé, même expiré ; tenter une échéance au-delà de 365 jours depuis attribution initiale. | Préparation technique |
| RM-14-03 | Révoquer avec motif un bon non consommé ; tester ensuite QR/PIN et consultation de l’historique. | Navigateur |
| RM-14-04 | Annuler avec motif une consommation enregistrée par erreur ; répéter sur un bon désormais expiré ou révoqué. | Préparation technique |
| RM-14-05 | **Accompagné :** lancer remise et révocation/remplacement en concurrence ; refaire sans permission de correction. | Navigateur |
| RM-15-01 | Publier une chasse avec droit actif puis une tombola/passeport ; tenter sans module et avec dernier crédit déjà consommé. | Part humaine |
| RM-15-02 | Déposer une demande complète de préparation puis consulter échéance et état. | Navigateur |
| RM-15-03 | Demander un complément côté Localeo, répondre côté client puis marquer prêt. | Navigateur |
| RM-15-04 | Ouvrir un dossier dépassant son délai, relancer puis faire communiquer une estimation révisée. | Préparation technique |
| RM-15-05 | Tenter de publier une chasse non prête ou non validée sur le terrain ; terminer les validations puis publier ; **accompagné**, deux publications sur le dernier crédit. | Part humaine |
| RM-15-06 | **Accompagné :** rendre le service de préparation technique E55 non prêt ; tenter l'achat du module ; examiner aussi une commande déjà confirmée avant l'indisponibilité. | Cible réservée |
| RM-16-01 | Télécharger le modèle ; charger CSV puis XLSX ; choisir une feuille et associer les colonnes avant aperçu. | Navigateur |
| RM-16-02 | Tester 100 puis 101 lignes ; fichier de 2 000 000 octets puis plus grand ; lignes invalides et formule dans un champ importable. | Navigateur |
| RM-16-03 | Charger email unique connu, email partagé, même email/SIRET différent, autre email/SIRET connu et deux lignes visant la même fiche. | Navigateur |
| RM-16-04 | Confirmer uniquement les lignes valides d’un fichier mixte ; télécharger le rapport ; tenter sans module ou permission. | Navigateur |
| RM-16-05 | Importer V1, modifier localement le téléphone ; dans V2 modifier ce téléphone différemment, changer un site non retouché localement, laisser une cellule vide et conserver un autre champ inchangé. | Navigateur |
| RM-16-06 | Après aperçu, faire modifier une fiche par un autre opérateur, puis confirmer ; changer email de contact, SIRET et commune dans des variantes distinctes. | Navigateur |
| RM-16-07 | **Accompagné :** interrompre après une ligne réussie, reprendre ; expirer le module avant démarrage puis pendant un autre import déjà commencé. | Préparation technique |
| RM-16-08 | **Accompagné :** consulter un import terminé/abandonné depuis plus de 30 jours, puis ses fiches et un réimport. | Préparation technique |
| RM-17-01 | Préparer un message pour chacune des audiences : tous, parcours non terminé, parcours terminé, gagnants ; essayer avant publication et après clôture +30 jours. | Préparation technique |
| RM-17-02 | Envoyer immédiatement aux comptes autorisant les messages, l’un avec Push et l’autre sans ; vérifier l'exclusion d'un participant opposé, d'un participant sans accord explicite et d'un simple abonné à la commune sans participation, même s'ils acceptent le Push ou les notifications automatiques. | Navigateur |
| RM-17-03 | Programmer en heure de Paris ; changer une préférence ou retirer la permission du gestionnaire avant démarrage. | Navigateur |
| RM-17-04 | Préparer/annuler des brouillons puis démarrer des campagnes jusqu’au quota, reprendre une campagne déjà commencée. | Navigateur |
| RM-17-05 | **Accompagné :** activer en fin de mois, passer le premier du mois Paris et une borne de changement d’heure ; comparer essai et achat. | Préparation technique |
| RM-17-06 | Laisser une programmation arriver avec quota épuisé ou droit expiré ; rétablir le droit/quota. | Préparation technique |
| RM-17-07 | Cibler la même personne dans deux campagnes/animations de A1 sur 24 h, avec plusieurs appareils ; attendre/préparer la fin de fenêtre. | Préparation technique |
| RM-17-08 | Cibler cette personne avec une troisième campagne distincte ; rejouer une reprise puis répéter sur plusieurs participants ; ajuster limite/multiplicateur côté ERP habilité. | Préparation technique |
| RM-17-09 | **Accompagné :** interrompre une campagne partiellement commencée, expirer le module puis reprendre, avec consentement retiré d’un destinataire restant. | Préparation technique |
| RM-17-10 | Préparer une campagne dont tous les destinataires sont exclus par préférence ou fréquence, puis lancer son traitement. | Navigateur |
| RM-17-11 | **Accompagné :** avec un seul crédit disponible, lancer deux campagnes ayant chacune un destinataire autorisé distinct. | Navigateur |
| RM-18-01 | Découvrir une animation, sa fiche, les commerçants et les modalités ; s’inscrire puis participer. | Navigateur |
| RM-18-02 | Ouvrir la fiche d’un commerce Animation seul et ses animations liées. | Navigateur |
| RM-18-03 | Ouvrir anciens QR/emails/carnets puis accéder au nouveau site ; suivre la reprise explicite si proposée. | Navigateur |
| RM-18-04 | Refuser la réactivation des notifications sur la nouvelle origine, puis participer et lire la messagerie ; refaire en acceptant. | Navigateur |
| RM-19-01 | Consulter l’aide puis créer une demande liée à une animation ; répondre côté Support puis client. | Navigateur |
| RM-19-02 | Comparer accusé automatique, cible de 2 jours ouvrés et première réponse humaine. | Préparation technique + Part humaine |
| RM-19-03 | Consulter avec A une demande de B et chercher les notes internes depuis le compte client. | Navigateur |
| RM-20-01 | Choisir les sections à réutiliser et de nouvelles dates ; créer l’édition dans A1 puis tenter A2. | Navigateur |
| RM-20-02 | Examiner participants, gains, QR, paiements, accords et consentements du brouillon ; tenter sa publication. | Navigateur |
| RM-20-03 | **Accompagné :** modifier la source après ouverture du formulaire ou reprendre une création après réponse perdue. | Préparation technique |
| RM-21-01 | Fixer les objectifs puis publier ; tenter de changer les objectifs ; comparer résultats et édition comparable. | Navigateur |
| RM-21-02 | Inscrire via les deux sources et sans source ; contrôler le bilan. | Navigateur |
| RM-21-03 | Vérifier les totaux avant/après remise, rescan, correction et remplacement à partir des références du jeu. | Navigateur |
| RM-21-04 | Après clôture, répondre dans Live avec note 1 puis 5 et commentaire facultatif ; tester 0/6, absence de réponse et accès avant clôture. | Navigateur |
| RM-22-01 | Retrouver chaque gain dans ERP/Support, filtrer par nature/commune, paginer et exporter la page affichée. | Navigateur |
| RM-22-02 | Vérifier les sommes financières des trois dotations ; tenter de sélectionner le commerce Animation seul comme fournisseur de prestation Coffrets dans Atelier. | Navigateur |
| RM-22-03 | Ouvrir une projection commerciale/CRM disponible et ses liens vers les parcours métier. | Navigateur |
| RM-23-01 | Consulter coûts par organisation puis commune/souscription/module selon données ; comparer au compte client. | Navigateur |
| RM-23-02 | **Accompagné :** faire passer le coût suivi de 79 à 80 puis 100 € ; rejouer les événements ; consulter l’organisation sans budget. | Préparation technique |
| RM-23-03 | Après dépassement, consulter abonnement, quotas et parcours de l’organisateur. | Navigateur |
| RM-24-01 | Demander un export avec collaborateur puis responsable ; suivre sa préparation et sa disponibilité. | Navigateur |
| RM-24-02 | Télécharger l’archive connecté ; ouvrir CSV, médias et guide ; comparer des références connues et les engagements en cours. | Navigateur |
| RM-24-03 | **Accompagné :** interrompre/reprendre la génération, tenter téléchargement sans rôle puis après 30 jours de disponibilité ; consulter les données sources. | Préparation technique |
| RM-24-04 | Demander séparément la fermeture comme responsable avec engagements ouverts ; tenter nouvel usage et fin des engagements existants. | Navigateur |
| RM-24-05 | Résoudre les engagements ou effectuer une reprise explicitement supportée et acceptée ; faire confirmer la fermeture par Localeo. | Part humaine |
| RM-25-01 | Examiner les commerces existants, saisir manuellement leurs périmètres puis tenter la bascule avec un commerce non revu ; terminer la revue. | Part humaine |
| RM-25-02 | **Accompagné :** pendant la vérification de bascule, créer/déplacer un commerce puis relire l’éligibilité. | Navigateur |
| RM-25-03 | **Accompagné :** générer un jeu synthétique puis le sauvegarder/restaurer sur cible isolée ; reprendre des parcours QR/PIN, import et permissions. | Cible réservée |
| RM-25-04 | Faire examiner le manifeste, les résultats des recettes et les anomalies ; faire valider l’UX par Localeo puis Martignas-sur-Jalle. | Part humaine |
| RM-25-05 | **Accompagné technique, sur cible isolée représentative :** restaurer base/fichiers/configuration et reprendre accès, participation, validation et remise ; chronométrer jusqu’aux contrôles terminés. | Cible réservée |
| RM-25-06 | Examiner un dossier sans preuve de restauration ou dont un objectif échoue. | Part humaine |
| RM-X-01 | Sur téléphone étroit puis ordinateur, parcourir les fonctions autorisées du portail ; côté interne, vérifier menus et retour accueil ERP ; côté public, découverte et participation. | Part humaine |
| RM-X-02 | Tester clavier seul, focus, zoom 200 %, erreurs de formulaire et états des lots sans s’appuyer uniquement sur leur couleur. | Part humaine |
| RM-X-03 | Depuis un appareil configuré hors France, lire échéances de bons, campagnes, factures et délais de service ; inclure un changement d’heure. | Préparation technique |
| RM-X-04 | Dans chaque action à effet, recharger après confirmation ; sur les jeux accompagnés, couper la réponse puis relire l’état ; ouvrir l’historique. | Préparation technique |
| RM-X-05 | Avec un lecteur puis un compte A, ouvrir un lien mémorisé vers écriture ou objet B ; retirer un droit pendant une session. | Navigateur |
| RM-X-06 | **Accompagné :** jeu de 10 communes et 10 000 participants au total ; 10 utilisateurs actifs simultanés. Paginer, filtrer, changer de commune, consulter bilan et poursuivre validation pendant import/campagne. Comparer au jeu réduit, mêmes actions. | Cible réservée |

## Ordre de réalisation

1. Socle, manifeste du jeu, précontrôles et rapport ; F01/F02 (comptes/invitations) pour éprouver les identités, emails et changements de session.
2. F03–F08 : périmètres, onboarding et droits commerciaux.
3. F09–F14 : trois dotations, tirage, remise QR/PIN et incidents.
4. F15–F17 : chasse, import/deltas et communication.
5. F18–F24 : parcours public, support, nouvelle édition, bilans, coûts, export et fermeture.
6. F25 et contrôles transverses : validations humaines, exercice réservé, charge et consolidation.

Chaque étape complète sa couverture et ses preuves avant d’étendre la campagne. Aucun commit, push, déploiement ou migration n’est déclenché par la préparation de cette automatisation.


Complément du 23 octobre 2026 : **RM-11-04 et RM-18-01 réussissent intégralement sur le clone isolé**. L’index privé `duree-decouverte-clone-preuves-completes.json` vérifie les empreintes de la durée (neuf contrôles navigateur, même animation publiée et tirée, échéance à attribution +90 jours) et de la découverte publique (six étapes, inscription unique et action personnelle autorisée). Les deux identifiants sont barrés dans la recette ; les erreurs antérieures du harnais restent conservées dans les rapports.


**RM-23-02 réussit intégralement sur le clone isolé** : `rm2302-clone-preuves-completes.json` associe budget100€, mesures estimées79/80/100€, absence/passage des seuils, une alerte logique, notifications dans l’outbox de test, huit commandes réellement rejouées et absence de double mesure/révision/alerte. ERP, Ops et organisation sans budget sont contrôlés au navigateur. Les lectures commerciales après101€ restent identiques hors identifiants de requête ; RM-23-03 reste partiel faute de parcours client complet et de lectures Finance/crédit activées dans ce clone.


**RM-11-01 et RM-22-03 réussissent intégralement sur le clone isolé**. Les index privés `parcours-libre-clone-index-completude.json` et `rm2203-clone-preuves-completes.json` vérifient respectivement la génération/reprise des trois exemplaires et la consultation commerciale sans vente, paiement, activation ou extension de périmètre. Les neuf nouveaux identifiants complets du clone s’ajoutent aux douze historiques TEST ; ils ne qualifient pas un déploiement commun.


**RM-18-02 réussit intégralement sur le clone isolé** : fiche publique d’un commerce réellement Animation seul dans une nouvelle commune fictive, animation liée et retour, aucune qualité Coffrets induite. L’index privé `public-discovery-clone-rm18-02-completude-scellee.json` contrôle sept empreintes et cinq étapes. Les contrôles Pro complémentaires sont conservés sans en déduire la validation de tous les profils F04/F05.


**RM-11-05 réussit intégralement sur le clone isolé** : trois exemplaires/deux éligibles, surplus jamais attribué libéré par confirmation, bon non consommé révoqué au formulaire, exemplaire attribué non libérable et historique conservé. Les preuves et la réserve sur une ancienne remise corrigée sont explicites dans `parcours-libre-clone-index-completude.json`. La navigation responsive apporte aussi dix-huit contrôles à360/1280pixels dans Animation, ERP et la surface publique (`navigation-ui-clone-rapport.json`), sans prétendre à un essai sur téléphone physique.


**RM-23-03 réussit désormais intégralement sur le clone isolé** après préparation des capacités de lecture Finance réellement activées sur TEST. L’index `rm2303-clone-preuves-completes.json` conserve les relevés immuables avant/après : responsable A1, budget200€/estimation201€, alerte interne ; abonnement, quotas, crédit, demandes/factures et droits du parcours organisateur inchangés par API et navigateur. Cette preuve remplace la qualification partielle du complément économique précédent ; aucune dépense fournisseur ni commande commerciale.


Vérification du24octobre : **RM-11-02/03 et RM-12-01/02/06 réussissent intégralement sur le clone isolé**. `cas-complets-libre-clone-index-20261024.json` fige les étapes et empreintes des cinq cas : collision sans double affectation, descriptions historiques après correctif UI, huit variantes de tirage, reprise sans nouveau résultat et remplacement avec ancien bon révoqué. Les premières erreurs du harnais et les limites transport/optique sont conservées ; ces cinq validations ne qualifient pas un déploiement partagé.


Passage des principaux du 24 octobre : les remises réelles dans Pro par responsable et salarié (QR saisi manuellement), puis dans Live par PIN, ont leurs reçus et historiques vérifiés. RM-13-01/02 restent partiels pour leurs exigences optiques/humaines ; **RM-13-03 est intégralement vérifié sur le clone**, avec reçu initial et audits sans double consommation ni notification. Index privé `rm1303-clone-preuves-completes.json`.


Le parcours principal de révocation **RM-14-03 est entièrement vérifié sur le clone** : formulaire motivé, refus du QR et de la demande PIN antérieure, relecture fraîche sans action, historique et unité non libérée. Index privé `rm1403-clone-preuves-completes.json`. Renvoi/rotation et correction du seul bon encore valide restent des principaux partiels de RM-14-01/04, sans réception fournisseur ni variantes temporelles revendiquées.
