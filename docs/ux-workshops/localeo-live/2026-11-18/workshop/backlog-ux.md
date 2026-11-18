# Backlog UX — orientations adoptées

**Suite du 18 novembre :** adoption utilisateur des six orientations pour cadrage,
A1/F1 P2 ; [décision](../validation/decisions.md) et
[backlog canonique E73-WL](../../../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-live-20261118).
Les mentions d'attente ci-dessous conservent l'état de la simulation initiale.
Le suivi des travaux est désormais dans E73 :
[spécification et réalisation locales](../../../../specifications/epic-73-animation-et-ou-coffrets/workshop-live-20261118.md).
Les observations et bénéfices attendus ci-dessous conservent leur portée initiale.

**État initial : backlog de conception issu d’une simulation, non implémenté.** Les bénéfices décrits sont attendus, pas mesurés. Références : [observations](../observations/observations-factuelles.md), [limites](../observations/limitations.md), [votes nominatifs](votes-et-arbitrages.md).

P0 = mission essentielle bloquée ; P1 = friction majeure à traiter avant lancement ; P2 = amélioration importante différable ; P3 = confort. **Aucun P0 établi.** Les P1 B1, C1 et E1 portent d’abord sur la levée d’incertitudes et une recette avant lancement ; l’effort de correction ne doit être engagé qu’après constat d’un écart. Une absence de test n’est pas une panne. D1 répond à une densité directement visible, dont l’impact habitant reste hypothétique.

Effort qualitatif, sans estimation de délai : S = texte ou accès local ; M = plusieurs états d’un parcours et recette ; L = plusieurs parcours/contrats ; XL = évolution structurelle. Les estimations ci-dessous restent provisoires.

| ID | Orientation | Priorité | Effort | Voix favorables |
| --- | --- | --- | --- | ---: |
| A1 | Relier explicitement le carnet aux trois missions | P2 | S | 11/12 |
| B1 | Conserver le contexte de l’animation du QR à la reprise | P1 | M | 12/12 |
| C1 | Rendre le lot confirmé immédiatement compréhensible et actionnable | P1 | M | 12/12 |
| D1 | Présenter un programme chronologique compact et un accès Prochainement | P1 | M | 11/12 |
| E1 | Vérifier l’accessibilité puis corriger les obstacles établis | P1 | M | 12/12 |
| F1 | Organiser la reprise autour de l’état confirmé et de la prochaine action | P2 | M | 12/12 |

## A1 — Relier explicitement le carnet aux trois missions

- **Mission :** Les trois missions ; première entrée.
- **Problème :** Le carnet vide présente Parcours et Coffrets, tandis que les dates se découvrent dans une autre rubrique. La compréhension immédiate de cet ensemble reste inconnue.
- **Preuve ou hypothèse :** OBSERVÉ : O1, O2 et captures 01 à 320/390 px. HYPOTHÈSE H1 : une phrase reliant animations, gains et programme aiderait à choisir.
- **Solution :** Une phrase concrète sur le carnet vide relie les trois missions aux destinations existantes ; l’accès au programme est nommé dans Découvrir. Préserver trois onglets, l’en-tête et une action principale.
- **Bénéfice utilisateur attendu :** Comprendre quoi retrouver et où commencer sans apprentissage du mot « carnet ».
- **Effort / priorité :** S / P2.
- **Vote simulé :** 11 pour, 0 contre, 1 abstention — **ADOPTÉE**.
- **Confiance :** Moyenne sur la cohérence du contenu ; faible sur le bénéfice habitant, non mesuré.
- **Dépendances et impacts :** Coordonner le libellé du programme avec D1 et la référence UX existante ; aucun changement de contrat ou migration prévu.

Critères d’acceptation proposés, à vérifier ultérieurement :

1. Depuis le carnet vide, un texte court nomme animations, lots et programme ; les destinations annoncées existent.
2. Dans Découvrir, l’accès aux animations à venir porte un libellé explicite ; aucune promesse de gain automatique ou de synchronisation de compte.
3. À 320 px et texte agrandi, l’explication n’occulte pas l’action de découverte ; recette de compréhension sur tâches sans explication préalable, résultat à documenter.

## B1 — Conserver le contexte de l’animation du QR à la reprise

