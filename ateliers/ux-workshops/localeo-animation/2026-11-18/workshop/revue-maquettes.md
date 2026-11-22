# Revue contradictoire des maquettes — Localeo Animation

**Réactions entièrement simulées.** Cinq experts et sept personnages métier examinent les propositions ; aucun entretien, test utilisateur ou vote humain n’a eu lieu. Une préférence exprimée ici ne vaut pas validation de l’utilisateur.

## Méthode et versions

La revue v1 porte sur neuf orientations, avec une réponse distincte à chacune des six questions pour chaque rôle : **108 fiches et 648 réponses simulées**. Les images effectivement ouvertes par les relecteurs sont listées dans leurs fichiers sources. Les conséquences évoquées restent des hypothèses.

Les défauts visuels de la maquette ont été constatés sur des images réellement rendues : il faut distinguer ces constats de rendu des réactions fictives des personnages. Les sources et les 60 rendus v1 sont préservés dans [les archives de première itération](../visuels/maquettes-apres/iterations/v1/manifest-v1.json). Les chemins de captures des fiches ont été redirigés vers ces copies ; le contenu des avis n’a pas été réécrit.

La v2 corrige notamment la confirmation visuellement active, le tableau mobile masqué, la sauvegarde trop basse et les libellés de résultat. Elle a fait l’objet d’une vérification ciblée par les trois groupes, avec une réaction finale par rôle. Aucun changement substantiel de l’orientation n’a été identifié ; aucun nouveau vote n’a été organisé.

## Résultat de la contradiction

- E1/E4 et plusieurs profils métier signalent des commandes masquées ou ambiguës : C2 et E1 sont corrigées visuellement, puis contrôlées dans le navigateur local.
- Françoise et Michel restent réservés sur l’import ; sa longueur et la compréhension des rapprochements doivent être testées en situation réelle.
- E2/E5 et Julie ne prennent pas une demande de référencement fictive pour un circuit disponible : la dépendance C1 reste ouverte.
- D1 est préférable comme présentation des erreurs et résultats, mais aucun avis ne démontre que le serveur fonctionne.
- La distinction brouillon/publication, accord/activation et information/remise est conservée. Les gains de temps ne sont pas chiffrés.

## Vérifications finales v2

- [Cinq experts : six rendus revus](verification-maquettes-v2-experts.md)
- [Françoise, Michel, Sophie, Julie : cinq rendus revus](verification-maquettes-v2-metier-1.md)
- [Karim, Élodie, Bernard : cinq rendus revus](verification-maquettes-v2-metier-2.md)
- [Arbitrages et réserves restantes](arbitrages-maquettes.md)

Ces vérifications ne constituent ni une conformité d’accessibilité complète ni une recette métier. Les interactions contrôlées dans le navigateur concernent seulement les maquettes locales.

## Les six questions posées

1. La nouvelle version est-elle plus claire ?
2. Le parcours est-il plus simple ?
3. Les actions sont-elles plus visibles ?
4. Les risques d’erreur sont-ils réduits ?
5. L’ancienne ou la nouvelle version est-elle préférable ?
6. Quelles difficultés restent présentes ?

## Réponses individuelles v1 conservées

Les fiches ci-dessous décrivent v1 avant corrections. Leur lecture doit être complétée par les vérifications v2 et les arbitrages, sans attribuer rétroactivement aux personnages une validation finale.

### A1 — Donner la priorité aux actions attendues

[Maquette finale](../visuels/maquettes-apres/A1.html) · vote initial simulé : 12/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : tâches et nouvelles sont séparées.
- **Simplicité :** Oui, la création et les tâches précèdent les nouvelles.
- **Actions visibles :** Oui, boutons placés près de chaque tâche.
- **Risque d’erreur :** Amélioration plausible de la hiérarchie, non mesurée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Les filtres Période et Statut sont dispersés ; leur portée sur les tâches ou les indicateurs reste ambiguë.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, l'accueil explique sa valeur opérationnelle.
- **Simplicité :** Oui, sans ajouter de moteur ni de personnalisation.
- **Actions visibles :** Oui, démarrer et reprendre sont prioritaires.
- **Risque d’erreur :** Le risque d'ignorer une action pourrait diminuer ; aucun taux mesuré.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Clarifier le périmètre des filtres ; garder le chantier limité à la hiérarchie.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui : une action urgente n'a plus la même présentation qu'une nouvelle.
- **Simplicité :** Oui, les échéances à traiter sont en premier.
- **Actions visibles :** Oui, préparation de clôture et invitations sont nommées.
- **Risque d’erreur :** Le texte distingue période atteinte et action réelle de clôture.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Éviter que des filtres d'indicateurs masquent silencieusement une action opérationnelle.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, succès et action attendue portent des mots différents.
- **Simplicité :** Oui, la création est visible même sur mobile.
- **Actions visibles :** Oui, les libellés annoncent la tâche.
- **Risque d’erreur :** Moins de dépendance à la seule couleur.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Les filtres éloignés doivent être regroupés ou leur portée explicitée ; remplacer les calendriers répétés par les pictogrammes existants.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Amélioration heuristique plausible de la hiérarchie.
- **Simplicité :** Simplicité supposée, pas de test humain.
- **Actions visibles :** Les actions sont visuellement plus hautes.
- **Risque d’erreur :** Réduction du risque d'oubli non démontrée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Comparer à tâches et données équivalentes ; les deux exemples ne prouvent pas le comportement avec un grand volume.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Je distingue mieux ce que je dois faire des nouvelles qui m'informent.
- **Simplicité :** Je peux commencer par une action, sans lire tous les cadres jaunes.
- **Actions visibles :** Préparer la clôture et Voir les invitations me donnent deux gestes précis.
- **Risque d’erreur :** Les mentions Action attendue, Succès et Information évitent de me fier seulement aux couleurs.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le filtre Période placé près des actions me fait encore hésiter : peut-il cacher une action qui m'attend ?

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Les actions qui m'engagent ressortent mieux que les nouvelles positives.
- **Simplicité :** Je retrouverais plus directement la tombola qui attend sa clôture.
- **Actions visibles :** Préparer la clôture annonce une vérification plutôt qu'une fermeture immédiate.
- **Risque d’erreur :** Les statuts restent lisibles, ce qui m'aide à ne pas confondre brouillon et événement fini.
- **Préférence :** nouvelle
- **Difficultés restantes :** Je vérifierais ce que les filtres Période et Statut affectent exactement avant de m'y fier.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** La séparation entre tâche à traiter et nouvelle reçue est plus exploitable pour plusieurs animations.
- **Simplicité :** Je peux partir d'un dossier qui attend réellement une intervention.
- **Actions visibles :** Les accès aux invitations et à la préparation de clôture sont immédiatement repérables.
- **Risque d’erreur :** Les catégories explicites réduisent les confusions entre état et urgence.
- **Préférence :** nouvelle
- **Difficultés restantes :** Les filtres Période et Statut sont éloignés ; leur périmètre doit être explicite et cohérent pour éviter une vue partielle incomprise.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** Je reconnais immédiatement les deux interventions attendues.
- **Simplicité :** Cette hiérarchie paraît plus rapide à parcourir, sans mesure de gain pour l'instant.
- **Actions visibles :** La création et les boutons d'action sont visibles.
- **Risque d’erreur :** Les libellés limitent les fausses alertes sans supprimer les nouvelles.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le filtre de période près des prochaines actions mérite un intitulé de portée pour éviter de masquer des tâches futures.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Je repère les deux tâches avant les bonnes nouvelles.
- **Simplicité :** Je peux commencer par l’action de mon association sans parcourir les alertes historiques.
- **Actions visibles :** Préparer la clôture et Voir les invitations sont immédiatement identifiables.
- **Risque d’erreur :** Le mot Action attendue limite la confusion avec une publication réussie ; le risque réel n’a pas été mesuré.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le filtre Période voisin des tâches me fait hésiter : filtre-t-il aussi les échéances futures ?

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** La nouvelle hiérarchie sépare intervention, réussite et information sans changer l’identité.
- **Simplicité :** Je peux balayer les tâches avant de lire les nouvelles ; c’est un gain attendu, pas une mesure.
- **Actions visibles :** Créer une animation reste très visible, les liens des nouvelles restent accessibles.
- **Risque d’erreur :** Les libellés complètent les couleurs et évitent de faire passer toutes les nouvelles pour des urgences.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La portée des filtres Période et Statut mérite d’être précisée ; je ne veux pas masquer une tâche à venir en regardant trente jours passés.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Je reconnais mieux ce qui réclame mon intervention et ce qui est une nouvelle positive.
- **Simplicité :** J’ai moins de messages de même apparence à interpréter.
- **Actions visibles :** Préparer la clôture dit clairement ce que je peux faire.
- **Risque d’erreur :** La couleur est accompagnée de mots, ce qui aide à éviter de tout lire comme une alerte.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je ne sais pas encore ce que les trente derniers jours changent dans la liste des prochaines actions.

