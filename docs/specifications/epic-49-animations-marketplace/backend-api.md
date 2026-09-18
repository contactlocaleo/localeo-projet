# Epic 49 - Conception backend et contrats API

> Consolidation des copies backend et Marketplace. Les compléments backend
> sur `CLOTUREE` et `statuts_publics` sont conservés : leur absence dans l'ancienne
> copie frontend ne constitue pas une suppression du contrat. Les dates de recette
> du document restent celles de la source, sans validation de déploiement nouvelle.

## 1. Objectif backend

Fournir a la Marketplace des projections publiques, coherentes et performantes des animations. Le domaine `animation_locale` demeure la source de verite. Le backend doit interdire toute exposition lorsque l'animation, sa periode, son couple partenaire-ville ou son abonnement ne sont plus eligibles.

## 2. Ecarts a corriger

L'implementation actuelle :

- selectionne toutes les animations puis filtre en memoire ;
- applique `limit` avant de calculer `count` ;
- appelle le detail public pour chaque ligne ;
- ne controle pas l'abonnement dans la liste ni dans le detail ;
- accepte seulement un filtre `commune_id` ;
- retourne `commune.active = true` en dur ;
- retourne le dictionnaire `regles` sans contrat public fin ;
- ne retourne ni statut public derive, ni ouverture d'inscription, ni URL de visuel.

Ces points doivent etre corriges dans un service applicatif dedie et non directement dans les fonctions FastAPI.

## 3. Composants proposes

### 3.1 `PredicatEligibiliteAnimationPublique`

Ce composant porte l'unique regle utilisee par liste, detail, synthese et recherche. Il recoit une horloge afin de rester testable.

Une animation est eligible si :

1. son statut metier est `PUBLIEE` ou `EN_COURS` ;
2. sa configuration courante existe et contient des dates valides ;
3. `date_fin` est strictement posterieure a maintenant ;
4. `date_debut` se situe dans l'horizon configure par `LOCALEO_ANIMATION_PUBLIC_HORIZON_DAYS`, soit 90 jours par defaut ;
5. la commune referencee existe dans l'unique table historique `villes` et est publiee sur la Marketplace ;
6. l'abonnement courant du couple `(animation.partenaire_id, animation.commune_id)` est strictement `ACTIF`, a commence et n'est pas arrive a sa date de fin ; `EN_GRACE` est exclu ;
7. l'animation n'est ni `ANNULEE`, ni `CLOTUREE`, ni `ARCHIVEE`.

Le service ne doit jamais evaluer un abonnement a partir de la commune seule : plusieurs partenaires peuvent exister dans une meme commune.

Lorsqu'un abonnement cesse d'etre `ACTIF`, la liste et le detail publics retirent immediatement l'animation, sous reserve du cache HTTP de 60 secondes. Les routes tokenisees d'un participant et les operations de continuite ne reutilisent pas ce predicat de decouverte et restent accessibles selon leurs propres droits.

### 3.2 `ServiceCatalogueAnimationsPubliques`

Responsabilites :

- construire une requete SQL bornee ;
- joindre la configuration courante, la ville et l'abonnement pertinent ;
- appliquer les filtres publics ;
- trier de facon deterministe ;
- enrichir par lots les noms de commercants et coffrets ;
- produire les resumes, details et syntheses avec les memes helpers ;
- ne jamais charger de participant, gain nominatif, achat ou identifiant Stripe.

### 3.3 Depot de lecture

Ajouter un port de lecture public distinct des repositories transactionnels, par exemple `CatalogueAnimationsPubliquesRepository`. Il expose :

- `rechercher(filtres, curseur, taille, now)` ;
- `obtenir_detail_eligible(animation_id, now)` ;
- `calculer_synthese(filtres, now)`.

L'adaptateur SQLAlchemy selectionne la derniere configuration publiee par animation dans une sous-requete. Le filtre `commercant_id` s'appuie d'abord sur le JSONB existant (`commercant_ids`) afin d'eviter une migration fonctionnelle prematuree. Le filtre `coffret_id` cible exclusivement les identifiants presents dans `lots[].coffret_id` de cette configuration, avec la nature publique `LOT_A_GAGNER`. Un index GIN et un test de plan de requete sont a prevoir ; une projection relationnelle ne sera introduite que si les mesures le justifient.

