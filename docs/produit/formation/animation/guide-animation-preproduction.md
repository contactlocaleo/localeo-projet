# Guide de formation — corrections de préproduction Animation

Ce guide accompagne les correctifs ANIM-001 à ANIM-014. Les états affichés
proviennent du backend; le navigateur ne confirme pas un paiement ou un tirage.

## Commune et session

Choisir la commune dans le sélecteur en haut de l'application, puis attendre le
rechargement. Les factures et demandes de deux communes d'un même partenaire
restent séparées. En cas de confirmation réseau perdue, le contexte du serveur
est relu. Une facture historique sans commune doit être traitée par le support.

La session n'est pas conservée après un rechargement complet. Elle expire même
si aucune action n'est effectuée. La déconnexion ferme immédiatement la session
locale; un message indique si le serveur n'a pas confirmé sa révocation.
Après reconnexion, la page demandée reste accessible si les droits le permettent.

## Préparer et publier une animation

Après une erreur réseau de création, réessayer avec le formulaire inchangé :
la même clé retrouve le même brouillon. Une modification constitue une nouvelle
intention. Le double clic est bloqué et le serveur garantit l'idempotence.

Le seuil correspond au nombre de commerçants distincts à visiter. Quatre
validations sur dix commerçants suffisent pour un seuil de quatre. Une seule
validation effective par commerçant est possible. Le serveur refuse la publication
si les commerçants ayant accepté ne permettent pas d'atteindre ce seuil.
Les règles historiques canoniques ne sont pas changées rétroactivement.

Les jours sont exprimés en Europe/Paris. Le dernier jour choisi est inclus :
une animation se termine au minuit suivant. Un changement d'heure ne rajoute ni
ne supprime une journée du calendrier. Les échéances de réponse commerçant restent
valables pendant toute la journée choisie à Paris.

## Préparer le terrain d’une chasse

La rubrique **Terrain** se limite à deux points :

1. **Supports à installer** : préparer et télécharger les QR des lieux du parcours.
2. **Préparation des participants** : consulter les commerces qui se sont déclarés
   prêts, si ce suivi a été activé. Ouvrir le détail seulement si nécessaire.

Il n’y a plus de checklist obligatoire, de fiche de visite ni de confirmation
à saisir pour chaque mission. Le guide pratique reste disponible à la demande.
Accepter de participer, déclarer son commerce prêt et publier l’animation restent
des actions distinctes. La jauge indique les préparatifs réellement nécessaires.

## Payer, suivre et clôturer

Après un retour Stripe ou un timeout, consulter la commande existante. Attendre
la confirmation serveur et les lots réservés. Un financement intégral par crédit
ne passe pas par Stripe; la capture est contrôlée côté backend. L'état
A_RECONCILIER nécessite le support, sans forcer de statut ni créer un nouvel achat.

Le live se recharge toutes les 15 secondes lorsque l'onglet est visible. Une
interruption d'actualisation est signalée avec les dernières données reçues.
La clôture fige les participants éligibles; un scan, une annulation ou une édition
en attente ne peut pas ensuite rouvrir l'animation ou altérer la population figée.

Pour une opération asynchrone, PENDING/RUNNING signifie qu'elle est encore en
cours. Seul SUCCEEDED permet d'annoncer le succès. Si l'attente dépasse la durée
de suivi, consulter l'état avant de relancer.

## Documents et exports

Une erreur de chargement des documents est distincte de l'absence de documents.
Les exports validations et bilans téléchargent les données réelles parcourues
sur toutes les pages de l'API. Le préfixe `Texte: ` neutralise les cellules
susceptibles d'être interprétées comme formules, y compris un téléphone avec +.
Les données sources restent intactes. Les journaux techniques n'incluent pas
les coordonnées, les corps d'erreur, les tokens ou les QR.

## Scénarios de recette avant activation

| Scénario | Résultat attendu |
| --- | --- |
| Deux communes du même partenaire | Refus des accès croisés, fichiers compris |
| Profil lecture puis gestion | Mutations refusées/autorisées par le serveur selon les droits |
| Réponse de création perdue, puis rejeu | Un seul brouillon |
| Crédit intégral puis rejeu | Une seule capture, aucun checkout Stripe |
| Deux scans simultanés | Deux validations distinctes, progression exacte |
| Scan ou édition pendant clôture | Population figée cohérente, aucune réouverture |
| 101 participants ou validations | Tous les éléments accessibles |
| Onglet masqué puis réouvert | Pause puis reprise du live |
| Fin au changement d'heure | Journées locales correctes, fin exclusive |
| Réseau coupé pendant logout | Session locale fermée, absence de fausse confirmation serveur |
| Job en attente ou en échec | Aucun succès prématuré |

Consigner l'environnement, les versions, le compte de recette, les résultats et
les références de corrélation sans enregistrer de credentials. Les preuves locales
sont dans le [suivi de remédiation](../../../audits/animation/remediation-2026-09-06.md).
