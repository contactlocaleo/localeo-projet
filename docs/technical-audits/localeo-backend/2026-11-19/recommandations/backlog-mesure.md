# Backlog révisé après mesures locales

**Huit orientations : deux P1 et six P2, aucun P0.** Aucune nouvelle cause ni ticket doublon. Les rangs restent conditionnels à l’exposition ; aucune mesure de déploiement acquise. Le [backlog préliminaire](backlog-preliminaire.md) et les rapports d’étape 3 restent historiques. [Résultats](../benchmarks/resultats.md), [limites](../benchmarks/limites.md), [protocole](../benchmarks/protocole.md).

OPT-01 est renforcé par une mesure de scheduling du corps source ; OPT-02 par une simulation, distincte d’une mesure de charge ; OPT-06 par des allocations locales. Les cinq autres orientations sont regroupées dans une catégorie **non mesurée en environnement représentatif**. Aucun défaut principal infirmé, donc aucun retrait artificiel. Aucune urgence nouvelle pour le CSV à 10 000 lignes ; P2 reste différable, grands volumes/concurrence/budget réels inconnus. La contre-relecture indépendante refuse de transformer ce petit jeu en preuve d’impact faible à toute échelle. Pas de déclassement généralisé ni hausse de priorité sans preuve.

**Gain démontré après correction : aucun, pour les huit orientations.** Chaque bénéfice plausible ci-dessous est qualitatif ; gain chiffré **NON MESURÉ**. Pas de benchmark de code optimisé, aucun patch applicatif. Les votes indiqués sont ceux simulés à l’étape 3, jamais des mesures et aucun nouveau scrutin à l’étape 4.

| Orientation | Priorité | État de validation | Décision |
| --- | --- | --- | --- |
| OPT-01 / RC-06 | P1 | Scheduling local mesuré | Première correction ciblée à préparer après autorisation |
| OPT-02 / RC-08 | P1 | Logique de bail simulée, charge non mesurée | Préserver claims et effets incertains ; valider ensuite sur PostgreSQL jetable |
| OPT-06 / RC-05 | P2 différable | Allocations CSV mesurées, capacité non mesurée | Pas d’OOM dans l’enveloppe ; gros volumes à quantifier |
| OPT-03 / RC-10 | P2 | Non mesuré | Vérifier progression cohorte avant correction |
| OPT-04 / RC-01 | P2 | Non mesuré | Priorité de sous-flux selon trafic Live/détail/historique |
| OPT-05 / RC-09 | P2 | Non mesuré | SQL et contention à quantifier |
| OPT-07 / RC-11 | P2 | Non mesuré | Délais réseau avant cache |
| OPT-08 / RC-12 | P2 | Non mesuré | Mesurer Stripe et occupation SQL |

## Mécanismes exercés localement

### OPT-01 — Déporter les quatre batchs ERP hors de la boucle

- **Cause racine :** RC-06 — Les handlers async appellent BatchRunner.execute puis requests dans leur thread, sans déport de l’unité synchrone.
- **Flux / API :** F12 batch ERP ; F01/F03 effets indirects. `POST /internal/emails/batch/envoyer ; /internal/emails/batch/synchroniser-statuts ; /internal/sms/batch/envoyer ; /internal/sms/batch/synchroniser-statuts`. Domaines : Concurrence, API, SRE.
- **Références :** [app/infrastructure/admin/admin.py:12523](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523), [app/infrastructure/admin/admin.py:12543](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12543), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642). Sources initiales : ASY-01.
- **Preuve actualisée : CONFIRMÉ PAR MESURE LOCALE DU MÉCANISME.** M01 : témoin médian 10,574 / 52,352 / 104,527 ms pour 1/5/10 batchs avec 10 ms injectées chacun ; contrôles 0,051 / 0,087 / 0,351 ms. Aucun percentile HTTP.
- **Confiance :** Élevée pour le corps des quatre handlers ; exposition et capacité réelles inconnues.
- **Correction minimale :** Déporter l’unité synchrone complète (résolution opérateur, UoW, BatchRunner et fournisseur) vers le mécanisme de threadpool existant. Conserver corrélation, erreurs et redirections ; pas de partage d’une session entre threads.
- **Effort / risque :** S / Faible à moyen. **Compatibilité :** Préserve la réponse ; ne crée aucune capacité SQL supplémentaire garantie. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P1 ; 6/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Disponibilité de la boucle pendant l’attente après déport ; charge threadpool/SQL à vérifier. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M01 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

### OPT-02 — Lier travail serveur, réservations et durée de bail

