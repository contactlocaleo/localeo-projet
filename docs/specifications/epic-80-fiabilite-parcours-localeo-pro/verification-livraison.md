# E80 — vérification de la réalisation locale

18 novembre 2026. Source des critères : [backlog E80](../../roadmap/en-cours/epic-80-fiabilite-parcours-localeo-pro-backlog.md) ; [spécification](README.md). Ce bilan décrit les changements locaux, sans recette sur environnement partagé ni déploiement. L'epic reste **En cours**.

## Réalisation

- **B1 / CA-01 :** le scanner Pro remplace le rejet « pack » hors contexte par un message commun qui indique le QR personnel du participant et le geste de reprise. La caméra propose aussi la saisie manuelle en cas de lecture impossible. La validation n'est pas appelée pour un rejet local ; confirmation, reçu et état incertain existants sont conservés.
- **C1 / CA-05–06 :** les notifications Animation précèdent PIN quand les deux produits sont autorisés ; PIN vide est repliable, consultable et actualisable. Une page PIN vide au sein d'un total non nul garde sa pagination. La boîte Animation présente les actions autorisées encore ouvertes depuis les demandes de participation, indépendamment des messages lus. L'accueil conserve sa liste d'actions.
- **D1 / CA-07 :** l'accueil et la liste des animations lisent désormais le même ensemble complet de pages et classent avec `animationCategory`. La pagination de la liste s'applique ensuite à chaque catégorie. Le constat historique 2/3 en TEST n'a pas été reproduit avec le même compte et le même instant ; sa cause initiale demeure inconnue.
- **E1 / CA-11 :** le service de kit présente début et fin en heure de Paris dans `modeOperatoire`, donc dans la réponse JSON et l'archive HTML. Une date civile conserve son jour ; un timestamp UTC naïf ou avec offset est converti comme instant. Aucune borne métier ne change. Le guide commerçant corrige les noms des supports qu'il annonçait.
- **E1 / présentation :** les consignes du kit et les dates sont visibles près du téléchargement. Le texte distingue QR public d'inscription/support et QR personnel à valider ; il sépare téléchargement et déclaration « Je suis prêt ».
- **F1 / reprise :** une expiration de session conserve le seul chemin de la page protégée pour la reconnexion. Les paramètres, données de scanner et liens externes ne sont pas conservés ; la page et ses droits sont relus après connexion. Une déconnexion volontaire repart de l'accueil.
- **B1/F1 existants :** le parcours local conserve la confirmation séparée et la vérification d'un reçu incertain. Le retour de visibilité de l'accueil et des notifications relit les données. Ces garanties ne prouvent pas le fonctionnement sur téléphone physique ou en réseau réel dégradé.

## Matrice des critères et preuves

| Critère | Résultat local et preuve | Limite / suite | Contrat, données, démonstration, exploitation |
| --- | --- | --- | --- |
| CA-01 | **Réussi localement :** `qr-identifiers.spec.js` vérifie le texte de reprise et zéro ouverture de transaction pour un QR inconnu. | Vérifier les autres formes de rejet sur téléphone. | Aucun contrat ni donnée modifié ; guide Pro mis à jour. |
| CA-02 | **Partiel :** parcours navigateur existant de QR autorisé, reconnaissance puis confirmation, réussi. | Double clic, doublon et résultat serveur réel non éprouvés dans cette livraison. | Règle backend et reçu existants conservés. |
| CA-03 | **Partiel :** `suivi-animation.spec.js` réussi : perte de réponse, lecture indisponible, aucun renvoi ni succès. | Réseau et reçu réels à éprouver. | Pas de changement de contrat ou de persistance. |
| CA-04 | **Non exécuté :** caméra et aides techniques sur téléphone physique. | Recette appareil requise. | Aucune configuration caméra modifiée. |
| CA-05 | **Réussi localement :** test UI de message marqué lu avec action de préparation encore visible ; lien direct vers l'état courant. | Cas réel et actualisation sur un compte TEST à confronter. | Lecture supplémentaire des demandes, cache de session partagé ; aucun nouveau champ ou contrat. |
| CA-06 | **Réussi localement pour l'ordre et PIN vide :** tests `NotificationsPage` et `PinNotifications`. | Lien profond et profils à vérifier en recette intégrée. | API PIN/Animation inchangées, pagination conservée. |
| CA-07 | **Réussi localement pour le périmètre :** même chargement complet et classement partagés par accueil et liste ; test de 21 animations sur deux pages vérifie les onglets globaux et la pagination locale. | Vérifier l'écart historique 2/3 en TEST au même instant ; la cause initiale n'est pas attribuée. | Aucun calcul métier ou endpoint ajouté ; coût de lecture de toutes les pages à mesurer avant extension. |
| CA-08 | **Partiel :** test existant `model.test.js` réussi pour fin dépassée, EN_COURS et avenir. | Règle backend et transition Paris sur données TEST à confronter. | Données et statuts inchangés. |
| CA-09 | **Partiel :** parcours `suivi-animation.spec.js` réussi pour invitation/préparation et reprise locale. | Incomplet/attente/prêt sur tous modèles et compréhension réelle à vérifier. | E56/E78 gardent les transitions ; aucune migration. |
| CA-10 | **Partiel :** archive kit synthétique et noms réels du producteur contrôlés ; consignes visibles, téléchargement distinct de « Je suis prêt » dans le code. | PDF et impression autorisés sur cible réelle non exécutés. | Générateur de kit inchangé sauf texte des dates ; aucun schéma. |
| CA-11 | **Réussi localement :** test applicatif JSON + archive HTML, hiver/été, changement de jour, date civile/invalide/UTC naïf. | Vérifier les bornes sur le kit de recette autorisé. | Guide fonctionnel mis à jour ; aucun changement de stockage ni de contrat. |
| CA-12 | **Partiel :** protections existantes relues ; parcours synthétique de réponse perdue réussi ; chemin protégé conservé après expiration, sans paramètres. | Expiration réelle et retour après semaines non exécutés. | Session et cache par compte conservés ; pas de QR dans URL. |
| CA-13 | **Non exécuté :** observation de commerçants et recette des aides techniques. | Condition avant extension à 500 commerces. | Aucune mesure d'adoption ou de vitesse revendiquée. |

## Contrôles exécutés

- Backend : `py -3 scripts/validation/test_isolated.py tests/application/animation_locale/test_kit_animation_commercant.py -q` : **30 réussis**, après le dernier changement du test de date. `tests/architecture`, classes de domaine et couverture des use cases : **755 réussis** avant cet ajout d'assertion, sans changement de code entre les deux passages hormis le test.
- Pro : `npm test` complet après les cinq orientations : **95 fichiers, 688 tests réussis**. Vitest ciblé (`NotificationsPage`, `PinNotifications`, `AnimationPages`, `AnimationKitSection`) : **40 réussis**. Build isolé `node scripts/build-check.mjs` : **réussi**.
- Navigateur Pro : `qr-identifiers.spec.js` et `suivi-animation.spec.js` : **9 parcours Chromium réussis** après les changements, sur scanner, accueil, préparation et réponse incertaine. Le premier passage ciblé avait eu un échec de sélecteur de test, corrigé avant le passage complet.
- Projet : `py -3 scripts/check_guidance.py` et `py -3 scripts/sync_documentation.py --check-sources` : **réussis**. Aucun test applicatif n'est remplacé par ces contrôles de liens.

Aucun commit, push, déploiement, migration ou génération sur environnement réel n'a été effectué.
