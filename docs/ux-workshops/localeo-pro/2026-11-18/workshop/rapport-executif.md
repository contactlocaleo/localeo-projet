# Rapport exécutif — workshop UX Localeo Pro

18 novembre 2026 — cinq experts et sept commerçants **fictifs**. Ce rapport est une analyse heuristique et une simulation contradictoire fondée sur l’étape 1. Aucun entretien réel, aucune mesure de temps ou d’adoption, aucun nouvel essai de validation n’a été réalisé.

**Recommandation : GO SOUS CONDITIONS.** Le socle permet de trouver scanner, animations, préparations et consignes. L’ouverture à 500 commerçants ne peut pas être considérée comme validée tant que les scénarios QR, les reprises, les documents et les usages accessibles n’ont pas été éprouvés. Cette conclusion autorise une suite de conception et de recette à proposer ; elle ne constitue pas une décision de déploiement.

## Ce que les preuves permettent de conclure

Les [observations communes](../observations/observations-factuelles.md), [parcours](../observations/cartographie-parcours.md), [inventaire](../observations/inventaire-ecrans.md), [limitations](../observations/limitations.md) et 22 [captures](../visuels/captures-avant/README.md) constituent la référence. **OBSERVÉ** : accueil à scanner prioritaire, boîte de notifications, préparations, guide et rejet d’une saisie QR invalide. **DÉDUIT du code** : confirmation distincte, doublon, reçu de validation incertaine, WebPush et rafraîchissement au retour de visibilité. **HYPOTHÈSE** : leur compréhension et leur efficacité au comptoir ou après plusieurs semaines.

La mauvaise adresse donnée à l’exploration ouvre un autre portail ; la connexion Pro fonctionne à l’adresse documentée. Cela impose de vérifier le support d’accès de la future campagne, mais ne démontre pas des liens erronés dans le produit. La caméra indisponible en Chromium automatisé ne prouve pas un défaut sur téléphone. Les barres fixes au milieu de captures longues ne prouvent pas un recouvrement en usage. L’URL directe /animations/notifications n’est pas le lien de navigation normal et n’est pas retenue comme défaut du parcours Notifications.

## Notes heuristiques sur 10

Appréciations de la séance simulée : 1 = très difficile sur les éléments visibles, 5 = expérience partiellement rassurante avec friction ou inconnues importantes, 10 = parcours clair et étayé de bout en bout. Ce ne sont ni des notes données par de vrais commerçants, ni des taux de réussite, ni des mesures de conformité. La confiance est séparée de la note ; une preuve manquante ne signifie pas une panne.

| Dimension | Note | Justification et preuve | Confiance |
| --- | ---: | --- | --- |
| Première impression | 6/10 | Connexion explicite et scanner visible ; rôle de préparation moins immédiat et point d’entrée fourni ambigu. [Connexion](../visuels/captures-avant/02-connexion-pro-mobile.png), [accueil](../visuels/captures-avant/03-accueil-pro-mobile.png), O01/O02. Compte déjà actif, pas de première activation. | Moyenne |
| Navigation | 7/10 | Quatre entrées mobiles stables, menu latéral ordinateur, liens de préparation. Détails longs et plusieurs entrées vers la même participation ; coût de recherche non mesuré. [Mobile](../visuels/captures-avant/05-animations-mobile.png), [ordinateur](../visuels/captures-avant/10-accueil-pro-desktop.png). | Moyenne |
| Validation des participations | 4/10, provisoire | Accès et repli manuel présents ; erreur « pack » peu aidante. Succès/doublon/incertitude non éprouvés sur téléphone : score prudent du parcours documenté, pas preuve d’échec nominal. [Erreur](../visuels/captures-avant/19-scanner-erreur-locale-mobile.png), C02 et limitations. | Faible |
| Notifications | 5/10 | Boîte, non-lu et liens utiles ; PIN vide en premier, contenu à interpréter pour savoir ce qui attend une action. Aucun push/email reçu ou moment de réception vérifié. [Boîte](../visuels/captures-avant/09-notifications-generales-mobile.png), O05/C06. | Moyenne sur boîte, faible sur réception |
| Préparation des animations | 7/10 | Mission, étapes guidées et état prêt sont visibles ; compteurs divergents et état incomplet non testé. [Vitrines](../visuels/captures-avant/16-preparation-vitrines-mobile.png), [Tombola](../visuels/captures-avant/17-preparation-tombola-mobile.png), O03/O06/O07. | Moyenne |
| Kit et logistique | 6/10 | Bouton et guide accessibles, consignes d’impression et distinction des QR présentes ; dates UTC brutes, fichiers et impression non vérifiés. [Guide](../visuels/captures-avant/21-guide-preparation-mobile.png), O08/C03. | Moyenne sur accès, faible sur fichiers |
| Accessibilité mobile | 6/10, provisoire | Libellés textuels, sections et alternatives visibles. Absence de mesure des contrastes/cibles, de tests au lecteur d’écran, clavier, zoom ou téléphone physique ; aucune conformité revendiquée. [Scanner](../visuels/captures-avant/04-scanner-mobile.png), [préparation](../visuels/captures-avant/16-preparation-vitrines-mobile.png). | Faible |

