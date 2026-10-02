---
name: localeo-cloturer-epic
description: Clôturer une epic Localeo après vérification de la documentation, de la couverture spécifications/code et des tests exécutés ; actualiser la roadmap, préparer le commit et les actions de configuration pour le déploiement. Utiliser pour une demande de clôture ou de bilan de clôture, pas pour une simple préparation de release.
---

# Clôturer une epic Localeo

Lire le [guide transverse](../../../AGENTS.md), le [cycle d'epic](../../../docs/organisation/cycle-epic.md), puis le backlog canonique, sa spécification et son bilan de vérification existant. Charger les instructions locales des seuls dépôts affectés.

## 1. Fixer le périmètre à clôturer

Retrouver l'identifiant et l'état dans la [roadmap](../../../docs/roadmap/README.md), même si l'IDE indique un ancien chemin. Examiner branches, HEAD, différences indexées et non indexées, fichiers nouveaux et modifications déjà présentes dans chaque dépôt concerné. Distinguer les travaux de l'epic des autres changements.

Une demande de clôture autorise la mise à jour du statut et le déplacement si les contrôles réussissent, sans nouvelle confirmation. Une demande limitée à un audit ou à un bilan n'autorise pas ce changement d'état. Créer ce skill ne clôture aucune epic. Pour une epic déjà terminée, vérifier son bilan sans la déplacer de nouveau ; une évolution ouverte conserve ses propres critères et preuves.

Conserver les identifiants, arbitrages et critères acceptés. Ne pas réduire le périmètre, supprimer un critère ou réécrire une exigence pour obtenir une clôture. Une livraison partielle ne termine pas l'epic complète.

## 2. Rapprocher exigences, code et documentation

Compléter la matrice du bilan existant, sans créer un registre concurrent :

| Critère | Spécification et code effectif | Preuve exécutée et contexte | Documentation et exploitation | Verdict / écart |
| --- | --- | --- | --- | --- |
| ID stable | Règle, propriétaire, entrées et consommateurs | Chemin, commande ou rapport, version, résultat | Guides, contrats, migration/configuration ou sans objet justifié | Vérifié, partiel, non satisfait ou non vérifiable |

Suivre chaque comportement jusqu'à son résultat observable : domaine, orchestration, API/ERP/batch et interfaces concernés. Examiner succès, refus, permissions, répétition et concurrence selon les risques. Un fichier existant, un pourcentage de couverture ou un build réussi ne prouve pas à lui seul un critère.

Vérifier les documents utilisateur/backoffice, ops, spécifications et contrats contre l'implémentation réelle : parcours, libellés, limites, diagnostic et reprise. Corriger les incohérences documentaires établies ; rendre les écarts fonctionnels visibles sans transformer la cible en description d'un défaut. Une nouvelle décision produit reste un arbitrage, pas une correction rédactionnelle.

Contrôler les producteurs et consommateurs des contrats, les migrations, les fixtures et le générateur/restaurateur lorsqu'ils sont affectés. Pour les documents publiés, vérifier alias d'export, liens réécrits, lecteur, bundle et révision documentaire utilisée par la livraison. Une source présente dans Git n'est pas une publication ERP. Justifier les impacts sans objet.

## 3. Vérifier les tests réellement exécutés

Appliquer la [matrice de contrôles](../../../docs/architecture/transverse/controle-architecture.md) et les exigences locales. Examiner les rapports disponibles : date, commande, dépôt, environnement, SHA testé ou SHA de base et différences locales, résultats et skips. Relier les preuves réutilisées au contenu actuel ; ne pas annoncer les avoir réexécutées.

Exécuter les tests comportementaux manquants, périmés ou affectés et les contrôles obligatoires. Respecter les outils isolés des applications ; aucun envoi réel ou test sur une base d'exploitation n'est implicite. Un `plan` de tests n'est pas leur exécution. Ne pas affaiblir une assertion ni ignorer un échec pour obtenir du vert.

Distinguer réussite, échec et non-exécution. Étayer une dette préexistante par une comparaison ou une référence vérifiable ; sa présence ne dispense pas d'un critère qu'elle empêche de vérifier. Une dette prouvée sans impact sur l'epic reste visible sans devenir un blocage artificiel. Après un correctif, renouveler les preuves affectées ; ne pas relancer les mêmes suites sans changement ou incertitude nouvelle.

Exécuter depuis `localeo-projet` :

- `python scripts/check_guidance.py` et le contrôle des Markdown modifiés avec `python scripts/check_guidance.py --changed --all-markdown` ; après déplacement, inclure les liens entrants concernés.
- `python scripts/sync_documentation.py --check-sources` si des sources exportées changent ; vérifier également les lecteurs/bundles si leurs chemins ou contrats changent.

## 4. Décider et appliquer la clôture

**Clôturer seulement si** tous les critères du périmètre sont vérifiés, les contrôles requis ont réussi, la documentation et les contrats sont cohérents et aucune réserve ne remet en cause cette acceptation. Une recette en environnement déployé est requise lorsqu'elle fait partie des critères ; une preuve locale ne la remplace pas. Une confirmation utilisateur vaut pour le scénario effectivement confirmé, sans inventer environnement, appareil ou résultat supplémentaire.

Si un critère reste partiel, non satisfait ou non vérifiable, conserver le statut et le chemin, documenter les écarts et les actions nécessaires dans le bilan, puis terminer les travaux indépendants possibles. Un correctif métier substantiel ou une décision nouvelle ne doit pas être introduit silencieusement pour forcer la clôture.

Si la clôture est autorisée et les conditions satisfaites :

1. Dater le bilan et le statut « Terminée », avec versions vérifiées, preuves, limites de livraison et référence de la décision de clôture.
2. Déplacer l'unique backlog vers `docs/roadmap/terminees/`, en conservant son nom et ses IDs. Vérifier le chemin source exact, l'absence de collision et la destination dans le dépôt avant le déplacement ; ne pas écraser un autre fichier.
3. Mettre à jour les index des dossiers d'état, les compteurs de roadmap, `product-roadmap.md`, `suivi-backlog.md`, l'index des spécifications et les autres liens entrants trouvés par recherche. Adapter les liens relatifs du fichier déplacé. Préserver les bilans historiques.
4. Relancer les contrôles documentaires et `git diff --check` dans les dépôts modifiés. Si le déplacement crée une incohérence, la résoudre avant d'annoncer la clôture réussie.

La clôture produit n'atteste pas un déploiement. Des actions de configuration futures ne bloquent pas à elles seules la clôture si les critères n'exigent pas une recette cible ; elles restent des prérequis explicites de livraison.

## 5. Préparer le commit et la configuration de déploiement

Préparer un lot par dépôt Git indépendant : fichiers/hunks de l'epic, différences relues, contrôles associés et message de commit proposé. Inclure le déplacement et ses liens. Signaler les fichiers mixtes à isoler ; ne pas embarquer les changements étrangers, secrets, artefacts privés ou bundles générés. En cas de clôture bloquée, présenter le lot comme un bilan/correctif, jamais comme une clôture.

« Préparer le commit » signifie rendre ce lot examinable ; ne pas modifier l'index, créer un commit, pousser, fusionner ou déployer sans demande correspondante. Si ces opérations sont déjà explicitement autorisées dans la tâche en cours, les réaliser dans ce périmètre sans redemander. Ne pas inventer un SHA pour des modifications non committées.

Compléter le bilan de livraison existant avec une synthèse opératoire dérivée des sources effectives :

| Composant / environnement | Action avant ou après déploiement | Valeur attendue ou défaut sans secret | Source / contrôle de réussite |
| --- | --- | --- | --- |
| Application concernée | Variable, migration, permission, tâche, URL, révision documentaire… | Obligatoire ou optionnel ; valeur non sensible vérifiée, sinon à renseigner | Fichier de référence, commande ou recette |

Inclure seulement les impacts réels : variables nouvelles/modifiées et valeurs par défaut, secrets à provisionner (noms et emplacement, jamais leurs valeurs), migrations et ordre, configuration fournisseur, flags, jobs, permissions, redémarrages, contrats et bundle documentaire. Préciser la révision à publier/sélectionner si elle dépend du commit à venir, sans qualifier de livré un arbre local. Si l'environnement est inconnu, fournir les exigences communes et marquer ce qui reste à renseigner, sans inventer de valeur cible.

Indiquer l'ordre de livraison entre dépôts, les contrôles santé/métier et la reprise applicable ; ne pas promettre un rollback de données non prouvé. Utiliser la [préparation de livraison](../../../docs/organisation/preparer-livraison.md) pour un manifeste de release demandé, sans lancer un déploiement implicite.

## Restitution

Donner le verdict (clôturée, clôture bloquée avec les critères concernés, ou clôturable mais non clôturée pour un audit seul), les chemins utiles et dépôts modifiés, les tests exécutés et preuves réutilisées, le lot/message de commit préparé, puis les actions de configuration à faire. Séparer explicitement statut produit, commit/push et déploiement effectif. Ne pas remplacer la synthèse opératoire demandée par un simple lien vers le bilan.
