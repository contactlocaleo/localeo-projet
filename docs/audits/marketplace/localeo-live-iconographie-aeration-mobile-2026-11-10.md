# Localeo Live — iconographie et respiration sur mobile

**Suite réalisée localement le 10 novembre 2026 : spécification puis implémentation.**
Les dix recommandations sont reprises dans [E73-EVO-LIVE-ICONOGRAPHIE](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-10-novembre-2026--iconographie-et-respiration-e73-evo-live-iconographie).
La [conception §14](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md#14-iconographie-et-respiration--e73-evo-live-iconographie)
et le [bilan IA](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#évolution--e73-evo-live-iconographie-10-novembre-2026)
portent la réalisation et ses preuves ; le constat initial ci-dessous reste daté.

Audit ciblé du **10 novembre 2026**, à la demande de l'utilisateur après
l'amélioration des parcours : renforcer l'iconographie au profit du texte et
aérer les zones, en conservant l'esprit **carnet de bord digital** et la
lisibilité de Localeo Pro. Ce rapport propose des évolutions ; il ne les implémente
pas et ne modifie pas le statut de l'epic.

## Diagnostic

La direction artistique est désormais identifiable : fond calme, actions vertes,
navigation stable, tampons et objets personnels. Le gain suivant vient d'une
meilleure répartition de l'information. Les cartes remplies accumulent encore
type, titre, état, explication, cadre de progression et bouton ; à l'inverse,
certains états vides occupent beaucoup d'espace sans aider davantage à choisir.

**Recommandation : une icône d'objet, un état explicite, une progression visuelle
et une action principale.** Supprimer les répétitions libère la place nécessaire
pour espacer les groupes. Augmenter uniformément les marges ferait descendre le
premier geste utile, particulièrement à 320 × 568.

Les pictogrammes doivent d'abord renseigner : le cadeau désigne actuellement
coffrets et lots, tandis que la page Mes lots alterne cadeau et trophée. La coche
appliquée à tous les lots historiques est un défaut de sens à corriger en priorité.

## Périmètre et preuves

| Source | Observation et limite |
| --- | --- |
| TEST, `https://test-animations.localeo.city/` | Inspection Chromium mobile automatisée en contexte neuf à 390 × 844 et 320 × 568. Entrée redirigée vers `/live/decouvrir`, HTTP 200 ; asset principal observé `index-C203eTc4.js`. Le SHA déployé n'a pas été attesté. |
| Vues TEST observées | Découvrir sans commune, recherche et sélection locale de Latresne, programme vide, Mon carnet vide, Mes lots vide, récupération par e-mail. Aucune animation n'était affichée pour Latresne dans les deux périodes après lecture ; cela ne signifie pas que tout TEST est vide. Aucun formulaire d'inscription/récupération soumis, aucune géolocalisation demandée. |
| Sources applicatives | Marketplace propre au commit `b9fb30deb0a07e17b350b55f027cfe3a038695ad`. Lecture des composants et styles, complétée par une exploration indépendante en lecture seule. |
| Nouvelles vues locales | Six scénarios existants exécutés pour produire les captures : carnet vide/mixte à 320/360/390, collections de tampons/tickets à 320/390, fiche publique avec/sans flyer à 393. **6/6 réussis**, sortie 0, build isolé. Données synthétiques et API simulées. |
| Vues locales réexaminées | Captures de la recette précédente pour participation passeport 320, Mes lots rempli 390 et Découvrir rempli 320/390, décrites dans le [rapport précédent](localeo-live-mobile-participation-lots-decouverte-2026-11-10.md). Elles ne sont pas des captures personnelles de TEST ni de nouveaux tests exécutés. |

Le navigateur interactif et le service Windows Computer Use étaient indisponibles ;
la capture automatisée a permis l'inspection du site. Aucune donnée personnelle
réelle ni accès de l'habitant n'a été utilisé. Pas de mesure de compréhension
avec des habitants ou de confort sur téléphone physique.

Les captures pleine page représentent la navigation fixe à sa position dans le
viewport initial : sa présence au milieu d'une image longue ne prouve pas qu'un
élément situé plus bas serait inaccessible après défilement.

Captures et sorties de travail, non versionnées dans le dépôt documentaire :
`localeo-marketplace/tmp/live-iconographie-aeration-2026-11-10/` (TEST), sous-dossier
`local/` (nouvelle recette). Sources précédentes : `tmp/live-mobile-ux-complete/`
et `tmp/live-mobile-ux-final/`. L'état du navigateur de recette reste dans ces
sorties temporaires ; il ne fait pas partie du rapport à publier.

## Constats et recommandations

P1 : sens ou repérage d'une action importante. P2 : confort de lecture et
cohérence. Les propositions ci-dessous gardent les informations nécessaires aux
droits, à l'inscription et au retrait.

| ID | Priorité / preuve | Constat | Recommandation concrète |
| --- | --- | --- | --- |
| **IA-01** | P1 — code des lots ; incohérence cadeau/trophée également visible en TEST | Une coche représente tous les lots historiques, y compris expirés/annulés. Cadeau et trophée changent de sens selon titre, carte et navigation. | Réserver la coche à « Retiré/Utilisé ». Distinguer expiration, annulation, remplacement et refus de remise avec un pictogramme adapté et le libellé exact. Unifier Mes lots autour du cadeau ; représenter le coffret par une boîte distincte. |
| **IA-02** | P1 — carnet mixte local 320/390 + CSS | L'icône de couverture occupe une colonne sur toute la hauteur. À 320, le texte, les tampons et le bouton disposent de moins de largeur alors que la zone sous l'icône reste vide. | Limiter la colonne visuelle à la ligne identité/titre ; donner ensuite toute la largeur aux tampons, aux informations utiles et au bouton. Garder la tranche de carnet. Aérer les groupes à largeur constante avant d'augmenter la hauteur. |
| **IA-03** | P1 — participation locale 320 + composant QR | Le geste principal « Présenter mon QR personnel » est textuel, sans pictogramme QR, alors que des informations secondaires sont illustrées. | Associer un QR de la famille graphique à « Présenter mon QR ». Garder un seul bouton principal, ses états de vérification et son nom accessible. Le pictogramme ne remplace jamais la confirmation d'accès. |
| **IA-04** | P2 — participation locale + code passeport/tombola | Le titre du carnet, le cadre des tampons, le compteur et « Encore X tampons… » réexpliquent la progression. La tombola dispose de plusieurs blocs pour une même participation. | Un espace de progression : tampons + compteur exact ; une courte incitation seulement si elle ajoute une prochaine action. Conserver séparément le statut de qualification/gain. Réunir la tombola en ticket avec état et action. Éviter les cadres imbriqués autour de la même information. |
| **IA-05** | P2 — nouvelles fiches locales avec/sans flyer | « Votre défi », la phrase d'objectif, « X tampons à collecter » et « Objectif du parcours » se succèdent avant l'action. | Un objectif illustré par les tampons et une phrase courte ; retirer les sous-titres explicatifs redondants. Exemple passeport : empreintes + « 4 tampons à collecter ». Développer la mécanique dans Comment jouer ; garder avant engagement gain, condition essentielle et règlement. |
| **IA-06** | P2 — Découvrir local rempli 320/390 + CSS | La première carte est très comprimée : espaces de période à 4 px, padding de 12 puis 10 px sur petit écran. À 320, le CTA tient juste avant la navigation. | Récupérer de la place dans les répétitions et le regroupement du contexte commune/outils, puis viser 12–16 px de padding et entre groupes. Garder recherche et favoris visibles. Une ligne concise objectif/date, puis CTA ; gains et Garder/Partager dans un pied secondaire. Ne pas réduire la police pour financer l'espacement. |
| **IA-07** | P2 — lot rempli local + code | Type, état, absence d'échéance, vérification à l'ouverture et consignes peuvent produire plusieurs lignes de précautions séparées. Le même symbole apparaît dans la carte, l'état et le CTA. | Une icône de nature en tête, puis un état et les informations décisives. Regrouper les précisions dans « Informations de retrait » dépliable. État non confirmé et contrainte de retrait restent visibles ; conserver une indication explicite si l'échéance est inconnue. Pour un lot externe à retirer, CTA « Voir les consignes » avec repère de retrait plutôt que trophée répété ; bons et coffrets conservent leur action propre. |
| **IA-08** | P2 — sources et captures transverses | Plusieurs familles SVG coexistent ; la boussole représente découverte et parcours, le cadeau représente coffret et lot. Les filtres du carnet sont purement textuels tandis que les cartes multiplient les symboles. | Définir une correspondance objet/état/action commune, puis réutiliser les mêmes dessins dans titres, filtres et cartes. Tampons et tickets gardent leur traitement expressif distinct. Ne pas ajouter une icône à chaque ligne : une icône doit améliorer le repérage. |
| **IA-09** | P2 — TEST sans commune et programme vide | Le grand zéro « Suivies », les indications techniques et « Aucune commune suivie » répètent l'absence de choix ; dans le programme vide, deux périodes répètent le même message et le même lien. | Sans commune : repère de lieu, invitation « Choisir ma commune », recherche et Autour de moi ; capacité de dix communes et stockage dans l'aide. Après succès des deux lectures vides, présenter une invitation commune à changer de commune. Garder les périodes séparées en cas de résultat partiel ou d'erreur. |
| **IA-10** | P2 — TEST carnet/lots vides et récupération | Le carnet vide possède déjà de bons repères Parcours/Coffrets/Lots. Mes lots vide empile deux zéros, rubrique vide, texte de tirages, aide et récupération ; les formulations longues de récupération accentuent la densité à 320. | Réutiliser un état vide unique illustré dans Mes lots, puis Découvrir et récupération. Éviter les compteurs à zéro sans valeur d'orientation. Raccourcir les appels à « Retrouver mon carnet » avec la précision « Participations et lots, par e-mail » au bon endroit ; maintenir la récupération coffret distincte. Conserver le trio illustré du carnet vide. |

IA-01 sur l'icône d'état historique est un constat de code ; il n'a pas été
reproduit avec un vrai lot expiré en TEST. Les propositions IA-06 et IA-09 demandent
une nouvelle vérification du premier viewport après composition ; leur effet
n'est pas mesuré par les captures de l'interface actuelle.

## Grammaire iconographique proposée

Deux familles suffisent : **icônes utilitaires homogènes** pour reconnaître les
objets/actions, **tampons et tickets** pour ressentir la collection et le progrès.
Réutiliser les SVG existants ; aucune banque d'illustrations ou image générée
n'est nécessaire pour ce périmètre.

| Sens | Repère proposé | Texte à conserver |
| --- | --- | --- |
| Mon carnet | Carnet avec tranche | Mon carnet, dans la navigation. |
| Parcours / passeport | Parcours ou boutique selon le moteur | Nom de l'animation ; état personnel si utile. |
| Coffret | Boîte ou coffret ouvert, distinct du cadeau | Coffret, prestations restantes/utilisées et validité connue. |
| Lot | Cadeau ; ticket pour la nature bon numérique | Nom du gain, état confirmé et action de retrait/utilisation. |
| QR | Carrés de repérage d'un QR | Présenter mon QR. Vérification/indisponibilité si applicable. |
| Date / lieu | Calendrier / épingle | Date utile / nom du lieu ; aucune donnée inconnue remplacée par une icône positive. |
| Garder / partager | Marque-page / partage | Garder, Gardée, Partager : verbes courts, toujours compréhensibles. |
| État | Coche, horloge, annulation, remplacement selon le fait | Retiré, expiré, annulé, remplacé, à vérifier ; jamais la couleur seule. |
| Outils usuels | Actualiser, fermer, réglages | Icône seule possible si nom accessible, focus visible et zone tactile suffisante. |

Conserver les libellés des trois destinations basses, les retours contextuels,
les actions essentielles et les conditions légales. Messages/Menu sont déjà
courts : la priorité est d'alléger le contenu des cartes, pas d'effacer ces repères.
Les tampons décoratifs ne deviennent pas des boutons sans action réelle.

## Rythme d'espacement proposé

Valeurs de départ à valider sur captures, **pas mesures déjà obtenues** :

| Relation | Cible |
| --- | --- |
| Icône + libellé, éléments d'une même information | 8 px. |
| Titre + état associé | 4–8 px ; pas un espacement de section. |
| Deux groupes distincts dans une carte | 12–16 px. |
| Intérieur de carte | 16 px à 390 ; 12 px minimum à 320 après regroupement. |
| Deux cartes | 16 px. |
| Deux sections fonctionnelles | 24 px, à adapter au premier viewport. |
| Icône utilitaire / objet | 20–24 px / 28–32 px ; dessin optiquement homogène. |
| Commande tactile | Au moins 44 × 44 px ; 48 px possible pour l'action principale. |

Garder corps/actions à 14 px et titres selon LIVE-UX-09, champs mobiles à 16 px.
Une carte principale peut conserver sa bordure ; ses sous-groupes se séparent
d'abord par l'espace. Préserver une seule surface expressive pour les tampons.
Pour gagner de la hauteur, retirer un texte redondant avant de réduire un espace,
une cible tactile ou la taille de police.

## Ordre de réalisation et critères de recette proposés

1. **Sens et action** — IA-01/03/08 : établir la correspondance des icônes,
   corriger les états historiques et illustrer le QR. Vérifier chaque état,
   la compréhension sans couleur et les noms accessibles.
2. **Cartes et progression** — IA-02/04/05/07 : élargir le contenu utile, retirer
   les répétitions, regrouper les précisions. Vérifier passeport, chasse, tombola,
   coffret et lot, y compris état inconnu, expiration et refus.
3. **Respiration du programme et états vides** — IA-06/09/10 : appliquer la grille
   d'espacement après simplification du contenu ; maintenir recherche/favoris
   atteignables et conditions nécessaires visibles.

Recette attendue après réalisation :

- À 320 × 568 et 390 × 844, prochaine action du carnet et premier CTA nominal
  de Découvrir/Mes lots entièrement au-dessus de la navigation basse. Titres
  longs et texte à 200 % restent accessibles sans débordement horizontal.
- Identifier en regardant la carte son objet, son état et le geste proposé.
  Une expiration/annulation n'utilise plus de coche de réussite. Un état non
  confirmé reste explicitement non confirmé.
- Un seul compteur exact pour la progression ; qualification et gain restent
  des informations distinctes. Pas de points, série quotidienne ou nouvelle
  récompense ajoutés par le décor.
- Clavier, focus, lecteur d'écran, réduction du mouvement et chargement lent :
  mêmes repères, pas de déplacement d'une action pendant son utilisation.
- Mini-recette avec des habitants sur téléphone : retrouver un lot, reconnaître
  le bouton QR, distinguer coffret/lot, garder une animation. Observer hésitations
  et erreurs avant de supprimer davantage de libellés.

## Références de code et vérifications exécutées

Revue au SHA Marketplace indiqué plus haut ; lignes données pour cette version :

- [Lots](../../../../localeo-marketplace/src/live/LiveLots.jsx), lignes 42–58,
  et [états](../../../../localeo-marketplace/src/live/liveRewards.mjs), lignes 2–17 : nature, état historique et précisions de remise.
- [Carnet](../../../../localeo-marketplace/src/live/LiveUnifiedCarnet.jsx), lignes 195–209,
  et [styles](../../../../localeo-marketplace/src/live/live-unified-carnet.css), lignes 13–30/58 : colonne de couverture et contenu.
- [Bouton QR](../../../../localeo-marketplace/src/live/ParticipantQrAction.jsx), ligne 9,
  [participation](../../../../localeo-marketplace/src/live/LiveAnimationGame.jsx), lignes 108–123/286–290 : action et progression.
- [Fiche publique](../../../../localeo-marketplace/src/live/LivePublicAnimationView.jsx), lignes 136–139,
  et [styles](../../../../localeo-marketplace/src/live/live-public-detail.css) : répétitions de l'objectif et surfaces.
- [Découvrir](../../../../localeo-marketplace/src/live/LiveDiscovery.jsx), lignes 120–125,
  et [styles mobiles](../../../../localeo-marketplace/src/live/live-discovery.css), règles `max-width:600px` et `max-height:650px` : densité et CTA.
- [Famille utilitaire](../../../../localeo-marketplace/src/live/LiveActivityIcon.jsx),
  [navigation](../../../../localeo-marketplace/src/live/LiveApp.jsx) et
  [en-tête](../../../../localeo-marketplace/src/live/LiveCarnetHeader.jsx) : harmonisation à partir de l'existant.

Nouvelle exécution locale, port isolé 8286, **6/6 réussis en 42,7 secondes** :

```text
node node_modules/@playwright/test/cli.js test --config=playwright.desktop.config.cjs
  tests/visual/live-audit-carnet.spec.cjs:177
  tests/visual/live-unified-carnet.spec.cjs:153
  tests/visual/live-public-detail-fd.spec.cjs:128
  --workers=2 --timeout=30000
  --output=tmp/live-iconographie-aeration-2026-11-10/local
```

Ce sont des contrôles et captures de l'existant, pas une validation des propositions.
Une tentative de lecture JSON de catalogue sur l'origine frontend a renvoyé le
fallback HTML et n'a fourni aucune preuve ; les constats TEST reposent sur les
pages rendues. Les premières captures de carnet/lots en attente ont été remplacées
après leur lecture complète pour l'examen des états vides.

## Impacts

Rapport et index d'audit ajoutés dans `localeo-projet` ; sources applicatives
inchangées. Les modifications documentaires de l'évolution PM déjà présentes
sont préservées. Aucun contrat, migration, flag, donnée métier ou générateur modifié.
La réalisation envisagée concerne principalement Marketplace/Live, sans toucher
aux règles backend ni à Pro. Les réserves de revalidation des participations
du [bilan PM](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#évolution--e73-evo-live-parcours-mobile-10-novembre-2026)
restent ouvertes et distinctes de cet audit visuel.

Références durables : [principes LIVE-UX-02 à 09](../../produit/live/principes-ux.md),
[spécification E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md).

Contrôle documentaire : `py -3.14 -X utf8 scripts/check_guidance.py` avec l'index
et ce rapport ajoutés via `--document` : **99 guides, 1 239 liens, aucune erreur
ni avertissement**. Revue indépendante intégrée : proposition de libellé de
retrait explicitement limitée aux lots externes, pour préserver l'accès propre
des bons et coffrets. Aucun commit, push ni déploiement réalisé pour cet audit.
