# EPIC 85 — Piloter une animation de sa création à sa fin

Spécification du 25 novembre 2026. **État produit : En cours.** Le gestionnaire doit pouvoir repérer l’édition qui demande son intervention, agir dans le bon dossier et retrouver ses autres animations. Sur une tombola clôturée, cela signifie passer directement de « Préparer le tirage » aux personnes éligibles et aux lots, puis du résultat confirmé au premier gain à traiter.

| Pour travailler sur… | Document de référence |
| --- | --- |
| Le périmètre et les engagements E85-CA-01 à 19 | [Cadrage et critères d’acceptation](../../roadmap/en-cours/epic-85-parcours-organisateur-backlog.md) |
| Les règles et les écrans propres à chaque jeu | [Parcours détaillés des six modèles implémentés et des trois modèles en projet](modeles.md) |
| Les recommandations, les droits, les refus et la reprise d’une opération | [Architecture et compatibilité](architecture.md) |
| Les scénarios à exécuter et la revue avec des gestionnaires | [Matrice de recette et lots](recette.md) |
| Les comportements implémentés et les vérifications locales | [Bilan par critère](verification-livraison.md) |
| Manipuler les écrans | [Fiche large](../../../livrables/design/animation/epic-85-parcours-organisateur/fiche.html) · [Parcours par modèle](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/index.html) · [Accès direct au suivi, à la clôture, au tirage et aux gains](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/exploitation.html) · [Planches](../../../livrables/design/animation/epic-85-parcours-organisateur/creation-cloture/planches/index.html) |

## Commencer sa journée

Le tableau de bord répond à « Quelle édition demande mon attention ? ». Chaque entrée d’intervention identifie l’édition et la commune, l’étape métier, le motif vérifié et le geste accessible. Une attente d’accord commerçant précise qui peut agir dès que cette information est connue. Un incident renvoie à son dossier quand la source l’identifie. Une date échue invite à contrôler la clôture selon les capacités reçues. Les archives se consultent depuis « Mes archives ».

La liste des animations répond à « Où est mon édition ? ». Elle s’ouvre sur les éditions accessibles et propose **Préparations** à côté de **Mes archives**. Préparations ouvre les travaux enregistrés avant la création définitive d’un brouillon. Depuis une liste filtrée, le nom ouvre la fiche et son action ouvre directement la destination annoncée. Le responsable qui peut publier arrive à la même revue depuis la ligne, le tableau de bord ou l’en-tête. Un lecteur peut consulter les faits autorisés. Une édition sans intervention connue reste trouvable dans sa liste, avec sa situation réelle.

**Exemple de reprise.** La gestionnaire filtre les éditions de sa commune, ouvre une publication en attente et retrouve l’invitation concernée. Après sa relance, le contrôle continue d’indiquer l’attente d’un accord. De retour dans sa liste, elle examine un incident sur une seconde édition, puis prépare le tirage d’une troisième. Chaque retour retrouve les critères, la page et l’entrée d’origine. Si une action fait sortir une ligne du filtre, le retour l’explique et replace le focus dans les résultats restants.

## Lire et utiliser la fiche

Sur ordinateur, le nom, la commune et la période identifient l’édition. La frise en lecture seule présente les étapes confirmées par le serveur. Elle indique en toutes lettres l’étape actuelle et distingue les étapes franchies et à venir. Le statut métier reste visible même si la frise est indisponible. Sur téléphone, le statut et le sélecteur de rubriques restent distincts. Le titre de la zone de travail désigne la **rubrique consultée**. Une gestionnaire peut ainsi lire « En cours » tout en examinant « Validations ».

L’en-tête porte le prochain geste permis pour l’édition. Quand la destination est déjà ouverte, la zone de travail porte l’action précise au point de décision, à côté de ses effets. Une même commande apparaît une seule fois dans cette vue. Les verbes annoncent le geste réel. « Voir les participants », « Vérifier la clôture » et « Préparer le tirage » ouvrent une lecture. « Publier l’animation », « Confirmer la clôture » et « Confirmer le tirage » engagent l’opération présentée.

