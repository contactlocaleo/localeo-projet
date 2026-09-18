# Polices de la Marketplace Localeo

La Marketplace utilise deux polices variables integrees au bundle de production et servies depuis l'infrastructure Localeo. Aucun appel a Google Fonts ou a un CDN de polices n'est effectue au rendu.

## DM Sans

- paquet : `@fontsource-variable/dm-sans` ;
- usage : textes, navigation, formulaires et composants fonctionnels ;
- projet source : `https://github.com/googlefonts/dm-fonts` ;
- licence : SIL Open Font License 1.1 ;
- fichiers livres : variantes WOFF2 latines selectionnees automatiquement par Vite.

## Oswald

- paquet : `@fontsource-variable/oswald` ;
- usage : titres editoriaux courts et reperes de section ;
- projet source : `https://github.com/googlefonts/OswaldFont` ;
- licence : SIL Open Font License 1.1 ;
- fichiers livres : variantes WOFF2 latines selectionnees automatiquement par Vite.

Les textes complets des licences sont fournis par les paquets installes et verrouilles dans `package-lock.json`.
