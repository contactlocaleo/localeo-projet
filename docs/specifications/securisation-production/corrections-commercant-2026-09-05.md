# Corrections de l'audit Commerçant

> Consolidation du 18 septembre 2026 : les règles d'interface issues de
> `commercant/corrections-audit-2026-09-05.md` sont réunies avec les contrats
> serveur de `backend/corrections-audit-commercant-2026-09-05.md`.
> Les identifiants F01 à F16 et les compléments de recette sont conservés.
> Les constats, nombres de tests et mesures ci-dessous décrivent les corrections
> historiques du 5 septembre 2026 ; la consolidation ne les réexécute pas et
> ne constitue pas une nouvelle preuve de déploiement.

Ce document complète la spécification de la version décrite dans les sources.
Les règles ci-dessous ont été introduites au fil des correctifs validés.

## F01 — Isolation du cache entre sessions

Une réponse d'une session terminée ne peut ni alimenter le cache ni être remise à un écran d'une nouvelle session. La déconnexion invalide les lectures en cours. Chaque abonné peut annuler sa lecture sans annuler celle des autres abonnés. Une commande métier invalide également les lectures antérieures des ressources modifiées.

Validation : `src/features/animations/queries.test.js` et tests des pages Animation.

## F02 — Déconnexion immédiate

La déconnexion efface immédiatement l'état local, le stockage de session et le cache. La révocation distante utilise la session capturée avant nettoyage ; elle est bornée à huit secondes. Un réseau indisponible ne retarde pas le retour à l'accueil. Une révocation non confirmée ne doit pas être présentée comme confirmée. Un stockage navigateur désactivé ne doit pas faire échouer le nettoyage de l'état en mémoire.

Validation : `src/app/logoutMerchant.test.js` et tests du menu de compte.

## F03 — Pagination des listes Animation

Les listes complètes proposent les pages précédente et suivante. La page, la taille et le total fournis par le backend déterminent la présence d'une suite. Sans total, une page pleine permet de demander la suivante sans inventer un total. Les compteurs et catégories affichés portent explicitement sur la page courante. Le menu reste un aperçu de la première page. Les caches distinguent chaque page ; une décision de participation invalide toutes les pages concernées.

Validation : métadonnées de 51 invitations, total inconnu et navigation réelle vers la deuxième page Animation.

## F04 — Résultat des validations

Une validation confirmée par le serveur est immédiatement affichée comme enregistrée et retirée des prestations à valider. L'échec du rafraîchissement ultérieur n'annule pas cette confirmation. Si la réponse de l'écriture est indéterminée, aucune nouvelle validation de cette prestation n'est proposée avant vérification explicite du statut serveur. Un verrou synchrone empêche deux soumissions simultanées dans le même écran. Aucune écriture n'est relancée automatiquement.

Validation : `commitAndRefresh.test.js` couvre le succès du POST suivi d'un GET en erreur et la réponse d'écriture perdue.

## F05 — Indisponibilité de la vérification de session

Un refus d'authentification 401 invalide la session locale. Une indisponibilité réseau/serveur ou un refus de permission 403 conserve la session mais suspend les écrans et actions privés. Le commerçant peut réessayer la vérification ou se déconnecter ; aucune mutation métier n'est autorisée par cet état de repli.

Validation : tests de l'application avec réponse 500, nouvelle tentative et réponse 401 (`sessionAvailability.test.jsx`).

## F06 — Upload commerçant authentifié

Le formulaire utilise `POST /protected/profils/commercants/me/images` avec une session Bearer valide et le scope `commercant:profil`. Aucun upload anonyme ni repli sur l'endpoint administrateur n'est autorisé. L'identité du quota provient exclusivement de cette session. Les quotas persistants DAM et de stockage global restent applicables.

Les fichiers JPEG, PNG et WebP sont décodés, limités à 16 millions de pixels, réencodés sans métadonnées et limités à 5 Mio après réencodage. La lecture initiale reste bornée par la limite DAM configurée. Le refus de quota intervient avant la lecture du fichier par le handler.

L'ancienne écriture `/public/dam/images` reste réservée aux administrateurs ; elle n'est pas ouverte aux sessions commerçants. La lecture du backend a donc levé l'hypothèse d'upload anonyme de l'audit. Déployer la nouvelle route avant le frontend qui l'utilise. La lecture des images reste publique, conformément à leur destination de page commerciale.

Validation : test frontend `merchantImageUpload.test.js` et tests backend `tests/security/test_merchant_images.py`, `test_upload_security.py`, `test_dam_upload_controls.py`.

## F07 — Configuration publique explicite

Seuls les noms listés dans `config/publicEnvironment.js` peuvent être injectés dans le JavaScript. Les préfixes `VITE_` et `LOCALEO_` n'exposent plus automatiquement de variables. `.env`, `.env.local` et les variantes `.env.*.local` ne sont pas versionnés. Les fichiers de modes production/test conservés dans Git sont exclusivement des configurations publiques, contrôlées par un test sur les noms ; leurs valeurs ne doivent jamais contenir de secret. Les fichiers locaux sont conservés sur le poste.