Depuis la fiche, une action ou un lien vers un dossier atteint sa destination en une activation. Le repère d’étape se maintient pendant les consultations secondaires. L’ouverture ordinaire d’une édition publiée ou en cours mène à Participation. Depuis cette rubrique, **Bilan provisoire** donne accès aux résultats et aux objectifs autorisés pendant le déroulement. Un lien explicite vers une rubrique ou un dossier autorisé prévaut sur la destination par défaut. [Règles d’entrée de la fiche](../epic-73-animation-et-ou-coffrets/parcours-organisateur.md)

## De la création à l’archive

| Situation | Informations et geste du gestionnaire | Résultat observable et suite |
| --- | --- | --- |
| Choix du modèle | Depuis le catalogue de la commune, lire la mécanique et le mode d’accès. Choisir une création autonome ou transmettre la demande accompagnée prévue pour ce modèle. | La création confirmée identifie l’édition et ouvre sa préparation. La demande transmise affiche son reçu et sa suite connue. Le lien vers l’édition devient disponible lorsqu’elle existe et que son accès est permis. |
| Préparation | Reprendre le travail à l’élément utile. Voir les prérequis satisfaits, les points en attente, l’acteur concerné et le lien vers la correction. Distinguer préparation terrain, invitations et conditions de publication. | Après modification, la revue relit le contrôle concerné. Les informations déjà saisies sont conservées. Les préparatifs facultatifs restent accessibles. |
| Revue et publication | Lire la présentation destinée au public, la période, les contrôles et leurs motifs. Le responsable peut corriger un blocage puis revenir au même contrôle. « Publier l’animation » engage la publication lorsque le serveur l’autorise. | La réussite affiche l’édition publiée et la période. Le suivi s’ouvre directement. Lors d’un refus, le motif actualisé reste associé au contrôle concerné. |
| Déroulement | Lire l’activité et les faits propres au jeu. Un indicateur ouvre la population qu’il mesure. Depuis la liste, ouvrir un participant, une validation ou un incident. Voir la preuve disponible, l’état et le geste permis. | Après un geste, relire le dossier et les agrégats affectés. Un gestionnaire peut revenir à sa recherche ou retrouver la prochaine intervention. Les dossiers sensibles conservent leurs restrictions de visibilité. |
| Revue de clôture | Voir ce que la fermeture interrompt, la règle d’éligibilité, les décomptes disponibles et les cas à examiner. Ouvrir un dossier, revenir, puis annuler ou choisir « Confirmer la clôture ». Une clôture anticipée, lorsqu’elle est autorisée, reste secondaire et annonce sa conséquence. | La clôture confirmée ferme les participations et validations selon le modèle et fige la population. Le reçu distingue ce qui est figé de ce qui reste à traiter. Selon les capacités, il propose le tirage, un résultat existant ou la fin. |
| Tirage applicable | « Préparer le tirage » ouvre la revue dans l’édition clôturée. Présenter la population figée, les lots ou exemplaires mobilisables, les conditions de dotation et le nombre d’attributions possibles lorsqu’il est établi. Un manque de financement, une population vide ou une opération en cours reçoit son état explicite. | Revenir ou annuler la revue préserve les lots. « Confirmer le tirage » lance la commande appropriée. Le résultat distingue attribution confirmée, traitement en cours et réponse à vérifier. Une réouverture retrouve l’opération ou son résultat. |
| Gains et remises | Depuis les attributions, ouvrir un dossier. Le gestionnaire voit le lot, la situation de l’envoi, de la remise ou du retrait, la prochaine action autorisée et son acteur lorsqu’il est établi. Les données du bénéficiaire suivent les droits du lecteur. | Le retour retrouve les dossiers à résoudre et leurs statuts relus. Une notification envoyée et une remise enregistrée ont des libellés distincts. Un dossier déjà résolu reste consultable dans l’historique. |
| Fin, bilan et archive | Ouvrir les contrôles de fin. Chaque blocage mène au dossier concerné, y compris une unité sans gagnant à justifier. Lorsque la capacité est ouverte, « Terminer l’animation » fige la gestion selon E73. « Archiver l’animation » est une décision ultérieure explicite. | Le bilan final et l’historique sont consultables selon les droits. L’archive disparaît du tableau de bord opérationnel et reste accessible dans « Mes archives ». Les gains acquis et les justificatifs conservent leurs règles d’accès. |

