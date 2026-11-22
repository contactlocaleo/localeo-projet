# Orientations non retenues

Sept propositions **REJETÉES** par vote simulé ; aucune ne recueille exactement six voix, donc aucune décision « NON ADOPTÉE » dans cette séance. Le seuil reste sept, même avec abstentions. Les besoins portés par les minorités sont conservés ci-dessous. Une priorité proposée n’autorise pas la réalisation d’une orientation rejetée.

Les critères ci-dessous servent à expliquer l’examen et les contradictions ; ils ne constituent pas un backlog de réalisation. Les risques de faux succès ou de fusion des responsabilités restent critiques, quel que soit le vote.

## A2 — Imposer cinq écrans de tutoriel avant le premier scan

- **Mission :** M1.
- **Problème :** Crainte d’un premier usage sans accompagnement, formulée par Martine.
- **Source :** HYPOTHÈSE issue de la simulation ; première activation et compte débutant non observés. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Un débutant pourrait hésiter ; un commerçant pressé pourrait être retardé.
- **Solution proposée :** Tutoriel obligatoire en cinq écrans avant l’accès initial au scanner.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : présenter toutes les étapes avant la première action.
- **Effort :** M. **Priorité :** P3. **Confiance :** Faible ; aucun test débutant.
- **Vote :** 1 pour / 11 contre / 0 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#a2).
- **Réserve ou argument minoritaire :** Martine vote pour : elle souhaite être guidée la première fois. Les onze autres refusent l’obligation.
- **Dépendances et limites :** Alternative conservée dans A1 : aide facultative au moment utile.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère hypothétique : le débutant restitue le rôle des QR après le tutoriel.
2. Critère de non-régression : aucune personne ne doit être bloquée devant un client ; ce point contredit le caractère obligatoire proposé.

## B2 — Valider automatiquement tout QR reconnu

- **Mission :** M2.
- **Problème :** Patrick souhaite éviter une confirmation répétée pendant la file.
- **Source :** HYPOTHÈSE de rapidité ; C02 décrit déjà une confirmation distincte, sans mesure de son coût. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Gain de geste espéré, mais une lecture accidentelle pourrait provoquer une validation non voulue.
- **Solution proposée :** Supprimer la confirmation après reconnaissance du QR.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : passer plus vite au participant suivant.
- **Effort :** M. **Priorité :** P2. **Confiance :** Faible sur le gain ; risque opérationnel identifié par raisonnement.
- **Vote :** 1 pour / 11 contre / 0 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#b2).
- **Réserve ou argument minoritaire :** Patrick est seul favorable. Sa contrainte de temps reste une exigence de recette de B1.
- **Dépendances et limites :** Non retenue ; aucune modification de la confirmation autorisée par ce workshop.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère d’examen : une lecture involontaire ne déclenche aucun effet métier ; incompatible avec l’automatisme tel que proposé.
2. Toute simplification future conserve une intention explicite et un résultat serveur ; aucun gain n’est accepté sur la seule base du vote.

## C2 — Relancer chaque jour tous les messages non lus par push

- **Mission :** M3.
- **Problème :** Crainte qu’un commerçant ne revienne pas consulter sa boîte.
- **Source :** HYPOTHÈSE ; C06 établit du code WebPush, pas une réception réelle ni le besoin d’une cadence quotidienne. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Rappel possible, mais interruptions sans rapport avec une action restante.
- **Solution proposée :** Push quotidien systématique à tous tant qu’un message reste non lu.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : augmenter les ouvertures de messages.
- **Effort :** L. **Priorité :** P3. **Confiance :** Faible ; aucun canal ou fréquence validé.
- **Vote :** 0 pour / 12 contre / 0 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#c2).
- **Réserve ou argument minoritaire :** Aucun vote favorable ; le besoin d’anticipation de Nadia reste couvert par C1/D1/F1.
- **Dépendances et limites :** Non retenue ; aucun envoi, abonnement ou nouveau canal demandé.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère d’examen : chaque rappel a une action encore pertinente, une échéance et un choix utilisateur ; la systématisation proposée ne respecte pas ces conditions.
2. La réception doit être testée avant toute promesse de canal ; absence de push n’empêche pas de retrouver l’information dans Pro.

## D2 — Fusionner les états dans « Tout est prêt »