## Matrice commerçants × missions prioritaires

Chaque cellule exprime une **hypothèse issue du persona**, pas une réussite ou un échec observé. Les positions détaillées avant débat figurent dans le [compte rendu](compte-rendu.md).

| Persona | Comprendre et se repérer | Valider une participation | Notifications et préparation | Kit et logistique |
| --- | --- | --- | --- | --- |
| Martine | Besoin du bon accès et d’un rôle expliqué ; commence par le gros scanner. | Besoin du QR à demander et d’une confirmation claire ; repli manuel potentiellement difficile. | Risque d’hésiter entre messages ; souhaite un geste simple pour demain. | Veut savoir quoi imprimer ; télécharger ne prouve pas qu’elle a pu imprimer. |
| Patrick | Scanner immédiat pendant le service ; peu de défilement souhaité. | Confirmation jugée coûteuse ; interruption et cadence prioritaires à mesurer. | Veut l’action restante sans relire les messages. | Préfère tout imprimer avant la file ; demande de rapidité à concilier avec état fiable. |
| Nadia | Cherche les animations à venir ; doute face aux compteurs divergents. | Confirmation contextualisée rassurante. | Veut anticiper même un message déjà lu et distinguer préparation/acceptation. | Vérifie affiches et QR avant la date, reprend entre rendez-vous. |
| Julien | Accès scanner et cohérence des compteurs attendus. | Exige distinction succès/doublon/incertitude pendant le service. | Veut des alertes choisies et l’heure d’ouverture connue. | Attend un contenu vérifiable et des QR identifiés. |
| Claire | Cherche la prochaine animation avant de scanner. | Message « pack » susceptible de la détourner du bon QR. | Veut distinguer information et demande, avec destination directe. | Attend support, emplacement et date lisibles. |
| Hugo | Conserve navigation existante, corrige cohérence avant refonte. | Distingue reconnaissance et validation, demande preuve sur téléphone. | Garde les liens utiles, replie le bloc vide. | Veut la liste réelle des fichiers et le rôle des QR. |
| Isabelle | Après absence, retrouve animation et changements pertinents. | Besoin d’un rappel court et d’un résultat qui signifie terminé. | Une demande lue peut rester ouverte ; besoin de prochaine échéance. | Conserve des repères stables et transmet le guide à une collègue. |

## Décisions du vote simulé

Douze voix par orientation, seuil fixe de sept : **7 adoptées, 7 rejetées, 168 votes nominatifs**. Aucun résultat à six voix ; les abstentions ne baissent pas le seuil. Le facilitateur n’a pas de voix supplémentaire. [Registre complet et arguments](votes-et-arbitrages.md).

| ID | Orientation adoptée | Priorité | Pour / contre / abstention |
| --- | --- | --- | --- |
| A1 | Accès Pro et rôle expliqués, aide facultative | P2 | 11 / 0 / 1 |
| B1 | Scan, erreurs et résultats explicites, garanties éprouvées | P1 | 11 / 1 / 0 |
| C1 | Informations et actions attendues distinguées | P1 | 12 / 0 / 0 |
| D1 | Dates, compteurs et prochaine action cohérents | P1 | 9 / 0 / 3 |
| E1 | Supports par usage et dates lisibles | P1 | 12 / 0 / 0 |
| F1 | Reprise de contexte fiable après interruption/absence | P1 | 12 / 0 / 0 |
| G1 | Alléger les répétitions sous contrôle de compréhension | P2 | 10 / 0 / 2 |

[Backlog détaillé, efforts et critères](backlog-ux.md). Les alternatives [rejetées](orientations-rejetees.md) incluent tutoriel obligatoire, auto-validation, relance push quotidienne, fusion des états, état prêt au téléchargement, succès hors connexion et remplacement systématique du scanner. Leurs objectifs utiles restent discutés ; leur rejet n’efface pas les arguments minoritaires.

D1 garde trois abstentions : Martine et deux experts craignent la multiplication des mots de statut. G1 garde deux abstentions sur les repères et les allers-retours. Patrick refuse la confirmation de B1 et soutient plusieurs raccourcis ; sa contrainte de file reste à mesurer, mais n’autorise pas un faux succès.

## Cinq améliorations prioritaires pour 500 commerçants

