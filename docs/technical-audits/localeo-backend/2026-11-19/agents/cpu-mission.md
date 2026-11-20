# Mission — CPU et algorithmes

Statut : préparée, non lancée ; autorisation utilisateur requise pour l’étape spécialisée.

Lire les instructions backend puis inspecter soi-même les sources au SHA inventorié, en vérifiant l’état du checkout. Citer les fichiers/fonctions/lignes réellement lus ; ne pas reprendre une conclusion de l’inventaire sans vérifier son chemin d’appel.

Périmètre : Complexité selon population, tris, sérialisation, hashing, QR/PDF/images, règles du moteur et tirages. Distinguer coût Python, SQL et réseau.
Points d’entrée : jeu_animation.py, tirages_animation.py, rendu QR/PDF/images, parseur imports.
Couverture : sélectionner F01–F12 et expliciter les flux/variantes non examinés.

Propriété d’écriture exclusive après lancement : `agents/cpu-rapport.md` et `agents/cpu-annexe.md`. Tu n’es pas seul dans le workspace : préserver les modifications des autres. Aucun code applicatif modifié, aucune commande sur base ou fournisseur, aucun serveur ni profiler lancé. Ne pas importer app.main ni lire les dotenv privés. Les ressources exécutables ne sont pas allouées.

Appliquer le [format commun](../inventaire/plan-orchestration-agents.md) : **cinq constats majeurs maximum dans le rapport principal**, classés par impact probable ; toutes les autres observations en annexe. Distinguer fait/hypothèse/mesure et proposer un moyen de réfutation. Relier chaque constat — une cause candidate et aux endpoints ; respecter domaine, atomicité, droits, idempotence et contrats. Proposer seulement des optimisations ciblées compatibles.

Premier contrôle : lire un fichier source et en citer une fonction avec ligne. Si les outils de lecture ne sont pas accessibles, signaler cette limite et ne produire aucun diagnostic supposé.
