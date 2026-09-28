# Contrats correctifs Marketplace du 6 septembre 2026

> Consolidation du 18 septembre 2026 : ce document réunit les contrats backend
> de `corrections-marketplace-2026-09-06.md` et les compléments de présentation
> issus de `corrections-marketplace-2026-09-06.marketplace.md`.
> Les identifiants MARKET-001 à MARKET-010 sont conservés. Les constats d'audit
> et résultats de tests cités restent ceux des corrections historiques ; cette
> consolidation n'est ni une nouvelle recette ni une preuve de déploiement.

## MARKET-001 — Jetons dans Analytics

Au 28 septembre 2026, le correctif local remplace le tag navigateur par un transport
serveur contrôlé vers Google Measurement Protocol. Le serveur ne permet toujours
pas le script Google dans sa CSP. L'activation nécessite le consentement, les flags,
l'environnement production, l'identifiant GA et le secret privé du serveur.
Ce constat local ne constitue pas une activation de la plateforme déployée.

L'invariant technique est porté par `analyticsPolicy.mjs`, partagé entre le
navigateur et le serveur Marketplace : seul un nom d'événement connu et ses
attributs énumérés sont admis. Aucune URL, query, ancre, titre, label libre,
coordonnée, identifiant métier ou capacité d'accès n'est transmis. Une route
personnelle est réduite à une catégorie fixe (`participant`, `feedback`, `live`,
etc.). Les anciennes fonctions de marquage conservent leur interface, mais leurs
labels et identifiants sont éliminés.

`POST /analytics/events` est un endpoint technique du serveur Node Marketplace,
sans appel au domaine backend ni persistance. Son JSON comporte exactement
`client_id` (UUID v4 aléatoire éphémère), `session_id` (début de session en secondes)
et `event` (`name`, `params`). `app_environment=production` est requis côté serveur.
Le client utilise un identifiant uniquement en mémoire, distinct des accès Live,
supprimé au retrait et à la sortie du document. Aucun cookie Analytics n'est créé.

Le serveur vérifie origine, méthode, type JSON, taille (4 Ko), schéma fermé,
débit et concurrence. Il reconstruit le payload ; les headers, cookies, IP et
Referer ne traversent jamais la frontière vers le destinataire injecté. Les erreurs
ne contiennent aucune valeur reçue. Aucun rejeu automatique ni file persistante.
La disponibilité publique `LOCALEO_ANALYTICS_TRANSPORT_AVAILABLE` est calculée
par le serveur et reste fausse sans configuration privée valide.
`analytics-google.cjs` transmet exclusivement le payload reconstruit vers
`https://www.google-analytics.com/mp/collect`, sans redirection ni rejeu, avec
annulation et délai de trois secondes. Seuls l'identifiant GA et le secret du
serveur sont ajoutés à l'URL Google ; ils ne proviennent jamais de la requête
navigateur. Aucune erreur du fournisseur ou URL contenant le secret n'est journalisée.
Le secret `LOCALEO_GA_API_SECRET` est exclu du bundle et de `/app-config.js`.
L'adaptateur réel utilise une fonction HTTP simulée dans les tests.

Preuves locales : `tests/security/analytics-collection.test.cjs`,
`analytics-consent.test.cjs`, `analytics-transport.test.cjs` et
`tests/visual/analytics-collection.spec.cjs` dans Marketplace. Les tests navigateur
inspectent le réseau sur accès directs et navigation SPA avec sentinelles privées,
puis la réception par le serveur et l'adaptateur Google à la frontière HTTP simulée. Ils ne prouvent pas
l'ingestion dans une propriété Google réelle.

Résultats locaux du 28 septembre après branchement de l'adaptateur : 100 tests de
sécurité, 18 scénarios navigateur et 12 tests serveur réussis, y compris les cas
du fournisseur simulé. Les événements d'inscription ont été raccourcis en
`animation_registration_started`, `animation_registration_succeeded` et
`animation_registration_failed` pour respecter la limite GA4 de 40 caractères.
Build isolé et lint des sources/scripts/tests
concernés réussis. Le lint global `eslint .` rencontre un accès `EPERM` dans une
sortie préexistante `output/demo-generation/pytest-bum-registry` ; le lint ciblé
n'a pas ce blocage. Aucun appel fournisseur, secret opérateur ou déploiement.