## 4. Statut public

Le statut de cycle de vie et l'ouverture des inscriptions ne doivent pas etre confondus.

| Champ | Valeur | Calcul |
| --- | --- | --- |
| `statut_public` | `A_VENIR` | `now < date_debut` |
| `statut_public` | `EN_COURS` | `date_debut <= now < date_fin` |
| `statut_public` | `CLOTUREE` | cycle de vie de l'animation en statut `CLOTUREE` |
| `inscription_ouverte` | booleen | animation eligible et `now < date_fin`, sous reserve des regles futures d'inscription |

`INSCRIPTIONS_OUVERTES` est donc un indicateur fonctionnel, pas un second statut concurrent de `A_VENIR`, `EN_COURS` ou `CLOTUREE`. Une animation cloturee n'est jamais ouverte aux inscriptions.

## 5. Contrats HTTP

### 5.1 Liste publique

`GET /public/animation-locale/animations`

Parametres :

| Parametre | Type | Regle |
| --- | --- | --- |
| `commune_id` | UUID optionnel | Identifiant de la commune dans l'unique referentiel stocke dans `villes` |
| `commercant_id` | UUID optionnel | Present dans `commercant_ids` de la configuration publiee |
| `coffret_id` | UUID optionnel | Present dans `lots[].coffret_id` de la configuration publiee ; nature publique `LOT_A_GAGNER` |
| `statut_public` | `A_VENIR`, `EN_COURS` ou `CLOTUREE` | Filtre singulier conserve pour compatibilite |
| `statuts_publics` | liste repetable optionnelle | Union des statuts demandes ; valeurs `A_VENIR`, `EN_COURS`, `CLOTUREE` |
| `inscription_ouverte` | booleen optionnel | Filtre independant du statut |
| `cursor` | chaine opaque | Position dans le tri stable |
| `page_size` | entier 1 a 50 | Defaut 20 |
| `limit` | entier 1 a 100 | Alias historique deprecie pendant la migration |

Ordre stable :

1. `EN_COURS` avant `A_VENIR`, puis `CLOTUREE` lorsqu'il est demande ;
2. `date_debut` croissante ;
3. `animation_id` croissant comme departage.

Sans filtre de statut, le catalogue conserve son comportement de decouverte et retourne seulement `A_VENIR` et `EN_COURS`. Exemple pour consulter les animations actives et cloturees d'une commune :

`GET /public/animation-locale/animations?commune_id={uuid}&statuts_publics=EN_COURS&statuts_publics=CLOTUREE`

Reponse additive :

```json
{
  "items": [],
  "count": 0,
  "pagination": {
    "page_size": 20,
    "total": 0,
    "next_cursor": null
  }
}
```

Pendant la compatibilite, `count` reste le nombre d'elements de `items`. `pagination.total` est le total eligible avant pagination.

### 5.2 Detail public

`GET /public/animation-locale/animations/{animation_id}`

- applique le predicat complet ;
- retourne `404` si la ressource est absente ou ineligible ;
- reutilise la meme projection que la liste ;
- ajoute description complete, commercants, lots et regles publiques ;
- ne retourne pas les donnees d'abonnement, les achats des lots ou les donnees participant.

### 5.3 Synthese territoriale

`GET /public/animation-locale/animations/synthese`

Cette route doit etre declaree avant `/{animation_id}`.

Parametres : `commune_id`, `commercant_id`, `coffret_id`.

Reponse :

```json
{
  "total_a_decouvrir": 12,
  "total_a_venir": 8,
  "total_en_cours": 4,
  "total_inscriptions_ouvertes": 12,
  "total_communes": 6,
  "programme_actif": true,
  "communes": [
    {
      "id": "uuid",
      "nom": "Saint-Loubes",
      "code_postal": "33450",
      "nombre_animations": 3,
      "nombre_en_cours": 1,
      "prochaine_date": "2026-09-01T08:00:00Z"
    }
  ]
}
```

`total_inscriptions_ouvertes` peut recouvrir `total_a_venir` et `total_en_cours`. `total_a_decouvrir` compte chaque animation une seule fois.

### 5.4 Visuel public

`GET /public/animation-locale/animations/{animation_id}/visuel`

