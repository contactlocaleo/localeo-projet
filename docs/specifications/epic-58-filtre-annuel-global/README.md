# Epic 58 - Filtre annuel global Animation

> Suivi produit au 18 septembre 2026 : **À faire** — [backlog de référence](../../roadmap/a-faire/epic-58-filtre-annuel-global-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Etat

`A developper`. Le cadrage et la conception technique sont disponibles ; les
arbitrages doivent etre valides avant l'implementation des tranches concernees.

## Objet

Cette Epic ajoute un contexte annuel global à Localeo Animation, affiché dans
la barre supérieure à côté de la commune active. Il borne les données des vues
pour lesquelles une année d'animation a un sens, sans empêcher l'accès direct
à une animation située hors de l'année sélectionnée.

La valeur initiale est l'année civile courante. Les années antérieures sont
proposées uniquement lorsqu'au moins une animation chevauche l'année concernée.

## Documents

- [Backlog](../../roadmap/a-faire/epic-58-filtre-annuel-global-backlog.md)
- [Conception technique](conception-technique.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Règle temporelle

Une animation appartient à une année si sa période chevauche l'année civile :

```text
animation.date_debut <= fin_annee
ET animation.date_fin >= debut_annee
```

Une animation de décembre 2025 à janvier 2026 est donc visible pour 2025 et
2026. Le filtre ne doit pas se limiter à l'année de `date_debut`.

## Surfaces concernées

- tableau de bord et indicateurs ;
- liste des animations ;
- participants globaux ;
- validations globales ;
- tirages et gains globaux ;
- flyers globaux ;
- bilans consolidés ;
- consommation globale des coffrets gagnés.

## Surfaces hors filtre

- notifications opérationnelles ;
- catalogue des modèles ;
- catalogue des coffrets disponibles ;
- abonnement et support ;
- formulaire de création ;
- détail d'une animation ouverte explicitement par son URL.

Le détail peut rappeler que l'animation est hors du contexte annuel courant,
mais il reste consultable et administrable selon ses permissions et son statut.

## État des API au démarrage

Déjà compatibles avec `date_debut` et `date_fin` :

- `GET /protected/animation-locale/dashboard-performance` ;
- `GET /protected/animation-locale/animations` ;
- `GET /protected/animation-locale/validations` ;
- `GET /protected/animation-locale/bilans`.

À compléter côté backend :

- `GET /protected/animation-locale/participants` ;
- `GET /protected/animation-locale/tirages` ;
- `GET /protected/animation-locale/flyers` ;
- `GET /protected/animation-locale/gains/coffrets/consommation` ;
- découverte paginée ou agrégée des années disponibles.

## Principes

- le filtrage des collections paginées est exécuté par le backend ;
- aucun total ne repose sur une page partiellement filtrée dans le navigateur ;
- les bornes sont exprimées en dates ISO 8601 et interprétées dans le fuseau de
  la commune ou selon la convention temporelle canonique de l'API ;
- l'année est un contexte d'affichage, pas une propriété persistée sur
  l'animation ;
- le changement de commune recharge les années disponibles et revient à
  l'année courante si l'année sélectionnée n'existe plus dans ce contexte.

[Retour à l’index des spécifications](../INDEX.md)
