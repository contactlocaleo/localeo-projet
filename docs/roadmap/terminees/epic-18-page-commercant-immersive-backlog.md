# Backlog Epic 18 - Page commercant immersive

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Perimetre

Epic source : `Epic 18. Page commercant immersive`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : transformer la fiche commercant en page publique et mobile plus humaine, plus immersive et plus actionnable, tout en gardant un cadre de moderation avant publication.

## Statut global

- Epic 18 : `Termine`
- Avancement : cadrage produit initialise. Aucun modele de donnees dedie n'est encore implemente.

## Vision produit

La page commercant doit donner envie de rencontrer le partenaire, pas seulement afficher une ligne de catalogue. Elle doit raconter le commerce, montrer l'ambiance, expliquer ce qui rend l'experience locale interessante et rassurer avant l'achat ou l'utilisation d'un coffret.

Principes :
- mettre en avant l'humain derriere le commerce ;
- separer les donnees publiques, operationnelles et sensibles ;
- permettre une edition progressive par le commercant depuis l'application mobile ;
- moderer les contenus editoriaux avant exposition publique ;
- reutiliser les signaux deja produits par Localeo : prestations, feed d'activite, feedbacks, validations, ville et coffrets ;
- eviter d'exposer des donnees personnelles ou contractuelles inutiles.

## Surfaces ciblees

### Marketplace publique

Objectif : presenter un commercant actif avec une page riche et rassurante.

Contenus attendus :
- hero image ou portrait ;
- accroche courte ;
- presentation humaine ;
- specialites et ambiance ;
- prestations disponibles via les coffrets ;
- signaux d'activite locale ;
- agregats de feedbacks moderes ;
- informations pratiques utiles.

### Back-office

Objectif : permettre a Localeo de creer, enrichir, relire et moderer la fiche.

Contenus attendus :
- vision complete des champs publics et operationnels ;
- statut de completion ;
- statut de moderation ;
- historique des modifications sensibles ;
- actions de validation, refus, masquage ou remise en brouillon.

### Application mobile commercant

Objectif : permettre au commercant de maintenir progressivement sa fiche sans donner acces aux champs sensibles.

Contenus attendus :
- consultation de sa fiche ;
- modification des champs operationnels autorises ;
- proposition de contenus publics soumis a moderation ;
- preview mobile avant soumission ;
- suivi du statut de moderation.

## Donnees actuelles disponibles

Le modele `Commercant` contient deja :
- `nom` ;
- `ville_id` ;
- `type_commercant_id` ;
- `description` ;
- `statut` ;
- `image_uri` ;
- `contact_nom` ;
- `contact_prenom` ;
- `contact_email` ;
- `contact_telephone` ;
- `date_referencement`.

Relations utiles :
- prestations rattachees au commercant ;
- validations de prestation ;
- feedbacks prestation ;
- activites locales ;
- comptes bancaires et acces commercant cote back-office uniquement.

## Donnees recommandees

### Profil public

Champs recommandes :
- `accroche_courte` : phrase courte affichee en haut de page ;
- `presentation_longue` : texte humain et immersif ;
- `portrait_image_uri` : URI d'une image issue de la bibliotheque d'images existante ;
- `galerie_images` : liste ordonnee d'URI issues de la bibliotheque d'images existante ;
- `specialites` : tags editoriaux, par exemple `fait maison`, `produits locaux`, `artisanat` ;
- `ambiance` : tags d'experience, par exemple `convivial`, `familial`, `calme`, `festif` ;
- `ce_qui_rend_unique` : texte court sur la singularite du commerce ;
- `conseil_du_commercant` : recommandation personnelle ;
- `bon_a_savoir` : informations pratiques non contractuelles ;
- `personne_a_rencontrer` : prenom ou formule publique, sans exposer le contact administratif complet.

### Informations pratiques

Champs recommandes :
- `adresse_affichage` ;
- `latitude` ;
- `longitude` ;
- `horaires_texte` en V1 ;
- structure horaires dediee en V2 ;
- `site_web_url` ;
- `instagram_url` ;
- `facebook_url` ;
- `reservation_url` ;
- `telephone_public` si distinct du telephone operationnel ;
- `email_public` si distinct de l'email de login.

### Liens publics et reseaux sociaux

Les liens publics proposes par le commercant doivent etre verifies avant publication.

Regles :
- verifier manuellement par un admin Localeo `site_web_url`, `instagram_url`, `facebook_url` et `reservation_url` avant publication ;
- ne pas prevoir de controle automatique d'accessibilite ou de rattachement en V1 ;
- refuser les URLs au mauvais format, trompeuses ou non rattachees clairement au commerce selon le controle admin ;
- ne publier un lien qu'apres validation par un admin Localeo ;
- stocker le resultat de verification dans la demande ou la version ;
- afficher un motif exploitable si un lien est refuse.

### Gouvernance et moderation

Champs recommandes :
- `profil_publication_statut` : `BROUILLON`, `A_MODERER`, `PUBLIEE`, `REFUSEE`, `ARCHIVEE`, `MASQUEE` ;
- `profil_modere_at` ;
- `profil_modere_par` ;
- `profil_motif_refus` ;
- `derniere_mise_a_jour_par_commercant_at` ;
- `derniere_mise_a_jour_par_commercant_id` nullable ;
- `score_completion_profil` calcule a la volee, non persiste en V1 ;
- `version_profil_public` pour tracer les revisions.

### Photos et bibliotheque d'images

Les photos de la page commercant utilisent la galerie d'images deja implementee.

Regles :
- ne pas creer de stockage image dedie a la page commercant ;
- referencer les images via les `image_uri` existants ;
- s'appuyer sur `media_assets`, l'API image et la bibliotheque d'images SQLAdmin existantes ;
- permettre au commercant d'uploader ou selectionner des images dans un etat non publie ;
- stocker dans la version de fiche uniquement les references et l'ordre d'affichage ;
- toute photo proposee pour publication doit etre validee par un admin Localeo avant exposition publique ;
- moderer la selection et l'ordre des images comme partie de la version editoriale ;
- ne pas exposer publiquement une image ajoutee a une proposition tant que la version de fiche n'est pas approuvee.

## Versioning de publication

