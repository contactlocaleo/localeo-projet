# Localeo Live — audit mobile du carnet de bord et des lots

Date : **9 novembre 2026**. Environnement : [Localeo Live TEST](https://test-animations.localeo.city/).
Retour utilisateur : parcours moins lisible après la refonte, lots difficiles à
retrouver, besoin d'une application quotidienne organisée autour d'un **carnet
de bord digital**, avec davantage de repères visuels et moins d'explications.

**Suivi de traitement du 9 novembre 2026 :** les neuf retours font l’objet de
l’évolution [E73-EVO-LIVE-CARNET-BORD](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-9-novembre-2026--carnet-de-bord-e73-evo-live-carnet-bord),
avec [réalisation, preuves et limites](../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md).
Le constat ci-dessous décrit la version auditée ; il reste distinct de la
recette locale et d’une future vérification de la version déployée.

**La priorité est de rétablir les repères personnels et la prochaine action.**
La navigation donne une place permanente aux communes, alors que les lots
deviennent un filtre conditionnel. Dans l'état vide observé, le carnet n'affiche
que « Tout » et une invitation à découvrir des animations. L'habitant qui
revient chercher un gain ne trouve aucun repère « Mes lots ».

La palette bleu profond, turquoise et orange, les boutons identifiables et la
navigation basse constituent une base à conserver. L'esprit carnet doit surtout
venir des objets personnels, des tampons et des actions utiles, soutenus par une
composition plus expressive.

## Périmètre observé

Inspection directe dans Chrome, par captures et lecture des éléments accessibles.
Émulation **360 × 800** (Samsung Galaxy A55, aperçu à 75 %), puis **390 × 844** et
**320 × 568** en mode responsive. Aucun ralentissement réseau configuré.

| Écran | Observation effective |
| --- | --- |
| Découvrir | Commune Latresne, animation « À vélo chez nos voisins », section Prochainement vide ; contrôlé à 360, 390 et 320 pixels de largeur. |
| Mon carnet | État vide, seul filtre Tout, découverte et récupération ; contrôlé à 360 et 320 pixels. |
| Retrouver mon carnet | Formulaire e-mail et aide dépliée, à 360 pixels ; aucun envoi. |
| Mes communes | Commune suivie, recherche et géolocalisation proposée ; aucun changement. |
| Fiche d'animation | Défi, conditions essentielles, raccourci Les lots, deux coffrets à gagner et commerces partenaires, à 360 pixels. |
| Inscription classique | Haut et bas du formulaire, quatre champs, consentements et bouton final ; aucune saisie ni inscription. |
| Ancien écran Mes lots | Route directe `/live/lots`, zéro lot et zéro tirage pour ce navigateur, aide de récupération ; contrôlé à 360 et 390 pixels. |
| Ancienne liste Mes participations | Route `/live/animations`, état vide confirmé à 390 pixels. |
| Commerçants | Entrée depuis Découvrir, filtres, premières adresses et défilement à 390 pixels ; aperçu à 320 pixels. |

Le navigateur ne contient aucune participation personnelle visible. Il n'a donc
pas permis d'observer un passeport commencé, un coffret détenu ou un lot gagné.
**Cet audit ne démontre aucune suppression de lots.** Les deux notifications
affichées ne constituent pas une preuve de gains. La récupération par e-mail,
la remise d'un lot et l'utilisation d'un accès restent hors de la recette
effectuée.

Une revue indépendante du code Marketplace au commit local `4cdf8bf` complète
l'observation. Le SHA servi par TEST n'a pas été attesté. Les constats de code
ci-dessous sont séparés des comportements reproduits dans le navigateur.
Il ne s'agit ni d'essais sur téléphone physique, ni d'une mesure d'accessibilité
ou de performance complète.

## Constats prioritaires

### CB01 — P1 — Les lots ont perdu leur point d'entrée

**Observé.** La barre affiche Mon carnet / Découvrir / Communes. Dans le carnet
vide, aucune rubrique Lots n'est visible. Pourtant, l'écran
[Mes lots](https://test-animations.localeo.city/live/lots) est toujours disponible
en saisissant son adresse et conserve un titre et des pictogrammes explicites.

**Explication dans le code.** La navigation a changé dans `LiveApp.jsx:189` et
le filtre Lots peut être masqué par `LiveUnifiedCarnet.jsx:139`. Ce masquage suit
la décision CN-03 actuelle ; le modifier demandera une évolution explicite de
la spécification, pas une réinterprétation silencieuse.

**Correction proposée.** Rétablir **Mes lots** comme destination permanente,
avec pictogramme cadeau et libellé. Garder cette destination même si aucun lot
n'est chargé. Un compteur éventuel doit représenter des données confirmées,
sans annoncer zéro pendant une erreur ou un chargement incomplet.

### CB02 — P1 — Le carnet vide répond mal à un habitant déjà inscrit

**Observé.** « Votre carnet commence ici » et « Les accès ajoutés dans ce
navigateur apparaîtront ici » conduisent principalement à Découvrir. Le filtre
Tout occupe une ligne entière sans offrir de choix. Retrouver mon carnet est un
lien secondaire. L'écran explique le stockage, mais montre peu ce que le carnet
permet de conserver.

**Correction proposée.** Un aperçu simple avec trois pictogrammes légendés
**Parcours / Coffrets / Lots**, puis deux intentions clairement distinguées :
**Je découvre les animations** et **Je retrouve mes participations et lots**.
Un texte court suffit : « Déjà participé ? Retrouvez votre carnet par e-mail. »
Les précisions sur ce navigateur et la sauvegarde restent dans une aide.
Retirer le filtre Tout lorsqu'il est seul, tout en conservant les destinations.

### CB03 — P1 — Une différence technique peut empêcher des lots de remonter

**Revue de code, cause personnelle non établie.** Le nouveau carnet interrompt
la lecture des suivis si la bibliothèque locale est vide
(`LiveUnifiedCarnet.jsx:43`). Lorsqu'elle contient des participations, il lit
les résumés de l'installation sans reprendre le rattachement que réalise
l'ancien `useLiveRewards.js:72–115`. Le backend filtre les récompenses selon les
participations suivies et leurs accès valides.

Une participation locale restaurée ou ancienne, un rattachement initial échoué
ou une installation renouvelée constituent donc des cas à reproduire : le
passeport peut être présent sans que sa récompense remonte dans le nouveau
carnet. Le bouton Actualiser ne reprend pas cette liaison dans ce composant.

**Action proposée avant une nouvelle passe graphique.** Comparer ancien et
nouveau parcours avec la même participation de test gagnante et un rattachement
manquant. Prévoir une reprise bornée à partir des accès valides, en conservant
les règles de refus et de renouvellement. Une amélioration visuelle seule ne
résout pas ce risque de continuité.

### CB04 — P1 — Le carnet doit porter la prochaine action quotidienne

**Revue de code.** La nouvelle liste classe les objets locaux et leurs résumés.
La logique « Un lot vous attend » / « À vous de jouer » reste dans `LiveHome.jsx`,
alors que `LiveRoot.jsx` envoie le retour générique d'un carnet connu vers Mon
carnet. Le meilleur raccourci personnel et l'entrée quotidienne sont ainsi
répartis entre deux écrans.

**Correction proposée.** En tête du carnet, afficher **une prochaine action**
fondée sur l'état confirmé : reprendre le parcours, présenter son coffret,
retirer ou activer son lot. Sous cette action, montrer les objets en cours avec
leurs tampons ou prestations restantes. Les favoris et l'historique restent
accessibles, avec une importance visuelle moindre. Ne pas inventer une urgence
ni réordonner les cartes pendant une interaction.

### CB05 — P1 — Les cartes doivent rendre les objets reconnaissables

**Observé sur le public.** L'animation utilise un petit pictogramme de lieu et
du texte. La section À gagner présente les deux coffrets essentiellement par
leur nom et leur quantité. Cela indique leur existence, mais permet peu de se
projeter dans la récompense. L'absence d'image observée ne prouve pas qu'un
visuel est disponible dans les données.

**Revue de code sur le personnel.** Le nouveau carnet utilise le même symbole
ticket pour animations et lots (`LiveUnifiedCarnet.jsx:143`). Sa projection de
récompense conserve peu du contexte présent dans l'ancien écran : animation
d'origine, échéance et consignes ne figurent pas sur la carte générique. Selon
le type d'accès, « Voir mon lot » rejoint la participation plutôt que le lot
exact (`unifiedCarnet.mjs:103–106`, `liveRewards.mjs:36`). Ce parcours n'a pas pu
être reproduit avec un gain dans le navigateur audité.

**Correction proposée.** Distinguer le passeport par ses tampons, le coffret
par ses prestations, le lot par un cadeau et son état de remise. Chaque carte
montre un titre, un état court et un seul verbe utile. Employer un visuel réel
s'il existe ; sinon, une illustration fonctionnelle propre au type d'objet.
« Voir mon lot » doit rejoindre ce lot ou sa section précise. Les conditions
de retrait restent atteignables sans être répétées sur toutes les cartes.

### CB06 — P2 — La fiche et les outils prennent le pas sur l'envie d'agir

**Observé.** À 360 pixels, la première vue de la fiche contient un bloc de
conditions de plusieurs lignes avant le détail des récompenses. Le bouton
d'inscription et la barre basse occupent simultanément le bas de l'écran.
À 320 × 568, sur Découvrir chargé, le bouton de la première animation nécessite
un défilement ; le haut affiche la marque, quatre outils, la commune, les deux
onglets et le titre de période avant cette carte.

**Correction proposée.** Composer la fiche autour de trois repères visibles :
**défi, progression attendue, récompense**. Résumer fidèlement la condition
essentielle, par exemple « Achat requis · sans minimum », avec le règlement
accessible avant engagement. Compacter les outils et espacements de Découvrir.
La mise en page doit privilégier l'action principale, sans retirer les conditions
utiles ni faire disparaître la navigation.

### CB07 — P2 — Les codes visuels varient entre les étapes

**Observé.** Découvrir utilise une petite marque et plusieurs outils ; le carnet
et le détail affichent la marque complète et les réglages. Actualiser change
de place et de représentation. Les actions principales sont tantôt bleu foncé
et arrondies, tantôt turquoise, puis orange et plus rectangulaires dans le
formulaire. Le texte du bouton final est « M'inscrire et enregistrer ».

**Correction proposée.** Stabiliser l'en-tête, la famille d'icônes et le style du
bouton principal. Réserver les variantes à des intentions explicites. Conserver
les libellés courts sous les icônes importantes : l'iconographie doit faciliter
la reconnaissance. Vérifier que « enregistrer » correspond bien à l'étape
effectuée ; expliquer par un parcours court les étapes inscription, e-mail,
puis ajout au carnet si cet ajout n'est pas immédiat.

Le téléphone obligatoire des inscriptions classiques reste la règle décidée ;
cet audit ne propose pas de la modifier. Les consentements conservent leurs
libellés et leur choix explicite.

### CB08 — P2 — La récupération juxtapose plusieurs explications

**Observé.** Retrouver mon carnet propose l'e-mail, explique à part les coffrets,
puis affiche une aide Déjà inscrit contenant trois situations et de longs
paragraphes. L'ancien écran Mes lots propose encore une autre aide en bas de
page, qui demande d'ouvrir un lien reçu par e-mail.

**Correction proposée.** Une entrée principale **Retrouver mes participations
et lots** avec pictogramme enveloppe. Présenter ensuite une confirmation simple
et l'objet retrouvé. Les alternatives « J'ai mon lien », « J'ai un coffret » et
« J'ai une sauvegarde » peuvent être des lignes courtes dépliables. Conserver le
périmètre décidé : participations et lots associés après vérification par
e-mail ; coffrets via leur récupération existante.

### CB09 — P2 — La découverte des commerces perd le contexte de proximité

**Observé.** Après Découvrir sur Latresne, l'onglet Commerçants ouvre un annuaire
sur « Toutes les communes », avec des premières adresses dans d'autres communes.
À 390 pixels, titre, retour, introduction et filtres repoussent la première
adresse vers le bas de la vue. Ce comportement peut exiger un nouvel effort de
sélection alors que la commune vient d'être choisie.

**Correction proposée.** Réutiliser visiblement le contexte communal ou proposer
un choix explicite pour l'élargir. Une ligne commune et une recherche compacte
suffisent en entrée ; les filtres avancés peuvent être dépliés. Une adresse
proposée doit aider à poursuivre le parcours ou à préparer une visite.

## Composition recommandée

La navigation principale proposée est **Mon carnet / Mes lots / Découvrir**,
avec icônes et libellés permanents. Le choix des communes reste disponible dans
Découvrir et ses sous-vues, via un sélecteur compact. Cette proposition modifie
explicitement CN-D01 ; elle n'est pas déjà une décision implémentée.

| Place dans le carnet | Rôle | Expression visuelle |
| --- | --- | --- |
| Première zone | Ce que je peux faire maintenant | Un objet personnel, un état confirmé, un bouton. |
| Parcours en cours | Mes progrès et la prochaine étape | Tampons, étapes validées, quantité courte telle que « 1 sur 2 ». |
| Coffrets | Ce qu'il me reste à utiliser | Visuel du coffret, prestations restantes, accès Présenter. |
| Lots | Ce que j'ai obtenu | Cadeau, état À retirer / À activer / Utilisé selon le fait réel, échéance utile. |
| Enregistrés et historique | Ce que je souhaite retrouver | Repères secondaires stables, hors de la priorité quotidienne. |

Les textures de papier, onglets ou tampons peuvent soutenir cette composition.
La sensation de carnet repose d'abord sur la continuité personnelle : **je
retrouve mes objets, je vois mes progrès, je sais quoi faire**. Éviter de
remplacer les textes indispensables par une série d'icônes ambiguës.

## Ordre de réalisation et recette à prévoir

1. **Accès et continuité des lots : CB01, CB03.** Restaurer le point d'entrée,
   reproduire le rattachement manquant, vérifier la destination exacte des gains.
2. **Carnet quotidien : CB02, CB04, CB05.** Prototyper avec un passeport commencé,
   un coffret partiellement utilisé et un lot à retirer, puis avec un carnet vide.
3. **Cohérence des étapes : CB06 à CB09.** Harmoniser fiche, inscription,
   récupération et commerces sans modifier leurs droits ni leurs obligations.

La recette devrait demander à un habitant, sans explication : « Retrouvez votre
lot », « Reprenez votre parcours », « Présentez votre coffret », « Retrouvez le
commerce à visiter ». Objectifs proposés : accès à Mes lots en un geste depuis
la navigation ; reconnaissance de l'état et de la prochaine action en quelques
secondes ; aucune confusion entre un lot à gagner et un lot obtenu. Les délais
de compréhension restent à mesurer avec des habitants.

Contrôler les tailles 320 × 568, 360 × 800 et 390 × 844, le texte agrandi, le
clavier et les cibles tactiles. Inclure chargement, panne partielle, absence
locale, accès expiré/révoqué et reprise d'une participation ancienne. Les états
vides ne doivent pas apparaître comme une conclusion pendant le chargement ;
des messages d'absence transitoires ont été vus sur Découvrir avec les squelettes.

## Sources et impacts

- [Spécification E73 et critères CN](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md),
  notamment CN-01 à 06, CN-09/10, CN-13/14 et CN-17. La future évolution devra
  tracer les modifications de CN-D01 et du masquage des catégories de CN-03.
- [Audit initial du 9 novembre](20261109-Audit%20Localeo%20Live.pdf) : conservé
  comme constat antérieur ; ce nouvel audit confronte la refonte à l'usage.
- Marketplace : [LiveApp](../../../../localeo-marketplace/src/live/LiveApp.jsx),
  [LiveUnifiedCarnet](../../../../localeo-marketplace/src/live/LiveUnifiedCarnet.jsx),
  [unifiedCarnet](../../../../localeo-marketplace/src/live/unifiedCarnet.mjs),
  [useLiveRewards](../../../../localeo-marketplace/src/live/useLiveRewards.js),
  [LiveLots](../../../../localeo-marketplace/src/live/LiveLots.jsx),
  [liveRewards](../../../../localeo-marketplace/src/live/liveRewards.mjs),
  [LiveHome](../../../../localeo-marketplace/src/live/LiveHome.jsx),
  [LiveRoot](../../../../localeo-marketplace/src/live/LiveRoot.jsx),
  [récupération](../../../../localeo-marketplace/src/live/LiveCarnetRecovery.jsx).
- Backend : [récompenses](../../../../localeo-backend/app/infrastructure/persistence/repositories/recompenses_live_repository.py)
  et [suivis](../../../../localeo-backend/app/infrastructure/persistence/repositories/rappels_live_repository.py)
  pour les préconditions de lecture ; aucune modification du domaine proposée
  sans reproduction du cas de continuité.

Livrable de ce tour : audit et index documentaire uniquement. Aucune correction
applicative, migration, modification de données métier, commit ou push.
La roadmap, les contrats et les preuves antérieures restent inchangés. La future
recette nécessitera un jeu de démonstration mixte ; aucun jeu n'a été généré pour
cette observation. Une capture du carnet vide en viewport 320 × 568 a été
téléchargée depuis Chrome, vérifiée et conservée hors des dépôts. Les autres
constats visuels reposent sur les captures de fenêtre inspectées pendant la
navigation.
