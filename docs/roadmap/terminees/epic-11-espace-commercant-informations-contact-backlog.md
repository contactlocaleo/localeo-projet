# Backlog Epic 11 - Espace commercant et informations contact

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Perimetre

Epic source : `Epic 11. Espace commercant et informations contact`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : permettre a un commercant authentifie de consulter ses informations de contact et de proposer ou appliquer leur mise a jour depuis son espace, sans passer systematiquement par le support ou le back-office.

## Statut global

- Epic 11 : `Termine`
- Avancement : implementation backend realisee pour la consultation, la modification des contacts autorises, le scope `commercant:profil` et les audits ; verification runtime a finaliser.

## Analyse d'impact

### Synthese

L'Epic s'appuie sur l'authentification commercant par login / mot de passe et sur les sessions courtes de l'Epic 10. Le commercant doit pouvoir consulter les informations qui le concernent et corriger ses donnees de contact operationnelles.

Le point sensible est la gouvernance de modification : seules les donnees de contact operationnelles sont modifiables directement par le commercant. Les informations sensibles restent controlees par le back-office et ne sont pas modifiables via l'espace commercant en V1.

### Informations concernees

Informations consultables par le commercant :
- nom du commerce ;
- type de commerce ;
- ville ;
- description ;
- image ;
- nom et prenom du contact ;
- email de contact ;
- telephone de contact ;
- statut commercant ;
- date de referencement.

Informations modifiables en V1 :
- `contact_nom` ;
- `contact_prenom` ;
- `contact_telephone`.

Informations sensibles non modifiables par le commercant en V1 :
- `contact_email`, car il peut etre utilise comme login et canal de reset ;
- `nom`, `ville_id`, `type_commercant_id`, car ils structurent le referencement ;
- `description`, car elle impacte le catalogue public ;
- `image_uri`, car elle impacte l'affichage catalogue et peut necessiter moderation ;
- `statut`, reserve au back-office.

## Impacts API

Endpoints a ajouter :
- `GET /commercants/me`
- `PATCH /commercants/me/contact`

Les endpoints sont proteges par `Authorization: Bearer <session_token>` et un scope dedie :
- `commercant:profil`

## Impacts use cases

Use cases a creer :
- `ConsulterProfilCommercant`
- `MettreAJourContactCommercant`

Use cases a adapter :
- `ServiceSessionCommercant` : ajouter le scope `commercant:profil`.
- `ValiderSessionCommercant` : exposer le scope sans changement de contrat.
- Back-office commercant : rendre visibles les dernieres modifications de contact.

## Impacts modele de donnees

Option V1 retenue :
- aucune nouvelle table metier n'est necessaire ;
- les champs contact modifiables sont appliques directement sur `commercants` ;
- les modifications sont tracees dans `evenements_audit`.

## Securite et audit

- Seul le commercant authentifie peut consulter ou modifier ses propres informations.
- Le `commercant_id` ne doit pas etre pris depuis le corps de requete ; il doit venir de la session.
- Le changement d'email de contact est hors perimetre V1.
- Les champs non autorises doivent etre rejetes explicitement.
- Les modifications doivent etre auditees.

Actions d'audit minimales :
- `merchant.profile.viewed`
- `merchant.contact.updated`

## Contrat API recommande

### `GET /commercants/me`

Reponse :

```json
{
  "id": "uuid",
  "nom": "Boulangerie Martin",
  "statut": "ACTIF",
  "ville_id": "uuid",
  "type_commercant_id": "uuid",
  "description": "Commerce de proximite",
  "image_uri": "media://...",
  "vignette_url": "https://...",
  "contact": {
    "nom": "Martin",
    "prenom": "Claire",
    "email": "contact@commerce.fr",
    "telephone": "+33600000000"
  },
  "date_referencement": "2026-04-22T10:00:00Z"
}
```

### `PATCH /commercants/me/contact`

Requete :

```json
{
  "contact_nom": "Martin",
  "contact_prenom": "Claire",
  "contact_telephone": "+33600000000"
}
```

Reponse :

