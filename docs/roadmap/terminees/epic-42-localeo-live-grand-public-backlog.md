# Backlog Epic 42 - Localeo Live grand public

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : creer une application grand public `Localeo Live` dediee aux utilisateurs finaux, distincte des surfaces internes et partenaires, pour decouvrir l'activite locale, suivre ses participations, ses coffrets, ses animations et recevoir des notifications utiles.
- Prerequis obligatoire : renommer l'application interne actuelle `Localeo Live` en `Localeo Control` afin de reserver le nom `Localeo Live` a l'experience grand public.
- Pourquoi maintenant : le nom `Localeo Live` porte mieux une experience publique de proximite, d'activite locale et de participation qu'une console interne d'exploitation. La clarification de marque evite la confusion entre supervision interne, portail partenaire et application utilisateur.
- Domaine fonctionnel cible : `experience_publique`, avec integrations vers `gestion_achats`, `animation_locale`, `commercialisation`, `referencement`, `support` et notifications.
- Surfaces concernees :
  - `Localeo Control` : nouvelle denomination de l'actuelle PWA interne d'exploitation.
  - `Localeo Live` : nouvelle application grand public mobile/PWA.
  - marketplace web : point d'entree public vers l'application et les parcours Live.
  - application commercant : surface complementaire pour validations terrain, sans devenir l'application grand public.

## Decisions de cadrage initiales

- `Localeo Live` devient le nom reserve a l'application grand public.
- L'actuelle PWA d'exploitation interne ne doit plus utiliser le nom `Localeo Live` dans les libelles, manifest, notifications, routes documentees ou guides ; elle devient `Localeo Control`.
- `Localeo Control` reste une surface interne authentifiee, reservee aux profils back-office autorises.
- `Localeo Live` vise les utilisateurs finaux : acheteurs, beneficiaires de coffrets, participants a des animations locales, gagnants et visiteurs interesses par la vie locale.
- Le MVP ne comporte aucun compte client : consultation de coffret et suivi de participation reposent sur des tokens opaques.
- L'utilisateur peut sauvegarder volontairement ses liens personnels dans une bibliotheque locale sur son appareil ; aucune synchronisation multi-appareils n'est proposee au MVP.
- Une evolution post-MVP permet d'activer explicitement un carnet anonyme persistant, de l'appairer a plusieurs appareils et de le recuperer par passkey sans creer de compte client.
- Les animations locales de l'Epic 41 sont un cas d'usage structurant pour `Localeo Live`, mais l'application ne doit pas etre limitee a ce seul domaine.
- Les notifications push grand public doivent etre distinctes des WebPush internes `Localeo Control` et des notifications commercants.
- La marketplace est le canal d'acquisition prioritaire : mise en avant editoriale, CTA d'installation, QR desktop et deep links mobile.
- Le MVP propose un passeport graphique pour les coffrets en cours, une inbox persistante et des preferences WebPush par categorie et commune.
- Le feed reutilise la projection et le vocabulaire `activites_locales` de l'Epic 16 ; aucun type `explorateur` n'est introduit.
- Les news sont des activites editoriales creees manuellement, globales ou scopees sur une ou plusieurs villes du referentiel existant.
- Les actualites rattachees a une animation sont gerees depuis Localeo Animation, reutilisent `activites_locales`, apparaissent dans `En direct > Animations` et respectent la preference de notification `ANIMATION`.
- La commune est choisie manuellement au MVP ; aucune geolocalisation n'est demandee.
- Localeo Live est une PWA autonome integree au projet `localeo-marketplace`, sous les routes `/live/*`.
- Le mode hors ligne porte le shell et les derniers contenus publics, mais exclut le cache durable des QR et tokens sensibles.
- Chaque affichage d'un QR personnel de passeport ou de participation exige une verification locale de l'utilisateur par le verrouillage securise de l'appareil, sans creer de compte ni de session client cote serveur.
- Specifications detaillees : `docs/specifications/epic-42-localeo-live/`.

## User Stories

