# E85 — Parcours et recette par modèle d’animation

Depuis le catalogue, le gestionnaire choisit un modèle accessible à son organisation. Il retrouve ensuite son édition depuis la liste ou le tableau de bord. Les six fiches ci-dessous correspondent aux stratégies du moteur. L’ouverture commerciale, les droits de l’utilisateur et les commandes autorisées pour cette édition sont lus auprès du serveur. [Cadrage E85, critères E85-CA-02 à 06, 09 et 10](../../roadmap/en-cours/epic-85-parcours-organisateur-backlog.md) · [Registre des stratégies](../../../../localeo-backend/app/domaine/animation_locale/services/registre_strategies_modeles_animation.py)

## De la clôture au dernier gain

Pour chacun des six modèles, **Clôturer** présente la règle d’éligibilité du jeu, la population retenue et les situations exclues. La confirmation fige la population. **Préparer le tirage** ouvre directement l’aperçu des attributions possibles. **Confirmer le tirage** est le geste qui engage les lots. Un retour sur la fiche après une coupure retrouve l’opération et son résultat. Un gestionnaire qui consulte ces écrans en lecture seule voit l’état atteint et les dossiers consultables selon ses droits. [Maquette des quatre vues après publication](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/exploitation.html)

| Dotation effective de l’édition | À contrôler dans l’aperçu | De l’attribution à la résolution du dossier |
| --- | --- | --- |
| Coffrets réservés | Montrer le stock réservé et les éligibles requis. En cas de population insuffisante, afficher le motif du refus. | Distinguer le Coffret attribué, son envoi et la réception attestée. Le dossier indique la preuve ou le traitement autorisé qui reste à fournir. |
| Lots libres à remise externe | En mode un lot par personne, au plus autant de gagnants distincts que de personnes éligibles et d’exemplaires. Montrer les unités qui resteront sans gagnant, y compris pour une population vide. | Ouvrir la fiche du gain pour consigner sa remise effective ou le traitement motivé autorisé. Justifier les exemplaires sans gagnant au contrôle de fin. |
| Lots libres à bon numérique | Même décompte des exemplaires. Montrer le commerce de retrait prévu par la configuration. | Depuis le gain, suivre l’émission puis la consommation effective du bon. L’envoi d’un message au gagnant laisse le retrait à traiter. |

L’interface choisit cette suite à partir de la dotation enregistrée et des capacités renvoyées pour l’édition. Les chiffres, lots et modes illustrés dans les maquettes sont des jeux de recette. Après résolution des dossiers, **Terminer l’animation** conduit au bilan selon les contrôles de fin existants. [Règles d’attribution et de remise](../epic-73-animation-et-ou-coffrets/dotation-lots.md) · [Fin et archives](../epic-73-animation-et-ou-coffrets/fin-animation-archives.md)

## Passeport commerçant

| Moment | Travail du gestionnaire et résultat attendu |
| --- | --- |
| Créer et préparer | Choisir le seuil de commerces distincts et la condition « Achat requis » ou « Visite sans achat ». La condition proposée et la lecture des anciennes éditions sans ce réglage sont « Achat requis », sans minimum de dépense. Inviter les commerces sur la condition annoncée. |
| Publier | Revoir les accords et le nombre de commerces effectivement participants. Une invitation encore en attente, une condition changée qui exige de nouveaux accords, ou un seuil supérieur au nombre de commerces acceptés conduisent au point à corriger. |
| Piloter | Depuis « Participants », ouvrir un passeport pour lire les commerces comptés et leurs preuves. Un nouveau passage dans un commerce déjà comptabilisé laisse le nombre de commerces distincts inchangé. Une preuve annulée avant clôture peut faire repasser le joueur sous le seuil. |
| Clôturer et tirer | Distinguer les passeports ouverts des personnes qui atteignent le seuil dans la population figée. Chaque personne qualifiée dispose d’une chance. Depuis le résultat, ouvrir le gain et suivre la remise prévue. |

