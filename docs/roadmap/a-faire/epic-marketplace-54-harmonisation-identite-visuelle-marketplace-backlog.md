# Backlog EPIC-MARKETPLACE-54 - Harmonisation de l'identite visuelle de la Marketplace

> État de classement : **À faire** (dossier courant au 18 septembre 2026). Identifiant distinct : `EPIC-MARKETPLACE-54` (ancien numéro local 54). Implémentation locale livrée, revue et recette connectée encore attendues ; aucune clôture produit commune n’est documentée.

## Synthese

- Criticite : `Haute`.
- Statut : `Implemente en local - pret pour revue et recette connectee`.
- Objectif : faire ressentir la Marketplace comme une experience Localeo native, coherente avec `localeo.city`, sans degrader la recherche, la conversion ni les parcours metier existants.
- Orientation : `localeo.city` fournit l'univers de marque ; la Marketplace le traduit en une experience de decouverte et d'achat.
- Repartition cible : environ `70 % de continuite de marque / 30 % d'adaptation e-commerce`, a utiliser comme guide de conception et non comme mesure mathematique stricte.
- Reference visuelle : `https://localeo.city`.
- Environnement audite : `https://test-marketplace.localeo.city/accueil`.
- Date de l'audit : `31 aout 2026`.
- Dependances : Epic 42 `Localeo Live`, Epic 49 `Animations Marketplace`, Epic 52 `Accueil contextualise`, Epic 53 `Bornage et pagination`, backlog UX Marketplace et contenus valides des communes, coffrets et commercants.
- Hors perimetre : refonte du logo, changement de positionnement de marque, reproduction page a page de `localeo.city`, modification du tunnel de paiement, changement des regles d'eligibilite, refonte fonctionnelle de la recherche, modification des contenus de test issus de la base et creation d'un nouveau design system multi-produits.
- Contrainte d'hebergement : aucune ressource necessaire au rendu ne depend d'un service tiers a l'execution. Polices, images, icones et actifs de marque sont heberges et servis par Localeo.
- Exigence responsive : la validation multi-viewport est realisee pendant chaque lot de refonte, et non reportee a une recette finale.

## Probleme

La Marketplace reprend les couleurs principales et certains actifs Localeo, mais son ressenti reste plus proche d'une interface SaaS ou e-commerce generique que du site institutionnel. A l'inverse, une copie trop fidele du site institutionnel risquerait de donner au parcours l'apparence d'un site de presentation et d'affaiblir la recherche, la comparaison et l'achat.

Les ecarts structurants identifies sont :

- typographie `Nunito Sans` differente du couple `Oswald` et `DM Sans` utilise sur `localeo.city` ;
- emploi generalise de capsules, grands rayons et ombres diffuses, alors que la marque institutionnelle utilise des formes franches, des lignes et des aplats ;
- hero principalement fonctionnel et illustratif, face a une direction institutionnelle immersive et photographique ;
- succession de cartes de meme poids, avec peu de rythme editorial ;
- palette secondaire creme et peche trop presente par rapport au bleu profond, au blanc et a l'orange de marque ;
- manque de motifs recurrents de la marque : surtitres, numeros de section, filets orange, titres condenses et alternance de blocs contrastes ;
- heterogeneite des CTA, des icones et des niveaux de composants ;
- contenus de test et microcopies imparfaites qui diminuent la perception de qualite.

## Principes directeurs

1. `localeo.city` est la marque mere et la reference d'ambiance, pas un gabarit d'interface a recopier.
2. La cible suit un equilibre indicatif `70 % continuite de marque / 30 % adaptation e-commerce`.
3. La Marketplace reste transactionnelle : la marque renforce le parcours, elle ne masque pas les actions utiles.
4. La recherche territoriale reste l'action dominante du premier ecran.
5. Prix, disponibilite, contenu des offres et appels a l'action restent plus visibles que les elements decoratifs.
6. La photographie montre des personnes, des commerces et des gestes reels plutot que des visuels publicitaires generiques.
7. Les titres editoriaux utilisent une voix visuelle forte, tandis que les donnees et formulaires restent sobres et lisibles.
8. Les capsules sont reservees aux filtres, statuts et informations compactes.
9. Les grandes surfaces reposent sur des aplats, des lignes et une grille plutot que sur une accumulation de cartes flottantes.
10. Les composants critiques conservent leurs affordances, leurs etats et leur accessibilite.
11. Chaque composant et chaque page sont valides pendant leur refonte aux largeurs de reference, avant fusion et avant passage au lot suivant.
12. La conception suit une approche mobile-first pragmatique : la hierarchie, les contenus et les actions sont adaptes au viewport sans supprimer une information essentielle.