1. `PRD-371` En tant qu'operateur Localeo, je veux renommer l'application interne actuelle `Localeo Live` en `Localeo Control` afin de liberer le nom `Localeo Live` pour l'application grand public.
   - Statut : `Termine`
   - Resultat attendu : les libelles visibles de la PWA interne, la page d'accueil backend, les manifestes, les titres, les documentations et les notifications internes utilisent `Localeo Control`.
   - Resultat attendu : les routes techniques existantes peuvent etre conservees temporairement si necessaire, mais les libelles publics et operationnels ne doivent plus exposer `Localeo Live` pour la console interne.
   - Resultat attendu : une note de migration liste les impacts de renommage pour les operateurs.

2. `PRD-372` En tant que responsable produit, je veux definir l'identite produit de `Localeo Live` grand public afin de cadrer clairement sa promesse et ses limites.
   - Statut : `A faire`
   - Resultat attendu : une expression de besoin decrit cible, proposition de valeur, parcours principaux, exclusions MVP et articulation avec marketplace, portail partenaire, application commercant et `Localeo Control`.
   - Resultat attendu : les termes `Localeo Live`, `Localeo Control`, `Marketplace Localeo`, `Portail partenaire` et `Application commercant` sont distingues.

3. `PRD-373` En tant qu'utilisateur grand public, je veux installer ou ouvrir `Localeo Live` sur mobile afin d'acceder rapidement a mes contenus Localeo.
   - Statut : `A faire`
   - Resultat attendu : l'application est pensee mobile first et installable en PWA ou deployable en application mobile selon arbitrage technique.
   - Resultat attendu : l'accueil permet d'acceder aux coffrets, animations, activites locales et notifications pertinentes.

4. `PRD-374` En tant qu'utilisateur, je veux consulter mes coffrets et QR depuis `Localeo Live` afin de retrouver facilement mes achats ou cadeaux.
   - Statut : `A faire`
   - Resultat attendu : un coffret accessible par token, compte ou lien securise peut etre affiche dans l'application.
   - Resultat attendu : le QR, les prestations restantes, les dates utiles et les informations commerçants sont lisibles sur mobile.
   - Resultat attendu : l'application respecte les regles de securite existantes des tokens de consultation et d'activation.

5. `PRD-375` En tant que participant, je veux suivre mes animations locales dans `Localeo Live` afin de voir ma progression, mon QR participant et mes gains.
   - Statut : `A faire`
   - Resultat attendu : les participations issues de l'Epic 41 sont consultables dans l'application.
   - Resultat attendu : le participant voit les etapes validees, restantes, son statut de qualification, les tirages et les gains eventuels.

6. `PRD-376` En tant qu'utilisateur local, je veux decouvrir les activites, animations, commercants et coffrets autour de moi afin de participer a la vie locale.
   - Statut : `A faire`
   - Resultat attendu : l'application propose une entree par commune ou localisation choisie.
   - Resultat attendu : les contenus publics proviennent des domaines existants sans duplication des referentiels ville, commercant, coffret ou animation.
   - Resultat attendu : la geolocalisation precise reste optionnelle et soumise a consentement.

7. `PRD-377` En tant qu'utilisateur, je veux recevoir des notifications utiles afin de ne pas rater une validation, une animation, un gain, une expiration ou une actualite locale importante.
   - Statut : `A faire`
   - Resultat attendu : les notifications grand public sont separees techniquement et fonctionnellement des notifications `Localeo Control` et commercants.
   - Resultat attendu : l'utilisateur peut accepter, refuser et parametrer les categories de notifications.
   - Resultat attendu : les contenus de notification restent sobres et ne divulguent pas de donnees sensibles.

