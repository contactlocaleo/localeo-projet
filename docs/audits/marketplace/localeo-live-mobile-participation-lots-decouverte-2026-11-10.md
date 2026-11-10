# Localeo Live — participation, lots et découverte sur mobile

Audit et corrections du **10 novembre 2026**, en complément de
[la première passe sur les retours et chargements](localeo-live-parcours-stabilite-2026-11-10.md).
Demande : prolonger l’expérience du carnet dans la participation, harmoniser les
chargements et rendre Mes lots et Découvrir plus directs. Précision de conception :
reprendre les tailles de police et les sections de Localeo Pro.

## Méthode et périmètre

Sources Marketplace à partir de `46ea8dc`, documentation à partir de `fc24724`,
puis corrections locales. Analyse des parcours et du code, Chromium sur build
isolé, API simulées avec attente, erreur ou refus, accès synthétiques distincts.
Largeurs principales 320 × 568 et 390 × 844 ; texte agrandi, clavier et historique
du navigateur. Les captures sont des preuves locales : la version déployée TEST
et son SHA ne sont pas attestés ici. Aucune donnée personnelle réelle utilisée.

Références : [E73](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md),
notamment CN-02/04/05/06/14/15/16/17, CB01/05/06/07, et
[LIVE-UX-01 à 09](../../produit/live/principes-ux.md).

## Constats et réponses

| Priorité | Friction observée dans les sources et les scénarios | Réponse locale |
| --- | --- | --- |
| P1 | Participation : résumé, raccourci commerces et historique repoussaient le QR ; plusieurs lectures affichaient provisoirement « QR indisponible ». | Statut et tampons, puis action QR du passeport ou de la tombola. Vérification neutre ; action bloquée jusqu’à confirmation. Gain et résultat précèdent l’historique et les commerces. |
| P1 | Des écrans chargeaient avec un texte seul ou un faux état vide. La facture annonçait notamment un coffret absent avant lecture locale. | Ossature statique commune, titre/retour disponibles, distinction attente/erreur/vide. Le statut de commande garde son formulaire. |
| P1 | Mes lots publiait les bons locaux avant les lots distants et présentait la liste comme fraîche après un échec. | Première composition après lecture, cartes conservées pendant actualisation, « Dernier état connu » explicite. |
| P1 | Le bon disparaissait à chaque actualisation. Des droits du détail coffret restaient visibles pendant une relecture. | Descriptif conservé ; QR, code secours et PIN suspendus pendant la vérification. Refus confirmé : retrait du contenu concerné. |
| P1 | Retour depuis un lot : historique refermé, pagination et carte consultée perdus. | Relecture bornée des pages déjà consultées, historique, carte et focus retrouvés. Une interaction pendant l’attente garde la main ; lot disparu annoncé. |
| P1 | Découvrir publiait les communes/périodes séparément ; un raccourci pouvait s’insérer au-dessus d’une carte utilisable. | Composition initiale groupée, puis conservation du programme pendant les actualisations. Réponses asymétriques testées. |
| P2 | Recherche dans le menu ; favoris invisibles avant le premier ajout ; pictogrammes seuls sur les cartes. | « Rechercher » et « Pour plus tard » toujours accessibles ; boutons « Garder » / « Gardée » et « Partager ». Aucun favori ne vaut inscription. |
| P2 | Gros compteurs et introduction redondante repoussaient les gains. | Compteurs compacts, cartes blanches, action de retrait explicite. État vide : Découvrir les animations, récupération secondaire. |
| P2 | Tailles et sections hétérogènes entre Pro, carnet, découverte et participation. | Police système, corps/actions 14 px, titres 25/18/15 px (H1 mobile 23 px), sections de 12 px et actions de 9 px. Tampons, tickets et tranche de carnet conservés. |

## Parcours proposés et mis en œuvre

- **Mon carnet → Voir ma participation** : retour vers son origine, nom,
  progression réelle, action autorisée puis informations secondaires. Une
  relecture ne célèbre pas une ancienne réussite et ne présente pas un ancien QR.
- **Participation → Mes lots → retour** : contexte de participation conservé.
  Un lot déjà retiré rejoint son historique autoritatif ; le libellé de retour
  correspond à la destination.
- **Mes lots → détail → retour** : accès exact, consignes, état et retour vers
  la carte consultée. Au plus cinq pages par source sont reconstruites, avec
  arrêt sur échec ; aucune réponse, aucun token ni curseur privé dans l’état de
  navigation. La suite reste manuelle. La reconstruction concerne les cartes de
  lots ; les liens vers les tirages conservent leur contexte d’URL existant.
- **Découvrir → garder / rechercher / ouvrir** : choix public sans inscription
  implicite, retour à la recherche accessible au clavier, favoris vides utilisables,
  programme initial cohérent malgré des réponses décalées.

## Couverture des chargements

