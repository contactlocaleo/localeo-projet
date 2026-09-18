# Backlog Epic 25 - Couche de tests fonctionnels domaine et application

## Objectif

Mettre en place une couche de tests fonctionnels automatisee sur le domaine et la couche application Localeo.

Cette Epic couvre :

- les entites domaine ;
- les value objects ;
- les use cases applicatifs ;
- les services applicatifs ;
- les invariants metier transverses issus des specifications fonctionnelles, des Epics produit et de la documentation back-office.

Elle ne vise pas les tests d'interface back-office ni les tests bout-en-bout HTTP complets. Ces derniers restent couverts par le cahier de recette back-office et pourront faire l'objet d'une Epic dediee.

## Sources fonctionnelles

- [docs/specifications/fonctionnelle.md](../../produit/specification-fonctionnelle.md) : liste de reference des UC-01 a UC-31.
- [docs/roadmap/product-roadmap.md](../product-roadmap.md) : priorisation et rattachement aux Epics produit.
- `docs/roadmap/*/epic-*.md` : details des invariants par Epic, classes par etat.
- [docs/ops/exploitation/README.md](../../exploitation/exploitation/README.md) : catalogue des procédures métier et support.
- [docs/ops/recette/cahier-tests-backoffice.md](../../exploitation/recette/cahier-tests-backoffice.md) : cas de recette a traduire partiellement en tests application quand ils ne dependent pas de l'UI.
- [docs/specifications/technique.md](../../architecture/backend/specification-technique.md) : architecture en couches, transactions, outbox, tokens et providers.

## Plan detaille des tests

La liste exhaustive des tests a implementer est maintenue dans :

- [docs/roadmap/terminees/epic-25-tests-fonctionnels-domaine-application-backlog.md](epic-25-tests-fonctionnels-domaine-application-backlog.md)

Ce plan contient les identifiants de tests `DOM-VO-*`, `DOM-ENT-*`, `APP-SVC-*`, `APP-UC-*` et `APP-XCUT-*`, avec priorite, scenario, resultat attendu et statut.

## Perimetre MVP

- Creer un package `tests/`.
- Structurer les tests par couche : `tests/domain`, `tests/application/use_cases`, `tests/application/services`, `tests/infrastructure`.
- Tester les invariants des value objects.
- Tester les methodes metier portees par les entites.
- Tester les use cases critiques avec Unit of Work fake en memoire.
- Tester les services applicatifs sans provider externe reel.
- Couvrir les chemins nominaux, refus metier et effets de bord attendus.
- Introduire des builders/fixtures metier reutilisables.
- Ajouter une convention de nommage des tests et une matrice UC -> tests.

## Hors perimetre MVP

- Tester les routes FastAPI HTTP.
- Tester SQLAdmin et le rendu HTML back-office.
- Tester Stripe, Brevo ou tout provider externe en integration reelle.
- Introduire une base de donnees de test obligatoire.
- Refaire les use cases pour les rendre plus testables.
- Viser une couverture exhaustive de toutes les branches des anciennes Epics au premier lot.

## Principes de test

- Un test fonctionnel de domaine verifie une regle metier observable, pas une implementation interne.
- Un test de use case verifie les entrees, sorties, erreurs metier, changements d'etat et appels aux ports.
- Toute modification d'un use case, d'un service applicatif ou d'un objet du domaine doit creer ou mettre a jour le test associe dans la meme livraison.
- Toute modification de la couche infrastructure doit creer ou mettre a jour le test associe dans la meme livraison, avec fakes ou stubs pour les providers externes.
- Chaque use case applicatif public exposant `execute` doit avoir une classe `Test<UseCase>` dediee.
- Chaque classe publique de `app/domaine` doit avoir un fichier de test dedie, range par domaine fonctionnel et categorie.
- Les tests peuvent regrouper plusieurs classes d'un meme domaine fonctionnel lorsque le regroupement rend le scenario plus lisible.
- Chaque classe de test de use case doit couvrir au moins une regle metier ou un workflow observable du use case : entree invalide, erreur metier, transition d'etat, idempotence, appel de port ou effet applicatif attendu.
- Un test d'import, d'existence de classe ou de simple instanciation ne suffit pas comme couverture metier.
- Les fakes doivent etre explicites et lisibles, pas des mocks opaques partout.
- Les tests ne doivent pas dependre de l'ordre d'execution.
- Les tests ne doivent pas appeler les providers externes.
- Les donnees personnelles de test doivent etre fictives.
- Les tokens bruts utilises en test ne doivent jamais etre reutilisables hors test.

## Structure cible

```text
tests/
  domain/
    entities/
      test_coffret_instance.py
      test_email_sortant.py
      test_sms_sortant.py
      test_mouvement_reversement.py
      ...
    value_objects/
      test_email.py
      test_numero_telephone.py
      test_code_postal.py
      test_montant_euro_centimes.py
      ...
  application/
    fakes/
      fake_unit_of_work.py
      fake_repositories.py
      fake_gateways.py
  infrastructure/
    fakes/
      http.py
      stripe.py
      sqlalchemy.py
    email/
      test_service_envoi_email.py
    sms/
      test_service_envoi_sms.py
    paiement/
      test_paiement_gateway.py
    persistence/
      test_repositories_sqlalchemy_mocks.py
    builders/
      achats.py
      catalogue.py
      commercants.py
      coffrets.py
      support.py
      reversements.py
    services/
      test_service_session_commercant.py
      test_service_validation_prestation.py
      test_service_preparation_email.py
      ...
    use_cases/
      test_initialiser_paiement.py
      test_valider_paiement.py
      test_activer_coffret_instance_achat.py
      test_valider_prestation.py
      ...
  conftest.py
```

## Matrice fonctionnelle a couvrir

### Domaine catalogue

- `UC-01` Villes : creation de `Ville`, code postal valide/invalide, consultation introuvable.
- `UC-02` Types commercants/coffrets : creation des referentiels et marge minimale.
- `UC-03` Commercants : statut, contact, absence de donnees d'authentification dans les sorties applicatives.
- `UC-04` Profils publics commercants : statuts de publication, version, demande et verification.
- `UC-05` Coffrets/prestations : statut, prix, duree, prestations actives, rentabilite.
- `UC-06` Images : a couvrir surtout en tests API/infrastructure hors MVP domaine.

### Achat, paiement et activation

- `UC-07` Initialiser paiement : coffret existant, statut achetable, quantite, montant total, idempotence.
- `UC-08` Valider paiement Stripe : evenement deduplique, achat confirme, instances creees, outbox creees.
- `UC-09` Achat particulier : instances actives, QR/code/token, statuts prestations, notifications.
- `UC-10` Achat professionnel : instances en attente, management token hashe, email de commande.
- `UC-11` Consulter achat : token de gestion valide, achat introuvable, non-exposition des secrets.
- `UC-12` Gerer instance d'achat : appartenance a l'achat, cooldown email, activation en statut autorise.
- `UC-13` Consultation par token : expiration, revocation, cloisonnement particulier/professionnel.

### Espace commercant et validation terrain

- `UC-14` Authentifier commercant : login normalise, mot de passe invalide, verrouillage, session creee.
- `UC-15` Mot de passe et sessions : reset/init token, TTL, revocation, purge sessions.
- `UC-16` Profil/contact commercant : mise a jour encadree du telephone et informations de contact.
- `UC-17` Prestations/reversements cote commercant : filtrage par commercant et statuts.
- `UC-18` Validation terrain nominale : transaction ouverte, non expiree, prestation validee, mouvement cree.
- `UC-19` Mode secours : decision autorisee/refusee/a controler, audit et idempotence metier.

### Support, documents et relation client

- `UC-20` Messages de contact : motif actif, cible, reference facultative, reponse admin avec rappel du message initial.
- `UC-21` Documents/facturation : snapshot, demande de facturation, generation recu/factures.
- `UC-22` Timeline support : aggregation ordonnee des evenements achat/coffret/support.
- `UC-23` Remboursements : annulation, statut remboursement, reference externe, refus des etats incoherents.

### Feedbacks, activites, notifications et batchs

- `UC-24` Feedback post-prestation : eligibilite, unicite, moderation, anonymisation.
- `UC-25` Feed activite locale : anonymisation, statut publication, purge.
- `UC-26` Outbox email : reservation, envoi, echec temporaire/definitif, annulation.
- `UC-27` Outbox SMS : reservation, envoi, echec temporaire/definitif, annulation.
- `UC-28` Expiration/relances : instances expirees, prestations restantes, relances planifiees.
- `UC-28B` Batchs : execution, verrou, historique, reprise, endpoints internes non testes au MVP.

