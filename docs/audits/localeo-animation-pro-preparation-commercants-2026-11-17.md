# Actions de préparation des commerçants — audit et décisions UX

Séance du **17 novembre 2026**. Périmètre : actions attendues des commerçants dans Localeo Pro et coordination de leur préparation par une association de commerçants dans Localeo Animation. Les modèles examinés sont le **Juste Prix local** et le **Jeu des vitrines**.

**Statut : orientations retenues pendant le brainstorming, à préciser et à tester.** Elles ne constituent ni une implémentation, ni une modification des spécifications ou de la roadmap. Les difficultés d'usage ci-dessous restent des hypothèses, faute d'observation auprès d'utilisateurs réels.

## Objectif et méthode

La séance cherche à faciliter les actions que le commerçant doit accomplir pour permettre le déroulement de l'animation et à améliorer leur suivi par le gestionnaire. Le contexte de travail retenu est celui d'un commerçant de bouche utilisant son téléphone, parfois interrompu par ses clients, et d'une association coordonnant plusieurs commerces. L'exemple d'une fleuriste a également servi à explorer la vitrine ; ces personnages et situations sont fictifs.

Les conclusions reposent sur une lecture ciblée de sources locales, de spécifications et sur les arbitrages du demandeur. Aucun parcours applicatif, test navigateur, essai sur appareil ou observation d'utilisateur n'a été réalisé durant la séance ; aucune commande métier n'a été déclenchée. Une simulation ne remplace pas un essai réel et aucun gain chiffré n'a été mesuré. La présente formalisation a été demandée séparément après la séance.

