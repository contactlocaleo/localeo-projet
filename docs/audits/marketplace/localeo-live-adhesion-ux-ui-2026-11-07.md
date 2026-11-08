# Localeo Live — audit du parcours, de l’UX et de l’UI pour l’adhésion habitant

Date : **7 novembre 2026**. Périmètre : découverte, inscription, participation, commerçants, lots, messages et retour dans Live. Référence applicative examinée : `localeo-marketplace`, commit `e94201b`, sans modification locale au début de l’audit.

## Avis produit

**Live possède déjà les fonctions utiles ; son principal levier d’adhésion est de mieux accompagner la prochaine action et de rendre les progrès plus gratifiants.** La découverte est structurée, les participations et les récompenses sont accessibles, les messages existent. Mais les différents moments restent parfois juxtaposés : découvrir, s’inscrire, retrouver son accès, reprendre, attendre un tirage, récupérer un lot.

La direction recommandée est un **compagnon de sortie locale** : « Voilà ce qui vous attend, voilà où vous en êtes, voilà ce que vous pouvez faire maintenant. » Le plaisir vient de la clarté, des rencontres locales et d’un progrès visible, autant que de l’habillage graphique.

L’objectif de retour doit suivre le rythme réel des animations. Une utilisation fréquente pendant un parcours et une reprise naturelle à la prochaine animation sont plus pertinentes qu’une ouverture quotidienne sans contenu nouveau. La rétention dépend aussi de la qualité et de la fréquence des animations proposées par les communes ; l’interface ne peut pas compenser seule un programme vide.

## Méthode et limites

- Revue des composants, styles, règles de présentation, spécifications E42/E73/E74 et scénarios de tests existants ; seconde lecture indépendante centrée sur inscription, continuité, notifications et récompenses.
- **Pas de recette visuelle connectée sur TEST** : l’outil navigateur intégré était indisponible, puis le contrôle du navigateur Windows a arrêté l’accès faute de pouvoir déterminer l’URL courante avec assez de confiance. Cette limite concerne l’outil d’audit, pas un défaut démontré de Live.
- Les constats ci-dessous sont des observations du code actuel. La densité perçue, le plaisir, la compréhension et les effets sur l’adhésion sont des **hypothèses ergonomiques à confirmer par des essais habitants**. Aucune mesure d’abandon, de performance réelle, de contraste rendu ou de rétention n’a été produite.
- Les tests cités ont été **lus, pas rejoués**. Leurs succès historiques ne valent pas recette de la version actuellement déployée.
- Audit et recommandations uniquement : aucune fonctionnalité, règle métier, donnée, notification ou configuration distante modifiée. Les propositions ne constituent pas un périmètre approuvé ni une réouverture des epics clôturées.

## Ce qu’il faut conserver

Le code contient déjà la recherche à la demande dans le header, la géolocalisation volontaire, les communes suivies, les favoris « Pour plus tard », le partage public, les images réellement configurées sur les flyers, des compteurs de participation, des progressions graphiques, les priorités « presque terminé / derniers jours », les commerçants et leurs informations pratiques, les lots disponibles avant l’historique, les prochains tirages, les messages avec non-lus, les rappels facultatifs et les aides de récupération/installation.

La navigation basse conserve quatre entrées explicites. Les boutons de rafraîchissement partagés, les retours contextualisés, les zones tactiles souvent dimensionnées à 44–48 px et le mouvement réduit sont aussi des acquis. **Il ne faut pas refaire ces fonctions sous d’autres noms.**

## Lecture du parcours habitant

