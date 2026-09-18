# Backlog Epic 57 - Bornage et pagination des API Marketplace

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC. L’ancien numéro local « Marketplace 53 » désigne cette EPIC 57, distincte de la tombola (EPIC 53).

## Synthese

- Criticite : `Haute`.
- Statut : `Termine`.
- Objectif : garantir qu'aucune surface Marketplace ou Localeo Live ne puisse charger une liste non bornee, tout en conservant une experience rapide et progressive.
- Dependances : Epic 16 `Feed d'activite locale`, Epic 42 `Localeo Live`, Epic 49 `Animations Marketplace` et Epic 52 `Accueil contextualise`.
- Hors perimetre : pagination des ecrans d'administration, exports complets, traitements batch et changement des regles d'eligibilite metier.

## Probleme

Plusieurs routes de liste sont consommees sans pagination explicite ou avec une limite uniquement choisie par le frontend. Cette situation presente quatre risques :

- augmentation progressive du poids des reponses avec le nombre de communes, coffrets, commercants ou signaux ;
- ralentissement du premier affichage et consommation inutile de donnees sur mobile ;
- multiplication d'appels unitaires pour enrichir une liste deja volumineuse ;
- possibilite pour un client d'envoyer une limite excessive si le backend ne force pas de plafond.

Le masquage ou le `slice` cote frontend ne constitue pas une protection suffisante : les donnees ont deja ete calculees, serialisees et transportees.

## Principes obligatoires

1. Toute route retournant une collection possede une taille par defaut et un maximum forces par le backend.
2. Le backend normalise une limite absente ou invalide et refuse ou borne une valeur excessive selon un contrat documente.
3. La pagination publique utilise un curseur opaque et stable plutot qu'un offset lorsque les donnees peuvent changer frequemment.
4. Le tri est applique avant la limite et comporte toujours un departage stable, par exemple `date_publication DESC, id DESC`.
5. La deduplication et les controles d'eligibilite sont appliques avant la limite.
6. Le frontend demande uniquement la quantite utile a la surface et n'accumule des pages qu'apres une action explicite.
7. Une reponse vide ou tronquee ne bloque jamais le reste de la page.
8. Les limites backend ne sont jamais supposees fiables uniquement parce que le frontend en envoie une.

## Contrat transverse recommande

### Parametres

- `limit` ou `page_size` : entier optionnel ;
- `cursor` : curseur opaque optionnel ;
- filtres metier propres a chaque route.

Les nouveaux contrats utilisent de preference `page_size`. Les routes existantes peuvent conserver `limit` pour compatibilite, sans accepter simultanement deux valeurs contradictoires.

### Reponse paginee

```json
{
  "items": [],
  "pagination": {
    "pageSize": 20,
    "nextCursor": null,
    "hasMore": false
  }
}
```

Regles :

- `pageSize` expose la taille effectivement appliquee par le backend ;
- `nextCursor` est opaque pour le frontend ;
- `hasMore` ne depend pas d'une comparaison fragile avec la taille recue ;
- le total global n'est retourne que s'il est disponible sans requete couteuse ;
- un curseur invalide produit une erreur fonctionnelle `400`, sans erreur serveur.

### Forcage backend

Pour chaque route, le backend applique :

```text
effective_limit = min(max(requested_limit || default_limit, 1), maximum_limit)
```

Le choix entre bornage silencieux et reponse `422` doit rester uniforme. Pour les routes publiques existantes, le bornage silencieux est recommande afin de conserver la compatibilite, avec journalisation technique de la valeur demandee.

## Matrice des API a optimiser