Le versioning V1 concerne uniquement les champs modifiables par le commercant et soumis a moderation. Les champs structurants sous controle Localeo ne sont pas versionnes dans un premier temps.

Le contenu editorial/moderable de la fiche commercant doit distinguer explicitement :
- la version publiee, validee et visible publiquement ;
- la version brouillon ou proposee, en cours de preparation ou d'approbation ;
- l'historique des versions et decisions sur ces champs moderables.

Objectif principal : une mise a jour refusee ne doit jamais desactiver le commercant, ni masquer la version deja publiee.

Regles obligatoires :
- les statuts de version sont fixes en V1 : `BROUILLON`, `A_MODERER`, `PUBLIEE`, `REFUSEE`, `ARCHIVEE`, `MASQUEE` ;
- la page publique lit les champs structurants depuis `commercants` et les champs editoriaux depuis la derniere version `PUBLIEE` ;
- une proposition `A_MODERER` ne remplace jamais la version publiee tant qu'elle n'est pas approuvee ;
- la granularite de versioning est la fiche editoriale complete, pas chaque attribut pris individuellement ;
- chaque version contient un snapshot complet des champs editoriaux/moderables de la fiche, meme si la demande ne modifie qu'un seul champ ;
- un refus passe uniquement la proposition en `REFUSEE` avec motif ;
- le refus d'une proposition ne modifie pas `CommercantOrm.statut` ;
- le refus d'une proposition ne modifie pas les champs structurants sous controle Localeo ;
- le refus d'une proposition ne modifie pas la version editoriale publiee courante ;
- un commercant `ACTIF` avec une version publiee doit rester visible meme si une future version est refusee ;
- si aucune version publiee n'existe, la page marketplace publique reste non publiee ;
- le fallback minimal depuis `commercants` est autorise uniquement en back-office et en preview authentifiee ;
- l'approbation cree une nouvelle version publiee des champs moderables et archive l'ancienne version editoriale comme version precedente ;
- une seule proposition active `BROUILLON` ou `A_MODERER` est autorisee par commercant en V1, sauf decision contraire.
- l'historique conserve uniquement les 3 dernieres versions de page commercant par profil ;
- la purge des anciennes versions est declenchee lors de la creation d'une nouvelle version ;
- la purge ne doit jamais supprimer la version `PUBLIEE` courante ni la proposition active `BROUILLON` ou `A_MODERER` ;
- si la conservation stricte des 3 dernieres versions entre en conflit avec la protection de la version publiee ou de la proposition active, la protection des versions actives prime et la purge ne supprime que les versions historiques purgeables.

Champs hors versioning V1 :
- `nom` ;
- `ville_id` ;
- `type_commercant_id` ;
- `statut` ;
- `contact_email` si utilise comme login ;
- donnees bancaires ;
- rattachements coffrets et prestations ;
- montants de reversement ;
- tout champ operationnel que Localeo decide de conserver sous controle back-office direct.

Modele recommande :
- table racine `profils_commercants`, dediee a la fiche immersive d'un commercant ;
- table `profils_commercants_versions` pour les versions des champs editoriaux/moderables uniquement ;
- `profils_commercants.commercant_id` est unique et reference `commercants.id` ;
- `profils_commercants` porte l'etat courant de publication et les references vers la version publiee et la proposition active ;
- chaque ligne represente une version complete de la fiche editoriale moderable ;
- `profil_commercant_id` rattache la version au profil ;
- `commercant_id` peut etre duplique sur la version pour faciliter les requetes back-office et dashboard ;
- `numero_version` identifie l'ordre de publication ;
- `statut_version` : `BROUILLON`, `A_MODERER`, `PUBLIEE`, `REFUSEE`, `ARCHIVEE`, `MASQUEE` ;
- `statut_demande` expose l'etat lisible de la demande cote commercant : `BROUILLON`, `EN_ATTENTE_RELECTURE`, `APPROUVEE`, `REFUSEE`, `ANNULEE` ;
- `source_modification` : `BACKOFFICE`, `MOBILE_COMMERCANT`, `IMPORT` ;
- `verification_liens_statut` et `verification_photos_statut` : `A_VERIFIER`, `VALIDEE`, `REFUSEE`, `NON_REQUISE` ;
- les champs publics versionnes sont stockes en colonnes dediees, pas dans un objet JSON generique ;
- les colonnes de version contiennent le snapshot complet des champs publics moderables ;
- les differences entre versions sont calculees a la volee entre deux snapshots, sans colonne `champs_modifies` en V1 ;
- `soumis_at`, `soumis_par_type`, `soumis_par_id` ;
- `modere_at`, `modere_par`, `motif_refus` ;
- `publie_at`, `remplace_version_id` ;
- `decision_commentaire_public` : message court affichable au commercant en cas de refus ou demande de correction.

Colonnes SQL retenues pour `profils_commercants` :

```sql
CREATE TABLE profils_commercants (
  id UUID PRIMARY KEY,
  commercant_id UUID NOT NULL UNIQUE REFERENCES commercants(id),

  statut_publication TEXT NOT NULL,

  version_publiee_id UUID NULL,
  proposition_active_id UUID NULL,

  premiere_publication_at TIMESTAMP NULL,
  derniere_publication_at TIMESTAMP NULL,
  derniere_soumission_at TIMESTAMP NULL,
  derniere_moderation_at TIMESTAMP NULL,
  masque_at TIMESTAMP NULL,

  masque_par_admin_id TEXT NULL,
  motif_masquage TEXT NULL,

  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX uq_profils_commercants_commercant
ON profils_commercants (commercant_id);

CREATE INDEX idx_profils_commercants_statut_publication
ON profils_commercants (statut_publication);

CREATE INDEX idx_profils_commercants_version_publiee
ON profils_commercants (version_publiee_id);

CREATE INDEX idx_profils_commercants_proposition_active
ON profils_commercants (proposition_active_id);
```

`profils_commercants.statut_publication` decrit l'etat public global de la fiche et non le cycle detaille d'une version. Les statuts retenus sont :
- `NON_PUBLIE` ;
- `EN_ATTENTE_MODERATION` ;
- `PUBLIE` ;
- `MASQUE`.

