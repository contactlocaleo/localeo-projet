# E69 — Vérification et préparation de livraison

Version **V1.3 — implémentation locale du 1er octobre 2026**. État : **En cours**.
Aucun déploiement, migration distante, compte réel ni recette en environnement partagé. Sources : [backlog](../../roadmap/en-cours/epic-69-profils-acces-erp-satellites-backlog.md),
[contrats](architecture-contrats.md), [permissions](permissions-surfaces.md).

## Traçabilité des 27 critères

Les scénarios ci-dessous constituent les exigences de référence. Les groupes de
preuves ajoutés à chaque critère renvoient aux fichiers exécutés décrits plus bas,
sans affirmer que toutes les variantes ont été testées ou acceptées en cible.
D = domaine pur, A = application/HTTP, P = PostgreSQL isolé, UI = navigateur.

| Critère / groupes de preuves locales | Comportement et scénarios de référence | Documentation / contrat | Fixtures / livraison |
| --- | --- | --- | --- |
| CA-01 — ID, HTTP | Identité : D combinaisons de rôles, A attribution admin et refus rôle ADMIN ; résultat audit/version | DTO compte, guide attribution | L/B/F/B+F ; migration ne crée pas d'admin |
| CA-02 — SUR, FIN, UI | Identité + projections : A/UI listes/détails/compteurs filtrés, aucune donnée technique à L | Matrice `metier.consulter` | Deux communes, données mixtes, noms identiques |
| CA-03 — SUR, MET, UI | Identité + métier : A refus L par méthode/URL/alias/commande en masse/GET à effet ; aucun appel fournisseur | Catalogue d'actions | Fake mail/Stripe/IA et état DB inchangés hors audit/session |
| CA-04 — MET, UI | Métier + identité : A/UI B gère parcours catalogue/onboarding/Support/Atelier ; garde domaine conservé | Matrice par action et contrats consommateurs | Dossier éligible/inéligible ; inventaire des refus résiduels |
| CA-05 — SUR, HTTP | Identité : A SQLAdmin CRUD/actions/exports, technique, batch, alias et profond refusés à L/B/F/B+F | Principal typé, cartes/navigation | Même compte avec rôle falsifié dans requête |
| CA-06 — HTTP, UI | Auth historique : A/UI login configuré, SQLAdmin et outils conservés | Compatibilité historique | Session avant/après migration ; compte historique non migré |
| CA-07 — ID, HTTP | Identité : A rôle métier ne peut créer/inviter/attribuer/reset un utilisateur interne | API utilisateurs | Falsification champs compte/capacité/CSRF |
| CA-08 — ID, PG, UI | Identité : P/UI retrait rôle et désactivation pendant session/commande/rejeu | Point d'ordre transactionnel | Deux sessions, ancien formulaire, commande déjà en file |
| CA-09 — PG, DEMO | Migration : P inventaire/correspondance explicite, aucun gain de scope ni perte admin | Procédure bascule | Anciens rôles dont FINANCE/EXPLOITATION ; rollback sans restauration de secrets |
| CA-10 — FIN, MET | Documentaire + identité : A export/pièce mêmes champs et scope ; lien réutilisé après révocation refusé | Lecture de document existant | Pièce KYC, facture et reçu absent ; aucune génération cachée |
| CA-11 — FIN, UI | Finance + identité : A/UI E65 L/B/F autorisés aux projections limitées, Audit/argent admin seuls | Dépendance E65 actualisée | Compteurs territoriaux, commande multi-communes, révélations masquées |
| CA-12 — UI | Interfaces : UI clavier/petit écran/login retour/refus ancien lien | Guide/navigation | Pages ERP, Support, Atelier, aucun redirect loop SQLAdmin |
| CA-13 — SUR, PG | Identité + orchestration : A capacité inconnue refusée ; P retrait avant worker/rejeu | Registre explicite et refus des entrées inconnues | Reçu existant, compte service et principal humain distincts |
| CA-14 — SUR, UI | Interfaces + identité : A accès direct sans session, API, pièce/export/PWA refusés | Guards et caches | Cache chaud puis logout ; aucune donnée hors écran |
| CA-15 — SUR, MET, UI | Atelier/Support : A L lit mais ne génère pas d'IA, coffret, réponse ou mail | Commandes séparées des GET | Espion fournisseur ; facture absente ne déclenche pas rendu |
| CA-16 — PG, UI | Sessions : P/UI utilisateur désactivé sur ERP et PWA ouverte, tâche différée | Session/revalidation | Requête suivante refusée ; vieux contenu retiré à réception refus |
| CA-17 — HTTP | Auth historique : A panne référentiel interne, accès configuré encore utilisable si registre historique disponible | Guide reprise | Panne comptes métier distincte de panne DB générale |
| CA-18 — ID, DOC | Audit : A chaque commande/refus tracés sans token/hash/password ; UI guide accessible à l'admin via bundle | Guide et lecteur documentaire | Tests du manifeste, absence de secret dans logs/emailpreview |
| CA-19 — FIN, UI | Finance : A/UI consultation/export et tickets/notes financiers Support | **E69-ARB-05 option A retenue** ; rattachement et projection Support dédiés | Paiement avec/sans instance, ticket financier autorisé et ticket général refusé ; état bancaire inchangé |
| CA-20 — SUR, MET, UI | Finance + identité : A/P commandes d'argent réservées refusées à B/F/B+F ; exceptions ARB-06 autorisées à B dans son périmètre | Capacité `finance.executer` distincte des trois capacités métier | Tous alias, reprise, idempotence ; F seul refusé aux exceptions |
| CA-21 — ID, FIN, UI | Identité : D/P union B+F par capacité, scopes indépendants | Attribution par rôle | B commune A, F commune B ; aucune propagation croisée |
| CA-22 — PG, FIN, UI | Identité : P/UI retrait F, B continue, export spécialisé et vieux lien refusés | Version d'autorisation | Tâche différée et résultat de commande historique |
| CA-23 — ID, PG | Identité + outbox : P création/invitation unique, doublon email et retry ; A refus non-admin | POST utilisateur et reçu | Course même email, commit échoue, transport arrêté |
| CA-24 — ID, HTTP, UI | Identité : D/P validité/politique password, ouverture non consommatrice, validation atomique ; UI première connexion | Formulaire, email HTML/texte | Compte attente sans session métier ; mot de passe mal confirmé |
| CA-25 — ID, PG | Identité : D/P liens expirés/falsifiés/remplacés/autre finalité, double activation | Erreurs génériques/token ERP | Horloge fixée, frontières expiration, jeton Animation |
| CA-26 — PG, TRANSPORT | Identité + communication : P génération renouvelée, suivi inconnu/échec, pas de doublon logique | Outbox et guide de renvoi | Fournisseur accepte puis timeout ; précédent email reçu tard |
| CA-27 — PG, TRANSPORT | Identité : P changement email/état/rôle contre activation ou transport | Versions et annulation | Ancien lien impossible, envoi engagé distingué d'envoi en attente |

