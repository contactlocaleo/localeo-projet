# Installation et mise à jour des applications Localeo

Évolution `PWA-20260929`, demandée le 29 septembre 2026. Elle étend les surfaces existantes sans rouvrir leurs clôtures historiques : [Live, EPIC 42](../roadmap/terminees/epic-42-localeo-live-grand-public-backlog.md), [Animation, EPIC 41](epic-41-api/README.md), [espace commerçant](espace-commercant/README.md), [Atelier, EPIC 66](epic-66-localeo-atelier/README.md), [OnBoard](epic-50-conformite-fiscale-bum/onboarding-commercant-mobile.md), [Ops](../exploitation/exploitation/localeo-ops.md) et [Support](../exploitation/exploitation/localeo-support.md). Localeo Control conserve son fonctionnement existant.

## Parcours utilisateur

Le header propose **Installer** tant que l'installation n'est pas connue du navigateur. Sur Android compatible, le bouton ouvre la demande native, que l'utilisateur peut accepter ou refuser. Sans cette possibilité, une aide indique le menu du navigateur. Sur iPhone/iPad, elle guide vers Safari, **Partager**, **Sur l'écran d'accueil**, puis **Ajouter**. Fermer l'aide n'enregistre jamais une installation réussie. Aucune installation ni permission de notification n'est déclenchée automatiquement.

Le bouton disparaît dans l'application ouverte en mode autonome et après confirmation native de l'installation. La détection n'est pas universelle : Safari ne permet pas à une page ordinaire de savoir avec certitude qu'une autre copie existe sur l'écran d'accueil. Aucun indicateur persistant supposant indéfiniment l'application installée n'est ajouté.

Une version plus récente détectée est proposée par un bouton **Mettre à jour** ou un bandeau équivalent. L'utilisateur peut continuer son travail et revenir à la proposition. La mise à jour demande une action explicite ; les saisies à terminer sont signalées avant le rechargement. Une activation faite dans un autre onglet ne recharge pas celui-ci. L'échec laisse un message et permet de réessayer. Hors ligne, aucune opération métier n'est rejouée et aucun succès de mise à jour n'est inventé.

## Critères d'acceptation

| ID | Comportement à vérifier | Preuve attendue |
| --- | --- | --- |
| PWA-CA1 | Les sept headers offrent l'installation ; le mode autonome et `appinstalled` masquent l'action | Tests des headers, simulation du mode autonome et événement navigateur |
| PWA-CA2 | Demande native unique, refus réessayable, aide iOS et navigateur de secours | Tests clics concurrents, refus, clavier, fermeture et restitution du focus |
| PWA-CA3 | Une modification des fichiers livrés produit une version détectable ; retour au premier plan vérifie les mises à jour | Tests de version par contenu et de retour dans l'application |
| PWA-CA4 | Mise à jour seulement après accord, pas de rechargement forcé des autres onglets ni activation automatique | Cycle réel entre deux workers, conservation d'une saisie dans un autre onglet |
| PWA-CA5 | Échec et réseau indisponible sont récupérables, doubles clics bloqués | Tests des erreurs, bouton occupé, réessai |
| PWA-CA6 | Aucun nouveau cache d'API, document privé, jeton ou page authentifiée ; droits et sessions inchangés | Tests SW et accès aux ressources publiques exactes, non-régression sessions |
| PWA-CA7 | Boutons et aides utilisables au clavier, sur mobile et bureau ; installation réelle iOS/Android | Recette navigateur responsive puis recette sur appareils physiques |
| PWA-CA8 | Sur mobile, le header principal reste sur une seule rangée, sans débordement ni recouvrement, même avec installation, mise à jour et compte visibles | Contrôles géométriques à 320, 360, 390 et 720 px ; boutons tactiles d’au moins 44 px, libellés accessibles et menus utilisables |

Correction du 9 octobre 2026 : les actions du header deviennent compactes sur
mobile, avec leurs noms accessibles conservés. Les noms longs sont tronqués si
nécessaire et restent consultables via les menus correspondants. Les menus,
dialogues et messages ouverts ne sont pas contraints à une ligne : leur contenu
doit rester lisible. Ce comportement concerne Pro, Live, Animation et le header
partagé OnBoard/Ops/Support/Atelier (également utilisé par l’ERP), ainsi que le
header distinct de Control. Control conserve son fonctionnement PWA existant.

### Vérification du header mobile — 9 octobre 2026

