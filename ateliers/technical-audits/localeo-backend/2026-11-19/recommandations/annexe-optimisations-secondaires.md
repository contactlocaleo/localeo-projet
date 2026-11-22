# Optimisations secondaires, causes différées et remèdes refusés

Ces éléments restent traçables ; ils ne deviennent pas des tickets supplémentaires du backlog principal. Aucun nouvel incident ni gain prouvé. Les votes sont simulés et détaillés dans [le débat](../contradiction/debats-et-votes.md).

## RC-02 — Qualification historique calculée avant pagination

Source : CPU-02. Flux : F09 participants historiques. API : `GET /protected/animation-locale/participants ; GET /protected/animation-locale/animations/{id}/participants`. Domaines : CPU, mémoire, persistance.

Fait : list(_iter_participations), qualification et filtres en Python puis tranche de page ; le lot de 500 ne borne pas le parcours entier. Symptôme possible : Petite page précédée d’un parcours et tri complets.

Preuves : [app/application/animation_locale/services/exploitation_animation.py:36](../../../../../../localeo-backend/app/application/animation_locale/services/exploitation_animation.py#L36), [app/application/animation_locale/services/exploitation_animation.py:288](../../../../../../localeo-backend/app/application/animation_locale/services/exploitation_animation.py#L288).

Décision et objection : **Annexe / P3**. Aucun appel UI actuel établi ; moteurs récents ont leurs pages dédiées. Une projection durable est disproportionnée sans volume/usage.

## RC-03 — Budget documentaire exprimé en octets encodés

Source : MEM-02. Flux : F06 OnBoard documentaire. API : `POST /internal/onboard/api/dossiers/{dossier_id}/documents`. Domaines : Mémoire, CPU, concurrence.

Fait : Les octets d’entrée et 20 pages sont bornés, mais toutes les pages RGB coexistent au moment du PDF, sans budget cumulé de pixels applicatif. Symptôme possible : Pics de rasters multipages ; pas de fuite persistante établie.

Preuves : [app/api/onboarding_commercant_api.py:241](../../../../../../localeo-backend/app/api/onboarding_commercant_api.py#L241), [app/security/document_upload.py:126](../../../../../../localeo-backend/app/security/document_upload.py#L126), [app/security/document_upload.py:163](../../../../../../localeo-backend/app/security/document_upload.py#L163).

Décision et objection : **Annexe / P2 investigation**. Le finally ferme déjà les pages. Pillow impose ses propres garde-fous. Nouveaux refus = breaking change ; pas de correction compatible prétendue complète sans mesure.

## RC-04 — Contrat de tirage Coffrets portant une population exhaustive

Source : MEM-03. Flux : F08 tirage Coffrets. API : `POST /protected/animation-locale/animations/{id}/tirages`. Domaines : Mémoire, CPU, persistance, verrous.

Fait : Le repository recharge tous les membres figés et le domaine attend une séquence entière pour contrôler et sélectionner. Symptôme possible : UUID, tuple, set de contrôle et copie list proportionnels au nombre d’éligibles.

Preuves : [app/infrastructure/persistence/repositories/animation_locale_repositories.py:1717](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L1717), [app/domaine/animation_locale/entities/tirage_animation.py:76](../../../../../../localeo-backend/app/domaine/animation_locale/entities/tirage_animation.py#L76).

Décision et objection : **Annexe / P2 mesure, P3 refonte**. Un tirage global peut légitimement coûter O(N). Retirer une copie ne borne pas le chargement ; refonte par rangs/réservoir non adoptée sans preuve et contrat aléatoire.

## RC-07 — Autorisation de remise maintenue par une transaction couvrant le fournisseur

Source : ASY-02. Flux : F12 remise email/SMS. API : `POST /protected/exploitation/emails/batch/envoyer ; POST /protected/exploitation/sms/batch/envoyer ; variantes ERP RC-06`. Domaines : Persistance, concurrence, accès, SRE.

Fait : Les verrous de capacité et de message restent détenus jusqu’au résultat fournisseur pour protéger les droits courants. Symptôme possible : Connexion et verrous conservés pendant HTTP ; attente de révocation possible.

Preuves : [app/application/exploitation/use_cases/emails_batch.py:72](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L72), [app/infrastructure/persistence/repositories/repositories_sqlalchemy.py:1105](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py#L1105), [app/infrastructure/persistence/conservation_emails_saas.py:96](../../../../../../localeo-backend/app/infrastructure/persistence/conservation_emails_saas.py#L96).

Décision et objection : **Annexe / P2 mesure**. Cause DISTINCTE de RC-08. Les budgets OPT-02 atténuent sa durée sans la supprimer. Sortir HTTP de la transaction exige un protocole métier ; aucun ticket de découplage retenu.

## RC-13 — Classes de jobs partageant le même executor scheduler

Source : SRE-02. Flux : F12 communications/CRM ; F08 clôtures/F11 génération. API : `POST /internal/prospection-batch/referentiels ; batchs communication, génération et clôture planifiés`. Domaines : Ordonnancement, SRE, concurrence.

Fait : Tous les jobs sont associés au pool default ; cadence alignée dans les défauts ; durées réelles et remplacements cron inconnus. Symptôme possible : Attente de place et misfire possibles, sans incident ni saturation observés.

Preuves : [app/infrastructure/scheduler/coordinator.py:110](../../../../../../localeo-backend/app/infrastructure/scheduler/coordinator.py#L110), [app/application/exploitation/services/batchs.py:364](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L364), [app/infrastructure/scheduler/settings.py:95](../../../../../../localeo-backend/app/infrastructure/scheduler/settings.py#L95).

Décision et objection : **Annexe / P3 isolation**. Partage prouvé, contention opérationnelle HYPOTHÈSE À VÉRIFIER. max_instances/coalesce/bail et logs misfire existent ; ne pas augmenter les workers sans budget global.

## RC-14 — Revalidation complète de médias immuables à chaque lecture

Source : API-02. Flux : F02/F09 lecture joueur. API : `GET /public/localeo-live/participations/{id}, avec illustration sélectionnée`. Domaines : CPU, allocations, API, stockage.

Fait : Le service réemploie le contrôle complet de contenu pour la projection, sans réutilisation des octets validés entre requêtes. Symptôme possible : Même média récupéré, base64 encodé/décodé et image chargée à nouveau entre lectures.

Preuves : [app/application/animation_locale/services/contenu_generation.py:300](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L300), [app/application/animation_locale/services/contenu_generation.py:368](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L368), [app/infrastructure/animation_locale/decodage_illustration.py:10](../../../../../../localeo-backend/app/infrastructure/animation_locale/decodage_illustration.py#L10).

Décision et objection : **Annexe / P3 cache avant mesure**. Validations d’intégrité utiles, médias de 44 Ko maximum et projection bornée. Un cache ajoute mémoire et invalidation ; coût dominant non établi.

## Conditions de réouverture et corrections plus simples

- RC-02 : démontrer un moteur historique réellement installé et un client actif ; tester filtres, gel, provenance et total avant toute projection maintenue. Effort L, risque élevé ; aucun LIMIT naïf avant qualification. M09.
- RC-03 : mesurer RSS/native, dimensions compressées, vingt pages et concurrence sur limites autorisées. Réduire décodages temporaires et concurrence peut atténuer, sans résoudre le budget de pixels. Les pages RGB sont déjà fermées en finally ; nouveaux refus ou réduction de résolution exigent arbitrage de contrat et recette de lisibilité. Effort M à L, risque moyen à élevé, breaking possible explicitement non adopté. M10.
- RC-04 : mesurer nombre de membres et pic de copies à faible nombre de gagnants. Une copie `list(tuple)` éventuellement supprimable (S, compatibilité des random/doubles à vérifier) ne résout ni `.all()` ni set de validation. Refonte L et risque élevé sur équité/atomicité, non adoptée. M11.
- RC-07 : mesurer checkout et verrous par remise, révocation concomitante et délai fournisseur. Le correctif OPT-02 réduit la durée cumulée, pas ce mécanisme par message ; protocole de découplage L, haut risque métier. Le retour Stripe OPT-08 ne sert pas de modèle à une remise d’accès. M12.
- RC-13 : relever jobs actifs, crons réels, durée, attente et misfires ; échelonner les quelques tâches en conflit avec les variables existantes si nécessaire. Séparation executors M, hausse globale des threads non proposée. Incident de saturation HYPOTHÈSE À VÉRIFIER. M13.
- RC-14 : profil des décodages et taux réel de réutilisation avant cache M ; conserver droits et provenance courants, taille maximale, invalidation par SHA et cloisonnement. Ne pas mettre en cache une autorisation. M07.

## Autres observations des annexes indépendantes

DAM : charger un blob avant 304 ou métadonnées est évitable mais les tailles sont bornées ; projection metadata S après relevé de trafic, pas de décodage raster complet allégué (`images_api.py:178–215`, `uploads.py:82–89`). Logs stdout synchrones, santé profonde et bail scheduler dépendant du pool : hypothèses de propagation sous charge, à mesurer avant nouvelle infrastructure. Les index non repérés dans les fichiers ne sont pas déclarés absents en exploitation ; aucun index ni changement d’ORM prescrit sans SQL/plans réels sur cible jetable.

Les imports commerçants possèdent une limite d’octets et des garde-fous ZIP/XML ; leur génération d’arbre n’est pas déclarée illimitée. Les exports Animation bornés ou spoolés, worker de génération à sémaphore et webhooks déportés sont des contre-exemples vérifiés, pas des anomalies par présence d’une boucle. Voir les six annexes dans [agents](../agents/README.md) et [la contre-expertise](../contradiction/contre-expertise.md).