</details>

### B1 — Sauvegarder avant la fin des sept étapes

[Maquette finale](../visuels/maquettes-apres/B1.html) · vote initial simulé : 12/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : le brouillon est distinct de la publication.
- **Simplicité :** Oui, l'interruption devient possible avant sept étapes.
- **Actions visibles :** Oui, Enregistrer est identifié et séparé de Continuer.
- **Risque d’erreur :** Le message d'échec évite une fausse impression de sauvegarde.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Il manque encore une illustration de sortie avec des modifications postérieures à la dernière sauvegarde.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, un projet incomplet devient un résultat assumé.
- **Simplicité :** Oui, pour organiser le travail en plusieurs sessions.
- **Actions visibles :** Oui, sauvegarde explicite sans promesse de mise en ligne.
- **Risque d’erreur :** Le message d'échec évite de considérer une écriture fictive comme réussie.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le contrat de brouillon partiel demeure un chantier L, la maquette ne le rend pas trivial.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui, la préparation incomplète n'est pas publiable.
- **Simplicité :** Oui, un organisateur interrompu peut reprendre.
- **Actions visibles :** Oui, enregistrer n'envoie rien selon les textes.
- **Risque d’erreur :** Les prérequis de publication sont maintenus dans la proposition.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Une reprise après perte de réseau doit être vérifiée dans le futur produit.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, l'état non enregistré est explicite.
- **Simplicité :** Oui, une interruption n'exige plus de finir le formulaire.
- **Actions visibles :** Oui, réessayer est séparé de continuer.
- **Risque d’erreur :** L'alerte n'affirme pas à tort que la saisie est conservée durablement.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Sur mobile, l'action de reprise se trouve après le formulaire ; tester sa découverte au clavier et en lecture vocale.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui, le résultat incomplet est explicite.
- **Simplicité :** Gain de reprise plausible, aucune durée mesurée.
- **Actions visibles :** La commande de sauvegarde est clairement dessinée.
- **Risque d’erreur :** L'état d'échec est utile ; sa persistance réelle n'est pas vérifiée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Tester une interruption réelle et la restitution des seuls champs sauvegardés ; le prototype n'enregistre rien.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Je comprends que je peux conserver mon travail sans connaître les dates.
- **Simplicité :** Cela paraît plus simple pour préparer petit à petit ; le gain de temps reste à tester.
- **Actions visibles :** Enregistrer le brouillon est clair quand je descends jusqu'au bouton.
- **Risque d’erreur :** Je vois que cela n'envoie rien, mais je voudrais savoir plus tôt que rien n'est encore enregistré.
- **Préférence :** nouvelle
- **Difficultés restantes :** Sur téléphone le bouton arrive après les dates ; je pourrais croire qu'il faut tout remplir avant de pouvoir enregistrer.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Je peux préparer le nom de notre tombola avant la réunion sur les lots.
- **Simplicité :** L'enregistrement séparé me convient mieux qu'une création à finir en une fois.
- **Actions visibles :** Le bouton Enregistrer est explicite et Continuer reste distinct.
- **Risque d’erreur :** La phrase sur l'absence de publication et d'invitation préserve ma maîtrise des engagements.
- **Préférence :** nouvelle
- **Difficultés restantes :** Je voudrais une confirmation très nette après le clic ; cette image de saisie ne montre pas la réussite réelle de l'enregistrement.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Le périmètre minimal du brouillon est clair et les champs ultérieurs peuvent rester vides.
- **Simplicité :** Cela correspond à une préparation municipale en plusieurs séances.
- **Actions visibles :** Enregistrer et Continuer ont des rôles distincts.
- **Risque d’erreur :** L'absence d'envoi implicite est utile ; il faudra prouver la reprise fidèle et les erreurs de sauvegarde avec le vrai contrat.
- **Préférence :** nouvelle
- **Difficultés restantes :** L'état non enregistré pourrait être visible près du titre, surtout lors d'une interruption sur mobile.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** L'enregistrement partiel est compréhensible et séparé de la progression.
- **Simplicité :** Cela répond à mes interruptions, mais je dois descendre longtemps sur mobile pour sauvegarder.
- **Actions visibles :** Le bouton est visible en bas ; je voudrais retrouver la sauvegarde depuis le haut du formulaire.
- **Risque d’erreur :** La phrase sur l'absence d'envoi est utile ; la présence d'un bouton ne démontre pas une sauvegarde réussie.
- **Préférence :** nouvelle
- **Difficultés restantes :** Afficher non enregistré puis l'état confirmé, et rapprocher la commande de sauvegarde d'un repère permanent sans créer un nouveau parcours.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Je comprends que mon travail peut être gardé avec un nom, sans tous les renseignements.
- **Simplicité :** Cela correspond à ma préparation entre deux rendez-vous ; je suppose moins de ressaisie sans avoir chronométré.
- **Actions visibles :** Enregistrer le brouillon est visible et distinct de Continuer.
- **Risque d’erreur :** La phrase sans publication ni invitation me rassure ; il faudra que l’état enregistré soit fiable.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je veux retrouver simplement ce brouillon après une interruption ; l’image de saisie ne démontre pas cette reprise.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** L’enregistrement partiel et l’absence de diffusion sont bien expliqués.
- **Simplicité :** Je peux garder des textes avant de connaître les dates, ce qui correspond à mon travail.
- **Actions visibles :** L’enregistrement a une action dédiée et les étapes restent disponibles.
- **Risque d’erreur :** La distinction entre sauvegarder et continuer limite une confusion ; la persistance reste une dépendance technique.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Après une modification ultérieure, il faudra indiquer précisément ce qui n’est pas encore enregistré ; ce premier état ne couvre pas tout.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Je peux commencer sans tout savoir, et le mot brouillon reste visible.
- **Simplicité :** Je n’ai plus besoin de finir les sept étapes pour garder cette première partie.
- **Actions visibles :** Enregistrer le brouillon se distingue de Continuer grisé.
- **Risque d’erreur :** Le texte dit bien que rien n’est publié ni envoyé ; cela réduit mon hésitation attendue.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Informations publiques peut encore me faire hésiter avant la phrase rassurante en bas ; rappeler près du titre que le brouillon n’est pas public serait utile.

