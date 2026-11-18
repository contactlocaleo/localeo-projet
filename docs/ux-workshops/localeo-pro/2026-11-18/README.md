# Workshop UX Localeo Pro — archive des étapes 1 à 5

**Suite du 18 novembre 2026 :** l'utilisateur a validé B1, C1, D1, E1 et F1 pour l'implémentation E80 après cet archivage. Voir le [registre actualisé](validation/decisions.md), l'[epic E80](../../../roadmap/en-cours/epic-80-fiabilite-parcours-localeo-pro-backlog.md) et sa [vérification locale](../../../specifications/epic-80-fiabilite-parcours-localeo-pro/verification-livraison.md). Le statut ci-dessous décrit la clôture historique du workshop, avant cette réponse.

- Date locale : 18 novembre 2026 (Europe/Paris).
- URL communiquée : https://test-animations.localeo.city
- URL Pro utilisée après vérification documentaire : https://test-commercant.localeo.city
- Branche documentaire : `main`.
- Commit documentaire initial : `7164846f266cc0c073dc0c4642c569d9b8c6676c`.
- Dépôt applicatif inspecté en lecture seule : `localeo-commercant`, branche `main`, commit `333b7607b7c0e72e2a1b4133068d37d7fc7ca760`.
- Statut à l'archivage initial : **PARTIEL — ARCHIVAGE TERMINÉ, CINQ DÉCISIONS UTILISATEUR EN ATTENTE ET TESTS TERRAIN NON EXÉCUTÉS**. Cet état précède la validation et la demande d'implémentation E80 consignées en tête du présent README.
- Archivage finalisé : 18/11/2026 11:10:27 +0100 (Europe/Paris).
- Version documentaire du protocole : **LOCALEO-PRO-UX-1.0**, attribuée à l’archivage ; [provenance et versions](prompts/provenance-et-versions.md).
- Modèle connu : agent Codex, famille GPT-6 indiquée par le contexte d’exécution. Révision exacte du modèle et niveau de raisonnement : **non exposés**. Aucun identifiant précis ni niveau n’est revendiqué pour les sous-agents.

## Périmètre et preuves

Exploration réelle avec Chromium/Playwright, sur vue mobile 390 × 844 puis ordinateur 1440 × 900, le 18 novembre 2026. Le compte de test fourni a été utilisé uniquement sur les deux portails TEST. Les identifiants ne figurent dans aucun fichier ni capture du workshop. La saisie QR invalide a été rejetée côté interface ; aucun QR participant valide, aucune validation effective, notification sortante, préparation confirmée ou retrait de participation n’a été exécuté.

- [Cartographie des parcours](observations/cartographie-parcours.md)
- [Inventaire des écrans](observations/inventaire-ecrans.md)
- [Observations factuelles](observations/observations-factuelles.md)
- [Limitations](observations/limitations.md)
- [Captures avant](visuels/captures-avant/README.md)
- [Prompts archivés](prompts/README.md)

À la clôture de l’étape 1, les dossiers workshop, maquettes, validation et synthèse étaient vides. L’étape 2 a ajouté le workshop simulé ; l’étape 3 a ajouté les propositions visuelles. L’étape 4 a préparé leur décision. La réponse utilisateur est intervenue après l'archivage initial ; aucune validation terrain n'a encore été reçue.

## Résultats principaux

1. L’URL communiquée affiche le portail gestionnaire « Localeo Animation » et refuse le compte commerçant avec HTTP 401. L’URL Pro déjà documentée dans le projet accepte ce compte.
2. L’accueil Pro met le scanner en action principale, puis les notifications, animations, invitations et préparations. Sur mobile, ces parcours passent par la navigation inférieure et les liens de l’accueil.
3. La caméra n’a pas démarré dans Chromium automatisé. La saisie manuelle est disponible ; un texte invalide a produit une erreur sans transmission de QR reconnu.
4. Le compte de test possède des invitations acceptées, trois cartes classées « En cours », une animation à venir, neuf notifications Animation dont une non lue, et des parcours de préparation et de kit consultables.
5. Des écarts visibles méritent le workshop : l’accueil annonce deux animations en cours tandis que la liste en montre trois ; la liste classe au moins une animation datée du 14 au 16 novembre en cours le 18 ; le guide de préparation affiche des horodatages ISO UTC bruts malgré la convention d’affichage en heure de Paris.

