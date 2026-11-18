# ÉTAPE 1 — INITIALISATION ET EXPLORATION UX LOCALEO ANIMATION

Tu es chargé de préparer un workshop UX complet sur la plateforme Localeo Animation, destinée aux organisateurs d'animations commerciales locales.

## 1. Accès à l'application

Renseigner avant exécution :

**URL de l'environnement de test :**
`https://test-animations.localeo.city`

**Identifiants de test :**
- Login : `[CONFIDENTIEL]`
- Mot de passe : `[CONFIDENTIEL]`

Ces informations sont exclusivement destinées à la connexion.

Ne conserve jamais le mot de passe ou les identifiants sensibles dans les fichiers du workshop, les captures, les rapports ou les journaux.

Lors de l'archivage du prompt, remplace les valeurs sensibles par `[CONFIDENTIEL]`.

Si les champs ne sont pas renseignés, demande les informations manquantes avant d'explorer les parcours authentifiés.

Privilégie, lorsque possible, l'utilisation de variables d'environnement ou d'un gestionnaire de secrets.

## 2. Objectif produit

Localeo Animation doit permettre à une association de commerçants, une commune ou un organisateur de :

1. Créer et publier une animation simplement.
2. Intégrer les commerçants participants.
3. Suivre le déroulement et les participations.
4. Clôturer l'animation et consulter son bilan.
5. Piloter l'ensemble de ses animations depuis une interface cohérente.

La promesse produit à challenger est :

**« Créer une animation simple en 5 à 10 minutes, puis la piloter en toute autonomie. »**

Cette durée constitue un objectif produit à vérifier, pas une performance acquise.

## 3. Périmètre de l'audit

### Mission A — Création et publication
- Découverte du processus de création.
- Choix du type d'animation.
- Paramétrage.
- Définition des dates et conditions.
- Configuration des dotations.
- Enregistrement et reprise d'un brouillon.
- Prévisualisation.
- Publication.
- Compréhension des erreurs et validations.

### Mission B — Onboarding des commerçants
- Ajout individuel.
- Import en masse lorsqu'il existe.
- Invitation et activation.
- Association à une animation.
- Suivi des commerçants participants.
- Gestion des erreurs et doublons.
- Compréhension des actions restantes.

### Mission C — Suivi opérationnel
- Accès à une animation en cours.
- Compréhension des statuts.
- Consultation des participations.
- Suivi des indicateurs.
- Identification des anomalies.
- Actions correctives disponibles.
- Communication et notifications lorsqu'elles existent.

### Mission D — Clôture
- Identification de la fin d'animation.
- Clôture manuelle ou automatique selon les mécanismes disponibles.
- Résultats et tirages au sort lorsqu'applicables.
- Gestion des lots et gagnants.
- Vérification des actions restantes.
- Bilan final.

### Mission E — Pilotage global
- Tableau de bord.
- Liste des animations.
- Recherche et filtres.
- Gestion des statuts.
- Suivi des échéances.
- Duplication et réutilisation.
- Pilotage de plusieurs animations.
- Compréhension de l'activité globale.

## 4. Initialisation du répertoire daté

Détermine la date locale au format YYYY-MM-DD.

Crée :

`docs/ux-workshops/localeo-animation/YYYY-MM-DD/`

Si une exécution existe déjà ce jour-là, utilise un suffixe -02, -03, etc.

Crée :

- `prompts/`
- `observations/`
- `workshop/`
- `visuels/captures-avant/`
- `visuels/maquettes-apres/`
- `validation/`
- `synthese/`

Initialise `README.md` avec :
- Date et heure.
- URL analysée, sans secrets.
- Branche Git.
- Commit Git.
- Objectif.
- Statut.
- Modèle et niveau de raisonnement, si connus.

## 5. Archivage des prompts

Prépare :

- `prompts/00-protocole-global.md`
- `prompts/01-exploration.md`
- `prompts/02-workshop.md`
- `prompts/03-maquettes.md`
- `prompts/04-validation.md`
- `prompts/05-archivage.md`

Enregistre ce prompt complet dans `01-exploration.md`, en supprimant les valeurs sensibles.

Ne prétends pas avoir archivé un prompt qui n'a pas été fourni.

## 6. Exploration réelle

Utilise Playwright ou un navigateur automatisé.

Privilégie le format ordinateur pour les parcours d'administration et vérifie également la compatibilité mobile.

Explore les parcours :

1. Première connexion.
2. Découverte du tableau de bord.
3. Création d'une tombola simple.
4. Création d'un passeport commerçant.
5. Configuration des dotations.
6. Enregistrement et reprise d'un brouillon.
7. Prévisualisation et publication.
8. Ajout individuel de commerçants.
9. Import en masse.
10. Invitation et suivi d'activation.
11. Consultation d'une animation en cours.
12. Suivi des participations.
13. Communication et notifications.
14. Clôture d'une animation.
15. Résultats, gagnants et lots.
16. Consultation du bilan.
17. Duplication d'une animation.
18. Pilotage de plusieurs animations.

Ne présuppose pas que tous les parcours existent.

Pour les actions qui modifient des données, utilise exclusivement des objets de test autorisés.

Avant toute publication, clôture, invitation ou notification susceptible d'affecter de vrais utilisateurs, vérifie que l'action est sûre et limitée à l'environnement de test. Sinon, arrête-toi avant l'action et documente la limitation.

## 7. Mesures de parcours

Pour chaque parcours, relève lorsque cela est réellement mesurable :
- Nombre d'étapes.
- Nombre de clics.
- Champs obligatoires.
- Points de friction.
- Retours arrière.
- Erreurs.
- Informations manquantes.
- Temps de réalisation si un chronométrage réel est disponible.

Ne fabrique pas de temps de parcours.

## 8. Analyse du code

Si le dépôt est accessible, complète l'observation par l'analyse :
- Des routes.
- Des formulaires.
- Des composants.
- Des validations.
- Des statuts.
- Des mécanismes de publication.
- Des imports.
- Des notifications.
- Des tableaux de bord.
- Des mécanismes de clôture.

Distingue les fonctionnalités implémentées, non accessibles et simplement envisagées.

## 9. Livrables

Dans `observations/`, crée :

- `cartographie-parcours.md`
- `inventaire-ecrans.md`
- `observations-factuelles.md`
- `limitations.md`
- `mesures-parcours.md`

Enregistre les captures dans `visuels/captures-avant/`.

Classe chaque constat :

- OBSERVÉ.
- DÉDUIT.
- HYPOTHÈSE.

Associe les constats à leurs preuves.

## 10. Contraintes et arrêt

- Aucune modification du code applicatif.
- Aucun secret archivé.
- Aucune simulation d'expert ou d'utilisateur à cette étape.
- Aucune maquette.
- Aucune action destructive non autorisée.
- Aucune publication réelle non autorisée.

Mets à jour le README.

Présente les résultats et les éventuelles limitations.

Arrête-toi et attends mon autorisation avant l'étape 2.
