# Limitations et précautions

- **OBSERVÉ** : l'exploration s'est déroulée sur TEST avec un seul compte. Les permissions et la vision d'un autre rôle n'ont pas été vérifiées.
- **OBSERVÉ** : la session mobile Playwright à 390 × 844 est restée sur « Ouverture de votre espace commercial… » ; une nouvelle navigation a expiré. Aucune capture mobile exploitable n'a été produite. **HYPOTHÈSE** : lenteur/transitoire réseau ou session ; aucune cause produit attribuée.
- **OBSERVÉ** : la lecture de Prospects a demandé environ 12 secondes avant l'affichage de 1 558 résultats dans une tentative. Cette mesure ponctuelle ne constitue pas une mesure de performance fiable. Les captures 03 et 08 peuvent documenter un chargement initial.
- **OBSERVÉ** : l'agenda a été consulté sur la semaine du 16 au 22 novembre. La navigation vers la semaine du rendez-vous fictif a été interrompue par un délai d'outil ; son affichage dans l'agenda n'est pas prouvé.
- **DÉDUIT du code** : modification, report, annulation, prise en charge et compte rendu d'un rendez-vous disposent de commandes. **Non vérifié en UI** : ces actions, tout comme la transition de statut et l'affectation du prospect.
- **Non exécuté** : import CSV, calcul ou adoption de qualification, notification WebPush/e-mail, suppression/archivage, vraie première connexion d'un compte neuf, test clavier/lecteur d'écran, test utilisateur.
- **HYPOTHÈSE** : la distinction responsable du prospect / responsable du dossier pourrait dérouter. Elle doit être testée auprès d'utilisateurs ; la spécification permet deux propriétaires.

## Objets fictifs laissés dans TEST

Ces objets ont été créés uniquement pour l'exploration, avec libellés `UX TEST`, sans coordonnées réelles ni contact externe :

| Objet | Identifiant de test | État vérifié |
| --- | --- | --- |
| Prospect « UX TEST 2026-11-19 CRM exploration » | `bdd06ffc-59f2-4869-80cd-a74a4ce4b12f` | Actif, Bordeaux, responsable du prospect non attribué. |
| Dossier « Exploration UX — dossier fictif » | Identifiant non relevé | Animation, responsable de dossier : compte connecté. |
| Contact « Contact UX Test » | Identifiant non relevé | Adresse fictive sous `example.invalid`. |
| Action « UX TEST — préparer la démonstration fictive » | Identifiant non relevé | Préparation interne, prévue le 20 novembre 2026 à 14 h, rappel à 9 h, heure de Paris. |
| Rendez-vous « UX TEST — démonstration fictive » | `408d75fc-f0d0-4259-b103-2eaeacf69c0d` | Réservation confirmée le 26 novembre 2026 à 10 h, heure de Paris ; aucun message au prospect selon le formulaire. |

Aucune fiche, tâche ou rendez-vous préexistants n'a été modifié. Le rendez-vous fictif et l'action restent dans TEST ; aucune annulation ou suppression n'a été réalisée faute de vérification de leur parcours UI. Cette dette de nettoyage devra être traitée avec ces identifiants, sans confondre ces objets avec des données commerciales.
