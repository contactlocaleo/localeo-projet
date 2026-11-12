# Prendre en main Localeo CRM

[Spécification](README.md) · [Qualification structurée](qualification-structuree.md) · [Format CSV](import-carte.md) · [Exploitation](exploitation.md).

Localeo CRM suit vos relations commerciales Animation et Coffrets. Il utilise votre compte interne Localeo. Une fiche représente une structure ; ses contacts, échanges et dossiers restent réunis même lorsqu’elle s’intéresse aux deux offres.

**UX quotidienne — 12 novembre 2026 :** [E71-EVOL-10](ux-productivite.md) conserve
votre contexte et simplifie les actions. Ces changements nécessitent la livraison
conjointe du backend et de ses ressources CRM.

- **Aujourd’hui** ouvre **Mes actions** pour votre compte nominatif. **Équipe**
  affiche le portefeuille partagé. En retard, Aujourd’hui et À venir sont trois
  groupes distincts, selon la date de l’action en heure de Paris ; chaque compteur
  correspond à sa portée. Les indicateurs collectifs sont repliés sous les actions.
- Le retour depuis une fiche conserve votre recherche et sa page. Sur téléphone,
  **Plus** donne accès à Suivi, Qualification, Carte, Imports et Préférences selon
  vos droits ; **Filtres** ouvre les critères secondaires de la recherche.
- La fiche présente contact, prochaine action et dernier échange avant la
  qualification. Sélectionnez le contact utile ; **Tous les contacts** permet de
  parcourir les pages. Après une note ou une action terminée, **Planifier la
  prochaine action** est facultatif : **Plus tard** ne crée aucune tâche.
- Le report d’un rendez-vous propose les disponibilités de son responsable.
  Celui-ci reste fixe ; un transfert passe par **Réaffecter**. Choisissez le
  rappel relatif ou personnalisé. Un conflit conserve votre saisie pour correction.
- Les formulaires d’action et d’opposition donnent accès aux contacts suivants.
  Pour rattacher une preuve, recherchez sa référence par nom. Pour constater un
  gain, choisissez une référence déjà rattachée et éligible ; le serveur la
  contrôle de nouveau lors de la confirmation.
- Le suivi d’import s’actualise automatiquement tant que la page est visible.
  Les commandes de confirmation/reprise restent explicites. En actualisation,
  **Appliquer et continuer** traite vos choix de la page, puis ouvre la suivante.
  Les liens d’évaluation ouvrent exactement le résultat produit. **Recalculer ce
  prospect** prépare une sélection d’un seul prospect avant votre confirmation.

## 1. Ouvrir votre espace

Depuis le menu **Applications** de l’ERP, choisissez **Localeo CRM**. L’adresse est `/internal/crm/` sur le même domaine backoffice. Si l’entrée manque, demandez à l’administrateur le droit **Consulter le CRM**. La gestion, les imports et la levée d’opposition disposent de droits distincts ; un accès ERP existant ne les ajoute pas automatiquement.

Après activation du domaine dédié, vous pouvez ouvrir directement
**https://test-crm.localeo.city** sur TEST, ou **https://crm.localeo.city** en
production. Les liens ERP y conduisent automatiquement une fois la configuration
activée. Utilisez le même compte personnel que dans l'ERP ; une première connexion
sur ce domaine est nécessaire. Vous retrouvez les mêmes prospects et droits.
L'URL conserve le chemin `/internal/crm/` après ouverture.

Si vous utilisiez déjà la PWA depuis le backoffice, installez-la à partir du
nouveau domaine et activez volontairement ses notifications sur cet appareil.
L'ancienne installation et ses abonnements ne sont pas transférés automatiquement.

**Aujourd’hui** présente les actions en retard, les dossiers sans prochaine action, le portefeuille et les gains du mois. Sur mobile, les entrées principales sont en bas de l’écran. **Installer Localeo CRM** propose l’installation de la PWA ; elle conserve la même session et les mêmes droits. Une connexion réseau est nécessaire : les fiches et notes ne sont pas conservées hors ligne sur l’appareil.

