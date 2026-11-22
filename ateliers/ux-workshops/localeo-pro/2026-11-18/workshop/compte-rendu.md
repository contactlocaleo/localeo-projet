# Compte rendu du workshop UX Localeo Pro

18 novembre 2026 — **simulation contradictoire de douze rôles fictifs**, aucun commerçant interrogé, aucun nouvel essai applicatif. La séance porte sur les quatre missions Animation. La gestion des coffrets reste hors périmètre ; les mots « pack » et le bloc PIN ne sont discutés que lorsqu’ils perturbent ce parcours.

## Référence commune et méthode

Lecture intégrale du [README](../README.md), de la [cartographie](../observations/cartographie-parcours.md), de l’[inventaire](../observations/inventaire-ecrans.md), des [observations](../observations/observations-factuelles.md), des [limitations](../observations/limitations.md) et des 22 [captures réelles](../visuels/captures-avant/README.md). **OBSERVÉ** = preuve de l’étape 1 ; **DÉDUIT** = lecture du code de cette étape ; **HYPOTHÈSE** = interprétation ou scénario simulé. Les opinions et bénéfices de cette séance sont tous des hypothèses, même lorsqu’ils partent d’un fait observé.

Les avis initiaux ont été produits séparément pour les cinq experts, quatre commerçants et trois commerçants, avant les votes. La confrontation et ses formulations sont une restitution éditoriale simulée, pas la transcription d’une réunion réelle. Chaque atelier présente écrans, douze avis, débat, points forts/difficultés, deux orientations et décision ; les 168 votes nominatifs et leur argument sont dans le [registre](votes-et-arbitrages.md). Le facilitateur possède une voix ordinaire. Aucun consensus n’a été imposé ni taux de réussite mesuré.

Les captures longues comportent des éléments fixes à la position de la fenêtre initiale : leur présence au milieu d’une image ne prouve ni recouvrement en usage ni défaut de focus. Le 401 concerne l’URL gestionnaire donnée à l’exploration. L’URL directe /animations/notifications ne correspond pas au lien normal de notification. Aucune de ces deux observations ne sera transformée en panne générale de Pro.

## Participants

| Rôle | Angle de lecture |
| --- | --- |
| Expert 1 — UX Designer senior | Hiérarchie, navigation et parcours mobile |
| Expert 2 — Accessibilité | Lisibilité, compréhension, clavier et aides techniques à éprouver |
| Expert 3 — Product Manager B2B | Valeur commerçant, périmètre et priorité MVP |
| Expert 4 — Opérations terrain | Comptoir, QR, préparation et logistique |
| Expert 5 — Researcher et facilitateur | Biais, preuves, scénarios et votes sans voix prépondérante |
| Martine, 63 ans, fleuriste | Très faible aisance numérique ; peur des manipulations |
| Patrick, 57 ans, boulanger | Temps limité, interruptions et file d’attente |
| Nadia, 44 ans, salon de coiffure | Aisance intermédiaire ; anticipation et supports |
| Julien, 35 ans, restaurateur | Habitué aux outils professionnels ; rapidité et fiabilité |
| Claire, 51 ans, prêt-à-porter | Usage occasionnel ; messages et information retrouvable |
| Hugo, 29 ans, boutique spécialisée | Forte aisance ; cohérence et efficacité |
| Isabelle, 48 ans, libraire | Usage intermittent ; repères après plusieurs semaines |

## Atelier A — Première impression

**Question :** Un commerçant comprend-il immédiatement à quoi sert Localeo Pro et ce qu’il doit faire ?

