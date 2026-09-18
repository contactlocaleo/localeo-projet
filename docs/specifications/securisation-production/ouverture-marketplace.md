# Sécurisation de l'ouverture en production

Ce complément fixe les règles corrigées à partir de l'audit du 5 septembre 2026.
Le rapport historique reste une description de l'état avant correction.

## F16 — Tests visuels couplés à une API distante

- Les tests utilisent leur propre serveur local ; un serveur existant ne doit jamais être réutilisé.
- Le serveur de test ne charge pas les fichiers d'environnement et ne proxifie aucune API.
- Les appels métier sont simulés. Les créations d'installation utilisent une identité fictive.
- Tout appel sortant non couvert par une fixture est bloqué et fait échouer le test.
- Les service workers sont désactivés dans les tests de présentation pour ne pas contourner l'interception réseau ; leur politique fait l'objet de tests dédiés.
- Aucune campagne de charge ou recette réelle n'est autorisée implicitement par `npm test`.

Validation : `npm run test:visual:desktop`, lint et build isolé de production.

## F02 — Filtre SVG contournable

- Les QR SVG sont affichés exclusivement comme images (`img` avec une URI de données), jamais comme du HTML intégré, un iframe, un object ou un lien vers le SVG.
- L'ancien assainisseur artisanal est remplacé par une validation de document SVG et par ce rendu passif. Les documents malformés, DTD/entités et documents de plus d'un million de caractères sont refusés.
- Les dimensions d'affichage et d'impression sont conservées. Le contenu du QR métier n'est pas modifié.
- Les scripts et ressources distantes restent inertes même sans CSP ; la CSP existante reste une défense supplémentaire.
- Les anciennes sondes d'audit décrivent le code précédent ; la référence de non-régression est désormais `npm run test:security` et le scénario visuel QR.

Référence : [restrictions SVG dans un contexte image](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image).

## F04 — Diagnostic QR public contenant le jeton brut

- L'écran d'impression n'affiche ni jeton brut, ni KID, ni contenu décodé, à l'écran comme sur papier.
- Seuls l'image du QR, son type et sa validité sont conservés dans l'état de présentation.
- Le paramètre `token` du lien entrant est capturé en mémoire puis retiré de l'entrée d'historique par remplacement, avant peinture. Aucun stockage persistant de ce jeton n'est ajouté.
- Après rechargement de l'URL nettoyée, l'utilisateur doit rouvrir son lien d'accès ; l'application ne reconstitue pas un accès absent.
- Le transport de ce jeton vers l'API relève du changement de contrat F03 ; ce correctif ne prétend pas nettoyer des journaux historiques.

Validation : scénario navigateur QR, absence des sentinelles token/KID/email dans le rendu et suppression du paramètre de l'URL.

## F06 — Cache PWA trop général

- Seuls les assets publics `/assets/`, le manifest, les deux icônes Live et le shell fixe `/live/` sont admissibles au cache du service worker.
- Les routes API, liens à capacité, configuration runtime, requêtes à paramètres ou en-têtes d'accès, réponses privées/no-store et redirections ne sont jamais mémorisés.
- Le serveur fournit explicitement `/live/` comme shell statique public revalidé ; les autres routes HTML restent `no-store`. Un hébergement statique doit reproduire cette distinction avant activation du mode hors ligne.
- Le cache v6 remplace les anciens caches Live à l'activation ; les caches d'autres applications sont préservés.
- En panne réseau, seul un document de navigation Live peut recevoir le shell. Une ressource manquante ne reçoit jamais du HTML à sa place.
- Les écritures sont rattachées à la durée de vie du worker ; une erreur de quota ne fait pas échouer une réponse réseau valide.
- Le carnet IndexedDB n'est pas supprimé par cette migration. La cohérence des versions des assets est suivie en F12.

Validation : tests de politique de cache, migration et fallback ; test serveur des en-têtes shell/capacité.

## F11 — Erreurs filesystem et stream non confinées

- Une erreur synchrone de lecture de fichier ne sort pas du gestionnaire HTTP : réponse générique 500 non cacheable si les en-têtes ne sont pas partis.
- Une erreur après début de transfert interrompt la réponse concernée, sans tenter de réécrire les en-têtes. La chaîne lecture/compression/réponse est fermée par `pipeline`.
- Aucune URL, capacité ou chemin disque n'est inclus dans l'erreur publique ni dans le message technique ajouté.
- L'absence de réponse complète ne justifie pas de continuer à utiliser un asset tronqué ; le navigateur doit pouvoir réessayer.

Validation : pannes disque synchrones et stream simulées sur un serveur local réel, puis requête suivante réussie ; tests HTTP existants.

## F08 — Ancien formulaire Live à idempotence divergente

- Le formulaire historique inaccessible, sa soumission et son extraction redondante de jetons sont retirés de `LiveAnimations`.
- L'inscription depuis Live passe exclusivement par le formulaire partagé Marketplace (`/animations/:id?inscription=1&from=live`).
- Un nouvel essai sans modification des données conserve la même clé d'idempotence. L'unicité métier doit également être garantie côté API ; la suppression du code mort ne vaut pas preuve d'une transaction serveur unique.

