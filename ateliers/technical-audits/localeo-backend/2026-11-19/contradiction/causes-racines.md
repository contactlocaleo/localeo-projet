# Causes racines et traçabilité

Référence : backend `7049e7fafc76f9119924f1082a5ee7457a175d85`, inspection directe du 19 novembre 2026. Les 17 constats principaux deviennent 14 causes candidates : quatre lectures convergent vers RC-01 ; ASY-03/SRE-01 convergent vers RC-08. API-02 est scindé : RC-11 porte le budget I/O, RC-14 la répétition des contrôles. Les autres causes restent distinctes. Aucun impact n’est additionné entre domaines et aucune mesure nouvelle n’est disponible.

Un fait de code est établi par lecture ; sa conséquence opérationnelle est un risque étayé ou une hypothèse. Aucun incident de performance n’est CONFIRMÉ PAR MESURE. Les décisions finales renvoient au [débat](debats-et-votes.md) et à la [contre-expertise indépendante](contre-expertise.md).

## RC-01 — Projections statistiques fabriquées avec des lecteurs exhaustifs

Constats dédupliqués : CPU-01, MEM-01, DB-01, API-01. Flux : F05 pilotage ; F09 suivi organisateur. Domaines : CPU, mémoire, persistance, API.

API : `GET /protected/animation-locale/dashboard-performance (sans mode_lecture=borne) ; GET /protected/animation-locale/animations/{id}/live ; détails appelant _animation_detail`.

Symptômes : Hydratation intertenant, relectures par animation, mapping pour len/count et latence potentielle.

Cause : Le service de dashboard charge tous les participants et filtre ensuite ; live et détails chargent les entités d’une animation pour des compteurs. Le lecteur ne porte pas la projection agrégée demandée.

