# Epic 41 - Specification Localeo Animation - Actualites d'une animation

## Objet du document

Cette specification decrit exclusivement les evolutions de l'application partenaire **Localeo Animation** necessaires pour creer et piloter les actualites rattachees a une animation.

Les regles backend transverses sont detaillees dans la [specification transverse](actualites.md). Le rendu grand public est decrit dans la [specification Localeo Live](actualites-localeo-live.md). Les arbitrages `ARB-64` a `ARB-69` sont valides et normatifs.

## Bilan d’implémentation consigné le 23 août 2026

Le bilan source annonce le périmètre backend/back-office implémenté : migration `v176`, permission dédiée, audit, cycle éditorial, API protégées, programmation par le batch existant, contrat OpenAPI et consultation SQLAdmin. Il indiquait alors que l’interface partenaire n’était pas présente dans le dépôt backend et restait à raccorder. L’application se trouve dans le dépôt voisin `localeo-animation` ; ce constat historique ne vaut pas état actuel de son raccordement. Le statut produit est porté par la [roadmap EPIC 41](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md), qui classe l’EPIC terminée.

## Utilisateur et habilitation

L'utilisateur cible est un gestionnaire connecte au portail Localeo Animation.

- L'entree `Actualites` est visible dans la fiche d'une animation seulement si l'utilisateur possede `animation:gerer_actualites` sur le tenant actif.
- Le backend controle le droit et le tenant a chaque requete ; le masquage frontend n'est pas une mesure de securite.
- Une ressource inconnue ou hors tenant retourne `404` ; une permission absente dans le tenant retourne `403`.
- Pour les habilitations existantes, la migration ajoute ce droit uniquement lorsque `animation:modifier` et `animation:publier` sont deja accordees.
- Les nouveaux profils de gestionnaire complet recoivent ce droit par defaut.

## Navigation

Depuis la fiche d'une animation, ajouter un onglet `Actualites` dans la navigation secondaire. Il conserve le contexte de l'animation :

- identifiant, nom, commune et statut visibles dans l'en-tete ;
- aucune selection manuelle d'une autre animation ou commune ;
- retour direct vers la vue d'ensemble de l'animation ;
- URL partageable et restaurable apres rafraichissement.

L'entree peut afficher un compteur de brouillons et un indicateur lorsqu'une publication programmee est bloquee.

## Ecran de liste

La liste est antichronologique et paginee. Elle expose au minimum :

| Information | Regle d'affichage |
| --- | --- |
| Titre | Texte principal de l'actualite. |
| Statut | `Brouillon`, `Programmee`, `Publiee`, `Masquee` ou `Expiree`. |
| Publication | Date effective, date programmee ou `Non planifiee`. |
| Expiration | Date optionnelle ou `Sans expiration`. |
| Diffusion | Nombres d'inbox creees, de WebPush envoyes et d'erreurs lorsqu'ils sont disponibles. |
| Derniere modification | Date et auteur issus de l'audit expose. |

Filtres attendus : statut et recherche textuelle. Les filtres sont conserves dans l'URL.

Actions contextuelles :

- `Creer une actualite` ;
- `Modifier` pour un contenu encore modifiable ;
- `Publier maintenant` ou `Programmer` selon le statut de l'animation ;
- `Masquer` pour une publication visible ;
- `Supprimer` uniquement pour un brouillon, apres confirmation explicite ;
- `Consulter dans Localeo Live` lorsque le deep link est disponible.

## Ecran de creation et d'edition

| Champ | Obligatoire | Regles UX |
| --- | --- | --- |
| Titre | Oui | Compteur de caracteres et erreur sous le champ. |
| Description | Oui | Zone multiligne ; aucun HTML fourni par le client ne fait autorite. |
| Visuel | Non | Selection depuis la DAM existante, apercu et texte alternatif. |
| Publication | Non | Choix `Brouillon`, `Publier maintenant` ou `Programmer`. |
| Date de publication | Si programmee | Date future, dans le fuseau affiche a l'utilisateur. |
| Date d'expiration | Non | Posterieur a la publication lorsqu'elle est renseignee. |

Le nom, la commune, le statut et l'URL publique de l'animation sont en lecture seule et resolus par le backend.

