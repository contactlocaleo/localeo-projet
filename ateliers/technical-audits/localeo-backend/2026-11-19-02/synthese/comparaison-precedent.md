# Comparaison avec la référence et les audits antérieurs

Référence sélectionnée : unique dossier daté antérieur 2026-11-19, README explicitement ARCHIVÉ. Même date réelle : nouvelle exécution suffixée -02 ; aucune sélection sur mtime. Les empreintes initiales de ses 101 fichiers sont dans validation/archives-avant.json ; son manifeste interne couvre 99 fichiers et concorde. Les trois sources et quatorze bruts/harness référencés concordent aussi. Les anciens diagnostics ne sont pas transmis aux six premières analyses.

## Révisions et portée Git

Backend précédent = courant : 7049e7fafc76f9119924f1082a5ee7457a175d85. Objet disponible (git cat-file -t : commit), diff --stat et --name-status précédent HEAD vides ; checkout suivi propre. Aucune correction applicative entre les deux exécutions. Les SHAs des cinq dépôts sont identiques à ceux consignés dans la référence. Les archives et atelier CRM non suivis du projet existaient déjà ; ils ne sont pas annulés.

Ancêtre pertinent du 8 novembre : 1b3e27c4755a441ddd9b99cd0ddf83887879e136 disponible, merge-base --is-ancestor vers HEAD réussi. Diff ciblé app/application/animation_locale, app/api/jeu_animation_api.py, app/api/localeo_live_api.py : 103 fichiers, 4 882 ajouts, 370 suppressions. Cela décrit un périmètre d'évolution, pas l'origine d'un constat ; aucun diagnostic nouveau n'est qualifié de régression depuis le 19 novembre.

## Corrections historiques vérifiées dans le code

L'agrégation du dashboard commerçant reste visible dans consulter_dashboard_operationnel_commercant.py:191/207 (COUNT/GROUP BY) ; ce dashboard est distinct du pilotage Animation historique. Les groupements de garde BUM restent dans catalogue_animations_publiques.py:252/577, et plusieurs projections sont groupées. Ces mécanismes sont conservés, mais leurs tests et anciens gains ne sont pas rejoués.

La réserve de l'ancien catalogue persiste : comptage global avant curseur vers :340, parametres_effectifs_dans_session dans le curseur :368 et la boucle :634. La recherche Live moderne groupée est un autre producteur. Les lectures bornées actuelles du carnet (tableau_de_bord_live.py:137–164 ; sélection locale App/Marketplace) interdisent de reprendre sans vérification l'ancien diagnostic de 2N GET du 8 novembre. L'orchestration complète de Mes lots n'est pas requalifiée par ce seul audit backend.

Les quatre corps ERP async restent à admin.py:12523–12600, le bail à batchs.py:608–700, le CSV entier à export_financier.py:13–27 et le budget média entourant une lecture synchrone à contenu_generation.py:368–395. Ils n'ont pas disparu parce qu'un autre audit les a relégués ou qu'une roadmap est clôturée.

## Correspondance sémantique et limites

Les identifiants locaux CPU-01/API-01 ne constituent pas une continuité d'identité. La correspondance détaillée des causes de cette exécution avec les huit OPT historiques est portée par la consolidation finale. Un sujet absent du backlog prioritaire actuel reste soit secondaire, soit non requalifié ; il n'est pas réputé corrigé.

| Mécanisme | État après revue du code courant |
| --- | --- |
| Agrégations dashboard commerçant et groupements BUM de septembre | CORRIGÉ VÉRIFIÉ dans la source ; anciens gains et tests non rejoués |
| Anciennes OPT-01/02/04/07 → R01/R10/R09/R06 | PERSISTANT ; image Juste Prix ajoute un consommateur/corps distinct à R01 |
| Anciennes OPT-03/05/06/08 et ancien catalogue public | PERSISTANT dans leur périmètre source, hors neuf priorités courantes ; CSV seulement rejoué |
| Compteur d'inscription, projections QR/PIN, producteurs notification, résumés passeport et écran gains actuels | NOUVELLEMENT DOCUMENTÉ ou davantage détaillé dans cette relance, pas régression attribuée à un commit |
| Population Coffrets et copie R05 | PERSISTANT comme réserve source ; transitoires désormais mesurés selon une nouvelle méthode, copie seule P3 |
| Capacité intégrée, migrations réellement appliquées, anciens gains privés et socle mémoire complet | NON VÉRIFIÉ dans cette campagne ; aucun déploiement attesté |

Audits pertinents lus : audit-performance-api-localeo-live-2026-11-08.md, suivi-implementation-performance-2026-09-12.md ; revue du socle mémoire du 18 septembre via ses limites historiques. Leurs protocoles HTTP TEST/PostgreSQL et mémoire après imports sont **NON COMPARABLES** aux composants AST, au SQLite logique, au CSV et au domaine de cette exécution. Pas de tendance CPU/RAM globale, p95 API ou capacité déduite.

Les replays M01/M02/M06 utilisent les mêmes sources et versions installées qu'au précédent banc, mais une machine partagée sans fréquence/cocharge/cache stabilisés ne permet pas d'attribuer les différences de temps à une évolution. Les allocations Python CSV de mêmes tailles/distributions et même code sont descriptivement rapprochables ; elles ne sont pas du RSS ou un gain. M-LIVE-01 est une nouvelle méthode, sans baseline antérieure : **NON COMPARABLE** quantitativement.

Aucun essai de correction avant/après. Gain après correction : **NON MESURÉ** pour toutes les propositions. Aucune décision utilisateur historique transposée. Tous les champs de choix courants restent vides.
