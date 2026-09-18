# Epic 60 - BackOffice ERP, referencement et commercialisation 360

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-60-vision-360-commercialisation-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Version implementee V1

La reference fonctionnelle est [la specification detaillee](specifications-fonctionnelles.md).
Le perimetre PRD-561 a PRD-582 est implemente ; la validation finale est suivie
dans [le rapport de developpement](rapport-developpement-v1.md).

- [Contrats API implementes](contrats-api.md).
- [Livraison, migration v218 et exploitation](livraison-v1.md).
- [Registre des arbitrages et hypotheses deleguees](registre-arbitrages.md).
- [Cadrage initial conserve](cadrage-v1.md).

Les analyses et conceptions ci-dessous constituent l'historique du cadrage.
En cas de divergence, specification detaillee, contrats implementes et rapport
de livraison priment. Epic 61 reste fusionnee ; aucun document separe n'est recree.

## Fusion des Epics 60 et 61

Decision utilisateur : fusionner les deux epics. L'Epic 60 devient la
reference unique ; l'identifiant 61 reste reserve pour les liens historiques.
Les stories PRD-561 a PRD-582 et les identifiants COM360-* et ERP-ARB-* sont
conserves, avec leurs validations acquises et leurs decisions encore ouvertes.

Le perimetre reunit diagnostic de vendabilite, alertes, atelier coffret
(creation, edition, composition et rentabilite), dossier commercant
(referencement, prestations et aptitude), navigation ERP et suivi d'activite.
La file de diagnostic reste une consultation avec reevaluation ; les ecritures
metier passent par les ateliers dedies au sein de cette meme epic.

Les ateliers et les sept API de diagnostic sont desormais implementes dans cette meme epic.

## Reference V1 pour demarrer les specifications

Le [cadrage V1](cadrage-v1.md) consolide les decisions utilisateur et definit
les livrables fonctionnels et techniques a produire. Il prime sur les anciennes
propositions non actualisees des analyses historiques. Bascule directe sur
les nouveaux parcours, sans maintien des anciennes interfaces (ERP-ARB-07).

## Dossier unifie

- [Revue produit - iteration 2](revue-produit-iteration-2.md) : reutilisation
  Onboard, publication cible, files de traitement et protection des engagements.

- [Analyse des parcours ERP et referencement](analyse-parcours-erp.md).
- [Registre unique des arbitrages](registre-arbitrages.md).
- [Plan de livraison unifie](plan-livraison-unifie.md).
- Les sections suivantes decrivent le diagnostic de commercialisation ; les
  ateliers et les menus sont decrits dans l'analyse ERP.

## Intention produit du volet diagnostic

La Vision 360 Commercialisation est le poste de contrôle de la disponibilité
réelle du catalogue Localeo. Elle répond en priorité à trois questions :

1. Quels coffrets sont réellement vendables maintenant ?
2. Quels coffrets ne le sont pas et pourquoi ?
3. Quelle action permet de les remettre en vente ?

Elle ne crée aucune règle de vendabilité dans l'interface. Elle projette le
résultat du diagnostic canonique déjà utilisé par la Marketplace et le paiement.

## Positionnement

| Dispositif existant | Responsabilité conservée |
| --- | --- |
| Vision 360 Coffret - Epic 28 | Rentabilité, composition et reversements d'un coffret |
| Vision 360 Commerçant - Epic 27 | Référencement et activité d'un commerçant |
| Conformité BUM - Epic 50 | Diagnostic fiscal, politique et qualification |
| Stripe Connect - Epic 39 | Capacité d'encaissement et de reversement |
| Vision 360 Commercialisation - Epic 60 | Verdict final, causes croisées, alertes et orientation vers le traitement |

## Modèle du diagnostic

### Verdict

| Verdict | Définition |
| --- | --- |
| `VENDABLE` | Aucun blocage canonique et route publique autorisée |
| `NON_VENDABLE` | Au moins un blocage métier identifié |
| `INDETERMINE` | Le diagnostic n'a pas pu être produit complètement |

Un statut source tel que `ACTIVE`, `AUTO_ELIGIBLE` ou `VALIDATED` ne doit
jamais être assimilé isolément au verdict final.

### Contrat d'un contrôle

