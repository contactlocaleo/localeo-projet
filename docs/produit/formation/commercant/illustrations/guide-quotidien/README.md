# Illustrations du guide quotidien commerçant

Captures réalisées le 26 septembre 2026 dans [Localeo Commerçant — test](https://test-commercant.localeo.city), version affichée `v1.0.0+d09fca1f`, avec le commerce fictif **Le Fournil des Tilleuls** du jeu de données installé.

| Fichier | Vue illustrée |
| --- | --- |
| `01-accueil.png` | Accueil et accès aux principales rubriques |
| `02-validation.png` | Prestation disponible après lecture d’un QR de coffret |
| `03-animation.png` | Préparation et mission pour un passeport commerçant |
| `04-reversements.png` | Sommes attendues et historique des versements |
| `05-horaires.png` | Informations pratiques de la page publique |
| `06-publication.png` | Enregistrement du brouillon ou demande de publication |
| `08-activite.png` | Indicateurs d’activité, achats et prestations réalisées |
| `10-alertes.png` | Activation des alertes d’achat dans Compte |
| `11-facturation.png` | Navigation entre les rubriques de facturation |
| `12-invitations.png` | Navigation entre invitations, animations et notifications |

Ces captures sont recadrées depuis les écrans réels, sans modification des libellés. Les montants et noms sont des exemples. Aucun identifiant de connexion, mot de passe ou QR personnel n’est inclus. La consultation n’a validé aucune prestation et n’a modifié aucune participation ni aucun paiement.

Le guide détaillé compte huit pages et neuf captures. La capture `04-reversements.png`, utilisée dans l’édition courte précédente, reste disponible comme illustration complémentaire.

Les fonctionnalités ont été recoupées avec les routes et composants de l’application. Le profil capturé n’a aucune demande de facture ni invitation en attente : ces écrans de détail n’ont pas été mis en scène. Chorus Pro et l’assistant d’émission sont décrits comme options conditionnelles ; aucune capture ne prétend les montrer activés. Le parcours de connexion du guide suit l’écran actuel email/mot de passe, sans reprendre la carte QR mentionnée par d’anciens documents.

La modification porte sur le guide et ses illustrations dans `localeo-projet`. Elle ne change aucun comportement applicatif, contrat, migration, configuration ou générateur de données et n’entraîne aucun déploiement.

Lors d’une mise à jour, utiliser un profil de démonstration, relever la version affichée et recapturer uniquement les zones utiles. Conserver les noms des fichiers, mettre à jour les légendes du [guide source](../../guide-quotidien-commercant.md), puis régénérer et contrôler visuellement les huit pages du PDF.
