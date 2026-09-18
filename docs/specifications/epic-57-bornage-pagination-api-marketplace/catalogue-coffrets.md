# Catalogue public de coffrets : contrat de lecture et pagination

La route `GET /public/commercialisation/coffrets/page` retourne les coffrets
vendables, triés par nom puis identifiant. La pagination intervient après les
contrôles de publication, de qualification BUM et de disponibilité Stripe.

| Paramètre | Comportement |
|---|---|
| `ville_id` | Limite les coffrets à une commune. |
| `type_coffret` | Filtre le type avant le chargement des diagnostics. |
| `commercant_id` | Retient les coffrets contenant une prestation active de ce commerçant. |
| `avec_prestations` | Inclut les prestations actives et leur version courante. |
| `page_size` | 24 par défaut, de 1 à 100. |
| `cursor` | Curseur opaque renvoyé par la page précédente. |

La réponse contient `items`, `page_size`, `has_more` et `next_cursor`.
`next_cursor` vaut `null` en fin de catalogue. Le client transmet le curseur
sans le modifier et conserve les filtres de commune, de type et de commerçant.
Changer ces filtres impose de repartir de la première page ; la signature du
curseur empêche sa réutilisation avec un autre périmètre.

La route historique `GET /public/commercialisation/coffrets` conserve une
réponse sous forme de tableau complet. Ses filtres restent compatibles.
Les consommateurs qui parcourent toutes les nouvelles pages doivent attendre
la fin du parcours avant de calculer des totaux globaux et transmettre
l'annulation aux requêtes devenues inutiles.

## Contrôles conservés

- Les listes publiques présélectionnent uniquement les coffrets actifs en SQL.
  Le repository général conserve tous les statuts lorsqu'aucun filtre de statut
  ne lui est fourni.
- Le diagnostic utilise les règles du domaine, y compris les prestations
  brouillon pour lesquelles les règles existantes contrôlent le commerçant.
  Seules les prestations actives sont présentées et comptées dans le catalogue.
- La politique BUM, les qualifications, les commerçants et les prestations sont
  chargés par ensemble de coffrets. La présentation réutilise ces mêmes faits.
- Le détail renvoie une erreur 404 lorsque le coffret n'est pas vendable.
- Aucun cache global de vendabilité n'est ajouté : une suspension BUM ou Stripe
  est prise en compte à la consultation suivante.

## Budgets vérifiés

Les tests PostgreSQL isolés de
`tests/integration/test_catalogue_coffrets_performance.py` utilisent 600 coffrets,
dont 500 exclus par de véritables conditions de statut, BUM, Stripe ou de
référencement. Ils vérifient la complétude, les égalités de noms, les versions de
prestations, les filtres et les modifications de statut immédiates.

Avec les gardes BUM et Stripe activés :

- liste historique avec prestations : 6 SELECT ; détail vendable : 6 SELECT ;
- page suivant directement des candidats vendables : au plus 6 SELECT ;
- première page après les 500 exclusions du jeu : 30 SELECT, soit cinq lots de
  100 candidats après exclusion SQL des 100 brouillons.

Les lectures des candidats sont bornées. Le nombre de lots dépend des exclusions
et peut donc augmenter sur un catalogue très majoritairement non vendable.
Ces budgets concernent les cas d'usage, hors authentification et traitement HTTP.
