# ÉTAPE 3 — MAQUETTES UX AVANT/APRÈS LOCALEO PRO

Tu es chargé de produire les propositions visuelles des améliorations UX retenues lors du workshop Localeo Pro.

## 1. Charger les résultats

Identifie le répertoire daté de l'exécution en cours.

Lis :

- Le rapport exécutif.
- Le backlog.
- Les votes.
- Les observations factuelles.
- Les captures réelles.

Enregistre cette instruction complète dans `prompts/03-maquettes.md`.

## 2. Périmètre

Travaille uniquement sur les orientations :

- Adoptées avec au moins 7 voix sur 12.
- Classées P0 ou P1.

Les améliorations doivent concerner les parcours prioritaires :

- Première prise en main.
- Validation des participations.
- Notifications.
- Préparation des animations.
- Kit et logistique.

## 3. Captures AVANT

Pour chaque orientation :

- Utilise une capture réelle de Localeo Pro.
- Identifie l'écran et le problème.
- Annote les zones concernées si nécessaire.
- Référence le constat et le vote.

Si la capture manque, tente de la produire dans l'environnement de test autorisé.

Ne présente jamais une maquette ou une reconstruction comme une capture réelle.

## 4. Maquettes APRÈS

Produis une proposition visuelle fidèle à l'identité graphique actuelle de Localeo Pro.

Respecte :

- Les composants existants.
- La cohérence visuelle.
- Les contraintes mobiles.
- La lisibilité.
- La rapidité d'utilisation.
- Les besoins des commerçants peu familiers du numérique.

Privilégie les optimisations simples.

Ne propose pas de refonte globale sans justification.

Les prototypes doivent être isolés du code applicatif.

## 5. Scénarios à illustrer

Lorsque des orientations P0/P1 concernent ces sujets, illustre notamment :

- L'accueil commerçant.
- L'accès à la validation.
- Le scan et sa confirmation.
- Les erreurs et doublons.
- Les notifications.
- La préparation d'une animation.
- Le kit d'animation.
- Les consignes logistiques.

Ne crée pas artificiellement des maquettes pour des sujets sans orientation adoptée.

## 6. Comparatif HTML interactif

Crée :

`visuels/comparatif-avant-apres.html`

La galerie doit être consultable sur mobile et ordinateur.

Pour chaque orientation, présente :

- ID.
- Priorité.
- Problème.
- Capture AVANT.
- Proposition APRÈS.
- Bénéfice.
- Effort estimé.
- Résultat du vote.

Prévois un affichage côte à côte sur ordinateur et une bascule avant/après sur mobile.

## 7. Revue contradictoire

Soumets les maquettes aux cinq experts et sept commerçants simulés.

Demande notamment :

- Comprenez-vous mieux cet écran ?
- Savez-vous immédiatement quoi faire ?
- Cette version vous ferait-elle gagner du temps ?
- Le risque d'erreur est-il réduit ?
- Préférez-vous l'ancienne ou la nouvelle version ?
- Qu'est-ce qui reste difficile ?

Les réactions doivent rester identifiées comme simulées.

Si une maquette change substantiellement l'orientation adoptée, organise un nouveau vote à la majorité de sept voix.

## 8. Livrables

Enregistre :

- Les captures réelles dans `visuels/captures-avant/`.
- Les maquettes dans `visuels/maquettes-apres/`.
- La galerie HTML.
- Les arbitrages complémentaires.

Mets à jour le backlog avec les références aux maquettes.

## 9. Contraintes et arrêt

Ne modifie aucun code applicatif.

Ne réalise aucune implémentation.

Ne considère pas les votes simulés comme une autorisation de développement.

Mets à jour le README.

Arrête-toi et attends ma validation.