**Recette.** Sur un seuil de trois, deux visites en A et une en B donnent deux commerces. Une visite valide en C fait entrer la personne dans les éligibles. Si cette dernière preuve est annulée avant clôture, le dossier explique le retour à deux et la population du tirage reflète la correction. [Conditions et accords E56](../epic-56-validation-participation-commercants-animation/README.md) · [Maquette Passeport](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/passeport.html)

## Tombola locale

| Moment | Travail du gestionnaire et résultat attendu |
| --- | --- |
| Créer et préparer | Inviter les commerces et préparer la consigne de caisse. Le premier achat validé chez un partenaire qualifie la personne, sans minimum de dépense ni saisie d’un montant ou d’un ticket. Préparer la dotation prévue. |
| Publier | Consulter les accords, le règlement, la période et les contrôles de dotation, dont la réservation des Coffrets lorsqu’ils sont utilisés. Un blocage ouvre le commerce ou la dotation à régulariser. |
| Piloter | Distinguer les achats validés des acheteurs qualifiés. Depuis chaque total, retrouver les validations ou les personnes correspondantes. Le détail d’un acheteur peut contenir plusieurs achats pour une seule chance. |
| Clôturer et tirer | Relire le nombre de personnes éligibles, figer la population, préparer puis confirmer le tirage. Le résultat expose les bénéficiaires et les dossiers restant à traiter. |

**Recette.** Pour 27 achats validés par 18 personnes qualifiées et deux Coffrets réservés, l’aperçu indique 18 éligibles et deux attributions possibles. Un retour après confirmation retrouve les deux dossiers. Un Coffret envoyé dont la réception reste à attester demeure identifiable. Refaire le scénario avec un seul éligible pour deux Coffrets et vérifier le refus avant attribution. [Tombola locale E53](../epic-53-tombola-locale/README.md) · [Maquette Tombola locale](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/tombola-locale.html)

## Tombola publique

| Moment | Travail du gestionnaire et résultat attendu |
| --- | --- |
| Créer et préparer | Choisir l’inscription publique standard ou le mode sur place. Pour le second, préparer le lieu, le QR et le code du jour. Un commerce de retrait peut être requis par un bon numérique, indépendamment de l’inscription publique. |
| Publier | Relire les conditions d’accès dans l’aperçu. En mode standard, vérifier le lien vers le formulaire. En mode sur place, la fiche publique donne les informations pratiques et le QR de diffusion ouvre le formulaire. Le code du jour s’affiche à côté du support imprimé. |
| Piloter | Compter une chance par adresse déclarée et par édition. Distinguer les nouvelles inscriptions qualifiées des anciennes demandes en attente. Une inscription explicite à la même adresse pendant l’ouverture peut terminer une ancienne attente. Un gagnant figure déjà parmi les qualifiés. En mode sur place, retrouver le code qui change à minuit, heure de Paris. |
| Clôturer et tirer | La fermeture du formulaire arrête les nouvelles qualifications. La revue montre séparément les attentes et les inscriptions qualifiées. Le résultat permet de suivre les gains, par exemple le retrait de chaque bon chez le commerce prévu. |

**Recette.** Avec 21 personnes qualifiées et trois anciennes demandes en attente à la fermeture, l’aperçu indique 21 éligibles. Les deux gagnants de deux bons restent inclus dans ces 21. Une tentative de qualification tardive est refusée. La consommation d’un bon met à jour son dossier sans changer le nombre de qualifiés. [Gestion de la Tombola publique E74](../epic-74-tombola-publique/guide-utilisation.md) · [Maquette Tombola publique](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/tombola-publique.html)

## Chasse au trésor commerçante

