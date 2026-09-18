# Epic 41 — Évolutions de l’application commerçant

## 1. Objet

Cette spécification décrit les évolutions à apporter à l’application commerçant Localeo pour prendre en charge les animations locales, sans modifier le parcours historique de validation des coffrets.

Le commerçant doit pouvoir utiliser un scanner unique, reconnaître un QR de coffret ou un QR personnel de participant à une animation, confirmer l’action adaptée et obtenir un résultat immédiatement compréhensible. Il doit également pouvoir consulter les animations auxquelles son commerce participe et être informé lorsqu’il est inclus dans une nouvelle animation.

Le backend Animation correspondant est implémenté. L’évolution de l’application reste un lot coordonné distinct, conformément aux arbitrages `ARB-47` et `ARB-57`.

## 2. Résultat attendu

À partir de l’espace commerçant authentifié :

1. le commerçant ouvre l’action `Scanner un QR` ;
2. l’application lit le QR sans interpréter ni afficher son secret ;
3. elle détermine le parcours `COFFRET` ou `ANIMATION` ;
4. elle affiche un écran de confirmation adapté ;
5. elle appelle exclusivement l’API correspondant au type détecté ;
6. elle présente le succès, le rejeu ou l’erreur métier ;
7. elle permet d’enchaîner avec un nouveau scan.

## 3. Décisions déjà validées

| Décision | Conséquence pour l’application |
| --- | --- |
| QR coffret et QR participant distincts | Aucun appel de validation coffret avec un token Animation, et inversement. |
| Identité du commerçant issue de la session | Aucun `commercant_id` n’est envoyé par le frontend. |
| Scope `commercant:validation` | Le bouton de scan est indisponible si la session ne possède pas ce scope. |
| Token participant opaque et sans PII | L’application ne décode jamais le token et ne le journalise pas. |
| Validation idempotente | Un retry réseau ne doit pas produire une seconde validation effective. |
| Contrôle de l’étape côté serveur | Le backend vérifie que le commerçant authentifié participe à l’animation. |
| Première version non déployée | Les deux parcours QR sont livrés ensemble, sans mécanisme de rétrocompatibilité. |
| Déploiement par commune | La rubrique Animation est visible uniquement si Localeo Animation est activé pour la commune active du commerce. |
| Inclusion à une animation | L’ajout effectif du commerce à une animation produit une notification idempotente adressée au commerçant. |

## 4. Périmètre fonctionnel

### 4.1 Inclus

- scanner unique depuis l’accueil ou la rubrique Validations ;
- détection du parcours QR ;
- maintien du parcours coffret existant ;
- résolution d’un QR participant Animation ;
- présentation de l’animation, du participant masqué et de l’étape du commerce ;
- confirmation de validation ;
- gestion du doublon et des retries ;
- affichage de la progression retournée lorsqu’elle est disponible ;
- erreurs actionnables ;
- télémétrie sans token ni PII ;
- activation maîtrisée par feature flag pendant la recette initiale.
- rubrique `Animations` affichée uniquement dans une commune où Localeo Animation est déployé ;
- liste des animations auxquelles le commerce connecté participe ;
- détail en lecture seule d’une animation et statut de l’étape du commerce ;
- notification lors de l’inclusion du commerce dans une animation ;
- ouverture de l’animation concernée depuis la notification.

### 4.2 Hors périmètre

- inscription d’un participant depuis l’application commerçant ;
- modification ou suppression d’un participant ;
- annulation d’une validation Animation par le commerçant au MVP ;
- consultation de la liste complète des participants ;
- tirage, gains, bilan ou gestion de l’animation ;
- validation hors ligne ou mise en file locale d’un scan ;
- décodage local des signatures ou secrets QR.

## 5. Navigation et écrans

### 5.0 Disponibilité de la rubrique Animation

Après authentification et à chaque changement de commune active, l’application récupère les capacités fonctionnelles du contexte commerçant. La rubrique `Animations` et ses raccourcis ne sont rendus que si `animation_locale_disponible=true`.

Cette valeur est une décision backend fondée sur l’activation du service Localeo Animation pour la commune. Elle ne doit jamais être déduite d’une liste vide : une commune équipée peut ne disposer d’aucune animation à cet instant.

Lorsque `animation_locale_disponible=false` :

