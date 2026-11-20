# Profils CPU et temps de traitement

Scénario M06, tentative 04, fonction source [produire_csv](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13), générateur synthétique inclus. cProfile exécuté séparément à 10 000 lignes ; fichier binaire et texte dans `localeo-backend/tmp/performance-stage4-2026-11-19/csv-10000.pstats` et `csv-10000-profile.txt`. Empreintes : [manifeste](../validation/etape-4-manifeste.json). Aucun profil après correction.

| Fonction / opération | Appels | Temps propre cProfile, s | Temps cumulé, s |
| --- | --- | --- | --- |
| produire_csv | 1 | 0,345 | 0,729 |
| csv.writer.writerow | 10 001 | 0,101 | 0,101 |
| str.startswith | 110 000 | 0,061 | 0,061 |
| Générateur synthétique rows | 10 001 | 0,058 | 0,058 |
| list.append | 110 000 | 0,056 | 0,056 |
| dict.get | 110 000 | 0,055 | 0,055 |
| str.lstrip | 110 000 | 0,052 | 0,052 |
| StringIO.getvalue | 1 | 0,001 | 0,001 |

460 006 appels, durée instrumentée arrondie 0,729 s. Le temps propre du parent inclut la boucle Python et les conversions non isolées dans la table ; ne pas l’attribuer à une seule allocation. Ne pas additionner temps parent cumulé et temps enfants. L’instrumentation modifie le temps : le p50 sans profileur à 10 000 lignes est 244,781 ms, CPU processus médian 203,125 ms ; ces séries distinctes ne constituent pas un gain. `process_time` Windows a ici des pas visibles de 15,625 ms : les petites valeurs ne permettent pas de précision sub-milliseconde.

Le profil local met en évidence le coût de formatage par cellule, mais ne justifie pas de supprimer la protection contre les formules tableur ni de micro-optimiser les conversions. Il inclut la fabrication des entrées (0,058 s instrumentée), et n’exerce ni SQL ni l’encodage de réponse. Goulot mémoire de la sortie plus directement étayé que l’urgence CPU ; pas de saturation CPU démontrée.

M01 : aucune cProfile supplémentaire, les attentes synchrones injectées suffisent à observer la progression de la coroutine témoin. Les compteurs CPU processus bruts sont conservés ; médianes souvent nulles à cette granularité, ce qui ne signifie pas zéro CPU. Le retard témoin n’est pas du CPU consommé. M02 : simulation fonctionnelle courte, pas un profil de charge.

CPU par requête API, CPU des scans QR/participations, coûts SQL, médias natifs, tirage et saturation multiworkers : **NON MESURÉS**. Les mesures avant/après restent nécessaires sur cible jetable, même jeu et mêmes ressources. Aucun gain chiffré proposé.