## Modele d'heritage de la marque

### A reprendre de `localeo.city`

- palette, typographies, formes et proportions caracteristiques ;
- traitement photographique, illustrations, pictogrammes et iconographie ;
- ton editorial local, humain, chaleureux et accessible ;
- principes d'espacement, de rythme, d'arrondis et de details graphiques distinctifs ;
- en-tete et pied de page clairement apparentes a l'ecosysteme Localeo ;
- sentiment de proximite, de confiance et d'ancrage territorial.

### A adapter pour la Marketplace

- recherche et choix de la ville immediatement accessibles ;
- produits, prix, disponibilite et CTA prioritaires dans la hierarchie visuelle ;
- cartes structurables, comparables et scannables ;
- parcours d'achat rapide, rassurant et sans distraction ;
- etats fonctionnels complets : chargement, erreur, absence de resultat, indisponibilite et confirmation ;
- lisibilite, accessibilite, performance et conversion prioritaires lorsqu'un choix institutionnel doit etre adapte.

### Regle de decision

Lorsqu'un arbitrage oppose fidelite visuelle et efficacite transactionnelle, conserver le code de marque qui cree la reconnaissance, puis adapter sa mise en oeuvre pour proteger la comprehension, l'accessibilite et la conversion. La Marketplace ne doit ressembler ni a un produit generique deconnecte de Localeo, ni a une simple page institutionnelle enrichie d'un bouton d'achat.

## Cible de marque

### Typographie

- titres de campagne et titres de sections majeures : `Oswald`, graisse 600, capitales selon le contexte ;
- texte courant, navigation, formulaires et composants fonctionnels : `DM Sans` ;
- texte manuscrit : reserve aux actifs de marque existants, sans ajout d'une police decorative dans l'interface ;
- aucune dependance fonctionnelle a `Nunito Sans` apres migration.

Les fichiers de polices sont auto-heberges par la Marketplace, idealement en `WOFF2`, avec les graisses et sous-ensembles strictement necessaires. Aucun appel a Google Fonts, Adobe Fonts ou a un CDN de polices tiers n'est autorise en production. Les licences de redistribution et d'auto-hebergement doivent etre verifiees et archivees avant integration.

### Palette principale

- bleu encre : `#082840` ;
- bleu Localeo : `#0B3D63` ;
- orange : `#F28A2E` ;
- blanc : `#FFFFFF` ;
- fond clair secondaire : teinte neutre tres legere, sans dominante peche excessive.

Les valeurs definitives doivent etre confirmees depuis les sources de style de `localeo.city`, puis centralisees sous forme de tokens semantiques.

### Geometrie

- CTA principaux : rectangulaires, rayon faible ou nul ;
- champs de recherche : rayon modere, sans apparence de capsule sur desktop ;
- cartes de contenu : rayon limite et ombre discrete ou absente ;
- filtres, statuts et choix de commune : capsules autorisees ;
- separateurs : lignes fines, alternance de fonds et reperes orange.

### Imagerie

- photographies documentaires de commerces et de situations locales reelles ;
- cadrages humains, lumiere naturelle et detail des savoir-faire ;
- voiles bleu Localeo lorsque du texte est superpose ;
- textes integres en HTML et non figes dans les images ;
- attributs alternatifs utiles et dimensions explicites pour limiter les decalages de mise en page.

### Hebergement des ressources

