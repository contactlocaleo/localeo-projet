# Specification frontend PWA - Localeo Live

> Document consolidé depuis les spécifications `localeo-marketplace` et
> `localeo-backend`. La refonte du carnet de septembre remplace la navigation initiale
> à quatre destinations et la confirmation systématique ; les exigences backend
> de suivi, d'actualités Animation, de protection QR et de carnet partagé sont conservées.
> Leur présence dans la spécification ne vaut pas constat d'implémentation ni de recette.

## Historique d'implementation au 19 aout 2026 — origine Marketplace

Un premier frontend navigable est implemente dans `localeo-marketplace` sous `/live/*`. Il couvre le shell PWA, la navigation, les vues principales, l'entree depuis la marketplace, le retour vers `/accueil`, le manifeste, l'icone et le service worker isole. L'ajout d'un coffret depuis sa vue detaillee est implemente avec transfert ephemere, verification backend, confirmation, IndexedDB, detection des doublons et suppression locale. Le feed, les communes, les passeports sauvegardes, les animations, les inscriptions, les participations, l'installation opaque, les preferences et l'inbox sont raccordes aux endpoints presents dans le contrat consommé à cette date (ancien chemin Marketplace retiré ; consulter le [contrat documentaire Live actuel](openapi.json)). L'abonnement WebPush navigateur peut etre active ou revoque depuis les reglages, avec preferences par categorie et ouverture securisee des deep links. Il reste conditionne par `webpush_enabled` et la presence d'une cle VAPID dans la configuration publique.

Ce bilan historique annonçait encore des travaux de raccordement API Live, IndexedDB, installation multi-navigateurs, WebPush, états réseau, protection finale des QR et recette F8. Il ne constitue pas un état de livraison actuel : certains raccordements sont déjà annoncés dans le paragraphe précédent, sans preuve suffisante pour clore l'ensemble de ces travaux. Le statut detaille de chaque lot est maintenu dans [@localeo-marketplace/docs/roadmap/epic-42-localeo-live-grand-public-backlog.md](../../roadmap/terminees/epic-42-localeo-live-grand-public-backlog.md).

## 1. Positionnement

Localeo Live est avant tout le carnet digital du client : il permet de sauvegarder facilement ses coffrets et participations, de les retrouver et de presenter leur QR chez un commercant. La decouverte locale reste secondaire.

### These visuelle

Une application chaleureuse et editoriale, inspiree du carnet de voyage local : photographie en situation, typographie nette, matiere papier discrete et un accent Localeo unique pour les actions et progressions.

### Plan de contenu

1. marketplace : mise en avant plein cadre, benefice, apercu reel et CTA `Installer Localeo Live` ;
2. accueil Live : mon carnet, avec deux rubriques stables « Mes coffrets » et « Mes animations » ;
3. coffrets : QR et prestations restantes, puis detail des prestations ;
4. animations : QR, progression et resultat, avec decouverte accessible separement ;
5. centre de notifications et preferences ;
6. reglages locaux, consentements, aide et installation.

### These d'interaction

- entree courte du fil avec apparition progressive des actualites ;
- progression du passeport animee uniquement lors d'une nouvelle validation ;
- transition partagee entre une animation du fil et sa fiche ;
- toutes les animations respectent `prefers-reduced-motion`.

## 2. Installation depuis la marketplace

La marketplace constitue le point d'acquisition principal :

- hero mobile et desktop dedie avec marque `Localeo Live`, promesse courte et visuel de l'application ;
- CTA d'installation prioritaire lorsque `beforeinstallprompt` est disponible ;
- instructions adaptees a iOS lorsque l'installation automatique n'est pas disponible ;
- CTA `Ouvrir` si l'application est deja installee ou lancee en mode standalone ;
- QR d'installation sur desktop et deep link sur mobile ;
- aucune interruption agressive avant une premiere interaction utile ;
- mesure des impressions, clics, installations acceptees/refusees et ouvertures, sans identifiant publicitaire.

Le manifeste definit nom, nom court, couleurs, icones maskable, screenshots, raccourcis `Mes coffrets` et `Animations`, ainsi qu'un `id` stable. Le service worker ne met jamais en cache durablement un QR ou un token sensible.

## 3. Navigation

Navigation principale mobile a deux destinations :