## 2. Créer un prospect et préparer la suite

### Planifier un rendez-vous commercial

Dans **Agenda → Mes disponibilités**, indiquez vos plages hebdomadaires et vos
absences, en heure de Paris. Plusieurs plages sont possibles dans une journée.
Sans plage configurée, aucune disponibilité n’est proposée. Une absence qui
recouvre un rendez-vous actif exige d’abord son report ou son annulation ;
modifier vos horaires habituels ne déplace pas vos rendez-vous existants.

Depuis une fiche prospect, choisissez **Nouveau rendez-vous**. Indiquez la durée
recherchée et la date de départ : chaque membre affiche sa prochaine disponibilité.
**Voir les créneaux** permet de choisir un autre horaire ; vous pouvez aussi saisir
directement les dates et sélectionner le collaborateur. Ajoutez un titre, une
note facultative et, si besoin, un rappel avant le rendez-vous. **Réserver le
rendez-vous** vérifie une dernière fois la disponibilité. En cas de conflit,
votre saisie reste disponible pour choisir un autre créneau.

Le rendez-vous apparaît dans **Agenda**, dans les actions du prospect et dans
les rappels avec une icône calendrier. **Planifié** réserve le créneau ; le
collaborateur désigné utilise **Confirmer ma prise en charge** pour passer à
**Validé**. Après l’entretien, **Enregistrer la réalisation** conserve son compte
rendu et passe à **Réalisé**. **Planifier la prochaine action** ouvre le formulaire
habituel avec le prospect déjà choisi.

Un report ou une réaffectation demande un motif et une nouvelle confirmation du
collaborateur. L’annulation libère le créneau et rend les anciens rappels caducs.
Si la sollicitation du prospect est bloquée, l’alerte reste visible et le
rendez-vous doit être traité explicitement.

**Mes notifications** rassemble les nouvelles affectations et les rappels ;
**Marquer comme lue** est distinct de la confirmation de prise en charge. Les
notifications WebPush et e-mail suivent vos **Préférences** et les canaux activés
sur la plateforme. La fiche du prospect n’est pas envoyée dans ces notifications.

### Se repérer dans les résultats

Les listes affichent le **nombre total de résultats correspondant aux filtres**,
la tranche consultée et la page : par exemple **26–50 sur 670 résultats**, puis
**Page 2 sur 27 · 25 par page**. Les flèches précédente/suivante sont désactivées
aux bornes ; leur nom reste accessible au clavier et aux lecteurs d’écran.
Une recherche sans résultat indique **0 résultat**.

Le total est calculé au chargement de la recherche. Survolez le compteur pour
voir sa date ; utilisez **Actualiser** pour le recalculer après les modifications
d’un autre gestionnaire. Les filtres relancent une recherche en première page.
La même présentation s’applique aux listes de suivi, rappels, contacts, échanges,
évaluations et imports. Une erreur en changeant de page conserve les résultats
déjà affichés ; vous pouvez réessayer la flèche.

### Ajouter une fiche

1. Choisissez **Nouveau prospect**. Saisissez son nom et son type. Recherchez puis sélectionnez sa **commune en Nouvelle-Aquitaine** : elle est obligatoire. Les autres coordonnées peuvent être complétées plus tard.
2. Choisissez le périmètre et l’objectif du premier dossier : souscription Animation, partenariat commerçant Coffrets ou achat entreprise/CSE. Affectez un responsable.
3. Enregistrez. Le prospect et son premier dossier sont créés ensemble. Une fiche ressemblante demande un examen explicite ; ouvrez la fiche existante si elle représente la même structure.
4. Ajoutez les personnes à contacter dans **Contacts**. Un contact devenu obsolète garde son historique.
5. Utilisez **Noter un échange** pour consigner une note, un appel, un rendez-vous ou un e-mail déjà réalisé. Cette action n’envoie aucun message au prospect. Une correction reste liée à l’échange d’origine.
6. **Planifier une action** précise le responsable, l’échéance et le rappel, en heure de Paris. Une préparation interne ne sollicite personne ; les autres actions précisent le canal et la structure ou le contact destinataire.