**Écrans présentés :** [00 portail](../visuels/captures-avant/00-portail-fourni-mobile.png), [01 refus](../visuels/captures-avant/01-portail-fourni-refus-mobile.png), [02 connexion](../visuels/captures-avant/02-connexion-pro-mobile.png), [03 accueil mobile](../visuels/captures-avant/03-accueil-pro-mobile.png), [10 accueil ordinateur](../visuels/captures-avant/10-accueil-pro-desktop.png).

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « Le scanner fournit une action identifiable ; invitations et préparation plus bas rendent le rôle de carnet moins visible. » |
| Expert 2 — Accessibilité | « Les quatre entrées mobiles sont un repère à conserver ; noms accessibles, focus et agrandissement restent à tester. » |
| Expert 3 — Product Manager B2B | « Clarifier le point d’entrée Pro sans conclure à une panne d’authentification de Pro. » |
| Expert 4 — Opérations terrain | « Le scanner doit rester rapide à atteindre pendant l’accueil ; une tâche de préparation doit aussi pouvoir émerger. » |
| Expert 5 — Researcher et facilitateur | « Un compte aux invitations déjà acceptées ne permet pas d’évaluer une première prise en main complète. » |
| Martine — fleuriste, 63 ans | « Si mon mot de passe ne marche pas sur le premier site, je demande de l’aide ; au bon endroit, je commencerais par le gros bouton Scanner. » |
| Patrick — boulanger, 57 ans | « J’appuierais directement sur Scanner ; pendant le service, je n’aurai pas le temps de descendre chercher le reste. » |
| Nadia — salon de coiffure, 44 ans | « Je regarderais les animations à venir ; deux ici et trois dans la liste me feraient vérifier si j’ai oublié quelque chose. » |
| Julien — restaurateur, 35 ans | « J’irais au scanner, mais l’écart des compteurs me ferait douter de ce qui est en cours. » |
| Claire — prêt-à-porter, 51 ans | « Sur la première adresse, je penserais avoir oublié mon mot de passe ; sur Pro, je chercherais la prochaine animation. » |
| Hugo — boutique spécialisée, 29 ans | « J’irais au scanner puis aux animations ; je chercherais ce que chaque compteur inclut. » |
| Isabelle — libraire, 48 ans | « Après plusieurs semaines, je regarderais à quelle animation je participe et ce qui a changé. » |

### Débat contradictoire et constats

Martine demande qu’on lui montre chaque étape ; Patrick et Julien refusent cinq écrans avant de servir. Le PM rappelle que le refus HTTP 401 appartient au portail gestionnaire, pas à une panne de connexion Pro. Hugo réclame de vérifier les supports existants avant d’ajouter du texte. Le compromis soumis au vote est une entrée identifiée et une aide facultative (A1), tandis que le tutoriel obligatoire reste une alternative distincte (A2).

**Points forts :** OBSERVÉ : scanner très visible, navigation courte sur mobile, espace commerçant nommé à la connexion.

**Difficultés et limites :** OBSERVÉ : mauvaise URL fournie à l’exploration. HYPOTHÈSE : rôle de préparation moins évident pour un nouvel arrivant ; aucun onboarding complet observé.

### Orientations et vote

- **A1 — Identifier l’accès Pro et expliquer son rôle en une phrase :** Vérifier les liens réellement diffusés ; identifier clairement l’espace commerçant et ajouter, si utile, une phrase sur la participation aux animations avec une aide courte à la demande. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#a1).
- **A2 — Imposer cinq écrans de tutoriel avant le premier scan :** Tutoriel obligatoire en cinq écrans avant l’accès initial au scanner. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#a2).

**Décision enregistrée :** A1 adopté à 11 voix avec l’abstention de Hugo ; A2 rejeté, malgré la voix de Martine. Vérifier la bonne adresse avant diffusion est une condition opérationnelle, pas une preuve que les liens du produit sont faux.

## Atelier B — Validation d’une participation

**Question :** Un commerçant peut-il valider une participation rapidement, sans erreur et sans assistance ?