| Priorite | Route | Risque actuel | Defaut | Maximum | Evolution attendue |
|---|---|---|---:|---:|---|
| P0 | `POST /public/referencement/villes/proches/accueil` | Les cinq widgets peuvent grossir dans une reponse unique | Par widget | Par widget | Plafonds forces dans la projection |
| P0 | `GET /public/exploitation/activites-locales` | Limite choisie par le client et filtrage animation apres reception | 5 | 50 | Curseur stable et filtre `animation_id` |
| P0 | `GET /public/commercialisation/coffrets` | Liste non paginee, potentiellement enrichie avec les prestations | 20 | 50 | Pagination et projection legere par defaut |
| P0 | `GET /protected/referencement/commercants` | Tous les commercants d'une commune peuvent etre retournes | 30 | 50 | Pagination par curseur |
| P1 | `GET /public/referencement/villes` | Une recherche vide peut retourner toutes les communes | 20 | 50 | Recherche prefixee et pagination |
| P1 | `GET /public/gestion-achats/achats/{achat_id}/coffrets-instances` | Une commande professionnelle peut contenir de nombreuses instances | 50 | 100 | Pagination stable |
| P1 | `GET /public/animation-locale/animations` | Plusieurs clients utilisent des tailles differentes | 20 | 50 | Unifier `page_size`, maximum force |
| P1 | `GET /public/localeo-live/installations/{id}/notifications` | Accumulation historique des notifications | 30 | 50 | Conserver le curseur et forcer le maximum |
| P2 | `GET /public/exploitation/feedbacks-prestation/commentaires` | Un client externe peut demander un volume excessif | 3 | 20 | Maximum force |
| P2 | Resolution de la bibliotheque Localeo Live | Enrichissement par appels unitaires, risque N+1 | 30 references | 50 references | Ajouter une resolution groupee |

## Projection territoriale de l'accueil

Route :

```http
POST /public/referencement/villes/proches/accueil
```

Plafonds recommandes :

| Widget | Maximum retourne |
|---|---:|
| `coffretDuMoment` | 1 |
| `communesDisponibles` | 8 |
| `animationsProches` | 4 |
| `enCeMoment` | 5 |
| `derniersCoffretsAjoutes` | 6 |

Regles backend :

- filtrer l'eligibilite et dedupliquer avant d'appliquer les plafonds ;
- ordonner chaque widget avec une strategie stable documentee ;
- ne jamais exposer des listes intermediaires completes dans la reponse ;
- conserver les plafonds dans une configuration backend versionnee ;
- inclure facultativement `meta.limits` pour faciliter le diagnostic sans permettre au client de les augmenter.

Usage frontend :

- consommer directement l'ordre retourne ;
- ne pas lancer un appel par commune pour completer la projection ;
- appliquer un `slice` defensif uniquement comme protection de rendu ;
- ne pas afficher automatiquement plus de trois signaux `enCeMoment` sans action utilisateur.

## Feed et actualites d'animation

La page de detail d'une animation ne doit plus recuperer jusqu'a 50 activites communales pour les filtrer localement.

Contrat cible :

```http
GET /public/exploitation/activites-locales
    ?animation_id={uuid}
    &type_activite=ACTUALITE_ANIMATION
    &page_size=10
    &cursor={opaque}
```

Le backend doit :

- filtrer relationnellement sur `animation_id` ;
- retourner uniquement les actualites publiques de cette animation ;
- ordonner par `date_publication DESC, id DESC` ;
- appliquer un maximum de 20 actualites par page ;
- indexer le chemin de lecture correspondant ;
- ne jamais demander au frontend de filtrer par `ressource_id` apres reception.

Le frontend doit :

- demander 10 actualites au premier affichage ;
- ne charger la suite que si un CTA `Voir les actualites precedentes` est present ;
- dedupliquer par `id` lors de l'ajout d'une page ;
- masquer la section sans erreur bloquante lorsque la liste est vide ou indisponible.

## Coffrets et commercants d'une commune

Les listes de coffrets et commercants doivent etre paginees independamment.

### Projection legere

La liste des coffrets ne doit pas retourner toutes les prestations detaillees par defaut. Le contrat recommande distingue :

- projection `summary` pour les cartes : identite, image, prix, type, validite et compteurs ;
- projection `detail` pour une fiche coffret unique ;
- inclusion explicite et bornee des prestations uniquement lorsqu'elle est necessaire.

Exemple :