- `Mon carnet` : deux rubriques distinctes, `Mes coffrets` et `Mes animations` ;
- `Decouvrir` : animations locales et actualites par commune.

Les reglages et le centre de notifications sont accessibles depuis l'en-tete. Les liens personnels ouvrent la ressource concernee. L'ajout se fait apres une action explicite du client, sans demander une seconde confirmation lorsque cette action vient deja d'etre effectuee.

La categorie canonique des preferences editoriales est `ACTUALITE_EDITORIALE`. Le frontend n'emet jamais `EDITORIAL` et convertit cet ancien libelle lorsqu'il est relu depuis une installation creee par une version anterieure.

## 4. Ecrans et comportements

### En direct

- ordre chronologique avec filtres `Tout`, `Coffrets`, `Commercants`, `Animations`, `News` ;
- commune selectionnee manuellement, explicite et modifiable ; aucune demande de geolocalisation au MVP ;
- chaque publication indique source, date, commune et action utile ;
- les actualites `ACTUALITE_ANIMATION` sont rangees sous le filtre `Animations`, affichent le nom de l'animation et ouvrent sa fiche via un deep link ;
- rafraichissement manuel et incremental, sans flux WebSocket requis au MVP ;
- etats vide, erreur, hors ligne et contenu perime clairement differencies.

### Passeports coffrets

- couverture du coffret dominante, beneficiaire et date d'expiration ;
- parcours graphique en etapes reliant les prestations disponibles et consommees ;
- QR accessible par une action volontaire et masque dans les apercus systeme ;
- prochaine action mise en avant : choisir, reserver, presenter le QR ou demander de l'aide ;
- vues `En cours`, `Termines`, `Expires` ;
- accessibilite : la progression reste comprehensible sans couleur ni animation.

#### Ajouter un coffret depuis sa vue detaillee

- la vue detaillee securisee existante affiche `Ajouter a mes coffrets Localeo Live` ; si l'identifiant est deja present dans IndexedDB, le libelle devient `Ouvrir dans Localeo Live` ;
- le clic depose temporairement `coffret_instance_id` et `consultation_token` dans `sessionStorage`, puis ouvre `/live/coffrets/ajouter` sur la meme origine ;
- Localeo Live lit et supprime immediatement le transfert temporaire et verifie le token avec la projection passeport backend ; une intention d'ajout explicite transmise depuis la fiche permet l'enregistrement sans seconde confirmation ; un lien externe sans cette intention conserve un apercu et un bouton d'ajout ;
- si `sessionStorage` ne peut pas etre partage, le fallback ouvre `/live/coffrets/ajouter/{coffret_instance_id}#token=...` ; le fragment est lu puis retire avec `history.replaceState` avant tout appel tiers ;
- le CTA direct de l'email doit utiliser `https://{marketplace}/live/coffrets/ajouter/{coffret_instance_id}#token={consultation_token}` ; un lien contenant uniquement l'identifiant de l'instance est incomplet et doit etre refuse ;
- le token n'est transmis ni aux logs, ni aux analytics, ni au service worker et ne figure jamais dans un parametre de requete du nouveau parcours ;
- l'action explicite `Ajouter a mes coffrets`, effectuée sur la fiche ou dans l'aperçu du lien externe, enregistre la ressource dans la bibliotheque IndexedDB après vérification ;
- depuis E42-UX-01 (26 septembre 2026), les options du coffret ne proposent plus l'action `Me prévenir des prochaines étapes` ni ses messages d'activation ; l'ajout local ne déclenche pas de suivi distant de remplacement ;
- l'email de confirmation conserve son lien de consultation ; lorsqu'un CTA direct `Ajouter a Localeo Live` est présent, il utilise le meme contrat d'entree. Son caractère systématique ou facultatif reste une divergence documentaire, détaillée ci-dessous.

### Refonte du carnet — septembre 2026, origine Marketplace

