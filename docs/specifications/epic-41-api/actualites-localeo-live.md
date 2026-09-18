# Epic 41 - Specification Localeo Live - Actualites d'animation

## Objet du document

Cette specification decrit exclusivement les evolutions de la PWA grand public **Localeo Live** pour afficher les actualites rattachees aux animations et notifier les installations eligibles, sans compte client.

La creation et le pilotage des contenus sont decrits dans la [specification Localeo Animation](actualites-interface-animation.md). Les regles backend transverses sont detaillees dans la [specification transverse](actualites.md). Les arbitrages `ARB-64` a `ARB-69` sont valides et normatifs.

## Portée du cadrage Live

Le [périmètre frontend EPIC 42](../epic-42-localeo-live/frontend-pwa.md) et son [registre](../epic-42-localeo-live/registre-arbitrages.md) portent la navigation et le MVP courants. La géolocalisation envisagée dans ce cadrage initial est exclue du MVP par LIVE-ARB-31 : la commune est choisie manuellement. Le libellé historique `En direct` employé ci-dessous désigne le flux d'actualités ; EPIC 42 nomme la destination principale `Découvrir` tout en conservant `En direct` pour le flux. La consolidation signale cette coexistence sans créer de nouvelle décision de nommage.

## Utilisateur et contexte

L'utilisateur est un visiteur ou un participant utilisant une installation Localeo Live anonyme :

- aucune creation de compte n'est requise ;
- l'installation et son secret restent stockes localement ;
- la commune est choisie manuellement au MVP ; la géolocalisation ponctuelle avec consentement appartient au cadrage historique écarté par LIVE-ARB-31 ;
- une participation suivie peut rendre l'installation eligible meme si la commune active a change ;
- aucune donnee nominative de participant n'est exposee dans une actualite ou un Push.

## Navigation et emplacement

Les actualites apparaissent dans l'onglet principal `En direct`, sous le filtre `Animations`.

Le filtre `Animations` regroupe `ANIMATION_PUBLIEE` et `ACTUALITE_ANIMATION`. Le filtre `News` conserve les actualites editoriales generiques et n'inclut pas `ACTUALITE_ANIMATION`. Le filtre global `Tout` peut afficher les deux familles.

## Carte d'actualite Animation

| Information | Regle d'affichage |
| --- | --- |
| Visuel | Visuel DAM de l'actualite ou placeholder accessible. |
| Type | Libelle explicite `Actualite d'animation`. |
| Titre | Titre complet ou tronque avec acces au detail. |
| Description | Extrait lisible, sans HTML non maitrise. |
| Animation | Nom de l'animation rattachee. |
| Commune | Commune heritee de l'animation. |
| Date | Date de publication effective. |
| Action | `Voir l'animation`, vers le deep link fourni par l'API. |

Le clic sur la carte ou son action ouvre la fiche de l'animation. Le frontend consomme `cta_url` et ne reconstruit pas le chemin a partir de l'identifiant.

## Fiche Animation

La fiche publique peut presenter un bloc ou une timeline `En direct` avec les publications visibles de l'animation. Elle reutilise les memes donnees que le feed et ne maintient aucune copie locale independante du contenu.

Les actualites masquees, expirees ou non publiees ne sont jamais affichees. Un deep link vers une animation indisponible presente un etat explicite et propose un retour vers les animations de la commune.

## Chargement et pagination

- Le feed est charge par curseur et conserve la position lors du retour depuis une fiche.
- Un rafraichissement manuel recharge la premiere page sans dupliquer les cartes.
- Le changement de commune invalide le feed territorial courant.
- Les nouvelles publications peuvent etre signalees sans deplacer brutalement la position de lecture.
- Le cache PWA peut conserver la derniere page consultee, clairement marquee comme potentiellement obsolete hors ligne.

## Preferences de notification

Dans `Reglages > Notifications`, la categorie `Animations` pilote conjointement l'inbox et le WebPush :

- categorie desactivee : aucune nouvelle inbox et aucun nouveau Push `ACTUALITE_ANIMATION` ;
- categorie activee : creation d'une inbox idempotente pour une installation eligible ;
- un WebPush est tente en complement seulement si l'abonnement navigateur est actif ;
- le refus de permission Push ou un abonnement absent n'empeche pas l'inbox ;
- la desactivation ne supprime pas retroactivement les messages deja remis.

L'interface distingue clairement la preference metier `Animations` de l'autorisation technique de notifications du navigateur.

## Audience

Une installation avec la categorie `ANIMATION` activee est eligible lorsqu'elle suit la commune de l'animation ou une participation a cette animation. L'audience est l'union dedupliquee de ces deux ensembles. Une installation sans lien territorial ni participation ne recoit rien.

## Inbox et WebPush