`profils_commercants` ne stocke ni score de completion, ni contenu editorial, ni champs structurants Localeo. Il sert uniquement de racine fonctionnelle, d'etat courant et d'aiguillage vers `version_publiee_id` et `proposition_active_id`.

Creation initiale :
- `profils_commercants` est cree en migration massive pour les commercants existants ;
- la migration cree une ligne racine par `commercants.id` ;
- les profils crees par migration demarrent en `NON_PUBLIE` ;
- la migration ne genere aucune version editoriale `PUBLIEE` ;
- apres migration, tout nouveau commercant doit recevoir automatiquement son profil racine dans `profils_commercants` au moment de sa creation.

Colonnes SQL retenues pour `profils_commercants_versions` :

```sql
CREATE TABLE profils_commercants_versions (
  id UUID PRIMARY KEY,
  profil_commercant_id UUID NOT NULL REFERENCES profils_commercants(id),
  commercant_id UUID NOT NULL REFERENCES commercants(id),

  numero_version INTEGER NOT NULL,
  statut_version TEXT NOT NULL,
  statut_demande TEXT NOT NULL,
  source_modification TEXT NOT NULL,

  accroche_courte TEXT,
  presentation_longue TEXT,
  histoire_commercant TEXT,
  mot_du_commercant TEXT,

  specialites TEXT,
  ambiance TEXT,
  valeurs TEXT,
  labels_certifications TEXT,

  bon_a_savoir TEXT,
  horaires_texte TEXT,
  acces_transport TEXT,
  accessibilite TEXT,

  site_web_url TEXT,
  instagram_url TEXT,
  facebook_url TEXT,
  reservation_url TEXT,

  image_principale_uri TEXT,
  image_portrait_uri TEXT,
  image_ambiance_1_uri TEXT,
  image_ambiance_2_uri TEXT,
  image_ambiance_3_uri TEXT,

  verification_liens_statut TEXT,
  verification_liens_resume TEXT,
  verification_photos_statut TEXT,
  verification_photos_resume TEXT,

  motif_refus TEXT,
  decision_commentaire_public TEXT,
  commentaire_moderation_interne TEXT,

  cree_par_type TEXT NOT NULL,
  cree_par_id TEXT,
  soumis_at TIMESTAMP,
  soumis_par_type TEXT,
  soumis_par_id TEXT,
  modere_at TIMESTAMP,
  modere_par_admin_id TEXT,
  publie_at TIMESTAMP,
  remplace_version_id UUID REFERENCES profils_commercants_versions(id),

  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX uq_profils_versions_numero
ON profils_commercants_versions (profil_commercant_id, numero_version);

CREATE INDEX idx_profils_versions_commercant_statut
ON profils_commercants_versions (commercant_id, statut_version);

CREATE INDEX idx_profils_versions_a_moderer
ON profils_commercants_versions (statut_version, statut_demande);
```

Invariants domaine obligatoires :
- au plus une version `PUBLIEE` active par commercant ;
- au plus une proposition active `BROUILLON` ou `A_MODERER` par commercant ;
- au plus 3 versions historiques recentes sont conservees par profil apres creation d'une nouvelle version, hors versions protegees non purgeables ;
- ces deux regles doivent etre portees par le domaine applicatif avant d'etre portees par la base ;
- une version `REFUSEE` est immutable hors correction technique admin ;
- une version `REFUSEE` ne peut pas etre resoumise directement ;
- une resoumission apres refus se fait en dupliquant la version `REFUSEE` vers une nouvelle version `BROUILLON` ;
- les champs structurants et sensibles ne sont jamais stockes dans le contenu public versionne ;
- les images rattachees a une proposition restent non publiques tant que la version n'est pas approuvee ;
- le diff affiche en back-office ou dans l'espace commercant est calcule a la volee depuis une liste applicative de champs comparables, par exemple entre `version_publiee_id` et `proposition_active_id`.

Garde-fous PostgreSQL recommandes :
- ajouter un index unique partiel sur `commercant_id` pour les versions `PUBLIEE` non archivees ou non masquees, afin de proteger l'invariant "une seule version publiee active" ;
- ajouter un index unique partiel sur `commercant_id` pour les statuts `BROUILLON` et `A_MODERER`, afin de proteger l'invariant "une seule proposition active" ;
- ces index ne remplacent pas les validations de domaine et doivent etre traites comme une derniere barriere contre les races conditions ou insertions hors use case.

Transitions recommandees :
- `BROUILLON -> A_MODERER` : soumission par commercant ou admin ;
- `A_MODERER -> PUBLIEE` : approbation admin, avec archivage de l'ancienne version publiee ;
- `A_MODERER -> REFUSEE` : refus admin avec motif, sans impact public ;
- `PUBLIEE -> MASQUEE` : masquage volontaire de la fiche publique, distinct du statut commercant ;
- `MASQUEE -> PUBLIEE` : republication admin ;
- `PUBLIEE -> ARCHIVEE` : remplacement par une nouvelle version approuvee.

Droits V1 :
- commercant authentifie : editer un brouillon, soumettre une proposition, consulter le statut des demandes, generer une preview authentifiee ;
- admin Localeo : creer ou modifier une fiche, approuver, refuser, masquer et republier ;
- public : lire uniquement une version `PUBLIEE` exposee par la marketplace.

Evenements d'audit V1 :
- `PROFIL_BROUILLON_CREE` ;
- `PROFIL_SOUMIS_MODERATION` ;
- `PROFIL_APPROUVE` ;
- `PROFIL_REFUSE` ;
- `PROFIL_MASQUE` ;
- `PROFIL_REPUBLIE`.

## Edition mobile ciblee

### Champs modifiables librement

Ces champs peuvent etre ouverts rapidement au commercant, avec validation de format :
- `contact_nom` ;
- `contact_prenom` ;
- `contact_telephone` ;
- `horaires_texte` ;
- `bon_a_savoir` ;
- `conseil_du_commercant` ;
- liens reseaux sociaux publics.

### Champs soumis a moderation

Ces champs peuvent etre proposes par le commercant mais ne doivent pas etre publies automatiquement :
- `accroche_courte` ;
- `presentation_longue` ;
- `portrait_image_uri` ;
- `galerie_images` ;
- `specialites` ;
- `ambiance` ;
- `ce_qui_rend_unique` ;
- `telephone_public` ;
- `email_public`.

