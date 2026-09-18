# Audit préproduction Localeo Animation — 6 septembre 2026

## Verdict initial : NO-GO PRODUCTION

Ce compte rendu conserve les constats **avant correction**. Le suivi des corrections,
tests et commits est tenu dans [le plan de remédiation](remediation-2026-09-06.md).
Il ne constitue pas une attestation de déploiement ou une certification de sécurité.

## Périmètre et preuves

- Frontend React/TypeScript/Vite : `localeo-animation`, révision initiale `04b44a0`.
- Backend FastAPI/SQLAlchemy/PostgreSQL : `localeo-backend`, révision initiale `81fef96`.
- Référentiel : architecture EPIC 41, conventions API/sécurité, contrats EPIC 46,
  spécification Finance EPIC 50 et ADR domaine du 28 août 2026.
- Aucun fichier modifié durant l'audit initial, aucun paiement/email métier exécuté.
- TypeScript, ESLint et 25 tests frontend réussis. Build production exécuté en mémoire
  (1 631 modules), minification active, source maps désactivées, manifestes/lock cohérents.
- Tests backend et recette PostgreSQL/Stripe non exécutés pendant l'audit initial.
- La consultation actualisée du registre npm a été refusée par le contrôle automatique,
  car elle transmet les noms/versions des dépendances. Aucun résultat CVE récent revendiqué.

Notation : `F:` désigne le dépôt Animation, `B:` le dépôt backend. Les numéros de ligne
ci-dessous correspondent à l'état audité et peuvent se déplacer après correction.

## Cartographie

Routes frontend : `/tableau-de-bord`, `/animations`, `/animations/nouvelle`,
`/animations/:id`, `/modeles`, `/coffrets`, `/participants`, `/validations`, `/tirages`,
`/flyers`, `/bilans`, `/finance/{credit,demandes,factures-localeo}`, `/abonnement`, `/support`.
Le détail Animation héberge configuration, participations commerçants, paiement,
actualités, workflow, live, participants, validations, tirages, gains, flyer et bilan.

Parcours : modèle → configuration → invitations/acceptations commerçants → commande
des lots → paiement/réservation → publication → inscriptions/validations → clôture/gel
→ tirage → envoi des gains. Les opérateurs internes et commerçants ont des sessions distinctes.

Le client central `F:src/app/api.ts` déclare 77 appels HTTP : identité, contexte,
communes/éligibilité, animations et commandes, actualités, participations, projections,
exports/documents et finance. Activation et télémétrie sont séparées. L'authentification
est un Bearer opaque en mémoire ; les permissions sont relues côté serveur par commune.
Le client n'effectue pas de retry implicite ; timeout ordinaire 20 s, flyer 120 s.

## ANIM-001 — Cloisonnement communal de la facturation

- **Sévérité : CRITIQUE si les modules Finance sont activés.** Bloquant : OUI sous cette condition.
- **Responsabilité : backend.** EPIC 50.
- **Localisation :** `B:app/api/demandes_facture_commercant_api.py:159-203`,
  `B:app/api/factures_localeo_api.py:149-173` et services de facturation associés.
- **Preuve :** comparaison du partenaire sans commune ; listes et téléchargements
  filtrés par demandeur/destinataire partenaire seulement.
- **Scénario :** un gestionnaire habilité seulement sur A accède aux demandes/documents
  de B du même partenaire, ou crée une demande pour une commande de B.
- **Impact :** exposition intercommunale de documents et opérations hors habilitation.
- **Correction :** filtrage serveur par commune avant liste, création et téléchargement ;
  tests avec deux communes du même partenaire et droits différents.

## ANIM-002 — Clés de reprise et d'annulation trop longues

- **Sévérité : HAUTE.** Bloquant : OUI.
- **Responsabilité : frontend, test de contrat backend.** EPIC 46.
- **Localisation :** `F:src/app/components/LotPaymentPanel.tsx:48-58,156-177` ;
  `B:app/api/animation_locale_api.py:1823-1851`.
- **Preuve exécutée en mémoire :** reprise 137 caractères, annulation 140, maximum API 128.
- **Scénario :** reprise/annulation normale avec UUID métier rejetée en 422 avant le service.
- **Impact :** récupération de paiement et annulation inutilisables.
- **Correction :** clé opaque courte et stable, contexte métier conservé séparément.

## ANIM-003 — Concurrence validations et clôture

