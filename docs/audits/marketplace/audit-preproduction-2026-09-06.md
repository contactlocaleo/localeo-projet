# VERDICT DE MISE EN PRODUCTION

> Actualisation du 7 septembre 2026 : les dix constats MARKET sont corriges et testes localement. Voir le [registre des commits, preuves et conditions de livraison](suivi-corrections-backend-marketplace-2026-09-06.md). Le texte ci-dessous conserve l'etat historique du 6 septembre ; il ne constitue pas le statut actuel du deploiement.

## 🔴 NO-GO PRODUCTION

Trois problèmes justifient de repousser l'ouverture du périmètre audité : risque de transmission de jetons à Analytics, retour de paiement incompatible avec le backend local et confirmation professionnelle affichant un succès sans paiement vérifié.

| Métadonnée | Valeur |
| --- | --- |
| Application | Localeo Marketplace, parcours Pro, animations publiques et Localeo Live |
| Date du compte rendu | 6 septembre 2026 |
| Référence Marketplace auditée | `ecb6d56` |
| Référence backend examinée | `728be26`, complétée par les modifications locales décrites ci-dessous |
| Nature | Audit de sources locales, contrôles ciblés et reproductions isolées |
| Document complémentaire | [Répartition des corrections backend / Marketplace](plan-corrections-backend-marketplace-2026-09-06.md) |

Ce document formalise le compte rendu présenté dans la conversation. Sa création n'est pas une nouvelle campagne de tests. Aucun correctif applicatif n'a été appliqué pendant l'audit ni lors de la rédaction de ces documents.

Le backend voisin contenait des modifications non committées sur `activer_coffret_instance_achat.py` et `models.py`, ainsi qu'un service `activation.py`, une migration `v221_unicite_droits_instance.sql`, un test de concurrence et un contre-audit. Les protections observées dans ces fichiers locaux ne prouvent ni leur livraison ni l'application de la migration en production.

## 1. Executive summary

### Points positifs

- Les achats, instances, participants et installations Live possèdent des contrôles d'accès serveur.
- Les jetons personnels sont aléatoires et hachés côté serveur, avec des contrôles d'expiration et de révocation.
- Le prix du checkout provient du catalogue backend.
- Le backend vérifie la signature Stripe et la cohérence du financement.
- Les QR sont rendus comme images passives.
- Les requêtes HTTP sont bornées, corps compris, sans répétition automatique des écritures.
- Le cache du service worker est réservé aux ressources publiques autorisées.
- Des protections existent contre les réponses tardives et certaines opérations locales concurrentes.

Ces protections ne clôturent pas les trois bloqueurs. Aucune fraude financière, double consommation ou intrusion inter-tenant n'a été démontrée pendant l'audit. Aucun paiement réel ni essai concurrent sur PostgreSQL n'a été effectué.

### Cartographie fonctionnelle

Référence : [App.jsx, routes à partir de la ligne 202](../../../../localeo-marketplace/src/App.jsx).

| Domaine | Routes principales | Parcours critique |
| --- | --- | --- |
| Découverte | `/accueil`, `/city`, `/coffrets`, `/coffret`, `/commercant` | Localisation → catalogue → offre |
| Achat particulier | `/coffret`, `/retour-paiement`, `/confirmation`, `/echec-paiement` | Initialisation → Stripe → vérification → accès au coffret |
| Achat Pro | `/commande-pro`, `/confirmation-pro`, `/mes-coffrets-pro`, `/achat/:achatId` | Commande multiple → distribution → activation |
| Bénéficiaire | `/activer-coffret`, `/activation-confirmee`, `/consulter-detail-coffret`, `/afficher-resume-coffret`, `/qr-impression` | Lien personnel → consultation ou activation → QR |
| Facturation et crédit | `/coffret/:instanceId/facturation`, `/pro/credit` | Accès personnel → facture ou authentification OTP |
| Animations | `/animations`, `/animations/:animation_id`, `/animations/participants/:token` | Découverte → inscription → suivi participant |
| Live | `/live/*` | Carnet local → rattachement par jeton → suivi et notifications |
| Support | `/contact`, `/p/:token`, `/feedback-prestation/:token` | Message, résolution de lien, avis |

Les espaces d'administration commerçants et collectivités sont des applications distinctes. Leur audit exhaustif n'est pas inclus dans ce rapport.

## 2. Bloqueurs production

