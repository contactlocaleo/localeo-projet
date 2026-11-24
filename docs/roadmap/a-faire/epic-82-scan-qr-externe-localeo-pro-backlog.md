# EPIC 82 — Scanner un QR client depuis l’appareil photo avec Localeo Pro

## Références

- **État produit : À faire**, selon la [roadmap commune](../README.md). Cadrage du 24 novembre 2026. Identifiant 82 vérifié dans le dépôt Projet et les quatre dépôts applicatifs.
- Décisions utilisateur : inclure les QR Coffret, participant Animation et bon numérique. L’analyse démarre automatiquement après connexion si nécessaire. Le commerçant confirme l’action finale. Le navigateur mobile suffit. Le scanner historique doit continuer à fonctionner comme aujourd’hui.
- Socles : [scan professionnel](../../specifications/validation-prestations/scan-commercant.md), [E72 — accès salariés](../../specifications/epic-72-acces-salaries/README.md), [E73 — remise des bons](../../specifications/epic-73-animation-et-ou-coffrets/dotation-lots.md) et [E80 — fiabilité et reprise](../en-cours/epic-80-fiabilite-parcours-localeo-pro-backlog.md). E82 ajoute l’entrée depuis le téléphone aux trois familles de QR. E80 traite la fiabilité du parcours Animation dans Pro.

## Problème et résultat attendu

Le scanner Pro reconnaît les trois familles de QR. Depuis l’appareil photo du téléphone, les QR Coffret et Bon numérique encodent un identifiant brut. Le QR personnel du participant ouvre l’accès client dans Localeo Live.

Au comptoir, un responsable ou un salarié habilité scanne le QR du client avec l’appareil photo, ouvre le lien détecté et se connecte si nécessaire. Localeo Pro affiche directement la prestation, l’étape ou le bon à confirmer. Le commerçant peut aussi ouvrir **Scanner** dans Pro et suivre le parcours habituel.

## Périmètre

- QR clients des coffrets, participants aux animations et bons numériques. Les nouveaux rendus utilisent un lien HTTPS vers Localeo Pro. Les supports distribués précédemment restent compatibles avec **Scanner** dans Pro.
- Applications web et PWA, responsables et salariés selon leurs droits. La capture par l’appareil photo du téléphone et l’ouverture du lien dépendent du lecteur. Le navigateur reste une destination prise en charge sur iPhone et Android.
- Conserver l’analyse, la confirmation explicite, la relecture du reçu, les liens d’accès client, la saisie manuelle et le PIN. Les QR publics d’inscription, les QR de lieu et la distribution d’une application native sont hors périmètre.
- Deux étapes de livraison : d’abord le consommateur Pro compatible avec les deux formats, puis l’activation du nouveau rendu backend par environnement.

## Critères d’acceptation

| Critère | Acteur et préconditions | Action | Résultat observable |
| --- | --- | --- | --- |
| E82-CA-01 | Responsable ou salarié habilité avec un QR historique ou nouveau des trois familles | Utiliser **Scanner**, par caméra ou saisie manuelle | Parcours, résultat et confirmation habituels disponibles. |
| E82-CA-02 | Responsable ou salarié habilité connecté, nouveau QR client | Scanner avec l’appareil photo et ouvrir le lien | Pro ouvre directement la prestation, l’étape ou le bon à confirmer, sans ouvrir sa propre caméra. |
| E82-CA-03 | Session absente ou expirée | Ouvrir le lien et se connecter | Une seule analyse démarre après vérification de session et des droits. Quitter le parcours, se déconnecter ou changer de compte efface le QR en attente. |
| E82-CA-04 | Action éligible dans Pro | Vérifier puis confirmer l’action | Seule la confirmation produit l’effet métier. Pour un coffret à plusieurs prestations, l’utilisateur sélectionne celle qu’il a fournie. |
| E82-CA-05 | Refus, doublon ou réponse à une confirmation perdue | Ouvrir le QR ou reprendre l’action | État réel affiché. Le reçu incertain est relu avant un nouveau scan. Aucun effet en double ou succès supposé. |
| E82-CA-06 | Nouveau QR reconnu | Ouvrir le lien dans Pro | Le fragment optique est retiré immédiatement et traité en mémoire. Le jeton brut n’est envoyé à l’API que dans le corps JSON authentifié. |
| E82-CA-07 | Nouveau visuel d’une des trois familles | Lire le QR sur écran, email ou impression selon le support | Le lien ouvre Pro sur iPhone et Android. L’accès client, la copie d’identifiant et le PIN restent utilisables. |

## Impacts à instruire

| Sujet | Impact initial |
| --- | --- |
| Applications et domaine | Backend pour le rendu et Pro pour l’arrivée. Les domaines Exploitation et Animation portent les règles en vigueur. Marketplace et Live consomment les visuels. |
| API et consommateurs | Le contenu optique des images évolue. Les contrats JSON, identifiants bruts, droits et commandes existants sont réutilisés. |
| Persistance et migrations | Le visuel est calculé à partir du jeton existant. Les droits et données stockés sont réutilisés. |
| Démonstration et fixtures | Utiliser des QR et des comptes fictifs pour les preuves. Le générateur conserve les mêmes données et scénarios. |
| Documentation fonctionnelle | Actualiser le [guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md), relire le PDF et synchroniser sa copie embarquée. Examiner le [guide Animation](../../produit/formation/animation/guide-quotidien-animation.md) pour les consignes organisateur. |
| Exploitation | Activation par environnement après livraison du scanner compatible. Recette optique physique sur TEST, puis décision d’activation sur les autres cibles. Documenter le retour au rendu historique. |

## Passage à la spécification

Les arbitrages produit du périmètre initial sont résolus. La [spécification fonctionnelle et technique E82](../../specifications/epic-82-scan-qr-externe-localeo-pro/README.md) détaille les deux parcours, les contrats, la traçabilité des critères et les preuves restantes avant activation.
