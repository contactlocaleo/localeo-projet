# Débat contradictoire et votes techniques

Le contradicteur indépendant a d’abord relu les six rapports et les sources, puis a reçu un projet de décisions ; ses objections et sa réponse finale sont conservées dans [contre-expertise.md](contre-expertise.md). Les diagnostics initiaux de l’étape 2 restent inchangés. Les décisions ci-dessous incorporent ses objections : P2 pour DB-03 et statistiques historiques, absence de nouvelle limite d’image, pas de cache obligatoire ni de déplacement aveugle de commit.

**Les voix sont simulées par l’orchestrateur**, conformément au prompt, à partir des six perspectives et des rapports déjà finalisés. Aucun nouveau scrutin réel ni réponse de vote des agents n’est revendiqué. Chaque perspective CPU/Mémoire/Concurrence/Persistance/API/SRE a exactement une voix : F favorable, C contre, A abstention (non favorable). Adoption de l’orientation décrite si F ≥4 ; le contradicteur ne vote jamais. Les réserves ci-dessous sont des justifications simulées et non des citations d’agents. Le vote ne constitue ni mesure, ni autorisation, ni validation de P1.

| Orientation | CPU | Mémoire | Concurrence | Persistance | API | SRE | Favorables | Décision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPT-01 | F | F | F | F | F | F | 6/6 | Adoptée sous conditions |
| OPT-02 | F | F | F | F | F | F | 6/6 | Adoptée sous conditions |
| OPT-03 | F | F | A | F | F | F | 5/6 | Adoptée sous conditions |
| OPT-04 | F | F | A | F | F | F | 5/6 | Adoptée sous conditions |
| OPT-05 | F | A | F | F | F | F | 5/6 | Adoptée sous conditions |
| OPT-06 | A | F | A | F | F | F | 4/6 | Adoptée sous conditions |
| OPT-07 | A | F | F | A | F | F | 4/6 | Adoptée sous conditions |
| OPT-08 | F | A | F | F | F | F | 5/6 | Adoptée sous conditions |

## Débat OPT-01 — Déporter les quatre batchs ERP hors de la boucle

Diagnostic initial : La boucle du processus attend SQL et HTTP synchrones. Sources : ASY-01.

Preuves : [app/infrastructure/admin/admin.py:12523](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523), [app/infrastructure/admin/admin.py:12543](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12543), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642). Mécanisme : Les handlers async appellent BatchRunner.execute puis requests dans leur thread, sans déport de l’unité synchrone.

Objection / réponse : Scénario : opérateur lance un lot non vide pendant lectures/scans du même processus ; une attente Brevo bloque cette boucle. Nombre de processus et fréquence restent inconnus. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-06**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Convertir le handler en def si entièrement synchrone est plus simple qu’un nouveau worker ; conserver async et déporter l’unité complète si lecture async nécessaire. Nouveau broker refusé.

Correction minimale retenue : Déporter l’unité synchrone complète (résolution opérateur, UoW, BatchRunner et fournisseur) vers le mécanisme de threadpool existant. Conserver corrélation, erreurs et redirections ; pas de partage d’une session entre threads.

Risques / compatibilité : Faible à moyen. Préserve la réponse ; ne crée aucune capacité SQL supplémentaire garantie. Effort S, priorité P1.

Mesures nécessaires : M01 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : F : même travail CPU isolé de la boucle.
- Mémoire : F : aucune nouvelle collection sans borne.
- Concurrence : F : frontière async/sync directement corrigée.
- Persistance : F : UoW conservée dans son unité de travail.
- API : F : contrat et disponibilité de réponse préservés.
- SRE : F : propagation interrequêtes réduite.

Issue : **6/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-02 — Lier travail serveur, réservations et durée de bail

Diagnostic initial : Travail survivant au timeout client et chevauchement après expiration du bail. Sources : ASY-03, SRE-01.

