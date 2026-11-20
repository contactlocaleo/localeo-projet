# Catalogue API statique

1329 modules Python parsés, 1365 décorateurs HTTP potentiels ; 0 erreurs AST. Préfixes APIRouter locaux résolus ; include_router/mount et api_route multi-méthodes non développés. Ces comptes ne sont ni routes déployées ni trafic, et ne sont pas directement comparables aux 1 346 opérations développées de la référence.

Détail brut ignoré : `localeo-backend/tmp/performance-audit-2026-11-19-02/static-routes.json`. Première tentative inline : erreur de nom de codec utf8-sig, zéro module parsé ; sortie rejetée, corrigée par utf-8-sig sans toucher aux sources.

| Méthode | Chemin local statique | Handler et source |
| --- | --- | --- |
| GET | `/animation-locale/lectures-globales/tirages` | `lister_tirages_globaux` — `app/api/animation_locale_api.py:1220` |
| GET | `/animation-locale/animations/{animation_id}/tirage-annonce` | `consulter_annonce_tirage` — `app/api/animation_locale_api.py:2176` |
| PUT | `/animation-locale/animations/{animation_id}/tirage-annonce` | `modifier_annonce_tirage` — `app/api/animation_locale_api.py:2185` |
| GET | `/animation-locale/animations/{animation_id}/tirage-annonce` | `consulter_annonce_tirage_erp` — `app/api/animation_locale_api.py:2195` |
| PUT | `/animation-locale/animations/{animation_id}/tirage-annonce` | `modifier_annonce_tirage_erp` — `app/api/animation_locale_api.py:2203` |
| GET | `/animation-locale/animations/{animation_id}/tirages` | `lister_tirages_animation` — `app/api/animation_locale_api.py:2722` |
| POST | `/animation-locale/animations/{animation_id}/tirages` | `lancer_tirage_animation` — `app/api/animation_locale_api.py:2741` |
| GET | `/animation-locale/animations/{animation_id}/live` | `consulter_live_animation` — `app/api/animation_locale_api.py:3302` |
| GET | `/animation-locale/animations/{animation_id}/live/evenements` | `lister_evenements_live_animation` — `app/api/animation_locale_api.py:3310` |
| GET | `/animation-locale/dashboard-performance` | `consulter_dashboard_performance_animation` — `app/api/animation_locale_api.py:3316` |
| GET | `/animation-locale/tirages` | `lister_tirages_globaux_animation` — `app/api/animation_locale_api.py:3485` |
| GET | `/animation-locale/animations/live` | `superviser_animations_live` — `app/api/animation_locale_api.py:3700` |
| GET | `/protected/referencement/commercants-animation` | `lister` — `app/api/gestion_commercants_animation_api.py:107` |
| GET | `/protected/referencement/commercants-animation/categories` | `categories` — `app/api/gestion_commercants_animation_api.py:113` |
| GET | `/protected/referencement/commercants-animation/recus/{cle}` | `recu` — `app/api/gestion_commercants_animation_api.py:118` |
| GET | `/protected/referencement/commercants-animation/{commerce_id}` | `detail` — `app/api/gestion_commercants_animation_api.py:125` |
| POST | `/protected/referencement/commercants-animation` | `creer` — `app/api/gestion_commercants_animation_api.py:130` |
| PATCH | `/protected/referencement/commercants-animation/{commerce_id}` | `modifier` — `app/api/gestion_commercants_animation_api.py:135` |
| POST | `/protected/referencement/commercants-animation/{commerce_id}/{action}` | `commander` — `app/api/gestion_commercants_animation_api.py:140` |
| GET | `/localeo-live/participations/{participation_id}/lieu-courant/pratique` | `lieu_courant_pratique` — `app/api/jeu_animation_api.py:61` |
| GET | `/localeo-live/participations/{participation_id}` | `lire` — `app/api/jeu_animation_api.py:77` |
| POST | `/localeo-live/participations/{participation_id}/commandes` | `commander` — `app/api/jeu_animation_api.py:91` |
| GET | `/localeo-live/participations/{participation_id}/commandes/{cle}` | `recu` — `app/api/jeu_animation_api.py:109` |
| GET | `/localeo-live/participations/{participation_id}/etapes/{step_id}/resultat` | `resultat` — `app/api/jeu_animation_api.py:117` |
| GET | `/localeo-live/participations/{participation_id}/vitrines` | `vitrines_participant` — `app/api/jeu_animation_api.py:126` |
| GET | `/localeo-live/participations/{participation_id}/juste-prix/produits` | `produits_juste_prix` — `app/api/jeu_animation_api.py:147` |
| POST | `/animation-locale/commercants/me/participants/resoudre` | `resoudre_scan_participant` — `app/api/merchant_animation_scan_api.py:27` |
| GET | `/animation-locale/commercants/me/participants/{participant_id}/attestations/commandes/{cle}` | `lire_recu_attestation` — `app/api/merchant_animation_scan_api.py:38` |
| GET | `/animation-locale/animations/recherche` | `rechercher` — `app/api/recherche_animations_live_api.py:39` |