Compléments de preuve V1.1, rattachés aux critères existants :

| Critères | Scénario supplémentaire | Résultat attendu |
| --- | --- | --- |
| CA-01/07/23 | DTO contenant rôle ADMIN, scope null/liste vide, rôle dupliqué ou état injecté dans PATCH | Rejet sans mutation ; aucun GLOBAL implicite ni faux compte historique |
| CA-02/04/21 | B commune A et F commune B ; ressource financière A+B, création, déplacement ou rattachement vers B | Union autorisée seulement pour une même capacité et couverture complète selon le contrat métier ; gestion catalogue B refusée ; contrôle source et cible |
| CA-10/19/22 | Retrait F d'un compte B+F puis demande d'export spécialisé avec ancien paramètre/projection | Export Finance refusé ; export métier B limité à ses colonnes et communes, pas de colonnes cachées envoyées |
| CA-06/12/16 | Connexion historique puis nominative dans un autre onglet ; contexte/monitor/PWA anciens | Principal courant cohérent, admin sans UUID métier fictif, droits recalculés, pas de boucle SQLAdmin |
| CA-08/16 | Modifier attribution puis consulter sans nouveau login ; révoquer les sessions ensuite | Première étape conserve session mais change capacités ; seconde invalide la session ; versions non interchangeables |
| CA-02/11/14 | Finance appelle directement contexte ERP et référentiels | Aucune liste catalogue complète, données limitées à la tâche financière autorisée |
| CA-24/25/27 | Modifier fragment/route de reset en initialisation, annuler invitation d'un autre compte, renvoyer reset | Refus de finalité/cible invalide ; renvoi légitime par route reset, une seule génération utilisable |
| CA-08/23/26 | Activité du monitor et mise à jour d'envoi pendant édition admin | Pas de conflit artificiel de version ; mutation admin concurrente réelle reste détectée |