- **Sévérité : HAUTE.** Bloquant : OUI.
- **Responsabilité : backend.** EPIC 41, ADR domaine.
- **Localisation :** `B:app/application/animation_locale/services/validations_animation.py:22-61,103-118`,
  `tirages_animation.py:150-187`, suppression dans `participants_animation.py`.
- **Preuve :** scan contrôlé avant sa transaction, sans verrou commun avec clôture/gel.
- **Scénario :** scan lit « ouverte », clôture fige les éligibles, scan écrit ensuite.
  Deux commerçants peuvent aussi recalculer simultanément une progression partielle.
- **Impact :** validation après clôture, participant qualifié absent du gel, statut périmé.
- **Correction :** ordre de verrouillage commun animation puis participant ; relire
  statut, période et configuration dans la transaction. Inclure annulation/suppression.

## ANIM-004 — Seuil de qualification incohérent

- **Sévérité : HAUTE.** Bloquant : OUI.
- **Responsabilité : frontend ET backend.** EPIC 41/53.
- **Localisation :** `F:src/app/App.tsx:3816-3846,5541,5871` ;
  `B:app/domaine/animation_locale/services/strategie_passeport_commercant.py:88-96`,
  `B:app/application/animation_locale/services/validations_animation.py:114-118`.
- **Preuve :** frontend envoie `seuil_validations`, serveur utilise `nombre_validations_requises`.
- **Scénario :** dix commerces, quatre validations annoncées ; serveur exige une autre valeur.
- **Impact :** qualification contraire à la promesse, tirage contestable ou bloqué.
- **Correction :** contrat canonique, validation des règles, calcul domaine commun,
  affichage des règles effectives ; compatibilité explicite des données historiques.

## ANIM-005 — Fuseaux et bornes temporelles incohérents

- **Sévérité : HAUTE.** Bloquant : OUI.
- **Responsabilité : frontend ET backend.** EPIC 41.
- **Localisation :** `F:src/app/App.tsx:3839-3843,5525-5533` ;
  `B:app/application/animation_locale/services/validations_animation.py:30-33`,
  `participants_animation.py:42-44`, `B:app/domaine/animation_locale/entities/animation.py:45-73`.
- **Preuve :** dates sans offset, UTC implicite, offset supprimé sans conversion,
  comparaisons différentes de la borne de fin.
- **Scénario :** journée française terminant une/deux heures trop tard ; dates explicites
  `+02:00` interprétées différemment par le domaine et le scan.
- **Impact :** opérations hors période et divergence avec le règlement.
- **Correction :** dates explicites, fuseau métier Europe/Paris, période `[début, fin[`,
  conversion commune ; tests de changement d'heure et traitement des anciennes valeurs.

## ANIM-006 — Paiement intégral par crédit bloqué

- **Sévérité : HAUTE si crédit B2B activé.** Bloquant : OUI sous cette condition.
- **Responsabilité : backend.** EPIC 46/50.
- **Localisation :** `B:app/application/animation_locale/services/commandes_lots.py:243-308` ;
  `B:app/domaine/gestion_achats/entities/commande_achat.py:68-70`.
- **Preuve :** crédit réservé et commité, session synthétique `url=None`, transition
  `demarrer_paiement` exigeant une URL avant matérialisation.
- **Scénario :** crédit suffisant pour toute la commande ; erreur et réservation sans lots.
- **Correction :** transition domaine sans Stripe pour financement intégral ; reprise
  idempotente et réservation cohérente en cas d'échec.

## ANIM-007 — Formules dans l'export CSV

- **Sévérité : MOYENNE.** Bloquant : NON isolément.
- **Responsabilité : backend.** EPIC 41 exports.
- **Localisation :** `B:app/application/animation_locale/services/bilans_exports_animation.py:203-214`.
- **Preuve/scénario :** un nom `=1+1` est exporté via `csv.DictWriter` sans neutralisation,
  puis interprété par certains tableurs. Aucune exécution distante automatique affirmée.
- **Impact :** interprétation de données utilisateur comme formules.
- **Correction :** neutraliser les préfixes dangereux à l'export, préserver le texte métier.

## ANIM-008 — Idempotence de création non atomique

- **Sévérité : MOYENNE.** Bloquant : NON isolément.
- **Responsabilité : frontend ET backend.** EPIC 41.
- **Localisation :** `F:src/app/api.ts:847-850`,
  `B:app/api/animation_locale_api.py:1329-1352`, `gestion_animations.py:44-54`.