### Reversements et finance commercant

- `UC-29` Mouvements : creation apres validation, statut `A_REVERSER`, rattachement validation.
- `UC-30` Generation reversements : aggregation par commercant, lignes, transitions de statut.
- `UC-31` Paiement manuel : lot, export CSV, confirmation/echec, absence de double paiement.

## User Stories

1. `PRD-147` En tant que developpeur, je veux une structure `tests/` claire par couche afin d'identifier rapidement ou placer un test.
   - Statut : `Termine`
   - Resultat attendu : les dossiers `tests/domain`, `tests/application/use_cases`, `tests/application/services` existent.
   - Resultat attendu : les conventions sont documentees.

2. `PRD-148` En tant que developpeur, je veux tester les value objects afin de verrouiller les invariants de base.
   - Statut : `Termine`
   - Resultat attendu : `Email`, `NumeroTelephone`, `CodePostal`, `MontantEuroCentimes`, `QrToken`, `VersionCarteCommercant` et `Money` sont couverts.

3. `PRD-149` En tant que developpeur, je veux tester les entites domaine critiques afin de securiser les transitions metier.
   - Statut : `Termine`
   - Resultat attendu : `CoffretInstance`, `EmailSortant`, `SmsSortant`, `MouvementReversement` et `PaiementReversement` sont couverts en priorite.

4. `PRD-150` En tant que developpeur, je veux des fakes de repositories et Unit of Work afin de tester les use cases sans base de donnees.
   - Statut : `Termine`
   - Resultat attendu : un `FakeUnitOfWork` permet de simuler commit, rollback et repositories utiles.
   - Resultat attendu : les fakes restent simples, typables et lisibles.

5. `PRD-151` En tant que responsable produit, je veux une matrice UC -> tests afin de savoir quels parcours metier sont securises.
   - Statut : `Termine`
   - Resultat attendu : chaque UC de la specification fonctionnelle est rattache a au moins un test cible ou une justification hors perimetre.

6. `PRD-152` En tant que developpeur, je veux tester les use cases achat/paiement afin de reduire le risque de regression sur le revenu.
   - Statut : `Termine`
   - Resultat attendu : initialisation paiement, validation paiement, achat particulier et achat professionnel sont couverts.

7. `PRD-153` En tant que developpeur, je veux tester les use cases tokens/activation/consultation afin de securiser les parcours beneficiaires.
   - Statut : `Termine`
   - Resultat attendu : management token, activation token, consultation token, expiration et revocation sont couverts.

8. `PRD-154` En tant que developpeur, je veux tester les use cases commercants et validation terrain afin de securiser l'usage en boutique.
   - Statut : `Termine`
   - Resultat attendu : authentification, session, transaction de validation, validation prestation et mode secours sont couverts.

9. `PRD-155` En tant que support, je veux tester les use cases messages, timeline, documents et remboursements afin de fiabiliser le back-office d'exploitation.
   - Statut : `Termine`
   - Resultat attendu : creation/reponse message, timeline, documents achat et annulation/remboursement sont couverts.

10. `PRD-156` En tant qu'exploitant, je veux tester les services email/SMS/batchs afin de limiter les regressions d'exploitation.
    - Statut : `Termine`
    - Resultat attendu : reservation, transitions de statut, retry, echec et verrou batch sont couverts.
    - Resultat actuel : adaptateurs Brevo email/SMS couverts avec doubles HTTP ; batchs encore a couvrir.

11. `PRD-157` En tant que finance, je veux tester les use cases reversements afin de securiser les montants dus aux commercants.
    - Statut : `Termine`
    - Resultat attendu : mouvement, campagne Stripe, paiement reversement, webhook transfer et reprise/echec Stripe sont couverts.

12. `PRD-158` En tant que responsable qualite, je veux executer la suite de tests avec une commande stable afin de l'integrer a la CI.
    - Statut : `Termine`
    - Resultat attendu : `pytest` lance les tests fonctionnels domaine/application.
    - Resultat attendu : une commande cible permet de lancer uniquement les tests rapides.

## Implementation actuelle

- Socle `pytest.ini` ajoute avec `testpaths`, `python_files` et markers `domain`, `application`, `infrastructure`, `functional`, `slow`.
- Structure `tests/` creee avec sous-packages domaine, application, fakes et builders.
- Fakes ajoutes : `FakeRepository`, `FakeTypeCoffretRepository`, `FakeRateLimitAuthentificationRepository`, `FakeUnitOfWork`.
- Fakes infrastructure ajoutes : `FakeRequests`/`FakeResponse` pour Brevo, `FakeStripeCheckoutSessionApi`/`FakeStripeWebhook` pour Stripe, `FakeSqlAlchemySession` pour repositories.
- Builders ajoutes : catalogue, notifications, reversements.
- Tests value objects ajoutes pour `Email`, `NumeroTelephone`, `CodePostal`, `MontantEuroCentimes`, `QrToken`, `VersionCarteCommercant`, `Money`.
- Tests entites critiques ajoutes pour `CoffretInstance`, `EmailSortant`, `SmsSortant`, `MouvementReversement`, `PaiementReversement`.
- Tests services applicatifs ajoutes pour `ServiceMotDePasse`, `ServiceSessionCommercant`, `ServiceRateLimitAuthentification`.
- Tests use cases ajoutes pour `CreerVille`, `CreerTypeCommercant`, `CreerTypeCoffret`.
- Tests infrastructure ajoutes pour `ServiceEnvoiEmail`, `ServiceEnvoiSms`, `PaiementGateway`, `VilleRepositorySqlAlchemy`, `TypeCoffretRepositorySqlAlchemy`.

## Priorisation de mise en oeuvre

### Lot 1 - Socle tests

- `PRD-147`
- `PRD-148`
- `PRD-150`
- `PRD-158`

### Lot 2 - Domaine critique

- `PRD-149`
- `PRD-151`

### Lot 3 - Parcours revenu et tokens

- `PRD-152`
- `PRD-153`

### Lot 4 - Usage terrain et exploitation

- `PRD-154`
- `PRD-156`

### Lot 5 - Support, documents et finance

- `PRD-155`
- `PRD-157`

## Criteres d'acceptation MVP

- Le dossier `tests/` existe et suit la structure cible.
- Les value objects critiques sont testes.
- Les entites avec methodes metier sont testees.
- Les use cases critiques achat, paiement, activation, consultation, validation prestation et reversements ont au moins un test nominal et un test d'erreur metier.
- Les providers externes sont remplaces par fakes ou stubs.
- Les tests ne necessitent pas de base de donnees.
- Les tests se lancent avec `pytest`.
- La matrice UC -> tests est documentee.
- Aucun secret reel n'est utilise dans les tests.

## Risques

- Fakes trop complexes qui reproduisent une base de donnees incomplete.
- Tests trop proches de l'implementation au lieu des regles metier.
- Couverture insuffisante des cas d'erreur et transitions interdites.
- Dependances implicites au temps courant ou aux UUID aleatoires.
- Instabilite si les tests reposent sur des providers externes.

## Decisions a prendre avant implementation

- Nom exact des marqueurs pytest : `domain`, `application`, `functional`, `slow`.
- Niveau de granularite de la matrice UC -> tests.
- Seuil minimal de couverture a viser au premier lot, si un outil de coverage est ajoute.


## Plan détaillé des tests fonctionnels

Ce complément est réuni au backlog de l’EPIC. Ses états de préparation et de recette sont historiques ; l’état produit commun reste **Terminée**.

### Objectif du document

Ce document liste les tests fonctionnels a implementer pour couvrir :

- la couche domaine : entites, value objects, exceptions metier simples ;
- la couche application : use cases et services applicatifs ;
- les invariants issus des UC-01 a UC-31 de la specification fonctionnelle ;
- les controles metier identifies dans les Epics produit et la documentation back-office.

Les tests listes ici sont des tests automatises `pytest`, sans appel HTTP, sans SQLAdmin, sans base de donnees obligatoire et sans provider externe reel.

### Conventions

#### Identifiants

- `DOM-VO-*` : tests des value objects.
- `DOM-ENT-*` : tests des entites.
- `APP-SVC-*` : tests des services applicatifs.
- `APP-UC-*` : tests des use cases.
- `APP-XCUT-*` : tests transverses application.

#### Priorites

- `P0` : indispensable avant de considerer la couche de tests comme utile en protection go-live.
- `P1` : important pour couvrir les parcours metier principaux.
- `P2` : utile pour durcir la qualite et reduire les regressions secondaires.

#### Statuts

