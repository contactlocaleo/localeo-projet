# Provenance des prompts et évolution du protocole

Contrôle du 19 novembre 2026. Les messages utilisateur séquentiels font foi ; aucune version historique supplémentaire n’est inventée. L’absence du protocole global initial demeure une anomalie explicite.

| Fichier | Source réellement utilisée | État et transformation |
| --- | --- | --- |
| [00](../prompts/00-protocole-global.md) | Aucun message distinct fourni. | Fichier de constat d’absence conservé ; ce n’est pas un prompt complet. Ne pas présenter le protocole comme entièrement archivé. |
| [01](../prompts/01-exploration.md) | Instruction étape 1 fournie en conversation et pièces jointes. | Texte complet expurgé ; login et mot de passe remplacés par `[CONFIDENTIEL]`. Les pièces jointes contenant les secrets ne sont pas copiées. |
| [02](../prompts/02-workshop.md) | Pièce jointe de l’étape 2 effectivement lue. | Texte complet ; comparaison à la pièce jointe disponible lors du contrôle. |
| [03](../prompts/03-maquettes.md) | Message étape 3 de la conversation. | Texte complet archivé ; pas de nouvelle version reçue. |
| [04](../prompts/04-validation.md) | Message étape 4 de la conversation. | Texte complet archivé ; prépare les décisions sans en recevoir. |
| [05](../prompts/05-archivage.md) | Message étape 5 de la conversation. | Texte complet archivé pendant cette phase, remplace uniquement le fichier d’attente. |

Les prompts 00–04 restent inchangés pendant l’étape 5. Les étapes 2, 3, 4 et 5 ont été autorisées par leurs demandes successives ; cela n’accorde aucune validation des orientations. Aucun historique de variantes non fourni n’est reconstitué.

## Nouvelle consolidation destinée à la prochaine exécution

[RELANCER-WORKSHOP.md](../prompts/RELANCER-WORKSHOP.md), version **relance v1.0**, créé le 19 novembre 2026 : reprend les cinq phases, les seuils de vote et les points d’arrêt, et rend explicites la découverte du protocole le plus récent, le nouveau dossier sans écrasement, les limites de preuve, l’anonymisation et la comparaison historique. Il n’a pas été utilisé pour l’exploration actuelle et ne remplace pas rétroactivement 00.

Version du protocole initial : **non fournie / non versionnée**. La version v1 des orientations figées avant vote est une version du contenu de conception, pas du protocole global. La rejouabilité offerte est méthodologique : un environnement et des générations simulées peuvent évoluer ; une sortie identique n’est pas garantie.

## Modèles et raisonnement

Contexte déclaré de l’agent principal de cette session : Codex, basé sur GPT-6. Identifiant exact de déploiement du modèle et niveau de raisonnement : non exposés dans les preuves archivées. Les agents du workshop et de revue sont identifiés par leur rôle dans les livrables ; leur modèle exact et leur niveau de raisonnement ne sont pas établis. Aucune valeur n’est déduite de la qualité des réponses ou du nom d’un persona.
