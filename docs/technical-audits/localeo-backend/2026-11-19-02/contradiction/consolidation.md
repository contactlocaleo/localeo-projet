# Consolidation par cause et flux

Six premières analyses finalisées avant consolidation : 17 constats majeurs (2 CPU, 4 mémoire, 2 concurrence, 3 persistance, 3 API, 3 SRE). Un agent persistance interrompu est exclu ; sa relève a analysé indépendamment avec contexte neuf. Les deux ajouts orchestrateur ERP/pilotage sont explicitement distingués, pas attribués aux spécialistes.

Après rapprochement et scission des mécanismes, 17 causes candidates distinctes : au stade préliminaire, 11 causes alimentent 10 corrections (R03 couvre deux projections distinctes), 6 causes sont annexées. Ces nombres ne sont pas des incidents. Preuves : code relu et six rapports, pas votes ni fréquence supposée.

| Cause | Origines sémantiques | Mécanisme | Orientation |
| --- | --- | --- | --- |
| RC-01 | CONC-01 + ajout orchestrateur ERP | Frontière async/sync manquante | R01 |
| RC-02 | PSQL-01 | Recomptages des inscrits sous coordination exclusive | R02 |
| RC-03 | CONC-02 / partie PSQL-01 | Rendu QR/template dans la section exclusive | Secondaire ; remède distinct de R02 |
| RC-04 | CPU-01 / PSQL-02 cadence | Hydratation de la minute pour une décision à seuil | R03 |
| RC-05 | PSQL-02 antériorité | Historique annulé complet pour une seule référence | R03, deuxième projection distincte |
| RC-06 | CPU-02 / MEM-03 / PSQL-03 | Population Coffrets et copies intégrales | R05 |
| RC-07 | MEM-01 | Producteur publication/résultat non borné | R04 |
| RC-08 | MEM-02 | Diffusion actualités globale et reprise non paginée | Secondaire C |
| RC-09 | MEM-04 | Faits complets au retrait classique pour lire les IDs | Secondaire |
| RC-10 | API-01 budget | Budget autour de l'I/O sans échéance transmise | R06 |
| RC-11 | API-01 revalidation | Relecture/décodage média répétée sans cache | Secondaire, ne pas fusionner avec deadline |
| RC-12 | API-02 | Lecture commerce par ID dans la projection passeport | R07 |
| RC-13 | API-03 | Collecte de toutes les pages avant rendu gains | R08 |
| RC-14 | SRE-01 / S-CONC-02 | Bail non lié au travail serveur | R10 |
| RC-15 | SRE-02 | Remise fournisseur sous transaction d'autorisation | Secondaire C, pas corrigé par R10 |
| RC-16 | SRE-03 | Executor scheduler commun | Hypothèse secondaire |
| RC-17 | Ajout orchestrateur vérifié directement | Statistiques depuis populations complètes | R09 |

Les causes CPU/mémoire/SQL d'une même population Coffrets sont regroupées. Le rendu inscription et le comptage sont séparés, de même que cache média et délai fournisseur. Le budget de cycle ne retire pas le verrou d'autorisation pendant la remise : RC-15 reste distinct.

## Correspondance historique

Ancienne OPT-01 → R01, périmètre élargi à un handler Juste Prix prouvé ; OPT-02 → R10 ; OPT-04 → R09 ; OPT-07 → R06. Anciennes OPT-03/05 (expiration Coffrets), OPT-06 (CSV) et OPT-08 (Stripe) restent secondaires persistantes, non réputées résolues. Les autres R sont nouvellement priorisées/documentées à source backend inchangée depuis la référence. Le tirage était déjà une réserve secondaire, désormais mesurable en composant ; aucun nouveau commit causal déduit.

Les anciens sujets OPT hors focus n'ont pas été relancés en SQL ; le CSV reste seulement un témoin de reproductibilité. L'absence d'un mécanisme dans le rapport antérieur ne prouve aucune régression.

## État final après contradiction et mesures

R05, copie seule, est P3 différable en annexe ; RC-06 population complète reste à qualifier. Dix causes alimentent désormais neuf corrections principales et sept causes sont secondaires. Les dix candidats du tableau restent la trace préliminaire, pas dix correctifs finalement retenus. Aucun P0 ; deux P1 conditionnels et sept P2. La contre-expertise indépendante et les réserves sont intégrées aux fiches finales.
