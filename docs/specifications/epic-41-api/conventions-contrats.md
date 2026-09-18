# Conventions et contrats communs - APIs EPIC 41

> Consolidation documentaire du 18 septembre 2026 : contributions Backend et Animation réunies ; les compléments ANIM-003, ANIM-004, ANIM-005 et ANIM-008 sont conservés dans cette version commune.

## 1. Exposition et routage

Les chemins suivent `/{exposition}/animation-locale/{ressource}` :

- `public` : inscription et consultation participant par token ;
- `protected` : portail partenaire et application commercant authentifies ;
- `internal` : supervision, correction exceptionnelle et batchs Localeo.

Chaque operation porte les tags OpenAPI `Animation locale` et son niveau d'exposition.

Les URLs publiques ne sont pas construites par le backend. `LOCALEO_ANIMATION_PUBLIC_URL_TEMPLATE` contient l'URL complete avec `{animation_id}` et `LOCALEO_ANIMATION_PARTICIPANT_URL_TEMPLATE` l'URL complete avec `{participant_token}`. Des URLs locales sont admises en developpement ; la recette de bout en bout et la production exigent HTTPS.

## 2. Authentification et tenant

Chaque appel protege du portail doit produire un contexte serveur contenant :

```text
acteur_id
partenaire_id
roles
communes_habilitees
commune_active_id
abonnement_id
permissions_effectives
correlation_id
```

Regles obligatoires :

- ne jamais faire confiance a un `partenaire_id` fourni par le client ;
- verifier que toute ressource demandee appartient a une commune habilitee ;
- appliquer le filtre tenant avant agregation, tri et pagination ;
- controler le droit d'acces et l'etat d'abonnement avant chaque commande payante ;
- retourner `404` plutot qu'exposer l'existence d'une ressource hors tenant.

La commune active est portee par une session Animation serveur distincte et modifiee par la commande dediee. Le token opaque reference cette session, expire apres 8 heures et ne porte aucune permission faisant autorite. Une ressource adressee par identifiant est toujours reverifiee depuis les habilitations persistantes. Aucun fournisseur OIDC externe n'est introduit au MVP.

La suppression d'un participant est une operation sensible distincte de la modification d'une animation. Elle exige la permission explicite `animation:supprimer_participant`, portee par l'habilitation persistante du gestionnaire pour la commune active. Les habilitations existantes ne recoivent pas automatiquement cette permission.

## 3. Pagination, filtres et tri

Format cible des listes :

```json
{
  "items": [],
  "page": 1,
  "page_size": 25,
  "total": 0,
  "next_cursor": null
}
```

Regles initiales :

- `page_size` par defaut : `25`, maximum : `100` ;
- pagination par curseur preferee pour flux live et audit ;
- pagination par page acceptable pour listes de gestion stables ;
- tris autorises listes explicitement par endpoint ;
- dates au format ISO 8601 avec fuseau ;
- filtres dates sous forme `date_debut` inclusive et `date_fin` exclusive ;
- recherche textuelle normalisee cote serveur.

## 4. Erreurs

Toutes les routes reutilisent `ApiErrorResponse` et stabilisent un `code` metier exploitable par le frontend.

| HTTP | Usage |
| ---: | --- |
| `400` | Requete syntaxiquement valide mais parametres incoherents. |
| `401` | Session ou token absent/invalide. |
| `403` | Acteur authentifie sans permission fonctionnelle. |
| `404` | Ressource absente ou hors tenant. |
| `409` | Transition ou invariant metier viole, doublon fonctionnel. |
| `410` | Token public expire ou revoque. |
| `422` | Validation structurelle du payload. |
| `429` | Limite anti-abus ou quota depasse. |
| `500` | Erreur interne non exposee. |
| `502` / `503` | Dependances externes indisponibles lorsque l'operation ne peut etre mise en file. |

Codes metier initiaux :

