# Résultats — mécanismes locaux, capacité non mesurée

Campagne du 19 novembre 2026, backend `7049e7fafc76f9119924f1082a5ee7457a175d85`. Conditions, seuils et amendement préalable à la reprise CSV : [protocole](protocole.md). [Limites](limites.md), [CPU](profils-cpu.md), [mémoire](profils-memoire.md). Aucun gain après correction démontré : aucune correction ni variante optimisée exécutée.

## Registre des tentatives

| Tentative | Statut réel | Durée rapportée | Usage des résultats |
| --- | --- | --- | --- |
| 01 | ÉCHEC avant mesure : structure Windows incomplète | pytest 2,77 s | Aucun ; XML et harness conservés |
| 02 | ÉCHEC harness : décorateur dataclass retiré par erreur à l’extraction | interne 8,759 s ; pytest 11,09 s | M01 conservé à titre de tentative ; non retenu pour la restitution finale |
| 03 | ARRÊT au seuil préétabli : profilage CSV 4,315 s >3 s | interne 29,678 s ; pytest 32,45 s | **M01 et M02 complets retenus** ; CSV partiel non conservé, non exploité |
| 04 | SUCCÈS, campagne réduite CSV seul, seuils inchangés | interne 8,794 s ; pytest 10,87 s | **M06 complet retenu** à 1 000 / 5 000 / 10 000 lignes |

Les trois échecs/arrêts précèdent toute conclusion de capacité et ne sont pas des erreurs de l’application. La tentative 03 ne devient pas un succès global parce que deux scénarios ont abouti. L’arrêt CSV n’est pas un incident métier ni une preuve de lenteur sans profileur. Pas de répétition des paliers M01 après cet arrêt ; le nouveau maximum CSV est inférieur à celui initialement prévu. Les bornes mémoire/temps campagne n’ont pas été relevées.

Commande réellement utilisée depuis le backend, avec XML propre à chaque tentative : `py -3.14 scripts/validation/test_isolated.py tmp/performance-stage4-2026-11-19/test_components.py -q --junitxml=tmp/performance-stage4-2026-11-19/pytest-attempt04.xml --tb=short`. Tentative 01 : `pytest.xml`, sans `--tb=short` ; tentative 02 : `pytest-attempt02.xml`, sans `--tb=short` ; tentative 03 : `pytest-attempt03.xml`, avec `--tb=short`. Le harness évolue entre tentatives ; ses quatre états et leurs empreintes restent archivés.

## M01 / OPT-01 — Blocage de la boucle reproduit

**CONFIRMÉ PAR MESURE LOCALE DU MÉCANISME**, avec dépendances doubles. Fonctions exécutées : [handlers ERP, lignes 12523–12600](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523). Les corps async réels ne rendent pas la main pendant l’appel du runner double puis du batch double. Attente synchrone injectée : **10 ms par appel batch**, et non une latence fournisseur observée. Témoin prêt juste après la mise en file des batchs ; une attente inclut donc les batchs qui le précèdent. 20 répétitions par cellule, témoin sans opération SQL/HTTP.

| Handler | Coroutines batch | Contrôle sans attente p50, ms | Attente témoin p50, ms | p95, ms | p99, ms |
| --- | --- | --- | --- | --- | --- |
| lancer_batch_envoi_emails | 1 | 0,051 | 10,574 | 10,741 | 10,761 |
| lancer_batch_envoi_emails | 5 | 0,087 | 52,352 | 52,923 | 52,924 |
| lancer_batch_envoi_emails | 10 | 0,351 | 104,527 | 108,504 | 170,016 |
| synchroniser_statuts_emails | 1 | 0,051 | 10,407 | 18,775 | 26,164 |
| lancer_batch_envoi_sms | 1 | 0,089 | 10,588 | 18,433 | 25,056 |
| synchroniser_statuts_sms | 1 | 0,096 | 10,487 | 10,774 | 10,774 |

240 tours mesurés, chacun avec un témoin ; zéro réponse d’erreur du double de redirection, vérifiée explicitement pour que le `except` du handler ne masque pas un défaut de harness. p99 = maximum sur 20 essais ; un contrôle SMS sans attente atteint déjà 17,630 ms au maximum : la machine partagée introduit du bruit. Aucun taux d’erreur HTTP mesuré.

Goulot dominant du scénario injecté : **attente synchrone dans le thread de boucle**, pas calcul CPU. Le contrôle sans attente et les trois autres handlers reproduisent la même frontière. Le véritable BatchRunner, UoW et fournisseur ne sont pas exercés dans M01 ; leur caractère synchrone reste prouvé par les sources. Aucun worker ASGI ni threadpool réellement saturé. Confiance élevée sur le mécanisme des quatre corps, incidence en exploitation inconnue. Correction minimale : déporter toute l’unité synchrone en conservant identité/corrélation/sessions/erreurs. Gain plausible : disponibilité de la boucle pendant I/O ; **gain chiffré NON MESURÉ**, test intégré et avant/après nécessaires.

## M02 / OPT-02 — Admission après expiration reproduite en simulation