Une erreur d’enregistrement conserve la saisie. Après un conflit de version, consultez les dernières informations avant de réessayer. Après une réponse réseau incertaine, réessayez la même demande : sa clé empêche la création d’un doublon.

Dans **Historique des échanges**, les entrées issues de l’import CSV affichent
uniquement **Source : …**, à partir de l’**Origine du prospect**. Si elle n’est pas
renseignée, la mention est explicite. Le contexte documentaire détaillé reste
enregistré, sans être développé dans cette liste. Les échanges saisis manuellement
conservent leur texte, leur date, leur auteur et leur action de correction.

L'auteur d'un échange est affiché par son **prénom et son nom**, sur la fiche
prospect comme dans le détail d'un rappel. Le nom actuel reste visible si le
compte est désactivé ; si le compte est introuvable ou sans nom, la mention
**Utilisateur indisponible** remplace l'identifiant technique. L'identité
enregistrée dans l'audit est conservée.

La saisie est actuellement limitée aux douze départements de Nouvelle-Aquitaine :
16, 17, 19, 23, 24, 33, 40, 47, 64, 79, 86 et 87. Les anciennes fiches hors région
ou sans commune restent consultables ; leurs contacts, coordonnées de contact et
suivi restent modifiables. Pour modifier leur adresse, code postal ou commune,
sélectionnez une commune de Nouvelle-Aquitaine. Le serveur vérifie la commune
sélectionnée dans le référentiel ; un code postal seul ne suffit pas.

### Compléter la qualification progressivement

La fiche propose **Compléter la qualification**, puis des sections repliables
**Identité**, **Territoire**, **Évaluations du potentiel** et **Activité**. Renseignez
seulement ce que vous connaissez : ces compléments restent facultatifs pour créer
une fiche, noter un échange ou planifier un rappel. Un nombre inconnu reste vide ;
**0** signifie un comptage effectivement nul.

- **Identité et activité** : distinguez commune/EPCI, personne morale/établissement,
  puis renseignez les identifiants et l’activité utiles. Un SIREN/SIRET saisi ne
  certifie pas son existence ; une ressemblance demande un examen explicite.
- **Contacts** : précisez personne, service ou accueil générique, rôle commercial
  et fiabilité. **Vérifié** exige une date et une source. Modifier les coordonnées
  peut imposer une nouvelle vérification ; ce statut ne lève aucune opposition.
- **Projet Animation** : depuis son dossier, **Qualifier le projet** permet de
  préciser besoin, contact porteur, prochaine opération, calendrier et budget.
  Portage et budget confirmés demandent date et preuve ; un porteur **À revalider**
  doit être revérifié. Sans dates, le calendrier reste « À qualifier ». Ces valeurs
  concernent ce dossier ; elles ne changent ni son étape ni les autres dossiers.
- **Potentiel** : créez une évaluation datée avec sa source, enregistrez un
  brouillon partiel puis confirmez les blocs documentés. L’historique est paginé ;
  sélectionnez deux observations pour les comparer. **Utiliser comme référence**
  choisit séparément les **Comptages**, la **Population** ou les **Compétences**.
  Une correction d’observation confirmée crée une révision et conserve l’original.
  Le résumé affiche le comptage retenu, sa base documentaire/terrain, sa date et
  son classement ; les nouvelles observations restent à examiner. Choisir la
  référence d’un bloc marque ses observations actuelles comme examinées ;
  leur historique reste conservé. Une nouvelle observation ou confirmation
  postérieure réaffiche l’indicateur pour ce bloc.