| Moment | Ce qui fonctionne dans le code | Point de friction ou occasion d’amélioration |
| --- | --- | --- |
| Première ouverture | Consultation publique ; choix manuel d’une commune ou géolocalisation. | Avant le premier contenu, les mentions « dans ce navigateur », limite de communes et choix de suivi peuvent prendre le pas sur le bénéfice concret. Montrer une promesse courte puis une seule action de départ. |
| Choix d’une animation | Visuel réel, type, dates, défi, statistiques, favoris et partage. | Beaucoup de niveaux d’information pour comparer plusieurs animations. Le vocabulaire « validations » reste fonctionnel ; l’effort et le plaisir attendus sont moins évidents. |
| Inscription | Tombola publique immédiate ; les autres parcours prévoient la continuité vers le carnet. | Pour la tombola, la réussite renvoie surtout à l’animation et décrit la suite par texte. L’accès personnel passe par l’e-mail, puis le carnet : cette continuité mérite un accompagnement visuel spécifique. |
| Retour pendant l’animation | Priorités et progression présentes. | Une participation non urgente n’est pas mise en avant comme les participations presque terminées. Le catalogue peut reprendre la place principale alors que l’habitant veut continuer. |
| Déplacement chez le commerçant | Annuaire, adresse, horaires publiés et itinéraire existent. | L’habitant doit encore relier son étape restante aux informations pratiques. Renforcer cette continuité sans dévoiler les lieux secrets d’une chasse. |
| Étape validée / qualification | Retour de succès, progression et résultat explicite. | La réussite peut être davantage ressentie : rendre le changement visible, puis proposer immédiatement la suite pertinente. |
| Message organisateur | Centre de messages, badge et filtrage existent. | L’information est davantage organisée comme une messagerie séparée que comme une aide au parcours concerné. Les différents accords de notification sont dispersés. |
| Gain, fin de jeu, prochaine visite | Lots, historique, tirage et avis existent. | Transformer le résultat en action pratique ou en souvenir positif, puis en prochain rendez-vous utile. |

## Améliorations priorisées

P1 : friction directe sur la compréhension, la continuité ou la prochaine action. P2 : plaisir et retour utile après sécurisation du socle. P3 : enrichissement à expérimenter. Les efforts sont relatifs, pas des engagements de délai.