## Scénarios techniques de référence

Compléments V1.2 des critères existants :

- CA-04/20/21 : B autorisé sur BUM VALIDER/SUSPENDRE avec conditions de domaine,
  activation déjà à zéro et annulation impayée non active ; L/F refusés, B hors
  territoire refusé même si F couvre ce territoire dans un cumul B+F.
- CA-04/20 : prix positif, commande payée ou active, version obsolète et absence
  de confirmation restent refusés ; aucun remboursement, remise ou annulation
  de facture implicitement autorisé par les trois ouvertures.
- CA-19 : création, modification et relecture d'un ticket et de ses notes sans instance,
  migration préservant les anciens tickets, notes internes bornées, responsable éligible et faux rattachement refusé ; aucun
  ticket général exposé par simple modification d'un type envoyé par le client.
- CA-24/25/26 : lien INITIALISATION valide avant 24 h et expiré à l'échéance ;
  renvoi crée une nouvelle génération ; reset déclenché uniquement par l'admin.

1. Tests de domaine sans ORM pour états, cumul, scope, finalité de jeton et
   autorisation ; cas frontière et refus inclus.
2. Tests applicatifs : HTTP/CSRF, identité stable, réponses masquées, projections
   et contrats, effet externe absent en refus. Tester aussi le hook d'autorisation
   avant récupération d'un reçu de commande existant.
3. PostgreSQL jetable : contraintes, ordre des verrous, deux connexions concurrentes,
   révocation vs login vs commande, double consommation, outbox et audit atomiques.
   Une simulation séquentielle seule ne prouve pas ces courses.
4. Tests consommateurs ERP/JS/monitor/PWA : capacités, liens, erreurs JSON/HTML,
   expiration et ancienne version frontend ; inventaire des routes sans garde.
5. Recette par attribution, y compris B+F et deux scopes différents. Admin historique
   peut reprendre l'exploitation sans compte nominatif, sans exception anonyme.

## Preuves exécutées

Les lots se recouvrent : **ne pas additionner les résultats** pour annoncer un
total unique. PostgreSQL a été utilisé sur une instance locale jetable avec
schémas isolés ; aucun test n’a utilisé une base distante ou un fournisseur réel.

