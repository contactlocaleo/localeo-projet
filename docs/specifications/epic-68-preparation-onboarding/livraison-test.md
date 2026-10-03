# Livraison TEST de l’EPIC 68 — 3 octobre 2026

Ce reçu complète la [vérification de livraison](verification-livraison.md). Il ne
clôture pas l’epic et ne vaut pas recette de production.

## Références du lot

| Dépôt | Révision |
| --- | --- |
| Projet, sources du bundle | `2ea629252451010cf3ee0e4065d84c7a791b6257` |
| Backend et ERP | `651df1b6c8b7c9140a26d6cb5d743727bd8f90e5` |
| Commerçant | `74a797ab99cc4f2eda4749bf976d2e864498e2d7` |
| Marketplace, inchangé | `4e948f1f52ffb86a3bf992e015ce6107daae6545` |
| Animation, inchangé | `cac5eb431b3d8a8a18bc1311635f4f2f9e78c27c` |

Les modifications CRM de l’EPIC 71 restent hors de ce lot. Les branches de
production et de démonstration ne sont pas modifiées.

## Base et configuration TEST

Les migrations additives `v254_epic68_preparation.sql` et
`v255_communications_preparation_onboarding.sql` ont été appliquées le
3 octobre 2026 à 08:09 UTC, après vérification explicite de la cible TEST et de sa
différence avec la cible de production. Les quatre tables E68 et la politique
initiale sont présentes. Aucun dossier historique n’a été repris.

Une sauvegarde PostgreSQL 18 de 31 902 574 octets a été créée avant migration.
Sa table des matières a été lue avec `pg_restore --list` ; sa restauration n’a pas
été répétée sur une autre base. Les sauvegardes et reçus opérateur restent privés
sous `.artifacts/epic68-test-delivery/` dans le backend.

Le module OnBoard est activé sur TEST, vérifié par la réponse authentifiée
`featureEnabled=true`. La politique de communications E68 reste **inactive**.
Aucun email ni SMS n’a été envoyé pour cette livraison. Avant activation :
approbation éditoriale des deux supports (ARB-07), coordonnées Localeo et URL TEST
de préparation, contrôle des expéditeurs et du mode des transports. Chaque
séquence reste soumise à confirmation explicite.

## Preuves locales

- Les lots métier, API, concurrence PostgreSQL et navigateurs sont détaillés dans
  la vérification de livraison. Les sources ont été commitées après ces tests ;
  seuls deux blancs de fin de fichier de test et la révision du bundle ont été
  ajustés pendant la préparation de livraison.
- Le build Commerçant `vite build --mode test` a réussi.
- Le profil démonstration strict sur PostgreSQL 18.3 a réussi : **5 tests,
  aucun skip**, 2 avertissements SQLAlchemy, 19 min 48. Il vérifie construction,
  installation, échec simulé du reset, restauration et rafraîchissement du schéma
  sur des bases jetables. Les clusters ont été arrêtés. Aucun jeu partagé n’a été
  régénéré. Le premier essai PG11 a échoué pour incompatibilité avec les outils
  PG18 ; il est conservé comme échec, sans neutralisation d’assertion.
- Le bundle a été reconstruit depuis la révision documentaire publiée :
  **122 exports, 123 documents distribués et sources vérifiés**, manifeste inclus.
  Le backend épingle cette révision exacte.
- Le hook documentaire du commit a validé 17 guides et 289 liens, sans erreur ni
  avertissement.

## Limites du contrôle global

Le profil workspace n’est pas entièrement vert : collecte backend bloquée par
quatre collisions de noms de modules de test préexistantes ; avec le mode
`importlib`, première assertion préexistante sur la redirection OnBoard
(`/admin/login` attendu, `/internal/connexion` réel), après 102 réussites et
3 skips. Le lint Marketplace rencontre un répertoire de sortie local inaccessible.
Ces échecs n’ont pas été masqués.

Les contrôles de contrats Commerçant et Marketplace ont d’abord échoué sur des
fins de ligne CRLF du checkout Windows. Les fichiers ont été remis aux octets LF
des blobs Git, après comparaison avec les manifestes ; les deux lots ciblés
passent ensuite (3 tests chacun), sans changement de contrat versionné.

Le manifeste automatique `.artifacts/quality/e68-test-release.json` reste
`blocked` : rapport workspace incomplet, preuves capturées avant commit et arbre
documentaire contenant encore les travaux E71. Sa comparaison avec cet arbre
diffère du bundle épinglé ; le contrôle indépendant du bundle publié a réussi.
Ce manifeste ne constitue donc pas un feu vert global ni une preuve de livraison.

## Vérification sur la cible

À 08:39 UTC, les versions backend `1.0.0+651df1b` et Commerçant `74a797a`
ont été constatées sur `https://test-backoffice.localeo.city` et
`https://test-commercant.localeo.city`. Les nouvelles routes sont présentes dans
le contrat OpenAPI authentifié (704 chemins). Les accès anonymes aux données de
préparation et à la politique sont refusés (401). La session administrative, la
liste des dossiers, la préparation d’un dossier et la lecture de la politique
répondent 200. La politique est inactive. Le frontend contient la route de
préparation et le SHA attendu.

**Livraison technique partielle : le bundle documentaire est indisponible sur
Render.** Le guide E68 et la page de configuration documentaire renvoient 503 ;
la politique expose zéro support disponible au lieu de deux. Le bundle construit
localement depuis le commit publié est valide. L’opérateur a confirmé que la
Build Command actuelle est seulement `pip install -r requirements.txt` : elle ne
prépare pas le bundle. Aucun accès d’administration Render n’est disponible dans
cette session.

Pour débloquer, remplacer la Build Command du backend TEST par :

```bash
pip install -r requirements.txt && python scripts/documentation/prepare_documentation.py
```

Laisser `LOCALEO_DOCUMENTATION_ROOT` non définie pour le chemin standard, ou la
définir à `/opt/render/project/src/.runtime/documentation`. Redéployer puis vérifier
le guide (200) et les deux supports disponibles. Définir cette variable seule ne
crée pas le bundle. Voir la [procédure canonique](../../exploitation/technique/reference-documentation-centralisee.md).

L’endpoint readiness refuse la clé batch du fichier opérateur local (403) ; ce
contrôle distant n’est pas validé. Les preuves de schéma sont la migration et la
vérification SQL explicite de TEST, complétées par les lectures E68 réussies.

Le contrôle officiel du déploiement Commerçant relève des en-têtes CSP,
`X-Frame-Options` et `Referrer-Policy` manquants sur accueil/profil. L’absence de
CSP avait déjà été observée avant publication. Son appel anonyme au contrat
OpenAPI est refusé ; le contrôle authentifié des routes a été exécuté séparément.
Aucune de ces limites n’est transformée en résultat vert.

Les onze jobs GitHub backend sont en échec avec les mêmes causes que le commit
précédent : collisions de tests, répertoire `tmp` absent en CI, fixtures Animation,
alertes de dépendances et contrôles sécurité préexistants. La comparaison des
alertes n’a identifié aucune nouvelle détection. La CI reste rouge.

Après commit, dix tests des supports et du guide passent avec la révision backend
et le bundle publié exacts. La recette réelle accompagnée, la délivrabilité
fournisseur et le pilote restent distincts de ces contrôles techniques.