- `A implementer` : test non cree.
- `Hors MVP` : test volontairement hors premier lot.
- `A confirmer` : comportement a clarifier dans le code ou la specification avant test.

### Socle technique de tests

| ID | Priorite | Cible | Tests a implementer | Statut |
| --- | --- | --- | --- | --- |
| APP-XCUT-001 | P0 | Structure | Creer `tests/domain/<domaine>/entities`, `tests/domain/shared/value_objects`, `tests/application/use_cases`, `tests/application/services`, `tests/application/fakes`, `tests/application/builders`. | Termine |
| APP-XCUT-002 | P0 | Pytest | Ajouter `tests/conftest.py` avec fixtures UUID, dates fixes, donnees fictives. | A implementer |
| APP-XCUT-003 | P0 | Fakes | Implementer un `FakeUnitOfWork` avec `commit_called`, `rollback_called`, context manager et repositories injectables. | A implementer |
| APP-XCUT-004 | P0 | Fakes | Implementer un `FakeRepository` generique avec `ajouter`, `obtenir`, `mettre_a_jour`, `lister`. | A implementer |
| APP-XCUT-005 | P0 | Temps | Fournir une date fixe `now` pour eviter les tests instables. | A implementer |
| APP-XCUT-006 | P0 | Builders | Ajouter des builders catalogue, achat, coffret, commercant, support, reversement. | A implementer |
| APP-XCUT-007 | P1 | Providers | Ajouter fakes Stripe, email, SMS, QR, token, lien court si necessaire. | En cours |
| APP-XCUT-008 | P1 | Markers | Declarer les markers `domain`, `application`, `infrastructure`, `functional`, `slow`. | Termine |
| APP-XCUT-009 | P1 | Commandes | Documenter `pytest tests/domain`, `pytest tests/application`, `pytest -m "not slow"`. | A implementer |
| APP-XCUT-010 | P1 | Matrice | Creer une matrice UC -> fichiers de tests. | A implementer |

### Tests domaine - Value objects

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-VO-001 | P0 | `test_email.py` | Creer `Email` avec une adresse valide. | L'objet est cree et `str(email)` retourne la valeur. | Termine |
| DOM-VO-002 | P0 | `test_email.py` | Creer `Email` avec chaine vide. | `ValueError` est levee. | Termine |
| DOM-VO-003 | P0 | `test_email.py` | Creer `Email` sans `@`. | `ValueError` est levee. | Termine |
| DOM-VO-004 | P1 | `test_email.py` | Creer `Email` avec espaces ou casse mixte. | Comportement documente : accepte tel quel ou refuse selon code courant. | A confirmer |
| DOM-VO-005 | P0 | `test_numero_telephone.py` | Creer `NumeroTelephone` avec numero FR valide. | L'objet est cree. | Termine |
| DOM-VO-006 | P0 | `test_numero_telephone.py` | Creer `NumeroTelephone` avec numero formate avec espaces. | L'objet est cree si au moins 8 chiffres apres nettoyage. | Termine |
| DOM-VO-007 | P0 | `test_numero_telephone.py` | Creer `NumeroTelephone` trop court. | `ValueError` est levee. | Termine |
| DOM-VO-008 | P1 | `test_numero_telephone.py` | Creer `NumeroTelephone` avec valeur `None` ou vide. | `ValueError` est levee. | Termine |
| DOM-VO-009 | P0 | `test_code_postal.py` | Creer `CodePostal` valide. | L'objet est cree et `str(code)` retourne la valeur. | Termine |
| DOM-VO-010 | P0 | `test_code_postal.py` | Creer `CodePostal` vide. | `ValueError` est levee. | Termine |
| DOM-VO-011 | P0 | `test_code_postal.py` | Creer `CodePostal` de longueur inferieure a 4. | `ValueError` est levee. | Termine |
| DOM-VO-012 | P0 | `test_montant_euro_centimes.py` | Creer `MontantEuroCentimes` positif. | L'objet est cree, `int(montant)` retourne les centimes. | Termine |
| DOM-VO-013 | P0 | `test_montant_euro_centimes.py` | Creer `MontantEuroCentimes` a zero. | L'objet est cree. | Termine |
| DOM-VO-014 | P0 | `test_montant_euro_centimes.py` | Creer `MontantEuroCentimes` negatif. | `ValueError` est levee. | Termine |
| DOM-VO-015 | P1 | `test_qr_token.py` | Creer `QrToken` avec token suffisamment long. | L'objet est cree. | Termine |
| DOM-VO-016 | P1 | `test_qr_token.py` | Creer `QrToken` vide ou trop court. | `ValueError` est levee. | Termine |
| DOM-VO-017 | P1 | `test_version_carte_commercant.py` | Creer version 1. | L'objet est cree, `int(version)` retourne 1. | Termine |
| DOM-VO-018 | P1 | `test_version_carte_commercant.py` | Creer version 0 ou negative. | `ValueError` est levee. | Termine |
| DOM-VO-019 | P1 | `test_money.py` | Creer `Money.from_euros(12.34)`. | Les centimes sont arrondis correctement. | Termine |
| DOM-VO-020 | P1 | `test_money.py` | Creer `Money` negatif. | `ValueError` est levee. | Termine |
| DOM-VO-021 | P2 | `test_money.py` | Convertir `Money` en euros et chaine. | Format attendu documente. | Termine |

### Tests domaine - Entites

#### Catalogue

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-001 | P1 | `test_ville.py` | Instancier une `Ville` avec `CodePostal` valide. | Les champs sont conserves. | Termine |
| DOM-ENT-002 | P1 | `test_type_commercant.py` | Instancier `TypeCommercant`. | Identifiant et libelle conserves. | Termine |
| DOM-ENT-003 | P1 | `test_type_coffret_config.py` | Instancier `TypeCoffretConfig` avec marge. | Code, libelle et marge conserves. | Termine |
| DOM-ENT-004 | P1 | `test_commercant.py` | Instancier `Commercant` sans statut explicite. | Statut par defaut `BROUILLON`. | Termine |
| DOM-ENT-005 | P1 | `test_commercant.py` | Instancier `Commercant` avec email/telephone de contact. | Value objects conserves. | Termine |
| DOM-ENT-006 | P1 | `test_coffret.py` | Instancier `Coffret` sans statut explicite. | Statut par defaut `BROUILLON`. | Termine |
| DOM-ENT-007 | P1 | `test_prestation_coffret.py` | Instancier `PrestationCoffret` sans statut explicite. | Statut par defaut `BROUILLON`, `version_courante=1`. | Termine |

#### Achat et coffret instance

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-020 | P0 | `test_achat_coffret.py` | Instancier achat particulier par defaut. | `type_client=PARTICULIER`, `quantite=1`. | Termine |
| DOM-ENT-021 | P0 | `test_achat_coffret.py` | Instancier achat professionnel. | Champs entreprise/contact conserves. | Termine |
| DOM-ENT-022 | P0 | `test_coffret_instance.py` | Instance `ACTIVE` non expiree. | `est_consommable(now)` retourne `True`. | Termine |
| DOM-ENT-023 | P0 | `test_coffret_instance.py` | Instance `ACTIVE` expiree. | `est_consommable(now)` retourne `False`. | Termine |
| DOM-ENT-024 | P0 | `test_coffret_instance.py` | Instance `EN_ATTENTE_ACTIVATION`. | `est_en_cours()` retourne `True`, `est_consommable()` retourne `False`. | Termine |
| DOM-ENT-025 | P0 | `test_coffret_instance.py` | Instance `UTILISE`, `EXPIRE` ou `ANNULE`. | `est_en_cours()` retourne `False`. | Termine |
| DOM-ENT-026 | P1 | `test_statut_prestation_coffret_instance.py` | Instancier statut prestation d'instance. | Statut et version prestation conserves. | Termine |
| DOM-ENT-027 | P1 | `test_paiement.py` | Instancier paiement. | Payload et transaction provider conserves. | Termine |

#### Validation et mode secours

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-040 | P1 | `test_transaction_validation.py` | Instancier transaction `OPEN`. | Dates et statut conserves. | Termine |
| DOM-ENT-041 | P1 | `test_validation_prestation.py` | Instancier validation prestation. | Email client et references conserves. | Termine |
| DOM-ENT-042 | P1 | `test_validation_secours.py` | Instancier secours `AUTORISE`. | Canal, decision, audit fields conserves. | Termine |
| DOM-ENT-043 | P1 | `test_validation_secours.py` | Instancier secours `REFUSE`. | Aucun champ execution obligatoire non prevu. | Termine |

