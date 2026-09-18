# VERDICT DE MISE EN PRODUCTION

## 🔴 NO-GO PRODUCTION — état initial audité

Application : Localeo Commerçants / Pro. Révision initiale : `e46322f`.
Ce compte rendu conserve les résultats de l'audit initial. Les corrections et
preuves ultérieures sont suivies dans [le registre de remédiation](remediation-preproduction-2026-09-06.md).
Un contrôle non vérifiable ne constitue pas une vulnérabilité démontrée.

## 1. Executive summary

Deux défauts frontend bloquent le lancement : une réponse d'un ancien compte
peut contaminer le cache du compte courant (PRO-001), et tout HTTP 409 de
validation Animation est affiché comme une étape déjà validée (PRO-002).

L'audit initial portait sur le frontend et ses OpenAPI, sans backend dans le
dépôt audité. Aucun appel de mutation n'a été envoyé à l'API métier.
La phase de correction découvre le dépôt voisin `localeo-backend` : les
conclusions serveur seront désormais confrontées à ce code, sans réécrire
rétroactivement les preuves de l'audit initial.

| Vérification initiale | Résultat |
| --- | --- |
| Build production | Réussi, sortie temporaire |
| Tests unitaires | 76 réussis, 16 fichiers |
| E2E | 4 réussites, 2 échecs ; processus interrompu après résultats pendant sa terminaison |
| npm audit production | 0 vulnérabilité signalée |
| npm audit complet | 13 dépendances affectées : 7 high, 4 moderate, 2 low, toutes dans l'outillage |
| Cache A/B | Fuite reproduite avec réponses différées simulées |
| HTTP 409 | Faux résultat `replayed` reproduit |
| Actions backend false | Réactivation frontend reproduite |

## Cartographie fonctionnelle

| Routes | Parcours / composants |
| --- | --- |
| `/`, `/menu` | MerchantLoginGate, MerchantMenu, session |
| `/mot-de-passe-oublie`, `/commercants/initialiser-mot-de-passe`, `/commercants/reinitialiser-mot-de-passe` | Mot de passe et token |
| `/validation` | ValidationActionWorkspace : QR coffret/Animation, confirmation, consommation, annulation |
| `/prestations` | Liste, détail, édition libellé/description |
| `/reversements`, `/dashboard-operationnel` | Encours, historique, indicateurs |
| `/profil`, `/mot-de-passe`, `/page-publique`, `/contact` | Contact, WebPush, accès, contenu public, support |
| `/animations`, `/animations/:animationId`, `/notifications` | Animations acceptées, mission, règlement, flyer, notifications |
| `/animations/invitations`, `/commercants/animations/invitations/:demandeId` | Acceptation/refus/retrait |
| `/finance/*` | Facturation, corrections et Chorus sous feature flags |
| `/stripe-connect/onboarding/return`, `/stripe-connect/onboarding/refresh` | Synchronisation et reprise Stripe |

Stack : React/JavaScript, Vite, React Router, hooks locaux. Session dans
`sessionStorage`, cache Animation en mémoire. Externes : API Localeo, DAM,
Stripe Connect, services WebPush. Aucun espace administrateur dans cette PWA.

## 2. Bloqueurs production

### PRO-001 — Réponse d'un ancien compte réinjectée dans le cache du compte courant

- Sévérité : HAUTE. Bloquant : OUI. Responsable : frontend.
- Localisation initiale : `src/features/animations/queries.js:48-91,125-134`, `src/App.jsx:3290-3324`.
- Problème : cache partagé, générations remises à zéro au changement de session,
  réponses anciennes et décisions encore capables d'écrire dans le nouveau cache.
- Scénario : réponse de A retardée, logout/login B dans la même SPA, chargement
  de B, retour tardif de A, puis lecture du cache sous B.
- Preuve exécutée : `Read using B session: {"owner":"A","privateData":"invitation A"}`.
- Impact : exposition de données Animation/participation sur navigateur partagé.
  Aucun contournement des autorisations serveur n'est déduit de ce défaut.
- Correction : époque de session immuable, rejet des résultats obsolètes,
  invalidation des lectures et mutations, nettoyage au logout.

### PRO-002 — Tout HTTP 409 de validation Animation devient « Étape déjà validée »

