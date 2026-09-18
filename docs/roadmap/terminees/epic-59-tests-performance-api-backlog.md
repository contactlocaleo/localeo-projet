# Backlog Epic 59 - Tests de performance et de capacite des API

## Synthese

- Statut : `Termine`.
- Criticite : `Haute`.
- Application principale : `localeo-backend`.
- Applications contributrices : Marketplace, Localeo Live, espace commercant,
  Localeo Animation, BackOffice et Localeo Control.
- Dependances : compte Grafana Cloud k6 Free, environnement ephemere cree a la
  demande, donnees de test, observabilite applicative et acces aux metriques
  PostgreSQL/Render.
- Action d'audit associee : `ASP-ACT-036`.

Voir le [cadrage](../../specifications/epic-59-tests-performance-api/README.md), la
[conception](../../specifications/epic-59-tests-performance-api/conception-technique.md)
et le [registre des arbitrages](../../specifications/epic-59-tests-performance-api/registre-arbitrages.md).

## Tranche A - Socle reproductible et garde-fous

- `PERF-US-001` (`Termine`) Valider les arbitrages structurants `PERF-ARB-01`
  a `PERF-ARB-16`.
- `PERF-US-002` Integrer les scripts k6 versionnes, leur execution par le
  binaire natif Windows et la transmission des resultats a Grafana Cloud k6
  Free.
- `PERF-US-003` Separer les parcours, profils de charge, donnees, controles et
  seuils dans une arborescence modulaire.
- `PERF-US-004` Refuser toute cible non explicitement autorisee et imposer un
  mode production sans effet de bord distinct du mode ephemere.
- `PERF-US-005` Definir un plafond par campagne pour la duree, le debit et le
  nombre d'utilisateurs virtuels.
- `PERF-US-006` Produire un `runId` et taguer les mesures par parcours,
  operation, environnement et commit.
- `PERF-US-007` Creer les profils `small`, `reference` et `capacity`, puis faire
  orchestrer par la campagne le backup, l'import, la surcouche `runId` et la
  restauration de la base ephemere.
- `PERF-US-008` Archiver un resume lisible et les resultats structures.

## Tranche B - Internaute Marketplace

- `PERF-US-009` Couvrir la selection territoriale et l'accueil geolocalise.
- `PERF-US-010` Couvrir la recherche, les commercants et les profils publics.
- `PERF-US-011` Couvrir les catalogues et listes publiques paginees.
- `PERF-US-012` Couvrir la consultation d'un coffret sans declencher de
  paiement reel.
- `PERF-US-013` Executer smoke, nominal, pointe et stress du parcours
  `PERF-JRN-01`.

## Tranche C - Internaute Localeo Live

- `PERF-US-014` Couvrir l'onboarding d'une installation et ses preferences.
- `PERF-US-015` Couvrir les suivis, animations et notifications recurrentes.
- `PERF-US-016` Couvrir les participations, QR codes et passeports coffret.
- `PERF-US-017` Simuler le pic de consultations suivant une notification
  WebPush.
- `PERF-US-018` Executer smoke, nominal, pic et endurance du parcours
  `PERF-JRN-02`.

## Tranche D - Commercant

- `PERF-US-019` Authentifier des commercants de test et charger leur contexte.
- `PERF-US-020` Couvrir tableaux de bord, animations et notifications.
- `PERF-US-021` Couvrir consultation et decision sur les invitations.
- `PERF-US-022` Couvrir les validations avec des QR codes uniques et une
  campagne d'idempotence dediee.
- `PERF-US-023` Executer smoke, nominal et pointe du parcours `PERF-JRN-03`.

## Tranche E - Animation / collectivite

- `PERF-US-024` Couvrir session, contexte portail et commune active.
- `PERF-US-025` Couvrir dashboard, listes, detail et workflow d'animation.
- `PERF-US-026` Couvrir participants, validations, live, tirages, gains,
  flyers et bilans.
- `PERF-US-027` Isoler creation, publication, cloture, tirage et envoi de gain
  dans des scenarios a donnees uniques.
- `PERF-US-028` Mesurer separement les exports CSV et PDF.
- `PERF-US-029` Executer smoke, nominal et endurance du parcours
  `PERF-JRN-04`.

## Tranche F - Administrateur BackOffice

