# ÉTAPE 2 — WORKSHOP UX MULTI-EXPERTS ET HABITANTS

Tu es chargé de réaliser un workshop UX contradictoire sur Localeo Live.

## 1. Charger le contexte

Identifie le dernier répertoire de workshop créé dans :

`docs/ux-workshops/`

Utilise exclusivement ce répertoire pour l'exécution en cours.

Lis intégralement :
- `README.md`
- `observations/cartographie-parcours.md`
- `observations/inventaire-ecrans.md`
- `observations/observations-factuelles.md`
- `observations/limitations.md`

Consulte les captures réelles.

Enregistre le texte complet de cette instruction dans :

`prompts/02-workshop.md`

## 2. Objectif

Évaluer la capacité d'un habitant à accomplir spontanément les trois missions prioritaires :

1. Participer aux animations de sa commune.
2. Retrouver, comprendre et utiliser ses lots.
3. Consulter le calendrier des animations.

La simplicité, l'accessibilité et la compréhension immédiate priment sur la richesse fonctionnelle.

## 3. Composition de la réunion

Simule 12 participants indépendants.

### Six experts

1. UX Designer senior : navigation, hiérarchie visuelle, ergonomie.
2. Expert accessibilité : lisibilité, WCAG, usages peu familiers du numérique.
3. Product Manager B2C : proposition de valeur et périmètre MVP.
4. Expert onboarding : première impression, QR codes, activation et adoption.
5. UX Researcher : scénarios, biais et qualité des observations.
6. Facilitateur produit : débats, arbitrages et organisation des votes.

### Six habitants

**Marie, 72 ans** : très peu à l'aise avec le numérique ; souhaite participer à une tombola et retrouver son lot.

**Jean-Pierre, 64 ans** : utilisateur occasionnel ; découvre une animation par QR code.

**Sophie, 46 ans** : utilisatrice intermédiaire ; souhaite consulter les prochaines animations familiales.

**Thomas, 32 ans** : utilisateur expérimenté ; attend une participation rapide et fluide.

**Nathalie, 55 ans** : faible appétence numérique ; souhaite retrouver un lot et savoir comment en profiter.

**Lucie, 21 ans** : utilisatrice très connectée ; souhaite suivre ses participations et découvrir les prochaines animations.

Chaque participant doit avoir une perspective indépendante.

Les habitants doivent s'exprimer naturellement, sans jargon UX.

Leurs réactions sont des simulations, jamais des résultats de tests réels.

## 4. Déroulement des ateliers

Organise six ateliers :

### Atelier A — Première impression

L'habitant comprend-il immédiatement à quoi sert Localeo Live ?

Les trois missions sont-elles visibles et compréhensibles ?

### Atelier B — Participation aux animations

Peut-on découvrir, rejoindre, suivre et retrouver une animation sans assistance ?

Analyse particulièrement le parcours QR code.

### Atelier C — Gestion des lots

Peut-on retrouver un gain, comprendre son statut et savoir comment l'utiliser ?

### Atelier D — Calendrier des animations

Peut-on identifier rapidement les animations à venir, leurs dates et les modalités de participation ?

Challenge les différentes présentations possibles : liste, calendrier, cartes.

### Atelier E — Maniabilité et accessibilité

Les trois missions sont-elles facilement réalisables sur smartphone, y compris pour les personnes peu familières du numérique ?

### Atelier F — Simplification et adoption

Quels éléments peuvent être simplifiés ?

Pourquoi un habitant reviendrait-il naturellement dans Localeo Live ?

## 5. Protocole de chaque atelier

Pour chaque atelier :

1. Présente les écrans et parcours réellement observés.
2. Fais formuler un avis indépendant aux experts.
3. Simule les réactions individuelles des habitants.
4. Organise un débat contradictoire.
5. Identifie les points forts.
6. Identifie les problèmes.
7. Formule les orientations d'amélioration.
8. Organise les votes.
9. Enregistre les décisions.

Ne fabrique pas de constats ou de mesures empiriques.

## 6. Gouvernance par vote

Chaque participant dispose d'une voix.

Une orientation est adoptée uniquement si elle obtient au moins **7 voix favorables sur 12**.

- 7 à 12 voix : ADOPTÉE.
- 6 voix : NON ADOPTÉE.
- 0 à 5 voix : REJETÉE.

Les participants peuvent voter pour, contre ou s'abstenir.

Les abstentions ne réduisent pas le seuil de sept voix favorables.

Chaque vote doit être individuel, cohérent avec les arguments du participant et enregistré nominativement.

Ne recherche pas artificiellement l'unanimité.

Les orientations rejetées doivent être conservées séparément.

Les problèmes critiques de sécurité, de fonctionnement ou d'accessibilité doivent rester signalés, même si leur correction est rejetée par la simulation.

## 7. Priorisation

Classe les orientations adoptées :

- P0 : bloquant pour une mission essentielle.
- P1 : friction majeure à corriger avant lancement.
- P2 : amélioration importante mais différable.
- P3 : confort ou évolution secondaire.

Pour chaque orientation, précise :
- Identifiant.
- Mission concernée.
- Problème.
- Preuve ou hypothèse.
- Solution.
- Bénéfice utilisateur.
- Critères d'acceptation.
- Effort S/M/L/XL.
- Priorité.
- Résultat du vote.
- Niveau de confiance.

Ne surclasse pas artificiellement les recommandations.

## 8. Livrables

Dans `workshop/`, crée :

- `rapport-executif.md`
- `compte-rendu.md`
- `votes-et-arbitrages.md`
- `backlog-ux.md`
- `orientations-rejetees.md`
- `quick-wins.md`

Le rapport exécutif doit inclure des notes heuristiques sur 10 pour :
- La première impression.
- La participation aux animations.
- La gestion des lots.
- Le calendrier.
- La maniabilité mobile.
- L'accessibilité.

Justifie chaque note.

Produis une matrice croisant les six habitants et les parcours principaux.

Termine par une recommandation :

GO / GO SOUS CONDITIONS / NO GO.

## 9. Question finale

« Si Localeo Live devait être ouvert demain à 10 000 habitants, quelles seraient les cinq améliorations les plus importantes pour rendre la participation aux animations, la gestion des lots et la consultation du calendrier simples et accessibles ? »

Ne retiens que des orientations adoptées.

S'il y en a moins de cinq réellement indispensables, ne complète pas artificiellement la liste.

## 10. Contraintes et arrêt

- Aucune modification applicative.
- Aucune maquette à cette étape.
- Aucun résultat simulé présenté comme une mesure réelle.
- Aucun changement de périmètre vers les fonctionnalités secondaires.

Mets à jour le README et enregistre tous les livrables dans le répertoire daté.

Arrête-toi et attends mon autorisation avant l'étape 3.
