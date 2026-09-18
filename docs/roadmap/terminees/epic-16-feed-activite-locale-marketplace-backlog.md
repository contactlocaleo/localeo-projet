# Backlog Epic 16 - Feed d'activite locale marketplace

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Perimetre

Epic source : `Epic 16. Feed d'activite locale marketplace`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : construire un feed public d'activite locale, anonymise et moderable, pour afficher sur la marketplace des signaux recents autour des coffrets, villes, commercants et prestations.

## Statut global

- Epic 16 : `Termine`
- Avancement : projection, API publique, generation automatique et moderation backoffice disponibles cote backend.

## Vision produit

Le feed d'activite locale doit rendre la marketplace plus vivante sans devenir intrusif. Il doit produire une preuve sociale sobre :

- des coffrets sont achetes ;
- des coffrets sont actives ;
- des prestations sont utilisees ;
- de nouveaux commercants ou coffrets arrivent ;
- certaines offres ont une dynamique locale.

Le feed public ne doit jamais exposer l'identite d'un client, ses coordonnees, ni une action trop precise qui permettrait de le reconnaitre.

## Surfaces marketplace ciblees

### Page d'accueil

Objectif : afficher une activite globale recente et rassurante.

Contenus possibles :
- achats recents anonymises ;
- coffrets recemment actives ;
- prestations recemment consommees ;
- nouveaux commercants actifs ;
- nouveaux coffrets actifs ;
- coffrets populaires sur une periode recente.
- coffret du moment, calcule depuis les meilleurs signaux de feed local.

### Page ville

Objectif : montrer la dynamique locale d'une ville.

Contenus possibles :
- activites rattachees a la ville ;
- coffrets achetes ou actives dans cette ville ;
- prestations validees chez des commercants de la ville ;
- nouveaux commercants actifs dans la ville ;
- nouveaux coffrets disponibles dans la ville.
- coffret du moment pour cette ville, base sur la dynamique locale recente.

### Page commercant

Objectif : renforcer la confiance autour d'un commercant.

Contenus possibles :
- prestation validee recemment chez ce commercant ;
- coffret contenant une prestation de ce commercant achete recemment ;
- commercant nouvellement actif ;
- prestation mise a jour ou enrichie.

### Page coffret

Objectif : montrer la dynamique d'un coffret precis.

Contenus possibles :
- coffret achete recemment ;
- coffret active recemment ;
- prestation du coffret consommee recemment ;
- coffret nouvellement disponible ;
- volume agrege d'activite recente si le volume est suffisant.

## Types d'activite V1

Types recommandes :
- `ACHAT_COFFRET_CONFIRME`
- `COFFRET_INSTANCE_ACTIVEE`
- `PRESTATION_VALIDEE`
- `COMMERCANT_ACTIVE`
- `COFFRET_ACTIVE`
- `PRESTATION_COFFRET_ACTIVE`
- `PRESTATION_COFFRET_VERSIONNEE`
- `COFFRET_POPULAIRE`

Types exclus du feed public V1 :
- paiement echoue ;
- annulation ;
- remboursement ;
- support ;
- erreur technique ;
- echec d'envoi email/SMS ;
- validation secours, sauf decision produit explicite ulterieure.

## Modele de donnees recommande

Creer une table `activites_locales`.

Champs recommandes :
- `id`
- `type_activite`
- `ville_id` nullable
- `commercant_id` nullable
- `coffret_id` nullable
- `prestation_coffret_id` nullable
- `achat_id` nullable, non expose publiquement
- `coffret_instance_id` nullable, non expose publiquement
- `titre`
- `description` nullable
- `niveau_visibilite` : `PUBLIC`, `BACKOFFICE`, `MASQUE`
- `poids` entier, pour ordonnancement
- `date_evenement`
- `date_publication`
- `metadata JSONB`
- `date_creation`

Index recommandes :
- `(niveau_visibilite, date_publication)`
- `(ville_id, niveau_visibilite, date_publication)`
- `(commercant_id, niveau_visibilite, date_publication)`
- `(coffret_id, niveau_visibilite, date_publication)`
- `(type_activite, niveau_visibilite, date_publication)`

