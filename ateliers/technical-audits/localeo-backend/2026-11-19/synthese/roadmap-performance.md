# Roadmap performance conditionnelle

Cette roadmap est propre à l’audit et **ne modifie pas la roadmap produit commune**. Aucune correction n’est validée ; aucune échéance ou affectation d’équipe n’est décidée. Les [huit fiches](../recommandations/backlog-final.md) et le [registre d’arbitrage](../validation/decisions.md) définissent le périmètre à décider. Les votes simulés ne déclenchent aucun travail.

| Horizon proposé | Sujet | Déclencheur | Critère de sortie et risque principal |
| --- | --- | --- | --- |
| Immédiat, après choix explicite | OPT-01 — A/P1/S, déporter les quatre batchs ERP | Validation d’OPT-01 ; correction locale séparée | Témoin/scan disponibles pendant I/O, identité/corrélation/303/erreurs inchangés, sessions dans un seul thread. Déconnexion ne provoquant pas de renvoi aveugle ; mesurer attente du threadpool et SQL |
| Immédiat, après choix explicite | OPT-02 — B/P1/M, budget et bail email/SMS | Validation distincte d’OPT-02 ; PostgreSQL jetable autorisé pour la preuve intégrée | Reliquat non commencé reprenable, droits et rapprochement préservés, propriété de bail et deux lanceurs vérifiés. Risque principal : envoi incertain ou message réservé abandonné |
| Moyen terme, selon cohortes | OPT-03 — B/P2/S, exclusion des relances avant LIMIT | Cohortes/fenêtres et défaut de progression exercés sur données synthétiques | Progression complète, clé d’unicité conservée et concurrence sans doublon ; pas d’augmentation arbitraire de limite |
| Moyen terme, selon trafic | OPT-04 — B/P2/M, projections Live/détails puis historique | Mesurer M04 et distinguer variantes consommées ; UI dashboard en mode borne | Payloads exacts, mêmes dates Paris/statuts/archives/droits, moins de faits hydratés. Ne pas remplacer silencieusement une réponse par le mode borne |
| Moyen terme, selon coût SQL | OPT-05 — B/P2/M, faits du lot d’expiration groupés | Mesurer SQL, temps sous verrou et RAM avant/après | Même sélection de racines/verrous, garde remboursement et crédit B2B, commit inchangé ; gain non transféré en allocations excessives |
| Moyen terme, différable | OPT-06 — B/P2/M, spool CSV | Volumétrie/concurrence et budget mémoire réels à établir ; pas d’OOM sur 10 000 lignes testées | Octets/BOM/formules/ordre identiques, projection fermée avant client lent, mémoire/disque bornés et temporaires nettoyés en abandon/erreur |
| Moyen terme, selon stockage | OPT-07 — B/P2/M, budget des médias distants | Mesurer get/read/retries sur le stockage réellement choisi et ses doubles | Intégrité/provenance/autorisation conservées, Body fermé, octets bornés ; ne pas promettre une deadline absolue sur simple read timeout |
| Moyen terme, selon retour paiement | OPT-08 — B/P2/M, lecture Stripe minimale hors UoW | Mesurer fréquence de l’en-tête, durée Stripe et rétention SQL | Helper de réconciliation conservé, token réautorisé après attente, statut webhook local, aucune transaction SQL pendant HTTP |
| Architecture future, hors plan | Projection historique, protocole de remise découplé, refonte de tirage, isolation scheduler/cache | Budget dépassé ou contention démontrée, fiche C distincte justifiée | Preuve métier, équité/rejeu, révocation, invalidation et capacité ; aucun chantier automatique issu de la présence d’un risque |

Les lots P1 restent séparables ; déporter ne borne pas un cycle et borner un cycle ne libère pas une boucle async. S’ils sont tous deux choisis, les réaliser séquentiellement sur les fichiers communs pour isoler validation et retour arrière. Aucun total d’efforts S/M converti en planning contractuel.

Avant toute mesure intégrée future : cible isolée explicitement désignée, données synthétiques, fournisseurs doubles, versions et ressources connues, budgets et seuils d’arrêt fixés. Reprendre le [protocole](../benchmarks/protocole.md) en **nouvelle exécution datée**, jamais écrire dans les preuves gelées. Sans environnement autorisé, préparer la mesure et consigner NON EXÉCUTÉ.

Après chaque correction autorisée : tests d’invariants et de contrat, comparaison avant/après sur mêmes conditions, CPU/RSS/SQL/latence ou progression selon le flux, retour arrière sans effacer les effets métier. Aucun gain cible chiffré fiable disponible aujourd’hui. Les nouvelles limites d’images, changements de réponse ou de statut HTTP relèveraient d’un arbitrage D distinct.

La prochaine action attendue est le choix utilisateur pour les P1, ou l’invocation du [prompt de relance](../prompts/RELANCER-AUDIT.md) pour une nouvelle photographie. L’archivage ne transforme aucune ligne en VALIDÉE, REFUSÉE, À APPROFONDIR ou REPORTÉE.
