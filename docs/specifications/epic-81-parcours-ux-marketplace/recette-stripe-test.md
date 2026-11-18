# E81-CA-08/09 — Protocole de recette de la frontière Stripe

Ce document prépare la recette ; **aucun appel, achat, session, paiement ou webhook n'a été exécuté pour EPIC 81**. L'[audit initial](../../ux-workshops/marketplace/2026-11-18/observations/parcours-achat-stripe.md) s'arrêtait avant le bouton final. Le `POST /public/gestion-achats/paiements/initialiser` crée un achat et une session avant la redirection : une simple visite de la page Stripe n'est donc pas une lecture sans effet.

## Conditions à établir avant le premier appel

1. Identifier par écrit l'environnement TEST visé, l'API réellement appelée par la configuration publique, le compte Stripe **test** et les responsables habilités. Ne pas supposer que le domaine web TEST pointe vers une base isolée.
2. Confirmer que les achats créés sont isolés des commandes réelles, des reversements, de la facturation, des e-mails/SMS externes et des tableaux de bord d'exploitation. Décrire les webhooks, les traitements asynchrones et le nettoyage des objets de test. Utiliser uniquement des identités fictives autorisées et des destinations de notification contrôlées.
3. Relever l'état initial des tables/projections d'achat et les identifiants de corrélation. Préparer une clé d'idempotence unique par scénario et la procédure de reprise ; la répétition d'une requête incertaine ne doit pas créer implicitement un nouvel achat.
4. Faire approuver l'innocuité documentée par le responsable de cet environnement et fixer la procédure d'arrêt si un effet imprévu apparaît. **Sans ces preuves, ne pas envoyer le POST.** Une validation UX de l'orientation ne tient pas lieu de cette autorisation technique.

## Scénarios seulement après levée des conditions

| Scénario | Action en TEST isolé | Preuves attendues |
| --- | --- | --- |
| Initialisation | Soumettre une offre et des coordonnées fictives autorisées une seule fois. | Un achat de test corrélé, une session Stripe test, une URL validée ; aucune commande réelle. |
| Reprise | Répéter uniquement selon la procédure d'idempotence, puis simuler une réponse réseau incertaine. | Une seule intention d'achat ou le comportement contractuel explicite ; aucun doublon silencieux. |
| Annulation/échec | Revenir de Stripe test par le chemin prévu, sans moyen bancaire réel. | Message exact, état backend vérifié, absence de coffret utilisable et possibilité de reprise appropriée. |
| Succès | Utiliser uniquement le mécanisme de test approuvé, sans facturation réelle. | Confirmation par l'état backend/webhook plutôt que par l'URL de retour ; cohérence achat, coffret et notifications contrôlées. |
| Nettoyage | Appliquer la procédure propre à l'environnement. | Objets de test identifiés et traités, sans altérer les données d'exploitation. |

Consigner pour chaque essai : date, environnement, versions/commits backend et frontend, configuration publique pertinente, identifiants de corrélation non sensibles, requêtes et réponses expurgées, états avant/après, résultat attendu/réel, anomalie et vérification du correctif. Aucun secret, jeton d'accès, numéro de carte ni donnée personnelle réelle dans le rapport.

**État au cadrage/à l'implémentation locale : porte ouverte.** L'innocuité et l'environnement n'ont pas été confirmés dans ce dossier ; E81-CA-09 ne doit pas être annoncé vérifié sur la base de tests simulés ou du seul rendu frontend.
