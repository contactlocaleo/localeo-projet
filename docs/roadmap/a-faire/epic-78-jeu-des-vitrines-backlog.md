# EPIC 78 — Le jeu des vitrines

## Références et état

- **État produit : À faire**, cadrage du **6 novembre 2026**, selon la
  [roadmap commune](../README.md).
- Identifiant `78` vérifié dans la roadmap, ses namespaces applicatifs et les
  noms de fichiers des quatre dépôts applicatifs ; aucun cadrage de ce jeu trouvé.
- Demande : valoriser les vitrines, notamment à **Noël et à Pâques**, en faisant
  chercher aux habitants **un intrus dans la vitrine** des commerces participants.
- Socles à réutiliser : [moteur E55](../../specifications/moteur-animation/README.md),
  [participation commerçante E56](../../specifications/epic-56-validation-participation-commercants-animation/README.md),
  [Live E42](../../specifications/epic-42-localeo-live/README.md),
  [Animation E73](../../specifications/epic-73-animation-et-ou-coffrets/README.md).
- Jeux proches : [mots croisés E75](epic-75-mots-croises-assistes-ia-backlog.md)
  et [Juste Prix E77](epic-77-juste-prix-local-backlog.md). Ici, le support du
  défi est **la vitrine réelle**, et la réponse identifie un intrus ; les règles
  de ces autres jeux ne sont pas transférées implicitement.
- Cadrage uniquement : pas de spécification détaillée, modèle enregistré,
  migration réservée, implémentation ou preuve de test métier E78 à ce stade.

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

## Décisions, propositions et questions

| Référence | Nature | Contenu |
| --- | --- | --- |
| E78-DEC-01 | Demande utilisateur | Nouveau jeu « Le jeu des vitrines » : trouver un intrus dans les vitrines participantes |
| E78-DEC-02 | Demande utilisateur | Noël et Pâques sont des occasions privilégiées ; le jeu doit rester utilisable pour d'autres thèmes et périodes |
| E78-PROP-01 | Proposition à confirmer, ARB-01 | Un défi et un intrus par commerce pour l'édition ; réponse par choix parmi plusieurs objets, puis confirmation définitive, modifiable avant confirmation |
| E78-PROP-02 | Proposition à confirmer, ARB-02 | Seuil de vitrines correctement résolues fixé par le gestionnaire, ouvrant l'accès au tirage existant ; aucun gain automatique ni chance supplémentaire par réponse |
| E78-PROP-03 | Proposition à confirmer, ARB-03 | Le commerçant propose l'intrus, la consigne et les réponses dans Pro ; l'organisateur approuve avant publication |
| E78-PROP-04 | Proposition UX | Une carte de défi par vitrine, progression visuelle et états « à découvrir / répondu / résolu » adaptés à la règle retenue ; accès direct aux profils et adresses des commerces |

Les propositions servent de base de travail et restent distinctes des décisions
acquises. Les réponses demandées à l'utilisateur sont consignées ici lorsqu'elles
sont reçues ; l'absence de réponse ne constitue pas une validation.

## Périmètre

### Inclus

- Type de jeu et assistant de préparation identifiables dans Localeo Animation.
- Thème, dates, commerces et vitrines retenus, consigne de recherche, intrus et
  règle de réponse ; contrôle de préparation matérielle avant ouverture.
- Préparation du contenu et validation de sa version, avec responsabilités
  explicites selon ARB-03. La mise en place physique de l'objet reste distincte
  de l'enregistrement de la réponse attendue dans l'application.
- Découverte dans Live, liste des commerces, adresses et informations pratiques
  disponibles, consigne courte, réponse et progression. Un lien ou QR ouvre
  Live sur l'animation ou sur le défi concerné.
- Règle d'essais, correction, qualification et gains selon les arbitrages retenus.
  Réutiliser inscription, carnet, tirage et remise existants lorsqu'ils conviennent.
- Kit commerçant imprimable : consigne de mise en place privée et support public
  d'accès au jeu distincts. La solution n'apparaît pas sur le support public.
- Suivi de préparation, participation et résultats par le gestionnaire ; reprise
  d'incident si une vitrine devient indisponible pendant le jeu.

### Contraintes de conception

