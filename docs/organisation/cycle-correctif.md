# Diagnostiquer et livrer un correctif Localeo

Cette procédure accompagne [localeo-corriger](../../.agents/skills/localeo-corriger/SKILL.md). Elle complète les [règles transverses](../../AGENTS.md) et les instructions des applications touchées. Un défaut circonscrit se traite directement ; il n'impose pas la création d'une epic ni la réécriture de toute une spécification.

## Établir les faits utiles

Recueillir à partir de la demande et des artefacts disponibles :

- résultat attendu et résultat observé, avec leur source ;
- déclencheur et étapes minimales, rôle ou droits pertinents ;
- environnement et version où le défaut apparaît, si connus ;
- message d'erreur, identifiant de corrélation ou données minimales expurgées ;
- caractère systématique ou intermittent, conséquences et éventuel contournement connu.

Lire le statut Git et les instructions des dépôts concernés. Distinguer la version signalée, la version déployée connue et l'arbre local testé. Une référence `LOC-…` ne prouve ni la cause ni l'accès aux journaux ; ne pas annoncer une consultation distante qui n'a pas eu lieu. Ne pas demander à l'utilisateur des informations déjà disponibles dans les fichiers ou tests locaux.

Le comportement attendu vient du besoin explicite et de la spécification canonique. Un ancien bilan ou le comportement actuel ne suffit pas à l'établir. Si plusieurs interprétations changent une règle produit, isoler cette décision et continuer le diagnostic indépendant ; ne pas ajouter une approbation pour une correction courante déjà autorisée.

## Reproduire et identifier la cause

Construire une reproduction minimale : test de domaine, application, adaptateur, consommateur ou scénario navigateur selon le point de défaillance. Utiliser les environnements isolés prévus par les guides locaux. Des fakes simulent les ports et incidents extérieurs sans recopier l'algorithme testé.

Quand le défaut s'y prête, exécuter le test avant le correctif et vérifier qu'il échoue pour la raison attendue. Une erreur d'import, de configuration ou d'environnement ne démontre pas le défaut métier. Après correction, réexécuter ce test et les scénarios adjacents significatifs. Ne pas modifier une assertion pour qu'elle accepte le comportement fautif.

Si la reproduction exige un service, des données ou un environnement indisponibles, préciser cette limite. Une correction peut s'appuyer sur une cause locale démontrée, mais elle ne prouve pas la résolution sur la version distante. Distinguer faits établis, hypothèses et observations restant à recueillir ; ne pas déclarer une dette préexistante sans comparaison vérifiable.

Suivre la chaîne de responsabilité : producteur, contrat, consommateur, données et points d'entrée. Pour une règle métier, identifier son propriétaire dans le domaine selon la [matrice d'architecture](../architecture/transverse/controle-architecture.md). Un message trompeur peut devoir être amélioré sans être la cause du refus ; retirer une protection de concurrence, d'accès ou de validation n'est pas une correction de sa cause.

## Corriger le périmètre nécessaire

Le correctif traite la cause et les consommateurs touchés, en conservant les modifications utilisateur. Éviter les refontes indépendantes. Une adaptation de contrat ou migration nécessaire fait partie du correctif ; la simplicité apparente d'un patch ne justifie pas un contournement des invariants.

Pour les défauts récurrents ou transverses, rattacher la correction à l'[anomalie](../roadmap/anomalies) ou à l'epic existante pertinente. Mettre à jour le suivi demandé sans inventer une nouvelle numérotation ni rouvrir implicitement une epic terminée. Si le besoin devient une nouvelle fonctionnalité, appliquer le [cycle d'epic](cycle-epic.md) à ce périmètre supplémentaire.

### Impacts à vérifier

Conserver le résultat dans la spécification, le suivi d'anomalie, la PR ou le compte rendu existant selon l'ampleur du correctif. Ne pas créer un registre parallèle pour une petite correction.

| Sujet | Question et preuve utile |
| --- | --- |
| Comportement corrigé | La reproduction passe-t-elle après correction ? Le nominal et les refus importants restent-ils couverts ? |
| Contrats et interfaces | Producteur, schéma, générateur et consommateurs restent-ils compatibles ? Les erreurs affichées décrivent-elles le refus réel ? |
| Persistance et versions | Les données existantes nécessitent-elles une migration ou réparation ? Ne pas confondre un patch de code et une réparation exécutée. |
| Démonstration et fixtures | Le défaut provient-il de données générées ou affecte-t-il génération, export, restauration, rôles ou parcours ? Vérifier les scénarios touchés. |
| Documentation fonctionnelle | Le document décrit-il encore le comportement réel ? Corriger la source canonique lorsque nécessaire. |
| Exploitation | Les diagnostics, paramètres, reprises et vérifications après livraison changent-ils ? Actualiser la procédure applicable. |

Indiquer « sans objet » avec la raison pour un impact absent. Une inconnue reste à examiner.

## Vérifier et rendre compte

Exécuter les tests proportionnés et contrôles obligatoires des dépôts affectés. Les contrôles statiques et builds complètent les preuves comportementales. Pour la documentation, `python scripts/check_guidance.py --document <document>` vérifie les liens ; `python scripts/sync_documentation.py --check-sources` s'ajoute si les sources exportées changent. Aucun de ces contrôles ne prouve un parcours métier.

Une revue indépendante est utile pour une cause sensible, plusieurs entrées métier ou un contrat transverse. Fournir le diff et le scénario concret ; demander notamment si le patch ouvre un contournement ou manque un consommateur. L'agent principal intègre et vérifie les corrections.

Un correctif urgent peut avoir un périmètre réduit et des vérifications différées explicitement identifiées. L'urgence ne transforme pas un échec ou un test ignoré en succès et ne dispense pas des contrôles requis. Ne pas supprimer de tests, affaiblir une assertion ni désactiver un garde-fou pour obtenir une CI verte. Présenter les limites restantes avant de déclarer le travail vérifié.

### Critères de fin

- Le déclencheur, l'attendu et l'observé sont compris ; la cause et ses limites sont explicites.
- Le correctif traite cette cause et respecte les frontières métier et contrats concernés.
- Le test de reproduction ou la preuve adaptée confirme la correction sur l'arbre effectivement testé ; les contrôles requis ont un résultat rapporté.
- Les impacts documentaires, démonstration, données et exploitation sont traités ou déclarés avec leur conséquence sur la livraison.
- Le compte rendu distingue réussite, échec, non-exécution et dette démontrée, et n'annonce ni déploiement ni réparation de données non réalisés.

Mentionner les dépôts, la version testée (SHA, ou SHA de base et changements locaux), les commandes, résultats et risques résiduels. Utiliser la note courte de reprise du [cycle d'epic](cycle-epic.md) si l'investigation se prolonge. Commit, push et déploiement restent des opérations distinctes suivant la demande ; la préparation de livraison suit les procédures d'[exploitation](../exploitation/INDEX.md).