| ID | Priorité | Proposition concrète | Pourquoi / preuve actuelle | Effort et dépendances |
| --- | --- | --- | --- | --- |
| A01 | **P1** | **Une action personnelle principale sur l’accueil**, même sans urgence : reprendre une participation disponible ; contexte de date et étape restante ; accès secondaire aux autres parcours. Lorsqu’une alerte empêche l’action, l’expliquer avant de proposer de continuer. | `useLiveDashboard` ne retient dans `priorities` que les indicateurs urgents ou presque terminés. `LiveHome` affiche jusqu’à trois priorités avant la découverte. Le raccourci vers un parcours ordinaire manque dans cette zone. [S1] | Moyen. Définir l’ordre des besoins ; une vraie « dernière activité » ou une prochaine étape autorisée peut demander une projection backend. Ne pas annoncer une personnalisation que la donnée ne permet pas. |
| A02 | **P1** | **Réussite d’inscription en deux temps explicites** : « Votre inscription est enregistrée », puis « Retrouvez votre accès personnel dans l’e-mail reçu ». Deux étapes illustrées pour ajouter au carnet, avec aide si le mail manque. | La tombola propose principalement « Retour à l’animation », suivie de paragraphes expliquant e-mail, carnet et installation. [S2] | Faible pour le guidage. La connaissance d’un e-mail ne donne jamais accès à la participation d’un tiers. Ne pas fabriquer un carnet personnel à partir de l’adresse saisie. |
| A03 | **P1** | **“Retrouver mes participations sur ce téléphone”**, avec trois choix simples : j’ai mon e-mail / je ne le retrouve plus / je change de téléphone. Exposer cette aide dans l’état vide et après une difficulté de continuité d’installation. | Carnet local, aide de récupération et sauvegarde JSON déjà présents ; l’habitant doit encore comprendre navigateur, appareil et installation. [S3] | Moyen pour orchestrer l’existant. Une récupération groupée ou synchronisation serait une évolution métier distincte. Vérification réelle iOS/Android indispensable. |
| A04 | **P1** | **Une carte de découverte plus courte** : nom, commune, repère temporel, promesse concrète, un indicateur utile, action. Déplier le reste dans la fiche. Dire « 5 commerces à visiter » uniquement si c’est réellement la règle, plutôt que « 5 validations ». | Chaque carte cumule statut, commune, titre, modèle, bouton, favoris/partage, défi, jusqu’à trois compteurs, note de dotation, dates et détails. Le premier CTA est déjà placé tôt ; c’est surtout le volume répété qui reste à réduire. [S4] | Faible à moyen. Conserver les informations réglementaires et ne pas déduire durée, distance, gratuité ou accessibilité non documentées. |
| A05 | **P1** | **Une recherche portant sur tout le catalogue concerné**, avec filtres familiers : aujourd’hui, ce week-end, en famille si ce critère est qualifié. Afficher les favoris via une entrée explicite quand ils existent. | La recherche actuelle filtre seulement les pages chargées ; « Pour plus tard » est un mode dans le panneau de recherche. L’interface l’explique, mais demande à l’habitant de comprendre la pagination. [S4] | Moyen à élevé pour recherche et filtres serveur paginés. Faible pour un accès direct aux favoris. Les attributs famille/durée nécessitent une donnée structurée avant affichage. |
| A06 | **P1** | **Messages reliés à la participation** : “Une nouvelle de l’organisateur” au bon endroit et lien déjà filtré ; état clair des accords et des alertes téléphone. | Cloche, centre de messages et non-lus présents. L’accord organisateur est dans un volet du parcours, tandis que push et rappels sont dans Réglages. [S5] | Moyen. Réutiliser les mécanismes existants ; dissocier accord de réception, permission navigateur et préférences de rappels. Une urgence opérationnelle doit rester visible même sans push. |
| A07 | **P2** | **Une microcélébration à chaque réussite utile** : étape qui se coche, progression qui avance, message bref puis prochaine action. À la qualification, montrer clairement le rendez-vous du tirage connu. | Les messages « Une étape de plus ! » et « Bravo » existent, avec progression. Il s’agit de renforcer le retour perceptible, pas d’inventer une qualification. [S6] | Faible à moyen. État confirmé par le serveur, pas de célébration d’une réponse incertaine ; mouvement réduit et absence de son automatique. |
| A08 | **P2** | **Un lot orienté retrait ou utilisation** : lieu, échéance, état, action “Présenter mon bon” ou “Voir où le retirer” selon les droits réels. | Le tri disponible/historique et les nouveautés existent. Le CTA “Voir mon lot” et certaines consignes repliées laissent encore une étape de compréhension. [S7] | Moyen. Ajouter une échéance ou un contact au contrat uniquement s’ils manquent ; conserver les états serveurs et distinguer chaque type de lot. |
| A09 | **P2** | **Un prochain rendez-vous, puis une sortie positive** : tirage prévu, nouvelles associées, préférence d’alerte appropriée ; après le résultat, bref bilan et prochaine animation pertinente de la commune. | Date, agenda, résultat et lien “Trouver mon prochain défi” existent. L’attente repose encore sur “Revenez ici”. [S8] | Moyen. Vérifier la couverture réelle des notifications de résultat avant tout nouveau canal ; pas de doublons. Les suggestions restent conditionnées à une animation publique réellement disponible. |
| A10 | **P2** | **Une identité locale et ludique plus cohérente** : motif de parcours discret, pictogramme propre au type de jeu, photo officielle lorsque disponible, une couleur d’action stable et des états visuels constants. | Le socle graphique a déjà été enrichi. La découverte reste essentiellement une succession de cartes et de compteurs ; les styles sont distribués entre shell, pages et composants. La cohérence visuelle exacte reste à vérifier sur rendu. [S9] | Moyen. Consolider les composants/tokens existants plutôt qu’empiler des surcharges CSS. Sans photo, composition typographique et pictogramme, aucune illustration de lieu inventée. |
| A11 | **P2** | **Un plan de visite lié au parcours** : depuis une étape connue, adresse, horaires publiés, itinéraire et retour à l’étape. Une vue carte peut venir ensuite si elle améliore réellement le choix. | L’annuaire vient d’être ajouté ; il faut l’intégrer au moment où l’habitant cherche où aller, pas créer un second annuaire. [S10] | Moyen. Respect des lieux cachés des chasses, des capacités serveur et de la confidentialité ; “ouvert maintenant” interdit sans horaires structurés fiables. |
| A12 | **P2** | **Une aide immédiatement actionnable** : contact public de l’organisateur et choix “inscription / jeu / retrait”, si ces coordonnées sont autorisées. | L’aide actuelle renvoie à l’affiche ou à l’e-mail pour retrouver les coordonnées à distance. [S11] | Moyen, dépend d’un contact de support explicitement publiable. Ne jamais réutiliser un contact opérationnel privé. |
| A13 | **P3** | **Un souvenir personnel de l’animation** : étapes réalisées, lieux effectivement découverts, résultat et avis facultatif ; partage éventuel d’une carte publique sans accès personnel. | Historique et avis existent. La mise en récit des acquis peut prolonger le plaisir sans dépendre d’un gain. [S6, S8] | Moyen. Uniquement des accomplissements prouvés ; pas de classement public, de points ou de série quotidienne ajoutés implicitement. |

