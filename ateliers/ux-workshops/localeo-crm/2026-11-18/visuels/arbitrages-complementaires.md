# Revue contradictoire et arbitrages complémentaires — étape 3

**Revue simulée par IA, le 19 novembre 2026.** Les douze profils ont été confrontés aux maquettes rendues. Les réactions, préférences et réserves sont fictives ; aucune personne réelle n’a été interrogée. Les agents terrain/pilotage ont aussi produit certains fragments : cette limite d’auto-relecture est déclarée. La revue experte et l’intégration finale complètent cette lecture sans lui donner une valeur de test utilisateur.

## Périmètre et gouvernance

Seules UX01–UX05, P1 adoptées à 7 voix ou plus, sont maquettées. Les votes d’orientation de l’étape 2 restent inchangés : 12, 8, 12, 12, 12 POUR sur 12. UX06–UX10 sont P2, UX11–UX13 sont rejetées ; aucun de ces lots n’est mis en œuvre visuellement. Le détail des responsabilités à la création ne remplace pas le formulaire complet.

La galerie montre 12 scènes, chacune avec un HTML statique et des PNG bureau/mobile. Les seuls comportements sont des liens de présentation, la bascule comparative et un volet de lecture ; aucun enregistrement, appel API ou état commercial n’est implémenté. Les quinze captures réelles de l’étape 1 sont conservées, sans retouche supplémentaire.

## Préférences simulées par orientation

Les réponses ci-dessous ne sont **pas un nouveau vote d’adoption** : APRES = préférence visuelle, AVANT = préférence pour l’existant, RESERVE = comparaison non tranchée. Elles ne modifient ni la majorité de l’étape 2 ni les conditions de recette. Une préférence ne signifie pas absence de réserve d’usage.

| Orientation | Vote étape 2 | APRÈS | AVANT | RÉSERVE |
| --- | --- | --- | --- | --- |
| UX01 | 12 / 12 | 12 | 0 | 0 |
| UX02 | 8 / 12 | 5 | 0 | 7 |
| UX03 | 12 / 12 | 12 | 0 | 0 |
| UX04 | 12 / 12 | 11 | 0 | 1 |
| UX05 | 12 / 12 | 10 | 0 | 2 |


**UX02 n’obtient pas une préférence majoritaire pour la maquette** : 5 APRÈS et 7 RÉSERVE. Les définitions, la portée des filtres et le coût de lecture mobile doivent être éprouvés avant de retenir son agencement. UX04 conserve une réserve de longueur ; UX05 deux réserves sur la continuité réelle et la densité mobile. La revue ne prétend pas qu’une image réduit effectivement les oublis.

## Ajustements retenus après confrontation

| ID | Constat de revue | Arbitrage final | Périmètre |
| --- | --- | --- | --- |
| AJ01 | Les liens et périodes des compteurs Équipe se touchaient. | Périodes passées sur une ligne séparée ; même périmètre, mêmes nombres. | UX01, présentation corrigée |
| AJ02 | La planche de création pouvait laisser croire que le reste du formulaire était supprimé. | Bandeau explicite : extrait ciblé responsabilités ; nom, commune et coordonnées conservés hors planche. | UX03 ; UX06 reste exclue |
| AJ03 | Les deux sauvegardes du compte rendu rendaient l’ordre ambigu. | Deux états successifs nommés : compte rendu à enregistrer, puis enregistré/RDV réalisé. Prochaine action non créée ; explication ajoutée explicitement au compte rendu. | UX05, précision de la suite déjà adoptée |
| AJ04 | Responsable du dossier semblait filtrer toutes les catégories de risques. | Texte de portée explicite : filtres des dossiers ; autres compteurs équipe et filtres propres à chaque liste. | UX02, unités et portées clarifiées |
| AJ05 | La liste complète des risques repoussait les résultats sur smartphone. | Situation active en volet compact sur mobile ; autres situations restent accessibles en dépliant. | UX02, même contenu et navigation |
| AJ06 | Un choix radio était séparé de son texte sur smartphone. | Alignement du choix et du libellé conservé sur la même ligne. | UX04, lisibilité corrigée |


L’expert a réexaminé les rendus corrigés de UX01 Équipe, UX03 création, UX05 compte rendu et UX02 mobile : les clarifications AJ01–AJ04 sont constatées, la réserve de longueur mobile reste ouverte. Les réponses initiales n’ont pas été réécrites pour fabriquer une adhésion après correction.

## Arbitrages ouverts et nouveau vote