- aucun onglet, bloc d’accueil, badge ou raccourci Animation n’est visible ;
- l’application ne charge ni la liste ni les notifications Animation ;
- un lien profond Animation affiche un écran fonctionnel indisponible puis revient vers l’accueil ;
- le scanner Coffret reste disponible ; si un QR Animation est néanmoins scanné, le backend refuse l’action et l’application indique que le service n’est pas disponible dans cette commune.

### 5.1 Point d’entrée

Le bouton principal reste `Scanner un QR`. Il ne faut pas créer deux scanners concurrents. Une aide courte indique : « Coffret ou animation Localeo ».

### 5.2 États du parcours

| État | Contenu principal | Action |
| --- | --- | --- |
| `CAMERA` | Viseur, permission caméra, saisie manuelle de secours si déjà disponible | Scanner |
| `ANALYSE` | Indicateur bref, interaction verrouillée | Aucune |
| `CONFIRMATION_COFFRET` | Parcours existant inchangé | Continuer vers la prestation |
| `CONFIRMATION_ANIMATION` | Nom de l’animation, participant masqué, étape/commerce, statut de l’étape | Confirmer la validation |
| `SUCCES_ANIMATION` | Animation, participant masqué, heure, progression si disponible | Scanner un autre QR |
| `DEJA_VALIDEE` | Information non bloquante : étape déjà enregistrée | Fermer ou scanner à nouveau |
| `ERREUR` | Message actionnable et identifiant de corrélation | Réessayer ou fermer |

### 5.3 Écran de confirmation Animation

Afficher uniquement :

- nom de l’animation ;
- commune ;
- référence participant pseudonymisée ou nom abrégé ;
- nom du commerce connecté ;
- intitulé `Étape chez votre commerce` ;
- état `À valider` ou `Déjà validée` ;
- bouton principal `Valider cette étape`.

Ne pas afficher l’email, le téléphone, le token, l’identifiant technique ou le QR sous forme textuelle.

### 5.4 Liste `Mes animations`

La rubrique présente uniquement les animations auxquelles le commerce de la session est effectivement rattaché. Elle ne doit pas exposer les animations simplement publiées dans la commune.

Les vues proposées sont :

- `À venir` : animation publiée dont la période n’a pas commencé ;
- `En cours` : animation publiée et dans sa période active ;
- `Terminées` : animation clôturée ou dont la date de fin est passée.

Chaque ligne affiche le nom, la commune, le type, les dates, le statut, le rôle ou l’étape du commerce et, si disponible, le nombre de validations réalisées chez ce commerce. Une liste vide affiche un état dédié sans masquer la rubrique.

Le détail est en lecture seule et présente la description, les dates, les consignes, l’étape du commerce, les validations agrégées et les contacts utiles. Il n’expose jamais la liste nominative des participants.

### 5.5 Centre de notifications

Une notification `ANIMATION_COMMERCANT_INCLUS` contient le nom de l’animation, la commune, sa période et un lien profond vers son détail. Elle peut être marquée comme lue ou non lue et contribue au badge non lu de l’application. Le commerçant peut également la retirer de son inbox ; cette suppression est logique afin de conserver la traçabilité technique de sa diffusion.

La notification est créée une seule fois pour le couple `(animation_id, commercant_id)`, au moment où l’inclusion devient effective. Une sauvegarde répétée de la configuration ne doit pas la dupliquer. Si le commerçant est retiré puis réintégré, une nouvelle notification n’est produite que si le backend crée une nouvelle occurrence d’inclusion auditée.

Le canal obligatoire est l’inbox persistante de l’application. Une notification WebPush est envoyée si l’appareil est abonné et si la préférence correspondante est active. L’email peut être activé comme canal de repli selon les préférences de notification du commerçant. Aucun message ne doit être envoyé tant que l’animation est encore un brouillon non destinée à être communiquée ; l’envoi intervient à la publication ou lors d’une inclusion dans une animation déjà publiée.

### 5.6 Inventaire des nouveaux écrans

