# Compte rendu du workshop Localeo Animation

18 novembre 2026 — **simulation contradictoire, étape 2 uniquement**. Aucun organisateur réel n’a été interrogé. Les citations sont fictives ; les notes, préférences et votes sont des instruments de discussion, jamais des mesures d’utilisabilité ni une autorisation de développement.

## Corpus et séquence

Base commune : [faits AN-01 à AN-24](../observations/observations-factuelles.md), [18 parcours](../observations/cartographie-parcours.md), [mesures réellement relevées](../observations/mesures-parcours.md), [limites](../observations/limitations.md), [inventaire des 63 captures réelles](../observations/inventaire-ecrans.md). La consultation du code est celle de l’étape 1, pas une nouvelle recette du code déployé.

Séquence suivie : lecture des preuves → avis séparés avant débat → formulation de 17 propositions → objections croisées → vote individuel sur un texte fixe → agrégation au seuil de sept → priorisation et conclusion. Trois agents ont préparé séparément les perspectives (cinq experts ; quatre profils métier ; trois profils métier). Cela ne crée pas douze évaluateurs humains indépendants : les rôles sont générés par des agents et partagent le même corpus.

Les **84 avis initiaux** (12 rôles × 7 ateliers) sont conservés, sans réécriture après vote : [E1 à E5](avis-independants-experts.md), [Françoise, Michel, Sophie, Julie](avis-independants-metier-1.md), [Karim, Élodie, Bernard](avis-independants-metier-2.md). Les objections ont été transmises entre groupes avant les bulletins. Les [propositions exactes](orientations-soumises.md), les [votes et réponses contradictoires](votes-et-arbitrages.md) et le [backlog](backlog-ux.md) permettent de suivre chaque décision.

### Participants fictifs

| ID de vote | Perspective |
| --- | --- |
| E1 | UX Designer senior : navigation, formulaires, cohérence |
| E2 | Product Manager SaaS B2B : autonomie, périmètre, adoption |
| E3 | Opérations événementielles : coordination, incidents, clôture |
| E4 | Onboarding et accessibilité : compréhension, guidage, usages peu expérimentés |
| E5 | UX Researcher/facilitateur : preuves, biais, vérification des hypothèses |
| Francoise | Françoise, 67 ans, présidente associative, très faible aisance numérique, 2–3 animations/an |
| Michel | Michel, 59 ans, trésorier bénévole, occasionnel, tombola et dotations |
| Sophie | Sophie, 43 ans, chargée de commerce en mairie, aisance intermédiaire, nombreux commerces |
| Julie | Julie, 36 ans, animatrice de centre-ville, expérimentée, rapidité et opérations |
| Karim | Karim, 48 ans, président associatif, peu de temps, invitations et préparation |
| Elodie | Élodie, 29 ans, communication, très à l’aise numériquement, supports et messages |
| Bernard | Bernard, 62 ans, élu au commerce, occasionnel, états et bilans |

Les besoins sont rattachés au contexte d’usage décrit, sans déduire une capacité de l’âge.

## A — Première impression et onboarding organisateur

**Question :** un nouvel organisateur sait-il immédiatement commencer ?

**Écrans présentés :** [connexion](../visuels/captures-avant/01-connexion-bureau.png), [accueil](../visuels/captures-avant/02-tableau-bord-bureau.png), [liste](../visuels/captures-avant/03-animations-bureau.png), [accueil mobile](../visuels/captures-avant/44-tableau-bord-mobile.png). La connexion a fonctionné avec un compte existant ; l’activation initiale n’a pas été testée.

**OBSERVÉ — forces :** contexte communal, navigation, accès aux animations, prochaines actions et notifications existent (AN-01–02, AN-19). **OBSERVÉ — problème :** de nombreuses cartes jaunes apparaissent avant les actions ; la capture 02 montre aussi des informations positives portant ce signal. **HYPOTHÈSE :** cette hiérarchie peut ralentir le repérage d’une urgence.

**Débat :** E1/E4 proposent de différencier information et action ; Françoise et Bernard interprètent fictivement le jaune comme une anomalie. Élodie tient à conserver les nouvelles ; E2 préfère réordonner les éléments existants avant d’offrir un tableau personnalisable. Arbitrage soumis : A1 conserve toutes les informations ; A2 traite séparément la personnalisation, dont le besoin est moins établi. Les cinq avis experts et sept réactions individuelles figurent à la ligne A de chaque annexe.

**Orientations et décision :** A1, A2 ; résultats nominatifs dans [votes et arbitrages](votes-et-arbitrages.md), portée et critères dans [backlog](backlog-ux.md).

## B — Création et publication