- controle l'eligibilite avant de servir le document ;
- sert le visuel principal, puis l'apercu du flyer si autorise ;
- retourne `404` si aucun visuel n'est disponible ;
- retourne `ETag`, `Content-Type` et une politique de cache publique ;
- ne redirige jamais vers une URL de stockage prive non signee.

## 6. Schemas de reponse

### `AnimationPubliqueResumePayload`

- `id`, `nom`, `description_courte` ;
- `modele_code`, `type_animation` ;
- `commune { id, nom, code_postal }` ;
- `date_debut`, `date_fin` ;
- `statut_public`, `inscription_ouverte` ;
- `visuel_url`, `detail_url` ;
- `nombre_commercants`, `nombre_lots`.

### `AnimationPubliqueDetailPayload`

Etend le resume avec :

- `description` ;
- `commercants[] { id, nom, image_uri }` ;
- `lots[] { coffret_id, nom, quantite, ordre, nature }` ;
- `regles_participation`, projection issue d'une liste blanche ;
- `inscription_url` lorsque l'inscription est ouverte.

Le champ historique `regles` peut etre conserve pendant la migration, mais son contenu doit etre assaini par la meme liste blanche.

## 7. Erreurs et securite

- `404` : animation inexistante, ineligible ou visuel absent ;
- `422` : filtre ou curseur invalide ;
- `429` : limitation de debit si elle est activee ;
- `500` : erreur technique avec `correlationId`, sans detail interne.

Les routes sont sans authentification, mais restent soumises aux protections HTTP publiques, a la limitation de debit et a la journalisation sans PII. Les tokens participant ne doivent jamais apparaitre dans ces projections, les logs, le cache ou les analytics.

## 8. Cache et invalidation

La proposition V1 est un cache HTTP court, sans cache applicatif :

```http
Cache-Control: public, max-age=60, stale-while-revalidate=300
```

Le detail d'une animation non eligible ne doit pas etre mis en cache positivement. Si un cache serveur est ajoute plus tard, ses cles devront inclure tous les filtres et etre invalidees lors de publication, annulation, cloture, modification de dates, suspension/expiration d'abonnement et changement de publication de la commune.

## 9. Donnees et migration

- `commune` est le terme metier canonique et continue de reposer sur l'unique table historique `villes` ; aucune table `communes` n'est creee ;
- ajout d'un indicateur `publiee_marketplace` sur ce referentiel existant, avec migration des communes deja exposees ;
- ajout de `visuel_principal_asset_id` dans la configuration versionnee ;
- ajout de `LOCALEO_ANIMATION_PUBLIC_HORIZON_DAYS` avec une valeur par defaut de `90` et une validation strictement positive ;
- index de lecture sur animations, abonnements et JSONB de configuration ;
- aucune copie des noms de commune, commercant ou coffret dans le domaine animation.

## 10. Tests backend

### Tests de domaine et application

- matrice complete des statuts animation et abonnement ;
- bornes exactes de `date_debut`, `date_fin` et horizon ;
- statut public independant de l'ouverture d'inscription ;
- meme resultat d'eligibilite pour liste, detail et synthese ;
- filtrage commercant et coffret sur la version courante ;
- liste blanche des regles publiques.

### Tests API

- pagination, curseur, tri et combinaison des filtres ;
- compatibilite de `limit` ;
- `count` et `pagination.total` ;
- route `/synthese` non capturee par `/{animation_id}` ;
- `404` apres suspension ou expiration ;
- absence de PII et de donnees d'abonnement dans chaque schema ;
- en-tetes de cache et `correlationId` des erreurs.

### Tests infrastructure

- absence de N+1 avec un volume representatif ;
- plan de requete utilisant les index attendus ;
- migration reversible et schema readiness ;
- retrait visible dans le delai de cache maximal.

## 11. OpenAPI et exploitation

- modeliser chaque reponse, y compris les erreurs ;
- documenter les champs historiques deprecies ;
- regenerer [Contrat OpenAPI EPIC 41](../epic-41-api/openapi.json) ;
- copier le contrat stabilise dans le projet Marketplace ;
- ajouter les nouvelles configurations a la reference d'environnement et a la page Configuration deployee ;
- ajouter les controles de disponibilite de la projection publique au cahier de recette avant MEP.
