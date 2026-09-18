# Validation des lectures a volume croissant - 12 septembre 2026

Ce controle complete l'[audit des consultations](audit-performance-recherches-consultations-2026-09-12.md)
et le [suivi des implementations](suivi-implementation-performance-2026-09-12.md).
Les durees locales incluent SQL, transfert vers Python et construction de la
reponse. Elles ne constituent pas un engagement de capacite ou de p95 sous
charge nominale.

## Methode reproductible

`scripts/performance/profile_read_volume.py` cree un schema PostgreSQL local
isole, copie les colonnes et indexes des modeles concernes, genere uniquement
des lignes synthetiques puis annule toute la transaction. Il n'applique aucune
migration, ne lit aucun fournisseur et refuse une cible hors loopback. Les
contraintes de graphes metier non utiles aux lectures ne sont pas reproduites;
ce jeu mesure les projections, pas les parcours d'achat ou leur coherence.

```powershell
$env:LOCALEO_PERF_LOCAL_DATABASE_URL = 'postgresql+psycopg://postgres@127.0.0.1:55439/postgres'
python scripts/performance/profile_read_volume.py --output output/performance/optimisations-20260912/volumes.json
```

Un passage chauffe les caches avant chaque mesure. Les SELECT sont comptes,
leurs lignes retournees additionnees, puis les requetes capturees sont executees
avec `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`. Seules les metriques et noms
d'indexes sont conserves, sans parametres ni contenus des reponses.

## Achats et chronologie apres optimisation

| Cas | SELECT | Lignes retournees | Duree locale chaude |
| --- | ---: | ---: | ---: |
| 6 000 achats, premiere page de 25 | 2 | 26 | 92 ms |
| Reference de l'achat le plus ancien | 2 | 2 | 115 ms |
| Filtre alertes sur les 6 000 achats sans alerte | 1 | 1 | 237 ms |
| Chronologie de 3 000 communications, page de 50 | 2 | 52 | 55 ms |

La recherche reste complete au-dela de l'ancienne borne 500. Le filtre d'alertes
travaille sur les faits SQL de tous les candidats avant le total: son cout en
base croitra avec l'historique, sans rapatrier cet historique en Python.
Les tests de chronologie parcourent aussi les 3 000 evenements par pages de
100 avec dates egales, sans perte ni doublon et avec au plus 101 evenements
transmis par page.

Les deux plans de la recherche courante executent respectivement 5,6 et 14,9 ms.
Ils utilisent la cle primaire et l'index existant sur `commande_achat_id` pour
les enfants de la page. La recherche textuelle de la reference ancienne reste
une recherche litterale en sous-chaine; ses plans executent 22,8 et 17,2 ms.
Le COUNT avec alertes execute 266,9 ms lors de son EXPLAIN distinct.

Un index candidat `(source_id, COALESCE(date_envoi,date_creation) DESC)` sur les
emails a ete cree uniquement dans le schema jetable. Le plan ne l'a pas retenu
pour cette distribution et la duree du service est passee de 55 a 59 ms.
**Aucune migration d'index n'est justifiee par ce test.** Les index existants
suffisent aux volumes testes; les distributions et historiques reels restent
a mesurer avant toute creation d'index supplementaire.

## Surveillance du dashboard commercant

| Statuts de prestations | Mouvements | SELECT | Lignes retournees | Duree avant agregation |
| ---: | ---: | ---: | ---: | ---: |
| 1 000 | 500 | 3 | 1 501 | 128 ms |
| 10 000 | 5 000 | 3 | 15 001 | 571 ms |
| 30 000 | 15 000 | 3 | 45 001 | 5 299 ms |

Le nombre de SELECT est stable, mais le volume ramene et agrege en Python ne
l'est pas. Au dernier palier, les plans SQL cumulent environ 167 ms; le reste
est principalement le transfert, la conversion et l'agregation applicative.
La surveillance preconisee confirme donc l'interet d'agreger ces lignes en SQL
en preservant periodes locales, versions et montants. Ce point est traite dans
un commit distinct pour comparer les memes fixtures avant et apres.

Apres aggregation SQL du dashboard, sur les memes distributions synthetiques:

| Statuts | Lignes avant | Lignes apres | Duree avant | Duree apres |
| ---: | ---: | ---: | ---: | ---: |
| 1 000 | 1 501 | 4 | 128 ms | 17 ms |
| 10 000 | 15 001 | 4 | 571 ms | 111 ms |
| 30 000 | 45 001 | 4 | 5 299 ms | 234 ms |

Les trois SELECT sont conserves: existence du commercant, groupes de statuts,
sommes de mouvements. Les groupes separent prestation, version historique,
statut et periodes utiles (jour/semaine/mois a Paris). Une date reelle du groupe
reste disponible pour respecter les bornes de recherche, y compris une semaine
ou un mois commence avant la date de debut demandee. Les conditions existantes
du calcul restent appliquees aux groupes ponderes, sans cache financier.

La parite avec les lectures detaillees historiques est testee sur 1 500 lignes
diversifiees, aux bornes de dates et au changement d'heure, pour les trois
granularites, avec/sans versions et avec/sans filtre prestation. Un test a
10 000 statuts verifie trois SELECT et au plus six lignes retournees pour cette
distribution. Le nombre de groupes depend des prestations, versions, statuts
et combinaisons de periodes; quatre lignes n'est donc pas un plafond universel.

La contre-mesure est conservee dans
`output/performance/optimisations-20260912/volumes-dashboard-apres.json`.

## Verification HTTP bornee

`scripts/performance/benchmark_public_reads.py` mesure exclusivement des GET
publics autorises, sans authentification ni redirection, avec borne de
concurrence, debit, delai et taille de reponse. Il ne conserve aucun corps de
reponse. Neuf tests couvrent ses bornes, destinations et percentiles.

```powershell
python scripts/performance/benchmark_public_reads.py --base-url https://test-api.localeo.city --allowed-host test-api.localeo.city --samples 6 --concurrency 2 --max-rps 2 --timeout 5 --output output/performance/optimisations-20260912/http-test-search.json
```

Endpoint: `/public/commercialisation/recherche?q=test&limit_total=8&limit_par_scope=4`.

| Cible | Echantillons | HTTP 200 | Erreurs | p50 | p95 | p99 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| API de test deja deployee | 6 | 6 | 0 | 3 711 ms | 3 914 ms | 3 917 ms |
| Route actuelle via HTTP local | 10 | 10 | 0 | 86 ms | 442 ms | 609 ms |

Les deux sondes utilisent une concurrence maximale de 2 et au plus 2 departs
par seconde. La route locale utilise la base locale d'audit en lecture seule,
un serveur FastAPI minimal et le code corrige. Elle inclut le premier appel
froid, mais exclut les middlewares complets, l'authentification et le reseau
de deploiement. Les percentiles sont descriptifs d'un petit echantillon.

La version deployee sur l'API de test n'a pas ete modifiee ni identifiee par
cette sonde. Ses resultats ne valident donc pas le deploiement des correctifs,
et le tableau ne permet pas de calculer un gain de production entre les deux
environnements. Une campagne k6 nominale reste necessaire apres deploiement
pour mesurer p50/p95/p99, erreurs et attente du pool dans le contexte cible.

Preuves privees: `output/performance/optimisations-20260912/volumes.json`,
`http-test-search.json`, `http-local-search.json` et le harnais HTTP local.