**Aucun changement substantiel de l’orientation n’a été retenu : aucun nouveau vote d’orientation nécessaire.** La distinction des trois responsables, le rattachement explicite, l’absence de tâche silencieuse et la vérification de l’existant sont conservés. Les clarifications visuelles ne créent ni obligation de champ, ni automatisation, ni transfert global. Si une suite impose un délai commun d’inactivité, modifie les règles de comptage, fusionne les rôles ou généralise une obligation de prochaine action, elle devra être soumise à un nouveau vote.

Pour UX02, « sans interaction récente » et « sans évolution » restent sans valeur tant qu’aucun délai n’est choisi. La définition affichée de dossier sans prochaine action et le traitement des pauses sont des exemples à valider avec le métier, pas une nouvelle règle appliquée au CRM. Les compteurs de catégories ne sont pas additionnés. Les totaux fictifs 2 retards / 3 actions du jour / 1 RDV correspondent aux lignes visibles ; le RDV du 26 novembre est hors de la fenêtre du 19 au 25 de l’accueil.

La longueur des vues mobile demeure une réserve de conception, notamment agenda et compte rendu. Cette dernière planche juxtapose deux états pour revue ; elle ne prescrit pas un écran unique de deux mille pixels. Une prochaine itération peut séparer les états sans étendre les règles métier. Le rendu responsive ne remplace pas la recette mobile réelle, restée incomplète à l’étape 1.

La qualification n’est pas refondue : seules les responsabilités sont clarifiées dans UX03. Aucun gain de calcul, de recherche de doublons ou de qualification ne peut être revendiqué. Les rendez-vous sont illustrés de bout en bout, mais modification, annulation, réception des rappels et collaboration multi-compte restent à vérifier dans l’application.

## Réponses aux six questions

### Expert UX B2B — E1

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | OBSERVÉ SUR MAQUETTE : UX01 rassemble trois nombres et explique directement qu'une file personnelle vide ne décrit pas le portefeuille collectif ; c'est un repère plus explicite que les trois blocs vides de la capture 01. |
| Les prochaines actions sont-elles plus visibles ? | OBSERVÉ SUR MAQUETTE : UX01-équipe place retards puis journée puis rendez-vous, avec noms et heures ; les liens des compteurs sont toutefois collés aux périodes, ce qui nuit à leur lecture. |
| La qualification est-elle plus simple ? | UX03 distingue visuellement relation, dossier et action, puis montre l'effet ciblé de l'affectation ; la scène de création doit être annoncée comme extrait, car elle ne représente pas les autres champs de la capture 09. Aucune amélioration globale de qualification P2 n'est évaluée. |
| Les rendez-vous sont-ils plus faciles à gérer ? | UX05-confirmation propose deux accès lisibles au rendez-vous et au bon jour, puis une préparation contextualisée ; dans le compte rendu, l'enregistrement principal et les deux suites ont besoin d'un état indiquant ce qui est sauvegardé. |
| Les risques d’oubli sont-ils réduits ? | UX04-suivi explique précisément pourquoi Association commerçante reste sans prochaine action alors qu'Animation centre-bourg en possède une ; cette explication résout visuellement l'ambiguïté de présentation de la capture 14, sans démontrer la règle réelle. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère les présentations après sur bureau pour leurs portées et récapitulatifs explicites, sous correction des détails de lecture et de sauvegarde ; la page mobile UX02 reste longue avant le premier dossier. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | Le résumé et le message de portée sont plus compacts et plus explicites que les trois zones vides avant ; séparer les liens des périodes dans la scène équipe. |
| UX02 | APRES | La liste active, sa définition et ses deux résultats sont réunis sur bureau ; ma préférence concerne la présentation proposée, car aucune vue globale avant stabilisée ne permet une comparaison fonctionnelle. |
| UX03 | APRES | Le récapitulatif montre prospect modifié, dossier et action conservés ; la scène création doit porter une mention d'extrait ciblé pour préserver le périmètre. |
| UX04 | APRES | Le choix prospect ou dossier puis le résumé d'enregistrement donnent un contexte absent de la capture d'action avant ; le second dossier reste clairement non couvert. |
| UX05 | APRES | Les accès vers la date précise et la note de préparation rendent la continuité proposée lisible ; préciser les étapes de sauvegarde du compte rendu sans ajouter de fonction. |


Réserves conservées :

- L'inspection d'images ne teste aucun lien ni enregistrement.
- Le premier dossier de UX02 mobile apparaît vers 1000 pixels de hauteur ; la densité devra être éprouvée sur téléphone.

