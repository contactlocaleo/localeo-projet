# Annexe — Audit CPU indépendant

Révision backend : `7049e7fafc76f9119924f1082a5ee7457a175d85`, 19 novembre 2026. Première analyse finalisée indépendamment, sans lecture d'autres rapports d'agents/conclusions. Seuls `01-cpu.md` et cette annexe sont écrits par cet agent.

## Piste secondaire CPU-A01 — Traitement raster documentaire à borner par pixels

**Statut : HYPOTHÈSE À VÉRIFIER.** Domaine OnBoard/documents. Chaîne : `POST /api/dossiers/{dossier_id}/documents` (chemin local du routeur, préfixe de montage non vérifié) → `ajouter_document_commercant`, `app/api/onboarding_commercant_api.py:547-581` → `_preparer_pages_documentaires`, `:241-275` → `inspect_document_content` → `_inspect_image`, `app/security/document_upload.py:126-138` → seconde ouverture et conversion en niveaux de gris de la pleine image, statistiques → `compose_images_as_pdf`, `:163-174` → nouveau décodage/conversion RGB et encodage PDF de toutes les images.

Mécanisme : travail proportionnel aux pixels décodés, pas seulement aux octets téléversés ; double décodage des images entre inspection et composition. Le contrôle final de taille PDF intervient après l'encodage. Les limites applicatives visibles sont 20 pages et un budget global d'octets ; la source ne fixe pas de budget total de pixels et ne réduit pas l'image avant statistiques/assemblage. Les garde-fous de Pillow subsistent : il n'est pas allégué une dimension arbitrairement illimitée. La configuration effective, les filtres de warnings globaux et les dimensions acceptées à l'exécution n'ont pas été vérifiés. La présence d'images très compressibles et de lecteurs concurrents est une condition de risque, sans preuve qu'elle existe actuellement.

Impact potentiel moyen à élevé pour le worker ; probabilité inconnue, vraisemblablement plus faible que les lectures courantes ; criticité moyenne (pièces OnBoard) ; preuve de traitements répétés forte, preuve d'un coût excessif absente ; facilité moyenne. Mesure disponible : aucune. Confiance moyenne sur le risque, élevée sur la chaîne statique. Correction minimale à étudier : fixer dimensions/pixels par page et budget global avant conversion, conserver la résolution nécessaire au document, et isoler les conversions du chemin HTTP si leur coût mesuré le justifie. Effort M, risque moyen (lisibilité et restitution des documents), breaking change possible **oui** si les documents actuellement acceptés au-delà de nouvelles limites sont refusés ; **non** pour une simple optimisation de décodage équivalente. Autres domaines : mémoire, concurrence, latence API ; cause racine possible : limite exprimée en octets compressés pour un travail exprimé en pixels. Non retenu dans les anomalies majeures faute d'établir l'exposition réelle et les bornes runtime.

## Couvertures négatives et limites qui empêchent de surqualifier

- `ServiceBilansExportsAnimation` (`app/application/animation_locale/services/bilans_exports_animation.py`) utilise des agrégats pour `bilan/page/bilans_page` ; CSV classiques et collecte PDF sont plafonnés à 10 000, l'export email est traité par lots avec fichier temporaire débordant sur disque. Pas d'anomalie majeure CPU tirée de ces seules boucles. Le rendu PDF lui-même n'a pas été analysé en profondeur.
- `ServiceTiragesLibres._unite_numerique_suivante/_unite_suivante`, `app/application/animation_locale/services/tirages_libres.py:346-377`, utilisent `pop(0)`, mais sur des pages de 100. Ne pas les annoncer comme un algorithme quadratique non borné sur toute la population. Le traitement comporte aussi des phases/budgets visibles ; leur efficacité runtime n'est pas mesurée.
- `PopulationEligibleAnimation.selectionner`, `app/domaine/animation_locale/entities/tirage_animation.py:80-94`, copie un tuple en liste avant `sample`. Transformation linéaire évitable possible, mais le contrôle d'unicité de population est lui-même linéaire et aucune mesure n'établit un coût dominant ; observation secondaire seulement.
- `couverture_bancaire`, `app/domaine/gestion_reversement/services/lecture_suivi.py:137-155`, filtre toutes les associations pour chaque paiement, soit `O(P*A)` en lecture directe. La recherche des appels applicatifs n'a trouvé aucun consommateur de ce helper hors sa définition ; ne pas en faire une anomalie de flux actif. Le même fichier propose `accumuler_couverture` pour des faits ordonnés en flux.
- `ventiler_remboursement`, `app/domaine/gestion_achats/services/remboursement.py:17-30`, trie les instances à chaque appel. Le wrapper existe, mais la répétition sur de grandes commandes n'est pas démontrée ; pas de constat majeur.
- `RechercherVillesProches` reçoit origine/rayon dans son repository puis calcule les distances et trie les candidats ; ce code seul ne prouve pas un scan de toutes les villes. Aucun constat de géolocalisation coûteuse retenu.
- `sanitize_merchant_image`, `app/security/merchant_images.py:6-25`, possède un plafond explicite de 16 millions de pixels avant décodage complet ; ne pas extrapoler CPU-A01 à cette voie.
- La recherche `rg` a rencontré une expansion de wildcard PowerShell invalide sur `repositories/*exploitation*`, corrigée par une recherche dans le répertoire ; aucune source inaccessible n'a été simulée. D'autres recherches de noms de fichiers participants/validations n'ont pas trouvé de fichiers séparés ; les implémentations réelles sont dans `animation_locale_repositories.py`.
- L'analyse n'a pas inspecté le trafic frontend, le profil CPU, le nombre de workers effectif, les cardinalités ou plans SQL. Aucune mesure disponible n'est réinterprétée en preuve de saturation. Les hotspots natifs (Pillow, chiffrement, PDF) et tous les modules du backend ne sont pas couverts exhaustivement.

