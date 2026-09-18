# Suivi des corrections backend et Marketplace

Date : 7 septembre 2026. Perimetre : les dix constats MARKET-001 a MARKET-010 du [rapport du 6 septembre](audit-preproduction-2026-09-06.md) et de son [plan de correction](plan-corrections-backend-marketplace-2026-09-06.md).

## Etat de la livraison

Les dix constats ont une correction implementee, des tests et des commits locaux identifies ci-dessous. Les specifications, contrats OpenAPI, epics concernes et consignes de formation ont ete actualises dans les deux depots. Analytics reste suspendu : sa reactivation ne fait pas partie de cette livraison.

Le NO-GO du rapport initial decrit les sources auditees le 6 septembre ; il ne decrit pas les sources corrigees. Aucun GO de production n'est toutefois prononce : les versions reellement servies, la migration sur la base cible, les prestataires et la configuration de recette/production n'ont pas ete verifies. Aucun deploiement ni migration d'une base metier n'a ete effectue. Les commits de cette campagne sont locaux.

## Registre de resolution

Chaque ligne est corrigee et testee localement. Les references sont propres au depot indique.

| ID et libelle du rapport | Correction livree | Commits Marketplace | Commits backend | Preuves principales |
| --- | --- | --- | --- | --- |
| MARKET-001 - Jetons dans Analytics | Suspension effective du fournisseur, meme avec ancien consentement et flag actif ; CSP sans script Google | 9304fe6 | Sans correction metier requise | Test de suspension et navigation navigateur directe/SPA sans appel Google |
| MARKET-002 - Retour de paiement | Capacite aleatoire avant checkout, hash serveur, retour minimal autorise et reprise avec la meme capacite, y compris credit integral | 5428d82 | 17d403d, df8839e | Domaine, API, retour mobile et reprise PostgreSQL avec refus d'une autre capacite |
| MARKET-003 - Faux succes Pro | Confirmation Pro et particulier uniquement apres verification fraiche du statut d'achat backend ; URL, cache et statut Stripe seuls insuffisants | 9fabe48, 228c7c6, 738dc34 | Statut fourni par MARKET-002 | Absence d'acces, 401/403/500, attente, succes, cache ancien et statut contradictoire |
| MARKET-004 - Donnees dans URL API | Initialisation en JSON et detail QR en X-QR-Token ; ancien transport query refuse | 48275f0 | cfbd67c, 8218159 | Validation API, appel client, quotas JSON et OpenAPI |
| MARKET-005 - Retrait Analytics | Retrait fournisseur, cookies GA accessibles retires, refus/remise a zero et synchronisation entre onglets | d6879ac | Sans correction metier requise | Fournisseur simule deja charge, cookies et evenements storage |
| MARKET-006 - Priorite des .env | Resolveur commun, priorite du processus et des fichiers de mode, liste exacte des seules cles publiques | e4101fc | Sans correction metier requise | Fixtures de priorite, serveur, build en memoire sans sentinelles privees LOCALEO_/VITE_ |
| MARKET-007 - Inscription non rejouable | Cle UUID v4 et payload conserves ; verrou SQL, reprise 24 h, token reconstructible sans stockage brut, aucun email duplique | 74424b3 | 3f8f2d2, f708efa | Perte de reponse dans le navigateur, concurrence sur PostgreSQL, conflit et rollback |
| MARKET-008 - Continuite participant | Projection dediee apres validation du token, independante du catalogue et de l'abonnement ; etats metier visibles | 8191e08 | 9683789 | Etats annule/cloture/archive, exclusion des champs internes, participant accessible avec catalogue en 404 |
| MARKET-009 - Pro sans credit rejete | Conditions et version chargees sans session credit ; acceptation explicite controlee dans le domaine avant effets | f3894b5, fd3ecf6 | 84f4253 | Formulaire sans credit, case non pre-cochee, version perimee et SIRET refuses avant transaction |
| MARKET-010 - Quantite non bornee | Entier strict de 1 a 1000 dans le formulaire, API, domaine et contrainte SQL v224 | 551895d | c79067a | Bornes et types invalides avant effets ; migration SQL reelle sur schemas jetables, refus d'un historique invalide |


## Campagne de verification

