# Harmonisation UX de la marketplace — 13 septembre 2026

Ce lot applique les onze axes de l’audit premium en conservant la direction visuelle Localeo : bleu, crème, orange lisible, photographies et contours sobres.

| Axe | Comportement livré |
| --- | --- |
| Confiance | Huit documents publics V1 complets, sommaire, tableaux accessibles et PDF téléchargeables. |
| Promesse du coffret | Distinction contenu inclus / exemples indicatifs, promesse publiée, durée réelle et résumé pratique avant achat. |
| Découverte | Coffrets et communes accessibles sans localisation ; adresses et animations conservées dans une ville sans coffret. |
| Recherche | Page de résultats avec filtres de contenu, commune, budget et type de coffret ; retour aux résultats et saisie conservée. |
| Hiérarchie | Introduction mobile raccourcie, offre visible avant les explications, entrée organisateur plus discrète. |
| Visuels | Photo propre au coffret prioritaire, attente animée, état explicite si aucun visuel n’est disponible. |
| Cohérence | Actions rectangulaires, contrastes et focus clavier renforcés, fil d’Ariane sans doublon. |
| Comparaison | Tous les coffrets en grille ; toutes les adresses accessibles et expériences reliées aux coffrets dans les carrousels partagés. |
| Preuve | Mise en avant nommée « À découvrir », aucun classement présenté comme une recommandation ; chiffres correctement situés et témoignages publics conservés si les métriques sont indisponibles. |
| Cadeau | Message facultatif, aperçu, impression, téléchargement PNG et partage natif lorsque disponible. QR explicitement valide et date de validité requise. |
| Après-achat | États de paiement précis, droits issus de la réponse vérifiée, accès direct et renvoi du lien, réception de l’e-mail annoncée sans promesse instantanée. |

## Contrats et limites

La recherche parcourt les API publiques paginées, avec annulation des requêtes et cache. Le parcours est borné à 25 pages par source ; un résultat incomplet ou une source indisponible est annoncé et le filtre de commune permet de réduire le catalogue. Aucun nouveau moteur de recherche backend n’est introduit.

Le nombre de personnes et les conditions de réservation ne sont pas des champs structurés disponibles dans le contrat actuel. La fiche invite à consulter les expériences et les adresses ; elle ne déduit pas ces informations. Les photographies spécifiques et les promesses utilisent les contenus réellement publiés.

La carte cadeau est préparée localement après achat. Le message ne transite pas par le serveur et le jeton de consultation n’est pas incorporé à l’export. Le partage nécessite une action de l’utilisateur. L’envoi programmé, évoqué comme une option ultérieure dans l’audit, nécessiterait un contrat et un traitement backend dédiés.

## Provenance des documents publics

Cette description du 13 septembre concernait l’ancien import statique. Il est désormais désactivé. Le corpus est centralisé sous `docs/juridique` dans `localeo-projet` ; la procédure courante de [publication juridique Marketplace](../../../juridique/publication/marketplace.md) utilise les PDF et le catalogue canoniques.



Cette intégration restitue la version fournie ; elle n’ajoute pas les traitements métier éventuellement décrits dans le corpus.

## Vérification

`npm test` exécute ESLint, les tests de sécurité et de logique, les parcours navigateur Playwright et les tests serveur. Les tests navigateur utilisent un serveur et des réponses API isolés, sans paiement ni requête vers un backend réel. Ils couvrent les nouveaux parcours, le clavier, les erreurs et plusieurs largeurs mobiles et PC. `npm run build:prod` vérifie également la compilation de production.

Validation du lot : ESLint, 59 tests de sécurité et de logique, 11 tests serveur et compilation de production réussis. Les 129 scénarios navigateur ont été exécutés ; les échecs de la campagne complète ont été corrigés ou diagnostiqués, puis rejoués séquentiellement avec les parcours concernés. La dernière relance passe ses 12 scénarios, dont le bouton d’achat entièrement visible à 320 × 568 px, le zoom à 200 %, les carrousels, les retours depuis Localeo Live, la confirmation et la carte cadeau. Aucun échec de test ne reste non résolu.