- Sévérité : HAUTE. Bloquant : OUI. Responsable : frontend ; contrat backend à vérifier.
- Localisation initiale : `src/App.jsx:3934-3948,4090`.
- Preuve : `error?.status === 409 ? "replayed" : "error"` ; handler réel testé
  avec un code fictif `ANIMATION_CLOSED` : état obtenu `replayed`.
- Scénario : fermeture de l'animation entre scan et confirmation, refus serveur
  409, interface présentant l'étape comme enregistrée.
- Impact : décision opérationnelle fondée sur un résultat faux.
- Correction : seul un résultat métier explicite peut confirmer un rejeu ;
  les conflits restent des refus et doivent permettre une réconciliation.

## 3. Sécurité

Pas de sink HTML dangereux, `eval` ou secret serveur identifié dans les sources.
Les contenus administrables sont rendus comme texte JSX. La clé VAPID est
publique. Les logs d'erreur UI ne transportent pas les sessions/payloads.
URLs Stripe filtrées sur HTTPS/connect.stripe.com. En-têtes prévus dans
`render.yaml`, application effective en production non vérifiée.

### PRO-005 — QR sensible transporté dans l'URL de requête

- Sévérité : MOYENNE. Bloquant : NON. Responsables : frontend/backend/infrastructure.
- Localisation initiale : `src/App.jsx:508`, `src/features/animations/api.js:59`.
- Preuve : QR coffret dans query string ; token participant dans chemin public.
- Scénario : infrastructure enregistrant les URLs complètes.
- Impact : QR/tokens présents dans des journaux ; collecte et réutilisabilité
  effectives non démontrées durant l'audit initial.
- Correction : corps JSON coffret, résolution authentifiée en corps si disponible
  pour Animation, masquage des journaux et contrôle des durées/portées serveur.

Images : JPEG/PNG/WebP, 5 Mo côté client ; PDF : MIME, extension, non-vacuité et
10 Mo. Signature réelle, quotas et autorisations doivent être contrôlés serveur.
Le DAM public sans Bearer est conforme au contrat initial, pas une omission
frontend démontrée. Tokens de reset dans l'URL pendant le formulaire : vérifier
usage unique, expiration et journalisation ; nettoyer l'URL dès acquisition.

## 4. Authentification / autorisations

Login/mot de passe par POST ; session Bearer opaque dans sessionStorage ;
validation distante à la navigation ; contrôle local d'expires_at ; aucun
refresh token ni renouvellement infini identifié. Les 401/403 sont hétérogènes.
sessionStorage reste accessible au JavaScript de l'origine, pas un coffre secret.

### PRO-004 — Nettoyage local retardé par l'invalidation distante

- Sévérité : MOYENNE. Bloquant : NON. Responsables : frontend ; révocation backend à vérifier.
- Localisation initiale : `src/App.jsx:489,6236`.
- Preuve : nettoyage après `await invalidateMerchantSession`, sans timeout.
- Scénario : logout sur réseau dégradé ; écran/session locaux restent accessibles.
- Impact : déconnexion locale retardée et révocation distante non confirmée.
- Correction : nettoyage immédiat, révocation bornée, retour honnête si échec.

Rôles : anonyme (connexion/reset), commerçant (son espace), scope
`commercant:validation` documenté pour consommer ; admin/partenaire hors PWA.
Les flags Finance ne constituent pas des permissions. CORS et les cookies
éventuellement utilisés par d'autres applications nécessitent une vérification serveur.

## 5. Intégrité métier

Le coffret est ouvert par transaction serveur ; le front transmet transaction
et statut de prestation, sans prix ou `status=CONSUMED`. La propriété et
l'atomicité ne sont pas prouvées par un bouton caché. `inferPackContext` peut
compléter depuis le QR une réponse serveur incomplète : supprimer ce fallback.
Les montants proviennent du backend ; « À recevoir » est une somme indicative
des mouvements reçus, pas une commande financière. Stripe est resynchronisé
serveur, jamais validé à partir du seul retour navigateur.

### PRO-007 — Réactivation frontend d'actions explicitement refusées par le backend

- Sévérité : MOYENNE. Bloquant : NON. Responsable : frontend.
- Localisation initiale : `src/features/animations/contracts.js:107`.
- Preuve exécutée : `actions:false` devient `{"accepter":true,"refuser":true,"retirer":false}`.
- Scénario : backend refuse une décision EN_ATTENTE ; date locale non dépassée ;
  navigateur réactive les actions. Certaines dates à minuit sont aussi prolongées.