Reste à réaliser sur la cible : fournir le secret privé côté serveur, effectuer
la recette fournisseur et déployer. L'ajout de l'adaptateur a été autorisé par
l'utilisateur après la revue des preuves locales. Aucun paramètre opérateur
n'a été modifié. Le Measurement Protocol seul n'offre pas toute l'attribution
automatique du tag navigateur ; les identifiants en mémoire ne permettent pas de
reconnaître un visiteur entre plusieurs documents. Le champ fixe
`engagement_time_msec=1` n'est pas une mesure du temps de lecture.
Aucune migration, contrat métier backend ou donnée de démonstration n'est modifiée.

Exploitation : livrer les nouveaux assets et headers, recharger les onglets de
l'ancienne version et desactiver tout tag injecte par un hebergeur externe.
Une session deja ouverte sur un ancien bundle ne recoit pas retroactivement ce correctif.

## MARKET-002 — Retour de paiement

Le navigateur genere 32 octets aleatoires avec Web Crypto avant l'initialisation,
conserve la capacite dans sessionStorage et l'envoie via X-Payment-Return-Token.
Le backend conserve uniquement SHA-256 dans checkout_request, dans la transaction
creant l'achat. Une reprise exige la meme capacite et la meme cle d'idempotence.
GET /public/gestion-achats/paiements/retour/{achat_id} exige cette capacite ;
X-Checkout-Session optionnel est verifie via les metadata Stripe pour les retours
Stripe. Le statut du webhook local reste la source de verite, y compris avant webhook.
La projection ne contient ni contact, ni jeton de gestion, ni QR, ni droit d'activation.
Expiration 24 h apres creation ; revocation via checkout_request.return_access_revoked
(la suppression locale seule ne revoque pas une copie du jeton). Aucun renouvellement automatique.
Le financement integral utilise le meme acces sans session Stripe.
Les anciens liens de gestion gardent leur autorisation ; aucun fallback anonyme.
Si l'onglet d'origine est perdu, utiliser les liens recus par email ou le support.
Les erreurs de verification ne doivent jamais inviter a repayer.

Une attente webhook ou une erreur reseau propose une nouvelle verification,
jamais un nouvel achat automatique. Deployer le backend compatible avant le
client et autoriser les en-tetes X-Payment-Return-Token et X-Checkout-Session
dans CORS.

## MARKET-003 - Faux succes Pro

La confirmation recharge le statut serveur a chaque ouverture, y compris apres un retour arriere ou pour le credit integral. URL et cache ne prouvent aucun paiement. Seul PAYMENT_CONFIRMED provenant de cette verification autorise le succes. Une erreur, un delai depasse ou un acces absent reste non confirme. La page ne pretend plus que l'email a ete livre. Le parcours particulier suit la meme regle de revalidation. Les deux confirmations partagent la resolution du statut ; PAYMENT_FAILED affiche explicitement un paiement echoue.

## MARKET-004 - Donnees dans URL API

POST initialiser exige un corps JSON valide. GET qrcode/detail exige X-QR-Token ; les anciennes query ne sont plus acceptees. Idempotence, credit, retour paiement et Live restent en headers. Publier le backend compatible puis le client dans la meme fenetre de livraison ; verifier les consommateurs tiers avant bascule. Les anciens logs peuvent encore contenir des URL : appliquer la politique de conservation et examiner les acces, sans exporter ces traces.

## MARKET-005 - Retrait Analytics

Refus, remise à zéro et changement de stockage entre onglets arrêtent les nouveaux
envois et annulent les requêtes encore en attente côté navigateur. Le stockage est
relu avant chaque émission ; un refus ou une remise à zéro reste prioritaire même
si son écriture échoue. Les écrans Marketplace et Live suivent les changements
entre onglets. Le nettoyage du fournisseur historique active `ga-disable` et
retire ses cookies accessibles, sans toucher aux cookies applicatifs. Un retrait
ne rappelle pas un événement déjà reçu par un destinataire. La collecte externe
reste indisponible sans la configuration privée de MARKET-001.