| ID écran | Intitulé | Route frontend indicative | API principale | Visibilité |
| --- | --- | --- | --- | --- |
| `COM-ANI-ACCUEIL` | Bloc Animation de l’accueil | `/` | `GET /protected/animation-locale/commercants/me/contexte` | Uniquement si `animation_locale_disponible=true` |
| `COM-ANI-LISTE` | Mes animations | `/animations` | `GET /protected/animation-locale/commercants/me/animations` | Uniquement si le module est disponible |
| `COM-ANI-DETAIL` | Détail et suivi d’une animation | `/animations/{animation_id}` | `GET /protected/animation-locale/commercants/me/animations/{animation_id}` | Commerce rattaché uniquement |
| `COM-ANI-INBOX` | Notifications Animation | `/notifications?categorie=animation` | `GET /protected/animation-locale/commercants/me/notifications` | Uniquement si le module est disponible |
| `COM-ANI-INDISPONIBLE` | Animation indisponible | Écran technique sans route permanente | Contexte ou réponse `404` | Lien profond devenu inaccessible |

### 5.7 Bloc Animation sur l’accueil

Le bloc donne un accès rapide au suivi sans concurrencer l’action principale `Scanner un QR`.

Contenu :

- titre `Mes animations` ;
- compteur des animations en cours ;
- prochaine animation à venir, si elle existe ;
- compteur de notifications non lues ;
- action `Voir mes animations` ;
- action secondaire `Voir les notifications` uniquement en présence d’au moins une notification.

```text
┌──────────────────────────────────────┐
│ Mes animations                  (2)  │
│ 1 animation en cours                 │
│ Prochaine : Passeport gourmand       │
│ Du 25 août au 15 septembre           │
│                                      │
│ [Voir mes animations]  1 nouveauté   │
└──────────────────────────────────────┘
```

Le bloc n’est pas rendu tant que le contexte n’est pas chargé. Il ne doit pas apparaître brièvement puis disparaître dans une commune non équipée. Pendant le chargement initial, utiliser un squelette neutre de l’accueil, sans libellé Animation.

### 5.8 Écran `Mes animations`

#### 5.8.1 En-tête et filtres

L’en-tête contient :

- bouton retour ou navigation principale ;
- titre `Mes animations` ;
- texte d’aide `Les animations auxquelles votre commerce participe` ;
- badge de notifications non lues ;
- onglets `En cours`, `À venir`, `Terminées` avec compteurs lorsqu’ils sont connus.

La catégorie d’affichage est dérivée des dates et du statut retournés :

| Catégorie UI | Règle |
| --- | --- |
| `À venir` | Statut publié et `date_debut` postérieure à maintenant |
| `En cours` | Statut `PUBLIEE` ou `EN_COURS` et instant courant compris entre les dates |
| `Terminées` | Statut `CLOTUREE`, `ARCHIVEE` ou `ANNULEE`, ou date de fin passée |

Les onglets sont des filtres de présentation. Ils ne modifient jamais l’appartenance du commerce à l’animation.

#### 5.8.2 Carte d’animation

Chaque carte affiche :

- visuel ou pictogramme du type d’animation ;
- nom de l’animation ;
- commune ;
- période au format local ;
- badge de statut utilisateur ;
- intitulé de l’étape du commerce ;
- nombre de validations effectuées chez ce commerce ;
- action `Voir le détail`.

```text
┌──────────────────────────────────────┐
│ [visuel] Passeport gourmand          │
│ Annecy · En cours                    │
│ 25 août — 15 septembre               │
│ Étape chez votre commerce            │
│ 18 validations réalisées             │
│                         [Voir détail] │
└──────────────────────────────────────┘
```

La carte entière peut être interactive, mais l’action doit conserver un libellé accessible. Aucun nom, email, téléphone ou identifiant de participant n’apparaît dans la liste.

#### 5.8.3 États de la liste

| État | Présentation | Action |
| --- | --- | --- |
| Chargement initial | 3 squelettes de cartes | Aucune |
| Rafraîchissement | Contenu conservé avec indicateur discret | Aucune |
| Liste vide globale | `Votre commerce ne participe encore à aucune animation` | Retour accueil |
| Onglet vide | `Aucune animation dans cette catégorie` | Changer d’onglet |
| Erreur récupérable | Message court et `Réessayer` | Relancer la même requête |
| Session expirée | Parcours de reconnexion existant | Reprendre la route demandée |
| Module désactivé entre deux requêtes | Purger les données locales et quitter la rubrique | Retour accueil |

La pagination se déclenche par bouton `Afficher plus` ou chargement progressif accessible. Le changement d’onglet replace le focus sur le titre de la liste et revient en première page.

### 5.9 Écran de détail et suivi d’une animation

L’écran est strictement en lecture seule. Il aide le commerçant à comprendre l’animation et à suivre son activité, sans lui donner accès au pilotage partenaire.

