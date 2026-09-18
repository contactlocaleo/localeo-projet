# Rapport de correction de l'audit d'integrite des donnees

Date : 6 septembre 2026.

Reference : [audit initial](audit-integrite-donnees-preproduction-2026-09-06.md),
realise sur le commit `0e386a2`. Le diagnostic initial est conserve sans modification
retroactive. Les regles et recettes detaillees figurent dans la
[specification des corrections](../../specifications/securisation-production/integrite-donnees.md).

## Traitement des constats

Les 16 constats sont traites. Chaque correction a ete validee par les tests
pertinents avant son commit. Trois complements de tests ont ensuite ete commites
separement, avec l'identifiant du constat concerne, lors de la non-regression globale.

| Constat | Correction livree | Commit principal |
|---|---|---|
| DATA-001 | Finalisation commune, atomique et rejouable des remboursements synchrones et asynchrones | `fdf8a9f` |
| DATA-002 | Financement mixte complet exige avant confirmation ; incident explicite si le credit manque ou expire | `1ddc65a` |
| DATA-003 | Remboursement Stripe limite a sa part encaissee ; restitution distincte du credit | `5116a79` |
| DATA-004 | Intention de transfer durable avant appel Stripe ; reprise avec requete et cle identiques | `148f54e` |
| DATA-005 | Verrou commun entre consommation et remboursement ; gel durable pendant le remboursement | `950535b` |
| DATA-006 | Calcul du reversement depuis la version vendue de la prestation | `68d10cd` |
| DATA-007 | Occurrences de validation historisees ; annulation puis nouvelle validation possibles sans ancien rejeu | `a7baf41` |
| DATA-008 | Controle serveur des roles sur les acces historiques, DAM et documents | `4f34f29` |
| DATA-009 | Commandes administratives en POST ; anciennes URLs GET limitees a une confirmation sans effet | `53b5a5e` |
| DATA-010 | Conservation du binaire lors d'un remplacement ou d'une suppression logique, y compris apres rollback | `66f671c` |
| DATA-011 | Immutabilite des documents probants et controle des delais de conservation | `1900f78` |
| DATA-012 | Cloture de l'instance apres ses deux dernieres consommations concurrentes, via le verrou DATA-005 | `0154022` |
| DATA-013 | Publication unique par type/scope, protegee par transaction et contrainte SQL | `7f4ec6c` |
| DATA-014 | Reservation exclusive des emails/SMS, reprise des reservations abandonnees et controle du proprietaire | `0941d1e` |
| DATA-015 | Socle SQL autonome sur base vide ; migrations suivies et transactionnelles | `ad2c1e8` |
| DATA-016 | Architecture alignee sur l'ADR Stripe Connect, avec renvoi vers la procedure applicable | Commit contenant ce rapport |

Complements de tests : `99cd753` (DATA-002), `5f3d047` (DATA-008),
`092c11a` (DATA-013). Aucun historique de migration deja applique n'a ete modifie.

## Validation

La suite generale isolee termine avec **2 391 tests reussis, 28 ignores et aucun
echec**. Les quatre avertissements concernent des deprecations existantes.
Les tests d'integration exigeant une base explicite sont executes separement.

Les **21 tests PostgreSQL d'integrite et ERP reussissent** : 13 scenarios couvrent
les corrections et 8 les parcours ERP existants. Les 23 avertissements concernent
le cycle connu des cles etrangeres des profils dans la fixture et des deprecations.
Les essais incluent les contentions reelles, la revalidation, les publications
concurrentes, les rollbacks documentaires et les reservations email/SMS.

La recette du gestionnaire de migrations termine avec **10 tests reussis**, dont
deux sur une seconde base PostgreSQL initialement vide : installation complete,
presence des tables et colonnes ORM, second passage sans operation, dry-run sans
ecriture et rollback d'une migration contenant un COMMIT puis une erreur.

Commandes de recette (interpreter Python de l'environnement de test) :

```powershell
python scripts/validation/test_isolated.py -q tests --tb=short --show-capture=no
python scripts/validation/test_isolated.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55437/localeo_audit_test -q tests/integration/test_data_integrity.py tests/integration/test_epic60_erp.py
python scripts/validation/test_isolated.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55437/localeo_audit_migrations_test -q tests/integration/test_data015_migrations.py tests/scripts/test_apply_migrations.py
```

Les deux bases ci-dessus sont exclusivement des bases locales jetables. Le runner
interdit les bases externes et ignore les fichiers dotenv de l'application.

Les appels Stripe, Brevo et stockage sont simules. Les essais SQL utilisent une
instance PostgreSQL 11 locale jetable ; ils ne constituent pas une recette de
l'environnement deploye ni de sa version PostgreSQL. Aucun envoi reel de message
ni aucune operation financiere externe n'a ete execute.

## Decisions et consequences d'exploitation

- Les ecrans historiques sans cloisonnement communal sont reserves au role ADMIN.
  Les autres profils utilisent les parcours ERP controles ; ils ne conservent pas
  un acces implicite aux anciennes vues globales.
- Un financement mixte tardif dont le credit n'est plus capturable reste en
  reconciliation, sans creation de droits. Les reservations restent limitees a
  30 minutes.
- Une intention Stripe inconnue ou agee de plus de 23 heures exige un rapprochement.
  La campagne ne fabrique pas une nouvelle cle pour contourner cette limite.
- Une version vendue absente bloque la consommation. Les anciennes transactions
  QR sans association fiable a une occurrence exigent un nouveau scan.
- Les fichiers physiques restent conserves apres suppression logique ou
  remplacement. Aucune purge automatique n'est introduite ; surveiller le volume
  stocke. Sans dates permettant de prouver l'expiration du delai de conservation,
  un document probant reste conserve.
- Une publication couvrant plusieurs scopes est archivee entierement lorsqu'une
  nouvelle publication remplace l'un de ses scopes. Le fichier source archive
  d'un HTML public reste accessible via ce document publie.
- Les outbox garantissent une reservation exclusive, avec reprise apres dix
  minutes et plafond de cinq tentatives. La livraison reste au moins une fois :
  une acceptation fournisseur dont la reponse est perdue peut etre suivie d'un
  nouvel envoi. Aucune garantie exactement une fois n'est revendiquee.

## Mise en service et donnees historiques

Appliquer les migrations avec `scripts/database/apply_migrations.py` avant le demarrage
des workers, notamment `v219` (occurrences de validation) et `v220` (unicite des
publications). Sur base vide, le runner utilise le nouveau socle fige
`baseline_v147.sql` puis la chaine suivante. Le schema cible est `public`.
Voir le [guide d'exploitation](../../exploitation/technique/reference-guide-exploitation-plateforme.md).

La migration v219 date la reprise des anciennes validations deja annulees ; cette
date ne remplace pas une date historique d'audit. La migration v220 conserve la
publication la plus recente en cas de conflit historique et archive les autres.

Les remboursements historiques deja confirmes avec des droits encore actifs,
les financements incomplets et les droits sans version vendue doivent etre
inventories dans l'environnement concerne puis rapproches avec leurs preuves.
Aucune correction de donnees distantes n'a ete executee dans cette intervention.
Les corrections de code et les migrations sont livrees ; leur deploiement et
la verification des fournisseurs reels restent des operations distinctes.
