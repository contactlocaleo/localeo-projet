---
name: localeo-cloturer-epic
description: Clôturer une epic Localeo après vérification de la documentation, de la couverture spécifications/code et des tests exécutés ; actualiser la roadmap, préparer le commit et les actions de configuration pour le déploiement. Utiliser pour une demande de clôture ou de bilan de clôture, pas pour une simple préparation de release.
---

# Clôturer une epic Localeo

Lire le [guide transverse](../../../AGENTS.md), le backlog canonique, sa spécification et son bilan existant, puis les seules instructions applicatives affectées. Le [cycle, section Clôturer](../../../docs/organisation/cycle-epic.md#clôturer) porte les conditions de passage.

## Périmètre et preuves

Retrouver l’identifiant et l’état dans la [roadmap](../../../docs/roadmap/README.md). Examiner branches, HEAD, index, diff et fichiers nouveaux pour distinguer l’epic des travaux étrangers. Conserver les critères et arbitrages acceptés ; une livraison partielle ne termine pas l’ensemble. Une epic déjà terminée se vérifie sans nouveau déplacement ; une évolution ouverte garde ses propres preuves.

Compléter le bilan existant avec le [noyau des preuves](../../../docs/organisation/cycle-epic.md#documenter-les-preuves-et-préparer-la-livraison) et sa [matrice](../../../docs/organisation/cycle-epic.md#matrice-de-traçabilité) : spécification, code réel, consommateurs, résultats et écarts par critère. Corriger les incohérences documentaires établies sans convertir un défaut en cible produit. Pour les documents publiés concernés, vérifier aussi alias d’export, liens réécrits, lecteur, bundle et révision de livraison : une source Git n’est pas une publication ERP.

Renouveler les preuves affectées/manquantes et exécuter les contrôles requis. Depuis Projet, ajouter `python scripts/check_guidance.py --changed --all-markdown` au contrôle des guides pour les Markdown modifiés et les liens entrants après déplacement. Les exports/lecteurs suivent le noyau commun.

## Décider et appliquer

Clôturer seulement si tous les critères sont vérifiés, les contrôles requis réussis et la documentation/les contrats cohérents, sans réserve invalidant l’acceptation. Une recette cible exigée ne se remplace pas par des tests locaux. Une dette prouvée sans impact reste explicite sans blocage artificiel. Si un critère est partiel, non satisfait ou non vérifiable, conserver statut et chemin, documenter les actions nécessaires et poursuivre les travaux indépendants ; ne pas introduire silencieusement un correctif substantiel pour forcer la clôture.

Une demande de clôture autorise ce changement d’état lorsque les conditions sont satisfaites ; un audit seul conserve l’état. Sans confirmation supplémentaire :

1. Dater le bilan et le statut « Terminée » avec versions, preuves, limites et référence de la demande.
2. Déplacer l’unique backlog vers `docs/roadmap/terminees/`, nom et IDs conservés. Vérifier source, destination et absence de collision avant déplacement.
3. Actualiser index d’état, compteurs, `product-roadmap.md`, `suivi-backlog.md`, index des spécifications et liens entrants ; adapter les liens relatifs et préserver les bilans historiques.
4. Vérifier les liens et `git diff --check` des dépôts modifiés avant d’annoncer la clôture.

Des configurations futures restent des prérequis de livraison ; elles ne bloquent la clôture que si ses critères exigent leur recette cible.

## Préparer le commit et la configuration

Préparer par dépôt les fichiers/hunks de l’epic, les contrôles et un message proposé, déplacement et liens compris. Isoler les fichiers mixtes, préserver les travaux étrangers et exclure secrets, sorties privées et bundles. Une clôture bloquée produit un lot de bilan/correctif. La préparation ne modifie pas l’index ni ne crée de commit ; réaliser les opérations déjà explicitement autorisées sans redemander. Ne pas inventer de SHA pour un arbre local.

Compléter le bilan de livraison avec une synthèse dérivée des sources effectives :

| Composant / environnement | Action et ordre | Valeur ou défaut sans secret | Source / contrôle |
| --- | --- | --- | --- |
| Application touchée | Variable, migration, permission, tâche, URL ou révision documentaire | Obligatoire/optionnel ; valeur vérifiée ou à renseigner | Chemin, commande ou recette |

Inclure les impacts réels : noms/emplacements des secrets à provisionner, flags, fournisseurs, jobs, migrations, redémarrages, contrats et bundle documentaire. Si la cible est inconnue, fournir les exigences communes et les valeurs restant à renseigner. Préciser la révision à publier après commit, l’ordre entre dépôts, les contrôles santé/métier et la reprise prouvée. Utiliser la [préparation de livraison](../../../docs/organisation/preparer-livraison.md) si un manifeste est demandé.

Restituer le verdict (clôturée, bloquée avec critères, ou clôturable pour audit seul), dépôts/chemins, preuves exécutées ou réutilisées, lot/message et synthèse de configuration. Distinguer statut produit, commit/push et déploiement effectif ; un lien vers le bilan seul ne remplace pas les actions demandées.
