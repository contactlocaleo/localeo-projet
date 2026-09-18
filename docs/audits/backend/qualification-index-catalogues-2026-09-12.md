# Qualification des index catalogue — 12 septembre 2026

Le script `scripts/performance/profile_catalogue_indexes.py` compare les vraies
requêtes des repositories dans un schéma PostgreSQL local jetable. Il crée
20 000 coffrets et 10 000 commerçants répartis sur 100 communes, ainsi que
36 000 villes géoréférencées. Les colonnes, index et contraintes uniques des
modèles sont reproduits ; les index candidats sont exclus du socle de comparaison.
Les tables, données et index sont annulés en fin de transaction, même en cas
d'échec. Aucun environnement distant ni donnée applicative n'est modifié.

## Changements retenus

La migration `v231_index_catalogues_pagines.sql` ajoute trois index B-tree :

- coffrets : `(ville_id, statut, nom, id)` pour une commune ;
- coffrets : `(statut, nom, id)` pour le catalogue global ;
- commerçants : `(ville_id, statut, nom, id)` pour une commune.

Le curseur des coffrets compare désormais le tuple `(nom, id)` à la position
précédente. PostgreSQL peut ainsi commencer à cette position dans l'index.
L'ancienne disjonction `nom > ... OR (nom = ... AND id > ...)` parcourait toutes
les lignes précédentes avant d'appliquer le filtre.

Les bornes géographiques sont transmises en `Decimal`, conformément aux colonnes
`NUMERIC`. Les paramètres flottants entraînaient une conversion de chaque colonne
en `double precision`, empêchant l'utilisation de l'index géographique existant.
Les tests conservent les résultats, y compris près des pôles et de l'antiméridien.

## Mesures

PostgreSQL 18.3 local, buffers chauds, médiane de cinq `EXPLAIN (ANALYZE, BUFFERS)`.
Le tableau reprend le dernier tir séquentiel, sans les tests exécutés en parallèle.
Les temps varient avec la charge de la machine ; les blocs consultés et les plans
montrent le changement structurel. Ce ne sont pas des latences HTTP ni des mesures
de capacité de l'environnement déployé.

| Requête | Avant : ms / blocs | Après : ms / blocs |
|---|---:|---:|
| 100 coffrets, catalogue global | 7,00 / 1 429 | 0,06 / 40 |
| 100 coffrets après curseur, avec index : disjonction puis tuple | 6,85 / 4 236 | 0,07 / 41 |
| 100 coffrets d'une commune | 0,44 / 202 | 0,17 / 104 |
| 24 commerçants d'une commune | 0,14 / 102 | 0,12 / 27 |
| Villes à 20 km : paramètres flottants puis Decimal, mêmes index | 31,16 / 410 | 0,75 / 81 |

Les index supplémentaires suivants ont été évalués puis écartés :

- `(statut, nom, id)` des commerçants : l'index unique existant `(nom, ville_id)`
  sert déjà le tri global ; gain irrégulier et limité, surtout hors pages profondes ;
- index géographique partiel des seules villes publiées : gain modeste après
  correction des paramètres ; l'index géographique existant suffit ;
- `lower(nom) text_pattern_ops` : inutilisé par le prédicat `ILIKE` actuel.
  L'ajouter seul ne corrigerait pas les scans des suggestions. Aucun changement
  de collation, de sémantique de recherche ou extension PostgreSQL n'est ajouté.

Les suggestions restent bornées en sortie ; un préfixe peu sélectif ou absent du
lexique peut encore entraîner un parcours plus large en base. Le rapport JSON
permet de qualifier séparément ce cas si le volume ou la charge le justifie.

## Reproduction et livraison

```powershell
$env:LOCALEO_PERF_LOCAL_DATABASE_URL = 'postgresql+psycopg://postgres@127.0.0.1:55439/base_locale'
python scripts/performance/profile_catalogue_indexes.py --output tmp/catalogue-indexes.json
```

Le JSON contient les plans complets et les index utilisés, sans URI de connexion.
Le script vérifie l'identité des résultats avant/après chaque groupe d'index et
entre les anciens/nouveaux prédicats. Il exécute aussi la migration exacte deux
fois dans le schéma jetable pour vérifier sa compatibilité et son idempotence.

Validation complémentaire : 25 tests passent pour la proximité, les enveloppes
géographiques, les suggestions et le catalogue de 600 coffrets comportant 500
exclusions réelles de vendabilité, avec égalités de noms et pagination complète.

Le runner `scripts/database/apply_migrations.py` découvre automatiquement les fichiers
`v*.sql` ; aucun registre statique supplémentaire n'est requis. La v231 utilise
une transaction normale, compatible avec ce runner, et conserve les index simples
existants. La création des index bloque temporairement les écritures sur les deux
tables : planifier son passage lors du déploiement selon leur volume. Elle n'a
pas été appliquée sur les environnements partagés pendant cet audit.
