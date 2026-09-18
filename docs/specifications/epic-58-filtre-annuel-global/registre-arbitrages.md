# Registre des arbitrages - Epic 58 Filtre annuel global

| ID | Sujet | Proposition | État |
| --- | --- | --- | --- |
| ANN-ARB-01 | Année d'appartenance | Utiliser le chevauchement de la période de l'animation avec l'année civile. | À valider |
| ANN-ARB-02 | Valeur par défaut | Sélectionner l'année civile courante. | À valider |
| ANN-ARB-03 | Années proposées | Année courante toujours visible ; années historiques uniquement avec animation. | À valider |
| ANN-ARB-04 | Source des années | Ajouter `/animations/annees` ou une facette backend équivalente. | À valider |
| ANN-ARB-05 | Persistance | Porter `annee` dans l'URL et utiliser `localStorage` en fallback. | À valider |
| ANN-ARB-06 | Détail animation | Ne jamais bloquer une ressource explicitement ouverte parce qu'elle est hors année. | À valider |
| ANN-ARB-07 | Notifications | Ne pas filtrer les notifications opérationnelles par année. | À valider |
| ANN-ARB-08 | Changement de commune | Conserver l'année si disponible, sinon revenir à l'année courante. | À valider |
| ANN-ARB-09 | Fuseau | Calculer les bornes selon le fuseau canonique de la commune/API. | À préciser |
| ANN-ARB-10 | Tableau de bord | Année passée = année entière par défaut ; année courante = période courte autorisée. | À valider |

## Questions ouvertes

1. Le fuseau de référence est-il celui de la commune, `Europe/Paris` pour le
   périmètre actuel, ou UTC pour toutes les bornes de recherche ?
2. L'endpoint des années doit-il inclure les animations annulées et archivées
   dans `nombre_animations` ?
3. Le sélecteur doit-il proposer une valeur `Toutes les années` ? La proposition
   MVP est de ne pas l'ajouter afin de conserver un contexte borné par défaut.
