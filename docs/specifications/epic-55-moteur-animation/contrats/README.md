# Contrats documentaires du moteur d’animation

## Schéma du résultat préparatoire de génération outillée

[reponse-generation-chasse.schema.json](reponse-generation-chasse.schema.json) conserve le JSON Schema utilisé pour les propositions de chasse et leurs missions commerçantes alternatives. Il constitue un **document d’entrée de la spécification** pour la conception du contrat de génération et de son import.

- Il décrit le résultat final assemblé de la génération outillée (récit et images réelles), pas les paramètres d’initialisation ni la seule réponse d’un modèle textuel.
- Il correspond à la révision 8 de l’[exemple Latresne](../exemples/latresne/README.md), avec cinq formats de défi, des missions à confirmer, un thème visuel facultatif et des illustrations par étape/mission embarquées en base64.
- Il contient encore les listes de commerçants et de POI de Latresne. Pour une autre chasse, ces listes doivent être instanciées à partir des lieux autorisés du brief ; elles ne constituent pas un catalogue global du moteur.
- Il contrôle la structure ; références croisées, accords, confirmations, assemblage, autorisations et publication relèvent du domaine.
- Ce fichier n’est pas un contrat backend déjà implémenté ni le DSL jouable. Les futurs modèles backend et leurs exports automatiques suivent la [spécification](../localeo_animation_engine_spec.md), notamment TRE-ARB-65.

Le fichier avait été déplacé sans changement depuis `exemples/latresne/reponse.schema.json` à la révision 6. La révision 7 ajoutait les blocs visuels ; la révision 8 ajoute les médias base64 à la même demande ; le prompt, la copie de schéma dans `requete-exemple.json` et son empreinte ont été synchronisés. Le prompt et l’animation restent regroupés dans `exemples/latresne/`.

`themeVisuel` appartient à l’animation ; `presentation` est facultative sur les positions et les missions. Les polices et couleurs sont en liste fermée. La même opération fournit le récit, les intentions d’illustration et les images réelles en `medias[].base64`, dédupliquées par identifiant. Un outil image puis un encodeur produisent les octets ; le modèle textuel ne les invente pas. Chaque objet média JSON compact UTF-8 reste sous 60 000 octets, avec une image commune PC/mobile ; voir la [section 8.1.2](../localeo_animation_engine_spec.md#812-thème-visuel-et-illustrations-de-lanimation).

Pour un essai manuel, envoyer [le prompt](../exemples/latresne/prompt-complet.md) et le schéma. L’export complet de la requête n’a pas à être envoyé en plus.

## Passage au contrat de production

Le [dossier technique V1](../conception-technique.md#3-contrats-de-production-et-frontières) précise les modèles backend et leurs exports automatiques. Le schéma ci-dessus reste l’entrée documentaire révision 8 ; il n’est pas remplacé par un second schéma de production maintenu manuellement. Lors de l’implémentation, porter la fixture Latresne vers les références de lieux `{type,id}` et le contrat généré, puis synchroniser prompt, requête et maquette. Les exemples actuels restent inchangés par le lot de conception.

[Retour au moteur d’animation](../README.md).