- polices servies depuis le domaine Localeo ou son infrastructure statique maitrisee ;
- images, pictogrammes, illustrations, logos et fichiers CSS necessaires au rendu servis par Localeo ;
- aucune ressource critique chargee depuis Google Fonts, Adobe Fonts, un CDN public ou un domaine tiers ;
- URLs d'actifs versionnees ou fingerprintees pour permettre un cache long et une invalidation fiable ;
- politique CSP compatible avec l'auto-hebergement, sans ajout de domaines tiers uniquement pour la refonte ;
- fonctionnement lisible avec les ressources de secours si un actif non critique ne charge pas ;
- inventaire de la source, de la licence et du proprietaire de chaque ressource integree.

## Lots d'implementation

| Lot | Priorite | Etat | Contenu | Sortie attendue |
|---|---|---|---|---|
| D0 | P0 | Fait | Inventaire des styles, composants, actifs et ecarts | Matrice de migration validee |
| D1 | P0 | Fait | Tokens de marque, fontes et primitives de base | Socle visuel centralise et documente |
| D2 | P0 | Fait | Hero et en-tete de l'accueil | Premier viewport immediatement identifiable Localeo |
| D3 | P1 | Fait | Boutons, champs, cartes, badges et icones | Geometrie coherente sur les parcours principaux |
| D4 | P1 | Fait | Rythme editorial des sections de l'accueil | Moins d'effet dashboard et plus de narration locale |
| D5 | P1 | Fait | Catalogue, detail coffret et fiche commercant | Continuite de marque jusqu'a la conversion |
| D6 | P1 | Fait | Direction photographique et gestion des actifs | Imagerie coherente, performante et accessible |
| D7 | P1 | Fait | Responsive, accessibilite et performance | Recette multi-viewport sans regression |
| D8 | P2 | Pret pour revue | Nettoyage, documentation et deploiement progressif | Migration maintenable et mesurable |

### Etat de l'implementation locale

- `DM Sans` et `Oswald` sont integrees en WOFF2 auto-heberges, sans appel a Google Fonts ni a un CDN de fontes ;
- le hero, l'en-tete, le pied de page, les sections editoriales et les primitives transactionnelles suivent la grammaire visuelle de `localeo.city` ;
- les pages ville, catalogue, detail coffret, commercant, commande et confirmation utilisent les memes fondations ;
- les largeurs 320, 360, 390, 430, 768, 1024 et 1440 px sont couvertes par les tests visuels de non-debordement ;
- les contenus provenant de la base n'ont pas ete modifies ; seules les microcopies statiques presentes dans les sources ont ete corrigees ;
- le build de production, le lint et les tests visuels representatifs passent en local ;
- le deploiement et la recette avec les donnees de l'environnement cible restent a effectuer apres revue.

## User Stories

### UI-540 - Inventorier l'interface actuelle

En tant qu'equipe produit, nous voulons connaitre les variantes visuelles reellement utilisees afin de migrer sans creer de nouveaux doublons.

#### Actions

- recenser fontes, tailles, couleurs, rayons, ombres, espacements et icones ;
- lister les variantes de boutons, champs, cartes, badges et liens ;
- identifier les styles globaux, styles locaux et valeurs codees en dur ;
- cartographier les composants partages par accueil, catalogue, detail, commercant, paiement et Localeo Live ;
- produire un tableau `conserver / adapter / remplacer / supprimer` ;
- qualifier chaque element selon sa contribution aux `70 % marque` ou aux `30 % e-commerce` ;
- capturer un etat de reference aux largeurs 320, 390, 768, 1024 et 1440 px.

#### Criteres d'acceptation

- chaque composant visible des parcours critiques appartient a une categorie de migration ;
- les variantes dupliquees et les valeurs codees en dur sont identifiees ;
- les pages de reference disposent de captures avant modification ;
- aucune modification fonctionnelle n'est incluse dans ce lot.

### UI-541 - Centraliser les tokens de marque

En tant que developpeur, je veux utiliser des tokens semantiques afin que l'identite Localeo reste coherente et ajustable.

#### Actions

