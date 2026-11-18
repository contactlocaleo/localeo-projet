# Arbitrages complémentaires — maquettes v2

18 novembre 2026. **Décisions de représentation, pas validation utilisateur ni autorisation de développement.** Périmètre : A1, B1, B2, B3, C1, C2, D1, D2, E1, toutes adoptées à au moins 7/12 et classées P0/P1.

## Corrections après revue v1

| Réserve | Arbitrage v2 | Preuve et limite |
| --- | --- | --- |
| E1 : bouton vert malgré une case vide | Style désactivé gris, consigne explicite, case toujours requise | Le HTML v1 était déjà désactivé ; la correction est visuelle. Interaction locale v2 vérifiée : désactivé → activé après coche → désactivé après décoche. Aucun serveur sollicité. |
| C2 : colonnes de comparaison et sélection invisibles sur mobile | Présentation empilée avec nom de chaque champ et cases visibles | Les deux cases sont dans la largeur 390 px ; le tableau de comparaison ne déborde plus horizontalement. La décision de sélection reste humaine. |
| B1 : enregistrement bas et état de saisie ambigu | Commande avant les champs facultatifs, « Modifications non enregistrées », brouillon non public | Bouton dans le premier viewport de 390 × 844 ; sa confirmation est un état illustré, pas une sauvegarde réelle. |
| A1 : filtres dispersés et portée ambiguë | Filtres regroupés, nommés « Période du tableau de bord » et « Statut des animations » | Le code local conserve la requête dashboard avec ces filtres. Leur interprétation et l’absence de tâches manquées restent à tester ; aucun nouveau moteur d’urgence. |
| D1 : « Envoi confirmé » trop affirmatif | « Demande de diffusion confirmée », distribution et lecture distinctes | Harmonisation du titre et du texte. Aucun résultat d’envoi réel produit. |
| D1 : résultat durablement incertain | Maintenir la tentative et passer au support si la lecture d’état ne conclut pas | Pas de délai inventé, pas de nouvelle tentative d’envoi automatique. |
| C1 : formulaire peu explicite | Nom et adresse marqués obligatoires, précisions facultatives dans la proposition | Champs proposés à confronter au contrat canonique ; responsable et délai toujours inconnus, pas inventés. |
| E1 : étape courante indiquée surtout par couleur | Repère textuel « Étape actuelle » et `aria-current` | Le cycle demeure distinct ; pas de fusion des états. |
| E1 : vocabulaire et transition simulée | « Personnes pouvant gagner » ; confirmation mène à une fin de scénario local | La maquette n’enchaîne plus la confirmation sur un gagnant déjà informé : les dossiers de lots illustrent une étape ultérieure sélectionnable séparément. Aucun tirage implicite. |
| D2 : commande répétée sur l’écran déjà atteint | Repère « Vous êtes dans le suivi opérationnel », accès distinct au bilan | L’incohérence de destination est illustrée sans ajouter un nouveau tableau de bord. |
| Navigation : icônes identiques | Pictogrammes distincts reprenant les fonctions existantes | Logo copié sans modification, couleurs et structure conservées ; aucun nouvel espace de navigation. |

Les trois groupes ont revu les corrections ciblées : [experts](verification-maquettes-v2-experts.md), [métier 1](verification-maquettes-v2-metier-1.md), [métier 2](verification-maquettes-v2-metier-2.md). Les réserves majeures de rendu C2/E1 sont levées pour les images examinées ; les dépendances produit ne le sont pas.

## Conformité au vote initial

