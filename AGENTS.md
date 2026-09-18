# Guide transverse Localeo

Lire le [README](README.md), la spécification du périmètre, les [conventions transverses](docs/architecture/transverse/README.md) et les instructions locales de chaque application touchée avant de modifier son code.

- Conserver les cinq dépôts Git indépendants. Documenter les applications affectées et les contrats partagés ; ne pas créer une documentation concurrente par application.
- Le domaine backend porte les règles métier ; l’application orchestre et les interfaces présentent. Respecter les instructions techniques locales.
- Les statuts de la roadmap commune priment sur les anciens détails de story. Ne pas transformer une divergence historique en nouvel arbitrage implicite.
- Modifier les sources canoniques ici, y compris les contrats OpenAPI documentaires du backend. Les lecteurs utilisent ce dépôt ou un bundle de déploiement généré depuis documentation.exports.json, contrôlé par empreintes et non versionné dans le backend.
- Conserver les générateurs et outils exécutables dans leur dépôt applicatif. Les contrats embarqués par les frontends restent auprès de leurs consommateurs. Ne pas déplacer les données de démonstration, secrets, imports ou sorties de travail dans ce dépôt documentaire.
- Préserver les modifications utilisateur. Adapter les liens relatifs au workspace, exécuter les vérifications proportionnées, puis rendre compte des dépôts modifiés et limites constatées.
- Les commits, push et déploiements sont des opérations distinctes ; suivre la demande en cours. Ne jamais déposer les quatre applications dans un Git parent.

Les guides voisins ne sont pas hérités automatiquement : leurs AGENTS.md renvoient explicitement à ce fichier. Si un dépôt voisin manque, le signaler et continuer les tâches qui n’en dépendent pas.
