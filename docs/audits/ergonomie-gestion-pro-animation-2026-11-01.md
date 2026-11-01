# Audit ergonomique — Localeo Pro et Localeo Animation

Date : **1er novembre 2026**. Périmètre : applications de gestion sur PC et
mobile, avec Localeo Pro comme référence de présentation et corrections dans
les deux applications. Bases : Pro `6c7489e`, Animation `9b0eb7a`, complétées
par les travaux locaux conservés, notamment le défilement unique Animation.
Cet audit décrit le code local et des recettes isolées, pas un déploiement.

## Référentiel et méthode

Lecture des composants partagés et des parcours, revue indépendante des
confirmations et reprises d’erreur, puis tests navigateur avec API synthétiques.
Les critères retenus sont : repères de navigation stables, action principale
identifiable, commandes nommées, confirmations explicites, visibilité des états,
reprise après erreur, usage clavier, lisibilité au zoom et accès tactile.

Références : [WCAG 2.2](https://www.w3.org/TR/WCAG22/), notamment noms des champs,
focus et identification des erreurs ; [recomposition du contenu à 320 pixels](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html),
[fenêtres modales accessibles](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
et [cibles de 44 × 44 pixels](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html).
Le confort tactile de 44 pixels est une convention Localeo, correspondant au
critère renforcé AAA, et non une présentation du minimum AA. Les essais de texte
à 200 % complètent les petits formats ; ils ne constituent pas une certification
WCAG ni un audit exhaustif RGAA.

## Constats et corrections

| Sujet | Écart démontré | Correction appliquée |
| --- | --- | --- |
| Navigation clavier Pro | Aucun accès d’évitement ; Échap dans Compte pouvait laisser le focus sur le corps de page. | Lien « Aller au contenu » et restitution du focus au déclencheur du menu. |
| Menus Pro sur écran bas | La déconnexion pouvait sortir de l’écran en paysage avec texte agrandi. | Menu Compte borné et défilant ; actions conservées et accessibles. |
| Lisibilité Pro | Champs à taille fixe malgré le zoom ; pied de page débordant à 320 pixels avec texte agrandi. | Tailles adaptatives et retour à la ligne à la source ; liens du compte portés à 44 pixels. |
| Navigation mobile Pro | Au texte agrandi, les mots du menu se coupaient en plusieurs morceaux et la réserve sous le contenu était fixe. | Grille adaptative comme Animation ; réserve ajustée à la hauteur réelle du menu pour garder les dernières actions accessibles. |
| Reprise d’erreur Pro | Les prestations ne proposaient aucune reprise après un échec de lecture. | « Réessayer » relance uniquement le GET ; aucune commande métier rejouée. |
| Erreurs de formulaire Pro | Le retour du changement de mot de passe restait sans focus explicite. | Réutilisation du message partagé, avec focus sur le retour et présentation homogène. |
| Confirmations salariés Pro | Confirmation générique après une longue liste, hors champ et sans focus. | Confirmation auprès du salarié, verbe, cible et conséquences explicites ; focus et défilement, puis retour au déclencheur après abandon. |
| Navigation Animation au zoom | En-tête et barre mobile trop hauts ; libellés découpés dans quatre colonnes. | Repères compacts ; disposition adaptative des mêmes destinations sans supprimer les accès. |
| Alertes Animation | Actions et titres comprimés en colonnes étroites, notamment Publication/Actualiser. | Retour à la ligne et place réservée au message ; pictogramme et action lisibles. |
| Reprise de configuration Animation | Après un conflit sur les lots, une action pouvait être recouverte par la barre fixe. | La zone de défilement réserve la hauteur réelle de la barre lors du positionnement d’une action ; reprise vérifiée par clic ordinaire. |
| Liste Animation | Filtres sans nom accessible et contraste insuffisant du badge Brouillon. | Filtres nommés et contraste renforcé ; vérification automatique ciblée de la liste. |
| Fenêtres Animation | Des fenêtres manuelles n’isolaient pas le clavier et ne rendaient pas le focus. | Primitive `ManagementDialog` commune : nom accessible, focus contenu, fond isolé, Échap avant commande et retour au déclencheur. |
| Retrait d’un commerçant | Annuler le prompt de motif déclenchait néanmoins le refus ; boutons et cases sans nom accessible. | Abandon sans requête et commandes nommées avec la cible. |
| Actualités Animation | Bouton de publication blanc sur orange ; commande trop large au zoom ; confirmation générique. | Action principale bleue comme Pro, contenu adaptable, confirmation « Publier », « Programmer », « Masquer » ou « Supprimer ». |

Les modales communes couvrent notamment la suppression des brouillons,
la préparation de publication, les invitations commerçants, les actualités,
la commande de lots et les demandes de factures. Les boutons, champs et
messages sont corrigés dans leurs composants ou styles sources, sans ajout
d’une feuille globale masquant les défauts par accumulation de surcharges.

## Principes conservés et harmonisés

- Sur PC : rubriques regroupées, titres et contexte de travail, accès secondaire
  distinct de l’action principale ; tableaux pour les données comparables.
- Sur mobile : navigation principale accessible, filtres repliables, listes
  présentées en fiches lorsque nécessaire, champs et actions dans la largeur.
- Clavier : focus visible, confirmations accessibles, fermeture volontaire et
  retour au point d’entrée ; pas de validation déclenchée par la fermeture.
- Retours : chargement, vide, erreur et succès distincts ; relecture explicite
  après une lecture échouée, sans répétition automatique d’une écriture.
- Commandes sensibles : conséquence et cible annoncées, état en cours visible,
  doubles activations bloquées, droits et versions du serveur préservés.

Pro et Animation gardent leurs tâches et leurs composants propres. L’homogénéité
porte sur les comportements observables, les repères, les tailles et les états,
sans imposer les mêmes fonctionnalités à un commerçant et à un organisateur.

## Preuves et limites

Les bancs utilisent des comptes et données synthétiques, sans fichier
d’environnement opérateur ni réseau métier réel. Les reproductions avant
correction couvrent notamment le focus perdu, l’absence de lien d’évitement,
le menu inaccessible en paysage, les confirmations salariés et les débordements
au zoom. Les scénarios d’abandon vérifient l’absence de commande.

| Dépôt / contrôle | Résultat |
| --- | --- |
| Pro — `npx vitest run --config scripts/audits/vitest-ergonomie.config.mjs --maxWorkers=2` | **36 tests réussis** dans 7 fichiers : cadre, compte, navigation, focus, salariés et reprise de lecture des prestations. Configuration isolée versionnée, sans `.env` opérateur. |
| Pro — Playwright : `management-ergonomics`, `employee-confirmation`, `business-ux`, `mobile-header`, `operational-ux` | **32 scénarios distincts réussis** ; 16 écrans métier à 390/1024/1440 pixels, contrôles clavier et zoom 320/390/1280/1440, paysage 844 × 390. Axe ne détecte aucune violation dans les états contrôlés. Build isolé réussi. |
| Pro — `perimetres` | **4 scénarios Animation seule réussis** ; travaux locaux antérieurs conservés. |
| Animation — `node --test tests/*.test.mjs`, TypeScript et ESLint | **295 tests unitaires réussis**, types et lint réussis. Adaptation du chargement CSS du banc d’invitations, sans changement de ses assertions. |
| Animation — `node scripts/build-generation-tests.mjs`, puis `WORKSPACE_CASE=ergonomics node tests/browser/animation-workspace-ux.mjs` | Build isolé réussi et **10 formats réussis**, de 320 à 1600 pixels, dont paysage 844 × 390 et texte à 200 %. Axe ne détecte aucune violation sur la liste et ses filtres dans ces états. |
| Animation — même banc avec `WORKSPACE_CASE=shell`, puis `WORKSPACE_CASE=scroll` | **8 parcours du cadre partagé et 8 parcours de défilement réussis** ; régression des travaux locaux antérieurs vérifiée. |
| Animation — `node tests/browser/news-action-feedback.mjs` | **165 contrôles réussis** : publier, annuler, reprise du focus, confinement clavier et verrouillage pendant la commande, succès/échec, 1280/390/320 pixels dont texte à 200 %. |
| Animation — `node tests/browser/finance-workspace-ux.mjs` | **215 contrôles réussis** : lecture, filtres, droits, confirmation de demande de factures, Échap et abandon sans écriture, PC/mobile/texte agrandi. |
| Animation — `node tests/browser/merchant-consent-ergonomics.mjs` | **4 formats réussis** : annuler le refus ou l’acceptation d’un retrait n’émet aucune commande ; refus confirmé envoyé une fois ; confirmation d’annulation d’invitation accessible. |
| Animation — `node tests/browser/passport-publication.mjs` | **158 contrôles réussis** sur la publication et ses confirmations, dont traitement en cours et réconciliation. |
| Animation — `node tests/browser/hunt-preparation.mjs` | **294 contrôles réussis** à 1280/390 pixels, dont boutons de fermeture désactivés et Échap sans effet pendant l’annulation d’une commande de lots. |
| Animation — `node tests/browser/animation-lots.mjs` | **Parcours complet réussi** : sélection, sauvegarde, commande, annulation, conflit concurrent 409, verrous après paiement/publication, erreurs de lecture et reprise, permissions et mobile. Clics ordinaires, sans forcer les actions masquées. |
| Revue indépendante des diffs | Aucun blocage introduit repéré sur les confirmations, le consentement et les gestionnaires de commandes. Revue en lecture, distincte des tests exécutés. |
| Documentation — `python scripts/check_guidance.py --changed --all-markdown` et `python scripts/sync_documentation.py --check-sources` | **5 guides, 140 liens locaux et 132 sources exportées vérifiés**, aucune erreur ; `git diff --check` réussi dans les trois dépôts modifiés. |

Les commandes Playwright complètes figurent dans le README Pro. Dans PowerShell,
définir `$env:WORKSPACE_CASE='ergonomics'` avant le banc Animation, puis changer
cette valeur pour `shell` et `scroll` et retirer la variable à la fin.

Les anciens tests `business-ux` Pro utilisaient des sélecteurs et des réponses
de facturation dépassés. Ils ont été alignés sur les sources et contrats déjà
présents dans HEAD, sans modifier ces écrans ni retirer leurs assertions métier.
Le banc `animation-lots` a également reçu la réponse synthétique manquante de
`selecteurs/coffrets/synthese`, appelée par un composant inchangé dans HEAD.
Ses assertions métier sont conservées ; les notifications sont fermées avec
leurs boutons explicites avant la reprise de saisie.
La suite unitaire Pro complète a été interrompue, sans résultat global ; aucun script lint ou
typecheck n’y est déclaré. Les captures locales restent dans leurs répertoires
`tmp/`, non versionnés.
Les essais sur appareils physiques, lecteurs d’écran et PWA installées ainsi
que les parcours de paiement réel ne sont pas exécutés. Toutes les combinaisons
de données, de droits et de pages ne sont pas couvertes par ces recettes.

## Impacts

Applications modifiées : **Commerçant et Animation** ; documentation canonique :
**Projet**. Pas de contrat API, règle d’éligibilité, permission, migration,
configuration d’exploitation ou générateur modifié. Le backend reste propriétaire
des transitions et refus : la correction du retrait porte sur l’émission de la
commande par l’interface après consentement, pas sur sa règle métier.

Les états de la roadmap et les conditions de clôture E73 restent inchangés.
Les modifications de scan Pro et de défilement Animation préexistantes sont
conservées. Aucun commit, push ou déploiement ne fait partie de cette demande.
