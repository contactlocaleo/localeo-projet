# Remédiation préproduction — Commerçants et backend

## Périmètre et règle de clôture

Source : [compte rendu initial](audit-preproduction-2026-09-06.md).
Chaque retour doit avoir correction ou preuve de conformité, documentation,
tests exécutés et commit portant son ID/libellé. Un contrôle d'infrastructure
sans accès à l'environnement reste ouvert, même si les tests locaux passent.
Les modifications Marketplace préexistantes dans le backend sont exclues des commits.

## Répartition des responsabilités

| ID | Libellé | Application Commerçants | Backend / infrastructure | État |
| --- | --- | --- | --- | --- |
| PRO-001 | Isolation du cache entre comptes | Époque de session, rejet des réponses, purge logout | Aucun correctif serveur déduit | Corrigé et testé localement |
| PRO-002 | Distinguer conflit et validation enregistrée | Résultat explicite, refus 409 | Vérifier codes et réponse de rejeu | Corrigé et testé localement |
| PRO-003 | Réconcilier les commandes et erreurs réseau | Résultats distincts, timeout, erreurs, reprise | Vérifier consommation/annulation atomiques | Corrigé et testé localement |
| PRO-004 | Déconnexion locale immédiate | Nettoyage avant révocation, délai maximal | Vérifier révocation/propriété session | Corrigé et testé localement |
| PRO-005 | Retirer les QR des URLs techniques | POST JSON, reset URL, allowlist production | Endpoint corps et logs expurgés | Corrigé et testé localement |
| PRO-006 | Pagination complète Animation | Parcourir/présenter les pages | Vérifier contrat de pagination | Corrigé et testé localement |
| PRO-007 | Respecter les interdictions et échéances serveur | Pas de réactivation ; dates civiles/instants | Vérifier autorité temporelle | Corrigé et testé localement |
| PRO-008 | Clé stable pour décision incertaine | Verrou et clé par commande | Vérifier idempotence et contraintes SQL | Corrigé et testé localement |
| PRO-009 | Aligner Finance sur le backend actuel | Contrats et activation compatibles | Vérifier statut produit Epic 50 | Corrigé et testé localement |
| PRO-010 | Assainir les dépendances d'outillage | Lockfile/outils/CI | Pas de CVE runtime déduite | Corrigé et testé localement ; scan CVE distant limité |
| PRO-011 | Contraste du pied de page | CSS et test axe | Aucun | Corrigé et testé localement |
| PRO-012 | Actualiser le référentiel et la formation | Specs/API/epics/guide | Contrats et preuves serveur | Corrigé et testé localement |
| BACK-001 | Autorisations et invariants serveur | Tests de contrat | BOLA, atomicité, expiration, révocation, fichiers/CORS/logs | Corrigé et testé localement ; exploitation à vérifier |

## Journal de validation

À compléter au fil des correctifs avec les commandes, résultats et limites.
État initial : NO-GO. Aucun déploiement ni mutation métier distante autorisé par ce registre.

### PRO-001 — validation
19 tests réussis (queries.test.js et AnimationPages.test.jsx). Les réponses obsolètes et les mutations après logout sont couvertes. Cache vidé dès changement explicite de session.


### PRO-002 — validation
Corrigé : statut VALIDEE obligatoire, ANOMALIE/refus non présentés comme succès. Backend actuel confirmé : ServiceValidationsAnimation peut renvoyer ANOMALIE ; le frontend ne le confirme plus. 21 tests unitaires ciblés et E2E validation-security réussis.


### PRO-003 — correction et validation
Délai de 15 secondes sur requête et corps, sans retry automatique des mutations. Succès de commande conservé si la lecture échoue ; actions coffret suspendues jusqu’à réconciliation ; reprise sans QR et relecture après refresh. Une transaction consommée exige un nouveau scan pour une autre prestation. Erreurs 401 distinctes de 403 ; erreurs Finance visibles. Invitation affichée avant enrichissement facultatif. 30 tests ciblés et 5 scénarios E2E réussis ; build réussi. Les runners E2E Windows restent parfois actifs après leurs résultats et sont arrêtés après vérification. Backend : 9 tests ciblés réussis, autres invariants suivis sous BACK-001.


