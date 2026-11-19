# Roadmap UX issue du workshop — proposition conditionnelle

**Actualisation après décision complémentaire du 19 novembre :** seuils UX02 confirmés à **30 jours sans interaction / 60 jours sans évolution** ; pauses justifiées et dossiers clos exclus des alertes temporelles. UX01–UX05 sont spécifiées et implémentées localement : [conception et preuves dans l’EPIC 71](../../../../specifications/epic-71-crm-prospection/workshop-crm-20261118.md). Les mentions de seuils à définir et d’implémentation non engagée ci-dessous décrivent la préparation antérieure à cette demande explicite.

État au 19 novembre 2026. Cette synthèse ne modifie pas la roadmap produit commune et n’engage aucune implémentation. Les [votes simulés](../workshop/votes-et-arbitrages.md) distinguent adoption de conception et [validation utilisateur](../validation/decisions.md), reçue le 19 novembre pour UX01–UX05, seuils UX02 à définir.

## Avant lancement — P0/P1 validées

**Cinq P1 validées : UX01–UX05.** Aucun P0 démontré. Seuils UX02 à définir ; aucune date de livraison ni recette déduite de cette validation.

| ID | Orientation P1 validée | Vote POUR / 12 | Effort relatif | Condition principale |
| --- | --- | --- | --- | --- |
| [UX01](../validation/dossier-decision.md#ux01) | Rendre visible un résumé quotidien et collectif | 12 | M | Portées et totaux concordants avec les listes. |
| [UX02](../validation/dossier-decision.md#ux02) | Donner accès aux listes de risques du portefeuille | 8 | L | Recetter l’existant ; définir populations/seuils ; traiter les 7 réserves visuelles. |
| [UX03](../validation/dossier-decision.md#ux03) | Clarifier les responsables du prospect, du dossier et de l'action | 12 | S | Vérifier les trois rôles et les permissions ; pas de copie silencieuse. |
| [UX04](../validation/dossier-decision.md#ux04) | Expliciter le rattachement de la prochaine action | 12 | M | Vérifier le cas de deux dossiers et le rattachement explicite. |
| [UX05](../validation/dossier-decision.md#ux05) | Rendre vérifiable la continuité du rendez-vous jusqu'à la prochaine étape | 12 | M | Recetter l’existant de bout en bout, y compris rappels et compte rendu. |

Pour les orientations validées : clarifier les termes de UX03/UX04 avant les agrégations UX01/UX02 ; commencer UX02/UX05 par une vérification des capacités existantes. Toute dépendance à une orientation refusée ou reportée devra être réarbitrée. Les [risques ouverts](../validation/risques-non-resolus.md) et les [tests réels](plan-tests-utilisateurs.md) restent des conditions de préparation à l’usage autonome, même après validation visuelle.

## Après premiers retours — P2

Orientations adoptées en simulation, à confronter aux premiers tests réels puis à soumettre à décision avant planification. Elles ne sont ni validées par l’utilisateur ni maquettées dans cette exécution.

| ID | Orientation | Vote POUR / 12 | Effort relatif | Retour attendu |
| --- | --- | --- | --- | --- |
| [UX06](../workshop/backlog-ux.md#ux06) | Alléger visuellement la création sans retirer les règles métier | 9 | M | Charge de saisie et conservation des règles. |
| [UX07](../workshop/backlog-ux.md#ux07) | Remplacer la valeur null dans la dernière interaction | 12 | S | Compréhension des états vides et distinction des erreurs. |
| [UX08](../workshop/backlog-ux.md#ux08) | Faciliter le retour aux résultats filtrés | 7 | M | Retour aux résultats, filtres et focus conservés. |
| [UX09](../workshop/backlog-ux.md#ux09) | Rendre la transmission d'un dossier explicite | 10 | M | Transmission et engagements restants compris à deux comptes. |
| [UX10](../workshop/backlog-ux.md#ux10) | Expliquer la qualification et les statuts au point d'usage | 10 | S | Distinction du potentiel, de l’étape et de la priorité. |

## Évolutions futures — P3

**Aucune P3 adoptée.** UX12 (répartition automatique des prospects) et UX13 (qualification exhaustive obligatoire) sont P3 mais rejetées en simulation ; elles ne sont pas réintroduites dans la roadmap. Un besoin futur devra être étayé et revoté, puis validé explicitement. UX11, P2 rejetée, est également exclue ; voir les [orientations rejetées](../workshop/orientations-rejetees.md).

## Pilotage des décisions

Validées : 5 ; à réviser : 0 ; reportées : 0 ; refusées : 0 ; en attente : 0 P1. Seuils UX02 à définir. Ces zéros ne signifient pas approbation tacite. Les 3 rejets simulés ne sont pas des refus utilisateur.

Les efforts S/M/L du workshop ne sont pas des devis. Aucun responsable ni calendrier n’est attribué. Le [backlog potentiel](../validation/backlog-implementation-potentiel.md) conserve critères, dépendances et modalités de suite ; seule une demande ultérieure peut engager une implémentation.