- Le **domaine backend** porte la correction d'une réponse, les essais autorisés
  et l'éligibilité. Pro, Animation, ERP et Live présentent ou orchestrent ces règles.
- Le défi doit correspondre à une vitrine réellement préparée et à un intrus
  identifiable sans ambiguïté. La préparation matérielle et son contrôle restent
  à définir ; un QR ne prouve pas à lui seul l'observation ou un passage.
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
lors du développement. Les branches liées à un arbitrage restent conditionnelles ;
aucun de ces critères n'est annoncé comme testé par ce cadrage.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E78-CA-01 | Gestionnaire habilité, modèle disponible | Créer « Le jeu des vitrines » | Brouillon de ce type avec thème, dates et préparation guidée ; aucune conversion d'une autre animation |
| E78-CA-02 | Brouillon avec commerces retenus | Préparer la publication | Règles de réponse et gain explicites, contenus complets ; préparation manquante ou règle inatteignable bloque la publication avec prochaine action compréhensible |
| E78-CA-03 | Préparateur autorisé selon ARB-03 | Enregistrer un intrus et la réponse attendue | Contenu rattaché au bon commerce, aperçu joueur distinct des consignes privées ; modification d'un autre périmètre refusée |
| E78-CA-04 | Organisateur, vitrines préparées | Approuver et publier | Version de contenu approuvée et préparation matérielle contrôlée selon la procédure retenue ; changement après approbation exige une nouvelle validation |
| E78-CA-05 | Habitant | Ouvrir le catalogue ou un QR/lien direct | Accès à Live sur la bonne édition/vitrine ; commerces, adresses disponibles et consigne faciles à trouver ; pas de renvoi vers la surface animations de la marketplace |
| E78-CA-06 | Animation visible avant, pendant ou après le jeu | Tenter de répondre | Réponse admise uniquement dans les dates et statuts autorisés ; motif et prochaine action lisibles hors période |
| E78-CA-07 | Habitant avec droit de réponse selon ARB-01 | Préparer puis soumettre sa réponse | Saisie conforme au format retenu et engagement explicite si réponse définitive ; correction serveur selon la version publiée, sans fuite de solution |
| E78-CA-08 | Réponse déjà traitée ou réseau interrompu | Réessayer la commande ou dépasser les essais autorisés | Rejeu retrouve le résultat ; aucun essai/chance supplémentaire ni écrasement de réponse définitive si ce mode est retenu |
| E78-CA-09 | Participant reprenant son carnet | Revenir dans Live ou actualiser | Progression par vitrine et prochaine action conservées ; retour réussite/échec conforme à ARB-05, sans nouveau compte ni doublon |
| E78-CA-10 | Participant répondant aux règles ARB-02/04 | Atteindre la condition d'éligibilité | Qualification serveur selon la règle publiée ; ni simple QR ni mauvaise réponse ne suffisent ; seuil et éventuelle preuve de passage expliqués avant de jouer |
| E78-CA-11 | Animation clôturée avec participants qualifiés | Effectuer le tirage si cette option est retenue | Population qualifiée figée, une participation par habitant selon les règles existantes ; gains, lots et remise retrouvés dans Live, aucun gain implicite à la réponse |
| E78-CA-12 | Gestionnaire autorisé | Consulter préparation et bilan | Vitrines à préparer, réponses et participants qualifiés lisibles ; listes paginées et compteurs agrégés, pas de solutions dans les vues publiques |
| E78-CA-13 | Objet absent, commerce fermé ou erreur après publication | Déclarer l'incident | Traitement tracé selon ARB-06, information des participants ; aucune modification silencieuse du défi ou qualification rétroactive arbitraire |
| E78-CA-14 | Habitant ou commerce non autorisé, requête manipulée | Chercher la solution ou modifier un contenu/résultat | Refus serveur ; solutions absentes des projections/QR publics avant révélation, droits limités au périmètre, aucune correction exclusivement frontend |
| E78-CA-15 | Habitant sur petit écran ou utilisateur de clavier/lecteur d'écran | Parcourir commerces, répondre et reprendre | Consigne/action/progression accessibles, états compréhensibles sans couleur seule, absence de débordement horizontal et aucun visuel inventé |
| E78-CA-16 | Implémentation et jeux synthétiques futurs | Exécuter preuves domaine, intégration, contrats et parcours | Correction, essais/reprise/concurrence, périodes, confidentialité, droits, gain, incidents et non-régression des autres jeux vérifiés ; pagination et capacité mesurées, échecs/non-exécutés distincts des succès |