Validation : une variable privée synthétique n'est pas injectée, et les noms des configurations versionnées appartiennent à la liste autorisée.

## F08 — QR dans le corps de la requête

L'ouverture de transaction transmet le JSON `{ "qr_coffret_instance": "…" }` sous session commerçant Bearer. Le frontend ne place plus le QR dans une URL et n'effectue aucun repli automatique vers une query string. Les logs et outils de diagnostic ne doivent pas enregistrer les corps contenant QR, tokens ou mots de passe.

Le paramètre query reste temporairement accepté et marqué obsolète dans OpenAPI pour permettre le déploiement backend avant frontend. Une requête fournissant les deux sources est refusée. Retirer cette compatibilité après mise à jour des clients et vérifier le filtrage des anciens journaux en exploitation.

Validation : `openTransaction.test.js` côté frontend ; JSON sans query, compatibilité transitoire et conflit rejeté sans appel métier dans `test_validation_qr_body.py` côté backend.

## F09 — Indisponibilité des données Finance

Une erreur sur une rubrique secondaire est affichée comme une indisponibilité ; elle ne produit jamais un faux compteur zéro. Un 401 invalide la session, y compris s'il provient d'une rubrique secondaire. Un téléchargement PDF en échec produit un message visible et permet de réessayer depuis le même bouton.

Validation : les tests de vue d'ensemble distinguent liste vide, rubrique indisponible et session expirée.

## F10 — Contrat implémenté et lecture des notifications

`api/localeo-openapi.json`, dans le dépôt commerçant, est son unique contrat de référence. Il est exporté depuis les routes effectivement enregistrées du backend avec `scripts/documentation/export_openapi_offline.py`, sans connexion externe ni configuration de déploiement. L'ancien doublon `docs/openapi.json` est supprimé. Le frontend synchronise son snapshot avant publication ; ses tests exécutent les clients HTTP avec un réseau simulé et vérifient chemins, méthodes et noms des champs JSON contre ce contrat.

`POST /protected/animation-locale/commercants/me/notifications/lire-tout` exige le scope commerçant Animation. La mise à jour atomique ne concerne que ses notifications non supprimées et non lues, dans sa commune courante. Une répétition n'altère pas les dates de lecture déjà enregistrées. La route partenaire homonyme n'est pas destinée à la PWA commerçant. Le compteur retourne les lignes modifiées par l'appel, pas une promesse de replay identique du compteur.

Les refus et retraits de participation utilisent le champ JSON `motif`. Déployer le backend correspondant avant le frontend.

La consultation `GET /protected/commercants/me/facturation/demandes-groupees/{demande_id}` retourne le détail après filtrage par identifiant de demande et commerçant de la session. Une demande appartenant à un autre compte reste introuvable. Le flag de facturation et le scope `commercant:validation` restent requis.

## F11 — Une lecture par page d'invitations

La liste affiche directement les résumés et snapshots fournis par le backend. Elle ne charge pas un détail de demande ou d'animation pour chaque ligne. Les informations absentes sont signalées ; leur chargement est différé jusqu'à l'ouverture de la demande, où la consultation complète avant décision reste obligatoire. Une page de 50 invitations nécessite une seule lecture de liste, hors nouvelle tentative réseau.

Validation : 50 résumés incomplets rendus avec un seul appel de liste et aucun appel de détail ; les tests de la page de détail et de confirmation restent actifs.

## F12 — Vérification du build et des en-têtes de livraison

Les tests navigateur servent un build optimisé, configuré avec des valeurs synthétiques et les en-têtes de `render.yaml`. Ils ne réutilisent pas un serveur de développement existant. Les appels API non simulés sont refusés et toute sortie réseau du navigateur hors du serveur local est bloquée. Un test vérifie CSP, nosniff, interdiction d'encadrement et blocage d'un script inline. Les contrats sont contrôlés séparément contre l'OpenAPI exporté du backend.

Lighthouse conserve ses rapports sur le système de fichiers, sans publication publique automatique. Un smoke test de l'environnement réellement déployé reste une vérification d'exploitation à effectuer après déploiement, avec des comptes synthétiques autorisés.

## F13 — Séparation des responsabilités

Les échanges d'authentification sont regroupés dans `features/session/api.js` et les échanges du profil, du support, des prestations et reversements dans `features/merchant/api.js`. L'application orchestre les écrans et appelle ces modules. Les anciennes fonctions locales dupliquant les modèles et clients extraits sont supprimées. Les règles de connexion, de validation de session et de révocation sont testées indépendamment des écrans ; les parcours existants sont rejoués après extraction.

Cette étape retire plus de 700 lignes à `App.jsx`. Le découpage des autres écrans reste progressif : cette refactorisation ne prétend pas réduire à elle seule le volume de JavaScript téléchargé.

