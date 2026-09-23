# Préparer une livraison vérifiable

Cette procédure assemble les preuves du [cycle d'epic](cycle-epic.md). Les [releases](../../releases/INDEX.md) conservent les références des livraisons, les [procédures d'exploitation](../exploitation/INDEX.md) décrivent les actions propres aux environnements. Elle ne remplace aucune de ces sources.

## Dossier à produire

Utiliser `python scripts/quality.py --help` depuis `localeo-projet` pour planifier et exécuter les contrôles, puis préparer un manifeste. Les sorties sous `.artifacts/quality/` sont ignorées par Git ; ne pas y mettre de secrets. Le manifeste décrit une préparation, jamais une preuve de déploiement.

| Élément | Preuve ou limite à consigner |
| --- | --- |
| Périmètre | Epic/spécification, environnement, applications affectées et compatibilité des autres applications |
| Versions | SHA complet de chaque dépôt, état de travail, références de la livraison précédente si connues |
| Validation | Commandes, dates, versions testées, résultats, scénarios non exécutés et échecs |
| API | Producteurs, contrats canoniques/embarqués et tests des consommateurs concernés |
| Documentation | Sources exportées, bundle vérifié et son empreinte ; contrôles des lecteurs si modifiés |
| Données | Migrations attendues et leurs checksums ; compatibilité du générateur et empreinte du jeu si utilisé |
| Configuration | Noms des paramètres requis ; disponibilité contrôlée par l'opérateur, sans valeurs sensibles |
| Reprise | Sauvegarde attendue, preuve de restauration adaptée, limites des migrations irréversibles |
| Exécution | Ordre des opérations, conditions d'arrêt et procédures canoniques applicables |
| Après livraison | Santé technique, recette des usages critiques et observations datées sur la cible |

Une commande réussie sur des fichiers non committés sert au développement ; elle ne prouve pas les octets d'un SHA de livraison. Renouveler les validations quand les sources testées changent. Ne pas réduire un profil de tests pour obtenir un dossier sans blocage.

## Contrôles automatiques et opérateur

Le runner conserve la sélection des contrôles et les états `passed`, `failed` ou `not_run`. Vérifier les noms exacts dans le rapport. La préparation signale les preuves manquantes ; un hash de fichier seul ne confirme pas sa validité ni son déploiement.

La commande `release` exige le rapport `workspace` pour une livraison coordonnée. Ajouter `--demonstration-required --demo-report <rapport> --dataset <artefact>` lorsque le générateur ou les données sont concernés. Le manifeste sépare les blocages automatiques et les vérifications opérateur restantes : `prepared_for_review` signifie que les preuves automatiques exigées sont présentes et cohérentes, jamais que la production est prête. Codes de sortie : `0` pour un plan, des contrôles réussis ou un dossier prêt à examiner ; `1` pour un contrôle incomplet/échoué ou un dossier bloqué ; `2` pour une entrée ou configuration invalide.

Pour le backend seul, construire et vérifier le vrai [bundle documentaire](../exploitation/technique/reference-documentation-centralisee.md). Pour les migrations, appliquer la [procédure schéma](../exploitation/technique/deployer-et-verifier-schema.md). Pour une séance de démonstration, utiliser la [recette du générateur](../exploitation/demonstration/realisation-recette.md), puis la préparation fournisseur de l'environnement autorisé.

Les bases jetables CI ne prouvent pas la préparation de Stripe, Brevo ou S3 sur une cible réelle. Les reçus opérateur et sauvegardes restent dans le stockage privé prévu. La conclusion distingue : code vérifié, livraison préparée, action autorisée, déploiement exécuté et usages vérifiés.

## Contrôles requis dans GitHub

Les workflows versionnés s'exécutent après publication des modifications. Dans les règles des branches utilisées pour livrer, rendre requis les jobs pertinents de tests, architecture, démonstration et documentation, une fois leurs noms constatés dans une exécution réelle. Conserver un job de synthèse stable si une matrice ou des filtres rendent les noms variables.

Le workflow documentaire local contrôle ce qui est disponible dans son dépôt. Le contrôle workspace requiert les cinq références exactes et un accès en lecture aux dépôts privés ; une absence d'accès doit échouer explicitement. Les réglages GitHub et les secrets ne sont pas installés par la seule création du YAML. Ne jamais mettre une valeur de jeton dans ce guide ou un manifeste.
