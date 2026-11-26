# EPIC 83 — Clés d’accès dans Localeo Pro

## Références

- **État produit · En cours.** Suivi ouvert le 24 novembre 2026 après la réalisation locale. La [roadmap commune](../README.md) porte le classement.
- [Spécification canonique](../../specifications/epic-83-cles-acces-localeo-pro/README.md) et [preuves locales](../../specifications/epic-83-cles-acces-localeo-pro/README.md#preuves-locales).
- Socles utilisés · [EPIC 10 — Connexion par mot de passe](../terminees/epic-10-authentification-commercant-login-password-backlog.md) et [EPIC 72 — Accès salariés](../terminees/epic-72-acces-salaries-validation-localeo-pro-backlog.md). L’inscription WebAuthn, la gestion des clés et le pilotage par environnement constituent le périmètre de l’EPIC 83.

## Problème et résultat attendu

Les titulaires et les salariés saisissent aujourd’hui leur email et leur mot de passe pour se connecter à Pro. Une fois leur clé d’accès créée, ils pourront ouvrir la même session en confirmant sur leur appareil, sans ressaisir ces informations. Le mot de passe et la récupération par email restent disponibles.

## Périmètre

- Ajouter la connexion WebAuthn et guider la première inscription depuis Pro. Permettre à chaque titulaire ou salarié de gérer ses propres clés.
- Permettre à un administrateur d’activer ou de désactiver la fonctionnalité par environnement depuis Localeo Ops. Livrer la fonctionnalité désactivée par défaut.
- Le périmètre couvre l’authentification de Pro. Les sessions support, l’authentification des autres applications et les actions métier accessibles après connexion suivent leurs propres règles.

## Critères d’acceptation

Les identifiants **CL-01 à CL-06** sont ceux de la spécification.

| Critère | Acteur et préconditions | Action | Résultat observable |
| --- | --- | --- | --- |
| CL-01 · Découverte et création | Titulaire ou salarié connecté par mot de passe | Suivre l’invitation ou ouvrir **Mes clés d’accès** | L’intérêt est expliqué, la création est guidée et le retour à l’activité est possible. **Plus tard** laisse le menu accessible. |
| CL-02 · Connexion et droits | Titulaire ou salarié avec une clé | Choisir **Se connecter avec une clé d’accès** | La session s’ouvre sans saisie d’identifiant. Le salarié retrouve le scanner et ses droits actuels. La gestion du PIN exige toujours le mot de passe. |
| CL-03 · Refus et récupération | Compte personnel avec une ou plusieurs clés | Retirer une clé, réinitialiser le mot de passe par email ou présenter une preuve refusée | Le retrait ferme les sessions de la clé. La réinitialisation retire les clés et ferme les sessions du seul compte concerné. Une preuve expirée, rejouée ou issue d’une autre origine ne crée pas de session. |
| CL-04 · Pilotage | Administrateur dans Localeo Ops | Activer, désactiver puis réactiver | La bascule s’applique à la cible choisie. L’arrêt ferme les sessions ouvertes par clé à leur prochaine requête. La réactivation accepte une nouvelle connexion avec une clé conservée. |
| CL-05 · Appareils | Titulaire ou salarié sur navigateur ou PWA | Créer une clé, se reconnecter puis annuler une demande | Le parcours est praticable sur les téléphones retenus. Le formulaire par mot de passe reste disponible après annulation ou indisponibilité. |
| CL-06 · Livraison | Backend migré, état initial désactivé | Servir une version de Pro avant et après l’ajout des clés d’accès | Le mot de passe fonctionne avec les deux versions et demeure accessible si la lecture de l’état échoue. |

## Impacts

| Sujet | Impact et référence |
| --- | --- |
| Applications et domaine | **Concernés** · Localeo Pro et le backend Identité et accès, avec la commande d’activation dans Localeo Ops. |
| API et consommateurs | **Concernés** · Backend producteur, Pro consommateur. [OpenAPI canonique](../../specifications/epic-41-api/openapi.json) et [contrat embarqué](../../../../localeo-commercant/api/localeo-openapi.json). |
| Persistance | **Concernée** · Migration PostgreSQL `v334` pour les clés, les demandes de vérification et le rattachement des sessions. |
| Démonstration | **Concernée pour la recette** · Utiliser les comptes synthétiques et créer les clés depuis leur navigateur. |
| Documentation fonctionnelle | **Concernée** · [Guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md), captures et PDF embarqué. Le guide Animation couvre un autre parcours de connexion. |
| Exploitation | **Concernée** · `LOCALEO_PRO_PASSKEY_ORIGIN` sur le backend, migration avant livraison du backend, puis livraison de Pro. [Procédure de configuration et de bascule](../../exploitation/exploitation/localeo-ops.md#authentification-localeo-pro). |

## Vérifications restant à mener

Le backend, les contrats et les parcours Chromium ont des preuves locales. La recette sur iPhone Safari et Android Chrome physiques, la bascule sur les cibles et les mesures de latence et de contention sur une cible de livraison restent à réaliser avant l’activation utilisateur.
