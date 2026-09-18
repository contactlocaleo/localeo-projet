# Plan de tests et livraison - Epic 60

> Historique de conception. Etat realise et decisions deleguees : [rapport V1](rapport-developpement-v1.md), [specification detaillee](specifications-fonctionnelles.md), [contrats implementes](contrats-api.md).

> Ce document couvre PRD-561 a PRD-570, volet diagnostic de l'epic fusionnee.
> Le [plan unifie](plan-livraison-unifie.md) le complete pour les ateliers ERP
> et la recette d'integration PRD-571 a PRD-582.

> Statut : scenarios de conception, non executes comme tests d'une implementation.

## 1. Matrice de tracabilite

| Story | Preuves attendues | Lot |
| --- | --- | --- |
| PRD-561 | Partition des trois verdicts, memes filtres, projection absente/perimee, KPI hors pagination, instant commun | C2 |
| PRD-562 | Defaut NON_VENDABLE, tous les filtres combines, tri stable et dernieres pages ; commercant partage sans doublon | C2-C3 |
| PRD-563 | Chaque code, controles independants cumules, UNKNOWN prioritaire, succes et non-applicabilite distingues | C0-C3 |
| PRD-564 | Catalogue code/libelle/cible complet ; chaque lien rendu atteint une route reelle autorisee ou fournit une consigne | C3 |
| PRD-565 | Transitions, empreinte stable, rechute identique, changement des causes, resolution et deux interfaces | C1-C4 |
| PRD-566 | Reevaluation sans mutation des sources, audit, replay, concurrence, nouvelle cle apres correction | C1-C2 |
| PRD-567 | Initialisation, ordre et curseur, dates de detection preservees, aucun faux changement sur reevaluation identique | C1-C5 |
| PRD-568 | Commune publiee sans coffret, sans vendable, avec indetermines, non publiee, filtre type et droits | C2-C5 |
| PRD-569 | Session/roles/perimetres, acces direct et indirect, CSRF, audit fiable, non-divulgation et no-store | C2-C5 |
| PRD-570 | Parite domaine/SQL/liste/detail/paiement, combinaisons des flags et erreurs de source | C0-C5 |

## 2. Tests de domaine sans infrastructure

Creer des fichiers par classe sous `tests/domain/commercialisation/` selon
l'organisation du depot. Horloge et faits explicites, aucun UnitOfWork ni ORM.

- Cas nominal ; chacun des codes du referentiel en isolation ; cause unique
  lorsque plusieurs prestations partagent un commercant bloque.
- Produit cartesien des axes structurants : statut coffret, presence de
  prestations actives, marchand actif/absent, capacites Stripe, politique et
  qualification BUM, publication territoriale. Ajouter tests generatifs si
  l'outillage existant le permet, sans nouvelle dependance obligatoire.
- Cas historique `VALIDATED + AUTO_ELIGIBLE + promesse absente` : jamais
  vendable avec la garde BUM active.
- Plusieurs echecs BUM et Stripe simultanes : tous les echecs independants
  apparaissent, sans inventer un resultat de controle dependant impossible.
- Prix nul/negatif, promesse contenant uniquement espaces, zero prestation,
  uniquement prestations inactives, commercant inactif sur prestation inactive.
- Flags BUM/Stripe on/off : aucune validation fictive des controles desactives.
- UNKNOWN obligatoire + FAILED = INDETERMINE ; controle non applicable
  UNKNOWN ne bloque pas ; avertissement seul conserve VENDABLE.
- Permutation des faits et changement de libelle/date : hash inchange ;
  changement de code, ressource, verdict ou version : hash change.
- Meme cause persistante conserve detectedAt ; disparition/reapparition le
  renouvelle ; reinitialisation du debut d'episode uniquement apres resolution.
- Toutes les transitions du tableau de conception, dont VENDABLE ->
  INDETERMINE -> NON_VENDABLE et NON_VENDABLE initial sans fausse perte de vente.

## 3. Application et PostgreSQL

Une classe `Test<UseCase>` pour chaque use case public avec `execute`.
Fakes UoW pour les scenarios metier ; PostgreSQL jetable pour les garanties
transactionnelles, contraintes, curseurs et plans de requete.

