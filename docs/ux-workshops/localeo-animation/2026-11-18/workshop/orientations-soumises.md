# Orientations soumises au débat et au vote simulés

Version 1 — 18 novembre 2026. Formulées après les avis indépendants. Les priorités proposées sont des jugements de risque et de portée, pas des votes déjà obtenus. Aucune proposition n’est validée par l’utilisateur ni autorisée au développement.

| ID | Atelier | Proposition précise soumise | Priorité proposée / effort provisoire |
| --- | --- | --- | --- |
| A1 | A — Accueil | Placer les actions à traiter et l’accès à la création avant les nouvelles ; différencier succès, information et alerte. Conserver le contexte communal, les filtres et l’accès à toutes les notifications. Aucun nouveau moteur d’alertes. | P1 / M |
| A2 | A — Accueil | Permettre à chaque organisateur de choisir et déplacer les blocs de son accueil, avec restauration de la disposition standard. Personnalisation facultative. | P3 / L |
| B1 | B — Création | Enregistrer explicitement un brouillon incomplet dès modèle, nom et commune renseignés ; reprendre les champs réellement enregistrés. Afficher état de sauvegarde et éléments manquants. Aucun envoi ni publication implicite ; les contrôles serveur de publication restent inchangés. Contrat de brouillon partiel à spécifier avant développement. | P1 / L |
| B2 | B — Publication | Expliquer tôt le résultat de la création : brouillon préparé, puis accords, puis publication. Remplacer les diagnostics techniques par action + responsable + raison du blocage + lien ciblé ; préciser les termes de dotation sans changer ses modes. Distinguer sélection, invitation, accord, préparation et activation seulement si cette dernière est connue. Ne promettre aucun délai humain non mesuré. | P1 / M |
| B3 | B — Passeport | Proposer au choix du seuil une valeur initiale compatible avec les commerces sélectionnés et expliquer la conséquence. Si la sélection change, signaler l’incompatibilité et demander un ajustement explicite, sans changer silencieusement une règle déjà choisie. Garder le contrôle serveur. | P1 / S |
| B4 | B — Création rapide | Ajouter un mode facultatif « formulaire unique » pour utilisateurs fréquents, avec les mêmes champs, validations, aperçu et confirmations que le parcours guidé, qui reste disponible. | P2 / L |
| C1 | C — Ajout individuel | Depuis le sélecteur, proposer « Mon commerce n’est pas dans la liste » et un parcours de demande individuelle de référencement avec suivi. Réutiliser la fonction canonique disponible après vérification de sa portée ; une demande ne rend pas le commerce éligible, activé ou participant. Ne pas créer un compte actif ni envoyer d’invitation automatiquement. | P1 / L |
| C2 | C — Import | Préassocier les colonnes reconnues du modèle fourni, laisser vérifier/corriger ; distinguer colonne requise et cellule requise ; présenter les limites de rapprochement. Signaler la similitude nom/adresse comme doute à examiner, sans fusion ni rejet automatiques, en conservant les conflits forts email/SIRET. Confirmation explicite des lignes. | P1 / L |
| C3 | C — Relances | Ajouter des relances planifiées facultatives : calendrier, aperçu des destinataires, confirmation de l’organisateur, possibilité d’annuler et contrôle des droits/plafonds à l’envoi. Aucun accord déduit d’une relance. | P2 / L |
| D1 | D — Communication | Diagnostiquer et rétablir la lecture Communication en erreur 500, vérifier préparation/aperçu et envoi sur destinataires isolés ; distinguer échec de lecture et envoi incertain, préserver le contexte et proposer une reprise/support. Pas de répétition automatique d’envoi. | P0 / M, à réestimer après diagnostic |
| D2 | D — Suivi | Faire aboutir « Consulter le suivi » au suivi opérationnel, avec accès distinct au bilan. Préserver les définitions, périmètres et dates des indicateurs ; aucun indicateur temps réel inventé. | P1 / S |
| E1 | E — Fin | Expliquer près de l’action les états « période finie », « clôturée », « terminée », « archivée », leurs conséquences et la prochaine tâche. Réutiliser les dossiers à résoudre existants et leur responsable connu ; remplacer le jargon de gel par une explication compréhensible. Conserver confirmation définitive, distinction informer/remettre et droits métier. | P1 / M |
| E2 | E — Automatisation | Ajouter une clôture programmée facultative à une date confirmée, avec précontrôle, avertissement préalable et annulation possible avant exécution ; ne pas tirer au sort ni déclarer de remise automatiquement. Nouvelle règle serveur à concevoir, avec traitement d’incidents en cours. | P2 / XL |
| F1 | F — Pilotage | Enregistrer et partager des vues de liste filtrées au sein de l’organisation, tout en gardant filtres actifs visibles, retour conservé, droits et réinitialisation. | P2 / M |
| F2 | F — Échéances | Ajouter un calendrier transversal des dates et échéances avec retour vers les actions existantes, en complément de la liste et sans remplacer les statuts métier. | P2 / L |
| G1 | G — Mobile | Ajouter dans le détail mobile des accès aux tâches courantes de l’animation, selon droits et état, tout en gardant le sélecteur complet et un repère de rubrique. Vérifier téléphone réel, clavier et lecteur d’écran avant de conclure à un gain. | P2 / M |
| G2 | G — Prise en main | Proposer une visite guidée facultative de première utilisation, quittable/rejouable, sans blocage de la navigation ni répétition imposée. Elle complète les aides contextuelles ; elle ne remplace pas la correction des obstacles. | P3 / M |

## Désaccords soumis aux participants

- B1 peut réduire la perte de travail mais élargit le contrat de création ; E3 demande de conserver tous les prérequis de publication.
- C1 répond au petit volume ; E2 demande de vérifier la responsabilité canonique avant d’ajouter un formulaire.
- C2 aide au contrôle de données ; E5 rappelle que deux propositions d’import ne prouvent pas deux fiches effectivement créées.
- D1 est une panne observée dans une session TEST, pas une mesure de disponibilité générale. La priorité P0 concerne la capacité à communiquer si elle est incluse dans le lancement à 500 organisations.
- E2 et C3 peuvent alléger le travail récurrent ; des profils métier préfèrent garder la décision d’agir au moment de l’événement.
- A2, B4, F2 et G2 offrent du confort mais ajoutent des surfaces à apprendre et maintenir ; ce coût doit être comparé aux simplifications locales.

Vote demandé : une position POUR / CONTRE / ABSTENTION par participant et par orientation, avec un argument propre au rôle. Le seuil reste sept POUR sur douze, quel que soit le nombre d’abstentions. Aucun résultat cible n’est demandé.