- Impact : commandes proposées à tort ; violation effective serveur non démontrée.
- Correction : interdictions serveur prioritaires ; date civile distincte d'un instant UTC.

### PRO-009 — Détail de facture groupée incompatible avec le contrat documentaire

- Sévérité : MOYENNE. Bloquant : NON tant que Finance reste désactivé.
- Localisation initiale : `src/features/finance/api.js:26` et spec Epic 50:297.
- Preuve : GET détail appelé alors que la spec demande une recherche dans la liste.
  Aucun endpoint Finance dans les OpenAPI locaux initiaux.
- Scénario : backend conforme à cette spec renvoie 404 à l'ouverture du détail.
- Impact : consultation/traitement impossibles.
- Correction : confronter au backend actuel, adapter le contrat et la fonctionnalité
  avant activation ; ne pas recréer une fonction éventuellement décommissionnée.

## 6. Gestion des appels API

Inventaire de référence détaillé : [docs/api.md](../../specifications/espace-commercant/contrats-api.md), `api/localeo-openapi.json` et
modules `src/features/*/api.js`, `src/lib/webPush.js`, fonctions de `src/App.jsx`.
Les corrections de contrat seront intégrées à ces sources.

| Famille | Méthodes / endpoints consommés | Auth / payload / résultat |
| --- | --- | --- |
| Identité | POST auth login, oubli, initialisation, réinitialisation ; GET session/valider ; POST session/{id}/invalider, me/mot-de-passe | Login/reset sans Bearer ; sinon Bearer ; credentials/token en JSON, session/confirmation |
| Profil | GET profils/commercants/me ; PATCH referencement/commercants/me/contact | Bearer ; nom/prénom/téléphone |
| Prestations | GET commercialisation/commercants/{c}/prestations et /{id} ; PATCH profils/commercants/me/prestations/{id} | Bearer ; libellé/description ; rechargement |
| Page | GET profils/commercants/me/page, /apercu, /demandes ; PATCH /brouillon ; POST /soumettre-moderation | Bearer ; textes/URLs/références images |
| DAM | POST public/dam/images ; GET images | Public ; multipart fichier/nom ; URI/binaire |
| Coffret | POST exploitation/validation/ouvrir-transaction, /valider-prestation, /validations/{id}/annuler | Bearer ; QR, transaction/prestation, motif/commentaire |
| Lectures coffret | GET gestion-achats/achats/{a}/coffrets-instances/{i}, /prestations ; public/commercialisation/coffrets/{id} ; referencement/commercants/{c} | Bearer sauf détail public ; résumé/statuts/libellés |
| Activité | GET exploitation/commercants/me/dashboard-operationnel | Bearer ; dates, group_by, prestation_id, inclure_versions |
| Reversements | GET gestion-reversement/commercants/{c}/reversements/mouvements/a-reverser, /mois/{n} | Bearer ; encours/historique |
| Support | GET public/support/contacts/motifs ; GET/POST support/commercants/{c}/messages ; GET /{thread} ; POST /{thread}/reponses | Bearer sauf motifs ; message/motif/références |
| Stripe | GET referencement/commercants/me/stripe-connect ; POST /onboarding, /synchroniser | Bearer ; statut ou URL filtrée |
| WebPush | GET/PATCH exploitation/commercants/me/notifications/preferences ; GET/POST webpush/abonnements ; DELETE /{id} ; POST webpush/deeplinks/resoudre | Bearer ; booléen, endpoint/clés/appareil, deeplink |
| Animation | GET animation-locale/commercants/me/contexte, /animations, /animations/{id}, /notifications, /demandes-participation, /demandes-participation/{id} | Bearer ; pagination ; projections normalisées |
| Commandes Animation | POST demandes-participation/{id}/accepter, /refuser, /retirer ; POST notifications/{id}/lire ; POST animation-locale/notifications/lire-tout ; DELETE notifications/{id} | Bearer ; clés d'idempotence, motifs facultatifs |
| Flyer | GET animations/{id}/flyer, /flyer/download | Bearer ; métadonnées/blob ; 404 masque le flyer |
| Scan Animation | GET public/animation-locale/participants/{token} ; POST protected/animation-locale/validations | Token puis Bearer ; qr_token/etape_id/Idempotency-Key |
| Finance historique | GET demandes/factures ; POST transitions/dépôt/correction ; POST/PATCH brouillon ; POST émission/mandat/révocation | Flags ; Bearer ; expectedVersion, PDF, données facture ; contrat à confronter au backend |

