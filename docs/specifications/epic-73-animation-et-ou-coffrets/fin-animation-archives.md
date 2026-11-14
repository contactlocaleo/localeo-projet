# Fin d’animation et archives — E73-EVO-FIN-ARCHIVES

Complément du **12 novembre 2026 — E73-EVO-CLOTURE-AUTO** : voir la
[spécification de clôture automatique et report de fin](#évolution-du-12-novembre-2026--clôture-automatique-et-report-de-fin).
Cette extension est spécifiée, avec trois choix utilisateur confirmés ; elle n’est pas implémentée.

Évolution du 11 novembre 2026. E73 conserve sa clôture historique ; les critères
ci-dessous portent le nouveau comportement demandé et ses preuves propres.
La demande remplace les étapes terminales de présentation « Tirage terminé »,
« Bilan disponible », « Archivée » par une fin explicite, puis un archivage.

## Décisions et parcours

- **Clôturer** ferme inscriptions et validations, fige la population et permet
  le traitement des tirages et des lots. Ce comportement reste conservé.
- **Terminer l’animation** est une commande explicite : chaque lot attribué est
  remis ou son dossier est explicitement clôturé ; les unités sans gagnant sont
  justifiées. Elle passe `CLOTUREE → TERMINEE`, fige la gestion, sous réserve
  du retrait exceptionnel d'un lot externe décrit ci-dessous, et donne accès
  au bilan. Une animation terminée reste visible dans Live pour
  les personnes inscrites jusqu’à son archivage.
- **Archiver l’animation** passe `TERMINEE → ARCHIVEE`. L’animation disparaît des
  vues de découverte et de Mon carnet. Elle reste consultable, avec son bilan,
  depuis **Animations → Mes archives** dans Localeo Animation. Aucun accès,
  gain acquis, justificatif ni historique n’est supprimé par cet archivage.

Le **Tableau de bord** exclut systématiquement les animations `ARCHIVEE` :
liste d’actions, alertes liées à une animation, indicateurs, séries et classement
des commerces. Aucun filtre n’y propose les archives ; une requête directe
filtrée sur une archive ne les réintroduit pas. Les alertes générales restent
visibles et les alertes d’animation suivent le périmètre des filtres du tableau.
Les animations `TERMINEE` restent présentes jusqu’à leur archivage explicite.
Cette projection opérationnelle ne modifie pas les bilans ni le profil historique
« Votre activité dans la commune », qui conservent l’activité des archives.

L’animation ne se termine ni sur une date, ni sur l’envoi des e-mails, ni sur la
seule confirmation du tirage. Les actions disponibles viennent du backend.
Les opérations de tirage et de remise restent visibles dans leur suivi dédié ;
elles ne sont plus des étapes terminales concurrentes de la timeline du cycle.
Le cycle présente Préparation, Publication, Déroulement, Clôture, Terminée,
Archivée. Une animation `CLOTUREE` reste à l’étape Clôture jusqu’à sa fin explicite.

## Résolution des lots

Le domaine possède la politique de fin et de résolution des dossiers. Les
interfaces présentent ses faits et ses refus ; les routes ne recalculent pas
une seconde éligibilité à la fin.

| Nature | Preuve de traitement | Refus significatif |
| --- | --- | --- |
| Lot externe | Remise déclarée encore effective, ou décision explicite de clôture motivée (refus, abandon, autre motif documenté) | Contact, email envoyé ou simple refus enregistré sans décision de clôture ne suffisent pas |
| Bon numérique | Consommation effective, ou clôture motivée avec révocation du bon par la commande existante dans la même transaction | Expiration seule, email envoyé, révocation sans décision de dossier ne suffisent pas |
| Coffret | Remise/réception explicitement attestée, ou dossier explicitement clôturé avec motif | `ENVOYE` et instance créée ne valent pas attestation de remise |
| Lot sans gagnant | Justification explicite couvrant le nombre exact d’unités publiées non attribuées, à leur version courante | Une absence de ligne sur une page ne prouve pas l’absence de gain |

Les décisions sont datées et attribuées à l’acteur habilité, avec identité du
gain et de l’animation, nature, version et motif. Les gains remplacés restent
historiques ; seule leur attribution courante doit être résolue. Un tirage
initial ou supplémentaire non confirmé bloque la fin. La justification des
unités sans gagnant est agrégée et bornée : aucune matérialisation de milliards
d’unités ni chargement de toutes les lignes en mémoire.

La clôture d’un dossier numérique annonce clairement sa révocation avant la
confirmation ; elle réutilise la règle et l’autorisation de révocation existantes.
La fin ne révoque aucun droit implicitement. La consommation d’un coffret acquis
dans le domaine Coffrets reste indépendante de la gestion de son animation.

La décision explicite de clôturer un dossier arrête, dans la même transaction,
ses intentions d'e-mail de gain encore à préparer ou en échec de préparation.
Les e-mails déjà déposés ne sont ni effacés ni retirés. Le motif du dossier
conserve la décision ; **Terminer** n'annule aucune intention silencieusement.

### Correctif du 14 novembre 2026 — retrait d'un lot externe après clôture du dossier

Précision utilisateur : un gagnant peut venir retirer son **lot externe** après
la clôture explicite de son dossier, même si l'animation a ensuite été terminée
ou archivée. Dans **Résultats → Fin et archivage**, y compris depuis
**Animations → Mes archives**, **Forcer le retrait du lot** permet au
gestionnaire habilité à modifier l'animation de constater cette remise réelle.
L'action ne concerne que l'attribution courante, issue d'un tirage confirmé,
dont le dossier est `CLOTURE`, à l'état `CLOTUREE`, `TERMINEE` ou `ARCHIVEE`.
Elle n'est proposée ni sur un dossier non clôturé ou déjà remis, ni pour un
ancien gagnant remplacé, un bon numérique, un coffret ou des lots sans gagnant.

La confirmation identifie le lot et le bénéficiaire, exige un motif de cinq
à 2 000 caractères et l'attestation de la remise effective. La décision
`FORCER_RETRAIT` enregistre un événement réel `REMISE_DECLAREE`, daté du serveur
et attribué à l'acteur courant, puis une preuve de décision à la nouvelle
version du dossier. L'attribution, le suivi et la version Animation sont
enregistrés dans la même transaction, sous les verrous existants. Un refus
antérieur reste dans l'historique ; le constat de remise n'efface aucun fait.

Le dossier et Mes lots deviennent **Remis**, et le bilan compte cette remise.
L'animation garde son état terminal et ses dates ; aucun jeu, tirage, accès
QR/PIN ou bon révoqué n'est rouvert. Aucun nouvel e-mail n'est préparé. La
clôture précédente reste conservée, ainsi que son motif. Même clé : même reçu,
sans second événement ; version périmée ou nouvelle demande après remise :
refus sans écriture partielle. Les autres commandes de gestion restent gelées.
Aucune migration ni réparation automatique des anciens dossiers n'est requise.
Les versions, preuves et limites figurent dans le
[registre d'anomalies Animation](../../roadmap/anomalies/animation.md#correctif-du-14-novembre-2026--retirer-un-lot-externe-après-clôture-du-dossier).

## Lecture seule, accès et concurrence

Après `TERMINEE` ou `ARCHIVEE`, les commandes de gestion de cette animation
échouent côté serveur : configuration, dotation, tirage/remplacement, suivi et
correction de remise, gestion des bons, messages/actualités, supports et autres
modifications d’exploitation. Les lectures, reçus idempotents et bilan restent
accessibles avec leurs contrôles habituels. La commande distincte d’archivage
reste permise depuis `TERMINEE`. Créer une nouvelle édition produit une nouvelle
animation ; cela ne modifie pas celle qui est figée.

Seule la décision versionnée `FORCER_RETRAIT` décrite ci-dessus fait exception
pour un lot externe explicitement clôturé. Elle ne rend pas disponibles les
commandes ordinaires de suivi ou de correction d'une remise après archivage.

L'exception existante de retrait des coordonnées du contact public est
conservée pour `TERMINEE` et `ARCHIVEE` : dépublication ou effacement seulement,
sans ajout ni remplacement de coordonnées. Les obligations de conservation et
d'effacement conservent leurs parcours et habilitations propres.
Le questionnaire volontaire d'un participant reste disponible après la clôture,
y compris à l'état `TERMINEE`, avec ses accès et versions ; il ne réouvre
aucune action de jeu ou de gestion. L'avis conservé continue d'alimenter le bilan.

Une programmation de communication encore à publier ou une opération asynchrone
de gestion non terminée est un blocage explicite à résoudre avant la fin.
Ni nouvelle publication tardive ni annulation silencieuse ne sont induites par
**Terminer**. Les workers relisent la garde terminale avant toute nouvelle
écriture de gestion et conservent les protections d'idempotence.

Le transport technique d'un message déjà durablement publié avant la fin reste
un effet acquis : Push, courrier et leurs traces peuvent se terminer avec les
contrôles habituels de préférences et d'accès. Un appareil indisponible ne
bloque pas la fin de l'animation. Cela ne permet ni nouveau message ni
modification de l'animation. Les envois de gains qui créent encore un droit
Coffret appartiennent au traitement des lots, à résoudre avant la fin.

Terminer, clôturer un dossier et archiver utilisent version attendue,
confirmation, clé d’idempotence et audit. Une fin concurrente à une remise,
correction, attribution ou publication est sérialisée par la coordination et
le verrou Animation existants ; la garde est relue après acquisition. Les
rejeux retournent le reçu acquis sans nouvel effet. Un refus ne produit ni
changement partiel de statut ni révocation partielle.

## Contrats et données

Le producteur est `ServiceFinAnimation` ; ses contrats Pydantic sont dans
`app/application/animation_locale/contrats_moteur/fin_animation.py`. Les chemins
suivants sont sous `/protected/animation-locale` :

| Méthode et chemin | Entrée et résultat |
| --- | --- |
| `GET /animations/{id}/etat-fin` | `limit` de 1 à 100, défaut 25, et `cursor` opaque lié à l’animation ; retourne l’état, la version Animation, les compteurs exacts, les blocages, les actions autorisées et une page de dossiers |
| `POST /animations/{id}/dossiers-fin/{ref}/decision` | `expected_version`, `version_dossier` opaque, `decision`, `motif` de 5 à 2 000 caractères, `confirmation: true` ; `nombre_unites` exact obligatoire pour la justification agrégée |
| `POST /animations/{id}/terminer` | `expected_version` et `confirmation: true` ; refuse tout dossier non résolu, dotation publiée indisponible, unité non justifiée ou opération de gestion non terminée |
| `POST /animations/{id}/archiver` | `expected_version` et `confirmation: true` ; exige `TERMINEE` |
| `GET /animations/{id}/commandes-fin/{cle}` | Reçu acquis : `200 CONFIRMEE`, `202 EN_COURS` ou `404 COMMANDE_NON_ENREGISTREE` ; aucune nouvelle écriture ni répétition implicite de commande |
| `GET /animations?archives=false` ou `archives=true` | La pagination `page` / `page_size` existante reste conservée ; défaut hors archives, `true` ne retourne que les `ARCHIVEE` |

La lecture de fin retourne `animation_id`, `statut`, `version`, `compteurs`
(`dossiers_non_resolus`, `nombre_unites_sans_gagnant`, `operations_en_cours`),
`blocages` (`code`, `libelle`, `nombre`), `actions_disponibles`, `items`,
`next_cursor` et `has_more`. Chaque dossier possède `ref`, `nature`, `libelle`,
`beneficiaire`, `quantite`, `statut_resolution`, `version_dossier`, ses actions et
la dernière décision applicable à cette version. Les références et versions ne
sont pas reconstruites par l’interface. Le bénéficiaire est une présentation
nom/prénom privée ; aucun e-mail, QR, PIN ou lien personnel n’est ajouté.

Les décisions sont `ATTESTER_REMISE`, `CLOTURER_DOSSIER`,
`JUSTIFIER_NON_ATTRIBUES` et `FORCER_RETRAIT`. Les capacités sont produites après vérification des
droits, dont `animation:tirer` pour une clôture de bon numérique. L’attestation
Coffret exige une instance effectivement créée et un gain `ENVOYE` ; ce fait ne
remplace pas l’attestation. Le total Coffrets vient des quantités de la
configuration publiée, le total Libre du compteur de sa dotation publiée. Les
unités non attribuées restent un seul dossier agrégé, sans matérialisation par
unité, même pour des totaux supérieurs à deux milliards.

Les trois commandes et la décision portent `Idempotency-Key`, partagent le
registre idempotent existant sous `FIN_ANIMATION:{id}` et retournent
`animation_id`, `statut`, `version`, `operation`, et éventuellement `dossier_ref`.
La même intention rejoue son reçu acquis. Une autre intention doit conserver sa
propre clé ; un conflit ou une version périmée n’est pas rejoué automatiquement.
Chaque décision augmente aussi la version Animation. La coordination exclusive,
puis le verrou Animation, précèdent les faits de résolution et la nouvelle
vérification des habilitations. La révocation numérique et la décision sont
atomiques. Une clôture explicite annule uniquement sa préparation d’e-mail non
encore déposée (`ANNULE_DOSSIER`) ; aucun message déjà déposé n’est retiré.
L’ancienne commande d’archivage en lot sans version/confirmation est refusée avec
`COMMANDE_ARCHIVAGE_VERSIONNEE_REQUISE`.

La migration additive `v309_fin_animation_archives.sql` crée les registres
`animation_decisions_fin_dossier` et `animation_transitions_fin`, avec identité
d’acteur, date, version et unicités ; elle ne convertit aucune ancienne
`CLOTUREE`. Les FK `RESTRICT` protègent les preuves contre une suppression
d’animation. Les décisions sont conservées dans leur historique et ne valent
résolution que pour la version courante du dossier. Les exports d’organisation
ajoutent deux projections explicites et ordonnées, sans JSON métier brut ni
accès personnel. Le registre de démonstration inclut les deux tables pour les
captures et restaurations. Les politiques existantes de conservation des
identités restent distinctes ; l’archivage ne purge aucun de ces registres.

## Critères et preuves

| Critère | Acceptation observable | Preuve à produire |
| --- | --- | --- |
| FA-01 | Clôturer conserve la population figée et permet encore de traiter les lots | Régressions domaine/application de clôture et tirage |
| FA-02 | Un seul dossier non résolu, un tirage en attente ou des unités non justifiées bloquent Terminer | Domaine pur, orchestration et API pour chaque nature, zéro lot et remplacements |
| FA-03 | Attestation et clôture sont explicites, motivées, auditées et refusées hors droits/tenant/version | Tests HTTP/PG, rollback clôture/révocation et rejeu |
| FA-04 | Fin confirmée : statut TERMINEE, bilan lisible et mutations refusées sur API, ERP et workers, sauf constat versionné du retrait réel d'un lot externe explicitement clôturé | Matrice des entrées, concurrence PostgreSQL et garde de domaine ; exception du 14 novembre, idempotence et refus des autres natures |
| FA-05 | Archiver exige TERMINEE, retire l’animation de Live et conserve les lots/droits acquis | Contrats catalogue/tableau privé, Mes lots et régressions Coffrets/Pro |
| FA-06 | Mes archives ouvre une liste paginée et les fiches/bilans en lecture seule ; les archives sont exclues du Tableau de bord et de tous ses agrégats/alertes, même avec un filtre direct | Recette Animation PC/mobile, erreurs, liens directs et clavier ; tests de projection dashboard |
| FA-07 | Timeline à six étapes, prochaine action concrète et compteurs de blocage visibles | Contrat workflow et recette de chaque état, sans progression inventée |
| FA-08 | Fin/reprise/archivage sont idempotents, sans double effet et sûrs en concurrence | PG jetable : remise, correction, remplacement et workers face à la fin |
| FA-09 | Démonstration, conservation/export/restauration et documentation utilisent le nouveau modèle | Tests générateur et lecteurs ; aucune génération sur environnement réel |

Périmètres : backend/API/ERP/batchs ; Localeo Animation ; Live et Pro pour les
statuts, les refus et la préservation des droits. Les règles financières et
l’utilisation des coffrets autonomes restent dans leur domaine propriétaire.
Aucun déploiement ni réparation de données n’est autorisé par cette spécification.

## Évolution du 12 novembre 2026 — clôture automatique et report de fin

**E73-EVO-CLOTURE-AUTO** complète les critères FA sans les renuméroter. La demande
porte sur le cadrage et la spécification. Aucun code, migration ou déclenchement
d’envoi n’est livré au titre de cette section. La clôture historique E73 reste
inchangée. La cible est commune à toutes les animations possédant une période
publiée et une participation ; les achats de coffrets autonomes sont hors périmètre.

### Besoin, existant et décisions confirmées

L’organisateur doit pouvoir laisser l’animation se clôturer à son échéance,
recevoir un rapport par e-mail et conserver les notifications de clôture des
participants. Un changement de date de fin doit informer les participants dans
Live et, selon leurs réglages, par WebPush. Une clôture automatique ne déclenche
ni tirage, ni attribution, ni fin `TERMINEE`, ni archivage.

État observé dans le backend `25224e0`, Animation `89579eb` et Marketplace
`f77f4a2`, le 12 novembre 2026 ; exploration du code seulement :

| Sujet | Comportement actuel vérifié | Écart à traiter |
| --- | --- | --- |
| Date atteinte | Le domaine refuse jeu/scans à `now >= fin_effective` ; `animations.synchroniser_statuts` démarre seulement les animations publiées | Un statut retardé ne rouvre pas le jeu ; ajouter le traitement de clôture |
| Clôture | `ServiceExploitationAnimation.cloturer` coordonne autorisation, versions, gel, audit et reçu ; `ServiceTiragesAnimation.cloturer` produit les notifications | Réutiliser ce noyau métier ; le helper `cloturer_echues`, sans appelant, charge tout et ne recontrôle pas la fin sous verrou : ne pas le brancher tel quel |
| Date modifiée | `ServiceParametresExploitation` applique une décision append-only aux paramètres effectifs, conserve le DSL et prolonge les accès ; notifications organisateur/commerces | Ajouter l’intention de notification participante à cette transaction |
| Notifications Live | `creer_cloture_dans_uow` : catégorie `ANIMATION`, une notification par installation suivant une participation, clé `ANIMATION_CLOTURE:{animation_id}` | Conserver l’audience fonctionnelle et la déduplication ; borner sa préparation et revalider les préférences avant transport |
| Rapport organisateur | Mesures agrégées et bilan PDF disponibles, mais aucun e-mail de clôture préparé | Créer un rapport intermédiaire daté, distinct du bilan final |

Les règles de modification de période restent celles du
[moteur, T6-QA02 et T6-E06](../moteur-animation/conception-technique.md#précisions-t6--exploitation-et-vérification).
Les trois arbitrages suivants ont été **confirmés par l’utilisateur le
12 novembre 2026**. Les précisions techniques en découlent sans ajouter de
réouverture après échéance au comportement du moteur.

| Décision | Choix confirmé et déclinaison | Impact |
| --- | --- | --- |
| A1 — Activation | Option par animation, activée par défaut pour les nouvelles ; migration des anciennes avec option désactivée, sans clôture rétroactive silencieuse | Valeur de création, migration des réglages et présentation de l’option |
| A2 — Report | Report avant clôture uniquement, sans réouverture ; la garde existante exige aussi une fin effective non atteinte et aucune population figée | Aucune remise en jeu d’une animation échue même si le batch a pris du retard |
| A3 — Rapport organisateur | Responsables actifs de l’organisation ; application des contrôles d’accès à l’animation | Tous les destinataires autorisés, gestion explicite de zéro responsable |

La conception ci-dessous applique ces décisions. La migration n’envoie aucun
message aux animations historiques. L’implémentation n’est pas demandée dans
cette phase ; sa préparation est vérifiée séparément des preuves d’exécution.

### Parcours de l’organisateur

**Prévoir la clôture.** Dans **Piloter → Publication et clôture**, présenter près
de la date de fin « Clôturer automatiquement à la date de fin », puis l’instant
effectif : « Clôture prévue le 18 novembre 2026 à 18 h (heure de Paris) ».
L’option est modifiable avant l’échéance avec
`animation:cloturer`, confirmation, version et audit. Elle ne change pas la fin
de jeu. À échéance passée, refuser son activation tardive et proposer la clôture
manuelle existante ; les retards d’une option déjà active sont rattrapés.
Avant publication, le réglage peut être préparé mais aucune clôture n’est due.

La prochaine action vient du serveur : « Clôture automatique prévue »,
« Clôture automatique en attente » après échéance, puis la prochaine action
réelle, par exemple « Lancer le tirage ». La clôture manuelle reste possible
avec sa confirmation actuelle. Une erreur durable affiche « Clôture à vérifier »
avec référence de diagnostic ; elle ne donne pas l’impression d’un succès.

**Modifier la date.** Le lien « Modifier la date de fin » mène au formulaire
existant des paramètres publiés dans l’onglet Live ; il ne crée pas un deuxième
éditeur de calendrier. Présenter ancienne et nouvelle date, le motif interne,
les recontrôles nécessaires et la fermeture des inscriptions séparée. Avant
validation, afficher « Les participants seront informés dans Live. Une alerte
sera envoyée aux appareils qui l’autorisent. » Bouton : **« Enregistrer et
informer les participants »**. Le motif interne n’est jamais copié dans le
message public. Si la date ne change pas, aucun nouveau message n’est préparé.

Conformément à A2 et à la règle de période existante, le report reste possible tant que
`now < fin_effective`, état `PUBLIEE` ou `EN_COURS`, sans gel. Après démarrage,
le début reste immuable et la fin ne peut pas être raccourcie. Une fermeture
d’inscriptions explicite reste inchangée ; une fermeture suivant la fin suit
la nouvelle fin. La réouverture d’une fenêtre d’inscription déjà fermée exige
toujours `rouvrirInscriptions:true` : cela ne rouvre pas une animation clôturée.
Préserver accords, qualifications et validations acquises, droits, QR et
expirations recalculées selon la règle existante ; signaler les supports à rééditer.

Une date de tirage annoncée ne doit pas devenir antérieure à la nouvelle fin.
Proposition de contrôle métier additionnel : refuser avec
`DATE_TIRAGE_INCOMPATIBLE` et inviter à modifier d’abord l’annonce de tirage
par sa commande habilitée. Ni déplacement ni suppression tacite du tirage.
Ce contrôle doit aussi empêcher l’annonce concurrente d’une date incompatible.

Une réponse perdue affiche **« Vérifier l’enregistrement »**, conserve clé et
corps de commande et consulte le reçu existant. Un conflit de versions demande
la relecture ; aucune deuxième intention ni deuxième notification automatique.
À l’issue confirmée : **« Nouvelle date enregistrée. Notifications en préparation. »**
L’interface ne prétend pas que les téléphones ont reçu le message.

### Clôture, temps, concurrence et propriété métier

Le domaine Animation décide de la clôturabilité, de la période et du gel. Le
service applicatif commun orchestre ; API, ERP et batch ne recopient pas ces
règles. Les paramètres viennent de `configuration_effective_dans_uow` et la
sélection SQL de `fin_effective_sql`, jamais du seul DSL initial.

1. Sélectionner les animations `PUBLIEE` ou `EN_COURS`, option active,
   fin effective atteinte, configuration publiée valide ; un retard de démarrage
   n’empêche pas de clôturer une animation publiée déjà échue.
2. Prendre la coordination exclusive puis le verrou Animation dans l’ordre
   existant. Relire statut, option, période effective, révision, gel et heure
   serveur **après** acquisition. Une prolongation déjà acquise rend le candidat
   non échu. Une modification de brouillon ne remplace jamais la publication.
3. Exécuter le même gel de population et de provenance que la clôture manuelle,
   avec qualifications recalculées depuis les faits et effets différés existants.
   Ne pas utiliser le seul statut de participation pour décider de l’éligibilité.
4. Acquérir dans une seule UoW la transition `CLOTUREE`, le gel, l’opération unique,
   l’audit, l’événement durable, la photographie agrégée du rapport et la capture
   relationnelle des destinataires Live éligibles avec leurs préférences à cet
   instant. Les intentions de diffusion et de rapport sont acquises avec ces
   données, pas reconstituées après coup. Même atomicité décision/événement/audience
   pour le report de fin. Zéro appel réseau ou rendu de PDF sous verrou.
   Un échec annule tout.
5. Préparer puis transporter les messages hors transaction de clôture, avec
   reprise et unicité. Une panne de messagerie ne rouvre pas l’animation et
   n’autorise pas un second gel ni un deuxième tirage.

La date limite de jeu est `fin_effective` ; `closed_at` reste l’instant réel de
transition. Le rapport conserve séparément échéance, heure de traitement et retard.
L’ordonnanceur vise la première passe après échéance, sans promettre une exécution
à la seconde. Les comparaisons utilisent des instants UTC ; la saisie et la
présentation utilisent Europe/Paris, avec refus d’heures saisonnières ambiguës.

L’identité du premier événement de clôture est unique par animation, commune
et organisation validées. Clôtures manuelle et automatique concurrentes retrouvent
le même événement et la même population. Le rejeu ne recrée pas d’opération
technique inutile. La clé Live historique de clôture reste reconnue. A2 exclut
une réouverture et donc toute seconde clôture de cette même animation.

Deux ordres de course sont à prouver : prolongation acquise avant le worker →
nouvelle échéance respectée ; clôture acquise ou échéance atteinte pendant attente
du formulaire → report refusé et état courant affiché. Les commandes de jeu,
clôtures manuelles et annonces de tirage utilisent la même coordination.

### Notifications des participants

Les événements sont des **notifications système** : pas de module Communication,
quota de campagne ou consentement individuel supplémentaire par animation. Ils
réutilisent la cloche, les nouvelles de l’animation et le transport WebPush.
Le workflow de clôture manuel et automatique doit rester identique côté habitant.

| Événement | Titre et corps proposés | Identité et cible |
| --- | --- | --- |
| Clôture | **« Animation clôturée »** — « Les participations à {nom} sont closes. Retrouvez la suite dans votre carnet. » Ajouter une date de tirage uniquement si elle est réellement annoncée | Source historique `ANIMATION_CLOTURE:{id}` ; lien relatif `/live/animations/{id}` |
| Fin modifiée | **« Nouvelle date de fin »** — « {nom} : fin prévue le {ancienne date et heure}, reportée au {nouvelle date et heure}. Votre participation est conservée. » Avant démarrage, si la date est avancée, remplacer « reportée » par « fixée » | Source `ANIMATION_FIN_MODIFIEE:{id}:{revision_exploitation}` ; même cible utile |

Le titre actuel « Animation terminée » est remplacé dans les deux chemins de
clôture, car `TERMINEE` désigne une autre transition. Aucun gagnant, tirage imminent
ou réouverture d’inscriptions n’est annoncé sans fait correspondant.

Audience : installations actives suivant au moins une participation effective
à l’animation, catégorie `ANIMATION` autorisée. Pas de filtre sur la qualification,
la commune suivie ou les gains ; plusieurs participations sur le même appareil
ne produisent qu’un message. Conserver les exclusions d’accès révoqués et
d’identités anonymisées selon le contrat participant commun ; expliciter ces
garde-fous dans le service commun, car la clôture actuelle ne les vérifie pas tous.
Une nouvelle installation apparue après l’événement ne reçoit pas rétroactivement
une alerte ; les dates et l’état restent consultables dans l’animation.

L’événement borne les liens de suivi à ceux existant à sa création ; l’audience
est préparée par pages, en revalidant activité, accès et préférence. Une catégorie
désactivée au moment de l’événement exclut le dépôt, même si elle est réactivée
avant reprise : conserver une photographie relationnelle de l’audience éligible,
sans liste JSON d’identités ni hydratation globale. Revalider encore avant
transport. Un retrait de suivi ou de droit supprime l’envoi restant, avec motif.

WebPush exige en plus les alertes de l’appareil activées, un abonnement actif,
la permission système et `WEBPUSH_PUBLIC_LIVE_ENABLED`. Un Push indisponible
n’empêche ni le dépôt Live autorisé ni la clôture. Réutiliser révocation des
abonnements 404/410, TTL et reprises existants. « Accepté par le fournisseur »
ne signifie ni reçu par le téléphone ni lu. Aucun e-mail/SMS participant ajouté.

En cas de reports successifs, une décision réelle possède son propre événement.
L’historique Live garde les notifications déjà déposées, datées et formulées
comme décisions ; la fiche affiche toujours la fin effective courante. Un Push
de report non encore envoyé est abandonné avec motif `REMPLACE_PAR_REPORT` si
une révision plus récente change la fin, ou `ANIMATION_CLOTUREE` après clôture.
Une révision sans changement de fin ne le rend pas obsolète. Aucun retrait d’un
message déjà transmis n’est prétendu ; la revalidation a lieu juste avant envoi.

### Rapport e-mail de clôture à l’organisateur

Le rapport est une **photographie intermédiaire de clôture**, pas le bilan final.
La nouvelle préparation concerne la clôture automatique demandée ; le socle
commun de clôture reste réutilisable sans ajouter implicitement un nouvel e-mail
à une clôture manuelle. Un événement conserve donc son origine `MANUELLE` ou
`AUTOMATIQUE`. Le gagnant d’une course manuelle/automatique détermine cette origine.

Objet : **« {nom} : clôture automatique — rapport de participation »**.
Contenu HTML et texte selon la [charte commune](../../architecture/transverse/charte-emails-localeo.md) :
nom, commune, type, fin effective et date de clôture ; inscrits, qualifiés et
non qualifiés issus du gel et de ses compteurs ; validations/taux de parcours
uniquement si applicables et de couverture connue ; dotation synthétique et
prochaine action réelle, par exemple **« Préparer le tirage »**. Afficher les
données absentes comme indisponibles, pas comme zéro. Bouton principal
**« Ouvrir l’animation »** vers Localeo Animation, avec authentification habituelle.
Pas de liste nominative, PIN, jeton participant ni résultat de tirage inventé.
Le PDF final reste accessible par le parcours Bilan ; aucune pièce jointe nouvelle
n’est nécessaire pour cette première version proposée.

Réutiliser les agrégats de `ServiceMesuresAnimation`/`ServiceBilansExportsAnimation`,
en fixant version, `observedAt` et couverture à la clôture. Un envoi retardé ne
recalcule pas ces chiffres sur une animation où le tirage a déjà eu lieu.
La population de tirage contient seulement les éligibles, tandis que la
provenance du gel couvre tous les participants : le compteur d’inscrits ne
doit donc pas être déduit de la taille de cette population. La photographie
agrégée est un nouveau stockage à produire atomiquement ; les lectures actuelles
de bilan ne sont pas déjà une photographie figée de ce futur rapport.

Conformément à A3, résoudre tous les responsables actifs, comptes et organisation
actifs, habilités à lire cette animation ; ordre déterministe et adresse courante
non vide, de syntaxe valide, issue du compte gestionnaire. Aucune adresse saisie
librement pour ce rapport ni nouvelle exigence de vérification de boîte e-mail.
L’existence d’une preuve de propriété de l’adresse n’est pas présumée à partir
du seul statut du compte. Ne pas utiliser le helper `responsable()` avec son
`LIMIT 1` sans ordre, ni inventer un e-mail de partenaire ou un créateur personnel.
Revalider accès et adresse avant dépôt dans `EmailSortant` puis avant transport.
Le destinataire révoqué ne reçoit pas le rapport. Zéro destinataire ne bloque
pas la clôture : état **« Rapport en attente de destinataire »**, visible dans
l’animation et en exploitation, avec résolution via la gestion d’équipe existante.
Une reprise après résolution sélectionne les destinataires courants et ne renvoie
pas aux comptes ayant déjà un reçu de dépôt pour cet événement.

Un reçu unique `(evenement_cloture_id, gestionnaire_id)` lie photographie et
message sortant ; `obtenir_par_source` seul ne suffit pas. L’insertion du reçu
et de l’e-mail est atomique, la reprise réutilise le même `EmailSortant`. Une
issue fournisseur incertaine reste diagnostiquée, sans créer un nouveau courrier
automatiquement. La garantie porte sur le dépôt unique ; le transport ne promet
pas une livraison « exactement une fois » lorsque le fournisseur est incertain.

Ajouter explicitement une garde de cette source au chemin d’envoi e-mail avant
appel fournisseur et à chaque reprise : le transport actuel ne revalide pas ces
responsables. Si compte, appartenance, droit ou adresse courante ne correspondent
plus au destinataire déposé, **annuler l’envoi restant de cette enveloppe**, avec
motif (`DESTINATAIRE_REVOQUE` ou `ADRESSE_MODIFIEE`), sans nouvel e-mail automatique.
Conserver son reçu et afficher « Rapport non envoyé » avec la raison ; le rapport
reste consultable depuis l’animation avec les droits habituels. Une adresse absente
ou invalide avant tout dépôt laisse au contraire la préparation en attente : après
correction, elle peut produire son premier dépôt. Le corps et l’adresse d’un
`EmailSortant` existant ne sont pas modifiés par `mettre_a_jour` aujourd’hui ;
cette évolution n’en suppose pas la capacité. Un fournisseur déjà appelé reste
un effet externe qui ne peut pas être rappelé ; conserver son état et sa trace.

Le renvoi générique qui crée une nouvelle UUID d’e-mail est interdit pour cette
source. La supervision propose uniquement la reprise de l’événement ou du même
courrier en échec technique selon sa garde, jamais la duplication d’un dépôt
acquis, annulé ou de résultat incertain. Ces refus doivent être appliqués dans
le service commun, y compris hors de l’interface ERP.

### Contrats, stockage et frontières

Contrats **cibles à implémenter**, sous `/protected/animation-locale` pour les
routes partenaires ; les noms nouveaux ci-dessous deviennent la référence de
conception, pas la description d’endpoints déjà déployés.

| Entrée / consommateur | Contrat cible et invariants |
| --- | --- |
| `GET /animations/{id}/exploitation/cloture-automatique` — Animation/ERP | `animationId`, `statut`, `enabled`, `effectiveEndsAt` nullable sans période publiée, `version` de l’Animation, `definitionVersion` nullable avant publication, `exploitationRevision`, `state` (`DESACTIVEE`, `A_PLANIFIER`, `PREVUE`, `EN_ATTENTE`, `CLOTUREE`, `A_VERIFIER`), `actions`, `reportState`, compteurs de diffusion ; lecture `animation:lire` et tenant/commune |
| `POST /animations/{id}/exploitation/cloture-automatique` | `enabled`, `expectedVersion`, `definitionVersion`, `expectedExploitationRevision`, `confirmer:true`, `motif` ; `animation:cloturer`, `Idempotency-Key`, commande sous verrou et reçu durable ; pas de nouvelle période dans cette commande |
| `GET /animations/{id}/exploitation/cloture-automatique/commandes/{cle}` | Même convention de réconciliation que les paramètres : `200 CONFIRMEE`, `202 EN_COURS`, absent explicite ; réautorisation du lecteur |
| `POST /animations/{id}/exploitation/parametres` — déjà existant | Préserver `expectedVersion`, `definitionVersion`, `expectedExploitationRevision`, `motif`, `endsAt`, contrôles et réouverture explicite ; ajouter la préparation système seulement si fin réellement modifiée |
| Reçu paramètres et lecture d’exploitation | Ajouter un résumé `participantNotification` : événement, état de préparation, nouvelle fin ; aucun destinataire personnel ni endpoint Push dans le JSON partenaire |
| Clôture manuelle API/ERP | Commandes et confirmations existantes conservées ; même noyau/gel/événement que le batch, même workflow Live |
| Batch `animations.cloturer_echues` — nouveau | Entrée machine `internal:batch`, intégration au registre et au déclenchement manuel supervisé ; identité système distincte d’un gestionnaire ; paramètres bornés de lot, réponse avec candidats/clôturées/reportées/en erreur/à reprendre, référence du rapport |
| Batch `animations.evenements_cycle.traiter` — nouveau | Préparation bornée des intentions Live et rapports acquises par clôture ou report, `internal:batch`, reprise par événement/curseur ; aucune nouvelle transition métier ; transmission aux transports Live et e-mail existants |
| Lecture Live et transport | Enveloppe et marquage lu existants ; événement de report et lien relatif sous `/live/`, aucune URL étrangère ni token ajouté ; afficheurs et service worker acceptent les nouveaux messages |

La lecture `GET …/exploitation/cloture-automatique` expose aussi `report`,
nullable avant clôture automatique, pour afficher **le rapport figé** dans
Animation/ERP, même en cas d’e-mail annulé. Objet borné sans identité personnelle :
`eventId`, `observedAt`, `animationVersion`, `definitionVersion`, `coverage`,
`scheduledEndAt`, `closedAt`, compteurs `inscrits`, `qualifies`, `nonQualifies`,
`validations`, `completionRate` et dotation agrégée par les trois natures existantes.
Une mesure non applicable ou indisponible vaut `null`, avec couverture explicite.
Le nom/type/commune sont issus de la photographie, sans lecture publique ni
nouvelle liste de participations. La prochaine action présentée dans ce rapport
est libellée **« Étape prévue à la clôture »** ; la prochaine action courante
vient séparément de la projection d’exploitation. Cette distinction vaut aussi
dans l’e-mail envoyé tardivement. Lecture `animation:lire`, tenant et commune
revalidés, y compris en accès direct à une animation archivée.

`reportState` qualifie la préparation : `SANS_OBJET` (pas de clôture automatique),
`A_PREPARER`, `ATTENTE_DESTINATAIRE`, `EN_PREPARATION`, `PARTIEL`, `DEPOSE` ou
`ERREUR_PREPARATION`. Des compteurs séparés distinguent destinataires prévus,
dépôts, envois acceptés, annulés et incertains ; `DEPOSE` ne signifie pas livré.
Pour Live/Push, même séparation entre capture, dépôt, acceptation et lecture.
Les nouvelles entrées batch prennent `limit` entier de 1 à 100, défaut 100 ;
la reprise de préparation accepte en plus `eventId` UUID facultatif, contrôlé
par le contexte d’exploitation autorisé. Curseurs et baux sont persistés côté
serveur ; le navigateur ne fournit ni liste de destinataires ni nouveau contenu.

Pour le nouveau réglage, `expectedVersion` compare `animation.version`, et
`expectedExploitationRevision` compare la coordination existante (initialisée
à zéro lorsqu’elle n’existe pas avant publication). Une modification effective
de l’option incrémente **seulement `animation.version`**, pas la révision des
paramètres de jeu ; les deux commandes la contrôlent et restent sérialisées.
Pas de quatrième CAS « version de réglage ». `definitionVersion` vaut `null`
uniquement sans définition publiée ; sinon entier strict positif conforme à
la définition relue. Cette nullabilité appartient au **nouveau contrat de
réglage**, sans assouplir les commandes existantes de clôture ou de paramètres.
Le motif comporte 5 à 2 000 caractères ; une demande strictement identique à
l’option actuelle est sans nouvel effet après revalidation des gardes, tandis
qu’un rejeu confirmé relit son reçu selon la convention habituelle.

`A_PLANIFIER` désigne une option active sans publication ; aucune échéance
n’est présentée comme un traitement déjà armé. `PREVUE` exige une publication
et une fin future. Les états terminaux de l’animation interdisent toute mutation
du réglage ; la lecture conserve le rapport et les faits de clôture.

Les refus conservés incluent `VERSION_OBSOLETE`, `EXPLOITATION_FERMEE`,
`DATES_INVALIDES`, `FIN_NON_REDUCTIBLE`, `RECONTROLES_REQUIS` et la réouverture
explicite des inscriptions. Nouveaux conflits `409` :
`ACTIVATION_CLOTURE_TARDIVE` si l’on active après fin publiée atteinte,
`DESACTIVATION_CLOTURE_TARDIVE` si l’on désactive après cette échéance,
`CLOTURE_AUTOMATIQUE_NON_MODIFIABLE` si animation clôturée, terminée, archivée
ou population figée, et `DATE_TIRAGE_INCOMPATIBLE` pour le report/l’annonce.
La garde de statut/gel précède les refus temporels. Même enveloppe avec référence
de corrélation, autorisation après verrou, refus cross-tenant sans fuite et
CSRF/origine habituels pour les mutations ERP.

Une migration additive doit porter réglage de clôture et sa trace d’auteur/date
rattachée à la version Animation, événement unique,
photographie agrégée, intentions, audience relationnelle, reçus d’e-mail et index
des échéances effectives. Réutiliser outbox et registre idempotent existants plutôt
que créer un deuxième transport. La décision de paramètres et sa révision restent
la source canonique du report. Les nouvelles références d’animation/organisation
conservent l’isolation et la rétention probatoire ; l’archivage ne les efface pas.
Le numéro de migration sera choisi lors de l’implémentation ; aucune v313 présumée.

### Exploitation, volumes et livraison prévus

Proposition d’ordonnancement : **toutes les deux minutes** pour chacun des deux
nouveaux batchs, indépendants du batch de démarrage, avec activation explicite via
les mécanismes d’exploitation existants. `animations.evenements_cycle.traiter`
reprend rapports et audiences capturés, y compris les reports d’animations dont
l’option de clôture automatique est désactivée. Son activation accompagne la
mise en service des notifications de report, sans dépendre de celle des clôtures.
Le lancement manuel ERP passe par le même batch audité. Rattraper les échéances
manquées sans lancer de tirage. Les erreurs d’une animation sont isolées avec
prochain essai différé ; elles ne bloquent ni les autres organisations ni la page
suivante. Claim/bail, ordre stable `(fin_effective, id)`, verrous non bloquants et
point de reprise empêchent double propriétaire et famine après `SKIP LOCKED`.
La préparation d’événements avance son curseur dans la transaction qui dépose
chaque page de notifications ou de reçus d’e-mail. Les destinataires inexistants
ou révoqués sont tracés comme exclus ; une absence de responsable garde le
rapport en attente, avec nouvel essai différé. Le contrôleur peut relancer la
préparation d’un événement par son identifiant depuis la supervision commune,
sans pouvoir modifier son contenu ou son audience arbitrairement. Une relance
respecte les identités uniques et ne réexpédie pas un courrier déjà déposé.

Bornes de conception : 100 candidats maximum par passe, 25 par page de sélection,
100 destinataires par page de préparation, une animation par transaction de clôture.
À 60 secondes de travail, arrêter de prendre de nouveaux candidats et achever
la transaction en cours ; la suite reste éligible à la prochaine passe.
Le gel existant accumule des faits par participant : le bornage des candidats ne
suffit pas. Refactorer son accès aux faits par pages de 500 avec évaluateur de
qualification existant, insertions/provenances par lots et compteurs agrégés,
**dans la même transaction de gel**. Les notifications sont capturées par
`INSERT … SELECT` indexé, puis matérialisées par pages depuis la photographie.
Pas de `.all()` sur toutes les animations, populations ou installations ; pas
d’appels par participant pour relire sa configuration. Les effets différés
restent idempotents et acquis avec la population. Aucun gel partiel visible.

Budgets de qualification proposés avant implémentation : jeux N/10N de
100/1 000 animations et 1 000/10 000 participants par animation, charge mixte
jeu/report/lecture ; sur PostgreSQL jetable, p95 de transaction de gel inférieur
à 10 s à 10N, surcoût mémoire worker inférieur à 128 Mio, aucune requête N+1.
Le retard nominal inférieur à deux passes concerne seulement une vague d’au
plus 100 échéances dont le travail total tient dans le budget de 60 s. Une vague
de 1 000 échéances exige au moins dix passes avec cette borne : mesurer le débit
réel, le temps de résorption et l’âge maximal, sans lui appliquer ce même objectif
de fraîcheur. Une saturation déclenche l’alerte de retard ; elle ne masque pas
des clôtures non réalisées. Sous charge finie, toute animation éligible sans
erreur finit par être traitée malgré les erreurs ou verrous d’autres animations.
Mesurer durée du verrou, lectures SQL, pages, mémoire et répartition par organisation.
Ces budgets ne sont pas des mesures acquises. Un dépassement bloque la mise en
service du lot concerné et impose une adaptation documentée ; ne pas découper
le gel en commits visibles ni exclure silencieusement une grosse animation.

Supervision : distinguer clôture acquise, rapport à préparer/en attente de
destinataire/en erreur/déposé/transport incertain, Live déposé et Push accepté,
ignoré ou expiré. Alerte si échéance en attente depuis plus de dix minutes ou
préparation bloquée ; référence de corrélation et reprise ciblée sans contenu
personnel dans les logs. La relance ne refait pas la transition ni le gel.

Ordre de livraison ultérieure : migration additive et backend avec batch désactivé ;
contrats canoniques/consommateurs ; interfaces ; scénarios de démonstration et
recette isolée ; activation contrôlée du batch et vérification des retards. Pas
de clôture ni de message rétroactif à la migration. Les animations existantes
suivent A1 arbitré, les déjà clôturées ne génèrent aucun nouveau rapport.
Retour arrière opérationnel : désactiver le batch, conserver événements acquis
et reprises ; ne pas annuler les clôtures réalisées ni retirer les notifications.

### Critères ajoutés et matrice de préparation

Tous les tests ci-dessous sont **à produire ou à réexécuter**, pas des preuves
réussies. Ils complètent FA-01/04/05/07/08/09 sans modifier leur acceptation.

| Critère | Acceptation observable | Propriétaire / preuve attendue | Impacts |
| --- | --- | --- | --- |
| CAF-01 | Activation et valeur initiale conformes à A1 ; échéance affichée, activation tardive refusée | Domaine/commande, migration nouvelles/anciennes lignes, recette PC/mobile et permission | Réglage, OpenAPI, Animation, guide |
| CAF-02 | À fin atteinte, clôture unique, y compris publiée jamais démarrée et rattrapage ; aucun tirage/fin/archive implicite | Domaine horloge figée, worker + PostgreSQL ; comparer fermeture manuelle/automatique de chaque type d’animation | Batch, FA-01/04/07 |
| CAF-03 | Population/provenance/effets/audit/événement acquis ensemble ; incident puis reprise sans doublon | PG : panne avant/après gel et dépôt intention, deux workers, manuel/auto dans les deux ordres | Gel commun, outbox, reçus |
| CAF-04 | Rapport intermédiaire cohérent à sa date, un dépôt par destinataire ; destinataire absent/révoqué et fournisseur incertain visibles | Application + PG + transport simulé, snapshot stable après tirage ; rendu HTML/texte mobile | A3, e-mail, supervision, charte |
| CAF-05 | Clôture manuelle/auto : même audience Live, catégorie et alertes respectées ; Push sans quota ; aucun doublon multi-participations | Matrice prefs/accès/anonymisation, changement entre capture et transport, flag Push off, 404/410 | Live, garde commune, transport |
| CAF-06 | Report réel enregistré et communiqué, sans nouvelle inscription ni perte d’acquis ; dates/fermeture distinctes | Domaine + PG paramètres, copie DSL inchangée, accès non réactivés, no-op et rejeu sans message | A2, T6-QA02, Animation/Live |
| CAF-07 | Prolongation acquise avant fermeture respectée ; après échéance ou gel refusée ; annonce de tirage cohérente | PG deux ordres, attente de verrou franchissant échéance, annonce/report concurrents, heures saisonnières | Coordination partagée, règles dates |
| CAF-08 | Reports successifs historisés ; Push remplacé non envoyé, nouvelle fin courante visible | Deux reports puis clôture, panne/reprise et lecture reçus ; rejet lien externe, clic Push vers animation | Outbox, Live/PWA |
| CAF-09 | Droits/tenant/commune et identité système vérifiés ; modification ou rejeu hors droits sans effet | API/ERP/worker, sessions/CSRF et révocation pendant attente | Contrats, sécurité, audit |
| CAF-10 | Flux visibles, libellés non ambigus, chargement/erreur/reçu accessible, pas de succès d’envoi inventé | Recette à 320/390/1280 px, clavier, focus et lecteurs d’écran ; refus date et absence responsable | Animation, ERP exploitation, Live |
| CAF-11 | Traitement borné, reprise et équité entre organisations ; pas de gel partiel | PG N/10N et charge mixte, plans/durées/mémoire, une animation fautive parmi les échues | Index, workers, exploitation |
| CAF-12 | Migration/export/restauration/démonstration préservent l’historique et ne déclenchent aucun envoi réel | Registre des tables, export tenant, restauration isolée, recettes dates/report/clôture avec transports factices | Migration, générateur, livraison |

Suites existantes à conserver : backend
`tests/domain/animation_locale/test_parametres_exploitation_dedicated.py`,
`tests/security/test_parametres_exploitation_postgres.py`,
`tests/security/test_exploitation_moteur_postgres.py`,
`tests/security/test_moteur_animation_postgres.py` et
`tests/application/animation_locale/test_synchronisation_statuts_animation.py`.
Les nouveaux cas de batch/rapport/prefs et recettes interfaces doivent être
ajoutés au même niveau de preuve. Un build ne prouve pas la course report/clôture.

Lots proposés : **1** règles/contrats/migration/gel et CAF-01/02/03/07/09 ;
**2** rapport/diffusion et CAF-04/05/06/08 ; **3** interfaces/ops/démonstration et
CAF-10/11/12. Le lot 2 utilise les événements du lot 1 ; le lot 3 consomme leurs
projections. Les trois lots restent non implémentés. A1/A2/A3 sont confirmés ;
leurs règles sont à couvrir dans chaque lot dépendant.

Dépôts affectés à terme : **Backend** (domaine/application/adaptateurs, ERP,
batch, tests et générateur), **Animation** (réglage/report/suivi), **Marketplace**
(messages et liens Live), **Projet** (sources/contrats/guides). **Commerçant** :
pas de nouveau parcours ni contrat attendu ; régression des notifications et
accords existants à vérifier. Coffrets autonomes, CRM et SMS de gains : sans
changement de règle ni nouveau transport. Aucun nouveau service Render requis.

## Suivi de réalisation

Mise à jour du **11 novembre 2026** : les commits ont été poussés dans
les cinq dépôts. Sur autorisation explicite ultérieure, la base TEST a
été migrée de v306 à **v309** avec sauvegarde et contrôles de schéma.
Voir le [compte rendu d’exploitation](../../exploitation/animation/deploiement-render.md#application-sur-test-confirmée-le-11-novembre-2026)
pour les preuves et limites. Les constats ci-dessous décrivent la phase de
réalisation initiale ; aucun parcours métier distant n’est attesté.

Spécification et implémentation locales établies à partir des deux arbitrages
utilisateur. Les cinq dépôts sont concernés ; aucun déploiement, commit ou push
au titre de cette évolution. Les suites backend, PostgreSQL et interfaces sont vérifiées localement.
La recette sur TEST et une PWA installée ne sont pas revendiquées ; la
compatibilité complète du générateur est consignée ci-dessous.

| Critères | Réalisation et preuves locales |
| --- | --- |
| FA-01/02/03 | Domaine de fin et commandes versionnées/idempotentes ; tests des trois natures de lot, refus, rollback révocation/décision, justifications exactes et dotation incomplète. Tests HTTP et PostgreSQL dans `tests/domain/animation_locale/test_fin_animation.py`, `tests/api/test_fin_animation_api.py`, `tests/security/test_fin_animation_postgres.py` du backend ; 839 tests réussis dans la passe finale incluant architecture, domaine, application et API ; 13 cas PostgreSQL distincts réussis, puis reprise de deux cas droits/dotation réussie. Rapports backend `tmp/fin-animation-verification-finale.txt`, `tmp/fin-animation-pg-livraison.txt` et `tmp/fin-animation-pg-droits-dotation.txt`. Les suites se recouvrent et ne s’additionnent pas. |
| FA-04/08 | Garde commune `gel_gestion_animation.py` sur les entrées existantes ; revue indépendante des verrous et revalidation des habilitations. Suites de gardes 142, 130 et 83 réussites (recouvrantes) ; concurrence PostgreSQL dans les deux ordres entre fin et correction de remise externe, plus double fin idempotente. Aucune course worker PostgreSQL séparée annoncée ; ses refus après verrou sont couverts dans les tests ciblés des services. |
| FA-05 | Live conserve `TERMINEE` et retire `ARCHIVEE` du carnet, sans supprimer les lots. Deux recettes 320/1280 réussies dans le run Marketplace `15-25-29-555Z-g8L0AL`, 23 tests Node incluant les projections du carnet. Lectures catalogue/participant/Pro et annonce figée : 94 tests ciblés, 2 tests PostgreSQL et 5 projections privées réussis après les corrections de revue. |
| FA-06/07 | Animation : `FinAnimationWorkspace`, `AnimationArchives`, statut et six étapes serveur, retour contextuel préservé ; 22 recettes Fin/Archives à 320/1280 et 26 recettes timeline réussies. Rapports `tmp/fin-animation-captures-lQ7ab9/report.json` et `tmp/workflow-timeline-95bLiq/report.json`. Types, lint complet, build isolé et 18 tests Node réussis. Les recettes utilisent une API simulée. |
| FA-09 | Deux tables classées `replace` dans le registre ; recette locale opt-in avec décisions explicites, sans modifier les dix scènes historiques. 85 tests unitaires de démonstration réussis. Recette avec le vrai `ContexteAutoriseAnimation` et commune explicite : 5 nouveaux cas PostgreSQL réussis (quatre scénarios et rollback complet), plus reprise réussie du cas historique, rapport `backend/tmp/demo-fin-recette-pg-final.txt`. Ces fixtures utilisent les métadonnées. Compatibilité avec migrations, génération et restauration : 8 cas réussis au passage complet, puis 2 variantes de changement de schéma réussies en reprise avec un chemin court ; détails et limites ci-dessous. |

Les revues ont fait corriger le total Coffrets, les intentions d'anciens gains,
les capacités des bons, les cibles de prochaine action, le retrait des contacts,
le snapshot des commerces, les lectures de lots après fin et l'annonce de date
restée modifiable depuis l'ERP. Le questionnaire volontaire habitant reste
indépendant du gel de gestion. Pro : 50 tests Vitest du modèle d'animation et des contrats API
réussis sur configuration isolée. Les contrats embarqués sont synchronisés
après les exports canoniques ; aucun résultat local ne prouve la migration TEST.

La pagination PostgreSQL est vérifiée sur 1 000 dossiers : 17 lectures SQL
constantes pour des pages de 1/10/50, sans doublons et sans matérialisation
par unité de lot. Plans et mesures dans `backend/tmp/fin-animation-pg-pagination.txt`.
Ce contrôle ne constitue pas une campagne de charge sur infrastructure hébergée.

### Compatibilité PostgreSQL du générateur

Le passage complet sur PostgreSQL 18, avec migrations jusqu'à v309, a produit
**8 réussites et 2 échecs d'écriture d'archive**, sans skip. Rapport backend
`tmp/fin-demo-detached-a44862b6e6434003af97d25bf3b5e825-proof/results.xml`.
Les deux chemins de checkpoint atteignaient 264 caractères sous Windows ; les
archives originales de 216 caractères étaient bien écrites. Sans modification
des assertions ou des sources produit, la reprise des deux variantes de
`test_demo_reset_schema.py` dans `tmp/dq4d2007ed/` réussit : **2 cas, 0 échec,
0 skip**, sortie 0. Le runner isolé et son contrôle des scénarios requis sont
conservés pour ce module ciblé. Il ne s'agit pas d'un nouveau passage global
des dix cas ; les deux rapports sont nécessaires au bilan.

Les fixtures ont été adaptées au CRM Nouvelle-Aquitaine et vérifient les
contraintes différées avant leur restauration dans une même transaction.
L'intégrité restaurée est comparée sur toutes les données, en attendant
explicitement l'incrément des quatre jetons CRM qui invalide les anciens baux ;
l'empreinte de la sauvegarde source reste identique à l'original. Aucun skip,
retrait d'assertion, mode produit spécial ou désactivation de contrainte.
Les premiers rapports rouges et un passage interrompu par une erreur de
stdout de l'outil sont conservés ; ils ne sont pas comptés comme succès.
Les trois clusters jetables 31475, 31571 et 31572 sont arrêtés ; aucune base
TEST ni aucun fournisseur réel n'ont été utilisés.
