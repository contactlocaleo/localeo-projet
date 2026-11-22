# Backlog préliminaire — dix corrections candidates

Propositions après finalisation des six analyses ; contre-expertise et mesures à venir. Deux P1 conditionnels (R01/R10), huit P2, aucun P0. Les priorités reposent sur preuve source et scénario explicite, pas sur incident observé. Aucune implémentation ni décision utilisateur.

## R01 — Déporter les unités synchrones des handlers async concernés

A conditionnelle / P1 / effort S / RC-01. Source : `app/api/juste_prix_api.py:123–133, illustrer_produit ; app/application/animation_locale/services/juste_prix.py:57–91 ; app/infrastructure/admin/admin.py:12523–12600, quatre handlers ERP`.

SQL/UoW/fournisseur synchrones appelés directement sur le thread de boucle après une lecture async. Une attente de verrou ou fournisseur peut immobiliser les autres requêtes du même event loop. Un dépôt image attend une coordination ou un pool occupé ; ou un batch ERP non vide attend son fournisseur pendant une lecture/scan sur le même processus. Pas besoin de supposer une saturation globale.

Minimum : Réutiliser run_in_threadpool autour de l'unité synchrone entière après capture d'identité/contexte ; ouvrir/fermer les sessions dans ce thread. Ne pas transporter de session active.

Mesure : M01 prévu : mécanisme ERP extrait avec attente injectée ; handler image non mesuré. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R02 — Réutiliser le compteur exact des inscrits dans l'inscription

B / P2 / effort M / RC-02. Source : `app/application/animation_locale/services/participants_animation.py:70/104/127, inscrire ; app/infrastructure/persistence/repositories/animation_locale_repositories.py:1331 ; sql/v283_e73_compteurs_lectures.sql:11–47`.

Comptage exhaustif des inscrits, éventuellement deux fois, pendant la coordination exclusive qui protège identité/capacité. Le verrou est nécessaire ; le recomptage peut être remplacé par un fait exact déjà projeté. Arrivées simultanées dans une animation déjà fréquentée ; coût à qualifier N/10N, sans débit plafond annoncé.

Minimum : Lire le compteur transactionnel exact existant avant insertion et réutiliser ce nombre pour capacité et premier inscrit, après preuve d'équivalence et présence de v283 ; garder la coordination.

Mesure : NON MESURÉ : SQL, contention, gain et taux d'inscription. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R03 — Borner les deux lectures auxiliaires QR/PIN

A conditionnelle / P2 / effort S / RC-04 + RC-05. Source : `app/application/animation_locale/services/validations_animation.py:133–141 ; app/infrastructure/persistence/repositories/animation_locale_repositories.py:1510–1518 ; app/domaine/animation_locale/entities/validation_animation.py:29–31`.

Toutes les preuves de la minute sont hydratées pour len, alors que le domaine décide à 60 ; toutes les annulations du participant sont chargées pour une seule antériorité. Nouvelles preuves distinctes d'un commerce en pointe ou historique de corrections croissant ; pas les simples rejeux d'une preuve effective.

Minimum : Port de nombre récent plafonné à 60 sans hydratation/tri ; requête séparée pour l'antériorité participant+commerce+étape annulée, même clé max(coalesce(annulee_at,validated_at),id), LIMIT 1. Deux remèdes explicitement requis.

Mesure : FORTEMENT ÉTAYÉ PAR LE CODE ; durée SQL et CPU NON MESURÉES. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R04 — Cibler et paginer les producteurs de notifications

B / P2 / effort M / RC-07. Source : `app/application/animation_locale/services/notifications_localeo_live.py:43–83/86–109/160–194 ; publication_animation.py:345/372 ; tirages_animation.py:280`.

Installations globales actives puis filtre commune en Python ; résultats chargés puis regroupés par installation et existence vérifiée par destinataire. Croissance des installations étrangères avec commune cible fixe ; plusieurs participations d'une installation pour un tirage.

Minimum : Ciblage SQL et pages stables d'installations distinctes ; insertion groupée idempotente, agrégation gagnant par installation. Préserver le commit métier et source_key.

Mesure : FORTEMENT ÉTAYÉ PAR LE CODE ; charge SQL/mémoire intégrée NON MESURÉE. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R05 — Retirer la copie liste inutile du tirage Coffrets

A conditionnelle / P2 / effort S / RC-06. Source : `app/domaine/animation_locale/entities/tirage_animation.py:74–110, PopulationEligibleAnimation.selectionner ; app/application/animation_locale/services/tirages_animation.py:232–286 ; animation_locale_repositories.py:1717–1723`.

UUID tous chargés, tuple puis set d'unicité puis list pour sample. Réduction locale possible d'une copie ; O(N) et transaction exclusive demeurent. Grande population gelée et peu de gagnants/suppléants ; le lancement déjà réalisé suit un chemin différent.