Ces constats sont datés et propres au compte et à l’environnement observés. Voir les preuves et les réserves dans `observations/`.

## Vérification documentaire de l’étape 1

Seul `localeo-projet` reçoit des livrables. Aucun code applicatif, contrat, migration, générateur, commit, push ou déploiement n’est modifié. `py -3 scripts/check_guidance.py` : succès (103 guides, 1 389 liens, 0 erreur, 0 avertissement). `py -3 scripts/sync_documentation.py --check-sources` : succès (151 documents). Contrôle ciblé : 71 liens locaux, aucune cible absente ; 22 captures PNG. Aucun test applicatif exécuté.

## Étape 2 — workshop contradictoire simulé

- Exécutée le 18 novembre 2026, dans le même dossier et à partir des preuves de l’étape 1, relues intégralement avec les 22 captures.
- [Prompt complet](prompts/02-workshop.md) archivé à l’identique depuis le fichier fourni ; aucun identifiant n’y figure.
- Cinq experts et sept commerçants fictifs, 84 avis initiaux, sept ateliers, 14 orientations et 168 votes nominatifs. Chaque rôle possède une voix, y compris le facilitateur. Seuil fixe de sept voix sur douze ; les abstentions ne le réduisent pas.
- Sept orientations adoptées, sept rejetées ; aucun résultat à six voix. Cinq P1 : B1 (scan/résultat), C1 (notifications/action), D1 (cohérence et préparation), E1 (supports/dates), F1 (reprise fiable). A1/G1 restent P2. Aucun P0 produit démontré.
- Recommandation : **GO SOUS CONDITIONS**. QR valide, doublon, résultat incertain, téléphones physiques, retour différé, fichiers du kit et accessibilité restent à éprouver ; les votes ne remplacent pas ces preuves.
- Les désaccords sont conservés : Patrick privilégie la vitesse ; trois abstentions portent sur la lisibilité des statuts D1 ; deux sur les repères et répétitions G1.

Livrables :

- [Rapport exécutif](workshop/rapport-executif.md) : sept notes heuristiques, matrice des sept commerçants, cinq améliorations prioritaires, risques et conditions d’ouverture à 500 commerces.
- [Compte rendu](workshop/compte-rendu.md) : écrans, douze avis initiaux par atelier, débats et six situations terrain simulées.
- [Votes et arbitrages](workshop/votes-et-arbitrages.md) : 168 votes individuels argumentés, décomptes et décisions.
- [Backlog UX](workshop/backlog-ux.md) : sept orientations adoptées, critères, confiance, efforts et dépendances.
- [Orientations rejetées](workshop/orientations-rejetees.md) : sept alternatives et arguments minoritaires.
- [Quick wins](workshop/quick-wins.md) : quatre lots ciblés proposés, non réalisés.

Seul `localeo-projet` est modifié pour cette étape. Aucun code applicatif ni contrat n’a changé ; aucun test applicatif, entretien réel, nouveau parcours distant, maquette, commit, push ou déploiement n’a été exécuté. Le workshop Localeo Live voisin est préservé.

**Arrêt de l’étape 2 respecté.** L’instruction suivante de l’utilisateur a ensuite autorisé l’étape 3 ci-dessous.

### Contrôles de l’étape 2