| Groupe | Preuves et comportement ciblé | Résultat local |
| --- | --- | --- |
| ID | [Domaine](../../../../localeo-backend/tests/domain/identite_acces/test_acces_interne_dedicated.py), [application comptes](../../../../localeo-backend/tests/application/test_comptes_internes.py), API et régressions communication/session : rôles, scopes, états, tokens, idempotence | Lot cœur **85 réussis**, recouvrant HTTP/TRANSPORT |
| HTTP | [API comptes](../../../../localeo-backend/tests/api/test_comptes_internes_api.py), [transition des principaux](../../../../localeo-backend/tests/security/test_transition_principaux_internes.py) : CSRF, endpoints publics, reprise historique | Rerun API **10 réussis**, déjà inclus dans le cœur |
| PG | [Concurrence comptes](../../../../localeo-backend/tests/integration/test_comptes_internes_postgres.py) : même email, double consommation, login/révocation, retrait rôle/rejeu, renvoi/activation, transport/désactivation | **6 réussis**, connexions PostgreSQL concurrentes |
| TRANSPORT | [Courses transport](../../../../localeo-backend/tests/integration/test_e69_transport_interne.py), suites comptes/exploitation : crash après acceptation possible, synchronisation après activation | Lot **52 réussis**, dont **2 nouveaux tests PostgreSQL** ; pas de reprise aveugle ni réécriture du corps purgé |
| SUR | [Surfaces internes](../../../../localeo-backend/tests/security/test_acces_internes_surfaces.py) : SQLAdmin/Ops/Control/Audit fermés aux nominatifs, Finance sans catalogue, méthodes/routes inconnues refusées | Lot d’intégration **127 réussis, 0 ignoré**, puis lot gardes/documentation/OpenAPI **35 réussis** ; registre des routes vérifié, sans prétendre couvrir tout comportement historique |
| MET | [Effets OnBoard](../../../../localeo-backend/tests/api/test_e69_onboard_effects.py), contrats OnBoard, [portées](../../../../localeo-backend/tests/integration/test_e69_perimetre_onboard.py), [délégation Animation](../../../../localeo-backend/tests/application/test_e69_delegation_animation.py) | API/contrats **26 réussis**, dont **6 nouveaux scénarios** ; premier lot PG portées/délégation **4 réussis**, repris avec compléments activité/projections dans le lot **127 réussis** |
| FIN | [API Finance](../../../../localeo-backend/tests/api/test_e69_finance.py), [projections/persistance](../../../../localeo-backend/tests/infrastructure/persistence/test_e69_finance.py), [migration Support](../../../../localeo-backend/tests/infrastructure/persistence/test_e69_support_migration.py) et E65/vision360 | Lots recouvrants **68**, **20**, puis **12 réussis** ; complément recherche/chronologie **16 réussis**. Dernier rerun GED **12 réussis** : propriétaire, famille, rattachements et cohérence source/destinataire |
| UI | [Accès internes](../../../../localeo-backend/tests/browser/epic69-acces-internes.cjs), [suivi financier](../../../../localeo-backend/tests/browser/epic69-suivi-financier.cjs), [OnBoard](../../../../localeo-backend/tests/browser/epic69-onboard.cjs) | Node/Playwright réussis : capacités, B+F, initialisation sans login automatique, CSRF, Lecteur sans mutation, purge et réponses tardives |
| DEMO | [Unitaires](../../../../localeo-backend/tests/unit/test_demo_comptes_internes.py), [génération/restauration PG](../../../../localeo-backend/tests/integration/test_demo_comptes_internes.py) | **2 unitaires + 4 PostgreSQL réussis** ; générateur complet et restauration neutralisée |
| DOC | Trois présents documents, guide canonique et manifeste d’export | **91 guides, 992 liens, 0 erreur, 0 avertissement** pour les trois docs ; export/bundle **119 documents** contrôlés localement |

Régressions navigateur réussies : [Audit E65](../../../../localeo-backend/tests/browser/epic65-audit-erp.cjs),
[Finance E65](../../../../localeo-backend/tests/browser/epic65-finance-erp.cjs),
[accès commerçant](../../../../localeo-backend/tests/browser/acces-commercant-erp.cjs),
[Atelier](../../../../localeo-backend/tests/browser/atelier-assiste-erp.cjs) et
[adresse ERP/OnBoard](../../../../localeo-backend/tests/browser/adresse-commercant-erp-onboard.cjs)
(création/édition et préservation, CSRF, largeurs 390 et 1280 px).

Le lot final de **35 réussis** inclut les surfaces internes, les lecteurs documentaires,
le générateur OpenAPI et sa protection : nouvelles routes explicitement classifiées,
route inconnue refusée et retrait Backoffice contrôlé avant relecture d’un reçu.

Suite d’architecture obligatoire : **445 réussis**, tests/architecture,
test_domain_dedicated_classes et test_use_case_business_test_coverage.