```json
{
  "id": "uuid",
  "contact": {
    "nom": "Martin",
    "prenom": "Claire",
    "email": "contact@commerce.fr",
    "telephone": "+33600000000"
  },
  "date_modification": "2026-04-22T10:15:00Z"
}
```

## User Stories

### Story `PRD-051` - Consulter mon profil commercant

En tant que commercant authentifie,
je veux consulter les informations de mon commerce et mes contacts,
afin de verifier les donnees visibles ou utilisees par Localeo.

Criticite : `Haute`
Statut : `Termine`

Critere d'acceptation :
- `GET /commercants/me` retourne uniquement le profil rattache a la session.
- La reponse ne contient pas de donnees sensibles d'authentification.
- Le commercant `SUSPENDU` conserve l'acces a la consultation si sa session existe encore.
- Le commercant `SUSPENDU` ou `ARCHIVE` ne peut pas modifier ses informations de contact.

### Story `PRD-052` - Modifier mes informations de contact

En tant que commercant authentifie,
je veux mettre a jour mon nom de contact, prenom de contact et telephone,
afin de garder mes informations operationnelles a jour.

Criticite : `Haute`
Statut : `Termine`

Critere d'acceptation :
- `PATCH /commercants/me/contact` accepte uniquement les champs autorises.
- Le `commercant_id` est deduit de la session.
- La modification est persistante et auditee avec `merchant.contact.updated`.
- Les formats email/telephone reutilisent les value objects existants quand applicable.
- La modification est refusee si le commercant est `SUSPENDU` ou `ARCHIVE`.

### Story `PRD-053` - Encadrer les modifications sensibles

En tant qu'exploitant,
je veux que les informations sensibles ne soient pas modifiables par le commercant,
afin d'eviter les changements non maitrises sur le catalogue, le login ou la relation contractuelle.

Criticite : `Moyenne`
Statut : `Termine`

Critere d'acceptation :
- Les champs `contact_email`, `nom`, `ville_id`, `type_commercant_id`, `description`, `image_uri` et `statut` ne sont pas modifiables via `/commercants/me/contact`.
- Toute tentative de modification d'un champ non autorise est rejetee explicitement.
- Le login commercant reste gere uniquement par les parcours d'authentification et les actions admin.

### Story `PRD-054` - Auditer les consultations et modifications de profil

En tant qu'exploitant,
je veux tracer les consultations et modifications du profil commercant,
afin de faciliter le support et les controles.

Criticite : `Moyenne`
Statut : `Termine`

Critere d'acceptation :
- La consultation produit une trace `merchant.profile.viewed`.
- La modification produit une trace `merchant.contact.updated`.
- Les valeurs sensibles ne sont pas journalisees en clair au-dela des donnees strictement necessaires.

## Regles de gestion

- Le profil consulte est toujours celui du commercant rattache a la session.
- La modification directe V1 est limitee aux donnees de contact operationnelles.
- Le changement de login/email d'authentification reste hors perimetre de cette Epic.
- La modification de `description` reste hors perimetre V1 et controlee par le back-office.
- La consultation reste autorisee pour un commercant `SUSPENDU` disposant encore d'une session valide.
- La modification est refusee pour un commercant `SUSPENDU` ou `ARCHIVE`.
- Les champs inconnus ou non autorises doivent etre rejetes avec une erreur metier lisible.
- Les modifications doivent etre atomiques.
- Les changements doivent etre visibles dans le back-office.

## Decisions actees

- Les informations sensibles ne sont pas modifiables par le commercant en V1.
- `contact_email` n'est pas modifiable par le commercant.
- `description` n'est pas modifiable par le commercant.
- Aucun workflow de proposition de modification n'est cree en V1.
- Aucune notification support/admin n'est envoyee lors d'une modification de contact.
- Aucun email de confirmation n'est envoye au commercant apres modification.

## Backlog technique