### MARKET-001 — Jetons d'accès transmis à Analytics

- **Sévérité : HAUTE.**
- **Bloquant production : OUI**, tant qu'Analytics peut fonctionner sur les parcours sensibles.
- **Localisation :** [analytics.js](../../../../localeo-marketplace/src/services/analytics.js), `buildSanitizedPageContext`, lignes 256–305 ; [AnalyticsRouteTracker.jsx](../../../../localeo-marketplace/src/components/AnalyticsRouteTracker.jsx), ligne 16.
- **Problème :** le filtrage retire des paramètres de requête, mais conserve le chemin complet. Les routes de participation, de feedback et certains liens Live contiennent leur jeton dans ce chemin.
- **Scénario :** un utilisateur ayant accepté Analytics ouvre `/animations/participants/<jeton>`. Le tracker place ce jeton dans `page_location` et `page_path`.
- **Impact :** divulgation d'une capacité d'accès personnelle au système de mesure et aux personnes ou intégrations autorisées à le consulter.
- **Preuve :** reproduction en mémoire avec un jeton fictif et un `gtag` simulé : `tokenSent: true`. Le backend résout effectivement le participant à partir de ce jeton dans [participants_animation.py](../../../../localeo-backend/app/application/animation_locale/services/participants_animation.py), ligne 74.
- **Correction minimale :** suspendre Analytics pour l'ouverture, puis contrôler toutes les émissions sur les routes sensibles, y compris les émissions automatiques du fournisseur. Le filtrage des seuls événements applicatifs n'est pas une preuve suffisante.

