# Backlog UX proposé — Localeo Pro

Étape 2, 18 novembre 2026. **Simulation : sept orientations adoptées par des rôles fictifs ; aucune validation utilisateur réelle ni autorisation de codage.** Seuil fixe : sept voix sur douze. Les bénéfices sont des hypothèses. Efforts S/M/L/XL relatifs, sans estimation de calendrier : S contenu ciblé, M parcours/composant, L plusieurs états ou couches, XL mécanisme nouveau. Ces efforts comprennent l’investigation nécessaire et seront affinés après recette.

Aucun P0 produit n’est établi. Les cinq P1 sont B1, C1, D1, E1 et F1 ; A1/G1 restent P2. Les [conditions de fonctionnement](rapport-executif.md#conditions-avant-ouverture-a-500-commercants) ne disparaissent pas avec un vote. B1/F1 commencent par une vérification de l’existant, pas par l’hypothèse d’une fonction absente. Les sept propositions non retenues sont décrites avec leurs critères dans [orientations rejetées](orientations-rejetees.md).

| ID | Orientation adoptée | Priorité | Effort | Pour / contre / abstention |
| --- | --- | --- | --- | --- |
| A1 | Identifier l’accès Pro et expliquer son rôle en une phrase | P2 | S | 11 / 0 / 1 |
| B1 | Rendre le scan et son résultat compréhensibles, éprouver les garanties existantes | P1 | M | 11 / 1 / 0 |
| C1 | Distinguer information reçue et action attendue | P1 | M | 12 / 0 / 0 |
| D1 | Rendre cohérents dates, états et prochaine action de préparation | P1 | L | 9 / 0 / 3 |
| E1 | Présenter les supports par usage et des dates lisibles | P1 | M | 12 / 0 / 0 |
| F1 | Retrouver le contexte fiable après interruption ou absence | P1 | L | 12 / 0 / 0 |
| G1 | Alléger les répétitions en gardant les repères et le détail accessible | P2 | M | 10 / 0 / 2 |

## A1 — Identifier l’accès Pro et expliquer son rôle en une phrase

- **Mission :** M1 — première impression.
- **Problème :** L’adresse fournie pour l’exploration mène au portail gestionnaire ; la connexion Pro dit surtout comment se connecter.
- **Source :** O01–O02, [connexion Pro](../visuels/captures-avant/02-connexion-pro-mobile.png) et [refus du portail fourni](../visuels/captures-avant/01-portail-fourni-refus-mobile.png). Aucun lien erroné du produit n’a été établi. Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Un débutant pourrait attribuer le refus à son mot de passe et demander une assistance.
- **Solution proposée :** Vérifier les liens réellement diffusés ; identifier clairement l’espace commerçant et ajouter, si utile, une phrase sur la participation aux animations avec une aide courte à la demande.
- **Bénéfice attendu (hypothèse) :** Rejoindre le bon espace et comprendre sa destination sans détour imposé.
- **Effort :** S. **Priorité :** P2. **Confiance :** Moyenne sur la clarté à améliorer ; faible sur l’existence d’un défaut de diffusion produit.
- **Vote :** 11 pour / 0 contre / 1 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#a1).
- **Réserve ou argument minoritaire :** Hugo s’abstient : vérifier les accès existants avant d’ajouter du texte.
- **Dépendances et limites :** Vérification des supports par produit/exploitation ; pas de changement d’authentification.

**Critères d’acceptation proposés :**

1. Les supports de test utilisés pour la recette conduisent au portail Pro de la même cible ; les autres portails gardent leur identité.
2. Une personne débutante peut expliquer l’utilité de Pro et trouver la connexion à partir du support fourni.
3. L’aide est facultative, nommée et accessible au clavier ; le scanner reste directement accessible après connexion.

## B1 — Rendre le scan et son résultat compréhensibles, éprouver les garanties existantes

- **Mission :** M2 — validation des participations.
- **Problème :** L’erreur observée parle de « pack » sans geste de reprise précis ; succès, doublon et incertitude n’ont pas été vus sur téléphone.
- **Source :** O04, C02 et [erreur locale](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png) ; [limites de recette](../observations/limitations.md). Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Le commerçant peut ne pas savoir quel QR demander ou si le passage a réellement été enregistré.
- **Solution proposée :** Corriger le message hors contexte ; expliquer quel QR présenter et le prochain geste possible. Conserver la confirmation distincte, le reçu et les protections contre les renvois. Recetter sur téléphone puis modifier seulement les écarts établis.
- **Bénéfice attendu (hypothèse) :** Décider devant l’habitant avec un résultat fiable et lisible.
- **Effort :** M. **Priorité :** P1. **Confiance :** Élevée sur le libellé ; moyenne sur l’utilité ; fonctionnement nominal encore non prouvé.
- **Vote :** 11 pour / 1 contre / 0 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#b1).
- **Réserve ou argument minoritaire :** Patrick vote contre le maintien de la confirmation à chaque client ; la recette doit mesurer son coût sans retirer la garantie.
- **Dépendances et limites :** Recette avec QR dédiés et accès de test ; domaine backend propriétaire de la validation, du doublon et du reçu. F1 couvre la reprise de contexte.

**Critères d’acceptation proposés :**

1. QR invalide : message sans « pack » dans le parcours Animation, sans faux succès, avec action de reprise compréhensible et annoncée aux aides techniques.
2. QR de test autorisé : animation et étape compréhensibles avant confirmation ; un seul effet après double clic ou retour du même QR.
3. Succès, déjà validé, refus et résultat incertain sont distingués ; aucune réussite n’est annoncée sans confirmation serveur.
4. Perte de réponse : vérifier le reçu avant tout renvoi ; caméra autorisée/refusée et repli manuel testés sur téléphones physiques.
5. Mesurer temps, erreurs et assistance en caisse ; aucune promesse de durée avant cette mesure.

## C1 — Distinguer information reçue et action attendue

- **Mission :** M3 — notifications et préparation.
- **Problème :** La boîte commence par une section PIN vide ; la carte d’accueil annonce une notification non lue, sans identifier la tâche dans ce résumé.
- **Source :** O05 et [boîte de réception](../visuels/captures-avant/09-notifications-generales-mobile.png), [accueil](../visuels/captures-avant/03-accueil-pro-mobile.png). Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Un commerçant intermittent peut confondre lecture et accomplissement, ou perdre du temps avant d’atteindre les messages Animation.
- **Solution proposée :** Donner la priorité aux notifications Animation pour ce profil, replier la section PIN vide sans retirer son accès. Exposer animation, nature information/action, échéance connue et lien direct vers l’action autorisée.
- **Bénéfice attendu (hypothèse) :** Comprendre ce qui mérite une intervention et y accéder sans rechercher le contexte.
- **Effort :** M. **Priorité :** P1. **Confiance :** Élevée sur l’ordre visible ; moyenne sur l’impact et sur les données d’action disponibles.
- **Vote :** 12 pour / 0 contre / 0 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#c1).
- **Réserve ou argument minoritaire :** Unanimité sur ce périmètre limité, sans soutien au rappel quotidien C2.
- **Dépendances et limites :** Vérifier les informations du contrat avant enrichissement ; conserver les préférences de notifications et les liens existants.

**Critères d’acceptation proposés :**

1. Un message purement informatif n’est pas présenté comme une obligation ; une action n’apparaît que si son état est fourni et toujours valable.
2. Marquer lu ne termine ni invitation ni préparation ; une tâche encore ouverte reste retrouvable après lecture.
3. La section PIN vide peut être repliée et retrouvée ; les fonctions utiles des autres profils restent disponibles.
4. Un lien ouvre la bonne animation/demande/préparation après contrôle de session ; aucun push ou email n’est supposé reçu.
5. Lecture, état non lu et actions restent compréhensibles sans couleur seule et au clavier.

## D1 — Rendre cohérents dates, états et prochaine action de préparation

- **Mission :** M3 et M4 — préparation et logistique.
- **Problème :** Deux animations en cours à l’accueil contre trois dans la liste ; une carte datée avant le test reste classée en cours. Plusieurs états de préparation existent.
- **Source :** O03, O06–O07, C04, [liste](../visuels/captures-avant/05-animations-mobile.png), [préparation Vitrines](../visuels/captures-avant/16-preparation-vitrines-mobile.png). Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Doute sur la bonne période et sur ce qui dépend encore du commerce ou de l’organisateur.
- **Solution proposée :** Diagnostiquer la règle et le périmètre des compteurs, puis afficher des états cohérents ou des différences explicitement justifiées. Mettre en avant le prochain geste, son responsable et sa date connue, en conservant les distinctions métier derrière une présentation progressive.
- **Bénéfice attendu (hypothèse) :** Savoir quoi préparer et quand agir sans solliciter l’organisateur pour interpréter l’état.
- **Effort :** L. **Priorité :** P1. **Confiance :** Élevée sur l’écart visuel ; moyenne sur son impact ; faible sur sa cause.
- **Vote :** 9 pour / 0 contre / 3 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#d1).
- **Réserve ou argument minoritaire :** UX, Accessibilité et Martine s’abstiennent : cinq statuts pourraient surcharger. La présentation devra faire l’objet d’un test de compréhension.
- **Dépendances et limites :** Diagnostic producteur/consommateur avant correction ; toute règle métier appartient au backend. Aucun nouveau statut décidé ici.

**Critères d’acceptation proposés :**

1. Pour un même compte, périmètre et instant, accueil et liste donnent un résultat cohérent ; une différence de périmètre est nommée.
2. Une période passée n’est pas présentée comme active sans explication fondée sur la règle métier ; transitions de dates vérifiées en heure de Paris.
3. Sur un cas incomplet, un cas en attente d’organisateur et un cas prêt, l’écran indique qui doit agir et le prochain geste autorisé.
4. Acceptation, approbation, installation, déclaration prêt et contrôle restent distincts ; l’écran n’affiche pas obligatoirement cinq badges simultanés.
5. Aucune échéance n’est inventée ; lorsque le suivi est arrêté, les consignes restent accessibles sans fausse action à terminer.

## E1 — Présenter les supports par usage et des dates lisibles

- **Mission :** M4 — kit et logistique.
- **Problème :** Le contenu du fichier n’a pas été vérifié ; le guide affiche des dates ISO UTC. Les opérations télécharger, imprimer, afficher et préparer l’équipe sont distinctes.
- **Source :** O08, C03 et [guide ouvert](../visuels/captures-avant/21-guide-preparation-mobile.png) ; [préparation Tombola](../visuels/captures-avant/17-preparation-tombola-mobile.png). Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Risque de mauvaise lecture des dates ou de confusion entre le fichier obtenu et les gestes à effectuer en boutique.
- **Solution proposée :** Vérifier le kit réel puis annoncer les supports effectivement disponibles et leur usage. Rendre les dates locales lisibles. Relier les consignes d’impression, d’affichage et d’équipe aux bons documents et expliciter le rôle des QR.
- **Bénéfice attendu (hypothèse) :** Préparer et transmettre les bons supports sans interpréter des noms techniques.
- **Effort :** M. **Priorité :** P1. **Confiance :** Élevée sur les dates brutes ; moyenne sur la confusion d’usage ; contenu PDF encore non vérifié.
- **Vote :** 12 pour / 0 contre / 0 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#e1).
- **Réserve ou argument minoritaire :** Unanimité conditionnée à l’examen des fichiers ; aucun accord pour E2.
- **Dépendances et limites :** Source de guide/kit et consommateurs à examiner ; aucune nouvelle collecte de preuve d’impression décidée.

**Critères d’acceptation proposés :**

1. Les supports annoncés correspondent au kit téléchargé de test ; aucun document ou QR absent n’est promis.
2. Les instants sont affichés en heure de Paris, les dates civiles gardent leur jour ; aucune chaîne ISO UTC brute dans le guide destiné au commerçant.
3. Le QR d’inscription du flyer est distingué du QR participant à scanner pour valider ; cette différence est testée avec un commerçant.
4. Télécharger n’atteste ni impression, ni installation, ni préparation terminée ; « Je suis prêt » reste une décision explicite lorsqu’elle est autorisée.
5. Le fichier est ouvert et imprimé lors de la recette ; lisibilité, QR et consignes sont vérifiés avant diffusion.

## F1 — Retrouver le contexte fiable après interruption ou absence

- **Mission :** M1 à M4 — continuité d’usage.
- **Problème :** Seul un rechargement immédiat est observé ; interruption, expiration et retour après semaines restent non testés.
- **Source :** O09, C05, [rechargement](../visuels/captures-avant/20-retour-rechargement-mobile.png) et [limitations](../observations/limitations.md). Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Risque hypothétique de recommencer une action ou de manquer une échéance après avoir perdu ses repères.
- **Solution proposée :** Éprouver les reprises existantes ; après reconnexion, relire l’état autorisé et redonner le contexte de l’animation, la prochaine échéance connue et l’étape restante. Compléter uniquement les manques démontrés.
- **Bénéfice attendu (hypothèse) :** Reprendre sans supposer qu’une validation ou préparation a été enregistrée.
- **Effort :** L. **Priorité :** P1. **Confiance :** Moyenne sur le besoin terrain ; faible sur l’existence d’un manque applicatif ; recette obligatoire avant extension.
- **Vote :** 12 pour / 0 contre / 0 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#f1).
- **Réserve ou argument minoritaire :** Unanimité sur la continuité fiable ; Patrick préfère aussi F2, rejeté pour son faux succès.
- **Dépendances et limites :** B1 couvre le résultat de transaction ; F1 couvre reprise/navigation/session. Réutiliser les capacités existantes, sans cache de validation hors connexion.

**Critères d’acceptation proposés :**

1. Après interruption avant confirmation, aucune validation n’est effectuée ; la reprise expose un contexte relu ou invite clairement à rescanner.
2. Après réponse perdue, le reçu serveur prévaut conformément à B1 ; aucun renvoi automatique ni coche locale de succès.
3. Après expiration puis reconnexion, les droits et états actuels sont relus ; aucun jeton ou QR n’est conservé dans l’URL ou les messages.
4. Après plusieurs semaines, l’animation pertinente, sa période et les actions encore valables sont retrouvables ; la lecture d’une notification ne les efface pas.
5. Recette avec file, interruption et mauvaise connexion ; l’absence d’état fiable est expliquée avec une voie de retour et un focus cohérent.

## G1 — Alléger les répétitions en gardant les repères et le détail accessible

- **Mission :** M1, M3 et M4.
- **Problème :** Le détail Vitrines expose toutes les étapes alors que la préparation guidée montre l’étape courante ; des blocs similaires sont répétés.
- **Source :** O07, C04, [détail Vitrines](../visuels/captures-avant/13-detail-vitrines-mobile.png) et [parcours guidé](../visuels/captures-avant/16-preparation-vitrines-mobile.png). Les identifiants O/C renvoient aux [observations communes](../observations/observations-factuelles.md).
- **Conséquence :** Effort de lecture hypothétique pour distinguer le résumé utile du dossier complet.
- **Solution proposée :** Comparer une présentation plus courte du détail, centrée sur mission, état et accès préparation/kit, en gardant l’historique et les consignes complètes atteignables. Maintenir les destinations actuelles.
- **Bénéfice attendu (hypothèse) :** Moins de relecture avec des repères stables pour l’usage intermittent.
- **Effort :** M. **Priorité :** P2. **Confiance :** Moyenne sur la répétition ; faible sur le gain avant comparaison.
- **Vote :** 10 pour / 0 contre / 2 abstention — **ADOPTÉE**. [Votes nominatifs](votes-et-arbitrages.md#g1).
- **Réserve ou argument minoritaire :** Opérations et Isabelle s’abstiennent : des répétitions peuvent éviter des allers-retours ou servir de repères.
- **Dépendances et limites :** Conserver la navigation et ne pas réécrire le parcours déjà guidé ; aucune maquette produite à cette étape.

**Critères d’acceptation proposés :**

1. Mission, période, kit et prochaine action restent trouvables depuis chaque entrée pertinente.
2. Les liens existants continuent d’ouvrir la bonne participation et les droits restent contrôlés.
3. Comparaison sur tâches avec commerçants avant suppression d’informations : aucun contenu nécessaire perdu, aucune hausse des erreurs.
4. Les détails complets et leur titre restent explicitement accessibles ; le parcours guidé conserve ses étapes et son état.

## Références de conception — étape 3

18 novembre 2026 : uniquement les cinq P1 adoptées. Les propositions restent à valider ; les votes et efforts ci-dessus sont inchangés. Aucun critère métier n’est déclaré satisfait par une maquette. [Galerie complète](../visuels/comparatif-avant-apres.html), [inventaire des 36 rendus](../visuels/maquettes-apres/README.md), [revue simulée](../visuels/revue-contradictoire.md), [arbitrages et limites](../visuels/arbitrages-maquettes.md).

| Orientation | Comparatif | États proposés | Dépendance conservée |
| --- | --- | --- | --- |
| B1 | [Avant/après B1](../visuels/comparatif-avant-apres.html#B1) | Scan, rejet local, confirmation, succès, doublon, refus, réponse perdue, vérification impossible | QR autorisé, reçu et cas réseau à éprouver ; Patrick maintient sa réserve de rapidité. |
| C1 | [Avant/après C1](../visuels/comparatif-avant-apres.html#C1) | Information reçue ; action encore attendue après lecture | État d’action fiable et courant ; aucune obligation dérivée du non-lu. |
| D1 | [Avant/après D1](../visuels/comparatif-avant-apres.html#D1) | Accueil ; incomplet ; attente organisateur ; prêt | Compteurs illustratifs ; diagnostic du 2/3 toujours requis. |
| E1 | [Avant/après E1](../visuels/comparatif-avant-apres.html#E1) | Kit, flyer, consignes, rôles des QR et fin de période visible | Fichier et impression non vérifiés ; convention de période à confirmer. |
| F1 | [Avant/après F1](../visuels/comparatif-avant-apres.html#F1) | Retour, expiration, interruption avant confirmation | Absence prolongée et reprise réelle non testées ; aucun rejeu automatique. |

A1 et G1 restent P2, sans maquette à cette étape. Aucun changement substantiel retenu : pas de nouveau vote. Les préférences de revue ne sont ni un scrutin supplémentaire ni une autorisation d’implémentation.

## Périmètre et impacts à examiner après validation

Ces propositions appartiennent au dossier UX, sans nouvelle roadmap concurrente. Toute suite devra être rapprochée des spécifications canoniques et des capacités déjà implémentées. Pro est le consommateur concerné ; backend et générateur de documents pourraient être concernés par D1/E1 seulement après diagnostic. B1/F1 ne déplacent aucune règle métier dans l’interface. Aucun changement de contrat, migration ou jeu de démonstration n’est décidé par ce workshop. Les guides commerçant et supports de diffusion devront refléter les libellés finalement retenus. Le générateur de démonstration n’a pas été exécuté ni modifié.