**Écrans présentés :** [04 scanner mobile](../visuels/captures-avant/04-scanner-mobile.png), [12 scanner ordinateur](../visuels/captures-avant/12-scanner-desktop.png), [19 erreur locale](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png). C02 décrit les autres états ; aucune capture de succès.

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « Le message « QRCode du pack » n’explique pas comment corriger la saisie et son vocabulaire est à vérifier. » |
| Expert 2 — Accessibilité | « La voie manuelle est utile ; libellés, clavier, focus et annonce de l’erreur doivent être vérifiés. » |
| Expert 3 — Product Manager B2B | « Les états présents dans le code doivent être éprouvés sur le déploiement avant de promettre une validation fiable. » |
| Expert 4 — Opérations terrain | « Le résultat doit permettre de décider devant le participant ; une issue incertaine doit donner une consigne. » |
| Expert 5 — Researcher et facilitateur | « L’échec en Chromium automatisé ne démontre pas une panne sur téléphone ; il faut caméra physique et QR autorisé. » |
| Martine — fleuriste, 63 ans | « Avant de confirmer, j’aimerais voir pour quelle animation je valide, puis savoir que c’est bien passé. » |
| Patrick — boulanger, 57 ans | « Confirmer à chaque client va me ralentir ; il faut au moins un bouton sous mon pouce. » |
| Nadia — salon de coiffure, 44 ans | « Une confirmation me rassurerait si elle me montre ce que je m’apprête à valider. » |
| Julien — restaurateur, 35 ans | « Si le même code revient, dites-moi s’il a déjà été validé. » |
| Claire — prêt-à-porter, 51 ans | « Le gros bouton me rassure, mais « QRCode du pack » ne me dit pas quel code demander. » |
| Hugo — boutique spécialisée, 29 ans | « Je veux distinguer le code reconnu de la participation validée et passer au client suivant sans hésiter. » |
| Isabelle — libraire, 48 ans | « Avant de scanner, j’aimerais une courte indication du code à demander et du message qui signifie que c’est terminé. » |

### Débat contradictoire et constats

Patrick préfère la validation automatique B2 pour sa file. Martine et Nadia veulent vérifier l’animation ; Hugo distingue reconnaissance et intention de valider. L’expert opérations souligne le coût d’une validation accidentelle. Le researcher refuse de déduire une panne caméra de Chromium. B1 conserve les garanties existantes et impose la recette avant changement ; la durée souhaitée par Patrick devient une mesure à recueillir, sans objectif chiffré inventé.

**Points forts :** OBSERVÉ : accès direct, voie manuelle, erreur visible. DÉDUIT : confirmation séparée et reçu de réconciliation présents dans le code.

**Difficultés et limites :** OBSERVÉ : erreur « pack » non contextualisée. NON TESTÉ : scan réel, confirmation, doublon, caméra physique, temps en caisse.

### Orientations et vote

- **B1 — Rendre le scan et son résultat compréhensibles, éprouver les garanties existantes :** Corriger le message hors contexte ; expliquer quel QR présenter et le prochain geste possible. Conserver la confirmation distincte, le reçu et les protections contre les renvois. Recetter sur téléphone puis modifier seulement les écarts établis. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#b1).
- **B2 — Valider automatiquement tout QR reconnu :** Supprimer la confirmation après reconnaissance du QR. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#b2).

**Décision enregistrée :** B1 adopté 11–1, Patrick contre ; B2 rejeté 1–11. Le besoin de rapidité reste ouvert. Une reconnaissance QR ne sera pas assimilée à une validation réussie.

## Atelier C — Notifications

**Question :** Le commerçant comprend-il qu’une animation approche et ce qui est attendu de lui ?

**Écrans présentés :** [09 boîte](../visuels/captures-avant/09-notifications-generales-mobile.png), [03 résumé accueil](../visuels/captures-avant/03-accueil-pro-mobile.png). [08 accès direct non prévu](../visuels/captures-avant/08-notifications-animation-mobile.png) n’est pas une preuve d’échec du lien Notifications.

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « Le bloc PIN vide avant les messages Animation donne une priorité visuelle à réexaminer pour ce profil. » |
| Expert 2 — Accessibilité | « La notification non lue doit être identifiable sans couleur seule ; sa destination doit être compréhensible. » |
| Expert 3 — Product Manager B2B | « Exposer action et échéance lorsqu’elles existent ; ne pas affirmer qu’elles manquent partout. » |
| Expert 4 — Opérations terrain | « Un message utile doit ouvrir la préparation ou la demande avec son contexte. » |
| Expert 5 — Researcher et facilitateur | « La boîte prouve des notifications internes, ni la réception push/email ni leur efficacité. » |
| Martine — fleuriste, 63 ans | « Avec neuf messages et une case PIN vide au-dessus, je ne saurais pas quoi regarder en premier. » |
| Patrick — boulanger, 57 ans | « Je veux un rappel quand quelque chose m’attend, pas neuf messages à relire. » |
| Nadia — salon de coiffure, 44 ans | « Je voudrais retrouver les consignes et un rappel avant la date, même si j’ai déjà lu le message. » |
| Julien — restaurateur, 35 ans | « Je veux choisir les alertes utiles et ouvrir directement l’action concernée. » |
| Claire — prêt-à-porter, 51 ans | « Je voudrais reconnaître le message qui me demande quelque chose et ouvrir l’animation. » |
| Hugo — boutique spécialisée, 29 ans | « Les liens me conviennent ; le bloc PIN vide prend de la place sans m’aider. » |
| Isabelle — libraire, 48 ans | « Une seule notification non lue ne me dit pas si une ancienne demande attend encore ma réponse. » |