### Champs non modifiables depuis mobile en V1

Ces champs restent controles par Localeo :
- `nom` ;
- `ville_id` ;
- `type_commercant_id` ;
- `statut` ;
- `contact_email` si utilise comme login ;
- donnees bancaires ;
- rattachements coffrets et prestations ;
- montants de reversement.

## API publique recommandee

Endpoints :
- `GET /public/commercants/{commercant_id}/page`
- `GET /public/commercants/{commercant_id}/activites`
- `GET /public/commercants/{commercant_id}/feedbacks`

`GET /public/commercants/{commercant_id}/page` retourne :
- identite publique ;
- contenu editorial de la version publiee ;
- ville et type commercant ;
- photos publiques ;
- prestations actives rattachees ;
- coffrets actifs contenant ses prestations ;
- informations pratiques publiques ;
- agregats de feedbacks ;
- feed d'activite publique rattache.

Regles :
- retourner uniquement les commercants `ACTIF` avec une version editoriale `PUBLIEE` ;
- lire la version `PUBLIEE` courante, jamais une proposition `A_MODERER` ;
- ne pas exposer de page marketplace publique si aucune version editoriale n'a ete approuvee ;
- ne jamais exposer email de login, telephone operationnel prive, compte bancaire ou donnees de support ;
- ne pas exposer les contenus `A_MODERER`, `REFUSEE` ou `MASQUEE` ;
- prevoir des fallbacks publics uniquement pour des champs optionnels manquants dans une version deja `PUBLIEE`.

## API mobile commercant recommandee

Endpoints :
- `GET /commercants/me/page`
- `GET /commercants/me/page/demandes`
- `GET /commercants/me/page/demandes/{demande_id}`
- `GET /commercants/me/page/apercu`
- `GET /commercants/me/page/demandes/{demande_id}/apercu`
- `PATCH /commercants/me/page/contact`
- `PATCH /commercants/me/page/brouillon`
- `POST /commercants/me/page/soumettre-moderation`

Regles :
- authentification commercant obligatoire ;
- limiter les champs acceptes selon les categories ci-dessus ;
- rejeter explicitement les champs sensibles ;
- tracer les modifications et soumissions ;
- ne pas publier automatiquement les champs soumis a moderation ;
- sauvegarder les modifications editoriales dans une version brouillon/proposition distincte de la version publiee ;
- permettre au commercant de consulter l'etat de ses demandes de modification, y compris date de soumission, statut, decision et motif de refus public si applicable ;
- permettre au commercant de generer un apercu de la page depuis l'application commercant avant soumission ou pendant la moderation.

En V1, la preview est une preview authentifiee integree a l'application commercant. L'API retourne des donnees JSON consommables par l'app mobile ou le front commercant authentifie. Elle ne genere pas d'URL web publique partageable, meme non indexee.

`GET /commercants/me/page/apercu` retourne :
- donnees JSON de preview basees sur la proposition active si elle existe ;
- fallback sur la version publiee ou le profil minimal si aucune proposition active n'existe ;
- indicateur `preview=true` ;
- en-tete ou metadata `noindex` attendu cote frontend.

Regles de preview :
- l'apercu n'est pas une publication ;
- l'apercu n'est pas indexable ;
- l'apercu ne doit pas etre accessible sans session commercant valide ;
- l'apercu ne doit pas etre partageable via un lien public ou token public en V1 ;
- l'apercu peut afficher une proposition `BROUILLON`, `A_MODERER` ou `REFUSEE` au commercant rattache uniquement ;
- l'apercu doit afficher clairement que le contenu n'est pas encore public.

`GET /commercants/me/page/demandes` retourne :
- demandes recentes rattachees au commercant ;
- identifiant de demande ;
- numero de version ;
- statut lisible ;
- date de creation ;
- date de soumission ;
- date de decision ;
- champs modifies en resume ;
- indicateur `action_requise` si la demande est refusee ou a corriger.

`GET /commercants/me/page/demandes/{demande_id}` retourne :
- detail de la demande ;
- contenu propose ;
- comparaison avec la version publiee si elle existe ;
- motif de refus ou commentaire de moderation si disponible ;
- prochaine action possible : modifier, soumettre, annuler, dupliquer depuis une version refusee.

## Back-office attendu

Fonctionnalites V1 :
- afficher un resume immersif de la fiche commercant ;
- afficher le score de completion ;
- visualiser les differences entre version publiee et proposition commercant ;
- consulter l'etat detaille d'une demande de modification ;
- afficher une alerte dashboard operationnel lorsque des demandes de publication sont en attente de traitement ;
- approuver une proposition ;
- refuser avec motif sans changer la version publiee ;
- masquer temporairement la fiche publique ;
- revenir en brouillon ;
- consulter l'historique de moderation.

Actions possibles :
- `Approuver la fiche`
- `Refuser la fiche`
- `Masquer la fiche`
- `Remettre en brouillon`
- `Annuler la demande`

API admin V1 :

Toutes les routes ci-dessous sont des API admin protegees par l'authentification et l'autorisation back-office Localeo. Prefixe recommande : `/admin/api/profils-commercants`.

