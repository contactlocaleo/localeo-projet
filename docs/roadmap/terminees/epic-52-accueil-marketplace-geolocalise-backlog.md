# Backlog Epic 52 - Accueil Marketplace contextualise par geolocalisation

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Moyenne`.
- Statut : `Termine`.
- Objectif : contextualiser l'accueil avec les communes publiees situees dans un rayon configurable, calcule depuis la position ponctuelle du visiteur ou depuis les coordonnees d'une ville de preference, tout en autorisant un accueil sans contexte territorial.
- Domaine principal : `referencement`, avec projections publiques pour la Marketplace.
- Surfaces ciblees : backend, BackOffice de gestion des communes et Marketplace publique.
- Dependances : Epic 16 `Feed d'activite locale`, Epic 33 `Recherche multi-scope` et Epic 49 `Animations dans la Marketplace`.

Voir [le cadrage fonctionnel](../../specifications/epic-52-accueil-marketplace-geolocalise/README.md) et [le registre des arbitrages](../../specifications/epic-52-accueil-marketplace-geolocalise/registre-arbitrages.md).

## Probleme

L'accueil Marketplace peut etre contextualise par une commune choisie, mais il ne sait pas identifier les territoires Localeo proches d'un visiteur. Le referentiel historique `villes` contient le nom, le code postal et l'indicateur `publiee_marketplace`, mais aucune latitude ni longitude. Un code postal seul ne permet pas de calculer une distance fiable.

L'enjeu n'est pas de suivre l'internaute : sa position doit uniquement servir a proposer ponctuellement des communes proches. L'accueil actuel et la selection manuelle doivent rester disponibles en permanence.

## Principes produit

- proposer par defaut le mode `Autour de moi` et tenter la geolocalisation apres acceptation du visiteur ;
- expliquer le benefice avant de demander l'autorisation du navigateur ;
- ne jamais rendre la geolocalisation obligatoire ;
- en cas de refus de la geolocalisation, proposer une ville Marketplace georeferencee comme origine alternative du calcul ;
- calculer la proximite cote backend depuis les coordonnees de reference des communes ;
- ne pas persister ni journaliser la position exacte de l'internaute ;
- retourner uniquement des communes publiables dans la Marketplace ;
- utiliser dans tous les modes contextualises toutes les communes publiees situees dans le rayon configure ;
- memoriser localement le mode territorial choisi et, en mode manuel, l'identifiant de la ville de preference ;
- conserver une recherche manuelle par commune ou code postal comme solution de repli ;
- permettre de choisir explicitement le mode sans commune ;
- ne pas afficher les widgets territoriaux en mode sans commune.

## Perimetre MVP

### Backend

- enrichir `villes` avec un code INSEE, une latitude, une longitude et les metadonnees de source optionnelles ;
- integrer l'API publique `geo.api.gouv.fr` pour proposer le centre geographique officiel d'une commune ;
- utiliser le code INSEE comme identifiant externe stable et ne recourir au nom avec code postal que pour rechercher les villes historiques a rapprocher ;
- conserver les coordonnees localement et ne jamais appeler l'API externe pendant une consultation Marketplace ;
- valider les bornes geographiques et tracer les modifications BackOffice ;
- fournir un endpoint public de recherche des communes proches ;
- accepter comme origine soit une latitude et une longitude ponctuelles, soit l'identifiant d'une commune georeferencee ;
- calculer une distance a vol d'oiseau avec la formule de Haversine ;
- appliquer un rayon par defaut de `30 km`, configurable cote backend, et un rayon maximal controle par le serveur ;
- trier les communes par distance avec un ordre secondaire stable ;
- ne jamais inclure une commune non publiee ou depourvue de coordonnees ;
- borner le nombre de resultats et proteger l'endpoint contre les abus ;
- ne pas ecrire latitude et longitude du visiteur dans les logs ou l'audit.
- retourner le meme contrat de communes proches quelle que soit l'origine du calcul ;
- fournir une projection dediee a la page d'accueil pour filtrer ses cinq widgets avec la liste des communes proches ;
- ne pas modifier le comportement territorial des catalogues, recherches et pages de detail hors accueil ;