```text
ANIMATION_HORS_TENANT
ABONNEMENT_INACTIF
PERMISSION_ANIMATION_INSUFFISANTE
TRANSITION_ANIMATION_INTERDITE
CONFIGURATION_ANIMATION_INCOMPLETE
COMMERCANT_NON_ELIGIBLE
COFFRET_NON_ELIGIBLE
INSCRIPTION_FERMEE
PARTICIPANT_DEJA_INSCRIT
PARTICIPANT_ENGAGE_DANS_TIRAGE
QR_PARTICIPANT_INVALIDE
QR_PARTICIPANT_EXPIRE
VALIDATION_DEJA_ENREGISTREE
POPULATION_ELIGIBLE_NON_FIGEE
TIRAGE_DEJA_REALISE
GAIN_DEJA_ENVOYE
DOCUMENT_ANIMATION_NON_DISPONIBLE
EXPORT_ANIMATION_EN_COURS
```

## 5. Commandes et idempotence

Les commandes suivantes exigent `Idempotency-Key` :

- publication ;
- cloture ;
- tirage ;
- envoi d'un gain ;
- regeneration de flyer ;
- inscription participant ;
- renvoi de QR ;
- generation d'export asynchrone.

La suppression d'un participant n'utilise pas de cle d'idempotence : le premier appel retourne `204`, puis un nouvel appel retourne `404` car la ressource n'existe plus.

Une meme cle, pour le meme acteur et la meme route, retourne le resultat initial. Une reutilisation avec un payload different retourne `409`.

Les documents et exports utilisent l'abstraction du domaine `documentaire`. Le backend local est reserve au developpement ; les environnements heberges utilisent un stockage objet prive et exposent le contenu par une route protegee ou une URL signee de courte duree.

Reponse commune recommandee :

```json
{
  "operation_id": "uuid",
  "resource_id": "uuid",
  "status": "SUCCEEDED",
  "resource_status": "PUBLIEE",
  "next_action": {
    "code": "SUIVRE_LIVE",
    "target": "live"
  },
  "processing": null
}
```

## 6. Traitements asynchrones

La publication, la generation documentaire, les exports et les notifications peuvent etre partiellement asynchrones.

Une commande acceptee retourne `202` avec :

```json
{
  "operation_id": "uuid",
  "status": "PENDING",
  "resource_id": "uuid",
  "processing": {
    "status_url": "/protected/animation-locale/operations/uuid",
    "retry_after_seconds": 2
  }
}
```

Le contrat de suivi valide est :

```text
GET /protected/animation-locale/operations/{operation_id}
```

L'echec de diffusion d'un email apres publication ne doit pas annuler la publication. Le resultat distingue l'etat metier de la ressource et l'etat des effets secondaires.

Les exports CSV UTF-8 sont synchrones jusqu'a 10 000 lignes et asynchrones au-dela. Un fichier exporte reste telechargeable 7 jours avant suppression automatique.

## 7. Audit

Chaque commande sensible enregistre :

- acteur, role, partenaire et tenant commune ;
- ressource et animation ;
- action, date et correlation ;
- ancienne et nouvelle valeur lorsque pertinent ;
- motif obligatoire pour annulation et correction interne ;
- cle d'idempotence ;
- origine `PORTAIL_PARTENAIRE`, `APP_COMMERCANT`, `PUBLIC_PARTICIPANT`, `BACKOFFICE_LOCALEO` ou `BATCH`.

Pour une suppression de participant, l'audit conserve l'identifiant technique, la reference pseudonymisee, l'animation, la commune et le nombre de validations supprimees. Il ne recopie ni nom, ni email, ni telephone.

La projection partenaire masque les evenements de securite, corrections internes et donnees personnelles non necessaires.

## 8. Donnees personnelles et tokens

