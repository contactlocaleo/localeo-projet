# EPIC 60 — Rapport de développement V1

Date : 6 septembre 2026. Branche : `feat/epic-60-backoffice-erp`.

La V1 réunit les 22 stories PRD-561 à PRD-582 des anciennes epics 60 et 61.
Les spécifications détaillées, les commandes métier, les interfaces ERP, la migration,
les tests et la procédure de livraison sont livrés ensemble dans un seul nouveau commit.
Le déploiement en production ne fait pas partie de cette exécution.

## Couverture livrée

| Story | Réalisation V1 |
| --- | --- |
| PRD-561 | Synthèse de vendabilité filtrée et datée, mêmes règles que le catalogue public |
| PRD-562 | File paginée, recherche et filtres, priorité aux pertes, sévérité et ancienneté |
| PRD-563 | Diagnostic canonique exhaustif, verdict indéterminé, contrôles réussis et bloquants |
| PRD-564 | Liens de traitement vers ateliers, fiscalité et outils spécialisés |
| PRD-565 | Épisodes d'alertes métier/technique, déduplication, résolution et notifications optionnelles |
| PRD-566 | Réévaluation manuelle, demandes persistées, invalidations et réconciliation planifiée |
| PRD-567 | Historique paginé par curseur, empreintes des causes et audit des commandes |
| PRD-568 | Couverture territoriale et regroupement des causes communes |
| PRD-569 | Rôles, périmètres SQL, CSRF, idempotence, validation des contrats et absence de détails Stripe publics |
| PRD-570 | Réutilisation des gardes canoniques et tests HTTP de parité Marketplace |
| PRD-571 | Accueil de travail : dossiers à reprendre, responsables, échéances, alertes et actions rapides |
| PRD-572 | Navigation par missions et bascule directe des anciens ateliers |
| PRD-573 | Création et modification des commerçants en brouillon, statut contrôlé |
| PRD-574 | Modèles de prestations du commerçant, édition et accès aux prestations rattachées |
| PRD-575 | Aptitude par capacités/checklist Onboard et actions explicites |
| PRD-576 | Même dossier Onboard, prochaine action, responsable, échéance, notes et activité |
| PRD-577 | Atelier coffret : informations, composition, économie, fiscalité, commercialisation et historique |
| PRD-578 | Copies de modèles versionnées, provenance et protection des engagements existants |
| PRD-579 | Rentabilité canonique, plafond de reversements et confirmation des dégradations de marge |
| PRD-580 | Simulation de la cible ACTIVE, publication atomique, retrait et archivage contrôlés |
| PRD-581 | Raccourcis de création, reprise, traitement et accès aux fonctions opérationnelles existantes |
| PRD-582 | Audit, concurrence optimiste, cloisonnement et instrumentation début/sauvegarde/abandon des parcours |

## Validation exécutée

- Suite complète isolée : **2 277 tests réussis, 1 ignoré, 12 avertissements**, en 133,80 s.
  Le test ignoré est la campagne volumétrique optionnelle, exécutée séparément avec succès.
- Huit scénarios d'intégration EPIC 60 sur PostgreSQL réel : application de v218,
  composition/publication/perte/rétablissement, modèles sans propagation, réutilisation Onboard,
  worker et notifications, sécurité HTTP/idempotence, concurrence et parité publique,
  incident de lecture sans fuite d'erreur interne.
- Vérification syntaxique JavaScript réussie et contrôle des différences Git sans erreur d'espacement.
- Recette dans Chrome sur données synthétiques locales : accueil, création commerçant,
  sauvegarde de la prochaine action, accès au même dossier Onboard, fiche coffret,
  onglets de commercialisation et simulation ACTIVE avec résultat vendable.
- Les avertissements concernent des dépréciations de dépendances, une méthode de date existante
  et le cycle de clés étrangères des profils dans la préparation du schéma de test.

Commande de régression reproductible (base PostgreSQL locale jetable requise) :

```powershell
.\tmp\audit-venv\Scripts\python.exe scripts/validation/test_isolated.py -q --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55437/localeo_audit_test --basetemp=tmp/epic60-recette
```

## Performance mesurée

Campagne séparée réussie : 10 000 coffrets, 100 000 prestations et 1 000 000 événements ;
20 échantillons après échauffement, PostgreSQL local, sans fournisseur externe.

| Lecture | p95 | Requêtes SQL maximales |
| --- | ---: | ---: |
| Liste, service | 138,84 ms | 2 |
| Détail, service | 4,12 ms | 2 |
| Chronologie, service | 3,82 ms | 2 |
| Synthèse, service | 991,96 ms | 11 |
| Liste, HTTP TestClient | 108,22 ms | — |
| Détail, HTTP TestClient | 19,83 ms | — |

Il s'agit d'un benchmark de lecture sur données synthétiques, pas d'une garantie de temps
de réponse en production ni d'un test du pire cas de réconciliation. L'instrumentation UX
est livrée ; les gains humains avant/après devront être observés avec des opérateurs.
Aucun gain de temps utilisateur n'est présenté comme déjà mesuré.

## Hypothèses prises sous délégation

Les décisions utilisateur sont conservées dans le [registre](registre-arbitrages.md).
Les choix complémentaires ne sont pas présentés comme de nouvelles validations utilisateur :

- H01 : file diagnostic en lecture, mutations dans les ateliers.
- H02 : épisodes séparés de perte et d'incident ; pas de fausse perte au premier chargement.
- H03 : ADMIN et EXPLOITATION habilités aux ateliers ; EXPLOITATION limité à ses communes.
  La qualification fiscale reste réservée à ADMIN.
- H04 : gardes catalogue, prestations, commerçants et territoires canoniques ; flags BUM/Stripe conservés.
- H05 : fraîcheur de 20 minutes, traitement chaque minute, historique et alertes fermées 365 jours,
  idempotence 24 heures ; aucune purge des alertes ouvertes.
- H06 : modèles autonomes, rattachements par copie versionnée, aucun remplissage automatique des modèles historiques.
- H07 : engagements achetés protégés ; exceptions via les fonctions existantes de fermeture/remboursement.
- H08 : bascule directe, anciens formulaires remplacés, fonctions spécialisées conservées avec leurs droits.

Le dossier et les fonctionnalités avancées de référencement réutilisent Onboard et ses flags existants.
Les notifications externes sont désactivées par défaut ; leur destinataire et son périmètre doivent être
configurés explicitement. Aucun email ni WebPush réel n'a été envoyé pendant les tests.

## Mise en service

Appliquer **v218** avec le runner de migrations avant le nouveau code, puis contrôler le traitement
initial et la tâche de réconciliation. La procédure, les flags et le retour arrière sont détaillés
dans [Livraison V1](livraison-v1.md). Les données de production n'ont pas été modifiées.

Références : [spécifications fonctionnelles](specifications-fonctionnelles.md),
[contrats API effectifs](contrats-api.md), [registre des arbitrages](registre-arbitrages.md).

## Correctif d'accès après livraison

Un refus `Profil non autorise` pouvait aussi désigner une ancienne session sans rôle.
Ce cas conduit désormais à une reconnexion pour les pages et à 401 pour les API,
sans attribuer de rôle par défaut. La casse et les espaces des rôles sont normalisés ;
un profil non habilité reste refusé en 403. Validation : 14 tests ciblés de session
et d'authentification réussis, puis les 8 tests d'intégration PostgreSQL EPIC 60 réussis.
Le rôle de la session déployée à l'origine du signalement n'a pas été inspecté.
