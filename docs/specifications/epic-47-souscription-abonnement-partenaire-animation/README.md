# Epic 47 — Conception de la souscription partenaire Animation

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-47-souscription-abonnement-partenaire-animation-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Etat

`Termine`. Cloture produit confirmee par l'utilisateur le 15 septembre 2026.
Le cadrage et les arbitrages sont valides. Le socle BDD, la commande consolidee,
Checkout, le webhook d'activation, les emails et le pilotage sont implementes
avec la migration `v215` et les evolutions suivantes. La procedure de recette
reste disponible pour l'exploitation ; aucune nouvelle recette Stripe reelle
n'est attestee par cette mise a jour documentaire.

## Objet

Ce dossier initialise la conception backend et back-office nécessaire pour
tarifer, faire payer et activer l'abonnement d'un partenaire Localeo Animation.

La source produit est
[`epic-47-souscription-abonnement-partenaire-animation-backlog.md`](../../roadmap/terminees/epic-47-souscription-abonnement-partenaire-animation-backlog.md).
Les décisions non encore validées sont centralisées dans le
[`registre des arbitrages`](registre-arbitrages.md).

## Besoin retenu

Deux offres catalogue sont disponibles :

| Code | Prix HT initial | Contenu |
|---|---:|---|
| `DECOUVERTE` | 390,00 € | Une animation clé en main |
| `ESSENTIELLE` | 708,00 € | Plateforme pendant un an, animations illimitées |

Le prix catalogue est paramétrable. Lors du référencement, l'administrateur
peut saisir un prix propre à la souscription, y compris `0 €`, pour une
promotion, un pilote ou une gratuité. Le prix et le motif sont snapshotés.

Une souscription payante est activée uniquement après confirmation Stripe. Une
souscription gratuite est activée par une décision administrative explicite et
auditée, sans transaction fictive.

## Décisions produit validées

- Essentielle est un paiement unique prépayé ouvrant douze mois de droits, sans
  renouvellement automatique.
- Découverte est utilisable pendant douze mois ; son crédit est consommé à la
  première publication réussie et n'est pas restitué après publication. Toute
  consommation ou réservation encore rattachée à un brouillon annulé avant le
  paiement des lots est toutefois libérée.
- Découverte utilise un modèle clé en main administrable ; les lots restent
  financés séparément par l'Epic 46.
- Le prix s'applique à un couple **partenaire + commune**. Une souscription
  porte une seule commune, même si le référencement en sélectionne plusieurs.
- HT, taux de TVA, montant de TVA et TTC sont snapshotés.
- Le prix Localeo snapshoté fait autorité pour Stripe ; toute différence au
  catalogue est motivée et auditée par l'administrateur.
- Le contact de facturation peut être distinct du premier gestionnaire.
- L'invitation portail est envoyée après paiement ou gratuité validée.
- Un lien expiré est régénéré sur le même snapshot ; changer le prix impose une
  nouvelle souscription.
- Les remboursements automatiques et changements d'offre sont hors MVP.
- Après paiement, une preuve est envoyée au contact de facturation et conservée
  dans un dossier permettant la production d'une facture conforme ; son format
  fiscal doit être validé avant la mise en production.
- Le suivi du CA distingue abonnements encaissés HT, TTC, frais Stripe et nombre
  de gratuités ; la date de rattachement est `paid_at`.
- La date de fin est visible dans la section abonnement. Le back-office et
  Localeo Animation signalent les abonnements approchant de l'expiration.

## Frontières de domaine

| Domaine | Responsabilité |
|---|---|
| `animation_locale` | Consommer le droit, contrôler la création/publication et le quota |
| `abonnements_plateforme` | Catalogue, souscription, prix, activation, durée, quota et événements Stripe |
| `identite_acces` | Préparer puis ouvrir l'accès du gestionnaire après activation |
| `exploitation` | Emails, audit, suivi du CA, alertes et procédures |
| Adaptateur Stripe | Créer Checkout, valider les signatures et lire les objets Stripe |