### Expert CRM / Sales Operations — E2

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | UX02 sépare six prospects actifs, quatre dossiers ouverts et deux dossiers sans prochaine action ; la note de non-addition des catégories protège la lecture, mais ces nombres fictifs ne prouvent pas l'exhaustivité du CRM. |
| Les prochaines actions sont-elles plus visibles ? | UX04 conserve deux dates et un responsable d'action nommé ; le périmètre Animation centre-bourg figure avant et après la confirmation, ce qui évite de confondre relation globale et dossier. |
| La qualification est-elle plus simple ? | La qualification commerciale reste hors du changement illustré ; UX03 clarifie la responsabilité du dossier sans imposer un score, un contact complet ou l'identité des propriétaires. |
| Les rendez-vous sont-ils plus faciles à gérer ? | Le compte rendu obligatoire pour réaliser est cohérent avec les repères de code disponibles ; la prochaine action est une proposition séparée et aucune création automatique n'est annoncée. La conservation d'une explication sans action doit préciser sa portée de sauvegarde. |
| Les risques d’oubli sont-ils réduits ? | UX02 garde Délai à choisir pour inactivité et stagnation, ce qui évite d'ériger un seuil arbitraire en règle ; la définition action future ouverte et les exclusions des pauses sont encore des hypothèses métier, y compris pour les actions en retard. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère les présentations après à titre de conception, car unités, propriétaires et rattachements sont plus explicites ; la préférence ne vaut pas accord métier sur les définitions de risque. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | Les périodes et la portée précèdent la lecture des nombres, et les lignes détaillées donnent un contexte aux totaux fictifs. |
| UX02 | APRES | Les unités et recouvrements sont visibles ; maintenir la confirmation métier des règles avant toute implémentation, notamment dossier avec tâche déjà en retard. |
| UX03 | APRES | L'affectation ne propage pas le changement du prospect aux engagements ; aucune transmission globale de UX09 n'est ajoutée. |
| UX04 | APRES | Les deux dossiers du même prospect ne sont pas artificiellement couverts par une tâche unique. |
| UX05 | APRES | Réalisation, compte rendu et prochaine action restent distincts ; la recette des fonctions existantes demeure nécessaire. |


Réserves conservées :

- Les règles d'exclusion des pauses justifiées et de tâche future ouverte ne sont pas validées par cette maquette.
- Le manifeste présente correctement UX05 comme continuité non prouvée ; aucune absence de capacité n'est démontrée.

### Expert responsable commercial — E3

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | Sur UX01-équipe, je repère deux retards, trois actions du jour et un rendez-vous sur la période annoncée ; l'accueil personnel explique immédiatement pourquoi ses zéros ne décrivent pas l'équipe. |
| Les prochaines actions sont-elles plus visibles ? | La scène équipe donne les noms, heures et dossiers dans les lignes, et UX04 affiche qui prépare la démonstration ; la priorité d'action est plus facile à déduire visuellement, sans temps de réalisation mesuré. |
| La qualification est-elle plus simple ? | Le prospect non attribué reste visible alors que le premier dossier est porté par Léa ; le choix explicite de Camille indique que la relation et l'opportunité peuvent appartenir à deux collègues. Aucun gain sur le calcul de qualification n'est revendiqué. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La confirmation réunit date, responsable, prospect et préparation ; les liens vers le rendez-vous et la semaine sont prometteurs pour le travail commercial, mais le compte rendu doit éviter de laisser croire qu'une prochaine action est déjà enregistrée. |
| Les risques d’oubli sont-ils réduits ? | La liste des dossiers sans action et l'alerte expliquée sur le deuxième dossier donnent un point de départ à la revue commerciale ; les seuils de stagnation restent à décider et le fonctionnement réel n'est pas testé. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère les cinq présentations après pour une revue sur ordinateur, avec réserve sur la longueur mobile et sur la lisibilité de la sauvegarde de la suite du rendez-vous. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | La journée et le collectif ont chacun une portée identifiable, sans imposer tous les indicateurs au commercial individuel. |
| UX02 | APRES | Deux dossiers à traiter sont présentés avec responsables et accès explicites ; les totaux fictifs ne sont pas un état réel du portefeuille. |
| UX03 | APRES | Le récapitulatif montre qui reprend la relation et qui garde les engagements, sans affectation automatique. |
| UX04 | APRES | Le résumé final montre exactement le dossier couvert et celui qui reste à suivre. |
| UX05 | APRES | Préparation et suite commerciale se lisent dans le contexte du même prospect ; la séparation des sauvegardes reste à préciser. |


