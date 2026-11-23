# Contrôles des maquettes locales

Le 23 novembre 2026, le comparatif et son écran autonome ont été ouverts depuis les fichiers locaux avec Chromium 151 et Playwright. Les contrôles couvrent la galerie et les planches.

| Contrôle | Résultat |
| --- | --- |
| Galerie sur ordinateur | Deux colonnes visibles à 1 440 px. Les 24 états sont accessibles. Huit montrent un AVANT équivalent, douze une capture de contexte et quatre signalent directement l’AVANT manquant. |
| Galerie mobile | À 320, 390 et 430 px, la bascule affiche un seul panneau et le document tient dans la largeur. Le panneau APRÈS a été relu avec la planche visible à 390 px. |
| Planches | 72 lectures, 24 états à chacune des trois largeurs. Un titre principal par état, identifiants uniques, liens de simulation valides et aucun débordement horizontal. |
| Texte agrandi | 24 lectures à 320 px avec taille de texte racine de 200 %. Le débordement de la barre de navigation identifié à la première passe a été corrigé. Résultat final sans débordement horizontal. |
| Navigation locale | B1 fiche → formulaire → fiche. B3 refus → récupération → refus. C1 ouvrir puis fermer le bon. L’état de lot incertain ne propose pas de présentation. |
| Focus | Entrée sur « Prochainement » atteint le titre de la période. Le lien de correction E1 atteint le champ e-mail. Le retour D3 place le focus sur le repère du programme. |
| Ressources et isolement | Logo et deux polices chargés localement. Zéro erreur JavaScript ou ressource manquante, zéro requête HTTP externe. Entrée dans le formulaire E1 conserve la même page. |
| Relecture visuelle | Galerie sur ordinateur, galerie mobile, et un écran par orientation à 390 × 844 relus en PNG. |

Le contrôle à 200 % porte sur un agrandissement de texte dans Chromium. Les annonces aux lecteurs d’écran, le clavier virtuel sur appareil et le comportement réel de l’API restent des sujets de recette. Le résultat sur le retour D3 démontre l’ancre du prototype. Il ne vérifie pas la restauration réelle des filtres et de la position dans Live. [Référence des états](reference-maquettes.md) · [Revue contradictoire](revue-contradictoire.md) · [Limites de l’exploration](../observations/limitations.md)
