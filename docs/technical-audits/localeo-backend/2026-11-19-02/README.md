# Audit de performance Localeo Backend — 2026-11-19-02

**ARCHIVÉ LOCALEMENT — diagnostic terminé, neuf corrections proposées, aucun choix utilisateur reçu.** Date locale réelle : 19 novembre 2026, Europe/Paris ; instant initial 16:00:25 +01:00. Référence unique précédente : 2026-11-19, explicitement archivée, conservée intégralement. Suffixe -02 choisi parce que le nom de base existe ; pas de sélection sur mtime.

[Rapport exécutif](synthese/rapport-executif.md) · [neuf fiches](recommandations/backlog-final.md) · [choix vides](validation/decisions.md) · [résultats](benchmarks/resultats.md) · [limites](benchmarks/limites.md) · [comparaison](synthese/comparaison-precedent.md).

| Dépôt | Branche / SHA inspecté | État initial et modifications de cette exécution |
| --- | --- | --- |
| localeo-projet | main / f437465c577d3754b8743c6c48519f0d7606613e | Audits et atelier CRM non suivis préexistants ; seul ce nouveau dossier ajouté |
| localeo-backend | main / 7049e7fafc76f9119924f1082a5ee7457a175d85 | Suivi propre ; scripts/bruts ignorés dans tmp/performance-audit-2026-11-19-02 |
| localeo-marketplace | main / 9527ebbfee23f7c5249ce4078c5c3f476da2d924 | Propre, lecture consommateurs seulement |
| localeo-commercant | main / c61f196774c477065dfc51ebb87fc1a02404329b | Propre, lecture consommateurs seulement |
| localeo-animation | main / 7688f1cea11bec8599bacbfaa512b265c36fed3a | Propre, lecture consommateurs seulement |

Ces cinq références sont identiques à celles de l'exécution précédente. Objet backend ancien disponible et diff Git vide, arbre suivi propre ; aucune régression attribuée à un nouveau commit. État/digests : [baseline](validation/baseline.json), [comparaison Git](validation/comparaison-git.json).

## Périmètre et résultats

Priorité Localeo Live et portail Animation : scans QR/PIN, inscription/participation/lecture jeu, recherche et carnet, pilotage, commerçants/imports, clôture/tirage/gains/résultats ; dépendances partagées email/SMS et fournisseurs. Carte [architecture](inventaire/architecture.md), [flux](inventaire/flux-critiques.md), [API](inventaire/catalogue-api.md), [stack](inventaire/stack-technique.md), [ressources](inventaire/configuration-ressources.md), [limitations](inventaire/limitations.md), [orchestration](inventaire/plan-orchestration-agents.md).

- Six vrais rapports indépendants, contexte neuf, deux vagues de trois maximum ; sept missions spécialistes créées dont une interrompue après exposition accidentelle à des extraits historiques, exclue et remplacée. [Incident](agents/04-persistance-incident.md). Aucun verdict historique transmis aux premières analyses retenues.
- 17 constats majeurs d'origine : CPU 2, mémoire4, concurrence 2, persistance 3, API 3, SRE 3, chacun<=5. Deux apports de source de l'orchestrateur explicités ; regroupements/scissions aboutissent à17 causes candidates, pas 17 incidents.
- Dix causes alimentent neuf corrections finales : **0 P0  / 2 P1 conditionnels  / 7 P2**, trois A conditionnelles/six B. Sept causes annexées. R05 copie seule est P3 différable ; population entière du tirage toujours à mesurer.
- Un contradicteur réel indépendant ; réserves intégrées sur compteur exact/capacité, deux projections QR/PIN, page gains enrichie, budgets I/O et réservations progressives. Votes six perspectives **simulés**, jamais décisions ou preuve.
- Trois commandes composants réussies : M01/M02, M06 réduit et M-LIVE-01 nouveau. M01 scheduling ERP mesuré avec doubles ; M02 admission après bail en simulation ; M06 allocations CSV mesurées ; M-LIVE-01 transitoires domaine tirage, population/SQL hors fenêtre.
- HTTP/PostgreSQL intégré **NON EXÉCUTÉ**, aucune cible jetable explicitement désignée. Capacité API, saturation, gains après correction **NON MESURÉS**. Aucun changement applicatif implémenté.

