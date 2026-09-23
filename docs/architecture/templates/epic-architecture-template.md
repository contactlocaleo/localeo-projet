# Architecture applicative EPIC XX - Nom

Utiliser ce modèle dans la spécification canonique selon le [cycle d'epic](../../organisation/cycle-epic.md). Adapter les liens après copie et réutiliser les critères du backlog. Les sections sans objet sont justifiées ; une petite correction ne nécessite pas tous ces développements.

## Statut

- Version :
- Source backlog :
- Portee :
- Hors portee :
- Applications et contrats concernés :
- État produit : lien vers la roadmap courante, sans état parallèle dans ce document.

## Objectif applicatif

Ce que l'architecture doit permettre.

## Comportements et critères d'acceptation

Relier les critères identifiés dans le backlog aux parcours nominaux et refus significatifs : acteur, préconditions, action, résultat observable, effets conservés ou interdits. Décrire l'existant vérifié et le comportement cible. Distinguer hypothèses et arbitrages acquis.

## Choix d'architecture

Decisions structurantes prises pour repondre a l'EPIC.

## Objets manipules ou crees

Objets metier, projections, tokens, evenements, documents, batchs, etc.

## Modele de domaine

### Agregats et entites

Pour chaque agregat modifie, indiquer sa racine, les objets qu'il protege et les operations metier exposees.

### Invariants et transitions

Lister les regles qui doivent rester vraies quel que soit le point d'entree, puis identifier leur porteur :
entite, objet-valeur ou service de domaine pur. Decrire les transitions de statut autorisees et refusees.

### Responsabilites applicatives

Limiter cette section au chargement des objets, au controle du perimetre d'acces, a la transaction, aux ports,
a la persistance et aux effets secondaires. Toute regle metier conservee dans cette couche doit etre justifiee.

Verification obligatoire : la conception respecte
l'[ADR domaine d'abord](../decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md).

## Vue applicative

Diagramme Mermaid : surfaces, use cases, domaines, dependances.

## Flux principaux

1 a 3 flux Mermaid maximum, seulement si utile.

## Frontieres avec les autres domaines

Ce que l'EPIC possede, consomme ou ne doit pas dupliquer.

## Contrats et compatibilité

Identifier producteur, source canonique, générateurs et consommateurs réels. Décrire les champs, erreurs et droits modifiés, la compatibilité avec les versions existantes et l'ordre de livraison si plusieurs applications évoluent ensemble. Lier les contrats sans recopier leurs schémas complets.

## Données, démonstration et migrations

Décrire la persistance affectée, la migration des données existantes et la reprise en cas d'échec. Identifier les adaptations du générateur de démonstration, des fixtures et de la restauration ; préciser les scénarios à tester. Justifier une absence d'impact plutôt que la supposer.

## Securite / audit / idempotence

Seulement si concerne.

## Preuves et impacts documentaires

Reprendre la matrice du [cycle d'epic](../../organisation/cycle-epic.md) : critère, comportement et propriétaire, test/scénario prévu, résultat réel, documentation fonctionnelle et contrat, démonstration, exploitation et livraison. Les contrôles statiques ne remplacent pas les preuves métier ; les tests prévus ne sont pas des tests réussis.

## Exploitation et livraison

Identifier les procédures à actualiser, les configurations requises sans secrets, l'ordre des migrations, les diagnostics, les vérifications après livraison et la reprise applicable. Référencer les documents canoniques ; ne pas annoncer une recette ou un déploiement non exécuté.

## Points ouverts

Decisions restantes, risques, arbitrages futurs.
