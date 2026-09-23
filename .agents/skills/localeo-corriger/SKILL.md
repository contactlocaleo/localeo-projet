---
name: localeo-corriger
description: Diagnostiquer et corriger un défaut Localeo à partir d'une erreur, d'un comportement observé ou d'une régression, avec reproduction et preuves ciblées. Utiliser pour un correctif, y compris urgent, sans imposer une nouvelle epic ; pas pour concevoir une fonctionnalité nouvelle.
---

# Corriger un défaut Localeo

Lire le [guide transverse](../../../AGENTS.md), le guide de l'application concernée et le [cycle de correctif](../../../docs/organisation/cycle-correctif.md). Commencer par l'erreur fournie et les sources ciblées, sans charger l'ensemble des epics.

1. Établir attendu/observé, déclencheur, rôle, environnement et version concernés. Lire le statut Git et distinguer la version signalée de l'arbre local. Exploiter les fichiers ou références d'erreur fournis ; ne pas supposer qu'ils donnent accès aux journaux distants ni charger de secrets.
2. Reproduire avec le cas minimal utile. Vérifier que le test de reproduction échoue pour la raison attendue avant correction lorsque c'est pertinent et possible. Si le défaut dépend d'un service ou de données indisponibles, déclarer ce qui reste hypothétique et poursuivre les vérifications locales indépendantes.
3. Chercher la cause dans le producteur et les entrées concernées, pas seulement dans le message affiché. Pour une règle métier ou un contrat partagé, appliquer [localeo-invariants](../localeo-invariants/SKILL.md). Ne pas neutraliser un contrôle de concurrence, de permissions ou de validation pour faire disparaître l'erreur.
4. Corriger le périmètre nécessaire à la cause, avec les consommateurs affectés. Préserver les modifications existantes et éviter une refonte voisine sans nécessité. Relier la correction au suivi d'anomalie ou à l'epic existante ; une petite correction n'exige pas une nouvelle epic.
5. Vérifier la disparition du défaut, le comportement nominal et les refus significatifs ; exécuter les contrôles requis par les guides locaux. Examiner les impacts documentation, contrat, démonstration, migration et exploitation selon la matrice du cycle de correctif. Un correctif urgent conserve les garde-fous et expose les preuves différées.
6. Rapporter cause démontrée ou hypothèse restante, comportement corrigé, versions testées, commandes/résultats et limites. Une suite ignorée ou indisponible reste non exécutée. Ne pas annoncer un correctif déployé ni des données réparées sans réalisation vérifiée ; commit, push et déploiement suivent la demande courante.