Réserves conservées :

- Cette préférence ne suffit pas à autoriser dix commerciaux à utiliser le produit en autonomie.
- Les scènes utilisent des données fictives différentes des captures avant ; aucun gain de productivité chiffré ne peut en être tiré.

### Expert onboarding / accessibilité — E4

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | Le message personnel vide de UX01 explique la portée en langage courant et propose un prochain geste ; la scène équipe doit séparer les liens des légendes de période pour une lecture moins compacte. |
| Les prochaines actions sont-elles plus visibles ? | Les mots En retard, Préparation interne et Responsable de l'action apportent des repères textuels indépendants de la couleur ; les contrôles gris étant inactifs dans la maquette, leur ergonomie interactive n'est pas jugée. |
| La qualification est-elle plus simple ? | Qui suit qui rend la distinction des rôles concrète ; la scène de création manque d'un avertissement d'extrait, car un novice pourrait croire que nom et commune ne sont plus à saisir. Ce point concerne le cadrage UX03, pas une refonte UX06. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La date et l'heure de Paris sont visibles, les accès de confirmation sont explicites ; les deux blocs du compte rendu demandent une instruction courte sur l'ordre et sur les informations effectivement sauvegardées. |
| Les risques d’oubli sont-ils réduits ? | Le bloc Pourquoi cette alerte reste-t-elle visible de UX04 aide à comprendre une alerte persistante ; sur UX02 mobile, les filtres et explications repoussent le premier dossier sous la première hauteur d'écran. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère après pour UX01, UX03, UX04 et UX05, sous les clarifications signalées ; je réserve mon choix UX02 tant que la densité mobile et la compréhension des catégories ne sont pas éprouvées. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | L'état vide explique ce qu'il signifie et offre un accès équipe, amélioration textuelle visible. |
| UX02 | RESERVE | Le bureau est lisible mais la page mobile fait environ 1590 pixels et le premier dossier commence vers 1000 pixels ; aucune capture mobile avant ne permet de comparer. |
| UX03 | APRES | Les phrases distinguent relation, dossier et action ; signaler que création est une zone ciblée avant toute préférence sur le formulaire complet. |
| UX04 | APRES | Le rattachement précède les dates, et le résumé annonce l'autre dossier non couvert. |
| UX05 | APRES | La confirmation est claire ; la sauvegarde du compte rendu et de l'explication sans tâche doit être rendue moins ambiguë. |


Réserves conservées :

- Ni contraste calculé, ni parcours clavier, ni lecteur d'écran, ni changement dynamique de focus n'ont été testés.
- La longueur mobile est un constat de composition sur image, pas un défaut confirmé de l'application.

### Expert UX Researcher — E5

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | La comparaison UX01 repose sur deux états personnels vides relativement comparables ; UX02 oppose une fiche avant à une liste après, ce qui autorise une appréciation de présentation mais pas une preuve de meilleure couverture. |
| Les prochaines actions sont-elles plus visibles ? | Les responsables, dates et rattachements sont visibles dans UX04 ; aucune mesure de compréhension ou de réduction des erreurs n'a été réalisée, malgré la cohérence apparente du scénario. |
| La qualification est-elle plus simple ? | UX03 répond à l'hypothèse de confusion O17, sans démontrer qu'elle était vécue ; annoncer l'extrait de création empêchera de transformer la disparition de champs hors cadrage en amélioration UX06 non autorisée. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La confirmation et le compte rendu illustrent la continuité souhaitée, tandis que l'avant est un agenda sur une autre semaine ; l'absence de parcours complet avant m'empêche d'attribuer une supériorité fonctionnelle au nouveau dessin. |
| Les risques d’oubli sont-ils réduits ? | Les listes définies, les unités et la note de recouvrement rendent l'hypothèse de pilotage examinable ; la maquette ne prouve ni les règles de comptage ni l'absence d'angles morts, et aucune notification n'a été reçue pendant cette revue. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère visuellement après sur UX01, UX03 et UX04 ; je garde une réserve UX02 et UX05 parce que les écrans avant ne documentent pas les mêmes états. Cette réserve ne signifie pas préférence pour l'ancien produit. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | Les états vides sont comparables et l'explication personnelle/collective est directement visible. |
| UX02 | RESERVE | L'avant n'est pas une liste globale stabilisée ; la conception semble utile mais la comparaison ne permet pas une préférence suffisamment étayée sur ce parcours. |
| UX03 | APRES | La distinction des rôles et les effets d'une affectation sont plus explicitement décrits, sous réserve d'annoncer le cadrage partiel de création. |
| UX04 | APRES | Le lien d'une tâche à un dossier et l'alerte persistante sont illustrés dans un cas à deux dossiers ; cela étaye une préférence de lisibilité, pas une réussite utilisateur. |
| UX05 | RESERVE | Les images proposent une chaîne dont l'état actuel n'a pas été recetté ; impossible de conclure à une amélioration fonctionnelle ni à un défaut existant. |