- **Cause racine :** RC-08 — Le timeout catalogue alimente le client et le bail timeout+60 ; handler() n’a ni budget de cycle imposé ni renouvellement du bail.
- **Flux / API :** F12 batchs ; F03 livraison et F01 capacité indirecte. `POST /protected/exploitation/emails/batch/envoyer ; variantes SMS et ERP ; autres BatchRunner à vérifier individuellement`. Domaines : Concurrence, persistance, API, SRE.
- **Références :** [app/application/exploitation/services/batchs.py:608](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642), [app/infrastructure/scheduler/http_client.py:34](../../../../../../localeo-backend/app/infrastructure/scheduler/http_client.py#L34), [app/application/exploitation/use_cases/emails_batch.py:25](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L25). Sources initiales : ASY-03, SRE-01.
- **Preuve actualisée : FORTEMENT ÉTAYÉ PAR LE CODE + SIMULATION LOCALE.** M02 : second lancement refusé à +359 s, admis à +361 s, premier handler encore actif ; horloge logique et SQLite, aucun traitement réel de 361 s.
- **Confiance :** Élevée pour la logique de bail ; fréquence/effets opérationnels non mesurés.
- **Correction minimale :** Budget monotone de cycle, réservation progressive ou restitution prouvée des éléments non commencés, délais fournisseur connect/read/retry explicites. Arrêter de prendre du travail si bail perdu ; renouvellement propriétaire pour les handlers pouvant légitimement durer. Aucun arrêt forcé d’un effet fournisseur incertain.
- **Effort / risque :** M / Moyen. **Compatibilité :** Le budget ne coupe pas automatiquement un appel en vol ; préserver révocation, idempotence et rapprochement incertain. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P1 ; 6/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Moins de cycles non bornés et de réservations commencées sans budget ; aucun double envoi démontré. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M02 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

### OPT-06 — Préparer les CSV paiements dans un spool

- **Cause racine :** RC-05 — Le générateur est consommé dans produire_csv puis retourné sous forme d’une chaîne complète avec BOM.
- **Flux / API :** F10 finance ERP. `GET /internal/gestion-achats/paiements/export-metier.csv ; GET /internal/gestion-achats/paiements/export-finance.csv`. Domaines : Mémoire, API, persistance.
- **Références :** [app/application/gestion_achats/services/consultation_paiements.py:150](../../../../../../localeo-backend/app/application/gestion_achats/services/consultation_paiements.py#L150), [app/application/gestion_achats/services/export_financier.py:13](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13). Sources initiales : MEM-04.
- **Preuve actualisée : CONFIRMÉ PAR MESURE LOCALE DES ALLOCATIONS.** M06 : à 10 000 lignes, sortie 1 190 189 octets, pic Python 5 494 404 octets ; pas d’épuisement observé, concurrence 1. CSV SQL/HTTP intégré non exercé.
- **Confiance :** Élevée pour la sortie en RAM ; impact des gros exports et budget RAM réels inconnus.
- **Correction minimale :** Écrire progressivement dans un fichier temporaire à seuil mémoire, terminer génération/audit puis fermer la projection SQL avant réponse par blocs. Fermer/supprimer le temporaire en succès, erreur ou abandon.
- **Effort / risque :** M / Faible à moyen. **Compatibilité :** Mêmes colonnes, BOM, format, filtres et erreurs avant envoi ; ne pas supprimer une cohérence d’instantané si le contrat l’exige. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P2 ; 4/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Spool limitant la sortie en RAM ; coût disque/encodage et pic final encore à mesurer. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M06 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

## Catégorie distincte — environnement de mesure manquant

Ces cinq orientations restent dans le programme principal conditionnel. Leur coût n’est ni confirmé ni infirmé par M01/M02/M06. Exécuter leurs protocoles sur cible isolée explicitement désignée avant de prétendre un gain ou d’accepter une capacité.

### OPT-03 — Sélectionner les relances restantes avant LIMIT

- **Cause racine :** RC-10 — LIMIT est appliqué aux instances actives avant _existing_relance ; ni exclusion SQL ni curseur de travail restant.
- **Flux / API :** F12 rappels avant expiration. `POST /protected/gestion-achats/coffrets-instances/expiration/reminders/batch`. Domaines : Persistance, progression, latence métier.
- **Références :** [app/application/gestion_achats/use_cases/expiration_coffrets.py:239](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L239), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [sql/v141_relances_expiration_coffrets.sql:35](../../../../../../localeo-backend/sql/v141_relances_expiration_coffrets.sql#L35). Sources initiales : DB-03.
- **Preuve actualisée : FORTEMENT ÉTAYÉ PAR LE CODE — NON MESURÉ.** M03 NON EXÉCUTÉ : cohorte réelle, progression répétée et concurrence PostgreSQL non mesurées.
- **Confiance :** Élevée pour LIMIT avant exclusion ; exposition de cohortes >limite inconnue.
- **Correction minimale :** NOT EXISTS avant LIMIT sur instance/date_expiration/type/reminder_days, ordre total date+ID ; conserver l’unicité et le contrôle de concurrence. Pas de migration d’index par défaut.
- **Effort / risque :** S / Faible à moyen. **Compatibilité :** Même fenêtre et même contenu ; aucune garantie de deux lanceurs sans test de concurrence. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P2 ; 5/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Progression des rappels restant éligibles ; délai réellement évité inconnu. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M03 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

### OPT-04 — Remplacer les lectures de faits par des projections agrégées

- **Cause racine :** RC-01 — Le service de dashboard charge tous les participants et filtre ensuite ; live et détails chargent les entités d’une animation pour des compteurs. Le lecteur ne porte pas la projection agrégée demandée.
- **Flux / API :** F05 pilotage ; F09 suivi organisateur. `GET /protected/animation-locale/dashboard-performance (sans mode_lecture=borne) ; GET /protected/animation-locale/animations/{id}/live ; détails appelant _animation_detail`. Domaines : CPU, mémoire, persistance, API.
- **Références :** [app/application/animation_locale/services/pilotage_animation.py:101](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L101), [app/application/animation_locale/services/pilotage_animation.py:65](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L65), [app/api/animation_locale_api.py:1331](../../../../../../localeo-backend/app/api/animation_locale_api.py#L1331), [app/infrastructure/persistence/repositories/animation_locale_repositories.py:1343](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L1343). Sources initiales : CPU-01, MEM-01, DB-01, API-01.
- **Preuve actualisée : FORTEMENT ÉTAYÉ PAR LE CODE — NON MESURÉ.** M04 NON EXÉCUTÉ. Le frontend courant utilise borne ; Live reste consommé. Pas de gain agrégats ni volume intertenant mesuré.
- **Confiance :** Élevée pour les chargements ; trafic et goulot dominant inconnus.
- **Correction minimale :** Pousser périmètre et période dans SQL, calculer les compteurs/séries/top et fournir des résumés groupés aux détails. Appliquer le même lecteur de compteurs aux vues live. Garder la forme historique ; ne pas substituer le mode borne.
- **Effort / risque :** M / Moyen. **Compatibilité :** Dates Paris, statuts, archives et mode de réponse identiques. Coût des résultats autorisés encore proportionnel aux animations réellement rendues. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P2 ; 5/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Moins de faits transférés/mappés pour des compteurs ; Live/détails puis historique selon trafic. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M04 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

### OPT-05 — Grouper les faits du lot d’expiration

- **Cause racine :** RC-09 — La sélection verrouille jusqu’à la limite, puis la boucle charge faits et relances unitairement avant un commit final.
- **Flux / API :** F12 expiration Coffrets ; F01 ressources et verrous partagés. `POST /protected/gestion-achats/coffrets-instances/expiration/batch`. Domaines : Persistance, concurrence, mémoire.
- **Références :** [app/application/gestion_achats/use_cases/expiration_coffrets.py:118](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L118), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [app/infrastructure/persistence/models.py:509](../../../../../../localeo-backend/app/infrastructure/persistence/models.py#L509). Sources initiales : DB-02.
- **Preuve actualisée : FORTEMENT ÉTAYÉ PAR LE CODE — NON MESURÉ.** M05 NON EXÉCUTÉ : nombre SQL effectif, plans, temps sous verrou et impact du préchargement inconnus.
- **Confiance :** Élevée pour les lectures répétées ; ampleur opérationnelle inconnue.
- **Correction minimale :** Charger les relances en un ensemble borné et les relations nécessaires en requêtes groupées pour les IDs verrouillés ; conserver la sélection de racines, l’ordre de verrous et le commit actuel. Ne pas joindre une collection avant LIMIT/FOR UPDATE.
- **Effort / risque :** M / Moyen. **Compatibilité :** Préserve atomisme, garde remboursement et crédit B2B ; mesurer aussi les octets et pas seulement le nombre SQL. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P2 ; 5/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Réduire aller-retours des faits du lot sans modifier sélection verrouillée ni commit. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M05 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

### OPT-07 — Transmettre les budgets aux lectures de médias distants

- **Cause racine :** RC-11 — Le budget monotone entoure get S3/Body.read sans lui transmettre une échéance ; cela ne garantit pas l’interruption au budget.
- **Flux / API :** F02/F09 lecture personnelle Live. `GET /public/localeo-live/participations/{id}`. Domaines : API, concurrence, stockage.
- **Références :** [app/application/animation_locale/services/contenu_generation.py:368](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L368), [app/infrastructure/storage/document_storage.py:83](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L83), [app/infrastructure/storage/document_storage.py:104](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L104), [app/application/animation_locale/services/jeu_animation.py:459](../../../../../../localeo-backend/app/application/animation_locale/services/jeu_animation.py#L459). Sources initiales : API-02.
- **Preuve actualisée : FORTEMENT ÉTAYÉ PAR LE CODE — NON MESURÉ.** M07 NON EXÉCUTÉ : durées S3/read/retries inconnues, pas de cache adopté. Taille média contrôlée dans le code.
- **Confiance :** Élevée pour absence de budget transmis ; exposition aux attentes longues inconnue.
- **Correction minimale :** Budget restant et politique explicite connect/read/retries dans l’adaptateur documentaire, fermeture du Body et lecture bornée aux octets attendus. Préserver SHA, provenance et autorisation ; ne pas annoncer une échéance dure sans moyen d’interruption effectif.
- **Effort / risque :** M / Moyen. **Compatibilité :** JSON et contrôle d’intégrité inchangés ; effets sur les autres consommateurs du stockage à tester. Cache : orientation séparée différée. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P2 ; 4/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Mieux borner l’attente et les octets ; un timeout lecture seul ne garantit pas une deadline absolue. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M07 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

### OPT-08 — Alléger la vérification Stripe du retour de paiement

- **Cause racine :** RC-12 — L’achat/token est lu avant retrieve enrichi ; seule metadata.achat_id sert à cette vérification, état financier toujours local.
- **Flux / API :** F10 retour paiement. `GET /public/gestion-achats/paiements/retour/{achat_id} avec X-Checkout-Session`. Domaines : API, persistance, concurrence.
- **Références :** [app/application/gestion_achats/use_cases/consulter_retour_paiement.py:11](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/consulter_retour_paiement.py#L11), [app/infrastructure/paiement/paiement_gateway.py:226](../../../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py#L226). Sources initiales : API-03.
- **Preuve actualisée : FORTEMENT ÉTAYÉ PAR LE CODE — NON MESURÉ.** M08 NON EXÉCUTÉ : aucune durée Stripe ni occupation du pool relevée. Variante sans en-tête évite cet appel.
- **Confiance :** Élevée pour expansions et UoW ouverte ; impact réel inconnu.
- **Correction minimale :** Créer une lecture de métadonnées spécifique sans expand ; autoriser dans une UoW courte, fermer avant HTTP, relire et réautoriser l’achat/token à la réponse. Conserver le helper enrichi des autres consommateurs et le statut webhook local.
- **Effort / risque :** M / Moyen. **Compatibilité :** La revalidation après I/O doit couvrir expiration/révocation du token et session incompatible. Aucun cache financier proposé. Breaking change : non visé, sous réserve des contrôles métier avant/après ; aucune preuve d’implémentation acquise.
- **Priorité / vote :** P2 ; 5/6 favorables simulés à l’étape 3, pas de nouveau vote.
- **Gain démontré :** aucun. **Gain plausible :** Moins d’enrichissement distant et de temps SQL retenu ; état/token à revalider après attente. **Gain chiffré : NON MESURÉ.**
- **Mesures avant/après nécessaires :** M08 du [plan de mesures](plan-mesures.md), précisions et limites du [protocole](../benchmarks/protocole.md). Même jeu/configuration, métriques API/SQL/RSS et invariants propres au flux avant toute acceptation.

## Secondaires et suites

Les risques OnBoard/pixels, population de tirage, transaction fournisseur et executor scheduler restent dans [l’annexe](annexe-optimisations-secondaires.md), avec leurs niveaux de preuve d’étape 3 ; aucun nouveau profil ne les réfute. Le cache médias et la projection historique demeurent différés. L’étape 4 ne justifie aucune migration, refonte ou augmentation générale des workers.

Aucune implémentation, migration ou activation. **Étape 5 en attente d’autorisation utilisateur.** Les huit corrections sont des orientations compatibles à vérifier, pas des garanties de gains ni une décision de déploiement.
