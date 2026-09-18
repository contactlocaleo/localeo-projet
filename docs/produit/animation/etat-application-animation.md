# Spécification produit et technique — Localeo Animation

> Synthèse historique conservée : les tarifs et statuts peuvent différer des textes juridiques et de la roadmap ultérieurs. Voir [les écarts à arbitrer](../../organisation/compte-rendu-reorganisation-2026-09-18.md#points-conservés-à-arbitrer).

## Identification du document

| Propriété | Valeur |
| --- | --- |
| Produit | Localeo Animation |
| Nature | Spécification fonctionnelle et technique de référence |
| Version | 1.0 |
| Date | 4 septembre 2026 |
| Périmètre | MVP partenaire, administration Localeo et intégrations associées |
| Domaine principal | `animation_locale` |
| Statut | Socle intégré ; souscription EPIC 47 à recetter avec Stripe Test |

Ce document décrit l'application **Localeo Animation** dans son ensemble. Les
spécifications détaillées par EPIC restent les sources de vérité pour les
règles fines. En cas d'écart, le registre d'arbitrages de l'EPIC concernée
prévaut.

## 1. Vision produit

Localeo Animation permet à une collectivité, une association de commerçants,
un office de tourisme ou un autre partenaire territorial de concevoir et
piloter des animations locales impliquant les commerçants et le public.

Le produit doit permettre au partenaire de gérer lui-même le cycle nominal
d'une animation. Localeo fournit la plateforme, les contrôles, les coffrets et
le support, mais n'est pas l'organisateur opérationnel de l'animation.

Le premier modèle de référence est le **Passeport commerçant**. La plateforme
prend également en charge la **Tombola locale**. Le Calendrier de l'Avent et la
Chasse au trésor sont des évolutions cadrées mais non comprises dans le produit
actuellement livré.

## 2. Objectifs du MVP

- référencer un partenaire et ses gestionnaires ;
- attribuer des droits par commune ;
- souscrire une offre Localeo Animation par commune ;
- créer et configurer une animation à partir d'un modèle ;
- solliciter et suivre le consentement des commerçants participants ;
- financer les lots constitués de coffrets Localeo actifs ;
- publier l'animation et générer son flyer ;
- inscrire les participants sans leur imposer de compte ;
- valider les étapes ou achats par QR participant ;
- suivre l'activité en direct ;
- clôturer l'animation et figer la population éligible ;
- effectuer un tirage traçable puis envoyer les gains ;
- consulter le bilan, les indicateurs et les exports ;
- publier des actualités liées à l'animation ;
- permettre à Localeo de superviser et traiter les blocages.

## 3. Périmètre applicatif

### 3.1 Dans Localeo Animation

La surface partenaire couvre :

1. l'authentification et le choix de la commune active ;
2. le tableau de bord ;
3. le catalogue des modèles d'animation ;
4. les animations et leur workflow ;
5. les commerçants sollicités et participants ;
6. les participants grand public ;
7. les validations terrain ;
8. les lots, tirages et gains ;
9. les flyers, bilans et exports ;
10. les actualités et notifications ;
11. l'abonnement et son échéance ;
12. le support et l'audit publiable.

### 3.2 Hors de Localeo Animation

| Capacité | Application responsable |
| --- | --- |
| Acceptation d'une participation par un commerçant | Application commerçant |
| Consultation publique et inscription | Marketplace / Localeo Live |
| QR et suivi personnel du participant | Localeo Live |
| Référencement, prix, gratuité et rapprochement | Backoffice Localeo |
| Paiement sécurisé | Stripe Checkout |
| Gestion métier des coffrets | Domaines coffrets et achats Localeo |
| Stockage et versionnement des documents | Domaine `documentaire` |

## 4. Acteurs et droits

| Acteur | Responsabilités |
| --- | --- |
| Gestionnaire Animation | Gère les animations des communes auxquelles il est habilité |
| Partenaire organisateur | Porte le contrat, l'abonnement et le financement des lots |
| Commerçant | Accepte ou refuse sa participation et réalise les validations autorisées |
| Participant | S'inscrit, présente son QR et consulte son parcours sans compte obligatoire |
| Opérateur Localeo | Supervise l'activité et accompagne le partenaire |
| Administrateur Localeo | Référence, tarifie, active les gratuités et traite les rapprochements |

Le tenant fonctionnel est la **commune**. Une animation appartient à une seule
commune. Un gestionnaire peut être habilité sur plusieurs communes mais doit
sélectionner explicitement la commune active.

Une ressource située hors du tenant autorisé retourne `404`. Une action non
permise dans un tenant autorisé retourne `403`.

## 5. Principes d'expérience utilisateur

Localeo Animation reprend la grammaire visuelle des autres applications
Localeo : navigation stable, écrans sobres, vocabulaire métier explicite et
actions principales immédiatement identifiables.

### 5.1 Navigation cible

- **Vue d'ensemble** : indicateurs, alertes et animations nécessitant une action ;
- **Animations** : liste, recherche, filtres et création ;
- **Participants** : consultation et export selon les droits ;
- **Validations** : suivi, anomalies et corrections autorisées ;
- **Tirages et gains** : population éligible, tirage et envoi ;
- **Documents** : flyers, bilans et exports ;
- **Actualités** : brouillons, programmation et publication ;
- **Abonnement** : offre, droits, consommation et date d'échéance ;
- **Support** : fil d'assistance contextualisé.

La commune active doit rester visible dans l'en-tête. Le changement de commune
ne doit jamais conserver à l'écran une donnée appartenant au tenant précédent.

### 5.2 Présentation du workflow

La fiche d'une animation présente les sections sous forme d'onglets :

- synthèse ;
- configuration ;
- commerçants ;
- participants ;
- validations ;
- communication ;
- tirage et gains ;
- bilan et audit.

L'écran affiche le statut courant, la progression, les blocages, leur cause et
un accès direct au traitement correspondant. Une action indisponible est
accompagnée d'une explication ; elle n'est pas seulement grisée.

## 6. Authentification et contexte

- la session partenaire est distincte des sessions administrateur et commerçant ;
- le token est opaque et référence une session serveur ;
- le Bearer est conservé uniquement en mémoire de l'onglet, jamais dans localStorage
  ou sessionStorage. Un rechargement ou un nouvel onglet exige une reconnexion ;
- l'ancien stockage `localeo_session` est supprimé au démarrage sans restaurer son
  contenu. Les sessions serveur existantes restent soumises à leur expiration et révocation ;
- la durée nominale d'une session est de huit heures ;
- les permissions sont relues depuis l'habilitation persistée ;
- la session contient le partenaire, l'acteur et la commune active ;
- la déconnexion révoque la session côté serveur ;
- aucune permission contenue dans le navigateur ne fait autorité.

Le rôle `GESTIONNAIRE_ANIMATION` est décliné en permissions fines, notamment
création, modification, publication, clôture, tirage, envoi des gains,
consultation du bilan et gestion des actualités.

## 7. Abonnement Localeo Animation

### 7.1 Catalogue MVP

| Offre | Prix catalogue HT | Durée | Usage | Modèle de service |
| --- | ---: | --- | --- | --- |
| Découverte | 390,00 € | 12 mois | Une première publication réussie | Clé en main |
| Essentielle | 708,00 € | 12 mois | Animations sans quota au MVP | Plateforme autonome |

Le prix s'applique au couple **partenaire + commune**. Un référencement portant
sur plusieurs communes crée une souscription distincte par commune, mais une
commande et un paiement Stripe consolidés.

### 7.2 Tarification

- le backoffice propose le prix catalogue par défaut ;
- le prix convenu est saisi en HT ;
- le taux et le montant de TVA ainsi que le TTC sont calculés puis snapshotés ;
- une remise, une majoration ou une gratuité exige un motif ;
- une gratuité exige une confirmation administrative explicite ;
- le montant persisté côté serveur fait autorité pour Stripe ;
- un prix payé ne peut plus être modifié.

### 7.3 Parcours payant

1. L'administrateur référence le partenaire, les communes et le premier gestionnaire.
2. Le backend crée une souscription mono-commune pour chaque commune.
3. Une commande consolidée est créée avec une ligne par souscription.
4. Stripe Checkout reçoit les montants TTC issus des snapshots persistés.
5. La demande de paiement est envoyée au contact de facturation.
6. Le webhook signé contrôle la session, le statut, le montant et la devise.
7. Les abonnements et habilitations sont activés après paiement seulement.
8. Le gestionnaire reçoit ensuite son invitation au portail.
9. Le contact de facturation reçoit une confirmation de paiement.

Un paiement reçu pour une commande annulée ou une ancienne session Checkout ne
réactive jamais automatiquement les droits : il passe en `A_RECONCILIER`.

### 7.4 Expiration

- la date de fin est calculée depuis la date d'activation ;
- des alertes sont créées à J-30, J-7 et J0 ;
- elles sont adressées au contact de facturation et aux gestionnaires actifs,
  avec déduplication ;
- l'envoi est idempotent par abonnement, seuil et destinataire ;
- après expiration, les nouvelles créations et publications sont bloquées ;
- une animation déjà publiée ou en cours peut être menée à son terme.

## 8. Cycle de vie d'une animation

```text
BROUILLON -> CONFIGUREE -> PUBLIEE -> EN_COURS -> CLOTUREE -> ARCHIVEE
BROUILLON -> ANNULEE
```

| Statut | Sens fonctionnel |
| --- | --- |
| `BROUILLON` | Animation créée, encore librement configurable |
| `CONFIGUREE` | Données obligatoires présentes, publication encore réversible |
| `PUBLIEE` | Animation visible et inscriptions ouvertes selon les dates |
| `EN_COURS` | Validations et suivi live actifs |
| `CLOTUREE` | Population éligible figée ; tirage possible |
| `ARCHIVEE` | Cycle terminé et conservé en consultation |
| `ANNULEE` | Brouillon abandonné par l'organisateur avant publication |

La réouverture par un gestionnaire est interdite. Une correction exceptionnelle
par Localeo exige un motif, un audit et, si nécessaire, la régénération de la
population éligible.

## 9. Création et configuration

Le gestionnaire choisit un modèle autorisé par son offre et renseigne au minimum :

- nom, description et visuels ;
- dates d'inscription, de début et de fin ;
- règles de participation et d'éligibilité ;
- commerçants sollicités ;
- mission attendue des commerçants ;
- lots financés ;
- contenus de communication.

Une animation n'est modifiable par le gestionnaire qu'en `BROUILLON` ou
`CONFIGUREE`. Les paramètres propres au modèle sont versionnés. Les actifs sont
téléversés par une route DAM protégée ; PNG, JPEG et WebP sont acceptés dans la
limite configurée de 5 Mo.

### Catalogue des coffrets vendables (F05)

Le filtre `eligible=true` applique toutes les gardes avant pagination : statut
actif, couverture des commercants lorsqu'une animation est fournie, politique
BUM active avec mentions approuvees, promesse garantie non vide et qualification
courante MULTI_PURPOSE/VALIDATED pour cette politique. Le tri nom puis identifiant
est stable. Les pages restent des listes, avec `page` et `page_size` (maximum
100). Le portail parcourt les pages jusqu'a la premiere page incomplete ; il
signale une erreur plutot qu'une liste tronquee si la limite de collecte est
atteinte. Les controles de publication et d'achat restent obligatoires.

### Annulation d'un brouillon

L'organisateur peut annuler une animation uniquement lorsqu'elle est encore en
`BROUILLON` et qu'aucun lot n'a été payé. L'opération est atomique et :

- passe l'animation à l'état `ANNULEE` avec le motif fourni ;
- expire la commande de lots et invalide les achats en attente ;
- marque uniquement les invitations courantes non refusees `ANNULEE` avec le
  motif technique `ANNULEE_PAR_ORGANISATEUR_DU_JEU` ; les refus et les cycles
  historiques restent inchanges et aucun cycle historique ne redevient courant ;
- libère toute consommation ou réservation de quota associée à l'animation ;
- journalise le nombre d'invitations annulées et la restitution du quota.

Une animation dont les lots sont payés ne peut pas suivre ce parcours. Elle
doit être traitée par la procédure financière adaptée. Le rejeu de la même
commande d'annulation est idempotent.

## 10. Participation des commerçants

La sélection d'un commerçant ne vaut pas acceptation. Localeo Animation crée
une demande de participation versionnée, présentant :

- l'identité et les dates de l'animation ;
- la mission attendue ;
- les règles de validation ;
- les engagements de communication ;
- les conditions concernant les lots.

Le commerçant accepte ou refuse depuis son application. Localeo Animation
affiche en temps réel les réponses, les relances possibles et les refus. Seuls
les commerçants ayant explicitement accepté sont intégrés à la publication, au
flyer et aux règles de validation.

## 11. Publication et communication

La publication vérifie atomiquement :

- l'abonnement et le droit de publier ;
- le quota disponible de l'offre Découverte ;
- la configuration obligatoire ;
- la présence de commerçants participants ;
- le financement et la disponibilité des lots requis ;
- la cohérence des dates et des règles du modèle.

Le quota Découverte est consommé lors de la première publication réussie. Un
rejeu idempotent ne consomme pas un second crédit. L'annulation d'un brouillon
avant paiement des lots libère toute consommation ou réservation éventuelle et
le compteur affiché dans Localeo Animation est recalculé à partir des
consommations non annulées.

La publication rend disponible le lien public et le QR d'inscription. Le flyer
PDF et son aperçu PNG sont générés après le gel des commerçants participants.
Un échec de génération documentaire ou de notification n'annule pas la
publication ; il crée une opération relançable et visible.

## 12. Participants et validations

Le participant ne crée pas de compte au MVP. Il fournit son email, son nom, son
prénom et son téléphone, puis reçoit un lien et un QR personnel opaques.

- l'unicité d'inscription est `animation_id + email_normalise` ;
- le QR ne contient aucune donnée personnelle ;
- les tokens sont aléatoires, révocables, expirables et stockés sous forme de hash ;
- QR participant et QR coffret utilisent des parcours distincts ;
- la validation est effectuée par le commerçant authentifié ;
- une soumission répétée à l'identique est idempotente ;
- une correction est tracée et motivée, jamais supprimée silencieusement ;
- le fonctionnement hors connexion est hors MVP.

Le Passeport commerçant qualifie le participant selon les étapes prévues. La
Tombola locale qualifie une personne après un achat validé chez un commerçant
participant, sans montant minimum, avec une chance au tirage.

## 13. Suivi en direct

Le tableau de bord actualise les projections par polling HTTP toutes les
15 secondes au MVP. Il expose au minimum :

- animations par statut ;
- inscriptions et évolution récente ;
- validations et progression ;
- commerçants sollicités, acceptants et sans activité ;
- participants qualifiés ;
- alertes et opérations en échec ;
- lots disponibles, tirages et gains à envoyer ;
- consommation de l'abonnement et date d'échéance.

Les vues globales Participants, Validations, Tirages/Gains, Flyers et Bilans
sont filtrables côté serveur. Les listes stables utilisent `page/page_size` ;
les flux live et l'audit utilisent un curseur.

## 14. Clôture, tirage et gains

- la clôture peut être automatique à la date de fin ou manuelle anticipée ;
- les deux chemins appellent le même cas d'usage atomique et idempotent ;
- la population éligible est figée dans la transaction de clôture ;
- une validation postérieure au verrouillage est rejetée ;
- le tirage utilise un générateur cryptographiquement sûr ;
- la population, sa version, les lots et les suppléants sont tracés ;
- un participant ne remporte qu'un lot par tirage ;
- le remplacement d'un gagnant est motivé et utilise le suppléant suivant ;
- l'envoi d'un gain crée et active la `CoffretInstance` correspondante ;
- l'échec d'une notification est relançable sans recréer le gain.

Les lots sont des coffrets Localeo actifs de la commune, acceptés par les
commerçants concernés et financés séparément selon le parcours de l'EPIC 46.

## 15. Actualités, notifications et support

Une actualité peut être préparée depuis la fiche Animation. Sa publication ou
sa programmation est autorisée pour une animation `PUBLIEE`, `EN_COURS` ou
`CLOTUREE`. Elle alimente Localeo Live pour les installations suivant la
commune ou participant à l'animation, sous réserve de la préférence `ANIMATION`.

Canaux du MVP :

- email obligatoire pour inscription, QR, paiement, invitation et gain ;
- inbox Localeo Live persistante lorsque la préférence l'autorise ;
- WebPush optionnel avec consentement et abonnement actif ;
- SMS hors MVP pour les parcours Animation.

Le support est un fil texte contextualisable par animation, sans pièce jointe
au MVP.

## 16. Bilans, indicateurs et exports

Le bilan doit séparer les indicateurs opérationnels, participant, commerçant et
financiers. Il inclut notamment inscriptions, validations, qualification,
commerçants actifs, gains, consommation des coffrets et incidents.

Les exports CSV UTF-8 sont synchrones jusqu'à 10 000 lignes, puis asynchrones.
Ils sont audités, téléchargeables pendant sept jours et supprimés au plus tard
après 90 jours.

La Vision 360 Localeo reste une projection en lecture. Elle ne devient jamais
une source de vérité métier.

## 17. Contrats d'API

| Préfixe | Public | Responsabilité |
| --- | --- | --- |
| `/public/identite-acces/animation` | Public | Entrée dans l'authentification partenaire |
| `/protected/identite-acces/animation` | Gestionnaire | Session, contexte et déconnexion |
| `/public/animation-locale` | Participant | Catalogue public, inscription et accès par token |
| `/protected/animation-locale` | Gestionnaire | Cycle métier complet des animations |
| `/internal/animation-locale` | Localeo | Supervision, support et opérations internes |
| `/internal/abonnements-plateforme` | Localeo | Catalogue, commandes, activation et CA |
| `/public/stripe/webhook` | Stripe signé | Confirmation et expiration de Checkout |

Toute commande asynchrone retourne `202`, un `operation_id`, un `resource_id`,
un `status_url` et un état initial. Les écritures rejouables utilisent une clé
d'idempotence. Les erreurs métier suivent un format stable comprenant un code,
un message exploitable et un identifiant de corrélation.

## 18. Données, sécurité et conformité

- HTTPS obligatoire hors développement ;
- signature Stripe vérifiée avant tout traitement ;
- aucun numéro de carte bancaire conservé par Localeo ;
- contrôle du tenant et des permissions sur chaque ressource ;
- journalisation sans secret ni donnée personnelle inutile ;
- audit des actions sensibles et des décisions commerciales ;
- protection CSRF et origine sur les sessions navigateur ;
- limitation de taille et contrôle réel du contenu des fichiers ;
- liens documentaires protégés ou signés avec courte durée de validité.

Conservation de référence : données nominatives participant jusqu'à fin de
l'animation + 12 mois, tokens jusqu'à fin + 3 mois, validations détaillées
24 mois, tirages et gains pseudonymisés 5 ans, exports 90 jours maximum et
traces de notification 12 mois. Ces durées doivent rester configurables et
validées juridiquement avant production.

## 19. Configuration

Les URLs sont des contrats de configuration ; le backend n'invente pas les
chemins frontend.

| Clé | Usage |
| --- | --- |
| `LOCALEO_ANIMATION_PORTAIL_URL` | Entrée du portail gestionnaire |
| `LOCALEO_ANIMATION_PUBLIC_URL_TEMPLATE` | Lien public d'une animation |
| `LOCALEO_ANIMATION_PARTICIPANT_URL_TEMPLATE` | Lien personnel participant |
| `LOCALEO_FRONT_LIVE_ANIMATION_URL_TEMPLATE` | Deep link vers Localeo Live |
| `LOCALEO_ANIMATION_SUBSCRIPTION_SUCCESS_URL` | Retour après paiement réussi |
| `LOCALEO_ANIMATION_SUBSCRIPTION_CANCEL_URL` | Retour après abandon du paiement |
| `LOCALEO_ANIMATION_SUBSCRIPTION_SUPPORT_URL` | Assistance contextualisée |
| `LOCALEO_ANIMATION_SUBSCRIPTION_EXPIRATION_ALERT_DAYS` | Seuils, par défaut `30,7,0` |

Les prix, durées, quotas et taux fiscaux sont des données métier administrées
ou versionnées, et non des variables d'environnement dispersées.

## 20. Exigences non fonctionnelles

- chargement d'une liste standard : cible inférieure à 500 ms côté API ;
- agrégation d'indicateurs complexes : cible inférieure à 1,5 s ;
- pagination maximale : 100 éléments par page ;
- polling live : 15 secondes, sans requête concurrente du même écran ;
- traitement idempotent des webhooks, publications, clôtures et notifications ;
- cinq tentatives maximum pour une opération asynchrone, avec backoff borné ;
- accessibilité clavier et contraste conformes au socle graphique Localeo ;
- interface responsive utilisable sur tablette et mobile ;
- traçabilité par identifiant de corrélation de bout en bout.

## 21. Périmètre non compris dans le MVP

- animation multi-communes portée par une seule animation ;
- renouvellement automatique de l'abonnement ;
- changement d'offre ou remboursement automatique ;
- fournisseur OIDC externe ;
- temps réel WebSocket ou SSE ;
- validation commerçant hors connexion ;
- pièces jointes dans le support ;
- SMS Animation ;
- gestion autonome de sponsors et groupes de participants ;
- Calendrier de l'Avent et Chasse au trésor en production.

## 22. Critères de recette prioritaires

1. Un gestionnaire ne voit et ne modifie que les communes habilitées.
2. Une commande multi-communes produit un seul Checkout avec une ligne par commune.
3. Aucun accès payant n'est ouvert avant un webhook Stripe valide.
4. Un webhook rejoué ne crée ni second abonnement ni second email.
5. Une session Stripe obsolète ou une commande annulée passe en rapprochement.
6. Une gratuité exige un motif et une confirmation explicite.
7. Le quota Découverte est consommé une seule fois à la publication réussie.
8. Une animation sans commerçant ayant accepté ne peut pas être publiée.
9. Le flyer ne contient que les commerçants participants figés à la publication.
10. Une validation hors tenant, en double ou après clôture est refusée.
11. La clôture fige une population éligible stable et versionnée.
12. Un tirage rejoué ne change pas les gagnants.
13. L'envoi d'un gain active une seule instance du coffret prévu.
14. Les alertes d'échéance J-30, J-7 et J0 sont dédupliquées.
15. Les blocages sont visibles avec leur cause et un accès à leur traitement.
16. L'annulation d'un brouillon est refusée si un lot est payé ; sinon elle
    libère le crédit one-shot éventuel et marque les invitations annulées par
    l'organisateur.

## 23. Déploiement et exploitation

Le déploiement de l'EPIC 47 exige la migration
`sql/v215_epic47_souscriptions_animation.sql`, les quatre URLs de souscription,
les secrets Stripe et la déclaration du webhook. La recette Stripe Test doit
couvrir paiement réussi, Checkout expiré, rejeu, session obsolète, commande
annulée et erreur d'activation.

La procédure détaillée est disponible dans
[la procédure d'exploitation de l'EPIC 47](../../specifications/epic-47-souscription-abonnement-partenaire-animation/procedure-exploitation.md).

## 24. Sources de vérité

- [Backlog de la plateforme Animation](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md)
- [Architecture du domaine Animation](../../architecture/backend/epics/epic-41-animation-locale-architecture.animation.md)
- [Catalogue des API Animation](../../specifications/epic-41-api/catalogue-api.md)
- [Spécification de la souscription](../../specifications/epic-47-souscription-abonnement-partenaire-animation/README.md)
- [Paiement des lots](../../specifications/epic-46-paiement-lots-animation/README.md)
- [Vision 360 Animation](../../specifications/epic-45-vision-360-animation/README.md)
- [Tombola locale](../../specifications/epic-53-tombola-locale/README.md)
- [Participation des commerçants](../../specifications/epic-56-validation-participation-commercants-animation/README.md)
- [Spécification BUM pour Localeo Animation](../../specifications/epic-50-conformite-fiscale-bum/localeo-animation.md)
