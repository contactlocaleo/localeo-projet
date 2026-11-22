# ÉTAPE 3 — CONSOLIDATION TRANSVERSE ET CONTRE-EXPERTISE

Tu es l'architecte orchestrateur chargé de consolider les six audits spécialisés du backend Localeo.

## 1. Charger les analyses

Lis les six rapports indépendants.

Archive ce prompt dans `prompts/03-contradiction.md`.

Le code source reste la référence principale.

## 2. Consolidation par cause racine

Ne juxtapose pas les rapports des agents.

**Regroupe obligatoirement les anomalies par cause racine et par flux métier.**

Pour chaque problème :

1. Identifie les symptômes.
2. Recherche la cause racine.
3. Vérifie les références au code.
4. Identifie les API concernées.
5. Identifie les domaines impactés : CPU, mémoire, persistance, concurrence, etc.
6. Déduplique les constats.
7. Propose une correction unique lorsque plusieurs symptômes ont la même origine.

Exemple :

Une API charge trop d'enregistrements.

Conséquences :

- Temps d'accès aux données élevé.
- Consommation mémoire excessive.
- Sérialisation coûteuse.

Une seule cause racine doit produire une seule recommandation consolidée si une correction commune suffit.

## 3. Analyse par flux métier

Reconstitue les risques sur :

- Validation QR.
- Participation.
- Consultation des animations.
- Tableau de bord.
- Import de commerçants.
- Clôture.
- Tirage au sort.
- Consultation des résultats.
- Autres flux critiques identifiés.

Identifie les goulots dominants.

## 4. Agent contradicteur

Fais intervenir un agent indépendant chargé de challenger les conclusions.

Il doit :

- Vérifier les preuves.
- Rechercher les faux positifs.
- Contester les priorités excessives.
- Identifier les optimisations prématurées.
- Proposer des corrections plus simples.
- Examiner les risques de régression.
- Vérifier la compatibilité.
- Identifier les mesures manquantes.

Livrable : `contradiction/contre-expertise.md`

## 5. Débat contradictoire

Organise une confrontation des conclusions.

Pour chaque problème majeur :

- Diagnostic initial.
- Preuves.
- Objections.
- Cause racine retenue.
- Alternatives.
- Correction minimale.
- Risques.
- Mesures nécessaires.

## 6. Vote technique

Les six agents spécialisés disposent chacun d'une voix simulée.

Une orientation est adoptée avec au moins 4 voix favorables sur 6.

Le contradicteur ne vote pas.

Le vote ne remplace jamais les preuves techniques.

Les problèmes critiques restent documentés indépendamment du vote.

## 7. Priorisation

P0 — Risque critique confirmé ou fortement étayé.

P1 — Problème significatif avec impact probable important.

P2 — Optimisation utile mais différable.

P3 — Optimisation secondaire ou prématurée.

Une anomalie ne peut être classée P0 ou P1 que si son impact est justifié par :

- Une mesure réelle.
- Une preuve technique solide.
- Ou un scénario de charge crédible, explicitement argumenté.

Ne confonds pas une mauvaise pratique avec un problème de performance avéré.

## 8. Backlog resserré

Produis un backlog principal de **5 à 10 optimisations maximum**, sauf si davantage de problèmes critiques sont réellement démontrés.

Ne complète pas artificiellement le backlog.

Pour chaque optimisation :

- ID.
- Cause racine.
- Flux concernés.
- API concernées.
- Références au code.
- Preuves.
- Niveau de confiance.
- Correction minimale.
- Effort.
- Risque.
- Compatibilité.
- Priorité.
- Vote.

Les optimisations secondaires sont conservées dans une annexe.

## 9. Livrables

Crée :

- `contradiction/consolidation.md`
- `contradiction/causes-racines.md`
- `contradiction/contre-expertise.md`
- `contradiction/debats-et-votes.md`
- `recommandations/backlog-preliminaire.md`
- `recommandations/annexe-optimisations-secondaires.md`
- `recommandations/plan-mesures.md`

## 10. Fin d'étape

Présente les problèmes majeurs consolidés.

Distingue les problèmes confirmés, les risques étayés et les hypothèses.

Ne modifie aucun code.

Attends mon autorisation avant l'étape 4.
