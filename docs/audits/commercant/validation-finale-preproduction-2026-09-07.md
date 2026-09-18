# Bilan de remédiation préproduction — 7 septembre 2026

## Décision

**Corrections applicatives vérifiées localement ; GO de production conditionnel, non prononcé sur l'environnement distant.** Les constats PRO-001 à PRO-012 ont reçu une correction, une mise à jour documentaire et une vérification. BACK-001 a aussi révélé puis corrigé une révocation de session insuffisamment protégée. Les tests d'intégrité n'ont pas montré de double consommation.

Le [CR initial](audit-preproduction-2026-09-06.md) conserve son verdict et ses preuves initiales. Le [registre frontend/backend](remediation-preproduction-2026-09-06.md) détaille chaque correction, les échecs intermédiaires et leurs résolutions, ainsi que le rapprochement avec les anciens constats SEC/UX/PERF. Ce bilan ne certifie ni une absence exhaustive de vulnérabilités ni une recette de production qui n'a pas été exécutée.

## Commits de correction

| ID / libellé | Application Commerçants | Backend |
| --- | --- | --- |
| PRO-001 — Isolation du cache entre comptes | 58eaac2 | Contrôles existants vérifiés |
| PRO-002 — Distinguer conflit et validation enregistrée | c9b8fbf | Contrats vérifiés |
| PRO-003 — Réconcilier commandes et erreurs réseau | db68ffb | Atomicité vérifiée |
| PRO-004 — Déconnexion locale immédiate | 5f8b99e | Voir BACK-001 |
| PRO-005 — Retirer les QR des URLs techniques | 4e65c59 et 317efda (Referer) | 38aa004 |
| PRO-006 — Pagination complète Animation | 5d408aa | Pagination vérifiée |
| PRO-007 — Respecter interdictions et échéances serveur | 5438dcf | Autorité serveur vérifiée |
| PRO-008 — Clé stable pour décision incertaine | 2039fd2 | Idempotence vérifiée |
| PRO-009 — Aligner Finance sur le backend actuel | 1852ebb | Contrats vérifiés, activation produit conditionnelle |
| PRO-010 — Assainir dépendances et chargement initial | e2477ae | Sans changement |
| PRO-011 — Contraste et noms accessibles | 95d52da | Sans changement |
| PRO-012 — Actualiser référentiel et formation | 0f496eb | OpenAPI exporté depuis les sources |
| BACK-001 — Autorisations et invariants serveur | 91d9e5e : preuves et runner | 59a73f0 : révocation ; c73e637 : concurrence |

Le dépôt backend contient des travaux parallèles Animation/Marketplace : utiliser les références et les procédures de versionnement du backend, sans considérer tout son HEAD comme une livraison implicitement validée par cet audit.

## Vérifications exécutées

| Vérification | Résultat et portée |
| --- | --- |
| Installation propre | npm ci --no-audit --fund=false réussie |
| Suite frontend après extraction des écrans | 119 tests / 27 fichiers réussis, sortie 0 |
| Suite E2E Chromium | 10 scénarios réussis, sortie 0 ; comprend 2 contrôles axe |
| Build production | Réussi ; contrôle API/QR/flags actif |
| Contrats | 447 chemins OpenAPI ; deux copies identiques ; scan POST et Bearer de révocation présents |
| Sécurité backend, première passe | 217 réussis, 7 ignorés, 5 erreurs de configuration PostgreSQL ; ces erreurs ont été reprises avec le runner adapté |
| PostgreSQL Animation | 12 réussis sur la base dédiée |
| Identité/exploitation/domaine | 74 réussis ; 24 tests exigeant PostgreSQL ignorés dans ce runner sans base |
| Intégrité PostgreSQL | 27 réussis ; annulation, revalidation, remboursement et contraintes d'unicité exercés |
| Révocation de session | 26 tests ciblés réussis, dont absence de Bearer et propriétaire étranger |
| Nouveau scan protégé et QR corps JSON | 6 tests ciblés réussis |
| Deux transactions concurrentes sur la même prestation | 1 test PostgreSQL réussi : exactement une validation et un mouvement financier |

Ces ensembles se recoupent : leurs nombres ne doivent pas être additionnés pour annoncer un total de tests uniques. Les tests PostgreSQL utilisent des schémas jetables dans le cluster local explicitement vérifié, sans accès à la base métier. Les avertissements restants concernent notamment les dépréciations Starlette et l'ordre de nettoyage de tables SQLAlchemy ; ils ne sont pas des échecs métier.

### Lighthouse

Trois passes Lighthouse 13.4.1, Chromium Playwright, simulation mobile sur preview local. Médianes : performance **93 %**, accessibilité **100 %**, bonnes pratiques **100 %**, FCP **1 679 ms**, LCP **2 338 ms**, CLS **0**, TBT **196 ms**. Tous les seuils numériques explicites passent, sortie 0. Les anciens dépassements ont conduit à corriger le chargement initial, sans abaisser ces seuils. Rapports locaux sous .lighthouseci et publication en artefacts du dépôt par la CI ; capture finale inspectée.

Dernier complément PRO-005 : 3 scénarios de validation/sécurité réussis après vérification des Referer ; 2 scénarios axe réussis sur la dernière CSS. La politique no-referrer est portée par HTML, Vite et Render.

## Documents livrés

- [Architecture](../../architecture/frontends/commercant/architecture.md), [spécification courante](../../specifications/espace-commercant/README.md), [API](../../specifications/espace-commercant/contrats-api.md) et copies OpenAPI synchronisées.
- [Epic 41](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md) et documents de validation/Finance actualisés dans les commits correspondants.
- [Guide de formation commerçant](../../produit/formation/commercant/guide-commercant.md).
- [Procédure de mise en production](../../exploitation/commercant/mise-en-production.md), avec ordre backend avant frontend, recette et critères d'arrêt.

## Conditions encore ouvertes pour le GO distant

1. Confirmer l'URL et le service de production Commerçants, les références backend/frontend effectivement déployées et la présence du nouveau scan POST. Aucun déploiement ni push n'a été effectué pendant cette remédiation.
2. Exécuter la recette sur comptes synthétiques prévue dans la procédure : droits croisés, expiration, deux appareils, annulation/revalidation et réponses réseau perdues.
3. Vérifier les migrations de la version retenue, les en-têtes Render réellement servis, CORS, l'expurgation des logs et une preuve de restauration. Les tokens des liens entrants exigent notamment une expurgation des paramètres côté proxy.
4. Garder les quatre flags Finance désactivés jusqu'à la recette et aux arbitrages produit Epic 50.
5. Compléter le contrôle CVE courant dans un environnement autorisé. La revue automatique a refusé npm audit car il transmet les métadonnées de dépendances au registre npm. Les familles vulnérables identifiées ont été retirées du lockfile ; aucun nouveau résultat exhaustif « zéro CVE » n'est revendiqué.

L'ancien SEC-03 reste un risque d'architecture documenté : le Bearer de sessionStorage est accessible au JavaScript de même origine. Aucune XSS exploitable n'a été démontrée ; CSP, contrôles serveur, expiration et révocation sont des défenses, pas une migration HttpOnly. Une évolution cookie/BFF n'a pas été implémentée et ne doit pas être présentée comme clôturée.