- Les listes agregees masquent email et telephone par defaut.
- Les exports sont autorises, traces et purges selon la politique EPIC 41.
- Les tokens publics sont opaques, signes ou stockes sous forme de hash, expirables et revocables.
- Les tokens QR participant sont aleatoires CSPRNG d'au moins 256 bits, encodes en Base64URL et stockes uniquement sous forme de hash.
- Par decision `ARB-46`, les PII participant ne sont pas chiffrees au niveau applicatif au MVP. Elles restent protegees par controle d'acces, masquage, audit, securite de l'infrastructure et politique de conservation ; ce choix doit etre reevalue avant production.
- Aucun token ni QR brut n'apparait dans les logs.
- Les endpoints de renvoi de QR appliquent rate limiting et reponse non enumerante.
- La suppression manuelle efface le participant, ses tokens et ses validations. Elle est refusee en `409` si le participant appartient a une population eligible figee ou si un gain le reference ; les preuves de tirage ne sont jamais reecrites.

## 9. Versionnement

Le MVP n'ajoute pas de prefixe `/v1`. Les changements compatibles enrichissent les schemas de maniere additive. Toute rupture future doit passer par une strategie de version explicite et une periode de migration documentee.


## ANIM-003 - Validations et population de tirage

La validation, son annulation, l'inscription et la suppression d'un participant
prennent le verrou transactionnel de l'animation, comme la cloture. Apres attente,
le statut, le token et les donnees participant sont relus dans la transaction.
La population figee contient ainsi toutes les validations commitees avant cloture;
aucune validation ni annulation ne peut modifier son eligibilite apres cloture.
Deux scans simultanes sont serialises avant de recalculer la progression.


## ANIM-004 - Seuil de qualification

Le contrat utilise `regles.nombre_validations_requises` (entier 1..1000) et
`validation_unique_par_commercant=true`. Le scan et l'evaluation metier comptent
les commercants participants distincts avec une validation effective. Quatre
validations distinctes sur dix commercants suffisent si le seuil vaut quatre.
La publication refuse un seuil superieur au nombre de commercants acceptes.
En mode AUTO, le seuil est recalcule sur ces acceptations avant publication.

Compatibilite : l'ancien `seuil_validations` est traduit si le champ canonique
est absent. Si les deux sont presents, le champ canonique fait foi, y compris
pour l'affichage des animations historiques. Aucun tirage existant n'est recalcule;
les regles deja publiees ne changent pas implicitement. Une modification explicite
du seuil en preparation devient MANUELLE et relance les invitations concernees.


## ANIM-005 - Calendrier et instants

Les dates saisies dans Animation representent des journees Europe/Paris.
Le client transmet des ISO UTC explicites : debut a minuit local, fin exclusive
au minuit suivant le dernier jour choisi. Une journee de changement d'heure dure
23 ou 25 heures. Le scan accepte exactement [debut, fin[; les inscriptions sont
refusees des la fin. Le flyer et le formulaire affichent le dernier jour inclus.
Les echeances de reponse commercant portent sur la journee locale Europe/Paris.
Les anciens instants sans decalage conservent leur interpretation UTC; aucune
migration automatique ne decale les animations publiees. Verifier leurs periodes
sur staging avant activation et corriger explicitement les brouillons si besoin.


## ANIM-008 - Creation rejouable et atomique

La meme intention de creation reutilise une cle UUID. L'API serialise cette cle
pour l'acteur et la route au moyen d'un verrou transactionnel PostgreSQL.
Animation, configuration, invitations initiales et reponse d'idempotence sont
commitees ensemble. Une interruption avant commit ne laisse aucun brouillon;
apres commit le rejeu renvoie la meme reponse. Un payload different pour la meme
cle est refuse. Les autorisations et la commune active sont controlees avant le rejeu.

Complement ANIM-003 : la modification de configuration, y compris la prolongation
de date de fin, prend aussi le verrou animation. Une edition demarree avant une
cloture ne peut donc pas restaurer un ancien statut EN_COURS apres celle-ci.

Complement ANIM-005 : la comparaison de dates et la generation de flyer acceptent
la prolongation UTC explicite d une animation historique dont le debut est un
instant sans fuseau. Ce debut conserve sa valeur et son interpretation UTC.