#### 5.9.1 En-tête

- bouton retour vers `Mes animations` ;
- nom de l’animation ;
- badge `À venir`, `En cours`, `Terminée` ou `Annulée` ;
- commune et période ;
- type d’animation.

#### 5.9.2 Sections

| Section | Contenu |
| --- | --- |
| Présentation | Description publique de l’animation |
| Votre participation | Nom de l’étape, rôle du commerce et consignes opérationnelles |
| Suivi chez votre commerce | Nombre total de validations réalisées, dernière activité si disponible |
| Période | Dates de début et de fin, avec état temporel explicite |
| Besoin d’aide | Contact ou accès au support Localeo existant |

```text
┌──────────────────────────────────────┐
│ ← Mes animations                     │
│ Passeport gourmand       [En cours]  │
│ Annecy · 25 août — 15 septembre      │
├──────────────────────────────────────┤
│ Présentation                         │
│ Découvrez les commerces locaux…      │
├──────────────────────────────────────┤
│ Votre participation                  │
│ Étape chez votre commerce            │
│ Scannez le QR présenté par le client │
├──────────────────────────────────────┤
│ Suivi chez votre commerce            │
│ 18 validations réalisées             │
├──────────────────────────────────────┤
│ [Scanner un QR]        [Aide]         │
└──────────────────────────────────────┘
```

Le bouton `Scanner un QR` est visible uniquement pendant une période permettant les validations. Il ouvre le scanner commun et ne préremplit jamais un participant. Pour une animation à venir, terminée ou annulée, le bouton est remplacé par une information expliquant pourquoi aucune validation n’est possible.

Une réponse `404` signifie que l’animation n’est plus accessible au commerce, qu’elle appartient à une autre commune ou que le module a été désactivé. L’application supprime alors la fiche de son cache et affiche `Cette animation n’est plus disponible pour votre commerce`.

### 5.10 Écran des notifications Animation

L’application peut réutiliser le centre de notifications existant en ajoutant une catégorie `Animations`. Il ne faut pas créer deux inbox concurrentes.

Chaque entrée affiche :

- état lu/non lu ;
- icône Animation ;
- titre ;
- message ;
- date relative, complétée par une date absolue accessible ;
- action implicite vers l’animation.

```text
┌──────────────────────────────────────┐
│ Notifications · Animations           │
├──────────────────────────────────────┤
│ ● Vous participez à une animation    │
│   Votre commerce est inclus dans     │
│   Passeport gourmand · il y a 2 h    │
├──────────────────────────────────────┤
│   Vous participez à une animation    │
│   Marché de Noël · 12 janvier        │
└──────────────────────────────────────┘
```

À l’ouverture d’une entrée, l’application marque la notification comme lue puis ouvre son `action_cible`. Si le marquage échoue mais que le détail reste autorisé, la navigation continue et le badge sera réconcilié au prochain chargement. Un lien profond WebPush suit le même parcours après restauration ou vérification de la session.

### 5.11 Écran `Animation indisponible`

Cet écran transitoire est réservé aux liens profonds, favoris ou notifications devenus invalides. Il ne constitue pas une rubrique visible.

Contenu :

- pictogramme informatif ;
- titre `Animation indisponible` ;
- message `Localeo Animation n’est pas disponible pour votre commerce dans cette commune` ou `Cette animation n’est plus accessible` selon le contexte connu ;
- action principale `Retour à l’accueil` ;
- aucune action commerciale ou proposition d’abonnement au commerçant.

L’écran ne révèle ni l’existence d’une animation d’un autre commerce, ni le nom d’un partenaire, ni la cause administrative de la désactivation.

### 5.12 Navigation et rafraîchissement

```text
Accueil
  └─ Mes animations
       ├─ Liste filtrée
       │    └─ Détail animation
       │          └─ Scanner un QR
       └─ Notifications Animation
             └─ Détail animation
```

- le contexte est chargé après authentification et après toute modification du commerce ou de la commune active ;
- la liste est rafraîchie à l’ouverture, au retour au premier plan et après une validation réussie ;
- le détail peut être rafraîchi par geste ou action explicite ;
- le compteur de notifications est réconcilié après lecture et au retour au premier plan ;
- tout passage de `animation_locale_disponible=true` à `false` purge immédiatement listes, détails et notifications Animation du cache local.

