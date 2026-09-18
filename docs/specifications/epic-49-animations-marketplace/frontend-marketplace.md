# Epic 49 - Conception Localeo Marketplace

> Fusion des copies backend et Marketplace. Seul écart de comportement décrit :
> la valeur par défaut du flag animations. Le code actuel de Marketplace confirme
> `true` dans [featureFlags](../../../../localeo-marketplace/src/services/featureFlags.js)
> et [public-config](../../../../localeo-marketplace/scripts/public-config.cjs), ainsi que
> dans `.env.example`. L'ancien exemple backend `false` est remplacé pour refléter
> l'existant ; aucune configuration d'environnement ni règle métier n'est modifiée.

## 1. Objectif frontend

Ajouter la decouverte des animations aux parcours Marketplace existants, sans dupliquer Localeo Live et sans degrader la consultation ou l'achat des coffrets.

La Marketplace consomme exclusivement les projections publiques de l'Epic 49. Elle ne charge pas les abonnements et ne reconstruit pas l'eligibilite a partir de statuts bruts.

## 2. Reutilisation de l'existant

- conserver `AnimationPublicPage` pour le detail public ;
- reutiliser et faire evoluer `AnimationDetailView` sans imposer le shell visuel de Localeo Live ;
- reutiliser `@localeo-marketplace/src/services/api.js`, React Query, le service analytics et les composants d'etat existants ;
- conserver les routes participant tokenisees hors catalogue et hors indexation ;
- ne pas reutiliser le stockage local du carnet Live pour la simple consultation Marketplace.

## 3. Configuration

Ajouter un flag runtime :

```text
LOCALEO_FEATURE_MARKETPLACE_ANIMATIONS_ENABLED=true
```

Le flag doit etre pris en charge dans :

- `@localeo-marketplace/src/services/runtimeConfig.js` ;
- `@localeo-marketplace/src/services/featureFlags.js` ;
- `@localeo-marketplace/scripts/write-app-config.cjs` ;
- `@localeo-marketplace/server.cjs` ;
- `.env.example` et la documentation d'environnement.

Les animations sont activees par defaut, y compris lorsque le flag est absent de la configuration. Quand il vaut explicitement `false`, les blocs et la route catalogue sont masques, mais le detail public existant reste accessible pour ne pas casser les liens deja diffuses.

## 4. Couche API et normalisation

Ajouter dans `@localeo-marketplace/src/services/api.js` :

- `fetchPublicAnimations(filters)` ;
- `fetchPublicAnimationsSummary(filters)` ;
- conserver `fetchLiveAnimation(animationId)` ou le renommer par alias non cassant vers `fetchPublicAnimation(animationId)`.

Ajouter des query keys centralisees :

- `publicAnimations(filters)` ;
- `publicAnimationsSummary(filters)` ;
- `publicAnimation(animationId)`.

Un module `@localeo-marketplace/src/services/publicAnimations.js` peut centraliser :

- la normalisation additive de l'ancien et du nouveau contrat ;
- les libelles `A venir` et `En cours` ;
- le formatage des dates ;
- la construction des URLs catalogue et detail ;
- le fallback typographique du visuel.

Aucun composant ne doit tester les statuts d'abonnement ou inspecter `regles` pour decider de la visibilite.

## 5. Routage

Routes cibles :

```text
/animations
/animations?commune_id={uuid}
/animations/{animation_id}
/animations/participants/{token}
```

La route catalogue est ajoutee explicitement avant les routes de detail et participant. Elle reste partageable et restaure ses filtres depuis l'URL. Les tokens participant ne sont jamais recopies dans une URL catalogue, un evenement analytics ou le store global.

## 6. Catalogue `/animations`

### Contenu

1. titre et perimetre territorial ;
2. synthese compacte ;
3. filtre commune ;
4. filtres `A venir`, `En cours` et `Inscriptions ouvertes` ;
5. une animation mise en avant, puis une liste chronologique ;
6. chargement de la page suivante ;
7. etat vide utile avec retour aux communes.

Le filtre `Inscriptions ouvertes` utilise le booleen du contrat et ne devient pas un statut de workflow.

### Comportements

- les filtres modifient l'URL et la query key ;
- le changement de filtre conserve le focus et annonce le nombre de resultats dans une zone `aria-live` ;
- la pagination ajoute les lignes sans doublon ;
- l'absence de visuel utilise la composition date + nom, jamais une image generique de coffret ;
- un echec propose `Reessayer` et laisse la navigation principale utilisable.

## 7. Page commune

Dans le composant historique `CityPage`, qui represente une commune :

- lancer la requete avec l'identifiant de l'objet historique `ville`, qui est le `commune_id` canonique ;
- afficher le bloc apres le coffret recommande et avant le catalogue complet des coffrets ;
- mettre en avant la premiere animation puis afficher une liste courte ;
- lier le CTA secondaire vers `/animations?commune_id=...` ;
- ne rendre aucun espace vide si la reponse contient zero animation ;
- en cas d'erreur, masquer le bloc et ne pas faire echouer les requetes commune, commercants ou coffrets.

Le code peut conserver temporairement les noms techniques historiques `CityPage` et `ville`, mais ils representent l'unique objet metier `commune`. Aucun modele frontend concurrent n'est cree.

## 8. Accueil

Ajouter un bloc `Animations Localeo` apres l'exploration des communes et avant le fil d'activite locale.

