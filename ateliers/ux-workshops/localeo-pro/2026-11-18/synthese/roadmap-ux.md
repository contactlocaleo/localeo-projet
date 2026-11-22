# Roadmap UX conditionnelle — Localeo Pro

18 novembre 2026. Projection du workshop, actualisée après la réponse utilisateur : B1, C1, D1, E1 et F1 sont **VALIDÉES** dans le [registre](../validation/decisions.md) et suivies par [E80](../../../../../docs/roadmap/en-cours/epic-80-fiabilite-parcours-localeo-pro-backlog.md). Cette projection ne remplace pas la roadmap canonique du projet et ne décide d'aucun déploiement.

## Avant lancement — P0/P1 validées

**Cinq orientations P1 validées par l'utilisateur : B1, C1, D1, E1 et F1.** Aucun P0 produit n’a été établi. Les conditions de fonctionnement du rapport restent ouvertes et leur réalisation est suivie dans E80.

Les cinq P1 ci-dessous ont reçu une décision explicite sans condition supplémentaire ; leur état de réalisation et leurs preuves figurent dans le [bilan E80](../../../../../docs/specifications/epic-80-fiabilite-parcours-localeo-pro/verification-livraison.md) :

| Orientation validée | Effort relatif | Dépendance principale | Preuve attendue |
| --- | --- | --- | --- |
| B1 · scan et résultats | M | QR autorisés, états et reçu existants | Validation réelle de test, doublon, refus, incertitude ; un seul effet, résultat conforme. |
| C1 · information/action | M | État d’action actuel et autorisé | Lire ne termine pas une tâche ; action retrouvable et lien au bon contexte. |
| D1 · dates/états/préparation | L | Diagnostic du 2/3 et règles de période | Même périmètre/instant cohérent, prochains gestes conformes aux responsabilités. |
| E1 · kit et logistique | M | Fichier réel, effets du téléchargement et dates | Ouverture, impression, QR et consignes vérifiés ; déclaration prêt distincte. |
| F1 · reprise fiable | L | B1 pour le résultat ; session et état courant | Avant/après envoi, expiration, retour différé ; pas de rejeu automatique. |

[Lots potentiels détaillés](../validation/backlog-implementation-potentiel.md). B1/F1 partagent une recette ; D1 doit être diagnostiqué avant de diffuser une présentation d’état vers C1/F1 ; E1 dépend du contenu réel. Aucun ordre de sprint décidé.

## Après premiers retours — P2 et ajustements

| Orientation adoptée par simulation | Vote | Statut utilisateur | Suite possible |
| --- | --- | --- | --- |
| A1 · bon accès Pro et rôle expliqué | 11 / 0 / 1 | Non soumise dans le lot P1 ; aucune validation ni report utilisateur | Vérifier les supports de diffusion, tester une aide courte à la demande si nécessaire. Le contrôle du bon accès peut rester une condition opérationnelle avant campagne. |
| G1 · alléger les répétitions en gardant les repères | 10 / 0 / 2 | Non soumise dans le lot P1 ; aucune validation ni report utilisateur | Observer recherche d’information et retour après absence avant toute suppression de contenu. |

Les ajustements issus du [plan de tests](plan-tests-commercants.md) seront qualifiés par leurs preuves et soumis à décision. Un blocage essentiel découvert devra être reclassé selon son impact ; il ne sera pas repoussé mécaniquement après lancement au motif qu’il vient d’un test tardif.

B2, D2, E2 et G2 étaient des propositions P2 rejetées par le vote simulé : elles ne sont pas des travaux différés à réactiver automatiquement.

## Évolutions futures — P3

**Aucune P3 adoptée à inscrire.** A2 (tutoriel obligatoire) et C2 (push quotidien sur non-lus), classées P3 dans les propositions, ont été rejetées. Leur existence dans les archives ne constitue pas un backlog futur accepté. De nouveaux besoins de confort devront être étayés, priorisés et décidés séparément.

F2, proposition P1 de succès hors connexion, est également rejetée et exclue de tous les horizons. Le besoin de continuité réseau reste traité comme risque ouvert dans B1/F1.

## Conditions de suivi

- Toute ligne validée doit conserver sa référence de maquette, les conditions utilisateur et les preuves à produire. Une décision UX n’autorise pas automatiquement son implémentation.
- Une ligne à réviser attend une nouvelle proposition ; une ligne reportée conserve le déclencheur éventuel exprimé, sans date inventée ; une ligne refusée reste archivée sans réalisation.
- [Risques ouverts](../validation/risques-ouverts.md) : R01 à R05 concernent les parcours essentiels ; R06/R07 l’accès, les tâches et les canaux promis. Aucun risque n’est levé à l’archivage.
- Les chiffres « 2/1 » des maquettes sont illustratifs. Aucun problème n’est déclaré corrigé par sa seule représentation APRÈS.