### Débat contradictoire et constats

Isabelle peut avoir lu un message dont l’action reste à faire ; Nadia souhaite un rappel lié à la date, tandis que Julien veut choisir ses interruptions. UX propose de replier PIN pour le compte observé ; Accessibilité exige une commande nommée et retrouvable. La discussion distingue la notification de publication du flyer, information, d’une demande nécessitant une décision. C1 utilise les états réellement disponibles ; C2 relance sur la nonlecture seule.

**Points forts :** OBSERVÉ : boîte interne, état lu/non lu, noms d’animations et liens vers demande/animation.

**Difficultés et limites :** OBSERVÉ : section PIN vide avant Animation. HYPOTHÈSE : lecture confondue avec tâche accomplie. Canaux push/email et moment de réception non testés.

### Orientations et vote

- **C1 — Distinguer information reçue et action attendue :** Donner la priorité aux notifications Animation pour ce profil, replier la section PIN vide sans retirer son accès. Exposer animation, nature information/action, échéance connue et lien direct vers l’action autorisée. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#c1).
- **C2 — Relancer chaque jour tous les messages non lus par push :** Push quotidien systématique à tous tant qu’un message reste non lu. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#c2).

**Décision enregistrée :** C1 adopté 12–0 ; C2 rejeté 0–12. La boîte interne est confirmée ; le code WebPush est connu, mais ni sa réception ni un email ne sont validés par ce vote.

## Atelier D — Préparation de l’animation

**Question :** Le commerçant sait-il exactement ce qu’il doit préparer avant le lancement ?

**Écrans présentés :** [05 liste mobile](../visuels/captures-avant/05-animations-mobile.png), [11 liste ordinateur](../visuels/captures-avant/11-animations-desktop.png), [06 invitations](../visuels/captures-avant/06-invitations-mobile.png), [07 préparations](../visuels/captures-avant/07-preparation-mobile.png), [16 Vitrines](../visuels/captures-avant/16-preparation-vitrines-mobile.png), [17 Tombola](../visuels/captures-avant/17-preparation-tombola-mobile.png).

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « L’étape 4/4 et l’état prêt sont utiles ; tester aussi un commerce qui n’a pas terminé. » |
| Expert 2 — Accessibilité | « La progression et les erreurs doivent rester compréhensibles autrement que par un changement visuel. » |
| Expert 3 — Product Manager B2B | « Vérifier le sens de prêt, approuvé et contrôlé avant de les simplifier. » |
| Expert 4 — Opérations terrain | « Pour une tombola à venir, validations fermées devrait s’accompagner d’un repère ou geste connu. » |
| Expert 5 — Researcher et facilitateur | « Un cas déjà approuvé ne renseigne pas sur les efforts, abandons ou aides pendant la préparation. » |
| Martine — fleuriste, 63 ans | « Pour demain, dites-moi simplement quoi faire avant d’ouvrir ma boutique. » |
| Patrick — boulanger, 57 ans | « Dites-moi ce qu’il manque et combien de temps cela va prendre. » |
| Nadia — salon de coiffure, 44 ans | « Le 4 sur 4 me rassure ; je voudrais aussi savoir quand commencer la prochaine préparation. » |
| Julien — restaurateur, 35 ans | « Pour demain, je veux connaître l’heure exacte où les validations ouvriront. » |
| Claire — prêt-à-porter, 51 ans | « Prête, 4 sur 4 me rassure ; pour la tombola, que puis-je préparer aujourd’hui ? » |
| Hugo — boutique spécialisée, 29 ans | « Montrez les éventuelles actions restantes et l’heure d’ouverture des validations. » |
| Isabelle — libraire, 48 ans | « L’état prête m’éviterait de tout revérifier si je vois pour quelle animation et quelle date. » |

