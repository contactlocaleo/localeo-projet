# Provenance du protocole et évolutions

## Instructions réellement disponibles

| Fichier | Provenance et intégrité | Statut |
| --- | --- | --- |
| [00-protocole-global.md](../prompts/00-protocole-global.md) | Aucun prompt global distinct n'a été fourni pour cette exécution. Le fichier reste le marqueur initial « Prompt non fourni ». | **Manquant comme prompt complet** ; aucune version historique fabriquée. |
| [01-exploration.md](../prompts/01-exploration.md) | Pièce fournie pour l'étape 1 ; SHA-256 identique à la pièce d'origine après correction d'archive le 18 novembre 2026. | Complet. |
| [02-workshop.md](../prompts/02-workshop.md) | Pièce fournie pour l'étape 2 ; SHA-256 identique à la pièce d'origine. | Complet. |
| [03-maquettes.md](../prompts/03-maquettes.md) | Instruction transmise directement dans la conversation, transcrite dans le fichier. | Complet selon vérification de contenu ; pas de pièce source permettant un contrôle binaire. |
| [04-validation.md](../prompts/04-validation.md) | Instruction transmise directement dans la conversation, transcrite dans le fichier. | Complet selon vérification de contenu ; pas de pièce source permettant un contrôle binaire. |
| [05-archivage.md](../prompts/05-archivage.md) | Instruction transmise directement dans la conversation, transcrite à cette étape. | Complet selon vérification de contenu ; pas de pièce source permettant un contrôle binaire. |

**Correction d'archive constatée à l'étape 5 :** la version de `01-exploration.md` présente au début de ce contrôle indiquait `https://coffret.localeo.city` à la place de l'URL TEST `https://test-coffrets.localeo.city` contenue dans la pièce d'origine. Le fichier a été remplacé par la pièce d'origine exacte. Les observations et captures portent déjà sur l'URL TEST ; elles n'ont pas été réécrites. Cette note documente l'écart et sa correction sans créer une fausse version historique.

**Amendement conversationnel de l'étape 1 :** après le prompt initial, le propriétaire a demandé de « purger le dossier existant et recommencer ». Cet amendement n'était pas contenu dans la pièce du prompt 01. L'état antérieur du dossier n'est pas conservé ici ; aucune reconstitution de cette version n'est faite.

**Décision de l'étape 4 :** le propriétaire a répondu globalement « VALIDÉE » à la présentation des sept orientations P0/P1. La portée et l'heure d'enregistrement figurent dans [decisions.md](../validation/decisions.md). Cette décision n'est pas un nouveau prompt de validation ni une autorisation de paiement.

## Version de relance

La [consigne autonome de relance](../prompts/RELANCER-WORKSHOP.md) reçoit la version **1.0**, créée pendant cette étape 5 pour les exécutions futures. Cette version ne prétend pas être le protocole global historique manquant du workshop du 18 novembre. Le prochain workshop devra archiver les instructions effectivement reçues et enregistrer sa propre version/provenance.
