# BACK-001 — Autoriser la révocation de session

Constat du 7 septembre 2026 : l'endpoint de révocation acceptait un ID sans principal authentifié. Un appelant connaissant un ID pouvait déconnecter un autre commerçant. Correction : Bearer avec scope commercant:session et politique de domaine exigeant que la session cible appartienne au commerçant authentifié. L'absence, le mauvais propriétaire ou une session déjà révoquée produisent une erreur générique sans mutation. La signature du cas d'usage exige le propriétaire vérifié. Aucune migration SQL. Le frontend fournit déjà le Bearer avant d'effacer sa copie locale (l'appel conserve la valeur capturée).

Tests : test_merchant_session_revocation.py et test_identite_acces_use_cases.py. Complète Epic 10 et PRO-004. Les opérations d'administration éventuelles doivent utiliser leur propre autorisation explicite, sans exposer ce cas d'usage anonymement.

Validation complémentaire BACK-001 : `tests/integration/test_merchant_double_consumption.py` exerce deux transactions simultanées sur la même prestation, avec PostgreSQL réel et UoW/repositories applicatifs. Résultat : une seule occurrence de validation et un seul mouvement financier. Test réussi le 7 septembre 2026. Les schemas de test sont uniques et jetables ; aucune base métier n'est utilisée.