**FORTEMENT ÉTAYÉ PAR LE CODE, CONFIRMÉ PAR SIMULATION FONCTIONNELLE LOCALE**. [BatchRunner, lignes 608–700](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608), définition `emails.envoyer` timeout 300 s, bail timeout+60 =360 s. SQLite en mémoire, deux mappings minimaux et domaine d’exécution réels ; horloge UTC contrôlée, perf_counter réel.

| Temps logique | Premier handler | Second lancement du même code |
| --- | --- | --- |
| +359 s | Présent dans la pile | Rejeté par le verrou existant |
| +361 s | Toujours présent dans la pile | Admis ; deuxième handler imbriqué exécuté |

Deux handlers simultanément présents dans la pile, deux journaux `SUCCES` en fin de scénario, aucun verrou restant. Temps mural du contrôle local : 65,381 ms. **Aucun traitement réel de 361 s, aucun timeout client observé, aucun parallélisme PostgreSQL ni double envoi démontré.** Le second handler finit avant le premier : ce cas ne prouve pas la sûreté de libération par ancien propriétaire, seulement l’admission lorsque le premier n’est pas terminé.

Cause retenue : bail expirant sans borne du handler ; le scénario confirme la logique suspectée. Goulot de capacité réel NON MESURÉ. Correction minimale inchangée : budget monotone et réservations progressives, délais fournisseur explicites, renouvellement propriétaire seulement si nécessaire ; préserver les remises incertaines. Gain plausible : cycles mieux bornés ; **gain de durée/débit NON MESURÉ**. La preuve PostgreSQL à deux lanceurs et la suite d’invariants outbox restent indispensables.

## M06 / OPT-06 — Sortie CSV entière et allocations croissantes mesurées

**CONFIRMÉ PAR MESURE LOCALE** pour la génération CSV : [produire_csv, lignes 13–27](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13). Le [service exporteur](../../../../../../localeo-backend/app/application/gestion_achats/services/consultation_paiements.py#L150) garde ses pages SQL de 100, mais il n’est pas exécuté par ce banc. Générateur paresseux de 11 colonnes finance, identifiants fixes ASCII, concurrence 1. Sept essais temporels sans profileur par volume ; trois essais allocations séparés.

| Lignes | Sortie UTF-8, octets | Durée p50, ms | p95, ms | p99, ms | CPU processus p50, ms | Débit médian, lignes/s |
| --- | --- | --- | --- | --- | --- | --- |
| 1,000 | 119,189 | 21,509 | 30,431 | 30,431 | 31,250 | 46491 |
| 5,000 | 595,189 | 136,894 | 147,504 | 147,504 | 125,000 | 36525 |
| 10,000 | 1,190,189 | 244,781 | 260,209 | 260,209 | 203,125 | 40853 |

p95/p99 = maximum sur sept essais. CPU et débit incluent la fabrication des lignes synthétiques ; il ne s’agit pas de CPU/requête HTTP ou de requêtes/s. BOM, nombre de lignes et empreinte identique vérifiés entre répétitions. Aucun essai avant/après de spool, ni projection SQL, client lent, abandon ou erreurs d’écriture.

Pics tracemalloc : 674 904 / 2 816 904 / 5 494 404 octets, chacun identique sur trois répétitions. À 10 000 lignes : sortie 1 190 189 octets, pic Python 5,24 Mio. Ce pic croît avec la sortie malgré une entrée génératrice. **Aucun OOM ou épuisement mémoire observé** dans l’enveloppe ; aucune borne de capacité pour de gros exports concurrents. Le détail des allocations et du working set est dans [profils-memoire.md](profils-memoire.md). Le spool reste plausible pour borner la sortie en RAM, **gain NON MESURÉ**.

## Hypothèses infirmées et sujets non mesurés

Aucune des huit causes principales n’est infirmée dans son périmètre. Le test du bail contredit l’idée qu’un timeout catalogue suffirait à arrêter le handler ; il ne démontre pas un double effet fournisseur. Les mesures CSV ne justifient aucune affirmation d’OOM à 10 000 lignes. Aucune conclusion de saturation CPU globale, de fuite mémoire ou de saturation scheduler n’est ajoutée.

M03/M04/M05/M07/M08 et M09–M13 : **NON EXÉCUTÉS**, conditions SQL, fournisseurs ou volumes réels manquants ; protocoles conservés. p50/p95/p99 API, débit HTTP, erreurs HTTP, SQL/temps cumulé, verrous PostgreSQL, saturation workers/pools et allocations natives : **NON MESURÉS**. [Backlog révisé](../recommandations/backlog-mesure.md) : huit orientations, deux P1 et six P2 conditionnels, aucun P0 ; preuve renforcée pour OPT-01/06 et simulation explicite pour OPT-02.

Sources des chiffres : `results-attempt03.json` et `results-attempt04.json` dans le répertoire backend indiqué au protocole. [Manifeste expurgé et empreintes](../validation/etape-4-manifeste.json). Les bruts ne sont pas copiés dans le dépôt documentaire.
