# Comparaison historique — périmètres et preuves distingués

Il n’existe aucune exécution datée antérieure dans `docs/technical-audits/localeo-backend/` au moment de cet archivage. Des audits backend précédents existent dans `docs/audits/backend/` ; ils sont utilisés comme références et restent inchangés. **Aucune métrique actuelle n’est suffisamment comparable pour calculer une évolution de latence API, CPU, mémoire ou capacité.**

## Références et commits

| Référence | Révision attestée / méthode | Portée de la comparaison |
| --- | --- | --- |
| [API Live, 8 novembre 2026](../../../../audits/backend/audit-performance-api-localeo-live-2026-11-08.md) | Backend `1b3e27c4755a441ddd9b99cd0ddf83887879e136`, Marketplace `c40ee5ab02f463dd159874a7e96f5748200b0403`, documentation `e04248e0ea4cb3f08e5f68081f751822f27bb350` ; SHA déployé TEST non attesté | Précédent le plus récent pertinent pour recherche/consultation ; benchmark PostgreSQL isolé et observations GET publics, pas remises ERP/CSV |
| [Mémoire Uvicorn, 18 septembre 2026](../../../../audits/backend/audit-memoire-uvicorn-2026-09-18.md) | Aucun SHA backend consigné ; checkout avec modifications locales, CPython 3.12.14 ; working set et mémoire privée après imports/GC | Socle de démarrage, distinct du pic d’allocations d’un export. Les expériences neutralisant des composants ne sont pas des corrections livrées |
| [Suivi performance, 12 septembre 2026](../../../../audits/backend/suivi-implementation-performance-2026-09-12.md) et [validation volume](../../../../audits/backend/validation-volume-recherches-2026-09-12.md) | Commits par correction et fixtures documentées, pas une révision globale unique de campagne | Historique de remédiation, à vérifier mécanisme par mécanisme dans le code courant |
| Audit actuel, 19 novembre 2026 | Backend `7049e7fafc76f9119924f1082a5ee7457a175d85`, documentation `f437465c577d3754b8743c6c48519f0d7606613e` ; CPython 3.14.3 | Six domaines puis bancs de composants hors réseau M01/M06 et simulation M02 ; pas de capacité HTTP/PostgreSQL |

Git vérifié en lecture seule : l’objet backend du 8 novembre est disponible et ancêtre du HEAD audité le 19 novembre (`merge-base --is-ancestor`, sortie 0). Cela établit l’ordre des révisions, pas le commit d’introduction de chaque risque. Un commit documentaire ne remplace pas la révision applicative mesurée.

## Corrections historiques encore lisibles

