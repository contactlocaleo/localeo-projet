---
name: localeo-preparer-deploiement
description: Préparer une livraison Localeo vérifiable entre ses dépôts indépendants, avec versions, preuves, migrations et procédures. Utiliser avant un déploiement ou pour contrôler une release ; la préparation ne déclenche ni push ni déploiement.
---

# Préparation d'une livraison

Lire le [guide transverse](../../../AGENTS.md) et la [préparation des livraisons](../../../docs/organisation/preparer-livraison.md). Examiner les procédures de l'environnement et des seules applications concernées dans l'[index exploitation](../../../docs/exploitation/INDEX.md).

1. Identifier environnement, périmètre et références Git de chacun des cinq dépôts. Lire les changements depuis la livraison précédente quand cette référence est connue ; sinon déclarer cette limite. Garder les historiques indépendants. Ne jamais qualifier de livré un arbre de travail non committé.
2. Préparer la livraison coordonnée avec `python scripts/quality.py plan --profile workspace` depuis `localeo-projet`, puis exécuter les profils requis selon son aide. Si les données générées sont affectées, prévoir aussi `plan --profile demonstration` et un rapport distinct. Compléter avec les tests des critères d'acceptation et des consommateurs. Consigner échecs et contrôles non exécutés ; une preuve doit correspondre au code livré.
3. Vérifier migrations/checksums, compatibilité des contrats embarqués, configuration attendue (noms uniquement), bundle documentaire et générateur si affectés. Lire la [procédure de bundle](../../../docs/exploitation/technique/reference-documentation-centralisee.md) et la [procédure schéma](../../../docs/exploitation/technique/deployer-et-verifier-schema.md). Une empreinte ne prouve pas à elle seule un test de restauration ou la validité sémantique d'un contrat.
4. Préparer le manifeste avec `python scripts/quality.py release --help`, les preuves disponibles et la procédure de livraison : ordre des opérations, arrêt en cas d'échec, sauvegarde/restauration adaptée aux migrations, contrôles santé puis métier. Ne pas inventer de rollback de données pour une migration irréversible.
5. Conserver les sorties de travail hors Git. Un dossier est « prêt à examiner » seulement si les limites sont explicites ; l'outil ne déploie rien et les vérifications opérateur restent distinctes des tests locaux. Après toute modification des sources ou références, renouveler les preuves devenues périmées.
6. Réaliser commit, push ou déploiement uniquement lorsqu'ils font partie de la demande en cours ; réutiliser l'autorisation déjà donnée, sans la redemander. Avant une action externe autorisée, appliquer la procédure réelle de l'environnement et ses conditions d'arrêt.