- **Preuve :** clé frontend renouvelée à chaque essai ; création commitée avant mémoire d'idempotence.
- **Scénario :** réponse perdue puis nouvelle tentative, ou appels parallèles de même clé.
- **Impact :** plusieurs brouillons persistés ; aucune preuve de double paiement.
- **Correction :** clé stable par intention et transaction atomique clé/création/résultat.

## ANIM-009 — Cache et changement de commune

- **Sévérité : MOYENNE.** Bloquant : NON isolément.
- **Responsabilité : frontend.** EPIC 41/50.
- **Localisation :** `F:src/app/httpClient.ts:117`, `F:src/app/api.ts:752`.
- **Preuve exécutée :** GET en A, changement B, nouveau GET partageant la promesse de A.
- **Impact :** ancien contexte restitué après changement, sans preuve d'IDOR serveur.
- **Correction :** génération de contexte et invalidation des lectures, sélecteur de commune
  explicite (helper présent mais non raccordé dans l'interface auditée).

## ANIM-010 — Live figé et listes incomplètes

- **Sévérité : MOYENNE.** Bloquant : NON isolément.
- **Responsabilité : frontend.** EPIC 41.
- **Localisation :** `F:src/app/App.tsx:769-782,2399-2402`, `F:src/app/api.ts:953-957,1037-1041`.
- **Preuve :** chargement live unique, plusieurs listes limitées à la page par défaut.
- **Scénario :** scans pendant que la vue reste ouverte ; plus de 25 éléments dans une liste.
- **Impact :** pilotage sur données périmées/incomplètes.
- **Correction :** polling 15 s borné à la visibilité, fraîcheur explicite et pagination complète.

## ANIM-011 — Build production compatible avec une origine de staging

- **Sévérité : MOYENNE.** Bloquant : NON pour le code seul, configuration obligatoire avant livraison.
- **Responsabilité : frontend/chaîne de livraison.** Déploiement.
- **Localisation :** `F:src/env.ts:1`, `F:vite.config.ts`, `F:Dockerfile:14`.
- **Preuve :** build production local résolvant une origine au nom de staging ; contrôle Docker
  de non-vacuité seulement. La valeur locale n'est pas une preuve de configuration déployée.
- **Impact :** authentification/données envoyées au mauvais environnement.
- **Correction :** environnement cible explicite, origine validée, contrôle du bundle livré.

## Retours complémentaires à traiter

- ANIM-012 : logout réseau ignoré, expiration écran non autonome, retour de paiement
  perdu après reconnexion ; clarifier état de session et reprendre le parcours autorisé.
- ANIM-013 : journalisation complète des erreurs, coordonnées de facturation dans les
  empreintes de sessionStorage ; minimiser les données et rendre les erreurs documentaires explicites.
- ANIM-014 : documentation d'authentification obsolète, recette et suivi asynchrones ;
  mettre à jour exploitation/formation et matérialiser les gates de mise en production.

Ces identifiants complémentaires rendent traçables les observations non numérotées
du compte rendu initial. Ils ne signifient pas de nouvelles vulnérabilités critiques.

## Matrice initiale

| Contrôle | État initial |
| --- | --- |
| Session opaque, mémoire frontend, révocation serveur | Conforme dans le code lu |
| Autorisations cœur Animation | Conforme dans le code lu |
| Isolation communale Finance | Non conforme si activée |
| Idempotence des commandes | Partiel |
| Qualification/clôture/dates | Non conforme |
| Prix serveur, paiement confirmé backend | Conforme dans le code lu |
| Tirage unique, distribution répétée | Protections présentes, recette concurrence manquante |
| Live et pagination | Non conforme |
| Build/lockfile | Compilation conforme, environnement non verrouillé |
| XSS sérieuse / secret serveur bundle | Aucun chemin/secret démontré |
| CORS, purges, batchs, webhooks réels, déploiement | Non vérifiable |

## Conclusion initiale

Un utilisateur ou des requêtes concurrentes peuvent-ils provoquer une opération
interdite, une incohérence ou un accès hors habilitation ? **OUI**, avec les conditions
d'activation exposées ci-dessus. Faut-il repousser la production ? **OUI**.
Le verdict après correction doit s'appuyer sur les tests réellement exécutés et
préserver les limites de recette, sans transformer une compilation réussie en GO global.