### 5.13 Responsive et accessibilité des écrans de suivi

- une colonne sur mobile ; deux colonnes maximum pour les cartes sur tablette ou écran large ;
- largeur de lecture du détail limitée pour conserver des lignes lisibles ;
- zones interactives d’au moins 44 × 44 px ;
- ordre de focus : retour, titre, statut, contenu, actions ;
- badges toujours accompagnés d’un libellé textuel ;
- compteurs annoncés avec leur sens, par exemple `18 validations réalisées` ;
- squelettes ignorés par les lecteurs d’écran et chargement annoncé une seule fois ;
- aucune actualisation ne déplace automatiquement le focus ;
- dates rendues dans le fuseau local de la commune et accompagnées de l’année lorsque nécessaire.

## 6. Reconnaissance des QR

### 6.1 QR participant Animation

Le QR contient une URL complète issue de `LOCALEO_ANIMATION_PARTICIPANT_URL_TEMPLATE` :

```text
{LOCALEO_ANIMATION_PARTICIPANT_URL_TEMPLATE}
```

L’application accepte uniquement une origine Localeo autorisée et le chemin `/participants/{token}`. Elle extrait le token en mémoire pour les appels API, sans le persister dans les logs, analytics, crash reports ou historique de navigation.

### 6.2 QR coffret

Le format signé historique reste pris en charge par le parcours coffret existant. L’application ne tente pas de décoder ou de vérifier sa signature localement ; elle transmet la valeur au backend Coffret.

### 6.3 Algorithme de routage

```text
si valeur = URL HTTPS d’une origine Localeo autorisée
   et chemin = /participants/{token}
      alors type = ANIMATION
sinon
      type = COFFRET_LEGACY
```

Toute URL absolue d’une origine non autorisée est rejetée localement comme QR non reconnu. Aucun fallback Coffret ne doit transmettre une URL externe au backend.

## 7. Authentification

L’application réutilise l’authentification et la session commerçant existantes. La connexion crée la session :

```http
POST /protected/identite-acces/commercants/auth/login
```

Les appels de résolution et de validation suivants utilisent ensuite :

```http
Authorization: Bearer <session_token>
```

La session doit contenir le scope `commercant:validation`. Les réponses `401` provoquent le renouvellement ou la reconnexion. Les réponses `403` affichent un écran d’accès insuffisant et ne doivent pas déclencher de boucle de retry.

## 8. Contrats API

### 8.0 Contexte fonctionnel du commerce

Contrat à exposer ou à intégrer au payload de session existant :

```http
GET /protected/animation-locale/commercants/me/contexte
Authorization: Bearer <session_token>
```

```json
{
  "commercant_id": "uuid",
  "commune_id": "uuid",
  "animation_locale_disponible": true,
  "permissions": ["animation:lire", "animation:valider"],
  "notifications_non_lues": 1
}
```

La réponse est recalculée côté serveur depuis la commune active, l’abonnement ou l’activation du module et les habilitations du commerce. Une commune inexistante dans la session ou un module non activé retourne `animation_locale_disponible=false`, sans révéler les données d’une autre commune.

### 8.1 Parcours coffret existant

| Étape | API |
| --- | --- |
| Ouvrir la transaction | `POST /protected/exploitation/validation/ouvrir-transaction` |
| Valider la prestation sélectionnée | `POST /protected/exploitation/validation/valider-prestation` |

Ce parcours reste inchangé et constitue un test de non-régression obligatoire.

### 8.2 Résoudre le QR participant — contrat immédiatement utilisable

```http
GET /public/animation-locale/participants/{participant_token}
```

La réponse fournit l’animation, le participant masqué et les étapes. L’application sélectionne l’étape dont `commercant_id` correspond au commerce de la session.

Si aucune étape ne correspond, l’application ne propose pas la validation. Le backend effectuera de nouveau ce contrôle lors de la commande.

### 8.3 Valider une étape Animation

```http
POST /protected/animation-locale/validations
Authorization: Bearer <session_token>
Idempotency-Key: <uuid-ou-ulid-stable-pour-la-tentative>
Content-Type: application/json

{
  "qr_token": "token-opaque-extrait-du-qr",
  "etape_id": "uuid-etape-retourne-par-la-resolution"
}
```

Réponse nominale actuelle :