Le domaine `animation_locale` ne doit connaître ni Checkout Session, ni
PaymentIntent, ni calcul de TVA. Il demande seulement si une action est
autorisée et, pour l'offre Découverte, consomme un quota par un use case
idempotent.

## Challenge du modèle existant

Le modèle actuel confond la décision commerciale et le droit actif :
`ActiverAbonnementAdministrativement` crée immédiatement un
`AbonnementPlateforme.ACTIF` pendant le référencement.

Ajouter simplement `EN_ATTENTE_PAIEMENT` à `AbonnementPlateforme` rendrait le
port de droits plus complexe et mélangerait commande commerciale, paiement et
habilitation. La cible validée introduit donc une racine
`SouscriptionPlateforme` :

- la souscription porte l'offre et les snapshots tarifaires ;
- elle existe avant le paiement ;
- elle porte Checkout et les preuves financières ;
- elle matérialise un abonnement actif pour sa commune après confirmation ;
- l'abonnement reste une projection de droit simple.

## Modèle cible validé

### Évolution de `OffrePlateforme`

| Attribut | Type | Règle |
|---|---|---|
| `prix_catalogue_ht_centimes` | entier | Positif ou nul pour une offre administrativement gratuite |
| `devise` | texte | `EUR` au MVP |
| `duree_mois` | entier nullable | `12` pour Découverte et Essentielle |
| `quota_animations` | entier nullable | `1` pour Découverte, `NULL` pour illimité |
| `modele_service` | texte | `CLE_EN_MAIN` ou `PLATEFORME_AUTONOME` |
| `active` | booléen | Une offre inactive n'est plus souscriptible |

Les champs existants `droits` et `limites` restent disponibles pour les règles
fonctionnelles, mais les données commerciales structurantes ne doivent pas
être dissimulées uniquement dans un JSON.

### Nouvelle racine `SouscriptionPlateforme`

| Groupe | Attributs principaux |
|---|---|
| Identité | `id`, `reference`, `partenaire_id`, `offre_id`, `statut` |
| Périmètre | `commune_id` unique ; prix applicable à ce couple partenaire + commune |
| Catalogue snapshoté | code, libellé, droits, limites, durée et quota |
| Prix | catalogue HT, proposé HT, TVA, TTC, devise |
| Décision commerciale | motif, acteur, date, type `CATALOGUE/REMISE/MAJORATION/GRATUITE` |
| Facturation | raison sociale, contact, email, adresse et identifiants fiscaux utiles |
| Stripe | customer, checkout session, payment intent, charge, statut et URL expirante |
| Dates | création, envoi, expiration Checkout, paiement, activation, annulation |

Les montants du navigateur ne font jamais autorité. Ils sont résolus depuis la
souscription persistée avant l'appel à Stripe.

### Paiement

Le paiement consolidé est porté par `commandes_souscriptions_plateforme`.
Chaque ligne reste une `souscription_plateforme` mono-commune et conserve son
propre snapshot commercial. Ce choix remplace les deux options initialement
étudiées :

1. étendre la table générique `paiements` avec une troisième racine
   `souscription_plateforme_id` et adapter sa contrainte d'unicité de racine ;
2. créer `paiements_abonnements_plateforme`, possédé par le domaine abonnement.

La proposition initiale retient l'extension de `paiements` pour mutualiser les
références Stripe et le suivi financier, à condition de conserver exactement
une racine parmi `achat_id`, `commande_achat_id` et
`souscription_plateforme_id`.

### Quota Découverte

Le quota ne doit pas être calculé par un simple nombre courant d'animations.
Une consommation dédiée et idempotente est nécessaire :

| Attribut | Rôle |
|---|---|
| `abonnement_id` | Droit consommé |
| `animation_id` | Animation ayant consommé le crédit |
| `type_consommation` | `PREMIERE_PUBLICATION_REUSSIE` |
| `consumed_at` | Date de consommation |
| `cancelled_at` | Restitution lors de l'annulation d'un brouillon avant paiement des lots |