**Question :** peut-on créer une tombola ou un passeport en 5–10 minutes sans assistance ?

**Écrans :** [modèles](../visuels/captures-avant/04-creation-modeles.png), [erreur de dates](../visuels/captures-avant/06-erreur-dates.png), [dotation](../visuels/captures-avant/09-dotation.png), [récapitulatif](../visuels/captures-avant/12-recapitulatif.png), [sortie sans enregistrement](../visuels/captures-avant/48-sortie-saisie-mobile.png).

**OBSERVÉ — forces :** sept étapes identifiables, validation des dates, récapitulatif modifiable, lots libres sans achat, responsabilité de remise, brouillon distinct de publication et aperçu signalant son QR provisoire (AN-03–09). **OBSERVÉ — problèmes :** sauvegarde initiale tardive ; seuil passeport à quatre après sélection de deux commerces ; diagnostics techniques (AN-03, AN-05, AN-10). **HYPOTHÈSE :** perte de travail ou confusion entre préparation et mise en ligne. Le blocage de publication sans accord est un garde-fou attendu, pas une panne constatée.

**Débat :** Julie veut gagner du temps mais ne demande pas de supprimer arbitrairement les étapes ; Françoise et Bernard trouvent ce guidage rassurant. E1/E4 privilégient sauvegarde et valeurs cohérentes ; E3 exige de conserver les conditions de publication et les responsabilités des lots. Michel veut reconnaître le chemin des cadeaux offerts. E2/E5 contestent une promesse chronométrique qui inclurait les réponses de tiers. Le formulaire unique B4 reste une proposition distincte, sans enlever le parcours guidé.

**Arbitrages :** B1 protège une préparation partielle, avec contrat à concevoir ; B2 explique résultat, acteurs et prérequis ; B3 ajuste seulement la valeur initiale et signale toute incompatibilité ultérieure ; B4 ajoute un mode facultatif. Aucune mesure humaine n’autorise à promettre 5–10 minutes. Les 14/15 actions automatisées ne deviennent pas un temps estimé.

**Orientations et décision :** B1–B4 ; [votes](votes-et-arbitrages.md) et [critères](backlog-ux.md).

## C — Onboarding des commerçants

**Question :** peut-on intégrer les commerces et savoir lesquels sont prêts ?

**Écrans :** [sélection](../visuels/captures-avant/07-selection-commercants.png), [invitations non envoyées](../visuels/captures-avant/15-invitations-non-envoyees.png), [import](../visuels/captures-avant/21-import-commercants.png), [aperçu](../visuels/captures-avant/23-import-apercu.png), [invitation acceptée existante](../visuels/captures-avant/58-invitation-acceptee-existante.png).

**OBSERVÉ — forces :** sélection, envoi, attente, acceptation et refus distincts ; échéance explicite ; aperçu d’import avant confirmation. **OBSERVÉ — problèmes :** ajout individuel non trouvé dans le périmètre ; modèle CSV à remapper ; deux lignes similaires proposées en création avec zéro conflit (AN-11–15). **DÉDUIT :** le code local rapproche des identifiants forts, pas simplement nom/adresse. **Limite :** ni création des deux fiches ni activation de compte exécutées.

**Débat :** Françoise cherche un chemin pour un seul fleuriste ; E2 exige de vérifier le référencement canonique avant de créer une nouvelle fonction. Sophie et Élodie veulent préassocier le modèle fourni ; E5 refuse d’appeler l’aperçu une preuve de doublons effectivement créés. E3/Sophie refusent la fusion automatique. Karim veut savoir qui doit agir mais s’oppose aux rappels qui partiraient sans maîtrise ; Julie évoque le coût des relances nombreuses.

**Arbitrages :** C1 demande un chemin et un suivi, sans activation implicite ; C2 rend le rapprochement explicite, les similitudes restant une décision humaine ; C3 propose des relances facultatives avec aperçu, confirmation et annulation. B2 couvre la prochaine action et les états fiables ; « accepté » ne signifie jamais « compte activé » par déduction.

**Orientations et décision :** C1–C3 ; [votes](votes-et-arbitrages.md) et [backlog](backlog-ux.md).

## D — Suivi opérationnel

**Question :** sait-on si l’animation se déroule correctement et comment intervenir ?

**Écrans :** [suivi détaillé](../visuels/captures-avant/26-suivi-detail.png), [participants](../visuels/captures-avant/27-participants-animation.png), [échec Communication](../visuels/captures-avant/31-communication-echec-confirme.png), [notifications](../visuels/captures-avant/32-notifications.png).

