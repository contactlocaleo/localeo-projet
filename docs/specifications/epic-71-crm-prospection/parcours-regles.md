# E71 — Parcours simples de Localeo CRM

[Version V1 et arbitrages](README.md). Comportements V1.1 du 3 novembre 2026, implémentés localement ; la [qualification V1.2](qualification-structuree.md) les complète. Les tests et réserves sont dans le [bilan](verification-livraison.md).

## Navigation PC et mobile

PWA distincte **Localeo CRM**, avec entrée autorisée depuis l'ERP et lancement direct après installation. Vues principales : **Aujourd'hui**, **Prospects**, **Suivi**, **Rappels**. Imports et préférences dans le menu secondaire ; aucune entrée d'administration sans droit. L'en-tête reprend l'identité partagée, le nom de l'application et l'environnement hors production. Retour ERP seulement si destination autorisée.

Sur PC, menu latéral et listes compactes exploitant la largeur disponible. Sur mobile, navigation principale accessible au pouce, listes en cartes et filtre dans un panneau ; aucune table débordante imposée. Une action principale par écran, actions secondaires regroupées. Icônes accompagnées de libellés pour les actions métier ; actualisation compacte avec nom accessible. Zones tactiles de 44 px au minimum, focus visible, statuts exprimés par texte et icône en plus de la couleur.

Un seul défilement du contenu, titres/retours cohérents, formulaires courts et aide près du champ. Revenir à la liste conserve recherche, filtres, tri, position et mode liste/carte. Le bouton retour du navigateur reste utilisable. Recherche côté serveur, pagination à la demande, pas de téléchargement complet du portefeuille. Une note non enregistrée déclenche une confirmation avant sortie ; un échec conserve le texte dans la page, sans persistance privée hors ligne.

Le mode hors connexion affiche un écran explicite de reconnexion : ni prospect en cache ni commande différée envoyée à la reconnexion. La PWA reste utile sans notifications autorisées. Chargement, vide, erreur et succès sont distincts ; succès seulement après confirmation serveur. Le délai réseau d'une mutation impose la relecture du résultat avant répétition.

## 1. Commencer sa journée — CA-05/06/22

« Aujourd'hui » montre d'abord mes actions en retard, puis celles du jour, puis les prochaines. Un filtre explicite permet de voir l'équipe, avec le même portefeuille global autorisé. Une section secondaire signale les dossiers actifs sans responsable/contact/prochaine action ; l'incomplétude n'empêche pas d'enregistrer un prospect.

Compteurs : prospects actifs distincts, dossiers ouverts par périmètre/étape, rappels en retard, dossiers sans prochaine action, gains vérifiés sur la période. Une structure Animation et Coffrets compte une fois comme prospect et deux fois comme dossiers. Les estimations facultatives ne deviennent jamais un chiffre d'affaires ; pas de prévision financière ou score de probabilité en V1.

## 2. Ajouter un prospect — CA-01/02/10

Formulaire rapide : **nom de la structure, commune de Nouvelle-Aquitaine sélectionnée, périmètre et objet commercial**. Le titre du dossier peut être prérempli par le libellé du périmètre/objectif, sans inventer de besoin. Les coordonnées de contact peuvent être ajoutées ensuite. Le responsable du dossier est l'utilisateur créateur par défaut pour la saisie manuelle, modifiable vers un utilisateur actif autorisé à gérer le CRM.

Une fiche prospect porte nom, type facultatif (collectivité, association, commerce, entreprise/CSE, autre), adresse facultative, commune/INSEE, coordonnées de structure, source, état actif/archivé et version. Depuis la demande du 4 novembre 2026, une commune de Nouvelle-Aquitaine identifiée par INSEE est obligatoire à la création et lors d'un changement effectif de localisation. Une commune hors catalogue Localeo reste admissible dans cette région ; résolution explicite au centre communal, sans géocodage d’adresse ni création/publication d'une ville marchande. Les fiches historiques hors région ou sans commune gardent leur suivi et leurs contacts modifiables sans relocalisation imposée.

Chaque contact porte nom, fonction, e-mail/téléphone professionnels connus et état actif/obsolète. Au moins un nom ou une coordonnée valide est nécessaire. Plusieurs contacts sont possibles ; un départ rend le contact obsolète sans supprimer son histoire. Les coordonnées de structure ne remplacent pas automatiquement celles d'une personne.