Compléments finaux : [projection checklist OnBoard](../../../../localeo-backend/tests/integration/test_e69_checklist_projection.py)
et progression existante, **6 réussis**, puis **2 PostgreSQL réussis** après contrôle
des aptitudes ERP. Aucune réécriture des snapshots globaux pendant les lectures.
Les titres de documents masqués, anciens blocages et taux historiques ne ressortent
plus dans les listes, récapitulatifs ou indicateurs nominatifs. Les indicateurs et
le filtre de blocage recalculent chaque dossier du périmètre visible ; cette voie
demande une mesure de charge en cible. La liste ordinaire reste paginée en SQL.

Deux contrôles documentaires métier supplémentaires réussis : refus des pièces
non autorisées et masquage des détails techniques antivirus/lisibilité. Le test
navigateur des accès internes a été rejoué avec le lien convention métier autorisé
et son équivalent SQLAdmin refusé. Instance PostgreSQL locale jetable arrêtée après
les validations ; aucune base distante utilisée.

Contrôle intégré des guides, des sources E69 et des index : **96 guides, 1 177 liens,
0 erreur, 0 avertissement**. Les lots de contrôles se recouvrent ; ne pas les additionner.
Syntaxe JS et contrôle des différences sans erreur. Des routes simulées dans
Playwright prouvent l’interface, pas la remise email ou l’installation PWA réelle.

### Constats de revue intégrés

- Autorisation avant rejeu idempotent et dans la transaction du métier ; aucun
  principal nominatif transformé en admin, aucune union des scopes entre capacités différentes.
- OnBoard conserve l’ordre d’autorisation pendant ses effets. Certains services
  historiques ont une transaction autonome : une pièce déjà créée ne peut pas
  être annoncée annulée si le diagnostic suivant échoue.
- Support financier : propriétaire unique, notes cloisonnées, responsable actif
  couvrant toute la source, sans modification bancaire par résolution de ticket.
- GED : facture PDF déjà publiée, exclusivement rattachée à la facture courante
  avec source/destinataire cohérents ; refus KYC, parent nul ou rattachement étranger.
- Transport incertain : pas de renvoi automatique aveugle ; consommation/annulation
  non contredite par une réponse tardive du fournisseur.

### Dette prouvée et recette restante