- definir les tokens de couleurs, typographies, espacements, bordures, rayons, ombres et transitions ;
- distinguer les tokens de marque des tokens fonctionnels de succes, alerte, erreur et information ;
- integrer localement `Oswald` et `DM Sans` en `WOFF2`, avec strategies de repli ;
- verifier et archiver les licences autorisant leur redistribution et leur auto-hebergement ;
- limiter les fichiers aux graisses, styles et jeux de caracteres reellement utilises ;
- declarer les fontes avec `@font-face`, `font-display` adapte et chemins versionnes ;
- supprimer tout import ou preconnexion vers Google Fonts, Adobe Fonts ou un CDN tiers ;
- remplacer progressivement les valeurs codees en dur ;
- documenter les usages autorises de l'orange et des fonds bleu profond ;
- conserver des contrastes conformes sur tous les etats.

#### Criteres d'acceptation

- les primitives partagees n'utilisent plus de valeurs de marque dupliquees ;
- aucune requete de police n'est emise vers un domaine tiers ;
- les fichiers de police sont servis par l'infrastructure Localeo avec une politique de cache explicite ;
- les licences d'auto-hebergement sont documentees dans le depot ou dans le registre de licences du projet ;
- l'absence temporaire d'une fonte web ne provoque pas de saut de mise en page majeur ;
- les contrastes texte/fond respectent au minimum WCAG 2.2 AA ;
- les tokens sont nommes par intention et non uniquement par couleur brute.

### UI-542 - Recomposer le hero de l'accueil

En tant que visiteur, je veux reconnaitre immediatement l'univers Localeo tout en comprenant comment chercher une offre locale.

#### Actions

- conserver la recherche comme action principale ;
- introduire un surtitre editorial, un titre condense et un accent orange ;
- remplacer le visuel publicitaire par une photographie locale validee ;
- tester une composition immersive ou une grille asymetrique plus proche de `localeo.city` ;
- maintenir la promesse, l'aide de saisie et la reassurance dans le premier parcours de lecture ;
- prevoir un rendu de secours sans image.
- verifier que le hero exprime la marque sans prendre l'apparence d'une page institutionnelle non transactionnelle.

#### Criteres d'acceptation

- la proposition de valeur et le champ de recherche sont compris sans defilement a 1440 px ;
- le titre, la recherche et le CTA conservent une hierarchie claire entre 320 et 430 px ;
- la photographie ne nuit ni a la lisibilite ni aux performances ;
- aucune information essentielle n'est embarquee uniquement dans l'image ;
- le changement n'ajoute aucune etape au lancement d'une recherche.

### UI-543 - Harmoniser l'en-tete et la navigation

En tant que visiteur, je veux retrouver une navigation Localeo coherente et comprendre la fonction de chaque commande.

#### Actions

- aligner le traitement du logo avec la marque institutionnelle ;
- reduire l'effet capsule des commandes principales ;
- harmoniser recherche, localisation, contact, accueil et menu mobile ;
- normaliser la famille et l'epaisseur des icones ;
- ajouter des libelles accessibles aux boutons iconographiques ;
- conserver un focus visible et une zone tactile d'au moins 44 par 44 px.

#### Criteres d'acceptation

- toutes les commandes disposent d'un nom accessible ;
- la navigation reste utilisable au clavier et a 200 % de zoom ;
- aucun controle ne se chevauche entre 320 et 430 px ;
- la recherche reste accessible depuis les pages ou elle est necessaire.

### UI-544 - Rationaliser les composants

En tant qu'utilisateur, je veux distinguer facilement actions, filtres, contenus et statuts afin de parcourir la Marketplace sans ambiguite.

#### Actions

- definir une hierarchie `primaire / secondaire / tertiaire / lien` pour les actions ;
- limiter les boutons en capsule aux usages justifies ;
- reduire les grands rayons et les ombres decoratives ;
- normaliser les etats hover, focus, actif, charge, indisponible et erreur ;
- eviter les cartes imbriquees lorsque grille, ligne ou separateur suffisent ;
- harmoniser prix, metadonnees, badges, tags et informations de reassurance.
- rendre les cartes d'offres suffisamment structurees pour comparer rapidement prix, contenu, disponibilite et territoire.

#### Criteres d'acceptation

