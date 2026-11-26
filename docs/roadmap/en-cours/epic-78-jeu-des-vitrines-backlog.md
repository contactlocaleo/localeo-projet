# EPIC 78 — Le jeu des vitrines

## Références et état

- **État produit : En cours**, cadrage du **6 novembre 2026**, selon la
  [roadmap commune](../README.md).
- [Spécification détaillée](../../specifications/epic-78-jeu-des-vitrines/README.md)
  du **15 novembre 2026**, décisions utilisateur intégrées ; six US et seize
  critères conservés. Aucun changement d'état produit par la seule spécification.
- Identifiant `78` vérifié dans la roadmap, ses namespaces applicatifs et les
  noms de fichiers des quatre dépôts applicatifs ; aucun cadrage de ce jeu trouvé.
- Demande : valoriser les vitrines, notamment à **Noël et à Pâques**, en faisant
  chercher aux habitants **un intrus dans la vitrine** des commerces participants.
- Socles à réutiliser : [moteur E55](../../specifications/epic-55-moteur-animation/README.md),
  [participation commerçante E56](../../specifications/epic-56-validation-participation-commercants-animation/README.md),
  [Live E42](../../specifications/epic-42-localeo-live/README.md),
  [Animation E73](../../specifications/epic-73-animation-et-ou-coffrets/README.md).
- Jeux proches : [mots croisés E75](../a-faire/epic-75-mots-croises-assistes-ia-backlog.md)
  et [Juste Prix E77](../en-cours/epic-77-juste-prix-local-backlog.md). Ici, le support du
  défi est **la vitrine réelle**, et la réponse identifie un intrus ; les règles
  de ces autres jeux ne sont pas transférées implicitement.
- Implémentation engagée le **16 novembre 2026** dans les cinq dépôts ; migration
  additive `v323` avec modèle inactif. [Bilan et preuves](../../specifications/epic-78-jeu-des-vitrines/bilan-realisation.md).
  Les constats de la phase de spécification restent datés du 15 novembre.

## Évolution du 17 novembre 2026 — préparation guidée

