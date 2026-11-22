# Vérification ciblée des maquettes v2 — experts simulés

18 novembre 2026. **Revue visuelle réelle de six PNG ; réactions des cinq experts simulées.** Aucun test humain, aucune interaction navigateur et aucun contrôle applicatif nouveau. Cette vérification complète les [avis initiaux v1](revue-maquettes-experts.json), qui restent inchangés. Les rendus v1 sont conservés dans [iterations/v1](../visuels/maquettes-apres/iterations/v1).

**Conclusion : les deux défauts visuels importants signalés en v1 sont corrigés dans les rendus examinés. Aucun problème bloquant de représentation restant identifié dans ce périmètre ciblé.** Cette conclusion ne vaut ni validation utilisateur, ni preuve de fonctionnement, ni autorisation de développement.

## Corrections effectivement vues

| Sujet | Preuve v2 examinée | Conclusion visuelle |
| --- | --- | --- |
| C2 — Comparaison mobile | [C2-comparaison-mobile.png](../visuels/maquettes-apres/C2-comparaison-mobile.png) | **CORRIGÉ.** Chaque champ présente successivement Ligne 2 et Ligne 3 ; nom, adresse, SIRET et email sont tous visibles dans le document. La deuxième ligne n’est plus hors du cadre horizontal. La vérification reste humaine. |
| C2 — Aperçu mobile | [C2-apercu-mobile.png](../visuels/maquettes-apres/C2-apercu-mobile.png) | **VU.** Deux blocs distincts portent le numéro de ligne, les données, la proposition et leur case de sélection. Les limites de « zéro conflit » et l’absence de fusion automatique restent explicites. |
| E1 — Confirmation mobile | [E1-confirmation-mobile.png](../visuels/maquettes-apres/E1-confirmation-mobile.png) | **CORRIGÉ.** Case vide, bouton définitif gris et aide « Cochez … pour activer le bouton » sont cohérents. Le retour sans clôturer reste disponible. La capture prouve l’apparence, pas l’exécution de la garde. |
| D1 — Confirmation de demande | [D1-confirme-bureau.png](../visuels/maquettes-apres/D1-confirme-bureau.png) | **CORRIGÉ AU TITRE.** « Demande de diffusion confirmée » correspond désormais à la phrase explicative ; le résultat de distribution reste renvoyé au suivi. |
| A1 — Filtres | [A1-accueil-bureau.png](../visuels/maquettes-apres/A1-accueil-bureau.png) | **CORRIGÉ VISUELLEMENT.** Période du tableau de bord et Statut des animations sont regroupés au-dessus des prochaines actions. Les tâches précèdent les nouvelles ; la création reste visible. |
| E1 — Étape actuelle | [E1-dossiers-mobile.png](../visuels/maquettes-apres/E1-dossiers-mobile.png) | **VU.** Le texte « Étape actuelle » complète le repère vert de Clôturée. Le dossier restant, son responsable fictif et la distinction informé/remis restent lisibles. Terminer est visuellement désactivé. |
| Fidélité des pictogrammes | A1 accueil bureau et D1 confirmé bureau, ci-dessus | **CORRIGÉ DANS CES DEUX RENDUS.** Tableau de bord, animations, modèles, commerces, participants, validations, tirages, lots et autres rubriques ont des pictogrammes distincts. Aucun contrôle exhaustif des autres pages v2 n’est revendiqué. |

## Réserves restantes et contrôles non exécutés

- **D1, cohérence rédactionnelle mineure :** le paragraphe final conserve « Un envoi confirmé ne garantit pas… ». Harmoniser éventuellement avec « Une demande de diffusion confirmée ne garantit ni la distribution ni la lecture… » éviterait de réintroduire le terme plus fort. Le titre corrigé et le renvoi au résultat de distribution lèvent l’ambiguïté principale ; ce détail ne bloque pas la présentation de la maquette.
- **A1, portée fonctionnelle :** le regroupement est vu, mais le comportement des filtres n’a pas été testé. L’implémentation future doit conserver les portées existantes et éviter de masquer implicitement une tâche opérationnelle par un filtre destiné aux indicateurs.
- **C2, longueur mobile :** l’empilement rend toute l’information accessible visuellement mais allonge la page. Sa lecture et le maintien du contexte de sélection devront être éprouvés avec des organisateurs. Aucun gain de vitesse n’est établi.
- **Accessibilité :** la présence d’un texte d’étape et d’un bouton gris n’est pas un audit clavier, contraste ou lecteur d’écran. Aucun téléphone physique ni aide technique n’a été utilisé dans cette revue.
- **Contrats non démontrés :** le brouillon partiel B1, le circuit canonique C1, le moteur de similitude C2, le rétablissement de Communication D1 et les opérations réelles de clôture restent des travaux ou preuves futurs. Les corrections visuelles ne lèvent pas ces dépendances.
- **Périmètre :** six images v2 examinées, pas tous les états de toutes les orientations. Les autres conclusions de v1 ne deviennent pas des vérifications v2 par défaut. Aucun nouvel AVANT B3 n’a été examiné ; sa limite de preuve demeure.

## Retours finaux simulés

| Expert fictif | Retour final simulé après inspection ciblée |
| --- | --- |
| E1 — UX senior | « Les deux corrections importantes rendent le mobile cohérent : comparer signifie voir les deux lignes et une confirmation indisponible paraît maintenant inactive. Les filtres regroupés et les pictogrammes distincts restaurent des repères utiles. Je conserve la réserve sur la longueur des pages et sur le périmètre réel des filtres. » |
| E2 — PM SaaS B2B | « Ces ajustements restent locaux et compatibles avec les orientations adoptées. Ils ne créent ni nouveau mode de création ni automatisation. La présentation est prête pour une décision sur les propositions ; B1 et C1 demandent toujours un cadrage de contrat, et D1 une réparation réellement vérifiée. » |
| E3 — Opérations événementielles | « Les états de clôture et de remise restent distincts ; le dossier non traité empêche visuellement de terminer. La confirmation de lecture est cohérente avec le contrôle inactif. Les responsabilités métier et la recette de clôture réelle restent à vérifier avant tout déploiement. » |
| E4 — Onboarding et accessibilité | « Le texte Étape actuelle et l’aide près de la case réduisent la dépendance à la couleur. Les lignes d’import sont lisibles sans deviner un défilement horizontal. Cela améliore la représentation ; je ne conclurai pas à l’accessibilité sans clavier, lecteur d’écran et téléphone réel. » |
| E5 — Researcher/facilitateur | « Les corrections signalées sont bien visibles dans ces six rendus. Aucune donnée humaine supplémentaire ne permet de chiffrer compréhension, vitesse ou erreurs. Ma réserve sur le circuit C1 demeure ; l’amélioration d’une maquette ne prouve pas l’existence ni l’efficacité du service. » |

## Portée du changement

**Aucun changement substantiel identifié : aucun nouveau vote organisé.** Empilement mobile, style désactivé, libellés cohérents, regroupement de filtres, repère textuel et pictogrammes distincts mettent les maquettes en accord avec les orientations déjà soumises. Aucun statut métier nouveau, aucune fusion automatique, aucun envoi ni clôture automatique n’est proposé par ces ajustements.

La validation finale appartient à l’utilisateur. Les avis simulés et les contrôles de rendu ne constituent pas son accord.
