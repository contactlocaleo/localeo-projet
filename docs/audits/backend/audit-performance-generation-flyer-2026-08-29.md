# Audit de performance de la génération des flyers

Date : 29 août 2026

## Conclusion

Le poids de 6,4 Mo provenait principalement de l'intégration dans le PDF d'une page A4 complète sous forme de PNG sans perte à 300 dpi (2480 × 3508 pixels). Les ombres étaient en outre calculées sur des calques RGBA de la taille de la page et plusieurs copies complètes du master coexistaient pendant la génération.

Le PDF est désormais composé directement à 200 dpi (1654 × 2339 pixels) puis produit par l'encodeur PDF natif de Pillow. Un repère logique conserve les proportions de la maquette historique sans créer de master intermédiaire à 300 dpi. La génération de référence produit un PDF de 397 778 octets.

## Mesures

Mesures locales sous Windows sur le flyer de référence de l'Epic 41 :

| Indicateur | Avant | Après | Évolution |
|---|---:|---:|---:|
| PDF | 6 400 499 octets | 397 778 octets | -93,8 % |
| Aperçu PNG | 783 468 octets | 801 269 octets | +2,3 % |
| Durée | 9,05 s | 0,63 s | -93,0 % |
| Pic mémoire du processus | 232,3 Mio | 59,3 Mio | -74,5 % |

Ces valeurs constituent une mesure comparative et peuvent varier selon la machine et le visuel fourni. Le processus Python occupait 23,7 Mio au repos pendant la mesure : la génération ajoute donc environ 35,6 Mio au pic. Le test automatisé empêche le flyer de référence de dépasser 500 000 octets et l'aperçu de dépasser 1 000 000 octets.

## Évolutions appliquées

- composition directe à 200 dpi et encodage PDF natif par Pillow, sans ReportLab ;
- projection des coordonnées de conception historiques par un repère logique indépendant de la résolution ;
- réutilisation et réduction en place du master pour construire l'aperçu social, puis fermeture avant encodage PNG ;
- calcul des ombres sur leur zone utile au lieu d'un calque couvrant toute la page ;
- fermeture explicite des images intermédiaires ;
- mise en cache des polices ;
- sérialisation des générations au sein d'un worker pour éviter la multiplication des pics mémoire lors de publications simultanées ;
- refus des visuels source dépassant 12 Mio ou 24 mégapixels, avec utilisation du visuel de repli.

## Limite restante

Le flyer demeure une composition raster. Un PDF majoritairement vectoriel pourrait encore réduire son poids et améliorer le texte à très fort grossissement, mais nécessiterait une réécriture du moteur graphique. Le rendu à 200 dpi constitue le compromis retenu pour l'impression A4, la diffusion numérique et la stabilité du processus de publication.