**E78-EVO-PREPARATION-UX**, demandée pour clarifier la préparation dans Pro et
les contrôles restants/en attente dans Animation. Extension UX de DEC-05,
avec réemploi des kits E55/E56 et du produit E77 dans la section Pro.
Les huit critères ajoutés **PU-01 à PU-08** et leurs impacts sont décrits dans
les [parcours canoniques](../../specifications/epic-78-jeu-des-vitrines/parcours-regles.md#évolution-du-17-novembre-2026--préparation-guidée).
Les CA-01 à CA-16, décisions métier, statut En cours et réserves d’activation
restent inchangés. Implémentation et preuves propres à cette évolution dans le
[bilan](../../specifications/epic-78-jeu-des-vitrines/bilan-realisation.md).

## Problème, acteurs et résultat attendu

Les décorations saisonnières peuvent devenir un parcours ludique de découverte
des commerces. L'habitant observe une vitrine, repère l'objet qui n'a rien à y
faire, indique sa réponse dans Localeo Live et suit sa progression.

**Acteurs :** habitant sur Live mobile ; commerçant dans Pro pour préparer et
suivre sa vitrine selon le parcours retenu ; gestionnaire dans Animation pour
organiser, contrôler et publier ; opérateur ERP pour le support autorisé.

**Exemple illustratif :** un ustensile de cuisine est glissé parmi les décorations
d'une vitrine de Noël. L'habitant doit identifier cet objet. Le thème, l'objet,
le nombre de commerces et les conditions de gain de cet exemple ne constituent
pas une configuration imposée.

Le résultat recherché est une balade simple et conviviale, avec une consigne
courte, des commerces faciles à trouver et un carnet de défis lisible.

## Décisions et trace du cadrage

| Référence | Nature | Contenu |
| --- | --- | --- |
| E78-DEC-01 | Demande utilisateur | Nouveau jeu « Le jeu des vitrines » : trouver un intrus dans les vitrines participantes |
| E78-DEC-02 | Demande utilisateur | Noël et Pâques sont des occasions privilégiées ; le jeu doit rester utilisable pour d'autres thèmes et périodes |
| E78-DEC-03 | Réponse utilisateur du 15 novembre, ARB-01/05 | QCM, un intrus par commerce, une seule réponse confirmée ; réussite/échec immédiat et solution après clôture ; sélection modifiable avant confirmation |
| E78-DEC-04 | Réponse utilisateur du 15 novembre, ARB-02/04 | « même condition que pour le just prix local » : seuil K fixé par l'organisateur, choix explicite avec/sans passages requis ; intersection bonne réponse/passage du même commerce si requis, dans les deux ordres pendant le jeu ; une chance au tirage existant |
| E78-DEC-05 | Réponse utilisateur du 15 novembre, ARB-03 | Le commerçant prépare dans Pro, puis l'organisateur approuve et contrôle sur le terrain ; installation attestée et contrôle liés à la version exacte |
| E78-DEC-06 | Réponse utilisateur du 15 novembre, ARB-06 | Suspendre l'édition ; reprendre à l'identique si le dispositif peut être rétabli, sinon annuler et créer une nouvelle édition |
| E78-DEC-07 | Réponse utilisateur du 15 novembre, ARB-07 | Inclus dans le forfait standard organisateur, avec les dotations existantes ; aucun tarif ou quota propre à E78 |
| E78-PROP-01 | Proposition initiale résolue par DEC-03 | Un défi et un intrus par commerce, choix puis confirmation définitive |
| E78-PROP-02 | Proposition initiale complétée par DEC-04 | Seuil puis tirage, avec les deux modes de passage du Juste Prix local ; aucun gain automatique ni chance supplémentaire par réponse |
| E78-PROP-03 | Proposition initiale résolue par DEC-05 | Proposition dans Pro puis approbation organisatrice |
| E78-PROP-04 | Conception UX détaillée dans la spécification | Une carte de défi par vitrine, progression confirmée et états accessibles ; accès aux profils/adresses des commerces |

Les propositions initiales restent identifiables pour la traçabilité. Les décisions
du 15 novembre les remplacent pour les points concernés. La reprise de la
qualification E77 ne reprend ni son prix ni sa tolérance ; ses
[conditions de passage et de seuil](../../specifications/epic-77-juste-prix-local/parcours-regles.md#réussite-passages-et-qualification--ca-09-à-13)
sont explicitées dans les parcours E78.

## Périmètre

### Inclus

- Type de jeu et assistant de préparation identifiables dans Localeo Animation.
- Thème, dates, commerces et vitrines retenus, consigne de recherche, intrus et
  règle de réponse ; contrôle de préparation matérielle avant ouverture.
- Préparation du contenu dans Pro et validation de sa version par l'organisateur.
  La mise en place physique de l'objet reste distincte
  de l'enregistrement de la réponse attendue dans l'application.
- Découverte dans Live, liste des commerces, adresses et informations pratiques
  disponibles, consigne courte, réponse et progression. Un lien ou QR ouvre
  Live sur l'animation ou sur le défi concerné.
- Réponse QCM définitive, correction immédiate, seuil avec/sans passages et tirage.
  Réutiliser inscription, carnet, tirage et remise existants lorsqu'ils conviennent.
- Kit commerçant imprimable : consigne de mise en place privée et support public
  d'accès au jeu distincts. La solution n'apparaît pas sur le support public.
- Suivi de préparation, participation et résultats par le gestionnaire ; reprise
  d'incident si une vitrine devient indisponible pendant le jeu.

### Contraintes de conception

- Le **domaine backend** porte la correction d'une réponse, les essais autorisés
  et l'éligibilité. Pro, Animation, ERP et Live présentent ou orchestrent ces règles.
- Le défi doit correspondre à une vitrine réellement préparée et à un intrus
  identifiable sans ambiguïté. Installation commerçante et contrôle organisateur
  portent sur la version exacte ; un QR ne prouve pas à lui seul un passage.
- Les solutions et marquages de bonne réponse restent privés jusqu'au moment
  de révélation autorisé ; pas de réponse correcte cachée dans le HTML/JSON public.
- Les contenus et règles joués sont versionnés à la publication ; pas de
  remplacement silencieux de l'intrus ou de correction rétroactive des réponses.
- Respect des périodes de jeu et droits existants. La visibilité d'une fiche
  avant ouverture ne donne pas le droit d'y répondre avant le début.
- Conserver la participation et la progression après rechargement ou reprise.
  Doubles clics et reprises réseau ne créent pas d'essais ou de chances supplémentaires.
- UX mobile : actions explicites, grands contrôles accessibles, consigne brève,
  progression graphique, états avec texte et pictogramme, sans dépendre d'une
  couleur seule. Utiliser les visuels réellement fournis ; ne pas inventer de
  photo de vitrine ni publier une photo dévoilant involontairement la solution.
- Recherche, listes et bilans bornés côté serveur ; budgets et preuves à prévoir
  selon la [convention de performance](../../architecture/transverse/performance-volumetrie.md).

### Hors périmètre initial

- Analyse automatique de photos ou reconnaissance de l'intrus par IA ; réalité
  augmentée, géolocalisation obligatoire ou achat de matériel dédié.
- Concours de la plus belle vitrine, vote public ou classement des commerçants.
- Refonte des autres jeux, de la marketplace Coffrets ou du moteur de tirage.
- Tarif, quota ou module payant repris automatiquement de la chasse ou d'E75.

## User stories

| ID | Besoin | Critères |
| --- | --- | --- |
| E78-US01 | Gestionnaire : préparer une édition saisonnière avec des étapes claires | CA-01 à 02 |
| E78-US02 | Commerçant/organisateur : préparer, contrôler et approuver chaque vitrine | CA-03 à 04 |
| E78-US03 | Habitant : découvrir les commerces et répondre simplement dans Live | CA-05 à 08 |
| E78-US04 | Habitant : retrouver sa progression et comprendre les conditions de gain | CA-09 à 11 |
| E78-US05 | Gestionnaire : suivre l'édition et traiter une vitrine indisponible | CA-12 à 13 |
| E78-US06 | Localeo : préserver confidentialité, droits, compatibilité et qualité mobile | CA-14 à 16 |

## Critères d'acceptation cibles

Les **16 critères E78-CA-01 à E78-CA-16** définissent des résultats à vérifier
lors du développement. Ils sont précisés après décisions du 15 novembre, sans
changement d'identifiant ; aucun n'est annoncé comme testé par la spécification.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E78-CA-01 | Gestionnaire habilité, modèle disponible | Créer « Le jeu des vitrines » | Brouillon de ce type avec thème, dates et préparation guidée ; aucune conversion d'une autre animation |
| E78-CA-02 | Brouillon avec commerces retenus | Préparer la publication | Règles de réponse et gain explicites, contenus complets ; préparation manquante ou règle inatteignable bloque la publication avec prochaine action compréhensible |
| E78-CA-03 | Commerçant principal accepté dans Pro | Enregistrer un intrus et le QCM | Contenu rattaché au bon commerce, aperçu joueur distinct des consignes privées ; salarié de validation et autre périmètre refusés |
| E78-CA-04 | Organisateur, installation attestée | Approuver, contrôler sur le terrain et publier | Contenu et installation exacts approuvés/contrôlés ; modification du contenu ou de l'installation exige une nouvelle validation correspondante |
| E78-CA-05 | Habitant | Ouvrir le catalogue ou un QR/lien direct | Accès à Live sur la bonne édition/vitrine ; commerces, adresses disponibles et consigne faciles à trouver ; pas de renvoi vers la surface animations de la marketplace |
| E78-CA-06 | Animation visible avant, pendant ou après le jeu | Tenter de répondre | Réponse admise uniquement dans les dates et statuts autorisés ; motif et prochaine action lisibles hors période |
| E78-CA-07 | Habitant sans réponse confirmée pour cette vitrine | Sélectionner puis confirmer un choix du QCM | Une seule réponse définitive, correcte ou incorrecte ; correction serveur selon la version publiée, résultat immédiat sans corrigé général avant clôture |
| E78-CA-08 | Réponse déjà traitée ou réseau interrompu | Réessayer la commande ou répondre de nouveau | Rejeu retrouve le résultat ; aucun essai/chance supplémentaire ni écrasement de réponse définitive, même avec une autre clé |
| E78-CA-09 | Participant reprenant son carnet | Revenir dans Live ou actualiser | Réponse, réussite/échec et progression conservés ; passage manquant distinct d'un échec, solution après clôture effective, sans nouveau compte ni doublon |
| E78-CA-10 | Participant, seuil K et mode de passage publiés | Atteindre la condition d'éligibilité | Comme E77 : K commerces correctement résolus, avec passage du même commerce si requis, dans les deux ordres avant fermeture ; une seule chance, seuil et mode expliqués avant de jouer |
| E78-CA-11 | Animation clôturée avec participants qualifiés | Effectuer le tirage existant | Population qualifiée figée, une participation par habitant selon les règles existantes ; gains, lots et remise retrouvés dans Live, aucun gain implicite à la réponse |
| E78-CA-12 | Gestionnaire autorisé | Consulter préparation et bilan | Vitrines à préparer, réponses et participants qualifiés lisibles ; listes paginées et compteurs agrégés, pas de solutions dans les vues publiques |
| E78-CA-13 | Objet absent, commerce fermé ou erreur après publication | Déclarer l'incident | Suspension tracée, reprise à définition identique après contrôle ou annulation puis nouvelle édition ; information des participants, aucun retrait/neutralisation ni transfert des faits |
| E78-CA-14 | Habitant ou commerce non autorisé, requête manipulée | Chercher la solution ou modifier un contenu/résultat | Refus serveur ; solutions absentes des projections/QR publics avant révélation, droits limités au périmètre, aucune correction exclusivement frontend |
| E78-CA-15 | Habitant sur petit écran ou utilisateur de clavier/lecteur d'écran | Parcourir commerces, répondre et reprendre | Consigne/action/progression accessibles, états compréhensibles sans couleur seule, absence de débordement horizontal et aucun visuel inventé |
| E78-CA-16 | Implémentation et jeux synthétiques futurs | Exécuter preuves domaine, intégration, contrats et parcours | Correction, essais/reprise/concurrence, périodes, confidentialité, droits, gain, incidents et non-régression des autres jeux vérifiés ; pagination et capacité mesurées, échecs/non-exécutés distincts des succès |

## Impacts spécifiés

| Sujet | Conception du 15 novembre ; réalisation future |
| --- | --- |
| Domaine backend | **Concerné** : moteur E78, QCM pur, réponse unique, qualification avec/sans passage, préparation versionnée et publication ; aucune progression linéaire de chasse |
| Animation et ERP | **Concernés** : préparation guidée, contrôle/approbation, publication, incidents, supervision et bilan |
| Pro | **Concerné** : proposition/installation par le principal, kit et validation de passage si requise ; droits principal/salarié distincts et périmètre Animation seul |
| Marketplace/Live | **Concerné pour Live** : carte de défi, accès aux commerces, réponse et carnet mobile ; marketplace Coffrets conservée, liens animations vers Live |
| API et consommateurs | **Concernés** : configuration, commandes/projections privées/publiques, compatibilité et erreurs ; contrats canoniques documentés ici, générateurs et contrats embarqués dans leurs dépôts propriétaires |
| Persistance, migrations, données existantes | **Concernées** : propositions/approbations, installation/contrôle, réponse, résultat, version et unicités, progression et clôture ; migration additive, aucune conversion des autres jeux ni numéro SQL réservé |
| Générateur de démonstration et fixtures | **Concernés** : Noël/Pâques, vitrines prêtes/incomplètes, réponses, deux modes de passage, reprise/incident, droits, qualification et tirage |
| Documentation fonctionnelle | **Concernée** : guides gestionnaire/Pro/Live, consignes publiques, kit privé et règlement ; sources communes sans copie concurrente |
| Exploitation et déploiement | **Concernés** : inclusion standard, activation après livraison coordonnée, conservation des réponses liée à la participation, reprise de clôture/incidents et diagnostics sans solutions |
| Volumétrie et coûts | **Concernés** : bornes et budgets chiffrés dans la spécification ; mesures N/10N et charge mixte à produire avant activation |

## Arbitrages résolus le 15 novembre 2026

| Référence conservée | Décision | Dépendances couvertes |
| --- | --- | --- |
| E78-ARB-01 | DEC-03 : un intrus et un QCM par commerce, une réponse définitive confirmée | Saisie, correction, accessibilité, confidentialité et persistance |
| E78-ARB-02 | DEC-04 : seuil réglable puis tirage existant, une chance comme E77 | Qualification, dotation et parcours de gain |
| E78-ARB-03 | DEC-05 : commerçant dans Pro, approbation et contrôle terrain organisateur | Droits, préparation, publication et kit |
| E78-ARB-04 | DEC-04 : mode avec/sans passage choisi explicitement ; mêmes conditions E77 | Validation Pro/PIN, qualification et parcours terrain |
| E78-ARB-05 | DEC-03 : réussite/échec immédiat, solution après clôture effective | États Live, réponse API et règlement |
| E78-ARB-06 | DEC-06 : suspension, reprise identique si rétabli, sinon annulation et nouvelle édition | Équité, support et version publiée |
| E78-ARB-07 | DEC-07 : forfait standard et dotations existantes, aucun tarif/quota E78 propre | Catalogue, droits et activation |

## Passage à l'implémentation

Les sept arbitrages produit sont résolus. Les 16 critères sont reliés aux règles,
contrats, migrations, documentation, fixtures et preuves dans la
[matrice de vérification](../../specifications/epic-78-jeu-des-vitrines/verification-livraison.md).
La spécification distingue quatre lots dépendants selon le
[cycle d'epic](../../organisation/cycle-epic.md). Les tests futurs constituent
les preuves attendues ; ni un pilote ni une approbation externe ne deviennent
une condition de clôture implicite. L’état est **En cours** depuis la demande
d’implémentation du 16 novembre ; clôture, commit, push et activation restent distincts.
