# Suivi des corrections avant ouverture — 5 septembre 2026

Périmètre : rapport Marketplace / Localeo Live, référence initiale `d823251`. Les commits ci-dessous sont séparés par anomalie et poussés sur `origin/main`. Les changements préexistants du compteur d'animations et de la typographie Live sont conservés hors de ces commits. Les tests portent sur cet arbre de travail, qui inclut ces changements préexistants.

Les règles et limites détaillées sont dans [la spécification de sécurisation](../../specifications/securisation-production/ouverture-marketplace.md). **Un correctif frontend testé ne certifie ni le backend ni la configuration réellement déployée. L'ouverture en production n'est pas encore validée.**

## Constats F01–F16

| Constat | Livraison | État et validation restante |
|---|---|---|
| F01 — Jeton de chemin conservé dans Analytics | Non livré | Arbitrage demandé : suspension temporaire d'Analytics ou validation de sa configuration réelle. Ne pas prétendre supprimer les émissions automatiques par le seul filtrage du wrapper. |
| F02 — Filtre SVG contournable | `dd0e088` | Rendu en image passive ; charge malveillante inerte en Chromium sans CSP, QR conservé. Vérifier aussi la CSP de l'origine déployée. |
| F03 — Coordonnées d'achat en query string | Non livré | Backend local encore fondé sur les paramètres d'URL. Coordonner migration JSON côté API, contrat OpenAPI, tests backend puis bascule frontend ; aucun retour silencieux vers des URL contenant les coordonnées. |
| F04 — Diagnostic QR public | `618b7da` | Token/payload/KID retirés du rendu, query nettoyée sans persistance. Le transport du token vers l'API reste à migrer avec F03. |
| F05 — Retrait du consentement | Non livré | Même arbitrage Analytics que F01 ; contrôler le tag chargé, les émissions automatiques, les cookies et les autres onglets. |
| F06 — Cache PWA trop général | `caae186` | Cache réservé aux ressources publiques, exclusion des capacités et réponses privées, purge des anciennes versions sensibles. Complété par F12. |
| F07 — Création concurrente d'installations | `27d8030` | Promesse partagée et verrou multi-onglets testés. Reste l'idempotence/récupération API après perte de réponse ou panne de persistance ; pas de réconciliation automatique des anciennes identités. |
| F08 — Formulaire Live historique divergent | `01730fc` | Branche morte retirée du catalogue ; reprise du formulaire partagé testée avec la même clé. |
| F09 — Pagination dans l'ancienne commune | `dde9602` | Génération, annulation et rejet des réponses/erreurs tardives, y compris mise à jour React différée. |
| F10 — Délais et annulation HTTP | `151a5e3` | Tous les helpers bornés, corps compris ; écritures interrompues signalées comme incertaines, sans retry automatique. Récupération métier après rechargement et unicité serveur à vérifier. |
| F11 — Erreurs filesystem/stream | `c95085b` | Pannes simulées confinées à la requête, serveur toujours joignable après incident. |
| F12 — Assets et reprise de version | `2662436`, `be9ae41` | 404 assets, préchargement lié au build, cache public N-1, entrée SPA et mise à jour consentie. Rétention N-1 de l'hébergement et essai réel de bascule/rollback encore requis. |
| F13 — Restauration non atomique | `8a17a69` | Validation complète et transaction unique vérifiées dans IndexedDB réel, avec pannes synchrones/asynchrones et aller-retour export/import. |
| F14 — Image d'accueil trop lourde | `aeba3d4` | WebP 93 312 / 232 292 octets ; rendu et sélection vérifiés à 390/800/1440 px. Image toujours non téléchargée sur mobile où elle est masquée. |
| F15 — Fiche bloquée par l'annuaire | `459301b` | Coffret et achat accessibles avant réponse marchande et après erreur ; coût O(N) restant à mesurer. |
| F16 — Tests couplés à une API distante | `bf17bbd`, `e425fb7` | Fixtures et refus réseau par défaut, serveur local non réutilisé, garde API sans proxy distant ; recette finale sur le bundle et les en-têtes de production. |