Validation : parcours catalogue Live vers formulaire partagé, deux soumissions après indisponibilité simulée avec une clé identique.

## F09 — Pagination d'une ancienne commune ajoutée à la nouvelle

- Chaque contexte de fil (commune, filtre, actualisation) dispose d'une génération distincte.
- Un changement de contexte ou un démontage annule les requêtes en cours. Même si un transport ignore cette annulation, ses résultats et erreurs tardifs sont écartés avant modification du fil ou du cache.
- Une seule pagination peut être engagée à la fois ; les doublons d'identifiant sont éliminés dans une page valide.

Validation : réponse et erreur volontairement retardées après changement de contexte, succès normal, double clic et déduplication ; parcours visuels Live.

## F15 — Les requêtes marchandes retardent toute la fiche

- Dès que le coffret est disponible, son descriptif, ses prestations et son accès à l'achat sont affichés. L'annuaire des commerçants et le nom de la commune ne bloquent plus cette étape.
- Les informations secondaires arrivent progressivement ; leur indisponibilité est signalée dans la section des adresses, avec un réessai dédié.
- Le nombre d'adresses repose sur les identifiants distincts des prestations, pas sur le nombre de réponses marchandes déjà reçues.
- Les droits, prix et disponibilité à l'achat restent contrôlés par l'API. Cette correction ne transforme pas les appels marchands en endpoint agrégé ; le coût O(N) à cache froid reste un sujet de mesure.

Validation : achat accessible avant déblocage d'une réponse marchande simulée, puis après succès et après erreur ; régression visuelle de la fiche.

## F13 — Import du carnet non atomique

- Limites d'import : 5 Mo (contrôlés avant lecture du fichier et avant décodage JSON), 1 000 éléments.
- Le format/version, chaque type et identifiant, les champs texte, dates et objets de présentation sont validés avant toute écriture. Une clé dupliquée ou un élément invalide refuse tout le fichier.
- Seuls les champs métier du carnet sont repris ; les clés sont recalculées et les dates de sauvegarde valides conservées. Les champs inconnus et états transitoires de l'interface sont ignorés.
- La restauration fusionne le carnet dans une transaction unique : succès complet ou annulation complète, y compris lors d'une exception synchrone après une première écriture. Les éléments non concernés et les métadonnées d'installation sont préservés.
- Le fichier contient des accès personnels : il demeure une sauvegarde privée, pas un fichier à partager publiquement.

Validation : vraie base IndexedDB dans un navigateur vierge, fichiers mixtes invalides, limites, doublons, erreurs de stockage synchrones/asynchrones, fusion et aller-retour export/import.

## F07 — Création concurrente d'installations

- Les appels concurrents d'un onglet partagent une promesse ; les onglets de la même origine sont sérialisés par un verrou exclusif, avec relecture IndexedDB sous verrou.
- Une identité existante n'est jamais recréée pour un changement de commune. `cityId` est seulement une préférence de création ; les réglages explicites continuent d'utiliser l'API de préférences après résolution de l'identité.
- Une erreur libère la promesse. Si seule la persistance échoue, la réponse reçue est conservée en mémoire pour réessayer son enregistrement sans nouvelle création dans cet onglet.
- Sans Web Locks, une identité déjà stockée reste utilisable ; une nouvelle synchronisation distante est refusée avec une explication. Le carnet local reste accessible. Web Locks exige un contexte sécurisé et coordonne les onglets de même origine ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API)).
- Limite distincte : une réponse réseau perdue, la fermeture de l'onglet avant persistance ou une panne du stockage partagé exigent une idempotence/récupération côté API pour garantir une création unique malgré incident. Le verrou navigateur ne constitue pas cette garantie serveur et ne réconcilie pas les anciennes identités.

Validation : deux vrais onglets avec IndexedDB et Web Locks, appels simultanés, options concurrentes, erreurs de création/persistance et navigateur sans verrou.

## F10 — Absence de délai applicatif central, annulation partielle

- Chaque tentative API est bornée, en-têtes et lecture du corps compris : lecture 15 s, écriture 30 s, téléchargement 60 s. Ce sont des budgets initiaux applicatifs, pas des SLO constatés ; les ajuster selon les mesures de préproduction.
- Tous les helpers HTTP transmettent le signal de l'appelant à un contrôleur commun. Délai, écouteur et transport sont libérés à la fin. Une annulation avant départ n'envoie aucune requête.
- Le transport ne réessaie jamais automatiquement une écriture. Une interruption après départ (délai, annulation ou rupture réseau) donne un résultat incertain, pas une preuve d'échec métier. Les messages publics préservent cette distinction sans exposer l'erreur technique.
- La clé d'idempotence existante des achats/inscriptions est conservée pendant la reprise de la même intention. Une vérification de confirmation est nécessaire avant de créer une nouvelle demande ; la récupération après rechargement et l'unicité serveur restent à valider avec le backend.
- Les GET gérés par React Query peuvent encore être réessayés selon la politique existante (une reprise) : le budget s'applique à chaque tentative.