## L’accueil que je recommande

Conserver la navigation basse actuelle pendant cette première amélioration. Ne pas y ajouter une cinquième ou sixième entrée. Garder recherche et messages faciles à atteindre ; rendre l’installation contextuelle après une première valeur perçue, tout en laissant un accès dans Réglages.

Ordre proposé, adapté aux données disponibles :

1. **Contexte court** : commune ou communes sélectionnées ; aucune grande bannière qui repousse le contenu.
2. **Un bloc principal personnel** si pertinent : “Plus qu’une étape à réaliser” ou “Reprendre votre parcours”. Si un lot ou un message exige une action plus importante, lui donner cette place avec une règle d’ordre explicable. Les autres informations restent compactes.
3. **À découvrir maintenant** : quelques animations facilement comparables, chacune avec une seule action principale. Ne pas masquer l’accès au programme complet.
4. **Votre prochain rendez-vous** si connu : animation à venir ou tirage auquel l’habitant est qualifié.

Cas sans participation : montrer directement les animations. Cas sans commune : choix simple puis programme. Cas sans programme : conserver la commune suivie, annoncer honnêtement l’absence de contenu et proposer une autre sélection ; ne pas fabriquer une activité locale ni promettre des alertes de nouvelles animations non prises en charge.

## Direction UI : plus de plaisir, moins de bruit