- **Territoire** : renseignez l’appartenance d’une commune à un EPCI avec sa date
  d’effet et sa source ; un remplacement conserve l’historique. La fiche EPCI
  présente ses membres actuels. Dans un dossier Animation, ajoutez ou retirez
  les communes couvertes par lots de 100, ou remplacez explicitement la couverture.
  Une ancienne référence devenue obsolète demande une observation correspondant
  à la couverture actuelle. Cette couverture ne déplace pas le point sur la carte.

Les **Autres filtres** de Prospects, Suivi et Carte permettent de cibler potentiel,
territoire, activité, besoin, porteur, budget, fiabilité et données à examiner.
Ils sont conservés dans l’URL. Les règles et preuves attendues sont détaillées
dans la [qualification structurée](qualification-structuree.md).

## 3. Suivre les dossiers

**Suivi** filtre les dossiers par périmètre et étape. Depuis un dossier, **Changer d’étape** accompagne sa progression : À contacter, En discussion, Proposition, Gagné, Perdu ou En pause.

- Une pause demande un motif et une date de réexamen.
- Une perte demande un motif ; la réouverture est explicite et motivée.
- Un gain exige une référence métier existante, rattachée et vérifiée. Il ne crée ni vente, ni souscription, ni accès commerçant. Une preuve ne peut faire gagner qu’un dossier.

Les références proviennent des espaces métier existants : souscription Animation activée payée ou gratuite, achat coffrets professionnel payé, ou acceptation OnBoard avec activation Coffrets attestée. Les droits CRM ne donnent pas automatiquement accès à ces données métier.

Dans **Rappels**, le filtre **Rappel disponible** retrouve les actions dont l’heure de rappel est atteinte, même si leur échéance est future. Ce suivi interne fonctionne sans activer e-mail ou WebPush. Ouvrez une action pour la terminer avec son résultat, la reporter, la réaffecter ou l’annuler. Les anciennes révisions de rappel deviennent inéligibles. Une notification déjà remise au transport peut néanmoins arriver.

Le filtre **Responsable** utilise une liste facultative, sans champ de recherche
supplémentaire. **Tous les responsables** retire ce filtre. Si la liste comporte
plusieurs pages, **Charger d’autres responsables** complète les choix sans perdre
la sélection ; cliquez sur **Afficher** pour appliquer vos filtres.

Pour retrouver les actions d'une journée, choisissez **Date de l’action** avec
le bouton calendrier puis cliquez sur **Afficher**. Le filtre utilise la date
prévue de l'action, en heure de Paris, et se combine avec le type et le
responsable. Effacez la date puis cliquez sur **Afficher** pour revenir à toutes
les dates. Votre sélection est conservée lorsque vous actualisez la page.

**E71-EVOL-07 — implémenté localement le 6 novembre, déploiement à effectuer :**
les champs sont nommés **Action prévue le** (quand réaliser l’action) et **Me rappeler le** (quand
recevoir le rappel). À la création, sans date de rappel, celui-ci est fixé à la
date de l’action ; il peut être avancé, jamais placé après l’action. Exemple :
appel vendredi à 14 h, rappel vendredi à 9 h. Ces libellés ne changent pas les
préférences WebPush/e-mail ni le responsable qui reçoit le rappel. Lors d’un
report, les deux dates sont préremplies et obligatoires : choisissez explicitement
la date du nouveau rappel. Une erreur conserve la saisie et indique le champ à
corriger.

## 4. Utiliser la carte

**Carte** présente les prospects de **Nouvelle-Aquitaine**, regroupés par commune.
Choisissez un **Département**, puis **Filtrer** : la carte se recadre et conserve
vos autres filtres de prospection. **Réinitialiser** revient à toute la région,
et **Recentrer** retrouve la zone choisie après un déplacement ou un zoom.

Le sélecteur **Colorer par** propose deux lectures :