</details>

### B2 — Expliquer préparation, accords et publication

[Maquette finale](../visuels/maquettes-apres/B2.html) · vote initial simulé : 12/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : préparer, accords et publication forment un chemin lisible.
- **Simplicité :** Oui, chaque blocage possède un lien ciblé.
- **Actions visibles :** Oui, l'action et la raison sont rapprochées.
- **Risque d’erreur :** Le bouton indisponible et les explications limitent la confusion entre brouillon et publication.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Sur mobile le texte allonge fortement la page ; vérifier la lecture sans réduire les explications essentielles.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, le résultat promis et les dépendances externes sont lisibles.
- **Simplicité :** Oui, sans second parcours de création.
- **Actions visibles :** Oui, les actions attendues ont un responsable explicite.
- **Risque d’erreur :** La promesse cinq à dix minutes n'est pas présentée comme une durée acquise.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Vérifier les acteurs et diagnostics réellement disponibles dans le contrat avant de produire ces messages.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui : qui agit et pourquoi sont explicités.
- **Simplicité :** Oui, les blocages conduisent à une tâche concrète.
- **Actions visibles :** Oui, inviter et configurer sont distincts.
- **Risque d’erreur :** Accord commerçant et publication ne sont pas fusionnés.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Conserver la responsabilité de remise et tous les prérequis quand le cas contient plusieurs commerces.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, les étapes générales sont en langage courant.
- **Simplicité :** Oui, le besoin d'aide peut diminuer, à vérifier.
- **Actions visibles :** Oui, tâche et bouton sont côte à côte ou empilés.
- **Risque d’erreur :** Le bouton désactivé est expliqué, contrairement à un simple contrôle muet.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La longueur mobile peut fatiguer ; ne pas cacher la raison du blocage dans un repli inaccessible.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui, le chemin de publication est mieux décrit.
- **Simplicité :** Moins de recherche attendue, sans mesure.
- **Actions visibles :** Actions et responsables sont visibles.
- **Risque d’erreur :** La proposition évite la confusion entre création et publication.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Ne pas déduire de l'écran une publication en cinq à dix minutes ou un délai de réponse commerçant.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Je comprends mieux les trois moments : préparer, attendre les accords, puis publier.
- **Simplicité :** Les choses manquantes sont plus concrètes que des diagnostics techniques.
- **Actions visibles :** Je sais qu'il faut ouvrir les invitations puis ajouter le cadeau.
- **Risque d’erreur :** Le bouton Publier grisé est expliqué ; je risque moins de croire que l'animation est déjà publique.
- **Préférence :** nouvelle
- **Difficultés restantes :** Dotation reste un mot moins familier que cadeaux ou lots, même si la phrase en dessous m'aide.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Ajouter la dotation est expliqué par le cadeau, le responsable et les consignes.
- **Simplicité :** Les deux éléments à compléter sont faciles à suivre.
- **Actions visibles :** Je sais où ouvrir les invitations et où configurer nos lots.
- **Risque d’erreur :** Les accords et la publication restent séparés, ce qui limite les engagements involontaires.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le mot dotation peut rester, mais j'ajouterais lots dans le libellé du bouton pour notre usage occasionnel.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Action, responsable et raison du blocage sont réunis.
- **Simplicité :** Je peux répartir les tâches de préparation plus facilement.
- **Actions visibles :** Les accès ciblés réduisent la recherche dans les rubriques.
- **Risque d’erreur :** La publication reste une étape distincte après vérification, sans promesse de délai.
- **Préférence :** nouvelle
- **Difficultés restantes :** Je voudrais que l'état attente du commerce se distingue de l'action encore à notre charge dans tous les cas, pas seulement cet exemple.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** Les deux blocages sont concrets et attribués à la bonne personne dans cet exemple.
- **Simplicité :** Je peux aller directement à l'endroit à corriger.
- **Actions visibles :** Ouvrir les invitations et Configurer la dotation donnent une destination précise.
- **Risque d’erreur :** Le bouton de publication et le rappel de contrôle évitent de présenter le brouillon comme prêt.
- **Préférence :** nouvelle
- **Difficultés restantes :** La présentation est assez espacée pour seulement deux tâches ; avec dix blocages il faudra vérifier que l'action prioritaire reste évidente.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Je vois les trois moments et ce qui manque avant de publier.
- **Simplicité :** Les liens ciblés évitent de rechercher moi-même où corriger.
- **Actions visibles :** Inviter la librairie est attribué à moi ; la dotation a sa propre action.
- **Risque d’erreur :** L’écran mobile distingue invitation et accord, et n’invente pas une activation du compte.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le bouton Préparer l’invitation mobile ne répète pas le nom du destinataire ; je le revérifierais avant l’envoi.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** Les responsabilités et la dotation manquante se lisent facilement.
- **Simplicité :** Les entrées ciblées devraient éviter des allers-retours entre rubriques.
- **Actions visibles :** Ouvrir les invitations et Configurer la dotation correspondent aux deux obstacles affichés.
- **Risque d’erreur :** L’accord n’est pas assimilé à une activation ; publier reste une décision distincte après les contrôles.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je vérifierai dans les autres états la disponibilité effective du QR final ; les images examinées ne prouvent pas la production de supports.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Préparer, obtenir les accords, publier raconte une histoire que je peux suivre.
- **Simplicité :** Les tâches sont exprimées avec des verbes, même si dotation reste un mot moins familier.
- **Actions visibles :** Le commerce à inviter est nommé et l’action m’est attribuée.
- **Risque d’erreur :** Inviter ne signifie pas obtenir un accord ; l’état inconnu du compte n’est pas présenté comme activé.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le texte sur l’activation est assez long sur téléphone ; je veux une explication courte sans supprimer cette distinction.

</details>

### B3 — Proposer un seuil de passeport cohérent