- Régression unitaires démonstration : **139 réussis, 7 échecs** dans
  test_demo_animation_deadlines. La fixture SimpleNamespace n’a pas de session,
  alors que animation_history utilise session.execute. Cet appel a été retrouvé
  dans le générateur de **HEAD** par git show HEAD:scripts/demonstration/generator.py,
  recherche de self.session.execute(insert(m.CoordinationAnimationOrm) ; E69 n’y
  ajoute que son appel de seed interne.
  Dette préexistante conservée, sans skip ni correction hors périmètre.
- Pas de tâche périodique universelle purgeant les corps d’invitations déjà
  envoyées, seulement expirées et jamais consommées ni annulées. Consommation,
  annulation et invalidité avant transport sont neutralisées, mais ne prouvent
  pas une politique de rétention entièrement automatisée.
- Recette cible non exécutée : remise email, environnement du lien, proxy/cookies
  HTTPS, appareil/PWA, permissions effectives, bascule et reprise historique.
- Les preuves ciblées ne certifient pas toutes les variantes des 27 critères,
  tous les alias historiques ou toutes les courses possibles. Les tableaux
  de référence restent la grille de revue et de recette avant ouverture réelle.

## Démonstration et restauration

Le générateur crée via domaine/ports huit comptes : L, B, F, B+F actifs ; attente ;
invitation expirée ; désactivé ; échec d’envoi. Le cumul a deux communes distinctes.
Contacts de type gestionnaire, sans fusion avec Animation : Mathilde/Émilie et
leurs droits sont conservés. Les secrets restent dans les artefacts privés.
Le registre comprend les cinq tables de comptes internes et les notes financières.
Aucun email réel, session ou invitation utilisable n’est créé ; seule une trace
historique d’échec neutralisée illustre le défaut de remise.

La restauration vérifie l’empreinte originale de sauvegarde avant transformation,
puis une empreinte distincte de l’état neutralisé : sessions révoquées, liens
annulés, outbox désarmée, anciens hash de mot de passe effacés, versions incrémentées.
ACTIF revient à EN_ATTENTE_INITIALISATION ; DESACTIVE reste DESACTIVE. Emails,
identités et rôles sont conservés ; initialized_at reste historique, sans valeur
d’autorisation. Nouvelle invitation admin nécessaire, ancien mot de passe invalide.
Le reçu distingue l’empreinte originale et l’empreinte de restauration sécurisée.

## Migrations, configuration et livraison ordonnées

1. Préparer sauvegarde et inventaire des accès réellement déployés sans extraire
   de secret ; contrôler l’admin historique et son registre indépendant.
2. Appliquer [v251 comptes](../../../../localeo-backend/sql/v251_comptes_internes.sql)
   puis [v252 Support](../../../../localeo-backend/sql/v252_support_financier.sql).
   Preuves PostgreSQL locales, aucune application distante dans cette phase.
   Aucun compte admin converti ni invitation envoyée par migration.
3. Vérifier LOCALEO_ERP_URL (origine HTTPS), transport mail et limites configurées :
   LOCALEO_INTERNE_INVITATION_INTERVAL_SECONDS (60 défaut),
   LOCALEO_INTERNE_INVITATION_MAX_PER_DAY (5 défaut). Invitations 24 h, sessions
   15 min d’inactivité/8 h absolues ; limites login et mot de passe existantes,
   bcrypt borné en octets. Contrôler leurs valeurs effectives en cible.
4. Livrer backend, contrats et JS ERP/Support/Atelier/OnBoard ensemble. Garder les
   nouveaux comptes fermés avant vérification des projections/refus ; une ancienne
   session EXPLOITATION ne devient pas un compte nominatif.
5. Préparer le bundle documentaire avec empreintes et vérifier sa lecture ERP.
   Créer un pilote autorisé ; recette invitation, rôles, B+F sur deux communes,
   retrait/révocation et SQLAdmin. Ces actions distantes restent à exécuter.

Retour arrière : fermer l’entrée nominative, révoquer liens/sessions, conserver
les données additives et reprendre par l’admin. Ne pas utiliser un artefact
interprétant un cookie nominatif comme admin, ni restaurer d’anciens secrets actifs.

## Guide backoffice

Source : [guide-backoffice.md](guide-backoffice.md). L’alias d’export
**docs/ops/formation/gerer-utilisateurs-internes.md** est ajouté au manifeste pour
le lecteur **/internal/docs/knowledge/formation/gerer-utilisateurs-internes.md**.
Gestion et guide réservés à l’admin historique. Un bundle temporaire réel de
119 documents a été construit, ses empreintes recontrôlées et la résolution du
guide par le lecteur ERP vérifiée en V1.3, puis le temporaire nettoyé. Cela ne
constitue pas une publication distante ; refaire le contrôle sur le bundle livré.

Le contrat OpenAPI complet canonique E41 a été régénéré hors ligne : **673 chemins**.
Il contient les routes publiques et internes, sans annoncer qu’un serveur partagé
expose déjà ce contrat. Le contrôle des sources exportées a réussi sur **119 documents**.

## Bilan d’acceptation

Dépôts modifiés : backend (domaine, application, adaptateurs, ERP et satellites
embarqués, SQL, générateur, tests) et projet (spécifications, contrats, guide).
Aucun nouveau rôle interne dans les applications publiques Animation, Commerçant
ou Marketplace ; leurs populations d’authentification restent distinctes.
Les décisions V1.2 sont appliquées : récupération administrée, Finance via Support,
et trois commandes métier ouvertes à Backoffice dans son périmètre.
**L’EPIC reste en cours ; aucune clôture ni livraison distante n’est annoncée.**