Le bouton principal enregistre un brouillon. La publication immediate ou la programmation utilise une action distincte afin d'eviter une diffusion involontaire. Une confirmation recapitule l'animation, l'audience et la date avant publication.

## Apercu Localeo Live

L'editeur propose un apercu non contractuel de la carte affichee dans `En direct > Animations` : visuel ou placeholder, titre, description tronquee, nom de l'animation, commune, date et action vers la fiche Animation.

L'apercu ne doit pas recopier la logique de formatage du backend et ne remplace pas une recette dans Localeo Live.

## Cycle de vie et actions

| Statut actualite | Actions principales | Contraintes |
| --- | --- | --- |
| `BROUILLON` | Modifier, programmer, publier, supprimer | Autorise pour toute animation non archivee. |
| `PROGRAMMEE` | Modifier la programmation, publier, annuler vers brouillon | Execution seulement si l'animation est `PUBLIEE`, `EN_COURS` ou `CLOTUREE`. |
| `PUBLIEE` | Consulter, modifier les donnees autorisees, masquer | Pas de suppression physique. |
| `MASQUEE` | Consulter et auditer | Invisible dans le feed ; aucune suppression retroactive de notification. |
| `EXPIREE` | Consulter et auditer | Aucune nouvelle diffusion. |

Une publication immediate est autorisee uniquement pour une animation `PUBLIEE`, `EN_COURS` ou `CLOTUREE` non archivee. Une execution programmee devenue incompatible est bloquee et expose une erreur `409` actionnable dans la liste.

## Contrats API consommes

| Methode et route | Usage ecran |
| --- | --- |
| `GET /protected/animation-locale/animations/{animation_id}/actualites` | Liste, filtres et pagination. |
| `POST /protected/animation-locale/animations/{animation_id}/actualites` | Creation du brouillon. |
| `GET /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}` | Detail et rechargement de l'editeur. |
| `PATCH /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}` | Modification du contenu ou de la programmation. |
| `POST /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}/publier` | Publication immediate idempotente. |
| `POST /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}/masquer` | Retrait du feed. |
| `DELETE /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}` | Suppression d'un brouillon. |

Les commandes de diffusion utilisent `Idempotency-Key`. Les objets de requete, de reponse et d'erreur sont modelises dans OpenAPI ; le frontend ne depend d'aucun modele ORM.

## Etats UX obligatoires

- chargement initial et chargement de page suivante ;
- liste vide avec action de creation ;
- sauvegarde en cours et confirmation de sauvegarde ;
- validation locale des champs puis affichage des erreurs API ;
- `403` avec explication du droit requis ;
- `404` avec retour a la liste des animations ;
- `409` avec statut courant et action de correction possible ;
- erreur reseau avec nouvelle tentative sans duplication de publication ;
- avertissement avant de quitter un formulaire modifie ;
- confirmation destructive avant suppression ou masquage.

## Accessibilite et responsive

- Toutes les actions sont accessibles au clavier avec un focus visible.
- Le statut n'est jamais communique uniquement par la couleur.
- Les confirmations restaurent le focus sur l'action declenchante apres fermeture.
- Les erreurs sont associees aux champs et annoncees aux technologies d'assistance.
- Sur mobile, le tableau devient une liste structuree sans perdre les actions ni les statuts.

## Criteres de recette Localeo Animation

- Un gestionnaire habilite cree un brouillon depuis la bonne animation sans pouvoir changer son rattachement.
- Un utilisateur sans droit ne voit pas l'onglet et obtient `403` s'il appelle directement une action dans son tenant.
- Une animation archivee refuse toute creation ou diffusion selon les regles du cycle de vie.
- Une animation au statut incompatible refuse la publication avec `409` sans perdre le brouillon.
- Deux clics ou reprises reseau sur `Publier` ne produisent qu'une seule diffusion fonctionnelle.
- Seul un brouillon peut etre supprime physiquement.
- Une publication masquee disparait du feed public.
- Les compteurs de diffusion ne sont jamais codes en dur dans l'interface.

## Hors perimetre

- Creation d'actualites globales ou multi-communes depuis Localeo Animation.
- Selection d'une audience nominative ou envoi manuel a un participant.
- Editeur HTML libre, commentaires publics ou messagerie bidirectionnelle.
- Duplication du moteur editorial `activites_locales` dans le domaine Animation.