Chaque dossier appartient à un prospect, avec périmètre **ANIMATION** ou **COFFRETS**. Coffrets exige un objectif **PARTENARIAT_COMMERCANT** ou **ACHAT_ENTREPRISE_CSE**. Plusieurs dossiers du même périmètre sont possibles pour des campagnes successives. Le responsable, l'étape, la priorité normale/haute et les tâches sont propres au dossier.

### Responsable du prospect — correctif du 6 novembre 2026

La fiche possède aussi son **responsable de prospect**, visible dans son en-tête et
modifiable directement avec le droit `crm.gerer`. Il peut être non attribué : les
anciennes fiches et les prospects importés ne sont jamais affectés implicitement
au responsable d'un dossier ni à celui du lot d'import. Une sélection explicite
doit désigner un utilisateur interne actif autorisé à gérer le CRM ; retirer
l'affectation laisse la fiche « Non attribué ».

Cette affectation est indépendante des responsables des dossiers et des actions :
la changer ne réaffecte aucun dossier, rappel ou notification. La commande conserve
le contrôle de version et l'idempotence existants, et ajoute un événement système
`RESPONSABLE` à l'historique avec l'auteur et les anciennes/nouvelles références.
Le responsable non habilité est refusé avant toute écriture. Une opposition ou un
archivage ne sont pas levés par cette opération.

Le filtre **Responsable du prospect** dans Prospects et Carte porte sur cette
affectation, y compris pour un prospect sans dossier. Les filtres Responsable dans
Suivi et Rappels restent ceux des dossiers et des actions respectivement. La
pagination, ses totaux et les agrégats de la carte appliquent la même sélection
avant de compter. L'API ajoute `responsable_id` nullable à la création, à la
modification et à la projection Organisation ; la migration
`v294_crm_responsable_prospect.sql` ajoute cette référence sans reprise automatique.
L'import CSV reste inchangé et préserve les affectations existantes.
Le détail expose aussi `responsable_nom` (prénom et nom, sans e-mail) et
`responsable_a_reaffecter`. Cette lecture directe reste complète si la personne
n'apparaît pas dans la première page du sélecteur. Une personne inactive ou ayant
perdu le droit de gérer le CRM ou le rôle BACKOFFICE conserve son nom affiché avec une invitation à
réaffecter ; aucune mutation automatique n'est effectuée.

Avant création, montrer les ressemblances (nom/commune, coordonnées), sans fusion automatique. Une correspondance certaine exige un identifiant CRM ou de source déjà établi ; nom ou e-mail générique commun ne suffisent jamais. Créer un prospect ne crée ni client, commerce, accès, souscription, commande ou e-mail.

## Carte interactive — CA-07/13/14/15

Dans **Prospects**, bascule « Liste / Carte » sans changer de filtre : périmètre/objectif, étape du dossier, responsable, priorité, commune/département et état actif/archivé. Un prospect ayant plusieurs dossiers correspondants apparaît une seule fois comme structure ; le groupe indique séparément prospects et dossiers.

La carte présente des centres communaux intitulés **« Localisation à la commune — approximative »**, jamais l'adresse exacte d'un contact. Les points superposés sont regroupés ; cliquer sur un groupe ouvre une liste paginée de prospects et leurs dossiers correspondant aux filtres, puis la fiche. Sur mobile, le panneau s'ouvre sous la carte ; retour conserve filtres, zone et zoom. Les contrôles sont nommés et accessibles au clavier ; la liste offre toutes les actions sans manipuler la carte.

Compteur « Sans commune identifiée » ouvrant une liste historique dédiée tous territoires. L'INSEE résolu et son centre sont séparés de la commune textuelle source. Nom ambigu ou code postal partagé : choix explicite parmi les candidats de Nouvelle-Aquitaine avant une nouvelle création. Une panne du référentiel conserve la saisie et la sélection existante ; un code non encore référencé demande de réessayer la recherche. Les mises à jour de suivi, les mutations avec une commune déjà référencée et les imports ne nécessitent pas de géocodage réseau. Une panne du fond de carte affiche un réessai et le retour à la liste.

Couverture actuelle : Nouvelle-Aquitaine, filtre sur ses douze départements. Les anciennes fiches hors région restent accessibles dans la liste générale ; aucune commune n'est placée sur un point arbitraire. Aucun GPS personnel nécessaire pour consulter les prospects. Le fournisseur de fond reçoit seulement les requêtes nécessaires aux tuiles, aucune fiche, note ou coordonnée de contact.

