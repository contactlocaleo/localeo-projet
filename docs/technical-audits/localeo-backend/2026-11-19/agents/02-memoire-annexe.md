# Annexe — mémoire Python

Complément du [rapport principal](02-memoire.md), établi sans lecture des autres rapports. Révision backend : `7049e7fafc76f9119924f1082a5ee7457a175d85`. Toutes les observations sont statiques, sans mesure exécutée.

## Observations secondaires et protections

### Export des participants Animation : distinction des deux chaînes

[ServiceBilansExportsAnimation.participants_csv, ligne 58](../../../../../../localeo-backend/app/application/animation_locale/services/bilans_exports_animation.py#L58) est effectivement lu, ainsi que `_participants_email_csv` ligne 68, `bilan_pdf` ligne 100 et `_collecter_export` ligne 132.

- Le CSV classique charge une liste et construit une seconde liste de dictionnaires puis `StringIO`/chaîne/octet. Cependant, [participants_export, lignes 138–142](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/lectures_bilans_animation_repository.py#L138) impose `LIMIT 10001` et refuse au-delà de 10 000 lignes. Coût borné en nombre de lignes ; absence de mesure du pic. Il ne s’agit pas d’un export sans borne comparable à MEM-04.
- Le CSV tombola email utilise des [pages de 500 par clé stable, lignes 147–161](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/lectures_bilans_animation_repository.py#L147), un `SpooledTemporaryFile` basculant sur disque après 1 Mio et des blocs de 64 Kio. La préparation précède la réponse et la fermeture est dans le `finally` de l’itérateur. Le risque résiduel de durée d’instantané ou de disque plein relève d’une mesure dédiée ; aucun chargement global de participants n’est démontré sur cette branche.
- Le PDF conserve sources, commentaires et audit jusqu’au rendu, mais chacune des collections contrôlées est refusée au-delà de 10 000 éléments. Les commentaires/audits sont lus par lots de 100. Rendu hors transaction. Le coût du renderer pour les plus gros ensembles admissibles reste **HYPOTHÈSE À VÉRIFIER** ; pas de cinquième anomalie majeure sans mesure ou preuve d’une expansion non maîtrisée.

### Kits, stockage documentaire et images commerçant

[KitAnimationRenderer.kit, lignes 34–47](../../../../../../localeo-backend/app/infrastructure/animation_locale/kit_animation_renderer.py#L34) assemble un ZIP en `BytesIO`, avec un petit nombre fixe de documents. Le renderer de flyer crée un canevas 1654 × 2339 et le ferme dans un `finally` ; le service [lire, lignes 196–209](../../../../../../localeo-backend/app/application/animation_locale/services/kit_animation_commercant.py#L196) sort d’UoW avant hydratation et rendu. Buffers simultanés image/PDF/ZIP plausibles, mais aucune taille réelle ou récurrence ne permet de classer ce flux majeur : **HYPOTHÈSE À VÉRIFIER** pour le pic mémoire sous téléchargements concurrents.

[LocalDocumentStorage.get, ligne 59 et S3DocumentStorage.get, ligne 104](../../../../../../localeo-backend/app/infrastructure/storage/document_storage.py#L59) lisent l’objet intégralement. Ce contrat `bytes` implique un tampon par objet, sans prouver à lui seul des fichiers non bornés sur chaque consommateur. Pas de constat de fuite S3 sans inspection du cycle fournisseur et mesure dédiée.

[sanitize_merchant_image, lignes 6–24](../../../../../../localeo-backend/app/security/merchant_images.py#L6) accepte jusqu’à 16 millions de pixels et crée une conversion RGB/RGBA et un tampon réencodé avant le contrôle final 5 Mio. Pic potentiellement significatif mais borné en pixels ; fermeture explicite de `clean` améliorable, aucune fuite durable prouvée. Cette observation n’est pas confondue avec les pages OnBoard sans budget de pixels cumulé de MEM-02.

### Réversibilité SaaS : assemblage ZIP sur disque

[AssembleurArchiveOrganisation.archiver, lignes 54–97](../../../../../../localeo-backend/app/infrastructure/documents/archive_organisation.py#L54) utilise `TemporaryFile` pour ZIP et manifeste, lit et écrit les documents par blocs et applique un budget d’octets. `csv_flux` tamponne un segment CSV, pas toute l’archive. Le commentaire des segments 100 lignes n’a pas fait l’objet d’un suivi exhaustif de tous les producteurs ; aucune anomalie de mémoire globale de cette chaîne n’est retenue. La bibliothèque ZIP garde ses métadonnées d’entrées : la volumétrie des segments serait à inclure dans une future mesure, sans déduire un incident de ce seul fonctionnement.

### Import CSV/XLSX et ancien pack de factures

[ParseurImportsCommercants](../../../../../../localeo-backend/app/infrastructure/referencement/parseur_imports_commercants.py#L19) a été lu : plafond d’entrée 2 000 000 octets, 200 entrées ZIP, 20 Mo décompressés, 10 Mo par XML, 10 000 cellules et limites de valeurs/feuilles. Les arbres XML sont matérialisés avant certains contrôles de cellules ; expansion RAM à vérifier sur les limites admissibles, mais protections explicites et absence de mesure justifient une observation secondaire.

[ServiceDocumentsAchat._build_invoice_pack_bytes, lignes 854–869](../../../../../../localeo-backend/app/application/gestion_achats/services/service_documents_achat.py#L854) construit un ZIP en mémoire. Les entrées publiques proches `prepare_pack_generation` et `download_pack` lèvent cependant explicitement une erreur de fonctionnalité désactivée. Aucun flux actif démontré vers cette méthode : elle n’est pas retenue comme anomalie majeure.

### UoW et rétention

[SqlAlchemyUnitOfWork.__exit__, lignes 216–225](../../../../../../localeo-backend/app/infrastructure/persistence/uow/sqlalchemy_unit_of_work.py#L216) appelle rollback en cas d’exception et ferme la session. L’audit n’établit pas une fuite de session générique. La fermeture ne supprime pas les listes d’entités que les services conservent après le `with` (MEM-01), ni les buffers explicitement retournés. Pas de conclusion globale sur l’identity map ou le GC sans profils.

## Sources effectivement consultées

Lecture intégrale ou plages ciblées ; le reste du code a seulement fait l’objet de recherches `rg` et n’est pas présenté comme revu exhaustivement.

- Guides : `localeo-projet/README.md`, `localeo-backend/README.md`, `localeo-backend/AGENTS.md`, `localeo-backend/AGENT.md` et instructions transverses fournies dans la mission.
- Contrat de mission : `prompts/02-agents.md` ; inventaire autorisé : `inventaire/flux-critiques.md`, `inventaire/limitations.md`. Les autres rapports agents, synthèses, contradictions et recommandations n’ont pas été ouverts.
- Application Animation : `bilans_exports_animation.py` (intégral), `pilotage_animation.py` (intégral), `tirages_animation.py` (160–350), `exploitation_animation.py` (26–110), `kit_animation_commercant.py` (131–225).
- API : `animation_locale_api.py` (3310–3365 et recherches ciblées sur handlers d’export/tirage), `onboarding_commercant_api.py` (210–295, 540–600 et repères), `consultation_paiements_api.py` (10–30, 230–250).
- Persistance : `animation_locale_repositories.py` (1338–1360, 1505–1548, 1669–1763), `lectures_bilans_animation_repository.py` (130–225), `uow/sqlalchemy_unit_of_work.py` (1–65, 210–225).
- Documents/images : `security/uploads.py`, `security/merchant_images.py`, `security/document_upload.py`, `infrastructure/animation_locale/kit_animation_renderer.py`, `infrastructure/animation_locale/illustration_flyer.py`, `infrastructure/documents/archive_organisation.py`, `infrastructure/referencement/parseur_imports_commercants.py` ; `infrastructure/storage/document_storage.py` (48–115).
- Achats : `consultation_paiements.py` (1–25, 45–105, 145–190), `export_financier.py` (intégral), `service_documents_achat.py` (730–995).
- Configuration : uniquement ligne publique de code définissant `DOCUMENT_UPLOAD_MAX_SIZE_BYTES` dans `app/config.py`, repérée par `rg`. Aucun fichier de configuration rempli ni secret lu.

Les recherches globales `rg` ont servi à localiser collections, images, tampons, caches et appels. Les résultats tronqués ont été complétés par lectures ciblées pour les constats retenus ; une occurrence de recherche seule ne constitue pas une preuve de chaîne complète. Quelques chemins supposés inexistants ont été résolus par `rg --files` ; ils ne sont pas comptés comme fichiers lus.

## Vérifications et suites nécessaires

Commandes effectivement exécutées : inventaire shell, lectures `Get-Content`, recherches `rg`, `git rev-parse HEAD`, `git status --short`. Aucun programme applicatif ni test métier exécuté. La création de ces deux rapports est la seule écriture de la mission.

Les cibles de tous les liens fichiers de ces deux rapports ont été résolues depuis leur répertoire `agents/` par un contrôle PowerShell : aucune cible absente. Une future campagne autorisée devra distinguer mémoire Python, RSS/native Pillow, volumes par tenant et globaux, concurrence des exports/téléchargements et comportement de fermeture. Aucun chiffre de capacité n’est fourni ici. Les validations documentaires transverses relèvent de l’intégration finale ; cette revue ne les présente pas comme exécutées.