8. `PRD-378` En tant qu'utilisateur, je veux activer un carnet anonyme persistant afin de synchroniser mes coffrets et animations entre mes appareils sans creer de compte client.
   - Statut : `A faire - evolution backend/frontend post-MVP initial`
   - Resultat attendu : le mode local historique reste disponible tant que l'utilisateur n'active pas explicitement la synchronisation.
   - Resultat attendu : le carnet partage contient les passeports/coffrets, participations Animation, favoris et configurations fonctionnelles partageables, sans email, telephone ou mot de passe Localeo.
   - Resultat attendu : chaque appareil conserve une installation et un secret distincts ; les abonnements WebPush et permissions systeme restent locaux.
   - Resultat attendu : un appareil proprietaire peut appairer un nouvel appareil avec une invitation courte, a usage unique et confirmee, par QR ou par code temporaire pour un PC sans camera.
   - Resultat attendu : une passkey enregistree au prealable permet de recuperer le carnet lorsqu'aucun ancien appareil n'est disponible.
   - Resultat attendu : les tokens Coffret et Participant sont valides lors de l'ajout mais ne sont ni persistes dans le carnet ni transmis aux autres appareils.
   - Resultat attendu : un proprietaire peut lister et revoquer les appareils rattaches.
   - Specifications detaillees : [docs/specifications/epic-42-localeo-live/carnet-partage-backend.md](../../specifications/epic-42-localeo-live/carnet-partage-backend.md) et `carnet-partage-frontend.md`.

9. `PRD-379` En tant que responsable conformite, je veux que `Localeo Live` respecte les exigences RGPD, consentements et minimisation afin de limiter les risques sur une application grand public.
   - Statut : `A faire`
   - Resultat attendu : les donnees collectees, finalites, bases legales, durees de conservation, consentements push/geolocalisation et droits utilisateur sont documentes.
   - Resultat attendu : les donnees enfant/mineur ou animation scolaire sont explicitement cadrees si le cas d'usage est retenu.
   - Resultat attendu : les politiques publiques sont identifiees avant mise en production.

10. `PRD-380` En tant que responsable produit, je veux mesurer l'usage de `Localeo Live` afin de piloter l'adoption sans compromettre la vie privee.
    - Statut : `A faire`
    - Resultat attendu : les indicateurs MVP distinguent installations/ouvertures, consultations de coffrets, inscriptions animations, validations vues, notifications opt-in et interactions avec contenus locaux.
    - Resultat attendu : les indicateurs sont agreges, minimises et compatibles avec les consentements applicables.
    - Resultat attendu : `Localeo Control` peut afficher une supervision agregee de l'usage public sans exposer de donnees personnelles inutiles.

11. `PRD-403` En tant que beneficiaire consultant le detail securise de mon coffret, je veux l'ajouter directement a Localeo Live afin de ne pas recopier son lien.
    - Statut : `A faire - evolution frontend`
    - Resultat attendu : la vue detaillee du coffret affiche `Ajouter a mes coffrets Localeo Live`, ou `Ouvrir dans Localeo Live` si le coffret est deja present localement.
    - Resultat attendu : sur la meme origine, le transfert temporaire de l'identifiant et du token utilise `sessionStorage`, puis les donnees de transfert sont supprimees des que Localeo Live les a lues.
    - Resultat attendu : un fallback par fragment `#token=...` est disponible si le transfert local est impossible ; le fragment est retire immediatement de l'adresse.
    - Resultat attendu : Localeo Live verifie le token via le backend avant de proposer l'ajout volontaire dans IndexedDB.
    - Resultat attendu : l'ajout a la bibliotheque et l'activation du suivi/WebPush restent deux consentements distincts.
    - Resultat attendu : l'email de confirmation peut conserver `Consulter mon coffret` et proposer en complement un raccourci `Ajouter a Localeo Live`.

12. `PRD-404` En tant qu'utilisateur Localeo Live, je veux initialiser l'application sans accepter WebPush et consulter clairement mes participations afin que les fonctions locales ne dependent pas du consentement aux notifications.
    - Statut : `Termine - backend`
    - Resultat attendu : `POST /public/localeo-live/installations` retourne un identifiant opaque et un secret une seule fois, sans creer d'abonnement Push.
    - Resultat attendu : la projection et le QR d'une participation sont exposes sous `/public/localeo-live/participations/{participation_id}`.
    - Resultat attendu : le token participant est transmis par Bearer et n'apparait dans aucun chemin Localeo Live.
    - Resultat attendu : le consentement WebPush peut intervenir ulterieurement et reste facultatif.

