# Epic 59 - Tests de performance et de capacite des API

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-59-tests-performance-api-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Objet

Cette Epic met en place un dispositif reproductible de tests de performance des
API Localeo. Elle doit detecter les regressions, verifier le comportement de la
plateforme sous charge, identifier ses premiers points de saturation et fournir
des resultats comparables entre deux versions du backend.

Elle concretise l'action `ASP-ACT-036` du rapport
[`audit-securite-performance-2026-08-29.md`](../../audits/backend/audit-securite-performance-2026-08-29.md).
Cette action ne pourra passer a `CORRIGE`, puis a `VALIDE`, qu'apres livraison du
socle et execution concluante d'une campagne de reference.

## Documents

- [Backlog](../../roadmap/terminees/epic-59-tests-performance-api-backlog.md)
- [Conception technique](conception-technique.md)
- [Registre des arbitrages](registre-arbitrages.md)
- [Procédure complète d'exécution d'une campagne](../../exploitation/technique/executer-campagne-tests-performance-api.md)

## Resultats attendus

- des parcours metier versionnes et executes manuellement avec le binaire k6
  installe sur un poste Windows, avec resultats transmis a Grafana Cloud k6 ;
- des profils `smoke`, nominal, pointe, stress, pic et endurance ;
- des seuils d'echec par parcours et par operation ;
- des jeux de donnees deterministes et isolables ;
- une campagne responsable du backup, de l'import et de la restauration de la
  base ephemere ;
- des garde-fous encadrant strictement tout benchmark de production ;
- des rapports rattaches au commit, a l'environnement et au jeu de donnees ;
- une baseline de reference et un premier constat de capacite documente.

## Parcours couverts

| ID | Parcours | Priorite | Finalite principale |
| --- | --- | --- | --- |
| `PERF-JRN-01` | Internaute Marketplace | P0 | Accueil geolocalise, recherche, catalogue et consultation |
| `PERF-JRN-02` | Internaute Localeo Live | P0 | Installation, suivis, animations, notifications et passeport coffret |
| `PERF-JRN-03` | Commercant | P0 | Contexte, animations, invitations, notifications et validations |
| `PERF-JRN-04` | Animation / collectivite | P0 | Pilotage, dashboard, workflow, participants, gains et bilans |
| `PERF-JRN-05` | Administrateur BackOffice | P0 | SQLAdmin, recherches, visions 360, documents et operations support |
| `PERF-JRN-06` | Achat et cycle de vie d'un coffret | P0 | Paiement de test, creation, ajout a Live et consommation |
| `PERF-JRN-07` | Exploitation / Localeo Control | P1 | Supervision, sante, readiness et diagnostic sous charge |
| `PERF-JRN-08` | Batchs, webhooks et traitements asynchrones | P1 | Debit, backlog, concurrence, reprise et absence de doublons |

Les parcours sont executes separement pour diagnostiquer leur capacite, puis
ensemble dans une campagne mixte representant le trafic de la plateforme.

## Principes de conception

- separer la logique metier d'un parcours de son profil de charge ;
- mesurer des percentiles et des taux d'erreur, jamais une moyenne seule ;
- taguer chaque requete par parcours, operation et type de donnees ;
- calibrer d'abord une baseline technique par paliers, puis etablir les volumes
  cibles a partir des mesures reelles lorsqu'elles seront disponibles ;
- executer les ecritures sur des donnees propres a la campagne ;
- isoler ou simuler Stripe, Brevo, le SMS, le WebPush et le stockage externe ;
- conserver les tests fonctionnels dans `pytest` et utiliser le banc de charge
  pour la latence, le debit, la concurrence et l'endurance ;
- rendre les echecs explicites et exploitables avec les identifiants de
  parcours, d'operation et de campagne.

## Hors perimetre initial

- Core Web Vitals, rendu navigateur et performance JavaScript des frontends ;
- test de penetration ou recherche de vulnerabilites ;
- campagne de charge non supervisee ou avec effets de bord sur la production ;
- dimensionnement contractuel de production depuis un environnement non
  representatif ;
- test du debit propre aux fournisseurs externes.

## Definition d'une campagne valide

Une campagne est comparable uniquement si elle conserve :

- la meme version de scripts ;
- le meme profil de charge ;
- la meme taille de jeu de donnees ;
- une topologie d'environnement documentee ;
- la meme strategie vis-a-vis des caches et fournisseurs externes.

Chaque resultat indique au minimum le `runId`, le commit, l'environnement, la
date, le profil, la taille des donnees, le resultat des seuils et les anomalies
observees.

## Etat initial

- Statut : `Cadrage arbitre - implementation a realiser`.
- Outil retenu : binaire k6 execute directement sur le poste Windows, sans
  Docker, avec scripts versionnes et resultats dans Grafana Cloud k6 Free.
- Environnements cibles : production pour les lectures sures, manuelles et
  bornees ; environnement ephemere cree a la demande pour les ecritures et les
  campagnes lourdes.
- Execution : exclusivement manuelle, sous autorisation et surveillance d'un
  administrateur.
- Topologie ephemere : PostgreSQL `0,5 CPU / 1 Go RAM` et backend Render
  `0,5 CPU / 512 Mo RAM`.
- Seuils : propositions initiales a confirmer apres la baseline.

[Retour à l’index des spécifications](../INDEX.md)