```json
{
  "code": "BUM_GUARANTEED_PROMISE_MISSING",
  "family": "BUM",
  "severity": "CRITICAL",
  "status": "FAILED",
  "message": "La promesse garantie du coffret n'est pas renseignée.",
  "resourceType": "COFFRET",
  "resourceId": "uuid",
  "detectedAt": "2026-09-05T08:30:00Z",
  "treatment": {
    "label": "Renseigner la promesse garantie",
    "target": "/admin/coffret/edit/uuid#promesse-garantie"
  }
}
```

Les statuts de contrôle sont `PASSED`, `FAILED` et `UNKNOWN`. La présence
d'un `UNKNOWN` sur un contrôle obligatoire conduit au verdict
`INDETERMINE`.

## Référentiel minimal des contrôles

| Famille | Codes minimaux | Traitement principal |
| --- | --- | --- |
| Catalogue | `COFFRET_NOT_ACTIVE`, `NO_ACTIVE_PRESTATION`, `INVALID_PRICE` | Fiche coffret |
| Contrat | `GUARANTEED_PROMISE_MISSING`, `INDICATIVE_CONTENT_MISSING` | Fiche coffret |
| BUM | Codes `BUM_*`, dont politique, wording, qualification et requalification | Localeo Onboard / diagnostic BUM |
| Commerçant | `MERCHANT_MISSING`, `MERCHANT_NOT_ACTIVE` | Vision 360 commerçant |
| Stripe | `STRIPE_ACCOUNT_MISSING`, `STRIPE_CHARGES_DISABLED`, `STRIPE_PAYOUTS_DISABLED`, `STRIPE_REQUIREMENTS_DUE`, `STRIPE_ACCOUNT_DISABLED` | Onboarding Stripe du commerçant |
| Territoire | `CITY_NOT_PUBLISHED`, `CITY_MISMATCH` | Fiche commune |
| Technique | `DIAGNOSTIC_FAILED`, `STALE_PROJECTION` | Réévaluation / exploitation |

Le code existant `BUM_GUARANTEED_PROMISE_MISSING` reste supporté. Une
normalisation des familles ne doit pas casser les consommateurs ou l'historique.

## Architecture de lecture

Le service `diagnostiquer_blocages_vendabilite_coffret` devient la façade
canonique et retourne un diagnostic structuré, pas uniquement une liste de
chaînes. Les routes publiques continuent à consommer le verdict sans exposer les
motifs internes.

Une projection `projection_vendabilite_coffret` conserve seulement l'état de
pilotage :

- `coffret_id` ;
- `verdict` ;
- `blocking_codes` ;
- `warning_codes` ;
- `diagnostic_hash` ;
- `evaluated_at`, `changed_at` et `source_event` ;
- `diagnostic_version`.

Cette projection n'est pas une source de vérité métier. Le détail est
recalculable depuis les agrégats existants.

## Déclenchement des évaluations

Une réévaluation est demandée après toute modification susceptible d'affecter
la vendabilité :

- statut, prix ou contenu contractuel du coffret ;
- ajout, retrait, version ou statut d'une prestation ;
- statut du commerçant ;
- synchronisation Stripe Connect ;
- activation ou modification de la politique BUM ;
- qualification ou requalification du coffret ;
- publication de la commune.

Un batch de réconciliation périodique traite les événements manqués et signale
les projections trop anciennes. Les traitements sont idempotents et protégés
contre les mises à jour concurrentes.

## Alertes

Une alerte ouverte est identifiée par :

```text
coffret_id + verdict + diagnostic_hash
```

Règles :

- transition `VENDABLE -> NON_VENDABLE` : alerte critique ;
- transition vers `INDETERMINE` : alerte technique critique ;
- modification des causes : mise à jour ou nouvelle occurrence historisée ;
- retour à `VENDABLE` : résolution automatique ;
- aucune répétition tant que l'empreinte ne change pas ;
- l'âge de l'alerte correspond à la première détection non résolue.

## UX BackOffice

La page s'ouvre sur la file `Non vendables`, avec :

- une ligne de KPI compacte ;
- des filtres persistants dans l'URL ;
- un tableau paginé ;
- une colonne `Pourquoi ?` affichant le blocage prioritaire et le nombre de
  causes supplémentaires ;