La date, la consultation d’une rubrique et le succès d’un envoi ne font pas avancer à eux seuls l’édition. Le tirage et les remises sont des tâches de la phase de clôture. Une édition annulée affiche son état propre et les lectures autorisées. [Cycle et règles de fin E73](../epic-73-animation-et-ou-coffrets/fin-animation-archives.md)

### Préparer un brouillon et sa dotation

Le modèle peut être corrigé tant que seul son choix a été fait. La première modification métier fixe le choix pour la préparation en cours. Une préparation enregistrée se reprend avec son modèle. **Retour aux animations** permet de retrouver le catalogue avec la protection de saisie habituelle. **Précédent** reste un geste local au formulaire.

Dans la création, **Comprendre les étapes** ouvre l’aide depuis le bouton « ? ». L’aide présente les accords seulement pour les modèles qui sollicitent les commerçants. La confirmation **Créer le brouillon** précise que la création n’envoie aucune invitation et ne publie rien.

Dans la création et la configuration d’un lot libre remis hors Localeo, **Lot à gagner** regroupe le libellé et la quantité initiale de 1. **Remise au gagnant** rassemble le responsable et les consignes de retrait. L’aperçu aide à vérifier l’ordre d’attribution. Une validation refusée préserve la saisie et le retour à la liste des lots restaure le focus.

## Retrouver les rubriques actuelles

Les regroupements ci-dessous organisent les liens et le contenu. Les tâches principales et les dossiers signalés s’ouvrent directement. Un ancien accès conserve l’édition et rejoint la destination autorisée correspondante. [Navigation](../../../../localeo-animation/src/app/components/AnimationDetailNavigation.tsx)

| État de l’édition | Rubriques utiles selon le modèle et les droits |
| --- | --- |
| Brouillon, configurée ou prête à publier | **Préparation** et **Publication**. Préparation donne accès aux objectifs, à la date annoncée du tirage, aux invitations et au terrain applicables ainsi qu’aux contenus à préparer. Publication réunit **Revue de publication** et **Supports de diffusion**. |
| Publiée ou en cours | **Participation**, **Exploitation**, **Publication**, **Communication** et **Clôture**. La revue de clôture est accessible depuis les rubriques dès la publication. La confirmation et la possibilité de clore avant l’échéance dépendent des capacités du serveur. Les résultats et objectifs courants se consultent via **Bilan provisoire** dans Participation. |
| Clôturée | **Tirage** pour les éditions concernées, accès aux gains et aux dossiers de fin, et **Bilan**. La clôture dirige vers la suite applicable au jeu. |
| Terminée ou archivée | **Bilan** en premier, puis les lectures historiques autorisées. |
| Annulée | Résumé de l’annulation et lectures autorisées. |

Sur ordinateur, les vues d’une rubrique apparaissent dans une bande distincte qui nomme leur rubrique parente. Sur téléphone, un sélecteur unique groupe les destinations sous leur rubrique parente. La frise reste un repère d’état indépendant.

Participation réunit la liste des participants, les qualifications et, pour les modèles concernés, les validations. Une participation et une preuve gardent leurs propres détails et filtres. Les incidents actifs apparaissent avant la liste. Dans Communication, le quota et les messages envoyés aux participants précèdent les outils complémentaires. « Nouveau message » ouvre le formulaire avec aperçu et protection de la saisie. Les messages reçus des habitants conservent leur propre destination.

**Exploitation** rassemble **Réglages d’exploitation** et **Configuration publiée**. Les réglages présentent les dates et inscriptions, le contact public et la date annoncée du tirage selon le modèle et les actions permises par le serveur. La configuration publiée se consulte en lecture seule. Après clôture, la date annoncée se retrouve dans Tirage lorsqu’il s’applique. Le retrait du contact public reste accessible via Publication selon les capacités reçues.

