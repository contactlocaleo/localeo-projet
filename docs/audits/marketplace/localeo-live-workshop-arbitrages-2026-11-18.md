# Localeo Live — audit des suites du workshop du 18 novembre 2026

## Conclusion et décision utilisateur

Les **six orientations A1/B1/C1/D1/E1/F1 sont retenues pour le cadrage** par
la réponse utilisateur du 18 novembre 2026 : « Retenir les six orientations,
avec A1/F1 en P2 ». B1/C1/D1/E1 restent P1 ; aucun P0 n'est établi.
Cette décision succède au registre initial sans validation. Elle ne transforme
ni les votes simulés en essais habitants, ni les maquettes en application testée.

Le [cadrage canonique E73-WL](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-live-20261118)
porte les travaux et leurs critères. L'EPIC 73 existante est réutilisée, avec
sa clôture historique conservée. Ce rapport ne crée pas de backlog concurrent.
L'audit initial portait sur l'analyse et le cadrage. La demande suivante a
explicitement autorisé spécification et implémentation : voir la
[réalisation et les preuves WL](../../specifications/epic-73-animation-et-ou-coffrets/workshop-live-20261118.md).
Le suivi ci-dessous intègre cette réalisation locale. Les sections explicitement
marquées « initial » conservent les constats et la portée de l'audit documentaire.

## Actions prises en compte — mise à jour du 18 novembre 2026