```http
GET /public/commercialisation/coffrets
    ?ville_id={uuid}
    &projection=summary
    &page_size=20
    &cursor={opaque}
```

Le frontend doit utiliser la projection `summary` pour la commune et le catalogue, puis la route de detail lors de l'ouverture d'un coffret.

Pour les commercants, le frontend demande une premiere page de 30 elements et propose une action explicite si une suite existe. Il ne doit pas charger toutes les pages en arriere-plan.

## Recherche des communes

La route `GET /public/referencement/villes` doit distinguer :

- autocompletion avec un prefixe d'au moins deux caracteres : maximum 10 suggestions ;
- catalogue ou selecteur complet : pagination de 20 elements ;
- recherche vide : ne jamais retourner silencieusement l'ensemble sans pagination.

Le frontend doit :

- attendre au moins deux caracteres pour une autocompletion ;
- conserver un debounce de 250 a 350 ms ;
- annuler la requete precedente lorsque la saisie change ;
- ne pas utiliser une recherche vide pour reconstruire un catalogue complet.

## Commandes professionnelles

La liste des instances d'une commande doit accepter `page_size` et `cursor`. Le curseur doit rester stable pendant les activations et envois d'e-mail.

Le frontend doit :

- afficher les 50 premieres instances ;
- charger la suite sur demande ou par pagination explicite ;
- mettre a jour localement une instance modifiee sans recharger toutes les pages ;
- conserver la reference d'achat et le token de gestion sur chaque requete paginee.

## Bibliotheque Localeo Live

Le chargement actuel peut provoquer une requete de detail par ressource sauvegardee. Une facade groupee est recommandee :

```http
POST /public/localeo-live/bibliotheque/resoudre
```

```json
{
  "references": [
    { "type": "COFFRET", "id": "uuid", "token": "opaque" },
    { "type": "PARTICIPATION", "id": "uuid", "token": "opaque" }
  ]
}
```

Contraintes :

- maximum 30 references par appel, maximum absolu 50 ;
- resultat individuel `RESOLU`, `EXPIRE`, `REVOQUE` ou `INTROUVABLE` ;
- aucune reference ou token dans les logs applicatifs ;
- aucune erreur individuelle ne fait echouer toute la reponse ;
- le frontend decoupe une bibliotheque plus grande en lots sequentiels et limite la concurrence.

## Observabilite et protections

Le backend mesure par route :

- taille demandee et taille effectivement retournee ;
- poids serialise de la reponse ;
- duree SQL et duree totale ;
- taux d'utilisation de `nextCursor` ;
- nombre de demandes superieures au maximum ;
- taux de reponses vides.

Alertes recommandees :

- reponse publique superieure a 500 Ko hors media ;
- P95 superieur a 500 ms pour une premiere page ;
- plus de 50 lignes retournees par une route publique standard ;
- augmentation anormale des appels de detail par page vue.

Les protections de debit HTTP restent complementaires : elles ne remplacent pas le bornage de la taille des reponses.

## Lots de realisation

| Lot | Priorite | Contenu | Sortie attendue |
|---|---|---|---|
| B0 | P0 | Helper backend commun de normalisation des limites et contrat de pagination | Bornage uniforme et teste |
| B1 | P0 | Plafonds de la projection territoriale et feed filtre par animation | Accueil et actualites bornes |
| B2 | P0 | Pagination coffrets et commercants, projection coffret `summary` | Pages commune et catalogue scalables |
| B3 | P1 | Recherche villes et commandes professionnelles | Listes volumineuses maitrisees |
| B4 | P1 | Facade groupee Localeo Live | Suppression du N+1 principal |
| F0 | P0 | Adaptation des services API frontend aux contrats pagines | Appels centralises |
| F1 | P0 | Chargement progressif et etats de pagination | Aucun chargement massif implicite |
| F2 | P1 | Recette performance, accessibilite et observabilite | Validation avant production |

Etat de realisation de B0 : le helper de taille, l'enveloppe commune, le codec
de curseur versionne et signe, la liaison aux filtres et l'erreur
`400 CURSEUR_INVALIDE` sont implementes et couverts par des tests.