#### Auth commercant

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-060 | P1 | `test_session_commercant.py` | Instancier session active. | Scopes et dates conserves. | Termine |
| DOM-ENT-061 | P1 | `test_identifiant_commercant.py` | Instancier identifiant sans password hash. | Acces initialisable. | Termine |
| DOM-ENT-062 | P1 | `test_identifiant_commercant.py` | Instancier identifiant verrouille. | `locked_at` et raison conserves. | Termine |
| DOM-ENT-063 | P1 | `test_token_acces_commercant.py` | Instancier token initialisation/reset. | Type, hash, expiration conserves. | Termine |
| DOM-ENT-064 | P1 | `test_rate_limit_authentification.py` | Instancier compteur rate limit. | Window, attempts et blocked_until conserves. | Termine |

#### Support et exploitation

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-080 | P1 | `test_motif_contact.py` | Instancier motif actif consommateur. | Cible, ordre et actif conserves. | Termine |
| DOM-ENT-081 | P1 | `test_message_contact.py` | Instancier message contact anonyme. | Statuts lecture et traitement conserves. | Termine |
| DOM-ENT-082 | P1 | `test_message_contact.py` | Instancier reponse rattachee a parent. | Parent, thread et emetteur conserves. | Termine |
| DOM-ENT-083 | P1 | `test_lien_court.py` | Instancier lien court actif. | Token, expiration, compteur conserves. | Termine |
| DOM-ENT-084 | P1 | `test_evenement_audit.py` | Instancier evenement audit avec metadata. | Contexte request et ressource conserves. | Termine |

#### Notifications

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-100 | P0 | `test_email_sortant.py` | `marquer_en_cours` depuis `A_ENVOYER`. | Statut `EN_COURS_ENVOI`, tentative incrementee, dates mises a jour. | Termine |
| DOM-ENT-101 | P0 | `test_email_sortant.py` | `marquer_en_cours` depuis `ECHEC_TEMPORAIRE`. | Reservation acceptee, tentative incrementee. | Termine |
| DOM-ENT-102 | P0 | `test_email_sortant.py` | `marquer_en_cours` depuis `ENVOYE`. | `ValueError` est levee. | Termine |
| DOM-ENT-103 | P0 | `test_email_sortant.py` | `marquer_envoye`. | Statut `ENVOYE`, date envoi, provider id, erreur nettoyee. | Termine |
| DOM-ENT-104 | P1 | `test_email_sortant.py` | `marquer_echec_temporaire`. | Statut, erreur et prochaine date conserves. | Termine |
| DOM-ENT-105 | P1 | `test_email_sortant.py` | `marquer_echec_definitif`. | Statut definitif et erreur conserves. | Termine |
| DOM-ENT-106 | P1 | `test_email_sortant.py` | `annuler`. | Statut `ANNULE`. | Termine |
| DOM-ENT-107 | P1 | `test_email_sortant.py` | `enregistrer_verification_statut`. | Date de verification mise a jour. | Termine |
| DOM-ENT-110 | P0 | `test_sms_sortant.py` | Memes transitions que `EmailSortant`. | Resultats equivalents pour SMS. | Termine |

#### Reversements

| ID | Priorite | Fichier cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| DOM-ENT-120 | P0 | `test_mouvement_reversement.py` | `marquer_en_cours` depuis `A_REVERSER`. | Statut `EN_COURS_DE_REVERSEMENT`, reversement_id renseigne. | Termine |
| DOM-ENT-121 | P0 | `test_mouvement_reversement.py` | `marquer_en_cours` depuis statut non disponible. | `ValueError` est levee. | Termine |
| DOM-ENT-122 | P0 | `test_mouvement_reversement.py` | `marquer_reverse` depuis `EN_COURS_DE_REVERSEMENT`. | Statut `REVERSE`. | Termine |
| DOM-ENT-123 | P0 | `test_mouvement_reversement.py` | `marquer_reverse` depuis `A_REVERSER`. | `ValueError` est levee. | Termine |
| DOM-ENT-124 | P1 | `test_reversement.py` | Instancier reversement. | Montant, compte connecte Stripe, statut conserves. | Termine |
| DOM-ENT-125 | P1 | `test_ligne_reversement.py` | Instancier ligne. | Reversement, mouvement et montant conserves. | Termine |
| DOM-ENT-126 | P1 | `test_campagne_reversement_stripe.py` | Instancier campagne Stripe Connect. | Periode, statut, createur et references Stripe conserves. | A implementer |
| DOM-ENT-127 | P1 | `test_compte_connecte_stripe.py` | Instancier compte connecte Stripe eligible. | Identifiant Stripe, statut onboarding et capacites conserves. | A implementer |
| DOM-ENT-128 | P1 | `test_paiement_reversement.py` | Instancier paiement reversement. | Statut, montant et references Stripe conserves. | Termine |

### Tests services applicatifs

| ID | Priorite | Service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-SVC-001 | P0 | `ServiceSessionCommercant` | Creer une session avec scopes valides. | Token brut retourne, hash stocke, expiration calculee. | A implementer |
| APP-SVC-002 | P0 | `ServiceSessionCommercant` | Verifier session valide. | Session retournee, scopes acceptes. | A implementer |
| APP-SVC-003 | P0 | `ServiceSessionCommercant` | Verifier session expiree. | `SessionExpiree` levee. | A implementer |
| APP-SVC-004 | P0 | `ServiceSessionCommercant` | Verifier session revoquee. | `SessionInvalide` levee. | A implementer |
| APP-SVC-005 | P1 | `ServiceSessionCommercant` | Scope manquant. | `ScopeInsuffisant` levee. | A implementer |
| APP-SVC-010 | P0 | `ServiceMotDePasse` | Hasher et verifier mot de passe valide. | Verification positive. | A implementer |
| APP-SVC-011 | P0 | `ServiceMotDePasse` | Verifier mauvais mot de passe. | Verification negative. | A implementer |
| APP-SVC-012 | P0 | `ServiceMotDePasse` | Mot de passe trop court. | Refus metier. | A implementer |
| APP-SVC-020 | P0 | `ServiceRateLimitAuthentification` | Incrementer tentative dans fenetre active. | Compteur mis a jour. | A implementer |
| APP-SVC-021 | P0 | `ServiceRateLimitAuthentification` | Depasser seuil. | Blocage jusqu'a date attendue. | A implementer |
| APP-SVC-022 | P1 | `ServiceRateLimitAuthentification` | Nouvelle fenetre apres expiration. | Nouveau compteur cree. | A implementer |
| APP-SVC-030 | P0 | `ServiceValidationPrestation` | Valider transaction ouverte non expiree. | Validation creee, statut prestation mis a jour. | A implementer |
| APP-SVC-031 | P0 | `ServiceValidationPrestation` | Transaction expiree. | Refus metier. | A implementer |
| APP-SVC-032 | P0 | `ServiceValidationPrestation` | Prestation deja validee. | Refus metier ou idempotence documentee. | A confirmer |
| APP-SVC-040 | P0 | `ServicePreparationEmail` | Creer email sortant minimal. | Outbox `A_ENVOYER`. | A implementer |
| APP-SVC-041 | P1 | `ServicePreparationEmail` | Creer email avec piece jointe. | Piece jointe conservee. | A implementer |
| APP-SVC-042 | P1 | `ServicePreparationEmail` | Correlation/source. | Champs source renseignes. | A implementer |
| APP-SVC-050 | P0 | `ServicePreparationSms` | Creer SMS sortant minimal. | Outbox `A_ENVOYER`. | A implementer |
| APP-SVC-051 | P1 | `ServicePreparationSms` | Correlation/source. | Champs source renseignes. | A implementer |
| APP-SVC-060 | P1 | `ServiceVerificationCodeCoffretInstance` | Generer code de verification. | Code et date stockables. | A implementer |
| APP-SVC-061 | P1 | `ServiceVerificationCodeCoffretInstance` | Verifier code exact. | Verification positive. | A implementer |
| APP-SVC-062 | P1 | `ServiceVerificationCodeCoffretInstance` | Verifier code faux ou expire. | Verification negative/refus. | A implementer |
| APP-SVC-070 | P1 | `ServiceConsultationCoffretInstance` | Verifier consultation token valide. | Instance accessible. | A implementer |
| APP-SVC-071 | P1 | `ServiceConsultationCoffretInstance` | Token expire ou revoque. | Refus metier. | A implementer |
| APP-SVC-080 | P1 | `ServiceLiensCourts` | Creer lien court avec URL autorisee. | Token cree, URL cible conservee. | A implementer |
| APP-SVC-081 | P1 | `ServiceLiensCourts` | Resoudre lien actif. | Compteur incrementable, URL retournee. | A implementer |
| APP-SVC-082 | P1 | `ServiceLiensCourts` | Lien expire ou inactif. | Refus metier. | A implementer |
| APP-SVC-090 | P1 | `ServiceDocumentsAchat` | Demande de generation recu. | Document attendu cree ou planifie. | A implementer |
| APP-SVC-091 | P1 | `ServiceDocumentsAchat` | Achat introuvable. | `RessourceDomaineIntrouvable`. | A implementer |
| APP-SVC-100 | P1 | `ServiceFeedbackPrestation` | Creer feedback eligible. | Feedback accepte. | A implementer |
| APP-SVC-101 | P1 | `ServiceFeedbackPrestation` | Feedback deja existant. | Refus ou idempotence documentee. | A confirmer |
| APP-SVC-110 | P1 | `ServiceActivitesLocales` | Publier activite anonymisee. | Aucune donnee nominative exposee. | A implementer |
| APP-SVC-111 | P1 | `ServiceActivitesLocales` | Purger activites anciennes. | Nombre purge retourne. | A implementer |
| APP-SVC-120 | P0 | `BatchRunner` | Executer batch connu sans verrou concurrent. | Execution creee, statut succes. | A implementer |
| APP-SVC-121 | P0 | `BatchRunner` | Batch inconnu. | `RegleMetierViolee`. | A implementer |
| APP-SVC-122 | P0 | `BatchRunner` | Verrou deja pris. | Execution refusee ou ignoree selon comportement. | A implementer |
| APP-SVC-123 | P1 | `BatchRunner` | Exception pendant batch. | Execution en echec et erreur tracee. | A implementer |
| APP-SVC-130 | P1 | `GouvernanceCatalogue` | Coffret publiable avec commercants/prestations actifs. | Eligible. | A implementer |
| APP-SVC-131 | P1 | `GouvernanceCatalogue` | Coffret avec prestation inactive ou commercant suspendu. | Non eligible. | A implementer |

