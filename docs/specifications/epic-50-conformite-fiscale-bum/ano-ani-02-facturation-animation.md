# ANO-ANI-02 — Facturation par animation

## Interface implémentée

Recherche par nom ou référence, résolution de la commande de lots sans saisie
d’UUID, remise à zéro de la sélection au changement d’animation, profil de
facturation prérempli et complété (Chorus conditionnel), clé de tentative liée
à la commande, sélection et profil. Les réponses tardives sont ignorées.

Les réponses backend sont adaptées depuis `requestSnapshot.commandeId`,
`lines`, `prestationSnapshot`, `financialSnapshot`, `previousRequestId`.
Les dossiers regroupent les demandes, les factures téléchargeables et les
relances. Les liens de paiement utilisent `?animationId=...`.

## Complément backend préparé, non appliqué

[ano-ani-02-backend.patch](ano-ani-02-backend.patch) cible `localeo-backend`.
Le contrôle automatique a refusé son application au dépôt voisin faute
d’autorisation explicite de ce périmètre. Aucun fichier backend n’a été modifié
par cette tâche. Le patch ajoute deux services, des tests, une documentation
et deux routes au fichier partagé `app/api/demandes_facture_commercant_api.py`.

Préfixe `/protected/animation-locale/facturation/demandes-groupees` :

- `GET /animations/{animation_id}/dossier` : permission LIRE, partenaire et commune active. Réponse `animationId`, `animationNom`, `summary`, `requests`.
- `POST /{demande_id}/relancer` : permission MODIFIER, même cloisonnement, Idempotency-Key de 8 à 128 caractères. Verrouillage de la demande, délai minimum de 24 heures, rejeu sans nouvel email, audit et outbox dans la même transaction.

Chaque demande expose `canRemind`, `reminderCount`, `lastRemindedAt`,
`nextReminderAt` et le nom du commerçant. Les demandes reçues, annulées ou
remplacées ne peuvent pas être relancées.

La synthèse expose `expectedPrestations`, `executedPrestations`,
`receivedPrestations`, `notExecutedPrestations`, `missingRequests`,
`pendingPrestations`, `lotsMaterialized`, `complete`.

Le dossier est complet uniquement si les lots achetés sont matérialisés,
leurs droits connus et chaque prestation couverte par une facture disponible.
Les validations annulées ne prouvent pas l’exécution. Une correction active
remplace son original ; un avoir seul ne couvre pas la prestation.
Une prestation non exécutée, expirée ou annulée sans couverture garde donc
le dossier incomplet. Aucun acquittement comptable automatique n’est inventé.

Sans le nouveau contrat serveur, l’interface conserve les demandes connues et
affiche « Couverture à vérifier » ; elle ne propose pas de relance non autorisée.

## Validation

Tests frontend : résolution animation/commande, absence et incohérence,
rattachement, demandes non rattachées, concurrence bornée, progression et
corrections, snapshots, profil transmis, synthèse serveur, contrat de relance.

Douze tests du backend préparé exécutés sans modifier le dépôt cible :
couverture partielle, lots non matérialisés, documents manquants/annulés,
corrections et avoirs, délai, cloisonnement, rejeu idempotent, outbox et audit.

Navigateur sur données fictives : recherche, préremplissage, création du
dossier, détail, relance et disparition du bouton après relance. Aucun envoi
réel. Recette intégrée à effectuer après application et déploiement du backend.
