# PRO-005 — Résolution des QR dans un corps authentifié

Le frontend Commerçants utilise POST `/protected/animation-locale/commercants/me/participants/resoudre`, avec Bearer de scope `commercant:validation` et JSON `{"qr_token":"…"}` (20 à 512 caractères, champs supplémentaires interdits). Aucun QR dans l'URL technique. La résolution applique le rate limit existant sur une empreinte et renvoie `Cache-Control: private, no-store`.

Le service vérifie la validité/révocation/expiration du token puis l'appartenance du commerce à la configuration publiée. Il expose uniquement le nom de l'animation/commune, la référence participant et l'étape du commerce connecté. Aucun email, nom de participant, token ou QR URL n'est renvoyé. Les identifiants commerçant du client sont refusés. Un commerce étranger reçoit 404 selon le gestionnaire d'exceptions global. Cette lecture ne consomme aucun droit ; POST validations conserve tous ses contrôles atomiques.

Le scan coffret utilise l'endpoint existant POST `/protected/exploitation/validation/ouvrir-transaction` avec JSON `qr_coffret_instance`. L'ancien paramètre query reste temporairement compatible côté backend pour les autres clients ; il n'est plus utilisé dans cette application.

Déploiement : backend d'abord, frontend ensuite ; aucun fallback par URL. Le lien public participant demeure disponible pour le bénéficiaire et n'est plus appelé par l'application Commerçants. Les accès et proxys doivent continuer de masquer les tokens dans les anciennes routes publiques et ne pas journaliser les corps de scans. Formation : identifier un participant par sa référence, scanner à nouveau pour une nouvelle transaction, contrôler le résultat serveur avant de remettre une prestation.

Tests : `tests/security/test_merchant_animation_scan.py` et `test_validation_qr_body.py`. Complète les conventions API Epic 41 et l'exploitation des Epics 2/5 sans rouvrir leur statut produit.