Minimum : Passer le tuple immuable directement à la source sample, après vérification de son contrat et des doubles. Garder le contrôle de doublons du domaine.

Mesure : M-LIVE-01 prévu : allocations transitoires du domaine avec population déjà construite ; aucun SQL/verrou mesuré. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R06 — Aligner le budget média avec les opérations du stockage

B / P2 / effort M / RC-10. Source : `app/application/animation_locale/services/contenu_generation.py:368–395 ; app/infrastructure/storage/document_storage.py:83–109 ; jeu_animation.py:459–463`.

Budget monotone testé autour de get/read synchrones sans transmission de budget restant. SDK possède ses propres défauts, pas une absence totale de timeout. Stockage S3 lent/trickle/retries ; client Live expire à 15 s pendant que le backend peut encore travailler. Stockage réel déployé inconnu.

Minimum : Politique connect/read/retries explicite adaptée au budget restant, fermeture Body et lecture bornée aux octets autorisés. Préserver SHA, provenance et erreurs maîtrisées.

Mesure : FORTEMENT ÉTAYÉ PAR LE CODE ; p95 stockage/HTTP et gain NON MESURÉS. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R07 — Grouper les résumés commerces du passeport

A conditionnelle / P2 / effort S / RC-12. Source : `app/application/animation_locale/services/jeu_animation.py:403–408 ; app/infrastructure/persistence/repositories/repositories_sqlalchemy.py:143–170/184`.

session.get par merchantId pour nom/adresse ; lectures SQL distinctes si identity map froide. Le nombre réel n'est pas compté ici. Passeport avec nombreux commerces et actualisations de progression ; dépend de la latence DB et identity map.

Minimum : Projection groupée des seules colonnes utiles pour les IDs autorisés, indexer par ID puis reconstruire exactement l'ordre DSL et l'erreur de commerce absent.

Mesure : FORTEMENT ÉTAYÉ PAR LE CODE ; N+1 potentiel source, nombre SELECT effectif NON MESURÉ. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R08 — Rendre l'onglet gains Coffrets par pages et agrégats

B / P2 / effort M / RC-13. Source : `localeo-animation/src/app/App.tsx:2939–2959 ; src/app/api.ts:838–856/1264–1280 ; backend app/api/animation_locale_api.py:2747–2753/2798–2810`.

collectPages collecte toutes les pages avant résolution et le composant attend gains+consommations ; route gains renvoie liste complète. Pagination serveur seule ne borne pas l'ouverture d'écran. Dotation de plus d'une page ; erreurs tardives ou actualisation complète.

Minimum : État page/cursor dans l'onglet, lecture locale conservant filtres/navigation/focus ; route gains paginée additive et agrégats serveur exacts séparés. Conserver les anciens consommateurs.

Mesure : FORTEMENT ÉTAYÉ PAR LE CODE ; premier rendu et requêtes HTTP réelles NON MESURÉS. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R09 — Calculer les statistiques Animation depuis des projections ciblées

B / P2 / effort M / RC-17. Source : `app/application/animation_locale/services/pilotage_animation.py:65–80/101–126 ; app/api/animation_locale_api.py ; localeo-animation/src/app/App.tsx:1792/1987 et api.ts:1234`.

participants/validations complets pour compter, notifications tenant avant filtre animation ; dashboard historique charge encore plus large. Dashboard courant borne demandé à App.tsx:1210, donc non accusé globalement. Animation fréquentée ouverte dans workflow/Live ; statistiques complètes répétées ; volume réel et fréquence inconnus.

Minimum : COUNT/GROUP BY/projections transactionnelles avec filtres tenant/animation avant lecture, alertes ciblées ; préserver calculs et toutes variantes de réponse.

Mesure : FORTEMENT ÉTAYÉ PAR LE CODE, ajout orchestrateur vérifié ; SQL/allocations intégrées NON MESURÉS. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.

## R10 — Lier les cycles email/SMS à leur budget et au bail

B / P1 / effort M / RC-14. Source : `app/application/exploitation/services/batchs.py:608–700 ; app/application/exploitation/use_cases/emails_batch.py:25–92 ; sms_batch.py:17–67 ; scheduler/http_client.py:51–63`.

Bail timeout+60 expirant sans deadline du handler ; timeout du client ne l'arrête pas. Une nouvelle invocation peut être admise après expiration pendant l'ancien travail. 100 remises séquentielles à environ 4 s chacune dépasseraient le bail de 360 s, puis déclenchement suivant ; scénario crédible explicite, aucune fréquence ni double envoi observé.

Minimum : Budget monotone de cycle, réservations progressives et marge pour fournisseur ; pas de nouvelle unité après perte de propriété. Renouvellement propriétaire borné uniquement si nécessaire.

Mesure : M02 prévu : SQLite/horloge logique, pas concurrence PostgreSQL ni latence 361 s. Confiance élevée sur le mécanisme, impact/fréquence réels à qualifier. Alternative et compatibilité à contredire avant finalisation.
