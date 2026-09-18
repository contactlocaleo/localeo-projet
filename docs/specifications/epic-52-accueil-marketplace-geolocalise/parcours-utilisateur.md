# Epic 52 - Accueil Marketplace contextualise par geolocalisation

## Objet

La Marketplace propose un accueil local a partir soit d'une position ponctuelle autorisee par le visiteur, soit d'une commune de preference. Le visiteur peut aussi choisir de ne fournir aucun contexte territorial.

Évolution du 13 septembre 2026 : commune détectée, disponibilité des coffrets dans cette commune et aux alentours, bandeau et en-tête contextualisés.

Le backend est seul responsable du rayon, de l'eligibilite des communes et de l'agregation des contenus. La Marketplace gere le consentement, la preference locale et la presentation des cinq widgets, sans recalculer les distances ni appeler directement une API geographique externe.

## Documents

- [Backlog Epic 52](../../roadmap/terminees/epic-52-accueil-marketplace-geolocalise-backlog.md)
- [Epic backend de reference](README.md)

## Parcours retenu

```text
Ouverture de l'accueil
        |
        +-- preference absente -> expliquer les choix
        |       +-- Autour de moi -> clic explicite -> navigator.geolocation
        |       +-- Ville preferee -> selecteur de commune
        |       +-- Aucune -> accueil sans widgets territoriaux
        |
        +-- AUTOUR_DE_MOI -> nouvelle position ponctuelle si autorisee
        +-- VILLE_PREFEREE -> reutiliser le ville_id s'il reste eligible
        +-- AUCUNE -> ne pas appeler la projection territoriale
```

La demande native de geolocalisation n'est jamais affichee avant une action explicite. Un refus, un timeout ou une erreur conduit au choix d'une commune ou au mode `AUCUNE`, sans bloquer le reste de la Marketplace.

## Preference navigateur

Stockage local versionne recommande :

```json
{
  "version": 1,
  "mode": "AUTOUR_DE_MOI | VILLE_PREFEREE | AUCUNE",
  "villeId": "uuid optionnel"
}
```

Regles :

- ne jamais stocker latitude, longitude, precision ou historique de positions ;
- `villeId` est present uniquement en mode `VILLE_PREFEREE` ;
- la preference persiste jusqu'au changement explicite ou a l'effacement du stockage local ;
- une commune restauree devenue ineligible provoque un retour au choix territorial ;
- la position exacte ne doit pas apparaitre dans une URL du navigateur, une query key React Query, un log Localeo ou un evenement analytics.

## Contrats backend disponibles

### Communes proches

```http
POST /public/referencement/villes/proches/rechercher
```

Origine GPS :

```json
{
  "origine": {
    "type": "POSITION",
    "latitude": 45.8992,
    "longitude": 6.1294,
    "precisionMetres": 35
  }
}
```

Origine communale :

```json
{
  "origine": {
    "type": "COMMUNE",
    "communeId": "uuid"
  }
}
```

Le backend impose le rayon, `30 km` par defaut, et retourne les communes publiees et georeferencees triees par distance.

### Projection des cinq widgets

```http
POST /public/referencement/villes/proches/accueil
```

Le corps est identique. La reponse contient :

- `contexte` : `origineType`, `rayonKm`, `communes`, `communeOrigine` et `localisationStatut` ;
- `disponibilite` : `coffretsCommune`, `coffretsAlentours`, `coffretsParCommune` ;
- `widgets.coffretDuMoment` ;
- `widgets.communesDisponibles` ;
- `widgets.animationsProches` ;
- `widgets.enCeMoment` ;
- `widgets.derniersCoffretsAjoutes`.

La Marketplace consomme cette projection unique. Elle ne lance pas un appel par commune et ne refait aucun tri global cote client.

## Responsabilites

| Sujet | Backend | Marketplace |
|---|---|---|
| Rayon et plafond | Configure et impose | Affiche `rayonKm` si utile |
| Distance Haversine | Calcule | Ne recalcule jamais |
| Eligibilite commune | Commune publiee et georeferencee | Utilise uniquement la reponse |
| API `geo.api.gouv.fr` | Enrichissement Backoffice et résolution ponctuelle de la commune GPS | Aucun appel direct |
| Consentement navigateur | Aucun | Explication et action explicite |
| Position exacte | Traitement en memoire, non persistee | Traitement ponctuel, jamais stocke |
| Preference territoriale | Valide la commune choisie | Stocke mode et `villeId` localement |
| Widgets | Projection multi-communes canonique | Etats chargement, succes, vide et erreur |

La variable backend `LOCALEO_GEO_API_GOUV_COMMUNES_URL` configure l'endpoint communes compatible avec l'API Decoupage administratif. Elle ne doit pas etre exposee dans la configuration runtime du frontend : la Marketplace n'appelle jamais ce fournisseur.

## Integration React Query