Réserves conservées :

- Les cinq préférences expertes ne constituent pas les douze voix de l'atelier ni une validation par des personnes réelles.
- Aucun nouvel arbitrage métier substantiel n'est accepté par cette revue ; si une règle est figée ultérieurement, son périmètre et un nouveau vote doivent être examinés.

### Delphine — DEL

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | Je distingue ma file personnelle de l'équipe et je vois le rôle de chaque dossier ; je ne peux pas déduire l'exhaustivité du portefeuille de compteurs fictifs. |
| Les prochaines actions sont-elles plus visibles ? | Le dossier concerné et les deux dates sont explicités ; le second dossier reste justement signalé sans prochaine action. |
| La qualification est-elle plus simple ? | Je comprends mieux qui suit la relation et qui porte une opportunité ; potentiel, statuts et qualité de qualification n'ont pas été refondus ni testés ici. |
| Les rendez-vous sont-ils plus faciles à gérer ? | Date, durée, responsable et accès au bon jour de l'agenda rendent la confirmation plus utile ; je n'ai pas exécuté le parcours de compte rendu. |
| Les risques d’oubli sont-ils réduits ? | L'explication de l'alerte persistante réduit une ambiguïté plausible ; la réception effective des rappels et la couverture de tous les dossiers restent à démontrer. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère les propositions UX01, UX03, UX04 et UX05 ; je réserve mon choix sur UX02 tant que les définitions et les vues existantes ne sont pas rapprochées. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | La portée et l'état vide sont compréhensibles sans imposer les chiffres de l'équipe à mon accueil personnel. |
| UX02 | RESERVE | Les listes paraissent utiles, mais l'avant Suivi n'était pas stabilisé et le sens des filtres de dossier appliqués aux risques prospect reste à préciser. |
| UX03 | APRES | Je peux confier la relation à Camille tout en gardant Léa sur le dossier et sa préparation. |
| UX04 | APRES | Le rattachement et le second dossier non couvert restent visibles ; la distinction des deux dates est conservée. |
| UX05 | APRES | Les accès au rendez-vous, à sa date d'agenda et à la fiche soutiennent la préparation commerciale. |


Réserves conservées :

- La fiche de suivi mobile s'étend sur environ deux hauteurs d'écran de 844 px ; le second dossier et son bouton demandent du défilement.
- Le rendu statique ne démontre ni gain de temps ni fonctionnement des notifications.

### Marc — MAR

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | La bascule Équipe et ses listes me donnent un état quotidien plus lisible : les deux retards, trois actions du jour et un rendez-vous correspondent aux lignes montrées. Cela ne prouve pas l'exhaustivité du CRM réel. |
| Les prochaines actions sont-elles plus visibles ? | Je vois le dossier et le responsable de chaque action d'équipe ; sur UX04, le récapitulatif précise que l'autre dossier reste découvert, ce qui rend la priorité compréhensible. |
| La qualification est-elle plus simple ? | Les responsabilités sont mieux séparées, mais les statuts et le potentiel n'ont pas été refondus. Je ne prétends donc pas qualifier mieux grâce à ces seules cinq orientations P1. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La confirmation affiche la date, Léa, le rappel interne et les deux accès utiles ; le compte rendu puis la suite proposée forment une continuité lisible. Les modifications et notifications ne sont pas testables sur ces images. |
| Les risques d’oubli sont-ils réduits ? | Les dossiers sans prochaine action deviennent repérables, avec une définition. Le risque d'oubli n'est pas éliminé : l'inactivité et la stagnation attendent encore un seuil métier. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère les cinq propositions après, sous réserve de vérifier les totaux et de conserver les écrans existants qui remplissent déjà ces objectifs. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | La portée personnelle vide est distinguée de l'activité collective, et le résumé Équipe mène visuellement à des lignes identifiables. |
| UX02 | APRES | Les deux dossiers listés correspondent au total deux sur quatre et la non-addition des listes est annoncée ; la revue devient actionnable dans le scénario fictif. |
| UX03 | APRES | Le récapitulatif indique que seul le prospect passe à Camille ; Léa conserve dossier et action, sans transfert global silencieux. |
| UX04 | APRES | Le choix prospect ou dossier et la phrase sur Association commerçante rendent l'alerte future interprétable. |
| UX05 | APRES | La confirmation et le rendez-vous partagent date, durée et responsable ; le compte rendu ne prétend pas créer une tâche automatiquement. |


