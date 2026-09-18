# Audit UX de la Marketplace Localeo — Epic 54

> Date de l’audit : 31 août 2026  
> Référence de marque : [localeo.city](https://localeo.city)  
> Environnement audité : [test-marketplace.localeo.city](https://test-marketplace.localeo.city/accueil)  
> Version auditée : `0b48f4a`

## 1. Contexte et périmètre

La Marketplace Localeo a été refondue pour se rapprocher de l’identité visuelle de `localeo.city`, tout en conservant les exigences propres à un parcours transactionnel : rechercher un territoire, comparer les offres, consulter un coffret ou un commerçant, acheter puis accéder à l’expérience Localeo Live.

L’audit vérifie quatre dimensions prioritaires :

- le potentiel de CTR et de conversion des appels à l’action ;
- la lisibilité et l’accessibilité perçue ;
- le respect de la charte graphique et de l’ambiance de `localeo.city` ;
- la réalité de l’approche mobile first, au-delà de la seule adaptation responsive.

L’équilibre cible est d’environ **70 % de continuité avec la marque Localeo** et **30 % d’adaptation aux usages e-commerce**. Il ne s’agit pas de reproduire le site institutionnel page par page : la Marketplace doit rester efficace pour rechercher, comparer, acheter et utiliser un coffret.

Deux exigences de marque complètent ce cadre :

- l’offre doit être présentée sous le nom visible **« Localeo Coffrets »**, avec le logo Localeo Coffrets repris dans le header et le footer ;
- la direction doit rester **premium, qualitative et désirable**, afin de donner envie de découvrir les coffrets, sans reprendre les codes d’une marketplace discount.

### Environnement et limites

- Le domaine `marketplace.localeo.city` ne résolvait pas lors de l’audit. Si ce domaine correspond à la production attendue, son DNS ou son déploiement doit être contrôlé en priorité.
- L’analyse fonctionnelle et visuelle a donc été conduite sur `test-marketplace.localeo.city`, version `0b48f4a`.
- Aucun contenu de la base de données n’a été modifié. Les recommandations portant sur les contenus concernent uniquement les textes statiques ou leur présentation.
- Aucune variation de CTR n’est annoncée comme certaine sans données analytiques. Les effets commerciaux décrits sont des hypothèses UX à valider par la mesure.
- Les constats d’accessibilité ne constituent pas une certification WCAG complète.

### Parcours couverts

- accueil et recherche territoriale ;
- résultats de recherche ;
- page ville ;
- catalogue de coffrets ;
- fiche coffret ;
- fiche commerçant ;
- commande, paiement et confirmation ;
- erreurs et états de chargement ;
- passage vers Localeo Live ;
- Localeo Live : header, fil d’activité, filtres, cartes, navigation basse, états et responsive ;
- navigation globale, header et footer.

### Viewports contrôlés

`320`, `360`, `390`, `430`, `768`, `1024` et `1440 px`.

## 2. Résumé exécutif

La refonte atteint clairement son objectif de continuité avec `localeo.city` : typographies condensées, bleu profond, orange, photographie locale, titres éditoriaux et géométrie franche. La Marketplace appartient désormais visuellement au même écosystème.

L’efficacité transactionnelle reste néanmoins partiellement dégradée par trois problèmes prioritaires :

1. sur mobile, le CTA d’achat fixe de la fiche coffret est positionné hors du viewport ;
2. dans le catalogue, le bloc d’activité locale précède les produits et éloigne fortement le premier CTA commercial ;
3. dans les confirmations mobiles, le statut de paiement est écrit en blanc sur un fond devenu transparent et devient illisible.

Deux problèmes transverses affectent également la lisibilité et le potentiel de clic :

- les CTA orange avec texte blanc présentent un contraste mesuré à `2,49:1`, insuffisant pour du texte courant au regard de WCAG 2.2 AA ;
- sur mobile, le texte explicitant la proposition de valeur est masqué : le slogan et la recherche restent visibles, mais le concept de coffret Localeo est moins immédiatement compréhensible.

Enfin, plusieurs informations sont encore présentées comme de simples capsules textuelles sur fond arrondi. Un système de vignettes associant pictogramme local, libellé et donnée essentielle améliorerait la lecture rapide et renforcerait le caractère visuel de la Marketplace.

**Conclusion générale :** la direction visuelle est réussie. Les parcours de conversion mobile, le contraste et certains composants d’information doivent être sécurisés avant de considérer l’Epic 54 comme totalement terminé.

## État d’implémentation au 1er septembre 2026

> Cet état reflète le working tree après traitement de l’audit. Les constats et preuves des sections suivantes sont conservés comme photographie historique de la version auditée `0b48f4a` ; ils ne doivent pas être interprétés comme des anomalies encore toutes présentes.

### Terminé

- **UX-01** — Statuts de confirmation rendus lisibles sur mobile.
- **UX-02** — Barre d’achat mobile repositionnée et rendue effectivement visible.
- **UX-03** — Première offre remontée avant le bloc d’activité locale.
- **UX-04** — Contraste des CTA corrigé et contrôlé.
- **UX-05** — Proposition de valeur concise réintroduite sur l’accueil mobile.
- **UX-06** — CTA d’achat ajouté sous le prix mobile.
- **UX-08** — Header des pages internes compacté sur mobile afin de restituer de la hauteur utile.
- **UX-09** — Résultats mobiles recomposés avec pictogramme, libellé et nom sur des lignes distinctes ; le nom peut occuper jusqu’à deux lignes.
- **UX-10** — Contraste de l’action « Changer de commune » amélioré.
- **UX-11** — Sur la confirmation particulier en échec, les actions de support et de retour au catalogue sont placées directement sous le message ; le parcours professionnel disposait déjà de ses actions dans le hero.
- **UX-12** — Pluriels corrigés dans les sources actives, sans modifier les contenus provenant de la base.
- **UX-13** — Vignettes iconographiques étendues au catalogue, à la fiche coffret et à la commande professionnelle ; les ressources restent locales.
- **UX-14** — Rythme vertical resserré et contrôlé sur mobile et desktop, avec suppression des doubles espacements entre sections.
- Le logo et la dénomination **« Localeo Coffrets »** sont intégrés au header et au footer.
- Les filtres de Localeo Live disposent d’un traitement iconographique.
- Les vignettes iconographiques sont déployées sur l’accueil, la page ville, le catalogue, la fiche coffret, la fiche commerçant, la commande, la recherche et les garanties de confirmation.
- Les polices, icônes et ressources indispensables au rendu sont servies localement.
- Les contrôles responsive et de contraste prévus pour cette passe sont automatisés et exécutés.

La validation finale ciblée de **UX-08**, **UX-09**, **UX-11**, **UX-13** et **UX-14** est réussie.

### Partiel

- **Simplification premium et photographie** — La charte, les principes et les anti-patterns sont formalisés. Les médias issus de la base n’ont volontairement pas été modifiés ; leur sélection, leur qualité et leur gouvernance nécessitent une action éditoriale distincte.

### À décider ou dépendance externe

- **UX-07** — Caractère obligatoire ou optionnel du téléphone : décision métier nécessaire.
- Résolution ou déploiement du domaine de production `marketplace.localeo.city` : dépendance d’infrastructure externe au correctif UI.
- Politique d’usage, de transparence et de traçabilité des images générées : validation produit, marque et juridique nécessaire.
- Outil, consentement et conventions de mesure du CTR et du tunnel : cadrage analytique à valider.

### Validation technique effectuée

- lint : réussi ;
- build de production : réussi ;
- validation serveur : réussie ;
- tests visuels : **32 scénarios réussis sur 32** lors de la passe finale ;
- scénarios ciblés catalogue, fiche coffret et bloc animation : **3 réussis sur 3** ;
- les attentes asynchrones de Localeo Live ont été rendues plus robustes afin de ne pas confondre le chargement différé avec une régression visuelle.

## 3. Notation synthétique

| Critère | Note | Justification |
|---|---:|---|
| Continuité avec la marque | 8,5/10 | Univers immédiatement reconnaissable et proche de `localeo.city`. |
| Efficacité transactionnelle | 5,5/10 | Produits et achat trop éloignés dans plusieurs parcours mobiles. |
| Potentiel de CTR | 5,5/10 | Recherche efficace, mais CTA catalogue et achat mal positionnés. |
| Lisibilité | 6,5/10 | Bonne hiérarchie générale, dégradée par les contrastes et la confirmation mobile. |
| Mobile first | 6/10 | Aucun débordement, mais ordre des contenus et CTA d’achat problématiques. |
| Cohérence entre les pages | 8/10 | Le système graphique reste stable de l’accueil aux pages métier. |
| Accessibilité perçue | 5/10 | Sémantique globalement correcte, mais défauts visuels critiques et contraste insuffisant. |
| Confiance et réassurance | 7,5/10 | Prix, validité, paiement sécurisé et utilisation sont bien expliqués. |

## 4. Points réussis à préserver

- L’accueil restitue l’impact visuel de `localeo.city`.
- La recherche territoriale demeure l’action principale.
- Le CTA de recherche reste visible dans le premier écran à toutes les largeurs contrôlées.
- Aucun débordement horizontal n’a été détecté entre 320 et 1 440 px.
- Les zones tactiles principales mesurent généralement entre 48 et 54 px de haut.
- La page ville fonctionne particulièrement bien sur mobile : identité, proposition, CTA et statistiques tiennent dans le premier écran.
- Les cartes coffret donnent une bonne visibilité au prix, à la durée et au nombre d’expériences.
- La fiche commerçant présente un CTA clair à la limite du premier viewport mobile.
- Localeo Live conserve une personnalité d’application mobile tout en restant affilié à la marque.
- La recherche utilise une combobox, une liste de résultats et des options accessibles.
- Le header et le footer créent une continuité cohérente entre les produits Localeo.
- Les polices et ressources indispensables à la refonte sont auto-hébergées.
- Les CTA qui affichent directement le prix réduisent l’ambiguïté transactionnelle.

## 5. Registre des constats

| ID | Page / viewport | Observation et preuve | Impact supposé | Priorité | Recommandation | Effort | Mesure de validation |
|---|---|---|---|---|---|---|---|
| UX-01 | Confirmation, ≤ 720 px | Les textes du statut sont blancs sur fond transparent. | Information critique invisible après paiement. | P0 | Restaurer le fond bleu ou afficher les textes en bleu encre sur fond clair. | Faible | Captures de référence des statuts succès, attente et erreur. |
| UX-02 | Coffret, 390 px | Le CTA mobile est déclaré fixe, mais sa boîte apparaît vers `5 165 px` pour un viewport de `844 px`. | Achat inaccessible sans défilement très long. | P0 | Monter la barre au niveau racine de l’application et supprimer tout ancêtre modifiant son repère de positionnement. | Moyen | CTA visible au premier écran ; clic achat par viewport. |
| UX-03 | Catalogue, tous viewports | À 390 px, le premier produit commence vers `1 364 px` et son premier CTA vers `2 109 px`. Sur desktop, le premier produit commence encore vers `1 254 px`. | Forte perte probable d’impressions et de clics produit. | P1 | Afficher le premier coffret après les filtres ; déplacer l’activité locale après les produits ou la rendre compacte et repliable. | Moyen | Impression produit → clic « Offrir » ; profondeur de scroll. |
| UX-04 | CTA orange, tous viewports | Contraste texte blanc / orange mesuré à `2,49:1`. | Lecture difficile, notamment sur mobile et en extérieur. | P1 | Utiliser le bleu encre sur l’orange ou assombrir la couleur d’action jusqu’au seuil requis. | Faible | Contraste automatisé ≥ `4,5:1` pour le texte courant. |
| UX-05 | Accueil, 320–430 px | Le paragraphe de proposition de valeur et l’aide de recherche sont masqués. | Le concept de coffret est moins clair pour un nouvel utilisateur. | P1 | Conserver une phrase mobile courte : « Un coffret numérique à offrir et à vivre localement ». | Faible | Recherche engagée ; temps avant première interaction ; retours arrière. |
| UX-06 | Coffret, mobile | Le prix est visible, mais le bouton principal du formulaire apparaît vers `1 731 px`. | Rupture entre intention d’achat et action. | P1 | Ajouter un CTA explicite directement sous le prix, y compris après correction de la barre fixe. | Faible | Vue fiche → clic achat. |
| UX-07 | Coffret / commande | Le téléphone est obligatoire alors que l’aide le présente comme utile seulement en cas de problème. | Friction et abandon potentiel. | P1 | Valider le besoin métier ; tester un champ optionnel ou demandé après l’achat. | Moyen | Abandon par champ ; taux de validation du formulaire. |
| UX-08 | Pages internes, mobile | Header d’environ `131 px`, puis fil d’Ariane d’environ `48 px` : le contenu commence vers `203 px`. | Réduction du premier écran utile. | P2 | Réduire le header après navigation ou remplacer la recherche par une action compacte. | Moyen | Hauteur utile ; scroll avant première action. |
| UX-09 | Recherche, 320–390 px | Les résultats d’adresses sont fortement tronqués sur deux colonnes. | Difficulté à distinguer des établissements similaires. | P2 | Présenter chaque résultat sur deux lignes : nom complet, puis type et commune. | Faible | Sélection du premier coup ; reformulations de recherche. |
| UX-10 | Page ville, desktop | « Changer de commune » manque de contraste sur la photographie sombre. | Action secondaire difficile à identifier. | P2 | Utiliser contour et texte blancs, ou déplacer l’action hors de l’image. | Faible | Clic « Changer de commune ». |
| UX-11 | Confirmation, mobile | Les actions de reprise apparaissent vers `2 065 px`. | Un utilisateur inquiet doit beaucoup défiler pour agir. | P2 | Placer une action de reprise ou de contact directement après le statut. | Faible | Clic support / reprise ; sorties de page. |
| UX-12 | Plusieurs pages | Libellés tels que `1 adresse(s)` ou `1 coffret(s)` visibles. | Baisse de qualité perçue et de confiance. | P3 | Gérer singulier et pluriel dans les textes statiques, sans toucher aux données de test. | Faible | Revue de contenu automatisée. |
| UX-13 | Accueil, ville, coffret, commerçant, confirmation | Plusieurs vignettes sont de simples textes dans un fond arrondi. | Lecture moins immédiate et impression d’interface générique. | P2 | Créer un système de vignette avec icône locale, intitulé court et information essentielle ; réserver les capsules aux filtres et statuts. | Moyen | Tests de compréhension ; temps d’identification ; cohérence visuelle. |
| UX-14 | Tous parcours, tous viewports | Des marges, `padding`, `gap` et hauteurs minimales s’additionnent entre certains blocs, avec jusqu’à plus de `100 px` de respiration sur l’accueil desktop. | Parcours ralenti, CTA repoussés et impression de contenu artificiellement étiré. | P1 | Définir une échelle d’espacement commune, supprimer les doubles espacements et contrôler la profondeur de défilement. | Moyen | Mesure automatisée des espacements, captures multi-viewport et position des CTA. |

### Exigences de marque complémentaires

#### Identité « Localeo Coffrets »

- Le header et le footer utilisent le logo officiel Localeo Coffrets, dans une version locale et optimisée.
- Le nom visible de l’offre est « Localeo Coffrets » sur les points de contact structurants : header, footer, titres et métadonnées utiles.
- Le logo reste lisible sur fond clair et sombre, sans déformation, effet décoratif ou concurrence avec les CTA.
- Le lien porté par le logo ramène vers l’accueil de Localeo Coffrets et possède un nom accessible explicite.
- Localeo Live conserve sa propre appellation ; son affiliation à Localeo Coffrets doit être compréhensible sans brouiller son rôle d’application d’usage.

#### Direction premium, qualitative et désirable

L’interface doit favoriser la découverte et la projection dans les expériences proposées. Les leviers attendus sont une photographie éditoriale soignée, une hiérarchie calme, des espaces respirants, des détails précis, des textes utiles et une mise en valeur claire de chaque coffret.

Principes de direction artistique :

- **présentation épurée** : peu d’éléments simultanés, composition lisible et rythme éditorial respirant ;
- **belles photographies** : priorité aux images de produits, lieux, gestes et commerçants, avec des cadrages cohérents et une lumière naturelle ;
- **images générées crédibles** : lorsqu’une image est générée, rechercher un rendu documentaire réaliste et imparfait de façon crédible — lumière et cadrage naturels, lieux vécus, textures et petits détails — plutôt qu’une perfection publicitaire ;
- **peu de codes promotionnels** : le prix reste clair, mais ne remplace ni l’histoire, ni l’expérience, ni la qualité perçue ;
- **typographie élégante** : hiérarchie expressive mais contenue, longueurs de ligne maîtrisées et absence d’effets typographiques gratuits ;
- **mise en scène de la découverte** : chaque écran doit donner envie d’explorer un territoire, une expérience et les personnes qui la rendent possible ;
- **le commerçant et son savoir-faire deviennent presque le produit** : portraits, gestes, lieux et récits doivent contribuer autant au désir que la description fonctionnelle du coffret.

Critères d’acceptation :

- chaque coffret mis en avant possède une photographie qualitative et suffisamment grande pour créer de la projection ;
- lorsque les données sont disponibles, la fiche présente clairement le commerçant, son lieu et son savoir-faire avant l’accumulation de détails secondaires ;
- la première zone visible ne comporte qu’un message principal et un CTA dominant ;
- le prix est visible sans traitement criard, clignotant ou artificiellement urgent ;
- les écrans alternent respiration, photographie et information utile au lieu d’empiler des blocs uniformes ;
- l’ensemble reste lisible et désirable à 320 px comme à 1 440 px, sans supprimer les informations essentielles sur mobile ;
- aucun contenu de test issu de la base n’est réécrit pour satisfaire la direction artistique : la recette juge la mise en forme et prévoit les règles applicables aux contenus réels.
- toute image générée passe par un contrôle humain des mains, textes, produits, objets, architecture, perspective et cohérence avec le territoire représenté ;
- chaque asset généré dispose d’une traçabilité interne permettant d’identifier son origine, sa date, son usage, ses transformations et son statut de validation.

Les codes suivants sont à éviter :

- promotions agressives, prix barrés omniprésents ou compteurs artificiels ;
- accumulation de badges, pastilles et capsules ;
- couleurs saturées utilisées simultanément ;
- ombres fortes, dégradés décoratifs ou effets brillants systématiques ;
- surenchère de CTA concurrents ;
- densité excessive donnant une impression de catalogue à bas prix ;
- iconographie générique, emojis ou pictogrammes de styles incompatibles.
- photographies minuscules reléguées derrière des blocs de texte ou recadrées sans considération pour le sujet ;
- cartes répétitives donnant le même poids au prix, aux tags, aux métadonnées et au récit ;
- présentation du commerçant comme une simple ligne de données sans lieu, visage, geste ou preuve de savoir-faire lorsque ces médias existent ;
- titres en capitales, graisses et couleurs trop nombreuses au point de perdre l’élégance typographique.
- rendu publicitaire artificiellement parfait, peau ou objets excessivement lissés et éclairage de studio incohérent avec une scène locale vécue ;
- artefacts caractéristiques d’une génération défectueuse : mains ou membres incorrects, textes illisibles, produits déformés, architecture impossible, répétitions de motifs et incohérences de perspective ;
- images génériques ou culturellement incohérentes avec la commune, le commerçant, la saison ou l’expérience représentée.

#### Gouvernance des images générées

L’usage éventuel d’images générées ne doit ni tromper sur la réalité d’un produit ou d’un commerçant, ni remplacer sans justification une photographie réelle disponible. La priorité reste donnée aux images authentiques des lieux, produits, personnes et savoir-faire.

Pour chaque image générée retenue, une fiche interne de traçabilité doit au minimum consigner :

- un identifiant d’asset et le fichier final utilisé ;
- la date de génération et, si disponible, l’outil ou le modèle employé ;
- le prompt ou une description de l’intention visuelle ;
- les images de référence et les droits associés, le cas échéant ;
- les retouches et recadrages réalisés ;
- la page, le composant et le contexte d’utilisation ;
- le nom ou rôle de la personne ayant effectué le contrôle humain ;
- la décision de validation, de correction ou de rejet.

La politique de transparence publique doit être validée avec les responsables produit, marque et juridique. La traçabilité interne, elle, est requise dans tous les cas.

Les filtres, tags et statuts peuvent rester compacts ou prendre la forme de capsules lorsqu’ils ont une fonction claire. Les informations importantes doivent privilégier une vignette structurée, une mise en page éditoriale ou un couple pictogramme / libellé.

### Règles de conception pour UX-13

Une vignette informative devrait réunir :

- un pictogramme filaire cohérent de 24 à 32 px ;
- un intitulé court ;
- une valeur ou une information secondaire, si nécessaire ;
- une bordure ou un filet plutôt qu’une ombre importante ;
- un accent orange limité au pictogramme ou au repère actif ;
- une zone tactile d’au moins 44 × 44 px lorsqu’elle est interactive.

Exemples de correspondances :

| Usage | Pictogramme | Libellé possible |
|---|---|---|
| Durée | Calendrier | Valable 90 jours |
| Contenu | Cadeau | 1 expérience incluse |
| Réseau | Boutique | 3 adresses Localeo |
| Territoire | Localisation | À vivre à Latresne |
| Paiement | Bouclier | Paiement sécurisé |
| Livraison | Enveloppe | Envoyé immédiatement |
| Contact | Téléphone | Appeler le commerçant |
| Activité | Signal / activité | 3 signaux récents |

Contraintes :

- une icône ne remplace jamais le libellé principal ;
- les icônes décoratives portent `aria-hidden="true"` ;
- les SVG sont hébergés localement, sans CDN ni bibliothèque distante ;
- une seule famille visuelle est utilisée, sans mélange arbitraire d’icônes pleines, filaires ou d’emojis ;
- les capsules textuelles restent pertinentes pour les filtres, tags et statuts.

### Règles de contrôle du rythme vertical et des espacements

Chaque page et chaque étape de parcours doit être contrôlée sur les points suivants :

- espace entre le header, le fil d’Ariane et le premier contenu utile ;
- espace entre deux sections successives, entre un titre et son contenu, entre une photographie et son récit, puis entre le prix et le CTA ;
- cumul des `margin`, `padding`, `gap`, séparateurs et `min-height` qui peuvent créer une zone vide sans intention éditoriale ;
- cohérence de la densité entre accueil, ville, catalogue, fiche coffret, commerçant, commande, confirmation et Localeo Live ;
- profondeur de défilement avant la première offre, le premier CTA et les informations décisives ;
- comportement des espacements à `320`, `360`, `390`, `430`, `768`, `1024` et `1440 px`.

Une zone vide supérieure à `64 px` sur mobile ou `96 px` sur desktop doit être examinée et justifiée ; ces valeurs sont des seuils de revue et non des règles absolues. L’audit doit distinguer une respiration premium utile d’un vide qui casse la continuité, donne une impression de lenteur ou repousse l’action. Le rapport doit comporter une colonne **Rythme / densité** et une catégorie **Espacements et profondeur de défilement**.

## 6. Preuves responsive multi-viewport

| Largeur | Accueil | Catalogue | Fiche coffret | Conclusion |
|---:|---|---|---|---|
| 320 px | Recherche visible, aucun débordement | Produit vers `1 413 px`, CTA vers `2 158 px` | CTA d’achat absent du premier écran | Compatible techniquement, hiérarchie commerciale à revoir. |
| 360 px | Recherche visible | Produit vers `1 381 px`, CTA vers `2 126 px` | Même rupture transactionnelle | Le gain de largeur ne corrige pas l’ordre du contenu. |
| 390 px | Action principale claire, explication masquée | Produit vers `1 364 px`, CTA vers `2 109 px` | Barre fixe hors viewport | Viewport mobile de référence à sécuriser. |
| 430 px | Stable et sans débordement | Hiérarchie comparable à 390 px | Même rupture | Le problème est structurel, pas lié à une largeur isolée. |
| 768 px | Bonne transition tablette | Produit vers `1 215 px` | À confirmer après correction du CTA | Responsive stable, offre encore tardive. |
| 1024 px | Composition stable | Produit vers `1 216 px` | Parcours desktop correct | La densité verticale du catalogue reste élevée. |
| 1440 px | Forte continuité de marque | Produit vers `1 254 px` | Hiérarchie claire | L’activité locale retarde aussi le produit sur desktop. |

Constats transverses :

- aucun débordement horizontal détecté entre 320 et 1 440 px ;
- les zones tactiles principales sont généralement comprises entre 48 et 54 px ;
- la conception est responsive, mais pas encore complètement mobile first sur le catalogue et l’achat : l’ordre des contenus doit être revu, pas seulement leur largeur.

## 7. Audit par parcours

### 7.1 Accueil

La recherche est immédiatement identifiable sur desktop et mobile. Son bouton occupe toute la largeur disponible sur petit écran et reste dans le premier viewport, ce qui est favorable à l’engagement.

La photographie, le bleu et les titres assurent une forte continuité avec la marque. Sur mobile, la photographie devient toutefois presque imperceptible sous le voile bleu. La lisibilité progresse, mais la dimension humaine et territoriale s’affaiblit.

Le retrait de la phrase explicative mobile laisse le slogan porter seul la compréhension du service. Une phrase concise doit expliquer la notion de coffret sans alourdir le premier écran.

### 7.2 Recherche

Points positifs :

- catégories « Ville » et « Adresse » visibles ;
- liste accessible et options tactiles proches de 48 px ;
- résultats affichés rapidement ;
- recherche maintenue au centre du parcours.

À 320–390 px, les noms d’adresses et catégories sont trop tronqués. La présentation doit passer sur deux lignes afin de distinguer des établissements similaires.

### 7.3 Page ville

Il s’agit du parcours mobile le plus abouti :

- H1 immédiatement compréhensible ;
- CTA « Voir les coffrets » vers `512 px` ;
- statistiques visibles dans le premier écran ;
- navigation vers coffrets, animations, adresses et activité ;
- absence de surcharge avant l’action principale.

Sur desktop, l’action « Changer de commune » doit gagner en contraste. Les statistiques constituent une bonne cible pour les nouvelles vignettes iconographiques.

### 7.4 Catalogue

Les cartes sont lisibles et les CTA comme « Offrir — 29,00 € » sont explicites. Prix, validité et contenu sont bien hiérarchisés.

Le bloc d’activité locale interrompt cependant le parcours commercial avant le premier produit. À 390 px, il occupe approximativement la zone `578–1 239 px`, puis le premier produit commence vers `1 364 px`. L’intention de réassurance est pertinente, mais son emplacement réduit la probabilité d’exposition des offres.

### 7.5 Fiche coffret

Sur desktop, visuel, titre, prix et informations essentielles sont regroupés. Le CTA d’achat du premier écran est cependant moins saillant que les CTA orange du catalogue.

Sur mobile, le prix est visible, mais aucun CTA d’achat utilisable n’est présent dans le premier écran. Le bouton du formulaire arrive vers `1 731 px` et la barre supposée fixe est hors viewport. Il s’agit de la rupture transactionnelle la plus importante de la refonte.

Les attributs de durée, contenu, territoire et réassurance doivent être convertis en vignettes iconographiques homogènes.

### 7.6 Fiche commerçant

La version mobile fonctionne bien. Le CTA « Voir les coffrets associés » apparaît vers `782 px`, à la limite du premier écran. Sur desktop, le lien retour et le fil d’Ariane sont partiellement redondants.

Les coordonnées et informations pratiques bénéficieraient de pictogrammes explicites, sans retirer les libellés textuels.

### 7.7 Commande et paiement

Les garanties de paiement sécurisé, réception immédiate, durée de validité et commerçants partenaires rassurent correctement. Elles constituent un usage prioritaire des vignettes iconographiques.

Le caractère obligatoire du téléphone doit être validé par le métier : sa justification actuelle ne semble pas proportionnée à la friction créée.

### 7.8 Confirmation, erreurs et chargement

La structure éditoriale est claire, mais le statut principal est illisible sur mobile à cause du texte blanc sur fond transparent. Tous les états réutilisant le composant doivent être testés : succès, traitement, attente, erreur et reprise.

Une action de sortie ou de contact doit rester immédiatement proche du message principal. Les icônes de statut peuvent accélérer la compréhension, à condition que couleur et pictogramme ne soient jamais les seuls moyens de transmettre l’information.

### 7.9 Localeo Live

Localeo Live fait partie intégrante du périmètre de refonte. Il doit préserver son identité d’application mobile affiliée à Localeo, et non devenir une copie réduite de la Marketplace.

Points à préserver :

- personnalité visuelle propre, tout en conservant les couleurs et repères de marque ;
- premier contenu visible dans le premier écran mobile ;
- navigation basse adaptée à l’usage récurrent ;
- filtres horizontaux compatibles avec le tactile ;
- actions de header correctement nommées pour les technologies d’assistance.

Volets de recette dédiés :

- **header** : compacité, titre ou contexte courant, actions accessibles et zones tactiles ≥ 44 px ;
- **feed** : hiérarchie date / lieu / activité, chargement progressif, absence de saut de mise en page ;
- **filtres** : état actif perceptible sans dépendre uniquement de la couleur, défilement horizontal maîtrisé, remise à zéro accessible ;
- **filtres iconographiques** : pictogrammes cohérents et auto-hébergés, libellés toujours présents, densité limitée et distinction nette entre filtre actif et inactif ;
- **cartes** : image ou pictogramme pertinent, métadonnées lisibles, action principale explicite, densité limitée ;
- **navigation basse** : libellé associé à chaque icône, état actif clair, respect des zones sûres mobiles et absence de recouvrement du contenu ;
- **états** : chargement, vide, erreur, hors ligne et reprise cohérents avec la Marketplace ;
- **responsive** : priorité au mobile, mais utilisation maîtrisée de l’espace à 768 px et au-delà.

Sur desktop, Localeo Live peut conserver une largeur d’application contenue si cette décision est assumée. Il ne faut pas étirer artificiellement le feed ; les espaces supplémentaires peuvent accueillir du contexte utile sans transformer l’outil en dashboard SaaS générique.

### 7.10 Navigation globale, header et footer

Le header et le footer assurent une affiliation de marque solide. Sur les pages internes mobiles, leur hauteur cumulée avec le fil d’Ariane réduit cependant le premier écran utile. Une version compacte du header doit être envisagée après l’entrée dans un parcours.

## 8. Plan d’action priorisé

### Mode de traitement automatique des retours

Après chaque passe d’audit, tous les constats techniquement actionnables doivent être traités dans la même branche, puis vérifiés par lint, build et recette responsive. Le traitement couvre le code, les textes statiques, la présentation, l’accessibilité, les CTA, les espacements et les tests. Il ne doit jamais réécrire les contenus provenant de la base.

Les constats qui nécessitent une décision métier, une action d’infrastructure, un outil analytique, des droits sur un média ou une validation humaine / juridique ne doivent pas être arbitrairement tranchés. Ils restent explicitement listés avec leur dépendance, leur responsable attendu et leur critère de résolution. La fin de passe comprend une mise à jour de ce document, l’amendement du dernier commit et le push de la branche demandée.

### Corrections immédiates

- [x] **UX-01** — Corriger le statut blanc sur fond transparent.
- [x] **UX-02** — Rendre la barre d’achat mobile réellement fixe et visible.
- [ ] Vérifier le DNS ou le déploiement de `marketplace.localeo.city`.
- [x] **UX-04** — Corriger le contraste des CTA orange.

### Court terme

- [x] **UX-03** — Remonter le premier coffret avant l’activité locale.
- [x] **UX-05** — Réintroduire une proposition de valeur concise sur mobile.
- [x] **UX-06** — Afficher un CTA d’achat directement sous le prix.
- [x] **UX-08** — Réduire la hauteur du header des pages internes mobiles.
- [x] **UX-09** — Recomposer les résultats de recherche mobiles sur deux lignes.
- [x] **UX-10** — Améliorer le contraste de « Changer de commune ».
- [x] **UX-11** — Remonter une action de reprise sur les confirmations.
- [x] **UX-12** — Corriger les pluriels dans les textes statiques.
- [x] **UX-13** — Déployer le système de vignettes iconographiques.
- [x] **UX-14** — Réduire les espacements cumulés et automatiser le contrôle du rythme vertical.
- [x] Reprendre le logo officiel et la dénomination « Localeo Coffrets » dans le header et le footer.
- [x] Réaliser une passe de simplification visuelle pour supprimer les codes discount, badges superflus et capsules excessives sur les parcours traités.

### Optimisations à tester

- [ ] Activité locale avant ou après la première offre.
- [ ] Téléphone obligatoire ou optionnel.
- [ ] « Acheter ce coffret » contre « Offrir ce coffret — 29 € ».
- [ ] Texte bleu encre sur orange contre orange assombri et texte blanc.
- [ ] Hero mobile avec davantage de photographie visible.
- [ ] Densité et largeur desktop de Localeo Live sans perdre son orientation mobile.

## 9. Plan de mesure analytique

| Événement | Propriétés recommandées | KPI associé |
|---|---|---|
| `marketplace_search_started` | viewport, origine, commune active | Taux d’engagement recherche |
| `marketplace_search_result_viewed` | type, position, nombre de résultats | Qualité et exposition des résultats |
| `marketplace_search_result_selected` | type, position, requête | Recherche → sélection |
| `marketplace_city_viewed` | commune, origine | Sélection → page ville |
| `marketplace_offer_impression` | coffret, position, au-dessus du fold | Visibilité réelle des offres |
| `marketplace_offer_clicked` | coffret, CTA, position | CTR produit |
| `marketplace_merchant_clicked` | commerçant, provenance | Exploration des adresses |
| `marketplace_checkout_started` | coffret, viewport, source du CTA | Fiche → commande |
| `marketplace_checkout_field_error` | champ, type d’erreur | Friction formulaire |
| `marketplace_payment_started` | coffret, montant | Formulaire → paiement |
| `marketplace_payment_status_viewed` | succès, attente, erreur | Résultat du tunnel |
| `marketplace_purchase_confirmed` | coffret, type client | Conversion finale |
| `marketplace_live_clicked` | emplacement du CTA, origine | Passage vers Localeo Live |
| `localeo_live_filter_used` | filtre, position, nombre de résultats | Usage des filtres Live |
| `localeo_live_card_opened` | type, position, commune | Engagement avec le feed Live |
| `localeo_live_navigation_used` | destination, origine | Compréhension de la navigation basse |

Les indicateurs doivent pouvoir être segmentés par viewport, commune, position du produit et profondeur de scroll, sans collecter de données personnelles inutiles.

## 10. Décisions nécessitant une validation métier

1. **Téléphone obligatoire :** est-il réellement indispensable au paiement ou peut-il devenir optionnel ?
2. **Priorité catalogue :** l’activité locale doit-elle précéder les offres pour une raison commerciale démontrée ?
3. **Libellé d’achat :** faut-il privilégier « Acheter » ou « Offrir », et le prix doit-il toujours être inclus dans le CTA ?
4. **Domaine de production :** `marketplace.localeo.city` est-il le domaine cible et quel service en porte la résolution ?
5. **Localeo Live desktop :** l’interface doit-elle rester volontairement contenue comme une application mobile ou exploiter davantage la largeur ?
6. **Mesure du CTR :** quel outil analytique, quel consentement et quelles conventions d’événements sont retenus ?
7. **Icônes :** faut-il constituer une petite famille Localeo originale ou adapter une famille open source auto-hébergée, licence incluse ?
8. **Logo Localeo Coffrets :** quel fichier source officiel, quelles variantes colorimétriques et quelle zone de protection doivent être utilisés ?
9. **Périmètre de renommage :** la dénomination « Localeo Coffrets » doit-elle aussi apparaître dans les titres de page, métadonnées sociales, courriels transactionnels et documents imprimables ?

## 11. Checklist d’implémentation

### Fondations et accessibilité

- [x] Définir les couleurs d’action conformes aux seuils de contraste retenus.
- [x] Créer un composant partagé de vignette iconographique.
- [ ] Documenter la provenance ou la licence des pictogrammes SVG locaux lorsque cela est applicable.
- [ ] Fournir libellés, focus visibles et noms accessibles aux contrôles interactifs.
- [ ] Ajouter `aria-hidden="true"` aux pictogrammes purement décoratifs.
- [x] Respecter `prefers-reduced-motion`.

### Identité et qualité perçue

- [x] Intégrer le logo Localeo Coffrets dans le header et le footer, sans ressource distante.
- [x] Remplacer les appellations visibles ambiguës par « Localeo Coffrets » dans le header et le footer.
- [ ] Vérifier les variantes du logo sur fonds clair, bleu encre et photographique.
- [x] Maintenir une hiérarchie éditoriale calme, des espacements maîtrisés et un seul CTA principal par zone.
- [x] Limiter les badges aux informations véritablement discriminantes sur les parcours traités.
- [x] Réserver les capsules aux filtres, tags et statuts qui les justifient sur les parcours traités.
- [x] Écarter promotions agressives, artifices d’urgence et codes visuels discount sur les parcours traités.
- [ ] Contrôler la qualité, le cadrage et la cohérence colorimétrique des photographies.
- [ ] Donner la priorité aux photographies authentiques lorsque des visuels représentatifs et autorisés existent.
- [ ] Pour tout visuel généré, viser un rendu documentaire crédible : lumière naturelle, cadrage plausible, textures et imperfections maîtrisées.
- [ ] Écarter les visuels trop lissés, publicitaires ou présentant des artefacts de génération.
- [ ] Documenter l’origine, l’usage, les transformations et la validation humaine de chaque asset généré.
- [ ] Donner aux portraits, lieux, gestes et savoir-faire des commerçants une place éditoriale majeure.
- [ ] Organiser les fiches comme une découverte progressive : promesse, image, artisan / commerçant, expérience, informations pratiques, achat.

### Parcours Marketplace

- [x] Corriger les confirmations et tous leurs états.
- [x] Repositionner le CTA fixe de la fiche coffret.
- [x] Ajouter une action d’achat sous le prix mobile.
- [x] Recomposer l’ordre catalogue : filtres, première offre, réassurance / activité.
- [x] Réintroduire une explication courte sur l’accueil mobile.
- [x] Compacter le header des pages internes.
- [x] Corriger la présentation des résultats et les pluriels statiques.
- [x] Déployer les vignettes sur accueil, ville, catalogue, coffret, commerçant, commande et confirmation.

### Localeo Live

- [ ] Harmoniser le header sans supprimer l’identité d’application mobile.
- [ ] Vérifier le feed, sa densité et le chargement progressif.
- [ ] Garantir des filtres tactiles, lisibles et accessibles.
- [x] Ajouter des pictogrammes aux filtres lorsque cela accélère leur reconnaissance, sans supprimer leur libellé.
- [ ] Harmoniser les cartes avec les nouveaux repères visuels.
- [ ] Tester la navigation basse et les zones sûres mobiles.
- [ ] Prévoir les états vide, chargement, erreur, hors ligne et reprise.
- [ ] Définir le comportement tablette et desktop.

### Mesure

- [ ] Valider le dictionnaire des événements analytiques.
- [ ] Instrumenter impressions, clics, démarrage de commande et confirmation.
- [ ] Segmenter les résultats par viewport et position de contenu.
- [ ] Établir une référence avant modification pour comparer les résultats.

## 12. Checklist de recette

### Matrice responsive

- [x] Contrôler chaque parcours automatisé à 320, 360, 390, 430, 768, 1024 et 1 440 px.
- [x] Vérifier l’absence de débordement horizontal sur les scénarios automatisés.
- [x] Vérifier la visibilité du CTA principal dans le premier écran pertinent sur les scénarios couverts.
- [x] Contrôler automatiquement les espacements structurants et la profondeur de défilement des écrans couverts.
- [ ] Vérifier portrait, paysage et zones sûres mobiles.
- [ ] Tester les contenus courts, longs, absents et en erreur.

### Parcours transactionnel

- [ ] Recherche → ville → catalogue → coffret → commande → confirmation.
- [ ] Achat depuis tous les CTA disponibles.
- [ ] Validation et erreurs de chaque champ.
- [ ] Statuts succès, attente, échec et reprise.
- [ ] Navigation retour sans perte de contexte.

### Accessibilité et lisibilité

- [x] Mesurer les contrastes texte / fond et focus / fond prévus dans la recette automatisée.
- [ ] Tester le zoom navigateur à 200 %.
- [ ] Parcourir les pages au clavier uniquement.
- [ ] Vérifier l’ordre de focus et l’absence de piège clavier.
- [ ] Contrôler les noms accessibles des boutons et icônes.
- [ ] Vérifier que la couleur ou l’icône ne sont jamais les seuls vecteurs d’information.
- [x] Tester `prefers-reduced-motion` sur les scénarios automatisés concernés.

### Marque et qualité perçue

- [x] Vérifier la présence du logo Localeo Coffrets dans le header et le footer.
- [x] Vérifier le libellé « Localeo Coffrets » dans le header et le footer.
- [ ] Contrôler le logo à 320, 390, 768 et 1 440 px, sans compression ni recouvrement.
- [ ] Vérifier que le logo reste accessible et ne repousse pas l’action principale hors du viewport.
- [ ] Inventorier badges et capsules ; justifier chacun ou le retirer.
- [ ] Vérifier qu’aucune promotion agressive, fausse urgence ou surcharge tarifaire ne dégrade la qualité perçue.
- [ ] Comparer l’ensemble accueil / catalogue / coffret / commerçant / commande pour confirmer une perception premium cohérente.
- [ ] Faire valider qualitativement un échantillon de coffrets par des utilisateurs : désir de découverte, confiance et qualité perçue.
- [ ] Vérifier qu’au moins une belle image de produit, lieu ou commerçant structure chaque contenu éditorial majeur lorsque la donnée média existe.
- [ ] Vérifier que le commerçant et son savoir-faire sont identifiables sans parcourir toute la fiche.
- [ ] Contrôler l’élégance typographique : nombre de styles limité, lignes lisibles, contraste et rythme cohérents.
- [ ] Faire contrôler humainement chaque image générée à sa taille d’affichage et en haute définition.
- [ ] Inspecter particulièrement mains, visages, textes, logos, produits, objets, architecture, perspective et arrière-plans.
- [ ] Vérifier la cohérence locale : territoire, type de commerce, saison, signalétique, matériaux et contexte culturel.
- [ ] Vérifier la présence de la fiche de traçabilité interne et du statut de validation de chaque asset généré.
- [ ] Confirmer que l’image ne présente pas comme réel un produit, un lieu ou un commerçant fictif sans information appropriée selon la politique de transparence validée.

### Localeo Live

- [ ] Tester header, filtres, cartes et navigation basse à chaque largeur mobile.
- [ ] Vérifier que la navigation basse ne masque aucun contenu ou CTA.
- [ ] Vérifier les états actif, inactif, focus et désactivé des filtres.
- [ ] Tester feed vide, chargement, erreur réseau et reprise.
- [ ] Vérifier la cohérence de marque sans effacer l’identité propre de Live.
- [ ] Vérifier la lisibilité du feed, le contraste de chaque état et la reconnaissance des filtres iconographiques.

### Ressources et performance

- [x] Vérifier l’absence de Google Fonts, Adobe Fonts ou CDN public nécessaire au rendu.
- [x] Confirmer le chargement local des polices et icônes.
- [ ] Contrôler le poids, les dimensions et le format des images.
- [ ] Vérifier l’absence de saut de mise en page significatif au chargement.

## 13. Critères de clôture

L’audit peut être considéré comme traité lorsque :

- tous les P0 et P1 sont corrigés et recettés ;
- chaque P2 est corrigé ou fait l’objet d’une décision documentée ;
- la matrice responsive passe sans débordement ni CTA critique masqué ;
- les contrastes répondent aux exigences retenues ;
- la première offre du catalogue est exposée assez tôt pour être mesurable ;
- les vignettes iconographiques sont cohérentes, accessibles et auto-hébergées ;
- le logo et la dénomination « Localeo Coffrets » sont cohérents dans le header, le footer et les supports validés ;
- la recette ne relève aucun code visuel discount ou surcharge incompatible avec le positionnement premium ;
- chaque image générée est crédible, contrôlée humainement, cohérente avec son contexte local et traçable en interne ;
- Localeo Live est recetté comme partie du même écosystème, avec son identité mobile préservée ;
- les événements nécessaires au suivi du CTR et du tunnel sont validés ;
- les choix métier en suspens sont tranchés et consignés.

## 14. Conclusion

La Marketplace semble clairement appartenir au même écosystème que `localeo.city`. La marque renforce la confiance et la cohérence, mais certaines décisions de composition retardent encore les actions commerciales.

Le CTA principal est évident sur l’accueil et la page ville, mais pas encore sur le catalogue ni sur la fiche coffret mobile. La lisibilité est globalement bonne, à l’exception des CTA orange et du statut de confirmation mobile. L’interface est techniquement responsive ; elle doit encore devenir réellement mobile first sur l’ordre du contenu transactionnel.

Les trois corrections au meilleur rendement attendu sont :

1. rendre le CTA d’achat mobile immédiatement visible ;
2. déplacer l’activité locale après la première offre ;
3. corriger la confirmation mobile et le contraste des CTA.

Le remplacement des capsules informatives par des vignettes iconographiques constitue ensuite une amélioration transversale à forte valeur visuelle, à condition de préserver les libellés, l’accessibilité et l’auto-hébergement des ressources.
