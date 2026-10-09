# PRO-005 — Résolution des QR dans un corps authentifié

Le frontend Commerçants utilise POST `/protected/animation-locale/commercants/me/participants/resoudre`, avec Bearer de scope `commercant:validation` et JSON `{"qr_token":"…"}` (20 à 512 caractères, champs supplémentaires interdits). Aucun QR dans l'URL technique. La résolution applique le rate limit existant sur une empreinte et renvoie `Cache-Control: private, no-store`.

Le service vérifie la validité/révocation/expiration du token puis l'appartenance du commerce à la configuration publiée. Il expose uniquement le nom de l'animation/commune, la référence participant et l'étape du commerce connecté. Aucun email, nom de participant, token ou QR URL n'est renvoyé. Les identifiants commerçant du client sont refusés. Un commerce étranger reçoit 404 selon le gestionnaire d'exceptions global. Cette lecture ne consomme aucun droit ; POST validations conserve tous ses contrôles atomiques.

Le scan coffret utilise l'endpoint existant POST `/protected/exploitation/validation/ouvrir-transaction` avec JSON `qr_coffret_instance`. L'ancien paramètre query reste temporairement compatible côté backend pour les autres clients ; il n'est plus utilisé dans cette application.

Déploiement : backend d'abord, frontend ensuite ; aucun fallback par URL. Le lien public participant demeure disponible pour le bénéficiaire et n'est plus appelé par l'application Commerçants. Les accès et proxys doivent continuer de masquer les tokens dans les anciennes routes publiques et ne pas journaliser les corps de scans. Formation : identifier un participant par sa référence, scanner à nouveau pour une nouvelle transaction, contrôler le résultat serveur avant de remettre une prestation.

Tests : `tests/security/test_merchant_animation_scan.py` et `test_validation_qr_body.py`. Complète les conventions API Epic 41 et l'exploitation des Epics 2/5 sans rouvrir leur statut produit.


## Lisibilité du résultat Coffret — 9 octobre 2026

Évolution **PRO-SCAN-20261009-ETATS**, commune au responsable et au salarié E72.
L’objectif est de comprendre immédiatement si une prestation du commerce peut
être validée et si la dernière action a réellement été prise en compte.
La couleur complète un libellé explicite et une icône ; elle ne porte jamais
seule l’information. Le résumé concerne les prestations du commerce connecté,
pas la consommation globale du coffret chez tous ses partenaires.

| Situation observée | Présentation attendue | Action |
| --- | --- | --- |
| Prestation du commerce disponible selon l’état serveur | Vert, « À valider » ; nom de la prestation visible | Un bouton de validation explicite par prestation ; le scan seul ne valide rien |
| Aucune prestation attribuée au commerce dans la réponse serveur | Rouge, « Aucune prestation pour votre commerce » | Aucune validation proposée ; possibilité de scanner un autre QR |
| Prestation déjà validée | Bleu, « Déjà validée » | Aucun nouveau bouton de validation ; droits d’annulation du responsable inchangés |
| Commande en cours | « Validation en cours… », retour visuel immédiat | Boutons de commande désactivés, aucun double envoi |
| Réponse serveur confirmant le succès | Bleu, « Validation confirmée » | Confirmation distincte d’un simple état disponible ; aucune nouvelle validation implicite |
| Réponse perdue ou résultat incertain | Ambre, « Résultat à vérifier » | Lecture du résultat serveur avant toute nouvelle commande ; jamais de succès local supposé |
| Prestation expirée, annulée ou état non reconnu | Indisponibilité explicitée | Aucun vert ni bouton prétendant que la prestation est validable |

Pour plusieurs prestations, chacune conserve son état et sa commande. Le résumé
ne prétend pas que tout le coffret est validé après une seule prestation.
Une erreur réseau ou un QR inutilisable ne devient pas artificiellement une
absence de prestation. La projection salariée reste limitée au commerce, sans
montants, coordonnées client ou actions réservées au responsable.

Les règles de consommation, d’autorisation et d’idempotence appartiennent au
backend et restent inchangées. Périmètre applicatif : Localeo Pro et documentation.
Aucun changement de contrat API, migration, configuration ou générateur : les
réponses existantes alimentent les états de présentation. Les preuves attendues
couvrent les trois couleurs demandées, les prestations multiples, l’attente, la
confirmation et le résultat incertain, avec rendu mobile à 320 et 390 pixels.
Le [bilan E72](../epic-72-acces-salaries/verification-livraison.md) consigne les
vérifications exécutées pour les deux profils.