- `PERF-US-030` Gerer la session admin, les cookies et les protections CSRF.
- `PERF-US-031` Couvrir le dashboard et les listes SQLAdmin paginees.
- `PERF-US-032` Couvrir les recherches et visions 360 client, commercant,
  achat et animation.
- `PERF-US-033` Couvrir catalogue, documents, communications, support et
  supervision des reversements.
- `PERF-US-034` Isoler les mutations, remboursements et communications dans un
  environnement sans effet externe reel.
- `PERF-US-035` Executer smoke, nominal et endurance du parcours
  `PERF-JRN-05`.

## Tranche G - Achat et cycle de vie d'un coffret

- `PERF-US-036` Initialiser un paiement avec Stripe en mode test.
- `PERF-US-037` Simuler les confirmations et repetitions de webhook.
- `PERF-US-038` Verifier la concurrence sur le stock et l'idempotence.
- `PERF-US-039` Retrouver l'achat, les coffrets crees et leur passeport Live.
- `PERF-US-040` Executer une validation de prestation sur une instance dediee.
- `PERF-US-041` Executer smoke, nominal et pointe du parcours `PERF-JRN-06`.

## Tranche H - Exploitation et traitements asynchrones

- `PERF-US-042` Verifier que Localeo Control, les healthchecks et readiness
  restent disponibles pendant une campagne nominale ou de pointe.
- `PERF-US-043` Mesurer le debit des outbox email, SMS et WebPush sans appeler
  les fournisseurs reels.
- `PERF-US-044` Mesurer les batchs d'expiration, de rappel et de maintenance.
- `PERF-US-045` Tester la concurrence des workers et l'absence de doublons.
- `PERF-US-046` Injecter un backlog controle, interrompre le traitement et
  mesurer sa reprise.
- `PERF-US-047` Executer les campagnes `PERF-JRN-07` et `PERF-JRN-08`.

## Tranche I - Baseline, campagne mixte et lancement manuel

- `PERF-US-048` Etablir une baseline technique par paliers depuis une charge
  minimale, puis la recalibrer lorsque des metriques de trafic seront
  disponibles.
- `PERF-US-049` Executer chaque parcours isole et ratifier ses seuils.
- `PERF-US-050` Executer une campagne mixte et ajuster sa repartition.
- `PERF-US-051` Identifier le premier point de saturation et la ressource
  limitante.
- `PERF-US-052` Fournir une commande manuelle de smoke obligatoire avant une
  campagne plus lourde.
- `PERF-US-053` Fournir les lancements manuels des profils nominal, mixte,
  pointe, stress, pic et endurance, avec autorisation administrateur.
- `PERF-US-054` Documenter l'analyse des ecarts et la procedure de diagnostic.
- `PERF-US-055` Mettre `ASP-ACT-036` a `CORRIGE`, puis `VALIDE` uniquement apres
  verification des preuves attendues.

## Criteres d'acceptation

- les huit parcours ont un identifiant stable et des mesures separees ;
- les six parcours P0 disposent au minimum d'un smoke et d'une charge nominale ;
- les parcours P1 disposent d'une campagne reproductible documentee ;
- un depassement de seuil provoque un code de sortie non nul ;
- la production ne peut etre ciblee qu'en mode explicite, manuel, borne et sans
  effet de bord ;
- aucun paiement, email, SMS ou WebPush reel n'est produit ;
- les ecritures concurrentes reposent sur des donnees uniques ou testent
  explicitement l'idempotence ;
- les resultats identifient commit, environnement, profil et jeu de donnees ;
- une regression volontaire de reference est detectee ;
- la baseline, la campagne mixte et le premier point de saturation sont
  documentes ;
- les metriques applicatives et PostgreSQL permettent d'expliquer les
  principaux ralentissements.

## Recette transverse

- execution manuelle sur le profil `small` ;
- execution manuelle du binaire k6 local sur une cible autorisee, avec
  resultats transmis a Grafana Cloud ;
- refus d'une URL non autorisee et refus des scenarios mutables en production ;
- expiration ou absence d'un secret de test ;
- donnees absentes, partielles puis volumineuses ;
- parcours isoles puis campagne mixte ;
- comparaison de deux commits sur la meme topologie ;
- saturation CPU, memoire, pool SQL et connexions PostgreSQL ;
- interruption puis reprise d'un traitement asynchrone ;
- verification de l'absence d'effets externes reels.
