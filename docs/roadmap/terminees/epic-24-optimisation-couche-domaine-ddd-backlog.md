# Backlog Epic 24 - Optimisation de la couche domaine DDD

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : clarifier la couche domaine Localeo en separant explicitement les entites metier, value objects, repositories et exceptions metier selon des conventions DDD lisibles.
- Decision produit : cette epic ne doit pas modifier le comportement fonctionnel.
- Decision technique : la migration doit etre one-shot, sans phase transitoire ni dette technique volontaire.
- Decision architecture : chaque concept domaine important doit avoir un nom explicite, un fichier dedie et une responsabilite claire.
- Decision compatibilite : les imports consommateurs sont migres dans la meme passe ; aucun ancien chemin d'import n'est maintenu par facade durable.
- Decision nommage : le package des value objects est `value_objects`, pas `value_objets`, pour rester coherent avec les conventions Python et DDD.

## Probleme

La couche domaine contient aujourd'hui plusieurs concepts metier regroupes dans des fichiers larges comme `modeles.py`, `value_objects.py`, `exceptions.py`, `emails.py`, `sms.py`, `reversements.py` et des protocoles repositories concentres dans quelques modules.

Cette organisation fonctionne, mais elle rend la lecture du domaine plus difficile :

- les objets metier sont nombreux et peu visibles individuellement ;
- les repositories ne sont pas tous representes par une classe/protocole dedie dans un fichier explicite ;
- les value objects sont regroupes ;
- les exceptions metier sont centralisees ;
- les noms de fichiers ne racontent pas toujours le concept metier porte ;
- l'evolution du domaine devient plus couteuse a mesure que la marketplace s'etend.

## Objectif cible

Structurer `app/domaine` autour de packages explicites :

```text
app/domaine/
  entities/
    achat_coffret.py
    coffret.py
    coffret_instance.py
    commercant.py
    prestation_coffret.py
    ...
  value_objects/
    email.py
    numero_telephone.py
    montant_euro_centimes.py
    consultation_token.py
    ...
  repositories/
    achat_coffret_repository.py
    coffret_repository.py
    commercant_repository.py
    message_contact_repository.py
    ...
  exceptions/
    regle_metier_violee.py
    ressource_domaine_introuvable.py
    configuration_technique_invalide.py
    ...
```

## Perimetre MVP

- Creer les packages `entities`, `value_objects`, `repositories` et `exceptions`.
- Deplacer chaque classe domaine dans un fichier dedie en une seule migration.
- Migrer tous les imports consommateurs dans la meme passe.
- Autoriser les renommages publics si tous les imports consommateurs sont migres dans la meme passe.
- Distinguer les noms internes de fichiers des noms publics importables.
- Documenter les conventions de nommage.
- Supprimer les modules fourre-tout ou les vider de leurs definitions metier dans la meme passe.
- Ajouter des tests de non-regression sur les imports et les comportements de base.

## Hors perimetre MVP

- Modifier les tables SQL.
- Modifier les endpoints API.
- Modifier les workflows metier.
- Repenser les aggregates et transactions metier en profondeur.
- Changer l'Unit of Work.
- Refaire les repositories SQLAlchemy.
- Introduire une nouvelle librairie DDD.

## User Stories

1. `PRD-135` En tant que developpeur, je veux trouver chaque entite metier dans un fichier dedie afin de comprendre rapidement le domaine.
   - Statut : `Termine`
   - Resultat attendu : chaque entite principale est exposee depuis `app.domaine.entities`.
   - Resultat attendu : les imports consommateurs pointent directement vers `app.domaine.entities`.

2. `PRD-136` En tant que developpeur, je veux trouver chaque value object dans un fichier dedie afin de distinguer clairement les types metier des primitives.
   - Statut : `Termine`
   - Resultat attendu : chaque value object est expose depuis `app.domaine.value_objects`.
   - Resultat attendu : les validations restent strictement equivalentes.

3. `PRD-137` En tant que developpeur, je veux avoir un package repositories avec une classe ou un protocole par repository afin de clarifier les ports de persistence du domaine.
   - Statut : `Termine`
   - Resultat attendu : chaque repository domaine a un fichier dedie.
   - Resultat attendu : les implementations infrastructure continuent de respecter ces ports.