Les règles ajoutées avec l’installation PWA autorisaient explicitement le retour
à la ligne des actions. Le défaut a été reproduit avant correction sur Pro
(décalage vertical de 51 px à 320 px), Live (48 px) et le header interne partagé.
Les captures corrigées à 320 px ont été inspectées pour Pro, Live, Animation et
OnBoard. Les actions restent nommées pour les lecteurs d’écran et accessibles
dans les menus/dialogues ; aucun traitement métier ou protocole PWA ne change.

| Surface | Preuves locales |
| --- | --- |
| Pro | 6 scénarios de header à 320/360/390/720/768/820 px, 3 scénarios PWA (accessibilité et cycle réel du worker), 19 tests Vitest et build isolé réussis |
| Pro salarié | Depuis `E72-CORR-20261009-UX` : en-tête et navigation partagés avec le principal, menu du compte réduit et entrées Scanner/Historique ; une rangée vérifiée à 320/390 px et présentation desktop à 1 280 px dans les scénarios navigateur E72 |
| Live | 6 scénarios de header aux mêmes largeurs, 5 tests de mise à jour et ESLint ciblé réussis ; état installé et ouverture des réglages vérifiés |
| Animation | Recette PWA à 320/360/390/720/1280 px avec installation et mise à jour simultanées, commune longue, clavier et dialogues ; 9 tests PWA, build isolé, types et lint réussis |
| OnBoard/Ops/Support/Atelier et ERP | `node tests/browser/header-mobile.cjs` réussi sur les cinq identités à 320/360/390/720/768/820 px : même rangée, absence de recouvrement/débordement, cibles de 44 px, navigation et aide d’installation ; 24 tests Python PWA réussis |
| Control | `node tests/browser/control-header-mobile.cjs` (Python du projet via `TEST_PYTHON`) réussi à 320/360/390/720/1280 px : header compact, action administration de 44 px, absence de chevauchement et navigation clavier ; capture 320 px inspectée. Extraction isolée du HTML, polices réseau bloquées : rendu de repli contrôlé |

Suite backend finale après adaptation de Control : **491 tests réussis**, dont
les contrôles d’architecture obligatoires et les 24 tests PWA. Documentation :
93 guides, 977 liens locaux et 122 sources exportées vérifiés sans erreur.

Limites indépendantes : le scénario étendu `pwa-lifecycle.cjs` bloque sur le champ
Support `[name="description"]`, avec le header corrigé **et avec les ressources
du HEAD antérieur**. Cette recette complète ne constitue donc pas une réussite
pour ce lot ; le test ciblé des headers passe. Le lint global Marketplace rencontre
un accès refusé à `output/demo-generation/pytest-bum-registry` ; le lint des deux
sources modifiées passe. Aucun changement API, SQL, habilitations, données de
démonstration ou configuration d’exploitation. Pas de déploiement ni de recette
sur appareils physiques réalisés pour ce correctif.

## Architecture et impacts

Chaque dépôt conserve son mécanisme de livraison. Les interfaces possèdent l'installation et la présentation de mise à jour ; aucune règle métier n'est déplacée depuis le domaine backend. Les applications internes mutualisent ces commandes dans leur header, avec identités et scopes propres. L'ERP classique ne devient pas une PWA.

Les frontends utilisent leurs versions de contenu de build et le cycle des service workers. Le backend utilise une empreinte de ses ressources UI pour les applications internes ; les informations publiques de version ne contiennent aucune donnée de session ou métier. Les anciens liens restent accessibles. L'activation explicite est compatible avec les versions précédentes qui ne connaissent pas encore le nouveau protocole.

| Impact | Traitement |
| --- | --- |
| Applications | Backend (Ops, Atelier, Support, OnBoard), Marketplace (Live), Animation, Commerçant |
| Contrats métier/OpenAPI | Sans impact : aucune commande ou réponse métier modifiée ; les ressources PWA sont des ressources de présentation |
| Authentification | Shells et API internes toujours protégés ; seules les ressources PWA publiques explicitement listées sont anonymes |
| Données et migration | Sans impact SQL : aucun nouveau champ ni changement de données |
| Générateur de démonstration | Sans impact sur fixtures, habilitations et données générées ; tester les mêmes interfaces dans le jeu existant |
| Coexistence | Ancien onglet conservé ; proposition de recharger uniquement cet onglet après consentement |
| Installation existante | Ne pas changer d'identité manifest ni demander une désinstallation ; conserver les liens d'entrée historiques |

## Utilisation et exploitation

Installer depuis le header, puis ouvrir l'icône créée sur l'écran d'accueil. Pour mettre à jour, terminer les saisies puis utiliser le bouton ou bandeau proposé. L'installation ne donne aucun droit supplémentaire et ne remplace pas la connexion. Les notifications gardent leur consentement distinct.