### BackOffice

- afficher et modifier le code INSEE d'une commune ;
- proposer une action d'enrichissement depuis l'API Decoupage administratif ;
- demander une confirmation lorsque la recherche par nom et code postal retourne plusieurs communes ;
- afficher et modifier les coordonnees d'une commune ;
- indiquer clairement qu'il s'agit du point de reference utilise pour la proximite ;
- signaler les communes publiees sans coordonnees ;
- permettre une reprise controlee des communes existantes ;
- permettre une correction manuelle et conserver la source et la date de derniere mise a jour.

### Marketplace

- proposer la selection manuelle d'une ville de preference georeferencee lorsque la geolocalisation est refusee ou indisponible ;
- proposer par defaut la geolocalisation avec une explication avant l'affichage de la demande navigateur ;
- utiliser `navigator.geolocation` uniquement apres action de l'utilisateur ;
- afficher un etat de recherche non bloquant et un delai maximal ;
- utiliser l'ensemble des communes publiees situees dans le rayon de `30 km` retourne par le backend ;
- contextualiser uniquement les widgets `Coffret du moment`, `Communes disponibles`, `Les animations a vivre pres de chez vous`, `En ce moment` et `Derniers coffrets ajoutes` ;
- gerer refus, indisponibilite, timeout et absence de resultat ;
- conserver la selection manuelle et permettre de modifier la preference locale ;
- enregistrer dans le navigateur le mode choisi et l'identifiant de la ville origine lorsqu'il existe ;
- n'afficher ces cinq widgets qu'en mode `AUTOUR_DE_MOI` ou `VILLE_PREFEREE` ;
- masquer ces cinq widgets, sans afficher de resultat global trompeur, en mode `AUCUNE` ;
- ne pas appliquer automatiquement le contexte memorise aux catalogues, a la recherche, aux pages ville, commercant, coffret ou animation.

## Hors perimetre MVP

- suivi continu ou en arriere-plan de la position ;
- stockage d'un historique de deplacements ;
- geolocalisation silencieuse par adresse IP ;
- calcul d'itineraire, temps de trajet ou distance routiere ;
- carte interactive obligatoire ;
- creation d'un compte client pour memoriser le territoire ;
- geocodage externe a chaque consultation ;
- classement personnalise a partir du comportement de navigation.

## Contrat public propose

`POST /public/referencement/villes/proches/rechercher`

Corps avec origine GPS :

```json
{
  "origine": {
    "type": "POSITION",
    "latitude": 45.8992,
    "longitude": 6.1294
  }
}
```

Corps avec ville de preference :

```json
{
  "origine": {
    "type": "COMMUNE",
    "communeId": "uuid"
  }
}
```

Le rayon n'est pas choisi par le client. Il est lu dans la configuration backend, avec une valeur initiale de `30 km`.

Exemple de reponse :

```json
{
  "origineType": "POSITION",
  "rayonKm": 30,
  "communes": [
    {
      "id": "uuid",
      "nom": "Annecy",
      "codePostal": "74000",
      "distanceKm": 2.4
    }
  ]
}
```

Le contrat ne retourne jamais les coordonnees de l'internaute. L'exposition des coordonnees exactes des communes n'est pas necessaire au MVP.

La projection des cinq widgets est exposee par `POST /public/referencement/villes/proches/accueil`, avec le meme corps. Elle retourne le contexte canonique et les cinq listes territorialisees dans un seul contrat OpenAPI.

## User Stories

### PRD-488 - Georeferencer les communes Localeo

En tant qu'operateur BackOffice, je veux renseigner le point de reference d'une commune afin qu'elle puisse etre proposee dans les recherches de proximite.