### PRO-004 — Déconnexion locale immédiate
La session mémoire, le stockage, le cache Animation et le contexte de validation sont supprimés avant la révocation réseau. La révocation utilise le délai HTTP borné de 15 secondes. Une erreur distante est signalée sans restaurer la session ni perturber une nouvelle connexion. L'expiration locale est contrôlée par temporisation et au retour du focus. Validation : 3 tests ciblés réussis (`src/lib/logout.test.js`, `src/app/useMerchantSession.test.jsx`). La révocation serveur reste vérifiée sous BACK-001.

### PRO-006 — Pagination complète Animation
Les listes animations, invitations et notifications parcourent les pages annoncées par `pagination.total`. Une page manquante, répétée ou invalide produit une erreur visible ; aucune liste partielle n'est mise en cache comme complète. Limite de protection : 500 pages, avec erreur explicite. Le signal d'annulation et l'époque de session restent appliqués. Contrat serveur vérifié dans `animation_locale_api.py` : `items` et `pagination` (page, page_size, total). Validation : 24 tests réussis (pagination, cache, pages Animation).

### PRO-007 — Respecter les interdictions et échéances serveur
Les interdictions explicites et `echeance_depassee=true` ne sont jamais annulées localement. Une liste d'actions vide interdit toute action. Une date civile YYYY-MM-DD s'affiche jusqu'en fin de journée locale ; un timestamp, même à minuit, garde son instant exact. Le backend décide lors de la commande. Validation : 32 tests réussis (contrats et pages Animation), dont échéance serveur, interdiction avant échéance et timestamp à minuit.

### PRO-005 — Retirer les QR des URLs techniques
Coffrets : POST JSON sur le contrat backend existant. Animation : nouvel endpoint authentifié `/protected/animation-locale/commercants/me/participants/resoudre`, corps `qr_token`, projection minimale limitée au commerce. Aucun fallback vers l'URL publique. Jetons de mot de passe retirés par remplacement d'historique, conservés uniquement en mémoire. Origine Marketplace de recette retirée de la production et remplacée par l'origine de production documentée. Déployer le backend avant le frontend. Tests : 6 backend ciblés réussis, build réussi, 3 E2E réussis après un premier timeout de démarrage Vite. Le runner peut utiliser `LOCALEO_E2E_EXTERNAL_SERVER=1` pour un serveur contrôlé séparément sur Windows. Le lien public bénéficiaire demeure côté backend ; la rétention des anciennes URLs dans les proxys reste un contrôle d'exploitation.

### PRO-008 — Clé stable pour décision incertaine
Verrou synchrone dès confirmation et clé conservée en mémoire pour une même décision et un même motif après erreur réseau. Les réponses d'enrichissement antérieures ne peuvent plus remplacer la décision. Un conflit recharge la demande autoritaire et exige un nouveau choix ; aucune commande n'est rejouée automatiquement. Les changements de demande/session invalident les réponses en cours. Validation : 18 tests réussis, dont double clic, réponse perdue avec clé identique, enrichissement tardif et conflit suivi de relecture.

### PRO-009 — Aligner Finance sur le backend actuel
Le GET de détail groupé existe désormais et filtre l'identifiant avec le commerçant : la spécification obsolète a été corrigée, aucun fallback global n'est ajouté. Les erreurs Finance ne sont plus présentées comme des listes vides (PRO-003). Les lectures abandonnées sont annulées/ignorées et une réponse d'ancien compte ne peut remplacer le compte courant ; verrou synchrone des commandes. Les quatre flags Epic 50 sont explicitement désactivés en production avant recette/arbitrages. Validation : 6 tests Finance réussis ; test backend `test_grouped_invoice_detail.py` réussi lors de la passe sécurité (217 tests). Le statut produit de l'Epic 50 reste inchangé.