- **Hiérarchie** : une action principale par carte ou état ; un secondaire immédiatement utile ; les gestes occasionnels restent disponibles à moindre poids visuel. Pas d’icônes seules pour les actions métier ambiguës.
- **Typographie** : le titre principal est déjà limité à environ 24–28 px via les variables Live. Ne pas le réduire encore globalement. Travailler surtout l’espace, les groupes et la fréquence des libellés ; vérifier les petits textes de statistiques à 0,70–0,75 rem sur téléphone réel. [S9]
- **Couleur** : bleu pour la structure, accent Localeo pour l’action, vert pour une réussite confirmée ; alerte réservée à un problème utile. Les couleurs accompagnent toujours un libellé ou une forme.
- **Animation d’interface** : transitions brèves et discrètes pour expliquer un changement d’état ; éviter un flux continuellement animé, les confettis répétitifs et le défilement forcé. Les préférences de mouvement réduit sont déjà partiellement traitées et doivent rester couvertes.
- **Contenu vivant** : privilégier un changement réel — étape accomplie, message publié, tirage annoncé — plutôt qu’un chiffre statique présenté comme de l’activité en direct. Les compteurs à zéro peuvent être relégués au détail sans modifier ni embellir la donnée.
- **Confort tactile** : conserver l’objectif produit de 44–48 px pour les principales commandes. Le minimum WCAG 2.2 AA est 24 × 24 px avec exceptions ; 44 px correspond au niveau renforcé, pas au minimum AA. [Référence W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
- **Mouvement accessible** : les effets non essentiels doivent pouvoir être désactivés ; le critère 2.3.3 est de niveau AAA. Cela guide la conception des célébrations sans constituer ici une certification. [Référence W3C](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html).

## Ordre de réalisation recommandé

| Lot | Contenu | Résultat attendu |
| --- | --- | --- |
| **1 — Se sentir accompagné** | A01–A04, accès direct aux favoris, contextualisation de base A06. | Savoir quoi faire à l’ouverture, comprendre que l’inscription a réussi et retrouver son parcours. |
| **2 — Prendre plaisir à participer** | A07, A08, A10, A11 et A12. | Voir ses progrès, se rendre facilement au bon endroit, profiter de son lot et obtenir de l’aide. |
| **3 — Revenir pour une bonne raison** | Recherche serveur et filtres A05, approfondissement A06, A09, expérimentation A13. | Découvrir tout le programme pertinent et revenir au moment utile sans pression. |

Une sélection de communes automatique, un nouveau compte habitant, une synchronisation complète, des points permanents ou un classement entre habitants ne sont pas nécessaires à ce premier plan. Ils demanderaient un besoin et des règles propres. La cadence et le ciblage des notifications doivent être examinés avant d’ajouter des envois : choix explicites, absence de doublons et fréquence adaptée au contenu.

Impacts possibles : Marketplace/Live pour les parcours et composants ; backend pour les projections personnelles, la recherche paginée ou les contacts publics supplémentaires ; Animation pour la qualité des informations publiées. Les évolutions de contrat, migrations, règles de qualification et générateur seront à examiner au lot retenu. **Le présent audit ne change aucun contrat ni critère d’acceptation existant.**

## Comment vérifier que cela améliore réellement l’adhésion

Faire une première session formative avec 5 à 8 habitants de niveaux numériques variés, puis corriger et rejouer. Ce petit groupe aide à découvrir les incompréhensions ; il ne mesure pas statistiquement la rétention. Inclure un téléphone Android, un iPhone, une personne peu habituée au numérique et un cas de texte agrandi.

| Scénario sans accompagnement | Observation à recueillir |
| --- | --- |
| Trouver une animation adaptée à sa commune. | Première action, hésitations, compréhension du défi et des contraintes avant inscription. |
| S’inscrire à une tombola depuis QR, ouvrir l’e-mail puis retrouver sa participation. | Comprend-on que l’inscription est déjà enregistrée ? Le carnet est-il retrouvé sans aide ? |
| Revenir le lendemain sur un parcours commencé, non urgent. | Temps et nombre d’actions jusqu’à la reprise ; destination choisie spontanément. |
| Identifier le prochain commerce connu et préparer sa visite. | Adresse/horaires trouvés sans quitter le parcours ; retour à l’étape conservé. |
| Recevoir une information de l’organisateur, sans autoriser les push. | L’information est-elle retrouvée et comprise ? Les permissions sont-elles expliquées ? |
| Comprendre une qualification puis récupérer un lot libre ou un bon. | Prochaine action identifiée ; aucune confusion entre progression, éligibilité et gain. |
| Ouvrir le lien personnel dans un autre navigateur puis installer Live. | Conservation ou récupération des accès comprise ; aucun sentiment de perte d’inscription. |
| Revenir sans nouveauté, hors période d’animation. | État vide compris ; aucune activité fictive ; raison du prochain retour identifiable si elle existe. |

Comparer avant/après sur les mêmes tâches : réussite sans aide, temps jusqu’à l’action utile, erreurs/retours arrière et satisfaction déclarée. Pour le suivi d’usage, établir d’abord une base de mesure : passage découverte → inscription → accès personnel ajouté, reprise d’une participation active, réalisation d’une étape, consultation d’un message pertinent et usage d’un lot. Suivre le retour à 7 jours uniquement chez les personnes ayant encore une animation ou un événement utile ; distinguer acquisition, usage actif et saisonnalité.

Les identités d’analytics, de navigateur, d’installation et de participation ne sont pas interchangeables. Ne pas fabriquer un taux de “rétention habitant” à partir de sessions anonymes sur plusieurs navigateurs. Définir les événements et le dénominateur avant instrumentation, conserver les choix de confidentialité, ne jamais inclure e-mail, token, QR ou position précise. Aucun objectif chiffré d’amélioration n’est promis sans mesure initiale.

## Sources de l’audit

Les chemins ci-dessous pointent vers les sources examinées ; les lignes mentionnées dans les constats de travail peuvent évoluer.

- **S1 — Accueil et priorités** : [LiveHome](../../../../localeo-marketplace/src/live/LiveHome.jsx), [useLiveDashboard](../../../../localeo-marketplace/src/live/useLiveDashboard.js), [règles de présentation](../../../../localeo-marketplace/src/live/liveDashboard.mjs), [carte de participation](../../../../localeo-marketplace/src/live/LiveParticipationCard.jsx). Repères : `LiveHome` 22–27 ; `useLiveDashboard` 72 ; `dashboardPriority` 10–12.
- **S2 — Inscription tombola** : [PublicTombolaRegistration](../../../../localeo-marketplace/src/components/PublicTombolaRegistration.jsx), succès autour de la ligne 42 ; [contrats E74, invariant I06](../../specifications/epic-74-tombola-publique/architecture-contrats.md).
- **S3 — Continuité et installation** : [guide de récupération](../../../../localeo-marketplace/src/live/LiveAccessRecoveryGuide.jsx), [LiveApp](../../../../localeo-marketplace/src/live/LiveApp.jsx), notamment `SavedNotice`, `InstallHelp`, `Settings` et sauvegarde/restauration ; [E42](../../specifications/epic-42-localeo-live/README.md).
- **S4 — Découverte** : [LiveDiscovery](../../../../localeo-marketplace/src/live/LiveDiscovery.jsx), carte 40–72 et recherche 208–217 ; [favoris/partage](../../../../localeo-marketplace/src/live/LiveDiscoveryActions.jsx), [communes](../../../../localeo-marketplace/src/live/LiveCommunes.jsx), [contexte communal](../../../../localeo-marketplace/src/live/LiveCommunityScene.jsx).
- **S5 — Messages** : [LiveMessages](../../../../localeo-marketplace/src/live/LiveMessages.jsx), [accord organisateur](../../../../localeo-marketplace/src/live/OrganizerMessagesPreference.jsx), `LiveNotificationSettings` dans LiveApp.
- **S6 — Jeu et satisfaction** : [LiveAnimationGame](../../../../localeo-marketplace/src/live/LiveAnimationGame.jsx), succès autour de 130 et 236 ; [satisfaction](../../../../localeo-marketplace/src/live/AnimationSatisfaction.jsx).
- **S7 — Récompenses** : [LiveLots](../../../../localeo-marketplace/src/live/LiveLots.jsx), [présentation des états](../../../../localeo-marketplace/src/live/liveRewards.mjs).
- **S8 — Tirage et rendez-vous** : [LiveDrawResult](../../../../localeo-marketplace/src/live/LiveDrawResult.jsx), [LiveDrawCalendar](../../../../localeo-marketplace/src/live/LiveDrawCalendar.jsx), [nouvelles de l’accueil](../../../../localeo-marketplace/src/live/LiveHomeHighlights.jsx).
- **S9 — UI** : [styles généraux](../../../../localeo-marketplace/src/live/live.css), [shell de jeu](../../../../localeo-marketplace/src/live/live-play-shell.css), [découverte](../../../../localeo-marketplace/src/live/live-discovery.css), [accueil](../../../../localeo-marketplace/src/live/live-home.css). Les constats portent sur les déclarations et la composition, pas sur un contrôle de styles calculés dans un navigateur.
- **S10 — Commerçants et principes E73** : [annuaire et fiche](../../../../localeo-marketplace/src/live/LiveMerchants.jsx), [spécification Live](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md), section « Commerçants partenaires ».
- **S11 — Aide** : [LiveJourneyHelp](../../../../localeo-marketplace/src/live/LiveJourneyHelp.jsx), notamment la redirection vers les supports externes pour le contact.

Scénarios existants lus ou repérés pour préparer la future recette : [densité d’accueil](../../../../localeo-marketplace/tests/visual/live-home-density.spec.cjs), [tombola](../../../../localeo-marketplace/tests/visual/e74-tombola-email.spec.cjs), [commerçants](../../../../localeo-marketplace/tests/visual/live-merchants.spec.cjs), [messages](../../../../localeo-marketplace/tests/visual/live-messages-product.spec.cjs), [lots](../../../../localeo-marketplace/tests/visual/live-lots-unified.spec.cjs). Le scénario de densité d’accueil examiné utilise un catalogue simple et un tableau de bord vide ; compléter la future recette avec plusieurs participations, messages et récompenses simultanés.

[Retour à l’index des audits](../INDEX.md)