- **Priorité commerciale** : les niveaux calculés actuels, avec les mêmes
  couleurs que Qualification. **Non calculé**, **À recalculer** et **Profil de
  priorité non disponible** restent visibles. Le filtre **Priorité du dossier**
  désigne séparément la priorité manuelle Haute/Normale. Les niveaux dépendent
  des filtres de dossiers : Gagnée ou Coffrets peut donner Non calculé si aucun
  résultat de qualification compatible n’est disponible.
- **Responsable du prospect** : une couleur stable par collaborateur. Le
  responsable retenu est celui de la fiche prospect. **Non attribué** est
  distinct ; **À réaffecter** signale un responsable qui n’est plus éligible.

Changer de lecture conserve les filtres et la position de la carte ; l’URL
permet de retrouver ce choix après rechargement. Une commune mixte présente
des segments proportionnels. La légende indique le nom et le nombre de
prospects de chaque catégorie parmi les communes affichées ; les détails du
point et la liste des communes permettent aussi de lire la répartition.

Au-delà de 24 responsables, les autres sont réunis sous **Autres responsables**,
avec leurs effectifs et le nombre de collaborateurs regroupés. Affinez par
département ou responsable pour les détailler. Les couleurs restent stables
après filtrage ; les noms distinguent les teintes proches dans une grande équipe.

Un point représente le centre approximatif de la commune, pas l’adresse d’une
personne. Cliquez sur un groupe pour ouvrir les prospects correspondants.
**Voir la liste avec ces filtres** conserve la région, le département et vos
filtres commerciaux. La rubrique générale **Prospects** reste utilisable pour
tous les territoires. Les compteurs distinguent structures et dossiers.

Les prospects sans commune restent accessibles dans une liste dédiée **tous
territoires** : leur département ne peut pas encore être déterminé. Depuis une
fiche, **Localiser la commune** permet de chercher puis choisir explicitement la
commune de Nouvelle-Aquitaine et son code INSEE. Si le fond de carte est indisponible, le filtre par
département et la liste des communes restent disponibles. Aucun contact ni
contenu de note n’est transmis au fournisseur cartographique.

Après un import CSV, les points sont alimentés automatiquement à partir des codes
INSEE. La carte indique les prospects **en attente de localisation automatique**
sans les confondre avec ceux sans commune. Laissez passer un traitement puis
rechargez la carte ; les fiches sont déjà consultables dans la liste. Si un code
ancien ou inconnu reste introuvable, utilisez **Localiser la commune** sur la fiche.
La vue régionale affiche au maximum **500 communes** : zoomez ou choisissez un
département pour retrouver les autres points.

## 5. Importer votre fichier Excel

Depuis **Aujourd’hui → Importer mes prospects**, choisissez le **Format du fichier**
puis téléchargez son modèle CSV. Le **format 1 reste sélectionné par défaut** et
conserve ses 21 colonnes. Choisissez explicitement le **format 2** pour les
compléments structurés : son [modèle](modele-import-qualification-v2.csv) comporte
85 colonnes, dont 64 nouvelles facultatives. Vous pouvez omettre les colonnes
facultatives ; il n’est pas nécessaire de remplir 85 cellules par prospect.
Exportez depuis Excel en UTF-8, séparateur `;`, avec des références stables.
La limite reste de 10 Mio et 10 000 lignes. Le [dictionnaire complet](import-carte.md)
fournit les valeurs et exemples ; le choix INIT/UPSERT est indépendant du format.

**Importer des prospects seuls :** renseignez leur référence, nom, commune et les
contacts/notes utiles. Laissez vides les colonnes du dossier (`opportunite_ref`,
`perimetre`, titre, objectif et qualification de projet), ou omettez-les. Les
comptages et observations du format 2 restent conservés. Aucun dossier
« Qualification… » n’est créé automatiquement. Retrouvez ces fiches dans
**Prospects**, puis utilisez **Ajouter un dossier** lorsqu’un projet se précise.
**Suivi** affiche les dossiers existants ; un filtre de périmètre de dossier
écarte les prospects qui n’en ont pas encore.