- `/live/` ouvre la dernière rubrique du carnet consultée ; par défaut, « Mes coffrets ».
- Deux rubriques stables : « Mes coffrets » (`/live/passeports`) et « Mes animations » (`/live/animations`). Le terme passeport reste interne aux anciennes URL compatibles.
- Le catalogue des animations se trouve sur `/live/decouvrir` et les actualités sur `/live/actualites` ; les deux destinations principales et les accès d'en-tête sont définis en section 3.
- Les cartes personnelles présentent un état principal et un accès volontaire au QR. Le détail et le retrait restent accessibles sans encombrer l’action principale ; les notifications générales se gèrent dans Réglages.
- « Actualiser mon coffret » recharge les données depuis la liste ou le détail, sans recharger la page. Le bouton indique le chargement puis la réussite ; en cas d’erreur, les dernières informations restent visibles et l’action peut être relancée. La dernière réponse actualisée est conservée dans le carnet local si le stockage est disponible.
- Aucune bienvenue modale ne précède l’ajout. La confirmation d’enregistrement propose facultativement l’installation sur l’écran d’accueil.
- L'intention explicite « Ajouter à mon carnet » est transmise dans l'état de navigation ; le parcours de confirmation est celui défini ci-dessus. Cette évolution Marketplace remplace la confirmation systématique de la version initiale.
- Le formulaire public « M’inscrire et enregistrer » conduit à la vérification puis à l’enregistrement de la participation. Un échec du stockage local propose de reprendre cet enregistrement sans refaire l’inscription.
- Le suivi distant d’une participation est indépendant de la réussite de son stockage local. Une animation simplement suivie est remplacée par sa participation au moment de l’enregistrement ; les participations distinctes d’une famille sont conservées.
- Les règles et le règlement restent consultables avant l’inscription. Dans la vue personnelle, les validations précèdent les informations secondaires regroupées sous « À propos de l’animation ».
- Le stockage reste local au navigateur ; aucun compte ni synchronisation entre appareils n’est ajouté par cette refonte.

### Animations

- liste des animations ouvertes/en cours autour de la commune choisie ;
- fiche avec periode, regles, commercants, lots, accessibilite et statut d'inscription ;
- inscription courte, consentements separes et confirmation explicite ;
- apres confirmation, rattachement idempotent de la participation a l'installation Live avec le token recu, puis rafraichissement du catalogue personnalise ;
- le catalogue et la fiche affichent l'etat retourne par l'API d'installation : `est_inscrit` represente l'inscription verifiee, tandis que `dans_carnet` represente seulement sa presence sur cet appareil ;
- espace `Mes participations` avec QR, etapes, progression, qualification et gains ;
- partage par Web Share API avec repli copie de lien ;
- les actualites rattachees a une animation peuvent aussi apparaitre dans sa fiche ou sa timeline, sans dupliquer leur contenu dans le frontend ;
- les emails participants affichent le meme pied Localeo Live contextualise Animation ; la confirmation d'inscription utilise le lien profond contenant le token participant dans son fragment.

### Protection locale des QR personnels

L'affichage d'un QR de passeport/coffret ou de participation Animation est protege localement sur chaque appareil, sans compte client ni nouvelle session d'authentification cote serveur :

- l'action explicite `Afficher le QR code` declenche WebAuthn avec un authentificateur de plateforme et `userVerification=required` ;
- le systeme d'exploitation choisit le moyen de verification configure : empreinte, reconnaissance faciale, code de deverrouillage, Windows Hello ou equivalent ; Localeo n'accede jamais aux donnees biometriques ;
- au premier usage sur un appareil, la PWA explique la protection puis enregistre un credential local dedie ; chaque appareil realise son propre enrolement ;
- la verification doit etre declenchee par une action utilisateur et l'application doit etre servie en HTTPS, avec `localhost` accepte pour le developpement ;
- le QR n'est charge depuis son endpoint qu'apres une verification reussie ; aucun prechargement, cache du service worker ou stockage IndexedDB n'est autorise ;
- la reponse QR conserve une politique `Cache-Control: no-store` et son contenu n'est pas transmis aux analytics ou aux journaux frontend ;
- le QR est retire du DOM et de la memoire applicative lorsque la PWA passe en arriere-plan, lorsque l'utilisateur quitte l'ecran ou a l'expiration de la duree d'affichage ;
- toute nouvelle demande d'affichage impose une nouvelle verification, sans periode de grace partagee entre plusieurs QR ;
- si WebAuthn ou l'authentificateur de plateforme n'est pas disponible ou si aucun verrouillage securise n'est configure, le QR reste masque et un ecran d'aide indique comment activer une protection compatible ;
- aucun repli autorisant un affichage non protege n'est propose.