L'entree inbox et le Push affichent le titre, un resume, le nom de l'animation, la categorie `ANIMATION`, la date et le deep link fourni par le backend.

La cle fonctionnelle `ACTUALITE_ANIMATION:{actualite_id}` garantit une seule notification par installation. L'ouverture marque la notification comme lue de facon idempotente puis navigue vers l'animation.

Le masquage ulterieur retire le contenu du feed mais ne supprime pas une notification deja remise. Si le lien est ouvert apres masquage, la fiche affiche l'animation sans republier le contenu masque.

## Contrats API consommes

| Methode et route | Usage ecran |
| --- | --- |
| `GET /public/exploitation/activites-locales?type_activite=ANIMATION` | Feed `En direct > Animations`, avec filtre commune et curseur. |
| `GET /public/exploitation/activites-locales/{activite_id}` | Detail partageable d'une publication lorsque disponible. |
| `GET /public/animation-locale/animations/{animation_id}` | Fiche publique ciblee par le deep link. |
| `GET /public/localeo-live/installations/{installation_id}/preferences` | Lecture de la preference `ANIMATION`. |
| `PUT /public/localeo-live/installations/{installation_id}/preferences` | Activation ou desactivation de la categorie. |
| `POST /public/localeo-live/abonnements-webpush` | Enregistrement de l'abonnement navigateur. |
| `DELETE /public/localeo-live/abonnements-webpush/{abonnement_id}` | Revocation du Push. |
| `GET /public/localeo-live/installations/{installation_id}/notifications` | Inbox paginee. |
| `POST /public/localeo-live/installations/{installation_id}/notifications/{notification_id}/lecture` | Lecture idempotente. |

`ActiviteLocalePayload` expose une reference `animation` optionnelle avec `id`, `nom`, `statut` et `commune`, ainsi que `cta_url`. Pour `ACTUALITE_ANIMATION`, la reference Animation est obligatoire.

## Configuration

Le backend utilise `LOCALEO_FRONT_LIVE_ANIMATION_URL_TEMPLATE`, qui contient obligatoirement `{animation_id}`, par exemple :

```text
https://marketplace.localeo.city/live/animations/{animation_id}
```

Cette variable est distincte de `LOCALEO_FRONT_LIVE_AJOUTER_ANIMATION_URL_TEMPLATE`, reservee a l'ajout d'une participation avec son token. Localeo Live ne doit pas coder en dur le domaine public.

## Etats UX obligatoires

- squelette de chargement du feed ;
- filtre sans resultat avec proposition de changer de commune ou de consulter toutes les actualites ;
- erreur reseau avec nouvelle tentative ;
- dernier contenu disponible hors ligne avec indication de fraicheur ;
- notification vide ou deja lue ;
- Push refuse par le navigateur sans bloquer l'inbox ;
- deep link vers une animation indisponible, terminee ou archivee ;
- contenu expire ou masque entre l'affichage de l'inbox et l'ouverture.

## Accessibilite et PWA

- Les cartes et filtres sont utilisables au clavier et avec lecteur d'ecran.
- Le filtre actif, les nouveaux contenus et les erreurs sont annonces explicitement.
- Le visuel possede un texte alternatif pertinent ou est marque decoratif.
- Le statut et la categorie ne reposent pas uniquement sur la couleur.
- Les notifications respectent le consentement, les preferences du navigateur et `prefers-reduced-motion`.
- La navigation profonde fonctionne en mode PWA installe et dans un onglet web classique.

## Criteres de recette Localeo Live

- Une publication `ACTUALITE_ANIMATION` visible apparait dans `En direct > Animations`, jamais dans `News` seul.
- La carte affiche le bon nom d'animation, la bonne commune et le bon visuel.
- Le CTA utilise exactement l'URL fournie par le backend et ouvre la bonne fiche.
- Une installation suivant la commune et une participation ne recoit qu'une notification.
- Une installation eligible avec `ANIMATION=false` ne recoit ni inbox ni Push.
- Une installation eligible avec `ANIMATION=true` sans abonnement Push recoit son inbox.
- Une installation sans commune suivie mais suivant la participation recoit la notification.
- Une installation sans lien territorial ni participation ne recoit rien.
- Deux executions du batch ne creent pas de doublon d'inbox ou de Push fonctionnel.
- Une actualite masquee disparait du feed sans supprimer les notifications deja remises.
- Le feed et la fiche restent comprehensibles hors ligne, sur mobile et avec technologies d'assistance.

## Hors perimetre

- Creation ou modification d'une actualite depuis Localeo Live.
- Commentaires, reactions ou messagerie publique.
- Ciblage nominatif manuel.
- Creation d'un compte client pour recevoir les notifications.
- Reconstruction frontend du deep link ou duplication locale du contenu editorial.