### Débat contradictoire et constats

Patrick et Martine veulent un état simple ; Nadia et Julien refusent qu’accepter vaille installer. Le PM demande de diagnostiquer le classement serveur avant de corriger les chiffres. D1 vise un prochain geste lisible, sans fusionner les décisions. UX, Accessibilité et Martine s’abstiennent car la présentation des cinq notions reste à définir : leur réserve devient un test de compréhension explicite. Le temps de préparation demandé par Patrick ne sera affiché que s’il est établi.

**Points forts :** OBSERVÉ : mission et dates, parcours en étapes, préparation prête/approuvée/contrôlée visible sur Vitrines.

**Difficultés et limites :** OBSERVÉ : compteurs divergents et carte passée classée en cours. HYPOTHÈSE : confusion sur responsabilité ou prochaine action ; cas incomplet non observé.

### Orientations et vote

- **D1 — Rendre cohérents dates, états et prochaine action de préparation :** Diagnostiquer la règle et le périmètre des compteurs, puis afficher des états cohérents ou des différences explicitement justifiées. Mettre en avant le prochain geste, son responsable et sa date connue, en conservant les distinctions métier derrière une présentation progressive. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#d1).
- **D2 — Fusionner les états dans « Tout est prêt » :** Un bouton unique fusionnerait accepté, prêt, approuvé et contrôlé. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#d2).

**Décision enregistrée :** D1 adopté 9 pour, 3 abstentions ; D2 rejeté 2–10. L’adoption n’efface pas la réserve sur les statuts. Aucune nouvelle règle de classement ou transition métier n’est décidée.

## Atelier E — Kit d’animation et logistique

**Question :** Le commerçant retrouve-t-il facilement les éléments nécessaires à sa participation ?

**Écrans présentés :** [13 détail Vitrines](../visuels/captures-avant/13-detail-vitrines-mobile.png), [14 Juste Prix](../visuels/captures-avant/14-detail-juste-prix-mobile.png), [15 Tombola](../visuels/captures-avant/15-detail-tombola-mobile.png), [18 invitation acceptée](../visuels/captures-avant/18-invitation-acceptee-mobile.png), [21 guide ouvert](../visuels/captures-avant/21-guide-preparation-mobile.png).

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « Distinguer les QR au moment de l’usage ; leur distinction dans le guide ne prouve pas sa compréhension. » |
| Expert 2 — Accessibilité | « Présenter les dates locales lisiblement ; accessibilité des fichiers téléchargés encore inconnue. » |
| Expert 3 — Product Manager B2B | « Distinguer ce qui peut être attesté de ce qui reste une déclaration de préparation. » |
| Expert 4 — Opérations terrain | « Relier impression et affichage à un support et une échéance lorsqu’ils sont connus. » |
| Expert 5 — Researcher et facilitateur | « Le bouton démontre un accès visible, pas la disponibilité du fichier ni sa qualité d’impression. » |
| Martine — fleuriste, 63 ans | « Je voudrais un bouton Imprimer mon affiche et des dates comme sur un calendrier. » |
| Patrick — boulanger, 57 ans | « Je préfère pouvoir tout imprimer d’un coup avant le coup de feu. » |
| Nadia — salon de coiffure, 44 ans | « J’ouvrirais le kit à l’avance pour vérifier les affiches et savoir quel QR donner au client. » |
| Julien — restaurateur, 35 ans | « Je vérifierais que le kit contient le nécessaire et que les QR ont chacun un usage clair. » |
| Claire — prêt-à-porter, 51 ans | « Quel support imprimer, où le poser et quel QR montrer aux clients ? » |
| Hugo — boutique spécialisée, 29 ans | « Avant de télécharger, je voudrais le contenu du kit et reconnaître le QR d’inscription. » |
| Isabelle — libraire, 48 ans | « Je veux retrouver le même guide avec des consignes que je peux transmettre à ma collègue. » |