Validation : en-têtes et corps suspendus pour chaque verbe, annulation avant/après départ, signal de tous les helpers, erreur réseau d'écriture, succès/nettoyage, absence de retry de transport et conservation de l'en-tête d'idempotence.

## F14 — Image principale PNG de 2 477 178 octets

- L'accueil charge une image WebP : 960 × 470 entre 721 et 980 px et 1 793 × 877 au-delà. Jusqu'à 720 px, le design existant masque cette image : aucun téléchargement ne doit être ajouté.
- Même composition et même recadrage CSS ; aucune nouvelle illustration. Le PNG original reste disponible comme source, mais n'est plus chargé par l'accueil.
- Budgets de non-régression : 110 000 octets pour la petite variante, 260 000 pour la grande. Mesures obtenues : 93 312 et 232 292 octets, soit environ 96 % et 91 % de moins que le PNG. Ce gain de taille n'est pas une mesure du LCP en production.
- Régénération locale reproductible dans l'environnement de test : `node scripts/optimize-home-image.cjs` (Chromium Playwright, aucune requête externe).

Validation : taille des fichiers, variante réellement demandée sans téléchargement du PNG, captures mobile et desktop.

## F12 — Asset absent renvoyé comme HTML 200, reprise incomplète

- `/assets/*` absent renvoie 404 texte, jamais le shell HTML. Les routes applicatives conservent le fallback SPA.
- Chaque build génère un worker dont le cache est identifié par le contenu du shell, du worker et des assets. Tous les modules, CSS et polices du répertoire `assets` sont préchargés ; un échec d'installation supprime le cache incomplet et laisse la version active intacte. La configuration runtime reste exclue du cache.
- À l'activation, conserver la version courante et la précédente de caches publics sûrs ; supprimer les anciens caches potentiellement sensibles. Un asset immuable peut être retrouvé par son URL exacte dans N-1 en cas de 404 ou de déconnexion. Aucun ancien shell ni contenu privé n'est utilisé comme substitut.
- L'entrée dans Live, directe ou SPA, déclenche l'enregistrement. Un refus du navigateur n'entraîne plus de rejet non géré.
- Une nouvelle version attend : un bouton propose sa prise en compte, après confirmation de la perte des saisies non enregistrées. Un changement de contrôleur ne recharge jamais spontanément un autre onglet.
- Le HTML et le worker portent la même révision de build. Une version en attente déjà affichée par la page ne déclenche pas d'alerte ; un ancien contrôleur seul ne suffit pas non plus. Le script du worker est revalidé par HTTP.
- « Plus tard » masque cette révision pendant la session de l'onglet. Le bouton reste utilisable si un autre onglet a déjà activé la version. Le chargement affiche sa progression ; après 15 secondes sans activation, un message permet de réessayer ou de continuer, sans rechargement tardif imposé.
- Exigence d'exploitation restant à vérifier avant clôture : conserver également les assets N-1 sur l'hébergement/CDN pour les clients sans cache Live, et effectuer un essai réel de bascule/retour arrière. La rétention navigateur ne remplace pas une stratégie de déploiement atomique.

Validation : assets manquants HTTP, manifeste/hash de build déterministe, cache N-1 en 404/hors ligne, purge des anciennes versions, refus d'enregistrement, absence de rechargement sans accord et entrée SPA. Tests complémentaires de comparaison de versions, report de l'alerte, échec/réessai, et cycle réel de worker sur serveur local avec plusieurs onglets.

## Observation — Compression HTTP : refus q=0 ignoré

Le serveur respecte les pondérations `Accept-Encoding`, les exclusions explicites, le joker et la préférence explicite pour `identity`. À poids égal entre compressions, Brotli reste préféré. Si toutes les représentations disponibles sont interdites, répondre 406 sans corps. Les valeurs q invalides sont traitées comme un refus du codage concerné. Référence : [RFC 9110, section 12.5.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-12.5.3).

Validation : préférences, exclusions, joker, absence de codage admissible et réponses HTTP réelles gzip/406.

## Observation — Redirection checkout pro non validée

Les parcours particulier et professionnel partagent la validation de redirection : HTTPS obligatoire et absence d'identifiants `user:password` dans l'URL. HTTP n'est accepté que pour une boucle locale en build de développement. Les protocoles exécutables et URLs invalides sont refusés avant navigation. La liste des domaines de paiement autorisés (notamment si Stripe utilise un domaine personnalisé) reste à confirmer avec l'exploitation avant ajout d'une restriction par origine.

Validation : URL HTTPS normale, protocoles actifs, HTTP distant/local, identifiants dans l'URL, nom de domaine trompeur et utilisation du même validateur dans les deux pages.

## Observation — Documentation de routage obsolète

Le routeur est `BrowserRouter` (React Router 7), avec Vite 8. Les liens entrants utilisent le chemin normal. L'hébergement doit servir le shell pour les routes applicatives mais conserver une réponse 404 pour les assets absents. Les installations de livraison utilisent `npm ci` avec le lockfile versionné. Le guide agent, le README et l'architecture sont alignés sur ces règles ; les contrôles HTTP de F12 vérifient le routage décrit.