Le suivi de septembre annonce le dashboard **commerçant** corrigé par `f654175a3609f9145f3ab324c655928f4ff4fa3f`. Le mécanisme reste présent : [consulter_dashboard_operationnel_commercant.py:139](../../../../../../localeo-backend/app/application/exploitation/use_cases/consulter_dashboard_operationnel_commercant.py#L139), agrégations COUNT/GROUP BY [ligne 191](../../../../../../localeo-backend/app/application/exploitation/use_cases/consulter_dashboard_operationnel_commercant.py#L191) et mouvements [ligne 207](../../../../../../localeo-backend/app/application/exploitation/use_cases/consulter_dashboard_operationnel_commercant.py#L207). Conclusion limitée : correction d’agrégation conservée dans le code, **tests et anciens gains non rejoués**. Le nombre historique de groupes n’est pas un plafond universel. Ce dashboard est distinct du dashboard Animation/Live de RC-01/OPT-04 ; aucun retour en arrière du premier n’est déduit du défaut du second.

Le groupement de la garde BUM et de projections du catalogue, suivi sous `04bcb8ae5712afaaa7cd2985299cf8a603ec4883`, demeure : [_animations_bloquees:252](../../../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py#L252), garde avant pagination [ligne 267](../../../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py#L267) et projections groupées [ligne 597](../../../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py#L597). Ce constat ne clôture pas tous les enrichissements du catalogue. Les chiffres avant/après de septembre restent ceux de leurs fixtures et révisions, pas des budgets actuels.

## Problèmes persistants et réserves non clôturées

L’ancien **API-01 du rapport du 8 novembre**, identifiant à ne pas confondre avec l’API-01 du spécialiste actuel, conserve son mécanisme : comptage avant curseur [ligne 338](../../../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py#L338), paramètres relus pour le curseur [ligne 368](../../../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py#L368), puis `parametres_effectifs_dans_session` dans la boucle [ligne 634](../../../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py#L634). Les configurations du service moderne distinct sont groupées [recherche_animations_live.py:149](../../../../../../localeo-backend/app/application/animation_locale/services/recherche_animations_live.py#L149).

Précision à la lecture de la ligne F04 de la consolidation actuelle : **plusieurs enrichissements sont groupés ; l’ancien catalogue conserve toutefois un comptage global et des paramètres effectifs par animation**. « Enrichissements groupés » ne ferme donc pas l’ancien constat N+1. Aucun compteur SQL actuel n’a été remesuré. Cette réserve historique ne crée pas une neuvième correction ni ne modifie rétroactivement les 17 constats et 14 causes de la campagne actuelle.

Les propositions de mémoire de démarrage ne sont pas toutes matérialisées : imports Stripe immédiats encore présents dans [paiement_gateway.py:2](../../../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py#L2) et [stripe_connect_gateway.py:6](../../../../../../localeo-backend/app/infrastructure/paiement/stripe_connect_gateway.py#L6) ; le coût présent de ce socle n’a pas été mesuré. Les réserves privées/frontend et de capacité du rapport Live ne sont pas clôturables sans leur recette spécifique ; leur absence du backlog courant ne prouve pas leur résolution, ni qu’elles sont toutes inchangées aujourd’hui.

## Risques nouvellement documentés

L’audit actuel étend l’examen aux batchs ERP async, au cycle/bail d’envoi, aux relances d’expiration, aux allocations CSV et aux lectures Stripe/médias. Les mécanismes d’OPT-01 et OPT-02 sont confirmés dans [admin.py:12523](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523) et [batchs.py:608](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608), puis mesurés/simulés avec la portée précisée dans [resultats.md](../benchmarks/resultats.md). Ce sont des **risques nouvellement examinés**, pas des régressions attribuées aux commits depuis le 8 novembre. Le fait que les routes Live auparavant examinées soient synchrones ne contredit pas le cas des routes ERP async.

## Métriques et évolutions : NON COMPARABLES

| Dimension | Historique | Audit actuel | Conclusion |
| --- | --- | --- | --- |
| API HTTP | GET publics TEST du 8 novembre, trois essais par route, clients curl distincts ; déploiement non attesté | Aucun HTTP : témoins asyncio et production CSV | Aucun gain/régression API ni p95 commun calculable |
| Persistance / débit | Recherche Live PostgreSQL 18.3, jeux et paliers de lecteurs documentés ; anciennes campagnes de recherche séparées | SQLite minimal avec horloge logique pour le bail ; pas de SQL PostgreSQL chronométré | Pas d’évolution de débit, plans ou nombre SQL à partir du banc actuel |
| CPU | Autres fonctions/scénarios et instrumentation historiques | Profil CSV 10 000 lignes, générateur inclus ; CPU processus Windows quantifié | Pas de tendance CPU/requête ou de saturation générale |
| Mémoire | Application complète après imports/GC, Python 3.12.14, versions propres à ce banc ; working set/mémoire privée | Python 3.14.3, pas d’import de l’application complète ; pic tracemalloc CSV et compteurs ponctuels du processus | Pas de baisse/hausse du socle, pas de comparaison allocations Python ↔ working set ou RSS Linux |

Même si certains outils ou le poste se ressemblent, périmètre, versions, jeux et état applicatif diffèrent. La réserve de capacité Live demeure non clôturée ; aucune mesure après correction n’est disponible pour les huit candidats actuels. Rejouer le même protocole sur une cible autorisée et des conditions comparables avant tout calcul d’écart.

## Décisions précédentes et état actuel

Le suivi de septembre consigne des corrections par commits locaux, une livraison progressive et aucun déploiement ; le rapport mémoire et celui du 8 novembre présentent des propositions/expériences, pas une validation de toutes leurs pistes. Ces informations sont des états documentés à leur date, **pas des décisions du demandeur actuel**.

Aujourd’hui : huit corrections candidates, deux P1 et six P2, aucune autorisée. Les champs de [decisions.md](../validation/decisions.md) restent vides. Aucun vote simulé, ancien état « terminé » ou demande d’archivage ne vaut validation. Les archives anciennes et leurs métriques ont seulement été lues et vérifiées, sans réexécution ni modification.
