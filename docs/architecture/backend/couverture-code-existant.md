# Couverture de tests du code existant

## Objectif

Ce document trace l'application retroactive du principe de developpement :
toute modification d'un use case, d'un objet domaine ou d'un composant
infrastructure doit creer ou mettre a jour un test utile dans la meme livraison.

## Principe retenu

Les tests sont regroupes par domaine fonctionnel lorsque cela rend les scenarios
plus lisibles. Un test doit verifier une regle observable :

- invariant de value object ou d'entite ;
- transition d'etat ;
- decision metier ;
- erreur metier attendue ;
- appel de port ou effet applicatif observable ;
- contrat technique utile pour un adapter d'infrastructure.

Les tests qui verifient uniquement l'import, l'existence d'une classe ou une
instanciation vide ne sont pas consideres comme une couverture metier.

Deux gardes structurels sont toutefois maintenus pour detecter les oublis de
test :

- chaque use case applicatif public exposant `execute` doit avoir une classe
  `Test<UseCase>` dediee avec au moins une methode `test_*` ;
- chaque classe publique de `app/domaine` doit avoir un fichier
  `test_<objet>_dedicated.py` dedie, range par domaine fonctionnel et categorie.

Ces gardes detectent les oublis de test, mais ne remplacent pas les scenarios
metier utiles lorsque le comportement evolue.

## Couverture transversale conservee

Le fichier `tests/architecture/test_module_contracts.py` reste utile comme garde
d'architecture. Il couvre :

- l'import de tous les modules `app/domaine` ;
- l'import de tous les modules `app/application/**/use_cases` ;
- l'import de tous les modules `app/infrastructure` ;
- l'absence de dependance du domaine vers FastAPI, Pydantic, SQLAdmin,
  SQLAlchemy, Stripe, `app.api`, `app.application` ou `app.infrastructure`.

Cette couverture detecte les imports cassants et les dependances interdites,
mais ne remplace pas les tests metier.

## Couverture dediee par classe et par use case

Le dossier `tests/application/use_cases` contient des classes `Test<UseCase>`
rangees par domaine fonctionnel. Chaque classe cible un use case applicatif
public exposant `execute` et doit tester au moins une regle observable du
workflow : entree invalide, erreur metier, transition d'etat, idempotence, appel
de port ou effet applicatif attendu.

Le fichier `tests/application/use_cases/test_use_case_business_test_coverage.py`
controle que :

- tous les use cases publics exposes sous `app/application/**/use_cases/*.py`
  disposent d'une classe `Test<UseCase>` ;
- chaque classe dediee contient au moins une methode `test_*` ;
- l'ancien fichier de couverture purement structurelle
  `test_use_case_dedicated_classes.py` n'existe pas ;
- aucune classe generique `TestUseCase...` ou `_DedicatedUseCaseTest` ne revient
  comme substitut a des tests metier.

Le dossier `tests/domain` contient 127 fichiers `test_<objet>_dedicated.py`,
soit un fichier par classe publique detectee sous `app/domaine/**/*.py`. Les
fichiers sont ranges par domaine fonctionnel et categorie :
`tests/domain/<domaine>/<categorie>`.

Le fichier `tests/domain/test_domain_dedicated_classes.py` controle que :

- toutes les classes publiques de `app/domaine` ont un fichier dedie ;
- tous les packages de domaine ont un package de test, y compris les enveloppes
  sans objet metier encore implemente.

## Tests comportementaux ajoutes

Les tests suivants couvrent des regles domaine explicites :

- `tests/domain/<domaine>/entities/test_*_dedicated.py` : regles
  d'instanciation et de conservation des champs specifiees pour catalogue,
  achat, paiement, validation, identite, support, exploitation et reversement ;
- `tests/domain/shared/value_objects/test_money.py` : conversion centimes/euros et
  formatage monetaire lisible avec symbole euro ;
- `tests/application/use_cases/test_initialiser_paiement.py` : normalisation de
  la cle d'idempotence, rejet des cles trop longues, creation d'achat,
  initialisation checkout et transmission du `transfer_group` Stripe ;
- `tests/application/use_cases/test_stripe_connect_onboarding.py` :
  initialisation onboarding Stripe Connect, reutilisation d'un compte existant,
  feature flag, consultation locale, synchronisation, webhook `account.updated`
  et idempotence webhook ;
- `tests/application/use_cases/test_valider_paiement.py` : idempotence des
  evenements Stripe, ignore des evenements non checkout, rejet des checkout
  incomplets et extraction des references Stripe `PaymentIntent`, `Charge`,
  `Customer` et `transfer_group` ;
- `tests/application/use_cases/test_transfers_stripe.py` : campagne de transfers
  Stripe Connect et confirmation locale par webhook ;
- `tests/application/use_cases/test_referencement_use_cases.py` : listing,
  consultation, mise a jour de contact, referencement, notes internes et vision
  360 commercant ;
- `tests/application/use_cases/test_commercialisation_profils_use_cases.py` :
  consultation des coffrets, prestations, rentabilite, marketplace et profil
  commercant ;
- `tests/application/use_cases/test_identite_acces_use_cases.py` :
  authentification, initialisation, reinitialisation, sessions, tokens de
  consultation et purge ;
- `tests/application/use_cases/test_documentaire_use_cases.py` : cycle de vie
  documentaire admin, publication, consultation publique et consultation
  commercant ;
- `tests/application/use_cases/test_gestion_achats_use_cases.py` : activation,
  consultation, QR, tokens, relances, expiration et reconciliation achat ;
- `tests/application/use_cases/test_exploitation_use_cases.py` : liens courts,
  statistiques, validations, batch emails/SMS, evenements et webpush ;
- `tests/application/use_cases/test_support_use_cases.py` : motifs de contact,
  messages, reponses admin, communications libres, timeline et vision 360
  client ;
- `tests/application/use_cases/test_gestion_reversement_use_cases.py` :
  mouvements eligibles, reversements, lots de paiement, exports et echecs de
  paiement de reversement ;
- `tests/domain/referencement/test_commercant.py` : eligibilite Stripe Connect
  du commercant ;
- `tests/domain/identite_acces/test_api_key.py` : controle strict des scopes
  API key ;
- `tests/domain/gestion_reversement/entities/test_reversement_stripe_objects.py` : objets de
  reversement et references Stripe ;
- tests existants sur `CoffretInstance`, `EmailSortant`, `SmsSortant`,
  `MouvementReversement`, `PaiementReversement` et value objects.

## Verification

Commandes executees :

```bash
pytest tests/application/use_cases -q
pytest tests/application/use_cases/test_gestion_reversement_use_cases.py -q
pytest tests/application/use_cases/test_use_case_business_test_coverage.py -q
pytest -q
```

Resultat cible use cases : 194 tests passants.

Resultat global : 812 tests passants, 2 warnings FastAPI sur `on_event`
deprecie.

## Regle pour les prochains changements

Aucun changement sur un use case, un objet domaine ou un composant
infrastructure ne doit etre livre sans test comportemental ou technique adapte
au changement. Le test peut etre place dans un fichier regroupe par domaine
fonctionnel si cela ameliore la lisibilite.

L'ajout d'un use case public sans classe `Test<UseCase>` dediee, sans methode de
test, ou avec une couverture limitee a l'import, l'existence de classe ou
l'instanciation doit faire echouer les gardes de couverture et etre refuse en
revue.

L'ajout d'une classe publique de domaine sans fichier dedie doit egalement faire
echouer les gardes de couverture.