## 3. Suivre et consigner un échange — CA-03/04

Six étapes : **À contacter**, **En discussion**, **Proposition envoyée**, **Gagnée**, **Perdue**, **En pause**. Sauts et retours sont autorisés entre étapes actives, avec trace ; pas de formulaire de qualification imposé avant chaque étape. Perte : motif obligatoire. Pause : motif et date de réexamen ; échéance = signal à reprendre, pas réouverture automatique. Réouverture d'un dossier terminal : action explicite et motif.

Conserver les preuves de gain décidées en octobre : partenariat commerçant accepté avec commerce et dossier OnBoard liés ; Animation avec souscription activée payée ou gratuite ; achat Coffrets avec commande payée. Le serveur lit les preuves canoniques. Un accord oral peut être noté en discussion ; il ne certifie pas le gain. Le changement d'étape n'active aucun objet métier. Les tâches ouvertes sont présentées lors de la clôture pour annulation/réalisation explicite, jamais supprimées en silence.

**Unicité du gain confirmée (ARB-04b).** Une même commande payée, souscription
activée ou acceptation commerçant ne peut faire gagner qu’un seul dossier CRM.
Plusieurs dossiers peuvent conserver un lien de consultation, clairement distinct
de l’attribution du gain. Un conflit indique que la preuve est déjà attribuée et
propose le dossier détenteur si l’utilisateur est autorisé à le consulter.

Réouvrir, perdre ou archiver le dossier ne libère pas automatiquement sa preuve.
Le même dossier peut retrouver son état gagné avec cette preuve si elle est encore
éligible ; cela ne compte pas une seconde vente. La V1 ne propose pas de transfert
silencieux d’attribution entre dossiers. Les indicateurs de gains comptent les
preuves canoniques distinctes et affichent leur période ; la chronologie conserve
chaque transition. Un gain est un constat commercial à sa date, pas une nouvelle
attestation de paiement : consulter l’état financier courant dans le domaine métier.

Dans la fiche, **Ajouter une note** est immédiatement visible. Types courts : note, appel, rendez-vous, e-mail consigné. Texte libre limité à 10 000 caractères, date réelle de l'échange, auteur et date de saisie serveur. Les corrections sont versionnées/tracées ; elles ne remplacent pas l'audit. Une note disant « e-mail envoyé » n'envoie rien et ne prouve aucune délivrance. Après enregistrement, proposer « Programmer la prochaine action » sans l'imposer.

**Correctif du 12 novembre 2026 :** l'historique quotidien présente une seule
ligne par échange initial, avec sa dernière correction (texte, date et auteur).
Les versions antérieures restent enregistrées, mais ne sont pas des échanges
supplémentaires dans cette liste. La nouvelle correction vise l'identifiant et
la version de la révision affichée ; un écran périmé garde le refus de concurrence.
Deux notes distinctes de même contenu restent deux échanges. Le type affiché
vient de l'échange initial ; la pagination et les totaux comptent ces échanges.

Les échanges globaux sont rattachés au prospect, ceux d'une affaire à son dossier ; la chronologie de la fiche indique ce contexte. Ni import ni réouverture ne réécrivent les notes, décisions ou preuves historiques.

## Recherche partagée — CA-07/13/35/50/54

État relu le **6 novembre 2026**, backend `d928b9a`. Les filtres suivants
existent dans les producteurs HTTP et SQL ; ils constituent le socle à réutiliser
pour Qualification. Les critères d’une recherche se combinent par **ET**. Plusieurs
conditions de contact doivent être satisfaites par **le même contact actif** ;
plusieurs conditions de dossier par **le même dossier**. Aucune multiplication
des prospects dans les résultats, les totaux ou les groupes de la carte.