Une contrainte unique empêche une animation de consommer deux fois le même
quota lors d'un rejeu. Le compteur d'utilisation ne compte que les lignes dont
`cancelled_at` est nul. L'annulation autorisée d'un brouillon renseigne ce champ
dans la même transaction que l'annulation des invitations et de l'animation.

Les consommations concurrentes sont serialisees par verrou PostgreSQL sur
l'abonnement avant le comptage et l'insertion. Une restitution prend le meme
verrou avant celui de la consommation. La contrainte d'unicite protege le rejeu,
mais ne remplace pas ce verrou portant sur le quota partage (F02). Le credit
est flushe avant une seconde consommation dans la meme transaction.

## Cycle transactionnel

### Souscription payante

1. L'administrateur crée le partenaire, les rattachements territoriaux et le
   premier gestionnaire en attente.
2. Il choisit l'offre et confirme le prix proposé pour chaque commune.
3. Le backend crée une souscription avec ses snapshots par commune.
4. Le backend crée une Checkout Session à partir du prix persisté.
5. L'outbox reçoit un email `PAIEMENT_ABONNEMENT_ANIMATION`.
6. Le partenaire paie sur Stripe.
7. Le webhook signé retrouve la souscription par metadata et références.
8. Le backend vérifie statut, montant, devise et unicité du paiement.
9. La souscription passe à `PAYEE`, puis matérialise l'abonnement et les droits
   de sa commune.
10. L'invitation `INVITATION_GESTIONNAIRE_ANIMATION` est placée dans l'outbox.
11. Le paiement alimente le suivi **Abonnements encaissés**.

### Gratuité

1. L'administrateur saisit `0 €` avec un motif.
2. Une confirmation renforcée rappelle qu'aucun paiement ne sera demandé.
3. La souscription est marquée `GRATUITE_ACTIVEE`.
4. Les abonnements et droits sont matérialisés.
5. L'invitation est envoyée.
6. La souscription compte dans les volumes, mais le montant encaissé reste nul.

## Intégration Stripe

### Création Checkout proposée

```http
POST /internal/abonnements-plateforme/commandes/{commande_id}/checkout
```

Le backend fournit à Stripe :

- le montant TTC calculé et snapshoté ;
- `currency=eur` ;
- le libellé de l'offre ;
- `souscription_id`, `partenaire_id` et `offre_code` dans les metadata ;
- des URLs de succès et d'annulation construites depuis la configuration
  backend et non depuis la requête.

Le mode Stripe validé au MVP est un paiement unique prépayé ouvrant un droit à
durée déterminée, sans renouvellement automatique. Lorsqu'un référencement
couvre plusieurs communes, une commande consolidee porte une ligne par
souscription et produit un paiement Stripe unique.

### Webhook

Le routeur `POST /public/stripe/webhook` doit distribuer les événements de
souscription avant ou à côté des achats et de Stripe Connect.

Événements minimaux :

- `checkout.session.completed` ;
- `checkout.session.expired` ;
- événement de remboursement si le remboursement entre dans le MVP.

Le handler est idempotent sur `stripe_event_id`. Une erreur après confirmation
du paiement place la souscription en `A_RECONCILIER` ; elle ne doit pas créer un
second encaissement lors de la reprise.

#### Atomicite et reprise apres erreur d'activation (F01)

La commande est verrouillee avant traitement. La creation de tous les droits,
habilitations, invitations et confirmations forme une unite atomique : une
erreur annule l'ensemble de ces effets, sans effacer la preuve du paiement.
La trace porte alors le code assaini `ACTIVATION_ECHOUEE` et la commande reste
`A_RECONCILIER`. Seul le rejeu du meme evenement signe, avec le meme contenu,
peut reprendre cette erreur technique. Les incoherences de montant, devise,
session ou annulation ne sont pas reprises automatiquement. Un evenement deja
traite reste sans effet. Aucun detail d'exception sensible n'est persiste.

