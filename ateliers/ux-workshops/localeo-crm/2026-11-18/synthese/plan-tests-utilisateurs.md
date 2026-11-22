# Plan de tests auprès d’utilisateurs réels — non exécuté

Version de préparation du 19 novembre 2026. Aucun recrutement ni test réel n’a eu lieu. Les votes des personas ne remplacent pas ces séances. Ce plan couvre les risques du [rapport exécutif](../workshop/rapport-executif.md) et du [registre](../validation/risques-non-resolus.md).

## Organisation et données

Prévoir 5 à 7 participants réels : commercial expérimenté, commercial peu familier des CRM, assistanat, responsable d’équipe et usage occasionnel. Ajouter une recette croisée à deux comptes de rôles différents. Prévoir 60 à 75 minutes par séance, quitte à répartir les scénarios ; ne pas annoncer un résultat statistiquement représentatif.

Utiliser uniquement l’environnement TEST autorisé et un jeu fictif isolé, préfixé par l’identifiant de la nouvelle séance. Le facilitateur prépare une fiche attendue : prospects avec/sans responsable, deux dossiers distincts sur un prospect, actions hier/aujourd’hui/demain, action de prospect ne couvrant aucun dossier, rendez-vous disponible et créneau concurrent. Fixer les dates relativement au jour de séance, le fuseau Europe/Paris et les seuils explicitement arbitrés. Si un seuil ou une règle reste indéfini, coder le résultat « non évaluable », jamais « réussi ».

Pour la première connexion, prévoir un compte neuf de test et un accès fourni hors archive. Pour la qualification, préparer des faits commerciaux fictifs sans prescrire les noms de boutons. Réserver les notifications à des destinataires de test autorisés. Aucun message à un prospect réel. Définir un inventaire de création et un nettoyage ciblé autorisé en fin de séance ; ne pas réutiliser aveuglément les objets UX TEST laissés lors de l’exploration.

Commencer sur ordinateur, puis reprendre les tâches critiques sur un smartphone réel dans des conditions réseau connues ; noter appareil, navigateur, résolution, version déployée et compte pseudonymisé. Prévoir clavier et lecteur d’écran avec un utilisateur compétent. Recueillir le consentement pour toute capture ou tout enregistrement ; conserver des identifiants de séance pseudonymes, pas les coordonnées des participants.

## Animation et mesure communes

Lire la consigne sans montrer le chemin ni le vocabulaire de la solution. Dire : « Faites comme vous le feriez au travail ; dites ce que vous cherchez et ce que vous comprenez. » Attendre une tentative, puis noter toute aide donnée. Ne pas demander « trouvez-vous cela plus simple ? » avant le parcours. Débriefer : « Qu’attendiez-vous ? Qu’avez-vous compris ? Qu’est-ce qui vous a fait hésiter ? »

Pour chaque scénario : enregistrer succès autonome / succès avec aide / échec / non évaluable, temps observé (sans seuil inventé), erreurs, retours arrière, abandons, aide exacte et compréhension reformulée. Vérifier ensuite les objets enregistrés et l’historique sur le jeu attendu. Une image ou un clic ne prouve pas la persistance d’une donnée.

Critère proposé de préparation : chaque étape critique est réussie sans aide par les participants concernés dans les séances observées ; zéro perte de saisie confirmée, attribution involontaire, doublon d’action ou message externe non voulu. Toute difficulté répétée ou critique déclenche analyse et nouvelle recette. Ces critères sont proposés, pas déjà satisfaits ni une garantie de généralisation.

## T01 — Première connexion et découverte

**Préparation :** compte neuf TEST, aucun historique ; autre cas avec session existante, sans enregistrer l’authentification.

**Consigne neutre :** « Vous rejoignez l’équipe aujourd’hui. Accédez à votre espace avec l’accès fourni et indiquez comment vous commenceriez votre journée. »

**Observations :** compréhension de l’arrivée, repères de navigation, portée affichée, demandes d’aide, erreur de connexion et reprise sans perte de contexte. Distinguer onboarding neuf et simple reconnexion.

**Réussite :** accès sans assistance aux identifiants exceptée leur remise ; la personne retrouve le travail du jour et explique ce que couvre l’écran. Aucune information d’authentification dans les preuves. **Liens :** O01, limites de première connexion ; UX01, R05.

## T02 — Tableau de bord et priorités

**Préparation :** file personnelle vide, activité collective non vide ; deuxième cas avec retard, action du jour et RDV futur, résultats attendus connus.

**Consigne neutre :** « Vous avez peu de temps ce matin. Dites ce qui demande votre attention et ce qui peut attendre ; montrez ce qui vous permet de le savoir. »

**Observations :** distinction personnel/collectif, lecture des périodes et fuseau, priorités choisies, accès au détail et compréhension de zéro/chargement/erreur. L’indisponibilité est un cas de recette contrôlé, sans simuler un défaut observé en production.

**Réussite :** bonne portée expliquée ; retard, journée et prochain RDV retrouvés ; totaux et listes attendus concordants sur toutes les pages ; aucune déduction « équipe inactive » à partir d’une file personnelle vide. **Liens :** UX01, R01/R05.

## T03 — Qualification d’un prospect

**Préparation :** prospect fictif à rechercher, faits nouveaux et contact fictif ; cas Non calculé ; quasi-doublon réservé au test ; responsables distincts.

**Consigne neutre :** « Vous venez d’échanger avec cette structure. Retrouvez son dossier, consignez les informations de cette fiche de situation et indiquez comment vous prépareriez la suite. »

**Observations :** recherche avant création, rapprochement proposé, distinction prospect/dossier/contact, compréhension du potentiel, du statut et de la priorité, champs bloquants, responsabilité et conservation des informations. Tester calcul/adoption seulement si le rôle et le jeu l’autorisent.

