# Maintenir les guides Commerçant et Animation

Les guides accessibles depuis les applications font partie du produit livré.
À chaque évolution ou correctif, examiner l’impact sur **les deux guides**, y
compris lorsque le changement vient du backend ou de Live. Mettre à jour le
guide concerné dans la même livraison logique dès qu’une action, un libellé
utile, une navigation, une règle visible ou un état décrit change. Si aucun
guide n’est affecté, en donner la raison dans le bilan du changement.

## Sources et copies distribuées

| Guide | Source canonique dans Projet | Livrable canonique dans Projet | Copie livrée par l’application |
| --- | --- | --- | --- |
| Commerçant | [Source éditable](../produit/formation/commercant/guide-quotidien-commercant.md) | [PDF Commerçant](../../livrables/formation/commercant/guide-quotidien-localeo-commercant.pdf) | `localeo-commercant/public/guides/guide-quotidien-localeo-commercant.pdf` |
| Animation | [Source éditable](../produit/formation/animation/guide-quotidien-animation.md) | [PDF Animation](../../livrables/formation/animation/guide-quotidien-localeo-animation.pdf) | `localeo-animation/public/guides/guide-quotidien-localeo-animation.pdf` |

Les sources et illustrations restent dans Projet. Les générateurs, outils de
capture, synchroniseurs et tests restent dans leur dépôt applicatif. La copie
publique est un livrable généré, jamais une seconde source éditoriale. Ne pas
modifier une ancienne édition pour faire disparaître son caractère historique.

## Rédiger par geste métier

- **Partir du besoin de la personne.** Lister les gestes qu’un gestionnaire
  Animation ou un commerçant doit pouvoir réaliser. Pour chaque geste, choisir
  un titre avec un verbe et un résultat concret, comme « Publier une animation »
  ou « Valider la prestation d’un client ». Regrouper les gestes selon le
  déroulement du travail, de la prise en main aux tâches du quotidien.
- **Donner un sommaire dès l’ouverture.** Afficher le sommaire dans les
  premières pages du PDF, avec les titres des gestes et un repère de page
  ou un lien vers chaque section. Aligner l’ordre et les intitulés du sommaire
  sur les sections. Conserver les signets du PDF en complément.
  Les générateurs reprennent les titres Markdown de forme `## N · Titre`.
  Pour ouvrir un groupe dans le sommaire, placer le commentaire
  `<!-- Sommaire : Nom du groupe -->` juste avant son premier geste.
- **Expliquer et illustrer chaque geste.** Indiquer ce que la personne va
  accomplir, où commencer et ce qu’elle doit avoir sous la main si nécessaire.
  Décrire le cas habituel étape par étape. Placer une ou plusieurs captures
  réelles près des actions qu’elles éclairent, avec une légende qui indique
  quoi repérer ou vérifier. Terminer le parcours par le signe visible qui
  confirme le résultat.
- **Employer les mots du quotidien.** S’adresser directement à la personne,
  avec des phrases courtes et les libellés affichés pour les menus, boutons et
  états. Expliquer les termes métier indispensables à leur première apparition
  et laisser les détails d’implémentation dans les documents techniques.
- **Placer les variantes après le cas habituel.** Ajouter les autres façons
  de faire, les options avancées ou les difficultés courantes quand elles
  aident à agir. Dire dans quelle situation elles s’appliquent et quelle
  action entreprendre. Indiquer dès le départ tout prérequis indispensable
  au parcours habituel.

### Relire comme une personne qui découvre Localeo

Ouvrir le PDF en se plaçant dans la situation d’un nouveau gestionnaire
Animation ou d’un nouveau commerçant. Parcourir d’abord le sommaire et
chercher des tâches concrètes de la journée. Les titres doivent permettre de
reconnaître les gestes essentiels et de trouver la bonne page sans connaître
les menus de l’application. Suivre ensuite le parcours habituel du geste
traité dans l’interface en s’aidant du texte et des captures. Vérifier que le
point de départ, chaque action et le résultat attendu se comprennent sans
explication orale. Corriger les gestes difficiles à trouver et les étapes
ambiguës avant de valider le guide.

## Actualiser et vérifier

1. Comparer le parcours décrit avec le comportement réellement livré et ses
   spécifications courantes. Décrire les fonctions conditionnelles selon les
   droits et services activés ; une évolution prévue reste hors du guide courant.
2. Corriger le geste concerné et son entrée dans le sommaire selon les règles
   de rédaction ci-dessus.
3. Recapturer les écrans affectés depuis la vraie interface avec des données
   fictives et des API locales simulées, ou un environnement explicitement
   autorisé. Ne pas dessiner un écran supposé. Exclure secrets, coordonnées
   personnelles et QR utilisables. Le README des illustrations indique date,
   version de base, parcours et commande de capture ; une recette locale ne
   prouve pas un déploiement distant.
4. Régénérer le PDF, rendre **toutes ses pages** en images et vérifier leur
   lisibilité : captures et légendes, sauts de page, polices, tableaux, liens,
   numérotation, absence de texte coupé ou superposé. Adapter la pagination au
   contenu plutôt que réduire les caractères jusqu’à les rendre illisibles.
   Vérifier les destinations du sommaire et faire la relecture en situation
   de découverte avant de synchroniser le PDF.
5. Synchroniser la copie embarquée, vérifier son égalité avec le PDF canonique,
   puis vérifier le lien depuis l’application et le PDF réellement servi dans
   le build. Une modification du point d’accès exige une recette mobile,
   bureau et clavier ; une mise à jour du PDF seul conserve un contrôle HTTP
   du fichier et de son contenu. Le guide reste accessible si la messagerie
   d’assistance est indisponible.
6. Dater l’édition dans le commentaire éditorial de la source (`Édition du
   <date>.`) : les générateurs en déduisent le pied de page et les métadonnées.
   Actualiser les légendes et les index si leur description
   change. Consigner les commandes exécutées et leurs résultats dans le bilan.
   Expliquer toute vérification non exécutée. Une livraison ne se déclare pas
   terminée avec un guide affecté encore obsolète.

## Commandes

Depuis **localeo-commercant**, avec les dépendances Python du générateur :

```console
python scripts/generate-merchant-guide.py --preview-dir tmp/merchant-guide-preview
npm run guide:sync
npm run guide:check
```

Depuis **localeo-animation** :

```console
python scripts/generate-animation-guide.py --preview-dir tmp/animation-guide-preview
npm run guide:sync
npm run guide:check
```

Les README applicatifs précisent les dépendances et les recettes de capture
et d’accès au PDF. Depuis **localeo-projet**, vérifier les liens et les sources :

```console
python scripts/check_guidance.py --changed --all-markdown
python scripts/sync_documentation.py --check-sources
```

Ces contrôles ne remplacent ni la relecture pédagogique ni l’inspection des
pages rendues. Commit, push et déploiement suivent la demande courante.