[Maquette finale](../visuels/maquettes-apres/B3.html) · vote initial simulé : 12/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : seuil, sélection et conséquence se lisent ensemble.
- **Simplicité :** Oui, le cas initial ne demande plus de réparer une incohérence.
- **Actions visibles :** Oui, ajuster et revoir les commerces sont distincts.
- **Risque d’erreur :** L'ancienne valeur est explicite et aucune modification silencieuse n'est proposée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** L'écran simplifié ne montre pas tous les champs Mission ; préciser qu'ils restent présents dans le produit.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, une petite incohérence est traitée au bon endroit.
- **Simplicité :** Oui, optimisation locale utile.
- **Actions visibles :** Oui, ajustement explicite conservé.
- **Risque d’erreur :** La règle choisie n'est pas modifiée à l'insu de l'organisateur.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La simplicité du cas deux commerces ne démontre pas tous les cas limites.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui : le nombre de commerces est relié à la règle.
- **Simplicité :** Oui, choix initial atteignable.
- **Actions visibles :** Oui, modifier le seuil reste une décision.
- **Risque d’erreur :** La réduction de sélection ne réécrit pas la règle silencieusement.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je maintiens ma préférence de priorité P2, sans rejeter cette maquette P1 retenue par le facilitateur.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, le sens de deux commerces est expliqué.
- **Simplicité :** Oui, la valeur impossible n'est plus proposée initialement.
- **Actions visibles :** Oui, appliquer et revoir sont explicites.
- **Risque d’erreur :** La correction est volontaire et son effet annoncé.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La description de mission absente de cette vue simplifiée doit rester dans le parcours réel ; tester les libellés du select au lecteur d'écran.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui, conséquence et correction sont explicitées.
- **Simplicité :** Optimisation crédible du cas observé.
- **Actions visibles :** Le choix explicite est visible.
- **Risque d’erreur :** Le contrôle serveur reste une condition future.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** L'AVANT ne montre pas le seuil dans la portion capturée ; conserver la limite de preuve AN-05 et DOM, sans reconstruction.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Deux commerces à visiter parmi deux sélectionnés est une explication que je comprends.
- **Simplicité :** Je n'ai plus à réparer moi-même un chiffre impossible.
- **Actions visibles :** Je repère le choix du nombre, Revoir la sélection et Continuer.
- **Risque d’erreur :** L'explication des deux commerces distincts me paraît limiter le malentendu sur deux visites au même endroit.
- **Préférence :** nouvelle
- **Difficultés restantes :** Je veux savoir si Date limite de réponse concerne bien les commerçants, pas les participants.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** La règle des deux commerces distincts me paraît compréhensible.
- **Simplicité :** Le chiffre proposé évite une correction qui n'apporterait rien.
- **Actions visibles :** Les boutons permettent de revoir les commerces ou de poursuivre.
- **Risque d’erreur :** Je risque moins de croire que deux validations dans le même commerce suffisent.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le passeport n'est pas mon usage principal ; je ne juge pas ici la totalité de ses règles.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Le nombre de commerces et la règle proposée sont rapprochés.
- **Simplicité :** Je comprends le choix sans revenir à la sélection pour recompter.
- **Actions visibles :** Revoir la sélection fournit un retour utile.
- **Risque d’erreur :** L'initialisation paraît cohérente ; l'image compatible ne prouve pas le traitement d'une modification ultérieure.
- **Préférence :** nouvelle
- **Difficultés restantes :** Il faudra vérifier les bornes et le message après retrait d'un commerce ; Date limite de réponse devrait nommer son destinataire.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** Le seuil et sa conséquence sont expliqués sans détour.
- **Simplicité :** Je n'ai plus le réglage impossible que j'avais signalé.
- **Actions visibles :** Je peux modifier le nombre ou revoir les commerces.
- **Risque d’erreur :** La règle des commerces distincts est conservée ; il faut toujours contrôler une sélection devenue incompatible.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le message de compatibilité est assez volumineux pour une situation normale ; à tester pour ne pas ralentir la lecture répétée.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Deux commerces à visiter sur deux sélectionnés a un sens immédiat.
- **Simplicité :** Je ne dois plus corriger une proposition impossible au premier passage.
- **Actions visibles :** Continuer et Revoir la sélection sont faciles à choisir.
- **Risque d’erreur :** Le texte explique des commerces distincts ; il ne me promet pas que leurs accords sont obtenus.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Il restera à vérifier la réaction si je change les commerces après avoir choisi la règle ; cette première image ne la prouve pas.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** Le seuil choisi et sa conséquence sont proches du champ.
- **Simplicité :** Une valeur initiale cohérente économise une correction purement mécanique attendue.
- **Actions visibles :** Le réglage et Revoir la sélection se trouvent sans ambiguïté.
- **Risque d’erreur :** La règle des commerces distincts est explicitée ; le contrôle serveur reste à réaliser.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le cas initial à deux commerces est clair ; les cas de retrait et d’ajout devront garder ma décision sans changement silencieux.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Je comprends qu’il faut visiter deux commerces différents.
- **Simplicité :** Le choix proposé m’évite une erreur dont je ne saurais pas toujours trouver la cause.
- **Actions visibles :** Continuer est visible après l’explication du réglage.
- **Risque d’erreur :** La cohérence affichée rassure, mais je dois encore comprendre qu’un choix compatible ne vaut pas publication.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Seuil reste un mot technique ; le libellé Nombre de commerces à visiter est plus concret et pourrait être le titre principal.

</details>

### C1 — Rendre trouvable l’ajout d’un commerce absent

