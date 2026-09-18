# Plan d'actions du BackOffice avant production

Ce lotissement découle de l'[audit BackOffice du 21 août 2026](audit-backoffice-preproduction-2026-08-21.md).

Hypothèse retenue : le backoffice sera utilisé au lancement par un seul administrateur, le fondateur de Localeo. La gestion de plusieurs comptes administrateurs et le RBAC ne font donc pas partie du chemin critique de mise en production.

## Vue d'ensemble

| Ordre | Lot | Objectif | Priorité | Effort estimatif | Bloque la PROD |
| ---: | --- | --- | --- | --- | --- |
| 0 | Sécurisation des données métier | Empêcher les modifications directes dangereuses | P0 | Faible à moyen | Oui |
| 1 | Traçabilité des corrections | Pouvoir expliquer toute intervention sensible | P0 | Moyen | Oui |
| 2 | Fiabilité des déploiements | Garantir que le schéma est compatible avec le code | P0 | Moyen | Oui |
| 3 | Recette et procédures de lancement | Valider les parcours critiques en conditions réelles | P0 | Moyen | Oui |
| 4 | Dashboard commercial et alertes | Piloter l'activité et les actions du jour | P1 | Moyen | Non, fortement recommandé |
| 5 | Pilotage multi-territoires | Rester efficace avec 10 à 20 territoires | P1 | Moyen | Non, avant montée en charge |
| 6 | Support et navigation transverse | Réduire le temps de diagnostic des incidents | P1/P2 | Moyen | Non |
| 7 | UX et qualité du menu | Simplifier et fiabiliser l'usage quotidien | P2 | Faible | Non |
| 8 | Préparation multi-opérateurs | Préparer l'arrivée d'une seconde personne | P2 | Moyen | Non au lancement |

## Lot 0 — Sécurisation des données métier

### Objectif

Supprimer le risque qu'une donnée financière ou transactionnelle soit modifiée ou supprimée directement par un formulaire SQLAdmin.

### Actions

1. Passer en lecture seule les vues suivantes :
   - achats ;
   - paiements client ;
   - coffrets instances ;
   - statuts de prestations d'une instance ;
   - transactions et validations de consommation ;
   - comptes et mouvements de reversement ;
   - reversements et lignes de reversement.
2. Déclarer explicitement `can_create = False`, `can_edit = False` et `can_delete = False` sur ces vues.
3. Conserver uniquement les actions métier existantes :
   - réconciliation d'un achat ;
   - renvoi de confirmation ;
   - régénération ou révocation de liens et QR ;
   - remboursement ;
   - annulation contrôlée d'une validation ;
   - exécution des reversements par le workflow prévu.
4. Identifier les corrections encore réalisées par édition de ligne et leur créer une action métier dédiée.
5. Ajouter un test automatisé vérifiant que toutes les vues transactionnelles sont non modifiables.

### Critères de sortie

- aucune écriture financière ne peut être modifiée ou supprimée depuis un formulaire générique ;
- chaque intervention autorisée passe par un cas d'usage métier ;
- les parcours de consultation et les actions existantes restent accessibles.

## Lot 1 — Traçabilité des corrections sensibles

### Objectif

Pouvoir répondre à « qui, quoi, quand, avant, après et pourquoi ? » pour chaque intervention manuelle.

### Actions

1. Définir la liste des actions sensibles : remboursement, annulation de validation, changement d'expiration, suspension commerçant, correction de statut, reprise d'un envoi et correction financière.
2. Imposer un motif métier pour chaque action de correction.
3. Enregistrer dans `evenements_audit` :
   - l'état avant ;
   - l'état après ;
   - le motif ;
   - la ressource concernée ;
   - l'identifiant de corrélation ;
   - l'administrateur configuré.
4. Afficher ces informations dans la fiche d'audit et les visions 360.
5. Vérifier que l'échec d'écriture de l'audit d'une opération critique remonte une alerte exploitable.
6. Ajouter des tests pour chaque action sensible.

### Critères de sortie

- chaque correction critique possède un motif et un événement d'audit complet ;
- l'historique est consultable sans ouvrir les logs ;
- aucune donnée secrète ou personnelle excessive n'est copiée dans les métadonnées d'audit.

## Lot 2 — Fiabilité des migrations et du déploiement

### Objectif