Il affiche :

- `total_a_decouvrir` ;
- `total_en_cours` ;
- `total_inscriptions_ouvertes` ;
- les premieres communes et leur nombre ;
- un CTA vers le catalogue.

La synthese porte sur la commune selectionnee lorsqu'elle existe ; sans commune selectionnee, elle porte sur l'ensemble du reseau. Le libelle annonce toujours ce perimetre. Si le total vaut zero ou si l'API echoue, le bloc est absent.

## 9. Page commercant

Dans `CommercantPage` :

- appeler la liste avec `commercant_id` ;
- afficher `Ce commerce participe` apres l'histoire du commercant et avant ses coffrets ;
- limiter l'apercu et proposer un lien vers le catalogue filtre si necessaire ;
- ne jamais afficher une animation de la meme commune si le commercant n'est pas retourne par le backend.

## 10. Page coffret

Dans `CoffretPage` :

- appeler la liste avec `coffret_id` ;
- afficher `Ce coffret est a gagner dans...` apres les experiences et adresses, avant l'activite locale ;
- utiliser la nature de lien retournee par l'API ;
- ne jamais deduire le lien depuis la commune ou les commercants du coffret ; afficher uniquement la nature `LOT_A_GAGNER` retournee par le backend pour les coffrets presents dans la configuration publiee.

## 11. Detail public

Faire evoluer `AnimationPublicPage` :

- chargement via la query key publique ;
- retour vers le catalogue et conservation du contexte commune ;
- affichage du statut public, des dates, de la commune, du visuel, des commercants et lots ;
- CTA d'inscription uniquement si `inscription_ouverte` ;
- CTA secondaire vers Localeo Live uniquement comme proposition, jamais comme prerequis ;
- message neutre sur `404`, sans reveler une suspension d'abonnement ;
- aucun affichage du nombre de participants.

## 12. Composants proposes

| Composant | Usage |
| --- | --- |
| `PublicAnimationsSummary` | Accueil et en-tete catalogue |
| `PublicAnimationFeatured` | Catalogue et page commune |
| `PublicAnimationList` | Liste chronologique partagee |
| `PublicAnimationListItem` | Resume accessible et responsive |
| `PublicAnimationStatus` | Libelle et tonalite du statut derive |
| `PublicAnimationFallbackVisual` | Composition typographique sans image |
| `PublicAnimationsContextBlock` | Variante compacte commercant/coffret |

Les composants de presentation ne declenchent pas directement les requetes. Les pages ou hooks de fonctionnalite orchestrent les appels.

## 13. Etats UX obligatoires

| Etat | Catalogue | Blocs contextuels |
| --- | --- | --- |
| Chargement | squelette stable sans saut de mise en page | emplacement reserve court ou bloc absent |
| Succes | contenu et total annonces | contenu compact |
| Vide | explication et retour vers les communes | bloc totalement absent |
| Erreur | message, reference si disponible et bouton reessayer | bloc masque, reste de la page intact |
| Hors ligne | contenu React Query precedent si disponible | bloc masque si aucune donnee |

## 14. Accessibilite

- cibles tactiles d'au moins 44 px ;
- titres hierarchises et dates dans des elements `time` ;
- statut jamais exprime par la couleur seule ;
- focus visible et restitue apres changement de filtre ;
- total de resultats annonce avec `aria-live="polite"` ;
- visuels decoratifs avec `alt=""`, visuels informatifs avec alternative utile ;
- aucun carrousel automatique.

## 15. SEO et analytics

### SEO

- titre et description specifiques au catalogue et au detail ;
- URL canonique sans parametres de tracking ;
- JSON-LD `Event` uniquement si nom, dates, lieu et URL sont disponibles ;
- `noindex` sur les routes participant ;
- le MVP reste client-side et ne promet ni rendu Open Graph serveur, ni SSR, ni prerendu.

### Analytics

Evenements proposes :

- `marketplace_animations_block_viewed` ;
- `marketplace_animations_catalog_viewed` ;
- `marketplace_animation_filter_changed` ;
- `marketplace_animation_opened` ;
- `marketplace_animation_registration_started`.

Proprietes autorisees : `animation_id`, `commune_id`, surface et filtre. Email, telephone, nom, token et identifiant participant sont interdits.

## 16. Tests Marketplace

### Tests unitaires

- normalisation ancien/nouveau contrat ;
- libelles des statuts et dates ;
- construction des URLs et filtres ;
- fallback sans visuel ;
- absence de PII dans les evenements.

### Tests composants et pages

- six surfaces en chargement, succes, vide et erreur ;
- masquage par feature flag ;
- conservation des filtres dans l'URL ;
- absence de bloc contextuel lorsque la liste est vide ;
- resilience des pages coffret et achat en cas de panne animation ;
- navigation clavier et annonces accessibles.

### Recette responsive

- 320 px, 375 px, tablette et desktop ;
- navigation directe et rechargement serveur de `/animations` et du detail ;
- retour arriere apres filtre et detail ;
- installation Localeo Live non requise ;
- validation des liens canoniques et JSON-LD.

## 17. Ordre d'implementation Marketplace

1. configuration, query keys, API et normalisation ;
2. composants partages et catalogue ;
3. evolution du detail public ;
4. bloc commune ;
5. synthese accueil ;
6. blocs commercant et coffret ;
7. accessibilite, SEO, analytics et recette ;
8. recherche animation en lot P2.