Criteres d'acceptation : code INSEE et coordonnees optionnels mais valides, proposition issue de `geo.api.gouv.fr`, confirmation operateur en cas d'ambiguite, modification auditee, source et date conservees, commune incomplete identifiable.

### PRD-489 - Rechercher les communes proches

En tant que Marketplace, je veux transmettre une position ponctuelle afin d'obtenir les communes Localeo situees dans le rayon autorise.

Criteres d'acceptation : origine GPS ou commune acceptee de maniere exclusive, coordonnees de la commune resolues cote backend, calcul Haversine et tri stable, rayon impose par la configuration backend, aucune commune non publiee.

### PRD-490 - Demander la geolocalisation avec contexte

En tant que visiteur, je veux comprendre pourquoi ma position est demandee afin de choisir librement d'afficher les offres proches.

Criteres d'acceptation : aucune demande avant action explicite, texte clair, refus sans blocage du parcours.

### PRD-491 - Contextualiser l'accueil autour de moi

En tant que visiteur geolocalise, je veux voir les communes et contenus proches afin de decouvrir rapidement les offres pertinentes.

Criteres d'acceptation : rayon effectif retourne par le backend, liste des communes proches identifiable, cinq widgets d'accueil issus de l'ensemble de ces communes ; le contrat de resultat est identique pour une origine GPS ou communale et les autres pages ne sont pas filtrees implicitement.

### PRD-492 - Conserver une selection territoriale

En tant que visiteur, je veux retrouver mon mode territorial lors d'une prochaine visite afin de conserver mon choix.

Criteres d'acceptation : le navigateur stocke `AUTOUR_DE_MOI`, `VILLE_PREFEREE` avec son `ville_id` d'origine, ou `AUCUNE`, sans stocker les coordonnees ; la preference est modifiable.

### PRD-493 - Garantir un parcours de repli

En tant que visiteur refusant la geolocalisation, je veux choisir manuellement une commune afin d'utiliser toute la Marketplace.

Criteres d'acceptation : recherche par nom ou code postal, messages adaptes au refus, timeout et absence de resultat ; le visiteur peut choisir une ville ou le mode sans commune.

### PRD-494 - Proteger la position de l'internaute

En tant que responsable conformite, je veux minimiser le traitement de la position afin de ne pas creer un historique de localisation.

Criteres d'acceptation : aucune persistance serveur, aucun log de coordonnees exactes, documentation du traitement et analytics sans position.

### PRD-495 - Superviser la couverture geographique

En tant qu'operateur Localeo, je veux identifier les communes publiees sans coordonnees afin de maintenir la qualite du service.

Criteres d'acceptation : indicateur BackOffice, compteur de couverture, aucune fuite de la position des visiteurs.

## Decoupage initial

| Lot | Priorite | Contenu | Sortie attendue |
| --- | --- | --- | --- |
| B0 | P0 | Code INSEE, coordonnees, migration, integration `geo.api.gouv.fr` et BackOffice | Communes georeferencees localement et modifications auditees |
| B1 | P0 | Service Haversine et API publique bornee | Communes eligibles triees par distance |
| F0 | P0 | Consentement contextuel, appel navigateur et etats de repli | Geolocalisation non bloquante |
| F1 | P1 | Contextualisation multi-communes de l'accueil | Contenus proches et territoire modifiable |
| Q0 | P1 | Securite, confidentialite, accessibilite, performance et recette | Mise en production observable sans collecte de position |

## Definition de termine