1. **B1 — Fiabiliser la compréhension du scan.** Corriger l’erreur hors contexte et vérifier sur téléphone les états reconnu, à confirmer, validé, déjà validé et incertain. Il s’agit en partie d’éprouver des fonctions déjà présentes dans le code.
2. **D1 — Dire quoi faire, pour quelle animation et à quelle date.** Diagnostiquer l’écart des compteurs, conserver les responsabilités métier et montrer le prochain geste utile sans imposer cinq badges simultanés.
3. **E1 — Rendre les supports utilisables en boutique.** Dates locales lisibles, contenu réellement vérifié, gestes imprimer/afficher/partager et QR d’inscription distinct du QR à scanner.
4. **C1 — Faire émerger les actions attendues des messages.** Préserver les liens directs et séparer lecture du message et achèvement de la tâche ; ne pas dépendre d’une réception push supposée.
5. **F1 — Permettre la reprise sans décision ambiguë.** Reconnecter au bon contexte, relire l’état autorisé et retrouver échéance/étape restante après interruption ou absence, sans rejouer automatiquement une validation.

Ces cinq P1 couvrent des risques distincts ; elles ne doivent pas donner lieu à cinq refontes. B1/F1 partagent la recette de l’incertitude, avec B1 responsable du résultat et F1 de la continuité de contexte. A1/G1 restent des P2 ciblés. Aucun P0 produit n’est démontré par cette exploration ; un défaut essentiel trouvé pendant la recette serait reclassé indépendamment du vote.

<a id="conditions-avant-ouverture-a-500-commercants"></a>

## Conditions avant ouverture à 500 commerçants

Toutes restent **à prouver** au terme de cette étape. Une bonne note ou un vote ne les clôture pas.

| Condition / risque indépendant des votes | Preuve attendue avant extension | Responsable à mobiliser | Lien |
| --- | --- | --- | --- |
| Entrée dans le bon espace | Support réel de diffusion testé avec compte commerçant et URL de la cible ; aucune confusion avec gestionnaire. Le mauvais lien de l’audit est corrigé dans les consignes de recette. | Produit/exploitation | A1, O01 |
| Validation essentielle et doublons | Téléphones physiques, QR dédiés, succès/refus/doublon/double clic et perte de réponse ; résultat sûr, aucun effet métier involontaire. | Pro + backend + opérations | B1 |
| Reprise et réseau dégradé | Avant/après envoi, expiration, reconnexion et retour différé ; reçu relu, pas de renvoi aveugle ni réussite locale. | Pro + backend | B1/F1 |
| Cohérence de la préparation | Cause de l’écart des compteurs identifiée ; cas incomplet/prêt/attente organisateur et période testés, avec responsabilités compréhensibles. | Produit + backend + Pro | D1 |
| Kit réellement exploitable | Téléchargement autorisé du kit de test, ouverture et impression, QR et dates contrôlés, consignes transmissibles à l’équipe. | Opérations + producteur des documents | E1 |
| Accessibilité des tâches essentielles | Clavier, focus, agrandissement, lecteur d’écran, messages d’erreur/résultat, tailles des cibles et contraste sur le parcours réel ; traiter tout blocage trouvé. | Pro + accessibilité | B1/C1/D1/F1 |
| Compréhension des commerçants | Tâches observées auprès de profils variés, dont faible aisance et usage intermittent ; consigner erreurs, aide et ambiguïtés, corriger les erreurs critiques avant extension. | Recherche + opérations | Tous |

La non-réception de push/email n’est pas une panne constatée. Si la campagne promet ces canaux, leur réception et leurs liens doivent être éprouvés séparément ; sinon la boîte interne doit rester suffisante pour retrouver les informations. La fonction de kit peut déclencher une préparation serveur : vérifier ses effets en environnement autorisé, sans la confondre avec la déclaration « prêt ».

## Points forts à préserver

- Scanner saillant et accès mobile stable, plutôt qu’un changement systématique de navigation.
- Missions, étapes guidées et distinction entre ce que fait le commerce et ce que valide l’organisateur.
- Guide dépliable et accès au kit depuis les écrans pertinents.
- Boîte interne et liens vers animation/demande ; historique utile aux usages intermittents.
- Garanties de confirmation, reçu et état incertain identifiées dans le code, sous réserve de leur recette.

## À valider avec de vrais commerçants

Recruter des profils correspondant aux sept situations, sans prétendre qu’un petit échantillon représente 500 commerces. Observer les tâches, sans leur montrer les réponses attendues : rejoindre Pro depuis une invitation ; préparer une animation demain ; expliquer la différence des QR ; scanner un participant de test ; reprendre après interruption ; retrouver une tâche déjà lue et un support après absence. Mesurer temps et assistance séparément de la réussite ; demander à la personne d’expliquer l’état final. Aucun seuil de durée n’est fixé par les réactions simulées.

Vérifier en particulier le coût de confirmation pour Patrick, le besoin d’aide de Martine, la hiérarchie des statuts soulevée par trois abstentions sur D1, les repères d’Isabelle et les répétitions défendues par Opérations. Le moment réel des notifications et la préparation sans appel à l’organisateur doivent être observés, pas présumés.

Les [quick wins](quick-wins.md) sont des lots possibles, non réalisés. Le workshop s’arrête avant l’étape 3 ; aucune maquette, modification applicative ou validation terrain n’est produite.
