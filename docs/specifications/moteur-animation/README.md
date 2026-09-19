# Moteur commun d'animation — EPIC 55

> Suivi produit au 19 septembre 2026 : **En cours** — [backlog de référence](../../roadmap/en-cours/epic-55-chasse-tresor-commercante-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

La [spécification unique du moteur](localeo_animation_engine_spec.md) décrit l'Animation générique, le DSL JSON, les moteurs spécialisés et le catalogue V1 : Passeport commerçant, Tombola locale et Chasse au trésor.

La Chasse V1 prévoit cinq activités : QCM, information, association, remise en ordre et saisie d’un mot/code (TRE-ARB-88, section 4.6.3). Les cinq validateurs métier et leurs contrats sont implémentés dans le socle T1 ; la persistance du jeu et les trois rendus Live sont implémentés et vérifiés localement en T4. Le [compte rendu d’implémentation](suivi-implementation.md) détaille les preuves et les limites par lot.

Le catalogue doit pouvoir accueillir de nouveaux types via des modules enregistrés (schéma, règles, commandes, projections et renderer). Le profil linéaire est propre à la Chasse V1 ; il ne limite pas le socle commun. Voir la section 4.8 et TRE-ARB-56 de la spécification.

Le [backlog EPIC 55](../../roadmap/en-cours/epic-55-chasse-tresor-commercante-backlog.md) suit les arbitrages et la livraison. Les contrats proposés restent une cible à implémenter et à vérifier. Le cadrage du 18 septembre 2026 retient une bascule directe : Live n’est pas encore déployé et aucune animation n’a été publiée avec l’ancien moteur. Aucune rétrocompatibilité Live ni coexistence de moteurs n’est requise ; les détails sont portés par la spécification et TRE-ARB-22/TRE-ARB-55.

Le questionnaire des 27 points a reçu ses réponses le 19 septembre 2026 (TRE-ARB-60 à TRE-ARB-86). La comparaison des fournisseurs IA commence pendant le développement V1, avec intégration après le pilote. Après V1, le prochain type prioritaire est le rallye à ordre libre ; la réutilisation dans une autre commune commencera par une adaptation contrôlée vers un nouveau brouillon. Les détails techniques, la réalisation et les vérifications restent à mener ; ces orientations ne changent pas le catalogue V1.

Les spécifications [EPIC 41](../epic-41-api/README.md), [Tombola — EPIC 53](../epic-53-tombola-locale/README.md) et [Calendrier de l'Avent — EPIC 54](../epic-54-calendrier-avent-local/README.md) documentent leurs périmètres propres. Leur antériorité ne valide pas implicitement les nouveaux arbitrages du moteur commun.

[Exemple de prompt simplifié — Latresne](exemples/latresne/README.md) : listes de commerçants et POI, fourchette d’étapes, durée, public, difficulté et thème ; export JSON et schéma de réponse séparé.

Le thème visuel de l’animation peut être complété par une illustration et des surcharges par étape ou mission. La même demande génère le récit et les images WebP réelles, embarquées en base64 dans le JSON final. Chaque média reste sous 60 000 octets, base64 et métadonnées compris ; sa résolution s’adapte au budget PC/mobile. Le rendu se fonde sur les éléments déclarés dans l’animation (TRE-ARB-90, [section 8.1.2](localeo_animation_engine_spec.md#812-thème-visuel-et-illustrations-de-lanimation)).

## Conception technique V1

Le [lot technique du 19 septembre 2026](conception-technique.md) fixe les six sujets : contrats de production, stockage/versions, concurrence/reprise, API/droits/projections, médias/budgets et exploitation/recette. Il s’appuie sur le code existant et définit les lots T1–T6 avec leurs preuves de sortie. Les décisions métier restent dans la spécification ; le [suivi T1–T6](suivi-implementation.md) distingue les mécanismes implémentés, leurs tests et ce qui reste à raccorder.

Le lot T2 est implémenté et vérifié localement : génération manuelle, quota, worker, import des WebP, préparation guidée, console ERP, POI et bibliothèque privée. Le lot T3 complète les accords, contrôles, QR, compilation et publication, vérifiés localement ; voir le [compte rendu](suivi-implementation.md). Le lot T4 raccorde le jeu, les preuves, la reprise et les liens personnels dans Live. Le lot T5 apporte retrait global, continuité, corrections tracées, population figée et suivi d’exploitation. La conservation et les contrôles d’ouverture restent à finaliser en T6.

## Exemples et documents d’entrée

- [Dossier des exemples](exemples/README.md) : prompt, réponse générée et requête exportée pour Latresne.
- [Schéma JSON de réponse du LLM](contrats/reponse-generation-chasse.schema.json) : document d’entrée pour la spécification et la future implémentation.
- [Portée et utilisation du schéma](contrats/README.md).

[Retour à l’index des spécifications](../INDEX.md)

La préparation des chasses prévoit désormais des missions alternatives à confirmer par chaque commerçant (TRE-ARB-89, section 8.1.1), raccordées aux demandes de participation EPIC 56. Le parcours publié ne conserve que les missions acceptées ; cette préparation est implémentée en T3.

## Support UX Localeo Live

La [maquette navigable de la chasse Halloween à Latresne](exemples/latresne/maquettes-live/index.html) illustre le parcours joueur, les cinq activités, les preuves et les états de reprise. Son [guide](exemples/latresne/maquettes-live/README.md) décrit les simulations et leurs limites. Les illustrations WebP et les thèmes sont résolus depuis les données de l’animation.
