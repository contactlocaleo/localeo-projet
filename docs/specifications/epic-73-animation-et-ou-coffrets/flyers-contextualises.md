# E73 — Flyers contextualisés

Évolution **E73-EVO-FLYER**, demandée le **22 octobre 2026**, rattachée aux
US02/04/05/06/23/29 et aux supports de communication de l'epic 41. Elle complète
les 63 critères initiaux sans les renuméroter ni modifier l'état de l'epic.
[Dossier E73](README.md), [backlog](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md),
[direction artistique existante](../epic-41-api/flyer-direction-artistique.md).

## Écart fonctionnel

Le flyer doit présenter la dotation effectivement choisie. La promesse historique
« coffret local digital » ne convient pas à une animation dotée de lots libres.
Le document met en évidence le nombre d'exemplaires à gagner et le nombre de
commerçants participants. Le gestionnaire peut remplacer son illustration par
une image personnelle, puis revenir à l'illustration habituelle.

| Dotation | Promesse sur le flyer | Remise évoquée |
| --- | --- | --- |
| Coffrets | Coffret(s) à gagner | Parcours Coffrets existant |
| Lots libres, gestion externe | Lot(s) à gagner, sans promesse de coffret ou de bon QR | Modalités communiquées par l'organisateur |
| Lots libres, bons numériques | Lot(s) à gagner sous forme de bons numériques | Présentation du bon au commerçant chargé de la remise |

Le choix de dotation demeure celui de l'animation ; le formulaire du flyer ne
permet pas de le modifier. La mécanique de participation reste celle du modèle
d'animation. Un scan de passage n'est pas présenté comme une remise de lot.

## Critères ajoutés

| ID | Résultat observable | Preuve attendue |
| --- | --- | --- |
| E73-CA-FLYER-01 | PDF, aperçu et informations du portail correspondent aux trois modes de dotation ; aucun texte Coffrets ne subsiste pour les lots libres | Tests de domaine des trois branches et rendu de chaque variante |
| E73-CA-FLYER-02 | Deux nombres lisibles : exemplaires à gagner et commerçants dont la participation est confirmée ; singulier/pluriel corrects | Plusieurs exemplaires d'un même modèle, invitation en attente/refusée exclue, consommation d'un bon sans diminution artificielle du total annoncé |
| E73-CA-FLYER-03 | Ajout/remplacement d'une illustration propre au flyer, aperçu et retour à l'image habituelle du PDF ; Live reprend uniquement l'illustration personnalisée si elle existe | Aller-retour navigateur et rendu PDF avec images paysage/portrait puis retrait ; blocs Live avec et sans illustration |
| E73-CA-FLYER-04 | Seuls les gestionnaires habilités sur l'animation peuvent modifier l'image ; formats, volume et dimensions contrôlés côté serveur | Lecteur/autre organisation refusés, faux fichier image et dépassements refusés sans modification |
| E73-CA-FLYER-05 | Une modification rend le support obsolète ; régénération explicite, versionnée, cohérente avec les faits métier courants et sans écrasement concurrent | Changement image/dotation/participants, conflit de version, rejeu de commande et publication |

## Règles de conception et contrats

Le domaine `animation_locale` prépare les libellés et les nombres ; le renderer
et le portail les présentent. L'application charge les faits par les ports
existants : quantités Coffrets configurées, compteur de dotation libre
`nombre_unites`, participation effective. Un type de lot disponible en trois
exemplaires représente trois lots. Les exemplaires déjà gagnés ou consommés ne
deviennent pas un « stock restant à gagner » sur le support de communication.
Les commerçants simplement sélectionnés ou invités ne sont pas comptabilisés.

Les lectures de dotation utilisent le compteur déjà maintenu, sans chargement
de l'intégralité des bons, gains ou participants clients. Le calcul des
commerçants réutilise la décision de participation effective, y compris lors de
la publication avant enregistrement de sa liste figée.

