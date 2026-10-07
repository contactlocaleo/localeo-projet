# EPIC 70 — Validation par PIN sur le téléphone du client

Version **V1 du 5 octobre 2026**. État produit **En cours**, suivi dans la
[roadmap](../../roadmap/README.md). Cette spécification traduit les 34 critères du
[backlog canonique](../../roadmap/en-cours/epic-70-validation-prestation-telephone-client-backlog.md).
Implémentation et vérifications locales le 7 octobre 2026 ; consulter le bilan pour les preuves. Aucun déploiement ni recette sur une cible réelle.

## Documents

- [Utilisation et exploitation](guide-utilisation-exploitation.md) : parcours, incidents, configuration et conservation.

- [Architecture et contrats](architecture-contrats.md) : existant vérifié, domaine,
  droits, transactions, API, données et compatibilité.
- [Vérification et livraison](verification-livraison.md) : couverture des 34 critères,
  scénarios de test, migrations, démonstration et limites de validation.
- EPIC 72 — Accès salariés (spécification publiée avec E72) : acteur nominatif
  distinct du PIN partagé, historique et protections de Localeo Pro.

## Décisions produit acquises

| Sujet | Règle V1 |
| --- | --- |
| Usage | Une prestation de coffret ou une validation terrain Animation, sur le téléphone connecté du client ; aucun équipement commerçant requis au comptoir |
| Secret | Un PIN actif par commerce, généré automatiquement sur 6 chiffres ; suites simples et chiffres tous identiques exclus |
| Validité | Immédiate ; de 1 à 30 jours entiers, 7 par défaut ; horloge serveur |
| Demande | 5 minutes pour saisir et confirmer ; expiration sans consommation ni progression |
| Essais | 5 PIN incorrects en 15 minutes par commerce, toutes demandes et tous appareils confondus, bloquent le canal PIN 15 minutes |
| Fin de blocage | Automatique, sans prolongation par des tentatives pendant le blocage ; aucun rétablissement d'un PIN expiré ou révoqué |
| Gestion | Principal dans Localeo Pro ; mot de passe vérifié depuis 15 minutes maximum pour créer/remplacer ; invalidation seule sans nouvelle saisie dans une session principale valable |
| Support | Admin et Backoffice peuvent invalider et aider à récupérer l'accès ; Lecteur/Finance seuls refusés ; aucun opérateur ne lit le PIN |
| Succès | Une notification Localeo Pro par validation effective, sans email de validation |
| Changement/blocage | Alerte Localeo Pro et email au principal, sans PIN |
| Audit | Succès et refus corrélés, commerce et version du PIN ; aucune identité de salarié prétendue |
| Surveillance | Pas de nouvelle alerte de volume propre au PIN ; règles métier du scan existant conservées |
| Conservation | Politiques Localeo existantes, selon catégorie ; aucune durée nouvelle arbitraire |

Un jour correspond ici à 24 heures depuis la génération, en UTC. L'interface
présente la date locale et le fuseau ; le passage heure d'été/hiver ne prolonge
pas la validité. Une date de fin est exclusive : `now >= expires_at` refuse.

## Parcours et interfaces

1. Le principal prépare le PIN dans Localeo Pro, rubrique « Validation par PIN » :
   durée, génération, affichage unique du nouveau code, état et date d'expiration.
   Un PIN perdu est remplacé ; aucun bouton de récupération de sa valeur.
2. Le client ouvre son coffret ou sa participation avec son droit personnel.
   « Faire valider par PIN » prépare une demande sur une cible éligible. Le nom
   du commerce, l'action et son effet s'affichent avant de tendre le téléphone.
3. Le commerçant saisit le code masqué et confirme. Le délai restant vient de
   `expires_at`, sans prolongation client. Aucun compte professionnel n'est ouvert.
4. Le serveur confirme l'effet ou refuse. Le reçu indique la cible, la date et la
   référence, sans argent professionnel ni autre dossier client. Le champ est vidé.
5. Après une coupure réseau, relire le reçu avant toute nouvelle action. Un résultat
   incertain n'est jamais un succès. Le scan QR et le secours E9 gardent leurs règles.

Erreur de code : « Code incorrect ». Blocage : heure de reprise affichée.
Demande expirée : « Relancer la validation ». PIN indisponible : proposer de
contacter le responsable ou d'utiliser le scan, sans indiquer le secret ni
inventer une validation hors ligne. Les commandes sensibles ne sont pas rejouées
automatiquement par le navigateur. Les réponses privées ne sont pas mises en cache.

## Existant, limites et préparation

La lecture des sources locales a porté sur le backend à base `760a5c9`,
Marketplace à base `4e948f1` et Commerçant à base `4785603` ; elle n'atteste aucun
déploiement. Les chemins et adaptations précis figurent dans l'architecture.

Le moteur Animation applique déjà une règle de cadence commune au scan, pouvant
retourner `ANOMALIE` sans progression. La décision « pas d'alerte de volume V1 »
est appliquée à l'ajout E70 : elle ne retire pas cette règle existante, conformément
à la décision de conserver exactement les conditions et effets du QR. Un résultat
`ANOMALIE` ne doit jamais être présenté comme un succès de validation.

Les comportements et contrats sont définis pour préparer l'implémentation. Le [rattachement commun de conservation](../identite-acces/conservation-validations-acces.md) est établi depuis le 7 octobre à partir de l'Annexe A : la limite documentaire est levée. Les traitements de conservation et leurs preuves restent à réaliser avant mise en service.