## Parcours back-office cible

L'écran **Animations locales > Référencer un partenaire** devient un parcours
en cinq étapes :

1. partenaire et contact de facturation ;
2. communes rattachées, chacune portant sa propre souscription ;
3. offre et synthèse de ses droits ;
4. prix catalogue, prix proposé et justification ;
5. premier utilisateur et validation finale.

Après validation :

- si le prix est supérieur à zéro, l'écran affiche le statut en attente, le
  lien Stripe, l'email préparé et les actions **Renvoyer** / **Régénérer** ;
- si le prix est nul, l'écran demande une confirmation puis affiche
  l'abonnement actif et l'invitation préparée ;
- le partenaire est visible dans la Vision 360 avec la souscription, son prix,
  son paiement et ses droits.

Pour un référencement multi-communes, chaque commune conserve son offre, son
prix snapshoté, son abonnement et son affectation de CA propres. La presentation
et le paiement sont consolides dans une commande et une Checkout Session uniques.

L'administration des offres expose les prix catalogue, mais ne doit jamais
autoriser la modification d'un snapshot de souscription payée.

## Emails

### Demande de paiement

Les renvois explicites successifs sont autorises tant que le lien Checkout est
actif. La verification d'existence ne suppose pas un email unique. La
deduplication de l'envoi initial porte sur commande + session Checkout : une
nouvelle session produit toujours son propre email, avec son nouveau lien.
Un lien expire ne peut pas etre renvoye ; il doit d'abord etre regenere (F06).

Le mail contient :

- identité Localeo et partenaire ;
- offre, durée ou quota ;
- prix catalogue HT et prix convenu HT ;
- taux et montant de TVA, total TTC ;
- commune couverte par la souscription ;
- lien Stripe et indication de son expiration ;
- contact support et référence de souscription.

### Invitation portail

La deduplication porte sur le gestionnaire, pas sur son partenaire : chacun
recoit son invitation propre (F07). Le dossier d'invitation conserve le rejeu
sans effet meme si l'email a ete purge. Les anciens emails references par
partenaire ne valent preuve d'envoi que pour leur destinataire exact. Seul un
renouvellement administratif explicite genere un nouveau lien. Emission et
activation verrouillent dans l'ordre gestionnaire puis invitation.

L'invitation est produite seulement après activation. Elle ne doit plus être
créée au moment initial du référencement payant.

Depuis F03, aucun mot de passe initial n'est genere ni conserve dans l'outbox.
L'email contient un lien a usage unique valable 24 heures. Le token aleatoire
est uniquement hashe dans `invitations_gestionnaires_animation` ; sa copie dans
l'email expire et devient inutilisable apres activation. Le portail lit le
fragment `#activation=...`, l'efface de l'URL, puis transmet token et mot de passe
dans le corps de `POST /public/identite-acces/animation/invitations/activer`.
Le backend applique la politique de mot de passe existante (72 octets UTF-8
maximum), refuse les comptes suspendus, consomme le lien sous verrou et revoque
les sessions precedentes dans la meme transaction. Le gestionnaire se connecte
ensuite normalement. Les emails historiques ne sont pas purges automatiquement.

### Confirmation et dossier de facturation

Après confirmation du webhook, l'outbox produit une confirmation contenant la
référence de souscription, la commune, l'offre, les montants HT/TVA/TTC, la
date et la référence Stripe. Cette preuve est conservée dans le dossier
documentaire de la souscription. Elle ne se substitue à une facture conforme
qu'après validation de son format par la comptabilité ou le conseil juridique.

## Suivi du chiffre d'affaires

Le paiement d'abonnement doit être intégré aux deux vues existantes :

- **Dashboard opérationnel > Pilotage commercial** ;
- **Localeo Control**, sur les mêmes périodes.