- une seule variante principale existe pour chaque famille fonctionnelle ;
- le CTA principal est identifiable sans dependre uniquement de la couleur ;
- les filtres et statuts restent distinguables des actions ;
- aucun changement ne degrade les formulaires, le paiement ou les etats asynchrones.

### UI-545 - Introduire un rythme editorial Localeo

En tant que visiteur, je veux decouvrir le territoire et ses commercants dans une page vivante plutot que dans une succession uniforme de cartes.

#### Actions

- introduire surtitres, numeros de section, filets orange et grands titres condenses ;
- alterner fonds blancs et surfaces bleu profond ;
- hierarchiser les sections `decouvrir`, `choisir`, `agir` et `suivre` ;
- transformer certaines listes de cartes en grilles editoriales ou lignes structurees ;
- conserver des points d'entree visibles vers communes, coffrets, animations et Localeo Live ;
- utiliser le module Localeo Live actuel comme reference de contraste et de presence de marque.

#### Criteres d'acceptation

- chaque section possede un role et un niveau de hierarchie identifiables ;
- les contenus prioritaires ne sont pas noyes dans des cartes de poids equivalent ;
- les blocs bleu profond ne creent pas de rupture de contraste ou de lecture ;
- l'ordre des contenus reste logique avec CSS desactive et pour les technologies d'assistance.

### UI-546 - Etendre la coherence aux pages transactionnelles

En tant qu'acheteur, je veux conserver le meme univers visuel de l'accueil au paiement afin d'avoir confiance dans le parcours.

#### Ecrans

- catalogue et resultats de recherche ;
- page commune ;
- detail coffret ;
- fiche commercant ;
- formulaire d'achat et confirmation ;
- etats vides, erreurs et chargements.

#### Actions

- appliquer les tokens et composants sans modifier la logique metier ;
- conserver prix, validite, contenu du coffret et CTA dans la zone de decision ;
- donner davantage de place aux photographies et aux preuves locales ;
- eviter que la decoration repousse l'achat ou masque les informations legales ;
- maintenir une experience d'achat rapide et sans distraction, notamment sur mobile ;
- harmoniser squelettes, erreurs et etats vides ;
- verifier la continuite avec Localeo Live sans effacer son identite fonctionnelle propre.

#### Criteres d'acceptation

- aucune regression du tunnel de recherche et d'achat ;
- les informations critiques restent visibles au meme moment ou plus tot ;
- les pages partagees ne melangent pas anciennes et nouvelles variantes ;
- tous les etats asynchrones ont un rendu coherent.

### UI-547 - Definir et produire les actifs photographiques

En tant qu'equipe de marque, nous voulons une bibliotheque d'images coherente afin que chaque territoire reste authentique sans fragmenter l'identite.

#### Actions

- rediger un brief de prise de vue et de selection ;
- definir cadrages, sujets, luminosite, traitement colorimetrique et usages ;
- obtenir les droits d'utilisation et consentements necessaires ;
- produire les formats desktop, tablette et mobile ;
- generer les variantes WebP ou AVIF et les images de repli ;
- heberger les originaux publies et leurs variantes optimisees sur l'infrastructure Localeo ;
- utiliser des noms versionnes ou fingerprintes et une politique de cache adaptee ;
- supprimer les dependances a des banques d'images ou CDN tiers au moment du rendu ;
- documenter recadrage, point focal et texte alternatif.

#### Criteres d'acceptation

- aucun actif provisoire ou texte de demonstration n'est publie ;
- les droits et la source de chaque image sont tracables ;
- les images responsives ne chargent pas un original surdimensionne ;
- aucune image, icone ou illustration necessaire a la page n'est servie par un domaine tiers ;
- les ressources publiees sont versionnees et disposent d'en-tetes de cache adaptes ;
- le contenu principal reste comprehensible si les images ne chargent pas.

### UI-548 - Assurer responsive, accessibilite et performance

En tant qu'utilisateur, je veux une experience robuste quels que soient mon appareil et mes besoins d'acces.

Cette User Story est transversale : ses controles sont executes pendant `D1` a `D6`. Le lot `D7` consolide la recette globale, mais ne doit pas devenir le premier moment ou les problemes responsive sont recherches.