13. `PRD-413` En tant que client Localeo, je veux retrouver un acces coherent a Localeo Live dans les emails lies a mes coffrets et animations afin de poursuivre mon parcours depuis mon telephone.
    - Statut : `Termine - backend`.
    - Resultat attendu : les emails beneficiaires Coffret et participant Animation affichent un pied HTML et texte commun, contextualise selon le domaine.
    - Resultat attendu : le lien profond d'ajout est utilise lorsqu'un token de consultation ou participant est disponible ; sinon `LOCALEO_FRONT_LIVE_URL` sert de repli.
    - Resultat attendu : le CTA reste secondaire par rapport a l'action transactionnelle du message et n'est pas ajoute aux emails commercants, partenaires, finance ou support.
    - Resultat attendu : aucun token n'est ajoute aux logs ou aux parametres de suivi.

14. `PRD-414` En tant qu'utilisateur Localeo Live, je veux confirmer localement mon identite avant d'afficher un QR personnel afin d'eviter qu'une personne utilisant temporairement mon appareil puisse presenter mon passeport ou ma participation.
    - Statut : `A faire - frontend`.
    - Resultat attendu : chaque action `Afficher le QR code` d'un passeport/coffret ou d'une participation Animation declenche une verification locale WebAuthn avec `userVerification=required`.
    - Resultat attendu : le systeme d'exploitation choisit le moyen disponible parmi biometrie, code de deverrouillage ou mecanisme equivalent ; Localeo ne recoit aucune donnee biometrique.
    - Resultat attendu : le QR n'est demande au backend et injecte dans le DOM qu'apres une verification reussie ; il n'est conserve ni dans IndexedDB ni dans le cache du service worker.
    - Resultat attendu : le QR est masque des que la PWA devient inactive, quitte l'ecran ou depasse sa duree d'affichage, et toute nouvelle ouverture exige une nouvelle verification.
    - Resultat attendu : le credential de protection est propre a l'appareil et ne constitue ni un compte client ni une session d'authentification serveur.
    - Resultat attendu : si aucun authentificateur de plateforme compatible n'est disponible ou configure, le QR reste masque et l'application explique comment activer le verrouillage de l'appareil ; aucun affichage non protege n'est autorise.
    - Resultat attendu : le fonctionnement est teste sur les navigateurs cibles en HTTPS ainsi que sur `localhost` pour le developpement.

## Hors MVP initial

- Remplacement de la marketplace web par `Localeo Live`.
- Fusion des comptes commercants, gestionnaires et utilisateurs grand public.
- Reseau social local complet, messagerie publique ou publication libre par les utilisateurs.
- Programme de fidelite transverse complexe non rattache aux coffrets ou animations.
- Gamification avancee hors besoins des animations locales cadrees.
- Geolocalisation permanente en arriere-plan.

## Arbitrages valides

- PWA integree a `localeo-marketplace` sous `/live`, avec manifeste, service worker et bundle dedies.
- Aucun compte au MVP ; acces par token et sauvegarde locale des liens.
- L'evolution de carnet partage conserve l'absence de compte : elle introduit un carnet pseudonyme, des installations par appareil, un appairage explicite et une recuperation WebAuthn.
- Feed complet + coffrets + animations + notifications dans le MVP, livre progressivement.
- News manuelles, globales ou scopees sur zero, une ou plusieurs villes du referentiel existant.
- Choix manuel obligatoire de la commune au MVP.
- Registre complet : [docs/specifications/epic-42-localeo-live/registre-arbitrages.md](../../specifications/epic-42-localeo-live/registre-arbitrages.md).
- Les arbitrages produit et techniques `LIVE-ARB-01` a `LIVE-ARB-40` sont valides. `LIVE-ARB-39` dissocie l'installation technique du consentement WebPush et explicite la facade des participations. `LIVE-ARB-40` impose une verification locale WebAuthn avant chaque affichage d'un QR personnel.