1. Créez une **source** stable, par exemple `prospection-gironde`, puis réutilisez-la pour chaque mise à jour du même fichier. Les boutons **Sources suivantes/précédentes** donnent accès aux autres sources en conservant votre sélection.
2. Choisissez **INIT** pour créer uniquement les groupes inconnus ou **UPSERT** pour compléter les informations vides non protégées et ajouter des contacts/dossiers.
3. Renseignez `code_insee` pour chaque nouveau prospect (commune de Nouvelle-Aquitaine). Le responsable des nouveaux dossiers est facultatif : conservez **Non attribué** pour les affecter plus tard, ou choisissez un responsable habilité. Aucune affectation automatique à la personne qui importe ; les responsables des dossiers déjà présents sont conservés. Déposez le fichier. Aucun prospect n’est encore créé.

   Si le message demande le modèle CSV alors que votre fichier comporte les
   colonnes de qualification du modèle à 85 colonnes, vérifiez d'abord le choix
   **Format 2** dans **Format du fichier**. Le diagnostic `FORMAT_2_REQUIS` indique
   ce cas explicitement ; réenvoyez le même fichier avec le bon format.

4. Examinez l’aperçu et les ressemblances : rapprochez une fiche existante, confirmez une fiche distincte ou excluez le groupe. Le format 2 distingue aussi compléments, valeurs conservées, observations et références proposées. Si plusieurs observations peuvent devenir la première référence d’un bloc, utilisez **Choisir la référence** pour ce bloc. Une référence déjà retenue reste conservée ; les nouvelles données seront à examiner dans la fiche. Les anomalies indiquent leur motif et les numéros des lignes CSV. Corrigez le fichier puis déposez un nouveau lot avec la même source si nécessaire. Si les données changent entre-temps, un nouvel examen est nécessaire.
5. Confirmez le plan. Actualisez l’écran pour suivre le traitement en arrière-plan. Gardez l’URL directe `/internal/crm/imports/<identifiant>` et téléchargez son rapport. Cette destination est conservée après reconnexion.
6. Un traitement interrompu peut être repris par son confirmateur ; les groupes déjà validés ne sont pas rejoués. Les autres personnes habilitées peuvent consulter le lot, mais les actions réservées au confirmateur ne leur sont pas proposées.

Le traitement des imports est planifié chaque minute dans l’ordonnanceur partagé.
Il prépare l’aperçu avant votre confirmation, puis applique les groupes confirmés.
Si le lot reste durablement en **Analyse du fichier** ou **Import en cours**, faites
vérifier **Traitement des imports CSV du CRM** dans la supervision des batchs.
Actualiser l’écran consulte l’avancement ; cela ne déclenche pas le traitement.

UPSERT n’écrase pas les notes, étapes, responsables, rappels, oppositions ni les champs corrigés ou volontairement vidés à la main. Les statuts et leurs preuves sont conservés ensemble ; une cellule différente ne remplace pas un budget confirmé, un porteur ou une vérification de contact. L’absence d’une ligne dans le nouveau fichier ne supprime rien. En INIT, un prospect déjà connu par sa référence source est ignoré avec tout son groupe, y compris ses nouveaux compléments de qualification.

## 6. Régler les rappels et respecter les oppositions

**Aujourd’hui → Préférences de rappel** permet d’activer les canaux disponibles. Le WebPush demande aussi l’autorisation du navigateur et l’activation de cet appareil. L’e-mail utilise exclusivement l’adresse vérifiée de votre compte interne ; il ne contacte jamais le prospect. L’activation ne provoque pas de rattrapage des anciens rappels. Les notifications restent génériques pour protéger les informations sur l’écran verrouillé.

Dans la fiche prospect, **Gestion et oppositions → Ne plus solliciter** enregistre une demande concernant la structure ou un contact. Les sollicitations concernées sont bloquées, y compris lorsqu’une coordonnée opposée est réutilisée. La préparation interne reste possible. Seul un utilisateur habilité à administrer le CRM peut lever l’opposition, avec motif et source. Archiver puis réactiver une fiche ne lève pas l’opposition.

