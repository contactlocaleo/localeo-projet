# ÉTAPE 5 — ARCHIVAGE ET REJOUABILITÉ DU WORKSHOP UX

Tu es chargé de finaliser l'archivage du workshop UX Localeo Live.

## 1. Vérifier le répertoire daté

Identifie le répertoire de l'exécution en cours :

`docs/ux-workshops/YYYY-MM-DD/`

Ne modifie pas les répertoires des autres exécutions.

## 2. Vérifier les prompts

Contrôle la présence de :

- `prompts/00-protocole-global.md`
- `prompts/01-exploration.md`
- `prompts/02-workshop.md`
- `prompts/03-maquettes.md`
- `prompts/04-validation.md`
- `prompts/05-archivage.md`

Chaque fichier doit contenir le texte complet du prompt réellement utilisé.

Si une instruction a été modifiée pendant l'exécution, conserve sa version finale et documente les modifications.

Si un prompt n'est pas disponible, signale-le explicitement. Ne reconstruis pas fictivement une instruction prétendument identique.

Enregistre cette instruction dans `prompts/05-archivage.md`.

## 3. Vérifier les livrables

Contrôle :

- Les observations.
- Les captures réelles.
- Les comptes rendus.
- Les votes.
- Le backlog.
- Les orientations rejetées.
- Les maquettes.
- La galerie comparative.
- Les décisions de validation.
- La roadmap.
- Le plan de tests utilisateurs.

Signale les éléments manquants.

## 4. Finaliser les métadonnées

Complète `README.md` avec :

- Date et heure de l'exécution.
- URL analysée.
- Branche et commit Git.
- Modèles et niveaux de raisonnement utilisés, si connus.
- Version du protocole.
- Statut : terminé, partiel ou interrompu.
- Parcours vérifiés.
- Limitations.
- Nombre d'orientations proposées.
- Nombre d'orientations adoptées.
- Nombre de P0/P1.
- Statut des validations.
- Liens vers les livrables.

## 5. Comparer avec le workshop précédent

Si un workshop antérieur existe, crée :

`synthese/comparaison-precedent.md`

Présente :

- Les problèmes précédemment identifiés et désormais corrigés.
- Les problèmes persistants.
- Les nouvelles difficultés.
- Les changements de priorité.
- Les évolutions des orientations.
- Les évolutions des notes heuristiques.

Ne présente une correction comme effective que si elle a été vérifiée.

## 6. Préparer la relance

Crée :

`prompts/RELANCER-WORKSHOP.md`

Ce fichier doit contenir un prompt autonome permettant de :

1. Identifier le dernier workshop terminé.
2. Créer un nouveau répertoire daté.
3. Reprendre le protocole complet.
4. Réexplorer l'application réelle.
5. Organiser les débats et votes.
6. Générer les nouvelles maquettes.
7. Comparer les résultats.
8. Préserver l'historique.
9. Attendre la validation avant toute implémentation.

Le prompt doit être utilisable dans une nouvelle conversation Codex sans dépendre de l'historique conversationnel.

## 7. Vérification finale

Vérifie que :

- Tous les fichiers sont accessibles.
- Les chemins relatifs sont corrects.
- Les captures sont référencées.
- Les maquettes sont consultables.
- Les prompts sont complets.
- Les résultats précédents sont préservés.
- Aucun code applicatif n'a été modifié.

Si le workshop est incomplet, indique-le sans déclarer artificiellement sa clôture.

## 8. Restitution

Présente :

- Le répertoire archivé.
- Le statut final.
- La liste des livrables.
- Les éventuelles anomalies.
- Le chemin du prompt de relance.

Ne réalise aucune modification applicative.
