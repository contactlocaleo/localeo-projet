# E85-EVO-VISUEL · Choisir le visuel de l’animation

Le visuel de l’édition était réglé depuis **Flyer**, qui le fournissait aussi à Localeo Live. L’organisateur le choisit désormais dans **Publication → Visuel de l’animation** pour les cartes et la fiche Marketplace et Live, la fiche Localeo Pro et le prochain flyer généré. [Contexte du flyer](../epic-73-animation-et-ou-coffrets/flyers-contextualises.md)

## Choisir et diffuser

- L’écran présente trois exemples du modèle et **Importer une image**. La sélection affiche un aperçu du recadrage avant **Enregistrer le visuel**. L’organisateur peut remplacer ou retirer son choix. Une nouvelle édition ou un clone commence sans visuel choisi. Une image déposée depuis le flyer est déjà le visuel choisi de son édition.
- Le lecteur autorisé peut consulter le visuel. Seul un gestionnaire habilité peut le modifier lorsque l’édition est en brouillon, configurée, publiée ou en cours. Le changement confirme la nouvelle version de l’édition. La revue et l’Assistant relisent leur contrôle facultatif après ajout ou retrait. Le lien historique d’édition du flyer retrouve ce même écran et le retour au contrôle d’origine.
- Les lecteurs web voient le visuel lorsque l’édition est visible publiquement. **Ses animations** sur une fiche commerce Live utilise la miniature carrée. Les cartes illustrées de Marketplace et de **Découvrir** dans Live utilisent la miniature paysage. La fiche publique et la fiche Pro utilisent la version de fiche. Au retrait, chaque lecteur reprend son repli habituel. Le PDF existant signale la régénération lorsqu’il ne correspond plus à la présentation courante.

## Images et contrat

L’import accepte JPEG, PNG et WebP fixes jusqu’à **5 Mio**, de 64 pixels minimum sur chaque côté et jusqu’à 24 mégapixels. Recommander un paysage de **1 600 × 900 px** avec le sujet au centre. Le serveur contrôle le fichier, applique l’orientation, efface les métadonnées et garde le PNG normalisé pour la génération du flyer. Les sorties WebP sont bornées selon l’usage.

| Usage | Dimensions maximales | Poids maximal |
| --- | --- | --- |
| Vignette compacte Live dans Ses animations | 216 × 216 px | 15 Kio |
| Carte Marketplace et Découvrir dans Live | 480 × 270 px | 35 Kio |
| Fiche | 1 600 px sur le côté le plus long | 300 Kio |

Les six modèles implémentés possèdent chacun trois images distinctes livrées dans le backend. Le manifeste rattache les exemples à leur modèle. La sélection enregistre une copie sur l’édition pour préserver le choix lors d’une révision du catalogue d’images. Le contrôle d’exhaustivité suit le registre des moteurs, y compris les modèles dont l’activation est conditionnée par le catalogue.

Les exemples sont conçus comme des couvertures Live lumineuses, lisibles en vignette. Les pictogrammes numériques et les objets du décor propres à chaque jeu identifient le modèle. Le geste mis en scène est le scan d’un QR sur téléphone, à l’ouverture d’un défi ou lors d’un passage validé par le commerçant. Les motifs QR des visuels illustrent le geste. Les QR publics à partager se préparent dans **Supports de diffusion**. Les QR personnels se présentent depuis Localeo Live.

- La ressource d’édition `GET /protected/animation-locale/animations/{id}/visuel` expose `animation_version`, `visuel_url`, `exemple_id` et les entrées `id`, `libelle`, `apercu_url`. Les lectures binaires passent par le contrôle d’accès de la fiche. Le `PUT` accepte `expectedVersion` et un fichier `image_base64` ou un `exemple_id` du modèle. Le `DELETE` accepte `expectedVersion`. Les mutations et la consultation du reçu réutilisent le registre idempotent du flyer.
- L’agrégat Animation protège l’état et la version. L’application prépare le PNG et les WebP hors transaction SQL et rattache la sélection et ses dérivés ensemble. Le retrait archive le choix courant. L’identité du visuel participe à l’empreinte du PDF. Les anciens contrats du flyer continuent à exercer la même règle.
- La projection publique fournit `visuel_url`, `visuel_vignette_url` et `visuel_vignette_compacte_url`. La route historique `illustration-flyer` sert le PNG en l’absence de paramètre et propose `variante=fiche`, `vignette` ou `compacte`. Les PNG historiques restent la source de leurs WebP, calculés à la demande avec un cache interne borné par révision. Chaque lecture vérifie la visibilité et le choix courant. Pro reçoit `visuel_url` uniquement quand la même édition est visible publiquement. Les tables documentaires existantes portent la reprise et la conservation.

## Couverture des cartes Découvrir dans Live

**Décision du 28 novembre 2026.** Dans **Découvrir → Animations**, la couverture
paysage remplace le carré à droite lorsque `visuel_vignette_url` est fourni. Le
bandeau de 160 px, comme pour les coffrets, couvre la largeur de la carte avec un
recadrage centré. La grille garde ses colonnes sur ordinateur, même lorsqu’une
période comporte une seule carte. Les dates et les actions se lisent sous l’image.
Sur un écran court, le bouton s’atteint en poursuivant la lecture de la carte.

- La carte charge le paysage à l’approche de l’écran. La version de fiche se charge à son ouverture.
- Si le paysage échoue, le pictogramme du modèle occupe le bandeau réservé. Une édition sans image garde le pictogramme compact. Une réponse ancienne qui fournit seulement un visuel historique garde sa miniature à droite.
- L’aperçu organisateur identifie l’usage paysage pour la fiche et les cartes de **Découvrir**, et l’usage carré pour les listes compactes de Live. Le guide Animation montre ces deux aperçus.

Pour E85-CA-27, vérifier le cadrage du Passeport et du Jeu des vitrines à 320,
390 et 1 280 px, les périodes avec une seule carte ou des cartes mixtes, le repli
sans déplacement du bouton, les requêtes d’image et le retour clavier à la carte.

## Critères de livraison

| ID | Résultat observable | Preuve |
| --- | --- | --- |
| E85-CA-25 | Choisir un exemple ou importer une image, la relire depuis le flyer et revenir au contrôle de publication. | Parcours navigateur Animation sur téléphone et bureau, accès en lecture seule et lien historique. |
| E85-CA-26 | Chacun des six modèles propose exactement trois exemples distincts. Une édition garde la sélection confirmée. | Contrôle d’exhaustivité backend et refus d’un exemple étranger au modèle. |
| E85-CA-27 | Le même visuel apparaît sur les supports autorisés, aux dimensions et budgets attendus. | Tests de conversion, lecture publique et lecture Pro. Vérifier le rendu, les octets transférés, un ancien PNG et une édition sans visuel. [Carte Découvrir](#couverture-des-cartes-découvrir-dans-live) |
| E85-CA-28 | Remplacement, retrait ou refus laissent un seul choix courant. Un reçu rejoué retrouve la version confirmée. | Commandes et concurrence PostgreSQL isolées, empreinte du PDF, ancienne URL après retrait et refus inter-tenant. |
| E85-CA-29 | Une édition de recette est illustrée et une autre conserve son repli. Les guides indiquent le geste au bon endroit. | Génération locale, contrats embarqués, guides Animation et Commerçant rendus et accessibles. |

Exporter les contrats EPIC 41 et 42, synchroniser les lecteurs Animation et Pro, et livrer le backend avant les interfaces. La démo s’appuie sur les commandes ordinaires du produit. La recette web compare notamment une vignette Live, une carte Marketplace et une fiche Pro après publication.