Les fiches décrivent causes, sources/fonctions/lignes, conséquences/déclencheurs, statut de preuve, confiance, minimum/alternative, effort/risque/compatibilité, tests et rollback conservant les effets. [Consolidation](contradiction/consolidation.md), [causes](contradiction/causes-racines.md), [contre-expertise](contradiction/contre-expertise.md), [votes simulés](contradiction/debats-et-votes.md), [secondaires](recommandations/annexe-optimisations-secondaires.md).

## Banc et limites

Poste Windows 11 10.0.26200, Intel i7-10510U, 4 cœurs/8 logiques, RAM 17 007 263 744 octets ; partagé, fréquence/cocharge non stabilisées. CPython 3.14.3 via py -3.14 ; alias python indisponible, aucune installation. [Runtime installé](validation/runtime.json), [matériel](validation/hardware.json).

Verrouillé : FastAPI 0.136.0, Starlette 1.3.1, Uvicorn 0.52.4, SQLAlchemy 2.0.52 sync, psycopg 3.3.5, SQLAdmin 0.29.0, APScheduler 3.11.3. Installé : FastAPI 0.128.8, Starlette 0.50.0, Uvicorn 0.41.0, SQLAlchemy 2.0.48, psycopg 3.3.3. PostgreSQL serveur, déploiement, workers/réplicas/CPU/RAM/pool effectifs INCONNUS. Modèle exact et effort de l'orchestrateur/des agents **INCONNUS**, non déduits des noms.

1 329 modules Python parsés sans import, 1 365 décorateurs HTTP potentiels ; includes/mount/multi-méthodes non développés, donc pas comparable au compte 1346 développé de la référence ni preuve de routes déployées/trafic. Première tentative d'inventaire rejetée (codec mal nommé), corrigée sans source applicative modifiée.

[Protocole et sélection préalable](benchmarks/protocole.md), [sélection empreintée](validation/selection-mesures-avant.json), [profils CPU](benchmarks/profils-cpu.md), [mémoire](benchmarks/profils-memoire.md), [backlog après mesures](recommandations/backlog-mesure.md). Budget 512 Mio, minimum1 Gio disponible, 3 s/cas/60 s/campagne, aucun seuil relevé. Profils et timings séparés ; pas d'extrapolation vers utilisateurs ou SLA.

## Conservation et contrôles

Prompt réellement invoqué intégral : [relance](prompts/00-relance-utilisee.md), briefs exacts et [messages](prompts/invocations.md). Les six anciens prompts n'ont pas été recopiés comme invoqués. Le script d'audit, harness et bruts restent applicatifs et ignorés, aucune donnée de travail déplacée ici.

Ancien manifeste 99/99 et 17 empreintes sources/bruts/harness concordent. [Empreintes avant](validation/archives-avant.json), [provenance](validation/provenance-ancienne-mesure.json), [manifeste des nouvelles mesures](validation/mesures-manifeste.json), [contrôles finaux](validation/controles.md). Bruts non versionnés : dépendance de rejouabilité locale, sauvegarde distante non garantie.

[Manifeste final de cette archive](validation/manifest-archive.json), hors lui-même et son empreinte pour éviter circularité. Contrôles documentaires distincts des trois tests composants et des décisions utilisateur. Aucun guide/contrat source exportée modifié ; source canonique et consommateurs conservés. Critères d'acceptation, fonctionnel/ops, migrations et générateur sans impact d'exécution par nature diagnostique ; leurs impacts potentiels sont conditions des fiches futures.

Statut final : archive locale, sans commit/push/déploiement. Les décisions restent entièrement vides. Suite : **R01 et R10 — VALIDÉE / REFUSÉE / À APPROFONDIR / REPORTÉE**, séparément. Aucune implémentation/migration/livraison autorisée par ce prompt.
