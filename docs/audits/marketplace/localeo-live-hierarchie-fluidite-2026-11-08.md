# Localeo Live — audit UX/UI après déploiement

Date : **8 novembre 2026**. Objet : relief des sections, plaisir de découverte,
chargement et visibilité des commerçants. Suite au retour utilisateur après la
livraison de l’évolution E73 consacrée à l’adhésion habitant.

Suite demandée le 8 novembre : les recommandations R01–R08 sont reprises dans
la [spécification E73-EVO-LIVE-HIERARCHIE](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-8-novembre-2026--hiérarchie-et-fluidité-e73-evo-live-hierarchie)
et sa conception. Cette traçabilité ne transforme pas les constats de cet audit
en corrections réalisées.

## Diagnostic

**Le parcours public fonctionne, mais sa composition reste trop uniforme et son
chargement trop présent.** L’accueil juxtapose un titre, un résumé communal, un
sélecteur, des titres de périodes et des cartes empilant plusieurs sous-blocs.
La hiérarchie ne permet pas de distinguer immédiatement le contexte, l’occasion
de jouer et les outils secondaires. Les commerçants restent visuellement en
marge de cette expérience.

Le prochain travail devrait porter sur une composition cohérente de l’accueil
et de la découverte. Le plaisir attendu vient d’une animation attirante, d’une
promesse concrète et d’une interaction fluide. Les effets décoratifs doivent
accompagner ces trois éléments.

## Méthode et limites