| Surface | Traitement |
| --- | --- |
| Ouverture du module Live, Mon carnet | Ossature commune et shell stable ; données conservées à l’actualisation. |
| Participation, fiche animation et QR | Titre/retour, attente neutre, prochaine action protégée ; lieu courant revérifié et illustration avec place réservée. |
| Mes lots, lot sélectionné, bon personnel | Ossature initiale, retour reconstruit, descriptif conservé et accès sensible revérifié. |
| Découvrir | Ossature par période, première publication groupée, programme conservé à l’actualisation. |
| Messages, communes, commerces et fiche commerce | Ossature dans les zones de lecture ; résultats vides seulement après réponse. |
| Coffrets, ajout coffret/participation, facture | Attente distincte d’un accès absent ; aucun QR/code conservé comme utilisable pendant une vérification. |
| Inscription, récupération carnet, confirmation tombola | Ossature initiale ; erreur de règlement avec reprise ; formulaire conservé pendant commande. |
| Réglages, fil local, juridique Live | Préférences en attente ; dernières nouvelles et documents conservés lors des relectures ; fallback JavaScript juridique propre à Live. |
| Reprise via fichier et restauration locale | Pas de lecture initiale distante à simuler ; formulaire immédiat et commande explicite existante. |

Les emplacements des retours d’actualisation réservent une ligne. Les erreurs
nécessitant plusieurs lignes restent visibles et peuvent modifier la hauteur :
la stabilité ne masque pas un refus ou une information nécessaire.

## Preuves et limites

Vérifications exécutées avec `node node_modules/@playwright/test/cli.js test
--config=playwright.desktop.config.cjs`, deux workers isolés et builds de
production sans configuration distante :

- **Dernier build : 16/16 réussis** dans `live-audit-discovery`, `live-mobile-ux`,
  le cas clavier LH-12 de `live-hierarchy-fluidity` et la lecture initiale FD-12
  de `live-public-detail-fd`. Première action publique et premier lot nominal
  visibles au-dessus de la navigation à 320 × 568 et 390 × 844, police calculée,
  cibles 44 px, réponse asymétrique, favoris, QR du bon suspendu puis refusé.
- **Parcours adjacents réussis** dans le passage principal : 9 scénarios de
  participation, 9 de continuité des lots, 10 de pages annexes, 14 de stabilité
  et 12 de protection QR. La continuité des lots a aussi été rejouée après la
  réorganisation des cartes. Les scénarios existants des lots unifiés couvrent
  les trois natures, les pages supplémentaires, les accès exacts et le renouvellement.
- **Fluidité publique** : actualisation sans déplacement, annulation d’une
  ancienne commune, pagination et retour froid de fiche vérifiés dans
  `live-hierarchy-fluidity`. FD-10/12 confirme la conservation de la fiche et du
  focus après relecture échouée, sans action d’inscription périmée.
- `npm run test:security` : **239/239**, aucun skip ; métadonnées des retours
  et lots bornées et filtrées. ESLint sur `src` et tous les tests modifiés :
  **succès**, puis contrôle ciblé des derniers changements : **succès**.
  `git diff --check` : **succès** dans les deux dépôts.
- `py -3.14 -X utf8 scripts/check_guidance.py` : **97 guides, 1 169 liens,
  aucun écart** ; `scripts/sync_documentation.py --check-sources` :
  **148 documents vérifiés**.

Les échecs intermédiaires ont été traités sans affaiblir les assertions : la
première action de Découvrir était encore masquée à 320 px, et Échap rendait le
focus au nouveau raccourci même après ouverture depuis le menu. Les deux cas
passent sur le dernier build. Deux GET protégés du coffret ont été explicitement
simulés pour compléter la fixture isolée. Le cas de synchronisation après 50
accès révoqués, initialement interrompu par le délai du test, réussit au rejeu
sans modification de sa logique ni de ses assertions.

Captures de travail non versionnées : `localeo-marketplace/tmp/live-mobile-ux-complete/`
(dernière découverte, lots, fiche, commerces et favoris),
`tmp/live-mobile-ux-final/` (participations, chargements, retours) et
`tmp/live-mobile-ux-verified/` (revalidation et pagination). Examen visuel effectué
sur la participation, les lots, Découvrir et la fiche publique à 320 px.

Cette recette ne mesure pas la vitesse sur téléphone physique ni la compréhension
par des habitants. Le temps réseau n’est pas supprimé ; un programme lent peut
retarder la première composition, mais ne réordonne plus ses premières cartes.

## Axes complémentaires à valider

1. **Recette habitant sur téléphone réel** : vérifier qu’une personne retrouve
   sa participation, son lot et la recherche sans explication ; observer les
   hésitations avant d’ajouter de nouveaux éléments.
2. **Lisibilité d’un carnet très rempli** : contrôler après livraison les retours
   au-delà de cinq pages et la compréhension de la suite manuelle. La limite
   évite une lecture exhaustive implicite et reste signalée.
3. **Consignes de remise** : améliorer les contenus saisis par les organisateurs
   lorsqu’adresse, échéance ou responsable manquent. L’interface ne les invente pas.
4. **Évolutions produit distinctes** : filtres métier supplémentaires des lots,
   recommandations personnalisées, rappels automatiques et nouvelles récompenses
   demandent une spécification. L’interactivité recherchée ici vient de commandes
   visibles et prévisibles, pas d’effets décoratifs supplémentaires.

## Impacts et livraison

Marketplace/Live et documentation canonique modifiés. Pro sert de référence
visuelle ; son code ne change pas. Backend et Animation inchangés. Aucun contrat
API, règle de qualification, commande métier, migration ou jeu de démonstration
modifié ; les fixtures restent synthétiques. Aucun flag ni opération de données
requis. Les principes UX et la convention d’identité documentent la nouvelle
référence visuelle sans modifier le statut de l’epic.

Correctifs locaux : livraison frontend puis recette TEST nécessaires.