Réserves conservées :

- Les totaux fictifs sont cohérents entre les vues examinées, mais aucun rapprochement avec une API ou les permissions réelles n'est démontré.
- Les seuils d'inactivité et de stagnation doivent être arrêtés et testés avant de présenter le pilotage comme exhaustif.
- La maquette ne prouve ni la livraison des rappels ni l'efficacité du compte rendu dans le produit déployé.

### Sophie — SOP

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | Les unités prospect et dossier sont distinguées et les compteurs de risques ouvrent une piste de travail ; la portée du filtre Responsable du dossier doit rester compréhensible sur une liste de prospects. |
| Les prochaines actions sont-elles plus visibles ? | Je peux lire quel dossier recevra la préparation et qui l'exécutera avant de confirmer, ce qui aide une saisie pour un collègue. |
| La qualification est-elle plus simple ? | Les responsabilités à la création sont plus explicites et aucune complétude artificielle n'est imposée ; la maquette ne prouve pas le contrôle de doublons ni la qualification effective. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La note de préparation et les références du rendez-vous sont réunies ; les commandes affichées ne prouvent pas les modifications ou annulations. |
| Les risques d’oubli sont-ils réduits ? | Les listes et l'alerte du dossier non couvert sont utiles pour une revue administrative, sous réserve de vérifier l'exactitude des totaux. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère les cinq propositions visuelles pour mon travail de préparation et de suivi, avec réserves sur les filtres et la longueur des formulaires. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | L'état vide distingue clairement mes tâches de celles de l'équipe et donne une entrée vers le travail partagé. |
| UX02 | APRES | La liste détaillée des deux dossiers sans action est exploitable, contrairement à un chiffre isolé ; la comparaison ne prouve pas que l'ancien Suivi en était dépourvu. |
| UX03 | APRES | Le récapitulatif limite l'ambiguïté lorsque je crée un dossier pour Léa sans attribuer le prospect. |
| UX04 | APRES | Le choix du contexte, le responsable de l'action et le résumé des dates correspondent à une saisie administrative vérifiable. |
| UX05 | APRES | La préparation associée au rendez-vous peut m'éviter de reconstruire le contexte à partir de plusieurs informations. |


Réserves conservées :

- La création mobile comporte de la répétition entre l'aide, l'avertissement et le récapitulatif ; cela pourrait rallonger les saisies en série.
- Imports et filtres avancés doivent rester accessibles ; cette revue ne teste pas leur conservation.
- La catégorie Sans interaction récente n'a pas encore de seuil défini : aucun total ne doit être présenté comme validé.

### Patrick — PAT

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | Je comprends que mes zéros ne décrivent pas le travail de l'équipe ; le tableau de risques est plus détaillé que ce dont j'ai besoin pour commencer. |
| Les prochaines actions sont-elles plus visibles ? | Je sais quel dossier l'action concerne, mais le formulaire de planification occupe une longue page pour une seule préparation ; je garde une réserve sur sa rapidité. |
| La qualification est-elle plus simple ? | Responsable du dossier et responsable du prospect ne désignent plus la même chose pour moi dans la lecture ; cela ne prouve pas que je saurais qualifier ou changer un statut. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La date et le bouton vers le bon jour de l'agenda sont immédiats à comprendre ; je voudrais essayer cette navigation avant d'en dépendre en tournée. |
| Les risques d’oubli sont-ils réduits ? | Le second dossier sans action est expliqué, mais sur mobile je dois descendre après le résumé de la première action pour le trouver. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère UX01, UX03 et UX05 ; je réserve ma préférence sur UX02 et UX04, trop détaillées pour juger leur facilité sans essai. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | Les phrases sur la file vide et le bouton Équipe donnent un prochain geste simple. |
| UX02 | RESERVE | Plusieurs catégories et définitions font concurrence à ma question immédiate : quelle fiche dois-je traiter maintenant ? |
| UX03 | APRES | Les trois rôles et le récapitulatif rendent l'affectation lisible sans attribuer tout le dossier à la même personne. |
| UX04 | RESERVE | Le contexte est mieux expliqué, mais la somme de textes, sections et résumé peut ralentir ma saisie ; je ne préfère pas encore l'ensemble à l'ancien formulaire. |
| UX05 | APRES | Le rendez-vous confirmé et l'accès au 26 novembre sont plus concrets qu'une confirmation sans suite visible. |


