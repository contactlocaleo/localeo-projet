# Epic 49 - Visibilite des animations dans la Marketplace

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-49-animations-marketplace-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

> Consolidation des copies backend et Marketplace. Les compléments backend
> sur `CLOTUREE` et `statuts_publics` sont conservés : leur absence dans l'ancienne
> copie frontend ne constitue pas une suppression du contrat. Les dates de recette
> du document restent celles de la source, sans validation de déploiement nouvelle.

## Objet

Cette conception rend les animations publiques de l'Epic 41 visibles dans la Marketplace sans dupliquer le domaine `animation_locale`, le referentiel des communes, les commercants ni les coffrets. Le nom physique historique de ce referentiel reste `villes`.

Etat au 23 aout 2026 : implementation backend et Marketplace terminee ; recette sur environnement deploye requise avant MEP.

Le backend reste seul responsable de l'eligibilite publique, des compteurs et des liens metier. La Marketplace ne fait que presenter les projections publiques retournees par l'API.

## Documents

- [Backlog Marketplace](../../roadmap/terminees/epic-49-animations-marketplace-backlog.md)

- [Backlog Epic 49](../../roadmap/terminees/epic-49-animations-marketplace-backlog.md)
- [Conception backend et contrats API](backend-api.md)
- [Conception Marketplace](frontend-marketplace.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Etat de l'existant

| Capacite | Etat | Evolution attendue |
| --- | --- | --- |
| Liste publique d'animations | Presente, filtre commune et `limit` | Centraliser l'eligibilite, paginer en base et enrichir le contrat |
| Detail public | Present sur l'API et la Marketplace | Appliquer la meme eligibilite et completer la projection |
| Inscription publique | Presente | Reutiliser sans creer un second parcours |
| Catalogue Marketplace | Absent | Creer `/animations` |
| Bloc page commune | Absent | Ajouter un bloc conditionnel |
| Blocs commercant et coffret | Absents | Ajouter des blocs fondes sur les liens reels de configuration |
| Synthese d'accueil | Absente | Ajouter un contrat agrege et un bloc conditionnel |
| Recherche animation | Absente | Etendre l'Epic 33 dans un lot P2 |

## Architecture cible

```text
Accueil / Commune / Commercant / Coffret / Catalogue / Detail
                              |
                              v
            API publique animation_locale (projections stables)
                              |
                              v
          ServiceCatalogueAnimationsPubliques + predicat unique
               /             |             |             \
      animations       configurations   abonnements      communes
                                                            (table `villes`)
                         commercants       plateforme     coffrets
```

`Commune` est le terme metier canonique. Dans l'implementation actuelle, une commune designe toujours une ligne de l'unique table historique `villes`. Aucune table ni entite concurrente n'est creee.

## Responsabilites

| Sujet | Backend | Marketplace |
| --- | --- | --- |
| Eligibilite publique | Calcule et impose | Ne la recalcule jamais |
| Statut affiche | Retourne un statut derive et un booleen d'inscription | Traduit les codes en libelles |
| Compteurs | Calcules avec le meme predicat que la liste | Affiches tels quels |
| Liens commercant/coffret | Resolus depuis la configuration publiee | Affiches uniquement si retournes |
| Pagination et tri | Garantis par le contrat | Pilotage du chargement et des filtres |
| Cache | En-tetes HTTP et coherence | React Query, duree inferieure ou egale au cache HTTP |
| Erreur partielle | API isolee du reste de la Marketplace | Masquage des blocs contextuels sans bloquer les coffrets |
| SEO et analytics | Donnees publiques stables, aucune PII | Metadonnees, JSON-LD et evenements soumis au consentement |

## Principes retenus dans la conception

- evolution additive du contrat deja utilise par Localeo Live ;
- visibilite reservee aux abonnements strictement `ACTIF`, dans leur periode de validite ;
- retrait immediat des projections publiques a l'expiration, avec maintien des acces participant tokenises ;
- horizon futur configurable avec une valeur par defaut de 90 jours ;
- aucune donnee participant, paiement, abonnement ou configuration interne dans les reponses publiques ;
- `statut_public` et `inscription_ouverte` sont deux notions distinctes pour eviter le doublon entre cycle de vie et possibilite d'inscription ;
- le filtre repetable `statuts_publics` permet d'inclure `CLOTUREE` dans les listes d'une commune, tandis que le catalogue sans filtre reste limite aux animations a venir et en cours ;
- une ressource devenue ineligible retourne `404`, y compris si elle existe encore en back-office ;
- le catalogue reste disponible sans installation de Localeo Live ;
- une panne de l'API animation ne doit jamais empecher la consultation ou l'achat d'un coffret.

## Lots techniques

| Lot | Etat | Perimetre backend | Perimetre Marketplace | Prealable |
| --- | --- | --- | --- | --- |
| B0 | Termine | Predicat, liste paginee, detail coherent, synthese, tests et OpenAPI | Aucun | Arbitrages P0 valides |
| F0 | Termine | Contrats stabilises | Catalogue et detail partageable | B0 |
| F1 | Termine | Filtres contextuels | Page commune | B0, F0 |
| F2 | Termine | Synthese territoriale | Accueil | B0, F0 |
| F3 | Termine | Filtres commercant/coffret | Pages commercant et coffret | B0 et F0 |
| F4 | Termine | En-tetes et donnees SEO | Accessibilite, SEO et analytics ; recette MEP a executer | F1 a F3 |
| B1/F5 | Termine | Scope public de recherche | Resultats animation dans la recherche | Epic 33 et F0 |

## Definition de termine

- tous les contrats sont modelises dans OpenAPI ;
- liste, detail et synthese utilisent exactement le meme predicat d'eligibilite ;
- les requetes sont bornees et ne declenchent pas de N+1 ;
- Localeo Live continue de fonctionner pendant la migration du contrat ;
- les six surfaces Marketplace sont testees en succes, vide, chargement et erreur ;
- le mobile, le clavier, les lecteurs d'ecran, les liens directs et le retour arriere sont recettables ;
- aucune information privee ou contractuelle n'est exposee.

[Retour à l’index des spécifications](../INDEX.md)