- une colonne `Depuis` ;
- un bouton `Traiter` menant à l'écran approprié ;
- un accès au détail 360.

La fiche 360 présente d'abord le verdict, puis les blocages. Les contrôles
réussis sont repliés par défaut. La chronologie et les données techniques sont
dans des sections secondaires.

## Localeo Control

Localeo Control expose :

- le nombre de coffrets nouvellement non vendables ;
- les cinq alertes les plus critiques ;
- un raccourci vers la file BackOffice filtrée ;
- une notification WebPush optionnelle pour les transitions critiques.

Localeo Control ne corrige aucune donnée de commercialisation.

## Contrats API cibles

| ID | Méthode et route | Finalité |
| --- | --- | --- |
| `COM360-API-001` | `GET /internal/commercialisation/vision-360/synthese` | KPI et ventilation des blocages |
| `COM360-API-002` | `GET /internal/commercialisation/vision-360/coffrets` | Recherche et file paginée |
| `COM360-API-003` | `GET /internal/commercialisation/vision-360/coffrets/{coffret_id}` | Diagnostic détaillé |
| `COM360-API-004` | `GET /internal/commercialisation/vision-360/coffrets/{coffret_id}/chronologie` | Historique paginé |
| `COM360-API-005` | `POST /internal/commercialisation/vision-360/coffrets/{coffret_id}/reevaluer` | Réévaluation idempotente |
| `COM360-API-006` | `GET /internal/commercialisation/vision-360/alertes` | Alertes ouvertes et résolues |
| `COM360-API-007` | `GET /internal/commercialisation/vision-360/territoires` | Communes sans offre vendable |

Les listes utilisent une pagination bornée. La réévaluation exige une clé
`Idempotency-Key`.

## Sécurité et audit

- accès réservé aux profils internes `ADMIN` et `EXPLOITATION` ;
- filtrage territorial appliqué aux profils limités à certaines communes ;
- absence de données personnelles et de secrets Stripe ;
- audit des consultations détaillées, exports éventuels et réévaluations ;
- codes d'erreur stables et corrélation selon l'Epic 44.

## Observabilité

Mesures minimales :

- nombre de coffrets par verdict ;
- transitions de vendabilité par famille ;
- âge médian et maximal des blocages ouverts ;
- délai moyen de retour à `VENDABLE` ;
- durée et taux d'échec des diagnostics ;
- nombre de projections obsolètes.

## Stratégie de tests

- tests unitaires de chaque contrôle et de la priorité des blocages ;
- tests de combinaison BUM, Stripe, commerçant et catalogue ;
- tests d'idempotence et de déduplication des alertes ;
- tests d'habilitation et de cloisonnement territorial ;
- test de parité entre verdict 360, liste publique, détail public et
  initialisation du paiement ;
- test de non-régression du cas
  `VALIDATED + AUTO_ELIGIBLE + promesse absente` ;
- tests de performance sur les volumes de référence.

## Documents

- [Backlog](../../roadmap/terminees/epic-60-vision-360-commercialisation-backlog.md)
- [Registre des arbitrages](registre-arbitrages.md)
- [Conception technique](conception-technique.md) : domaine, controles,
  integration au code existant, persistance, concurrence, alertes et securite.
- [Contrats API](contrats-api.md) : sept routes, schemas, filtres,
  idempotence et erreurs.
- [Plan de tests et livraison](plan-tests-et-livraison.md) : couverture
  PRD-561 a PRD-570, parite publique et recette ; bascule selon le cadrage V1.

La conception precise les cas limites du present document : un controle
non applicable est distingue d'un controle reussi ; une projection obsolete
expose un verdict indetermine et son dernier verdict connu ; la cle d'alerte
deduplique une occurrence ouverte sans empecher une rechute identique.
Les choix proposes et les confirmations utilisateur restent traces dans le
registre, sans assimiler conception et implementation.

## État

`Cadrage V1 finalise pour lancement des specifications - conception diagnostic a consolider - specification ERP a produire - implementation a realiser`.

## Documents complémentaires du dossier

- [Commission par prestation et saisie en euros](commission-par-prestation.md)

[Retour à l’index des spécifications](../INDEX.md)
