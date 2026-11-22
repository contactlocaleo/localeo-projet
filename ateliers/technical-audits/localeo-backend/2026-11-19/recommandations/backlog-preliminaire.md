# Backlog préliminaire resserré

Huit orientations, dédupliquées par cause et flux ; aucune implémentation autorisée. **Aucun P0. Deux P1 et six P2.** P1 signifie risque technique significatif avec déclencheur argumenté, pas incident mesuré. Tous les gains et percentiles sont inconnus. Les causes non retenues et les remèdes disproportionnés restent dans [l’annexe](annexe-optimisations-secondaires.md).

Le vote est une simulation explicite de six perspectives, rédigée par l’orchestrateur ; aucune prétention à un nouveau scrutin réel des agents. Les justifications, abstentions et refus d’alternatives sont dans [debats-et-votes.md](../contradiction/debats-et-votes.md). Adoption ≥4/6 ; contradicteur sans voix. Le vote ne relève aucune priorité et ne remplace aucune preuve.

| ID | Orientation | Priorité | Effort | Vote simulé favorable |
| --- | --- | --- | --- | --- |
| OPT-01 | Déporter les quatre batchs ERP hors de la boucle | P1 | S | 6/6 |
| OPT-02 | Lier travail serveur, réservations et durée de bail | P1 | M | 6/6 |
| OPT-03 | Sélectionner les relances restantes avant LIMIT | P2 | S | 5/6 |
| OPT-04 | Remplacer les lectures de faits par des projections agrégées | P2 | M | 5/6 |
| OPT-05 | Grouper les faits du lot d’expiration | P2 | M | 5/6 |
| OPT-06 | Préparer les CSV paiements dans un spool | P2 | M | 4/6 |
| OPT-07 | Transmettre les budgets aux lectures de médias distants | P2 | M | 4/6 |
| OPT-08 | Alléger la vérification Stripe du retour de paiement | P2 | M | 5/6 |

## OPT-01 — Déporter les quatre batchs ERP hors de la boucle

Cause : **RC-06**, Les handlers async appellent BatchRunner.execute puis requests dans leur thread, sans déport de l’unité synchrone.

Flux : F12 batch ERP ; F01/F03 effets indirects. API : `POST /internal/emails/batch/envoyer ; /internal/emails/batch/synchroniser-statuts ; /internal/sms/batch/envoyer ; /internal/sms/batch/synchroniser-statuts`. Domaines : Concurrence, API, SRE.

Preuves : [app/infrastructure/admin/admin.py:12523](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523), [app/infrastructure/admin/admin.py:12543](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12543), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642). Sources indépendantes : ASY-01. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Déporter l’unité synchrone complète (résolution opérateur, UoW, BatchRunner et fournisseur) vers le mécanisme de threadpool existant. Conserver corrélation, erreurs et redirections ; pas de partage d’une session entre threads.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. Préserve la réponse ; ne crée aucune capacité SQL supplémentaire garantie.

Effort : **S**. Risque : **Faible à moyen**. Priorité : **P1**. Justification : Scénario : opérateur lance un lot non vide pendant lectures/scans du même processus ; une attente Brevo bloque cette boucle. Nombre de processus et fréquence restent inconnus.

Vote simulé : **6/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M01**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-02 — Lier travail serveur, réservations et durée de bail

Cause : **RC-08**, Le timeout catalogue alimente le client et le bail timeout+60 ; handler() n’a ni budget de cycle imposé ni renouvellement du bail.

Flux : F12 batchs ; F03 livraison et F01 capacité indirecte. API : `POST /protected/exploitation/emails/batch/envoyer ; variantes SMS et ERP ; autres BatchRunner à vérifier individuellement`. Domaines : Concurrence, persistance, API, SRE.