Etat de realisation de B1 : les plafonds fixes `1/8/4/5/6`, la separation entre
le perimetre territorial et les huit communes affichees, ainsi que les
departages stables des widgets sont implementes. Le feed expose egalement le
filtre relationnel `animation_id`, une enveloppe paginee, un curseur composite
versionne et signe, un maximum general de 50 et un maximum de 20 pour les
actualites d'une animation.

## User Stories

### PRD-545 - Forcer les limites cote backend

En tant qu'operateur, je veux que chaque route de liste impose une taille maximale afin qu'aucun client ne puisse degrader le service avec une reponse excessive.

### PRD-546 - Paginer les catalogues territoriaux

En tant que visiteur, je veux consulter progressivement les coffrets et commercants afin que la page reste rapide meme dans une commune tres fournie.

### PRD-547 - Borner les widgets de l'accueil

En tant que visiteur mobile, je veux un accueil local synthetique afin que les signaux et nouveautes ne repoussent pas les actions principales.

### PRD-548 - Filtrer les actualites par animation

En tant que visiteur d'une animation, je veux charger uniquement ses actualites afin d'obtenir rapidement une frise pertinente.

### PRD-549 - Paginer les commandes professionnelles

En tant qu'acheteur professionnel, je veux gerer une commande volumineuse par pages afin que l'interface reste utilisable quel que soit le nombre de coffrets.

### PRD-550 - Resoudre la bibliotheque Live par lot

En tant qu'utilisateur Localeo Live, je veux retrouver rapidement mes ressources sauvegardees sans declencher une requete independante pour chacune.

## Criteres d'acceptation

- toutes les routes identifiees possedent une valeur par defaut et un maximum testes cote backend ;
- une limite absente, negative, nulle, non numerique ou excessive est traitee conformement au contrat commun ;
- aucun widget de l'accueil ne depasse son plafond documente ;
- la frise d'une animation ne telecharge plus les actualites des autres animations ;
- les listes coffrets, commercants, villes et instances exposent un curseur stable lorsque la suite existe ;
- le frontend n'infere pas `hasMore` uniquement depuis la taille de la page ;
- aucun chargement de page suivante n'est declenche sans action utilisateur, sauf scroll infini explicitement valide ;
- les erreurs de page suivante conservent les elements deja affiches et permettent de reessayer ;
- les tests couvrent les plafonds, curseurs invalides, doublons entre pages, suppression ou ajout entre deux pages et reponses vides ;
- les pages critiques restent sans debordement et utilisables a 320, 390 et 430 px ;
- les mesures de poids et de latence sont disponibles avant la mise en production.

## Strategie de migration

1. Ajouter le helper de bornage et les metadonnees de pagination sans retirer les anciens champs.
2. Forcer immediatement les maxima sur les routes existantes.
3. Ajouter les curseurs et projections legeres route par route.
4. Adapter le frontend pour lire `items` et `pagination.nextCursor` avec compatibilite temporaire des anciennes reponses.
5. Supprimer les heuristiques frontend fondees sur `items.length === limit` apres stabilisation.
6. Mesurer les poids et latences avant et apres deploiement.
7. Retirer les anciens contrats uniquement apres expiration de la periode de compatibilite.

## Definition of done

- contrats OpenAPI mis a jour ;
- bornes serveur centralisees et couvertes par des tests unitaires ;
- tests d'integration sur toutes les routes P0 et P1 ;
- index SQL verifies sur les tris et filtres pagines ;
- frontend migre sans chargement integral implicite ;
- recette mobile et reseau lent realisee ;
- documentation des valeurs par defaut et maximales publiee ;
- tableaux de bord de poids, latence et tailles effectives disponibles.


## Compléments Marketplace

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### Feed et actualites d'animation

```http
GET /public/exploitation/activites-locales
    ?animation_id={uuid}
    &type_activite=ACTUALITE_ANIMATION
    &limit=10
    &cursor={opaque}
```
