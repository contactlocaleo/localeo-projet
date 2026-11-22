# Rapport exécutif — audit backend du 19 novembre 2026

**Deux corrections P1 méritent un arbitrage : déporter les batchs ERP hors de la boucle async et encadrer le cycle/bail des remises email/SMS. Aucune correction n’est autorisée ni implémentée.** Le dossier est archivé ; les huit choix du [registre](../validation/decisions.md) restent en attente. L’autorisation d’archiver ne vaut pas validation des corrections.

L’inspection directe de 1 329 modules a permis de cartographier 1 346 opérations HTTP statiques potentielles. Six spécialistes indépendants ont produit 17 constats majeurs, rapprochés en **14 problèmes causaux distincts / causes candidates** : huit alimentent le backlog principal, six restent en annexe. Ce comptage ne signifie pas que 14 incidents sont démontrés. Le [backlog final](../recommandations/backlog-final.md) propose huit corrections, **0 P0, 2 P1, 6 P2**, une A conditionnelle et sept B. Aucun refactoring C ou breaking change D recommandé.

## Goulots, preuves et API à risque

| Cause / correction | Flux et API | État de preuve et limite | Priorité |
| --- | --- | --- | --- |
| RC-06 / OPT-01 : absence de frontière async/sync | Quatre POST `/internal/emails/batch/envoyer`, `/internal/emails/batch/synchroniser-statuts`, `/internal/sms/batch/envoyer`, `/internal/sms/batch/synchroniser-statuts` ; effets indirects sur les requêtes du même processus | Blocage de scheduling mesuré sur corps source et doubles. Dix appels avec 10 ms injectées chacun : témoin p50 104,527 ms, contrôle 0,351 ms. Pas de latence HTTP ni de capacité mesurée | P1 / A conditionnelle / S |
| RC-08 / OPT-02 : durée du handler non liée au bail | POST `/protected/exploitation/emails/batch/envoyer`, `/protected/exploitation/sms/batch/envoyer` et déclenchements ERP d’envoi | Code fortement étayé ; simulation SQLite/UTC : deuxième lancement rejeté à +359 s et admis à +361 s pendant le premier handler. Pas de durée réelle de 361 s, concurrence PostgreSQL ou double envoi prouvés | P1 / B / M |
| RC-01 / OPT-04 : projections statistiques à partir de populations entières | GET `/protected/animation-locale/animations/{id}/live`, dashboard sans `mode_lecture=borne`, GET détail et réponse PATCH hors branche Tombola | Chargements/mapping prouvés par code, impact non mesuré. L’UI actuelle demande le dashboard borné ; ne pas généraliser le défaut à cette variante, à la création ou aux listes déjà résumées | P2 / B / M |
| RC-10 / OPT-03 et RC-09 / OPT-05 : sélection de rappels avant exclusion et lectures répétées sous verrou | POST `/protected/gestion-achats/coffrets-instances/expiration/reminders/batch` et `/expiration/batch` | Risques de progression et de contention étayés ; cohortes, SQL et concurrence non mesurés. Pas de perte réelle de rappel démontrée | P2 / B / S puis M |
| RC-05 / OPT-06 : sortie CSV entière en mémoire | GET `/internal/gestion-achats/paiements/export-metier.csv` et `/export-finance.csv` | Allocations locales mesurées : 10 000 lignes, sortie 1 190 189 octets, pic Python 5 494 404 octets (5,24 Mio). Aucun OOM ; SQL/HTTP/client lent non exercés | P2 différable / B / M |
| RC-11 / OPT-07 : budget média non transmis à l’I/O | GET `/public/localeo-live/participations/{id}`, avec média sélectionné | Code étayé ; durées stockage inconnues. Limites média/JSON existantes ; pas de payload illimité ni de nécessité de cache démontrés | P2 / B / M |
| RC-12 / OPT-08 : helper Stripe enrichi sous transaction de lecture | GET `/public/gestion-achats/paiements/retour/{achat_id}`, avec `X-Checkout-Session` | Code étayé ; latence Stripe et occupation SQL non mesurées. La variante sans en-tête évite cet appel | P2 / B / M |

