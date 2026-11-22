# Maquettes Localeo Animation — étape 3

**Propositions, données fictives, aucun accès à une API.** Les fichiers HTML et leurs rendus PNG sont des maquettes isolées, pas des écrans déployés. Les boutons ne font que changer un état de présentation local ; aucune donnée n’est enregistrée, publiée, importée ou envoyée.

## Intention de conception avant réalisation

- **Direction visuelle :** conserver la sobriété opérationnelle de Localeo Animation, son en-tête bleu nuit, son vert d’action et ses surfaces claires, en rendant le prochain geste plus lisible.
- **Organisation du contenu :** contexte d’animation, action attendue, explication utile et détails secondaires ; conserver les étapes, la navigation et les confirmations existantes.
- **Interactions :** bascule entre états pour la revue ; focus visible et retour de confirmation ; changement avant/après dans la galerie mobile. Pas d’animation décorative, respect de la préférence de mouvement réduit.

Le skill frontend est adapté aux contraintes de fidélité de l’utilisateur : aucun hero marketing, nouvelle identité ou suppression générale des panneaux existants.

## Périmètre fermé

A1, B1, B2, B3, C1, C2, D1, D2, E1 : neuf orientations adoptées P0/P1. F1 et G1 restent P2 et ne donnent lieu à aucune nouvelle proposition. Les déclinaisons mobiles adaptent uniquement les neuf orientations autorisées ; elles ne réalisent pas les raccourcis G1.

## Identité réutilisée

Lecture des sources locales `localeo-animation/src/styles/theme.css` et `application-frame.css` : police système, fond `#f5f7f9`, texte `#183243`, primaire `#09685e`, en-tête `#123247`, bordure `#d8e1e7`, contrôles de 44 px minimum, rayon de panneau 12 px, contrôle 9 px, champ 7 px. Le pictogramme `header-mark.svg` est copié sans modification depuis les ressources de l’application ; aucune ressource distante n’est nécessaire.

## Limites à garder visibles

- B1 illustre un contrat de brouillon partiel à concevoir ; il ne prouve pas sa disponibilité.
- C1 est une proposition de demande de référencement et de suivi : propriétaire, contrat et droits restent à vérifier avant implémentation.
- C2 conserve un contrôle humain ; une similitude n’est pas un doublon certain.
- D1 ne répare pas le 500 par une maquette. Les états de service rétabli, aperçu et retour d’envoi sont uniquement des propositions de présentation.
- E1 conserve la confirmation de clôture et la distinction information/remise ; aucune règle d’automatisation n’est ajoutée.
- La capture 18 situe le paramétrage du passeport mais ne montre pas le seuil inférieur. Pour B3, le problème est attesté par AN-05 et le relevé DOM, pas par cette seule image. La galerie signale cette lacune visuelle au lieu de reconstruire un AVANT.

La [galerie comparative](../comparatif-avant-apres.html) relie chaque orientation à ses preuves et à ses états. Les votes initiaux et les retours de revue restent simulés. La validation de l’utilisateur est attendue.


## Fichiers finaux et revue

Version v2 après revue contradictoire ; [arbitrages](../../workshop/arbitrages-maquettes.md). Les [sources v1](iterations/v1-sources.zip) et les [rendus initiaux](iterations/v1/manifest-v1.json) sont conservés. Les sources HTML archivées doivent être replacées dans leur contexte d’origine pour retrouver la galerie ; les PNG v1 restent directement consultables. Les actions de présentation ne sont pas un prototype connecté ni une implémentation du domaine.

| Orientation | Maquette | États | Rendu principal bureau | Rendu principal mobile |
| --- | --- | ---: | --- | --- |
| A1 | [Donner la priorité aux actions attendues](A1.html) | 1 | [PNG](A1-accueil-bureau.png) | [PNG](A1-accueil-mobile.png) |
| B1 | [Sauvegarder avant la fin des sept étapes](B1.html) | 3 | [PNG](B1-saisie-bureau.png) | [PNG](B1-saisie-mobile.png) |
| B2 | [Expliquer préparation, accords et publication](B2.html) | 5 | [PNG](B2-publication-bureau.png) | [PNG](B2-publication-mobile.png) |
| B3 | [Proposer un seuil de passeport cohérent](B3.html) | 2 | [PNG](B3-compatible-bureau.png) | [PNG](B3-compatible-mobile.png) |
| C1 | [Rendre trouvable l’ajout d’un commerce absent](C1.html) | 3 | [PNG](C1-selection-bureau.png) | [PNG](C1-selection-mobile.png) |
| C2 | [Sécuriser la compréhension de l’import](C2.html) | 4 | [PNG](C2-apercu-bureau.png) | [PNG](C2-apercu-mobile.png) |
| D1 | [Rétablir et fiabiliser Communication](D1.html) | 6 | [PNG](D1-lecture-bureau.png) | [PNG](D1-lecture-mobile.png) |
| D2 | [Diriger le suivi vers le suivi opérationnel](D2.html) | 2 | [PNG](D2-suivi-bureau.png) | [PNG](D2-suivi-mobile.png) |
| E1 | [Rendre explicite le chemin de fin](E1.html) | 4 | [PNG](E1-periode-bureau.png) | [PNG](E1-periode-mobile.png) |