La projection expose au minimum :

| Indicateur | Définition validée |
|---|---|
| `montant_abonnements_encaisses_ht` | Somme HT des souscriptions payées sur la période |
| `montant_abonnements_encaisses_ttc` | Somme réellement encaissée via Stripe |
| `nombre_abonnements_payes` | Nombre de souscriptions payées distinctes |
| `nombre_abonnements_gratuits` | Gratuités activées, exclues du montant encaissé |
| `ca_coffrets` | Indicateur existant, conservé séparément |
| `frais_stripe_abonnements` | Frais Stripe affichés séparément lorsqu'ils sont disponibles |
| `ca_total_localeo` | Non publié tant que le CA coffrets n'utilise pas une base homogène validée |

Règles :

- date de rattachement : `paid_at` issue du webhook ;
- une souscription et un paiement ne sont comptés qu'une fois ;
- `EN_ATTENTE_PAIEMENT`, Checkout expirée et gratuité ne génèrent aucun CA ;
- ventilation par offre, partenaire et commune ;
- chaque souscription étant rattachée à une seule commune, le filtre communal
  sélectionne directement son encaissement ; le total global déduplique par
  paiement Stripe ;
- un remboursement futur est un mouvement négatif à sa date d'exécution.

L'indicateur **Abonnements encaissés** reste distinct pour rendre la composition
du CA compréhensible. Le total global n'est publié qu'après validation de la
convention comptable commune avec le CA coffrets.

## Expiration et alertes

- `date_fin` est calculée à douze mois de la date d'activation pour Découverte
  et Essentielle ;
- la section abonnement du portail affiche la date de fin ;
- le dashboard opérationnel expose le volume d'abonnements proches de
  l'expiration et un lien vers leur gestion ;
- Localeo Animation affiche une alerte non bloquante avant expiration, puis
  bloque les nouvelles créations/publications après expiration selon les
  droits existants ;
- une alerte est affichee et envoyee par email a J-30, J-7 et a expiration ;
- les destinataires sont le contact de facturation et les gestionnaires actifs,
  apres deduplication des adresses ;
- chaque envoi est idempotent par souscription, seuil et destinataire.

## APIs internes proposées

| Méthode et route | Usage |
|---|---|
| `GET /internal/abonnements-plateforme/offres` | Lister les offres actives et leurs prix |
| `POST /internal/abonnements-plateforme/commandes` | Créer une commande et ses souscriptions snapshotées |
| `GET /internal/abonnements-plateforme/souscriptions/{id}` | Consulter le dossier complet |
| `POST /internal/abonnements-plateforme/commandes/{id}/checkout` | Créer ou reprendre le paiement consolidé |
| `POST /internal/abonnements-plateforme/commandes/{id}/email-paiement` | Renvoyer la demande de paiement |
| `POST /internal/abonnements-plateforme/commandes/{id}/activer-gratuitement` | Valider une gratuité auditée |
| `POST /internal/abonnements-plateforme/souscriptions/{id}/annuler` | Annuler avant paiement |
| `GET /internal/abonnements-plateforme/ca` | Agréger les encaissements par période, offre, partenaire et commune |

Ces routes sont réservées à l'administration. Le parcours public ne reçoit
qu'une page de retour informative ; il ne peut pas activer l'abonnement.

## Configuration proposée

| Clé | Objet |
|---|---|
| `LOCALEO_ANIMATION_SUBSCRIPTION_SUCCESS_URL` | Page informative après paiement |
| `LOCALEO_ANIMATION_SUBSCRIPTION_CANCEL_URL` | Page de retour après abandon |
| `LOCALEO_ANIMATION_SUBSCRIPTION_SUPPORT_URL` | Contact contextualisé en cas de blocage |
| `LOCALEO_ANIMATION_SUBSCRIPTION_EXPIRATION_ALERT_DAYS` | Seuils d'alerte du MVP, par defaut `30,7,0` |