- `EP11-T01` Ajouter les schemas API `ProfilCommercantPayload` et `MettreAJourContactCommercantRequest`. - `Fait`
- `EP11-T02` Ajouter le scope `commercant:profil`. - `Fait`
- `EP11-T03` Creer `ConsulterProfilCommercant`. - `Fait`
- `EP11-T04` Creer `MettreAJourContactCommercant`. - `Fait`
- `EP11-T05` Ajouter `GET /commercants/me`. - `Fait`
- `EP11-T06` Ajouter `PATCH /commercants/me/contact`. - `Fait`
- `EP11-T07` Ajouter les audits `merchant.profile.viewed` et `merchant.contact.updated`. - `Fait`
- `EP11-T08` Ajouter les tests API consultation et modification.
- `EP11-T09` Mettre a jour la documentation fonctionnelle et technique.


## Compléments Commerçant

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### Périmètre

Épic source : `Epic 11. Consultation et modification des informations de contact commercant`
Reference : `docs/roadmap/product-roadmap.md`

Objectif : permettre au commerçant authentifié de consulter et modifier ses informations de contact depuis la PWA commerçant, sans passer par le support ou le back-office.

Les informations de contact ciblées en V1 sont celles déjà exposees dans `CommercantContactPayload` :

- `prenom`
- `nom`
- `email`
- `telephone`

### Statut global

- Avancement : spécification fonctionnelle et technique initiale a valider.

### Analyse d'impact / Synthese

Le commerçant dispose déjà d'une session courte et revocable via `Authorization: Bearer <session_token>`. Cette epic ajoute un parcours self-service permettant de consulter et mettre à jour les coordonnées de contact rattachées au commerçant connecté.

Le changement ne modifie pas l'authentification, les scopes existants ni le statut du commerçant. Il ajoute une surface de modification limitee a des champs de contact non sensibles au sens mot de passe, mais sensibles pour les communications opérationnelles.

### Analyse d'impact / Impacts fonctionnels

- Le commerçant peut consulter ses coordonnées de contact depuis son espace authentifié.
- Le commerçant peut modifier son nom, prénom, email de contact et téléphone.
- Le commerçant voit les valeurs actuellement enregistrées avant modification.
- Le commerçant peut annuler une modification non enregistrée.
- Le système valide le format de l'email et du téléphone.
- Le système conserve une trace d'audit des modifications.
- Les modifications ne changent pas automatiquement le login d'authentification, sauf decision produit explicite ulterieure.
- Le back-office conserve la capacite de modifier ces informations si nécessaire.

### Analyse d'impact / Hors périmètre V1

- Modification du login d'authentification.
- Vérification email par double opt-in.
- Vérification téléphone par OTP.
- Modification de l'adresse physique, horaires, reseaux sociaux ou informations publiques marketing.
- Gestion multi-contacts pour un meme commerçant.
- Workflow de validation admin avant publication.

### Decisions produit recommandees

- Le login d'authentification reste distinct de l'email de contact modifiable.
- Une modification d'email de contact ne révoqué pas les sessions existantes.
- Une modification d'email de contact ne déclenche pas de réinitialisation de mot de passe.
- Le front affiche une confirmation après sauvegarde.
- Les champs `prenom`, `nom`, `email`, `telephone` sont optionnels individuellement en lecture, mais l'email de contact doit rester renseigné si déjà requis par le modèle backend.
- La normalisation du téléphone est faite côté backend ; le front applique seulement une validation ergonomique.

### Impacts API

L'OpenAPI actuel expose `CommercantPayload.contact` via :

- `GET /commercants/{commercant_id}`

Il n'expose pas encore de route dédiée pour modifier les informations de contact du commerçant connecté.

### Impacts API / API cible recommandee / `GET /commercants/me/contact`

Retourne les informations de contact du commerçant connecté.

Headers :

```http
Authorization: Bearer <session_token>
```

Reponse `200` :

```json
{
  "prenom": "Marie",
  "nom": "Durand",
  "email": "contact@commerce.fr",
  "telephone": "+33612345678"
}
```

### Impacts API / API cible recommandee / `PATCH /commercants/me/contact`

Met à jour les informations de contact du commerçant connecté.

Headers :

```http
Authorization: Bearer <session_token>
Content-Type: application/json
```

```json
{
  "prenom": "Marie",
  "nom": "Durand",
  "email": "contact@commerce.fr",
  "telephone": "+33612345678"
}
```

Reponse `200` :

