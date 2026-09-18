# Backlog Epic 58 - Filtre annuel global Animation

> État produit commun : **À faire**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthèse

- Statut : `A developper - cadrage initialise, arbitrages et implementation a realiser`.
- Criticité : `Moyenne`.
- Applications : `Backend Localeo` et `Localeo Animation`.
- Dépendances : Epic 41 et conventions API Animation.

Voir le [cadrage](../../specifications/epic-58-filtre-annuel-global/README.md), la
[conception](../../specifications/epic-58-filtre-annuel-global/conception-technique.md)
et le [registre](../../specifications/epic-58-filtre-annuel-global/registre-arbitrages.md).

## Tranche A - Contrats et moteur backend

- valider les arbitrages `ANN-ARB-01` à `ANN-ARB-10` ;
- définir la sémantique canonique de chevauchement et le fuseau ;
- exposer les années disponibles pour la commune active ;
- ajouter `date_debut` et `date_fin` aux participants globaux ;
- ajouter `date_debut` et `date_fin` aux tirages globaux ;
- ajouter `date_debut` et `date_fin` aux flyers globaux ;
- ajouter `date_debut` et `date_fin` à la consommation globale des gains ;
- vérifier et aligner Dashboard, Animations, Validations et Bilans ;
- filtrer avant pagination et avant calcul des agrégats ;
- documenter les contrats dans l'OpenAPI et ajouter les index nécessaires.

## Tranche B - Contexte annuel Localeo Animation

- créer le provider ou état global annuel au niveau de `App` ;
- charger les années depuis le backend ;
- ajouter le sélecteur accessible dans `TopBar` à côté de la commune ;
- initialiser l'année courante ;
- synchroniser l'année avec l'URL et le stockage local ;
- conserver le paramètre pendant les navigations ;
- gérer le changement de commune et les erreurs de chargement.

## Tranche C - Raccordement des vues

- raccorder Dashboard et adapter son filtre de période ;
- raccorder Animations et intersecter les champs `Du/Au` ;
- raccorder Participants et ses KPI ;
- raccorder Validations ;
- raccorder Tirages et gains ;
- raccorder Flyers ;
- raccorder Bilans ;
- raccorder la consommation globale des coffrets ;
- contextualiser les états vides ;
- vérifier que les détails et vues hors périmètre restent inchangés.

## Critères d'acceptation

- l'année courante est sélectionnée par défaut ;
- seules les années historiques contenant une animation sont proposées ;
- une animation chevauchant deux années apparaît dans les deux contextes ;
- chaque collection paginée est filtrée côté backend ;
- les totaux et KPI correspondent à l'ensemble annuel, pas à la page chargée ;
- le filtre survit à la navigation et au rechargement ;
- un changement de commune ne conserve pas une année invalide ;
- une animation hors année reste accessible par lien direct ;
- notifications, modèles, coffrets disponibles, abonnement et support ne sont
  pas affectés ;
- aucune régression sur les appels sans bornes temporelles ;
- les erreurs exposent leur `correlationId`.

## Recette transverse

- commune sans animation historique ;
- commune avec plusieurs années ;
- animation située sur une année ;
- animation traversant le 31 décembre ;
- navigation sur toutes les vues concernées ;
- retour navigateur et lien partagé contenant `annee` ;
- changement de commune ;
- comparaison des totaux API et UI ;
- contrôle des performances avec pagination et agrégats.


## Références complémentaires des interfaces

- Animation : [cadrage](../../specifications/epic-58-filtre-annuel-global/README.md)
- Animation : [conception](../../specifications/epic-58-filtre-annuel-global/conception-technique.md)
- Animation : [registre](../../specifications/epic-58-filtre-annuel-global/registre-arbitrages.md)
