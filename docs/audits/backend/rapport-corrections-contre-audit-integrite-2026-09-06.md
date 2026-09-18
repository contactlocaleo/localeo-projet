# Rapport de correction du contre-audit d'integrite

Date : 6 septembre 2026. Reference initiale : `39d8c54`.

Les neuf constats REAUDIT-001 a REAUDIT-009 ont ete corriges dans l'application,
avec tests de regression et mise a jour des
[regles et procedures](../../specifications/securisation-production/contre-audit-integrite.md).
Le rapport d'audit initial reste conserve, sans modification retrospective.

## Corrections

| Constat | Correction | Commit |
|---|---|---|
| REAUDIT-001 | Activation serialisee, rejeu sans nouveaux droits ni email, unicite SQL des droits | `728be26` |
| REAUDIT-002 | Expiration sous verrou, report des instances occupees, exclusion des remboursements en cours | `6b06b4d` |
| REAUDIT-003 | Intention Stripe durable, reprise bornee, correlation du webhook apres perte de reponse | `06ce176` |
| REAUDIT-004 | Relecture sous verrou apres appel Stripe, conservation des confirmations et inversions | `27aa970` |
| REAUDIT-005 | Retrait de l'index historique global, maintien de l'unicite de la validation active | `f83bdbc` |
| REAUDIT-006 | Activation depuis la composition, les versions et la duree vendues, y compris les gains Animation | `30b0349` |
| REAUDIT-007 | Tentatives OTP persistees avant reponse d'erreur, quota de cinq effectif | `8368aa7` |
| REAUDIT-008 | Controle du partenaire et de la commune active avant reservation de credit | `1a7beb6` |
| REAUDIT-009 | Capture du credit exigee avant confirmation des lots, rejeu sans second debit | Commit contenant ce rapport |

## Validation

- Suite globale : **2403 tests reussis**, 40 ignores dans ce passage sans PostgreSQL.
- Integrite, contre-audit et ERP sur PostgreSQL : **32 tests reussis**.
- Securite et parcours admin sur PostgreSQL : **4 tests reussis**.
- Migrations sur base vide, rejeu, atomicite et concurrence : **3 tests reussis**.
- Dernier complement REAUDIT-009 sur les verrous d'expiration : **2 tests reussis**
  (reexecution ciblee de cas deja comptes dans la campagne d'integrite).
- Compilation des fichiers Python modifies et verification des espaces Git : OK.

Les 39 recettes PostgreSQL ignorees dans la suite globale ont donc ete executees
separement. Seule la campagne de performance en volume, qui exige une activation
explicite, n'a pas ete lancee. Aucun echec de test ne reste ouvert.

Deux attentes anciennes de recette ont ete alignees sur les regles deja
specifiees : refus de FINANCE sur SQLAdmin (DATA-008), et obligation du schema
public pour les migrations (DATA-015). La recette de serialisation des runners
est conservee sur une base public jetable ; une autre recette verifie le refus
sans effet de bord d'un schema prive. Aucun droit applicatif n'a ete elargi.

Les recettes de concurrence utilisent plusieurs transactions PostgreSQL reelles.
Les appels Stripe, emails et autres fournisseurs externes utilisent des doubles de
test : aucun paiement ou message reel n'a ete emis. PostgreSQL 11 local et jetable
est le moteur disponible pour ces recettes ; elles ne constituent pas une recette
du prestataire Stripe ou de l'environnement de production.

Commandes reproductibles depuis la racine, avec un Python contenant les dependances :

```powershell
python scripts/validation/test_isolated.py -q tests -rs
python scripts/validation/test_isolated.py -q tests/integration/test_data_integrity.py tests/integration/test_reaudit_integrity.py tests/integration/test_epic60_erp.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55437/localeo_audit_test
python scripts/validation/test_isolated.py -q tests/security/test_postgres_audit_integration.py tests/integration/test_admin_route_accessibility.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55437/localeo_audit_test
python scripts/validation/test_isolated.py -q tests/integration/test_data015_migrations.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55437/localeo_audit_migrations_test
```

La derniere commande exige une base dediee initialement vide. Les fixtures refusent
un schema preexistant et ne nettoient que leur environnement de recette.

## Deploiement et dossiers historiques

Trois migrations correctives sont ajoutees, sans modifier les migrations deja
appliquees : v221 (unicite des droits), v222 (intention de remboursement) et v223
(index de validation historique). Utiliser le runner de migrations habituel.

Avant deploiement, inventorier les droits dupliques : v221 s'arrete volontairement
sans suppression de donnees si des doublons sont presents. Le rapprochement doit
preserver les consommations et leurs preuves.

Decisions conservatrices retenues :

- Une activation rejouee conserve les tokens existants ; sa reponse ne recree pas
  le lien secret de consultation. L'email initial reste la reference.
- Une demande de remboursement incertaine sans intention historique, trop ancienne
  (23 heures), ou avec une reference fournisseur deja connue exige un rapprochement.
  Ne pas changer la cle d'idempotence ni rajeunir sa date pour forcer une creation.
  Stripe peut supprimer ses cles apres au moins 24 heures :
  [documentation Stripe](https://docs.stripe.com/api/idempotent_requests).
- Un snapshot de vente incomplet bloque l'activation. Les conditions historiques
  doivent etre etablies depuis les preuves de vente, sans recours silencieux au
  catalogue actuel.
- Une commande de lots insuffisamment financee n'est pas confirmee. Rapprocher le
  paiement et le credit, puis rejouer le webhook ; ne pas forcer le statut PAYEE.

Le code et les migrations sont livres dans Git. Aucun deploiement ni correction
de donnees historiques d'un environnement distant n'a ete effectue.