Servir en HTTPS les manifests, icônes et workers, avec leurs types MIME corrects. Le worker et les informations de version doivent être revalidés, pas figés dans un cache CDN. Livrer HTML, scripts, styles et empreinte de version ensemble. Aucun paramètre secret supplémentaire n'est nécessaire. Le backend et les trois frontends peuvent être livrés indépendamment ; aucun ordre SQL n'est requis.

Après livraison, ouvrir une version précédente, déployer la suivante, revenir au premier plan et vérifier la proposition. Contrôler qu'un second onglet garde sa saisie, puis accepter dans le premier. Tester Safari iOS depuis l'écran d'accueil et Chrome Android, y compris réseau coupé puis rétabli. En cas d'absence de proposition, contrôler HTTPS, scope, version, réponse du worker et caches d'hébergement avant d'effacer des données utilisateur. Un rollback livré comme une nouvelle empreinte suit le même accord explicite.

## Preuves et limites

Arbres locaux fondés sur Projet `0c5b0d9`, Backend `a28592d`, Marketplace `68f4823`, Animation `802212c`, Commerçant `185c8aa`. Les modifications Atelier V1.2 déjà présentes sont conservées ; leurs résultats antérieurs ne constituent pas une preuve de cette évolution.

| Dépôt | Contrôles exécutés et portée |
| --- | --- |
| Marketplace / Live | `node --test tests/security/live-update.test.cjs` : 13 succès (versions, confidentialité du cache, erreurs, multionglets et retour foreground). ESLint ciblé : succès. Playwright `live-install-header`, `live-update`, `live-update-lifecycle` : 11 succès avec build production isolé, vrai cycle SW et contrôle des boutons à 320/390/1440 px. Captures inspectées ; aucun débordement de header après correction. |
| Animation | 9 tests PWA ciblés, types et lint : succès. `node scripts/build-pwa-tests.mjs` et `node tests/browser/pwa-smoke.mjs` : succès ; vrai SW, deux onglets, réseau/caches, aide iOS simulée, clavier et headers à 320/390/1280 px. |
| Backend | 73 tests Python ciblés et 10 tests Node OnBoard réussis. `node tests/browser/pwa-lifecycle.cjs` : quatre headers, vrais workers, passage depuis les workers historiques Ops/Atelier, formulaire Support modifié avec une seule confirmation, conservation de la saisie du second onglet, version déjà chargée, session, double clic et hors connexion. `node tests/browser/atelier-pwa.cjs` : non-régression session et isolation Atelier réussie. Captures header 390 px inspectées. |
| Commerçant | Build isolé `node scripts/build-browser-tests.mjs` réussi. Vitest isolé : 30 succès puis 9 tests lifecycle après le dernier scénario réseau (31 tests distincts). Playwright/Axe final : 5 succès, dont deux versions réelles du SW, annulation, coupure réseau, deux onglets et saisie conservée. Capture mobile inspectée. |
| Projet | `check_guidance.py` avec les documents PWA et OnBoard : 89 guides, 908 liens locaux, zéro erreur/avertissement. `sync_documentation.py --check-sources` : 118 documents vérifiés. `git diff --check` réussi dans les cinq dépôts. |

La fermeture automatique du serveur Playwright Marketplace est restée bloquée sous Windows après les 11 scénarios réussis ; le seul processus local de recette sur le port 8273 a été arrêté, puis Playwright a terminé avec le code 0. Le serveur utilisateur existant sur 8173 a été conservé. La recette Commerçant a utilisé un serveur isolé lancé séparément, arrêté après les 5 succès, pour éviter le même blocage Windows. Le build Animation signale un bundle supérieur à 500 kB, sans échec de build.

La revue indépendante a relevé puis confirmé la correction des identités historiques de manifest Support/OnBoard et de la double confirmation de formulaire Support. Les chemins canoniques restent dans leur scope ; les anciennes URL et les droits sont conservés. Les compteurs d'actions en cours et les protections de saisie Atelier empêchent une mise à jour au milieu d'une commande.

Les simulations navigateur ne prouvent pas l'installation OS sur appareil physique ; cette recette reste distincte et nécessaire avant de déclarer PWA-CA7 entièrement vérifié. Aucun déploiement n'est réalisé par cette évolution locale.

Références navigateur : [événement beforeinstallprompt](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeinstallprompt_event), [installation des PWA](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable), [applications d'écran d'accueil iOS](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/), [cycle du service worker](https://web.dev/articles/service-worker-lifecycle).