Preuves : [app/application/exploitation/services/batchs.py:608](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642), [app/infrastructure/scheduler/http_client.py:34](../../../../../../localeo-backend/app/infrastructure/scheduler/http_client.py#L34), [app/application/exploitation/use_cases/emails_batch.py:25](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L25). Sources indépendantes : ASY-03, SRE-01. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Budget monotone de cycle, réservation progressive ou restitution prouvée des éléments non commencés, délais fournisseur connect/read/retry explicites. Arrêter de prendre du travail si bail perdu ; renouvellement propriétaire pour les handlers pouvant légitimement durer. Aucun arrêt forcé d’un effet fournisseur incertain.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. Le budget ne coupe pas automatiquement un appel en vol ; préserver révocation, idempotence et rapprochement incertain.

Effort : **M**. Risque : **Moyen**. Priorité : **P1**. Justification : Scénario crédible non mesuré : lot de 100 remises séquentielles, fournisseur lent ; somme des attentes >360 s et nouveau lancement. Aucun double envoi démontré ; messages déjà réservés ne doivent pas être abandonnés.

Vote simulé : **6/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M02**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-03 — Sélectionner les relances restantes avant LIMIT

Cause : **RC-10**, LIMIT est appliqué aux instances actives avant _existing_relance ; ni exclusion SQL ni curseur de travail restant.

Flux : F12 rappels avant expiration. API : `POST /protected/gestion-achats/coffrets-instances/expiration/reminders/batch`. Domaines : Persistance, progression, latence métier.

Preuves : [app/application/gestion_achats/use_cases/expiration_coffrets.py:239](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L239), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [sql/v141_relances_expiration_coffrets.sql:35](../../../../../../localeo-backend/sql/v141_relances_expiration_coffrets.sql#L35). Sources indépendantes : DB-03. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : NOT EXISTS avant LIMIT sur instance/date_expiration/type/reminder_days, ordre total date+ID ; conserver l’unicité et le contrôle de concurrence. Pas de migration d’index par défaut.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. Même fenêtre et même contenu ; aucune garantie de deux lanceurs sans test de concurrence.

Effort : **S**. Risque : **Faible à moyen**. Priorité : **P2**. Justification : Défaut de progression fortement étayé ; cohorte >limite et perte effective non établies. P1 refusé après contradiction ; garder contraintes d’unicité et tests simultanés.

Vote simulé : **5/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M03**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-04 — Remplacer les lectures de faits par des projections agrégées

Cause : **RC-01**, Le service de dashboard charge tous les participants et filtre ensuite ; live et détails chargent les entités d’une animation pour des compteurs. Le lecteur ne porte pas la projection agrégée demandée.

Flux : F05 pilotage ; F09 suivi organisateur. API : `GET /protected/animation-locale/dashboard-performance (sans mode_lecture=borne) ; GET /protected/animation-locale/animations/{id}/live ; détails appelant _animation_detail`. Domaines : CPU, mémoire, persistance, API.

Preuves : [app/application/animation_locale/services/pilotage_animation.py:101](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L101), [app/application/animation_locale/services/pilotage_animation.py:65](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L65), [app/api/animation_locale_api.py:1331](../../../../../../localeo-backend/app/api/animation_locale_api.py#L1331), [app/infrastructure/persistence/repositories/animation_locale_repositories.py:1343](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L1343). Sources indépendantes : CPU-01, MEM-01, DB-01, API-01. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Pousser périmètre et période dans SQL, calculer les compteurs/séries/top et fournir des résumés groupés aux détails. Appliquer le même lecteur de compteurs aux vues live. Garder la forme historique ; ne pas substituer le mode borne.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. Dates Paris, statuts, archives et mode de réponse identiques. Coût des résultats autorisés encore proportionnel aux animations réellement rendues.

Effort : **M**. Risque : **Moyen**. Priorité : **P2**. Justification : Le frontend courant demande borne ; live reste consommé. Une recommandation de projection commune, deux expositions distinguées ; aucun changement silencieux du mode par défaut.

Vote simulé : **5/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M04**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-05 — Grouper les faits du lot d’expiration

Cause : **RC-09**, La sélection verrouille jusqu’à la limite, puis la boucle charge faits et relances unitairement avant un commit final.

Flux : F12 expiration Coffrets ; F01 ressources et verrous partagés. API : `POST /protected/gestion-achats/coffrets-instances/expiration/batch`. Domaines : Persistance, concurrence, mémoire.

Preuves : [app/application/gestion_achats/use_cases/expiration_coffrets.py:118](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L118), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [app/infrastructure/persistence/models.py:509](../../../../../../localeo-backend/app/infrastructure/persistence/models.py#L509). Sources indépendantes : DB-02. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Charger les relances en un ensemble borné et les relations nécessaires en requêtes groupées pour les IDs verrouillés ; conserver la sélection de racines, l’ordre de verrous et le commit actuel. Ne pas joindre une collection avant LIMIT/FOR UPDATE.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. Préserve atomisme, garde remboursement et crédit B2B ; mesurer aussi les octets et pas seulement le nombre SQL.

Effort : **M**. Risque : **Moyen**. Priorité : **P2**. Justification : Lot borné, SKIP LOCKED et exclusion remboursements présents. La validité d’un scan d’instance déjà expirée n’est pas supposée ; impact transversal réel à mesurer.

Vote simulé : **5/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M05**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-06 — Préparer les CSV paiements dans un spool

Cause : **RC-05**, Le générateur est consommé dans produire_csv puis retourné sous forme d’une chaîne complète avec BOM.

Flux : F10 finance ERP. API : `GET /internal/gestion-achats/paiements/export-metier.csv ; GET /internal/gestion-achats/paiements/export-finance.csv`. Domaines : Mémoire, API, persistance.

Preuves : [app/application/gestion_achats/services/consultation_paiements.py:150](../../../../../../localeo-backend/app/application/gestion_achats/services/consultation_paiements.py#L150), [app/application/gestion_achats/services/export_financier.py:13](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13). Sources indépendantes : MEM-04. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Écrire progressivement dans un fichier temporaire à seuil mémoire, terminer génération/audit puis fermer la projection SQL avant réponse par blocs. Fermer/supprimer le temporaire en succès, erreur ou abandon.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. Mêmes colonnes, BOM, format, filtres et erreurs avant envoi ; ne pas supprimer une cohérence d’instantané si le contrat l’exige.

Effort : **M**. Risque : **Faible à moyen**. Priorité : **P2**. Justification : Période limitée, colonnes scalaires et accès interne : pas d’OOM prouvé. Spool avant réponse conserve erreurs/audit et libère la transaction avant client lent.

Vote simulé : **4/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M06**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-07 — Transmettre les budgets aux lectures de médias distants

Cause : **RC-11**, hydrater_medias lit et valide chaque média, hors transaction ; le budget n’est pas transmis au get S3/Body.read.

Flux : F02/F09 lecture personnelle Live. API : `GET /public/localeo-live/participations/{id}`. Domaines : API, concurrence, CPU, stockage.

Preuves : [app/application/animation_locale/services/contenu_generation.py:368](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L368), [app/infrastructure/storage/document_storage.py:83](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L83), [app/infrastructure/storage/document_storage.py:104](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L104), [app/application/animation_locale/services/jeu_animation.py:459](../../../../../../localeo-backend/app/application/animation_locale/services/jeu_animation.py#L459). Sources indépendantes : API-02. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Budget restant et politique explicite connect/read/retries dans l’adaptateur documentaire, fermeture du Body et lecture bornée aux octets attendus. Préserver SHA, provenance et autorisation ; ne pas annoncer une échéance dure sans moyen d’interruption effectif.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. JSON et contrôle d’intégrité inchangés ; effets sur les autres consommateurs du stockage à tester. Cache : orientation séparée différée.

Effort : **M**. Risque : **Moyen**. Priorité : **P2**. Justification : 44 Ko par média et 256 Ko de projection, gardes de lecture et dimensions strictes. Pas de payload illimité. Budget réseau d’abord ; cache privé non adopté avant mesure et invalidation.

Vote simulé : **4/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M07**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.

## OPT-08 — Alléger la vérification Stripe du retour de paiement

Cause : **RC-12**, L’achat/token est lu avant retrieve enrichi ; seule metadata.achat_id sert à cette vérification, état financier toujours local.

Flux : F10 retour paiement. API : `GET /public/gestion-achats/paiements/retour/{achat_id} avec X-Checkout-Session`. Domaines : API, persistance, concurrence.

Preuves : [app/application/gestion_achats/use_cases/consulter_retour_paiement.py:11](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/consulter_retour_paiement.py#L11), [app/infrastructure/paiement/paiement_gateway.py:226](../../../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py#L226). Sources indépendantes : API-03. Statut : **FORTEMENT ÉTAYÉ PAR LE CODE** ; confiance forte sur le mécanisme, impact réel inconnu. Aucune mesure disponible.

Correction minimale unique : Créer une lecture de métadonnées spécifique sans expand ; autoriser dans une UoW courte, fermer avant HTTP, relire et réautoriser l’achat/token à la réponse. Conserver le helper enrichi des autres consommateurs et le statut webhook local.

Compatibilité / breaking change : **non visé**, conditionnée aux preuves suivantes. La revalidation après I/O doit couvrir expiration/révocation du token et session incompatible. Aucun cache financier proposé.

Effort : **M**. Risque : **Moyen**. Priorité : **P2**. Justification : Absence d’en-tête évite l’appel. Créer une lecture minimale spécifique, fermer puis relire et réautoriser ; ne pas modifier le helper partagé ni supprimer la correspondance de session.

Vote simulé : **5/6, orientation adoptée sous ces conditions**, et non autorisation d’exécuter. Plan de mesure : **M08**, [plan-mesures.md](plan-mesures.md). Les tests et budgets devront être fixés avant exécution.