## 7. Vérifier les informations d’un prospect

Depuis la fiche, choisissez **Vérifier les données**. Sélectionnez les blocs
souhaités puis lancez la vérification. Vous pouvez quitter la page : le traitement
continue et son historique reste accessible sur le prospect.

Pour évaluer le territoire d'un projet précis, ouvrez **Évaluer la couverture
d’un dossier** et choisissez son dossier Animation. Pour un commerce ou une
association, cette couverture est nécessaire au comptage territorial ; elle
doit déjà avoir été renseignée sur le dossier.

Le bilan distingue les sources disponibles, absentes ou momentanément
indisponibles. Pour chaque proposition, comparez **Valeur actuelle** et **Valeur
trouvée**, avec sa source et ses dates. Choisissez **Conserver ma valeur** ou
**Utiliser la valeur trouvée**, puis **Appliquer mes choix**. Une correction
protégée demande une confirmation supplémentaire, y compris si vous l’aviez vidée.
Changer de page n’applique pas les choix en cours.

Les nouvelles observations de potentiel sont des **brouillons**. Dans la fiche,
ouvrez **Évaluations du potentiel**, vérifiez puis confirmez l’observation et
choisissez explicitement la référence souhaitée. Une vérification documentaire
ne prouve ni un passage sur le terrain ni l’identité du décideur.

Si la fiche change pendant la comparaison, relancez la vérification ; les
modifications concurrentes ne sont pas écrasées. En cas d’erreur de réseau,
réessayez la même demande : elle conserve sa clé et son résultat déjà enregistré.
L’environnement doit avoir activé la fonction et préparé ses sources.

## 8. Repérer les prospects prioritaires

Le menu **Qualification** permet de chercher les communes ou intercommunalités,
de filtrer par département et de préparer un calcul sur **tous les résultats**,
même au-delà de la page affichée. Vérifiez le nombre exact de prospects avant
de confirmer. Le lot possède une URL de suivi ; les succès sont conservés lors
d’une interruption et les conflits demandent une nouvelle préparation.

Le filtre **Département** propose une liste des douze départements de
Nouvelle-Aquitaine, avec numéro et nom (par exemple **33 · Gironde**).
**Tous les départements** retire ce filtre. La sélection est conservée dans
l'URL, après actualisation et lors du passage entre liste et carte.

Le potentiel prime : une commune avec au moins 10 commerces ou un EPCI avec au
moins 50 peut être prioritaire même sans projet ni contact identifié. Les niveaux
intermédiaires commencent à 5 et 20. Le projet et la fiabilité servent à préciser
les prochaines actions, sans transformer une donnée inconnue en zéro.

La **Carte des priorités commerciales**, accessible aussi depuis Carte, reprend
ces niveaux avec couleurs et libellés. Un groupe peut contenir plusieurs niveaux ;
sa répartition reste visible. Les prospects non localisés sont comptés séparément.
Une preuve expirée ou modifiée est signalée **À recalculer** sur l’axe concerné :
un contact à revalider ne supprime pas un potentiel encore courant.

Depuis **Pourquoi ce niveau ?**, un gestionnaire peut **Attester un fait actuel** :
choisir l'information, indiquer la date de vérification et sa référence, puis
confirmer. Une absence connue est distincte d'une information non recherchée.
Cette attestation ne recalcule pas automatiquement le classement.

Si le territoire d'un prospect ou la composition d'un EPCI change, vérifiez
à nouveau le comptage puis choisissez sa référence. Recalculer seul ne rend
pas valide un comptage établi sur l'ancien territoire.

## En cas de difficulté

Conservez le message et l’identifiant de corrélation lorsqu’il est affiché. Pour un import, conservez aussi son URL et son rapport privé. Ne communiquez pas de mot de passe, de lien d’invitation ou de coordonnées prospect dans un journal technique. Un accès retiré efface les données visibles et demande une nouvelle vérification de session.