Preuves : [app/application/exploitation/services/batchs.py:608](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608), [app/application/exploitation/services/batchs.py:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642), [app/infrastructure/scheduler/http_client.py:34](../../../../../../localeo-backend/app/infrastructure/scheduler/http_client.py#L34), [app/application/exploitation/use_cases/emails_batch.py:25](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L25). Mécanisme : Le timeout catalogue alimente le client et le bail timeout+60 ; handler() n’a ni budget de cycle imposé ni renouvellement du bail.

Objection / réponse : Scénario crédible non mesuré : lot de 100 remises séquentielles, fournisseur lent ; somme des attentes >360 s et nouveau lancement. Aucun double envoi démontré ; messages déjà réservés ne doivent pas être abandonnés. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-08**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Un cycle court avec réservation progressive est préféré à une infrastructure universelle de heartbeat. Renouveler le bail ne borne pas le travail ; un break après claim de tout le lot est refusé.

Correction minimale retenue : Budget monotone de cycle, réservation progressive ou restitution prouvée des éléments non commencés, délais fournisseur connect/read/retry explicites. Arrêter de prendre du travail si bail perdu ; renouvellement propriétaire pour les handlers pouvant légitimement durer. Aucun arrêt forcé d’un effet fournisseur incertain.

Risques / compatibilité : Moyen. Le budget ne coupe pas automatiquement un appel en vol ; préserver révocation, idempotence et rapprochement incertain. Effort M, priorité P1.

Mesures nécessaires : M02 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : F : limite le travail cumulé sans algorithme nouveau.
- Mémoire : F : réserve progressivement, évite rétention du lot inutile.
- Concurrence : F : budget/bail traités séparément, sans tuer un thread.
- Persistance : F : maintien des garanties de remise et propriété.
- API : F : même réponse, effets incertains préservés.
- SRE : F : scénario de chevauchement explicite et mesurable.

Issue : **6/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-03 — Sélectionner les relances restantes avant LIMIT

Diagnostic initial : Préfixe traité relu ; candidats restants potentiellement jamais sélectionnés dans leur fenêtre. Sources : DB-03.

Preuves : [app/application/gestion_achats/use_cases/expiration_coffrets.py:239](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L239), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [sql/v141_relances_expiration_coffrets.sql:35](../../../../../../localeo-backend/sql/v141_relances_expiration_coffrets.sql#L35). Mécanisme : LIMIT est appliqué aux instances actives avant _existing_relance ; ni exclusion SQL ni curseur de travail restant.

Objection / réponse : Défaut de progression fortement étayé ; cohorte >limite et perte effective non établies. P1 refusé après contradiction ; garder contraintes d’unicité et tests simultanés. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-10**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Réutiliser unicité et prédicat existants ; pas de nouvelle projection, de batch sans borne ou d’index ajouté sans plan.

Correction minimale retenue : NOT EXISTS avant LIMIT sur instance/date_expiration/type/reminder_days, ordre total date+ID ; conserver l’unicité et le contrôle de concurrence. Pas de migration d’index par défaut.

Risques / compatibilité : Faible à moyen. Même fenêtre et même contenu ; aucune garantie de deux lanceurs sans test de concurrence. Effort S, priorité P2.

Mesures nécessaires : M03 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : F : évite relecture du préfixe traité.
- Mémoire : F : ne charge que candidats restants bornés.
- Concurrence : A : concurrence double lanceur encore à prouver.
- Persistance : F : prédicat SQL aligné sur unicité existante.
- API : F : progression métier utile sans changer payload.
- SRE : F : file restante sélectionnable, priorité P2.

Issue : **5/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-04 — Remplacer les lectures de faits par des projections agrégées

Diagnostic initial : Hydratation intertenant, relectures par animation, mapping pour len/count et latence potentielle. Sources : CPU-01, MEM-01, DB-01, API-01.

Preuves : [app/application/animation_locale/services/pilotage_animation.py:101](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L101), [app/application/animation_locale/services/pilotage_animation.py:65](../../../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py#L65), [app/api/animation_locale_api.py:1331](../../../../../../localeo-backend/app/api/animation_locale_api.py#L1331), [app/infrastructure/persistence/repositories/animation_locale_repositories.py:1343](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/animation_locale_repositories.py#L1343). Mécanisme : Le service de dashboard charge tous les participants et filtre ensuite ; live et détails chargent les entités d’une animation pour des compteurs. Le lecteur ne porte pas la projection agrégée demandée.

Objection / réponse : Le frontend courant demande borne ; live reste consommé. Une recommandation de projection commune, deux expositions distinguées ; aucun changement silencieux du mode par défaut. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-01**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Sous-lots : compteurs Live actifs d’abord, détails ensuite, dashboard historique selon trafic. Basculer silencieusement en borne changerait la réponse.

Correction minimale retenue : Pousser périmètre et période dans SQL, calculer les compteurs/séries/top et fournir des résumés groupés aux détails. Appliquer le même lecteur de compteurs aux vues live. Garder la forme historique ; ne pas substituer le mode borne.

Risques / compatibilité : Moyen. Dates Paris, statuts, archives et mode de réponse identiques. Coût des résultats autorisés encore proportionnel aux animations réellement rendues. Effort M, priorité P2.

Mesures nécessaires : M04 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : F : retire mapping pour simples compteurs.
- Mémoire : F : réduit les faits hydratés hors périmètre.
- Concurrence : A : contention réelle et fréquence inconnues.
- Persistance : F : agrégats et résumés groupés adaptés.
- API : F : Live actif, contrat historique conservé.
- SRE : F : amélioration structurelle, pas urgence de capacité démontrée.

Issue : **5/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-05 — Grouper les faits du lot d’expiration

Diagnostic initial : Requête de relance par instance, relations lazy possibles et durée du lot sous verrou. Sources : DB-02.

Preuves : [app/application/gestion_achats/use_cases/expiration_coffrets.py:118](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L118), [app/application/gestion_achats/use_cases/expiration_coffrets.py:82](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/expiration_coffrets.py#L82), [app/infrastructure/persistence/models.py:509](../../../../../../localeo-backend/app/infrastructure/persistence/models.py#L509). Mécanisme : La sélection verrouille jusqu’à la limite, puis la boucle charge faits et relances unitairement avant un commit final.

Objection / réponse : Lot borné, SKIP LOCKED et exclusion remboursements présents. La validité d’un scan d’instance déjà expirée n’est pas supposée ; impact transversal réel à mesurer. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-09**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Chargements groupés bornés, sans jointure multipliant les racines ; réduction de lot éventuellement configurable après mesure. Commits partiels non adoptés.

Correction minimale retenue : Charger les relances en un ensemble borné et les relations nécessaires en requêtes groupées pour les IDs verrouillés ; conserver la sélection de racines, l’ordre de verrous et le commit actuel. Ne pas joindre une collection avant LIMIT/FOR UPDATE.

Risques / compatibilité : Moyen. Préserve atomisme, garde remboursement et crédit B2B ; mesurer aussi les octets et pas seulement le nombre SQL. Effort M, priorité P2.

Mesures nécessaires : M05 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : F : évite répétitions de préparation de détail.
- Mémoire : A : enrichissement eager peut augmenter pic du lot.
- Concurrence : F : réduit durée des lectures sous verrou sans nouveaux commits.
- Persistance : F : faits groupés des racines verrouillées.
- API : F : interface batch inchangée.
- SRE : F : garde un lot fini et mesure contention.

Issue : **5/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-06 — Préparer les CSV paiements dans un spool

Diagnostic initial : CSV complet en StringIO malgré pages SQL de 100. Sources : MEM-04.

Preuves : [app/application/gestion_achats/services/consultation_paiements.py:150](../../../../../../localeo-backend/app/application/gestion_achats/services/consultation_paiements.py#L150), [app/application/gestion_achats/services/export_financier.py:13](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13). Mécanisme : Le générateur est consommé dans produire_csv puis retourné sous forme d’une chaîne complète avec BOM.

Objection / réponse : Période limitée, colonnes scalaires et accès interne : pas d’OOM prouvé. Spool avant réponse conserve erreurs/audit et libère la transaction avant client lent. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-05**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Réutiliser le principe de spool déjà présent dans les exports Animation ; ne pas créer un service autonome ni streamer sous transaction jusqu’au client.

Correction minimale retenue : Écrire progressivement dans un fichier temporaire à seuil mémoire, terminer génération/audit puis fermer la projection SQL avant réponse par blocs. Fermer/supprimer le temporaire en succès, erreur ou abandon.

Risques / compatibilité : Faible à moyen. Mêmes colonnes, BOM, format, filtres et erreurs avant envoi ; ne pas supprimer une cohérence d’instantané si le contrat l’exige. Effort M, priorité P2.

Mesures nécessaires : M06 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : A : gain CPU non établi.
- Mémoire : F : tampon de sortie à seuil explicite.
- Concurrence : A : effet sur concurrence non quantifié.
- Persistance : F : projection fermée avant client lent.
- API : F : CSV/audit/erreurs conservés.
- SRE : F : ressources temporaires et nettoyage explicités.

Issue : **4/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-07 — Transmettre les budgets aux lectures de médias distants

Diagnostic initial : Attente de stockage dépassant le budget de lecture constatée seulement après retour I/O. Sources : API-02.

Preuves : [app/application/animation_locale/services/contenu_generation.py:368](../../../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py#L368), [app/infrastructure/storage/document_storage.py:83](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L83), [app/infrastructure/storage/document_storage.py:104](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L104), [app/application/animation_locale/services/jeu_animation.py:459](../../../../../../localeo-backend/app/application/animation_locale/services/jeu_animation.py#L459). Mécanisme : Le budget monotone entoure get S3/Body.read sans lui transmettre une échéance ; cela ne garantit pas l’interruption au budget.

Objection / réponse : 44 Ko par média et 256 Ko de projection, gardes de lecture et dimensions strictes. Pas de payload illimité. Budget réseau d’abord ; cache privé non adopté avant mesure et invalidation. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-11**, pas un ticket par symptôme ou domaine.

Alternatives examinées : D’abord politique réseau explicite. Cache immuable, parallélisme ou suppression de validation ne sont pas inclus : RC-14 doit être mesurée séparément.

Correction minimale retenue : Budget restant et politique explicite connect/read/retries dans l’adaptateur documentaire, fermeture du Body et lecture bornée aux octets attendus. Préserver SHA, provenance et autorisation ; ne pas annoncer une échéance dure sans moyen d’interruption effectif.

Risques / compatibilité : Moyen. JSON et contrôle d’intégrité inchangés ; effets sur les autres consommateurs du stockage à tester. Cache : orientation séparée différée. Effort M, priorité P2.

Mesures nécessaires : M07 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : A : ne résout pas les décodages répétés.
- Mémoire : F : lecture plafonnée aux octets attendus.
- Concurrence : F : attentes réseau explicites et restant propagé.
- Persistance : A : effet SQL marginal sur ce chemin hors TX.
- API : F : projection et intégrité préservées.
- SRE : F : limites adaptateur auditable, pas promesse deadline dure.

Issue : **4/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Débat OPT-08 — Alléger la vérification Stripe du retour de paiement

Diagnostic initial : Expansions Stripe non consommées et connexion SQL retenue pendant HTTP. Sources : API-03.

Preuves : [app/application/gestion_achats/use_cases/consulter_retour_paiement.py:11](../../../../../../localeo-backend/app/application/gestion_achats/use_cases/consulter_retour_paiement.py#L11), [app/infrastructure/paiement/paiement_gateway.py:226](../../../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py#L226). Mécanisme : L’achat/token est lu avant retrieve enrichi ; seule metadata.achat_id sert à cette vérification, état financier toujours local.

Objection / réponse : Absence d’en-tête évite l’appel. Créer une lecture minimale spécifique, fermer puis relire et réautoriser ; ne pas modifier le helper partagé ni supprimer la correspondance de session. La contre-expertise maintient le mécanisme et limite l’extrapolation aux incidents. Cause retenue : **RC-12**, pas un ticket par symptôme ou domaine.

Alternatives examinées : Nouveau helper léger pour le seul retour ; ne pas alléger le helper partagé de réconciliation ni mettre en cache le statut financier.

Correction minimale retenue : Créer une lecture de métadonnées spécifique sans expand ; autoriser dans une UoW courte, fermer avant HTTP, relire et réautoriser l’achat/token à la réponse. Conserver le helper enrichi des autres consommateurs et le statut webhook local.

Risques / compatibilité : Moyen. La revalidation après I/O doit couvrir expiration/révocation du token et session incompatible. Aucun cache financier proposé. Effort M, priorité P2.

Mesures nécessaires : M08 dans [plan-mesures.md](../recommandations/plan-mesures.md), avant toute acceptation de capacité. Aucune mesure exécutée.

Voix simulées et motifs :

- CPU : F : évite expansion fournisseur inutile.
- Mémoire : A : réduction mémoire effective inconnue.
- Concurrence : F : pas de connexion SQL durant HTTP.
- Persistance : F : relecture et réautorisation prévues.
- API : F : lecture dédiée garde le helper de réconciliation.
- SRE : F : dépendance externe et ressources distinguées.

Issue : **5/6**, orientation adoptée sous conditions techniques et autorisation ultérieure ; aucun effet d’un vote sur le niveau de preuve.

## Orientations concurrentes refusées ou différées

Les causes restent documentées même lorsque le remède n’obtient pas quatre voix ; aucune cause critique n’est masquée par le scrutin. Aucun P0 identifié.

| Cause / alternative précise | CPU | Mémoire | Concurrence | Persistance | API | SRE | F/6 | Issue et réserve déterminante |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-02 : nouvelle projection durable des qualifications historiques maintenant | A | A | C | F | A | C | 1 | Différée : usage actuel non établi ; invariant gel/qualification et maintenance supplémentaires |
| RC-03 : nouveaux refus selon pixels sans arbitrage | F | F | A | A | C | C | 2 | Refusée : breaking change ; garde RAM/capacité inconnue, fermeture déjà présente |
| RC-04 : refonte immédiate du tirage par rangs/réservoir | A | F | C | A | C | F | 2 | Différée : preuve d’équité, rejouabilité et volume manquante ; petite copie seule possible après mesure |
| RC-07 : relâcher les verrous avant l’envoi fournisseur | A | A | C | C | C | A | 0 | Refusée : révocation et remise incertaine ; garder mesure et risque résiduel |
| RC-13 : séparer d’emblée les executors scheduler | A | A | F | A | A | F | 2 | Différée : partage réel, saturation hypothétique ; crons actuels à relever |
| RC-14 : cache privé des médias activé avant mesure | F | C | A | A | F | A | 2 | Différé : invalidation, intégrité et mémoire ajoutées ; budget réseau RC-11 distinct |

Pour chacune, diagnostic et preuves restent dans [causes-racines.md](causes-racines.md), objections et alternative minimale dans [l’annexe des optimisations](../recommandations/annexe-optimisations-secondaires.md), mesures dans M09–M13. « Différée » porte sur le remède proposé, pas sur la réalité de tous les faits de code. Ces orientations ne sont pas des positions réellement exprimées par les anciens sous-agents.