Preuves : [app/application/animation_locale/services/pilotage_animation.py:101](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L101), [app/application/animation_locale/services/pilotage_animation.py:65](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L65), [app/api/animation_locale_api.py:1331](../../../../../../localeo-backend/app/api/animation_locale_api.py#L1331), [app/infrastructure/persistence/repositories/animation_locale_repositories.py:1343](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L1343).

Objection retenue : Le frontend courant demande borne ; live reste consommé. Une recommandation de projection commune, deux expositions distinguées ; aucun changement silencieux du mode par défaut.

Décision : **OPT-04 / P2**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-02 — Qualification historique calculée avant pagination

Constats dédupliqués : CPU-02. Flux : F09 participants historiques. Domaines : CPU, mémoire, persistance.

API : `GET /protected/animation-locale/participants ; GET /protected/animation-locale/animations/{id}/participants`.

Symptômes : Petite page précédée d’un parcours et tri complets.

Cause : list(_iter_participations), qualification et filtres en Python puis tranche de page ; le lot de 500 ne borne pas le parcours entier.

Preuves : [app/application/animation_locale/services/exploitation_animation.py:36](../../../../../../localeo-backend/app/application/animation_locale/services/exploitation_animation.py#L36), [app/application/animation_locale/services/exploitation_animation.py:288](../../../../../../localeo-backend/app/application/animation_locale/services/exploitation_animation.py#L288).

Objection retenue : Aucun appel UI actuel établi ; moteurs récents ont leurs pages dédiées. Une projection durable est disproportionnée sans volume/usage.

Décision : **Annexe / P3**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-03 — Budget documentaire exprimé en octets encodés

Constats dédupliqués : MEM-02. Flux : F06 OnBoard documentaire. Domaines : Mémoire, CPU, concurrence.

API : `POST /internal/onboard/api/dossiers/{dossier_id}/documents`.

Symptômes : Pics de rasters multipages ; pas de fuite persistante établie.

Cause : Les octets d’entrée et 20 pages sont bornés, mais toutes les pages RGB coexistent au moment du PDF, sans budget cumulé de pixels applicatif.

Preuves : [app/api/onboarding_commercant_api.py:241](../../../../../../localeo-backend/app/api/onboarding_commercant_api.py#L241), [app/security/document_upload.py:126](../../../../../../localeo-backend/app/security/document_upload.py#L126), [app/security/document_upload.py:163](../../../../../../localeo-backend/app/security/document_upload.py#L163).

Objection retenue : Le finally ferme déjà les pages. Pillow impose ses propres garde-fous. Nouveaux refus = breaking change ; pas de correction compatible prétendue complète sans mesure.

Décision : **Annexe / P2 investigation**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-04 — Contrat de tirage Coffrets portant une population exhaustive

Constats dédupliqués : MEM-03. Flux : F08 tirage Coffrets. Domaines : Mémoire, CPU, persistance, verrous.

API : `POST /protected/animation-locale/animations/{id}/tirages`.

Symptômes : UUID, tuple, set de contrôle et copie list proportionnels au nombre d’éligibles.

Cause : Le repository recharge tous les membres figés et le domaine attend une séquence entière pour contrôler et sélectionner.

Preuves : [app/infrastructure/persistence/repositories/animation_locale_repositories.py:1717](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L1717), [app/domaine/animation_locale/entities/tirage_animation.py:76](../../../../../../localeo-backend/app/domaine/animation_locale/entities/tirage_animation.py#L76).

Objection retenue : Un tirage global peut légitimement coûter O(N). Retirer une copie ne borne pas le chargement ; refonte par rangs/réservoir non adoptée sans preuve et contrat aléatoire.

Décision : **Annexe / P2 mesure, P3 refonte**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-05 — Pagination des entrées sans génération en flux de la sortie

Constats dédupliqués : MEM-04. Flux : F10 finance ERP. Domaines : Mémoire, API, persistance.

API : `GET /internal/gestion-achats/paiements/export-metier.csv ; GET /internal/gestion-achats/paiements/export-finance.csv`.

Symptômes : CSV complet en StringIO malgré pages SQL de 100.

Cause : Le générateur est consommé dans produire_csv puis retourné sous forme d’une chaîne complète avec BOM.

Preuves : [app/application/gestion_achats/services/consultation_paiements.py:150](../../../../../../localeo-backend/app/application/gestion_achats/services/consultation_paiements.py#L150), [app/application/gestion_achats/services/export_financier.py:13](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13).

Objection retenue : Période limitée, colonnes scalaires et accès interne : pas d’OOM prouvé. Spool avant réponse conserve erreurs/audit et libère la transaction avant client lent.

Décision : **OPT-06 / P2**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-06 — Frontière async/sync absente sur les commandes batch ERP

Constats dédupliqués : ASY-01. Flux : F12 batch ERP ; F01/F03 effets indirects. Domaines : Concurrence, API, SRE.

API : `POST /internal/emails/batch/envoyer ; /internal/emails/batch/synchroniser-statuts ; /internal/sms/batch/envoyer ; /internal/sms/batch/synchroniser-statuts`.

Symptômes : La boucle du processus attend SQL et HTTP synchrones.

Cause : Les handlers async appellent BatchRunner.execute puis requests dans leur thread, sans déport de l’unité synchrone.

Preuves : [app/infrastructure/admin/admin.py:12523](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523), [app/infrastructure/admin/admin.py:12543](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12543), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642).

Objection retenue : Scénario : opérateur lance un lot non vide pendant lectures/scans du même processus ; une attente Brevo bloque cette boucle. Nombre de processus et fréquence restent inconnus.

Décision : **OPT-01 / P1**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-07 — Autorisation de remise maintenue par une transaction couvrant le fournisseur

Constats dédupliqués : ASY-02. Flux : F12 remise email/SMS. Domaines : Persistance, concurrence, accès, SRE.

API : `POST /protected/exploitation/emails/batch/envoyer ; POST /protected/exploitation/sms/batch/envoyer ; variantes ERP RC-06`.

Symptômes : Connexion et verrous conservés pendant HTTP ; attente de révocation possible.

Cause : Les verrous de capacité et de message restent détenus jusqu’au résultat fournisseur pour protéger les droits courants.

Preuves : [app/application/exploitation/use_cases/emails_batch.py:72](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L72), [app/infrastructure/persistence/repositories/repositories_sqlalchemy.py:1105](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py#L1105), [app/infrastructure/persistence/conservation_emails_saas.py:96](../../../../../../localeo-backend/app/infrastructure/persistence/conservation_emails_saas.py#L96).

Objection retenue : Cause DISTINCTE de RC-08. Les budgets OPT-02 atténuent sa durée sans la supprimer. Sortir HTTP de la transaction exige un protocole métier ; aucun ticket de découplage retenu.

Décision : **Annexe / P2 mesure**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-08 — Durée d’exécution serveur non liée au bail de batch

Constats dédupliqués : ASY-03, SRE-01. Flux : F12 batchs ; F03 livraison et F01 capacité indirecte. Domaines : Concurrence, persistance, API, SRE.

API : `POST /protected/exploitation/emails/batch/envoyer ; variantes SMS et ERP ; autres BatchRunner à vérifier individuellement`.

Symptômes : Travail survivant au timeout client et chevauchement après expiration du bail.

Cause : Le timeout catalogue alimente le client et le bail timeout+60 ; handler() n’a ni budget de cycle imposé ni renouvellement du bail.

Preuves : [app/application/exploitation/services/batchs.py:608](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642), [app/infrastructure/scheduler/http_client.py:34](../../../../../../localeo-backend/app/infrastructure/scheduler/http_client.py#L34), [app/application/exploitation/use_cases/emails_batch.py:25](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L25).

Objection retenue : Scénario crédible non mesuré : lot de 100 remises séquentielles, fournisseur lent ; somme des attentes >360 s et nouveau lancement. Aucun double envoi démontré ; messages déjà réservés ne doivent pas être abandonnés.

Décision : **OPT-02 / P1**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-09 — Aides de détail réutilisées sous verrou de lot d’expiration

Constats dédupliqués : DB-02. Flux : F12 expiration Coffrets ; F01 ressources et verrous partagés. Domaines : Persistance, concurrence, mémoire.

API : `POST /protected/gestion-achats/coffrets-instances/expiration/batch`.

Symptômes : Requête de relance par instance, relations lazy possibles et durée du lot sous verrou.

Cause : La sélection verrouille jusqu’à la limite, puis la boucle charge faits et relances unitairement avant un commit final.

Preuves : [app/application/gestion_achats/use_cases/expiration_coffrets.py:118](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L118), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [app/infrastructure/persistence/models.py:509](../../../../../../localeo-backend/app/infrastructure/persistence/models.py#L509).

Objection retenue : Lot borné, SKIP LOCKED et exclusion remboursements présents. La validité d’un scan d’instance déjà expirée n’est pas supposée ; impact transversal réel à mesurer.

Décision : **OPT-05 / P2**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-10 — Idempotence évaluée après la limite de candidats

Constats dédupliqués : DB-03. Flux : F12 rappels avant expiration. Domaines : Persistance, progression, latence métier.

API : `POST /protected/gestion-achats/coffrets-instances/expiration/reminders/batch`.

Symptômes : Préfixe traité relu ; candidats restants potentiellement jamais sélectionnés dans leur fenêtre.

Cause : LIMIT est appliqué aux instances actives avant _existing_relance ; ni exclusion SQL ni curseur de travail restant.

Preuves : [app/application/gestion_achats/use_cases/expiration_coffrets.py:239](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L239), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [sql/v141_relances_expiration_coffrets.sql:35](../../../../../../localeo-backend/sql/v141_relances_expiration_coffrets.sql#L35).

Objection retenue : Défaut de progression fortement étayé ; cohorte >limite et perte effective non établies. P1 refusé après contradiction ; garder contraintes d’unicité et tests simultanés.

Décision : **OPT-03 / P2**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-11 — Budget de lecture média vérifié autour d’un I/O bloquant

Constats dédupliqués : API-02. Flux : F02/F09 lecture personnelle Live. Domaines : API, concurrence, CPU, stockage.

API : `GET /public/localeo-live/participations/{id}`.

Symptômes : Budget dépassé détecté seulement après retour I/O ; les décodages répétés relèvent de RC-14.

Cause : hydrater_medias lit et valide chaque média, hors transaction ; le budget n’est pas transmis au get S3/Body.read.

Preuves : [app/application/animation_locale/services/contenu_generation.py:368](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L368), [app/infrastructure/storage/document_storage.py:83](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L83), [app/infrastructure/storage/document_storage.py:104](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L104), [app/application/animation_locale/services/jeu_animation.py:459](../../../../../../localeo-backend/app/application/animation_locale/services/jeu_animation.py#L459).

Objection retenue : 44 Ko par média et 256 Ko de projection, gardes de lecture et dimensions strictes. Pas de payload illimité. Budget réseau d’abord ; cache privé non adopté avant mesure et invalidation.

Décision : **OPT-07 / P2**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-12 — Helper de réconciliation financière utilisé pour une lecture légère

Constats dédupliqués : API-03. Flux : F10 retour paiement. Domaines : API, persistance, concurrence.

API : `GET /public/gestion-achats/paiements/retour/{achat_id} avec X-Checkout-Session`.

Symptômes : Expansions Stripe non consommées et connexion SQL retenue pendant HTTP.

Cause : L’achat/token est lu avant retrieve enrichi ; seule metadata.achat_id sert à cette vérification, état financier toujours local.

Preuves : [app/application/gestion_achats/use_cases/consulter_retour_paiement.py:11](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/consulter_retour_paiement.py#L11), [app/infrastructure/paiement/paiement_gateway.py:226](../../../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py#L226).

Objection retenue : Absence d’en-tête évite l’appel. Créer une lecture minimale spécifique, fermer puis relire et réautoriser ; ne pas modifier le helper partagé ni supprimer la correspondance de session.

Décision : **OPT-08 / P2**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-13 — Classes de jobs partageant le même executor scheduler

Constats dédupliqués : SRE-02. Flux : F12 communications/CRM ; F08 clôtures/F11 génération. Domaines : Ordonnancement, SRE, concurrence.

API : `POST /internal/prospection-batch/referentiels ; batchs communication, génération et clôture planifiés`.

Symptômes : Attente de place et misfire possibles, sans incident ni saturation observés.

Cause : Tous les jobs sont associés au pool default ; cadence alignée dans les défauts ; durées réelles et remplacements cron inconnus.

Preuves : [app/infrastructure/scheduler/coordinator.py:110](../../../../../../localeo-backend/app/infrastructure/scheduler/coordinator.py#L110), [app/application/exploitation/services/batchs.py:364](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L364), [app/infrastructure/scheduler/settings.py:95](../../../../../../localeo-backend/app/infrastructure/scheduler/settings.py#L95).

Objection retenue : Partage prouvé, contention opérationnelle HYPOTHÈSE À VÉRIFIER. max_instances/coalesce/bail et logs misfire existent ; ne pas augmenter les workers sans budget global.

Décision : **Annexe / P3 isolation**. Confiance forte dans le mécanisme de code ; impact réel non quantifié. RC-13 : seulement hypothèse de saturation. Correction et mesures : voir orientation correspondante ou annexe.

## RC-14 — Revalidation répétée de médias immuables

Source : API-02, scindée pour ne pas confondre deux remèdes. Flux F02/F09 ; `GET /public/localeo-live/participations/{id}` avec médias sélectionnés. Domaines CPU, allocations, API et stockage. Le service relit et contrôle intégralement les octets à chaque projection, puis charge le WebP. Preuves : [contrôle](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L300), [hydratation](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L368), [décodeur](../../../../../../localeo-backend/app/infrastructure/animation_locale/decodage_illustration.py#L10).

Le mécanisme est confirmé par lecture, mais l’impact excessif est une hypothèse : images ≤44 000 octets, dimensions strictes, projection bornée et contrôle d’intégrité utile. Cache conditionné à M07, classé P3 avant mesure ; aucun second correctif obligatoire ajouté à OPT-07. Source relue, aucun coût CPU réel mesuré.
