# Annexe CPU — observations secondaires et bornes

Complément de [01-cpu.md](01-cpu.md). Lecture statique uniquement ; aucun résultat de performance mesuré. Modèle exact et effort du modèle : **INCONNU**.

## A-CPU-01 — Liste historique de participants : pagination après calcul intégral

**FORTEMENT ÉTAYÉ PAR LE CODE**, mais non retenu comme constat majeur du parcours actuel.

`ServiceExploitationAnimation.lister_participants`, `app/application/animation_locale/services/exploitation_animation.py`, lignes 321–342 et 368–371 : les modèles historiques qui ne sont pas redirigés chargent les provenances gelées, matérialisent `_participations` (lignes 35–36), recalculent/filtrent les lignes, puis trient la collection avant de découper la page. Coût O(N) de faits et O(N log N) de tri, mémoire O(N), même pour la première page. En mélange historique/moteurs projetés, lignes 347–365, la source projetée est parcourue par pages et fusionnée, mais les lignes historiques sont toujours toutes calculées.

Les routes restent exposées : `animation_locale_api.py`, lignes 3414–3420 et 3443–3448. **Ne pas étendre ce constat aux listes principales actuelles** : `localeo-animation/src/app/App.tsx:1625` sélectionne `GlobalReadWorkspace` pour les autres modèles ; `src/app/globalReadApi.ts:12` utilise `/lectures-globales/participants`, dont le repository `app/infrastructure/persistence/repositories/lectures_globales_animation.py:86` applique `limit+1` avant hydratation. Chasse, Juste Prix, Vitrines et Tombola publique possèdent aussi des voies dédiées/projetées (exploitation, lignes 297–314). La présence des anciens wrappers `api.ts:1236` et `1312` ne prouve pas leur fréquence d’appel actuelle.

Confiance élevée sur le coût, faible sur l’exposition réelle résiduelle. Impact potentiel moyen, probabilité faible/inconnue, criticité faible à moyenne. Correction minimale : inventorier les derniers appelants de ces routes et les rediriger vers les lectures projetées ; ne pas changer silencieusement recherche/tri/total historiques. Effort M ; risque de compatibilité si route supprimée, pas nécessaire de la supprimer pour améliorer ses consommateurs. API/Animation/ERP à inventorier avant changement.

## A-CPU-02 — Imports : boucles imbriquées présentes, mais périmètre borné

`app/application/referencement/services/preparation_commercant_import.py:43–58` compare chaque ligne à chaque fiche candidate ; `imports_commercants.py:167–170` compare chaque source aux provenances. Complexité O(L×C) / O(L×P) sur les collections effectivement chargées. **FORTEMENT ÉTAYÉ PAR LE CODE**, sans preuve d’un problème majeur.

Le périmètre moderne impose L ≤ 100 (`charger_faits_dans_uow:22–23`, parseur `preparer:141`). Le repository de candidats plafonne les branches et le résultat à 101 (`preparation_import_commercant_repository.py:83–110`), puis signale l’excès. L’import de fichier est limité à 2 000 000 octets ; CSV : 50 colonnes et 10 000 cellules ; XLSX : taille décompressée totale déclarée ≤ 20 000 000 octets, 200 entrées maximum, 20 feuilles et 10 000 cellules (`parseur_imports_commercants.py:13,32,55–58,65–66,90–110`). Le worker traite 1–100 lignes avec un budget temporel (`traitement_imports_commercants.py:101–123`).

Impact/probabilité faibles aux limites actuelles, confiance élevée sur les bornes. Indexer en mémoire les fiches/provenances par email/SIRET/ID peut réduire les comparaisons (S/M), mais cette revue ne justifie pas une refonte. Préserver détection d’ambiguïtés, masquage hors commune, versions et provenance. Avant un élargissement des plafonds, réexaminer le parseur, le rapprochement et les consommateurs ensemble.

## A-CPU-03 — Jeux et dashboard : travail par définition, pages explicitement bornées

Le dashboard Live limite ses pages à 50 (`tableau_de_bord_live.py`, `consulter`, lignes 137–144) et précharge validations/exécutions avant les projections (`_items`, lignes 117–135). `_item` calcule progression puis parfois qualification : travail répété à observer si les définitions grossissent, sans charge non bornée démontrée ici. `jeu_animation.py:477` et `522–523` trient les produits/vitrines avant la tranche, mais la définition Vitrines impose 1–100 commerces (`domaine/animation_locale/moteurs/vitrines.py:41`). Aucun constat de complexité majeure sur ces seuls tris bornés.

La recherche Live (`recherche_animations_live.py`) impose 1–10 communes et 1–50 résultats (lignes 68–70), puis hydrate la page SQL sélectionnée avec `page_size+1`. Ne pas lui attribuer le coût de l’ancien calcul historique des participants. L’efficacité SQL réelle reste à mesurer ; cette annexe ne déduit pas un plan d’exécution de la présence d’un `LIMIT`.

## A-CPU-04 — Clôture et tirages libres : distinguer streaming et reprise

Le gel commun accumule des lots et une empreinte incrémentale dans `exploitation_animation.py:215–258` ; son coût total reste linéaire en participants et preuves. Une lecture par lots limite les conteneurs, pas nécessairement la durée totale d’une transaction. Les clôtures Juste Prix et Vitrines disposent en plus d’un état de reprise : `exploitation_juste_prix.py:82–95`, `exploitation_vitrines.py:143–156` ; lot de 1–100 participants et curseur persisté. Les lanceurs limitent aussi les cycles à 250 lots et 30 secondes. Ne pas fusionner ces mécanismes dans un constat de clôture globale non bornée.

Le tirage libre (`tirages_libres.py:252–285`) indexe puis classe au plus 500 candidats par tranche ; unités de dotation lues par 100 (`346–377`), budget de scellement 20 secondes (`313–335`). Le `pop(0)` sur ces buffers déplace des éléments mais la taille est plafonnée à 100 : observation mineure, pas algorithme quadratique dans toute la population. Cette voie ne corrige pas automatiquement le tirage Coffrets de CPU-02.

## Périmètre et limites de l’annexe

Les observations servent à éviter les généralisations et préparer une vérification ciblée, pas à fixer des quotas de constats. Les parcours source consultés couvrent QR/participation, recherche et catalogue Live, dashboard, imports/référencement commerçant, exploitation/clôture et tirages/résultats. Pas de profil de sérialisation Pydantic/JSON ni de volumétrie utilisateur exécuté ; aucun goulot CPU général attribué au framework. Les domaines/API cités constituent des liens de dépendance source, pas une preuve de trafic réel ou de déploiement.