### Débat contradictoire et constats

Martine demande une affiche à imprimer ; Patrick veut tout récupérer d’un coup ; Hugo exige la liste réelle des fichiers. Le researcher rappelle que seul le bouton a été vu. E1 doit donc vérifier les fichiers avant d’annoncer leur contenu. Sur E2, Patrick accepterait une déclaration automatique ; Martine objecte qu’elle peut télécharger sans réussir à imprimer et Opérations distingue fichier disponible et installation physique.

**Points forts :** OBSERVÉ : kit accessible depuis plusieurs entrées, guide dépliable, gestes imprimer/afficher/partager et distinction des QR écrits dans le guide.

**Difficultés et limites :** OBSERVÉ : dates techniques UTC brutes. NON TESTÉ : fichiers du kit, impression, QR du support ; aucune absence de document n’est démontrée.

### Orientations et vote

- **E1 — Présenter les supports par usage et des dates lisibles :** Vérifier le kit réel puis annoncer les supports effectivement disponibles et leur usage. Rendre les dates locales lisibles. Relier les consignes d’impression, d’affichage et d’équipe aux bons documents et expliciter le rôle des QR. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#e1).
- **E2 — Déclarer prêt dès le téléchargement du kit :** Déclencher automatiquement l’état prêt au téléchargement. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#e2).

**Décision enregistrée :** E1 adopté 12–0 ; E2 rejeté 1–11. Les dates lisibles sont un correctif concret ; disponibilité et lisibilité du PDF restent des conditions de recette. Aucun téléchargement ni déclaration prêt n’est effectué ici.

## Atelier F — Utilisation en situation réelle

**Question :** Que deviennent les parcours en file d’attente, après interruption, avec un mauvais réseau ou après plusieurs semaines ?

**Écrans présentés :** [04 scanner](../visuels/captures-avant/04-scanner-mobile.png), [19 erreur](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png), [20 rechargement](../visuels/captures-avant/20-retour-rechargement-mobile.png), [15 Tombola demain](../visuels/captures-avant/15-detail-tombola-mobile.png), [17 préparation](../visuels/captures-avant/17-preparation-tombola-mobile.png).

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « La reprise devrait exposer contexte et état connu ; aucune interruption défaillante n’a été observée. » |
| Expert 2 — Accessibilité | « Tester une main, forte luminosité et aides techniques ; les captures ne prouvent pas ces usages. » |
| Expert 3 — Product Manager B2B | « Recetter le résultat incertain avec la règle métier pour éviter une nouvelle tentative ambiguë. » |
| Expert 4 — Opérations terrain | « Concilier rapidité en file et confirmation nette, sans imposer des messages longs à chaque passage. » |
| Expert 5 — Researcher et facilitateur | « Le rechargement immédiat ne prouve ni retour après semaines ni expiration ni reprise réseau. » |
| Martine — fleuriste, 63 ans | « Si le téléphone refuse de filmer, il me faut une consigne que je peux suivre sans chercher partout. » |
| Patrick — boulanger, 57 ans | « Si un client m’interrompt, je dois retrouver tout de suite où j’en étais. » |
| Nadia — salon de coiffure, 44 ans | « Entre deux rendez-vous, je dois pouvoir préparer un peu puis reprendre sans tout relire. » |
| Julien — restaurateur, 35 ans | « En service, une erreur doit dire quoi faire ensuite ; QRCode du pack ne m’aide pas. » |
| Claire — prêt-à-porter, 51 ans | « Entre deux clientes, les dates du guide me feraient perdre du temps ; un jour et une heure suffiraient. » |
| Hugo — boutique spécialisée, 29 ans | « L’échec de caméra en navigateur mérite un essai au comptoir avant de conclure que le scanner fonctionne mal. » |
| Isabelle — libraire, 48 ans | « Ma collègue doit comprendre quel QR afficher et lequel scanner sans dépendre de ma mémoire. » |

