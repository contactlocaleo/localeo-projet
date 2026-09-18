# Epic 52 - Accueil Marketplace contextualise par geolocalisation

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-52-accueil-marketplace-geolocalise-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Objet

Cette Epic permet a la Marketplace de contextualiser l'accueil avec les communes publiees situees dans un rayon configurable. Le centre du rayon est soit la position ponctuelle du visiteur apres son accord, soit les coordonnees d'une ville choisie manuellement. Le visiteur peut aussi refuser tout contexte territorial.

La geolocalisation est le mode propose par defaut, mais elle ne devient ni une condition d'acces, ni un mecanisme de suivi, ni une nouvelle identite client. Les coordonnees ne sont jamais conservees dans le navigateur : seul le mode choisi et, le cas echeant, le `ville_id` de preference le sont.

## Documents

- [Backlog](../../roadmap/terminees/epic-52-accueil-marketplace-geolocalise-backlog.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Ancrage dans l'existant

| Existant | Constat | Evolution attendue |
| --- | --- | --- |
| `VilleOrm` / table `villes` | Referentiel canonique avec nom, code postal, image et `publiee_marketplace`, mais sans code INSEE | Ajouter le code INSEE et un point geographique optionnels sans creer une nouvelle entite `commune` |
| `GET /public/referencement/villes` | Liste les territoires connus et permet une selection manuelle | Conserver ce repli et ajouter un contrat de proximite distinct |
| Pages et filtres Marketplace | Plusieurs contenus sont deja filtrables par `ville_id` ou `commune_id` | Reutiliser ces contrats a partir des communes proches |
| Epic 49 | Centralise l'eligibilite des animations publiques | Reutiliser ses projections, sans recalcul frontend |
| Feed d'activite locale | Porte deja une contextualisation territoriale | Filtrer par les communes selectionnees lorsque le contrat le permet |
| Geolocalisation | Aucune coordonnee de commune et aucun parcours navigateur | Ajouter un consentement ponctuel et un calcul serveur |

`Commune` reste le terme metier public. La persistance conserve le nom historique `villes`.

## Architecture initiale

```text
Visiteur
   |
   +--> AUTOUR_DE_MOI : autorisation -> position ponctuelle -> communes dans 30 km
   |
   +--> VILLE_PREFEREE : selection -> coordonnees de la ville origine
   |
   +--> AUCUNE : aucun contexte territorial
   |
   v
mode memorise dans le navigateur, sans coordonnees
   |
   +--> AUTOUR_DE_MOI / VILLE_PREFEREE
   |       -> backend : communes publiees dans le rayon configurable
   |       -> cinq widgets cibles de l'accueil contextualises
   |
   +--> AUCUNE
           -> widgets territoriaux non rendus
```

## Donnees cibles

Evolution additive de `villes` :

- `code_insee` : texte nullable, unique lorsqu'il est renseigne ;
- `latitude` : decimal nullable, borne `[-90, 90]` ;
- `longitude` : decimal nullable, borne `[-180, 180]` ;
- `coordonnees_source` : origine optionnelle de la donnee ;
- `coordonnees_updated_at` : date de derniere mise a jour.

Une commune est georeferencee uniquement lorsque latitude et longitude sont toutes deux presentes. Les coordonnees sont le point de reference de la commune, pas la position d'un batiment ou d'un utilisateur.

## Source des coordonnees communales

La source de reference du MVP est l'[API Decoupage administratif](https://geo.api.gouv.fr/decoupage-administratif/communes). Elle expose le centre d'une commune et permet une consultation directe par code INSEE :

L'URL de sa collection de communes est configurable par `LOCALEO_GEO_API_GOUV_COMMUNES_URL`, avec `https://geo.api.gouv.fr/communes` par defaut. Une URL alternative doit conserver le meme contrat JSON ; elle peut notamment pointer vers un proxy ou un mock d'environnement.

```http
GET https://geo.api.gouv.fr/communes/{code_insee}?fields=nom,code,codesPostaux,centre&format=json&geometry=centre
```

Le champ GeoJSON `centre.coordinates` est interprete dans l'ordre `[longitude, latitude]`.

Pour les villes historiques depourvues de code INSEE, le Backoffice recherche des candidats avec le nom et le code postal. Le rapprochement n'est jamais valide automatiquement lorsqu'il existe zero ou plusieurs candidats : l'operateur choisit le bon resultat ou renseigne les donnees manuellement.

Apres confirmation, Localeo conserve :

- le code INSEE ;
- la latitude et la longitude du centre ;
- la source `API_DECOUPAGE_ADMINISTRATIF` ou `SAISIE_MANUELLE` ;
- la date de mise a jour.

L'API externe n'est jamais appelee dans le parcours public. La recherche de proximite et Haversine utilisent exclusivement les donnees locales. Une indisponibilite de `geo.api.gouv.fr` peut empecher temporairement un enrichissement Backoffice, mais ne degrade pas la Marketplace.

L'integration applique un timeout court, des reprises bornees pour les erreurs temporaires et une validation stricte du payload. Une synchronisation ulterieure par code INSEE peut etre executee en batch, sans ecraser silencieusement une correction manuelle.

## Calcul de proximite

La formule de Haversine calcule une distance a vol d'oiseau entre la position ponctuelle du visiteur et le point de reference de chaque commune. Cette precision est suffisante pour ordonner des territoires ; elle ne doit jamais etre presentee comme une distance routiere ou un temps de trajet.

Le calcul est effectue cote backend pour garantir :

- la meme regle pour tous les clients ;
- le respect du rayon maximal ;
- l'application du rayon par defaut de `30 km`, configurable cote backend ;
- l'exclusion des communes non publiables ;
- une evolution ulterieure possible vers PostGIS sans rupture du contrat.

Le service accepte deux formes d'origine exclusives :

- `POSITION` : latitude et longitude ponctuelles transmises par le navigateur ;
- `COMMUNE` : identifiant d'une ville de preference dont le backend lit lui-meme les coordonnees.

La reponse contient dans les deux cas le rayon effectif et la meme liste de communes publiees, triees par distance. Les coordonnees de reference d'une commune ne sont pas necessaires au frontend.

Le repository preselectionne les communes dans une enveloppe latitude/longitude
contenant le cercle spherique. Cette selection SQL utilise l'index geographique
existant et conserve les deux cotes de l'antimeridien; un cercle atteignant un
pole ne filtre pas la longitude. Le domaine applique ensuite la distance exacte,
le rayon et le tri habituels. Aucune limite arbitraire n'est appliquee aux
candidats avant ce calcul: les communes proches ne sont pas perdues lorsque
le referentiel national grandit.

La selection manuelle `GET /public/referencement/villes?nom=...` retourne au plus
20 suggestions par defaut pour un prefixe non vide. `limit` (1 a 100) et `offset`
permettent de parcourir les suggestions avec un ordre stable `(nom, id)`.
Les caracteres `%` et `_` sont litteraux. Sans prefixe, le contrat historique
de liste complete est conserve pour les selecteurs existants; les clients
peuvent egalement demander des pages explicites avec `limit` et `offset`.

## Confidentialite et securite

- l'autorisation du navigateur est demandee apres une action explicite ;
- la position exacte n'est ni stockee en base, ni ajoutee a l'audit, ni envoyee aux analytics ;
- les logs techniques excluent les parametres latitude et longitude ou les reduisent a un indicateur de presence ;
- le endpoint est borne et soumis au rate limiting public ;
- la commune choisie peut etre stockee localement, mais pas les coordonnees exactes ;
- aucune geolocalisation IP silencieuse n'est incluse au MVP.

## Strategie de repli

La selection manuelle d'une ville et le mode sans commune sont disponibles sans geolocalisation. En cas de refus, erreur, timeout ou resultat vide, le frontend affiche une explication courte et ces deux choix sans redemander l'autorisation en boucle.

En mode `AUCUNE`, la Marketplace reste consultable mais les cinq widgets territorialises de l'accueil ne sont pas rendus. Aucun contenu global ne doit etre presente dans ces emplacements comme s'il etait local.

Le navigateur memorise le mode choisi. `AUTOUR_DE_MOI` provoque une nouvelle acquisition ponctuelle de la position lors d'une prochaine session si l'autorisation est disponible ; `VILLE_PREFEREE` restaure son `ville_id` s'il est toujours publiable et georeference ; `AUCUNE` conserve l'accueil non territorialise.

## Contextualisation des widgets d'accueil

Le contexte de proximite concerne exclusivement :

1. `Coffret du moment` ;
2. `Communes disponibles` ;
3. `Les animations a vivre pres de chez vous` ;
4. `En ce moment` ;
5. `Derniers coffrets ajoutes`.

| Mode | Perimetre des cinq widgets |
| --- | --- |
| `AUTOUR_DE_MOI` | Ensemble des communes publiees et georeferencees dans le rayon backend, `30 km` par defaut |
| `VILLE_PREFEREE` | Ensemble des communes publiees dans le meme rayon autour des coordonnees de la ville choisie |
| `AUCUNE` | Widgets territoriaux non affiches |

Les cinq widgets utilisent exactement la liste de communes retournee par le backend. Cette preference n'est pas appliquee implicitement aux catalogues, a la recherche, aux pages ville, commercant, coffret ou animation.

Une projection backend dediee a l'accueil compose les cinq resultats avec un tri global par widget, sans etendre a toute la Marketplace les filtres multi-communes. Les endpoints publics existants restent utilisables independamment sur leurs autres surfaces.

Le contrat implemente est `POST /public/referencement/villes/proches/accueil`. Il accepte exactement la meme origine que la recherche de communes et retourne :

- `contexte` : origine, rayon effectif et communes eligibles ;
- `widgets.coffretDuMoment` : un classement unique sur tout le rayon ;
- `widgets.communesDisponibles` : les huit premieres communes de la liste
  canonique du contexte ; la projection des contenus continue d'utiliser toutes
  les communes eligibles du contexte ;
- `widgets.animationsProches` : au plus quatre animations publiques a venir ou en cours ;
- `widgets.enCeMoment` : au plus cinq signaux publics, dedupliques avant limitation,
  puis tries globalement par date de publication decroissante et poids editorial
  decroissant, avec departage par identifiant ; ce plafond est fixe cote serveur ;
- `widgets.derniersCoffretsAjoutes` : au plus six coffrets actifs, d'apres leur activite d'activation publique.

Un resultat territorial vide produit cinq listes vides. Il n'existe aucun repli implicite vers des contenus globaux. Le endpoint applique le meme rate limiting public que la recherche de proximite et interdit le cache partage (`private, no-store`).

## Conception technique implementee

- `CoordonneesGeographiques` porte les bornes et le calcul Haversine dans le domaine ;
- `Ville` porte l'eligibilite territoriale et interdit les paires de coordonnees incompletes ;
- le repository des villes expose uniquement les communes publiees et georeferencees ;
- `RechercherVillesProches` orchestre les deux origines sans dependance SQLAlchemy ;
- une projection de lecture d'infrastructure compose les widgets sans diluer les invariants du domaine ;
- le catalogue des animations et le classement du coffret du moment acceptent en interne un ensemble de communes, sans modifier leurs contrats publics existants ;
- l'adaptateur `GeoApiGouvCommunesClient` est reserve au Backoffice et ne participe jamais au chemin public ;
- les migrations `v185` et `v186` ajoutent les donnees puis leurs contraintes sans modifier le checksum d'une migration deja appliquee.

## Restant hors implementation backend

- parcours de consentement, stockage local du mode et affichage conditionnel dans la Marketplace ;
- eventuel batch de reprise des communes historiques, apres validation operateur des rapprochements ambigus ;
- mesure produit anonymisee, si elle est retenue ulterieurement.

## Documents complémentaires du dossier

- [Epic 52 - Accueil Marketplace contextualise par geolocalisation](parcours-utilisateur.md)

[Retour à l’index des spécifications](../INDEX.md)
