# Backlog Epic 23 - Gestion des batchs et ordonnancement

## Synthese

- Criticite : `Critique`
- Statut : `Termine`
- Objectif : industrialiser l'execution des batchs Localeo avec un inventaire centralise, un ordonnancement fiable, une supervision exploitable et des garde-fous de production.
- Decision produit : les batchs doivent etre pilotables par l'exploitation sans intervention developpeur.
- Decision technique : conserver les endpoints batch existants sous `/protected`, puis ajouter une couche d'ordonnancement et de suivi d'execution.
- Decision operationnelle : chaque batch doit avoir une frequence cible, un statut de derniere execution, des compteurs, une politique de retry et une alerte en cas d'echec.
- Evolution d'implementation : l'[Epic 48](epic-48-apscheduler-ordonnancement-batchs-backlog.md) intègre APScheduler au service FastAPI Render en réutilisant ce socle.

## Probleme

Localeo dispose deja de plusieurs traitements batch : envoi email, synchronisation email, envoi SMS, synchronisation SMS, expiration des coffrets, relances avant expiration, purge des sessions commercant et purge des activites locales obsoletes.

Ces traitements sont aujourd'hui executables via API protegee ou action back-office, mais leur ordonnancement reste externe ou manuel. Sans orchestration explicite, Localeo risque des oublis d'execution, des doubles lancements non maitrises, des retards d'envoi, des expirations non appliquees et des difficultes de diagnostic en production.

## Risque business

- Emails ou SMS transactionnels envoyes en retard.
- Coffrets expires encore utilisables ou visibles comme actifs.
- Relances avant expiration non envoyees.
- Sessions commercant conservees trop longtemps.
- Support incapable de savoir si un batch a tourne correctement.
- Incident de production difficile a diagnostiquer faute d'historique d'execution.

## Risque technique

- Dependances implicites entre batchs non documentees.
- Absence de verrouillage pouvant provoquer des executions concurrentes.
- Resultats de batchs visibles seulement dans les logs.
- Pas de healthcheck dedie par traitement asynchrone.
- Pas de politique standard de retry, timeout, dry-run et alerte.

## Perimetre MVP

- Inventorier les batchs existants et leurs endpoints.
- Definir une frequence recommandee par batch.
- Ajouter une documentation operationnelle des batchs.
- Ajouter un modele d'execution batch auditable.
- Tracer chaque lancement avec statut, dates, duree, acteur, endpoint, parametres non sensibles et compteurs.
- Ajouter un verrou anti-concurrence par type de batch.
- Exposer une vue back-office de supervision des batchs.
- Prevoir un mode lancement manuel securise depuis le back-office.
- Ajouter un endpoint de health operationnel des batchs critiques.
- Formaliser l'ordonnancement cible pour l'infrastructure de production.

## Hors perimetre MVP

- Developper un orchestrateur distribue complexe.
- Remplacer les providers email/SMS.
- Refaire la logique metier interne des batchs existants.
- Ajouter une file de messages externe obligatoire.
- Automatiser les remboursements bancaires.
- Faire du scheduling multi-tenant.

## User Stories

1. `PRD-125` En tant qu'exploitant, je veux consulter l'inventaire des batchs disponibles afin de savoir quels traitements doivent etre planifies.
   - Statut : `Termine`
   - Resultat attendu : chaque batch affiche son nom, son endpoint, son scope de securite, ses parametres, sa criticite et sa frequence cible.

2. `PRD-126` En tant qu'exploitant, je veux voir la derniere execution de chaque batch afin de detecter rapidement un traitement en retard.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche date de debut, date de fin, statut, duree, acteur et compteurs principaux.

3. `PRD-127` En tant que systeme, je veux journaliser chaque execution batch dans une table dediee afin de conserver une trace exploitable hors logs techniques.
   - Statut : `Termine`
   - Resultat attendu : chaque execution porte un `batch_code`, un statut, les dates, les compteurs, les erreurs et une correlation technique.

4. `PRD-128` En tant que systeme, je veux empecher deux executions concurrentes d'un meme batch afin d'eviter les doubles envois ou traitements incoherents.
   - Statut : `Termine`
   - Resultat attendu : un verrou logique ou base de donnees bloque un second lancement si une execution est deja en cours.

5. `PRD-129` En tant qu'exploitant, je veux lancer manuellement un batch depuis le back-office afin de reprendre un traitement apres incident.
   - Statut : `Termine`
   - Resultat attendu : le lancement manuel reste reserve aux admins autorises.
   - Resultat attendu : les batchs sensibles proposent un `dry_run` quand applicable.

6. `PRD-130` En tant qu'exploitant, je veux recevoir une alerte quand un batch critique echoue ou ne tourne pas dans sa fenetre attendue afin d'intervenir avant impact client.
   - Statut : `Termine`
   - Resultat attendu : les echecs des batchs critiques remontent dans un dashboard ou un canal d'alerte configure.