[Maquette finale](../visuels/maquettes-apres/C1.html) · vote initial simulé : 9/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : le commerce absent a une entrée contextuelle.
- **Simplicité :** Oui pour demander ; le traitement externe reste inconnu.
- **Actions visibles :** Oui, bouton et retour sont repérables.
- **Risque d’erreur :** La demande ne prétend pas associer ni activer le commerce.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le terme référencement et la personne qui examine la demande restent abstraits.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, le besoin est mieux nommé.
- **Simplicité :** Partiellement, une demande n'assure pas sa résolution.
- **Actions visibles :** Oui, l'entrée est claire et le suivi illustré.
- **Risque d’erreur :** La dissociation compte, référencement et participation est préservée.
- **Préférence :** SANS_PREFERENCE
- **Difficultés restantes :** Je garde ma réserve tant que propriétaire, coût et circuit réel de demande ne sont pas vérifiés.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui, le commerce demandé ne devient pas participant.
- **Simplicité :** Oui pour signaler une absence.
- **Actions visibles :** Oui, suivi et retour sont compréhensibles.
- **Risque d’erreur :** Aucune activation ou invitation implicite n'est représentée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** L'organisateur doit savoir qui traite la demande, sans inventer de délai de traitement.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, une question simple remplace une impasse.
- **Simplicité :** Oui, une personne peut demander un seul commerce sans fichier.
- **Actions visibles :** Oui, le bouton principal répond directement au problème.
- **Risque d’erreur :** La demande ne vaut pas invitation.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Référencement et référentiel restent du jargon ; préférer une explication comme rendre le commerce disponible dans la liste.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui, la demande est intelligible comme proposition.
- **Simplicité :** Simplicité de la résolution inconnue.
- **Actions visibles :** L'entrée est plus visible que l'absence de parcours trouvé.
- **Risque d’erreur :** Les effets automatiques sont exclus par les textes.
- **Préférence :** SANS_PREFERENCE
- **Difficultés restantes :** Le parcours canonique et son accessibilité initiale restent inconnus ; ma réserve du vote n'est pas levée par une maquette.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Le bouton Mon commerce n'est pas dans la liste répond directement à ma question.
- **Simplicité :** Demander un seul commerce semble plus accessible qu'un fichier à importer.
- **Actions visibles :** Je sais où transmettre la demande et comment revenir à ma sélection.
- **Risque d’erreur :** Le message explique que cela n'invite personne et n'ajoute pas encore le commerce.
- **Préférence :** nouvelle
- **Difficultés restantes :** Je ne sais pas à qui ma demande est transmise, quels champs sont indispensables ni comment je saurai qu'on m'a répondu.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Je distingue la demande de référencement de l'invitation à participer.
- **Simplicité :** Pour un nouveau partenaire, le petit formulaire paraît abordable.
- **Actions visibles :** Transmettre la demande et Retour à la sélection sont bien séparés.
- **Risque d’erreur :** Le texte dit clairement qu'aucun compte ni accord n'est créé par ce geste.
- **Préférence :** nouvelle
- **Difficultés restantes :** Il manque pour moi le service qui prend la demande en charge et l'indication des champs obligatoires.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Le chemin pour un commerce manquant est visible et ne prétend pas activer un compte.
- **Simplicité :** Le formulaire est court, mais la procédure de traitement reste inconnue.
- **Actions visibles :** L'action de transmettre est explicite et ne se confond pas avec l'import.
- **Risque d’erreur :** Les effets exclus sont bien indiqués ; le suivi devra afficher un état réel provenant du circuit canonique.
- **Préférence :** nouvelle
- **Difficultés restantes :** Responsable de traitement, champs requis et moyen de consulter la réponse sont à préciser sans inventer un délai de service.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** Je comprends où demander un commerce absent et ce que cela ne fait pas.
- **Simplicité :** Le formulaire paraît simple, mais l'attente opérationnelle demeure inconnue.
- **Actions visibles :** Les boutons sont visibles et nommés.
- **Risque d’erreur :** La séparation demande/invitation est bonne ; je ne peux pas conclure sur le traitement réel.
- **Préférence :** sans préférence
- **Difficultés restantes :** Je conserve ma réserve tant que le circuit canonique, son responsable et la reprise de ma sélection ne sont pas établis.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Je comprends où aller quand un partenaire manque et qu’une demande précède sa sélection.
- **Simplicité :** Le point d’entrée m’évite une recherche extérieure, mais le travail ne sera fini qu’au référencement.
- **Actions visibles :** Mon commerce n’est pas dans la liste répond exactement à mon problème.
- **Risque d’erreur :** Le suivi indique non associé et aucune invitation, ce qui évite une fausse impression de participation.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Demande transmise ne me dit pas qui la traite ni comment reprendre contact. Ne pas inventer un responsable ; expliciter ce qui reste inconnu.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** Le commerce absent mène à une demande, pas à un compte actif.
- **Simplicité :** Je peux choisir entre demande individuelle et import sans chercher une autre section.
- **Actions visibles :** L’action individuelle est bien nommée, le suivi affiche une référence fictive.
- **Risque d’erreur :** Non associé, aucune invitation envoyée protège la distinction entre demande et participation.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La confirmation devrait indiquer comment suivre une attente prolongée ; le responsable et le circuit réels doivent être vérifiés avant d’afficher une promesse.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Je sais enfin quoi faire pour signaler le commerce manquant.
- **Simplicité :** L’entrée individuelle me paraît plus simple que préparer un fichier pour une seule personne.
- **Actions visibles :** Le bouton décrit mon problème, puis le suivi dit que le commerce n’est pas encore disponible.
- **Risque d’erreur :** Aucune invitation envoyée évite de croire que la personne a déjà été contactée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** À qui la demande a-t-elle été transmise ? Si on ne sait pas encore, il faut le dire dans le dossier de conception et ne pas nommer un service imaginaire.

</details>

### C2 — Sécuriser la compréhension de l’import

[Maquette finale](../visuels/maquettes-apres/C2.html) · vote initial simulé : 9/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui sur bureau : similitude et conflit sont distingués.
- **Simplicité :** Oui pour examiner les deux lignes sur bureau ; non sur le rendu mobile initial.
- **Actions visibles :** Oui, comparer et revoir les colonnes sont séparés.
- **Risque d’erreur :** Le choix humain est préservé ; le mobile masque la deuxième colonne hors du cadre initial.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Corriger la comparaison mobile pour rendre les deux lignes visibles ou leur défilement explicite.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, les limites de contrôle sont enfin visibles.
- **Simplicité :** Oui sur bureau ; le mobile demande correction.
- **Actions visibles :** Oui, la décision humaine est une action claire.
- **Risque d’erreur :** Le doute n'est ni une fusion ni un blocage automatique.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** L'effort L reste à cadrer ; ne pas présenter le moteur de similitude comme déjà disponible.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui, deux commerces semblables ne sont pas déclarés identiques.
- **Simplicité :** Oui sur bureau ; contrôle difficile si une colonne manque sur mobile.
- **Actions visibles :** Oui, sélection humaine et retour sont explicités.
- **Risque d’erreur :** Pas de fusion automatique et possibilité de corriger le fichier.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Les cas de conflit fort doivent conserver leur traitement canonique au-delà de cet exemple sans identifiants.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui sur bureau, pas suffisamment sur mobile initial.
- **Simplicité :** Partiellement, une colonne hors champ empêche une comparaison évidente.
- **Actions visibles :** Oui sur bureau ; l'accès au contenu mobile doit être rendu perceptible.
- **Risque d’erreur :** Le discours limite les faux doublons, mais l'information masquée gêne le contrôle.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Empiler Ligne 2 et Ligne 3 ou fournir un défilement nommé, visible et accessible au clavier.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui sur les limites du rapprochement.
- **Simplicité :** Le bureau paraît plus explicite, le mobile initial est incomplet visuellement.
- **Actions visibles :** Comparaison et sélection sont matérialisées.
- **Risque d’erreur :** Aucune preuve que le moteur proposé détecte ces cas ; seule la présentation est évaluée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Corriger la colonne mobile hors champ puis faire expliquer le sens de zéro conflit à une personne réelle.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Je comprends surtout que deux lignes se ressemblent et qu'il faut vérifier.
- **Simplicité :** Le tableau reste difficile pour moi et je demanderais encore de l'aide.
- **Actions visibles :** Comparer les deux lignes est visible ; sur téléphone je ne vois pas les cases de sélection.
- **Risque d’erreur :** Le texte évite de croire que zéro conflit signifie zéro doublon, mais je ne saurais pas décider seule.
- **Préférence :** sans préférence
- **Difficultés restantes :** Le côté droit du tableau est coupé sur téléphone et le vocabulaire identifiants/SIRET me demande encore une explication.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** La ressemblance est signalée sans affirmer qu'il s'agit certainement du même commerce.
- **Simplicité :** Je comprends mieux le contrôle, mais l'import n'est pas mon outil habituel.
- **Actions visibles :** Sur ordinateur je peux lire et comparer ; les cases à droite disparaissent du rendu mobile.
- **Risque d’erreur :** Je retiens qu'aucune fusion n'est automatique et que le zéro ne suffit pas à me rassurer.
- **Préférence :** sans préférence
- **Difficultés restantes :** Je ferais traiter ce fichier par une personne plus à l'aise ; le contrôle à droite doit être accessible sur téléphone.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Les ressemblances et la limite du zéro conflit sont mieux expliquées.
- **Simplicité :** L'aperçu me permet de décider après comparaison plutôt que de remapper à l'aveugle.
- **Actions visibles :** Les cases sont visibles sur bureau ; elles sont hors cadre dans le rendu mobile.
- **Risque d’erreur :** Ne pas fusionner automatiquement protège des homonymes ; la formulation évite une fausse garantie.
- **Préférence :** nouvelle
- **Difficultés restantes :** Sur téléphone la sélection devient invisible : une liste de fiches ou une colonne d'action accessible est nécessaire avant validation visuelle.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** L'avertissement décrit précisément les deux lignes à examiner.
- **Simplicité :** Sur bureau la lecture est plus orientée décision ; sur mobile je dois deviner le tableau hors cadre.
- **Actions visibles :** Comparer est visible, mais les cases à droite ne le sont pas sur téléphone.
- **Risque d’erreur :** La prudence sur les doublons est bonne ; cacher la sélection peut provoquer une décision incomplète.
- **Préférence :** nouvelle
- **Difficultés restantes :** Corriger le mobile avant la restitution et prévoir un accès direct aux champs comparés pour les fichiers plus longs.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Deux lignes se ressemblent me parle davantage que zéro conflit.
- **Simplicité :** Comparer les deux lignes est une bonne prochaine étape, même si je dois décider moi-même.
- **Actions visibles :** Les sélections sont explicites et non précochées sur l’image.
- **Risque d’erreur :** Je comprends que zéro conflit ne garantit pas zéro doublon et qu’aucune fusion automatique n’est prévue.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je ne sais pas décider si je manque d’information ; prévoir la possibilité claire de reprendre après vérification extérieure, sans inventer une identité.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** La similitude est nommée comme doute et les identifiants absents expliquent la limite.
- **Simplicité :** La comparaison est plus utile qu’un compteur zéro conflit isolé.
- **Actions visibles :** Comparer est l’action dominante ; Revoir les colonnes reste disponible.
- **Risque d’erreur :** L’absence de fusion ou exclusion automatique est claire et protège la décision humaine.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je souhaite vérifier aussi les colonnes reconnues, les vraies erreurs email/SIRET et la confirmation finale ; l’aperçu seul ne couvre pas le flux complet.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Je comprends le doute entre deux lignes, mais je reste peu à l’aise avec l’import.
- **Simplicité :** Je ne peux pas dire que cela me ferait gagner du temps puisque je n’utilise pas ce parcours.
- **Actions visibles :** Comparer les deux lignes est lisible, les cases me demandent une décision.
- **Risque d’erreur :** La phrase sur zéro conflit m’empêche de croire que tout est vérifié ; je demanderais encore de l’aide.
- **Préférence :** SANS_PREFERENCE
- **Difficultés restantes :** Je ne sais pas quelle ligne choisir quand les deux sont identiques. La maquette explique la limite mais ne peut pas remplacer la connaissance du commerce.