**OBSERVÉ — forces :** définitions, périmètres et dates d’indicateurs ; distinction inscription/progression/qualification/validation ; notifications consultables. **OBSERVÉ — problèmes :** « Consulter le suivi » aboutit au bilan ; Communication échoue deux fois en 500 (AN-16–19). **Limites :** pas de nouvel envoi ni de réception testée, pas de diagnostic causal du 500.

**Débat :** Julie et E1 demandent un lien prévisible. Michel/Sophie/Bernard veulent conserver les distinctions des chiffres ; aucun nouveau tableau temps réel n’est proposé. Élodie refuse de remplacer une réparation par une meilleure phrase d’erreur. E2 considère Communication prioritaire si elle fait partie de la promesse de lancement ; E5 limite cette conclusion au contexte en échec. E3 distingue échec de lecture et envoi au résultat inconnu.

**Arbitrages :** D1 couvre fiabilité et reprise, sans renvoi automatique ; D2 corrige l’accès en conservant les explications des indicateurs. Le P0 de D1 est attaché à l’ouverture autonome incluant cette fonction ; aucune indisponibilité générale n’est affirmée.

**Orientations et décision :** D1–D2 ; [votes](votes-et-arbitrages.md), [risques critiques](rapport-executif.md#risques-critiques-et-limites-de-décision).

## E — Clôture et bilan

**Question :** peut-on terminer sereinement et comprendre ce qui reste ?

**Écrans :** [confirmation de clôture](../visuels/captures-avant/62-confirmation-cloture-detail.png), [fin et archivage](../visuels/captures-avant/35-fin-archivage.png), [gains et remises](../visuels/captures-avant/37-gains-remises.png), [bilan](../visuels/captures-avant/38-bilan-cloturee.png), [gagnant masqué](../visuels/captures-avant/63-gagnant-email-masque.png).

**OBSERVÉ — forces :** conséquences définitives explicites, confirmation, dossiers restants, distinction gagnant informé/lot remis. **OBSERVÉ — situation à expliquer :** date dépassée et animation encore En cours ; clôturée, terminée, archivée sont des états distincts (AN-20–21). **HYPOTHÈSE :** un utilisateur occasionnel peut croire l’opération achevée trop tôt. Rien ne prouve que la clôture manuelle soit une erreur métier.

**Débat :** Françoise demande d’expliquer le « gel » par la liste de personnes éligibles qui ne change plus. Michel protège la traçabilité de remise. Bernard veut comprendre pourquoi la date et le statut diffèrent. E3 et Julie refusent de résoudre cette ambiguïté par une clôture automatique imposée. Une programmation facultative E2 est soumise séparément, avec précontrôles et annulation ; ses risques subsistent même si le vote la rejette.

**Arbitrages :** E1 améliore explication et accès aux dossiers existants ; E2 constitue une nouvelle règle métier importante, pas une modification de libellé. Tirage, remise, export et partage n’ont pas été exécutés : aucune réussite bout en bout n’est revendiquée.

**Orientations et décision :** E1–E2 ; [votes](votes-et-arbitrages.md) et [orientations non retenues](orientations-rejetees.md).

## F — Pilotage global

**Question :** peut-on piloter plusieurs animations sans perdre le fil ?

**Écrans :** [liste](../visuels/captures-avant/03-animations-bureau.png), [recherche](../visuels/captures-avant/39-recherche-brouillons.png), [clonage](../visuels/captures-avant/40-clonage.png), [clone](../visuels/captures-avant/42-clone-cree.png).

**OBSERVÉ — forces :** recherche et filtres conservés au retour ; réinitialisation ; clone sans reprise d’engagements, participants, accords ou lots (AN-22–23). **HYPOTHÈSE — besoins :** vues récurrentes, échéances transversales, consultation entre deux événements. Le jeu de sept animations initiales n’est pas une preuve de pilotage de 500 organisations.

**Débat :** Sophie/Julie privilégient une vision transversale ; Karim veut d’abord les prochaines actions ; Françoise n’a que quelques animations et demande une reprise claire. Élodie/Michel soutiennent la transparence des exclusions au clonage ; E2 refuse une reprise automatique d’engagements périmés. E3 n’impose pas un calendrier à tous les usages.

**Arbitrages :** préserver recherche et clonage ; A1/B2 répondent déjà à la hiérarchie des actions. F1 ajoute des vues sauvegardées partageables ; F2 un calendrier complémentaire, à éprouver avec des volumes représentatifs.

**Orientations et décision :** F1–F2 ; [votes](votes-et-arbitrages.md) et [backlog](backlog-ux.md).

## G — Simplification et autonomie

**Question :** qu’est-ce qui exige encore un accompagnement ?

**Écrans :** [assistant mobile](../visuels/captures-avant/49-assistant-mobile.png), [invitations mobile](../visuels/captures-avant/51-invitations-mobile.png), [navigation mobile](../visuels/captures-avant/52-navigation-mobile.png), avec les écrans des ateliers B–E.

**OBSERVÉ — forces :** structure cohérente, navigation mobile et huit contrôles de largeur sans débordement global. **OBSERVÉ — sources de friction :** diagnostics techniques, sauvegarde tardive, 18 rubriques mobiles (AN-03, AN-10, AN-24). **HYPOTHÈSE :** la recherche d’une tâche peut être difficile ; aucun test sur téléphone physique ou lecteur d’écran ne permet de conclure à l’accessibilité.

**Débat :** E4 préfère mots simples et reprise sûre à une réduction de champs qui déplacerait le risque ; E2 limite les nouvelles fonctions. Julie/Élodie refusent un tutoriel imposé ; Bernard veut retrouver le prochain geste après une absence ; Françoise demande des repères. E5 rappelle que leurs préférences ne valident aucune solution.

**Arbitrages :** B1/B2/B3/D2/E1 constituent les simplifications de fond. G1 propose des raccourcis mobiles sans retirer le sélecteur complet ; G2 une visite facultative, jamais utilisée pour masquer les défauts. Aucune étape n’est supprimée uniquement pour faire baisser le nombre de clics.

**Orientations et décision :** G1–G2 ; [votes](votes-et-arbitrages.md) et [quick wins](quick-wins.md).

## Matrice des sept profils × cinq missions

**Toutes les cellules expriment une difficulté ou une attente SIMULÉE, non une réussite/erreur observée chez une personne.** La matrice synthétise les avis individuels conservés ; elle n’est pas une enquête ni un score.

| Profil fictif | A — Créer/publier | B — Intégrer les commerces | C — Suivre/intervenir | D — Clôturer/bilan | E — Piloter plusieurs animations |
| --- | --- | --- | --- | --- | --- |
| Françoise | Étapes rassurantes ; enregistrer sans tout connaître | Trouver où demander un commerce absent | Un lien Suivi doit mener au suivi | Comprendre les conséquences en mots courants | Retrouver la prochaine action après plusieurs semaines |
| Michel | Reconnaître les cadeaux fournis et leur responsable | Savoir qu’un brouillon n’envoie rien | Comprendre inscrits versus éligibles | Ne pas confondre email et remise | Voir ce que le clone reprend ou exclut |
| Sophie | Préparer en plusieurs sessions avec l’équipe | Importer le modèle sans remappage inutile | Lire des chiffres définis et datés | Savoir ce qui reste après la fin de période | Conserver les filtres et voir les échéances |
| Julie | Reprendre vite ; seuil cohérent | Distinguer sélection, invitation, accord, préparation | Accès direct et Communication fonctionnelle | Garder la maîtrise de la clôture | Accès rapides en mobilité et retour conservé |
| Karim | Interrompre/reprendre ; pas de promesse dépendant de tiers | Identifier le prochain acteur | Trouver les actions sans détour par le bilan | Résoudre un dossier restant par un lien direct | Voir les animations qui attendent son intervention |
| Élodie | Savoir quand diffuser le support définitif | Reconnaître le modèle et les limites de rapprochement | Préparer/envoyer sans doute ni répétition implicite | Communiquer des résultats sans masquer les remises restantes | Clonage explicite et informations hiérarchisées |
| Bernard | Comprendre résultat et prérequis ; garder le guidage | Lire des statuts simples et fiables | Distinguer inscription, fin et qualification | Comprendre date, clôture et périmètre du bilan | Retrouver le contexte sans apprendre tous les modules |

## Limites de preuve visuelle

Une capture ne prouve que sa portion visible. La 18 ne montre pas suffisamment le champ de seuil inférieur ; AN-05 et les relevés DOM portent ce constat. La 22 ne montre pas tout le mapping. La 60, malgré son nom, montre surtout la configuration : le bouton de publication bloqué est documenté par AN-09 et les relevés techniques. Le panneau partiellement hors champ de la 52 ne suffit pas à conclure à un défaut permanent. Aucune de ces captures n’a été reconstruite ou retouchée pendant le workshop.

## Suites autorisées à ce stade

Les votes sélectionnent des orientations de discussion. Ils ne valident ni maquette, ni spécification, ni développement. La conclusion et les cinq améliorations de lancement sont dans le [rapport exécutif](rapport-executif.md). L’étape 3 attend une autorisation de l’utilisateur ; aucun prototype ni changement applicatif n’est réalisé ici.