7. `PRD-131` En tant que systeme, je veux exposer un endpoint de health batch afin que l'infrastructure puisse superviser les traitements planifies.
   - Statut : `Termine`
   - Resultat attendu : l'endpoint retourne les batchs en retard, en echec et les derniers compteurs utiles.

8. `PRD-132` En tant qu'exploitant, je veux documenter l'ordonnancement de production afin de configurer cron, Cloud Scheduler, GitHub Actions ou tout autre ordonnanceur sans ambiguite.
   - Statut : `Termine`
   - Resultat attendu : la documentation fournit les frequences, les URLs, les scopes, les timeouts, les limites et l'ordre de lancement recommande.

9. `PRD-133` En tant que responsable exploitation, je veux distinguer les batchs automatiques, manuels et de reprise afin de ne pas automatiser un traitement qui doit rester sous controle humain.
   - Statut : `Termine`
   - Resultat attendu : chaque batch porte une strategie d'execution cible : automatique, manuel, reprise, ou back-office uniquement.

10. `PRD-134` En tant que responsable securite, je veux que les endpoints batch soient proteges, limites et audites afin de reduire le risque d'abus ou de declenchement non autorise.
    - Statut : `Termine`
    - Resultat attendu : les endpoints batch utilisent `internal:batch` ou un scope plus precis.
    - Resultat attendu : les lancements batch sont rate-limites et auditables.

## Inventaire initial des batchs

| Batch | Endpoint automatisable | Strategie cible | Frequence cible |
|---|---|---|---|
| Envoi emails sortants | `POST /protected/emails/batch/envoyer` | Automatique | Toutes les 1 a 5 minutes |
| Synchronisation statuts emails | `POST /protected/emails/batch/synchroniser-statuts` | Automatique | Toutes les 15 a 30 minutes |
| Envoi SMS sortants | `POST /protected/sms/batch/envoyer` | Automatique | Toutes les 1 a 5 minutes |
| Synchronisation statuts SMS | `POST /protected/sms/batch/synchroniser-statuts` | Automatique | Toutes les 15 a 30 minutes |
| Expiration coffrets instances | `POST /protected/coffrets-instances/expiration/batch` | Automatique avec reprise manuelle | 1 fois par jour |
| Relance avant expiration coffrets | `POST /protected/coffrets-instances/expiration/reminders/batch` | Automatique avec reprise manuelle | 1 fois par jour |
| Purge sessions commercant | `POST /protected/maintenance/sessions-commercant/purger` | Automatique | 1 fois par jour |
| Purge activites locales obsoletes | A creer sous `/protected/maintenance/activites-locales/purger` | Automatique ou back-office | 1 fois par jour ou semaine |

## Regles de gestion

- Un batch doit etre idempotent ou explicitement declare non idempotent.
- Un batch critique doit avoir une frequence cible documentee.
- Un batch critique doit produire des compteurs exploitables.
- Un batch ne doit pas exposer de donnees sensibles dans ses parametres traces.
- Un batch en cours ne doit pas etre relance en parallele sauf autorisation explicite.
- Un lancement manuel doit indiquer l'acteur.
- Un lancement par ordonnanceur doit indiquer une identite technique stable.
- Les erreurs doivent etre conservees de facon synthetique, sans secrets ni donnees personnelles inutiles.
- Les batchs d'envoi doivent conserver leur logique outbox et ne pas envoyer directement depuis les parcours metier.
- Les batchs de synchronisation de statuts email/SMS ne doivent interroger le provider que pour les messages dont le statut local n'est pas definitif.
- Pour les emails, les statuts definitifs de synchronisation sont `DELIVRE`, `OUVERT`, `ECHEC_DEFINITIF` et `ANNULE`; les statuts suivis restent `ENVOYE`, `EN_COURS_ENVOI` et `ECHEC_TEMPORAIRE`.
- Pour les SMS, les statuts definitifs de synchronisation sont `DELIVRE`, `ECHEC_DEFINITIF` et `ANNULE`; les statuts suivis restent `ENVOYE`, `EN_COURS_ENVOI` et `ECHEC_TEMPORAIRE`.
- Le statut `OUVERT` email est considere final pour Localeo tant que le suivi des clics n'est pas un besoin metier explicite.

## Modele de donnees cible

### Table `executions_batch`

- `id`
- `batch_code`
- `batch_label`
- `endpoint`
- `acteur`
- `statut` : `EN_COURS`, `SUCCES`, `ECHEC`, `ANNULE`, `TIMEOUT`
- `date_debut`
- `date_fin`
- `duree_ms`
- `parametres`
- `compteurs`
- `erreur_type`
- `erreur_message`
- `correlation_id`
- `date_creation`

