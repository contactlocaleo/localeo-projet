# Epic 57 - Bornage et pagination des API Marketplace

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-57-bornage-pagination-api-marketplace-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## References

- [Backlog](../../roadmap/terminees/epic-57-bornage-pagination-api-marketplace-backlog.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Socle implemente

Les nouvelles collections paginees utilisent l'enveloppe suivante :

```json
{
  "items": [],
  "pagination": {
    "pageSize": 5,
    "nextCursor": null,
    "hasMore": false
  }
}
```

Le helper commun impose une valeur par defaut et un maximum. Une taille nulle,
negative, non numerique, excessive ou contradictoire entre `page_size` et
`limit` retourne `422`.

Les curseurs :

- sont opaques, versionnes et signes par HMAC-SHA-256 ;
- contiennent toutes les valeurs du tuple de tri et l'identifiant stable ;
- sont lies a la route et a une empreinte canonique des filtres ;
- ne contiennent ni token metier ni donnee personnelle ;
- n'expirent pas temporellement au MVP ;
- retournent `400 CURSEUR_INVALIDE` lorsqu'ils sont malformes, falsifies,
  incompatibles avec les filtres ou produits par une version non supportee.

Le secret `LOCALEO_PAGINATION_CURSOR_SECRET` doit etre long, aleatoire et
identique sur toutes les instances du backend.

## Feed des activites locales

```http
GET /public/exploitation/activites-locales
    ?animation_id={uuid}
    &type_activite=ACTUALITE_ANIMATION
    &page_size=10
    &cursor={opaque}
```

Regles implementees :

- taille par defaut de 5 et maximum general de 50 ;
- maximum de 20 lorsqu'un `animation_id` est fourni ;
- `limit` conserve comme alias deprecie de `page_size` ;
- filtre SQL relationnel par `animation_id` ;
- eligibilite publique et deduplication avant limitation ;
- tri `date_publication DESC, poids DESC, id DESC` ;
- lecture de `pageSize + 1` lignes pour calculer `hasMore` sans `COUNT` global ;
- `nextCursor` produit uniquement lorsqu'une page suivante existe.

Le passage de la liste JSON historique a l'enveloppe paginee est volontairement
cassant conformement a `PAG-ARB-04` : aucun contrat permettant une lecture non
bornee n'est conserve.

## Documents complémentaires du dossier

- [Catalogue public de coffrets : contrat de lecture et pagination](catalogue-coffrets.md)
- [Catalogue public sans contacts operationnels](catalogue-public-sans-contacts.md)

[Retour à l’index des spécifications](../INDEX.md)