- Prompt 02 identique octet par octet au fichier fourni ; SHA-256 `c496604b58d5c236cb6bbc613b9dd0393e64ef22f70259ea1abcd83c5a24dc1e`.
- Six livrables présents ; sept ateliers, douze avis par atelier (84), quatorze orientations avec douze votants uniques chacune (168), arguments présents et totaux vérifiés ; sept adoptions et sept rejets conformes au seuil.
- 218 liens locaux du dossier vérifiés, aucune cible ni ancre manquante ; sept notes heuristiques ; 22 captures avant conservées ; aucune maquette.
- `py -3 scripts/check_guidance.py` : succès, 103 guides et 1 396 liens, aucune erreur ni avertissement. `py -3 scripts/sync_documentation.py --check-sources` : succès, 151 documents.
- Dépôt commerçant toujours propre, au commit relevé à l’étape 1. Les contrôles ci-dessus valident les livrables documentaires ; aucune preuve métier ou terrain supplémentaire n’est revendiquée.

## Étape 3 — propositions visuelles avant/après

Exécutée le 18 novembre 2026, à la demande explicite de l’utilisateur, dans le même dossier. Le [prompt complet](prompts/03-maquettes.md) est archivé. Rapport exécutif, backlog, votes, observations et captures ont été relus.

**Ouvrir la [galerie interactive avant/après](visuels/comparatif-avant-apres.html)** directement dans un navigateur. Elle présente les preuves réelles, les propositions, les constats, les votes, le bénéfice hypothétique et l’effort de chaque orientation. Affichage côte à côte sur ordinateur, bascule sur mobile ; sélecteurs d’état et de format, liens vers les images complètes et le prototype responsive.