- Observation directe dans Chrome de [TEST — accueil](https://test-animations.localeo.city/live/decouvrir),
  de [l’annuaire](https://test-animations.localeo.city/live/commercants) et de la
  fiche publique L’Escale Douce. Lecture des arbres d’accessibilité et des rendus.
- Accueil et défilement inspectés en émulation **390 × 844**, sans ralentissement
  réseau ; aperçu affiché à 75 %. Inspection bureau dans une fenêtre d’environ
  1 020 × 951 pixels avec zoom navigateur préexistant à 90 %. Ce ne sont pas des
  essais sur téléphone physique ni des mesures de pixels CSS sur ordinateur.
- Sélection existante : deux communes, cinq animations en cours, aucune à venir
  dans l’aperçu. Cartes avec et sans visuel observées ; la section Prochainement
  a été inspectée dans son état vide seulement. Aucun suivi personnel n’était
  mis en avant dans cet accueil.
- Revue indépendante du code, puis confrontation avec le rendu. Version locale
  Marketplace/Live : `498b9392650b6c55bfef3a65d4de9d0196cd08ee`, arbre propre.
  Le SHA réellement servi par TEST n’a pas été attesté : la comparaison du code
  n’est pas une preuve d’identité exacte avec le bundle déployé.
- Aucun enregistrement, inscription, consentement, commune suivie ou contenu
  métier modifié. Pas de mesure chronométrée des requêtes, de CLS, de contraste,
  de rétention ou de compréhension par des habitants. Les bénéfices attendus
  ci-dessous restent des hypothèses produit à vérifier.
- Audit uniquement : aucune correction applicative ni migration. L’audit
  [du 7 novembre](localeo-live-adhesion-ux-ui-2026-11-07.md) et les
  [preuves E73](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md)
  restent des documents datés distincts. Les statuts de roadmap ne changent pas.

## Constats et recommandations prioritaires

### R01 — P1 : rendre les périodes immédiatement reconnaissables

**Observé.** « En ce moment » est un titre simple entre le choix communal et les
cartes. « Prochainement » reprend le même traitement après une longue liste.
Le résumé du haut emploie « À venir », alors que la section porte un autre nom.
La rupture visuelle entre les deux périodes est faible.

**Proposition.** Employer partout « En ce moment » et « Prochainement ». Donner à
chaque période un véritable en-tête : pictogramme, titre, accent graphique et
espacement. Utiliser un accent chaud Localeo pour le présent et un traitement
calendrier plus calme pour le futur, sans dépendre uniquement de la couleur.
Conserver une typographie mesurée. Les repères du haut doivent rejoindre
directement la bonne section ; leurs nombres restent ceux des résultats chargés,
avec une mention de portée si nécessaire, jamais un total inventé.

**Preuve code.** Les deux périodes partagent le même markup et la même classe
dans `LiveDiscovery.jsx:268` ; `live-discovery.css:8` apporte surtout un espacement
et un titre standard. `LiveCommunityScene.jsx` utilise « À venir » dans le raccourci.

### R02 — P1 : faire du chargement un état discret et stable

**Observé.** Au retour dans la fenêtre, « Actualisation de vos suivis… » apparaît
avant le programme. En revenant depuis les commerçants, l’arbre d’accessibilité
expose simultanément ce message, « Recherche des animations… » et une phrase
sur le chargement du programme. À l’ouverture de l’annuaire, les résultats sont
remplacés par un texte de recherche dans une grande zone vide.

**Cause locale.** `LiveHome.jsx:25–48` couple le rafraîchissement personnel et
celui du catalogue. Un retour au premier plan après 60 secondes peut le lancer.
`useLiveDashboard.js:38` réinitialise les éléments ; `LiveDiscovery.jsx:181–187`
recrée des emplacements vides. Le titre de `LiveCommunityScene.jsx:23` varie
selon le chargement. Plusieurs messages peuvent donc se superposer.

**Proposition.** Distinguer trois situations :

1. Première ouverture sans contenu : ossature compacte aux dimensions prévues,
   titre stable et une seule annonce de chargement par zone indépendante.
2. Actualisation du même contexte : conserver le dernier contenu lisible,
   indiquer discrètement la revalidation et remplacer les résultats sans tout
   retirer. Garder la fraîcheur, les erreurs et l’accès à Réessayer explicites.
3. Changement de commune ou de filtre : ne pas afficher les anciens résultats
   comme s’ils répondaient au nouveau choix ; conserver seulement la structure.

La dernière lecture d’un catalogue ne constitue jamais une autorisation de
participation. Ne pas mettre les API privées en cache PWA, ni assouplir les
contrôles serveur pour donner une impression de vitesse.

La réserve technique **LA-16** reste ouverte dans les preuves E73. Cet audit ne
permet pas d’attribuer le chargement observé à Render, à la base ou au réseau.
Les changements inattendus de mise en page doivent être mesurés séparément des
temps API ([référence web.dev](https://web.dev/articles/optimize-cls)).

### R03 — P1 : donner une place structurelle aux commerçants

**Observé.** Sur l’accueil, « Commerçants » est un petit bouton voisin du
rafraîchissement. Dans l’annuaire, « Animations / Commerçants » devient une large
navigation à deux choix. La même destination change donc de poids et de forme
selon la page. Aucun aperçu de commerces n’apparaît dans le programme observé.

**Proposition.** Réutiliser une navigation **Animations | Commerçants**, au même
emplacement et avec la même apparence sur ces deux vues. La placer dans la zone
de découverte, après le contexte communal compact. Sur l’accueil, remplacer le
petit raccourci actuel et réduire le résumé existant pour ne pas ajouter une
nouvelle hauteur d’en-tête. Conserver les quatre entrées de navigation basse.

Donner une promesse explicite à la vue commerçants : « Les adresses de vos
animations », puis accès directs aux horaires, aux animations et à l’itinéraire.
Un aperçu de deux ou trois commerces dans l’accueil peut être exploré ensuite,
avec seulement des données publiques autorisées et un coût réseau borné ; il
n’est pas nécessaire à la première correction. Ne jamais divulguer les étapes
secrètes d’une chasse au trésor.

**Preuve code.** `LiveHome.jsx:37`, `live-explore-nav.css:5` et `LiveApp.jsx:145`.

### R04 — P1 : recomposer les cartes autour de l’envie de participer

**Observé.** Une carte sans flyer empile badge, commune, titre, grand bouton
sombre, favoris/partage, encart défi, nombre de lots et dates. Le bouton arrive
avant l’explication de ce que l’habitant va faire. Les premières cartes sont
hautes et ressemblent à des fiches ; le programme se parcourt lentement.

**Proposition.** Ordre de lecture : titre et commune → défi concret et période →
un indicateur utile → action principale. Favori et partage restent secondaires,
identifiables et accessibles. Réunir les métadonnées courtes au lieu de créer un
sous-bloc pour chacune. Remplacer « validations à réaliser » par une formulation
habitante adaptée au moteur, par exemple « Faites valider votre passage chez
2 commerçants » lorsque cette règle est effectivement celle de l’animation.

Conserver « Découvrir l’animation » pour ouvrir une fiche : « Jouer » ou
« Participer » ne doivent pas promettre une action immédiate si le clic ouvre
seulement le détail. Ne pas augmenter globalement la taille des textes.

**Preuve code.** Ordre des éléments dans `LiveDiscovery.jsx:72–78`.

### R05 — P2 : construire une identité visuelle même sans photo

**Observé.** Les premières cartes, sans visuel, reposent sur des rectangles
blancs et vert pâle. Plus bas, le flyer chocolat de Test passeport TCA crée une
rupture d’attractivité. La qualité perçue dépend donc fortement des contenus.

**Proposition.** Définir deux variantes assumées : carte avec flyer officiel et
carte sans image, compacte, avec un pictogramme de jeu, une composition
typographique et un accent graphique. Ne pas ajouter une photographie par
défaut, une illustration prétendument liée au commerce ou un grand emplacement
vide. Stabiliser la place du vrai flyer lorsqu’il existe, y compris pendant son
chargement ou en cas d’échec.

L’effet distinctif peut venir d’un motif discret de parcours, d’une forme de
ticket ou d’une icône de défi cohérente avec la charte. Une seule convention
graphique suffit ; les variantes par moteur ne doivent pas produire une palette
et des composants différents pour chaque animation.

### R06 — P2 : harmoniser découverte et annuaire

**Observé.** La page commerçants se resserre nettement sur ordinateur. Recherche,
commune, lien de choix des communes puis résultats se succèdent. La liste montre
des adresses longues, alors que l’utilité immédiate est « où aller et pour quelle
animation ». La fiche L’Escale Douce rend bien accessibles horaires, itinéraire
et trois animations, mais sa présentation reste essentiellement textuelle.

**Proposition.** Partager le même cadre de page, le contexte communal et les
principes de navigation. Composer chaque résultat autour du nom, du repère
communal et des deux actions « Horaires et animations » / « Y aller ». Utiliser
les vraies photos lorsqu’elles existent ; garder une icône sobre sinon. Réserver
l’adresse complète au détail si elle surcharge la liste, sans la tronquer dans
le lien d’itinéraire. Ne pas afficher « ouvert maintenant » sans horaires
structurés et fiables permettant ce calcul.

**Qualité de données à distinguer.** Le premier commerce de TEST affiche trois
fois la même ligne d’adresse, et son adresse postale diffère de sa commune de
rattachement affichée. Ces faits nuisent au rendu. Leur cause n’est pas établie
par cet audit : contrôler source et assemblage avant une correction. Les noms
« TEST… » affectent aussi l’effet de démonstration ; ne pas les renommer
automatiquement au titre d’une retouche UX.

### R07 — P2 : alléger les états sans activité

**Observé.** Après les cinq animations, l’état vide Prochainement est suivi de
l’aide de récupération, de la date d’actualisation des participations et d’un
nouveau lien vers celles-ci. Le bas de page revient à des informations de gestion.

**Proposition.** Conserver un état futur compact et accueillant, avec un seul
lien utile vers les communes. Garder l’aide de récupération disponible dans une
zone secondaire. Dans ce contexte sans action personnelle, reléguer l’horodatage
à une information de fraîcheur discrète. Ne pas suggérer d’activer des alertes
qui n’existent pas et ne pas masquer une erreur sous un faux état vide.

### R08 — P2 : ajouter une sensation de réponse, après stabilisation

Prévoir un retour tactile visuel immédiat sur les commandes, des transitions
courtes lors d’un changement de vue et une mise à jour locale des résultats.
Conserver position de lecture et focus au retour d’une fiche. Une réussite
personnelle confirmée peut être mise en valeur ; une ouverture de page ou un
rafraîchissement ne doit pas déclencher une célébration.

Ne pas ajouter de carrousel automatique, de compte à rebours artificiel ou de
pulsation permanente. Les mouvements non essentiels respectent les préférences
de réduction d’animation
([recommandation W3C, critère 2.3.3 de niveau AAA](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)).

## Composition cible proposée

| Ordre | Zone | Intention |
| --- | --- | --- |
| 1 | Header Live compact : identité, recherche, messages | Se repérer sans consommer le premier écran. |
| 2 | Contexte communal : noms suivis et commande Modifier | Comprendre immédiatement quel territoire est présenté. |
| 3 | Une action personnelle lorsqu’elle existe | Reprendre son parcours ou consulter son gain confirmé. |
| 4 | Navigation stable Animations / Commerçants | Rendre les deux possibilités visibles au même endroit. |
| 5 | En ce moment : en-tête marqué puis cartes courtes | Donner envie et aider à choisir rapidement. |
| 6 | Prochainement : rupture claire, traitement calendrier | Préparer la prochaine sortie sans concurrencer le présent. |
| 7 | Aide et informations secondaires | Rester disponibles sans diriger le parcours public. |

Le résumé « Ça se passe dans vos communes » est absorbé dans le contexte et
l’en-tête de période. Les raccourcis de période restent compacts. Il n’est pas
nécessaire d’ajouter un grand bandeau promotionnel avant les animations.

## Ordre de réalisation et critères de vérification

1. **Fluidité : R02.** Séparer première ouverture, revalidation et nouveau
   contexte ; éliminer les messages concurrents. Vérifier retour après 60 s,
   rafraîchissement manuel, erreur partielle, réseau lent et changement de filtre.
2. **Composition : R01, R03, R04.** Traiter ensemble sections, navigation et
   cartes. À 390 × 844, sans action personnelle, viser une première proposition
   et son CTA visibles dans le premier écran. Avec une action personnelle, cette
   action garde la priorité. Les commerçants doivent être repérables sans ouvrir
   un menu ni devoir connaître leur emplacement.
3. **Finition : R05 à R08.** Valider avec/sans flyer, une et plusieurs communes,
   zéro résultat, plusieurs animations à venir, annuaire et fiche commerçant.

Recette à prévoir sur 320, 390, 768 et 1 280 pixels, zoom 200 %, clavier,
mouvement réduit et téléphone réel. Vérifier que le bouton visé ne change pas
de place sous le doigt pendant une actualisation ; préserver focus et lecture.
Mesurer le CLS sur le parcours complet, puis les temps API indépendamment.
Un court essai habitant peut compléter ces preuves : identifier une animation
ouverte, une animation future et l’accès aux commerçants sans explication.
Cet essai complète l’évaluation ergonomique ; il n’introduit pas un nouveau
prérequis externe de clôture de l’epic.

La hiérarchie, la cohérence et les mots employés s’appuient sur les principes
de [visibilité, cohérence et langage utilisateur de NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/).
Les choix graphiques précis ci-dessus sont des propositions pour Localeo,
pas des prescriptions universelles issues de ces références.

## Impacts et résultat de cet audit

- **Application concernée :** Localeo Live, dépôt Marketplace. Les travaux
  proposés se concentrent sur les composants et hooks existants ; retirer les
  styles devenus inutiles plutôt qu’empiler des surcharges.
- **Domaine, contrats et SQL :** aucun changement nécessaire identifié pour la
  hiérarchie et la gestion des états. Un nouvel aperçu de commerces demanderait
  une vérification du contrat public et de son coût avant réalisation.
- **Documentation et tests :** préciser la composition E73 lors d’une demande
  d’implémentation ; adapter les tests de rendu aux objectifs de lecture, tout en
  conservant fraîcheur, isolation des contextes et refus métier.
- **Démonstration :** prévoir des jeux avec/sans flyer et des périodes variées ;
  la correction des données TEST est un sujet distinct, non exécuté ici.
- **Contrôles exécutés ici :** parcours public décrit ci-dessus et revue de
  sources. Aucun test fonctionnel automatisé ni benchmark rejoué. L’audit
  n’atteste pas la clôture LA-16, la compatibilité de tous les appareils ou une
  amélioration mesurée de l’adhésion.