- centraliser les deux appels dans `src/services/api.js` ou un service dedie ;
- utiliser `POST` avec un corps JSON ;
- ne pas inclure les coordonnees exactes dans la query key ;
- ne pas persister la requete GPS dans un cache durable ;
- respecter `Cache-Control: private, no-store` ;
- annuler une requete devenue obsolete lors d'un changement de mode ;
- conserver le reste de l'accueil utilisable si la projection territoriale echoue.

## Regles des widgets

Les widgets territorialises sont exclusivement :

1. `Coffret du moment` ;
2. `Communes disponibles` ;
3. `Les animations a vivre pres de chez vous` ;
4. `En ce moment` ;
5. `Derniers coffrets ajoutes`.

Ils sont affiches en modes `AUTOUR_DE_MOI` et `VILLE_PREFEREE`. En mode `AUCUNE`, ils sont absents : aucun contenu global ne doit etre presente comme local. La preference ne filtre pas implicitement les catalogues, la recherche ni les pages ville, commercant, coffret ou animation.

## Etats UX obligatoires

- explication avant consentement ;
- acquisition de position en cours ;
- chargement de la projection ;
- resultat disponible avec commune(s) et rayon ;
- aucune commune dans le rayon ;
- permission refusee ;
- geolocalisation indisponible ou timeout ;
- commune de preference devenue indisponible ;
- erreur API non bloquante.

Tous les etats proposent une action claire : reessayer, choisir une ville, changer de preference ou continuer sans commune. Les messages et boutons sont accessibles au clavier et annonces aux technologies d'assistance.

## Configuration backend a connaitre

```env
LOCALEO_VILLES_PROCHES_RAYON_KM=30
LOCALEO_VILLES_PROCHES_MAX_RAYON_KM=100
LOCALEO_VILLES_PROCHES_MAX_RESULTATS=50
LOCALEO_GEO_API_GOUV_COMMUNES_URL=https://geo.api.gouv.fr/communes
```

La quatrième valeur configure également la résolution de commune depuis la position GPS. Le plafond de résultats s'applique à la recherche de communes proches ; les totaux de l'accueil utilisent toutes les communes du rayon, indépendamment des plafonds des widgets.

## Commune détectée et disponibilité

- `communeOrigine` contient `nom`, `codeInsee` et `villeId` (nul si aucun rattachement Localeo publié). La commune est déterminée par l'API administrative à partir des coordonnées, jamais déduite de la première commune Localeo proche.
- `localisationStatut` vaut `DETECTEE`, `APPROXIMATIVE`, `INDISPONIBLE` ou `CHOISIE`. Une précision absente ou supérieure à 1 000 mètres produit la mention « Position approximative ».
- Le backend effectue un seul appel de résolution, avec un timeout de 1,5 seconde. Une erreur ou une réponse ambiguë conserve la recherche à proximité. Le choix manuel ne sollicite pas ce service.
- Le rapprochement utilise le code INSEE. Si la commune est introuvable et que certaines communes publiées n'ont pas ce code, `coffretsCommune` reste nul : l'interface ne doit pas conclure à zéro offre locale.
- Les compteurs utilisent les coffrets distincts réellement vendables selon les règles du catalogue (dont les contrôles fiscaux et Stripe activés). Ils ne dépendent ni du nombre de prestations ni du nombre de vignettes affichées.
- Les coffrets sont rattachés à la ville du coffret. Les coffrets de la commune d'origine sont exclus du total des alentours et prioritaires dans les sélections. Les autres communes restent classées par distance.
- La commune d'origine reste incluse même si son point de référence est hors du rayon. Une commune sans coordonnées peut être reconnue par son code INSEE ; sa distance reste alors nulle et n'est pas affichée.
- Les distances affichées concernent les points de référence des communes, à vol d'oiseau. Elles ne représentent pas un trajet vers un commerçant.
- Le nom détecté reste uniquement en mémoire pour l'en-tête. Un changement de préférence le réinitialise et annule la requête en cours.

Déployer le backend avant la marketplace : l'ancien schéma refuse le nouveau champ optionnel `precisionMetres`. Aucune migration de schéma n'est nécessaire ; vérifier les codes INSEE des communes publiées dans l'administration. La requête vers le fournisseur contient les coordonnées dans ses paramètres : ne pas journaliser son URL ou ses erreurs brutes.

## Definition de termine

- aucun prompt navigateur sans action explicite ;
- aucune coordonnee exacte stockee, journalisee, mise en URL ou envoyee aux analytics ;
- les modes `AUTOUR_DE_MOI`, `VILLE_PREFEREE` et `AUCUNE` sont modifiables ;
- les cinq widgets utilisent une seule projection backend ;
- aucun de ces widgets n'apparait en mode `AUCUNE` ;
- refus, timeout, vide et erreur ne bloquent ni la navigation ni l'achat ;
- desktop, mobile, clavier et lecteurs d'ecran sont recettables ;
- les autres pages de la Marketplace conservent leur comportement territorial actuel.
