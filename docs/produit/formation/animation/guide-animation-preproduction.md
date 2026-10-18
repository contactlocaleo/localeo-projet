# Guide de formation — corrections de préproduction Animation

Ce guide accompagne les correctifs ANIM-001 à ANIM-014. Les états affichés
proviennent du backend; le navigateur ne confirme pas un paiement ou un tirage.

## Commune et session

Choisir la commune dans le sélecteur en haut de l'application, puis attendre le
rechargement. Les factures et demandes de deux communes d'un même partenaire
restent séparées. En cas de confirmation réseau perdue, le contexte du serveur
est relu. Une facture historique sans commune doit être traitée par le support.

Le rechargement vérifie la session serveur avant de présenter les vues privées.
Elle expire même si aucune action n'est effectuée. La déconnexion ferme immédiatement
la session locale ; un message indique si le serveur n'a pas confirmé sa révocation.
Après reconnexion, la page demandée reste accessible si les droits le permettent.

## Compte et équipe — évolution E73

Ce parcours fait partie de la [réalisation locale E73](../../../specifications/epic-73-animation-et-ou-coffrets/suivi-implementation.md) ; son ouverture sur un environnement reste une opération distincte.

Depuis la connexion, **Mot de passe oublié** prépare un lien valable une heure. Le même message apparaît que l’adresse corresponde ou non à un compte. Après utilisation, reconnectez-vous avec le nouveau mot de passe ; les anciennes sessions sont fermées. Depuis **Compte et équipe**, le changement de mot de passe exige également votre mot de passe actuel.

Le responsable invite un collaborateur par email, choisit son profil et ses communes parmi celles vérifiées par Localeo, puis attribue séparément les autorisations complémentaires. Le lien d’invitation dure sept jours. Renvoyer une invitation invalide le précédent lien. Un collaborateur ayant déjà un compte se connecte puis accepte explicitement le rattachement ; il garde son compte et ses autres organisations.

Pour la toute première invitation du responsable, Localeo utilise **ERP → Accès Animation → Demandes d’organisation → Invitations initiales**. Si le lien a expiré, le renvoi prépare un nouveau message et invalide l’ancien lien. Il ne confirme ni la réception de l’email ni l’acceptation du responsable.

Pour changer de responsable, proposez le transfert à un collaborateur actif. Vous restez responsable jusqu’à son acceptation. En cas de perte de tous les accès responsables, contactez Localeo : la récupération exige une vérification d’identité et d’autorité, enregistrée dans l’ERP.

Le choix d’organisation recharge le contexte ; vérifiez ensuite la commune avant de travailler. Un compte sans commune accessible peut accepter une invitation et gérer son mot de passe, mais n’ouvre aucun écran métier. Une erreur réseau sur une commande laisse son résultat incertain : actualisez les informations avant de confirmer une reprise. Le simple clic ne prouve pas l’enregistrement.

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

## Dotation libre et remise externe — évolution E73, lot 04

Ce parcours est réalisé et vérifié localement ; son ouverture sur un environnement
reste distincte. À la création, choisir explicitement **Coffrets** ou **Lots libres**,
puis **Gestion externe** pour les lots remis hors Localeo. Aucun choix n’est précoché.
Les bons numériques seront complétés au lot 05.

Dans la dotation, renseigner pour chaque lot son libellé, sa quantité, le responsable
de la remise et les consignes du gagnant. Mettre les lots dans l’ordre d’attribution
souhaité. Les consignes et le responsable sont réservés au suivi autorisé et au
gagnant ; la fiche publique présente les libellés et quantités. Les listes sont
paginées : passer à la page suivante pour voir les autres lots.

Le choix reste modifiable en brouillon tant qu’aucun engagement ne le bloque.
La publication fige le mode et l’ordre ; elle ne demande pas de paiement Coffrets
pour une dotation libre. Un paiement Coffrets ancien reçu après un changement de
mode reste à rapprocher par Localeo, sans transformer la dotation libre.

Après clôture, ouvrir l’animation puis son suivi des lots. Le tirage prépare les
gagnants et les suppléants en arrière-plan. **En préparation** ne confirme aucune
attribution : attendre le résultat enregistré et l’actualiser si la réponse a été
perdue. Un même participant reçoit au maximum un lot. En cas de candidats
insuffisants, le surplus reste non attribué.

Pour chaque gain, distinguer trois informations : l’attribution, l’état réel de
l’email et le suivi de remise. Le gagnant reçoit les consignes et un lien de
consultation ; aucun QR de consommation ni compte commerçant n’est imposé pour
une remise externe. **Email envoyé** ne signifie jamais **Lot remis**. Un échec
de préparation du mail se reprend depuis le même gain.

Consigner le contact, la réponse, le refus, l’incident ou la remise déclarée.
Une correction référence l’événement erroné et conserve son historique. Pour un
gagnant injoignable, le remplacement est possible après quatorze jours depuis le
premier email envoyé avec succès ; un refus explicite permet de le faire plus tôt.
Confirmer le remplacement pour utiliser le premier suppléant encore éligible.
Si la réserve est épuisée, le retirage est une action distincte et explicite.
Un lot dont la remise reste déclarée ne peut pas être réattribué.

La rubrique générale **Tirages Coffrets** conserve son périmètre historique.
Les tirages libres sont accessibles depuis la fiche de chaque animation ; leur
intégration à une liste globale commune est prévue au lot 09.

## Préparer le terrain d’une chasse

La rubrique **Terrain** distingue les préparatifs de votre équipe et ceux des commerces :

1. **Supports des lieux publics** : préparer et télécharger les QR à installer
   dans les lieux publics du parcours. Ce bloc disparaît s’il n’y en a aucun.
2. **Préparation des participants** : consulter les commerces qui se sont déclarés
   prêts, si ce suivi a été activé. Ouvrir le détail seulement si nécessaire.

Chaque commerçant reçoit les supports de son étape dans son kit et les installe
lui-même. Vous n’avez aucun QR commerce à créer ni à confirmer à sa place.
Une erreur de chargement demande une actualisation ; elle ne signifie pas que
le parcours ne contient aucun lieu public.

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
