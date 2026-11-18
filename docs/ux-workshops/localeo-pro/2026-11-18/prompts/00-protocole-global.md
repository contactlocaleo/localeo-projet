# ÉTAPE 1 — INITIALISATION ET EXPLORATION UX LOCALEO PRO

> Prompt utilisateur complet utilisé pour cette étape, transcrit avec les identifiants remplacés par `[CONFIDENTIEL]`.

Tu es chargé de préparer le workshop UX de Localeo Pro, l'application destinée aux commerçants.

## 1. Accès à l'application

**Environnement de test :**

[https://test-animations.localeo.city](https://test-animations.localeo.city)

**Identifiants de connexion :**

- Login : [CONFIDENTIEL]
- Mot de passe : [CONFIDENTIEL]

Utilise exclusivement ces identifiants pour accéder à l'environnement de test.

Ne publie jamais les identifiants dans les rapports, les captures d'écran, les journaux ou les fichiers versionnés du projet.

Si les identifiants ne sont pas fournis, demande-les avant de tester les parcours authentifiés.

## 2. Périmètre du workshop

Localeo Pro est le carnet opérationnel du commerçant pour participer aux animations de sa commune.

Quatre missions prioritaires :

1. **Première impression et prise en main** : accès, connexion, compréhension de l'accueil, navigation et actions principales.
2. **Validation des participations** : accès au scanner, validation QR code, confirmation, erreurs et doublons.
3. **Notifications et préparation** : informations sur les animations à venir, actions attendues et préparation de la participation.
4. **Kit d'animation et logistique** : supports, QR codes, consignes, échéances et suivi des tâches.

La gestion des coffrets, les reversements et les statistiques avancées sont hors périmètre, sauf s'ils perturbent la navigation principale.

## 3. Initialisation du répertoire

Crée un répertoire daté :

`docs/ux-workshops/localeo-pro/YYYY-MM-DD/`

Utilise la date locale de l'exécution.

Si un workshop existe déjà ce jour-là, ajoute un suffixe `-02`, `-03`, etc.

Crée :

- `prompts/`
- `observations/`
- `workshop/`
- `visuels/captures-avant/`
- `visuels/maquettes-apres/`
- `validation/`
- `synthese/`

Initialise le README avec la date, l'URL, la branche Git, le commit et le statut.

## 4. Archivage des prompts

Prépare les fichiers :

- `prompts/00-protocole-global.md`
- `prompts/01-exploration.md`
- `prompts/02-workshop.md`
- `prompts/03-maquettes.md`
- `prompts/04-validation.md`
- `prompts/05-archivage.md`

Enregistre les prompts complets réellement utilisés, en remplaçant systématiquement les identifiants par `[CONFIDENTIEL]`.

Ne conserve jamais le mot de passe en clair dans les fichiers du workshop.

## 5. Exploration réelle

Utilise Playwright ou un navigateur automatisé pour explorer l'application sur smartphone, puis sur ordinateur.

Teste les parcours :

1. Première connexion.
2. Découverte de l'accueil.
3. Accès à une animation.
4. Validation d'une participation par QR code.
5. Confirmation et gestion des erreurs.
6. Réception ou consultation des notifications.
7. Préparation d'une animation.
8. Accès au kit d'animation.
9. Consultation des supports et consignes.
10. Retour dans l'application après plusieurs jours.

Utilise uniquement des données de test autorisées.

Ne valide pas de participations réelles et n'envoie pas de notifications à de véritables commerçants.

## 6. Analyse du code

Complète les observations par une inspection du dépôt si disponible.

Identifie les routes, composants, mécanismes de scan, notifications et parcours logistiques.

Distingue les fonctionnalités implémentées de celles qui ne sont pas accessibles.

## 7. Livrables

Dans `observations/`, crée :

- `cartographie-parcours.md`
- `inventaire-ecrans.md`
- `observations-factuelles.md`
- `limitations.md`

Enregistre les captures dans `visuels/captures-avant/`.

Pour chaque constat, indique :

- OBSERVÉ.
- DÉDUIT.
- HYPOTHÈSE.

Associe les observations à leurs preuves.

## 8. Contraintes et arrêt

- Aucune modification du code applicatif.
- Aucun secret enregistré.
- Aucune simulation de workshop à cette étape.
- Aucune maquette.
- Aucune action destructive sur les données de test.

Mets à jour le README, présente les résultats et les limitations, puis attends mon autorisation avant l'étape 2.