Éviter qu'une vue du backoffice tombe en erreur après déploiement à cause d'une colonne ou d'un index absent.

### Actions

1. Exécuter les migrations SQL dans une étape `pre-deploy` Render.
2. Conserver un historique des migrations appliquées avec checksum.
3. Ajouter un contrôle de schéma au readiness : tables, colonnes et index critiques.
4. Faire échouer le déploiement si une migration échoue.
5. Tester les migrations sur :
   - une base neuve ;
   - une copie anonymisée d'une base historique ;
   - une base partiellement migrée.
6. Documenter le rollback applicatif et la restauration de base.
7. Ajouter un contrôle spécifique des tables achats, reversements, audit et Localeo Live.

### Critères de sortie

- le code applicatif ne démarre pas sur un schéma incompatible ;
- les migrations sont automatiques, ordonnées et idempotentes lorsque nécessaire ;
- une procédure de restauration testée est disponible.

## Lot 3 — Recette et procédures de lancement

### Objectif

Valider le backoffice avec des données représentatives avant le GO PROD.

### Actions

1. Préparer un jeu de données couvrant deux territoires, plusieurs commerçants et les principaux statuts.
2. Recetter les visions 360 :
   - client ;
   - commerçant ;
   - coffret ;
   - reversements ;
   - animation.
3. Simuler les sept incidents décrits dans l'audit.
4. Tester les batchs, leur idempotence et leur reprise après erreur.
5. Tester un remboursement avant transfert et un incident après transfert.
6. Valider la politique du reliquat à expiration.
7. Tester la restauration de la base et la reprise PSP.
8. Rédiger une procédure quotidienne courte et une procédure d'escalade Stripe.

### Critères de sortie

- chaque scénario possède un résultat attendu et une preuve de recette ;
- aucune opération courante ne nécessite un accès direct à la base ;
- les procédures d'urgence sont accessibles depuis le backoffice ou la documentation d'exploitation.

## Lot 4 — Dashboard commercial et alertes actionnables

**État : implémenté.** Les indicateurs temporels, comparaisons, classements et alertes actionnables sont disponibles dans le dashboard opérationnel. Les définitions de calcul sont documentées dans [docs/ops/dashboard-commercial-backoffice.md](../../architecture/backend/backoffice/dashboard-commercial-backoffice.md).

### Objectif

Comprendre l'état de Localeo en moins de 30 secondes et savoir quoi traiter.

### Actions

1. Ajouter les périodes Aujourd'hui, 7 jours et 30 jours.
2. Afficher :
   - CA encaissé ;
   - nombre de commandes ;
   - coffrets vendus ;
   - panier moyen ;
   - comparaison avec la période précédente ;
   - commissions Localeo générées.
3. Ajouter les coffrets les plus vendus et commerçants les plus actifs.
4. Ajouter l'alerte « coffrets expirant bientôt avec reliquat ».
5. Ajouter les remboursements et WebPush en erreur.
6. Faire pointer chaque carte d'alerte vers une liste déjà préfiltrée.
7. Distinguer visuellement indicateurs, alertes et actions de batch.

### Critères de sortie

- les chiffres commerciaux sont cohérents avec les achats payés ;
- une carte d'alerte ouvre directement les enregistrements concernés ;
- aucun indicateur financier ne mélange euros et centimes.

## Lot 5 — Pilotage multi-territoires

**État : implémenté.** Le territoire actif est conservé en session, affiché sur le dashboard et appliqué aux principales listes commerciales, transactionnelles et financières. Les règles de rattachement sont documentées dans [docs/ops/pilotage-multi-territoires-backoffice.md](../../architecture/backend/backoffice/pilotage-multi-territoires-backoffice.md).

### Objectif

Conserver un backoffice utilisable lors du passage à 10–20 territoires.

### Actions

1. Ajouter un sélecteur territorial persistant dans le backoffice.
2. Prévoir l'option « Tous les territoires » pour l'administrateur unique.
3. Propager le filtre au dashboard et aux listes principales : commerçants, coffrets, achats, instances, consommations et finance.
4. Afficher systématiquement le territoire dans les résultats transverses.
5. Ajouter les statistiques commerciales et financières par territoire.
6. Tester l'absence de confusion entre deux objets portant des noms similaires sur des territoires différents.

### Critères de sortie