Cette protection vise l'utilisation normale de la PWA sur un appareil temporairement accessible a un tiers. Elle ne remplace pas les controles d'autorisation existants des endpoints QR et ne permet pas d'empecher une capture d'ecran apres affichage.

### Notifications

- inbox persistante meme si le WebPush est refuse ;
- consentement WebPush demande apres une action explicite et contextualisee ;
- preferences par categorie et commune ;
- suivi transactionnel d'un coffret ou d'une participation active explicitement apres validation de son token ;
- deep link vers la ressource concernee ;
- option silencieuse pour les actualites editoriales, notifications transactionnelles non desactivables uniquement si leur base legale le permet ;
- les actualites d'animation respectent la categorie configurable `ANIMATION`; une preference desactivee interdit la creation de notification et l'envoi WebPush pour ce type de publication.

### Bibliotheque locale et confiance

- ajout d'un coffret avec son token de consultation depuis la vue detaillee ou le raccourci de l'email, et ajout automatique d'une participation apres inscription ;
- sauvegarde locale explicite des liens, suppression unitaire et effacement global ;
- aucun compte, aucune synchronisation multi-appareils et aucune recuperation serveur au MVP ;
- commune choisie manuellement ; aucune geolocalisation au MVP ;
- gestion des consentements et acces aux politiques ;
- support contextualise et version de l'application.

L'evolution post-MVP de persistance, partage entre appareils et recuperation du carnet est decrite separement dans [la specification du carnet partage](carnet-partage-frontend.md). Elle conserve le mode local historique jusqu'a une activation explicite ; les arbitrages associés restent à valider.

## 5. Etats applicatifs

| Etat | Comportement |
| --- | --- |
| Visiteur | Feed, catalogue et animations publiques ; inscription/token ponctuels possibles. |
| Bibliotheque locale | Coffrets et participations sauvegardes sur cet appareil, chacun restant resolu par son token. |
| QR personnel verrouille | Verification locale WebAuthn obligatoire avant chargement et affichage ; retour a l'ecran verrouille apres masquage. |
| Hors ligne | Consultation des derniers contenus non sensibles synchronises ; actions bloquees avec reprise explicite. |
| Token invalide ou expire | Entree locale signalee, contenu masque et suppression proposee. |
| Push refuse | Inbox disponible et aide non intrusive pour modifier le choix systeme. |

## 6. Exigences PWA

- responsive a partir de 320 px et zones tactiles d'au moins 44 px ;
- WCAG 2.2 AA, navigation clavier, lecteurs d'ecran et contraste controle ;
- shell applicatif chargeable hors ligne, mise a jour du service worker explicite ;
- strategie `network-first` pour donnees personnelles, `stale-while-revalidate` pour contenus publics versionnes ;
- bibliotheque locale effacable depuis les reglages ; tokens exclus du cache du service worker et des analytics ;
- Core Web Vitals cibles : LCP <= 2,5 s, INP <= 200 ms, CLS <= 0,1 au 75e percentile ;
- installation testee sur Chrome/Edge Android, Safari iOS et navigateurs desktop supportes ;
- aucune dependance frontend ou stack nouvelle n'est actee dans ce document.
- module autonome sous `/live` dans `localeo-marketplace`, avec bundle, manifeste et service worker dedies ;
- service worker limite au scope `/live/` et cache versionne distinct de la marketplace ;
- IndexedDB versionnee pour la bibliotheque, l'installation, son secret et l'acquittement de l'aide iOS ;
- support des deux dernieres versions majeures de Chrome, Edge et Firefox, de Safari iOS 16.4+ pour WebPush, avec fonctionnement sans Push ailleurs ;
- aide iOS affichee uniquement apres action sur `Installer` ;
- passeport lineaire avec etats disponible, consomme, indisponible et expire, prochaine action et alternative textuelle ;
- detection de WebAuthn et de l'authentificateur de plateforme avant l'enrolement ; l'absence de capacite produit un etat explique et maintient les QR masques ;
- aucun QR personnel dans IndexedDB, Cache Storage, les caches HTTP applicatifs ou les apercus persistants ; masquage immediat sur `visibilitychange` lorsque le document n'est plus visible.