- Backend : 234 tests passent dans la campagne consolidee tests/security et tests/application/services/test_participants_animation.py, sans skip (95,14 s), via scripts/archives/run_market_postgres_tests.py. La base PostgreSQL 18 est une instance jetable, verifiee par son repertoire et son port ; elle a ete arretee apres recette. Les fournisseurs HTTP sont bloques ; aucun .env metier n'est charge.
- Backend complementaire : campagne domaine achats, initialisation, webhooks, passerelle Stripe et catalogue : 174 succes initiaux et 3 echecs de fixtures participants devenues incompatibles avec le verrou ajoute par un changement ANIM concomitant. Les fixtures ont ete corrigees et leurs cinq tests ont repasse, puis ont ete inclus dans la campagne consolidee ci-dessus. Cette campagne complementaire n'est pas presentee comme une execution unique sans echec.
- PostgreSQL : les six integrations explicites de paiement, activation, inscription et migration ont passe ; la derniere campagne de securite consolidee les execute aussi. La contrainte v224 a ete testee a partir du fichier SQL, pas uniquement des metadonnees ORM.
- Frontend : 34 tests de securite et 10 tests serveur passent. La campagne consolidee (npm test) passe le lint puis 61 des 62 scenarios navigateur ; elle termine en echec sur le delai global de la fiche coffret, et ne doit pas etre presentee comme une commande integralement verte. Une reprise sur le build actualise passe 11 scenarios MARKET ; les deux cas restants sont verifies par la reprise finale detaillee ci-dessous.
- Build production : compilation validee ; un build supplementaire en memoire ne contient aucune des trois sentinelles privees injectees dans LOCALEO_PRIVATE_SECRET, LOCALEO_API_BASE_URL_SECRET et VITE_PRIVATE_SECRET. Le lint est inclus dans npm test.
- Contrats : extraction OpenAPI locale sans reseau, sept routes concernees et schemas transitifs ; les snapshots des epics 41/42 sont synchronises sur ces changements. Les nouveaux scenarios navigateur MARKET sont inclus dans la commande npm test habituelle (bed9ca0). La documentation backend finale est commitee dans bcd3ec4.

Les premiers echecs observes ont ete traites : fixture de conditions Pro manquante dans la recette mobile, doubles de verrouillage/date participants et cookie de session territorial conserve avec deux domaines de test. Les corrections de fixtures sont commitees. Les assertions de securite n'ont pas ete desactivees. Deux corrections de recette finales concernent l'attente de la fiche coffret (panneau affiche et polices chargees au lieu de networkidle, budget global de 180 s pour huit formats) et le ciblage du premier recapitulatif parmi les trois occurrences du libelle de paiement echoue. Toutes les assertions de geometrie sont conservees.

Reprise finale : les deux tests restants passent (2 passed, 2,7 min) sur le build actualise : fiche coffret en huit formats et PAYMENT_FAILED Pro. La campagne et ses reprises couvrent les 63 scenarios navigateur actuels ; les 12 scenarios MARKET ont tous passe. Le correctif de recette coffret est commite dans 7f5b341. Le build de production et le lint passent ; la syntaxe des deux fichiers Playwright a aussi ete verifiee. Aucun test en echec identifie dans cette campagne ne reste sans correction verifiee.

## Documents mis a jour

- [Specifications correctives Marketplace](../../specifications/securisation-production/corrections-marketplace-2026-09-06.md) et [contrat OpenAPI](../../specifications/corrections-marketplace-2026-09-06.openapi.json).
- Specifications correctives et OpenAPI equivalents dans localeo-backend ; specifications fonctionnelles et techniques des deux projets, epics Analytics/animations/paiement/credit concernes.
- [Formation, procedure de livraison, repli et recette](../../exploitation/marketplace/guide-corrections-marketplace-2026-09-06.md), egalement disponible dans le backend et reliee au guide de formation backoffice.

## Conditions restant a lever avant GO production

1. Fournir l'environnement de recette et la procedure de deploiement ; figer les deux revisions a livrer et verifier la version effectivement servie. Le backend partage contient aussi des commits ANIM/PRO concomitants qui ne sont pas une livraison MARKET isolee. Le commit ANIM f3749b3 est notamment arrive apres la campagne consolidee ; il exige la validation du responsable de ce lot dans le couple final.
2. Verifier les avis de securite actuels des dependances. Le controle npm externe est en attente d'autorisation explicite : le controle automatique avait refuse l'export de l'inventaire pendant l'audit. La demande porte sur les seuls noms et versions des paquets publics ; aucun resultat actuel n'est presume.
3. Executer le diagnostic et la migration v224 sur la cible, verifier le statut valide de la contrainte et conserver les preuves. Une anomalie historique doit etre rapprochee, sans correction financiere automatique.
4. Livrer le couple compatible JSON/headers, verifier CORS, configuration publique, caches et absence de tag externe. Recetter les paiements avec prestataires de test, les webhooks/emails, les reprises et la continuite participant selon le guide. Garder Analytics suspendu et le credit desactive jusqu'a validation de ses parcours.

Ces points dependent de l'environnement cible et de l'autorisation externe ; ils ne sont pas consideres resolus par les tests locaux. Le guide fournit les etapes concretes et les criteres de verification avant toute decision de mise en production.