**Étape 3 — maquettes conditionnelles :** [comparatif B1](../visuels/comparatif-avant-apres.html#B1), [inscription](../visuels/maquettes-apres/B1-inscription.html), [confirmation illustrative](../visuels/maquettes-apres/B1-confirmation.html), [résultat incertain](../visuels/maquettes-apres/B1-incertain.html). Continuité représentée, non exécutée ; recette positive toujours requise.

- **Mission :** Participer à une animation et la retrouver.
- **Problème :** Le QR invalide et le formulaire sont documentés séparément. Le parcours positif, la confirmation et la reprise n’ont pas été vérifiés.
- **Preuve ou hypothèse :** OBSERVÉ : O5, O6, O9 ; captures 03, 04, 06 et 10. HYPOTHÈSE H2 : conserver le contexte limitera la désorientation ; aucune perte de contexte constatée.
- **Solution :** Vérifier avec un QR valide de Bouliac la chaîne fiche → inscription → résultat confirmé → carnet → reprise. Corriger uniquement les écarts : titre public conservé si connu, prochaine étape explicite, récupération accessible sur erreur et retour utile.
- **Bénéfice utilisateur attendu :** Savoir à quelle animation l’action se rapporte et si la participation est effectivement enregistrée.
- **Effort / priorité :** M / P1.
- **Vote simulé :** 12 pour, 0 contre, 0 abstention — **ADOPTÉE**.
- **Confiance :** Faible sur le besoin de modification ; élevée sur la nécessité de couvrir le parcours positif.
- **Dépendances et impacts :** Identité autorisée et QR Bouliac requis. Utiliser les contrats existants ; toute donnée absente du contrat appelle un arbitrage séparé. Aucun changement de règle de collecte adopté.

Critères d’acceptation proposés, à vérifier ultérieurement :

1. Jeu de test autorisé : QR valide, lien invalide/expiré, inscription réussie, erreur et résultat incertain ; chaque branche a une preuve navigateur.
2. L’identité publique de l’animation connue traverse les étapes ; un code inconnu ne révèle ni n’invente d’informations personnelles.
3. Seule la réponse métier confirme inscription ou participation ; une réponse incertaine propose une vérification, sans double envoi silencieux.
4. Après inscription confirmée, fermeture puis retour à l’application permet de retrouver la participation ; le détour par récupération conserve une destination explicite.

## C1 — Rendre le lot confirmé immédiatement compréhensible et actionnable

**Étape 3 — maquettes conditionnelles :** [comparatif C1](../visuels/comparatif-avant-apres.html#C1), [disponible](../visuels/maquettes-apres/C1-disponible.html), [incertain](../visuels/maquettes-apres/C1-incertain.html), [remis](../visuels/maquettes-apres/C1-remis.html), [expiré](../visuels/maquettes-apres/C1-expire.html), [annulé](../visuels/maquettes-apres/C1-revoque.html), [présentation du bon](../visuels/maquettes-apres/C1-bon.html). Données fictives ; AVANT attribué absent, comparaison non équivalente.

- **Mission :** Retrouver, comprendre et utiliser ses lots.
- **Problème :** L’état vide est clair, mais il ne renseigne pas sur l’autonomie devant un lot réellement attribué. L’état personnel et les modalités de remise sont non testés.
- **Preuve ou hypothèse :** OBSERVÉ : O7 et O8, captures 08 et 09. DÉDUIT : D1, états de lots présents dans le code. HYPOTHÈSE H3 : l’ordre état → conditions pratiques → action aide le gagnant.
- **Solution :** Confronter la fiche existante à des lots réels de test. Si nécessaire, présenter d’abord le gain, sa disponibilité confirmée, sa limite de validité, où/comment l’utiliser et l’action autorisée. Maintenir récupération et états inconnus explicites.
- **Bénéfice utilisateur attendu :** Éviter un déplacement sans consigne et distinguer un gain consulté d’un gain remis.
- **Effort / priorité :** M / P1.
- **Vote simulé :** 12 pour, 0 contre, 0 abstention — **ADOPTÉE**.
- **Confiance :** Faible sur les écarts d’interface ; élevée sur les distinctions métier à conserver.
- **Dépendances et impacts :** Lots de test et interlocuteur de remise nécessaires. Pas de transition métier, contrat, migration ou démonstration modifiés par ce workshop.

Critères d’acceptation proposés, à vérifier ultérieurement :

1. Couvrir un lot disponible, remis, expiré/révoqué et temporairement non vérifiable ; chacun affiche son état confirmé ou son incertitude sans assimilation.
2. Le lot disponible expose la date limite et le lieu ou mode de retrait lorsqu’ils existent ; information manquante signalée, jamais inventée.
3. L’action adaptée respecte l’état renvoyé par le domaine ; afficher/fermer le QR et marquer comme vu ne consomment pas le lot.
4. La lecture après remise reflète la confirmation du système ; un autre appareil passe par l’accès ou la récupération autorisés.
5. Recette de compréhension : demander où, avant quand et comment profiter du lot ; consigner les réponses réelles avant de conclure.

## D1 — Présenter un programme chronologique compact et un accès Prochainement

**Étape 3 — maquettes :** [comparatif D1](../visuels/comparatif-avant-apres.html#D1), [programme de Bouliac](../visuels/maquettes-apres/D1-programme.html), [vide illustratif](../visuels/maquettes-apres/D1-vide.html), [erreur illustrative](../visuels/maquettes-apres/D1-erreur.html). Conditions clés conservées, bénéfice à mesurer.

- **Mission :** Consulter les animations en cours et à venir.
- **Problème :** Les longues descriptions sur les cartes précèdent l’animation à venir dans les captures de Bouliac. Les dates existent mais leur comparaison nécessite de parcourir ces cartes.
- **Preuve ou hypothèse :** OBSERVÉ : O4, O5, O11 et captures 02 à 320/390/430 px. HYPOTHÈSE H4 : une liste plus compacte et un accès direct à Prochainement faciliteront la planification.
- **Solution :** Conserver un programme en liste, avec sections temporelles, entrée Prochainement visible, titre, date, statut et commune. Réserver les longs développements au détail ; garder dans la liste les conditions déterminantes pour choisir.
- **Bénéfice utilisateur attendu :** Repérer une prochaine animation et vérifier ses dates avant d’ouvrir sa fiche.
- **Effort / priorité :** M / P1.
- **Vote simulé :** 11 pour, 0 contre, 1 abstention — **ADOPTÉE**.
- **Confiance :** Moyenne : densité visible, bénéfice comparatif à vérifier auprès d’habitants.
- **Dépendances et impacts :** Conserver trois onglets et intégrer la cible aux références UX canoniques lors d’une phase ultérieure. Aucune nouvelle catégorie familiale ni grille obligatoire.

Critères d’acceptation proposés, à vérifier ultérieurement :

1. L’entrée Prochainement est accessible depuis le haut de Découvrir sans traverser les descriptions des animations en cours.
2. Chaque ligne/carte affiche titre, période réelle, état et contexte communal ; un manque de date est explicite.
3. Le tri utilise les dates confirmées au sein des groupes, sans modifier les règles de statut du backend ; dates en heure de Paris selon la convention du projet.
4. L’achat requis ou une restriction déterminante demeure visible avant inscription ; le détail conserve règlement et conditions complets.
5. Tester zéro, une et plusieurs animations dans chaque période ; retour fiche → programme conserve commune, filtres et position pertinente.

## E1 — Vérifier l’accessibilité puis corriger les obstacles établis

**Étape 3 — maquettes conditionnelles :** [comparatif E1](../visuels/comparatif-avant-apres.html#E1), [accès invalide](../visuels/maquettes-apres/E1-acces-invalide.html), [erreur e-mail](../visuels/maquettes-apres/E1-formulaire-erreur.html), [contrôles locaux](../visuels/controles/controle-technique.md). Les mesures des planches ne valident pas l’accessibilité de l’application.

- **Mission :** Les trois missions sur mobile et avec aides d’accès.
- **Problème :** Les captures ne prouvent pas l’usage au clavier, au zoom, avec lecteur d’écran ou une récupération après erreur. Le texte sombre du bouton QR appelle un contrôle de contraste.
- **Preuve ou hypothèse :** OBSERVÉ SUR CAPTURE : 10 pour le bouton ; 01 à 430 px est un chargement. NON EXÉCUTÉ : audit d’accessibilité. HYPOTHÈSE H5 : certains états pourraient gêner ces usages.
- **Solution :** Faire une recette ciblée des actions essentielles et corriger les obstacles établis. Préserver textes visibles, focus, annonces et messages explicites ; documenter le résultat de chaque contrôle.
- **Bénéfice utilisateur attendu :** Accomplir les missions sans dépendre de la vision, d’un geste précis ou d’une mémoire des pictogrammes.
- **Effort / priorité :** M / P1.
- **Vote simulé :** 12 pour, 0 contre, 0 abstention — **ADOPTÉE**.
- **Confiance :** Élevée sur le besoin de contrôle ; faible sur la présence et l’étendue des défauts.
- **Dépendances et impacts :** Référence WCAG 2.2 et principes UX locaux ; priorité d’une correction à réévaluer seulement si un obstacle bloquant est reproduit.

Critères d’acceptation proposés, à vérifier ultérieurement :

1. Parcourir les trois missions au clavier et lecteur d’écran : noms, rôles, ordre du focus, erreurs et états annoncés ; absence de piège ; preuves conservées.
2. À 320 px, texte agrandi à 200 % et test de redistribution adapté, contenu et commandes essentiels restent disponibles ; contrôler le focus face à la barre fixe et au clavier virtuel.
3. Mesurer contrastes du texte et commandes sur les états normaux/erreurs, notamment le bouton de récupération QR, et corriger les écarts établis.
4. Mesurer les cibles ; appliquer la cible locale de 44 px pour les commandes essentielles, distincte du minimum WCAG 2.2 et de ses exceptions.
5. Soumission invalide, chargement, erreur réseau et résultat incertain conservent un chemin compréhensible ; aucune conformité globale annoncée après cette seule recette.

## F1 — Organiser la reprise autour de l’état confirmé et de la prochaine action

- **Mission :** Suivre et retrouver ses participations et lots.
- **Problème :** La commune est conservée au retour, mais le carnet rempli et sa prochaine action n’ont pas été inspectés.
- **Preuve ou hypothèse :** OBSERVÉ : O10 et capture 11 ; O7 carnet vide seulement. DÉDUIT : composants de carnet personnel. HYPOTHÈSE H6 : une reprise adaptée à l’état facilite le retour.
- **Solution :** Vérifier le carnet rempli, puis compléter les écarts éventuels : état personnel confirmé, prochaine action adaptée et récupération accessible, y compris après interruption. S’appuyer sur l’existant.
- **Bénéfice utilisateur attendu :** Reprendre une activité en cours ou retrouver un résultat sans refaire la découverte.
- **Effort / priorité :** M / P2.
- **Vote simulé :** 12 pour, 0 contre, 0 abstention — **ADOPTÉE**.
- **Confiance :** Faible : l’interface personnelle existe dans le code mais reste non éprouvée ici.
- **Dépendances et impacts :** Partage la recette personnelle de B1/C1. Complément conditionnel à un écart, aucune reconstruction du domaine dans l’interface.

Critères d’acceptation proposés, à vérifier ultérieurement :

1. Couvrir une participation en cours, achevée et un résultat connu ; l’action principale correspond à l’état confirmé.
2. Une progression inconnue n’est pas annoncée comme acquise ; un lot attribué est retrouvé dans Mes lots sans le confondre avec une dotation à gagner.
3. Le lien de récupération reste accessible dans un carnet rempli ; deux participations distinctes ne sont pas fusionnées.
4. Au retour après fermeture, la participation autorisée et les repères utiles sont retrouvables ; aucun abonnement aux notifications n’est imposé.

## Cadre transversal et suite

Étape 3 : [référence détaillée des 14 planches](../visuels/reference-maquettes.md) et [revue contradictoire simulée](../visuels/revue-contradictoire.md). Quatre P1 seulement ; A1/F1 restent P2 sans maquette. Les votes et priorités d’origine sont inchangés ; aucun changement substantiel retenu, aucun nouveau vote. Validation utilisateur des maquettes attendue.

Les orientations concernent le consommateur `localeo-marketplace` et sa surface Live. Le backend demeure propriétaire des statuts, droits et transitions. Ce workshop ne modifie aucun contrat API, migration, jeu de démonstration, configuration d’exploitation ou code. Pour B1/C1/F1, les données de test sont une dépendance de recette ; leur absence ne justifie pas de générer ou modifier un environnement réel.

La [référence UX Live](../../../../produit/live/principes-ux.md) conserve l’en-tête et les trois onglets. Les présentes orientations ne remplacent pas les arbitrages et maquettes du 17/18 novembre ; une divergence future devra être identifiée dans la source canonique avant implémentation. Les règles d’inscription restent inchangées après le rejet de B2.

Pour E1, la recette cible notamment contraste, redistribution, clavier, focus visible/non masqué, libellés, erreurs et noms accessibles. Les critères et exceptions doivent être lus dans les [WCAG 2.2 du W3C](https://www.w3.org/TR/WCAG22/) ; le seuil local de 44 px est une exigence de conception Localeo, pas une reformulation du minimum WCAG. Aucun audit de conformité n’a été réalisé dans ce workshop.

Si un parcours satisfait déjà ces critères, conserver le comportement et documenter sa preuve plutôt que créer une modification. Les critères d’essais habitants seront précisés à la phase de validation ; aucun taux de réussite ou temps cible empirique n’est inventé ici.