## Decoupage en lots backend

| Lot | Statut | Contenu | Dependances | Sortie attendue |
| --- | --- | --- | --- | --- |
| B0 | Termine | Architecture backend et contrat OpenAPI 3.1 | Arbitrages valides, Epic 41 stabilisee | OpenAPI reproductible de 29 chemins, schemas, erreurs et matrice reutiliser/evoluer/implementer. |
| B1 | Termine | Tokens et projections passeport | B0, `gestion_achats` | Consultation coffret par Bearer token, sans token dans l'URL, et projection passeport. |
| B2 | Termine | Catalogue et suivi public des animations | B0, Epic 41 | Liste/detail publics, inscription idempotente, lien participant, progression et QR. |
| B3 | Termine + evolution a faire | Feed et publications editoriales | B0, Epic 16, `EP41-T51` | Activites manuelles, programmation et scopes global/multi-villes ; ajouter les actualites `ACTUALITE_ANIMATION` rattachees et leur projection publique. |
| B4 | Termine | Installation, preferences et WebPush optionnel | B0 | Installation opaque autonome, rotation/revocation du secret, abonnements facultatifs et preferences par ville/categorie. |
| B5 | Termine | Suivis transactionnels et inbox | B1-B2-B4 | Associations installation-ressource verifiees, inbox paginee et lectures idempotentes. |
| B6 | Termine | Batchs, retention et supervision | B3-B5 | Diffusion idempotente, reprise exponentielle, purge a 90 jours, readiness et supervision Localeo Control. |
| B7 | Termine | Administration editoriale | B3 | Console de creation, programmation, publication, masquage et ciblage via le referentiel Ville. |
| B8 | Termine | Recette backend et readiness production | B1-B7 | 1 147 tests passes, validation syntaxique, OpenAPI controle et documentation d'exploitation mise a jour. |
| B9 | A faire | Persistance du carnet anonyme | B4-B5, arbitrages LIVE-ARB-41 a LIVE-ARB-51 | Carnet, appartenances appareils, ressources partagees, revisions, migration additive et autorisations objet. |
| B10 | A faire | Synchronisation, appairage et gestion des appareils | B9 | Snapshot avec ETag, commandes idempotentes, invitation a usage unique par QR ou code saisissable, confirmation et revocation. |
| B11 | A faire | Passkeys de recuperation et recette de securite | B9-B10 | Enregistrement et verification WebAuthn, recuperation sans ancien appareil, observabilite et tests multi-appareils. |

## Decoupage en lots frontend PWA

| Lot | Contenu | Dependances | Sortie attendue |
| --- | --- | --- | --- |
| F0 | Socle Localeo Live dans `localeo-marketplace` | OpenAPI B0 pour les clients API, arbitrages frontend | Module `/live`, navigation, manifeste, bundle et service worker isole. |
| F1 | Mise en avant et installation depuis la marketplace | F0 | Hero marketplace, CTA installer/ouvrir, QR desktop, aide iOS et deep links. |
| F2 | Bibliotheque locale et reglages | F0 | IndexedDB versionnee, sauvegarde/suppression des liens, transfert securise depuis la vue detaillee, commune manuelle et preferences locales. |
| F3 | Feed d'activite locale | F0, B3 ou mocks OpenAPI | Ecran `En direct`, filtres, commune, actualites globales/locales, actualites d'animation sous `Animations` et etats vide/erreur/hors ligne. |
| F4 | Passeport graphique des coffrets | F2, B1 ou mocks OpenAPI | Ajout depuis l'email ou la vue detaillee, progression lineaire accessible, QR protege par verification locale WebAuthn, prochaine action et gestion des tokens invalides. |
| F5 | Decouverte et inscription aux animations | F0, B2 ou mocks OpenAPI | Catalogue, fiche, inscription sans compte et sauvegarde du lien participant. |
| F6 | Mes participations | F2-F5, B2 ou mocks OpenAPI | Progression, QR participant protege par verification locale WebAuthn, qualification, resultat et gains. |
| F7 | Notifications, suivis et inbox | F2, B4-B5 ou mocks OpenAPI | Opt-in WebPush, preferences, suivis par ressource, inbox et deep links. |
| F8 | Qualite PWA et recette frontend | F1-F7, B8 | Hors ligne, accessibilite WCAG 2.2 AA, compatibilite et repli WebAuthn, absence de cache des QR, navigateurs cibles, Core Web Vitals et analytics responsables. |
| F9 | Activation et migration du carnet partage | F2, B9 | Consentement explicite, passkey initiale, import de la bibliotheque IndexedDB et snapshot partage. |
| F10 | Synchronisation, appairage et appareils | F9, B10 | Etats de synchronisation, QR/lien/code temporaire utilisable sans camera, confirmation, liste et revocation des appareils. |
| F11 | Recuperation et recette multi-appareils | F10, B11 | Recuperation par passkey sans ancien appareil, revocation des appareils perdus, erreurs et recette croisee. |