- `GET /admin/api/profils-commercants` : lister les profils avec filtres par statut de publication, demandes a moderer, ville, type commercant, completion et recherche texte ;
- `GET /admin/api/profils-commercants/a-moderer` : lister les demandes de publication en attente pour le dashboard operationnel et la file de moderation ;
- `GET /admin/api/profils-commercants/{profil_id}` : consulter la fiche admin complete, avec commercant, etat courant, version publiee, proposition active et historique court ;
- `POST /admin/api/profils-commercants` : creer manuellement un profil racine dans `profils_commercants` si absent, en secours de la migration ou de la creation automatique ;
- `GET /admin/api/profils-commercants/{profil_id}/versions` : lister l'historique des versions ;
- `GET /admin/api/profils-commercants/{profil_id}/versions/{version_id}` : consulter une version precise ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/brouillon` : creer une version `BROUILLON` admin depuis la version publiee ou une version refusee ;
- `PATCH /admin/api/profils-commercants/{profil_id}/versions/{version_id}` : modifier une version `BROUILLON` cote admin ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/soumettre` : passer une version `BROUILLON` en `A_MODERER` ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/approuver` : approuver une version `A_MODERER`, publier la nouvelle version, archiver l'ancienne et mettre a jour `version_publiee_id` ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/refuser` : refuser une version `A_MODERER` avec `motif_refus` et `decision_commentaire_public` ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/dupliquer` : dupliquer une version vers un nouveau `BROUILLON`, notamment apres refus ;
- `POST /admin/api/profils-commercants/{profil_id}/masquer` : masquer la fiche publique sans modifier `Commercant.statut` ;
- `POST /admin/api/profils-commercants/{profil_id}/republier` : republier une fiche `MASQUEE` si une version `PUBLIEE` existe ;
- `GET /admin/api/profils-commercants/{profil_id}/diff` : comparer `version_publiee_id` et `proposition_active_id`, ou deux versions via query params ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/verifier-liens` : enregistrer la validation manuelle admin des liens publics ;
- `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/verifier-photos` : enregistrer la validation manuelle admin des photos ;
- `GET /admin/api/profils-commercants/{profil_id}/versions/{version_id}/preview` : retourner le JSON de preview admin pour controler une version avant approbation ;
- `GET /admin/api/profils-commercants/{profil_id}/audit` : consulter les evenements d'audit du profil.

Payloads admin principaux :

`PATCH /admin/api/profils-commercants/{profil_id}/versions/{version_id}` modifie uniquement une version `BROUILLON`.

Request :

```json
{
  "accroche_courte": "Une cave chaleureuse au coeur du quartier.",
  "presentation_longue": "Texte de presentation complet.",
  "histoire_commercant": "L'histoire du lieu.",
  "mot_du_commercant": "Bienvenue chez nous.",
  "specialites": "Vins naturels, planches locales, accords mets-vins",
  "ambiance": "Conviviale, intimiste, conseils personnalises",
  "valeurs": "Circuit court, artisans locaux, conseil",
  "labels_certifications": "Bio, artisans partenaires",
  "bon_a_savoir": "Reservation conseillee le vendredi soir.",
  "horaires_texte": "Du mardi au samedi, 10h-19h.",
  "acces_transport": "Tram A, arret Centre.",
  "accessibilite": "Acces PMR partiel.",
  "site_web_url": "https://example.com",
  "instagram_url": "https://instagram.com/example",
  "facebook_url": null,
  "reservation_url": null,
  "image_principale_uri": "/images/...",
  "image_portrait_uri": "/images/...",
  "image_ambiance_1_uri": "/images/...",
  "image_ambiance_2_uri": null,
  "image_ambiance_3_uri": null
}
```

Response :

```json
{
  "profil_id": "uuid",
  "version_id": "uuid",
  "statut_version": "BROUILLON",
  "statut_demande": "BROUILLON",
  "score_completion": 82,
  "palier_completion": "FICHE_PUBLIABLE_SI_CRITERES_OK",
  "criteres_publication": {
    "publiable": false,
    "blocages": ["verification_photos_requise"]
  },
  "updated_at": "2026-05-12T10:30:00Z"
}
```

`POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/approuver`

Request :

```json
{
  "commentaire_moderation_interne": "Contenu relu et conforme.",
  "decision_commentaire_public": "Votre fiche est publiee."
}
```

Response :

```json
{
  "profil_id": "uuid",
  "version_id": "uuid",
  "ancienne_version_publiee_id": "uuid",
  "statut_version": "PUBLIEE",
  "statut_publication": "PUBLIE",
  "publie_at": "2026-05-12T10:35:00Z",
  "audit_event": "PROFIL_APPROUVE"
}
```

`POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/refuser`

Request :

```json
{
  "motif_refus": "Les photos ne permettent pas d'identifier clairement le commerce.",
  "decision_commentaire_public": "Merci d'ajouter des photos plus representatives de votre commerce.",
  "commentaire_moderation_interne": "Refus lie a la galerie photo."
}
```

Response :

```json
{
  "profil_id": "uuid",
  "version_id": "uuid",
  "statut_version": "REFUSEE",
  "statut_demande": "REFUSEE",
  "motif_refus": "Les photos ne permettent pas d'identifier clairement le commerce.",
  "decision_commentaire_public": "Merci d'ajouter des photos plus representatives de votre commerce.",
  "audit_event": "PROFIL_REFUSE",
  "peut_dupliquer_en_brouillon": true
}
```

`POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/verifier-liens`

Request :

```json
{
  "verification_liens_statut": "VALIDEE",
  "verification_liens_resume": "Site web et Instagram coherents avec le commerce."
}
```

Response :

```json
{
  "profil_id": "uuid",
  "version_id": "uuid",
  "verification_liens_statut": "VALIDEE",
  "verification_liens_resume": "Site web et Instagram coherents avec le commerce.",
  "updated_at": "2026-05-12T10:40:00Z"
}
```

`POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/verifier-photos`

Request :

```json
{
  "verification_photos_statut": "REFUSEE",
  "verification_photos_resume": "La photo principale est floue et ne montre pas le lieu."
}
```

Response :

```json
{
  "profil_id": "uuid",
  "version_id": "uuid",
  "verification_photos_statut": "REFUSEE",
  "verification_photos_resume": "La photo principale est floue et ne montre pas le lieu.",
  "criteres_publication": {
    "publiable": false,
    "blocages": ["verification_photos_refusee"]
  },
  "updated_at": "2026-05-12T10:42:00Z"
}
```

Erreurs API standardisees :

```json
{
  "code": "VERSION_NON_MODIFIABLE",
  "message": "Seule une version BROUILLON peut etre modifiee.",
  "details": {
    "statut_version": "A_MODERER"
  }
}
```

Codes d'erreur V1 :
- `VERSION_NON_MODIFIABLE` ;
- `VERSION_DEJA_TRAITEE` ;
- `VERSION_INCOMPATIBLE_STATUT` ;
- `PROFIL_PUBLICATION_INVALIDE` ;
- `VALIDATION_LIENS_REQUISE` ;
- `VALIDATION_PHOTOS_REQUISE` ;
- `CRITERES_PUBLICATION_INCOMPLETS` ;
- `PROPOSITION_ACTIVE_EXISTANTE` ;
- `VERSION_PUBLIEE_ACTIVE_EXISTANTE`.