| Besoin utilisateur | Paramètres existants | Présentation |
| --- | --- | --- |
| Trouver une structure ou une coordonnée | `q` | Recherche principale ; téléphone/e-mail, nom/commune et identifiants légaux pris en charge par le serveur, sans recherche dans les longues notes |
| Cibler le territoire | `departement`, `insee`, `region`, `epci_siren`, `sans_commune` | Département toujours visible dans Prospects ; douze départements de Nouvelle-Aquitaine. Commune/EPCI et non-localisés dans les filtres détaillés ; `sans_commune` concerne la liste, pas des points inventés sur la carte |
| Sélectionner communes et intercommunalités | `sous_type_collectivite`, `nature_epci` | Sous-type et nature d’EPCI ; ne pas présenter un filtre générique `type` comme déjà disponible |
| Retrouver son portefeuille | `responsable_id`, `etat` | Responsable **du prospect** dans Prospects/Carte, responsable **du dossier** dans Suivi. Actif/archivé conservés ; pas de réaffectation implicite |
| Cibler un dossier | `perimetre`, `objectif`, `etape`, `priorite`, `besoin_statut`, `budget_statut`, `porteur_statut` | Groupe « Projet commercial » ; priorité manuelle distincte du futur niveau calculé. La sélection porte sur un même dossier admissible |
| Évaluer le potentiel documenté | `classement`, `base_comptage`, `nb_commerces_min`, `nb_commerces_max`, `non_evalue`, `a_examiner` | Groupe « Potentiel » ; zéro différent d’inconnu, référence de comptage cohérente avec commune/EPCI ; minimum supérieur au maximum refusé |
| Trouver un interlocuteur | `nature_contact`, `role_commercial`, `fiabilite_contact` | Groupe « Contacts » ; un contact vérifié ne prouve ni consentement ni autorisation de solliciter |
| Cibler l’activité | `famille_animation` | Groupe « Activité » ; ne pas déduire la famille d’une simple recherche de texte |

Les filtres inconnus de l’évolution ne doivent jamais être ignorés en silence :
la future lecture Qualification possède un schéma fermé, affiche les filtres
actifs et refuse les valeurs incompatibles avec le profil. Les paramètres
existants des anciennes routes restent compatibles ; la nouvelle validation
ne modifie pas tacitement leurs clients.

Les ajouts **objectif/profil de calcul, niveau, état du résultat et tri de priorité calculée**
sont spécifiés dans [E71-EVOL-06](niveau-qualification.md) et restent à développer.
Le niveau commercial ne remplace pas `classement`, qui décrit le potentiel de
référence, ni `priorite`, choisie manuellement dans un dossier. Les filtres
portant sur les dossiers d’une liste de prospects ne changent pas le sens du
responsable propre au prospect.

Sur mobile : département et recherche restent accessibles sans ouvrir toutes
les sections ; les filtres détaillés sont regroupés avec le nombre de filtres
actifs. « Appliquer » relance à la première page ; « Réinitialiser » retire les
choix utilisateur et conserve seulement le périmètre explicite de la vue.
Le retour depuis une fiche retrouve les filtres de l’URL ; aucune note ou
coordonnée de contact n’est ajoutée à une URL par le composant. Une recherche
textuelle saisie par l’opérateur peut déjà contenir une coordonnée : elle ne doit
pas être copiée dans les journaux techniques ou les liens envoyés à un tiers.

Le total est daté, demandé une fois par recherche ; pagination 25/100 et curseurs
signés liés aux filtres/droits conservés. Les interfaces ne filtrent pas les seuls
éléments téléchargés. Preuves de non-régression à rejouer lors d’E71-EVOL-06 :
département + responsable + potentiel, contact/dossier commun aux prédicats,
zéro/non-évalué, même audience liste/carte/calcul, retour de fiche et petit écran.
Les tests déjà exécutés des filtres existants ne valident pas les nouveaux filtres
de niveau ni la capture d’une audience de calcul.

## 4. Programmer et recevoir un rappel — CA-05/06/26/27

Action depuis la fiche ou un dossier : libellé, type commercial, responsable, date de l’action et rappel. Les types proposés sont **Prospection d’appel**, **Relance**, **Suivi**, **Fidélisation**, **Hors cible**, **Barrage secrétariat** et **Pas intéressé** (`PROSPECTION_APPEL`, `RELANCE`, `SUIVI`, `FIDELISATION`, `HORS_CIBLE`, `BARRAGE_SECRETARIAT`, `PAS_INTERESSE`). Une **Préparation interne** séparée reste possible sans sollicitation. Les anciennes actions `APPEL`, `EMAIL`, `RENDEZ_VOUS` et `PREPARATION` restent lisibles, filtrables et gérables ; aucune donnée n’est renommée automatiquement.