## Strategie de generation

Le feed ne doit pas etre calcule a la volee depuis toutes les tables metier. La V1 doit utiliser une projection.

Principe :
1. Un evenement metier eligibile survient.
2. Le use case metier ou un service de projection cree une ligne `activites_locales`.
3. L'API publique lit uniquement la projection publiee.
4. Le backoffice peut masquer ou reactiver une activite.

Sources d'evenements V1 :
- validation paiement achat coffret ;
- activation `CoffretInstance` ;
- validation prestation ;
- passage commercant a `ACTIF` ;
- passage coffret a `ACTIVE` ;
- passage prestation coffret a `ACTIVE` ;
- creation d'une nouvelle version de prestation.

Generation batch optionnelle :
- recalculer des activites agregees comme `COFFRET_POPULAIRE` ;
- recalculer ou exposer le coffret du moment a partir des activites publiques recentes ;
- rattraper des activites manquantes apres migration ;
- supprimer ou masquer automatiquement des activites trop anciennes si necessaire.

## Regles d'anonymisation

Regles obligatoires :
- ne jamais exposer `email_client`, `telephone_client`, `nom_contact`, `nom_entreprise` ou toute donnee personnelle client ;
- ne jamais exposer `achat_id` ni `coffret_instance_id` dans l'API publique ;
- ne pas afficher une heure exacte si le volume local est faible ;
- preferer des libelles comme `recemment`, `cette semaine`, `aujourd'hui` selon le contexte ;
- ne pas afficher de localisation plus precise que la ville ;
- ne pas publier les evenements negatifs ou sensibles en V1.

Exemples de formulations publiques :
- `Un coffret a ete offert a Toulouse`
- `Une prestation a ete utilisee chez Maison Dupont`
- `Le coffret Bien-etre est actif a Albi`
- `Nouveau commercant partenaire a Montauban`
- `Ce coffret a ete choisi recemment`

Decision actee :
- le nom public du commercant peut etre affiche sur les activites de validation ou d'utilisation de prestation, par exemple `Une prestation a ete utilisee chez Maison Dupont`, tant qu'aucune donnee client n'est exposee.
- une activite locale est visible publiquement pendant 45 jours par defaut. Les nouveautes catalogue peuvent rester visibles 90 jours. Les signaux agreges de popularite sont recalcules et visibles 14 jours. Passe ce delai, l'activite reste consultable en backoffice mais n'est plus exposee publiquement.
- en V1, les evenements peuvent etre affiches individuellement tant qu'ils ne contiennent aucune donnee client. Pour les zones ou objets a faible volume, le libelle doit etre floute temporellement et peut etre agrege. Le regroupement automatique strict est reporte en V2.
- les activites editoriales manuelles sont autorisees en V2. Elles devront etre creees et moderees depuis le backoffice, avec les memes regles de visibilite publique que les activites generees automatiquement.
- les libelles V1 du feed d'activite locale sont generes depuis des templates fixes par type d'activite. Ils peuvent afficher le nom public du commercant, le nom public du coffret et la ville, mais jamais d'information client. Les dates exactes sont remplacees par une formulation temporelle floutee comme `recemment`, `cette semaine` ou `ce mois-ci`.

Templates de libelles V1 :
- `ACHAT_COFFRET_CONFIRME` : `Un coffret a ete offert recemment a {ville}` ;
- `COFFRET_INSTANCE_ACTIVEE` : `Un coffret vient d'etre active a {ville}` ;
- `PRESTATION_VALIDEE` : `Une prestation a ete utilisee chez {commercant}` ;
- `COMMERCANT_ACTIVE` : `{commercant} rejoint les commercants partenaires a {ville}` ;
- `COFFRET_ACTIVE` : `Le coffret {coffret} est disponible a {ville}` ;
- `PRESTATION_COFFRET_ACTIVE` : `Une nouvelle prestation est disponible chez {commercant}` ;
- `PRESTATION_COFFRET_VERSIONNEE` : `{commercant} a mis a jour une prestation` ;
- `COFFRET_POPULAIRE` : `Le coffret {coffret} est souvent choisi recemment`.