| Moment | Travail du gestionnaire et résultat attendu |
| --- | --- |
| Créer et préparer | Ouvrir une demande accompagnée. Retrouver le brief, les compléments demandés, la version issue de l’import contrôlé et les missions associées aux commerces. L’écran indique qui traite la demande et quel élément le gestionnaire peut revoir. |
| Publier | Examiner l’ordre des étapes, les lieux, les preuves exigées, les missions et leurs accords, puis publier explicitement la version validée. L’espace de préparation des QR de lieux publics et la visite terrain restent accessibles séparément. Le contrôle de publication explique chaque donnée obligatoire manquante pour l’étape concernée. |
| Piloter | Lire l’étape atteinte, les récits terminés, les preuves manquantes et les joueurs qualifiés. Ouvrir le dossier à régulariser. Si un lieu est devenu inaccessible, le retrait autorisé d’une étape s’applique à tous, présente les effets et conserve l’historique des preuves. |
| Clôturer et tirer | Vérifier l’achèvement des étapes encore requises et leurs preuves. Une finale jouée avec une preuve obligatoire manquante est explicable dans le suivi. La revue figée alimente le tirage de la dotation et les dossiers de gains. |

**Recette.** Avec une mission acceptée et des contrôles de publication satisfaits, laisser un support public facultatif à imprimer et accéder à la publication. Puis, sur une chasse jouée jusqu’au bout, annuler une preuve encore requise avant clôture. Retrouver le récit achevé et la régularisation à effectuer. Un nouveau passage valide rétablit la chance unique avant le gel. [Préparation accompagnée et terrain E55](../moteur-animation/exploitation-moteur.md) · [Règles de progression et de correction](../moteur-animation/localeo_animation_engine_spec.md) · [Maquette Chasse](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/chasse.html)

## Juste Prix Local

| Moment | Travail du gestionnaire et résultat attendu |
| --- | --- |
| Créer et préparer | Inviter les commerces, faire proposer les produits et leurs prix de référence privés, puis examiner la version de chaque proposition. Définir la tolérance commune, le seuil de commerces distincts, l’exigence éventuelle de passage et le budget de mauvaises réponses par étape. |
| Publier | Vérifier les produits approuvés, les règles explicites et la dotation. L’aperçu destiné aux joueurs explique comment réussir et combien d’erreurs sont permises. Les prix de référence restent privés. |
| Piloter | Distinguer réponses correctes, passages manquants, étapes invalides et personnes qualifiées. Si un passage est exigé, estimation réussie et passage concernent le même commerce, quel que soit leur ordre. Un prix erroné après publication ouvre le traitement d’incident, avec reprise à l’identique si possible ou annulation puis nouvelle édition corrigée. |
| Clôturer et tirer | L’échéance arrête le jeu. La clôture métier confirmée ouvre le corrigé aux participants autorisés, y compris pendant l’attente du tirage. Le seuil atteint donne une chance unique. Le résultat du tirage et la remise restent accessibles séparément du corrigé. |

**Recette.** Avec un seuil de trois commerces sur cinq, épuiser les essais d’un produit. Le serveur refuse une nouvelle réponse et un scan de rattrapage sur cette étape. Trois autres produits réussis, avec leurs passages si requis, qualifient la personne. Trois étapes invalides rendent le seuil impossible. Avant clôture, le suivi protège les prix et les estimations individuelles et ne donne aucun indice « plus » ou « moins ». [Parcours et évolution commune des essais E77/E78](../epic-77-juste-prix-local/parcours-regles.md) · [Maquette Juste Prix](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/prix.html)

## Jeu des vitrines

| Moment | Travail du gestionnaire et résultat attendu |
| --- | --- |
| Créer et préparer | Inviter les commerces, examiner chaque défi d’intrus proposé et approuver sa version. Régler le seuil de vitrines, les passages éventuels et le budget de mauvaises réponses. |
| Publier | Pour chaque vitrine, distinguer l’approbation éditoriale du défi, l’attestation d’installation par le commerce et le contrôle du dispositif par l’organisateur. Une vitrine encore à contrôler mène à son dossier avant publication. |
| Piloter | Suivre les vitrines réussies, les passages attendus et les étapes invalides. Un intrus déplacé conduit à la suspension de toute l’édition. Après rétablissement à l’identique, consigner un nouveau contrôle pour chaque incident bloquant du cycle, puis confirmer la reprise dans la période autorisée. |
| Clôturer et tirer | Pour une édition reprise et clôturée, présenter la population qui satisfait le seuil, le corrigé autorisé puis le tirage applicable. Une édition encore suspendue à l’échéance oriente le gestionnaire habilité vers l’annulation. Une nouvelle édition repart avec ses propres participations. |

