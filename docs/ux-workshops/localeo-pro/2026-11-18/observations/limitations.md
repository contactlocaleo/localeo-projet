# Limitations et contrôles

## Non observé ou non exécuté

- **OBSERVÉ** : la caméra était indisponible dans les deux contextes Chromium automatisés. Cela ne prouve rien sur la caméra d’un téléphone physique ; seule la saisie manuelle invalide a été essayée. Preuves : [mobile](../visuels/captures-avant/04-scanner-mobile.png), [ordinateur](../visuels/captures-avant/12-scanner-desktop.png).
- **OBSERVÉ** : aucune invitation en attente sur ce compte ; l’acceptation/refus n’a pas été testée. [Liste](../visuels/captures-avant/06-invitations-mobile.png).
- **OBSERVÉ** : la connexion d’un compte de test déjà actif a été effectuée. La création du compte, son invitation initiale et la première définition d’un mot de passe n’ont pas été reproduites. [Connexion](../visuels/captures-avant/02-connexion-pro-mobile.png).
- **DÉDUIT** : la confirmation et le doublon Animation existent comme états UI, mais aucun QR participant de test permettant leur ouverture sans risque de validation réelle n’a été fourni. Le code expose ces états dans `localeo-commercant/src/features/validation/ValidationActionWorkspace.jsx:615-630`. **Non exécuté** : analyse d’un QR valide, « Valider cette étape », reçu, rejeu et erreur serveur.
- **DÉDUIT** : « Télécharger mon kit » peut appeler une commande de préparation (`kit/preparer`) ; le bouton n’a pas été activé. Aucun PDF n’a été téléchargé ni inspecté, et aucun QR de support n’a été testé. Source : `localeo-commercant/src/features/animations/components/AnimationKitSection.jsx:43-75`.
- **OBSERVÉ** : les notifications étaient consultables ; aucune notification n’a été marquée lue, supprimée ou envoyée. Aucun WebPush entrant en temps réel n’a été provoqué. [Boîte](../visuels/captures-avant/09-notifications-generales-mobile.png).
- **OBSERVÉ** : le retour après rechargement immédiat fonctionne sur la session courante. **HYPOTHÈSE** : comportement après plusieurs jours, expiration de session ou nouvelle notification ; impossible à observer le même jour sans modifier artificiellement le temps ou attendre. [Rechargement](../visuels/captures-avant/20-retour-rechargement-mobile.png).
- **OBSERVÉ** : `/animations/notifications` affichait « Animation inaccessible » en accès direct, mais aucun lien UI ne mène à cette URL ; l’onglet Notifications cible `/notifications`. Cet essai direct ne constitue pas une anomalie du parcours normal. [Écran direct](../visuels/captures-avant/08-notifications-animation-mobile.png).
- **HYPOTHÈSE** : les différences de compteurs et de dates pourraient venir d’une projection, d’un cache ou de données TEST incohérentes. Aucune cause n’a été établie ; voir [constat O03](observations-factuelles.md).

## Cible et protocole

L’URL fournie était un portail gestionnaire, non Localeo Pro, dans l’environnement observé. L’URL Pro a été trouvée dans les sources du projet puis testée avec le seul compte fourni. Les constats se limitent à ce compte, à la commune Bouliac, aux données présentes le 18 novembre 2026 et aux vues 390 × 844 / 1440 × 900. Les captures longues ne démontrent pas à elles seules un problème de recouvrement par la navigation fixe. Aucun utilisateur réel n’a été interrogé.

## Contrôles de fin d’étape

- Inspection du dépôt commerçant en lecture seule ; statut Git initial propre, branche `main`, commit `333b7607b7c0e72e2a1b4133068d37d7fc7ca760`.
- Contrôle des secrets : champs de connexion vidés avant la capture du HTTP 401 ; captures de connexion Pro prises avant saisie. Les scripts Playwright temporaires ne sont pas versionnés et sont supprimés après l’exploration.
- Validation documentaire : `py -3 scripts/check_guidance.py` réussi (103 guides, 1 389 liens, 0 erreur, 0 avertissement) ; `py -3 scripts/sync_documentation.py --check-sources` réussi (151 documents). Contrôle ciblé de 71 liens locaux : aucune cible absente ; 22 captures PNG.
- Aucun build, test métier ni recette de déploiement exécuté, puisqu’aucun code applicatif ou contrat n’a changé. Ces contrôles ne sont pas revendiqués.
