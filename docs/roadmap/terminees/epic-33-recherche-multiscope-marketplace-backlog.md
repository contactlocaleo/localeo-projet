# Backlog Epic 33 - Recherche multi-scope marketplace

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthèse

- Criticité : `Élevée`
- Statut : `Termine`
- Objectif : fournir un service de recherche unique pour la barre de recherche marketplace, capable de retrouver une ville, un commerçant, une prestation ou un coffret par son nom.
- Décision produit : les résultats sont priorisés par scope dans l'ordre `Ville`, puis `Commerçant`, puis `Prestation`, puis `Coffret`.
- Décision d'usage : la recherche sert d'abord l'intention de navigation rapide vers une page ville, une fiche commerçant, une prestation ou un coffret.
- Décision technique : le service expose un contrat public stable, avec typage du scope, libellé affichable et cible de navigation typée ; le frontend reste responsable de construire les URLs finales.

## Problème

La marketplace a besoin d'une barre de recherche transversale. Aujourd'hui, les parcours publics sont principalement structurés par pages et listes dédiées. Un visiteur qui connaît déjà une ville, un commerçant, une prestation ou un coffret doit pouvoir retrouver rapidement la bonne destination sans comprendre la structure interne du catalogue.

## Risque business

- Un visiteur peut abandonner s'il ne retrouve pas rapidement une ville, un commerçant, une prestation ou un coffret connu.
- Les commerçants référencés sont moins visibles si la navigation dépend uniquement des listes éditoriales.
- Les coffrets peuvent être difficiles à retrouver quand le catalogue s'élargit.
- Une recherche non priorisée peut renvoyer un coffret avant une ville homonyme, alors que la ville est l'entrée de navigation la plus structurante.

## Risque technique

- Mélanger des entités de nature différente sans contrat clair peut rendre l'IHM fragile.
- Une recherche trop large peut exposer des commerçants, prestations ou coffrets non publiables.
- Les performances peuvent se dégrader si chaque scope est interrogé sans limite ni index adapté.
- L'absence de normalisation peut rendre les résultats sensibles aux accents, majuscules ou pluriels.
- Une priorité mal définie peut créer des résultats instables entre deux appels.

## Périmètre MVP

- Rechercher par texte libre sur le nom d'une ville, d'un commerçant, d'une prestation ou d'un coffret.
- Retourner des résultats multi-scope dans un ordre stable :
  1. villes ;
  2. commerçants ;
  3. prestations ;
  4. coffrets.
- Limiter le nombre de résultats par scope et le nombre total de résultats.
- Normaliser la recherche pour ignorer casse et accents.
- Exclure les entités non publiables de la marketplace.
- Retourner pour chaque résultat :
  - `scope` ;
  - `id` ou référence publique ;
  - `label` ;
  - `subtitle` si utile ;
  - `target` de navigation typée, sans URL finale ;
  - `score` ou rang interne si nécessaire au diagnostic.
- Fournir un endpoint public utilisable par la barre de recherche marketplace.
- Ajouter des tests sur l'ordre de priorité, la visibilité publique et la normalisation.

## Hors périmètre MVP

- Recherche full-text avancée avec synonymes métier.
- Recherche géographique par distance.
- Suggestions personnalisées.
- Historique de recherche utilisateur.
- Analytics détaillés de requêtes.
- Recherche sur descriptions longues, tags, activités ou commentaires.
- Autocomplétion typo-tolérante avancée.
- Moteur externe type Meilisearch, Algolia ou Elasticsearch.

## User Stories

1. `PRD-233` En tant que visiteur marketplace, je veux rechercher une ville par son nom afin d'accéder rapidement à son catalogue local.
   - Statut : `Termine`
   - Résultat attendu : une ville publiable correspondant à la requête apparaît dans les résultats de type `VILLE`.
   - Résultat attendu : les villes sont toujours présentées avant les autres scopes.

2. `PRD-234` En tant que visiteur marketplace, je veux rechercher un commerçant par son nom afin d'accéder rapidement à sa fiche publique.
   - Statut : `Termine`
   - Résultat attendu : seuls les commerçants publiables et visibles sur la marketplace sont retournés.
   - Résultat attendu : les commerçants sont présentés après les villes et avant les coffrets.

3. `PRD-235` En tant que visiteur marketplace, je veux rechercher un coffret par son nom afin d'accéder rapidement à l'offre correspondante.
   - Statut : `Termine`
   - Résultat attendu : seuls les coffrets actifs ou publiables sur la marketplace sont retournés.
   - Résultat attendu : les coffrets sont présentés après les villes, les commerçants et les prestations.

4. `PRD-235 bis` En tant que visiteur marketplace, je veux rechercher une prestation par son nom afin d'accéder rapidement à l'offre ou au coffret qui la porte.
   - Statut : `Termine`
   - Résultat attendu : seules les prestations actives et exposables sur la marketplace sont retournées.
   - Résultat attendu : les prestations sont présentées après les commerçants et avant les coffrets.

5. `PRD-236` En tant qu'application marketplace, je veux consommer un endpoint unique de recherche multi-scope afin d'alimenter une barre de recherche simple.
   - Statut : `Termine`
   - Résultat attendu : l'API accepte une requête texte et retourne une liste homogène de résultats typés.
   - Résultat attendu : le contrat fournit une cible typée exploitable par le frontend, sans imposer l'URL finale.

6. `PRD-237` En tant que système, je veux appliquer une priorité de résultats par scope afin de garantir un ordre stable et compréhensible.
   - Statut : `Termine`
   - Résultat attendu : l'ordre global est toujours `VILLE`, puis `COMMERCANT`, puis `PRESTATION`, puis `COFFRET`.
   - Résultat attendu : à l'intérieur de chaque scope, les résultats sont triés par pertinence puis par nom.

