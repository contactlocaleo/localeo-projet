# Incident de périmètre de lecture — persistance/SQL

Date : 19 novembre 2026.

## Mission et restriction

La mission transmise était le brief archivé `prompts/brief-persistance.md` : audit indépendant sur le code courant, sans lecture d'anciens audits ni de rapports d'autres agents avant finalisation.

## Commande en cause

Une commande PowerShell regroupait une recherche frontend et des lectures source backend :

```text
rg -n 'mode_lecture.*borne|live/evenements|/live[`"\\x27]|dashboard-performance' ../localeo-animation/src ../localeo-marketplace/src
```

La commande était suivie, dans la même invocation `exec_command`, de lectures ciblées de `app/api/limitation_lectures_live.py`, d'un extrait de `animation_locale_repositories.py` et d'un extrait de `productivite_animation.py`.

L'expression contenant une apostrophe et un accent grave a été mal échappée à travers les couches JavaScript/PowerShell. Le résultat observé de `rg` a parcouru le dépôt documentaire courant au lieu de rester limité aux deux dossiers `src` voisins.

## Portée observée

La sortie a affiché des lignes provenant de l'inventaire de l'audit courant `2026-11-19-02` et des extraits de rapports de l'audit `2026-11-19` : inventaire, agents, contradiction, synthèse et recommandations. Aucun fichier d'archive n'a été ouvert volontairement après cette sortie. Des recherches de code supplémentaires ont eu lieu avant réception de l'instruction d'arrêt ; elles étaient explicitement limitées aux fichiers source backend et frontend.

L'incident a été signalé immédiatement à l'agent principal par message. L'indépendance de cette première analyse ne peut plus être garantie après exposition à ces extraits.

## Arrêt

Sur instruction de l'agent principal, cette analyse est arrêtée. Aucun rapport principal `04-persistance.md` ni annexe `04-persistance-annexe.md` n'a été produit par cet agent. Cette note ne contient aucune conclusion technique. Aucun code applicatif n'a été modifié ; aucun import applicatif, accès réseau/base, serveur, test ou benchmark n'a été exécuté.

Modèle exact : INCONNU. Effort de raisonnement : INCONNU.
