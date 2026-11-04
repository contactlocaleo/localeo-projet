# Prendre en main Localeo CRM

[Spécification](README.md) · [Format CSV](import-carte.md) · [Exploitation](exploitation.md).

Localeo CRM suit vos relations commerciales Animation et Coffrets. Il utilise votre compte interne Localeo. Une fiche représente une structure ; ses contacts, échanges et dossiers restent réunis même lorsqu’elle s’intéresse aux deux offres.

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

1. Choisissez **Nouveau prospect**. Saisissez son nom et son type. Recherchez puis sélectionnez sa **commune en Nouvelle-Aquitaine** : elle est obligatoire. Les autres coordonnées peuvent être complétées plus tard.
2. Choisissez le périmètre et l’objectif du premier dossier : souscription Animation, partenariat commerçant Coffrets ou achat entreprise/CSE. Affectez un responsable.
3. Enregistrez. Le prospect et son premier dossier sont créés ensemble. Une fiche ressemblante demande un examen explicite ; ouvrez la fiche existante si elle représente la même structure.
4. Ajoutez les personnes à contacter dans **Contacts**. Un contact devenu obsolète garde son historique.
5. Utilisez **Noter un échange** pour consigner une note, un appel, un rendez-vous ou un e-mail déjà réalisé. Cette action n’envoie aucun message au prospect. Une correction reste liée à l’échange d’origine.
6. **Planifier une action** précise le responsable, l’échéance et le rappel, en heure de Paris. Une préparation interne ne sollicite personne ; les autres actions précisent le canal et la structure ou le contact destinataire.

Une erreur d’enregistrement conserve la saisie. Après un conflit de version, consultez les dernières informations avant de réessayer. Après une réponse réseau incertaine, réessayez la même demande : sa clé empêche la création d’un doublon.

La saisie est actuellement limitée aux douze départements de Nouvelle-Aquitaine :
16, 17, 19, 23, 24, 33, 40, 47, 64, 79, 86 et 87. Les anciennes fiches hors région
ou sans commune restent consultables ; leurs contacts, coordonnées de contact et
suivi restent modifiables. Pour modifier leur adresse, code postal ou commune,
sélectionnez une commune de Nouvelle-Aquitaine. Le serveur vérifie la commune
sélectionnée dans le référentiel ; un code postal seul ne suffit pas.

## 3. Suivre les dossiers

**Suivi** filtre les dossiers par périmètre et étape. Depuis un dossier, **Changer d’étape** accompagne sa progression : À contacter, En discussion, Proposition, Gagné, Perdu ou En pause.

- Une pause demande un motif et une date de réexamen.
- Une perte demande un motif ; la réouverture est explicite et motivée.
- Un gain exige une référence métier existante, rattachée et vérifiée. Il ne crée ni vente, ni souscription, ni accès commerçant. Une preuve ne peut faire gagner qu’un dossier.

Les références proviennent des espaces métier existants : souscription Animation activée payée ou gratuite, achat coffrets professionnel payé, ou acceptation OnBoard avec activation Coffrets attestée. Les droits CRM ne donnent pas automatiquement accès à ces données métier.

Dans **Rappels**, le filtre **Rappel disponible** retrouve les actions dont l’heure de rappel est atteinte, même si leur échéance est future. Ce suivi interne fonctionne sans activer e-mail ou WebPush. Ouvrez une action pour la terminer avec son résultat, la reporter, la réaffecter ou l’annuler. Les anciennes révisions de rappel deviennent inéligibles. Une notification déjà remise au transport peut néanmoins arriver.

## 4. Utiliser la carte

**Carte** présente les prospects de **Nouvelle-Aquitaine**, regroupés par commune.
Choisissez un **Département**, puis **Filtrer** : la carte se recadre et conserve
vos autres filtres de prospection. **Réinitialiser** revient à toute la région,
et **Recentrer** retrouve la zone choisie après un déplacement ou un zoom.

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

## 5. Importer votre fichier Excel

Depuis **Aujourd’hui → Importer mes prospects**, téléchargez le modèle CSV. Exportez votre fichier Excel en UTF-8, séparateur `;`, avec les 21 colonnes du modèle et des références stables. La limite est de 10 Mio et 10 000 lignes. Le [dictionnaire complet](import-carte.md) fournit les valeurs et exemples.

1. Créez une **source** stable, par exemple `prospection-gironde`, puis réutilisez-la pour chaque mise à jour du même fichier. Les boutons **Sources suivantes/précédentes** donnent accès aux autres sources en conservant votre sélection.
2. Choisissez **INIT** pour créer uniquement les groupes inconnus ou **UPSERT** pour compléter les informations vides non protégées et ajouter des contacts/dossiers.
3. Renseignez `code_insee` pour chaque nouveau prospect (commune de Nouvelle-Aquitaine). Choisissez le responsable des nouveaux dossiers et déposez le fichier. Aucun prospect n’est encore créé.
4. Examinez l’aperçu et les ressemblances : rapprochez une fiche existante, confirmez une fiche distincte ou excluez le groupe. Les anomalies indiquent leur motif et les numéros des lignes CSV. Corrigez le fichier puis déposez un nouveau lot avec la même source si nécessaire. Si les données changent entre-temps, un nouvel examen est nécessaire.
5. Confirmez le plan. Actualisez l’écran pour suivre le traitement en arrière-plan. Gardez l’URL directe `/internal/crm/imports/<identifiant>` et téléchargez son rapport. Cette destination est conservée après reconnexion.
6. Un traitement interrompu peut être repris par son confirmateur ; les groupes déjà validés ne sont pas rejoués. Les autres personnes habilitées peuvent consulter le lot, mais les actions réservées au confirmateur ne leur sont pas proposées.

UPSERT n’écrase pas les notes, étapes, responsables, rappels, oppositions ni les champs corrigés ou volontairement vidés à la main. L’absence d’une ligne dans le nouveau fichier ne supprime rien.

## 6. Régler les rappels et respecter les oppositions

**Aujourd’hui → Préférences de rappel** permet d’activer les canaux disponibles. Le WebPush demande aussi l’autorisation du navigateur et l’activation de cet appareil. L’e-mail utilise exclusivement l’adresse vérifiée de votre compte interne ; il ne contacte jamais le prospect. L’activation ne provoque pas de rattrapage des anciens rappels. Les notifications restent génériques pour protéger les informations sur l’écran verrouillé.

Dans la fiche prospect, **Gestion et oppositions → Ne plus solliciter** enregistre une demande concernant la structure ou un contact. Les sollicitations concernées sont bloquées, y compris lorsqu’une coordonnée opposée est réutilisée. La préparation interne reste possible. Seul un utilisateur habilité à administrer le CRM peut lever l’opposition, avec motif et source. Archiver puis réactiver une fiche ne lève pas l’opposition.

## En cas de difficulté

Conservez le message et l’identifiant de corrélation lorsqu’il est affiché. Pour un import, conservez aussi son URL et son rapport privé. Ne communiquez pas de mot de passe, de lien d’invitation ou de coordonnées prospect dans un journal technique. Un accès retiré efface les données visibles et demande une nouvelle vérification de session.