## Impacts à instruire

| Sujet | Analyse initiale |
| --- | --- |
| Domaine backend | **Concerné** : modèle de défi de vitrine, correction, essais, qualification et publication ; réutilisation des mécanismes QCM/mot de la chasse à examiner sans hériter de son parcours linéaire |
| Animation et ERP | **Concernés** : préparation guidée, contrôle/approbation, publication, incidents, supervision et bilan |
| Pro | **À préciser selon ARB-03/04** : proposition du contenu, kit de mise en place et éventuelle validation de passage ; préserver droits principal/salarié et Animation seul |
| Marketplace/Live | **Concerné pour Live** : carte de défi, accès aux commerces, réponse et carnet mobile ; marketplace Coffrets conservée, liens animations vers Live |
| API et consommateurs | **Concernés** : configuration, commandes/projections privées/publiques, compatibilité et erreurs ; contrats canoniques documentés ici, générateurs et contrats embarqués dans leurs dépôts propriétaires |
| Persistance, migrations, données existantes | **À examiner** : propositions/approuvés, réponse, résultat, version et unicités ; pas de migration d'autres jeux supposée ni numéro SQL réservé |
| Générateur de démonstration et fixtures | **Concernés** : Noël/Pâques, vitrines prêtes/incomplètes, réponse correcte/incorrecte, reprise et incident, droits et tirage selon arbitrages |
| Documentation fonctionnelle | **Concernée** : guides gestionnaire/Pro/Live, consignes publiques, kit privé et règlement ; sources communes sans copie concurrente |
| Exploitation et déploiement | **À examiner** : activation/offre, livraison coordonnée, conservation des réponses, reprise d'incident et diagnostics sans solutions |
| Volumétrie et coûts | **Concernés** : réponses/rejeux, médias réels, listes et agrégations bornées ; budgets à chiffrer puis mesures N/10N et charge mixte avant activation |

## Arbitrages ouverts

| Référence | Décision attendue / recommandation de cadrage | Dépendances |
| --- | --- | --- |
| E78-ARB-01 | Nombre de défis par commerce, format et essais : proposition d'un intrus par commerce, choix parmi plusieurs objets et une réponse définitive après confirmation ; alternative texte libre ou photo | Saisie, correction, accessibilité, confidentialité et persistance |
| E78-ARB-02 | Condition et attribution du gain : proposition de seuil de vitrines résolues réglable puis tirage existant ; alternative toutes les vitrines ou gain automatique | Qualification, dotation et parcours de gain |
| E78-ARB-03 | Qui prépare et approuve : proposition Pro commerçant puis validation organisatrice ; définir contrôle de mise en place réelle | Droits, préparation, publication et kit |
| E78-ARB-04 | Faut-il une preuve de passage en plus de la bonne réponse ? Aucun mode imposé ni paramétrabilité d'E77 reprise implicitement ; un QR public n'est pas une preuve | Validation Pro/PIN, qualification et parcours terrain |
| E78-ARB-05 | Retour immédiat ou différé, révélation de l'intrus et affichage des réussites ; proposition de résultat immédiat sans révéler la solution avant clôture | États Live, réponse API et règlement |
| E78-ARB-06 | Objet déplacé, commerce fermé ou réponse erronée : modalités de suspension/reprise, retrait et effet sur l'éligibilité ; pas de remplacement silencieux | Équité, support et version publiée |
| E78-ARB-07 | Modèle inclus ou module payant, tarif HT, durée, quota, accompagnement et modes de lots ; aucune offre d'un autre jeu transférée | Catalogue, souscription, dotation et activation |

## Passage à la spécification

Le problème et les usages permettent de poursuivre le cadrage indépendamment
des arbitrages. Résoudre chaque question avant de spécifier ou implémenter son
comportement dépendant, puis relier les 16 critères aux responsabilités, contrats,
migrations, fixtures et preuves dans le dossier canonique prévu par le
[cycle d'epic](../../organisation/cycle-epic.md). Les tests futurs constituent
les preuves attendues ; ni un pilote ni une approbation externe ne deviennent
une condition de clôture implicite.