## 7. Gestion des erreurs

### PRO-003 — Résultat d'une mutation confondu avec le résultat de son rechargement

- Sévérité : MOYENNE. Bloquant : NON isolément. Responsables : frontend et preuve backend.
- Localisation initiale : `src/App.jsx:3862,4009,4623`.
- Preuve : commande et GET dans le même try/catch ; état ancien conservé si GET échoue.
- Scénario : POST accepté, GET en 500 ; bouton à nouveau disponible sur l'ancien état.
- Impact : résultat ambigu et retry d'une commande déjà effectuée ; double écriture non prouvée.
- Correction : distinguer succès commande/échec lecture ; état indéterminé sur perte
  de réponse ; réconcilier avant nouvelle commande ; conserver les erreurs typées.

Inclut : 401/403 hétérogènes, appels sans délai maximal, erreurs Finance masquées,
enrichissement facultatif d'invitation bloquant, message de boundary affirmant
sans preuve que les données n'ont pas été modifiées.

## 8. Concurrence / doubles actions

Verrou ref pour scan et validation Animation ; boutons pending pour coffret.
Aucune garantie frontend contre deux téléphones/onglets. Transaction perdue
au refresh. Atomicité de consommation/annulation et unicité du mouvement
doivent être établies dans la transaction et les contraintes SQL backend.

### PRO-008 — Nouvelle clé d'idempotence à chaque tentative de décision

- Sévérité : MOYENNE. Bloquant : NON. Responsable : frontend ; idempotence métier serveur à vérifier.
- Localisation initiale : `ParticipationRequestDetailPage.jsx:65`.
- Preuve : génération de clé dans chaque confirmDecision.
- Scénario : acceptation enregistrée, réponse perdue, confirmation avec une nouvelle clé.
- Impact : retry non reconnu par la clé ; le serveur peut avoir une autre protection.
- Correction : clé stable par payload/commande incertaine, verrou synchrone, relecture sur conflit.

## 9. Cloisonnement des données

PRO-001 démontré. Backend initialement NON VÉRIFIABLE pour commerçant,
prestation, achat, instance, support, animation, invitation, notification,
flyer, facturation et preuve documentaire. Exiger tests A/B sans se limiter aux scopes.

### PRO-006 — Pagination non parcourue pour les listes Animation

- Sévérité : MOYENNE. Bloquant : NON. Responsable : frontend.
- Localisation initiale : `queries.js:101`, `ParticipationRequestsPage.jsx:82`.
- Preuve : page 1 uniquement, limites 20 animations et 50 invitations.
- Scénario : invitation en attente sur une page suivante, invisible dans l'UI.
- Impact : échéance manquée, compteurs incomplets.
- Correction : parcours de pagination explicite et compteurs couvrant le périmètre réel.

## 10. Conformité ADR / architecture

Références : architecture/API, Epic 10, Epic 41, arbitrages Epic 56, Epic 50, PWA.
Aucun ADR formel trouvé dans le dépôt frontend. L'ancien QR commerçant est
remplacé par Epic 10 : sa suppression n'est pas une non-conformité.

### PRO-012 — Référentiel documentaire contradictoire

- Sévérité : FAIBLE. Bloquant : NON. Responsables : frontend/backend pour leurs contrats.
- Localisation : [docs/specification/specification-version-actuelle.md](../../specifications/espace-commercant/README.md), [docs/architecture.md](../../architecture/frontends/commercant/architecture.md), OpenAPI.
- Preuve : documentation « actuelle » décrivant login QR et contact non branché.
- Scénario : recette/intégration basée sur l'ancien contrat.
- Impact : attentes et tests divergents.
- Correction : source de vérité actuelle, archives signalées, contrat unique,
  formation et epics mis à jour sans rouvrir artificiellement un epic terminé.

## 11. Tests

76 tests initiaux réussis. E2E : contraste footer et invitation bloquée sur
enrichissement non mocké. Tests backend, double téléphone, réponse perdue,
cache multi-compte, révocation et contrats Finance insuffisants initialement.

### PRO-011 — Contraste insuffisant du pied de page