#### Matrice minimale

- largeurs : 320, 360, 390, 430, 768, 1024 et 1440 px ;
- navigateurs : Chrome, Firefox et Safari mobile ;
- zoom : 200 % ;
- interactions : souris, tactile et clavier ;
- preferences : reduction des animations et contraste renforce lorsqu'il est supporte.

#### Methode de validation continue

- definir le comportement responsive attendu avant l'implementation de chaque composant ;
- verifier chaque composant isole puis dans le contexte reel de la page ;
- controler au minimum 320, 390, 768, 1024 et 1440 px dans chaque lot ;
- executer la matrice complete 320, 360, 390, 430, 768, 1024 et 1440 px avant validation de chaque page ;
- tester les contenus courts, longs, absents et issus de donnees variables afin de detecter debordements et ruptures de grille ;
- joindre des captures desktop et mobile a la recette de chaque lot significatif ;
- bloquer la fusion lorsqu'une regression responsive critique est identifiee.

#### Criteres d'acceptation

- aucun defilement horizontal involontaire ;
- ordre de focus logique et focus toujours visible ;
- contrastes WCAG 2.2 AA pour textes, controles et etats ;
- zones tactiles suffisantes ;
- animations non essentielles desactivees avec `prefers-reduced-motion` ;
- pas de regression notable des Core Web Vitals sur les pages migrees ;
- absence de decalage majeur lie aux fontes et aux images du hero.
- aucun lot de refonte n'est considere termine sans validation responsive de ses composants et pages.

### UI-549 - Nettoyer les contenus et finaliser la migration

En tant que visiteur, je veux une interface sans contenu provisoire ni incoherence afin de percevoir la Marketplace comme un produit abouti.

#### Actions

- corriger uniquement les fautes et incoherences des textes statiques presents dans les sources ;
- ne pas modifier dans cette Epic les contenus de test provenant de la base, notamment les noms, descriptions et libelles metier ;
- normaliser dates relatives, capitales, ponctuation et libelles d'action ;
- supprimer les anciennes classes et variantes devenues inutiles ;
- documenter les composants et regles d'usage ;
- recapturer les pages de reference apres migration.

#### Criteres d'acceptation

- les textes statiques visibles ont fait l'objet d'une revue produit ;
- aucune correction editoriale de donnees issues de la base n'est incluse dans ce lot ;
- les anciennes variantes non utilisees sont supprimees ;
- les captures avant/apres et la checklist de recette sont archivees.

## Plan d'action detaille

### Phase 0 - Cadrage et baseline

1. valider le perimetre des pages et composants ;
2. produire l'inventaire `UI-540` ;
3. confirmer les couleurs et fontes depuis les sources officielles ;
4. verifier les licences et definir l'emplacement d'hebergement Localeo de chaque famille d'actifs ;
5. capturer les references visuelles et les mesures de performance ;
6. valider deux directions de hero avant implementation ;
7. choisir les actifs photographiques et confirmer leurs droits.
8. documenter pour chaque direction ce qui releve de la continuite de marque et ce qui releve de l'adaptation e-commerce.

Sortie : inventaire, baseline, direction validee et liste des composants a migrer.

### Phase 1 - Fondations

1. ajouter les tokens sans modifier le rendu ;
2. integrer localement `Oswald` et `DM Sans` avec fallback, sans appel tiers ;
3. migrer boutons, liens, champs, badges et cartes dans un environnement isole ;
4. ajouter les tests des variantes et etats ;
5. documenter les regles de geometrie et de contraste.
6. valider les primitives aux largeurs 320, 390, 768, 1024 et 1440 px avant leur generalisation.

Sortie : primitives stables, testees et reutilisables.

### Phase 2 - Accueil pilote

1. migrer l'en-tete et la navigation ;
2. recomposer le hero sans changer le contrat de recherche ;
3. appliquer le rythme editorial aux sections ;
4. rationaliser les cartes et listes ;
5. integrer les actifs photographiques optimises ;
6. recetter desktop, mobile, clavier et chargements lents.
7. corriger les ruptures responsive avant d'engager la migration des pages transactionnelles.

