# Respect de l'architecture pendant le développement

Ce document rend vérifiables les principes existants ; il ne remplace ni les
conventions ni les ADR acceptées. Il s'applique aux évolutions du backend et à
leurs impacts identifiés sur les autres applications.

## Sources et preuves attendues

| Changement | Source à lire | Preuve dans le code et la revue |
| --- | --- | --- |
| Règle métier, état, éligibilité | [Architecture, couches](architecture-solution.md), [ADR domaine d'abord](../decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md) | Agrégat/objet-valeur/service pur propriétaire ; invariant et transition testés sans ORM, UoW ni fournisseur ; orchestration testée séparément. |
| Nouveau concept ou déplacement | [Domaines fonctionnels](domaines-fonctionnels.md) | Domaine propriétaire explicite ; imports consommateurs migrés ensemble ; aucune façade historique pérennisée par commodité. |
| API ou contrat public | [API et OpenAPI](conventions-api-openapi.md), [sécurité](conventions-securite.md) | Exposition, domaine, schémas et contrôles d'accès cohérents ; route fine ; tests de contrat et de refus ; impacts sur les consommateurs identifiés. |
| Action sensible, paiement, notification | [Sécurité](conventions-securite.md), [architecture](architecture-solution.md) | Périmètre d'accès, audit, transaction et idempotence vérifiés ; outbox et ports existants réutilisés ; scénario répété/échec testé selon le risque. |
| Écran ou commande ERP | [Back-office](conventions-backoffice.md) | Navigation rattachée au domaine ; invariants identiques aux API/batchs ; ORM réservé aux responsabilités techniques des vues et adaptateurs. |
| Email système | [Charte email](charte-emails-localeo.md) | Rendu commun, échappement, QR/liens/texte conservés ; tests et aperçus adaptés, sans envoi réel implicite. |
| Persistance ou intégration | [Architecture](architecture-solution.md), [guide opérateur](../../exploitation/technique/reference-guide-exploitation-plateforme.md) | Ports et mapping explicites, migrations additives/checksums préservés, documents binaires hors base selon leur contrat ; tests d'adaptateurs, pas d'accès à une base d'exploitation. |

Avant de coder, identifier les invariants et transitions avant les endpoints et
services applicatifs. Une correction courte peut le faire dans son plan/compte
rendu ; une nouvelle Epic le fait dans sa conception. Ne pas générer de document
supplémentaire sans besoin.

La question de revue centrale reste : « Cette condition doit-elle rester vraie
quel que soit le point d'entrée ? » Si oui, elle appartient au domaine. Une
projection de lecture ou un contrôle technique d'orchestration n'est pas déplacé
artificiellement dans une entité. SQLAdmin reste un adaptateur couplé aux ORM.

## Contrôles exécutables

Depuis la racine de `localeo-backend`, dans son environnement Python :

```bash
python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q
```

Le même groupe est une étape explicite, sans `continue-on-error`, du workflow
`Tests` sur Python 3.12 et 3.14. Les tests de régression complets restent conservés.

| Contrôle existant ou renforcé | Ce qu'il vérifie | Limite |
| --- | --- | --- |
| `tests/architecture/test_module_contracts.py` : imports | Imports statiques absolus, relatifs, `from app import infrastructure`, imports locaux et conditionnels ; frameworks, couches sortantes, configuration runtime, drivers/clients réseau/providers/rendu interdits dans le domaine. | Pas un graphe transitif, pas une analyse d'imports dynamiques ni des effets d'E/S de tout code Python. Ne prouve pas la pureté métier. |
| Même fichier : agrégats protégés | Affectations directes des statuts/attributs explicitement recensés, avec exceptions de projection ciblées. | Liste de fichiers/variables précise, pas une analyse de tous les agrégats ou alias. L'étendre pour une nouvelle transition protégée ; revoir les mutations manuellement. |
| `tests/domain/test_domain_dedicated_classes.py` | Recensement des classes publiques du domaine et des tests dédiés déclarés. | La présence d'un test ne prouve pas sa valeur métier. |
| `tests/application/use_cases/test_use_case_business_test_coverage.py` | Classe de test dédiée aux use cases publics exposant `execute` et refus des anciens placeholders connus. | N'analyse pas la pertinence complète des assertions et ne couvre pas tous les services par convention de nom. |

Les imports de la façade de logs historique `app.observability` restent hors de
la liste interdite ; cela n'autorise pas de nouvelles dépendances techniques dans
le domaine. Les imports dynamiques ne sont pas une échappatoire aux principes.

Ajouter des tests ciblés de comportement après ces contrôles. Le succès d'un
garde-fou, d'un import ou de `py_compile` ne remplace jamais un scénario métier.
Les fakes simulent les ports et ne recopient pas l'algorithme que le test doit vérifier.

## Dette et exceptions

Corriger le placement d'une règle historique quand on la modifie, sans lancer
une refonte globale hors périmètre. Un couplage ORM voisin n'est pas une
autorisation de l'étendre.

Une exception nécessaire est décrite dans la conception technique ou un ADR :
principe concerné, raison, fichiers/périmètre exacts, risque, tests compensatoires
et condition de résorption. Ne pas ajouter une exclusion large, un `skip` ou
affaiblir un test pour masquer une régression. Une nouvelle décision qui change
la cible doit être explicite ; une correction conforme au périmètre autorisé ne
requiert pas une approbation supplémentaire par principe.

## Revue et protection des fusions

Le [modèle de PR](../../../../localeo-backend/.github/pull_request_template.md) demande les documents
appliqués, le placement des règles, les preuves et les écarts. Pour une tâche sans
PR, fournir ces éléments brièvement dans le compte rendu. Utiliser « sans objet »
avec une raison pour les éléments non concernés.

Les fichiers CI font échouer le workflow en cas de violation ; **empêcher la
fusion** exige aussi que les statuts correspondants du workflow `Tests` soient
obligatoires dans les règles de protection GitHub de la branche. Identifier les
noms exacts après une exécution du workflow et conserver les protections déjà
en place. Cette configuration distante n'est pas appliquée par ce document.

## Découverte du guide par les agents

Dans `localeo-backend`, `AGENTS.md` renvoie à `AGENT.md`, référence technique locale, et au guide transverse de `localeo-projet`.
Codex recherche le nom standard `AGENTS.md` ; un autre nom dépend des noms de
repli configurés. Ce point d'entrée évite une dépendance à la configuration
personnelle d'un développeur, sans dupliquer toutes les instructions.
[Référence officielle](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Dans une nouvelle session ouverte dans le backend, vérifier que le guide est
pris en compte avant l'édition ; les instructions des sous-dossiers restent
applicables. Ce mécanisme facilite la lecture, mais les tests et la revue restent
nécessaires pour vérifier le respect des principes.

## Validation du 18 septembre 2026

La commande de contrôle ci-dessus a été exécutée localement sous Python 3.12 :
**356 tests réussis, 2 contrôles de recensement en échec**. Les nouveaux tests
sur les imports passent, ainsi que les contrats d'architecture existants.
Les 103 liens locaux des guides et documents modifiés ont été vérifiés.

Les deux contrôles en échec sont inchangés par cette livraison ; leur échec a
été reproduit à partir de leur version Git HEAD sur le même arbre de travail :

- Domaine : huit déclarations manquent dans le recensement des tests dédiés :
  `AnimationNonDemarree`, `AnimationTerminee`, `PeriodePilotage`,
  `PublicationJuridiqueInvalide`, `ContenuJuridiqueInvalide`, `FaitsAlertesAchat`,
  `SessionConsultationCoffret`, `SessionConsultationCoffretRepository`.
- Use cases : trois classes de test dédiées manquent dans le recensement :
  `ConsulterRetourPaiement`, `EchangerLienConsultationCoffret`,
  `RenvoyerLienConsultationPublic`.

Cela ne signifie pas que tout comportement de ces classes est dépourvu de
couverture : certains tests fonctionnels existent hors de ce recensement.
Raccorder les tests pertinents et compléter les comportements manquants avant
la mise au vert ; ne pas créer des tests d'import factices ni des exclusions.
Cette dette préexistante n'est pas masquée par le nouveau contrôle CI.

La suite métier complète et la matrice GitHub Python 3.12/3.14 n'ont pas été
réexécutées dans cet environnement pour cette modification. Aucune protection
de branche distante n'a été modifiée.