Les supports peuvent être préparés en brouillon selon les droits existants. L’usage public d’un lien ou d’un QR de diffusion dépend de la visibilité de l’édition et de sa configuration publiée. Le QR terrain reste accessible depuis sa préparation. Le contrôle facultatif de visuel reconnaît une illustration personnalisée du flyer active sur cette édition ou un visuel déjà déclaré dans sa configuration. Relire le contrôle après ajout ou retrait confirmé. [Règle du visuel et lecture du flyer](../epic-73-animation-et-ou-coffrets/flyers-contextualises.md#illustration-personnalisée)

Clôture expose les indicateurs disponibles, les blocages éventuels et la confirmation. Pendant le gel par lots du Juste Prix et du Jeu des vitrines, seul l’avancement confirmé est présenté. Pour les lots libres, si le serveur autorise le tirage avec zéro éligible et zéro gagnant possible, la confirmation s’intitule « Enregistrer un tirage sans gagnant ». La règle d’attribution des coffrets reste celle du moteur. Bilan présente la période, les données disponibles, la progression comparable et l’export PDF ou CSV. La fin de gestion marque le passage au bilan définitif.

| Espace de travail | Identifiant actuel → contenu proposé | Accès utile en situation |
| --- | --- | --- |
| Préparation et Exploitation | `assistant` → préparation guidée · `configuration` → réglages du brouillon ou configuration publiée · `participations` → invitations commerçants · `preparation` → terrain · `exploitation` → réglages d’exploitation | Ouvrir la correction ou l’accord depuis son contrôle. Les anciennes destinations de préparation mènent aux lectures autorisées après publication. L’ancien accès aux paramètres dans Participation rejoint Exploitation. |
| Publication ou clôture | `workflow` → revue de publication, revue de clôture ou bilan selon l’état | Ouvrir la publication avant clôture, la clôture lorsqu’elle est recommandée ou confirmée, et le bilan pour une édition terminée, archivée ou annulée. |
| Supports de diffusion | `flyer` → Flyer · `diffusion` → Liens et QR de diffusion | Retrouver chaque outil dans **Publication → Supports de diffusion**, y compris après publication. Depuis le contrôle de visuel, **Ajouter un visuel** ouvre l’éditeur d’illustration du flyer et conserve le retour à la revue. |
| Participation | `live` → suivi de la participation · `participants` → participants · `validations` → validations | L’indicateur mène à sa liste déjà filtrée. Un incident identifié mène à sa situation métier. |
| Communication | `communication` → messages aux participants · `messages-habitants` → messages habitants · `actualites` → actualités | Avant publication, les entrées qui permettent de préparer une actualité ou un message rejoignent Préparation. Une destination réservée au suivi explique quand elle s’ouvre et propose une rubrique utile dans la même édition. |
| Tirage et gains | `tirage` → préparation, état ou résultat · `gains` → gains et remises | Après fermeture effective, la recommandation « tirages » ouvre la rubrique. Avant cette fermeture, le lien direct explique le prérequis et propose la revue de clôture lorsqu’elle est permise. Le résultat confirmé donne accès aux gains. |
| Fin et bilan | `fin` → dossiers de fin et archivage · `bilan` → bilan disponible à la phase consultée · `bilan-objectifs` → objectifs · `audit` → historique autorisé | Un contrôle de fin ouvre le dossier. Le bilan indique la période et le caractère provisoire ou final de la lecture. En brouillon, l’ancien lien vers les objectifs rejoint leur réglage. |

En cas de destination retirée au rôle ou inapplicable au modèle, la fiche explique l’indisponibilité et offre un retour autorisé. Elle protège toute saisie en cours avant changement de cible. En lecture seule, le gestionnaire retrouve les informations permises et le résultat d’une opération déjà effectuée.

### Passer d’une vue à l’autre dans une rubrique

Dès qu’une rubrique contient plusieurs vues, sa navigation locale les nomme toutes, y compris la première. Après clôture, **Fin et archivage** est accessible dans **Tirage** pour les jeux qui le prévoient et dans **Clôture** pour les autres. **Tirage** donne aussi accès à **Tirage au sort** et **Gains et remises**. La première entrée de Communication est **Messages aux participants**. Bilan regroupe les résultats, objectifs, origines des inscriptions, commentaires, comparaison et historique au même niveau. L’état courant reste repérable pendant ces consultations. Sur téléphone les destinations restent accessibles dans un seul sélecteur. Les droits, la lecture seule et l’applicabilité du tirage déterminent les entrées proposées.

Une recommandation du bandeau mène à la même revue que le raccourci placé auprès d’un blocage. Par exemple, « Vérifier la clôture » depuis un ancien lien de tirage ouvre la revue de cette édition. La confirmation définitive se trouve dans le formulaire qui explique ses conséquences. En présence d’un tirage confirmé avec zéro gagnant, Gains et remises en rend compte. Les lots sans gagnant ont leur propre dossier de justification.

Dans **Gains et remises**, le détail d’un lot externe attribué dont la remise
reste à déclarer présente **Déclarer la remise du lot** en premier lorsque
l’action est autorisée. La remise effective est enregistrée après
**Confirmer la remise**, avec un motif et une date passée facultative.
**Ajouter un suivi** ouvre une saisie secondaire pour consigner un événement.
Les deux formulaires s’ouvrent sur demande, chacun à son tour. Leur annulation
ramène aux actions du gain avec le focus sur la commande utilisée.
Les bons numériques se remettent par QR ou PIN.

### Retrouver une animation dans la liste

La barre au-dessus des résultats réunit recherche, choix de vue et filtres. Les critères appliqués peuvent être retirés individuellement. Une vue enregistrée s’applique depuis le sélecteur. **Enregistrer les filtres actuels** ouvre la création. **Gérer les vues** présente les vues privées et partagées et les actions autorisées pour chacune. Le remplacement des filtres d’une vue est explicite. **Cloner** s’affiche sous le nom des éditions éligibles dans Animations et Archives. La prochaine action reste dédiée au travail sur l’édition en cours. La sélection des brouillons fait apparaître les actions groupées. Le retour d’une consultation ou du clonage retrouve les critères, la page et la ligne concernée. Sur les jeux de recette, deux éditions complètes doivent être visibles à 1280 × 800 et la première avec sa prochaine action à 390 × 800.

### Repérer les interventions du jour

Le tableau de bord de la commune ouvre sur **À traiter aujourd’hui**, avant le choix de la période et les mesures d’activité. Il présente jusqu’à trois recommandations dans l’ordre du serveur. Chaque intervention nomme l’édition, le motif connu et le geste disponible. Une lecture confirmée sans intervention affiche « Aucune intervention à traiter aujourd’hui ». La première action reste visible à 390 × 800 et à 1280 × 800.

La liste et le bandeau partagent le libellé du statut métier. Le gestionnaire peut consulter une autre rubrique tout en repérant l’étape actuelle. Pour une clôture attendue, la date de fin prévue accompagne l’accès à la revue. Une recommandation liée à un seul dossier ouvre celui-ci. Si plusieurs dossiers restent à traiter, elle ouvre la liste filtrée de l’édition. Revenir à la liste ou au tableau de bord restitue le point de départ.

Avant l’attribution, Fin et archivage distingue les lots encore attribuables des lots définitivement sans gagnant. Seuls les seconds peuvent faire l’objet d’une justification lorsqu’elle est autorisée. Le reçu de publication présente la date effective si elle est connue et un accès au suivi autorisé. La ligne d’un participant propose sa consultation et réserve la suppression au menu de la ligne. Le bilan précise si le tirage est à venir, en cours ou confirmé. Il garde un zéro confirmé et signale explicitement une lecture indisponible.

## Contenu commun des écrans de gestion

| Composant | Règle de présentation et d’usage |
| --- | --- |
| Pictogrammes | Reprendre les pictogrammes de gestion du portail pour identifier les mesures, les états et les actions dans les onglets. Associer chaque pictogramme à un libellé visible et conserver le même sens sur téléphone. Les icônes d’accompagnement sont ignorées par les lecteurs d’écran. |
| Métriques | Placer les valeurs liées à la tâche avant la liste concernée. Nommer l’unité, la période ou la population. Distinguer « inscrits », « qualifiés » et « gains remis ». Un zéro confirmé s’affiche comme zéro. Une lecture indisponible affiche son état. Le lien de détail reprend exactement le périmètre annoncé. |
| Recherche et filtres | Conserver le même ordre de lecture, un libellé visible par champ, les critères actifs et un moyen de les effacer. À la modification d’un filtre, revenir à la première page des résultats. Une requête ancienne arrivée en retard ne remplace jamais les résultats de la recherche courante. |
| Tableau | Donner à chaque colonne un en-tête. Mettre l’identité du dossier en premier, puis les preuves ou valeurs comparables, l’état en texte et son action. Un lien identifiable ouvre le dossier au clavier. Les colonnes métier varient avec le modèle, leur ordre d’usage reste stable. |
| Pagination | Sur une liste paginée de gestion, présenter plage affichée, total filtré, page et commandes disponibles. Une dernière page disparue après une action ramène à la dernière page valide. Une lecture à curseur sans total conserve des commandes adaptées à son contrat. L’écart éventuel au CA-06 doit être résolu pour toute liste incluse dans sa recette. [Contrats et périmètre des totaux](architecture.md) |
| Retour et fraîcheur | Conserver édition, recherche, filtres, page et point de focus entre liste et dossier. Afficher la date d’observation si elle est fournie et utile à la décision. Une action réussie relit les seuls résultats affectés. |
| Lecture partielle ou en erreur | À la première lecture, signaler le chargement. Après une erreur, conserver la saisie et identifier les dernières données affichées le cas échéant. Distinguer « aucune participation », « aucun résultat pour ces filtres », accès refusé et incident de lecture. Un seul réessai pour la zone affectée, tel que « Réessayer le chargement des participants ». Une relecture ne rejoue aucune écriture. |

Appliquer les [conventions de gestion communes](../../architecture/transverse/conventions-backoffice.md) aux participants, validations, invitations, gains, historique et listes transversales touchées. Les photos, références confidentielles et justificatifs ne sont affichés que dans les dossiers et phases qui les autorisent.

## Téléphone, clavier et arbitrage d’usage

La proposition à évaluer conserve sur téléphone l’identité de l’édition, son étape, le titre consulté et le geste principal. « Toutes les rubriques » ouvre en une fois la liste des destinations autorisées, regroupées sous des intertitres. Le choix d’une destination la charge directement. La fermeture rend le focus au bouton d’ouverture. Sur ordinateur, l’espace disponible sert d’abord au travail en cours, notamment à la comparaison des colonnes. Les destinations fréquentes restent accessibles par des liens nommés.

À 320 et 390 px et avec texte agrandi à 200 %, les lignes se replient en couples libellé–valeur si la comparaison en colonnes ne tient plus. Chaque action garde le contexte de sa ligne. Le repère se compacte en une étape nommée et sa position. Le focus reste visible, l’ordre de tabulation suit la tâche, la sélection se lit indépendamment de la couleur et les retours de commande sont annoncés. Après annulation, le focus revient au déclencheur. Après confirmation, il atteint le reçu ou son titre.

**Décision à valider en usage.** Comparer cette entrée secondaire avec les raccourcis et le sélecteur complet E73 sur trois tâches : retrouver les messages habitants, reprendre un gain, revenir à une liste filtrée. Relever détours, hésitations, erreurs d’édition et compréhension de l’effet avant confirmation. Si « Toutes les rubriques » masque un geste quotidien, donner un accès direct à ce geste à l’endroit où le besoin apparaît. Les maquettes illustrent la proposition avec des données fictives. La validation repose sur la [recette comparative](recette.md).
