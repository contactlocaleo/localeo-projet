# Cartographie des 20 parcours demandés

Codes : **UI** = parcours observé avec Playwright ; **formulaire** = saisie ouverte, sans validation finale ; **code** = possibilité repérée localement sans recette réelle ; **non vérifié** = absence de preuve suffisante. Les numéros de capture renvoient à `../visuels/captures-avant/`.

| # | Parcours | État et preuve |
| --- | --- | --- |
| 1 | Première connexion | UI : formulaire puis arrivée sur Aujourd'hui ; capture 01. Première connexion d'un compte neuf non testée. |
| 2 | Découverte du tableau de bord | UI : trois périodes, portée Mes actions/Équipe, indicateurs repliés ; 01. |
| 3 | État global de la prospection | UI partielle : Suivi et ses filtres, 03 ; indicateurs partagés repérés dans 01 mais non ouverts. |
| 4 | Actions prioritaires | UI : sections En retard/Aujourd'hui/À venir, Rappels et priorité de dossier ; 01, 05, 14. |
| 5 | Recherche d'un prospect | UI : recherche « Léognan », deux résultats ; 10. |
| 6 | Création d'un prospect | UI : fiche fictive créée, premier dossier associé ; 09, 11. |
| 7 | Qualification | UI partielle : liste de qualification et section de fiche repérées ; 06, 11. Calcul/adoption non exécutés. |
| 8 | Modification du statut | Code : transition de dossier présente ; aucun statut existant modifié. |
| 9 | Ajout d'un contact | UI : contact fictif ajouté ; 12, 11. |
| 10 | Consultation de l'historique | UI : section Historique des échanges de la fiche fictive, initialement vide puis événement de réservation ; 11, 14. |
| 11 | Création d'une tâche | UI : action fictive enregistrée pour le 20 novembre ; 13, 14. |
| 12 | Planification d'une relance | UI : champs « Action prévue le » et « Me rappeler le », avec rappel antérieur à l'action ; 13. Notification effective non attendue/testée. |
| 13 | Tâches en retard | UI : liste Rappels avec badges En retard ; 05. |
| 14 | Création d'un rendez-vous | UI : réservation fictive sur créneau publié du 26 novembre ; 15 et confirmation textuelle sur fiche. |
| 15 | Agenda | UI : vue semaine, filtre collaborateur et rendez-vous existant annulé ; 04. Recherche du nouveau rendez-vous interrompue. |
| 16 | Modification d'un rendez-vous | Code : action Modifier visible dans `crm-agenda.js` ; non vérifié dans l'UI. |
| 17 | Préparation d'une démonstration | UI partielle : note facultative de rendez-vous et tâche de préparation fictive ; 13, 15. Parcours complet non vérifié. |
| 18 | Compte rendu après rendez-vous | Code : action Réaliser avec compte rendu obligatoire ; non exécutée, le rendez-vous fictif est futur. |
| 19 | Affectation d'un prospect | UI : fiche créée sans responsable du prospect, bouton Attribuer un responsable ; 11. Affectation effective non exécutée. |
| 20 | Suivi collectif | UI partielle : portée Équipe, agenda et responsable des rappels visibles ; 01, 04, 05. Portée Équipe non ouverte en recette. |

Ces états portent sur le compte utilisé et l'environnement TEST aux dates indiquées, pas sur tous les profils ni toutes les données du CRM.
