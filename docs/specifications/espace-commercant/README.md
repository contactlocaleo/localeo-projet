# Espace commerçant — spécification fonctionnelle et technique

Voir également l’[adresse postale du commerce](adresse-postale.md), règle commune aux profils, à Onboard et aux animations (20 septembre 2026).

## 1. Objet

Les [règles de correction de l'audit](../securisation-production/corrections-commercant-2026-09-05.md) complètent cette spécification et prévalent pour les comportements corrigés.

Révision de référence : remédiation PRO-001 à PRO-012 du 7 septembre 2026.

> **Écart historique d'authentification.** Cette description du 7 septembre
> mentionne encore une connexion de secours par carte QR. La
> [roadmap de l'EPIC 5](../../roadmap/abandonnees/epic-5-session-commercant-securisee-par-qr-code-backlog.md)
> abandonne le mécanisme `qr_commercant` au profit de l'EPIC 10. Les mentions
> de carte conservées ci-dessous décrivent la révision source et ne réouvrent
> pas cette décision produit. La consolidation documentaire ne tranche pas
> l'écart entre cette description et la décision, et ne constitue pas une
> nouvelle vérification du comportement déployé. Le QR client/coffret utilisé
> pour valider une prestation reste distinct de l'authentification commerçant.

Ce document décrit la version de référence de l'application `localeo-commercant` documentée le 7 septembre 2026 ; il ne constitue pas une vérification supplémentaire du déploiement actuel.

Il couvre :
- le périmètre fonctionnel réellement disponible dans le front
- les flux utilisateur
- les dépendances API
- les règles de gestion visibles dans l'interface
- les principaux choix techniques d'implémentation

## 2. Contexte produit

L'application est une PWA destinée aux commerçants Localeo.

Elle permet actuellement :
- la connexion par login/mot de passe et la connexion de secours par carte QR
- l'ouverture et la validation d'une session commerçant
- l'accès à un menu d'actions sécurisé par session
- la validation de prestations à partir d'un QR code de pack
- l'annulation directe d'une prestation récemment validée
- la consultation et la modification du contenu de ses prestations
- la consultation de ses reversements
- l'activation des notifications WebPush de live tracking achats

## 3. Parcours fonctionnels disponibles

## 3.1 Identification commerçant

### Objectif
Permettre au commerçant de se connecter par login/mot de passe ou par sa carte QR. Le serveur authentifie les deux parcours.

### Entrée utilisateur
- login et mot de passe (parcours principal)
- carte QR commerçant, scannée ou saisie, comme autre mode de connexion

### Comportement
- l'application ouvre une session après authentification du login ou du QR côté serveur
- en cas de succès, elle conserve les informations de session
- en cas d'échec, elle affiche un message d'erreur et permet de recommencer

### Résultat attendu
- succès : accès au menu principal
- échec : retour à l'étape d'identification avec message

### Données utilisées
- `session_token`
- `expires_at`
- `scopes`
- `commercant`
- `session_id` si retourné par l'API de validation de session

## 3.2 Contrôle de session

### Objectif
Garantir qu'aucune action métier n'est accessible si la session commerçant n'est plus valide.

### Règles appliquées
- la session est validée avant l'affichage du menu
- la session est revalidée au clic sur une action du menu
- une session expirée ou refusée renvoie vers l'écran d'identification
- la déconnexion efface immédiatement la session locale et le contexte de validation, puis demande la révocation backend avec un délai borné
- l'expiration est contrôlée aussi sans navigation, par temporisation et retour du focus

### Persistance locale
- la session est stockée dans `sessionStorage`
- la session est restaurée au rechargement tant qu'elle n'est pas expirée

## 3.3 Menu principal

### Actions affichées
- `Valider une prestation`
- `Consulter mes reversements`
- `Animer / modifier le contenu de mes prestations`
- `Contacter Localeo`

### Informations visibles
- nom du commerçant
- statut du commerçant
- statut de la carte commerçant
- date de fin de session au format local
- bouton discret de copie de l'identifiant commerçant
- heure locale dans la barre haute

## 3.4 Validation d'une prestation

### Objectif
Permettre au commerçant de valider la ou les prestations d'un pack après scan du QR code pack.

### Étapes
1. Le commerçant clique sur `Valider une prestation`
2. L'application demande le scan du QR code pack ou sa saisie manuelle
3. L'application ouvre une transaction de validation
4. Elle récupère l'instance de pack et les prestations associées
5. Elle affiche le résumé du pack et la liste des prestations
6. Le commerçant peut valider uniquement ses prestations non encore validées

### Règles d'affichage
- les prestations déjà validées affichent leur date de validation
- les prestations du commerçant connecté affichent un bouton `Valider la prestation`
- l'API de prestations filtre les résultats sur le commerçant connecté ; leur nombre ne représente pas le total du coffret
- le champ `Statut des prestations dans votre commerce` porte uniquement sur les prestations du commerçant connecté : `EN COURS` s'il en reste à valider, `TERMINÉ` si toutes sont validées, `Aucune prestation` si aucune ne lui est attribuée ; il ne décrit pas le statut global du coffret
- le statut de l'instance est relu après validation, annulation et actualisation ; un échec de relecture affiche `À actualiser`
- après une validation confirmée, un écran dédié affiche `Validation confirmée`, le statut actualisé des prestations dans le commerce, les prestations du commerçant et `Scanner un autre QR`, sans historique horodaté ni message technique de reprise
- si l'actualisation échoue sur cet écran, la confirmation reste affichée, mais le résumé obsolète est masqué jusqu'à une relecture réussie

### Données pack affichées
- nom du pack
- date d'expiration
- statut
- progression de validation chez le commerçant connecté, libellée `Prestations consommées chez vous`

### Règles d'identification métier
- le nom des prestations est résolu à partir du détail du pack
- le nom du commerçant porteur est résolu via l'API commerçant

### Annulation directe d'une validation récente
Quand une prestation du commerçant connecté a déjà été validée, l'interface peut proposer une action `Annuler la validation`.

Cette action est disponible uniquement si :
- la prestation appartient au commerçant connecté
- l'API retourne un identifiant de validation exploitable
- la validation date de moins de la fenêtre autorisée

La fenêtre d'annulation est configurable côté front par `LOCALEO_VALIDATION_PRESTATION_API_ANNULATION_MAX_HOURS`.
La valeur par défaut est `24` heures.

L'annulation demande :
- un motif obligatoire d'au moins 10 caractères
- un commentaire optionnel
- une confirmation explicite avant envoi

Après succès, la liste des prestations du pack est rechargée afin d'afficher l'état backend à jour.
Les cas hors délai, sans identifiant de validation, ou refusés par le backend restent traités hors parcours direct, par exemple via le support ou le back-office Localeo.

## 3.5 Consultation / modification des prestations

### Objectif
Permettre au commerçant de consulter ses prestations et de modifier uniquement le contenu autorisé.

### Liste
L'application charge la liste des prestations du commerçant connecté et affiche pour chaque prestation :
- nom
- pack associé
- statut
- montant reversé

### Détail / édition
Le panneau d'édition affiche :
- nom de la prestation
- description
- pack associé
- statut
- montant reversé au commerçant en lecture seule

### Champs modifiables
- `libelle`
- `description`

### Champs non modifiables
- `montant_reversement`
- `statut`
- rattachements techniques

### Règles d'éditabilité
L'édition est disponible uniquement si `LOCALEO_FEATURE_MERCHANT_PRESTATION_EDIT_ENABLED=true` est défini dans l'environnement de compilation. Sans cette variable, ou avec toute autre valeur, la liste et le détail restent consultables en lecture seule : aucun formulaire d'édition ni envoi de modification depuis le client.

Comme les autres flags publics Vite, un changement de valeur nécessite une nouvelle compilation et un déploiement. Ce flag pilote l'application commerçant ; les autorisations de l'API restent gérées par le backend.

Seules les prestations dans les statuts suivants sont modifiables :
- `ACTIVE`
- `BROUILLON`
- `REFERENCE`

Toute prestation dans un autre statut est consultable mais non modifiable.

### Sauvegarde
- le bouton `Enregistrer` n'est actif que s'il y a des changements
- en cas de succès, la liste est rechargée
- un message de confirmation est affiché

## 3.6 Consultation des reversements

### Objectif
Permettre au commerçant de consulter les montants à reverser et l'historique des reversements effectués.

### Bloc 1 - Mouvements à reverser
L'application affiche un tableau synthétique des mouvements à reverser avec :
- prestation
- montant
- statut
- date du mouvement

### Calcul total
Le total à reverser est calculé côté front par somme des montants de mouvements retournés par l'API.

### Bloc 2 - Historique
L'application affiche l'historique des reversements sur les 12 derniers mois avec :
- identifiant du reversement
- montant total
- statut
- nombre de mouvements
- date de création
- date d'exécution
- référence de paiement si disponible

### Limitation actuelle
Le bloc de détail prestation dans la vue reversements a été retiré de cette version.

## 3.7 Contacter Localeo

### État de la fonctionnalité
Le parcours est implémenté : choix d'un motif fourni par l'API, saisie d'un message et envoi au support avec contexte commerçant authentifié. La confirmation n'est affichée qu'après succès serveur.

## 3.8 Live tracking achats / WebPush

### Concept Localeo
Le WebPush est le canal de notification temps réel de l'application commerçant.
Il permet à Localeo de prévenir un appareil du commerçant lorsqu'un achat confirmé contient une prestation rattachée à son commerce, même si l'application n'est pas ouverte au premier plan.

Ce canal n'est ni un email, ni un SMS.
Il repose sur l'autorisation de notification donnée par le navigateur et sur un abonnement technique propre à chaque appareil.

### Parcours d'activation
L'activation est disponible dans `Mes informations personnelles`, section `Live tracking achats`.

Le commerçant doit :
1. activer la préférence de live tracking pour son compte
2. autoriser les notifications dans le navigateur
3. abonner l'appareil courant

Si la préférence est active mais que l'appareil courant n'est pas encore abonné, l'interface affiche un message indiquant que le live tracking est actif pour le compte mais pas encore pour cet appareil.
Un même commerçant peut donc recevoir les notifications sur plusieurs appareils, à condition que chaque appareil soit abonné.

### Sécurité et données envoyées
La notification WebPush ne doit pas contenir de données personnelles client ni d'identifiants métier directs comme `achat_id` ou `coffret_id`.
Le payload transporte uniquement un message lisible et un deeplink opaque.

Au clic sur la notification :
- l'application commerçant est ouverte ou ramenée au premier plan
- aucune session n'est créée automatiquement
- le deeplink est résolu uniquement après authentification avec une session commerçant valide

## 3.9 Demandes de participation aux animations

Les demandes de participation sont séparées des animations déjà acceptées. Depuis `Mes animations`, le commerçant accède à une liste dédiée présentant les demandes qui nécessitent une réponse et l'historique de ses décisions.

Le détail d'une demande restitue la version présentée par le backend : organisateur, commune, dates, description, règlement et sa version, mission du commerçant, consignes, contraintes pratiques, contact et date limite de réponse.

Le commerçant peut :

- accepter directement avec un engagement explicite visible, sans écran de confirmation supplémentaire ; pour une chasse, confirmer globalement les préparatifs affichés de la mission choisie (accord non précoché) ;
- refuser après une confirmation explicite, avec un motif facultatif limité à 1 000 caractères ;
- retirer une acceptation, directement avant publication ou sous forme de demande traitée par le partenaire après publication.

Une échéance dépassée désactive les décisions et explique que le partenaire doit prolonger la date limite. Les commandes portent une clé d'idempotence. Les liens reçus par notification ouvrent directement la demande, mais la route reste protégée par la session commerçant.

Après acceptation et publication, le détail de l'animation affiche la mission et le règlement courants. Un bloc « Flyer de l’animation » figure dans cette vue ainsi que dans le détail d’une participation acceptée. Lorsque le backend confirme sa disponibilité, le commerçant peut télécharger le PDF ou l’ouvrir pour impression. Pendant le chargement ou en cas de réponse `404`, le bouton de téléchargement reste désactivé et un message explique l’indisponibilité. « Actualiser le flyer » permet de vérifier à nouveau sa disponibilité sans quitter la fiche. Le document reste inaccessible avant publication.

L’évolution [E56-UX-01](../epic-56-validation-participation-commercants-animation/README.md#e56-ux-01--préparation-commerçant-simplifiée-26-septembre-2026)
donne priorité à la mission et aux deux gestes de préparation : télécharger le
kit, puis déclarer le commerce prêt lorsque le serveur l’autorise. Règlement,
guide complet et flyer séparé se consultent à la demande. L’accord de participation
et la déclaration de préparation restent deux décisions distinctes.

Depuis E55-UX-12, le kit d’une chasse contient aussi `qr-lieu.pdf`, QR opaque
`LQL1` du lieu à scanner dans Localeo Live. Ce document est distinct de
`flyer-joueurs.pdf`, dont le QR URL ouvre le support explicitement autorisé
(`supportAccessibleParQr: true`) ou l’inscription. Les consignes et le guide
privés ne sont pas rendus publics par cette évolution.

Le backend prépare le QR commerce dans la transaction d’acceptation. Pour les
accords historiques, **Télécharger mon kit** appelle la commande de préparation
avant de lire le ZIP, sans demander une confirmation supplémentaire. Les GET
du kit restent sans écriture. L’interface verrouille le téléchargement pendant
la commande ; un refus ou un résultat incertain reste visible et ne déclenche
aucun renvoi automatique. **Je suis prêt** conserve sa commande indépendante.
Le gestionnaire prépare uniquement les supports des POI ; son bloc disparaît
si le parcours ne comporte aucun lieu public.

## 4. APIs utilisées

## 4.1 Authentification / session
- `POST /protected/identite-acces/commercants/auth/login`
- `POST /protected/identite-acces/commercants/auth/mot-de-passe-oublie`
- `POST /protected/identite-acces/commercants/auth/initialiser-mot-de-passe`
- `POST /protected/identite-acces/commercants/auth/reinitialiser-mot-de-passe`
- `GET /protected/identite-acces/commercants/session/valider`
- `POST /protected/identite-acces/commercants/session/{session_id}/invalider`

## 4.2 Validation de prestation
- `POST /protected/exploitation/validation/ouvrir-transaction`
- `GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}`
- `GET /protected/gestion-achats/achats/{achat_id}/coffrets-instances/{coffret_instance_id}/prestations`
- `GET /public/coffrets/{coffret_id}`
- `GET /protected/referencement/commercants/{commercant_id}`
- `POST /protected/exploitation/validation/valider-prestation`
- `POST /protected/exploitation/validation/validations/{validation_prestation_id}/annuler`

## 4.3 Prestations commerçant
- `GET /protected/commercialisation/commercants/{commercant_id}/prestations`
- `GET /protected/commercialisation/commercants/{commercant_id}/prestations/{prestation_id}`
- `PATCH /protected/commercants/me/prestations/{prestation_id}`

## 4.4 Reversements
- `GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mouvements/a-reverser`
- `GET /protected/gestion-reversement/commercants/{commercant_id}/reversements/mois/{nb_mois}`

## 4.5 Contact Localeo
- `GET /public/contacts/motifs?cible=COMMERCANT`
- `POST /protected/commercants/{commercant_id}/messages`
- `GET /protected/commercants/{commercant_id}/messages`
- `GET /protected/commercants/{commercant_id}/messages/{thread_id}`
- `POST /protected/commercants/{commercant_id}/messages/{thread_id}/reponses`

## 4.6 Notifications WebPush
- `GET /protected/commercants/me/notifications/preferences`
- `PATCH /protected/commercants/me/notifications/preferences`
- `GET /protected/commercants/me/webpush/abonnements`
- `POST /protected/commercants/me/webpush/abonnements`
- `DELETE /protected/commercants/me/webpush/abonnements/{abonnement_id}`
- `POST /protected/commercants/me/webpush/deeplinks/resoudre`

## 4.7 Participation aux animations

- `GET /protected/animation-locale/commercants/me/demandes-participation`
- `GET /protected/animation-locale/commercants/me/demandes-participation/{id}`
- `POST /protected/animation-locale/commercants/me/demandes-participation/{id}/accepter`
- `POST /protected/animation-locale/commercants/me/demandes-participation/{id}/refuser`
- `POST /protected/animation-locale/commercants/me/demandes-participation/{id}/retirer`
- `GET /protected/animation-locale/commercants/me/animations/{id}/flyer`
- `GET /protected/animation-locale/commercants/me/animations/{id}/flyer/download`
- `DELETE /protected/animation-locale/commercants/me/notifications/{id}`

L'accueil expose en permanence un accès aux invitations Animation et met en avant les demandes en attente dans la zone « À traiter ». L'espace Animation possède une navigation commune entre invitations, animations acceptées et notifications. Une date limite fournie sans heure reste valide jusqu'à la fin de la journée locale concernée. Les notifications Animation peuvent être supprimées individuellement afin de maîtriser leur accumulation.

La liste `/animations/invitations` affiche la commune, l'organisateur, les dates de l'animation, la date de réception (« Reçue le », issue de `premier_envoi_at`) et la date limite de réponse, y compris dans l'historique. Une relance ne remplace pas la date de réception initiale. La réponse paginée fournit un résumé `animation` (`id`, `nom`, `commune`, `date_debut`, `date_fin`) et `organisateur`, sans charger le détail de chaque invitation. Le nom, les dates et l'organisateur proviennent du contenu présenté lors de l'envoi ; les communes sont chargées en lot côté serveur. Le contenu complet reste réservé au détail autorisé.

## 5. Architecture technique front

## 5.1 Stack
- React
- Vite
- PWA via manifeste web
- Service worker pour la réception WebPush
- CSS natif sans framework UI

## 5.2 Organisation actuelle

Le front est actuellement concentré principalement dans :
- `src/App.jsx`
- `src/styles.css`

### Workspaces d'action implémentés
- `ValidationActionWorkspace`
- `PrestationsActionWorkspace`
- `ReversementsActionWorkspace`
- pages Animation modulaires : liste et détail des animations acceptées, notifications, liste et détail des demandes de participation

## 5.3 Gestion des états

### État global
`App.jsx` gère notamment :
- la session commerçant authentifiée
- la vue courante
- l'action sélectionnée
- le contrôle périodique d'heure locale affichée
- les préférences et abonnements WebPush du commerçant

### États locaux par workspace
Chaque écran métier gère ses propres états :
- chargement
- erreur
- sélection
- formulaire
- confirmation

## 5.4 Persistance

La session commerçant est persistée dans :
- `window.sessionStorage`

Clé utilisée :
- `localeo-merchant-session` : Bearer, expiration et identité de session
- `localeo-validation-recovery` : identifiants de transaction/coffret, propriétaire de session et expiration, sans QR ni Bearer ; relecture serveur obligatoire à la reprise

## 5.5 Sécurité d'accès

Les appels sécurisés utilisent :
- `Authorization: Bearer <session_token>`

Le front ne se repose pas uniquement sur la date d'expiration locale.
Il appelle également l'API de validation de session avant les parcours sensibles.

## 5.6 Proxy API en développement

Le projet utilise un proxy Vite en développement pour appeler les APIs locales sans problème de CORS.

Principe :
- le front appelle `/api/...`
- Vite proxifie vers la cible backend locale configurée

## 6. Règles de gestion visibles

## 6.1 Session
- une session non valide bloque l'accès au menu et aux actions
- une session expirée renvoie vers l'écran d'identification

## 6.2 Prestations
- seules `ACTIVE`, `BROUILLON`, `REFERENCE` sont modifiables
- seul le nom et la description sont modifiables
- le montant reversé est informatif

## 6.3 Validation pack
- un commerçant ne peut valider que ses propres prestations
- un pack avec toutes ses prestations validées est présenté comme terminé
- une validation récente peut être annulée depuis l'interface si le délai configuré n'est pas dépassé
- l'annulation directe reste soumise aux contrôles backend

## 6.4 Reversements
- la somme totale à reverser est calculée à partir des mouvements à reverser
- l'historique affiché porte sur 12 mois

## 6.5 WebPush
- l'activation est volontaire et se fait par compte commerçant puis par appareil
- un navigateur qui ne supporte pas WebPush ou qui refuse les notifications ne peut pas recevoir d'alerte
- les notifications ne contiennent pas de données personnelles ni d'identifiants métier directs
- la navigation depuis une notification nécessite une session commerçant valide

## 7. Limites connues de cette version

- Le code front reste largement centralisé dans `src/App.jsx`
- La vue reversements n'affiche plus de bloc de détail prestation dans sa version actuelle
- Certaines pages secondaires utilisent encore un point d'entrée générique

## 8. Références du projet

- Contrat API attendu dans le dépôt commerçant : `api/localeo-openapi.json`. Son absence au 18 septembre 2026 et les consommateurs affectés sont décrits dans [la source des contrats](contrats-api.md#source-des-contrats--pro-012).
- [Contrats API consommés](contrats-api.md).
- [EPIC édition des prestations](../../roadmap/terminees/epic-animation-edition-prestations.md).
- [Parcours canonique de validation des prestations](../validation-prestations/README.md).
- [Ancien parcours de validation à deux scans](../archives/validation-prestation-deux-scans.md), conservé comme archive et non comme contrat d'implémentation.


## 9. Règles de remédiation préproduction

- Un HTTP 409 ou un statut ANOMALIE ne confirme jamais une validation. VALIDEE est obligatoire.
- Les commandes ont un délai de 15 secondes sans retry automatique. Une confirmation POST reste distincte de la lecture suivante ; une lecture échouée bloque les actions coffret jusqu'à réconciliation.
- Une transaction coffret consommée impose un nouveau scan pour une autre prestation. Un rechargement ne rejoue aucune commande.
- Les QR sont envoyés en JSON aux endpoints de scan, jamais dans leurs URLs techniques. Les jetons de mot de passe quittent l'URL par remplacement d'historique et restent seulement en mémoire.
- Les listes Animation parcourent toutes les pages annoncées ; une réponse partielle ou répétée n'est pas présentée comme complète.
- Une action interdite par le serveur ne peut pas être réactivée localement. Un timestamp à minuit demeure un instant ; seul YYYY-MM-DD est une date civile.
- Les décisions d'invitation conservent une clé par commande incertaine et bloquent les doubles clics. Un conflit impose relecture et nouveau choix.
- Finance suit le contrat de l'Epic 50 ; ses quatre options sont désactivées dans la configuration de production jusqu'à recette et décision produit.
- La CI utilise Node 22.19 ou ultérieur, npm ci, tests, build, scénarios Playwright/axe et Lighthouse local sans publication des rapports.

Voir le [registre de remédiation](../../audits/commercant/remediation-preproduction-2026-09-06.md), le [guide de formation](../../produit/formation/commercant/guide-commercant.md) et le [guide de mise en production](../../exploitation/commercant/mise-en-production.md).

[Retour à l’index des spécifications](../INDEX.md)