Google documente que la mesure améliorée peut produire des pages vues malgré `send_page_view: false` : [documentation Google](https://developers.google.com/analytics/devguides/collection/ga4/views?hl=en).

### MARKET-002 — Retour de paiement incompatible avec l'authentification backend

- **Sévérité : HAUTE.**
- **Bloquant production : OUI** pour le couple frontend/backend local examiné.
- **Localisation :** [api.js](../../../../localeo-marketplace/src/services/api.js), `fetchAchatCoffretFromSession`, lignes 511–512 ; [RetourPaiementPage.jsx](../../../../localeo-marketplace/src/pages/RetourPaiementPage.jsx), ligne 113 ; [consulter_achat_depuis_session_checkout.py](../../../../localeo-backend/app/application/gestion_achats/use_cases/consulter_achat_depuis_session_checkout.py), lignes 19–30.
- **Problème :** le client appelle `/achats/depuis-session/{session_id}` sans `Authorization` ni `X-Management-Token`. Le backend exige désormais un jeton de gestion avant toute résolution.
- **Scénario :** après paiement, le client revient avec `session_id`. Les trois tentatives sans jeton échouent et le parcours reste en vérification.
- **Impact :** confirmation post-paiement indisponible, charge support et risque de nouvel achat malgré le premier paiement.
- **Preuve :** même avec un jeton fictif en session, le client produit `authorizationSent: false` et `managementHeaderSent: false`. Le garde backend exige explicitement le jeton.
- **Correction minimale :** définir un contrat sécurisé de consultation du résultat checkout pour B2C et Pro, puis aligner backend, client et OpenAPI.

Un ajout de header ne suffit pas à lui seul : dans le code lu, le jeton de gestion est généré lors de la validation des achats professionnels puis communiqué par le parcours d'email. Le retour particulier ne possède pas un mécanisme équivalent. Ne pas supprimer le garde serveur ni rendre les commandes généralement accessibles par simple `session_id`.

### MARKET-003 — Confirmation Pro positive sans achat vérifié

- **Sévérité : HAUTE.**
- **Bloquant production : OUI** pour le parcours Pro.
- **Localisation :** [ConfirmationProPage.jsx](../../../../localeo-marketplace/src/pages/ConfirmationProPage.jsx), lignes 87, 112, 141–147 et 205–209 ; [CommandeProPage.jsx](../../../../localeo-marketplace/src/pages/CommandeProPage.jsx), ligne 196.
- **Problème :** le statut par défaut est `succes`. Sans `session_id`, aucun achat n'est chargé, mais le succès est affiché. Une erreur de chargement peut également coexister avec cette confirmation.
- **Scénario :** ouvrir `/confirmation-pro?quantite=10` dans une session vide.
- **Impact :** fausse confirmation financière susceptible d'induire l'acheteur en erreur sur une distribution de coffrets. Ce rendu ne crée pas à lui seul de droits backend.
- **Preuve :** rendu isolé du composant réel : `claimsPaymentValidated: true`, `claimsOrderCreated: true`, `hasTenCoffrets: true`.
- **Correction minimale :** statut initial indéterminé et succès seulement après confirmation serveur de l'achat concerné, y compris pour le financement intégral par crédit.

Le parcours sans `checkout_url` transmet `achat_id` à cette page, mais la page ne charge pas l'achat à partir de ce paramètre.

## 3. Sécurité

### MARKET-004 — Coordonnées et jeton QR dans les URL d'API

- **Sévérité : MOYENNE. Bloquant production : NON isolément.**
- **Localisation :** [api.js](../../../../localeo-marketplace/src/services/api.js), `createCheckout`, lignes 449–482, et `fetchQrDetail`, ligne 599 ; [paiements_api.py](../../../../localeo-backend/app/api/paiements_api.py), ligne 14.
- **Problème / preuve :** l'achat utilise la query string d'un POST pour email, téléphone et identité professionnelle. Le détail QR utilise celle d'un GET pour `token`. Le contrat backend confirme ce transport.
- **Scénario / impact :** conservation possible de ces URL dans les traces HTTP, outils de diagnostic ou intermédiaires. La collecte effective en production n'a pas été vérifiée.
- **Correction minimale :** JSON pour l'achat et header d'accès pour le QR, avec migration coordonnée du contrat et revue des traces.

### MARKET-005 — Retrait du consentement non propagé au tag chargé

- **Sévérité : MOYENNE. Bloquant production : NON isolément**, à traiter avec MARKET-001 avant réactivation d'Analytics.
- **Localisation :** [analytics.js](../../../../localeo-marketplace/src/services/analytics.js), `setAnalyticsConsent`, ligne 114.
- **Problème :** le refus après acceptation modifie le stockage et bloque les événements applicatifs, sans adresser de commande de retrait au tag chargé.
- **Scénario / impact :** les émissions automatiques éventuelles restent hors du contrôle du mécanisme de retrait ; leur poursuite effective dépend de la configuration Google non inspectée.
- **Preuve :** `consentUpdateSent: false`, alors que `customEventsBlocked: true`.
- **Correction minimale :** propager le retrait au fournisseur, gérer les autres onglets et vérifier les requêtes après retrait.

### Autres contrôles

Les anciens SVG intégrés ont été remplacés par des images passives. Aucun usage actif de `dangerouslySetInnerHTML` ou `innerHTML` n'a été trouvé dans les sources applicatives recherchées. Les données textuelles métier sont généralement rendues par React.

Les redirections checkout imposent HTTPS et refusent les identifiants intégrés à l'URL. Elles ne limitent pas les origines à celles du prestataire. Aucun contrôle de cette URL par un attaquant n'a été démontré.

## 4. Authentification / autorisations

L'application publique ne comporte pas de compte consommateur classique. Elle utilise des liens à capacité.

| Acteur | Accès attendu | Contrôle serveur observé |
| --- | --- | --- |
| Visiteur | Catalogue, inscription, initialisation d'achat | Validations et certains quotas |
| Acheteur Pro | Achat et instances associés | Jeton de gestion lié à l'achat |
| Bénéficiaire | Instance et QR associés | Jeton de consultation lié à l'instance |
| Destinataire d'activation | Activation de l'instance ciblée | Jeton lié à l'achat et à l'instance |
| Participant | Participation et QR | Jeton haché, expiration/révocation |
| Installation Live | Préférences, suivis, notifications propres | Identifiant et secret d'installation |
| Titulaire de crédit | Compte de crédit associé | Code + OTP puis session |

Références : [management_token.py](../../../../localeo-backend/app/security/management_token.py), ligne 32 ; [verifier_consultation_token_coffret_instance.py](../../../../localeo-backend/app/application/identite_acces/use_cases/verifier_consultation_token_coffret_instance.py), ligne 17.

- Pas de refresh token automatique ni de boucle de renouvellement dans les parcours consommateurs.
- Contrôles serveur d'expiration et de révocation présents.
- Pas de déconnexion générale des liens consommateurs.
- Retirer un élément du carnet ne révoque pas automatiquement sa capacité.
- Les erreurs 401/403 remontent, sans purge systématique de tous les caches sensibles.
- Le crédit reste en mémoire avec contrôle d'expiration côté client.

La présence d'un identifiant dans une URL ne constitue pas, à elle seule, une IDOR.

## 5. Intégrité métier

Le checkout utilise le prix du catalogue backend. Le navigateur ne transmet pas un prix faisant autorité. La signature Stripe et la cohérence du financement sont vérifiées côté serveur. Le retour navigateur n'est pas utilisé comme preuve de paiement par le backend : [principe de fulfillment Stripe](https://docs.stripe.com/checkout/fulfillment).

### MARKET-009 — Crédit activé : achat Pro sans session de crédit rejeté

- **Sévérité : MOYENNE. Bloquant production : NON si le crédit reste désactivé.** Correction nécessaire avant son activation.
- **Localisation :** [CommandeProPage.jsx](../../../../localeo-marketplace/src/pages/CommandeProPage.jsx), lignes 179–192 ; [initialiser_paiement.py](../../../../localeo-backend/app/application/gestion_achats/use_cases/initialiser_paiement.py), lignes 339–357.
- **Problème / preuve :** backend crédit actif : acceptation des conditions requise pour l'achat Pro. Le frontend ne la transmet que si une session de crédit existe.
- **Scénario / impact :** une entreprise sans session de crédit commande normalement et reçoit un rejet avant checkout.
- **Correction minimale :** aligner collecte des conditions et contrat pour les acheteurs avec ou sans crédit ; valider la version côté serveur.

### MARKET-010 — Quantité d'achat insuffisamment bornée côté serveur

- **Sévérité : MOYENNE. Bloquant production : NON sur les preuves disponibles.**
- **Localisation :** [paiements_api.py](../../../../localeo-backend/app/api/paiements_api.py), ligne 21 ; [initialiser_paiement.py](../../../../localeo-backend/app/application/gestion_achats/use_cases/initialiser_paiement.py), ligne 274 ; [achat_coffret.py](../../../../localeo-backend/app/domaine/gestion_achats/entities/achat_coffret.py), lignes 34–42.
- **Problème / preuve :** quantité entière sans borne métier dans l'endpoint ni validation de quantité dans l'entité. Le montant est calculé et le traitement peut persister l'achat avant l'appel au prestataire.
- **Scénario / impact :** zéro ou une quantité excessive peuvent atteindre un traitement incohérent ou une erreur tardive. Ni coffret gratuit ni traitement financier indu n'ont été démontrés.
- **Correction minimale :** minimum et maximum métier dans l'API et le domaine, avec contraintes de données appropriées, avant persistance.
- **Limite :** constat par lecture de code ; aucun essai sur base réelle ou paiement n'a été effectué.

## 6. Gestion des appels API

Les appels métier passent par [api.js](../../../../localeo-marketplace/src/services/api.js), puis [request.js](../../../../localeo-marketplace/src/services/request.js). Les réponses non réussies lèvent une erreur centralisée ; chaque page gère ensuite sa présentation, avec les limites de MARKET-003.

Le snapshot [OpenAPI](../../../../localeo-marketplace/api/localeo-openapi.json) comporte 263 chemins. Il ne décrit pas les nouveaux headers requis pour la résolution depuis session : désynchronisation confirmée avec le backend local.

### Inventaire regroupé des endpoints consommés

Les variantes de liste/détail et les alias de helpers sont réunis. `Gestion` désigne les headers de gestion ; `Consultation` le Bearer d'instance/participation ; `Live` le secret d'installation.

| Famille | Méthodes | Paramètres / payload | Accès client |
| --- | --- | --- | --- |
| `/public/referencement/villes`, `/{id}` | GET | Nom ou identifiant | Aucun |
| `/public/referencement/villes/proches/{rechercher,accueil}` | POST | Origine commune ou coordonnées JSON | Aucun |
| `/public/commercialisation/recherche` | GET | Texte, limites | Aucun |
| `/public/commercialisation/coffrets`, `/{id}`, `/du-moment` | GET | Commune, type, période, limite | Aucun |
| `/protected/referencement/commercants`, `/{id}` | GET | Commune ou identifiant | Aucun |
| `/public/profils/commercants/{id}/page` | GET | Identifiant | Aucun |
| `/public/exploitation/liens-courts/{token}` | GET | Jeton de chemin | Capacité |
| `/public/support/contacts/motifs` | GET | Cible | Aucun |
| `/public/support/contacts/consommateur/messages` | POST | Coordonnées, message, références JSON | Aucun |
| `/public/gestion-achats/paiements/initialiser` | POST | Coordonnées et quantité en query | Idempotence ; crédit/Live facultatifs |
| `/protected/gestion-achats/achats/depuis-session/{id}` | GET | Session checkout | Manquant : MARKET-002 |
| `/protected/gestion-achats/achats/{id}` et instances/prestations | GET | Achat, instance | Gestion |
| `/…/coffrets-instances/{id}/activer` | POST | Bénéficiaire éventuel | Gestion ou activation |
| `/…/envoyer-lien-activation` | POST | Email JSON | Gestion |
| `/protected/gestion-achats/coffrets-instances/{id}` et prestations/QR | GET | Instance | Consultation |
| `/public/gestion-achats/qrcode/detail` | GET | Jeton en query | Capacité |
| `/public/coffrets-instances/{id}/profils-facturation` | GET, POST, PATCH | Profil, version, coordonnées | Jeton d'instance |
| `/public/coffrets-instances/{id}/demandes-facture` et téléchargement | GET, POST | Validation, facturation | Jeton d'instance |
| `/…/achats/{id}/demandes-facture-groupees` et variantes | GET, POST | Validations, facturation | Gestion |
| `/public/credits-achat-b2b/{conditions,otp,sessions,me}` | GET, POST | Code, OTP, conditions | Session pour le compte |
| `/public/animation-locale/animations`, synthèse et détail | GET | Filtres territoriaux, statut, curseur | Aucun |
| `/…/animations/{id}/inscriptions` | POST | Identité et consentements JSON | Idempotence |
| `/…/participants/{token}` et QR | GET | Jeton de chemin | Capacité |
| `/public/localeo-live/configuration` et installations | GET, POST | Préférences initiales | Aucun à la création |
| `/…/installations/{id}/preferences` | GET, PUT | Préférences JSON | Live |
| `/…/abonnements-webpush` et `/{id}` | POST, DELETE | Abonnement Push | Live |
| `/…/installations/{id}/notifications` et lectures | GET, POST | Curseur, notification | Live |
| `/…/installations/{id}/suivis` | POST, DELETE | Ressource et jeton à rattacher | Live + preuve ressource |
| `/…/installations/{id}/animations` et détail | GET | Filtres, animation | Live |
| `/…/coffrets/{id}/passeport`, participations et QR | GET | Ressource | Consultation |
| `/public/exploitation/activites-locales` et métriques | GET | Scopes, filtres, curseur | Aucun |
| `/public/exploitation/feedbacks-prestation/{token}` | GET, POST | Note, commentaire, publication | Capacité |
| `/…/feedbacks-prestation/{metriques,commentaires}` | GET | Filtres, limite | Aucun |

Les lectures de catalogue commerçant sous `/protected` sont accessibles sans dépendance d'authentification dans les routes examinées. Le préfixe ne fait pas autorisation. Le caractère public de chaque champ de contact doit être validé par le métier ; aucune fuite de secret marchand n'est affirmée.

## 7. Gestion des erreurs

Délais : 15 s pour lecture, 30 s pour écriture, 60 s pour téléchargement. Le corps est inclus. Une écriture interrompue est signalée comme incertaine, sans retry automatique.

Limites restantes : confirmation Pro positive après erreur ; affichage direct de certains messages backend ; suppression distante de suivis Live parfois abandonnée lorsque le retrait local réussit ; absence de réconciliation universelle après rechargement ; clés checkout seulement en mémoire ; certaines pannes interprétées comme accès expiré.

Les tests exécutés ne couvrent pas toutes les réponses 401/403/409 de tous les formulaires.

## 8. Concurrence / doubles actions

### MARKET-007 — Inscription non rejouable malgré la clé d'idempotence

- **Sévérité : MOYENNE. Bloquant production : NON isolément.**
- **Localisation :** [AnimationRegistrationForm.jsx](../../../../localeo-marketplace/src/components/AnimationRegistrationForm.jsx), ligne 37 ; [animation_locale_api.py](../../../../localeo-backend/app/api/animation_locale_api.py), ligne 3016 ; [participants_animation.py](../../../../localeo-backend/app/application/animation_locale/services/participants_animation.py), lignes 37–48.
- **Problème / preuve :** le client conserve la clé après erreur ; le backend l'utilise comme corrélation mais ne rejoue pas la réponse. Une adresse déjà inscrite produit un conflit.
- **Scénario :** l'inscription est enregistrée, sa réponse est perdue, le client réessaie avec la même clé et reçoit « déjà inscrit ».
- **Impact :** inscription existante mais parcours local bloqué, sans récupération immédiate du lien. Pas de deuxième inscription démontrée.
- **Correction minimale :** reprise sécurisée donnant le même résultat pour la même clé et le même payload, sans délivrer le jeton d'autrui à partir de son email.

Le checkout particulier utilise un verrou frontend et une clé stable pendant la page. L'achat bénéficie d'une migration d'index unique et d'une clé Stripe liée à l'achat. Live utilise une promesse partagée et un verrou multi-onglets pour l'installation.

Les corrections locales d'activation emploient un verrou de ligne et une contrainte d'unicité des droits. Leur livraison et l'application des migrations restent à prouver. Aucun test transactionnel de double validation sur une base réelle n'a été effectué ici.

## 9. Cloisonnement des données

### MARKET-008 — Accès participant dépendant de la visibilité publique

- **Sévérité : MOYENNE. Bloquant production : NON isolément.**
- **Localisation :** [animation_locale_api.py](../../../../localeo-backend/app/api/animation_locale_api.py), `consulter_participant_animation`, lignes 3029–3033 ; [catalogue_animations_publiques.py](../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py), ligne 275.
- **Problème / preuve :** après validation du jeton, la route recharge l'animation via le catalogue public, soumis notamment à abonnement actif et commune publiée.
- **Scénario / impact :** l'abonnement expire alors que le participant possède un jeton valide : sa page devient indisponible. Le QR direct suit un autre chemin et peut rester accessible.
- **Correction minimale :** projection dédiée au participant authentifié, conforme à la continuité prévue par `MKTANIM-ARB-02`.

Les autres contrôles examinés associent le jeton à l'objet demandé. Les suivis Live vérifient également la preuve d'accès à la ressource.

| Stockage navigateur | Contenu sensible observé |
| --- | --- |
| sessionStorage | Gestion/consultation, accès facturation, brouillon Pro, récapitulatif |
| IndexedDB | Carnet, jetons personnels, secret d'installation, détails sauvegardés |
| Mémoire | Session crédit, coordonnées GPS, résultats React Query |
| Export du carnet | Liens et jetons personnels en JSON |
| Cache service worker | Ressources publiques autorisées |

Le stockage durable Live est un arbitrage explicite. Les capacités restent accessibles aux scripts de la même origine et aux détenteurs du fichier exporté. Les caches privés ne sont pas systématiquement invalidés lors d'un changement de jeton ou d'une révocation ; chaque écriture doit rester revalidée côté serveur.

## 10. Conformité ADR / architecture

Référentiel examiné : [architecture frontend](../../architecture/frontends/marketplace/frontend-architecture-marketplace.md), [conventions CSS](../../architecture/frontends/marketplace/css-architecture.md), [spécification fonctionnelle](../../produit/marketplace/specification-fonctionnelle-marketplace.md), [spécification technique](../../architecture/frontends/marketplace/specification-technique-marketplace.md), [sécurisation](../../specifications/securisation-production/ouverture-marketplace.md), [arbitrages animations](../../specifications/epic-49-animations-marketplace/registre-arbitrages.md), [arbitrages Live](../../specifications/epic-42-localeo-live/registre-arbitrages.md), [Epic 50](../../specifications/epic-50-conformite-fiscale-bum/localeo-marketplace.md), [accueil géolocalisé](../../specifications/epic-52-accueil-marketplace-geolocalise/parcours-utilisateur.md), contrats OpenAPI et [conventions sécurité backend](../../architecture/transverse/conventions-securite.md).

Les écarts majeurs concernent la confidentialité Analytics, les confirmations financières, la continuité des participations, l'idempotence et l'alignement API. Les incohérences documentaires de routage et écarts CSS ne sont pas des bloqueurs.

## 11. Tests

| Vérification réalisée pendant l'audit | Résultat |
| --- | --- |
| `npm run lint` | Réussi |
| Tests ciblés sécurité et serveur | 28/28 réussis |
| Compilation production en mémoire | Réussie |
| Compilation avec configuration réelle, hors hooks d'écriture | Réussie |
| Reproduction Analytics | Jeton dans l'événement |
| Reproduction headers checkout | Headers absents |
| Rendu Pro sans achat | Succès financier affiché |
| Priorité `.env`, fixtures en mémoire | Production remplacée par local |

Tests lancés : `checkout-url.test.cjs`, `request-deadline.test.cjs`, `feed-pagination.test.cjs`, `service-worker.test.cjs` et `server.test.cjs`.

Les tests HTTP utilisent le serveur actuel et les artefacts existants. La compilation en mémoire ne les a pas remplacés. La suite navigateur complète n'a pas été relancée : elle écrit `dist` et des résultats, ce que la mission d'audit interdisait. Les tests backend complets n'ont pas été exécutés. Les résultats historiques ne sont pas une nouvelle recette.

Manquent surtout : contrat retour Stripe B2C/Pro ; absence de fausse confirmation ; absence de jeton dans toutes les émissions Analytics ; reprise d'inscription après réponse perdue ; Pro sans crédit lorsque le crédit est actif ; concurrence PostgreSQL ; révocation avec caches et onglets ouverts.

## 12. Dépendances / build

Lockfile format 3 présent ; dépendances principales cohérentes avec `package.json` ; aucune résolution hors registre npm trouvée. La compilation génère 81 sorties en mémoire, sans source maps. Aucun motif de clé privée ou clé secrète Stripe recherché n'a été trouvé dans les chunks produits : ce n'est pas une preuve exhaustive d'absence de tout secret.

### MARKET-006 — `.env.local` peut remplacer la configuration de production

- **Sévérité : MOYENNE. Bloquant production : NON isolément.** Vérifier le mode de livraison retenu.
- **Localisation :** [write-app-config.cjs](../../../../localeo-marketplace/scripts/write-app-config.cjs), `readEnvFiles`, lignes 45–55.
- **Problème :** `.env.local` est chargé après `.env.production`, contrairement à l'ordre Vite.
- **Scénario / impact :** build production depuis un poste possédant une configuration locale : divergence compilation/runtime ou mauvaise API en hébergement statique. Le serveur Node possède un autre mécanisme runtime.
- **Preuve :** fixtures fictives en mémoire : le générateur en mode production sélectionne l'API staging définie dans `.env.local`.
- **Correction minimale :** harmoniser la résolution avec Vite, ajouter des assertions sur l'environnement final et recetter chaque mode de livraison.

Référence : [priorité des environnements Vite](https://vite.dev/guide/env-and-mode). Le préfixe public large `LOCALEO_` mérite une liste explicite ; aucune exposition effective de secret par ce mécanisme n'est affirmée.

Le contrôle actualisé des avis npm est **NON VÉRIFIÉ**. La requête réseau initiale a échoué et l'escalade a été rejetée par le contrôle automatique d'approbation : l'envoi de l'inventaire des dépendances à npm nécessitait une autorisation explicite. Aucun résultat « zéro vulnérabilité » ne peut en être déduit. La demande actuelle de rédaction n'autorise pas implicitement cette transmission.

## 13. Risques résiduels

Restent à vérifier sur l'environnement déployé : versions servies ; migrations et contraintes ; Analytics ; TLS/CORS/headers CDN ; conservation des traces ; Stripe et réconciliation ; concurrence ; rétention d'assets et rollback ; restauration ; quotas et charge.

Le backend rend CORS paramétrable et désactive les credentials par défaut. Ses valeurs effectives n'ont pas été vérifiées. Les parcours Marketplace utilisent principalement des headers explicites plutôt qu'une authentification par cookie automatiquement jointe.

## 14. Matrice de conformité

| Référence | Règle | État | Preuve / écart |
| --- | --- | --- | --- |
| ADR-001 | BrowserRouter et fallback SPA | ✅ CONFORME | Routage et tests serveur |
| ADR-002 | TanStack Query standard | ⚠️ PARTIEL | Plusieurs flux Live manuels |
| ADR-003 | Configuration runtime | ⚠️ PARTIEL | MARKET-006 |
| ADR-004 | Store session minimal | ⚠️ PARTIEL | Schéma libre, données et capacités multiples |
| Paiement §8.3 | Backend source de vérité | ❌ NON CONFORME côté présentation Pro | MARKET-003 |
| MKTANIM-ARB-11 | Aucun jeton dans Analytics | ❌ NON CONFORME | MARKET-001 |
| MKTANIM-ARB-02 | Continuité participant | ❌ NON CONFORME | MARKET-008 |
| LIVE-ARB-19 | Expiration/révocation explicites | ⚠️ PARTIEL | Certaines erreurs UI ambiguës |
| LIVE-ARB-20 | Carnet IndexedDB explicite | ✅ CONFORME sur le mécanisme | Ajout, retrait, import transactionnel |
| Contrat Live | Idempotence inscription | ❌ NON CONFORME | MARKET-007 |
| Sécurisation F02/F04 | QR passif et diagnostic retiré | ✅ CONFORME dans le code | Rendu image et nettoyage URL QR |
| Sécurisation F06 | Cache public uniquement | ✅ CONFORME sur tests exécutés | Service worker |
| Sécurisation F10 | Délais et incertitude | ✅ CONFORME au niveau HTTP | Tests ciblés |
| Contrat checkout | Client et serveur alignés | ❌ NON CONFORME | MARKET-002 et snapshot API |
| Epic 50 | Pro avec/sans crédit | ⚠️ PARTIEL | MARKET-009 |
| Autorisations | Objet lié au principal | ⚠️ PARTIEL | Contrôles lus ; déploiement et concurrence non certifiés |
| Exploitation | Migrations, restauration, rollback | ❓ NON VÉRIFIABLE | Preuves déployées absentes |

## 15. Plan de remédiation

Le [plan détaillé par application](plan-corrections-backend-marketplace-2026-09-06.md) précise les propriétaires, dépendances et critères d'acceptation.

### P0 — obligatoire avant production

1. Fermer MARKET-001 par suspension ou preuve complète d'absence d'émission sensible.
2. Livrer le contrat sécurisé de retour de paiement et son client : MARKET-002.
3. Retirer toute confirmation positive sans achat serveur : MARKET-003.
4. Ajouter les tests d'intégration et recetter le couple effectivement livré.
5. Vérifier migrations et concurrence pour activation/consommation.
6. Maintenir les fonctionnalités crédit/facturation non recettées désactivées.

### P1 — rapidement après production

Migrer les données hors des URL ; corriger reprise d'inscription et continuité participant ; borner les quantités ; harmoniser le build ; clarifier les erreurs et reprises ; achever le contrôle des dépendances. MARKET-005 doit être clos avant réactivation d'Analytics ; MARKET-009 avant activation du crédit.

### P2 — amélioration

Formaliser le stockage et les invalidations de cache ; renforcer la synchronisation entre onglets ; documenter les rôles ; mesurer chargements N+1 et charge.

## Checklist finale obligatoire

Pour les réponses négatives concernant un exploit ou un secret, « NON » signifie non démontré dans le périmètre inspecté, pas garantie universelle.

| Question | Réponse |
| --- | --- |
| Authentification robuste ? | INCERTAIN — contrôles présents, capacités divulguées par MARKET-001 |
| Autorisations contrôlées côté serveur ? | OUI sur les parcours sensibles examinés |
| Cloisonnement des données garanti ? | INCERTAIN |
| Données sensibles exposées dans le frontend ? | OUI |
| Secrets présents dans le bundle ? | NON détectés par la recherche ciblée |
| Risque XSS sérieux ? | NON démontré dans le code actuel |
| Manipulation de payload dangereuse ? | OUI pour l'intégrité des entrées ; fraude financière non démontrée |
| Double soumission dangereuse ? | NON démontrée ; concurrence encore à valider |
| États frontend/backend cohérents ? | NON |
| Gestion correcte des erreurs critiques ? | NON |
| Violation majeure d'ADR ? | NON pour ADR-001 à ADR-004 ; violations d'arbitrages métier détaillées |
| Build production sain ? | NON entièrement validé — compilation réussie, chaîne de livraison non clôturée |
| Tests des parcours critiques suffisants ? | NON |
| Bloqueur production restant ? | OUI |

## Conclusion obligatoire

> Un utilisateur volontairement malveillant ou simplement confronté à des erreurs réseau, doubles clics, retries ou plusieurs onglets peut-il provoquer une opération métier interdite, une incohérence de données ou accéder à des données qui ne lui appartiennent pas ?

**OUI** pour une incohérence entre l'état financier affiché et l'état serveur. La divulgation de jetons crée également un risque concret d'accès personnel par un tiers. Aucune double consommation ou fraude financière exécutée n'a été démontrée.

> Ai-je identifié un problème qui justifie de repousser la mise en production de cette application ?

**OUI : MARKET-001, MARKET-002 et MARKET-003.**