## Synchronisation des deux trajectoires

- `B0` est le contrat d'integration commun et doit preceder le branchement reel des lots frontend.
- `F0`, `F1` et `F2` peuvent commencer avec des mocks sans attendre les implementations backend.
- `B1/F4`, `B2/F5-F6`, `B3/F3` et `B4-B5/F7` forment les couples de recette fonctionnelle.
- la mise en production exige la validation conjointe de `B8` et `F8` ; la fin d'un seul flux ne suffit pas a terminer l'Epic 42.
- l'evolution de carnet partage suit ensuite les couples `B9/F9`, `B10/F10` et `B11/F11` ; elle ne modifie pas retroactivement la livraison du MVP local initial.

## Documents de specification

- [Vue d'ensemble](../../specifications/epic-42-localeo-live/README.md)
- [Backend et API](../../specifications/epic-42-localeo-live/backend-api.md)
- [Frontend PWA](../../specifications/epic-42-localeo-live/frontend-pwa.md)
- [Carnet partage - backend](../../specifications/epic-42-localeo-live/carnet-partage-backend.md)
- [Carnet partage - frontend](../../specifications/epic-42-localeo-live/carnet-partage-frontend.md)
- [Registre des arbitrages](../../specifications/epic-42-localeo-live/registre-arbitrages.md)


## Compléments Marketplace

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

Cette contribution conserve la photographie du MVP frontend et son avancement
au 19 août 2026. Ses variantes de `PRD-378`, de QR volontaire et de bibliothèque
locale précèdent les évolutions de carnet partagé et de protection WebAuthn
décrites dans le corps commun et les registres d'arbitrage ; elles ne les remplacent pas.

### User Stories

8. `PRD-378` En tant qu'utilisateur, je veux creer ou retrouver un profil leger afin de synchroniser mes coffrets, animations et preferences entre appareils.
   - Resultat attendu : une bibliotheque locale permet de sauvegarder les liens de consultation de coffrets et de participations sur l'appareil.
   - Resultat attendu : chaque ressource reste protegee par son token opaque ; les tokens sont exclus du cache du service worker, des logs et des analytics.
   - Resultat attendu : l'utilisateur peut supprimer une entree ou effacer toute sa bibliotheque locale.

### Arbitrages valides

- Les arbitrages produit et techniques `LIVE-ARB-01` a `LIVE-ARB-38` sont valides. `LIVE-ARB-31` exclut la geolocalisation du MVP, `LIVE-ARB-32` confie toute la gestion editoriale au backend et `LIVE-ARB-38` cadre l'ajout d'un coffret depuis sa vue detaillee.

### Decoupage en lots backend

| Lot | Statut | Contenu | Dependances | Sortie attendue |
| --- | --- | --- | --- | --- |
| B3 | Termine | Feed et publications editoriales | B0, Epic 16 | Activites manuelles, programmation et scopes global/multi-villes fondes exclusivement sur `villes`. |
| B4 | Termine | Installation et preferences WebPush | B0 | Installation opaque, rotation/revocation du secret, abonnements et preferences par ville/categorie. |

### Decoupage en lots frontend PWA

| Lot | Contenu | Dependances | Sortie attendue |
| --- | --- | --- | --- |
| F3 | Feed d'activite locale | F0, B3 ou mocks OpenAPI | Ecran `En direct`, filtres, commune, actualites globales/locales et etats vide/erreur/hors ligne. |
| F4 | Passeport graphique des coffrets | F2, B1 ou mocks OpenAPI | Ajout depuis l'email ou la vue detaillee, progression lineaire accessible, QR volontaire, prochaine action et gestion des tokens invalides. |
| F6 | Mes participations | F2-F5, B2 ou mocks OpenAPI | Progression, QR participant, qualification, resultat et gains. |
| F8 | Qualite PWA et recette frontend | F1-F7, B8 | Hors ligne, accessibilite WCAG 2.2 AA, navigateurs cibles, Core Web Vitals et analytics responsables. |

### Avancement frontend au 19 aout 2026

| Lot | Etat | Implementation disponible | Reste a faire |
| --- | --- | --- | --- |
| F0 | `Socle livre` | Module React autonome sous `/live/*`, chargement differe, navigation mobile a quatre destinations, manifeste, icone et service worker de scope `/live/`. | Durcir la strategie de cache et completer les tests de navigation directe sur les navigateurs cibles. |
| F1 | `Partiel` | Vignette Localeo Live sur l'accueil marketplace, lien vers `/live`, identite visuelle partagee et retour permanent vers `/accueil`. | Integrer `beforeinstallprompt`, l'etat standalone, l'aide iOS, le QR desktop et la mesure des installations. |
| F2 | `Partiel avance` | IndexedDB versionnee pour les liens, ajout explicite de coffret, detection des doublons, suppression unitaire, effacement global, compteur et choix manuel de commune. | Etendre la bibliotheque aux participations et migrer les preferences restantes vers IndexedDB. |
| F3 | `Connecte` | Ecran `En direct` branche sur `/public/exploitation/activites-locales`, filtres, communes issues de l'API et etats chargement, vide, erreur et hors ligne. | Ajouter la pagination incrementale et l'indication de contenu perime. |
| F4 | `Partiel connecte` | Passeport graphique lineaire, verification du lien via B1 avant ajout, transfert ephemere par `sessionStorage`, fallback par fragment, prochaine action et affichage volontaire du QR. | Alimenter la liste des passeports depuis les projections sauvegardees, traiter les tokens invalides, expires ou revoques et masquer le QR dans les apercus systeme. |
| F5 | `Connecte` | Catalogue communal branche sur B2, inscription idempotente, consentements separes et sauvegarde locale du lien participant. | Completer la fiche detaillee et la recette des erreurs metier. |
| F6 | `Partiel connecte` | Participations sauvegardees resolues via l'API avec statut et qualification. | Finaliser l'affichage du QR, de la progression detaillee, des resultats et des gains selon les payloads de production. |
| F7 | `Partiel connecte` | Installation opaque et secret en IndexedDB, abonnement navigateur WebPush activable et revocable, preferences serveur, inbox, lecture unitaire et globale, reception Push et deep links internes securises. | Activer et recetter la configuration VAPID sur les environnements cibles, puis finaliser les suivis par ressource. |
| F8 | `En cours` | Responsive mobile, cibles tactiles, focus visible, libelles accessibles, `prefers-reduced-motion` et compilation Vite de production validee. | Effectuer la recette WCAG 2.2 AA, hors ligne, navigateurs, Core Web Vitals, mises a jour du service worker et analytics responsables. |

Le frontend livre a ce stade une experience navigable et demonstrable. Les donnees metier affichees dans Live sont des mocks structures : elles ne constituent pas encore une recette integree avec les API B1 a B5.