L'empreinte source du flyer comprend la dotation, les compteurs et l'identité de
l'illustration. La génération conserve le pipeline existant : capture des faits,
rendu et stockage hors transaction longue, puis relecture et rattachement
conditionnel. Une modification concurrente ne doit pas publier un rendu annoncé
à jour sur des faits devenus obsolètes. Les PDF déjà imprimés ne sont pas modifiés :
le gestionnaire doit télécharger et diffuser la nouvelle version.

L'image est rattachée à l'animation. Depuis le correctif du **31 octobre 2026**,
les blocs de présentation de Localeo Live reprennent aussi cette illustration
personnalisée, uniquement lorsque l'animation est visible du public. Sans image
personnalisée, après retrait ou en cas d'échec de chargement, Live n'affiche
aucune illustration ni emplacement vide. Il n'utilise ni aperçu PDF, ni photo
par défaut, ni autre asset de l'animation. Le visuel de jeu et
`visuel_principal_asset_id` restent indépendants. Le stockage
documentaire existant est réutilisé ; aucune URL distante arbitraire n'est
téléchargée et aucun accès global au DAM n'est ouvert. PNG, JPEG et WebP sont
acceptés dans la limite de **5 Mio** ; le serveur vérifie le contenu décodé,
borne les dimensions et neutralise les métadonnées. L'image est recadrée dans
le bloc existant, sans déformer le logo ni masquer le QR d'inscription.

Le contrat ajoute sous `/protected/animation-locale/animations/{animation_id}` :

| Opération | Entrée / résultat |
| --- | --- |
| `GET /flyer` | Informations existantes et `nombre_lots`, `nombre_commercants`, `mode_dotation`, `gestion_libre`, `libelle_dotation`, `animation_version`, `illustration_url`, `illustration_personnalisee_url` |
| `GET /flyer/illustration` | Image effective binaire avec contrôle d'accès et cache privé désactivé |
| `PUT /flyer/illustration` | JSON `expectedVersion`, `image_base64` et en-tête `Idempotency-Key` ; reçu avec la nouvelle version de l'animation |
| `DELETE /flyer/illustration` | JSON `expectedVersion` et même mécanisme d'idempotence ; retour au visuel habituel |
| `GET /flyer/illustration/commandes/{cle}` | Réconciliation d'une commande dont la réponse a été perdue, sans nouveau dépôt |

Les valeurs de dotation sont `COFFRETS` ou `LIBRE` ; les valeurs de gestion
libre sont `EXTERNE` ou `NUMERIQUE`. Les compteurs complémentaires restent
facultatifs pour les consommateurs historiques de listes ; une valeur absente
ne vaut pas zéro. La liste globale indique **PDF disponible**, sans promettre
sa fraîcheur ; le détail contrôle l'empreinte et affiche **À régénérer** si les
faits courants diffèrent du document.

Le binaire décodé est limité à 5 Mio, sa représentation base64 à 6 990 508
caractères. L'image doit être fixe, avoir au moins 64 pixels par côté et au plus
24 millions de pixels ; elle est normalisée en PNG RGB de 2 400 pixels maximum
par côté, puis réduite si nécessaire à 2 Mio maximum pour le stockage documentaire
existant, sans EXIF ni géolocalisation. Le stockage utilise un document
`FLYER_ANIMATION_ILLUSTRATION` rattaché à l'animation. Son administration reste
privée dans le portail. Sa seule image personnalisée peut être servie par
`GET /public/animation-locale/animations/{animation_id}/illustration-flyer`,
après contrôle de visibilité publique de l'animation et de son rattachement
exact. La projection publique `visuel_url` désigne cette route, ou vaut `null`.
Le binaire est contrôlé par empreinte et servi sans cache ; les documents
archivés et les médias des autres animations restent inaccessibles par ce chemin.
Les illustrations remplacées sont archivées ; les fichiers préparés puis non
rattachés suivent la conservation des fichiers de flyer. Aucun ajout de colonne
ou nouvelle clé de configuration n'est requis.

