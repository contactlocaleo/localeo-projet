# Suivi des audits spécialisés

Autorisation : prompt utilisateur de l’étape 2, archivé dans [02-agents.md](../prompts/02-agents.md). Consolidation non autorisée.

Référence backend au lancement : branche `main`, commit `7049e7fafc76f9119924f1082a5ee7457a175d85`, arbre propre. Référence documentaire : `f437465c577d3754b8743c6c48519f0d7606613e`. Le dossier utilisateur `docs/ux-workshops/localeo-crm/` est déjà présent et n’appartient pas à cette tâche.

Véritables sous-agents Codex avec contexte séparé : `fork_turns=none`. Ils reçoivent seulement leur mission, les contraintes et les chemins vers la cartographie. Les conclusions et messages des autres spécialistes ne leur sont pas transmis. Les rapports et annexes leur sont attribués exclusivement. Aucun serveur, port, base temporaire, build ni profiler partagé n’est alloué.

Le prévol des missions CPU et mémoire confirme cette fois un accès réel au shell et la lecture directe de fonctions du backend. La limite d’outillage signalée lors de l’étape 1 ne s’applique donc pas à ces deux missions. Les autres prévols seront consignés après leur exécution.

Ordre initial : CPU + mémoire, concurrence + persistance, API + SRE. Lancement glissant ensuite, avec trois spécialistes au maximum pendant la finalisation des rapports précédents, soit quatre créneaux avec l’orchestrateur. L’orchestrateur contrôle chaque rapport après sa première finalisation : champs de preuve, maximum de cinq anomalies, classement, références aux sources, limites et compatibilité des corrections proposées. Ce contrôle de qualité ne constitue pas une consolidation transverse ; aucun registre de causes communes ni ticket n’est alimenté.

Prévols suivants confirmés : concurrence (`main.py`, `application_lifespan`, ligne 169), persistance (`db.py`, `construire_options_pool`, ligne 33), API (`main.py`, montages des routeurs). Les deux premiers rapports ont reçu uniquement des corrections documentaires de préfixes exposés et des liens de preuve après leur finalisation indépendante ; ces retouches sont mentionnées à leur fin.

Prévol SRE confirmé : `db.py`, `construire_options_pool`, lignes 33–44, et `SchedulerCoordinator._execute_schedule`, lignes 160–171. Les six prévols ont donc réussi avec lecture effective des sources. Les six premières analyses et leurs annexes ont été finalisées indépendamment ; voir [le contrôle final](etape-2-verification.md). Aucun sous-agent de repli n’a été nécessaire.

Aucun benchmark, profilage, test de charge, migration, déploiement, refactoring ou changement applicatif autorisé ou exécuté pour ces missions. Les vérifications documentaires restent permises.