Les références locales relevées sont Projet `8b20cf9`, Animation `845d94a` et Commerçant `e60ce30`. Les arbres des deux applications étaient propres ; le dépôt documentaire contenait déjà des modifications. Ces références ne prouvent pas les versions déployées. Les deux modèles restent en cours dans la [roadmap](../roadmap/README.md) ; le [guide d'exploitation](../specifications/epic-55-moteur-animation/exploitation-moteur.md#juste-prix-local--e77) indique que le Juste Prix est implémenté localement mais encore inactif, et la roadmap indique également le Jeu des vitrines inactif.

Le [rapport sur le suivi des animations](localeo-animation-pro-suivi-brainstorming-2026-11-17.md) est un travail distinct : ses orientations ne sont pas automatiquement modifiées ou réadoptées par la présente séance.

## Parcours actuels reconstitués

### Juste Prix : proposition de produit

Après acceptation de sa participation, le commerçant principal prépare dans Pro le nom, la description, le format et le prix TTC de son produit ; un visuel peut être fourni. Un brouillon incomplet peut être enregistré. Le formulaire distingue l'**enregistrement** de la **proposition** envoyée au gestionnaire. Les états comprennent « À compléter », « Proposé à l'organisateur », « À corriger » et « Approuvé par l'organisateur ».

Le gestionnaire habilité consulte les propositions privées par commerce, accepte la révision présentée ou demande une correction motivée. Le commerçant voit le motif et peut corriger, enregistrer puis proposer une nouvelle version. Une modification peut invalider une approbation précédente ; l'approbation porte sur la version effectivement examinée. Le prix de référence reste privé selon les règles du modèle.

Le formulaire indique les modifications non enregistrées et le code demande au navigateur d'avertir avant de quitter une saisie modifiée. Cela ne prouve pas la conservation de la saisie non enregistrée après une interruption ou une fermeture, notamment sur appareil réel. Le résultat incertain nécessite une vérification avant de poursuivre.

Sources : [parcours Juste Prix](../specifications/epic-77-juste-prix-local/parcours-regles.md), [préparation Pro](../../../localeo-commercant/src/features/animations/pages/AnimationPreparationPage.jsx), [formulaire produit Pro](../../../localeo-commercant/src/features/animations/components/JustePrixProduct.jsx) et [propositions dans Animation](../../../localeo-animation/src/app/components/JustePrixProducts.tsx).

### Jeu des vitrines : contenu, installation et contrôle

Dans le parcours local, le commerçant prépare sa vitrine en quatre étapes : prévoir la vitrine et l'intrus ; préparer la question et les choix ; relire et proposer ; installer et faire contrôler. La revue distingue les éléments présentés aux joueurs — emplacement, consigne et choix — des informations privées, notamment la désignation de la bonne réponse et les instructions de mise en place.

Après proposition, le gestionnaire approuve la révision ou demande une correction. Une fois le contenu approuvé, le commerçant installe le dispositif et atteste son installation. L'organisateur vérifie ensuite sur place et confirme son contrôle. Ces faits restent distincts ; une modification du contenu ou une nouvelle attestation peut invalider des validations ou contrôles antérieurs selon les règles du modèle.

Dans Pro, le parcours affiche déjà une « Prochaine étape » adaptée à l'état. Dans Animation, les dossiers sont regroupés entre « À traiter par l’organisation », « En attente des commerçants » et « Prêtes », avec les étapes de contenu, installation et contrôle. Les regroupements et compteurs affichés concernent la page courante.

Sources : [parcours des vitrines](../specifications/epic-78-jeu-des-vitrines/parcours-regles.md), [préparation de vitrine dans Pro](../../../localeo-commercant/src/features/animations/components/VitrinePreparation.jsx) et [suivi des vitrines dans Animation](../../../localeo-animation/src/app/components/VitrinesPreparation.tsx).

## Constats et hypothèses d'usage

| Constat dans les sources locales | Hypothèse à tester auprès des utilisateurs |
| --- | --- |
| Dans Pro, enregistrer un produit Juste Prix et le proposer sont deux actions distinctes ; le résultat de l'enregistrement indique la suite. | Après une interruption, le commerçant pourrait croire que le produit enregistré a déjà été transmis. |
| Le produit peut être enregistré en brouillon incomplet ; la saisie modifiée non enregistrée déclenche un avertissement navigateur. | Le commerçant pourrait croire qu'une saisie non enregistrée a été conservée ou ne pas penser à enregistrer avant d'interrompre sa tâche. |
| Une correction Juste Prix affiche un motif ; après modification, il faut enregistrer puis reproposer. | Le commerçant pourrait penser qu'une correction enregistrée a automatiquement été transmise à l'association. |
| Les propositions Juste Prix sont affichées dans une liste paginée ; les états et actions figurent sur les lignes. | Un gestionnaire peut devoir parcourir plusieurs pages pour trouver les propositions qui attendent sa décision. |
| Pour les vitrines, Pro indique déjà la prochaine étape ; après approbation, l'installation et son attestation restent à la charge du commerçant. | Après interruption, le commerçant pourrait ne pas revenir dans le détail et ne pas voir que l'installation lui revient. |
| La vue vitrines d'Animation regroupe les états et précise que ses compteurs concernent la page. | Un gestionnaire pourrait interpréter « aucune décision à prendre sur cette page » comme une absence d'action pour toute l'animation. |
| Le parcours de vitrine explique les champs et distingue déjà, à la relecture, les informations publiques des informations privées. | Un commerçant pourrait hésiter sur ce qu'il doit installer, rédiger pour les joueurs ou garder privé. |

Ces hypothèses n'établissent ni un défaut confirmé, ni une perte de données, ni un gain de temps. Les propositions ci-dessous visent à les éprouver.

## Quatre améliorations retenues

Ces orientations ne créent pas de nouveaux critères d'acceptation canoniques. Les efforts sont relatifs ; les données disponibles, droits et effets sur les contrats doivent être vérifiés avant une éventuelle réalisation.

### 1. Guider la proposition et la correction d'un produit Juste Prix

- **Écran et acteur :** formulaire produit et préparation dans Pro, pour le commerçant principal autorisé.
- **Difficulté supposée :** confondre brouillon enregistré et proposition reçue, perdre le fil après interruption ou croire qu'une correction enregistrée a été retransmise.
- **Décisions retenues :** montrer les étapes « préparer et enregistrer → proposer à l'organisateur → attendre sa réponse », l'étape courante et la prochaine action. Rendre la saisie non enregistrée visible et faciliter l'enregistrement d'un brouillon incomplet ; au retour, montrer le dernier état confirmé. En cas de correction, montrer le motif, guider vers le champ concerné lorsqu'il est connu et accompagner les étapes « corriger → enregistrer → proposer à nouveau → attendre la réponse ».
- **Arbitrage :** pour la reprise du brouillon Juste Prix, la séance a retenu la clarification et l'enregistrement explicite, plutôt qu'une nouvelle entrée dédiée sur l'accueil. Elle n'a pas retenu de sauvegarde automatique. Un motif général ou portant sur plusieurs éléments ne doit pas désigner arbitrairement un champ.
- **Bénéfice attendu :** retrouver une prochaine action compréhensible et distinguer les faits confirmés. **Effort et risque :** changement de présentation et de guidage ; conserver la proposition explicite, les révisions, permissions et relectures après résultat incertain.
- **Validation :** sans aide, un commerçant distingue un brouillon d'une proposition transmise ; après interruption, il reconnaît le dernier état confirmé ; après correction, il comprend que l'enregistrement ne suffit pas à envoyer la nouvelle version.

### 2. Retrouver les actions du gestionnaire sur toute l'animation

- **Écrans et acteur :** propositions Juste Prix et suivi des vitrines dans Animation, pour le gestionnaire habilité.
- **Difficulté supposée :** identifier les actions qui lui reviennent parmi plusieurs commerces et pages.
- **Décision retenue :** fournir un moyen de retrouver, sur l'ensemble de l'animation, les propositions Juste Prix à examiner ; pour les vitrines, distinguer les contenus à examiner et les contrôles sur place à réaliser. Conserver l'accès à tous les commerces et des états explicites : préparation ou correction attendue du commerçant, proposition à examiner, contenu approuvé, installation ou contrôle selon le modèle.
- **Bénéfice attendu :** retrouver le travail qui relève du gestionnaire sans parcourir toutes les pages. **Effort et risque :** vérifier les capacités des producteurs, droits, pagination, fraîcheur et coût d'une recherche sur l'ensemble ; un regroupement des seules lignes chargées ne suffit pas. Une erreur de lecture ne doit pas être présentée comme « rien à faire ».
- **Validation :** avec des actions réparties sur plusieurs pages, le gestionnaire retrouve sans aide une proposition à examiner et un contrôle terrain à réaliser, tout en distinguant les attentes envers les commerçants.

### 3. Retrouver l'installation d'une vitrine après approbation

- **Écrans et acteur :** accueil et préparation de vitrine dans Pro, pour le commerçant autorisé.
- **Difficulté supposée :** après interruption, ne pas voir que le contenu a été approuvé et que l'installation lui revient.
- **Décision retenue :** compléter le guidage existant par une tâche « Installer ma vitrine » sur l'accueil lorsque le contenu est approuvé et que l'installation reste à attester ; elle ouvre directement l'étape concernée. Après l'attestation, le parcours indique que le contrôle sur place est attendu de l'association.
- **Bénéfice attendu :** aider à découvrir et reprendre la tâche au moment opportun. **Effort et risque :** vérifier l'accès à un état fiable et les droits, la place de plusieurs tâches sur téléphone et la relecture après action depuis un autre accès. Aucun état inconnu ne devient « prêt ».
- **Validation :** après approbation et interruption, la commerçante retrouve les consignes et atteste son installation ; elle comprend ensuite que le contrôle revient au gestionnaire. Si l'installation a déjà été attestée ailleurs, la relecture ne lui demande pas de recommencer.

### 4. Comprendre la préparation du défi vitrine

- **Écran et acteur :** parcours de vitrine dans Pro, pour le commerçant.
- **Difficulté supposée :** hésiter entre l'installation réelle, la consigne destinée aux joueurs et les éléments privés.
- **Décision retenue :** associer des consignes concrètes aux champs et un exemple fictif complet, facultatif et consultable au moment utile. Montrer séparément l'emplacement, la consigne et les choix publics d'une part, et la désignation de la bonne réponse et les instructions privées de mise en place d'autre part. L'exemple ne remplit aucun champ automatiquement.
- **Bénéfice attendu :** comprendre la tâche sans confondre son propre défi et l'exemple. **Effort et risque :** vérifier la lisibilité sur téléphone et préserver la confidentialité de la bonne réponse ; le libellé de l'objet correct peut lui-même figurer parmi les choix publics, seule sa désignation comme réponse correcte reste privée.
- **Validation :** sans assistance, le commerçant prépare son propre défi et explique ce que les joueurs verront et ce qui reste privé.

## Points ouverts et règles à préserver

1. Vérifier les états accessibles à l'accueil Pro et les lectures ou projections nécessaires, sans supposer qu'une tâche peut être calculée de façon complète à partir d'une seule page. Préciser le comportement en chargement, erreur, droits insuffisants et réponse obsolète.
2. Vérifier la faisabilité de filtres portant sur toute l'animation, côté producteurs et consommateurs ; distinguer un résultat vide confirmé d'une lecture indisponible.
3. Tester sur téléphone les interruptions, la protection des saisies non enregistrées et la reprise du dernier brouillon confirmé. Ne pas promettre de conservation automatique de saisies non enregistrées.
4. Conserver les droits du commerçant principal et du gestionnaire, les commandes explicites, les révisions et la confidentialité. Une approbation porte sur la version examinée ; une proposition ou une installation modifiée peut invalider des faits antérieurs selon le domaine.
5. Distinguer approbation du contenu, installation attestée et contrôle terrain. Le contrôle correspond à une vérification réelle sur place. Préserver la relecture après conflit ou résultat incertain et éviter les répétitions automatiques d'écritures.
6. Examiner séparément les critères d'acceptation, contrats, documentation fonctionnelle et d'exploitation, migrations et générateur de démonstration si ces orientations donnent lieu à une évolution ; aucune absence d'impact n'est présumée à ce stade.

## Protocole de test proposé — non exécuté

Faire essayer les parcours actuels puis les propositions à des commerçants et gestionnaires d'aisance numérique variée. Utiliser des données fictives et un prototype ou un environnement de démonstration maîtrisé ; les commandes et communications sont simulées ou isolées des destinataires et données réels. Formuler les tâches sans indiquer le bouton ; varier l'ordre des variantes et utiliser les équipements habituels, notamment des téléphones physiques côté commerçant.

| Rôle et départ | Objectif formulé pour l'utilisateur | Réussite observable | Cas défavorable à organiser |
| --- | --- | --- | --- |
| Commerçant, participation Juste Prix acceptée | « Préparez votre produit et transmettez-le à l'association. » | Renseigne les éléments nécessaires et distingue brouillon enregistré et proposition transmise. | Visuel absent ; interrompre avant puis après enregistrement et comparer le dernier état confirmé. |
| Gestionnaire, plusieurs commerces Juste Prix | « Retrouvez les produits sur lesquels vous devez vous prononcer. » | Trouve les propositions et distingue les préparations encore attendues des commerçants. | Propositions sur plusieurs pages ; lecture indisponible ou droit de consultation seul. |
| Gestionnaire puis commerçant, produit proposé | « Demandez une précision sur le format », puis « Corrigez et renvoyez votre proposition ». | Le motif est compris ; la nouvelle version est enregistrée puis explicitement proposée ; le gestionnaire sait qu'une décision lui revient. | Motif général, modification concurrente ou résultat d'envoi incertain. |
| Commerçant, préparation vitrine | « Préparez un défi que les joueurs pourront utiliser devant votre vitrine. » | Conçoit son propre défi et distingue les contenus publics de la bonne réponse et des consignes privées. | Première utilisation sans aide ; exemple fictif consulté sans remplissage automatique. |
| Commerçant puis gestionnaire, vitrine approuvée | « Retrouvez ce qu'il vous reste à installer », puis « Retrouvez les contrôles à effectuer ». | Le commerçant installe et atteste ; le gestionnaire identifie le contrôle terrain puis le confirme selon ses droits. | Attestation réalisée entre-temps par un accès autorisé ; plusieurs commerces et actions répartis sur plusieurs pages. |

Observer la réussite sans assistance, les hésitations, erreurs, retours en arrière, changements d'écran et ressaisies ; mesurer séparément le temps actif et les attentes. Consigner ce qui est observé, simulé et non exécuté. Aucun gain n'est annoncé avant mesure ; la recette réelle reste à organiser.
