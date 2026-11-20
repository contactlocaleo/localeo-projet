# Rapport exécutif — relance indépendante du 19 novembre 2026

Neuf corrections proposées : **0 P0, 2 P1 conditionnels, 7 P2**. Trois A conditionnelles et six B. Aucun code applicatif corrigé, aucune migration/donnée réelle/installation/commit/push/déploiement. Champs de [décision](../validation/decisions.md) vides.

## Cinq constats majeurs consolidés

| Constat | Flux et mécanisme | Preuve et orientation |
| --- | --- | --- |
| 1. Certaines actions bloquent la boucle du processus | Image Juste Prix async avec SQL direct ; quatre batchs ERP async avec travail synchrone | R01 P1 conditionnel. Code et M01 ERP : dix coroutines avec 10 ms injectées reportent le témoin p50 à106,051 ms contre0,278 ms sans attente. Pas de percentile HTTP, image non mesurée |
| 2. Durée du cycle non liée au bail | Remises email/SMS partagées avec accès et résultats Live | R10 P1 conditionnel. Bail 360 s ; simulation admet le second callback à+361 s pendant le premier, refuse à+359. Aucun double envoi ou conflit PostgreSQL prouvé |
| 3. Lectures auxiliaires coûtant davantage que le fait nécessaire | Inscription : COUNT sous verrou ; QR/PIN : minute et historique annulé hydratés ; passeport : commerces par ID | R02/R03/R07 P2. Code fortement étayé ; compteur exact existant sous préconditions, deux projections QR/PIN et chargement groupé proposés. SQL/CPU intégré non mesuré |
| 4. Certaines projections de gestion et producteurs Live chargent leur population | Publication/résultat notifications et statistiques /live | R04/R09 P2. Ciblage/agrégats compatibles proposés. Dashboard actuel borné et carnet personnel préchargé distincts ; aucune accusation globale |
| 5. Latence dépendante de lectures ou pages séquentielles | Média sélectionné : I/O synchrone sans budget transmis ; onglet gains : toutes pages avant rendu | R06/R08 P2. Politique I/O explicite sans deadline dure, page gains enrichie/agrégats additifs. Stockage effectif, SQL et premier rendu non mesurés |

Sources/fonctions/lignes, risques, compatibilité, tests et rollback : [neuf fiches](../recommandations/backlog-final.md). Le [contradicteur réel](../contradiction/contre-expertise.md) confirme les mécanismes avec ajustements, pas une capacité ou autorisation.

Six rapports indépendants donnent17 constats d'origine, rapprochés en17 causes candidates après regroupements/scissions et deux apports source explicites de l'orchestrateur. Dix causes alimentent neuf corrections ; sept causes restent secondaires, dont la population complète du tirage. Les symptômes CPU/mémoire/SQL du même chargement ne multiplient pas les corrections.

M-LIVE-01 observe les allocations transitoires de construction/sélection du tirage avec UUID/tuple préexistants. La suppression de copie R05 seule est P3 différable ; le chargement intégral sous coordination reste à mesurer, sans conclusion d'innocuité. M06 CSV reproduit le pic Python 5 494 404 octets à10k, hors SQL/HTTP, aucune fuite/OOM. Trois commandes de composants réussies ; aucun arrêt de cette relance.

**Gains après correction et capacité API NON MESURÉS.** Pas de saturation CPU/RAM/pool/scheduler ou incident de production établi. Timings antérieurs non comparables pour attribuer une tendance à source inchangée ; les allocations CSV de même jeu sont identiques descriptivement. Une simulation ne remplace pas deux workers PostgreSQL.

[Protocole](../benchmarks/protocole.md), [résultats](../benchmarks/resultats.md), [limites](../benchmarks/limites.md), [comparaison](comparaison-precedent.md). Bruts et scripts ignorés dans le backend, empreintés mais non garantis par Git documentaire. Anciennes archives conservées, intégrité vérifiée en fin de campagne.
