# ÉTAPE 1 — INITIALISATION ET EXPLORATION UX LOCALEO CRM

Tu es chargé de préparer un workshop UX complet consacré à Localeo CRM, l'application de gestion et de pilotage de la prospection commerciale de Localeo.

## 1. Accès à l'application

À renseigner avant exécution :

URL de test : `https://test-crm.localeo.city`

Login : [CONFIDENTIEL]

Mot de passe : [CONFIDENTIEL]

Utilise ces informations exclusivement pour te connecter à l'environnement autorisé.

Ne conserve jamais les identifiants sensibles dans les rapports, captures, fichiers Git ou prompts archivés.

Lors de l'archivage, remplace les valeurs sensibles par `[CONFIDENTIEL]`.

Privilégie les variables d'environnement ou un gestionnaire de secrets lorsque possible.

## 2. Objectif produit

Localeo CRM doit permettre à une petite équipe commerciale de piloter efficacement la prospection de communes, associations de commerçants et autres prospects professionnels.

Il doit permettre de :

1. Disposer d'une vision claire et exhaustive de l'état de la prospection.
2. Identifier les actions à réaliser aujourd'hui et prochainement.
3. Planifier, préparer et suivre les rendez-vous.
4. Qualifier et suivre chaque prospect.
5. Collaborer sans doublons, oublis ou perte d'informations.

Le CRM doit être suffisamment intuitif pour être utilisé par une personne peu habituée aux outils commerciaux.

## 3. Périmètre de l'audit

### Mission A — Tableau de bord et pilotage

- Compréhension de l'accueil.
- Vision du pipeline.
- Indicateurs clés.
- Répartition par statut.
- Opportunités prioritaires.
- Prospects inactifs.
- Actions en retard.
- Rendez-vous à venir.
- Vision individuelle et collective.

### Mission B — Qualification des prospects

- Recherche.
- Création.
- Import éventuel.
- Identification des doublons.
- Fiche prospect.
- Contacts et interlocuteurs.
- Qualification.
- Statuts.
- Historique.
- Notes.
- Prochaines actions.
- Affectation à un responsable.

### Mission C — Rendez-vous

- Création.
- Planification.
- Agenda.
- Disponibilités.
- Association à un prospect.
- Préparation.
- Compte rendu.
- Résultat.
- Prochaine étape.
- Modification et annulation.

### Mission D — Relances et tâches

- Création d'une tâche.
- Échéances.
- Rappels.
- Tâches du jour.
- Actions en retard.
- Priorités.
- Relances.
- Historique des actions.
- Prévention des oublis.

### Mission E — Collaboration

- Affectation des prospects.
- Visibilité des responsables.
- Partage des rendez-vous.
- Historique des interventions.
- Transmission d'un dossier.
- Prévention des doublons.
- Pilotage global de l'équipe.

## 4. Initialisation du répertoire

Détermine la date locale au format YYYY-MM-DD.

Crée :

`docs/ux-workshops/localeo-crm/YYYY-MM-DD/`

Si une autre exécution existe déjà ce jour-là, ajoute -02, -03, etc.

Crée :
- `prompts/`
- `observations/`
- `workshop/`
- `visuels/captures-avant/`
- `visuels/maquettes-apres/`
- `validation/`
- `synthese/`

Initialise README.md avec la date, l'URL sans secrets, la branche Git, le commit et le statut.

## 5. Archivage des prompts

Prépare :
- `prompts/00-protocole-global.md`
- `prompts/01-exploration.md`
- `prompts/02-workshop.md`
- `prompts/03-maquettes.md`
- `prompts/04-validation.md`
- `prompts/05-archivage.md`

Enregistre cette instruction complète dans `01-exploration.md`, en supprimant les valeurs sensibles.

Ne prétends pas avoir archivé les autres prompts s'ils ne sont pas encore disponibles.

## 6. Exploration réelle

Utilise Playwright ou un navigateur automatisé.

Explore prioritairement sur ordinateur, puis sur smartphone.

Teste les parcours :

1. Première connexion.
2. Découverte du tableau de bord.
3. Consultation de l'état global de la prospection.
4. Identification des actions prioritaires.
5. Recherche d'un prospect.
6. Création d'un prospect.
7. Qualification.
8. Modification du statut.
9. Ajout d'un contact.
10. Consultation de l'historique.
11. Création d'une tâche.
12. Planification d'une relance.
13. Consultation des tâches en retard.
14. Création d'un rendez-vous.
15. Consultation de l'agenda.
16. Modification d'un rendez-vous.
17. Préparation d'une démonstration.
18. Compte rendu après rendez-vous.
19. Affectation d'un prospect.
20. Suivi collectif de l'activité.

Ne présuppose pas que toutes ces fonctionnalités existent.

Utilise exclusivement des données de test autorisées.

Ne modifie pas de véritables prospects, rendez-vous ou tâches sans autorisation explicite.

## 7. Analyse de l'exhaustivité du pilotage

Vérifie particulièrement si le CRM permet d'identifier :

- Les prospects sans responsable.
- Les prospects sans prochaine action.
- Les prospects sans interaction récente.
- Les relances en retard.
- Les rendez-vous à venir.
- Les opportunités sans évolution.
- Les doublons potentiels.
- Les actions affectées aux différents utilisateurs.

Distingue les capacités existantes des besoins non couverts.

## 8. Analyse complémentaire du code

Si le dépôt est accessible, examine :
- Les routes.
- Les composants.
- Le modèle de données.
- Les statuts.
- Les formulaires.
- Les filtres.
- Les tâches.
- L'agenda.
- Les rendez-vous.
- Les mécanismes de notification.
- Les règles d'affectation.

Ne confonds pas l'existence d'une fonctionnalité dans le code avec son utilisabilité réelle.

## 9. Livrables

Dans `observations/`, crée :
- `cartographie-parcours.md`
- `inventaire-ecrans.md`
- `observations-factuelles.md`
- `couverture-pilotage-commercial.md`
- `limitations.md`

Enregistre les captures réelles dans `visuels/captures-avant/`.

Pour chaque constat :
- OBSERVÉ.
- DÉDUIT.
- HYPOTHÈSE.

Associe les observations à leurs preuves.

## 10. Contraintes

Aucune modification du code applicatif.

Aucune donnée réelle modifiée sans autorisation.

Aucun secret archivé.

Aucune simulation d'utilisateurs à cette étape.

Aucune maquette.

Mets à jour le README et attends mon autorisation avant l'étape 2.

