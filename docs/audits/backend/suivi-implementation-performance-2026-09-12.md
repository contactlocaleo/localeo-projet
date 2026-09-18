# Mise en oeuvre de l'audit recherche et consultation

Chaque point ci-dessous donne lieu a un commit distinct et a une verification.
Les ajustements des consommateurs sont inclus dans le point correspondant;
une adaptation dans un depot voisin a son propre commit dans ce depot.

| Point | Etat | Commit / validation |
|---|---|---|
| Base : recherche multiscope et audits | Termine | 0c7be86; 55 tests Python, build et 12 tests HTTP Marketplace |
| Detail ville par identifiant | Termine | 6bf9b19; 3 tests: lecture par cle, absence et UUID invalide |
| Lecture dossier ERP sans verrou | Termine | 2891cbb; lecture sans FOR UPDATE et commandes toujours verrouillees |
| Agregation compteurs activites | Termine | 6ecd1d3; 15 SELECT vers 1; 6 tests API, periodes et visibilite preserves |
| Agregation avis du profil public | Termine | 492616d; AVG/COUNT SQL, test moderation/publication/absence |
| Agregation synthese vendabilite | Termine | 0b41439; 11 SELECT vers 2; scope, anciennete, familles et alertes distinctes |
| Catalogue coffrets : lectures groupees, detail et pagination | Termine | a89aed8; 46 SELECT vers 6 avec prestations; 600 coffrets/500 exclus, 4 tests PostgreSQL |
| Catalogue animations : BUM, projections, completude | Termine | 04bcb8a; 35 SELECT vers 9; BUM avant pagination et total, lots absents, detail 404 |
| Recherche Achats 360 | Termine | 1dce870; 306 SELECT vers 2; 606 achats, parite des 14 alertes, totaux exacts |
| Fiche Commercant 360 | Termine | 903f7b9; 43 SELECT vers 9 initiaux; onglets a la demande, 28 tests |
| Connexes Support a la demande | Termine | d80edc1; compteurs 2 SELECT, famille 3; 1000 emails, permissions et DOM |
| Chronologie Achats 360 | Termine | 047afb2; sources SQL bornees; 3000 evenements/30 pages, 15 sources, dates et scope |
| Chronologie Animation 360 | Termine | db8b194; 5000 evenements/50 pages, egalites date/UUID entre familles sans perte |
| Indicateurs Animation 360 | Termine | dab8f0d; 6000 participants et 6000 validations agreges en SQL; cache et autorisations |
| Recherche villes et preselection geographique | Termine | bdd7e85; 48 tests, poles/antimeridien, 600 communes hors rayon exclues en SQL |
| Liste commercants filtree et paginee | Termine | 82aa1ac; 1000 commercants, filtres avant total/page; SDK Marketplace 1b0acb9 |
| OnBoard : pagination et indicateurs | Termine | 672e927; 1200 dossiers; liste 2 SELECT, indicateurs 1; filtre blocage SQL et UI |
| Interfaces : enrichissements, cache et annulation | Termine | Marketplace cd16d76; pagination complete, lectures ciblees, cache scoped, 49 tests Node et build |
| Volumes, pages profondes et mesure HTTP | Termine | 8366f1e; scripts reproductibles, 6000 achats, sonde HTTP locale et test; 9 tests |
| Dashboard commercant a fort historique | Termine | f654175; 45001 lignes vers 4, 5299 ms vers 234 ms; 47 tests dont parite des periodes et versions |
| Qualification des index catalogue et geographiques | Termine | Migration v231 : 3 index mesures, bornes Decimal et curseur tuple; 25 tests et migration rejouee |

Les changements preexistants sans lien avec l'audit restent hors de ces commits.
Les mesures apres correction et leur perimetre exact figurent ci-dessous.

## Mesures sur la base de test, depuis le poste de developpement

Le code local corrige a ete execute en lecture seule sur la meme base de test
que l'audit. Aucun deploiement, changement de donnees ou appel fournisseur.
Les 27 scenarios (deux passages chacun) ont abouti sans erreur. Les durées
ci-dessous sont celles du second passage, pas des percentiles HTTP.