**Recette.** Déplacer un objet après publication et signaler deux vitrines touchées. Le premier nouveau contrôle laisse la reprise bloquée tant que l’autre incident n’est pas couvert. Après reprise dans la période, retrouver les acquis. Rejouer à l’échéance avec un incident ouvert et vérifier le refus de reprise et de clôture, même si des participants avaient déjà atteint le seuil. [Installation, incidents et reprise E78](../epic-78-jeu-des-vitrines/parcours-regles.md) · [Maquette Vitrines](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/vitrines.html)

**Essais communs au Juste Prix et aux vitrines.** En brouillon, tester 1 et 10 mauvaises réponses maximum par étape et le refus de 0 et 11. La valeur proposée est 1. Une définition historique sans paramètre conserve 1 et ses échecs terminaux. Le plafond est figé à publication. Une bonne réponse au dernier essai autorisé réussit l’étape. Une double soumission du même essai ne consomme qu’une tentative. Sur les fiches de suivi, une étape invalide, une qualification encore possible et un seuil devenu impossible ont des libellés distincts. [Règle et preuves E77/E78-ESSAIS](../epic-77-juste-prix-local/parcours-regles.md)

## Trois parcours prospectifs pour la revue de conception

Ces maquettes éprouvent les mêmes repères de navigation. Elles utilisent des exemples locaux. Les capacités à afficher dans un catalogue réel relèvent de l’epic de chaque modèle.

| Modèle | Création et publication | Déroulement et cas à examiner | Clôture, résultats et gains |
| --- | --- | --- | --- |
| Calendrier de l’Avent local · E54 | Sur la proposition d’un calendrier à cases quotidiennes, relire la programmation, le jour et le lot concernés avant publication. | Ouvrir une journée et retrouver ses participants, sa population et son résultat tout en gardant le contexte du calendrier. Examiner la reprise d’une journée interrompue sans seconde attribution. | Revoir les résultats **par journée** puis les envois encore à traiter sur l’ensemble. La dernière case achevée ouvre cette revue. Le nombre de cases, l’automatisation, les limites de gain et les conditions de clôture du parent restent à arbitrer. [Arbitrages E54](../epic-54-calendrier-avent-local/registre-arbitrages.md) · [Maquette Calendrier](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/avent.html) |
| Mots croisés assistés par l’IA · E75 | Suivre la demande accompagnée, l’import contrôlé, l’approbation de la version de grille et la concordance des fiches indices des commerces acceptés. La publication explicite contrôle les droits et le quota propres au module. | Une grille entièrement correcte **et** tous les passages requis sans achat, dans l’un ou l’autre ordre, donnent une chance. Examiner une grille correcte avec un passage manquant. En cas d’erreur dans la version publiée, retrait pour diagnostic, puis reprise identique ou nouvelle édition après annulation motivée. | Le dernier passage reçu après fermeture est refusé. Le tirage prévu utilise les personnes qualifiées au gel et mène aux dossiers de gains de la dotation. La clôture ne publie pas le corrigé de la grille. [Décisions E75](../epic-75-mots-croises-assistes-ia/README.md) · [Parcours cible](../epic-75-mots-croises-assistes-ia/parcours-regles.md) · [Maquette Mots croisés](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/mots-croises.html) |
| Escape Game assisté par l’IA · E79 | Revoir le brief, le scénario préparé hors ligne puis importé et contrôlé, les corrections et la validation avant publication explicite. | Suivre une progression personnelle sur un téléphone, en solo ou en famille, dans la commune et les commerces. Examiner comment le gestionnaire identifie la mission en cours puis la réussite finale. | La revue à l’échéance restitue la réussite narrative. Le coffre virtuel du scénario peut s’ouvrir sans créer de gain. Les règles de fin, d’incident et de récompense, dont un éventuel tirage, dépendent des arbitrages E79-ARB-05 à 08. [Cadrage et arbitrages E79](../../roadmap/a-faire/epic-79-escape-game-assiste-ia-backlog.md) · [Maquette Escape Game](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/escape-game.html) |