Regle de securite : `approuver` recalcule toujours les criteres de publication cote backend. Le backend ne doit jamais publier une version uniquement sur la base du score ou d'un etat envoye par le front.

## User Stories detaillees

### `PRD-093` Page publique commercant immersive


Statut : `Termine`

En tant que visiteur marketplace, je veux consulter une page commercant riche afin de comprendre l'univers du partenaire avant d'acheter ou d'utiliser un coffret.

Resultat attendu :
- la page affiche accroche, presentation, photos, specialites, ambiance, prestations et informations pratiques publiques.

### `PRD-094` Donnees editoriales de profil commercant


Statut : `Termine`

En tant qu'admin Localeo, je veux enrichir les informations publiques d'un commercant afin de rendre sa fiche plus humaine et differenciante.

Resultat attendu :
- le back-office permet de renseigner les champs editoriaux et de controler leur publication.

### `PRD-095` Edition mobile encadree


Statut : `Termine`

En tant que commercant authentifie, je veux proposer des modifications de ma fiche depuis l'application mobile afin de garder ma presentation a jour.

Resultat attendu :
- les champs autorises sont modifiables ou soumis a moderation selon leur sensibilite.

### `PRD-096` Moderation des contenus commercant


Statut : `Termine`

En tant qu'operateur Localeo, je veux moderer les contenus proposes par les commercants afin de garantir la qualite et la conformite des fiches publiques.

Resultat attendu :
- chaque proposition publique passe par un statut de moderation avant publication, et un refus ne modifie ni la version publiee ni le statut du commercant.

### `PRD-096 bis` Versioning de fiche commercant


Statut : `Termine`

En tant qu'operateur Localeo, je veux conserver une version publiee stable pendant qu'une future version est en approbation afin de ne pas degrader la page publique en cas de refus.

Resultat attendu :
- le systeme distingue version publiee, proposition en cours et versions historiques ;
- la page publique continue de servir la version publiee tant qu'une proposition n'est pas approuvee ;
- le refus d'une proposition conserve le commercant actif et la fiche publiee existante.

### `PRD-096 ter` Suivi d'etat des demandes de modification


Statut : `Termine`

En tant que commercant authentifie, je veux consulter l'etat de mes demandes de modification afin de savoir si ma fiche est en brouillon, en attente, approuvee ou refusee.

Resultat attendu :
- l'espace commercant affiche la liste des demandes de modification ;
- chaque demande expose son statut, les dates importantes et les champs modifies ;
- en cas de refus, le commercant voit un motif exploitable sans que la version publiee soit impactee ;
- le commercant peut reprendre une demande refusee en nouveau brouillon si le back-office l'autorise.

### `PRD-096 quater` Alerte dashboard demandes de publication


Statut : `Termine`

En tant qu'operateur Localeo, je veux voir une alerte dans le dashboard operationnel lorsqu'une demande de publication de fiche commercant est en attente afin de ne pas laisser les propositions sans traitement.

Resultat attendu :
- le dashboard operationnel affiche le nombre de demandes de publication `A_MODERER` ou `EN_ATTENTE_RELECTURE` ;
- l'alerte est visible dans les alertes prioritaires lorsque le compteur est superieur a zero ;
- l'alerte pointe vers la vue back-office de traitement des demandes ;
- l'absence de demande en attente ne doit pas generer d'alerte.

### `PRD-097` Score de completion de fiche


Statut : `Termine`

En tant qu'operateur Localeo, je veux connaitre le niveau de completion d'une fiche afin de prioriser les enrichissements.

Resultat attendu :
- le back-office et l'espace commercant affichent un score ou une checklist de completion calcule a la volee depuis la version publiee et/ou la proposition active.

Bareme V1 calcule a la volee sur 100 points :

| Bloc | Points |
| --- | ---: |
| Accroche courte renseignee | 10 |
| Presentation longue renseignee | 15 |
| Histoire ou mot du commercant renseigne | 10 |
| Au moins 3 photos validees | 15 |
| Image principale ou portrait valide | 10 |
| Au moins une specialite renseignee | 10 |
| Ambiance renseignee | 10 |
| Information pratique renseignee | 10 |
| Au moins une prestation active rattachee | 10 |
| Total | 100 |

Paliers d'affichage :
- `0-39` : fiche insuffisante ;
- `40-69` : fiche a completer ;
- `70-89` : fiche bien renseignee ;
- `90-100` : fiche tres complete.

Regles :
- le score est indicatif et aide a prioriser les enrichissements ;
- le score n'est pas persiste en V1 ;
- les liens publics ne contribuent pas au score V1 ;
- un score faible ne bloque pas la soumission ni la publication ;
- le back-office peut encourager la completion progressive sans imposer un formulaire complet en une seule fois.

### `PRD-097 bis` Publication progressive sans seuil minimal


Statut : `Termine`

En tant qu'operateur Localeo, je veux pouvoir publier progressivement une fiche meme incomplete afin de ne pas decourager les commercants avec un formulaire trop lourd a remplir en une seule fois.

Resultat attendu :
- aucun champ editorial n'est obligatoire pour soumettre ou publier une fiche ;
- le score de completion et la checklist guident l'enrichissement progressif, sans bloquer ;
- les liens publics, emails publics, telephones publics et photos ne bloquent pas s'ils sont absents ;
- un contenu renseigne puis explicitement refuse en moderation ou verification peut bloquer la publication tant qu'il n'est pas corrige ou retire ;
- l'admin conserve la decision finale de publier, refuser ou demander une correction.

### `PRD-097 ter` Apercu mobile non indexe


Statut : `Termine`

En tant que commercant authentifie, je veux generer un apercu de ma page commercant depuis l'application mobile afin de verifier le rendu avant soumission ou publication.

Resultat attendu :
- l'application commercant peut afficher un apercu base sur la proposition active ;
- l'apercu est protege par session commercant ;
- l'apercu est marque non indexable ;
- l'apercu est fourni sous forme de donnees JSON de preview en V1 ;
- aucun lien public partageable de preview n'est genere en V1 ;
- l'apercu ne remplace pas la version publique publiee ;
- l'apercu indique clairement que le contenu est en previsualisation.