- le territoire actif est toujours visible ;
- les indicateurs et listes utilisent le même périmètre ;
- le retour à « Tous les territoires » est explicite.

## Lot 6 — Support et navigation transverse

**État : implémenté.** La recherche globale alimente une chronologie unifiée et les principales ressources disposent de liens contextuels. La fiche commerçant prévisualise l'impact d'une suspension ou d'un archivage. Voir [docs/ops/support-navigation-transverse-backoffice.md](../../architecture/backend/backoffice/support-navigation-transverse-backoffice.md).

### Objectif

Réduire le temps nécessaire pour diagnostiquer une réclamation client ou commerçant.

### Actions

1. Construire une chronologie unifiée : commande → paiement → instance → activation → consommation → reversement → communication.
2. Ajouter des liens directs :
   - validation vers mouvement attendu ;
   - mouvement vers paiement de reversement ;
   - achat vers paiement, instance, email et remboursement ;
   - instance vers consommations et audit.
3. Ajouter une recherche globale acceptant : email, téléphone, référence achat, identifiant instance et référence PSP.
4. Ajouter une explication métier des statuts et blocages.
5. Créer une prévisualisation d'impact avant suspension ou fermeture d'un commerçant.

### Critères de sortie

- les incidents 1 à 3 de l'audit sont diagnostiqués depuis un seul point d'entrée ;
- aucune référence technique ne doit être copiée manuellement entre plusieurs écrans.

## Lot 7 — UX et qualité du menu

**État : implémenté.** Les doublons Animation ont été supprimés et un garde-fou impose l'unicité des BaseView. Les badges, libellés, tableaux et messages d'action suivent les conventions décrites dans [docs/ops/ux-menu-backoffice.md](../../architecture/backend/backoffice/ux-menu-backoffice.md).

### Objectif

Réduire les erreurs de manipulation et la charge cognitive.

### Actions

1. Supprimer les enregistrements dupliqués des BaseView Animation.
2. Ajouter un test garantissant l'unicité des entrées de menu.
3. Harmoniser les libellés français des statuts et actions.
4. Utiliser une palette de badges cohérente pour succès, attente, avertissement, erreur et archivage.
5. Revoir les tableaux trop larges et déplacer les informations secondaires dans le détail.
6. Vérifier les confirmations des actions irréversibles.
7. Uniformiser les messages de succès et d'erreur avec une référence de corrélation.

### Critères de sortie

- aucune entrée de menu n'est dupliquée ;
- une même notion possède le même libellé et la même couleur partout ;
- les actions dangereuses sont clairement distinguées des actions de consultation.

## Lot 8 — Préparation multi-opérateurs

### Déclencheur

Ce lot doit être réalisé avant de donner accès au backoffice à une deuxième personne, y compris un prestataire.

### Actions

1. Mettre en place une authentification OIDC.
2. Créer des comptes nominatifs.
3. Définir les rôles Admin, Finance, Support et Exploitation.
4. Restreindre vues et actions selon les rôles.
5. Permettre la révocation immédiate d'un accès.
6. Ajouter une authentification multifacteur via le fournisseur d'identité.
7. Vérifier que l'audit stocke l'identité réelle de chaque opérateur.

### Critères de sortie

- aucun compte n'est partagé ;
- chaque action est attribuable à une personne ;
- les actions financières sont réservées aux rôles autorisés.

## Ordonnancement recommandé

```text
Lot 0 ──> Lot 1 ──> Lot 3 ──> décision GO PROD
   └────> Lot 2 ──────┘

Lot 4 ──> Lot 5 ──> Lot 6 ──> Lot 7

Lot 8 : avant l'arrivée d'un second opérateur
```

Les lots 0, 1 et 2 peuvent être développés en parallèle, mais le lot 3 doit valider leur résultat commun. Les lots 4 et 7 peuvent être engagés avant la production si la capacité le permet ; ils ne doivent pas retarder la sécurisation des données et des déploiements.

## Décision de passage en production

Le passage en production peut être réévalué lorsque :

- les lots 0, 1 et 2 sont terminés ;
- le lot 3 ne révèle aucun incident bloquant ;
- le compte administrateur est personnel, son secret est stocké hors du dépôt et une procédure de rotation existe ;
- les sauvegardes et la restauration ont été testées ;
- la politique d'expiration et de reliquat est validée.