Références : [causes racines et fichiers](../contradiction/causes-racines.md), [preuves et fiches avec lignes](../recommandations/backlog-final.md), [résultats détaillés](../benchmarks/resultats.md). Les scans QR, inscriptions, imports commerçants, clôtures et tirages ont été suivis de bout en bout ; leur capacité nominale n’a pas été qualifiée. Ils peuvent subir une indisponibilité des ressources partagées sans qu’un hotspot direct ait été démontré sur chacun.

## Corrections immédiates proposées, sous validation

**OPT-01** réutilise le threadpool présent : capter identité/contexte de requête, puis déporter l’unité synchrone complète avec des sessions confinées au thread. Risques : perte de corrélation, session traversant les threads, effets encore actifs après déconnexion. Conserver réponse 303, erreurs et droits ; ne pas rejouer un envoi pour compenser une réponse perdue.

**OPT-02** lie budget de cycle, réservation progressive et bail propriétaire pour email/SMS. Risques : messages réservés non commencés, reprise incertaine, perte de bail, effet fournisseur accepté avant crash. Ne pas interrompre aveuglément une remise ni sortir HTTP de sa transaction d’autorisation ; RC-07, rétention SQL pendant remise, demeure une cause distincte. L’effort M suppose ce périmètre limité, sans refonte générale du scheduler.

Les P1 sont indépendants. Leur priorité repose sur un mécanisme local et un scénario crédible de dégradation fournisseur, pas sur un incident de production observé. Les tests de concurrence PostgreSQL, contrats et retours arrière restent à exécuter après choix utilisateur.

## Moyen terme et options architecturales

Choisir les P2 selon exposition et mesures : progression des relances, agrégats Live/détails, groupement des lectures d’expiration, spool CSV borné, budget de stockage et lecture Stripe minimale avec réautorisation après attente. Aucun calendrier ni coût en jours/euros n’est inventé ; S/M sont relatifs. Les [fiches](../recommandations/backlog-final.md) définissent les alternatives, risques et tests.

Les six autres causes restent annexées : qualification historique avant pagination, pixels OnBoard, population exhaustive du tirage, transaction de remise, contention scheduler hypothétique et revalidation média. Une nouvelle projection durable, un protocole découplé de remise ou une refonte de tirage pourraient relever de C ; nouveaux refus d’images ou changement de réponse API de D. Leur nécessité n’est pas démontrée. Le cache média, l’augmentation générale des workers/pools et un nouveau broker ne sont pas des corrections adoptées.

## Mesures, gains et réserves

Deux mécanismes sont **confirmés par mesure locale** : blocage des corps async ERP et allocations CSV. Le bail est **confirmé en simulation structurelle**, pas en charge réelle. Les cinq autres orientations principales restent fortement étayées par le code et non mesurées. Saturation CPU globale, fuite mémoire, OOM, saturation de l’executor et double envoi restent non démontrés. Aucune cause principale n’a été infirmée dans son périmètre.

**Gain après correction : NON MESURÉ pour les huit orientations.** Bénéfices plausibles : progression de la boucle, cycles mieux bornés, moins de faits/aller-retours, sortie CSV moins retenue en RAM, connexion SQL libérée pendant Stripe. Aucun pourcentage fiable ni gain de capacité estimé. Le profil CSV mesure aussi son générateur synthétique ; les percentiles sur sept exports ou vingt témoins ne sont pas des SLA.

Quatre tentatives de banc conservées : deux erreurs de harness, une interruption au seuil de profilage CSV, puis succès d’une campagne CSV réduite. M01/M02 proviennent de la tentative 03, M06 de 04. Aucun serveur HTTP, fournisseur ou PostgreSQL de production testé ; configuration déployée, workers et ressources allouées inconnus. Versions installées différentes du verrouillage. Les [limites](../benchmarks/limites.md), [empreintes](../validation/etape-4-manifeste.json) et [comparaison historique](comparaison-precedent.md) empêchent toute lecture comme qualification de production.

Statut final : archivage documentaire, preuves conservées, décisions non reçues, aucune implémentation/migration/déploiement. [Roadmap conditionnelle](roadmap-performance.md), [prompt de relance](../prompts/RELANCER-AUDIT.md).