## 7. Mesure produit

Evenements minimaux : exposition/clic du CTA marketplace, resultat d'installation, ouverture standalone, opt-in push, consultation/rattachement coffret, consultation/inscription animation, ouverture de notification et erreur de parcours. Les mesures sont agregees, documentees et soumises au consentement applicable.

## 8. Criteres de recette MVP

- installation en trois actions maximum depuis la marketplace sur un navigateur compatible ;
- feed d'activite locale exploitable sans authentification ;
- coffrets sauvegardes par token affiches sous forme de passeports accessibles ;
- ajout d'un coffret possible depuis sa vue detaillee en deux actions maximum, sans token persistant dans l'URL et sans activation implicite du Push ;
- inscription et suivi d'une animation de bout en bout ;
- preferences WebPush modifiables et inbox disponible sans Push ;
- deep links fonctionnels apres installation, sans compte ;
- verification locale par biometrie ou code systeme avant chaque affichage d'un QR de coffret ou de participation, avec QR masque sur refus, echec, annulation ou incompatibilite ;
- QR charge uniquement apres verification, non cache et masque lorsque la PWA devient inactive ;
- aucune donnee d'un autre client accessible par modification d'identifiant ;
- mode hors ligne et mise a jour de version testes.


## 9. Écarts documentaires à confirmer

| Sujet | Origine backend | Origine Marketplace | Traitement de la consolidation |
| --- | --- | --- | --- |
| CTA dans les emails coffrets | Pied Localeo Live commun ; lien profond avec token valide, sinon `LOCALEO_FRONT_LIVE_URL` ; la confirmation propose un CTA direct. | La confirmation « peut proposer » un second CTA direct. | Contrat technique conservé, portée systématique/facultative non arbitrée. Le lien profond n'est jamais fabriqué sans token. |
| Protection QR | `LIVE-ARB-40` indiqué validé : WebAuthn obligatoire, aucune solution de repli non protégée. | Absent du descriptif, « protection finale » encore citée dans le bilan historique. | Exigence validée conservée ; couverture de l'implémentation et de la recette à vérifier, sans abaisser la règle. |
| Avancement MVP | Le socle API et les lots backend initiaux sont annoncés terminés. | Le bilan du 19 août annonce à la fois des raccordements réalisés et à terminer. | Chaque bilan garde sa portée et sa date ; aucune clôture des lots frontend n'est déduite de la fusion. |

La bibliothèque conserve les participations distinctes d'une famille selon la
refonte Marketplace. Les règles détaillées d'inscription et de reprise sont
référencées dans [Inscriptions multiples et récupération](inscriptions-multiples.md).

## 10. E42-UX-01 — retrait du suivi facultatif des coffrets, 26 septembre 2026

À la demande produit, supprimer « Me prévenir des prochaines étapes » dans
les options des coffrets du carnet. Cette évolution remplace l'action de suivi
distincte décrite précédemment lors de l'ajout d'un coffret ; elle ne change pas
la séparation entre ajout local et consentement WebPush de LIVE-ARB-38.

- **E42-UX-01-A** : aucun bouton d'activation, message « Suivi des prochaines
  étapes activé » ou erreur de cette ancienne action n'est présenté, y compris
  pour une entrée historique contenant `followId` ou `followStatus`.
- **E42-UX-01-B** : supprimer le gestionnaire d'activation depuis les coffrets,
  sans créer de suivi automatique à l'ajout, à l'ouverture ou à l'actualisation.
- **E42-UX-01-C** : préserver l'ajout et la consultation des coffrets, leur
  actualisation, le QR et le retrait du carnet. Les notifications générales,
  l'inbox et le suivi des participations Animation restent inchangés. Les
  suivis déjà enregistrés ne sont pas révoqués automatiquement ; la gestion
  existante du retrait du carnet reste applicable.

Impact : interface Marketplace/Live et documentation centrale seulement.
Le contrat des suivis reste consommé par les participations Animation ; aucun
endpoint, droit ou règle backend n'est supprimé. Aucune migration ni modification
des données, du générateur de démonstration ou de sa configuration n'est requise.
La livraison porte uniquement sur le bundle Marketplace. Les preuves ciblées
et leur résultat figurent dans le backlog de l'epic, dont la clôture historique
est conservée.
