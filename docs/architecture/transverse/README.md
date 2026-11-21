# Architecture transverse

Ce dossier documente les choix communs a plusieurs EPIC.

## Choisir selon le changement

| Sujet touché | Référence à lire |
| --- | --- |
| Affichage, saisie, tri ou échéance de dates/horaires | [Affichage des dates](affichage-dates.md) |
| Logo, nom, actions ou adaptation mobile d’un en-tête | [Identité des en-têtes](identite-entetes-applications.md) |
| Règle, contrat, lecture ou commande | [Matrice de contrôles](controle-architecture.md) pour sélectionner les conventions et preuves |

## Documents

- [Identité des en-têtes des applications](identite-entetes-applications.md) : signatures publiques et signatures des applications de gestion, couleurs, typographie et adaptation mobile.
- [Principes directeurs UX de Localeo Live](../../produit/live/principes-ux.md) : à appliquer aux évolutions de l’expérience habitant, du cadrage à la revue visuelle.

- [Architecture solution](architecture-solution.md) : vue d'ensemble du backend, couches et integrations.
- [Domaines fonctionnels](domaines-fonctionnels.md) : decoupage cible issu de l'EPIC 40.
- [Conventions API et OpenAPI](conventions-api-openapi.md) : organisation des routes, domaines et contrats.
- [Performance et volumétrie](performance-volumetrie.md) : lectures paginées en base, index, mémoire, contention et preuves de capacité pour les évolutions.
- [Conventions back-office](conventions-backoffice.md) : domaines de navigation, gabarit, [recherche et actualisation ciblée des résultats](conventions-backoffice.md#recherche-et-actualisation-ciblée-des-résultats) pour CRM/ERP/Pro/Animation et [règles UX des pages de gestion ERP](conventions-backoffice.md#ux-des-pages-de-gestion-erp), avec checklist de recette.
- [Conventions securite](conventions-securite.md) : exposition publique/protegee/interne, audit et idempotence.
- [Charte email](charte-emails-localeo.md) : rendu commun, liens, QR et recette des emails.
- [Contrôle d'architecture](controle-architecture.md) : principes applicables, preuves de revue, contrôles CI et limites.
- [ADR domaine d'abord](../decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md) : placement des invariants et correction progressive de la dette.


- [Affichage des dates](affichage-dates.md) : heure de Paris commune aux interfaces, dates civiles et preuves.