```json
{
  "prenom": "Marie",
  "nom": "Durand",
  "email": "contact@commerce.fr",
  "telephone": "+33612345678"
}
```

### Impacts API / Codes erreur attendus

- `400` : données invalides ou incoherentes.
- `401` : session absente ou invalide.
- `403` : session valide mais scope insuffisant.
- `404` : commerçant rattaché a la session introuvable.
- `409` : conflit métier, par exemple email déjà utilisé comme contact unique si contrainte applicable.
- `422` : erreur de validation schema.
- `500` : erreur technique.

### Impacts use cases

- `ConsulterContactCommercantConnecte`
- `MettreAJourContactCommercantConnecte`

- Aucun use case d'authentification ne doit être modifie.
- `ValiderSessionCommercant` peut rester inchange, sauf si le payload de session doit inclure un résumé de contact en V2.

### Impacts modèle de données

Le modèle `commercants` ou l'entité associée conserve les champs de contact existants.

Champs concernes :

- `contact.prenom`
- `contact.nom`
- `contact.email`
- `contact.telephone`

Aucune nouvelle table n'est requise en V1, sauf si l'audit existant ne permet pas de tracer les modifications.

Si le backend distingue déjà les données de contact dans une structure dédiée, le repository doit exposer une methode de mise à jour atomique limitee a ces champs.

### Regles de gestion consolidees

- Seul le commerçant authentifié peut consulter ses propres informations de contact via `/commercants/me/contact`.
- Seul le commerçant authentifié peut modifier ses propres informations de contact via `/commercants/me/contact`.
- Un commerçant ne peut pas modifier les informations d'un autre commerçant.
- Un commerçant `SUSPENDU` ou `ARCHIVE` conserve l'acces selon la politique de session existante ; si la session est refusee par le backend, le front redirige vers la connexion.
- Le champ `email` doit être au format email valide si renseigné.
- Le champ `telephone` doit être accepté dans un format compatible France/international et normalisé côté backend.
- Les champs texte sont trims côté backend.
- Les champs vides sont convertis en `null` si le modèle l'autorise.
- Une modification de contact ne modifie pas le login d'authentification.
- Une modification de contact ne révoqué pas les sessions existantes.
- Les anciennes et nouvelles valeurs doivent être auditées avec prudence, sans exposer de secret.

### Impacts sécurité et conformité

- Les routes sont protégées par `Authorization: Bearer <session_token>`.
- Les scopes commerçant existants doivent être vérifiés.
- Les erreurs ne doivent pas exposer d'information inutile sur d'autrès comptes.
- Les modifications doivent être auditées avec l'action `merchant.contact.updated`.
- L'audit doit contenir le `commercant_id`, les champs modifiés, la date, et si disponible l'IP/user-agent.
- Les données de contact sont des données personnelles : elles doivent être traitées comme telles dans les logs.

### Impacts front commerçant

Ajouter une entrée dans le menu commerçant :

- Titre : `Mes informations`
- Description : `Consulter et mettre à jour vos coordonnées de contact.`

Ajouter un écran connecté :

- Chargement des informations de contact.
- Affichage des champs :
  - prénom ;
  - nom ;
  - email ;
  - téléphone.
- Bouton `Enregistrer`.
- Bouton `Annuler` ou `Retour au menu`.
- État `loading`.
- État `error`.
- État `success`.
- Gestion `401`/`403` : suppression de la session locale et retour au login.

Le front peut utiliser `GET /commercants/me/contact` en cible. En attente backend, il peut temporairement récupérer le contact via `GET /commercants/{commercant_id}` avec l'id de la session, mais la modification doit passer par une route `/me` pour éviter toute confusion d'autorisation.

### Contrat front cible / Lecture

```js
GET /commercants/me/contact
Authorization: Bearer <session_token>
```

### Contrat front cible / Mise à jour

```js
PATCH /commercants/me/contact
Authorization: Bearer <session_token>
Content-Type: application/json
```

Payload :

```json
{
  "prenom": "Marie",
  "nom": "Durand",
  "email": "contact@commerce.fr",
  "telephone": "+33612345678"
}
```

### Impacts tests / Backend

