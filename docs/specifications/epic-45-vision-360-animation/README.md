# Specification technique - Epic 45 Vision 360 Animation

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-45-vision-360-animation-backend-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Etat

Socle backend realise le 2026-08-19. L'extension des cinq indicateurs economiques et d'usage est specifiee le 2026-08-28 dans le contrat cible, mais son implementation et sa recette restent a realiser.

## Architecture

La Vision 360 est une couche d'agregation en lecture sur les donnees de l'Epic 41. Elle ne possede ni table analytique ni source de verite propre. La migration `v169` ajoute uniquement une reference metier immutable et les index de lecture.

## Securite

- `ADMIN` : acces plateforme et coordonnees completes sur demande explicite ; la consultation est auditee.
- `EXPLOITATION` : acces limite aux communes de `admin_commune_ids`, coordonnees toujours masquees.
- autres profils et sessions absentes : acces refuse.

## API

Le contrat est disponible dans `openapi.json`. Les routes sont montees sous `/internal/animation-locale/vision-360` : recherche, synthese, indicateurs, chronologie, participants et alertes.

La route d'indicateurs accepte `horizon_expiration_jours` entre 1 et 365, avec 30 par defaut. Elle expose dans `consommation_financiere` :

- le montant reinjecte et le montant potentiel restant a reinjecter, en centimes et en EUR ;
- le nombre de coffrets entierement non consommes expirant dans l'horizon retourne ;
- le delai moyen entre l'envoi du gain et sa premiere consommation, avec la taille de l'echantillon ;
- le nombre de commercants participants effectifs sans validation, avec le denominateur ;
- la repartition du montant reinjecte par commercant.

Les definitions opposables, populations, exclusions et cas limites sont celles de [l'Epic 41](../epic-41-api/indicateurs-economiques.md). Ces valeurs couvrent le cycle de consommation complet des gains de l'animation jusqu'a `generated_at`; le filtre d'analyse ne doit pas supprimer une consommation posterieure a la cloture.

## Exploitation

- appliquer `sql/v169_epic45_vision_360_animation.sql` avant le deploiement du code ;
- surveiller les temps de reponse de recherche/synthese (cible 500 ms) et indicateurs (cible 1,5 s) ;
- ne jamais reconstruire les coordonnees anonymisees depuis une autre source ;
- conserver une taille maximale de page de 100 elements.


## Documents complémentaires du dossier

- [Résultats lisibles dans le Live](live-evenements.md)
- [openapi.json](openapi.json)

[Retour à l’index des spécifications](../INDEX.md)
