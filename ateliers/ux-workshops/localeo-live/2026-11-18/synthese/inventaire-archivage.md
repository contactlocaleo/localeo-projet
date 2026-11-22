# Inventaire d’archivage — workshop du 18 novembre 2026

Statut : **PARTIEL**. Exploration réelle, workshop simulé et maquettes sont produits. L’étape 4 a préparé la décision, mais l’utilisateur n’a validé, refusé, reporté ni demandé la révision de B1/C1/D1/E1. L’archivage de l’état est achevé sans clôturer le workshop.

## Prompts et versions

| Fichier | Contrôle |
| --- | --- |
| [00-protocole-global.md](../prompts/00-protocole-global.md) | **PROMPT À FOURNIR** : aucun texte global exact n’a été fourni. Fichier présent, prompt complet manquant. |
| [01-exploration.md](../prompts/01-exploration.md) | Instruction complète de l’étape 1 ; exécutée pour Bouliac après deux [compléments reçus](../prompts/01-complements.md) conservés dans leur formulation exacte. |
| [02-workshop.md](../prompts/02-workshop.md) | Instruction complète de l’étape 2 ; exécutée sous simulation explicitement fictive. |
| [03-maquettes.md](../prompts/03-maquettes.md) | Instruction complète de l’étape 3 ; exécutée pour quatre P1 adoptées. |
| [04-validation.md](../prompts/04-validation.md) | Instruction complète de l’étape 4 ; revue et registre préparés, décisions utilisateur en attente. |
| [05-archivage.md](../prompts/05-archivage.md) | Instruction complète actuelle de l’étape 5 ; archivage exécuté pour le statut partiel. |
| [RELANCER-WORKSHOP.md](../prompts/RELANCER-WORKSHOP.md) | **Nouveau prompt autonome**, rédigé pour une future conversation ; pas un prompt historique prétendu identique. |

**Compléments reçus pendant l’exécution.** L’utilisateur a demandé Bouliac, puis la suppression/recréation des captures avec Bouliac ; leur texte exact et leur effet sont conservés dans [01-complements.md](../prompts/01-complements.md). Une demande ultérieure de relance a créé un dossier `-02`, puis l’utilisateur a expressément demandé sa suppression : ce dossier a été supprimé. L’instruction d’archivage actuelle s’applique donc au dossier conservé `2026-11-18`. Les prompts 01–04 restent les textes complets reçus à leurs étapes ; les compléments ne les ont pas remplacés. Aucun texte 00 complet n’est reconstitué.

## Livrables

| Élément | État et référence |
| --- | --- |
| Observations | Quatre documents dans [observations/](../observations/observations-factuelles.md), dont [limitations](../observations/limitations.md). |
| Captures réelles | 15 PNG Bouliac dans `visuels/captures-avant/` ; tous listés dans le [manifeste](manifeste-visuels.md), référencés par observations, galerie et référence visuelle. |
| Comptes rendus | [Compte rendu des six ateliers simulés](../workshop/compte-rendu.md) et [rapport exécutif](../workshop/rapport-executif.md). |
| Votes | [Registre nominatif](../workshop/votes-et-arbitrages.md) : 144 bulletins simulés, six orientations adoptées, six rejetées ; seuil de sept voix. |
| Backlog | [Backlog UX](../workshop/backlog-ux.md) avec six orientations adoptées, quatre P1. |
| Orientations rejetées | [Alternatives rejetées](../workshop/orientations-rejetees.md). |
| Maquettes | 14 HTML et 28 PNG APRÈS dans `visuels/maquettes-apres/`, tous liés par le [manifeste](manifeste-visuels.md) et la [référence](../visuels/reference-maquettes.md). |
| Galerie comparative | [HTML avant/après](../visuels/comparatif-avant-apres.html), avec 15 captures AVANT conservées sans retouche. |
| Décisions de validation | [Registre](../validation/decisions.md) présent : B1/C1/D1/E1 **EN ATTENTE**, aucune décision utilisateur. |
| Roadmap | [Roadmap commune](../../../../../docs/roadmap/README.md) existante ; aucune intégration spécifique de ce backlog UX non validé. **Travail ultérieur conditionnel**, pas une anomalie de lien. |
| Plan de tests utilisateurs | **Manquant dans ce workshop.** Les critères de recette et scénarios à éprouver figurent dans le backlog, le rapport et la revue ; ils ne constituent pas un plan terrain approuvé ou une étude exécutée. |
| Comparaison précédente | [Synthèse](comparaison-precedent.md) : aucun workshop antérieur disponible dans `docs/ux-workshops/` après la suppression du dossier `-02`. |
| Contrôles | [Contrôle technique des seules maquettes](../visuels/controles/controle-technique.md), empreintes des versions soumises dans [maquettes-soumises.json](../validation/maquettes-soumises.json). |

## Limites de l’archive

- Pas de QR Bouliac valide, d’identité autorisée ni de lot personnel attribué : parcours positif, remise et reprise non éprouvés dans le navigateur.
- État vide réel C1 seulement ; ses maquettes de lot rempli utilisent des données fictives. Les confirmations B1 et avis habitants du workshop sont simulés.
- Les notes heuristiques et votes ne sont pas des mesures de terrain ; la charge de 10 000 habitants n’a pas été testée.
- Aucune décision utilisateur B1/C1/D1/E1 et aucun développement. La roadmap et un plan de tests utilisateurs restent à préparer selon les décisions, sans les attribuer rétroactivement à cette exécution.

L’archive des éléments disponibles est complète **avec ces manques déclarés** ; elle ne représente pas une validation UX finale.