- Sévérité : FAIBLE. Bloquant : NON techniquement ; CI doit repasser au vert.
- Localisation : `src/styles.css:2795`.
- Preuve axe : contraste 4,41:1 au lieu de 4,5:1.
- Scénario/impact : lecture du footer moins accessible.
- Correction : couleur conforme et test a11y.

## 12. Dépendances / build

Build minifié réussi, aucun sourcemap identifié. API production correcte dans
le bundle contrôlé. Pas de TypeScript : sources JS/JSX. Lockfile v3 cohérent.
Installation vierge indépendante non exécutée pendant l'audit initial.
Origine QR de staging autorisée en production : retirer ou justifier.

### PRO-010 — Vulnérabilités dans l'outillage de développement

- Sévérité : MOYENNE projet. Bloquant : NON.
- Localisation : package-lock.json : tmp, extract-zip, qs, uuid, chaîne Lighthouse.
- Preuve : audit complet 13 alertes, omit=dev aucune.
- Scénario : archive/chemin/entrée hostile traité par l'outillage selon l'avis.
- Impact : poste/CI ; aucun chemin d'exploitation PWA démontré.
- Correction : mises à jour/alternatives maintenues, audit et exécution des outils.

## 13. Risques résiduels

À vérifier côté backend/infrastructure : hachage/rate limiting, révocation,
tokens à usage unique, BOLA, transactions SQL concurrentes, expiration,
versions, recalcul financier, CORS, quotas/types fichiers, minimisation des
réponses publiques et WebPush, masquage des logs, configuration déployée.
Ne pas déclarer ces contrôles conformes à partir de tests frontend simulés.

## 14. Matrice de conformité initiale

| Référence / règle | État initial | Preuve |
| --- | --- | --- |
| Architecture : scans serveur / reprise | PARTIEL / NON CONFORME | PRO-002/003, état mémoire |
| Epic 10 : login et sessionStorage | CONFORME frontend | loginMerchant/useMerchantSession |
| Epic 10 : révocation | PARTIEL | PRO-004 |
| Autorisations API | NON VÉRIFIABLE | Backend absent du dépôt initial |
| Stripe : statut serveur, URL non persistée | CONFORME frontend | StripeConnect |
| Epic 41 : conflit distinct du rejeu | NON CONFORME | PRO-002 |
| Epic 56 : authentification des décisions | CONFORME frontend | Bearer et route |
| Epic 56 : isolation/idempotence/échéance | NON CONFORME/PARTIEL | PRO-001/007/008 |
| Flyer après publication | PARTIEL | Disponibilité API ; serveur non vérifié |
| Epic 50 : détail groupé | NON CONFORME au document initial | PRO-009 |
| PWA : pas de login automatique | CONFORME | Résolution après authentification |
| PWA : payload minimisé | NON VÉRIFIABLE | Émetteur backend absent |
| En-têtes déployés | PARTIEL | render.yaml seulement |
| Build/lockfile | CONFORME localement | Build réussi |
| Parcours critiques / documentation | NON CONFORME | PRO-012 et lacunes de tests |

## 15. Plan de remédiation

- P0 : PRO-001/002, tests réseau/concurrence, preuves backend et E2E verts ;
  contrats Finance avant toute activation.
- P1 : PRO-003 à 010, uniformisation des erreurs, délais réseau, vérifications
  infrastructure, contrôle d'installation/build.
- P2 : documentation et extraction des workspaces, tests de contrat continus.

## Checklist initiale et conclusion

| Question | Réponse initiale |
| --- | --- |
| Authentification robuste / autorisations serveur | INCERTAIN |
| Cloisonnement garanti | NON |
| Données sensibles frontend | OUI |
| Secrets dans bundle / XSS sérieux démontré | NON |
| Manipulation de payload exploitée | NON démontrée, backend non vérifiable |
| Double soumission dangereuse | OUI pour l'ambiguïté opérationnelle ; double écriture non prouvée |
| États cohérents / erreurs critiques correctes | NON |
| Violation majeure d'ADR formel | NON identifié |
| Build sain | OUI localement |
| Tests critiques suffisants | NON |
| Bloqueur restant | OUI |

Un utilisateur peut-il provoquer une incohérence ou accéder à des données
d'un autre compte ? **OUI**, frontend démontré. Un problème justifie-t-il de
repousser le lancement ? **OUI**, PRO-001 et PRO-002.

Références externes : [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
et [OWASP HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html).