| Scenario | Resultat observable |
| --- | --- |
| Mutation source rollback | Aucune demande durable, projection et alertes inchangees |
| Sauvegarde SQLAdmin, API ou synchronisation Stripe | Tous les coffrets lies invalides dans la transaction ; anciens/nouveaux rattachements couverts |
| Politique globale changee au milieu d'un fan-out | Toutes les anciennes revisions sont deja perimees ; curseur de reprise durable |
| Deux premieres evaluations concurrentes | Une seule projection, aucune double transition ou alerte |
| Evenement ancien traite apres evenement recent | Il ne remplace jamais un verdict issu de sources plus recentes |
| Worker lent dont le claim expire | Le nouveau worker publie ; l'ancien ne peut ni publier ni accuser la nouvelle generation |
| Crash avant commit | Aucun effet partiel |
| Crash apres commit avant ack | Replay sans doublon de changement ou outbox |
| Source modifiee pendant calcul | Resultat ancien rejete, nouvelle generation toujours en attente |
| BUM absent / exception de lecture | Echec metier certain distingue de l'indetermination technique |
| Base inaccessible | Pas de faux succes persistant ; signal de supervision externe aux projections |
| Reevaluation identique repetee | evaluatedAt avance ; changedAt, detectedAt et nombre d'alertes restent stables |
| Expiration naturelle | KPI indetermine immediatement a l'expiration ; alerte lors du passage du batch |
| Reconciliation d'une mutation SQL sans evenement | Ecart detecte et projection corrigee au tour complet |
| Reevaluation manuelle avec replay | Une action effective, meme reponse initiale ; nouvelle cle permet la nouvelle evaluation |

Tester la migration a vide et sur base renseignee, reexecution par le runner,
rollback transactionnel en echec et contraintes d'unicite. Le backfill laisse
les donnees sources et les Checkout durables intacts. Aucune base de production
pour ces tests ; reutiliser l'option PostgreSQL de `scripts/validation/test_isolated.py`.

## 4. Parite et non-regression

Pour chaque fixture du referentiel, et chaque combinaison de flags :

1. Evaluer les faits par le domaine.
2. Appeler `GET /public/commercialisation/coffrets?ville_id=...` et verifier
   appartenance/exclusion, pas seulement le nombre total.
3. Appeler le detail public et verifier 200/404 ; incident technique = erreur
   explicite conforme au contrat, jamais exposition des raisons internes.
4. Initialiser un nouvel achat avec donnees valides et Stripe fake : un coffret
   refuse n'entraine ni Checkout ni effet financier ; un coffret vendable passe
   la garde catalogue, les autres regles d'achat restant testees separement.
5. Reevaluer puis consulter la Vision 360 : meme verdict pour les memes faits,
   flags et commune ; une projection stale est affichee comme telle.
6. Verifier les selections paginees utilisant le predicat SQL BUM, y compris
   exclusions avant LIMIT/OFFSET, total, pages pleines et derniere page.

Couvrir aussi coffrets du moment, recherche multi-scope et details de prestation
qui dependraient de la vendabilite. Aucun endpoint secondaire ne doit contourner
la nouvelle garde de publication de commune.

Reexecuter les regressions existantes, notamment :

- `tests/application/conformite_fiscale_bum/test_garde_bum.py` ;
- `tests/application/test_coffrets_eligibles_pagination.py` ;
- suites paiement durable/idempotence, protections des routes internes,
  redaction des erreurs et echappement des resumes BackOffice.

Lors du passage liste de dicts -> diagnostic structure, adapter les tests au
comportement observable et aux codes ; ne pas conserver de tests qui exigent
le retour premature au premier blocage.

## 5. API, habilitations et recette interface

- Anonyme, session expiree, role absent/inconnu, ADMIN et EXPLOITATION avec
  zero/une/deux communes ; UUID hors perimetre et changement de droits sur replay.
- Meme cloisonnement sur KPI, facettes, liste, detail, controle contextuel,
  chronologie, alertes, territoires et raccourcis Localeo Control.
- Host malforme, acces direct a une route de donnees, mauvais token CSRF,
  origine non autorisee, GET sur reevaluation : aucun contournement.
- Cle manquante/trop longue, cle reutilisee pour autre coffret, deux appels
  simultanes, limitation atomique, backoff et Retry-After.
- Aucun compte Stripe, email, telephone, details d'exigences ou stack dans
  payloads/erreurs/logs/outbox ; X-Actor-ID forge n'altere pas l'acteur audite.
- Filtres et bornes invalides = 422 ; tris stables ; total independant de page ;
  curseurs invalides rejetes ; controles du detail tous accessibles par pages.
- Nom et motif contenant balises HTML rendus comme texte ; liens sans URL
  externe arbitraire ; absence de cache offline des reponses internes.

Recette operateur : ouvrir la file depuis le dashboard, choisir commune et
cause, consulter le detail, suivre le traitement autorise, corriger sur
l'ecran proprietaire, revenir et reevaluer avec une nouvelle cle, constater
retour vendable et resolution dans les deux interfaces. Verifier historique,
retour aux filtres, navigation clavier, mobile Control et etats d'erreur.
Completer le cahier BackOffice et l'aide operationnelle lors de la livraison
des ecrans, sans les decrire aujourd'hui comme deja disponibles.

