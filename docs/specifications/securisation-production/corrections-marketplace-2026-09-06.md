# Contrats correctifs Marketplace du 6 septembre 2026

> Consolidation du 18 septembre 2026 : ce document réunit les contrats backend
> de `corrections-marketplace-2026-09-06.md` et les compléments de présentation
> issus de `corrections-marketplace-2026-09-06.marketplace.md`.
> Les identifiants MARKET-001 à MARKET-010 sont conservés. Les constats d'audit
> et résultats de tests cités restent ceux des corrections historiques ; cette
> consolidation n'est ni une nouvelle recette ni une preuve de déploiement.

## MARKET-001 — Jetons dans Analytics

Analytics est suspendu dans le code, y compris avec un consentement ancien et un
flag runtime actif. Le serveur ne permet plus le script Google dans sa CSP.
La reactivation exige un correctif revu et une recette reseau des navigations SPA
sensibles ; changer une variable ne reactive pas la collecte.

Test : `node --test tests/security/analytics-suspension.test.cjs`.

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

Refus, remise a zero et changement storage entre onglets propagent le retrait au fournisseur deja charge, activent ga-disable et retirent les cookies GA accessibles sur le domaine. Les cookies applicatifs restent intacts. Analytics reste suspendu par MARKET-001 ; aucun flag ne contourne cette suspension.

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