- Cinq orientations P1 uniquement : B1 (11 voix), C1 (12), D1 (9), E1 (12), F1 (12). A1/G1 P2 exclues ; aucun P0 artificiel.
- [18 états et 36 PNG APRÈS](visuels/maquettes-apres/README.md), en mobile et ordinateur : accueil, scanner, confirmation, succès, erreur, doublon, incertitude, notifications, trois états de préparation, kit/logistique, retour et session expirée.
- 22 captures AVANT réelles préservées. Chaque orientation disposait déjà d’une capture ; aucune nouvelle connexion ni action distante. Les états complémentaires sans équivalent réel sont identifiés comme scénarios de conception.
- [Revue contradictoire](visuels/revue-contradictoire.md) des cinq experts et sept commerçants fictifs, six questions par rôle. Les revues déléguées portent sur une transcription du contenu, sans inspection visuelle autonome ; les rendus ont été inspectés par l’agent principal. Aucun test utilisateur réel.
- [Arbitrages complémentaires](visuels/arbitrages-maquettes.md) : fin de période visible, issue d’une vérification impossible, action retrouvable après lecture, détails des statuts conservés. Aucun changement substantiel des orientations, donc pas de nouveau vote. Le [backlog](workshop/backlog-ux.md#références-de-conception--étape-3) référence les maquettes.
- [Contrôles de la galerie](visuels/controle-galerie/README.md) : 320, 390, 768 et 1440 px ; bascule mobile, activation clavier, côte à côte, sélecteurs et 36 variantes d’image vérifiés sans échec. Aucune erreur JavaScript ni débordement horizontal détecté.

### Limites toujours ouvertes

Les succès/doublons/incertitudes ne sont pas des captures de validations réelles. La cause de l’écart des compteurs demeure inconnue. Le PDF du kit n’est pas vérifié. Le retour différé, l’expiration réelle, la caméra physique et les aides techniques restent à éprouver. Les bénéfices de temps et de compréhension sont hypothétiques. Les votes simulés n’autorisent aucun développement.

Seul le dossier UX de `localeo-projet` est modifié. Les quatre dépôts applicatifs sont propres au contrôle final. Aucun code applicatif, contrat, migration, générateur, donnée de test, commit, push ou déploiement modifié. Les fichiers HTML/CSS/JS sont des prototypes documentaires isolés, sans API ni session. Le workshop Localeo Live voisin est préservé. `check_guidance.py` et `sync_documentation.py --check-sources` réussissent ; les liens locaux et les captures sont contrôlés séparément.

**Arrêt de l’étape 3 respecté.** L’instruction suivante de l’utilisateur a demandé de préparer le dossier de décision ci-dessous, sans valider les maquettes.

## Étape 4 — dossier de décision utilisateur

Préparé le 18 novembre 2026, dans le même répertoire. [Instruction complète archivée](prompts/04-validation.md). Les sources des étapes précédentes ont été relues ; aucune nouvelle exploration, maquette ou recette applicative n’a été réalisée.

- [Cinq fiches à décider](validation/orientations-a-decider.md), toutes P1 : B1, C1, D1, E1, F1. Chaque fiche relie mission, problème, conséquence, vote, AVANT réel, APRÈS proposé, bénéfice hypothétique, effort et dépendances.
- [Risques ouverts](validation/risques-ouverts.md), présentés séparément : preuves manquantes sur validation/reprise, périodes, kit et accessibilité ; accès et tâches ; besoins persistants derrière les sept solutions rejetées par le workshop. Aucun P0 artificiellement déclaré.
- [Registre des décisions](validation/decisions.md) : cinq lignes **VALIDÉE** le 18 novembre 2026, sans condition ajoutée par l'utilisateur. A1/G1 P2 restent hors du lot présenté.
- [Synthèse des décisions](synthese/decisions-ux.md) : 5 validées, 0 à réviser, 0 reportée, 0 refusée, 0 en attente.
- [Backlog d’implémentation potentiel](validation/backlog-implementation-potentiel.md) : cinq lots conditionnels, dépendances, preuves attendues et impacts à instruire. Aucun ticket, epic, engagement de réalisation ou changement de roadmap créé.

Les prérequis techniques proposés ne sont pas enregistrés comme des conditions déjà acceptées par l’utilisateur. Les votes simulés ne constituent aucune décision utilisateur. Une validation UX ne lance aucun développement automatiquement.

Seuls les documents du workshop Pro sont modifiés. Aucun code applicatif, contrat, donnée, commit, push ou déploiement modifié. Contrôle des liens locaux et vérifications documentaires exécutés ; ils ne valent pas recette UX ou métier.

**Décision reçue après l'étape 5 : B1, C1, D1, E1 et F1 validées pour E80.** La demande d’archivage elle-même n’avait apporté aucune décision. Le registre, la synthèse, le README et les empreintes sont actualisés à la suite de cette réponse.

## Étape 5 — archivage et rejouabilité

L’[instruction d’archivage](prompts/05-archivage.md) est conservée intégralement. Les six prompts sont présents. Le fichier 01 contenait un protocole résumé : l’instruction globale réellement appliquée a été ajoutée, et le [fichier initial](prompts/historique/01-exploration-initial.txt) est préservé. La provenance signale les textes internes dont la version exacte n’est pas disponible. Aucun historique n’est inventé.

### Bilan chiffré

| Indicateur | Valeur |
| --- | --- |
| Orientations proposées et votées | 14 |
| Orientations adoptées par simulation | 7 : A1, B1, C1, D1, E1, F1, G1 |
| Orientations rejetées par simulation | 7 ; aucune à exactement six voix |
| Votes nominatifs | 168 : douze rôles × quatorze propositions |
| P0 adoptées | 0 ; aucun P0 produit démontré |
| P1 adoptées / soumises à décision | 5 : B1, C1, D1, E1, F1 |
| P0/P1 parmi toutes les propositions | 0 P0 et 6 P1, dont F2 rejetée ; ne pas confondre avec les 5 P1 retenues |
| P2 adoptées | 2 : A1/G1, hors lot de décision P1 |
| P3 adoptées | 0 ; A2/C2 proposées P3 puis rejetées |
| Validations utilisateur à l'archivage initial | 0 validée, 0 refusée, 0 à réviser, 0 reportée ; 5 EN ATTENTE. Suite du 18 novembre : 5 VALIDÉES pour E80. |
| Visuels | 22 captures AVANT réelles ; 18 états APRÈS, 36 PNG ; 4 captures de contrôle de galerie |

### Parcours réellement vérifiés et limites

Connexion d’un compte déjà actif au portail Pro, accueil/navigation, listes/détails d’animations, invitations acceptées, consultation des préparations et notifications internes, accès visuel au kit et au guide, rejet local d’un QR invalide et rechargement immédiat authentifié ont été observés. Mobile émulé 390 × 844 puis ordinateur 1440 × 900. L’URL fournie initialement était le portail Animation et a renvoyé 401 ; l’URL Pro documentée a ensuite été utilisée.

Première activation de compte, validation QR réelle autorisée, confirmation/doublon/reçu, caméra physique, réception push/email, téléchargement/impression du kit, expiration réelle, retour après plusieurs jours et tests avec commerçants **non exécutés**. Les maquettes, votes et contrôles documentaires ne prouvent pas ces comportements. L’écart des compteurs et la convention de fin de période restent à diagnostiquer. Les [risques ouverts](validation/risques-ouverts.md) conservent les besoins sous-jacents aux solutions rejetées.

### Livrables de clôture

- [Roadmap UX](synthese/roadmap-ux.md) : aucun lot P0/P1 validé avant lancement ; P2 conditionnelles après retours ; aucune P3 adoptée à planifier.
- [Plan de tests commerçants](synthese/plan-tests-commercants.md) : huit scénarios, cinq à sept personnes à recruter dont au moins deux peu familières du numérique ; tâches, consignes neutres, réussite, observations et retour à 7–14 jours.
- [Comparaison historique](synthese/comparaison-precedent.md) : aucun précédent Localeo Pro ; le workshop Localeo Live voisin n’est pas utilisé comme référence Pro. Aucune correction ni évolution de note revendiquée.
- [Contrôle d’archivage et inventaire complet](synthese/controle-archivage.md) : tous les types de livrables demandés, anomalies et limites de rejouabilité.
- [Résultats d’intégrité](synthese/controle-integrite.json), [contrôle de galerie](synthese/controle-galerie-archivage.json), [manifeste SHA-256 courant](synthese/manifest-sha256.json) et [version à l'archivage initial](synthese/manifest-sha256-archivage-initial.json).
- **[Prompt autonome pour relancer le workshop](prompts/RELANCER-WORKSHOP.md)** : nouveau dossier daté, exploration réelle, simulation, votes, priorisation, visuels, comparaison et attente de validation ; aucun identifiant embarqué.

Les sections précédentes référencent les observations, cartographies, captures, rapports, votes, backlog, rejets, quick wins, maquettes, décisions et synthèse de décision. Les **cinq décisions utilisateur sont maintenant enregistrées** ; les preuves terrain restent manquantes.

### Préservation et contrôles finaux

Les 100 fichiers des autres workshops présents sont inchangés par comparaison SHA-256. Aucun précédent Pro trouvé ; seuls les fichiers de cette exécution ont été complétés. Les quatre dépôts applicatifs ont gardé leur HEAD et un statut propre, vérifiés avant/après l’archivage. Aucun code, contrat, migration, donnée de test, commit, push ou déploiement modifié. Les modèles précis et niveaux de raisonnement non disponibles restent signalés, sans estimation.

Les images ont été vérifiées puis décodées ; les liens relatifs, votes et prompts contrôlés. La galerie a été recontrôlée dans Chromium sans erreur ni requête distante. Les vérificateurs documentaires réussissent. Le manifeste couvre tous les fichiers de l’exécution sauf lui-même ; il permet de contrôler une copie future, sans constituer une signature externe.

**À la fin de l'archivage initial : workshop PARTIEL.** La suite du 18 novembre a apporté les cinq décisions et la demande d'implémentation E80. Les tests réels restent à obtenir ; voir le [bilan E80](../../../specifications/epic-80-fiabilite-parcours-localeo-pro/verification-livraison.md).