## Observations supplémentaires

| Sujet | État |
|---|---|
| Compression HTTP | Corrigée et poussée, `db1ba80` : facteurs q, exclusions, joker et 406 ; dix tests serveur passent. |
| Redirection checkout pro | Corrigée et poussée, `a5f2f89` : validateur HTTPS commun testé ; domaines autorisés du prestataire à confirmer avant restriction par origine. |
| Contraste de confirmation particulier, découvert sur le build production | Corrigé et poussé, `7705fac` : thème indépendant de l'ordre de chargement CSS ; quatre états et deux ordres testés, puis contraste mesuré sur la page réelle. |
| Documentation de routage/stack et installation | Mise à jour BrowserRouter, Router 7/Vite 8, installation à partir du lockfile. |
| Fichiers `.env` suivis | À traiter avec l'exploitant : aucun secret démontré, valeurs et historique non examinés. Ne pas purger/révoquer ou retirer une configuration de déploiement sans analyse d'impact. |
| Préfixes publics du build et ordre des `.env` | Restent à corriger avec des fixtures de configuration fictives et vérification des modes de déploiement. Aucun secret exposé n'est affirmé. |
| Minimisation/expiration du stockage local | Politique métier de durée/révocation à définir sans casser le carnet hors ligne. L'import atomique ne clôt pas cette question. |
| Messages API | Délais/incertitude normalisés ; revue des autres messages métier encore nécessaire pour éviter les détails techniques sans masquer les règles de gestion. |
| Autorisations, isolation objets/tenants, JWT, CORS/CSRF, injections, quotas, webhooks | Pas de preuve de correction globale depuis le frontend : tests backend dédiés et matrice de droits nécessaires. |
| Sauvegardes BDD, migrations, rollback, TLS/CDN, CI déployée, observabilité et SLO | Validation d'exploitation à documenter avec preuves ; ni charge distante ni test intrusif effectués. |

## Vérifications transversales

- Sécurité : 28/28 tests réussis lors de la dernière campagne complète, sur données fictives, sans API distante.
- Serveur : 10 tests réussis sur serveur local.
- Build production isolé et lint réussis ; le lint exclut `tmp/**`, utilisé par d'autres travaux concurrents.
- Installation depuis le lockfile vérifiée à blanc : `npm ci --dry-run --ignore-scripts --offline --no-audit --no-fund` réussit ; aucune réinstallation ni exécution de scripts d'installation effectuée.
- Suite navigateur finale : **48/48 réussis**, en 8 minutes, sur le bundle compilé et le serveur Node avec ses en-têtes de production.
- Historique de recette : campagne Vite 42/48, puis 5/6 en relance (timeouts locaux) ; première campagne compilée 47/48, révélant le défaut réel de contraste corrigé par `7705fac`. Le budget fonctionnel définitif est de 90 s par scénario ; les délais API de l'application ne sont pas augmentés. Voir [le profil de recette](../../exploitation/marketplace/recette/tests-isoles-production.md).
- Aucun test de charge, paiement réel, purge d'historique ou de données, révocation de jeton ou modification des réglages Analytics distants.

## Décisions nécessaires pour poursuivre

1. Confirmer la suspension temporaire d'Analytics, ou fournir le contexte de configuration permettant de valider F01/F05 sans l'interrompre.
2. Identifier l'environnement et le processus autorisant un déploiement backend compatible JSON avant activation du nouveau contrat Marketplace (F03).
3. Valider avec l'exploitation les preuves restantes : origines de paiement, rétention d'assets N-1, CSP/TLS effectifs, idempotence serveur et restauration/rollback.

Les rapports et modifications déjà présents dans les dépôts commerçant/backend ne sont pas incorporés à ces commits. Ce suivi ne remplace pas leur audit propre.
