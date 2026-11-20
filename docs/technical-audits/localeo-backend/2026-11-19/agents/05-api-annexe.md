# Annexe API — observations, exclusions et preuves de lecture

Cette annexe accompagne la [première analyse indépendante](05-api.md). Aucun rapport, conclusion ou fichier d’un autre agent n’a été consulté. Seuls la mission, le prompt `prompts/02-agents.md` et l’inventaire ont complété les sources applicatives.

## Observation secondaire API-S01 — Les lectures DAM chargent le blob avant un 304 ou une réponse de métadonnées

**Domaine :** médias publics. **Statut : FORTEMENT ÉTAYÉ PAR LE CODE.** `lire_image`, `app/api/images_api.py:178–193`, fait `session.get(MediaAssetOrm, id)`, contrôle la signature avec `asset.contenu`, puis seulement vérifie `If-None-Match`/`If-Modified-Since`. `MediaAssetOrm.contenu`, `app/infrastructure/persistence/media_models.py:24`, est un `LargeBinary` non différé. `lire_image_meta`, `images_api.py:197–215`, charge aussi l’entité complète sans utiliser le blob dans sa réponse. La variante sluggée délègue à `lire_image`, lignes 218–220.

Entrées complètes : `GET /public/dam/images/{image_id}`, `GET /public/dam/images/{image_id}/{slug}`, `GET /public/dam/images/{image_id}/meta`. Le préfixe `/dam/images` est déclaré ligne 26 et monté dans `app/main.py:536`. Les réponses image sont `public, no-cache` (ligne 89), donc une revalidation HTTP peut refaire le transfert blob PostgreSQL vers application même lorsque le corps HTTP final est vide.

Le coût évitable est le chargement binaire ; **pas** un décodage complet d’image. `validate_raster_image_content`, `app/security/uploads.py:82–89`, vérifie uniquement les signatures et le MIME. La limite d’upload image par défaut est 150 × 1024 octets (`config.py:400`), avec contrôle de taille à l’entrée (`images_api.py:36–48`) et quota global. Ces protections justifient le classement secondaire en l’absence de trafic mesuré. Une limite configurée ne prouve cependant pas la taille de tous les médias historiques.

Correction minimale : requête de métadonnées sans `contenu`, réponse 304 lorsque le contrat de validation/invalidation le permet, puis récupération du blob pour le seul 200 ; projection de colonnes pour `/meta`. Effort S/M, risque faible à moyen : conserver les protections de contenu des 200 et ne pas servir un 304 pour un asset inactif ou invalidé. Breaking change non. Confiance élevée ; mesure aucune. Autres domaines : trafic SQL, mémoire et capacité HTTP. Cause possible indépendante : mapping ORM complet partagé entre métadonnées et contenu.

## Autres pistes secondaires sans anomalie majeure retenue

- `ServiceJeuAnimation.lire`, `jeu_animation.py:403–408`, recharge les commerces un par un pour le passeport. Le chemin est directement visible mais la population marchande est bornée par le contrat, et le coût SQL réel manque. Un chargement groupé peut être utile ; absence de mesure, à rapprocher ultérieurement des observations de persistance, sans les consulter ici.
- Le téléchargement du kit commerçant construit un ZIP à la demande : `kit_animation_api.py:81–86`, `ServiceKitAnimationCommercant.lire`, `kit_animation_commercant.py:131–209`, puis `KitAnimationRenderer.kit`, `kit_animation_renderer.py:34–48`. La lecture privée est authentifiée, le rendu n’est pas exécuté sous transaction, les médias sont bornés. Les volumes et la fréquence ne permettent pas de le promouvoir au rang majeur sur cette seule lecture.
- Le service documentaire ordinaire retourne les octets complets : `GestionDocumentaireService.lire_contenu`, `gestion_documentaire.py:508–510`, et stockage S3 `document_storage.py:104–109`. Cela concerne plusieurs documents, mais on ne peut conclure à un fichier géant ou à une consommation mémoire problématique sans examiner ses règles d’entrée, ses producteurs et les tailles réelles. Pas d’affirmation générale d’absence de streaming pour tous les exports.
- Les contrôles d’autorisation de Live sont répétés dans le handler puis le service ; le garde impose une phase avant et une phase après autorisation. Supprimer un appel sans comprendre cet ordonnancement pourrait dégrader la protection. Aucun constat majeur d’« authentification redondante » n’est retenu.

## Faux positifs écartés et bornes contrôlées