Réserves conservées :

- UX04-action atteint environ 1 310 px en bureau sur cette capture ; le bouton final est sous le premier écran de 1 000 px.
- La création mobile conserve un bouton final très bas ; ne pas déduire que sa lecture est simple de sa seule absence de débordement.
- Réduire des répétitions serait un ajustement possible ; supprimer la distinction prospect/dossier changerait l'orientation et nécessiterait un nouveau vote.

### Julie — JUL

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | Je comprends que mes trois zéros concernent mes responsabilités et que l'équipe a d'autres actions. La page personnelle reste centrée sur mon travail, ce qui répond à mon objection initiale au grand dashboard. |
| Les prochaines actions sont-elles plus visibles ? | L'action prévue le 20 novembre à 14 h et son rappel à 9 h sont distincts. Le formulaire est cependant haut : les boutons de confirmation viennent après de nombreuses explications. |
| La qualification est-elle plus simple ? | La fiche de responsabilités m'aide à agir sur le bon périmètre, mais elle ne démontre aucun gain de vitesse de qualification. La création progressive et les aides de statut restent hors de cette sélection P1. |
| Les rendez-vous sont-ils plus faciles à gérer ? | Je préfère les accès explicites de confirmation ; sur mobile, l'agenda répète le titre, le prospect et le dossier avant le panneau de détail, ce qui augmente le défilement jusqu'à Modifier. |
| Les risques d’oubli sont-ils réduits ? | Les alertes expliquées peuvent éviter de recréer une tâche pour le mauvais dossier. Je reste réservée sur l'ajout de listes de risques tant que leur usage quotidien et les capacités existantes ne sont pas vérifiés. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Après pour l'accueil, les rôles et les actions ; réserve sur la densité de UX02 et le parcours mobile de UX05. Je ne demande pas de revenir à une confirmation moins explicite. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | Le compromis par portée protège mon accueil léger tout en rendant l'équipe accessible. |
| UX02 | RESERVE | Les définitions sont utiles, mais le panneau de catégories et les filtres demandent une lecture supplémentaire ; les lignes Délai à choisir ne sont pas encore actionnables. |
| UX03 | APRES | Les rôles sont lisibles et l'affectation annoncée ne change pas mes tâches implicitement. |
| UX04 | APRES | Le contexte explicite vaut la place prise, sous réserve de vérifier la durée de saisie réelle et de conserver un résumé bref. |
| UX05 | RESERVE | Le contenu de confirmation progresse ; la capture mobile mesure visuellement plus de deux hauteurs d'écran usuelles, avec répétition du résumé avant les commandes. Aucun temps d'interaction n'est mesuré. |


Réserves conservées :

- L'agenda mobile est lisible sans coupure horizontale visible, mais sa longueur et les répétitions appellent un essai de navigation réel.
- Le lien vers le rendez-vous sélectionné peut faciliter l'accès direct ; sa mise au point du focus et son comportement tactile restent non vérifiés.
- Aucun gain en nombre de clics ou en temps ne peut être conclu des boutons métier inactifs.

### Nathalie — NAT

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | L'explication de Mes actions me permet de reprendre mes repères sans supposer que toute l'équipe est inactive. |
| Les prochaines actions sont-elles plus visibles ? | Je comprends mieux pourquoi Association commerçante reste en alerte malgré la préparation déjà prévue ; le contexte doit rester visible quand je reviens plus tard. |
| La qualification est-elle plus simple ? | Les rôles à la création sont expliqués sur place, mais les notions de potentiel et de statut restent hors de cette amélioration. |
| Les rendez-vous sont-ils plus faciles à gérer ? | La confirmation me dit quand et avec qui le rendez-vous est prévu ; les actions ultérieures doivent encore être testées pour vérifier que je retrouve mes repères. |
| Les risques d’oubli sont-ils réduits ? | La distinction entre dossiers couverts et non couverts aide à interpréter les alertes ; elle ne garantit pas que je verrai l'alerte située plus bas sur mobile. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Je préfère UX01, UX03, UX04 et UX05 pour leurs explications locales ; je reste réservée sur la densité d'UX02. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | La phrase sur la file personnelle vide évite de devoir mémoriser le sens du périmètre. |
| UX02 | RESERVE | Les unités sont nommées mais je dois encore comprendre plusieurs catégories, les filtres et les seuils à choisir avant de savoir quoi traiter. |
| UX03 | APRES | Les aides locales et le récapitulatif évitent de réapprendre les deux responsabilités entre mes connexions. |
| UX04 | APRES | L'explication de l'alerte persistante et les dates nommées rendent la situation cohérente dans la lecture. |
| UX05 | APRES | Les boutons vers le rendez-vous et le bon jour fournissent des repères concrets pour retrouver la réservation. |