</details>

### D1 — Rétablir et fiabiliser Communication

[Maquette finale](../visuels/maquettes-apres/D1.html) · vote initial simulé : 12/12, P0.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : lecture impossible et envoi incertain sont différenciés.
- **Simplicité :** Oui, chaque état fournit une action de reprise appropriée.
- **Actions visibles :** Oui, vérifier l'envoi ne ressemble pas à renvoyer.
- **Risque d’erreur :** La non-répétition de l'envoi réduit un risque de compréhension ; aucun effet serveur n'est prouvé.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Envoi confirmé désigne en réalité une demande de diffusion confirmée : harmoniser titre et portée.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui pour les états opérationnels.
- **Simplicité :** Oui pour comprendre la prochaine action ; aucune preuve de fiabilité réelle.
- **Actions visibles :** Oui, reprise et support existent dans la proposition.
- **Risque d’erreur :** Les états incertains évitent la suggestion d'un nouvel envoi immédiat.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La condition de lancement reste le rétablissement et la recette réelle du service, pas l'approbation de cet écran.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui, lecture et diffusion sont clairement des opérations différentes.
- **Simplicité :** Oui, vérifier une tentative existante est le bon prochain geste.
- **Actions visibles :** Oui, reprise et support sont distingués.
- **Risque d’erreur :** Le texte décourage un renvoi pouvant solliciter deux fois les participants.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La consultation de l'état doit réellement identifier la tentative existante ; ce contrat n'est pas prouvé par le rendu.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, l'erreur dit ce qui a échoué.
- **Simplicité :** Oui, une prochaine possibilité est proposée.
- **Actions visibles :** Oui, vérifier ne suggère pas de renvoyer.
- **Risque d’erreur :** Le texte évite une conclusion hâtive d'échec définitif de l'envoi.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Envoi confirmé paraît plus fort que demande confirmée ; garder un vocabulaire cohérent et annoncer les changements d'état aux aides techniques.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui sur la distinction des catégories d'erreur.
- **Simplicité :** La suite est compréhensible ; service réellement non retesté.
- **Actions visibles :** Les boutons de vérification et de support sont distincts.
- **Risque d’erreur :** Aucun rétablissement du 500 démontré par cet APRÈS.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Titre Envoi confirmé à aligner sur la demande de diffusion ; séparer jugement d'interface et preuve de livraison.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Je comprends que les messages ne chargent pas et que ce n'est pas un envoi que j'aurais déclenché.
- **Simplicité :** Réessayer est un geste simple ; contacter le support me semble encore moins direct.
- **Actions visibles :** Je vois Réessayer le chargement, puis les informations pour le support.
- **Risque d’erreur :** La phrase sur l'absence d'envoi rassure, sans me garantir que le service est réparé.
- **Préférence :** nouvelle
- **Difficultés restantes :** Que dois-je faire des informations du support, et comment joindre quelqu'un si Réessayer ne marche pas ?

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Le message distingue la lecture de messages d'un envoi.
- **Simplicité :** Je comprends quoi réessayer, sans croire que je dois renvoyer ma communication.
- **Actions visibles :** Les deux boutons de reprise et de support sont visibles.
- **Risque d’erreur :** C'est plus rassurant pour éviter un second envoi inutile ; cela ne prouve pas encore le rétablissement.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le support doit déboucher sur une démarche concrète si l'erreur persiste.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** La nature de l'échec et la conservation du contexte sont explicites.
- **Simplicité :** Je peux retenter une lecture sans recommencer mes filtres.
- **Actions visibles :** Réessayer et Support constituent deux issues compréhensibles.
- **Risque d’erreur :** La distinction lecture/envoi diminue le risque de mauvaise réaction, mais seule une recette pourra établir le comportement réel.
- **Préférence :** nouvelle
- **Difficultés restantes :** Il manque dans cette vue le contenu du support et la procédure si la panne dure ; aucun délai de résolution ne doit être inventé.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** L'écran explique ce qui a échoué sans laisser penser qu'un message a été envoyé.
- **Simplicité :** La reprise ciblée est utile si le service fonctionne réellement après correction.
- **Actions visibles :** Je peux réessayer sans revenir à la liste des animations.
- **Risque d’erreur :** La différenciation des erreurs est utile ; les autres états d'envoi devront être vérifiés séparément.
- **Préférence :** nouvelle
- **Difficultés restantes :** Ne pas compter cet écran plus clair comme une résolution du 500 ; l'aide au support doit être directement exploitable.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Je distingue un problème de chargement d’un envoi dont le résultat est inconnu.
- **Simplicité :** Deux issues utiles sont proposées : vérifier ou demander de l’aide.
- **Actions visibles :** Sur mobile, Vérifier l’état de cet envoi est bien plus sûr à comprendre que Réessayer.
- **Risque d’erreur :** La consigne de ne pas créer un second envoi est explicite ; la maquette ne garantit pas le comportement serveur.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Après plusieurs vérifications sans résultat, je voudrais savoir quand et comment reprendre contact avec le support, sans délai promis arbitrairement.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** Lecture impossible et résultat d’envoi incertain sont enfin deux situations distinctes.
- **Simplicité :** Les actions correspondent au problème, sans demander de recommencer aveuglément.
- **Actions visibles :** Vérifier l’état de cet envoi annonce explicitement qu’il ne renvoie rien.
- **Risque d’erreur :** La tentative existante et sa date limitent le risque de doublon dans la présentation ; l’idempotence et les statuts réels restent à prouver.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Un résultat confirmé doit distinguer demande acceptée, message envoyé et réception si ces données existent ; je ne déduis pas leur équivalence de cette maquette.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Je comprends mieux ce qui a échoué ; sur téléphone il est dit que le message a peut-être été envoyé.
- **Simplicité :** La vérification indiquée m’évite de choisir moi-même entre attendre et renvoyer.
- **Actions visibles :** Vérifier l’état de cet envoi est compréhensible et le support reste accessible.
- **Risque d’erreur :** Ne créez pas un second envoi est une consigne utile ; aucune réception réelle n’est démontrée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je ne sais pas combien de fois vérifier si l’état reste incertain. Une suite explicite vers le support serait rassurante sans promettre un délai.

