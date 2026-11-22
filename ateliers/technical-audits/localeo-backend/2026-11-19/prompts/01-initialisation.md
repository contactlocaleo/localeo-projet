# ÉTAPE 1 — INITIALISATION ET CARTOGRAPHIE PERFORMANCE LOCALEO BACKEND

Tu es l'architecte orchestrateur d'un audit multi-agents des performances du backend Python Localeo.

## Objectif

Identifier les risques de saturation CPU, mémoire, concurrence, persistance et latence API, en privilégiant des optimisations ciblées, sans breaking change ni refactoring majeur.

Le code source complet est disponible dans le workspace Codex.

**Son inspection directe est obligatoire. Aucun diagnostic générique ne sera accepté.**

## 1. Préparer le répertoire

Détermine la date locale au format YYYY-MM-DD.

Crée :

`docs/technical-audits/localeo-backend/YYYY-MM-DD/`

En cas de doublon, ajoute -02, -03, etc.

Crée les dossiers :

- `prompts/`
- `inventaire/`
- `agents/`
- `contradiction/`
- `benchmarks/`
- `recommandations/`
- `validation/`
- `synthese/`

Crée un README contenant les métadonnées disponibles : date, branche, commit, stack, configuration et statut.

Archive ce prompt complet dans `prompts/01-initialisation.md`.

## 2. Explorer la stack réelle

Identifie :

- Version Python.
- Framework web.
- Serveur ASGI/WSGI.
- Workers et modèle de concurrence.
- Bibliothèques principales.
- ORM et moteur de persistance.
- Gestion des transactions.
- Tâches de fond.
- Intégrations externes.
- Caches.
- Ressources CPU et mémoire.
- Configuration des conteneurs.
- Observabilité disponible.

Ne présuppose aucune technologie non vérifiée.

## 3. Cartographier les API et les flux métier

Explore directement les routes, handlers, services, repositories et dépendances.

Identifie les flux critiques :

1. Validation QR.
2. Participation à une animation.
3. Consultation des animations.
4. Tableau de bord organisateur.
5. Gestion des commerçants.
6. Import de commerçants.
7. Clôture et tirage au sort.
8. Consultation des résultats.
9. Autres flux significatifs identifiés dans le code.

Pour chaque flux, reconstitue :

Endpoint → Handler → Services → Persistance → Traitements → Réponse.

Documente les fichiers, fonctions et lignes concernés.

## 4. Préparer les agents

Définis six missions indépendantes :

- CPU et algorithmes.
- Mémoire et allocations.
- Async et concurrence.
- Persistance.
- Performance API.
- SRE et capacité.

Chaque agent devra examiner le code source lui-même.

Chaque agent devra produire **cinq constats majeurs au maximum dans son rapport principal**, classés par impact probable.

Les observations supplémentaires seront placées en annexe.

Définis un format commun de restitution pour faciliter la consolidation.

## 5. Préparer la consolidation transverse

Identifie les flux métier qui devront être analysés de bout en bout.

Prévois un mécanisme permettant de :

- Regrouper les anomalies liées à une même cause racine.
- Éviter les tickets redondants.
- Distinguer les symptômes des causes.
- Identifier les API impactées par une même anomalie.
- Prioriser selon l'impact métier et technique.

## 6. Livrables

Crée :

- `inventaire/architecture.md`
- `inventaire/stack-technique.md`
- `inventaire/catalogue-api.md`
- `inventaire/flux-critiques.md`
- `inventaire/configuration-ressources.md`
- `inventaire/limitations.md`
- `inventaire/plan-orchestration-agents.md`

## 7. Contraintes

Aucune modification du code applicatif.

Aucun test de charge en production.

Aucune migration ni déploiement.

Aucun secret dans les livrables.

Ne réalise pas encore les audits spécialisés.

Présente le plan d'orchestration et attends mon autorisation.