**Réussite :** bonne fiche utilisée sans doublon involontaire ; informations retrouvées après réouverture ; responsables correctement expliqués ; Non calculé non assimilé à faible potentiel ; prochaine étape cohérente avec les faits fournis. Si une fonction est absente ou inaccessible, le noter sans inventer une réussite. **Liens :** UX03 ; P2 UX06/UX07/UX10 à évaluer, R03/R04.

## T04 — Planifier et retrouver un rendez-vous

**Préparation :** prospect fictif et disponibilités publiées ; deux créneaux dont un indisponible ; horaire de référence fixé.

**Consigne neutre :** « Cette structure souhaite une démonstration la semaine prochaine sur l’un de ces horaires. Organisez-la avec le collègue indiqué, puis retrouvez ce rendez-vous et notez ce qu’il faut préparer. »

**Observations :** choix du créneau et du responsable, refus éventuel, conservation de saisie, confirmation, accès à la bonne date d’agenda, contexte du prospect, notes de préparation et destinataire du rappel.

**Réussite :** un seul RDV au bon horaire, fuseau, prospect et responsable ; retrouvé sans aide ; saisie conservée après refus ; préparation récupérable ; aucun message externe non autorisé. **Liens :** UX05, R06.

## T05 — Relances et prévention des oublis

**Préparation :** prospect avec deux dossiers, action de prospect, dossier sans action ; une tâche en retard, une du jour ; destinataire interne de test pour rappel.

**Consigne neutre :** « Vous devez reprendre contact demain pour le premier de ces deux projets et vous préparer avant l’appel. Organisez ce suivi, puis indiquez ce qui reste à faire sur l’autre projet et ce qui est déjà en retard. »

**Observations :** rattachement choisi, différence échéance/rappel, responsable, interprétation de l’alerte persistante, duplication éventuelle, visibilité des retards et réception effective.

**Réussite :** action au bon dossier et au bon responsable ; autre dossier correctement identifié sans suivi ; dates distinctes conservées ; retard retrouvé ; rappel reçu par le compte de test selon préférences, sans contact externe. Distinguer réussite UX et livraison technique non encore observée. **Liens :** UX04, R03/R06.

## T06 — Pilotage collectif

**Préparation :** jeu contrôlé avec responsables différents, non attribué, sans action, inactivité et stagnation selon seuils convenus ; deux rôles de test, plusieurs pages et catégories qui se recoupent.

**Consigne neutre :** « Vous préparez le point d’équipe. Repérez les dossiers qui demandent une attention particulière, expliquez pourquoi et indiquez qui doit s’en occuper. Vérifiez les éléments sur lesquels vous vous appuyez. »

**Observations :** portée, filtres, unités prospect/dossier/action, recouvrement des catégories, accès aux éléments, limites de droits et absence de responsable. Ne pas nommer les filtres à utiliser.

**Réussite :** situations attendues retrouvées, totaux rapprochés des listes sans addition abusive, responsabilités explicites, même conclusion cohérente avec chaque rôle autorisé. Aucune donnée hors droits visible. **Liens :** UX01/UX02/UX03, R01/R02/R04.

## T07 — Fin du rendez-vous et changement de programme

**Préparation :** RDV fictif pouvant être réalisé, second RDV pour report puis annulation ; résultat fictif et prochaine étape fournis.

**Consigne neutre :** « La démonstration vient de se terminer avec le résultat décrit ici. Laissez les informations utiles à votre collègue et préparez la suite. Pour ce second rendez-vous, la structure a changé de disponibilité, puis renonce : mettez le dossier à jour. »

**Observations :** compte rendu et état enregistré, prochain engagement ou absence motivée, maintien du contexte lors du report, validation des disponibilités et historique d’annulation.

**Réussite :** résultat persistant et consultable, statut cohérent, prochaine action explicite sans doublon, modification/annulation tracées sans effacer les informations utiles. **Liens :** UX05, R06.

## T08 — Transmission et usage mobile accessible

**Préparation :** deux comptes autorisés, dossier fictif avec engagements existants ; smartphone réel, clavier et lecteur d’écran pour séquences adaptées.

**Consigne neutre :** « Votre collègue prend la suite de ce dossier. Faites ce qui vous paraît nécessaire pour qu’il sache où en est la relation et ce qui reste à faire. Retrouvez ensuite le prochain engagement sur ce téléphone. »

**Observations :** champs modifiés, responsabilités conservées, historique, capacité du second compte à reformuler ; navigation et commandes accessibles, focus, erreurs, zoom et lecture du contenu.

**Réussite :** aucun engagement perdu ou propriétaire changé involontairement ; collègue capable de retrouver la suite ; tâches critiques réalisables sur mobile et au clavier sans contenu inaccessible. Consigner séparément tout contrôle de lecteur d’écran non exécuté. **Liens :** UX03/UX04, P2 UX09 à évaluer, R04/R05.

## Restitution et suites

Créer un rapport de séance daté avec version déployée, pseudonyme participant, scénario, consigne réellement donnée, résultat, temps, erreurs, aide, preuves expurgées et état de nettoyage. Ne conserver aucun mot de passe ni identité de participant dans les rapports. Pour comparer deux versions, contrebalancer l’ordre et garder des jeux équivalents ; ne pas présenter une maquette statique comme une application fonctionnelle.

Rapprocher les résultats des observations O01–O18 et des orientations UX01–UX13. Marquer « corrigé » uniquement après reproduction initiale documentée et vérification du comportement attendu sur une version identifiée. Classer les autres constats persistants, nouveaux ou non vérifiés ; proposer des changements de priorité à arbitrer. Aucune décision utilisateur ni résultat de test n’est prérempli.