**Spécification et réalisation locales effectuées dans E73-WL.** Les six
orientations sont prises en compte, avec A1/F1 en P2. Une qualification conforme
de l'existant ne nécessite pas de modification artificielle. Le
[bilan canonique WL](../../specifications/epic-73-animation-et-ou-coffrets/workshop-live-20261118.md#bilan-dexécution)
porte le détail des scénarios, des tentatives et des limites.

| Action / critères | État actuel | Actions prises en compte et preuves | Reste à qualifier |
| --- | --- | --- | --- |
| **A1 · P2** — WL-01/02 | **Réalisée localement** | Texte du carnet vide reliant animations, Mes lots et programme dans Découvrir ; trois onglets conservés. Vérification à 320 px et texte 200 %, accès à la découverte et à la récupération préservés. | Compréhension par les habitants : WL-18. |
| **B1 · P1** — WL-03/04/05/15 | **Qualifiée sur fixtures ; complément réalisé** | Issue sans inscription explicitée après QR refusé. Parcours depuis l'URL publique du QR jusqu'à l'inscription confirmée puis au même accès après rechargement testé ; refus, stockage en panne et résultat incertain vérifiés sans réinscription silencieuse. | Scan optique et reprise sur un autre appareil réel non exécutés ; essais habitants WL-18. |
| **C1 · P1** — WL-06/07/08 | **Existant qualifié sur fixtures** | Trois natures de gains, états disponibles/remis/expirés/révoqués et incertains, consignes manquantes, échéances et accès exacts vérifiés. Présenter/fermer le bon ne consomme rien ; remise affichée après confirmation métier. Aucune nouvelle transition ni correction métier nécessaire dans les scénarios vérifiés. | Compréhension des modalités « où, avant quand, comment » avec des habitants : WL-18. |
| **D1 · P1** — WL-09/10/11 | **Réalisée localement** | Navigation « En ce moment / Prochainement » disponible en haut des petits programmes ; dates et commune remontées, règles Juste Prix/Vitrines condensées, restrictions conservées. Tri de la seule fenêtre historique chargée, ordre/pagination serveur préservés. Tests mobile 320/390/430, vide/erreur, retours, focus et nombre d'appels réussis. | Bénéfice de compréhension et de compacité à mesurer avec les habitants : WL-18. |
| **E1 · P1** — WL-12/13/14/15 | **Correction réalisée ; qualification partielle** | Contraste du bouton de récupération QR reproduit à 2,27:1 puis corrigé : 6,66:1 normal, 6,85:1 focus, 8,12:1 survol ; cible 252 × 44 px. Clavier, noms accessibles, focus, redistribution et texte 200 % contrôlés sur les parcours ciblés. | Lecteur d'écran et clavier virtuel sur appareil physique : WL-12/13. Pas de conformité globale revendiquée. |
| **F1 · P2** — WL-05/16/17 | **Existant qualifié sur fixtures** | Carnet rempli, prochaine action selon l'état confirmé, deux participations distinctes, état inconnu/refus et lectures bornées vérifiés. Retours vers participation/coffret et reprise conservés sans réintroduire les filtres internes du carnet. | Reprise sur appareil réel et essais habitants : WL-18. |

**Quick wins pris en compte :** QW-1 dans le texte A1, QW-2 dans le programme
D1 et QW-3 dans la mesure puis correction du contraste E1.

Preuves de réalisation : **102 scénarios navigateur réussis**, aucun échec,
skip ou flaky, dans le passage final `2026-11-18T14-14-53-678Z-rqPOkN` ;
**318 tests de sécurité réussis**. Build isolé, lint ciblé et contrôles
documentaires réussis. Le lint global reste bloqué par `EPERM scandir` sur
`output/bum-politique/pytest-approval-1` ; cette limite n'est pas masquée.
Ces résultats proviennent de la réalisation consignée dans le bilan, sans
nouvelle exécution applicative pour la présente mise à jour de l'audit.

**Travaux restant ouverts :** composantes humaines de WL-12/13 et essais
habitants WL-18 ; aucune amélioration de compréhension ou de temps n'est
mesurée. WL-L0, WL-L1 et WL-L2 sont réalisés ; WL-L3 est terminé pour la
recette automatisée et reste ouvert pour cette qualification humaine.
La réalisation a modifié Projet et Marketplace, sans changement d'API ni
migration. La [publication Git ensuite autorisée](../../specifications/epic-73-animation-et-ou-coffrets/workshop-live-20261118.md#publication-git-autorisée-le-18-novembre-2026)
trace le commit Marketplace `29053df` poussé et la documentation associée.
Aucun déploiement effectué ; clôture historique E73 conservée.

## Sources et portée de l'analyse initiale

- [Workshop Live / Bouliac](../../ux-workshops/localeo-live/2026-11-18/README.md),
  identifié comme le workshop demandé (« localeo-livedu 2026-11-18 »).
- [Observations O1 à O11 et déduction D1](../../ux-workshops/localeo-live/2026-11-18/observations/observations-factuelles.md),
  [limites](../../ux-workshops/localeo-live/2026-11-18/observations/limitations.md),
  [backlog des six orientations](../../ux-workshops/localeo-live/2026-11-18/workshop/backlog-ux.md),
  [votes simulés](../../ux-workshops/localeo-live/2026-11-18/workshop/votes-et-arbitrages.md).
- [Registre utilisateur actualisé](../../ux-workshops/localeo-live/2026-11-18/validation/decisions.md),
  [précisions M01–M08](../../ux-workshops/localeo-live/2026-11-18/visuels/revue-contradictoire.md)
  et [quick wins](../../ux-workshops/localeo-live/2026-11-18/workshop/quick-wins.md).
- [Référence UX obligatoire](../../produit/live/principes-ux.md) et
  [spécification Live E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md) :
  LM-01 à LM-11, puis correctifs LIVE-COR-01 à LIVE-COR-07 du 18 novembre.

L'analyse initiale était documentaire, sans nouvelle navigation TEST, reproduction applicative
ou exécution de tests métier. Les résultats applicatifs déjà consignés dans E73
ne sont pas rejoués ici. Le workshop a observé un navigateur vierge à Bouliac,
au commit Marketplace `db4dc57e6b2fd78f83a9d2981d181c0eb17c582d` ; il n'établit
pas l'état de la version courante ou déployée après les correctifs du 18 novembre.
Les captures initiales à 430 px en chargement et les captures longues avec barre
fixe ne suffisent pas à prouver un obstacle. Aucun carnet rempli, lot attribué,
QR positif ou inscription confirmée n'a été éprouvé par ce workshop.

## Qualification initiale des travaux retenus

| Orientation | Nature et constat | Recouvrement et suite à donner |
| --- | --- | --- |
| A1 · P2 | Complément éditorial : relier animations, lots et programme dans le carnet vide et nommer le programme dans Découvrir. Compréhension habitant non mesurée. | Complète LIVE-UX-01 et LM-01. Vérifier le texte courant, ajouter uniquement le complément utile ; pas de quatrième onglet. |
| B1 · P1 | Qualification de continuité puis correction conditionnelle. O5/O6/O9 documentent fiche/formulaire/QR invalide séparément, aucune rupture positive prouvée. | LM-04 et les tests de confirmation décrivent déjà reçu métier, stockage et incertitude. Recette QR valide → inscription → résultat → carnet → reprise, erreurs comprises ; corriger seulement les écarts reproduits. |
| C1 · P1 | Qualification des lots puis correction conditionnelle de leur présentation. O7/O8 ne couvrent que lots vides et récupération. | LM-09/10 couvrent déjà état, consignes, échéance, bon et vu local. Éprouver les trois natures de gains et les états autorisés ; compléter les informations réellement disponibles, sans nouvelle transition de remise. |
| D1 · P1 | Évolution de présentation du programme : densité observée O4/O5/O11, bénéfice de la compacité encore hypothétique. | Complète LM-03 et la découverte existante : sections chronologiques, Prochainement accessible en haut, dates/statuts/commune et conditions déterminantes. Conserver les correctifs LIVE-COR-04/05 et les retours. |
| E1 · P1 | Campagne ciblée d'accessibilité puis corrections d'obstacles établis ; aucune non-conformité globale prouvée. | LM-11 prévoit déjà clavier, focus, 44 px et texte 200 %. Réutiliser les preuves applicables, compléter lecteur d'écran, clavier virtuel, contrastes et reprise ; les contrôles des planches ne valident pas l'application. |
| F1 · P2 | Qualification de reprise puis complément conditionnel ; carnet rempli absent de la recette initiale. | LM-05/06 et LIVE-COR-01/02 couvrent déjà récupération, identité, priorité et fraîcheur. Tester fermeture/retour, plusieurs participations et états inconnus, sans reconstruction ni régression du carnet. |

**L'audit documentaire initial ne démontrait aucune correction applicative nouvelle.**
La recette ultérieure a reproduit le défaut de contraste décrit dans le suivi ci-dessus.
L'adoption porte aussi sur la qualification des parcours : un résultat conforme
se clôt par une preuve réutilisable, sans retouche artificielle. D1 et A1 portent
des évolutions identifiables ; B1/C1/E1/F1 demandent d'abord de constater l'écart
résiduel avec l'existant. Les priorités ne constituent pas une date de livraison.

## Arbitrages, exclusions et compatibilité

Les six alternatives rejetées par le workshop restent hors périmètre : A2
(quatrième onglet), B2 (suppression de champs obligatoires), C2 (QR consommateur),
D2 (grille mensuelle imposée), E2 (icônes seules), F2 (notifications imposées
dès l'entrée). Leurs votes ne sont pas des refus utilisateur individuels ;
l'adoption des six orientations n'introduit aucune de ces alternatives.

M01 explicite l'incertitude d'inscription ; M02/M03 retirent l'invitation à
utiliser un bon indisponible et proposent « Bon annulé » pour REVOQUE ; M04
préserve les conditions de participation ; M06 explique le retour existant
après QR invalide sans inscription. Ce sont des précisions de conception à
confronter aux états réels. M05/M07 assurent la transparence des illustrations
et M08 conserve les capacités existantes ; ils ne créent pas de nouvelles APIs.

L'adoption des orientations **ne valide pas au pixel près les 14 planches**
et ne remplace pas implicitement les maquettes obligatoires du 17 novembre.
Les correctifs du 18 novembre priment sur leurs anciennes mentions : en-tête
et outils conservés, retrait de « Garder pour plus tard », absence des filtres
internes du carnet, statut d'animation distinct du résultat personnel et lecture
bornée. Toute divergence visuelle effective devra être identifiée à la
spécification ; seules les parties qui en dépendent nécessitent un arbitrage.

Les identifiants A1–F1 sont locaux à **Live** : ne pas leur appliquer les décisions
du workshop **Animation**, suivi dans E73-WA, ni celles de **Pro**, suivi dans E80.

## Ordre de préparation initial et suite réalisée

1. WL-L0 : rapprocher la version à traiter, les preuves E73 et les données de
   test autorisées ; constater les écarts, notamment B1/C1/E1/F1.
2. WL-L1 : préparer D1 et les corrections P1 réellement reproduites ; la mesure
   QW-3 du contraste peut avancer indépendamment. QW-2 est un sous-ensemble de D1.
3. WL-L2 : préparer A1 et F1 en P2, avec QW-1 inclus dans A1.
4. WL-L3 : recette transversale et essais habitants ; publier résultats et limites
   séparément des votes et des contrôles de maquettes.

Cet ordre a été suivi pour la spécification, les corrections et la recette
automatisée. Les résultats et les limites humaines sont actualisés dans le
tableau de suivi en tête de ce rapport. Aucun accès personnel réel, envoi,
retrait de lot, génération de données d'environnement ou déploiement n'a été
effectué. Les commits et push ensuite demandés sont suivis dans le bilan WL.

## Vérifications du cadrage initial

- `py -3 scripts/check_guidance.py` : succès, 108 guides, 1 577 liens locaux,
  zéro erreur et avertissement.
- Contrôle étendu avec `--document` sur backlog E73, audit, registre utilisateur,
  backlog du workshop, synthèses roadmap et index d'audits : succès,
  115 guides, 1 974 liens, zéro erreur et avertissement. Un ancien lien relatif
  du backlog UX vers les principes Live a été corrigé après son échec initial.
- `py -3 scripts/sync_documentation.py --check-sources` : succès, 151 documents
  vérifiés ; aucun contrat exporté modifié.
- `git diff --check` : succès. Le lanceur `python` était indisponible ; les
  contrôles ont été exécutés avec le lanceur Python Windows `py -3`.
- Revue indépendante sur extraits transmis, sans accès direct aux fichiers :
  recouvrements LM, portée conditionnelle et nomenclature métier contrôlés.
  L'adoption utilisateur reçue ensuite remplace l'attente décrite dans les
  extraits initiaux. D1 vise Découvrir, LM-06 le parcours personnel : aucun
  conflit entre ces deux priorités n'est établi.

Lors du cadrage initial, seul `localeo-projet` avait été modifié. Le dossier du workshop était déjà non suivi
par Git au début de l'intervention ; ses livrables sont préservés. Les applications,
tests métier et recettes habitantes n'ont pas été exécutés par ce cadrage.