```json
{
  "id": "uuid-validation",
  "animation_id": "uuid-animation",
  "participant_id": "uuid-participant",
  "commercant_id": "uuid-commercant",
  "etape_id": "uuid-etape",
  "statut": "VALIDEE",
  "validated_at": "2026-08-20T10:30:00Z",
  "annulation_motif": null
}
```

La même `Idempotency-Key` doit être réutilisée pour tous les retries techniques d’une tentative. Un nouveau scan confirmé crée une nouvelle clé.

## 9. Évolutions backend recommandées pour l’application

Ces évolutions ne bloquent pas une première intégration, mais évitent au frontend de composer un contrat public et améliorent fortement le retour utilisateur.

### 9.1 Résolution protégée du scan

Contrat recommandé :

```http
POST /protected/animation-locale/scans/resoudre
Authorization: Bearer <session_token>

{
  "valeur_qr": "https://.../participants/token"
}
```

Réponse cible :

```json
{
  "type": "ANIMATION_PARTICIPANT",
  "animation": {"id": "uuid", "nom": "Passeport gourmand", "commune": "Annecy"},
  "participant": {"reference": "PART-0247", "nom_affiche": "Alice D."},
  "etape": {"id": "uuid", "statut": "A_VALIDER"},
  "action_autorisee": true,
  "raison_blocage": null
}
```

Le backend dérive le commerçant depuis la session et ne retourne que les données utiles à la confirmation.

### 9.2 Réponse de validation enrichie

Ajouter de manière compatible :

```json
{
  "progression": 60,
  "nombre_validations": 3,
  "nombre_validations_requises": 5,
  "participant_qualifie": false,
  "idempotent_replay": false,
  "deja_validee": false
}
```

À terme, `etape_id` pourra devenir optionnel : le backend peut le dériver du couple animation/commerçant après résolution du token.

### 9.3 Animations du commerce

```http
GET /protected/animation-locale/commercants/me/animations?statut=EN_COURS&page=1&page_size=20
GET /protected/animation-locale/commercants/me/animations/{animation_id}
```

Le commerçant est toujours dérivé de la session. La liste est filtrée par la commune active et par l’existence d’un rattachement effectif dans `animation_commercants`. Le détail retourne `404` si le commerce n’est pas rattaché à l’animation et `403` si la commune demandée sort du tenant actif.

Le payload de liste fournit au minimum `id`, `nom`, `description_courte`, `type`, `commune`, `date_debut`, `date_fin`, `statut`, `etape_commercant`, `nombre_validations` et `detail_url`.

### 9.4 Notifications du commerce

```http
GET  /protected/animation-locale/commercants/me/notifications?lue=false
POST /protected/animation-locale/commercants/me/notifications/{notification_id}/lire
POST /protected/animation-locale/commercants/me/notifications/{notification_id}/non-lire
DELETE /protected/animation-locale/commercants/me/notifications/{notification_id}
```

Les trois mutations sont idempotentes et ne peuvent cibler qu'une notification du commerce authentifié. `non-lire` remet `lue_at` à `null`. `DELETE` renseigne `supprimee_at` sans supprimer physiquement la ligne ; une notification supprimée disparaît des listes et du compteur non lu.

La publication d’une animation crée les notifications pour les commerces déjà inclus. L’ajout ultérieur d’un commerce à une animation publiée crée immédiatement la sienne. La création s’appuie sur une clé d’idempotence métier stable et sur l’outbox existante afin d’éviter pertes et doublons entre inbox, WebPush et email.

Événement interne attendu :

```json
{
  "type": "ANIMATION_COMMERCANT_INCLUS",
  "animation_id": "uuid",
  "commercant_id": "uuid",
  "commune_id": "uuid",
  "inclusion_id": "uuid",
  "occurred_at": "2026-08-20T10:30:00Z"
}
```

## 10. Règles métier et UX