## Sources effectivement consultées

Lectures complètes ou extraits ciblés (les extraits suffisent aux chaînes mentionnées) :

- Backend : `AGENTS.md`, `AGENT.md`, `README.md`.
- `app/application/animation_locale/services/pilotage_animation.py` ; `bilans_exports_animation.py` ; `tirages_animation.py` ; `traitement_tirages_libres.py` ; extraits de `tirages_libres.py`, `exploitation_animation.py`, `jeu_animation.py`.
- `app/api/animation_locale_api.py` (helpers détail, routes pilotage, participants et préfixes), `app/api/onboarding_commercant_api.py` (uploads et route documents).
- `app/infrastructure/persistence/repositories/animation_locale_repositories.py` (mappers et listes participants/validations), `exploitation_animation_repository.py` (lots et sélection animations).
- `app/domaine/animation_locale/entities/tirage_animation.py`, `app/domaine/animation_locale/services/periode_pilotage.py`, `app/domaine/animation_locale/moteurs/politique_exploitation.py`, début de `execution.py` et repères qualification.
- `app/application/referencement/use_cases/rechercher_villes_proches.py`, `contextualiser_accueil_marketplace.py`, `app/application/exploitation/use_cases/consulter_statistiques.py`, `app/application/prospection/priorite.py`.
- `app/domaine/gestion_reversement/services/lecture_suivi.py`, `app/domaine/gestion_achats/services/remboursement.py`, `app/application/gestion_achats/services/ventilation_remboursement.py`.
- `app/security/document_upload.py`, `app/security/merchant_images.py`.
- Projet transverse : `README.md`, instructions `AGENTS.md` fournies dans la mission, `docs/technical-audits/localeo-backend/2026-11-19/prompts/02-agents.md` (contrat de preuve).

Recherches textuelles uniquement, sans lecture exhaustive : inventaire des noms de fichiers CPU/exports/tirages ; boucles/tri/copies/sérialisation dans `app/application` et `app/domaine` ; références des deux helpers finance ; dimensions images et limites documentaires sous `app`/`tests` ; repères d'agrégats dans `lectures_bilans_animation_repository.py`. Les autres fichiers renvoyés par ces recherches ne sont pas prétendus audités. `app/config.py:413` a été vu uniquement comme ligne source renvoyée par `rg` (valeur par défaut du plafond documentaire), sans chargement de configuration ni lecture de dotenv.

## Opérations réellement effectuées et état

Lecture shell via `tools.exec_command`, `Get-Content -Encoding utf8`, `rg`/`rg --files`, `git rev-parse HEAD`, `git status --short`, et inventaire des noms du dossier agents. Aucun autre rapport d'agent n'a été ouvert. Le backend était sans modification signalée par `git status --short` au contrôle. Aucun benchmark, test métier, import de l'application, requête SQL, réseau, migration ou refactoring exécuté. Aucun secret/`.env` lu. Aucune mesure ni assertion de suite verte. Les seules écritures sont les deux livrables de cet audit CPU.
