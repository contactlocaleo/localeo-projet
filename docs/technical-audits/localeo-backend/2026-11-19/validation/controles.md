# Contrôles de l’étape 1

Statut : succès des contrôles documentaires ; aucune mesure de performance exécutée.

| Contrôle réellement exécuté | Résultat |
| --- | --- |
| `py -3.14 scripts/check_guidance.py` avec rapport | 118 guides, 1687 liens locaux, zéro erreur, zéro avertissement |
| `py -3.14 scripts/check_guidance.py --repo . --all-markdown --changed` avec rapport | 53 documents, 1997 liens locaux, zéro erreur, zéro avertissement au moment du contrôle initial |
| Contrôle direct des références de lignes du dossier | 1474 références vers des fichiers existants et lignes valides ; 177 sources backend référencées, empreintes conservées |
| Présence des sept livrables | Succès |
| Contrôle UTF-8 et chemins statiques non résolus dans les livrables | Zéro anomalie restante |
| `git diff --check` | Succès ; contrôle des différences suivies, complété par les vérifications explicites des nouveaux documents |
| État final backend | Checkout propre ; HEAD `7049e7fafc76f9119924f1082a5ee7457a175d85`, identique à l’état inspecté |

Python local utilisé : 3.14.3, via `py -3.14`. L’alias `python` ne fonctionne pas dans cette session Windows ; le lanceur disponible exécute les mêmes scripts documentaires.

Preuves : [guidance.json](guidance.json), [liens-audit.json](liens-audit.json), [références et empreintes](references-sources.json), [métadonnées](metadonnees.json). Le rapport des documents modifiés peut inclure les documents utilisateur déjà présents dans `docs/ux-workshops/localeo-crm/` ; ils n’ont pas été édités par cette tâche. Les nombres peuvent évoluer après l’ajout de ce compte rendu.

Le seul dépôt modifié par la tâche est `localeo-projet`, sous le dossier daté de cet audit. Les autres dépôts ne reçoivent aucune écriture. Aucune modification des exports : `sync_documentation.py --check-sources` non requis et non exécuté. Aucun test métier, import d’application, charge, profilage, connexion base, migration, appel fournisseur ou déploiement. Les contrôles de liens ne valident ni les règles métier ni la capacité.

Les deux sous-agents de cartographie ont terminé sans accès aux sources ; leurs périmètres ont été repris par lecture directe de l’agent principal. Aucun agent spécialisé ni processus applicatif n’est actif pour cet audit. Prochain geste : autorisation utilisateur selon la dernière contrainte du prompt, puis prévol d’accès aux outils avant lancement des six missions.