### Tests use cases par UC fonctionnel

#### UC-01 - Lister et consulter les villes

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-001 | P1 | `ListerVilles` | Lister villes sans filtre. | Toutes les villes retournees. | A implementer |
| APP-UC-002 | P1 | `ListerVilles` | Filtrer par debut de nom. | Seules les villes correspondantes sont retournees. | A implementer |
| APP-UC-003 | P1 | `ConsulterDetailVille` | Ville existante. | Detail retourne. | A implementer |
| APP-UC-004 | P1 | `ConsulterDetailVille` | Ville absente. | `RessourceDomaineIntrouvable`. | A implementer |

#### UC-02 - Types commercants et coffrets

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-010 | P1 | `ListerTypesCommercants` | Lister referentiel. | Libelles et ids retournes. | A implementer |
| APP-UC-011 | P1 | `ListerTypesCoffrets` | Lister referentiel. | Code, libelle, marge retournes. | A implementer |
| APP-UC-012 | P1 | `CreerTypeCommercant` | Creer type valide. | Type ajoute et commit. | A implementer |
| APP-UC-013 | P1 | `CreerTypeCoffret` | Creer type avec marge valide. | Type ajoute et commit. | A implementer |
| APP-UC-014 | P1 | `CreerTypeCoffret` | Marge invalide. | Refus metier. | A implementer |

#### UC-03 - Lister et consulter les commercants

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-020 | P1 | `ListerCommercants` | Lister sans filtre. | Commercants retournes. | A implementer |
| APP-UC-021 | P1 | `ListerCommercants` | Filtrer par ville. | Commercants de la ville retournes. | A implementer |
| APP-UC-022 | P1 | `ConsulterDetailCommercant` | Commercant existant. | Detail retourne sans donnees auth. | A implementer |
| APP-UC-023 | P1 | `ConsulterDetailCommercant` | Commercant absent. | `RessourceDomaineIntrouvable`. | A implementer |
| APP-UC-024 | P1 | `ReferencerCommercant` | Referencer commercant valide. | Commercant cree, identifiant si requis, commit. | A implementer |
| APP-UC-025 | P1 | `ReferencerCommercant` | Type commercant absent. | `TypeCommercantIntrouvable`. | A implementer |

#### UC-04 - Profils publics commercants

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-030 | P1 | `ServiceProfilsCommercants` | Creer profil manquant. | Profil non publie cree. | A implementer |
| APP-UC-031 | P1 | `ServiceProfilsCommercants` | Creer version brouillon. | Version `BROUILLON`, demande `BROUILLON`. | A implementer |
| APP-UC-032 | P1 | `ServiceProfilsCommercants` | Soumettre version complete. | Version `A_MODERER`, demande en relecture. | A implementer |
| APP-UC-033 | P1 | `ServiceProfilsCommercants` | Soumettre version incomplete. | Refus metier. | A implementer |
| APP-UC-034 | P1 | `ServiceProfilsCommercants` | Approuver version. | Version publiee, ancienne archivee. | A implementer |
| APP-UC-035 | P1 | `ServiceProfilsCommercants` | Refuser version. | Statut refuse, motif conserve. | A implementer |
| APP-UC-036 | P2 | `ServiceProfilsCommercants` | Masquer puis republier profil. | Statuts publication coherents. | A implementer |

#### UC-05 - Lister et consulter les coffrets

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-040 | P1 | `ListerCoffrets` | Lister coffrets actifs. | Coffrets eligibles retournes. | A implementer |
| APP-UC-041 | P1 | `ListerCoffrets` | Filtrer par ville/type. | Resultats filtres. | A implementer |
| APP-UC-042 | P1 | `ConsulterDetailCoffret` | Coffret existant. | Detail et prestations actives retournes. | A implementer |
| APP-UC-043 | P1 | `ConsulterDetailCoffret` | Coffret absent. | `RessourceDomaineIntrouvable`. | A implementer |
| APP-UC-044 | P1 | `AjouterPrestationAUnCoffret` | Ajouter prestation valide. | Prestation ajoutee, commit. | A implementer |
| APP-UC-045 | P1 | `AjouterPrestationAUnCoffret` | Coffret absent. | `CoffretIntrouvable`. | A implementer |
| APP-UC-046 | P1 | `ConsulterRentabiliteCoffret` | Reversements inferieurs a seuil marge. | Rentabilite positive. | A implementer |
| APP-UC-047 | P1 | `ConsulterRentabiliteCoffret` | Reversements trop eleves. | Alerte rentabilite. | A implementer |

#### UC-06 - Images et bibliotheque media

| ID | Priorite | Cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-050 | P2 | API/infrastructure | Upload image valide. | Hors MVP domaine/application. | Hors MVP |
| APP-UC-051 | P2 | API/infrastructure | SVG ou taille excessive. | Hors MVP domaine/application. | Hors MVP |

#### UC-07 - Initialiser un paiement

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-060 | P0 | `InitialiserPaiement` | Coffret actif, client particulier, quantite 1. | Achat `PAYMENT_PENDING`, montant calcule, checkout URL retournee. | A implementer |
| APP-UC-061 | P0 | `InitialiserPaiement` | Coffret actif, client pro, quantite > 1. | Achat pro avec quantite et contact entreprise. | A implementer |
| APP-UC-062 | P0 | `InitialiserPaiement` | Coffret absent. | `CoffretIntrouvable`. | A implementer |
| APP-UC-063 | P0 | `InitialiserPaiement` | Coffret non achetable. | `RegleMetierViolee`. | A implementer |
| APP-UC-064 | P0 | `InitialiserPaiement` | Quantite invalide. | Refus metier. | A implementer |
| APP-UC-065 | P1 | `CreerAchatEtInitialiserPaiement` | Idempotency key deja utilisee. | Achat existant ou comportement documente. | A confirmer |
| APP-UC-066 | P1 | `CreerAchatEtInitialiserPaiement` | Provider Stripe renvoie erreur. | Rollback et erreur metier/technique controlee. | A implementer |

#### UC-08, UC-09, UC-10 - Valider paiement, achat particulier, achat professionnel

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-070 | P0 | `ValiderPaiement` | Evenement Stripe valide pour achat particulier. | Achat confirme, paiement cree, 1 instance active, prestations creees, outbox creee. | A implementer |
| APP-UC-071 | P0 | `ValiderPaiement` | Evenement Stripe valide pour achat pro quantite N. | N instances en attente, management token cree, email commande cree. | A implementer |
| APP-UC-072 | P0 | `ValiderPaiement` | Evenement deja traite. | Pas de doublon paiement/instances/outbox. | A implementer |
| APP-UC-073 | P0 | `ValiderPaiement` | Achat absent. | `AchatCoffretIntrouvable`. | A implementer |
| APP-UC-074 | P0 | `ValiderPaiement` | Evenement non pertinent. | Aucun changement, commit selon comportement. | A implementer |
| APP-UC-075 | P0 | `ValiderPaiement` | Signature invalide. | `PaiementInvalide`. | A implementer |
| APP-UC-076 | P1 | `ValiderPaiement` | Generation documents echoue. | Comportement transactionnel documente. | A confirmer |
| APP-UC-077 | P1 | `RelancerReconciliationAchatNonConfirme` | Achat payable non confirme. | Reconciliation relancee. | A implementer |
| APP-UC-078 | P1 | `RelancerReconciliationAchatNonConfirme` | Achat deja confirme. | Refus metier. | A implementer |