| Scenario | Avant : SQL / ms | Apres : SQL / ms |
|---|---|---|
| Catalogue coffrets avec prestations | 46 / 1087 | 6 / 269 |
| Catalogue animations | 35 / 1222 | 9 / 295 |
| Recherche Achats 360, 25 resultats | 306 / 6854 | 2 / 194 |
| Recherche Achats 360 sans resultat | 10 / 347 | 1 / 86 |
| Synthese initiale Commercant 360 | 42 / 940 | 9 / 321 |
| Objets connexes Support, contrat complet | 19 / 461 | 6 / 201 |
| Compteurs seuls objets connexes Support | non disponible | 2 / 112 |
| Synthese vendabilite | 11 / 326 | 2 / 302 |

La variabilite reseau/poste reste visible : le detail coffret passe de 9 a 6
SELECT mais ce passage mesure 444 ms contre 250 ms dans l'audit initial.
Ces echantillons ne constituent donc pas un engagement de latence. Le gain
structurel et les budgets SQL sont verifies separement par les tests.

La synthese du catalogue animations utilise maintenant 5 SELECT contre 1 :
elle applique enfin les exclusions BUM et ses compteurs concordent avec la
liste publique. Il s'agit aussi d'une correction de completude.

Preuves locales ignorees : `output/performance/consultations-audit-20260912/`
(`profile_after.py`, `local-after.json`, `remote-after.json`). Les rapports
contiennent des compteurs et empreintes SQL, aucun contenu client ni secret.

## Contrats et limites

Le [contrat du catalogue coffrets](../../specifications/epic-57-bornage-pagination-api-marketplace/catalogue-coffrets.md)
detaille le curseur, les filtres et le remplissage apres exclusions. Les lectures
de candidats sont bornees par lots de 100 ; une page precedee de nombreux
coffrets non vendables peut necessiter plusieurs lots. Aucun resultat n'est
tronque a un nombre arbitraire de candidats.

Les listes historiques restent completes pour compatibilite. Les selecteurs
de toutes les communes gardent leur liste complete ; les suggestions avec
prefixe sont limitees par defaut a 20, avec `limit`/`offset` explicites.

Le cache des indicateurs Animation conserve sa duree de 60 secondes et inclut
le perimetre communal ; l'autorisation est relue meme lors d'un acces au cache.
Aucun cache global de publication, de BUM ou de disponibilite Stripe n'est ajoute.


## Verification finale et livraison

- Suite cumulative backend : 180 tests reussis sur 30 fichiers, comprenant les
  schemas PostgreSQL isoles et la lecture seule du catalogue local existant.
- Dashboard : 47 tests reussis (7 nouveaux tests de parite/volume et 40 tests
  d'exploitation existants).
- Benchmark HTTP : 9 tests reussis.
- Interfaces Support et OnBoard : 4 tests DOM Node reussis.
- Marketplace : les 49 tests du repertoire security passent et le build Vite
  de production passe. Les changements de presentation presents avant ce
  travail restent hors des commits de performance.
- Index et requetes de catalogue : 25 tests cibles passent apres les derniers
  ajustements ; migration exacte executee deux fois dans un schema isole et
  resultats des requetes compares avant/apres.

Le [rapport de volumes et HTTP](validation-volume-recherches-2026-09-12.md)
contient les commandes reproductibles, les volumes et les limites des mesures.
L'audit de plans a ete mene sans installer d'index sur la base distante.
La [qualification des index](qualification-index-catalogues-2026-09-12.md)
documente les trois index retenus et les candidats rejetes. La migration
`sql/v231_index_catalogues_pagines.sql` est livree pour le mecanisme habituel
de migration ; elle n'a pas ete appliquee a l'environnement partage.

Livrer le backend avant le frontend Marketplace : le client utilise les
nouveaux endpoints de pagination. Les anciennes routes sont conservees pour
permettre cette livraison progressive. Ce travail cree les commits locaux ;
aucun deploiement n'a ete effectue. Les mesures HTTP de la version deployee
ne sont donc pas une validation des nouveaux commits.