Le type commercial décrit l’action planifiée et ne remplace pas son canal. Une sollicitation désigne explicitement sa cible : un contact actif du prospect (`contact_id`) ou la structure (`cible=STRUCTURE`, coordonnées de structure), avec un canal explicite (téléphone, e-mail ou présentiel). Tous les types commerciaux restent sollicitants ; seule la préparation interne est non sollicitante. Les libellés « Hors cible », « Barrage secrétariat » et « Pas intéressé » ne modifient ni l’état du prospect, ni l’étape d’un dossier, ni les oppositions. Une opposition réelle s’enregistre toujours par l’action dédiée ; une simple note après un échange se consigne dans l’historique.

L’opposition de la structure bloque toutes ses cibles ; une opposition de contact bloque les tâches qui le ciblent. Si sa coordonnée est réutilisée comme coordonnée de structure, le blocage reste applicable à cette coordonnée normalisée : pas de contournement par changement de libellé. Une tâche peut appartenir au prospect sans dossier ; si un dossier est indiqué, il doit appartenir au même prospect. Proposition simple : rappel à l'échéance par défaut ; l'utilisateur peut fixer une date/heure antérieure. Pas de récurrence automatique en V1. Cette évolution des libellés et codes de type ne nécessite pas de migration : le stockage existant et la contrainte « préparation seule non sollicitante » restent compatibles.

La liste **Rappels** propose un filtre **Type d’action**, combinable avec l’état,
le responsable et les rappels disponibles/en retard. « Tous les types » supprime
ce filtre ; les types historiques restent sélectionnables. Le paramètre `type`
de `GET /internal/prospection/taches` et de son alias `/rappels` est validé avant
lecture, puis appliqué avant le calcul des totaux et la pagination. Changer le
type réinitialise les pages ; un curseur d’une autre recherche est refusé.

Le filtre facultatif **Date de l’action**, avec calendrier, sélectionne les
actions prévues ce jour-là en **Europe/Paris**, indépendamment de leur date de
rappel. Une date vide ne restreint pas la recherche. `date_action=AAAA-MM-JJ`
est validé sur les mêmes routes, puis appliqué en stockage avant pagination
et total : minuit Paris inclus, minuit du lendemain exclu, même lors des
changements d'heure. La date se combine avec les autres filtres, reste dans
l'URL après actualisation et son changement invalide les anciens curseurs.

Dates affichées en **Europe/Paris**, instants stockés UTC avec fuseau ; les heures inexistantes ou ambiguës au changement d'heure demandent correction/choix explicite. Lors de la programmation d'une action, une date seule nécessite une heure confirmée. Terminer exige un résultat court, annuler un motif ; reporter conserve l'ancienne échéance et invalide l'ancien rappel. La « prochaine action » est calculée depuis la première tâche ouverte, pas un deuxième champ éditable.

Le rappel interne est toujours disponible. **WebPush** est activé volontairement par appareil depuis les préférences ; aucun prompt navigateur avant un clic explicite. Refus, navigateur non compatible ou abonnement expiré : message clair, file interne intacte. À l'ouverture, la notification mène à la tâche après authentification, puis contrôle les droits courants.

**E-mail facultatif** : préférence personnelle désactivée initialement. Un message à la même échéance, adressé à l’adresse vérifiée du compte interne du responsable, jamais au contact du prospect. La vérification est liée à la version d’adresse courante par Identité interne (consommation d’un lien valide d’initialisation/réinitialisation), pas au seul état actif du compte. Changer l’adresse suspend l’option jusqu’à vérification puis nouvel opt-in pour cette adresse. Sans adresse interne vérifiée disponible, l’option e-mail est indisponible avec explication ; la file interne et le push restent utilisables. Activer l'e-mail en plus du push peut produire un message sur chaque canal choisi ; aucun basculement e-mail implicite après refus du push. Aucun rattrapage massif lors de la première activation d'un canal : tâches déjà échues restent dans la file interne.

Un rappel n'est produit qu'une fois par tâche/révision d'échéance/destinataire/canal (et abonnement pour le push). Réaffectation, annulation, réalisation, archivage, perte de droits ou changement de préférence annulent les envois encore en attente ; recontrôle avant remise au transport. Un message déjà remis au fournisseur ne peut pas être rappelé et ne prouve pas la lecture. En cas d'issue incertaine, distinguer cet état d'un échec certain ; pas de promesse de livraison « exactement une fois » par un fournisseur externe.