#### UC-11 - Consulter un achat

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-080 | P0 | `ConsulterDetailAchatCoffret` | Achat existant avec token valide. | Detail achat retourne. | A implementer |
| APP-UC-081 | P0 | `ConsulterDetailAchatCoffret` | Achat absent. | `AchatCoffretIntrouvable`. | A implementer |
| APP-UC-082 | P0 | `ConsulterAchatDepuisSessionCheckout` | Session checkout valide. | Achat associe retourne. | A implementer |
| APP-UC-083 | P1 | `ListerCoffretInstancesAchat` | Achat avec instances. | Liste instances retournee. | A implementer |

#### UC-12 - Consulter et gerer une instance d'achat

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-090 | P0 | `ConsulterCoffretInstanceAchat` | Instance appartient a l'achat. | Detail retourne. | A implementer |
| APP-UC-091 | P0 | `ConsulterCoffretInstanceAchat` | Instance n'appartient pas a l'achat. | `RessourceDomaineIntrouvable` ou refus metier. | A implementer |
| APP-UC-092 | P0 | `ActiverCoffretInstanceAchat` | Instance en attente, token activation valide. | Instance activee, QR/code/token/prestations crees. | A implementer |
| APP-UC-093 | P0 | `ActiverCoffretInstanceAchat` | Instance deja active. | Refus metier ou idempotence documentee. | A confirmer |
| APP-UC-094 | P0 | `ActiverCoffretInstanceAchat` | Token activation expire/revoque. | Refus metier. | A implementer |
| APP-UC-095 | P1 | `EnvoyerLienActivationCoffretInstanceAchat` | Envoi autorise. | Email activation cree. | A implementer |
| APP-UC-096 | P1 | `EnvoyerLienActivationCoffretInstanceAchat` | Cooldown non ecoule. | Refus metier. | A implementer |
| APP-UC-097 | P1 | `RenvoyerEmailConfirmationCoffretInstance` | Instance active. | Email confirmation cree. | A implementer |

#### UC-13 - Consultation par token

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-100 | P0 | `VerifierConsultationTokenCoffretInstance` | Token valide. | Verification OK. | A implementer |
| APP-UC-101 | P0 | `VerifierConsultationTokenCoffretInstance` | Token expire. | `SessionExpiree`. | A implementer |
| APP-UC-102 | P0 | `VerifierConsultationTokenCoffretInstance` | Token revoque ou hash inconnu. | `SessionInvalide`. | A implementer |
| APP-UC-103 | P0 | `ConsulterDetailCoffretInstanceParToken` | Token particulier. | Detail instance et achat utile retournes. | A implementer |
| APP-UC-104 | P0 | `ConsulterDetailCoffretInstanceParToken` | Token professionnel. | Donnees globales achat masquees. | A implementer |
| APP-UC-105 | P1 | `ListerPrestationsCoffretInstanceParToken` | Token valide. | Prestations retournees. | A implementer |
| APP-UC-106 | P1 | `RegenererConsultationTokenCoffretInstance` | Instance active. | Ancien token revoque, nouveau token cree. | A implementer |
| APP-UC-107 | P1 | `RevoquerConsultationTokenCoffretInstance` | Token existant. | Token revoque. | A implementer |

#### UC-14, UC-15 - Authentification, mot de passe et sessions commercant

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-120 | P0 | `AuthentifierCommercantParMotDePasse` | Login/password valides, commercant actif. | Session creee, derniere connexion mise a jour. | A implementer |
| APP-UC-121 | P0 | `AuthentifierCommercantParMotDePasse` | Password invalide. | Tentative incrementee, `SessionInvalide`. | A implementer |
| APP-UC-122 | P0 | `AuthentifierCommercantParMotDePasse` | Trop d'echecs. | Compte verrouille. | A implementer |
| APP-UC-123 | P0 | `AuthentifierCommercantParMotDePasse` | Commercant suspendu/archive. | Refus session. | A implementer |
| APP-UC-124 | P0 | `VerifierSessionCommercant` | Session valide. | Commercant/session retournes. | A implementer |
| APP-UC-125 | P0 | `VerifierSessionCommercant` | Scope insuffisant. | `ScopeInsuffisant`. | A implementer |
| APP-UC-126 | P1 | `InitialiserSessionCommercant` | Token d'acces initialisation valide. | Session initialisee. | A implementer |
| APP-UC-127 | P1 | `InvaliderSessionCommercant` | Session existante. | Session revoquee. | A implementer |
| APP-UC-128 | P1 | `DemanderInitialisationAccesCommercant` | Commercant actif avec email unique. | Identifiant/token/email crees. | A implementer |
| APP-UC-129 | P1 | `DemanderInitialisationAccesCommercant` | Email deja utilise. | Refus metier, pas de doublon. | A implementer |
| APP-UC-130 | P1 | `DemanderReinitialisationMotDePasseCommercant` | Login existant. | Token reset/email crees. | A implementer |
| APP-UC-131 | P1 | `DemanderReinitialisationMotDePasseCommercant` | Rate limit reset depasse. | Refus metier. | A implementer |
| APP-UC-132 | P1 | `ReinitialiserMotDePasseCommercant` | Token reset valide. | Password hash mis a jour, token utilise. | A implementer |
| APP-UC-133 | P1 | `MettreAJourMotDePasseCommercant` | Session valide, ancien password correct. | Password mis a jour. | A implementer |
| APP-UC-134 | P1 | `PurgerSessionsCommercant` | Sessions expirees/revoquees anciennes. | Sessions purgees, compteur retourne. | A implementer |

#### UC-16, UC-17 - Profil/contact, prestations et dashboard commercant

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-140 | P1 | `ConsulterProfilCommercant` | Commercant existant. | Profil/contact retournes. | A implementer |
| APP-UC-141 | P1 | `MettreAJourContactCommercant` | Telephone valide. | Contact mis a jour, commit. | A implementer |
| APP-UC-142 | P1 | `MettreAJourContactCommercant` | Commercant absent. | `RessourceDomaineIntrouvable`. | A implementer |
| APP-UC-143 | P1 | `AfficherPrestationsCommercant` | Commercant actif. | Prestations filtrees retournees. | A implementer |
| APP-UC-144 | P1 | `AfficherMouvementsReversementAReverser` | Mouvements disponibles. | Montants retournes. | A implementer |
| APP-UC-145 | P1 | `AfficherReversementsEffectues` | Reversements executes. | Historique retourne. | A implementer |
| APP-UC-146 | P1 | `ConsulterDashboardOperationnelCommercant` | Donnees presentes. | KPI, encours, historique retournes. | A implementer |
| APP-UC-147 | P2 | `MettreAJourContenuPrestationCommercant` | Proposition valide. | Contenu modifie/propose selon regles. | A implementer |

#### UC-18 - Validation terrain nominale

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-160 | P0 | `OuvrirTransactionValidation` | QR valide, commercant autorise. | Transaction `OPEN` creee avec expiration. | A implementer |
| APP-UC-161 | P0 | `OuvrirTransactionValidation` | QR invalide. | `QRInvalide`. | A implementer |
| APP-UC-162 | P0 | `ValiderPrestation` | Transaction ouverte, prestation a valider. | Validation creee, statut `VALIDEE`, mouvement reversement cree. | A implementer |
| APP-UC-163 | P0 | `ValiderPrestation` | Transaction expiree. | `TransactionExpiree`. | A implementer |
| APP-UC-164 | P0 | `ValiderPrestation` | Transaction absente. | `TransactionIntrouvable`. | A implementer |
| APP-UC-165 | P0 | `ValiderPrestation` | Prestation absente ou non rattachee. | `PrestationIntrouvable` ou refus metier. | A implementer |
| APP-UC-166 | P1 | `ConsulterDetailQrToken` | QR valide. | Detail token retourne. | A implementer |
| APP-UC-167 | P1 | `ConsulterDetailQrCoffretInstance` | Instance QR valide. | Detail instance retourne. | A implementer |

