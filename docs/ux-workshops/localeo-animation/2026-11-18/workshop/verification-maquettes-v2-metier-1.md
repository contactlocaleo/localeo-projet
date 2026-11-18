# Vérification visuelle v2 — Françoise, Michel, Sophie et Julie

18 novembre 2026. **Réactions de profils entièrement SIMULÉES.** La vérification porte sur cinq images de propositions isolées. Les corrections visuelles décrites ci-dessous ont effectivement été examinées ; leur effet sur des organisateurs reste une hypothèse. Aucune interaction navigateur, aucun appel serveur et aucun test avec une personne n’ont été réalisés dans cette revue. Les avis v1 restent conservés dans [revue-maquettes-metier-1.json](revue-maquettes-metier-1.json).

## Corrections observées

| Orientation | Image v2 examinée | Constat visuel | Portée |
| --- | --- | --- | --- |
| B1 | [Saisie mobile](../visuels/maquettes-apres/B1-saisie-mobile.png) | « Modifications non enregistrées » apparaît dans le premier panneau. « Enregistrer le brouillon » est placé avant le nom, la description et les dates. Le texte précise que le brouillon n’est pas public et qu’aucun envoi ni publication n’a lieu. | Les deux réserves visuelles de v1 sur l’état de sauvegarde et la position de la commande sont traitées dans cet état. La sauvegarde effective et la reprise ne sont pas prouvées par l’image. |
| C2 | [Aperçu mobile](../visuels/maquettes-apres/C2-apercu-mobile.png) | Les lignes 2 et 3 sont présentées verticalement avec nom/adresse, proposition, avertissement de similitude et case de sélection propres à chaque ligne. Les deux cases sont visibles, sans partie droite coupée. | La réserve majeure de v1 sur les sélections masquées est levée pour ce rendu. Le contrôle reste humain et le zéro conflit ne devient pas une garantie. |
| E1 | [Confirmation mobile](../visuels/maquettes-apres/E1-confirmation-mobile.png) | Case non cochée et bouton de confirmation grisé sont cohérents visuellement. Une consigne explique qu’il faut cocher pour activer le bouton. « Personnes pouvant gagner » remplace « participants éligibles ». Le retour sans clôture reste visible. | La réserve majeure visuelle et la réserve de vocabulaire sont traitées. Aucun comportement d’activation, de clavier ou de clôture réelle n’est attesté par cette revue d’image. |
| C1 | [Demande mobile](../visuels/maquettes-apres/C1-demande-mobile.png) | Nom commercial et adresse portent « obligatoire » ; Précisions utiles porte « facultatif ». La commune est affichée dans un champ distinct. La demande reste séparée de l’activation, de l’ajout à l’animation et de l’invitation. | L’ambiguïté visuelle des champs est traitée. Ces obligations illustrent une proposition de formulaire, pas un contrat backend déjà confirmé. |
| D2 | [Suivi bureau](../visuels/maquettes-apres/D2-suivi-bureau.png) | Le bouton redondant « Consulter le suivi opérationnel » n’est plus affiché dans l’en-tête de l’écran cible. « Vous êtes dans le suivi opérationnel » identifie la position. « Ouvrir le bilan » reste distinct. | La réserve de repérage et de répétition du bouton est traitée. La destination de la vraie route applicative n’a pas été modifiée ni testée ici. |

## Réserves conservées

- **C1 — dépendance :** le service responsable, les droits, le contrat de demande et son traitement restent à confirmer. L’image ne dit pas à qui la demande est transmise. Ne pas inventer de destinataire ou de délai pour combler cette dépendance ; la documenter avant une éventuelle implémentation.
- **C2 — usage :** les fiches rendent les cases visibles mais allongent l’écran. La comparaison de nombreux commerces et l’accès clavier/tactile restent à tester. La revue v2 ne change pas les abstentions initiales de Françoise et Michel ni leurs difficultés avec l’import.
- **E1 — comportement :** le bouton grisé répond à la réserve visuelle. Vérifier séparément que le prototype local respecte la case puis, lors d’un éventuel développement autorisé, que les contrôles métier restent effectifs côté serveur.
- **D2 — actions sensibles :** suspendre, préparer la clôture et annuler restent voisins. La réserve de prudence sur leur distinction demeure ; aucune suppression de confirmation n’est demandée.
- **B1 — saisie :** la position haute rend la sauvegarde trouvable. Vérifier ensuite que l’état se met à jour après chaque modification et ne déclare enregistré qu’après une réponse effective, sans publication ou invitation implicite.
- **Hors périmètre de ce contrôle :** la portée des filtres A1, les autres états B1/C1/C2/D1/E1 et les autres rendus n’ont pas été réexaminés en v2 par ce sous-groupe. Leur validation visuelle ne peut pas être déduite de ces cinq images.

## Réactions finales simulées

| Profil fictif | Réaction simulée après correction |
| --- | --- |
| Françoise | « Je vois maintenant tout de suite que mon travail n’est pas enregistré et où l’enregistrer. Le bouton de clôture grisé m’explique qu’il reste une vérification. L’import reste quelque chose pour lequel je demanderais de l’aide, même si je vois enfin les cases. » |
| Michel | « Les mots de la clôture sont plus compréhensibles et je peux revenir sans fermer. Pour le commerce absent, je sais quoi remplir, mais je voudrais encore savoir qui prendra ma demande en charge. La séparation entre cadeau remis et animation clôturée doit rester. » |
| Sophie | « La sélection des lignes est maintenant lisible sur téléphone et le repère du suivi évite un clic redondant. Cela corrige les problèmes de présentation que j’avais signalés ; il reste à établir le circuit canonique des demandes et à tester les vraies réponses de sauvegarde et de clôture. » |
| Julie | « La sauvegarde haute et les cases visibles corrigent deux obstacles concrets des rendus. La clôture semble maintenant correctement conditionnée visuellement. Je garde ma réserve sur le circuit de référencement et sur la proximité des commandes sensibles ; ces images ne démontrent pas encore un gain de temps sur le terrain. » |

## Périmètre et décision

Aucun changement substantiel de l’orientation adoptée n’est constaté dans ces cinq corrections : position et état de sauvegarde, adaptation des lignes d’import, restitution de la confirmation, libellés de champs et repère de navigation restent dans B1, C2, E1, C1 et D2. **Aucun vote supplémentaire organisé par ce sous-groupe.**

Les préférences fictives et les corrections visuelles ne constituent ni validation de l’utilisateur, ni autorisation de développement, ni preuve d’efficacité auprès d’organisateurs réels. Cette revue a écrit uniquement le présent fichier.
