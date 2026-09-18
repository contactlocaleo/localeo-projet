# Analyse et suivi des corrections — 7 septembre 2026

Source : [compte rendu initial du 6 septembre](audit-preproduction-2026-09-06.md).
Périmètre : les 14 retours ANIM-001 à ANIM-014 de cet audit, dans les dépôts Animation et backend. Les suivis historiques conservent leur propre périmètre.

## Résultat

**Les 14 retours sont corrigés dans le code et documentés. Verdict : GO SOUS CONDITIONS pour préparer la livraison ; activation en production non validée.** Les contrôles locaux ci-dessous sont réussis. Les contrôles de cible et de dépendances restent des conditions bloquantes avant activation. Aucun push ni déploiement réalisé.

## Répartition frontend / backend et commits

Tous les correctifs portent leur ID et leur libellé dans les commits. Plusieurs commits complémentaires peuvent traiter le même retour.

| ID et libellé | Application Animation | Backend | État |
| --- | --- | --- | --- |
| ANIM-001 — Cloisonnement communal de la facturation | Consomme le filtrage serveur | Filtrage commune/partenaire, documents historiques fermés au portail, accès administrateur conservé : ee9c350, 58cd122 | Corrigé et testé |
| ANIM-002 — Clés de reprise et annulation compatibles | UUID stable, taille bornée : 322460f | Contrat existant respecté | Corrigé et testé |
| ANIM-003 — Sérialiser validations et clôture | Aucun correctif requis | Verrou partagé, relecture après attente, modification tardive protégée : 0d02de9, 843abc1 ; dépendance 3f8f2d2 | Corrigé et testé |
| ANIM-004 — Unifier le seuil de qualification | Seuil canonique et validations distinctes : 8252370 | Normalisation et seuil atteignable à la publication : 2bd8bc6 | Corrigé et testé |
| ANIM-005 — Unifier fuseaux et bornes temporelles | Journées Europe/Paris, fin exclusive : 5aaf72d | Comparaisons UTC et compatibilité historique : 6beec04, d1a9673 | Corrigé et testé |
| ANIM-006 — Finaliser les commandes financées par crédit | Contrat existant | Crédit seul sans URL Stripe, reprise et capture unique : d1a64bf | Corrigé et testé |
| ANIM-007 — Neutraliser les formules CSV | Protection des nouveaux exports, livrée avec ANIM-010 : 360beda | Cellules dangereuses, contrôles et opérateurs Unicode : 32da2d3, f3749b3 | Corrigé et testé |
| ANIM-008 — Garantir l'idempotence de création | Intention stable et prévention double clic : ba5c143 | Création et réponse idempotente dans la même transaction : 83494ee | Corrigé et testé |
| ANIM-009 — Invalider les lectures au changement de commune | Sélecteur, invalidation et rejet des anciennes réponses : 1fec07d | Contrats de contexte conservés | Corrigé et testé |
| ANIM-010 — Actualiser le live et parcourir les listes | Polling, toutes les pages et vrais exports CSV : 360beda | Pagination existante utilisée | Corrigé et testé |
| ANIM-011 — Valider la cible du build | Origine HTTPS attendue, cible explicite, garde des variables exposées : 2e14e80 | Configuration effective à vérifier sur cible | Corrigé et testé |
| ANIM-012 — Fiabiliser expiration et déconnexion | Expiration autonome, nettoyage immédiat et état de révocation explicite : d0cbee6 | Endpoint de révocation existant | Corrigé et testé |
| ANIM-013 — Minimiser stockage et journalisation | Empreinte/UUID sans payload financier, logs réduits, erreurs visibles : ac81a04 | Contrats conservés | Corrigé et testé |
| ANIM-014 — Consolider documentation et recette production | Suivi des opérations asynchrones jusqu'au succès réel, tests, formation et présent rapport : commit ANIM-014 portant ce fichier | Guide, epics et CI PostgreSQL isolée : 9c43cd7 | Corrigé et testé localement ; recette de cible requise |

Le commit backend concurrent Marketplace 3f8f2d2 a intégré une partie des verrous inscription/suppression et de la résolution transactionnelle nécessaires à ANIM-003. Cette dépendance doit être conservée lors d'un éventuel cherry-pick. Les autres travaux Marketplace/Pro présents dans le dépôt n'ont pas été annulés. Une livraison doit intégrer l'historique approprié, pas uniquement copier les fichiers de ce tableau.

## Documentation mise à jour