</details>

### D2 — Diriger le suivi vers le suivi opérationnel

[Maquette finale](../visuels/maquettes-apres/D2.html) · vote initial simulé : 12/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : suivi et bilan sont séparés.
- **Simplicité :** Oui, le détour disparaît dans la proposition.
- **Actions visibles :** Oui, le bilan conserve un accès nommé distinct.
- **Risque d’erreur :** L'ambiguïté du point d'entrée diminue sans inventer de données temps réel.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le bouton de titre reste visible sur le suivi lui-même ; tester son utilité plutôt que multiplier les accès redondants.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, un terme correspond à sa destination.
- **Simplicité :** Oui, correction de périmètre réduit.
- **Actions visibles :** Oui, le bilan reste séparé.
- **Risque d’erreur :** Réduit une ambiguïté sans ajouter de fonctionnalité.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Vérifier tous les points d'entrée existants lors d'une éventuelle implémentation.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui, je retrouve les commandes d'exploitation.
- **Simplicité :** Oui, le bilan ne se substitue plus au pilotage.
- **Actions visibles :** Oui, les actions sensibles restent distinctes.
- **Risque d’erreur :** La proposition ne confond pas indicateurs et commandes.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Vérifier les confirmations de suspension et annulation dans le parcours complet, hors scénario actuel.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, les mots suivi opérationnel et bilan différencient les buts.
- **Simplicité :** Oui, pas de détour conceptuel imposé.
- **Actions visibles :** Oui, bouton bilan identifiable.
- **Risque d’erreur :** Le risque de se perdre entre deux rubriques est plausiblement réduit.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le vert n'est pas le seul repère ; conserver les textes et vérifier le focus après navigation.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui, le changement est directement lié à AN-16.
- **Simplicité :** Simplification plausible du trajet.
- **Actions visibles :** Les destinations sont distinctes.
- **Risque d’erreur :** Réduction d'ambiguïté, pas mesure de taux d'erreur.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La navigation est illustrée ; vérifier ultérieurement les routes du produit déployé.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Le bilan est mieux séparé, mais suivi opérationnel n'est pas une expression très familière.
- **Simplicité :** Je sais où voir le bilan ; je suis moins sûre de ce que je dois faire dans le suivi.
- **Actions visibles :** Je vois trois actions importantes, dont suspendre et annuler.
- **Risque d’erreur :** Ces trois boutons proches me font craindre d'en choisir un trop vite.
- **Préférence :** sans préférence
- **Difficultés restantes :** J'aimerais savoir simplement ce que je peux consulter sans modifier l'animation ; le bouton Consulter reste affiché alors que je suis déjà dans le suivi.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Le bilan possède maintenant son propre bouton, ce qui m'aide à le retrouver.
- **Simplicité :** Je fais moins de détour pour choisir entre bilan et opérations.
- **Actions visibles :** La clôture est nommée Préparer, et les autres commandes restent visibles.
- **Risque d’erreur :** Je voudrais une séparation plus nette d'Annuler cette édition pour ne pas la confondre avec un retour.
- **Préférence :** nouvelle
- **Difficultés restantes :** L'écran montre surtout des commandes ; je ne peux pas juger sur cette image les chiffres qui resteront dans le bilan.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Le suivi et le bilan ont des destinations distinctes.
- **Simplicité :** Je sais où chercher les résultats pour mes comptes rendus.
- **Actions visibles :** Les opérations sont visibles et le bilan garde une entrée dédiée.
- **Risque d’erreur :** Le risque de détour diminue ; la preuve des définitions et dates exige encore la revue de l'état bilan.
- **Préférence :** nouvelle
- **Difficultés restantes :** L'action de consultation en haut devrait refléter que nous sommes déjà dans le suivi, et les commandes sensibles rester protégées.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** Le bilan est séparé et le suivi opérationnel est identifié.
- **Simplicité :** Le parcours annoncé paraît plus direct.
- **Actions visibles :** Les commandes opérationnelles sont là, mais le bouton Consulter le suivi reste redondant sur l'écran cible.
- **Risque d’erreur :** Les confirmations devront rester présentes pour suspendre, annuler ou fermer.
- **Préférence :** nouvelle
- **Difficultés restantes :** Mettre Annuler à distance des actions courantes et éviter une commande qui donne l'impression de rouvrir l'écran où je suis déjà.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** Le suivi opérationnel et le bilan ont maintenant des noms et destinations distincts.
- **Simplicité :** Je suppose un détour évité ; aucun temps gagné n’a été mesuré.
- **Actions visibles :** Les actions sur le jeu sont visibles ; le bilan garde son lien.
- **Risque d’erreur :** La distinction réduit une confusion de navigation, pas les risques propres à suspendre ou annuler.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Suspendre, clôturer et annuler sont proches : je veux garder leurs explications et confirmations dans les écrans suivants.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** Je sais où agir et où lire les chiffres.
- **Simplicité :** La correction est locale et évite le détour constaté vers le bilan.
- **Actions visibles :** Le lien Ouvrir le bilan est conservé et clairement séparé.
- **Risque d’erreur :** On n’annonce pas de données en temps réel ; les définitions doivent rester exactes dans le bilan.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Les actions sensibles restent proches visuellement ; leur confirmation et leur droit d’accès doivent être conservés à l’implémentation.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** Les résultats sont séparés des commandes de pilotage.
- **Simplicité :** Je trouve le bilan sans le confondre avec les actions sur l’animation.
- **Actions visibles :** Ouvrir le bilan est clair ; les commandes d’arrêt demandent davantage d’attention.
- **Risque d’erreur :** La séparation réduit mon erreur de rubrique, mais annuler doit toujours demander une confirmation compréhensible.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Opérationnel est moins familier que Suivi de l’animation ; je vérifierais la compréhension de ce libellé avec d’autres utilisateurs occasionnels.

</details>

### E1 — Rendre explicite le chemin de fin

[Maquette finale](../visuels/maquettes-apres/E1.html) · vote initial simulé : 12/12, P1.

<details><summary>E1 — réaction simulée v1</summary>

