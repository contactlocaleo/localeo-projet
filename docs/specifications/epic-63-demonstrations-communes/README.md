# Epic 63 — Outillage des démonstrations communales

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-63-jeux-demonstration-communes-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

- Version 1.3, 12 septembre 2026 : recentrage demandé par l'utilisateur.
- Principe directeur absolu : **la génération n'impacte jamais le code applicatif**.
- Point d'entrée : `python -m scripts.demonstration`.
- Référence : [backlog Epic 63](../../roadmap/terminees/epic-63-jeux-demonstration-communes-backlog.md).

L'outillage fabrique des données compatibles avec les applications existantes.
Il réutilise leurs modèles et règles sans les modifier, puis sauvegarde,
installe et restaure ces données. Les applications et les intégrations
Stripe test, Brevo et Scaleway fonctionnent normalement.

Le précédent mode applicatif de démonstration est retiré : aucun endpoint,
middleware, badge, filtre de notification, marquage PDF, clé spécifique au
runtime ou migration de contrôle n'est requis. Aucun frontend n'est adapté.
Le journal et les identifiants de génération sont conservés dans les fichiers
privés de l'opérateur.

| Document | Objet |
| --- | --- |
| [Guide opérateur](../../exploitation/demonstration/exploitation.md) | Préparation, commandes et procédure de remplacement. |
| [Architecture](architecture.md) | Frontière absolue entre outillage et applications. |
| [Configuration et CLI](../../exploitation/demonstration/configuration-cli.md) | Contrats, paramètres, artefacts et erreurs. |
| [Données](../../exploitation/demonstration/donnees-generation.md) | Profil réaliste, références et cohérence. |
| [Sauvegarde et restauration](../../exploitation/demonstration/installation-restauration.md) | Transfert transactionnel et reprise. |
| [Recette](../../exploitation/demonstration/realisation-recette.md) | Vérifications et parcours connectés. |
| [Bilan](livraison-recette.md) | Retrait des adaptations et preuves actuelles. |
| [Configuration de séance](../../../../localeo-backend/scripts/demonstration/examples/demo.example.json) | Commune, dates et alias. |
| [Profil opérateur](../../../../localeo-backend/scripts/demonstration/examples/operator.example.json) | Cibles et paramètres privés sans secrets. |

Une commune réelle et trois voisines accueillent des commerces et personnes
fictifs : 16 commerçants, 18 coffrets de deux à trois prestations, 9 actualités,
10 animations, 30 clients, 60 achats et 100 inscriptions. Les actions des
présentateurs font ensuite évoluer cette plateforme, via les parcours habituels.

[Retour à l’index des spécifications](../INDEX.md)