| ID | Vote initial | Ce qui est illustré | Limites conservées / nouveau vote |
| --- | ---: | --- | --- |
| A1 | 12/12 | Actions avant nouvelles, information et succès distincts, filtres conservés | Aucun calcul d’urgence nouveau ; pas de personnalisation A2. Aucun changement substantiel. |
| B1 | 12/12 | Saisie, sauvegarde explicite, reprise, échec | Brouillon partiel à spécifier ; aucun accord ni publication implicites. Aucun changement substantiel. |
| B2 | 12/12 | Démarrage, accords, diagnostics, dotation et aperçu provisoire | Pas de délai 5–10 min promis ; activation uniquement si connue ; QR définitif après publication. Aucun changement substantiel. |
| B3 | 12/12 | Seuil compatible, incompatibilité après changement de sélection | Aucun ajustement silencieux d’une règle choisie. Aucun changement substantiel. |
| C1 | 9/12 | Commerce absent, demande individuelle, suivi | Circuit canonique à vérifier ; demande ≠ activation/participation. Aucun changement substantiel. |
| C2 | 9/12 | Colonnes reconnues, doute de similitude, comparaison et confirmation explicite | Pas de fusion/rejet automatiques ; contrôles forts existants à préserver. Aucun changement substantiel. |
| D1 | 12/12 | Lecture en échec, préparation, aperçu, résultat confirmé/refusé/incertain | La panne n’est pas corrigée par ces visuels ; aucun renvoi automatique. Aucun changement substantiel. |
| D2 | 12/12 | Accès au suivi et bilan distinct | Pas de nouveaux indicateurs ou de temps réel supposé. Aucun changement substantiel. |
| E1 | 12/12 | Fin de période, confirmation, dossiers et bilan | Confirmation définitive et responsabilités conservées ; aucune clôture programmée E2. Aucun changement substantiel. |

**Aucun nouveau vote requis ni organisé** : la revue n’a identifié aucune modification substantielle. Les votes initiaux restent ceux de l’étape 2 ; les préférences de revue ne les remplacent pas. Aucun ajout P2/P3, aucun calendrier, aucune relance programmée, aucun tutoriel ou formulaire unique.

## Dépendances et risques encore ouverts

1. **D1 :** diagnostic et rétablissement de Communication, destinataires isolés et recette d’envoi toujours nécessaires. P0 inchangé pour le lancement incluant cette fonction.
2. **B1 :** contrat de brouillon partiel, reprise et traitement d’erreur à spécifier ; le clic local ne prouve aucune persistance.
3. **C1 :** responsable, droits, circuit et conditions du référencement non établis. Le suivi représenté est conceptuel ; aucun délai garanti.
4. **C2 :** faux positifs, qualité des adresses et cohérence des obligations à valider avec le domaine. Une similitude n’est jamais déclarée doublon certain.
5. **B3 :** l’AVANT est partiellement cadré. Le seuil problématique est documenté par AN-05 et les relevés, pas visible sur la capture 18. Aucune reconstitution présentée comme preuve réelle.
6. **Accessibilité et autonomie :** contrôles locaux de largeur, focus et état désactivé réalisés ; téléphone réel, lecteur d’écran et tests avec organisateurs restent nécessaires. Les longs imports doivent être éprouvés avec des personnes peu familières du numérique.
7. **Clôture et navigation :** responsabilités, habilitations et conséquences métier restent décidées par le backend. Les commandes de suspension/annulation déjà présentes dans D2 ne sont pas rendues exécutables dans les maquettes.

## Versions et preuves

- [Galerie finale](../visuels/comparatif-avant-apres.html), neuf comparaisons ; [correspondances des preuves](../visuels/preuves-comparatif.json).
- [Scénarios v2](../visuels/maquettes-apres/scenarios.json), trente états et soixante rendus.
- [Rendus v1](../visuels/maquettes-apres/iterations/v1/manifest-v1.json) et [sources exactes v1 en archive](../visuels/maquettes-apres/iterations/v1-sources.zip).
- [Contrôles d’interactions locaux](controle-interactions-maquettes.json), [mesures des rendus](../visuels/maquettes-apres/mesures-rendus.json).
- [108 réactions initiales et relecture finale](revue-maquettes.md).

**Arrêt après livraison : validation de l’utilisateur attendue. Aucun changement applicatif ni développement exécuté.**