#### UC-19 - Mode secours telephonique

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-180 | P0 | `TraiterValidationSecours` | Decision `AUTORISE`. | ValidationSecours creee, validation nominale executee, audit. | A implementer |
| APP-UC-181 | P0 | `TraiterValidationSecours` | Decision `REFUSE`. | ValidationSecours creee sans validation prestation. | A implementer |
| APP-UC-182 | P1 | `TraiterValidationSecours` | Decision `A_CONTROLER`. | Secours enregistre, execution conforme au code courant. | A confirmer |
| APP-UC-183 | P1 | `TraiterValidationSecours` | Secours request deja traitee. | Idempotence ou refus documente. | A confirmer |
| APP-UC-184 | P1 | `TraiterValidationSecours` | Donnees commerçant/prestation incoherentes. | Refus metier. | A implementer |

#### UC-20 - Messages de contact

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-200 | P0 | `CreerMessageContactConsommateur` | Message valide avec motif actif. | Message cree, thread initialise, notification eventuelle. | A implementer |
| APP-UC-201 | P0 | `CreerMessageContactConsommateur` | Motif absent/inactif. | Refus metier. | A implementer |
| APP-UC-202 | P1 | `CreerMessageContactConsommateur` | Reference achat/coffret optionnelle presente. | Reference conservee. | A implementer |
| APP-UC-203 | P0 | `CreerMessageContactCommercant` | Commercant authentifie. | Message cree avec emetteur commercant. | A implementer |
| APP-UC-204 | P1 | `ListerMotifsContact` | Filtre cible consommateur/commercant. | Motifs actifs compatibles retournes. | A implementer |
| APP-UC-205 | P1 | `ListerMessagesContactCommercant` | Messages d'un commercant. | Threads retournes sans fuite d'autres commercants. | A implementer |
| APP-UC-206 | P0 | `RepondreMessageContactConsommateurAdmin` | Reponse a message consommateur. | Reponse creee, message initial rappele dans email. | A implementer |
| APP-UC-207 | P0 | `RepondreMessageContactCommercantAdmin` | Reponse a message commercant. | Reponse creee, message initial rappele dans email. | A implementer |
| APP-UC-208 | P1 | `RepondreThreadMessageContactCommercant` | Reponse commercant dans son thread. | Message rattache au thread. | A implementer |
| APP-UC-209 | P1 | `ConsulterThreadMessageContactCommercant` | Thread d'un autre commercant. | Refus/introuvable. | A implementer |

#### UC-21 - Documents et facturation

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-220 | P1 | `ServiceDocumentsAchat` | Generer recu achat. | Document cree avec snapshot. | A implementer |
| APP-UC-221 | P1 | `ServiceDocumentsAchat` | Generer pack factures. | Documents attendus crees. | A implementer |
| APP-UC-222 | P1 | `ServiceDocumentsAchat` | Achat absent. | `RessourceDomaineIntrouvable`. | A implementer |
| APP-UC-223 | P1 | Demande facturation | Demande valide. | Demande stockee avec statut attendu. | A implementer |
| APP-UC-224 | P2 | Documents PDF | Contenu PDF exact. | Hors MVP application pur ; test PDF/integration dedie. | Hors MVP |

#### UC-22 - Timeline support

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-230 | P1 | `ConsulterTimelineSupport` | Achat avec paiement, instances, messages, documents. | Evenements agreges et tries. | A implementer |
| APP-UC-231 | P1 | `ConsulterTimelineSupport` | Ressource absente. | `RessourceDomaineIntrouvable`. | A implementer |
| APP-UC-232 | P1 | `ConsulterTimelineSupport` | Donnees sensibles. | Tokens bruts non exposes. | A implementer |

#### UC-23 - Remboursements achat

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-240 | P0 | Annulation instance | Instance active payee. | Statut annule, remboursement a traiter. | A implementer |
| APP-UC-241 | P0 | Annulation instance | Instance deja utilisee. | Refus metier. | A implementer |
| APP-UC-242 | P1 | Remboursement | Marquer remboursement en cours. | Statut coherent. | A implementer |
| APP-UC-243 | P1 | Remboursement | Marquer rembourse avec reference externe. | Reference conservee, audit. | A implementer |
| APP-UC-244 | P1 | Remboursement | Echec/refus remboursement. | Motif conserve. | A implementer |

#### UC-24 - Feedback post-prestation

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-250 | P1 | `ServiceFeedbackPrestation` | Feedback eligible apres validation. | Feedback cree. | A implementer |
| APP-UC-251 | P1 | `ServiceFeedbackPrestation` | Token feedback expire. | Refus metier. | A implementer |
| APP-UC-252 | P1 | `ServiceFeedbackPrestation` | Deuxieme feedback meme validation. | Refus ou idempotence documentee. | A confirmer |
| APP-UC-253 | P1 | Moderation feedback | Approuver commentaire. | Statut publication coherent. | A implementer |
| APP-UC-254 | P1 | Moderation feedback | Refuser commentaire. | Motif conserve. | A implementer |

#### UC-25 - Feed d'activite locale

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-260 | P1 | `IdentifierCoffretsDuMoment` | Coffrets actifs avec activite. | Selection pertinente retournee. | A implementer |
| APP-UC-261 | P1 | `ServiceActivitesLocales` | Activite achat publiee. | Donnees anonymisees. | A implementer |
| APP-UC-262 | P1 | `PurgerActivitesLocales` | Activites au-dela retention. | Activites purgees. | A implementer |
| APP-UC-263 | P2 | Feed public par page. | Hors MVP application sans HTTP. | Hors MVP |

#### UC-26 - Outbox email

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-270 | P0 | `EmailsBatch` | Emails `A_ENVOYER`. | Emails reserves puis envoyes via fake provider. | A implementer |
| APP-UC-271 | P0 | `EmailsBatch` | Provider echec temporaire. | Email `ECHEC_TEMPORAIRE`, retry planifie. | A implementer |
| APP-UC-272 | P0 | `EmailsBatch` | Provider echec definitif. | Email `ECHEC_DEFINITIF`. | A implementer |
| APP-UC-273 | P1 | `EmailsBatch` | Aucun email a envoyer. | Pas d'erreur, compteur zero. | A implementer |
| APP-UC-274 | P1 | Synchronisation email | Provider statut delivre/ouvert. | Statut local mis a jour. | A implementer |

#### UC-27 - Outbox SMS

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-280 | P0 | `SmsBatch` | SMS `A_ENVOYER`. | SMS reserves puis envoyes via fake provider. | A implementer |
| APP-UC-281 | P0 | `SmsBatch` | Provider echec temporaire. | SMS `ECHEC_TEMPORAIRE`. | A implementer |
| APP-UC-282 | P0 | `SmsBatch` | Provider echec definitif. | SMS `ECHEC_DEFINITIF`. | A implementer |
| APP-UC-283 | P1 | `SmsBatch` | Aucun SMS a envoyer. | Pas d'erreur, compteur zero. | A implementer |
| APP-UC-284 | P1 | Synchronisation SMS | Provider statut delivre. | Statut local mis a jour. | A implementer |

#### UC-28 - Expiration et relances

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-290 | P0 | `ExpirationCoffrets` | Instance active expiree. | Instance `EXPIRE`, prestations restantes `EXPIREE`. | A implementer |
| APP-UC-291 | P0 | `ExpirationCoffrets` | Instance active non expiree. | Aucun changement. | A implementer |
| APP-UC-292 | P1 | `ExpirationCoffrets` | Instance deja utilisee/annulee. | Aucun changement. | A implementer |
| APP-UC-293 | P1 | Relance expiration | Instance proche expiration. | Relance creee si non deja envoyee. | A implementer |
| APP-UC-294 | P1 | Relance expiration | Relance deja envoyee. | Pas de doublon. | A implementer |

#### UC-28B - Supervision et ordonnancement batchs

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-300 | P0 | `BatchRunner` | Batch configure execute. | Historique succes, duree, compteur. | A implementer |
| APP-UC-301 | P0 | `BatchRunner` | Batch echoue. | Historique echec, erreur conservee. | A implementer |
| APP-UC-302 | P0 | `BatchRunner` | Verrou concurrent. | Deuxieme execution bloquee. | A implementer |
| APP-UC-303 | P1 | Health batch | Derniere execution recente. | Etat healthy. | A implementer |
| APP-UC-304 | P1 | Health batch | Batch critique absent ou trop ancien. | Etat unhealthy. | A implementer |

#### UC-29 - Mouvements de reversement

