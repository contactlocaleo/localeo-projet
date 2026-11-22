# Contrôles techniques des maquettes

Date : 18 novembre 2026. Portée : fichiers locaux de l’étape 3 uniquement, Chromium via Playwright. Aucun résultat ci-dessous ne valide l’application en ligne ni un comportement métier.

## Résultats exécutés

| Contrôle | Résultat | Preuve |
| --- | --- | --- |
| 14 planches à 320, 390 et 430 px | 42 lectures sans débordement horizontal de page ou de zone principale | [rapport JSON](rapport.json) |
| Navigation principale | Trois commandes textuelles sur les 42 lectures | rapport JSON |
| Hauteur des boutons visibles | Minimum mesuré ≥ 44 px sur les 42 lectures ; ne couvre pas tous les types de cibles | rapport JSON |
| Texte agrandi ×2 | Quatre planches principales à 320 px sans débordement horizontal | PNG de contrôle et rapport JSON |
| Galerie à 320, 390, 430 et 1440 px | Quatre orientations, 14 états sélectionnables ; comparaison double sur ordinateur, bascule exclusive sur mobile ; aucun débordement | rapport JSON |
| Clavier B1 à 320 px | 21 pressions Tab ; aucun élément de la zone principale focalisé hors de sa zone visible | rapport JSON |
| JavaScript / réseau de la série | Aucune exception de page ; aucune requête HTTP(S) observée | rapport JSON |
| E1 après ajout du retour explicite sans inscription | Nouveau rendu, 320 px sans débordement | finalE1 du rapport JSON |
| Rendus | 14 PNG de fenêtre et 14 PNG complets produits ; inspection visuelle des familles d’écrans et de la galerie | dossier maquettes-apres |

Le mode `?large` simule un texte de base à 200 % et adapte le flux. **Ce n’est pas un test de zoom natif du navigateur ni une preuve WCAG de redistribution.** Le contrôle Tab est limité au formulaire B1 de la maquette, sans clavier virtuel.

Les premières tentatives du script de contrôle attendaient un iframe visible alors que la bascule mobile l’avait volontairement masqué ; cette attente de test a été corrigée. La série finale est celle du rapport, aucune erreur de l’application n’en a été déduite.

## Mesures de palette des planches

Calcul du contraste par luminance relative sRGB, avec couleurs CSS opaques :

| Texte | Fond | Rapport |
| --- | --- | ---: |
| #ffffff | #09685e | 6,66:1 |
| #183243 | #f5f7f9 | 12,41:1 |
| #526575 | #ffffff | 6,04:1 |
| #725000 | #fff2d6 | 6,61:1 |
| #963b23 | #ffffff | 7,13:1 |

Ces valeurs portent sur cinq paires de la maquette. Le contraste du bouton AVANT n’a pas été mesuré sur l’application ; aucun ratio de l’avant n’est inventé. Les états de focus, les icônes, toutes les combinaisons et tous les composants n’ont pas fait l’objet d’un audit exhaustif.

## Captures de contrôle

- [Galerie ordinateur 1440 px](galerie-1440.png)
- [Galerie mobile 320 px](galerie-320.png), [390 px](galerie-390.png), [430 px](galerie-430.png)
- [B1 texte agrandi](B1-inscription-320-texte200.png)
- [C1 texte agrandi](C1-disponible-320-texte200.png)
- [D1 texte agrandi](D1-programme-320-texte200.png)
- [E1 texte agrandi](E1-formulaire-erreur-320-texte200.png)

## Non exécuté et limites

Lecteur d’écran, zoom natif, clavier virtuel, appareils physiques, audit de conformité, temps de chargement réel, contraste exhaustif, inscription, envoi d’e-mail, récupération, accès QR personnel, retrait, PIN et transitions de lot. Aucun test habitant réel.

Les fonctions métier sont volontairement des représentations statiques. Le panneau de règlement est un emplacement ; les liens de récupération et les boutons métier ne constituent pas une implémentation. Les captures de contrôle sont des rendus APRÈS, jamais des preuves de l’application actuelle.
