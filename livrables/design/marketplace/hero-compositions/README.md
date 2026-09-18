# Trois compositions de hero Localeo

Ouvrir `index.html` pour comparer les variantes et basculer entre ordinateur et mobile. Les fichiers sont maintenant dans le dépôt transverse : ouvrir `index.html` directement, ou servir le dossier parent des cinq dépôts avec `python -m http.server 8000 --bind 127.0.0.1`, puis ouvrir `/localeo-projet/livrables/design/marketplace/hero-compositions/index.html`.

## Direction artistique

Une identité chaleureuse et contemporaine : scènes de commerce lumineuses, bleu Localeo, crème, accent orange, typographies DM Sans et Oswald du projet.

1. **Immersion** : photographie plein écran, texte superposé, recherche directe. Promesse : « Tout près. Tellement à vivre. »
2. **Éditorial** : texte sur un aplat crème et photographie dominante à droite ; sur mobile, photographie puis texte. Promesse : « Le bonheur est au coin de la rue. »
3. **À partager** : panorama et bandeau bleu avec titre et action côte à côte ; empilés sur mobile. Promesse : « Offrez du local. Partagez l’essentiel. »

Chaque proposition comprend le header, une promesse, une phrase de soutien, une action principale et une réassurance. Apparition progressive du texte, léger rapprochement de l’image à l’entrée et transitions de survol ; respect de `prefers-reduced-motion`.

Les photos mettent en avant une vie locale cosmopolite et intergénérationnelle, avec des personnes d’origines variées qui découvrent les commerces ensemble : trois générations devant une pâtisserie, une dégustation entre un jeune adulte, une senior et une commerçante, puis la découverte du travail d’une chocolatière par des jeunes et un senior. Fichiers : `../hero-variantes/16-boulangerie-generations.png`, `17-primeur-generations.png` et `18-chocolatier-generations.png`. Images synthétiques générées avec l’outil intégré image_gen ; prompts dans `../hero-variantes/PROMPTS-cosmopolite-generations.md`. Les polices et le symbole de marque sont référencés dans le projet.

Prototypes isolés : aucun changement à l’accueil de production. Le comparateur présente les compositions ; ses liens métier absolus (`/accueil`, `/recherche`) nécessitent une marketplace servie sur le même hôte. Les polices et le symbole sont référencés dans le dépôt voisin ; installer les dépendances Marketplace pour charger ses polices locales.
