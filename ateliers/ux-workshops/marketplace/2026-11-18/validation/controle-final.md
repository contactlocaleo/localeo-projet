# Contrôle final d'archivage — 18 novembre 2026

## Résultat

**Archivage local avec réserve documentaire.** Les livrables demandés sont présents, mais [`prompts/00-protocole-global.md`](../prompts/00-protocole-global.md) reste un marqueur : aucun prompt global distinct n'avait été fourni. Il serait inexact de le remplir a posteriori. La [consigne autonome de relance v1.0](../prompts/RELANCER-WORKSHOP.md) couvre les futures exécutions sans prétendre être cette pièce historique. Voir la [provenance](../synthese/notes-protocole.md).

## Inventaire contrôlé

| Élément | Vérification | Statut |
| --- | --- | --- |
| Prompts 00–05 | 01 et 02 identiques (SHA-256) aux deux pièces sources ; 03, 04 et 05 complets selon vérification du contenu conversationnel ; 00 non fourni. | **Réserve : 00 manquant comme prompt complet.** |
| Instruction modifiée | 01 avait une URL de production incorrecte dans l'archive ; remplacé par la pièce d'origine avec l'URL TEST. L'amendement « purger et recommencer » est documenté sans reconstitution historique. | Corrigé et documenté. |
| Observations et cartographie | 5 fichiers : cartographie, inventaire, faits, frontière Stripe, limites. | Présents. |
| Captures AVANT | 27 fichiers PNG ; signature PNG, taille minimale et dimensions positives vérifiées. | 27 valides. |
| Workshop | Rapport exécutif, compte rendu, votes individuels et arguments, backlog, orientations rejetées, quick wins et revue contradictoire des maquettes. | Présents. |
| Maquettes et galerie | 7 maquettes HTML O-01, O-02, O-03, O-05, O-06, O-07, O-08 ; galerie comparative. Le [contrôle visuel](revue-visuelle.md) vérifie la bascule mobile et les largeurs. | Présentes. |
| Validation | 7 lignes VALIDÉE sur réponse globale du propriétaire, dossier de décision et backlog potentiel. | Enregistrées ; aucune implémentation. |
| Synthèse | [Roadmap](../synthese/roadmap-ux.md), [plan de tests auprès de vrais utilisateurs](../synthese/plan-tests-utilisateurs.md), provenance du protocole. | Présents ; aucun test utilisateur réel encore effectué. |
| Comparaison historique | Un seul répertoire marketplace daté a été trouvé : `2026-11-18`. | Non applicable ; `comparaison-precedent.md` non créé. |
| Dépôts applicatifs | `localeo-marketplace`, `localeo-backend`, `localeo-commercant` et `localeo-animation` : `git status --short` sans sortie lors de ce contrôle. | Aucune modification applicative dans cette étape. |
| Achat et paiement | Aucune requête mutante, commande, session Stripe ni paiement lancés à cette étape ; les étapes précédentes s'arrêtaient avant la soumission. | Aucun achat réel effectué. |

**Limites maintenues :** la page Stripe et le retour ne sont pas vérifiés ; l'environnement de lancement et ses contenus ne sont pas inspectés ; l'accessibilité de l'application n'a pas été auditée complètement ; les profils et votes du workshop étaient simulés. Les maquettes ne prouvent pas l'efficacité auprès de vrais visiteurs.

**Version du protocole de relance :** v1.0 créée à l'étape 5. **Statut Git du dossier :** non suivi par Git dans `localeo-projet` au moment du contrôle ; aucun commit ni push demandé ou effectué pour ce dossier.

**Contrôles documentaires finaux :** `py -3 scripts/check_guidance.py` : 110 guides, 1 627 liens locaux, aucune erreur ni alerte ; `py -3 scripts/sync_documentation.py --check-sources` : 151 documents vérifiés. Ces contrôles valident les sources et les liens, pas l'UX, le paiement ou les contenus de production.