- [Contrats corrigés](../../specifications/securisation-production/contrats-animation.md) : invariants métier, isolation, dates, paiements, exports et opérations asynchrones.
- [Guide de formation et recette Animation](../../produit/formation/animation/guide-animation-preproduction.md).
- [Authentification](../../specifications/identite-acces/session-animation.md), [EPIC 41](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md), [EPIC 53](../../roadmap/terminees/epic-53-tombola-locale-backlog.md), [contrats EPIC 46](../../specifications/epic-46-paiement-lots-animation/contrats-api.md).
- [Déploiement](../../exploitation/animation/deploiement-render.md), variables d'environnement, Docker et CI frontend.
- Backend : guide docs/ops/formation/guide-animation-preproduction.md, spécifications Finance EPIC 50, backlogs EPIC 41/53 et workflow .github/workflows/animation-audit.yml.

Les statuts globaux des epics ne sont pas réinterprétés comme une validation de production.

## Vérifications exécutées

| Vérification | Résultat |
| --- | --- |
| Suite frontend complète | 47 tests réussis, aucun ignoré |
| TypeScript | tsc --noEmit réussi |
| ESLint | src et vite.config.ts : réussi |
| Build frontend final | Vite réussi, 1 639 modules, source maps désactivées |
| Suite backend ciblant Animation et régressions Finance/achats | 293 tests réussis, aucun ignoré |
| PostgreSQL | Instance 18 isolée sur 127.0.0.1:55439, base anim_remediation_test |

Le build de vérification utilise une origine synthétique https://api-staging.example.invalid et sort dans tmp/build-validation. **Ces artefacts ne doivent pas être déployés.** Le dossier tmp est exclu de Git.

Environnement local : Node 24.14.0, Python 3.14.3, FastAPI 0.128.8, SQLAlchemy 2.0.48, pytest 8.4.2. Les exigences backend verrouillées indiquent FastAPI 0.136.0, SQLAlchemy 2.0.52 et pytest 9.1.1 : les tests locaux ne prouvent donc pas une installation propre de ces versions. La CI ajoutée installe les exigences avec vérification des hashes et exécute pip check ; son exécution distante reste à obtenir. Le frontend CI utilise Node 22.

Commande backend exécutée depuis localeo-backend, avec le Python indiqué ci-dessus :

```powershell
python -B scripts/validation/run_animation_audit_tests.py tests/domain/animation_locale tests/application/animation_locale tests/security/test_animation_finance_tenant.py tests/security/test_animation_validation_concurrency.py tests/security/test_animation_creation_atomicity.py tests/application/conformite_fiscale_bum/test_factures_localeo.py tests/application/use_cases/test_valider_paiement_commande_lots.py tests/domain/gestion_achats/entities/test_commande_achat.py -q -p no:cacheprovider
```

Le lanceur impose la base isolée, ignore dotenv, désactive bootstrap/scheduler et bloque les connexions sortantes autres que PostgreSQL local. Les tests exercent notamment l'isolation commune A/B d'un même partenaire, les verrous concurrents, le rollback/idempotence, le crédit seul, les seuils et les changements d'heure. Certaines dépendances métier et le fournisseur de paiement sont des doubles de test : ceci ne remplace pas une recette Stripe ou un parcours navigateur complet sur la cible.

## Conditions restantes avant activation en production

1. **Identifier les URL publiques réelles** de l'API et de l'application, demandées mais non reçues. Vérifier les origines attendues au build, HTTPS, CORS et en-têtes sur cette cible.
2. **Exécuter les CI sur installations propres verrouillées**, dont PostgreSQL et la combinaison de versions effectivement livrée ; obtenir un audit récent des dépendances. La consultation du registre npm a été refusée par le contrôle automatique car elle transmet les noms et versions des dépendances. Aucun bilan CVE récent n'est revendiqué.
3. **Vérifier la configuration de cible** : secrets non exposés, modes Stripe et signatures webhooks, flags métier, jobs/outbox, modes email/SMS et comptes de recette. Ne pas activer un flux réel à partir des variables de test.
4. **Réaliser la recette intégrée en staging** : deux communes d'un même partenaire, changement de contexte pendant une requête, création avec réponse perdue, scan concurrent avec clôture, paiement Stripe/crédit/reprise, exports et session expirée. Consigner les preuves et anomalies éventuelles.
5. **Examiner les données historiques** : factures sans commune accessibles seulement à l'administration, règles de qualification héritées et périodes anciennes. Aucun déplacement automatique des dates ni réécriture de migration appliquée n'a été effectué.
6. **Préparer l'exploitation de la livraison** : sauvegarde/restauration vérifiable, éventuelles migrations de la release complète, retour arrière, supervision et validation par le responsable de mise en production.

Les corrections applicatives demandées sont terminées. La sécurité effective de l'environnement déployé et l'autorisation de mise en production restent à établir par ces preuves ; le présent rapport ne vaut pas certification.