Notifications discrètes : « Une action commerciale vous attend », sans nom, note, téléphone ou e-mail de prospect sur écran verrouillé. Notification interne et état de tâche restent la référence même si l'envoi échoue. Les erreurs sont observables et les retries bornés ; jamais de boucle de renvoi à chaque visite.

### E71-EVOL-07 — dates des actions plus explicites

Évolution demandée le **5 novembre 2026**, spécification précisée le **6 novembre**,
**implémentée localement le 6 novembre**, sans déploiement. Le calendrier
explicite présent dans `d928b9a` est conservé avec les nouveaux libellés et aides.
Le formulaire utilisait « Échéance » et « Rappel », difficiles à distinguer.
La cible concerne la planification, le détail et le report d’une action, ainsi
que les libellés de dates affichés dans les listes. Le menu **Rappels** est conservé.

| Champ existant | Libellé cible | Aide visible associée au champ |
| --- | --- | --- |
| `due_at`, obligatoire | **Action prévue le · heure de Paris** | Date et heure auxquelles vous prévoyez de réaliser l’action. Si elle reste ouverte après cette date, elle apparaît en retard. |
| `remind_at`, facultatif à la création | **Me rappeler le · heure de Paris** | Date et heure du rappel, au plus tard à la date de l’action. Si vous laissez ce champ vide, le rappel est fixé à la date de l’action. |

Exemple présenté à proximité des champs : « Appel prévu vendredi à 14 h ; rappel
vendredi à 9 h pour le préparer. » Dans le détail et le report, reprendre les
mêmes libellés, sans réintroduire « Nouvelle échéance » ou « Nouveau rappel ».
Dans une liste, une date unique doit être identifiée comme date de l’action,
pas comme date de notification. « En retard » reste déterminé par `due_at`.

Au report, « Me rappeler le » est obligatoire et prérempli. Remplacer l’aide
de création sur le champ vide par « Choisissez la date du nouveau rappel, au
plus tard à la date de l’action. » Le même libellé n’implique pas la même
facultativité : l’aide ne doit pas promettre un défaut que la commande de report
n’applique pas.

Les deux dates restent distinctes et éditables ; conserver les valeurs en cas
d’erreur. Une aide ne dépend pas d’un survol : texte lisible PC/mobile et associé
au champ pour les lecteurs d’écran. Erreur près du rappel si celui-ci dépasse
l’action : « Le rappel doit précéder ou coïncider avec la date de l’action. »
Les contrôles de fuseau et d’heure ambiguë/inexistante restent appliqués.

Le rappel interne reste disponible ; l’aide précise que WebPush/e-mail dépendent
des préférences et autorisations du responsable. Le champ ne promet pas un envoi
ni une notification à l’utilisateur opérateur si le responsable choisi est une
autre personne. Aucun message ne part au prospect grâce à ces seuls champs.

Règles conservées : à la création, rappel omis = date de l’action ; rappel
antérieur ou égal accepté, postérieur refusé. Le report réutilise les commandes
existantes et invalide l’ancien rappel. Ne pas modifier par cette retouche le
traitement d’un rappel omis au report, les états, versions, droits ou déduplication.
Le domaine `TacheProspection` reste propriétaire de `remind_at <= due_at` ; aucune
nouvelle règle ni différence de calcul entre formulaire, filtre et worker.

Impacts : libellés et aides PWA CRM dans le backend, guide utilisateur et tests
navigateur à adapter. **Sans migration ni nouveau contrat API** : noms JSON,
valeurs stockées, notifications et CSV inchangés ; aucun impact direct sur les
trois autres frontends ou les droits ERP. Le générateur conserve ses dates et
fixtures ; seuls ses éventuels sélecteurs de formulaire sont à vérifier à la livraison.
Ni configuration ni opération TEST nécessaire à cette spécification.

#### Contrat de saisie et scénarios à vérifier

Les noms JSON restent `due_at` et `remind_at`, instants ISO 8601 avec fuseau.
Le champ natif avec calendrier et saisie clavier utilise l’heure de Paris ; la
conversion reste celle du module ERP partagé `instants-paris.js`. Les boutons
calendrier reprennent le nouveau nom accessible du champ, sans « échéance »
résiduelle, et ne soumettent pas le formulaire. L’aide est reliée par
`aria-describedby` ; le champ invalide reçoit `aria-invalid` et le focus.

