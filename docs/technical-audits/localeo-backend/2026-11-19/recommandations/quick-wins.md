# Quick wins proposés

**Un seul candidat A : OPT-01, P1, effort S. Aucun choix utilisateur reçu.** [Fiche complète](backlog-final.md#opt-01--déporter-les-quatre-batchs-erp-hors-de-la-boucle), [registre de décision](../validation/decisions.md). Les gains après correction sont **NON MESURÉS**.

Les quatre handlers ERP email/SMS exécutent aujourd’hui du travail synchrone dans leur corps async. Le mécanisme est mesuré localement : dix appels comportant chacun 10 ms d’attente injectée retardent le témoin de 104,527 ms en médiane, contre 0,351 ms sans cette attente. Ce n’est ni un percentile HTTP ni une estimation du gain du patch.

Proposition locale : capturer identité et contexte de requête, puis déporter l’unité complète BatchRunner/UoW/fournisseur/journal dans le threadpool existant. Garder les redirections, messages et erreurs. Chaque session doit naître, être utilisée et se fermer dans le même thread ; contexte de corrélation propagé et nettoyé. Aucun ajout de service, worker ou pool.

Le bénéfice plausible est la progression de la boucle pendant l’attente du batch. La durée du batch et la capacité totale peuvent rester identiques ; le threadpool et le pool SQL restent des ressources limitées. Catégorie A proposée pour les seuls quatre handlers, avec risque faible si ces frontières sont préservées ; une extension de périmètre se requalifie en B.

Preuves requises après autorisation : quatre routes en succès/échec, permissions et identité inchangées, réponse 303 et messages, corrélation, thread des sessions, témoin/scan simultané avec fournisseur double lent. Couvrir aussi déconnexion/annulation du client : une réponse absente n’autorise pas à renvoyer une communication. Mesurer ensuite les attentes threadpool/SQL sur cible isolée. Retour arrière : changement local réversible après fin des unités en cours, sans annuler les effets métier ; retour au risque initial explicitement signalé.

OPT-03 reste B malgré son effort S : progression, identité de relance et concurrence PostgreSQL demandent une preuve dédiée. OPT-02 reste B : un simple arrêt du lot après réservation ne suffit pas. Le spool CSV, les agrégats, les budgets S3 et la séparation Stripe ont plusieurs contraintes de compatibilité ; ils ne sont pas promus artificiellement en quick wins.

Aucun autre A ne découle de la suppression des contrôles d’intégrité, de révocation, d’audit, de preuve de tirage ou des limites existantes. Aucun quick win exécuté à cette étape.