## MARKET-006 - Priorite des .env

Resolution commune aux cles publiques : processus > .env.MODE.local > .env.MODE > .env.local > .env. Liste exacte dans scripts/public-config.cjs, utilisee par le build Vite, le generateur statique et le serveur Node (processus seulement). envPrefix est vide : meme une cle privee commencant par LOCALEO_ ou VITE_ ne peut entrer dans le bundle. Le parseur accepte des valeurs litterales ; pas de substitution de variables. `node scripts/write-app-config.cjs production --check` resout sans ecrire.

## MARKET-007 - Inscription non rejouable

Idempotency-Key est un UUID v4. Verrou transactionnel de l'animation avant recherche de reprise, unicite existante email/animation et cle/acteur/route. La table d'idempotence conserve empreintes de cle et payload, participant_id et key_id, jamais le token brut. Le token est reconstructible par HMAC SHA-256 avec separation de contexte et keyring QR, puis son empreinte et sa validite sont controlees au rejeu. Meme cle et payload : meme resultat pendant 24 h, meme apres fermeture des inscriptions ; autre payload : conflit. Aucun nouvel email au rejeu. Une rotation conserve l'ancienne cle pendant la fenetre de reprise, sinon le support est requis.

Apres perte de reponse, delai depasse, erreur serveur ou absence de capacite dans le resultat, le formulaire conserve le payload et la cle UUID v4. Les champs restent verrouilles et la reprise reutilise exactement cette demande. Une erreur metier explicite permet a nouveau la correction. Aucun acces n'est presente sans token recu.

## MARKET-008 - Continuite participant

Apres validation du token (expiration et revocation incluses), une projection participant reutilise uniquement les champs publics autorises. Elle ne depend ni de l'abonnement ni de la publication de la commune ni du filtre de vendabilite des lots. La decouverte garde ses filtres. Le participant voit les etats annule/cloture/archive, sans invitation a se reinscrire ni droit de validation supplementaire. QR et autorisations metier restent verifies separement.

Marketplace et Live affichent cette projection sans confondre fin de visibilite
et token invalide. Elle ne permet aucune nouvelle inscription.

## MARKET-009 - Pro sans credit rejete

GET /public/gestion-achats/paiements/conditions-achat-pro indique required, version et text sans exiger de session credit. Lorsque requis, tout achat Pro exige une acceptation explicite de la version courante et un SIRET avant ouverture de transaction. Cette regle de domaine vaut avec ou sans credit ; la reservation reste liee a l'organisation authentifiee. Aucun consentement ne decoule du simple token credit.

Le formulaire charge les conditions applicables depuis le backend, independamment du solde ou du flag local. Si required est vrai, le texte et la version sont presentes et une case non pre-cochee est obligatoire. Une ancienne session credit ne constitue pas une acceptation. Une erreur de chargement bloque le paiement sans creer d'achat.

## MARKET-010 - Quantite non bornee

Plafond de commande fixe a 1000 coffrets, minimum 1, entier strict (booleens, chaines et decimaux refuses). Controle API, domaine et debut du use case avant transaction, credit et Stripe. Migration v224 ajoute et valide CHECK quantite BETWEEN 1 AND 1000. Executer le diagnostic SQL commente avant migration ; une anomalie historique bloque la validation et doit etre rapprochee manuellement, sans correction automatique de donnees financieres. Les calculs restent en centimes entiers.

Le formulaire Pro applique les memes bornes. Une valeur decimale ou hors borne
bloque tous les boutons de paiement ; la validation serveur reste obligatoire.

## Contrat et recette

Contrat OpenAPI des routes concernees, extrait le 7 septembre 2026 : [OpenAPI](../corrections-marketplace-2026-09-06.openapi.json).

[Formation, procedure de livraison et recette](../../exploitation/guide-corrections-marketplace-2026-09-06.md). Les corrections locales ne constituent pas une preuve de deploiement.

Le [complément de recette issu de la Marketplace](../../exploitation/marketplace/guide-corrections-marketplace-2026-09-06.md)
conserve la provenance des vérifications côté interface.
