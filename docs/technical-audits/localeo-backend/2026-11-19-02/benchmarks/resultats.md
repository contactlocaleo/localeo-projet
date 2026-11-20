# Résultats des composants isolés

Trois commandes achevées : 1 test réussi chacune, respectivement 9,72 s /7,30 s /2,54 s pytest. Durées internes 7,559 /5,447 /1,044 s. Aucun arrêt ni échec de cette campagne ; aucun seuil relevé. Les échecs 01/02 et arrêt 03 antérieurs restent ceux de la référence, pas des tentatives de cette relance. [Protocole](protocole.md), [limites](limites.md).

## M01 — CONFIRMÉ PAR MESURE LOCALE DU MÉCANISME

240 tours avec corps ERP extraits et doubles. Attente injectée 10 ms, pas une observation fournisseur.

| Handler | Coroutines | Contrôle p50 ms | Témoin p50 ms | p95 ms | p99 ms |
| --- | --- | --- | --- | --- | --- |
| admin_lancer_batch_envoi_emails | 1 | 0.037 | 10.657 | 10.962 | 11.070 |
| admin_lancer_batch_envoi_emails | 5 | 0.141 | 53.184 | 53.712 | 53.917 |
| admin_lancer_batch_envoi_emails | 10 | 0.278 | 106.051 | 107.274 | 108.492 |
| admin_synchroniser_statuts_emails | 1 | 0.065 | 10.506 | 11.060 | 11.105 |
| admin_lancer_batch_envoi_sms | 1 | 0.048 | 10.680 | 10.842 | 10.868 |
| admin_synchroniser_statuts_sms | 1 | 0.162 | 10.605 | 11.091 | 12.154 |

Zéro erreur des doubles vérifiée. p99=max sur 20 essais, pas percentile HTTP. Le mécanisme des quatre corps est confirmé ; le handler image Juste Prix reste fortement étayé par code, non mesuré. Pas de worker/pool saturé ni gain après déport établi.

## M02 — simulation fonctionnelle, pas mesure de concurrence SQL

Bail 360 s : second lancement refusé à +359 s, admis à +361 s alors que le premier callback est encore dans la pile. Deux handlers imbriqués, deux journaux SUCCES, aucun verrou restant ; temps réel 38,991 ms. Horloge UTC simulée ; aucune durée réelle 361 s, aucun double envoi ni conflit de workers PostgreSQL démontré. FORTEMENT ÉTAYÉ PAR LE CODE, reproduit en simulation.

## M06 — CONFIRMÉ PAR MESURE LOCALE DES ALLOCATIONS

Sept exports par volume, entrée génératrice, timings séparés de trois tracemalloc et cProfile.

| Lignes | Sortie UTF-8 octets | p50 ms | p95/p99 ms | Pic Python octets (3 essais) |
| --- | --- | --- | --- | --- |
| 1000 | 119189 | 17.168 | 20.221 | 674904 |
| 5000 | 595189 | 67.764 | 92.597 | 2816904 |
| 10000 | 1190189 | 105.507 | 149.274 | 5494404 |

BOM, nombre de lignes et SHA identiques entre répétitions ; les trois empreintes CSV concordent aussi avec les bruts précédents. Pic croissant avec sortie ; aucune fuite/OOM. SQL/projection/HTTP/encodage client non exercés. CSV secondaire dans cet audit orienté Live.

## M-LIVE-01 — allocations transitoires du domaine tirage Coffrets

Nouvelle méthode, sans baseline historique. Source réelle construction PopulationEligibleAnimation puis selectionner, 1 gagnant+5 suppléants ; tuple et UUID déjà alloués hors fenêtre.

| Population | p50 ms (harness compris) | p95/p99 ms | Pic Python min–max octets |
| --- | --- | --- | --- |
| 1000 | 1.526 | 2.867 | 41792–41808 |
| 5000 | 7.983 | 11.772 | 656096–656112 |
| 10000 | 8.650 | 11.622 | 656064–656064 |

Les transitoires (notamment set) sont observés ; plateau 5 000→10 000 compatible avec capacité interne des collections. Ne pas prétendre à une pente mémoire mesurée constante ni à une saturation. Les assertions d’appartenance de six UUID parcourent le tuple et font partie du temps : ce n’est pas le CPU pur du domaine. Random déterministe est un double, pas la source sûre de production. Ni repository, UUID SQL, verrou, gains/notifications ou HTTP mesurés. R05 réduit une copie seulement ; aucun gain après correction démontré.

## Ressources et retour après campagne

| Campagne | Working set initial/final octets | Maximum historique processus octets | Disponible physique final octets |
| --- | --- | --- | --- |
| M01/M02 | 78127104 / 91308032 | 139833344 | 2597109760 |
| M06 | 78880768 / 79585280 | 84377600 | 2452676608 |
| M-LIVE-01 | 78643200 / 80711680 | 80986112 | 2264784896 |

Instantanés sous 512 Mio et au-dessus de 1 Gio disponible. Maximum historique du processus ≠ pic par cas ; RSS final différent de l’initial ne prouve pas une fuite. Tous les processus terminés, aucun serveur/port/base laissé actif. Bruts et scripts dans backend/tmp/performance-audit-2026-11-19-02, ignorés Git. [Manifeste](../validation/mesures-manifeste.json). Gains après correction et capacité API NON MESURÉS.