| ID | Priorite | Use case/service | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-310 | P0 | Validation prestation | Validation cree mouvement. | Mouvement `A_REVERSER`, montant prestation. | A implementer |
| APP-UC-311 | P0 | Validation prestation | Validation deja traitee. | Pas de double mouvement. | A confirmer |
| APP-UC-312 | P1 | `AfficherMouvementsReversementAReverser` | Mouvements par commercant. | Liste filtree et montants corrects. | A implementer |

#### UC-30 - Generation reversements

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-320 | P0 | `GenererReversements` | Mouvements a reverser pour un commercant avec compte bancaire. | Reversement et lignes crees, mouvements en cours. | A implementer |
| APP-UC-321 | P0 | `GenererReversements` | Aucun mouvement eligible. | Aucun reversement cree, compteur zero. | A implementer |
| APP-UC-322 | P0 | `GenererReversements` | Compte bancaire absent. | Mouvement ignore ou refus selon regle documentee. | A confirmer |
| APP-UC-323 | P1 | `GenererReversements` | Plusieurs commercants. | Un reversement par commercant eligible. | A implementer |
| APP-UC-324 | P1 | `AfficherReversementsEffectues` | Reversements payes depuis une date. | Historique filtre. | A implementer |

#### UC-31 - Paiement manuel des reversements

| ID | Priorite | Use case | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-UC-330 | P0 | `PreparerLotPaiementReversement` | Reversements eligibles. | Lot prepare, paiements `A_INITIER`. | A implementer |
| APP-UC-331 | P0 | `PreparerLotPaiementReversement` | Aucun reversement eligible. | Aucun lot ou lot vide selon regle documentee. | A confirmer |
| APP-UC-332 | P0 | `ExporterLotPaiementReversement` | Lot prepare. | CSV genere, lot `EXPORTE`, hash/taille conserves. | A implementer |
| APP-UC-333 | P0 | `ConfirmerPaiementReversement` | Paiement exporte. | Paiement `EXECUTE`, reversement `PAYE`, mouvements `REVERSE`. | A implementer |
| APP-UC-334 | P0 | `MarquerEchecPaiementReversement` | Paiement exporte. | Paiement `ECHEC`, motif conserve, reversement coherent. | A implementer |
| APP-UC-335 | P1 | `ExporterLotPaiementReversement` | Lot deja exporte. | Idempotence ou refus documente. | A confirmer |

### Tests transverses securite, RGPD et erreurs metier

| ID | Priorite | Cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| APP-XCUT-020 | P0 | Tokens | Aucun use case ne retourne de token hash persistant dans ses sorties publiques. | Hash non expose. | A implementer |
| APP-XCUT-021 | P0 | Donnees personnelles | Les tests utilisent emails/telephones fictifs reserves au test. | Aucun secret reel. | A implementer |
| APP-XCUT-022 | P0 | Exceptions | Les erreurs metier attendues utilisent les exceptions domaine dediees. | Pas de `Exception` generique dans les cas metier testes. | A implementer |
| APP-XCUT-023 | P1 | Transactions | En cas d'erreur metier dans un use case transactionnel. | `rollback` appele ou absence de `commit`. | A implementer |
| APP-XCUT-024 | P1 | Audit | Actions sensibles creent un evenement audit quand le use case le prevoit. | Audit cree avec contexte minimum. | A implementer |
| APP-XCUT-025 | P1 | Outbox | Les use cases ne contactent pas directement Brevo. | Creation outbox ou service fake appele. | A implementer |
| APP-XCUT-026 | P1 | Paiement | Les use cases ne contactent pas directement Stripe hors gateway fake. | Gateway fake appelee. | A implementer |
| APP-XCUT-027 | P1 | Temps | Expiration et TTL calcules depuis une date controlee. | Tests deterministes. | A implementer |
| APP-XCUT-028 | P2 | Documentation | Chaque test P0 reference son UC ou sa regle dans le nom ou commentaire. | Traçabilite lisible. | A implementer |

### Tests infrastructure avec doubles

Ces tests ne remplacent pas des tests d'integration reels en preproduction. Ils verrouillent les contrats techniques locaux : payloads envoyes, erreurs transformees en exceptions metier et mapping ORM/domaine sans provider externe ni base de donnees.

| ID | Priorite | Cible | Scenario | Resultat attendu | Statut |
| --- | --- | --- | --- | --- | --- |
| INF-EMAIL-001 | P0 | `ServiceEnvoiEmail` | Mode dev sans cle Brevo. | Aucun appel HTTP, retour `dev_skipped`. | Termine |
| INF-EMAIL-002 | P0 | `ServiceEnvoiEmail` | Absence de cle hors mode dev. | `ConfigurationTechniqueInvalide` levee. | Termine |
| INF-EMAIL-003 | P0 | `ServiceEnvoiEmail` | Envoi nominal. | Payload Brevo conforme, identifiant provider retourne. | Termine |
| INF-EMAIL-004 | P0 | `ServiceEnvoiEmail` | Brevo retourne une erreur HTTP. | `EnvoiEmailImpossible` levee. | Termine |
| INF-EMAIL-005 | P1 | `ServiceEnvoiEmail` | Verification statut. | Parametres de recherche Brevo conformes, evenement mappe. | Termine |
| INF-SMS-001 | P0 | `ServiceEnvoiSms` | Normalisation numero FR. | Numero converti au format international attendu par Brevo. | Termine |
| INF-SMS-002 | P0 | `ServiceEnvoiSms` | Mode dev sans cle Brevo. | Aucun appel HTTP, retour `dev_skipped`. | Termine |
| INF-SMS-003 | P0 | `ServiceEnvoiSms` | Absence de cle hors mode dev. | `ConfigurationTechniqueInvalide` levee. | Termine |
| INF-SMS-004 | P0 | `ServiceEnvoiSms` | Envoi nominal. | Payload Brevo conforme, identifiant provider retourne. | Termine |
| INF-SMS-005 | P0 | `ServiceEnvoiSms` | Brevo retourne une erreur HTTP. | `EnvoiSmsImpossible` levee. | Termine |
| INF-SMS-006 | P1 | `ServiceEnvoiSms` | Verification statut. | Evenement correspondant au `messageId` retrouve. | Termine |
| INF-PAY-001 | P0 | `PaiementGateway` | Creation checkout Stripe. | Session creee avec montant, quantite, URLs et idempotency key. | Termine |
| INF-PAY-002 | P0 | `PaiementGateway` | Cle Stripe manquante. | `ConfigurationTechniqueInvalide` levee. | Termine |
| INF-PAY-003 | P0 | `PaiementGateway` | Webhook Stripe valide. | Evenement retourne apres verification signature. | Termine |
| INF-PAY-004 | P0 | `PaiementGateway` | Signature webhook invalide. | `QRInvalide` levee selon le comportement courant. | Termine |
| INF-PAY-005 | P1 | `PaiementGateway` | Reconciliation session checkout. | Evenement `checkout.session.completed` reconstruit. | Termine |
| INF-DB-001 | P1 | `VilleRepositorySqlAlchemy` | Ajout ville via fake session. | ORM ajoute, flush appele, entite retournee. | Termine |
| INF-DB-002 | P1 | `VilleRepositorySqlAlchemy` | Obtention ville par id. | ORM mappe vers entite domaine, absence retournee `None`. | Termine |
| INF-DB-003 | P1 | `TypeCoffretRepositorySqlAlchemy` | Ajout type coffret via fake session. | ORM ajoute, flush appele, config retournee. | Termine |

### Ordre d'implementation recommande

1. Creer le socle `tests/`, fixtures, fakes et builders.
2. Implementer tous les tests `DOM-VO-*`.
3. Implementer les tests entites avec methodes metier : `CoffretInstance`, `EmailSortant`, `SmsSortant`, `MouvementReversement`.
4. Couvrir `InitialiserPaiement` et `ValiderPaiement`.
5. Couvrir activation, consultation token et validation prestation.
6. Couvrir authentification commercant et sessions.
7. Couvrir messages contact et reponses support.
8. Couvrir batchs email/SMS/expiration.
9. Couvrir reversements Stripe Connect, campagnes, paiements reversement et reprises/echecs Stripe.
10. Completer les tests P1/P2 et la matrice UC -> tests.

### Definition of Done

- Tous les tests P0 sont implementes et passent.
- Les tests P1 du lot courant sont implementes et passent.
- Les tests ne dependent pas d'une base de donnees ni de providers externes.
- Les fakes restent limites aux comportements necessaires.
- La matrice UC -> tests indique les tests implementes, hors MVP ou a confirmer.
- `pytest` peut etre lance localement avec une commande documentee.
