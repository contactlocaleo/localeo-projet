# Profils mémoire — CSV synthétique

Source exécutée sans modification : [produire_csv](../../../../../../localeo-backend/app/application/gestion_achats/services/export_financier.py#L13). Scénario M06, tentative 04 ; protocole et tentatives dans [resultats.md](resultats.md). Aucune image ni donnée métier réelle. Trois profils tracemalloc indépendants par volume, sortie retenue pendant le relevé. Encodage UTF-8 de contrôle effectué en dehors de cette fenêtre : il n’est pas inclus au pic Python ci-dessous.

| Lignes | Sortie UTF-8, octets | Python retenu, octets | Pic Python, octets | Working set après cas, octets | Pic historique processus, octets |
| --- | --- | --- | --- | --- | --- |
| 1,000 | 119,189 | 244,168 | 674,904 | 79,056,896 | 79,056,896 |
| 5,000 | 595,189 | 1,196,168 | 2,816,904 | 78,417,920 | 81,391,616 |
| 10,000 | 1,190,189 | 2,386,168 | 5,494,404 | 78,426,112 | 83,251,200 |

Chaque pic Python est identique sur les trois répétitions de son volume. La chaîne retournée avec BOM est conservée au moment du snapshot. `current` comprend cette chaîne et les petits objets encore vivants du générateur et du writer, ce n’est pas un nombre total d’allocations effectuées. Les blocs du snapshot sont les blocs retenus ; le churn total d’allocations n’a pas été mesuré. L’emplacement source principal du snapshot est le retour `export_financier.py:27`.

Le pic Python passe de 674 904 à 5 494 404 octets lorsque le nombre de lignes passe de 1 000 à 10 000 : sortie matérialisée, mémoire croissante sur cet intervalle. L’augmentation n’est pas convertie en prévision pour un million de lignes. La mémoire des lignes d’entrée n’est pas retenue dans une liste globale. Le fait que la sortie soit peu volumineuse en UTF-8 ne représente pas son coût interne Python.

Working set initial tentative 04 : 78,602,240 octets ; final : 78,467,072 ; maximum historique processus en fin de campagne : 83,251,200. Disponibilité physique finale : 3,198,259,200 octets, au-dessus du seuil d’arrêt 1 Gio. Le working set final inférieur à l’initial ne prouve ni fuite ni absence de fuite : mesures ponctuelles, caches/allocateur/OS et autres essais du même processus. Le maximum Windows est cumulatif, **pas un pic RSS propre à chaque CSV**.

Goulot confirmé : `StringIO` puis chaîne entière ; SQL paginé seul ne borne pas cette sortie. Aucun épuisement observé sur les volumes testés, concurrence 1. P2 conditionnel conservé : plus gros volumes, concurrence réelle et budget RAM cible sont inconnus. Aucun gain après spool mesuré. Nécessaire ensuite : RSS/native continu, allocation/sortie HTTP, spool et disque bornés, projection fermée avant client lent, double export et abandon, mêmes octets et nettoyage.

OnBoard/rasters, tirage gelé, statistiques et CSV de 50 000 lignes : **aucun profil exploitable validé** dans cette campagne. L’arrêt au seuil de temps sous tracemalloc ne permet pas d’attribuer une latence non instrumentée ni un pic à ce volume. Aucun outil mémoire natif installé.