| Situation | Résultat exigé, sans changement de règle |
| --- | --- |
| Création : action le 10 décembre à 14 h Paris, rappel omis | `due_at=2026-12-10T13:00:00Z` ; serveur initialise `remind_at` au même instant |
| Rappel le même jour à 9 h Paris | Accepté, `remind_at=2026-12-10T08:00:00Z` ; l’action n’est en retard qu’après 14 h |
| Rappel égal à l’action | Accepté ; ne pas imposer un délai minimal nouveau |
| Rappel après l’action | Refus `DATE_RAPPEL_INVALIDE`, message près de « Me rappeler le » ; conserver les autres valeurs |
| Report | Préremplir les deux valeurs courantes ; transmettre les deux dates explicitement avec `expected_version` et la clé d’idempotence. Un rappel effacé au report est refusé par la règle existante : aucun défaut silencieux copié de la création |
| Heure de Paris inexistante ou ambiguë au changement d’heure | Refus de conversion et correction demandée ; ni décalage automatique ni choix arbitraire d’un instant |
| Responsable du rappel différent du responsable du prospect | Le rappel reste destiné au responsable **de l’action**, avec ses préférences ; aucun changement d’affectation |
| Conflit de version ou réponse incertaine | Valeurs conservées ; refus concurrent explicite ou rejeu de la même commande, sans nouveau rappel dupliqué |

Le report exige un motif comme auparavant. La modification des textes ne change
pas les capacités `crm.consulter`/`crm.gerer`, le contrôle de sollicitation, les
révisions de rappel ni les transports. Son implémentation est indépendante de
l’actualisation externe et du barème de qualification commerciale.

| Critères | Preuves prévues, résultats dans le bilan de livraison | Livraison |
| --- | --- | --- |
| E71-CA-60 | Navigateur PC/mobile/clavier : création, détail, liste et report, libellés cohérents, aides associées, valeurs préservées après erreur et responsable distinct | PWA CRM et guide, aucune modification des routes ou données |
| E71-CA-61 | Non-régression domaine/HTTP : rappel omis à la création, avant/égal/après l’action, changement d’heure et report ; filtres retard/rappel disponible toujours distincts | Réutiliser les tests de tâches/rappels ; aucune notification externe réelle ni migration |

## 5. Importer — CA-08 à 12/28

Parcours **Fichier → Aperçu → Confirmation → Bilan**. Choisir source stable, mode INIT/UPSERT et responsable des nouveaux dossiers (opérateur par défaut). Télécharger le [modèle](modele-import.csv), puis préparer le CSV selon le [contrat d'import](import-carte.md). L'aperçu montre créations, compléments, valeurs conservées, conflits et rejets. Aucune conversion, tâche ou notification n'est déclenchée par l'import.

## 6. Passer au métier — CA-16/17/18

Depuis un dossier, rechercher puis rattacher une référence canonique existante, ou ouvrir le parcours ERP/OnBoard autorisé et revenir rattacher son résultat. Les droits CRM et métier se cumulent ; un accès CRM ne donne pas un accès Animation, Pro, Finance ou SQLAdmin. Aucun contact/note dans l'URL de retour. En cas d'interruption après création métier, chercher le résultat existant ; ne pas recréer automatiquement.

Conserver la fiche, ses contacts, notes et rappels après gain/rattachement : c'est la continuité de la relation client. Support, facturation, contrats, livraison et gestion opérationnelle restent dans leurs applications ; aucun ticket ou paiement dupliqué dans le CRM.

## Opposition et archivage — CA-20

Proposition simple : **Ne plus contacter** au niveau prospect (tous ses contacts) ou contact, pour toutes les sollicitations commerciales. Enregistrement immédiat par gestionnaire CRM, motif/source/date/acteur ; une levée requiert l'administration CRM et une justification/provenance explicites. Cette simplification remplace la proposition antérieure d'opposition configurable par axe/canal ; la levée demeure sensible.

La saisie manuelle, l'import et les tâches utilisent la même règle. Les tâches de sollicitation ouvertes deviennent bloquées et leurs rappels externes sont annulés ; notes factuelles et préparation interne restent possibles. Une tâche « préparation » ne permet pas d'y cacher une demande d'appel ; le canal/type sollicitation est explicite. Archiver interdit de nouvelles sollicitations et retire la fiche des vues actives ; réactiver ne lève pas l'opposition. Aucune cellule CSV ne réactive un contact obsolète, une fiche archivée ou une opposition.
