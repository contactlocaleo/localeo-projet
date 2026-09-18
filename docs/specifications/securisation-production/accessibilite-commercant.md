# F12 — Mesure d'accessibilité du build

Le contrôle Axe de la liste Animation attend la réponse synthétique de liste et la fin des animations d'entrée finies avant de mesurer les contrastes. L'opacité transitoire d'un élément en apparition ne doit pas produire un résultat aléatoire selon la vitesse du navigateur. Les animations restent actives pendant le parcours ; le test ne modifie ni les couleurs, ni les seuils, ni les règles Axe.

Validation : suite navigateur avec le build optimisé et la CSP Render, plus répétition du scénario d'accessibilité pour vérifier sa stabilité.