- la Marketplace reste entierement utilisable sans geolocalisation ;
- une position autorisee retourne uniquement les communes eligibles situees dans le rayon ;
- les distances sont coherentes sur des cas de reference connus ;
- aucune position visiteur n'est stockee ni journalisee ;
- la selection est modifiable et supprimable ;
- le mode territorial est restaure depuis le navigateur sans conserver la position exacte ;
- en mode `AUTOUR_DE_MOI`, les cinq widgets cibles couvrent les communes eligibles du rayon backend de `30 km` ;
- en mode `VILLE_PREFEREE`, les cinq widgets cibles couvrent les communes eligibles situees dans le meme rayon autour des coordonnees de la ville choisie ;
- en mode `AUCUNE`, aucun des cinq widgets cibles n'est rendu ;
- aucune autre page Marketplace n'est filtree implicitement par ce contexte ;
- les communes sans coordonnees sont pilotables depuis le BackOffice ;
- aucune consultation Marketplace ne depend de la disponibilite de `geo.api.gouv.fr` ;
- les contrats et comportements de succes, refus, timeout, vide et erreur sont testes.


## Compléments Marketplace

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### Synthese

- Objectif : contextualiser cinq widgets de l'accueil avec toutes les communes Localeo publiees situees dans le rayon backend.
- Dependances : Epic 16 `Feed d'activite locale`, Epic 49 `Animations Marketplace` et contrats backend Epic 52.
- Hors perimetre : geolocalisation IP, suivi continu, carte obligatoire et filtrage implicite des autres pages.

Voir la [specification Marketplace](../../specifications/epic-52-accueil-marketplace-geolocalise/parcours-utilisateur.md).

### Lots Marketplace

| Lot | Priorite | Etat | Contenu | Sortie attendue |
|---|---|---|---|---|
| F0 | P0 | A faire | Service API et modelisation des deux contrats POST | Appels centralises et testables |
| F1 | P0 | A faire | Preference locale versionnee et trois modes territoriaux | Aucun stockage de coordonnees |
| F2 | P0 | A faire | Consentement contextuel et `navigator.geolocation` | Refus et timeout non bloquants |
| F3 | P0 | A faire | Integration de la projection des cinq widgets | Aucun appel par commune |
| F4 | P1 | A faire | Selecteur de commune, changement et suppression de preference | Repli complet sans GPS |
| F5 | P1 | A faire | Accessibilite, confidentialite, analytics et recette responsive | Parcours recettable avant MEP |

### User Stories / PRD-496 - Choisir le contexte territorial

Le visiteur peut choisir `Autour de moi`, une ville de preference ou aucune commune. Le choix est explique, modifiable et conserve sans coordonnees exactes.

### User Stories / PRD-497 - Consentir a une position ponctuelle

La demande navigateur suit un clic explicite. La position est utilisee uniquement pour le POST courant puis abandonnee.

### User Stories / PRD-498 - Contextualiser les cinq widgets

La Marketplace affiche exactement les cinq listes de la projection backend, avec un ordre global stable et sans recalcul multi-communes.

### User Stories / PRD-499 - Assurer le repli manuel

Un refus, un timeout, une erreur ou un resultat vide propose une ville de preference ou le mode sans commune.

### User Stories / PRD-500 - Proteger les donnees de localisation

Aucune coordonnee n'est placee dans `localStorage`, `sessionStorage`, les URLs, les query keys, les logs ou les analytics.

### Criteres d'acceptation

- le prompt de geolocalisation n'apparait jamais automatiquement ;
- la Marketplace n'appelle jamais `geo.api.gouv.fr` ;
- la variable backend `LOCALEO_GEO_API_GOUV_COMMUNES_URL` n'est pas exposee dans `window.__APP_CONFIG__` ;
- la projection `POST /public/referencement/villes/proches/accueil` alimente les cinq widgets ;
- le mode `AUCUNE` masque les cinq widgets sans masquer le reste de l'accueil ;
- une commune de preference est revalidee par le backend a chaque restauration ;
- les erreurs territoriales ne bloquent ni catalogues, ni recherche, ni achat ;
- les tests couvrent succes GPS, succes commune, refus, timeout, vide, erreur API et preference obsolete.

### Ordre recommande

1. ajouter les contrats au service API ;
2. implementer le stockage local versionne ;
3. construire le selecteur et le consentement GPS ;
4. brancher les cinq widgets sur la projection unique ;
5. finaliser accessibilite, confidentialite et recette.