4. `PRD-138` En tant que developpeur, je veux avoir un package exceptions avec une classe par exception metier afin de rendre les erreurs domaine explicites.
   - Statut : `Termine`
   - Resultat attendu : chaque exception metier a son propre fichier.
   - Resultat attendu : les imports consommateurs pointent directement vers `app.domaine.exceptions`.

5. `PRD-139` En tant que responsable technique, je veux une cartographie des objets domaine afin de savoir quels concepts existent et ou ils sont definis.
   - Statut : `Termine`
   - Resultat attendu : une documentation liste entites, value objects, repositories et exceptions.

6. `PRD-140` En tant que developpeur, je veux des conventions de nommage domaine afin d'eviter les classes generiques ou ambiguës.
   - Statut : `Termine`
   - Resultat attendu : les fichiers utilisent le nom metier en snake_case.
   - Resultat attendu : les classes utilisent un nom metier explicite en PascalCase.

7. `PRD-141` En tant que mainteneur, je veux migrer tous les imports domaine en une seule passe afin d'atteindre directement la structure cible.
   - Statut : `Termine`
   - Resultat attendu : aucun import applicatif ne pointe encore vers les anciens modules domaine a la fin de la migration.

8. `PRD-142` En tant que mainteneur, je veux supprimer les anciens modules fourre-tout une fois la migration terminee afin d'eviter deux sources de verite.
   - Statut : `Termine`
   - Resultat attendu : `modeles.py`, `value_objects.py` et `exceptions.py` ne contiennent plus de definitions metier finales ni de reexports de compatibilite durables.

9. `PRD-143` En tant que developpeur, je veux que la couche domaine reste independante de FastAPI, SQLAlchemy et des providers externes afin de conserver une architecture propre.
   - Statut : `Termine`
   - Resultat attendu : les packages domaine ne dependent pas de l'infrastructure.

10. `PRD-144` En tant que responsable qualite, je veux des tests de non-regression sur les objets domaine afin de securiser la migration.
    - Statut : `Termine`
    - Resultat attendu : les value objects, exceptions et entites critiques sont testes.
    - Resultat attendu : les nouveaux chemins d'import sont testes et les anciens chemins sont absents du code applicatif.

11. `PRD-145` En tant que mainteneur, je veux gerer explicitement les noms publics du domaine afin d'eviter les ruptures d'import non maitrisees.
    - Statut : `Termine`
    - Resultat attendu : tous les renommages publics retenus sont documentes.
    - Resultat attendu : tout renommage de classe publique est applique directement dans tous les imports consommateurs.

12. `PRD-146` En tant que developpeur, je veux une strategie de refactoring one-shot des imports afin de supprimer immediatement les anciens chemins.
    - Statut : `Termine`
    - Resultat attendu : tous les imports sont recalcules et verifies dans la meme branche.
    - Resultat attendu : les anciens chemins d'import echouent si reutilises apres la migration cible.

## Regles de structuration

### Package `entities`

- Une classe par entite metier.
- Un fichier par entite.
- Les enums fortement rattaches a une entite restent dans le meme fichier que cette entite au debut de la migration one-shot.
- Les entites ne dependent pas de SQLAlchemy, FastAPI ou Pydantic.
- Les noms doivent refleter le langage metier : `AchatCoffret`, `CoffretInstance`, `MessageContact`, `RemboursementAchat`.

### Package `value_objects`

- Une classe par value object.
- Un fichier par value object.
- Les value objects portent leurs invariants.
- Les value objects sont immuables ou traites comme tels.
- Les noms doivent eviter les abreviations techniques.

### Package `repositories`

- Une classe ou protocole par repository.
- Un fichier par repository.
- Les repositories domaine restent des ports, pas des implementations SQLAlchemy.
- Les implementations restent dans `app.infrastructure.persistence`.

### Package `exceptions`

- Une classe par exception metier.
- Un fichier par exception.
- Les exceptions doivent exprimer une intention metier.
- Les exceptions techniques ne doivent pas etre melangees avec les erreurs domaine si elles ne concernent pas le domaine.

## Imports et noms publics

### Principes