## 6. Performance et supervision

Volume de reference propose pour qualification, a confirmer : 10 000 coffrets,
100 communes, 5 000 commercants, 100 000 prestations et 1 million de changements.
Au moins un coffret a 1 000 prestations et un commercant partage par 1 000
coffrets. Distribution 60 % vendables, 30 % non vendables, 10 % indetermines.
Datasets synthetiques, pas de copie de donnees personnelles de production.

Executer selon la campagne Epic 59 : warmup puis 10 minutes a 10 lecteurs
concurrents, cache chaud et froid, pendant consommation de la file. Documenter
machine, PostgreSQL, version, volume, taux d'erreur et plans EXPLAIN ANALYZE.
Objectifs MVP : p95 liste <= 500 ms, detail pagine <= 800 ms. Mesurer aussi
synthese, filtre commercant, recherche nom et territoires sans offre.

Verifier le nombre borne de requetes par page/lot et zero appel reseau Stripe.
Mesurer duree d'un tour complet, delai mutation -> projection et retard des
alertes. Cibles proposees : p95 evenement < 2 minutes en charge nominale,
tour complet < 15 minutes ; depassement du seuil de fraicheur rend le retard
visible. Aucun SLO n'est considere atteint sur la seule base de cette conception.

## 7. Lots implementables et criteres de sortie

| Lot | Travail concret | Condition de sortie |
| --- | --- | --- |
| C0 | Faits/controles/domaine ; inventaire consommateurs ; catalogue de codes ; migration des gardes BUM/Stripe ; alignement public/paiement/SQL ; schemas API | Tests unitaires et parite verts ; effets des nouvelles exclusions qualifies |
| C1 | Migration additive, repos/UoW, generations/claims, hooks transactionnels, reevaluation, reconciliation et suivi | Tests PostgreSQL concurrence/crash verts ; backfill reprenable et mesurable |
| C2 | Sept routes, DTO, filtrage territorial, idempotence, audit et CSRF | Contrats TestClient/OpenAPI verts, cloisonnement des agregats et objets prouve |
| C3 | Vue liste/detail, liens profonds, integration dashboard et commercant | Recette traitement de bout en bout, liens reels et accessibilite |
| C4 | Occurrences d'alerte, integration Control, canaux optionnels via outbox | Rechute/dedup/resolution et absence de double envoi logique testees |
| C5 | Historique final, couverture, performance, supervision et guides | Matrice PRD-561..570 complete, seuils mesures, procedure d'exploitation livree |

L'historique et les regles d'alerte sont modelises/persistes des C1 ; C4/C5
livrent leurs interfaces et finissent la recette, sans reconstruire les
transitions perdues a posteriori.

## 8. Activation et retour arriere

Decision V1 : les etapes techniques ci-dessous se preparent en recette.
La bascule des interfaces est directe, sans ancienne interface maintenue en
parallele ; mettre a jour liens et traitements vers les nouvelles destinations.
Le [cadrage V1](cadrage-v1.md) prime sur toute interpretation de coexistence.


1. Relever les decisions du registre, versions deployees et flags BUM/Stripe.
   Inventorier les chemins de mutation et clients de l'ancien diagnostic.
2. Livrer schema additif et moteur en mode comparaison sans changer encore
   les reponses publiques ; activer les hooks de demandes durables.
3. Lancer le backfill sans notification de fausse perte historique. Quantifier
   ecarts entre ancien et nouveau moteur, notamment les gardes nouvellement
   introduites. Corriger les donnees sur leurs ecrans proprietaires.
4. Basculer tous les consommateurs publics et paiement vers la meme version
   canonique, puis ouvrir la Vision 360 apres couverture complete et recette.
   Tant que les moteurs divergent, presenter la vue comme previsualisation,
   sans pretendre garantir la parite de production.
5. Activer les alertes BackOffice/Control, verifier le tour complet et un
   scenario de perte/retablissement ; activer les canaux externes separement.
6. Conserver versions, rapports de tests et courbes dans le bilan de livraison.

Retour arriere : desactiver interfaces et notifications nouvelles si necessaire,
conserver schema/historique et gardes de securite deja livrees. Ne pas revenir
implicitement a une autorisation de vente plus permissive : toute regression
du moteur de vendabilite exige une decision explicite et une recette de parite.
Une panne de projection ne doit pas empecher un diagnostic canonique courant
de proteger le paiement. Ne jamais purger les demandes en attente pour masquer
un incident ; reprendre a partir des generations et curseurs persistants.