### Débat contradictoire et constats

Patrick demande qu’une panne réseau ne bloque pas sa file ; Julien et Hugo refusent une coche verte avant réponse fiable. Martine ne sait pas comment comprendre un succès provisoire, d’où son abstention F2. Isabelle et Nadia demandent surtout de retrouver contexte et consignes. F1 relit ce qui a été enregistré et ne crée pas un nouveau mode de validation. Le périmètre B1 est le résultat de transaction ; F1 concerne reprise de session, navigation et tâche restante.

**Points forts :** OBSERVÉ : rechargement courant authentifié et préparation consultable avant ouverture ; DÉDUIT : reçu et rafraîchissement de visibilité prévus.

**Difficultés et limites :** NON TESTÉ : coupure après commande, reprise après interruption/expiration, retour réel après semaines, changement de téléphone.

### Orientations et vote

- **F1 — Retrouver le contexte fiable après interruption ou absence :** Éprouver les reprises existantes ; après reconnexion, relire l’état autorisé et redonner le contexte de l’animation, la prochaine échéance connue et l’étape restante. Compléter uniquement les manques démontrés. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#f1).
- **F2 — Afficher une validation réussie hors connexion puis synchroniser :** Coche verte immédiate hors connexion, puis synchronisation automatique. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#f2).

**Décision enregistrée :** F1 adopté 12–0 ; F2 rejeté 1 pour, 10 contre, 1 abstention. Le risque de faux succès est signalé même hors vote. Les six scénarios ci-dessous restent des tests à réaliser, pas des résultats.

### Six contextes simulés à vérifier sur le terrain

| Contexte | Base réellement disponible | Mise en situation fictive et comportement attendu à tester | Ce qui reste inconnu |
| --- | --- | --- | --- |
| File d’attente en caisse | Scanner saillant O02, confirmation déduite C02 | Patrick enchaîne plusieurs participants de test ; résultat certain et action suivante lisibles sans relire un long texte. | Durée, taux d’erreur, nombre de gestes et assistance ; aucune mesure fournie. |
| Interruption pendant validation | Rechargement courant O09 seulement | Julien quitte avant confirmation, puis après envoi sans réponse ; distinguer absence de commande et reçu à relire. | Persistance réelle du contexte et réception du reçu. |
| Mauvaise connexion | État incertain dans le code C02 | Couper le réseau après une commande de test : expliquer l’incertitude puis vérifier le reçu, sans coche verte anticipée. | Fonctionnement déployé sous coupure ; aucune commande exécutée au workshop. |
| Retour après plusieurs semaines | Consignes et historique consultables ; refresh déduit C05 | Isabelle se reconnecte avec dates/droits actualisés et retrouve l’action encore pertinente. | Expiration, actualisation effective et repères humains. |
| Erreur de scan | Rejet local O04 | Martine demande le bon QR, suit la consigne de reprise et identifie qu’aucune validation n’est confirmée. | Compréhension terrain et repli caméra réelle ; QR valide non essayé. |
| Animation demain | Tombola O07, guide O08 | Nadia prépare les supports avant ouverture et explique ce qu’elle doit faire le lendemain. | Fichier imprimable, horaire exact transmis, nécessité réelle de contacter l’organisateur. |

## Atelier G — Simplification et adoption

**Question :** Localeo Pro est-elle suffisamment simple pour être utilisée régulièrement lors des animations ?

**Écrans présentés :** [03 accueil](../visuels/captures-avant/03-accueil-pro-mobile.png), [07 préparations](../visuels/captures-avant/07-preparation-mobile.png), [13 détail long](../visuels/captures-avant/13-detail-vitrines-mobile.png), [16 parcours guidé](../visuels/captures-avant/16-preparation-vitrines-mobile.png).

### Avis initiaux indépendants — simulation