Réserves conservées :

- Sur mobile, les explications sont lisibles mais longues ; leur efficacité demande un test avec retour après une période sans connexion.
- Le menu mobile est visible sous forme de représentation ; aucun test d'ouverture, clavier ou lecteur d'écran n'a été réalisé.
- La préférence pour UX04 porte sur la compréhension, sans preuve de gain de vitesse.

### Thomas — THO

| Question | Réponse simulée |
| --- | --- |
| Comprenez-vous mieux l’état de la prospection ? | La portée Équipe, les échéances et le détail des compteurs améliorent ma lecture du scénario. Le rendez-vous du 26 novembre est correctement hors de la fenêtre du 19 au 25 de l'accueil. |
| Les prochaines actions sont-elles plus visibles ? | Je peux identifier le propriétaire d'une action, son dossier et son rappel ; j'apprécie que la même préparation ne fasse pas disparaître l'alerte d'un second dossier. |
| La qualification est-elle plus simple ? | La clarification des responsabilités sécurise l'organisation du suivi. La qualité du potentiel, les transitions et la complétude de qualification ne sont pas démontrées par ces maquettes. |
| Les rendez-vous sont-ils plus faciles à gérer ? | Le rendez-vous a le même créneau de 30 minutes, le même responsable et le même rappel dans la confirmation et l'agenda. La proposition après rendez-vous garde une décision humaine sur la tâche. |
| Les risques d’oubli sont-ils réduits ? | La couverture visuelle est meilleure, mais des seuils non choisis et une population fictive ne prouvent pas la détection de tous les dossiers à risque d'une équipe de dix personnes. |
| Préférez-vous l’ancienne ou la nouvelle version ? | Après pour les quatre orientations aux responsabilités et parcours explicites ; réserve sur UX02 tant que les définitions et le rapprochement réel des listes ne sont pas validés. |


| Orientation | Préférence | Argument simulé |
| --- | --- | --- |
| UX01 | APRES | Les compteurs sont accompagnés de portée et d'horizon ; la fenêtre des prochains rendez-vous explique l'exclusion du 26 novembre. |
| UX02 | RESERVE | Je soutiens l'orientation votée, mais la vue reste partiellement définie : l'exclusion des pauses justifiées et les seuils d'ancienneté doivent être confirmés par le métier avant toute conclusion d'exhaustivité. |
| UX03 | APRES | L'affectation limitée au prospect respecte les rôles distincts ; le panneau n'introduit pas le transfert global UX09 non retenu pour cette phase. |
| UX04 | APRES | Les deux dates et le dossier concerné sont vérifiables dans le récapitulatif, sans rattachement automatique au second dossier. |
| UX05 | APRES | La réalisation reste liée au compte rendu et la prochaine action est explicitement à compléter puis confirmer ; il n'y a pas de tâche silencieuse ni d'envoi prospect annoncé. |


Réserves conservées :

- Les règles de comptage illustrées sont des propositions, pas des invariants supplémentaires adoptés par ces images.
- Le bouton Guide de prise en main sur l'accueil est secondaire : ne pas en déduire un nouveau chantier d'onboarding dans le lot P1.
- La relation entre enregistrement du compte rendu puis ajout d'une explication sans action doit rester explicite au moment d'une future implémentation.

## Sources et limites

[Revue des experts](revue-simulee-experts.json), [revue terrain](revue-simulee-terrain.json), [revue pilotage](revue-simulee-pilotage.json). Les listes d’images effectivement examinées figurent dans chaque source. [Préparation de la revue](revue-experts-preparation.md), [galerie comparative](comparatif-avant-apres.html), [inventaire des maquettes](inventaire-maquettes.md).

Aucune modification du code applicatif, aucune connexion au CRM, aucune donnée de TEST modifiée durant cette étape. La validation finale appartient à l’utilisateur. **Étape 3 produite, en attente de validation ; étape 4 non engagée.**