Sortie : accueil pilote representatif de la cible de marque.

### Phase 3 - Parcours transactionnel

1. migrer catalogue, page commune et fiches de resultat ;
2. migrer detail coffret et fiche commercant ;
3. migrer formulaire, paiement, confirmation et reassurance ;
4. harmoniser erreurs, vides et squelettes ;
5. verifier les transitions avec Localeo Live ;
6. executer les tests de non-regression fonctionnelle.
7. valider chaque page sur la matrice responsive complete avant de passer a la suivante.

Sortie : parcours complet sans rupture d'identite ni perte de conversion.

### Phase 4 - Stabilisation et deploiement

1. supprimer les styles et composants obsoletes ;
2. finaliser la revue des contenus ;
3. executer la matrice responsive et accessibilite ;
4. comparer performance et indicateurs de conversion a la baseline ;
5. deployer progressivement avec possibilite de retour arriere ;
6. surveiller erreurs, recherche, consultation et achat apres mise en ligne.

Sortie : migration documentee, mesuree et exploitable en production.

## Strategie de decoupage technique

- un commit pour les tokens et fontes ;
- un commit par famille de primitives ;
- un commit pour l'en-tete ;
- un commit pour le hero ;
- un commit par section ou page fonctionnelle ;
- un commit separe pour le nettoyage des styles obsoletes ;
- aucune modification fonctionnelle opportuniste dans les commits visuels ;
- captures et resultat de recette joints a chaque lot significatif.
- aucune fusion d'un lot visuel sans preuves de validation desktop et mobile.

## Indicateurs de succes

### Qualite de marque

- validation interne que l'accueil appartient clairement au meme univers que `localeo.city` ;
- validation que la Marketplace reste identifiable comme une interface d'achat et non comme une copie du site institutionnel ;
- revue explicite de l'equilibre indicatif `70 % marque / 30 % e-commerce` sur l'accueil et les pages transactionnelles ;
- disparition des variantes typographiques et geometriques non documentees ;
- reduction du nombre de valeurs de couleur, rayon et ombre codees en dur.

### Experience

- maintien ou amelioration du taux de lancement d'une recherche ;
- maintien ou amelioration du taux de consultation d'un coffret ;
- maintien ou amelioration du passage du detail au formulaire ;
- absence d'augmentation des abandons sur mobile.

### Technique

- aucun echec des tests de parcours critiques ;
- aucune regression d'accessibilite bloquante ;
- pas de degradation notable du LCP, CLS ou INP liee a la refonte ;
- absence d'erreur console introduite sur les pages migrees.

## Risques et mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| Esthetique institutionnelle trop dominante | Recherche moins visible | Prototyper le hero avec la recherche comme action primaire |
| Copie trop fidele de `localeo.city` | Apparence de site de presentation et baisse de conversion | Adapter hierarchie, cartes, CTA et densite aux usages transactionnels |
| Adaptation e-commerce trop generique | Rupture de marque et perte de confiance | Imposer les tokens, la direction photographique, le ton et les reperes Localeo |
| Oswald utilisee sur trop de contenu | Lisibilite degradee | Limiter Oswald aux titres courts et editoriaux |
| Photographies lourdes | LCP degrade | Formats responsives, preload cible et budget de poids |
| Dependances a des ressources tierces | Indisponibilite, confidentialite et rendu non maitrise | Auto-heberger toutes les ressources necessaires et controler les requetes reseau |
| Licence de police incompatible | Blocage juridique | Verifier la redistribution avant integration et choisir une alternative auto-hebergeable si necessaire |
| Migration globale trop risquee | Regressions visuelles | Deploiement par page et composants partages versionnes |
| Responsive traite uniquement en fin de projet | Corrections tardives, couteuses et incoherentes | Validation multi-viewport obligatoire dans chaque lot et blocage des regressions critiques avant fusion |
| Suppression excessive des cartes | Affordances moins claires | Conserver les conteneurs lorsqu'ils portent une action ou un etat |
| Orange trop present | Fatigue visuelle et contraste | Reserver l'orange aux accents et CTA prioritaires |
| Rupture avec Localeo Live | Ecosysteme fragmente | Conserver ses codes propres et harmoniser uniquement les primitives communes |
| Contenus ou images non valides | Retard de livraison | Valider le corpus photographique pendant la phase 0 |

