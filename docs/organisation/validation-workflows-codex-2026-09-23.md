# Mise en place et validation des workflows Codex — 23 septembre 2026

Le [guide d'usage](utiliser-workflows-codex.md) est l'entrée opérationnelle. Ce bilan est daté : il ne remplace pas une exécution de contrôle sur un changement ultérieur.

## Livré dans les cinq dépôts

- Projet : six nouveaux skills (cadrage, spécification, implémentation, correctif, démonstration, livraison), en complément des deux existants ; cycles canoniques, modèles et guide d'usage.
- Projet : hooks Codex de début/fin bornés, installation Git locale préservant les hooks existants, contrôle incrémental des Markdown fonctionnels/ops et de leurs liens entrants après suppression.
- Projet : profils qualité, rapports liés aux versions testées, manifeste de préparation et CI documentaire locale/workspace.
- Backend : jobs architecture/régressions indépendants, tests dédiés manquants et compatibilité PostgreSQL du générateur réellement exécutée.
- Marketplace : CI à quatre jobs indépendants (lint, contrats sensibles, serveur/build isolé, navigateur), gate de synthèse et modèle de PR.
- Animation et Commerçant : routage vers les workflows et modèles de PR ; les pipelines applicatifs existants sont conservés.

## Preuves locales

| Contrôle | Résultat observé |
| --- | --- |
| Validateur officiel de skills | Les huit skills passent ; PyYAML installé uniquement dans `.artifacts/skill-validation-deps`, ignoré, sans changement de l'environnement global |
| Contrôles de découverte/contextes et hooks | Métadonnées et budgets vérifiés ; commandes Windows exécutées via PowerShell et cmd depuis un sous-dossier ; tests de refus des configurations vides/non scalaires |
| Hook Git | Installation locale activée dans `localeo-projet` ; aucune configuration globale modifiée ; exécution réelle et refus vérifiés dans un dépôt temporaire |
| Backend architecture et nouveaux tests | 453 tests ciblés réussis ; assertions de recensement inchangées, tests dédiés pour huit classes de domaine et trois use cases |
| Backend runner démo et applicatif ciblé | 24 tests réussis |
| Générateur sur PostgreSQL 18 | Cinq tests réels réussis, zéro skip : migrations, génération, inventaire, lecteurs métier et droits, transfert, reset, échec injecté, restauration et évolution du schéma |
| Marketplace | 82 tests contrats sensibles et 12 tests serveur réussis ; build isolé et lint des fichiers Git suivis réussis |
| Marketplace navigateur local | 189 scénarios découverts ; smoke borné à 60 secondes : un réussi et quatre non exécutés, sortie 1 au timeout/teardown ; aucun succès global revendiqué |

Les tests PostgreSQL ont utilisé deux clusters temporaires locaux, arrêtés après exécution ; aucune base d'exploitation n'a été utilisée. Deux avertissements SQLAlchemy de réflexion de `dialect_options` restent visibles. Le rapport JUnit reste dans le dossier ignoré `localeo-backend/tmp/demo-compatibility.xml` et le workflow CI le conserve comme artefact.

Les outils documentaires et qualité sont testés sur des dépôts Git temporaires : preuves absentes/partielles/périmées, modification du code ou du registre pendant les contrôles, commande indisponible/échouée, environnement et dépôt manquants. Le profil documentaire workspace fournit le rapport local ignoré `.artifacts/quality/documentation.json`. Le test de symlink du synchroniseur documentaire est ignoré sur le Windows local lorsque la création de liens est interdite ; cette limite ne concerne pas les cinq tests PostgreSQL.

## Mise à l'épreuve des workflows

Ces essais sont des revues de comportement en lecture seule ; ils ne constituent pas des livraisons produit :

1. Besoin « sas de validation des prestations » : le workflow de cadrage retrouve Epic 62 et ses index, conserve son état à faire et ses arbitrages ouverts. Aucun doublon créé, aucune ancienne epic rouverte.
2. Revue indépendante du correctif « GET participants répond 409 sans édition après génération » : sélection du workflow correctif, distinction version signalée/arbre local, recherche de reproduction et du propriétaire de règle. Les cas attendus incluent lecture sans édition, répétition sans mutation, refus d'accès et maintien du contrôle après une vraie modification pertinente. Aucun correctif fictif ni suppression du contrôle de concurrence demandé par le skill.
3. Revue indépendante de livraison « tests verts avant une nouvelle modification, PostgreSQL non exécuté » : preuves devenues périmées et contrôle manquant doivent rester explicites. Les tests de l'outil qualité vérifient effectivement le refus des preuves anciennes ou partielles.

La revue a conduit à préciser les profils de livraison et les rapports distincts, à refuser les définitions de hooks vides et métadonnées non scalaires, à vérifier l'exécution réelle du hook Git et à supprimer la double expansion PowerShell des commandes Windows.

Pour les prochains essais, conserver le besoin et les versions des sources, relever les erreurs/omissions et reprises nécessaires, puis corriger uniquement les instructions en cause. Aucun gain de temps ou de tokens n'est chiffré sans mesure comparative.

## Activation et limites restantes

- La confiance native des hooks Codex se valide dans `/hooks` sur la définition exacte ; les commandes testées seules ne prouvent pas cette activation dans le client.
- Les workflows GitHub doivent être publiés puis exécutés. Le contrôle documentaire transverse exige cinq SHAs et un accès privé en lecture `LOCALEO_WORKSPACE_READ_TOKEN`. Les protections de branche se configurent avec les noms réels des jobs, selon le [guide de livraison](preparer-livraison.md).
- La suite backend complète et les matrices Linux/Python CI n'ont pas été rejouées localement. La Marketplace présente un blocage local Playwright/teardown déjà documenté ; son job Linux reste à exécuter. ESLint sur tout le disque local rencontre des permissions sur des dossiers temporaires non versionnés.
- Aucun déploiement, aucune validation de fournisseur réel, aucun commit ni push ne sont réalisés au titre de cette mise en place. Un manifeste préparatoire n'atteste pas la disponibilité d'une cible réelle.