### Table `verrous_batch`

- `batch_code`
- `locked_at`
- `locked_by`
- `expires_at`
- `correlation_id`

## Endpoints cibles

### Supervision batchs

- `GET /protected/maintenance/batchs`
- Scope : `internal:batch`
- Usage : retourne l'inventaire, le dernier statut et les frequences cibles.

### Historique executions

- `GET /protected/maintenance/batchs/executions`
- Scope : `internal:batch`
- Usage : liste les executions recentes avec filtres par `batch_code`, statut et dates.

### Health batchs

- `GET /protected/maintenance/batchs/health`
- Scope : `internal:batch`
- Usage : retourne `OK`, `WARNING` ou `CRITICAL` selon les echecs et retards.

### Purge activites locales

- `POST /protected/maintenance/activites-locales/purger`
- Scope : `internal:batch`
- Usage : expose en API batch le use case deja disponible dans le back-office.

## Ordonnancement recommande MVP

```text
*/2 * * * *     POST /protected/emails/batch/envoyer?limit=100
*/2 * * * *     POST /protected/sms/batch/envoyer?limit=100
*/30 * * * *    POST /protected/emails/batch/synchroniser-statuts?limit=100
*/30 * * * *    POST /protected/sms/batch/synchroniser-statuts?limit=100
10 0 * * *      POST /protected/coffrets-instances/expiration/batch?dry_run=false&limit=1000
30 7 * * *      POST /protected/coffrets-instances/expiration/reminders/batch?dry_run=false&limit=1000
45 2 * * *      POST /protected/maintenance/sessions-commercant/purger
15 3 * * *      POST /protected/maintenance/activites-locales/purger
```

## Securite

- Tous les endpoints automatisables doivent etre sous `/protected`.
- Les endpoints batch doivent exiger une cle API avec scope `internal:batch`.
- Les endpoints financiers doivent rester sous un scope dedie si necessaire.
- Les lancements doivent etre audites.
- Les parametres traces doivent etre nettoyes.
- Les erreurs ne doivent pas contenir de token, secret, cle API, email complet si non necessaire ou contenu client sensible.
- Ajouter un rate limiting sur les endpoints batch.

## Observabilite

- Compteurs par execution.
- Derniere execution par batch.
- Temps moyen et temps max.
- Echecs consecutifs.
- Retard par rapport a la frequence cible.
- Volume restant a traiter pour emails/SMS.
- Alertes sur batch critique en echec.

## Lots de realisation

### Lot 1 - Documentation et inventaire

- Ajouter la documentation operationnelle des batchs.
- Documenter endpoints, frequences, scopes, parametres et timeouts.
- Ajouter la purge activites locales a l'inventaire cible.

### Lot 2 - Traces d'execution

- Ajouter `executions_batch`.
- Wrapper les use cases batch pour enregistrer debut, fin, statut et compteurs.
- Masquer les parametres sensibles.

### Lot 3 - Verrouillage

- Ajouter un verrou par `batch_code`.
- Ajouter une expiration de verrou pour gerer les executions interrompues.
- Retourner une erreur metier claire si un batch est deja en cours.

### Lot 4 - API supervision

- Ajouter les endpoints d'inventaire, historique et health.
- Ajouter les schemas de reponse.
- Ajouter les tests de protection par scope.

### Lot 5 - Back-office exploitation

- Ajouter une page de supervision batch.
- Afficher derniere execution, prochain lancement recommande, statut et compteurs.
- Ajouter lancement manuel reserve admin pour les batchs autorises.

### Lot 6 - Ordonnancement production

- Fournir les exemples cron ou Cloud Scheduler.
- Documenter les timeouts et retries infrastructure.
- Documenter les alertes minimales de go-live.

## Tests attendus

- Un batch succes cree une execution `SUCCES`.
- Un batch en erreur cree une execution `ECHEC`.
- Deux lancements concurrents du meme batch sont refuses.
- Un verrou expire peut etre repris.
- Les endpoints batch refusent une cle sans scope `internal:batch`.
- Les parametres sensibles ne sont pas stockes en clair.
- Le health passe en `WARNING` si un batch est en retard.
- Le health passe en `CRITICAL` si un batch critique echoue plusieurs fois.

## Criteres d'acceptation MVP

- L'inventaire des batchs est documente.
- Les frequences recommandees sont documentees.
- Les executions batch sont tracees en base.
- Les batchs critiques ont un verrou anti-concurrence.
- Le back-office permet de voir les dernieres executions.
- L'exploitation dispose d'un endpoint de health batch.
- La purge activites locales est exposable comme batch automatise.
- Les endpoints batch restent proteges par scope.
- Les erreurs et parametres traces ne contiennent pas de secrets.
