# Préparation de la revue des maquettes par cinq experts simulés

**Statut : protocole préparé le 19 novembre 2026 ; revue des maquettes non réalisée.** Aucun visuel final n'a été examiné dans cette mission de préparation. Aucun vote, préférence ou résultat d'utilisabilité n'est attribué à un expert. Les profils ci-dessous seront simulés par IA ; ils ne représentent ni des professionnels interrogés ni des tests avec de vrais utilisateurs.

## Périmètre retenu

La revue porte uniquement sur les orientations P1 adoptées [UX01 à UX05](../workshop/backlog-ux.md) : résumé quotidien et collectif, listes de risques du portefeuille, clarification des responsabilités, rattachement des prochaines actions et continuité du rendez-vous. Les [votes de l'étape 2](../workshop/votes-et-arbitrages.md) concernent les orientations, pas les maquettes à venir.

Les constats d'origine restent ceux des [observations factuelles](../observations/observations-factuelles.md), de la [couverture du pilotage](../observations/couverture-pilotage-commercial.md) et des [limitations](../observations/limitations.md). Une maquette peut proposer une présentation ; elle ne prouve ni l'existence d'une API, ni la cohérence des données réelles, ni l'efficacité pour une équipe de dix personnes.

## Les six questions de revue

| Repère | Question à instruire lors de l'examen futur | Type de preuve attendu |
| --- | --- | --- |
| Q1 | Comprend-on l'état de la prospection et la portée des informations affichées ? | Zones visibles de synthèse et de listes, unités, périodes, filtres, états vide/chargement/indisponible. |
| Q2 | Identifie-t-on les actions à réaliser maintenant et prochainement ? | Hiérarchie des priorités, échéances, responsables et accès proposé aux actions. |
| Q3 | Peut-on comprendre comment qualifier et suivre un prospect ? | Contexte du prospect, de ses dossiers et de leurs responsables ; conservation des notions existantes. |
| Q4 | Peut-on comprendre comment planifier, retrouver et poursuivre un rendez-vous ? | Continuité proposée entre fiche, confirmation, agenda, préparation, compte rendu et prochaine étape. |
| Q5 | Les risques d'oubli deviennent-ils repérables sans créer d'alertes trompeuses ? | Définition des listes de risques, rattachement des tâches, cas de recouvrement et exceptions. |
| Q6 | Quelle présentation est préférable, pour quel besoin et avec quelles réserves ? | Comparaison argumentée avec les captures réelles, à scénario et données comparables ; absence de préférence admise. |

## Grille par expert

Chaque expert devra examiner les mêmes versions et répondre séparément avant confrontation. Les cellules ci-dessous sont des questions à poser, jamais des résultats anticipés.

| Expert simulé | Q1 — État de prospection | Q2 — Actions | Q3 — Qualification et suivi | Q4 — Rendez-vous | Q5 — Oublis | Q6 — Préférence |
| --- | --- | --- | --- | --- | --- | --- |
| E1 — UX SaaS B2B | La portée Mes actions/Équipe est-elle identifiable sans effort, avec une hiérarchie stable ? | Le prochain geste se distingue-t-il des informations secondaires sans saturer l'accueil ? | Les rôles prospect/dossier/action sont-ils nommés dans leur contexte sans transformer toute la fiche ? | Les transitions proposées conservent-elles le contexte et un accès clair à l'objet confirmé ? | Une personne peut-elle comprendre pourquoi une fiche figure dans une liste de risque et accéder à son détail ? | Quel écran réduit la navigation ou l'ambiguïté, et quelle zone visible étaye ce jugement ? |
| E2 — CRM et Sales Operations | Chaque total précise-t-il son unité, sa population et sa période ; les catégories évitent-elles les additions trompeuses ? | L'échéance, le rappel et le responsable de l'action restent-ils distincts des autres objets ? | L'étape du dossier reste-t-elle distincte du prospect et de son potentiel, sans nouvelle règle de qualification ? | Compte rendu, statut et prochaine action sont-ils cohérents avec les commandes déjà repérées ? | Prospect sans action, dossier sans action, inactivité et stagnation sont-ils définis séparément, avec seuils à arbitrer ? | Quelle présentation favorise un pilotage interprétable, sans attribuer à des nombres fictifs une valeur de preuve ? |
| E3 — Responsable commercial | Une revue d'équipe peut-elle commencer par quelques faits actionnables plutôt qu'une accumulation de chiffres ? | Un commercial voit-il qui agit et quand, ainsi que ses engagements proches ? | Peut-il identifier rapidement qui suit la relation et qui porte l'opportunité sans demander aux collègues ? | Peut-il comprendre où préparer le rendez-vous et retrouver sa suite commerciale ? | Les dossiers nécessitant une décision ressortent-ils sans imposer des tâches sur tous les dossiers clos ou en pause ? | Quel gain opérationnel paraît le plus plausible, et quelle limite empêcherait encore un usage autonome ? |
| E4 — Onboarding et accessibilité | Les mots, unités et états vides sont-ils compréhensibles sans connaître les règles du CRM ? | La priorité et le retard sont-ils exprimés autrement que par couleur seule, avec libellés lisibles ? | Les trois responsabilités sont-elles explicites au point d'action sans aide longue ou jargon ajouté ? | Dates, horaires, fuseau, erreurs et confirmation sont-ils lisibles ; les limites d'un examen d'image sont-elles signalées ? | Une alerte explique-t-elle son sens et son périmètre, notamment lorsqu'une autre action existe déjà sur le prospect ? | Quelle présentation facilite l'orientation d'un novice ; quels aspects clavier, focus, lecteur d'écran ou mobile restent non évaluables ? |
| E5 — UX researcher et facilitateur | Les variantes utilisent-elles un scénario équitable et une population comparable, sans faux zéro ni total inventé présenté comme réel ? | L'expert décrit-il une possibilité visible ou prétend-il mesurer une réussite qui n'a pas été testée ? | Le jugement sur les responsabilités reste-t-il une hypothèse de compréhension à éprouver avec des personnes réelles ? | La maquette distingue-t-elle clairement le parcours proposé des fonctions non vérifiées dans l'application ? | Les seuils, exclusions et recouvrements sont-ils explicitement discutables, et les angles morts conservés dans le rapport ? | La préférence est-elle rattachée à une preuve visuelle et à un besoin, avec possibilité de réserve ou d'absence de préférence ? |

## Garde-fous de périmètre

| Risque de dépassement | Contrôle nécessaire pendant la revue |
| --- | --- |
| Fixer arbitrairement la stagnation ou l'inactivité de UX02 | Tout seuil numérique de démonstration doit être identifié comme hypothèse illustrative à valider avec le métier ; aucun délai ne devient une règle canonique par son seul affichage. Définir séparément interaction récente et évolution de dossier. |
| Prétendre à l'exhaustivité par une somme de cartes | Vérifier les unités prospect/dossier/action et les catégories qui se recoupent ; les nombres fictifs ne prouvent ni couverture complète ni rapprochement backend. |
| Fusionner responsabilités ou rattachements | Un responsable de dossier ne devient pas automatiquement responsable du prospect ou exécutant de toutes les actions ; une tâche du prospect ne couvre pas tous ses dossiers. Aucun transfert silencieux. |
| Intégrer les orientations P2 hors du périmètre de cette étape | UX06 (création progressive), UX07 (null), UX08 (retour filtré), UX09 (transmission) et UX10 (aides qualification) restent exclues des améliorations revendiquées. Leur adoption à l'étape 2 ne les fait pas entrer dans ce lot P1. Le périmètre de UX03 est la compréhension des responsabilités, pas une nouvelle transmission de dossier. |
| Réintroduire les solutions rejetées | Aucune prochaine action obligatoire à toute sortie, aucune affectation universelle à tour de rôle et aucune complétude totale imposée dès la création : UX11, UX12 et UX13 restent rejetées. |
| Présenter UX05 comme création d'une capacité absente | Réservation observée ; commandes de modification, annulation et compte rendu repérées dans le code local. La continuité en UI reste non vérifiée. La maquette illustre des raccords à vérifier, elle ne démontre pas leur absence actuelle. |
| Transformer une image en validation de fonctionnement | Totaux, filtrage, pagination, notifications, disponibilité et enregistrement doivent être testés ultérieurement. Un lien dessiné ou un état de succès fictif ne constitue pas une exécution. |
| Conclure au mobile ou à l'accessibilité sur le timeout d'exploration | Le délai n'établit aucun défaut produit. Une image mobile pourrait permettre une inspection de composition seulement ; clavier, focus dynamique, lecture d'écran et usage réel restent à éprouver. |
| Confondre comparaison visuelle et préférence utilisateur | Le jugement des experts est simulé. Une différence de volume, de données ou de cadrage entre captures et maquettes doit être signalée avant toute préférence. |

## Déroulement prévu après réception des visuels

1. Consigner les fichiers, versions, dimensions et scénarios réellement examinés ; identifier les captures « avant » et les maquettes « après ». Aucun examen ne sera déclaré sur la seule description d'un fichier.
2. Examiner chaque image, puis répondre aux six questions pour chaque expert avec une zone précise ou un état visible comme preuve.
3. Qualifier chaque remarque : **OBSERVÉ SUR MAQUETTE** pour une caractéristique visuelle, **DÉDUIT** pour une conséquence probable, **HYPOTHÈSE** pour un effet sur l'utilisateur. Ces étiquettes ne remplacent pas les observations réelles de l'étape 1.
4. Repérer les écarts au périmètre P1 et les informations manquantes ; conserver les réserves, même si la majorité préfère une variante.
5. Confronter les avis initiaux ; documenter la préférence ou l'absence de préférence de chaque expert, sans reprendre automatiquement les votes de l'étape 2 et sans attribuer de voix aux personas non examinés dans cette mission.
6. Si des corrections de maquette sont apportées, identifier la nouvelle version et ne considérer comme réexaminées que les images effectivement revues. Une validation métier ou un test utilisateur restera une étape distincte.

## Fiche de relevé à remplir ultérieurement

| Champ | Valeur actuelle |
| --- | --- |
| Images et versions inspectées | Aucune dans cette mission de préparation. |
| Réponses E1–E5 aux questions Q1–Q6 | À produire après inspection. |
| Réserves ou écarts constatés sur les maquettes | Aucun constat produit à ce stade. |
| Préférences individuelles | Non recueillies, même sous forme simulée. |
| Votes sur les maquettes | Aucun. |
| Conclusion de revue | En attente des visuels. |