Fallbacks de libelles :
- `{ville}` absente : `dans une ville partenaire` ;
- `{commercant}` absent : `chez un commercant partenaire` ;
- `{coffret}` absent : `un coffret Localeo`.

## API publique recommandee

Endpoint :
- `GET /public/activites-locales`
- `GET /public/coffrets/du-moment`

Parametres :
- `ville_id` optionnel ;
- `commercant_id` optionnel ;
- `coffret_id` optionnel ;
- `limit` optionnel, borne cote serveur ;
- `type_activite` optionnel ;
- `scope` optionnel : `HOME`, `VILLE`, `COMMERCANT`, `COFFRET`.

Parametres `GET /public/coffrets/du-moment` :
- `ville_id` optionnel, pour calculer le coffret du moment sur une ville ;
- `jours` optionnel, borne cote serveur, par defaut 14 jours ;
- `limit` optionnel, par defaut 1, borne cote serveur.

Contrat de reponse `GET /public/coffrets/du-moment` :
- `coffret`, avec uniquement les champs publics ;
- `score_feed_local` ;
- `periode_jours` ;
- `signaux`, par exemple nombre d'activites publiques recentes, nombre de commercants actifs representes, nombre de prestations actives rattachees ;
- `activites_recentes`, liste courte optionnelle d'activites publiques ayant contribue au score.

Contrat de reponse :
- `id`
- `type_activite`
- `titre`
- `description`
- `date_relative`
- `ville`
- `commercant` nullable, avec uniquement les champs publics ;
- `coffret` nullable, avec uniquement les champs publics ;
- `poids`

Contraintes :
- seuls les items `niveau_visibilite = PUBLIC` sont exposes ;
- aucun identifiant technique sensible n'est expose ;
- la limite maximale doit etre imposee par le backend.
- le coffret du moment ne considere que les coffrets `ACTIVE`, les prestations `ACTIVE` et les commercants `ACTIF` ;
- le scoring doit etre simple, explicable et stable sur une courte periode ;
- si aucun signal de feed local recent n'existe, l'API peut retourner un fallback base sur les coffrets actifs les plus complets ou retourner une absence de resultat explicite.

Scoring V1 recommande pour le coffret du moment :
- poids des activites publiques recentes rattachees au coffret ;
- poids des activites publiques recentes rattachees aux commercants ou prestations du coffret ;
- bonus de diversite des commercants actifs representes ;
- bonus de nombre de prestations actives rattachees ;
- bonus optionnel de feedbacks moderes et autorises, si disponible ;
- tie-break stable par date de publication recente puis nom du coffret.

## Backoffice attendu

Ajouter une vue `Activites locales`.

Fonctionnalites V1 :
- lister les activites ;
- filtrer par type, visibilite, ville, commercant, coffret ;
- voir les rattachements metier ;
- masquer une activite ;
- reactiver une activite masquee ;
- consulter les metadata techniques.

Actions possibles :
- `Masquer`
- `Publier`
- `Passer en backoffice uniquement`

Implementation V1 :
- migration `sql/v133_feed_activite_locale.sql` ;
- projection ORM `ActiviteLocaleOrm` ;
- endpoint public `GET /public/activites-locales` ;
- endpoint public `GET /public/coffrets/du-moment` ;
- vue backoffice `Activites locales` avec actions `Publier`, `Backoffice uniquement`, `Masquer` ;
- generation depuis paiement confirme, activation d'instance, validation de prestation, activation commercant/coffret/prestation et versionning prestation.

## User Stories detaillees

### `PRD-081` Feed accueil marketplace


Statut : `Termine`

En tant que visiteur marketplace, je veux voir une activite locale recente afin de percevoir que les coffrets sont reellement utilises.

Resultats attendus :
- la page d'accueil consomme l'API publique du feed ;
- les items affiches sont anonymises ;
- les items sont ordonnes par date de publication et poids ;
- l'absence d'activite ne bloque pas l'affichage de la page.

### `PRD-082` Feed page ville


Statut : `Termine`

En tant que visiteur d'une page ville, je veux voir les activites rattachees a cette ville afin de comprendre la dynamique locale.