- **Clarté :** Oui : période, clôture, fin et archive sont différenciées.
- **Simplicité :** Oui, une tâche attendue est associée à chaque moment illustré.
- **Actions visibles :** Partiellement : le bouton définitif paraît actif avec case vide dans le PNG initial.
- **Risque d’erreur :** Les conséquences sont claires ; l'apparence désactivée doit correspondre à la garde HTML réelle.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Rendre visuellement inactif le bouton avant la coche et indiquer pourquoi.

</details>

<details><summary>E2 — réaction simulée v1</summary>

- **Clarté :** Oui, les étapes métier gardent leur valeur.
- **Simplicité :** Oui pour savoir quoi faire ; aucune automatisation ajoutée.
- **Actions visibles :** Partiellement, le style du bouton définitif est trompeur avant coche.
- **Risque d’erreur :** La distinction tirage, information et remise est conservée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Corriger le style désactivé ; ne pas réintroduire la clôture programmée rejetée.

</details>

<details><summary>E3 — réaction simulée v1</summary>

- **Clarté :** Oui, période finie ne signifie pas clôturée.
- **Simplicité :** Oui, la prochaine responsabilité est lisible.
- **Actions visibles :** Partiellement, bouton de confirmation visuellement actif malgré absence de coche.
- **Risque d’erreur :** Les effets sont expliqués ; la garde HTML existe, mais son apparence doit être corrigée.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** La clôture reste définitive ; aucun tirage ni remise ne doit être déduit de la transition illustrée.

</details>

<details><summary>E4 — réaction simulée v1</summary>

- **Clarté :** Oui, les conséquences sont compréhensibles et proches de la case.
- **Simplicité :** Oui, retour sans clôturer disponible.
- **Actions visibles :** Non complètement : bouton vert avec case vide est un signal contradictoire.
- **Risque d’erreur :** La formulation protège, mais l'état visuel du contrôle doit être corrigé.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Rendre disabled perceptible et expliquer cochez pour activer ; tester lecture de la case et du bouton sur mobile réel.

</details>

<details><summary>E5 — réaction simulée v1</summary>

- **Clarté :** Oui, les états et conséquences sont mieux expliqués.
- **Simplicité :** Simplicité à vérifier lors d'une clôture réelle isolée.
- **Actions visibles :** L'état désactivé n'est pas visuellement fidèle dans le PNG initial.
- **Risque d’erreur :** Les garde-fous sont présents dans le HTML ; la représentation doit les rendre perceptibles.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Aucune nouvelle clôture n'a été exécutée ; la préférence ne valide ni le contrat ni les actions irréversibles.

</details>

<details><summary>Francoise — réaction simulée v1</summary>

- **Clarté :** Je comprends enfin pourquoi une période finie n'est pas encore une animation clôturée.
- **Simplicité :** Les étapes de fin et la prochaine action me guident.
- **Actions visibles :** Je vois Préparer la clôture, puis Revenir sans clôturer sur téléphone.
- **Risque d’erreur :** L'avertissement définitif est clair, mais le bouton vert semble utilisable alors que je n'ai pas coché la case.
- **Préférence :** nouvelle
- **Difficultés restantes :** Il faut faire voir que la case est obligatoire et expliquer participants éligibles avec les mots personnes pouvant gagner.

</details>

<details><summary>Michel — réaction simulée v1</summary>

- **Clarté :** Les étapes et les conséquences sont plus faciles à expliquer à l'association.
- **Simplicité :** Je sais que fermer n'atteste pas que les cadeaux ont été remis.
- **Actions visibles :** Préparer, confirmer et revenir sont nommés sans ambiguïté.
- **Risque d’erreur :** La case et le caractère définitif me rassurent, sous réserve que le bouton soit réellement bloqué tant que la case est vide.
- **Préférence :** nouvelle
- **Difficultés restantes :** Participants éligibles reste technique ; je garderais la formulation personnes pouvant gagner du premier écran.

</details>

<details><summary>Sophie — réaction simulée v1</summary>

- **Clarté :** Les quatre étapes donnent une lecture commune à l'équipe.
- **Simplicité :** La prochaine vérification et les conséquences de fermeture sont explicites.
- **Actions visibles :** Le retour au suivi est disponible avant la confirmation.
- **Risque d’erreur :** La présentation réduit la confusion sur fin de période et fin de dossier, mais la confirmation semble active avec case vide.
- **Préférence :** nouvelle
- **Difficultés restantes :** Il faut distinguer les informations d'état des actions permises et garder les responsables des dossiers dans les états suivants.

</details>

<details><summary>Julie — réaction simulée v1</summary>

- **Clarté :** Les conséquences de chaque étape sont compréhensibles et la fermeture reste manuelle.
- **Simplicité :** La préparation et la confirmation constituent deux gestes assumés.
- **Actions visibles :** La possibilité de revenir sans clôturer est explicite.
- **Risque d’erreur :** La case non cochée avec bouton vert est une incohérence visuelle à corriger avant de conclure que la confirmation protège correctement.
- **Préférence :** nouvelle
- **Difficultés restantes :** Le texte mobile doit garder les mots simples du premier écran et le blocage de confirmation doit être vérifié au clavier et au toucher.

</details>

<details><summary>Karim — réaction simulée v1</summary>

- **Clarté :** La période finie n’est plus présentée comme un travail entièrement terminé.
- **Simplicité :** La prochaine action et le dossier de lot restant forment un parcours compréhensible.
- **Actions visibles :** Ouvrir le dossier de remise est précis ; Terminer reste bloqué tant que le dossier attend.
- **Risque d’erreur :** Informer ne signifie pas remis est clair, et la clôture reste distincte du tirage et de la remise.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Le repère courant de la frise repose beaucoup sur sa barre verte ; ajouter un mot comme Étape actuelle aiderait ma lecture.

</details>

<details><summary>Elodie — réaction simulée v1</summary>

- **Clarté :** Les quatre états ont chacun une explication courte et les lots gardent leur propre tâche.
- **Simplicité :** Le responsable affiché dans l’exemple facilite la coordination sans tout réunir en une seule clôture.
- **Actions visibles :** Le dossier de remise précède logiquement Terminer l’animation.
- **Risque d’erreur :** L’information du gagnant reste distincte de la remise, et aucun automatisme de tirage n’est ajouté.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Je veux que la situation actuelle soit identifiable sans la seule couleur de la frise et que les remises non renseignées ne soient jamais présentées comme non effectuées.

</details>

<details><summary>Bernard — réaction simulée v1</summary>

- **Clarté :** La fin de période, la clôture et la remise ne signifient plus la même chose.
- **Simplicité :** Une prochaine tâche et un dossier restant me donnent un chemin pour terminer.
- **Actions visibles :** Ouvrir le dossier de remise est concret et Terminer indisponible est expliqué.
- **Risque d’erreur :** Le gagnant informé n’est pas marqué comme servi ; la clôture n’effectue ni tirage ni remise automatiquement.
- **Préférence :** NOUVELLE
- **Difficultés restantes :** Dans la frise, tous les titres ont un poids semblable. Dire explicitement Vous êtes à l’étape Clôturée m’aiderait à savoir où j’en suis.

</details>

## Sources intégrales

- [45 fiches experts](revue-maquettes-experts.json)
- [36 fiches métier 1](revue-maquettes-metier-1.json)
- [27 fiches métier 2](revue-maquettes-metier-2.json)

**Validation utilisateur : en attente.** Aucun vote de conception ni autorisation de développement déduit de ces réactions.