7. `PRD-238` En tant que système, je veux normaliser la recherche afin que les accents et la casse ne bloquent pas la découverte.
   - Statut : `Termine`
   - Résultat attendu : `cafe`, `Café` et `CAFÉ` peuvent produire les mêmes correspondances.
   - Résultat attendu : la normalisation reste côté backend pour garder un comportement uniforme.

8. `PRD-239` En tant qu'exploitant, je veux que la recherche respecte strictement la visibilité publique afin de ne pas exposer de contenu non publié.
   - Statut : `Termine`
   - Résultat attendu : les villes, commerçants, prestations et coffrets non publiables sont exclus.
   - Résultat attendu : les règles de statut existantes du catalogue sont réutilisées.

9. `PRD-240` En tant que responsable produit, je veux pouvoir faire évoluer les scopes de recherche sans casser l'IHM afin d'ajouter plus tard activités, suggestions ou nouveaux types de résultats.
   - Statut : `Termine`
   - Résultat attendu : le contrat API est extensible par `scope` sans changer la structure de base d'un résultat.

## Règles de gestion

- La recherche est publique et ne doit retourner que des entités visibles sur la marketplace.
- La requête minimale recommandée est de 2 caractères après trim.
- Une requête vide ou trop courte retourne une liste vide ou une erreur fonctionnelle légère selon le contrat API retenu.
- L'ordre de priorité inter-scope est strict : `VILLE`, `COMMERCANT`, `PRESTATION`, `COFFRET`.
- Une correspondance ville ne masque pas les commerçants, prestations ou coffrets correspondants si la limite totale permet de les afficher.
- Les limites sont configurables ou explicites dans le contrat, par exemple `limit_total` et `limit_par_scope`.
- La recherche ignore la casse et les accents.
- Le backend ne retourne pas d'URL finale de page frontend ; il retourne une cible typée permettant au frontend de décider la route.
- Le backend reste responsable de la visibilité, de la priorité et de la normalisation.

## Modèle de réponse cible

```json
{
  "query": "lyon",
  "results": [
    {
      "scope": "VILLE",
      "id": "ville-uuid",
      "label": "Lyon",
      "subtitle": "12 commerçants partenaires",
      "target": {
        "type": "VILLE",
        "id": "ville-uuid",
        "slug": "lyon"
      }
    },
    {
      "scope": "COMMERCANT",
      "id": "commercant-uuid",
      "label": "Maison Lyonnaise",
      "subtitle": "Épicerie fine à Lyon",
      "target": {
        "type": "COMMERCANT",
        "id": "commercant-uuid",
        "slug": "maison-lyonnaise"
      }
    },
    {
      "scope": "PRESTATION",
      "id": "prestation-uuid",
      "label": "Atelier dégustation",
      "subtitle": "Maison Lyonnaise",
      "target": {
        "type": "PRESTATION",
        "id": "prestation-uuid",
        "commercant_id": "commercant-uuid"
      }
    },
    {
      "scope": "COFFRET",
      "id": "coffret-uuid",
      "label": "Découverte lyonnaise",
      "subtitle": "Coffret local",
      "target": {
        "type": "COFFRET",
        "id": "coffret-uuid",
        "slug": "decouverte-lyonnaise"
      }
    }
  ]
}
```

## API cible

- `GET /public/recherche?q={query}`
- Paramètres optionnels :
  - `limit_total`
  - `limit_par_scope`
- Réponse : liste ordonnée de résultats typés avec cible de navigation, sans URL frontend finale.
- Authentification : aucune.
- Sécurité : aucune donnée privée ou back-office ne doit être exposée.

## Lots d'implémentation

### Lot 1 - Contrat et règles

- Définir les scopes `VILLE`, `COMMERCANT`, `PRESTATION`, `COFFRET`.
- Définir le DTO de résultat public.
- Définir les limites, la requête minimale et les règles de tri.
- Documenter les statuts publics éligibles par scope.

### Lot 2 - Recherche backend

- Ajouter un use case `RechercherMarketplaceMultiScope`.
- Ajouter les méthodes repository nécessaires.
- Implémenter la normalisation casse/accents.
- Appliquer la priorité stricte par scope.
- Appliquer les limites par scope et totale.

### Lot 3 - API publique

- Ajouter `GET /public/recherche`.
- Exposer un contrat stable pour la barre de recherche marketplace.
- Ajouter erreurs ou réponses vides sur requête trop courte.
- Vérifier que les cibles de navigation retournées sont typées et suffisantes pour le frontend.

### Lot 4 - Performance et indexation

- Vérifier les index existants sur les noms recherchés.
- Ajouter des index si nécessaire.
- Mesurer le comportement avec un catalogue réaliste.
- Encadrer les limites pour éviter une requête trop coûteuse.

### Lot 5 - Tests

- Tester ville avant commerçant avant prestation avant coffret.
- Tester normalisation casse/accents.
- Tester exclusion des entités non publiables.
- Tester limites par scope et limite totale.
- Tester requête vide ou trop courte.

## Definition of Done

- L'API publique de recherche multi-scope est disponible.
- La barre de recherche marketplace peut consommer un endpoint unique.
- Les résultats sont toujours ordonnés `Ville`, puis `Commerçant`, puis `Prestation`, puis `Coffret`.
- Les recherches ignorent casse et accents.
- Les entités non publiables ne sont jamais retournées.
- Le contrat de réponse permet au frontend de construire la navigation marketplace sans URL imposée par le backend.
- Les limites protègent l'API contre les requêtes trop larges.
- Les tests couvrent priorité, visibilité, normalisation et limites.

## Points arbitres restants

- Aucun point en suspens identifié à ce stade.