### `PRD-098` Signaux de confiance sur la page commercant


Statut : `Termine`

En tant que visiteur marketplace, je veux voir des signaux de confiance rattaches au commercant afin d'etre rassure.

Resultat attendu :
- la page peut afficher activites publiques, feedbacks agreges et prestations recemment utilisees sans exposer de donnees client.

## Backlog d'implementation

### Lot 1 - Migration et modele SQL

Objectif : poser les tables, contraintes et garde-fous sans exposer encore de nouvelle surface fonctionnelle.

Taches :
- creer la migration SQL `profils_commercants` ;
- creer la migration SQL `profils_commercants_versions` ;
- creer une ligne `profils_commercants` par commercant existant avec `statut_publication = NON_PUBLIE` ;
- ne generer aucune version editoriale `PUBLIEE` pendant la migration massive ;
- ajouter la creation automatique du profil racine a la creation d'un nouveau commercant ;
- ajouter les index standards sur statut, version publiee, proposition active et moderation ;
- ajouter les index uniques partiels PostgreSQL comme garde-fous, si la base cible le permet ;
- documenter le rollback attendu de la migration.

Sortie attendue :
- les tables existent ;
- tous les commercants existants ont un profil racine `NON_PUBLIE` ;
- aucune page marketplace publique n'est exposee par cette migration.

### Lot 2 - Domaine et invariants metier

Objectif : centraliser les regles de cycle de vie avant d'exposer les APIs.

Taches :
- definir les enums domaine : `statut_publication`, `statut_version`, `statut_demande`, `statut_verification` ;
- implementer les invariants : une seule version `PUBLIEE` active et une seule proposition active par commercant ;
- implementer la creation de brouillon ;
- implementer la soumission en moderation ;
- implementer l'approbation avec archivage de l'ancienne version publiee ;
- implementer le refus sans impact sur la version publiee ni sur `Commercant.statut` ;
- implementer la duplication d'une version `REFUSEE` vers un nouveau `BROUILLON` ;
- implementer la purge automatique des anciennes versions de page commercant a la creation d'une nouvelle version, avec conservation des 3 dernieres versions et protection des versions actives ;
- implementer le masquage et la republication ;
- implementer le calcul de completion sur 100 points ;
- implementer la verification des contenus explicitement refuses avant publication ;
- implementer le diff a la volee entre deux snapshots.

Sortie attendue :
- les regles de publication sont testables sans API ;
- aucune transition invalide ne peut etre executee par un use case nominal.

### Lot 3 - Persistence, repositories et audit

Objectif : fournir les acces donnees et traces necessaires aux use cases.

Taches :
- ajouter les modeles ORM `ProfilCommercantOrm` et `ProfilCommercantVersionOrm` ;
- ajouter les relations utiles vers `CommercantOrm` ;
- ajouter les repositories de lecture/ecriture des profils et versions ;
- ajouter les requetes de listing des demandes `A_MODERER` ;
- ajouter les requetes de dashboard pour compter les demandes a traiter ;
- emettre les evenements d'audit `PROFIL_BROUILLON_CREE`, `PROFIL_SOUMIS_MODERATION`, `PROFIL_APPROUVE`, `PROFIL_REFUSE`, `PROFIL_MASQUE`, `PROFIL_REPUBLIE` ;
- exposer la lecture de l'audit pour la fiche admin.

Sortie attendue :
- les use cases domaine peuvent persister et relire les profils ;
- les evenements critiques sont traces.

### Lot 4 - API admin back-office

Objectif : livrer la surface de moderation Localeo.

Taches :
- implementer `GET /admin/api/profils-commercants` ;
- implementer `GET /admin/api/profils-commercants/a-moderer` ;
- implementer `GET /admin/api/profils-commercants/{profil_id}` ;
- implementer `POST /admin/api/profils-commercants` ;
- implementer `GET /admin/api/profils-commercants/{profil_id}/versions` ;
- implementer `GET /admin/api/profils-commercants/{profil_id}/versions/{version_id}` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/brouillon` ;
- implementer `PATCH /admin/api/profils-commercants/{profil_id}/versions/{version_id}` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/soumettre` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/approuver` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/refuser` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/dupliquer` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/masquer` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/republier` ;
- implementer `GET /admin/api/profils-commercants/{profil_id}/diff` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/verifier-liens` ;
- implementer `POST /admin/api/profils-commercants/{profil_id}/versions/{version_id}/verifier-photos` ;
- implementer `GET /admin/api/profils-commercants/{profil_id}/versions/{version_id}/preview` ;
- implementer `GET /admin/api/profils-commercants/{profil_id}/audit` ;
- standardiser les erreurs API V1.

Sortie attendue :
- un admin peut creer, enrichir, moderer, refuser, masquer, republier et auditer une fiche ;
- l'approbation recalcule toujours les criteres de publication cote backend.

### Lot 5 - API commercant authentifiee

Objectif : permettre au commercant de preparer et suivre sa fiche sans exposition publique directe.

Taches :
- implementer `GET /commercants/me/page` ;
- implementer `GET /commercants/me/page/demandes` ;
- implementer `GET /commercants/me/page/demandes/{demande_id}` ;
- implementer `GET /commercants/me/page/apercu` ;
- implementer `GET /commercants/me/page/demandes/{demande_id}/apercu` ;
- implementer `PATCH /commercants/me/page/contact` pour les champs autorises ;
- implementer `PATCH /commercants/me/page/brouillon` ;
- implementer `POST /commercants/me/page/soumettre-moderation` ;
- rejeter explicitement les champs sensibles et structurants ;
- retourner le score de completion, les alertes de contenu a corriger et le statut lisible ;
- garantir que la preview retourne du JSON authentifie sans URL publique partageable.

Sortie attendue :
- un commercant peut editer un brouillon, soumettre, suivre une demande et previsualiser sans publier.

### Lot 6 - Publication marketplace

Objectif : exposer uniquement les fiches approuvees.

Taches :
- implementer `GET /public/commercants/{commercant_id}/page` ;
- lire uniquement la version editoriale `PUBLIEE` courante ;
- refuser l'exposition si aucune version `PUBLIEE` n'existe ;
- refuser l'exposition si le commercant n'est pas `ACTIF` ;
- exclure les contenus `BROUILLON`, `A_MODERER`, `REFUSEE`, `ARCHIVEE`, `MASQUEE` ;
- construire les donnees publiques avec prestations actives, photos validees, infos pratiques et signaux autorises ;
- integrer les signaux publics issus des Epics 16 et 17 sans exposer de donnees client.