Les prix, taux fiscaux et durées fonctionnelles appartiennent aux données
administrables ou à une configuration fiscale versionnée ; ils ne doivent pas
être dispersés dans des variables d'environnement.

## Sécurité et audit

- seules les sessions administrateur peuvent créer ou modifier une
  souscription ;
- motif obligatoire pour tout écart au catalogue ;
- confirmation renforcée pour la gratuité ;
- metadata Stripe sans donnée personnelle inutile ;
- signature webhook obligatoire ;
- aucun numéro de carte ni secret dans Localeo ;
- audit des prix avant/après, acteur, motif, lien régénéré, email renvoyé,
  activation et réconciliation ;
- journaux assainis et corrélés par `correlationId`.

## Stratégie de tests

- domaine : prix, gratuité, transitions, durée et quota ;
- application : création, Checkout, webhook, activation et idempotence ;
- persistence : contraintes de racine paiement, snapshots et unicité ;
- API : modèles de réponse OpenAPI et erreurs ;
- administration : saisie du prix, motif obligatoire et actions par statut ;
- emails : aucun secret, montants cohérents et lien attendu ;
- CA : paiement unique, période, gratuité, ventilation par commune et absence
  de double comptage global ;
- recette Stripe Test : payé, expiré, refusé, rejoué et activation en erreur.

## Livrables attendus

- migration SQL versionnée ;
- domaine et use cases `abonnements_plateforme` enrichis ;
- adaptateur Checkout et traitement webhook ;
- parcours de référencement et Vision 360 partenaire actualisés ;
- templates email ;
- indicateurs du dashboard opérationnel et Localeo Control ;
- OpenAPI interne modélisé ;
- procédure de reprise et cahier de recette.

La procédure de déploiement, de recette Stripe Test et de reprise est décrite
dans [`procedure-exploitation.md`](procedure-exploitation.md).
# Protection des transitions administratives (F08)

Une commande annulée est terminale : ni Checkout ni activation gratuite ne la réactivent.
Checkout est autorisé uniquement pour EN_ATTENTE_PAIEMENT, PAIEMENT_EN_COURS et EXPIREE.
L'activation gratuite exige GRATUITE_A_ACTIVER ; son replay après GRATUITE_ACTIVEE
retourne le dossier existant sans recréer de droits ou d'emails. A_RECONCILIER reste
réservé au rapprochement, avec la reprise technique contrôlée décrite en F01.
Ces opérations et l'annulation verrouillent la commande avant toute décision.
Un webhook d'expiration tardif ne déclasse pas une commande finalisée.
# Exécution du webhook (F09)

La route lit le corps brut de manière asynchrone puis déporte la validation Stripe
et le traitement transactionnel synchrone dans le pool de threads borné Starlette/AnyIO.
La réponse attend la fin du traitement : aucun acquittement anticipé ni tâche volatile.
Une signature invalide ne déclenche aucun traitement métier ; les erreurs continuent
à remonter via le contrat HTTP existant. Aucune connexion SQL n'est partagée entre threads.
# Rattrapage des échéances (F12)

À chaque passage, le job sélectionne uniquement le seuil le plus récent franchi
(J30, J7 ou J0 par défaut) et peut le rattraper pendant 30 jours après sa date prévue.
Il n'envoie pas simultanément les anciens seuils manqués. La déduplication conserve
la clé abonnement/seuil/destinataire, y compris après expiration. Les abonnements
sont verrouillés, avec passage suivant pour les lignes déjà prises par un autre job.

La mise à jour du statut ne dépend ni d'un seuil configuré, ni de l'existence d'une
souscription ou d'un destinataire. La date de fin est inclusive, conformément au
calcul des droits : J0 peut être notifié, mais EXPIRE s'applique dès J+1. Les droits
expirés depuis plus de 30 jours sont régularisés sans envoyer les anciennes alertes.

[Retour à l’index des spécifications](../INDEX.md)