### PRO-011 — Contraste du pied de page et noms accessibles
Couleur du pied de page assombrie (#5d6872 sur #f6f5f1). La vérification Lighthouse a aussi révélé le nom absent du bouton Installer en affichage mobile et le décalage entre libellé visible et nom accessible du lien d'accueil : ces deux écarts sont corrigés dans ce même retour accessibilité. Validation : 4 tests de composants réussis et 2 scénarios axe sans violation (liste Animation et connexion mobile avec installation).


### BACK-001 — Autorisations et invariants serveur

Défaut confirmé puis corrigé : la route de révocation acceptait un ID sans authentification. Elle exige maintenant un Bearer de scope commercant:session ; la politique de domaine vérifie le propriétaire avant toute mutation. Commits backend : 59a73f0 (correction), c73e637 (test de consommation concurrente). 26 tests identité/révocation ciblés réussis.

Preuves complémentaires : 217 tests de sécurité réussis lors de la passe initiale (7 contrôles PostgreSQL/Marketplace ignorés, 5 erreurs de configuration PostgreSQL ensuite levées par le runner approprié) ; 12 tests PostgreSQL Animation réussis ; 74 tests identité/exploitation/domaine réussis ; 27 tests PostgreSQL d'intégrité réussis avec le runner Windows adapté. Les cinq échecs initiaux de cette dernière passe venaient du blocage du socket interne asyncio, pas d'un défaut métier. Un test supplémentaire de deux transactions sur une même prestation réussit avec une seule validation et un seul mouvement financier. Les migrations v219/v223, la revalidation, le remboursement, l'expiration et les verrous concurrents sont exercés dans des schémas PostgreSQL jetables.

Le nouveau scan authentifié est dans le commit backend 38aa004. Les tests existants couvrent aussi uploads authentifiés, quotas, réencodage raster, accès aux factures, limites de corps, CORS/CSRF et expurgation des logs. Les contrôles réels du proxy, des migrations déployées et de restauration restent une recette d'exploitation.

### Vérification globale intermédiaire

119 tests frontend / 27 fichiers réussis ; 10 scénarios E2E réussis dont 2 axe. Les versions d'outillage ont été résolues sans appel à npm audit ; la tentative d'audit distant a été refusée par le contrôle automatique d'autorisations. Aucune absence exhaustive de CVE nouvelle n'est déduite de cette limitation. Les cinq familles identifiées dans le lockfile initial (LHCI, tmp, extract-zip, qs, uuid) sont retirées du nouveau graphe.


## Rapprochement avec le rapport MVP du 29 août

| Ancien ID | Traitement et preuve actuelle |
| --- | --- |
| SEC-01 | Upload Commerçants déplacé sur le endpoint protégé, scope profil, quota par identité vérifiée et réencodage raster. Tests backend test_merchant_images.py réussis. L'ancien constat « backend absent » est dépassé. |
| SEC-02 | React Router 7.18.2 dans le lockfile ; tests de navigation réussis. La limite de vérification CVE courante est explicitée sous PRO-010. |
| SEC-03 | Risque structurel du Bearer accessible à JavaScript conservé dans le référentiel : sessionStorage n'est pas HttpOnly. Aucune XSS exploitable n'a été démontrée. CSP sans scripts tiers/inline, contrôles serveur, expiration, purge locale et révocation propriétaire renforcent la défense. Une migration cookie/BFF n'est pas implémentée ni présentée comme telle ; elle reste une évolution d'architecture, sans bloqueur démontré dans les parcours audités. |
| SEC-04 | Redirections Stripe limitées à connect.stripe.com ; tests d'allowlist conservés dans la suite réussie. |
| SEC-05 | En-têtes versionnés dans render.yaml ; application réelle sur le service Render à confirmer lors de la recette. |
| UX-01 | Relations ARIA de chargement conservées ; tests de composants et axe réussis. |
| UX-02 | Contrôles frontend de fichiers et contrôles backend de type, signature, taille, quota et contenu vérifiés. |
| UX-03 | MIME du manifeste versionné dans Render ; vérifier la réponse déployée. |
| PERF-01 | Icône adaptée au shell et polices locales ; logo initial remplacé par l’asset 64 px existant et préchargé dans PRO-010. |
| PERF-02 | Enrichissements bornés et facultatifs ; PRO-003 et PRO-008 évitent leur blocage et leurs écrasements tardifs. |
| PERF-03 | Lighthouse actualisé, trois passes et seuils explicites conservés ; rapports locaux et artefacts CI du dépôt. |


### PRO-012 — Actualiser le référentiel et la formation
Architecture, spécification courante, contrats API, mapping validation, démarrage, index documentaire, formation commerçant et procédure de livraison actualisés. Les epics terminés restent historiques ; Epic 41 référence les corrections et Epic 50 conserve ses conditions produit. Les deux copies OpenAPI sont générées depuis le backend sans dotenv ni réseau : 447 chemins, copies identiques, nouveau scan POST et sécurité Bearer de révocation présents. Script durable : `scripts/export-openapi.py`. Le build refuse API/QR de recette en production et exige quatre flags Finance explicites ; 8 tests dédiés réussis dans la suite de 119 tests. Liens du nouveau référentiel vérifiés. La procédure impose backend avant frontend et preuves de recette distante avant GO.


### PRO-010 — Assainir les dépendances d’outillage
LHCI et ses dépendances transitives identifiées dans le constat initial sont remplacés par Lighthouse 13.4.1 et chrome-launcher 1.2.1, avec Chromium Playwright. Le lockfile ne contient plus @lhci/cli, tmp, extract-zip, qs ni uuid. Installation propre `npm ci --no-audit --fund=false` réussie. Node >= 22.19 et trois passes Lighthouse locales/CI sont documentés ; les seuils numériques explicites sont conservés, sans stockage public temporaire des rapports. Le runner traite les ports de débogage et la fermeture Windows. Sources : [version Lighthouse](https://github.com/GoogleChrome/lighthouse/releases/tag/v13.4.1), [avis extract-zip](https://github.com/advisories/ghsa-7pqw-9j4j-h8q3).

La mesure actualisée a révélé un dépassement LCP, traité par extraction des écrans métier en chargement différé, réduction et préchargement du logo existant, préchargement des polices initiales et affichage immédiat du formulaire. Les comportements métier sont conservés : après extraction, 119 tests unitaires et 10 E2E (dont 2 axe) réussissent, avec codes de sortie 0. Résultat Lighthouse final consigné dans le bilan de validation. Le contrôle distant des CVE reste limité par le refus automatique de transmission des métadonnées npm ; le retrait des familles vulnérables connues ne constitue pas un nouvel audit exhaustif.


PRO-010, mesure finale après suppression du chargement initial Caveat dû à une priorité CSS incorrecte : trois passes réussies, code de sortie 0. Médianes Lighthouse 13.4.1 : accessibilité 1, bonnes pratiques 1, performance 0,93, FCP 1 679 ms, LCP 2 338 ms, CLS 0, TBT 196 ms. Tous les seuils explicites passent, avertissements compris. Mesure mobile simulée sur preview local, pas sur production.


### PRO-005 — Complément Referer
La balise meta no-referrer précède les ressources dans index.html ; Render porte la même politique. Le token de réinitialisation ne peut ainsi pas être propagé dans le Referer des assets de même origine avant sa suppression par React. Le lien reçu reste nécessairement dans la requête HTML initiale : le proxy doit expurger les paramètres sensibles de ses journaux. Le scénario navigateur vérifie désormais aussi les Referer des ressources.

Le premier test Referer a révélé l’injection du client Vite avant la meta en développement. La même politique HTTP est maintenant appliquée par Vite (dev/preview) et Render. Nouvelle passe : 3 tests de validation/sécurité réussis ; les 2 tests axe ont aussi réussi après la dernière correction CSS.


## Bilan et références de livraison
Voir le [bilan final](validation-finale-preproduction-2026-09-07.md) pour les commits par ID, les résultats consolidés et les conditions restant à vérifier sur l’environnement distant. Les points applicatifs corrigés ne ferment pas automatiquement les contrôles d’exploitation ni le risque structurel SEC-03.