| Chemin inspecté | Protection observée | Limite de la conclusion |
| --- | --- | --- |
| Dashboard `mode_lecture=borne` | Page 1–100, curseur, agrégats SQL, alertes limitées à 50 | Ne borne pas automatiquement la variante historique, qui reste exposée |
| Catalogue public d’animations | Recherche SQL avec `LIMIT taille + 1`, `catalogue_animations_publiques.py:359–360` ; enrichissements groupés `573–627` | Pas de diagnostic N+1 global sur ce service |
| Recherche Marketplace | `recherche_api.py:25–26`, total limité à 30 et 10 par scope | Aucun benchmark ou plan SQL examiné |
| Lecture de participants | Route `/participants-page`, `animation_locale_api.py:3392–3402`, page ≤100 et total optionnel | Distincte des lectures de compteurs historiques |
| Import commerçants | `imports_commercants_api.py:258–265`, lecture `MAX_OCTETS+1`, traitement par threadpool | L’acceptation HTTP et le traitement différé ont des coûts distincts |
| Webhooks Stripe | `stripe_platform_api.py:70–72` et `stripe_connect_api.py:41–43`, traitement déporté via `run_in_threadpool` | Pas d’affirmation d’appel Stripe synchrone bloquant l’event loop à ces entrées |
| Lecture joueur | Projection ≤256 000 octets, média ≤44 000 octets ; garde d’origine/personnel | Le volume est borné, les répétitions et délais externes demeurent |
| Kit Animation | Contrôle d’accès, préparation explicite, rendu après sortie UoW | Fréquence réelle non connue |

## Lectures réalisées et chemins de montage

Prévol réel via `exec_command` : `AGENTS.md`, `AGENT.md`, `README.md` du backend, puis README transverse. `rg -n` sur `app/main.py` a révélé les montages ; les lignes 527–702 et les définitions de préfixes des routeurs concernés ont été recoupées. Le catalogue statique de l’inventaire compte les montages et variantes ; aucun inventaire runtime n’a été tenté.

Sources principales lues ou extraites avec lignes :

- `app/main.py` : montages publics/protégés/internes ; notamment 536, 544, 550 et 693.
- `app/api/animation_locale_api.py` : préfixes, `_animation_detail:1321–1379`, Live 3301–3312, dashboard 3315–3346, participants 3349–3420.
- `app/application/animation_locale/services/pilotage_animation.py` : `live`, `dashboard`, événements et faits de tirage.
- `app/infrastructure/persistence/repositories/animation_locale_repositories.py` : listes de participants 1343–1348 et validations 1510–1518, pages tenant adjacentes.
- `app/application/animation_locale/services/productivite_animation.py` et repository homonyme : page, agrégats et bornes.
- `app/api/jeu_animation_api.py`, `app/api/limitation_lectures_live.py`, composition et service de limitation applicative.
- `app/application/animation_locale/services/jeu_animation.py` : projection personnelle, sélection des médias, résultat, pages dédiées.
- `app/application/animation_locale/services/contenu_generation.py` : budget, lecture brute, contrôles médias et hydratation.
- Contrats `commun.py`, `generation.py`, `definition.py`, projections et `projections_jeu.py` : dimensions, poids et enveloppes.
- Adaptateurs `decodage_illustration.py`, `stockage_generation.py`, `document_storage.py` et factories `composition.py`.
- `app/api/paiements_api.py`, `consulter_retour_paiement.py`, `paiement_gateway.py`, portions d’`initialiser_paiement.py` et entité `achat_coffret.py` ; clôture d’UoW 216–225.
- `app/api/images_api.py`, `app/security/uploads.py`, `merchant_images.py`, modèle média, service DAM et constantes de configuration non secrètes.
- Recherche Marketplace, catalogue d’animations, kit/service/rendu, routes documents métier et QR ; recherches textuelles des appels `requests`, `httpx` et Stripe dans les sources Python.

Les commandes PowerShell utilisant un joker au milieu d’un chemin transmis littéralement à `rg` ont parfois échoué. Elles n’ont pas été comptées comme lectures ; les fichiers utiles ont ensuite été lus par leur chemin exact ou par recherche ciblée de répertoire. Une recherche trop large a affiché un résultat tronqué incluant du JavaScript fournisseur : ce résultat n’est pas une preuve d’absence de timeout. La recherche ciblée `rg` sur les sources Python pour `stripe.default_http_client`, `default_http_client`, `max_network_retries`, `StripeClient`, `RequestsClient` n’a pas trouvé de configuration explicite dans `app`.

## Limites et mesures à demander ultérieurement

Ni latence observée, ni profil CPU/RAM, ni métrique fournisseur, ni nombre SQL mesuré. L’environnement, les volumes, le nombre de workers, le CDN effectif et la fréquence des consommateurs ne sont pas déduits de valeurs privées. Les bornes citées sont celles des sources, pas une capture du paramétrage déployé. Le SHA a été lu par `git rev-parse HEAD` et l’arbre backend était propre selon `git status --short`.

Pour une phase autorisée de mesure : comparer les deux modes dashboard à volume global croissant et commune constante ; instrumenter séparément SQL, enrichissements et sérialisation ; relever appels de stockage et décodages par lecture joueur à données identiques ; mesurer le retour de paiement avec et sans en-tête session en simulant une latence fournisseur ; distinguer temps total, occupation de connexion et taille transférée. Ce sont des propositions, aucune exécution ni aucun gain n’est annoncé.

Seuls `agents/05-api.md` et cette annexe sont écrits dans `localeo-projet`. Aucun code backend, frontend, contrat consommé, migration, critère d’acceptation ou générateur n’a changé ; sans impact d’exécution pour cette phase documentaire. La vérification documentaire globale et l’intégration des rapports relèvent de l’agent principal, afin de ne pas exécuter plusieurs contrôles partagés en parallèle.