Resultats attendus :
- la page ville filtre le feed par `ville_id` ;
- seules les activites publiques de la ville sont affichees ;
- les nouveaux commercants, coffrets et usages recents peuvent remonter.

### `PRD-083` Feed page commercant


Statut : `Termine`

En tant que visiteur d'une page commercant, je veux voir des signaux d'activite lies a ce commercant afin de renforcer la confiance.

Resultats attendus :
- la page commercant filtre le feed par `commercant_id` ;
- les validations ou activites liees aux prestations du commercant peuvent remonter ;
- aucune information client n'est affichee.

### `PRD-084` Feed page coffret


Statut : `Termine`

En tant que visiteur d'une page coffret, je veux voir des signaux d'activite lies a ce coffret afin d'evaluer sa dynamique.

Resultats attendus :
- la page coffret filtre le feed par `coffret_id` ;
- les achats, activations ou validations rattaches au coffret peuvent remonter ;
- les formulations restent anonymisees.

### `PRD-085` Moderation backoffice


Statut : `Termine`

En tant qu'admin, je veux moderer les activites affichees afin de masquer une activite non pertinente ou sensible.

Resultats attendus :
- une vue backoffice liste les activites locales ;
- un admin peut masquer une activite ;
- une activite masquee disparait immediatement de l'API publique ;
- un admin peut republier une activite si besoin.

### `PRD-086` Projection d'activite locale


Statut : `Termine`

En tant que systeme, je veux generer les activites locales depuis les evenements metier afin d'avoir une lecture publique simple et performante.

Resultats attendus :
- les use cases eligibles creent une activite locale ;
- la generation est idempotente autant que possible ;
- les activites contiennent les rattachements utiles ;
- l'API publique ne depend pas de jointures lourdes sur les tables transactionnelles.

### `PRD-087` Coffret du moment base sur le feed local


Statut : `Termine`

En tant que visiteur marketplace, je veux voir le coffret du moment afin de decouvrir l'offre locale la plus dynamique actuellement.

Resultats attendus :
- l'API `GET /public/coffrets/du-moment` retourne le coffret actif ayant les meilleurs signaux de feed local recent ;
- le calcul peut etre filtre par `ville_id` ;
- le score est base sur les activites publiques recentes, la diversite des commercants actifs et les prestations actives rattachees ;
- aucune donnee personnelle client ni identifiant transactionnel n'est expose ;
- le resultat est stable et explicable, avec les principaux signaux ayant contribue au score ;
- si aucun signal recent n'existe, l'API retourne un fallback explicite ou une absence de resultat exploitable par le front.

## UX marketplace attendue

Principes :
- affichage compact ;
- ton sobre ;
- pas de donnees personnelles ;
- possibilite de masquer le bloc si aucune activite pertinente ;
- eviter l'effet "reseau social".

Composants possibles :
- liste de 3 a 6 items ;
- timestamp floute : `recemment`, `cette semaine`, `ce mois-ci` ;
- icone par type d'activite ;
- lien optionnel vers ville, coffret ou commercant public.

## Criteres d'acceptation globaux

- Le feed public n'expose aucune donnee personnelle client.
- Les activites negatives ou sensibles ne sont pas publiees en V1.
- Les activites publiques sont filtrables par ville, commercant et coffret.
- La page d'accueil, la page ville, la page commercant et la page coffret peuvent consommer la meme API.
- La marketplace peut consommer une API publique de coffret du moment basee sur le feed local.
- Le coffret du moment ne remonte que des coffrets actifs portes par des commercants actifs.
- Un admin peut masquer une activite depuis le backoffice.
- Une activite masquee n'est plus retournee par l'API publique.
- Le feed reste disponible meme si aucune activite n'est presente.

## Hors perimetre V1

- Personnalisation par geolocalisation precise.
- Commentaires ou interactions utilisateur.
- Reactions sociales.
- Scoring avance par machine learning.
- Publication manuelle editoriale riche.
- Notifications push a partir du feed.

## Questions ouvertes

- Aucune question ouverte a ce stade pour la V1.
