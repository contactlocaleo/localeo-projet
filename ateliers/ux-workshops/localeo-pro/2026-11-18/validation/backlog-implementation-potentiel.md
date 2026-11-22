# Backlog d’implémentation potentiel — état préparatoire archivé

**Suite du 18 novembre 2026 :** les cinq orientations ont été validées et la réalisation demandée dans [E80](../../../../../docs/roadmap/en-cours/epic-80-fiabilite-parcours-localeo-pro-backlog.md). Le tableau ci-dessous conserve le cadrage préparatoire de l'étape 4 ; le [bilan E80](../../../../../docs/specifications/epic-80-fiabilite-parcours-localeo-pro/verification-livraison.md) porte l'état actuel.

18 novembre 2026. **Préparation documentaire uniquement : aucun développement autorisé ou commencé.** Les cinq orientations sont [en attente de décision utilisateur](decisions.md). Ce tableau décline le backlog UX existant ; il ne crée ni epic, ni ticket, ni roadmap concurrente.

## Règles d’utilisation après décision

- VALIDÉE : conserver l’orientation et ses conditions comme candidate à un futur travail explicitement demandé ; ne pas démarrer automatiquement.
- À RÉVISER : produire d’abord la révision demandée et la soumettre à nouveau ; pas d’implémentation de la version actuelle.
- REPORTÉE : ne pas planifier de réalisation ; conserver la raison et le déclencheur éventuel exprimés par l’utilisateur, sans inventer de date.
- REFUSÉE : retirer la solution des candidats à réaliser ; garder la décision et les risques associés, sans réintroduire la proposition sous un autre identifiant.
- EN ATTENTE : aucune décision acquise ; les lots restent conditionnels.

## Lots candidats

Les efforts M/L sont ceux du workshop, relatifs et sans calendrier ; les sous-tâches ne s’additionnent pas à une estimation de charge. Chaque lot commence par vérifier ce qui existe déjà et ne modifie que les écarts établis. Les critères détaillés restent ceux du [backlog UX](../workshop/backlog-ux.md).

| Lot candidat | Orientation / effort | Travail potentiel | Dépendances et périmètre envisagé | Preuves attendues avant de considérer le lot terminé |
| --- | --- | --- | --- | --- |
| I-B1 | B1 · M | Recetter les états existants ; corriger l’erreur « pack » dans le contexte Animation ; préciser reconnaissance, confirmation, résultat et prochain geste. | Pro validation ; domaine backend propriétaire de l’effet, du doublon et du reçu. Contrat à vérifier, changement non présumé. Maquettes B1. | QR autorisés, succès/refus/doublon/double clic, caméra autorisée/refusée, perte de réponse et vérification sans renvoi ; messages annoncés et focus utile ; mesure en caisse. |
| I-C1 | C1 · M | Vérifier les données de tâche ; prioriser Animation, replier PIN vide, distinguer information et action, conserver les fonctions existantes. | Pro notifications ; producteur des données uniquement si manque démontré ; session/liens partagés avec F1. | Lire ne termine pas une tâche ; tâche actuelle retrouvable après lecture ; aucune action inventée ; bon lien autorisé ; états lisibles sans couleur seule. |
| I-D1 | D1 · L | Diagnostiquer l’écart des compteurs et dates ; expliciter périmètre, prochain geste, responsable et échéance connue. | Pro accueil/animations/préparation ; backend si projection ou règle concernée. Aucun calcul métier concurrent dans l’UI. | Même compte/périmètre/instant cohérents ; transitions Paris ; cas incomplet, attente, prêt et suivi arrêté ; distinctions métier conservées, compréhension vérifiée. |
| I-E1 | E1 · M | Ouvrir le kit autorisé, inventorier les supports réels ; présenter usage et consignes ; dates locales et rôle des QR ; état prêt séparé. | Pro kit ; producteur documentaire/backend selon diagnostic ; examiner la commande kit/preparer avant recette. | Fichier conforme à l’annonce, impression lisible, QR corrects, bornes exactes, téléchargement sans déclaration prêt automatique. |
| I-F1 | F1 · L | Recetter les reprises existantes ; restituer contexte autorisé et tâche encore valable après interruption/reconnexion/absence. | Pro session/navigation/actualisation ; reçu de B1 ; données de tâche C1 et préparation D1. | Avant envoi : pas d’effet ; réponse perdue : reçu relu ; expiration : droits actuels ; aucun rejeu ni succès local ; pas de QR/jeton dans URL ; retour différé observé. |

## Enchaînement possible, non décidé

1. Obtenir les décisions et conditions explicites, puis une demande de travail ultérieure.
2. Rapprocher les orientations retenues des epics/spécifications canoniques et vérifier les capacités existantes. Préparer le jeu de recette autorisé, sans toucher à des participations réelles.
3. Instruire ensemble B1/F1 pour le résultat et la reprise ; D1 avant de propager une nouvelle présentation d’état vers C1/F1 ; vérifier le contenu réel avant de figer E1.
4. Réaliser uniquement les changements explicitement demandés, puis les preuves propres au lot et une observation avec des commerçants. Une validation documentaire ne remplace pas la recette du produit.

Cet ordre exprime des dépendances possibles. Il ne fixe ni priorité différente des P1, ni sprint, ni responsable assigné, ni date.

## Impacts à instruire lors d’une future spécification

| Domaine | Situation à l’étape 4 |
| --- | --- |
| Applications | Pro est le consommateur ciblé. Backend/producteur documentaire potentiellement concernés selon les diagnostics. Aucun travail décidé pour Marketplace ou Animation ; vérifier les contrats partagés si une évolution est ensuite proposée. |
| Invariants | Règles métier, droits et effets restent dans le domaine backend ; Pro présente les états autorisés. Pas de règle de période décidée par la maquette. |
| Contrats | Aucun changement acté. Vérifier reçu, tâche et kit avant de conclure à un besoin d’extension ; tests des consommateurs seulement si leur contrat évolue. |
| Documentation fonctionnelle / exploitation | Adapter ultérieurement guides et supports aux libellés retenus et comportements effectivement livrés ; aucun guide produit changé ici. |
| Migrations | Aucune migration identifiée ou requise pour cette préparation documentaire ; à réévaluer si un futur diagnostic implique un changement de modèle. |
| Générateur de démonstration | Aucun changement ni génération. Prévoir des cas dédiés uniquement si la future recette en a besoin et avec autorisation adaptée. |
| Déploiement | Hors périmètre. Aucune validation UX ne constitue une autorisation de livraison. |

Les [risques ouverts](risques-ouverts.md) continuent d’exister pour les besoins essentiels, y compris si une solution est refusée. Les alternatives B2/F2/D2/E2/A2/C2/G2 rejetées par la simulation ne sont pas réintroduites dans les lots candidats.
