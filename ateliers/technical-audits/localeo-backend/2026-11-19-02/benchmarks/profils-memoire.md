# Profils mémoire

[Résultats chiffrés](resultats.md). CSV : pics Python 674 904 /2 816 904 /5 494 404 octets à1k/5k/10k, trois essais identiques ; sortie entière et transitoires visibles. M-LIVE-01 : environ 41,8ko puis 656,1ko à5k/10k, pas la population totale (tuple/UUID hors fenêtre). Collections à capacité discrète, plateau explicite.

Allocations Python ≠ RSS ; working set et maximum Windows séparés. Ni mémoire native/ORM/driver complète, ni fuite mesurés. Pas de somme de pics de processus distincts. Les snapshots bruts montrent les objets retenus ; une allocation temporaire peut avoir disparu.

Aucun spool ou sélection optimisée exercé ; bénéfice plausible seulement, gain NON MESURÉ.