Dans le PDF, le retrait de l'image personnalisée rétablit la sélection historique : visuel
de l'animation lorsqu'il existe, sinon photographie Localeo embarquée. La
régénération d'un aperçu brouillon reste privée ; les règles existantes de
publication documentaire et de téléchargement sont conservées.

## Accès et recette métier

Dans **Localeo Animation → animation concernée → Flyer**, contrôler le mode et
les nombres affichés, choisir une illustration, puis régénérer et télécharger
le flyer. Le menu global **Flyers** permet de retrouver l'animation concernée.

Préparer trois animations de la même commune autorisée : Coffrets, lots externes
et bons numériques, avec une dotation connue et au moins un commerce confirmé
et un commerce seulement invité. Préparer un JPEG paysage, un PNG portrait et
un fichier non image ; disposer d'un gestionnaire autorisé et d'un lecteur.

1. **RM-FLYER-01** : ouvrir successivement les trois animations, générer puis
   télécharger leur flyer. Vérifier la promesse propre au mode, les quantités
   connues, le nombre de commerces confirmés, les dates et le QR d'inscription.
2. **RM-FLYER-02** : sur l'animation à bons, utiliser plusieurs exemplaires du
   même modèle. Vérifier qu'ils sont comptés séparément. Après attribution/remise
   d'un bon, régénérer : son utilisation ne doit pas réduire le total annoncé.
3. **RM-FLYER-03** : choisir le JPEG, vérifier l'aperçu, enregistrer et régénérer.
   Télécharger le PDF puis recommencer avec le PNG portrait. L'image remplace
   celle du flyer et des blocs Live publics ; texte et QR restent visibles.
   Retirer l'image, régénérer, vérifier le retour au visuel habituel du PDF et
   l'absence d'illustration sur Live. Une image retirée ne doit pas réapparaître
   depuis un ancien document archivé ou l'aperçu généré.
4. **RM-FLYER-04** : soumettre un fichier non image puis un fichier dépassant
   5 Mio. Vérifier le refus compréhensible et la conservation de l'image
   enregistrée. Avec le lecteur, vérifier l'absence de commande d'édition.
5. **RM-FLYER-05** : ouvrir deux onglets gestionnaire, modifier l'image dans le
   premier, puis tenter une écriture depuis l'état ancien du second. Vérifier
   qu'un conflit demande une actualisation sans écraser le premier changement.
   Contrôler le statut du flyer et sa nouvelle version après régénération.

Ces scénarios sont **à exécuter en recette**. Les preuves locales et leurs limites
sont consignées dans le [suivi](suivi-implementation.md), séparément des
validations de l'environnement de test.

## Impacts

- Backend : contenu métier, faits de génération, illustration documentaire,
  contrôle d'accès, contrats HTTP et PDF/PNG.
- Localeo Animation : édition du visuel et présentation des informations du
  flyer, consommation des contrats et états de reprise.
- Pro/Marketplace : pas de nouveau formulaire ; les consommateurs du flyer
  publié bénéficient du document contextualisé. Live affiche l'illustration
  personnalisée seule dans ses blocs de présentation publics, sans repli.
- Données historiques : pas de conversion de dotation ; absence d'image dédiée
  compatible avec le comportement antérieur. Les anciens PDF nécessitent une
  régénération pour bénéficier du nouveau contenu.
- Générateur : absence d'image personnalisée admise ; aucun secret ni nouvelle
  donnée obligatoire. Les fixtures des trois modes servent aux tests locaux,
  sans génération distante implicite.
- Exploitation : stockage documentaire existant et droits associés ; aucune
  activation commerciale supplémentaire. Les détails du contrat et les preuves
  de livraison sont complétés dans le suivi une fois l'implémentation vérifiée.
