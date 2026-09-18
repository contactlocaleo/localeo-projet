---
name: localeo-invariants
description: Concevoir, modifier ou revoir une règle métier Localeo, une transition d'état ou un contrat API partagé entre backend, ERP, batchs et frontends. Utiliser pour vérifier le propriétaire d'une règle et ses preuves de comportement. Ne pas déclencher pour une retouche visuelle ou rédactionnelle sans effet métier.
---

# Invariants et contrats Localeo

Lire le [guide transverse](../../../AGENTS.md), les instructions du dépôt touché et seulement la spécification pertinente. Consulter la [matrice des preuves](../../../docs/architecture/transverse/controle-architecture.md) ; ne pas charger tous les epics.

1. Formuler l'invariant et son déclencheur observable : « dans tel état et avec ces droits, cette opération doit réussir/refuser, même si elle est répétée ». Identifier l'agrégat ou objet-valeur propriétaire avant de choisir la route ou le service. Distinguer état métier, projection de lecture et contrôle technique.
2. Tracer les entrées réellement concernées : API, SQLAdmin, batch, webhook, interface. Lire les imports et appels concrets, pas seulement les noms de fichiers. Le domaine décide ; l'application orchestre transaction et ports ; les adaptateurs traduisent ; l'interface présente. Une dette voisine ne justifie pas sa propagation.
3. Pour une modification d'API, identifier producteur, schéma canonique, générateur, contrat embarqué et consommateurs effectifs. Vérifier champs obligatoires, erreurs, accès, pagination ou idempotence selon le changement. Ne pas recréer un contrat supprimé ni en changer la source sans comprendre les consommateurs et le périmètre autorisé.
4. Choisir une preuve comportementale proportionnée : cas nominal et refus significatif ; répétition/échec pour les effets sensibles ; test de frontière si plusieurs entrées appliquent la même règle. Utiliser le runner isolé décrit par le backend. Pas de base d'exploitation, notification réelle ou secret chargé implicitement par un test.
5. Exécuter les contrôles d'architecture si les couches, imports ou agrégats changent, puis les tests ciblés. Les tests statiques ne prouvent ni pureté transitive ni couverture métier complète. Ne pas créer de tests d'import factices, d'exclusion large ou de skip pour masquer un échec.
6. Rapporter règle, propriétaire, entrées affectées et résultats : réussi, échoué, non exécuté. Une dette préexistante est étayée, pas supposée. Une exception décrit motif, périmètre, risque, preuve compensatoire et condition de résorption dans le support existant ; elle n'impose pas une nouvelle approbation pour une correction déjà autorisée.

Une revue indépendante peut être confiée à `localeo-invariant-reviewer` et, pour un contrat partagé, à `localeo-contract-reviewer`. Leur fournir le diff ou les fichiers précis et attendre des constats avec chemins, scénarios et limites. L'agent principal décide des corrections et les vérifie.