Sortie attendue :
- la marketplace ne sert que des fiches publiques explicitement approuvees.

### Lot 7 - Dashboard operationnel et back-office visuel

Objectif : rendre la moderation exploitable au quotidien.

Taches :
- ajouter le compteur de demandes de publication en attente au dashboard operationnel ;
- afficher l'alerte prioritaire si le compteur est superieur a zero ;
- faire pointer l'alerte vers `GET /admin/api/profils-commercants/a-moderer` ou la vue back-office equivalente ;
- afficher dans la fiche admin le score de completion, les blocages, les validations liens/photos et le diff ;
- afficher les actions admin selon le statut courant de la version.

Sortie attendue :
- les demandes a traiter sont visibles et actionnables depuis le back-office.

### Lot 8 - Tests et validation

Objectif : securiser les invariants et les parcours critiques.

Taches :
- tester la migration massive en `NON_PUBLIE` sans version publiee ;
- tester la creation automatique de `profils_commercants` pour un nouveau commercant ;
- tester les transitions autorisees et interdites ;
- tester l'unicite domaine de la version `PUBLIEE` active ;
- tester l'unicite domaine de la proposition active ;
- tester le refus sans impact public ;
- tester la duplication d'une version `REFUSEE` en `BROUILLON` ;
- tester la purge automatique des anciennes versions lors de la creation d'une nouvelle version ;
- tester que la purge conserve les 3 dernieres versions et ne supprime jamais la version publiee courante ni la proposition active ;
- tester le calcul de completion indicatif et les contenus explicitement refuses ;
- tester l'approbation avec recalcul backend des criteres ;
- tester la validation manuelle des liens et photos ;
- tester que la marketplace ne retourne rien sans version `PUBLIEE` ;
- tester que la preview est authentifiee et non partageable publiquement ;
- tester l'alerte dashboard demandes a moderer ;
- tester les erreurs standardisees.

Sortie attendue :
- les invariants de publication sont couverts par tests unitaires et tests API ;
- les parcours admin, commercant et public sont verifies.

### Ordre recommande

1. Lot 1 - Migration et modele SQL.
2. Lot 2 - Domaine et invariants metier.
3. Lot 3 - Persistence, repositories et audit.
4. Lot 4 - API admin back-office.
5. Lot 5 - API commercant authentifiee.
6. Lot 6 - Publication marketplace.
7. Lot 7 - Dashboard operationnel et back-office visuel.
8. Lot 8 - Tests et validation en continu, avec durcissement final avant livraison.

## Criteres d'acceptation globaux

- Une fiche commercant publique ne doit exposer que des donnees explicitement publiables.
- Un commercant non actif ne doit pas etre visible publiquement.
- Les contenus proposes depuis mobile ne sont pas publics avant moderation.
- La version publiee reste active tant qu'une nouvelle version n'est pas approuvee.
- Le refus d'une future version ne doit jamais desactiver le commercant.
- Le refus d'une future version ne doit jamais masquer ou modifier la version publiee courante.
- Un commercant doit pouvoir consulter l'etat de ses demandes de modification depuis son espace authentifie.
- Une demande de modification doit exposer un statut lisible et un motif de refus public lorsque la demande est refusee.
- Le dashboard operationnel doit signaler les demandes de publication en attente de traitement.
- L'historique de page commercant doit etre limite aux 3 dernieres versions purgeables apres creation d'une nouvelle version.
- Les champs sensibles sont rejetes explicitement par les endpoints mobile.
- Une fiche peut etre publiee progressivement sans seuil minimal de completion.
- Le commercant doit pouvoir generer un apercu non indexe de sa fiche depuis l'application commercant.
- Le back-office permet de comprendre rapidement l'etat de completion et de moderation.
- Les images publiques passent par les mecanismes media existants.
- Les activites et feedbacks publics respectent les regles d'anonymisation des Epics 16 et 17.

## Hors perimetre V1

- messagerie publique directe entre visiteur et commercant ;
- reservation ou achat direct depuis la fiche ;
- edition bancaire depuis mobile ;
- publication automatique sans moderation ;
- horaires structures complexes ;
- multi-etablissements pour un meme commercant ;
- contenu multilingue.

## Questions ouvertes

Aucune question ouverte a ce stade.


## Compléments Commerçant

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### User Stories detaillees / `PRD-097` Score de completion de fiche

Paliers d'affichage :
- `70-89` : fiche publiable si les criteres obligatoires sont respectes ;

Regles :
- un score eleve ne suffit pas a publier si un critere obligatoire ou une validation admin manque.

### User Stories detaillees / `PRD-097 bis` Seuil minimal de publication

En tant qu'operateur Localeo, je veux bloquer la publication d'une fiche insuffisamment renseignee afin de garantir une experience publique coherente et qualitative.

Resultat attendu :
- la publication exige une accroche courte ;
- la publication exige une presentation longue ;
- la publication exige au moins trois photos validees au total, dont une image principale ou un portrait ;
- la publication exige au moins une specialite ;
- la publication exige au moins une ambiance ;
- la publication exige au moins une information pratique : `bon_a_savoir`, `horaires_texte`, ou mention explicite equivalent `horaires variables / sur reservation` ;
- la publication exige au moins une prestation active rattachee au commercant ;
- les liens publics, emails publics et telephones publics ne bloquent pas s'ils sont absents, mais doivent etre valides et approuves manuellement s'ils sont renseignes.

### Backlog d'implementation / Lot 2 - Domaine et invariants metier

Taches :
- implementer la verification des criteres bloquants de publication ;

### Backlog d'implementation / Lot 5 - API commercant authentifiee

Taches :
- retourner le score de completion, les blocages de publication et le statut lisible ;

### Backlog d'implementation / Lot 8 - Tests et validation

Taches :
- tester le calcul de completion et les criteres bloquants ;

### Criteres d'acceptation globaux

- Une fiche ne peut etre publiee que si le seuil minimal de publication est atteint.