| Situation | Comportement attendu |
| --- | --- |
| Étape valide | Afficher le succès et la progression disponible. |
| Même étape déjà validée | Ne pas présenter une erreur rouge ; afficher `Étape déjà validée`. |
| QR participant expiré ou révoqué | Demander au participant de faire renvoyer son QR. |
| Animation non publiée, clôturée ou hors période | Expliquer que l’animation n’accepte plus de validation. |
| Commerce absent de l’animation | Indiquer que cette étape ne concerne pas ce commerce. |
| Module Animation non déployé dans la commune | Masquer la rubrique et refuser tout accès direct aux données Animation. |
| Module déployé mais aucune animation rattachée | Afficher l’état vide `Aucune animation pour votre commerce`. |
| Commerce inclus dans une animation publiée | Créer une seule notification et ouvrir le détail depuis son lien profond. |
| Cadence de scan anormale | Afficher `Validation en cours de contrôle` si le statut retourné est `ANOMALIE`. |
| Session expirée | Conserver l’intention en mémoire, reconnecter, puis demander une nouvelle confirmation. |
| Réseau indisponible | Ne pas valider hors ligne ; proposer de réessayer avec la même clé d’idempotence. |

## 11. Mapping des erreurs

| HTTP | Message utilisateur | Retry |
| ---: | --- | --- |
| `400` / `422` | QR ou demande non reconnu | Non, nouveau scan |
| `401` | Votre session a expiré | Après reconnexion |
| `403` | Vous n’êtes pas autorisé à valider cette étape | Non |
| `404` | Participation introuvable | Non |
| `409` | Validation impossible dans l’état actuel de l’animation | Selon le détail métier |
| `410` | Ce QR n’est plus valide | Non, renvoi du QR |
| `429` | Trop de scans rapprochés, patientez un instant | Oui, temporisé |
| `5xx` | Service momentanément indisponible | Oui, même clé d’idempotence |

L’application affiche le `correlationId` dans la zone de détail/support, jamais le token QR.

## 12. Sécurité et confidentialité

- liste blanche stricte des origines QR Localeo ;
- aucune navigation automatique vers l’URL scannée ;
- aucun token dans les logs, analytics, breadcrumbs, notifications ou stockage permanent ;
- token conservé en mémoire uniquement pendant le parcours ;
- HTTPS obligatoire hors développement ;
- validation finale exclusivement côté backend ;
- aucun `commercant_id`, `participant_id` ou statut calculé par le client ne fait autorité ;
- nettoyage de l’écran et du token à la fermeture, au logout et au passage prolongé en arrière-plan ;
- masquage des données participant dans les captures de diagnostic.

## 13. Résilience et concurrence

- une tentative possède une seule `Idempotency-Key` ;
- double tap : bouton désactivé dès le premier envoi ;
- timeout : proposer `Réessayer`, sans générer une nouvelle clé ;
- retour arrière avant succès : demander confirmation avant abandon ;
- reprise après fermeture de l’application : nouveau scan obligatoire ;
- aucune file de validations hors ligne, car le statut de l’animation et l’éligibilité doivent être vérifiés en temps réel.

## 14. Observabilité

Événements autorisés, sans PII ni secret :

- `merchant_scan_started` ;
- `merchant_scan_type_detected` avec `type=COFFRET|ANIMATION|UNKNOWN` ;
- `merchant_animation_scan_resolved` ;
- `merchant_animation_validation_confirmed` ;
- `merchant_animation_validation_succeeded` ;
- `merchant_animation_validation_replayed` ;
- `merchant_animation_validation_failed` avec code HTTP/code métier ;
- `merchant_animation_list_viewed` ;
- `merchant_animation_detail_viewed` ;
- `merchant_animation_inclusion_notification_opened` ;
- `merchant_animation_feature_hidden` avec motif non sensible ;
- `merchant_scan_abandoned`.

Mesurer taux de résolution, taux de succès, délais, erreurs par version d’application et part de QR inconnus. Ne jamais envoyer la valeur scannée.

## 15. Accessibilité et compatibilité

- bouton de validation d’au moins 44 px ;
- contraste WCAG AA ;
- retour texte et visuel, pas uniquement couleur ou vibration ;
- lecteur d’écran annonçant le type de QR et le résultat ;
- permission caméra explicable et récupérable depuis les réglages ;
- prise en charge des appareils actuellement supportés par l’application commerçant ;
- affichage portrait prioritaire, mais confirmation utilisable en paysage.

## 16. Déploiement

1. livrer derrière un feature flag `animation_validation_enabled` ;
2. publier le backend avant l’application ;
3. activer sur un groupe pilote de commerces participants ;
4. vérifier télémétrie, erreurs et non-régression Coffret ;
5. généraliser progressivement.

L’application n’étant pas encore déployée, la première version publiée embarque directement les parcours Coffret et Animation. Aucun fallback ni contrôle de version minimale n’est requis.

## 17. Découpage proposé

