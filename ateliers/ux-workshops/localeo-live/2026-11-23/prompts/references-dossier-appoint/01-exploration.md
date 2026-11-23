# ÉTAPE 1 — INITIALISATION ET EXPLORATION UX LOCALEO LIVE

Tu interviens dans le projet Localeo pour préparer un workshop UX complet sur l'application Localeo Live.

Application : [https://test-live.localeo.city](https://test-live.localeo.city)

## 1. Périmètre prioritaire

Localeo Live est le carnet digital de l'habitant.

Pour son lancement, trois missions sont prioritaires :

1. Participer aux animations de sa commune : découvrir, rejoindre, participer et suivre ses animations.
2. Gérer ses lots : retrouver ses gains, comprendre leurs conditions d'utilisation et suivre leurs statuts.
3. Consulter le calendrier des animations : identifier les animations en cours et à venir, consulter leurs dates et accéder à leurs détails.

Les coffrets et les autres fonctionnalités sont secondaires dans ce workshop. Examine-les uniquement pour vérifier qu'ils ne perturbent pas la compréhension des trois missions principales.

## 2. Initialiser le répertoire daté

Détermine la date locale d'exécution au format YYYY-MM-DD.

Crée :

`docs/ux-workshops/YYYY-MM-DD/`

Si un répertoire existe déjà pour cette date et correspond à une autre exécution, ajoute un suffixe -02, -03, etc.

N'écrase jamais un workshop précédent.

Crée immédiatement cette structure :

- `prompts/`
- `observations/`
- `workshop/`
- `visuels/captures-avant/`
- `visuels/maquettes-apres/`
- `validation/`
- `synthese/`

Crée également un fichier `README.md` avec les métadonnées disponibles : date, URL, branche, commit Git, objectif, statut et répertoire de travail.

## 3. Préparer la rejouabilité

Crée dans `prompts/` :

- `00-protocole-global.md`
- `01-exploration.md`
- `02-workshop.md`
- `03-maquettes.md`
- `04-validation.md`
- `05-archivage.md`

Enregistre dans `01-exploration.md` le texte complet de cette instruction.

Pour les autres fichiers, utilise uniquement les prompts complets effectivement disponibles dans le contexte ou dans les fichiers du projet.

Si leur contenu exact n'est pas disponible, crée un fichier indiquant `PROMPT À FOURNIR` plutôt que d'inventer une version prétendument identique.

Les fichiers seront complétés au fur et à mesure des étapes.

## 4. Explorer l'application réelle

Utilise un navigateur automatisé, idéalement Playwright, pour accéder à :

[https://test-live.localeo.city](https://test-live.localeo.city)

Tu as aussi des visuels dans le repertoier visuels de la version atuellemement dépoyée avec des exemples d'animations.

L'analyse doit être mobile-first.

Inspecte au minimum :

- L'accueil et la première impression.
- La découverte des animations.
- L'accès depuis un QR code.
- L'inscription et l'authentification.
- La participation à une animation.
- Le suivi des participations.
- La consultation et l'utilisation des lots.
- Le calendrier des animations.
- Le retour dans l'application.


Teste plusieurs tailles d'écran mobile.

Examine également les états vides, erreurs, chargements, redirections et retours arrière.

Si un parcours nécessite des données ou des identifiants de test, signale-le et demande les éléments manquants.

## 5. Analyser le code

Complète l'inspection par une analyse du dépôt, si accessible.

Identifie :

- Les routes.
- Les composants de navigation.
- Les écrans d'animation.
- Les écrans de lots.
- Les composants de calendrier.
- Les mécanismes d'authentification.
- Les composants réutilisables.

Ne confonds jamais ce qui est visible dans le code avec ce qui a été réellement testé dans le navigateur.

## 6. Produire les livrables

Dans `observations/`, crée :

- `cartographie-parcours.md`
- `inventaire-ecrans.md`
- `observations-factuelles.md`
- `limitations.md`

Dans `visuels/captures-avant/`, enregistre les captures réelles.

Pour chaque constat, indique :

- OBSERVÉ : vérifié dans l'application.
- DÉDUIT : issu du code ou de l'analyse.
- HYPOTHÈSE : nécessite une validation terrain.

Associe les observations aux captures et parcours correspondants.

## 7. Contraintes

- Ne modifie aucun code applicatif.
- N'invente aucune observation.
- Ne simule pas encore les experts ou habitants.
- Ne propose pas encore de modifications.
- Ne commence pas le workshop.

## 8. Fin d'étape

Mets à jour le README avec le statut de l'exploration.

Présente :

1. Les parcours réellement inspectés.
2. Les captures réalisées.
3. Les limitations.
4. Les informations éventuellement manquantes.

Arrête-toi et attends mon autorisation de passer à l'étape 2.