| Participant | Avis avant débat |
| --- | --- |
| Expert 1 — UX Designer senior | « Essayer une hiérarchie tournée vers l’action actuelle tout en gardant l’accès direct au scanner. » |
| Expert 2 — Accessibilité | « Réduire les éléments ne doit pas supprimer libellés, repères ou voies alternatives. » |
| Expert 3 — Product Manager B2B | « Expliquer l’écart des compteurs avant de refaire leur présentation ; cause encore inconnue. » |
| Expert 4 — Opérations terrain | « L’adoption dépendra de la prochaine échéance et des supports retrouvables après absence, cas non testé. » |
| Expert 5 — Researcher et facilitateur | « Comparer sur des tâches concrètes ; ne pas attribuer de gain d’adoption à des utilisateurs non rencontrés. » |
| Martine — fleuriste, 63 ans | « Je garderais trois choses visibles : scanner, préparer la prochaine animation, lire ce qui est nouveau. » |
| Patrick — boulanger, 57 ans | « Mettez l’action du jour en haut, avec un gros message quand c’est terminé. » |
| Nadia — salon de coiffure, 44 ans | « Je regrouperais dates, consignes et supports de chaque animation au même endroit. » |
| Julien — restaurateur, 35 ans | « Scanner à portée immédiate et rappels de préparation visibles à l’approche de l’échéance. » |
| Claire — prêt-à-porter, 51 ans | « Peu de choix sur l’accueil, prochaine animation et action visibles sans descendre longtemps. » |
| Hugo — boutique spécialisée, 29 ans | « Je garderais la navigation et clarifierais les libellés et compteurs avant d’ajouter des raccourcis. » |
| Isabelle — libraire, 48 ans | « Pas de tutoriel à chaque retour ; un rappel de la prochaine échéance et l’accès aux consignes. » |

### Débat contradictoire et constats

Hugo préfère stabiliser les repères et corriger les mots avant une refonte. Nadia et Claire veulent la prochaine tâche en haut ; Patrick et Julien défendent le scanner pendant le service. G2 remplace systématiquement le grand scanner et n’emporte pas l’adhésion. G1 garde destinations et détail accessible ; Opérations s’abstient car certaines répétitions évitent des déplacements, Isabelle parce qu’elle veut vérifier ses repères. Aucun élément essentiel ne sera retiré sur la seule longueur d’une capture.

**Points forts :** OBSERVÉ : scanner et navigation déjà présents, accès kit depuis plusieurs entrées, détails complets disponibles.

**Difficultés et limites :** OBSERVÉ : détail Vitrines long avec toutes les étapes, alors que préparation propose une étape courante. HYPOTHÈSE : répétition coûteuse ; aucune gêne mesurée.

### Orientations et vote

- **G1 — Alléger les répétitions en gardant les repères et le détail accessible :** Comparer une présentation plus courte du détail, centrée sur mission, état et accès préparation/kit, en gardant l’historique et les consignes complètes atteignables. Maintenir les destinations actuelles. [Fiche](backlog-ux.md), [vote individuel](votes-et-arbitrages.md#g1).
- **G2 — Remplacer systématiquement le grand scanner par la prochaine tâche :** Remplacer le grand scanner de l’accueil par une carte tâche ; conserver le scanner uniquement dans la navigation. [Fiche](orientations-rejetees.md), [vote individuel](votes-et-arbitrages.md#g2).

**Décision enregistrée :** G1 adopté 10 pour, 2 abstentions ; G2 rejeté 2 pour, 8 contre, 2 abstentions. La prochaine action de D1/F1 peut être rendue visible sans supprimer le scanner. Aucun gain d’adoption n’est prouvé.

## Clôture de la simulation

Sept orientations adoptées et sept rejetées ; aucune ne recueille exactement six voix. Les cinq P1 sont B1/C1/D1/E1/F1 ; A1/G1 sont P2. **GO SOUS CONDITIONS** pour poursuivre vers une ouverture à 500 commerçants : les preuves manquantes ne sont pas remplacées par les avis. Les conditions, risques indépendants des votes et questions aux vrais commerçants sont dans le [rapport exécutif](rapport-executif.md). Aucun code, maquette, commit, push ou déploiement réalisé. Arrêt avant l’étape 3, conformément au prompt.