| Lot | Contenu | Dépendances | Critère de sortie |
| --- | --- | --- | --- |
| `COM-0` | Feature flag de recette et télémétrie sans token | Configuration | Fonction masquée et mesurable |
| `COM-1` | Scanner unique et routage QR Coffret/Animation | `ARB-47` | Aucun impact sur les coffrets |
| `COM-2` | Résolution et écran de confirmation Animation | API participant actuelle ou résolution protégée | Étape du commerce affichée |
| `COM-3` | Validation, idempotence, succès, doublon et erreurs | `POST /validations` | Parcours E2E nominal et retries |
| `COM-4` | Accessibilité, pilote, support et déploiement progressif | Backend publié et commerce pilote | Recette terrain validée |
| `COM-5` | Capacité Animation par commune et navigation conditionnelle | Activation/abonnement commune | Rubrique absente si le module n’est pas déployé |
| `COM-6` | Liste et détail en lecture seule des animations du commerce | APIs `/commercants/me/animations` | À venir, en cours et terminées couvertes |
| `COM-7` | Notification d’inclusion, inbox, badge et lien profond | Outbox et préférences de notification | Une inclusion produit une notification unique |

## 18. Critères d’acceptation

- [ ] Le scanner reconnaît un QR participant Animation sans casser un QR coffret.
- [ ] Une origine externe n’est jamais ouverte ni transmise au backend.
- [ ] Le commerce et l’étape sont dérivés et contrôlés depuis la session/backend.
- [ ] Une validation nominale n’est créée qu’une fois.
- [ ] Un retry réseau réutilise la même clé d’idempotence.
- [ ] Une étape déjà validée produit un état informatif, pas un faux échec.
- [ ] Une animation clôturée, hors période ou étrangère au commerce est refusée proprement.
- [ ] Aucun token ou PII n’apparaît dans les logs et analytics.
- [ ] Le parcours Coffret passe intégralement ses tests de non-régression.
- [ ] Les tests caméra, faible réseau, double tap, session expirée et reprise sont couverts.
- [ ] La rubrique Animation est invisible si le module n’est pas activé pour la commune active.
- [ ] Une commune équipée sans animation affiche un état vide, et non une rubrique masquée.
- [ ] Seules les animations auxquelles le commerce est rattaché sont listées et consultables.
- [ ] Le changement de commune active recalcule la disponibilité et vide les données Animation précédentes.
- [ ] Une inclusion dans une animation publiée crée exactement une notification persistante.
- [ ] Une inclusion préparée dans un brouillon est notifiée au moment de la publication, sans doublon.
- [ ] Le lien profond de la notification ouvre le détail autorisé de l’animation.
- [ ] Les préférences WebPush/email sont respectées sans empêcher la création de l’inbox.

## 19. Matrice de tests minimale

| Cas | Attendu |
| --- | --- |
| QR coffret valide | Parcours coffret historique |
| QR participant valide et étape ouverte | Confirmation puis succès Animation |
| QR participant déjà validé | État `Déjà validée`, aucun doublon |
| QR d’un autre commerce | Refus métier |
| QR expiré/révoqué | Message de renvoi du QR |
| Animation avant début/après fin/clôturée | Refus métier explicite |
| Double validation simultanée | Une seule validation effective |
| Timeout après envoi | Retry idempotent |
| QR URL externe | Rejet local |
| Session sans scope | `403`, aucune commande |
| Mode avion | Aucun stockage de validation, retry manuel |
| Commune sans Localeo Animation | Aucun élément de navigation Animation et aucun chargement API métier |
| Commune équipée, liste vide | Rubrique visible avec état vide |
| Animation publiée sans rattachement du commerce | Absente de la liste et détail inaccessible |
| Inclusion avant publication | Une notification émise à la publication |
| Inclusion après publication | Une notification émise immédiatement |
| Sauvegarde répétée de la même inclusion | Aucune notification supplémentaire |
| Changement vers une commune non équipée | Cache Animation purgé et rubrique masquée |

## 20. Définition de terminé

L’évolution est terminée lorsque les lots `COM-0` à `COM-7` sont validés, que la recette bout en bout couvre au moins un commerce pilote, une animation publiée, une commune équipée et une commune non équipée, que la notification d’inclusion est idempotente, que les journaux ont été contrôlés pour l’absence de token/PII et que le parcours Coffret ne présente aucune régression.