- Test lecture contact avec session valide.
- Test lecture contact sans session.
- Test modification contact avec session valide.
- Test modification impossible sans session.
- Test modification impossible avec session d'un autre contexte si applicable.
- Test validation email invalide.
- Test validation téléphone invalide.
- Test normalisation des champs trims.
- Test audit `merchant.contact.updated`.

### Impacts tests / Front

- Test rendu de l'entrée `Mes informations`.
- Test chargement et affichage des informations.
- Test modification avec succès.
- Test message d'erreur API.
- Test expiration session et redirection login.
- Test validation minimale email/téléphone côté front.

### Backlog priorise / Story `PRD-051` - Consulter ses informations de contact

Priorite : `P1`
Statut : `À faire`

Valeur métier : permettre au commerçant de vérifier les coordonnées utilisées par Localeo pour le contacter.

Criteres d'acceptation :

- Un endpoint `GET /commercants/me/contact` retourne les coordonnées du commerçant connecté.
- La route est protégée par session commerçant.
- Le front affiche les informations dans une page `Mes informations`.
- En cas de session invalide, le front redirige vers la connexion.

Taches :

- Ajouter le use case `ConsulterContactCommercantConnecte`.
- Ajouter le schema `ContactCommercantPayload`.
- Ajouter l'endpoint `GET /commercants/me/contact`.
- Ajouter l'action menu front `Mes informations`.
- Ajouter l'écran front de consultation.
- Ajouter les tests API et front.

Definition of done :

- Un commerçant connecté peut consulter ses informations de contact sans passer par le back-office.

### Backlog priorise / Story `PRD-052` - Modifier ses informations de contact

Priorite : `P1`
Statut : `À faire`

Valeur métier : permettre au commerçant de maintenir à jour ses coordonnées de contact.

Criteres d'acceptation :

- Un endpoint `PATCH /commercants/me/contact` accepte les champs `prenom`, `nom`, `email`, `telephone`.
- La route est protégée par session commerçant.
- Le backend valide email et téléphone.
- Le backend normalisé les champs texte.
- Le backend persiste les modifications.
- Le backend retourne le contact mis à jour.
- Une trace d'audit `merchant.contact.updated` est produite.
- Le front affiche une confirmation après sauvegarde.

Taches :

- Ajouter le use case `MettreAJourContactCommercantConnecte`.
- Ajouter le schema `MettreAJourContactCommercantRequest`.
- Ajouter la methode repository de mise à jour contact.
- Ajouter l'endpoint `PATCH /commercants/me/contact`.
- Ajouter le formulaire front d'edition.
- Ajouter les tests de validation, autorisation et audit.

Definition of done :

- Un commerçant connecté peut modifier ses informations de contact et voir les nouvelles valeurs immédiatement.

### Proposition de tickets implémentables

- `EP11-T01` Ajouter le use case backend de consultation contact commerçant connecté.
- `EP11-T02` Ajouter le use case backend de mise à jour contact commerçant connecté.
- `EP11-T03` Ajouter les schemas API contact commerçant.
- `EP11-T04` Ajouter `GET /commercants/me/contact`.
- `EP11-T05` Ajouter `PATCH /commercants/me/contact`.
- `EP11-T06` Ajouter l'audit `merchant.contact.updated`.
- `EP11-T07` Ajouter les tests API backend.
- `EP11-T08` Ajouter l'entrée front `Mes informations`.
- `EP11-T09` Ajouter l'écran front lecture/edition contact.
- `EP11-T10` Ajouter la gestion des erreurs et expiration de session côté front.
- `EP11-T11` Mettre à jour `api/localeo-openapi.json`.
- `EP11-T12` Mettre à jour la documentation produit.

### Questions ouvertes

- L'email de contact doit-il être unique entre commerçants ?
- Le téléphone doit-il être obligatoire pour tous les commerçants ?
- Une modification d'email doit-elle envoyer une notification a l'ancien email, au nouvel email, ou aux deux ?
- Souhaite-t-on exposer aussi les informations publiques du commerce dans cette epic, ou les garder pour une epic distincte ?
- Les modifications de contact doivent-elles être visibles/modérables dans SQLAdmin avec un historique détaillé ?