- **Mission :** M3 et M4.
- **Problème :** La multiplicité de mots peut décourager les profils peu à l’aise.
- **Source :** HYPOTHÈSE de simulation face à O07/C04 ; aucune équivalence métier démontrée. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Simplicité apparente, mais perte de la responsabilité et des conditions réellement remplies.
- **Solution proposée :** Un bouton unique fusionnerait accepté, prêt, approuvé et contrôlé.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : une décision et un état faciles à lire.
- **Effort :** L. **Priorité :** P2. **Confiance :** Faible sur le bénéfice ; incompatibilité avec la séparation des décisions identifiée.
- **Vote :** 2 pour / 10 contre / 0 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#d2).
- **Réserve ou argument minoritaire :** Martine et Patrick votent pour la simplicité ; cette demande motive la présentation progressive de D1.
- **Dépendances et limites :** Non retenue ; simplifier les mots sans fusionner les règles.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère d’examen : accepter ne doit pas attester l’installation ni l’approbation de l’organisateur.
2. Chaque acteur garde sa décision propre ; ce critère invalide la fusion proposée.

## E2 — Déclarer prêt dès le téléchargement du kit

- **Mission :** M4.
- **Problème :** Patrick souhaite éviter un geste après récupération des documents.
- **Source :** HYPOTHÈSE ; C03 distingue préparation du kit et déclaration prêt. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Un commerce non installé pourrait apparaître prêt auprès de l’organisateur.
- **Solution proposée :** Déclencher automatiquement l’état prêt au téléchargement.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : supprimer une confirmation.
- **Effort :** S. **Priorité :** P2. **Confiance :** Faible sur le gain ; confusion opérationnelle clairement identifiée.
- **Vote :** 1 pour / 11 contre / 0 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#e2).
- **Réserve ou argument minoritaire :** Patrick vote pour ; Martine souligne qu’elle peut avoir téléchargé sans réussir à imprimer.
- **Dépendances et limites :** Non retenue ; préserver la distinction existante dans C03/E1.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère d’examen : aucun état prêt sans attestation de préparation effective ; le téléchargement seul ne le satisfait pas.
2. Une reprise du téléchargement ne doit pas produire une nouvelle déclaration de préparation.

## F2 — Afficher une validation réussie hors connexion puis synchroniser

- **Mission :** M2.
- **Problème :** Patrick craint de bloquer sa file en cas de réseau dégradé.
- **Source :** HYPOTHÈSE de terrain ; aucun test hors connexion, aucune garantie de synchronisation observée. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** L’habitant pourrait repartir sur un succès ensuite refusé, avec conflit ou doublon différé.
- **Solution proposée :** Coche verte immédiate hors connexion, puis synchronisation automatique.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : aucune attente réseau au comptoir.
- **Effort :** XL. **Priorité :** P1 proposé, non retenu. **Confiance :** Faible sur faisabilité et bénéfice ; risque de faux succès établi par raisonnement.
- **Vote :** 1 pour / 10 contre / 1 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#f2).
- **Réserve ou argument minoritaire :** Patrick vote pour afin de préserver la file ; Martine s’abstient car elle ne saurait pas si l’action est terminée.
- **Dépendances et limites :** Rejet indépendant du risque critique ; conserver F1 et la lecture du reçu.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère d’examen : ne jamais présenter comme validé ce que le serveur n’a pas confirmé ; la proposition échoue à cette condition.
2. Un éventuel mode différé nécessiterait un cadrage distinct, des états d’attente explicites et une règle métier ; il n’est pas autorisé par ce vote.

## G2 — Remplacer systématiquement le grand scanner par la prochaine tâche

- **Mission :** M1 et M3.
- **Problème :** Nadia et Claire veulent voir la préparation immédiatement à l’ouverture.
- **Source :** HYPOTHÈSE de priorité ; O02 montre un scanner très visible et un accès Préparation plus bas. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Une tâche ressortirait mieux, mais le scanner perdrait sa priorité pendant le service.
- **Solution proposée :** Remplacer le grand scanner de l’accueil par une carte tâche ; conserver le scanner uniquement dans la navigation.
- **Bénéfice attendu (hypothèse) :** Bénéfice espéré : attirer l’attention sur la préparation.
- **Effort :** M. **Priorité :** P2. **Confiance :** Faible ; besoins opposés selon le moment.
- **Vote :** 2 pour / 8 contre / 2 abstention — **REJETÉE**. [Votes nominatifs](votes-et-arbitrages.md#g2).
- **Réserve ou argument minoritaire :** Nadia et Claire votent pour ; Accessibilité et Isabelle s’abstiennent. Le besoin d’échéance est repris par D1/F1 sans retirer le scanner.
- **Dépendances et limites :** Non retenue ; aucun changement global de navigation décidé.

**Critères d’acceptation proposés, non approuvés pour réalisation :**

1. Critère d’examen : accès au scan aussi évident pendant une animation et tâche trouvable avant celle-ci.
2. Une comparaison préparation/jour J doit démontrer l’intérêt ; le remplacement systématique n’est pas justifié par les preuves actuelles.