- Un nom public est une classe, enum, protocole ou exception importee par les couches `application`, `api`, `infrastructure` ou par des tests.
- Tous les renommages publics sont acceptes dans la migration one-shot s'ils sont appliques partout dans la meme passe.
- Un deplacement de fichier n'implique pas un renommage de classe.
- Un renommage de classe doit etre applique partout dans la meme passe.
- Les modules historiques (`modeles.py`, `value_objects.py`, `exceptions.py`) ne doivent pas devenir des facades durables.
- Les imports doivent pointer directement vers les packages cibles (`entities`, `value_objects`, `repositories`, `exceptions`) a la fin de la migration.

### Strategie one-shot

1. Cartographier tous les objets domaine et tous les imports consommateurs.
2. Creer les packages et fichiers cibles.
3. Deplacer les definitions dans les fichiers cibles.
4. Mettre a jour tous les imports applicatifs, infrastructure, API et tests.
5. Supprimer les definitions et reexports des anciens modules.
6. Lancer la compilation complete et les tests.
7. Refuser le merge s'il reste un import vers un ancien module domaine devenu obsolete.

### Regles de renommage

- Les renommages purement cosmetiques sont evites.
- Un renommage est accepte seulement si le nom actuel est ambigu, faux ou trop technique.
- Le nouveau nom doit appartenir au langage metier Localeo.
- L'ancien nom n'est pas conserve par alias si la decision de migration one-shot valide le renommage.
- Les usages de l'ancien nom doivent etre corriges dans la meme passe.

### Tests requis

- Test d'import depuis le nouveau package.
- Test d'absence d'imports consommateurs vers les anciens modules obsoletes.
- Test de comportement pour les value objects et exceptions deplacees.
- Compilation de tous les use cases consommateurs apres la migration one-shot.

## Migration cible one-shot

- Creer `app/domaine/entities`.
- Creer `app/domaine/value_objects`.
- Creer `app/domaine/repositories`.
- Creer `app/domaine/exceptions`.
- Ajouter des `__init__.py` propres aux nouveaux packages, sans facade de compatibilite durable.
- Definir les renommages publics retenus et leur cible finale.
- Extraire les exceptions de `exceptions.py`.
- Extraire `Email`, `NumeroTelephone`, `MontantEuroCentimes` et autres value objects.
- Extraire les entites catalogue.
- Extraire les entites achat/coffret/paiement.
- Extraire messages contact, emails, SMS, reversements, remboursements.
- Scinder `repositories/protocols.py` et `repositories/reversements_protocols.py`.
- Un fichier par repository.
- Adapter l'Unit of Work si necessaire sans changer son contrat public.
- Mettre a jour tous les imports consommateurs dans `app/application`, `app/api`, `app/infrastructure` et les tests.
- Supprimer les definitions restantes dans les modules fourre-tout.
- Supprimer les reexports ou alias de compatibilite.
- Verifier qu'aucun import obsolète ne subsiste.
- Mettre a jour la documentation architecture.

## Criteres d'acceptation MVP

- Les packages cibles existent.
- Les exceptions metier sont separees.
- Les principaux value objects sont separes.
- Les principales entites sont separees.
- Les repositories domaine sont decoupés par concept.
- Aucun import consommateur ne pointe vers les anciens modules domaine obsoletes.
- Aucun endpoint API ne change.
- Aucun schema base de donnees ne change.
- Les tests existants passent.
- La documentation de la couche domaine est mise a jour.
- Les renommages publics retenus sont documentes.
- Les nouveaux chemins d'import sont couverts par des tests.
- Aucun alias temporaire ou facade de compatibilite durable n'est introduit.

## Risques

- Refactor massif difficile a relire.
- Imports circulaires entre entites.
- Rupture immediate si un import consommateur est oublie.
- Regression silencieuse si les value objects sont modifies au lieu d'etre deplaces.
- Trop vouloir modeliser les aggregates avant d'avoir stabilise la structure.

## Decisions actees

- Nom final du package : `value_objects`.
- Niveau de decoupage des enums : avec l'entite au debut.
- Liste des noms publics qui doivent rester strictement identiques : aucune liste specifique a maintenir.
- Liste des renommages publics acceptes dans la migration one-shot : tous.
- Ordre exact de migration des entites les plus sensibles : aucun ordre impose.

## Decisions a prendre avant implementation

- Aucune decision bloquante restante identifiee a ce stade.