Une seconde étape isole le scanner dans un module chargé à la demande et précharge les polices principales : voir [le chargement initial](chargement-initial-commercant.md).

## F14 — Durée de conservation des sessions

Voir [les protections et limites du Bearer](../identite-acces/session-bearer-commercant.md). L'expiration automatique et la vérification au retour au premier plan limitent la conservation d'une session expirée. Une migration HttpOnly reste une évolution coordonnée ; le risque d'accès JavaScript pendant une session valide n'est pas supprimé.

## F15 — Diagnostic navigateur

La route `POST /protected/support/commercants/me/incidents-ui` exige le scope `commercant:profil`. Elle reçoit uniquement une référence UUID préfixée UI, une catégorie fixe et une version. Le corps est limité à 1 Kio ; les erreurs de validation ne reflètent jamais le contenu reçu. Le quota indépendant limite chaque commerçant à cinq tentatives par minute par processus et refuse les nouveaux acteurs à saturation de ses 2 048 entrées.

L'événement structuré `merchant.ui.render_failed` associe référence UI, version frontend et corrélation HTTP de la collecte, sans identité, Bearer ni détail d'erreur. La collecte authentifiée est bornée et corrélée aux journaux backend ; voir [les règles de diagnostic et la procédure d'exploitation](../../exploitation/commercant/diagnostic-incidents.md).

Aucun changement de politique de rétention ni configuration d'alerte externe n'est implicite. L'exploitation doit vérifier la collecte, les accès aux logs, les alertes et la restauration réelle d'une sauvegarde dans un environnement isolé avant de considérer ces capacités comme validées.

## F16 — Révocation Chorus

Les commandes de mandat sont verrouillées pendant leur exécution et suivies d'une relecture serveur. Une réponse perdue ne provoque aucun rejeu automatique. Un état serveur indisponible bloque les nouvelles commandes jusqu'à une nouvelle vérification ; les erreurs d'authentification rendent la main au parcours de connexion. Les tests de `ChorusPage` couvrent ces situations.

## Complément F12 — Dépendances et mesures Lighthouse

L'audit npm autorisé a révélé 13 alertes dans les dépendances de l'ancienne CLI Lighthouse, contre aucune dans les dépendances de production. La CLI est remplacée par Lighthouse 13.4.1 et un lanceur local. Le lockfile mis à jour ne présente plus d'alerte lors de la vérification du 5 septembre 2026 ; ce résultat doit être réévalué régulièrement.

`npm run test:lighthouse` construit le bundle synthétique, applique les en-têtes Render et bloque les requêtes navigateur externes. Les rapports restent dans `tmp/lighthouse-reports`. Les seuils explicites existants d'accessibilité, de bonnes pratiques, de performance, FCP, LCP, CLS et TBT sont conservés et vérifiés sur la médiane de trois exécutions. Une métrique manquante échoue au contrôle correspondant. Les règles implicites du preset de l'ancienne CLI ne sont plus appliquées ; les budgets suivis sont ceux déclarés dans `lighthouserc.json`. Le contrôle porte sur l'écran de connexion local et ne mesure ni le backend réel ni tous les écrans authentifiés.

Lighthouse 13 nécessite Node 22.19 ou une version supérieure compatible ; la CI utilise Node 22 à jour.

## Vérification finale locale

- Frontend : 148 tests unitaires et d'intégration réussis dans 33 fichiers, lors du rejeu isolé.
- Navigateur : huit parcours Chromium réussis sur build compilé, avec API synthétiques, en-têtes de sécurité et compression.
- Backend : 33 régressions ciblées réussies, avec SQLite ou doubles de test et connexions externes interdites.
- Compilation de production réussie ; audit npm du lockfile sans alerte le 5 septembre 2026, y compris l'outillage.
- Lighthouse, médiane de trois mesures : accessibilité 100/100, bonnes pratiques 96/100, performance 83/100, FCP 1,97 s, LCP 2,47 s et CLS inférieur à 0,001. Tous les seuils bloquants passent. Le TBT médian de 431 ms dépasse le seuil d'avertissement de 300 ms ; il reste à surveiller. Ces mesures locales ne constituent pas une mesure de production.

Déployer les routes backend avant le frontend. La migration HttpOnly (F14), les alertes et exercices réels de restauration (F15), ainsi que le retrait de la compatibilité QR query après migration des clients (F08), restent des actions coordonnées de déploiement/exploitation. Aucun déploiement ni test de production n'a été effectué ici.

## Complément F12 — Contrôle du déploiement réel

La commande `npm run test:deployment` vérifie les en-têtes et le contrat des URL explicitement fournies. Voir [la procédure et ses limites](../../exploitation/commercant/verification-deploiement-audit.md). Les tests locaux couvrent ses refus et ses bornes ; son exécution en préproduction reste à effectuer avec les URL de cet environnement.