## Criteres d'acceptation globaux

- la Marketplace utilise `Oswald` pour les titres editoriaux et `DM Sans` pour l'interface ;
- toutes les polices sont auto-hebergees par Localeo et aucune requete n'est envoyee a Google Fonts, Adobe Fonts ou un CDN tiers ;
- toutes les images, icones, illustrations et ressources critiques du rendu sont servies par l'infrastructure Localeo ;
- les couleurs de marque sont centralisees et appliquees semantiquement ;
- les CTA principaux ne reposent plus sur une capsule generique ;
- le hero combine promesse Localeo, photographie humaine et recherche visible ;
- l'interface reprend l'univers de `localeo.city` sans reproduire son organisation page a page ;
- la hierarchie transactionnelle rend recherche, prix, disponibilite et CTA immediatement identifiables ;
- les sections utilisent un rythme editorial identifiable ;
- les pages de recherche, coffret, commercant et paiement restent fonctionnellement inchangees ;
- les microcopies statiques connues comme incorrectes sont corrigees sans modifier les contenus issus de la base ;
- la recette couvre la matrice responsive, clavier, zoom et contrastes ;
- chaque lot fournit ses preuves de validation responsive avant integration ;
- la performance et les conversions ne regressent pas de maniere significative ;
- la documentation des tokens et composants est a jour.

## Definition of Done

- [ ] Inventaire visuel et captures de baseline valides.
- [ ] Direction du hero et brief photographique approuves.
- [ ] Equilibre `70 % continuite de marque / 30 % adaptation e-commerce` valide sur les ecrans pilotes.
- [ ] Tokens, fontes et primitives documentes.
- [ ] Licences des polices et actifs verifiees et archivees.
- [ ] Polices, images, icones et illustrations auto-hebergees par Localeo.
- [ ] Audit reseau confirmant l'absence de ressources critiques chargees depuis un domaine tiers.
- [ ] Accueil migre et recette.
- [ ] Catalogue, page commune, coffret et commercant migres.
- [ ] Paiement, confirmation, erreurs et etats vides harmonises.
- [ ] Fautes des textes statiques visibles corrigees, sans modification des contenus provenant de la base.
- [ ] Recette aux largeurs 320, 360, 390, 430, 768, 1024 et 1440 px.
- [ ] Captures desktop et mobile jointes a chaque lot de refonte significatif.
- [ ] Aucune page n'a attendu le lot final pour sa premiere validation responsive.
- [ ] Recette clavier, zoom 200 % et lecteur d'ecran realisee.
- [ ] Budget de performance respecte.
- [ ] Tests de recherche et d'achat valides.
- [ ] Captures avant/apres archivees.
- [ ] Deploiement progressif et plan de retour arriere valides.

## Ordre recommande

1. `UI-540` - inventaire et baseline ;
2. `UI-541` - tokens et typographies ;
3. `UI-542` et `UI-543` - hero, en-tete et navigation ;
4. `UI-544` - primitives et composants ;
5. `UI-545` et `UI-547` - rythme editorial et photographie ;
6. `UI-546` - extension aux pages transactionnelles ;
7. `UI-548` - recette responsive, accessibilite et performance ;
8. `UI-549` - nettoyage, documentation et stabilisation.

## Elements a conserver

- recherche territoriale dominante ;
- comprehension immediate de l'offre de coffrets ;
- achat invite sans creation de compte ;
- informations de reassurance pres des actions critiques ;
- palette bleu, orange et blanc ;
- codes typographiques, photographiques et editoriaux de `localeo.city` ;
- ergonomie transactionnelle propre a la Marketplace ;
- acces aux communes, animations et Localeo Live ;
- dimension locale, humaine et chaleureuse des contenus ;
- distinction fonctionnelle de Localeo Live ;
- logique metier, contrats API et instrumentation existante.
